"""Mask ops (T9, T10): rasterize and GIMP-style selection edits."""
from __future__ import annotations

from typing import Literal

import numpy as np
from PIL import Image as PImage, ImageDraw
from pydantic import Field as PField
from scipy import ndimage
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon

from ..layers import Geometry, Mask
from ..noise import fbm
from ..registry import ParamModel, op
from .common import NonNegFt, PosFt, Ref, signed_distance, soft_step


def polygons_of(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, MultiPolygon):
        return list(g.geoms)
    if hasattr(g, "geoms"):
        out = []
        for x in g.geoms:
            out.extend(polygons_of(x))
        return out
    return []


class Patch:
    """Coverage for a sub-rectangle of the frame: alpha (h, w) placed at (y0, x0)."""
    __slots__ = ("alpha", "y0", "x0")

    def __init__(self, alpha, y0, x0):
        self.alpha, self.y0, self.x0 = alpha, y0, x0

    @property
    def slices(self):
        h, w = self.alpha.shape
        return slice(self.y0, self.y0 + h), slice(self.x0, self.x0 + w)


def _lineish(g):
    if isinstance(g, (LineString, MultiLineString)):
        return True
    return hasattr(g, "geoms") and any(isinstance(x, (LineString, MultiLineString)) for x in g.geoms)


def rasterize_patch(frame, g, line_width_ft: float = 0.5) -> Patch | None:
    """Antialiased coverage of a geometry, rendered only over its bounding box."""
    if g.is_empty:
        return None
    if _lineish(g):
        g = g.buffer(line_width_ft / 2, quad_segs=8)
        if g.is_empty:
            return None
    H, W = frame.shape
    s = frame.scale
    minx, miny, maxx, maxy = g.bounds
    x0 = max(int(np.floor(minx * s)) - 2, 0)
    y0 = max(int(np.floor(miny * s)) - 2, 0)
    x1 = min(int(np.ceil(maxx * s)) + 2, W)
    y1 = min(int(np.ceil(maxy * s)) + 2, H)
    if x1 <= x0 or y1 <= y0:
        return None
    w, h = x1 - x0, y1 - y0
    aa = 4 if h * w <= 2_000_000 else 2
    img = PImage.new("L", (w * aa, h * aa), 0)
    d = ImageDraw.Draw(img)
    sa = s * aa

    def ring(coords):
        return [((x * s - x0) * aa - 0.5, (y * s - y0) * aa - 0.5) for x, y in coords]

    for pg in polygons_of(g):
        d.polygon(ring(pg.exterior.coords), fill=255)
        for hole in pg.interiors:
            d.polygon(ring(hole.coords), fill=0)
    a = np.asarray(img, np.float32).reshape(h, aa, w, aa).mean(axis=(1, 3)) / 255.0
    return Patch(a.astype(np.float32), y0, x0)


def rasterize_geom(frame, g, line_width_ft: float = 0.5) -> np.ndarray:
    """Antialiased coverage of a geometry at the frame's working resolution."""
    out = np.zeros(frame.shape, np.float32)
    p = rasterize_patch(frame, g, line_width_ft)
    if p is not None:
        out[p.slices] = p.alpha
    return out


class RasterizeP(ParamModel):
    src: Ref
    line_width: PosFt = 0.5


@op("rasterize", params=RasterizeP, inputs={"src": Geometry}, output=Mask, group="2 masks")
def rasterize(ctx, p, src):
    """Geometry → antialiased Mask. Lines are drawn `line_width` feet wide."""
    return Mask(rasterize_geom(ctx.frame, src.geom, p.line_width))


class ByP(ParamModel):
    src: Ref
    by: NonNegFt


@op("grow", params=ByP, inputs={"src": Mask}, output=Mask, group="2 masks")
def grow(ctx, p, src):
    """Grow a selection by `by` feet (GIMP: Select → Grow)."""
    return Mask(soft_step(signed_distance(src.data), ctx.frame.px(p.by)))


