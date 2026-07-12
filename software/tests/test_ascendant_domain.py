"""Ascendant Domain — the Tier 3 Technique that grants a prismatic domain.

Issue #8 / docs/DESIGN_ascendant_domain.md. PR #7 added the Technique to the PHB
and facet.yaml; the engine honored none of its three clauses (II.4b / II.4c):

  1. "Your original domain is unchanged."
  2. "The Broad difficulty table applies — Hard at Minor scope, Very Hard at
     Significant and Major."
  3. "Its Major-scope ceiling cannot be moved by Sparks."

These tests pin all three, plus the catalog they all depend on and the isolation
of Second Domain's penalty from the Ascendant route.
"""
from __future__ import annotations

import pytest

from app.game.character import create_default_character
from app.game.engine import resolve_magic_roll


ZAHNA_ATTRS = {
    "strength": 1, "dexterity": 3, "constitution": 1, "intelligence": 3,
    "wisdom": 1, "knowledge": 3, "spirit": 2, "luck": 3, "charisma": 1,
}


def _mind_mage(ruleset):
    """A Mind character with Inscription, standing at the Archive Tier 3 gate."""
    char, errors = create_default_character(
        name="Zahna", player_name="P", primary_facet="mind",
        attributes=dict(ZAHNA_ATTRS), ruleset=ruleset,
        background_id="guild_apprentice", magic_domain="inscription",
    )
    assert not errors, errors
    for tech, choice in [("arcane_study", "inscription"), ("cross_reference", None)]:
        char.technique_picks_available += 1
        ok, msg = char.select_technique(tech, ruleset=ruleset, choice=choice)
        assert ok, msg
    char.technique_picks_available += 1
    return char


# ---------------------------------------------------------------------------
# The catalog (D-A1) — everything below depends on domains resolving to a type
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "domain_id,expected_type",
    [
        ("fire", "focused"),
        ("shadow", "focused"),
        ("storm", "standard"),
        ("the_tide", "standard"),
        ("inscription", "focused"),
        ("constructed_force", "focused"),
        ("illusion", "standard"),
        ("the_undying", "broad"),
        ("fate", "broad"),
        ("the_living_world", "broad"),
        ("the_arcane", "broad"),
        ("the_constructed_mind", "broad"),
        ("chronomancy", "broad"),
    ],
)
def test_domain_catalog_resolves_with_canonical_type(ruleset, domain_id, expected_type):
    """Every domain resolves from facet.yaml with the type the appendix gives it.

    Before this, get_domain() returned None for every domain and the engine
    silently substituted a synthetic type="standard" — which is why a prismatic
    domain rolled the Standard table.
    """
    domain = ruleset.magic.get_domain(domain_id)
    assert domain is not None, f"{domain_id!r} is not registered in facet.yaml"
    assert domain.type == expected_type


def test_prismatic_domains_require_tier3(ruleset):
    """Prismatic (broad) domains are gated behind a Tier 3 Technique; others aren't."""
    for domain in ruleset.magic.all_domains:
        assert domain.requires_tier3 == (domain.type == "broad"), (
            f"{domain.id}: requires_tier3={domain.requires_tier3} but type={domain.type}"
        )


def test_domain_tradition_follows_facet(ruleset):
    """Soul domains roll Spirit (intuitive), Mind domains roll Knowledge (scholarly)."""
    assert {d.tradition for d in ruleset.magic.soul_domains} == {"intuitive"}
    assert {d.tradition for d in ruleset.magic.mind_domains} == {"scholarly"}


# ---------------------------------------------------------------------------
# Clause 1 — "Your original domain is unchanged" (D-A2, D-A3)
# ---------------------------------------------------------------------------

def test_ascendant_domain_preserves_original_domain(ruleset):
    """Taking Ascendant Domain must not overwrite the character's primary domain.

    Regression on the destructive bug: selecting it set magic_domain = choice,
    silently erasing Inscription from Zahna's sheet and her .fof export.
    """
    char = _mind_mage(ruleset)
    ok, msg = char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )
    assert ok, msg
    assert char.magic_domain == "inscription"
    assert char.ascendant_domain == "chronomancy"


def test_ascendant_domain_rejects_non_prismatic_choice(ruleset):
    """"Choose one prismatic domain" — a standard domain is not a legal pick (D-A5)."""
    char = _mind_mage(ruleset)
    ok, msg = char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="illusion"
    )
    assert not ok
    assert "prismatic" in msg.lower()
    assert char.ascendant_domain is None
    assert char.magic_domain == "inscription"


def test_ascendant_domain_rejects_other_facets_prismatic(ruleset):
    """A Mind mage cannot ascend into a Soul prismatic domain (D-A5)."""
    char = _mind_mage(ruleset)
    ok, msg = char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="fate"
    )
    assert not ok
    assert char.ascendant_domain is None


def test_ascendant_domain_survives_fof_round_trip(ruleset):
    """The prismatic domain persists — a sheet that forgets it lies about the game."""
    char = _mind_mage(ruleset)
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]

    from app.game.character import Character
    restored = Character.from_fof(char.to_fof(module_refs=[], session_id="s1"))
    assert restored.magic_domain == "inscription"
    assert restored.ascendant_domain == "chronomancy"


