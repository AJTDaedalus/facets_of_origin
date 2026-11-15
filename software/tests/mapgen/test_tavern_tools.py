"""Tavern round (owner, 2026-11-15: a forest tavern and gambling hall, "lots of bright colors", each wing
with its own flair): per-step prop colours, gaming and shop props, timber and wattle materials."""
from pathlib import Path

import numpy as np
import pytest
import yaml

import mapgen.ops.props as P
from mapgen.recipe import RecipeError
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft
STYLE = yaml.safe_load((Path(__file__).resolve().parents[2] / "mapgen" / "styles" / "inked_parchment.yaml").read_text())
NEW = ["card_table", "dice_table", "wheel", "counter", "stool", "shelf", "hearth", "clutter", "sack", "boards", "palm"]


def canvas(steps, styled=False):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + steps,
                   style=STYLE if styled else None, **H)
    return store.get("canvas").data


def parts(kind, size=None, seed=1):
    fn, default = P.PROPS[kind]
    return fn(size or default, np.random.default_rng(seed))


@pytest.mark.parametrize("kind", NEW)
@pytest.mark.parametrize("size", [0.3, 1.0, 3.0, 12.0])
def test_new_props_are_valid_geometry(kind, size):
    for seed in range(5):
        for g, ck, iw in parts(kind, size, seed):
            assert not g.is_empty and g.is_valid, (kind, size, seed, ck)
            if ck:
                assert g.geom_type in ("Polygon", "MultiPolygon")
            else:
                assert g.geom_type in ("LineString", "MultiLineString", "LinearRing") and iw > 0


@pytest.mark.parametrize("kind", NEW)
def test_new_props_draw_and_fit_their_size(kind):
    c = canvas([{"op": "prop", "kind": kind, "at": [20, 15], "size": 6, "shadow": 0, "id": "p"}])
    drawn = c[..., :3].mean(-1) < 0.97
    ys, xs = np.nonzero(drawn)
    assert drawn.sum() > 50
    assert xs.max() - xs.min() <= 6 * 8 + 4 and ys.max() - ys.min() <= 6 * 8 + 4


class TestGamingProps:
    def test_card_table_has_felt_cards_and_chips(self):
        ps = parts("card_table", 5)
        assert sum(1 for _, ck, _ in ps if ck == "felt") == 1
        assert sum(1 for _, ck, _ in ps if ck == "linen") >= 3            # cards
        assert sum(1 for _, ck, _ in ps if ck == "chip") >= 2

    def test_dice_table_is_oblong_with_a_rail(self):
        ps = parts("dice_table", 6)
        rail = next(g for g, ck, _ in ps if ck == "wood")
        minx, miny, maxx, maxy = rail.bounds
        assert (maxx - minx) > 1.6 * (maxy - miny)
        assert any(ck == "felt" for _, ck, _ in ps)

    def test_wheel_has_alternating_wedges(self):
        ps = parts("wheel", 4)
        wedges = [ck for g, ck, _ in ps if ck in ("cloth", "felt", "rug_trim", "linen") and g.area < 4]
        assert len(wedges) >= 8 and len(set(wedges)) >= 3

    def test_cards_vary_with_seed(self):
        a = [g.centroid.coords[0] for g, ck, _ in parts("card_table", 5, 1) if ck == "linen"]
        b = [g.centroid.coords[0] for g, ck, _ in parts("card_table", 5, 2) if ck == "linen"]
        assert a != b


class TestShopProps:
    def test_counter_is_long_and_shallow_with_mugs(self):
        ps = parts("counter", 12)
        top = ps[0][0]
        minx, miny, maxx, maxy = top.bounds
        assert maxx - minx == pytest.approx(12) and maxy - miny <= 2.6
        assert sum(1 for _, ck, _ in ps if ck == "metal") >= 2

    def test_shelf_carries_coloured_goods(self):
        goods = {ck for _, ck, _ in parts("shelf", 8) if ck not in ("wood", "wood_dark", None)}
        assert len(goods) >= 3

    def test_hearth_has_fire(self):
        assert any(ck == "fire" for _, ck, _ in parts("hearth", 5))


