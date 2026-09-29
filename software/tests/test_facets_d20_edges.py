"""Facets d20 edges (BRIEF Amendment 5; DESIGN v0.2 §1.3b, §1.4b, §3.6; V50–V56).

An edge is a small combat or utility pick at 2nd, 4th, 6th, 8th and 10th, beside that
level's knack or ability pick. These tests hold the data to the contract (a shared list,
flavour tags, nothing a talent or rank already gives, one mechanic per job), the engine to
the rules (edges never count toward depth; the checker enforces the slots), and the
simulator to each edge's effect with scripted dice. Nothing here re-implements a rule.
"""
from __future__ import annotations

import random
from fractions import Fraction

import pytest
import yaml

from facets_d20 import build as B
from facets_d20 import combat
from facets_d20 import data as D
from facets_d20 import sim as S
from facets_d20.combat import MonsterAttack, RuleOptions
from facets_d20.dice import Dice

DATA = D.RULES_FILE


class Script:
    """A fake RNG that returns scripted die faces in order (and checks the range)."""

    def __init__(self, faces):
        self.faces = list(faces)

    def randint(self, a, b):
        assert self.faces, "script ran out of dice"
        v = self.faces.pop(0)
        assert a <= v <= b, f"scripted face {v} outside {a}..{b}"
        return v

    def random(self):
        return 0.5

    def choice(self, seq):
        return seq[0]

    def shuffle(self, seq):
        return None


@pytest.fixture(scope="module")
def data():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def rs():
    return D.load()


@pytest.fixture(scope="module")
def edges(data):
    return {e["id"]: e for e in data["edges"]}


def picks(rs, bid, level, **changes):
    entry = rs.presets.get(bid) or rs.sim_builds[bid]
    p = B.Picks.from_entry(rs, entry, level)
    for k, v in changes.items():
        setattr(p, k, v)
    return p


# ================================================================ data

RANK_JOBS = {"casting", "domains", "weapon_proficiency", "armor_proficiency", "hit_die_step",
             "hp_per_level", "extra_attack", "crit_range", "attack_bonus", "ac_bonus",
             "ac_formula", "spark", "reroll", "extra_damage_dice"}


