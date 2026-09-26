"""Render the MM toolbox tables (`software/facets/base/tables.yaml`) into MM6.

MM6 marks where each table goes:

    <!-- table: reaction -->
    <!-- /table -->

and this tool fills the region from tables.yaml, so the book and the app roll
on the same table (INV-25). Each table is printed as:

    <!-- table: reaction -->
    *Roll 2d6. When the party meets someone whose attitude the fiction hasn't fixed.*

    **Table MM6–1: Reaction**

    | 2d6 | Result |
    |---|---|
    | 2–4 | Hostile. ... |
    <!-- /table -->

Numbering: the N in "Table MM6–N" is the table's position among every table
caption in MM6 in document order — generated tables and any hand-written
`**Table MM6–n: …**` captions outside markers count alike — so the chapter
numbers 1..n with no gaps (INV-9) as long as hand-written captions are
themselves numbered in document order.

Usage:
    cd software
    python -m tools.build_toolbox           # fill MM6
    python -m tools.build_toolbox --check   # exit 1 if anything would change
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MM6 = REPO_ROOT / "mm_manual" / "MM6_The_Toolbox.md"
TABLES_YAML = REPO_ROOT / "software" / "facets" / "base" / "tables.yaml"
CHAPTER = "MM6"

MARKER = re.compile(r"(<!-- table: ([a-z0-9_]+) -->\n)(.*?)(<!-- /table -->)", re.S)
CAPTION = re.compile(rf"^\*\*Table {CHAPTER}–(\d+): .+\*\*$", re.M)


def load_tables(path: Path = TABLES_YAML) -> dict:
    """{id: TableDef} from tables.yaml (validated: every die covered exactly once)."""
    from app.facets.loader import load_tables_file
    return {t.id: t for t in load_tables_file(path).tables}


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def render_table(table, number: int) -> str:
    """One table's generated block (without the markers)."""
    lines = []
    use = _cell(table.use)
    lines.append(f"*Roll {table.die}.{(' ' + use) if use else ''}*")
    lines.append("")
    lines.append(f"**Table {CHAPTER}–{number}: {_cell(table.name)}**")
    lines.append("")
    lines.append(f"| {table.die} | Result |")
    lines.append("|---|---|")
    for entry in table.entries:
        roll = str(entry.roll).replace("-", "–")
        lines.append(f"| {roll} | {_cell(entry.text)} |")
    return "\n".join(lines) + "\n"


def fill_text(text: str, tables: dict) -> tuple[str, list[str]]:
    """Fill every marker. Returns (new text, unknown table ids)."""
    unknown: list[str] = []
    out: list[str] = []
    pos = 0
    number = 0
    for m in MARKER.finditer(text):
        before = text[pos:m.start()]
        number += len(CAPTION.findall(before))
        out.append(before)
        opener, tid, _body, closer = m.groups()
        table = tables.get(tid)
        number += 1
        if table is None:
            unknown.append(tid)
            out.append(m.group(0))
        else:
            out.append(opener + render_table(table, number) + closer)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), unknown


def placed_ids(path: Path = MM6) -> list[str]:
    if not path.exists():
        return []
    return [m.group(2) for m in MARKER.finditer(path.read_text(encoding="utf-8"))]


def unplaced_tables(path: Path = MM6, tables_path: Path = TABLES_YAML) -> list[str]:
    """Table ids in tables.yaml that MM6 has no marker for."""
    placed = set(placed_ids(path))
    return [tid for tid in load_tables(tables_path) if tid not in placed]


def build(write: bool, path: Path = MM6, tables_path: Path = TABLES_YAML) -> list[str]:
    """Fill MM6. Returns what is stale: the file name if it would change, or a
    note if MM6 or tables.yaml is missing.

    Raises:
        KeyError: a marker names a table that tables.yaml does not have.
    """
    if not tables_path.exists():
        return [f"{tables_path.name} (missing)"]
    if not path.exists():
        return [f"{path.name} (missing)"]
    tables = load_tables(tables_path)
    text = path.read_text(encoding="utf-8")
    new_text, unknown = fill_text(text, tables)
    if unknown:
        raise KeyError(f"{path.name} marks unknown table(s): {', '.join(unknown)}")
    if new_text == text:
        return []
    if write:
        path.write_text(new_text, encoding="utf-8")
    return [path.name]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    stale = build(write=not check)
    if check:
        if stale:
            print(f"MM6 is stale ({', '.join(stale)}) — run `python -m tools.build_toolbox`.")
            return 1
        print("MM6 is up to date.")
        return 0
    print(f"MM6: {len(placed_ids())} table(s) placed; {', '.join(stale) or 'no change'}")
    missing = unplaced_tables() if TABLES_YAML.exists() and MM6.exists() else []
    if missing:
        print(f"Not placed in MM6: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