class TestColorOverrides:
    def test_prop_colors_change_only_the_named_part(self):
        step = {"op": "prop", "kind": "card_table", "at": [20, 15], "size": 8, "shadow": 0, "id": "p"}
        plain = canvas([step])
        red = canvas([dict(step, colors={"felt": "#d01010"})])
        centre = (slice(118, 122), slice(158, 162))                      # middle of the felt
        assert red[centre][..., 0].mean() > 0.7 and red[centre][..., 1].mean() < 0.3
        assert not np.allclose(plain[centre], red[centre])
        rim = (slice(120 - 31, 120 - 29), slice(158, 162))               # the wood rim, 8 ft table at 8 px/ft
        assert np.allclose(plain[rim], red[rim], atol=0.02)

    def test_scatter_passes_colors_to_every_prop(self):
        steps = [{"op": "rect", "out": "r", "x": 2, "y": 2, "w": 36, "h": 26},
                 {"op": "rasterize", "out": "rm", "src": "r"}]
        sc = {"op": "scatter", "kind": "rug", "mask": "rm", "density": 0.5, "spacing": 8, "size": 5, "id": "s"}
        a = canvas(steps + [sc])
        b = canvas(steps + [dict(sc, colors={"rug": "#1060e0"})])
        assert (b[..., 2] - b[..., 0] > 0.4).sum() > 200 and (a[..., 2] - a[..., 0] > 0.4).sum() == 0

    def test_palette_names_work_in_overrides(self):
        c = canvas([{"op": "prop", "kind": "rug", "at": [20, 15], "size": 8, "shadow": 0, "id": "p",
                     "colors": {"rug": "secret"}}], styled=True)
        assert c[118:122, 158:162, 0].mean() > c[118:122, 158:162, 2].mean() + 0.2      # the style's red

    def test_bad_override_colour_is_an_error(self):
        with pytest.raises(RecipeError):
            canvas([{"op": "prop", "kind": "rug", "at": [20, 15], "id": "p", "colors": {"rug": "not-a-colour"}}])

    def test_no_override_is_unchanged(self):
        step = {"op": "prop", "kind": "bed", "at": [20, 15], "size": 6, "id": "p"}
        assert np.array_equal(canvas([step]), canvas([dict(step, colors={})]))


class TestTavernMaterials:
    @pytest.mark.parametrize("name", ["wall_timber", "wall_wattle", "rushes", "wood_floor_rough"])
    def test_material_exists_and_renders(self, name):
        assert name in STYLE["materials"]
        c = canvas([{"op": "fill", "material": name, "id": "f"}], styled=True)
        assert c[..., :3].std() > 0.01                                   # textured, not flat


class TestDarkness:
    def lum(self, steps):
        return canvas(steps)[..., :3].mean(-1)

    def test_darkens_everything_without_lights(self):
        base = self.lum([])
        dark = self.lum([{"op": "darkness", "strength": 0.6}])
        assert dark.mean() < base.mean() * 0.6

    def test_lights_open_pools(self):
        l = self.lum([{"op": "light", "at": [10, 15], "radius": 16},
                      {"op": "darkness", "strength": 0.7, "pool": 0.5}])
        assert l[120, 80] > 0.95 and l[120, 300] < 0.5             # at the lamp vs 27 ft away

    def test_only_earlier_lights_count(self):
        l = self.lum([{"op": "darkness", "strength": 0.7}, {"op": "light", "at": [10, 15], "radius": 16}])
        assert l[120, 80] < 0.5

    def test_pool_size_follows_radius_and_pool(self):
        small = self.lum([{"op": "light", "at": [20, 15], "radius": 8}, {"op": "darkness", "strength": 0.7, "pool": 0.5}])
        big = self.lum([{"op": "light", "at": [20, 15], "radius": 24}, {"op": "darkness", "strength": 0.7, "pool": 0.5}])
        assert (big > 0.8).sum() > 4 * (small > 0.8).sum() > 0

    def test_mask_limits_it(self):
        steps = [{"op": "rect", "out": "w", "x": 0, "y": 0, "w": 20, "h": 30},
                 {"op": "rasterize", "out": "wm", "src": "w"}, {"op": "darkness", "strength": 0.7, "mask": "wm"}]
        l = self.lum(steps)
        assert l[:, :150].mean() < 0.5 and l[:, 170:].mean() > 0.95

    def test_warm_tints_the_pools(self):
        c = canvas([{"op": "light", "at": [20, 15], "radius": 16},
                    {"op": "darkness", "strength": 0.7, "pool": 0.5, "warm": "#ff9040", "warmth": 0.5}])
        ring = c[120, 160 + 30]                                      # inside the pool, off its centre
        assert ring[0] > ring[2] + 0.05

    def test_vtt_lights_unchanged(self):
        _, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "light", "at": [20, 15], "radius": 16},
                    {"op": "darkness", "strength": 0.7}], **H)
        assert len(e.collector.lights) == 1