class TestEdgeData:
    def test_edges_come_at_the_even_levels(self, data):
        assert data["advancement"]["edge_levels"] == [2, 4, 6, 8, 10]

    def test_even_levels_two_small_picks_odd_levels_one(self, data):
        # Amendment 5 item 3: an even-level level-up is two small picks; odd levels one.
        a = data["advancement"]
        for lvl in range(2, 11):
            big = sum(lvl in a[k] for k in ("talent_levels", "knack_levels", "asi_levels"))
            edge = lvl in a["edge_levels"]
            assert big == 1, lvl
            assert (big + edge) == (2 if lvl % 2 == 0 else 1), lvl
            if edge:
                assert lvl not in a["talent_levels"], lvl

    def test_about_thirty_edges_in_one_shared_list(self, data):
        assert 24 <= len(data["edges"]) <= 36
        for e in data["edges"]:
            assert "menus" not in e, e["id"]

    def test_required_fields(self, data):
        for e in data["edges"]:
            for key in ("id", "name", "tag", "basis", "summary", "effects"):
                assert key in e, (e["id"], key)
            assert "scaling" not in e, e["id"]

    def test_tags_are_flavour_and_every_tag_is_used(self, data):
        tags = [e["tag"] for e in data["edges"]]
        assert set(tags) == {"steel", "spell", "general"}
        for t in ("steel", "spell", "general"):
            assert tags.count(t) >= 6, t

    def test_edges_carry_no_track(self, data):
        for e in data["edges"]:
            assert "track" not in e, e["id"]

    def test_ids_unique_across_talents_knacks_edges(self, data):
        ids = [x["id"] for x in data["talents"] + data["knacks"] + data["edges"]]
        assert len(ids) == len(set(ids))

    def test_no_edge_does_a_talent_or_rank_job(self, data):
        for e in data["edges"]:
            for eff in e["effects"]:
                assert eff["type"] not in RANK_JOBS, (e["id"], eff["type"])
                assert not eff.get("rider"), e["id"]

    def test_no_edge_copies_a_talent_effect(self, data):
        def sig(eff):
            roll = eff.get("roll")
            return (eff["type"], eff.get("trigger"), tuple(roll) if isinstance(roll, list) else roll,
                    str(eff.get("scope")), tuple(eff.get("damage_types") or ()),
                    tuple(eff.get("condition") or ()))
        taken = set()
        for t in data["talents"]:
            for eff in list(t["effects"]) + [x for v in (t.get("scaling") or {}).values() for x in v]:
                taken.add(sig(eff))
        for tr in ("steel", "spell"):
            for r in data["tracks"][tr]["ranks"]:
                taken |= {sig(eff) for eff in r["effects"]}
        for e in data["edges"]:
            for eff in e["effects"]:
                if eff["type"] in ("narrative", "resource"):
                    continue
                assert sig(eff) not in taken, (e["id"], sig(eff))

    def test_min_levels_are_few_and_even(self, data):
        mins = {e["id"]: e["min_level"] for e in data["edges"] if e.get("min_level")}
        assert 1 <= len(mins) <= 5
        assert all(m in (4, 6, 8, 10) for m in mins.values()), mins

    def test_basis_names_no_non_srd_feat(self, data):
        banned = ("War Caster", "Sentinel", "Mobile", "Observant", "Resilient", "Tough",
                  "Defensive Duelist", "Shield Master", "Polearm", "Inspiring Leader",
                  "Spell Sniper", "Sharpshooter", "Great Weapon Master", "Ritual Caster",
                  "Crusher", "Slasher", "Piercer", "Dual Wielder", "Heavy Armor Master")
        for e in data["edges"]:
            assert not any(b in e["basis"] for b in banned), e["id"]

    def test_every_preset_and_sim_build_names_an_edge_at_each_even_level(self, data, edges):
        for entry in data["presets"] + data["sim_builds"]:
            if entry.get("preset"):
                continue
            got = entry.get("edges")
            assert got is not None, entry["id"]
            assert sorted(got) == [2, 4, 6, 8, 10], entry["id"]
            assert len(set(got.values())) == 5, entry["id"]
            for lvl, eid in got.items():
                assert eid in edges, (entry["id"], eid)
                assert lvl >= (edges[eid].get("min_level") or 2), (entry["id"], eid)

    def test_every_edge_is_shown_on_some_build(self, data, edges):
        used = {e for x in data["presets"] + data["sim_builds"] for e in (x.get("edges") or {}).values()}
        unused = set(edges) - used
        assert len(unused) <= 3, sorted(unused)


# ================================================================ engine: build and check


