"""Ink line-work (owner feedback 2026-11-13: "shading lines seem to be the biggest difference").

Published hand-inked maps carry their depth in strokes, not soft gradients:
  shade_lines - short strokes perpendicular to an edge (walls, cliffs, banks), longer in shadow
  cracks      - branching hairline cracks across a floor or rock surface
  stipple     - ink dots that thin out away from an edge (grit, rubble dust)

Lighting convention (the whole style uses it): light from the north-west, so shadows fall
south-east, i.e. `shadow: [0.6, 0.8]`. A sunken area (a floor inside walls) is shaded inside
its north and west edges; a raised mass (a forest, brush, a hill) is shaded inside its south
and east edges, which is `shadow: [-0.6, -0.8]` with `side: inside`.

Every op works on the mask's bounding box (plus a margin), not the full frame.
"""
from __future__ import annotations

from typing import Any, Literal

import numpy as np
from PIL import Image as PImage, ImageDraw
from pydantic import Field as PField

from ..color import composite_patch, resolve_color
from ..layers import Image, Mask
from ..registry import ParamModel, op
from .common import Point, PosFt, Ref, Unit, signed_distance
from .masks import Patch


def _crop(m: np.ndarray, margin_px: float, outside: bool = False):
    """(y0, x0, y1, x1) of the area the op needs, or None if there's nothing to do."""
    h, w = m.shape
    if outside:
        if (m >= 0.5).all():
            return None
    ys, xs = np.nonzero(m > 0.01)
    if not len(ys):
        return None
    mg = int(np.ceil(margin_px)) + 2
    return (max(ys.min() - mg, 0), max(xs.min() - mg, 0), min(ys.max() + 1 + mg, h), min(xs.max() + 1 + mg, w))


def _edges_px(mask: np.ndarray):
    """Contour polylines of a mask at 0.5, in pixel coordinates (x, y) of the array given."""
    import contourpy
    gen = contourpy.contour_generator(z=mask)
    return [seg for seg in gen.lines(0.5) if len(seg) >= 2]


def _resample(seg: np.ndarray, step: float, rng) -> np.ndarray:
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(seg, axis=0).T))]
    if d[-1] < step:
        return seg[:1]
    t = np.arange(rng.uniform(0, step), d[-1], step)
    return np.c_[np.interp(t, d, seg[:, 0]), np.interp(t, d, seg[:, 1])]


def _composite(ctx, into, alpha_sub: np.ndarray, box, color, opacity: float) -> None:
    y0, x0 = box[0], box[1]
    col = resolve_color(ctx.style, color)
    composite_patch(into.data, Patch((alpha_sub * opacity).astype(np.float32), y0, x0), col[:3])


class ShadeLinesP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    side: Literal["inside", "outside"] = "inside"
    length: PosFt = 2.0
    spacing: PosFt = 0.35
    width: PosFt = 0.06
    jitter: Unit = 0.5
    angle_jitter: float = PField(10.0, ge=0, le=60)
    shadow: Point | None = [0.6, 0.8]
    min_share: Unit = 0.3
    color: Any = "ink"
    opacity: Unit = 0.75


