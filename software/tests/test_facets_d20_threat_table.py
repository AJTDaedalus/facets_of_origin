"""Facets d20 — Table 9–2 (per-monster Threat) and the numbers printed in chapter 09.

BRIEF Amendment 4, ruling 2: every SRD 5.2.1 monster in ``srd_monsters.yaml`` is priced
from its own stat block by the engine (``facets_d20.analysis``) and printed in
``facets_d20/Appendix_Monster_Threat.md`` by ``tools/build_d20_threat_table.py``, which
carries no rule of its own. Chapter 09 is hand-written; the tests below hold every
encounter number it prints to the yaml the simulator wrote.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import pytest
import yaml

from facets_d20 import analysis as A
from facets_d20 import monsters as M

REPO = Path(__file__).resolve().parents[2]
RULES = REPO / "facets_d20" / "data" / "facets_d20.yaml"
LADDER = REPO / "software" / "facets_d20" / "data" / "srd_monsters.yaml"
APPENDIX = REPO / "facets_d20" / "Appendix_Monster_Threat.md"
CH09 = REPO / "facets_d20" / "09_Mirror_Masters_Guide.md"


@pytest.fixture(scope="module")
def raw():
    return yaml.safe_load(RULES.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ladder_ids():
    return [m["id"] for m in yaml.safe_load(LADDER.read_text(encoding="utf-8"))["monsters"]]


@pytest.fixture(scope="module")
def model(raw):
    return A.threat_model_from_data(raw)


@pytest.fixture(scope="module")
def rows(raw):
    return A.threat_appendix(raw)


# ================================================================ the pricing model from the yaml


class TestThreatModelFromData:
    def test_reads_the_printed_constants(self, model, raw):
        # Re-derived by the Edges pass (edges on every preset; V56 stabilizing).
        assert model.minion_hp == pytest.approx(8.6)
        assert model.boss == pytest.approx(3.43)
        assert model.never == pytest.approx(1.17)
        assert model.hard == pytest.approx(1.07)
        assert A.lone_boss_factor(raw) == pytest.approx(1.2)

    def test_reproduces_the_yaml_threat_by_cr_table(self, model, raw):
        assert model.table() == raw["monster_threat"]["by_cr"]

    def test_default_reads_the_shipped_yaml(self, model):
        assert A.threat_model_from_data() == model

    def test_missing_constant_is_an_error(self, raw):
        broken = {**raw, "monster_threat": {"model": {"standard": "sqrt(HP x damage per turn)"}}}
        with pytest.raises(ValueError):
            A.threat_model_from_data(broken)


class TestClashTotals:
    def test_is_four_times_the_per_character_budget(self, raw):
        totals = A.clash_totals(raw)
        assert totals == {L: 4 * raw["encounter_table"][L]["clash"] for L in range(1, 11)}

    def test_other_party_sizes_scale_per_character(self, raw):
        assert A.clash_totals(raw, party_size=5)[4] == 5 * raw["encounter_table"][4]["clash"]

    def test_unknown_tier_is_an_error(self, raw):
        with pytest.raises(KeyError):
            A.clash_totals(raw, tier="massacre")


# ================================================================ one row per monster


class TestMonsterRow:
    def test_values_are_the_engines_pricing(self, rows, model):
        for r in rows:
            blk = M.get(r["id"])
            for role in ("standard", "minion", "boss"):
                assert r[role] == round(model.of(blk, role)), (r["id"], role)

    def test_every_yaml_monster_appears_once(self, rows, ladder_ids):
        ids = [r["id"] for r in rows]
        assert sorted(ids) == sorted(ladder_ids)
        assert len(ids) == len(set(ids))

    def test_engine_only_blocks_are_left_out(self, rows):
        ids = {r["id"] for r in rows}
        assert "bandit_leader" not in ids and "brute" not in ids

    def test_sorted_by_cr_then_name(self, rows):
        keys = [(M.get(r["id"]).cr, r["name"]) for r in rows]
        assert keys == sorted(keys)

    def test_never_breaks_flag_follows_morale(self, rows):
        for r in rows:
            assert r["never"] == (M.get(r["id"]).morale == "never")
        assert {r["id"] for r in rows if r["never"]} >= {"zombie", "skeleton"}

    def test_hard_hitter_flag_is_damage_above_the_cr_line(self, rows):
        for r in rows:
            blk = M.get(r["id"])
            line = A.generic(float(blk.cr)).damage_per_turn
            assert r["hits_hard"] == (blk.routine_damage >= A.HARD_HITTER_FACTOR * line), r["id"]

    def test_a_known_hard_hitter_and_a_known_soft_one(self, rows):
        by = {r["id"]: r for r in rows}
        assert by["hobgoblin_warrior"]["hits_hard"]      # 12 a turn at CR 1/2
        assert not by["ogre"]["hits_hard"]

    def test_standard_levels_are_where_three_to_ten_make_a_clash(self, rows, raw):
        totals = A.clash_totals(raw)
        lo, hi = A.STANDARD_COUNT
        for r in rows:
            want = [L for L, t in totals.items() if lo <= t / r["standard"] <= hi]
            assert r["standard_levels"] == want, r["id"]

    def test_boss_levels_are_where_it_is_half_to_all_of_a_clash(self, rows, raw):
        totals = A.clash_totals(raw)
        lo, hi = A.BOSS_SHARE
        for r in rows:
            want = [L for L, t in totals.items() if lo <= r["boss"] / t <= hi]
            assert r["boss_levels"] == want, r["id"]

    def test_ogre_pinned(self, rows):
        ogre = next(r for r in rows if r["id"] == "ogre")
        # Edges pass: minion 8.6, boss 3.43 (re-derived with edges on every preset).
        assert (ogre["standard"], ogre["minion"], ogre["boss"]) == (30, 11, 102)
        assert ogre["standard_levels"] == [3, 4, 5, 6, 7, 8]
        assert ogre["boss_levels"] == [4, 5]

    def test_row_needs_budget_totals(self, model):
        with pytest.raises(ValueError):
            A.monster_threat_row(M.get("ogre"), model, {})


class TestLevelRange:
    def test_contiguous_range_prints_with_a_dash(self):
        assert A.level_range([3, 4, 5]) == "3–5"

    def test_single_level(self):
        assert A.level_range([1]) == "1"

    def test_empty_is_a_dash(self):
        assert A.level_range([]) == "—"

    def test_gap_is_an_error(self):
        with pytest.raises(ValueError):
            A.level_range([1, 3])


# ================================================================ the generated appendix


def _table_rows(text: str) -> list[list[str]]:
    body = text.split("<!-- threat-table -->", 1)[1].split("<!-- /threat-table -->", 1)[0]
    lines = [l for l in body.splitlines() if l.startswith("| ") and not l.startswith("| Monster")]
    return [[c.strip() for c in l.strip("|").split("|")] for l in lines]


class TestAppendix:
    def test_regenerates_with_no_diff(self):
        from tools.build_d20_threat_table import build
        assert build(check=True) == [], (
            "Appendix_Monster_Threat.md is stale — run `python -m tools.build_d20_threat_table`")

    def test_every_monster_appears_once(self, ladder_ids):
        names = [row[0] for row in _table_rows(APPENDIX.read_text(encoding="utf-8"))]
        want = sorted(M.get(i).name for i in ladder_ids)
        assert sorted(names) == want

    def test_printed_values_match_the_engine(self, rows):
        printed = {row[0]: row for row in _table_rows(APPENDIX.read_text(encoding="utf-8"))}
        for r in rows:
            row = printed[r["name"]]
            assert row[2:5] == [str(r["standard"]), str(r["minion"]), str(r["boss"])], r["id"]
            assert row[5] == A.level_range(r["standard_levels"])
            assert row[6] == A.level_range(r["boss_levels"])

    def test_carries_the_generated_note_and_srd_attribution(self):
        text = APPENDIX.read_text(encoding="utf-8")
        assert "Generated — do not edit" in text
        assert "System Reference Document 5.2.1" in text
        assert "Creative Commons Attribution 4.0" in text
        assert "**Table 9–2:" in text

    def test_render_is_deterministic(self):
        from tools.build_d20_threat_table import render_region
        assert render_region() == render_region()

    def test_fill_replaces_only_the_marked_region(self):
        from tools.build_d20_threat_table import fill
        text = "head\n<!-- threat-table -->\nold\n<!-- /threat-table -->\ntail\n"
        out = fill(text, "NEW\n")
        assert out == "head\n<!-- threat-table -->\nNEW\n<!-- /threat-table -->\ntail\n"

    def test_fill_without_markers_is_an_error(self):
        from tools.build_d20_threat_table import fill
        with pytest.raises(ValueError):
            fill("no markers here", "x")


# ================================================================ chapter 09's numbers


def _md_table(text: str, caption: str) -> list[list[str]]:
    start = text.index(caption)
    rows = []
    for line in text[start:].splitlines()[1:]:
        if not line.strip():
            if rows:
                break
            continue
        if not line.startswith("|"):
            break
        rows.append([c.strip().strip("*") for c in line.strip().strip("|").split("|")])
    return rows[2:]   # header and rule


@pytest.fixture(scope="module")
def ch09():
    return CH09.read_text(encoding="utf-8")


class TestChapter09Numbers:
    def test_table_9_1_is_the_yaml_encounter_table(self, ch09, raw):
        rows = _md_table(ch09, "**Table 9–1:")
        got = {int(r[0]): [int(x) for x in r[1:5]] for r in rows}
        want = {L: [raw["encounter_table"][L][t] for t in A.TIERS] for L in range(1, 11)}
        assert got == want

    def test_threat_by_cr_table_is_the_yaml(self, ch09, raw):
        rows = _md_table(ch09, "**Table 9–3:")
        got = {r[0]: [int(x) for x in r[1:5]] for r in rows}
        want = {str(cr): [v["standard"], v["minion"], v["boss"], v["damage"]]
                for cr, v in raw["monster_threat"]["by_cr"].items()}
        assert got == want

    def test_pricing_constants_match_the_yaml(self, ch09, model, raw):
        assert f"√({model.minion_hp:g} × damage per turn)" in ch09
        assert f"× {model.boss:.2f}" in ch09
        assert f"× {model.never:.2f}" in ch09
        assert f"× {model.hard:.2f}** in every role" in ch09
        assert f"× {A.lone_boss_factor(raw):g}" in ch09

    def test_adventuring_day_is_three_clashes(self, ch09, raw):
        day = raw["adventuring_day"]
        assert day["clashes"] == 3 and day["short_rests_after"] == [1, 2]
        assert "three Clashes" in ch09 and "short rest after the first and the second" in ch09

    def test_baseline_budget_is_four_times_the_4th_level_row(self, ch09, raw):
        per = raw["encounter_table"][4]["clash"]
        assert f"{per} × 4 = {4 * per}" in ch09

    def test_example_monsters_carry_their_appendix_threat(self, ch09, rows):
        by_name = {r["name"]: r for r in rows}
        found = re.findall(r"\*\*([A-Z][A-Za-z ]+?)\*\*s?(?: [a-z]+)? \((standard|minion|boss), (\d+)\)", ch09)
        assert len(found) >= 5
        for name, role, value in found:
            assert int(value) == by_name[name][role], (name, role)

    def test_example_sums_add_up(self, ch09):
        for expr, total in re.findall(r"`([\d ×+.]+) = (\d+)`", ch09):
            value = eval(expr.replace("×", "*"))   # noqa: S307 — digits and operators only
            assert round(value) == int(total), expr

    def test_tier_targets_are_the_yamls(self, ch09, raw):
        for tier in raw["encounter_tiers"]:
            lo, hi = tier["targets"]["party_hp_lost_pct"]
            line = next(l for l in ch09.splitlines() if l.startswith(f"- **{tier['name']}:**"))
            assert f"{lo}–{hi}% of the party's hit points" in line, tier["id"]
            if "win_pct_max" in tier["targets"]:
                t = tier["targets"]
                assert f"wins {t['win_pct_min']}–{t['win_pct_max']}% of the time" in line

    def test_party_size_numbers_are_the_yamls(self, ch09, raw):
        adj = raw["encounter_adjustments"]
        three, five, six = (abs(adj[k]["clash_pct"]) for k in ("three_players", "five_players", "six_players"))
        assert f"three players need {three}% less, five {five}% more, six {six}% more" in ch09

    def test_terminology_and_attribution(self, ch09):
        for bad in (r"\bGM\b", r"\bDM\b", r"D&D", r"Dungeon Master"):
            assert not re.search(bad, ch09), bad
        assert "Mirror Master (MM)" in ch09
        assert "System Reference Document 5.2.1" in ch09
        assert "Appendix_Monster_Threat.md" in ch09

    def test_tables_are_numbered_in_order(self, ch09):
        nums = [int(n) for n in re.findall(r"^\*\*Table 9–(\d+):", ch09, re.M)]
        assert nums == sorted(nums) and len(nums) == len(set(nums))
        assert 2 not in nums   # Table 9–2 lives in the appendix


class TestPlaytestFixPass:
    """docs/PLAYTEST_facets_d20_fresh_mm.md: the fixes chapter 09 and 10 print."""

    def test_hard_hitters_are_priced_not_a_tier_cliff(self, ch09, model, raw):
        # Amendment 4 item 2, implemented precisely: the mark-up lives in Table 9–2.
        assert "next tier up" not in ch09 and "counts as the next tier" not in ch09
        assert model.hard > 1.0
        assert raw["monster_threat"]["model"]["hard_hitter"].startswith("x ")

    def test_hard_hitters_carry_the_mark_up_in_every_role(self, model):
        knight = M.get("knight")
        assert A.hits_hard(knight)
        base = A.ThreatModel(minion_hp=model.minion_hp, boss=model.boss, never=model.never)
        for role in ("standard", "minion", "boss"):
            assert model.of(knight, role) == pytest.approx(base.of(knight, role) * model.hard)

    def test_soft_monsters_are_unchanged(self, model):
        ogre = M.get("ogre")
        assert not A.hits_hard(ogre)
        base = A.ThreatModel(minion_hp=model.minion_hp, boss=model.boss, never=model.never)
        assert model.of(ogre) == pytest.approx(base.of(ogre))

    def test_generic_foes_never_hit_hard(self):
        for cr in M.TEMPLATE_CRS:
            assert not A.hits_hard(A.generic(float(cr)))

    def test_owlbear_worked_example(self, ch09, rows):
        owl = next(r for r in rows if r["name"] == "Owlbear")
        assert f"Table 9–2 gives as {owl['boss']}" in ch09

    def test_quick_reference_budget_is_the_yaml(self, raw):
        qr = (REPO / "facets_d20" / "10_Quick_Reference.md").read_text(encoding="utf-8")
        rows = _md_table(qr, "**Table 10–6:")
        got = {int(r[0]): [int(x) for x in r[1:5]] for r in rows}
        want = {L: [raw["encounter_table"][L][t] for t in A.TIERS] for L in range(1, 11)}
        assert got == want

    def test_boss_rules_in_one_place(self, ch09):
        sec = ch09.split("### Bosses")[1].split("### Ending the Fight")[0]
        for phrase in ("twice its stat block's hit points", "top of the round",
                       "right after the first character's turn", "reaction", "Recharge",
                       "whether or not it allowed a save", "surprised"):
            assert phrase in sec, phrase

    def test_boss_heavy_and_four_character_warnings(self, ch09):
        assert "three-quarters of the budget" in ch09
        assert "*Boss at levels* column is for four characters" in ch09
        assert "less than a fifth" in ch09

    def test_short_rest_and_survive_defined(self, ch09):
        assert "What a short rest gives back" in ch09
        assert "*survive* means" in ch09


class TestConversionRules:
    """09 *Pricing Any SRD Monster*, steps 1–2 (playtest fix pass, MM #3)."""

    def test_alternative_routines_take_the_higher(self):
        claws = [{"fixed": 7}, {"fixed": 6, "count": 2}]
        spikes = [{"fixed": 7, "count": 3}]
        assert M.turn_damage([claws, spikes]) == 21

    def test_area_counts_twice(self):
        assert M.turn_damage([[{"fixed": 10, "targets": 3}]]) == 20

    def test_save_counts_in_full(self):
        assert M.turn_damage([[{"fixed": 12, "save": True}]]) == 12

    def test_limited_spells_left_out(self):
        assert M.turn_damage([[{"fixed": 8}, {"fixed": 28, "targets": 4, "limited": True}]]) == 8

    def test_recharge_adds_a_quarter_after_the_area_doubling(self):
        # A breath of 56 on two or more: 56 × 2 ÷ 4 = 28 on top of the attacks.
        assert M.turn_damage([[{"fixed": 16, "count": 3},
                               {"fixed": 56, "targets": 2, "recharge": True}]]) == 48 + 28

    def test_ladder_recharge_monsters_price_the_quarter(self):
        red = M.get("young_red_dragon")
        assert red.routine_damage == 48
        assert red.damage_per_turn == 48 + (56 * 2) // 4

    def test_resistance_doubles_hit_points_and_regeneration_adds_three_rounds(self):
        assert M.effective_hp(40, resists_party=True) == 80
        assert M.effective_hp(40, regeneration=10) == 70

    def test_effective_hp_rejects_negatives(self):
        with pytest.raises(ValueError):
            M.effective_hp(-1)

    def test_resistance_is_worth_root_two(self, model):
        plain = model.price(40, 10)
        resisted = model.price(M.effective_hp(40, resists_party=True), 10)
        assert resisted / plain == pytest.approx(math.sqrt(2))

    def test_ladder_damage_uses_the_same_rule(self):
        ogre = M.get("ogre")
        assert ogre.damage_per_turn == M.turn_damage(
            [[{"fixed": a.fixed, "count": a.count} for a in ogre.attacks]])

    def test_price_rejects_unknown_role(self, model):
        with pytest.raises(ValueError):
            model.price(10, 10, "villain")


class TestBossMarkup:
    def test_alone_is_the_lone_factor(self, raw):
        assert A.boss_markup(100, 0, raw) == pytest.approx(1.2)

    def test_small_company_is_one_point_one(self, raw):
        assert A.boss_markup(100, 19, raw) == pytest.approx(1.1)

    def test_real_company_is_no_markup(self, raw):
        assert A.boss_markup(100, 20, raw) == 1.0

    def test_rejects_nonsense(self, raw):
        with pytest.raises(ValueError):
            A.boss_markup(0, 10, raw)

    def test_chapter_09_states_both(self, ch09):
        assert "counts **× 1.2**" in ch09 and "counts **× 1.1**" in ch09
