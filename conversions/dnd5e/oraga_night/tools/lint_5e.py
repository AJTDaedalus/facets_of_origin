"""Style linter for the Oraga Night 5e module (DESIGN_oraga_5e_official §4).

Usage (from the repo root):
    python conversions/dnd5e/oraga_night/tools/lint_5e.py            # hits + summary
    python conversions/dnd5e/oraga_night/tools/lint_5e.py --report   # summary tables only
    python conversions/dnd5e/oraga_night/tools/lint_5e.py --baseline # write lint_baseline.json
    python conversions/dnd5e/oraga_night/tools/lint_5e.py --check    # compare to the baseline
    ... --file 04_The_Ball.md                                         # one file only

Rule families
    hard       counts that must reach 0 (role name, rules-term capitals, check/save/damage
               grammar, conversion talk, narrator voice, designer "we", "Deadly" budgets,
               PCs, spelled distances, gp, British spelling, grey, Designer's note, the
               removed Attendant habit)
    soft       per-file metrics with targets (sentence length, em dashes, long paragraphs)
               and counts ("the players", "player character", "you", "perhaps",
               rhetorical questions, "not X but Y")
    structure  cross-references resolve, bold creature names have stat blocks, every
               read-aloud box has a trigger line

--check fails (exit 1) on any hard or structure hit that is not in the baseline, and on
any soft regression: a targeted metric that got worse by more than its tolerance while
above its target, or a count (other than "you") that went up. Hits going down never
fail. "you" is reported but never fails, because the DM swap (§3) adds legitimate ones.
After a task that moves text between files, re-run --baseline and say so in the LOG.

Whitelist: tools/lint_5e_allow.txt, one `file|quoted text|reason` per line (`*` = any
file). A line containing the quoted text is exempt from every rule.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, namedtuple
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
MODULE = TOOLS.parent
ALLOW = TOOLS / "lint_5e_allow.txt"
BASELINE = TOOLS / "lint_baseline.json"
EXCLUDE = {"INVENTIONS_5e.md", "STYLE_5e.md"}

Hit = namedtuple("Hit", "file line family rule match")
AllowEntry = namedtuple("AllowEntry", "file text reason")

ABIL = r"(?:Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
SKILL = (r"(?:Perception|Insight|Investigation|Persuasion|Deception|Intimidation|Stealth|"
         r"Athletics|Acrobatics|Arcana|History|Religion|Nature|Survival|Medicine|Performance|"
         r"Sleight of Hand|Animal Handling)")
DTYPE = (r"(?:acid|bludgeoning|cold|fire|force|lightning|necrotic|piercing|poison|psychic|"
         r"radiant|slashing|thunder)")
CONDITIONS = (r"(?:blinded|charmed|deafened|frightened|grappled|incapacitated|invisible|"
              r"paralyzed|petrified|poisoned|prone|restrained|stunned|unconscious)")
ACTIONS = r"(?:attack|dash|disengage|dodge|help|hide|influence|magic|ready|search|study|utilize)"
NUMWORDS = (r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
            r"twenty-five|thirty|forty|fifty|sixty|ninety|hundred)")

# ---------------------------------------------------------------------------------------
# Line classes


def classify(text: str, fname: str = "") -> list[str]:
    """One kind per line: blank, heading, table, rule, code, statblock, readaloud, prose.

    readaloud: a blockquote block whose first content line starts with a single `*`
    (the indented italic box), or an italic paragraph inside any other blockquote.
    statblock: from an H2/H3 whose next few lines carry `**AC**` to the next `---` or H2.
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    kinds = ["prose"] * len(lines)
    in_code = in_stat = False
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            in_code = not in_code
            kinds[i] = "code"
            i += 1
            continue
        if in_code:
            kinds[i] = "code"
            i += 1
            continue
        if re.match(r"^#{1,6} ", ln):
            kinds[i] = "heading"
            if ln.startswith("## ") or ln.startswith("# "):
                in_stat = False
            if re.match(r"^#{2,3} ", ln):
                ahead = "\n".join(lines[i + 1:i + 8])
                if "**AC**" in ahead:
                    in_stat = True
            i += 1
            continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", ln):
            kinds[i] = "rule"
            in_stat = False
            i += 1
            continue
        if not s:
            kinds[i] = "blank"
            i += 1
            continue
        if in_stat:
            kinds[i] = "statblock"
            i += 1
            continue
        if s.startswith("|"):
            kinds[i] = "table"
            i += 1
            continue
        if ln.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            block = [re.sub(r"^>\s?", "", x) for x in lines[i:j]]
            first = next((b for b in block if b.strip()), "")
            whole = bool(re.match(r"^\*[^*]", first.strip()))
            para_italic = False
            for k, b in enumerate(block):
                if not b.strip():
                    kinds[i + k] = "blank"
                    para_italic = False
                    continue
                prev_blank = k == 0 or not block[k - 1].strip()
                if prev_blank or re.match(r"^\*[^*]", b.strip()):
                    para_italic = bool(re.match(r"^\*[^*]", b.strip())) or (
                        not prev_blank and para_italic)
                if whole or para_italic:
                    kinds[i + k] = "readaloud"
                else:
                    kinds[i + k] = "prose"
            i = j
            continue
        i += 1
    return kinds


