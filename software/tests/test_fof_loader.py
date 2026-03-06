"""Tests for .fof file loading via load_facet_file() and discover_facet_files()."""
import sys
import os
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("FACETS_DIR", str(Path(__file__).parent.parent / "facets"))
os.environ.setdefault("DATA_DIR", str(Path(__file__).parent / "_test_data"))
os.environ.setdefault("SECRET_KEY", "test-secret-key-do-not-use-in-production")

from app.facets.loader import load_facet_file, discover_facet_files, FacetLoadError
from app.facets.registry import build_ruleset, MergedRuleset

SPEC_EXAMPLES = Path(__file__).parent.parent.parent / "spec" / "examples"
BASE_FOF = SPEC_EXAMPLES / "base-ruleset.fof"
BASE_YAML = Path(__file__).parent.parent / "facets" / "base" / "facet.yaml"


class TestLoadFofFile:
    def test_load_base_ruleset_fof_succeeds(self):
        ff = load_facet_file(BASE_FOF)
        assert ff.id == "base"
        assert ff.version == "0.1.0"

    def test_fof_produces_correct_attribute_count(self):
        ff = load_facet_file(BASE_FOF)
        assert len(ff.attributes.major) == 3
        assert len(ff.attributes.minor) == 9

    def test_fof_has_attribute_distribution(self):
        ff = load_facet_file(BASE_FOF)
        assert ff.attributes.distribution is not None
        assert ff.attributes.distribution.total_points == 18

    def test_fof_facets_parsed(self):
        ff = load_facet_file(BASE_FOF)
        facet_ids = {cf.id for cf in ff.facets}
        assert facet_ids == {"body", "mind", "soul"}

    def test_fof_skills_count_matches_yaml(self):
        """The .fof and facet.yaml must define the same number of skills."""
        ff_fof = load_facet_file(BASE_FOF)
        ff_yaml = load_facet_file(BASE_YAML)
        assert len(ff_fof.skills) == len(ff_yaml.skills)

    def test_fof_skill_ids_match_yaml(self):
        ff_fof = load_facet_file(BASE_FOF)
        ff_yaml = load_facet_file(BASE_YAML)
        assert {sk.id for sk in ff_fof.skills} == {sk.id for sk in ff_yaml.skills}

    def test_fof_advancement_matches_yaml(self):
        ff_fof = load_facet_file(BASE_FOF)
        ff_yaml = load_facet_file(BASE_YAML)
        assert ff_fof.advancement is not None
        assert ff_yaml.advancement is not None
        assert ff_fof.advancement.session_skill_points == ff_yaml.advancement.session_skill_points
        assert ff_fof.advancement.marks_per_rank == ff_yaml.advancement.marks_per_rank
        assert ff_fof.advancement.facet_level_threshold == ff_yaml.advancement.facet_level_threshold

    def test_fof_spark_matches_yaml(self):
        ff_fof = load_facet_file(BASE_FOF)
        ff_yaml = load_facet_file(BASE_YAML)
        assert ff_fof.spark is not None
        assert ff_yaml.spark is not None
        assert ff_fof.spark.base_sparks_per_session == ff_yaml.spark.base_sparks_per_session

    def test_fof_merged_ruleset_equivalent_to_yaml(self):
        """A MergedRuleset from .fof should be functionally equivalent to one from facet.yaml."""
        from app.facets.registry import MergedRuleset
        ff_fof = load_facet_file(BASE_FOF)
        ff_yaml = load_facet_file(BASE_YAML)
        ruleset_fof = MergedRuleset([ff_fof])
        ruleset_yaml = MergedRuleset([ff_yaml])

        assert len(ruleset_fof.minor_attributes) == len(ruleset_yaml.minor_attributes)
        assert len(ruleset_fof.skills) == len(ruleset_yaml.skills)
        assert len(ruleset_fof.character_facets) == len(ruleset_yaml.character_facets)
        assert ruleset_fof.advancement.marks_per_rank == ruleset_yaml.advancement.marks_per_rank


class TestDiscoverFofFiles:
    def test_discover_finds_facet_yaml_by_default(self):
        facets_dir = Path(__file__).parent.parent / "facets"
        paths = discover_facet_files(facets_dir)
        assert any(p.name == "facet.yaml" for p in paths)

    def test_discover_returns_empty_for_nonexistent_dir(self):
        paths = discover_facet_files(Path("/nonexistent/dir"))
        assert paths == []

    def test_fof_supersedes_yaml_in_same_dir(self, tmp_path):
        """A .fof ruleset file in the same dir as facet.yaml wins."""
        import shutil
        # Copy base facet.yaml and base-ruleset.fof into the same tmp dir
        fof_dest = tmp_path / "base-ruleset.fof"
        yaml_dest = tmp_path / "facet.yaml"
        shutil.copy(BASE_FOF, fof_dest)
        shutil.copy(BASE_YAML, yaml_dest)

        paths = discover_facet_files(tmp_path)
        names = [p.name for p in paths]
        assert "base-ruleset.fof" in names
        assert "facet.yaml" not in names

    def test_fof_without_type_key_is_included(self, tmp_path):
        """A .fof file with no 'type' key is treated as a ruleset (backward compat)."""
        import yaml as _yaml
        import shutil
        raw = _yaml.safe_load(BASE_FOF.read_text(encoding="utf-8"))
        raw.pop("type", None)
        fof_path = tmp_path / "no-type.fof"
        fof_path.write_text(_yaml.dump(raw), encoding="utf-8")

        paths = discover_facet_files(tmp_path)
        assert fof_path in paths

    def test_character_fof_not_discovered_as_ruleset(self, tmp_path):
        """A .fof file with type: character should NOT be returned by discover."""
        import shutil
        char_fof = SPEC_EXAMPLES / "character-example.fof"
        dest = tmp_path / "character-example.fof"
        shutil.copy(char_fof, dest)

        paths = discover_facet_files(tmp_path)
        assert dest not in paths
