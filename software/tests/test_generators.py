"""Tests for the generated-block tools: build_bestiary, build_scene_cards,
build_toolbox and build_table_register. Write tests use tmp_path copies only."""
import shutil
from pathlib import Path

import pytest
import yaml

from app.facets.schema import TableDef
from tests.conftest import make_enemy
from tools import build_bestiary as bb
from tools import build_scene_cards as sc
from tools import build_table_register as tr
from tools import build_toolbox as tbx

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def core():
    return bb.load_ruleset()


# ---------------------------------------------------------------------------
# build_bestiary
# ---------------------------------------------------------------------------

class TestRenderBlock:
    def test_standard_block_has_every_card_field(self, core):
        e = make_enemy(level=3, role="standard", armor=1, morale=8, nastier="n", weapon="Cudgel")
        block = bb.render_block(e, core)
        assert block.startswith("**standard 3** · *Level 3 Standard* · Cudgel")
        assert "**HP** 14" in block and "**Attack** +2" in block and "**Damage** 6" in block
        assert "**Armor** 1" in block and "**Morale** 8" in block
        for label in ("Wants", "Special", "When bloodied", "Tells", "Breaks", "Nastier"):
            assert f"**{label}:**" in block
        assert "**Twists (d6):**" in block and "6. x" in block
        assert "†" not in block

    def test_overrides_carry_a_dagger(self, core):
        e = make_enemy(level=1, role="mook", damage_override=1, attack_override=-1)
        block = bb.render_block(e, core)
        assert "**Damage** 1†" in block and "**Attack** −1†" in block
        assert "overrides the level table" in block

    def test_mook_line_and_mob_note(self, core):
        block = bb.render_block(make_enemy(role="mook"), core)
        assert "drops to any hit" in block
        assert "mob" in block
        assert "When bloodied" not in block

    def test_boss_phase_and_fearless(self, core):
        block = bb.render_block(make_enemy(level=2, role="boss", morale=12), core)
        assert "Changes phase when Bloodied" in block
        assert "(fearless)" in block
        assert "**Attacks** 2" in block


class TestFillChapter:
    def test_fills_marker(self, core):
        e = make_enemy(id="gob")
        text = "Intro\n<!-- statblock: gob -->\nold\n<!-- /statblock -->\nOutro\n"
        out = bb.fill_chapter(text, {"gob": e}, "B1.md", core)
        assert "old" not in out and "**HP** 8" in out and out.startswith("Intro")

    def test_idempotent(self, core):
        e = make_enemy(id="gob")
        text = "<!-- statblock: gob -->\n<!-- /statblock -->\n"
        once = bb.fill_chapter(text, {"gob": e}, "B1.md", core)
        assert bb.fill_chapter(once, {"gob": e}, "B1.md", core) == once

    def test_unknown_id_raises(self, core):
        with pytest.raises(KeyError):
            bb.fill_chapter("<!-- statblock: ghost -->\n<!-- /statblock -->", {}, "B1.md", core)


class TestFindingAids:
    def test_sorted_by_level_then_role(self, core):
        es = {"a": make_enemy(id="a", name="Alpha", level=2, role="boss"),
              "b": make_enemy(id="b", name="Beta", level=1, role="standard"),
              "c": make_enemy(id="c", name="Gamma", level=2, role="mook")}
        where = {k: "B1_Beasts_and_Vermin.md" for k in es}
        text = bb.generate_finding_aids_text(es, where, core)
        by_level = text.split("## By Role")[0]
        assert by_level.index("Beta") < by_level.index("Gamma") < by_level.index("Alpha")

    def test_only_referenced_creatures_listed(self, core):
        es = {"a": make_enemy(id="a", name="Alpha"), "b": make_enemy(id="b", name="Beta")}
        text = bb.generate_finding_aids_text(es, {"a": "B2_Folk.md"}, core)
        assert "Alpha" in text and "Beta" not in text

    def test_captions_are_numbered(self, core):
        text = bb.generate_finding_aids_text({}, {}, core)
        assert "**Table B0–1: Creatures by Level**" in text
        assert "**Table B0–2: Creatures by Role**" in text

    def test_real_finding_aids_list_every_creature(self):
        text = bb.FINDING_AIDS.read_text(encoding="utf-8")
        enemies = bb.load_enemies()
        for eid in bb.referenced_ids():
            assert enemies[eid].name in text


class TestBestiaryBuild:
    def test_build_on_a_copy(self, tmp_path):
        bdir = tmp_path / "bestiary"
        shutil.copytree(bb.BESTIARY_DIR, bdir)
        # Blank one stat block and delete the aids: both must be reported.
        ch = bdir / bb.CHAPTERS[0]
        text = ch.read_text(encoding="utf-8")
        text = bb.BLOCK.sub(lambda m: m.group(1) + m.group(3), text, count=1)
        ch.write_text(text, encoding="utf-8")
        (bdir / "Finding_Aids.md").unlink()
        changed = bb.build(write=True, bestiary_dir=bdir)
        assert bb.CHAPTERS[0] in changed and "Finding_Aids.md" in changed
        assert bb.build(write=False, bestiary_dir=bdir) == []

    def test_real_bestiary_is_up_to_date(self):
        assert bb.build(write=False) == []

    def test_load_enemies_reads_every_card(self):
        enemies = bb.load_enemies()
        assert len(enemies) == len(list(bb.ENEMY_DIR.glob("*.fof")))
        assert all(e.name for e in enemies.values())

    def test_signed_uses_true_minus(self):
        assert bb.signed(2) == "+2" and bb.signed(0) == "+0" and bb.signed(-1) == "−1"