def strip_quotes(s: str) -> str:
    """Blank out quoted speech so prose rules do not read NPC dialogue."""
    s = re.sub(r"“[^”]*”", lambda m: " " * len(m.group()), s)
    return re.sub(r'"[^"]*"', lambda m: " " * len(m.group()), s)


def body(line: str) -> str:
    return re.sub(r"^>\s?", "", line)


# ---------------------------------------------------------------------------------------
# Whitelist


def load_allow(path) -> list[AllowEntry]:
    out = []
    p = Path(path)
    if not p.exists():
        return out
    for n, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("|")
        if len(parts) < 3 or not parts[0].strip() or not parts[1]:
            raise ValueError(f"{p}:{n}: expected 'file|quoted text|reason', got {raw!r}")
        out.append(AllowEntry(parts[0].strip(), parts[1], "|".join(parts[2:]).strip()))
    return out


def is_allowed(fname: str, line: str, allow) -> bool:
    return any((e.file == "*" or e.file == fname) and e.text in line for e in allow)


# ---------------------------------------------------------------------------------------
# Hard rules: (family, rule id, pattern, scope, flags)
#   scope ALL     every line
#   scope NOBOX   every line except read-aloud
#   scope SPEECH  NOBOX, with quoted speech blanked out
#   scope TEXT    SPEECH, and not in tables


