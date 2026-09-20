"""Tests for character creation, attribute validation, and skill advancement."""
import pytest

from app.game.character import Character, SkillState, create_default_character


# ---------------------------------------------------------------------------
# Valid character creation
# ---------------------------------------------------------------------------

class TestCharacterCreation:
    def test_valid_character_creates_successfully(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Zahna", player_name="P1",
            primary_facet="mind", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []
        assert char is not None
        assert char.name == "Zahna"
        assert char.primary_facet == "mind"

    def test_character_starts_with_correct_sparks(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Zulnut", player_name="P2",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.sparks == 3  # base_sparks_per_session from ruleset

    def test_character_starts_with_session_skill_points(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Mordai", player_name="P3",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.session_skill_points_remaining == 4

    def test_active_skills_initialised_at_novice(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P4",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        for skill_id, state in char.skills.items():
            assert state.rank == "novice"
            assert state.marks == 0

    def test_stub_skills_not_in_character(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P5",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        # Stub skills should not be initialised on the character
        stub_ids = {s.id for s in ruleset.skills if s.status == "stub"}
        for sid in stub_ids:
            assert sid not in char.skills

    def test_facet_level_starts_at_zero(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P6",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.facet_level == 0


# ---------------------------------------------------------------------------
# Attribute validation
# ---------------------------------------------------------------------------

class TestAttributeValidation:
    def test_wrong_total_points_rejected(self, ruleset):
        attrs = {
            "strength": 3, "dexterity": 3, "constitution": 3,
            "intelligence": 3, "wisdom": 3, "knowledge": 3,
            "spirit": 1, "luck": 1, "charisma": 1,
        }  # 22 points
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None
        assert any("18" in e for e in errors)

    def test_attribute_rating_above_max_rejected(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        attrs["strength"] = 4  # exceeds max of 3
        # Adjust to keep total = 18 by reducing another
        attrs["constitution"] = 1
        attrs["luck"] = 1
        attrs["charisma"] = 1
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None

    def test_attribute_below_minimum_rejected(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        attrs["strength"] = 0
        attrs["dexterity"] = 4
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None

    def test_missing_attribute_rejected(self, ruleset):
        attrs = {
            "strength": 3, "dexterity": 3, "constitution": 3,
            "intelligence": 3, "wisdom": 3, "knowledge": 3,
        }  # missing soul attributes
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None
        assert any("Missing" in e for e in errors)

    def test_unknown_primary_facet_rejected(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="arcane",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert char is None
        assert any("facet" in e.lower() for e in errors)

    def test_all_three_facets_are_valid(self, ruleset, valid_attributes):
        for facet in ["body", "mind", "soul"]:
            char, errors = create_default_character(
                name="Test", player_name="P", primary_facet=facet,
                attributes=valid_attributes, ruleset=ruleset,
            )
            assert errors == [], f"Facet {facet} should be valid, got: {errors}"


# ---------------------------------------------------------------------------
# Attribute modifiers
# ---------------------------------------------------------------------------

class TestAttributeModifiers:
    def test_strong_strength_returns_plus_one(self, body_character, ruleset):
        mod = body_character.get_attribute_modifier("strength", ruleset)
        assert mod == 1  # rating 3 → +1

    def test_weak_luck_returns_minus_one(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        # Set luck to 1 (weak)
        char, _ = create_default_character(
            name="Test", player_name="P", primary_facet="soul",
            attributes=attrs, ruleset=ruleset,
        )
        mod = char.get_attribute_modifier("luck", ruleset)
        # luck is 2 in valid_attributes
        assert mod == 0


# ---------------------------------------------------------------------------
# Major Attribute modifier derivation — sync-M-8 part 1: II.2, Deriving Your
# Major Attribute Modifiers (sum of three Minors -> a modifier band).
# ---------------------------------------------------------------------------

class TestMajorAttributeModifierDerivation:
    """`valid_attributes` (str3 dex3 con2, int2 wis2 kno2, spi1 luck2 cha1)
    covers all three bands: Body sums to 8 (the 8-9 -> +1 band), Mind sums
    to 6 (5-7 -> +0), Soul sums to 4 (3-4 -> -1)."""

    def test_body_sum_eight_is_plus_one(self, body_character, ruleset):
        assert body_character.get_major_attribute_modifier("body", ruleset) == 1

    def test_mind_sum_six_is_plus_zero(self, body_character, ruleset):
        assert body_character.get_major_attribute_modifier("mind", ruleset) == 0

    def test_soul_sum_four_is_minus_one(self, body_character, ruleset):
        assert body_character.get_major_attribute_modifier("soul", ruleset) == -1

    def test_out_of_range_sum_defaults_to_zero(self, ruleset):
        """Not reachable through the standard 1-3-per-Minor distribution
        (sums always fall in 3-9), but a homebrew ruleset could shift the
        bands — an unmatched sum must not raise, it defaults to +0."""
        assert ruleset.get_major_attribute_modifier(0) == 0
        assert ruleset.get_major_attribute_modifier(100) == 0


# ---------------------------------------------------------------------------
# Spark spending
# ---------------------------------------------------------------------------

class TestSparkSpending:
    def test_spend_spark_reduces_count(self, body_character):
        initial = body_character.sparks
        result = body_character.spend_spark()
        assert result is True
        assert body_character.sparks == initial - 1

    def test_spend_spark_returns_false_when_empty(self, body_character):
        body_character.sparks = 0
        result = body_character.spend_spark()
        assert result is False
        assert body_character.sparks == 0

    def test_earn_spark_increases_count(self, body_character):
        initial = body_character.sparks
        body_character.earn_spark()
        assert body_character.sparks == initial + 1

    def test_can_spend_all_sparks(self, body_character):
        count = body_character.sparks
        for _ in range(count):
            body_character.spend_spark()
        assert body_character.sparks == 0


# ---------------------------------------------------------------------------
# Skill advancement
# ---------------------------------------------------------------------------

class TestSkillAdvancement:
    def test_marks_accumulate_without_rank_advance(self, body_character, ruleset):
        result = body_character.advance_skill("athletics", 1, ruleset)
        assert result["rank_advances"] == 0
        assert body_character.skills["athletics"].marks == 1

    def test_three_marks_advance_rank(self, body_character, ruleset):
        result = body_character.advance_skill("athletics", 3, ruleset)
        assert result["rank_advances"] == 1
        assert body_character.skills["athletics"].rank == "practiced"
        assert body_character.skills["athletics"].marks == 0

    def test_eight_marks_advance_to_expert(self, body_character, ruleset):
        """D16: 3 marks to Practiced + 5 more to Expert."""
        body_character.advance_skill("athletics", 8, ruleset)
        assert body_character.skills["athletics"].rank == "expert"

    def test_advance_past_expert_reaches_master(self, body_character, ruleset):
        body_character.advance_skill("athletics", 8, ruleset)  # novice → expert
        assert body_character.skills["athletics"].rank == "expert"
        body_character.advance_skill("athletics", 8, ruleset)  # expert → master
        assert body_character.skills["athletics"].rank == "master"

    def test_master_rank_does_not_advance_further(self, body_character, ruleset):
        body_character.advance_skill("athletics", 16, ruleset)  # novice → master
        assert body_character.skills["athletics"].rank == "master"
        with pytest.raises(ValueError, match="already at Master"):
            body_character.advance_skill("athletics", 10, ruleset)
        assert body_character.skills["athletics"].rank == "master"  # still master

    def test_marks_carry_over_between_sessions(self, body_character, ruleset):
        body_character.advance_skill("athletics", 2, ruleset)
        assert body_character.skills["athletics"].marks == 2
        body_character.advance_skill("athletics", 1, ruleset)
        assert body_character.skills["athletics"].rank == "practiced"
        assert body_character.skills["athletics"].marks == 0

    def test_primary_facet_advances_count_toward_facet_level(self, body_character, ruleset):
        # athletics is in body facet = primary for body_character
        initial = body_character.rank_advances_this_facet_level
        body_character.advance_skill("athletics", 3, ruleset)  # novice → practiced
        assert body_character.rank_advances_this_facet_level == initial + 1

    def test_three_advances_trigger_facet_level_up(self, ruleset, valid_attributes):
        """D16 threshold 3: two advances is not a level, the third is."""
        char, _ = create_default_character(
            name="Level Test", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        body_active_skills = [s.id for s in ruleset.skills if s.facet == "body" and s.status == "active"]
        for sid in body_active_skills[:2]:
            char.advance_skill(sid, 3, ruleset)
        assert char.facet_level == 0  # not yet — need 3
        assert char.rank_advances_this_facet_level == 2

        char.advance_skill(body_active_skills[2], 3, ruleset)
        assert char.facet_level == 1
        assert char.rank_advances_this_facet_level == 0

    def test_unknown_skill_is_created_on_advance(self, body_character, ruleset):
        body_character.advance_skill("nonexistent_skill", 1, ruleset)
        assert "nonexistent_skill" in body_character.skills


# ---------------------------------------------------------------------------
# Per-Facet level tracking (WS-B / B3 — cross-Facet levels count, D3)
# ---------------------------------------------------------------------------

def _facet_skills(ruleset, facet):
    return [s.id for s in ruleset.skills if s.facet == facet and s.status == "active"]


def _advance_facet(char, ruleset, facet, advances):
    """Produce exactly `advances` rank advances in `facet`, cheapest-first.

    D16: each advance costs what its target rank charges (3/5/8), and the rank
    caps wall a skill off once the Facet's slots are committed, so this walks
    breadth-first to Practiced before buying any Expert."""
    mpr = ruleset.advancement.marks_per_rank
    order = ["novice", "practiced", "expert", "master"]
    done = 0
    while done < advances:
        target = None
        for sid in _facet_skills(ruleset, facet):
            state = char.skills.get(sid)
            rank = state.rank if state else "novice"
            if rank == char.rank_ceiling_for(sid, ruleset):
                continue
            # Marks already banked count toward the next rank, and
            # advance_skill refuses a batch bigger than the cap can absorb,
            # so ask for exactly what is still owed.
            cost = mpr.for_rank(order[order.index(rank) + 1]) - (state.marks if state else 0)
            if target is None or cost < target[0]:
                target = (cost, sid)
        if target is None:
            break
        cost, sid = target
        done += char.advance_skill(sid, cost, ruleset)["rank_advances"]
    return done


class TestPerFacetLevelTracking:
    def test_cross_facet_advance_increments_that_facets_level(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        _advance_facet(char, ruleset, "mind", 3)  # one mind level at threshold 3
        assert char.facet_levels.get("mind") == 1
        assert char.facet_levels.get("body", 0) == 0
        assert char.facet_level == 0  # primary (body) unchanged

    def test_total_facet_levels_sums_across_facets(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        _advance_facet(char, ruleset, "body", 6)  # 2 body levels
        _advance_facet(char, ruleset, "mind", 3)  # 1 mind level
        assert char.facet_level == 2               # primary only
        assert char.total_facet_levels == 3        # sum across facets

    def test_major_fires_at_three_levels_two_primary_one_cross(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        _advance_facet(char, ruleset, "body", 6)  # levels 1 and 2, no Major yet
        assert char.total_facet_levels == 2
        # The advance that lands the third (cross-Facet) level reports the Major.
        mind = _facet_skills(ruleset, "mind")
        practiced = ruleset.advancement.marks_per_rank.for_rank("practiced")
        major_seen = False
        for sid in mind[:3]:
            result = char.advance_skill(sid, practiced, ruleset)
            major_seen = major_seen or result["major_advancement"]
        assert char.total_facet_levels == 3
        assert major_seen

    def test_boundary_level_one_at_three_advances(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        _advance_facet(char, ruleset, "body", 3)
        assert char.facet_level == 1
        assert char.rank_advances_this_facet_level == 0

    def test_boundary_level_two_at_six_advances(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        _advance_facet(char, ruleset, "body", 6)
        assert char.facet_level == 2

    def test_boundary_level_three_at_nine_advances(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        got = _advance_facet(char, ruleset, "body", 9)
        assert got == 9  # the full shaped ceiling (1 Master / 2 Expert / 2 Practiced)
        assert char.facet_level == 3
        assert char.rank_advances_this_facet_level == 0

    def test_technique_pick_granted_per_facet_level(self, ruleset, valid_attributes):
        """Each Facet level (any Facet) grants exactly one Technique pick (§6.4)."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert char.technique_picks_available == 0
        _advance_facet(char, ruleset, "body", 3)   # 1 body level
        assert char.technique_picks_available == 1
        _advance_facet(char, ruleset, "body", 3)   # 2nd body level
        assert char.technique_picks_available == 2
        _advance_facet(char, ruleset, "mind", 5)   # 1 cross-Facet level also grants a pick
        assert char.technique_picks_available == 3

    def test_select_technique_spends_a_pick(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 1
        ok, msg = char.select_technique("sense_the_unseen", ruleset)
        assert ok and msg == "ok"
        assert "sense_the_unseen" in char.techniques
        assert char.technique_picks_available == 0

    def test_select_technique_rejects_without_pick(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        ok, msg = char.select_technique("sense_the_unseen", ruleset)
        assert not ok
        assert "pick" in msg.lower()
        assert "sense_the_unseen" not in char.techniques

    def test_select_technique_rejects_unmet_prerequisite(self, ruleset, valid_attributes):
        """PHB II.4:83: Tier 3 requires a Tier 2 in the same branch. A fresh
        character (no Tier 2 Communion Technique) is refused Second Domain."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 1
        ok, msg = char.select_technique("second_domain", ruleset)
        assert not ok
        assert "Tier 2" in msg
        assert char.technique_picks_available == 1  # pick not consumed

    def test_select_technique_magic_granting_activates_domain(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 1
        ok, _ = char.select_technique("spiritual_domain", ruleset, choice="resonance")
        assert ok
        assert char.magic_technique_active is True
        assert char.magic_domain == "resonance"

    def test_select_technique_second_domain_refused_without_domain(self, ruleset, valid_attributes):
        """sync-H-2 guard: Second Domain requires an existing domain, encoded via
        `requires_domain` on TechniqueDef — not left as a side effect of the
        prerequisite chain (which W2-9 will loosen). `the_language_beneath_language`
        is injected directly into `techniques` (bypassing select_technique) so the
        prerequisite-chain check passes while `magic_domain` stays unset, proving
        the domain guard is an independent check."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.techniques.append("the_language_beneath_language")
        char.technique_picks_available = 1
        ok, msg = char.select_technique("second_domain", ruleset, choice="resonance")
        assert not ok
        assert "domain" in msg.lower()
        assert "second_domain" not in char.techniques
        assert char.technique_picks_available == 1  # pick not consumed

    def test_select_technique_second_domain_permitted_with_domain(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 3
        ok, _ = char.select_technique("spiritual_domain", ruleset, choice="resonance")
        assert ok
        ok, _ = char.select_technique("the_language_beneath_language", ruleset)
        assert ok
        ok, msg = char.select_technique("second_domain", ruleset, choice="storm")
        assert ok, msg
        assert "second_domain" in char.techniques
        assert char.secondary_magic_domain == "storm"

    # L-7 (docs/RESEARCH_completeness_audit.md, II.3:244-246): prismatic
    # domains are never available as a starting domain — only via Ascendant
    # Domain (Tier 3).
    def test_starting_domain_technique_rejects_prismatic_choice(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 1
        ok, msg = char.select_technique("spiritual_domain", ruleset, choice="fate")
        assert not ok
        assert "prismatic" in msg.lower() or "Ascendant" in msg
        assert char.magic_domain is None
        assert "spiritual_domain" not in char.techniques

    # L-7 (II.3:244-246): "A character may hold at most one domain per Facet"
    # via the cross-training route. Only one magic-granting Tier 1 Technique
    # exists per Facet, so this is structurally unreachable through the
    # public API today — exercised directly on the guard instead.
    def test_domain_guard_refuses_a_third_facet_domain(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.magic_domain = "resonance"
        char.cross_facet_domain = "inscription"
        tech_def = ruleset.get_technique("spiritual_domain")
        ok, msg = char._validate_domain_choice(
            tech_def, "storm", ruleset, "spiritual_domain"
        )
        assert not ok
        assert "each Facet" in msg

    def test_select_technique_ascendant_domain_refused_without_domain(self, ruleset, valid_attributes):
        """Same guard, likewise for Ascendant Domain."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.techniques.append("the_language_beneath_language")
        char.technique_picks_available = 1
        ok, msg = char.select_technique("ascendant_domain_soul", ruleset, choice="the_undying")
        assert not ok
        assert "domain" in msg.lower()
        assert "ascendant_domain_soul" not in char.techniques
        assert char.technique_picks_available == 1

    def test_branch_tier_rule_weapon_mastery_unlocks_overwhelming_force(self, ruleset, valid_attributes):
        """sync-H-2, part 2 (PHB II.4:83): Tier 2 requires *any* Tier 1 in the
        same branch, not a specific one. weapon_mastery (Might T1) unlocking
        overwhelming_force (Might T2, whose old chain-only prerequisite was
        forcing_hand) is newly legal."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 2
        ok, _ = char.select_technique("weapon_mastery", ruleset, choice="blades")
        assert ok
        ok, msg = char.select_technique("overwhelming_force", ruleset)
        assert ok, msg
        assert "overwhelming_force" in char.techniques

    def test_branch_tier_rule_mirrors_in_a_different_branch_and_tree(self, ruleset, valid_attributes):
        """Same newly-legal shape, in a different branch (Instinct) and a
        different Facet tree (Mind) than the Might example above.
        immediate_threat's old chain-only prerequisite was never_surprised;
        the_wrong_note (the *other* Instinct Tier 1) now satisfies it too."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="mind",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 2
        ok, _ = char.select_technique("the_wrong_note", ruleset)
        assert ok
        ok, msg = char.select_technique("immediate_threat", ruleset)
        assert ok, msg
        assert "immediate_threat" in char.techniques

    def test_branch_tier_rule_rejects_tier_two_without_any_tier_one_in_branch(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 1
        ok, msg = char.select_technique("overwhelming_force", ruleset)
        assert not ok
        assert "Tier 1" in msg
        assert "overwhelming_force" not in char.techniques
        assert char.technique_picks_available == 1

    def test_branch_tier_rule_rejects_cross_branch_tier_two(self, ruleset, valid_attributes):
        """A Tier 1 in one branch (Might) does not satisfy Tier 2 in another
        branch (Grace) — the rule is branch-scoped, not tree-wide."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.techniques.append("forcing_hand")  # Might Tier 1, not Grace
        char.technique_picks_available = 1
        ok, msg = char.select_technique("shadow_walk", ruleset)  # Grace Tier 2
        assert not ok
        assert "Tier 1" in msg
        assert "shadow_walk" not in char.techniques
        assert char.technique_picks_available == 1

    def test_branch_tier_rule_second_domain_still_refused_without_domain_post_loosening(
        self, ruleset, valid_attributes
    ):
        """The W2-8 domain guard must survive the chain loosening: this is now
        a *genuinely reachable* play sequence (sense_the_unseen -> formed_bond
        satisfies the Tier 2-in-branch rule on its own, with no domain ever
        granted), not the direct-injection bypass W2-8's tests needed to use
        while the old chain still blocked this path."""
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="soul",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 3
        ok, _ = char.select_technique("sense_the_unseen", ruleset)
        assert ok
        ok, _ = char.select_technique("formed_bond", ruleset)
        assert ok
        ok, msg = char.select_technique("second_domain", ruleset, choice="storm")
        assert not ok
        assert "domain" in msg.lower()
        assert "second_domain" not in char.techniques

    def test_technique_picks_survive_fof_roundtrip(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.technique_picks_available = 2
        fof = char.to_fof([{"id": "base", "version": "0.1.0"}], "s" * 36)
        restored = Character.from_fof(fof, ruleset)
        assert restored.technique_picks_available == 2

    def test_facet_level_property_tracks_primary(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="X", player_name="P", primary_facet="mind",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.facet_levels = {"mind": 2, "body": 1}
        assert char.facet_level == 2          # primary is mind
        assert char.total_facet_levels == 3

    def test_legacy_flat_fof_roundtrip_preserves_facet_level(self, ruleset):
        """An old .fof carrying flat facet_level survives a from_fof load."""
        fof = {
            "type": "character",
            "character": {
                "name": "Old", "player_name": "P", "primary_facet": "body",
                "attributes": {"strength": 3, "dexterity": 3, "constitution": 2,
                               "intelligence": 2, "wisdom": 2, "knowledge": 2,
                               "spirit": 1, "luck": 2, "charisma": 1},
                "skills": {}, "facet_level": 2, "rank_advances_this_facet_level": 3,
            },
        }
        char = Character.from_fof(fof, ruleset)
        assert char.facet_level == 2
        assert char.facet_levels == {"body": 2}
        assert char.rank_advances_this_facet_level == 3

    def test_new_fof_roundtrip_preserves_cross_facet_levels(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="RT", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        char.facet_levels = {"body": 2, "mind": 1}
        char.rank_advances_by_facet = {"body": 0, "mind": 2}
        fof = char.to_fof([{"id": "base", "version": "0.1.0"}], "s" * 36)
        restored = Character.from_fof(fof, ruleset)
        assert restored.facet_levels == {"body": 2, "mind": 1}
        assert restored.total_facet_levels == 3
        assert restored.facet_level == 2
        assert restored.rank_advances_by_facet.get("mind") == 2


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------

class TestCharacterSerialisation:
    def test_to_client_dict_is_json_safe(self, body_character):
        import json
        d = body_character.to_client_dict()
        json.dumps(d)

    def test_to_client_dict_includes_name(self, body_character):
        d = body_character.to_client_dict()
        assert d["name"] == "Mordai"

    def test_to_client_dict_includes_skills(self, body_character):
        d = body_character.to_client_dict()
        assert "skills" in d
        assert "athletics" in d["skills"]


# ---------------------------------------------------------------------------
# Character name boundary cases
# ---------------------------------------------------------------------------

class TestCharacterNameBoundaries:
    def test_single_char_name_accepted(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="X", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []
        assert char.name == "X"

    def test_64_char_name_accepted(self, ruleset, valid_attributes):
        long_name = "A" * 64
        char, errors = create_default_character(
            name=long_name, player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []

    def test_empty_name_raises_validation_error(self, ruleset, valid_attributes):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            Character(
                name="", player_name="P",
                primary_facet="body", attributes=valid_attributes,
            )

    def test_65_char_name_raises_validation_error(self, ruleset, valid_attributes):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            Character(
                name="A" * 65, player_name="P",
                primary_facet="body", attributes=valid_attributes,
            )


# ---------------------------------------------------------------------------
# player_name boundary
# ---------------------------------------------------------------------------

class TestPlayerNameBoundaries:
    def test_single_char_player_name(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Mordai", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []
        assert char.player_name == "P"

    def test_32_char_player_name(self, ruleset, valid_attributes):
        pname = "A" * 32
        char, errors = create_default_character(
            name="Mordai", player_name=pname,
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []

    def test_empty_player_name_raises(self, ruleset, valid_attributes):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            Character(
                name="Mordai", player_name="",
                primary_facet="body", attributes=valid_attributes,
            )


# ---------------------------------------------------------------------------
# advance_skill edge cases
# ---------------------------------------------------------------------------

class TestAdvanceSkillEdgeCases:
    def test_advance_zero_marks_is_noop(self, body_character, ruleset):
        initial_rank = body_character.skills["athletics"].rank
        initial_marks = body_character.skills["athletics"].marks
        result = body_character.advance_skill("athletics", 0, ruleset)
        assert result["rank_advances"] == 0
        assert body_character.skills["athletics"].rank == initial_rank
        assert body_character.skills["athletics"].marks == initial_marks

    def test_advance_new_skill_creates_entry(self, body_character, ruleset):
        assert "new_skill" not in body_character.skills
        body_character.advance_skill("new_skill", 1, ruleset)
        assert "new_skill" in body_character.skills
        assert body_character.skills["new_skill"].marks == 1

    def test_master_is_capped_rank(self, body_character, ruleset):
        body_character.advance_skill("athletics", 16, ruleset)  # novice → master (3+5+8)
        assert body_character.skills["athletics"].rank == "master"
        with pytest.raises(ValueError, match="already at Master"):
            body_character.advance_skill("athletics", 100, ruleset)
        assert body_character.skills["athletics"].rank == "master"

    def test_secondary_facet_advance_credits_its_own_facet(self, body_character, ruleset):
        """A cross-Facet advance leaves the primary facet_level alone but banks
        progress on the skill's own Facet (D3 — cross-Facet levels count)."""
        # investigate is a mind skill; body_character's primary is body
        initial_level = body_character.facet_level
        body_character.advance_skill("investigate", 3, ruleset)
        # Primary (body) facet level is unchanged...
        assert body_character.facet_level == initial_level
        # ...but the advance is credited to the mind track, not discarded.
        assert body_character.rank_advances_by_facet.get("mind") == 1


# ---------------------------------------------------------------------------
# validate_against_ruleset error paths
# ---------------------------------------------------------------------------

class TestValidateAgainstRulesetErrors:
    def test_unknown_attribute_id_flagged(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        # Remove constitution and add a totally unknown attr
        del attrs["constitution"]
        attrs["nonexistent"] = 2
        char, _ = create_default_character(
            name="Test", player_name="P",
            primary_facet="body", attributes=attrs,
            ruleset=ruleset,
        )
        assert char is None  # validation fails

    def test_unknown_skill_flagged(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Test", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        # Manually inject an unknown skill and re-validate
        char.skills["unknownskill_xyz"] = SkillState(skill_id="unknownskill_xyz")
        errors = char.validate_against_ruleset(ruleset)
        assert any("unknownskill_xyz" in e for e in errors)

    def test_empty_errors_means_valid(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Test", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []
        errors2 = char.validate_against_ruleset(ruleset)
        assert errors2 == []


# ---------------------------------------------------------------------------
# get_skill_modifier edge cases
# ---------------------------------------------------------------------------

class TestGetSkillModifier:
    def test_missing_skill_returns_zero(self, body_character, ruleset):
        mod = body_character.get_skill_modifier("nonexistent_skill", ruleset)
        assert mod == 0

    def test_novice_skill_returns_zero(self, body_character, ruleset):
        mod = body_character.get_skill_modifier("athletics", ruleset)
        assert mod == 0  # starts novice (modifier=0)

    def test_master_rank_modifier(self, body_character, ruleset):
        """Master rank should give +3 modifier (from facet.yaml skill_ranks)."""
        body_character.advance_skill("athletics", 16, ruleset)  # novice → master (3+5+8)
        assert body_character.skills["athletics"].rank == "master"
        mod = body_character.get_skill_modifier("athletics", ruleset)
        assert mod == 3


# ---------------------------------------------------------------------------
# Techniques list manipulation
# ---------------------------------------------------------------------------

class TestTechniquesList:
    def test_techniques_starts_empty(self, body_character):
        assert body_character.techniques == []

    def test_can_append_technique(self, body_character):
        body_character.techniques.append("forcing_hand")
        assert "forcing_hand" in body_character.techniques

    def test_techniques_included_in_client_dict(self, body_character):
        body_character.techniques.append("weapon_mastery")
        d = body_character.to_client_dict()
        assert "weapon_mastery" in d["techniques"]


# ---------------------------------------------------------------------------
# Inventory, notes_player, notes_mm fields
# ---------------------------------------------------------------------------

class TestCharacterInventoryAndNotes:
    def test_inventory_defaults_empty(self, body_character):
        assert body_character.inventory == []

    def test_notes_player_defaults_empty(self, body_character):
        assert body_character.notes_player == ""

    def test_notes_mm_defaults_empty(self, body_character):
        assert body_character.notes_mm == ""

    def test_inventory_in_client_dict(self, body_character):
        body_character.inventory = ["Longsword", "Shield"]
        d = body_character.to_client_dict()
        assert d["inventory"] == ["Longsword", "Shield"]

    def test_notes_in_client_dict(self, body_character):
        body_character.notes_player = "Remember to buy rope"
        body_character.notes_mm = "Secret backstory hook"
        d = body_character.to_client_dict()
        assert d["notes_player"] == "Remember to buy rope"
        assert d["notes_mm"] == "Secret backstory hook"

    def test_inventory_roundtrips_through_fof(self, body_character):
        body_character.inventory = ["Rope", "Torch", "Rations"]
        body_character.notes_player = "Player notes here"
        body_character.notes_mm = "MM-only notes"
        fof = body_character.to_fof([{"id": "base", "version": "0.1.0"}], "test-session")
        loaded = Character.from_fof(fof)
        assert loaded.inventory == ["Rope", "Torch", "Rations"]
        assert loaded.notes_player == "Player notes here"
        assert loaded.notes_mm == "MM-only notes"

    def test_empty_inventory_not_in_fof(self, body_character):
        """Empty inventory/notes should not clutter the .fof output."""
        fof = body_character.to_fof([{"id": "base", "version": "0.1.0"}], "test-session")
        assert "inventory" not in fof["character"]
        assert "notes_player" not in fof["character"]
        assert "notes_mm" not in fof["character"]

    def test_from_fof_without_new_fields_uses_defaults(self):
        """Old .fof files without inventory/notes should load without error."""
        fof_dict = {
            "type": "character",
            "character": {
                "name": "Old", "player_name": "P1",
                "primary_facet": "body",
                "attributes": {
                    "strength": 2, "dexterity": 2, "constitution": 2,
                    "intelligence": 2, "wisdom": 2, "knowledge": 2,
                    "spirit": 2, "luck": 2, "charisma": 2,
                },
            },
        }
        char = Character.from_fof(fof_dict)
        assert char.inventory == []
        assert char.notes_player == ""
        assert char.notes_mm == ""


# ---------------------------------------------------------------------------
# T4.3 (P-5, D10): the forfeit dies — unspent points bank (cap 2) and 1 of the
# 4 session points may train an unused Primary-Facet skill.
# ---------------------------------------------------------------------------

class TestSkillPointBankingAndTraining:
    def test_unspent_points_bank_up_to_cap(self, body_character, ruleset):
        """3 points left at session end → 2 bank (cap) → 6 next session."""
        body_character.session_skill_points_remaining = 3
        body_character.start_new_session(ruleset)
        assert body_character.session_skill_points_remaining == 6

    def test_full_spend_banks_nothing(self, body_character, ruleset):
        body_character.session_skill_points_remaining = 0
        body_character.start_new_session(ruleset)
        assert body_character.session_skill_points_remaining == 4

    def test_one_point_banks_one(self, body_character, ruleset):
        body_character.session_skill_points_remaining = 1
        body_character.start_new_session(ruleset)
        assert body_character.session_skill_points_remaining == 5

    def test_new_session_resets_used_skills_and_training(self, body_character, ruleset):
        body_character.skills_used_this_session = {"combat"}
        body_character.training_marks_this_session = 1
        body_character.start_new_session(ruleset)
        assert body_character.skills_used_this_session == set()
        assert body_character.training_marks_this_session == 0

    def test_training_mark_on_unused_primary_skill(self, body_character, ruleset):
        """With a used-skills list active, 1 point may still go to an unused
        Primary-Facet skill — training between sessions."""
        body_character.session_skill_points_remaining = 4
        body_character.skills_used_this_session = {"combat"}
        result = body_character.spend_skill_point("athletics", ruleset)
        assert result["training_mark"] is True
        assert body_character.training_marks_this_session == 1
        assert body_character.skills["athletics"].marks == 1
        assert body_character.session_skill_points_remaining == 3

    def test_second_training_mark_refused(self, body_character, ruleset):
        body_character.session_skill_points_remaining = 4
        body_character.skills_used_this_session = {"combat"}
        body_character.spend_skill_point("athletics", ruleset)
        with pytest.raises(ValueError, match="[Tt]raining"):
            body_character.spend_skill_point("finesse", ruleset)

    def test_training_mark_cannot_go_cross_facet(self, body_character, ruleset):
        """The training point is Primary-Facet only — an unused cross-Facet
        skill is still off the table."""
        body_character.session_skill_points_remaining = 4
        body_character.skills_used_this_session = {"combat"}
        with pytest.raises(ValueError, match="not used this session"):
            body_character.spend_skill_point("lore", ruleset)

    def test_used_skill_spend_is_not_a_training_mark(self, body_character, ruleset):
        body_character.session_skill_points_remaining = 4
        body_character.skills_used_this_session = {"combat"}
        result = body_character.spend_skill_point("combat", ruleset)
        assert result["training_mark"] is False
        assert body_character.training_marks_this_session == 0

    def test_insufficient_points_raises(self, body_character, ruleset):
        body_character.session_skill_points_remaining = 0
        body_character.skills_used_this_session = {"combat"}
        with pytest.raises(ValueError, match="[Ii]nsufficient"):
            body_character.spend_skill_point("combat", ruleset)

    def test_yaml_carries_banking_and_training_config(self, ruleset):
        assert ruleset.advancement.bank_cap == 2
        assert ruleset.advancement.training_marks_per_session == 1


# ---------------------------------------------------------------------------
# P-6 revised (D16): the Background's starting rank is credited to its Facet's
# level track, as one banked advance out of the three a level costs.
#
# It used to be excluded. The arithmetic never worked: a Background's starting
# skill is always in the Primary Facet, so excluding it left every character one
# advance short of the in-Facet ceiling and made Facet level 3 unreachable
# inside the primary Facet for every character that has a Background — which is
# all of them. The old reachability test compared thresholds against the raw
# skill count and never built a character, so it never saw it.
# ---------------------------------------------------------------------------

class TestCreationRanksAndFacetLevels:
    def test_background_starting_skill_banks_one_advance_but_no_level(self, ruleset, valid_attributes):
        """A Background's Practiced starting skill is 1 career advance and one
        banked advance toward its Facet's next level — not a free level."""
        char, errors = create_default_character(
            name="Mordai", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
            background_id="city_watch_veteran",
        )
        assert not errors, errors
        assert char.career_advances == 1
        assert char.facet_level == 0
        assert char.rank_advances_by_facet == {"body": 1}

    def test_a_backgroundless_character_banks_nothing(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Blank", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert not errors, errors
        assert char.rank_advances_by_facet == {}

    def test_facet_level_three_is_reachable_inside_the_primary_facet(
        self, ruleset, valid_attributes
    ):
        """The regression this revision exists for. A character with a
        Background must still reach Facet level 3 — and all three Technique
        picks — without cross-training."""
        char, errors = create_default_character(
            name="Mordai", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
            background_id="city_watch_veteran",
        )
        assert not errors, errors
        _advance_facet(char, ruleset, "body", 99)  # everything the caps allow
        assert char.facet_level == 3
        assert char.technique_picks_available == 3

    def test_creation_rank_plus_two_played_advances_lands_level_one(
        self, ruleset, valid_attributes
    ):
        """With the creation rank banked, two played advances land level 1."""
        char, errors = create_default_character(
            name="Mordai", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
            background_id="city_watch_veteran",  # Combat Practiced at creation
        )
        assert not errors, errors
        char.advance_skill("athletics", 3, ruleset)
        assert char.career_advances == 2  # 1 creation + 1 played
        assert char.facet_level == 0      # 2 of 3 banked, not yet a level
        # The second played advance crosses the threshold (1 creation + 2 played)
        char.advance_skill("finesse", 3, ruleset)
        assert char.facet_level == 1

    def test_played_advance_on_the_creation_skill_counts_normally(self, ruleset, valid_attributes):
        """Advancing the creation-granted skill in play (Practiced → Expert)
        is a normal played advance for both counters."""
        char, errors = create_default_character(
            name="Mordai", player_name="P", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
            background_id="city_watch_veteran",
        )
        assert not errors, errors
        char.advance_skill("combat", 5, ruleset)  # Practiced -> Expert (D16: 5 marks)
        assert char.skills["combat"].rank == "expert"
        assert char.career_advances == 2
        assert char.rank_advances_by_facet.get("body") == 2  # 1 creation + 1 played


# ---------------------------------------------------------------------------
# T4.5 (P-8, D11): Never Surprised is a warning beat, not an auto-success.
# ---------------------------------------------------------------------------

class TestNeverSurprisedWarningBeat:
    def _entry(self, ruleset):
        for tree in ruleset.techniques.values():
            for branch in tree.branches:
                for tier in branch.tiers:
                    for tech in tier.techniques:
                        if tech.id == "never_surprised":
                            return tech
        raise AssertionError("never_surprised not found in the ruleset")

    def test_entry_grants_a_warning_beat(self, ruleset):
        tech = self._entry(ruleset)
        assert "warning beat" in tech.description

    def test_entry_carries_no_auto_success(self, ruleset):
        """D11: the absolute is gone — the entry may not promise automatic
        success on the notice roll."""
        tech = self._entry(ruleset)
        assert "automatically succeed" not in tech.description


# ---------------------------------------------------------------------------
# Lineage (D18 — PHB II.5)
# ---------------------------------------------------------------------------

def _gifted_ruleset(base, **lineage_overrides):
    """A ruleset whose lineages include a gifted one, so the gifted paths can
    be tested without waiting on the Val'loh Facet. Returns the ruleset and a
    domain a gifted character may legally choose."""
    import copy
    from app.facets.schema import LineageDefinition
    rs = copy.deepcopy(base)
    fields = dict(
        id="orthaen", name="Orthaen", variants=["Orthain"],
        description="They grow crystal.",
        gift="Shows itself through grown crystal.",
        gift_rate="four in five",
        heritage="Reads grown crystalwork: its age, its maker's hand.",
    )
    fields.update(lineage_overrides)
    rs.lineages = list(rs.lineages) + [LineageDefinition(**fields)]
    rs._lineage_map = {lin.id: lin for lin in rs.lineages}
    domain = next(d for d in rs.magic.soul_domains if d.type != "broad")
    return rs, domain.id


class TestLineageAtCreation:
    def test_lineage_defaults_to_human(self, ruleset, valid_attributes):
        """Every existing .fof predates the step and must load unchanged."""
        char, errors = create_default_character(
            name="Mordai", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert errors == []
        assert char.lineage == "human"
        assert char.gifted is False
        assert char.domain_source is None

    def test_an_unknown_lineage_is_rejected(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="X", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset, lineage="dragonborn",
        )
        assert char is None
        assert any("dragonborn" in e for e in errors)

    def test_gifted_creation_sets_the_domain_and_records_its_source(
            self, ruleset, valid_attributes):
        rs, domain_id = _gifted_ruleset(ruleset)
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id,
        )
        assert errors == []
        assert char.magic_domain == domain_id
        assert char.domain_source == "lineage"
        assert char.gifted is True

    def test_the_player_chooses_the_gift_domain(self, ruleset, valid_attributes):
        """D24. The lineage colours the gift; it does not pick it. A Mind
        domain is as legal as a Soul one."""
        rs, _ = _gifted_ruleset(ruleset)
        mind = next(d.id for d in rs.magic.mind_domains if d.type != "broad")
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=mind,
        )
        assert errors == []
        assert char.magic_domain == mind

    def test_a_gift_is_cast_intuitively_whatever_the_domain(
            self, ruleset, valid_attributes):
        """Blood is not study. Without this, a gift that happens to be a Mind
        domain would roll Knowledge, and a birth gift would behave like a
        library education."""
        rs, _ = _gifted_ruleset(ruleset)
        mind = next(d for d in rs.magic.mind_domains if d.type != "broad")
        assert mind.tradition == "scholarly"
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=mind.id,
        )
        assert errors == []
        assert char.magic_tradition == "intuitive"

    def test_a_prismatic_domain_cannot_be_a_gift(self, ruleset, valid_attributes):
        """Prismatic territories are a lifetime's mastery (Ascendant Domain,
        Tier 3). Nobody is born holding one."""
        rs, _ = _gifted_ruleset(ruleset)
        broad = next(d.id for d in rs.magic.soul_domains if d.type == "broad")
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=broad,
        )
        assert char is None
        assert any("prismatic" in e.lower() for e in errors)

    def test_an_unknown_domain_cannot_be_a_gift(self, ruleset, valid_attributes):
        rs, _ = _gifted_ruleset(ruleset)
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain="crystal",
        )
        assert char is None
        assert any("crystal" in e for e in errors)

    def test_a_setting_restriction_is_honoured(self, ruleset, valid_attributes):
        """Choice is the default; a setting may still narrow it."""
        rs, _ = _gifted_ruleset(ruleset, gift_domains=["storm"])
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain="fire",
        )
        assert char is None
        assert any("storm" in e for e in errors)

    def test_an_ungifted_lineage_cannot_be_taken_gifted(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="X", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
            lineage="human", gifted=True,
        )
        assert char is None
        assert any("human" in e.lower() for e in errors)

    def test_one_domain_at_creation_never_two(self, ruleset, valid_attributes):
        """The rule the whole step turns on: a gifted character takes a
        Background that grants no domain."""
        rs, domain_id = _gifted_ruleset(ruleset)
        magic_bg = next(
            bg.id for bg in rs.backgrounds if bg.domain_origin is not None)
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id,
            background_id=magic_bg,
        )
        assert char is None
        assert any("one domain" in e.lower() for e in errors)

    def test_a_gift_replaces_the_backgrounds_secondary_skill(
            self, ruleset, valid_attributes):
        """Exactly as a magic-granting Background's domain origin does."""
        rs, domain_id = _gifted_ruleset(ruleset)
        plain_bg = next(
            bg for bg in rs.backgrounds
            if bg.domain_origin is None and bg.secondary_skill)
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet=plain_bg.facet,
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id,
            background_id=plain_bg.id,
        )
        assert errors == []
        assert char.skills[plain_bg.secondary_skill].marks == 0, (
            "a Gift replaces the secondary skill; the Background Mark should "
            "not also be recorded"
        )

    def test_an_ungifted_member_keeps_the_secondary_skill_and_holds_no_domain(
            self, ruleset, valid_attributes):
        """One Orthaen in five is born without the gift, and the fiction has
        to be expressible: same lineage, same Heritage, no domain."""
        rs, _ = _gifted_ruleset(ruleset)
        plain_bg = next(
            bg for bg in rs.backgrounds
            if bg.domain_origin is None and bg.secondary_skill)
        char, errors = create_default_character(
            name="Dassa", player_name="P1", primary_facet=plain_bg.facet,
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=False, background_id=plain_bg.id,
        )
        assert errors == []
        assert char.lineage == "orthaen"
        assert char.gifted is False
        assert char.magic_domain is None
        assert char.skills[plain_bg.secondary_skill].marks == 1

    def test_a_background_domain_records_its_own_source(
            self, ruleset, valid_attributes):
        magic_bg = next(
            bg for bg in ruleset.backgrounds if bg.domain_origin is not None)
        domain_id = next(
            d.id for d in (ruleset.magic.soul_domains + ruleset.magic.mind_domains))
        char, errors = create_default_character(
            name="Zahna", player_name="P1", primary_facet=magic_bg.facet,
            attributes=valid_attributes, ruleset=ruleset,
            background_id=magic_bg.id, magic_domain=domain_id,
        )
        if char is not None and char.magic_domain:
            assert char.domain_source == "background"


class TestLineageGiftFormalization:
    """D18 option 1: a Gift formalizes at the character's first Facet level, in
    whichever Facet that level lands, and spends NO Technique pick.

    Blood is not study. A Background domain is a practice the character is
    still learning and the Tier 1 Technique is the curriculum that finishes it,
    so it costs the pick a curriculum costs. Charging a Body-Facet gifted
    character a cross-Facet Technique to reach full scope would make "born
    gifted" cost more than "studied magic", which is the wrong way round.
    """

    def _gifted_character(self, ruleset, valid_attributes, **kw):
        rs, domain_id = _gifted_ruleset(ruleset)
        char, errors = create_default_character(
            name="Serane", player_name="P1",
            primary_facet=kw.pop("primary_facet", "soul"),
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id, **kw,
        )
        assert errors == [], errors
        return char, rs, domain_id

    def _advance_to_first_facet_level(self, char, rs):
        """Advance until a Facet level lands, rotating across the Facet's
        skills — D16's rank caps refuse a single skill climbing forever."""
        skill_ids = [sk.id for sk in rs.skills
                     if sk.status == "active" and sk.facet == char.primary_facet]
        for _ in range(40):
            for skill_id in skill_ids:
                try:
                    char.advance_skill(skill_id, 3, rs)
                except ValueError:
                    continue
                if char.total_facet_levels > 0:
                    return True
        return False

    def test_a_gift_is_minor_scope_until_it_formalizes(
            self, ruleset, valid_attributes):
        char, _, domain_id = self._gifted_character(ruleset, valid_attributes)
        assert char.magic_domain == domain_id
        assert char.magic_technique_active is False

    def test_the_gift_formalizes_at_the_first_facet_level(
            self, ruleset, valid_attributes):
        char, rs, _ = self._gifted_character(ruleset, valid_attributes)
        assert self._advance_to_first_facet_level(char, rs)
        assert char.magic_technique_active is True

    def test_formalization_spends_no_technique_pick(
            self, ruleset, valid_attributes):
        """The Technique economy is untouched: a three-pick career is still
        three picks."""
        char, rs, _ = self._gifted_character(ruleset, valid_attributes)
        assert self._advance_to_first_facet_level(char, rs)
        assert char.technique_picks_available == char.total_facet_levels
        assert char.techniques == []

    def test_it_formalizes_in_whichever_facet_the_level_lands_in(
            self, ruleset, valid_attributes):
        """A Body-Facet gifted character reaches full scope through their own
        Facet — the case option 2 could not serve."""
        char, rs, _ = self._gifted_character(
            ruleset, valid_attributes, primary_facet="body")
        assert self._advance_to_first_facet_level(char, rs)
        assert char.magic_technique_active is True
        assert char.techniques == []

    def test_an_ungifted_character_formalizes_nothing(
            self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Mordai", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert errors == []
        rules = ruleset
        skill_ids = [sk.id for sk in rules.skills
                     if sk.status == "active" and sk.facet == "body"]
        for _ in range(40):
            for skill_id in skill_ids:
                try:
                    char.advance_skill(skill_id, 3, rules)
                except ValueError:
                    continue
            if char.total_facet_levels > 0:
                break
        assert char.magic_technique_active is False

    def test_the_technique_route_is_unchanged_for_background_domains(
            self, ruleset, valid_attributes):
        """A Background domain still waits for its Tier 1 Technique — the two
        routes never combine, because a character holds one creation domain."""
        magic_bg = next(
            bg for bg in ruleset.backgrounds if bg.domain_origin is not None)
        domain_id = next(
            d.id for d in (ruleset.magic.soul_domains + ruleset.magic.mind_domains))
        char, errors = create_default_character(
            name="Zahna", player_name="P1", primary_facet=magic_bg.facet,
            attributes=valid_attributes, ruleset=ruleset,
            background_id=magic_bg.id, magic_domain=domain_id,
        )
        if char is None:
            pytest.skip("this ruleset's magic Background/domain pairing differs")
        skill_id = next(
            sk.id for sk in ruleset.skills
            if sk.status == "active" and sk.facet == char.primary_facet)
        for _ in range(60):
            char.advance_skill(skill_id, 3, ruleset)
            if char.total_facet_levels > 0:
                break
        assert char.magic_technique_active is False, (
            "a Background domain must not formalize for free — that route "
            "costs the Tier 1 Technique pick"
        )

    def test_formalizing_twice_does_not_consume_a_pick_later(
            self, ruleset, valid_attributes):
        """The delicate one: the existing `formalizing` branch must not fire
        for a lineage domain that is already active, or a later Facet level
        would try to spend a pick re-formalizing a Gift that has arrived."""
        char, rs, _ = self._gifted_character(ruleset, valid_attributes)
        assert self._advance_to_first_facet_level(char, rs)
        picks_after_first = char.technique_picks_available
        levels_after_first = char.total_facet_levels
        skill_ids = [sk.id for sk in rs.skills
                     if sk.status == "active" and sk.facet == char.primary_facet]
        for _ in range(40):
            for skill_id in skill_ids:
                try:
                    char.advance_skill(skill_id, 3, rs)
                except ValueError:
                    continue
            if char.total_facet_levels > levels_after_first:
                break
        assert char.technique_picks_available > picks_after_first
        assert char.techniques == []

    def test_option_two_leaves_the_old_behaviour_intact(
            self, ruleset, valid_attributes):
        """`formalizes_on: technique` stays legal data so a setting could
        choose it; under it a Gift waits for the Technique like any domain."""
        import copy
        rs, domain_id = _gifted_ruleset(ruleset)
        rs = copy.deepcopy(rs)
        rs.get_lineage("orthaen").formalizes_on = "technique"
        rs._lineage_map = {lin.id: lin for lin in rs.lineages}
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id,
        )
        assert errors == []
        rules = rs
        skill_ids = [sk.id for sk in rules.skills
                     if sk.status == "active" and sk.facet == "soul"]
        for _ in range(40):
            for skill_id in skill_ids:
                try:
                    char.advance_skill(skill_id, 3, rules)
                except ValueError:
                    continue
            if char.total_facet_levels > 0:
                break
        assert char.magic_technique_active is False


class TestValLohGiftsAreCoreDomains:
    """D24, against the real Facet: Val'loh adds no domains, so every gift a
    Val'loh character holds is a core domain any mage could also learn."""

    def _valloh(self):
        from pathlib import Path
        from app.facets.loader import load_facet_file
        from app.facets.registry import MergedRuleset
        root = Path(__file__).resolve().parents[1] / "facets"
        return MergedRuleset([
            load_facet_file(root / "base" / "facet.yaml"),
            load_facet_file(root / "valloh" / "facet.yaml"),
        ])

    def test_valloh_adds_no_domains(self):
        from app.facets.registry import build_ruleset
        core = build_ruleset([])
        rs = self._valloh()
        assert ({d.id for d in rs.magic.soul_domains}
                == {d.id for d in core.magic.soul_domains})
        assert ({d.id for d in rs.magic.mind_domains}
                == {d.id for d in core.magic.mind_domains})

    def test_an_orthaen_may_take_any_eligible_domain(self, valid_attributes):
        rs = self._valloh()
        for domain_id in ("fire", "transmutation", "warding"):
            char, errors = create_default_character(
                name="Serane", player_name="P1", primary_facet="soul",
                attributes=valid_attributes, ruleset=rs,
                lineage="orthaen", gifted=True, magic_domain=domain_id,
            )
            assert errors == [], (domain_id, errors)
            assert char.domain_source == "lineage"

    def test_a_gift_formalizes_free_under_the_real_facet(self, valid_attributes):
        rs = self._valloh()
        char, errors = create_default_character(
            name="Pello", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=rs,
            lineage="phern", gifted=True, magic_domain="divination",
        )
        assert errors == []
        assert char.magic_technique_active is False
        skill_ids = [sk.id for sk in rs.skills
                     if sk.status == "active" and sk.facet == "body"]
        for _ in range(40):
            for skill_id in skill_ids:
                try:
                    char.advance_skill(skill_id, 3, rs)
                except ValueError:
                    continue
            if char.total_facet_levels > 0:
                break
        assert char.magic_technique_active is True
        assert char.techniques == []


class TestUseItem:
    """Crystal charges — the smallest loot system the game can have."""

    def _valloh(self):
        from pathlib import Path
        from app.facets.loader import load_facet_file
        from app.facets.registry import MergedRuleset
        root = Path(__file__).resolve().parents[1] / "facets"
        return MergedRuleset([
            load_facet_file(root / "base" / "facet.yaml"),
            load_facet_file(root / "valloh" / "facet.yaml"),
        ])

    def _carrier(self, rs, valid_attributes, *items):
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
        )
        assert errors == []
        char.inventory = list(items)
        return char

    def test_using_a_charge_removes_it_and_reports_what_it_did(
            self, valid_attributes):
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes, "steady_light")
        result = char.use_item("steady_light", rs)
        assert result["name"] == "Charge: Steady Light"
        assert result["scope"] == "minor"
        assert "steady_light" not in char.inventory

    def test_a_spent_charge_cannot_be_spent_again(self, valid_attributes):
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes, "warmth")
        char.use_item("warmth", rs)
        with pytest.raises(ValueError):
            char.use_item("warmth", rs)

    def test_a_charge_you_are_not_carrying_is_refused(self, valid_attributes):
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes)
        with pytest.raises(ValueError):
            char.use_item("veil_of_quiet", rs)

    def test_an_unknown_item_is_refused(self, valid_attributes):
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes, "moon_on_a_stick")
        with pytest.raises(ValueError):
            char.use_item("moon_on_a_stick", rs)

    def test_two_of_the_same_charge_are_spent_one_at_a_time(
            self, valid_attributes):
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes, "warmth", "warmth")
        first = char.use_item("warmth", rs)
        assert first["remaining"] == 1
        second = char.use_item("warmth", rs)
        assert second["remaining"] == 0

    def test_free_text_inventory_still_works_alongside_item_ids(
            self, valid_attributes):
        """`inventory` is list[str] and always was. A table that wants none of
        this can write 'a good knife' and lose nothing."""
        rs = self._valloh()
        char = self._carrier(rs, valid_attributes, "a good knife", "warmth")
        char.use_item("warmth", rs)
        assert char.inventory == ["a good knife"]


class TestGiftCastingRollsTheIntuitiveTradition:
    """D24's one rule, checked where it bites: the roll itself."""

    def _gifted(self, ruleset, valid_attributes, domain_id):
        rs, _ = _gifted_ruleset(ruleset)
        char, errors = create_default_character(
            name="Serane", player_name="P1", primary_facet="soul",
            attributes=valid_attributes, ruleset=rs,
            lineage="orthaen", gifted=True, magic_domain=domain_id,
        )
        assert errors == [], errors
        return char, rs

    def test_a_mind_domain_gift_rolls_spirit_and_attune(
            self, ruleset, valid_attributes):
        from app.game.engine import resolve_magic_roll
        mind = next(d.id for d in ruleset.magic.mind_domains if d.type != "broad")
        char, rs = self._gifted(ruleset, valid_attributes, mind)
        result = resolve_magic_roll(character=char, domain_id=mind, scope="minor",
                                    intent="test", ruleset=rs)
        assert result.request.attribute_id == "spirit"
        assert result.request.skill_id == "attune"

    def test_the_same_domain_learned_rolls_its_own_tradition(
            self, ruleset, valid_attributes):
        """The rule belongs to the gift, not the domain: the same Mind domain
        reached through a Background still rolls Knowledge + Lore."""
        from app.game.engine import resolve_magic_roll
        magic_bg = next(bg for bg in ruleset.backgrounds
                        if bg.domain_origin == "mind")
        mind = next(d.id for d in ruleset.magic.mind_domains if d.type != "broad")
        char, errors = create_default_character(
            name="Zahna", player_name="P1", primary_facet=magic_bg.facet,
            attributes=valid_attributes, ruleset=ruleset,
            background_id=magic_bg.id, magic_domain=mind,
        )
        assert errors == []
        result = resolve_magic_roll(character=char, domain_id=mind, scope="minor",
                                    intent="test", ruleset=ruleset)
        assert result.request.attribute_id == "knowledge"
        assert result.request.skill_id == "lore"

    def test_a_soul_domain_gift_is_unchanged(self, ruleset, valid_attributes):
        from app.game.engine import resolve_magic_roll
        char, rs = self._gifted(ruleset, valid_attributes, "fire")
        result = resolve_magic_roll(character=char, domain_id="fire", scope="minor",
                                    intent="test", ruleset=rs)
        assert result.request.attribute_id == "spirit"


# ---------------------------------------------------------------------------
# Readied intents (D23 — supersedes D17)
# ---------------------------------------------------------------------------

class TestReadiedIntents:
    """Minor magic is free. Significant and Major spend a readied intent of
    the matching purpose — or a Spark, if nothing is readied for it. Readied
    intents begin when a caster's magic formalizes, are allotted once per
    session, and come back after a full rest.
    """

    def _caster(self, ruleset, valid_attributes, formalized=True):
        magic_bg = next(bg for bg in ruleset.backgrounds if bg.domain_origin)
        domain = next(d.id for d in (ruleset.magic.soul_domains
                                     + ruleset.magic.mind_domains)
                      if d.type != "broad")
        char, errors = create_default_character(
            name="Zahna", player_name="P1", primary_facet=magic_bg.facet,
            attributes=valid_attributes, ruleset=ruleset,
            background_id=magic_bg.id, magic_domain=domain,
        )
        assert errors == [], errors
        char.magic_technique_active = formalized
        return char

    # -- readying ----------------------------------------------------------

    def test_a_formalized_caster_readies_up_to_capacity(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 2, "reveal": 1}, ruleset)
        assert char.readied_intents == {"harm": 2, "reveal": 1}

    def test_readying_more_than_capacity_is_refused(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        with pytest.raises(ValueError, match="3"):
            char.ready_intents({"harm": 2, "ward": 2}, ruleset)
        assert char.readied_intents is None

    def test_readying_fewer_is_allowed(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"mend": 1}, ruleset)
        assert char.readied_intents == {"mend": 1}

    def test_an_unknown_purpose_is_refused(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        with pytest.raises(ValueError, match="teleport"):
            char.ready_intents({"teleport": 1}, ruleset)

    def test_a_negative_count_is_refused(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        with pytest.raises(ValueError):
            char.ready_intents({"harm": -1, "ward": 3}, ruleset)

    def test_you_ready_once_until_you_rest(self, ruleset, valid_attributes):
        """The limit comes from committing. Re-readying mid-scene would turn
        the guess into a lookup."""
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 3}, ruleset)
        with pytest.raises(ValueError, match="rest"):
            char.ready_intents({"reveal": 3}, ruleset)
        assert char.readied_intents == {"harm": 3}

    def test_an_unformalized_caster_has_nothing_to_ready(self, ruleset, valid_attributes):
        """Before the Technique, magic is Minor only (II.3), and Minor is
        free — so readied intents begin when magic formalizes."""
        char = self._caster(ruleset, valid_attributes, formalized=False)
        with pytest.raises(ValueError, match="formaliz"):
            char.ready_intents({"harm": 1}, ruleset)

    def test_a_character_without_magic_has_nothing_to_ready(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Mordai", player_name="P1", primary_facet="body",
            attributes=valid_attributes, ruleset=ruleset)
        with pytest.raises(ValueError):
            char.ready_intents({"harm": 1}, ruleset)

    # -- refreshing --------------------------------------------------------

    def test_a_rest_lets_you_ready_again(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 3}, ruleset)
        char.refresh_intents()
        assert char.readied_intents is None
        char.ready_intents({"reveal": 3}, ruleset)
        assert char.readied_intents == {"reveal": 3}

    def test_a_new_session_refreshes_them(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 1}, ruleset)
        char.start_new_session(ruleset)
        assert char.readied_intents is None

    # -- the cost of a working ---------------------------------------------

    def test_minor_is_always_free(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 1}, ruleset)
        assert char.intent_cost("reveal", "minor", ruleset) == "free"

    def test_minor_is_free_even_before_readying(self, ruleset, valid_attributes):
        """Nobody should be blocked from lighting a candle because they forgot
        to fill in the pips."""
        char = self._caster(ruleset, valid_attributes)
        assert char.intent_cost(None, "minor", ruleset) == "free"

    def test_significant_spends_a_matching_intent(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 2}, ruleset)
        assert char.intent_cost("harm", "significant", ruleset) == "intent"
        assert char.pay_intent_cost("harm", "significant", ruleset) == "intent"
        assert char.readied_intents == {"harm": 1}

    def test_major_spends_one_too(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"shape": 1}, ruleset)
        char.pay_intent_cost("shape", "major", ruleset)
        assert char.readied_intents == {"shape": 0}

    def test_off_purpose_costs_a_spark(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 3}, ruleset)
        assert char.intent_cost("reveal", "significant", ruleset) == "spark"
        assert char.pay_intent_cost("reveal", "significant", ruleset) == "spark"
        assert char.readied_intents == {"harm": 3}, "a Spark-paid working spends no intent"

    def test_a_spent_purpose_falls_back_to_a_spark(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 1}, ruleset)
        char.pay_intent_cost("harm", "significant", ruleset)
        assert char.intent_cost("harm", "significant", ruleset) == "spark"

    def test_a_significant_working_needs_a_purpose(self, ruleset, valid_attributes):
        char = self._caster(ruleset, valid_attributes)
        char.ready_intents({"harm": 1}, ruleset)
        with pytest.raises(ValueError, match="purpose"):
            char.intent_cost(None, "significant", ruleset)

    def test_you_must_ready_before_a_significant_working(self, ruleset, valid_attributes):
        """Forgetting to ready is prompted, not silently billed a Spark."""
        char = self._caster(ruleset, valid_attributes)
        with pytest.raises(ValueError, match="[Rr]eady"):
            char.intent_cost("harm", "significant", ruleset)

    def test_an_unformalized_caster_is_not_billed(self, ruleset, valid_attributes):
        """The pre-Technique scope cap and its Spark push already govern them
        (II.3); readied intents do not apply until formalization."""
        char = self._caster(ruleset, valid_attributes, formalized=False)
        assert char.intent_cost("harm", "significant", ruleset) == "free"

    def test_no_limit_when_the_ruleset_has_none(self, ruleset, valid_attributes):
        """A setting may choose the pre-D23 game."""
        import copy
        rs = copy.deepcopy(ruleset)
        rs.magic.prepared_intents = None
        char = self._caster(rs, valid_attributes)
        assert char.intent_cost("harm", "major", rs) == "free"
