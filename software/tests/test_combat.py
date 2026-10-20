"""Tests for `app/game/combat.py` — the shared, pure combat-rules module."""
import random
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.facets.registry import build_ruleset
from app.facets.schema import StepTriggerDef, TechniqueDef
from app.game import combat


@pytest.fixture(scope="module")
def ruleset():
    return build_ruleset([])


class _TagBearer:
    """Minimal stand-in for anything carrying end-of-exchange combat tags.

    `expire_end_of_exchange` is duck-typed on purpose: the app's `Enemy`
    (pydantic) and the simulator's `EnemyState` (dataclass) are different
    types that carry the same tags, and the rule must not be written twice
    to serve both.
    """

    def __init__(self, **tags):
        for k, v in tags.items():
            setattr(self, k, v)


def _with_open_clears(base, mode: str):
    """A copy of `base` whose Open lifecycle is `mode`. Both modes are legal
    data (schema `EnemyDurabilityDef.open_clears`), so a test may pin either."""
    import copy
    rs = copy.deepcopy(base)
    rs.combat.enemy_durability.open_clears = mode
    return rs


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

    # L-4 (docs/RESEARCH_completeness_audit.md): Defensive's "-1 Endurance
    # cost per reaction (min 0)" floor is an explicit yaml field
    # (postures.defensive.min_reaction_cost), not a hardcoded literal.
    def test_defensive_floor_reads_from_yaml_not_a_literal(self, ruleset):
        original = ruleset.combat.postures["defensive"].get("min_reaction_cost", 0)
        try:
            ruleset.combat.postures["defensive"]["min_reaction_cost"] = 3
            assert combat.reaction_cost("dodge", "defensive", ruleset) == 3
        finally:
            ruleset.combat.postures["defensive"]["min_reaction_cost"] = original


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
# apply_final_blow_removal() — B4 Q3, TD-13: *The Final Blow* is a licensed
# override, resolved as a defeat event through the canonical defeat path,
# never a raw `resolve_current = 0` write.
# ---------------------------------------------------------------------------

class TestApplyFinalBlowRemoval:
    def test_removal_produces_a_defeat_event(self, ruleset):
        """Works on any target, Bosses included — the removal does not care
        how much Resolve remained."""
        result = combat.apply_final_blow_removal(8)
        assert result.resolve_current == 0
        assert result.defeated is True
        assert result.depletion == 8

    def test_removal_routes_through_phase_crossed(self, ruleset):
        """The drop to 0 must be detected by the same `phase_crossed`
        primitive `apply_resolve_damage` uses — a Boss phase sitting between
        the target's current Resolve and 0 must still fire, exactly as it
        would from an ordinary Strike that happened to zero the pool."""
        result = combat.apply_final_blow_removal(8, phase_thresholds=[2])
        assert result.phase_index == 0

        # Already at/under every threshold: no re-fire, same "fires exactly
        # once" invariant apply_resolve_damage's phase tests pin.
        already_low = combat.apply_final_blow_removal(1, phase_thresholds=[2])
        assert already_low.phase_index is None

    def test_transcript_entry_is_distinguishable_from_a_resolve_zero_defeat(self, ruleset):
        """A Final Blow removal must be tellable apart from an ordinary
        Strike that happened to deplete Resolve to exactly 0 — both by
        result *type* (a future sim series can `isinstance`-branch) and by
        the `cause` field a transcript/broadcast can log directly."""
        ordinary_defeat = combat.apply_resolve_damage(2, "full_success", ruleset)
        final_blow = combat.apply_final_blow_removal(2)

        assert ordinary_defeat.resolve_current == 0
        assert ordinary_defeat.defeated is True
        assert final_blow.resolve_current == 0
        assert final_blow.defeated is True

        # Same surface-level outcome; different type and a distinguishing cause.
        assert not isinstance(ordinary_defeat, combat.FinalBlowResult)
        assert isinstance(final_blow, combat.FinalBlowResult)
        assert not hasattr(ordinary_defeat, "cause")
        assert final_blow.cause == "final_blow"

    def test_no_raw_resolve_current_zero_write_in_source(self):
        """Guards the P11 invariant at the source level: nowhere in
        `apply_final_blow_removal` may `resolve_current` be assigned `0`
        directly outside of building the `FinalBlowResult` via
        `phase_crossed` — the function must route the crossing check
        through `phase_crossed`, matching `apply_resolve_damage`'s shape,
        rather than a bare `resolve_current = 0` that would skip it."""
        import inspect

        source = inspect.getsource(combat.apply_final_blow_removal)
        assert "phase_crossed(" in source, (
            "apply_final_blow_removal must route through phase_crossed"
        )
        assert "resolve_current = 0" not in source.replace(" ", ""), (
            "found a raw `resolve_current = 0` write — must route through "
            "phase_crossed like apply_resolve_damage does"
        )


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
# enemy_incoming_condition_tier() / enemy_posture_reaction_difficulty() —
# sync-M-6: III.3 Enemy Attacks (incoming tier by enemy type, Posture shifts
# PC reaction difficulty, Mooks never declare Posture).
# ---------------------------------------------------------------------------

