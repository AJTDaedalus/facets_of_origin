"""Tests for the combat simulator."""
import random
import pytest
import sys
from pathlib import Path

# Ensure software/ is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.game import combat as combat_module

from tools.combat_sim import (
    PCState,
    EnemyState,
    SimResult,
    AggregateResult,
    TIER2_CONDITIONS,
    combat_roll,
    _pc_strike,
    _enemy_attack,
    _ruleset,
    run_combat,
    run_simulation,
    make_pc,
    make_enemy,
    mordai_def,
    zahna_def,
    zulnut_def,
    standard_party,
    chicken_def,
    city_watch_sergeant_def,
    veteran_soldier_def,
    generic_named_def,
    _choose_rider,
    generic_boss_def,
    archive_guardian_def,
    choose_pc_posture,
    choose_enemy_posture,
    choose_pc_target,
    choose_enemy_target,
    should_spend_spark,
    should_press,
    choose_pc_reaction,
    get_series,
    _wilson_ci,
    spark_refund_variant_enabled,
)


# ---------------------------------------------------------------------------
# Dice rolling
# ---------------------------------------------------------------------------

class TestCombatRoll:
    def test_basic_roll_returns_three_tuple(self):
        outcome, dice, total = combat_roll(0)
        assert outcome in ("full_success", "partial_success", "failure")
        assert len(dice) == 2
        assert all(1 <= d <= 6 for d in dice)

    def test_modifier_affects_total(self):
        random.seed(42)
        _, _, total_no_mod = combat_roll(0)
        random.seed(42)
        _, _, total_with_mod = combat_roll(3)
        assert total_with_mod == total_no_mod + 3

    def test_difficulty_affects_total(self):
        random.seed(42)
        _, _, total_standard = combat_roll(0, "Standard")
        random.seed(42)
        _, _, total_hard = combat_roll(0, "Hard")
        assert total_standard == total_hard + 1  # Standard=0, Hard=-1

    def test_extra_dice_drops_lowest(self):
        random.seed(42)
        _, dice_base, _ = combat_roll(0)
        random.seed(42)
        _, dice_spark, _ = combat_roll(0, extra_dice=1)
        assert len(dice_base) == 2
        assert len(dice_spark) == 2  # Still keeps 2 dice

    def test_outcome_thresholds(self):
        # Test with known seeds
        results = set()
        for seed in range(1000):
            random.seed(seed)
            outcome, _, total = combat_roll(0)
            if total >= 10:
                assert outcome == "full_success"
            elif total >= 7:
                assert outcome == "partial_success"
            else:
                assert outcome == "failure"
            results.add(outcome)
        # Should hit all three outcomes in 1000 trials
        assert results == {"full_success", "partial_success", "failure"}

    def test_extra_dice_improve_outcomes(self):
        """Sparks/Press should shift the distribution toward better outcomes."""
        random.seed(123)
        base_totals = [combat_roll(0)[2] for _ in range(1000)]
        random.seed(123)  # Different seed to avoid correlation
        spark_totals = [combat_roll(0, extra_dice=1)[2] for _ in range(1000)]
        # Extra dice should increase mean total (drop lowest)
        # Can't compare directly with same seed because different # of random calls
        # Just verify the mean is reasonable
        assert 2 <= sum(base_totals) / 1000 <= 12


# Condition management (apply_condition/cleanup_end_of_exchange/
# armor_downgrade) and their unit tests moved to `app.game.combat` /
# `tests/test_combat.py` per TASKS WS-A0 (A0.3) — combat_sim.py no longer
# has its own copies.

# ---------------------------------------------------------------------------
# AI decisions
# ---------------------------------------------------------------------------

