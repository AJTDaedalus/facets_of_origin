"""Facets d20 — talent menus, presets and signatures (facets_d20/data/facets_d20.yaml).

The contract is docs/DESIGN_facets_d20.md §1–§2. These tests pin the fixed numbers,
the shape of every talent menu, and the legality of every preset build: each preset's
recommended picks must be takeable, in order, by a real character following the
tier, level, prerequisite and cross-Facet rules the books print.
"""
from __future__ import annotations

import copy
import math
from pathlib import Path

import pytest
import yaml

DATA = Path(__file__).resolve().parents[2] / "facets_d20" / "data" / "facets_d20.yaml"

FACETS = ("body", "mind", "soul")

# DESIGN §1, verbatim.
EXPECTED_NUMBERS = {
    "body": dict(hit_die=10, hp_first=10, hp_per_level=6, saves=["str", "con"],
                 armor=["light", "medium", "heavy", "shields"],
                 weapons=["simple", "martial"], skill_picks=3, talents_at_first=3,
                 extra_attack_level=5, tradition=None),
    "mind": dict(hit_die=6, hp_first=6, hp_per_level=4, saves=["int", "wis"],
                 armor=["light"], weapons=["simple"], skill_picks=4,
                 talents_at_first=2, extra_attack_level=None, tradition="thaumaturgy"),
    "soul": dict(hit_die=8, hp_first=8, hp_per_level=5, saves=["wis", "cha"],
                 armor=["light", "medium", "shields"], weapons=["simple"],
                 skill_picks=3, talents_at_first=2, extra_attack_level=None,
                 tradition="invocation"),
}
TIER_MIN_LEVEL = {1: 1, 2: 3, 3: 6}
TRADITION_TALENTS = {"thaumaturgy", "invocation"}


# ---------------------------------------------------------------- helpers

def load(path: Path = DATA) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def talents_by_id(data: dict) -> dict:
    return {t["id"]: t for t in data["talents"]}


def prereqs(talent: dict) -> list[str]:
    """A talent's prerequisite: None, one id, or a list meaning 'any one of these'."""
    p = talent.get("prereq")
    if p is None:
        return []
    return [p] if isinstance(p, str) else list(p)


def min_level(talent: dict) -> int:
    return max(TIER_MIN_LEVEL[talent["tier"]], talent.get("min_level") or 1)


def normalise_pick(pick) -> tuple[str, bool]:
    if isinstance(pick, str):
        return pick, False
    return pick["id"], bool(pick.get("cross", False))


def preset_build(preset: dict) -> list[tuple[int, str, bool]]:
    """Every talent pick a preset makes, as (level, talent id, cross?) in order."""
    picks = [(1, t, False) for t in preset["level1_talents"]]
    for level in sorted(preset["recommended_picks"]):
        tid, cross = normalise_pick(preset["recommended_picks"][level])
        picks.append((int(level), tid, cross))
    return picks


def build_errors(data: dict, preset: dict) -> list[str]:
    """Replay a preset's build and return every rule it breaks (empty = legal)."""
    talents = talents_by_id(data)
    facet = preset["facet"]
    taken: list[str] = []
    errors: list[str] = []
    for level, tid, cross in preset_build(preset):
        t = talents.get(tid)
        if t is None:
            errors.append(f"L{level}: unknown talent {tid}")
            continue
        own = facet in t["facets"]
        if own and cross:
            errors.append(f"L{level}: {tid} is in the {facet} menu but flagged cross")
        if not own:
            if not cross:
                errors.append(f"L{level}: {tid} is not in the {facet} menu and not flagged cross")
            if level < 2:
                errors.append(f"L{level}: cross-Facet pick {tid} before 2nd level")
            if t["tier"] >= 2:
                from_there = [x for x in taken
                              if any(f in talents[x]["facets"] for f in t["facets"])
                              and facet not in talents[x]["facets"]]
                if len(from_there) < 2:
                    errors.append(f"L{level}: cross-Facet T{t['tier']} {tid} without two talents from that Facet")
        if level < min_level(t):
            errors.append(f"L{level}: {tid} needs level {min_level(t)}")
        req = prereqs(t)
        if req and not any(r in taken for r in req):
            errors.append(f"L{level}: {tid} needs one of {req} first")
        if tid in taken and not t.get("repeatable", False):
            errors.append(f"L{level}: {tid} taken twice")
        taken.append(tid)
    return errors


