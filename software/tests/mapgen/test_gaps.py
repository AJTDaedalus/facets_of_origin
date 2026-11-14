"""Tool gaps found building the misty coast (owner, 2026-11-14: "take on each gap"):
1 recipe-level palette/materials/ink, 2 directional noise and warp, 3 prop footprint masks,
4 atmosphere steps judged underneath by `quality`."""
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import yaml

from mapgen.engine import Engine
from mapgen.recipe import RecipeError, Style, load_recipe, parse_recipe
from tests.mapgen.conftest import header
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft
WHITE = {"op": "canvas", "out": "canvas", "color": "#ffffff"}


def recipe(steps, style=None, **extra):
    return parse_recipe({"map": header(**H), "steps": steps, **extra}, style=Style(**(style or {})))


def render(r, **kw):
    e = Engine(r, **kw)
    return e.run(keep_all=True), e


# ---------------------------------------------------------------- 1 recipe-level style
class TestRecipeStyle:
    def test_recipe_palette_overrides_include(self):
        r = recipe([WHITE], style={"palette": {"ink": "#000000", "x": "#111111"}}, palette={"ink": "#ff0000"})
        assert r.style.palette["ink"] == "#ff0000" and r.style.palette["x"] == "#111111"

    def test_recipe_material_is_usable_by_a_step(self):
        mats = {"pink_sand": {"type": "dirt", "colors": ["#f0a0a0", "#f4b0b0", "#f8c0c0"], "scale": 6}}
        r = recipe([WHITE, {"op": "fill", "material": "pink_sand"}], materials=mats)
        store, _ = render(r)
        c = store.get("canvas").data[..., :3].mean((0, 1))
        assert c[0] > c[1] + 0.1                                   # reddish: the recipe's material drew

    def test_recipe_ink_and_material_merge_per_entry(self):
        r = recipe([WHITE], style={"materials": {"a": {"type": "dirt"}}, "ink": {"heavy": 0.5, "fine": 0.1}},
                   materials={"b": {"type": "dirt"}}, ink={"fine": 0.2})
        assert set(r.style.materials) == {"a", "b"} and r.style.ink == {"heavy": 0.5, "fine": 0.2}

    def test_non_mapping_is_an_error(self):
        with pytest.raises(RecipeError, match="palette"):
            recipe([WHITE], palette=["#fff"])

    def test_other_unknown_top_level_keys_still_rejected(self):
        with pytest.raises(RecipeError):
            recipe([WHITE], colours={"ink": "#000"})

    def test_macros_see_the_recipe_palette(self):
        style = {"macros": {"paint_it": {"params": {}, "steps": [{"op": "fill", "color": "mine"}]}}}
        r = recipe([WHITE, {"op": "paint_it"}], style=style, palette={"mine": "#0000ff"})
        store, _ = render(r)
        assert store.get("canvas").data[10, 10, 2] > 0.9

    def test_coast_recipe_loads_with_inline_style(self):
        p = Path(__file__).resolve().parents[3] / "maps" / "recipes" / "mist_coast.map.yaml"
        r = load_recipe(p)
        assert "white_sand" in r.style.materials and r.style.palette["stone"] == "#2a2c30"


