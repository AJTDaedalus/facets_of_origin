"""Generate the PHB/MM Manual term index from the Glossary.

Facets of Origin is digital-first (Brain ruling B2, docs/DECISIONS.md) — a
page-number index is meaningless, so the right artifact is a term -> section
map with links, generated from the books rather than hand-maintained. A
hand-written index in a moving ruleset goes stale, and a stale index
misdirects with confidence.

The Glossary is the term list: every entry's base term (the bold word or
phrase before any parenthetical variants, e.g. "Condition" out of
"Condition (Tier 1/2/3)") is looked up across every file in `player_handbook/`
and `mm_manual/`, and every heading under which it appears — in the heading
itself or the body text below it — becomes one linked entry.

Usage:
    cd software
    python -m tools.build_index            # regenerate player_handbook/Index.md
    python -m tools.build_index --check     # exit 1 if regeneration would change the file

See docs/DESIGN_production_apparatus.md §4.9 and TASKS PA-10.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYER_HANDBOOK = REPO_ROOT / "player_handbook"
MM_MANUAL = REPO_ROOT / "mm_manual"
GLOSSARY = PLAYER_HANDBOOK / "Glossary.md"
INDEX_FILE = PLAYER_HANDBOOK / "Index.md"

# The file this generator produces. Excluded from its own input so that
# regenerating never feeds the previous run's output back into the next one.
GENERATED_FILENAME = "Index.md"

# "**Term** — definition..." at the start of a line. Only the bold term is
# captured; the definition and chapter pointer aren't needed here.
_GLOSSARY_TERM = re.compile(r"^\*\*(.+?)\*\* — ", re.M)

_HEADING = re.compile(r"^(#{1,6})[ \t]+(\S.*?)\s*$", re.M)

# A chapter token that is a bare or dotted roman numeral ("I", "II.4b") — the
# PHB's own chapter-numbering convention (see test_docs_consistency.py).
_ROMAN_CHAPTER = re.compile(r"^[IVX]+(\.\d+[a-c]?)?$")
_MM_CHAPTER = re.compile(r"^MM\d$")


def parse_glossary_terms(glossary_path: Path = GLOSSARY) -> list[str]:
    """Every glossary entry's base term, in file order.

    "Posture (Aggressive/Measured/Defensive/Withdrawn)" yields "Posture" —
    the parenthetical variants aren't separately indexed, matching
    test_docs_consistency.py's INV-3 base-term convention.
    """
    return [
        raw.split("(")[0].strip()
        for raw in _GLOSSARY_TERM.findall(glossary_path.read_text())
    ]


def _chapter_label(path: Path) -> str:
    """A human-readable chapter label for a book file, from its filename."""
    token = path.stem.split("_", 1)[0]
    if _ROMAN_CHAPTER.match(token) or _MM_CHAPTER.match(token):
        return token
    return path.stem.replace("_", " ")


def _slugify(heading: str) -> str:
    """A GitHub-flavored-markdown-style anchor for a heading."""
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def find_term_sections(term: str, path: Path) -> list[tuple[str, str]]:
    """[(heading text, anchor), ...] of every heading under which `term`
    appears in `path`, in document order. A term counts as appearing under a
    heading if it's in the heading itself or anywhere in the body text before
    the next heading of any level. Returns [] if the term is absent or the
    file has no headings at all.
    """
    text = path.read_text()
    pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
    headings = list(_HEADING.finditer(text))

    sections: list[tuple[str, str]] = []
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section_text = text[match.start():end]
        if pattern.search(section_text):
            heading_text = match.group(2)
            sections.append((heading_text, _slugify(heading_text)))
    return sections


def _book_files() -> list[Path]:
    """Every markdown file in both books except the generated index itself."""
    files = sorted(PLAYER_HANDBOOK.glob("*.md")) + sorted(MM_MANUAL.glob("*.md"))
    return [f for f in files if f.name != GENERATED_FILENAME]


def _link(path: Path, anchor: str) -> str:
    """A markdown link to a heading, relative to player_handbook/ (where
    Index.md lives)."""
    if path.parent == MM_MANUAL:
        return f"../mm_manual/{path.name}#{anchor}"
    return f"{path.name}#{anchor}"


def build_index(
    terms: list[str] | None = None, files: list[Path] | None = None
) -> dict[str, list[tuple[Path, str, str]]]:
    """{term: [(file, heading, anchor), ...]}, in book-walk order per term."""
    terms = parse_glossary_terms() if terms is None else terms
    files = _book_files() if files is None else files

    index: dict[str, list[tuple[Path, str, str]]] = {}
    for term in terms:
        occurrences = []
        for path in files:
            for heading, anchor in find_term_sections(term, path):
                occurrences.append((path, heading, anchor))
        index[term] = occurrences
    return index


def render_index(index: dict[str, list[tuple[Path, str, str]]]) -> str:
    lines = [
        "# Index",
        "",
        "*Generated by `software/tools/build_index.py` from the "
        "[Glossary](Glossary.md) term list — do not edit by hand. "
        "Regenerating this file should produce no diff (INV-4); if it "
        "doesn't, the index was stale.*",
        "",
        "---",
        "",
    ]
    for term in sorted(index, key=str.lower):
        lines.append(f"## {term}")
        lines.append("")
        occurrences = index[term]
        if not occurrences:
            lines.append("_No sections found._")
        else:
            for path, heading, anchor in occurrences:
                label = _chapter_label(path)
                lines.append(f"- [{label} — {heading}]({_link(path, anchor)})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_index_text() -> str:
    return render_index(build_index())


def main() -> int:
    check = "--check" in sys.argv
    text = generate_index_text()
    if check:
        current = INDEX_FILE.read_text() if INDEX_FILE.exists() else None
        if current != text:
            print("Index.md is stale — run `python -m tools.build_index` to regenerate.")
            return 1
        print("Index.md is up to date.")
        return 0
    INDEX_FILE.write_text(text)
    print(f"Wrote {INDEX_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
