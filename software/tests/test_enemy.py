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
        assert e.resolve == 0
        assert e.attack_modifier == 0
        assert e.armor == "none"
        assert e.techniques == []
        assert e.loot == []
        assert e.phases == []

    def test_named_npc(self):
        e = Enemy(id="sergeant", name="Sergeant", tier="named", resolve=3,
                  attack_modifier=2, defense_modifier=2, armor="light")
        assert e.tier == "named"
        assert e.resolve == 3

    def test_boss_npc(self):
        e = Enemy(id="guardian", name="Archive Guardian", tier="boss",
                  resolve=5, attack_modifier=3, special="Phase change at 50% Resolve")
        assert e.special == "Phase change at 50% Resolve"


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
        # offense=2, durability=0, armor=0, techniques=0 -> raw=2, min=1
        assert e.calculate_tr() == 2

    def test_mook_durability_is_zero_regardless_of_resolve(self):
        """A Mook's durability_value is always 0, even if `resolve` is set."""
        e = Enemy(id="chicken", name="Chicken", tier="mook",
                  resolve=5, attack_modifier=0)
        # offense=2, durability=0 (mook, resolve ignored), armor=0 -> raw=2
        assert e.calculate_tr() == 2

    def test_named_npc_tr_sergeant_preserved(self):
        """City Watch Sergeant: attack +2 -> offense 4, resolve 3, light -> 1 = 8 (TR preserved from v0.2)."""
        e = Enemy(id="sergeant", name="Sergeant", tier="named",
                  resolve=3, attack_modifier=2, armor="light")
        assert e.calculate_tr() == 8

    def test_named_npc_tr_veteran_soldier_preserved(self):
        """Veteran Soldier: attack +3 -> offense 5, resolve 4, light -> 1 = 10 (TR preserved from v0.2)."""
        e = Enemy(id="veteran_soldier", name="Veteran Soldier", tier="named",
                  resolve=4, attack_modifier=3, armor="light")
        assert e.calculate_tr() == 10

    def test_boss_archive_guardian_recomputes_to_14(self):
        """Archive Guardian: offense(3->5) + resolve(5) + armor(heavy->2) + technique_bonus(2) = 14.

        Was published as 16 under the old formula, which double-counted the
        phase-change special as both a durability and a technique bonus.
        """
        e = Enemy(id="guardian", name="Archive Guardian", tier="boss",
                  resolve=5, attack_modifier=3, armor="heavy",
                  techniques=["phase_change", "tier1_immunity"])
        assert e.calculate_tr() == 14

    def test_named_minimum_enforced(self):
        """Named NPC with low stats still gets TR >= 8."""
        e = Enemy(id="weak_named", name="Weak Named", tier="named",
                  resolve=1, attack_modifier=-1, armor="none")
        assert e.calculate_tr() >= 8

    def test_boss_minimum_enforced(self):
        """Boss always has TR >= 12."""
        e = Enemy(id="boss", name="Boss", tier="boss",
                  resolve=2, attack_modifier=0)
        assert e.calculate_tr() >= 12

    def test_boss_high_stats(self):
        e = Enemy(id="dragon", name="Dragon", tier="boss",
                  resolve=7, attack_modifier=4, armor="heavy",
                  techniques=["fire_breath", "tail_sweep", "frightful_presence"])
        tr = e.calculate_tr()
        # offense=6, durability=7, armor=2, techniques=3 -> raw=18
        assert tr == 18

    def test_techniques_add_to_tr(self):
        e = Enemy(id="elite", name="Elite", tier="named",
                  resolve=3, attack_modifier=2, armor="light",
                  techniques=["shield_wall"])
        assert e.calculate_tr() == 9  # base 8 + 1 technique

    def test_heavy_armor_bonus(self):
        e = Enemy(id="knight", name="Knight", tier="named",
                  resolve=4, attack_modifier=2, armor="heavy")
        # offense=4, durability=4, armor=2, techniques=0 -> raw=10
        assert e.calculate_tr() == 10


# ---------------------------------------------------------------------------
# Combat tracker state
# ---------------------------------------------------------------------------