def talents_before(preset: dict, level: int) -> list[str]:
    return [tid for lvl, tid, _ in preset_build(preset) if lvl <= level]


@pytest.fixture(scope="module")
def data() -> dict:
    return load()


@pytest.fixture(scope="module")
def talents(data) -> dict:
    return talents_by_id(data)


# ---------------------------------------------------------------- loading

class TestLoads:
    def test_file_exists(self):
        assert DATA.is_file(), DATA

    def test_parses_to_mapping(self, data):
        assert isinstance(data, dict)

    def test_has_top_level_sections(self, data):
        for key in ("facets", "talents", "presets", "signatures"):
            assert key in data, key

    def test_levels_are_one_to_ten(self, data):
        assert data["levels"] == {"min": 1, "max": 10}

    def test_proficiency_bonus_table(self, data):
        pb = {int(k): v for k, v in data["proficiency_bonus"].items()}
        assert pb == {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4}

    def test_tier_levels(self, data):
        assert {int(k): v for k, v in data["talent_tiers"].items()} == TIER_MIN_LEVEL


# ---------------------------------------------------------------- facet numbers

class TestFacetNumbers:
    def test_exactly_three_facets(self, data):
        assert sorted(data["facets"]) == sorted(FACETS)

    @pytest.mark.parametrize("facet", FACETS)
    def test_numbers_match_design(self, data, facet):
        f = data["facets"][facet]
        for key, value in EXPECTED_NUMBERS[facet].items():
            assert f[key] == value, (facet, key, f[key], value)

    @pytest.mark.parametrize("facet", FACETS)
    def test_exactly_one_facet_feature(self, data, facet):
        feature = data["facets"][facet]["feature"]
        assert isinstance(feature, dict)
        assert feature["id"] and feature["name"] and feature["summary"]

    def test_hp_first_equals_hit_die(self, data):
        for facet in FACETS:
            f = data["facets"][facet]
            assert f["hp_first"] == f["hit_die"]

    def test_hp_per_level_is_fixed_average_rounded_up(self, data):
        for facet in FACETS:
            f = data["facets"][facet]
            assert f["hp_per_level"] == f["hit_die"] // 2 + 1

    def test_only_body_gets_automatic_extra_attack(self, data):
        auto = [f for f in FACETS if data["facets"][f]["extra_attack_level"]]
        assert auto == ["body"]

    def test_body_has_no_tradition(self, data):
        assert data["facets"]["body"]["tradition"] is None

    @pytest.mark.parametrize("facet", FACETS)
    def test_facet_skill_list_covers_picks(self, data, facet):
        f = data["facets"][facet]
        assert len(f["skills"]) > f["skill_picks"]
        assert len(set(f["skills"])) == len(f["skills"])

    def test_tradition_talents_live_in_their_own_menu(self, data, talents):
        for facet in ("mind", "soul"):
            trad = data["facets"][facet]["tradition"]
            assert talents[trad]["facets"] == [facet]
            assert talents[trad]["tier"] == 1


# ---------------------------------------------------------------- talents

class TestTalentIds:
    def test_ids_unique(self, data):
        ids = [t["id"] for t in data["talents"]]
        assert len(ids) == len(set(ids))

    def test_names_unique(self, data):
        names = [t["name"] for t in data["talents"]]
        assert len(names) == len(set(names))

    def test_ids_are_snake_case(self, data):
        for t in data["talents"]:
            assert t["id"] == t["id"].lower() and " " not in t["id"], t["id"]

    def test_signature_ids_do_not_collide_with_talents(self, data, talents):
        for s in data["signatures"]:
            assert s["id"] not in talents


