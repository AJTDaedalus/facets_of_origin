"""Fixes from the PR #35 review (docs/REVIEW_pr35.md): engine edge cases and the ops that had one test."""
import json
from pathlib import Path

import numpy as np
import pytest
from shapely.geometry import Point, box

from mapgen.export import render_recipe
from mapgen.ops.masks import rasterize_geom
from mapgen.recipe import RecipeError, load_recipe, parse_recipe
from mapgen.units import Frame
from tests.mapgen.conftest import header
from tests.mapgen.helpers import layer, run

H = dict(width_ft=40, height_ft=30, px_per_square=20, supersample=1)
ROOM = [{"op": "canvas", "out": "canvas", "color": "#ffffff"},
        {"op": "rect", "out": "room", "x": 5, "y": 5, "w": 30, "h": 20},
        {"op": "wall", "src": "room", "name": "w", "thickness": 1}]


def canvas(steps, **h):
    store, e = run(steps, **dict(H, **h))
    return store.get("canvas").data, e.collector


# ---------- R4 ----------
class TestIslandInHole:
    @pytest.mark.parametrize("order", ["island_first", "ring_first"])
    def test_island_survives_any_part_order(self, order):
        from shapely.geometry import MultiPolygon
        ring = box(0, 0, 50, 50).difference(box(10, 10, 40, 40))
        island = box(20, 20, 30, 30)
        parts = [island, ring] if order == "island_first" else [ring, island]
        fr = Frame(parse_recipe({"map": header(width_ft=50, height_ft=50, px_per_square=10), "steps": []}).map)
        m = rasterize_geom(fr, MultiPolygon(parts))
        assert m[50, 50] == pytest.approx(1.0) and m[30, 30] == pytest.approx(0.0) and m[5, 5] == pytest.approx(1.0)


# ---------- R5 ----------
class TestSecretDoor:
    def test_no_mark_by_default(self):
        plain, _ = canvas(ROOM)
        secret, _ = canvas(ROOM + [{"op": "secret_door", "wall": "w", "at": [5, 15]}])
        assert np.array_equal(plain, secret)

    def test_mark_on_request(self):
        plain, _ = canvas(ROOM)
        marked, _ = canvas(ROOM + [{"op": "secret_door", "wall": "w", "at": [5, 15], "mark": True}])
        assert not np.array_equal(plain, marked)

    def test_not_exported_as_a_uvtt_door(self, write_recipe, tmp_out):
        rec = {"map": header(**H), "steps": ROOM + [{"op": "secret_door", "wall": "w", "at": [5, 15]},
                                                    {"op": "door", "wall": "w", "at": [20, 5]}]}
        r = render_recipe(write_recipe(rec), out_dir=tmp_out)
        d = json.loads(Path(r["dd2vtt"]).read_text())
        m = json.loads(Path(r["meta"]).read_text())
        assert len(d["portals"]) == 1 and any(p["secret"] for p in m["portals"])


