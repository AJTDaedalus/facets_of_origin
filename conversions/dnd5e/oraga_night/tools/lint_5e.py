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
               removed Attendant habit; and from the review-fix pass, R0.2: emphasis
               italics, "(X or Y)" skills, HTML comments, repo file names, simulation
               jargon, wider conversion talk, anachronisms)
    soft       per-file metrics with targets (sentence length, em dashes, long paragraphs)
               and counts ("the players", "player character", "you", "perhaps",
               rhetorical questions, "not X but Y"); and the verbal tics (R5.3, O39): module-wide
               targets for "exactly", "the whole", "quietly", "out loud", "genuinely",
               "say so", "to everyone's permanent confusion" and "not X… but Y", counted per
               file outside read-aloud and quoted speech, with each file's budget (its
               proportional share of the cut) in the report. A tic count that goes up fails
               --check; allowlist rule `tics`
    structure  cross-references resolve, bold creature names have stat blocks, every
               read-aloud box has a trigger line in the pinned form "**Read this when …:**"
               (trigger_format), box labels are heading style (box_label), and every proper
               term used is glossed (defined_terms, against tools/terms.txt and the canon
               vocabulary of settings/valloh V0/V1/V3)
    near_duplicate  the R5.2 soft rule (O38): no paragraph in one chapter is more than 80%
               similar (difflib ratio over words) to a paragraph in another chapter. A
               repeat belongs in one home with pointers elsewhere; a deliberate repeat (a
               canon line reused on purpose) is whitelisted with its reason. Reported with
               the structure rules so --check fails on a new one.

The hard rules run on unwrapped paragraphs (unwrap()), so a phrase split across a hard
line break is seen; a hit is reported at the line where its match starts.

--check fails (exit 1) on any hard or structure hit that is not in the baseline, and on
any soft regression: a targeted metric that got worse by more than its tolerance while
above its target, or a count (other than "you") that went up. Hits going down never
fail. "you" is reported but never fails, because the DM swap (§3) adds legitimate ones.
After a task that moves text between files, re-run --baseline and say so in the LOG.

Whitelist: tools/lint_5e_allow.txt, one `file|rule|quoted text|reason` per line (`*` file =
any file). An entry exempts only hits of its rule (family or rule id; `soft` for the soft
metrics) and only where its quoted text overlaps the hit. Rule `*` exempts every rule and is
reserved for fixed canonical text.
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
TERMS = TOOLS / "terms.txt"
SETTINGS = MODULE.parents[2] / "settings" / "valloh"
BASELINE = TOOLS / "lint_baseline.json"
EXCLUDE = {"INVENTIONS_5e.md", "STYLE_5e.md"}

Hit = namedtuple("Hit", "file line family rule match")
AllowEntry = namedtuple("AllowEntry", "file rule text reason")

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
# Unwrapping: hard-wrapped lines joined into the paragraphs Markdown renders


Block = namedtuple("Block", "text kind lines offsets quoted")
_LIST_ITEM = re.compile(r"^(?:[-*+]|\d+\.) ")


