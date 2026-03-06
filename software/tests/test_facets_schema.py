"""Unit tests for every Pydantic schema class in app/facets/schema.py."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.facets.schema import (
    AdvancementDef,
    AttributeDistribution,
    AttributeRating,
    AttributesDef,
    BranchDef,
    CharacterFacetDef,
    DifficultyModifier,
    FacetFile,
    FacetTreeDef,
    MajorAttributeDef,
    MinorAttributeDef,
    OutcomeLabel,
    OutcomesDef,
    RollResolutionDef,
    SkillDef,
    SkillPointCostDef,
    SkillRankDef,
    SparkDef,
    SparkEarnMethod,
    SparkMechanicDef,
    TechniqueDef,
    TierDef,
)


# ---------------------------------------------------------------------------
# AttributeRating
# ---------------------------------------------------------------------------

class TestAttributeRating:
    def test_valid_rating_constructs(self):
        ar = AttributeRating(rating=2, label="Average", modifier=0)
        assert ar.rating == 2
        assert ar.modifier == 0

    def test_rating_below_minimum_rejected(self):
        with pytest.raises(ValidationError):
            AttributeRating(rating=0, label="Zero", modifier=-10)

    def test_rating_above_maximum_rejected(self):
        with pytest.raises(ValidationError):
            AttributeRating(rating=11, label="Legendary", modifier=5)

    def test_rating_at_minimum_boundary(self):
        ar = AttributeRating(rating=1, label="Weak", modifier=-1)
        assert ar.rating == 1

    def test_rating_at_maximum_boundary(self):
        ar = AttributeRating(rating=10, label="Mythic", modifier=4)
        assert ar.rating == 10

    def test_negative_modifier_allowed(self):
        ar = AttributeRating(rating=1, label="Weak", modifier=-3)
        assert ar.modifier == -3


# ---------------------------------------------------------------------------
# MajorAttributeDef
# ---------------------------------------------------------------------------

class TestMajorAttributeDef:
    def test_constructs_with_required_fields(self):
        ma = MajorAttributeDef(
            id="body", name="Body",
            description="Physical presence",
            minor_attributes=["strength", "dexterity"],
        )
        assert ma.id == "body"
        assert len(ma.minor_attributes) == 2

    def test_empty_minor_list_allowed(self):
        ma = MajorAttributeDef(id="x", name="X", description=".", minor_attributes=[])
        assert ma.minor_attributes == []


# ---------------------------------------------------------------------------
# MinorAttributeDef
# ---------------------------------------------------------------------------

class TestMinorAttributeDef:
    def test_constructs(self):
        mi = MinorAttributeDef(id="strength", name="Strength", description="Raw power", major="body")
        assert mi.major == "body"

    def test_missing_major_raises(self):
        with pytest.raises(ValidationError):
            MinorAttributeDef(id="strength", name="Strength", description="test")


# ---------------------------------------------------------------------------
# AttributeDistribution
# ---------------------------------------------------------------------------

class TestAttributeDistribution:
    def test_constructs_with_all_fields(self):
        dist = AttributeDistribution(total_points=18, min_per_attribute=1, max_per_attribute=3)
        assert dist.total_points == 18

    def test_missing_field_raises(self):
        with pytest.raises(ValidationError):
            AttributeDistribution(total_points=18)


# ---------------------------------------------------------------------------
# CharacterFacetDef
# ---------------------------------------------------------------------------

class TestCharacterFacetDef:
    def test_constructs(self):
        cf = CharacterFacetDef(id="body", name="Body", description=".", major_attribute="body")
        assert cf.id == "body"

    def test_missing_major_attribute_raises(self):
        with pytest.raises(ValidationError):
            CharacterFacetDef(id="body", name="Body", description=".")


# ---------------------------------------------------------------------------
# SkillDef
# ---------------------------------------------------------------------------

class TestSkillDef:
    def test_constructs_active(self):
        s = SkillDef(id="athletics", name="Athletics", facet="body",
                     attribute="strength", description="Climbing, jumping.")
        assert s.status == "active"

    def test_explicit_stub_status(self):
        s = SkillDef(id="arcana", name="Arcana", facet="mind",
                     attribute="intelligence", description="Magic.", status="stub")
        assert s.status == "stub"

    def test_invalid_status_rejected(self):
        with pytest.raises(ValidationError):
            SkillDef(id="bad", name="Bad", facet="x", attribute="y",
                     description=".", status="legendary")

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            SkillDef(id="x", name="X", facet="body")  # missing attribute and description


# ---------------------------------------------------------------------------
# TechniqueDef
# ---------------------------------------------------------------------------

class TestTechniqueDef:
    def test_constructs_with_required_fields(self):
        t = TechniqueDef(id="forcing_hand", name="Forcing Hand", description="...")
        assert t.has_choice is False
        assert t.prerequisites == []
        assert t.choice_prompt == ""

    def test_has_choice_and_prompt(self):
        t = TechniqueDef(
            id="mastery", name="Mastery", description=".",
            has_choice=True, choice_prompt="Choose a weapon type.",
        )
        assert t.has_choice is True
        assert t.choice_prompt == "Choose a weapon type."

    def test_prerequisites_list(self):
        t = TechniqueDef(id="tier2", name="Tier 2", description=".",
                         prerequisites=["tier1a", "tier1b"])
        assert len(t.prerequisites) == 2


# ---------------------------------------------------------------------------
# TierDef
# ---------------------------------------------------------------------------

class TestTierDef:
    def test_tier_at_minimum(self):
        tier = TierDef(tier=1, techniques=[])
        assert tier.tier == 1

    def test_tier_at_maximum(self):
        tier = TierDef(tier=3, techniques=[])
        assert tier.tier == 3

    def test_tier_below_minimum_raises(self):
        with pytest.raises(ValidationError):
            TierDef(tier=0, techniques=[])

    def test_tier_above_maximum_raises(self):
        with pytest.raises(ValidationError):
            TierDef(tier=4, techniques=[])


# ---------------------------------------------------------------------------
# RollResolutionDef
# ---------------------------------------------------------------------------

class TestRollResolutionDef:
    def _outcomes(self):
        return OutcomesDef(
            full_success=OutcomeLabel(label="Full", description="Clean."),
            partial_success=OutcomeLabel(label="Partial", description="Cost."),
            failure=OutcomeLabel(label="Fail", description="Wrong."),
        )

    def test_constructs_with_required_fields(self):
        rr = RollResolutionDef(
            thresholds={"full_success": 10, "partial_success": 7},
            outcomes=self._outcomes(),
        )
        assert rr.dice == "2d6"

    def test_default_dice_format(self):
        rr = RollResolutionDef(
            thresholds={"full_success": 10, "partial_success": 7},
            outcomes=self._outcomes(),
        )
        assert rr.dice == "2d6"

    def test_difficulty_modifiers_default_empty(self):
        rr = RollResolutionDef(
            thresholds={"full_success": 10, "partial_success": 7},
            outcomes=self._outcomes(),
        )
        assert rr.difficulty_modifiers == []

    def test_custom_thresholds(self):
        rr = RollResolutionDef(
            thresholds={"full_success": 8, "partial_success": 5},
            outcomes=self._outcomes(),
        )
        assert rr.thresholds["full_success"] == 8


# ---------------------------------------------------------------------------
# SparkDef
# ---------------------------------------------------------------------------

class TestSparkDef:
    def test_base_sparks_non_negative_required(self):
        with pytest.raises(ValidationError):
            SparkDef(
                base_sparks_per_session=-1,
                mechanic=SparkMechanicDef(spend="per_spark", description="."),
            )

    def test_zero_sparks_allowed(self):
        s = SparkDef(
            base_sparks_per_session=0,
            mechanic=SparkMechanicDef(spend="none", description="."),
        )
        assert s.base_sparks_per_session == 0

    def test_earn_methods_default_empty(self):
        s = SparkDef(
            base_sparks_per_session=3,
            mechanic=SparkMechanicDef(spend="per_spark", description="."),
        )
        assert s.earn_methods == []

    def test_earn_methods_list(self):
        s = SparkDef(
            base_sparks_per_session=3,
            mechanic=SparkMechanicDef(spend="per_spark", description="."),
            earn_methods=[SparkEarnMethod(id="mm_award", label="MM Award", description=".")],
        )
        assert len(s.earn_methods) == 1


# ---------------------------------------------------------------------------
# AdvancementDef
# ---------------------------------------------------------------------------

class TestAdvancementDef:
    def test_defaults(self):
        adv = AdvancementDef()
        assert adv.session_skill_points == 4
        assert adv.marks_per_rank == 3
        assert adv.facet_level_threshold == 6

    def test_skill_ranks_default_empty(self):
        adv = AdvancementDef()
        assert adv.skill_ranks == []

    def test_skill_point_costs_default_empty(self):
        adv = AdvancementDef()
        assert adv.skill_point_costs == []

    def test_custom_marks_per_rank(self):
        adv = AdvancementDef(marks_per_rank=5)
        assert adv.marks_per_rank == 5


# ---------------------------------------------------------------------------
# FacetFile — root model
# ---------------------------------------------------------------------------

class TestFacetFile:
    def test_minimal_facet_file(self):
        ff = FacetFile(id="minimal", name="Min", version="0.0.1")
        assert ff.id == "minimal"
        assert ff.description == ""
        assert ff.priority == 10

    def test_optional_sections_absent_means_empty(self):
        ff = FacetFile(id="empty", name="Empty", version="1.0")
        assert ff.facets == []
        assert ff.skills == []
        assert ff.techniques == {}
        assert ff.roll_resolution is None
        assert ff.spark is None
        assert ff.advancement is None

    def test_authors_defaults_empty(self):
        ff = FacetFile(id="auth", name="Authors", version="1.0")
        assert ff.authors == []

    def test_priority_default_is_10(self):
        ff = FacetFile(id="prio", name="Priority", version="1.0")
        assert ff.priority == 10

    def test_base_priority_override(self):
        ff = FacetFile(id="base", name="Base", version="1.0", priority=0)
        assert ff.priority == 0


# ---------------------------------------------------------------------------
# id_is_slug validator
# ---------------------------------------------------------------------------

class TestIdSlugValidator:
    def test_valid_slug_alphanumeric(self):
        ff = FacetFile(id="basemod", name="X", version="1")
        assert ff.id == "basemod"

    def test_valid_slug_with_hyphens(self):
        ff = FacetFile(id="my-mod", name="X", version="1")
        assert ff.id == "my-mod"

    def test_valid_slug_with_underscores(self):
        ff = FacetFile(id="my_mod", name="X", version="1")
        assert ff.id == "my_mod"

    def test_slug_with_spaces_rejected(self):
        with pytest.raises(ValidationError):
            FacetFile(id="invalid slug", name="X", version="1")

    def test_slug_with_special_chars_rejected(self):
        with pytest.raises(ValidationError):
            FacetFile(id="mod!@#", name="X", version="1")

    def test_empty_id_rejected(self):
        with pytest.raises(ValidationError):
            FacetFile(id="", name="X", version="1")
