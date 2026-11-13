"""Terrain ops (Phase 2, R2-R3): isolines, thermal erosion, rivers."""
from __future__ import annotations

import heapq

import numpy as np
import shapely
from PIL import Image as PImage
from pydantic import Field as PField, model_validator
from shapely.geometry import LineString, MultiLineString

from ..layers import Field, Geometry
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import NonNegFt, PosFt, Ref


class IsolinesP(ParamModel):
    src: Ref
    levels: list[float] | None = None
    interval: float | None = PField(None, gt=0)
    simplify: NonNegFt = 0.0

    @model_validator(mode="after")
    def _need(self):
        if not self.levels and not self.interval:
            raise ValueError("give `levels` or `interval`")
        return self


@op("isolines", params=IsolinesP, inputs={"src": Field}, output=Geometry, group="3 fields")
def isolines(ctx, p, src):
    """Contour lines of a field at `levels` (or every `interval`) → line Geometry. For terrain contours, coastlines (sea level) and depth lines."""
    import contourpy
    z = src.data
    levels = p.levels or list(np.arange(np.ceil(z.min() / p.interval) * p.interval, z.max(), p.interval))
    gen = contourpy.contour_generator(z=z)
    s = ctx.frame.scale
    out = []
    for lv in levels:
        for seg in gen.lines(float(lv)):
            if len(seg) >= 2:
                out.append(LineString((seg + 0.5) / s))
    g = MultiLineString(out) if out else MultiLineString()
    if p.simplify and out:
        g = g.simplify(p.simplify)
    return Geometry(g)


class ErodeP(ParamModel):
    src: Ref
    iterations: int = PField(20, ge=0, le=500)
    talus: float = PField(0.004, ge=0)
    rate: float = PField(0.25, gt=0, le=0.5)


@op("erode", params=ErodeP, inputs={"src": Field}, output=Field, group="3 fields")
def erode(ctx, p, src):
    """Thermal erosion: material slides from steeper than `talus` (field units per pixel) to lower neighbours. Mass-conserving; softens noise into weathered terrain."""
    h = src.data.astype(np.float32).copy()
    for _ in range(p.iterations):
        d = h[:, :-1] - h[:, 1:]
        f = np.sign(d) * np.clip(np.abs(d) - p.talus, 0, None) * (p.rate / 2)
        h[:, :-1] -= f
        h[:, 1:] += f
        d = h[:-1, :] - h[1:, :]
        f = np.sign(d) * np.clip(np.abs(d) - p.talus, 0, None) * (p.rate / 2)
        h[:-1, :] -= f
        h[1:, :] += f
    return Field(h)


class RiversP(ParamModel):
    src: Ref
    sea_level: float = 0.0
    threshold: float = PField(0.01, gt=0, lt=1)
    resolution: int = PField(256, ge=32, le=1024)
    width: list[float] = PField([0.3, 2.0], min_length=2, max_length=2)
    line: bool = False
    smooth: int = PField(2, ge=0, le=5)


_NB = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def _flow(hc, sea):
    """Priority-flood fill, D8 receivers and accumulation on a coarse grid."""
    H, W = hc.shape
    filled = np.full((H, W), np.inf)
    done = np.zeros((H, W), bool)
    heap = []
    for y in range(H):
        for x in range(W):
            if y in (0, H - 1) or x in (0, W - 1) or hc[y, x] < sea:
                filled[y, x] = hc[y, x]
                heapq.heappush(heap, (hc[y, x], y, x))
                done[y, x] = True
    eps = 1e-6
    order = []
    recv = -np.ones((H, W, 2), int)
    while heap:
        z, y, x = heapq.heappop(heap)
        order.append((y, x))
        for dy, dx in _NB:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and not done[ny, nx]:
                done[ny, nx] = True
                filled[ny, nx] = max(hc[ny, nx], z + eps)
                recv[ny, nx] = (y, x)
                heapq.heappush(heap, (filled[ny, nx], ny, nx))
    acc = np.ones((H, W))
    for y, x in reversed(order):
        ry, rx = recv[y, x]
        if ry >= 0:
            acc[ry, rx] += acc[y, x]
    return filled, recv, acc / (H * W)


@op("rivers", params=RiversP, inputs={"src": Field}, output=Geometry, group="3 fields")
def rivers(ctx, p, src):
    """Rivers from a height field: fill depressions, route water downhill (D8), keep cells draining more than `threshold` of the map, trace them to the sea (height < `sea_level`) or the edge. Polygons tapered `width` [source, mouth] in map units, or centre lines with `line: true`."""
    fr = ctx.frame
    h = src.data
    H0, W0 = h.shape
    k = p.resolution / max(H0, W0)
    W, H = max(8, int(W0 * k)), max(8, int(H0 * k))
    hc = np.asarray(PImage.fromarray(h.astype(np.float32), mode="F").resize((W, H), PImage.BOX), np.float64)
    filled, recv, acc = _flow(hc, p.sea_level)
    river = (acc >= p.threshold) & (hc >= p.sea_level)
    cell_x, cell_y = fr.width_ft / W, fr.height_ft / H

    def pos(y, x):
        return ((x + 0.5) * cell_x, (y + 0.5) * cell_y)

    has_up = np.zeros((H, W), bool)
    ys, xs = np.nonzero(river)
    for y, x in zip(ys, xs):
        ry, rx = recv[y, x]
        if ry >= 0:
            has_up[ry, rx] = True
    visited = np.zeros((H, W), bool)
    paths = []
    sources = sorted((acc[y, x], y, x) for y, x in zip(ys, xs) if not has_up[y, x])
    for _, y, x in sources:
        pts, accs = [], []
        while True:
            pts.append(pos(y, x))
            accs.append(acc[y, x])
            if visited[y, x]:
                break
            visited[y, x] = True
            ry, rx = recv[y, x]
            if ry < 0 or hc[y, x] < p.sea_level:
                break
            y, x = ry, rx
            if hc[y, x] < p.sea_level:
                pts.append(pos(y, x))
                accs.append(acc[y, x])
                break
        if len(pts) >= 2:
            paths.append((pts, accs))
    if not paths:
        return Geometry(MultiLineString())
    from .geometry import _chaikin
    amax = max(max(a) for _, a in paths)
    if p.line:
        lines = [LineString(_chaikin(pts, p.smooth) if p.smooth else pts) for pts, _ in paths]
        return Geometry(MultiLineString(lines))
    w0, w1 = p.width
    pieces = []
    for pts, accs in paths:
        for (a, b), ac in zip(zip(pts[:-1], pts[1:]), accs[1:]):
            wv = w0 + (w1 - w0) * np.sqrt(ac / amax)
            pieces.append(LineString([a, b]).buffer(wv / 2, quad_segs=6))
    return Geometry(shapely.unary_union(pieces).simplify(min(cell_x, cell_y) * 0.15))
