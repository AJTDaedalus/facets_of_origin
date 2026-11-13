"""Semantic ops (T19, T20): walls and openings paint *and* emit VTT data."""
from __future__ import annotations

from typing import Any, Literal

import numpy as np
import shapely
from pydantic import Field as PField
from shapely.geometry import LineString, MultiLineString, Point as SPoint, Polygon, box
from shapely.ops import linemerge

from ..color import composite_inplace, composite_patch, resolve_color
from ..layers import Geometry, Image
from ..noise import fbm_at
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import NonNegFt, Point, PosFt, Ref, Unit, polygonal
from .geometry import _rough_ring
from .masks import rasterize_geom, rasterize_patch
from .materials import render_material
from .paint import _width_ft, lines_of, stroke_geometry_alpha

DEFAULTS = {"wall": "#8f877a", "door": "#efe6d2", "door_ink": "ink", "secret": "#9c2a1f",
            "stair": "#d6cdbb", "window": "#f4f0e6"}


def col(ctx, name_or_color, key=None):
    try:
        return resolve_color(ctx.style, name_or_color)
    except RecipeError:
        if key and key in DEFAULTS:
            return resolve_color(ctx.style, DEFAULTS[key])
        raise


def _split_lines(g) -> list[LineString]:
    if g.is_empty:
        return []
    if isinstance(g, LineString):
        return [g]
    if isinstance(g, MultiLineString):
        return list(g.geoms)
    if hasattr(g, "geoms"):
        out = []
        for x in g.geoms:
            out.extend(_split_lines(x))
        return out
    return []


class WallP(ParamModel):
    into: Ref = "canvas"
    src: Ref
    name: str = "wall"
    thickness: PosFt = 1.0
    style: Literal["dressed", "rough", "ruined"] = "dressed"
    fill: Any = "wall"
    material: str | None = None
    weight: str | None = "heavy"
    outer_weight: str | None = "fine"
    ink: Any = "ink"
    roughness: NonNegFt | None = None
    gaps: float = PField(0.3, ge=0, le=0.9)
    emit_los: bool = True
    exclude: Ref | None = None


@op("wall", params=WallP, inputs={"into": Image, "src": Geometry, "exclude": Geometry}, group="5 semantic")
def wall(ctx, p, into, src, exclude=None):
    """Walls around a floor polygon (the walkable area): a band `thickness` feet outside its edge, filled and inked. Styles: dressed (true lines), rough (cave rock, wobbly outer edge), ruined (noise gaps). Emits line-of-sight walls and registers `name` for doors. `exclude` (a geometry) leaves a stretch open, e.g. a cave mouth."""
    floor = polygonal(src.geom)
    if floor.is_empty:
        raise RecipeError("wall needs a polygon (the floor it surrounds)")
    t = p.thickness
    lines = [LineString(l.coords) for l in lines_of(floor)]
    outer = floor.buffer(t, join_style=2, mitre_limit=4)
    rough = p.roughness if p.roughness is not None else (0.35 if p.style == "rough" else 0.0)
    if p.style == "rough" and rough > 0:
        outer = polygonal(shapely.segmentize(outer, 0.5))
        rings = []
        for pg in getattr(outer, "geoms", [outer]):
            rings.append(Polygon(_rough_ring(pg.exterior.coords, rough, 4.0, ctx.seed),
                                 [_rough_ring(h.coords, rough, 4.0, ctx.seed + 1) for h in pg.interiors]))
        outer = polygonal(shapely.unary_union(rings)).union(floor.buffer(t * 0.4))
    band = polygonal(outer.difference(floor))
    kept = lines
    if p.style == "ruined" and p.gaps > 0:
        segs, scores = [], []
        for ln in lines:
            ln = shapely.segmentize(ln, 1.0)
            cs = list(ln.coords)
            for a, b in zip(cs[:-1], cs[1:]):
                segs.append(LineString([a, b]))
        mids = np.array([s.interpolate(0.5, normalized=True).coords[0] for s in segs])
        scores = fbm_at(mids[:, 0], mids[:, 1], 7.0, ctx.seed, 3)
        cut = np.quantile(scores, 1 - p.gaps)
        keep = [s for s, sc in zip(segs, scores) if sc < cut]
        merged = linemerge(keep) if keep else LineString()
        kept = _split_lines(merged)
        cover = shapely.unary_union([k.buffer(t * 1.05, cap_style=2) for k in kept]) if kept else Polygon()
        band = polygonal(band.intersection(cover))
    if exclude is not None and not exclude.geom.is_empty:
        band = polygonal(band.difference(exclude.geom))
        cut = []
        for k in kept:
            cut.extend(_split_lines(k.difference(exclude.geom)))
        kept = [k for k in cut if k.length > 1e-6]
    if not band.is_empty:
        patch = rasterize_patch(ctx.frame, band)
        if patch is None:
            pass                                  # wall lies entirely off the map: nothing to paint
        elif p.material:
            m = np.zeros(ctx.frame.shape, np.float32)
            m[patch.slices] = patch.alpha
            composite_inplace(into.data, render_material(ctx, p.material, m, ctx.seed), m)
        else:
            composite_patch(into.data, patch, col(ctx, p.fill, "wall")[:3])
        inkc = resolve_color(ctx.style, p.ink)[:3]
        if p.outer_weight:
            w = _width_ft(ctx, type("W", (), {"width": None, "weight": p.outer_weight})())
            composite_patch(into.data, stroke_geometry_alpha(ctx, band, w, patch=True), inkc)
        if p.weight:
            w = _width_ft(ctx, type("W", (), {"width": None, "weight": p.weight})())
            edge = shapely.unary_union(kept) if kept else LineString()
            composite_patch(into.data, stroke_geometry_alpha(ctx, edge, w, patch=True), inkc)
    ctx.collector.walls[p.name] = {"floor": floor, "band": band, "thickness": t, "lines": kept, "d0": 0.0}
    if p.emit_los:
        ctx.collector.los.extend(kept)