def unwrap(text: str, fname: str = "", kinds=None) -> list[Block]:
    """Paragraph blocks, each with the source line of every piece joined into it.

    A block is a run of non-blank lines of one kind (classify). Headings and table rows are
    one block per line. A list item starts a new block; so do a change into or out of a
    blockquote, a bold field label inside a blockquote or stat block (``**Wants.**``,
    ``**AC**``), and the line after a Markdown hard break. Blockquote markers and
    indentation are stripped and the pieces joined with one space, so a phrase split across
    a line break reads as one string.
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    kinds = kinds if kinds is not None else classify(text, fname)
    out, cur = [], None
    hard_break = False

    def flush():
        nonlocal cur
        if cur:
            out.append(Block(" ".join(cur["pieces"]), cur["kind"], cur["lines"], cur["offsets"],
                             cur["quoted"]))
        cur = None

    for i, (ln, kind) in enumerate(zip(lines, kinds)):
        if kind in ("blank", "code", "rule"):
            flush()
            hard_break = False
            continue
        quoted = ln.startswith(">")
        piece = body(ln).strip() if quoted else ln.strip()
        if not piece:
            flush()
            continue
        new = (cur is None or hard_break or kind != cur["kind"] or kind in ("heading", "table")
               or quoted != cur["quoted"] or bool(_LIST_ITEM.match(piece))
               or (kind == "statblock" and piece.startswith("*"))
               or (quoted and piece.startswith("**")))
        if new:
            flush()
            cur = {"pieces": [], "kind": kind, "lines": [], "offsets": [], "quoted": quoted}
        off = sum(len(p) + 1 for p in cur["pieces"])
        cur["pieces"].append(piece)
        cur["lines"].append(i + 1)
        cur["offsets"].append(off)
        hard_break = ln.endswith("  ") or ln.endswith("\\")
    flush()
    return out


def block_line(block: Block, pos: int) -> int:
    """Source line of the character at `pos` in an unwrapped block."""
    line = block.lines[0]
    for off, ln in zip(block.offsets, block.lines):
        if off > pos:
            break
        line = ln
    return line


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
        if (len(parts) < 4 or not parts[0].strip() or not parts[1].strip() or not parts[2]
                or not "|".join(parts[3:]).strip()):
            raise ValueError(f"{p}:{n}: expected 'file|rule|quoted text|reason', got {raw!r}")
        out.append(AllowEntry(parts[0].strip(), parts[1].strip(), parts[2],
                              "|".join(parts[3:]).strip()))
    return out


def _rule_ok(e, rules) -> bool:
    return e.rule == "*" or e.rule in rules


def is_allowed(fname: str, line: str, allow, *rules) -> bool:
    """True if an entry for this file and one of `rules` (or rule `*`) quotes text in `line`.

    With no rules given, only `*` entries count.
    """
    return any((e.file == "*" or e.file == fname) and _rule_ok(e, rules) and e.text in line
               for e in allow)


def _allowed_span(fname: str, text: str, start: int, end: int, allow, *rules) -> bool:
    """True if an entry for these rules quotes text in `text` overlapping [start, end)."""
    for e in allow:
        if (e.file == "*" or e.file == fname) and _rule_ok(e, rules):
            i = text.find(e.text)
            while i >= 0:
                if i < end and start < i + len(e.text):
                    return True
                i = text.find(e.text, i + 1)
    return False


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
    # --- R0.2 (review-fix pass) families
    ("emphasis_italics", "STYLE emphasis", None, "SPEECH", 0),   # handled in code
    ("or_skills", "X or Y skill",
     r"\(" + SKILL + r"\s*(?:\bor\b|/)\s*" + SKILL + r"\)", "NOBOX", 0),
    ("html_comment", "comment", r"<!--", "ALL", 0),
    ("repo_filename", "file name",
     r"\b\d\d_[A-Za-z_]+\.md\b|\b(?:INVENTIONS|STYLE)_5e(?:\.md)?\b|"
     r"\b[\w-]+\.(?:md|yaml|yml|json|py|fof|svg)\b|\btools/", "ALL", 0),
    ("sim_jargon", "simulation",
     r"\bsimulat\w*|\bMonte Carlo\b|\bone (?:fight|run) in (?:\d+|[a-z]+(?:-[a-z]+)?)\b|"
     r"\b\d[\d,]* (?:runs|trials|iterations)\b|\bruns? in (?:\d|a hundred\b|a thousand\b)|"
     r"\bplaytest\w*", "NOBOX", I),
    ("conversion_wide", "wide",
     r"\bFacets (?:edition|rules|version)\b|\bfifth[- ]edition conversion\b|"
     r"\b5e (?:conversion|edition)\b|\bold domains?\b|\bInventions\b|\bconverted (?:from|to)\b",
     "NOBOX", 0),
    ("anachronism", "modern word",
     r"\bmemos?\b|\bbusiness(?:person|people|man|men|woman|women)\b|\bokay\b|\bclipboards?\b",
     "ALL", I),
]
HARD_FAMILIES = list(dict.fromkeys(r[0] for r in RULES))
_COMPILED = [(f, rid, re.compile(p, fl) if p else None, sc) for f, rid, p, sc, fl in RULES]
STRUCTURE_RULES = ["xref", "creature_bold", "readaloud_trigger", "trigger_format", "box_label",
                   "defined_terms", "near_duplicate"]

_DC = re.compile(r"\bDC ?(\d+)")
_DC_OK_AFTER = re.compile(
    r"^ " + ABIL + r"(?: \([^)]*\))?"
    r"(?:,? or (?:a )?(?:DC \d+ )?" + ABIL + r"(?: \([^)]*\))?)*"
    r" (?:checks?|saving throws?|save)\b")
_DC_SAVE_FORM = re.compile(r"(?:Saving Throw:\*?|save) $", re.I)
_BUDGET_LINE = re.compile(r"\bXP\b|budget|\bLow\b|\bModerate\b|\bHigh\b|multiplier|difficulty", re.I)
_IDIOM_BEFORE = re.compile(r"(?:\btakes? |\btaking |\bto (?:his|her|their|its|your|our|my) |\bat a )$")
_FALL = re.compile(r"\b(?:fall|falls|falling|fell|drop|drops|plunge|pushed over)\b", re.I)
_ITALIC = re.compile(r"(?<![*\w])\*(?![\s*])([^*\n]{1,60}?)(?<![\s*])\*(?![*\w])")
_RULES_TERMS = re.compile(
    r"^(?:Heroic Inspiration|Advantage|Disadvantage|Hit Points|Short Rest|Long Rest|Bloodied|"
    r"Difficult Terrain|Dim Light|Bright Light|Stable|Unconscious|Prone)$")  # not Darkness: a spell
NO_FILENAME_RULE = {"README.md"}  # the README is the one place file names belong


def _emphasis_hits(s: str):
    """Italic spans used for emphasis: lowercase words (up to four), or a rules term.

    Not emphasis: Title Case spans (spells, items, book sections), labels ending in a
    colon, parenthetical asides, and a span that is the whole paragraph (a DM note).
    """
    whole = s.strip()
    for m in _ITALIC.finditer(s):
        inner = m.group(1)
        if m.group() == whole or len(m.group()) > 0.8 * len(whole):
            continue
        if inner.rstrip().endswith(":") or inner.startswith("("):
            continue
        if _RULES_TERMS.match(inner) or (
                re.match(r"^[a-z][\w'’-]*(?: [\w'’-]+){0,3}[.,!?]?$", inner)):
            yield m.start(), m.group()


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


_LINK_TARGET = re.compile(r"\]\([^)\s]*\)")


def lint_hard(text: str, fname: str, allow=()) -> list[Hit]:
    """Hard-rule hits, run on unwrapped paragraphs so a phrase split across lines is seen.

    A hit is reported at the source line where its match starts. An allowlist entry exempts
    a hit only for its own rule (family name or rule id, or `*`) and only where its quoted
    text overlaps the match.
    """
    hits = []
    for blk in unwrap(text, fname):
        kind = blk.kind
        for family, rid, rx, scope in _COMPILED:
            if kind == "heading" and scope != "ALL" and family not in (
                    "pcs", "conversion_talk", "conversion_wide"):
                continue
            if family == "repo_filename" and fname in NO_FILENAME_RULE:
                continue
            s = _scoped(blk.text, kind, scope)
            if s is None:
                continue
            found = []
            if family == "bare_dc" and rx is None:
                for col, mt in _bare_dc_hits(s):
                    found.append((col, "no 'check'" if re.search(ABIL, mt) else "bare", mt))
            elif family == "emphasis_italics":
                if kind == "heading":
                    continue
                found = [(col, rid, mt) for col, mt in _emphasis_hits(s)]
            else:
                if family == "deadly_budget" and not _BUDGET_LINE.search(s):
                    continue
                if family == "repo_filename":    # a Markdown link target is not prose (R4 maps)
                    s = _LINK_TARGET.sub(lambda m: " " * len(m.group()), s)
                for m in rx.finditer(s):
                    g = m.group()
                    if family == "lowercase_terms" and g in ("advantage", "disadvantage"):
                        if _IDIOM_BEFORE.search(s[:m.start()]) or s[m.end():].startswith(" of "):
                            continue
                    if rid == "S11 bare dice" and _FALL.search(s[max(0, m.start() - 160):m.start()]):
                        continue
                    found.append((m.start(), rid, g))
            for col, r, mt in found:
                if _allowed_span(fname, blk.text, col, col + len(mt), allow, family, rid, r):
                    continue
                n = block_line(blk, col)
                hits.append((n, col, Hit(fname, n, family, r, mt)))
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
        if kind != "prose" or is_allowed(fname, line, allow, "soft"):
            flush()
            continue
        b = body(line).strip()
        if re.match(r"^(?:[-*+]|\d+\.) ", b) and not b.startswith("**"):
            flush()
            b = re.sub(r"^(?:[-*+]|\d+\.) ", "", b)
        cur.append(b)
    flush()
    return out


# Verbal tics (R5.3, O39, P2-23): module-wide targets; counted per file in DM text
# (prose, tables, stat blocks, DM boxes), never in read-aloud or quoted speech.
TIC_TARGETS = {"exactly": 15, "the_whole": 15, "quietly": 10, "out_loud": 8, "genuinely": 4,
               "say_so": 5, "permanent_confusion": 1, "not_but": 8}
TIC_LABELS = {"exactly": "exactly", "the_whole": "the whole", "quietly": "quietly",
              "out_loud": "out loud", "genuinely": "genuinely", "say_so": "say so",
              "permanent_confusion": "permanent confusion", "not_but": "not X… but Y"}
_TICS = {
    "exactly": re.compile(r"\bexactly\b", re.I),
    "the_whole": re.compile(r"\bthe whole\b", re.I),
    "quietly": re.compile(r"\bquietly\b", re.I),
    "out_loud": re.compile(r"\bout loud\b", re.I),
    "genuinely": re.compile(r"\bgenuinely\b", re.I),
    "say_so": re.compile(r"\bsay so\b", re.I),
    "permanent_confusion": re.compile(r"\bto everyone['’]s permanent confusion\b", re.I),
    "not_but": re.compile(r"\bnot\b[^.;:!?]{1,60}?\bbut\b", re.I),
}


def tic_counts(text: str, fname: str, allow=()) -> Counter:
    """Tic hits in one file's DM text. Read-aloud, headings and quoted speech are skipped;
    an allowlist entry for rule `tics`, `soft` or the tic's own id exempts a hit."""
    out = Counter({k: 0 for k in _TICS})
    for blk in unwrap(text, fname):
        if blk.kind in ("readaloud", "heading"):
            continue
        s = strip_quotes(blk.text)
        for k, rx in _TICS.items():
            for m in rx.finditer(s):
                if _allowed_span(fname, blk.text, m.start(), m.end(), allow, "tics", "soft", k):
                    continue
                out[k] += 1
    return out


