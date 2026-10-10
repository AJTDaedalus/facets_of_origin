"""Continuity checker for the Oraga Night 5e module (review-fix task R0.1).

It reads the continuity bible (`../facts.yaml`), unwraps every module chapter into the
paragraphs Markdown renders, and flags each phrasing that contradicts a fact, with
file:line and the unwrapped context. The check types are documented at the top of
facts.yaml: forbid, sentence, count, size, movement, require, rule_copy.

Usage (from the repo root):
    python conversions/dnd5e/oraga_night/tools/fact_check.py             # every hit; exit 1 if any
    python conversions/dnd5e/oraga_night/tools/fact_check.py --report    # counts per fact, then the hits
    python conversions/dnd5e/oraga_night/tools/fact_check.py --baseline  # write fact_baseline.json
    python conversions/dnd5e/oraga_night/tools/fact_check.py --check     # fail only on hits not in the baseline

--check is the phase gate while the hits are worked down, like lint_5e.py --check: a hit
count going up fails, going down never does. After a phase fixes hits, re-run --baseline
and say so in the LOG. Not scanned: INVENTIONS_5e.md and STYLE_5e.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, namedtuple
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import lint_5e as L  # noqa: E402  (shared classify/unwrap)

MODULE = TOOLS.parent
FACTS = MODULE / "facts.yaml"
BASELINE = TOOLS / "fact_baseline.json"
EXCLUDE = L.EXCLUDE

Hit = namedtuple("Hit", "fact kind file line match context why")

TYPES = {
    "forbid": ("pattern",),
    "sentence": ("all",),
    "count": ("noun", "window", "allowed"),
    "size": ("subject", "window", "allowed"),
    "movement": ("subject", "from"),
    "require": ("file", "pattern"),
    "rule_copy": ("home", "elements"),
}

# ---------------------------------------------------------------------------------------
# Numbers and Roman numerals

_UNITS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
          "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
          "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
_TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
         "eighty": 80, "ninety": 90}
_ONES = {"one": 1, **{k: v for k, v in _UNITS.items() if v < 10}}
NUMBER = re.compile(
    r"\b(?:(?:a|two|three|half a) dozen|dozen|(?:a |one )?hundred|"
    r"(?:" + "|".join(_TENS) + r")(?:-(?:" + "|".join(_ONES) + r"))?|"
    r"(?:" + "|".join(_UNITS) + r")|\d[\d,]*)\b", re.I)


def number_value(s: str) -> int:
    t = s.lower().strip()
    if re.fullmatch(r"\d[\d,]*", t):
        return int(t.replace(",", ""))
    if "dozen" in t:
        n = {"a": 1, "two": 2, "three": 3, "half a": 0.5, "dozen": 1}.get(t.replace(" dozen", ""), 1)
        return int(n * 12)
    if "hundred" in t:
        return 100
    if "-" in t:
        a, b = t.split("-", 1)
        return _TENS[a] + _ONES[b]
    if t in _TENS:
        return _TENS[t]
    return _UNITS[t]


_ROMAN = {"I": 1, "V": 5, "X": 10}


def roman(s: str) -> int:
    if not s or any(c not in _ROMAN for c in s):
        raise ValueError(f"not a Roman numeral: {s!r}")
    total = 0
    for a, b in zip(s, s[1:] + " "):
        v = _ROMAN[a]
        total += -v if b in _ROMAN and _ROMAN[b] > v else v
    return total


# ---------------------------------------------------------------------------------------
# Loading


def validate(data: dict) -> list[dict]:
    """Check the bible's shape and compile its regexes; return the fact list."""
    if not isinstance(data, dict) or not isinstance(data.get("facts"), list):
        raise ValueError("facts file needs a top-level 'facts' list")
    seen, out = set(), []
    for f in data["facts"]:
        fid = f.get("id")
        if not fid or "truth" not in f:
            raise ValueError(f"fact needs 'id' and 'truth': {f!r}")
        if fid in seen:
            raise ValueError(f"duplicate fact id {fid!r}")
        seen.add(fid)
        checks = []
        for c in f.get("checks") or []:
            t = c.get("type")
            if t not in TYPES:
                raise ValueError(f"{fid}: unknown check type {t!r}")
            for field in TYPES[t]:
                if field not in c:
                    raise ValueError(f"{fid}: {t} check needs {field!r}")
            c = dict(c)
            try:
                for key in ("pattern", "noun", "subject", "unless", "anchor"):
                    if key in c:
                        c["_" + key] = re.compile(c[key])
                if t == "sentence":
                    c["_all"] = [re.compile(p) for p in c["all"]]
                if t == "rule_copy":
                    c["_elements"] = [re.compile(p) for p in c["elements"]]
            except re.error as e:
                raise ValueError(f"{fid}: bad regex in {t} check: {e}") from e
            if t == "movement":
                c["_from"] = roman(str(c["from"]))
            checks.append(c)
        out.append({**f, "checks": checks})
    return out


