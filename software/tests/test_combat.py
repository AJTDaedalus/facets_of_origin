"""Tests for `app/game/combat.py` — the shared, pure combat-rules module."""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.facets.registry import build_ruleset
from app.game import combat


@pytest.fixture(scope="module")
def ruleset():
    return build_ruleset([])


# ---------------------------------------------------------------------------
# roll()
# ---------------------------------------------------------------------------

class TestRoll:
    def test_happy_path_returns_outcome_dice_total(self, ruleset):
        random.seed(1)
        result = combat.roll(0, "Standard", ruleset)
        assert result.outcome in ("full_success", "partial_success", "failure")
        assert len(result.dice) == 2
        assert result.total == sum(result.dice)

    def test_extra_dice_drops_lowest(self, ruleset):
        random.seed(1)
        result = combat.roll(0, "Standard", ruleset, extra_dice=2)
        # 4 dice rolled, lowest 2 dropped, 2 kept
        assert len(result.dice) == 2

    def test_difficulty_modifier_shifts_total(self, ruleset):
        random.seed(42)
        easy = combat.roll(0, "Easy", ruleset)
        random.seed(42)
        hard = combat.roll(0, "Hard", ruleset)
        # Same dice (same seed), Easy is +1 relative to Hard's -1
        assert easy.total == hard.total + 2

    def test_unknown_difficulty_defaults_to_zero_modifier(self, ruleset):
        random.seed(7)
        result = combat.roll(0, "Nonexistent", ruleset)
        random.seed(7)
        standard = combat.roll(0, "Standard", ruleset)
        assert result.total == standard.total


# ---------------------------------------------------------------------------
# armor_budget() / armor_downgrade() — D2 PC per-scene downgrade budget
# ---------------------------------------------------------------------------

class TestArmorBudget:
    def test_light_budget(self, ruleset):
        assert combat.armor_budget("light", ruleset) == 2

    def test_heavy_budget(self, ruleset):
        assert combat.armor_budget("heavy", ruleset) == 4

    def test_no_armor_budget_is_zero(self, ruleset):
        assert combat.armor_budget(None, ruleset) == 0
        assert combat.armor_budget("bogus", ruleset) == 0


class TestArmorDowngrade:
    def test_light_downgrades_hits_1_and_2_not_hit_3(self, ruleset):
        remaining = combat.armor_budget("light", ruleset)  # 2
        r1 = combat.armor_downgrade(2, "light", remaining, ruleset)
        assert r1.tier == 1 and r1.downgraded is True and r1.downgrades_remaining == 1

        r2 = combat.armor_downgrade(2, "light", r1.downgrades_remaining, ruleset)
        assert r2.tier == 1 and r2.downgraded is True and r2.downgrades_remaining == 0

        r3 = combat.armor_downgrade(2, "light", r2.downgrades_remaining, ruleset)
        assert r3.tier == 2 and r3.downgraded is False and r3.downgrades_remaining == 0

    def test_heavy_downgrades_hits_1_through_4_not_hit_5(self, ruleset):
        remaining = combat.armor_budget("heavy", ruleset)  # 4
        for expected_remaining in (3, 2, 1, 0):
            result = combat.armor_downgrade(2, "heavy", remaining, ruleset)
            assert result.tier == 1 and result.downgraded is True
            assert result.downgrades_remaining == expected_remaining
            remaining = result.downgrades_remaining

        result = combat.armor_downgrade(2, "heavy", remaining, ruleset)
        assert result.tier == 2 and result.downgraded is False and result.downgrades_remaining == 0

    def test_tier1_downgrade_is_fully_absorbed(self, ruleset):
        result = combat.armor_downgrade(1, "light", 2, ruleset)
        assert result.tier == 0
        assert result.downgraded is True
        assert result.downgrades_remaining == 1

    def test_budget_persists_across_end_exchange(self, ruleset):
        # end_exchange only ever touches a conditions list — the budget is a
        # separate counter passed explicitly, so nothing about calling it
        # should change what armor_downgrade sees on the next hit.
        remaining = combat.armor_budget("light", ruleset)
        r1 = combat.armor_downgrade(2, "light", remaining, ruleset)

        conditions = ["winded"]
        combat.end_exchange(conditions, ruleset)

        r2 = combat.armor_downgrade(2, "light", r1.downgrades_remaining, ruleset)
        assert r2.downgrades_remaining == remaining - 2

    def test_budget_resets_at_scene_end(self, ruleset):
        remaining = combat.armor_budget("heavy", ruleset)
        remaining = combat.armor_downgrade(2, "heavy", remaining, ruleset).downgrades_remaining
        remaining = combat.armor_downgrade(2, "heavy", remaining, ruleset).downgrades_remaining
        assert remaining == 2

        # Scene ends — re-fetch the starting budget rather than reusing `remaining`.
        remaining = combat.armor_budget("heavy", ruleset)
        assert remaining == 4

    def test_no_armor_is_a_no_op(self, ruleset):
        result = combat.armor_downgrade(2, None, 2, ruleset)
        assert result.tier == 2
        assert result.downgraded is False
        assert result.downgrades_remaining == 2

    def test_unknown_armor_string_is_a_no_op(self, ruleset):
        result = combat.armor_downgrade(2, "bogus", 2, ruleset)
        assert result.tier == 2
        assert result.downgraded is False

    def test_zero_budget_is_a_no_op(self, ruleset):
        result = combat.armor_downgrade(2, "light", 0, ruleset)
        assert result.tier == 2
        assert result.downgraded is False
        assert result.downgrades_remaining == 0

    def test_zero_tier_is_a_no_op(self, ruleset):
        result = combat.armor_downgrade(0, "light", 2, ruleset)
        assert result.tier == 0
        assert result.downgraded is False