@op("shade_lines", params=ShadeLinesP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def shade_lines(ctx, p, into, mask):
    """Hatching along a mask's edge: short ink strokes perpendicular to the edge, every `spacing` feet, up to `length` feet long (randomised by `jitter`). `shadow` is the direction shadows fall (default south-east, light from the north-west): a stroke pointing along it is full length, one pointing against it shrinks to `min_share`. For a sunken area (a floor) use `side: inside` with the default; for a raised mass (forest, brush, hill) use `side: inside` with `shadow: [-0.6, -0.8]`; `side: outside` shades beyond an edge (cliffs, banks); `shadow: null` makes every edge full length."""
    fr = ctx.frame
    rng = ctx.rng
    box = _crop(mask.data, fr.px(p.length) + 2, outside=p.side == "outside")
    if box is None:
        return
    y0, x0, y1, x1 = box
    m = mask.data[y0:y1, x0:x1]
    sd = signed_distance(m)
    gy, gx = np.gradient(sd)
    h, w = m.shape
    img = PImage.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    lw = max(1, int(round(fr.px(p.width))))
    sh = None
    if p.shadow is not None:
        v = np.asarray(p.shadow, float)
        sh = v / (np.linalg.norm(v) or 1)
    for seg in _edges_px(m):
        for x, y in _resample(seg, fr.px(p.spacing), rng):
            ix, iy = min(max(int(x), 0), w - 1), min(max(int(y), 0), h - 1)
            n = np.array([gx[iy, ix], gy[iy, ix]])
            nn = np.linalg.norm(n)
            if nn < 1e-6:
                continue
            out = n / nn                                # outward normal (sd grows outward)
            dirv = -out if p.side == "inside" else out
            share = 1.0
            if sh is not None:
                share = p.min_share + (1 - p.min_share) * max(0.0, float(np.dot(dirv, sh)))
            a = np.deg2rad(rng.uniform(-p.angle_jitter, p.angle_jitter))
            ca, sa = np.cos(a), np.sin(a)
            dv = np.array([dirv[0] * ca - dirv[1] * sa, dirv[0] * sa + dirv[1] * ca])
            L = fr.px(p.length) * share * rng.uniform(1 - p.jitter, 1)
            if L < 1.0:
                continue
            d.line([(x, y), (x + dv[0] * L, y + dv[1] * L)], fill=255, width=lw)
    a = np.asarray(img, np.float32) / 255.0
    region = m if p.side == "inside" else (1.0 - m)
    _composite(ctx, into, a * region, box, p.color, p.opacity)


class CracksP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    density: float = PField(0.15, gt=0, le=4)
    length: PosFt = 3.0
    step: PosFt = 0.35
    wobble: float = PField(35.0, ge=0, le=90)
    branch: Unit = 0.25
    width: PosFt = 0.05
    color: Any = "ink"
    opacity: Unit = 0.5


@op("cracks", params=CracksP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def cracks(ctx, p, into, mask):
    """Branching hairline cracks inside a mask: `density` cracks per grid square, each a wandering line about `length` feet long (steps of `step` feet, turning up to `wobble` degrees), forking with chance `branch` over its length."""
    fr = ctx.frame
    rng = ctx.rng
    box = _crop(mask.data, 1)
    if box is None:
        return
    y0, x0, y1, x1 = box
    m = mask.data[y0:y1, x0:x1]
    h, w = m.shape
    inside = np.argwhere(m >= 0.5)
    if not len(inside):
        return
    area_sq = len(inside) / (fr.scale ** 2) / (fr.fps ** 2)
    n = int(round(p.density * area_sq))
    img = PImage.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    lw = max(1, int(round(fr.px(p.width))))
    step = fr.px(p.step)
    for _ in range(n):
        yy, xx = inside[int(rng.integers(len(inside)))]
        stack = [(float(xx), float(yy), rng.uniform(0, 2 * np.pi), fr.px(p.length) * rng.uniform(0.5, 1.2))]
        while stack:
            x, y, ang, left = stack.pop()
            while left > 0:
                ang += np.deg2rad(rng.uniform(-p.wobble, p.wobble))
                nx, ny = x + np.cos(ang) * step, y + np.sin(ang) * step
                if not (0 <= int(nx) < w and 0 <= int(ny) < h) or m[int(ny), int(nx)] < 0.5:
                    break
                d.line([(x, y), (nx, ny)], fill=255, width=lw)
                x, y, left = nx, ny, left - step
                if rng.random() < p.branch * step / max(fr.px(p.length), 1):
                    stack.append((x, y, ang + rng.choice([-1, 1]) * rng.uniform(0.5, 1.1), left * 0.5))
    a = np.asarray(img, np.float32) / 255.0
    _composite(ctx, into, a * m, box, p.color, p.opacity)


class StippleP(ParamModel):
    into: Ref = "canvas"
    mask: Ref
    density: float = PField(3.0, gt=0, le=60)
    size: PosFt = 0.08
    falloff: float | None = PField(2.5, gt=0)
    side: Literal["inside", "outside"] = "inside"
    color: Any = "ink"
    opacity: Unit = 0.6


@op("stipple", params=StippleP, inputs={"into": Image, "mask": Mask}, group="4 paint")
def stipple(ctx, p, into, mask):
    """Ink dots: `density` per square foot at the mask's edge, thinning linearly to nothing `falloff` feet away (or an even `density` everywhere with `falloff: null`). The count is density × the weighted area, so it doesn't depend on the map's size. Grit along walls, dust round rubble, texture on rock."""
    fr = ctx.frame
    rng = ctx.rng
    outside = p.side == "outside"
    box = _crop(mask.data, fr.px(p.falloff or 0) + 2, outside=outside) if not (outside and not p.falloff) \
        else (0, 0) + mask.data.shape
    if box is None:
        return
    y0, x0, y1, x1 = box
    m = mask.data[y0:y1, x0:x1]
    region = (m >= 0.5) if not outside else (m < 0.5)
    if p.falloff:
        sd = signed_distance(m) / fr.scale
        dist = np.maximum(-sd, 0) if not outside else np.maximum(sd, 0)
        weight = np.clip(1 - dist / p.falloff, 0, 1) * region
    else:
        weight = region.astype(np.float32)
    total = float(weight.sum())
    if total <= 0:
        return
    n = int(round(p.density * total / (fr.scale ** 2)))       # dots = density × weighted ft²
    if n <= 0:
        return
    flat = weight.ravel() / total
    idx = rng.choice(flat.size, size=n, replace=True, p=flat)
    ys, xs = np.divmod(idx, m.shape[1])
    img = PImage.new("L", (m.shape[1], m.shape[0]), 0)
    d = ImageDraw.Draw(img)
    r = max(fr.px(p.size) / 2, 0.6)
    for x, y in zip(xs, ys):
        rr = r * rng.uniform(0.6, 1.3)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
    a = np.asarray(img, np.float32) / 255.0
    _composite(ctx, into, a, box, p.color, p.opacity)
