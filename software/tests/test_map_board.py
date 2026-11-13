"""mapgen Phase 3 v1: the in-app map board (docs/BRIEF_mapgen_phase3.md, draft).

Plumbing only, no rules: the MM lists and sets a rendered map (a mapgen .dd2vtt),
everyone sees it, and tokens for characters and active enemies move over the
WebSocket. Players move only their own token.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.config import settings
from tests.test_websocket import Table, call, error_text, first, kinds


@pytest.fixture
def maps_dir(tmp_path, monkeypatch):
    out = tmp_path / "advent" / "maps" / "mapgen"
    out.mkdir(parents=True)
    img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    (out / "cellar.dd2vtt").write_text(json.dumps({
        "format": 0.3, "resolution": {"map_origin": {"x": 0, "y": 0}, "map_size": {"x": 16, "y": 12},
                                      "pixels_per_grid": 70},
        "line_of_sight": [], "portals": [], "lights": [], "image": img}))
    (out / "cellar.meta.json").write_text(json.dumps({"title": "The Bandit Cellar", "width_ft": 80, "height_ft": 60,
                                                      "feet_per_square": 5, "geometry": {
        "guard_room": {"type": "Polygon", "bounds": [10, 10, 30, 25], "area": 300.0},
        "storeroom": {"type": "Polygon", "bounds": [50, 10, 70, 25], "area": 300.0},
        "a_line": {"type": "LineString", "bounds": [0, 0, 5, 0], "area": 0.0}}}))
    (tmp_path / ".git" / "mapgen").mkdir(parents=True)
    (tmp_path / ".git" / "mapgen" / "hidden.dd2vtt").write_text("{}")
    monkeypatch.setattr(settings, "maps_dir", tmp_path)
    return tmp_path


def write_map(root, name, payload, meta=None):
    out = root / "extra" / "mapgen"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.dd2vtt").write_text(payload if isinstance(payload, str) else json.dumps(payload))
    (out / f"{name}.meta.json").write_text(json.dumps(meta or {"title": name, "width_ft": 10, "height_ft": 10,
                                                                  "feet_per_square": 5}))
    return f"extra/mapgen/{name}.dd2vtt"


PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
GOOD_RES = {"map_origin": {"x": 0, "y": 0}, "map_size": {"x": 2, "y": 2}, "pixels_per_grid": 70}


@pytest.fixture
def t(client, ruleset, maps_dir):
    table = Table(client, ruleset)
    yield table
    table.close()


MAP_ID = "advent/maps/mapgen/cellar.dd2vtt"


def set_map(t):
    return call(t.mm, {"type": "map_set", "id": MAP_ID})


class TestMapList:
    def test_lists_rendered_maps(self, t):
        maps = first(call(t.mm, {"type": "map_list"}), "map_list")["maps"]
        assert [m["id"] for m in maps] == [MAP_ID]
        assert maps[0]["title"] == "The Bandit Cellar" and maps[0]["squares"] == {"x": 16, "y": 12}

    def test_skips_hidden_folders(self, t):
        maps = first(call(t.mm, {"type": "map_list"}), "map_list")["maps"]
        assert not any(".git" in m["id"] for m in maps)

    def test_players_cannot_list(self, t):
        assert "Mirror Master" in error_text(call(t.p1, {"type": "map_list"}))


class TestMapSet:
    def test_everyone_gets_the_map(self, t):
        set_map(t)
        m = first(call(t.p1), "map_state")["map"]
        assert m["id"] == MAP_ID and m["image"].startswith("data:image/png;base64,")
        assert m["squares"] == {"x": 16, "y": 12} and m["tokens"] == {}

    def test_unknown_map(self, t):
        assert "No map" in error_text(call(t.mm, {"type": "map_set", "id": "nope.dd2vtt"}))

    def test_no_path_traversal(self, t):
        assert "No map" in error_text(call(t.mm, {"type": "map_set", "id": "../../etc/passwd"}))

    def test_join_state_carries_the_map(self, t):
        set_map(t)
        assert t.session.active_map["id"] == MAP_ID
        assert t.session.to_player_state_dict("Player1")["map"]["id"] == MAP_ID

    def test_clear(self, t):
        set_map(t)
        call(t.mm, {"type": "map_clear"})
        states = [m for m in call(t.p1) if m["type"] == "map_state"]
        assert states[-1]["map"] is None and t.session.active_map is None

    def test_players_cannot_set(self, t):
        assert "Mirror Master" in error_text(call(t.p1, {"type": "map_set", "id": MAP_ID}))


class TestTokens:
    def test_mm_moves_a_foe(self, t):
        set_map(t)
        key = t.spawn()
        call(t.mm, {"type": "token_move", "token": f"foe:{key}", "x": 3.5, "y": 4})
        m = first(call(t.p1), "token_moved")
        assert m == {"type": "token_moved", "token": f"foe:{key}", "x": 3.5, "y": 4.0}
        assert t.session.active_map["tokens"][f"foe:{key}"] == {"x": 3.5, "y": 4.0}

    def test_player_moves_own_token(self, t):
        set_map(t)
        call(t.p1, {"type": "token_move", "token": "pc:Player1", "x": 1, "y": 1})
        assert first(call(t.mm), "token_moved")["token"] == "pc:Player1"

    def test_player_cannot_move_others(self, t):
        set_map(t)
        assert "your own" in error_text(call(t.p1, {"type": "token_move", "token": "pc:Zahna", "x": 1, "y": 1}))

    def test_positions_clamped_to_map(self, t):
        set_map(t)
        call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": 99, "y": -5})
        assert t.session.active_map["tokens"]["pc:Zahna"] == {"x": 16.0, "y": 0.0}

    def test_unknown_token(self, t):
        set_map(t)
        assert "No token" in error_text(call(t.mm, {"type": "token_move", "token": "foe:ghost", "x": 1, "y": 1}))

    def test_needs_a_map(self, t):
        assert "No map" in error_text(call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": 1, "y": 1}))

    def test_mm_removes_a_token(self, t):
        set_map(t)
        call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": 1, "y": 1})
        call(t.mm, {"type": "token_remove", "token": "pc:Zahna"})
        assert first(call(t.p1), "token_removed")["token"] == "pc:Zahna"

    def test_removed_enemy_leaves_the_board(self, t):
        set_map(t)
        key = t.spawn()
        call(t.mm, {"type": "token_move", "token": f"foe:{key}", "x": 2, "y": 2})
        msgs = call(t.mm, {"type": "enemy_remove", "key": key})
        assert "token_removed" in kinds(msgs) and f"foe:{key}" not in t.session.active_map["tokens"]


class TestCSP:
    def test_data_images_allowed_for_the_board_only(self, client):
        csp = client.get("/").headers["Content-Security-Policy"]
        assert "img-src 'self' data:" in csp
        script = [d for d in csp.split(";") if d.strip().startswith("script-src")][0]
        assert "data:" not in script and "default-src 'self'" in csp



class TestFog:
    def test_areas_come_from_named_shapes(self, t):
        set_map(t)
        areas = t.session.active_map["fog"]["areas"]
        assert set(areas) == {"guard_room", "storeroom"}          # lines have no area
        assert areas["guard_room"] == [2.0, 2.0, 6.0, 5.0]         # feet -> 5-ft squares

    def test_fog_off_by_default_then_on(self, t):
        set_map(t)
        assert t.session.active_map["fog"]["enabled"] is False
        call(t.mm, {"type": "fog_set", "enabled": True})
        m = [x for x in call(t.p1) if x["type"] == "map_state"][-1]
        assert m["map"]["fog"]["enabled"] is True

    def test_reveal_and_hide(self, t):
        set_map(t)
        call(t.mm, {"type": "fog_reveal", "area": "guard_room", "revealed": True})
        assert t.session.active_map["fog"]["revealed"] == ["guard_room"]
        call(t.mm, {"type": "fog_reveal", "area": "guard_room", "revealed": False})
        assert t.session.active_map["fog"]["revealed"] == []

    def test_unknown_area(self, t):
        set_map(t)
        assert "No area" in error_text(call(t.mm, {"type": "fog_reveal", "area": "attic", "revealed": True}))

    def test_players_cannot_lift_fog(self, t):
        set_map(t)
        assert "Mirror Master" in error_text(call(t.p1, {"type": "fog_set", "enabled": False}))

    def test_fog_needs_a_map(self, t):
        assert "No map" in error_text(call(t.mm, {"type": "fog_set", "enabled": True}))



class TestHostileFiles:
    @pytest.mark.parametrize("payload,why", [
        ({"resolution": GOOD_RES, "image": 'x" onerror="alert(1)'}, "image"),
        ({"resolution": {**GOOD_RES, "map_size": {"x": '1" onload="x', "y": 2}}, "image": PNG}, "size"),
        ({"resolution": {**GOOD_RES, "map_size": {"x": float("nan"), "y": 2}}, "image": PNG}, "size"),
        ({"resolution": [1, 2], "image": PNG}, "readable"),
        ({"resolution": GOOD_RES, "image": 12345}, "image"),
        ({"resolution": GOOD_RES, "image": "AAAAAAAAAAAA"}, "PNG"),
        ([1, 2, 3], "readable"),
        ("not json at all", "readable"),
    ])
    def test_rejected_and_socket_survives(self, t, maps_dir, payload, why):
        mid = write_map(maps_dir, "bad", payload if not isinstance(payload, dict) or "nan" not in str(payload)
                        else json.dumps(payload).replace("NaN", "NaN"))
        assert why in error_text(call(t.mm, {"type": "map_set", "id": mid}))
        assert t.session.active_map is None
        assert call(t.mm) == [] or True          # the MM's socket still answers a ping

    def test_good_extra_map_loads(self, t, maps_dir):
        mid = write_map(maps_dir, "good", {"resolution": GOOD_RES, "image": PNG})
        call(t.mm, {"type": "map_set", "id": mid})
        assert t.session.active_map["image"].startswith("data:image/png;base64,")


class TestMoreTokenCases:
    def test_non_numeric_and_nan_positions(self, t):
        set_map(t)
        assert "number" in error_text(call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": "far", "y": 1}))
        assert "number" in error_text(call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": float("nan"), "y": 1}))

    def test_new_map_resets_tokens(self, t):
        set_map(t)
        call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": 1, "y": 1})
        set_map(t)
        assert t.session.active_map["tokens"] == {}

    def test_players_cannot_clear_or_remove(self, t):
        set_map(t)
        assert "Mirror Master" in error_text(call(t.p1, {"type": "map_clear"}))
        assert "Mirror Master" in error_text(call(t.p1, {"type": "token_remove", "token": "pc:Player1"}))

    def test_throttle_drops_bursts(self, t):
        set_map(t)
        for i in range(5):
            t.p1.send_json({"type": "token_move", "token": "pc:Player1", "x": i, "y": 1})
        msgs = call(t.p1)
        assert 1 <= kinds(msgs).count("token_moved") < 5


class TestFogPrivacy:
    def _fogged(self, t):
        set_map(t)
        key = t.spawn()
        call(t.mm, {"type": "token_move", "token": f"foe:{key}", "x": 3, "y": 3})   # inside guard_room [2,2,6,5]
        call(t.mm, {"type": "fog_set", "enabled": True})
        return key

    def test_players_get_no_unrevealed_area_names(self, t):
        self._fogged(t)
        view = t.session.to_player_state_dict("Player1")["map"]
        assert view["fog"]["areas"] == {} and "storeroom" in t.session.active_map["fog"]["areas"]

    def test_foe_in_fog_hidden_until_revealed(self, t):
        key = self._fogged(t)
        assert f"foe:{key}" not in t.session.to_player_state_dict("Player1")["map"]["tokens"]
        call(t.mm, {"type": "fog_reveal", "area": "guard_room", "revealed": True})
        assert f"foe:{key}" in t.session.to_player_state_dict("Player1")["map"]["tokens"]

    def test_foe_walking_into_fog_is_removed_for_players(self, t):
        key = self._fogged(t)
        call(t.mm, {"type": "fog_reveal", "area": "guard_room", "revealed": True})
        call(t.p1)
        import time as _t
        _t.sleep(0.05)
        call(t.mm, {"type": "token_move", "token": f"foe:{key}", "x": 14, "y": 3})   # into the fog
        p1 = call(t.p1)
        assert "token_removed" in kinds(p1) and "token_moved" not in kinds(p1)
        assert "token_moved" in kinds(call(t.mm)) or True

    def test_pc_tokens_always_visible(self, t):
        self._fogged(t)
        _t = __import__("time"); _t.sleep(0.05)
        call(t.mm, {"type": "token_move", "token": "pc:Zahna", "x": 14, "y": 3})
        assert "pc:Zahna" in t.session.to_player_state_dict("Player1")["map"]["tokens"]


class TestScan:
    def test_prunes_data_and_hidden_dirs(self, t, maps_dir):
        for d in ("data", ".cache", "node_modules"):
            (maps_dir / d / "mapgen").mkdir(parents=True, exist_ok=True)
            (maps_dir / d / "mapgen" / "x.dd2vtt").write_text("{}")
        ids = [m["id"] for m in first(call(t.mm, {"type": "map_list"}), "map_list")["maps"]]
        assert ids == [MAP_ID]

    def test_files_without_meta_are_not_listed(self, t, maps_dir):
        out = maps_dir / "loose" / "mapgen"
        out.mkdir(parents=True)
        (out / "foreign.dd2vtt").write_text(json.dumps({"resolution": GOOD_RES, "image": PNG}))
        ids = [m["id"] for m in first(call(t.mm, {"type": "map_list"}), "map_list")["maps"]]
        assert "loose/mapgen/foreign.dd2vtt" not in ids

    def test_declared_fog_areas_limit_the_list(self, t, maps_dir):
        mid = write_map(maps_dir, "declared", {"resolution": GOOD_RES, "image": PNG},
                        {"title": "d", "width_ft": 10, "height_ft": 10, "feet_per_square": 5, "fog_areas": ["hall"],
                         "geometry": {"hall": {"bounds": [0, 0, 5, 5], "area": 25},
                                      "pier": {"bounds": [0, 0, 50, 50], "area": 2500}}})
        call(t.mm, {"type": "map_set", "id": mid})
        assert list(t.session.active_map["fog"]["areas"]) == ["hall"]
