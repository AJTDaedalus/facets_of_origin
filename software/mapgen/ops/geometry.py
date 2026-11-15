"""Geometry ops (T7, T8): shapes and booleans in feet."""
from __future__ import annotations

from typing import Literal

import numpy as np
import shapely
from pydantic import Field as PField
from shapely import affinity
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point as SPoint, Polygon, box

from ..layers import Geometry, Mask
from ..noise import fbm_at
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import NonNegFt, Point, PosFt, Ref, polygonal

ROUGH_GAIN = 2.0   # fbm rarely nears ±1; this makes `amount` read as feet of wobble
JOIN = {"round": 1, "mitre": 2, "bevel": 3}
CAP = {"round": 1, "flat": 2, "square": 3}


class RectP(ParamModel):
    x: float
    y: float
    w: PosFt
    h: PosFt
    rotate: float = 0.0


@op("rect", params=RectP, output=Geometry, group="1 geometry")
def rect(ctx, p):
    """Rectangle with its north-west corner at (x, y), w × h feet; optional rotation (degrees, about its centre)."""
    g = box(p.x, p.y, p.x + p.w, p.y + p.h)
    if p.rotate:
        g = affinity.rotate(g, p.rotate, origin="center")
    return Geometry(g)


class PolygonP(ParamModel):
    points: list[Point] = PField(min_length=3)
    holes: list[list[Point]] = []


@op("polygon", params=PolygonP, output=Geometry, group="1 geometry")
def polygon(ctx, p):
    """Polygon from a list of [x, y] points in feet, with optional holes. Self-intersections are repaired."""
    return Geometry(polygonal(Polygon(p.points, [h for h in p.holes if len(h) >= 3])))


class CircleP(ParamModel):
    center: Point
    r: PosFt


@op("circle", params=CircleP, output=Geometry, group="1 geometry")
def circle(ctx, p):
    """Circle of radius r feet."""
    return Geometry(SPoint(p.center).buffer(p.r, quad_segs=32))


class EllipseP(ParamModel):
    center: Point
    rx: PosFt
    ry: PosFt
    rotate: float = 0.0


@op("ellipse", params=EllipseP, output=Geometry, group="1 geometry")
def ellipse(ctx, p):
    """Ellipse with radii rx, ry feet, optionally rotated (degrees)."""
    g = affinity.scale(SPoint(p.center).buffer(1.0, quad_segs=32), p.rx, p.ry)
    if p.rotate:
        g = affinity.rotate(g, p.rotate, origin="center")
    return Geometry(g)


class PathP(ParamModel):
    points: list[Point] = PField(min_length=2)
    width: PosFt = 5.0
    cap: Literal["round", "flat", "square"] = "round"
    join: Literal["round", "mitre", "bevel"] = "round"
    line: bool = False
    smooth: int = PField(0, ge=0, le=5)


def _chaikin(pts, n):
    pts = np.asarray(pts, float)
    for _ in range(n):
        q = 0.75 * pts[:-1] + 0.25 * pts[1:]
        r = 0.25 * pts[:-1] + 0.75 * pts[1:]
        mid = np.empty((len(q) * 2, 2))
        mid[0::2], mid[1::2] = q, r
        pts = np.vstack([pts[:1], mid, pts[-1:]])
    return pts


@op("path", params=PathP, output=Geometry, group="1 geometry")
def path(ctx, p):
    """A polyline through points, buffered to `width` feet (a corridor, road or stream). `smooth` rounds the corners (Chaikin passes); `line: true` keeps the centre line instead."""
    pts = _chaikin(p.points, p.smooth) if p.smooth else p.points
    ln = LineString(pts)
    if p.line:
        return Geometry(ln)
    return Geometry(ln.buffer(p.width / 2, cap_style=CAP[p.cap], join_style=JOIN[p.join], quad_segs=16))


class ManyP(ParamModel):
    of: list[Ref] = PField(min_length=1)


@op("union", params=ManyP, inputs={"of": Geometry}, output=Geometry, group="1 geometry")
def union(ctx, p, of):
    """Union of several geometries."""
    return Geometry(shapely.unary_union([g.geom for g in of]))


@op("intersect", params=ManyP, inputs={"of": Geometry}, output=Geometry, group="1 geometry")
def intersect(ctx, p, of):
    """Intersection of several geometries (may be empty)."""
    g = of[0].geom
    for o in of[1:]:
        g = g.intersection(o.geom)
    return Geometry(g)