I = re.I
RULES = [
    ("role_name", "MM", r"\bMM\b", "ALL", 0),
    ("role_name", "Mirror Master", r"\bMirror Master\b", "ALL", 0),
    ("lowercase_terms", "terms",
     r"\b(?:advantage|disadvantage|temporary hit points|hit points?|short rests?|long rests?|"
     r"difficult terrain|dim light|bright light|heavily obscured|lightly obscured|"
     r"half cover|three-quarters cover|bloodied|heroic inspiration|opportunity attacks?)\b",
     "SPEECH", 0),
    ("lowercase_terms", "condition", CONDITIONS + r" condition\b", "SPEECH", 0),
    ("lowercase_terms", "prone/unconscious",
     r"\b(?:is|are|falls?|knocked|lands?|becomes?|left|drops?) (?:prone|unconscious)\b", "SPEECH", 0),
    ("lowercase_terms", "stable", r"\b(?:and|is|are|becomes?) stable\b", "SPEECH", 0),
    ("lowercase_terms", "action", r"\b" + ACTIONS + r" action\b", "SPEECH", 0),
    ("lowercase_terms", "speed", r"\b(?:its|their|your|his|her|half) speed\b", "SPEECH", 0),
    ("bare_dc", "S5 range", r"\bDC ?\d+ ?[–-] ?\d+", "NOBOX", 0),
    ("bare_dc", "S5 approx", r"\bDC (?:of )?(?:about|around|~)", "NOBOX", 0),
    ("bare_dc", "S3 skill only", r"\bDC ?\d+ " + SKILL + r" (?:check|roll)", "NOBOX", 0),
    ("bare_dc", "S4 skill check", r"\b(?:an?|the) " + SKILL + r" (?:check|roll)\b", "NOBOX", 0),
    ("bare_dc", "bare", None, "NOTABLE", 0),          # handled in code
    ("roll_check", "S6 roll ability", r"\b(?:roll|rolls|rolling) (?:a |an |the )?" + ABIL + r"\b", "NOBOX", 0),
    ("roll_check", "S6 skill roll", r"\b" + SKILL + r" rolls?\b", "NOBOX", 0),
    ("roll_check", "S6 roll the ability", r"\broll (?:the )?(?:ability|skill)\b", "NOBOX", 0),
    ("roll_check", "S7 beat the DC",
     r"\b(?:beat|beats|beating|pass|passes|passing|meet|meets|hit|hits|miss|misses|missed) "
     r"(?:the |a |its |their )?DC\b", "NOBOX", 0),
    ("save_damage", "S8 save demand",
     r"\b(?:make|makes|making|attempt|attempts) a DC ?\d+ " + ABIL + r" save\b", "NOBOX", 0),
    ("save_damage", "S9 failed saving throw", r"\bon a (?:failed|successful) saving throw\b", "NOBOX", 0),
    ("save_damage", "S10 half", r"\bhalf (?:damage )?on a (?:success\b|successful save)|\bhalf as much on\b", "NOBOX", 0),
    ("save_damage", "S11 bare dice", r"\b(?:takes|taking|deals|dealing|take|deal) \d+d\d+", "NOBOX", 0),
    ("save_damage", "S12 type missing", r"\b\d+ \(\d+d\d+(?: ?[+−-] ?\d+)?\) damage\b", "NOBOX", 0),
    ("save_damage", "S12 type lowercase", r"\b\d+ \(\d+d\d+(?: ?[+−-] ?\d+)?\) " + DTYPE + r" damage\b", "NOBOX", 0),
    ("conversion_talk", "talk",
     r"\bthe source\b|\bthe original\b|\bthis edition\b|\(source Ch|\bNew in this edition\b", "NOBOX", I),
    ("narrator_voice", "module", r"\bthe module (?:would|notes|suggests|prefers|intends|has spent)\b", "NOBOX", I),
    ("narrator_voice", "honest", r"\bHonest (?:note|warning)\b", "NOBOX", I),
    ("designer_we", "S28", r"\b(?:we|We|our|Our|us|Us|ours)\b", "SPEECH", 0),
    ("deadly_budget", "S34", r"\bDeadly\b", "NOBOX", 0),  # line filter in code
    ("pcs", "S1", r"\bPCs?\b", "NOBOX", 0),
    ("spelled_distance", "S37", r"\b" + NUMWORDS + r"(?: |-)(?:feet|foot)\b", "SPEECH", I),
    ("gp", "gp", r"\bgp\b", "ALL", 0),
    ("british_spelling", "BALL-22",
     r"\b(?:colour(?:s|ed|ful|ing)?|rumour(?:s|ed)?|centre(?:s|d)?|labell(?:ed|ing)|"
     r"recognis(?:e|es|ed|ing)|realis(?:e|es|ed|ing)|organis(?:e|es|ed|ing|ation)|"
     r"apologis(?:e|es|ed|ing)|honour(?:s|ed|able)?|favour(?:s|ed|ite|able)?|armour(?:ed)?|"
     r"behaviour(?:s)?|neighbour(?:s|ing)?|travell(?:ed|ing|er|ers)|cancell(?:ed|ing)|"
     r"defence|offence)\b", "ALL", I),
    ("grey", "grey", r"\bgrey\b", "ALL", I),
    ("designers_note", "designer's note", r"\bDesigner['’]s note\b", "ALL", I),
    ("attendant_habit", "Q5", r"\bdirect question\b|\bliterally and truthfully\b", "ALL", I),
]
HARD_FAMILIES = list(dict.fromkeys(r[0] for r in RULES))
_COMPILED = [(f, rid, re.compile(p, fl) if p else None, sc) for f, rid, p, sc, fl in RULES]

_DC = re.compile(r"\bDC ?(\d+)")
_DC_OK_AFTER = re.compile(
    r"^ " + ABIL + r"(?: \([^)]*\))?"
    r"(?:,? or (?:a )?(?:DC \d+ )?" + ABIL + r"(?: \([^)]*\))?)*"
    r" (?:checks?|saving throws?|save)\b")
