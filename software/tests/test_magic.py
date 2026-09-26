"""Tests for casting (app/game/magic.py)."""
import pytest

from app.game.magic import plan_cast, resolve_cast
from tests.conftest import make_caster, make_character, make_enemy

SIG = "A sealing glyph"


class TestPlanScopes:
    def test_minor_is_standard_and_free(self, ruleset, caster):
        p = plan_cast(ruleset, caster, domain="inscription", scope="minor")
        assert p.ok and (p.difficulty, p.fatigue, p.stat) == ("Standard", 0, "mind")

    def test_significant_costs_one(self, ruleset, caster):
        p = plan_cast(ruleset, caster, domain="inscription", scope="significant")
        assert (p.difficulty, p.fatigue) == ("Standard", 1)

    def test_major_is_hard_two_and_needs_level_three(self, ruleset, caster):
        assert not plan_cast(ruleset, caster, domain="inscription", scope="major").ok
        caster.level = 3
        p = plan_cast(ruleset, caster, domain="inscription", scope="major")
        assert p.ok and (p.difficulty, p.fatigue) == ("Hard", 2)

    def test_unknown_scope_or_domain(self, ruleset, caster):
        assert not plan_cast(ruleset, caster, domain="inscription", scope="epic").ok
        assert not plan_cast(ruleset, caster, domain="nope", scope="minor").ok

    def test_domain_not_held(self, ruleset, caster):
        assert not plan_cast(ruleset, caster, domain="warding", scope="minor").ok

    def test_non_caster_cannot_cast(self, ruleset, body_character):
        assert not plan_cast(ruleset, body_character, domain="fire", scope="minor").ok


class TestPlanSteps:
    def test_signature_is_one_step_easier(self, ruleset, caster):
        p = plan_cast(ruleset, caster, domain="inscription", scope="significant", working=SIG)
        assert p.signature and p.difficulty == "Easy"

    def test_signature_can_be_forced_off(self, ruleset, caster):
        p = plan_cast(ruleset, caster, domain="inscription", scope="significant",
                      working=SIG, signature=False)
        assert p.difficulty == "Standard"

    def test_non_signature_working_is_standard(self, ruleset, caster):
        p = plan_cast(ruleset, caster, domain="inscription", scope="significant",
                      working="Something else")
        assert not p.signature and p.difficulty == "Standard"

    def test_wider_domain_harder_until_improved(self, ruleset, caster):
        assert caster.level_up(ruleset, kind="talent", talent_id="wider_domain",
                               choice="warding") == []
        assert plan_cast(ruleset, caster, domain="warding", scope="significant").difficulty == "Hard"
        caster.talent("wider_domain").improved = True
        assert plan_cast(ruleset, caster, domain="warding",
                         scope="significant").difficulty == "Standard"

    def test_prismatic_always_harder(self, ruleset, caster):
        caster.magic.domains.append("chronomancy")
        caster.level_up(ruleset, kind="talent", talent_id="wider_domain", choice="warding")
        caster.talent("wider_domain").improved = True
        assert plan_cast(ruleset, caster, domain="chronomancy",
                         scope="significant").difficulty == "Hard"

    def test_heavy_armor_adds_fatigue_to_full_workings_only(self, ruleset, caster):
        caster.equipped["armor"] = "heavy"
        assert plan_cast(ruleset, caster, domain="inscription", scope="significant").fatigue == 2
        assert plan_cast(ruleset, caster, domain="inscription", scope="minor").fatigue == 0

    def test_arcane_mastery_cheapens_its_working(self, ruleset, caster):
        caster.level = 3
        caster.signature, caster.arcane_mastery_working = "arcane_mastery", SIG
        assert plan_cast(ruleset, caster, domain="inscription", scope="significant",
                         working=SIG).fatigue == 0
        assert plan_cast(ruleset, caster, domain="inscription", scope="significant",
                         working="A warning rune").fatigue == 1

    def test_improved_casting_reduction_once_per_scene(self, ruleset, caster):
        assert not plan_cast(ruleset, caster, domain="inscription", scope="significant",
                             reduce_fatigue=True).ok        # not improved
        caster.talent("thaumaturgy").improved = True
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         reduce_fatigue=True, dice=[5, 5])
        assert r.fatigue_paid == 0 and caster.fatigue == 0
        assert not plan_cast(ruleset, caster, domain="inscription", scope="significant",
                             reduce_fatigue=True).ok        # spent this scene
        caster.reset_uses(ruleset, "scene")
        assert plan_cast(ruleset, caster, domain="inscription", scope="significant",
                         reduce_fatigue=True).ok

    def test_miracle(self, ruleset, caster):
        caster.level = 3
        assert not plan_cast(ruleset, caster, domain="inscription", scope="major",
                             miracle=True).ok               # no Miracle signature
        caster.signature = "miracle"
        assert not plan_cast(ruleset, caster, domain="inscription", scope="significant",
                             miracle=True).ok               # Major only
        r = resolve_cast(ruleset, caster, domain="inscription", scope="major",
                         miracle=True, dice=[6, 5])
        assert r.fatigue_paid == 0
        assert not plan_cast(ruleset, caster, domain="inscription", scope="major",
                             miracle=True).ok               # spent this session

    def test_no_free_slot_no_full_working(self, ruleset, caster):
        caster.fatigue = caster.slots_free(ruleset)
        assert not plan_cast(ruleset, caster, domain="inscription", scope="significant").ok
        assert plan_cast(ruleset, caster, domain="inscription", scope="minor").ok