# ---------- R8 ----------
class TestEdgeErrors:
    def test_material_wall_off_map_is_harmless(self):
        st = {"materials": {"stone": {"type": "flat", "color": "#808080"}}}
        store, col = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                          {"op": "rect", "out": "far", "x": 500, "y": 500, "w": 10, "h": 10},
                          {"op": "wall", "src": "far", "material": "stone"},
                          {"op": "path", "out": "l", "points": [[500, 500], [520, 500]], "line": True},
                          {"op": "partition", "src": "l", "material": "stone"}], style=st, **H)
        assert np.allclose(store.get("canvas").data[..., :3], 1)

    def test_path_label_on_empty_geometry(self):
        with pytest.raises(RecipeError, match="empty"):
            run([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                 {"op": "rect", "out": "a", "x": 0, "y": 0, "w": 1, "h": 1},
                 {"op": "rect", "out": "b", "x": 5, "y": 5, "w": 1, "h": 1},
                 {"op": "intersect", "out": "none", "of": ["a", "b"]},
                 {"op": "path_label", "text": "x", "src": "none"}], **H)

    def test_map_too_small_to_render(self):
        with pytest.raises(RecipeError, match="px"):
            Frame(parse_recipe({"map": header(width_ft=0.2, height_ft=10, px_per_square=10), "steps": []}).map)

    def test_include_must_be_a_mapping(self, write_recipe, tmp_path):
        (tmp_path / "bad.yaml").write_text("- just\n- a list\n")
        with pytest.raises(RecipeError, match="mapping"):
            load_recipe(write_recipe({"map": header(include=["bad.yaml"]), "steps": []}))

    def test_cli_reports_internal_errors_without_traceback(self, write_recipe, tmp_out, capsys, monkeypatch):
        from mapgen import __main__ as cli
        import mapgen.export as ex
        monkeypatch.setattr(ex, "render_recipe", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
        assert cli.main(["render", str(write_recipe({"map": header(), "steps": []})), "--out", str(tmp_out)]) == 3
        assert "internal error" in capsys.readouterr().err


# ---------- R9 ----------
class TestDoorJambs:
    def test_perpendicular_wall_keeps_its_end_at_the_jamb(self):
        _, col = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                         {"op": "path", "out": "a", "points": [[10, 10], [10, 20]], "line": True},
                         {"op": "partition", "src": "a", "name": "A"},
                         {"op": "path", "out": "b", "points": [[10, 10], [30, 10]], "line": True},
                         {"op": "partition", "src": "b", "name": "B"},
                         {"op": "double_door", "wall": "A", "at": [10, 15], "width": 10}])
        b_lines = [l for l in col.los if abs(l.coords[0][1] - 10) < 1e-6 and abs(l.coords[-1][1] - 10) < 1e-6]
        assert any(min(l.coords[0][0], l.coords[-1][0]) == pytest.approx(10, abs=1e-6) for l in b_lines)

    def test_cut_matches_the_portal(self):
        _, col = canvas(ROOM + [{"op": "door", "wall": "w", "at": [20, 5], "width": 4}])
        (a, b) = col.portals[0]["bounds"]
        ends = [Point(c) for l in col.los for c in (l.coords[0], l.coords[-1])]
        assert min(e.distance(Point(a)) for e in ends) < 0.01 and min(e.distance(Point(b)) for e in ends) < 0.01


# ---------- R13 ----------
class TestMacroSeedOffset:
    STYLE = "macros:\n  speck:\n    params: {}\n    steps:\n      - {op: noise, out: n, scale: 5}\n"

    def test_seed_offset_reaches_the_macro_body(self, write_recipe, tmp_path):
        (tmp_path / "s.yaml").write_text(self.STYLE)
        a = load_recipe(write_recipe({"map": header(include=["s.yaml"]), "steps": [{"op": "speck"}]}, name="a.map.yaml"))
        b = load_recipe(write_recipe({"map": header(include=["s.yaml"]),
                                      "steps": [{"op": "speck", "seed_offset": 3}]}, name="b.map.yaml"))
        assert a.steps[0].seed_offset == 0 and b.steps[0].seed_offset == 3


class TestFogAreasMeta:
    def test_declared_areas_reach_meta(self, write_recipe, tmp_out):
        rec = {"map": header(**H), "fog_areas": ["room"], "steps": ROOM}
        m = json.loads(Path(render_recipe(write_recipe(rec), out_dir=tmp_out)["meta"]).read_text())
        assert m["fog_areas"] == ["room"]

    def test_unknown_area_is_an_error(self, write_recipe, tmp_out):
        rec = {"map": header(**H), "fog_areas": ["attic"], "steps": ROOM}
        with pytest.raises(RecipeError, match="attic"):
            render_recipe(write_recipe(rec), out_dir=tmp_out)


