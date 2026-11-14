"""Paint ops (T13, T17, T18): canvas, fill, stroke, shadow, occlusion, hatch, paper."""
from __future__ import annotations

from typing import Any, Literal

import numpy as np
import shapely
from pydantic import Field as PField, model_validator
from scipy import ndimage
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon
from shapely.ops import substring

from ..color import composite_inplace, resolve_color
from ..layers import Geometry, Image, Mask
from ..noise import fbm
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import NonNegFt, Point, PosFt, Ref, Unit, signed_distance
from .geometry import _rough_ring
from .masks import rasterize_geom, rasterize_patch
from .materials import hatch_alpha, render_material

Blend = Literal["normal", "multiply", "screen", "overlay", "darken", "lighten"]


def mask_or_ones(ctx, m):
    return m.data if m is not None else np.ones(ctx.frame.shape, np.float32)


class CanvasP(ParamModel):
    color: Any = None
    material: str | None = None


@op("canvas", params=CanvasP, output=Image, group="4 paint")
def canvas(ctx, p):
    """A new opaque image filled with a colour or material. Name it `canvas` for the final map."""
    img = np.zeros(ctx.frame.shape + (4,), np.float32)
    img[..., 3] = 1
    if p.material:
        img[..., :3] = render_material(ctx, p.material, np.ones(ctx.frame.shape, np.float32), ctx.seed)
    else:
        img[..., :3] = resolve_color(ctx.style, p.color if p.color is not None else "#ffffff")[:3]
    return Image(img)


class FillP(ParamModel):
    into: Ref = "canvas"
    mask: Ref | None = None
    color: Any = None
    material: str | None = None
    opacity: Unit = 1.0
    blend: Blend = "normal"


