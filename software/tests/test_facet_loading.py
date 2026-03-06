"""Tests for Facet YAML loading, schema validation, and cross-reference checks."""
import textwrap
from pathlib import Path

import pytest
import yaml

from app.facets.loader import FacetLoadError, load_facet_file
from app.facets.registry import MergedRuleset, build_ruleset
from app.facets.schema import FacetFile


# ---------------------------------------------------------------------------
# Base ruleset loading
# ---------------------------------------------------------------------------

class TestBaseRulesetLoading:
    def test_base_loads_without_error(self, ruleset):
        assert ruleset is not None

    def test_minor_attributes_count(self, ruleset):
        assert len(ruleset.minor_attributes) == 9

    def test_all_nine_minor_attributes_present(self, ruleset):
        ids = {a.id for a in ruleset.minor_attributes}
        expected = {"strength", "dexterity", "constitution",
                    "intelligence", "wisdom", "knowledge",
                    "spirit", "luck", "charisma"}
        assert ids == expected

    def test_three_major_attributes(self, ruleset):
        assert len(ruleset.major_attributes) == 3
        ids = {a.id for a in ruleset.major_attributes}
        assert ids == {"body", "mind", "soul"}

    def test_three_character_facets(self, ruleset):
        assert len(ruleset.character_facets) == 3
        ids = {cf.id for cf in ruleset.character_facets}
        assert ids == {"body", "mind", "soul"}

    def test_skills_loaded(self, ruleset):
        assert len(ruleset.skills) > 0

    def test_five_body_skills_active(self, ruleset):
        body_skills = [s for s in ruleset.skills if s.facet == "body" and s.status == "active"]
        assert len(body_skills) == 5
        skill_ids = {s.id for s in body_skills}
        assert skill_ids == {"athletics", "combat", "stealth", "finesse", "endurance"}

    def test_roll_resolution_loaded(self, ruleset):
        assert ruleset.roll_resolution is not None
        assert ruleset.roll_resolution.thresholds["full_success"] == 10
        assert ruleset.roll_resolution.thresholds["partial_success"] == 7

    def test_spark_loaded(self, ruleset):
        assert ruleset.spark is not None
        assert ruleset.spark.base_sparks_per_session == 3
        assert len(ruleset.spark.earn_methods) == 3

    def test_advancement_loaded(self, ruleset):
        adv = ruleset.advancement
        assert adv is not None
        assert adv.session_skill_points == 4
        assert adv.marks_per_rank == 3
        assert adv.facet_level_threshold == 6

    def test_attribute_ratings_three_tiers(self, ruleset):
        assert len(ruleset.attribute_ratings) == 3
        mods = {r.rating: r.modifier for r in ruleset.attribute_ratings}
        assert mods == {1: -1, 2: 0, 3: 1}

    def test_attribute_distribution_correct(self, ruleset):
        dist = ruleset.attribute_distribution
        assert dist is not None
        assert dist.total_points == 18
        assert dist.min_per_attribute == 1
        assert dist.max_per_attribute == 3

    def test_body_techniques_loaded(self, ruleset):
        assert "body" in ruleset.techniques
        body_tree = ruleset.techniques["body"]
        branch_ids = {b.id for b in body_tree.branches}
        assert branch_ids == {"might", "grace", "iron"}

    def test_each_branch_has_three_tiers(self, ruleset):
        body_tree = ruleset.techniques["body"]
        for branch in body_tree.branches:
            tier_nums = {t.tier for t in branch.tiers}
            assert tier_nums == {1, 2, 3}, f"Branch {branch.id} missing tiers: {tier_nums}"

    def test_difficulty_modifiers_four_levels(self, ruleset):
        mods = {d.label: d.modifier for d in ruleset.roll_resolution.difficulty_modifiers}
        assert mods["Easy"] == 1
        assert mods["Standard"] == 0
        assert mods["Hard"] == -1
        assert mods["Very Hard"] == -2

    def test_skill_point_costs_all_contexts(self, ruleset):
        costs = {c.context: c.cost for c in ruleset.advancement.skill_point_costs}
        assert costs["primary_facet_success"] == 1
        assert costs["primary_facet_failure"] == 2
        assert costs["secondary_facet_success"] == 2
        assert costs["secondary_facet_failure"] == 4


# ---------------------------------------------------------------------------
# Schema validation — malformed Facet files
# ---------------------------------------------------------------------------

