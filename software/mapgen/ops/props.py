"""Prop library, place and scatter (T21, T22). Props are built from shapely parts
in prop-local feet, then rotated, placed, shadowed, filled and inked."""
from __future__ import annotations

from typing import Any, Literal

import numpy as np
import shapely
from pydantic import Field as PField
from scipy import ndimage
from shapely import affinity
from shapely.geometry import LineString, Point as SPoint, Polygon, box

from ..color import composite_patch, resolve_color
from ..layers import Image, Mask
from ..recipe import RecipeError
from ..registry import ParamModel, op
from .common import Point, PosFt, Ref, Unit
from .masks import Patch, rasterize_patch
from .paint import stroke_geometry_alpha

COLORS = {"wood": "#8a6440", "wood_light": "#a77f55", "wood_dark": "#5e412a", "cloth": "#9c3b32",
          "linen": "#e8e0cc", "metal": "#77736c", "stone_light": "#c2bbad", "stone": "#9d968a",
          "stone_dark": "#6f695f", "foliage": "#4c5a44", "foliage_light": "#66755c",
          "foliage_dark": "#2f4722", "foliage_top": "#8a977a", "fire": "#f0a040", "rug": "#7b3f3a", "rug_trim": "#c9a45c",
          "upland_light": "#e3d3a6", "upland_dark": "#a9925f", "ink_fill": "#1c1814",
          "mtn_light": "#cfc2ae", "mtn_dark": "#7d6a58"}

INK_FINE, INK_MED = 0.08, 0.13


def _blob(r, lobes, rng, rough=0.18, n=64):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ph = rng.uniform(0, 2 * np.pi)
    rr = r * (1 + rough * np.sin(lobes * a + ph) * 0.6 + rough * 0.4 * np.sin((lobes + 3) * a + 2 * ph))
    rr *= 1 + rng.uniform(-0.05, 0.05, n) * rough * 2
    return Polygon(np.c_[rr * np.cos(a), rr * np.sin(a)])


def _scallop(r, lobes, rng):
    parts = [SPoint(0, 0).buffer(r * 0.72)]
    for i in range(lobes):
        a = 2 * np.pi * i / lobes + rng.uniform(-0.25, 0.25)
        d = r * rng.uniform(0.55, 0.68)
        parts.append(SPoint(d * np.cos(a), d * np.sin(a)).buffer(r * rng.uniform(0.32, 0.42)))
    return shapely.unary_union(parts)


# Each builder: (size_ft, rng) -> list of (geometry, colour key or None, ink width or 0)
def p_table(s, rng):
    t = box(-s / 2, -s * 0.28, s / 2, s * 0.28)
    lines = [LineString([(-s / 2, y), (s / 2, y)]) for y in (-s * 0.093, s * 0.093)]
    return [(t, "wood", INK_MED)] + [(l, None, INK_FINE * 0.7) for l in lines]


def p_round_table(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "wood", INK_MED), (SPoint(0, 0).buffer(s * 0.36).exterior, None, INK_FINE * 0.7)]


def p_chair(s, rng):
    return [(box(-s / 2, -s / 2, s / 2, s / 2), "wood_light", INK_FINE),
            (box(-s / 2, -s / 2, s / 2, -s * 0.3), "wood_dark", INK_FINE)]


def p_bed(s, rng):
    w = s * 0.5
    frame = box(-s / 2, -w / 2, s / 2, w / 2)
    blanket = box(-s / 2 + s * 0.3, -w / 2 + 0.04 * s, s / 2 - 0.03 * s, w / 2 - 0.04 * s)
    pillow = box(-s / 2 + s * 0.05, -w / 2 + w * 0.15, -s / 2 + s * 0.24, w / 2 - w * 0.15)
    return [(frame, "wood", INK_MED), (blanket, "cloth", INK_FINE), (pillow, "linen", INK_FINE)]


