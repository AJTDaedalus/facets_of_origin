"""Combat (PHB III.3) — app/game/combat.py, the only combat rules implementation (T3)."""
from __future__ import annotations

import pytest

from app.game import combat
from app.game.combat import (
    CombatState, apply_armor, apply_damage_to_enemy, declare_defend, expire_exchange_effects,
    level_gap_difficulty, mob_bonus, morale_check, options_allowed, resolve_attack,
    resolve_enemy_attack, retainer_morale,
)
from app.game.character import TalentState
from tests.conftest import make_caster, make_character, make_enemy


def foe(ruleset, level=1, role="standard", armor=0, morale=7, count=1, key=None):
    return make_enemy(level=level, role=role, armor=armor, morale=morale).spawn(
        ruleset, count=count, key=key)


def scout(ruleset):
    return make_character(ruleset, name="Scout", player_name="Scout", class_id="scout",
                          talent_choices={}, background_id="wilderness_scout")


# ---------------------------------------------------------------------------
# Small rules
# ---------------------------------------------------------------------------

class TestLevelGap:
    def test_same_level_is_standard(self, ruleset):
        assert level_gap_difficulty(ruleset, 3, 3) == "Standard"

    def test_three_above_is_hard_six_above_very_hard(self, ruleset):
        assert level_gap_difficulty(ruleset, 1, 4) == "Hard"
        assert level_gap_difficulty(ruleset, 1, 7) == "Very Hard"

    def test_lower_foe_is_standard(self, ruleset):
        assert level_gap_difficulty(ruleset, 9, 1) == "Standard"


class TestMobBonus:
    def test_single_mook_has_no_bonus(self, ruleset):
        assert mob_bonus(ruleset, 1) == 0

    def test_plus_one_per_extra_capped_at_four(self, ruleset):
        assert mob_bonus(ruleset, 3) == 2 and mob_bonus(ruleset, 12) == 4

    def test_empty_mob_raises(self, ruleset):
        with pytest.raises(ValueError):
            mob_bonus(ruleset, 0)


class TestApplyArmor:
    def test_armor_subtracts(self, ruleset):
        assert apply_armor(ruleset, 5, 2) == 3

    def test_minimum_one(self, ruleset):
        assert apply_armor(ruleset, 2, 3) == 1

    def test_zero_damage_stays_zero(self, ruleset):
        assert apply_armor(ruleset, 0, 2) == 0

    def test_pierce_and_ignore(self, ruleset):
        assert apply_armor(ruleset, 5, 2, pierce=1) == 4
        assert apply_armor(ruleset, 5, 2, ignore=True) == 5

    def test_armor_above_cap_counts_as_cap(self, ruleset):
        assert apply_armor(ruleset, 10, 5) == 7


class TestRetainerMorale:
    def test_seven_plus_soul(self, ruleset, body_character):
        assert retainer_morale(ruleset, body_character) == 8

    def test_soul_zero(self, ruleset):
        assert retainer_morale(ruleset, make_character(ruleset, second_stat="mind")) == 7

    def test_high_soul(self, ruleset):
        ch = make_character(ruleset, facet="soul", second_stat="mind", class_id="captain",
                            talent_choices={})
        assert retainer_morale(ruleset, ch) == 9


# ---------------------------------------------------------------------------
# Exchange state
# ---------------------------------------------------------------------------

class TestCombatState:
    def test_exposure_is_consumed_once(self):
        s = CombatState()
        s.expose("A", "e1")
        assert s.is_exposed_to("A", "e1") and s.consume_exposure("A", "e1")
        assert not s.consume_exposure("A", "e1")

    def test_wildcard_exposure_matches_any_foe(self):
        s = CombatState()
        s.expose("A")
        assert s.is_exposed_to("A", "anything")

    def test_interceptor_for(self):
        s = CombatState()
        s.defend("Guard", ["Mage"])
        s.defend("Loner")
        assert s.interceptor_for("Mage") == "Guard"
        assert s.interceptor_for("Guard") is None and s.interceptor_for("Other") is None

    def test_star_intercepts_everyone(self):
        s = CombatState()
        s.defend("Guard", ["*"])
        assert s.interceptor_for("Anyone") == "Guard"

    def test_end_exchange_clears_and_counts(self):
        s = CombatState()
        s.expose("A")
        s.defend("B")
        s.covered["C"] = "B"
        s.warded.add("C")
        assert s.end_exchange() == 2
        assert not (s.exposed or s.defending or s.covered or s.warded)
        assert s.to_dict()["exchange"] == 2


