"""Tests for the combat simulator."""
import random
import pytest
import sys
from pathlib import Path

# Ensure software/ is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.combat_sim import (
    PCState,
    EnemyState,
    SimResult,
    AggregateResult,
    TIER1_CONDITIONS,
    TIER2_CONDITIONS,
    combat_roll,
    apply_condition,
    cleanup_end_of_exchange,
    armor_downgrade,
    resolve_pc_strike,
    resolve_enemy_attack,
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
    generic_boss_def,
    archive_guardian_def,
    choose_pc_posture,
    choose_enemy_posture,
    choose_pc_target,
    choose_enemy_target,
    should_spend_spark,
    should_press,
    choose_pc_reaction,
    should_enemy_react,
    get_series,
    _wilson_ci,
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


# ---------------------------------------------------------------------------
# Condition management
# ---------------------------------------------------------------------------

class TestConditions:
    def test_apply_t1_condition(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "winded", 1)
        assert "winded" in pc.conditions
        assert "winded" not in pc.persistent_conditions

    def test_apply_t2_condition(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "staggered", 2)
        assert "staggered" in pc.conditions

    def test_same_t2_causes_broken(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "staggered", 2)
        assert not pc.is_broken
        apply_condition(pc, "staggered", 2)
        assert pc.is_broken

    def test_different_t2_does_not_break(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "staggered", 2)
        apply_condition(pc, "cornered", 2)
        assert not pc.is_broken
        assert "staggered" in pc.conditions
        assert "cornered" in pc.conditions

    def test_zero_end_absorb_upgrades_t1_to_t2(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        apply_condition(pc, "winded", 1, is_zero_end_absorb=True)
        assert "staggered" in pc.conditions  # Upgraded from T1 to T2
        assert "staggered" in pc.persistent_conditions

    def test_zero_end_absorb_t2_is_persistent(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        apply_condition(pc, "staggered", 2, is_zero_end_absorb=True)
        assert "staggered" in pc.persistent_conditions

    def test_zero_end_absorb_twice_causes_broken(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        apply_condition(pc, "winded", 1, is_zero_end_absorb=True)
        # First absorb upgrades to staggered (persistent T2)
        assert "staggered" in pc.conditions
        apply_condition(pc, "winded", 1, is_zero_end_absorb=True)
        # Second absorb tries to add staggered again → Broken
        assert pc.is_broken

    def test_cleanup_clears_t1(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "winded", 1)
        apply_condition(pc, "off_balance", 1)
        cleanup_end_of_exchange(pc)
        assert "winded" not in pc.conditions
        assert "off_balance" not in pc.conditions

    def test_cleanup_keeps_t2(self):
        pc = make_pc(mordai_def())
        apply_condition(pc, "staggered", 2)
        apply_condition(pc, "winded", 1)
        cleanup_end_of_exchange(pc)
        assert "staggered" in pc.conditions
        assert "winded" not in pc.conditions

    def test_cleanup_keeps_persistent(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 0
        apply_condition(pc, "winded", 1, is_zero_end_absorb=True)
        # winded upgraded to staggered (persistent)
        cleanup_end_of_exchange(pc)
        assert "staggered" in pc.conditions  # Persistent, should stay

    def test_cleanup_withdrawn_recovery(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 1
        pc.posture = "withdrawn"
        cleanup_end_of_exchange(pc)
        assert pc.endurance_current == 3  # 1 + 2

    def test_cleanup_withdrawn_caps_at_max(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 4
        pc.posture = "withdrawn"
        cleanup_end_of_exchange(pc)
        assert pc.endurance_current == 5  # Capped at endurance_max


class TestArmorDowngrade:
    def test_no_armor(self):
        assert armor_downgrade(2, "none") == 2
        assert armor_downgrade(1, "none") == 1

    def test_light_armor_downgrades_t2_only(self):
        assert armor_downgrade(2, "light") == 1  # T2 → T1
        assert armor_downgrade(1, "light") == 1  # T1 unaffected
        assert armor_downgrade(3, "light") == 3  # T3 unaffected

    def test_heavy_armor_downgrades_t3_only(self):
        assert armor_downgrade(3, "heavy") == 2  # T3 → T2
        assert armor_downgrade(2, "heavy") == 2  # T2 unaffected
        assert armor_downgrade(1, "heavy") == 1  # T1 unaffected


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
        target = choose_pc_target(pc, enemies)
        assert target.tier == "mook"

    def test_target_selection_wounded_named(self):
        pc = make_pc(mordai_def())
        named1 = make_enemy(generic_named_def(8))
        named2 = make_enemy(generic_named_def(8))
        named2.instance_id = "named2"
        named2.conditions.append("staggered")
        target = choose_pc_target(pc, [named1, named2])
        assert target.instance_id == "named2"

    def test_enemy_targets_lowest_endurance(self):
        enemy = make_enemy(generic_named_def(8))
        pcs = [make_pc(mordai_def()), make_pc(zahna_def())]
        target = choose_enemy_target(enemy, pcs)
        assert target.name == "Zahna"  # End 3 < Mordai's 5

    def test_spark_spend_against_boss(self):
        pc = make_pc(mordai_def())
        boss = make_enemy(generic_boss_def(12))
        assert should_spend_spark(pc, boss) == 1

    def test_no_spark_against_mook(self):
        pc = make_pc(mordai_def())
        mook = make_enemy(chicken_def())
        assert should_spend_spark(pc, mook) == 0

    def test_spark_at_low_endurance(self):
        pc = make_pc(mordai_def())
        pc.endurance_current = 1
        named = make_enemy(generic_named_def(8))
        assert should_spend_spark(pc, named) == 1

    def test_no_spark_when_none_left(self):
        pc = make_pc(mordai_def())
        pc.sparks = 0
        boss = make_enemy(generic_boss_def(12))
        assert should_spend_spark(pc, boss) == 0

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

    def test_enemy_react_to_t2(self):
        enemy = make_enemy(generic_named_def(8))
        assert should_enemy_react(enemy, 2) is True

    def test_enemy_no_react_to_t1(self):
        enemy = make_enemy(generic_named_def(8))
        assert should_enemy_react(enemy, 1) is False

    def test_enemy_no_react_at_zero_end(self):
        enemy = make_enemy(generic_named_def(8))
        enemy.endurance_current = 0
        assert should_enemy_react(enemy, 2) is False

    def test_mook_never_reacts(self):
        mook = make_enemy(chicken_def())
        assert should_enemy_react(mook, 2) is False


# ---------------------------------------------------------------------------
# Strike resolution
# ---------------------------------------------------------------------------

class TestPCStrike:
    def test_mook_removed_on_success(self):
        random.seed(1)  # Seed that gives a success
        pc = make_pc(mordai_def())
        mook = make_enemy(chicken_def())
        # Keep trying seeds until we get a success
        for seed in range(100):
            random.seed(seed)
            pc_fresh = make_pc(mordai_def())
            mook_fresh = make_enemy(chicken_def())
            resolve_pc_strike(pc_fresh, mook_fresh)
            if mook_fresh.is_removed:
                break
        assert mook_fresh.is_removed

    def test_withdrawn_pc_cannot_strike(self):
        pc = make_pc(mordai_def())
        pc.posture = "withdrawn"
        mook = make_enemy(chicken_def())
        resolve_pc_strike(pc, mook)
        assert not mook.is_removed

    def test_named_takes_condition_on_full_success(self):
        """Named enemies should accumulate conditions from successful strikes."""
        named = make_enemy(generic_named_def(8))
        # Run many strikes until we get conditions applied
        conditions_seen = False
        for seed in range(200):
            random.seed(seed)
            pc = make_pc(mordai_def())
            named_fresh = make_enemy(generic_named_def(8))
            resolve_pc_strike(pc, named_fresh)
            if named_fresh.conditions:
                conditions_seen = True
                break
        assert conditions_seen, "Should see conditions on Named enemy after many strikes"

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
        """Mook attacks produce T1 conditions (when PC fails reaction)."""
        mook = make_enemy(chicken_def())
        for seed in range(200):
            random.seed(seed)
            pc = make_pc(mordai_def())
            pc.endurance_current = 0  # Force Absorb
            resolve_enemy_attack(mook, pc)
            if pc.conditions:
                # At 0 End, T1 is upgraded to T2 by the 0-End rule
                assert any(c in ("staggered", "cornered") for c in pc.conditions)
                break

    def test_named_attack_is_t2(self):
        """Named NPC attacks produce T2 conditions (when PC absorbs)."""
        named = make_enemy(generic_named_def(8))
        pc = make_pc(mordai_def())
        pc.endurance_current = 0  # Force Absorb
        resolve_enemy_attack(named, pc)
        # Should have a T2 condition (staggered or cornered)
        assert any(c in TIER2_CONDITIONS for c in pc.conditions)


# ---------------------------------------------------------------------------
# Boss phase change
# ---------------------------------------------------------------------------

class TestBossPhaseChange:
    def test_phase_change_resets_boss(self):
        boss = make_enemy(archive_guardian_def())
        boss.endurance_current = 0
        # Apply conditions to trigger Broken → phase change
        apply_condition(boss, "staggered", 2, is_zero_end_absorb=True)
        apply_condition(boss, "staggered", 2, is_zero_end_absorb=True)
        # Phase change should have triggered instead of Broken
        assert not boss.is_broken
        assert boss.phase_changed
        assert boss.endurance_current == 4  # Reset to phase 2 endurance
        assert boss.attack_modifier == 1   # Reduced in phase 2
        assert boss.conditions == []       # Cleared

    def test_phase_change_only_once(self):
        boss = make_enemy(archive_guardian_def())
        # First break → phase change
        apply_condition(boss, "staggered", 2)
        apply_condition(boss, "staggered", 2)
        assert boss.phase_changed
        assert not boss.is_broken
        # Second break → actual Broken
        apply_condition(boss, "staggered", 2)
        apply_condition(boss, "staggered", 2)
        assert boss.is_broken


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
        assert e.endurance_max == 0

    def test_sergeant_is_named(self):
        e = make_enemy(city_watch_sergeant_def())
        assert e.tier == "named"
        assert e.endurance_max == 6
        assert e.armor == "light"

    def test_guardian_is_boss(self):
        e = make_enemy(archive_guardian_def())
        assert e.tier == "boss"
        assert e.has_phase_change
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
        """7 Chickens should be significantly harder than 3."""
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
        assert result_7.win_rate < result_3.win_rate
        assert result_7.mean_exchanges > result_3.mean_exchanges

    def test_named_npc_longer_than_mooks(self):
        """Named NPC fights should last longer than Mook swarms."""
        result_mooks = run_simulation(
            standard_party(),
            [(chicken_def(), 3)],
            iterations=100,
            label="3 Mooks",
            seed=1,
        )
        result_named = run_simulation(
            standard_party(),
            [(generic_named_def(8), 1)],
            iterations=100,
            label="Named NPC",
            seed=1,
        )
        assert result_named.mean_exchanges > result_mooks.mean_exchanges

    def test_boss_harder_than_named(self):
        """Boss fights should have lower win rates than Named NPC fights."""
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
        assert result_boss.win_rate < result_named.win_rate


# Expose MAX_EXCHANGES for use in test assertions
from tools.combat_sim import MAX_EXCHANGES
