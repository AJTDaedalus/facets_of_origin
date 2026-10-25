"""WP6 guards (three-player pass): T6.2 rule 2, T6.7 live cards, T6.17 / TP57 one level, and the
other WP6 facts. Each guard: it fires on the old wording, is clean on the new, and the real
chapters pass."""
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import fact_check as F  # noqa: E402


@pytest.fixture(scope="module")
def facts():
    return F.load_facts(F.FACTS)


def _hits(facts, fid, text, fname):
    return [h for h in F.check_text(text, fname, facts) if h.fact == fid]


def _req(facts, fid, fname, text, tmp_path):
    (tmp_path / fname).write_text(text, encoding="utf-8")
    fact = next(f for f in facts if f["id"] == fid)
    checks = [c for c in fact["checks"] if c["type"] == "require" and c["file"] == fname]
    assert checks, f"{fid} has no require on {fname}"
    return [h for c in checks for h in F._require(fact, dict(c, file=fname), tmp_path)]


def _real(facts, fid):
    root = TOOLS.parent
    out = []
    for p in sorted(root.glob("*.md")):
        if p.name in F.EXCLUDE:
            continue
        out += _hits(facts, fid, p.read_text(encoding="utf-8"), p.name)
    return out


class TestRiskDialRuleTwo:
    def test_old_rule_two_is_forbidden(self, facts):
        text = ("2. **Every fight is visible and optional.** No snake ambushes a character, and no\n"
                "   snake is the reason a character dies before midnight.\n")
        assert len(_hits(facts, "risk_dial", text, "09_The_Snakes.md")) == 2

    def test_one_or_two_lines_is_forbidden(self, facts):
        text = "*Optional; show one or two, then let them be.*\n"
        assert _hits(facts, "risk_dial", text, "04_The_Ball.md")

    def test_new_wording_is_clean(self, facts):
        text = ("2. **Every ambush is foreshadowed.** No snake moves on a character whose tell the\n"
                "   table has not been shown. *Optional; show one, then let them be.*\n")
        assert not _hits(facts, "risk_dial", text, "09_The_Snakes.md")

    def test_rule_missing_is_a_hit(self, facts, tmp_path):
        text = "## The Snakes at the Ball\n\n2. **Every fight is visible and optional.**\n"
        assert _req(facts, "risk_dial", "09_The_Snakes.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "risk_dial")


class TestOneLevel:
    """TP57: the Gentle / Sharp / Merciless dial is cut."""

    def test_dial_cells_are_forbidden(self, facts):
        text = ("At **Gentle**, no snake finishes anyone. At **Merciless**, a snake finishes whoever\n"
                "crossed it.\n")
        assert len(_hits(facts, "one_level", text, "05_The_Longest_Night.md")) == 2

    def test_sharp_as_a_setting_is_forbidden(self, facts):
        for text in ("At Sharp it strikes a fallen creature only if it interfered.\n",
                     "That is the Sharp setting, the one the book is written at.\n",
                     "**Tonight's setting:** ☐ one ☐ two\n",
                     "That holds at every setting of the dial.\n"):
            assert _hits(facts, "one_level", text, "09_The_Snakes.md"), text

    def test_plain_rule_is_clean(self, facts):
        text = ("A snake at heat 4 finishes a downed character who crossed it. The edge was sharp,\n"
                "and the dials of the clock stood still.\n")
        assert not _hits(facts, "one_level", text, "05_The_Longest_Night.md")

    def test_conditional_say_it_is_a_hit(self, facts, tmp_path):
        text = ("## Down, Not Out\n\n**Everyone else's steel.**\n\n**Say it when the lights die** "
                "(at Sharp or Merciless): *\"From here on the knives are real.\"*\n")
        assert _req(facts, "one_level", "05_The_Longest_Night.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "one_level")

    def test_head_text_fires(self, facts):
        """The guard fires on the pre-TP57 text of chapter V (git HEAD), if git is available."""
        import subprocess
        try:
            old = subprocess.run(["git", "show", "HEAD:conversions/dnd5e/oraga_night/05_The_Longest_Night.md"],
                                 cwd=TOOLS, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            pytest.skip("git not available")
        if "Gentle" not in old:
            pytest.skip("HEAD already carries TP57")
        assert _hits(facts, "one_level", old, "05_The_Longest_Night.md")


class TestDefaultLiveCards:
    """T6.7: S11 and S12 live by default; the Circle starts at heat 2."""

    def test_one_card_default_is_forbidden(self, facts):
        text = ("Maiven goes east whatever her heat. So by default **one** card is live in the dark —\n"
                "S11, the Phern door — plus the gate.\n")
        assert _hits(facts, "default_live_cards", text, "09_The_Snakes.md")

    def test_old_do_nothing_heats_are_forbidden(self, facts):
        text = "**If the table does nothing,** midnight arrives with the Circle at 2, the Church at 2.\n"
        assert _hits(facts, "default_live_cards", text, "08_Handouts.md")

    def test_new_wording_is_clean(self, facts):
        text = ("midnight arrives like this: the Circle at 3, the Church at 2. So by default **two**\n"
                "cards are live in the dark: S11 and S12.\n")
        assert not _hits(facts, "default_live_cards", text, "09_The_Snakes.md")

    def test_circle_starting_at_one_is_a_hit(self, facts, tmp_path):
        text = ("**Table IX–2: The Snake Tracker**\n\n| **The Circle** ☐☐☐☐ | 1 | x |\n\n"
                "**If the table does nothing at all**, by default **two** cards are live in the dark.\n")
        got = _req(facts, "default_live_cards", "09_The_Snakes.md", text, tmp_path)
        assert any("Circle" in h.match for h in got)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "default_live_cards")