class TestDeclareDefend:
    def test_defend_records(self, ruleset, body_character):
        s = CombatState()
        out = declare_defend(ruleset, s, body_character)
        assert "Mordai" in s.defending and out["can_attack"] is False

    def test_intercept_two_allies_needs_sentinel(self, ruleset, body_character):
        with pytest.raises(ValueError, match="Sentinel"):
            declare_defend(ruleset, CombatState(), body_character, ["A", "B"])

    def test_guardian_with_sentinel_intercepts_everyone(self, ruleset):
        g = make_character(ruleset, class_id="guardian", talent_choices={})
        s = CombatState()
        declare_defend(ruleset, s, g, ["*"])
        assert s.interceptor_for("Zahna") == "Mordai"

    def test_downed_character_cannot_defend(self, ruleset, body_character):
        body_character.status = "out"
        with pytest.raises(ValueError):
            declare_defend(ruleset, CombatState(), body_character)


class TestExpireExchangeEffects:
    def test_stunt_opening_and_study_expire(self, ruleset):
        e = foe(ruleset)
        e.openings, e.studied = ["*", "Mordai"], True
        expire_exchange_effects(e)
        assert e.openings == ["Mordai"] and e.studied is False

    def test_named_openings_persist(self, ruleset):
        e = foe(ruleset)
        e.openings = ["A", "B"]
        expire_exchange_effects(e)
        assert e.openings == ["A", "B"]

    def test_empty_is_fine(self, ruleset):
        e = foe(ruleset)
        expire_exchange_effects(e)
        assert e.openings == []


# ---------------------------------------------------------------------------
# Damage to foes
# ---------------------------------------------------------------------------

class TestApplyDamageToEnemy:
    def test_crossing_half_marks_bloodied_once(self, ruleset):
        e = foe(ruleset)                                   # 8 HP
        r = apply_damage_to_enemy(ruleset, e, 4)
        assert r.bloodied_now and r.when_bloodied == "wb" and e.hp_current == 4
        assert not apply_damage_to_enemy(ruleset, e, 1).bloodied_now

    def test_zero_hp_defeats(self, ruleset):
        e = foe(ruleset)
        r = apply_damage_to_enemy(ruleset, e, 20)
        assert r.defeated and e.hp_current == 0

    def test_boss_changes_phase_when_bloodied(self, ruleset):
        e = foe(ruleset, role="boss")                      # 40 HP
        r = apply_damage_to_enemy(ruleset, e, 20)
        assert r.phase_change and e.phase == 2

    def test_mook_drops_to_any_hit(self, ruleset):
        e = foe(ruleset, role="mook", count=3)
        r = apply_damage_to_enemy(ruleset, e, 1)
        assert r.mooks_dropped == 1 and e.count == 2 and not r.defeated

    def test_cleave_drops_several_and_defeats_the_mob(self, ruleset):
        e = foe(ruleset, role="mook", count=2)
        r = apply_damage_to_enemy(ruleset, e, 1, drops=3)
        assert r.mooks_dropped == 2 and r.defeated

    def test_negative_damage_raises(self, ruleset):
        with pytest.raises(ValueError):
            apply_damage_to_enemy(ruleset, foe(ruleset), -1)

    def test_defeated_foe_raises(self, ruleset):
        e = foe(ruleset)
        e.defeated = True
        with pytest.raises(ValueError):
            apply_damage_to_enemy(ruleset, e, 1)


# ---------------------------------------------------------------------------
# Player attacks
# ---------------------------------------------------------------------------