class TestEdgesInTheBuild:
    def test_edges_never_count_toward_depth_or_main_track(self, rs):
        # The Wizard with five Steel-tagged edges is still Spell 3 and Spell main.
        steel = [eid for eid, e in rs.edges.items() if e["tag"] == "steel"][:5]
        p = picks(rs, "wizard", 10, edges={2: steel[0], 4: steel[1], 6: steel[2], 8: steel[3],
                                            10: steel[4]})
        base = picks(rs, "wizard", 10)
        assert B.track_depth(rs, p) == B.track_depth(rs, base) == {"spell": 3}
        assert B.picks_main_track(rs, p) == "spell"
        assert B.track_ranks(rs, p) == B.track_ranks(rs, base)
        assert B.build(rs, p).progression == "full"

    def test_edge_effects_join_from_the_level_taken(self, rs):
        assert "sap" not in B.build(rs, picks(rs, "fighter", 1)).features
        ch = B.build(rs, picks(rs, "fighter", 2))
        assert "sap" in ch.features
        assert any(src == "sap" and e["type"] == "impose_disadvantage" for src, e in ch.effects)

    def test_from_entry_reads_edges_up_to_the_level(self, rs):
        assert picks(rs, "priest", 5).edges == {2: "far_casting", 4: "steady_focus"}
        assert picks(rs, "priest", 1).edges == {}

    def test_srd_baselines_have_no_edges(self):
        srd = D.load_baselines()
        pid = next(iter(srd.presets))
        p = B.Picks.from_preset(srd, pid, 10)
        assert not p.edges
        assert B.check(srd, p) == []

    def test_missing_edge_is_an_error(self, rs):
        p = picks(rs, "fighter", 4, edges={2: "sap"})
        assert any("L4: no edge chosen" in e for e in B.check(rs, p))

    def test_edge_on_an_odd_level_is_an_error(self, rs):
        p = picks(rs, "fighter", 4, edges={2: "parry", 3: "sap", 4: "drive_back"})
        assert any("L3: no edge pick at this level" in e for e in B.check(rs, p))

    def test_unknown_edge_and_a_talent_as_an_edge(self, rs):
        errs = B.check(rs, picks(rs, "fighter", 2, edges={2: "nope"}))
        assert any("'nope' is not an edge" in e for e in errs)
        errs = B.check(rs, picks(rs, "fighter", 2, edges={2: "hardy"}))
        assert any("it is a talent" in e for e in errs)

    def test_edge_taken_twice(self, rs):
        errs = B.check(rs, picks(rs, "fighter", 4, edges={2: "parry", 4: "parry"}))
        assert any("edge parry taken twice" in e for e in errs)

    def test_edge_below_its_minimum_level(self, rs):
        errs = B.check(rs, picks(rs, "wizard", 4, edges={2: "steady_focus", 4: "ritual_scholar"}))
        assert any("steady_focus needs level 4" in e for e in errs)
        assert B.check(rs, picks(rs, "wizard", 4, edges={2: "ritual_scholar", 4: "steady_focus"})) == []

    def test_edge_above_character_level(self, rs):
        errs = B.check(rs, picks(rs, "fighter", 2, edges={2: "parry", 4: "sap"}))
        assert any("L4: edge chosen above character level 2" in e for e in errs)

    def test_retraining_an_edge_changes_nothing_else(self, rs):
        a = B.build(rs, picks(rs, "fighter", 6))
        b = B.build(rs, picks(rs, "fighter", 6, edges={2: "quick_draw", 4: "drive_back", 6: "sap"}))
        assert (a.hp, a.ac, a.weapon.to_hit, a.hit_die) == (b.hp, b.ac, b.weapon.to_hit, b.hit_die)


# ================================================================ engine: each simulated edge


def with_edge(rs, bid, level, eid, slot=2):
    p = picks(rs, bid, level)
    e = dict(p.edges)
    for k, v in list(e.items()):
        if v == eid:
            return p
    e[slot] = eid
    p.edges = e
    return p


def _fight(profile, faces, *, ac=10, attacks=()):
    from facets_d20.monsters import MonsterBlock
    block = MonsterBlock("dummy", "Dummy", Fraction(0), ac, 10_000, tuple(attacks),
                         {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0},
                         morale="never", source="engine")
    f = S.Fight(Script(faces), [profile], S.Encounter.of(S.FoeSpec(block)), RuleOptions(), 1.0)
    return f, f.pcs[0], f.foes[0]


class TestHeavyHands:
    def test_two_handed_melee_dice_floor_at_three(self, rs):
        ch = B.build(rs, picks(rs, "barbarian", 2))
        assert ch.weapon.name == "greataxe" and ch.weapon.min_face == 3

    def test_not_one_handed_with_a_shield(self, rs):
        ch = B.build(rs, with_edge(rs, "fighter", 2, "heavy_hands"))
        assert ch.weapon.name == "longsword" and ch.weapon.min_face == 1

    def test_versatile_two_handed_counts(self, rs):
        p = with_edge(rs, "fighter", 2, "heavy_hands")
        p.kit = dict(p.kit, shield=False, weapons=["longsword"])
        assert B.build(rs, p).weapon.min_face == 3

    def test_the_floor_reaches_the_damage_roll(self, rs):
        prof = B.build(rs, picks(rs, "barbarian", 2)).profile()
        f, me, foe = _fight(prof, [])
        f.rng = Script([15, 1])                    # hit; greataxe d12 shows 1 → counts 3
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn={})
        assert f.damage_by_pc[me.id] == 3 + prof.weapon.mod


