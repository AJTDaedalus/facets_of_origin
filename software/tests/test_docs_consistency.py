"""Consistency invariants for the three books, the module, and the ruleset data.

Lean Facets v1.0 (docs/DESIGN_lean_facets.md §6). The books are prose, but the
apparatus around them is mechanical, and every piece of it has an invariant a
machine can check. The v0.3 suite is preserved at tag `pre-lean-facets`; the
generic apparatus invariants carried over unchanged, the mechanic-specific ones
were rewritten against v1.

  INV-2   the Character Sheet names every field the character file carries
  INV-3   every Glossary entry's chapter pointer resolves and contains the term
  INV-4   Index.md is byte-identical to a fresh regeneration
  INV-5   every `Chapter X.Y` reference in the books resolves to a file
  INV-6   MM5 uses typographic dashes, not ASCII `--` / `-->`
  INV-7   facet.yaml's domain catalog matches the Magic Domain appendix
  INV-9   every lookup table carries a numbered caption, unique and 1..n per chapter
  INV-10  List_of_Tables.md and List_of_Boxes.md regenerate to no diff
  INV-11  no "see below" / "as mentioned above" — pointers must resolve
  INV-12  no capitalized term the Glossary does not define
  INV-13  every box declares a species, and Front Matter declares each
  INV-15  the Bestiary's stat blocks, finding aids, and Lore boxes are complete
  INV-16  every lineage gift domain resolves
  INV-17  a setting Facet is additive: it changes no core number
  INV-18  a module enemy reskin changes flavour only, never numbers
  INV-19  scene-card stat lines and pregen blocks regenerate to no diff
  INV-20  every `Chapter X.Y` reference in an adventure resolves
  INV-21  read-aloud blocks stay under 120 words
  INV-22  every talent has use/text/normal (talents also improved) and the
          books print it with a header that agrees with facet.yaml
  INV-23  every preset class resolves and is printed in its Facet chapter
  INV-24  every MM table covers its die exactly once
  INV-25  MM6's tables regenerate to no diff
  INV-26  the books print the numbers facet.yaml holds (weapon dice, grit
          dice, the monster level table)
  INV-27  no retired v0.3 term survives on a live rules surface

Also: worked example-of-play arithmetic agrees with the printed outcome tiers.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tools.build_index import generate_index_text

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYER_HANDBOOK = REPO_ROOT / "player_handbook"
MM_MANUAL = REPO_ROOT / "mm_manual"
BESTIARY = REPO_ROOT / "bestiary"
FACET_YAML = REPO_ROOT / "software" / "facets" / "base" / "facet.yaml"
CHARACTER_SHEET = PLAYER_HANDBOOK / "Appendix_Character_Sheet.md"
GLOSSARY = PLAYER_HANDBOOK / "Glossary.md"
INDEX_FILE = PLAYER_HANDBOOK / "Index.md"

# "Chapter II.4b", "Chapter III.3", "Chapter IV.1" — the number is the capture.
CHAPTER_REFERENCE = re.compile(r"Chapter ([IVX]+\.\d+[a-c]?)")


def _book_files() -> list[Path]:
    """Every markdown file in all three books, sorted for stable failure output.

    The Bestiary joined the line in 2026-08 as the third core book; it is held to
    the same apparatus invariants as the other two.
    """
    return (sorted(PLAYER_HANDBOOK.glob("*.md"))
            + sorted(MM_MANUAL.glob("*.md"))
            + sorted(BESTIARY.glob("*.md")))


def _chapter_numbers() -> dict[str, Path]:
    """Map each chapter number to its file, keyed on the filename prefix.

    `II.4b_Character_Creation_Facet_Mind.md` -> "II.4b". Files whose prefix is
    not a chapter number (MM1-MM5, Quick_Start, Table_of_Contents) are keyed on
    their prefix too; they simply never match a `Chapter X.Y` citation.
    """
    return {path.name.split("_", 1)[0]: path for path in _book_files()}


def test_cross_references_resolve() -> None:
    """INV-5: no `Chapter X.Y` citation points at a chapter that does not exist.

    The guard on renumbering (PA-2). Renaming a chapter by hand and hoping you
    caught every "see Chapter II.4" is how a book ships with a dangling
    reference.
    """
    known = _chapter_numbers()
    dangling: list[str] = []

    for path in _book_files():
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            for number in CHAPTER_REFERENCE.findall(line):
                if number not in known:
                    rel = path.relative_to(REPO_ROOT)
                    dangling.append(f"{rel}:{lineno} cites Chapter {number}")

    assert not dangling, "Unresolved chapter references:\n" + "\n".join(dangling)


# Markdown structure that legitimately contains runs of hyphens: thematic
# breaks (`---`) and table delimiter rows (`|---|---|`). Everything else in a
# line is prose, where `--` means someone typed an ASCII dash.
_THEMATIC_BREAK = re.compile(r"^\s*-{3,}\s*$")
_TABLE_DELIMITER = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def _prose_lines(path: Path) -> list[tuple[int, str]]:
    """Lines of a markdown file that carry prose, not table/rule syntax."""
    lines = []
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if _THEMATIC_BREAK.match(line) or _TABLE_DELIMITER.match(line):
            continue
        lines.append((lineno, line))
    return lines


def test_mm5_uses_typographic_dashes() -> None:
    """INV-6: MM5 prose contains no ASCII `--` or `-->`.

    Regression guard on the closed D8 finding. The quick reference once used
    `--` and `-->` where the rest of the books use em-dashes and `→`; those
    render as literal double-hyphens.
    """
    mm5 = MM_MANUAL / "MM5_Quick_Reference.md"
    offenders = [
        f"MM5_Quick_Reference.md:{lineno}: {line.strip()}"
        for lineno, line in _prose_lines(mm5)
        if "--" in line
    ]

    assert not offenders, "ASCII dashes in MM5 prose:\n" + "\n".join(offenders)


def _normalize(text: str) -> str:
    return " ".join(text.split())


# A Glossary entry: `**Term** — definition text. *(pointer)*`. The pointer is
# either a PHB citation (`Chapter II.4b`) or a bare MM manual citation (`MM1`)
# — the book's own convention never writes "Chapter MM1" (see Front_Matter.md,
# Table_of_Contents.md). The term may itself contain a parenthetical, e.g.
# "Posture (Aggressive/Measured/Defensive/Withdrawn)" — the non-greedy `.+?`
# for the bold term stops at the first `**`, not inside that parenthetical.
_GLOSSARY_ENTRY = re.compile(
    r"^\*\*(.+?)\*\* — .+? \*\((?:Chapter )?([A-Za-z0-9.]+)\)\*\s*$", re.M
)


def _glossary_entries() -> list[tuple[str, str]]:
    """[(term, chapter token), ...] parsed out of Glossary.md."""
    return _GLOSSARY_ENTRY.findall(GLOSSARY.read_text())


def test_glossary_pointers_resolve() -> None:
    """INV-3: every Glossary entry's chapter pointer resolves and contains the term.

    A glossary is a quick reference — it may only compress canonical body
    text (CLAUDE.md's quick-ref law). A pointer to a chapter that doesn't
    exist, or that doesn't actually contain the term it's citing, is a
    glossary lying about where its own definitions come from.
    """
    known = _chapter_numbers()
    errors: list[str] = []

    for term, chapter in _glossary_entries():
        path = known.get(chapter)
        if path is None:
            errors.append(f"{term!r}: pointer cites {chapter!r}, no such chapter")
            continue
        # The bold term may carry a parenthetical of variants
        # ("Reaction (Dodge/Parry/Absorb/Intercept)") — only the base word
        # before it needs to appear in the source chapter.
        base_term = term.split("(")[0].strip()
        if base_term.lower() not in path.read_text().lower():
            errors.append(
                f"{term!r}: {chapter!r} ({path.name}) does not contain {base_term!r}"
            )

    assert not errors, "Glossary pointer mismatches:\n" + "\n".join(errors)


# A domain heading in the appendix: `**Fire** *(Focused)*` on its own line. The
# appendix is canon; facet.yaml is a transcription of it.

def test_index_is_up_to_date() -> None:
    """INV-4: Index.md is byte-identical to a fresh regeneration.

    The lockfile pattern: `Index.md` is generated, not hand-maintained
    (PA-10), so the only thing that keeps it honest in a ruleset that's
    still moving is checking it was actually regenerated after the last
    change to the Glossary or either book.
    """
    assert INDEX_FILE.read_text() == generate_index_text(), (
        "Index.md is stale — regenerate with "
        "`python -m tools.build_index` (from software/)."
    )


# ---------------------------------------------------------------------------
# INV-9 / INV-10 / INV-11 / INV-12: the style-guide apparatus invariants.
#
# From docs/RESEARCH_style_audit.md, which measured the books against
# style/STYLE_GUIDE.md. The four findings these pin were each corpus-wide and
# each mechanically checkable, which is the only reason they are tests rather
# than review notes: a style rule nobody can run drifts back within two commits.
# ---------------------------------------------------------------------------

# "**Table III.3–2: Postures**" — chapter designation, en dash, sequence, title.
TABLE_CAPTION = re.compile(r"^\*\*Table ([A-Za-z0-9.]+)–(\d+): (.+?)\*\*$")

# A markdown table's header row is any `|` line followed by a `|---|---|` rule.
TABLE_RULE = re.compile(r"^\|[\s\-:|]+\|\s*$")

# Files that hold no lookup tables by design. The character sheet's grids are a
# blank form to fill in, not data to look up; the ToC, register, and index are
# navigation furniture whose tables *are* the finding aid.
NO_LOOKUP_TABLES = {
    "Appendix_Character_Sheet.md",
    "Table_of_Contents.md",
    "List_of_Tables.md",
    "List_of_Boxes.md",
    "Index.md",
}

# Pointers with no resolvable target. In a digital-first book with anchors, a
# bare "below" is strictly worse than a page number — there is nothing to click
# and nothing to flip to. Style guide Law 2; audit finding S6.
VAGUE_POINTERS = re.compile(
    r"\b(?:see|described|discussed|mentioned|noted)\s+"
    r"(?:the\s+)?(?:above|below|earlier|previously|next\s+section|example\s+below)\b",
    re.I,
)

# Terms the books capitalize that the Glossary does not define. Capitalization
# is a promise that a term has a definition somewhere; Law 5 keeps the capped
# set small and stable so the promise stays true. Audit finding S8.
# A line that is entirely a heading-style label — "**Table MM5-7: ...**",
# "> **Sidebar: ...**", "**Act II - Rising Action**". Title Case is correct in
# these positions (rulebooks.md §2), so they are exempt from the Law 5 check.
_TITLE_CASE_LABEL = re.compile(r"^>?\s*\*\*[^*]+\*\*:?\s*$")

#: An inline code span. Its contents are a literal name, not prose.
_INLINE_CODE = re.compile(r"`[^`]*`")

CAPITALIZABLE_CANDIDATES = [
    "Skill", "Skills", "Scene", "Scenes", "Roll", "Rolls", "Action", "Actions",
    "Check", "Checks", "Turn", "Turns",
]


def _table_header_lines(text: str) -> list[tuple[int, str]]:
    """Every markdown table header row: (1-indexed line number, line)."""
    lines = text.split("\n")
    headers = []
    for i, line in enumerate(lines):
        if (line.startswith("|")
                and i + 1 < len(lines)
                and TABLE_RULE.match(lines[i + 1])):
            headers.append((i + 1, line))
    return headers


def _fenced_line_numbers(text: str) -> set[int]:
    """1-indexed line numbers inside ``` fences — MM5 draws an ASCII card there."""
    inside = set()
    open_fence = False
    for i, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith("```"):
            open_fence = not open_fence
            continue
        if open_fence:
            inside.add(i)
    return inside


def test_every_table_carries_a_numbered_caption() -> None:
    """INV-9: every lookup table in either book has a `**Table X–N: Title**` line.

    Style guide Law 6 and rulebooks.md §8.6. The audit found ~50 tables and zero
    designations, which forced body text into "the table above" pointers and made
    a table register impossible to build.
    """
    offenders = []
    for path in _book_files():
        if path.name in NO_LOOKUP_TABLES:
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        fenced = _fenced_line_numbers(text)
        for number, header in _table_header_lines(text):
            if number in fenced:
                continue
            # The caption sits above the table, separated by one blank line.
            preceding = [ln for ln in lines[max(0, number - 4):number - 1] if ln.strip()]
            if not (preceding and TABLE_CAPTION.match(preceding[-1])):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: {header[:60]}")

    assert not offenders, (
        "These tables have no numbered caption. Add "
        "`**Table <chapter>–<n>: <Title>**` on the line above:\n"
        + "\n".join(offenders))


def test_table_designations_are_unique_and_sequential() -> None:
    """INV-9: no two tables share a designation, and each chapter counts from 1.

    A duplicate designation makes every citation to it ambiguous, which is worse
    than no designation at all.
    """
    by_chapter: dict[str, list[int]] = {}
    for path in _book_files():
        for line in path.read_text(encoding="utf-8").split("\n"):
            match = TABLE_CAPTION.match(line)
            if match:
                chapter, number, _ = match.groups()
                by_chapter.setdefault(chapter, []).append(int(number))

    problems = []
    for chapter, numbers in sorted(by_chapter.items()):
        if len(numbers) != len(set(numbers)):
            problems.append(f"{chapter}: duplicate numbers in {numbers}")
        if sorted(numbers) != list(range(1, len(numbers) + 1)):
            problems.append(f"{chapter}: not 1..n — {sorted(numbers)}")

    assert not problems, "Table designations are broken:\n" + "\n".join(problems)


def test_table_register_is_up_to_date() -> None:
    """INV-10: both registers are byte-identical to a fresh regeneration.

    Same contract as INV-4 for the Index: a stale finding aid misdirects with
    confidence, so staleness is a test failure rather than a review note.
    """
    from tools.build_table_register import (
        BOX_REGISTER_FILE, REGISTER_FILE,
        generate_box_register_text, generate_register_text,
    )

    for path, generate in ((REGISTER_FILE, generate_register_text),
                           (BOX_REGISTER_FILE, generate_box_register_text)):
        assert path.exists(), (
            f"{path.name} is missing — generate it with "
            f"`python -m tools.build_table_register` (from software/).")
        assert path.read_text(encoding="utf-8") == generate(), (
            f"{path.name} is stale — regenerate with "
            f"`python -m tools.build_table_register` (from software/).")


def test_no_vague_cross_references() -> None:
    """INV-11: no "see below" / "as mentioned above" pointers in either book.

    Style guide Law 2 and gm_books.md §9. Cite by section name and number —
    `(see Reactions, III.3)` — or by table designation. Audit finding S6.
    """
    offenders = []
    for path in _book_files():
        if path.name in {"Index.md", "List_of_Tables.md", "List_of_Boxes.md"}:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            match = VAGUE_POINTERS.search(line)
            if match:
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: ...{match.group(0)}...")

    assert not offenders, (
        "These pointers have no resolvable target. Cite the section by name and "
        "number, or the table by designation:\n" + "\n".join(offenders))


def test_capitalized_terms_are_glossary_defined() -> None:
    """INV-12: the books do not capitalize terms the Glossary never defines.

    Style guide Law 5: capitalize only formally defined terms; "roll", "check",
    and "scene" stay lowercase. Wall-to-wall capitalization of Every Cool Noun is
    on the guide's amateur-tells list. Audit finding S8.
    """
    from tools.build_index import parse_glossary_terms

    defined = set()
    for term in parse_glossary_terms():
        defined.add(term)
        defined.add(term + "s")

    undefined = [t for t in CAPITALIZABLE_CANDIDATES if t not in defined]
    pattern = re.compile(
        r"(?<=[a-z,;)])\s+(" + "|".join(undefined) + r")\b")

    offenders = []
    for path in _book_files():
        if path.name in {"Index.md", "List_of_Tables.md", "List_of_Boxes.md", "Glossary.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        fenced = _fenced_line_numbers(text)
        for number, line in enumerate(text.split("\n"), 1):
            # Headings and run-in field labels are Title Case by convention
            # (rulebooks.md §2) — "## Group Rolls" is a B-head, not prose.
            if number in fenced or line.startswith(("|", "#")):
                continue
            if _TITLE_CASE_LABEL.match(line.strip()):
                continue
            # An inline code span is a literal — a filename, a field, a UI
            # control like `End Scene`. Capitalisation inside one is the thing's
            # actual name, not a claim that it is a defined game term, so it is
            # blanked before the scan rather than exempted case by case.
            scanned = _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)
            for match in pattern.finditer(scanned):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: '{match.group(1)}' "
                    f"in: {line.strip()[:80]}")

    assert not offenders, (
        f"These terms are capitalized mid-sentence but not defined in the "
        f"Glossary ({', '.join(undefined)}). Lowercase them, or define them:\n"
        + "\n".join(offenders[:40])
        + (f"\n... and {len(offenders) - 40} more" if len(offenders) > 40 else ""))


