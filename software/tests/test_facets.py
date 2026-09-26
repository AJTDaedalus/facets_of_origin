"""Schema, loader and registry for the Lean Facets v1.0 ruleset (T1)."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from app.facets.loader import (
    FacetLoadError, discover_facet_files, load_facet_file, load_tables_file,
)
from app.facets.registry import REQUIRED_TABLE_IDS, MergedRuleset, build_ruleset
from app.facets.schema import (
    FacetFile, TableDef, TalentDef, die_faces, expand_roll, table_coverage_errors,
)

FACETS = Path(__file__).parent.parent / "facets"
BASE = FACETS / "base" / "facet.yaml"
VALLOH = FACETS / "valloh" / "facet.yaml"


@pytest.fixture(scope="module")
def base_raw() -> dict:
    return yaml.safe_load(BASE.read_text(encoding="utf-8"))


def _write(tmp_path: Path, data: dict, name: str = "facet.yaml") -> Path:
    path = tmp_path / name
    path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def _merged(*raws: dict) -> MergedRuleset:
    files = []
    for raw in raws:
        ff = FacetFile.model_validate(raw)
        files.append(ff)
    return MergedRuleset(files)


def _table(tid="t", die="1d6", entries=None):
    return TableDef(id=tid, name=tid, die=die, entries=entries or [
        {"roll": "1-3", "text": "low"}, {"roll": "4-6", "text": "high"}])


# ---------------------------------------------------------------------------
# Dice faces and table coverage
# ---------------------------------------------------------------------------

class TestDieFaces:
    def test_d66_has_36_faces_in_tens_units(self):
        faces = die_faces("d66")
        assert len(faces) == 36 and faces[0] == 11 and faces[-1] == 66 and 17 not in faces

    def test_2d6_runs_two_to_twelve(self):
        assert die_faces("2d6") == list(range(2, 13))

    def test_unknown_die_raises(self):
        with pytest.raises(ValueError):
            die_faces("3d4")


class TestExpandRoll:
    def test_single_value(self):
        assert expand_roll("7", "2d6") == [7]

    def test_en_dash_range(self):
        assert expand_roll("2–4", "2d6") == [2, 3, 4]

    def test_d66_range_skips_impossible_faces(self):
        assert expand_roll("15-22", "d66") == [15, 16, 21, 22]

    def test_out_of_range_value_covers_nothing(self):
        assert expand_roll(13, "2d6") == []

    def test_backwards_range_raises(self):
        with pytest.raises(ValueError):
            expand_roll("6-1", "1d6")


class TestTableCoverage:
    def test_exact_cover_has_no_errors(self):
        assert table_coverage_errors(_table()) == []

    def test_gap_is_reported(self):
        t = _table(entries=[{"roll": "1-3", "text": "a"}, {"roll": "5-6", "text": "b"}])
        assert any("no entry for [4]" in e for e in table_coverage_errors(t))

    def test_overlap_is_reported(self):
        t = _table(entries=[{"roll": "1-4", "text": "a"}, {"roll": "4-6", "text": "b"}])
        assert any("more than one entry" in e for e in table_coverage_errors(t))

    def test_blank_text_is_reported(self):
        t = _table(entries=[{"roll": "1-3", "text": " "}, {"roll": "4-6", "text": "b"}])
        assert any("no text" in e for e in table_coverage_errors(t))

    def test_lookup_finds_the_entry(self):
        assert _table().lookup(5).text == "high"

    def test_lookup_missing_face_raises(self):
        t = TableDef(id="t", name="t", die="1d6", entries=[{"roll": "1", "text": "x"}])
        with pytest.raises(ValueError):
            t.lookup(4)

    def test_unknown_die_is_rejected_by_the_schema(self):
        with pytest.raises(Exception):
            TableDef(id="t", name="t", die="1d7", entries=[])


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestTalentDef:
    def _t(self, **kw):
        base = dict(id="x", name="X", facet="body", kind="talent", use="passive",
                    text="t", normal="n", improved="i")
        base.update(kw)
        return TalentDef(**base)

    def test_menu_talent_needs_improved_form(self):
        with pytest.raises(Exception):
            self._t(improved=None)

    def test_signature_needs_no_improved_form(self):
        assert self._t(kind="signature", improved=None).kind == "signature"

    def test_shared_talent_is_on_both_menus(self):
        t = self._t(facet="mind", shared_with=["soul"])
        assert t.on_menu_of("mind") and t.on_menu_of("soul") and not t.on_menu_of("body")

    def test_uses_allowed_passive_is_untracked(self):
        assert self._t().uses_allowed() is None

    def test_uses_allowed_twice_when_improved_says_twice(self):
        t = self._t(use="once_per_scene", improved="Twice per scene.")
        assert t.uses_allowed() == 1 and t.uses_allowed(improved=True) == 2

    def test_effect_prefers_improved_effects(self):
        t = self._t(effects={"unarmored_armor": 1}, improved_effects={"unarmored_armor": 2})
        assert t.effect("unarmored_armor") == 1
        assert t.effect("unarmored_armor", improved=True) == 2
        assert t.effect("missing", default=0) == 0


class TestFacetFileSchema:
    def test_base_validates(self, base_raw):
        ff = FacetFile.model_validate(base_raw)
        assert ff.is_core and ff.version == "1.0.0"

    def test_unknown_top_level_key_is_rejected(self, base_raw):
        bad = dict(base_raw, skills=[])
        with pytest.raises(Exception):
            FacetFile.model_validate(bad)

    def test_setting_facet_is_not_core_and_writes_no_core_section(self):
        ff = FacetFile.model_validate(yaml.safe_load(VALLOH.read_text()))
        assert not ff.is_core
        assert ff.written_core_sections() == []

    def test_equipment_other_than_items_counts_as_a_core_write(self):
        ff = FacetFile.model_validate({"id": "s", "name": "S", "version": "1",
                                       "equipment": {"weapon_kinds": ["x"], "items": []}})
        assert ff.written_core_sections() == ["equipment.weapon_kinds"]


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

class TestLoadFacetFile:
    def test_loads_base_with_its_tables(self):
        ff = load_facet_file(BASE)
        assert len(ff.loaded_tables) >= len(REQUIRED_TABLE_IDS)

    def test_missing_tables_file_is_a_warning_not_an_error(self, tmp_path, base_raw):
        path = _write(tmp_path, dict(base_raw, tables_file="nope.yaml"))
        ff = load_facet_file(path)
        assert ff.loaded_tables == [] and "not found" in ff.load_warnings[0]

    def test_bad_yaml_raises(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("a: [unclosed")
        with pytest.raises(FacetLoadError):
            load_facet_file(path)

    def test_non_mapping_raises(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("- a\n- b\n")
        with pytest.raises(FacetLoadError, match="mapping"):
            load_facet_file(path)

    def test_schema_failure_names_the_field(self, tmp_path, base_raw):
        bad = copy.deepcopy(base_raw)
        del bad["talents"][0]["normal"]
        with pytest.raises(FacetLoadError, match="normal"):
            load_facet_file(_write(tmp_path, bad))

    def test_inline_table_with_a_gap_raises(self, tmp_path):
        data = {"id": "s", "name": "S", "version": "1", "tables": [
            {"id": "t", "name": "T", "die": "1d6", "entries": [{"roll": "1-5", "text": "x"}]}]}
        with pytest.raises(FacetLoadError, match="no entry"):
            load_facet_file(_write(tmp_path, data))

    def test_fof_envelope_keys_are_stripped(self, tmp_path, base_raw):
        data = dict(base_raw, fof_version="1.0", type="ruleset", tables_file=None)
        ff = load_facet_file(_write(tmp_path, data, "rules.fof"))
        assert ff.id == "base"


class TestLoadTablesFile:
    def test_real_tables_file_validates(self):
        tf = load_tables_file(FACETS / "base" / "tables.yaml")
        assert {t.id for t in tf.tables} >= set(REQUIRED_TABLE_IDS)

    def test_empty_file_is_empty(self, tmp_path):
        p = tmp_path / "tables.yaml"
        p.write_text("")
        assert load_tables_file(p).tables == []

    def test_duplicate_ids_raise(self, tmp_path):
        entry = {"id": "t", "name": "T", "die": "1d6",
                 "entries": [{"roll": "1-6", "text": "x"}]}
        p = _write(tmp_path, {"tables": [entry, entry]}, "tables.yaml")
        with pytest.raises(FacetLoadError, match="duplicate"):
            load_tables_file(p)

    def test_coverage_error_raises(self, tmp_path):
        p = _write(tmp_path, {"tables": [{"id": "t", "name": "T", "die": "2d6",
                                         "entries": [{"roll": "2-11", "text": "x"}]}]},
                   "tables.yaml")
        with pytest.raises(FacetLoadError, match="12"):
            load_tables_file(p)


class TestDiscover:
    def test_finds_base_and_valloh(self):
        names = {p.parent.name for p in discover_facet_files(FACETS)}
        assert {"base", "valloh"} <= names

    def test_missing_dir_is_empty(self, tmp_path):
        assert discover_facet_files(tmp_path / "none") == []

    def test_character_fof_is_not_a_ruleset(self, tmp_path):
        (tmp_path / "c.fof").write_text("type: character\n")
        assert discover_facet_files(tmp_path) == []


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class TestMergedRuleset:
    def test_counts_match_the_data(self, ruleset, base_raw):
        assert len(ruleset.talents) == len(base_raw["talents"])
        assert len(ruleset.classes) == 12
        assert len(ruleset.magic_domains) == len(base_raw["magic_domains"])

    def test_outcome_tiers_have_id_and_threshold(self, ruleset):
        tiers = {t.id: t.threshold for t in ruleset.roll_resolution.outcome_tiers}
        assert tiers == {"full_success": 10, "partial_success": 7, "failure": None}

    def test_client_dict_carries_combat_and_advancement(self, ruleset):
        d = ruleset.to_client_dict()
        assert d["combat"]["armor"]["cap"] == 3
        assert d["advancement"]["max_level"] == 10
        assert "reaction" in d["tables"]

    def test_no_required_table_is_missing(self, ruleset):
        assert ruleset.missing_required_tables() == []

    def test_two_cores_are_rejected(self, base_raw):
        other = dict(copy.deepcopy(base_raw), id="other")
        with pytest.raises(FacetLoadError, match="Exactly one core"):
            _merged(base_raw, other)

    def test_no_core_is_rejected(self):
        with pytest.raises(FacetLoadError):
            _merged({"id": "s", "name": "S", "version": "1"})

    def test_core_missing_a_section_is_rejected(self, base_raw):
        bad = {k: v for k, v in base_raw.items() if k != "combat"}
        with pytest.raises(FacetLoadError, match="combat"):
            _merged(bad)


class TestCrossReferences:
    def _broken(self, base_raw, mutate):
        raw = copy.deepcopy(base_raw)
        mutate(raw)
        with pytest.raises(FacetLoadError, match="Cross-reference") as exc:
            _merged(raw)
        return str(exc.value)

    def test_class_talent_must_exist(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["classes"][0]["talents"].__setitem__(0, "nope"))
        assert "unknown talent 'nope'" in msg

    def test_class_talent_must_be_on_its_menu(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["classes"][0]["talents"].__setitem__(0, "loremaster"))
        assert "not a talent on the body menu" in msg

    def test_class_signature_must_be_a_signature(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["classes"][0].__setitem__("signature", "tough"))
        assert "not a body signature" in msg

    def test_kit_item_must_exist(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["classes"][0]["kit"].append("laser"))
        assert "laser" in msg

    def test_requires_must_resolve(self, base_raw):
        def mutate(r):
            t = next(t for t in r["talents"] if t["id"] == "wider_domain")
            t["requires"] = {"any_talent": ["ghostcraft"]}
        assert "ghostcraft" in self._broken(base_raw, mutate)

    def test_shared_with_must_be_a_facet(self, base_raw):
        def mutate(r):
            next(t for t in r["talents"] if t["id"] == "wider_domain")["shared_with"] = ["heart"]
        assert "heart" in self._broken(base_raw, mutate)

    def test_domain_tradition_must_exist(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["magic_domains"][0].__setitem__("tradition", "x"))
        assert "unknown tradition" in msg

    def test_level_table_must_cover_every_level(self, base_raw):
        msg = self._broken(base_raw, lambda r: r["monsters"]["level_table"].pop())
        assert "level_table" in msg


class TestSettingFacets:
    def test_valloh_adds_lineages_and_curios(self, valloh_ruleset, ruleset):
        assert len(valloh_ruleset.lineages) == len(ruleset.lineages) + 10
        assert sum(1 for i in valloh_ruleset.items if i.curio) == 6

    def test_valloh_changes_no_core_number(self, valloh_ruleset, ruleset):
        a, b = ruleset.to_client_dict(), valloh_ruleset.to_client_dict()
        for section in ("combat", "advancement", "magic", "monsters", "roll_resolution", "hp"):
            assert a[section] == b[section]

    def test_valloh_gifts_are_minor_and_player_chosen(self, valloh_ruleset):
        orthaen = valloh_ruleset.get_lineage("orthaen")
        assert orthaen.gifted and orthaen.gift_domain_scope == "minor"
        assert orthaen.gift_knack == "Orthaen gift" and orthaen.gift_domains == []

    def test_setting_facet_writing_a_core_rule_is_rejected(self, base_raw):
        setting = {"id": "evil", "name": "E", "version": "1", "priority": 1,
                   "combat": base_raw["combat"]}
        with pytest.raises(FacetLoadError, match="combat"):
            _merged(base_raw, setting)

    def test_setting_facet_redefining_a_core_id_is_rejected(self, base_raw):
        setting = {"id": "evil", "name": "E", "version": "1", "priority": 1,
                   "lineages": [{"id": "human", "name": "Human"}]}
        with pytest.raises(FacetLoadError, match="redefines lineage 'human'"):
            _merged(base_raw, setting)

    def test_setting_facet_may_add_a_talent_and_class(self, base_raw):
        setting = {"id": "s", "name": "S", "version": "1", "priority": 1,
                   "talents": [{"id": "sea_legs", "name": "Sea Legs", "facet": "body",
                                "kind": "talent", "use": "passive", "text": "t",
                                "normal": "n", "improved": "i"}],
                   "items": [{"id": "harpoon", "name": "Harpoon", "weapon": "standard"}]}
        rs = _merged(base_raw, setting)
        assert rs.get_talent("sea_legs") and rs.get_item("harpoon").weapon == "standard"


class TestLookups:
    def test_get_helpers(self, ruleset):
        assert ruleset.get_stat("body").name == "Body"
        assert ruleset.get_facet("mind").grit_die == 6
        assert ruleset.get_class("warrior").signature == "unstoppable"
        assert ruleset.get_background("dockworker").knack == "Dockworker"
        assert ruleset.get_item("longbow").weapon == "ranged"
        assert ruleset.get_domain("fire").tradition == "invocation"
        assert ruleset.get_table("reaction").die == "2d6"

    def test_get_helpers_return_none_for_unknown(self, ruleset):
        for fn in (ruleset.get_stat, ruleset.get_facet, ruleset.get_talent, ruleset.get_class,
                   ruleset.get_background, ruleset.get_lineage, ruleset.get_item,
                   ruleset.get_domain, ruleset.get_table):
            assert fn("nope") is None

    def test_talent_menu_includes_shared_talents(self, ruleset):
        soul = {t.id for t in ruleset.talent_menu("soul")}
        assert "wider_domain" in soul and "invocation" in soul and "thaumaturgy" not in soul
        sigs = {t.id for t in ruleset.talent_menu("body", "signature")}
        assert sigs == {"unstoppable", "whirlwind", "bulwark", "deadeye", "ghost", "second_wind"}

    def test_classes_for_facet(self, ruleset):
        assert {c.id for c in ruleset.classes_for_facet("soul")} == {
            "invoker", "speaker", "wanderer", "captain"}

    def test_domains_for_tradition(self, ruleset):
        prismatic = ruleset.domains_for_tradition("thaumaturgy", prismatic=True)
        assert {d.id for d in prismatic} == {"the_arcane", "the_constructed_mind", "chronomancy"}
        assert ruleset.domains_for_tradition("none") == []

    def test_shift_difficulty_clamps(self, ruleset):
        assert ruleset.shift_difficulty("Standard", 1) == "Easy"
        assert ruleset.shift_difficulty("Easy", 3) == "Easy"
        assert ruleset.shift_difficulty("Hard", -5) == "Very Hard"
        with pytest.raises(ValueError):
            ruleset.shift_difficulty("Trivial", 1)

    def test_harder_of(self, ruleset):
        assert ruleset.harder_of("Easy", "Hard") == "Hard"
        assert ruleset.harder_of("Very Hard", "Standard") == "Very Hard"

    def test_difficulty_modifier(self, ruleset):
        assert ruleset.difficulty_modifier("Very Hard") == -2
        with pytest.raises(ValueError):
            ruleset.difficulty_modifier("Impossible")

    def test_damage_bonus_steps(self, ruleset):
        adv = ruleset.advancement
        assert [adv.damage_bonus_at(n) for n in (1, 2, 3, 5, 6, 9, 10)] == [0, 0, 1, 1, 2, 3, 3]

    def test_monster_row(self, ruleset):
        assert ruleset.monsters.row(3).hp == 14
        with pytest.raises(ValueError):
            ruleset.monsters.row(11)


class TestBuildRuleset:
    def test_base_only(self):
        assert [f.id for f in build_ruleset([])._files] == ["base"]

    def test_with_valloh(self):
        assert [f.id for f in build_ruleset(["valloh"])._files] == ["base", "valloh"]

    def test_unknown_module_raises(self):
        with pytest.raises(FacetLoadError, match="Unknown Facet module"):
            build_ruleset(["atlantis"])

    def test_module_refs(self):
        assert build_ruleset(["valloh"]).module_refs() == [
            {"id": "base", "version": "1.0.0"}, {"id": "valloh", "version": "1.0.0"}]