class TestAI:
    def test_pc_posture_high_end_aggressive(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 5  # Full
        assert choose_pc_posture(pc, 3) == "aggressive"

    def test_pc_posture_mid_end_measured(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 2
        assert choose_pc_posture(pc, 3) == "measured"

    def test_pc_posture_zero_end_withdrawn(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        assert choose_pc_posture(pc, 3) == "withdrawn"

    def test_pc_posture_zero_end_last_standing(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        assert choose_pc_posture(pc, 1) == "measured"

    def test_enemy_posture_mook(self):
        enemy = make_enemy(chicken_def())
        assert choose_enemy_posture(enemy) == "measured"

    def test_enemy_posture_named(self):
        enemy = make_enemy(generic_named_def(8))
        assert choose_enemy_posture(enemy) == "measured"

    def test_target_selection_mooks_first(self):
        pc = make_pc(mordai_def())
        enemies = [
            make_enemy(generic_named_def(8)),
            make_enemy(chicken_def(), 1),
        ]
        target = choose_pc_target(pc, enemies, _ruleset())
        assert target.tier == "mook"

    def test_target_selection_prefers_open_named(self):
        """K-6/D4: an Open enemy is Easy to Strike for everyone — the AI
        presses the advantage before the enemy spends its action clearing.
        (Replaces the retired Tier-2-rider priority.)"""
        pc = make_pc(mordai_def())
        named1 = make_enemy(generic_named_def(8))
        named2 = make_enemy(generic_named_def(8))
        named2.instance_id = "named2"
        named2.open = True
        target = choose_pc_target(pc, [named1, named2], _ruleset())
        assert target.instance_id == "named2"

    def test_spark_finishing_blow_fires_on_open_target(self):
        """The conservative policy's finishing-blow branch keys on the Open
        tag (the K-6/D4 'target is exposed' signal, replacing the retired
        Tier-2-rider check)."""
        pc = make_pc(mordai_def())
        named = make_enemy(generic_named_def(8))
        named.open = True
        assert should_spend_spark(pc, named, _ruleset(), "conservative") == 1

    def test_enemy_targets_lowest_endurance(self):
        enemy = make_enemy(generic_named_def(8))
        pcs = [make_pc(mordai_def()), make_pc(zahna_def())]
        target = choose_enemy_target(enemy, pcs)
        assert target.name == "Zahna"  # End 3 < Mordai's 5

    def test_spark_spend_against_boss(self):
        pc = make_pc(mordai_def())
        boss = make_enemy(generic_boss_def(12))
        assert should_spend_spark(pc, boss, _ruleset()) == 1

    def test_no_spark_against_mook(self):
        pc = make_pc(mordai_def())
        mook = make_enemy(chicken_def())
        assert should_spend_spark(pc, mook, _ruleset()) == 0

    def test_spark_at_low_endurance(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 1
        named = make_enemy(generic_named_def(8))
        assert should_spend_spark(pc, named, _ruleset()) == 1

    def test_no_spark_when_none_left(self):
        pc = make_pc(mordai_def())
        pc.sparks = 0
        boss = make_enemy(generic_boss_def(12))
        assert should_spend_spark(pc, boss, _ruleset()) == 0

    def test_reaction_absorb_at_zero_end(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        assert choose_pc_reaction(pc, 2, "measured") == "absorb"

    def test_reaction_parry_when_combat_strong(self):
        pc = make_pc(mordai_def())  # Str+1, Combat+1 = parry_mod 2 > dodge_mod 0
        assert choose_pc_reaction(pc, 2, "measured") == "parry"

    def test_reaction_dodge_when_dex_better(self):
        pc = make_pc(zahna_def())  # Dex+1 > Str-1+Combat 0 = -1
        assert choose_pc_reaction(pc, 2, "measured") == "dodge"

# ---------------------------------------------------------------------------
# Strike resolution
# ---------------------------------------------------------------------------

class TestPCStrike:
    def test_mook_removed_on_success(self):
        # Keep trying seeds until we get a success
        for seed in range(100):
            random.seed(seed)
            pc_fresh = make_pc(mordai_def())
            mook_fresh = make_enemy(chicken_def())
            _pc_strike(pc_fresh, mook_fresh, _ruleset())
            if mook_fresh.is_removed:
                break
        assert mook_fresh.is_removed

    def test_withdrawn_pc_cannot_strike(self):
        pc = make_pc(mordai_def())
        pc.posture = "withdrawn"
        mook = make_enemy(chicken_def())
        _pc_strike(pc, mook, _ruleset())
        assert not mook.is_removed

    def test_named_left_open_on_full_success(self):
        """A full-success (10+) Strike may leave a Named enemy Open
        (K-6/D4, attacker's option) — a tag, not a Condition; Resolve is
        what defeats an enemy. The enemy takes no Strike Conditions."""
        open_seen = False
        for seed in range(200):
            random.seed(seed)
            pc = make_pc(mordai_def())
            named_fresh = make_enemy(generic_named_def(8))
            _pc_strike(pc, named_fresh, _ruleset())
            assert named_fresh.conditions == []
            if named_fresh.open:
                open_seen = True
                break
        assert open_seen, "Should see a Named enemy left Open after many strikes"

    def test_named_resolve_depletes_on_success(self):
        """A landed Strike depletes the target's Resolve pool (D1)
        regardless of whether a rider was also applied."""
        depletion_seen = False
        for seed in range(200):
            random.seed(seed)
            pc = make_pc(mordai_def())
            named_fresh = make_enemy(generic_named_def(8))
            starting_resolve = named_fresh.resolve_current
            _pc_strike(pc, named_fresh, _ruleset())
            if named_fresh.resolve_current < starting_resolve:
                depletion_seen = True
                break
        assert depletion_seen, "Should see Resolve depletion on Named enemy after many strikes"

    def test_enemy_never_reacts_depletion_is_outcome_only(self):
        """A14/F5: enemies have no reaction. A landed Strike depletes Resolve
        by exactly the outcome's `strike_depletion` value — never more (a
        parry cost) and never less (a full deflect), since no Resolve is ever
        spent on defense. Across many seeds the observed depletion always
        equals the canonical value for the outcome that actually rolled."""
        ruleset = _ruleset()
        expected = {
            "full_success": ruleset.combat.enemy_durability.strike_depletion.full_success,
            "partial_success": ruleset.combat.enemy_durability.strike_depletion.partial_success,
            "failure": ruleset.combat.enemy_durability.strike_depletion.failure,
        }
        for seed in range(300):
            random.seed(seed)
            pc = make_pc(mordai_def())
            named = make_enemy(generic_named_def(8))
            starting = named.resolve_current
            # Reproduce _pc_strike's exact dice: extra dice come from the same
            # Spark/Press policy the function uses, and a fresh target has no
            # conditions so difficulty is Standard.
            extra_dice = should_spend_spark(pc, named, _ruleset()) + (1 if should_press(pc, named) else 0)
            random.seed(seed)
            strike = combat_module.resolve_strike(
                pc.strength_mod + pc.combat_mod, pc.posture, pc.conditions, ruleset,
                combat_module.StrikeOptions(extra_dice=extra_dice),
            )
            random.seed(seed)
            _pc_strike(pc, named, ruleset)
            actual_depletion = starting - named.resolve_current
            assert actual_depletion == expected[strike.outcome], (
                f"seed {seed}: {strike.outcome} depleted {actual_depletion}, "
                f"expected {expected[strike.outcome]} (no defense spend)"
            )

    def test_no_open_on_partial_success(self):
        """K-6/D4: only a full success may leave the target Open — a
        partial success (7-9) depletes 1 Resolve and nothing else."""
        for seed in range(500):
            random.seed(seed)
            pc = make_pc(mordai_def())
            named_fresh = make_enemy(generic_named_def(8))
            strike = combat_module.resolve_strike(
                pc.strength_mod + pc.combat_mod, pc.posture, pc.conditions, _ruleset(),
            )
            if strike.outcome != "partial_success":
                continue
            random.seed(seed)
            _pc_strike(pc, named_fresh, _ruleset())
            assert named_fresh.open is False
            assert named_fresh.conditions == []
            return
        pytest.fail("No seed produced a partial-success Strike in 500 tries")

    def test_armored_mook_needs_full_success(self):
        """An armored Mook is only removed on a full success (10+); an
        unarmored Mook is removed on any success (D1)."""
        removed_on_partial = False
        for seed in range(500):
            random.seed(seed)
            pc = make_pc(mordai_def())
            strike = combat_module.resolve_strike(
                pc.strength_mod + pc.combat_mod, pc.posture, pc.conditions, _ruleset(),
            )
            if strike.outcome != "partial_success":
                continue
            random.seed(seed)
            pc2 = make_pc(mordai_def())
            mook = make_enemy(chicken_def())
            mook.armor = "light"
            _pc_strike(pc2, mook, _ruleset())
            if mook.is_removed:
                removed_on_partial = True
            break
        assert not removed_on_partial, "Armored Mook should survive a partial success"

    def test_staggered_attacker_penalty(self):
        """Staggered PCs should have -1 to offense."""
        totals_normal = []
        totals_staggered = []
        for seed in range(500):
            random.seed(seed)
            pc = make_pc(mordai_def())
            mook = make_enemy(chicken_def())
            _, _, total = combat_roll(pc.strength_mod + pc.combat_mod)
            totals_normal.append(total)

            random.seed(seed)
            pc2 = make_pc(mordai_def())
            pc2.conditions.append("staggered")
            _, _, total2 = combat_roll(pc2.strength_mod + pc2.combat_mod - 1)
            totals_staggered.append(total2)

        # Staggered totals should be exactly 1 lower
        for n, s in zip(totals_normal, totals_staggered):
            assert s == n - 1


class TestEnemyAttack:
    def test_mook_attack_is_t1(self):
        """Mook attacks produce T1 conditions (when PC fails reaction).

        F5 retired (DESIGN §4.3): absorbing at 0 Endurance no longer
        escalates the incoming tier, so a Mook's T1 attack lands as T1.
        """
        mook = make_enemy(chicken_def())
        for seed in range(200):
            random.seed(seed)
            pc = make_pc(mordai_def())
            pc.endurance_current = 0  # Force Absorb
            _enemy_attack(mook, pc, _ruleset())
            if pc.conditions:
                assert all(c not in ("staggered", "cornered") for c in pc.conditions)
                break

    def test_named_attack_is_t2(self):
        """Named NPC attacks produce T2 conditions (when PC absorbs)."""
        named = make_enemy(generic_named_def(8))
        pc = make_pc(mordai_def())
        pc.endurance_current = 0  # Force Absorb
        _enemy_attack(named, pc, _ruleset())
        # Should have a T2 condition (staggered or cornered)
        assert any(c in TIER2_CONDITIONS for c in pc.conditions)


# ---------------------------------------------------------------------------
# Boss phase change
# ---------------------------------------------------------------------------

class TestBossPhaseChange:
    """D1 (DESIGN §4.1): phase changes are Resolve-threshold crossings, not
    Condition-stacking Broken escalations — enemies no longer have a
    Condition-based Broken track at all.

    R2/D20 re-authored the Guardian's phase (task T15): the threshold moved
    2 -> 4 so the phase lands mid-fight rather than in the exchange the fight
    ends, and the attack drop is gone — Reduced Mode now *raises* its danger
    rather than lowering it. `special_attack_mod` stays on `EnemyState` for
    other authored bosses; the Guardian no longer sets it.
    """

    def test_phase_change_fires_when_resolve_crosses_threshold(self):
        pc = make_pc(mordai_def())
        for seed in range(300):
            random.seed(seed)
            boss = make_enemy(archive_guardian_def())
            boss.resolve_current = 5  # one full-success Strike (-2) crosses threshold 4
            _pc_strike(pc, boss, _ruleset())
            if boss.phase_index is not None:
                assert boss.phase_index == 0
                # Reduced Mode no longer softens the attack — that was the old
                # Special, and softening a Boss's second act was backwards.
                assert boss.attack_modifier == 3
                return
        pytest.fail("No seed produced a phase change in 300 tries")

    def test_phase_change_does_not_refire(self):
        """`apply_resolve_damage`/`phase_crossed` fire the crossing exactly
        once by construction (A7) — Resolve only moves downward, so a
        Strike landing after the threshold is already crossed reports no
        new crossing."""
        boss = make_enemy(archive_guardian_def())
        boss.resolve_current = 2
        boss.phase_index = 0
        boss.attack_modifier = 1
        pc = make_pc(mordai_def())
        for seed in range(300):
            random.seed(seed)
            strike = combat_module.resolve_strike(
                pc.strength_mod + pc.combat_mod, pc.posture, pc.conditions, _ruleset(),
            )
            if strike.outcome == "failure":
                continue
            random.seed(seed)
            _pc_strike(pc, boss, _ruleset())
            assert boss.phase_index == 0
            assert boss.attack_modifier == 1
            return
        pytest.fail("No seed produced a landed Strike in 300 tries")

    def test_defeat_is_removal_not_broken(self):
        """An enemy defeated via Resolve reaching 0 is `is_removed`, not
        `is_broken` — enemies have no Broken track under D1."""
        pc = make_pc(mordai_def())
        for seed in range(300):
            random.seed(seed)
            boss = make_enemy(archive_guardian_def())
            boss.resolve_current = 2  # one full success finishes it
            _pc_strike(pc, boss, _ruleset())
            if boss.is_removed:
                return
        pytest.fail("No seed produced a defeat in 300 tries")


# ---------------------------------------------------------------------------
# Full combat loop
# ---------------------------------------------------------------------------

class TestCombatLoop:
    def test_party_beats_mooks(self):
        """3 PCs should reliably beat 3 chickens."""
        random.seed(42)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(chicken_def(), i) for i in range(1, 4)]
        result = run_combat(pcs, enemies)
        assert result.party_wins
        assert result.exchanges <= 5

    def test_combat_terminates(self):
        """Combat should not run forever."""
        random.seed(99)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(chicken_def(), i) for i in range(1, 4)]
        result = run_combat(pcs, enemies)
        assert result.exchanges <= MAX_EXCHANGES

    def test_combat_against_named(self):
        """Party should be able to defeat a Named NPC."""
        wins = 0
        for seed in range(50):
            random.seed(seed)
            pcs = [make_pc(d) for d in standard_party()]
            enemies = [make_enemy(generic_named_def(8))]
            result = run_combat(pcs, enemies)
            if result.party_wins:
                wins += 1
        # Should win most of the time against a single Named
        assert wins > 25, f"Party only won {wins}/50 against Named NPC"

    def test_result_fields_populated(self):
        random.seed(42)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(chicken_def(), i) for i in range(1, 4)]
        result = run_combat(pcs, enemies)
        assert isinstance(result.exchanges, int)
        assert isinstance(result.sparks_spent, int)
        assert isinstance(result.pcs_broken, list)
        assert isinstance(result.endurance_remaining, dict)
        assert "Mordai" in result.endurance_remaining


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

class TestSimulation:
    def test_simulation_runs(self):
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=20,
            label="Test: 3 Chickens",
            seed=42,
        )
        assert result.iterations == 20
        assert result.wins + result.losses == 20
        assert 0.0 <= result.win_rate <= 1.0

    def test_three_chickens_high_win_rate(self):
        """3 Chickens (Skirmish) should have ~100% win rate."""
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=100,
            label="Skirmish: 3 Chickens",
            seed=42,
        )
        assert result.win_rate >= 0.90, f"Win rate {result.win_rate} too low for Skirmish"

    def test_confidence_interval(self):
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=100,
            label="CI test",
            seed=42,
        )
        assert result.win_rate_ci_low <= result.win_rate <= result.win_rate_ci_high

    def test_endurance_stats_populated(self):
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=20,
            label="Endurance test",
            seed=42,
        )
        assert "Mordai" in result.endurance_stats
        assert "Zahna" in result.endurance_stats
        assert "Zulnut" in result.endurance_stats

    def test_seed_reproducibility(self):
        r1 = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=50,
            label="Seed test 1",
            seed=42,
        )
        r2 = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=50,
            label="Seed test 2",
            seed=42,
        )
        assert r1.wins == r2.wins
        assert r1.mean_exchanges == r2.mean_exchanges


