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
