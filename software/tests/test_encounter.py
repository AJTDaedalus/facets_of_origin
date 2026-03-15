"""Tests for the Encounter model — TR budget, action economy, serialization."""
import json
import pytest

from app.game.encounter import Encounter, EncounterEnemy


# ---------------------------------------------------------------------------
# Construction and defaults
# ---------------------------------------------------------------------------

class TestEncounterDefaults:
    def test_defaults(self):
        e = Encounter(id="test", name="Test Encounter")
        assert e.difficulty == "standard"
        assert e.enemies == []
        assert e.rewards_sparks == 0

    def test_with_enemies(self):
        e = Encounter(id="ambush", name="Ambush", enemies=[
            EncounterEnemy(enemy_id="thug", count=4),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        assert len(e.enemies) == 2
        assert e.total_enemy_count() == 5


# ---------------------------------------------------------------------------
# Difficulty multiplier
# ---------------------------------------------------------------------------

class TestDifficultyMultiplier:
    @pytest.mark.parametrize("diff,mult", [
        ("skirmish", 1.0),
        ("standard", 2.0),
        ("hard", 3.0),
        ("deadly", 4.0),
    ])
    def test_multipliers(self, diff, mult):
        assert Encounter.difficulty_multiplier(diff) == mult

    def test_unknown_difficulty_defaults_standard(self):
        assert Encounter.difficulty_multiplier("legendary") == 2.0


# ---------------------------------------------------------------------------
# Action economy multiplier
# ---------------------------------------------------------------------------

class TestActionEconomy:
    def test_solo(self):
        assert Encounter.action_economy_multiplier(1) == 0.75

    def test_small_group(self):
        assert Encounter.action_economy_multiplier(3) == 1.0

    def test_medium_group(self):
        assert Encounter.action_economy_multiplier(5) == 1.25

    def test_medium_group_mooks(self):
        assert Encounter.action_economy_multiplier(5, all_mooks=True) == 1.1

    def test_large_group(self):
        assert Encounter.action_economy_multiplier(8) == 1.5


# ---------------------------------------------------------------------------
# Budget calculation
# ---------------------------------------------------------------------------

class TestBudgetCalculation:
    def test_standard_budget(self):
        # 3 career advances * 2.0 = 6.0
        assert Encounter.calculate_budget(3, "standard") == 6.0

    def test_hard_budget(self):
        assert Encounter.calculate_budget(5, "hard") == 15.0

    def test_skirmish_budget(self):
        assert Encounter.calculate_budget(10, "skirmish") == 10.0


# ---------------------------------------------------------------------------
# Effective TR calculation
# ---------------------------------------------------------------------------

class TestEffectiveTR:
    def test_solo_named_enemy(self):
        e = Encounter(id="duel", name="Duel", enemies=[
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"sergeant": 8}
        # Solo: 8 * 0.75 = 6.0
        assert e.calculate_effective_tr(trs) == 6.0

    def test_group_of_mooks(self):
        e = Encounter(id="brawl", name="Brawl", enemies=[
            EncounterEnemy(enemy_id="thug", count=5),
        ])
        trs = {"thug": 1}
        # 5 mooks, all_mooks=True, medium group → 5 * 1.1 = 5.5
        assert e.calculate_effective_tr(trs) == 5.5

    def test_mixed_group(self):
        e = Encounter(id="ambush", name="Ambush", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"thug": 1, "sergeant": 8}
        # 4 enemies, not all mooks → raw = 3 + 8 = 11, * 1.25 = 13.75
        assert e.calculate_effective_tr(trs) == 13.75

    def test_unknown_enemy_id_treated_as_zero_tr(self):
        e = Encounter(id="mystery", name="Mystery", enemies=[
            EncounterEnemy(enemy_id="unknown_creature", count=2),
        ])
        assert e.calculate_effective_tr({}) == 0.0


# ---------------------------------------------------------------------------
# Tier-weighted effective TR (new simulation-calibrated formula)
# ---------------------------------------------------------------------------

class TestTierWeightedTR:
    def test_mook_weight_halves_tr(self):
        e = Encounter(id="mooks", name="Mooks", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
        ])
        trs = {"thug": 1}
        tiers = {"thug": "mook"}
        # 3 mooks × TR 1 × 0.5 weight × 1.0 group mod = 1.5
        assert e.calculate_effective_tr(trs, tiers) == 1.5

    def test_named_weight_is_one(self):
        e = Encounter(id="duel", name="Duel", enemies=[
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"sergeant": 8}
        tiers = {"sergeant": "named"}
        # 1 named × TR 8 × 1.0 weight × 1.0 group mod = 8.0
        assert e.calculate_effective_tr(trs, tiers) == 8.0

    def test_boss_weight_increases_tr(self):
        e = Encounter(id="boss", name="Boss Fight", enemies=[
            EncounterEnemy(enemy_id="guardian", count=1),
        ])
        trs = {"guardian": 16}
        tiers = {"guardian": "boss"}
        # 1 boss × TR 16 × 1.25 weight × 1.0 group mod = 20.0
        assert e.calculate_effective_tr(trs, tiers) == 20.0

    def test_mixed_group_with_tiers(self):
        e = Encounter(id="mixed", name="Mixed", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"thug": 1, "sergeant": 8}
        tiers = {"thug": "mook", "sergeant": "named"}
        # (3×1×0.5 + 1×8×1.0) × 1.1 (4 enemies) = 9.5 × 1.1 = 10.45
        assert e.calculate_effective_tr(trs, tiers) == pytest.approx(10.45)

    def test_large_group_modifier(self):
        e = Encounter(id="swarm", name="Swarm", enemies=[
            EncounterEnemy(enemy_id="thug", count=10),
        ])
        trs = {"thug": 1}
        tiers = {"thug": "mook"}
        # 10 mooks × 1 × 0.5 × 1.2 (7+ enemies) = 6.0
        assert e.calculate_effective_tr(trs, tiers) == 6.0

    def test_boss_plus_mooks(self):
        e = Encounter(id="boss-adds", name="Boss + Adds", enemies=[
            EncounterEnemy(enemy_id="boss", count=1),
            EncounterEnemy(enemy_id="minion", count=4),
        ])
        trs = {"boss": 12, "minion": 1}
        tiers = {"boss": "boss", "minion": "mook"}
        # (1×12×1.25 + 4×1×0.5) × 1.1 (5 enemies) = 17.0 × 1.1 = 18.7
        assert e.calculate_effective_tr(trs, tiers) == pytest.approx(18.7)

    def test_fallback_without_tiers_uses_legacy(self):
        """Without tier info, falls back to the legacy action economy path."""
        e = Encounter(id="legacy", name="Legacy", enemies=[
            EncounterEnemy(enemy_id="thug", count=5),
        ])
        trs = {"thug": 1}
        # Legacy: 5 × 1 × 1.1 (mook-only medium group) = 5.5
        assert e.calculate_effective_tr(trs) == 5.5


class TestGroupSizeModifier:
    def test_small(self):
        assert Encounter.group_size_modifier(1) == 1.0
        assert Encounter.group_size_modifier(3) == 1.0

    def test_medium(self):
        assert Encounter.group_size_modifier(4) == 1.1
        assert Encounter.group_size_modifier(6) == 1.1

    def test_large(self):
        assert Encounter.group_size_modifier(7) == 1.2
        assert Encounter.group_size_modifier(15) == 1.2


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

class TestEncounterSerialization:
    def test_to_fof_roundtrip(self):
        e = Encounter(
            id="archive-fight", name="Archive Battle",
            difficulty="hard", environment="Cramped stone basement",
            description="The guardian attacks.",
            enemies=[
                EncounterEnemy(enemy_id="guardian", count=1),
                EncounterEnemy(enemy_id="construct", count=3),
            ],
            lateral_solutions=["Disable sensory matrix", "Exploit shoulder weakness"],
            rewards_sparks=1,
            rewards_narrative="Access to restricted archive",
            notes="Designed above budget.",
        )
        fof = e.to_fof()
        loaded = Encounter.from_fof(fof)
        assert loaded.id == "archive-fight"
        assert loaded.difficulty == "hard"
        assert len(loaded.enemies) == 2
        assert loaded.enemies[0].enemy_id == "guardian"
        assert loaded.enemies[1].count == 3
        assert loaded.lateral_solutions == ["Disable sensory matrix", "Exploit shoulder weakness"]
        assert loaded.rewards_sparks == 1
        assert loaded.notes == "Designed above budget."

    def test_from_fof_wrong_type_raises(self):
        with pytest.raises(ValueError, match="Expected type 'encounter'"):
            Encounter.from_fof({"type": "character"})

    def test_from_fof_missing_encounter_block_raises(self):
        with pytest.raises(ValueError, match="Missing or invalid 'encounter'"):
            Encounter.from_fof({"type": "encounter"})

    def test_to_client_dict_is_json_safe(self):
        e = Encounter(id="test", name="Test")
        json.dumps(e.to_client_dict())

    def test_fof_includes_type(self):
        e = Encounter(id="test", name="Test")
        assert e.to_fof()["type"] == "encounter"
