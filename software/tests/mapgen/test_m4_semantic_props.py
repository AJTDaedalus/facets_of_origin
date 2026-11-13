"""T19-T23: walls, openings, stairs, lights, props, scatter, overlay."""
import numpy as np
import pytest
from shapely.geometry import Point

from mapgen.ops.props import PROPS
from mapgen.recipe import RecipeError
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=20, supersample=1)    # 4 px/ft, 160x120
ROOM = [{"op": "canvas", "out": "canvas", "color": "#ffffff"},
        {"op": "rect", "out": "room", "x": 5, "y": 5, "w": 30, "h": 20}]


def go(extra, **h):
    store, e = run(ROOM + extra, **dict(H, **h))
    return store, e.collector


def total_len(lines):
    return sum(l.length for l in lines)


# ---------- T19 ----------
class TestWall:
    def test_los_covers_boundary(self):
        _, col = go([{"op": "wall", "src": "room", "name": "w"}])
        assert total_len(col.los) == pytest.approx(100, rel=0.01)

    def test_wall_paints_band_outside_floor(self):
        store, _ = go([{"op": "wall", "src": "room", "thickness": 1.5, "fill": "#808080"}])
        c = store.get("canvas").data
        assert c[60, 80, 0] == pytest.approx(1)          # floor untouched
        assert c[60, 17, 0] < 0.6                        # 0.75 ft outside the west wall

    def test_pillar_hole_emits_closed_loop(self):
        steps = [{"op": "circle", "out": "pil", "center": [20, 15], "r": 2},
                 {"op": "subtract", "out": "floor", "a": "room", "b": ["pil"]},
                 {"op": "wall", "src": "floor", "name": "w"}]
        _, col = go(steps)
        assert any(l.is_ring and l.length == pytest.approx(2 * np.pi * 2, rel=0.02) for l in col.los)

    def test_ruined_wall_has_gaps(self):
        _, col = go([{"op": "wall", "src": "room", "style": "ruined", "gaps": 0.4, "id": "rw"}])
        assert 30 < total_len(col.los) < 95

    def test_wall_registered_for_openings(self):
        _, col = go([{"op": "wall", "src": "room", "name": "north"}])
        assert "north" in col.walls

    def test_no_los_when_disabled(self):
        _, col = go([{"op": "wall", "src": "room", "emit_los": False}])
        assert col.los == []

    def test_exclude_leaves_wall_open(self):
        _, col = go([{"op": "rect", "out": "gap", "x": 15, "y": 20, "w": 10, "h": 10},
                     {"op": "wall", "src": "room", "exclude": "gap"}])
        assert total_len(col.los) == pytest.approx(90, rel=0.01)

    def test_wall_needs_polygon(self):
        with pytest.raises(RecipeError, match="polygon"):
            go([{"op": "path", "out": "l", "points": [[0, 0], [5, 5]], "line": True},
                {"op": "wall", "src": "l"}])


# ---------- T20 ----------
WALL = [{"op": "wall", "src": "room", "name": "w", "thickness": 1}]


