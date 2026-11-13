"""T31-T32: the three proof recipes render, and the canon proof matches facts.yaml."""
import json
from pathlib import Path

import pytest
import yaml

from mapgen.export import render_recipe

REPO = Path(__file__).resolve().parents[3]
COURT = REPO / "conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml"
FACTS = REPO / "conversions/dnd5e/oraga_night/facts.yaml"
PROOFS = [COURT, REPO / "maps/recipes/proof_cave.map.yaml", REPO / "maps/recipes/proof_ruins.map.yaml",
          REPO / "maps/recipes/proof_cellar.map.yaml", REPO / "maps/recipes/proof_region.map.yaml"]


@pytest.fixture(scope="module")
def court(tmp_path_factory):
    out = tmp_path_factory.mktemp("court")
    r = render_recipe(COURT, out_dir=out, draft=True)
    return json.loads(Path(r["meta"]).read_text()), json.loads(Path(r["dd2vtt"]).read_text()), r


@pytest.fixture(scope="module")
def facts():
    return yaml.safe_load(FACTS.read_text())["maps"]


class TestCrystalCourtCanon:
    def test_floor_matches_facts(self, court, facts):
        m = court[0]["measures"]["court_floor"]["actual"]
        assert m["w"] == pytest.approx(facts["court"]["width"]) and m["h"] == pytest.approx(facts["court"]["length"])

    def test_aisles_match_facts(self, court, facts):
        for side in ("west_aisle", "east_aisle"):
            m = court[0]["measures"][side]["actual"]
            assert m["w"] == pytest.approx(facts["court"]["aisle_deep"])
            assert m["h"] == pytest.approx(facts["court"]["length"])

    def test_court_plus_galleries_is_terrace_width(self, court, facts):
        g = court[0]["geometry"]["ground"]
        assert g["w"] == pytest.approx(facts["terraces"]["wide"])

    def test_dais(self, court, facts):
        d = court[0]["geometry"]["dais"]
        assert d["w"] == pytest.approx(facts["court"]["dais_across"])
        # dais_from_doors: the dais's near edge is 120 ft from the main-doors wall (y = 160 in recipe space)
        assert 160 - d["bounds"][3] == pytest.approx(facts["court"]["dais_from_doors"])

    def test_musicians_gallery(self, court, facts):
        assert court[0]["geometry"]["musicians_gallery"]["h"] == pytest.approx(facts["court"]["musicians_gallery_deep"])

    def test_main_doors_width(self, court, facts):
        main = [p for p in court[0]["portals"] if p["position"][1] == pytest.approx(160)]
        assert len(main) == 1
        (x0, _), (x1, _) = main[0]["bounds"]
        assert abs(x1 - x0) == pytest.approx(facts["court"]["main_doors"])

    def test_west_doors(self, court, facts):
        west = sorted(p["position"][1] for p in court[0]["portals"] if p["position"][0] == pytest.approx(10))
        wd = facts["court"]["west_doors"]
        b4_center = 160 - (wd["b4_at"] + wd["b4_wide"] / 2)
        service_center = 160 - (wd["service_at"] + facts["service_run"]["door"] / 2)
        assert west == [pytest.approx(service_center), pytest.approx(b4_center)]

    def test_walls_enclose_floor(self, court):
        assert court[1]["line_of_sight"] and court[0]["los_length_ft"] > 2 * (120 + 140) - 60

    def test_no_light_sources_beyond_canon(self, court):
        # the palace's lights are a plot point (they die at midnight); the map invents none
        assert court[0]["lights"] == [] and court[1]["lights"] == []

    def test_east_stair_door_matches_the_svg(self, court):
        stair = [p for p in court[0]["portals"] if p["position"][0] == pytest.approx(130)]
        (x0, y0), (x1, y1) = stair[0]["bounds"]
        assert abs(y1 - y0) == pytest.approx(10)              # build_maps geometry(): east_door_w = 10

    def test_terrace_is_the_terrace_width(self, court, facts):
        assert court[0]["geometry"]["terrace"]["w"] == pytest.approx(facts["terraces"]["wide"])

    def test_fog_areas_declared(self, court):
        assert court[0]["fog_areas"] == ["court_floor", "west_aisle", "east_aisle", "garden_walk", "stairwell"]

    def test_no_props_beyond_canon(self, court):
        assert not (set(court[0]["legend"]) - {"door", "double_door", "stairs"})


@pytest.mark.parametrize("recipe", PROOFS[1:], ids=lambda p: p.stem)
def test_generic_proofs_render(recipe, tmp_path):
    r = render_recipe(recipe, out_dir=tmp_path, draft=True)
    d = json.loads(Path(r["dd2vtt"]).read_text())
    assert d["image"]
    if "region" not in recipe.stem:
        assert d["line_of_sight"]          # battle maps have walls; region maps don't


def test_skill_op_catalogue_is_current():
    """The skill's references/ops.md is generated (`python -m mapgen ops --markdown`); no hand edits."""
    from mapgen.docs import ops_markdown
    from mapgen.ops import REGISTRY
    path = REPO / ".claude/skills/build-map/references/ops.md"
    assert path.read_text() == ops_markdown(REGISTRY), \
        "regenerate: cd software && python -m mapgen ops --markdown > ../.claude/skills/build-map/references/ops.md"
