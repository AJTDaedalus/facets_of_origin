"""Tests for the Enemy model — TR calculation, serialization, combat tracker."""
import pytest
import yaml

from app.game.enemy import Enemy


# ---------------------------------------------------------------------------
# Construction and defaults
# ---------------------------------------------------------------------------

class TestEnemyDefaults:
    def test_mook_defaults(self):
        e = Enemy(id="thug", name="Harbor Thug")
        assert e.tier == "mook"
        assert e.endurance == 0
        assert e.attack_modifier == 0
        assert e.armor == "none"
        assert e.techniques == []
        assert e.loot == []

    def test_named_npc(self):
        e = Enemy(id="sergeant", name="Sergeant", tier="named", endurance=6,
                  attack_modifier=2, defense_modifier=2, armor="light")
        assert e.tier == "named"
        assert e.endurance == 6

    def test_boss_npc(self):
        e = Enemy(id="guardian", name="Archive Guardian", tier="boss",
                  endurance=10, attack_modifier=3, special="Phase change at 50% Endurance")
        assert e.special == "Phase change at 50% Endurance"


# ---------------------------------------------------------------------------
# TR Calculation (matches MM1 formula)
# ---------------------------------------------------------------------------

class TestTRCalculation:
    def test_mook_minimum_tr(self):
        """Mooks always have TR >= 1 regardless of stats."""
        e = Enemy(id="chicken", name="Chicken", tier="mook",
                  attack_modifier=-2)
        assert e.calculate_tr() == 1

    def test_mook_with_positive_attack(self):
        e = Enemy(id="thug", name="Thug", tier="mook", attack_modifier=0)
        # offense=2, durability=0, armor=0, techniques=0 → raw=2, min=1
        assert e.calculate_tr() == 2

    def test_named_npc_tr(self):
        """City Watch Sergeant: attack +2 → offense 4, endurance 6 → durability 3, light → 1 = 8."""
        e = Enemy(id="sergeant", name="Sergeant", tier="named",
                  endurance=6, attack_modifier=2, armor="light")
        assert e.calculate_tr() == 8

    def test_named_minimum_enforced(self):
        """Named NPC with low stats still gets TR >= 8."""
        e = Enemy(id="weak_named", name="Weak Named", tier="named",
                  endurance=2, attack_modifier=-1, armor="none")
        assert e.calculate_tr() >= 8

    def test_boss_minimum_enforced(self):
        """Boss always has TR >= 12."""
        e = Enemy(id="boss", name="Boss", tier="boss",
                  endurance=4, attack_modifier=0)
        assert e.calculate_tr() >= 12

    def test_boss_high_stats(self):
        e = Enemy(id="dragon", name="Dragon", tier="boss",
                  endurance=14, attack_modifier=4, armor="heavy",
                  techniques=["fire_breath", "tail_sweep", "frightful_presence"])
        tr = e.calculate_tr()
        # offense=6, durability=7, armor=2, techniques=3 → raw=18
        assert tr == 18

    def test_techniques_add_to_tr(self):
        e = Enemy(id="elite", name="Elite", tier="named",
                  endurance=6, attack_modifier=2, armor="light",
                  techniques=["shield_wall"])
        assert e.calculate_tr() == 9  # base 8 + 1 technique

    def test_heavy_armor_bonus(self):
        e = Enemy(id="knight", name="Knight", tier="named",
                  endurance=8, attack_modifier=2, armor="heavy")
        # offense=4, durability=4, armor=2, techniques=0 → raw=10
        assert e.calculate_tr() == 10


# ---------------------------------------------------------------------------
# Combat tracker state
# ---------------------------------------------------------------------------

class TestEnemyCombatTracker:
    def test_init_combat_named(self):
        e = Enemy(id="sgt", name="Sgt", tier="named", endurance=6)
        e.init_combat()
        assert e.endurance_current == 6
        assert e.conditions == []

    def test_init_combat_mook(self):
        e = Enemy(id="thug", name="Thug", tier="mook")
        e.init_combat()
        assert e.endurance_current == 0

    def test_init_combat_boss(self):
        e = Enemy(id="boss", name="Boss", tier="boss", endurance=10)
        e.init_combat()
        assert e.endurance_current == 10


# ---------------------------------------------------------------------------
# Serialization: to_fof / from_fof
# ---------------------------------------------------------------------------

class TestEnemySerialization:
    def test_to_fof_roundtrip(self):
        e = Enemy(id="thug", name="Harbor Thug", tier="mook",
                  attack_modifier=0, description="A hired thug.",
                  tactics="Fights dirty.", personality="Cowardly.")
        fof = e.to_fof()
        loaded = Enemy.from_fof(fof)
        assert loaded.id == "thug"
        assert loaded.name == "Harbor Thug"
        assert loaded.tier == "mook"
        assert loaded.tactics == "Fights dirty."
        assert loaded.personality == "Cowardly."

    def test_to_fof_named_includes_endurance(self):
        e = Enemy(id="sgt", name="Sergeant", tier="named", endurance=6)
        fof = e.to_fof()
        assert fof["enemy"]["endurance"] == 6

    def test_to_fof_mook_omits_endurance(self):
        e = Enemy(id="thug", name="Thug", tier="mook")
        fof = e.to_fof()
        assert "endurance" not in fof["enemy"]

    def test_to_fof_includes_tr(self):
        e = Enemy(id="sgt", name="Sergeant", tier="named",
                  endurance=6, attack_modifier=2, armor="light")
        fof = e.to_fof()
        assert fof["enemy"]["tr"] == 8

    def test_from_fof_wrong_type_raises(self):
        with pytest.raises(ValueError, match="Expected type 'enemy'"):
            Enemy.from_fof({"type": "character", "enemy": {}})

    def test_from_fof_missing_enemy_block_raises(self):
        with pytest.raises(ValueError, match="Missing or invalid 'enemy'"):
            Enemy.from_fof({"type": "enemy"})

    def test_from_fof_loads_existing_enemy_file(self):
        """Load the canonical harbor_thug.fof file."""
        from pathlib import Path
        fof_path = Path(__file__).parent.parent.parent / "enemies" / "harbor_thug.fof"
        if fof_path.exists():
            fof_dict = yaml.safe_load(fof_path.read_text())
            e = Enemy.from_fof(fof_dict)
            assert e.id == "harbor_thug"
            assert e.tier == "mook"
            assert e.calculate_tr() >= 1

    def test_to_client_dict_is_json_safe(self):
        import json
        e = Enemy(id="thug", name="Thug")
        json.dumps(e.to_client_dict())

    def test_loot_roundtrips(self):
        e = Enemy(id="bandit", name="Bandit", tier="mook",
                  loot=["Gold Coin", "Rusty Dagger"])
        fof = e.to_fof()
        loaded = Enemy.from_fof(fof)
        assert loaded.loot == ["Gold Coin", "Rusty Dagger"]