# The five box species declared in Front_Matter.md's "The Boxes" section. A box
# whose label is not one of these is an undeclared species, which is the exact
# thing gm_books.md §8.2 forbids ("never introduce an undeclared box species
# later"). Audit finding S2.
BOX_SPECIES = ("Through the Mirror", "MM Note", "Example", "Variant",
               "Reading the Entries", "What Characters Can Know")

# The first line of a box: "> **MM Note — The golden rule**".
BOX_LABEL = re.compile(r"^>\s*\*\*(.+?)\*\*")


def _box_openers(text: str) -> list[tuple[int, str]]:
    """Every blockquote's first line: (1-indexed line number, label or '')."""
    openers = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(">") and (i == 0 or not lines[i - 1].startswith(">")):
            match = BOX_LABEL.match(line)
            openers.append((i + 1, match.group(1) if match else ""))
    return openers


def test_every_box_declares_its_species() -> None:
    """INV-13: every boxed sidebar opens with one of the declared species.

    Style guide Law 6 and gm_books.md §8.2. The audit found ~40 boxes using three
    incompatible label syntaxes and no declaration anywhere, so a reader had no
    way to know whether a given box was a rule, an aside, or a joke.
    """
    offenders = []
    for path in _book_files():
        if path.name in {"Index.md", "List_of_Tables.md", "List_of_Boxes.md", "Front_Matter.md"}:
            continue
        for number, label in _box_openers(path.read_text(encoding="utf-8")):
            if not any(label.startswith(species) for species in BOX_SPECIES):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: "
                    f"{label[:60] or '(no label)'}")

    assert not offenders, (
        f"These boxes do not declare a species ({', '.join(BOX_SPECIES)}). "
        f"A rule the game always uses belongs in body text, not a box:\n"
        + "\n".join(offenders))


