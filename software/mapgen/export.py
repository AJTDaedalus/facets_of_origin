"""Outputs (T24): PNG, Universal VTT (.dd2vtt) and meta.json."""
from __future__ import annotations

import base64
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image as PImage

from .engine import Engine
from .recipe import RecipeError, load_recipe


def to_pil(canvas: np.ndarray, out_size) -> PImage.Image:
    a = canvas[..., 3:4]
    rgb = np.divide(canvas[..., :3], a, out=np.ones_like(canvas[..., :3]), where=a > 1e-6)
    # flatten onto white where not opaque
    rgb = rgb * a + (1 - a)
    img = PImage.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")
    if img.size != tuple(out_size):
        img = img.resize(tuple(out_size), PImage.LANCZOS)
    return img


def image_hash(png_path) -> str:
    arr = np.asarray(PImage.open(png_path).convert("RGB"))
    return hashlib.sha256(arr.tobytes() + str(arr.shape).encode()).hexdigest()


def _pt(x, y, fps):
    return {"x": round(float(x) / fps, 4), "y": round(float(y) / fps, 4)}


def uvtt(frame, collector, png_bytes: bytes) -> dict:
    fps = frame.fps
    los = []
    for ln in collector.los:
        cs = list(ln.coords)
        if len(cs) >= 2:
            los.append([_pt(x, y, fps) for x, y in cs])
    portals = []
    for p in collector.portals:
        portals.append({"position": _pt(*p["position"], fps),
                        "bounds": [_pt(*b, fps) for b in p["bounds"]],
                        "rotation": p["rotation"], "closed": p["closed"], "freestanding": p["freestanding"]})
    lights = []
    for l in collector.lights:
        lights.append({"position": _pt(*l["position"], fps), "range": round(l["range"] / fps, 4),
                       "intensity": l["intensity"], "color": "ff" + l["color"].lstrip("#"),
                       "shadows": l["shadows"]})
    return {
        "format": 0.3,
        "resolution": {"map_origin": {"x": 0, "y": 0},
                       "map_size": {"x": round(frame.width_ft / fps, 4), "y": round(frame.height_ft / fps, 4)},
                       "pixels_per_grid": frame.pps},
        "line_of_sight": los,
        "objects_line_of_sight": [],
        "portals": portals,
        "environment": {"baked_lighting": True, "ambient_light": "ffffffff"},
        "lights": lights,
        "image": base64.b64encode(png_bytes).decode("ascii"),
    }


def _geom_info(g) -> dict:
    minx, miny, maxx, maxy = g.bounds if not g.is_empty else (0, 0, 0, 0)
    return {"type": g.geom_type, "bounds": [round(v, 4) for v in (minx, miny, maxx, maxy)],
            "w": round(maxx - minx, 4), "h": round(maxy - miny, 4), "area": round(g.area, 4),
            "length": round(g.length, 4)}


def meta(recipe, frame, collector) -> dict:
    geoms = {k: _geom_info(g) for k, g in collector.geometry.items()}
    measures = {}
    for name, declared in recipe.measure.items():
        if name not in collector.geometry:
            raise RecipeError(f"measure: no geometry named '{name}' (name the step's `out`)")
        info = geoms[name]
        measures[name] = {"declared": declared, "actual": {k: info[k] for k in ("w", "h", "area", "length")}}
    return {
        "title": recipe.map.title, "width_ft": recipe.map.width_ft, "height_ft": recipe.map.height_ft,
        "feet_per_square": recipe.map.feet_per_square, "px_per_square": frame.pps, "seed": recipe.map.seed,
        "draft": frame.draft, "measures": measures, "geometry": geoms,
        "walls": {k: {"floor": _geom_info(v["floor"]) if v.get("floor") is not None else None,
                      "line": _geom_info(v["line"]) if v.get("line") is not None else None,
                      "thickness": v["thickness"]} for k, v in collector.walls.items()},
        "portals": collector.portals, "lights": collector.lights, "legend": sorted(collector.legend),
        "los_segments": len(collector.los), "los_length_ft": round(sum(l.length for l in collector.los), 3),
    }


def stem_of(path: Path) -> str:
    name = path.name
    for suf in (".map.yaml", ".map.yml", ".yaml", ".yml"):
        if name.endswith(suf):
            return name[: -len(suf)]
    return path.stem


def render_recipe(path, out_dir=None, draft: bool = False, only_png: bool = False) -> dict:
    path = Path(path)
    recipe = load_recipe(path)
    eng = Engine(recipe, draft=draft)
    store = eng.run()
    if "canvas" not in store:
        raise RecipeError("the recipe never made a layer named 'canvas' (start with {op: canvas, out: canvas})")
    out = Path(out_dir) if out_dir else path.parent / "mapgen"
    out.mkdir(parents=True, exist_ok=True)
    stem = stem_of(path)
    img = to_pil(store.get("canvas").data, eng.frame.out_size)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=False)
    png = out / f"{stem}.png"
    png.write_bytes(buf.getvalue())
    result = {"png": str(png)}
    if only_png:
        return result
    m = meta(recipe, eng.frame, eng.collector)
    (out / f"{stem}.meta.json").write_text(json.dumps(m, indent=2) + "\n")
    (out / f"{stem}.dd2vtt").write_text(json.dumps(uvtt(eng.frame, eng.collector, buf.getvalue())))
    result["meta"] = str(out / f"{stem}.meta.json")
    result["dd2vtt"] = str(out / f"{stem}.dd2vtt")
    result["collector"] = eng.collector
    return result