class TestResolveAttack:
    def test_full_success_deals_weapon_die_plus_option(self, ruleset, body_character):
        e = foe(ruleset, armor=1)
        r = resolve_attack(ruleset, body_character, e, dice=[5, 4], damage_dice=[6],
                           options=["extra_damage"], extra_damage_roll=[3])
        assert r.tier == "full_success" and r.raw_damage == 9 and r.damage == 8
        assert r.enemy_result.hp_after == 0 and r.enemy_result.defeated

    def test_partial_success_exposes_the_attacker(self, ruleset, body_character):
        s = CombatState()
        e = foe(ruleset, key="e1")
        r = resolve_attack(ruleset, body_character, e, state=s, dice=[3, 3], damage_dice=[2])
        assert r.tier == "partial_success" and r.exposed and s.is_exposed_to("Mordai", "e1")
        assert r.options == []                  # options only on a 10+

    def test_failure_is_a_miss_and_an_mm_move(self, ruleset, body_character):
        e = foe(ruleset)
        r = resolve_attack(ruleset, body_character, e, dice=[1, 2])
        assert not r.hit and r.mm_move and r.damage == 0 and e.hp_current == 8

    def test_attack_rolls_body_whatever_the_weapon(self, ruleset):
        s = scout(ruleset)
        r = resolve_attack(ruleset, s, foe(ruleset), dice=[4, 3], damage_dice=[1])
        assert r.roll.stat == "body" and r.roll.stat_value == 2

    def test_level_gap_makes_it_hard(self, ruleset, body_character):
        r = resolve_attack(ruleset, body_character, foe(ruleset, level=4), dice=[4, 3],
                           damage_dice=[1])
        assert r.difficulty == "Hard" and r.roll.total == 8

    def test_opening_eases_and_is_used_up(self, ruleset, body_character):
        e = foe(ruleset)
        e.openings = ["Mordai"]
        r = resolve_attack(ruleset, body_character, e, dice=[3, 2], damage_dice=[1])
        assert r.opening_used and r.difficulty == "Easy" and e.openings == []

    def test_stunt_opens_the_foe_for_allies(self, ruleset, body_character):
        e = foe(ruleset, role="boss")
        resolve_attack(ruleset, body_character, e, dice=[6, 5], damage_dice=[1],
                       options=["stunt"])
        assert "*" in e.openings

    def test_unknown_option_raises(self, ruleset, body_character):
        with pytest.raises(ValueError, match="Unknown option"):
            resolve_attack(ruleset, body_character, foe(ruleset), options=["decapitate"])

    def test_two_options_need_improved_weapon_master(self, ruleset, body_character):
        with pytest.raises(ValueError, match="at most 1"):
            resolve_attack(ruleset, body_character, foe(ruleset),
                           options=["extra_damage", "stunt"])

    def test_improved_weapon_master_with_its_kind_picks_two(self, ruleset, body_character):
        body_character.talent("weapon_master").improved = True
        body_character.equipped_weapon().kind = "blades"
        assert options_allowed(ruleset, body_character) == 2
        r = resolve_attack(ruleset, body_character, foe(ruleset, role="boss"), dice=[6, 5],
                           damage_dice=[5], options=["extra_damage", "stunt"],
                           extra_damage_roll=[2])
        assert r.options == ["extra_damage", "stunt"] and r.weapon_die == 10

    def test_sparks_are_debited(self, ruleset, body_character):
        resolve_attack(ruleset, body_character, foe(ruleset), sparks=2, dice=[1, 1, 6, 6],
                       damage_dice=[1])
        assert body_character.sparks == 1

    def test_more_sparks_than_held_raises(self, ruleset, body_character):
        with pytest.raises(ValueError):
            resolve_attack(ruleset, body_character, foe(ruleset), sparks=5)

    def test_downed_attacker_raises(self, ruleset, body_character):
        body_character.hp_current = 0
        with pytest.raises(ValueError):
            resolve_attack(ruleset, body_character, foe(ruleset))

    def test_level_damage_bonus_is_added(self, ruleset, body_character):
        body_character.level = 6
        r = resolve_attack(ruleset, body_character, foe(ruleset, role="boss"), dice=[4, 3],
                           damage_dice=[3])
        assert r.damage_bonus == 2 and r.raw_damage == 5

    def test_apply_false_leaves_the_foe_alone(self, ruleset, body_character):
        e = foe(ruleset)
        r = resolve_attack(ruleset, body_character, e, dice=[5, 5], damage_dice=[8], apply=False)
        assert r.damage == 8 and e.hp_current == 8 and body_character.sparks == 3


