"""Generate the List of Tables and List of Boxes registers from the books.

The 3.5-era books this project's style guide is drawn from all end their
contents with a register of every numbered table (`style/analysis/rulebooks.md`
§1, `gm_books.md` §1). A table you cannot cite by designation is a table body
text has to point at with "the table above", which is the failure mode the
style guide's Law 6 exists to prevent.

Every real lookup table in `player_handbook/` and `mm_manual/` carries a caption
line immediately above it:

    **Table III.3-2: Postures**

    | Posture | Offense | ... |

This generator scans for those captions and writes `player_handbook/List_of_Tables.md`.
Like the Index, it is generated rather than hand-maintained: a hand-written
register in a moving ruleset goes stale, and a stale register misdirects with
confidence.

Usage:
    cd software
    python -m tools.build_table_register           # regenerate the register
    python -m tools.build_table_register --check   # exit 1 if it would change

See docs/RESEARCH_style_audit.md finding S1.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYER_HANDBOOK = REPO_ROOT / "player_handbook"
MM_MANUAL = REPO_ROOT / "mm_manual"
BESTIARY = REPO_ROOT / "bestiary"
REGISTER_FILE = PLAYER_HANDBOOK / "List_of_Tables.md"
BOX_REGISTER_FILE = PLAYER_HANDBOOK / "List_of_Boxes.md"

# "> **MM Note — The golden rule**" — species, then the box's own title.
BOX_CAPTION = re.compile(r"^>\s*\*\*(Through the Mirror|MM Note|Example|Variant|"
                         r"Reading the Entries)(?: — (.+?))?\*\*", re.M)

# "**Table III.3-2: Postures**" on its own line. The en dash between chapter and
# sequence number is the typographic convention (style/analysis/rulebooks.md §5);
# the ASCII hyphen is rejected rather than accepted, so drift is caught here
# instead of surviving into the register.
CAPTION = re.compile(r"^\*\*Table ([A-Za-z0-9.]+)–(\d+): (.+?)\*\*$", re.M)

# Chapter files, in reading order. The register follows the book's order, not
# alphabetical order — a reader scanning for "the combat tables" wants them
# contiguous and in the place combat sits in the book.
BOOK_ORDER = [
    ("Player Handbook", PLAYER_HANDBOOK, [
        "II.1_Character_Creation_Overview.md",
        "II.2_Character_Creation_Attributes.md",
        "II.3_Magic.md",
        "II.4_Character_Creation_Facets.md",
        "II.4a_Character_Creation_Facet_Body.md",
        "II.4b_Character_Creation_Facet_Mind.md",
        "II.4c_Character_Creation_Facet_Soul.md",
        "II.6_Character_Creation_Skills.md",
        "III.1_Core_Resolution.md",
        "III.2_Adventuring.md",
        "III.3_Combat.md",
        "IV.1_Equipment.md",
        "Quick_Start.md",
    ]),
    ("Mirror Master's Manual", MM_MANUAL, [
        "MM1_Encounters_and_Enemies.md",
        "MM2_Session_Design.md",
        "MM3_Campaign_Design.md",
        "MM4_Running_the_Table.md",
        "MM5_Quick_Reference.md",
    ]),
    ("Bestiary", BESTIARY, [
        "Front_Matter.md",
        "B1_Beasts_and_Vermin.md",
        "B2_Folk.md",
        "B3_The_Made.md",
        "B4_What_Remains.md",
        "Finding_Aids.md",
    ]),
]


def _anchor(title: str) -> str:
    """GitHub's heading-anchor slug, applied to a caption line.

    Captions are not headings, so they have no anchor of their own; the link
    target is the table's nearest enclosing heading, resolved by the caller.
    """
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"[\s_]+", "-", slug).strip("-")


# The registers live in player_handbook/, so links out of it are relative.
_BOOK_DIR = {"Player Handbook": "", "Mirror Master's Manual": "../mm_manual/",
             "Bestiary": "../bestiary/"}


def _link(book_name: str, filename: str, anchor: str) -> str:
    relative = f"{_BOOK_DIR[book_name]}{filename}"
    return f"{relative}#{anchor}" if anchor else relative


def _nearest_heading(text: str, position: int) -> str | None:
    """The last markdown heading at or before `position`."""
    headings = [m for m in re.finditer(r"^#{1,6}[ \t]+(\S.*?)\s*$", text, re.M)
                if m.start() < position]
    return headings[-1].group(1) if headings else None


def collect_tables() -> list[tuple[str, list[tuple[str, str, str, str]]]]:
    """Every captioned table, grouped by book, in reading order.

    Returns [(book_name, [(designation, title, filename, anchor), ...]), ...].
    """
    books = []
    for book_name, directory, filenames in BOOK_ORDER:
        rows: list[tuple[str, str, str, str]] = []
        for filename in filenames:
            path = directory / filename
            if not path.exists():
                continue
            text = path.read_text()
            for match in CAPTION.finditer(text):
                chapter, number, title = match.groups()
                heading = _nearest_heading(text, match.start())
                anchor = _anchor(heading) if heading else ""
                rows.append((f"{chapter}–{number}", title, filename, anchor))
        books.append((book_name, rows))
    return books


def generate_register_text() -> str:
    """The full text of List_of_Tables.md."""
    lines = [
        "# List of Tables",
        "",
        "*Generated by `software/tools/build_table_register.py` from the table captions"
        " in both books — do not edit by hand. Regenerating this file should produce no"
        " diff (INV-9); if it doesn't, the register is stale.*",
        "",
        "*Tables are numbered per chapter. Body text cites them by full designation"
        " — \"Table III.3–2: Postures\" — never as \"the table above\".*",
        "",
    ]
    for book_name, rows in collect_tables():
        if not rows:
            continue
        lines.append("---")
        lines.append("")
        lines.append(f"## {book_name}")
        lines.append("")
        lines.append("| Table | Title | Section |")
        lines.append("|---|---|---|")
        for designation, title, filename, anchor in rows:
            link = _link(book_name, filename, anchor)
            lines.append(f"| **{designation}** | [{title}]({link}) | {filename} |")
        lines.append("")
    return "\n".join(lines)


def collect_boxes() -> list[tuple[str, list[tuple[str, str, str, str]]]]:
    """Every declared box, grouped by book: (species, title, filename, anchor).

    DMG1 ends with a list of sidebars beside its list of tables, because a boxed
    designer note the reader half-remembers is unfindable otherwise
    (gm_books.md §1). Same reasoning, same treatment.
    """
    books = []
    for book_name, directory, filenames in BOOK_ORDER:
        rows: list[tuple[str, str, str, str]] = []
        for filename in filenames:
            path = directory / filename
            if not path.exists():
                continue
            text = path.read_text()
            for match in BOX_CAPTION.finditer(text):
                species, title = match.group(1), match.group(2) or ""
                heading = _nearest_heading(text, match.start())
                anchor = _anchor(heading) if heading else ""
                rows.append((species, title, filename, anchor))
        books.append((book_name, rows))
    return books


def generate_box_register_text() -> str:
    """The full text of List_of_Boxes.md."""
    lines = [
        "# List of Boxes",
        "",
        "*Generated by `software/tools/build_table_register.py` from the box labels in"
        " both books — do not edit by hand. Regenerating this file should produce no"
        " diff (INV-10); if it doesn't, the register is stale.*",
        "",
        "*The five species are declared in the Front Matter, under **The Boxes**. A rule"
        " the game always uses is never in a box — anything listed here is optional,"
        " worked, or meta.*",
        "",
    ]
    for book_name, rows in collect_boxes():
        if not rows:
            continue
        lines += ["---", "", f"## {book_name}", "",
                  "| Box | Title | Section |", "|---|---|---|"]
        for species, title, filename, anchor in rows:
            link = _link(book_name, filename, anchor)
            shown = title or "(untitled)"
            lines.append(f"| **{species}** | [{shown}]({link}) | {filename} |")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text = generate_register_text()
    box_text = generate_box_register_text()
    if "--check" in argv:
        stale = []
        if (REGISTER_FILE.read_text() if REGISTER_FILE.exists() else "") != text:
            stale.append("List_of_Tables.md")
        if (BOX_REGISTER_FILE.read_text() if BOX_REGISTER_FILE.exists() else "") != box_text:
            stale.append("List_of_Boxes.md")
        if stale:
            print(f"{', '.join(stale)} stale — run `python -m tools.build_table_register`.")
            return 1
        print("Both registers are up to date.")
        return 0
    REGISTER_FILE.write_text(text)
    BOX_REGISTER_FILE.write_text(box_text)
    tables = sum(len(rows) for _, rows in collect_tables())
    boxes = sum(len(rows) for _, rows in collect_boxes())
    print(f"Wrote List_of_Tables.md ({tables} tables) and List_of_Boxes.md ({boxes} boxes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
