"""T7-T10: geometry ops, roughen_geom, rasterize, mask ops."""
import numpy as np
import pytest

from mapgen.recipe import RecipeError
from tests.mapgen.helpers import layer, run

BIG = dict(width_ft=40, height_ft=40, px_per_square=20, supersample=1)


# ---------- T7 ----------
class TestShapes:
    def test_rect_area(self):
        g = layer([{"op": "rect", "out": "a", "x": 1, "y": 2, "w": 10, "h": 4}], "a").geom
        assert g.area == pytest.approx(40) and g.bounds == (1, 2, 11, 6)

    def test_rect_rotated_keeps_area(self):
        g = layer([{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 10, "h": 4, "rotate": 30}], "a").geom
        assert g.area == pytest.approx(40)

    def test_rect_needs_positive_size(self):
        with pytest.raises(RecipeError, match="w"):
            run([{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 0, "h": 4}])

    def test_polygon(self):
        g = layer([{"op": "polygon", "out": "a", "points": [[0, 0], [10, 0], [10, 10]]}], "a").geom
        assert g.area == pytest.approx(50) and g.is_valid

    def test_polygon_with_hole(self):
        g = layer([{"op": "polygon", "out": "a", "points": [[0, 0], [10, 0], [10, 10], [0, 10]],
                    "holes": [[[2, 2], [4, 2], [4, 4], [2, 4]]]}], "a").geom
        assert g.area == pytest.approx(96)

    def test_polygon_too_few_points(self):
        with pytest.raises(RecipeError, match="points"):
            run([{"op": "polygon", "out": "a", "points": [[0, 0], [1, 1]]}])

    def test_self_intersecting_polygon_is_repaired(self):
        g = layer([{"op": "polygon", "out": "a", "points": [[0, 0], [10, 10], [10, 0], [0, 10]]}], "a").geom
        assert g.is_valid and g.area > 0

    def test_circle_and_ellipse(self):
        c = layer([{"op": "circle", "out": "a", "center": [5, 5], "r": 3}], "a").geom
        assert c.area == pytest.approx(np.pi * 9, rel=0.01)
        e = layer([{"op": "ellipse", "out": "a", "center": [5, 5], "rx": 4, "ry": 2}], "a").geom
        assert e.area == pytest.approx(np.pi * 8, rel=0.01)

    def test_circle_radius_positive(self):
        with pytest.raises(RecipeError):
            run([{"op": "circle", "out": "a", "center": [5, 5], "r": -1}])

    def test_path_width(self):
        g = layer([{"op": "path", "out": "a", "points": [[0, 5], [10, 5]], "width": 2, "cap": "flat"}], "a").geom
        assert g.area == pytest.approx(20)

    def test_path_round_cap_longer(self):
        g = layer([{"op": "path", "out": "a", "points": [[0, 5], [10, 5]], "width": 2}], "a").geom
        assert g.area == pytest.approx(20 + np.pi, rel=0.02)

    def test_path_as_line(self):
        g = layer([{"op": "path", "out": "a", "points": [[0, 5], [10, 5]], "line": True}], "a").geom
        assert g.geom_type == "LineString" and g.length == pytest.approx(10)

    def test_booleans(self):
        steps = [{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 10, "h": 10},
                 {"op": "rect", "out": "b", "x": 5, "y": 0, "w": 10, "h": 10},
                 {"op": "union", "out": "u", "of": ["a", "b"]},
                 {"op": "intersect", "out": "i", "of": ["a", "b"]},
                 {"op": "subtract", "out": "s", "a": "a", "b": ["b"]}]
        store, _ = run(steps)
        assert store.get("u").geom.area == pytest.approx(150)
        assert store.get("i").geom.area == pytest.approx(50)
        assert store.get("s").geom.area == pytest.approx(50)

    def test_intersect_empty(self):
        steps = [{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 1, "h": 1},
                 {"op": "rect", "out": "b", "x": 5, "y": 5, "w": 1, "h": 1},
                 {"op": "intersect", "out": "i", "of": ["a", "b"]}]
        assert layer(steps, "i").geom.is_empty

    def test_union_needs_geometry(self):
        with pytest.raises(RecipeError, match="Geometry"):
            run([{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 1, "h": 1},
                 {"op": "rasterize", "out": "m", "src": "a"},
                 {"op": "union", "out": "u", "of": ["a", "m"]}])

    def test_offset(self):
        steps = [{"op": "rect", "out": "a", "x": 5, "y": 5, "w": 10, "h": 10},
                 {"op": "offset", "out": "g", "src": "a", "by": 1, "join": "mitre"},
                 {"op": "offset", "out": "s", "src": "a", "by": -1, "join": "mitre"}]
        store, _ = run(steps, **BIG)
        assert store.get("g").geom.area == pytest.approx(144)
        assert store.get("s").geom.area == pytest.approx(64)