class TestEnemyIncomingConditionTier:
    def test_mook_incoming_tier_from_yaml(self, ruleset):
        assert combat.enemy_incoming_condition_tier("mook", ruleset) == 1

    def test_named_incoming_tier_from_yaml(self, ruleset):
        assert combat.enemy_incoming_condition_tier("named", ruleset) == 2

    def test_boss_incoming_tier_from_yaml(self, ruleset):
        assert combat.enemy_incoming_condition_tier("boss", ruleset) == 2

    def test_modified_yaml_tier_changes_the_result(self, ruleset):
        original = ruleset.combat.enemy_attacks.incoming_tier.named
        try:
            ruleset.combat.enemy_attacks.incoming_tier.named = 3
            assert combat.enemy_incoming_condition_tier("named", ruleset) == 3
        finally:
            ruleset.combat.enemy_attacks.incoming_tier.named = original


class TestEnemyPostureReactionDifficulty:
    def test_aggressive_named_shifts_one_step_harder(self, ruleset):
        result = combat.enemy_posture_reaction_difficulty("Standard", "named", "aggressive", ruleset)
        assert result == "Hard"

    def test_defensive_boss_shifts_one_step_easier(self, ruleset):
        result = combat.enemy_posture_reaction_difficulty("Standard", "boss", "defensive", ruleset)
        assert result == "Easy"

    def test_measured_named_is_unchanged(self, ruleset):
        result = combat.enemy_posture_reaction_difficulty("Standard", "named", "measured", ruleset)
        assert result == "Standard"

    def test_mook_posture_is_ignored_even_if_aggressive(self, ruleset):
        """Mooks do not declare Postures (III.3) — passing one anyway must
        not shift the difficulty; the MM sets Mook difficulty by situation."""
        result = combat.enemy_posture_reaction_difficulty("Standard", "mook", "aggressive", ruleset)
        assert result == "Standard"


# ---------------------------------------------------------------------------
# maneuver_target_difficulty() / support_bonus_modes() — sync-M-7: III.3
# Maneuver (10+/7-9/6- effect on rolls against the target) and Support (the
# two non-stacking next-roll-only bonus modes).
# ---------------------------------------------------------------------------

class TestManeuverTargetDifficulty:
    def test_full_success_makes_target_easy(self, ruleset):
        assert combat.maneuver_target_difficulty("full_success", "Standard", ruleset) == "Easy"

    def test_partial_success_leaves_base_difficulty(self, ruleset):
        assert combat.maneuver_target_difficulty("partial_success", "Standard", ruleset) == "Standard"

    def test_failure_backfires_no_effect_on_target(self, ruleset):
        assert combat.maneuver_target_difficulty("failure", "Standard", ruleset) == "Standard"

    def test_modified_yaml_outcome_changes_the_effect(self, ruleset):
        original = ruleset.combat.actions.maneuver.partial_success
        try:
            ruleset.combat.actions.maneuver.partial_success = "easy"
            assert combat.maneuver_target_difficulty("partial_success", "Standard", ruleset) == "Easy"
        finally:
            ruleset.combat.actions.maneuver.partial_success = original


class TestSupportBonusModes:
    def test_support_has_exactly_two_modes_from_yaml(self, ruleset):
        assert combat.support_bonus_modes(ruleset) == ["add_die", "ease_difficulty"]

    def test_modified_yaml_modes_changes_accepted_set(self, ruleset):
        original = ruleset.combat.actions.support.modes
        try:
            ruleset.combat.actions.support.modes = ["add_die"]
            assert combat.support_bonus_modes(ruleset) == ["add_die"]
        finally:
            ruleset.combat.actions.support.modes = original

    def test_support_is_next_roll_only_and_non_stacking_per_yaml(self, ruleset):
        """The duration and non-stacking rule ('only the most recent
        applies') are encoded as data. No live 'pending bonus' tracking
        exists in the session yet to test the replacement behaviorally —
        see the LOG for this task; that's a larger feature than moving a
        literal into data."""
        assert ruleset.combat.actions.support.duration == "next_roll_only"
        assert ruleset.combat.actions.support.stacking == "most_recent_only"


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
# The Open tag — K-6/D4: on a 10+ vs an enemy, the attacker may leave it
# Open (Easy to Strike for everyone) instead of the retired five-option
# rider-Condition menu. PvP Strike outcomes are unchanged.
# ---------------------------------------------------------------------------