@op("shrink", params=ByP, inputs={"src": Mask}, output=Mask, group="2 masks")
def shrink(ctx, p, src):
    """Shrink a selection by `by` feet (GIMP: Select → Shrink)."""
    return Mask(soft_step(signed_distance(src.data), -ctx.frame.px(p.by)))


class BlurP(ParamModel):
    src: Ref
    sigma: PosFt


@op("blur", params=BlurP, inputs={"src": Mask}, output=Mask, group="2 masks")
def blur(ctx, p, src):
    """Gaussian blur, sigma in feet (feathering)."""
    return Mask(ndimage.gaussian_filter(src.data, ctx.frame.px(p.sigma)).astype(np.float32))


class ThresholdP(ParamModel):
    src: Ref
    level: float = PField(0.5, ge=0, le=1)
    softness: float = PField(0.0, ge=0, le=0.5)


@op("threshold", params=ThresholdP, inputs={"src": Mask}, output=Mask, group="2 masks")
def threshold(ctx, p, src):
    """Hard (or `softness`-ramped) threshold of a mask."""
    if p.softness == 0:
        return Mask((src.data >= p.level).astype(np.float32))
    lo, hi = p.level - p.softness, p.level + p.softness
    return Mask(np.clip((src.data - lo) / (hi - lo), 0, 1).astype(np.float32))


class SrcP(ParamModel):
    src: Ref


@op("invert", params=SrcP, inputs={"src": Mask}, output=Mask, group="2 masks")
def invert(ctx, p, src):
    """1 − mask. (Any mask reference can also be inverted inline as `~name`.)"""
    return Mask(1.0 - src.data)


class BandP(ParamModel):
    src: Ref
    inner: NonNegFt = 0.0
    outer: PosFt
    side: Literal["outside", "inside", "both"] = "outside"


@op("band", params=BandP, inputs={"src": Mask}, output=Mask, group="2 masks")
def band(ctx, p, src):
    """Ring between `inner` and `outer` feet from a mask's edge, outside, inside or both sides (e.g. a hatching band beyond the walls)."""
    sd = signed_distance(src.data)
    if p.side == "inside":
        sd = -sd
    elif p.side == "both":
        sd = np.abs(sd)
    i, o = ctx.frame.px(p.inner), ctx.frame.px(p.outer)
    a = np.clip(0.5 - (sd - o), 0, 1) * np.clip(0.5 + (sd - i), 0, 1)
    return Mask(a.astype(np.float32))


class CombineP(ParamModel):
    of: list[Ref] = PField(min_length=1)
    mode: Literal["max", "min", "mul", "add", "sub"] = "max"


@op("combine", params=CombineP, inputs={"of": Mask}, output=Mask, group="2 masks")
def combine(ctx, p, of):
    """Combine masks: max (union), min (intersection), mul, add, sub (first minus the rest)."""
    a = of[0].data.copy()
    for m in of[1:]:
        b = m.data
        a = {"max": np.maximum, "min": np.minimum, "mul": np.multiply,
             "add": lambda x, y: np.clip(x + y, 0, 1), "sub": lambda x, y: np.clip(x - y, 0, 1)}[p.mode](a, b)
    return Mask(a.astype(np.float32))


class RoughenP(ParamModel):
    src: Ref
    amount: NonNegFt = 1.0
    scale: PosFt = 5.0
    octaves: int = PField(3, ge=1, le=6)


@op("roughen", params=RoughenP, inputs={"src": Mask}, output=Mask, group="2 masks")
def roughen(ctx, p, src):
    """Raster edge wobble: displace the mask edge by noise (amount feet, feature size `scale` feet)."""
    sd = signed_distance(src.data)
    n = fbm(ctx.frame.shape, ctx.frame.px(p.scale), ctx.seed, p.octaves)
    return Mask(soft_step(sd + n * 2.0 * ctx.frame.px(p.amount)))
