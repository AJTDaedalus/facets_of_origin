"""Facets d20 v0.2 data integrity: facets, tracks, talents, knacks, backgrounds, presets.

Contract: docs/DESIGN_facets_d20_v0_2.md (§1 schema, §3 chassis, §4 talents). Data:
facets_d20/data/facets_d20.yaml. These tests check the data is well-formed and obeys the
build rules as *data* (ids resolve, effect types are in the contract, presets respect the
advancement and cross-Facet rules). Computed rules — HP, attack bonus, save DC, slots,
damage, legality through the engine, the balance band — are tested through the engine in
test_facets_d20_engine.py (ruling 6). Chapter-agreement tests were retired with v0.1:
chapters 01–10 are rewritten from the DESIGN in the prose pass and get tests back then.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "facets_d20" / "data" / "facets_d20.yaml"
SPELLS = REPO / "facets_d20" / "data" / "facets_d20_spells.yaml"
DESIGN = REPO / "docs" / "DESIGN_facets_d20_v0_2.md"

FACETS = ("body", "mind", "soul")
STANDARD_ARRAY = [8, 10, 12, 13, 14, 15]
ABILITIES = ("str", "dex", "con", "int", "wis", "cha")

# Ruling 5: these v0.1 talents mirrored non-SRD material and must not come back by id.
RETIRED_IDS = {"tough", "deadeye", "bulwark", "cleaving_blow", "ambush", "beast_heart",
               "thaumaturgy", "invocation",          # Amendment 2 / V23: casting is a rank
               "infuse_item", "clockwork_companion", "fighting_style", "survivor",
               "font_of_life", "glimpses", "twist_of_fate", "well_timed_word",
               "martial_training", "magic_initiate", "ability_score_improvement"}


# ---------------------------------------------------------------- fixtures

@pytest.fixture(scope="module")
def data():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def spells():
    return yaml.safe_load(SPELLS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def talents(data):
    return {t["id"]: t for t in data["talents"]}


@pytest.fixture(scope="module")
def knacks(data):
    return {k["id"]: k for k in data["knacks"]}


@pytest.fixture(scope="module")
def contract():
    """Effect types, non-combat types and condition keywords named in DESIGN §1."""
    text = DESIGN.read_text(encoding="utf-8")
    sec = text[text.index("## 1. Data schema"):text.index("\n## 2.")]
    types, noncombat = set(), set()
    for line in sec.splitlines():
        m = re.match(r"^\| `([a-z_]+)`", line)
        if m:
            types.add(m.group(1))
            if "(N)" in line or r"(N\*)" in line:
                noncombat.add(m.group(1))
    words = set(re.findall(r"`([a-z_]+)`", sec))
    return {"types": types, "noncombat": noncombat, "words": words}


def all_effects(entry):
    for e in entry.get("effects", []) or []:
        yield e
    for lvl_effects in (entry.get("scaling") or {}).values():
        for e in lvl_effects:
            yield e


def everything_with_effects(data):
    for f in data["facets"].values():
        yield from f["features"]
    for name, tr in data["tracks"].items():
        if isinstance(tr, dict) and "ranks" in tr:
            yield from tr["ranks"]
    yield from data["talents"]
    yield from data["knacks"]
    yield from data.get("edges") or []          # Amendment 5


def menu(data, facet):
    return {t["id"] for t in data["talents"] if facet in t["menus"]}


def domain_tradition(spells):
    return {d["id"]: d["tradition"] for d in spells["domains"]}


# ---------------------------------------------------------------- shape

class TestTop:
    def test_version(self, data):
        assert str(data["version"]) == "0.2"

    def test_levels_and_pb(self, data):
        assert data["levels"] == {"min": 1, "max": 10}
        assert data["proficiency_bonus"] == {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4}

    def test_build_rules(self, data):
        br = data["build_rules"]
        assert br["cross_facet_talent_cap"] == 2
        assert br["one_tradition"] is True
        assert br["rider_limit_per_turn"] == 1
        assert br["controlled_creature_limit"] == 1


class TestAdvancement:
    """Ruling 1: a level-up is one choice at most, and some levels are zero choices."""

    def test_five_talents(self, data):
        assert data["advancement"]["talent_levels"] == [1, 3, 5, 7, 9]

    def test_choice_levels_disjoint(self, data):
        a = data["advancement"]
        t, k, s = set(a["talent_levels"]), set(a["knack_levels"]), set(a["asi_levels"])
        assert not (t & k or t & s or k & s)

    def test_at_most_one_choice_per_level_up(self, data):
        a = data["advancement"]
        for lvl in range(2, 11):
            choices = (lvl in a["talent_levels"]) + (lvl in a["knack_levels"])
            assert choices <= 1, lvl

    def test_asi_is_a_choice_v21(self, data):
        # V21 (owner): at 4th and 8th, +2 to one ability, +1 to two, or one extra knack.
        assert data["advancement"]["asi_rule"] == "choice"

    def test_every_level_up_is_at_most_one_choice(self, data):
        # Amendment 5 amends the budget: an even level adds an edge beside its one pick
        # (test_facets_d20_edges.py); the talent/knack/ability pick stays one per level.
        a = data["advancement"]
        for lvl in range(2, 11):
            picks = sum(lvl in a[k] for k in ("talent_levels", "knack_levels", "asi_levels"))
            assert picks <= 1, lvl
            assert (lvl in a.get("edge_levels", [])) == (lvl % 2 == 0), lvl


class TestFacetsAndTracks:
    """Amendment 2: no paths; tracks bought with talent picks (DESIGN §1.2, §3.2)."""

    def test_three_facets(self, data):
        assert tuple(data["facets"]) == FACETS

    def test_hit_dice(self, data):
        assert {f: data["facets"][f]["hit_die"] for f in FACETS} == {"body": 10, "mind": 6, "soul": 8}

    def test_no_paths_anywhere(self, data):
        assert "paths" not in data
        assert not any("paths" in f for f in data["facets"].values())
        assert not any("requires_path" in t or "path" in t for t in data["talents"])
        for b in data["presets"] + data["sim_builds"]:
            assert "path" not in b, b["id"]

    def test_traditions(self, data):
        assert data["facets"]["body"]["tradition"] is None          # E3
        assert data["facets"]["mind"]["tradition"] == "thaumaturgy"
        assert data["facets"]["soul"]["tradition"] == "invocation"

    def test_two_tracks_three_ranks_each(self, data):
        tr = data["tracks"]
        for t in ("steel", "spell"):
            assert sorted({r["depth"] for r in tr[t]["ranks"]}) == [1, 2, 3], t
            for r in tr[t]["ranks"]:
                assert isinstance(r["main"], bool), r["id"]
                # only depth-1 ranks may apply off the main track
                if r["depth"] > 1:
                    assert r["main"] is True, r["id"]

    def test_depth_gates_the_upgrades(self, data):
        assert data["tracks"]["scaling_depth"] == {5: 2, 9: 3}

    def test_main_track_rule(self, data):
        # Playtest fix pass V43: a tie keeps the main track you had.
        assert data["tracks"]["main_track"] == {"rule": "more_talents", "tie": "existing"}
        assert data["tracks"]["facet_weight"] == {"body": {"steel": 2}}      # E3 / V27

    def test_first_spell_talent_is_half_second_is_full(self, data):
        cast = {r["depth"]: e["progression"] for r in data["tracks"]["spell"]["ranks"]
                for e in r["effects"] if e["type"] == "casting"}
        assert cast == {1: "half", 2: "full"}
        first = [r for r in data["tracks"]["spell"]["ranks"] if r["depth"] == 1]
        assert all(r["main"] is False for r in first)   # a hybrid still casts (Half)

    def test_deep_magic_is_the_only_prismatic_door(self, data):
        prism = [(r["depth"], r["main"]) for r in data["tracks"]["spell"]["ranks"]
                 for e in r["effects"] if e["type"] == "domains" and e.get("prismatic")]
        assert prism == [(3, True)]

    def test_extra_attack_is_steel_depth_two_from_fifth(self, data):
        ea = [r for r in data["tracks"]["steel"]["ranks"]
              if any(e["type"] == "extra_attack" for e in r["effects"])]
        assert len(ea) == 1 and ea[0]["depth"] == 2 and ea[0]["level"] == 5 and ea[0]["main"]

    def test_off_main_steel_gives_weapons_only(self, data):
        # V26: a caster's Steel pick brings martial weapons, not armor or a hit die.
        off = [e["type"] for r in data["tracks"]["steel"]["ranks"] if not r["main"]
               for e in r["effects"]]
        assert off == ["weapon_proficiency"]

    def test_martial_training_steps_mind_and_soul_only(self, data):
        mt = next(r for r in data["tracks"]["steel"]["ranks"] if r["id"] == "martial_training")
        hd = [e for e in mt["effects"] if e["type"] == "hit_die_step"]
        assert hd and hd[0]["facets"] == ["mind", "soul"]
        arm = next(e for e in mt["effects"] if e["type"] == "armor_proficiency")
        assert arm["categories"] == {"body": [], "mind": ["medium", "shields"], "soul": ["heavy"]}

    def test_veteran_bonus_is_not_a_rider(self, data):
        vet = next(r for r in data["tracks"]["steel"]["ranks"] if r["depth"] == 3)
        assert not any(e.get("rider") for e in vet["effects"])

    def test_two_skill_picks_everywhere(self, data):
        for f in FACETS:
            fa = data["facets"][f]
            assert fa["skill_picks"] == 2 and len(fa["skills"]) >= 6

    def test_each_facet_has_a_first_level_feature(self, data):
        for f in FACETS:
            assert any(x["level"] == 1 for x in data["facets"][f]["features"]), f

    def test_extra_attack_is_not_a_facet_feature(self, data):
        for f in FACETS:
            assert not any(e["type"] == "extra_attack" for x in data["facets"][f]["features"]
                           for e in all_effects(x)), f


class TestIds:
    def test_unique_across_talents_knacks_features(self, data):
        ids = [t["id"] for t in data["talents"]] + [k["id"] for k in data["knacks"]]
        ids += [x["id"] for f in data["facets"].values() for x in f["features"]]
        ids += [r["id"] for t in ("steel", "spell") for r in data["tracks"][t]["ranks"]]
        assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]

    def test_snake_case(self, data):
        for e in everything_with_effects(data):
            assert re.fullmatch(r"[a-z][a-z0-9_]*", e["id"]), e["id"]

    def test_retired_ids_gone(self, data):
        ids = {t["id"] for t in data["talents"]} | {k["id"] for k in data["knacks"]}
        assert not ids & RETIRED_IDS


class TestEffectsFollowContract:
    def test_every_effect_type_is_in_design(self, data, contract):
        for entry in everything_with_effects(data):
            for e in all_effects(entry):
                assert e["type"] in contract["types"], (entry["id"], e["type"])

    def test_condition_keywords_are_in_design(self, data, contract):
        for entry in everything_with_effects(data):
            for e in all_effects(entry):
                for key in ("condition", "condition_any", "condition_target"):
                    for word in e.get(key) or []:
                        assert word in contract["words"], (entry["id"], word)

    def test_knacks_use_noncombat_types_only(self, data, contract):
        for k in data["knacks"]:
            for e in all_effects(k):
                assert e["type"] in contract["noncombat"] | {"advantage"}, (k["id"], e["type"])
                if e["type"] == "advantage":
                    assert e["roll"] == ["check"], k["id"]

    def test_no_boolean_keys(self, data):
        # PyYAML reads a bare `on:` key as True; the schema uses `roll:` (DESIGN §1.4a).
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    assert not isinstance(k, bool), x
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(data)

    def test_scaling_levels_in_range(self, data):
        for entry in everything_with_effects(data):
            for lvl in (entry.get("scaling") or {}):
                assert 2 <= int(lvl) <= 10, entry["id"]

    def test_every_resource_reference_is_declared(self, data):
        for entry in everything_with_effects(data):
            declared = {e["id"] for e in all_effects(entry) if e["type"] == "resource"}
            for e in all_effects(entry):
                ref = e.get("resource")
                if ref and e["type"] not in ("resource", "resource_refill") and ref not in ("focus",):
                    assert ref in declared, (entry["id"], ref)


class TestTalents:
    def test_required_fields(self, data):
        for t in data["talents"]:
            for key in ("id", "name", "menus", "track", "requires", "basis", "summary", "effects"):
                assert key in t, (t["id"], key)

    def test_menus_are_facets(self, data):
        for t in data["talents"]:
            assert t["menus"] and set(t["menus"]) <= set(FACETS), t["id"]

    def test_track_tags(self, data):
        for t in data["talents"]:
            assert t["track"] in (None, "steel", "spell"), t["id"]

    def test_no_gates(self, data):
        # Amendment 2: no talent requires a path, a Facet, casting or another talent.
        for t in data["talents"]:
            assert t["requires"] is None, t["id"]

    def test_casting_lives_in_the_tracks(self, data):
        # V23: no talent carries a casting effect; the first Spell talent casts (Half).
        for t in data["talents"]:
            assert not any(e["type"] == "casting" for e in all_effects(t)), t["id"]

    def test_body_menu_has_no_spell_talents(self, data):
        # Canon (E3): Body has no tradition; it casts only through cross-Facet picks.
        for t in data["talents"]:
            if "body" in t["menus"]:
                assert t["track"] != "spell", t["id"]

    def test_every_facet_has_a_steel_talent_of_its_own(self, data):
        # V30: a Mind or Soul martial needs no cross pick to open the Steel track.
        for f in FACETS:
            assert any(t["track"] == "steel" for t in data["talents"] if f in t["menus"]), f

    def test_mind_and_soul_can_reach_deep_magic_on_their_own_menu(self, data):
        for f in ("mind", "soul"):
            assert sum(t["track"] == "spell" for t in data["talents"] if f in t["menus"]) >= 3, f

    def test_tracked_growth_lives_in_scaling(self, data):
        # §1.2 step 6: a tracked talent's growth must sit in `scaling` so the depth gate covers it.
        for t in data["talents"]:
            if t["track"]:
                for e in all_effects(t):
                    assert not e.get("by_level"), t["id"]

    def test_menu_sizes(self, data):
        for f in FACETS:
            assert 8 <= len(menu(data, f)) <= 13, f

    def test_shared_talents_printed_once(self, data):
        names = [t["name"] for t in data["talents"]]
        assert len(names) == len(set(names))

    def test_riders_are_once_per_turn(self, data):
        for t in data["talents"]:
            for e in all_effects(t):
                if e.get("rider"):
                    assert e["frequency"] == "once_per_turn", t["id"]

    def test_weapon_riders_are_steel_talents(self, data):
        # V24: resource-paid weapon damage is bought in the Steel track, never with slots.
        for t in data["talents"]:
            if any(e.get("rider") for e in all_effects(t)):
                assert t["track"] == "steel", t["id"]

    def test_basis_names_no_non_srd_source(self, data):
        banned = ("Tough", "Sharpshooter", "Sentinel", "Great Weapon Master", "Healer feat",
                  "Assassin", "Circle of the Moon", "Artificer", "Dueling", "Protection style")
        for t in data["talents"] + data["knacks"]:
            assert not any(b in t["basis"] for b in banned), t["id"]


class TestKnacksAndBackgrounds:
    def test_knack_list(self, data):
        assert 10 <= len(data["knacks"]) <= 16

    def test_backgrounds_shape(self, data, knacks):
        for b in data["backgrounds"]:
            assert len(b["abilities"]) == 3 and set(b["abilities"]) <= set(ABILITIES), b["id"]
            assert len(b["skills"]) == 2, b["id"]
            assert b["knack"] in knacks, b["id"]


# ---------------------------------------------------------------- builds as data
# Legality is a rule, so it is checked by the engine (facets_d20.build.check), not by a
# second copy of the rules here (audit T1/T8; CLAUDE.md "never a second rules copy").
# What stays here is data consistency: a build's declared `cross` list matches the menus.

def declared_cross_problems(data, b):
    own = menu(data, b["facet"])
    cross = [tid for tid in b["talents"].values() if tid not in own]
    if sorted(cross) != sorted(b.get("cross", [])):
        return [f"cross list {cross} vs declared {b.get('cross', [])}"]
    return []


def engine_errors(b, level=10):
    import sys
    sys.path.insert(0, str(REPO / "software"))
    from facets_d20 import build as B
    from facets_d20 import data as D
    rs = D.load()
    return B.check(rs, B.Picks.from_entry(rs, b, level))


@pytest.fixture(scope="module")
def all_builds(data):
    presets = {p["id"]: p for p in data["presets"]}
    out = list(data["presets"])
    for s in data["sim_builds"]:
        out.append(presets[s["preset"]] if "preset" in s else s)
    return out


def depths(talents, b, level=10):
    """Tag counts (data, not a rule: the engine decides what they buy)."""
    d = {"steel": 0, "spell": 0}
    for lvl, tid in b["talents"].items():
        if int(lvl) <= level and talents[tid]["track"]:
            d[talents[tid]["track"]] += 1
    return d


class TestPresets:
    def test_twelve_four_per_facet(self, data):
        for f in FACETS:
            assert sum(p["facet"] == f for p in data["presets"]) == 4, f

    def test_required_names(self, data):
        soul = {p["name"] for p in data["presets"] if p["facet"] == "soul"}
        assert {"Priest", "Druid", "Oracle"} <= soul

    def test_mind_and_soul_offer_casters_and_warriors(self, data, talents):
        # Amendment 2: each has a pure caster and a build whose main line is Steel.
        for f in ("mind", "soul"):
            shapes = {tuple(sorted(depths(talents, p).items())) for p in data["presets"] if p["facet"] == f}
            assert any(d["spell"] >= 3 and d["steel"] == 0 for d in map(dict, shapes)), f
            assert any(d["steel"] >= d["spell"] and d["steel"] >= 1 for d in map(dict, shapes)), f

    def test_oathsworn_is_the_natural_hybrid(self, data, talents):
        o = next(p for p in data["presets"] if p["id"] == "oathsworn")
        d = depths(talents, o)
        assert d["steel"] == 2 and d["spell"] == 1

    def test_abilities_are_array_plus_background(self, data):
        bgs = {b["id"]: b for b in data["backgrounds"]}
        for p in data["presets"]:
            base = dict(p["abilities"])
            for a in bgs[p["background"]]["abilities"]:
                base[a] -= 1
            assert sorted(base.values()) == STANDARD_ARRAY, p["id"]

    def test_skills(self, data):
        bgs = {b["id"]: b for b in data["backgrounds"]}
        for p in data["presets"]:
            facet = data["facets"][p["facet"]]
            assert len(p["skills"]) == facet["skill_picks"], p["id"]
            assert set(p["skills"]) <= set(facet["skills"]), p["id"]
            assert not set(p["skills"]) & set(bgs[p["background"]]["skills"]), p["id"]

    def test_knacks(self, data, knacks):
        bgs = {b["id"]: b for b in data["backgrounds"]}
        for p in data["presets"]:
            assert sorted(int(k) for k in p["knacks"]) == data["advancement"]["knack_levels"], p["id"]
            chosen = list(p["knacks"].values()) + [bgs[p["background"]]["knack"]]
            assert all(k in knacks for k in chosen), p["id"]
            assert len(chosen) == len(set(chosen)), p["id"]

    def test_kit(self, data):
        for p in data["presets"]:
            assert p["kit"]["weapons"], p["id"]


class TestBuildsAreLegalData:
    def test_every_preset_and_sim_build_is_legal(self, data, all_builds):
        for b in all_builds:
            for level in (1, 4, 7, 10):
                assert engine_errors(b, level) == [], (b["id"], level)

    def test_declared_cross_lists_match_the_menus(self, data, all_builds):
        for b in all_builds:
            assert declared_cross_problems(data, b) == [], b["id"]

    def test_sim_builds_name_their_audit(self, data):
        for s in data["sim_builds"]:
            assert s.get("audit"), s["id"]

    def test_checker_catches_a_domain_of_the_other_tradition(self, data):
        bad = {"id": "x", "facet": "mind", "domain": "presence",
               "abilities": {"str": 8, "dex": 14, "con": 14, "int": 16, "wis": 13, "cha": 10},
               "talents": {1: "evoker", 3: "iron_mind", 5: "hardy", 7: "alert", 9: "anticipate"},
               "kit": {"weapons": ["quarterstaff"]}}
        assert engine_errors(bad)

    def test_checker_catches_third_cross_pick(self, data):
        bad = {"id": "x", "facet": "body",
               "abilities": {"str": 16, "dex": 13, "con": 15, "int": 8, "wis": 13, "cha": 10},
               "talents": {1: "anticipate", 3: "iron_mind", 5: "warden", 7: "hardy", 9: "alert"},
               "kit": {"weapons": ["longsword"]}}
        assert any("cap is 2" in e for e in engine_errors(bad))


class TestDomainsAsData:
    """Where each build's domains come from (§1.5): the first Spell talent, Wider Study,
    Deep Magic. Prismatic only as Deep Magic's (§5.1, provisional option (a))."""

    def test_prismatic_only_as_deep_domain(self, data, spells, all_builds):
        prism = {d["id"] for d in spells["domains"] if d["prismatic"]}
        for b in all_builds:
            assert b.get("domain") not in prism, b["id"]
            assert not set((b.get("extra_domains") or {}).values()) & prism, b["id"]

    def test_deep_domain_only_with_three_spell_talents(self, data, talents, all_builds):
        for b in all_builds:
            if b.get("deep_domain"):
                assert depths(talents, b)["spell"] >= 3, b["id"]

    def test_extra_domains_match_wider_study(self, data, all_builds):
        for b in all_builds:
            ws = [int(l) for l, t in b["talents"].items() if t == "wider_study"]
            assert sorted(int(l) for l in (b.get("extra_domains") or {})) == ws, b["id"]

    def test_casters_name_a_domain_and_non_casters_none(self, data, talents, all_builds):
        for b in all_builds:
            if depths(talents, b)["spell"]:
                assert b.get("domain"), b["id"]
            else:
                assert not b.get("domain") and not b.get("extra_domains"), b["id"]

    def test_body_casters_name_a_tradition(self, data, talents, all_builds):
        for b in all_builds:
            if b["facet"] == "body" and depths(talents, b)["spell"]:
                assert b.get("tradition") in ("invocation", "thaumaturgy"), b["id"]

    def test_the_oracle_gets_fate_from_deep_magic(self, data):
        o = next(p for p in data["presets"] if p["id"] == "oracle")
        assert o["domain"] != "fate" and o["deep_domain"] == "fate"