class TestGraze:
    def _prof(self, rs):
        return B.build(rs, picks(rs, "barbarian", 6)).profile()

    def test_profile(self, rs):
        assert self._prof(rs).graze == 4          # Strength 16, +2 at 4th = 18 → +4

    def test_a_miss_still_deals_strength(self, rs):
        prof = self._prof(rs)
        f, me, foe = _fight(prof, [], ac=30)
        f.rng = Script([2])                        # a miss (no Spark: none held)
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn={})
        assert f.damage_by_pc[me.id] == prof.graze

    def test_once_per_turn(self, rs):
        prof = self._prof(rs)
        f, me, foe = _fight(prof, [], ac=30)
        f.rng = Script([2, 3])
        turn = {}
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn=turn)
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn=turn)
        assert f.damage_by_pc[me.id] == prof.graze

    def test_nothing_without_the_edge(self, rs):
        prof = B.build(rs, picks(rs, "barbarian", 4)).profile()
        assert prof.graze == 0


class TestSap:
    def test_profile(self, rs):
        assert B.build(rs, picks(rs, "fighter", 2)).profile().sap
        assert not B.build(rs, picks(rs, "fighter", 1)).profile().sap

    def test_a_hit_saps_the_target_and_its_next_attack_has_disadvantage(self, rs):
        prof = B.build(rs, picks(rs, "fighter", 6)).profile()
        atk = MonsterAttack("Strike", 5, 7)
        f, me, foe = _fight(prof, [], attacks=[atk])
        f.rng = Script([15, 4])                     # hit, longsword d8 = 4
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn={})
        assert "sapped" in foe.conditions
        # the foe attacks: two d20s (disadvantage), 19 and 3 → 3 + 5 = 8 misses AC 20
        f.rng = Script([19, 3])
        f.foe_attack(foe, me, atk)
        assert me.hp == me.max_hp and "sapped" not in foe.conditions

    def test_sap_ends_at_the_start_of_your_next_turn(self, rs):
        prof = B.build(rs, picks(rs, "fighter", 6)).profile()
        f, me, foe = _fight(prof, [])
        f.rng = Script([15, 4])
        f.weapon_attack(me, foe, prof.weapon, attack_action=True, turn={})
        f.clear_sap(me)
        assert "sapped" not in foe.conditions


class TestParry:
    """Parry: +2 AC against one melee hit, a melee weapon in hand and no shield."""

    def _prof(self, rs, level=4):
        return B.build(rs, picks(rs, "rogue", level)).profile()      # rapier, leather, no shield

    def test_profile(self, rs):
        assert self._prof(rs).parry == 2
        assert self._prof(rs, 2).parry == 0                         # taken at 4th

    def test_not_with_a_shield(self, rs):
        ch = B.build(rs, with_edge(rs, "fighter", 2, "parry"))
        assert ch.shield and ch.profile().parry == 0

    def test_turns_a_near_hit_into_a_miss_with_the_reaction(self, rs):
        prof = self._prof(rs)
        assert prof.ac == 15
        atk = MonsterAttack("Strike", 5, 7)
        f, me, foe = _fight(prof, [], attacks=[atk])
        f.rng = Script([11])                        # 11 + 5 = 16 vs AC 15: a hit; +2 → miss
        f.foe_attack(foe, me, atk)
        assert me.hp == me.max_hp and not me.reaction_available

    def test_a_clear_hit_still_lands_and_the_reaction_is_spent(self, rs):
        # Hidden AC (V46): the player hears "hit" and parries without knowing the margin.
        prof = self._prof(rs)
        atk = MonsterAttack("Strike", 5, 7)
        f, me, foe = _fight(prof, [], attacks=[atk])
        f.rng = Script([13])                        # 18: beats AC 17 too
        f.foe_attack(foe, me, atk)
        assert me.hp == me.max_hp - 7 and not me.reaction_available

    def test_a_crit_is_not_parried(self, rs):
        prof = self._prof(rs)
        atk = MonsterAttack("Strike", 5, 7)
        f, me, foe = _fight(prof, [], attacks=[atk])
        f.rng = Script([20])
        f.foe_attack(foe, me, atk)
        assert me.hp == me.max_hp - 14 and me.reaction_available

    def test_needs_a_melee_weapon_in_hand(self, rs):
        p = picks(rs, "rogue", 5)
        p.kit = dict(p.kit, weapons=["shortbow"])
        assert B.build(rs, p).profile().parry == 0


