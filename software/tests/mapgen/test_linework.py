"""Ink line-work ops: shade_lines, cracks, stipple (owner feedback 2026-11-13)."""
from pathlib import Path

import numpy as np
import pytest
import yaml

from mapgen.recipe import RecipeError
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=20, supersample=1)     # 4 px/ft
ROOM = [{"op": "canvas", "out": "canvas", "color": "#ffffff"},
        {"op": "rect", "out": "r", "x": 5, "y": 5, "w": 30, "h": 20},
        {"op": "rasterize", "out": "m", "src": "r"}]


def ink(extra, **kw):
    store, _ = run(ROOM + extra, **dict(H, **kw))
    return store.get("canvas").data[..., 0] < 0.6


class TestShadeLines:
    def test_strokes_hug_the_inside_of_the_edge(self):
        a = ink([{"op": "shade_lines", "mask": "m", "length": 2, "id": "s"}])
        assert a.sum() > 100
        assert not a[:18, :].any() and not a[:, :18].any()          # nothing outside the room
        assert not a[40:80, 50:110].any()                           # nothing in the room's middle

    def test_longer_on_the_shadow_side(self):
        a = ink([{"op": "shade_lines", "mask": "m", "length": 3, "shadow": [0, 1], "min_share": 0.2, "id": "s"}])
        north = a[20:34, 30:130].sum()      # floor under the north wall: shadow falls south onto it
        south = a[86:100, 30:130].sum()
        assert north > south * 2

    def test_outside_side_and_no_shadow(self):
        a = ink([{"op": "shade_lines", "mask": "m", "side": "outside", "shadow": None, "length": 2, "id": "s"}])
        assert a[:19, 30:130].any() and not a[30:70, 40:120].any()

    def test_deterministic(self):
        steps = [{"op": "shade_lines", "mask": "m", "id": "s"}]
        assert np.array_equal(ink(steps), ink(steps))

    def test_bad_params(self):
        with pytest.raises(RecipeError):
            ink([{"op": "shade_lines", "mask": "m", "length": 0}])


class TestCracks:
    def test_inside_only_and_scales_with_density(self):
        few = ink([{"op": "cracks", "mask": "m", "density": 0.1, "id": "c"}])
        many = ink([{"op": "cracks", "mask": "m", "density": 1.5, "id": "c"}])
        assert many.sum() > few.sum() > 0
        assert not many[:19, :].any() and not many[:, :19].any()

    def test_empty_mask_is_harmless(self):
        store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                        {"op": "rect", "out": "r", "x": 500, "y": 500, "w": 3, "h": 3},
                        {"op": "rasterize", "out": "m", "src": "r"},
                        {"op": "cracks", "mask": "m"}], **H)
        assert np.allclose(store.get("canvas").data[..., :3], 1)

    def test_bad_density(self):
        with pytest.raises(RecipeError, match="density"):
            ink([{"op": "cracks", "mask": "m", "density": 0}])


class TestStipple:
    def test_denser_at_the_edge(self):
        a = ink([{"op": "stipple", "mask": "m", "density": 8, "falloff": 3, "id": "d"}])
        edge = a[20:28, 30:130].mean()
        middle = a[52:60, 30:130].mean()
        assert edge > middle and a.sum() > 20

    def test_even_spread(self):
        a = ink([{"op": "stipple", "mask": "m", "density": 4, "falloff": None, "id": "d"}])
        assert a[52:60, 30:130].any()

    def test_bad_size(self):
        with pytest.raises(RecipeError, match="size"):
            ink([{"op": "stipple", "mask": "m", "size": -1}])


# ---------- review round (docs/REVIEW_pr37.md) ----------
from mapgen.recipe import load_recipe, parse_recipe, Style
from tests.mapgen.conftest import header


def dots(steps, **h):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + steps, **h)
    from scipy import ndimage
    ink_px = store.get("canvas").data[..., 0] < 0.6
    return ndimage.label(ink_px)[1]


class TestStippleDensityIsAbsolute:
    ROOM10 = [{"op": "rect", "out": "r", "x": 1, "y": 1, "w": 10, "h": 10},
              {"op": "rasterize", "out": "m", "src": "r"},
              {"op": "stipple", "mask": "m", "density": 1.0, "falloff": None, "size": 0.15, "id": "d"}]

    def test_same_room_same_count_in_any_frame(self):
        counts = [dots(self.ROOM10, width_ft=w, height_ft=w, px_per_square=20, supersample=1) for w in (12, 40, 120)]
        assert max(counts) / max(min(counts), 1) < 1.35       # was 258 / 57 / 9 before the fix

    def test_count_near_density_times_area(self):
        n = dots(self.ROOM10, width_ft=40, height_ft=40, px_per_square=40, supersample=1)
        assert 60 <= n <= 110                                # ~100 dots for 100 ft² (some merge)


