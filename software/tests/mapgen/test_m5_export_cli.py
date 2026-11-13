"""T24-T26: export (PNG, dd2vtt, meta.json), CLI, golden renders."""
import base64
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image as PImage

from mapgen import __main__ as cli
from mapgen.export import render_recipe, image_hash, stem_of
from tests.mapgen.conftest import header

HERE = Path(__file__).parent
SOFTWARE = HERE.parents[1]
FIX = json.loads((HERE / "fixtures" / "uvtt_min.json").read_text())

ROOM = {"map": header(width_ft=30, height_ft=20, px_per_square=20, title="Room"),
        "measure": {"room": {"w": 20, "h": 10}},
        "steps": [{"op": "canvas", "out": "canvas", "color": "#ffffff"},
                  {"op": "rect", "out": "room", "x": 5, "y": 5, "w": 20, "h": 10},
                  {"op": "wall", "src": "room", "name": "w"},
                  {"op": "door", "wall": "w", "at": [15, 5]},
                  {"op": "light", "at": [15, 10], "radius": 15}]}


@pytest.fixture
def rendered(write_recipe, tmp_out):
    p = write_recipe(ROOM, name="room.map.yaml")
    return render_recipe(p, out_dir=tmp_out)


# ---------- T24 ----------
class TestExport:
    def test_writes_three_files(self, rendered):
        assert {k for k in rendered} >= {"png", "dd2vtt", "meta"}
        for k in ("png", "dd2vtt", "meta"):
            assert Path(rendered[k]).is_file()
        assert Path(rendered["png"]).name == "room.png"

    def test_png_size(self, rendered):
        assert PImage.open(rendered["png"]).size == (120, 80)

    def test_uvtt_shape(self, rendered):
        d = json.loads(Path(rendered["dd2vtt"]).read_text())
        for k in FIX["required"]:
            assert k in d
        for k in FIX["resolution"]["required"]:
            assert k in d["resolution"]
        assert d["resolution"]["pixels_per_grid"] == 20
        assert d["resolution"]["map_size"] == {"x": 6, "y": 4}
        for k in FIX["portal"]:
            assert k in d["portals"][0]
        for k in FIX["light"]:
            assert k in d["lights"][0]

    def test_uvtt_units_are_squares(self, rendered):
        d = json.loads(Path(rendered["dd2vtt"]).read_text())
        pts = [pt for line in d["line_of_sight"] for pt in line]
        xs = [pt["x"] for pt in pts]
        assert min(xs) == pytest.approx(1) and max(xs) == pytest.approx(5)
        assert d["portals"][0]["position"] == {"x": pytest.approx(3), "y": pytest.approx(1)}
        assert d["lights"][0]["range"] == pytest.approx(3)

    def test_uvtt_image_round_trips(self, rendered):
        d = json.loads(Path(rendered["dd2vtt"]).read_text())
        img = PImage.open(io.BytesIO(base64.b64decode(d["image"])))
        assert np.array_equal(np.asarray(img), np.asarray(PImage.open(rendered["png"])))

    def test_meta_measures(self, rendered):
        m = json.loads(Path(rendered["meta"]).read_text())
        assert m["measures"]["room"]["declared"] == {"w": 20, "h": 10}
        assert m["measures"]["room"]["actual"]["w"] == pytest.approx(20)
        assert m["geometry"]["room"]["area"] == pytest.approx(200)

    def test_meta_with_partition(self, write_recipe, tmp_out):
        rec = dict(ROOM, steps=ROOM["steps"] + [
            {"op": "path", "out": "split", "points": [[15, 5], [15, 15]], "line": True},
            {"op": "partition", "src": "split", "name": "mid"}])
        r = render_recipe(write_recipe(rec, name="p.map.yaml"), out_dir=tmp_out)
        m = json.loads(Path(r["meta"]).read_text())
        assert m["walls"]["mid"]["floor"] is None and m["walls"]["mid"]["line"]["length"] == pytest.approx(10)

    def test_measure_of_missing_geometry_errors(self, write_recipe, tmp_out):
        bad = dict(ROOM, measure={"nothing": {"w": 1}})
        with pytest.raises(Exception, match="nothing"):
            render_recipe(write_recipe(bad), out_dir=tmp_out)

    def test_only_png(self, write_recipe, tmp_out):
        r = render_recipe(write_recipe(ROOM, name="x.map.yaml"), out_dir=tmp_out, only_png=True)
        assert set(r) == {"png"}

    def test_default_out_dir_beside_recipe(self, write_recipe, tmp_path):
        p = write_recipe(ROOM, name="y.map.yaml")
        r = render_recipe(p, only_png=True)
        assert Path(r["png"]).parent == p.parent / "mapgen"