class TestGift:
    def gifted(self, valloh_ruleset):
        return make_character(valloh_ruleset, lineage="orthaen", gift_domain="inscription")

    def test_gift_minor_cast_with_soul_for_free(self, valloh_ruleset):
        p = plan_cast(valloh_ruleset, self.gifted(valloh_ruleset),
                      domain="inscription", scope="minor")
        assert p.ok and p.gift and p.stat == "soul" and p.fatigue == 0

    def test_gift_is_minor_only(self, valloh_ruleset):
        p = plan_cast(valloh_ruleset, self.gifted(valloh_ruleset),
                      domain="inscription", scope="significant")
        assert not p.ok and any("Minor" in e for e in p.errors)

    def test_gift_rolls_soul(self, valloh_ruleset):
        ch = self.gifted(valloh_ruleset)
        r = resolve_cast(valloh_ruleset, ch, domain="inscription", scope="minor", dice=[3, 3])
        assert r.roll.stat == "soul" and r.roll.total == 7

    def test_ungifted_cannot_use_the_gift(self, valloh_ruleset):
        ch = self.gifted(valloh_ruleset)
        ch.gifted = False
        assert not plan_cast(valloh_ruleset, ch, domain="inscription", scope="minor").ok


class TestResolve:
    def test_full_success_pays_fatigue(self, ruleset, caster):
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         dice=[5, 4])
        assert r.outcome == "full_success" and caster.fatigue == 1
        assert r.complication_options == [] and r.mishap is None

    def test_partial_offers_two_complications(self, ruleset, caster):
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         dice=[3, 3])
        assert r.outcome == "partial_success"
        assert r.complication_table == "magic_complications"
        assert len(r.complication_options) == 2
        assert r.complication_options[0]["entry_roll"] != r.complication_options[1]["entry_roll"]

    def test_failure_mishap_and_graceful_fail_still_pays(self, ruleset, caster):
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         dice=[1, 2])
        assert r.outcome == "failure" and r.graceful_fail_applies
        assert r.mishap["table"] == "magic_mishaps" and caster.fatigue == 1

    def test_plan_errors_raise(self, ruleset, caster):
        with pytest.raises(ValueError):
            resolve_cast(ruleset, caster, domain="warding", scope="minor")

    def test_sparks_debited_and_overspend_raises(self, ruleset, caster):
        r = resolve_cast(ruleset, caster, domain="inscription", scope="minor",
                         sparks=1, dice=[1, 1, 6])
        assert r.roll.kept == [6, 1] and caster.sparks == 2
        with pytest.raises(ValueError):
            resolve_cast(ruleset, caster, domain="inscription", scope="minor", sparks=5)

    def test_downed_caster_cannot_cast(self, ruleset, caster):
        caster.status = "out"
        with pytest.raises(ValueError):
            resolve_cast(ruleset, caster, domain="inscription", scope="minor")

    def test_apply_false_changes_nothing(self, ruleset, caster):
        resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                     dice=[5, 5], apply=False)
        assert caster.fatigue == 0


class TestHarm:
    def test_harm_damage_minus_armor(self, ruleset, caster):
        foe = make_enemy(armor=1).spawn(ruleset)
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         intent="harm", enemy=foe, dice=[5, 5], damage_dice=[5])
        assert (r.raw_damage, r.damage) == (5, 4) and foe.hp_current == 4

    def test_level_damage_bonus_applies(self, ruleset, caster):
        caster.level = 3
        r = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         intent="harm", dice=[5, 5], damage_dice=[5])
        assert r.damage_bonus == 1 and r.raw_damage == 6

    def test_minor_and_misses_deal_no_damage(self, ruleset, caster):
        r1 = resolve_cast(ruleset, caster, domain="inscription", scope="minor",
                          intent="harm", dice=[6, 5])
        r2 = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                          intent="harm", dice=[1, 2])
        r3 = resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                          intent="ward", dice=[6, 5])
        assert r1.damage == r2.damage == r3.damage == 0

    def test_major_group_rolled_once_minus_each_armor(self, ruleset, caster):
        caster.level = 3
        foes = [make_enemy(id="a", armor=0).spawn(ruleset, key="a"),
                make_enemy(id="b", armor=2).spawn(ruleset, key="b")]
        r = resolve_cast(ruleset, caster, domain="inscription", scope="major",
                         intent="harm", enemies=foes, dice=[6, 5], damage_dice=[4, 4])
        assert r.raw_damage == 9
        assert [x["damage"] for x in r.enemy_results] == [9, 7]
        assert [f.hp_current for f in foes] == [0, 1]

    def test_group_needs_a_group_scope(self, ruleset, caster):
        foes = [make_enemy().spawn(ruleset)]
        with pytest.raises(ValueError):
            resolve_cast(ruleset, caster, domain="inscription", scope="significant",
                         intent="harm", enemies=foes, dice=[6, 5], damage_dice=[4])

    def test_group_without_apply_only_reports(self, ruleset, caster):
        caster.level = 3
        foes = [make_enemy(armor=1).spawn(ruleset)]
        r = resolve_cast(ruleset, caster, domain="inscription", scope="major", intent="harm",
                         enemies=foes, dice=[6, 5], damage_dice=[2, 2], apply=False)
        assert r.enemy_results[0]["damage"] == 4 and foes[0].hp_current == 8


def test_to_dict_is_json_safe(ruleset, caster):
    import json
    r = resolve_cast(ruleset, caster, domain="inscription", scope="significant", dice=[3, 3])
    json.dumps(r.to_dict())
