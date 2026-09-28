"""Facets d20 rules engine — direct rule tests (BRIEF Amendment 1, ruling 6).

Every test here drives `software/facets_d20/`, the single source of Facets d20 rule
logic. Nothing in this file re-implements a rule: expected values are hand-derived
numbers written into the test, and the engine has to produce them.

Scripted dice: `Script([...])` hands out the listed die faces in order, so a rule can be
tested against an exact roll instead of a distribution.
"""
from __future__ import annotations

import random

import pytest

from facets_d20 import combat, dice
from facets_d20.combat import Combatant, RuleOptions
from facets_d20.dice import Dice


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


def pc(**kw) -> Combatant:
    base = dict(id="pc", name="PC", side="party", max_hp=20, ac=15, role="pc",
                saves={"str": 0, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0})
    base.update(kw)
    return Combatant(**base)


def foe(**kw) -> Combatant:
    base = dict(id="foe", name="Foe", side="enemy", max_hp=20, ac=13, role="standard",
                saves={"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0})
    base.update(kw)
    return Combatant(**base)


# ================================================================ dice


class TestDice:
    def test_parse_plain(self):
        assert Dice.parse("2d6") == Dice(2, 6)

    def test_parse_rejects_garbage(self):
        with pytest.raises(ValueError):
            Dice.parse("two dee six")

    def test_parse_zero_dice_rejected(self):
        with pytest.raises(ValueError):
            Dice.parse("0d6")

    def test_average(self):
        assert Dice(2, 6).average == 7.0
        assert Dice(1, 8).average == 4.5

    def test_roll_sums_faces(self):
        assert dice.roll(Script([3, 5]), Dice(2, 6)) == 8

    def test_roll_min_face_great_weapon(self):
        # Great Weapon style: a 1 or 2 on a damage die counts as a 3.
        assert dice.roll(Script([1, 2]), Dice(2, 6), min_face=3) == 6

    def test_d20_straight(self):
        r = dice.d20(Script([11]))
        assert r.natural == 11 and r.rolls == (11,)

    def test_d20_advantage_takes_higher(self):
        assert dice.d20(Script([4, 17]), advantage=True).natural == 17

    def test_d20_disadvantage_takes_lower(self):
        assert dice.d20(Script([4, 17]), disadvantage=True).natural == 4

    def test_d20_advantage_and_disadvantage_cancel(self):
        r = dice.d20(Script([9]), advantage=True, disadvantage=True)
        assert r.rolls == (9,)

    def test_advantage_math_seeded(self):
        # P(at least one 11+ on 2d20) = 1 - 0.5^2 = 0.75.
        rng = random.Random(7)
        n = 20000
        hits = sum(dice.d20(rng, advantage=True).natural >= 11 for _ in range(n))
        assert abs(hits / n - 0.75) < 0.015

    def test_disadvantage_math_seeded(self):
        rng = random.Random(8)
        n = 20000
        hits = sum(dice.d20(rng, disadvantage=True).natural >= 11 for _ in range(n))
        assert abs(hits / n - 0.25) < 0.015


# ================================================================ attacks and damage


class TestAttackRoll:
    def test_hit_on_meeting_ac(self):
        r = combat.attack_roll(Script([10]), bonus=5, ac=15)
        assert r.hit and not r.crit and r.total == 15

    def test_miss_below_ac(self):
        assert not combat.attack_roll(Script([9]), bonus=5, ac=15).hit

    def test_natural_20_always_hits_and_crits(self):
        r = combat.attack_roll(Script([20]), bonus=-5, ac=30)
        assert r.hit and r.crit

    def test_natural_1_always_misses(self):
        assert not combat.attack_roll(Script([1]), bonus=30, ac=10).hit

    def test_expanded_crit_range(self):
        r = combat.attack_roll(Script([19]), bonus=0, ac=25, crit_min=19)
        assert r.hit and r.crit

    def test_advantage_uses_higher_die(self):
        r = combat.attack_roll(Script([3, 18]), bonus=0, ac=15, advantage=True)
        assert r.hit and r.natural == 18

    def test_hit_chance_expected(self):
        # +5 vs AC 15 hits on 10+: 55%.
        assert combat.hit_chance(5, 15) == pytest.approx(0.55)

    def test_hit_chance_clamped(self):
        assert combat.hit_chance(30, 10) == pytest.approx(0.95)
        assert combat.hit_chance(-10, 30) == pytest.approx(0.05)


class TestDamage:
    def test_pc_damage_rolls_dice_plus_mod(self):
        assert combat.roll_damage(Script([6]), Dice(1, 8), 3) == 9

    def test_crit_doubles_dice_not_modifier(self):
        # 1d8+3 crit = 2d8+3.
        assert combat.roll_damage(Script([6, 2]), Dice(1, 8), 3, crit=True) == 11

    def test_damage_never_negative(self):
        assert combat.roll_damage(Script([1]), Dice(1, 4), -3) == 0

    def test_monster_fixed_damage_uses_no_dice(self):
        atk = combat.MonsterAttack(name="club", to_hit=3, fixed=4, dice=Dice(1, 6), mod=1)
        assert combat.monster_damage(Script([]), atk, crit=False) == 4

    def test_monster_crit_rolls_double_dice_plus_mod(self):
        atk = combat.MonsterAttack(name="club", to_hit=3, fixed=4, dice=Dice(1, 6), mod=1)
        assert combat.monster_damage(Script([6, 5]), atk, crit=True) == 12

    def test_monster_crit_doubles_extra_dice_too(self):
        # Young Red Dragon Rend: 2d6+6 plus 1d6 fire; a crit rolls 4d6 + 2d6 + 6.
        atk = combat.MonsterAttack(name="Rend", to_hit=10, fixed=16, dice=Dice(2, 6), mod=6,
                                   extra=(Dice(1, 6),))
        assert combat.monster_damage(Script([1, 2, 3, 4, 5, 6]), atk, crit=True) == 27

    def test_monster_attack_without_dice_crits_to_double_fixed(self):
        atk = combat.MonsterAttack(name="slam", to_hit=3, fixed=5, dice=None, mod=0)
        assert combat.monster_damage(Script([]), atk, crit=True) == 10


# ================================================================ taking damage


class TestApplyDamage:
    def test_hp_drops(self):
        c = foe()
        combat.apply_damage(Script([]), c, 5)
        assert c.hp == 15

    def test_temp_hp_absorbs_first(self):
        c = pc(temp_hp=4)
        combat.apply_damage(Script([]), c, 6)
        assert c.temp_hp == 0 and c.hp == 18

    def test_resistance_halves_round_down(self):
        c = foe(resist={"slashing"})
        combat.apply_damage(Script([]), c, 7, dtype="slashing")
        assert c.hp == 17

    def test_bloodied_at_half(self):
        c = foe()
        out = combat.apply_damage(Script([]), c, 10)
        assert out.became_bloodied and combat.is_bloodied(c)

    def test_not_bloodied_above_half(self):
        c = foe()
        out = combat.apply_damage(Script([]), c, 9)
        assert not out.became_bloodied and not combat.is_bloodied(c)

    def test_bloodied_reported_once(self):
        c = foe()
        combat.apply_damage(Script([]), c, 10)
        out = combat.apply_damage(Script([]), c, 2)
        assert not out.became_bloodied

    def test_minion_dies_to_any_damage(self):
        c = foe(role="minion", max_hp=1)
        out = combat.apply_damage(Script([]), c, 1)
        assert out.killed and c.state == "dead"

    def test_minion_zero_damage_survives(self):
        c = foe(role="minion", max_hp=1)
        out = combat.apply_damage(Script([]), c, 0)
        assert not out.killed and c.state == "active"

    def test_monster_at_zero_is_dead(self):
        c = foe()
        out = combat.apply_damage(Script([]), c, 25)
        assert out.killed and c.hp == 0 and c.state == "dead"

    def test_pc_at_zero_falls_unconscious(self):
        c = pc()
        out = combat.apply_damage(Script([]), c, 20)
        assert out.dropped and c.state == "down" and c.hp == 0

    def test_massive_damage_kills_pc(self):
        c = pc(max_hp=10)
        combat.apply_damage(Script([]), c, 20)  # 10 left over >= max HP
        assert c.state == "dead"

    def test_damage_at_zero_is_a_death_save_failure(self):
        c = pc()
        combat.apply_damage(Script([]), c, 20)
        combat.apply_damage(Script([]), c, 3)
        assert c.death_failures == 1

    def test_crit_at_zero_is_two_failures(self):
        c = pc()
        combat.apply_damage(Script([]), c, 20)
        combat.apply_damage(Script([]), c, 3, crit=True)
        assert c.death_failures == 2

    def test_concentration_dc_reported(self):
        c = pc(concentrating="spirit_guardians")
        out = combat.apply_damage(Script([]), c, 30 - 20 + 4)  # 14 damage
        assert out.concentration_dc == 10

    def test_concentration_dc_half_damage(self):
        c = pc(max_hp=60, concentrating="bless")
        out = combat.apply_damage(Script([]), c, 26)
        assert out.concentration_dc == 13


class TestSavesAndMinions:
    def test_save_success(self):
        assert combat.saving_throw(Script([12]), bonus=2, dc=14).success

    def test_save_failure(self):
        assert not combat.saving_throw(Script([11]), bonus=2, dc=14).success

    def test_save_for_half(self):
        assert combat.damage_after_save(foe(), 21, saved=True, half_on_save=True) == 10

    def test_save_negates(self):
        assert combat.damage_after_save(foe(), 21, saved=True, half_on_save=False) == 0

    def test_minion_takes_none_on_successful_save(self):
        assert combat.damage_after_save(foe(role="minion", max_hp=1), 21, saved=True,
                                        half_on_save=True) == 0

    def test_minion_takes_full_on_failed_save(self):
        assert combat.damage_after_save(foe(role="minion", max_hp=1), 21, saved=False,
                                        half_on_save=True) == 21

    def test_evasion_pc_success_takes_none(self):
        c = pc(evasion=True)
        assert combat.damage_after_save(c, 20, saved=True, half_on_save=True) == 0
        assert combat.damage_after_save(c, 20, saved=False, half_on_save=True) == 10


class TestConcentration:
    def test_keeps_on_success(self):
        c = pc(concentrating="bless")
        assert combat.concentration_check(Script([10]), c, dc=10)  # 10 + 2 con
        assert c.concentrating == "bless"

    def test_drops_on_failure(self):
        c = pc(concentrating="bless")
        assert not combat.concentration_check(Script([3]), c, dc=10)
        assert c.concentrating is None

    def test_down_ends_concentration(self):
        c = pc(concentrating="bless")
        combat.apply_damage(Script([]), c, 20)
        assert c.concentrating is None


# ================================================================ morale


class TestMorale:
    def test_fail_breaks(self):
        c = foe()
        assert combat.morale_check(Script([9]), c) is True
        assert c.state == "broken"

    def test_success_holds(self):
        c = foe()
        assert combat.morale_check(Script([10]), c) is False
        assert c.state == "active"

    def test_uses_wisdom_save(self):
        c = foe(saves={"wis": 3})
        assert combat.morale_check(Script([7]), c) is False

    def test_boss_never_checks(self):
        c = foe(role="boss")
        assert combat.morale_check(Script([]), c) is None

    def test_never_break_creature_exempt(self):
        c = foe(morale="never")
        assert combat.morale_check(Script([]), c) is None

    def test_triggers_on_first_bloodied(self):
        opts = RuleOptions()
        c = foe()
        out = combat.apply_damage(Script([]), c, 10)
        assert combat.morale_triggers(c, out, leader_fell=False, opts=opts)

    def test_no_trigger_when_unhurt(self):
        opts = RuleOptions()
        c = foe()
        out = combat.apply_damage(Script([]), c, 2)
        assert not combat.morale_triggers(c, out, leader_fell=False, opts=opts)

    def test_leader_falls_triggers_minions(self):
        assert combat.morale_triggers(foe(role="minion", max_hp=1), None, leader_fell=True,
                                      opts=RuleOptions(leader_morale="minions"))

    def test_leader_falls_only_minions_under_v02_option(self):
        assert not combat.morale_triggers(foe(), None, leader_fell=True,
                                          opts=RuleOptions(leader_morale="minions"))

    def test_leader_falls_everyone_under_v01_option(self):
        assert combat.morale_triggers(foe(), None, leader_fell=True,
                                      opts=RuleOptions(leader_morale="all"))


# ================================================================ initiative, turns, bosses


class TestInitiative:
    """DESIGN v0.2 §6.1: one d20 per side + the side's best modifier; ties to players."""

    def test_surprise_decides(self):
        assert combat.side_initiative(Script([]), [0], [5], surprised="enemy") == "party"
        assert combat.side_initiative(Script([]), [5], [0], surprised="party") == "enemy"

    def test_one_die_per_side_best_modifier(self):
        # Party rolls ONE d20 (8) + its best Dex (+3) = 11; MM rolls 10 + best (+0) = 10.
        assert combat.side_initiative(Script([8, 10]), [0, 3, 1], [0, -1]) == "party"

    def test_party_does_not_roll_per_player(self):
        # Only two dice are consumed however many players there are.
        rng = Script([5, 12])
        assert combat.side_initiative(rng, [0, 0, 0, 0], [0]) == "enemy"
        assert rng.faces == []

    def test_enemy_uses_best_modifier(self):
        assert combat.side_initiative(Script([10, 8]), [0], [-1, 3]) == "enemy"

    def test_tie_goes_to_players(self):
        assert combat.side_initiative(Script([10, 10]), [0], [0]) == "party"

    def test_alert_gives_the_party_roll_advantage(self):
        # Advantage: party rolls 4 and 15, keeps 15; MM rolls 12.
        assert combat.side_initiative(Script([4, 15, 12]), [0], [0], party_advantage=True) == "party"

    def test_equal_sides_first_move_about_half(self):
        rng = random.Random(11)
        n = 20000
        first = sum(combat.side_initiative(rng, [2, 2, 2, 2], [2]) == "party" for _ in range(n))
        assert abs(first / n - 0.525) < 0.015     # 21/40 with ties to players


class TestBossTurns:
    def test_boss_two_turns(self):
        assert combat.turns_per_phase(foe(role="boss")) == 2

    def test_standard_one_turn(self):
        assert combat.turns_per_phase(foe()) == 1

    def test_boss_resolve_turns_a_stun_into_one_lost_turn(self):
        b = foe(role="boss")
        assert combat.inflict(b, "stunned", round_no=1) == "resolve"
        assert "stunned" not in b.conditions
        assert [combat.begin_turn(b) for _ in range(2)] == [False, True]

    @pytest.mark.parametrize("cond", ["paralyzed", "incapacitated", "banished", "polymorphed",
                                      "asleep", "held"])
    def test_boss_resolve_covers_every_disabling_condition(self, cond):
        b = foe(role="boss")
        assert combat.inflict(b, cond, round_no=2) == "resolve"
        assert cond not in b.conditions

    def test_boss_loses_at_most_one_turn_a_round(self):
        b = foe(role="boss")
        combat.inflict(b, "stunned", round_no=3)
        assert combat.inflict(b, "paralyzed", round_no=3) == "resisted"
        assert [combat.begin_turn(b) for _ in range(2)] == [False, True]

    def test_boss_resolve_again_next_round(self):
        b = foe(role="boss")
        combat.inflict(b, "stunned", round_no=3)
        combat.begin_turn(b)
        assert combat.inflict(b, "stunned", round_no=4) == "resolve"

    def test_non_boss_takes_the_condition(self):
        c = foe()
        assert combat.inflict(c, "paralyzed", round_no=1) == "applied"
        assert "paralyzed" in c.conditions

    def test_boss_takes_non_disabling_condition(self):
        b = foe(role="boss")
        assert combat.inflict(b, "prone", round_no=1) == "applied"

    def test_stunned_standard_loses_its_turn(self):
        c = foe()
        c.conditions.add("stunned")
        assert combat.begin_turn(c) is False

    def test_enemy_phase_order_boss_top_of_round(self):
        order = combat.round_order("party", RuleOptions(boss_top_of_round=True),
                                   enemy_has_boss=True)
        assert order == ["boss", "party", "enemy"]

    def test_enemy_phase_order_v01(self):
        order = combat.round_order("party", RuleOptions(boss_top_of_round=False),
                                   enemy_has_boss=True)
        assert order == ["party", "enemy"]

    def test_enemy_first_order(self):
        assert combat.round_order("enemy", RuleOptions(), enemy_has_boss=False) == ["enemy", "party"]


class TestRecharge:
    def test_recharge_on_high_roll(self):
        c = foe()
        c.special_ready = False
        assert combat.roll_recharge(Script([5]), c, recharge_min=5) is True

    def test_no_recharge_on_low_roll(self):
        c = foe()
        c.special_ready = False
        assert combat.roll_recharge(Script([4]), c, recharge_min=5) is False

    def test_ready_special_rolls_nothing(self):
        c = foe()
        c.special_ready = True
        assert combat.roll_recharge(Script([]), c, recharge_min=5) is True


class TestReactions:
    def test_one_reaction_per_round(self):
        c = pc()
        assert combat.take_reaction(c)
        assert not combat.take_reaction(c)

    def test_reaction_returns_at_turn_start(self):
        c = pc()
        combat.take_reaction(c)
        combat.begin_turn(c)
        assert combat.take_reaction(c)

    def test_leaving_reach_provokes(self):
        assert combat.provokes_opportunity_attack(leaves_reach=True)

    def test_disengage_forced_or_teleport_does_not_provoke(self):
        assert not combat.provokes_opportunity_attack(leaves_reach=True, disengaged=True)
        assert not combat.provokes_opportunity_attack(leaves_reach=True, forced=True)
        assert not combat.provokes_opportunity_attack(leaves_reach=False)


class TestDeath:
    def _down(self):
        c = pc()
        combat.apply_damage(Script([]), c, 20)
        return c

    def test_success(self):
        c = self._down()
        combat.death_save(Script([10]), c)
        assert c.death_successes == 1

    def test_failure(self):
        c = self._down()
        combat.death_save(Script([9]), c)
        assert c.death_failures == 1

    def test_three_successes_stable(self):
        c = self._down()
        for _ in range(3):
            combat.death_save(Script([15]), c)
        assert c.state == "stable"

    def test_three_failures_dead(self):
        c = self._down()
        for _ in range(3):
            combat.death_save(Script([5]), c)
        assert c.state == "dead"

    def test_natural_1_two_failures(self):
        c = self._down()
        combat.death_save(Script([1]), c)
        assert c.death_failures == 2

    def test_natural_20_back_with_1(self):
        c = self._down()
        combat.death_save(Script([20]), c)
        assert c.hp == 1 and c.state == "active"

    def test_healing_wakes_and_resets(self):
        c = self._down()
        combat.death_save(Script([5]), c)
        combat.heal(c, 7)
        assert c.state == "active" and c.hp == 7 and c.death_failures == 0

    def test_heal_caps_at_max(self):
        c = pc()
        c.hp = 15
        combat.heal(c, 50)
        assert c.hp == 20

    def test_heal_does_not_raise_dead(self):
        c = pc()
        c.state = "dead"
        c.hp = 0
        combat.heal(c, 10)
        assert c.state == "dead" and c.hp == 0


# ================================================================ monsters (09 conversions)

from fractions import Fraction  # noqa: E402

from facets_d20 import monsters  # noqa: E402


class TestMonsterLibrary:
    @pytest.mark.parametrize("mid", ["bandit", "goblin_warrior", "brute", "ogre", "zombie",
                                     "owlbear", "young_red_dragon"])
    def test_library_has(self, mid):
        assert mid in monsters.LIBRARY

    def test_ladder_two_per_cr_from_eighth_to_twelve(self):
        from collections import Counter
        counts = Counter(m.cr for m in monsters.ladder())
        want = [Fraction(1, 8), Fraction(1, 4), Fraction(1, 2)] + [Fraction(n) for n in range(1, 13)]
        assert all(counts[c] >= 2 for c in want), counts

    def test_ladder_numbers_are_the_srd_printed_averages(self):
        # 09 worked conversions (checked against the SRD 5.2.1 PDF by the Planner).
        assert (monsters.get("bandit").ac, monsters.get("bandit").hp,
                monsters.get("bandit").damage_per_turn) == (12, 11, 4)
        assert monsters.get("goblin_warrior").damage_per_turn == 5   # conditional +1d4 excluded
        assert monsters.get("hell_hound").attacks[0].fixed == 10     # 7 (1d8+3) plus 3 (1d6)

    def test_ladder_mixes_ranged_and_casters(self):
        names = {m.name for m in monsters.ladder()}
        assert {"Scout", "Mage", "Priest", "Archmage"} <= names

    def test_mindless_never_break(self):
        assert monsters.get("skeleton").morale == "never"
        assert monsters.get("animated_armor").morale == "never"
        assert monsters.get("ogre").morale == "normal"

    def test_ogre_numbers_match_09(self):
        o = monsters.LIBRARY["ogre"]
        assert (o.ac, o.hp, o.damage_per_turn) == (11, 68, 13)

    def test_owlbear_multiattack_sums(self):
        assert monsters.LIBRARY["owlbear"].damage_per_turn == 28

    def test_young_red_dragon_matches_09(self):
        d = monsters.LIBRARY["young_red_dragon"]
        assert (d.ac, d.hp, d.damage_per_turn) == (18, 178, 48)
        breath = d.special
        assert breath.fixed == 56 and breath.save_dc == 17 and breath.recharge_min == 5

    def test_zombie_never_breaks(self):
        assert monsters.LIBRARY["zombie"].morale == "never"

    def test_unknown_monster(self):
        with pytest.raises(KeyError):
            monsters.get("tarrasque")


class TestConversion:
    def test_minion_has_one_hp(self):
        c = monsters.convert("bandit", role="minion")
        assert c.max_hp == 1 and c.role == "minion"

    def test_minion_keeps_fixed_damage(self):
        c = monsters.convert("bandit", role="minion")
        assert c.attacks[0].fixed == 4

    def test_standard_keeps_block_hp(self):
        assert monsters.convert("bandit").max_hp == 11

    def test_boss_role(self):
        c = monsters.convert("ogre", role="boss")
        assert c.role == "boss" and combat.turns_per_phase(c) == 2

    def test_bad_role(self):
        with pytest.raises(ValueError):
            monsters.convert("ogre", role="champion")

    def test_unique_ids(self):
        a = monsters.convert("bandit", uid="b1")
        b = monsters.convert("bandit", uid="b2")
        assert a.id != b.id

    def test_never_break_budget_hp(self):
        # 09: a foe that never breaks counts its HP x 1.25; a minion counts 7 (L1-4).
        assert monsters.budget_hp(monsters.convert("zombie"), party_level=2) == 18  # 15 * 1.25 = 18.75
        assert monsters.budget_hp(monsters.convert("bandit", role="minion"), party_level=2) == 7
        assert monsters.budget_hp(monsters.convert("bandit", role="minion"), party_level=5) == 10


class TestGenericTemplates:
    @pytest.mark.parametrize("cr", monsters.TEMPLATE_CRS)
    def test_template_exists(self, cr):
        t = monsters.template(cr)
        assert t.hp > 0 and t.ac >= 10 and t.damage_per_turn > 0

    def test_templates_grow_with_cr(self):
        lo, mid, hi = (monsters.template(c) for c in (Fraction(1, 8), 3, 10))
        assert lo.hp < mid.hp < hi.hp
        assert lo.damage_per_turn < mid.damage_per_turn < hi.damage_per_turn

    def test_template_is_the_ladder_median(self):
        # CR 5 ladder HPs: 90, 94, 105, 112, 67 -> median 94.
        assert monsters.template(5).hp == 94

    def test_template_unknown_cr(self):
        with pytest.raises(KeyError):
            monsters.template(30)


# ================================================================ build (schema v0.2, synthetic ruleset)

import copy  # noqa: E402

from facets_d20 import build as B  # noqa: E402
from facets_d20 import data as D  # noqa: E402

_PB = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4}
_FULL = {1: [2], 2: [3], 3: [4, 2], 4: [4, 3], 5: [4, 3, 2], 6: [4, 3, 3], 7: [4, 3, 3, 1],
         8: [4, 3, 3, 2], 9: [4, 3, 3, 3, 1], 10: [4, 3, 3, 3, 2]}
_HALF = {1: [2], 2: [2], 3: [3], 4: [3], 5: [4, 2], 6: [4, 2], 7: [4, 3], 8: [4, 3],
         9: [4, 3, 2], 10: [4, 3, 2]}

MINI = {
    "version": 0.2,
    "levels": {"min": 1, "max": 10},
    "proficiency_bonus": _PB,
    "advancement": {"talent_levels": [1, 3, 5, 7, 9], "knack_levels": [2, 6, 10],
                    "asi_levels": [4, 8], "asi_rule": "two_highest_plus_one"},
    "build_rules": {"cross_facet_talent_cap": 2, "one_tradition": True},
    "paths": {
        "steel": {"hit_die_step": 1, "applies_hit_die_step_to": ["mind", "soul"],
                  "weapons_add": ["martial"],
                  "armor_add": {"mind": ["medium", "shields"], "soul": ["heavy"], "body": []},
                  "features": [{"id": "extra_attack", "level": 5,
                                "effects": [{"type": "extra_attack", "attacks": 2}]}]},
        "spell": {"casting": {"progression": "full"}},
    },
    "facets": {
        "body": {"name": "Body", "hit_die": 10, "saves": ["str", "con"],
                 "armor": ["light", "medium", "heavy", "shields"],
                 "weapons": ["simple", "martial"], "paths": ["steel"], "tradition": None,
                 "features": [{"id": "second_wind", "level": 1, "effects": [
                     {"type": "resource", "id": "second_wind", "uses": 2, "recharge": "short"},
                     {"type": "heal", "amount": "1d10+level", "action": "bonus",
                      "targets": "self", "resource": "second_wind"}]}]},
        "mind": {"name": "Mind", "hit_die": 6, "saves": ["int", "wis"], "armor": ["light"],
                 "weapons": ["simple"], "paths": ["steel", "spell"],
                 "tradition": "thaumaturgy", "features": []},
        "soul": {"name": "Soul", "hit_die": 8, "saves": ["wis", "cha"],
                 "armor": ["light", "medium", "shields"], "weapons": ["simple"],
                 "paths": ["steel", "spell"], "tradition": "invocation", "features": []},
    },
    "talents": [
        {"id": "tough", "name": "Tough", "menus": ["body", "mind", "soul"],
         "effects": [{"type": "hp_per_level", "value": 2}]},
        {"id": "precision", "name": "Precision", "menus": ["body", "mind"],
         "requires_path": "steel",
         "effects": [{"type": "extra_damage_dice", "dice": "1d6", "rider": True,
                      "frequency": "once_per_turn",
                      "condition": ["advantage_or_ally_adjacent"]}],
         "scaling": {5: [{"type": "extra_damage_dice", "dice": "2d6", "rider": True,
                          "frequency": "once_per_turn",
                          "condition": ["advantage_or_ally_adjacent"]}],
                     9: [{"type": "extra_damage_dice", "dice": "3d6", "rider": True,
                          "frequency": "once_per_turn",
                          "condition": ["advantage_or_ally_adjacent"]}]}},
        {"id": "dueling", "name": "Dueling", "menus": ["body"],
         "effects": [{"type": "damage_bonus", "value": 2, "weapon": "melee",
                      "condition": "one_handed_melee"}]},
        {"id": "battle_casting", "name": "Battle Casting", "menus": ["soul"],
         "requires_path": "steel",
         "effects": [{"type": "casting", "tradition": "invocation", "progression": "half"}]},
        {"id": "warden", "name": "Warden", "menus": ["soul"], "requires": {"casting": "any"},
         "effects": [{"type": "heal_boost", "amount": "2+level"}]},
        {"id": "wider_study", "name": "Wider Study", "menus": ["mind", "soul"],
         "requires": {"casting": "any"}, "effects": [{"type": "domains", "count": 1}]},
        {"id": "grit", "name": "Grit", "menus": ["body"], "repeatable": True,
         "effects": [{"type": "hp_per_level", "value": 1}]},
        {"id": "resolve", "name": "Resolve", "menus": ["soul"], "repeatable": True,
         "effects": [{"type": "save_bonus", "value": 1, "targets": ["self"]}]},
        {"id": "defense", "name": "Defense", "menus": ["body"],
         "effects": [{"type": "ac_bonus", "value": 1, "condition": "armored"}]},
    ],
    "knacks": [
        {"id": "streetwise", "name": "Streetwise", "kind": "knack",
         "effects": [{"type": "narrative", "text": "knows the streets"}]},
        {"id": "linguist", "name": "Linguist", "kind": "knack",
         "effects": [{"type": "languages", "count": 2}]},
        {"id": "trivia", "name": "Trivia", "kind": "knack",
         "effects": [{"type": "narrative", "text": "knows things"}]},
        {"id": "healer_knack", "name": "Healer", "kind": "knack",
         "effects": [{"type": "skill_proficiency", "choose": 1, "from": ["medicine"]}]},
    ],
    "backgrounds": [{"id": "watch", "name": "Watch", "abilities": {"str": 2, "con": 1},
                     "skills": ["athletics"], "knack": "streetwise"}],
    "presets": [],
}
MINI_SPELLS = {
    "version": 0.2,
    "traditions": {"thaumaturgy": {"facet": "mind", "ability": ["int"]},
                   "invocation": {"facet": "soul", "ability": ["wis", "cha"]}},
    "common_list": [{"name": "Fire Bolt", "level": 0}, {"name": "Magic Missile", "level": 1},
                    {"name": "Fireball", "level": 3}],
    "casting": {"domains_on_path": 1},
    "full_table": _FULL, "half_table": _HALF,
    "domains": [
        {"id": "flame", "name": "Flame", "tradition": "thaumaturgy",
         "spells": [{"name": "Burning Hands", "level": 1}]},
        {"id": "the_tide", "name": "The Tide", "tradition": "invocation",
         "spells": [{"name": "Cure Wounds", "level": 1}, {"name": "Spirit Guardians", "level": 3},
                    {"name": "Sacred Flame", "level": 0}]},
        {"id": "presence", "name": "Presence", "tradition": "invocation",
         "spells": [{"name": "Bless", "level": 1}]},
    ],
}

ARRAY = {"str": 15, "dex": 12, "con": 14, "int": 8, "wis": 13, "cha": 10}


@pytest.fixture(scope="module")
def mini():
    return D.from_dicts(copy.deepcopy(MINI), copy.deepcopy(MINI_SPELLS))


def fighter(level, **kw):
    t = {1: "dueling", 3: "defense", 5: "tough", 7: "precision", 9: "grit"}
    base = dict(facet="body", path="steel", level=level,
                abilities={"str": 17, "dex": 12, "con": 15, "int": 8, "wis": 13, "cha": 10},
                background="watch", talents={k: v for k, v in t.items() if k <= level},
                knacks={k: v for k, v in {2: "linguist", 6: "healer_knack", 10: "trivia"}.items() if k <= level},
                kit={"armor": "chain_mail", "shield": True, "weapons": ["longsword"]})
    base.update(kw)
    return B.Picks(**base)


def priest(level, **kw):
    t = {1: "warden", 3: "wider_study", 5: "tough", 7: "resolve", 9: "resolve"}
    base = dict(facet="soul", path="spell", level=level,
                abilities={"str": 10, "dex": 12, "con": 14, "int": 8, "wis": 16, "cha": 13},
                talents={k: v for k, v in t.items() if k <= level},
                knacks={k: v for k, v in {2: "linguist", 6: "healer_knack", 10: "trivia"}.items() if k <= level},
                casting_ability="wis",
                domains=["the_tide", "presence"] if level >= 3 else ["the_tide"],
                kit={"armor": "scale_mail", "shield": True, "weapons": ["mace"]})
    base.update(kw)
    return B.Picks(**base)


class TestDataLoader:
    def test_mini_loads(self, mini):
        assert set(mini.facets) == {"body", "mind", "soul"}

    def test_version_must_be_0_2(self):
        raw = copy.deepcopy(MINI)
        raw["version"] = 0.1
        with pytest.raises(D.DataError, match="version 0.2"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_unknown_effect_type_is_load_error(self):
        raw = copy.deepcopy(MINI)
        raw["talents"][0]["effects"] = [{"type": "teleport_everything"}]
        with pytest.raises(D.DataError, match="unknown effect type"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_unknown_condition_is_load_error(self):
        raw = copy.deepcopy(MINI)
        raw["talents"][2]["effects"][0]["condition"] = "on_tuesdays"
        with pytest.raises(D.DataError, match="unknown condition"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_knack_with_combat_effect_is_load_error(self):
        raw = copy.deepcopy(MINI)
        raw["knacks"][0]["effects"] = [{"type": "attack_bonus", "value": 1}]
        with pytest.raises(D.DataError, match="non-combat"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_bad_expression_is_load_error(self):
        raw = copy.deepcopy(MINI)
        raw["talents"][0]["effects"][0]["value"] = "lots"
        with pytest.raises(D.DataError, match="unknown term"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_duplicate_id(self):
        raw = copy.deepcopy(MINI)
        raw["talents"].append(copy.deepcopy(raw["talents"][0]))
        with pytest.raises(D.DataError, match="duplicate"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_background_knack_must_exist(self):
        raw = copy.deepcopy(MINI)
        raw["backgrounds"][0]["knack"] = "nope"
        with pytest.raises(D.DataError, match="unknown knack"):
            D.from_dicts(raw, MINI_SPELLS)

    def test_unknown_sim_spell_model(self):
        sp = copy.deepcopy(MINI_SPELLS)
        sp["sim_spells"] = [{"name": "Wish", "model": "anything_goes"}]
        with pytest.raises(D.DataError, match="unknown model"):
            D.from_dicts(MINI, sp)


class TestExpressions:
    ctx = B.Ctx(level=5, pb=3, mods={"str": 3, "dex": 1, "con": 2, "int": 0, "wis": 4, "cha": -1},
                casting_mod=4, soul_mod=None)

    def test_int(self):
        assert B.eval_int(7, self.ctx) == 7

    def test_sum(self):
        assert B.eval_int("8+pb+wis", self.ctx) == 15

    def test_half_level(self):
        assert B.eval_int("half_level", self.ctx) == 2

    def test_soul_without_casting_is_higher_of_wis_cha(self):
        assert B.eval_int("soul", self.ctx) == 4

    def test_dice_amount(self):
        d, flat = B.eval_amount("1d10+level", self.ctx)
        assert d == Dice(1, 10) and flat == 5

    def test_min(self):
        assert B.eval_int("cha", self.ctx, minimum=1) == 1

    def test_unknown_term(self):
        with pytest.raises(D.DataError):
            B.eval_int("moxie", self.ctx)


class TestComputedNumbers:
    def test_body_level1_hp(self, mini):
        assert B.build(mini, fighter(1)).hp == 12          # d10 + Con 2

    def test_asi_raises_two_highest_and_con_is_retroactive(self, mini):
        ch = B.build(mini, fighter(4))
        assert ch.abilities["str"] == 18 and ch.abilities["con"] == 16
        assert ch.hp == 13 + 3 * (5 + 1 + 3)               # d10+3, then 3 x (6+3) = 40

    def test_asi_capped_at_20(self, mini):
        ch = B.build(mini, fighter(8, abilities={"str": 20, "dex": 12, "con": 15, "int": 8,
                                                 "wis": 13, "cha": 10}))
        assert ch.abilities["str"] == 20 and ch.abilities["con"] == 17 and ch.abilities["wis"] == 15

    def test_tough(self, mini):
        assert B.build(mini, fighter(5)).hp == 13 + 4 * 9 + 2 * 5   # 59

    def test_steel_path_steps_mind_hit_die(self, mini):
        p = B.Picks(facet="mind", path="steel", level=1, abilities=ARRAY,
                    talents={1: "precision"}, kit={"weapons": ["rapier"], "armor": "leather"})
        ch = B.build(mini, p)
        assert ch.hit_die == 8 and ch.hp == 10

    def test_proficiency_by_level(self, mini):
        assert [B.build(mini, fighter(l)).prof for l in (1, 4, 5, 9)] == [2, 2, 3, 4]

    def test_ac_heavy_armor_shield_defense(self, mini):
        assert B.build(mini, fighter(3)).ac == 16 + 2 + 1

    def test_ac_medium_caps_dex(self, mini):
        p = priest(1, abilities={"str": 10, "dex": 16, "con": 14, "int": 8, "wis": 15, "cha": 10})
        assert B.build(mini, p).ac == 14 + 2 + 2

    def test_attack_and_dueling_damage(self, mini):
        w = B.build(mini, fighter(1)).weapon
        assert (w.to_hit, w.mod, str(w.dice)) == (5, 5, "1d8")   # +3 Str +2 PB; +3 +2 Dueling

    def test_versatile_two_hands_without_shield(self, mini):
        w = B.build(mini, fighter(1, kit={"armor": "chain_mail", "weapons": ["longsword"]})).weapon
        assert str(w.dice) == "1d10" and w.mod == 3   # Dueling needs one hand

    def test_save_dc_and_spell_attack(self, mini):
        ch = B.build(mini, priest(1))
        assert (ch.save_dc, ch.spell_attack) == (13, 5)

    def test_saves(self, mini):
        ch = B.build(mini, priest(1))
        assert ch.saves["wis"] == 5 and ch.saves["str"] == 0

    def test_full_slots_by_character_level(self, mini):
        assert B.build(mini, priest(5)).slots == [4, 3, 2]

    def test_half_caster_slots(self, mini):
        p = B.Picks(facet="soul", path="steel", level=5, abilities=ARRAY,
                    talents={1: "battle_casting", 3: "wider_study", 5: "tough"},
                    knacks={2: "linguist"}, domains=["the_tide", "presence"],
                    kit={"armor": "chain_mail", "weapons": ["longsword"]})
        ch = B.build(mini, p)
        assert ch.slots == [4, 2] and ch.progression == "half"

    def test_spell_list_capped_by_slot_level(self, mini):
        ch1, ch5 = B.build(mini, priest(1)), B.build(mini, priest(5))
        assert "Spirit Guardians" not in ch1.spells and "Fireball" not in ch1.spells
        assert "Spirit Guardians" in ch5.spells and "Fireball" in ch5.spells
        assert "Sacred Flame" in ch1.cantrips and "Fire Bolt" in ch1.cantrips

    def test_scaling_replaces_rider(self, mini):
        p = fighter(7)
        prof = B.build(mini, p).profile()
        assert prof.riders[0].dice == Dice(2, 6)

    def test_extra_attack_from_path_at_5(self, mini):
        assert B.build(mini, fighter(4)).profile().attacks_per_action == 1
        assert B.build(mini, fighter(5)).profile().attacks_per_action == 2

    def test_second_wind_profile(self, mini):
        sw = B.build(mini, fighter(3)).profile().second_wind
        assert sw["uses"].uses == 2 and sw["uses"].recharge == "short"
        assert sw["dice"] == Dice(1, 10) and sw["bonus"] == 3

    def test_heal_boost_marks_healer(self, mini):
        prof = B.build(mini, priest(1)).profile()
        assert prof.healer and prof.caster.heal_boost


class TestLegality:
    def _errs(self, mini, p):
        with pytest.raises(B.BuildError) as ei:
            B.build(mini, p)
        return ei.value.errors

    def test_legal_builds_pass(self, mini):
        for l in range(1, 11):
            B.build(mini, fighter(l))
            B.build(mini, priest(l))

    def test_body_cannot_take_spell_path(self, mini):
        assert any("no 'spell' path" in e for e in self._errs(mini, fighter(1, path="spell")))

    def test_talent_at_wrong_level(self, mini):
        p = fighter(3, talents={1: "dueling", 2: "tough", 3: "defense"})
        assert any("L2: no talent pick" in e for e in self._errs(mini, p))

    def test_missing_talent(self, mini):
        p = fighter(3, talents={1: "dueling"})
        assert any("L3: no talent chosen" in e for e in self._errs(mini, p))

    def test_requires_path(self, mini):
        p = priest(1, talents={1: "battle_casting"}, casting_ability="wis")
        errs = self._errs(mini, p)
        assert any("requires the steel path" in e for e in errs)

    def test_requires_casting(self, mini):
        p = fighter(1, talents={1: "warden"})
        assert any("requires spellcasting" in e for e in self._errs(mini, p))

    def test_cross_facet_cap(self, mini):
        p = B.Picks(facet="mind", path="steel", level=5, abilities=ARRAY,
                    talents={1: "dueling", 3: "defense", 5: "battle_casting"},
                    casting_ability="cha", domains=["the_tide"],
                    kit={"weapons": ["rapier"]})
        assert any("cross-Facet" in e and "cap is 2" in e for e in self._errs(mini, p))

    def test_one_tradition(self, mini):
        p = priest(1, path="spell", talents={1: "battle_casting"})
        errs = self._errs(mini, p)
        assert any("one tradition" in e for e in errs)

    def test_domain_must_match_tradition(self, mini):
        p = priest(1, domains=["flame"])
        assert any("flame is thaumaturgy" in e for e in self._errs(mini, p))

    def test_domain_count(self, mini):
        p = priest(1, domains=["the_tide", "presence"])
        assert any("2 domains chosen; this build has 1" in e for e in self._errs(mini, p))

    def test_casting_ability_must_fit_tradition(self, mini):
        p = priest(1, casting_ability="int")
        assert any("not int" in e for e in self._errs(mini, p))

    def test_soul_casting_ability_is_the_higher(self, mini):
        p = priest(1, casting_ability=None,
                   abilities={"str": 10, "dex": 12, "con": 14, "int": 8, "wis": 12, "cha": 16})
        assert B.build(mini, p).casting_ability == "cha"

    def test_armor_proficiency(self, mini):
        p = priest(1, kit={"armor": "plate", "weapons": ["mace"]})
        assert any("heavy armor" in e for e in self._errs(mini, p))

    def test_knack_is_not_a_talent(self, mini):
        p = fighter(1, talents={1: "linguist"})
        assert any("it is a knack" in e for e in self._errs(mini, p))

    def test_background_knack_not_again(self, mini):
        p = fighter(2, knacks={2: "streetwise"})
        assert any("taken twice" in e for e in self._errs(mini, p))

    def test_same_talent_twice(self, mini):
        p = fighter(3, talents={1: "dueling", 3: "dueling"})
        assert any("taken twice" in e for e in self._errs(mini, p))

    def test_all_errors_listed_at_once(self, mini):
        p = fighter(3, path="spell", talents={1: "linguist"})
        assert len(self._errs(mini, p)) >= 3

    def test_level_range(self, mini):
        assert any("outside" in e for e in self._errs(mini, fighter(11)))

    def test_custom_base_abilities_checked(self, mini):
        p = fighter(1, base_abilities={"str": 15, "dex": 15, "con": 15, "int": 15, "wis": 15,
                                       "cha": 15})
        assert any("standard array" in e for e in self._errs(mini, p))

    def test_custom_background_bonus_checked(self, mini):
        p = fighter(1, base_abilities={"str": 15, "dex": 12, "con": 14, "int": 8, "wis": 13,
                                       "cha": 10})
        B.build(mini, p)   # 15+2=17, 14+1=15: matches fighter()'s final scores
        p2 = fighter(1, base_abilities={"str": 14, "dex": 12, "con": 15, "int": 8, "wis": 13,
                                        "cha": 10})
        assert any("base + background" in e for e in self._errs(mini, p2))


class TestDropToOneAndFortitude:
    def test_floor_one_keeps_pc_up(self):
        c = pc()
        out = combat.apply_damage(Script([]), c, 25, floor_one=True)
        assert c.hp == 1 and c.state == "active" and out.floored

    def test_floor_one_not_used_when_not_dropping(self):
        c = pc()
        out = combat.apply_damage(Script([]), c, 5, floor_one=True)
        assert c.hp == 15 and not out.floored

    def test_floor_one_does_not_stop_massive_damage(self):
        c = pc(max_hp=10)
        combat.apply_damage(Script([]), c, 25, floor_one=True)
        assert c.state == "dead"

    def test_undead_fortitude_save_keeps_it_at_1(self):
        z = foe(max_hp=15, tags={"undead_fortitude"}, saves={"con": 3})
        combat.apply_damage(Script([15]), z, 16)          # DC 5 + 16 = 21; 15 + 3 = 18 fails
        assert z.state == "dead"
        z2 = foe(max_hp=15, tags={"undead_fortitude"}, saves={"con": 3})
        combat.apply_damage(Script([19]), z2, 15)         # DC 20; 19 + 3 = 22 holds
        assert z2.hp == 1 and z2.state == "active"

    def test_undead_fortitude_not_vs_crit_or_radiant(self):
        z = foe(max_hp=15, tags={"undead_fortitude"}, saves={"con": 30})
        combat.apply_damage(Script([]), z, 15, crit=True)
        assert z.state == "dead"
        z2 = foe(max_hp=15, tags={"undead_fortitude"}, saves={"con": 30})
        combat.apply_damage(Script([]), z2, 15, dtype="radiant")
        assert z2.state == "dead"


class TestSparkDie:
    """DESIGN v0.2 §6.3 / V15: a Spark adds 1d6 after the roll (Turn the Odds: subtracts)."""

    def test_spark_turns_a_miss_into_a_hit(self):
        r = combat.attack_roll(Script([10]), bonus=3, ac=15)          # 13: miss
        r2 = combat.spark_attack(Script([4]), r, ac=15)
        assert r2.hit and r2.total == 17

    def test_spark_can_fail(self):
        r = combat.attack_roll(Script([10]), bonus=3, ac=16)
        assert not combat.spark_attack(Script([2]), r, ac=16).hit

    def test_spark_never_fixes_a_natural_1(self):
        r = combat.attack_roll(Script([1]), bonus=30, ac=10)
        assert not combat.spark_attack(Script([6]), r, ac=10).hit

    def test_spark_worth_spending_only_within_six(self):
        assert combat.spark_can_turn(total=10, target=16)
        assert not combat.spark_can_turn(total=9, target=16)
        assert not combat.spark_can_turn(total=16, target=16)

    def test_subtract_turns_a_hit_into_a_miss(self):
        r = combat.attack_roll(Script([12]), bonus=4, ac=15)          # 16: hit
        assert not combat.spark_attack(Script([3]), r, ac=15, subtract=True).hit

    def test_subtract_cannot_undo_a_crit(self):
        r = combat.attack_roll(Script([20]), bonus=0, ac=15)
        assert combat.spark_attack(Script([6]), r, ac=15, subtract=True).hit

    def test_spark_on_a_save(self):
        s = combat.saving_throw(Script([8]), bonus=2, dc=13)          # 10: fail
        assert combat.spark_save(Script([3]), s, dc=13).success


# ================================================================ simulator mechanics (rules applied through the sim)

from facets_d20 import sim as S  # noqa: E402
from facets_d20.profile import CombatProfile, Rider, Weapon  # noqa: E402


def _dummy_fight(profile, faces, *, ac=10):
    from facets_d20.monsters import MonsterBlock
    dummy = MonsterBlock("dummy", "Dummy", Fraction(0), ac, 10_000, (),
                         {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0},
                         morale="never", source="engine")
    f = S.Fight(Script(faces), [profile], S.Encounter.of(S.FoeSpec(dummy)), RuleOptions(), 1.0)
    return f, f.pcs[0], f.foes[0]


class TestRidersThroughTheSim:
    def _prof(self, riders, limit=1, attacks=2):
        return CombatProfile(name="r", level=5, prof=3, hp=30, ac=15, saves={}, dex_mod=3,
                             weapon=Weapon("rapier", Dice(1, 8), 20, 3, "piercing", finesse=True),
                             attacks_per_action=attacks, riders=riders, rider_limit=limit)

    def test_once_per_turn_rider_lands_once(self):
        prof = self._prof([Rider("sneak", Dice(1, 6), frozenset({"has_advantage"}),
                                 frozenset({"finesse"}))], limit=99)
        f, me, foe = _dummy_fight(prof, [], ac=10)
        # Two attacks with advantage: d20s (2,15)(2,15); weapon d8=4 each; rider d6=6 once.
        f.rng = Script([2, 15, 4, 6, 2, 15, 4])
        turn = {}
        foe.conditions.add("desperate")          # grants advantage in the sim
        f.attack_action(me, turn)
        assert f.damage_by_pc[me.id] == (4 + 3 + 6) + (4 + 3)

    def test_e1_one_rider_a_turn_across_sources(self):
        prof = self._prof([Rider("a", Dice(1, 6), frozenset(), frozenset()),
                           Rider("b", Dice(2, 6), frozenset(), frozenset())], limit=1)
        f, me, foe = _dummy_fight(prof, [])
        # Two hits: the bigger rider (b, 2d6 = 5+5) on the first, nothing on the second.
        f.rng = Script([15, 4, 5, 5, 15, 4])
        f.attack_action(me, {})
        assert f.damage_by_pc[me.id] == (4 + 3 + 10) + (4 + 3)

    def test_rider_needs_its_condition(self):
        prof = self._prof([Rider("sneak", Dice(1, 6), frozenset({"has_advantage"}),
                                 frozenset({"finesse"}))], attacks=1)
        f, me, foe = _dummy_fight(prof, [])
        f.rng = Script([15, 4])                   # no advantage, no melee ally
        f.attack_action(me, {})
        assert f.damage_by_pc[me.id] == 7


# ================================================================ V21 ability picks and Amendment 2 (no paths)


@pytest.fixture(scope="module")
def mini_v21():
    raw = copy.deepcopy(MINI)
    raw["advancement"]["asi_rule"] = "choice"
    return D.from_dicts(raw, copy.deepcopy(MINI_SPELLS))


class TestAbilityChoiceV21:
    def test_default_is_plus_two_primary_weapon(self, mini_v21):
        ch = B.build(mini_v21, fighter(4))
        assert ch.abilities["str"] == 19 and ch.abilities["con"] == 15

    def test_default_overflow_splits_at_19(self, mini_v21):
        ch = B.build(mini_v21, fighter(8))
        assert ch.abilities["str"] == 20 and ch.abilities["con"] == 16

    def test_default_for_a_caster_is_the_casting_ability(self, mini_v21):
        ch = B.build(mini_v21, priest(4))
        assert ch.abilities["wis"] == 18 and ch.save_dc == 8 + 2 + 4

    def test_explicit_plus_one_to_two(self, mini_v21):
        ch = B.build(mini_v21, fighter(4, asi={4: {"plus1": ["str", "con"]}}))
        assert (ch.abilities["str"], ch.abilities["con"]) == (18, 16)
        assert ch.hp == 13 + 3 * (5 + 1 + 3)

    def test_knack_instead(self, mini_v21):
        ch = B.build(mini_v21, fighter(4, asi={4: {"knack": "trivia"}}))
        assert ch.abilities["str"] == 17 and "trivia" in ch.features

    def test_cannot_pass_20(self, mini_v21):
        p = fighter(4, abilities={"str": 20, "dex": 12, "con": 15, "int": 8, "wis": 13, "cha": 10},
                    asi={4: {"plus2": "str"}})
        with pytest.raises(B.BuildError, match="above 20"):
            B.build(mini_v21, p)

    def test_bad_form(self, mini_v21):
        with pytest.raises(B.BuildError, match="exactly one"):
            B.build(mini_v21, fighter(4, asi={4: {"plus2": "str", "knack": "trivia"}}))

    def test_wrong_level(self, mini_v21):
        with pytest.raises(B.BuildError, match="no ability-score pick"):
            B.build(mini_v21, fighter(5, asi={5: {"plus2": "str"}}))

    def test_unknown_knack(self, mini_v21):
        with pytest.raises(B.BuildError, match="not a knack"):
            B.build(mini_v21, fighter(4, asi={4: {"knack": "juggling"}}))

    def test_knack_not_twice(self, mini_v21):
        with pytest.raises(B.BuildError, match="taken twice"):
            B.build(mini_v21, fighter(6, asi={4: {"knack": "healer_knack"}}))

    def test_automatic_rules_reject_a_choice(self, mini):
        with pytest.raises(B.BuildError, match="automatic"):
            B.build(mini, fighter(4, asi={4: {"plus2": "str"}}))


@pytest.fixture(scope="module")
def mini_no_paths():
    raw = copy.deepcopy(MINI)
    raw["paths"] = {}
    for f in raw["facets"].values():
        f.pop("paths", None)
    raw["talents"] += [
        {"id": "arcane_study", "name": "Arcane Study", "menus": ["mind"],
         "effects": [{"type": "casting", "tradition": "thaumaturgy", "progression": "full",
                      "ability": ["int"]}]},
        {"id": "soldiering", "name": "Soldiering", "menus": ["mind", "soul"],
         "effects": [{"type": "armor_proficiency", "categories": ["medium", "shields"]},
                     {"type": "weapon_proficiency", "categories": ["martial"]},
                     {"type": "extra_attack", "attacks": 2}]},
    ]
    for t in raw["talents"]:
        t.pop("requires_path", None)
    return D.from_dicts(raw, copy.deepcopy(MINI_SPELLS))


class TestNoPathsAmendment2:
    def _mind(self, talents, **kw):
        base = dict(facet="mind", path=None, level=5,
                    abilities={"str": 8, "dex": 14, "con": 13, "int": 16, "wis": 12, "cha": 10},
                    talents=talents, knacks={2: "linguist"},
                    kit={"armor": "leather", "weapons": ["quarterstaff"]})
        base.update(kw)
        return B.Picks(**base)

    def test_caster_from_a_talent(self, mini_no_paths):
        ch = B.build(mini_no_paths, self._mind({1: "arcane_study", 3: "tough", 5: "precision"},
                                               domains=["flame"]))
        assert ch.progression == "full" and ch.slots == [4, 3, 2]

    def test_martial_from_a_talent(self, mini_no_paths):
        ch = B.build(mini_no_paths, self._mind({1: "soldiering", 3: "tough", 5: "precision"},
                                               kit={"armor": "chain_shirt", "shield": True,
                                                    "weapons": ["rapier"]}))
        assert ch.profile().attacks_per_action == 2 and ch.ac == 13 + 2 + 2
        assert ch.weapon.to_hit == 2 + 3        # martial rapier is proficient

    def test_hybrid_is_legal(self, mini_no_paths):
        B.build(mini_no_paths, self._mind({1: "arcane_study", 3: "soldiering", 5: "tough"},
                                          domains=["flame"]))

    def test_no_proficiency_without_the_talent(self, mini_no_paths):
        with pytest.raises(B.BuildError, match="medium armor"):
            B.build(mini_no_paths, self._mind({1: "tough", 3: "precision", 5: "wider_study"},
                                              kit={"armor": "chain_shirt", "weapons": ["rapier"]}))

    def test_a_path_is_rejected_when_the_ruleset_has_none(self, mini_no_paths):
        with pytest.raises(B.BuildError, match="no paths"):
            B.build(mini_no_paths, self._mind({1: "tough", 3: "precision", 5: "grit"},
                                              path="steel"))


# ================================================================ the real data: presets pinned (hand-derived)

from facets_d20 import analysis as AN  # noqa: E402
from facets_d20 import spells as SP  # noqa: E402

# (level: HP, AC, to-hit with the kit's first weapon, save DC or None, slots)
# Hand-derived from the yaml as of 2026-09-28 (Amendment 2 track chassis; V21 default +2 to
# the main track's ability at 4th and 8th). HP = die + Con, then (die/2 + 1 + Con) a level,
# recomputed when Hardy or Martial Training steps the die; Hardened +1/level at Steel
# depth 3. Casting: Spell depth 1 half, depth 2 full (main track only). Re-derive when a
# preset changes.
PRESET_NUMBERS = {
    # Body d10, Con +2. Steel: Weapon Expert 1, Guardian 3, Cleave 5 (depth 3 → Hardened
    # +1 HP/level; depth 2 → Extra Attack at 5th). Hardy 7 → d12. Str 16→18→20.
    # L7: 12+2+6×(7+2)=68, +7 = 75. L10: 14+9×9=95, +10 = 105. Chain mail+shield+1 = 19.
    "fighter": {1: (12, 19, 6, None, []), 4: (36, 19, 7, None, []),
                7: (75, 19, 8, None, []), 10: (105, 19, 10, None, [])},
    # Steel: Precision 1, Marksman 5, Weapon Expert 7 (+1 hit, +1 AC in leather). Dex 16→20.
    "rogue": {1: (12, 14, 5, None, []), 4: (36, 15, 6, None, []),
              7: (67, 16, 8, None, []), 10: (94, 17, 10, None, [])},
    # Steel: Rage 1, Cleave 5, Guardian 7; Hardy 3 → d12. AC 10+Dex+Con.
    "barbarian": {1: (12, 14, 5, None, []), 4: (41, 14, 6, None, []),
                  7: (75, 14, 7, None, []), 10: (105, 14, 9, None, [])},
    # Steel: Martial Arts 1, Weapon Expert 5 (depth 2). Hardy 9 → d12. AC 10+Dex+Wis.
    "monk": {1: (12, 15, 5, None, []), 4: (36, 16, 6, None, []),
             7: (60, 16, 8, None, []), 10: (95, 17, 10, None, [])},
    # Mind d6, Con +2. Spell: Evoker 1 (half), Wider Study 3 (full), Turn the Odds 5
    # (Deep Magic). Hardy 9 → d8. Int 16→18→20. Quarterstaff Str −1.
    "wizard": {1: (8, 12, 1, 13, [2]), 4: (26, 12, 1, 14, [4, 3]),
               7: (44, 12, 2, 15, [4, 3, 3, 1]), 10: (73, 12, 3, 17, [4, 3, 3, 3, 2])},
    # Steel main from 1st: Martial Training (d6→d8, medium armor, shields, martial).
    # Precision 1, Anatomist 5, Weapon Expert 9 (depth 3: Hardened). Hardy 7 → d10.
    "investigator": {1: (9, 17, 5, None, []), 4: (27, 17, 6, None, []),
                     7: (53, 17, 7, None, []), 10: (84, 18, 10, None, [])},
    # Spell: Turn the Odds 1, Wider Study 3 (full). Con +1. Dagger Dex +1.
    "loremaster": {1: (7, 12, 3, 13, [2]), 4: (22, 12, 3, 14, [4, 3]),
                   7: (37, 12, 4, 15, [4, 3, 3, 1]), 10: (52, 12, 5, 17, [4, 3, 3, 3, 2])},
    # Spell 1 at 1st (half); Weapon Expert 3 makes a 1/1 tie → Steel main (d8, medium
    # armor, shields) with half casting. Kit from 3rd: breastplate+shield+1 = 19, rapier.
    # Steel main → V21 default +2 Dex (15→17→19). Hardy 7 → d10. Int stays 16.
    "tinker": {1: (7, 13, 4, 13, [2]), 4: (27, 19, 6, 13, [3]),
               7: (53, 19, 7, 14, [4, 3]), 10: (74, 19, 9, 15, [4, 3, 2])},
    # Soul d8, Con +2. Spell: Channel 1, Wider Study 3, Mending Hands 5. Hardy 9 → d10.
    "priest": {1: (10, 16, 3, 13, [2]), 4: (31, 16, 3, 14, [4, 3]),
               7: (52, 16, 4, 15, [4, 3, 3, 1]), 10: (84, 16, 5, 17, [4, 3, 3, 3, 2])},
    # Spell: Wild Shape 1, Wider Study 3, Channel 5. Hardy 7 → d10. Leather+shield 15.
    "druid": {1: (10, 15, 1, 13, [2]), 4: (31, 15, 1, 14, [4, 3]),
              7: (60, 15, 2, 15, [4, 3, 3, 1]), 10: (84, 15, 3, 17, [4, 3, 3, 3, 2])},
    # Spell: Turn the Odds 1, Wider Study 3, Prophecy 5. Cha 16→18→20 casts. Con +1.
    "oracle": {1: (9, 16, 1, 13, [2]), 4: (27, 16, 1, 14, [4, 3]),
               7: (45, 16, 2, 15, [4, 3, 3, 1]), 10: (63, 16, 3, 17, [4, 3, 3, 3, 2])},
    # Steel: Sworn Strike 1, Weapon Expert 5 (Extra Attack); Spell: Mending Hands 3
    # (secondary: half caster, Wis 15). Martial Training: d8→d10, heavy armor. Str 16→20.
    "oathsworn": {1: (12, 18, 5, None, []), 4: (36, 18, 6, 12, [3]),
                  7: (60, 19, 8, 13, [4, 3]), 10: (84, 19, 10, 14, [4, 3, 2])},
}

# SRD 5.2.1 baselines (engine-owned data): standard array + background +2/+1, ASI +2 main.
SRD_NUMBERS = {
    "srd_fighter_champion": {1: (12, 18, 5), 4: (36, 18, 6), 7: (67, 18, 8), 10: (104, 18, 9)},
    "srd_rogue_thief": {1: (10, 14, 5), 4: (31, 15, 6), 7: (52, 15, 7), 10: (93, 16, 9)},
    "srd_wizard_evoker": {1: (8, 11, 1), 4: (26, 11, 1), 7: (44, 11, 2), 10: (72, 11, 3)},
    "srd_cleric_life": {1: (10, 18, 3), 4: (31, 18, 3), 7: (52, 18, 4), 10: (83, 18, 5)},
    "srd_paladin_devotion": {1: (11, 18, 5), 4: (32, 18, 8), 7: (53, 18, 9), 10: (74, 18, 12)},
    "srd_barbarian_berserker": {1: (14, 13, 5), 4: (41, 13, 6), 7: (68, 13, 7), 10: (105, 14, 9)},
}


@pytest.fixture(scope="module")
def rs():
    return D.load()


@pytest.fixture(scope="module")
def srd():
    return D.load_baselines()


class TestPresetNumbers:
    @pytest.mark.parametrize("pid,level", [(p, l) for p in PRESET_NUMBERS for l in (1, 4, 7, 10)])
    def test_numbers(self, rs, pid, level):
        if pid not in rs.presets:
            pytest.skip(f"{pid} no longer a preset")
        ch = B.build(rs, B.Picks.from_preset(rs, pid, level))
        w = ch.attack_with(rs.presets[pid]["kit"]["weapons"][0])
        assert (ch.hp, ch.ac, w.to_hit, ch.save_dc, ch.slots) == PRESET_NUMBERS[pid][level]

    def test_every_preset_pinned(self, rs):
        assert set(rs.presets) <= set(PRESET_NUMBERS)

    def test_every_preset_builds_every_level(self, rs):
        for pid in rs.presets:
            for level in range(1, 11):
                B.build(rs, B.Picks.from_preset(rs, pid, level)).profile()

    def test_every_sim_build_builds_every_level(self, rs):
        for bid in rs.sim_builds:
            for level in (1, 4, 7, 10):
                B.build(rs, B.Picks.from_sim_build(rs, bid, level)).profile()


class TestSrdBaselines:
    @pytest.mark.parametrize("bid,level", [(b, l) for b in SRD_NUMBERS for l in (1, 4, 7, 10)])
    def test_numbers(self, srd, bid, level):
        ch = B.build(srd, B.Picks.from_preset(srd, bid, level))
        w = ch.attack_with(srd.presets[bid]["kit"]["weapons"][0])
        assert (ch.hp, ch.ac, w.to_hit) == SRD_NUMBERS[bid][level]

    def test_they_are_the_yaml_baselines(self, rs, srd):
        assert set(rs.raw["balance"]["srd_baselines"]) == set(srd.presets)

    def test_srd_caster_dcs(self, srd):
        dc = {b: B.build(srd, B.Picks.from_preset(srd, b, 10)).save_dc
              for b in ("srd_wizard_evoker", "srd_cleric_life", "srd_paladin_devotion")}
        assert dc == {"srd_wizard_evoker": 17, "srd_cleric_life": 17, "srd_paladin_devotion": 15}

    def test_srd_sneak_attack_scales(self, srd):
        prof = B.build(srd, B.Picks.from_preset(srd, "srd_rogue_thief", 9)).profile()
        assert prof.riders[0].dice == Dice(5, 6)

    def test_srd_has_no_rider_limit(self, srd):
        prof = B.build(srd, B.Picks.from_preset(srd, "srd_barbarian_berserker", 5)).profile()
        assert prof.rider_limit > 1 and prof.rage["damage"] == 2


class TestAuditExploitBuilds:
    """Audit C1/C2 under the Amendment 2 track chassis (DESIGN v0.2 P-17): the v0.1 exploit
    shapes are legal again — the tracks make them pay instead of forbidding them."""

    def _soul(self, rs, talents, level, **kw):
        base = dict(facet="soul", path=None, level=level,
                    abilities={"str": 16, "dex": 10, "con": 13, "int": 8, "wis": 12, "cha": 16},
                    talents=talents, knacks=None,
                    kit={"armor": "chain_mail", "shield": True, "weapons": ["longsword"]})
        base.update(kw)
        p = B.Picks(**base)
        p.domains = ["presence"] if B._casting_sources(rs, p) else []
        return p

    def test_v01_battle_priest_shape_is_legal_but_half(self, rs):
        p = self._soul(rs, {1: "sworn_strike", 3: "channel", 5: "weapon_expert"}, 5)
        ch = B.build(rs, p)
        assert ch.profile().attacks_per_action == 2 and ch.progression == "half"

    def test_it_never_reaches_full_casting_with_extra_attack(self, rs):
        for level in range(1, 11):
            talents = {k: v for k, v in {1: "sworn_strike", 3: "channel", 5: "weapon_expert",
                                         7: "guardian", 9: "mending_hands"}.items() if k <= level}
            ch = B.build(rs, self._soul(rs, talents, level))
            assert not (ch.progression == "full" and ch.profile().attacks_per_action > 1), level

    def test_two_spell_one_steel_soul_is_full_without_extra_attack_or_heavy_armor(self, rs):
        p = self._soul(rs, {1: "channel", 3: "wider_study", 5: "sworn_strike"}, 5,
                       kit={"armor": "scale_mail", "shield": True, "weapons": ["longsword"]})
        p.domains = ["presence", "the_tide"]
        ch = B.build(rs, p)
        assert ch.progression == "full" and ch.profile().attacks_per_action == 1
        p.kit = {"armor": "chain_mail", "shield": True, "weapons": ["longsword"]}
        assert any("heavy armor" in e for e in B.check(rs, p))

    def test_three_cross_picks_are_illegal(self, rs):
        p = B.Picks(facet="body", path=None, level=5,
                    abilities={"str": 16, "dex": 13, "con": 15, "int": 8, "wis": 13, "cha": 10},
                    talents={1: "anticipate", 3: "iron_mind", 5: "warden"}, knacks=None,
                    kit={"armor": "chain_mail", "weapons": ["longsword"]})
        assert any("cap is 2" in e for e in B.check(rs, p))

    def test_sim_builds_name_an_audit_finding(self, rs):
        assert all(b.get("audit") for b in rs.sim_builds.values())


class TestPlannerChecks:
    """The checks DESIGN v0.2 P-6, P-9 and P-12 name."""

    def test_body_with_two_spell_talents_is_a_half_caster(self, rs):
        p = B.Picks(facet="body", path=None, level=5,
                    abilities={"str": 10, "dex": 13, "con": 15, "int": 8, "wis": 16, "cha": 12},
                    talents={1: "channel", 3: "wider_study", 5: "alert"}, knacks=None,
                    tradition="invocation", domains=["the_tide", "presence"],
                    kit={"armor": "chain_mail", "weapons": ["mace"]})
        ch = B.build(rs, p)
        assert ch.progression == "half" and ch.slots == [4, 2]

    def test_body_weight_makes_steel_main_with_no_talents(self, rs):
        p = B.Picks.from_preset(rs, "fighter", 1)
        p.talents = {1: "alert"}
        assert B.picks_main_track(rs, p) == "steel"

    def test_soul_caster_at_third_with_fate_is_illegal(self, rs):
        p = B.Picks.from_preset(rs, "oracle", 3)
        p.domains = ["fate", "binding"]
        assert any("Deep Magic" in e for e in B.check(rs, p))

    def test_oracle_at_fifth_has_fate(self, rs):
        assert "fate" in _levels(rs, "oracle", 5).domains

    def test_priest_at_fifth_has_three_domains(self, rs):
        assert sorted(_levels(rs, "priest", 5).domains) == ["presence", "the_living_world", "the_tide"]

    def test_veteran_damage_is_flat_not_a_rider(self, rs):
        prof = _levels(rs, "fighter", 5).profile()
        w = _levels(rs, "fighter", 5).attack_with("longsword")
        assert w.mod == 4 + 2 and all(r.name != "veteran" for r in prof.riders)   # Str 18 + Veteran

    def test_paladin_baseline_keeps_its_smite(self, srd):
        prof = B.build(srd, B.Picks.from_preset(srd, "srd_paladin_devotion", 5)).profile()
        assert "Divine Smite" in prof.caster.spells and "Divine Smite" in srd.sim_spells


class TestControlledCreatureLimitE2:
    def test_two_companions_illegal(self):
        raw = copy.deepcopy(MINI)
        raw["build_rules"]["controlled_creature_limit"] = 1
        for i in (1, 2):
            raw["talents"].append({"id": f"pet{i}", "name": f"Pet {i}", "menus": ["body"],
                                   "effects": [{"type": "companion", "ac": 12, "hp": 10}]})
        mini = D.from_dicts(raw, MINI_SPELLS)
        with pytest.raises(B.BuildError, match="E2"):
            B.build(mini, fighter(3, talents={1: "pet1", 3: "pet2"}))

    def test_one_companion_fine(self):
        raw = copy.deepcopy(MINI)
        raw["build_rules"]["controlled_creature_limit"] = 1
        raw["talents"].append({"id": "pet1", "name": "Pet", "menus": ["body"],
                               "effects": [{"type": "companion", "ac": 12, "hp": 10}]})
        B.build(D.from_dicts(raw, MINI_SPELLS), fighter(3, talents={1: "pet1", 3: "defense"}))

    def test_no_limit_declared(self, mini):
        B.build(mini, fighter(3))


# ================================================================ spells from the yaml


@pytest.fixture(scope="module")
def book(rs):
    return SP.book(rs)


class TestSimSpells:
    def test_every_sim_spell_parses(self, book, rs):
        assert set(book) == set(rs.sim_spells)

    def test_upcast_adds_dice(self, book):
        assert SP.dice_at(book["Fireball"], 5) == (Dice(10, 6),)

    def test_cantrip_scales_at_5(self, book):
        assert SP.dice_at(book["Fire Bolt"], 0, 4) == (Dice(1, 10),)
        assert SP.dice_at(book["Fire Bolt"], 0, 5) == (Dice(2, 10),)

    def test_mixed_dice(self, book):
        assert SP.dice_at(book["Ice Storm"], 4) == (Dice(2, 10), Dice(4, 6))
        assert SP.dice_at(book["Ice Storm"], 5) == (Dice(3, 10), Dice(4, 6))

    def test_eldritch_beams_by_level(self, book):
        assert SP.beams_at(book["Eldritch Blast"], 0, 4) == 1
        assert SP.beams_at(book["Eldritch Blast"], 0, 5) == 2

    def test_magic_missile_darts(self, book):
        assert SP.beams_at(book["Magic Missile"], 3) == 5

    def test_too_low_a_slot(self, book):
        with pytest.raises(ValueError):
            SP.dice_at(book["Fireball"], 2)

    def test_unknown_model_rejected(self):
        with pytest.raises(ValueError):
            SP.from_entry({"name": "Wish", "level": 9, "model": "anything"})


# ================================================================ the simulator: determinism, day, analysis


def _ref_party(rs, level=4):
    return [B.build(rs, B.Picks.from_preset(rs, p, level)).profile()
            for p in rs.raw["balance"]["reference_party"]]


class TestSimulator:
    def test_deterministic_under_a_seed(self, rs):
        party = _ref_party(rs)
        enc = S.Encounter.of(S.FoeSpec("owlbear"), S.FoeSpec("goblin_warrior", role="minion", count=3))
        a = S.simulate(party, enc, n=60, seed=5)
        b = S.simulate(party, enc, n=60, seed=5)
        assert a.as_row() == b.as_row() and a.dpr_by_pc == b.dpr_by_pc

    def test_different_seed_differs(self, rs):
        party = _ref_party(rs)
        enc = S.Encounter.of(S.FoeSpec("owlbear"))
        assert S.simulate(party, enc, n=60, seed=5).dpr_by_pc != \
            S.simulate(party, enc, n=60, seed=6).dpr_by_pc

    def test_a_hopeless_fight_is_lost(self, rs):
        party = _ref_party(rs, 1)
        s = S.simulate(party, S.Encounter.of(S.FoeSpec("young_red_dragon", role="boss")), n=20)
        assert s.win_rate == 0.0 and s.p_death > 0

    def test_a_trivial_fight_is_won_fast(self, rs):
        party = _ref_party(rs, 10)
        s = S.simulate(party, S.Encounter.of(S.FoeSpec("bandit", role="minion", count=2)), n=40)
        assert s.win_rate == 1.0 and s.mean_rounds <= 1.5

    def test_minions_die_to_one_hit(self, rs):
        party = _ref_party(rs, 4)
        r = S.run_fight(random.Random(3), party,
                        S.Encounter.of(S.FoeSpec("ogre", role="minion", count=4)))
        assert r.won and r.foes_killed + r.foes_broken == 4

    def test_share_allowance(self, rs):
        prof = B.build(rs, B.Picks.from_preset(rs, "wizard", 5)).profile()
        allow, slots = S.share_allowance(prof, 0.25)
        assert slots == [1, 1, 1]           # ceil(¼ of [4, 3, 2]) after Mage Armor's 1st


class TestDay:
    def test_pacing_spreads_slots(self, rs):
        prof = B.build(rs, B.Picks.from_preset(rs, "wizard", 5)).profile()
        d = S._DayPC(prof)
        _, first = d.allowance(4, False)
        _, last = d.allowance(1, False)
        assert first == [1, 1, 1] and last == prof.caster.slots

    def test_short_rest_refills_short_pools_and_spends_hit_dice(self, rs):
        prof = B.build(rs, B.Picks.from_preset(rs, "fighter", 4)).profile()
        d = S._DayPC(prof)
        d.left["action_surge"] = 0
        d.hp = 5
        d.short_rest(Script([10, 10, 10]), hd_bonus=0)
        assert d.left["action_surge"] == 1 and d.hp > 5 and d.hd < 4

    def test_a_day_runs_four_fights(self, rs):
        party = _ref_party(rs, 4)
        enc = S.Encounter.of(S.FoeSpec("goblin_warrior", count=2))
        day = S.run_day(random.Random(1), party, [enc] * 4)
        assert day.survived and len(day.fights) == 4 and day.rounds >= 4


class TestThreatModel:
    def test_standard_threat_grows_with_cr(self):
        assert AN.standard_threat(1) < AN.standard_threat(3) < AN.standard_threat(8)

    def test_cr_for_threat_inverts(self):
        assert AN.cr_for_threat(AN.standard_threat(4.0)) == pytest.approx(4.0, rel=0.02)

    def test_roles(self):
        m = AN.ThreatModel(minion_hp=8, boss=2, never=1.2)
        blk = AN.generic(3)
        assert m.of(blk, "boss") == pytest.approx(2 * AN.strength(blk))
        assert m.of(blk, "minion") == pytest.approx((8 * blk.damage_per_turn) ** 0.5)

    def test_compose_hits_its_budget(self):
        m = AN.ThreatModel()
        for shape in AN.SHAPES:
            enc = AN.compose(shape, 120, m)
            assert m.encounter_threat(enc) == pytest.approx(120, rel=0.35), shape

    def test_classify(self):
        tiers = AN.tiers_spec()
        o = AN.Outcome(n=1, win=1.0, rounds=3, hp_lost=0.27, p_drop=0, p_death=0)
        assert AN.classify(o, tiers) == "clash"
        assert AN.classify(AN.Outcome(1, 0.7, 5, 0.7, 1, 0.1), tiers) == "desperate"


class TestSrdLadderTool:
    def test_damage_average_with_rider(self):
        from tools.build_srd_monsters import parse_damage
        assert parse_damage("13 (2d6 + 6) Slashing damage plus 3 (1d6) Fire damage.") == \
            [(13, 2, 6, 6, "slashing"), (3, 1, 6, 0, "fire")]

    def test_conditional_rider_excluded(self):
        from tools.build_srd_monsters import parse_damage
        d = "5 (1d6 + 2) Slashing damage, plus 2 (1d4) Slashing damage if the attack roll had Advantage."
        assert parse_damage(d) == [(5, 1, 6, 2, "slashing")]

    def test_no_bonus(self):
        from tools.build_srd_monsters import parse_damage
        assert parse_damage("Failure: 56 (16d6) Fire damage.") == [(56, 16, 6, 0, "fire")]


@pytest.fixture(scope="module")
def table(rs):
    t = rs.raw.get("encounter_table")
    if not t:
        pytest.skip("encounter_table not written yet (run tools/d20_sim.py all --write)")
    mt = rs.raw["monster_threat"]["model"]
    m = AN.ThreatModel(minion_hp=float(mt["minion"].split("(")[1].split(" ")[0]),
                       boss=float(mt["boss"].split("x ")[1]),
                       never=float(mt["never_breaks"].split("x ")[1]))
    return {int(k): v for k, v in t.items()}, m


class TestEncounterTableReproduces:
    """Ruling 2: the table in the yaml is what the simulator finds (within tolerance)."""

    def test_clash_at_4th_lands_in_band(self, rs, table):
        t, m = table
        o = AN.mixed_outcome(_ref_party(rs, 4), 4 * t[4]["clash"], m, n=150, seed=11)
        assert 0.17 <= o.hp_lost <= 0.38 and o.win >= 0.93

    def test_clash_lasts_three_to_four_rounds(self, rs, table):
        t, m = table
        o = AN.mixed_outcome(_ref_party(rs, 4), 4 * t[4]["clash"], m, n=150, seed=12)
        assert 2.7 <= o.rounds <= 4.6

    def test_tiers_order_by_difficulty(self, rs, table):
        t, m = table
        hp = [AN.mixed_outcome(_ref_party(rs, 7), 4 * t[7][tier], m, n=80, seed=13).hp_lost
              for tier in AN.TIERS]
        assert hp == sorted(hp)

    def test_budgets_grow_with_level(self, table):
        t, _ = table
        clash = [t[L]["clash"] for L in range(1, 11)]
        assert clash[-1] > 3 * clash[0]


# ================================================================ tracks (Amendment 2): depth, main track, ranks


def _levels(rs, bid, level):
    entry = rs.presets.get(bid) or rs.sim_builds[bid]
    return B.build(rs, B.Picks.from_entry(rs, entry, level, name=bid))


class TestTracks:
    def test_depth_counts_tagged_talents(self, rs):
        p = B.Picks.from_preset(rs, "fighter", 10)
        assert B.track_depth(rs, p) == {"steel": 3}

    def test_main_track_is_the_deeper(self):
        assert B.main_track({"steel": 1, "spell": 3}) == "spell"
        assert B.main_track({"steel": 2}) == "steel"

    def test_tie_goes_to_steel(self):
        assert B.main_track({"steel": 2, "spell": 2}) == "steel"

    def test_no_track_no_main(self):
        assert B.main_track({}) is None

    def test_spell_depth_one_is_half_two_is_full(self, rs):
        assert _levels(rs, "wizard", 1).progression == "half"
        assert _levels(rs, "wizard", 3).progression == "full"

    def test_extra_attack_needs_steel_depth_two_and_fifth_level(self, rs):
        assert _levels(rs, "fighter", 4).profile().attacks_per_action == 1   # depth 2, level 4
        assert _levels(rs, "fighter", 5).profile().attacks_per_action == 2

    def test_hardened_at_steel_depth_three(self, rs):
        # fighter L5 vs L4: +1 level of HP (6+2) plus Hardened 5
        assert _levels(rs, "fighter", 5).hp - _levels(rs, "fighter", 4).hp == 8 + 5

    def test_tie_is_steel_main_with_half_casting(self, rs):
        ch = _levels(rs, "battle_priest", 7)             # Spell 2 · Steel 2
        assert ch.progression == "half" and ch.profile().attacks_per_action == 2

    def test_spell_main_again_drops_extra_attack(self, rs):
        ch = _levels(rs, "battle_priest_deep", 9)         # Steel 2 · Spell 3
        assert ch.progression == "full" and ch.profile().attacks_per_action == 1

    def test_secondary_steel_keeps_only_martial_weapons(self, rs):
        ch = _levels(rs, "armored_caster", 5)             # Spell 3 · Steel 1
        assert ch.hit_die == 6                             # no Martial Training die step
        assert "martial" in B._weapon_profs(rs, ch.picks)
        assert "medium" not in B._armor_profs(rs, ch.picks)

    def test_steel_main_mind_gets_armor_and_die(self, rs):
        ch = _levels(rs, "investigator", 1)
        assert ch.hit_die == 8 and {"medium", "shields"} <= B._armor_profs(rs, ch.picks)

    def test_scaling_needs_depth(self, rs):
        # Monk's Martial Arts (Steel) scales at 5th only with Steel depth 2: the monk has
        # Weapon Expert at 5th, so its 5th-level line (d8 die, Stunning Strike) applies.
        assert _levels(rs, "monk", 5).profile().stun is not None
        mini = copy.deepcopy(rs.presets["monk"])
        mini["talents"] = {1: "martial_arts", 3: "cunning", 5: "alert", 7: "hardy", 9: "anticipate"}
        mini["id"] = "shallow_monk"
        ch = B.build(rs, B.Picks.from_entry(rs, mini, 5))
        assert ch.profile().stun is None                   # depth 1: no 5th-level line

    def test_deep_magic_opens_a_prismatic_domain(self, rs):
        assert "the_arcane" in _levels(rs, "wizard", 5).domains
        assert "the_arcane" not in _levels(rs, "wizard", 4).domains

    def test_prismatic_without_deep_magic_is_illegal(self, rs):
        p = B.Picks.from_preset(rs, "wizard", 4)
        p.domains = ["constructed_force", "the_arcane"]
        assert any("Deep Magic" in e for e in B.check(rs, p))

    def test_body_caster_names_its_tradition(self, rs):
        ch = _levels(rs, "body_caster", 3)
        assert ch.tradition == "invocation" and ch.casting_ability == "wis"

    def test_body_caster_without_a_tradition_is_illegal(self, rs):
        entry = dict(rs.sim_builds["body_caster"])
        entry.pop("tradition")
        p = B.Picks.from_entry(rs, entry, 3)
        assert any("names its tradition" in e for e in B.check(rs, p))

    def test_kit_by_level(self, rs):
        assert _levels(rs, "tinker", 1).picks.kit["armor"] == "leather"
        assert _levels(rs, "tinker", 3).picks.kit["armor"] == "breastplate"

    def test_facets_filter_on_rank_effects(self, rs):
        # Martial Training's die step applies to Mind and Soul, not Body.
        assert _levels(rs, "fighter", 1).hit_die == 10


class TestPrimaryAbilityV21:
    def test_spell_main_raises_casting(self, rs):
        assert B.primary_ability(rs, B.Picks.from_preset(rs, "wizard", 4)) == "int"

    def test_steel_main_hybrid_raises_its_weapon_ability(self, rs):
        assert B.primary_ability(rs, B.Picks.from_preset(rs, "oathsworn", 4)) == "str"
        assert B.primary_ability(rs, B.Picks.from_preset(rs, "tinker", 4)) == "dex"

    def test_monk_raises_dex(self, rs):
        assert B.primary_ability(rs, B.Picks.from_preset(rs, "monk", 4)) == "dex"


class TestRanksLapseAmendment3:
    """BRIEF Amendment 3: the main track is always recomputed from current talents, so a
    rank lapses when the main track changes (a 2/2 Priest drops to the Half table)."""

    def _priest(self, rs, talents, level):
        p = B.Picks.from_preset(rs, "priest", level)
        p.talents = talents
        p.knacks = None
        p.domains = ["the_tide", "presence"]
        p.kit = {"armor": "scale_mail", "shield": True, "weapons": ["mace"]}
        return p

    def test_two_spell_one_steel_priest_is_full(self, rs):
        ch = B.build(rs, self._priest(rs, {1: "channel", 3: "wider_study", 5: "weapon_expert"}, 5))
        assert ch.progression == "full" and ch.slots == [4, 3, 2]

    def test_two_two_priest_drops_to_the_half_table(self, rs):
        ch = B.build(rs, self._priest(rs, {1: "channel", 3: "wider_study", 5: "weapon_expert",
                                           7: "sworn_strike"}, 7))
        assert ch.progression == "half" and ch.slots == [4, 3]
        assert B.picks_main_track(rs, ch.picks) == "steel"

    def test_retraining_back_restores_full(self, rs):
        p = self._priest(rs, {1: "channel", 3: "wider_study", 5: "weapon_expert",
                              7: "mending_hands"}, 7)
        p.domains.append("the_living_world")        # Spell 3 · main again: Deep Magic
        ch = B.build(rs, p)
        assert ch.progression == "full" and ch.slots == [4, 3, 3, 1]