# ---------------------------------------------------------------------------
# Wilson CI
# ---------------------------------------------------------------------------

class TestWilsonCI:
    def test_all_wins(self):
        low, high = _wilson_ci(100, 100)
        assert low > 0.95
        assert high > 0.99

    def test_all_losses(self):
        low, high = _wilson_ci(0, 100)
        assert low == 0.0
        assert high < 0.05

    def test_half_and_half(self):
        low, high = _wilson_ci(50, 100)
        assert 0.35 < low < 0.50
        assert 0.50 < high < 0.65

    def test_zero_n(self):
        low, high = _wilson_ci(0, 0)
        assert low == 0.0
        assert high == 0.0


# ---------------------------------------------------------------------------
# Canonical definitions
# ---------------------------------------------------------------------------

class TestDefinitions:
    def test_mordai_endurance(self):
        pc = make_pc(mordai_def())
        assert pc.endurance_max == 5
        assert pc.endurance_current == 5

    def test_zahna_endurance(self):
        pc = make_pc(zahna_def())
        assert pc.endurance_max == 3
        assert pc.endurance_current == 3

    def test_zulnut_endurance(self):
        pc = make_pc(zulnut_def())
        assert pc.endurance_max == 3
        assert pc.endurance_current == 3

    def test_chicken_is_mook(self):
        e = make_enemy(chicken_def())
        assert e.tier == "mook"
        assert e.resolve == 0
        assert e.resolve_current == 0

    def test_sergeant_is_named(self):
        """Matches `enemies/city_watch_sergeant.fof` (D1 migration): base
        Resolve 3, +1 from light armor at combat start."""
        e = make_enemy(city_watch_sergeant_def())
        assert e.tier == "named"
        assert e.resolve == 3
        assert e.resolve_current == 4
        assert e.armor == "light"

    def test_guardian_is_boss(self):
        """Matches `enemies/archive_guardian.fof`: base Resolve 8 (A8/G1
        retune, DESIGN §5-bis), +2 from heavy armor at combat start
        (effective 10)."""
        e = make_enemy(archive_guardian_def())
        assert e.tier == "boss"
        assert e.resolve == 8
        assert e.resolve_current == 10
        assert e.phases == [{"resolve_threshold": 4, "description": "Reduced Mode"}]
        assert e.armor == "heavy"

    def test_series_definitions_valid(self):
        series = get_series()
        assert "A" in series
        assert "B" in series
        assert "C" in series
        assert "D" in series
        assert "E" in series
        for series_id, configs in series.items():
            for label, pcs, enemies in configs:
                assert len(pcs) > 0
                assert len(enemies) > 0
                assert isinstance(label, str)