class TestOpenTag:
    def test_open_on_full_success_only(self, ruleset):
        assert combat.can_apply_open("full_success", ruleset) is True
        assert combat.can_apply_open("partial_success", ruleset) is False
        assert combat.can_apply_open("failure", ruleset) is False

    def test_modified_yaml_open_outcome_changes_eligibility(self, ruleset):
        # `ruleset` is session-scoped (shared across the whole test run) —
        # restore the original value so this mutation doesn't leak into
        # other tests.
        original = ruleset.combat.enemy_durability.open_on
        try:
            ruleset.combat.enemy_durability.open_on = "partial_success"
            assert combat.can_apply_open("partial_success", ruleset) is True
            assert combat.can_apply_open("full_success", ruleset) is False
        finally:
            ruleset.combat.enemy_durability.open_on = original

    def test_open_target_is_easy_for_everyone(self, ruleset):
        """Easy to Strike for everyone — not just the attacker who opened it."""
        assert combat.target_strike_difficulty("Standard", True, ruleset) == "Easy"
        assert combat.target_strike_difficulty("Hard", True, ruleset) == "Easy"
        assert combat.target_strike_difficulty("Very Hard", True, ruleset) == "Easy"

    def test_not_open_keeps_base_difficulty(self, ruleset):
        assert combat.target_strike_difficulty("Standard", False, ruleset) == "Standard"
        assert combat.target_strike_difficulty("Hard", False, ruleset) == "Hard"

    def test_open_composes_through_the_difficulty_pipeline(self, ruleset):
        """Open is an Easy-tag source in compose_difficulty's precedence
        (III.1 step 2) — target_strike_difficulty must agree with the
        pipeline, not carry its own copy of the override."""
        expected, _ = combat.compose_difficulty("Hard", ruleset=ruleset, easy_tag=True)
        assert combat.target_strike_difficulty("Hard", True, ruleset) == expected

    def test_base_ruleset_expires_open_at_end_of_exchange(self, ruleset):
        """R2/D20. The base ruleset's choice; `enemy_action` stays a legal
        value a setting may take (schema `EnemyDurabilityDef.open_clears`)."""
        assert combat.open_clear_mode(ruleset) == "end_of_exchange"

    def test_open_never_reduces_resolve(self, ruleset):
        """Open is a tag, not damage — the 10+'s Resolve depletion comes
        from the Strike itself; leaving the enemy Open adds none."""
        damage = combat.apply_resolve_damage(5, "full_success", ruleset)
        assert damage.resolve_current == 3
        assert combat.can_apply_open("full_success", ruleset) is True
        # Applying Open is a state flag on the enemy; nothing here touches Resolve.
        assert damage.resolve_current == 3

    # -- R2: Open expires with the Tier 1 Conditions --------------------
    # BRIEF_fun_second_act §2. The lifecycle is data
    # (`combat.enemy_durability.open_clears`), so these tests pin both
    # modes rather than the one the base ruleset happens to carry.

    def test_open_clears_at_end_of_exchange_reads_the_mode(self, ruleset):
        assert combat.open_clears_at_end_of_exchange(ruleset) is True
        assert combat.open_clears_at_end_of_exchange(
            _with_open_clears(ruleset, "enemy_action")) is False

    def test_expire_clears_open_under_end_of_exchange(self, ruleset):
        enemy = _TagBearer(open=True)
        assert combat.expire_end_of_exchange(enemy, ruleset) == ["open"]
        assert enemy.open is False

    def test_expire_leaves_open_standing_under_enemy_action(self, ruleset):
        """The pre-R2 rule stays reachable: under `enemy_action` nothing but
        the enemy's own spent action takes the tag off, and end of exchange
        must not do it behind the mode's back."""
        enemy = _TagBearer(open=True)
        rs = _with_open_clears(ruleset, "enemy_action")
        assert combat.expire_end_of_exchange(enemy, rs) == []
        assert enemy.open is True

    def test_expire_reports_nothing_when_no_tag_is_set(self, ruleset):
        enemy = _TagBearer(open=False)
        assert combat.expire_end_of_exchange(enemy, ruleset) == []

    def test_the_tier_condition_rider_menu_stays_retired(self):
        """WS-3/T3.4 killed the *Tier-Condition* rider menu vs enemies (a
        10+ hanging 'staggered' or 'cornered' on a Named). R3's rider menu
        is a different animal — three tempo options, no Conditions — so the
        old names must stay dead even though `apply_rider` now exists."""
        assert not hasattr(combat, "can_apply_rider")
        assert not hasattr(combat, "rider_tier_eligible")

    def test_easy_flows_through_resolve_strike_as_a_bonus(self, ruleset):
        random.seed(1)
        baseline = combat.resolve_strike(0, "measured", [], ruleset)
        random.seed(1)
        difficulty = combat.target_strike_difficulty("Standard", True, ruleset)
        eased = combat.resolve_strike(
            0, "measured", [], ruleset, combat.StrikeOptions(difficulty=difficulty)
        )
        assert eased.total == baseline.total + 1