class TestFacetSchemaValidation:
    def _write_yaml(self, tmp_path, content: str) -> Path:
        p = tmp_path / "facet.yaml"
        p.write_text(textwrap.dedent(content))
        return p

    def test_missing_required_id_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            name: "Test"
            version: "1.0"
        """)
        with pytest.raises(FacetLoadError, match="id"):
            load_facet_file(path)

    def test_invalid_id_slug_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "invalid id with spaces"
            name: "Test"
            version: "1.0"
        """)
        with pytest.raises(FacetLoadError):
            load_facet_file(path)

    def test_yaml_parse_error_raises(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(": this is not valid yaml: {{{")
        with pytest.raises(FacetLoadError, match="YAML parse error"):
            load_facet_file(path)

    def test_not_a_mapping_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, "- item1\n- item2\n")
        with pytest.raises(FacetLoadError, match="mapping"):
            load_facet_file(path)

    def test_attribute_rating_out_of_range_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "test"
            name: "Test"
            version: "1.0"
            attributes:
              ratings:
                - rating: 0
                  label: Zero
                  modifier: -99
        """)
        with pytest.raises(FacetLoadError):
            load_facet_file(path)

    def test_nonexistent_file_raises(self, tmp_path):
        with pytest.raises(FacetLoadError, match="Cannot read file"):
            load_facet_file(tmp_path / "doesnotexist.yaml")

    def test_valid_minimal_facet_loads(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "minimal"
            name: "Minimal Facet"
            version: "0.0.1"
        """)
        ff = load_facet_file(path)
        assert ff.id == "minimal"
        assert ff.name == "Minimal Facet"


# ---------------------------------------------------------------------------
# Cross-reference validation
# ---------------------------------------------------------------------------

class TestCrossReferenceValidation:
    def test_skill_referencing_unknown_attribute_fails(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "bad-skill"
            name: "Bad Skill Facet"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: "Body"
                description: "test"
                major_attribute: body
            skills:
              - id: bad_skill
                name: "Bad Skill"
                facet: body
                attribute: nonexistent_attribute
                description: "test"
        """))
        from app.facets.loader import load_facet_file as lff
        ff = lff(path)
        with pytest.raises(FacetLoadError, match="unknown attribute"):
            MergedRuleset([ff])

    def test_skill_referencing_unknown_facet_fails(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "bad-facet-ref"
            name: "Test"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: "Body"
                description: "test"
                major_attribute: body
            skills:
              - id: bad_skill
                name: "Bad"
                facet: nonexistent_facet
                attribute: strength
                description: "test"
        """))
        from app.facets.loader import load_facet_file as lff
        ff = lff(path)
        with pytest.raises(FacetLoadError, match="unknown facet"):
            MergedRuleset([ff])


# ---------------------------------------------------------------------------
# Facet composition / override
# ---------------------------------------------------------------------------

class TestFacetComposition:
    def test_later_facet_overrides_skill(self, tmp_path):
        """A second Facet file with the same skill ID wins."""
        from app.facets.loader import load_facet_file as lff

        base_path = tmp_path / "base.yaml"
        base_path.write_text(textwrap.dedent("""
            id: "base-mini"
            name: "Base"
            version: "1.0"
            priority: 0
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: "test"
                major_attribute: body
            skills:
              - id: athletics
                name: Athletics
                facet: body
                attribute: strength
                description: "Original description"
        """))

        override_path = tmp_path / "override.yaml"
        override_path.write_text(textwrap.dedent("""
            id: "override"
            name: "Override"
            version: "1.0"
            priority: 10
            skills:
              - id: athletics
                name: Athletics
                facet: body
                attribute: strength
                description: "Overridden description"
        """))

        base_ff = lff(base_path)
        override_ff = lff(override_path)
        merged = MergedRuleset([base_ff, override_ff])
        skill = merged.get_skill("athletics")
        assert skill is not None
        assert skill.description == "Overridden description"


# ---------------------------------------------------------------------------
# discover_facet_files edge cases
# ---------------------------------------------------------------------------