def test_front_matter_declares_every_species_in_use() -> None:
    """INV-13: the taxonomy in Front_Matter covers every species the books use.

    The declaration and the usage are two halves of one contract; this is the
    half that catches a species added to the books but never announced.
    """
    front_matter = (PLAYER_HANDBOOK / "Front_Matter.md").read_text(encoding="utf-8")
    assert "## The Boxes" in front_matter, (
        "Front_Matter.md has no box taxonomy — the books' boxes are undeclared.")

    used = set()
    for path in _book_files():
        if path.name in {"Index.md", "List_of_Tables.md", "List_of_Boxes.md", "Front_Matter.md"}:
            continue
        for _, label in _box_openers(path.read_text(encoding="utf-8")):
            for species in BOX_SPECIES:
                if label.startswith(species):
                    used.add(species)

    undeclared = [s for s in sorted(used) if f"**{s}**" not in front_matter]
    assert not undeclared, (
        f"These box species are used but not declared in Front_Matter.md's "
        f"'The Boxes': {undeclared}")



def test_bestiary_is_up_to_date() -> None:
    """INV-15: every Bestiary stat block and its finding aids regenerate to no diff.

    The Bestiary's prose is hand-written and its numbers are not: each chapter
    marks where a block goes and the generator fills it from `enemies/*.fof`. The
    book therefore cannot disagree with the stat files about a creature's Resolve,
    which makes `monster_books.md` §9's format-drift anti-pattern structurally
    impossible rather than merely discouraged. Audit finding E1.
    """
    from tools.build_bestiary import build

    changed = build(write=False)
    assert not changed, (
        f"Bestiary is stale ({', '.join(changed)}) — regenerate with "
        f"`python -m tools.build_bestiary` (from software/).")


