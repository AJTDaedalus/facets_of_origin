"""Unit tests for every Pydantic schema class in app/facets/schema.py."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.facets.schema import (
    AdvancementDef,
    ArmorDef,
    ArmorEntryDef,
    ArmorResolveBonusDef,
    AttributeDistribution,
    AttributeRating,
    AttributesDef,
    BranchDef,
    CharacterFacetDef,
    ContestedRollDef,
    ContestedRollVsNpcDef,
    ContestedRollVsPcDef,
    DeathDef,
    DifficultyModifier,
    EnemyDurabilityDef,
    LineageDefinition,
    ItemDefinition,
    StrikeRiderDef,
    EquipmentDef,
    FacetFile,
    FacetTreeDef,
    GroupRollDef,
    HazardsDef,
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
    SparkVariantsDef,
    StepTriggerDef,
    StrikeDepletionDef,
    TechniqueDef,
    ThreatClockDef,
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

    # -- TD-4: difficulty_step / step_trigger (B4 Q1) --------------------

    def test_no_step_parses_unchanged(self):
        """Every pre-existing Technique omits these fields and must parse
        exactly as before — both optional fields default to None."""
        t = TechniqueDef(id="forcing_hand", name="Forcing Hand", description="...")
        assert t.difficulty_step is None
        assert t.step_trigger is None

    def test_auto_trigger_technique_parses(self):
        t = TechniqueDef(
            id="weapon_mastery", name="Weapon Mastery", description=".",
            difficulty_step="easier",
            step_trigger=StepTriggerDef(kind="auto", match="weapon_type", against="choice"),
        )
        assert t.difficulty_step == "easier"
        assert t.step_trigger.kind == "auto"
        assert t.step_trigger.match == "weapon_type"
        assert t.step_trigger.against == "choice"

    def test_declared_trigger_technique_parses(self):
        t = TechniqueDef(
            id="the_uncanny_angle", name="The Uncanny Angle", description=".",
            difficulty_step="easier",
            step_trigger=StepTriggerDef(kind="declared"),
        )
        assert t.step_trigger.kind == "declared"
        assert t.step_trigger.match is None
        assert t.step_trigger.against is None

    def test_invalid_step_trigger_kind_raises(self):
        with pytest.raises(ValidationError):
            StepTriggerDef(kind="bogus")

    def test_invalid_difficulty_step_raises(self):
        with pytest.raises(ValidationError):
            TechniqueDef(id="x", name="X", description=".", difficulty_step="sideways")

    # -- TD-19: choices (DESIGN §8) ----------------------------------------

    def test_no_choices_parses_unchanged(self):
        """Every Technique that predates TD-19 — including domain-granting
        ones, which build their picker from the domain catalog instead —
        omits `choices` and must parse exactly as before."""
        t = TechniqueDef(id="forcing_hand", name="Forcing Hand", description="...")
        assert t.choices is None

    def test_technique_with_choices_parses(self):
        t = TechniqueDef(
            id="weapon_mastery", name="Weapon Mastery", description=".",
            has_choice=True, choice_prompt="Choose a weapon type.",
            choices=["blades", "blunt", "polearms", "unarmed"],
        )
        assert t.choices == ["blades", "blunt", "polearms", "unarmed"]


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

    def test_variants_default_off(self):
        s = SparkDef(
            base_sparks_per_session=3,
            mechanic=SparkMechanicDef(spend="per_spark", description="."),
        )
        assert s.variants.refund_on_failed_pretechnique_cast is False


class TestSparkEarnMethod:
    def test_structured_defaults_false(self):
        m = SparkEarnMethod(id="graceful_fail", label="The Graceful Fail", description=".")
        assert m.structured is False

    def test_structured_can_be_true(self):
        m = SparkEarnMethod(
            id="graceful_fail", label="The Graceful Fail", description=".", structured=True
        )
        assert m.structured is True

    def test_target_per_session_default_empty(self):
        m = SparkEarnMethod(id="mm_award", label="MM Award", description=".")
        assert m.target_per_session == ""


class TestSparkVariantsDef:
    def test_defaults_off(self):
        v = SparkVariantsDef()
        assert v.refund_on_failed_pretechnique_cast is False

    def test_can_be_enabled(self):
        v = SparkVariantsDef(refund_on_failed_pretechnique_cast=True)
        assert v.refund_on_failed_pretechnique_cast is True


# ---------------------------------------------------------------------------
# ThreatClockDef / HazardsDef / DeathDef (D4 — PHB III.2)
# ---------------------------------------------------------------------------

class TestThreatClockDef:
    def test_defaults(self):
        c = ThreatClockDef()
        assert c.segments == 4
        assert c.advances_on == ["partial_success", "failure"]
        assert c.wind_back_cost == "1_action"
        assert c.wind_back_requires_roll is False

    def test_segments_below_minimum_rejected(self):
        with pytest.raises(ValidationError):
            ThreatClockDef(segments=0)

    def test_custom_segments(self):
        c = ThreatClockDef(segments=6)
        assert c.segments == 6

    def test_wind_back_never_requires_roll_by_default(self):
        # Brain ruling (BRIEF §EF4): a rolled wind-back would let a 7-9
        # advance the very clock being wound.
        c = ThreatClockDef()
        assert c.wind_back_requires_roll is False


class TestHazardsDef:
    def test_default_threat_clock(self):
        h = HazardsDef()
        assert h.threat_clock.segments == 4

    def test_custom_threat_clock(self):
        h = HazardsDef(threat_clock=ThreatClockDef(segments=3))
        assert h.threat_clock.segments == 3


class TestDeathDef:
    def test_defaults(self):
        d = DeathDef()
        assert d.broken_is_lethal is False
        assert d.doom_gate == ["permanent_scar", "heroic_death"]

    def test_broken_is_lethal_is_always_false_by_default(self):
        d = DeathDef()
        assert d.broken_is_lethal is False


# ---------------------------------------------------------------------------
# AdvancementDef
# ---------------------------------------------------------------------------

class TestAdvancementDef:
    def test_defaults_match_canon(self):
        """Schema defaults must equal facets/base/facet.yaml, not an earlier
        revision. v0.3 moved facet_level_threshold 6 -> 5 and
        major_advancement_threshold 4 -> 3; D16 moved the threshold again
        (5 -> 3) and replaced the flat mark cost with the 3/5/8 curve. The
        defaults have lagged before, so any Facet omitting them would silently
        load stale advancement pacing.
        """
        adv = AdvancementDef()
        assert adv.session_skill_points == 4
        assert (adv.marks_per_rank.practiced,
                adv.marks_per_rank.expert,
                adv.marks_per_rank.master) == (3, 5, 8)
        assert adv.facet_level_threshold == 3
        assert adv.major_advancement_threshold == 3

    @pytest.mark.parametrize("field", [
        "session_skill_points",
        "facet_level_threshold",
        "major_advancement_threshold",
    ])
    def test_defaults_do_not_drift_from_base_facet(self, field):
        """Pin the defaults to the base Facet so a future ruleset change to
        facet.yaml cannot leave the schema behind again."""
        import yaml
        from app.config import settings

        with open(settings.facets_dir / "base" / "facet.yaml", encoding="utf-8") as fh:
            advancement = yaml.safe_load(fh)["advancement"]

        assert getattr(AdvancementDef(), field) == advancement[field], (
            f"AdvancementDef.{field} default disagrees with facets/base/facet.yaml"
        )

    def test_skill_ranks_default_empty(self):
        adv = AdvancementDef()
        assert adv.skill_ranks == []

    def test_skill_point_costs_default_empty(self):
        adv = AdvancementDef()
        assert adv.skill_point_costs == []

    def test_custom_marks_per_rank(self):
        adv = AdvancementDef(marks_per_rank={"practiced": 2, "expert": 4, "master": 6})
        assert adv.marks_per_rank.for_rank("expert") == 4

    def test_marks_per_rank_default_does_not_drift_from_base_facet(self):
        """The per-tier curve gets its own pin — it is a mapping, not a scalar."""
        import yaml
        from app.config import settings

        with open(settings.facets_dir / "base" / "facet.yaml", encoding="utf-8") as fh:
            marks = yaml.safe_load(fh)["advancement"]["marks_per_rank"]

        default = AdvancementDef().marks_per_rank
        for rank, value in marks.items():
            assert default.for_rank(rank) == value, (
                f"AdvancementDef.marks_per_rank.{rank} disagrees with base/facet.yaml"
            )

    def test_rank_caps_default_does_not_drift_from_base_facet(self):
        """Caps default to uncapped, but base must state them — a Facet that
        omits the block is homebrew and stays unconstrained on purpose."""
        import yaml
        from app.config import settings

        with open(settings.facets_dir / "base" / "facet.yaml", encoding="utf-8") as fh:
            caps = yaml.safe_load(fh)["advancement"]["rank_caps"]

        assert caps == {"beyond_practiced": 3, "master": 1}
        assert AdvancementDef().rank_caps.beyond_practiced is None
        assert AdvancementDef().rank_caps.master is None

    def test_legacy_flat_marks_per_rank_deprecates(self):
        with pytest.warns(DeprecationWarning, match="marks_per_rank"):
            adv = AdvancementDef(marks_per_rank=3)
        assert adv.marks_per_rank.for_rank("master") == 3


# ---------------------------------------------------------------------------
# ArmorEntryDef / ArmorDef (D2 — PC per-scene downgrade budget)
# ---------------------------------------------------------------------------

class TestArmorEntryDef:
    def test_defaults(self):
        a = ArmorEntryDef()
        assert a.downgrades_per_scene == 2
        assert a.tiers_reduced == 1

    def test_custom_values(self):
        a = ArmorEntryDef(downgrades_per_scene=4, tiers_reduced=1)
        assert a.downgrades_per_scene == 4


class TestArmorDef:
    def test_defaults(self):
        a = ArmorDef()
        assert a.light.downgrades_per_scene == 2
        assert a.heavy.downgrades_per_scene == 4

    def test_heavy_outlasts_light(self):
        a = ArmorDef()
        assert a.heavy.downgrades_per_scene > a.light.downgrades_per_scene


# ---------------------------------------------------------------------------
# StrikeDepletionDef / ArmorResolveBonusDef / EnemyDurabilityDef (D1 — Resolve)
# ---------------------------------------------------------------------------

class TestStrikeDepletionDef:
    def test_defaults(self):
        d = StrikeDepletionDef()
        assert d.full_success == 2
        assert d.partial_success == 1
        assert d.failure == 0


class TestArmorResolveBonusDef:
    def test_defaults(self):
        b = ArmorResolveBonusDef()
        assert b.none == 0
        assert b.light == 1
        assert b.heavy == 2


class TestEnemyDurabilityDef:
    def test_defaults(self):
        e = EnemyDurabilityDef()
        assert e.strike_depletion.full_success == 2
        assert e.armor_resolve_bonus.heavy == 2
        assert e.mook_removed_on == "partial_success"
        assert e.armored_mook_removed_on == "full_success"

    def test_custom_construction(self):
        e = EnemyDurabilityDef(
            strike_depletion=StrikeDepletionDef(full_success=3, partial_success=1, failure=0),
            armor_resolve_bonus=ArmorResolveBonusDef(none=0, light=2, heavy=3),
            mook_removed_on="full_success",
            armored_mook_removed_on="full_success",
        )
        assert e.strike_depletion.full_success == 3
        assert e.armor_resolve_bonus.light == 2

    # -- open_clears is a closed set (R2, BRIEF_fun_second_act §2) ----------
    # The lifecycle of the Open tag is a rule, and a ruleset that names a
    # lifecycle the engine does not implement must fail at load, not at the
    # table. Both values stay legal: `end_exchange` is the base ruleset's
    # choice, `enemy_action` is what a setting may choose and what Series 12
    # Part A's regression floor runs under.

    def test_open_clears_accepts_enemy_action(self):
        assert EnemyDurabilityDef(open_clears="enemy_action").open_clears == "enemy_action"

    def test_open_clears_accepts_end_of_exchange(self):
        e = EnemyDurabilityDef(open_clears="end_of_exchange")
        assert e.open_clears == "end_of_exchange"

    def test_open_clears_rejects_unknown_lifecycle(self):
        with pytest.raises(ValidationError):
            EnemyDurabilityDef(open_clears="never")

    # -- R3: the 10+ rider menu (BRIEF_fun_second_act §3) -------------------
    # A 10+ Strike depletes 2 Resolve and chooses one rider. The menu is
    # data so the app can render the confirm from it and a setting can add
    # or remove one; the *effects* are engine, so a rider naming an effect
    # the engine does not implement must fail at load.

    def test_strike_riders_default_to_the_two_the_book_prints(self):
        """Cover was drafted as a third and cut at the gate (Series 12 Part
        C, D20) — it undid R2 by shortening the Boss fight back to a median
        2 exchanges. Its effect stays implemented for a setting to offer
        deliberately; the core menu is two."""
        e = EnemyDurabilityDef()
        assert [r.id for r in e.strike_riders] == ["open", "position"]

    def test_cover_remains_constructible_for_a_setting(self):
        rider = StrikeRiderDef(id="cover", label="Cover",
                               effect="free_reaction_ally",
                               duration="end_of_exchange")
        assert rider.effect == "free_reaction_ally"

    def test_strike_rider_carries_label_effect_and_duration(self):
        e = EnemyDurabilityDef()
        open_rider = next(r for r in e.strike_riders if r.id == "open")
        assert open_rider.label == "Open"
        assert open_rider.effect == "easy_tag"
        assert open_rider.duration == "end_of_exchange"

    def test_strike_riders_reject_an_unimplemented_effect(self):
        with pytest.raises(ValidationError):
            StrikeRiderDef(id="banish", label="Banish", effect="delete_enemy",
                           duration="end_of_exchange")

    def test_strike_riders_reject_an_unknown_duration(self):
        with pytest.raises(ValidationError):
            StrikeRiderDef(id="open", label="Open", effect="easy_tag",
                           duration="forever")

    def test_a_setting_may_reshape_the_menu(self):
        """The menu is data. A setting may trim to one rider or add Cover
        back; neither is a schema error."""
        one = EnemyDurabilityDef(strike_riders=[
            StrikeRiderDef(id="open", label="Open", effect="easy_tag",
                           duration="end_of_exchange"),
        ])
        assert [r.id for r in one.strike_riders] == ["open"]
        three = EnemyDurabilityDef(strike_riders=[
            StrikeRiderDef(id="open", label="Open", effect="easy_tag",
                           duration="end_of_exchange"),
            StrikeRiderDef(id="position", label="Position",
                           effect="easy_tag_next_roll",
                           duration="next_roll_or_end_of_next_exchange"),
            StrikeRiderDef(id="cover", label="Cover",
                           effect="free_reaction_ally",
                           duration="end_of_exchange"),
        ])
        assert [r.id for r in three.strike_riders] == ["open", "position", "cover"]


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
        assert ff.hazards is None
        assert ff.death is None

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


# ---------------------------------------------------------------------------
# ContestedRollDef / GroupRollDef — sync-M-10, M-11 (D11: encoding only, no
# engine work — the contested handler already exists and group rolls wait
# for a playtest to demand them).
# ---------------------------------------------------------------------------

class TestContestedRollDef:
    def test_defaults_match_phb_iii1(self):
        block = ContestedRollDef()
        assert block.vs_npc.only_pc_rolls is True
        assert block.vs_pc.both_roll is True
        assert block.vs_pc.higher_wins is True
        assert block.vs_pc.tie_result == "both_partial_success"

    def test_base_ruleset_loads_and_validates_the_block(self, ruleset):
        block = ruleset.roll_resolution.contested_roll
        assert isinstance(block, ContestedRollDef)
        assert block.vs_pc.tie_result == "both_partial_success"

    def test_contested_handler_tie_rule_matches_yaml(self, ruleset):
        """The WebSocket contested-roll handler (websocket.py:_handle_contested_roll)
        reports `winner = "tie"` when both totals are equal — the same
        comparison, reproduced here — and the yaml's `tie_result` names what
        that tie means under PHB III.1: both sides get a partial success,
        not a re-roll or a stalemate."""
        total_a = 9
        total_b = 9
        winner = "player_a" if total_a > total_b else ("player_b" if total_b > total_a else "tie")
        assert winner == "tie"
        assert ruleset.roll_resolution.contested_roll.vs_pc.tie_result == "both_partial_success"


class TestGroupRollDef:
    def test_defaults_match_phb_iii1(self):
        block = GroupRollDef()
        assert block.majority_rule == "partial_success_or_better_counts"
        assert block.lead_roller_alternative is True

    def test_base_ruleset_loads_and_validates_the_block(self, ruleset):
        block = ruleset.roll_resolution.group_roll
        assert isinstance(block, GroupRollDef)
        assert block.majority_rule == "partial_success_or_better_counts"
        assert block.lead_roller_alternative is True


# ---------------------------------------------------------------------------
# EquipmentDef / weapon_categories — sync-M-12: IV.1:13-19 weapon category ->
# attribute reference table. Reference data only — the engine stays
# deliberately permissive on which attribute a Strike uses.
# ---------------------------------------------------------------------------

class TestDifficultyStepMetadataInBaseFacet:
    """TD-6 (B4 Q1): exactly five Techniques in facet.yaml carry
    `difficulty_step` metadata. Pinned by name so a sixth cannot be added
    without a deliberate change to this test — `pressure_point` is
    deliberately deferred (DESIGN §2.5, docs/TODO.md T7) and must stay out."""

    EXPECTED = {
        "weapon_mastery": ("easier", "auto"),
        "acclimated": ("easier", "auto"),
        "field_of_mastery": ("easier", "auto"),
        "steady_hand": ("easier", "auto"),
        "the_uncanny_angle": ("easier", "declared"),
    }

    def _techniques_with_step(self, ruleset):
        found = {}
        for facet_id, tree in ruleset.techniques.items():
            for branch in tree.branches:
                for tier_def in branch.tiers:
                    for tech in tier_def.techniques:
                        if tech.difficulty_step is not None:
                            found[tech.id] = tech
        return found

    def test_exactly_five_techniques_carry_the_step(self, ruleset):
        found = self._techniques_with_step(ruleset)
        assert set(found) == set(self.EXPECTED), (
            f"expected exactly {sorted(self.EXPECTED)}, found {sorted(found)}"
        )

    def test_each_technique_matches_its_expected_step_and_trigger_kind(self, ruleset):
        found = self._techniques_with_step(ruleset)
        for tech_id, (expected_step, expected_kind) in self.EXPECTED.items():
            tech = found[tech_id]
            assert tech.difficulty_step == expected_step, tech_id
            assert tech.step_trigger is not None, tech_id
            assert tech.step_trigger.kind == expected_kind, tech_id

    def test_pressure_point_deliberately_carries_no_step(self, ruleset):
        pressure_point = ruleset.get_technique("pressure_point")
        assert pressure_point is not None
        assert pressure_point.difficulty_step is None
        assert pressure_point.step_trigger is None

    def test_auto_triggers_match_declared_fields(self, ruleset):
        found = self._techniques_with_step(ruleset)
        assert found["weapon_mastery"].step_trigger.match == "weapon_type"
        assert found["weapon_mastery"].step_trigger.against == "choice"
        assert found["acclimated"].step_trigger.match == "hazard_type"
        assert found["acclimated"].step_trigger.against == "choice"
        assert found["field_of_mastery"].step_trigger.match == "knowledge_field"
        assert found["field_of_mastery"].step_trigger.against == "choice"
        assert found["steady_hand"].step_trigger.match == "skill_id"
        assert found["steady_hand"].step_trigger.against == "finesse"


class TestFinalBlowOverrideFlag:
    """TD-12 (B4 Q3): exactly one Technique in facet.yaml carries
    `removes_target_from_conflict`, and it is *The Final Blow*. Pinned by
    name, same pattern as `TestDifficultyStepMetadataInBaseFacet`, so a
    second override can't creep in without a deliberate test change —
    overrides must stay greppable and countable."""

    def _techniques_with_override_flag(self, ruleset):
        found = {}
        for facet_id, tree in ruleset.techniques.items():
            for branch in tree.branches:
                for tier_def in branch.tiers:
                    for tech in tier_def.techniques:
                        if tech.removes_target_from_conflict:
                            found[tech.id] = tech
        return found

    def test_exactly_one_technique_carries_the_flag(self, ruleset):
        found = self._techniques_with_override_flag(ruleset)
        assert set(found) == {"the_final_blow"}, (
            f"expected only 'the_final_blow', found {sorted(found)}"
        )

    def test_the_final_blow_carries_the_flag(self, ruleset):
        tech = ruleset.get_technique("the_final_blow")
        assert tech is not None
        assert tech.removes_target_from_conflict is True

    def test_an_ordinary_technique_does_not_carry_the_flag(self, ruleset):
        """Backward compatibility: a Technique that predates TD-12 parses
        with the flag defaulting to False."""
        unstoppable = ruleset.get_technique("unstoppable")
        assert unstoppable is not None
        assert unstoppable.removes_target_from_conflict is False


class TestWeaponCategories:
    def test_base_ruleset_loads_equipment_block(self, ruleset):
        assert isinstance(ruleset.equipment, EquipmentDef)

    def test_all_five_categories_present_with_attributes(self, ruleset):
        categories = ruleset.equipment.weapon_categories
        assert set(categories) == {"heavy", "standard", "light", "ranged", "unarmed"}
        assert categories["heavy"].attributes == ["strength"]
        assert categories["standard"].attributes == ["strength", "dexterity"]
        assert categories["light"].attributes == ["dexterity"]
        assert categories["ranged"].attributes == ["dexterity"]
        assert categories["unarmed"].attributes == ["strength", "dexterity"]

    def test_weapon_types_present_and_orthogonal_to_categories(self, ruleset):
        """TD-18 (DESIGN §8): `weapon_types` is the separate, fictional
        vocabulary Weapon Mastery masters — it is not a subset or a rename
        of `weapon_categories` above. Only `unarmed` legitimately overlaps
        both lists; the rest are disjoint by design."""
        types = set(ruleset.equipment.weapon_types)
        assert types == {"blades", "blunt", "polearms", "unarmed"}
        categories = set(ruleset.equipment.weapon_categories)
        assert types - categories == {"blades", "blunt", "polearms"}


class TestNonDomainTechniqueChoices:
    """TD-19 (DESIGN §8): the three non-domain `has_choice` Techniques
    (Weapon Mastery, Acclimated, Field of Mastery) enumerate their options
    as data. `choice_prompt` stays the printed prose; `choices` is what the
    picker renders from — and the two must never drift apart, since the
    book and the data would then be silently telling players different
    things a Technique can be taken in."""

    NON_DOMAIN_CHOICE_TECHNIQUES = ("weapon_mastery", "acclimated", "field_of_mastery")

    def test_all_three_carry_choices(self, ruleset):
        for tech_id in self.NON_DOMAIN_CHOICE_TECHNIQUES:
            tech = ruleset.get_technique(tech_id)
            assert tech is not None, tech_id
            assert tech.choices, f"{tech_id} has no choices"

    def test_a_technique_without_choices_still_parses(self, ruleset):
        """Backward compatibility: an ordinary Technique with no `choices`
        (most of the tree) is unaffected."""
        forcing_hand = ruleset.get_technique("forcing_hand")
        assert forcing_hand is not None
        assert forcing_hand.choices is None

    def test_choices_match_the_printed_choice_prompt_text(self, ruleset):
        """The acceptance test that matters: every value in `choices` must
        appear (case-insensitively) in `choice_prompt`, so the machine-
        readable list and the book's human-readable prompt cannot drift."""
        mismatches = []
        for tech_id in self.NON_DOMAIN_CHOICE_TECHNIQUES:
            tech = ruleset.get_technique(tech_id)
            prompt = tech.choice_prompt.lower()
            for choice in tech.choices:
                if choice.lower() not in prompt:
                    mismatches.append(f"{tech_id}: '{choice}' not found in "
                                      f"choice_prompt {tech.choice_prompt!r}")
        assert not mismatches, "\n".join(mismatches)

    def test_weapon_mastery_choices_are_the_fictional_weapon_type_vocabulary(self, ruleset):
        tech = ruleset.get_technique("weapon_mastery")
        assert tech.choices == ["blades", "blunt", "polearms", "unarmed"]

    def test_acclimated_choices(self, ruleset):
        tech = ruleset.get_technique("acclimated")
        assert tech.choices == ["extreme cold", "extreme heat", "altitude", "deprivation"]

    def test_field_of_mastery_choices_are_suggestions_not_a_closed_set(self, ruleset):
        """PHB II.4a: 'or another domain with MM approval' — nothing in the
        schema or the engine enforces membership in this list (INV-8)."""
        tech = ruleset.get_technique("field_of_mastery")
        assert "history" in tech.choices
        assert "arcane theory" in tech.choices