_DC_SAVE_FORM = re.compile(r"(?:Saving Throw:\*?|save) $", re.I)
_BUDGET_LINE = re.compile(r"\bXP\b|budget|\bLow\b|\bModerate\b|\bHigh\b|multiplier|difficulty", re.I)
_IDIOM_BEFORE = re.compile(r"(?:\btakes? |\btaking |\bto (?:his|her|their|its|your|our|my) |\bat a )$")
_FALL = re.compile(r"\b(?:fall|falls|falling|fell|drop|drops|plunge|pushed over)\b", re.I)


def _scoped(line: str, kind: str, scope: str):
    """Text a rule of this scope sees on this line, or None to skip."""
    if scope == "ALL":
        return line
    if kind == "readaloud":
        return None
    if scope == "NOBOX":
        return body(line)
    if scope == "SPEECH":
        return strip_quotes(body(line))
    if scope == "NOTABLE":
        return None if kind == "table" else body(line)
    raise ValueError(scope)


def _bare_dc_hits(s: str):
    for m in _DC.finditer(s):
        before, after = s[:m.start()], s[m.end():]
        if _DC_SAVE_FORM.search(before):
            continue
        if re.match(r"^ ?[–-] ?\d", after):
            continue  # reported as a range
        if re.match(r"^ " + SKILL + r" (?:check|roll)", after):
            continue  # reported by S3
        if _DC_OK_AFTER.match(after):
            continue
        # a chain "DC 15 Intelligence (Religion) or DC 15 Charisma (Persuasion) check":
        # an earlier DC in the chain is fine if the chain ends in "check"
        am = re.match(r"^ " + ABIL + r"(?: \([^)]*\))?", after)
        yield m.start(), m.group() + (am.group() if am else "")


def lint_hard(text: str, fname: str, allow=()) -> list[Hit]:
    kinds = classify(text, fname)
    lines = text.split("\n")
    hits = []
    for n, (line, kind) in enumerate(zip(lines, kinds), 1):
        if kind in ("blank", "code", "rule") or is_allowed(fname, line, allow):
            continue
        for family, rid, rx, scope in _COMPILED:
            if kind == "heading" and scope != "ALL" and family not in ("pcs", "conversion_talk"):
                continue
            s = _scoped(line, kind, scope)
            if s is None:
                continue
            if rx is None:  # bare DC; read on into the next line so a wrapped
                # "DC 15 Strength\nsaving throw" is not a false hit
                nxt = lines[n] if n < len(lines) and n < len(kinds) and kinds[n] == kind else ""
                joined = s + " " + body(nxt).strip() if nxt.strip() else s
                for col, mt in _bare_dc_hits(joined):
                    if col >= len(s):
                        continue
                    mt = mt if col + len(mt) <= len(s) else s[col:].rstrip()
                    r = "no 'check'" if re.search(ABIL, mt) else "bare"
                    hits.append((n, col, Hit(fname, n, family, r, mt)))
                continue
            if family == "deadly_budget" and not _BUDGET_LINE.search(s):
                continue
            for m in rx.finditer(s):
                g = m.group()
                if family == "lowercase_terms" and g in ("advantage", "disadvantage"):
                    if _IDIOM_BEFORE.search(s[:m.start()]) or s[m.end():].startswith(" of "):
                        continue
                if rid == "S11 bare dice" and _FALL.search(s[max(0, m.start() - 160):m.start()]):
                    continue
                hits.append((n, m.start(), Hit(fname, n, family, rid, g)))
    hits.sort(key=lambda t: (t[0], t[1]))
    return [t[2] for t in hits]


# ---------------------------------------------------------------------------------------
# Soft metrics