def test_every_bestiary_creature_is_in_the_finding_aids() -> None:
    """INV-15: no creature has an entry the level-sorted list does not carry.

    `monster_books.md` §1: the difficulty-sorted list is the single most-used
    finding aid an MM has. One it does not list is one nobody finds.
    """
    from tools.build_bestiary import FINDING_AIDS, load_enemies, referenced_ids

    aids = FINDING_AIDS.read_text(encoding="utf-8")
    enemies = load_enemies()
    missing = [enemies[eid].name for eid in referenced_ids()
               if enemies[eid].name not in aids]
    assert not missing, f"Not listed in Finding_Aids.md: {missing}"


def test_every_bestiary_creature_has_a_lore_box() -> None:
    """INV-15: every family entry ships its tiered "What Characters Can Know" box.

    `monster_books.md` §8.11 — three to five tiers of what characters can know,
    each written as sentences the MM can read aloud. This is the device that
    rations lore deliberately instead of by accident, and it is the FoO-native
    one: the tiers are the outcome tiers. Audit finding P6.
    """
    from tools.build_bestiary import BESTIARY_DIR, CHAPTERS

    problems = []
    for name in CHAPTERS:
        text = (BESTIARY_DIR / name).read_text(encoding="utf-8")
        families = re.findall(r"^## (.+)$", text, re.M)
        boxes = re.findall(r"^> \*\*What Characters Can Know", text, re.M)
        if len(boxes) < len(families):
            problems.append(
                f"{name}: {len(families)} families, {len(boxes)} Lore boxes")
        for box in re.finditer(
                r"^> \*\*What Characters Can Know.+?(?=\n\n)", text, re.M | re.S):
            for tier in ("6−", "7–9", "10+"):
                if tier not in box.group(0):
                    problems.append(f"{name}: a Lore box has no {tier} row")

    assert not problems, "Lore boxes are incomplete:\n" + "\n".join(problems)



# ---------------------------------------------------------------------------
# INV-8b  worked example-of-play arithmetic reconciles with the printed tiers
# ---------------------------------------------------------------------------

_ROLL_LINE = re.compile(
    r"^→ .*?\bgets? (?:a|an) \*\*(\d+)\*\*\.\s*(Full success|Partial success|Failure)\b",
)


def _example_roll_lines(text: str):
    for lineno, line in enumerate(text.split("\n"), start=1):
        m = _ROLL_LINE.match(line.strip())
        if m:
            yield lineno, int(m.group(1)), m.group(2)


