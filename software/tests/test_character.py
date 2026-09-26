"""Tests for the Lean Facets v1.0 character model (app/game/character.py)."""
from pathlib import Path

import pytest
import yaml

from app.game.character import (
    Character, CharacterFormatError, InventoryItem, MagicState, TalentState,
    create_character, planned_signature, roll_starting_coin,
)
from tests.conftest import make_caster, make_character

REPO = Path(__file__).resolve().parents[2]


def soul_char(ruleset, **kw):
    kw.setdefault("name", "Wren")
    return make_character(ruleset, facet="soul", second_stat="mind", class_id="wanderer",
                          background_id="luck_touched_wanderer", talent_choices={}, **kw)


def custom(ruleset, facet, talents, second="soul", **kw):
    ch, errors = create_character(
        ruleset, name=kw.pop("name", "Custom"), player_name="P", facet=facet,
        second_stat=second if second != facet else "mind",
        custom_class={"name": "Odd", "concept": "I am odd.", "knack": "Oddity",
                      "talents": talents, "kit": kw.pop("kit", ["rope"])},
        background_id="hedge_scholar", coin=0, **kw)
    assert not errors, errors
    return ch


# ---------------------------------------------------------------------------
# create_character
# ---------------------------------------------------------------------------

class TestCreatePreset:
    def test_warrior_preset_stats_knacks_and_kit(self, ruleset):
        ch = make_character(ruleset)
        assert ch.stats == {"body": 2, "mind": 0, "soul": 1}
        assert ch.knacks == ["Soldiering", "City Watch Veteran"]
        assert [t.id for t in ch.talents] == ["weapon_master", "tough"]
        assert ch.talent("weapon_master").choice == "blades"
        assert ch.equipped == {"weapon": "standard_weapon", "armor": "heavy", "shield": True}
        assert ch.hp_current == 16 and ch.sparks == 3 and ch.coin == 40

    def test_second_stat_cannot_be_the_facet_stat(self, ruleset):
        ch, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                      second_stat="body", class_id="guardian",
                                      background_id="dockworker")
        assert ch is None and errors

    def test_preset_of_another_facet_is_refused(self, ruleset):
        ch, errors = create_character(ruleset, name="X", player_name="X", facet="mind",
                                      second_stat="soul", class_id="guardian",
                                      background_id="dockworker")
        assert ch is None and any("body class" in e for e in errors)

    def test_unknown_facet_and_class(self, ruleset):
        assert create_character(ruleset, name="X", player_name="X", facet="heart",
                                second_stat="soul", class_id="warrior")[0] is None
        assert create_character(ruleset, name="X", player_name="X", facet="body",
                                second_stat="soul", class_id="nope")[0] is None

    def test_no_class_at_all_is_refused(self, ruleset):
        ch, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                      second_stat="soul", background_id="dockworker")
        assert ch is None and errors

    def test_preset_and_custom_together_is_refused(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="body", second_stat="soul",
            class_id="guardian", background_id="dockworker",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["tough", "athlete"]})
        assert any("not both" in e for e in errors)

    def test_weapon_master_needs_a_kind(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="warrior",
                                     background_id="dockworker")
        assert any("Weapon Master" in e for e in errors)

    def test_starting_coin_rolled_when_unspecified(self, ruleset, rng):
        ch, _ = create_character(ruleset, name="X", player_name="X", facet="body",
                                 second_stat="soul", class_id="guardian",
                                 background_id="dockworker", rng=rng)
        assert 20 <= ch.coin <= 120 and ch.coin % 10 == 0

    def test_negative_coin_refused(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", coin=-5)
        assert errors


class TestCreateCustom:
    def test_custom_class_and_background(self, ruleset):
        ch, errors = create_character(
            ruleset, name="Zulnut", player_name="Z", facet="body", second_stat="soul",
            custom_class={"name": "Wandering Disciple", "concept": "I move.",
                          "knack": "Motion", "talents": ["unarmored_discipline", "athlete"],
                          "kit": ["rope"], "signature": "ghost"},
            custom_background={"name": "Pilgrim", "knack": "Roads", "specialty": "Shrines."},
            coin=0)
        assert not errors
        assert ch.custom_class and ch.class_signature == "ghost"
        assert ch.class_talents == ["unarmored_discipline", "athlete"]
        assert ch.knacks == ["Motion", "Roads"] and ch.specialty == "Shrines."
        assert planned_signature(ruleset, ch) == "ghost"

    def test_custom_class_needs_name_concept_knack(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="body", second_stat="soul",
            custom_class={"name": "", "concept": "", "knack": "",
                          "talents": ["tough", "athlete"]}, background_id="dockworker")
        assert len([e for e in errors if "custom class" in e]) == 3

    def test_custom_class_talents_from_own_menu_only(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="body", second_stat="soul",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["tough", "linguist"]}, background_id="dockworker")
        assert any("Linguist" in e for e in errors)

    def test_custom_class_needs_two_different_talents(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="body", second_stat="soul",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["tough", "tough"]}, background_id="dockworker")
        assert any("2 different talents" in e for e in errors)

    def test_custom_signature_must_be_a_facet_signature(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="body", second_stat="soul",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["tough", "athlete"], "signature": "miracle"},
            background_id="dockworker")
        assert any("miracle" in e for e in errors)

    def test_custom_background_needs_its_parts(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     custom_background={"name": "a", "knack": "",
                                                        "specialty": ""})
        assert any("custom background" in e for e in errors)

    def test_both_backgrounds_or_none_refused(self, ruleset):
        _, e1 = create_character(ruleset, name="X", player_name="X", facet="body",
                                 second_stat="soul", class_id="guardian")
        _, e2 = create_character(ruleset, name="X", player_name="X", facet="body",
                                 second_stat="soul", class_id="guardian",
                                 background_id="dockworker",
                                 custom_background={"name": "a", "knack": "b", "specialty": "c"})
        assert e1 and e2

    def test_unknown_background_refused(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="nope")
        assert errors

    def test_kit_overflow_is_refused(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", kit=["heavy_armor"] * 7)
        assert any("Kit" in e for e in errors)

    def test_kit_with_unknown_item_refused(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", kit=["laser"])
        assert any("laser" in e for e in errors)


class TestCreateLineageAndMagic:
    def test_gifted_lineage_adds_knack_and_domain(self, valloh_ruleset):
        ch = make_character(valloh_ruleset, lineage="orthaen", gift_domain="inscription")
        assert ch.gifted and ch.gift_domain == "inscription"
        assert ch.knacks[-1] == "Orthaen gift"

    def test_ungifted_member_of_gifted_lineage(self, valloh_ruleset):
        ch = make_character(valloh_ruleset, lineage="orthaen", gifted=False)
        assert not ch.gifted and ch.gift_domain is None
        assert "Orthaen gift" not in ch.knacks

    def test_gifted_lineage_without_domain_refused(self, valloh_ruleset):
        _, errors = create_character(valloh_ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", lineage="orthaen")
        assert any("domain" in e for e in errors)

    def test_prismatic_gift_domain_refused(self, valloh_ruleset):
        _, errors = create_character(valloh_ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", lineage="orthaen",
                                     gift_domain="chronomancy")
        assert any("prismatic" in e for e in errors)

    def test_gift_on_human_refused(self, ruleset):
        _, e1 = create_character(ruleset, name="X", player_name="X", facet="body",
                                 second_stat="soul", class_id="guardian",
                                 background_id="dockworker", gifted=True)
        _, e2 = create_character(ruleset, name="X", player_name="X", facet="body",
                                 second_stat="soul", class_id="guardian",
                                 background_id="dockworker", gift_domain="fire")
        assert e1 and e2

    def test_unknown_lineage_refused(self, ruleset):
        _, errors = create_character(ruleset, name="X", player_name="X", facet="body",
                                     second_stat="soul", class_id="guardian",
                                     background_id="dockworker", lineage="orthaen")
        assert any("orthaen" in e for e in errors)

    def test_caster_gets_magic_block(self, ruleset):
        ch = make_caster(ruleset)
        assert ch.magic.tradition == "thaumaturgy"
        assert ch.magic.domains == ["inscription"]
        assert len(ch.magic.signature_workings) == 2

    def test_caster_domain_must_be_own_tradition_and_not_prismatic(self, ruleset):
        for dom in ("fire", "chronomancy"):
            _, errors = create_character(
                ruleset, name="Z", player_name="Z", facet="mind", second_stat="soul",
                class_id="thaumaturge", background_id="guild_apprentice",
                magic={"domain": dom, "signature_workings": ["a", "b"]})
            assert errors, dom

    def test_caster_needs_two_workings_and_non_caster_no_magic(self, ruleset):
        _, e1 = create_character(ruleset, name="Z", player_name="Z", facet="mind",
                                 second_stat="soul", class_id="thaumaturge",
                                 background_id="guild_apprentice",
                                 magic={"domain": "inscription", "signature_workings": ["a"]})
        _, e2 = create_character(ruleset, name="Z", player_name="Z", facet="body",
                                 second_stat="soul", class_id="guardian",
                                 background_id="dockworker",
                                 magic={"domain": "inscription", "signature_workings": ["a", "b"]})
        assert e1 and e2

    def test_wider_domain_at_creation(self, ruleset):
        ch = custom(ruleset, "mind", ["thaumaturgy", "wider_domain"],
                    talent_choices={"wider_domain": "warding"},
                    magic={"domain": "inscription", "signature_workings": ["a", "b"]})
        assert ch.magic.domains == ["inscription", "warding"]

    def test_wider_domain_bad_choice(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="mind", second_stat="soul",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["thaumaturgy", "wider_domain"]},
            background_id="hedge_scholar", talent_choices={"wider_domain": "fire"},
            magic={"domain": "inscription", "signature_workings": ["a", "b"]})
        assert any("Wider Domain" in e for e in errors)

    def test_wider_domain_without_caster_refused(self, ruleset):
        _, errors = create_character(
            ruleset, name="X", player_name="X", facet="mind", second_stat="soul",
            custom_class={"name": "a", "concept": "b", "knack": "c",
                          "talents": ["loremaster", "wider_domain"]},
            background_id="hedge_scholar")
        assert any("requires" in e for e in errors)


def test_roll_starting_coin_is_2d6_times_10(ruleset, rng):
    values = {roll_starting_coin(ruleset, rng) for _ in range(200)}
    assert min(values) >= 20 and max(values) <= 120
    assert all(v % 10 == 0 for v in values)


# ---------------------------------------------------------------------------
# Derived numbers
# ---------------------------------------------------------------------------

class TestHP:
    def test_level_one_is_grit_max_plus_body_plus_tough(self, ruleset):
        assert make_character(ruleset).hp_max(ruleset) == 16
        assert make_caster(ruleset).hp_max(ruleset) == 6

    def test_levels_without_recorded_gains_use_average(self, ruleset):
        ch = make_caster(ruleset)
        ch.level = 3
        assert ch.hp_max(ruleset) == 6 + 4 + 4

    def test_recorded_gains_are_used(self, ruleset):
        ch = make_character(ruleset)
        ch.level, ch.hp_gains = 3, [1, 10]
        assert ch.hp_max(ruleset) == 16 + 11

    def test_hp_never_below_one(self, ruleset):
        ch = make_caster(ruleset)
        ch.stats["body"] = -20
        assert ch.hp_max(ruleset) == 1

    def test_unknown_facet_raises(self, ruleset):
        ch = make_caster(ruleset)
        ch.facet = "heart"
        with pytest.raises(ValueError):
            ch.hp_max(ruleset)


class TestSlots:
    def test_total_used_free(self, ruleset):
        ch = make_character(ruleset)
        assert ch.slots_total(ruleset) == 12
        assert ch.slots_used(ruleset) == 6
        assert ch.slots_free(ruleset) == 6

    def test_wounds_fatigue_and_coin_fill_slots(self, ruleset):
        ch = make_character(ruleset)
        ch.add_wound("Cut")
        ch.fatigue = 1
        ch.coin = 250
        assert ch.slots_used(ruleset) == 6 + 1 + 1 + 2
        assert ch.coin_slots(ruleset) == 2

    def test_iron_lungs_adds_two(self, ruleset):
        ch = custom(ruleset, "body", ["iron_lungs", "athlete"])
        assert ch.slots_total(ruleset) == 10 + 2 + 2

    def test_items_to_drop_when_over(self, ruleset):
        ch = make_character(ruleset)
        assert ch.items_to_drop(ruleset) == 0
        for i in range(8):
            ch.add_wound(f"w{i}")
        assert ch.items_to_drop(ruleset) == 2


class TestArmorAndWeapon:
    def test_heavy_plus_shield_is_capped_at_three(self, ruleset):
        assert make_character(ruleset).armor_value(ruleset) == 3

    def test_light_plus_shield(self, ruleset):
        ch = make_character(ruleset)
        ch.equipped["armor"] = "light"
        assert ch.armor_value(ruleset) == 2

    def test_no_armor_is_zero(self, ruleset):
        ch = make_character(ruleset)
        ch.equipped.update(armor="none", shield=False)
        assert ch.armor_value(ruleset) == 0

    def test_unarmored_discipline_and_improved(self, ruleset):
        ch = make_character(ruleset, facet="body", class_id="brawler",
                            background_id="arena_fighter", talent_choices={})
        assert ch.armor_value(ruleset) == 1
        ch.talent("unarmored_discipline").improved = True
        assert ch.armor_value(ruleset) == 2
        ch.equipped["shield"] = True
        assert ch.armor_value(ruleset) == 1      # a shield ends the discipline

    def test_weapon_master_steps_the_chosen_kind(self, ruleset):
        ch = make_character(ruleset)
        assert ch.weapon_die(ruleset) == 8        # kit weapon has no kind
        ch.equipped_weapon().kind = "blades"
        assert ch.weapon_die(ruleset) == 10
        ch.equipped_weapon().kind = "blunt"
        assert ch.weapon_die(ruleset) == 8

    def test_unarmed_and_improved_unarmored(self, ruleset):
        ch = make_character(ruleset, facet="body", class_id="brawler",
                            background_id="arena_fighter", talent_choices={})
        assert ch.weapon_die(ruleset) == 6       # light weapon
        ch.equipped["weapon"] = None
        assert ch.weapon_die(ruleset) == 4
        ch.talent("unarmored_discipline").improved = True
        assert ch.weapon_die(ruleset) == 8

    def test_equipped_weapon_not_carried_is_none(self, ruleset):
        ch = make_character(ruleset)
        ch.equipped["weapon"] = "longbow"
        assert ch.equipped_weapon() is None and not ch.is_ranged(ruleset)

    def test_ranged(self, ruleset):
        ch = make_character(ruleset, facet="body", class_id="scout",
                            background_id="wilderness_scout", talent_choices={})
        assert ch.is_ranged(ruleset)

    def test_damage_bonus_by_level(self, ruleset):
        ch = make_character(ruleset)
        got = []
        for lvl in (1, 2, 3, 5, 6, 9, 10):
            ch.level = lvl
            got.append(ch.damage_bonus(ruleset))
        assert got == [0, 0, 1, 1, 2, 3, 3]


# ---------------------------------------------------------------------------
# Sparks and talent uses
# ---------------------------------------------------------------------------

class TestSparks:
    def test_spend_and_earn(self, ruleset):
        ch = make_character(ruleset)
        assert ch.spend_spark(2) == 1
        assert ch.earn_spark() == 2

    def test_spend_more_than_held_raises(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.spend_spark(4)

    def test_zero_spend_or_earn_raises(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.spend_spark(0)
        with pytest.raises(ValueError):
            ch.earn_spark(0)

    def test_start_session_resets_without_carry_over(self, ruleset):
        ch = soul_char(ruleset)
        ch.sparks = 9
        ch.use_talent(ruleset, "lucky")
        ch.start_session(ruleset)
        assert ch.sparks == 3 and ch.uses_remaining(ruleset, "lucky") == 1


class TestTalentUses:
    def test_once_per_scene_then_spent(self, ruleset):
        ch = soul_char(ruleset)
        assert ch.use_talent(ruleset, "hunch") == 0
        with pytest.raises(ValueError):
            ch.use_talent(ruleset, "hunch")

    def test_improved_twice(self, ruleset):
        ch = soul_char(ruleset)
        ch.talent("hunch").improved = True
        assert ch.uses_remaining(ruleset, "hunch") == 2

    def test_lucky_rerolls_from_effects(self, ruleset):
        ch = soul_char(ruleset)
        assert ch.uses_remaining(ruleset, "lucky") == 1
        ch.talent("lucky").improved = True
        assert ch.uses_remaining(ruleset, "lucky") == 2

    def test_passive_untracked(self, ruleset):
        ch = make_character(ruleset)
        assert ch.use_talent(ruleset, "tough") is None
        assert ch.uses_remaining(ruleset, "tough") is None

    def test_not_held_or_unknown_raises(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.use_talent(ruleset, "hunch")
        with pytest.raises(ValueError):
            ch.uses_remaining(ruleset, "nope")

    def test_explicit_period_for_improved_ability(self, ruleset):
        ch = make_character(ruleset)
        assert ch.use_talent(ruleset, "tough", period="scene") == 0
        with pytest.raises(ValueError):
            ch.use_talent(ruleset, "tough", period="scene")
        with pytest.raises(ValueError):
            ch.use_talent(ruleset, "tough", period="week")

    def test_reset_scene_rest_session(self, ruleset):
        ch = soul_char(ruleset)
        ch.use_talent(ruleset, "hunch")
        ch.use_talent(ruleset, "lucky")
        ch.reset_uses(ruleset, "scene")
        assert ch.uses_remaining(ruleset, "hunch") == 1
        assert ch.uses_remaining(ruleset, "lucky") == 0
        ch.reset_uses(ruleset, "rest")
        assert ch.uses_remaining(ruleset, "lucky") == 0
        ch.reset_uses(ruleset, "session")
        assert ch.uses_remaining(ruleset, "lucky") == 1

    def test_rest_resets_once_per_rest(self, ruleset):
        ch = custom(ruleset, "mind", ["alchemist", "linguist"])
        ch.use_talent(ruleset, "alchemist")
        ch.reset_uses(ruleset, "session")
        assert ch.uses_remaining(ruleset, "alchemist") == 0
        ch.reset_uses(ruleset, "rest")
        assert ch.uses_remaining(ruleset, "alchemist") == 1

    def test_reset_unknown_period_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).reset_uses(ruleset, "year")


# ---------------------------------------------------------------------------
# Damage, dying, rest
# ---------------------------------------------------------------------------

class TestDamage:
    def test_take_damage(self, ruleset):
        ch = make_character(ruleset)
        r = ch.take_damage(ruleset, 5)
        assert r["hp_after"] == 11 and not r["dropped"]

    def test_damage_floors_at_zero(self, ruleset):
        ch = make_character(ruleset)
        r = ch.take_damage(ruleset, 99)
        assert r["hp_after"] == 0 and r["dropped"]

    def test_negative_damage_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).take_damage(ruleset, -1)

    def test_unstoppable_once_per_scene(self, ruleset):
        ch = make_character(ruleset)
        ch.signature, ch.level = "unstoppable", 3
        assert ch.take_damage(ruleset, 99)["unstoppable_used"]
        assert ch.hp_current == 1
        assert ch.take_damage(ruleset, 5)["hp_after"] == 0

    def test_heal(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_current, ch.status = 0, "out"
        assert ch.heal(ruleset, 100) == 16 and ch.status == "ok"

    def test_heal_errors(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.heal(ruleset, -1)
        ch.status = "dead"
        with pytest.raises(ValueError):
            ch.heal(ruleset, 1)


class TestWounds:
    def test_add_and_remove(self, ruleset):
        ch = make_character(ruleset)
        ch.add_wound(" Cracked ribs ")
        assert ch.wounds == [{"name": "Cracked ribs"}]
        assert ch.remove_wound() == {"name": "Cracked ribs"}

    def test_blank_wound_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).add_wound("  ")

    def test_remove_errors(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.remove_wound()
        ch.add_wound("a")
        with pytest.raises(ValueError):
            ch.remove_wound(3)


class TestHoldOn:
    def test_full_success_stands_at_one(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_current = 0
        r = ch.hold_on(ruleset, dice=[5, 4])
        assert r.outcome == "full_success" and ch.hp_current == 1 and ch.status == "ok"

    def test_partial_is_out_and_failure_dying(self, ruleset):
        ch = make_character(ruleset)
        ch.hold_on(ruleset, dice=[3, 3])
        assert ch.status == "out" and ch.hp_current == 0
        ch.hold_on(ruleset, dice=[1, 2])
        assert ch.status == "dying"

    def test_improved_tough_is_easy_and_stands_on_partial(self, ruleset):
        ch = make_character(ruleset)
        ch.talent("tough").improved = True
        r = ch.hold_on(ruleset, dice=[2, 2])        # 4 + 2 + 1 (Easy) = 7
        assert r.difficulty == "Easy" and r.outcome == "partial_success"
        assert ch.status == "ok" and ch.hp_current == 1

    def test_errors(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.hold_on(ruleset, sparks=9)
        ch.status = "dead"
        with pytest.raises(ValueError):
            ch.hold_on(ruleset)

    def test_fall_takes_a_wound_and_rolls(self, ruleset):
        ch = make_character(ruleset)
        out = ch.fall(ruleset, wound="Cracked ribs", dice=[6, 6])
        assert out["wound"] == {"name": "Cracked ribs"} and ch.status == "ok"
        assert out["items_to_drop"] == 0

    def test_fall_rolls_the_wound_table(self, ruleset, rng):
        ch = make_character(ruleset)
        out = ch.fall(ruleset, rng=rng)
        assert out["wound"]["name"] and len(ch.wounds) == 1

    def test_fall_when_dead_raises(self, ruleset):
        ch = make_character(ruleset)
        ch.status = "dead"
        with pytest.raises(ValueError):
            ch.fall(ruleset, wound="x")


class TestTendAndDeath:
    def test_tend_saves_at_zero_hp(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_current, ch.status = 0, "dying"
        assert ch.tend() == "out" and ch.hp_current == 0

    def test_field_surgeon_stands_at_one(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_current, ch.status = 0, "dying"
        assert ch.tend(field_surgeon=True) == "ok" and ch.hp_current == 1

    def test_tend_not_dying_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).tend()

    def test_scar_choice(self, ruleset):
        ch = make_character(ruleset)
        ch.status = "dying"
        out = ch.death_choice(ruleset, "scar", scar="Shoulder set wrong")
        assert out["status"] == "out" and ch.scars == [{"name": "Shoulder set wrong"}]

    def test_scar_rolled_from_table(self, ruleset, rng):
        ch = make_character(ruleset)
        ch.status = "dying"
        ch.death_choice(ruleset, "scar", rng=rng)
        assert ch.scars[0]["name"]

    def test_heroic_choice_and_errors(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.death_choice(ruleset, "heroic")
        ch.status = "dying"
        with pytest.raises(ValueError):
            ch.death_choice(ruleset, "flee")
        assert ch.death_choice(ruleset, "heroic")["status"] == "dead"


class TestRest:
    def test_breather_restores_half(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_current = 0
        assert ch.breather(ruleset) == 8

    def test_iron_lungs_improved_restores_all(self, ruleset):
        ch = custom(ruleset, "body", ["iron_lungs", "athlete"])
        ch.talent("iron_lungs").improved = True
        ch.hp_current = 1
        assert ch.breather(ruleset) == ch.hp_max(ruleset)

    def test_breather_while_dying_raises(self, ruleset):
        ch = make_character(ruleset)
        ch.status = "dying"
        with pytest.raises(ValueError):
            ch.breather(ruleset)

    def test_night_rest_clears_fatigue_one_wound_and_uses(self, ruleset):
        ch = soul_char(ruleset)
        ch.hp_current, ch.fatigue = 1, 2
        ch.add_wound("a")
        ch.add_wound("b")
        ch.use_talent(ruleset, "hunch")
        out = ch.night_rest(ruleset, wound_index=1)
        assert ch.hp_current == ch.hp_max(ruleset) and ch.fatigue == 0
        assert out["wounds_cleared"] == [{"name": "b"}] and ch.wounds == [{"name": "a"}]
        assert ch.uses_remaining(ruleset, "hunch") == 1

    def test_night_rest_with_no_wounds(self, ruleset):
        out = make_character(ruleset).night_rest(ruleset)
        assert out["wounds_cleared"] == []

    def test_night_rest_dying_or_dead_raises(self, ruleset):
        ch = make_character(ruleset)
        for st in ("dying", "dead"):
            ch.status = st
            with pytest.raises(ValueError):
                ch.night_rest(ruleset)


class TestFatigue:
    def test_add_fatigue(self, ruleset):
        ch = make_caster(ruleset)
        assert ch.add_fatigue(ruleset, 2) == 2

    def test_no_free_slot_refused(self, ruleset):
        ch = make_caster(ruleset)
        with pytest.raises(ValueError):
            ch.add_fatigue(ruleset, 6)

    def test_negative_refused(self, ruleset):
        with pytest.raises(ValueError):
            make_caster(ruleset).add_fatigue(ruleset, -1)


# ---------------------------------------------------------------------------
# Gear
# ---------------------------------------------------------------------------

def curio(n=0):
    return InventoryItem(id=f"c{n}", name=f"Charge: Thing {n}", slots=0, curio=True)


class TestItems:
    def test_add_by_id(self, ruleset):
        ch = make_character(ruleset)
        it = ch.add_item(ruleset, "lantern")
        assert it.name == "Lantern" and ch.slots_free(ruleset) == 5

    def test_add_unknown_or_too_big(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.add_item(ruleset, "laser")
        for _ in range(3):
            ch.add_item(ruleset, "heavy_armor")
        with pytest.raises(ValueError):
            ch.add_item(ruleset, "rope")

    def test_curio_limit(self, ruleset):
        ch = make_character(ruleset)
        for i in range(3):
            ch.add_item(ruleset, curio(i))
        with pytest.raises(ValueError):
            ch.add_item(ruleset, curio(9))

    def test_tinker_carries_four(self, ruleset):
        ch = custom(ruleset, "mind", ["tinker", "linguist"])
        for i in range(4):
            ch.add_item(ruleset, curio(i))
        assert ch.curio_limit(ruleset) == 4

    def test_remove_unequips(self, ruleset):
        ch = make_character(ruleset)
        ch.remove_item("standard_weapon")
        assert ch.equipped["weapon"] is None

    def test_remove_missing_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).remove_item("lantern")


class TestUsageDie:
    def test_steps_down(self, ruleset):
        ch = make_character(ruleset)
        r = ch.usage_roll(ruleset, "rations", roll=1)
        assert r["stepped_down"] and r["usage_die"] == 4

    def test_holds_on_high_roll_and_gone_at_the_end(self, ruleset):
        ch = make_character(ruleset)
        assert not ch.usage_roll(ruleset, "rations", roll=5)["stepped_down"]
        ch.usage_roll(ruleset, "rations", roll=2)
        r = ch.usage_roll(ruleset, "rations", roll=2)
        assert r["gone"] and not any(i.id == "rations" for i in ch.inventory)

    def test_random_roll(self, ruleset, rng):
        r = make_character(ruleset).usage_roll(ruleset, "rations", rng=rng)
        assert 1 <= r["roll"] <= 6

    def test_errors(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.usage_roll(ruleset, "rations", roll=7)
        with pytest.raises(ValueError):
            ch.usage_roll(ruleset, "rope")
        with pytest.raises(ValueError):
            ch.usage_roll(ruleset, "lantern")


class TestCoin:
    def test_spend_and_add(self, ruleset):
        ch = make_character(ruleset)
        assert ch.spend_coin(15) == 25
        assert ch.add_coin(5) == 30

    def test_overspend_raises(self, ruleset):
        with pytest.raises(ValueError):
            make_character(ruleset).spend_coin(41)

    def test_negative_raises(self, ruleset):
        ch = make_character(ruleset)
        with pytest.raises(ValueError):
            ch.spend_coin(-1)
        with pytest.raises(ValueError):
            ch.add_coin(-1)


# ---------------------------------------------------------------------------
# Level-up
# ---------------------------------------------------------------------------

def to_level(ruleset, ch, target):
    """Drive a Warrior up with valid picks."""
    while ch.level < target:
        nl = ch.level + 1
        kw = {}
        if nl == 3:
            kw = {"kind": "signature", "talent_id": "unstoppable"}
        else:
            menu = [t for t in ("athlete", "cleave", "brawler", "fast_hands", "sentinel",
                                "iron_lungs", "marksman", "dread_presence")
                    if not ch.has_talent(t)]
            kw = {"kind": "talent", "talent_id": menu[0]}
        if nl in (4, 8):
            kw["stat"] = "soul" if ch.stats["body"] >= 3 else "body"
        assert ch.level_up(ruleset, **kw) == []
    return ch


class TestLevelUp:
    def test_new_talent_and_average_hp(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete") == []
        assert ch.level == 2 and ch.talent("athlete").level_taken == 2
        assert ch.hp_max(ruleset) == 22 and ch.hp_current == 22

    def test_hp_roll_used_and_validated(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete", hp_roll=11)
        assert ch.level == 1
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete", hp_roll=3) == []
        assert ch.hp_gains == [3]

    def test_taking_tough_raises_current_hp_too(self, ruleset):
        ch = make_caster(ruleset)
        ch.level_up(ruleset, kind="talent", talent_id="linguist", teacher=False)
        ch2 = make_character(ruleset, facet="body", class_id="scout",
                             background_id="wilderness_scout", talent_choices={})
        ch2.level_up(ruleset, kind="talent", talent_id="tough")
        assert ch2.hp_current == ch2.hp_max(ruleset) == 10 + 2 + 6 + 4

    def test_improve(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="improve", talent_id="tough") == []
        assert ch.talent("tough").improved

    def test_improve_errors(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="improve", talent_id="athlete")
        ch.talent("tough").improved = True
        assert ch.level_up(ruleset, kind="improve", talent_id="tough")

    def test_duplicate_or_unknown_talent(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="talent", talent_id="tough")
        assert ch.level_up(ruleset, kind="talent", talent_id="nope")
        assert ch.level_up(ruleset, kind="bogus", talent_id="athlete")

    def test_signature_only_at_three(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="signature", talent_id="unstoppable")
        to_level(ruleset, ch, 2)
        assert ch.level_up(ruleset, kind="talent", talent_id="cleave")
        assert ch.level_up(ruleset, kind="signature", talent_id="miracle")
        assert ch.level_up(ruleset, kind="signature", talent_id="unstoppable") == []
        assert ch.signature == "unstoppable"

    def test_stat_at_four_and_eight(self, ruleset):
        ch = to_level(ruleset, make_character(ruleset), 3)
        assert ch.level_up(ruleset, kind="talent", talent_id="cleave")      # no stat
        assert ch.level_up(ruleset, kind="talent", talent_id="cleave", stat="body") == []
        assert ch.stats["body"] == 3
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete", stat="body")  # not 5

    def test_stat_cannot_pass_maximum(self, ruleset):
        ch = to_level(ruleset, make_character(ruleset), 7)
        assert ch.stats["body"] == 3
        assert any("maximum" in e for e in
                   ch.level_up(ruleset, kind="talent", talent_id="marksman", stat="body"))
        assert ch.level_up(ruleset, kind="talent", talent_id="marksman", stat="mind") == []

    def test_caster_names_workings_at_five(self, ruleset):
        ch = make_caster(ruleset)
        ch.level = 4
        assert ch.level_up(ruleset, kind="talent", talent_id="linguist")
        assert ch.level_up(ruleset, kind="talent", talent_id="linguist",
                           signature_working="A door that forgets") == []
        assert ch.magic.signature_workings[-1] == "A door that forgets"

    def test_off_facet_needs_a_teacher(self, ruleset):
        ch = make_character(ruleset)
        assert ch.level_up(ruleset, kind="talent", talent_id="linguist")
        assert ch.level_up(ruleset, kind="talent", talent_id="linguist", teacher=True) == []
        assert ch.talent("linguist").via_teacher

    def test_casting_talent_never_off_facet(self, ruleset):
        ch = make_character(ruleset)
        errors = ch.level_up(ruleset, kind="talent", talent_id="thaumaturgy", teacher=True)
        assert any("casting talent" in e for e in errors)

    def test_wider_domain_at_level_up(self, ruleset):
        ch = make_caster(ruleset)
        assert ch.level_up(ruleset, kind="talent", talent_id="wider_domain", choice="fire")
        assert ch.level_up(ruleset, kind="talent", talent_id="wider_domain",
                           choice="warding") == []
        assert ch.magic.domains == ["inscription", "warding"]

    def test_weapon_master_needs_kind_at_level_up(self, ruleset):
        ch = make_character(ruleset, facet="body", class_id="scout",
                            background_id="wilderness_scout", talent_choices={})
        assert ch.level_up(ruleset, kind="talent", talent_id="weapon_master")
        assert ch.level_up(ruleset, kind="talent", talent_id="weapon_master",
                           choice="bows") == []

    def test_polymath(self, ruleset):
        ch = make_caster(ruleset)
        ch.level = 2
        assert ch.level_up(ruleset, kind="signature", talent_id="polymath",
                           extra_talents=["athlete"])
        assert ch.level_up(ruleset, kind="signature", talent_id="polymath",
                           extra_talents=["athlete", "invocation"])
        assert ch.level_up(ruleset, kind="signature", talent_id="polymath",
                           extra_talents=["athlete", "hunch"]) == []
        assert ch.has_talent("athlete") and ch.has_talent("hunch")

    def test_arcane_mastery(self, ruleset):
        ch = make_caster(ruleset)
        ch.level = 2
        assert ch.level_up(ruleset, kind="signature", talent_id="arcane_mastery",
                           choice="not mine")
        assert ch.level_up(ruleset, kind="signature", talent_id="arcane_mastery",
                           choice="A warning rune") == []
        assert ch.arcane_mastery_working == "A warning rune"

    def test_arcane_mastery_requires_a_caster(self, ruleset):
        ch = make_character(ruleset, facet="mind", second_stat="soul", class_id="tactician",
                            background_id="hedge_scholar", talent_choices={})
        ch.level = 2
        assert ch.level_up(ruleset, kind="signature", talent_id="arcane_mastery")

    def test_max_level_and_dead(self, ruleset):
        ch = make_character(ruleset)
        ch.level = 10
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete")
        ch.level, ch.status = 1, "dead"
        assert ch.level_up(ruleset, kind="talent", talent_id="athlete")


class TestRespec:
    def test_can_respec_before_three(self, ruleset):
        ch = make_character(ruleset)
        assert ch.can_respec(ruleset)
        ch.level = 3
        assert not ch.can_respec(ruleset)

    def test_respec_swaps_talents(self, ruleset):
        ch = make_character(ruleset)
        assert ch.respec(ruleset, [{"id": "sentinel"}, {"id": "athlete"}]) == []
        assert [t.id for t in ch.talents] == ["sentinel", "athlete"]
        assert ch.hp_current == ch.hp_max(ruleset) == 12

    def test_respec_errors(self, ruleset):
        ch = make_character(ruleset)
        assert ch.respec(ruleset, [{"id": "sentinel"}])                       # count
        assert ch.respec(ruleset, [{"id": "sentinel"}, {"id": "linguist"}])   # menu
        assert ch.respec(ruleset, [{"id": "tough"}, {"id": "tough"}])         # dupe
        assert ch.respec(ruleset, [{"id": "tough"}, {"id": "weapon_master"}])  # choice
        ch.level = 3
        assert ch.respec(ruleset, [{"id": "sentinel"}, {"id": "athlete"}])

    def test_respec_improved_counts_as_a_pick(self, ruleset):
        ch = make_character(ruleset)
        ch.level = 2
        assert ch.respec(ruleset, [{"id": "tough", "improved": True},
                                   {"id": "athlete"}]) == []

    def test_caster_respec_keeps_magic_unless_changed(self, ruleset):
        ch = make_caster(ruleset)
        assert ch.respec(ruleset, [{"id": "thaumaturgy"}, {"id": "linguist"}]) == []
        assert ch.magic.domains == ["inscription"]
        assert ch.respec(ruleset, [{"id": "thaumaturgy"}, {"id": "linguist"}],
                         magic={"domain": "warding", "signature_workings": ["a", "b"]}) == []
        assert ch.magic.domains == ["warding"]

    def test_caster_respec_bad_magic_is_refused(self, ruleset):
        ch = make_caster(ruleset)
        assert ch.respec(ruleset, [{"id": "thaumaturgy"}, {"id": "linguist"}],
                         magic={"domain": "fire", "signature_workings": ["a", "b"]})
        assert ch.magic.domains == ["inscription"]


# ---------------------------------------------------------------------------
# Validation and serialisation
# ---------------------------------------------------------------------------

class TestValidate:
    def test_valid_character_has_no_errors(self, ruleset):
        assert make_character(ruleset).validate_against_ruleset(ruleset) == []
        assert make_caster(ruleset).validate_against_ruleset(ruleset) == []

    def test_catches_bad_fields(self, ruleset):
        ch = make_character(ruleset)
        ch.status = "zombie"
        ch.talents.append(TalentState(id="nope"))
        ch.signature = "unstoppable"          # at level 1
        ch.equipped["weapon"] = "longbow"
        errors = ch.validate_against_ruleset(ruleset)
        assert len(errors) >= 4

    def test_caster_needs_magic_block(self, ruleset):
        ch = make_caster(ruleset)
        ch.magic = None
        assert any("magic block" in e for e in ch.validate_against_ruleset(ruleset))
        ch2 = make_character(ruleset)
        ch2.magic = MagicState(tradition="thaumaturgy", domains=["inscription"])
        assert any("casting talent" in e for e in ch2.validate_against_ruleset(ruleset))

    def test_unknown_facet_short_circuits(self, ruleset):
        ch = make_character(ruleset)
        ch.facet = "heart"
        assert ch.validate_against_ruleset(ruleset) == ["Unknown Facet 'heart'."]

    def test_armor_not_carried(self, ruleset):
        ch = make_caster(ruleset)
        ch.equipped.update(armor="heavy", shield=True)
        errors = ch.validate_against_ruleset(ruleset)
        assert any("heavy" in e for e in errors) and any("shield" in e for e in errors)


class TestWarnings:
    def test_no_warnings_for_fresh_character(self, ruleset):
        assert make_character(ruleset).warnings(ruleset) == []

    def test_hp_mismatch(self, ruleset):
        ch = make_character(ruleset)
        ch.hp_max_stored = 99
        assert any("99" in w for w in ch.warnings(ruleset))

    def test_over_burdened(self, ruleset):
        ch = make_character(ruleset)
        for i in range(8):
            ch.add_wound(f"w{i}")
        assert any("Over-burdened" in w for w in ch.warnings(ruleset))


class TestFof:
    def test_round_trip(self, ruleset):
        ch = make_caster(ruleset)
        ch.add_wound("Sprain")
        ch.use_talent(ruleset, "thaumaturgy", period="scene")
        fof = ch.to_fof(ruleset.module_refs(), "sess", ruleset=ruleset)
        assert fof["fof_version"] == "1.0" and fof["session_id"] == "sess"
        back = Character.from_fof(fof, ruleset)
        assert back.to_fof(ruleset.module_refs(), "sess", ruleset=ruleset) == fof

    def test_yaml_round_trip_keeps_hp_and_magic(self, ruleset):
        ch = make_character(ruleset)
        ch.level_up(ruleset, kind="talent", talent_id="athlete", hp_roll=7)
        text = yaml.dump(ch.to_fof([], ruleset=ruleset))
        back = Character.from_fof(yaml.safe_load(text), ruleset)
        assert back.hp_max(ruleset) == ch.hp_max(ruleset) == 23
        assert back.warnings(ruleset) == []

    def test_v03_file_refused_clearly(self):
        old = {"fof_version": "0.1", "type": "character",
               "character": {"name": "Old", "primary_facet": "body",
                             "attributes": {"strength": 3}}}
        with pytest.raises(CharacterFormatError, match="v0.3"):
            Character.from_fof(old)

    def test_not_a_character_or_missing_fields(self):
        with pytest.raises(ValueError):
            Character.from_fof({"type": "enemy"})
        with pytest.raises(ValueError):
            Character.from_fof({"type": "character"})
        with pytest.raises(ValueError):
            Character.from_fof({"type": "character", "fof_version": "1.0",
                                "character": {"name": "X"}})

    @pytest.mark.parametrize("path", sorted((REPO / "characters").glob("*.fof"))
                             + sorted((REPO / "adventures" / "oraga_night" / "characters")
                                      .glob("*.fof")), ids=lambda p: p.stem)
    def test_real_character_files_load_and_validate(self, valloh_ruleset, path):
        ch = Character.from_fof(yaml.safe_load(path.read_text(encoding="utf-8")), valloh_ruleset)
        assert ch.validate_against_ruleset(valloh_ruleset) == []
        assert ch.hp_max(valloh_ruleset) == ch.hp_max_stored

    def test_there_are_eight_real_files(self):
        n = len(list((REPO / "characters").glob("*.fof"))) + len(
            list((REPO / "adventures" / "oraga_night" / "characters").glob("*.fof")))
        assert n == 8

    def test_to_client_dict(self, ruleset):
        ch = make_character(ruleset)
        bare = ch.to_client_dict()
        assert "derived" not in bare and bare["id"] == "mordai"
        full = ch.to_client_dict(ruleset)
        assert full["derived"]["hp_max"] == 16 and full["derived"]["armor"] == 3
        assert full["derived"]["slots_free"] == 6 and full["status"] == "ok"

    def test_to_client_dict_shows_status(self, ruleset):
        ch = make_character(ruleset)
        ch.status = "dying"
        assert ch.to_client_dict(ruleset)["status"] == "dying"


class TestParts:
    def test_inventory_item_from_dict_fills_from_ruleset(self, ruleset):
        it = InventoryItem.from_dict({"id": "rations"}, ruleset)
        assert it.name == "Rations" and it.usage_die == 6

    def test_inventory_item_from_ruleset_unknown(self, ruleset):
        with pytest.raises(ValueError):
            InventoryItem.from_ruleset(ruleset, "laser")

    def test_talent_state_round_trip(self):
        t = TalentState(id="x", improved=True, choice="c", level_taken=4, via_teacher=True)
        assert TalentState.from_dict(t.to_dict()) == t

    def test_magic_state_none(self):
        assert MagicState.from_dict(None) is None