def tic_budget(per_file: dict, targets=None) -> dict:
    """Each file's allowed count per tic, so the module meets its targets.

    The cut a tic needs (module total minus target) is shared in proportion to each file's
    count, by largest remainder, so the budgets sum to the target exactly.
    """
    targets = TIC_TARGETS if targets is None else targets
    out = {f: {} for f in per_file}
    for k, target in targets.items():
        counts = {f: per_file[f].get(k, 0) for f in per_file}
        total = sum(counts.values())
        excess = max(0, total - target)
        if not excess:
            for f, c in counts.items():
                out[f][k] = c
            continue
        shares = {f: excess * c / total for f, c in counts.items()}
        cut = {f: int(v) for f, v in shares.items()}
        left = excess - sum(cut.values())
        order = sorted(counts, key=lambda f: (-(shares[f] - cut[f]), -counts[f], f))
        for f in order[:left]:
            cut[f] += 1
        for f, c in counts.items():
            out[f][k] = c - cut[f]
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
        **{f"tic_{k}": v for k, v in tic_counts(text, fname, allow).items()},
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
        keep = [("" if is_allowed(p.name, ln, allow, "xref") else body(ln)) for ln in lines]
        flat = "\n".join(keep)
        flat_c = "\n".join("" if is_allowed(p.name, ln, allow, "creature_bold") else body(ln)
                           for ln in lines)

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
            for para_m in re.finditer(r"(?ms)^\*\*Enem(?:y|ies)\b[^*]*\*\*(.*?)(?:\n\s*\n|\Z)", flat_c):
                for bm in re.finditer(r"\*\*([^*]+?)\*\*", para_m.group(1)):
                    _creature_check(p.name, at(para_m.start(1) + bm.start()), bm.group(1),
                                    heads10, seen, hits)
            for bm in re.finditer(r"\*\*([^*]+?)\*\*\s*\((?:see\s+)?[Cc]hapter\s+X\)", flat_c):
                _creature_check(p.name, at(bm.start()), bm.group(1), heads10, seen, hits)

        # read-aloud trigger lines; the trigger's format (R0.2: STYLE pins
        # "**Read this when …:**", decision O41)
        blocks = unwrap(raw, p.name)
        line_block = {}
        for blk in blocks:
            for ln_no in blk.lines:
                line_block[ln_no] = blk
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
                if not ok and not is_allowed(p.name, lines[i], allow, "readaloud_trigger"):
                    snippet = " ".join(body(lines[i]).split()[:6])
                    hits.append(Hit(p.name, i + 1, "structure", "readaloud_trigger",
                                    f"untriggered read-aloud: {snippet}"))
                if ok:
                    trig = line_block.get(prev[-1] + 1)
                    if trig is not None and not TRIGGER_FORM.match(trig.text) and not is_allowed(
                            p.name, trig.text, allow, "trigger_format"):
                        hits.append(Hit(p.name, trig.lines[0], "structure", "trigger_format",
                                        " ".join(trig.text.split()[:10])))
            i += 1

        # box labels: heading style, "**DM Note — title**" alone on its line (O41)
        for n, ln in enumerate(lines, 1):
            if kinds[n - 1] in ("code", "table"):
                continue
            b = body(ln).strip()
            if BOX_START.match(b) and not BOX_FORM.match(b) and not is_allowed(
                    p.name, ln, allow, "box_label"):
                hits.append(Hit(p.name, n, "structure", "box_label", " ".join(b.split()[:8])))
    hits.sort(key=lambda h: (h.file, h.line))
    return hits


