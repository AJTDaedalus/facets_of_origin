"""Copyright phrasing scan for the Oraga Night 5e module (review-fix task R6.1).

It cuts every sentence of the module chapters into 8-word shingles (lowercased, punctuation
stripped, whitespace collapsed) and looks each one up in plain-text extracts of official
books. Overlapping shingles in one sentence merge into a single hit. A hit whose every
shingle also appears in an allowed corpus (the CC BY 4.0 SRDs) is class (a), stock rules
grammar. Every other hit needs a human ruling: either rewrite the sentence, or, for a short
functional phrase that is generic English or 5e boilerplate, list it in the allowlist as
class (b).

The extracts are NOT part of the repo and must never be committed. Make them with PyMuPDF
(one .txt per book, a `=== PAGE n ===` line before each page so hits can cite a page) in a
scratch directory and pass that directory here.

Usage (from the repo root):
    python conversions/dnd5e/oraga_night/tools/copyright_scan.py --refs DIR --srd DIR
    python conversions/dnd5e/oraga_night/tools/copyright_scan.py --refs DIR --srd DIR --check
    python conversions/dnd5e/oraga_night/tools/copyright_scan.py ... --json out.json

--check exits 1 if any hit is neither class (a) nor allowlisted. The allowlist
(`copyright_allow.txt`) holds the SHA-1 of a hit's normalized run plus the module file and a
reason, never the text, so no official wording is stored. Not scanned: INVENTIONS_5e.md,
STYLE_5e.md, facts.yaml and the tools.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import namedtuple
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import lint_5e as L  # noqa: E402  (shared classify/unwrap)

MODULE = TOOLS.parent
ALLOW = TOOLS / "copyright_allow.txt"
EXCLUDE = L.EXCLUDE
N = 8

Seg = namedtuple("Seg", "file line words lines")
Hit = namedtuple("Hit", "file line run digest sources srd")

_PAGE = re.compile(r"^=== PAGE (\d+) ===$", re.M)
_SENT = re.compile(r"(?<=[.!?;:])[\"'”’)\]]*\s+")


def normalize(text: str) -> list[str]:
    """Lowercase words with punctuation stripped (apostrophes vanish, dashes split)."""
    t = text.lower().replace("’", "").replace("'", "").replace("‘", "")
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)  # PDF end-of-line hyphenation
    t = re.sub(r"[^\w\s]|_", " ", t)
    return t.split()


def strip_md(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return s.replace("**", " ").replace("*", " ").replace("`", " ")


def segments(text: str, fname: str) -> list[Seg]:
    """Sentences (table cells count as sentences), each as normalized words with lines."""
    out = []
    for b in L.unwrap(text, fname):
        if b.kind == "code":
            continue
        parts = b.text.split("|") if b.kind == "table" else [b.text]
        base = 0
        for part in parts:
            pos = 0
            for m in list(_SENT.finditer(part)) + [None]:
                end = m.start() if m else len(part)
                sent = part[pos:end]
                words, lines = [], []
                for w in re.finditer(r"\S+", strip_md(sent)):
                    for tok in normalize(w.group()):
                        words.append(tok)
                        lines.append(L.block_line(b, base + pos + w.start()))
                if len(words) >= N:
                    out.append(Seg(fname, lines[0], words, lines))
                if m:
                    pos = m.end()
            base += len(part) + 1
    return out


def shingles(words):
    return [" ".join(words[i:i + N]) for i in range(len(words) - N + 1)]


def module_files(module: Path):
    return sorted(p for p in module.glob("*.md") if p.name not in EXCLUDE)


def load_module(module: Path) -> list[Seg]:
    segs = []
    for p in module_files(module):
        segs += segments(p.read_text(encoding="utf-8"), p.name)
    return segs


def index_corpus(directory: Path, wanted: set[str]) -> dict[str, list[tuple[str, int]]]:
    """Map each wanted shingle to the (book, page) places it occurs in a directory of .txt."""
    found: dict[str, list[tuple[str, int]]] = {}
    for p in sorted(Path(directory).glob("*.txt")):
        raw = p.read_text(encoding="utf-8", errors="replace")
        pieces = _PAGE.split(raw)
        # pieces: [pre, n1, text1, n2, text2, ...]; no markers means one page "0"
        pages = [(0, pieces[0])] + [(int(pieces[i]), pieces[i + 1])
                                    for i in range(1, len(pieces) - 1, 2)]
        words, wpage = [], []
        for num, txt in pages:
            w = normalize(txt)
            words += w
            wpage += [num] * len(w)
        for i in range(len(words) - N + 1):
            s = " ".join(words[i:i + N])
            if s in wanted:
                lst = found.setdefault(s, [])
                if (p.stem, wpage[i]) not in lst:
                    lst.append((p.stem, wpage[i]))
    return found


def digest(run: str) -> str:
    return hashlib.sha1(run.encode()).hexdigest()


def scan(segs: list[Seg], refs: dict, srd: dict) -> list[Hit]:
    """Merge overlapping shingle matches per sentence into hits."""
    hits = []
    for seg in segs:
        sh = shingles(seg.words)
        i = 0
        while i < len(sh):
            if sh[i] not in refs:
                i += 1
                continue
            j = i
            while j + 1 < len(sh) and sh[j + 1] in refs:
                j += 1
            run = " ".join(seg.words[i:j + N])
            srcs = []
            for s in sh[i:j + 1]:
                for x in refs[s]:
                    if x not in srcs:
                        srcs.append(x)
            hits.append(Hit(seg.file, seg.lines[i], run, digest(run), srcs,
                            all(s in srd for s in sh[i:j + 1])))
            i = j + 1
    return hits


def load_allow(path: Path) -> set[tuple[str, str]]:
    """`sha1 | file | reason` lines; returns {(sha1, file)}."""
    out = set()
    if not Path(path).exists():
        return out
    for n, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        if len(parts) < 3 or not re.fullmatch(r"[0-9a-f]{40}", parts[0]) or not parts[2]:
            raise ValueError(f"{path}:{n}: expected 'sha1 | file | reason', got {raw!r}")
        out.add((parts[0], parts[1]))
    return out


def classify_hits(hits: list[Hit], allow: set[tuple[str, str]]):
    a = [h for h in hits if h.srd]
    b = [h for h in hits if not h.srd and (h.digest, h.file) in allow]
    c = [h for h in hits if not h.srd and (h.digest, h.file) not in allow]
    return a, b, c


def run(module: Path, refs_dir: Path, srd_dirs: list[Path], allow_path: Path):
    segs = load_module(module)
    wanted = {s for seg in segs for s in shingles(seg.words)}
    refs = index_corpus(refs_dir, wanted)
    srd: dict = {}
    for d in srd_dirs:
        for k, v in index_corpus(d, wanted).items():
            srd.setdefault(k, []).extend(v)
    hits = scan(segs, refs, srd)
    return classify_hits(hits, load_allow(allow_path)), len(segs), len(wanted)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--refs", required=True, type=Path, help="directory of official-book .txt")
    ap.add_argument("--srd", action="append", default=[], type=Path,
                    help="directory of allowed (CC BY) .txt; repeatable")
    ap.add_argument("--module", type=Path, default=MODULE)
    ap.add_argument("--allow", type=Path, default=ALLOW)
    ap.add_argument("--check", action="store_true", help="exit 1 on any class (c) hit")
    ap.add_argument("--json", type=Path, help="write every hit as JSON (keep it out of the repo)")
    args = ap.parse_args(argv)
    if not args.refs.is_dir():
        ap.error(f"--refs {args.refs} is not a directory")
    (a, b, c), nseg, nsh = run(args.module, args.refs, args.srd, args.allow)
    print(f"{nseg} sentences, {nsh} distinct shingles; hits: (a) SRD {len(a)}, "
          f"(b) allowlisted {len(b)}, (c) to review {len(c)}")
    for h in c:
        src = ", ".join(f"{bk} p{pg}" for bk, pg in h.sources[:4])
        print(f"{h.file}:{h.line}: [{src}] {h.digest[:10]} {h.run}")
    if args.json:
        args.json.write_text(json.dumps(
            {k: [h._asdict() for h in v] for k, v in (("a", a), ("b", b), ("c", c))},
            indent=1), encoding="utf-8")
    return 1 if (args.check and c) else 0


if __name__ == "__main__":
    sys.exit(main())