# ---------------------------------------------------------------------------
# The breakability assertion (Brain, EF6) — a PC that only ever Absorbs
# against a lone Named enemy landing a guaranteed Tier 2 every exchange.
# Fully deterministic (no dice: Absorb doesn't roll and NPCs don't roll),
# so the exact Broken exchange for each armor state is asserted, not a band.
# This is the acceptance test for research/armored_enemy_breaking_problem.md.
# ---------------------------------------------------------------------------

class TestArmorBreakability:
    def _exchange_broken(self, ruleset, armor: str | None) -> int:
        """Run the fixed policy (Absorb every hit, enemy always lands the
        same Tier 2 type) and return the exchange number Broken lands on.
        """
        conditions: list[str] = []
        remaining = combat.armor_budget(armor, ruleset)
        exchange = 0
        while True:
            exchange += 1
            incoming_tier = 2
            downgrade = combat.armor_downgrade(incoming_tier, armor, remaining, ruleset)
            remaining = downgrade.downgrades_remaining
            tier = downgrade.tier

            if tier > 0:
                conds = ruleset.combat.conditions
                condition_id = conds.tier1[0].id if tier == 1 else conds.tier2[0].id
                result = combat.apply_condition(conditions, condition_id, tier, ruleset)
                if result.broken:
                    return exchange

            combat.end_exchange(conditions, ruleset)
            if exchange > 50:
                raise AssertionError("Broken never landed within 50 exchanges")

    def test_unarmored_breaks_at_exact_exchange(self, ruleset):
        assert self._exchange_broken(ruleset, None) == 2

    def test_light_breaks_at_exact_exchange(self, ruleset):
        assert self._exchange_broken(ruleset, "light") == 4

    def test_heavy_breaks_at_exact_exchange(self, ruleset):
        assert self._exchange_broken(ruleset, "heavy") == 6

    def test_heavy_strictly_outlasts_light_which_strictly_outlasts_none(self, ruleset):
        none = self._exchange_broken(ruleset, None)
        light = self._exchange_broken(ruleset, "light")
        heavy = self._exchange_broken(ruleset, "heavy")
        assert heavy > light > none
        assert light <= 2 * none  # G2 pass condition, DESIGN §5


# ---------------------------------------------------------------------------
# apply_condition()
# ---------------------------------------------------------------------------