class TestWithdrawnRecoveryCap:
    """D5: Withdrawn recovers 2 Endurance, up to your pool — the clamp is
    a rule and lives here, not re-derived by each caller."""

    def test_recovery_clamps_at_pool(self, ruleset):
        assert combat.apply_withdrawn_recovery(4, 5, ruleset) == 5

    def test_recovery_full_amount_below_cap(self, ruleset):
        assert combat.apply_withdrawn_recovery(1, 5, ruleset) == 3

    def test_recovery_at_pool_stays_at_pool(self, ruleset):
        assert combat.apply_withdrawn_recovery(5, 5, ruleset) == 5

    def test_recovery_amount_read_from_ruleset(self, ruleset):
        original = ruleset.combat.endurance.recovery_withdrawn
        try:
            ruleset.combat.endurance.recovery_withdrawn = 3
            assert combat.apply_withdrawn_recovery(1, 8, ruleset) == 4
        finally:
            ruleset.combat.endurance.recovery_withdrawn = original


class TestUncontestedExchange:
    """K-2/D5: an exchange in which no PC took an offensive action lets the
    situation advance for free — the MM may reposition, reinforce,
    progress a clock, or take the objective, no roll."""

    def test_no_participants_is_uncontested(self, ruleset):
        assert combat.exchange_uncontested([]) is True

    def test_all_defensive_is_uncontested(self, ruleset):
        assert combat.exchange_uncontested([False, False, False]) is True

    def test_single_offensive_action_contests(self, ruleset):
        assert combat.exchange_uncontested([False, True, False]) is False


class TestPvPOutcomesUnchanged:
    """K-6 scope guard: the Open merge touches only the enemy-target path.
    PC-vs-PC Strikes keep the tier outcomes (10+ = Tier 2, 7-9 = Tier 1)
    and the same-type-Tier-2 escalation to Broken."""

    def test_pvp_strike_outcome_tiers_unchanged(self, ruleset):
        assert combat._strike_outcome_tier("full_success", ruleset) == 2
        assert combat._strike_outcome_tier("partial_success", ruleset) == 1
        assert combat._strike_outcome_tier("failure", ruleset) == 0

    def test_pvp_second_tier2_same_type_still_escalates_to_broken(self, ruleset):
        conditions = ["staggered"]
        result = combat.apply_condition(conditions, "staggered", 2, ruleset)
        assert result.broken is True
        assert result.applied is False

    def test_apply_condition_has_no_rider_flag(self, ruleset):
        """`is_rider` retired with the menu — enemies no longer take Strike
        Conditions, so the flag has nothing left to mark."""
        with pytest.raises(TypeError):
            combat.apply_condition([], "staggered", 2, ruleset, is_rider=True)


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

    def test_reaction_downgrade_amount_reads_from_yaml(self, ruleset):
        """sync-M-5: the reaction's tier reduction was a hardcoded `tier - 1`
        in resolve_incoming_condition; it now reads
        combat.armor.reaction_downgrade_tiers. `ruleset` is session-scoped
        (shared across the test run) — restore the original value."""
        original = ruleset.combat.armor.reaction_downgrade_tiers
        try:
            ruleset.combat.armor.reaction_downgrade_tiers = 2
            result = combat.resolve_incoming_condition(
                2, None, 0, ruleset, reaction_downgraded=True,
            )
            assert result.tier == 0  # 2 - 2, not the old hardcoded 2 - 1
        finally:
            ruleset.combat.armor.reaction_downgrade_tiers = original

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


# ---------------------------------------------------------------------------
# apply_character_difficulty_step() — TD-5, B4 Q1's composition mechanism
# (DESIGN_technique_difficulty.md §2.2, §5)
#
# Tests inject synthetic TechniqueDef instances via a thin ruleset wrapper so
# this rule is pinned independently of TD-6's real facet.yaml metadata —
# TD-5 is sequenced before TD-6 precisely so the mechanism is proven first.
# ---------------------------------------------------------------------------

class _FakeRulesetWithTechniques:
    """Wraps a real `MergedRuleset` but overrides `get_technique()` with a
    caller-supplied map, so composition tests do not depend on which real
    Techniques (if any) carry `difficulty_step` metadata."""

    def __init__(self, base_ruleset, techniques: dict):
        self._base = base_ruleset
        self._techniques = techniques

    def __getattr__(self, name):
        return getattr(self._base, name)

    def get_technique(self, technique_id):
        return self._techniques.get(technique_id)