# ---------------------------------------------------------------------------
# Clauses 2 and 3 — the Broad table and the Spark ceiling (D-A4)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "scope,expected",
    [("minor", "Hard"), ("significant", "Very Hard"), ("major", "Very Hard")],
)
def test_broad_domain_uses_broad_difficulty_table(ruleset, scope, expected):
    """Clause 2: Hard at Minor, Very Hard at Significant and Major.

    Minor scope is the load-bearing case — the engine used to flatten every
    Broad cast to Very Hard with a stray assignment that called itself a ceiling.
    """
    char = _mind_mage(ruleset)
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]

    result = resolve_magic_roll(
        character=char, domain_id="chronomancy", scope=scope,
        intent="bend a moment", ruleset=ruleset,
    )
    assert result.request.difficulty_label == expected


def test_sparks_cannot_push_scope_on_a_prismatic_domain(ruleset):
    """Clause 3: the ceiling cannot be moved by Sparks."""
    char = _mind_mage(ruleset)
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]

    with pytest.raises(ValueError, match="cannot be pushed"):
        resolve_magic_roll(
            character=char, domain_id="chronomancy", scope="major",
            intent="unmake an hour", ruleset=ruleset, spark_use="push_scope",
        )


def test_ascendant_domain_takes_no_second_domain_penalty(ruleset):
    """The Broad table is Ascendant's cost — it does not also take Second Domain's
    one-step-harder penalty. Penalty isolation is why ascendant_domain is its own
    field rather than a reuse of secondary_magic_domain (D-A2).
    """
    char = _mind_mage(ruleset)
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]

    result = resolve_magic_roll(
        character=char, domain_id="chronomancy", scope="minor",
        intent="read a moment", ruleset=ruleset,
    )
    # Broad/minor is Hard. A leaked +1 step would show up as Very Hard.
    assert result.request.difficulty_label == "Hard"


# ---------------------------------------------------------------------------
# Second Domain — the other Tier 3 route (D-A5, D-A6)
# ---------------------------------------------------------------------------

def _soul_mage(ruleset):
    """A Soul character with Fire, standing at the Communion Tier 3 gate."""
    char, errors = create_default_character(
        name="Vesh", player_name="P", primary_facet="soul",
        attributes=dict(ZAHNA_ATTRS), ruleset=ruleset,
        background_id="temple_acolyte", magic_domain="fire",
    )
    assert not errors, errors
    for tech, choice in [("spiritual_domain", "fire"),
                         ("the_language_beneath_language", None)]:
        char.technique_picks_available += 1
        ok, msg = char.select_technique(tech, ruleset=ruleset, choice=choice)
        assert ok, msg
    char.technique_picks_available += 1
    return char


def test_second_domain_populates_secondary_field(ruleset):
    """Second Domain's choice must actually reach `secondary_magic_domain`.

    Nothing outside .fof loading ever wrote that field, so the one-step-harder
    penalty it gates could only fire for a hand-authored character (D-A6).
    """
    char = _soul_mage(ruleset)
    ok, msg = char.select_technique("second_domain", ruleset=ruleset, choice="storm")
    assert ok, msg
    assert char.magic_domain == "fire"           # original survives
    assert char.secondary_magic_domain == "storm"
    assert char.ascendant_domain is None         # different route, different slot


def test_second_domain_rejects_prismatic_choice(ruleset):
    """"Prismatic territories require Ascendant Domain" (II.4c) — enforced (D-A5)."""
    char = _soul_mage(ruleset)
    ok, msg = char.select_technique("second_domain", ruleset=ruleset, choice="fate")
    assert not ok
    assert "ascendant" in msg.lower()
    assert char.secondary_magic_domain is None


def test_second_domain_is_one_step_harder(ruleset):
    """The penalty that distinguishes Second Domain from Ascendant Domain.

    Storm is Standard (minor = Standard); as a *second* domain it lands Hard.
    """
    char = _soul_mage(ruleset)
    assert char.select_technique("second_domain", ruleset=ruleset, choice="storm")[0]

    result = resolve_magic_roll(
        character=char, domain_id="storm", scope="minor",
        intent="still the wind", ruleset=ruleset,
    )
    assert result.request.difficulty_label == "Hard"

    # ...while the original domain is untaxed: Fire is Focused, minor = Easy.
    original = resolve_magic_roll(
        character=char, domain_id="fire", scope="minor",
        intent="light a candle", ruleset=ruleset,
    )
    assert original.request.difficulty_label == "Easy"


def test_rejected_domain_choice_does_not_burn_a_technique_pick(ruleset):
    """An illegal pick is refused without costing the player their Tier 3 slot."""
    char = _mind_mage(ruleset)
    picks_before = char.technique_picks_available

    ok, _ = char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="illusion"
    )
    assert not ok
    assert char.technique_picks_available == picks_before
    assert "ascendant_domain_mind" not in char.techniques

    # The slot is still there, and a legal pick still works.
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]


def test_primary_domain_unaffected_by_ascension(ruleset):
    """Inscription is Focused — it still rolls Focused difficulties afterwards."""
    char = _mind_mage(ruleset)
    assert char.select_technique(
        "ascendant_domain_mind", ruleset=ruleset, choice="chronomancy"
    )[0]

    result = resolve_magic_roll(
        character=char, domain_id="inscription", scope="minor",
        intent="copy a page", ruleset=ruleset,
    )
    assert result.request.difficulty_label == "Easy"  # focused/minor
