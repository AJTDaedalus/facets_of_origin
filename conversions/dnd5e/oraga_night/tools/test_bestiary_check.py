"""Tests for the checks T3.4 added to bestiary_check.py (Kovaun's CR line, the Wept's
attacks per turn, and the XP/PB printed on every CR line).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q
"""
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import bestiary_check as BC  # noqa: E402

WEPT_BASE = """
**CR** 11 (XP 7,200; PB +4)

**Traits**

***She Arrives.*** {arrives}

**Actions**

***Multiattack.*** The Wept makes two Strength Like a Fact attacks.
"""


def _blocks():
    return BC.split_blocks(BC.BESTIARY.read_text(encoding="utf-8"))


# attacks_per_turn ---------------------------------------------------------------

def test_attacks_per_turn_extra_trait_attack_counts():
    blk = WEPT_BASE.format(arrives="When she uses Shadow-Step, she can make one Strength "
                                   "Like a Fact attack immediately after she arrives.")
    assert BC.attacks_per_turn(blk) == 3


def test_attacks_per_turn_counts_toward_adds_nothing():
    blk = WEPT_BASE.format(arrives="When she uses Shadow-Step, she can make one of her "
                                   "Multiattack's two attacks at once on arrival. That "
                                   "attack counts toward her Multiattack that turn.")
    assert BC.attacks_per_turn(blk) == 2


def test_attacks_per_turn_no_multiattack_is_one():
    assert BC.attacks_per_turn("**Traits**\n\n***Calm.*** Nothing.\n\n**Actions**\n") == 1


def test_attacks_per_turn_wrapped_trait_text_is_read():
    blk = WEPT_BASE.format(arrives="When she uses Shadow-Step, she can\nmake one Strength "
                                   "Like a Fact\nattack on arrival.")
    assert BC.attacks_per_turn(blk) == 3


# fixed_value_problems -----------------------------------------------------------

def test_fixed_values_clean_on_the_module():
    assert BC.fixed_value_problems(_blocks()) == []


def test_fixed_values_catch_kovaun_reverted():
    blocks = _blocks()
    blocks["Damaris Kovaun"] = blocks["Damaris Kovaun"].replace(
        "**CR** 1/2 (XP 100; PB +2)", "**CR** 1 (XP 200; PB +2)")
    probs = BC.fixed_value_problems(blocks)
    assert any("Damaris Kovaun: text CR line" in p for p in probs)


def test_fixed_values_catch_wrong_xp_for_cr():
    blocks = _blocks()
    blocks["Tavva"] = blocks["Tavva"].replace("(XP 450; PB +2)", "(XP 400; PB +2)")
    probs = BC.fixed_value_problems(blocks)
    assert any(p.startswith("Tavva: CR 2 prints XP 400") for p in probs)


def test_fixed_values_catch_a_third_wept_attack():
    blocks = _blocks()
    blocks["The Wept"] = blocks["The Wept"].replace("counts toward", "is added to")
    probs = BC.fixed_value_problems(blocks)
    assert any("The Wept: 3 attacks per turn" in p for p in probs)


def test_fixed_values_missing_wept_block_is_reported():
    blocks = _blocks()
    del blocks["The Wept"]
    assert any("The Wept: block not found" in p for p in BC.fixed_value_problems(blocks))


# main ---------------------------------------------------------------------------

def test_main_exits_zero_on_the_module():
    with pytest.raises(SystemExit) as e:
        BC.main(["--quiet"])
    assert e.value.code == 0