def _character(techniques=None, technique_choices=None):
    return SimpleNamespace(
        techniques=techniques or [], technique_choices=technique_choices or {},
    )


def _auto_step_technique(tech_id, *, match, against, step="easier"):
    return TechniqueDef(
        id=tech_id, name=tech_id, description=".",
        difficulty_step=step,
        step_trigger=StepTriggerDef(kind="auto", match=match, against=against),
    )


def _declared_step_technique(tech_id, *, step="easier"):
    return TechniqueDef(
        id=tech_id, name=tech_id, description=".",
        difficulty_step=step,
        step_trigger=StepTriggerDef(kind="declared"),
    )


class TestApplyCharacterDifficultyStep:
    def test_clamping_from_easy_stays_easy(self, ruleset):
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(techniques=["weapon_mastery"])
        context = {"weapon_category": "blades"}

        label, applied = combat.apply_character_difficulty_step(
            "Easy", character, context, fake,
        )
        assert label == "Easy"
        assert applied == "weapon_mastery"

    def test_hard_plus_step_yields_standard_not_easy(self, ruleset):
        """Proves the step composes with the MM's call rather than
        replacing it — DESIGN §5.4."""
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(techniques=["weapon_mastery"])
        context = {"weapon_category": "blades"}

        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, context, fake,
        )
        assert label == "Standard"
        assert applied == "weapon_mastery"

    def test_two_qualifying_techniques_yield_one_step_deterministic_id(self, ruleset):
        """The guardrail: at most one character-side step per roll. Two
        auto Techniques both qualify; only one step is applied, and the
        reported id is the lower of the two regardless of unlock order."""
        tech_a = _auto_step_technique("acclimated", match="hazard_type", against="cold")
        tech_b = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"acclimated": tech_a, "weapon_mastery": tech_b})
        character = _character(techniques=["weapon_mastery", "acclimated"])
        context = {"hazard_type": "cold", "weapon_category": "blades"}

        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, context, fake,
        )
        assert label == "Standard"  # only one step, not two
        assert applied == "acclimated"  # lowest technique id wins between two autos

    def test_unlocked_only_technique_not_in_characters_list_does_not_fire(self, ruleset):
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(techniques=[])  # not unlocked
        context = {"weapon_category": "blades"}

        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, context, fake,
        )
        assert label == "Hard"
        assert applied is None

    def test_absent_context_field_does_not_fire(self, ruleset):
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(techniques=["weapon_mastery"])
        context = {}  # weapon_category absent entirely

        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, context, fake,
        )
        assert label == "Standard"
        assert applied is None

    def test_mismatched_choice_does_not_fire(self, ruleset):
        """`against == "choice"` compares the roll context against the
        character's recorded `technique_choices` for that Technique —
        Weapon Mastery (blades) does not fire on an unarmed Strike."""
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="choice")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(
            techniques=["weapon_mastery"],
            technique_choices={"weapon_mastery": "blades"},
        )
        context = {"weapon_category": "unarmed"}

        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, context, fake,
        )
        assert label == "Standard"
        assert applied is None

    def test_matched_choice_fires(self, ruleset):
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="choice")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = _character(
            techniques=["weapon_mastery"],
            technique_choices={"weapon_mastery": "blades"},
        )
        context = {"weapon_category": "blades"}

        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, context, fake,
        )
        assert label == "Easy"
        assert applied == "weapon_mastery"

    def test_declared_beats_auto(self, ruleset):
        """A player-declared toggle wins precedence over a qualifying auto
        Technique, even when the auto Technique's id sorts lower."""
        declared = _declared_step_technique("zzz_the_uncanny_angle")
        auto = _auto_step_technique("aaa_weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(
            ruleset, {"zzz_the_uncanny_angle": declared, "aaa_weapon_mastery": auto},
        )
        character = _character(techniques=["aaa_weapon_mastery", "zzz_the_uncanny_angle"])
        context = {
            "weapon_category": "blades",
            "declared_technique_ids": ["zzz_the_uncanny_angle"],
        }

        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, context, fake,
        )
        assert label == "Standard"
        assert applied == "zzz_the_uncanny_angle"

    def test_declared_technique_not_toggled_does_not_fire(self, ruleset):
        tech = _declared_step_technique("the_uncanny_angle")
        fake = _FakeRulesetWithTechniques(ruleset, {"the_uncanny_angle": tech})
        character = _character(techniques=["the_uncanny_angle"])
        context = {}  # not declared this roll

        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, context, fake,
        )
        assert label == "Standard"
        assert applied is None

    def test_no_qualifying_technique_leaves_label_unchanged(self, ruleset):
        character = _character(techniques=[])
        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, {}, ruleset,
        )
        assert label == "Standard"
        assert applied is None

    def test_technique_without_step_metadata_never_fires(self, ruleset):
        """A Technique the character has unlocked but which carries no
        `difficulty_step`/`step_trigger` (the overwhelming majority) is
        silently skipped rather than raising."""
        plain = TechniqueDef(id="forcing_hand", name="Forcing Hand", description=".")
        fake = _FakeRulesetWithTechniques(ruleset, {"forcing_hand": plain})
        character = _character(techniques=["forcing_hand"])

        label, applied = combat.apply_character_difficulty_step(
            "Standard", character, {"weapon_category": "blades"}, fake,
        )
        assert label == "Standard"
        assert applied is None


