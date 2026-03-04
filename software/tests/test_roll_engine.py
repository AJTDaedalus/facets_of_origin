"""Tests for the 2d6 roll resolution engine — outcomes, modifiers, Spark mechanics."""
import random
from collections import Counter
from unittest.mock import patch

import pytest

from app.game.engine import (
    RollRequest,
    RollResult,
    resolve_roll,
    roll_result_to_dict,
    _determine_outcome,
    _get_difficulty_modifier,
)


def make_request(
    attribute_id="strength",
    attribute_rating=2,
    skill_id=None,
    skill_rank_id=None,
    difficulty_label="Standard",
    sparks_spent=0,
    description="",
) -> RollRequest:
    return RollRequest(
        attribute_id=attribute_id,
        attribute_rating=attribute_rating,
        skill_id=skill_id,
        skill_rank_id=skill_rank_id,
        difficulty_label=difficulty_label,
        sparks_spent=sparks_spent,
        description=description,
    )


# ---------------------------------------------------------------------------
# Outcome tiers
# ---------------------------------------------------------------------------

class TestOutcomeTiers:
    @pytest.mark.parametrize("total,expected", [
        (10, "full_success"),
        (11, "full_success"),
        (12, "full_success"),
        (9, "partial_success"),
        (8, "partial_success"),
        (7, "partial_success"),
        (6, "failure"),
        (5, "failure"),
        (4, "failure"),
        (2, "failure"),
    ])
    def test_outcome_tiers(self, total, expected, ruleset):
        tier, label, desc = _determine_outcome(total, ruleset)
        assert tier == expected

    def test_full_success_label(self, ruleset):
        tier, label, desc = _determine_outcome(10, ruleset)
        assert "success" in label.lower()

    def test_failure_description_mentions_story(self, ruleset):
        tier, label, desc = _determine_outcome(2, ruleset)
        assert "story" in desc.lower() or "wrong" in desc.lower()


# ---------------------------------------------------------------------------
# Modifiers
# ---------------------------------------------------------------------------

class TestAttributeModifiers:
    @pytest.mark.parametrize("rating,expected_mod", [(1, -1), (2, 0), (3, 1)])
    def test_modifier_from_rating(self, rating, expected_mod, ruleset):
        mod = ruleset.get_minor_attribute_modifier("strength", rating)
        assert mod == expected_mod

    def test_strong_attribute_shifts_total_up(self, ruleset):
        """Rating 3 (+1) should produce totals 1 higher than rating 2 (+0) for same dice."""
        with patch("random.randint", return_value=4):
            req_avg = make_request(attribute_rating=2)
            req_strong = make_request(attribute_rating=3)
            r_avg = resolve_roll(req_avg, ruleset)
            r_strong = resolve_roll(req_strong, ruleset)
        assert r_strong.total == r_avg.total + 1

    def test_weak_attribute_shifts_total_down(self, ruleset):
        with patch("random.randint", return_value=4):
            req_avg = make_request(attribute_rating=2)
            req_weak = make_request(attribute_rating=1)
            r_avg = resolve_roll(req_avg, ruleset)
            r_weak = resolve_roll(req_weak, ruleset)
        assert r_weak.total == r_avg.total - 1


class TestDifficultyModifiers:
    @pytest.mark.parametrize("label,expected", [
        ("Easy", 1), ("Standard", 0), ("Hard", -1), ("Very Hard", -2),
    ])
    def test_difficulty_modifier_values(self, label, expected, ruleset):
        mod = _get_difficulty_modifier(label, ruleset)
        assert mod == expected

    def test_easy_difficulty_raises_total(self, ruleset):
        with patch("random.randint", return_value=4):
            easy = resolve_roll(make_request(difficulty_label="Easy"), ruleset)
            standard = resolve_roll(make_request(difficulty_label="Standard"), ruleset)
        assert easy.total == standard.total + 1

    def test_very_hard_reduces_total_by_two(self, ruleset):
        with patch("random.randint", return_value=4):
            standard = resolve_roll(make_request(difficulty_label="Standard"), ruleset)
            very_hard = resolve_roll(make_request(difficulty_label="Very Hard"), ruleset)
        assert standard.total == very_hard.total + 2

    def test_unknown_difficulty_defaults_to_zero(self, ruleset):
        mod = _get_difficulty_modifier("Mythical", ruleset)
        assert mod == 0


class TestSkillModifiers:
    def test_practiced_skill_adds_one(self, ruleset):
        with patch("random.randint", return_value=4):
            no_skill = resolve_roll(make_request(), ruleset)
            with_skill = resolve_roll(make_request(skill_id="athletics", skill_rank_id="practiced"), ruleset)
        assert with_skill.total == no_skill.total + 1

    def test_expert_skill_adds_two(self, ruleset):
        with patch("random.randint", return_value=4):
            no_skill = resolve_roll(make_request(), ruleset)
            expert = resolve_roll(make_request(skill_id="athletics", skill_rank_id="expert"), ruleset)
        assert expert.total == no_skill.total + 2

    def test_novice_skill_adds_zero(self, ruleset):
        with patch("random.randint", return_value=4):
            no_skill = resolve_roll(make_request(), ruleset)
            novice = resolve_roll(make_request(skill_id="athletics", skill_rank_id="novice"), ruleset)
        assert novice.total == no_skill.total

    def test_modifier_stacking_attr_plus_skill(self, ruleset):
        """Strong attr (+1) + Expert skill (+2) = +3 net modifier."""
        with patch("random.randint", return_value=4):
            base = resolve_roll(make_request(attribute_rating=2), ruleset)
            stacked = resolve_roll(
                make_request(attribute_rating=3, skill_id="athletics", skill_rank_id="expert"),
                ruleset,
            )
        assert stacked.total == base.total + 3


