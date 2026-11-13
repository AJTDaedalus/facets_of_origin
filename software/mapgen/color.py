"""Colour resolution and compositing (premultiplied RGBA, float32)."""
from __future__ import annotations

import re

import numpy as np

from .recipe import RecipeError

_HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
FALLBACK = {"ink": "#2b2620", "shadow": "#000000", "white": "#ffffff", "black": "#000000"}


def resolve_color(style, c, _depth: int = 0) -> np.ndarray:
    """'#rgb', '#rrggbb', '#rrggbbaa', a palette name, or [r, g, b(, a)] in 0-255 → RGBA 0..1."""
    if _depth > 8:
        raise RecipeError(f"colour palette loop at {c!r}")
    if isinstance(c, (list, tuple)):
        if len(c) not in (3, 4):
            raise RecipeError(f"colour lists need 3 or 4 values: {c!r}")
        v = [float(x) / 255.0 for x in c] + ([1.0] if len(c) == 3 else [])
        return np.array(v, np.float32)
    if isinstance(c, str):
        m = _HEX.match(c)
        if m:
            h = m.group(1)
            if len(h) == 3:
                h = "".join(ch * 2 for ch in h)
            vals = [int(h[i:i + 2], 16) / 255.0 for i in range(0, len(h), 2)]
            if len(vals) == 3:
                vals.append(1.0)
            return np.array(vals, np.float32)
        palette = getattr(style, "palette", {}) or {}
        if c in palette:
            return resolve_color(style, palette[c], _depth + 1)
        if c in FALLBACK:
            return resolve_color(style, FALLBACK[c], _depth + 1)
    raise RecipeError(f"unknown colour {c!r} (use #hex, [r,g,b] or a palette name)")


def ramp(colors: list[np.ndarray], t: np.ndarray) -> np.ndarray:
    """Piecewise-linear colour ramp; t in 0..1 → (h, w, 3)."""
    cs = np.stack([c[:3] for c in colors]).astype(np.float32)
    if len(cs) == 1:
        return np.broadcast_to(cs[0], t.shape + (3,)).astype(np.float32).copy()
    t = np.clip(t, 0, 1) * (len(cs) - 1)
    i = np.minimum(np.floor(t).astype(np.int32), len(cs) - 2)
    f = (t - i)[..., None]
    return (cs[i] * (1 - f) + cs[i + 1] * f).astype(np.float32)


def _blend_fn(mode, s, d):
    if mode == "normal":
        return s
    if mode == "multiply":
        return s * d
    if mode == "screen":
        return 1 - (1 - s) * (1 - d)
    if mode == "overlay":
        return np.where(d < 0.5, 2 * s * d, 1 - 2 * (1 - s) * (1 - d))
    if mode == "darken":
        return np.minimum(s, d)
    if mode == "lighten":
        return np.maximum(s, d)
    raise RecipeError(f"unknown blend mode {mode!r}")


def blend(dst: np.ndarray, src_rgb: np.ndarray, alpha: np.ndarray, mode: str = "normal") -> np.ndarray:
    """Composite an opaque source colour (h,w,3) with coverage alpha (h,w) onto premultiplied dst."""
    a = alpha[..., None].astype(np.float32)
    da = dst[..., 3:4]
    dc = np.divide(dst[..., :3], da, out=np.zeros_like(dst[..., :3]), where=da > 1e-6)
    mixed = (1 - da) * src_rgb + da * _blend_fn(mode, src_rgb, dc)
    out = np.empty_like(dst)
    out[..., :3] = (1 - a) * dst[..., :3] + a * mixed
    out[..., 3:4] = a + da * (1 - a)
    return out


def composite_inplace(img: np.ndarray, src_rgb, alpha: np.ndarray, mode: str = "normal") -> None:
    if not isinstance(src_rgb, np.ndarray) or src_rgb.ndim == 1:
        src_rgb = np.broadcast_to(np.asarray(src_rgb, np.float32)[:3], img.shape[:2] + (3,))
    img[...] = blend(img, src_rgb, alpha, mode)


def composite_patch(img: np.ndarray, patch, src_rgb, opacity: float = 1.0, mode: str = "normal") -> None:
    """Composite a flat colour through a :class:`mapgen.ops.masks.Patch`."""
    if patch is None:
        return
    ys, xs = patch.slices
    sub = img[ys, xs]
    rgb = np.broadcast_to(np.asarray(src_rgb, np.float32)[:3], sub.shape[:2] + (3,))
    img[ys, xs] = blend(sub, rgb, (patch.alpha * opacity).astype(np.float32), mode)
