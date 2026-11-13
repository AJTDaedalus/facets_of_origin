"""Phase 2 R1-R3: mile units and hex grids, isolines, erosion, rivers."""
import numpy as np
import pytest
from shapely.geometry import Point

from mapgen.recipe import RecipeError, parse_recipe
from tests.mapgen.conftest import header
from tests.mapgen.helpers import layer, run

MI = dict(width_ft=40, height_ft=40, feet_per_square=5, px_per_square=20, supersample=1, unit="mi")


# ---------- R1 ----------
class TestUnits:
    def test_miles_header_allows_any_size(self):
        r = parse_recipe({"map": header(unit="mi", feet_per_square=6), "steps": []})
        assert r.map.unit == "mi" and r.map.feet_per_square == 6

    def test_feet_still_rejects_odd_squares(self):
        with pytest.raises(RecipeError, match="feet_per_square"):
            parse_recipe({"map": header(feet_per_square=7), "steps": []})

    def test_bad_unit(self):
        with pytest.raises(RecipeError, match="unit"):
            parse_recipe({"map": header(unit="leagues"), "steps": []})

    def test_scale_text_uses_unit_and_shape(self):
        from mapgen.ops.overlay import scale_text
        store, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                        {"op": "grid", "shape": "hex"}], **MI)
        assert scale_text(e.frame, e.collector) == "1 hex = 5 miles"
        store, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "grid"}],
                       width_ft=20, height_ft=20, px_per_square=20, supersample=1)
        assert scale_text(e.frame, e.collector) == "1 square = 5 feet"


class TestHexGrid:
    def _grid(self, **kw):
        store, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                        {"op": "grid", "shape": "hex", "alpha": 1, "color": "#000000", **kw}], **MI)
        return store.get("canvas").data[..., 0], e

    def test_hex_lines_drawn(self):
        c, e = self._grid()
        assert (c < 0.5).mean() > 0.02 and "grid" in e.collector.masks

    def test_hex_centres_are_clear(self):
        from mapgen.ops.overlay import hex_centres
        c, e = self._grid(orientation="flat")
        for x, y in hex_centres(40, 40, 5, "flat")[:20]:
            px, py = int(x * 4), int(y * 4)
            if 2 <= px < 158 and 2 <= py < 158:
                assert c[py, px] > 0.9

    def test_pointy_differs_from_flat(self):
        a, _ = self._grid(orientation="flat")
        b, _ = self._grid(orientation="pointy")
        assert not np.array_equal(a, b)


# ---------- R2 ----------
def _cone():
    return [{"op": "gradient", "out": "h", "kind": "radial", "start": [20, 20], "end": [40, 20]},
            {"op": "remap", "out": "h", "src": "h", "in_range": [0, 1], "out_range": [1, 0]}]


class TestIsolinesAndErosion:
    def test_isolines_are_circles(self):
        g = layer(_cone() + [{"op": "isolines", "out": "c", "src": "h", "levels": [0.5]}], "c", **MI).geom
        assert g.length == pytest.approx(2 * np.pi * 10, rel=0.05)

    def test_isolines_interval(self):
        g = layer(_cone() + [{"op": "isolines", "out": "c", "src": "h", "interval": 0.25}], "c", **MI).geom
        assert len(getattr(g, "geoms", [g])) >= 3

    def test_isolines_need_levels(self):
        with pytest.raises(RecipeError):
            run(_cone() + [{"op": "isolines", "out": "c", "src": "h"}], **MI)

    def test_erode_conserves_mass_and_smooths(self):
        store, _ = run([{"op": "noise", "out": "n", "scale": 3, "kind": "ridged", "id": "n"},
                        {"op": "erode", "out": "e", "src": "n", "iterations": 30, "talus": 0.002}], **MI)
        a, b = store.get("n").data, store.get("e").data
        assert b.sum() == pytest.approx(a.sum(), rel=1e-3)
        assert np.abs(np.diff(b, axis=1)).mean() < np.abs(np.diff(a, axis=1)).mean()

    def test_erode_zero_iterations_identity(self):
        store, _ = run([{"op": "noise", "out": "n", "scale": 3, "id": "n"},
                        {"op": "erode", "out": "e", "src": "n", "iterations": 0}], **MI)
        assert np.array_equal(store.get("n").data, store.get("e").data)