class TestTransform:
    def geom(self, **kw):
        from tests.mapgen.helpers import layer
        return layer([{"op": "rect", "out": "r", "x": 10, "y": 10, "w": 10, "h": 4},
                      dict({"op": "transform", "out": "t", "src": "r"}, **kw)], "t", **H).geom

    def test_rotate_about_centroid_keeps_area_and_centre(self):
        g = self.geom(rotate=30)
        assert g.area == pytest.approx(40) and g.centroid.distance(shapely.Point(15, 12)) < 1e-6
        assert g.bounds[3] - g.bounds[1] > 4.5

    def test_rotate_about_a_point_and_move(self):
        g = self.geom(rotate=90, about=[10, 10], move=[1, 2])
        minx, miny, maxx, maxy = g.bounds
        assert (minx, miny, maxx, maxy) == pytest.approx((7, 12, 11, 22))

    def test_scale(self):
        assert self.geom(scale=2).area == pytest.approx(160)

    def test_skew_makes_a_parallelogram(self):
        g = self.geom(skew=[15, 0])
        assert g.area == pytest.approx(40) and len(g.exterior.coords) == 5 and not g.equals(self.geom())

    def test_identity(self):
        assert self.geom().equals(self.geom(rotate=0, move=[0, 0], scale=1))


import shapely  # noqa: E402


class TestClutter:
    def test_clutter_is_many_small_items_inside_its_size(self):
        ps = parts("clutter", 4)
        assert len([1 for _, ck, _ in ps if ck]) >= 4
        allg = shapely.unary_union([g for g, _, _ in ps])
        assert shapely.Point(0, 0).buffer(2.01).contains(allg)

    def test_clutter_varies_with_seed(self):
        k = lambda seed: sorted(ck for _, ck, _ in parts("clutter", 4, seed) if ck)
        assert len({tuple(k(sd)) for sd in range(6)}) >= 3

    def test_sack_is_lumpy(self):
        g = next(g for g, ck, _ in parts("sack", 2.5) if ck == "sack")
        assert len(g.exterior.coords) > 10 and g.area < 2.5 * 2.5


class TestBoards:
    def test_a_few_uneven_loose_planks(self):
        planks = [g for g, ck, _ in parts("boards", 8) if ck in ("wood", "wood_light", "wood_dark")]
        assert 3 <= len(planks) <= 5
        lengths = [max(g.bounds[2] - g.bounds[0], g.bounds[3] - g.bounds[1]) for g in planks]
        assert np.std(lengths) > 0.05 and max(lengths) <= 8 + 1e-6

    def test_planks_span_the_long_way(self):
        allg = shapely.unary_union([g for g, ck, _ in parts("boards", 8) if ck])
        minx, miny, maxx, maxy = allg.bounds
        assert maxx - minx > 6.5 and maxy - miny < 4

    def test_mud_material(self):
        assert "mud" in STYLE["materials"]
        c = canvas([{"op": "fill", "material": "mud", "id": "f"}], styled=True)
        assert c[..., :3].mean() < 0.5 and c[..., :3].std() > 0.01


class TestPalm:
    """Mists region (owner concept art, 2026-11-15): thin palms behind the beach."""

    def test_radiating_fronds_with_midribs(self):
        ps = parts("palm", 8)
        fronds = [g for g, ck, _ in ps if ck in ("palm", "palm_dark") and g.area > 0.2]
        ribs = [g for g, ck, _ in ps if ck is None]
        assert 6 <= len(fronds) <= 11 and len(ribs) >= len(fronds)
        angles = sorted(np.degrees(np.arctan2(g.centroid.y, g.centroid.x)) % 360 for g in fronds)
        assert max(np.diff(angles + [angles[0] + 360])) < 120          # spread all round, no big empty side

    def test_fronds_vary_with_seed(self):
        a = [round(g.area, 3) for g, ck, _ in parts("palm", 8, 1) if ck == "palm"]
        b = [round(g.area, 3) for g, ck, _ in parts("palm", 8, 2) if ck == "palm"]
        assert a != b

    def test_palm_ignores_rotate_for_its_shading(self):
        a = canvas([{"op": "prop", "kind": "palm", "at": [20, 15], "size": 8, "id": "p"}])
        b = canvas([{"op": "prop", "kind": "palm", "at": [20, 15], "size": 8, "rotate": 90, "id": "p"}])
        assert np.array_equal(a, b)


