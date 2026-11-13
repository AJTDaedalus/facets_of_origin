"""Town ops (Phase 2b): building lots along streets, gabled buildings."""
from __future__ import annotations

from typing import Any

import numpy as np
import shapely
from pydantic import Field as PField
from shapely import affinity
from shapely.geometry import LineString, Polygon, box

from ..color import composite_patch, resolve_color
from ..layers import Geometry, Image
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import PosFt, Ref, Unit, polygonal
from .masks import Patch, polygons_of, rasterize_patch
from .paint import lines_of, stroke_geometry_alpha


class FrontageP(ParamModel):
    roads: list[Ref] = PField(min_length=1)
    road_width: PosFt = 20.0
    setback: float = PField(3.0, ge=0)
    width: list[float] = PField([18.0, 34.0], min_length=2, max_length=2)
    depth: list[float] = PField([16.0, 28.0], min_length=2, max_length=2)
    gap: list[float] = PField([4.0, 14.0], min_length=2, max_length=2)
    fill: Unit = 0.85
    rotate_jitter: float = PField(0.0, ge=0, le=45)
    setback_jitter: float = PField(0.0, ge=0)
    l_shape: Unit = 0.0
    within: Ref | None = None
    avoid: Ref | None = None


@op("frontage", params=FrontageP, inputs={"roads": Geometry, "within": Geometry, "avoid": Geometry},
    output=Geometry, group="8 town")
def frontage(ctx, p, roads, within=None, avoid=None):
    """Building footprints along both sides of street lines: each faces its street, `setback` feet back from a `road_width` road, random `width`/`depth`/`gap` ranges; `fill` is the share of frontage built up; `rotate_jitter`/`setback_jitter` loosen the rows and `l_shape` adds cross-gabled wings. Stays clear of every road, `avoid`, and other lots, and inside `within`."""
    rng = ctx.rng
    road_lines = [l for r in roads for l in lines_of(r.geom)]
    keep_out = shapely.unary_union([l.buffer(p.road_width / 2 + 0.5) for l in road_lines])
    if avoid is not None:
        keep_out = keep_out.union(avoid.geom)
    area = within.geom if within is not None else box(0, 0, ctx.frame.width_ft, ctx.frame.height_ft)
    placed = []
    union = Polygon()
    for ln in road_lines:
        L = ln.length
        for side in (-1, 1):
            pos = rng.uniform(0, p.gap[1])
            while pos < L:
                w = rng.uniform(*p.width)
                d = rng.uniform(*p.depth)
                mid = min(pos + w / 2, L - 1e-6)
                c = np.array(ln.interpolate(mid).coords[0])
                a = np.array(ln.interpolate(max(mid - 1, 0)).coords[0])
                b = np.array(ln.interpolate(min(mid + 1, L)).coords[0])
                t = (b - a) / (np.linalg.norm(b - a) or 1)
                n = np.array([-t[1], t[0]]) * side
                sb = p.setback + (rng.uniform(0, p.setback_jitter) if p.setback_jitter else 0.0)
                base = c + n * (p.road_width / 2 + sb)
                rect = Polygon([base - t * w / 2, base + t * w / 2, base + t * w / 2 + n * d, base - t * w / 2 + n * d])
                parts = [rect]
                if p.l_shape and rng.random() < p.l_shape:
                    ww = w * rng.uniform(0.35, 0.5)
                    end = rng.choice([-1, 1])
                    wbase = base + t * end * (w / 2 - ww / 2) + n * d * 0.8
                    wing = Polygon([wbase - t * ww / 2, wbase + t * ww / 2, wbase + t * ww / 2 + n * d * 0.7,
                                    wbase - t * ww / 2 + n * d * 0.7])
                    parts.append(wing)
                if p.rotate_jitter:
                    ang = rng.uniform(-p.rotate_jitter, p.rotate_jitter)
                    ctr = rect.centroid
                    parts = [affinity.rotate(q, ang, origin=ctr) for q in parts]
                whole = shapely.unary_union(parts)
                if (rng.random() < p.fill and area.contains(whole) and not whole.intersects(keep_out)
                        and not whole.buffer(1.5).intersects(union)):
                    placed.extend(parts)
                    union = union.union(whole)
                pos += w + rng.uniform(*p.gap)
    return Geometry(shapely.GeometryCollection(placed) if placed else shapely.MultiPolygon())


class BuildingsP(ParamModel):
    into: Ref = "canvas"
    src: Ref
    roofs: list[Any] = ["#9b4a35", "#7e5a3f", "#6e6f7a", "#8a7a5c", "#a35f3c"]
    shade: Unit = 0.35
    shadow: Unit = 0.45
    ink: Any = "ink"
    ridge: bool = True


@op("buildings", params=BuildingsP, inputs={"into": Image, "src": Geometry}, group="8 town")
def buildings(ctx, p, into, src):
    """Draw building footprints as gabled roofs seen from above: a ridge along the long side, the south/east half shaded, a cast shadow and ink outline. Roof colours are picked per building from `roofs`."""
    polys = polygons_of(src.geom)
    if not polys:
        raise RecipeError("buildings needs polygon footprints (e.g. from frontage or rect)")
    rng = ctx.rng
    fr = ctx.frame
    inkc = resolve_color(ctx.style, p.ink)[:3]
    cols = [resolve_color(ctx.style, c) for c in p.roofs]
    from scipy import ndimage
    for pg in polys:
        off = max(min(pg.minimum_rotated_rectangle.exterior.length / 40, 3.0), 0.8)
        sh = affinity.translate(pg, off, off * 1.1)
        pat = rasterize_patch(fr, sh)
        if pat is not None:
            pat.alpha = ndimage.gaussian_filter(pat.alpha, max(fr.px(off * 0.3), 0.6))
            composite_patch(into.data, pat, (0, 0, 0), p.shadow)
        base = cols[int(rng.integers(len(cols)))][:3] * rng.uniform(0.9, 1.08)
        composite_patch(into.data, rasterize_patch(fr, pg), np.clip(base, 0, 1))
        mrr = list(pg.minimum_rotated_rectangle.exterior.coords)[:4]
        e1 = np.subtract(mrr[1], mrr[0])
        e2 = np.subtract(mrr[2], mrr[1])
        if np.linalg.norm(e1) >= np.linalg.norm(e2):
            r0 = (np.add(mrr[0], mrr[3])) / 2
            r1 = (np.add(mrr[1], mrr[2])) / 2
            half = Polygon([mrr[0], mrr[1], r1, r0]) if (np.add(mrr[0], mrr[1]) / 2)[1] > r0[1] else Polygon([r0, r1, mrr[2], mrr[3]])
        else:
            r0 = (np.add(mrr[0], mrr[1])) / 2
            r1 = (np.add(mrr[3], mrr[2])) / 2
            half = Polygon([mrr[1], mrr[2], r1, r0]) if (np.add(mrr[1], mrr[2]) / 2)[0] > r0[0] else Polygon([r0, r1, mrr[3], mrr[0]])
        half = half.intersection(pg)
        if not half.is_empty:
            composite_patch(into.data, rasterize_patch(fr, half), (0, 0, 0), p.shade)
        if p.ridge:
            composite_patch(into.data, stroke_geometry_alpha(ctx, LineString([r0, r1]), 0.5, patch=True), inkc, 0.8)
        composite_patch(into.data, stroke_geometry_alpha(ctx, pg, 0.8, patch=True), inkc)
    ctx.collector.legend.setdefault("building", "building")