def test_example_of_play_rolls_match_the_outcome_tiers() -> None:
    """A worked example that narrates a partial success off a 10 teaches the
    table the wrong game, and it is the kind of error that survives every
    other check in this file — the prose is well-formed, the cross-references
    resolve, and only the arithmetic is wrong.

    Every `→ ... gets a **N**. <Outcome>` line in either book is checked
    against the printed thresholds (10+ full, 7-9 partial, 6- failure), which
    are read from the ruleset rather than restated here.
    """
    from app.facets.registry import build_ruleset

    tiers = {t.id: t.threshold for t in build_ruleset([]).roll_resolution.outcome_tiers}
    full, partial = tiers["full_success"], tiers["partial_success"]

    def expected(total: int) -> str:
        if total >= full:
            return "Full success"
        if total >= partial:
            return "Partial success"
        return "Failure"

    problems = []
    checked = 0
    for path in sorted(PLAYER_HANDBOOK.glob("*.md")) + sorted(MM_MANUAL.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for lineno, total, stated in _example_roll_lines(text):
            checked += 1
            if stated != expected(total):
                problems.append(
                    f"{path.name}:{lineno} — a {total} is {expected(total)}, "
                    f"but the example says {stated}"
                )

    assert checked, "no worked example rolls found — has the → notation changed?"
    assert not problems, "worked example arithmetic disagrees with the tiers:\n" + "\n".join(problems)



# ---------------------------------------------------------------------------
# INV-19  scene-card stat lines regenerate to no diff
# INV-20  a module's `Chapter X.Y` pointers resolve
# INV-21  read-aloud blocks stay short enough to read aloud
# ---------------------------------------------------------------------------

ADVENTURE_DIRS = sorted(p for p in (REPO_ROOT / "adventures").iterdir() if p.is_dir())


def test_scene_card_statlines_are_up_to_date() -> None:
    """INV-19. A scene card's numbers are generated from the module's enemy
    files, exactly as the Bestiary's stat blocks are.

    The failure this prevents is specific and expensive: someone retunes an
    enemy after a simulation, the card still shows the old Resolve, and the
    MM runs a fight that was never tested at the numbers in front of them.
    """
    from tools.build_scene_cards import build

    stale = build(write=False)
    assert not stale, (
        "Scene card stat lines are stale — regenerate with "
        "`python -m tools.build_scene_cards` (from software/):\n  "
        + "\n  ".join(stale))


def test_pregen_blocks_are_up_to_date() -> None:
    """The same no-diff rule as the scene cards, applied to the pregenerated
    characters.

    A pregen used to exist twice — a paragraph of prose in the module, and a
    block of numbers somebody typed under it — and the two could disagree
    without anything noticing. They now have one source, `characters/*.fof`,
    and the printed block is generated from it. `build_scene_cards` fills both
    kinds of marker, so this shares its check.
    """
    from tools.build_scene_cards import build

    stale = build(write=False)
    assert not stale, (
        "Pregen or scene-card blocks are stale — regenerate with "
        "`python -m tools.build_scene_cards` (from software/):\n  "
        + "\n  ".join(stale))


def test_module_chapter_references_resolve() -> None:
    """INV-20 (INV-5 extended to `adventures/`). A module cites the rulebooks
    constantly — "see *Strike*, III.3" — and a renumber that misses the
    adventures leaves a starter module pointing new tables at chapters that do
    not exist. This is the guard the II.5 renumber wanted and did not have.
    """
    known = _chapter_numbers()
    dangling: list[str] = []
    for module_dir in ADVENTURE_DIRS:
        for path in sorted(module_dir.rglob("*.md")):
            for lineno, line in enumerate(path.read_text().splitlines(), start=1):
                for number in CHAPTER_REFERENCE.findall(line):
                    if number not in known:
                        dangling.append(
                            f"{path.relative_to(REPO_ROOT)}:{lineno} cites "
                            f"Chapter {number}")
    assert not dangling, ("Unresolved chapter references in adventures:\n"
                          + "\n".join(dangling))


def _read_aloud_blocks(text: str):
    """Yield (line number, words) for every read-aloud block in a module.

    A read-aloud block is a *paragraph* of blockquote whose content is
    italicised — which means consecutive `> ` lines have to be joined before
    anything is measured. Matching one line at a time (the first version of
    this check) silently exempted every multi-line block, which is to say it
    exempted exactly the blocks most likely to be too long. It also counted
    every one-line italic aside — a Q&A question, a handout caption — as a
    read-aloud, so it was loud about the wrong things and quiet about the right
    ones.
    """
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].startswith(">"):
            i += 1
            continue
        start = i
        chunk = []
        while i < len(lines) and lines[i].startswith(">"):
            chunk.append(lines[i].lstrip("> ").rstrip())
            i += 1
        body = " ".join(part for part in chunk if part).strip()
        # Italic-wrapped, and not a bolded sidebar header (**Sidebar — ...**).
        if body.startswith("*") and body.endswith("*") and not body.startswith("**"):
            yield start + 1, len(body.strip("*").split())


def test_read_aloud_blocks_stay_readable() -> None:
    """INV-21. Nothing anyone will actually say at a table runs past 120 words.

    A long read-aloud is not a style problem, it is a play problem: the table
    stops listening halfway, the MM loses the room, and the detail that
    mattered was in the second half. The style analysis puts the target at
    2-6 sentences; 120 words is the outer bound that catches a runaway.
    """
    offenders: list[str] = []
    for module_dir in ADVENTURE_DIRS:
        for path in sorted(module_dir.rglob("*.md")):
            for lineno, words in _read_aloud_blocks(path.read_text()):
                if words > 120:
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}:{lineno} — {words} words")
    assert not offenders, ("Read-aloud blocks too long to read aloud:\n"
                           + "\n".join(offenders))


def test_the_read_aloud_check_actually_sees_multiline_blocks() -> None:
    """The guard on the guard. An invariant that cannot fail is decoration, and
    this one silently could not: its first version matched a single line at a
    time, so a 300-word block spread over six lines passed."""
    long_block = "> *" + " ".join(["word"] * 200) + "\n> more words here.*"
    found = list(_read_aloud_blocks(long_block))
    assert found and found[0][1] > 120

    short_block = "> *The whole hill is lit. Nobody is hurrying.*"
    assert list(_read_aloud_blocks(short_block))[0][1] < 120

    # A bolded sidebar is not a read-aloud and must not be measured as one.
    assert not list(_read_aloud_blocks("> **Sidebar — steel at the ball**"))



# ---------------------------------------------------------------------------
# Lean Facets v1.0 invariants (INV-2, 7, 16-18, 22-27)
# ---------------------------------------------------------------------------

def _facet() -> dict:
    return yaml.safe_load(FACET_YAML.read_text(encoding="utf-8"))


FACET_CHAPTERS = {
    "body": PLAYER_HANDBOOK / "II.4a_Character_Creation_Facet_Body.md",
    "mind": PLAYER_HANDBOOK / "II.4b_Character_Creation_Facet_Mind.md",
    "soul": PLAYER_HANDBOOK / "II.4c_Character_Creation_Facet_Soul.md",
}

# `**Weapon Master** *(Body, talent — passive)*` — the talent entry header.
TALENT_HEAD = re.compile(
    r"^\*\*([^*]+)\*\* \*\(((?:Body|Mind|Soul)(?: and (?:Body|Mind|Soul))?), "
    r"(talent|signature) — ([^)]+)\)\*\s*$", re.M)