TARGETS = {"mean_wps": 19.0, "long_sentence_pct": 12.0, "emdash_per_k": 8.0, "long_paras": 3}
TOLERANCE = {"mean_wps": 0.3, "long_sentence_pct": 0.5, "emdash_per_k": 0.3, "long_paras": 0}
COUNTS = ["the_players", "player_character", "you", "perhaps", "rhetorical", "not_but"]
INFO_ONLY = {"you"}
_ABBR = re.compile(r"\b(?:ft|e\.g|i\.e|etc|vs|Mr|Mrs|Ms|St|No|Ch|cf|approx)\.", re.I)
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’,.\-]*")
_SOFT = {
    "the_players": re.compile(r"\b[Tt]he players\b"),
    "player_character": re.compile(r"\b[Pp]layer characters?\b"),
    "you": re.compile(r"\b[Yy]ou(?:r|rs|rself|rselves)?\b"),
    "perhaps": re.compile(r"\b[Pp]erhaps\b"),
    "not_but": re.compile(r"\bnot\b[^.;:!?]{1,60}?\bbut\b|, not\b"),
}


def _words(s: str) -> int:
    return len(_WORD.findall(s))


def _sentences(s: str, semicolon=False):
    s = _ABBR.sub(lambda m: m.group().replace(".", "§"), s)
    s = re.sub(r"(\d)\.(\d)", r"\1§\2", s)
    pat = r"(?<=[.!?])[*_)\"”’]*\s+|(?<=[.!?])[*_)\"”’]*$"
    if semicolon:
        pat = r";\s+|" + pat
    return [x for x in re.split(pat, s) if x and _words(x)]


def _paragraphs(text: str, fname: str, allow):
    """(heading context, paragraph text) for DM prose, list items separate."""
    kinds = classify(text, fname)
    lines = text.split("\n")
    heading, cur, out = "", [], []

    def flush():
        if cur:
            out.append((heading, " ".join(cur)))
            cur.clear()

    for line, kind in zip(lines, kinds):
        if kind == "heading":
            flush()
            heading = line
            continue
        if kind != "prose" or is_allowed(fname, line, allow):
            flush()
            continue
        b = body(line).strip()
        if re.match(r"^(?:[-*+]|\d+\.) ", b) and not b.startswith("**"):
            flush()
            b = re.sub(r"^(?:[-*+]|\d+\.) ", "", b)
        cur.append(b)
    flush()
    return out


def soft_metrics(text: str, fname: str, allow=()) -> dict:
    paras = _paragraphs(text, fname, allow)
    words = sents = long_s = dashes = long_p = 0
    counts = Counter()
    for heading, p in paras:
        w = _words(p)
        words += w
        dashes += p.count("—")
        if w > 120 and "background" not in heading.lower():
            long_p += 1
        ss = _sentences(p)
        sents += len(ss)
        long_s += sum(1 for x in _sentences(p, semicolon=True) if _words(x) > 30)
        q = strip_quotes(p)
        for k, rx in _SOFT.items():
            counts[k] += len(rx.findall(q))
        counts["rhetorical"] += sum(1 for x in _sentences(q) if x.rstrip("*_ ").endswith("?"))
    semi_sents = sum(len(_sentences(p, semicolon=True)) for _, p in paras)
    return {
        "words": words,
        "sentences": sents,
        "mean_wps": round(words / sents, 2) if sents else 0.0,
        "long_sentence_pct": round(100.0 * long_s / semi_sents, 2) if semi_sents else 0.0,
        "emdash_per_k": round(1000.0 * dashes / words, 2) if words else 0.0,
        "long_paras": long_p,
        **{k: counts[k] for k in COUNTS},
    }


# ---------------------------------------------------------------------------------------
# Structure

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
         "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15}
CREATURE_FILES = ("04_The_Ball.md", "05_The_Longest_Night.md", "09_The_Snakes.md")
NOT_CREATURES = {"nastier", "low", "moderate", "high", "beyond high", "focused", "idle"}


def _norm(s: str) -> str:
    s = re.sub(r"[*_`\"“”'’]", "", s).lower()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _singular(w: str) -> str:
    for a, b in (("knives", "knife"), ("men", "man"), ("ies", "y"), ("ches", "ch"),
                 ("shes", "sh"), ("sses", "ss")):
        if w.endswith(a):
            return w[: -len(a)] + b
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def _creature_key(s: str) -> str:
    n = _norm(s)
    n = re.sub(r"^(?:\d+|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) ", "", n)
    n = re.sub(r"^the ", "", n)
    return " ".join(_singular(w) for w in n.split())


def module_files(module: Path):
    return sorted(p for p in Path(module).glob("*.md") if p.name not in EXCLUDE)