def p_bunk(s, rng):
    parts = p_bed(s, rng)
    w = s * 0.5
    parts.append((box(-s / 2 + 0.08 * s, -w / 2 + 0.06 * s, s / 2 - 0.08 * s, w / 2 - 0.06 * s).exterior, None, INK_FINE))
    return parts


def p_crate(s, rng):
    b = box(-s / 2, -s / 2, s / 2, s / 2)
    i = box(-s * 0.38, -s * 0.38, s * 0.38, s * 0.38)
    x = [LineString([(-s * 0.38, -s * 0.38), (s * 0.38, s * 0.38)]), LineString([(-s * 0.38, s * 0.38), (s * 0.38, -s * 0.38)])]
    return [(b, "wood_light", INK_MED), (i.exterior, None, INK_FINE)] + [(l, None, INK_FINE) for l in x]


def p_barrel(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "wood", INK_MED),
            (SPoint(0, 0).buffer(s * 0.36), "wood_light", INK_FINE),
            (SPoint(0, 0).buffer(s * 0.18).exterior, None, INK_FINE * 0.8)]


def p_chest(s, rng):
    w = s * 0.6
    return [(box(-s / 2, -w / 2, s / 2, w / 2), "wood_dark", INK_MED),
            (box(-s / 2, -w * 0.12, s / 2, w * 0.12), "metal", INK_FINE),
            (box(-s * 0.08, -w * 0.18, s * 0.08, w * 0.18), "fire", INK_FINE)]


def p_rubble(s, rng):
    parts = []
    for _ in range(int(rng.integers(5, 9))):
        r = s * rng.uniform(0.08, 0.2)
        c = rng.uniform(-s * 0.32, s * 0.32, 2)
        g = affinity.translate(_blob(r, int(rng.integers(3, 6)), rng, 0.35, 12), *c)
        parts.append((g, rng.choice(["stone_light", "stone", "stone_dark"]), INK_FINE))
    return parts


def p_pebbles(s, rng):
    parts = []
    for _ in range(int(rng.integers(2, 5))):
        r = s * rng.uniform(0.07, 0.16)
        c = rng.uniform(-s * 0.35, s * 0.35, 2)
        g = affinity.translate(_blob(r, int(rng.integers(3, 5)), rng, 0.3, 10), *c)
        parts.append((g, rng.choice(["stone_light", "stone"]), INK_FINE * 0.8))
    return parts


def p_stalagmite(s, rng):
    base = _blob(s / 2, 7, rng, 0.1, 48)
    mid = affinity.translate(_blob(s * 0.34, 6, rng, 0.12, 36), -s * 0.04, -s * 0.05)
    tip = affinity.translate(_blob(s * 0.13, 5, rng, 0.1, 24), -s * 0.07, -s * 0.08)
    cracks = []
    for i in range(int(rng.integers(4, 7))):
        a = rng.uniform(0, 2 * np.pi)
        r0, r1 = s * 0.18, s * rng.uniform(0.36, 0.46)
        cracks.append((LineString([(r0 * np.cos(a), r0 * np.sin(a)), (r1 * np.cos(a + 0.15), r1 * np.sin(a + 0.15))]),
                       None, INK_FINE * 0.6))
    return [(base, "stone_dark", INK_MED), (mid, "stone", INK_FINE * 0.7), (tip, "stone_light", 0)] + cracks


def p_boulder(s, rng):
    b = _blob(s / 2, 4, rng, 0.35, 20)
    hl = affinity.translate(affinity.scale(b, 0.55, 0.5), -s * 0.1, -s * 0.12)
    return [(b, "stone", INK_MED), (hl, "stone_light", 0)]


def _canopy(r, lobes, rng):
    parts = [SPoint(0, 0).buffer(r * 0.7)]
    for i in range(lobes):
        a = 2 * np.pi * i / lobes + rng.uniform(-0.15, 0.15)
        d = r * rng.uniform(0.66, 0.76)
        parts.append(SPoint(d * np.cos(a), d * np.sin(a)).buffer(r * rng.uniform(0.2, 0.28)))
    return shapely.unary_union(parts)


