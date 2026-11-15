"""Mists region style (owner concept art, 2026-11-15; docs/REFERENCE_mists_region_visual_brief.md)."""
import colorsys
from pathlib import Path

import numpy as np
import pytest

from mapgen.recipe import _load_style
from tests.mapgen.helpers import run

STYLES = Path(__file__).resolve().parents[2] / "mapgen" / "styles"
STYLE = _load_style(["mists_region.yaml"], STYLES)
H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)
LAND = [{"op": "rect", "out": "land", "x": 0, "y": 0, "w": 20, "h": 30},
        {"op": "rasterize", "out": "land_m", "src": "land"},
        {"op": "rect", "out": "none", "x": -10, "y": -10, "w": 1, "h": 1},
        {"op": "rasterize", "out": "clear", "src": "none"}]


def canvas(steps):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#808080"}] + LAND + steps, style=STYLE, **H)
    return store.get("canvas").data[..., :3]


def sat(rgb):
    return np.mean([colorsys.rgb_to_hsv(*p)[1] for p in rgb.reshape(-1, 3)[::37]])


class TestRegionStyle:
    def test_includes_the_parchment_style(self):
        assert "stone_room" in STYLE["macros"] and "flagstone" in STYLE["materials"]

    @pytest.mark.parametrize("m", ["ash_sand", "wet_ash", "dune_dark", "grey_sea"])
    def test_materials_are_near_grey_and_never_cyan(self, m):
        c = canvas([{"op": "fill", "material": m, "id": "f"}])
        r, g, b = c.reshape(-1, 3).mean(0)
        assert sat(c) < 0.2 and b <= g + 0.03                     # no blue cast

    def test_dunes_are_dark_than_the_sand(self):
        c = canvas([{"op": "fill", "mask": "land_m", "material": "ash_sand", "id": "s"},
                    {"op": "dunes", "within": "land_m", "clear": "clear", "cover": -0.3, "id": "d"}])
        sand = canvas([{"op": "fill", "mask": "land_m", "material": "ash_sand", "id": "s"}])
        assert c[:, :150].mean() < sand[:, :150].mean() - 0.05

    def test_rough_sea_puts_whitecaps_only_off_the_land(self):
        base = canvas([{"op": "fill", "material": "grey_sea", "id": "w"}])
        c = canvas([{"op": "fill", "material": "grey_sea", "id": "w"},
                     {"op": "rough_sea", "land": "land_m", "from": 3, "amount": 0.15, "soft": 0.25, "id": "rs"}])
        assert np.allclose(c[:, :150], base[:, :150], atol=1e-6)    # land untouched
        assert (c[:, 190:].mean(-1) > 0.6).sum() > 100              # white flecks on the water

    def test_lit_mist_is_brightest_near_its_centre(self):
        steps = [{"op": "rect", "out": "all", "x": 0, "y": 0, "w": 40, "h": 30},
                 {"op": "rasterize", "out": "mist_m", "src": "all"},
                 {"op": "lit_mist", "mist": "mist_m", "center": [38, 2], "edge": [8, 2], "id": "lm"}]
        c = canvas(steps).mean(-1)
        assert c[16, 300] > c[220, 20] + 0.2


class TestReviewPR41:
    def test_r2_dunes_stay_inside_within_and_out_of_clear(self):
        steps = [{"op": "rect", "out": "w", "x": 0, "y": 0, "w": 20, "h": 30},
                 {"op": "rasterize", "out": "w_m", "src": "w"},
                 {"op": "rect", "out": "c", "x": 0, "y": 10, "w": 20, "h": 8},
                 {"op": "rasterize", "out": "c_m", "src": "c"}]
        base = canvas(steps)
        c = canvas(steps + [{"op": "dunes", "within": "w_m", "clear": "c_m", "cover": -0.4, "id": "d"}])
        diff = np.abs(c - base).max(-1) > 0.02
        assert diff[:, 162:].sum() == 0                     # nothing beyond x = 20 ft (+ 2 px)
        assert diff[82:142, :150].sum() == 0               # nothing inside the clear band (10-18 ft, inset 2 px)
        assert diff.sum() > 1000

    def test_r3_lit_mist_doc_names_only_real_params(self):
        m = STYLE["macros"]["lit_mist"]
        import re
        named = set(re.findall(r"`(\w+)`", m["doc"]))
        assert named <= set(m["params"]) | {"atmosphere"}
