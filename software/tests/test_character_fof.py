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
    # Give Zahna some non-default skill state (PHB skill names: investigate, not investigation)
    char.advance_skill("investigate", 5, ruleset)  # practiced + 2 marks
    char.sparks = 2
    char.facet_levels = {"mind": 1}
    char.rank_advances_by_facet = {"mind": 3}
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
        # investigate was advanced — must be present
        assert "investigate" in skills
        # athletics was never touched — must not appear
        assert "athletics" not in skills

    def test_to_fof_investigate_state(self, sample_character):
        result = sample_character.to_fof(MODULE_REFS, SESSION_ID)
        inv = result["character"]["skills"]["investigate"]
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
                "skills": {"investigate": {"rank": "practiced", "marks": 2}},
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
        assert "investigate" in char.skills
        assert char.skills["investigate"].rank == "practiced"
        assert char.skills["investigate"].marks == 2
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
        # investigate: practiced, 2 marks (PHB II.4b skill name)
        assert char.skills["investigate"].rank == "practiced"
        assert char.skills["investigate"].marks == 2
        # survival: novice, 1 mark (PHB II.4b skill name)
        assert char.skills["survival"].rank == "novice"
        assert char.skills["survival"].marks == 1


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

        assert "investigate" in restored.skills
        assert restored.skills["investigate"].rank == sample_character.skills["investigate"].rank
        assert restored.skills["investigate"].marks == sample_character.skills["investigate"].marks

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

    def test_master_rank_serializes_in_fof(self, ruleset, valid_attributes):
        """Master rank skills survive to_fof / from_fof round-trip."""
        char, _ = create_default_character(
            name="Master",
            player_name="Player3",
            primary_facet="body",
            attributes=valid_attributes,
            ruleset=ruleset,
        )
        char.advance_skill("athletics", 16, ruleset)  # novice → master (D16: 3+5+8)
        assert char.skills["athletics"].rank == "master"
        fof_dict = char.to_fof(MODULE_REFS, SESSION_ID)
        assert fof_dict["character"]["skills"]["athletics"]["rank"] == "master"
        restored = Character.from_fof(fof_dict)
        assert restored.skills["athletics"].rank == "master"


class TestOragaNightPregens:
    """The module's five pregenerated characters, shipped as `.fof` so there is
    one source of truth for them rather than a sheet and a paragraph that can
    disagree (DESIGN_oraga_rewrite §2, ruling 1).
    """

    PREGENS = ("serane", "pello", "andra", "dassa", "ilesse")

    @staticmethod
    def _ruleset():
        from pathlib import Path
        from app.facets.loader import load_facet_file
        from app.facets.registry import MergedRuleset
        root = Path(__file__).resolve().parents[1] / "facets"
        return MergedRuleset([
            load_facet_file(root / "base" / "facet.yaml"),
            load_facet_file(root / "valloh" / "facet.yaml"),
        ])

    @staticmethod
    def _dir():
        from pathlib import Path
        return (Path(__file__).resolve().parents[2]
                / "adventures" / "oraga_night" / "characters")

    def _load(self, slug):
        import yaml
        from app.game.character import Character
        data = yaml.safe_load((self._dir() / f"{slug}.fof").read_text(encoding="utf-8"))
        return Character.from_fof(data, self._ruleset()), data["character"]

    def test_all_five_load_and_validate(self):
        rs = self._ruleset()
        for slug in self.PREGENS:
            char, _ = self._load(slug)
            assert char.validate_against_ruleset(rs) == [], slug

    def test_two_of_the_five_have_a_real_endurance_pool(self):
        """The module used to ship five Endurance-3 characters, which meant
        nobody at the table could afford to react twice. Two at 4-5 is what
        makes the fights playable (BRIEF §6.5)."""
        rs = self._ruleset()
        pools = sorted(self._load(slug)[0].endurance_max(rs) for slug in self.PREGENS)
        assert sum(1 for p in pools if p >= 4) >= 2, pools

    def test_the_gifted_hold_their_lineage_domain(self):
        for slug in ("serane", "pello", "andra", "ilesse"):
            char, _ = self._load(slug)
            assert char.gifted is True, slug
            assert char.magic_domain is not None, slug
            assert char.domain_source == "lineage", slug

    def test_the_gifted_have_not_yet_formalized(self):
        """Facet level 0 at the start of the night: their gift is real and
        Minor-scope, and it arrives in full at their first Facet level."""
        for slug in ("serane", "pello", "andra", "ilesse"):
            char, _ = self._load(slug)
            assert char.magic_technique_active is False, slug
            assert char.techniques == [], slug

    def test_dassa_is_the_ungifted_case(self):
        """One Orthaen in five. She keeps her Background's secondary skill and
        holds no domain — the case the whole Lineage step exists to express."""
        char, _ = self._load("dassa")
        assert char.lineage == "orthaen"
        assert char.gifted is False
        assert char.magic_domain is None
        assert char.domain_source is None

    def test_every_sheet_names_the_technique_it_would_take(self):
        """So a first-night table sees the road ahead (BRIEF §8.2)."""
        rs = self._ruleset()
        for slug in self.PREGENS:
            _, block = self._load(slug)
            tech_id = block.get("technique_at_facet_level_1")
            assert tech_id, slug
            assert rs.get_technique(tech_id) is not None, (slug, tech_id)

    def test_carried_charges_are_real_items(self):
        """A pregen's inventory may hold free text, but an id that looks like a
        crystal charge had better be one."""
        rs = self._ruleset()
        item_ids = {i.id for i in rs.items}
        for slug in self.PREGENS:
            char, _ = self._load(slug)
            for entry in char.inventory:
                if entry in item_ids or "_" in entry:
                    assert entry in item_ids, (slug, entry)

    def test_the_party_covers_all_three_facets(self):
        facets = {self._load(slug)[0].primary_facet for slug in self.PREGENS}
        assert facets == {"body", "mind", "soul"}