class TestDifficultyPrecedence:
    """T2.4 (C-3/C-4/K-8, D2): III.1's printed precedence, in one place —
    base from the situation → Easy-tag override (downward, non-stacking) →
    at most ONE character-side step (Technique OR Specialty, one pool) →
    Support's step → ladder clamps at both ends."""

    def _char(self, techniques=None, technique_choices=None, specialty=None):
        return SimpleNamespace(
            techniques=techniques or [],
            technique_choices=technique_choices or {},
            specialty=specialty,
        )

    def test_easy_tag_overrides_base_downward(self, ruleset):
        label, _ = combat.compose_difficulty(
            "Very Hard", ruleset=ruleset, easy_tag=True,
        )
        assert label == "Easy"

    def test_easy_tag_does_not_stack_below_the_floor(self, ruleset):
        """A rider Condition and a Maneuver both tagging the target Easy is
        still just Easy — and a character step on top of the tag is absorbed
        by the ladder floor, not banked."""
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = self._char(techniques=["weapon_mastery"])
        label, _ = combat.compose_difficulty(
            "Hard", character, {"weapon_category": "blades"}, fake, easy_tag=True,
        )
        assert label == "Easy"

    def test_specialty_alone_is_a_character_side_step(self, ruleset):
        character = self._char(specialty="Knows how cargo manifests get falsified")
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, {"specialty_declared": True}, ruleset,
        )
        assert label == "Standard"
        assert applied == "specialty"

    def test_specialty_without_declaration_does_not_fire(self, ruleset):
        character = self._char(specialty="Knows how cargo manifests get falsified")
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, {}, ruleset,
        )
        assert label == "Hard"
        assert applied is None

    def test_declared_specialty_on_specialtyless_character_does_not_fire(self, ruleset):
        character = self._char(specialty=None)
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, {"specialty_declared": True}, ruleset,
        )
        assert label == "Hard"
        assert applied is None

    def test_technique_and_specialty_share_one_step(self, ruleset):
        """C-4: two character-side sources → one step. A Hard roll reaches
        Standard via either source, never Easy via both."""
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = self._char(
            techniques=["weapon_mastery"],
            specialty="Reads an opponent's style in the first exchange",
        )
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character,
            {"weapon_category": "blades", "specialty_declared": True},
            fake,
        )
        assert label == "Standard"  # one step, not two
        assert applied == "specialty"  # the player's pick beats the auto step

    def test_support_step_applies_after_the_character_step(self, ruleset):
        """Support is party-side, not character-side — its step lands on top
        of the single character step: Hard → Standard (Technique) → Easy."""
        tech = _auto_step_technique("weapon_mastery", match="weapon_category", against="blades")
        fake = _FakeRulesetWithTechniques(ruleset, {"weapon_mastery": tech})
        character = self._char(techniques=["weapon_mastery"])
        label, applied = combat.compose_difficulty(
            "Hard", character, {"weapon_category": "blades"}, fake,
            support_ease=True,
        )
        assert label == "Easy"
        assert applied == "weapon_mastery"

    def test_ladder_clamps_at_easy(self, ruleset):
        character = self._char(specialty="anything")
        label, _ = combat.compose_difficulty(
            "Easy", character, {"specialty_declared": True}, ruleset,
            support_ease=True,
        )
        assert label == "Easy"

    def test_ladder_clamps_at_very_hard(self, ruleset):
        harder = _declared_step_technique("grim_burden", step="harder")
        fake = _FakeRulesetWithTechniques(ruleset, {"grim_burden": harder})
        character = self._char(techniques=["grim_burden"])
        label, _ = combat.compose_difficulty(
            "Very Hard", character,
            {"declared_technique_ids": ["grim_burden"]}, fake,
        )
        assert label == "Very Hard"

    def test_full_order_base_tag_step_support(self, ruleset):
        """The whole chain at once: Very Hard base, Easy tag overrides,
        character step and Support then saturate at the floor."""
        character = self._char(specialty="anything")
        label, _ = combat.compose_difficulty(
            "Very Hard", character, {"specialty_declared": True}, ruleset,
            easy_tag=True, support_ease=True,
        )
        assert label == "Easy"