class TestTalentShape:
    REQUIRED = ("id", "name", "facets", "tier", "origin", "summary")

    def test_every_talent_has_required_fields(self, data):
        for t in data["talents"]:
            for key in self.REQUIRED:
                assert key in t, (t.get("id"), key)

    def test_tiers_are_one_two_three(self, data):
        assert {t["tier"] for t in data["talents"]} == {1, 2, 3}

    def test_facets_are_known(self, data):
        for t in data["talents"]:
            assert t["facets"] and set(t["facets"]) <= set(FACETS), t["id"]

    def test_min_level_never_below_tier(self, data):
        for t in data["talents"]:
            if t.get("min_level"):
                assert t["min_level"] >= TIER_MIN_LEVEL[t["tier"]], t["id"]
                assert t["min_level"] <= 10

    def test_origin_only_on_tier_one(self, data):
        for t in data["talents"]:
            if t["origin"]:
                assert t["tier"] == 1, t["id"]

    def test_tradition_talents_are_not_origin(self, talents):
        for tid in TRADITION_TALENTS:
            assert talents[tid]["origin"] is False

    def test_each_menu_has_some_origin_talents(self, data):
        for facet in FACETS:
            assert any(t["origin"] for t in data["talents"] if facet in t["facets"]), facet

    def test_summaries_are_short_rules_text(self, data):
        for t in data["talents"]:
            assert 20 <= len(t["summary"]) <= 400, t["id"]


class TestMenus:
    @pytest.mark.parametrize("facet", FACETS)
    def test_menu_size(self, data, facet):
        menu = [t for t in data["talents"] if facet in t["facets"]]
        assert 18 <= len(menu) <= 24, (facet, len(menu))

    @pytest.mark.parametrize("facet", FACETS)
    def test_menu_has_every_tier(self, data, facet):
        tiers = {t["tier"] for t in data["talents"] if facet in t["facets"]}
        assert tiers == {1, 2, 3}

    def test_asi_in_all_three_menus_repeatable(self, talents):
        asi = talents["ability_score_improvement"]
        assert sorted(asi["facets"]) == sorted(FACETS)
        assert asi["tier"] == 1 and asi.get("repeatable") is True

    def test_thaumaturgy_and_invocation(self, talents):
        assert talents["thaumaturgy"]["name"] == "Thaumaturgy"
        assert talents["invocation"]["name"] == "Invocation"

    def test_wider_study_mind_and_soul_t2(self, talents):
        ws = talents["wider_study"]
        assert ws["name"] == "Wider Study"
        assert sorted(ws["facets"]) == ["mind", "soul"] and ws["tier"] == 2
        assert set(prereqs(ws)) == TRADITION_TALENTS

    def test_martial_training_and_extra_attack_for_mind_and_soul(self, talents):
        assert sorted(talents["martial_training"]["facets"]) == ["mind", "soul"]
        ea = talents["extra_attack"]
        assert sorted(ea["facets"]) == ["mind", "soul"]
        assert ea["tier"] == 2 and ea["min_level"] == 5

    def test_body_menu_lacks_extra_attack_and_traditions(self, data):
        body = {t["id"] for t in data["talents"] if "body" in t["facets"]}
        assert not body & ({"extra_attack", "martial_training"} | TRADITION_TALENTS)

    @pytest.mark.parametrize("tid,facet", [
        ("sneak_attack", "body"), ("rage", "body"), ("martial_arts", "body"),
        ("wild_shape", "soul"), ("mending_hands", "soul"), ("glimpses", "soul"),
        ("sworn_strike", "soul"),
    ])
    def test_signature_shapes_present(self, talents, tid, facet):
        assert facet in talents[tid]["facets"]


class TestPrerequisites:
    def test_each_prereq_exists(self, data, talents):
        for t in data["talents"]:
            for p in prereqs(t):
                assert p in talents, (t["id"], p)

    def test_prereq_same_or_lower_tier(self, data, talents):
        for t in data["talents"]:
            for p in prereqs(t):
                assert talents[p]["tier"] <= t["tier"], (t["id"], p)

    def test_no_self_prereq(self, data):
        for t in data["talents"]:
            assert t["id"] not in prereqs(t)

    def test_at_most_one_prerequisite(self, data):
        # A list means "any one of these" and is only used for the tradition talents.
        for t in data["talents"]:
            p = t.get("prereq")
            if isinstance(p, list):
                assert set(p) <= TRADITION_TALENTS, t["id"]

    def test_prereq_is_reachable_in_a_shared_menu(self, data, talents):
        for t in data["talents"]:
            for facet in t["facets"]:
                req = prereqs(t)
                if req:
                    assert any(facet in talents[p]["facets"] for p in req), (t["id"], facet)