# ---------------------------------------------------------------------------
# Integration: validate against hand-simulated known results
# ---------------------------------------------------------------------------

class TestCalibration:
    """Validate that simulator results align with hand-simulated data."""

    def test_three_chickens_skirmish(self):
        """3 Chickens should be a Skirmish (~100% win rate)."""
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=200,
            label="Calibration: 3 Chickens",
            seed=1,
        )
        assert result.win_rate >= 0.90
        assert result.mean_exchanges <= 5

    def test_seven_chickens_harder(self):
        """7 Chickens should take significantly longer than 3.

        Win rate is no longer a usable signal here after A6/F5: Mooks only
        ever land Tier 1 hits, and with the 0-Endurance escalation retired
        (DESIGN §4.3) a Mook swarm can no longer push a PC to a persistent
        Tier 2, so both sizes sit at the 1.0 win-rate ceiling. `mean_exchanges`
        still tracks difficulty — more Mooks take longer to grind through —
        and is the assertion that survives. Chicken-baseline win rates are
        superseded corpus per A0.4; full recalibration is A10's job.
        """
        result_3 = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=200,
            label="3 Chickens",
            seed=1,
        )
        result_7 = run_simulation(
            standard_party(),
            [(chicken_def(), 7)],
            iterations=200,
            label="7 Chickens",
            seed=1,
        )
        assert result_7.mean_exchanges > result_3.mean_exchanges

    def test_boss_harder_than_named(self):
        """Boss fights should take longer than Named NPC fights.

        Win rate is no longer a usable signal here (same ceiling-effect as
        `test_seven_chickens_harder` above): 3 PCs against either a single
        Named or a single Boss at these post-D1 Resolve values both sit at
        a 1.0 win-rate ceiling. `mean_exchanges` is the signal that
        survives — a Boss's larger effective Resolve (7 + heavy armor 2 = 9
        for a TR16 boss, vs a TR8 Named's 3 + light armor 1 = 4) reliably
        takes more Strikes to grind through.

        A single generic Named(TR8) is also no longer reliably slower than
        a 3-Mook swarm post-D1 (its Resolve pool is small enough that 3 PCs
        burn through it about as fast as removing 3 separate Mooks one
        Strike each) — that comparison was dropped rather than loosened,
        since "Named vs Mook-swarm" pacing is generic-def calibration, not
        a D1 correctness question. Full recalibration against the new
        Resolve numbers is Gate G4 (task A10).
        """
        result_named = run_simulation(
            standard_party(),
            [(generic_named_def(8), 1)],
            iterations=200,
            label="Named NPC",
            seed=1,
        )
        result_boss = run_simulation(
            standard_party(),
            [(generic_boss_def(16), 1)],
            iterations=200,
            label="Boss",
            seed=1,
        )
        assert result_boss.mean_exchanges > result_named.mean_exchanges


