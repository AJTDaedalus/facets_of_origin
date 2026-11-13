"""T11-T18: noise and fields, canvas/fill/blend, materials, stroke, shadow, hatch, paper."""
import numpy as np
import pytest

from mapgen.color import resolve_color, blend
from mapgen.noise import fbm, noise_grid
from mapgen.recipe import RecipeError
from tests.mapgen.helpers import layer, run

M = dict(width_ft=20, height_ft=20, px_per_square=20, supersample=1)   # 80x80 px, 4 px/ft
STYLE = {"palette": {"ink": "#202020", "paper": "#e0d8c0", "stone": "ink"},
         "ink": {"heavy": 0.5, "medium": 0.3, "fine": 0.12},
         "materials": {
             "plain": {"type": "flat", "color": "#808080"},
             "rock": {"type": "ramp_noise", "colors": ["#505050", "#a0a0a0"], "scale": 4},
             "dirt": {"type": "dirt", "colors": ["#6b5a40", "#8a7656"], "scale": 4},
             "hatch": {"type": "bedrock_hatch", "color": "#c8c0b0", "ink": "ink", "spacing": 2.5},
             "flags": {"type": "flagstone", "colors": ["#9a958a", "#bdb7aa"], "size": 2.5,
                       "mortar": 0.15, "mortar_color": "#4a463e"},
             "ashlar": {"type": "flagstone", "pattern": "ashlar", "colors": ["#9a958a", "#bdb7aa"], "size": 2.5},
             "boards": {"type": "planks", "colors": ["#7a5534", "#9b7048"], "width": 1.0, "length": 6, "angle": 0},
             "cobbles": {"type": "cobble", "colors": ["#7d7a72", "#a29e94"], "size": 1.0},
             "lawn": {"type": "grass", "colors": ["#56703a", "#7d9450"], "scale": 3},
             "veined": {"type": "ramp_noise", "colors": ["#505050", "#606060"], "scale": 4, "veins": 0.9,
                        "vein_color": "#f0f0f0", "vein_dark": "#101010", "vein_scale": 4},
             "pond": {"type": "water", "shallow": "#9cc3cf", "deep": "#3d6f85", "depth": 4},
         }}


def full(extra, **h):
    kw = dict(M, **h)
    return run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + extra, style=STYLE, **kw)


def canvas(extra, **h):
    store, _ = full(extra, **h)
    return store.get("canvas").data


SQ = [{"op": "rect", "out": "r", "x": 5, "y": 5, "w": 10, "h": 10},
      {"op": "rasterize", "out": "m", "src": "r"}]


# ---------- T11 ----------
class TestNoise:
    def test_deterministic(self):
        assert np.array_equal(fbm((64, 64), 16, 5), fbm((64, 64), 16, 5))

    def test_seed_changes(self):
        assert not np.array_equal(fbm((64, 64), 16, 5), fbm((64, 64), 16, 6))

    def test_range(self):
        a = fbm((128, 128), 20, 3, octaves=5)
        assert a.min() >= -1 and a.max() <= 1 and a.std() > 0.05

    def test_frequency_tracks_scale(self):
        def centroid(scale):
            a = noise_grid((256, 256), scale, 9)
            spec = (np.abs(np.fft.rfft(a - a.mean(), axis=1)) ** 2).mean(axis=0)
            f = np.arange(len(spec))
            return (spec * f).sum() / spec.sum()
        ratio = centroid(8) / centroid(32)
        assert 2.0 < ratio < 8.0

    def test_coarse_path_is_smooth(self):
        a = noise_grid((200, 200), 80, 1)            # uses the coarse lattice
        assert np.abs(np.diff(a, axis=1)).max() < 0.15

    def test_noise_op(self):
        f = layer([{"op": "noise", "out": "n", "scale": 5, "kind": "ridged"}], "n", **M)
        assert f.data.shape == (80, 80) and f.data.min() >= -1

    def test_noise_op_rejects_bad_kind(self):
        with pytest.raises(RecipeError, match="kind"):
            run([{"op": "noise", "out": "n", "scale": 5, "kind": "plaid"}], **M)