class TestTraditionDef:
    """The tradition block decides which attribute and skill every casting
    roll uses (II.3, Rolling Magic; T4.1/D7). It was the one rules block still
    typed `dict[str, Any]`, so a misspelled key validated cleanly and silently
    rolled the other tradition's attribute and skill at the table.
    """

    def test_valid_tradition_parses(self):
        from app.facets.schema import TraditionDef
        trad = TraditionDef(attribute="spirit", skill="attune")
        assert (trad.attribute, trad.skill) == ("spirit", "attune")

    def test_misspelled_attribute_key_is_rejected(self):
        from app.facets.schema import TraditionDef
        with pytest.raises(ValidationError):
            TraditionDef(atribute="knowledge", skill="lore")

    def test_missing_skill_is_rejected(self):
        """The skill is the whole point of D7 — a tradition without one is
        an attribute-only casting rule, which is the thing D7 retired."""
        from app.facets.schema import TraditionDef
        with pytest.raises(ValidationError):
            TraditionDef(attribute="knowledge")

    def test_magic_def_traditions_are_typed(self):
        from app.facets.schema import MagicDef, TraditionDef
        magic = MagicDef(traditions={"scholarly": {"attribute": "knowledge", "skill": "lore"}})
        assert isinstance(magic.traditions["scholarly"], TraditionDef)

    def test_base_facet_traditions_load_typed(self, ruleset):
        from app.facets.schema import TraditionDef
        for key in ("intuitive", "scholarly"):
            assert isinstance(ruleset.magic.traditions[key], TraditionDef)