class TestLineageRoundTrips:
    """L8 added `lineage`, `gifted` and `domain_source` to the model; the .fof
    round-trip has to carry them or a saved gifted character reloads as an
    ungifted human who happens to know a domain.
    """

    def _rs(self):
        from pathlib import Path
        from app.facets.loader import load_facet_file
        from app.facets.registry import MergedRuleset
        root = Path(__file__).resolve().parents[1] / "facets"
        return MergedRuleset([
            load_facet_file(root / "base" / "facet.yaml"),
            load_facet_file(root / "valloh" / "facet.yaml"),
        ])

    def test_a_gifted_character_survives_a_round_trip(self):
        from app.game.character import Character, create_default_character
        rs = self._rs()
        char, errors = create_default_character(
            name="Serane", player_name="Serane", primary_facet="soul",
            attributes=dict(strength=1, dexterity=2, constitution=1,
                            intelligence=3, wisdom=2, knowledge=2, spirit=2,
                            luck=2, charisma=3),
            ruleset=rs, lineage="orthaen", gifted=True, magic_domain="transmutation")
        assert errors == []
        back = Character.from_fof(
            char.to_fof([{"id": "base", "version": "0.1.0"}], "s"), rs)
        assert back.lineage == "orthaen"
        assert back.gifted is True
        assert back.domain_source == "lineage"
        assert back.magic_domain == "transmutation"
        # A Mind domain chosen as a gift keeps its intuitive tradition across a
        # save and load, or the reloaded character rolls the wrong attribute.
        assert back.magic_tradition == "intuitive"

    def test_an_ungifted_member_survives_a_round_trip(self):
        from app.game.character import Character, create_default_character
        rs = self._rs()
        char, errors = create_default_character(
            name="Dassa", player_name="Dassa", primary_facet="body",
            attributes=dict(strength=3, dexterity=2, constitution=3,
                            intelligence=1, wisdom=2, knowledge=2, spirit=1,
                            luck=2, charisma=2),
            ruleset=rs, lineage="orthaen", gifted=False,
            background_id="city_watch_veteran")
        assert errors == []
        back = Character.from_fof(
            char.to_fof([{"id": "base", "version": "0.1.0"}], "s"), rs)
        assert back.lineage == "orthaen"
        assert back.gifted is False
        assert back.magic_domain is None

    def test_a_human_sheet_does_not_grow_a_lineage_field(self):
        """Every .fof written before II.5 existed must round-trip unchanged —
        the default is not written out."""
        from app.game.character import create_default_character
        rs = self._rs()
        char, errors = create_default_character(
            name="Mordai", player_name="Mordai", primary_facet="body",
            attributes=dict(strength=3, dexterity=2, constitution=3,
                            intelligence=1, wisdom=1, knowledge=2, spirit=2,
                            luck=2, charisma=2),
            ruleset=rs)
        assert errors == []
        block = char.to_fof([{"id": "base", "version": "0.1.0"}], "s")["character"]
        assert "lineage" not in block
        assert "gifted" not in block
