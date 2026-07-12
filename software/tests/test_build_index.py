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
    parse_glossary_pointers,
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


def test_find_term_sections_prefers_headings_over_passing_mentions(tmp_path: Path) -> None:
    """A heading naming the term wins outright; a bare prose mention elsewhere is
    not an index entry.

    The old rule indexed any mention, which made "Tier" resolve to 72 sections —
    a concordance, not an index. `## Reactions` merely *says* "Armor"; it isn't
    about it, and sending a reader there is a false promise.
    """
    doc = _write(
        tmp_path,
        "III.3_Combat.md",
        "## Armor\n\nArmor softens incoming Conditions.\n\n"
        "## Reactions\n\nDodge, Parry, and Absorb all cost Endurance; "
        "Armor doesn't apply here.\n",
    )
    assert find_term_sections("Armor", doc) == [("Armor", "armor")]


def test_find_term_sections_falls_back_to_bold_when_no_heading_names_it(
    tmp_path: Path,
) -> None:
    """Terms named in no heading anywhere (Resolve, Mook) still need entries. The
    books bold a term where they state its rule, so bold is the fallback rank."""
    doc = _write(
        tmp_path,
        "MM1_Encounters.md",
        "## Stat Blocks\n\nEvery enemy has **Resolve**, depleted by Strikes.\n\n"
        "## Budgets\n\nA fight's Resolve total is a rough ordering check.\n",
    )
    # Only the section that *states the rule* (bold) is indexed, not the aside.
    assert find_term_sections("Resolve", doc) == [("Stat Blocks", "stat-blocks")]


def test_find_term_sections_ignores_prose_only_mentions(tmp_path: Path) -> None:
    """Neither in a heading nor bolded anywhere — the term is only mentioned, so
    the file contributes no entries at all."""
    doc = _write(
        tmp_path,
        "III.3_Combat.md",
        "## Reactions\n\nDodge and Parry both cost Endurance, unlike Armor.\n",
    )
    assert find_term_sections("Armor", doc) == []


def test_find_term_sections_respects_word_boundaries(tmp_path: Path) -> None:
    """"Facet" must not match inside "Facets" — the plural is a different word."""
    doc = _write(tmp_path, "II.4_Facets.md", "## Facets and Advancement\n\nProse.\n")
    assert find_term_sections("Facet", doc) == []


def test_build_index_walks_multiple_files_in_order(tmp_path: Path) -> None:
    phb = tmp_path / "player_handbook"
    phb.mkdir()
    first = _write(phb, "II.4_Facets.md", "## Facet Levels\n\nA Facet levels up.\n")
    second = _write(phb, "III.3_Combat.md", "## Armor\n\nYour **Facet** matters here.\n")

    index = build_index(terms=["Facet"], files=[first, second])

    assert index["Facet"] == [
        (first, "Facet Levels", "facet-levels"),      # heading rank
        (second, "Armor", "armor"),                   # bold rank, no heading in that file
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


def test_parse_glossary_pointers_reads_the_defining_chapter(tmp_path: Path) -> None:
    """PHB entries cite "Chapter X.Y"; MM entries cite a bare "MM1"."""
    glossary = _write(
        tmp_path,
        "Glossary.md",
        "**Armor** — definition. *(Chapter III.3)*\n\n"
        "**Resolve** — definition. *(MM1)*\n"
        "**Posture (Aggressive/Defensive)** — definition. *(Chapter III.3)*\n",
    )
    assert parse_glossary_pointers(glossary) == {
        "Armor": "III.3",
        "Resolve": "MM1",
        "Posture": "III.3",
    }


def test_render_index_links_the_defining_chapter() -> None:
    """Every term gets a definitional anchor, even one no heading names."""
    text = render_index({"Resolve": []}, pointers={"Resolve": "MM1"})
    assert "*Defined in [MM1](../mm_manual/MM1_Encounters_and_Enemies.md).*" in text


def test_render_index_omits_pointer_for_unknown_chapter() -> None:
    """A pointer at a chapter that doesn't exist is dropped, not rendered broken.
    (INV-3 already fails the build in that case — this just keeps output sane.)"""
    text = render_index({"Ghost": []}, pointers={"Ghost": "XI.9"})
    assert "Defined in" not in text
