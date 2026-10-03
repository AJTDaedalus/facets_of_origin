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