@op("fill", params=FillP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def fill(ctx, p, into, mask=None):
    """Paint a colour or material through a mask (default: everywhere), with opacity and a blend mode."""
    if p.color is None and p.material is None:
        raise RecipeError("fill needs a color or material")
    m = mask_or_ones(ctx, mask)
    if p.material:
        src = render_material(ctx, p.material, m, ctx.seed)
        alpha = m * p.opacity
    else:
        c = resolve_color(ctx.style, p.color)
        src, alpha = c[:3], m * p.opacity * c[3]
    composite_inplace(into.data, src, alpha.astype(np.float32), p.blend)


class StrokeP(ParamModel):
    into: Ref = "canvas"
    src: Ref
    width: PosFt | None = None
    weight: str | None = None
    color: Any = "ink"
    opacity: Unit = 1.0
    roughness: NonNegFt = 0.0
    rough_scale: PosFt = 4.0
    double: NonNegFt = 0.0
    dash: list[float] | None = None
    jitter: Unit = 0.0
    side: Literal["center", "inside", "outside"] = "center"


def _width_ft(ctx, p) -> float:
    if p.width is not None:
        return p.width
    weights = {"heavy": 0.5, "medium": 0.3, "fine": 0.12, **(ctx.style.ink or {})}
    w = p.weight or "medium"
    if w not in weights:
        raise RecipeError(f"unknown ink weight {w!r} (have {', '.join(weights)})")
    # style weights are in feet; on a mile-scale map a "heavy" line would be half a mile wide
    scale = 0.25 if getattr(ctx.frame, "unit", "ft") == "mi" else 1.0
    return float(weights[w]) * scale


def lines_of(g):
    if g.is_empty:
        return []
    if isinstance(g, (Polygon, MultiPolygon)):
        b = g.boundary
        return list(b.geoms) if hasattr(b, "geoms") else [b]
    if isinstance(g, LineString):
        return [g]
    if isinstance(g, MultiLineString):
        return list(g.geoms)
    if hasattr(g, "geoms"):
        out = []
        for x in g.geoms:
            out.extend(lines_of(x))
        return out
    return []


def stroke_geometry_alpha(ctx, g, width_ft, roughness=0.0, rough_scale=4.0, double=0.0,
                          dash=None, side="center", seed=0, patch=False, jitter=0.0):
    rng = np.random.default_rng(seed + 991)
    lines = lines_of(g)
    if side != "center" and isinstance(g, (Polygon, MultiPolygon)):
        g2 = g.buffer(width_ft / 2 if side == "outside" else -width_ft / 2, join_style=2)
        lines = lines_of(g2)
    out = []
    for ln in lines:
        if roughness > 0:
            ln = shapely.segmentize(ln, max(rough_scale / 6, 0.2))
            closed = ln.is_ring
            ln = LineString(_rough_ring(ln.coords, roughness, rough_scale, seed, closed=closed))
        variants = [ln]
        if double > 0:
            variants = [ln.offset_curve(double / 2), ln.offset_curve(-double / 2)]
        for v in variants:
            if v.is_empty:
                continue
            if dash:
                pattern = list(dash) if len(dash) % 2 == 0 else list(dash) * 2
                pos, L, k = 0.0, v.length, 0
                while pos < L:
                    on, off = pattern[k % len(pattern)], pattern[(k + 1) % len(pattern)]
                    if jitter:
                        on *= 1 + rng.uniform(-jitter, jitter)
                        off *= 1 + rng.uniform(-jitter, jitter)
                    wmul = 1 + rng.uniform(-jitter, jitter) * 0.8 if jitter else 1.0
                    out.append((substring(v, pos, min(pos + on, L)), wmul))
                    pos += on + off
                    k += 2
            else:
                out.append((v, 1.0))
    if not out:
        return None if patch else np.zeros(ctx.frame.shape, np.float32)
    cap = 1 if (not dash or jitter) else 2
    pieces = [(o, wm) for o, wm in out if o.length > 0]
    if all(wm == 1.0 for _, wm in pieces):
        lines = [o for o, _ in pieces]
        geom = shapely.MultiLineString(lines).buffer(width_ft / 2, cap_style=cap, quad_segs=8) if lines else Polygon()
    else:
        geom = shapely.unary_union([o.buffer(width_ft * wm / 2, cap_style=cap, quad_segs=8) for o, wm in pieces])
    if patch:
        return rasterize_patch(ctx.frame, geom)
    return rasterize_geom(ctx.frame, geom)


@op("stroke", params=StrokeP, inputs={"into": Image, "src": (Mask, Geometry)}, group="4 paint")
def stroke(ctx, p, into, src):
    """Ink a line along a mask's edge or a geometry's outline: width in feet or a style `weight` (heavy/medium/fine), `roughness` wobble, `double` lines `double` feet apart, `dash: [on, off, ...]` (geometry only; `jitter` 0..1 randomises dash lengths and widths for a hand-inked look), `side`."""
    w = _width_ft(ctx, p)
    fr = ctx.frame
    if isinstance(src, Geometry):
        a = stroke_geometry_alpha(ctx, src.geom, w, p.roughness, p.rough_scale, p.double, p.dash, p.side, ctx.seed,
                                  jitter=p.jitter)
    else:
        if p.dash:
            raise RecipeError("dash needs a Geometry source, not a Mask")
        sd = signed_distance(src.data)
        if p.roughness > 0:
            sd = sd + fbm(fr.shape, fr.px(p.rough_scale), ctx.seed, 3) * 2.0 * fr.px(p.roughness)
        c = {"center": 0.0, "inside": -fr.px(w) / 2, "outside": fr.px(w) / 2}[p.side]
        hw = fr.px(w) / 2
        centers = [c] if p.double == 0 else [c - fr.px(p.double) / 2, c + fr.px(p.double) / 2]
        a = np.zeros(fr.shape, np.float32)
        for cc in centers:
            a = np.maximum(a, np.clip(hw + 0.5 - np.abs(sd - cc), 0, 1))
    col = resolve_color(ctx.style, p.color)
    composite_inplace(into.data, col[:3], (a * p.opacity * col[3]).astype(np.float32))


def _shift(a, dx_px, dy_px):
    return ndimage.shift(a, (dy_px, dx_px), order=1, mode="constant", cval=0.0)


class ShadowP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    mode: Literal["inner", "drop"] = "inner"
    width: PosFt = 2.0
    offset: Point = [0.0, 0.0]
    blur: NonNegFt = 0.5
    strength: Unit = 0.5
    color: Any = "shadow"
    outside_only: bool = True


@op("shadow", params=ShadowP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def shadow(ctx, p, into, mask):
    """Inner shadow (darkens inside the mask near its edge, over `width` feet; `offset` moves the light) or drop shadow (the mask's shape, offset and blurred, under/around it)."""
    fr = ctx.frame
    m = mask.data
    if p.mode == "inner":
        src = _shift(m, -fr.px(p.offset[0]), -fr.px(p.offset[1])) if any(p.offset) else m
        d = np.maximum(-signed_distance(src), 0)
        s = np.clip(1 - d / fr.px(p.width), 0, 1) ** 1.6
        if p.blur > 0:
            s = ndimage.gaussian_filter(s, fr.px(p.blur) / 2)
        a = s * m
    else:
        s = _shift(m, fr.px(p.offset[0]), fr.px(p.offset[1]))
        if p.blur > 0:
            s = ndimage.gaussian_filter(s, fr.px(p.blur))
        a = s * (1 - m) if p.outside_only else s
    col = resolve_color(ctx.style, p.color)
    composite_inplace(into.data, col[:3], (np.clip(a, 0, 1) * p.strength).astype(np.float32))


class OcclusionP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    falloff: PosFt = 1.5
    strength: Unit = 0.4
    color: Any = "shadow"


@op("occlusion", params=OcclusionP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def occlusion(ctx, p, into, mask):
    """Ambient occlusion: darken inside a walkable mask close to its edges (exponential falloff in feet)."""
    d = np.maximum(-signed_distance(mask.data), 0) / ctx.frame.scale
    a = p.strength * np.exp(-d / p.falloff) * mask.data
    col = resolve_color(ctx.style, p.color)
    composite_inplace(into.data, col[:3], a.astype(np.float32))


class HatchP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    spacing: PosFt = 2.0
    length: PosFt = 1.8
    width: PosFt = 0.1
    lines: int = PField(3, ge=1, le=6)
    angle: float | None = None
    angle_jitter: float = PField(180.0, ge=0, le=360)
    color: Any = "ink"
    opacity: Unit = 1.0


@op("hatch", params=HatchP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def hatch(ctx, p, into, mask):
    """Clusters of short parallel ink strokes inside a mask (typically a band just beyond the walls)."""
    fr = ctx.frame
    a = hatch_alpha(fr.shape, mask.data, fr.px(p.spacing), fr.px(p.length), fr.px(p.width),
                    p.lines, ctx.seed, p.angle, p.angle_jitter)
    col = resolve_color(ctx.style, p.color)
    composite_inplace(into.data, col[:3], (a * p.opacity).astype(np.float32))


class PaperP(ParamModel):
    into: Ref = "canvas"
    strength: Unit = 0.15
    scale: PosFt = 30.0
    grain: Unit = 0.3
    color: Any = None


@op("paper", params=PaperP, inputs={"into": Image}, group="4 paint")
def paper(ctx, p, into):
    """Parchment: low-frequency blotches plus fine grain, multiplied over the image (optionally tinted)."""
    fr = ctx.frame
    n = 0.65 * fbm(fr.shape, fr.px(p.scale), ctx.seed, 4) + 0.35 * fbm(fr.shape, fr.px(p.scale / 5), ctx.seed + 1, 3)
    g = np.random.default_rng(ctx.seed + 2).random(fr.shape).astype(np.float32) - 0.5
    g = ndimage.gaussian_filter(g, 0.7)
    factor = 1 - p.strength * (0.5 + 0.5 * n) * 0.6 - p.grain * p.strength * g * 1.5
    img = into.data
    img[..., :3] *= np.clip(factor, 0, 1.2)[..., None]
    if p.color is not None:
        c = resolve_color(ctx.style, p.color)
        composite_inplace(img, c[:3], np.full(fr.shape, p.strength, np.float32), "multiply")
    np.clip(img, 0, 1, out=img)


class VignetteP(ParamModel):
    into: Ref = "canvas"
    strength: Unit = 0.3
    start: Unit = 0.55


@op("vignette", params=VignetteP, inputs={"into": Image}, group="4 paint")
def vignette(ctx, p, into):
    """Darken towards the corners."""
    h, w = ctx.frame.shape
    y = (np.arange(h) + 0.5)[:, None] / h * 2 - 1
    x = (np.arange(w) + 0.5)[None, :] / w * 2 - 1
    r = np.sqrt(x * x + y * y) / np.sqrt(2)
    f = 1 - p.strength * np.clip((r - p.start) / (1 - p.start), 0, 1) ** 2
    into.data[..., :3] *= f[..., None].astype(np.float32)