class PartitionP(ParamModel):
    into: Ref = "canvas"
    src: Ref
    name: str = "partition"
    thickness: PosFt = 0.75
    fill: Any = "wall"
    material: str | None = None
    weight: str | None = "medium"
    ink: Any = "ink"
    emit_los: bool = True


@op("partition", params=PartitionP, inputs={"into": Image, "src": Geometry}, group="5 semantic")
def partition(ctx, p, into, src):
    """An interior wall along a line (or a polygon's outline), centred on it, `thickness` feet. Emits LOS and registers `name`, so doors can be set in it."""
    lines = [LineString(l.coords) for l in lines_of(src.geom)]
    if not lines:
        raise RecipeError("partition needs a line or polygon")
    t = p.thickness
    geom = shapely.unary_union(lines)
    band = polygonal(geom.buffer(t / 2, cap_style=2, join_style=2))
    patch = rasterize_patch(ctx.frame, band)
    if patch is None:
        pass
    elif p.material:
        m = np.zeros(ctx.frame.shape, np.float32)
        m[patch.slices] = patch.alpha
        composite_inplace(into.data, render_material(ctx, p.material, m, ctx.seed), m)
    else:
        composite_patch(into.data, patch, col(ctx, p.fill, "wall")[:3])
    if p.weight:
        w = _width_ft(ctx, type("W", (), {"width": None, "weight": p.weight})())
        composite_patch(into.data, stroke_geometry_alpha(ctx, band, w, patch=True), resolve_color(ctx.style, p.ink)[:3])
    ctx.collector.walls[p.name] = {"floor": None, "line": geom, "band": band, "thickness": t, "lines": lines,
                                   "d0": -t / 2}
    if p.emit_los:
        ctx.collector.los.extend(lines)


# ---------- openings ----------

class OpeningP(ParamModel):
    into: Ref = "canvas"
    wall: str
    mark: bool = False
    at: Point
    width: PosFt | None = None
    color: Any = None
    ink: Any = "ink"
    floor_color: Any = None
    floor_material: str | None = None
    closed: bool = True


def _locate(ctx, p, default_w):
    rec = ctx.collector.walls.get(p.wall)
    if rec is None:
        raise RecipeError(f"wall '{p.wall}' is not defined (give the wall op name: {p.wall})")
    floor, t = rec["floor"], rec["thickness"]
    bnd = floor.boundary if floor is not None else rec["line"]
    P = SPoint(p.at)
    d = bnd.project(P)
    q = np.array(bnd.interpolate(d).coords[0])
    a = np.array(bnd.interpolate(max(d - 0.05, 0)).coords[0])
    b = np.array(bnd.interpolate(d + 0.05).coords[0])
    tng = b - a
    if np.linalg.norm(tng) < 1e-9:
        tng = np.array([1.0, 0.0])
    tng = tng / np.linalg.norm(tng)
    nrm = np.array([-tng[1], tng[0]])
    if floor is not None and floor.contains(SPoint(q + nrm * 0.1)):
        nrm = -nrm
    w = p.width or default_w
    return rec, q, tng, nrm, w, t


def _draw_q(rec, q, nrm):
    return q + nrm * rec.get("d0", 0.0)


def _rect(q, tng, nrm, w, d0, d1):
    hw = tng * w / 2
    return Polygon([q - hw + nrm * d0, q + hw + nrm * d0, q + hw + nrm * d1, q - hw + nrm * d1])