# ---------------------------------------------------------------------------
# build_scene_cards
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def full():
    return sc.load_ruleset()


class TestRenderStatline:
    def test_standard_line(self, full):
        line = sc.render_statline(make_enemy(level=3, armor=1, morale=8), full)
        assert line.startswith("**standard 3** · *level 3 Standard* · HP **14** · attack +2 · "
                               "damage 6 · armor 1 · morale 8")
        assert "**Wants:** w" in line and "Twists" not in line

    def test_mook_mob_line(self, full):
        line = sc.render_statline(make_enemy(role="mook"), full)
        assert "drops to any hit" in line
        assert "per extra in the mob, max +4" in line

    def test_elite_two_attacks_and_override_dagger(self, full):
        line = sc.render_statline(make_enemy(role="elite", hp_override=30), full)
        assert "two attacks" in line and "HP **30**†" in line


class TestRenderPregen:
    def test_gifted_pregen(self, full):
        fof = yaml.safe_load((REPO / "adventures/oraga_night/characters/andra.fof").read_text())
        block = sc.render_pregen(fof, full)
        assert "**Lineage:** Orthaen — **gifted**" in block
        assert "Minor workings in Inscription" in block
        assert "**HP 6**" in block and "*curios:*" in block
        assert "**Suggested agenda:**" in block

    def test_ungifted_pregen(self, full):
        fof = yaml.safe_load((REPO / "adventures/oraga_night/characters/dassa.fof").read_text())
        assert "**Lineage:** Orthaen — ungifted" in sc.render_pregen(fof, full)

    def test_cast_caster_prints_magic(self, full):
        fof = yaml.safe_load((REPO / "characters/Zahna.fof").read_text())
        block = sc.render_pregen(fof, full)
        assert "**Magic:** Thaumaturgy (Mind) — Inscription" in block
        assert "**Signature workings:**" in block
        assert "**Lineage:** Human" in block

    def test_cast_warrior_weapon_die_includes_weapon_master(self, full):
        fof = yaml.safe_load((REPO / "characters/Mordai.fof").read_text())
        block = sc.render_pregen(fof, full)
        assert "Longsword (d10)" in block and "Weapon Master (blades)" in block

    def test_v03_pregen_refused(self, full):
        with pytest.raises(ValueError):
            sc.render_pregen({"type": "character", "fof_version": "0.1",
                              "character": {"attributes": {}}}, full)


class TestSceneCardFill:
    def test_fill_both_kinds(self, full):
        fof = yaml.safe_load((REPO / "characters/Mordai.fof").read_text())
        text = ("<!-- statline: gob -->\n<!-- /statline -->\n"
                "<!-- pregen: mordai -->\n<!-- /pregen -->\n")
        out, missing = sc.fill_text(text, {"gob": make_enemy(id="gob")}, {"mordai": fof}, full)
        assert not missing and "HP **8**" in out and "**HP 16**" in out

    def test_unknown_ids_reported_and_left(self, full):
        text = "<!-- statline: nobody -->\nkeep\n<!-- /statline -->\n"
        out, missing = sc.fill_text(text, {}, {}, full)
        assert missing == ["nobody"] and out == text

    def test_build_unknown_marker_exits(self, tmp_path):
        mod = tmp_path / "mod"
        mod.mkdir()
        (mod / "cards.md").write_text("<!-- statline: nobody -->\n<!-- /statline -->\n")
        with pytest.raises(SystemExit):
            sc.build(write=False, adventures=tmp_path)

    def test_build_on_a_copy_then_clean(self, tmp_path):
        mod = tmp_path / "mod"
        mod.mkdir()
        (mod / "cards.md").write_text("<!-- statline: chicken -->\n<!-- /statline -->\n")
        assert len(sc.build(write=True, adventures=tmp_path)) == 1
        assert sc.build(write=False, adventures=tmp_path) == []
        assert "Chicken" in (mod / "cards.md").read_text()

    def test_real_adventures_up_to_date(self):
        assert sc.build(write=False) == []

    def test_module_enemies_shadow_bestiary(self):
        enemies = sc.load_enemies(REPO / "adventures" / "oraga_night")
        assert "tavva" in enemies and "chicken" in enemies

    def test_statline_regex_group_two_is_the_id(self):
        m = sc.STATLINE.search("<!-- statline: bought_blade -->\nx\n<!-- /statline -->")
        assert m.group(2) == "bought_blade"


