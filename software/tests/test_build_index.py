"""Tests for software/tools/build_index.py — the generated PHB/MM term index.

See docs/DESIGN_production_apparatus.md §4.9 and TASKS PA-10. INV-4 itself
(regenerating Index.md produces no diff) lives in test_docs_consistency.py,
since it's a book-level invariant rather than a unit test of this module.
"""
from __future__ import annotations

from pathlib import Path

from tools.build_index import (
    build_index,
    find_term_sections,
    parse_glossary_terms,
    render_index,
)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text)
    return path


def test_parse_glossary_terms_strips_parenthetical_variants(tmp_path: Path) -> None:
    """A glossary entry's indexed term is the base word before any `(...)`."""
    glossary = _write(
        tmp_path,
        "Glossary.md",
        "**Armor** — definition. *(Chapter III.3)*\n\n"
        "**Condition (Tier 1/2/3)** — definition. *(Chapter III.3)*\n",
    )
    assert parse_glossary_terms(glossary) == ["Armor", "Condition"]


def test_find_term_sections_absent_term_returns_empty(tmp_path: Path) -> None:
    """A term that never appears in a file yields zero sections, not a crash."""
    doc = _write(tmp_path, "III.3_Combat.md", "## Armor\n\nSome prose about defense.\n")
    assert find_term_sections("Spark", doc) == []


def test_find_term_sections_matches_heading_and_body_separately(tmp_path: Path) -> None:
    """A term can appear in a heading's title and, independently, in another
    section's body text — both must be reported, as distinct headings."""
    doc = _write(
        tmp_path,
        "III.3_Combat.md",
        "## Armor\n\nArmor softens incoming Conditions.\n\n"
        "## Reactions\n\nDodge, Parry, and Absorb all cost Endurance; "
        "Armor doesn't apply here.\n",
    )
    sections = find_term_sections("Armor", doc)
    assert sections == [
        ("Armor", "armor"),
        ("Reactions", "reactions"),
    ]


def test_find_term_sections_respects_word_boundaries(tmp_path: Path) -> None:
    """"Facet" must not match inside "Facets" — the plural is a different word."""
    doc = _write(tmp_path, "II.4_Facets.md", "## Facets and Advancement\n\nProse.\n")
    assert find_term_sections("Facet", doc) == []


def test_build_index_walks_multiple_files_in_order(tmp_path: Path) -> None:
    phb = tmp_path / "player_handbook"
    phb.mkdir()
    first = _write(phb, "II.4_Facets.md", "## Advancement\n\nA Facet levels up.\n")
    second = _write(phb, "III.3_Combat.md", "## Armor\n\nFacet durability note.\n")

    index = build_index(terms=["Facet"], files=[first, second])

    assert index["Facet"] == [
        (first, "Advancement", "advancement"),
        (second, "Armor", "armor"),
    ]


def test_render_index_reports_terms_with_no_sections() -> None:
    """A term with zero occurrences is still listed, flagged rather than hidden."""
    text = render_index({"Ghost Term": []})
    assert "## Ghost Term" in text
    assert "_No sections found._" in text


def test_render_index_sorts_terms_case_insensitively() -> None:
    index = {"skill": [], "Armor": [], "technique": []}
    text = render_index(index)
    assert text.index("## Armor") < text.index("## skill") < text.index("## technique")