# ---------------------------------------------------------------- signatures

class TestSignatures:
    @pytest.mark.parametrize("facet", FACETS)
    def test_six_per_facet(self, data, facet):
        assert len([s for s in data["signatures"] if s["facet"] == facet]) == 6

    def test_signature_ids_unique(self, data):
        ids = [s["id"] for s in data["signatures"]]
        assert len(ids) == len(set(ids))

    def test_signature_requirements_exist(self, data, talents):
        for s in data["signatures"]:
            for r in ([s["requires"]] if isinstance(s.get("requires"), str)
                      else s.get("requires") or []):
                assert r in talents, (s["id"], r)

    def test_signatures_have_summaries(self, data):
        for s in data["signatures"]:
            assert s["name"] and len(s["summary"]) >= 20


# ---------------------------------------------------------------- presets

class TestPresetRoster:
    @pytest.mark.parametrize("facet", FACETS)
    def test_four_per_facet(self, data, facet):
        assert len([p for p in data["presets"] if p["facet"] == facet]) == 4

    def test_priest_druid_oracle_are_soul(self, data):
        soul = {p["name"] for p in data["presets"] if p["facet"] == "soul"}
        assert {"Priest", "Druid", "Oracle"} <= soul

    def test_body_presets(self, data):
        body = {p["name"] for p in data["presets"] if p["facet"] == "body"}
        assert body == {"Fighter", "Rogue", "Barbarian", "Monk"}

    def test_mind_presets(self, data):
        mind = {p["name"] for p in data["presets"] if p["facet"] == "mind"}
        assert {"Wizard", "Investigator", "Loremaster"} <= mind and len(mind) == 4

    def test_preset_ids_unique(self, data):
        ids = [p["id"] for p in data["presets"]]
        assert len(ids) == len(set(ids))

    def test_each_facet_has_a_non_caster_preset(self, data):
        for facet in FACETS:
            assert any(not set(talents_before(p, 1)) & TRADITION_TALENTS
                       for p in data["presets"] if p["facet"] == facet), facet


class TestPresetCounts:
    def test_level1_talent_count(self, data):
        for p in data["presets"]:
            want = data["facets"][p["facet"]]["talents_at_first"]
            assert len(p["level1_talents"]) == want, p["id"]

    def test_one_pick_every_level_two_to_ten(self, data):
        for p in data["presets"]:
            assert sorted(int(k) for k in p["recommended_picks"]) == list(range(2, 11)), p["id"]

    def test_total_talents_by_tenth(self, data):
        for p in data["presets"]:
            want = data["facets"][p["facet"]]["talents_at_first"] + 9
            assert len(preset_build(p)) == want, p["id"]


class TestPresetLegality:
    def test_every_preset_build_is_legal(self, data):
        problems = {p["id"]: build_errors(data, p) for p in data["presets"]}
        assert not {k: v for k, v in problems.items() if v}

    def test_every_preset_talent_exists(self, data, talents):
        for p in data["presets"]:
            for _, tid, _ in preset_build(p):
                assert tid in talents, (p["id"], tid)

    def test_level1_talents_are_own_menu(self, data, talents):
        for p in data["presets"]:
            for tid in p["level1_talents"]:
                assert p["facet"] in talents[tid]["facets"], (p["id"], tid)

    def test_signature_is_own_facet_and_requirement_met(self, data):
        sigs = {s["id"]: s for s in data["signatures"]}
        for p in data["presets"]:
            s = sigs[p["signature"]]
            assert s["facet"] == p["facet"], p["id"]
            req = s.get("requires")
            if req:
                req = [req] if isinstance(req, str) else req
                assert any(r in talents_before(p, 3) for r in req), p["id"]

    def test_signatures_distinct_within_facet(self, data):
        for facet in FACETS:
            sigs = [p["signature"] for p in data["presets"] if p["facet"] == facet]
            assert len(sigs) == len(set(sigs))

    def test_at_least_one_preset_uses_a_cross_pick(self, data):
        assert any(cross for p in data["presets"] for _, _, cross in preset_build(p))