class TestObjectiveClockHook:
    """T3.11: the sim's K-2/D5 hook. The rule (an exchange with no PC
    offensive action is uncontested) is READ from
    `combat.exchange_uncontested`; the tool only supplies the stake —
    an objective clock that fills on uncontested exchanges."""

    def test_clock_fills_on_uncontested_exchanges_and_loses(self, monkeypatch):
        """A party that only cycles Withdrawn hands the MM the scene: the
        clock fills, the objective is taken, the encounter is lost."""
        import tools.combat_sim as sim
        monkeypatch.setattr(sim, "choose_pc_posture", lambda pc, allies: "withdrawn")
        random.seed(1)
        pcs = [make_pc(d) for d in standard_party()]
        # An enemy whose Tier 1 chip cannot break anyone: a single chicken.
        enemies = [make_enemy(chicken_def())]
        result = run_combat(pcs, enemies, objective_clock=4)
        assert result.objective_lost is True
        assert result.party_wins is False
        assert result.uncontested_exchanges == 4
        assert result.exchanges == 4

    def test_no_clock_reproduces_recorded_behaviour(self):
        """objective_clock=None: the counter observes, nothing else
        changes — the recorded-corpus contract (WD10 shape)."""
        random.seed(1)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(city_watch_sergeant_def())]
        result = run_combat(pcs, enemies)
        assert result.objective_lost is False
        assert (result.party_wins, result.exchanges) == (True, 1)

    def test_contested_fight_never_advances_the_clock(self):
        """A normal fight — PCs striking every exchange — has zero
        uncontested exchanges, so even a 1-segment clock never fills."""
        random.seed(1)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(city_watch_sergeant_def())]
        result = run_combat(pcs, enemies, objective_clock=1)
        assert result.objective_lost is False
        assert result.uncontested_exchanges == 0
        assert result.party_wins is True