# ---------- T12 ----------
class TestFields:
    def test_linear_gradient(self):
        f = layer([{"op": "gradient", "out": "g", "start": [0, 0], "end": [20, 0]}], "g", **M).data
        assert f[0, 0] == pytest.approx(0, abs=0.02) and f[0, -1] == pytest.approx(1, abs=0.02)

    def test_radial_gradient(self):
        f = layer([{"op": "gradient", "out": "g", "kind": "radial", "start": [10, 10], "end": [20, 10]}], "g", **M).data
        assert f[40, 40] < 0.05 and f[40, 79] > 0.95

    def test_gradient_needs_distinct_points(self):
        with pytest.raises(RecipeError):
            run([{"op": "gradient", "out": "g", "start": [1, 1], "end": [1, 1]}], **M)

    def test_distance_in_feet(self):
        f = layer(SQ + [{"op": "distance", "out": "d", "src": "m"}], "d", **M).data
        assert f[40, 79] == pytest.approx(5, abs=0.3) and f[40, 40] == 0

    def test_signed_distance(self):
        f = layer(SQ + [{"op": "distance", "out": "d", "src": "m", "side": "signed"}], "d", **M).data
        assert f[40, 40] == pytest.approx(-5, abs=0.3)

    def test_distance_inside(self):
        f = layer(SQ + [{"op": "distance", "out": "d", "src": "m", "side": "inside"}], "d", **M).data
        assert f[40, 40] == pytest.approx(5, abs=0.3) and f[0, 0] == 0

    def test_remap(self):
        f = layer([{"op": "gradient", "out": "g", "start": [0, 0], "end": [20, 0]},
                   {"op": "remap", "out": "r", "src": "g", "in_range": [0, 1], "out_range": [10, 20]}], "r", **M).data
        assert f.min() == pytest.approx(10, abs=0.3) and f.max() == pytest.approx(20, abs=0.3)

    def test_remap_clamps_and_curves(self):
        f = layer([{"op": "gradient", "out": "g", "start": [0, 0], "end": [20, 0]},
                   {"op": "remap", "out": "r", "src": "g", "in_range": [0.25, 0.75], "curve": "smooth"}], "r", **M).data
        assert f[0, 0] == 0 and f[0, -1] == 1

    def test_field_to_mask(self):
        m = layer([{"op": "gradient", "out": "g", "start": [0, 0], "end": [20, 0]},
                   {"op": "field_to_mask", "out": "m", "src": "g", "lo": 0.5, "hi": 0.5}], "m", **M).data
        assert m[0, 0] == 0 and m[0, -1] == 1

    def test_mix_fields(self):
        f = layer([{"op": "gradient", "out": "a", "start": [0, 0], "end": [20, 0]},
                   {"op": "gradient", "out": "b", "start": [20, 0], "end": [0, 0]},
                   {"op": "mix", "out": "c", "of": ["a", "b"], "weights": [0.5, 0.5]}], "c", **M).data
        assert np.allclose(f, 0.5, atol=0.02)


# ---------- T13 ----------
class TestColorAndFill:
    def test_resolve_color_forms(self):
        st = type("S", (), {"palette": STYLE["palette"]})
        assert np.allclose(resolve_color(st, "#ff0000"), [1, 0, 0, 1])
        assert np.allclose(resolve_color(st, "#f00"), [1, 0, 0, 1])
        assert np.allclose(resolve_color(st, [0, 255, 0]), [0, 1, 0, 1])
        assert np.allclose(resolve_color(st, "#0000ff80")[3], 128 / 255)
        assert np.allclose(resolve_color(st, "stone"), resolve_color(st, "#202020"))

    def test_resolve_unknown_color(self):
        st = type("S", (), {"palette": {}})
        with pytest.raises(RecipeError, match="colour"):
            resolve_color(st, "chartreuse-ish")

    def test_canvas_color(self):
        c = canvas([])
        assert np.allclose(c[..., :3], 1) and np.allclose(c[..., 3], 1)

    def test_fill_half_mask_mixes(self):
        c = canvas([{"op": "rect", "out": "r", "x": 0, "y": 0, "w": 20, "h": 20},
                    {"op": "rasterize", "out": "m", "src": "r"},
                    {"op": "fill", "mask": "m", "color": "#000000", "opacity": 0.5}])
        assert np.allclose(c[..., :3], 0.5, atol=0.01)

    def test_fill_inverted_mask(self):
        c = canvas(SQ + [{"op": "fill", "mask": "~m", "color": "#000000"}])
        assert c[40, 40, 0] == pytest.approx(1) and c[0, 0, 0] == pytest.approx(0)

    @pytest.mark.parametrize("mode,expect", [("normal", 0.2), ("multiply", 0.12),
                                             ("screen", 0.68), ("overlay", 0.36)])
    def test_blend_formulas(self, mode, expect):
        dst = np.array([[[0.6, 0.6, 0.6, 1.0]]], np.float32)
        src = np.array([[[0.2, 0.2, 0.2]]], np.float32)
        out = blend(dst, src, np.ones((1, 1), np.float32), mode)
        assert out[0, 0, 0] == pytest.approx(expect, abs=1e-3)

    def test_fill_needs_color_or_material(self):
        with pytest.raises(RecipeError, match="color or material"):
            full([{"op": "fill"}])

    def test_unknown_material(self):
        with pytest.raises(RecipeError, match="lava"):
            full([{"op": "fill", "material": "lava"}])


