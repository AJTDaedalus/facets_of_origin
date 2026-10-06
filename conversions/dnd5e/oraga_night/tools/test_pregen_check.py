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

**Carrying.** Dagger · the lattice · {carry} · 40 GP · Heroic Inspiration

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