class TestOpenings:
    def test_door_on_right_square(self):
        _, col = go(WALL + [{"op": "door", "wall": "w", "at": [20, 5.3]}])
        p = col.portals[0]
        assert p["kind"] == "door" and p["closed"] is True
        assert p["position"][0] == pytest.approx(20) and p["position"][1] == pytest.approx(5)

    def test_door_gap_equals_width(self):
        _, col = go(WALL + [{"op": "door", "wall": "w", "at": [20, 5], "width": 5}])
        assert total_len(col.los) == pytest.approx(95, rel=0.01)

    def test_door_snaps_to_nearest_edge(self):
        _, col = go(WALL + [{"op": "door", "wall": "w", "at": [34, 15]}])
        assert col.portals[0]["position"][0] == pytest.approx(35)
        assert col.portals[0]["rotation"] == pytest.approx(np.pi / 2, abs=1e-6) or \
            col.portals[0]["rotation"] == pytest.approx(-np.pi / 2, abs=1e-6)

    def test_secret_door(self):
        store, col = go(WALL + [{"op": "secret_door", "wall": "w", "at": [5, 15], "width": 5}])
        assert col.portals[0]["secret"] is True and col.portals[0]["closed"] is True
        # the wall keeps blocking sight in the VTT data (UVTT has no secret flag)
        assert total_len(col.los) == pytest.approx(100, rel=0.01)

    def test_window_keeps_los_and_draws(self):
        store, col = go(WALL + [{"op": "window", "wall": "w", "at": [20, 25]}])
        assert total_len(col.los) == pytest.approx(100, rel=0.01) and col.portals == []

    def test_double_door_and_portcullis(self):
        _, col = go(WALL + [{"op": "double_door", "wall": "w", "at": [20, 5], "width": 10},
                            {"op": "portcullis", "wall": "w", "at": [20, 25]}])
        kinds = sorted(p["kind"] for p in col.portals)
        assert kinds == ["double_door", "portcullis"]
        assert total_len(col.los) == pytest.approx(85, rel=0.01)

    def test_opening_fills_with_floor(self):
        store, col = go([{"op": "rasterize", "out": "fm", "src": "room"},
                         {"op": "fill", "mask": "fm", "color": "#00ff00"}] + WALL +
                        [{"op": "opening", "wall": "w", "at": [20, 5], "floor_color": "#00ff00"}])
        c = store.get("canvas").data
        assert c[18, 80, 1] > 0.9 and c[18, 80, 0] < 0.2       # 0.5 ft into the wall band
        assert col.portals == []

    def test_partition_door(self):
        store, col = go([{"op": "path", "out": "split", "points": [[20, 5], [20, 25]], "line": True},
                         {"op": "partition", "src": "split", "name": "mid"},
                         {"op": "door", "wall": "mid", "at": [20.4, 15], "width": 4}])
        assert total_len(col.los) == pytest.approx(16, rel=0.01)
        assert col.portals[0]["position"] == [pytest.approx(20), pytest.approx(15)]
        c = store.get("canvas").data
        assert c[60, 80, 0] < 0.98          # door leaf drawn across the partition

    def test_partition_needs_line(self):
        with pytest.raises(RecipeError):
            go([{"op": "partition", "src": "nope"}])

    def test_unknown_wall(self):
        with pytest.raises(RecipeError, match="wall 'nope'"):
            go(WALL + [{"op": "door", "wall": "nope", "at": [20, 5]}])

    def test_stairs_draw_and_light_emits(self):
        store, col = go([{"op": "stairs", "x": 10, "y": 10, "w": 5, "h": 10, "down": "s"},
                         {"op": "light", "at": [20, 15], "radius": 20, "glow": True}])
        c = store.get("canvas").data
        assert (c[40:80, 40:60, 0] < 0.5).sum() > 20
        assert col.lights[0]["range"] == pytest.approx(20)


# ---------- T21 ----------
class TestProps:
    @pytest.mark.parametrize("kind", sorted(PROPS))
    def test_every_prop_renders_inside_bounds(self, kind):
        store, _ = go([{"op": "prop", "kind": kind, "at": [20, 15], "size": 4, "id": "p"}])
        c = store.get("canvas").data
        changed = np.any(np.abs(c[..., :3] - 1) > 0.02, axis=-1)
        ys, xs = np.nonzero(changed)
        assert changed.sum() > 10
        # within 4 ft square + shadow/ink margin of 1.5 ft around (20, 15)
        assert xs.min() >= (20 - 3.5) * 4 and xs.max() <= (20 + 3.5) * 4
        assert ys.min() >= (15 - 3.5) * 4 and ys.max() <= (15 + 3.5) * 4

    @pytest.mark.parametrize("kind", ["table", "tree", "barrel"])
    def test_prop_deterministic(self, kind):
        a = go([{"op": "prop", "kind": kind, "at": [20, 15], "id": "p"}])[0].get("canvas").data
        b = go([{"op": "prop", "kind": kind, "at": [20, 15], "id": "p"}])[0].get("canvas").data
        assert np.array_equal(a, b)

    def test_rotation_changes_orientation(self):
        a = go([{"op": "prop", "kind": "bed", "at": [20, 15], "size": 6}])[0].get("canvas").data
        b = go([{"op": "prop", "kind": "bed", "at": [20, 15], "size": 6, "rotate": 90}])[0].get("canvas").data
        assert not np.array_equal(a, b)

    def test_unknown_prop(self):
        with pytest.raises(RecipeError, match="kind"):
            go([{"op": "prop", "kind": "spaceship", "at": [1, 1]}])

    def test_prop_registers_legend(self):
        _, col = go([{"op": "prop", "kind": "crate", "at": [20, 15]}])
        assert "crate" in col.legend

    def test_prop_footprint_recorded(self):
        _, col = go([{"op": "prop", "kind": "table", "at": [20, 15], "size": 4}])
        assert any(g.contains(Point(20, 15)) for g in col.footprints)


