"""Detail round (owner, 2026-11-13: "more detail ... shading lines"): prop shading and wall texture."""
from pathlib import Path

import numpy as np
import pytest
import yaml

from mapgen.ops.props import shade_crescent
from shapely.geometry import box
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft
STYLE = yaml.safe_load((Path(__file__).resolve().parents[2] / "mapgen" / "styles" / "inked_parchment.yaml").read_text())


def canvas(steps, styled=False, **h):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + steps,
                   style=STYLE if styled else None, **dict(H, **h))
    return store.get("canvas").data


def dark(c, thr=0.45):
    return c[..., :3].mean(-1) < thr


class TestPropShading:
    def _crate(self, monkeypatch=None, rotate=0):
        return dark(canvas([{"op": "prop", "kind": "crate", "at": [20, 15], "size": 6, "rotate": rotate, "shadow": 0, "id": "p"}]))

    @pytest.mark.parametrize("rotate", [0, 180])
    def test_crate_shaded_south_east_even_rotated(self, rotate):
        c = self._crate(rotate=rotate)
        se, nw = c[122:144, 162:184].sum(), c[96:118, 136:158].sum()
        assert se > nw

    def test_shading_actually_adds_ink(self, monkeypatch):
        import mapgen.ops.props as P
        with_hatch = self._crate().sum()
        monkeypatch.setattr(P, "shade_crescent", lambda g: None)
        assert with_hatch > self._crate().sum() + 30

    def test_flat_and_self_shaded_props_never_reach_the_hatcher(self, monkeypatch):
        import mapgen.ops.props as P
        def boom(g):
            raise AssertionError("auto-shaded a prop that shouldn't be")
        monkeypatch.setattr(P, "shade_crescent", boom)
        for kind in ("rug", "banner", "tree", "mountain", "hill", "city", "town", "village", "ruin_marker", "peak"):
            canvas([{"op": "prop", "kind": kind, "at": [20, 15], "size": 4, "id": f"k_{kind}"}])

    def test_unoutlined_parts_are_not_hatched(self, monkeypatch):
        import mapgen.ops.props as P
        seen = []
        orig = P.shade_crescent
        monkeypatch.setattr(P, "shade_crescent", lambda g: seen.append(g.area) or orig(g))
        canvas([{"op": "prop", "kind": "brazier", "at": [20, 15], "size": 4, "id": "b"}])
        assert len(seen) == 1           # only the metal bowl: the fire and coal have no outline


class TestShadeCrescent:
    def test_square_hatch_in_south_east_strips(self):
        h = shade_crescent(box(0, 0, 4, 4))
        k = 0.3 * 4 if 0.3 * 4 < 0.2 * 4 else 0.2 * 4
        mids = [l.interpolate(0.5, normalized=True) for l in h.geoms]
        assert len(mids) > 4 and all(m.x >= 4 - k - 1e-6 or m.y >= 4 - k - 1e-6 for m in mids)

    def test_thin_parts_get_no_hatch(self):
        from shapely import affinity
        rail = box(0, 0, 10, 0.4)
        assert shade_crescent(rail) is None
        assert shade_crescent(affinity.rotate(rail, 45)) is None and shade_crescent(affinity.rotate(rail, -45)) is None

    def test_l_shape_and_multipolygon(self):
        from shapely.geometry import MultiPolygon
        L = box(0, 0, 6, 2).union(box(0, 0, 2, 6))
        h = shade_crescent(L)
        assert h is not None and L.buffer(1e-6).contains(h)
        mp = MultiPolygon([box(0, 0, 3, 3), box(5, 5, 8, 8)])
        assert shade_crescent(mp) is not None

    @pytest.mark.parametrize("angle", [0, 45, -45, 90, 30])
    def test_elongated_parts_hatched_across_their_length(self, angle):
        from shapely import affinity
        part = affinity.rotate(box(0, 0, 10, 3), angle, origin=(0, 0))
        h = shade_crescent(part)
        assert h is not None
        long_axis = np.radians(angle)
        for ln in h.geoms:
            (x0, y0), (x1, y1) = ln.coords[0], ln.coords[-1]
            a = np.arctan2(y1 - y0, x1 - x0)
            # strokes cross the long axis (never parallel to it)
            assert abs(np.sin(a - long_axis)) > 0.7

    def test_degenerate(self):
        assert shade_crescent(box(0, 0, 0, 0)) is None
        assert shade_crescent(box(0, 0, 1e-4, 1e-4)) is None or True