class TestShadeLinesGeometry:
    def test_outside_with_shadow_is_longer_south_east(self):
        a = ink([{"op": "shade_lines", "mask": "m", "side": "outside", "length": 3, "shadow": [0, 1], "min_share": 0.1,
                  "id": "s"}])
        south, north = a[100:115, 30:130].sum(), a[5:20, 30:130].sum()
        assert south > north * 2

    def test_mask_with_hole_shades_round_the_hole(self):
        a = ink([{"op": "circle", "out": "c", "center": [20, 15], "r": 3},
                 {"op": "subtract", "out": "rh", "a": "r", "b": ["c"]},
                 {"op": "rasterize", "out": "mh", "src": "rh"},
                 {"op": "shade_lines", "mask": "mh", "shadow": None, "length": 1.5, "id": "s"}])
        ring = a[38:82, 58:102]
        assert ring.sum() > 10 and not a[58:62, 78:82].any()          # strokes round the pillar, none inside it

    def test_mask_touching_the_border(self):
        store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                        {"op": "rect", "out": "r", "x": -5, "y": -5, "w": 20, "h": 20},
                        {"op": "rasterize", "out": "m", "src": "r"},
                        {"op": "shade_lines", "mask": "m", "id": "s"}], **H)
        assert (store.get("canvas").data[..., 0] < 0.6).any()


class TestCracksShape:
    def test_length_scales_ink(self):
        short = ink([{"op": "cracks", "mask": "m", "density": 1, "length": 1, "branch": 0, "id": "c"}]).sum()
        long_ = ink([{"op": "cracks", "mask": "m", "density": 1, "length": 6, "branch": 0, "id": "c"}]).sum()
        assert long_ > short * 2

    def test_branching_adds_ink(self):
        none = ink([{"op": "cracks", "mask": "m", "density": 1, "length": 6, "branch": 0, "id": "c"}]).sum()
        lots = ink([{"op": "cracks", "mask": "m", "density": 1, "length": 6, "branch": 1, "id": "c"}]).sum()
        assert lots > none


STYLE_FILE = Path(__file__).resolve().parents[2] / "mapgen" / "styles" / "inked_parchment.yaml"


def styled(steps, **h):
    store, e = run(steps, style=yaml.safe_load(STYLE_FILE.read_text()), **dict(H, **h))
    return store.get("canvas").data


class TestShadingConvention:
    """Light from the north-west: floors darker along their north wall, raised masses along their south edge."""

    def test_floor_fill_soft_shadow_and_hatching_agree(self):
        c = styled([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                    {"op": "rect", "out": "room", "x": 5, "y": 5, "w": 30, "h": 20},
                    {"op": "floor_fill", "src": "room", "material": "flagstone", "cracks": 0.0001}])
        lum = c[..., :3].mean(-1)
        north, south = lum[21:32, 40:120].mean(), lum[88:99, 40:120].mean()
        assert north < south - 0.02

    def test_brush_shaded_on_its_south_east_side(self):
        c = styled([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                    {"op": "rect", "out": "all", "x": 0, "y": 0, "w": 40, "h": 30},
                    {"op": "rasterize", "out": "edges", "src": "all"},
                    {"op": "rect", "out": "none", "x": 500, "y": 500, "w": 1, "h": 1},
                    {"op": "rasterize", "out": "clear", "src": "none"},
                    {"op": "brush", "within": "edges", "clear": "clear", "scale": 40, "cover": -1.0}])
        # brush covers nearly everything; its north edge (map top) must be lighter than its south edge
        lum = c[..., :3].mean(-1)
        assert lum[2:10, 20:140].mean() > lum[110:118, 20:140].mean()

    def test_trees_are_not_rotated(self):
        a = styled([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                    {"op": "prop", "kind": "tree", "at": [20, 15], "size": 12, "id": "t"}])
        b = styled([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                    {"op": "prop", "kind": "tree", "at": [20, 15], "size": 12, "rotate": 137, "id": "t"}])
        assert np.array_equal(a, b)


class TestMacroParams:
    def test_unknown_macro_param_is_an_error(self):
        with pytest.raises(RecipeError, match="doesn't take"):
            parse_recipe({"map": header(), "steps": [{"op": "finish", "floor": "x"}]},
                         style=Style(**yaml.safe_load(STYLE_FILE.read_text())))

    def test_declared_params_are_fine(self):
        r = parse_recipe({"map": header(), "steps": [{"op": "stream", "points": [[0, 0], [5, 5]], "bank": 0.5}]},
                         style=Style(**yaml.safe_load(STYLE_FILE.read_text())))
        assert any(s.op == "shade_lines" and s.params()["length"] == 0.5 for s in r.steps)