class TestDiscoverFacetFiles:
    def test_empty_directory_returns_empty_list(self, tmp_path):
        from app.facets.loader import discover_facet_files
        result = discover_facet_files(tmp_path)
        assert result == []

    def test_nonexistent_directory_returns_empty_list(self, tmp_path):
        from app.facets.loader import discover_facet_files
        result = discover_facet_files(tmp_path / "does_not_exist")
        assert result == []

    def test_directory_with_non_yaml_files_returns_empty(self, tmp_path):
        from app.facets.loader import discover_facet_files
        (tmp_path / "readme.txt").write_text("not a facet")
        (tmp_path / "data.json").write_text("{}")
        result = discover_facet_files(tmp_path)
        assert result == []

    def test_discovers_yaml_in_subdirectory(self, tmp_path):
        from app.facets.loader import discover_facet_files
        sub = tmp_path / "mymod"
        sub.mkdir()
        (sub / "facet.yaml").write_text("id: mymod\nname: My Mod\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        assert len(result) == 1

    def test_discovers_multiple_facets(self, tmp_path):
        from app.facets.loader import discover_facet_files
        for name in ("mod_a", "mod_b", "mod_c"):
            d = tmp_path / name
            d.mkdir()
            (d / "facet.yaml").write_text(f"id: '{name}'\nname: '{name}'\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        assert len(result) == 3

    def test_returns_sorted_paths(self, tmp_path):
        from app.facets.loader import discover_facet_files
        for name in ("c_mod", "a_mod", "b_mod"):
            d = tmp_path / name
            d.mkdir()
            (d / "facet.yaml").write_text(f"id: '{name}'\nname: '{name}'\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        names = [p.parent.name for p in result]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# load_facet_file additional edge cases
# ---------------------------------------------------------------------------

class TestLoadFacetFileEdgeCases:
    def test_facet_with_all_optional_sections_absent(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("id: bare\nname: Bare\nversion: '1.0'\n")
        ff = load_facet_file(path)
        assert ff.facets == []
        assert ff.skills == []
        assert ff.roll_resolution is None
        assert ff.spark is None
        assert ff.advancement is None

    def test_facet_with_valid_technique_prerequisites(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "tech-test"
            name: "Tech Test"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: test
                  major: body
              major:
                - id: body
                  name: Body
                  description: test
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: test
                major_attribute: body
            techniques:
              body:
                branches:
                  - id: might
                    name: Might
                    attribute: strength
                    tiers:
                      - tier: 1
                        techniques:
                          - id: tier1
                            name: Tier 1
                            description: First tier.
                            prerequisites: []
                      - tier: 2
                        techniques:
                          - id: tier2
                            name: Tier 2
                            description: Requires tier1.
                            prerequisites: [tier1]
                      - tier: 3
                        techniques:
                          - id: tier3
                            name: Tier 3
                            description: Requires tier2.
                            prerequisites: [tier2]
        """))
        ff = load_facet_file(path)
        body_tree = ff.techniques.get("body")
        assert body_tree is not None
        tier2 = body_tree.branches[0].tiers[1].techniques[0]
        assert "tier1" in tier2.prerequisites

    def test_facet_priority_zero_accepted(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("id: base\nname: Base\nversion: '1.0'\npriority: 0\n")
        ff = load_facet_file(path)
        assert ff.priority == 0

    def test_facet_with_authors_list(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "authored"
            name: "Authored Facet"
            version: "1.0"
            authors:
              - Alice
              - Bob
        """))
        ff = load_facet_file(path)
        assert len(ff.authors) == 2
        assert "Alice" in ff.authors


# ---------------------------------------------------------------------------
# Override priority ordering
# ---------------------------------------------------------------------------

class TestFacetOverridePriority:
    def _make_facet_yaml(self, tmp_path, id_, priority, skill_desc):
        d = tmp_path / id_
        d.mkdir()
        (d / "facet.yaml").write_text(textwrap.dedent(f"""
            id: "{id_}"
            name: "{id_}"
            version: "1.0"
            priority: {priority}
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: test
                  major: body
              major:
                - id: body
                  name: Body
                  description: test
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: test
                major_attribute: body
            skills:
              - id: common_skill
                name: Common
                facet: body
                attribute: strength
                description: "{skill_desc}"
        """))
        return d / "facet.yaml"

    def test_higher_priority_wins(self, tmp_path):
        from app.facets.loader import load_facet_file as lff
        path_low = self._make_facet_yaml(tmp_path, "low", 0, "Low priority description")
        path_high = self._make_facet_yaml(tmp_path, "high", 20, "High priority description")
        merged = MergedRuleset([lff(path_low), lff(path_high)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "High priority description"

    def test_equal_priority_last_in_list_wins(self, tmp_path):
        from app.facets.loader import load_facet_file as lff
        path_a = self._make_facet_yaml(tmp_path, "aaa", 10, "AAA description")
        path_b = self._make_facet_yaml(tmp_path, "bbb", 10, "BBB description")
        # bbb appears second in the list
        merged = MergedRuleset([lff(path_a), lff(path_b)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "BBB description"

    def test_base_priority_zero_is_lowest(self, tmp_path):
        """Priority 0 (base) must yield to any module with higher priority."""
        from app.facets.loader import load_facet_file as lff
        path_base = self._make_facet_yaml(tmp_path, "base_mod", 0, "Base description")
        path_mod = self._make_facet_yaml(tmp_path, "expansion", 5, "Expansion description")
        merged = MergedRuleset([lff(path_base), lff(path_mod)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "Expansion description"
