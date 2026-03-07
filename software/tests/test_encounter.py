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