class TestApplyCondition:
    def test_happy_path_appends_condition(self, ruleset):
        conditions: list[str] = []
        result = combat.apply_condition(conditions, "winded", 1, ruleset)
        assert result.applied is True
        assert result.broken is False
        assert conditions == ["winded"]

    def test_same_tier2_twice_escalates_to_broken(self, ruleset):
        conditions: list[str] = []
        combat.apply_condition(conditions, "staggered", 2, ruleset)
        result = combat.apply_condition(conditions, "staggered", 2, ruleset)
        assert result.broken is True
        assert result.applied is False
        assert conditions == ["staggered"]  # not appended twice

    def test_different_tier2_conditions_do_not_escalate(self, ruleset):
        conditions: list[str] = []
        combat.apply_condition(conditions, "staggered", 2, ruleset)
        result = combat.apply_condition(conditions, "cornered", 2, ruleset)
        assert result.broken is False
        assert set(conditions) == {"staggered", "cornered"}

    def test_zero_end_absorb_applies_tier_unmodified(self, ruleset):
        """F5 retired (DESIGN §4.3): no special-casing for 0 Endurance —
        an Absorb at 0 Endurance takes the incoming tier as-is."""
        conditions: list[str] = []
        result = combat.apply_condition(conditions, "winded", 1, ruleset)
        assert result.tier == 1
        assert result.condition == "winded"
        assert conditions == ["winded"]


# ---------------------------------------------------------------------------
# end_exchange()
# ---------------------------------------------------------------------------

class TestEndExchange:
    def test_happy_path_clears_tier1(self, ruleset):
        conditions = ["winded", "off_balance"]
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == ["winded", "off_balance"]
        assert conditions == []

    def test_tier2_persists(self, ruleset):
        conditions = ["staggered", "winded"]
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == ["winded"]
        assert conditions == ["staggered"]

    def test_no_tier1_conditions_is_a_no_op(self, ruleset):
        conditions = ["staggered"]
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == []
        assert conditions == ["staggered"]

    def test_empty_conditions_list(self, ruleset):
        conditions: list[str] = []
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == []
        assert conditions == []


# ---------------------------------------------------------------------------
# resolve_strike()
# ---------------------------------------------------------------------------

class TestResolveStrike:
    def test_happy_path_full_success_maps_to_tier2(self, ruleset):
        random.seed(20)  # produces full_success at modifier 0, measured posture
        result = combat.resolve_strike(0, "measured", [], ruleset)
        assert result.outcome == "full_success"
        assert result.condition_tier == 2
        assert result.mook_removed is True

    def test_failure_maps_to_tier0_and_no_mook_removal(self, ruleset):
        random.seed(2)  # produces failure at modifier 0
        result = combat.resolve_strike(0, "measured", [], ruleset)
        assert result.outcome == "failure"
        assert result.condition_tier == 0
        assert result.mook_removed is False

    def test_staggered_condition_applies_minus_one_offense(self, ruleset):
        random.seed(1)
        baseline = combat.resolve_strike(0, "measured", [], ruleset)
        random.seed(1)
        staggered = combat.resolve_strike(0, "measured", ["staggered"], ruleset)
        assert staggered.total == baseline.total - 1

    def test_aggressive_posture_adds_offense_modifier(self, ruleset):
        random.seed(1)
        baseline = combat.resolve_strike(0, "measured", [], ruleset)
        random.seed(1)
        aggressive = combat.resolve_strike(0, "aggressive", [], ruleset)
        assert aggressive.total == baseline.total + 1

    def test_extra_dice_from_opts_are_applied(self, ruleset):
        random.seed(1)
        result = combat.resolve_strike(0, "measured", [], ruleset, combat.StrikeOptions(extra_dice=2))
        assert len(result.dice) == 2  # base 2d6, extras dropped


# ---------------------------------------------------------------------------
# resolve_reaction()
# ---------------------------------------------------------------------------