def p_tree(s, rng):
    c = _canopy(s / 2, int(rng.integers(13, 18)), rng)
    mid = affinity.translate(_canopy(s * 0.36, int(rng.integers(9, 12)), rng), -s * 0.05, -s * 0.06)
    top = affinity.translate(_canopy(s * 0.2, int(rng.integers(6, 9)), rng), -s * 0.1, -s * 0.11)
    cx, cy = -s * 0.04, -s * 0.05
    branches = []
    n = int(rng.integers(7, 11))
    for i in range(n):
        a = 2 * np.pi * i / n + rng.uniform(-0.3, 0.3)
        L = s * rng.uniform(0.12, 0.24)
        branches.append((LineString([(cx, cy), (cx + L * np.cos(a), cy + L * np.sin(a))]), None, INK_FINE * 0.55))
    crescent = c.difference(affinity.translate(c, -s * 0.16, -s * 0.16))
    shading = []
    for k in np.linspace(-0.5, 0.5, 11):
        ln = LineString([(k * s - s * 0.3, s * 0.6), (k * s + s * 0.3, -s * 0.6)]).intersection(crescent)
        for piece in getattr(ln, "geoms", [ln]):
            if not piece.is_empty and piece.length > s * 0.03:
                shading.append((piece, None, INK_FINE * 0.55))
    return [(c, "foliage", INK_MED * 2.0), (mid, "foliage_light", INK_FINE * 0.9), (top, "foliage_top", INK_FINE * 0.6)] + branches + shading


def p_bush(s, rng):
    c = _scallop(s / 2, int(rng.integers(5, 8)), rng)
    inner = affinity.translate(_scallop(s * 0.28, 4, rng), -s * 0.06, -s * 0.06)
    return [(c, "foliage", INK_FINE), (inner, "foliage_light", 0)]


def p_bridge(s, rng):
    w = s * 0.42
    deck = box(-s / 2, -w / 2, s / 2, w / 2)
    planks = [(LineString([(x, -w / 2), (x, w / 2)]), None, INK_FINE * 0.7) for x in np.linspace(-s / 2, s / 2, int(s / 0.8) + 1)[1:-1]]
    rails = [(box(-s / 2, y - w * 0.06, s / 2, y + w * 0.06), "wood_dark", INK_FINE) for y in (-w / 2, w / 2)]
    return [(deck, "wood_light", INK_MED)] + planks + rails


def p_brazier(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "metal", INK_MED), (SPoint(0, 0).buffer(s * 0.3), "fire", 0),
            (SPoint(0, 0).buffer(s * 0.14), "linen", 0)]


def p_pillar(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "stone_light", INK_MED), (SPoint(0, 0).buffer(s * 0.36).exterior, None, INK_FINE)]


def p_statue(s, rng):
    star = Polygon([(np.cos(a) * (s * 0.3 if i % 2 else s * 0.14), np.sin(a) * (s * 0.3 if i % 2 else s * 0.14))
                    for i, a in enumerate(np.linspace(-np.pi / 2, 1.5 * np.pi, 10, endpoint=False))])
    return [(box(-s / 2, -s / 2, s / 2, s / 2), "stone_light", INK_MED), (star, "stone_dark", INK_FINE)]


def p_rug(s, rng):
    w = s * 0.62
    o = box(-s / 2, -w / 2, s / 2, w / 2)
    i = box(-s * 0.42, -w * 0.38, s * 0.42, w * 0.38)
    d = Polygon([(0, -w * 0.3), (s * 0.3, 0), (0, w * 0.3), (-s * 0.3, 0)])
    return [(o, "rug", INK_FINE), (i.exterior, "rug_trim", INK_FINE * 0.7), (d, "rug_trim", 0)]


def p_banner(s, rng):
    return [(box(-s / 2, -s * 0.12, s / 2, s * 0.12), "cloth", INK_FINE),
            (LineString([(-s / 2, s * 0.06), (s / 2, s * 0.06)]), None, INK_FINE * 0.6)]