class TestEnemyCombatTracker:
    def test_init_combat_named(self):
        e = Enemy(id="sgt", name="Sgt", tier="named", resolve=3)
        e.init_combat()
        assert e.resolve_current == 3
        assert e.conditions == []

    def test_init_combat_mook(self):
        e = Enemy(id="thug", name="Thug", tier="mook")
        e.init_combat()
        assert e.resolve_current == 0

    def test_init_combat_boss(self):
        e = Enemy(id="boss", name="Boss", tier="boss", resolve=5)
        e.init_combat()
        assert e.resolve_current == 5

    def test_init_combat_light_armor_adds_one_resolve(self):
        e = Enemy(id="sgt", name="Sgt", tier="named", resolve=3, armor="light")
        e.init_combat()
        assert e.resolve_current == 4

    def test_init_combat_heavy_armor_adds_two_resolve(self):
        e = Enemy(id="boss", name="Boss", tier="boss", resolve=5, armor="heavy")
        e.init_combat()
        assert e.resolve_current == 7

    def test_init_combat_mook_armor_grants_no_resolve(self):
        e = Enemy(id="thug", name="Thug", tier="mook", armor="heavy")
        e.init_combat()
        assert e.resolve_current == 0


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

    def test_to_fof_named_includes_resolve(self):
        e = Enemy(id="sgt", name="Sergeant", tier="named", resolve=3)
        fof = e.to_fof()
        assert fof["enemy"]["resolve"] == 3

    def test_to_fof_mook_omits_resolve(self):
        e = Enemy(id="thug", name="Thug", tier="mook")
        fof = e.to_fof()
        assert "resolve" not in fof["enemy"]

    def test_to_fof_includes_tr(self):
        e = Enemy(id="sgt", name="Sergeant", tier="named",
                  resolve=3, attack_modifier=2, armor="light")
        fof = e.to_fof()
        assert fof["enemy"]["tr"] == 8

    def test_resolve_key_roundtrips_without_warning(self, recwarn):
        e = Enemy(id="sgt", name="Sergeant", tier="named", resolve=4)
        fof = e.to_fof()
        loaded = Enemy.from_fof(fof)
        assert loaded.resolve == 4
        assert not any(issubclass(w.category, DeprecationWarning) for w in recwarn.list)

    def test_from_fof_legacy_endurance_maps_and_warns(self):
        """A legacy `endurance` key (no `resolve`) maps through the v0.1->v0.2 table and warns."""
        fof = {
            "type": "enemy",
            "id": "sergeant",
            "name": "Sergeant",
            "enemy": {"tier": "named", "endurance": 6, "attack_modifier": 2, "armor": "light"},
        }
        with pytest.warns(DeprecationWarning):
            loaded = Enemy.from_fof(fof)
        assert loaded.resolve == 3
        assert loaded.calculate_tr() == 8

    @pytest.mark.parametrize("legacy_endurance,expected_resolve", [
        (1, 1), (2, 1),
        (3, 2), (4, 2),
        (5, 3), (6, 3),
        (7, 4), (8, 4),
        (9, 5), (10, 5),
        (11, 6), (12, 6),
        (13, 7), (20, 7),
    ])
    def test_legacy_endurance_mapping_table(self, legacy_endurance, expected_resolve):
        fof = {
            "type": "enemy",
            "id": "x",
            "name": "X",
            "enemy": {"tier": "named", "endurance": legacy_endurance},
        }
        with pytest.warns(DeprecationWarning):
            loaded = Enemy.from_fof(fof)
        assert loaded.resolve == expected_resolve

    def test_from_fof_resolve_present_ignores_legacy_endurance(self):
        """When both keys are present, `resolve` wins and no warning fires."""
        fof = {
            "type": "enemy",
            "id": "x",
            "name": "X",
            "enemy": {"tier": "named", "resolve": 9, "endurance": 1},
        }
        loaded = Enemy.from_fof(fof)
        assert loaded.resolve == 9

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


# ---------------------------------------------------------------------------
# Phase changes
# ---------------------------------------------------------------------------

class TestEnemyPhases:
    def test_phases_default_empty(self):
        e = Enemy(id="boss", name="Boss", tier="boss", resolve=5)
        assert e.phases == []

    def test_phases_accept_resolve_threshold_and_description(self):
        e = Enemy(id="guardian", name="Archive Guardian", tier="boss", resolve=5,
                  phases=[{"resolve_threshold": 2, "description": "Reduced Mode."}])
        assert e.phases[0].resolve_threshold == 2
        assert e.phases[0].description == "Reduced Mode."

    def test_phases_roundtrip_through_fof(self):
        e = Enemy(id="guardian", name="Archive Guardian", tier="boss", resolve=5,
                  phases=[{"resolve_threshold": 2, "description": "Reduced Mode."}])
        fof = e.to_fof()
        loaded = Enemy.from_fof(fof)
        assert len(loaded.phases) == 1
        assert loaded.phases[0].resolve_threshold == 2
        assert loaded.phases[0].description == "Reduced Mode."