# ---------- T8 ----------
class TestRoughen:
    base = [{"op": "rect", "out": "a", "x": 5, "y": 5, "w": 20, "h": 20}]

    def _r(self, **kw):
        return layer(self.base + [{"op": "roughen_geom", "out": "r", "src": "a", "id": "rg", **kw}],
                     "r", **BIG).geom

    def test_deterministic(self):
        assert self._r(amount=1.5, scale=5).equals(self._r(amount=1.5, scale=5))

    def test_area_within_10pct_and_valid(self):
        g = self._r(amount=1.5, scale=5)
        assert g.is_valid and abs(g.area - 400) / 400 < 0.10

    def test_actually_rough(self):
        g = self._r(amount=1.5, scale=5)
        assert len(g.exterior.coords) > 20

    def test_zero_amount_identity(self):
        assert self._r(amount=0, scale=5).area == pytest.approx(400)

    def test_seed_offset_changes_shape(self):
        assert not self._r(amount=1.5, scale=5).equals(self._r(amount=1.5, scale=5, seed_offset=3))


# ---------- T9 ----------
class TestRasterize:
    def test_rect_coverage(self):
        # 30x40 ft at 70 px/sq -> 420x560 px
        m = layer([{"op": "rect", "out": "a", "x": 5, "y": 5, "w": 30, "h": 40},
                   {"op": "rasterize", "out": "m", "src": "a"}], "m",
                  width_ft=40, height_ft=50, px_per_square=70, supersample=1).data
        assert m.sum() == pytest.approx(420 * 560, rel=0.005)
        assert m.dtype == np.float32 and m.max() <= 1.0

    def test_edges_are_antialiased(self):
        m = layer([{"op": "circle", "out": "a", "center": [10, 10], "r": 6},
                   {"op": "rasterize", "out": "m", "src": "a"}], "m", **BIG).data
        frac = ((m > 0.05) & (m < 0.95)).sum()
        assert frac > 20

    def test_holes_stay_holes(self):
        m = layer([{"op": "polygon", "out": "a", "points": [[0, 0], [20, 0], [20, 20], [0, 20]],
                    "holes": [[[5, 5], [15, 5], [15, 15], [5, 15]]]},
                   {"op": "rasterize", "out": "m", "src": "a"}], "m", **BIG).data
        assert m[40, 40] == 0 and m[10, 10] == 1   # 4 px per ft

    def test_off_canvas_clipped(self):
        m = layer([{"op": "rect", "out": "a", "x": -10, "y": -10, "w": 15, "h": 15},
                   {"op": "rasterize", "out": "m", "src": "a"}], "m", **BIG).data
        assert m.sum() == pytest.approx(20 * 20, rel=0.02)

    def test_line_rasterizes_with_width(self):
        m = layer([{"op": "path", "out": "a", "points": [[0, 10], [40, 10]], "line": True},
                   {"op": "rasterize", "out": "m", "src": "a", "line_width": 2}], "m", **BIG).data
        assert m.sum() == pytest.approx(160 * 8, rel=0.05)


