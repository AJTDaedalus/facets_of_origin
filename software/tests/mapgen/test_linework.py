"""Ink line-work ops: shade_lines, cracks, stipple (owner feedback 2026-11-13)."""
import numpy as np
import pytest

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