TRIGGER_FORM = re.compile(r"^\*\*Read this when [^*]+:\*\*$")
BOX_SPECIES = r"(?:DM Note|Sidebar|Troubleshooting)"
BOX_START = re.compile(r"^\*\*" + BOX_SPECIES + r"\b")
BOX_FORM = re.compile(r"^\*\*" + BOX_SPECIES + r" — [^*]*[^*\s.:]\*\*$")


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
# Defined terms (R0.2): every setting or module term the text uses must be glossed


CANON_FILES = {"V0", "V1", "V3"}  # Ten Things, Lineages, Rekuzan and the Tribes
TermEntry = namedtuple("TermEntry", "term canon gloss_file gloss_text")


def load_terms(path) -> list[TermEntry]:
    """`term|canon source|gloss file|gloss text` per line; gloss file `-` = not yet glossed."""
    out = []
    p = Path(path)
    if not p.exists():
        return out
    for n, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|", 3)]  # the gloss text may hold a "|"
        if len(parts) != 4 or not all(parts):
            raise ValueError(f"{p}:{n}: expected 'term|canon|gloss file|gloss text', got {raw!r}")
        out.append(TermEntry(*parts))
    return out


def canon_vocabulary(settings) -> set[str]:
    """Proper terms the setting files define: one-word lineage headings, the first column of
    a tribe table, and bold comma lists of names (the sects)."""
    voc = set()
    d = Path(settings)
    if not d.is_dir():
        return voc
    for p in sorted(x for x in d.glob("V*.md") if x.name.split("_")[0] in CANON_FILES):
        text = p.read_text(encoding="utf-8")
        if p.name.startswith("V1"):  # each lineage has a one-word heading
            voc.update(re.findall(r"^## ([A-Z][\w'’]+)\s*$", text, re.M))
        in_tribes = False
        for ln in text.splitlines():
            if ln.startswith("|"):
                cells = [c.strip() for c in ln.strip("|").split("|")]
                if cells and cells[0] in ("Tribe", "Lineage"):
                    in_tribes = True
                    continue
                if in_tribes and re.fullmatch(r"[A-Z][\w'’]+", cells[0]):
                    voc.add(cells[0])
            else:
                in_tribes = False
        for m in re.finditer(r"\*\*([A-Z][\w'’]+(?:, [A-Z][\w'’]+){2,})\.?\*\*", text):
            voc.update(m.group(1).split(", "))
    return voc