_USE_WORDS = {
    "passive": "passive",
    "at_will": "at will",
    "once_per_scene": "once per scene",
    "once_per_session": "once per session",
    "once_per_rest": "once per rest",
}

CHARACTER_SHEET_LABELS = [
    "Facet", "Class", "Level", "Body", "Mind", "Soul", "HP", "Knacks",
    "Specialty", "Background", "Lineage", "Talents", "Signature", "Slots",
    "Fatigue", "Wounds", "Sparks", "Coin",
]


def test_character_sheet_names_every_character_field() -> None:
    """INV-2: the printed sheet carries a place for every field the character
    file does (DESIGN §3.3). A sheet missing HP or Slots is a sheet a player
    cannot play from."""
    sheet = CHARACTER_SHEET.read_text(encoding="utf-8")
    missing = [label for label in CHARACTER_SHEET_LABELS if label not in sheet]
    assert not missing, f"Character sheet has no place for: {missing}"


_APPENDIX_DOMAIN = re.compile(r"^\*\*([A-Z][\w '&-]+?)\*\* \*\(([^)]*)\)\*\s*$", re.M)
DOMAIN_APPENDIX = PLAYER_HANDBOOK / "Appendix_Magic_Domains.md"


def test_domain_catalog_matches_appendix() -> None:
    """INV-7: facet.yaml's domain catalog is the appendix, transcribed — same
    names, and the prismatic ones marked prismatic in both."""
    catalog = {d["name"]: d for d in _facet()["magic_domains"]}
    appendix = dict(_APPENDIX_DOMAIN.findall(DOMAIN_APPENDIX.read_text(encoding="utf-8")))
    errors = []
    for name in sorted(set(catalog) - set(appendix)):
        errors.append(f"{name}: in facet.yaml, missing from the appendix")
    for name in sorted(set(appendix) - set(catalog)):
        errors.append(f"{name}: in the appendix, missing from facet.yaml")
    for name in sorted(set(catalog) & set(appendix)):
        says_prismatic = "prismatic" in appendix[name].lower()
        if says_prismatic != bool(catalog[name].get("prismatic")):
            errors.append(f"{name}: prismatic flag disagrees")
    assert not errors, "Domain catalog / appendix mismatches:\n" + "\n".join(errors)


def test_every_talent_has_its_fields_in_facet_yaml() -> None:
    """INV-22 (data half): every talent carries use, text and normal, and every
    menu talent (not a signature) has an improved form."""
    problems = []
    for t in _facet()["talents"]:
        for field in ("use", "text", "normal"):
            if not t.get(field):
                problems.append(f"{t['id']}: no {field}")
        if t["kind"] == "talent" and not t.get("improved"):
            problems.append(f"{t['id']}: a menu talent with no improved form")
        if t["use"] not in _USE_WORDS:
            problems.append(f"{t['id']}: unknown use {t['use']!r}")
    assert not problems, "\n".join(problems)


def test_every_talent_is_printed_with_a_matching_header() -> None:
    """INV-22 (book half): each talent appears in its Facet's chapter with a
    header whose Facet, kind and use agree with facet.yaml, and the entry
    prints its Normal line (and Improved line for menu talents)."""
    problems = []
    printed: dict[str, tuple[str, str, str, str]] = {}
    for facet_id, path in FACET_CHAPTERS.items():
        text = path.read_text(encoding="utf-8")
        for match in TALENT_HEAD.finditer(text):
            name, facet, kind, use = match.groups()
            entry = text[match.end():].split("\n**", 1)[0]
            rest = text[match.end():]
            nxt = TALENT_HEAD.search(rest)
            entry = rest[: nxt.start()] if nxt else rest
            # A shared talent prints "Mind and Soul"; its home Facet is the first.
            printed.setdefault(name, (facet.split(" and ")[0].lower(), kind,
                                      use.strip().lower(), entry))
    for t in _facet()["talents"]:
        got = printed.get(t["name"])
        if got is None:
            problems.append(f"{t['name']}: not printed in {FACET_CHAPTERS[t['facet']].name}")
            continue
        facet, kind, use, entry = got
        if facet != t["facet"]:
            problems.append(f"{t['name']}: printed under {facet}, data says {t['facet']}")
        if kind != t["kind"]:
            problems.append(f"{t['name']}: printed as {kind}, data says {t['kind']}")
        if use != _USE_WORDS[t["use"]]:
            problems.append(f"{t['name']}: printed use {use!r}, data says {_USE_WORDS[t['use']]!r}")
        if "**Normal:**" not in entry:
            problems.append(f"{t['name']}: no Normal line")
        if t["kind"] == "talent" and "**Improved:**" not in entry:
            problems.append(f"{t['name']}: no Improved line")
    assert not problems, "Talent entries disagree with facet.yaml:\n" + "\n".join(problems)


def test_every_preset_class_resolves_and_is_printed() -> None:
    """INV-23: a preset's talents, signature and kit exist, belong to its Facet,
    and the preset appears in its Facet chapter."""
    data = _facet()
    talents = {t["id"]: t for t in data["talents"]}
    items = {i["id"] for i in data["equipment"]["items"]}
    problems = []
    for c in data["classes"]:
        for tid in c["talents"] + [c["signature"]]:
            t = talents.get(tid)
            if t is None:
                problems.append(f"{c['id']}: unknown talent {tid}")
            elif t["facet"] != c["facet"] and c["facet"] not in t.get("shared_with", []):
                problems.append(f"{c['id']}: {tid} is not on the {c['facet']} menu")
        if talents.get(c["signature"], {}).get("kind") != "signature":
            problems.append(f"{c['id']}: signature {c['signature']} is not a signature")
        for k in c["kit"]:
            if k not in items:
                problems.append(f"{c['id']}: unknown kit item {k}")
        if c["name"] not in FACET_CHAPTERS[c["facet"]].read_text(encoding="utf-8"):
            problems.append(f"{c['name']}: not printed in its Facet chapter")
    assert not problems, "\n".join(problems)


TABLES_YAML = REPO_ROOT / "software" / "facets" / "base" / "tables.yaml"