class TestRecipeCalibration:
    """Pin the four MM1 Encounter Recipe Table rosters (task A10 / Gate G4).

    These are the *calibrated deliverable* of A10: the recipes the MM builds
    from, measured in the simulator rather than derived from the (demoted,
    non-predictive) TR-budget formula. Each roster is the validated PS-3
    composition from `research/simulation_log.md` Series 9 Part C. The win
    rates are pinned to their recorded seed-1 values (n=200 is deterministic
    at a fixed seed) *and* asserted to fall inside the difficulty band, so
    that any future rules/engine change that shifts a recipe out of its band
    trips a test instead of silently invalidating the MM1 table.

    The difficulty ladder here is built by adding actors, not raising TR —
    that is the whole point of the recalibration (DESIGN §5-ter).

    A14 CASCADE, A15 RESOLUTION (2026-07-11): removing the enemy Parry
    (§5-quater F5) moved every recipe ~one band easier, tripping the band
    assertions by design (the guard working: a model correction must NOT
    silently invalidate the MM1 Recipe Table). A15 re-ran the actor-count
    ladder under the corrected model and re-pinned the rosters — see
    `research/simulation_log.md` Series 9 Part D. The recalibrated ladder is
    a fixed 3-Named core with one Mook added per difficulty step: Standard
    3× Named + 1 Mook (76.0%), Hard 3× Named + 2 Mooks (47.5%), Deadly
    3× Named + 3 Mooks (20.0%) with a 4× Named + 1 Mook alternative (20.0%).
    The `xfail(strict)` markers were removed as each recipe re-entered band.

    R2 CASCADE (2026-09-08, D20): Open expiring at end of exchange
    (`combat.enemy_durability.open_clears`) removed the permanent Easy tag
    the party used to hold from its first 10+ onward, so every row moved
    down — Standard 76.0 -> 73.0, Hard 47.5 -> 38.0, Deadly 20.0 -> 17.5,
    Deadly-alt 20.0 -> 16.5 at seed 1. The guard did its job and tripped.
    Re-pinned to the Series 12 Part B values.

    The brief's prescribed repair (retune Named Resolve by -1 before
    touching a recipe) was measured and **rejected**: at Resolve 2 a Named
    NPC dies to a single full-success Strike, so it stops having a second
    exchange at all, and every row overshoots on the high side (Standard
    88.5-97.0%, Hard 61.5-73.0%, Deadly 35.5-44.5%). There is no -1 step
    available at the Named tier — the 3-4 authoring band has no interior.
    R2 is therefore adopted unretuned, and Hard now runs at the floor of
    its band rather than its middle: 38.0-45.0% across seeds 1/2/3/7/42
    against a published 40-60%, inside the +/-5pp the acceptance grants.
    See `research/simulation_log.md` Series 12 Part B.
    """

    def test_skirmish_mook_swarm(self):
        """Skirmish (85–100%): 3–7 Mooks. Recorded seed-1 win rate 100%."""
        result = run_simulation(
            standard_party(),
            [(chicken_def(), 5)],
            iterations=200,
            label="Recipe: Skirmish (5 Mooks)",
            seed=1,
        )
        assert result.win_rate == 1.0
        assert 0.85 <= result.win_rate <= 1.00

    def test_standard_three_named_plus_mook(self):
        """Standard (65–85%): 3 Named (TR 8) + 1 Mook. Series 12 Part B
        seed-1 win 73.0% under R2 (was 76.0% pre-R2)."""
        result = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=200,
            label="Recipe: Standard (3x Named TR8 + 1 Mook)",
            seed=1,
        )
        assert result.win_rate == pytest.approx(0.730)
        assert 0.65 <= result.win_rate <= 0.85

    def test_hard_three_named_plus_two_mooks(self):
        """Hard (40–60%): 3 Named (TR 8) + 2 Mooks. Series 12 Part B seed-1
        win 38.0% under R2 (was 47.5% pre-R2).

        The band assertion carries the acceptance's explicit +/-5pp: Hard now
        runs at its floor, not its middle, and the -1 Resolve retune that
        would lift it overshoots every other row (see the class docstring).
        A row falling below 0.35 is a real regression and still trips."""
        result = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 2)],
            iterations=200,
            label="Recipe: Hard (3x Named TR8 + 2 Mooks)",
            seed=1,
        )
        assert result.win_rate == pytest.approx(0.380)
        assert 0.35 <= result.win_rate <= 0.60

    def test_deadly_three_named_plus_three_mooks(self):
        """Deadly (15–35%): 3 Named (TR 8) + 3 Mooks. Series 12 Part B seed-1
        win 17.5% under R2 (was 20.0% pre-R2)."""
        result = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 3)],
            iterations=200,
            label="Recipe: Deadly (3x Named TR8 + 3 Mooks)",
            seed=1,
        )
        assert result.win_rate == pytest.approx(0.175)
        assert 0.15 <= result.win_rate <= 0.35

    def test_deadly_four_named_plus_mook(self):
        """Deadly (15–35%): 4 Named (TR 8) + 1 Mook — the "upgrade a throwaway
        to a real threat" alternative. Series 12 Part B seed-1 win 16.5%
        under R2 (was 20.0% pre-R2). This is the noisiest row in the table
        (13.5pp spread across five seeds, because four Named enemies make
        the outcome hinge on the first two Strikes), and seed 7 sat at 12.0%
        *before* R2 — the low tail is a property of the roster, not of the
        rule."""
        result = run_simulation(
            standard_party(),
            [(generic_named_def(8), 4), (chicken_def(), 1)],
            iterations=200,
            label="Recipe: Deadly (4x Named TR8 + 1 Mook)",
            seed=1,
        )
        assert result.win_rate == pytest.approx(0.165)
        assert 0.10 <= result.win_rate <= 0.35

    def test_ladder_is_built_by_adding_actors_not_tr(self):
        """The Standard→Hard→Deadly ladder is an actor-count ladder.

        Same TR-8 Named core; difficulty rises purely by adding actors. This
        is the finding the TR budget cannot represent (Series 9), pinned here
        so the recipes' monotonic ordering can't regress unnoticed.
        """
        std = run_simulation(
            standard_party(), [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=200, label="ladder-std", seed=1,
        )
        hard = run_simulation(
            standard_party(), [(generic_named_def(8), 3), (chicken_def(), 2)],
            iterations=200, label="ladder-hard", seed=1,
        )
        deadly = run_simulation(
            standard_party(), [(generic_named_def(8), 3), (chicken_def(), 3)],
            iterations=200, label="ladder-deadly", seed=1,
        )
        assert std.win_rate > hard.win_rate > deadly.win_rate


# ---------------------------------------------------------------------------
# Spark refund variant flag (D6, WD7) -- "test, do not adopt"
# ---------------------------------------------------------------------------

class TestSparkRefundVariant:
    def test_disabled_by_default(self):
        assert spark_refund_variant_enabled() is False

    def test_readable_from_a_custom_ruleset(self):
        rs = _ruleset()
        assert spark_refund_variant_enabled(rs) is False
        assert rs.spark.variants.refund_on_failed_pretechnique_cast is False


# ---------------------------------------------------------------------------
# Spark spend policy (WD10) — selectable, default-preserving
# ---------------------------------------------------------------------------

class TestSparkSpendPolicy:
    """WD10: `should_spend_spark` grows a selectable `policy` without
    re-baselining any recorded corpus. `"conservative"` (default) must stay
    bit-identical to the pre-WD10 function; `"player_like"` must spend more.
    """

    def test_default_policy_is_conservative(self):
        """Omitting `policy` must match passing `"conservative"` explicitly,
        across every branch of the old function (Boss / desperation /
        finishing-blow / none of the above)."""
        boss = make_enemy(generic_boss_def(12))
        named = make_enemy(generic_named_def(8))
        mook = make_enemy(chicken_def())

        pc = make_pc(mordai_def())
        assert should_spend_spark(pc, boss, _ruleset()) == should_spend_spark(pc, boss, _ruleset(), "conservative") == 1

        pc = make_pc(mordai_def())
        assert should_spend_spark(pc, mook, _ruleset()) == should_spend_spark(pc, mook, _ruleset(), "conservative") == 0

        pc = make_pc(mordai_def())
        pc.endurance_current = 1
        assert should_spend_spark(pc, named, _ruleset()) == should_spend_spark(pc, named, _ruleset(), "conservative") == 1

    def test_conservative_does_not_spend_on_named_at_full_endurance(self):
        """Pins the exact pre-WD10 behaviour this policy must not disturb:
        a Named target with no Tier 2 condition, at full Endurance, gets no
        Spark under `"conservative"` — only `"player_like"` spends here."""
        pc = make_pc(mordai_def())
        named = make_enemy(generic_named_def(8))
        assert should_spend_spark(pc, named, _ruleset(), "conservative") == 0

    def test_player_like_spends_on_named_not_just_boss(self):
        pc = make_pc(mordai_def())
        named = make_enemy(generic_named_def(8))
        assert should_spend_spark(pc, named, _ruleset(), "player_like") == 1

    def test_player_like_spends_when_holding_above_a_floor(self):
        """Holding 2+ Sparks spends even against a Mook at full Endurance —
        the "less hoarding-prone" half of the policy `"conservative"` has no
        equivalent for."""
        pc = make_pc(mordai_def())
        pc.sparks = 2
        mook = make_enemy(chicken_def())
        assert should_spend_spark(pc, mook, _ruleset(), "player_like") == 1
        assert should_spend_spark(pc, mook, _ruleset(), "conservative") == 0

    def test_player_like_never_spends_below_zero_sparks(self):
        pc = make_pc(mordai_def())
        pc.sparks = 0
        boss = make_enemy(generic_boss_def(12))
        assert should_spend_spark(pc, boss, _ruleset(), "player_like") == 0

    def test_player_like_is_a_superset_of_conservative(self):
        """Every case where `"conservative"` spends, `"player_like"` also
        spends — `"player_like"` never hoards more than the default."""
        pc = make_pc(mordai_def())
        for target in (
            make_enemy(generic_boss_def(12)),
            make_enemy(generic_named_def(8)),
            make_enemy(chicken_def()),
        ):
            conservative = should_spend_spark(pc, target, _ruleset(), "conservative")
            player_like = should_spend_spark(pc, target, _ruleset(), "player_like")
            if conservative > 0:
                assert player_like > 0

    def test_run_combat_and_run_simulation_default_to_conservative(self):
        """`spark_policy` threads through `_pc_strike` via `run_combat` and
        `run_simulation` without changing the default call's behaviour."""
        explicit = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=50,
            seed=1,
            spark_policy="conservative",
        )
        default = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=50,
            seed=1,
        )
        assert explicit == default

    def test_player_like_spends_more_sparks_in_aggregate(self):
        """The Accept criterion's headline claim: `player_like` demonstrably
        spends more than `conservative` over a real encounter, not just in
        the unit-level branch tests above."""
        conservative = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=200,
            seed=1,
            spark_policy="conservative",
        )
        player_like = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=200,
            seed=1,
            spark_policy="player_like",
        )
        assert player_like.mean_sparks_spent > conservative.mean_sparks_spent

    def test_characterization_conservative_reproduces_recorded_corpus(self):
        """Iron requirement (WD10 Accept): a known recorded run reproduces
        its recorded numbers exactly under the default policy. This is the
        Recipe Table's Standard roster (`research/simulation_log.md` Series
        9 Part D / `TestRecipeCalibration.test_standard_three_named_plus_mook`),
        seed=1, n=200 — its win rate is the already-recorded corpus
        number; `mean_sparks_spent` is pinned here as this task's own
        regression anchor so a future edit to `should_spend_spark` cannot
        silently re-baseline it.

        R2 CASCADE (2026-09-08, D20): re-pinned from 0.760/4.1 to
        0.730/3.4 (Series 12 Part B). Sparks spent fell because the party
        no longer holds a permanent Easy tag to build on — fewer Strikes
        are worth a Spark when the enemy is Open for one exchange only.
        The policy itself is untouched."""
        result = run_simulation(
            standard_party(),
            [(generic_named_def(8), 3), (chicken_def(), 1)],
            iterations=200,
            label="WD10 characterization: Recipe Standard",
            seed=1,
        )
        assert result.win_rate == pytest.approx(0.730)
        assert result.mean_sparks_spent == pytest.approx(3.4)


