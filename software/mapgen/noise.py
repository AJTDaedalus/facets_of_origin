"""Vectorised gradient (Perlin) noise and fractal sums.

Written in numpy rather than taking opensimplex, which is pure Python without
numba (~30 s per octave at 2000² px). Low-frequency octaves are sampled on a
coarse lattice (8 samples per wavelength) and spline-upsampled.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage

_ANG = np.arange(16) * (2 * np.pi / 16)
_GX = np.cos(_ANG).astype(np.float32)
_GY = np.sin(_ANG).astype(np.float32)
SAMPLES_PER_WAVE = 8


def _perm(seed: int) -> np.ndarray:
    p = np.random.default_rng(seed & 0x7FFFFFFF).permutation(256)
    return np.concatenate([p, p]).astype(np.int32)


def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def perlin(x: np.ndarray, y: np.ndarray, seed: int) -> np.ndarray:
    """Gradient noise at lattice coordinates (x, y); output roughly in [-1, 1]."""
    p = _perm(seed)
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    xi = np.floor(x).astype(np.int64)
    yi = np.floor(y).astype(np.int64)
    xf = (x - xi).astype(np.float32)
    yf = (y - yi).astype(np.float32)
    xi &= 255
    yi &= 255

    def grad(ix, iy, dx, dy):
        h = p[p[ix] + iy] & 15
        return _GX[h] * dx + _GY[h] * dy

    n00 = grad(xi, yi, xf, yf)
    n10 = grad(xi + 1, yi, xf - 1, yf)
    n01 = grad(xi, yi + 1, xf, yf - 1)
    n11 = grad(xi + 1, yi + 1, xf - 1, yf - 1)
    u, v = _fade(xf), _fade(yf)
    a = n00 + u * (n10 - n00)
    b = n01 + u * (n11 - n01)
    return ((a + v * (b - a)) * 1.4142).astype(np.float32)


def _octave_seed(seed: int, i: int) -> int:
    return (seed * 1_000_003 + i * 7919 + 17) & 0x7FFFFFFF


def _offsets(seed: int) -> tuple[float, float]:
    r = np.random.default_rng(seed)
    return float(r.uniform(0, 256)), float(r.uniform(0, 256))


def noise_grid(shape: tuple[int, int], scale_px: float, seed: int) -> np.ndarray:
    """One octave over an (h, w) pixel grid; one wavelength = ``scale_px`` pixels."""
    h, w = shape
    scale_px = max(float(scale_px), 1e-3)
    ox, oy = _offsets(seed)
    step = scale_px / SAMPLES_PER_WAVE
    if step > 1.5:
        ch, cw = int(np.ceil(h / step)) + 2, int(np.ceil(w / step)) + 2
        xs = (np.arange(cw) * step) / scale_px + ox
        ys = (np.arange(ch) * step) / scale_px + oy
        coarse = perlin(xs[None, :], ys[:, None], seed)
        yy = (np.arange(h, dtype=np.float32) + 0.5) / step
        xx = (np.arange(w, dtype=np.float32) + 0.5) / step
        # separable cubic upsample: rows then columns
        tmp = ndimage.map_coordinates(coarse, np.meshgrid(yy, np.arange(cw), indexing="ij"),
                                      order=3, mode="nearest")
        out = ndimage.map_coordinates(tmp, np.meshgrid(np.arange(h), xx, indexing="ij"),
                                      order=3, mode="nearest")
        return out.astype(np.float32)
    xs = (np.arange(w) + 0.5) / scale_px + ox
    ys = (np.arange(h) + 0.5) / scale_px + oy
    return perlin(xs[None, :], ys[:, None], seed)


def _shape_octave(n, kind):
    if kind == "ridged":
        r = 1.0 - np.abs(n)
        return r * r * 2 - 1
    if kind == "billow":
        return np.abs(n) * 2 - 1
    return n


def fbm(shape, scale_px, seed, octaves=4, persistence=0.5, lacunarity=2.0, kind="fbm") -> np.ndarray:
    """Fractal sum over a pixel grid, clipped to [-1, 1]."""
    total = np.zeros(shape, np.float32)
    amp, norm, sc = 1.0, 0.0, float(scale_px)
    for i in range(int(octaves)):
        total += amp * _shape_octave(noise_grid(shape, sc, _octave_seed(seed, i)), kind)
        norm += amp
        amp *= persistence
        sc /= lacunarity
        if sc < 1.0:
            break
    return np.clip(total / norm, -1, 1)


def fbm_at(x, y, scale, seed, octaves=3, persistence=0.5, lacunarity=2.0) -> np.ndarray:
    """Fractal noise at arbitrary points (same units as ``scale``)."""
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    total = np.zeros(x.shape, np.float32)
    amp, norm, sc = 1.0, 0.0, float(scale)
    for i in range(int(octaves)):
        s = _octave_seed(seed, i)
        ox, oy = _offsets(s)
        total += amp * perlin(x / sc + ox, y / sc + oy, s)
        norm += amp
        amp *= persistence
        sc /= lacunarity
    return np.clip(total / norm, -1, 1)