class TestRasterizeSpeed:
    """2026-11-15: a meadow outline of ~2,300 parts took 94 s because every holed geometry drew each part
    on a full-size layer. Holed parts now use bounding-box layers; the coverage must not change."""

    def _slow_reference(self, frame, g):
        from PIL import Image as PImage, ImageChops, ImageDraw
        from mapgen.ops.masks import polygons_of
        s = frame.scale
        H, W = frame.shape
        img = PImage.new("L", (W * 4, H * 4), 0)
        ring = lambda c: [((x * s) * 4 - 0.5, (y * s) * 4 - 0.5) for x, y in c]
        for pg in polygons_of(g):
            layer = PImage.new("L", img.size, 0)
            ld = ImageDraw.Draw(layer)
            ld.polygon(ring(pg.exterior.coords), fill=255)
            for h in pg.interiors:
                ld.polygon(ring(h.coords), fill=0)
            img = ImageChops.lighter(img, layer)
        return np.asarray(img, np.float32).reshape(H, 4, W, 4).mean(axis=(1, 3)) / 255.0

    def test_lake_with_island_and_many_parts_match_the_full_layer_method(self):
        from shapely.geometry import MultiPolygon, Point, box
        from mapgen.ops.masks import rasterize_geom
        from tests.mapgen.helpers import run
        _, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}], **H)
        lake = box(2, 2, 20, 20).difference(box(6, 6, 16, 16))          # a ring with a hole
        island = box(9, 9, 13, 13)                                       # inside the hole
        dots = [Point(25 + (i % 6) * 2.2, 3 + (i // 6) * 2.2).buffer(0.8) for i in range(30)]
        g = MultiPolygon([island, lake] + dots)                          # island listed before the lake
        fast = rasterize_geom(e.frame, g)
        ref = self._slow_reference(e.frame, g)
        assert np.allclose(fast, ref, atol=1e-6)
        assert fast[int(11 * 8), int(11 * 8)] > 0.99                     # the island survives the lake's hole

    def test_many_parts_are_fast(self):
        import time
        from shapely.geometry import MultiPolygon, Point, box
        from mapgen.ops.masks import rasterize_geom
        from tests.mapgen.helpers import run
        _, e = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}], **H)
        holed = box(1, 1, 3, 3).difference(box(1.5, 1.5, 2.5, 2.5))
        g = MultiPolygon([holed] + [Point(4 + (i % 40) * 0.9, 4 + (i // 40) * 0.9).buffer(0.3) for i in range(1000)])
        t = time.perf_counter()
        rasterize_geom(e.frame, g)
        assert time.perf_counter() - t < 3.0


class TestReviewPR41:
    """docs/REVIEW_pr41.md."""

    def test_r1_overrides_accept_prop_part_names(self):
        a = canvas([{"op": "prop", "kind": "rug", "at": [20, 15], "size": 8, "shadow": 0, "id": "p", "colors": {"rug": "cloth"}}])
        b = canvas([{"op": "prop", "kind": "rug", "at": [20, 15], "size": 8, "shadow": 0, "id": "p", "colors": {"rug": P.COLORS["cloth"]}}])
        assert np.array_equal(a, b)

    def test_r1_unknown_name_still_errors(self):
        with pytest.raises(RecipeError):
            canvas([{"op": "prop", "kind": "rug", "at": [20, 15], "id": "p", "colors": {"rug": "no_such_name"}}])

    @pytest.mark.parametrize("skew", [[90, 0], [-85, 0], [45, 45], [0, 89]])
    def test_r4_degenerate_skew_is_refused(self, skew):
        from tests.mapgen.helpers import layer
        with pytest.raises(RecipeError):
            layer([{"op": "rect", "out": "r", "x": 10, "y": 10, "w": 10, "h": 4},
                   {"op": "transform", "out": "t", "src": "r", "skew": skew}], "t", **H)

    def test_r4_moderate_skew_is_fine(self):
        from tests.mapgen.helpers import layer
        g = layer([{"op": "rect", "out": "r", "x": 10, "y": 10, "w": 10, "h": 4},
                   {"op": "transform", "out": "t", "src": "r", "skew": [30, 10]}], "t", **H).geom
        assert g.is_valid and g.area > 0