class SubP(ParamModel):
    a: Ref
    b: list[Ref] = PField(min_length=1)


@op("subtract", params=SubP, inputs={"a": Geometry, "b": Geometry}, output=Geometry, group="1 geometry")
def subtract(ctx, p, a, b):
    """`a` minus every geometry in `b`."""
    return Geometry(a.geom.difference(shapely.unary_union([g.geom for g in b])))


class OffsetP(ParamModel):
    src: Ref
    by: float
    join: Literal["round", "mitre", "bevel"] = "round"


@op("offset", params=OffsetP, inputs={"src": Geometry}, output=Geometry, group="1 geometry")
def offset(ctx, p, src):
    """Grow (by > 0) or shrink (by < 0) a geometry by `by` feet."""
    return Geometry(src.geom.buffer(p.by, join_style=JOIN[p.join], mitre_limit=5.0, quad_segs=16))


class TransformP(ParamModel):
    src: Ref
    rotate: float = 0.0
    about: Point | None = None
    move: Point = [0.0, 0.0]
    scale: float = PField(1.0, gt=0)
    skew: Point = [0.0, 0.0]


@op("transform", params=TransformP, inputs={"src": Geometry}, output=Geometry, group="1 geometry")
def transform(ctx, p, src):
    """Scale, skew [x°, y°], rotate (degrees, clockwise on the map since y runs south) about `about` (default: the shape's centroid), then `move` [dx, dy] feet. Knocks a wing askew so an add-on doesn't line up with the building it's bolted to."""
    g = src.geom
    if g.is_empty:
        return Geometry(g)
    o = tuple(p.about) if p.about else g.centroid.coords[0]
    if p.scale != 1:
        g = affinity.scale(g, p.scale, p.scale, origin=o)
    if p.skew != [0.0, 0.0]:
        g = affinity.skew(g, p.skew[0], p.skew[1], origin=o)
    if p.rotate:
        g = affinity.rotate(g, p.rotate, origin=o)
    if p.move != [0.0, 0.0]:
        g = affinity.translate(g, p.move[0], p.move[1])
    return Geometry(g)


class RoughenGeomP(ParamModel):
    src: Ref
    amount: NonNegFt = 1.0
    scale: PosFt = 6.0
    octaves: int = PField(3, ge=1, le=6)
    mode: Literal["noise", "cusps"] = "noise"
    period: PosFt = 4.0
    jitter: float = PField(0.3, ge=0, le=1)


def _cusp_ring(coords, amount, period, jitter, seed, closed=True):
    """Push each vertex outward (right of the direction of travel) by a row of scallops `period` feet
    long whose sharp horns stay on the original line: beach cusps along a waterline."""
    pts = np.asarray(coords, float)
    if closed:
        pts = pts[:-1]
    if len(pts) < 3 and closed:
        return coords
    seg = np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]) if closed else pts, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])[:len(pts)]
    if closed and seg.sum() > 0:                           # a whole number of scallops round a ring: no seam
        P = seg.sum()
        s = s * max(round(P / period), 1) * period / P
    if jitter:
        s = s + fbm_at(pts[:, 0], pts[:, 1], period * 3, seed) * jitter * period
    d = amount * np.abs(np.sin(np.pi * s / period)) ** 0.6
    nxt = np.roll(pts, -1, axis=0) if closed else np.vstack([pts[1:], pts[-1:]])
    prv = np.roll(pts, 1, axis=0) if closed else np.vstack([pts[:1], pts[:-1]])
    tang = nxt - prv
    norm = np.stack([tang[:, 1], -tang[:, 0]], axis=1)
    ln = np.linalg.norm(norm, axis=1, keepdims=True)
    norm = np.divide(norm, ln, out=np.zeros_like(norm), where=ln > 0)
    out = pts + norm * d[:, None]
    if not closed:
        out[0], out[-1] = pts[0], pts[-1]
    else:
        out = np.vstack([out, out[:1]])
    return out


