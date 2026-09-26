"""Monster cards (MM1) and the danger read — app/game/enemy.py, encounter.py (T4)."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from app.game.encounter import Encounter, EncounterEnemy, danger_read, foe_points
from app.game.enemy import Enemy, EnemyFormatError
from tests.conftest import make_enemy

REPO = Path(__file__).resolve().parents[2]
CARD_FILES = sorted((REPO / "enemies").glob("*.fof")) + sorted(
    (REPO / "adventures").glob("*/enemies/*.fof"))


def card_fof(**enemy) -> dict:
    body = {"level": 3, "role": "standard", "armor": 1, "morale": 8, "weapon": "Cudgel",
            "wants": "w", "special": "s", "when_bloodied": "wb", "tells": "t", "breaks": "b",
            "twists": [str(i) for i in range(6)]}
    body.update(enemy)
    return {"fof_version": "1.0", "type": "enemy", "id": "sgt", "name": "Sergeant",
            "ruleset": {"modules": [{"id": "base", "version": "1.0.0"}]}, "enemy": body}


class TestDerivedNumbers:
    def test_standard_uses_the_level_row(self, ruleset):
        e = make_enemy(level=3)
        assert (e.hp_max(ruleset), e.damage(ruleset), e.attack(ruleset), e.attacks(ruleset)) == (
            14, 6, 2, 1)

    def test_elite_doubles_hp_and_attacks_twice(self, ruleset):
        e = make_enemy(level=5, role="elite")
        assert e.hp_max(ruleset) == 40 and e.attacks(ruleset) == 2

    def test_boss_quintuples_hp_and_adds_damage(self, ruleset):
        e = make_enemy(level=10, role="boss")
        assert e.hp_max(ruleset) == 175 and e.damage(ruleset) == 15 and e.attacks(ruleset) == 2
        assert e.attack(ruleset) == 5

    def test_mook_has_no_hp_and_weaker_numbers(self, ruleset):
        e = make_enemy(level=1, role="mook")
        assert e.hp_max(ruleset) is None and e.damage(ruleset) == 3 and e.attack(ruleset) == 0

    def test_overrides_are_final_values(self, ruleset):
        e = make_enemy(level=1, role="mook", damage_override=1, attack_override=-1)
        assert e.damage(ruleset) == 1 and e.attack(ruleset) == -1
        assert e.overridden() == ["damage", "attack"]

    def test_hp_override(self, ruleset):
        assert make_enemy(level=2, hp_override=30).hp_max(ruleset) == 30

    def test_unknown_role_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_enemy(role="minion").damage(ruleset)

    def test_level_off_the_table_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_enemy(level=11).attack(ruleset)


class TestCard:
    def test_card_preview(self, ruleset):
        c = make_enemy(level=4, role="boss", morale=12).card(ruleset)
        assert c["hp"] == 85 and c["bloodied_phase"] and c["fearless"] and c["attacks"] == 2

    def test_mook_card_is_a_mob(self, ruleset):
        c = make_enemy(role="mook").card(ruleset)
        assert c["mob"] and c["mob_damage_cap"] == 4 and c["hp"] is None

    def test_card_lists_overrides(self, ruleset):
        assert make_enemy(attacks_override=3).card(ruleset)["overrides"] == ["attacks"]


class TestValidate:
    def test_complete_card_is_valid(self, ruleset):
        assert make_enemy().validate(ruleset) == []

    def test_twists_must_be_six(self, ruleset):
        e = make_enemy()
        e.twists = ["only one"]
        assert any("six twists" in m for m in e.validate(ruleset))

    def test_non_mook_needs_when_bloodied(self, ruleset):
        e = make_enemy()
        e.when_bloodied = None
        assert any("WHEN BLOODIED" in m for m in e.validate(ruleset))

    def test_armor_and_morale_ranges(self, ruleset):
        errs = make_enemy(armor=3, morale=13).validate(ruleset)
        assert any("armor" in m for m in errs) and any("morale" in m for m in errs)

    def test_blank_card_line(self, ruleset):
        e = make_enemy()
        e.special = " "
        assert any("SPECIAL" in m for m in e.validate(ruleset))


class TestSpawn:
    def test_spawn_sets_full_hp_and_key(self, ruleset):
        live = make_enemy(level=2).spawn(ruleset, key="a#1")
        assert live.hp_current == 11 and live.key == "a#1" and not live.defeated

    def test_spawn_is_a_copy(self, ruleset):
        base = make_enemy()
        live = base.spawn(ruleset)
        live.twists.append("x")
        assert len(base.twists) == 6

    def test_mook_mob(self, ruleset):
        assert make_enemy(role="mook").spawn(ruleset, count=5).count == 5

    def test_non_mook_mob_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_enemy().spawn(ruleset, count=2)

    def test_zero_count_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_enemy(role="mook").spawn(ruleset, count=0)


class TestFof:
    def test_from_fof_reads_a_card(self, ruleset):
        e = Enemy.from_fof(card_fof())
        assert e.level == 3 and e.armor == 1 and e.weapon == "Cudgel" and e.validate(ruleset) == []

    def test_round_trip(self):
        e = Enemy.from_fof(card_fof(damage=9, nastier="n"))
        again = Enemy.from_fof(e.to_fof())
        assert again.to_fof() == e.to_fof() and again.damage_override == 9

    def test_v03_card_is_refused_clearly(self):
        old = {"fof_version": "0.1", "type": "enemy", "id": "x",
               "enemy": {"tier": "named", "resolve": 3}}
        with pytest.raises(EnemyFormatError, match="v0.3"):
            Enemy.from_fof(old)

    def test_wrong_type_is_refused(self):
        with pytest.raises(EnemyFormatError):
            Enemy.from_fof({"type": "character"})

    def test_missing_level_is_refused(self):
        fof = card_fof()
        del fof["enemy"]["level"]
        with pytest.raises(EnemyFormatError, match="level"):
            Enemy.from_fof(fof)

    @pytest.mark.parametrize("path", CARD_FILES, ids=lambda p: f"{p.parent.parent.name}/{p.stem}")
    def test_every_shipped_card_loads_and_validates(self, ruleset, path):
        e = Enemy.from_fof(yaml.safe_load(path.read_text(encoding="utf-8")))
        assert e.validate(ruleset) == []

    def test_client_dict(self, ruleset):
        d = make_enemy().spawn(ruleset).to_client_dict(ruleset)
        assert d["card"]["hp"] == 8 and d["hp_current"] == 8 and d["twists"]
        assert "card" not in make_enemy().to_client_dict()


# ---------------------------------------------------------------------------
# Danger read (MM1, Table MM1–4)
# ---------------------------------------------------------------------------

class TestFoePoints:
    def test_role_points(self):
        assert [foe_points(r, 1, 1) for r in ("mook", "standard", "elite", "boss")] == [
            0.25, 1, 2, 4]

    def test_three_above_doubles_three_below_halves(self):
        assert foe_points("standard", 4, 1) == 2 and foe_points("standard", 1, 4) == 0.5
        assert foe_points("standard", 3, 1) == 1

    def test_unknown_role_raises(self):
        with pytest.raises(ValueError):
            foe_points("dragon", 1, 1)


class TestDangerRead:
    def test_four_mooks_is_a_skirmish(self):
        assert danger_read([("mook", 1, 4)], 4, 1)["read"] == "skirmish"

    def test_one_per_pc_is_a_real_fight(self):
        assert danger_read([("standard", 1, 4)], 4, 1)["read"] == "fight"

    def test_boss_against_four_is_a_fight_and_a_bigger_one_hard(self):
        assert danger_read([("boss", 1, 1)], 4, 1)["read"] == "fight"
        assert danger_read([("boss", 1, 1), ("standard", 1, 2)], 4, 1)["read"] == "hard"

    def test_above_one_and_a_half_is_deadly(self):
        d = danger_read([("elite", 1, 4)], 4, 1)
        assert d["read"] == "deadly" and d["points"] == 8 and d["per_pc"] == 2

    def test_mooks_round_up_per_four(self):
        assert danger_read([("mook", 1, 5)], 4, 1)["points"] == 2
        assert danger_read([("mook", 1, 3), ("mook", 1, 1)], 4, 1)["points"] == 1

    def test_counts_by_role(self):
        assert danger_read([("mook", 1, 3), ("mook", 2, 2)], 2, 1)["counts"] == {"mook": 5}

    def test_bad_inputs_raise(self):
        with pytest.raises(ValueError):
            danger_read([], 0, 1)
        with pytest.raises(ValueError):
            danger_read([("mook", 1, -1)], 2, 1)


class TestEncounter:
    def _lib(self):
        return {"thug": make_enemy(id="thug", role="mook"), "sgt": make_enemy(id="sgt", level=3)}

    def test_roster_and_danger(self):
        enc = Encounter(id="e", name="E", enemies=[EncounterEnemy("thug", 4),
                                                    EncounterEnemy("sgt", 1)])
        assert enc.roster(self._lib()) == [("mook", 1, 4), ("standard", 3, 1)]
        assert enc.danger(self._lib(), 4, 1)["points"] == 2      # 4 Mooks = 1, sergeant 1

    def test_missing_foes_are_listed_and_skipped(self):
        enc = Encounter(id="e", name="E", enemies=[EncounterEnemy("ghost", 1)])
        assert enc.missing(self._lib()) == ["ghost"] and enc.roster(self._lib()) == []

    def test_client_dict(self):
        enc = Encounter(id="e", name="E", enemies=[EncounterEnemy("thug", 2)],
                        lateral_solutions=["talk"])
        d = enc.to_client_dict()
        assert d["enemies"] == [{"enemy_id": "thug", "count": 2}] and d["lateral_solutions"] == ["talk"]