class TestDieHard:
    def test_death_save_with_advantage_takes_the_higher(self):
        c = combat.Combatant(id="p", name="p", side="party", max_hp=10, ac=10, role="pc", hp=0,
                             state="down")
        combat.death_save(Script([4, 12]), c, advantage=True)
        assert (c.death_successes, c.death_failures) == (1, 0)

    def test_without_advantage_one_die(self):
        c = combat.Combatant(id="p", name="p", side="party", max_hp=10, ac=10, role="pc", hp=0,
                             state="down")
        combat.death_save(Script([4]), c)
        assert (c.death_successes, c.death_failures) == (0, 1)

    def test_a_twenty_on_either_die_revives(self):
        c = combat.Combatant(id="p", name="p", side="party", max_hp=10, ac=10, role="pc", hp=0,
                             state="down")
        assert combat.death_save(Script([3, 20]), c, advantage=True) == "active"
        assert c.hp == 1

    def test_profile_and_sim_roll_with_advantage(self, rs):
        prof = B.build(rs, picks(rs, "fighter", 8)).profile()
        assert prof.death_save_advantage
        f, me, foe = _fight(prof, [])
        me.hp, me.state = 0, "down"
        f.rng = Script([2, 11])
        f.pc_turn(me)
        assert me.death_successes == 1


class TestSecondBreath:
    def test_profile(self, rs):
        assert B.build(rs, picks(rs, "rogue", 8)).profile().second_breath == 8

    def test_first_bloodied_gives_temp_hp_once(self, rs):
        prof = B.build(rs, picks(rs, "rogue", 8)).profile()
        f, me, foe = _fight(prof, [])
        half = me.max_hp // 2
        f.hurt_pc(me, me.max_hp - half)             # now Bloodied, standing
        assert me.temp_hp == 8
        f.hurt_pc(me, 8)                            # the temp HP soak it
        f.hurt_pc(me, 1)
        assert me.temp_hp == 0

    def test_not_when_dropped(self, rs):
        prof = B.build(rs, picks(rs, "rogue", 8)).profile()
        f, me, foe = _fight(prof, [])
        f.hurt_pc(me, me.max_hp)
        assert me.temp_hp == 0


class TestHale:
    def test_profile(self, rs):
        assert B.build(rs, picks(rs, "tinker", 10)).profile().hd_max
        assert not B.build(rs, picks(rs, "tinker", 8)).profile().hd_max

    def test_hit_dice_restore_the_maximum(self, rs):
        prof = B.build(rs, picks(rs, "tinker", 10)).profile()
        d = S._DayPC(prof)
        con = (prof.abilities["con"] - 10) // 2
        d.hp = prof.hp - (prof.hit_die + con)
        d.short_rest(Script([]), hd_bonus=0)        # no die is rolled
        assert d.hp == prof.hp and d.hd == prof.level - 1

    def test_without_hale_the_die_is_rolled(self, rs):
        prof = B.build(rs, picks(rs, "tinker", 8)).profile()
        d = S._DayPC(prof)
        d.hp = prof.hp - 20
        d.short_rest(Script([1] * 10), hd_bonus=0)
        assert d.hp < prof.hp


class TestHardened:
    def test_poison_resistance(self, rs):
        assert "poison" in B.build(rs, picks(rs, "barbarian", 8)).profile().resist
        assert "poison" not in B.build(rs, picks(rs, "barbarian", 6)).profile().resist


class TestPiercingSpell:
    def test_profile_and_pool(self, rs):
        prof = B.build(rs, picks(rs, "wizard", 6)).profile()
        assert prof.piercing is not None and prof.piercing.uses == 1
        assert S.pools(prof)["piercing"].recharge == "short"

    def test_first_save_spell_target_rolls_with_disadvantage(self, rs):
        prof = B.build(rs, picks(rs, "wizard", 6)).profile()
        f, me, foe = _fight(prof, [])
        st = f.state[me.id]
        st.piercing = 1
        assert f.save_disadvantage(me) is True
        assert st.piercing == 0
        assert f.save_disadvantage(me) is False

    def test_no_edge_no_disadvantage(self, rs):
        prof = B.build(rs, picks(rs, "wizard", 4)).profile()
        f, me, foe = _fight(prof, [])
        assert prof.piercing is None and f.save_disadvantage(me) is False


