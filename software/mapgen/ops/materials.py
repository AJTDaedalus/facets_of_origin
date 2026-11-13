"""Procedural materials (T14-T16). A material turns a coverage mask into an RGB field.

Materials live in the style under ``materials:`` as ``name: {type: ..., params}``.
Never sampled from imported textures: everything is generated here.
"""
from __future__ import annotations

from typing import Any, Literal

import numpy as np
from PIL import Image as PImage, ImageDraw
from pydantic import BaseModel, ConfigDict, Field as PField, ValidationError
from scipy import ndimage

from ..color import ramp, resolve_color
from ..noise import fbm, perlin
from ..recipe import RecipeError
from .common import signed_distance


class _M(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str


class FlatM(_M):
    color: Any


class RampNoiseM(_M):
    colors: list[Any] = PField(min_length=1)
    scale: float = PField(6.0, gt=0)
    octaves: int = PField(4, ge=1, le=8)
    contrast: float = PField(1.0, gt=0)
    kind: Literal["fbm", "ridged", "billow"] = "fbm"
    grain: float = PField(0.0, ge=0, le=0.5)


class DirtM(RampNoiseM):
    grain: float = PField(0.06, ge=0, le=0.5)
    speckle: float = PField(0.05, ge=0, le=1)
    speckle_color: Any = None


class HatchM(_M):
    color: Any = "#d8d0bf"
    ink: Any = "ink"
    spacing: float = PField(2.5, gt=0)
    length: float = PField(2.0, gt=0)
    width: float = PField(0.12, gt=0)
    lines: int = PField(3, ge=1, le=6)
    mottle: float = PField(0.06, ge=0, le=0.5)


class FlagstoneM(_M):
    colors: list[Any] = PField(min_length=1)
    size: float = PField(2.5, gt=0)
    pattern: Literal["voronoi", "ashlar"] = "voronoi"
    mortar: float = PField(0.15, ge=0)
    mortar_color: Any = "#4a463e"
    jitter: float = PField(0.8, ge=0, le=1)
    mottle: float = PField(0.3, ge=0, le=1)
    ratio: float = PField(1.6, gt=0)
    bevel: float = PField(0.18, ge=0, le=1)


class PlanksM(_M):
    colors: list[Any] = PField(min_length=1)
    width: float = PField(1.0, gt=0)
    length: float = PField(6.0, gt=0)
    angle: float = 0.0
    seam_color: Any = "#3a2a1a"
    seam: float = PField(0.06, ge=0)
    grain: float = PField(0.35, ge=0, le=1)


class CobbleM(_M):
    colors: list[Any] = PField(min_length=1)
    size: float = PField(1.0, gt=0)
    mortar_color: Any = "#5a564e"
    dome: float = PField(0.35, ge=0, le=1)


class GrassM(_M):
    colors: list[Any] = PField(min_length=1)
    scale: float = PField(4.0, gt=0)
    speckle: float = PField(0.08, ge=0, le=1)
    tufts: float = PField(0.25, ge=0, le=2)
    tuft_color: Any = None


class WaterM(_M):
    shallow: Any = "#a9cdd6"
    deep: Any = "#3f7189"
    depth: float = PField(5.0, gt=0)
    ripples: float = PField(1.5, ge=0)
    ripple_color: Any = "#e8f2f4"
    grain: float = PField(0.03, ge=0, le=0.5)


MODELS = {"flat": FlatM, "ramp_noise": RampNoiseM, "dirt": DirtM, "bedrock_hatch": HatchM,
          "flagstone": FlagstoneM, "planks": PlanksM, "cobble": CobbleM, "grass": GrassM,
          "water": WaterM}


def _spec(name: str, raw: dict):
    t = raw.get("type")
    if t not in MODELS:
        raise RecipeError(f"material {name!r}: unknown type {t!r} (have: {', '.join(MODELS)})")
    try:
        return MODELS[t](**raw)
    except ValidationError as e:
        msg = "; ".join(f"{'.'.join(map(str, er['loc']))}: {er['msg']}" for er in e.errors())
        raise RecipeError(f"material {name!r}: {msg}") from None


def _cols(style, cs):
    return [resolve_color(style, c) for c in cs]


def _hash_tones(n: int, seed: int) -> np.ndarray:
    return np.random.default_rng(seed).random(n).astype(np.float32)


def cells(shape, size_px: float, seed: int, jitter: float = 0.8):
    """Jittered-grid Voronoi: (cell ids, F1, F2) in pixels."""
    h, w = shape
    s = float(size_px)
    gh, gw = int(np.ceil(h / s)) + 3, int(np.ceil(w / s)) + 3
    rng = np.random.default_rng(seed)
    jx = rng.uniform(-jitter / 2, jitter / 2, (gh, gw)).astype(np.float32)
    jy = rng.uniform(-jitter / 2, jitter / 2, (gh, gw)).astype(np.float32)
    yy = (np.arange(h, dtype=np.float32) + 0.5)[:, None]
    xx = (np.arange(w, dtype=np.float32) + 0.5)[None, :]
    ci = (np.floor(yy / s).astype(np.int32) + 1)
    cj = (np.floor(xx / s).astype(np.int32) + 1)
    f1 = np.full((h, w), np.inf, np.float32)
    f2 = np.full((h, w), np.inf, np.float32)
    ids = np.zeros((h, w), np.int32)
    for di in (-1, 0, 1):
        i = np.clip(ci + di, 0, gh - 1)
        for dj in (-1, 0, 1):
            j = np.clip(cj + dj, 0, gw - 1)
            sx = ((j - 1) + 0.5 + jx[i, j]) * s
            sy = ((i - 1) + 0.5 + jy[i, j]) * s
            d = np.hypot(xx - sx, yy - sy)
            closer = d < f1
            f2 = np.where(closer, f1, np.minimum(f2, d))
            ids = np.where(closer, i * gw + j, ids)
            f1 = np.where(closer, d, f1)
    return ids, f1, f2


def hatch_alpha(shape, region: np.ndarray, spacing_px, length_px, width_px, lines, seed,
                angle: float | None = None, angle_jitter: float = 180.0) -> np.ndarray:
    """Clusters of short parallel strokes (dungeon-map hatching) inside a region."""
    h, w = shape
    rng = np.random.default_rng(seed)
    img = PImage.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    s = float(spacing_px)
    lw = max(1, int(round(width_px)))
    for gy in np.arange(s / 2, h + s, s):
        for gx in np.arange(s / 2, w + s, s):
            cx = gx + rng.uniform(-0.45, 0.45) * s
            cy = gy + rng.uniform(-0.45, 0.45) * s
            iy, ix = int(cy), int(cx)
            if not (0 <= iy < h and 0 <= ix < w) or region[iy, ix] < 0.5:
                rng.random(3)
                continue
            base = angle if angle is not None else 0.0
            a = np.deg2rad(base + rng.uniform(-angle_jitter / 2, angle_jitter / 2))
            n = max(1, lines + int(rng.integers(-1, 2)))
            ux, uy = np.cos(a), np.sin(a)
            gap = length_px / (n + 0.5)
            for k in range(n):
                off = (k - (n - 1) / 2) * gap
                L = length_px * rng.uniform(0.7, 1.1) / 2
                px, py = cx - uy * off, cy + ux * off
                d.line([(px - ux * L, py - uy * L), (px + ux * L, py + uy * L)], fill=255, width=lw)
    a = np.asarray(img, np.float32) / 255.0
    return (a * np.clip(region, 0, 1)).astype(np.float32)


def add_grain(rgb: np.ndarray, amount: float, seed: int, sigma_px: float = 0.6) -> np.ndarray:
    """Fine per-pixel tonal grit (multiplicative), so no surface is digitally flat."""
    if amount <= 0:
        return rgb
    g = np.random.default_rng(seed).random(rgb.shape[:2]).astype(np.float32) - 0.5
    if sigma_px > 0:
        g = ndimage.gaussian_filter(g, sigma_px)
        g /= max(float(g.std()), 1e-6) * 3.5
    return np.clip(rgb * (1 + amount * 2 * g)[..., None], 0, 1).astype(np.float32)


def render_material(ctx, name: str, mask: np.ndarray, seed: int) -> np.ndarray:
    """RGB (h, w, 3) float32 for a style material over the frame."""
    raw = (ctx.style.materials or {}).get(name)
    if raw is None:
        raise RecipeError(f"unknown material {name!r}")
    m = _spec(name, raw)
    rgb = _render(ctx, name, m, mask, seed)
    return add_grain(rgb, getattr(m, "grain", 0.0), seed + 101, ctx.frame.px(0.04))


def _render(ctx, name, m, mask, seed):
    fr = ctx.frame
    shape = fr.shape
    st = ctx.style

    if m.type == "flat":
        return np.broadcast_to(resolve_color(st, m.color)[:3], shape + (3,)).astype(np.float32).copy()

    if m.type in ("ramp_noise", "dirt"):
        n = fbm(shape, fr.px(m.scale), seed, m.octaves, kind=m.kind)
        t = np.clip(0.5 + 0.5 * n * m.contrast, 0, 1)
        rgb = ramp(_cols(st, m.colors), t)
        if m.type == "dirt" and m.speckle > 0:
            rng = np.random.default_rng(seed + 1)
            dots = (rng.random(shape) < m.speckle * 0.15).astype(np.float32)
            dots = ndimage.gaussian_filter(dots, max(fr.px(0.08), 0.6)) * 3
            sc = resolve_color(st, m.speckle_color)[:3] if m.speckle_color else rgb.mean((0, 1)) * 0.6
            a = np.clip(dots, 0, 0.8)[..., None]
            rgb = rgb * (1 - a) + sc * a
        return rgb.astype(np.float32)

    if m.type == "bedrock_hatch":
        base = resolve_color(st, m.color)[:3]
        n = fbm(shape, fr.px(m.spacing * 4), seed, 3)
        rgb = np.broadcast_to(base, shape + (3,)) * (1 + m.mottle * n)[..., None]
        region = (mask > 0.01).astype(np.float32)
        a = hatch_alpha(shape, region, fr.px(m.spacing), fr.px(m.length), fr.px(m.width), m.lines, seed + 7)
        ink = resolve_color(st, m.ink)[:3]
        return (rgb * (1 - a[..., None]) + ink * a[..., None]).astype(np.float32)

    if m.type == "flagstone":
        s = fr.px(m.size)
        if m.pattern == "voronoi":
            ids, f1, f2 = cells(shape, s, seed, m.jitter)
            edge = (f2 - f1) / 2
        else:
            h, w = shape
            yy = (np.arange(h, dtype=np.float32) + 0.5)[:, None]
            xx = (np.arange(w, dtype=np.float32) + 0.5)[None, :]
            row = np.floor(yy / s).astype(np.int32)
            L = s * m.ratio
            off = (_hash_tones(int(row.max()) + 2, seed + 3)[row] * L)
            xr = xx + off
            col = np.floor(xr / L).astype(np.int32)
            ids = row * 100003 + col
            ey = np.minimum(yy - row * s, (row + 1) * s - yy)
            ex = np.minimum(xr - col * L, (col + 1) * L - xr)
            edge = np.minimum(np.broadcast_to(ey, ex.shape), ex)
        uniq, inv = np.unique(ids, return_inverse=True)
        tone = _hash_tones(len(uniq), seed + 1)[inv.reshape(ids.shape)]
        n = fbm(shape, s * 1.5, seed + 2, 3)
        t = np.clip(tone * (1 - m.mottle) + (0.5 + 0.5 * n) * m.mottle, 0, 1)
        rgb = ramp(_cols(st, m.colors), t)
        if m.bevel > 0:
            shade = 1 - m.bevel * np.clip(1 - edge / (s * 0.18), 0, 1)
            rgb = rgb * shade[..., None]
        mw = fr.px(m.mortar) / 2
        ma = np.clip(mw - edge + 0.5, 0, 1)[..., None]
        mc = resolve_color(st, m.mortar_color)[:3]
        return (rgb * (1 - ma) + mc * ma).astype(np.float32)

    if m.type == "cobble":
        s = fr.px(m.size)
        ids, f1, f2 = cells(shape, s, seed, 0.9)
        uniq, inv = np.unique(ids, return_inverse=True)
        tone = _hash_tones(len(uniq), seed + 1)[inv.reshape(ids.shape)]
        rgb = ramp(_cols(st, m.colors), tone)
        dome = 1 - m.dome * np.clip(f1 / (s * 0.65), 0, 1) ** 2
        rgb = rgb * dome[..., None]
        edge = (f2 - f1) / 2
        ma = np.clip(s * 0.09 - edge + 0.5, 0, 1)[..., None]
        mc = resolve_color(st, m.mortar_color)[:3]
        return (rgb * (1 - ma) + mc * ma).astype(np.float32)

    if m.type == "planks":
        h, w = shape
        a = np.deg2rad(m.angle)
        yy = (np.arange(h, dtype=np.float32) + 0.5)[:, None]
        xx = (np.arange(w, dtype=np.float32) + 0.5)[None, :]
        u = xx * np.cos(a) + yy * np.sin(a)
        v = -xx * np.sin(a) + yy * np.cos(a)
        W, L = fr.px(m.width), fr.px(m.length)
        vmin = float(v.min())
        row = np.floor((v - vmin) / W).astype(np.int32)
        nrows = int(row.max()) + 2
        off = _hash_tones(nrows, seed + 3)[row] * L
        ur = u + off
        col = np.floor(ur / L).astype(np.int32)
        cmin = int(col.min())
        ids = row * 100003 + (col - cmin)
        uniq, inv = np.unique(ids, return_inverse=True)
        tone = _hash_tones(len(uniq), seed + 1)[inv.reshape(ids.shape)]
        grain = perlin(ur / (L * 0.6), (v - vmin) / (W * 0.18), seed + 5)
        t = np.clip(tone * (1 - m.grain) + (0.5 + 0.5 * grain) * m.grain, 0, 1)
        rgb = ramp(_cols(st, m.colors), t)
        sw = max(fr.px(m.seam) / 2, 0.5)
        ev = np.minimum((v - vmin) - row * W, (row + 1) * W - (v - vmin))
        eu = np.minimum(ur - col * L, (col + 1) * L - ur)
        edge = np.minimum(ev, eu)
        sa = np.clip(sw - edge + 0.5, 0, 1)[..., None]
        sc = resolve_color(st, m.seam_color)[:3]
        return (rgb * (1 - sa) + sc * sa).astype(np.float32)

    if m.type == "grass":
        n = fbm(shape, fr.px(m.scale), seed, 5)
        n2 = fbm(shape, fr.px(m.scale / 6), seed + 9, 2)
        t = np.clip(0.5 + 0.45 * n + 0.15 * n2, 0, 1)
        cols = _cols(st, m.colors)
        rgb = ramp(cols, t)
        rng = np.random.default_rng(seed + 1)
        if m.speckle > 0:
            sp = (rng.random(shape) < m.speckle * 0.2).astype(np.float32)
            sp = ndimage.gaussian_filter(sp, max(fr.px(0.06), 0.5)) * 2.5
            rgb = rgb * (1 - 0.35 * np.clip(sp, 0, 1))[..., None]
        if m.tufts > 0:
            region = np.ones(shape, np.float32)
            ta = hatch_alpha(shape, region, fr.px(1.6 / m.tufts), fr.px(0.45), max(fr.px(0.05), 1),
                             3, seed + 4, angle=-75, angle_jitter=40)
            tc = resolve_color(st, m.tuft_color)[:3] if m.tuft_color else cols[0][:3] * 0.75
            rgb = rgb * (1 - 0.7 * ta[..., None]) + tc * 0.7 * ta[..., None]
        return rgb.astype(np.float32)

    if m.type == "water":
        sd = signed_distance(mask)
        d = np.maximum(-sd, 0) / fr.scale
        if not (mask < 0.5).any():
            d = np.full(shape, m.depth, np.float32)
        t = np.clip(d / m.depth, 0, 1) ** 0.8
        n = fbm(shape, fr.px(m.depth * 2), seed, 3)
        t = np.clip(t + 0.08 * n, 0, 1)
        rgb = ramp([resolve_color(st, m.shallow), resolve_color(st, m.deep)], t)
        if m.ripples > 0:
            wob = fbm(shape, fr.px(3.0), seed + 3, 2) * 0.35
            ph = (d / m.ripples + wob) % 1.0
            line = np.clip(1 - np.abs(ph - 0.5) * 2 / 0.12, 0, 1)
            near = np.clip(1 - d / (m.depth * 0.9), 0, 1) * (0.5 + 0.5 * fbm(shape, fr.px(6.0), seed + 4, 2) > 0.45)
            ra = (line * near * 0.55)[..., None]
            rc = resolve_color(st, m.ripple_color)[:3]
            rgb = rgb * (1 - ra) + rc * ra
        return rgb.astype(np.float32)

    raise RecipeError(f"material {name!r}: unhandled type {m.type}")