class TestReviewFindingsB4:
    """Regressions for two rule bypasses found in review of the B4 cycle.

    Both slipped past the original suite because no test exercised a character
    with zero Sparks, and none asserted that a skill-scoped Technique *fails* to
    fire on the wrong skill.
    """

    def test_skill_scoped_technique_does_not_fire_on_another_skill(self, ruleset):
        """Acclimated is "Endurance rolls against your chosen hardship" (II.4a).

        Before the fix the trigger matched on `hazard_type` alone, so a character
        with Acclimated (extreme cold) rolling Combat in a warm tavern — while
        sending `hazard_type: "extreme cold"` — got the step. The engine was
        implementing a wider rule than the book prints.
        """
        character = SimpleNamespace(
            techniques=["acclimated"],
            technique_choices={"acclimated": "extreme cold"},
        )
        wrong_skill = {"skill_id": "combat", "hazard_type": "extreme cold"}
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, wrong_skill, ruleset)
        assert (label, applied) == ("Hard", None)

        right_skill = {"skill_id": "endurance", "hazard_type": "extreme cold"}
        label, applied = combat.apply_character_difficulty_step(
            "Hard", character, right_skill, ruleset)
        assert (label, applied) == ("Standard", "acclimated")

    def test_field_of_mastery_is_scoped_to_lore(self, ruleset):
        character = SimpleNamespace(
            techniques=["field_of_mastery"],
            technique_choices={"field_of_mastery": "history"},
        )
        assert combat.apply_character_difficulty_step(
            "Hard", character, {"skill_id": "persuade", "knowledge_field": "history"},
            ruleset) == ("Hard", None)
        assert combat.apply_character_difficulty_step(
            "Hard", character, {"skill_id": "lore", "knowledge_field": "history"},
            ruleset) == ("Standard", "field_of_mastery")

    def test_non_iterable_declared_ids_does_not_raise(self, ruleset):
        """A client sending a scalar used to raise straight through the dispatch
        loop and disconnect the sender."""
        character = SimpleNamespace(techniques=["the_uncanny_angle"], technique_choices={})
        for junk in (5, None, {"a": 1}, "the_uncanny_angle"):
            label, applied = combat.apply_character_difficulty_step(
                "Hard", character, {"declared_technique_ids": junk}, ruleset)
            assert label == "Hard" and applied is None