# ---------- T14-T16 materials ----------
def _mat(name, **h):
    return canvas([{"op": "fill", "material": name, "id": "f"}], **h)


def local_std(img, k=5):
    from scipy import ndimage
    lum = img[..., :3].mean(-1)
    m = ndimage.uniform_filter(lum, k)
    m2 = ndimage.uniform_filter(lum * lum, k)
    return np.sqrt(np.clip(m2 - m * m, 0, None)).mean()


ALL = ["rock", "dirt", "hatch", "flags", "ashlar", "boards", "cobbles", "lawn", "pond"]


class TestMaterials:
    def test_flat(self):
        c = _mat("plain")
        assert np.allclose(c[..., :3], 128 / 255, atol=0.01)

    @pytest.mark.parametrize("name", ALL)
    def test_deterministic(self, name):
        assert np.array_equal(_mat(name), _mat(name))

    @pytest.mark.parametrize("name", ALL)
    def test_not_flat(self, name):
        floor = 0.005 if name == "pond" else 0.01     # open deep water is calm in the references too
        assert local_std(_mat(name)) > floor

    def test_ramp_colors_in_range(self):
        c = _mat("rock")[..., 0]
        assert c.min() >= 0x50 / 255 - 0.01 and c.max() <= 0xa0 / 255 + 0.01

    def test_flagstone_mortar_fraction(self):
        c = _mat("flags", width_ft=20, height_ft=20, px_per_square=40)
        mortar = (c[..., 0] < 0.40).mean()     # far darker than any stone, even bevelled
        assert 0.03 < mortar < 0.35

    def test_flagstone_stone_count(self):
        from mapgen.ops.materials import cells
        ids, f1, f2 = cells((160, 160), 10.0, 3)   # 10 px stones on 160 px
        n = len(np.unique(ids))
        assert 256 * 0.75 <= n <= 256 * 1.25

    def test_planks_run_along_angle(self):
        c = _mat("boards", width_ft=20, height_ft=20)[..., 0]
        # angle 0: boards run east-west, so variation along rows < across rows
        along = np.abs(np.diff(c, axis=1)).mean()
        across = np.abs(np.diff(c, axis=0)).mean()
        assert along < across

    def test_water_darker_in_middle(self):
        c = canvas([{"op": "circle", "out": "p", "center": [10, 10], "r": 9},
                    {"op": "rasterize", "out": "m", "src": "p"},
                    {"op": "fill", "mask": "m", "material": "pond"}])
        assert c[40, 40, :3].mean() < c[40, 6, :3].mean()

    def test_veins_add_lines(self):
        plain = local_std(_mat("rock"))
        assert local_std(_mat("veined")) > 0.03 and _mat("veined")[..., 0].max() > 0.6

    def test_grass_is_green(self):
        c = _mat("lawn")
        assert c[..., 1].mean() > c[..., 0].mean() and c[..., 1].mean() > c[..., 2].mean()

    def test_bad_material_param(self):
        st = dict(STYLE)
        st = {**STYLE, "materials": {"x": {"type": "flagstone", "colors": ["#000"], "size": -1}}}
        with pytest.raises(RecipeError, match="size"):
            run([{"op": "canvas", "out": "canvas", "material": "x"}], style=st, **M)


# ---------- T17 ----------
def _ink_mask(c):
    return c[..., 0] < 0.5