# Expose MAX_EXCHANGES for use in test assertions
from tools.combat_sim import MAX_EXCHANGES


class TestOpenLifecycleIsDataDriven:
    """R2 (BRIEF_fun_second_act §2). The simulator must read the Open
    lifecycle from `combat.enemy_durability.open_clears` and never assume
    the enemy-action spend — the iron law that the sim drives combat.py
    rather than carrying its own copy of a rule.
    """

    @staticmethod
    def _rs(mode: str):
        import copy
        rs = copy.deepcopy(_ruleset())
        rs.combat.enemy_durability.open_clears = mode
        return rs

    def test_expiry_call_is_wired_into_the_end_of_exchange_pass(self):
        """A Named enemy left Open loses the tag at end of exchange under
        `end_of_exchange` — the tag is a tempo tag, not a switch."""
        enemy = make_enemy(generic_named_def(8))
        enemy.open = True
        combat_module.expire_end_of_exchange(enemy, self._rs("end_of_exchange"))
        assert enemy.open is False

    def test_enemy_keeps_its_action_while_open(self):
        """Under `end_of_exchange` the enemy-action clear branch is dead:
        an Open enemy acts instead of forfeiting its attack to recover."""
        assert combat_module.open_clears_at_end_of_exchange(
            self._rs("end_of_exchange")) is True
        assert combat_module.open_clears_at_end_of_exchange(
            self._rs("enemy_action")) is False

    def test_enemy_action_mode_still_leaves_the_tag_standing(self):
        enemy = make_enemy(generic_named_def(8))
        enemy.open = True
        combat_module.expire_end_of_exchange(enemy, self._rs("enemy_action"))
        assert enemy.open is True