def _term_rx(term: str):
    return re.compile(r"(?<![\w'’])" + re.escape(term) + r"(?:['’]s|n|ns|ian|ians)?(?![\w'’])")


def lint_terms(module=MODULE, terms_path=TERMS, settings=SETTINGS, allow=(), only=None) -> list[Hit]:
    """defined_terms hits: a term used but not glossed in the module (each use), a gloss that
    is no longer in its file, and a canon term the module uses that terms.txt does not list."""
    module = Path(module)
    entries = load_terms(terms_path)
    listed = {e.term for e in entries}
    texts = {p.name: p.read_text(encoding="utf-8") for p in module_files(module)}
    flat = {f: [(blk, blk.text) for blk in unwrap(t, f) if blk.kind != "code"] for f, t in texts.items()}
    hits = []

    def uses(term):
        rx = _term_rx(term)
        for f, blocks in flat.items():
            if only and f != only:
                continue
            for blk, t in blocks:
                for m in rx.finditer(t):
                    if not _allowed_span(f, t, m.start(), m.end(), allow, "defined_terms"):
                        yield f, block_line(blk, m.start())

    for e in entries:
        if e.gloss_file == "-":
            for f, n in uses(e.term):
                hits.append(Hit(f, n, "structure", "defined_terms", f"undefined term: {e.term}"))
        elif e.gloss_file not in texts:
            hits.append(Hit(e.gloss_file, 0, "structure", "defined_terms", f"stale gloss: {e.term}"))
        else:
            g = " ".join(b.text for b, _ in flat[e.gloss_file])
            if e.gloss_text not in g or not _term_rx(e.term).search(g):
                hits.append(Hit(e.gloss_file, 0, "structure", "defined_terms", f"stale gloss: {e.term}"))
    for term in sorted(canon_vocabulary(settings) - listed):
        first = {}
        for f, n in uses(term):
            first.setdefault(f, n)
        for f, n in sorted(first.items()):
            hits.append(Hit(f, n, "structure", "defined_terms", f"unlisted canon term: {term}"))
    if only:
        hits = [h for h in hits if h.file == only]
    hits.sort(key=lambda h: (h.file, h.line, h.match))
    return hits