def _index(module: Path):
    chapters, tables, areas, cards, heads10 = {}, set(), set(), set(), set()
    for p in module_files(module):
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# ([IVX]+)\.", text, re.M)
        names = set()
        for m in re.finditer(r"^#{1,6} (.+)$", text, re.M):
            names.add(_norm(m.group(1)))
            am = re.match(r"(B\d+)\.", m.group(1))
            if am:
                areas.add(am.group(1))
            cm = re.match(r"(S\d+)\.", m.group(1))
            if cm and p.name.startswith("09"):
                cards.add(cm.group(1))
            if p.name.startswith("10") and re.match(r"^#{2,3} ", m.group(0)):
                heads10.add(_creature_key(m.group(1)))
        for m in re.finditer(r"\*\*([^*]{2,80}?)[.:]?\*\*", text):
            names.add(_norm(m.group(1)))
        for m in re.finditer(r"\*\*(B\d+)\.", text):
            areas.add(m.group(1))
        for m in re.finditer(r"^\*\*Table ([IVX]+)[–-](\d+)", text, re.M):
            tables.add(f"{m.group(1)}–{m.group(2)}")
        if h1:
            chapters[h1.group(1)] = names
    return chapters, tables, areas, cards, heads10


_XCH = re.compile(r"(?<!source )\b(?:[Cc]hapter|Ch\.)\s+([IVX]+)\b"
                  r"(?:,\s+(?:\"([^\"]+)\"|“([^”]+)”|\*([^*]+)\*))?")
_XCARD = re.compile(r"\b[Cc]ards?:?\s+(S\d+(?:(?:,\s*|\s+and\s+|\s+or\s+|\s*/\s*)S\d+)*)")
_XAREA = re.compile(r"\bB\d{1,2}\b")
_XTABLE = re.compile(r"\bTable\s+([IVX]+)[–-](\d+)\b")


def lint_structure(module: Path, allow=(), only=None) -> list[Hit]:
    module = Path(module)
    chapters, tables, areas, cards, heads10 = _index(module)
    hits = []
    for p in module_files(module):
        if only and p.name != only:
            continue
        raw = p.read_text(encoding="utf-8")
        lines = raw.split("\n")
        kinds = classify(raw, p.name)
        kinds += ["blank"] * (len(lines) - len(kinds))
        keep = [("" if is_allowed(p.name, ln, allow) else body(ln)) for ln in lines]
        flat = "\n".join(keep)

        def at(pos):
            return flat.count("\n", 0, pos) + 1

        # cross-references
        for m in _XCH.finditer(flat):
            num, title = m.group(1), m.group(2) or m.group(3) or m.group(4)
            if num not in chapters:
                hits.append(Hit(p.name, at(m.start()), "structure", "xref", re.sub(r"\s+", " ", m.group())))
                continue
            if title:
                t = _norm(title)
                if t and not any(t in h for h in chapters[num]):
                    hits.append(Hit(p.name, at(m.start()), "structure", "xref", re.sub(r"\s+", " ", m.group())))
        for m in _XCARD.finditer(flat):
            for c in re.findall(r"S\d+", m.group(1)):
                if c not in cards:
                    hits.append(Hit(p.name, at(m.start()), "structure", "xref", f"card {c}"))
        for n, (ln, kind) in enumerate(zip(keep, kinds), 1):
            if kind == "statblock":
                continue
            for m in _XAREA.finditer(ln):
                if m.group() not in areas:
                    hits.append(Hit(p.name, n, "structure", "xref", f"area {m.group()}"))
            for m in _XTABLE.finditer(ln):
                key = f"{m.group(1)}–{m.group(2)}"
                if key not in tables and not ln.lstrip().startswith(f"**Table {m.group(1)}"):
                    hits.append(Hit(p.name, n, "structure", "xref", f"Table {key}"))

        # bold creature names at first mention
        if p.name in CREATURE_FILES:
            seen = set()
            for para_m in re.finditer(r"(?ms)^\*\*Enem(?:y|ies)\b[^*]*\*\*(.*?)(?:\n\s*\n|\Z)", flat):
                for bm in re.finditer(r"\*\*([^*]+?)\*\*", para_m.group(1)):
                    _creature_check(p.name, at(para_m.start(1) + bm.start()), bm.group(1),
                                    heads10, seen, hits)
            for bm in re.finditer(r"\*\*([^*]+?)\*\*\s*\((?:see\s+)?[Cc]hapter\s+X\)", flat):
                _creature_check(p.name, at(bm.start()), bm.group(1), heads10, seen, hits)

        # read-aloud trigger lines
        i = 0
        while i < len(lines):
            if kinds[i] == "readaloud" and lines[i].startswith(">") and (
                    i == 0 or not lines[i - 1].startswith(">")) and \
                    re.match(r"^\*[^*]", body(lines[i]).strip()):
                prev = [k for k in range(max(0, i - 2), i) if lines[k].strip()]
                ok = False
                if prev:
                    k = prev[-1]
                    t = lines[k].strip().rstrip("*_) ")
                    ok = kinds[k] == "prose" and not lines[k].startswith(">") and t.endswith(":")
                if not ok and not is_allowed(p.name, lines[i], allow):
                    snippet = " ".join(body(lines[i]).split()[:6])
                    hits.append(Hit(p.name, i + 1, "structure", "readaloud_trigger",
                                    f"untriggered read-aloud: {snippet}"))
            i += 1
    hits.sort(key=lambda h: (h.file, h.line))
    return hits