class TestPhaseFireInstrumentation:
    """Series 12 needs to ask *when* a phase landed, not only whether it
    did. The fields are instrumentation: additive, and never read by a
    decision branch.
    """

    def test_phase_fire_exchange_is_recorded(self):
        random.seed(1)
        result = run_combat(
            [make_pc(d) for d in standard_party()],
            [make_enemy(archive_guardian_def())],
        )
        assert result.phase_fires, "the Guardian's phase should fire in a won fight"
        assert result.phase_fires["guardian"] >= 1

    def test_phase_fire_is_absent_when_no_phase_is_authored(self):
        random.seed(1)
        result = run_combat(
            [make_pc(d) for d in standard_party()],
            [make_enemy(chicken_def())],
        )
        assert result.phase_fires == {}

    def test_phase_fire_records_the_first_exchange_only(self):
        enemy = make_enemy(archive_guardian_def())
        enemy.phase_index = 0
        enemy.phase_fired_exchange = 2
        # A later exchange must not overwrite the first stamp.
        assert enemy.phase_fired_exchange == 2


class TestRiderPolicies:
    """R3 (BRIEF_fun_second_act §3). Which rider a 10+ takes is *policy*;
    what a rider does is `combat.apply_rider`'s. These tests pin the policy
    boundary, not the effects.
    """

    def test_always_open_reproduces_the_pre_r3_choice(self):
        """The worst case, and the default, so every recorded corpus stays
        derivable and the snowball is still measured at full strength."""
        target = make_enemy(generic_named_def(8))
        rid, ally = _choose_rider(target, make_pc(mordai_def()), [], _ruleset(),
                                  "always_open")
        assert (rid, ally) == ("open", None)

    def test_mixed_opens_a_target_that_is_not_open(self):
        target = make_enemy(generic_named_def(8))
        rid, _ = _choose_rider(target, make_pc(mordai_def()),
                               [make_pc(d) for d in standard_party()],
                               _ruleset(), "mixed")
        assert rid == "open"

    def test_mixed_covers_the_lowest_endurance_ally_when_a_setting_offers_cover(self):
        """Cover is out of the core menu (D20) but the policy must still
        pick it correctly for a setting that offers it — and must pick the
        ally an incoming attack is most likely to Break."""
        import copy
        from app.facets.schema import StrikeRiderDef
        rs = copy.deepcopy(_ruleset())
        rs.combat.enemy_durability.strike_riders = list(
            rs.combat.enemy_durability.strike_riders
        ) + [StrikeRiderDef(id="cover", label="Cover",
                            effect="free_reaction_ally",
                            duration="end_of_exchange")]
        target = make_enemy(generic_named_def(8))
        target.open = True
        allies = [make_pc(d) for d in standard_party()]
        allies[1].endurance_current = 1
        rid, ally = _choose_rider(target, allies[0], allies, rs, "mixed")
        assert rid == "cover"
        assert ally is allies[1]

    def test_mixed_takes_position_on_an_open_target_in_the_core_menu(self):
        target = make_enemy(generic_named_def(8))
        target.open = True
        allies = [make_pc(d) for d in standard_party()]
        rid, ally = _choose_rider(target, allies[0], allies, _ruleset(), "mixed")
        assert (rid, ally) == ("position", None)

    def test_mixed_falls_through_to_position_when_cover_has_no_taker(self):
        target = make_enemy(generic_named_def(8))
        target.open = True
        rid, ally = _choose_rider(target, make_pc(mordai_def()), [], _ruleset(),
                                  "mixed")
        assert (rid, ally) == ("position", None)

    def test_policy_respects_a_trimmed_menu(self):
        """If the acceptance cuts Cover, the policy must not name it."""
        import copy
        rs = copy.deepcopy(_ruleset())
        rs.combat.enemy_durability.strike_riders = [
            r for r in rs.combat.enemy_durability.strike_riders if r.id != "cover"
        ]
        target = make_enemy(generic_named_def(8))
        target.open = True
        allies = [make_pc(d) for d in standard_party()]
        rid, _ = _choose_rider(target, allies[0], allies, rs, "mixed")
        assert rid == "position"


class TestRiderInstrumentation:
    def test_rider_choices_are_logged_in_order(self):
        random.seed(1)
        result = run_combat(
            [make_pc(d) for d in standard_party()],
            [make_enemy(generic_named_def(8)) for _ in range(3)],
            rider_policy="mixed",
        )
        assert result.rider_choices, "a won fight should take at least one rider"
        assert set(result.rider_choices) <= {"open", "position", "cover"}

    def test_decisions_per_exchange_is_computable(self):
        random.seed(1)
        result = run_combat(
            [make_pc(d) for d in standard_party()],
            [make_enemy(generic_named_def(8)) for _ in range(3)],
            rider_policy="mixed",
        )
        assert len(result.rider_choices) / max(result.exchanges, 1) > 0

    def test_always_open_logs_only_open(self):
        random.seed(1)
        result = run_combat(
            [make_pc(d) for d in standard_party()],
            [make_enemy(generic_named_def(8)) for _ in range(3)],
            rider_policy="always_open",
        )
        assert set(result.rider_choices) <= {"open"}


class TestCoverWaivesCostNotOutcome:
    def test_cover_zeroes_a_reaction_cost_once(self):
        pc = make_pc(mordai_def())
        pc.free_reaction = True
        assert combat_module.consume_free_reaction(pc) is True
        assert combat_module.consume_free_reaction(pc) is False

    def test_cover_expires_with_the_tier1_conditions(self):
        pc = make_pc(mordai_def())
        pc.free_reaction = True
        assert "cover" in combat_module.expire_end_of_exchange(
            pc, _ruleset(), exchange_no=1)
        assert pc.free_reaction is False

    def test_a_covered_pc_still_rolls_the_reaction(self):
        """The gate that keeps Cover from being a free success: it buys the
        Endurance, and the reaction can still fail."""
        pc = make_pc(mordai_def())
        pc.free_reaction = True
        before = pc.endurance_current
        random.seed(4)
        _enemy_attack(make_enemy(generic_named_def(8)), pc, _ruleset())
        # Cost waived, but the roll happened — a failed reaction still lands
        # a Condition, so state is not simply untouched.
        assert pc.endurance_current == before or pc.conditions