class TestStrikeRiders:
    """R3 (BRIEF_fun_second_act §3): a 10+ Strike depletes 2 Resolve and
    chooses one of three riders. The menu is data; the effects are engine.
    """

    # -- the menu ---------------------------------------------------------

    def test_menu_is_read_from_the_ruleset(self, ruleset):
        """Two in the core book: Cover was cut at the gate (D20)."""
        assert [r.id for r in combat.strike_riders(ruleset)] == ["open", "position"]

    def test_menu_is_offered_only_on_a_full_success(self, ruleset):
        assert combat.rider_menu("full_success", False, ruleset)
        assert combat.rider_menu("partial_success", False, ruleset) == []
        assert combat.rider_menu("failure", False, ruleset) == []

    def test_a_removed_mook_takes_no_rider(self, ruleset):
        """Against a Mook a 10+ removes it, and there is nothing left to
        hang a tempo tag on."""
        assert combat.rider_menu("full_success", True, ruleset) == []

    # -- Open -------------------------------------------------------------

    def test_open_rider_sets_the_tag(self, ruleset):
        enemy = _TagBearer(open=False)
        combat.apply_rider("open", enemy, ruleset, exchange_no=1)
        assert enemy.open is True

    def test_open_rider_expires_at_end_of_exchange(self, ruleset):
        enemy = _TagBearer(open=False)
        combat.apply_rider("open", enemy, ruleset, exchange_no=1)
        assert combat.expire_end_of_exchange(enemy, ruleset, exchange_no=1) == ["open"]
        assert enemy.open is False

    # -- Position ---------------------------------------------------------

    def test_position_makes_the_next_roll_easy(self, ruleset):
        enemy = _TagBearer(open=False)
        combat.apply_rider("position", enemy, ruleset, exchange_no=1)
        assert combat.has_easy_tag(enemy) is True

    def test_position_is_consumed_by_one_roll(self, ruleset):
        enemy = _TagBearer(open=False)
        combat.apply_rider("position", enemy, ruleset, exchange_no=1)
        assert combat.consume_position(enemy) is True
        assert combat.has_easy_tag(enemy) is False
        assert combat.consume_position(enemy) is False

    def test_position_survives_this_exchange_and_expires_after_the_next(self, ruleset):
        """'this exchange or next' — so it must NOT expire at the end of the
        exchange it was applied in."""
        enemy = _TagBearer(open=False)
        combat.apply_rider("position", enemy, ruleset, exchange_no=1)
        assert combat.expire_end_of_exchange(enemy, ruleset, exchange_no=1) == []
        assert combat.has_easy_tag(enemy) is True
        assert combat.expire_end_of_exchange(enemy, ruleset, exchange_no=2) == ["position"]
        assert combat.has_easy_tag(enemy) is False

    # -- Open and Position do not stack ------------------------------------

    def test_open_and_position_do_not_stack(self, ruleset):
        """Both are Easy-tag sources, and III.1's precedence makes Easy an
        absolute override that does not stack with itself. The composed
        difficulty with both must equal the composed difficulty with one."""
        both = _TagBearer(open=True)
        combat.apply_rider("position", both, ruleset, exchange_no=1)
        one = _TagBearer(open=True)
        assert (combat.target_strike_difficulty("Hard", combat.has_easy_tag(both), ruleset)
                == combat.target_strike_difficulty("Hard", combat.has_easy_tag(one), ruleset))

    def test_easy_tag_is_true_for_either_source(self, ruleset):
        assert combat.has_easy_tag(_TagBearer(open=True)) is True
        assert combat.has_easy_tag(_TagBearer(open=False)) is False

    # -- Cover --------------------------------------------------------------
    # Cut from the core menu at the gate (D20) because it undid R2, but the
    # effect stays implemented for a setting or a future Technique to offer.
    # These tests run against a ruleset that puts it back, which is also the
    # regression guard on that promise.

    @pytest.fixture
    def cover_ruleset(self, ruleset):
        import copy
        from app.facets.schema import StrikeRiderDef
        rs = copy.deepcopy(ruleset)
        rs.combat.enemy_durability.strike_riders = list(
            rs.combat.enemy_durability.strike_riders
        ) + [StrikeRiderDef(id="cover", label="Cover",
                            effect="free_reaction_ally",
                            duration="end_of_exchange")]
        return rs

    def test_cover_is_not_in_the_core_menu(self, ruleset):
        assert "cover" not in [r.id for r in combat.strike_riders(ruleset)]

    def test_cover_frees_one_reaction_for_the_named_ally(self, cover_ruleset):
        ally = _TagBearer()
        enemy = _TagBearer(open=False)
        combat.apply_rider("cover", enemy, cover_ruleset, ally=ally, exchange_no=1)
        assert combat.consume_free_reaction(ally) is True

    def test_cover_frees_exactly_one_reaction(self, cover_ruleset):
        ally = _TagBearer()
        combat.apply_rider("cover", _TagBearer(open=False), cover_ruleset,
                           ally=ally, exchange_no=1)
        assert combat.consume_free_reaction(ally) is True
        assert combat.consume_free_reaction(ally) is False

    def test_cover_reaches_only_the_named_ally(self, cover_ruleset):
        ally, bystander = _TagBearer(), _TagBearer()
        combat.apply_rider("cover", _TagBearer(open=False), cover_ruleset,
                           ally=ally, exchange_no=1)
        assert combat.consume_free_reaction(bystander) is False

    def test_cover_expires_at_end_of_exchange(self, cover_ruleset):
        ally = _TagBearer()
        enemy = _TagBearer(open=False)
        combat.apply_rider("cover", enemy, cover_ruleset, ally=ally, exchange_no=1)
        assert combat.expire_end_of_exchange(ally, cover_ruleset, exchange_no=1) == ["cover"]
        assert combat.consume_free_reaction(ally) is False

    def test_cover_requires_an_ally(self, cover_ruleset):
        with pytest.raises(ValueError):
            combat.apply_rider("cover", _TagBearer(open=False), cover_ruleset,
                               exchange_no=1)

    # -- errors -------------------------------------------------------------

    def test_unknown_rider_is_rejected(self, ruleset):
        with pytest.raises(ValueError):
            combat.apply_rider("banish", _TagBearer(open=False), ruleset,
                               exchange_no=1)

    def test_the_core_ruleset_refuses_the_cut_rider(self, ruleset):
        """The engine must refuse a rider the book does not print, rather
        than quietly applying it — this is what makes the D20 cut real
        rather than cosmetic."""
        with pytest.raises(ValueError):
            combat.apply_rider("cover", _TagBearer(open=False), ruleset,
                               ally=_TagBearer(), exchange_no=1)
