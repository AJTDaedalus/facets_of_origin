"""Geometry ops (T7, T8): shapes and booleans in feet."""
from __future__ import annotations

from typing import Literal

import numpy as np
import shapely
from pydantic import Field as PField
from shapely import affinity
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point as SPoint, Polygon, box

from ..layers import Geometry
from ..noise import fbm_at
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import NonNegFt, Point, PosFt, Ref, polygonal

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


class RoughenGeomP(ParamModel):
    src: Ref
    amount: NonNegFt = 1.0
    scale: PosFt = 6.0
    octaves: int = PField(3, ge=1, le=6)


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
    out = pts + norm * (d[:, None] * amount)
    if not closed:
        out[0], out[-1] = pts[0], pts[-1]
    if closed:
        out = np.vstack([out, out[:1]])
    return out


@op("roughen_geom", params=RoughenGeomP, inputs={"src": Geometry}, output=Geometry, group="1 geometry")
def roughen_geom(ctx, p, src):
    """Hand-drawn wobble: densify the outline and push each vertex along its normal by noise (amount feet, feature size `scale` feet). Use for caves, cliffs, ruins and shorelines."""
    g = src.geom
    if p.amount == 0 or g.is_empty:
        return Geometry(g)
    seg = max(p.scale / 6, 0.25)
    g = shapely.segmentize(g, seg)

    def poly(pg):
        ext = _rough_ring(pg.exterior.coords, p.amount, p.scale, ctx.seed)
        holes = [_rough_ring(h.coords, p.amount, p.scale, ctx.seed) for h in pg.interiors]
        return Polygon(ext, holes)

    if isinstance(g, Polygon):
        out = polygonal(poly(g))
    elif isinstance(g, MultiPolygon):
        out = polygonal(MultiPolygon([poly(x) for x in g.geoms]))
    elif isinstance(g, LineString):
        out = LineString(_rough_ring(g.coords, p.amount, p.scale, ctx.seed, closed=False))
    elif isinstance(g, MultiLineString):
        out = MultiLineString([_rough_ring(x.coords, p.amount, p.scale, ctx.seed, closed=False) for x in g.geoms])
    else:
        raise RecipeError(f"roughen_geom cannot handle {g.geom_type}")
    return Geometry(out)