def _rough_ring(coords, amount, scale, seed, closed=True):
    pts = np.asarray(coords, float)
    if closed:
        pts = pts[:-1]
    n = len(pts)
    if n < 3 and closed:
        return coords
    nxt = np.roll(pts, -1, axis=0) if closed else np.vstack([pts[1:], pts[-1:]])
    prv = np.roll(pts, 1, axis=0) if closed else np.vstack([pts[:1], pts[:-1]])
    tang = nxt - prv
    norm = np.stack([tang[:, 1], -tang[:, 0]], axis=1)
    ln = np.linalg.norm(norm, axis=1, keepdims=True)
    norm = np.divide(norm, ln, out=np.zeros_like(norm), where=ln > 0)
    d = fbm_at(pts[:, 0], pts[:, 1], scale, seed)
    out = pts + norm * (d[:, None] * amount * ROUGH_GAIN)
    if not closed:
        out[0], out[-1] = pts[0], pts[-1]
    if closed:
        out = np.vstack([out, out[:1]])
    return out


@op("roughen_geom", params=RoughenGeomP, inputs={"src": Geometry}, output=Geometry, group="1 geometry")
def roughen_geom(ctx, p, src):
    """Hand-drawn wobble: densify the outline and push each vertex along its normal by noise (amount feet, feature size `scale` feet). Use for caves, cliffs, ruins and shorelines. `mode: cusps` instead scallops the outline outward into crescents `period` feet long, up to `amount` feet deep, with sharp horns left on the original edge (`jitter` 0..1 makes them uneven): the beach cusps waves cut along a waterline. A line is pushed to the right of its direction."""
    from shapely.geometry.polygon import orient
    g = src.geom
    if p.amount == 0 or g.is_empty:
        return Geometry(g)
    if p.mode == "cusps":
        seg = max(min(p.period / 16, 0.25), 0.02)

        def ring(coords, closed=True):
            return _cusp_ring(coords, p.amount, p.period, p.jitter, ctx.seed, closed)
    else:
        seg = max(p.scale / 6, 0.25)

        def ring(coords, closed=True):
            return _rough_ring(coords, p.amount, p.scale, ctx.seed, closed=closed)
    g = shapely.segmentize(g, seg)

    def poly(pg):
        if p.mode != "cusps":
            return Polygon(ring(pg.exterior.coords), [ring(h.coords) for h in pg.interiors])
        pg = orient(pg, 1.0)                                       # outward = right of travel round a CCW ring
        out = Polygon(ring(pg.exterior.coords), [ring(h.coords) for h in pg.interiors]).buffer(0)
        # a scalloped hole can pinch off slivers at its corners: keep only the real holes
        keep = lambda q: Polygon(q.exterior, [h for h in q.interiors if Polygon(h).area > p.amount ** 2])
        return MultiPolygon([keep(q) for q in out.geoms]) if out.geom_type == "MultiPolygon" else keep(out)

    if isinstance(g, Polygon):
        out = polygonal(poly(g))
    elif isinstance(g, MultiPolygon):
        out = polygonal(MultiPolygon([poly(x) for x in g.geoms]))
    elif isinstance(g, LineString):
        out = LineString(ring(g.coords, closed=False))
    elif isinstance(g, MultiLineString):
        out = MultiLineString([ring(x.coords, closed=False) for x in g.geoms])
    else:
        raise RecipeError(f"roughen_geom cannot handle {g.geom_type}")
    return Geometry(out)


class TraceP(ParamModel):
    src: Ref
    level: float = PField(0.5, gt=0, lt=1)
    simplify: NonNegFt = 0.15
    min_area: NonNegFt = 1.0


@op("trace", params=TraceP, inputs={"src": Mask}, output=Geometry, group="1 geometry")
def trace(ctx, p, src):
    """Mask → polygons (marching squares at `level`), simplified by `simplify` feet; drops pieces under `min_area` ft². Lets a noise-made region be inked, dashed or walled like a drawn shape."""
    import contourpy
    data = np.pad(src.data, 1)
    gen = contourpy.contour_generator(z=data, fill_type="OuterOffset")
    polys, offs = gen.filled(p.level, 2.0)
    out = []
    s = ctx.frame.scale
    for pts, off in zip(polys, offs):
        rings = [(pts[off[i]:off[i + 1]] - 1 + 0.5) / s for i in range(len(off) - 1)]
        rings = [r for r in rings if len(r) >= 4]
        if rings:
            out.append(polygonal(Polygon(rings[0], rings[1:])))
    g = polygonal(shapely.unary_union(out)) if out else Polygon()
    if p.simplify:
        g = polygonal(g.simplify(p.simplify))
    parts = [x for x in getattr(g, "geoms", [g]) if x.area >= p.min_area]
    return Geometry(polygonal(shapely.unary_union(parts)) if parts else Polygon())