class TestResolveReaction:
    def test_happy_path_dodge_rolls_and_pays_cost(self, ruleset):
        random.seed(1)
        result = combat.resolve_reaction("dodge", 0, "measured", "Standard", ruleset)
        assert result.outcome in ("full_success", "partial_success", "failure")
        assert result.cost == 1

    def test_absorb_does_not_roll(self, ruleset):
        result = combat.resolve_reaction("absorb", 0, "measured", "Standard", ruleset)
        assert result.outcome is None
        assert result.dice == []
        assert result.cost == 0

    def test_aggressive_posture_raises_cost(self, ruleset):
        result = combat.resolve_reaction("parry", 0, "aggressive", "Standard", ruleset)
        assert result.cost == 2

    def test_withdrawn_reactions_are_free(self, ruleset):
        result = combat.resolve_reaction("parry", 0, "withdrawn", "Standard", ruleset)
        assert result.cost == 0

    def test_intercept_does_not_roll_but_costs_more(self, ruleset):
        result = combat.resolve_reaction("intercept", 0, "measured", "Standard", ruleset)
        assert result.outcome is None
        assert result.cost == 2


# ---------------------------------------------------------------------------
# Ruleset-lookup helpers
# ---------------------------------------------------------------------------

class TestConditionTier:
    def test_tier1_condition(self, ruleset):
        assert combat.condition_tier("winded", ruleset) == 1

    def test_tier2_condition(self, ruleset):
        assert combat.condition_tier("staggered", ruleset) == 2

    def test_tier3_condition(self, ruleset):
        assert combat.condition_tier("broken", ruleset) == 3

    def test_unknown_condition_returns_zero(self, ruleset):
        assert combat.condition_tier("nonexistent", ruleset) == 0


class TestReactionCost:
    def test_measured_is_base_cost(self, ruleset):
        assert combat.reaction_cost("dodge", "measured", ruleset) == 1

    def test_aggressive_adds_one(self, ruleset):
        assert combat.reaction_cost("dodge", "aggressive", ruleset) == 2

    def test_defensive_subtracts_one_floored_at_zero(self, ruleset):
        assert combat.reaction_cost("dodge", "defensive", ruleset) == 0

    def test_withdrawn_is_always_free_regardless_of_reaction(self, ruleset):
        assert combat.reaction_cost("intercept", "withdrawn", ruleset) == 0

    # K1 (BRIEF D8, adopted after Gate G3 — research/simulation_log.md
    # Series 8): Aggressive's surcharge applies to the first reaction of
    # the exchange only.
    def test_aggressive_first_reaction_pays_surcharge(self, ruleset):
        assert combat.reaction_cost("dodge", "aggressive", ruleset, is_first_reaction=True) == 2

    def test_aggressive_second_reaction_no_surcharge(self, ruleset):
        assert combat.reaction_cost("dodge", "aggressive", ruleset, is_first_reaction=False) == 1

    def test_is_first_reaction_defaults_to_true(self, ruleset):
        assert combat.reaction_cost("dodge", "aggressive", ruleset) == 2

    def test_measured_unaffected_by_is_first_reaction(self, ruleset):
        assert combat.reaction_cost("dodge", "measured", ruleset, is_first_reaction=False) == 1

    def test_defensive_unaffected_by_is_first_reaction(self, ruleset):
        assert combat.reaction_cost("dodge", "defensive", ruleset, is_first_reaction=False) == 0


class TestWithdrawnRecoveryAmount:
    def test_matches_ruleset_value(self, ruleset):
        assert combat.withdrawn_recovery_amount(ruleset) == 2

    def test_returns_int(self, ruleset):
        assert isinstance(combat.withdrawn_recovery_amount(ruleset), int)


class TestPostureOffenseModifier:
    def test_aggressive_is_plus_one(self, ruleset):
        assert combat.posture_offense_modifier("aggressive", ruleset) == 1

    def test_defensive_is_minus_one(self, ruleset):
        assert combat.posture_offense_modifier("defensive", ruleset) == -1

    def test_withdrawn_is_none_cannot_attack(self, ruleset):
        assert combat.posture_offense_modifier("withdrawn", ruleset) is None


# ---------------------------------------------------------------------------
# apply_resolve_damage() — D1 enemy Resolve depletion (A4)
# ---------------------------------------------------------------------------