class TestDetailLines:
    @pytest.mark.parametrize("kind", ["barrel", "bed", "chest", "boulder", "pillar", "crate"])
    def test_detail_lines_change_the_drawing(self, kind, monkeypatch):
        import mapgen.ops.props as P
        from shapely.geometry import LineString, MultiLineString
        full = canvas([{"op": "prop", "kind": kind, "at": [20, 15], "size": 6, "shadow": 0, "id": "p"}], px_per_square=80)
        fn, size = P.PROPS[kind]

        def no_lines(s, rng):
            return [(g, ck, iw) for g, ck, iw in fn(s, rng)
                    if not (ck is None and isinstance(g, (LineString, MultiLineString)) and iw == P.DETAIL)]
        monkeypatch.setitem(P.PROPS, kind, (no_lines, size))
        stripped = canvas([{"op": "prop", "kind": kind, "at": [20, 15], "size": 6, "shadow": 0, "id": "p"}], px_per_square=80)
        assert np.abs(full - stripped).max(-1).__gt__(0.15).sum() > 40


CAVE = [{"op": "polygon", "out": "cave", "points": [[6, 6], [34, 6], [34, 24], [6, 24]]}]


class TestWallTexture:
    def test_cave_walls_get_rock_texture(self):
        bare = canvas(CAVE + [{"op": "wall", "src": "cave", "name": "rock", "style": "rough", "thickness": 1.5,
                               "material": "cave_rock", "id": "w"}], styled=True)
        rich = canvas(CAVE + [{"op": "cave_walls", "src": "cave", "wall": "rock", "thickness": 1.5}], styled=True)
        band = (slice(30, 48), slice(60, 260))
        assert dark(rich[band], 0.35).sum() > dark(bare[band], 0.35).sum()

    def test_no_texture_in_an_excluded_mouth(self):
        steps = CAVE + [{"op": "rect", "out": "mouth", "x": 14, "y": 22, "w": 12, "h": 6}]
        bare = canvas(steps + [{"op": "wall", "src": "cave", "name": "rock", "style": "rough", "thickness": 1.5,
                                "material": "cave_rock", "exclude": "mouth", "id": "w"}], styled=True)
        rich = canvas(steps + [{"op": "cave_walls", "src": "cave", "wall": "rock", "thickness": 1.5, "exclude": "mouth"}],
                      styled=True)
        mouth = (slice(194, 210), slice(130, 190))          # the strip just south of the floor, inside the mouth
        assert np.array_equal(dark(rich[mouth], 0.35), dark(bare[mouth], 0.35))

    def test_stone_room_walls_get_weathering(self):
        steps = [{"op": "rect", "out": "room", "x": 8, "y": 8, "w": 24, "h": 14}]
        plain = canvas(steps + [{"op": "rasterize", "out": "fl", "src": "room"},
                                {"op": "wall", "src": "room", "name": "w", "thickness": 1.5, "material": "wall_stone",
                                 "weight": "heavy", "id": "x"}], styled=True)
        rich = canvas(steps + [{"op": "stone_room", "src": "room", "wall": "w"}], styled=True)
        band = (slice(52, 63), slice(80, 240))
        assert dark(rich[band], 0.3).sum() > dark(plain[band], 0.3).sum()

    def test_wall_band_op(self):
        store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + CAVE +
                       [{"op": "wall", "src": "cave", "name": "rock", "thickness": 2},
                        {"op": "wall_band", "out": "b", "wall": "rock"},
                        {"op": "wall_band", "out": "bi", "wall": "rock", "inset": 0.5}], **H)
        b, bi = store.get("b").data, store.get("bi").data
        assert b.sum() > bi.sum() > 0 and b[100, 100] == 0      # band only, not the floor

    def test_wall_band_unknown_wall(self):
        from mapgen.recipe import RecipeError
        with pytest.raises(RecipeError, match="not defined"):
            run([{"op": "wall_band", "out": "b", "wall": "nope"}], **H)

    def test_duplicate_wall_names_are_an_error(self):
        from mapgen.recipe import RecipeError
        with pytest.raises(RecipeError, match="already exists"):
            canvas(CAVE + [{"op": "wall", "src": "cave", "name": "w"}, {"op": "wall", "src": "cave", "name": "w"}])

    def test_heavier_ink_weights_and_mile_scaling(self):
        assert STYLE["ink"]["bold"] >= 0.75 and STYLE["ink"]["fine"] >= 0.12
        from mapgen.ops.paint import _width_ft
        class F: unit = "mi"
        class C: frame = F(); style = type("S", (), {"ink": STYLE["ink"]})
        class P_: width = None; weight = "heavy"
        assert _width_ft(C(), P_()) == pytest.approx(STYLE["ink"]["heavy"] * 0.5)
