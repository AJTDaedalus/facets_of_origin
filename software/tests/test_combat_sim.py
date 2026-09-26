"""The combat simulator drives combat.py only, and the DESIGN §6 pacing ladder (T5)."""
from __future__ import annotations

import inspect
import random

import pytest

import tools.combat_sim as sim
from tools.combat_sim import (
    build_character, build_party, generic_foe, ladder, parse_foes, run_fight, simulate,
)


class TestNoPrivateRules:
    def test_simulator_imports_the_rules_modules(self):
        src = inspect.getsource(sim)
        assert "from app.game import combat" in src
        assert "resolve_attack" in src and "resolve_enemy_attack" in src

    def test_simulator_never_rolls_2d6_itself(self):
        """Every roll goes through combat/magic/character: no randint in the sim."""
        assert "randint" not in inspect.getsource(sim)

    def test_simulator_carries_no_threshold_numbers(self):
        src = inspect.getsource(sim)
        for rule in (">= 10", ">= 7", "armor.cap", "mob_damage"):
            assert rule not in src


class TestBuilding:
    def test_party_levels_up_through_the_engine(self, ruleset):
        party = build_party(ruleset, 5)
        assert [c.level for c in party] == [5, 5, 5, 5]
        assert all(c.signature for c in party)
        assert party[2].magic and len(party[2].magic.signature_workings) == 3

    def test_level_one_party_has_class_hp(self, ruleset):
        party = build_party(ruleset, 1)
        assert [c.hp_max(ruleset) for c in party] == [16, 12, 6, 9]

    def test_bad_spec_raises(self, ruleset):
        with pytest.raises(ValueError):
            build_character(ruleset, {"name": "X", "facet": "body", "second_stat": "body",
                                      "class_id": "warrior"}, 1)

    def test_parse_foes_makes_mobs_and_singles(self, ruleset):
        foes = parse_foes(ruleset, "mook:1x4,standard:2x2")
        assert [(f.role, f.count) for f in foes] == [("mook", 4), ("standard", 1), ("standard", 1)]
        assert len({f.key for f in foes}) == 3

    def test_parse_foes_reads_a_card(self, ruleset):
        (f,) = parse_foes(ruleset, "card:city_watch_sergeant")
        assert f.name == "City Watch Sergeant" and f.hp_current == 14

    def test_generic_foe_is_a_valid_card(self, ruleset):
        assert generic_foe("boss", 3).validate(ruleset) == []


class TestRunFight:
    def test_fight_ends_with_a_winner(self, ruleset):
        r = run_fight(ruleset, build_party(ruleset, 1), parse_foes(ruleset, "mook:1x4"),
                      random.Random(1))
        assert r.won and 1 <= r.exchanges <= sim.MAX_EXCHANGES

    def test_overwhelming_foes_win(self, ruleset):
        r = run_fight(ruleset, build_party(ruleset, 1), parse_foes(ruleset, "boss:10x3"),
                      random.Random(2))
        assert not r.won and r.pcs_down == 4

    def test_log_records_actions(self, ruleset):
        r = run_fight(ruleset, build_party(ruleset, 1), parse_foes(ruleset, "standard:1"),
                      random.Random(3))
        assert r.log and any("attacks" in line or "casts" in line for line in r.log)

    def test_simulate_is_deterministic_with_a_seed(self, ruleset):
        a = simulate(1, "standard:1x2", trials=30, seed=7, ruleset=ruleset)
        b = simulate(1, "standard:1x2", trials=30, seed=7, ruleset=ruleset)
        assert a == b and 0 <= a.win_rate <= 1

    def test_cli_runs(self, capsys):
        assert sim.main(["--level", "1", "--foes", "mook:1x2", "--trials", "5"]) == 0
        assert "win" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# DESIGN §6 pacing: 4 Mooks trivial; mixed standard fights 2-4 exchanges;
# a Boss dangerous — at levels 1, 5 and 10.
# ---------------------------------------------------------------------------

TRIALS = 300


@pytest.fixture(scope="module")
def results(ruleset):
    out = {}
    for level in (1, 5, 10):
        for name, foes in ladder(level).items():
            out[(level, name)] = simulate(level, foes, trials=TRIALS, seed=11, ruleset=ruleset)
    return out


@pytest.mark.parametrize("level", [1, 5, 10])
class TestPacingLadder:
    def test_four_mooks_are_trivial(self, results, level):
        s = results[(level, "trivial")]
        assert s.win_rate == 1.0 and s.mean_exchanges <= 2 and s.mean_pcs_down < 0.05

    def test_mixed_standard_fight_takes_two_to_four_exchanges(self, results, level):
        s = results[(level, "standard")]
        assert 2 <= s.mean_exchanges <= 4 and s.win_rate >= 0.9

    def test_a_boss_costs_more_than_a_standard_fight(self, results, level):
        boss, std = results[(level, "boss")], results[(level, "standard")]
        assert boss.mean_hp_lost > std.mean_hp_lost

    def test_a_same_level_boss_is_dangerous(self, results, level):
        """DESIGN §6: a lone Boss at the party's level drops a PC in a real share
        of fights (tuned 2026-09-25: Boss ×5 HP, +2 damage, +1 attack; damage 3 + level)."""
        assert results[(level, "boss")].any_down_rate >= 0.25