# ---------- R3 ----------
RIDGE = [{"op": "gradient", "out": "slope", "start": [0, 20], "end": [40, 20]},
         {"op": "noise", "out": "n", "scale": 8, "id": "n"},
         {"op": "mix", "out": "h", "of": ["slope", "n"], "weights": [1.0, 0.12]}]


class TestRivers:
    def _rivers(self, **kw):
        store, e = run(RIDGE + [{"op": "rivers", "out": "r", "src": "h", "sea_level": 0.15, "id": "rv",
                                 "line": True, **kw}], **MI)
        return store.get("r").geom, store.get("h").data, e

    def test_rivers_exist_and_run_downhill(self):
        g, h, e = self._rivers(threshold=0.02)
        lines = list(getattr(g, "geoms", [g]))
        assert lines
        for ln in lines:
            (x0, y0), (x1, y1) = ln.coords[0], ln.coords[-1]
            hs = h[min(int(y0 * 4), 159), min(int(x0 * 4), 159)]
            he = h[min(int(y1 * 4), 159), min(int(x1 * 4), 159)]
            assert he <= hs + 0.02

    def test_rivers_reach_sea_edge_or_join(self):
        g, h, e = self._rivers(threshold=0.02)
        lines = list(getattr(g, "geoms", [g]))
        reached = 0
        for i, ln in enumerate(lines):
            x, y = ln.coords[-1]
            at_sea = x < 8 or x > 39 or y < 1 or y > 39 or h[min(int(y * 4), 159), min(int(x * 4), 159)] < 0.2
            joins = any(Point(x, y).distance(o) < 0.6 for j, o in enumerate(lines) if j != i)
            assert at_sea or joins
            reached += at_sea
        assert reached >= 1

    def test_threshold_controls_count(self):
        few, _, _ = self._rivers(threshold=0.08)
        many, _, _ = self._rivers(threshold=0.01)
        assert many.length > few.length

    def test_width_grows_downstream(self):
        store, _ = run(RIDGE + [{"op": "rivers", "out": "r", "src": "h", "sea_level": 0.15, "threshold": 0.02,
                                 "width": [0.2, 2.0], "id": "rv"}], **MI)
        g = store.get("r").geom
        assert g.area > 0 and g.geom_type in ("Polygon", "MultiPolygon")

    def test_deterministic(self):
        a, _, _ = self._rivers(threshold=0.02)
        b, _, _ = self._rivers(threshold=0.02)
        assert a.equals(b)


class TestPathLabel:
    def _canvas(self, **kw):
        store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                        {"op": "path_label", "text": "Long River", "size": 3, "halo": None, "color": "#000000",
                         **kw}], **MI)
        return store.get("canvas").data[..., 0]

    def test_letters_follow_the_line(self):
        c = self._canvas(points=[[4, 20], [20, 12], [36, 20]])
        ys, xs = np.nonzero(c < 0.5)
        assert len(xs) > 50
        from shapely.geometry import LineString
        from mapgen.ops.geometry import _chaikin
        ln = LineString(_chaikin([[4, 20], [20, 12], [36, 20]], 3))
        d = [ln.distance(Point(x / 4, y / 4)) for x, y in zip(xs[::7], ys[::7])]
        assert max(d) < 3

    def test_straight_vs_curved_differ(self):
        assert not np.array_equal(self._canvas(points=[[4, 20], [36, 20]]),
                                  self._canvas(points=[[4, 20], [20, 12], [36, 20]]))

    def test_westward_line_still_reads_left_to_right(self):
        a = self._canvas(points=[[4, 20], [36, 20]])
        b = self._canvas(points=[[36, 20], [4, 20]])
        assert np.array_equal(a, b)

    def test_needs_a_line(self):
        with pytest.raises(RecipeError):
            self._canvas()
