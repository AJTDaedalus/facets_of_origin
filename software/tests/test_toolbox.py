"""Tests for app/game/toolbox.py — the MM toolbox (MM6)."""
import random

import pytest

from app.facets.registry import MergedRuleset
from app.game import toolbox as tb


@pytest.fixture(scope="module")
def bare_ruleset(ruleset):
    """The core ruleset with no MM tables loaded."""
    files = [f.model_copy(update={"loaded_tables": [], "tables": []}) for f in ruleset._files]
    return MergedRuleset(files)


# --- roll_die -------------------------------------------------------------

class TestRollDie:
    def test_d66_reads_tens_then_units(self):
        rng = random.Random(1)
        for _ in range(200):
            v = tb.roll_die("d66", rng)
            assert 1 <= v // 10 <= 6 and 1 <= v % 10 <= 6

    def test_2d6_range(self):
        rng = random.Random(2)
        vals = {tb.roll_die("2d6", rng) for _ in range(500)}
        assert min(vals) >= 2 and max(vals) <= 12 and len(vals) > 5

    @pytest.mark.parametrize("die,top", [("1d6", 6), ("1d8", 8), ("1d12", 12), ("1d20", 20)])
    def test_single_die_range(self, die, top):
        rng = random.Random(3)
        vals = [tb.roll_die(die, rng) for _ in range(300)]
        assert min(vals) >= 1 and max(vals) <= top

    def test_unknown_die_raises(self):
        with pytest.raises(ValueError):
            tb.roll_die("3d7")


# --- roll_table -----------------------------------------------------------

class TestRollTable:
    def test_fixed_roll_reads_the_range_entry(self, ruleset):
        res = tb.roll_table(ruleset, "reaction", roll=3)
        assert res["entry_roll"] == "2-4"
        assert res["roll"] == 3 and res["die"] == "2d6"
        assert res["text"]

    def test_every_face_of_a_d66_table_has_an_entry(self, ruleset):
        for a in range(1, 7):
            for b in range(1, 7):
                assert tb.roll_table(ruleset, "trinkets", roll=a * 10 + b)["text"]

    def test_random_roll_is_a_face(self, ruleset, rng):
        res = tb.roll_table(ruleset, "curios", rng=rng)
        assert 1 <= res["roll"] <= 20

    def test_bad_fixed_roll_raises(self, ruleset):
        with pytest.raises(ValueError):
            tb.roll_table(ruleset, "trinkets", roll=17)       # not a d66 face

    def test_unknown_table_raises_keyerror(self, ruleset):
        with pytest.raises(KeyError):
            tb.roll_table(ruleset, "no_such_table")


class TestRollDistinct:
    def test_two_different_entries(self, ruleset, rng):
        res = tb.roll_distinct(ruleset, "magic_complications", 2, rng)
        assert len(res) == 2
        assert res[0]["entry_roll"] != res[1]["entry_roll"]

    def test_all_entries_of_a_small_table(self, ruleset, rng):
        res = tb.roll_distinct(ruleset, "reaction", 5, rng)
        assert len({r["entry_roll"] for r in res}) == 5

    def test_more_than_entries_raises(self, ruleset):
        with pytest.raises(ValueError):
            tb.roll_distinct(ruleset, "reaction", 6)

    def test_unknown_table_raises(self, ruleset):
        with pytest.raises(KeyError):
            tb.roll_distinct(ruleset, "nope", 1)


# --- reaction -------------------------------------------------------------

class TestReactionRoll:
    def test_fixed_dice(self, ruleset):
        res = tb.reaction_roll(ruleset, dice=[6, 6])
        assert res["total"] == 12 and res["dice"] == [6, 6]
        assert res["text"]

    def test_modifier_clamps_to_the_table(self, ruleset):
        assert tb.reaction_roll(ruleset, dice=[6, 6], modifier=3)["total"] == 12
        assert tb.reaction_roll(ruleset, dice=[1, 1], modifier=-3)["total"] == 2

    def test_modifier_shifts_band(self, ruleset):
        low = tb.reaction_roll(ruleset, dice=[2, 2])["entry_roll"]
        high = tb.reaction_roll(ruleset, dice=[2, 2], modifier=4)["entry_roll"]
        assert low != high

    def test_bad_dice_raise(self, ruleset):
        with pytest.raises(ValueError):
            tb.reaction_roll(ruleset, dice=[7, 1])
        with pytest.raises(ValueError):
            tb.reaction_roll(ruleset, dice=[3])


# --- pressure -------------------------------------------------------------

