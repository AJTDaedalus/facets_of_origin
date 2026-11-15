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
NEW = ["card_table", "dice_table", "wheel", "counter", "stool", "shelf", "hearth"]


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