class TestPresetOriginTalent:
    def test_origin_talent_exists_and_is_flagged(self, data, talents):
        for p in data["presets"]:
            t = talents[p["origin_talent"]]
            assert t["origin"] is True and t["tier"] == 1, p["id"]

    def test_origin_talent_not_repeated_in_build(self, data, talents):
        for p in data["presets"]:
            if not talents[p["origin_talent"]].get("repeatable"):
                assert p["origin_talent"] not in talents_before(p, 10), p["id"]

    def test_origin_talent_never_a_tradition(self, data):
        for p in data["presets"]:
            assert p["origin_talent"] not in TRADITION_TALENTS


class TestBuildChecker:
    """The legality checker must actually catch each kind of illegal build."""

    @pytest.fixture
    def fighter(self, data):
        return copy.deepcopy(next(p for p in data["presets"] if p["id"] == "fighter"))

    def test_catches_tier_two_at_level_two(self, data, fighter):
        fighter["recommended_picks"][2] = "evasion"
        assert any("needs level" in e for e in build_errors(data, fighter))

    def test_catches_tier_three_at_level_five(self, data, fighter):
        fighter["recommended_picks"][5] = "indomitable"
        assert any("needs level" in e for e in build_errors(data, fighter))

    def test_catches_missing_prereq(self, data, fighter):
        fighter["recommended_picks"][3] = "relentless_rage"
        assert any("first" in e for e in build_errors(data, fighter))

    def test_catches_unflagged_cross_pick(self, data, fighter):
        fighter["recommended_picks"][2] = "invocation"
        assert any("not flagged cross" in e for e in build_errors(data, fighter))

    def test_catches_cross_pick_at_first_level(self, data, fighter):
        fighter["level1_talents"][0] = "invocation"
        errs = build_errors(data, fighter)
        assert errs

    def test_catches_cross_tier_two_without_two_from_that_facet(self, data, fighter):
        fighter["recommended_picks"][4] = {"id": "wider_study", "cross": True}
        fighter["recommended_picks"][2] = {"id": "invocation", "cross": True}
        assert any("without two talents" in e for e in build_errors(data, fighter))

    def test_allows_flagged_cross_tier_one_from_second(self, data, fighter):
        fighter["recommended_picks"][2] = {"id": "invocation", "cross": True}
        assert build_errors(data, fighter) == []

    def test_catches_duplicate_non_repeatable(self, data, fighter):
        fighter["recommended_picks"][2] = "weapon_mastery"
        assert any("twice" in e for e in build_errors(data, fighter))

    def test_asi_may_repeat(self, data, fighter):
        fighter["recommended_picks"][2] = "ability_score_improvement"
        fighter["recommended_picks"][4] = "ability_score_improvement"
        fighter["recommended_picks"][8] = "ability_score_improvement"
        assert not any("twice" in e for e in build_errors(data, fighter))

    def test_catches_extra_attack_before_fifth(self, data):
        oath = copy.deepcopy(next(p for p in data["presets"] if p["id"] == "oathsworn"))
        oath["recommended_picks"][4] = "extra_attack"
        oath["recommended_picks"][5] = "ability_score_improvement"
        assert any("needs level 5" in e for e in build_errors(data, oath))


CHAPTERS = {
    "body": DATA.parents[1] / "03_Facet_of_the_Body.md",
    "mind": DATA.parents[1] / "04_Facet_of_the_Mind.md",
    "soul": DATA.parents[1] / "05_Facet_of_the_Soul.md",
}


def chapter(facet: str) -> str:
    return CHAPTERS[facet].read_text(encoding="utf-8")