class TestStroke:
    def test_mask_edge_line_near_edge(self):
        c = canvas(SQ + [{"op": "stroke", "src": "m", "width": 0.5}])
        ys, xs = np.nonzero(_ink_mask(c))
        # edge at 20 px and 60 px; 0.5 ft = 2 px wide
        d = np.minimum.reduce([np.abs(xs - 20), np.abs(xs - 60), np.abs(ys - 20), np.abs(ys - 60)])
        assert len(xs) > 100 and d.max() <= 2

    def test_geometry_and_mask_agree(self):
        a = canvas(SQ + [{"op": "stroke", "src": "m", "width": 0.5}])
        b = canvas(SQ + [{"op": "stroke", "src": "r", "width": 0.5}])
        assert np.abs(_ink_mask(a).sum() - _ink_mask(b).sum()) / _ink_mask(a).sum() < 0.15

    def test_weight_name(self):
        heavy = _ink_mask(canvas(SQ + [{"op": "stroke", "src": "r", "weight": "heavy"}])).sum()
        fine = _ink_mask(canvas(SQ + [{"op": "stroke", "src": "r", "weight": "fine"}])).sum()
        assert heavy > fine * 2

    def test_dash_duty_cycle(self):
        solid = _ink_mask(canvas([{"op": "path", "out": "l", "points": [[0, 10], [20, 10]], "line": True},
                                  {"op": "stroke", "src": "l", "width": 0.5}])).sum()
        dashed = _ink_mask(canvas([{"op": "path", "out": "l", "points": [[0, 10], [20, 10]], "line": True},
                                   {"op": "stroke", "src": "l", "width": 0.5, "dash": [1, 1]}])).sum()
        assert 0.35 < dashed / solid < 0.65

    def test_roughness_zero_straight(self):
        c = canvas([{"op": "path", "out": "l", "points": [[0, 10], [20, 10]], "line": True},
                    {"op": "stroke", "src": "l", "width": 0.5}])
        rows = np.nonzero(_ink_mask(c).any(axis=1))[0]
        assert rows.max() - rows.min() <= 3

    def test_roughness_wobbles(self):
        c = canvas([{"op": "path", "out": "l", "points": [[0, 10], [20, 10]], "line": True},
                    {"op": "stroke", "src": "l", "width": 0.5, "roughness": 1.0}])
        rows = np.nonzero(_ink_mask(c).any(axis=1))[0]
        assert rows.max() - rows.min() > 3

    def test_double_line(self):
        c = canvas([{"op": "path", "out": "l", "points": [[0, 10], [20, 10]], "line": True},
                    {"op": "stroke", "src": "l", "width": 0.25, "double": 1.0}])
        col = _ink_mask(c)[:, 40]
        runs = np.count_nonzero(np.diff(col.astype(int)) == 1)
        assert runs == 2

    def test_dash_needs_geometry(self):
        with pytest.raises(RecipeError, match="dash"):
            full(SQ + [{"op": "stroke", "src": "m", "width": 0.5, "dash": [1, 1]}])


# ---------- T18 ----------
class TestShadowEtc:
    def test_inner_shadow_darkest_at_edge(self):
        c = canvas(SQ + [{"op": "shadow", "mask": "m", "mode": "inner", "width": 2, "strength": 0.8}])
        row = c[40, 21:40, 0]
        assert row[0] < row[-1] and np.all(np.diff(row) >= -1e-4)
        assert c[0, 0, 0] == pytest.approx(1)

    def test_drop_shadow_outside_offset(self):
        c = canvas(SQ + [{"op": "shadow", "mask": "m", "mode": "drop", "offset": [1, 1], "blur": 0.5}])
        assert c[62, 62, 0] < 0.9 and c[18, 18, 0] > 0.95

    def test_occlusion(self):
        c = canvas(SQ + [{"op": "occlusion", "mask": "m", "falloff": 1.5, "strength": 0.6}])
        assert c[40, 21, 0] < c[40, 40, 0] and c[0, 0, 0] == pytest.approx(1)

    def test_hatch_only_in_band(self):
        c = canvas(SQ + [{"op": "band", "out": "b", "src": "m", "outer": 2},
                         {"op": "hatch", "mask": "b", "spacing": 1.5, "length": 1.5}])
        ink = _ink_mask(c)
        assert ink.sum() > 50 and not ink[25:55, 25:55].any() and not ink[:8, :8].any()

    def test_hatch_deterministic(self):
        a = canvas(SQ + [{"op": "band", "out": "b", "src": "m", "outer": 2},
                         {"op": "hatch", "mask": "b", "id": "h"}])
        b = canvas(SQ + [{"op": "band", "out": "b", "src": "m", "outer": 2},
                         {"op": "hatch", "mask": "b", "id": "h"}])
        assert np.array_equal(a, b)

    def test_paper_adds_texture(self):
        c = canvas([{"op": "paper", "strength": 0.3}])
        assert local_std(c) > 0.003 and c[..., :3].mean() < 1

    def test_vignette_darkens_corners(self):
        c = canvas([{"op": "vignette", "strength": 0.5}])
        assert c[0, 0, 0] < c[40, 40, 0]

    def test_shadow_strength_bounds(self):
        with pytest.raises(RecipeError, match="strength"):
            full(SQ + [{"op": "shadow", "mask": "m", "strength": 3}])