def p_mountain(s, rng):
    ax = rng.uniform(-0.12, 0.12) * s
    A = (ax, -0.42 * s)
    L, R = (-s / 2, 0.28 * s), (s / 2, 0.28 * s)
    F = (ax + rng.uniform(0.02, 0.14) * s, 0.28 * s)
    left = Polygon([A, L, F])
    right = Polygon([A, F, R])
    hatch = []
    for t in np.linspace(0.08, 0.92, int(rng.integers(7, 11))):
        px, py = A[0] + (R[0] - A[0]) * t, A[1] + (R[1] - A[1]) * t
        ln = LineString([(px, py), (px - 0.08 * s, py + 0.35 * s)]).intersection(right)
        if not ln.is_empty and ln.length > 0:
            hatch.append((ln, None, INK_FINE * 0.7))
    return [(left, "mtn_light", 0), (right, "mtn_dark", 0), (Polygon([A, L, R]).exterior, None, INK_MED),
            (LineString([A, F]), None, INK_FINE)] + hatch


def p_hill(s, rng):
    """A round dome seen from above, shaded and radially hatched on its south-east side."""
    dome = _blob(s / 2, 5, rng, 0.08, 40)
    shade = dome.intersection(affinity.translate(SPoint(0, 0).buffer(s / 2), s * 0.22, s * 0.22))
    top = affinity.translate(SPoint(0, 0).buffer(s * 0.16), -s * 0.08, -s * 0.08)
    hatch = []
    for i in range(int(rng.integers(8, 13))):
        a = rng.uniform(-0.35, 2.0)            # mostly the lower-right half
        r0, r1 = s * rng.uniform(0.18, 0.28), s * 0.48
        hatch.append((LineString([(r0 * np.cos(a), r0 * np.sin(a)), (r1 * np.cos(a), r1 * np.sin(a))]),
                      None, INK_FINE * 0.75))
    return [(dome, "upland_light", INK_FINE), (shade, "upland_dark", 0), (top, "linen", 0)] + hatch


def p_peak(s, rng):
    return [(Polygon([(0, -s / 2), (s / 2, s / 2), (-s / 2, s / 2)]), "linen", INK_MED)]


def p_city(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "linen", INK_MED), (SPoint(0, 0).buffer(s * 0.3), "ink_fill", 0)]


def p_town(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "linen", INK_MED * 1.2)]


def p_village(s, rng):
    return [(SPoint(0, 0).buffer(s / 2), "ink_fill", 0)]


def p_ruin_marker(s, rng):
    return [(box(-s / 2, -s / 2, s / 2, s / 2), "ink_fill", 0)]


def p_conifer(s, rng):
    pts = []
    for i in range(16):
        a = -np.pi / 2 + 2 * np.pi * i / 16
        r = s / 2 if i % 2 == 0 else s * 0.3
        pts.append((r * np.cos(a), r * np.sin(a)))
    return [(Polygon(pts), "foliage", INK_FINE)]


MARKERS = {"peak", "city", "town", "village", "ruin_marker"}

PROPS = {"table": (p_table, 4.0), "round_table": (p_round_table, 4.0), "chair": (p_chair, 1.5),
         "bed": (p_bed, 6.0), "bunk": (p_bunk, 6.0), "crate": (p_crate, 2.5), "barrel": (p_barrel, 2.5),
         "chest": (p_chest, 3.0), "rubble": (p_rubble, 3.0), "pebbles": (p_pebbles, 1.2), "stalagmite": (p_stalagmite, 3.0),
         "boulder": (p_boulder, 4.0), "tree": (p_tree, 12.0), "bush": (p_bush, 4.0), "bridge": (p_bridge, 10.0),
         "brazier": (p_brazier, 2.0), "pillar": (p_pillar, 2.5), "statue": (p_statue, 5.0), "rug": (p_rug, 8.0),
         "banner": (p_banner, 4.0), "mountain": (p_mountain, 4.0), "hill": (p_hill, 3.0), "peak": (p_peak, 1.2),
         "city": (p_city, 1.6), "town": (p_town, 1.1), "village": (p_village, 0.7), "ruin_marker": (p_ruin_marker, 0.9),
         "conifer": (p_conifer, 1.5)}

