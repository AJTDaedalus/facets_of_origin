"""Field ops (T11, T12): noise, gradients, distances, remapping."""
from __future__ import annotations

from typing import Literal

import numpy as np
from pydantic import Field as PField, model_validator

from ..layers import Field, Mask
from ..noise import fbm
from ..registry import ParamModel, op
from .common import Point, PosFt, Ref, signed_distance


class NoiseP(ParamModel):
    scale: PosFt = 10.0
    kind: Literal["fbm", "ridged", "billow"] = "fbm"
    octaves: int = PField(4, ge=1, le=8)
    persistence: float = PField(0.5, gt=0, le=1)
    lacunarity: float = PField(2.0, ge=1.2, le=4)
    stretch: float = PField(1.0, ge=1.0, le=12)
    angle: float = 0.0


def directional(shape, scale_px, seed, stretch=1.0, angle=0.0, **kw) -> np.ndarray:
    """fbm whose features run `stretch` times longer along `angle` (degrees, 0 = east, 90 = south):
    isotropic noise on a squashed, rotated lattice, sampled back onto the pixel grid."""
    if stretch == 1.0:
        return fbm(shape, scale_px, seed, **kw)
    from scipy import ndimage
    h, w = shape
    th = np.deg2rad(angle)
    c, s_ = np.cos(th), np.sin(th)
    d = float(np.hypot(h, w))
    gu, gv = int(np.ceil(d / stretch)) + 4, int(np.ceil(d)) + 4      # lattice: u along the grain, v across
    lattice = fbm((gv, gu), scale_px, seed, **kw)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    xs -= w / 2
    ys -= h / 2
    u = (xs * c + ys * s_) / stretch + gu / 2
    v = (-xs * s_ + ys * c) + gv / 2
    return ndimage.map_coordinates(lattice, [v, u], order=1, mode="nearest").astype(np.float32)


@op("noise", params=NoiseP, output=Field, group="3 fields")
def noise(ctx, p):
    """Fractal gradient noise in −1..1. `scale` is the largest feature size in feet; kinds fbm (clouds), ridged (veins, ridges), billow (puffy). `stretch` > 1 draws the features that many times longer along `angle` (degrees, 0 = east, 90 = south): wind ripples, drifting mist, wood grain, strata."""
    return Field(directional(ctx.frame.shape, ctx.frame.px(p.scale), ctx.seed, p.stretch, p.angle,
                             octaves=p.octaves, persistence=p.persistence, lacunarity=p.lacunarity, kind=p.kind))


class WarpP(ParamModel):
    src: Ref
    amount: PosFt = 2.0
    scale: PosFt = 8.0
    octaves: int = PField(3, ge=1, le=6)
    drift: Point = [0.0, 0.0]


@op("warp", params=WarpP, inputs={"src": (Field, Mask)}, output="same", group="3 fields")
def warp(ctx, p, src):
    """Domain warp: drag a field or mask through a noise flow, each pixel moved up to `amount` feet by noise with features `scale` feet across; `drift` [dx, dy] (feet) adds a steady push, so shapes smear downwind. Curls mist into wisps, makes shorelines and stains swirl. Returns the same kind of layer it was given."""
    from scipy import ndimage
    h, w = ctx.frame.shape
    a = ctx.frame.px(p.amount)
    sc = ctx.frame.px(p.scale)
    dx = fbm((h, w), sc, ctx.seed, octaves=p.octaves) * a
    dy = fbm((h, w), sc, ctx.seed ^ 0x5F3759DF, octaves=p.octaves) * a
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    # sampling upstream of the drift pushes the pattern downstream
    xs -= dx + ctx.frame.px(p.drift[0])
    ys -= dy + ctx.frame.px(p.drift[1])
    out = ndimage.map_coordinates(src.data, [ys, xs], order=1, mode="nearest").astype(np.float32)
    return type(src)(out)


class GradientP(ParamModel):
    kind: Literal["linear", "radial"] = "linear"
    start: Point
    end: Point

    @model_validator(mode="after")
    def _distinct(self):
        if self.start == self.end:
            raise ValueError("start and end must differ")
        return self