def _cut_los(ctx, q, tng, w):
    # The cut is a thin strip along the door, stopping 1e-3 ft short of each jamb so a wall
    # that meets the jamb (e.g. a perpendicular partition) keeps its endpoint on the door.
    half = max(w / 2 - 1e-3, 0)
    gap = LineString([q - tng * half, q + tng * half]).buffer(0.08, cap_style=2)
    new = []
    for ln in ctx.collector.los:
        if ln.intersects(gap):
            new.extend(_split_lines(ln.difference(gap)))
        else:
            new.append(ln)
    ctx.collector.los = [l for l in new if l.length > 1e-6]


def _portal(ctx, kind, q, tng, w, closed=True, secret=False):
    a, b = q - tng * w / 2, q + tng * w / 2
    ctx.collector.portals.append({
        "kind": kind, "position": [float(q[0]), float(q[1])],
        "bounds": [[float(a[0]), float(a[1])], [float(b[0]), float(b[1])]],
        "rotation": float(np.arctan2(tng[1], tng[0])), "closed": bool(closed),
        "secret": bool(secret), "freestanding": False})
    ctx.collector.legend.setdefault(kind, kind.replace("_", " "))


def _fill_poly(ctx, img, g, color):
    composite_patch(img, rasterize_patch(ctx.frame, g), color[:3], float(color[3]))


def _ink(ctx, img, g, width, color="ink"):
    composite_patch(img, stroke_geometry_alpha(ctx, g, width, patch=True), resolve_color(ctx.style, color)[:3])


