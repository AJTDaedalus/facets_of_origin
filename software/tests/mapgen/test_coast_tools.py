"""Coast styling round (owner, 2026-11-14: "the sand effects look a little weak ... the lace and crests too"):
cellular noise for foam lace, slope facing for ripple shadow sides, clipped and tapered strokes,
weighted stipple, and beach cusps."""
import numpy as np
import pytest
import shapely
from shapely.geometry import LineString, box

from mapgen.recipe import RecipeError
from tests.mapgen.helpers import layer, run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft, 320 × 240 px
CANVAS = [{"op": "canvas", "out": "canvas", "color": "#ffffff"}]


def ink(steps, **h):
    store, _ = run(CANVAS + steps, **dict(H, **h))
    return 1 - store.get("canvas").data[..., :3].mean(-1)          # 0 = paper, 1 = full ink


def cells(**kw):
    return layer([dict({"op": "cells", "out": "c", "id": "c"}, **kw)], "c", **H).data


class TestCells:
    def test_edge_distance_is_zero_on_borders_and_small_on_average(self):
        c = cells(scale=4)
        assert c.min() >= 0 and c.min() < 0.05
        assert 0.3 < c.mean() < 1.5                         # half a 4 ft cell is 2 ft at the very most
        assert (c < 0.15).mean() < 0.25                     # the borders are thin lines, not areas

    def test_bigger_cells_mean_farther_from_an_edge(self):
        assert cells(scale=8).mean() > 1.5 * cells(scale=3).mean()

    def test_deterministic_and_seeded(self):
        assert np.array_equal(cells(scale=4), cells(scale=4))
        a = layer([{"op": "cells", "out": "c", "scale": 4, "id": "a"}], "c", **H).data
        b = layer([{"op": "cells", "out": "c", "scale": 4, "id": "b"}], "c", **H).data
        assert not np.array_equal(a, b)

    def test_zero_jitter_is_a_regular_grid(self):
        c = cells(scale=5, jitter=0)                        # 5 ft = 40 px period
        assert np.allclose(c[60:100, 60:100], c[100:140, 100:140], atol=1e-3)

    def test_center_metric_is_zero_at_the_seed_points(self):
        c = cells(scale=4, metric="center")
        assert c.min() < 0.1 and c.max() > cells(scale=4).max()

    def test_lace_mask_from_cells_is_a_net(self):
        steps = [{"op": "cells", "out": "c", "scale": 3, "id": "c"},
                 {"op": "remap", "out": "e", "src": "c", "in_range": [0, 0.2], "out_range": [1, 0]},
                 {"op": "field_to_mask", "out": "m", "src": "e", "lo": 0.5, "hi": 0.5}]
        m = layer(steps, "m", **H).data
        from scipy import ndimage
        _, n_holes = ndimage.label(m < 0.5)
        assert 0.05 < m.mean() < 0.4 and n_holes > 20     # a net: thin lines round many separate holes

    @pytest.mark.parametrize("bad", [{"scale": 0}, {"jitter": 1.5}, {"metric": "f3"}])
    def test_bad_params(self, bad):
        with pytest.raises(RecipeError):
            cells(**bad)


def facing(field_steps, **kw):
    return layer(field_steps + [dict({"op": "facing", "out": "f", "src": "g"}, **kw)], "f", **H).data


EAST_DOWN = [{"op": "gradient", "out": "g", "start": [40, 0], "end": [0, 0]}]   # high in the west, falls east