# ---------------------------------------------------------------------------
# Spark mechanics
# ---------------------------------------------------------------------------

class TestSparkMechanics:
    def test_one_spark_rolls_three_dice(self, ruleset):
        req = make_request(sparks_spent=1)
        result = resolve_roll(req, ruleset)
        assert len(result.dice_rolled) == 3

    def test_two_sparks_rolls_four_dice(self, ruleset):
        req = make_request(sparks_spent=2)
        result = resolve_roll(req, ruleset)
        assert len(result.dice_rolled) == 4

    def test_no_sparks_rolls_two_dice(self, ruleset):
        req = make_request(sparks_spent=0)
        result = resolve_roll(req, ruleset)
        assert len(result.dice_rolled) == 2

    def test_spark_keeps_only_two_dice(self, ruleset):
        req = make_request(sparks_spent=1)
        result = resolve_roll(req, ruleset)
        assert len(result.dice_kept) == 2

    def test_spark_keeps_highest_dice(self, ruleset):
        """With 1 Spark: roll 3d6, drop the lowest. Kept should be top 2."""
        with patch("random.randint", side_effect=[2, 5, 3]):
            result = resolve_roll(make_request(sparks_spent=1), ruleset)
        assert sorted(result.dice_kept) == [3, 5]

    def test_two_sparks_keep_two_highest_of_four(self, ruleset):
        with patch("random.randint", side_effect=[1, 6, 2, 5]):
            result = resolve_roll(make_request(sparks_spent=2), ruleset)
        assert sorted(result.dice_kept) == [5, 6]

    def test_spark_dice_sum_matches_kept(self, ruleset):
        result = resolve_roll(make_request(sparks_spent=1), ruleset)
        assert result.dice_sum == sum(result.dice_kept)

    def test_spark_improves_expected_value(self, ruleset):
        """Empirically: rolling with 1 Spark should average higher than without."""
        random.seed(42)
        no_spark_totals = [resolve_roll(make_request(sparks_spent=0), ruleset).dice_sum for _ in range(500)]
        random.seed(42)
        spark_totals = [resolve_roll(make_request(sparks_spent=1), ruleset).dice_sum for _ in range(500)]
        assert sum(spark_totals) / len(spark_totals) > sum(no_spark_totals) / len(no_spark_totals)

    def test_zero_sparks_dice_rolled_equals_kept(self, ruleset):
        result = resolve_roll(make_request(sparks_spent=0), ruleset)
        assert result.dice_rolled == result.dice_kept


# ---------------------------------------------------------------------------
# Full roll integration
# ---------------------------------------------------------------------------

class TestFullRoll:
    def test_total_is_dice_sum_plus_modifiers(self, ruleset):
        with patch("random.randint", return_value=4):
            result = resolve_roll(
                make_request(attribute_rating=3, skill_id="athletics", skill_rank_id="practiced",
                             difficulty_label="Hard"),
                ruleset,
            )
        # dice_sum = 8, attr mod = +1, skill mod = +1, difficulty = -1 → 9
        assert result.dice_sum == 8
        assert result.attribute_modifier == 1
        assert result.skill_modifier == 1
        assert result.difficulty_modifier == -1
        assert result.total == 9

    def test_outcome_matches_total(self, ruleset):
        with patch("random.randint", return_value=5):
            result = resolve_roll(make_request(attribute_rating=2), ruleset)
        # dice_sum = 10, no mods → full_success
        assert result.total == 10
        assert result.outcome == "full_success"

    def test_partial_success_range(self, ruleset):
        """Dice sum 7 with no mods → partial success."""
        with patch("random.randint", side_effect=[3, 4]):
            result = resolve_roll(make_request(), ruleset)
        assert result.total == 7
        assert result.outcome == "partial_success"

    def test_failure_range(self, ruleset):
        with patch("random.randint", side_effect=[1, 2]):
            result = resolve_roll(make_request(), ruleset)
        assert result.total == 3
        assert result.outcome == "failure"

    def test_roll_result_to_dict_is_json_safe(self, ruleset):
        import json
        result = resolve_roll(make_request(), ruleset)
        d = roll_result_to_dict(result)
        # Should not raise
        json.dumps(d)

    def test_dice_values_in_valid_range(self, ruleset):
        for _ in range(100):
            result = resolve_roll(make_request(), ruleset)
            for die in result.dice_rolled:
                assert 1 <= die <= 6

    def test_description_preserved(self, ruleset):
        req = make_request(description="Attempting to climb the wall")
        result = resolve_roll(req, ruleset)
        d = roll_result_to_dict(result)
        assert d["description"] == "Attempting to climb the wall"