class TestApplyResolveDamage:
    def test_full_success_depletes_two(self, ruleset):
        result = combat.apply_resolve_damage(5, "full_success", ruleset)
        assert result.depletion == 2
        assert result.resolve_current == 3
        assert result.defeated is False

    def test_partial_success_depletes_one(self, ruleset):
        result = combat.apply_resolve_damage(5, "partial_success", ruleset)
        assert result.depletion == 1
        assert result.resolve_current == 4

    def test_failure_depletes_zero(self, ruleset):
        result = combat.apply_resolve_damage(5, "failure", ruleset)
        assert result.depletion == 0
        assert result.resolve_current == 5

    def test_resolve_cannot_drop_below_zero(self, ruleset):
        result = combat.apply_resolve_damage(1, "full_success", ruleset)
        assert result.resolve_current == 0

    def test_zero_resolve_is_defeated(self, ruleset):
        result = combat.apply_resolve_damage(1, "full_success", ruleset)
        assert result.defeated is True

    def test_nonzero_resolve_is_not_defeated(self, ruleset):
        result = combat.apply_resolve_damage(5, "partial_success", ruleset)
        assert result.defeated is False

    def test_phase_change_fires_when_threshold_crossed(self, ruleset):
        # resolve 5 -> 3, threshold 2 not yet crossed
        first = combat.apply_resolve_damage(5, "full_success", ruleset, phase_thresholds=[2])
        assert first.phase_index is None
        # resolve 3 -> 1, threshold 2 crossed
        second = combat.apply_resolve_damage(3, "full_success", ruleset, phase_thresholds=[2])
        assert second.phase_index == 0

    def test_phase_change_fires_exactly_once(self, ruleset):
        # Already at/under threshold before this hit -> no re-fire.
        result = combat.apply_resolve_damage(1, "full_success", ruleset, phase_thresholds=[2])
        assert result.phase_index is None

    def test_no_phase_thresholds_is_a_no_op(self, ruleset):
        result = combat.apply_resolve_damage(5, "full_success", ruleset)
        assert result.phase_index is None

    def test_landing_exactly_on_threshold_fires_the_phase(self, ruleset):
        """A14/F4: a depletion that lands Resolve *exactly on* a threshold
        (resolve_after == threshold) still fires that phase — the crossing
        rule is `before > threshold >= after`."""
        result = combat.apply_resolve_damage(4, "full_success", ruleset, phase_thresholds=[2])
        assert result.resolve_current == 2
        assert result.phase_index == 0

    def test_landing_exactly_on_threshold_fires_exactly_once(self, ruleset):
        """A14/F4: once Resolve has landed on the threshold, a further
        depletion below it must NOT re-fire the same phase — routing every
        change through phase_crossed keeps 'fires exactly once' an invariant,
        never a raw re-decrement that could double-fire."""
        landed = combat.apply_resolve_damage(4, "full_success", ruleset, phase_thresholds=[2])
        assert landed.phase_index == 0
        # From exactly-on-threshold (2) down to 0: no re-fire.
        below = combat.apply_resolve_damage(landed.resolve_current, "full_success",
                                            ruleset, phase_thresholds=[2])
        assert below.resolve_current == 0
        assert below.phase_index is None


# ---------------------------------------------------------------------------
# enemy_armor_resolve_bonus() — D1 flat Resolve from armor (A8)
# ---------------------------------------------------------------------------

class TestEnemyArmorResolveBonus:
    def test_no_armor_grants_nothing(self, ruleset):
        assert combat.enemy_armor_resolve_bonus("none", ruleset) == 0

    def test_light_armor_grants_one(self, ruleset):
        assert combat.enemy_armor_resolve_bonus("light", ruleset) == 1

    def test_heavy_armor_grants_two(self, ruleset):
        assert combat.enemy_armor_resolve_bonus("heavy", ruleset) == 2

    def test_none_armor_string_grants_nothing(self, ruleset):
        assert combat.enemy_armor_resolve_bonus(None, ruleset) == 0


# ---------------------------------------------------------------------------
# mook_removed() — D1 Mook removal thresholds (A4)
# ---------------------------------------------------------------------------

