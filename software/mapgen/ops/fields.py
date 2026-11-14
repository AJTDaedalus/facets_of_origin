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


class CellsP(ParamModel):
    scale: PosFt = 3.0
    jitter: float = PField(0.9, ge=0, le=1)
    metric: Literal["edge", "center"] = "edge"


@op("cells", params=CellsP, output=Field, group="3 fields")
def cells(ctx, p):
    """Cellular (Worley) noise: random points about `scale` feet apart (`jitter` 0 is a regular grid), each pixel's distance in feet to the nearest cell border (`metric: edge`, half the gap between the nearest two points) or to its cell's point (`center`). Threshold small edge values into a net of thin lines: foam lace, cracked mud, scales, cobbles."""
    from scipy.spatial import cKDTree
    fr = ctx.frame
    h, w = fr.shape
    s = fr.px(p.scale)
    nx, ny = int(np.ceil(w / s)) + 3, int(np.ceil(h / s)) + 3            # one spare ring of cells round the map
    gy, gx = np.mgrid[-1:ny - 1, -1:nx - 1].astype(np.float64)
    off = ctx.rng.uniform(-0.5, 0.5, size=(2,) + gx.shape) * p.jitter
    pts = np.stack([(gx + 0.5 + off[0]).ravel() * s, (gy + 0.5 + off[1]).ravel() * s], axis=1)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float64)
    q = np.stack([xs.ravel() + 0.5, ys.ravel() + 0.5], axis=1)
    d, _ = cKDTree(pts).query(q, k=2)
    out = (d[:, 1] - d[:, 0]) / 2 if p.metric == "edge" else d[:, 0]
    return Field((out / fr.scale).reshape(h, w).astype(np.float32))


class FacingP(ParamModel):
    src: Ref
    toward: Point = [0.6, 0.8]
    lo: float = PField(0.2, ge=-1, le=1)
    hi: float = PField(0.7, ge=-1, le=1)
    steep: PosFt | None = None


@op("facing", params=FacingP, inputs={"src": Field}, output=Mask, group="3 fields")
def facing(ctx, p, src):
    """Treat a field as height and select the slopes that face `toward` [dx, dy] (default south-east, the shadow side under north-west light): 0 where the downhill direction's cosine with `toward` is below `lo`, 1 above `hi`. `steep` (height per foot) also fades out gentle slopes. Clip ripple or crest strokes to it so only their shadowed sides are inked."""
    gy, gx = np.gradient(src.data.astype(np.float64))
    gx, gy = gx * ctx.frame.scale, gy * ctx.frame.scale                  # height per foot
    mag = np.hypot(gx, gy)
    t = np.asarray(p.toward, float)
    t = t / (np.linalg.norm(t) or 1.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        cos = np.where(mag > 1e-12, -(gx * t[0] + gy * t[1]) / mag, -2.0)
    if p.hi <= p.lo:
        m = (cos >= p.lo).astype(np.float64)
    else:
        m = np.clip((cos - p.lo) / (p.hi - p.lo), 0, 1)
    m[mag <= 1e-12] = 0
    if p.steep:
        m *= np.clip(mag / p.steep, 0, 1)
    return Mask(m.astype(np.float32))


class WarpP(ParamModel):
    src: Ref
    amount: PosFt = 2.0
    scale: PosFt = 8.0
    octaves: int = PField(3, ge=1, le=6)
    drift: Point = [0.0, 0.0]
    iterations: int = PField(1, ge=1, le=6)
    curl: bool = False


@op("warp", params=WarpP, inputs={"src": (Field, Mask)}, output="same", group="3 fields")
def warp(ctx, p, src):
    """Domain warp: drag a field or mask through a noise flow, each pixel moved up to `amount` feet by noise with features `scale` feet across; `drift` [dx, dy] (feet) adds a steady push, so shapes smear downwind. `iterations` > 1 warps the warp (nested domain warping: each pass uses fresh noise), which folds shapes into filaments. `curl: true` instead follows the curl of the noise, a swirling flow that neither bunches nor thins, traced in `iterations` steps along its streamlines, so shapes curl into eddies like smoke. Smooth (blurred) inputs swirl best. Returns the same kind of layer it was given."""
    from scipy import ndimage
    h, w = ctx.frame.shape
    a = ctx.frame.px(p.amount)
    sc = ctx.frame.px(p.scale)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    px, py = xs.copy(), ys.copy()
    if p.curl:
        n = fbm((h, w), sc, ctx.seed, octaves=p.octaves)
        gy, gx = np.gradient(ndimage.gaussian_filter(n, max(sc / 16, 0.5)))
        vx, vy = gy, -gx                                   # curl of a scalar potential: divergence-free
        vmax = float(np.percentile(np.hypot(vx, vy), 99)) or 1.0
        step = a / p.iterations / vmax
        for _ in range(p.iterations):                      # trace each sample back along the streamline
            px -= ndimage.map_coordinates(vx, [py, px], order=1, mode="nearest") * step
            py -= ndimage.map_coordinates(vy, [py, px], order=1, mode="nearest") * step
    else:
        for k in range(p.iterations):
            seed = ctx.seed if k == 0 else (ctx.seed * 31 + k * 7919) & 0x7FFFFFFF
            dx = fbm((h, w), sc, seed, octaves=p.octaves) * a
            dy = fbm((h, w), sc, seed ^ 0x5F3759DF, octaves=p.octaves) * a
            if k:                                          # nested: the new offset is read at the warped point
                dx = ndimage.map_coordinates(dx, [py, px], order=1, mode="nearest")
                dy = ndimage.map_coordinates(dy, [py, px], order=1, mode="nearest")
            px -= dx
            py -= dy
    # sampling upstream of the drift pushes the pattern downstream
    px -= ctx.frame.px(p.drift[0])
    py -= ctx.frame.px(p.drift[1])
    out = ndimage.map_coordinates(src.data, [py, px], order=1, mode="nearest").astype(np.float32)
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
