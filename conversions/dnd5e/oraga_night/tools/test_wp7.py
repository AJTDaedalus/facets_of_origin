"""WP7 guards (three-player pass): each fires on the old wording, is clean on the new, and the
real chapters pass."""
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


class TestNoHeat4Finish:
    def test_old_05_wording_fires(self, facts):
        text = ("mercies\"). A snake at heat 4 finishes a downed character who\n"
                "crossed it tonight; the rest leave the fallen where they lie.\n")
        assert _hits(facts, "no_heat4_finish", text, "05_The_Longest_Night.md")

    def test_old_09_wording_fires(self, facts):
        text = ("At heat 4 it is the deadliest card of the night, because Draunel's men finish "
                "a fallen character who crossed them.\n")
        assert len(_hits(facts, "no_heat4_finish", text, "09_The_Snakes.md")) >= 2

    def test_old_table_label_fires(self, facts):
        text = "| **S13** | x | 1,100 XP — plays Moderate, and kills at heat 4 |\n"
        assert _hits(facts, "no_heat4_finish", text, "09_The_Snakes.md")

    def test_new_wording_is_clean(self, facts):
        text = ("Nobody goes back to finish the fallen, at any heat: they leave them where they "
                "lie, because they have somewhere to be.\n")
        assert not _hits(facts, "no_heat4_finish", text, "05_The_Longest_Night.md")

    def test_missing_line_is_a_hit(self, facts, tmp_path):
        text = "**Everyone else's steel.** The snakes use the ordinary rules for dying.\n"
        assert _req(facts, "no_heat4_finish", "05_The_Longest_Night.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "no_heat4_finish")


class TestRaunuPlan:
    def test_send_away_fires(self, facts):
        text = "Raunu sends her off by boat before the bells.\n"
        assert _hits(facts, "raunu_plan", text, "04_The_Ball.md")

    def test_send_by_boat_fires(self, facts):
        text = "He meant to send Veier downriver by boat at midnight.\n"
        assert _hits(facts, "raunu_plan", text, "07_Cast_of_the_Ball.md")

    def test_plan_wording_is_clean(self, facts):
        text = ("**His plan for Veier:** keep her in the sealed east wing until the child is born. "
                "The boat is Vell's, never his.\n")
        assert not _hits(facts, "raunu_plan", text, "07_Cast_of_the_Ball.md")

    def test_missing_plan_is_a_hit(self, facts, tmp_path):
        text = "### Raunu Boranis — the Host\n\n### Veier Nolonaire — the Bride\n"
        assert len(_req(facts, "raunu_plan", "07_Cast_of_the_Ball.md", text, tmp_path)) == 2

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "raunu_plan")


class TestGardenDoors:
    def test_open_garden_doors_fire(self, facts):
        text = "At midnight the garden doors stand open on the dark terraces.\n"
        assert _hits(facts, "garden_doors", text, "05_The_Longest_Night.md")

    def test_old_trick_five_fires(self, facts):
        text = "| 5 | **Another door.** Make the crowd surge at the gallery-side service door. |\n"
        assert _hits(facts, "garden_doors", text, "05_The_Longest_Night.md")

    def test_new_wording_is_clean(self, facts):
        text = ("He holds the main doors and the garden doors, so until he turns east the floor's "
                "one open door is the gallery-side service door (card S11).\n")
        assert not _hits(facts, "garden_doors", text, "05_The_Longest_Night.md")

    def test_post_missing_is_a_hit(self, facts, tmp_path):
        text = ("***The Post.*** While the Hollow is within 10 feet of the doors he holds, no "
                "creature passes.\n")
        assert _req(facts, "garden_doors", "10_Bestiary.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "garden_doors")


class TestVellRoute:
    def test_old_route_fires(self, facts):
        text = ("Master Vell is already moving along the service passages toward the east wing, "
                "and the fastest route runs through the garden stair.\n")
        assert _hits(facts, "vell_route", text, "05_The_Longest_Night.md")

    def test_old_table_cell_fires(self, facts):
        text = "| **Vell** | — | Service passages → garden stair → the river gate (B5) |\n"
        assert _hits(facts, "vell_route", text, "08_Handouts.md")

    def test_new_route_is_clean(self, facts):
        text = ("Master Vell was at the river gate when the bells rang. From there he climbs back "
                "up through the gardens to the foot of the garden stair to meet her.\n")
        assert not _hits(facts, "vell_route", text, "05_The_Longest_Night.md")

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "vell_route")


class TestEpilogueEndings:
    def test_everyone_dreams_fires(self, facts):
        text = "> from time to time, each of you dreams of dancing — a warm hand in yours\n"
        assert _hits(facts, "epilogue_endings", text, "05_The_Longest_Night.md")

    def test_new_line_is_clean(self, facts):
        text = "> from time to time, the one she danced with dreams of dancing\n"
        assert not _hits(facts, "epilogue_endings", text, "05_The_Longest_Night.md")

    def test_table_missing_is_a_hit(self, facts, tmp_path):
        text = "### Epilogue (one-shot ending)\n\nThe fires are out by dawn.\n"
        assert _req(facts, "epilogue_endings", "05_The_Longest_Night.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "epilogue_endings")


class TestForcedWingGuards:
    def test_forced_wing_cell_missing_is_a_hit(self, facts, tmp_path):
        text = "**Table VIII–7: The Honor Guard**\n\n| The east-wing doors (B9) | Two | Four | Two, who stay |\n"
        assert _req(facts, "honor_guards", "08_Handouts.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "honor_guards")


class TestCorvalEndPoint:
    def test_old_end_point_fires(self, facts):
        text = ("Corval leaves them and goes back to the head of the service stair, to the wing's "
                "service door, and holds it for his household.\n")
        assert _hits(facts, "corval_end_point", text, "05_The_Longest_Night.md")

    def test_old_table_cell_fires(self, facts):
        text = "| **Corval** | x | then back to the head of the service stair, holding the wing's service door |\n"
        assert _hits(facts, "corval_end_point", text, "08_Handouts.md")

    def test_new_wording_is_clean(self, facts):
        text = ("Corval leaves them and leads his household out of the palace, through the kitchens "
                "and the service passages.\n")
        assert not _hits(facts, "corval_end_point", text, "05_The_Longest_Night.md")

    def test_missing_line_is_a_hit(self, facts, tmp_path):
        text = "### Minister Corval — the Majordomo\n\nHe is a guide, never a fighter.\n"
        assert _req(facts, "corval_end_point", "07_Cast_of_the_Ball.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "corval_end_point")


class TestGardenStairDoor:
    def test_open_door_at_the_half_bell_fires(self, facts):
        text = "At the half-bell the garden stair's top door is open, and the slingers walk up.\n"
        assert _hits(facts, "garden_stair_door", text, "09_The_Snakes.md")

    def test_midnight_open_is_clean(self, facts):
        text = "At midnight the household unlocks the garden stair's top door, and it stands open.\n"
        assert not _hits(facts, "garden_stair_door", text, "09_The_Snakes.md")

    def test_terrain_line_missing_is_a_hit(self, facts, tmp_path):
        text = "## S10. Over the Wall\n\n- *The wall* is 20 feet of grown crystal.\n"
        assert _req(facts, "garden_stair_door", "09_The_Snakes.md", text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "garden_stair_door")