class TestChaptersMatchData:
    @pytest.mark.parametrize("facet", FACETS)
    def test_every_menu_talent_has_an_entry(self, data, facet):
        text = chapter(facet)
        for t in data["talents"]:
            if facet in t["facets"]:
                assert f"**{t['name']}** *(tier {t['tier']}" in text, (facet, t["name"])

    @pytest.mark.parametrize("facet", FACETS)
    def test_origin_flag_matches_entry(self, data, facet):
        text = chapter(facet)
        for t in data["talents"]:
            if facet in t["facets"]:
                flagged = f"**{t['name']}** *(tier {t['tier']}, origin)*" in text
                assert flagged == t["origin"], (facet, t["name"])

    @pytest.mark.parametrize("facet", FACETS)
    def test_no_entry_for_talents_off_the_menu(self, data, facet):
        text = chapter(facet)
        for t in data["talents"]:
            if facet not in t["facets"]:
                assert f"**{t['name']}** *(tier" not in text, (facet, t["name"])

    @pytest.mark.parametrize("facet", FACETS)
    def test_every_signature_has_an_entry(self, data, facet):
        text = chapter(facet)
        for s in data["signatures"]:
            if s["facet"] == facet:
                assert f"\n**{s['name']}**\n" in text, s["name"]

    @pytest.mark.parametrize("facet", FACETS)
    def test_every_preset_has_a_card(self, data, facet):
        text = chapter(facet)
        for p in data["presets"]:
            if p["facet"] == facet:
                assert f"\n### {p['name']}\n" in text, p["name"]

    @pytest.mark.parametrize("facet", FACETS)
    def test_facet_feature_named(self, data, facet):
        assert f"### {data['facets'][facet]['feature']['name']}" in chapter(facet)

    @pytest.mark.parametrize("facet", FACETS)
    def test_card_level1_and_signature_match(self, data, facet):
        text = chapter(facet)
        talents = talents_by_id(data)
        sigs = {s["id"]: s["name"] for s in data["signatures"]}
        for p in data["presets"]:
            if p["facet"] != facet:
                continue
            card = text.split(f"\n### {p['name']}\n", 1)[1].split("\n---", 1)[0]
            line = next(l for l in card.splitlines() if l.startswith("**Level 1:**"))
            for tid in p["level1_talents"]:
                assert f"*{talents[tid]['name']}*" in line, (p["id"], tid)
            assert f"**Signature:** *{sigs[p['signature']]}*" in card, p["id"]
            assert f"origin talent *{talents[p['origin_talent']]['name']}*" in card, p["id"]

    @pytest.mark.parametrize("facet", FACETS)
    def test_card_picks_match(self, data, facet):
        text = chapter(facet)
        talents = talents_by_id(data)
        for p in data["presets"]:
            if p["facet"] != facet:
                continue
            card = text.split(f"\n### {p['name']}\n", 1)[1].split("\n---", 1)[0]
            picks = next(l for l in card.splitlines() if l.startswith("**Picks:**"))
            later = next(l for l in card.splitlines() if l.startswith("**Later:**"))
            for level in range(2, 6):
                tid, _ = normalise_pick(p["recommended_picks"][level])
                assert talents[tid]["name"] in picks, (p["id"], level, tid)
            pos = 0
            for level in range(6, 11):
                tid, _ = normalise_pick(p["recommended_picks"][level])
                found = later.find(talents[tid]["name"], pos)
                assert found >= 0, (p["id"], level, tid)
                pos = found + 1

    @pytest.mark.parametrize("facet", FACETS)
    def test_attribution_present(self, facet):
        assert "System Reference Document 5.2.1" in chapter(facet)
        assert "creativecommons.org/licenses/by/4.0" in chapter(facet)

    @pytest.mark.parametrize("facet", FACETS)
    def test_never_gm_or_dm(self, facet):
        import re
        assert not re.search(r"\b(GM|DM|Game Master|Dungeon Master)\b", chapter(facet))


def test_half_caster_math_is_ceil_half():
    # DESIGN §2: a half caster reads the Half table at ceil(level / 2).
    assert [math.ceil(l / 2) for l in range(1, 11)] == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]