class TestPressureRoll:
    @pytest.mark.parametrize("variant", tb.PRESSURE_VARIANTS)
    def test_every_variant_rolls(self, ruleset, variant, rng):
        res = tb.pressure_roll(ruleset, variant, rng=rng)
        assert res["table"] == f"pressure_{variant}"
        assert 1 <= res["roll"] <= 6

    def test_fixed_roll(self, ruleset):
        assert tb.pressure_roll(ruleset, roll=6)["roll"] == 6

    def test_unknown_variant_raises(self, ruleset):
        with pytest.raises(ValueError):
            tb.pressure_roll(ruleset, "space")


# --- oracle ---------------------------------------------------------------

class TestOracle:
    def test_even_tiers(self, ruleset):
        assert tb.oracle(ruleset, dice=[5, 5])["answer"] == "Yes"
        assert tb.oracle(ruleset, dice=[4, 4])["answer"] == "Yes, but…"
        assert tb.oracle(ruleset, dice=[3, 2])["answer"] == "No"

    def test_odds_shift_the_total(self, ruleset):
        assert tb.oracle(ruleset, "likely", dice=[3, 3])["total"] == 7
        assert tb.oracle(ruleset, "unlikely", dice=[3, 3])["total"] == 5
        assert tb.oracle(ruleset, "very_unlikely", dice=[5, 5])["answer"] == "Yes, but…"
        assert tb.oracle(ruleset, "likely", dice=[4, 5])["answer"] == "Yes"

    def test_naturals(self, ruleset):
        assert tb.oracle(ruleset, "very_unlikely", dice=[6, 6])["answer"] == "Yes, and…"
        res = tb.oracle(ruleset, "likely", dice=[1, 1])
        assert res["answer"] == "No, and…" and res["natural"] == "low"

    def test_prompts_come_from_the_oracle_tables(self, ruleset, rng):
        res = tb.oracle(ruleset, rng=rng)
        assert res["action"] and res["theme"]
        assert tb.oracle(ruleset, rng=rng, prompts=False)["action"] is None

    def test_prompts_absent_without_tables(self, bare_ruleset):
        res = tb.oracle(bare_ruleset, dice=[3, 4])
        assert res["action"] is None and res["theme"] is None

    def test_unknown_odds_and_bad_dice_raise(self, ruleset):
        with pytest.raises(ValueError):
            tb.oracle(ruleset, "certain")
        with pytest.raises(ValueError):
            tb.oracle(ruleset, dice=[0, 3])


# --- hoard ----------------------------------------------------------------

class TestHoard:
    def test_coin_is_2d6_x10_x_level(self, ruleset, rng):
        res = tb.roll_hoard(ruleset, 3, coin_dice=[4, 5], relic_die=1, rng=rng)
        assert res["coin"] == 9 * 10 * 3
        assert res["curio"]["table"] == "curios"
        assert res["trinket"]["table"] == "trinkets"
        assert res["relic"] is None

    def test_relic_on_a_six(self, ruleset, rng):
        res = tb.roll_hoard(ruleset, 1, coin_dice=[1, 1], relic_die=6, rng=rng)
        assert res["relic"]["table"] == "relics"
        assert res["coin"] == 20

    def test_random_hoard_in_range(self, ruleset, rng):
        res = tb.roll_hoard(ruleset, 10, rng=rng)
        assert 200 <= res["coin"] <= 1200

    def test_errors(self, ruleset):
        with pytest.raises(ValueError):
            tb.roll_hoard(ruleset, 0)
        with pytest.raises(ValueError):
            tb.roll_hoard(ruleset, 11)
        with pytest.raises(ValueError):
            tb.roll_hoard(ruleset, 1, coin_dice=[7, 1])
        with pytest.raises(ValueError):
            tb.roll_hoard(ruleset, 1, coin_dice=[1, 1], relic_die=0)

    def test_without_tables_only_coin(self, bare_ruleset):
        res = tb.roll_hoard(bare_ruleset, 2, coin_dice=[2, 2], relic_die=6)
        assert res["coin"] == 80 and res["curio"] is None and res["relic"] is None


# --- stuck helper ---------------------------------------------------------

class TestStuckHelper:
    def test_three_options_threat_arrival_secret(self, ruleset, rng):
        opts = tb.stuck_helper(ruleset, rng)
        assert [o["kind"] for o in opts] == ["threat", "arrival", "secret"]
        assert all(o["text"] for o in opts)
        assert opts[1]["table"] == "npc_names+npc_wants" and opts[1]["reaction"]
        assert opts[2]["detail"]

    def test_names_the_clock(self, ruleset, rng):
        assert "Midnight" in tb.stuck_helper(ruleset, rng, clock="Midnight")[0]["text"]

    def test_fallback_without_tables(self, bare_ruleset):
        opts = tb.stuck_helper(bare_ruleset)
        assert len(opts) == 3
        assert all(o["table"] is None and o["text"] for o in opts)