class TestAttackTalents:
    def test_marksman_pierces_armor_and_ignores_cover(self, ruleset):
        s = scout(ruleset)
        e = foe(ruleset, armor=2, role="boss")
        r = resolve_attack(ruleset, s, e, in_cover=True, dice=[4, 3], damage_dice=[5])
        assert r.difficulty == "Standard" and r.damage == 4        # 5 - (2-1)

    def test_cover_makes_ranged_attacks_hard_without_marksman(self, ruleset, body_character):
        body_character.inventory.append(
            __import__("app.game.character", fromlist=["InventoryItem"]).InventoryItem(
                id="longbow", name="Longbow", weapon="ranged", kind="bows"))
        body_character.equipped["weapon"] = "longbow"
        r = resolve_attack(ruleset, body_character, foe(ruleset), in_cover=True, dice=[4, 3],
                           damage_dice=[1])
        assert r.difficulty == "Hard"

    def test_deadeye_rolls_the_weapon_die_twice_on_a_ranged_ten(self, ruleset):
        s = scout(ruleset)
        s.signature = "deadeye"
        r = resolve_attack(ruleset, s, foe(ruleset, role="boss"), dice=[6, 5],
                           damage_dice=[4, 5])
        assert r.damage_dice == [4, 5] and r.raw_damage == 9

    def test_brawler_hit_is_also_a_stunt(self, ruleset):
        b = make_character(ruleset, class_id="brawler", talent_choices={})
        e = foe(ruleset, role="boss")
        r = resolve_attack(ruleset, b, e, brawling=True, dice=[4, 3], damage_dice=[2])
        assert "stunt" in r.options and "*" in e.openings

    def test_cleave_improved_drops_three_mooks_on_a_ten(self, ruleset, body_character):
        body_character.talents.append(TalentState(id="cleave", improved=True))
        e = foe(ruleset, role="mook", count=5)
        r = resolve_attack(ruleset, body_character, e, dice=[6, 5], damage_dice=[1])
        assert r.enemy_result.mooks_dropped == 3 and e.count == 2

    def test_anatomist_ignores_armor_on_a_studied_foe(self, ruleset, body_character):
        body_character.signature = "anatomist"
        e = foe(ruleset, armor=2, role="boss")
        e.studied = True
        r = resolve_attack(ruleset, body_character, e, dice=[3, 3], damage_dice=[5])
        assert r.damage == 5


# ---------------------------------------------------------------------------
# Enemy attacks
# ---------------------------------------------------------------------------