# ---------- R12: the ops that had a single test ----------
SQ = [{"op": "canvas", "out": "canvas", "color": "#ffffff"},
      {"op": "rect", "out": "r", "x": 10, "y": 8, "w": 20, "h": 14},
      {"op": "rasterize", "out": "m", "src": "r"}]


class TestThinlyTestedOps:
    def test_ellipse_rotation_keeps_area(self):
        g = layer([{"op": "ellipse", "out": "e", "center": [20, 15], "rx": 8, "ry": 3, "rotate": 40}], "e", **H).geom
        assert g.area == pytest.approx(np.pi * 24, rel=0.01)

    def test_ellipse_needs_positive_radii(self):
        with pytest.raises(RecipeError):
            run([{"op": "ellipse", "out": "e", "center": [1, 1], "rx": 0, "ry": 1}], **H)

    def test_grow_zero_is_identity_ish(self):
        store, _ = run(SQ + [{"op": "grow", "out": "g", "src": "m", "by": 0}], **H)
        assert abs(store.get("g").data.sum() - store.get("m").data.sum()) / store.get("m").data.sum() < 0.03

    def test_grow_needs_a_mask(self):
        with pytest.raises(RecipeError, match="Mask"):
            run([{"op": "rect", "out": "r", "x": 0, "y": 0, "w": 1, "h": 1}, {"op": "grow", "out": "g", "src": "r", "by": 1}], **H)

    def test_invert_twice_is_identity(self):
        store, _ = run(SQ + [{"op": "invert", "out": "i", "src": "m"}, {"op": "invert", "out": "j", "src": "i"}], **H)
        assert np.allclose(store.get("j").data, store.get("m").data)

    def test_threshold_softness_ramps(self):
        store, _ = run(SQ + [{"op": "blur", "out": "b", "src": "m", "sigma": 2},
                             {"op": "threshold", "out": "t", "src": "b", "level": 0.5, "softness": 0.2}], **H)
        t = store.get("t").data
        assert ((t > 0.05) & (t < 0.95)).any()

    def test_threshold_level_bounds(self):
        with pytest.raises(RecipeError, match="level"):
            run(SQ + [{"op": "threshold", "out": "t", "src": "m", "level": 2}], **H)

    def test_roughen_zero_amount_keeps_area(self):
        store, _ = run(SQ + [{"op": "roughen", "out": "r2", "src": "m", "amount": 0}], **H)
        assert abs(store.get("r2").data.sum() - store.get("m").data.sum()) / store.get("m").data.sum() < 0.03

    def test_occlusion_strength_zero_noop(self):
        a, _ = canvas(SQ)
        b, _ = canvas(SQ + [{"op": "occlusion", "mask": "m", "strength": 0}])
        assert np.allclose(a, b)

    def test_occlusion_bad_falloff(self):
        with pytest.raises(RecipeError, match="falloff"):
            run(SQ + [{"op": "occlusion", "mask": "m", "falloff": 0}], **H)

    def test_paper_strength_zero_noop(self):
        a, _ = canvas(SQ)
        b, _ = canvas(SQ + [{"op": "paper", "strength": 0}])
        assert np.allclose(a, b, atol=1e-6)

    def test_vignette_strength_zero_noop(self):
        a, _ = canvas(SQ)
        b, _ = canvas(SQ + [{"op": "vignette", "strength": 0}])
        assert np.allclose(a, b)

    def test_vignette_bad_strength(self):
        with pytest.raises(RecipeError, match="strength"):
            run(SQ + [{"op": "vignette", "strength": 2}], **H)

    def test_double_door_default_width_8(self):
        _, col = canvas(ROOM + [{"op": "double_door", "wall": "w", "at": [20, 5]}])
        (a, b) = col.portals[0]["bounds"]
        assert np.hypot(a[0] - b[0], a[1] - b[1]) == pytest.approx(8)

    def test_double_door_unknown_wall(self):
        with pytest.raises(RecipeError, match="wall"):
            canvas(ROOM + [{"op": "double_door", "wall": "nope", "at": [20, 5]}])

    def test_opening_keeps_portals_empty_and_needs_wall(self):
        _, col = canvas(ROOM + [{"op": "opening", "wall": "w", "at": [20, 5]}])
        assert col.portals == []
        with pytest.raises(RecipeError):
            canvas(ROOM + [{"op": "opening", "wall": "x", "at": [20, 5]}])

    def test_portcullis_is_a_closed_portal(self):
        _, col = canvas(ROOM + [{"op": "portcullis", "wall": "w", "at": [20, 25]}])
        assert col.portals[0]["kind"] == "portcullis" and col.portals[0]["closed"] is True

    def test_window_default_width_and_bad_wall(self):
        a, _ = canvas(ROOM)
        b, _ = canvas(ROOM + [{"op": "window", "wall": "w", "at": [20, 25]}])
        assert not np.array_equal(a, b)
        with pytest.raises(RecipeError):
            canvas(ROOM + [{"op": "window", "wall": "x", "at": [20, 25]}])

    @pytest.mark.parametrize("down", ["n", "e", "s", "w"])
    def test_stairs_all_directions(self, down):
        c, col = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                         {"op": "stairs", "x": 10, "y": 10, "w": 8, "h": 8, "down": down}])
        assert (c[40:72, 40:72, 0] < 0.9).any() and "stairs" in col.legend

    def test_stairs_bad_direction(self):
        with pytest.raises(RecipeError):
            canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                    {"op": "stairs", "x": 1, "y": 1, "w": 2, "h": 2, "down": "up"}])

    def test_label_circle_and_bold(self):
        a, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                       {"op": "label", "text": "7", "at": [20, 15], "size": 3, "circle": True, "bold": True}])
        assert (a[45:75, 65:95, 0] < 0.5).any()

    def test_label_needs_text_position(self):
        with pytest.raises(RecipeError):
            canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "label", "text": "x"}])

    def test_title_top_vs_bottom(self):
        top, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "title", "text": "T", "position": "top"}])
        bot, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "title", "text": "T", "position": "bottom"}])
        assert (top[:40, :, 0] < 0.5).any() and not (bot[:40, :, 0] < 0.5).any()

    def test_title_bad_position(self):
        with pytest.raises(RecipeError):
            canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "title", "text": "T", "position": "left"}])

    def test_scale_bar_custom_text_and_corner(self):
        c, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "scale_bar", "at": "se", "text": "50 ft"}])
        assert (c[90:, 100:, 0] < 0.5).any() and not (c[:30, :60, 0] < 0.5).any()

    def test_frame_margin_moves_line(self):
        a, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "frame", "margin": 0}])
        b, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "frame", "margin": 3}])
        assert a[0, 80, 0] < 0.5 and b[0, 80, 0] > 0.9

    def test_legend_empty_draws_nothing(self):
        a, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}])
        b, col = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, {"op": "legend"}])
        assert np.array_equal(a, b) and col.legend_drawn == []

    def test_legend_exclude(self):
        _, col = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                         {"op": "prop", "kind": "crate", "at": [10, 10]},
                         {"op": "prop", "kind": "barrel", "at": [14, 10]},
                         {"op": "legend", "exclude": ["crate"]}])
        assert col.legend_drawn == ["barrel"]

    def test_path_label_offset_moves_text(self):
        a, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                       {"op": "path_label", "text": "River", "points": [[5, 15], [35, 15]], "size": 3, "halo": None}])
        b, _ = canvas([{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                       {"op": "path_label", "text": "River", "points": [[5, 15], [35, 15]], "size": 3, "halo": None,
                        "offset": 5}])
        ya = np.nonzero((a[..., 0] < 0.5).any(axis=1))[0].mean()
        yb = np.nonzero((b[..., 0] < 0.5).any(axis=1))[0].mean()
        assert abs(ya - yb) > 10