def test_main_exits_one_on_a_reverted_text(tmp_path):
    bad = tmp_path / "10.md"
    bad.write_text(BC.BESTIARY.read_text(encoding="utf-8").replace(
        "**CR** 1/2 (XP 100; PB +2)", "**CR** 1 (XP 200; PB +2)"), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        BC.main(["--quiet", "--file", str(bad)])
    assert e.value.code == 1


# T4.4: SRD 5.2.1 layout (Gear line, folded Initiative) ----------------------------

def _blk(ac_line, gear=None):
    g = f"**Gear** {gear}\n" if gear else ""
    return f"{ac_line}\n**HP** 22 (4d8 + 4)\n\n**Skills** Athletics +4\n{g}**Senses** Passive Perception 10\n"


def test_parse_gear_reads_the_items():
    assert BC.parse_gear(_blk("**AC** 16 · **Initiative** +1 (11)", "Chain Shirt, Shield, Longsword")) == \
        ["Chain Shirt", "Shield", "Longsword"]


def test_parse_gear_none_when_absent():
    assert BC.parse_gear(_blk("**AC** 11 · **Initiative** +1 (11)")) == []


def test_gear_armor_gives_the_printed_ac():
    # Bought Blade: Dex 13 (+1); Chain Shirt 13 + 1 + Shield 2 = 16
    blk = _blk("**AC** 16 · **Initiative** +1 (11)", "Chain Shirt, Shield, Longsword")
    assert BC.layout_problems({"Bought Blade": blk}) == []


def test_gear_armor_ac_mismatch_is_reported():
    blk = _blk("**AC** 16 · **Initiative** +1 (11)", "Chain Shirt, Longsword")
    probs = BC.layout_problems({"Bought Blade": blk})
    assert any("Bought Blade: Gear gives AC 14" in p for p in probs)


def test_ac_with_armor_in_parentheses_is_reported():
    blk = _blk("**AC** 16 (Chain Shirt, Shield) · **Initiative** +1 (11)")
    probs = BC.layout_problems({"Bought Blade": blk})
    assert any("Bought Blade: AC line carries a parenthetical" in p for p in probs)


def test_parse_initiative_reads_bonus_and_score():
    assert BC.parse_initiative("**AC** 11 · **Initiative** +1 (16)") == (1, 16, False)


def test_parse_initiative_flags_the_2014_suffix():
    assert BC.parse_initiative("**AC** 11 · **Initiative** +1 (11), with Advantage") == (1, 11, True)


def test_initiative_advantage_folded_is_clean():
    # Pellin Corro has Advantage on Initiative: score = 10 + 1 + 5
    blk = _blk("**AC** 11 · **Initiative** +1 (16)")
    assert BC.layout_problems({"Pellin Corro": blk}) == []


def test_initiative_advantage_suffix_is_reported():
    blk = _blk("**AC** 11 · **Initiative** +1 (11), with Advantage")
    probs = BC.layout_problems({"Pellin Corro": blk})
    assert any("Pellin Corro: Initiative" in p and "fold" in p for p in probs)


def test_initiative_advantage_not_folded_is_reported():
    blk = _blk("**AC** 11 · **Initiative** +1 (11)")
    probs = BC.layout_problems({"Pellin Corro": blk})
    assert any("Pellin Corro: Initiative score 11, expected 16" in p for p in probs)


def test_initiative_score_without_advantage_is_ten_plus_bonus():
    blk = _blk("**AC** 16 · **Initiative** +1 (12)", "Chain Shirt, Shield")
    probs = BC.layout_problems({"Bought Blade": blk})
    assert any("Bought Blade: Initiative score 12, expected 11" in p for p in probs)


def test_initiative_bonus_must_come_from_dex_and_pb():
    # Dex +1, PB +2: +1, +3 or +5 are possible; +2 is not
    blk = _blk("**AC** 16 · **Initiative** +2 (12)", "Chain Shirt, Shield")
    probs = BC.layout_problems({"Bought Blade": blk})
    assert any("Bought Blade: Initiative bonus +2" in p for p in probs)


def test_layout_clean_on_the_module():
    assert BC.layout_problems(_blocks()) == []


# T9 final review: trait save DCs read from the text (NEW-BESTIARY-1) ---------------

def test_trait_dc_clean_on_the_module():
    assert BC.trait_dc_problems(_blocks()) == []


def test_trait_dc_catches_put_aside_at_14():
    blocks = _blocks()
    blocks["The Attendant"] = blocks["The Attendant"].replace(
        "*Strength Saving Throw:* DC 15", "*Strength Saving Throw:* DC 14")
    probs = BC.trait_dc_problems(blocks)
    assert any("Attendant: Put Aside DC 14 vs 8+3+4 = 15" in p for p in probs)


def test_trait_dc_reads_a_wrapped_trait():
    blocks = _blocks()
    blocks["The Attendant"] = blocks["The Attendant"].replace(
        "*Strength Saving Throw:* DC 15", "*Strength Saving Throw:*\nDC 15")
    assert BC.trait_dc_problems(blocks) == []


def test_trait_dc_missing_trait_is_reported():
    blocks = _blocks()
    blocks["The Attendant"] = blocks["The Attendant"].replace("***Put Aside", "***Set Aside")
    assert any("Put Aside not found" in p for p in BC.trait_dc_problems(blocks))


def test_trait_dc_data_agrees():
    assert (15, 0) in BC.B["Attendant"]["dc"]


# R1.4 (review P1-7, owner QR3): the Nastier variants the cards field are named blocks --

PROMOTED = ["Veteran Bought Sergeant", "Boranis Cousin of 3160", "Veteran Draunel Duelist"]


def test_promoted_variants_are_full_blocks_in_data():
    for name in PROMOTED:
        assert name in BC.B, name
        assert name not in BC.VARIANT_OF, name
        assert BC.PROMOTED[name] in BC.TEXT_NAME.values() or BC.PROMOTED[name] in BC.B


def test_promoted_variants_have_blocks_in_the_text():
    blocks = _blocks()
    for name in PROMOTED:
        assert name in blocks, name


def test_variant_problems_clean_on_the_module():
    assert BC.variant_problems(_blocks()) == []


def test_variant_missing_block_is_reported():
    blocks = _blocks()
    del blocks["Veteran Bought Sergeant"]
    assert any("Veteran Bought Sergeant: no block" in p for p in BC.variant_problems(blocks))


def test_variant_missing_card_line_is_reported():
    blocks = _blocks()
    blocks["Boranis Cousin of 3160"] = blocks["Boranis Cousin of 3160"].replace("**Nastier.**", "**Meaner.**")
    assert any("Boranis Cousin of 3160: no Nastier line" in p for p in BC.variant_problems(blocks))


def test_base_nastier_must_point_to_the_variant():
    blocks = _blocks()
    blocks["Draunel Duelist"] = blocks["Draunel Duelist"].replace("Veteran Draunel Duelist", "a better duelist")
    assert any("Draunel Duelist: Nastier line does not name Veteran Draunel Duelist" in p
               for p in BC.variant_problems(blocks))


def test_base_nastier_must_not_reprint_the_variant_numbers():
    blocks = _blocks()
    blocks["Bought Sergeant"] = blocks["Bought Sergeant"].replace(
        "**Nastier.**", "**Nastier.** CR 4 (XP 1,100), 78 HP (12d8 + 24).")
    assert any("Bought Sergeant: Nastier line reprints numbers" in p for p in BC.variant_problems(blocks))


def test_variant_text_numbers_checked_like_any_block(tmp_path):
    bad = tmp_path / "10.md"
    bad.write_text(BC.BESTIARY.read_text(encoding="utf-8").replace(
        "**HP** 78 (12d8 + 24)", "**HP** 80 (12d8 + 24)"), encoding="utf-8")
    probs = BC.text_problems(bad.read_text(encoding="utf-8"))
    assert any(p.startswith("Veteran Bought Sergeant: text HP") for p in probs)


# R6.2 (review 2, N7): S1's principal is a named variant line, not the kinsmen's Nastier --

PRINCIPAL = "Kinsman principal (variant)"


def test_principal_is_a_variant_not_a_nastier_line():
    assert PRINCIPAL in BC.B
    assert not any("(Nastier)" in k for k in BC.B)
    assert BC.VARIANT_OF[PRINCIPAL] == ("Feuding Kinsman", "Variant: the principal")


def test_kinsman_nastier_line_no_longer_carries_the_principal():
    line = BC._card_line(_blocks()["Feuding Kinsman"], "Nastier")
    assert line and "HP (" not in line and "principal" in line


def test_variant_line_problems_clean_on_the_module():
    text = BC.BESTIARY.read_text(encoding="utf-8")
    assert not [p for p in BC.text_problems(text) if PRINCIPAL in p]


def test_variant_line_missing_is_reported():
    text = BC.BESTIARY.read_text(encoding="utf-8").replace("**Variant: the principal.**", "**A principal.**")
    assert any(f"{PRINCIPAL}: variant line not found" in p for p in BC.text_problems(text))


def test_variant_line_wrong_hp_is_reported():
    text = BC.BESTIARY.read_text(encoding="utf-8").replace("22 HP (4d8 + 4)", "24 HP (4d8 + 4)")
    assert any(f"{PRINCIPAL}: text HP/HD" in p for p in BC.text_problems(text))


def test_variant_line_wrong_cr_is_reported():
    text = BC.BESTIARY.read_text(encoding="utf-8")
    i = text.index("**Variant: the principal.**")
    j = text.index("CR 1/8", i)
    text = text[:j] + "CR 1/4" + text[j + 6:]
    assert any(f"{PRINCIPAL}: text CR 1/4" in p for p in BC.text_problems(text))