def _die_faces(die: str) -> list[str]:
    if die == "d66":
        return [f"{a}{b}" for a in range(1, 7) for b in range(1, 7)]
    if die == "2d6":
        return [str(n) for n in range(2, 13)]
    sides = int(die.split("d")[1])
    return [str(n) for n in range(1, sides + 1)]


def _expand(roll: str) -> list[str]:
    roll = str(roll).replace("–", "-")
    if "-" in roll:
        lo, hi = roll.split("-")
        if len(lo) == 2 and len(hi) == 2 and lo[0] != hi[0]:
            faces = [f"{a}{b}" for a in range(1, 7) for b in range(1, 7)]
            return [f for f in faces if lo <= f <= hi]
        return [str(n) for n in range(int(lo), int(hi) + 1)]
    return [roll]


REQUIRED_TABLES = [
    "reaction", "reaction_wants", "pressure_generic", "pressure_underground",
    "pressure_wild", "pressure_settlement", "pressure_occasion", "trouble",
    "complications_fight", "complications_explore", "complications_social",
    "magic_complications", "magic_mishaps", "wounds", "scars", "trinkets",
    "curios", "relics", "npc_names", "npc_traits", "npc_wants", "npc_secrets",
    "oracle_actions", "oracle_themes",
]


def test_every_mm_table_covers_its_die_exactly_once() -> None:
    """INV-24: a table with a gap is a table the app cannot roll, and one with
    an overlap is a table the MM reads two ways."""
    tables = yaml.safe_load(TABLES_YAML.read_text(encoding="utf-8"))["tables"]
    by_id = {t["id"]: t for t in tables}
    problems = [f"missing table {tid}" for tid in REQUIRED_TABLES if tid not in by_id]
    for t in tables:
        seen: list[str] = []
        for e in t["entries"]:
            seen.extend(_expand(e["roll"]))
        faces = _die_faces(t["die"])
        if sorted(seen) != sorted(faces):
            extra = sorted(set(seen) - set(faces))
            gaps = sorted(set(faces) - set(seen))
            dupes = sorted({x for x in seen if seen.count(x) > 1})
            problems.append(f"{t['id']} ({t['die']}): gaps {gaps} extra {extra} dupes {dupes}")
        if any(not str(e.get("text", "")).strip() for e in t["entries"]):
            problems.append(f"{t['id']}: an entry with no text")
    assert not problems, "\n".join(problems)


def test_mm6_tables_are_up_to_date() -> None:
    """INV-25: MM6's tables are generated from tables.yaml, like the Bestiary's
    stat blocks, so the book and the app cannot disagree about a table."""
    from tools.build_toolbox import build
    stale = build(write=False)
    assert not stale, (
        f"MM6 is stale ({stale}) — regenerate with `python -m tools.build_toolbox`.")


def test_books_print_the_weapon_and_grit_dice() -> None:
    """INV-26: every weapon category's die and every Facet's grit die is printed
    as facet.yaml holds it."""
    data = _facet()
    equipment = (PLAYER_HANDBOOK / "IV.1_Equipment.md").read_text(encoding="utf-8")
    problems = []
    for cat, spec in data["equipment"]["weapon_categories"].items():
        row = next((ln for ln in equipment.splitlines()
                    if ln.startswith("|") and cat.lower() in ln.lower()), None)
        if row is None or f"d{spec['die']}" not in row:
            problems.append(f"IV.1: no table row printing {cat} as d{spec['die']}")
    facets_chapter = (PLAYER_HANDBOOK / "II.4_Character_Creation_Facets.md").read_text(encoding="utf-8")
    for f in data["facets"]:
        if f"d{f['grit_die']}" not in facets_chapter:
            problems.append(f"II.4: {f['id']} grit die d{f['grit_die']} not printed")
    assert not problems, "\n".join(problems)


def test_mm1_prints_the_monster_level_table() -> None:
    """INV-26: the MM builds monsters from MM1's level table, the app from
    facet.yaml's; each level's row must carry the same HP, damage and attack."""
    mm1 = (MM_MANUAL / "MM1_Encounters_and_Enemies.md").read_text(encoding="utf-8")
    problems = []
    for row in _facet()["monsters"]["level_table"]:
        pattern = re.compile(
            rf"^\|\s*{row['level']}\s*\|\s*{row['hp']}\s*\|\s*{row['damage']}\s*\|\s*\+?{row['attack']}\s*\|", re.M)
        if not pattern.search(mm1):
            problems.append(f"level {row['level']}: no row | {row['level']} | {row['hp']} | {row['damage']} | +{row['attack']} |")
    assert not problems, "MM1's level table disagrees with facet.yaml:\n" + "\n".join(problems)


# Retired v0.3 rules vocabulary. Each is a term of art that no longer exists.
RETIRED_TERMS: list[tuple[str, str]] = [
    (r"\bEndurance Pool\b", "L7: grit HP and slots replace the Endurance Pool"),
    (r"\bPostures?\b", "L2/L7: postures are cut"),
    (r"\bResolve (?:pool|\d)", "L3: enemies have HP"),
    (r"\bdepletes? (?:its |an enemy's |the enemy's )?Resolve", "L3"),
    (r"\bThreat Rating\b", "L3: monsters are levelled, not rated"),
    (r"\bTR \d", "L3"),
    (r"\bTechniques?\b", "L9: talents replace Techniques"),
    (r"\bFacet levels?\b", "L8: levels replace Facet levels"),
    (r"\bskill points?\b", "L8"),
    (r"\bMinor Attributes?\b", "L4"),
    (r"\bMajor Attributes?\b", "L4"),
    (r"\breadied intents?\b", "L5: Fatigue replaces readied intents"),
    (r"\bTier [12] Conditions?\b", "L3/L7"),
    (r"\bManeuver\b", "L7: stunts replace Maneuver"),
    (r"\bAbsorb\b", "L2: enemies roll; no reactions"),
    (r"\bParry\b", "L2"),
    (r"\bEncounter Recipe", "L3"),
    (r"\bcareer[_ ]advances\b", "L8"),
    (r"\bMajor Advancement\b", "L8"),
    (r"\bAscendant Domain\b", "L6"),
]