def load_facts(path=FACTS) -> list[dict]:
    return validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")))


# ---------------------------------------------------------------------------------------
# Scopes

_ABBR = re.compile(r"\b(?:ft|e\.g|i\.e|etc|vs|Mr|Mrs|Ms|St|No|Ch|cf|approx|Mv)\.", re.I)
_LABEL = re.compile(r"^\s*\*{2,3}[^*]+\*{2,3}\s*$")
_SPLIT = re.compile(r"(?<=[.!?])[*_)\"”’]*\s+(?=[*_(\"“‘>]*[A-Z0-9⟨])")


def sentences(text: str):
    """(start, end) spans of the sentences in an unwrapped block."""
    masked = _ABBR.sub(lambda m: m.group().replace(".", "§"), text)
    masked = re.sub(r"(\d)\.(\d)", r"\1§\2", masked)
    spans, start = [], 0
    for m in _SPLIT.finditer(masked):
        spans.append((start, m.end()))
        start = m.end()
    spans.append((start, len(text)))
    spans = [s for s in spans if text[s[0]:s[1]].strip()]
    # a bold run-in label ("**Who they brought.**") belongs to the sentence after it
    merged = []
    for s in spans:
        if merged and _LABEL.match(text[merged[-1][0]:merged[-1][1]]):
            merged[-1] = (merged[-1][0], s[1])
        else:
            merged.append(s)
    return merged


def _units(block: L.Block, scope: str):
    if scope == "block" or block.kind == "table":
        return [(0, len(block.text))]
    return sentences(block.text)


def _applies(check: dict, fname: str) -> bool:
    files = check.get("files")
    return not files or any(fname.startswith(p) for p in files)


def _context(text: str, start: int, end: int, width: int = 90) -> str:
    a, b = max(0, start - width), min(len(text), end + width)
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


# ---------------------------------------------------------------------------------------
# Checks

_MEASURE = re.compile(r"\b(\d+)(?:-foot| feet| ft\.?) (\w+)")
_MV = re.compile(r"\b(?:Mv|Movements?)\s+([IVX]+)\b(?:\s*[–-]\s*[IVX]+\b)?|\bany Movement\b(?!\s+from\s+[IVX]+)")


def _check_block(fact: dict, c: dict, block: L.Block, fname: str):
    t, text = c["type"], block.text
    why = c.get("why", "")
    unless = c.get("_unless")

    def hit(start, end):
        return Hit(fact["id"], t, fname, L.block_line(block, start), text[start:end],
                   _context(text, start, end), why)

    if t in ("forbid", "sentence"):
        for a, b in _units(block, c.get("scope", "sentence")):
            unit = text[a:b]
            if unless and unless.search(unit):
                continue
            if t == "forbid":
                for m in c["_pattern"].finditer(unit):
                    yield hit(a + m.start(), a + m.end())
            else:
                ms = [rx.search(unit) for rx in c["_all"]]
                if all(ms):
                    yield hit(a + ms[0].start(), a + ms[0].end())
        return

    if t == "count":
        allowed = {int(x) for x in c["allowed"]}
        for a, b in _units(block, "sentence"):
            unit = text[a:b]
            if unless and unless.search(unit):
                continue
            for nm in c["_noun"].finditer(unit):
                before = unit[:nm.start()]
                floor = before.rfind("|") + 1  # never count across a table cell
                words = list(re.finditer(r"[\w,'’-]+", before[floor:]))[-int(c["window"]):]
                if not words:
                    continue
                lo = floor + words[0].start()
                for num in NUMBER.finditer(before, lo):
                    if number_value(num.group()) not in allowed:
                        yield hit(a + num.start(), a + nm.end())
                        break
        return

    if t == "size":
        allowed = {k: {int(v) for v in vs} for k, vs in c["allowed"].items()}
        for a, b in _units(block, "sentence"):
            unit = text[a:b]
            if unless and unless.search(unit):
                continue
            for sm in c["_subject"].finditer(unit):
                win = unit[sm.end():sm.end() + int(c["window"])]
                for mm in _MEASURE.finditer(win):
                    dim = mm.group(2).lower()
                    if dim in allowed and int(mm.group(1)) not in allowed[dim]:
                        s = a + sm.end() + mm.start()
                        yield hit(s, s + len(mm.group()))
        return

    if t == "rule_copy":
        # A rule printed in one home (O36): a paragraph, list item or table row outside
        # the home file that matches more than `max` of the rule's elements restates it.
        if fname.startswith(str(c["home"])):
            return
        found = [rx.search(text) for rx in c["_elements"]]
        got = [m for m in found if m]
        if len(got) > int(c.get("max", 2)):
            first = min(got, key=lambda m: m.start())
            yield Hit(fact["id"], t, fname, L.block_line(block, first.start()),
                      f"{len(got)} of {len(found)} elements: "
                      + "; ".join(m.group() for m in sorted(got, key=lambda m: m.start())),
                      _context(text, first.start(), first.end()), why)
        return

    if t == "movement":
        for a, b in _units(block, "sentence"):
            unit = text[a:b]
            if (unless and unless.search(unit)) or not c["_subject"].search(unit):
                continue
            for mm in _MV.finditer(unit):
                first = 1 if mm.group(1) is None else roman(mm.group(1))
                if first < c["_from"]:
                    yield hit(a + mm.start(), a + mm.end())
        return