_CREATURE_SHAPE = re.compile(
    r"^(?:[Tt]he )?[A-Z][\w'’-]*(?: (?:of |the |and )?[A-Z][\w'’-]*){0,4}$")


def _creature_check(fname, line, name, heads10, seen, hits):
    name = name.strip()
    if re.search(r"\d", name) or not _CREATURE_SHAPE.match(name):
        return  # an XP figure, a budget, or a bolded sentence: not a creature name
    key = _creature_key(name)
    if not key or key in NOT_CREATURES or re.search(r"\d", key) or key in seen:
        return
    seen.add(key)
    if key not in heads10 and not any(h.endswith(" " + key) or key.endswith(" " + h) for h in heads10):
        hits.append(Hit(fname, line, "structure", "creature_bold", name.strip()))


# ---------------------------------------------------------------------------------------
# Running, baseline, check, report


def run(module=MODULE, files=None, allow=None) -> dict:
    module = Path(module)
    allow = load_allow(ALLOW) if allow is None else allow
    hard, soft = [], {}
    for p in module_files(module):
        if files and p.name not in files:
            continue
        text = p.read_text(encoding="utf-8")
        hard += lint_hard(text, p.name, allow)
        soft[p.name] = soft_metrics(text, p.name, allow)
    structure = []
    for f in (files or [None]):
        structure += lint_structure(module, allow, only=f)
    return {"hard": hard, "structure": structure, "soft": soft}


def _bucket(hits, key):
    out = {}
    for h in hits:
        r = out.setdefault(h.file, {}).setdefault(getattr(h, key), {})
        r[h.match] = r.get(h.match, 0) + 1
    return out


def make_baseline(rep: dict) -> dict:
    return {"version": 1,
            "hard": _bucket(rep["hard"], "family"),
            "structure": _bucket(rep["structure"], "rule"),
            "soft": rep["soft"]}


def compare(rep: dict, base: dict, files=None) -> list[str]:
    problems = []
    for kind, key in (("hard", "family"), ("structure", "rule")):
        now = _bucket(rep[kind], key)
        for f, fams in now.items():
            for fam, matches in fams.items():
                for mt, c in matches.items():
                    b = base.get(kind, {}).get(f, {}).get(fam, {}).get(mt, 0)
                    if c > b:
                        where = [h.line for h in rep[kind] if h.file == f and getattr(h, key) == fam and h.match == mt]
                        problems.append(f"NEW {kind} {f} {fam} {mt!r}: {c} now vs {b} in baseline (lines {where})")
    for f, m in rep["soft"].items():
        if files and f not in files:
            continue
        b = base.get("soft", {}).get(f)
        if b is None:
            problems.append(f"NEW file {f} has no soft baseline; re-run --baseline")
            continue
        for k, target in TARGETS.items():
            if m[k] > b.get(k, 0) + TOLERANCE[k] and m[k] > target:
                problems.append(f"SOFT {f} {k}: {m[k]} vs baseline {b.get(k)} (target {target})")
        for k in COUNTS:
            if k in INFO_ONLY:
                continue
            if m[k] > b.get(k, 0):
                problems.append(f"SOFT {f} {k}: {m[k]} vs baseline {b.get(k)}")
    return problems


