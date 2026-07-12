"""Consistency invariants for the PHB and MM Manual.

The books are prose, but the *apparatus* around them — cross-references,
glossary pointers, the character sheet, the generated index — is mechanical,
and every piece of it has an invariant a machine can check. This module is
where those live. See docs/DESIGN_production_apparatus.md §5 for the full
table (INV-1 through INV-6) and which task lands each one.

Currently implemented:
  INV-1  every skill's facet.yaml description matches its II.6 prose entry
  INV-2  every Character Sheet field maps to a real Character model attribute
  INV-3  every Glossary entry's chapter pointer resolves and contains the term
  INV-4  Index.md is byte-identical to a fresh regeneration
  INV-5  every `Chapter X.Y` reference in either book resolves to a file
  INV-6  MM5 uses typographic dashes, not ASCII `--` / `-->`
  INV-7  facet.yaml's domain catalog matches the Magic Domain appendix
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from app.game.character import Character
from tools.build_index import generate_index_text

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYER_HANDBOOK = REPO_ROOT / "player_handbook"
MM_MANUAL = REPO_ROOT / "mm_manual"
FACET_YAML = REPO_ROOT / "software" / "facets" / "base" / "facet.yaml"
SKILLS_CHAPTER = PLAYER_HANDBOOK / "II.6_Character_Creation_Skills.md"
CHARACTER_SHEET = PLAYER_HANDBOOK / "Appendix_Character_Sheet.md"
GLOSSARY = PLAYER_HANDBOOK / "Glossary.md"
INDEX_FILE = PLAYER_HANDBOOK / "Index.md"

# "Chapter II.4b", "Chapter III.3", "Chapter IV.1" — the number is the capture.
CHAPTER_REFERENCE = re.compile(r"Chapter ([IVX]+\.\d+[a-c]?)")


def _book_files() -> list[Path]:
    """Every markdown file in both books, sorted for stable failure output."""
    return sorted(PLAYER_HANDBOOK.glob("*.md")) + sorted(MM_MANUAL.glob("*.md"))


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


def _facet_yaml_skills() -> list[dict]:
    data = yaml.safe_load(FACET_YAML.read_text())
    return data["skills"]


# A skill entry in II.6's "The Skill List": a bold name, an italic governing
# attribute, then a prose paragraph running to the next blank line.
_SKILL_ENTRY = re.compile(
    r"\*\*([A-Za-z]+)\*\* \*\([A-Za-z]+\)\*\n(.+?)(?=\n\n|\Z)", re.S
)


def _skill_list_entries() -> dict[str, str]:
    """Parse {skill name: prose} out of II.6's "## The Skill List" section."""
    text = SKILLS_CHAPTER.read_text()
    start = text.index("## The Skill List")
    rest = text[start:]
    next_heading = re.search(r"\n## ", rest[1:])
    section = rest[: next_heading.start() + 1] if next_heading else rest
    return {
        name: _normalize(body) for name, body in _SKILL_ENTRY.findall(section)
    }


def test_skill_descriptions_match_facet_yaml() -> None:
    """INV-1: facet.yaml's `description` for every skill is the canonical prose.

    Four copies of every skill description used to drift independently. Now
    there are two coupled homes — data (facet.yaml) and prose (II.6) — and
    this is what stops them from becoming two different rules. II.6 may add
    a trailing usage sentence; it must not alter or contradict the data
    description itself, so the check is verbatim substring containment.
    """
    entries = _skill_list_entries()
    mismatches: list[str] = []

    for skill in _facet_yaml_skills():
        name = skill["name"]
        expected = _normalize(skill["description"])
        prose = entries.get(name)
        if prose is None:
            mismatches.append(f"{name}: no entry in II.6 'The Skill List'")
        elif expected not in prose:
            mismatches.append(
                f"{name}: facet.yaml description not found verbatim in II.6\n"
                f"    facet.yaml: {expected}\n"
                f"    II.6:       {prose}"
            )

    assert not mismatches, "Skill description mismatches:\n" + "\n".join(mismatches)