class TestBalanceAndEncounterSpec:
    def test_band(self, data):
        b = data["balance"]
        assert b["levels"] == [1, 4, 7, 10] and b["band_pct"] == 15
        assert set(b["reference_party"]) <= {p["id"] for p in data["presets"]}

    def test_roles_cover_every_facet(self, data):
        # Amendment 2: pure caster, pure martial and hybrids for each Facet (§8 item 7).
        roles = data["balance"]["roles"]
        known = {p["id"] for p in data["presets"]} | {s["id"] for s in data["sim_builds"]}
        assert set(roles) == set(FACETS)
        for f, r in roles.items():
            for key in ("pure_martial", "pure_caster", "hybrids"):
                assert r[key] and set(r[key]) <= known, (f, key)

    def test_audit_combos_are_hybrids(self, data):
        hybrids = {b for r in data["balance"]["roles"].values() for b in r["hybrids"]}
        assert {"battle_priest", "battle_priest_deep", "paladin_max", "spellblade"} <= hybrids

    def test_sim_build_roles_match(self, data):
        listed = {}
        for f, r in data["balance"]["roles"].items():
            for key, role in (("pure_martial", "pure_martial"), ("pure_caster", "pure_caster"),
                              ("hybrids", "hybrid")):
                for b in r[key]:
                    listed[b] = role
        for s in data["sim_builds"]:
            if s["id"] in listed:
                assert s.get("role") == listed[s["id"]], s["id"]

    def test_hybrid_rule(self, data):
        assert data["balance"]["hybrid_rule"] == {"from_level": 4, "swap_tolerance_pct": 3,
                                                  "pi_tolerance_pct": 15, "job_tolerance_pct": 5}

    def test_primary_measure_is_the_swap_test(self, data):
        # Balance pass V32: the swap test is the band's primary measure, PI secondary.
        assert data["balance"]["measure"] == "swap"

    def test_adventuring_day(self, data):
        # Balance pass V34: three Clashes, a short rest after the first and the second.
        assert data["adventuring_day"] == {"clashes": 3, "short_rests_after": [1, 2]}

    def test_four_named_tiers(self, data):
        assert [t["id"] for t in data["encounter_tiers"]] == ["skirmish", "clash", "battle", "desperate"]

    def test_baseline_party(self, data):
        assert data["encounter_baseline"]["party_size"] == 4
        assert data["encounter_baseline"]["level"] == 4