class TestSteadyFocus:
    def test_profile(self, rs):
        assert B.build(rs, picks(rs, "wizard", 4)).profile().steady_focus
        assert not B.build(rs, picks(rs, "wizard", 2)).profile().steady_focus

    def test_a_failed_concentration_save_is_kept_with_the_reaction(self, rs):
        prof = B.build(rs, picks(rs, "wizard", 4)).profile()
        f, me, foe = _fight(prof, [])
        me.concentrating = "Web"
        f.rng = Script([1])                         # the Con save fails
        f.hurt_pc(me, 4)
        assert me.concentrating == "Web" and not me.reaction_available

    def test_without_a_reaction_it_is_lost(self, rs):
        prof = B.build(rs, picks(rs, "wizard", 4)).profile()
        f, me, foe = _fight(prof, [])
        me.concentrating = "Web"
        me.reaction_available = False
        f.rng = Script([1])
        f.hurt_pc(me, 4)
        assert me.concentrating is None


class TestUnsimulatedEdgesChangeNothing:
    def test_narrative_edges_leave_the_profile_alone(self, rs):
        base = B.build(rs, picks(rs, "fighter", 4, edges={2: "quick_draw", 4: "drive_back"})).profile()
        for eid, e in rs.edges.items():
            if all(x["type"] in ("narrative", "resource", "spells_known")
                   or (x["type"] == "advantage" and set(x["roll"]) <= {"check", "save"})
                   for x in e["effects"]) and not e.get("min_level"):
                p = picks(rs, "fighter", 4, edges={2: "quick_draw", 4: eid}) if eid != "quick_draw" \
                    else picks(rs, "fighter", 4, edges={2: "drive_back", 4: eid})
                prof = B.build(rs, p).profile()
                for k in ("hp", "ac", "parry", "sap", "graze", "second_breath", "hd_max",
                          "steady_focus", "death_save_advantage", "piercing", "resist", "riders"):
                    assert getattr(prof, k) == getattr(base, k), (eid, k)


# ================================================================ V56: stabilizing needs no check


class TestStabilizeV56:
    def _down(self):
        return combat.Combatant(id="p", name="p", side="party", max_hp=10, ac=10, role="pc",
                                hp=0, state="down", death_failures=2)

    def test_the_rule_is_no_check(self):
        assert RuleOptions().stabilize == "auto"
        c = self._down()
        assert combat.stabilize(Script([]), c, check=False)
        assert c.state == "stable" and c.death_failures == 0

    def test_the_srd_check_can_fail(self):
        c = self._down()
        assert not combat.stabilize(Script([7]), c, bonus=2)      # 9 < DC 10
        assert c.state == "down"
        assert combat.stabilize(Script([8]), c, bonus=2)          # 10
        assert c.state == "stable"

    def test_only_a_dying_creature(self):
        c = self._down()
        c.state = "active"
        assert not combat.stabilize(Script([]), c, check=False)

    def test_the_sim_stabilizes_a_friend_at_two_failures(self, rs):
        party = [B.build(rs, picks(rs, "fighter", 4)).profile(),
                 B.build(rs, picks(rs, "rogue", 4)).profile()]
        from facets_d20.monsters import MonsterBlock
        block = MonsterBlock("dummy", "Dummy", Fraction(0), 10, 10_000, (),
                             {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0},
                             morale="never", source="engine")
        f = S.Fight(random.Random(1), party, S.Encounter.of(S.FoeSpec(block)), RuleOptions(), 1.0)
        f.setup()
        fighter, rogue = f.pcs
        rogue.hp, rogue.state, rogue.death_failures = 0, "down", 1
        f.take_action(fighter, {})
        assert rogue.state == "down"                              # one failure: keep fighting
        rogue.death_failures = 2
        f.take_action(fighter, {})
        assert rogue.state == "stable"
