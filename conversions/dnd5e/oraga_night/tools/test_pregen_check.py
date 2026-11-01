"""Tests for the focus check T3.5 added to pregen_check.py (CAST-11: Andra's crystal is
listed as her arcane focus, in her Spellcasting line and in her Carrying line).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q
"""
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import pregen_check as PC  # noqa: E402

ANDRA = """## Andra Tessarin

**Spellcasting** (Intelligence; save DC 14, attack +6; {spell})

**Carrying.** Dagger · the lattice · {carry} · 40 GP · Inspiration

---

## Dassa

**Carrying.** Longsword
"""

# O16: SRD 5.2.1 Title-Cases equipment and focus names ("Arcane Focus").
GOOD_SPELL = "a crystal as Arcane Focus"
GOOD_CARRY = "crystal (Arcane Focus)"


def _text():
    return PC.PREGENS.read_text(encoding="utf-8")


# focus_issues -------------------------------------------------------------------

def test_focus_clean_on_the_module():
    assert PC.focus_issues(_text()) == []


def _andra(probs):
    return [p for p in probs if p[0] == "Andra"]


def test_focus_clean_on_a_minimal_sheet():
    assert _andra(PC.focus_issues(ANDRA.format(spell=GOOD_SPELL, carry=GOOD_CARRY))) == []


def test_focus_missing_from_carrying_is_reported():
    probs = PC.focus_issues(ANDRA.format(spell=GOOD_SPELL, carry="jeweler's tools"))
    assert ("Andra", "focus not carried", None, GOOD_CARRY) in probs


def test_focus_lattice_as_focus_is_reported():
    probs = PC.focus_issues(ANDRA.format(spell="the lattice as focus", carry=GOOD_CARRY))
    assert any(p[0] == "Andra" and p[1] == "spellcasting focus" for p in probs)


def test_focus_line_wrapped_across_lines_is_read():
    text = ANDRA.format(spell="a crystal as\nArcane Focus", carry="crystal\n(Arcane Focus)")
    assert _andra(PC.focus_issues(text)) == []


# Q16b (2026-10-05): Ilesse's warding crystal is her Holy Symbol.
def test_focus_ilesse_holy_symbol_on_the_module():
    assert [p for p in PC.focus_issues(_text()) if p[0] == "Ilesse"] == []


def test_focus_ilesse_plain_focus_is_reported():
    text = _text().replace("warding crystal as\nHoly Symbol", "warding crystal as\nfocus")
    assert any(p[0] == "Ilesse" and p[1] == "spellcasting focus" for p in PC.focus_issues(text))


def test_focus_ilesse_holy_symbol_not_carried_is_reported():
    text = _text().replace("warding crystal (Holy Symbol)", "crystal focus")
    assert ("Ilesse", "focus not carried", None, "warding crystal (Holy Symbol)") in PC.focus_issues(text)


def test_focus_lowercase_name_is_reported():
    # O16: the 2014-style lowercase "arcane focus" no longer passes.
    probs = PC.focus_issues(ANDRA.format(spell="a crystal as arcane focus",
                                         carry="crystal (arcane focus)"))
    assert any(p[1] == "spellcasting focus" for p in probs)
    assert any(p[1] == "focus not carried" for p in probs)


def test_focus_missing_section_is_reported():
    assert ("Andra", "section missing in text", None, None) in PC.focus_issues("## Dassa\n")


def test_focus_carrying_of_another_pregen_does_not_count():
    text = ANDRA.format(spell=GOOD_SPELL, carry="jeweler's tools").replace(
        "**Carrying.** Longsword", "**Carrying.** Longsword · crystal (Arcane Focus)")
    assert any(p[1] == "focus not carried" for p in PC.focus_issues(text))


# main ---------------------------------------------------------------------------

def test_main_exits_zero_on_the_module():
    with pytest.raises(SystemExit) as e:
        PC.main(["--quiet"])
    assert e.value.code == 0


def test_main_exits_one_when_the_focus_is_dropped(tmp_path):
    bad = tmp_path / "11.md"
    bad.write_text(_text().replace("crystal (Arcane Focus)", "crystal"), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        PC.main(["--quiet", "--file", str(bad)])
    assert e.value.code == 1


# --------------------------------------------------------------------------- 2014 rules
# REVIEW2 S5: the 2014 rewrite of pregen_check gets its own red/green tests.

import copy

TEXT = PC.PREGENS.read_text(encoding="utf-8")


@pytest.fixture
def pcs(monkeypatch):
    data = copy.deepcopy(PC.PCs)
    monkeypatch.setattr(PC, "PCs", data)
    return data


def _issues(kind):
    return [i for i in PC.legality_issues(lambda *a, **k: None) if i[1] == kind]


def test_legality_clean_on_the_module():
    assert PC.legality_issues(lambda *a, **k: None) == []


def test_bard_cantrip_count_is_three_in_2014(pcs):
    pcs["Serane"]["cantrips"].append("light")
    assert _issues("cantrips") == [("Serane", "cantrips", 4, 3)]


def test_bard_knows_seven_spells_in_2014(pcs):
    pcs["Serane"]["known"].pop()
    assert _issues("spells known") == [("Serane", "spells known", 6, 7)]


def test_cleric_prepared_is_wisdom_plus_level(pcs):
    pcs["Ilesse"]["prep"].pop()
    assert _issues("prepared") == [("Ilesse", "prepared", 7, 8)]


def test_wizard_spellbook_is_six_plus_two_per_level(pcs):
    pcs["Andra"]["book2"].pop()
    assert _issues("spellbook") == [("Andra", "spellbook", 11, 12)]


def test_scores_must_come_from_array_human_and_asi(pcs):
    pcs["Serane"]["final"]["CHA"] = 19
    assert [i[0] for i in _issues("abilities")] == ["Serane"]


def test_jack_of_all_trades_adds_to_initiative(pcs):
    pcs["Serane"]["printed"]["init"] = 2
    assert ("Serane", "init", 3, 2) in PC.legality_issues(lambda *a, **k: None)


def test_text_clean_on_the_module():
    assert PC.text_issues(TEXT) == []


def test_text_skill_drift_is_caught():
    bad = TEXT.replace("**Skills** Persuasion +8, Deception +6", "**Skills** Persuasion +9, Deception +6", 1)
    assert ("Serane", "text skill Persuasion", "9", 8) in PC.text_issues(bad)


def test_text_skill_not_in_data_is_caught():
    bad = TEXT.replace("Insight +4, Perception +4,", "Insight +4, Perception +4, Arcana +1,", 1)
    assert any(i[0] == "Pello" and i[1] == "text skill Arcana" for i in PC.text_issues(bad))


def test_text_saving_throws_drift_is_caught():
    bad = TEXT.replace("**Saving Throws** Str +6, Con +4", "**Saving Throws** Str +6, Con +5", 1)
    assert ("Dassa", "text saves", "Str +6, Con +5", "Str +6, Con +4") in PC.text_issues(bad)


def test_text_spell_dc_drift_is_caught():
    bad = TEXT.replace("(Wisdom; save DC 14, attack +6;", "(Wisdom; save DC 13, attack +6;", 1)
    assert any(i[0] == "Ilesse" and i[1] == "text spell dc/atk" for i in PC.text_issues(bad))