class TestMookRemoved:
    def test_unarmored_mook_removed_on_partial_success(self, ruleset):
        assert combat.mook_removed("partial_success", armored=False, ruleset=ruleset) is True

    def test_unarmored_mook_removed_on_full_success(self, ruleset):
        assert combat.mook_removed("full_success", armored=False, ruleset=ruleset) is True

    def test_unarmored_mook_survives_failure(self, ruleset):
        assert combat.mook_removed("failure", armored=False, ruleset=ruleset) is False

    def test_armored_mook_survives_partial_success(self, ruleset):
        assert combat.mook_removed("partial_success", armored=True, ruleset=ruleset) is False

    def test_armored_mook_removed_on_full_success(self, ruleset):
        assert combat.mook_removed("full_success", armored=True, ruleset=ruleset) is True

    def test_armored_mook_survives_failure(self, ruleset):
        assert combat.mook_removed("failure", armored=True, ruleset=ruleset) is False


# ---------------------------------------------------------------------------
# apply_condition(is_rider=True) — D1 enemy Conditions as riders (A4)
# ---------------------------------------------------------------------------

class TestApplyConditionRider:
    def test_rider_applies_like_a_normal_condition(self, ruleset):
        conditions: list[str] = []
        result = combat.apply_condition(conditions, "staggered", 2, ruleset, is_rider=True)
        assert result.applied is True
        assert conditions == ["staggered"]

    def test_rider_never_escalates_to_broken(self, ruleset):
        conditions: list[str] = ["staggered"]
        result = combat.apply_condition(conditions, "staggered", 2, ruleset, is_rider=True)
        assert result.broken is False
        assert result.applied is True

    def test_tier1_rider_clears_at_end_exchange(self, ruleset):
        conditions: list[str] = []
        combat.apply_condition(conditions, "winded", 1, ruleset, is_rider=True)
        assert combat.target_strike_difficulty("Standard", conditions, ruleset) == "Standard"
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == ["winded"]
        assert conditions == []

    def test_tier2_rider_persists_past_end_exchange(self, ruleset):
        conditions: list[str] = ["cornered"]
        cleared = combat.end_exchange(conditions, ruleset)
        assert cleared == []
        assert conditions == ["cornered"]


# ---------------------------------------------------------------------------
# target_strike_difficulty() — D1 Tier 2 rider -> Easy (A4)
# ---------------------------------------------------------------------------

class TestTargetStrikeDifficulty:
    def test_no_conditions_keeps_base_difficulty(self, ruleset):
        assert combat.target_strike_difficulty("Standard", [], ruleset) == "Standard"

    def test_tier1_condition_keeps_base_difficulty(self, ruleset):
        assert combat.target_strike_difficulty("Standard", ["winded"], ruleset) == "Standard"

    def test_tier2_rider_forces_easy(self, ruleset):
        assert combat.target_strike_difficulty("Standard", ["staggered"], ruleset) == "Easy"

    def test_tier2_rider_overrides_hard_base(self, ruleset):
        assert combat.target_strike_difficulty("Hard", ["cornered"], ruleset) == "Easy"

    def test_easy_flows_through_resolve_strike_as_a_bonus(self, ruleset):
        random.seed(1)
        baseline = combat.resolve_strike(0, "measured", [], ruleset)
        random.seed(1)
        difficulty = combat.target_strike_difficulty("Standard", ["staggered"], ruleset)
        eased = combat.resolve_strike(
            0, "measured", [], ruleset, combat.StrikeOptions(difficulty=difficulty)
        )
        assert eased.total == baseline.total + 1


# ---------------------------------------------------------------------------
# offense_modifier() — posture + Condition penalties, shared by both callers
#
# The Staggered −1 ("−1 to offensive rolls", PHB III.3) previously lived as a
# literal inside resolve_strike, which no production code path calls — so it
# was simulated but never applied at a real table. These pin it to the
# ruleset and to the one helper both callers now use.
# ---------------------------------------------------------------------------