def report_tables(rep: dict) -> str:
    files = sorted(rep["soft"])
    hb = Counter(h.file for h in rep["hard"])
    sb = Counter(h.file for h in rep["structure"])
    cols = ["file", "hard", "struct", "words", "wps", ">30%", "—/1k", "paras>120",
            "players", "pl.char", "you", "perhaps", "rq", "not…but"]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    tot = Counter()
    for f in files:
        m = rep["soft"][f]
        tot.update({"hard": hb[f], "struct": sb[f], **{k: m[k] for k in
                    ("words", "long_paras", *COUNTS)}})
        out.append("| " + " | ".join(str(x) for x in (
            f, hb[f], sb[f], m["words"], m["mean_wps"], m["long_sentence_pct"], m["emdash_per_k"],
            m["long_paras"], m["the_players"], m["player_character"], m["you"], m["perhaps"],
            m["rhetorical"], m["not_but"])) + " |")
    out.append("| " + " | ".join(str(x) for x in (
        "TOTAL", tot["hard"], tot["struct"], tot["words"], "", "", "", tot["long_paras"],
        tot["the_players"], tot["player_character"], tot["you"], tot["perhaps"],
        tot["rhetorical"], tot["not_but"])) + " |")
    out.append("")
    out.append(f"Targets: wps ≤ {TARGETS['mean_wps']:g}, >30-word sentences ≤ "
               f"{TARGETS['long_sentence_pct']:g}%, em dashes ≤ {TARGETS['emdash_per_k']:g}/1k, "
               f"paragraphs > 120 words ≤ {TARGETS['long_paras']} per file.")
    out.append("")
    fam = Counter(h.family for h in rep["hard"])
    fam.update(h.rule for h in rep["structure"])
    out.append("| family | hits |")
    out.append("|---|---|")
    for f in HARD_FAMILIES + ["xref", "creature_bold", "readaloud_trigger"]:
        out.append(f"| {f} | {fam[f]} |")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Oraga Night 5e style linter")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--baseline", action="store_true", help="write the baseline JSON")
    g.add_argument("--check", action="store_true", help="fail on new hits / soft regressions")
    ap.add_argument("--report", action="store_true", help="summary tables only")
    ap.add_argument("--file", help="limit to one module file (basename)")
    ap.add_argument("--module", default=str(MODULE), help=argparse.SUPPRESS)
    ap.add_argument("--baseline-path", default=str(BASELINE), help=argparse.SUPPRESS)
    ap.add_argument("--allow", default=str(ALLOW), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    files = [a.file] if a.file else None
    rep = run(Path(a.module), files, load_allow(a.allow))

    if a.baseline:
        if files:
            print("--baseline covers the whole module; drop --file", file=sys.stderr)
            return 2
        Path(a.baseline_path).write_text(json.dumps(make_baseline(rep), indent=1, sort_keys=True,
                                                    ensure_ascii=False) + "\n", encoding="utf-8")
        print(report_tables(rep))
        print(f"\nBaseline written to {a.baseline_path}")
        return 0
    if a.check:
        bp = Path(a.baseline_path)
        if not bp.exists():
            print(f"No baseline at {bp}; run --baseline first", file=sys.stderr)
            return 2
        probs = compare(rep, json.loads(bp.read_text(encoding="utf-8")), files)
        for x in probs:
            print(x)
        n_h, n_s = len(rep["hard"]), len(rep["structure"])
        print(f"lint_5e --check: {'FAIL' if probs else 'OK'} ({len(probs)} problem(s); "
              f"{n_h} hard and {n_s} structure hits remain)")
        return 1 if probs else 0
    if not a.report:
        for h in rep["hard"] + rep["structure"]:
            print(f"{h.file}:{h.line}: [{h.family if h.family != 'structure' else h.rule}] "
                  f"{h.rule}: {h.match}")
        print()
    print(report_tables(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