def check_text(text: str, fname: str, facts: list[dict]) -> list[Hit]:
    """Every block-level hit in one file (require checks run in check_module)."""
    blocks = L.unwrap(text, fname)
    out = []
    for fact in facts:
        for c in fact["checks"]:
            if c["type"] == "require" or not _applies(c, fname):
                continue
            for blk in blocks:
                out.extend(_check_block(fact, c, blk, fname))
    out.sort(key=lambda h: (h.line, h.fact))
    return out


def _require(fact: dict, c: dict, module: Path) -> list[Hit]:
    p = module / c["file"]
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    flat = " ".join(b.text for b in L.unwrap(text, p.name))
    if c["_pattern"].search(flat):
        return []
    line, ctx = 1, ""
    if "_anchor" in c:
        for blk in L.unwrap(text, p.name):
            m = c["_anchor"].search(blk.text)
            if m:
                line, ctx = L.block_line(blk, m.start()), _context(blk.text, m.start(), m.end())
                break
    return [Hit(fact["id"], "require", p.name, line, f"missing: {c['pattern']}", ctx, c.get("why", ""))]


def module_files(module: Path):
    return sorted(p for p in Path(module).glob("*.md") if p.name not in EXCLUDE)


def check_module(module=MODULE, facts=None) -> list[Hit]:
    module = Path(module)
    facts = load_facts() if facts is None else facts
    out = []
    for p in module_files(module):
        out += check_text(p.read_text(encoding="utf-8"), p.name, facts)
    for fact in facts:
        for c in fact["checks"]:
            if c["type"] == "require":
                out += _require(fact, c, module)
    out.sort(key=lambda h: (h.file, h.line, h.fact))
    return out


# ---------------------------------------------------------------------------------------
# Baseline and CLI


def make_baseline(hits) -> dict:
    data = {}
    for h in hits:
        r = data.setdefault(h.fact, {}).setdefault(h.file, {})
        r[h.match] = r.get(h.match, 0) + 1
    return {"version": 1, "facts": data}


def compare(hits, base: dict) -> list[str]:
    now = make_baseline(hits)["facts"]
    probs = []
    for fid, files in now.items():
        for f, matches in files.items():
            for mt, n in matches.items():
                b = base.get("facts", {}).get(fid, {}).get(f, {}).get(mt, 0)
                if n > b:
                    lines = [h.line for h in hits if h.fact == fid and h.file == f and h.match == mt]
                    probs.append(f"NEW {fid} {f} {mt!r}: {n} now vs {b} in baseline (lines {lines})")
    return probs


def format_hit(h: Hit) -> str:
    return f"{h.file}:{h.line}: [{h.fact}/{h.kind}] {h.match!r} — {h.why}\n    {h.context}"


def report(hits, facts) -> str:
    c = Counter(h.fact for h in hits)
    out = ["| fact | hits |", "|---|---|"]
    for f in facts:
        out.append(f"| {f['id']} | {c[f['id']]} |")
    out.append(f"| TOTAL | {len(hits)} |")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Oraga Night 5e continuity checker")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--baseline", action="store_true", help="write the baseline JSON")
    g.add_argument("--check", action="store_true", help="fail only on hits not in the baseline")
    g.add_argument("--report", action="store_true", help="counts per fact, then the hits")
    ap.add_argument("--module", default=str(MODULE), help=argparse.SUPPRESS)
    ap.add_argument("--facts", default=str(FACTS), help=argparse.SUPPRESS)
    ap.add_argument("--baseline-path", default=str(BASELINE), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    facts = load_facts(a.facts)
    hits = check_module(Path(a.module), facts)

    if a.baseline:
        Path(a.baseline_path).write_text(json.dumps(make_baseline(hits), indent=1, sort_keys=True,
                                                    ensure_ascii=False) + "\n", encoding="utf-8")
        print(report(hits, facts))
        print(f"\nBaseline written to {a.baseline_path}")
        return 0
    if a.check:
        bp = Path(a.baseline_path)
        if not bp.exists():
            print(f"No baseline at {bp}; run --baseline first", file=sys.stderr)
            return 2
        probs = compare(hits, json.loads(bp.read_text(encoding="utf-8")))
        for x in probs:
            print(x)
        print(f"fact_check --check: {'FAIL' if probs else 'OK'} ({len(probs)} problem(s); "
              f"{len(hits)} hits remain)")
        return 1 if probs else 0
    if a.report:
        print(report(hits, facts))
        print()
    for h in hits:
        print(format_hit(h))
    if not a.report:
        print(f"\nfact_check: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