# ---------------------------------------------------------------------------------------
# Near-duplicate paragraphs across chapters (R5.2, O38)

NEAR_DUP_RATIO = 0.8
NEAR_DUP_MIN_WORDS = 20
_DUP_KINDS = ("prose", "readaloud")


def _dup_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:['’][a-z]+)?", re.sub(r"[*_`]", "", text.lower()))


def lint_near_duplicates(module=MODULE, allow=(), only=None, ratio=NEAR_DUP_RATIO,
                         min_words=NEAR_DUP_MIN_WORDS) -> list[Hit]:
    """near_duplicate hits: paragraph pairs in different files above `ratio` similar.

    Paragraphs are unwrapped blocks of prose or read-aloud (list items and box paragraphs
    included) with at least `min_words` words. Candidates share word 3-grams (an inverted
    index); each candidate pair is scored with difflib's ratio over the word lists. A pair is
    reported once, on the paragraph in the later file, naming its partner; a whitelist entry
    quoting text in that paragraph exempts it.
    """
    from difflib import SequenceMatcher
    module = Path(module)
    paras = []  # (file, line, words, text)
    for p in module_files(module):
        for blk in unwrap(p.read_text(encoding="utf-8"), p.name):
            if blk.kind not in _DUP_KINDS:
                continue
            w = _dup_words(blk.text)
            if len(w) >= min_words:
                paras.append((p.name, blk.lines[0], w, blk.text))
    index = {}
    for i, (_, _, w, _) in enumerate(paras):
        for g in {tuple(w[k:k + 3]) for k in range(len(w) - 2)}:
            index.setdefault(g, []).append(i)
    shared = Counter()
    for ids in index.values():
        if len(ids) > 40:  # a stock phrase, not evidence of a copy
            continue
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                a, b = ids[x], ids[y]
                if paras[a][0] != paras[b][0]:
                    shared[(a, b)] += 1
    hits = []
    for (a, b), n in shared.items():
        wa, wb = paras[a][2], paras[b][2]
        if n < 0.5 * ratio * min(len(wa), len(wb)):
            continue
        r = SequenceMatcher(None, wa, wb, autojunk=False).ratio()
        if r <= ratio:
            continue
        (fa, la, _, ta), (fb, lb, _, tb) = sorted((paras[a], paras[b]), key=lambda q: (q[0], q[1]))
        if only and fb != only:
            continue
        if is_allowed(fb, tb, allow, "near_duplicate") or is_allowed(fa, ta, allow, "near_duplicate"):
            continue
        hits.append(Hit(fb, lb, "structure", "near_duplicate",
                        f"~{fa}:{la} ({r:.2f}) " + " ".join(tb.split()[:8])))
    hits.sort(key=lambda h: (h.file, h.line))
    return hits


# ---------------------------------------------------------------------------------------
# Running, baseline, check, report


def run(module=MODULE, files=None, allow=None, terms=TERMS, settings=SETTINGS) -> dict:
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
        structure += lint_terms(module, terms, settings, allow, only=f)
        structure += lint_near_duplicates(module, allow, only=f)
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
        for t in TIC_TARGETS:
            k = f"tic_{t}"
            if k in b and m.get(k, 0) > b[k]:     # a baseline from before R5.3 has no tics
                problems.append(f"SOFT {f} {k}: {m[k]} vs baseline {b[k]}")
    return problems


def tic_tables(rep: dict) -> str:
    """Module totals against the tic targets, then each file's count and budget."""
    files = sorted(rep["soft"])
    per_file = {f: {t: rep["soft"][f].get(f"tic_{t}", 0) for t in TIC_TARGETS} for f in files}
    budget = tic_budget(per_file)
    out = ["| tic | target | module | cut needed |", "|---|---|---|---|"]
    for t, target in TIC_TARGETS.items():
        tot = sum(per_file[f][t] for f in files)
        out.append(f"| {TIC_LABELS[t]} | {target} | {tot} | {max(0, tot - target)} |")
    out.append("")
    out.append("Per file: count / budget (the file's share of the cut, by largest remainder).")
    out.append("")
    out.append("| file | " + " | ".join(TIC_LABELS[t] for t in TIC_TARGETS) + " |")
    out.append("|" + "---|" * (len(TIC_TARGETS) + 1))
    for f in files:
        out.append(f"| {f} | " + " | ".join(f"{per_file[f][t]} / {budget[f][t]}"
                                             for t in TIC_TARGETS) + " |")
    return "\n".join(out)


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
    for f in HARD_FAMILIES + STRUCTURE_RULES:
        out.append(f"| {f} | {fam[f]} |")
    out.append("")
    out.append(tic_tables(rep))
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