# ---------------------------------------------------------------------------
# LineageDefinition (D18 — Lineage as a core creation step, PHB II.5)
# ---------------------------------------------------------------------------

class TestLineageDefinition:
    """A lineage is who a character was born as, orthogonal to the Background's
    what-they-did. The core ships exactly one — Human, ungifted — and every
    other lineage belongs to a setting Facet.
    """

    def test_minimal_ungifted_lineage(self):
        lin = LineageDefinition(id="human", name="Human", description="The default.")
        assert lin.gift_domains == []
        assert lin.gift_rate is None
        assert lin.heritage is None
        assert lin.playable is True

    def test_formalizes_on_defaults_to_the_first_facet_level(self):
        """D18 option 1: blood is not study, so a Gift arrives at the first
        Facet level in any Facet and spends no Technique pick."""
        assert LineageDefinition(id="x", name="X", description="d").formalizes_on == (
            "first_facet_level")

    def test_formalizes_on_keeps_the_technique_route_reachable(self):
        """Option 2 stays legal data so a setting could choose it, even though
        the core does not."""
        lin = LineageDefinition(id="x", name="X", description="d",
                                formalizes_on="technique")
        assert lin.formalizes_on == "technique"

    def test_formalizes_on_rejects_an_unknown_route(self):
        with pytest.raises(ValidationError):
            LineageDefinition(id="x", name="X", description="d",
                              formalizes_on="whenever")

    def test_a_gifted_lineage_carries_domains_a_rate_and_a_heritage(self):
        lin = LineageDefinition(
            id="orthaen", name="Orthaen", variants=["Orthain"],
            description="Crystal-growers.", gift_domains=["crystal"],
            gift_rate="four in five",
            heritage="Reads grown crystalwork: its age, its maker's hand.",
        )
        assert lin.gift_domains == ["crystal"]
        assert lin.gift_rate == "four in five"

    def test_variants_default_to_empty(self):
        assert LineageDefinition(id="x", name="X", description="d").variants == []

    def test_playable_false_is_expressible(self):
        """Krenn and Tyndi exist in data so their NPCs can be statted honestly
        and are never offered to a player."""
        assert LineageDefinition(id="krenn", name="Krenn", description="Gone.",
                                 playable=False).playable is False