class TestResolveEnemyAttack:
    def test_hit_deals_damage_minus_armor(self, ruleset):
        z = make_caster(ruleset)                            # armor 1, 6 HP
        e = foe(ruleset, level=3)                           # attack +2, damage 6
        r = resolve_enemy_attack(ruleset, e, z, dice=[3, 3])
        assert r.tier == "partial_success" and r.damage == 5 and z.hp_current == 1

    def test_hard_hit_adds_two(self, ruleset, body_character):
        e = foe(ruleset, level=3)
        r = resolve_enemy_attack(ruleset, e, body_character, dice=[5, 4])
        assert r.tier == "full_success" and r.raw_damage == 8 and r.damage == 5

    def test_miss_deals_nothing(self, ruleset, body_character):
        r = resolve_enemy_attack(ruleset, foe(ruleset), body_character, dice=[2, 3])
        assert not r.hit and r.damage == 0 and body_character.hp_current == 16

    def test_defend_makes_it_hard(self, ruleset, body_character):
        s = CombatState()
        s.defend("Mordai")
        r = resolve_enemy_attack(ruleset, foe(ruleset), body_character, state=s, dice=[3, 3])
        assert r.difficulty == "Hard" and r.total == 6 and not r.hit

    def test_hard_sources_do_not_stack(self, ruleset, body_character):
        r = resolve_enemy_attack(ruleset, foe(ruleset), body_character, defending=True,
                                 cover=True, warded=True, dice=[4, 4])
        assert r.difficulty_modifier == -1

    def test_exposure_adds_a_die_and_is_consumed(self, ruleset, body_character):
        s = CombatState()
        s.expose("Mordai", "e1")
        e = foe(ruleset, key="e1")
        r = resolve_enemy_attack(ruleset, e, body_character, state=s, dice=[1, 6, 5])
        assert r.exposure_die and r.kept == [6, 5] and not s.is_exposed_to("Mordai", "e1")

    def test_natural_two_opens_the_foe_to_its_target(self, ruleset, body_character):
        e = foe(ruleset, level=10)
        r = resolve_enemy_attack(ruleset, e, body_character, dice=[1, 1])
        assert r.natural_low and not r.hit and e.openings == ["Mordai"]

    def test_natural_twelve_always_hits_hard(self, ruleset, body_character):
        r = resolve_enemy_attack(ruleset, foe(ruleset), body_character, defending=True,
                                 dice=[6, 6])
        assert r.natural_high and r.tier == "full_success"

    def test_mob_adds_damage(self, ruleset):
        z = make_caster(ruleset)
        e = foe(ruleset, role="mook", count=4)              # damage 3, +3
        r = resolve_enemy_attack(ruleset, e, z, dice=[4, 4])
        assert r.mob_bonus == 3 and r.raw_damage == 6

    def test_intercept_redirects_to_the_guard(self, ruleset, body_character):
        z = make_caster(ruleset)
        s = CombatState()
        s.defend("Mordai", ["Zahna"])
        r = resolve_enemy_attack(ruleset, foe(ruleset, level=3), z, state=s,
                                 party={"Mordai": body_character, "Zahna": z}, dice=[5, 3])
        assert r.target == "Mordai" and r.original_target == "Zahna"
        assert r.difficulty == "Hard"                       # the guard is Defending
        assert z.hp_current == 6 and body_character.hp_current == 13

    def test_damage_to_zero_reports_the_drop(self, ruleset):
        z = make_caster(ruleset)
        r = resolve_enemy_attack(ruleset, foe(ruleset, level=10), z, dice=[5, 5])
        assert r.target_result["dropped"] and z.hp_current == 0

    def test_defeated_foe_raises(self, ruleset, body_character):
        e = foe(ruleset)
        e.defeated = True
        with pytest.raises(ValueError):
            resolve_enemy_attack(ruleset, e, body_character)

    def test_wrong_dice_count_raises(self, ruleset, body_character):
        with pytest.raises(ValueError):
            resolve_enemy_attack(ruleset, foe(ruleset), body_character, exposed=True,
                                 dice=[3, 3])

    def test_apply_false_does_not_hurt(self, ruleset, body_character):
        r = resolve_enemy_attack(ruleset, foe(ruleset, level=5), body_character, dice=[6, 5],
                                 apply=False)
        assert r.hit and body_character.hp_current == 16


class TestMorale:
    def test_over_morale_breaks(self, ruleset):
        e = foe(ruleset, morale=7)
        r = morale_check(ruleset, e, dice=[4, 4])
        assert r.breaks and e.broken and r.breaks_text == "b"

    def test_equal_to_morale_holds(self, ruleset):
        r = morale_check(ruleset, foe(ruleset, morale=8), dice=[4, 4])
        assert not r.breaks

    def test_fearless_never_breaks(self, ruleset):
        r = morale_check(ruleset, foe(ruleset, morale=12), bonus=2, dice=[6, 6])
        assert r.fearless and not r.breaks

    def test_dread_presence_bonus_counts(self, ruleset):
        assert morale_check(ruleset, foe(ruleset, morale=9), bonus=2, dice=[4, 4]).breaks

    def test_defeated_foe_raises(self, ruleset):
        e = foe(ruleset)
        e.defeated = True
        with pytest.raises(ValueError):
            morale_check(ruleset, e)

    def test_bad_dice_raise(self, ruleset):
        with pytest.raises(ValueError):
            morale_check(ruleset, foe(ruleset), dice=[3])

    def test_triggers_from_the_ruleset(self, ruleset):
        assert combat.morale_triggers(ruleset) == [
            "first_to_fall", "half_down", "leader_down", "lone_and_hurt"]