# Every field on Appendix_Character_Sheet.md, mapped to the Character model
# attribute that stores it. Keys are the human-readable labels as they appear
# on the sheet; values must be real Character attributes (declared field or
# @computed_field). Multiple sheet fields may share one model attribute (e.g.
# Starting Skill and Secondary Skill both live in the `skills` dict) — that's
# not duplication, it's two views onto one piece of state.
CHARACTER_SHEET_FIELDS = {
    "Character Name": "name",
    "Player Name": "player_name",
    "Attributes": "attributes",
    "Primary Facet": "primary_facet",
    "Facet Level": "facet_level",
    "Advancement Track (marks toward next level)": "rank_advances_this_facet_level",
    "Title & Origin": "background_id",
    "Starting Skill (Practiced)": "skills",
    "Secondary Skill (Novice, 1 mark)": "skills",
    "Specialty": "specialty",
    "Skills": "skills",
    "Technique": "techniques",
    "Choice (if any)": "technique_choices",
    "Sparks": "sparks",
    "Skill Points Remaining This Session": "session_skill_points_remaining",
}


def test_character_sheet_fields_map_to_model() -> None:
    """INV-2: every Character Sheet field has a real home on the Character model.

    A sheet field with no model attribute behind it is a sheet that lets a
    player record something the engine cannot store — it lies about the game.
    Checks both directions: every mapped attribute must actually exist on
    `Character` (guards the sheet against the model drifting out from under
    it), and every field label must actually appear on the sheet (guards the
    mapping against going stale relative to the document).
    """
    known_attrs = set(Character.model_fields) | set(Character.model_computed_fields)
    sheet_text = _normalize(CHARACTER_SHEET.read_text())

    bad_attrs = [
        f"{label!r} -> {attr!r} (no such Character attribute)"
        for label, attr in CHARACTER_SHEET_FIELDS.items()
        if attr not in known_attrs
    ]
    missing_labels = [
        f"{label!r} not found on the sheet"
        for label in CHARACTER_SHEET_FIELDS
        if _normalize(label) not in sheet_text
    ]

    errors = bad_attrs + missing_labels
    assert not errors, "Character Sheet / model mismatches:\n" + "\n".join(errors)


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
_APPENDIX_DOMAIN = re.compile(r"^\*\*([A-Z][\w '&-]+?)\*\* \*\(([A-Za-z]+)\)\*\s*$", re.M)
DOMAIN_APPENDIX = PLAYER_HANDBOOK / "Appendix_Magic_Domains.md"


def _appendix_domains() -> dict[str, str]:
    """{domain id: type} as the appendix declares them, across both Facets."""
    domains: dict[str, str] = {}
    for name, dtype in _APPENDIX_DOMAIN.findall(DOMAIN_APPENDIX.read_text()):
        domain_id = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        domains[domain_id] = dtype.lower()
    return domains


def test_domain_catalog_matches_appendix() -> None:
    """INV-7: facet.yaml's domain catalog is the appendix, transcribed.

    The catalog now lives in two coupled homes — canon prose (the appendix) and
    data (facet.yaml) — and a domain whose *type* differs between them is a
    domain that rolls one difficulty at the table and another in the engine.
    That divergence is exactly what let prismatic domains be silently treated as
    standard ones (issue #8).
    """
    data = yaml.safe_load(FACET_YAML.read_text())["magic"]
    catalog = {
        d["id"]: d["type"]
        for d in data.get("soul_domains", []) + data.get("mind_domains", [])
    }
    appendix = _appendix_domains()

    errors: list[str] = []
    for domain_id, dtype in sorted(appendix.items()):
        if domain_id not in catalog:
            errors.append(f"{domain_id}: in the appendix, missing from facet.yaml")
        elif catalog[domain_id] != dtype:
            errors.append(
                f"{domain_id}: appendix says {dtype!r}, facet.yaml says {catalog[domain_id]!r}"
            )
    for domain_id in sorted(set(catalog) - set(appendix)):
        errors.append(f"{domain_id}: in facet.yaml, missing from the appendix")

    assert not errors, "Domain catalog / appendix mismatches:\n" + "\n".join(errors)


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