class TestOffenseModifier:
    def test_measured_with_no_conditions_is_zero(self, ruleset):
        assert combat.offense_modifier("measured", [], ruleset) == 0

    def test_aggressive_posture_is_plus_one(self, ruleset):
        assert combat.offense_modifier("aggressive", [], ruleset) == 1

    def test_staggered_applies_minus_one(self, ruleset):
        assert combat.offense_modifier("measured", ["staggered"], ruleset) == -1

    def test_staggered_and_posture_combine(self, ruleset):
        assert combat.offense_modifier("aggressive", ["staggered"], ruleset) == 0
        assert combat.offense_modifier("defensive", ["staggered"], ruleset) == -2

    def test_tier1_conditions_carry_no_offense_penalty(self, ruleset):
        assert combat.offense_modifier("measured", ["winded"], ruleset) == 0

    def test_withdrawn_cannot_attack(self, ruleset):
        assert combat.offense_modifier("withdrawn", [], ruleset) is None

    def test_penalty_is_read_from_the_ruleset_not_hardcoded(self, ruleset):
        staggered = next(
            c for c in ruleset.combat.conditions.tier2 if c.id == "staggered"
        )
        assert combat.offense_modifier("measured", ["staggered"], ruleset) == (
            staggered.offense_modifier
        )

    def test_unknown_condition_is_ignored(self, ruleset):
        assert combat.offense_modifier("measured", ["nonsense"], ruleset) == 0


# ---------------------------------------------------------------------------
# resolve_incoming_condition() — armor/reaction non-stacking (PHB III.3)
#
# "Armor downgrades and successful reaction downgrades do not stack. Apply the
# greater reduction only." Both reduce by one tier, so a partial reaction and
# armor together still land one tier down — and the armor charge is NOT spent,
# because armor softened nothing that the reaction had not already softened.
# ---------------------------------------------------------------------------

class TestResolveIncomingCondition:
    def test_unarmored_no_reaction_passes_tier_through(self, ruleset):
        result = combat.resolve_incoming_condition(2, None, 0, ruleset)
        assert result.tier == 2
        assert result.downgrades_remaining == 0
        assert result.armor_spent is False

    def test_armor_alone_downgrades_and_spends_a_charge(self, ruleset):
        result = combat.resolve_incoming_condition(2, "light", 2, ruleset)
        assert result.tier == 1
        assert result.downgrades_remaining == 1
        assert result.armor_spent is True

    def test_reaction_alone_downgrades_without_armor(self, ruleset):
        result = combat.resolve_incoming_condition(
            2, None, 0, ruleset, reaction_downgraded=True,
        )
        assert result.tier == 1
        assert result.armor_spent is False

    def test_armor_and_reaction_do_not_stack(self, ruleset):
        """PHB III.3: light armor + partial Parry vs Tier 2 lands as Tier 1,
        not negated entirely."""
        result = combat.resolve_incoming_condition(
            2, "light", 2, ruleset, reaction_downgraded=True,
        )
        assert result.tier == 1

    def test_redundant_armor_charge_is_not_spent(self, ruleset):
        """The reaction already applied the greater (equal) reduction, so the
        per-scene budget that keeps armored PCs breakable is left intact."""
        result = combat.resolve_incoming_condition(
            2, "light", 2, ruleset, reaction_downgraded=True,
        )
        assert result.downgrades_remaining == 2
        assert result.armor_spent is False

    def test_reaction_negates_tier1_without_spending_armor(self, ruleset):
        result = combat.resolve_incoming_condition(
            1, "light", 2, ruleset, reaction_downgraded=True,
        )
        assert result.tier == 0
        assert result.downgrades_remaining == 2

    def test_exhausted_budget_lets_condition_through_at_full_tier(self, ruleset):
        result = combat.resolve_incoming_condition(2, "light", 0, ruleset)
        assert result.tier == 2
        assert result.armor_spent is False

    def test_heavy_armor_uses_its_own_budget(self, ruleset):
        result = combat.resolve_incoming_condition(2, "heavy", 4, ruleset)
        assert result.tier == 1
        assert result.downgrades_remaining == 3

    def test_armor_fully_absorbs_tier1(self, ruleset):
        result = combat.resolve_incoming_condition(1, "light", 2, ruleset)
        assert result.tier == 0
        assert result.armor_spent is True
