"""Tests for the dice notation parser and roller."""
import pytest

from app.game.dice import DiceSpec


class TestDiceSpecParse:
    def test_parse_2d6(self):
        spec = DiceSpec.parse("2d6")
        assert spec.count == 2
        assert spec.sides == 6

    def test_parse_1d20(self):
        spec = DiceSpec.parse("1d20")
        assert spec.count == 1
        assert spec.sides == 20

    def test_parse_1d100(self):
        spec = DiceSpec.parse("1d100")
        assert spec.count == 1
        assert spec.sides == 100

    def test_parse_3d8(self):
        spec = DiceSpec.parse("3d8")
        assert spec.count == 3
        assert spec.sides == 8

    @pytest.mark.parametrize("bad_input", ["", "d6", "2d", "abc", "2x6", "0d6", "2d0"])
    def test_parse_invalid_raises(self, bad_input):
        with pytest.raises(ValueError):
            DiceSpec.parse(bad_input)


class TestDiceSpecRoll:
    def test_roll_returns_correct_count(self):
        spec = DiceSpec(count=2, sides=6)
        result = spec.roll()
        assert len(result) == 2

    def test_roll_returns_correct_count_3d8(self):
        spec = DiceSpec(count=3, sides=8)
        result = spec.roll()
        assert len(result) == 3

    def test_roll_values_in_range(self):
        spec = DiceSpec(count=4, sides=20)
        for _ in range(100):
            for val in spec.roll():
                assert 1 <= val <= 20


# ---------------------------------------------------------------------------
# Modifier notation — for the MM's table roller
# ---------------------------------------------------------------------------

class TestModifierNotation:
    """The MM's table roller lets an MM type what a random table asks for
    ("1d20+3"), so the parser accepts a trailing modifier. Plain 'NdS' is
    unchanged and still parses to a modifier of 0 — the resolution engine and
    combat module both go through this parser.
    """

    def test_plain_notation_has_no_modifier(self):
        assert DiceSpec.parse("2d6").modifier == 0

    def test_positive_modifier(self):
        spec = DiceSpec.parse("1d20+3")
        assert (spec.count, spec.sides, spec.modifier) == (1, 20, 3)

    def test_negative_modifier(self):
        spec = DiceSpec.parse("2d6-1")
        assert (spec.count, spec.sides, spec.modifier) == (2, 6, -1)

    def test_whitespace_around_the_modifier_is_tolerated(self):
        assert DiceSpec.parse(" 3d8 + 2 ").modifier == 2

    def test_total_applies_the_modifier(self):
        spec = DiceSpec.parse("1d1+5")   # 1d1 always rolls 1
        assert spec.total([1]) == 6

    def test_total_of_a_plain_spec_is_the_dice_sum(self):
        assert DiceSpec.parse("3d6").total([2, 3, 4]) == 9

    def test_a_bare_modifier_is_still_invalid(self):
        with pytest.raises(ValueError):
            DiceSpec.parse("+3")

    def test_a_trailing_operator_is_invalid(self):
        with pytest.raises(ValueError):
            DiceSpec.parse("1d20+")