class TestFacing:
    def test_slopes_facing_the_direction_are_selected(self):
        assert facing(EAST_DOWN, toward=[1, 0])[100:140, 100:220].min() > 0.99
        assert facing(EAST_DOWN, toward=[-1, 0])[100:140, 100:220].max() < 0.01

    def test_default_is_south_east_and_a_sideways_slope_is_partial(self):
        f = facing(EAST_DOWN)[100:140, 100:220]                  # east-falling vs SE light: cos = 0.6
        assert 0.2 < f.mean() < 1.0

    def test_flat_field_faces_nowhere(self):
        flat = [{"op": "gradient", "out": "g0", "start": [0, 0], "end": [40, 0]},
                {"op": "remap", "out": "g", "src": "g0", "in_range": [0, 1], "out_range": [0.5, 0.5]}]
        f = facing(flat)
        assert np.isfinite(f).all() and f.max() == 0

    def test_steep_scales_by_slope(self):
        gentle = facing(EAST_DOWN, toward=[1, 0], steep=1.0)       # slope 1/40 per ft, far below 1
        assert gentle[100:140, 100:220].max() < 0.1

    def test_needs_a_field(self):
        with pytest.raises(RecipeError):
            layer([{"op": "rect", "out": "r", "x": 0, "y": 0, "w": 5, "h": 5},
                   {"op": "facing", "out": "f", "src": "r"}], "f", **H)


LINE = [{"op": "path", "out": "ln", "points": [[4, 15], [36, 15]], "line": True}]


class TestStrokeClipAndTaper:
    def test_clip_mask_keeps_ink_out_of_its_holes(self):
        steps = LINE + [{"op": "rect", "out": "west", "x": 0, "y": 0, "w": 20, "h": 30},
                        {"op": "rasterize", "out": "west_m", "src": "west"},
                        {"op": "stroke", "src": "ln", "width": 0.4, "clip": "west_m"}]
        a = ink(steps)
        assert a[:, 20:150].max() > 0.8 and a[:, 170:].max() < 0.01

    def test_clip_works_for_mask_sources(self):
        steps = [{"op": "rect", "out": "r", "x": 5, "y": 5, "w": 30, "h": 20},
                 {"op": "rasterize", "out": "rm", "src": "r"},
                 {"op": "rect", "out": "west", "x": 0, "y": 0, "w": 20, "h": 30},
                 {"op": "rasterize", "out": "west_m", "src": "west"},
                 {"op": "stroke", "src": "rm", "width": 0.4, "clip": "west_m"}]
        a = ink(steps)
        assert a[:, :150].max() > 0.8 and a[:, 170:].max() < 0.01

    def test_taper_is_thick_in_the_middle_thin_at_the_ends(self):
        a = ink(LINE + [{"op": "stroke", "src": "ln", "width": 0.6, "taper": 0.9}])
        mid = (a[:, 158:162] > 0.5).sum(0).mean()
        end = (a[:, 38:42] > 0.5).sum(0).mean()
        assert mid >= 4 and end < mid / 2

    def test_taper_applies_to_each_dash(self):
        a = ink(LINE + [{"op": "stroke", "src": "ln", "width": 0.6, "taper": 0.9, "dash": [8, 2]}])
        col = (a > 0.5).sum(0)                                    # dash 1 spans 4..12 ft = 32..96 px
        assert col[62:66].mean() > 2 * max(col[34:36].mean(), 0.5)

    def test_no_taper_is_unchanged(self):
        base = ink(LINE + [{"op": "stroke", "src": "ln", "width": 0.3, "dash": [3, 1], "jitter": 0.4}])
        zero = ink(LINE + [{"op": "stroke", "src": "ln", "width": 0.3, "dash": [3, 1], "jitter": 0.4, "taper": 0}])
        assert np.array_equal(base, zero)

    def test_taper_needs_a_geometry(self):
        with pytest.raises(RecipeError, match="taper"):
            ink([{"op": "rect", "out": "r", "x": 5, "y": 5, "w": 30, "h": 20},
                 {"op": "rasterize", "out": "rm", "src": "r"},
                 {"op": "stroke", "src": "rm", "taper": 0.5}])

    def test_tapered_closed_ring_is_valid(self):
        a = ink([{"op": "circle", "out": "c", "center": [20, 15], "r": 8},
                 {"op": "stroke", "src": "c", "width": 0.4, "taper": 0.8, "dash": [5, 1]}])
        assert a.max() > 0.8


