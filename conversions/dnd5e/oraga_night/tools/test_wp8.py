"""WP8 guards (three-player pass): each fires on the old wording, is clean on the new, and the
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


class TestGalleryGeometry:
    def test_old_guard_change_view_fires(self, facts):
        text = ("The slingers are no longer walking to the east wing corridor; they are watching "
                "the guard change on it from the gallery rail.\n")
        assert _hits(facts, "gallery_geometry", text, "04_The_Ball.md")

    def test_old_table_row_fires(self, facts):
        text = "| III | Maiven petitions. The slingers watch the guard change from the gallery rail | x | — |\n"
        assert _hits(facts, "gallery_geometry", text, "09_The_Snakes.md")

    def test_old_gallery_walk_fires(self, facts):
        text = "Behind her, the slingers walk the gallery toward the east wing as far as the cleared corridor.\n"
        assert _hits(facts, "gallery_geometry", text, "04_The_Ball.md")

    def test_new_wording_is_clean(self, facts):
        text = ("The slingers are no longer walking to the east wing corridor; they are timing "
                "the guard change on its doors instead. Behind her, the slingers go out by the east "
                "doors and up the stair as far as the cleared corridor.\n")
        assert not _hits(facts, "gallery_geometry", text, "04_The_Ball.md")

    @pytest.mark.parametrize("fname,text", [
        ("05_The_Longest_Night.md", "- *The Crystal Court (B2)* is about 140 feet long.\n"),
        ("04_The_Ball.md", "The banquet is called, and the galleries fill.\n"),
        ("09_The_Snakes.md", "## S11. The Phern Door\n\na service door on the gallery side.\n"),
    ])
    def test_missing_lines_are_hits(self, facts, tmp_path, fname, text):
        assert _req(facts, "gallery_geometry", fname, text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "gallery_geometry")


class TestSecondFloor:
    def test_second_floor_above_the_galleries_fires(self, facts):
        text = "Raunu's study is on the second floor, above the galleries.\n"
        assert _hits(facts, "second_floor", text, "04_The_Ball.md")

    def test_gallery_level_second_floor_is_clean(self, facts):
        text = ("The banquet galleries and the east wing are at gallery level, 12 feet up: the second "
                "floor.\n")
        assert not _hits(facts, "second_floor", text, "05_The_Longest_Night.md")

    @pytest.mark.parametrize("fname,text", [
        ("05_The_Longest_Night.md", "- **Elevations.** The galleries are 12 feet up. Raunu's study (B8) "
                                    "is on the second floor.\n"),
        ("09_The_Snakes.md", "## S10. Over the Wall\n\n- *The wall* is 20 feet of grown crystal.\n"),
    ])
    def test_missing_lines_are_hits(self, facts, tmp_path, fname, text):
        assert _req(facts, "second_floor", fname, text, tmp_path)

    def test_real_chapters_are_clean(self, facts):
        assert not _real(facts, "second_floor")
