"""Core roll resolution (PHB III.1) — app/game/engine.py (T3)."""
from __future__ import annotations

import random

import pytest

from app.game.engine import (
    capped_modifier, outcome_for_total, outcome_label, resolve_avoid, resolve_roll,
    roll_character, roll_d6s, roll_expr, roll_result_to_dict,
)


class TestResolveRoll:
    def test_total_is_kept_dice_plus_stat_plus_knack(self, ruleset):
        r = resolve_roll(ruleset, stat_value=2, knack=True, dice=[4, 3])
        assert r.total == 10 and r.outcome == "full_success" and r.modifier == 3

    def test_partial_and_failure_tiers(self, ruleset):
        assert resolve_roll(ruleset, stat_value=0, dice=[4, 3]).outcome == "partial_success"
        assert resolve_roll(ruleset, stat_value=0, dice=[3, 3]).outcome == "failure"

    def test_difficulty_applies(self, ruleset):
        r = resolve_roll(ruleset, stat_value=1, difficulty="Very Hard", dice=[5, 3])
        assert r.total == 7 and r.difficulty_modifier == -2

    def test_modifier_capped_at_four(self, ruleset):
        r = resolve_roll(ruleset, stat_value=3, knack=True, bonus=2, dice=[2, 2])
        assert r.modifier == 4 and r.capped is True and r.total == 8

    def test_difficulty_is_outside_the_cap(self, ruleset):
        r = resolve_roll(ruleset, stat_value=3, knack=True, bonus=1, difficulty="Easy", dice=[2, 2])
        assert r.total == 9          # 4 (capped) + 1 Easy

    def test_extra_dice_keep_best_two(self, ruleset):
        r = resolve_roll(ruleset, stat_value=0, sparks=1, help=1, borrowed_trouble=True,
                         dice=[1, 2, 6, 5, 3])
        assert r.kept == [6, 5] and r.total == 11

    def test_natural_twelve_is_full_success_whatever_the_modifiers(self, ruleset):
        r = resolve_roll(ruleset, stat_value=-1, difficulty="Very Hard", dice=[6, 6])
        assert r.total == 9 and r.outcome == "full_success" and r.natural_high

    def test_natural_two_on_failure_confirms_the_graceful_fail(self, ruleset):
        r = resolve_roll(ruleset, stat_value=0, dice=[1, 1])
        assert r.natural_low and r.graceful_fail_auto

    def test_natural_two_that_succeeds_is_not_a_graceful_fail(self, ruleset):
        r = resolve_roll(ruleset, stat_value=3, knack=True, bonus=0, difficulty="Easy", dice=[1, 1])
        assert r.outcome == "partial_success" and not r.graceful_fail_auto

    def test_naturals_read_on_kept_dice(self, ruleset):
        r = resolve_roll(ruleset, stat_value=0, sparks=1, dice=[1, 1, 4])
        assert not r.natural_low and r.kept == [4, 1]

    def test_unknown_difficulty_raises(self, ruleset):
        with pytest.raises(ValueError):
            resolve_roll(ruleset, stat_value=0, difficulty="Trivial")

    def test_too_much_help_raises(self, ruleset):
        with pytest.raises(ValueError):
            resolve_roll(ruleset, stat_value=0, help=2)

    def test_negative_sparks_raise(self, ruleset):
        with pytest.raises(ValueError):
            resolve_roll(ruleset, stat_value=0, sparks=-1)

    def test_wrong_number_of_fixed_dice_raises(self, ruleset):
        with pytest.raises(ValueError):
            resolve_roll(ruleset, stat_value=0, sparks=1, dice=[3, 3])

    def test_out_of_range_fixed_die_raises(self, ruleset):
        with pytest.raises(ValueError):
            resolve_roll(ruleset, stat_value=0, dice=[7, 1])

    def test_random_rolls_are_in_range(self, ruleset):
        rng = random.Random(3)
        for _ in range(50):
            r = resolve_roll(ruleset, stat_value=1, sparks=2, rng=rng)
            assert len(r.dice) == 4 and all(1 <= d <= 6 for d in r.dice)


class TestResolveAvoid:
    def test_avoid_carries_the_tier_text(self, ruleset):
        r = resolve_avoid(ruleset, stat_value=2, stat="body", dice=[5, 4])
        assert r.kind == "avoid" and r.extra["text"] == "You avoid it entirely."

    def test_avoid_partial_is_the_worst_of_it(self, ruleset):
        r = resolve_avoid(ruleset, stat_value=0, dice=[4, 4])
        assert "worst" in r.extra["text"]

    def test_avoid_failure_takes_hold(self, ruleset):
        r = resolve_avoid(ruleset, stat_value=0, difficulty="Hard", dice=[3, 3])
        assert r.outcome == "failure" and r.extra["text"] == "It takes hold."

    def test_avoid_unknown_difficulty_raises(self, ruleset):
        with pytest.raises(ValueError):
            resolve_avoid(ruleset, stat_value=0, difficulty="Nope")


class TestRollCharacter:
    def test_reads_the_stat_and_debits_sparks(self, ruleset, body_character):
        r = roll_character(ruleset, body_character, "body", sparks=2, dice=[1, 2, 6, 3])
        assert r.stat_value == 2 and body_character.sparks == 1 and r.kept == [6, 3]

    def test_unknown_stat_raises(self, ruleset, body_character):
        with pytest.raises(ValueError):
            roll_character(ruleset, body_character, "luck")

    def test_more_sparks_than_held_raises(self, ruleset, body_character):
        with pytest.raises(ValueError):
            roll_character(ruleset, body_character, "body", sparks=4)
        assert body_character.sparks == 3


class TestHelpers:
    def test_roll_expr_fixed(self):
        assert roll_expr("2d8+1", fixed=[3, 4]) == ([3, 4], 8)

    def test_roll_expr_random_in_range(self):
        dice, total = roll_expr("1d8", rng=random.Random(1))
        assert 1 <= dice[0] <= 8 and total == dice[0]

    def test_roll_expr_bad_fixed_raises(self):
        with pytest.raises(ValueError):
            roll_expr("1d6", fixed=[7])

    def test_roll_d6s(self):
        assert len(roll_d6s(3, random.Random(1))) == 3
        assert roll_d6s(0) == []
        assert all(1 <= d <= 6 for d in roll_d6s(20))

    def test_outcome_for_total_boundaries(self, ruleset):
        assert [outcome_for_total(ruleset, t) for t in (6, 7, 9, 10)] == [
            "failure", "partial_success", "partial_success", "full_success"]

    def test_outcome_label(self, ruleset):
        assert outcome_label(ruleset, "partial_success") == "Success with Cost"
        assert outcome_label(ruleset, "failure") == "Things Go Wrong"
        assert outcome_label(ruleset, "odd") == "odd"

    def test_capped_modifier(self, ruleset):
        assert capped_modifier(ruleset, 2, True, 0) == (3, False)
        assert capped_modifier(ruleset, 3, True, 1) == (4, True)
        assert capped_modifier(ruleset, -1, False, 0) == (-1, False)

    def test_roll_result_to_dict_is_json_safe(self, ruleset):
        import json
        d = roll_result_to_dict(resolve_roll(ruleset, stat_value=1, dice=[4, 4]))
        assert json.loads(json.dumps(d))["total"] == 9 and d["succeeded"] is True