# ---------- T22 ----------
class TestScatter:
    def _pts(self, **kw):
        _, col = go([{"op": "rasterize", "out": "fm", "src": "room"},
                     {"op": "scatter", "kind": "rubble", "mask": "fm", "id": "s", **kw}])
        return col.scatter_points["s"]

    def test_spacing(self):
        pts = np.array(self._pts(density=0.5, spacing=2))
        d = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1)) + np.eye(len(pts)) * 99
        assert d.min() >= 2 - 1e-6

    def test_inside_mask(self):
        pts = self._pts(density=0.5, spacing=2)
        assert all(5 <= x <= 35 and 5 <= y <= 25 for x, y in pts)

    def test_density(self):
        pts = self._pts(density=0.3, spacing=1)
        expected = 0.3 * (30 * 20) / 25
        assert expected * 0.8 <= len(pts) <= expected * 1.2

    def test_deterministic(self):
        assert self._pts(density=0.3, spacing=1) == self._pts(density=0.3, spacing=1)

    def test_avoid(self):
        _, col = go([{"op": "rasterize", "out": "fm", "src": "room"},
                     {"op": "circle", "out": "c", "center": [20, 15], "r": 6},
                     {"op": "rasterize", "out": "cm", "src": "c"},
                     {"op": "scatter", "kind": "rubble", "mask": "fm", "avoid": ["cm"], "density": 0.5,
                      "spacing": 1.5, "id": "s"}])
        assert all(np.hypot(x - 20, y - 15) > 5.5 for x, y in col.scatter_points["s"])

    def test_region_polygon(self):
        _, col = go([{"op": "scatter", "kind": "rubble", "region": [[5, 5], [15, 5], [15, 15], [5, 15]],
                      "density": 0.5, "spacing": 1.5, "id": "s"}])
        assert all(5 <= x <= 15 and 5 <= y <= 15 for x, y in col.scatter_points["s"])


# ---------- T23 ----------
class TestOverlay:
    def test_grid_lines_on_square_multiples(self):
        store, col = go([{"op": "grid", "color": "#000000", "alpha": 1.0, "weight": 0.1}])
        c = store.get("canvas").data[..., 0]
        cols = np.nonzero((c < 0.5).mean(axis=0) > 0.9)[0]
        assert set(cols) <= {x for k in range(0, 9) for x in range(k * 20 - 1, k * 20 + 2)}
        assert "grid" in col.masks

    def test_grid_clip(self):
        store, _ = go([{"op": "rasterize", "out": "fm", "src": "room"},
                       {"op": "grid", "mask": "fm", "color": "#000000", "alpha": 1.0}])
        c = store.get("canvas").data[..., 0]
        assert c[:15, :].min() > 0.95 and c[25:95, 25:135].min() < 0.5

    def test_label_and_title(self):
        store, _ = go([{"op": "label", "text": "1", "at": [20, 15], "size": 3},
                       {"op": "title", "text": "Test Room", "position": "bottom"}])
        c = store.get("canvas").data[..., 0]
        assert (c[48:72, 70:90] < 0.5).any()

    def test_compass_scale_frame(self):
        store, _ = go([{"op": "compass", "at": "ne", "size": 5},
                       {"op": "scale_bar", "at": "nw"},
                       {"op": "frame", "margin": 1}])
        c = store.get("canvas").data[..., 0]
        assert (c[:30, 120:] < 0.5).any() and (c[:20, :60] < 0.5).any() and c[4:7, 80].min() < 0.5

    def test_legend_lists_present_kinds(self):
        store, col = go([{"op": "prop", "kind": "crate", "at": [10, 10]},
                         {"op": "prop", "kind": "barrel", "at": [12, 10]},
                         {"op": "legend", "at": "sw"}])
        assert col.legend_drawn == ["barrel", "crate"]

    def test_bad_corner(self):
        with pytest.raises(RecipeError):
            go([{"op": "compass", "at": "middle-ish"}])
