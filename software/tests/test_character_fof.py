"""Tests for Character.to_fof() / from_fof() serialization."""
import sys
import os
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("FACETS_DIR", str(Path(__file__).parent.parent / "facets"))
os.environ.setdefault("DATA_DIR", str(Path(__file__).parent / "_test_data"))
os.environ.setdefault("SECRET_KEY", "test-secret-key-do-not-use-in-production")

from app.game.character import Character, SkillState, create_default_character
from app.facets.registry import build_ruleset

SPEC_EXAMPLES = Path(__file__).parent.parent.parent / "spec" / "examples"
CHARACTER_FOF = SPEC_EXAMPLES / "character-example.fof"


@pytest.fixture(scope="module")
def ruleset():
    return build_ruleset([])


@pytest.fixture(scope="module")
def valid_attributes():
    return {
        "strength": 1,
        "dexterity": 2,
        "constitution": 2,
        "intelligence": 3,
        "wisdom": 3,
        "knowledge": 2,
        "spirit": 1,
        "luck": 2,
        "charisma": 2,
    }


@pytest.fixture(scope="module")
def sample_character(ruleset, valid_attributes):
    char, errors = create_default_character(
        name="Zahna",
        player_name="Zahna",
        primary_facet="mind",
        attributes=valid_attributes,
        ruleset=ruleset,
    )
    assert not errors
    # Give Zahna some non-default skill state
    char.advance_skill("investigation", 5, ruleset)  # practiced + 2 marks
    char.sparks = 2
    char.facet_level = 1
    char.rank_advances_this_facet_level = 3
    return char


MODULE_REFS = [{"id": "base", "version": "0.1.0"}]
SESSION_ID = "abc12345-0000-0000-0000-000000000000"


class TestToFof:
    def test_to_fof_returns_dict(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        assert isinstance(result, dict)

    def test_to_fof_type_is_character(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        assert result["type"] == "character"

    def test_to_fof_fof_version(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        assert result["fof_version"] == "0.1"

    def test_to_fof_id_is_slug_prefixed(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        assert result["id"].startswith("zahna-")
        assert result["id"].endswith(SESSION_ID[:8])

    def test_to_fof_character_block_fields(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        char = result["character"]
        assert char["name"] == "Zahna"
        assert char["player_name"] == "Zahna"
        assert char["primary_facet"] == "mind"
        assert char["sparks"] == 2
        assert char["facet_level"] == 1

    def test_to_fof_skips_default_skills(self, sample_character):
        """Only non-default skills (rank != novice or marks != 0) appear in output."""
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        skills = result["character"]["skills"]
        # investigation was advanced — must be present
        assert "investigation" in skills
        # athletics was never touched — must not appear
        assert "athletics" not in skills

    def test_to_fof_investigation_state(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        inv = result["character"]["skills"]["investigation"]
        assert inv["rank"] == "practiced"
        assert inv["marks"] == 2

    def test_to_fof_module_refs(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        assert result["ruleset"]["modules"] == MODULE_REFS

    def test_to_fof_yaml_roundtrip(self, sample_character):
        """to_fof() output should survive a yaml.dump / yaml.safe_load cycle."""
        fof_dict = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        yaml_str = yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)
        restored = yaml.safe_load(yaml_str)
        assert restored["type"] == "character"
        assert restored["character"]["name"] == fof_dict["character"]["name"]


class TestFromFof:
    def test_from_fof_wrong_type_raises(self):
        with pytest.raises(ValueError, match="character"):
            Character.from_fof({"type": "ruleset", "character": {}})

    def test_from_fof_missing_character_block_raises(self):
        with pytest.raises(ValueError, match="'character' block"):
            Character.from_fof({"type": "character"})

    def test_from_fof_missing_required_field_raises(self):
        with pytest.raises(ValueError, match="player_name"):
            Character.from_fof({
                "type": "character",
                "character": {"name": "X", "primary_facet": "body", "attributes": {}},
            })

    def test_from_fof_returns_character_instance(self, ruleset, valid_attributes):
        fof_dict = {
            "type": "character",
            "character": {
                "name": "Zahna",
                "player_name": "Zahna",
                "primary_facet": "mind",
                "attributes": valid_attributes,
                "skills": {"investigation": {"rank": "practiced", "marks": 2}},
                "sparks": 2,
                "session_skill_points_remaining": 4,
                "facet_level": 1,
                "rank_advances_this_facet_level": 3,
                "techniques": ["forcing_hand"],
            },
        }
        char = Character.from_fof(fof_dict)
        assert isinstance(char, Character)
        assert char.name == "Zahna"
        assert char.primary_facet == "mind"
        assert char.sparks == 2
        assert char.facet_level == 1
        assert "investigation" in char.skills
        assert char.skills["investigation"].rank == "practiced"
        assert char.skills["investigation"].marks == 2
        assert "forcing_hand" in char.techniques

    def test_from_fof_character_example_file(self, ruleset):
        """Loading the canonical character-example.fof should produce a valid character."""
        raw = yaml.safe_load(CHARACTER_FOF.read_text(encoding="utf-8"))
        char = Character.from_fof(raw)
        errors = char.validate_against_ruleset(ruleset)
        assert errors == [], f"Validation errors: {errors}"
        assert char.name == "Zahna"
        assert char.primary_facet == "mind"
        assert char.sparks == 2

    def test_from_fof_character_example_skills(self, ruleset):
        raw = yaml.safe_load(CHARACTER_FOF.read_text(encoding="utf-8"))
        char = Character.from_fof(raw)
        # investigation: practiced, 2 marks
        assert char.skills["investigation"].rank == "practiced"
        assert char.skills["investigation"].marks == 2
        # perception: novice, 1 mark
        assert char.skills["perception"].rank == "novice"
        assert char.skills["perception"].marks == 1


class TestRoundTrip:
    def test_to_fof_from_fof_preserves_core_fields(self, sample_character):
        fof_dict = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        restored = Character.from_fof(fof_dict)

        assert restored.name == sample_character.name
        assert restored.player_name == sample_character.player_name
        assert restored.primary_facet == sample_character.primary_facet
        assert restored.attributes == sample_character.attributes
        assert restored.sparks == sample_character.sparks
        assert restored.facet_level == sample_character.facet_level
        assert restored.rank_advances_this_facet_level == sample_character.rank_advances_this_facet_level

    def test_to_fof_from_fof_preserves_non_default_skills(self, sample_character):
        fof_dict = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        restored = Character.from_fof(fof_dict)

        assert "investigation" in restored.skills
        assert restored.skills["investigation"].rank == sample_character.skills["investigation"].rank
        assert restored.skills["investigation"].marks == sample_character.skills["investigation"].marks

    def test_to_fof_from_fof_omits_default_skills(self, sample_character):
        """Skills at default state (novice/0) are not preserved — that is correct."""
        fof_dict = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        restored = Character.from_fof(fof_dict)
        # athletics was never advanced — absent from restored (implicitly novice/0)
        assert "athletics" not in restored.skills

    def test_to_fof_from_fof_techniques(self, ruleset, valid_attributes):
        char, _ = create_default_character(
            name="Bruiser",
            player_name="Player2",
            primary_facet="body",
            attributes=valid_attributes,
            ruleset=ruleset,
        )
        char.techniques = ["forcing_hand", "weapon_mastery"]
        fof_dict = char.to_fof(MODULE_REFS, SESSION_ID)
        restored = Character.from_fof(fof_dict)
        assert set(restored.techniques) == {"forcing_hand", "weapon_mastery"}