class TestCasterPresetsUnaffectedByRulingA:
    """Planner ruling (a): full-caster slots count from the level the tradition talent
    was taken. Every caster preset takes it at 1st, so the §6 balance table stands."""

    def test_caster_presets_take_tradition_at_first(self, data):
        for p in data["presets"]:
            picks = [normalise_pick(v)[0] for v in p["recommended_picks"].values()]
            late = TRADITION_TALENTS & set(picks)
            assert not late, (p["id"], late)

    def test_non_caster_presets_never_take_a_tradition(self, data):
        for p in data["presets"]:
            if TRADITION_TALENTS & set(p["level1_talents"]):
                continue
            build = {tid for _, tid, _ in preset_build(p)}
            assert not (TRADITION_TALENTS & build), p["id"]

    def test_tradition_summaries_say_caster_level(self, talents):
        for tid in TRADITION_TALENTS:
            assert "caster level" in talents[tid]["summary"], tid


class TestMenuTablePrerequisites:
    """Each chapter's talent-menu table prints the same prerequisite as the yaml."""

    @staticmethod
    def rows(facet: str) -> dict:
        out = {}
        for line in chapter(facet).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 4 and cells[0] in {"1", "2", "3"}:
                name = cells[1].split(" (")[0]
                out[name] = cells[2]
        return out

    @pytest.mark.parametrize("facet", FACETS)
    def test_table_prereq_matches_yaml(self, data, talents, facet):
        rows = self.rows(facet)
        for t in data["talents"]:
            if facet not in t["facets"]:
                continue
            want = " or ".join(talents[p]["name"] for p in prereqs(t)) or "—"
            assert rows[t["name"]] == want, (facet, t["name"], rows[t["name"]], want)

    @pytest.mark.parametrize("facet", FACETS)
    def test_entry_prereq_line_matches_yaml(self, data, talents, facet):
        text = chapter(facet)
        for t in data["talents"]:
            if facet not in t["facets"]:
                continue
            entry = text.split(f"**{t['name']}** *(tier", 1)[1].split("\n**", 2)
            has_line = len(entry) > 1 and entry[1].startswith("Prerequisite:")
            assert has_line == bool(prereqs(t)), (facet, t["name"])


class TestDominanceAudit:
    """docs/RESEARCH_facets_d20_dominance.md: the fixes for dominant, dominated and
    dip-abuse talents stay fixed."""

    def test_aura_of_resolve_is_the_protector_capstone(self, talents):
        # Every Soul preset took it when it had no prerequisite.
        assert talents["aura_of_resolve"]["prereq"] == "interpose"

    def test_aura_of_resolve_not_universal_among_soul_presets(self, data):
        soul = [p for p in data["presets"] if p["facet"] == "soul"]
        takers = [p["id"] for p in soul
                  if "aura_of_resolve" in {tid for _, tid, _ in preset_build(p)}]
        assert 0 < len(takers) < len(soul), takers

    def test_sworn_strike_uses_scale_with_soul_modifier(self, talents):
        # Proficiency-bonus uses made it a must-take cross-Facet dip for Body.
        s = talents["sworn_strike"]["summary"]
        assert "Soul modifier" in s and "proficiency bonus" not in s
        assert "your Soul modifier (minimum 1)" in chapter("soul")

    def test_radiant_strikes_once_per_turn(self, talents):
        assert talents["radiant_strikes"]["summary"].startswith("Once on each of your turns")

    def test_anticipate_has_no_daily_limit(self, talents):
        # With a daily limit it was strictly worse than Glimpses (Soul T1).
        s = talents["anticipate"]["summary"]
        assert "per long rest" not in s and "No limit" in s
        entry = chapter("mind").split("**Anticipate** *(tier 2)*", 1)[1].split("\n**", 1)[0]
        assert "long rest" not in entry

    def test_unarmored_defense_constitution_rider(self, talents):
        assert "advantage on Dex saves" in talents["unarmored_defense"]["summary"]
        assert "advantage on Dexterity saving throws" in chapter("body")

    def test_potent_cantrips_summary_matches_chapter(self, talents):
        assert "one of its damage rolls" in talents["potent_cantrips"]["summary"]