# ---------------------------------------------------------------------------
# build_toolbox
# ---------------------------------------------------------------------------

def _table(tid="t", name="Tee", die="1d6", entries=None, use="Use it."):
    entries = entries or [{"roll": "1-3", "text": "low"}, {"roll": "4-6", "text": "high | pipe"}]
    return TableDef(id=tid, name=name, die=die, use=use, entries=entries)


class TestRenderTable:
    def test_caption_and_header(self):
        out = tbx.render_table(_table(), 3)
        assert "**Table MM6–3: Tee**" in out
        assert "| 1d6 | Result |" in out and out.startswith("*Roll 1d6. Use it.*")

    def test_en_dash_ranges_and_escaped_pipes(self):
        out = tbx.render_table(_table(), 1)
        assert "| 1–3 | low |" in out and "high \\| pipe" in out

    def test_caption_sits_directly_above_the_table(self):
        lines = tbx.render_table(_table(), 1).split("\n")
        idx = lines.index("| 1d6 | Result |")
        assert lines[idx - 1] == "" and lines[idx - 2].startswith("**Table MM6–1")


class TestToolboxFill:
    def test_numbers_in_marker_order(self):
        tables = {"a": _table("a", "A"), "b": _table("b", "B")}
        text = ("<!-- table: b -->\n<!-- /table -->\n"
                "<!-- table: a -->\n<!-- /table -->\n")
        out, unknown = tbx.fill_text(text, tables)
        assert not unknown
        assert out.index("MM6–1: B") < out.index("MM6–2: A")

    def test_hand_captions_before_a_marker_count(self):
        tables = {"a": _table("a", "A")}
        text = "**Table MM6–1: Hand**\n\n<!-- table: a -->\n<!-- /table -->\n"
        out, _ = tbx.fill_text(text, tables)
        assert "**Table MM6–2: A**" in out

    def test_regeneration_is_stable(self):
        tables = {"a": _table("a", "A")}
        once, _ = tbx.fill_text("<!-- table: a -->\n<!-- /table -->\n", tables)
        twice, _ = tbx.fill_text(once, tables)
        assert once == twice

    def test_unknown_marker_reported(self):
        out, unknown = tbx.fill_text("<!-- table: zz -->\n<!-- /table -->\n", {})
        assert unknown == ["zz"]


class TestToolboxBuild:
    def _setup(self, tmp_path, marker="reaction"):
        mm6 = tmp_path / "MM6.md"
        mm6.write_text(f"# MM6\n\n<!-- table: {marker} -->\n<!-- /table -->\n")
        tables = tmp_path / "tables.yaml"
        shutil.copy(tbx.TABLES_YAML, tables)
        return mm6, tables

    def test_build_then_clean(self, tmp_path):
        mm6, tables = self._setup(tmp_path)
        assert tbx.build(write=False, path=mm6, tables_path=tables) == ["MM6.md"]
        assert tbx.build(write=True, path=mm6, tables_path=tables) == ["MM6.md"]
        assert tbx.build(write=False, path=mm6, tables_path=tables) == []
        assert "**Table MM6–1: Reaction**" in mm6.read_text()

    def test_unknown_marker_raises(self, tmp_path):
        mm6, tables = self._setup(tmp_path, marker="no_such")
        with pytest.raises(KeyError):
            tbx.build(write=False, path=mm6, tables_path=tables)

    def test_missing_files_noted(self, tmp_path):
        mm6, tables = self._setup(tmp_path)
        assert tbx.build(False, path=tmp_path / "none.md", tables_path=tables) == ["none.md (missing)"]
        assert tbx.build(False, path=mm6, tables_path=tmp_path / "x.yaml") == ["x.yaml (missing)"]

    def test_placed_and_unplaced(self, tmp_path):
        mm6, tables = self._setup(tmp_path)
        assert tbx.placed_ids(mm6) == ["reaction"]
        unplaced = tbx.unplaced_tables(mm6, tables)
        assert "reaction" not in unplaced and "oracle_themes" in unplaced

    def test_real_mm6_marks_every_table(self):
        assert sorted(tbx.placed_ids()) == sorted(tbx.load_tables())


# ---------------------------------------------------------------------------
# build_table_register
# ---------------------------------------------------------------------------

class TestTableRegister:
    def _files(self):
        return {f for _, _, files in tr.BOOK_ORDER for f in files}

    def test_book_order_has_the_v1_chapters(self):
        files = self._files()
        for name in ("II.2_Character_Creation_Stats.md", "IV.2_Treasure.md", "MM6_The_Toolbox.md"):
            assert name in files
        assert "II.7_Character_Creation_Skills.md" not in files
        assert "II.2_Character_Creation_Attributes.md" not in files

    def test_register_generates(self):
        text = tr.generate_register_text()
        assert text.startswith("# List of Tables")
        assert "Mirror Master's Manual" in text

    def test_box_register_generates(self):
        assert tr.generate_box_register_text().startswith("# List of Boxes")