_RETIRED_SCAN = ["player_handbook", "mm_manual", "bestiary", "adventures",
                 "settings", "characters", "enemies", "software/facets",
                 "software/app/static"]


def test_no_retired_term_survives() -> None:
    """INV-27: a rewrite that lands in one file and misses its siblings is the
    drift this project has fought every release. No v0.3 term of art may
    survive on a live rules surface."""
    patterns = [(re.compile(p), why) for p, why in RETIRED_TERMS]
    offenders = []
    for rel in _RETIRED_SCAN:
        root = REPO_ROOT / rel
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if path.suffix not in {".md", ".yaml", ".fof", ".js", ".html", ".css"}:
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for pat, why in patterns:
                    if pat.search(line):
                        offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno} {pat.pattern} ({why})")
    assert not offenders, ("Retired v0.3 terms survive:\n" + "\n".join(offenders[:60])
                           + (f"\n... and {len(offenders) - 60} more" if len(offenders) > 60 else ""))


# ---------------------------------------------------------------------------
# INV-16 / 17 / 18: setting Facets and module reskins
# ---------------------------------------------------------------------------

VALLOH_FACET = REPO_ROOT / "software" / "facets" / "valloh" / "facet.yaml"
VALLOH_BOOK = REPO_ROOT / "settings" / "valloh"
_CORE_RULE_SECTIONS = ("stats", "stat_rules", "facets", "roll_resolution", "spark",
                       "advancement", "hp", "recovery", "wounds", "hold_on", "death",
                       "slots", "magic", "combat", "monsters", "hazards", "exploration")


def test_setting_facet_changes_no_core_rule() -> None:
    """INV-17: a setting Facet is additive. It may add lineages, items, talents,
    classes, backgrounds, domains and tables; it may not write a core rule."""
    data = yaml.safe_load(VALLOH_FACET.read_text(encoding="utf-8"))
    written = [s for s in _CORE_RULE_SECTIONS if data.get(s)]
    assert not written, f"the Val'loh Facet writes core rule sections: {written}"


def test_setting_facet_loads_without_changing_the_core() -> None:
    """INV-17: loading the setting leaves the core's numbers as they were."""
    from app.facets.registry import build_ruleset
    base = build_ruleset([])
    with_setting = build_ruleset(["valloh"])
    assert base.to_client_dict().get("combat") == with_setting.to_client_dict().get("combat")
    assert base.to_client_dict().get("advancement") == with_setting.to_client_dict().get("advancement")


def test_lineage_gift_domains_resolve() -> None:
    """INV-16: a lineage that names a gift domain names a real one."""
    known = {d["id"] for d in _facet()["magic_domains"]}
    data = yaml.safe_load(VALLOH_FACET.read_text(encoding="utf-8"))
    known |= {d["id"] for d in data.get("magic_domains") or []}
    problems = []
    for lin in (data.get("lineages") or []) + _facet()["lineages"]:
        for dom in lin.get("gift_domains") or []:
            if dom not in known:
                problems.append(f"{lin['id']}: gift domain {dom} resolves to nothing")
    assert not problems, "\n".join(problems)


def test_valloh_book_and_data_agree_on_the_lineages() -> None:
    """Every playable lineage in the data has an entry in V1."""
    data = yaml.safe_load(VALLOH_FACET.read_text(encoding="utf-8"))
    text = (VALLOH_BOOK / "V1_Lineages.md").read_text(encoding="utf-8")
    missing = [lin["name"] for lin in data.get("lineages") or []
               if lin.get("playable", True) and lin["name"] not in text]
    assert not missing, f"lineages missing from V1: {missing}"


MODULE_ENEMY_DIRS = sorted((REPO_ROOT / "adventures").glob("*/enemies"))
_MECHANICAL_ENEMY_FIELDS = ("level", "role", "armor", "morale", "hp", "damage",
                            "attack", "attacks", "special", "when_bloodied")


def test_module_enemy_reskins_do_not_fork_the_numbers() -> None:
    """INV-18: a module may reskin a Bestiary enemy's flavour; never its numbers."""
    problems = []
    for enemy_dir in MODULE_ENEMY_DIRS:
        for path in sorted(enemy_dir.glob("*.fof")):
            here = yaml.safe_load(path.read_text(encoding="utf-8"))["enemy"]
            original = here.get("reskin_of") or (path.stem if (REPO_ROOT / "enemies" / path.name).exists() else None)
            if not original:
                continue
            there = yaml.safe_load((REPO_ROOT / "enemies" / f"{original}.fof").read_text(encoding="utf-8"))["enemy"]
            for field in ("level", "role", "armor", "morale", "hp", "damage", "attack", "attacks"):
                if here.get(field) != there.get(field):
                    problems.append(f"{path.relative_to(REPO_ROOT)} changes {field}: {there.get(field)!r} -> {here.get(field)!r}")
    assert not problems, "\n".join(problems)


def test_the_bestiary_originals_stay_setting_agnostic() -> None:
    """B9: no Bestiary enemy names a setting."""
    setting_words = ("Val'loh", "Rekuzan", "Orthaen", "Oraga", "Boranis", "Blackwatch")
    offenders = [f"{p.name}: {w!r}" for p in sorted((REPO_ROOT / "enemies").glob("*.fof"))
                 for w in setting_words if w in p.read_text(encoding="utf-8")]
    assert not offenders, "\n".join(offenders)


def test_every_enemy_card_is_complete() -> None:
    """A card missing its gimmick or its twists is a card that plays as a bag of
    HP — the exact failure the card format exists to prevent."""
    problems = []
    for path in sorted((REPO_ROOT / "enemies").glob("*.fof")) + [
            p for d in MODULE_ENEMY_DIRS for p in sorted(d.glob("*.fof"))]:
        e = yaml.safe_load(path.read_text(encoding="utf-8"))["enemy"]
        for field in ("level", "role", "morale", "wants", "special", "breaks"):
            if e.get(field) in (None, ""):
                problems.append(f"{path.relative_to(REPO_ROOT)}: no {field}")
        if len(e.get("twists") or []) != 6:
            problems.append(f"{path.relative_to(REPO_ROOT)}: needs exactly six twists")
    assert not problems, "\n".join(problems)
