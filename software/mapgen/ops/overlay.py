"""Overlay ops (T23): grid, compass, scale bar, title, labels, frame, legend."""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Literal, Union

import numpy as np
from PIL import Image as PImage, ImageDraw, ImageFilter, ImageFont
from pydantic import Field as PField
from shapely.geometry import LineString, Point as SPoint, Polygon, box

from ..color import composite_inplace, composite_patch, resolve_color
from ..layers import Geometry, Image, Mask
from ..registry import ParamModel, op
from .common import Point, PosFt, Ref, Unit
from .masks import Patch, rasterize_patch
from .paint import stroke_geometry_alpha

Corner = Union[Literal["ne", "nw", "se", "sw"], Point]
FONT_FILES = {False: ["DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
              True: ["DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
              "italic": ["DejaVuSerif-Italic.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
                         "DejaVuSerif.ttf"],
              "bolditalic": ["DejaVuSerif-BoldItalic.ttf",
                             "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf", "DejaVuSerif-Bold.ttf"]}


@lru_cache(maxsize=64)
def font(px: int, bold: bool = False):
    for f in FONT_FILES[bold]:
        try:
            return ImageFont.truetype(f, max(px, 6))
        except OSError:
            continue
    return ImageFont.load_default(size=max(px, 6))


def text_alpha(text, px, bold=False, halo_px=0):
    f = font(int(round(px)), bold)
    l, t, r, b = f.getbbox(text)
    pad = int(halo_px) + 2
    img = PImage.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=f, fill=255)
    a = np.asarray(img, np.float32) / 255
    halo = None
    if halo_px > 0:
        k = int(halo_px) * 2 + 1
        halo = np.asarray(img.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    return a, halo


def _place(img, alpha, center_px, color, opacity=1.0):
    H, W = img.shape[:2]
    h, w = alpha.shape
    y0 = int(round(center_px[1] - h / 2))
    x0 = int(round(center_px[0] - w / 2))
    ys0, xs0 = max(y0, 0), max(x0, 0)
    ys1, xs1 = min(y0 + h, H), min(x0 + w, W)
    if ys1 <= ys0 or xs1 <= xs0:
        return
    sub = alpha[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    composite_patch(img, Patch(sub, ys0, xs0), color[:3], opacity * float(color[3]))


def draw_text(ctx, img, text, at_ft, size_ft, color, bold=False, halo="parchment", halo_ft=0.25):
    fr = ctx.frame
    px = fr.px(size_ft)
    hp = fr.px(halo_ft) if halo is not None else 0
    a, h = text_alpha(text, px, bold, hp)
    c = (at_ft[0] * fr.scale, at_ft[1] * fr.scale)
    if h is not None:
        try:
            hc = resolve_color(ctx.style, halo)
        except Exception:
            hc = resolve_color(ctx.style, "#efe6cf")
        _place(img, h, c, hc, 0.9)
    _place(img, a, c, color if isinstance(color, np.ndarray) else resolve_color(ctx.style, color))


def corner_xy(ctx, at, half_w, half_h):
    if isinstance(at, list):
        return at
    fr = ctx.frame
    m = fr.fps * 0.6
    x = m + half_w if at[1] == "w" else fr.width_ft - m - half_w
    y = m + half_h if at[0] == "n" else fr.height_ft - m - half_h
    return [x, y]


def scale_text(frame, collector) -> str:
    cell = "hex" if collector.grid_shape == "hex" else "square"
    n = frame.fps
    n = int(n) if float(n).is_integer() else n
    word = {"ft": "feet", "mi": "miles"}[frame.unit]
    if n == 1:
        word = word[:-1] if word == "miles" else "foot"
    return f"1 {cell} = {n} {word}"


def hex_centres(width, height, size, orientation="flat"):
    """Hex centres covering a width × height area; `size` is the flat-to-flat distance."""
    R = size / np.sqrt(3)
    pts = []
    if orientation == "flat":
        dx, dy = 1.5 * R, size
        for c in range(-1, int(width / dx) + 2):
            for r in range(-1, int(height / dy) + 2):
                pts.append((c * dx, r * dy + (dy / 2 if c % 2 else 0)))
    else:
        dx, dy = size, 1.5 * R
        for r in range(-1, int(height / dy) + 2):
            for c in range(-1, int(width / dx) + 2):
                pts.append((c * dx + (dx / 2 if r % 2 else 0), r * dy))
    return pts


def hex_lines(width, height, size, orientation="flat"):
    import shapely
    R = size / np.sqrt(3)
    off = 0 if orientation == "flat" else np.pi / 6
    ang = np.arange(6) * np.pi / 3 + off
    rings = []
    for x, y in hex_centres(width, height, size, orientation):
        rings.append(LineString([(x + R * np.cos(a), y + R * np.sin(a)) for a in list(ang) + [ang[0]]]))
    return shapely.unary_union(rings)


class GridP(ParamModel):
    into: Ref = "canvas"
    mask: Ref | None = None
    color: Any = "ink"
    alpha: Unit = 0.3
    weight: PosFt = 0.06
    shape: Literal["square", "hex"] = "square"
    orientation: Literal["flat", "pointy"] = "flat"


@op("grid", params=GridP, inputs={"into": Image, "mask": Mask}, group="7 overlay")
def grid(ctx, p, into, mask=None):
    """Square grid at the map's grid size (lines on pixel columns, crisp), or a hex grid (`shape: hex`, flat or pointy, `feet_per_square` across the flats). Optionally clipped to a mask."""
    fr = ctx.frame
    h, w = fr.shape
    ctx.collector.grid_shape = p.shape
    if p.shape == "hex":
        from .masks import rasterize_geom
        a = rasterize_geom(fr, hex_lines(fr.width_ft, fr.height_ft, fr.fps, p.orientation),
                           max(p.weight, 1.0 / fr.scale))
        if mask is not None:
            a = a * mask.data
        ctx.collector.masks["grid"] = a
        c = resolve_color(ctx.style, p.color)
        composite_inplace(into.data, c[:3], (a * p.alpha).astype(np.float32))
        return
    sq = fr.square_px
    hw = max(fr.px(p.weight) / 2, 0.5)

    def lines(n):
        c = np.arange(n, dtype=np.float32)
        d = np.mod(c, sq)
        d = np.minimum(d, sq - d)
        return np.clip(hw + 0.5 - d, 0, 1)

    a = np.maximum(lines(w)[None, :], lines(h)[:, None])
    if mask is not None:
        a = a * mask.data
    ctx.collector.masks["grid"] = a
    c = resolve_color(ctx.style, p.color)
    composite_inplace(into.data, c[:3], (a * p.alpha).astype(np.float32))


class CompassP(ParamModel):
    into: Ref = "canvas"
    at: Corner = "ne"
    size: PosFt = 6.0
    color: Any = "ink"
    fill: Any = "parchment"


@op("compass", params=CompassP, inputs={"into": Image}, group="7 overlay")
def compass(ctx, p, into):
    """A compass rose with N, at a corner (ne/nw/se/sw) or [x, y] feet."""
    c = corner_xy(ctx, p.at, p.size / 2, p.size / 2 + p.size * 0.15)
    cx, cy = c
    r = p.size * 0.42
    ink = resolve_color(ctx.style, p.color)
    try:
        light = resolve_color(ctx.style, p.fill)
    except Exception:
        light = resolve_color(ctx.style, "#efe6cf")
    img = into.data
    ring = SPoint(cx, cy).buffer(r * 0.55)
    composite_patch(img, stroke_geometry_alpha(ctx, ring, 0.08, patch=True), ink[:3])
    for i, ang in enumerate(np.arange(4) * np.pi / 2 - np.pi / 2):
        tip = (cx + np.cos(ang) * r, cy + np.sin(ang) * r)
        l = (cx + np.cos(ang - np.pi / 2) * r * 0.16, cy + np.sin(ang - np.pi / 2) * r * 0.16)
        rr = (cx + np.cos(ang + np.pi / 2) * r * 0.16, cy + np.sin(ang + np.pi / 2) * r * 0.16)
        for half, colr in ((Polygon([tip, l, (cx, cy)]), ink), (Polygon([tip, rr, (cx, cy)]), light)):
            composite_patch(img, rasterize_patch(ctx.frame, half), colr[:3])
            composite_patch(img, stroke_geometry_alpha(ctx, half, 0.05, patch=True), ink[:3])
    draw_text(ctx, img, "N", (cx, cy - r - p.size * 0.12), p.size * 0.22, ink, bold=True)


class ScaleBarP(ParamModel):
    into: Ref = "canvas"
    at: Corner = "nw"
    size: PosFt = 1.6
    text: str | None = None
    color: Any = "ink"


@op("scale_bar", params=ScaleBarP, inputs={"into": Image}, group="7 overlay")
def scale_bar(ctx, p, into):
    """The "1 square = 5 feet" note at a corner."""
    t = p.text or scale_text(ctx.frame, ctx.collector)
    wft = len(t) * p.size * 0.32
    c = corner_xy(ctx, p.at, wft, p.size)
    draw_text(ctx, into.data, t, c, p.size, p.color)


class TitleP(ParamModel):
    into: Ref = "canvas"
    text: str
    position: Literal["top", "bottom"] = "bottom"
    size: PosFt = 3.0
    color: Any = "ink"
    fill: Any = "parchment"
    box: bool = True


@op("title", params=TitleP, inputs={"into": Image}, group="7 overlay")
def title(ctx, p, into):
    """Map title in a double-ruled cartouche at the top or bottom edge."""
    fr = ctx.frame
    wft = len(p.text) * p.size * 0.62 + p.size * 2
    hft = p.size * 1.8
    cx = fr.width_ft / 2
    cy = (fr.fps * 0.6 + hft / 2) if p.position == "top" else fr.height_ft - fr.fps * 0.6 - hft / 2
    if p.box:
        r = box(cx - wft / 2, cy - hft / 2, cx + wft / 2, cy + hft / 2)
        try:
            f = resolve_color(ctx.style, p.fill)
        except Exception:
            f = resolve_color(ctx.style, "#efe6cf")
        composite_patch(into.data, rasterize_patch(fr, r), f[:3], 0.95)
        ink = resolve_color(ctx.style, p.color)[:3]
        composite_patch(into.data, stroke_geometry_alpha(ctx, r, 0.14, patch=True), ink)
        composite_patch(into.data, stroke_geometry_alpha(ctx, r.buffer(-p.size * 0.18, join_style=2), 0.06, patch=True), ink)
    draw_text(ctx, into.data, p.text, (cx, cy), p.size, p.color, bold=True, halo=None)


class LabelP(ParamModel):
    into: Ref = "canvas"
    text: str
    at: Point
    size: PosFt = 2.0
    color: Any = "ink"
    bold: bool = False
    halo: Any = "parchment"
    circle: bool = False


@op("label", params=LabelP, inputs={"into": Image}, group="7 overlay")
def label(ctx, p, into):
    """Text centred at `at` with a parchment halo; `circle: true` puts it in a ring (room keys)."""
    if p.circle:
        ring = SPoint(p.at).buffer(p.size * 0.75)
        try:
            f = resolve_color(ctx.style, p.halo)
        except Exception:
            f = resolve_color(ctx.style, "#efe6cf")
        composite_patch(into.data, rasterize_patch(ctx.frame, ring), f[:3])
        composite_patch(into.data, stroke_geometry_alpha(ctx, ring, 0.1, patch=True),
                        resolve_color(ctx.style, p.color)[:3])
    draw_text(ctx, into.data, p.text, p.at, p.size, p.color, p.bold, None if p.circle else p.halo)


class FrameP(ParamModel):
    into: Ref = "canvas"
    margin: float = PField(0.0, ge=0)
    color: Any = "ink"
    weight: PosFt = 0.3


@op("frame", params=FrameP, inputs={"into": Image}, group="7 overlay")
def frame(ctx, p, into):
    """A double-ruled border around the map, `margin` feet in from the edge."""
    fr = ctx.frame
    m = p.margin + p.weight / 2
    r = box(m, m, fr.width_ft - m, fr.height_ft - m)
    ink = resolve_color(ctx.style, p.color)[:3]
    composite_patch(into.data, stroke_geometry_alpha(ctx, r, p.weight, patch=True), ink)
    inner = r.buffer(-p.weight * 2.2, join_style=2)
    if not inner.is_empty:
        composite_patch(into.data, stroke_geometry_alpha(ctx, inner, p.weight * 0.3, patch=True), ink)


class LegendP(ParamModel):
    into: Ref = "canvas"
    at: Corner = "sw"
    size: PosFt = 1.4
    color: Any = "ink"
    fill: Any = "parchment"
    exclude: list[str] = []


@op("legend", params=LegendP, inputs={"into": Image}, group="7 overlay")
def legend(ctx, p, into):
    """A key box listing the props and features used so far, with a small icon for each prop."""
    from .props import PROPS, draw_prop
    kinds = sorted(k for k in ctx.collector.legend if k not in p.exclude)
    ctx.collector.legend_drawn = kinds
    if not kinds:
        return
    row = p.size * 1.7
    wft = p.size * 2.2 + max(len(k) for k in kinds) * p.size * 0.62 + p.size
    hft = row * len(kinds) + p.size
    cx, cy = corner_xy(ctx, p.at, wft / 2, hft / 2)
    r = box(cx - wft / 2, cy - hft / 2, cx + wft / 2, cy + hft / 2)
    try:
        f = resolve_color(ctx.style, p.fill)
    except Exception:
        f = resolve_color(ctx.style, "#efe6cf")
    composite_patch(into.data, rasterize_patch(ctx.frame, r), f[:3], 0.95)
    composite_patch(into.data, stroke_geometry_alpha(ctx, r, 0.1, patch=True), resolve_color(ctx.style, p.color)[:3])
    for i, k in enumerate(kinds):
        y = cy - hft / 2 + p.size / 2 + row * (i + 0.5)
        x_icon = cx - wft / 2 + p.size * 1.2
        if k in PROPS:
            draw_prop(ctx, into.data, k, (x_icon, y), p.size * 1.1, 0, 7, shadow=0.0)
            ctx.collector.legend.setdefault(k, k)
        name = ctx.collector.legend.get(k, k).capitalize()
        tx = x_icon + p.size * 1.1 + len(name) * p.size * 0.31
        draw_text(ctx, into.data, name, (tx, y), p.size, p.color, halo=None)


class PathLabelP(ParamModel):
    into: Ref = "canvas"
    text: str = PField(min_length=1)
    points: list[Point] | None = None
    src: Ref | None = None
    size: PosFt = 2.0
    spacing: float = PField(1.0, gt=0.3, le=4)
    offset: float = 0.0
    color: Any = "ink"
    halo: Any = "parchment"
    halo_ft: float = PField(0.25, ge=0)
    style: Literal["regular", "bold", "italic", "bolditalic"] = "italic"
    align: Literal["start", "center", "end"] = "center"


@op("path_label", params=PathLabelP, inputs={"into": Image, "src": Geometry}, group="7 overlay")
def path_label(ctx, p, into, src=None):
    """Text set along a line (rivers, roads, mountain ranges, forests): each letter follows the curve. Give `points` (smoothed) or a line geometry `src`; `offset` shifts it sideways; `spacing` loosens the letters."""
    from shapely.geometry import LineString as LS
    from ..recipe import RecipeError
    if p.points:
        from .geometry import _chaikin
        line = LS(_chaikin(p.points, 3)) if len(p.points) > 2 else LS(p.points)
    elif src is not None:
        g = src.geom
        line = g if g.geom_type == "LineString" else max(getattr(g, "geoms", [g]), key=lambda x: x.length)
        if line.geom_type != "LineString":
            line = line.exterior if hasattr(line, "exterior") else line
    else:
        raise RecipeError("path_label needs `points` or a line `src`")
    if p.offset:
        line = line.offset_curve(p.offset)
    fr = ctx.frame
    key = {"regular": False, "bold": True}.get(p.style, p.style)
    fpx = int(round(fr.px(p.size)))
    f = None
    for fn in FONT_FILES[key]:
        try:
            f = ImageFont.truetype(fn, max(fpx, 6))
            break
        except OSError:
            continue
    f = f or font(fpx)
    widths = [f.getlength(ch) / fr.scale * p.spacing for ch in p.text]
    total = sum(widths)
    L = line.length
    start = {"start": 0.0, "center": max((L - total) / 2, 0), "end": max(L - total, 0)}[p.align]
    # read left-to-right: flip the line if it runs westward
    a0, a1 = line.coords[0], line.coords[-1]
    if a1[0] < a0[0]:
        line = LS(list(line.coords)[::-1])
    col = resolve_color(ctx.style, p.color)
    try:
        hc = resolve_color(ctx.style, p.halo) if p.halo is not None else None
    except Exception:
        hc = resolve_color(ctx.style, "#efe6cf")
    pos = start
    hp = int(fr.px(p.halo_ft)) if hc is not None else 0
    for ch, w in zip(p.text, widths):
        mid = min(pos + w / 2, L)
        c = np.array(line.interpolate(mid).coords[0])
        a = np.array(line.interpolate(max(mid - w / 2, 0)).coords[0])
        b = np.array(line.interpolate(min(mid + w / 2, L)).coords[0])
        ang = np.degrees(np.arctan2(b[1] - a[1], b[0] - a[0]))
        if ch.strip():
            l, t, r, bt = f.getbbox(ch)
            pad = hp + 3
            img = PImage.new("L", (r - l + 2 * pad, bt - t + 2 * pad), 0)
            ImageDraw.Draw(img).text((pad - l, pad - t), ch, font=f, fill=255)
            rot = img.rotate(-ang, resample=PImage.BICUBIC, expand=True)
            if hc is not None and hp > 0:
                halo = rot.filter(ImageFilter.MaxFilter(hp * 2 + 1)).filter(ImageFilter.GaussianBlur(0.6))
                _place(into.data, np.asarray(halo, np.float32) / 255, c * fr.scale, hc, 0.85)
            _place(into.data, np.asarray(rot, np.float32) / 255, c * fr.scale, col)
        pos += w