AREA = [{"op": "rect", "out": "all", "x": 0, "y": 0, "w": 40, "h": 30},
        {"op": "rasterize", "out": "all_m", "src": "all"},
        {"op": "rect", "out": "west", "x": 0, "y": 0, "w": 20, "h": 30},
        {"op": "rasterize", "out": "west_m", "src": "west"}]


class TestStippleWeight:
    def test_dots_follow_the_weight(self):
        a = ink(AREA + [{"op": "stipple", "mask": "all_m", "falloff": None, "density": 4, "weight": "west_m", "id": "s"}])
        assert a[:, :150].sum() > 50 and a[:, 170:].sum() == 0

    def test_partial_weight_thins_the_dots(self):
        steps = AREA + [{"op": "gradient", "out": "g", "start": [0, 0], "end": [40, 0]},
                        {"op": "field_to_mask", "out": "gm", "src": "g", "lo": 0, "hi": 1},
                        {"op": "stipple", "mask": "all_m", "falloff": None, "density": 6, "weight": "gm", "id": "s"}]
        a = ink(steps)
        assert a[:, 240:].sum() > 2 * a[:, :80].sum()

    def test_all_ones_weight_matches_no_weight(self):
        plain = ink(AREA + [{"op": "stipple", "mask": "west_m", "falloff": None, "id": "s"}])
        weighted = ink(AREA + [{"op": "stipple", "mask": "west_m", "falloff": None, "weight": "all_m", "id": "s"}])
        assert np.array_equal(plain, weighted)

    def test_zero_weight_draws_nothing(self):
        steps = AREA + [{"op": "invert", "out": "east_m", "src": "all_m"},
                        {"op": "stipple", "mask": "all_m", "falloff": None, "weight": "east_m", "id": "s"}]
        assert ink(steps).sum() == 0


def rough(src_steps, **kw):
    return layer(src_steps + [dict({"op": "roughen_geom", "out": "r", "src": "s", "id": "r"}, **kw)], "r", **H).geom


SQUARE = [{"op": "rect", "out": "s", "x": 10, "y": 5, "w": 20, "h": 20}]


class TestCusps:
    def test_cusps_only_push_outward_by_at_most_amount(self):
        sq = box(10, 5, 30, 25)
        g = rough(SQUARE, mode="cusps", amount=0.6, period=4)
        assert g.buffer(1e-6).contains(sq) and g.area > sq.area
        assert sq.hausdorff_distance(g) == pytest.approx(0.6, abs=0.08)

    def test_period_sets_the_number_of_scallops(self):
        def peaks(period):
            g = rough(SQUARE, mode="cusps", amount=0.6, period=period, jitter=0)
            pts = np.asarray(g.exterior.coords)
            north = pts[(pts[:, 0] > 11) & (pts[:, 0] < 29) & (pts[:, 1] > 4.97) & (pts[:, 1] < 5.01)]   # near the horns, which stay on the old edge
            xs = np.sort(north[:, 0])
            return 1 + int((np.diff(xs) > period / 3).sum()) if len(xs) else 0
        assert peaks(2) > 1.6 * peaks(4)

    def test_lines_are_pushed_to_one_side(self):
        ln = [{"op": "path", "out": "s", "points": [[2, 15], [38, 15]], "line": True}]
        g = rough(ln, mode="cusps", amount=0.5, period=3)
        ys = np.asarray(g.coords)[:, 1]
        assert (ys <= 15 + 1e-9).all() or (ys >= 15 - 1e-9).all()
        assert np.ptp(ys) == pytest.approx(0.5, abs=0.05)

    def test_default_mode_is_unchanged_noise(self):
        a = rough(SQUARE, amount=0.8, scale=4)
        b = rough(SQUARE, amount=0.8, scale=4, mode="noise")
        assert a.equals(b)

    def test_cusped_shapes_stay_valid(self):
        circle = [{"op": "circle", "out": "s", "center": [20, 15], "r": 6}]
        g = rough(circle, mode="cusps", amount=1.0, period=1.5)
        assert g.is_valid and not g.is_empty