# ---------------------------------------------------------------------------
# ItemDefinition + lineage_gift / draft flags (Val'loh Facet)
# ---------------------------------------------------------------------------

class TestItemDefinition:
    """The smallest loot system the game can have: a one-use item, declared
    when it is made, released at a touch, with no roll and no arithmetic.
    """

    def test_a_consumable_charge(self):
        item = ItemDefinition(id="steady_light", name="Steady Light",
                              kind="consumable", scope="minor",
                              effect="A grown crystal sheds steady light for a scene.")
        assert item.kind == "consumable"
        assert item.scope == "minor"

    def test_kind_is_a_closed_set(self):
        with pytest.raises(ValidationError):
            ItemDefinition(id="x", name="X", kind="artifact", scope="minor",
                           effect="...")

    def test_scope_is_the_magic_scope_ladder(self):
        """A charge holds a working at a scope, so the ladder is II.3's, not
        a second vocabulary."""
        for scope in ("minor", "significant", "major"):
            assert ItemDefinition(id="x", name="X", kind="consumable",
                                  scope=scope, effect="...").scope == scope
        with pytest.raises(ValidationError):
            ItemDefinition(id="x", name="X", kind="consumable", scope="huge",
                           effect="...")


class TestDomainSettingFlags:
    def test_lineage_gift_defaults_false(self):
        from app.facets.schema import MagicDomainDef
        d = MagicDomainDef(id="fire", name="Fire", type="focused",
                           tradition="intuitive", description="...")
        assert d.lineage_gift is False
        assert d.draft is False

    def test_a_gift_domain_marks_itself(self):
        """`lineage_gift` is what keeps a setting's blood-magic out of the
        core's Tier 1 shopping list — a Soul mage in Shattered Origin cannot
        pick "Crystal"."""
        from app.facets.schema import MagicDomainDef
        d = MagicDomainDef(id="crystal", name="Crystal", type="focused",
                           tradition="intuitive", description="...",
                           lineage_gift=True, draft=True)
        assert d.lineage_gift is True
        assert d.draft is True

    def test_draft_is_a_flag_not_a_gate(self):
        """`draft: true` says the owner has not read the example intents yet.
        It must not stop the domain loading, or the Facet cannot be tested
        before it is approved."""
        from app.facets.schema import MagicDomainDef
        d = MagicDomainDef(id="x", name="X", type="focused",
                           tradition="intuitive", description="...", draft=True)
        assert d.id == "x"