PropKind = Literal[tuple(PROPS)]  # type: ignore[valid-type]


def _color(ctx, key):
    try:
        return resolve_color(ctx.style, key)
    except RecipeError:
        return resolve_color(ctx.style, COLORS[key])


def draw_prop(ctx, img, kind, at, size=None, rotate=0.0, seed=0, shadow=0.35, ink="ink"):
    fn, default = PROPS[kind]
    s = size or default
    if kind in MARKERS:
        shadow = 0.0
    if kind == "tree":
        rotate = 0.0          # its shading crescent must stay south-east (light from the north-west)
    rng = np.random.default_rng(seed)
    parts = fn(s, rng)
    placed = []
    for g, ck, iw in parts:
        if rotate:
            g = affinity.rotate(g, rotate, origin=(0, 0))
        placed.append((affinity.translate(g, at[0], at[1]), ck, iw))
    solid = [g for g, ck, _ in placed if ck and g.geom_type in ("Polygon", "MultiPolygon")]
    foot = shapely.unary_union(solid) if solid else Polygon()
    if shadow > 0 and not foot.is_empty:
        off = s * (0.1 if kind in ("tree", "bush") else 0.06) + 0.15
        sh = affinity.translate(foot, off, off * 1.1)
        p = rasterize_patch(ctx.frame, sh.buffer(s * 0.03))
        if p is not None:
            blurred = ndimage.gaussian_filter(np.pad(p.alpha, 6), max(ctx.frame.px(s * 0.04), 0.8))
            pad = Patch(blurred, p.y0 - 6, p.x0 - 6)
            if pad.y0 >= 0 and pad.x0 >= 0:
                ys, xs = pad.slices
                H, W = img.shape[:2]
                hh, ww = min(ys.stop, H) - ys.start, min(xs.stop, W) - xs.start
                pad.alpha = pad.alpha[:hh, :ww]
                composite_patch(img, pad, (0, 0, 0), shadow)
            else:
                composite_patch(img, p, (0, 0, 0), shadow)
    inkc = resolve_color(ctx.style, ink)[:3]
    for g, ck, iw in placed:
        if ck and g.geom_type in ("Polygon", "MultiPolygon"):
            c = _color(ctx, ck)
            composite_patch(img, rasterize_patch(ctx.frame, g), c[:3], float(c[3]))
        if iw:
            composite_patch(img, stroke_geometry_alpha(ctx, g, iw, patch=True), inkc)
    ctx.collector.legend.setdefault(kind, kind.replace("_", " "))
    if not foot.is_empty:
        ctx.collector.footprints.append(foot)
    return foot


class PropP(ParamModel):
    into: Ref = "canvas"
    kind: PropKind
    at: Point
    size: PosFt | None = None
    rotate: float = 0.0
    shadow: Unit = 0.35
    ink: Any = "ink"


@op("prop", params=PropP, inputs={"into": Image}, group="6 props")
def prop(ctx, p, into):
    """Place one prop at `at` (feet), `size` feet across its long side, rotated `rotate` degrees, with a soft cast shadow. Trees ignore `rotate`: their shading always sits south-east."""
    draw_prop(ctx, into.data, p.kind, p.at, p.size, p.rotate, ctx.seed, p.shadow, p.ink)