def _grid_ft(frame):
    h, w = frame.shape
    xs = (np.arange(w, dtype=np.float32) + 0.5) / frame.scale
    ys = (np.arange(h, dtype=np.float32) + 0.5) / frame.scale
    return xs[None, :], ys[:, None]


@op("gradient", params=GradientP, output=Field, group="3 fields")
def gradient(ctx, p):
    """0 at `start`, 1 at `end` (linear), or by distance from `start` with `end` on the unit circle (radial); clamped to 0..1."""
    x, y = _grid_ft(ctx.frame)
    (x0, y0), (x1, y1) = p.start, p.end
    if p.kind == "linear":
        dx, dy = x1 - x0, y1 - y0
        t = ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)
    else:
        r = np.hypot(x1 - x0, y1 - y0)
        t = np.hypot(x - x0, y - y0) / r
    return Field(np.clip(t, 0, 1).astype(np.float32))


class DistanceP(ParamModel):
    src: Ref
    side: Literal["outside", "inside", "signed"] = "outside"


@op("distance", params=DistanceP, inputs={"src": Mask}, output=Field, group="3 fields")
def distance(ctx, p, src):
    """Distance in feet from a mask's edge: outside (0 inside), inside (0 outside), or signed (negative inside)."""
    sd = np.clip(signed_distance(src.data), -1e5, 1e5) / ctx.frame.scale
    if p.side == "outside":
        sd = np.maximum(sd, 0)
    elif p.side == "inside":
        sd = np.maximum(-sd, 0)
    return Field(sd.astype(np.float32))


class RemapP(ParamModel):
    src: Ref
    in_range: list[float] = PField([-1.0, 1.0], min_length=2, max_length=2)
    out_range: list[float] = PField([0.0, 1.0], min_length=2, max_length=2)
    curve: Literal["linear", "smooth", "pow"] = "linear"
    gamma: float = PField(1.0, gt=0)


@op("remap", params=RemapP, inputs={"src": Field}, output=Field, group="3 fields")
def remap(ctx, p, src):
    """Map in_range → out_range, clamped, with an optional smoothstep or power curve."""
    lo, hi = p.in_range
    t = np.clip((src.data - lo) / ((hi - lo) or 1e-9), 0, 1)
    if p.curve == "smooth":
        t = t * t * (3 - 2 * t)
    elif p.curve == "pow":
        t = t ** p.gamma
    a, b = p.out_range
    return Field((a + t * (b - a)).astype(np.float32))


class F2MP(ParamModel):
    src: Ref
    lo: float = 0.0
    hi: float = 0.0


@op("field_to_mask", params=F2MP, inputs={"src": Field}, output=Mask, group="3 fields")
def field_to_mask(ctx, p, src):
    """Mask = 0 below `lo`, 1 above `hi`, ramped between (lo == hi gives a hard cut)."""
    if p.hi <= p.lo:
        return Mask((src.data >= p.lo).astype(np.float32))
    return Mask(np.clip((src.data - p.lo) / (p.hi - p.lo), 0, 1).astype(np.float32))


class MixP(ParamModel):
    of: list[Ref] = PField(min_length=1)
    weights: list[float] | None = None
    mode: Literal["sum", "max", "min", "mul"] = "sum"


@op("mix", params=MixP, inputs={"of": (Field, Mask)}, output=Field, group="3 fields")
def mix(ctx, p, of):
    """Weighted sum (or max/min/product) of fields or masks → Field."""
    w = p.weights or [1.0] * len(of)
    if len(w) != len(of):
        from ..recipe import RecipeError
        raise RecipeError("mix: weights must match 'of'")
    arrs = [x.data * wi for x, wi in zip(of, w)]
    if p.mode == "sum":
        out = np.sum(arrs, axis=0)
    elif p.mode == "max":
        out = np.max(arrs, axis=0)
    elif p.mode == "min":
        out = np.min(arrs, axis=0)
    else:
        out = np.prod(arrs, axis=0)
    return Field(out.astype(np.float32))