# ---------- T10 ----------
def _sq(extra):
    return [{"op": "rect", "out": "a", "x": 10, "y": 10, "w": 20, "h": 20},
            {"op": "rasterize", "out": "m", "src": "a"}] + extra


class TestMaskOps:
    def test_grow(self):
        m = layer(_sq([{"op": "grow", "out": "g", "src": "m", "by": 5}]), "g", **BIG).data
        # width 20 + 2*5 = 30 ft -> 120 px along the middle row
        assert (m[80] > 0.5).sum() == pytest.approx(120, abs=1)

    def test_shrink(self):
        m = layer(_sq([{"op": "shrink", "out": "s", "src": "m", "by": 5}]), "s", **BIG).data
        assert (m[80] > 0.5).sum() == pytest.approx(40, abs=1)

    def test_shrink_to_nothing(self):
        m = layer(_sq([{"op": "shrink", "out": "s", "src": "m", "by": 15}]), "s", **BIG).data
        assert m.max() == 0

    def test_blur_spreads_but_keeps_mass(self):
        store, _ = run(_sq([{"op": "blur", "out": "b", "src": "m", "sigma": 1}]), **BIG)
        a, b = store.get("m").data, store.get("b").data
        assert b.sum() == pytest.approx(a.sum(), rel=0.01) and ((b > 0) & (b < 1)).sum() > ((a > 0) & (a < 1)).sum()

    def test_threshold(self):
        m = layer(_sq([{"op": "blur", "out": "b", "src": "m", "sigma": 2},
                       {"op": "threshold", "out": "t", "src": "b", "level": 0.5}]), "t", **BIG).data
        assert set(np.unique(m)) <= {0.0, 1.0}

    def test_invert(self):
        store, _ = run(_sq([{"op": "invert", "out": "i", "src": "m"}]), **BIG)
        assert np.allclose(store.get("i").data + store.get("m").data, 1)

    def test_band_outside(self):
        m = layer(_sq([{"op": "band", "out": "b", "src": "m", "inner": 0, "outer": 2}]), "b", **BIG).data
        # ring 2 ft wide around a 20 ft square: (24^2 - 20^2) ft² * 16 px/ft²
        assert m.sum() == pytest.approx((24 * 24 - 20 * 20) * 16, rel=0.06)
        assert m[80, 80] == 0

    def test_band_inside(self):
        m = layer(_sq([{"op": "band", "out": "b", "src": "m", "inner": 0, "outer": 2, "side": "inside"}]), "b", **BIG).data
        assert m.sum() == pytest.approx((20 * 20 - 16 * 16) * 16, rel=0.06)

    def test_combine_modes(self):
        steps = _sq([{"op": "rect", "out": "c", "x": 20, "y": 10, "w": 20, "h": 20},
                     {"op": "rasterize", "out": "n", "src": "c"},
                     {"op": "combine", "out": "mx", "of": ["m", "n"], "mode": "max"},
                     {"op": "combine", "out": "mn", "of": ["m", "n"], "mode": "min"},
                     {"op": "combine", "out": "sb", "of": ["m", "n"], "mode": "sub"}])
        store, _ = run(steps, **BIG)
        px = 16
        assert store.get("mx").data.sum() == pytest.approx(600 * px, rel=0.01)
        assert store.get("mn").data.sum() == pytest.approx(200 * px, rel=0.01)
        assert store.get("sb").data.sum() == pytest.approx(200 * px, rel=0.01)

    def test_roughen_mask(self):
        store, _ = run(_sq([{"op": "roughen", "out": "r", "src": "m", "amount": 1.5, "scale": 4}]), **BIG)
        a, r = store.get("m").data, store.get("r").data
        assert abs(r.sum() - a.sum()) / a.sum() < 0.15 and not np.array_equal(a, r)

    def test_mask_op_rejects_geometry(self):
        with pytest.raises(RecipeError, match="Mask"):
            run([{"op": "rect", "out": "a", "x": 0, "y": 0, "w": 1, "h": 1},
                 {"op": "blur", "out": "b", "src": "a", "sigma": 1}])