# ---------------------------------------------------------------- 2 directional noise, warp
def _corr(a, dy, dx):
    a = a - a.mean()
    h, w = a.shape
    x = a[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)]
    y = a[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return float((x * y).mean() / (a.var() + 1e-9))


def noise(**kw):
    store, _ = run([{"op": "noise", "out": "n", "scale": 4, "octaves": 2, "id": "n", **kw}], **H)
    return store.get("n").data


class TestDirectionalNoise:
    def test_stretch_along_east_correlates_further_east_than_south(self):
        n = noise(stretch=5, angle=0)
        assert _corr(n, 0, 24) > _corr(n, 24, 0) + 0.3

    def test_angle_90_runs_south(self):
        n = noise(stretch=5, angle=90)
        assert _corr(n, 24, 0) > _corr(n, 0, 24) + 0.3

    def test_stretch_one_is_the_old_isotropic_noise(self):
        from mapgen.noise import fbm
        store, e = run([{"op": "noise", "out": "n", "scale": 4, "octaves": 2, "id": "n"}], **H)
        assert np.array_equal(store.get("n").data, fbm(e.frame.shape, e.frame.px(4), e.recipe and _seed(e, "n"), 2))

    def test_range_and_determinism(self):
        a, b = noise(stretch=3, angle=30), noise(stretch=3, angle=30)
        assert np.array_equal(a, b) and a.min() >= -1 and a.max() <= 1 and a.std() > 0.05

    def test_stretch_bounds_validated(self):
        with pytest.raises(RecipeError):
            run([{"op": "noise", "out": "n", "stretch": 0.5}], **H)


def _seed(e, key):
    from mapgen.engine import step_seed
    return step_seed(e.recipe.map.seed, key, 0)


class TestWarp:
    def _mask(self, **kw):
        steps = [{"op": "rect", "out": "r", "x": 15, "y": 10, "w": 10, "h": 10},
                 {"op": "rasterize", "out": "m", "src": "r"},
                 {"op": "warp", "out": "w", "src": "m", "id": "w", **kw}]
        store, _ = run(steps, **H)
        return store.get("m"), store.get("w")

    def test_mask_in_mask_out(self):
        from mapgen.layers import Mask
        _, w = self._mask()
        assert isinstance(w, Mask)

    def test_field_in_field_out(self):
        from mapgen.layers import Field
        store, _ = run([{"op": "noise", "out": "n"}, {"op": "warp", "out": "w", "src": "n"}], **H)
        assert isinstance(store.get("w"), Field)

    def test_amount_moves_edges(self):
        m, w = self._mask(amount=2, scale=4)
        assert np.abs(m.data - w.data).sum() > 50

    def test_drift_pushes_downstream(self):
        m, w = self._mask(amount=0.01, drift=[3, 0])          # 3 ft east, almost no swirl
        xs_m = np.nonzero(m.data.sum(0) > 1)[0]
        xs_w = np.nonzero(w.data.sum(0) > 1)[0]
        assert xs_w.min() - xs_m.min() == pytest.approx(24, abs=2)

    def test_deterministic(self):
        assert np.array_equal(self._mask()[1].data, self._mask()[1].data)

    def test_geometry_rejected(self):
        with pytest.raises(RecipeError, match="needs a"):
            run([{"op": "rect", "out": "r", "x": 1, "y": 1, "w": 2, "h": 2}, {"op": "warp", "out": "w", "src": "r"}], **H)


def _edge(m):
    b = m > 0.5
    return int((b[1:] != b[:-1]).sum() + (b[:, 1:] != b[:, :-1]).sum())


class TestWarpSwirl:
    def _w(self, **kw):
        steps = [{"op": "circle", "out": "c", "center": [20, 15], "r": 8},
                 {"op": "rasterize", "out": "m", "src": "c"},
                 {"op": "warp", "out": "w", "src": "m", "id": "w", "scale": 6, **kw}]
        store, _ = run(steps, **H)
        return store.get("m").data, store.get("w").data

    def test_curl_moves_the_shape_but_keeps_its_area(self):
        m, w = self._w(curl=True, amount=3, iterations=4)
        assert np.abs(m - w).sum() > 200                       # it moved
        assert abs(w.sum() - m.sum()) / m.sum() < 0.06         # divergence-free: no bunching or thinning

    def test_nested_iterations_fold_the_edge(self):
        m, one = self._w(amount=2, iterations=1)
        _, three = self._w(amount=2, iterations=3)
        assert _edge(three) - _edge(m) > 1.5 * (_edge(one) - _edge(m))   # extra edge: more folding

    def test_one_iteration_is_the_plain_warp(self):
        _, a = self._w(amount=2)
        _, b = self._w(amount=2, iterations=1)
        assert np.array_equal(a, b)

    def test_curl_deterministic_and_bounded(self):
        assert np.array_equal(self._w(curl=True)[1], self._w(curl=True)[1])
        with pytest.raises(RecipeError):
            self._w(iterations=9)


# ---------------------------------------------------------------- 3 footprints
def fp_steps(extra):
    return [WHITE,
            {"op": "prop", "kind": "crate", "at": [8, 8], "size": 4, "shadow": 0, "id": "c1"},
            {"op": "prop", "kind": "barrel", "at": [30, 20], "size": 4, "shadow": 0, "id": "b1"}] + extra


class TestFootprints:
    def test_all_props(self):
        store, _ = run(fp_steps([{"op": "footprints", "out": "f"}]), **H)
        f = store.get("f").data
        assert f[64, 64] > 0.9 and f[160, 240] > 0.9 and f[10, 300] == 0

    def test_filter_by_step_id(self):
        store, _ = run(fp_steps([{"op": "footprints", "out": "f", "of": ["b1"]}]), **H)
        f = store.get("f").data
        assert f[64, 64] == 0 and f[160, 240] > 0.9

    def test_filter_by_kind(self):
        store, _ = run(fp_steps([{"op": "footprints", "out": "f", "kinds": ["crate"]}]), **H)
        f = store.get("f").data
        assert f[64, 64] > 0.9 and f[160, 240] == 0

    def test_grow(self):
        store, _ = run(fp_steps([{"op": "footprints", "out": "f", "kinds": ["crate"], "grow": 2}]), **H)
        assert store.get("f").data[64, 64 + 8 * 3] > 0.9       # 3 ft from the centre: inside 2 + 2 ft

    def test_unknown_or_later_id_is_an_error(self):
        with pytest.raises(RecipeError, match="no earlier step has id nope"):
            run(fp_steps([{"op": "footprints", "out": "f", "of": ["nope"]}]), **H)

    def test_empty_when_nothing_drawn(self):
        store, _ = run([WHITE, {"op": "footprints", "out": "f"}], **H)
        assert store.get("f").data.max() == 0

    def test_legend_icons_are_not_footprints(self):
        store, e = run(fp_steps([{"op": "legend", "at": "sw"}, {"op": "footprints", "out": "f"}]), **H)
        assert len(e.collector.footprints) == 2

    def test_scatter_can_avoid_earlier_props(self):
        steps = fp_steps([{"op": "footprints", "out": "f", "grow": 1},
                          {"op": "scatter", "kind": "pebbles", "region": [[0, 0], [40, 0], [40, 30], [0, 30]],
                           "density": 3, "spacing": 1.5, "avoid": ["f"], "id": "peb"}])
        _, e = run(steps, **H)
        from shapely.geometry import Point
        crate = e.collector.footprints[0]
        pts = e.collector.scatter_points.get("peb") or []
        assert pts and not any(crate.contains(Point(p)) for p in pts)


# ---------------------------------------------------------------- 4 atmosphere
ATM = [WHITE,
       {"op": "noise", "out": "n", "id": "n", "atmosphere": True},
       {"op": "field_to_mask", "out": "m", "src": "n", "lo": -1, "hi": 1},
       {"op": "fill", "mask": "m", "color": "#000000", "opacity": 0.8, "atmosphere": True},
       {"op": "stipple", "mask": "m", "density": 0.5, "falloff": None, "opacity": 1}]   # index-seeded, after


class TestAtmosphere:
    def test_skip_drops_paint_but_keeps_layers(self):
        store, _ = render(recipe(ATM), skip_atmosphere=True)
        assert "n" in store and store.get("canvas").data[..., :3].mean() > 0.9

    def test_full_render_keeps_it(self):
        store, _ = render(recipe(ATM))
        assert store.get("canvas").data[..., :3].mean() < 0.9

    def test_skip_does_not_reseed_later_steps(self):
        under, _ = render(recipe(ATM), skip_atmosphere=True)
        clear = [dict(s) for s in ATM]
        clear[3]["opacity"] = 0.0
        ref, _ = render(recipe(clear))
        assert np.allclose(under.get("canvas").data, ref.get("canvas").data)

    def test_macro_call_marks_its_body(self):
        style = {"macros": {"fog": {"params": {}, "steps": [{"op": "fill", "color": "#000"}, {"op": "fill", "color": "#111"}]}}}
        r = recipe([WHITE, {"op": "fog", "atmosphere": True}], style=style)
        assert [s.atmosphere for s in r.steps] == [False, True, True]

    def test_atmosphere_is_not_passed_to_the_op(self):
        r = recipe([WHITE, {"op": "fill", "color": "#000", "atmosphere": True}])
        assert "atmosphere" not in r.steps[1].params()

    def test_quality_measures_under_atmosphere(self, tmp_path, capsys):
        from mapgen.quality import cli_quality, render_under_atmosphere
        rp = tmp_path / "a.map.yaml"
        rp.write_text(yaml.safe_dump({"map": header(**H), "steps": ATM}))
        img = render_under_atmosphere(rp)
        assert img is not None and np.asarray(img)[..., :3].mean() > 220
        full = tmp_path / "a.png"
        from mapgen.export import render_recipe
        render_recipe(rp, tmp_path, only_png=True)
        args = SimpleNamespace(baseline=False, png=str(full), px_per_square=None, recipe=str(rp),
                               category=None, as_drawn=False)
        assert cli_quality(args) == 0
        assert "under atmosphere" in capsys.readouterr().out

    def test_no_atmosphere_steps_returns_none(self, tmp_path):
        from mapgen.quality import render_under_atmosphere
        rp = tmp_path / "b.map.yaml"
        rp.write_text(yaml.safe_dump({"map": header(**H), "steps": [WHITE]}))
        assert render_under_atmosphere(rp) is None
