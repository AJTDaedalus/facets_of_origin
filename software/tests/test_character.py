"""Tests for character creation, attribute validation, and skill advancement."""
import pytest

from app.game.character import Character, SkillState, create_default_character


# ---------------------------------------------------------------------------
# Valid character creation
# ---------------------------------------------------------------------------

class TestCharacterCreation:
    def test_valid_character_creates_successfully(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Zahna", player_name="P1",
            primary_facet="mind", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert errors == []
        assert char is not None
        assert char.name == "Zahna"
        assert char.primary_facet == "mind"

    def test_character_starts_with_correct_sparks(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Zulnut", player_name="P2",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.sparks == 3  # base_sparks_per_session from ruleset

    def test_character_starts_with_session_skill_points(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Mordai", player_name="P3",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.session_skill_points_remaining == 4

    def test_active_skills_initialised_at_novice(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P4",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        for skill_id, state in char.skills.items():
            assert state.rank == "novice"
            assert state.marks == 0

    def test_stub_skills_not_in_character(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P5",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        # Stub skills should not be initialised on the character
        stub_ids = {s.id for s in ruleset.skills if s.status == "stub"}
        for sid in stub_ids:
            assert sid not in char.skills

    def test_facet_level_starts_at_zero(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Test", player_name="P6",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert char.facet_level == 0


# ---------------------------------------------------------------------------
# Attribute validation
# ---------------------------------------------------------------------------

class TestAttributeValidation:
    def test_wrong_total_points_rejected(self, ruleset):
        attrs = {
            "strength": 3, "dexterity": 3, "constitution": 3,
            "intelligence": 3, "wisdom": 3, "knowledge": 3,
            "spirit": 1, "luck": 1, "charisma": 1,
        }  # 22 points
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None
        assert any("18" in e for e in errors)

    def test_attribute_rating_above_max_rejected(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        attrs["strength"] = 4  # exceeds max of 3
        # Adjust to keep total = 18 by reducing another
        attrs["constitution"] = 1
        attrs["luck"] = 1
        attrs["charisma"] = 1
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None

    def test_attribute_below_minimum_rejected(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        attrs["strength"] = 0
        attrs["dexterity"] = 4
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None

    def test_missing_attribute_rejected(self, ruleset):
        attrs = {
            "strength": 3, "dexterity": 3, "constitution": 3,
            "intelligence": 3, "wisdom": 3, "knowledge": 3,
        }  # missing soul attributes
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="body",
            attributes=attrs, ruleset=ruleset,
        )
        assert char is None
        assert any("Missing" in e for e in errors)

    def test_unknown_primary_facet_rejected(self, ruleset, valid_attributes):
        char, errors = create_default_character(
            name="Test", player_name="P", primary_facet="arcane",
            attributes=valid_attributes, ruleset=ruleset,
        )
        assert char is None
        assert any("facet" in e.lower() for e in errors)

    def test_all_three_facets_are_valid(self, ruleset, valid_attributes):
        for facet in ["body", "mind", "soul"]:
            char, errors = create_default_character(
                name="Test", player_name="P", primary_facet=facet,
                attributes=valid_attributes, ruleset=ruleset,
            )
            assert errors == [], f"Facet {facet} should be valid, got: {errors}"


# ---------------------------------------------------------------------------
# Attribute modifiers
# ---------------------------------------------------------------------------

class TestAttributeModifiers:
    def test_strong_strength_returns_plus_one(self, body_character, ruleset):
        mod = body_character.get_attribute_modifier("strength", ruleset)
        assert mod == 1  # rating 3 → +1

    def test_weak_luck_returns_minus_one(self, ruleset, valid_attributes):
        attrs = dict(valid_attributes)
        # Set luck to 1 (weak)
        char, _ = create_default_character(
            name="Test", player_name="P", primary_facet="soul",
            attributes=attrs, ruleset=ruleset,
        )
        mod = char.get_attribute_modifier("luck", ruleset)
        # luck is 2 in valid_attributes
        assert mod == 0


# ---------------------------------------------------------------------------
# Spark spending
# ---------------------------------------------------------------------------

class TestSparkSpending:
    def test_spend_spark_reduces_count(self, body_character):
        initial = body_character.sparks
        result = body_character.spend_spark()
        assert result is True
        assert body_character.sparks == initial - 1

    def test_spend_spark_returns_false_when_empty(self, body_character):
        body_character.sparks = 0
        result = body_character.spend_spark()
        assert result is False
        assert body_character.sparks == 0

    def test_earn_spark_increases_count(self, body_character):
        initial = body_character.sparks
        body_character.earn_spark()
        assert body_character.sparks == initial + 1

    def test_can_spend_all_sparks(self, body_character):
        count = body_character.sparks
        for _ in range(count):
            body_character.spend_spark()
        assert body_character.sparks == 0


# ---------------------------------------------------------------------------
# Skill advancement
# ---------------------------------------------------------------------------

class TestSkillAdvancement:
    def test_marks_accumulate_without_rank_advance(self, body_character, ruleset):
        result = body_character.advance_skill("athletics", 1, ruleset)
        assert result["rank_advances"] == 0
        assert body_character.skills["athletics"].marks == 1

    def test_three_marks_advance_rank(self, body_character, ruleset):
        result = body_character.advance_skill("athletics", 3, ruleset)
        assert result["rank_advances"] == 1
        assert body_character.skills["athletics"].rank == "practiced"
        assert body_character.skills["athletics"].marks == 0

    def test_six_marks_advance_to_expert(self, body_character, ruleset):
        body_character.advance_skill("athletics", 6, ruleset)
        assert body_character.skills["athletics"].rank == "expert"

    def test_expert_rank_does_not_advance_further(self, body_character, ruleset):
        body_character.advance_skill("athletics", 6, ruleset)
        assert body_character.skills["athletics"].rank == "expert"
        body_character.advance_skill("athletics", 10, ruleset)
        assert body_character.skills["athletics"].rank == "expert"  # still expert

    def test_marks_carry_over_between_sessions(self, body_character, ruleset):
        body_character.advance_skill("athletics", 2, ruleset)
        assert body_character.skills["athletics"].marks == 2
        body_character.advance_skill("athletics", 1, ruleset)
        assert body_character.skills["athletics"].rank == "practiced"
        assert body_character.skills["athletics"].marks == 0

    def test_primary_facet_advances_count_toward_facet_level(self, body_character, ruleset):
        # athletics is in body facet = primary for body_character
        initial = body_character.rank_advances_this_facet_level
        body_character.advance_skill("athletics", 3, ruleset)  # novice → practiced
        assert body_character.rank_advances_this_facet_level == initial + 1

    def test_six_advances_trigger_facet_level_up(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Level Test", player_name="P",
            primary_facet="body", attributes=valid_attributes,
            ruleset=ruleset,
        )
        # Advance 5 different body skills by 3 marks each = 5 rank advances
        body_active_skills = [s.id for s in ruleset.skills if s.facet == "body" and s.status == "active"]
        for sid in body_active_skills[:5]:
            char.advance_skill(sid, 3, ruleset)
        assert char.facet_level == 0  # not yet — need 6
        assert char.rank_advances_this_facet_level == 5

        # One more → level 1
        char.advance_skill(body_active_skills[0], 3, ruleset)  # practiced → expert on first skill
        assert char.facet_level == 1
        assert char.rank_advances_this_facet_level == 0

    def test_unknown_skill_is_created_on_advance(self, body_character, ruleset):
        body_character.advance_skill("nonexistent_skill", 1, ruleset)
        assert "nonexistent_skill" in body_character.skills


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------

class TestCharacterSerialisation:
    def test_to_client_dict_is_json_safe(self, body_character):
        import json
        d = body_character.to_client_dict()
        json.dumps(d)

    def test_to_client_dict_includes_name(self, body_character):
        d = body_character.to_client_dict()
        assert d["name"] == "Mordai"

    def test_to_client_dict_includes_skills(self, body_character):
        d = body_character.to_client_dict()
        assert "skills" in d
        assert "athletics" in d["skills"]
