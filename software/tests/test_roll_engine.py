"""Tests for the 2d6 roll resolution engine — outcomes, modifiers, Spark mechanics."""
import random
from collections import Counter
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.facets.schema import MagicDomainDef
from app.game.engine import (
    RollRequest,
    RollResult,
    resolve_magic_roll,
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
        assert sorted(result.dice_rolled) == result.dice_kept


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


# ---------------------------------------------------------------------------
# Extreme modifier stacking
# ---------------------------------------------------------------------------

class TestExtremeModifiers:
    def test_weak_hard_still_produces_valid_outcome(self, ruleset):
        """Rating 1 (-1) + Very Hard (-2) still resolves without error."""
        with patch("random.randint", return_value=1):
            result = resolve_roll(
                make_request(attribute_rating=1, difficulty_label="Very Hard"),
                ruleset,
            )
        assert result.outcome == "failure"
        assert result.total == 2 + (-1) + (-2)  # dice_sum=2 + attr=-1 + diff=-2

    def test_strong_easy_produces_high_total(self, ruleset):
        with patch("random.randint", return_value=6):
            result = resolve_roll(
                make_request(attribute_rating=3, difficulty_label="Easy"),
                ruleset,
            )
        # dice_sum=12, attr=+1, diff=+1 → 14
        assert result.total == 14
        assert result.outcome == "full_success"

    def test_expert_skill_easy_difficulty_stacks(self, ruleset):
        """Strong (+1) + Expert skill (+2) + Easy (+1) = +4 net."""
        with patch("random.randint", return_value=4):
            base = resolve_roll(make_request(attribute_rating=2, difficulty_label="Standard"), ruleset)
            stacked = resolve_roll(
                make_request(attribute_rating=3, skill_id="athletics",
                             skill_rank_id="expert", difficulty_label="Easy"),
                ruleset,
            )
        assert stacked.total == base.total + 4

    def test_weak_expert_skill_nets_plus_one(self, ruleset):
        """Weak (-1) + Expert (+2) = net +1."""
        with patch("random.randint", return_value=4):
            base = resolve_roll(make_request(attribute_rating=2), ruleset)
            result = resolve_roll(
                make_request(attribute_rating=1, skill_id="athletics", skill_rank_id="expert"),
                ruleset,
            )
        assert result.total == base.total + 1


# ---------------------------------------------------------------------------
# Edge cases on dice counts and totals
# ---------------------------------------------------------------------------

class TestDiceEdgeCases:
    def test_minimum_possible_roll(self, ruleset):
        """2 ones, weak attribute, very hard — minimum conceivable total."""
        with patch("random.randint", return_value=1):
            result = resolve_roll(
                make_request(attribute_rating=1, difficulty_label="Very Hard"),
                ruleset,
            )
        # dice_sum=2, attr=-1, diff=-2 → -1
        assert result.total == -1
        assert result.outcome == "failure"

    def test_maximum_possible_roll_no_spark(self, ruleset):
        with patch("random.randint", return_value=6):
            result = resolve_roll(
                make_request(attribute_rating=3, skill_id="athletics",
                             skill_rank_id="expert", difficulty_label="Easy"),
                ruleset,
            )
        assert result.outcome == "full_success"

    def test_partial_success_boundary_at_seven(self, ruleset):
        """Total == 7 is exactly partial_success threshold."""
        with patch("random.randint", side_effect=[3, 4]):
            result = resolve_roll(make_request(attribute_rating=2), ruleset)
        assert result.total == 7
        assert result.outcome == "partial_success"

    def test_just_below_partial_is_failure(self, ruleset):
        with patch("random.randint", side_effect=[2, 4]):
            result = resolve_roll(make_request(attribute_rating=2), ruleset)
        assert result.total == 6
        assert result.outcome == "failure"

    def test_full_success_boundary_at_ten(self, ruleset):
        with patch("random.randint", side_effect=[5, 5]):
            result = resolve_roll(make_request(attribute_rating=2), ruleset)
        assert result.total == 10
        assert result.outcome == "full_success"

    def test_just_below_full_success(self, ruleset):
        with patch("random.randint", side_effect=[4, 5]):
            result = resolve_roll(make_request(attribute_rating=2), ruleset)
        assert result.total == 9
        assert result.outcome == "partial_success"


# ---------------------------------------------------------------------------
# All 4 difficulties × all 3 skill ranks
# ---------------------------------------------------------------------------

class TestDifficultySkillCombinations:
    @pytest.mark.parametrize("difficulty,diff_mod", [
        ("Easy", 1), ("Standard", 0), ("Hard", -1), ("Very Hard", -2),
    ])
    @pytest.mark.parametrize("rank,rank_mod", [
        ("novice", 0), ("practiced", 1), ("expert", 2),
    ])
    def test_combination_total(self, ruleset, difficulty, diff_mod, rank, rank_mod):
        """Each difficulty × skill rank combination must produce the right total."""
        with patch("random.randint", return_value=4):
            result = resolve_roll(
                make_request(
                    attribute_rating=2,  # mod 0
                    skill_id="athletics",
                    skill_rank_id=rank,
                    difficulty_label=difficulty,
                ),
                ruleset,
            )
        expected = 8 + 0 + rank_mod + diff_mod  # dice_sum=8, attr_mod=0
        assert result.total == expected, (
            f"difficulty={difficulty}, rank={rank}: expected {expected}, got {result.total}"
        )


# ---------------------------------------------------------------------------
# Probability distribution validation
# ---------------------------------------------------------------------------

class TestProbabilityDistribution:
    def test_2d6_average_is_near_seven(self, ruleset):
        """Empirical: 2d6 average should be ~7.0 over a large sample."""
        random.seed(99)
        totals = [resolve_roll(make_request(), ruleset).dice_sum for _ in range(1000)]
        mean = sum(totals) / len(totals)
        assert 6.5 < mean < 7.5, f"Mean {mean} is outside expected range"

    def test_one_spark_mean_exceeds_no_spark(self, ruleset):
        random.seed(77)
        no_sparks = [resolve_roll(make_request(sparks_spent=0), ruleset).dice_sum for _ in range(500)]
        random.seed(77)
        one_spark = [resolve_roll(make_request(sparks_spent=1), ruleset).dice_sum for _ in range(500)]
        assert sum(one_spark) / 500 > sum(no_sparks) / 500


# ---------------------------------------------------------------------------
# RollRequest / RollResult field completeness
# ---------------------------------------------------------------------------

class TestRequestResultFields:
    def test_roll_request_preserves_all_fields(self, ruleset):
        req = make_request(
            attribute_id="strength", attribute_rating=3,
            skill_id="athletics", skill_rank_id="expert",
            difficulty_label="Hard", sparks_spent=1,
            description="Scale the cliffs",
        )
        result = resolve_roll(req, ruleset)
        assert result.request is req

    def test_roll_result_dict_has_all_keys(self, ruleset):
        result = resolve_roll(make_request(), ruleset)
        d = roll_result_to_dict(result)
        expected_keys = {
            "dice_rolled", "dice_kept", "dice_sum",
            "attribute_modifier", "skill_modifier", "difficulty_modifier",
            "total", "outcome", "outcome_label", "outcome_description",
            "sparks_spent", "attribute_id", "skill_id", "difficulty", "description",
        }
        assert expected_keys == set(d.keys())

    def test_negative_sparks_raises(self, ruleset):
        with pytest.raises(ValueError, match="sparks_spent"):
            make_request(sparks_spent=-1)

    def test_zero_sparks_allowed(self, ruleset):
        req = make_request(sparks_spent=0)
        result = resolve_roll(req, ruleset)
        assert result.sparks_spent == 0

    def test_large_spark_count_rolls_many_dice(self, ruleset):
        req = make_request(sparks_spent=5)
        result = resolve_roll(req, ruleset)
        assert len(result.dice_rolled) == 7  # 2 base + 5 extra
        assert len(result.dice_kept) == 2

    def test_description_truncated_at_200_chars(self, ruleset):
        long_desc = "x" * 300
        # description truncation is done in the WS handler, not the engine
        # but the engine must accept long strings without error
        req = make_request(description=long_desc)
        result = resolve_roll(req, ruleset)
        d = roll_result_to_dict(result)
        assert d["description"] == long_desc


# ---------------------------------------------------------------------------
# B3.5 — push_scope Spark use (implemented, not dead code)
# ---------------------------------------------------------------------------

def _make_magic_ruleset(domain_type: str, tradition: str = "intuitive") -> MagicMock:
    """Build a minimal MergedRuleset mock that supports a single magic domain."""
    domain = MagicDomainDef(
        id="test_domain",
        name="Test Domain",
        type=domain_type,
        tradition=tradition,
        description="A test domain.",
    )
    magic_mock = MagicMock()
    magic_mock.get_domain.return_value = domain
    magic_mock.domain_types = {
        "focused": {"scope_difficulties": {"minor": "Easy", "significant": "Standard", "major": "Hard"}},
        "standard": {"scope_difficulties": {"minor": "Standard", "significant": "Hard", "major": "Very Hard"}},
        "broad":    {"scope_difficulties": {"minor": "Hard", "significant": "Very Hard", "major": "Very Hard"}},
    }
    magic_mock.pre_technique_scope_limit = "minor"
    magic_mock.pre_technique_difficulty_penalty = 1

    ruleset_mock = MagicMock()
    ruleset_mock.magic = magic_mock
    ruleset_mock.roll_resolution = None  # falls back to hardcoded defaults
    ruleset_mock.get_minor_attribute_modifier.return_value = 0
    ruleset_mock.get_skill_rank_modifier.return_value = 0
    return ruleset_mock


def _make_caster(technique_active: bool = True) -> SimpleNamespace:
    return SimpleNamespace(
        magic_technique_active=technique_active,
        magic_domain="test_domain",
        attributes={"spirit": 2, "knowledge": 2},
    )


class TestPushScopeResolution:
    def test_push_scope_raises_for_broad_domain(self):
        """B3.5: push_scope on a Broad domain raises ValueError."""
        ruleset = _make_magic_ruleset("broad")
        character = _make_caster()
        with pytest.raises(ValueError, match="Broad"):
            resolve_magic_roll(
                character=character,
                domain_id="test_domain",
                scope="minor",
                intent="test",
                ruleset=ruleset,
                spark_use="push_scope",
            )

    def test_push_scope_steps_difficulty_harder_for_focused_domain(self):
        """B3.5: push_scope on a non-broad domain steps difficulty one step harder."""
        ruleset = _make_magic_ruleset("focused")
        character = _make_caster()
        # Focused minor is Easy (modifier +1). push_scope steps to Standard (modifier 0).
        # With dice=5,5 (sum=10) and attr=0, difficulty=0: total=10 → full_success
        # vs with Easy (+1): total=11
        with patch("random.randint", return_value=5):
            result_normal = resolve_magic_roll(
                character=character,
                domain_id="test_domain",
                scope="minor",
                intent="test",
                ruleset=ruleset,
                spark_use=None,
            )
            result_pushed = resolve_magic_roll(
                character=character,
                domain_id="test_domain",
                scope="minor",
                intent="test",
                ruleset=ruleset,
                spark_use="push_scope",
            )
        # push_scope steps Easy → Standard: difficulty_modifier goes from +1 to 0
        assert result_pushed.difficulty_modifier == result_normal.difficulty_modifier - 1

    def test_push_scope_steps_difficulty_harder_for_standard_domain(self):
        """B3.5: push_scope on a Standard domain steps difficulty one level harder."""
        ruleset = _make_magic_ruleset("standard")
        character = _make_caster()
        # Standard minor is Standard (modifier 0). push_scope steps to Hard (modifier -1).
        with patch("random.randint", return_value=5):
            result_normal = resolve_magic_roll(
                character=character,
                domain_id="test_domain",
                scope="minor",
                intent="test",
                ruleset=ruleset,
                spark_use=None,
            )
            result_pushed = resolve_magic_roll(
                character=character,
                domain_id="test_domain",
                scope="minor",
                intent="test",
                ruleset=ruleset,
                spark_use="push_scope",
            )
        assert result_pushed.difficulty_modifier == result_normal.difficulty_modifier - 1


# ---------------------------------------------------------------------------
# Data-driven outcome tiers
# ---------------------------------------------------------------------------

class TestDataDrivenOutcomeTiers:
    """Tests for generalized N-tier outcome system."""

    def _make_tier_ruleset(self, tiers):
        """Build a MagicMock ruleset with custom outcome_tiers."""
        from app.facets.schema import OutcomeTierDef
        tier_defs = [OutcomeTierDef(**t) for t in tiers]
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.outcome_tiers = tier_defs
        mock.roll_resolution.thresholds = {}
        mock.roll_resolution.outcomes = None
        mock.roll_resolution.difficulty_modifiers = []
        return mock

    def test_outcome_from_4_tier_system(self):
        """4-tier system: critical (20+), success (10+), fail (5+), fumble (catch-all)."""
        ruleset = self._make_tier_ruleset([
            {"id": "critical", "threshold": 20, "label": "Critical!", "description": "Crit"},
            {"id": "success", "threshold": 10, "label": "Success", "description": "OK"},
            {"id": "fail", "threshold": 5, "label": "Fail", "description": "Bad"},
            {"id": "fumble", "threshold": None, "label": "Fumble", "description": "Oops"},
        ])
        tier, label, desc = _determine_outcome(25, ruleset)
        assert tier == "critical"
        tier, label, desc = _determine_outcome(20, ruleset)
        assert tier == "critical"
        tier, label, desc = _determine_outcome(15, ruleset)
        assert tier == "success"
        tier, label, desc = _determine_outcome(10, ruleset)
        assert tier == "success"
        tier, label, desc = _determine_outcome(7, ruleset)
        assert tier == "fail"
        tier, label, desc = _determine_outcome(5, ruleset)
        assert tier == "fail"
        tier, label, desc = _determine_outcome(4, ruleset)
        assert tier == "fumble"
        tier, label, desc = _determine_outcome(-1, ruleset)
        assert tier == "fumble"

    def test_outcome_from_2_tier_binary(self):
        """Binary pass/fail — 2 tiers (success at 10, failure catch-all)."""
        ruleset = self._make_tier_ruleset([
            {"id": "success", "threshold": 10, "label": "Pass", "description": "You pass"},
            {"id": "failure", "threshold": None, "label": "Fail", "description": "You fail"},
        ])
        tier, _, _ = _determine_outcome(10, ruleset)
        assert tier == "success"
        tier, _, _ = _determine_outcome(9, ruleset)
        assert tier == "failure"

    def test_outcome_tiers_backward_compat(self):
        """Old thresholds+outcomes format works when outcome_tiers is empty."""
        from app.facets.schema import OutcomeLabel, OutcomesDef
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.outcome_tiers = []
        mock.roll_resolution.thresholds = {"full_success": 10, "partial_success": 7}
        mock.roll_resolution.outcomes = OutcomesDef(
            full_success=OutcomeLabel(label="Full Success", description="Clean success"),
            partial_success=OutcomeLabel(label="Partial", description="Cost"),
            failure=OutcomeLabel(label="Failure", description="Bad"),
        )
        tier, label, _ = _determine_outcome(10, mock)
        assert tier == "full_success"
        assert label == "Full Success"
        tier, _, _ = _determine_outcome(7, mock)
        assert tier == "partial_success"
        tier, _, _ = _determine_outcome(6, mock)
        assert tier == "failure"


# ---------------------------------------------------------------------------
# Data-driven difficulty order
# ---------------------------------------------------------------------------

class TestDataDrivenDifficulty:
    def test_difficulty_order_derived_from_modifiers(self):
        """Custom difficulty names derive correct stepping order."""
        from app.game.engine import _step_difficulty_harder, _step_difficulty_easier
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.difficulty_modifiers = [
            MagicMock(label="Trivial", modifier=2),
            MagicMock(label="Normal", modifier=0),
            MagicMock(label="Brutal", modifier=-3),
        ]
        # Trivial → Normal → Brutal (sorted by modifier descending)
        result = _step_difficulty_harder("Trivial", mock)
        assert result == "Normal"
        result = _step_difficulty_harder("Normal", mock)
        assert result == "Brutal"
        result = _step_difficulty_harder("Brutal", mock)
        assert result == "Brutal"  # already at hardest

    def test_step_easier_uses_ruleset_order(self):
        from app.game.engine import _step_difficulty_easier
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.difficulty_modifiers = [
            MagicMock(label="Trivial", modifier=2),
            MagicMock(label="Normal", modifier=0),
            MagicMock(label="Brutal", modifier=-3),
        ]
        result = _step_difficulty_easier("Brutal", mock)
        assert result == "Normal"
        result = _step_difficulty_easier("Trivial", mock)
        assert result == "Trivial"  # already at easiest


# ---------------------------------------------------------------------------
# Data-driven dice (1d20, etc.)
# ---------------------------------------------------------------------------

class TestDataDrivenDice:
    def test_dice_1d20_produces_correct_range(self):
        """Roll with dice='1d20' uses d20, not d6."""
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.dice = "1d20"
        mock.roll_resolution.outcome_tiers = []
        mock.roll_resolution.thresholds = {"full_success": 15, "partial_success": 10}
        mock.roll_resolution.outcomes = MagicMock()
        mock.roll_resolution.outcomes.full_success.label = "Hit"
        mock.roll_resolution.outcomes.full_success.description = "Hit"
        mock.roll_resolution.outcomes.partial_success.label = "Graze"
        mock.roll_resolution.outcomes.partial_success.description = "Graze"
        mock.roll_resolution.outcomes.failure.label = "Miss"
        mock.roll_resolution.outcomes.failure.description = "Miss"
        mock.roll_resolution.difficulty_modifiers = []
        mock.get_minor_attribute_modifier.return_value = 0
        mock.get_skill_rank_modifier.return_value = 0

        # Mock random to return 17 (valid d20 value, > 6)
        with patch("random.randint", return_value=17):
            result = resolve_roll(make_request(), mock)
        # With 1d20: only 1 die kept, sum = 17
        assert len(result.dice_rolled) == 1
        assert len(result.dice_kept) == 1
        assert result.dice_sum == 17

    def test_1d20_validation_integration(self):
        """Build a minimal ruleset with 1d20 and 2 outcome tiers, full resolve."""
        from app.facets.schema import OutcomeTierDef
        mock = MagicMock()
        mock.roll_resolution = MagicMock()
        mock.roll_resolution.dice = "1d20"
        mock.roll_resolution.outcome_tiers = [
            OutcomeTierDef(id="pass", threshold=10, label="Pass", description="You pass"),
            OutcomeTierDef(id="fail", threshold=None, label="Fail", description="You fail"),
        ]
        mock.roll_resolution.thresholds = {}
        mock.roll_resolution.outcomes = None
        mock.roll_resolution.difficulty_modifiers = []
        mock.get_minor_attribute_modifier.return_value = 0
        mock.get_skill_rank_modifier.return_value = 0

        with patch("random.randint", return_value=15):
            result = resolve_roll(make_request(), mock)
        assert result.outcome == "pass"
        assert result.dice_sum == 15

        with patch("random.randint", return_value=5):
            result = resolve_roll(make_request(), mock)
        assert result.outcome == "fail"