@op("door", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def door(ctx, p, into):
    """A door in a named wall, snapped to the wall edge nearest `at` (default 5 ft wide = one square... use 3–5). Draws a door leaf across the wall, cuts the LOS and emits a portal."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 4.0)
    dq = _draw_q(rec, q, nrm)
    leaf = _rect(dq, tng, nrm, w * 0.9, t * 0.2, t * 0.8)
    gap = _rect(dq, tng, nrm, w, -0.02, t + 0.02)
    _fill_poly(ctx, into.data, gap, col(ctx, p.floor_color or p.color or "door", "door"))
    _fill_poly(ctx, into.data, leaf, col(ctx, p.color or "door", "door"))
    _ink(ctx, into.data, leaf, 0.12, p.ink)
    _cut_los(ctx, q, tng, w)
    _portal(ctx, "door", q, tng, w, p.closed)


@op("double_door", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def double_door(ctx, p, into):
    """Two door leaves meeting in the middle (default 8 ft); one portal."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 8.0)
    dq = _draw_q(rec, q, nrm)
    gap = _rect(dq, tng, nrm, w, -0.02, t + 0.02)
    _fill_poly(ctx, into.data, gap, col(ctx, p.floor_color or p.color or "door", "door"))
    for s in (-1, 1):
        leaf = _rect(dq + tng * s * w / 4, tng, nrm, w * 0.45, t * 0.2, t * 0.8)
        _fill_poly(ctx, into.data, leaf, col(ctx, p.color or "door", "door"))
        _ink(ctx, into.data, leaf, 0.12, p.ink)
    _cut_los(ctx, q, tng, w)
    _portal(ctx, "double_door", q, tng, w, p.closed)


@op("secret_door", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def secret_door(ctx, p, into):
    """A secret door. The wall stays drawn and keeps blocking sight in the VTT data (Universal VTT has no secret flag, so exporting it as a door would show players a door). It's recorded in meta.json. `mark: true` paints the red `S` (for a DM-only print; the image goes to players)."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 4.0)
    if p.mark:
        from .overlay import draw_text
        draw_text(ctx, into.data, "S", _draw_q(rec, q, nrm) + nrm * t / 2, max(t * 1.6, 1.6),
                  col(ctx, p.color or "secret", "secret"), bold=True, halo=None)
    _portal(ctx, "secret_door", q, tng, w, True, secret=True)


@op("portcullis", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def portcullis(ctx, p, into):
    """Bars across a wall gap (a row of dots). The wall's LOS is cut and a closed portal emitted, so in a VTT it behaves as a door: it blocks sight until opened. Real bars would let sight through; Universal VTT can't express that."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 5.0)
    dq = _draw_q(rec, q, nrm)
    gap = _rect(dq, tng, nrm, w, -0.02, t + 0.02)
    _fill_poly(ctx, into.data, gap, col(ctx, p.floor_color or "door", "door"))
    n = max(3, int(w / 0.7))
    for i in range(n):
        c = dq - tng * w / 2 + tng * w * (i + 0.5) / n + nrm * t / 2
        _fill_poly(ctx, into.data, SPoint(c).buffer(0.18), resolve_color(ctx.style, p.ink))
    _cut_los(ctx, q, tng, w)
    _portal(ctx, "portcullis", q, tng, w, True)


@op("window", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def window(ctx, p, into):
    """A window: a pale pane across the wall with a centre line. Walls still block movement and sight in VTT data."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 3.0)
    dq = _draw_q(rec, q, nrm)
    pane = _rect(dq, tng, nrm, w, t * 0.25, t * 0.75)
    _fill_poly(ctx, into.data, pane, col(ctx, p.color or "window", "window"))
    _ink(ctx, into.data, pane, 0.08, p.ink)
    _ink(ctx, into.data, LineString([dq - tng * w / 2 + nrm * t / 2, dq + tng * w / 2 + nrm * t / 2]), 0.06, p.ink)
    ctx.collector.legend.setdefault("window", "window")


@op("opening", params=OpeningP, inputs={"into": Image}, group="5 semantic")
def opening(ctx, p, into):
    """An open doorway or arch: the wall is cut and filled with floor colour/material; LOS cut, no portal."""
    rec, q, tng, nrm, w, t = _locate(ctx, p, 5.0)
    dq = _draw_q(rec, q, nrm)
    gap = _rect(dq, tng, nrm, w, -0.05, t + 0.1)
    if p.floor_material:
        m = rasterize_geom(ctx.frame, gap)
        composite_inplace(into.data, render_material(ctx, p.floor_material, m, ctx.seed), m)
    else:
        _fill_poly(ctx, into.data, gap, col(ctx, p.floor_color or "floor", "door"))
    for s in (-1, 1):
        e = dq + tng * s * w / 2
        _ink(ctx, into.data, LineString([e, e + nrm * t]), 0.14, p.ink)
    _cut_los(ctx, q, tng, w)


class StairsP(ParamModel):
    into: Ref = "canvas"
    x: float
    y: float
    w: PosFt
    h: PosFt
    down: Literal["n", "e", "s", "w"] = "s"
    step: PosFt = 1.0
    color: Any = "stair"
    ink: Any = "ink"
    shade: Unit = 0.45


@op("stairs", params=StairsP, inputs={"into": Image}, group="5 semantic")
def stairs(ctx, p, into):
    """A flight of stairs in a rectangle, treads `step` feet apart, darkening toward the `down` side."""
    r = box(p.x, p.y, p.x + p.w, p.y + p.h)
    base = col(ctx, p.color, "stair")
    _fill_poly(ctx, into.data, r, base)
    horizontal = p.down in ("n", "s")
    length = p.h if horizontal else p.w
    n = max(2, int(round(length / p.step)))
    for i in range(n):
        f = (i + 1) / n
        k = f if p.down in ("s", "e") else 1 - f + 1 / n
        if horizontal:
            y0 = p.y + p.h * i / n
            tread = box(p.x, y0, p.x + p.w, y0 + p.h / n)
            line = LineString([(p.x, y0), (p.x + p.w, y0)])
        else:
            x0 = p.x + p.w * i / n
            tread = box(x0, p.y, x0 + p.w / n, p.y + p.h)
            line = LineString([(x0, p.y), (x0, p.y + p.h)])
        composite_patch(into.data, rasterize_patch(ctx.frame, tread), (0, 0, 0), p.shade * k)
        if i:
            _ink(ctx, into.data, line, 0.07, p.ink)
    _ink(ctx, into.data, r, 0.12, p.ink)
    ctx.collector.legend.setdefault("stairs", "stairs")


class LightP(ParamModel):
    into: Ref = "canvas"
    at: Point
    radius: PosFt = 20.0
    color: Any = "#ffd9a0"
    intensity: Unit = 0.8
    glow: bool = False
    glow_radius: PosFt | None = None


@op("light", params=LightP, inputs={"into": Image}, group="5 semantic")
def light(ctx, p, into):
    """A light source for the VTT (range in feet); `glow: true` also paints a soft screen-blended glow."""
    c = resolve_color(ctx.style, p.color)
    if p.glow:
        fr = ctx.frame
        gr = p.glow_radius or p.radius / 3
        h, w = fr.shape
        y = (np.arange(h, dtype=np.float32) + 0.5)[:, None] / fr.scale
        x = (np.arange(w, dtype=np.float32) + 0.5)[None, :] / fr.scale
        d = np.hypot(x - p.at[0], y - p.at[1])
        a = np.clip(1 - d / gr, 0, 1) ** 2 * p.intensity * 0.6
        composite_inplace(into.data, c[:3], a.astype(np.float32), "screen")
    hexc = "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])
    ctx.collector.lights.append({"position": [float(p.at[0]), float(p.at[1])], "range": float(p.radius),
                                 "intensity": float(p.intensity), "color": hexc, "shadows": True})