def poisson_disk(bounds, r, rng, k=20):
    """Bridson's Poisson-disk sampling in a rectangle (minx, miny, maxx, maxy)."""
    minx, miny, maxx, maxy = bounds
    w, h = maxx - minx, maxy - miny
    if w <= 0 or h <= 0:
        return []
    cell = r / np.sqrt(2)
    gw, gh = int(np.ceil(w / cell)), int(np.ceil(h / cell))
    grid = -np.ones((gh, gw), int)
    pts = []
    first = np.array([rng.uniform(0, w), rng.uniform(0, h)])
    pts.append(first)
    grid[int(first[1] / cell), int(first[0] / cell)] = 0
    active = [0]
    while active:
        idx = active[int(rng.integers(len(active)))]
        base = pts[idx]
        found = False
        for _ in range(k):
            a = rng.uniform(0, 2 * np.pi)
            d = rng.uniform(r, 2 * r)
            c = base + d * np.array([np.cos(a), np.sin(a)])
            if not (0 <= c[0] < w and 0 <= c[1] < h):
                continue
            gx, gy = int(c[0] / cell), int(c[1] / cell)
            ok = True
            for yy in range(max(gy - 2, 0), min(gy + 3, gh)):
                for xx in range(max(gx - 2, 0), min(gx + 3, gw)):
                    j = grid[yy, xx]
                    if j >= 0 and np.sum((pts[j] - c) ** 2) < r * r:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                pts.append(c)
                grid[gy, gx] = len(pts) - 1
                active.append(len(pts) - 1)
                found = True
                break
        if not found:
            active.remove(idx)
    return [(float(x + minx), float(y + miny)) for x, y in pts]


class ScatterP(ParamModel):
    into: Ref = "canvas"
    kind: PropKind
    mask: Ref | None = None
    region: list[Point] | None = None
    avoid: list[Ref] = []
    density: float = PField(0.2, gt=0, le=4)
    spacing: PosFt = 2.0
    size: PosFt | None = None
    size_jitter: Unit = 0.25
    rotate_jitter: float = PField(180.0, ge=0, le=360)
    shadow: Unit = 0.35
    sort_y: bool = False


@op("scatter", params=ScatterP, inputs={"into": Image, "mask": Mask, "avoid": Mask}, group="6 props")
def scatter(ctx, p, into, mask=None, avoid=None):
    """Scatter props by Poisson disk inside a mask and/or a region polygon: `density` props per grid square, at least `spacing` feet apart, avoiding the `avoid` masks. `sort_y: true` draws north to south so glyphs (mountains, trees) overlap correctly."""
    fr = ctx.frame
    rng = ctx.rng
    allowed = np.ones(fr.shape, bool) if mask is None else mask.data >= 0.5
    if p.region:
        from .masks import rasterize_geom
        allowed &= rasterize_geom(fr, Polygon(p.region)) >= 0.5
    for a in avoid or []:
        allowed &= a.data < 0.5
    if not allowed.any():
        pts = []
    else:
        ys, xs = np.nonzero(allowed)
        b = (xs.min() / fr.scale, ys.min() / fr.scale, (xs.max() + 1) / fr.scale, (ys.max() + 1) / fr.scale)
        cand = poisson_disk(b, p.spacing, rng)
        pts = []
        for x, y in cand:
            ix, iy = int(x * fr.scale), int(y * fr.scale)
            if 0 <= iy < fr.shape[0] and 0 <= ix < fr.shape[1] and allowed[iy, ix]:
                pts.append((x, y))
        area_sq = allowed.sum() / (fr.scale ** 2) / (fr.fps ** 2)
        target = int(round(p.density * area_sq))
        if len(pts) > target:
            keep = np.sort(rng.choice(len(pts), target, replace=False))
            pts = [pts[i] for i in keep]
    base = p.size or PROPS[p.kind][1]
    if p.sort_y:
        pts = sorted(pts, key=lambda q: (q[1], q[0]))
    for i, (x, y) in enumerate(pts):
        s = base * (1 + rng.uniform(-p.size_jitter, p.size_jitter))
        rot = rng.uniform(-p.rotate_jitter / 2, p.rotate_jitter / 2)
        draw_prop(ctx, into.data, p.kind, (x, y), s, rot, ctx.seed + 31 * i + 1, p.shadow)
    key = ctx.step.id if ctx.step and ctx.step.id else f"#{ctx.index}"
    ctx.collector.scatter_points[key] = [(round(x, 4), round(y, 4)) for x, y in pts]