# ---------- T25 ----------
class TestCli:
    def test_render(self, write_recipe, tmp_out):
        p = write_recipe(ROOM, name="c.map.yaml")
        assert cli.main(["render", str(p), "--out", str(tmp_out)]) == 0
        assert (tmp_out / "c.png").is_file() and (tmp_out / "c.dd2vtt").is_file()

    def test_draft_is_smaller(self, write_recipe, tmp_out):
        p = write_recipe(dict(ROOM, map=header(width_ft=30, height_ft=20, px_per_square=70)), name="d.map.yaml")
        cli.main(["render", str(p), "--out", str(tmp_out / "full"), "--only-png"])
        cli.main(["render", str(p), "--out", str(tmp_out / "draft"), "--only-png", "--draft"])
        assert PImage.open(tmp_out / "draft" / "d.png").size[0] < PImage.open(tmp_out / "full" / "d.png").size[0]

    def test_ops_markdown_lists_every_op(self, capsys):
        from mapgen.ops import REGISTRY
        assert cli.main(["ops", "--markdown"]) == 0
        out = capsys.readouterr().out
        for spec in REGISTRY.list():
            assert f"`{spec.name}`" in out

    def test_bad_recipe_exits_2_naming_step(self, write_recipe, tmp_out, capsys):
        p = write_recipe({"map": header(), "steps": [{"op": "rect", "out": "a", "x": 0}]})
        assert cli.main(["render", str(p), "--out", str(tmp_out)]) == 2
        assert "step 1" in capsys.readouterr().err

    def test_ops_plain(self, capsys):
        assert cli.main(["ops"]) == 0
        assert "rect" in capsys.readouterr().out


# ---------- T26 ----------
GOLDENS = sorted((HERE / "goldens").glob("*.map.yaml"))
HASHES = HERE / "goldens" / "hashes.json"


@pytest.mark.parametrize("recipe", GOLDENS, ids=lambda p: p.stem)
def test_golden(recipe, tmp_out):
    r = render_recipe(recipe, out_dir=tmp_out, only_png=True)
    h = image_hash(r["png"])
    known = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    if os.environ.get("MAPGEN_UPDATE_GOLDENS"):
        known[stem_of(recipe)] = h
        HASHES.write_text(json.dumps(known, indent=2, sort_keys=True) + "\n")
        pytest.skip("golden updated")
    assert stem_of(recipe) in known, "no golden yet: run with MAPGEN_UPDATE_GOLDENS=1"
    assert h == known[stem_of(recipe)]


def test_golden_stable_across_processes(tmp_out):
    code = ("import sys; sys.path.insert(0, '.');"
            "from mapgen.export import render_recipe, image_hash, stem_of;"
            f"print(image_hash(render_recipe(r'{GOLDENS[0]}', out_dir=r'{tmp_out}', only_png=True)['png']))")
    outs = {subprocess.run([sys.executable, "-c", code], cwd=SOFTWARE, capture_output=True, text=True,
                           env={**os.environ, "PYTHONHASHSEED": s}).stdout.strip() for s in ("1", "2")}
    assert len(outs) == 1 and len(next(iter(outs))) == 64


def test_param_change_breaks_golden(tmp_path, tmp_out):
    room = HERE / "goldens" / "stone_room.map.yaml"
    src = room.read_text()
    assert "strength: 0.4" in src
    p = tmp_path / room.name
    p.write_text(src.replace("strength: 0.4", "strength: 0.6"))
    known = json.loads(HASHES.read_text())
    assert image_hash(render_recipe(p, out_dir=tmp_out, only_png=True)["png"]) != known["stone_room"]


class TestFoundryImporterConformance:
    """What the public Foundry 'Universal Battlemap Importer' (moo-man/FVTT-DD-Import, ddimport.js)
    actually reads, checked 2026-11-13: missing arrays or empty polylines throw there."""

    def _d(self, rendered):
        return json.loads(Path(rendered["dd2vtt"]).read_text())

    def test_required_arrays_always_present(self, rendered):
        d = self._d(rendered)
        for k in ("line_of_sight", "portals", "lights"):
            assert isinstance(d[k], list)
        assert {"x", "y"} <= set(d["resolution"]["map_origin"]) and {"x", "y"} <= set(d["resolution"]["map_size"])

    def test_no_empty_or_single_point_polylines(self, rendered):
        assert all(len(line) >= 2 for line in self._d(rendered)["line_of_sight"])

    def test_portal_bounds_are_two_points(self, rendered):
        for p in self._d(rendered)["portals"]:
            assert len(p["bounds"]) == 2 and isinstance(p["closed"], bool)

    def test_light_colour_is_argb_hex(self, rendered):
        import re
        for l in self._d(rendered)["lights"]:
            assert re.fullmatch(r"[0-9a-f]{8}", l["color"]) and l["color"].startswith("ff")

    def test_image_is_bare_base64_png_matching_the_grid(self, rendered):
        d = self._d(rendered)
        raw = base64.b64decode(d["image"])
        assert not d["image"].startswith("data:") and raw[:4] == b"\x89PNG"
        w, h = PImage.open(io.BytesIO(raw)).size
        ppg = d["resolution"]["pixels_per_grid"]
        assert (w, h) == (round(d["resolution"]["map_size"]["x"] * ppg), round(d["resolution"]["map_size"]["y"] * ppg))
