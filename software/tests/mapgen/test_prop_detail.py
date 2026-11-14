"""Prop detail round (owner, 2026-11-14: "crates, bridges etc still look less detailed ... mostly
shading lines"): bevelled faces toned by light direction, grain, nails, uneven bridge planks."""
import numpy as np
import pytest
import shapely
from shapely.geometry import LineString, Polygon, box

import mapgen.ops.props as P
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft


def canvas(steps):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + steps, **H)
    return store.get("canvas").data


def parts(kind, size=None, seed=1):
    fn, default = P.PROPS[kind]
    return fn(size or default, np.random.default_rng(seed))


class TestFacetTone:
    def test_south_east_face_is_dark(self):
        face = box(1, 1, 2, 2)                                  # centroid south-east of the prop centre
        assert P._facet_tone("wood", face, (0, 0)) == "wood_dark"

    def test_north_west_face_is_light(self):
        assert P._facet_tone("wood", box(-2, -2, -1, -1), (0, 0)) == "wood_light"

    def test_side_face_keeps_base_and_unknown_base_falls_back(self):
        assert P._facet_tone("wood", box(1, -2, 2, -1), (0, 0)) == "wood"        # north-east: across the light
        assert P._facet_tone("rug", box(1, 1, 2, 2), (0, 0)) == "rug"
        assert P._facet_tone("wood", box(-1, -1, 1, 1), (0, 0)) == "wood"        # centred: no direction

    @pytest.mark.parametrize("rotate", [0, 90, 180, 270])
    def test_crate_dark_face_stays_south_east_when_rotated(self, rotate):
        c = canvas([{"op": "prop", "kind": "crate", "at": [20, 15], "size": 8, "rotate": rotate, "shadow": 0, "id": "p"}])
        lum = c[..., :3].mean(-1)
        # bevel band centres: 8 ft crate at 8 px/ft -> 64 px, faces ~1 ft deep inside the edge
        south = lum[120 + 60 // 2 - 2:120 + 32 - 2, 150:170].mean()             # inside the south edge
        north = lum[120 - 32 + 2:120 - 32 + 8, 150:170].mean()                  # inside the north edge
        assert south < north


class TestMergeLineRuns:
    def test_consecutive_same_width_lines_merge(self):
        a, b = LineString([(0, 0), (1, 0)]), LineString([(0, 1), (1, 1)])
        out = P._merge_line_runs([(a, None, 0.1), (b, None, 0.1)])
        assert len(out) == 1 and out[0][0].geom_type == "MultiLineString" and len(out[0][0].geoms) == 2

    def test_different_widths_or_fills_break_the_run(self):
        a, b = LineString([(0, 0), (1, 0)]), LineString([(0, 1), (1, 1)])
        poly = box(0, 0, 1, 1)
        out = P._merge_line_runs([(a, None, 0.1), (b, None, 0.2), (poly, "wood", 0.1), (a, None, 0.2)])
        assert [o[2] for o in out] == [0.1, 0.2, 0.1, 0.2]

    def test_paint_order_kept_across_a_fill(self):
        a = LineString([(0, 0), (1, 0)])
        poly = box(0, 0, 1, 1)
        out = P._merge_line_runs([(a, None, 0.1), (poly, "wood", 0), (a, None, 0.1)])
        assert len(out) == 3 and out[1][1] == "wood"

    def test_rings_merge_with_lines(self):
        ring = shapely.Point(0, 0).buffer(1).exterior
        out = P._merge_line_runs([(ring, None, 0.1), (LineString([(0, 0), (1, 1)]), None, 0.1)])
        assert len(out) == 1


class TestCrate:
    def test_has_bevel_faces_nails_and_detail(self):
        ps = parts("crate", 2.5)
        assert sum(1 for _, ck, _ in ps if ck == "facet:wood") == 4
        assert sum(1 for _, ck, _ in ps if ck == "ink_fill") == 4
        assert sum(1 for g, ck, _ in ps if ck is None and g.geom_type == "LineString") >= 6

    def test_styles_vary_with_seed(self):
        braces = {sum(1 for g, ck, iw in parts("crate", 2.5, seed=s) if ck == "wood" and iw and iw < P.INK_MED)
                  for s in range(12)}
        assert len(braces) >= 2

    def test_deterministic_per_seed(self):
        a, b = parts("crate", 2.5, 7), parts("crate", 2.5, 7)
        assert all(x[0].equals(y[0]) for x, y in zip(a, b))


class TestBridge:
    @pytest.mark.parametrize("seed", range(6))
    def test_planks_cover_the_deck_end_to_end(self, seed):
        s = 10
        ps = parts("bridge", s, seed)
        planks = shapely.unary_union([g for g, ck, _ in ps if ck == "wood_light"])
        minx, _, maxx, _ = planks.bounds
        assert minx < -s / 2 + 0.1 and maxx > s / 2 - 0.1

    def test_planks_are_uneven(self):
        ps = parts("bridge", 10, 3)
        widths = [g.bounds[2] - g.bounds[0] for g, ck, _ in ps if ck == "wood_light"]
        assert len(widths) >= 8 and np.std(widths) > 0.05

    def test_rope_rails_and_four_posts(self):
        ps = parts("bridge", 10, 3)
        assert sum(1 for _, ck, _ in ps if ck == "linen") == 2
        posts = [g for g, ck, _ in ps if ck == "wood" and g.geom_type == "Polygon"]
        assert len(posts) == 4

    def test_short_bridge_still_builds(self):
        ps = parts("bridge", 1.0, 0)
        assert any(ck == "wood_light" for _, ck, _ in ps)


class TestBarrelAndChest:
    def test_barrel_has_grain_hoop_and_bung(self):
        ps = parts("barrel", 2.5)
        assert sum(1 for _, ck, _ in ps if ck == "wood_dark") == 1
        assert sum(1 for g, ck, _ in ps if ck is None) >= 14 + 3

    def test_chest_has_bands_and_rivets(self):
        ps = parts("chest", 3)
        assert sum(1 for _, ck, _ in ps if ck == "metal") == 3
        assert sum(1 for _, ck, _ in ps if ck == "ink_fill") == 7

    def test_crate_carries_far_more_line_work_than_a_plain_box(self, monkeypatch):
        step = [{"op": "prop", "kind": "crate", "at": [20, 15], "size": 8, "shadow": 0, "id": "p"}]

        def edges(c):
            lum = c[100:140, 140:180, :3].mean(-1)                   # inside the crate, clear of its outline
            return (np.abs(np.diff(lum, axis=0)) > 0.08).sum() + (np.abs(np.diff(lum, axis=1)) > 0.08).sum()

        detailed = edges(canvas(step))
        monkeypatch.setitem(P.PROPS, "crate", (lambda s, rng: [(box(-s / 2, -s / 2, s / 2, s / 2), "wood", P.INK_MED)], 2.5))
        assert detailed > 3 * max(edges(canvas(step)), 1)
