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
  INV-8  the books may not restrict a Strike pairing the engine permits

Style-guide apparatus (docs/RESEARCH_style_audit.md, 2026-08):
  INV-9   every lookup table carries a numbered caption, unique and 1..n per chapter
  INV-10  List_of_Tables.md and List_of_Boxes.md regenerate to no diff
  INV-11  no "see below" / "as mentioned above" — pointers must resolve
  INV-12  no capitalized term the Glossary does not define
  INV-13  every box declares one of the six species, and Front Matter declares each
  INV-14  every Technique carries use/normal, and its header agrees with facet.yaml
  INV-15  the Bestiary's stat blocks, finding aids, and Lore boxes are complete
          and regenerate to no diff
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
BESTIARY = REPO_ROOT / "bestiary"
FACET_YAML = REPO_ROOT / "software" / "facets" / "base" / "facet.yaml"
SKILLS_CHAPTER = PLAYER_HANDBOOK / "II.6_Character_Creation_Skills.md"
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


def _facet_yaml_skills() -> list[dict]:
    data = yaml.safe_load(FACET_YAML.read_text())
    return data["skills"]


# A skill entry in II.6's "The Skill List": a bold name, an italic
# "(Facet — Attribute)" line, a **Roll:** field, then the prose paragraph that
# defines what the skill covers (audit finding P3 gave the entries a field
# skeleton; before that the prose followed the name directly).
_SKILL_ENTRY = re.compile(
    r"\*\*([A-Za-z]+)\*\* \*\([A-Za-z]+ — [A-Za-z]+\)\*\n\n"
    r"\*\*Roll:\*\*[^\n]*\n\n(.+?)(?=\n\n|\Z)", re.S
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
    "Rank Advances Toward Next Level": "rank_advances_this_facet_level",
    "Career Advances": "career_advances",
    "Title & Origin": "background_id",
    "Starting Skill (Practiced)": "skills",
    "Secondary Skill (Novice, 1 mark) or Domain Origin": "skills",
    "Specialty": "specialty",
    "Skills": "skills",
    "Technique": "techniques",
    "Choice (if any)": "technique_choices",
    "Magic Domain": "magic_domain",
    "Endurance (current / max) — max is 4 + Constitution modifier + Endurance skill rank": "endurance_current",
    "Armor Type": "armor",
    "Armor Downgrade Budget Remaining This Scene": "armor_downgrades_remaining",
    "Active Conditions": "conditions",
    "Sparks": "sparks",
    "Inventory": "inventory",
    "Item": "inventory",
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


# The Magic, Combat, and Inventory sections (new in this task), plus the
# Facet section's new Career Advances row.
NEW_CHARACTER_SHEET_SECTION_LABELS = [
    "Career Advances",
    "Magic Domain",
    "Endurance (current / max) — max is 4 + Constitution modifier + Endurance skill rank",
    "Armor Type",
    "Armor Downgrade Budget Remaining This Scene",
    "Active Conditions",
    "Inventory",
]


def test_new_character_sheet_sections_need_no_new_model_field() -> None:
    """D7 (W3-2/W3-3): the Magic, Combat, and Inventory sections are new
    *sheet* content, but every field they add was already tracked on
    `Character` before this task (DESIGN Section 1 S3) — no new Character
    field was added to support them.
    """
    known_attrs = set(Character.model_fields) | set(Character.model_computed_fields)
    for label in NEW_CHARACTER_SHEET_SECTION_LABELS:
        assert label in CHARACTER_SHEET_FIELDS, f"{label!r} not registered in CHARACTER_SHEET_FIELDS"
        assert CHARACTER_SHEET_FIELDS[label] in known_attrs, (
            f"{label!r} maps to {CHARACTER_SHEET_FIELDS[label]!r}, not a real Character attribute"
        )


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


def _find_technique(technique_id: str) -> dict:
    """Find a Technique's yaml block anywhere in facet.yaml's `techniques` tree."""
    data = yaml.safe_load(FACET_YAML.read_text())["techniques"]
    for tree in data.values():
        for branch in tree.get("branches", []):
            for tier in branch.get("tiers", []):
                for technique in tier.get("techniques", []):
                    if technique["id"] == technique_id:
                        return technique
    raise AssertionError(f"No technique {technique_id!r} found in facet.yaml")


def test_overwhelming_force_matches_phb_ii4a() -> None:
    """sync-H-1: Overwhelming Force is the current (once/scene, 10+) rule.

    facet.yaml still carried the pre-v0.3 "succeed by 3 or more above the
    threshold... staggered... act last... no reactions" version, which no
    longer matches PHB II.4a:39-40's rule at all.
    """
    description = _find_technique("overwhelming_force")["description"].lower()
    assert "once per scene" in description
    assert "10+" in description or "full success" in description


def test_no_pre_v03_overwhelming_force_text_survives() -> None:
    """The old threshold-margin wording must not survive anywhere in facet.yaml,
    not just in the Overwhelming Force entry itself."""
    assert "3 or more above the threshold" not in FACET_YAML.read_text()


def test_first_move_matches_phb_ii4b_timing_and_scope() -> None:
    """sync-M-1: First Move governs *this* exchange, not the next, and
    includes the ambush/trap-negation clause (PHB II.4b:96). facet.yaml had
    drifted to "acts first in the next exchange" with no mention of
    ambushes or traps.
    """
    description = _find_technique("first_move")["description"].lower()
    assert "this exchange" in description
    assert "next exchange" not in description
    assert "ambush" in description
    assert "trap" in description


# A pre-built Background entry in II.5: "**Name**\n\n*Title:* ...", up to the
# next thematic break. Distinguishes the 15 real entries from the five bold
# element-definition headers (**Title**, **Specialty**, etc.) earlier in the
# chapter, which are never followed by a "**Title:**" line.
#
# Field labels are bold, not italic: bold marks a field label, italics mark a
# named game object (style guide Law 5, audit finding S9). The instances used
# italic labels while the legend defining them used bold, which made the two
# typographic signals mean the same thing in one file.
_BACKGROUND_SECTION = re.compile(
    r"^\*\*([A-Z][^\n*]+)\*\*\n\n\*\*Title:\*\*.*?(?=\n---\n|\Z)", re.M | re.S
)
_SPECIALTY_LINE = re.compile(r"^\*\*Specialty:\*\*\s*(.+?)\.?\s*$", re.M)
BACKGROUNDS_CHAPTER = PLAYER_HANDBOOK / "II.5_Character_Creation_Backgrounds.md"


def _phb_background_specialties() -> dict[str, str | None]:
    """{Background name: Specialty text, or None if the entry has no Specialty line}."""
    text = BACKGROUNDS_CHAPTER.read_text()
    result: dict[str, str | None] = {}
    for m in _BACKGROUND_SECTION.finditer(text):
        name, block = m.group(1), m.group(0)
        spec = _SPECIALTY_LINE.search(block)
        result[name] = spec.group(1).strip() if spec else None
    return result


def _yaml_backgrounds() -> list[dict]:
    return yaml.safe_load(FACET_YAML.read_text())["backgrounds"]


def test_guild_apprentice_specialty_matches_quick_start() -> None:
    """rul-H1 / D4: the Quick Start text is the source of truth. II.5 had no
    Specialty at all for Guild Apprentice, and facet.yaml carried a third,
    different string ("Formal training in a structured discipline...") —
    both must now equal Quick Start's wording exactly, not merge with it.
    """
    quick_start_text = (
        "Artificers' Guild technical records — Standard becomes Easy when directly applicable"
    )
    phb_specialty = _phb_background_specialties()["Guild Apprentice"]
    assert phb_specialty == quick_start_text

    yaml_specialty = next(
        b["specialty"] for b in _yaml_backgrounds() if b["id"] == "guild_apprentice"
    )
    assert yaml_specialty.rstrip(".") == quick_start_text


def test_all_fifteen_backgrounds_have_a_specialty_in_phb_and_yaml() -> None:
    """II.5's five-elements claim (Title, Description, Starting Skill, Secondary
    Skill/Domain Origin, Specialty) must hold for every pre-built Background."""
    phb = _phb_background_specialties()
    assert len(phb) == 15
    missing_in_phb = [name for name, spec in phb.items() if not spec]
    assert not missing_in_phb, f"No Specialty in II.5 for: {missing_in_phb}"

    yaml_bgs = _yaml_backgrounds()
    assert len(yaml_bgs) == 15
    missing_in_yaml = [b["id"] for b in yaml_bgs if not b.get("specialty")]
    assert not missing_in_yaml, f"No specialty in facet.yaml for: {missing_in_yaml}"


# ---------------------------------------------------------------------------
# INV-8: the books may not restrict a Strike pairing the engine permits
# ---------------------------------------------------------------------------

#: A line that states the Strike roll and names both skills. Whatever it says
#: about Combat and Finesse has to be a default, not a restriction.
_STRIKE_SKILL_HEDGES = ("default", "whichever", "usually", "or finesse —",
                        "fits", "the fiction")


def _strike_skill_lines() -> list[tuple[Path, int, str]]:
    """Every book line that pairs a Strike with both Combat and Finesse."""
    found = []
    for path in _book_files():
        for number, line in _prose_lines(path):
            lowered = line.lower()
            if "combat" not in lowered or "finesse" not in lowered:
                continue
            if "strike" in lowered or "hit something" in lowered:
                found.append((path, number, line))
    return found


def test_books_do_not_restrict_the_strike_pairing() -> None:
    """INV-8. `_handle_strike` accepts any attribute/skill the client sends —
    `test_websocket.py::...Strike can use any attribute` pins that. III.3 said
    "the skill is **Combat** for melee and unarmed Strikes, **Finesse** for
    ranged ones", which reads as a restriction the engine does not enforce, and
    which makes a Finesse-based unarmed character unbuildable by the book.

    Found by an agentic playtest, 2026-07-31
    (playtest/08_npc_variance/subagent_session/report.md, F1) — a monk-adjacent
    PC struck with Dexterity + Finesse, the engine allowed it, and the book
    forbade it.

    Any line naming both skills for a Strike must hedge. Quick references are
    compressions, not paraphrases: if the body text hedges, they must too.
    """
    offenders = []
    for path, number, line in _strike_skill_lines():
        if not any(hedge in line.lower() for hedge in _STRIKE_SKILL_HEDGES):
            offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: {line.strip()}")

    assert not offenders, (
        "These lines state the Strike skill as a rule the engine does not "
        "enforce:\n" + "\n".join(offenders))


def test_the_strike_rule_is_stated_somewhere() -> None:
    """Guard against the previous test passing because the rule vanished."""
    assert _strike_skill_lines(), "No book line describes the Strike pairing at all"


def test_specialty_covers_the_no_skill_case() -> None:
    """II.5 defined a Specialty only as a difficulty shift, which says nothing
    about an action with no roll attached — the gap an MM had to rule on live
    (report F3). A Specialty must never manufacture a roll."""
    text = (PLAYER_HANDBOOK / "II.5_Character_Creation_Backgrounds.md").read_text(
        encoding="utf-8").lower()
    assert "when no skill fits" in text
    assert "do not invent a roll" in text


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
            for match in pattern.finditer(line):
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


# ---------------------------------------------------------------------------
# INV-14: every Technique entry has the fields its legend promises
# ---------------------------------------------------------------------------

FACET_CHAPTERS = {
    "body": PLAYER_HANDBOOK / "II.4a_Character_Creation_Facet_Body.md",
    "mind": PLAYER_HANDBOOK / "II.4b_Character_Creation_Facet_Mind.md",
    "soul": PLAYER_HANDBOOK / "II.4c_Character_Creation_Facet_Soul.md",
}

# "**Forcing Hand** *(Might, Tier 1 — Strength)*"
TECHNIQUE_HEAD = re.compile(
    r"^\*\*([A-Z][^*]+?)\*\* \*\(([A-Za-z ]+), Tier ([123]) — ([A-Za-z]+)\)\*$", re.M)


def _facet_yaml_techniques() -> dict[str, list[dict]]:
    """{facet: [technique, ...]} with branch and tier folded into each entry."""
    data = yaml.safe_load(FACET_YAML.read_text())
    out: dict[str, list[dict]] = {}
    for facet, tree in data["techniques"].items():
        entries = []
        for branch in tree["branches"]:
            for tier in branch["tiers"]:
                for technique in tier["techniques"]:
                    entries.append({**technique,
                                    "branch": branch["name"],
                                    "branch_attribute": branch["attribute"],
                                    "tier": tier["tier"]})
        out[facet] = entries
    return out


def test_every_technique_has_use_and_normal_in_facet_yaml() -> None:
    """INV-14: facet.yaml carries `use` and `normal` for every Technique.

    `normal` restates the baseline a Technique departs from — the field
    rulebooks.md §4 calls "a masterstroke worth stealing", because without it a
    reader cannot tell how big the exception is. Audit findings P1 and P2.
    """
    missing = []
    for facet, techniques in _facet_yaml_techniques().items():
        for technique in techniques:
            for field in ("use", "normal"):
                if not technique.get(field):
                    missing.append(f"{facet}/{technique['id']}: no `{field}`")

    assert not missing, "Techniques missing their fields:\n" + "\n".join(missing)


def test_every_technique_entry_states_branch_tier_and_attribute() -> None:
    """INV-14: no Technique entry in II.4a-c omits its header fields.

    The audit found the first catalog a reader meets drifting inside one file:
    Tier 1 entries carried an attribute tag and Tier 2/3 did not. Format drift
    mid-catalog is the "no mid-catalog format drift" anti-pattern.
    """
    yaml_names = {t["name"] for ts in _facet_yaml_techniques().values() for t in ts}
    offenders = []
    for facet, path in FACET_CHAPTERS.items():
        text = path.read_text(encoding="utf-8")
        headed = {m.group(1) for m in TECHNIQUE_HEAD.finditer(text)}
        for name in sorted(yaml_names):
            # Only require a header for Techniques this chapter actually lists.
            if re.search(rf"^\*\*{re.escape(name)}\*\*", text, re.M) and name not in headed:
                offenders.append(f"{path.name}: '{name}' has no "
                                 f"*(Branch, Tier N — Attribute)* header")

    assert not offenders, "Technique headers are incomplete:\n" + "\n".join(offenders)


def test_technique_headers_match_facet_yaml() -> None:
    """INV-14: a Technique's branch, tier, and attribute agree with facet.yaml.

    Two Techniques share a name across Facets (Second Domain, Ascendant Domain).
    Anything that keys Technique data by name alone silently gives the Mind
    entries the Soul entries' branch and roll — which is exactly what happened
    while this format was being applied.
    """
    attribute_names = {
        "strength": "Strength", "dexterity": "Dexterity",
        "constitution": "Constitution", "intelligence": "Intelligence",
        "wisdom": "Wisdom", "knowledge": "Knowledge", "spirit": "Spirit",
        "luck": "Luck", "charisma": "Charisma",
    }
    mismatches = []
    for facet, path in FACET_CHAPTERS.items():
        expected = {t["name"]: t for t in _facet_yaml_techniques()[facet]}
        for match in TECHNIQUE_HEAD.finditer(path.read_text(encoding="utf-8")):
            name, branch, tier, attribute = match.groups()
            technique = expected.get(name)
            if technique is None:
                mismatches.append(f"{path.name}: '{name}' is not in facet.yaml's "
                                  f"{facet} tree")
                continue
            actual = (branch, int(tier), attribute)
            wanted = (technique["branch"], technique["tier"],
                      attribute_names[technique["branch_attribute"]])
            if actual != wanted:
                mismatches.append(f"{path.name}: '{name}' says {actual}, "
                                  f"facet.yaml says {wanted}")

    assert not mismatches, "Technique headers disagree with facet.yaml:\n" + "\n".join(mismatches)


def test_every_technique_entry_carries_a_normal_line() -> None:
    """INV-14: each Technique entry in the books prints its Normal field."""
    missing = []
    for facet, path in FACET_CHAPTERS.items():
        text = path.read_text(encoding="utf-8")
        blocks = TECHNIQUE_HEAD.split(text)
        # split() yields [prefix, name, branch, tier, attr, body, name, ...]
        for i in range(1, len(blocks), 5):
            name, body = blocks[i], blocks[i + 4]
            if "**Normal:**" not in body:
                missing.append(f"{path.name}: '{name}' has no **Normal:** line")

    assert not missing, "Techniques without a Normal line:\n" + "\n".join(missing)


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
    """INV-15: no creature has an entry the TR-sorted list does not carry.

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
# B4 Q2 (docs/DECISIONS.md) — the Second Domain wording defect (TD-2)
# ---------------------------------------------------------------------------

def test_second_domain_wording_does_not_anchor_on_primary_domain() -> None:
    """B4 Q2 regression guard: no book or facet.yaml surface says a Second
    Domain is "harder than your primary domain".

    That anchoring is wrong for a Focused-primary caster: Focused-plus-one-step
    *is* the Standard table, so the phrase silently deletes the penalty. The
    correct, re-anchored wording is "harder than normal for that domain" —
    the ruling prices the *grant*, not the caster's other domain. The string
    is short and copy-pastable, hence the standing regression guard rather
    than a one-time fix.
    """
    offenders = []
    for path in _book_files():
        if "harder than your primary domain" in path.read_text():
            offenders.append(str(path.relative_to(REPO_ROOT)))
    if "harder than your primary domain" in FACET_YAML.read_text():
        offenders.append(str(FACET_YAML.relative_to(REPO_ROOT)))
    assert not offenders, (
        f"stale 'harder than your primary domain' wording in: {offenders}"
    )
