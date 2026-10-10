#!/usr/bin/env python3
"""Build the keyed palace maps for Oraga Night, 5e edition (review-fix task R4.1, owner QR5).

    python maps/build_maps.py            # all five SVGs and their PNG previews
    python maps/build_maps.py --no-png   # SVGs only
    python maps/build_maps.py --no-grid  # leave the 5-foot grid layer out

Every map is original drawing code: plain SVG strings, no external assets, no network. The
dimensions come from the `maps` block of ../facts.yaml (the O28 sizes, O33's elevations,
O34's terraces, card S3's gatehouse heights). Whatever the text does not fix is a drawing
choice, recorded in DECISIONS O53–O56 and O62; the maps themselves print no decision IDs and
no hedges, only one caption line each (R6.2, tools/test_maps.py).

Each measured shape declares the dimension it draws (`data-fact-w`, `data-fact-h`,
`data-fact-len`, in feet, keyed to facts.yaml), and tools/test_maps.py measures it back.
PNG previews are rasterized with ImageMagick `convert` (its internal renderer does not
read font-family lists, so the PNG copy names DejaVu Serif alone).

Plan coordinates are feet: x runs east, y runs north. The origin is the south-west corner
of the Crystal Court's floor, the main-doors wall is y = 0, and the dais end is y = 140.
Only east is given by the text ("the east doors", "the east wing"); the maps draw the dais
end at the top, as the old palace diagram did, and mark east alone.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
FACTS = HERE.parent / "facts.yaml"

FONT = "'DejaVu Serif', Georgia, 'Times New Roman', serif"
PNG_FONT = "DejaVu Serif"

INK = "#22201c"
WALL = "#2a2723"
SOFT = "#6b655c"
FLOOR = "#f6f1e6"
GALLERY = "#ebe1cb"
UPPER = "#e3d6ea"
GARDEN = "#e4ecd9"
GARDEN2 = "#d9e5cb"
GARDEN3 = "#cfdfbf"
LAWN = "#e9f0e1"
WATER = "#d5e3ec"
STREET = "#e7e4de"
GRID = "#b8b0a0"
STAIR = "#d8cfbd"
ACCENT = "#8c2f1f"
SERVICE = "#5b6f86"
CONTEXT = "#efede8"

REQUIRED = {
    "court": ["length", "width", "vault", "main_doors", "dais_high", "dais_across",
              "dais_from_doors", "gallery_rail", "east_stair_rise"],
    "terraces": ["count", "deep", "wide", "drop", "lower_garden"],
    "east_wing": ["floor", "cleared_corridor.wide", "cleared_corridor.long",
                  "inner_corridor.wide", "inner_corridor.long", "room_across.min",
                  "room_across.max"],
    "service_run": ["wide", "door"],
    "gatehouse": ["gate_walk_height", "walk_to_street_drop", "stair_fall", "wicket_wide",
                  "blades_out"],
}


def load_dims(path=FACTS) -> dict:
    """The `maps` block of facts.yaml, checked for every dimension the maps draw."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    dims = data.get("maps")
    if not isinstance(dims, dict):
        raise ValueError(f"{path}: needs a top-level 'maps' block (the map dimensions)")
    for group, keys in REQUIRED.items():
        for key in keys:
            node = dims.get(group)
            for part in key.split("."):
                if not isinstance(node, dict) or part not in node:
                    raise ValueError(f"{path}: maps block is missing {group}.{key}")
                node = node[part]
    return dims


# --------------------------------------------------------------------------- SVG writing

def n(v: float) -> str:
    """A number for an SVG attribute: at most two decimals, no trailing zeros."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def attrs(**kw) -> str:
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        k = k.rstrip("_").replace("_", "-")
        out.append(f'{k}="{n(v) if isinstance(v, (int, float)) else esc(str(v))}"')
    return " ".join(out)


class Svg:
    def __init__(self, width: int, height: int, scale: float):
        self.w, self.h, self.scale = width, height, scale
        self.parts: list[str] = []

    def add(self, s: str):
        self.parts.append(s)

    def open(self, **kw):
        self.add(f"<g {attrs(**kw)}>")

    def close(self):
        self.add("</g>")

    def rect(self, x, y, w, h, **kw):
        self.add(f"<rect {attrs(x=x, y=y, width=w, height=h, **kw)}/>")

    def line(self, x1, y1, x2, y2, **kw):
        self.add(f"<line {attrs(x1=x1, y1=y1, x2=x2, y2=y2, **kw)}/>")

    def poly(self, pts, **kw):
        p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        self.add(f"<polygon {attrs(points=p, **kw)}/>")

    def polyline(self, pts, **kw):
        p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        self.add(f"<polyline {attrs(points=p, fill='none', **kw)}/>")

    def circle(self, cx, cy, r, **kw):
        self.add(f"<circle {attrs(cx=cx, cy=cy, r=r, **kw)}/>")

    def text(self, x, y, s, size=11, anchor="start", weight=None, style=None, fill=INK,
             halo=False, **kw):
        base = dict(x=x, y=y, font_family=FONT, font_size=size, text_anchor=anchor,
                    font_weight=weight, font_style=style)
        if halo:
            self.add(f"<text {attrs(**base, fill='#ffffff', stroke='#ffffff', stroke_width=3, stroke_linejoin='round')}>{esc(s)}</text>")
        self.add(f"<text {attrs(**base, fill=fill, **kw)}>{esc(s)}</text>")

    def render(self, title: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" data-px-per-ft="{n(self.scale)}">\n'
                f"<title>{esc(title)}</title>\n")
        return head + "\n".join(self.parts) + "\n</svg>\n"


def wrap(s: str, width: int) -> list[str]:
    words, lines, cur = [w for w in s.split(" ") if w], [], ""   # NBSP holds "10 × 60" together
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def text_w(s: str, size: float) -> float:
    """Rough rendered width of DejaVu Serif text, for layout (bold runs wider)."""
    return len(s) * size * 0.6


def bold_w(s: str, size: float) -> float:
    return len(s) * size * 0.72


class Plan:
    """Feet to pixels for one plan view: x east, y north, north up."""

    def __init__(self, svg: Svg, ox, oy, x0, y1, scale):
        self.svg, self.ox, self.oy, self.x0, self.y1, self.s = svg, ox, oy, x0, y1, scale

    def X(self, x):
        return self.ox + (x - self.x0) * self.s

    def Y(self, y):
        return self.oy + (self.y1 - y) * self.s

    def rect(self, x, y, w, h, **kw):
        """A rectangle whose south-west corner is (x, y) in feet."""
        self.svg.rect(self.X(x), self.Y(y + h), w * self.s, h * self.s, **kw)

    def line(self, x1, y1, x2, y2, **kw):
        self.svg.line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), **kw)

    def text(self, x, y, s, **kw):
        self.svg.text(self.X(x), self.Y(y), s, **kw)

    def grid(self, x, y, w, h, step=5):
        if not getattr(self, "grid_on", True):
            return
        sv = self.svg
        k = step
        while k < w - 0.01:
            sv.line(self.X(x + k), self.Y(y), self.X(x + k), self.Y(y + h))
            k += step
        k = step
        while k < h - 0.01:
            sv.line(self.X(x), self.Y(y + k), self.X(x + w), self.Y(y + k))
            k += step

    # -- cartographic symbols --------------------------------------------------------

    def walls(self, pts, closed=True, width=2.2):
        p = [(self.X(x), self.Y(y)) for x, y in pts]
        if closed:
            self.svg.poly(p, fill="none", stroke=WALL, stroke_width=width, stroke_linejoin="miter")
        else:
            self.svg.polyline(p, stroke=WALL, stroke_width=width, stroke_linejoin="miter")

    def door(self, x, y, length, horizontal=True, fact=None, double=False, fill=FLOOR,
             label=None, **kw):
        """A door gap in a wall: a clear gap with two jamb ticks (and a leaf line)."""
        s = self.svg
        if horizontal:
            x1, y1, x2, y2 = self.X(x), self.Y(y), self.X(x + length), self.Y(y)
            s.line(x1, y1, x2, y2, stroke=fill, stroke_width=5)
            s.line(x1, y1 - 4, x1, y1 + 4, stroke=WALL, stroke_width=1.6)
            s.line(x2, y2 - 4, x2, y2 + 4, stroke=WALL, stroke_width=1.6)
        else:
            x1, y1, x2, y2 = self.X(x), self.Y(y), self.X(x), self.Y(y + length)
            s.line(x1, y1, x2, y2, stroke=fill, stroke_width=5)
            s.line(x1 - 4, y1, x1 + 4, y1, stroke=WALL, stroke_width=1.6)
            s.line(x2 - 4, y2, x2 + 4, y2, stroke=WALL, stroke_width=1.6)
        if double:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if horizontal:
                s.line(mx, my - 3, mx, my + 3, stroke=WALL, stroke_width=1)
            else:
                s.line(mx - 3, my, mx + 3, my, stroke=WALL, stroke_width=1)
        if fact:
            s.line(x1, y1, x2, y2, stroke="none", data_fact_len=fact, **kw)

    def stairs(self, x, y, w, h, up="n", treads=None, label=None, label_kw=None):
        """A flight of stairs in a w × h box (feet); `up` is the climbing direction."""
        self.rect(x, y, w, h, fill=STAIR, stroke=WALL, stroke_width=1)
        s, X, Y = self.svg, self.X, self.Y
        along_y = up in "ns"
        run = h if along_y else w
        count = treads or max(3, int(run / 1.5))
        for i in range(1, count):
            t = i / count
            if along_y:
                s.line(X(x), Y(y + h * t), X(x + w), Y(y + h * t), stroke=SOFT, stroke_width=0.6)
            else:
                s.line(X(x + w * t), Y(y), X(x + w * t), Y(y + h), stroke=SOFT, stroke_width=0.6)
        cx, cy = x + w / 2, y + h / 2
        if along_y:
            a, b = (cy - h * 0.38, cy + h * 0.38) if up == "n" else (cy + h * 0.38, cy - h * 0.38)
            s.line(X(cx), Y(a), X(cx), Y(b), stroke=INK, stroke_width=1.1)
            d = 1 if up == "n" else -1
            s.poly([(X(cx), Y(b)), (X(cx) - 3.5, Y(b) + 6 * d), (X(cx) + 3.5, Y(b) + 6 * d)], fill=INK)
        else:
            a, b = (cx - w * 0.38, cx + w * 0.38) if up == "e" else (cx + w * 0.38, cx - w * 0.38)
            s.line(X(a), Y(cy), X(b), Y(cy), stroke=INK, stroke_width=1.1)
            d = 1 if up == "e" else -1
            s.poly([(X(b), Y(cy)), (X(b) - 6 * d, Y(cy) - 3.5), (X(b) - 6 * d, Y(cy) + 3.5)], fill=INK)

    def rail(self, x1, y1, x2, y2):
        """A rail or balustrade: a fine double line with posts."""
        s = self.svg
        X1, Y1, X2, Y2 = self.X(x1), self.Y(y1), self.X(x2), self.Y(y2)
        s.line(X1, Y1, X2, Y2, stroke=WALL, stroke_width=3.2)
        s.line(X1, Y1, X2, Y2, stroke="#ffffff", stroke_width=1.4)
        s.line(X1, Y1, X2, Y2, stroke=WALL, stroke_width=0.5, stroke_dasharray="1 5")

    def tag(self, x, y, code, dx=0, dy=0):
        """A card marker (S1, S3 …): a small dark-red label."""
        s = self.svg
        X, Y = self.X(x) + dx, self.Y(y) + dy
        w = 8 + 7.2 * len(code)
        s.rect(X - w / 2, Y - 8, w, 16, rx=3, fill=ACCENT)
        s.text(X, Y + 4, code, size=10.5, anchor="middle", weight="bold", fill="#ffffff")

    def dim(self, x1, y1, x2, y2, label, fact=None, side=1, size=9.5, at=0.5):
        """A dimension line with end ticks and a label."""
        s = self.svg
        X1, Y1, X2, Y2 = self.X(x1), self.Y(y1), self.X(x2), self.Y(y2)
        s.line(X1, Y1, X2, Y2, stroke=SOFT, stroke_width=0.8, data_fact_len=fact)
        if abs(X2 - X1) > abs(Y2 - Y1):
            for X_ in (X1, X2):
                s.line(X_, Y1 - 4, X_, Y1 + 4, stroke=SOFT, stroke_width=0.8)
            s.text((X1 + X2) / 2, Y1 - 4 if side > 0 else Y1 + 12, label, size=size,
                   anchor="middle", style="italic", fill=SOFT, halo=True)
        else:
            for Y_ in (Y1, Y2):
                s.line(X1 - 4, Y_, X1 + 4, Y_, stroke=SOFT, stroke_width=0.8)
            mx, my = X1 + (6 if side > 0 else -6), Y1 + (Y2 - Y1) * at + 3
            for i, ln in enumerate(label.split("\n")):
                s.text(mx, my + 12 * i, ln, size=size, anchor="start" if side > 0 else "end",
                       style="italic", fill=SOFT, halo=True)


# --------------------------------------------------------------------------- frame

LEGEND_W = 250
TOP = 74
PAD = 22


def frame(svg: Svg, title: str, subtitle: str, legend: list[tuple], caption: list[str],
          map_w: int, scale_ft=None, scale=None, map_h=None, east=True, key=None):
    """Border, title cartouche, legend, scale bar, east mark and caption."""
    W, H = svg.w, svg.h
    s = svg
    # border
    s.rect(6, 6, W - 12, H - 12, fill="none", stroke=INK, stroke_width=1.2)
    s.rect(10, 10, W - 20, H - 20, fill="none", stroke=INK, stroke_width=0.5)
    # title cartouche
    s.open(id="title")
    tw = max(text_w(title, 17), text_w(subtitle, 11)) + 40
    tx = (map_w + PAD * 2) / 2
    s.rect(tx - tw / 2, 18, tw, 46, fill="#ffffff", stroke=INK, stroke_width=1)
    s.rect(tx - tw / 2 + 3, 21, tw - 6, 40, fill="none", stroke=INK, stroke_width=0.4)
    s.text(tx, 40, title, size=17, anchor="middle", weight="bold")
    s.text(tx, 56, subtitle, size=11, anchor="middle", style="italic", fill=SOFT)
    s.close()
    # legend column
    lx = map_w + PAD * 2
    s.open(id="legend")
    s.rect(lx, 18, LEGEND_W - 12, H - 36, fill="#ffffff", stroke=INK, stroke_width=0.8)
    y = 40
    s.text(lx + 14, y, "Legend", size=13, weight="bold")
    y += 8
    for item in legend:
        kind, label = item[0], item[1]
        y += 20
        sx = lx + 14
        if kind == "wall":
            s.line(sx, y - 4, sx + 26, y - 4, stroke=WALL, stroke_width=2.2)
        elif kind == "door":
            s.line(sx, y - 4, sx + 26, y - 4, stroke=WALL, stroke_width=2.2)
            s.line(sx + 8, y - 4, sx + 18, y - 4, stroke="#ffffff", stroke_width=5)
            s.line(sx + 8, y - 8, sx + 8, y, stroke=WALL, stroke_width=1.4)
            s.line(sx + 18, y - 8, sx + 18, y, stroke=WALL, stroke_width=1.4)
        elif kind == "stairs":
            s.rect(sx, y - 11, 26, 13, fill=STAIR, stroke=WALL, stroke_width=0.8)
            for i in range(1, 6):
                s.line(sx + i * 26 / 6, y - 11, sx + i * 26 / 6, y + 2, stroke=SOFT, stroke_width=0.5)
            s.line(sx + 4, y - 4.5, sx + 20, y - 4.5, stroke=INK, stroke_width=1)
            s.poly([(sx + 23, y - 4.5), (sx + 18, y - 7.5), (sx + 18, y - 1.5)], fill=INK)
        elif kind == "rail":
            s.line(sx, y - 4, sx + 26, y - 4, stroke=WALL, stroke_width=3.2)
            s.line(sx, y - 4, sx + 26, y - 4, stroke="#ffffff", stroke_width=1.4)
            s.line(sx, y - 4, sx + 26, y - 4, stroke=WALL, stroke_width=0.5, stroke_dasharray="1 5")
        elif kind == "service":
            s.line(sx, y - 4, sx + 26, y - 4, stroke=SERVICE, stroke_width=2, stroke_dasharray="5 3")
        elif kind == "above":
            s.rect(sx, y - 11, 26, 13, fill="none", stroke=INK, stroke_width=1, stroke_dasharray="4 2")
        elif kind == "fill":
            s.rect(sx, y - 11, 26, 13, fill=item[2], stroke=WALL, stroke_width=0.6,
                   stroke_dasharray=item[3] if len(item) > 3 else None)
        elif kind == "grid":
            s.rect(sx, y - 11, 26, 13, fill=FLOOR, stroke=WALL, stroke_width=0.6)
            for i in (1, 2, 3, 4):
                s.line(sx + i * 5.2, y - 11, sx + i * 5.2, y + 2, stroke=GRID, stroke_width=0.5)
            s.line(sx, y - 4.5, sx + 26, y - 4.5, stroke=GRID, stroke_width=0.5)
        elif kind == "tag":
            s.rect(sx, y - 12, 26, 15, rx=3, fill=ACCENT)
            s.text(sx + 13, y - 1, "S#", size=9.5, anchor="middle", weight="bold", fill="#ffffff")
        elif kind == "figure":
            s.circle(sx + 13, y - 4.5, 4.5, fill="#ffffff", stroke=ACCENT, stroke_width=1.6)
        elif kind == "dim":
            s.line(sx, y - 4, sx + 26, y - 4, stroke=SOFT, stroke_width=0.8)
            s.line(sx, y - 8, sx, y, stroke=SOFT, stroke_width=0.8)
            s.line(sx + 26, y - 8, sx + 26, y, stroke=SOFT, stroke_width=0.8)
        lines = wrap(label, 27)
        for i, ln in enumerate(lines):
            s.text(sx + 36, y + i * 13, ln, size=10.5)
        y += 13 * (len(lines) - 1)
    if key:
        y += 30
        s.text(lx + 14, y, "Key", size=13, weight="bold")
        y += 4
        for code, label in key:
            y += 17
            s.text(lx + 14, y, code, size=10.5, weight="bold")
            lines = wrap(label, 28)
            for i, ln in enumerate(lines):
                s.text(lx + 50, y + i * 13, ln, size=10.5)
            y += 13 * (len(lines) - 1)
    s.close()
    # caption, wrapped to the map's width
    caption = wrap(" ".join(caption), int((map_w + PAD) / (10.5 * 0.53)))
    s.open(id="caption")
    cy = H - 22 - 14 * (len(caption) - 1)
    for i, ln in enumerate(caption):
        s.text(PAD + 6, cy + 14 * i, ln, size=10.5, style="italic", fill=SOFT)
    s.close()
    # scale bar
    if scale_ft:
        s.open(id="scalebar")
        bx, by = PAD + 10, H - 40 - 14 * len(caption)
        seg = scale_ft / 5
        for i in range(5):
            s.rect(bx + i * seg * scale, by, seg * scale, 6,
                   fill=INK if i % 2 == 0 else "#ffffff", stroke=INK, stroke_width=0.6)
        s.rect(bx, by, scale_ft * scale, 6, fill="none", stroke=INK, stroke_width=0.6,
               id="scalebar-span", data_fact_w=str(scale_ft))
        for i in (0, 5):
            s.text(bx + i * seg * scale, by - 4, f"{int(i * seg)}", size=9.5, anchor="middle")
        s.text(bx + scale_ft * scale + 8, by + 6, "feet  (one grid square = 5 feet)", size=9.5)
        s.close()
    if east:
        s.open(id="orientation")
        ex, ey = map_w + PAD * 2 - 70, TOP + 24
        s.line(ex, ey, ex + 36, ey, stroke=INK, stroke_width=1.4)
        s.poly([(ex + 44, ey), (ex + 34, ey - 5), (ex + 34, ey + 5)], fill=INK)
        s.text(ex + 22, ey - 9, "E", size=12, anchor="middle", weight="bold")
        s.close()


# --------------------------------------------------------------------------- shared plan

def geometry(d: dict) -> dict:
    """The one palace layout maps VIII–3 to VIII–5 share (feet; see the module docstring)."""
    c, t, w, sr = d["court"], d["terraces"], d["east_wing"], d["service_run"]
    G = {}
    G["W"], G["L"] = c["width"], c["length"]
    G["gw"] = (t["wide"] - c["width"]) / 2           # gallery depth: Court + galleries = terrace width (O54)
    G["walk"] = 10                                   # the garden walk's depth (O54, approximate)
    G["dais"] = (c["width"] / 2 - c["dais_across"] / 2, c["dais_from_doors"], c["dais_across"], 15)
    G["east_door_y"] = 30                            # the east doors' south jamb (O54)
    G["east_door_w"] = 10
    G["stair_run"] = 24                              # 12 feet up at a comfortable pitch
    gx = c["width"] + G["gw"]                        # the east gallery's outer wall
    G["gx"] = gx
    cc, ic = w["cleared_corridor"], w["inner_corridor"]
    G["stair"] = (gx, G["east_door_y"], cc["wide"], G["stair_run"])
    y0 = G["east_door_y"] + G["stair_run"]
    G["cleared"] = (gx, y0, cc["wide"], cc["long"])
    G["inner"] = (gx, y0 + cc["long"], ic["wide"], ic["long"])
    G["room_w"] = 25                                  # within O28's 20–30 feet (O55)
    G["terr0"] = c["length"] + G["walk"]
    G["sr"] = sr["wide"]
    return G


# --------------------------------------------------------------------------- map VIII–2

def map_gatehouse(d: dict, grid=True) -> str:
    g = d["gatehouse"]
    scale = 6
    x0, x1, y0, y1 = -14, 74, -32, 66
    mw, mh = int((x1 - x0) * scale), int((y1 - y0) * scale)
    sec_h = 200
    W, H = mw + PAD * 2 + LEGEND_W, TOP + mh + sec_h + 120
    svg = Svg(W, H, scale)
    svg.rect(0, 0, W, H, fill="#ffffff")
    P = Plan(svg, PAD, TOP + 10, x0, y1, scale)
    P.grid_on = grid

    # ground: street, gatehouse, court
    P.rect(x0, y0, x1 - x0, -y0, fill=STREET)
    P.text(x0 + 2, -27, "B0  GATE STREET", size=12, weight="bold", fill=SOFT)
    P.text(x0 + 2, -30.5, "the hill, and the line", size=9.5, style="italic", fill=SOFT)
    court = (0, 15, 60, 45)
    P.rect(*court, fill=FLOOR)
    P.rect(10, 0, 40, 15, fill="#ece6d8")
    P.rect(22.5, 0, 15, 15, fill=FLOOR)                         # the arch passage
    if grid:
        svg.open(id="grid", stroke=GRID, stroke_width=0.5, opacity=0.8)
        P.grid(*court)
        P.grid(22.5, 0, 15, 15)
        P.grid(x0, y0, x1 - x0, -y0)
        svg.close()

    # walls
    P.walls([(0, 15), (0, 60), (60, 60), (60, 15)], closed=False)
    P.walls([(0, 15), (10, 15)], closed=False)
    P.walls([(50, 15), (60, 15)], closed=False)
    P.walls([(10, 0), (10, 15), (22.5, 15), (22.5, 0), (10, 0)], closed=False)     # the cell
    P.walls([(37.5, 0), (37.5, 15), (50, 15), (50, 0), (37.5, 0)], closed=False)   # stair tower
    # the gate: two leaves on the street face, the wicket in the leaf on the court's left
    svg.open(id="gate")
    P.line(22.5, 0.6, 30, 0.6, stroke=WALL, stroke_width=3)
    P.line(30, 0.6, 37.5, 0.6, stroke=WALL, stroke_width=3)
    P.line(30, -0.6, 30, 1.8, stroke="#ffffff", stroke_width=1)
    P.line(31.25, 0.6, 36.25, 0.6, stroke=ACCENT, stroke_width=3)
    P.line(31.25, 0.6, 36.25, 0.6, stroke="none", data_fact_len="gatehouse.wicket_wide")
    P.line(21, -1.2, 39, -1.2, stroke=INK, stroke_width=2.2, stroke_linecap="round")    # the bar
    svg.close()
    P.text(30, 4.0, "the arch", size=9.5, anchor="middle", style="italic", fill=SOFT)
    P.text(16.25, 8.8, "the cell", size=10, anchor="middle", style="italic")
    # doors from the court
    P.door(14, 15, 4, fill="#ece6d8")
    P.door(44, 15, 4, fill="#ece6d8")
    # the court-side stair: a dog-leg with a landing 5 feet up (O53)
    P.stairs(44.5, 4.5, 5, 10, up="s")
    P.rect(38, 1, 11.5, 3.5, fill=STAIR, stroke=WALL, stroke_width=1)
    P.stairs(38.5, 4.5, 5, 10, up="n")
    P.text(43.75, 2.1, "landing, 5 ft", size=7.5, anchor="middle", style="italic", fill=SOFT)
    # the outer stair down to the street
    P.stairs(11, -5, 11, 4.5, up="e")
    # the gate-walk above
    P.rect(10, 0, 40, 15, fill="none", stroke=INK, stroke_width=1, stroke_dasharray="5 3")
    # main doors into the Crystal Court
    P.door(25, 60, 10, double=True, fill=FLOOR)
    P.rect(5, 60.4, 50, 5.6, fill=CONTEXT)
    P.text(30, 62.8, "B2, the Crystal Court (map VIII–3)", size=9.5, anchor="middle",
           style="italic", fill=SOFT)

    # labels
    P.text(30, 44, "B1  THE GATEHOUSE COURT", size=13, anchor="middle", weight="bold", halo=True)
    P.text(30, 40, "B12 after midnight, held", size=10.5, anchor="middle", style="italic", halo=True)
    P.text(30, 34.5, "the court's crystal wall, lit (S3)", size=9.5, anchor="middle",
           style="italic", fill=SOFT, halo=True)
    P.text(30, 56.8, "main doors (10 ft)", size=9.5, anchor="middle", style="italic", halo=True)
    P.text(52, 31, "gatehouse stair", size=9.5, anchor="middle", style="italic", halo=True)
    P.text(52, 28.5, "door; up to the walk", size=9.5, anchor="middle", style="italic", halo=True)
    P.line(52, 27, 47, 15.5, stroke=SOFT, stroke_width=0.7)
    P.text(52, 12.5, "gate-walk above,", size=9.5, style="italic", halo=True)
    P.text(52, 10.2, "15 ft up, over the", size=9.5, style="italic", halo=True,
           data_fact="gatehouse.gate_walk_height")
    P.text(52, 7.9, "arch (dashed)", size=9.5, style="italic", halo=True)
    P.text(30, 17.4, "fourth Blade, on the walk above", size=9.5, anchor="middle", style="italic", halo=True)
    P.line(30, 16.6, 30, 9.9, stroke=SOFT, stroke_width=0.7)
    P.text(-12.5, -4.0, "outer stair,", size=9.5, style="italic", halo=True)
    P.text(-12.5, -6.3, "walk to street", size=9.5, style="italic", halo=True)
    P.text(41, -3.0, "the bar (street side)", size=9.5, style="italic", halo=True)
    P.text(30, -15, "wicket: 5 ft, in the leaf on the court's left", size=9.5, anchor="middle",
           style="italic", halo=True)
    P.line(33.75, -13.5, 33.75, -0.6, stroke=SOFT, stroke_width=0.7)
    # the Bought at midnight (S3: "Where the Bought stand")
    svg.open(id="bought")
    for bx in (18, 30, 42):
        P.svg.circle(P.X(bx), P.Y(-g["blades_out"]), 5, fill="#ffffff", stroke=ACCENT, stroke_width=1.8)
    P.svg.circle(P.X(34), P.Y(-2.8), 5, fill=ACCENT, stroke=ACCENT, stroke_width=1.8)
    P.svg.circle(P.X(30), P.Y(9), 5, fill="#ffffff", stroke=ACCENT, stroke_width=1.8,
                 stroke_dasharray="2 1.5")
    svg.close()
    P.text(46, -10.8, "three Blades, 10 ft out", size=9.5, style="italic", halo=True)
    P.text(46, -13.1, "across Gate Street", size=9.5, style="italic", halo=True)
    P.text(36, -6.2, "the sergeant, at the wicket", size=9.5, style="italic", halo=True)
    P.dim(24, 0, 24, -g["blades_out"], "10 ft", fact="gatehouse.blades_out")
    P.tag(30, 24, "S3")

    # section through the gatehouse (elevation), cut through the stair tower
    ss = 5
    sx0, sy0 = PAD + 30, TOP + 10 + mh + 34
    svg.open(id="section", data_px_per_ft=n(ss))
    svg.text(sx0 - 10, sy0, "Section through the gatehouse, looking west (heights from card S3)",
             size=11, weight="bold")
    base = sy0 + 26 * ss                              # street and court level

    def SX(ft):
        return sx0 + (ft + 26) * ss

    def SY(ft):
        return base - ft * ss

    svg.rect(SX(-26), SY(0), 26 * ss, 3 * ss, fill=STREET)
    svg.rect(SX(15), SY(0), 45 * ss, 3 * ss, fill=FLOOR)
    svg.line(SX(-26), SY(0), SX(60), SY(0), stroke=WALL, stroke_width=1.6)
    svg.text(SX(-25), SY(0) + 12, "Gate Street", size=9.5, style="italic", fill=SOFT)
    svg.text(SX(59), SY(0) + 12, "the Gatehouse Court", size=9.5, anchor="end", style="italic", fill=SOFT)
    hw = g["gate_walk_height"]
    svg.rect(SX(0), SY(hw), 15 * ss, hw * ss, fill="#ece6d8", stroke=WALL, stroke_width=1.2)
    svg.polyline([(SX(0), SY(hw)), (SX(0), SY(hw + 3.5)), (SX(15), SY(hw + 3.5)), (SX(15), SY(hw))],
                 stroke=WALL, stroke_width=0.8, stroke_dasharray="3 2")
    svg.text(SX(7.5), SY(hw + 3.5) - 5, "the gate-walk", size=9.5, anchor="middle", style="italic")
    # the dog-leg inside the tower: door → lower flight → landing at 5 ft → upper flight → walk
    svg.polyline([(SX(15), SY(0)), (SX(5), SY(5)), (SX(1.5), SY(5))], stroke=WALL, stroke_width=1.6)
    svg.polyline([(SX(5), SY(5)), (SX(15), SY(hw))], stroke=WALL, stroke_width=1.6,
                 stroke_dasharray="5 2")
    # the measures
    svg.line(SX(-7), SY(hw), SX(-7), SY(0), stroke=SOFT, stroke_width=0.9,
             data_fact_len="gatehouse.walk_to_street_drop", data_px_per_ft=n(ss))
    svg.line(SX(-7), SY(hw), SX(0), SY(hw), stroke=SOFT, stroke_width=0.6, stroke_dasharray="2 2")
    svg.text(SX(-8), SY(hw / 2) + 3, "15-ft drop from the walk", size=9.5, anchor="end",
             style="italic", fill=SOFT)
    svg.text(SX(-8), SY(hw / 2) + 15, "to the street", size=9.5, anchor="end", style="italic", fill=SOFT)
    svg.line(SX(17), SY(hw), SX(17), SY(0), stroke=SOFT, stroke_width=0.9,
             data_fact_len="gatehouse.gate_walk_height", data_px_per_ft=n(ss))
    svg.text(SX(18), SY(1.5), "walk 15 ft up", size=9.5, style="italic", fill=SOFT)
    svg.line(SX(21), SY(hw), SX(21), SY(5), stroke=ACCENT, stroke_width=1.2,
             data_fact_len="gatehouse.stair_fall", data_px_per_ft=n(ss))
    svg.line(SX(15), SY(hw), SX(21), SY(hw), stroke=ACCENT, stroke_width=0.6, stroke_dasharray="2 2")
    svg.line(SX(5), SY(5), SX(21), SY(5), stroke=ACCENT, stroke_width=0.6, stroke_dasharray="2 2")
    svg.text(SX(22), SY(11), "shoved from the top:", size=9.5, style="italic", fill=ACCENT)
    svg.text(SX(22), SY(11) + 13, "falls 10 ft to the landing, 5 ft up", size=9.5, style="italic", fill=ACCENT)
    svg.line(SX(0), SY(0), SX(0), SY(9), stroke=ACCENT, stroke_width=2.6)
    svg.text(SX(0.8), SY(8), "gate", size=9, style="italic", fill=ACCENT)
    svg.close()

    legend = [("wall", "Wall"), ("door", "Door or doorway"), ("stairs", "Stairs (arrow points up)"),
              ("above", "Gate-walk, overhead (15 ft)"), ("grid", "5-foot grid"),
              ("figure", "A Bought Blade at midnight (S3)"), ("tag", "Fight card (chapter IX)"),
              ("dim", "Measured distance")]
    key = [("B0", "Gate Street, the street and the line"),
           ("B1", "The Gatehouse Court (chapter IV)"),
           ("B12", "The same court after midnight, held (chapter V; card S3)")]
    caption = ["Heights, the wicket and the Bought's posts from card S3; other positions approximate."]
    frame(svg, "Map VIII–2: The Gatehouse Court", "B0 · B1 · B12 — the outer gate, the wicket and the gate-walk",
          legend, caption, mw, scale_ft=20, scale=scale, key=key)
    return svg.render("Map VIII–2: The Gatehouse Court")


# --------------------------------------------------------------------------- map VIII–3

def map_court(d: dict, grid=True) -> str:
    c = d["court"]
    G = geometry(d)
    W_, L, gw, gx = G["W"], G["L"], G["gw"], G["gx"]
    scale = 4
    x0, x1, y0, y1 = -gw - 26, gx + 36, -12, L + G["walk"] + 14
    mw, mh = int((x1 - x0) * scale), int((y1 - y0) * scale)
    W, H = mw + PAD * 2 + LEGEND_W, TOP + mh + 124
    svg = Svg(W, H, scale)
    svg.rect(0, 0, W, H, fill="#ffffff")
    P = Plan(svg, PAD, TOP + 10, x0, y1, scale)
    P.grid_on = grid

    # floors
    P.rect(-gw, L, gw * 2 + W_, G["walk"], fill=GARDEN)              # garden walk
    P.rect(-gw, L + G["walk"], gw * 2 + W_, y1 - L - G["walk"], fill=GARDEN2, opacity=0.6)
    P.rect(-gw, 0, gw, L, fill=GALLERY)
    P.rect(W_, 0, gw, L, fill=GALLERY)
    P.rect(0, 0, W_, L, fill=FLOOR, id="court-floor", data_fact_w="court.width",
           data_fact_h="court.length")
    sx, sy, sw, sh = G["stair"]
    P.rect(W_, G["east_door_y"], gw, G["east_door_w"], fill=FLOOR)    # passage under the gallery
    if grid:
        svg.open(id="grid", stroke=GRID, stroke_width=0.5, opacity=0.8)
        P.grid(0, 0, W_, L)
        P.grid(-gw, 0, gw, L)
        P.grid(W_, 0, gw, L)
        P.grid(-gw, L, gw * 2 + W_, G["walk"])
        svg.close()
    # the dais
    dx, dy, dw, dh = G["dais"]
    P.rect(dx, dy, dw, dh, fill="#e2d3b4", stroke=WALL, stroke_width=1.2, id="dais",
           data_fact_w="court.dais_across")
    P.rect(dx + 5, dy + 8, dw - 10, 3.5, fill="#c9b48c", stroke=WALL, stroke_width=0.6)
    P.text(W_ / 2, dy + 4.2, "the dais, 3 ft high", size=10, anchor="middle", style="italic",
           data_fact="court.dais_high")
    P.text(W_ / 2, dy + 12.6, "high table", size=8.5, anchor="middle", style="italic", fill=SOFT)

    # walls: outer shell of Court + galleries
    P.walls([(-gw, 0), (-gw, L), (gx, L), (gx, 0), (-gw, 0)], closed=False)
    P.walls([(gx, G["east_door_y"] + G["east_door_w"]), (gx, 0)], closed=False)
    # the rails along the Court's long sides, 12 ft up
    P.rail(0, 0.5, 0, L - 0.5)
    P.rail(W_, 0.5, W_, G["east_door_y"])
    P.rail(W_, G["east_door_y"] + G["east_door_w"], W_, L - 0.5)
    # the passage under the east gallery, to the stair
    P.line(W_, G["east_door_y"], gx, G["east_door_y"], stroke=WALL, stroke_width=1.4)
    P.line(W_, G["east_door_y"] + G["east_door_w"], gx, G["east_door_y"] + G["east_door_w"],
           stroke=WALL, stroke_width=1.4)
    P.door(W_, G["east_door_y"], G["east_door_w"], horizontal=False, double=True)
    # the stair up to gallery level, and the start of the cleared corridor
    P.walls([(sx, sy), (sx + sw, sy), (sx + sw, sy + sh + 18), (sx, sy + sh + 18), (sx, sy + G["east_door_w"])],
            closed=False)
    P.rect(sx, sy + sh, sw, 18, fill=UPPER)
    P.stairs(sx, sy, sw, sh, up="n")
    P.door(sx, sy, G["east_door_w"], horizontal=False, fill=FLOOR)
    # main doors, garden doors, west doors
    P.door(W_ / 2 - c["main_doors"] / 2, 0, c["main_doors"], double=True, fact="court.main_doors")
    P.door(8, L, 10, double=True, fill=GARDEN)
    P.door(W_ - 18, L, 10, double=True, fill=GARDEN)
    P.door(-gw, 96, 5, horizontal=False, fill=GALLERY, fact="service_run.door")
    P.door(-gw, 56, 10, horizontal=False, double=True, fill=GALLERY)
    # the garden walk's rail
    P.rail(-gw, L + G["walk"], gx, L + G["walk"])

    # labels
    P.text(W_ / 2, 72, "B2", size=22, anchor="middle", weight="bold", halo=True)
    P.text(W_ / 2, 66, "THE CRYSTAL COURT", size=12.5, anchor="middle", weight="bold", halo=True)
    P.text(W_ / 2, 61.5, "ground level · about 140 × 80 ft", size=10, anchor="middle",
           style="italic", halo=True)
    P.text(W_ / 2, 57.5, "vault some 50 ft high", size=10, anchor="middle", style="italic",
           halo=True, data_fact="court.vault")
    P.text(W_ / 2, 45, "the Dance", size=10, anchor="middle", style="italic", fill=SOFT, halo=True)
    for gxm, side in ((-gw / 2, "west"), (W_ + gw / 2, "east")):
        P.text(gxm, 80, "B3", size=18, anchor="middle", weight="bold", halo=True)
        for i, ln in enumerate(["banquet", "gallery", f"({side})", "", "gallery", "level,", "12 ft up"]):
            P.text(gxm, 75 - 3.6 * i, ln, size=10, anchor="middle",
                   style="italic" if i > 3 else None, weight="bold" if i < 3 else None, halo=True)
    P.text(1.2, 108, "rail 12 ft", size=9, style="italic", halo=True, data_fact="court.gallery_rail")
    P.text(1.2, 105.5, "above the floor", size=9, style="italic", halo=True)
    P.text(W_ / 2, -4.5, "main doors (10 ft)", size=10, anchor="middle", style="italic")
    P.text(W_ / 2, -8.2, "to B1, the Gatehouse Court (map VIII–2)", size=9.5, anchor="middle",
           style="italic", fill=SOFT)
    P.text(W_ - 2, G["east_door_y"] + G["east_door_w"] / 2 + 6.5, "east doors", size=9.5,
           anchor="end", style="italic", halo=True)
    P.text(sx + sw + 1.5, sy + 8, "stair up", size=9.5, style="italic", halo=True)
    P.text(sx + sw + 1.5, sy + 5.5, "12 ft to", size=9.5, style="italic", halo=True,
           data_fact="court.east_stair_rise")
    P.text(sx + sw + 1.5, sy + 3, "gallery level", size=9.5, style="italic", halo=True)
    P.text(sx + sw + 1.5, sy + sh + 12, "cleared", size=9.5, style="italic", halo=True)
    P.text(sx + sw + 1.5, sy + sh + 9.5, "corridor to", size=9.5, style="italic", halo=True)
    P.text(sx + sw + 1.5, sy + sh + 7, "B9 (map VIII–5)", size=9.5, style="italic", halo=True)
    P.text(W_ / 2, L + 4, "garden walk (railed)", size=10, anchor="middle", style="italic", halo=True)
    P.text(W_ / 2, L + G["walk"] + 6, "the upper terrace, below the rail (map VIII–4)", size=9.5,
           anchor="middle", style="italic", fill=SOFT, halo=True)
    P.text(4, L - 2.6, "garden doors", size=9, style="italic", halo=True)
    P.text(-gw - 1.5, 101.5, "service door,", size=9, anchor="end", style="italic", halo=True)
    P.text(-gw - 1.5, 99, "5 ft, to B10", size=9, anchor="end", style="italic", halo=True)
    P.text(-gw - 1.5, 62.5, "to B4, the", size=9, anchor="end", style="italic", halo=True)
    P.text(-gw - 1.5, 60, "Audience Hall", size=9, anchor="end", style="italic", halo=True)
    P.dim(W_ - 5, 0, W_ - 5, c["dais_from_doors"], "about 120 ft,\ndoors to dais",
          fact="court.dais_from_doors", side=-1, at=0.8)
    P.tag(W_ + gw / 2, 18, "S1")
    P.tag(-gw / 2, 26, "S1")
    P.tag(-gw - 6, 92, "S11")
    P.tag(-gw / 2, 120, "S13")
    P.tag(W_ + gw / 2, 120, "S12")

    legend = [("wall", "Wall"), ("door", "Door or doorway"), ("stairs", "Stairs (arrow points up)"),
              ("rail", "Rail, 12 ft above the Court floor"), ("fill", "Ground level", FLOOR),
              ("fill", "Gallery level, 12 ft up", GALLERY), ("fill", "Corridor at gallery level", UPPER),
              ("fill", "Garden walk (ground level)", GARDEN), ("grid", "5-foot grid"),
              ("tag", "Fight card (chapter IX)"), ("dim", "Measured distance")]
    key = [("B2", "The Crystal Court"), ("B3", "The banquet galleries, along both long sides"),
           ("S1", "The seating feud, in either gallery"),
           ("S11", "The one open door at midnight"),
           ("S12", "The minister in the smoke"), ("S13", "The arrest in the fire")]
    caption = ["Distances from chapter V; other positions approximate."]
    frame(svg, "Map VIII–3: The Crystal Court", "B2 · B3 — the Court, the banquet galleries and the east doors",
          legend, caption, mw, scale_ft=50, scale=scale, key=key)
    return svg.render("Map VIII–3: The Crystal Court")


# --------------------------------------------------------------------------- map VIII–4

def map_terraces(d: dict, grid=True) -> str:
    t = d["terraces"]
    G = geometry(d)
    W_, L, gw, gx = G["W"], G["L"], G["gw"], G["gx"]
    scale = 2.4
    lo = G["terr0"] + t["count"] * t["deep"]
    gate_y = lo + t["lower_garden"]
    ix, iy, iw, ih = G["inner"]
    wing_top = iy + ih
    x0, x1, y0, y1 = -gw - 36, gx + 40, L - 12, gate_y + 22
    mw, mh = int((x1 - x0) * scale), int((y1 - y0) * scale)
    prof_h = 150
    W, H = mw + PAD * 2 + LEGEND_W, TOP + mh + prof_h + 110
    svg = Svg(W, H, scale)
    svg.rect(0, 0, W, H, fill="#ffffff")
    P = Plan(svg, PAD, TOP + 10, x0, y1, scale)
    P.grid_on = grid

    # context: the Court's end and the east wing
    P.rect(-gw, y0, gw * 2 + W_, L - y0, fill=CONTEXT)
    P.text(W_ / 2, L - 7, "B2, the Crystal Court (map VIII–3)", size=9.5, anchor="middle",
           style="italic", fill=SOFT)
    P.rect(gx, y0, x1 - gx, wing_top - y0, fill=CONTEXT)
    P.walls([(gx, y0), (gx, wing_top), (x1, wing_top)], closed=False, width=1.2)
    P.text(gx + 4, wing_top - 12, "B9, the", size=9.5, style="italic", fill=SOFT)
    P.text(gx + 4, wing_top - 17, "east wing,", size=9.5, style="italic", fill=SOFT)
    P.text(gx + 4, wing_top - 22, "12 ft up", size=9.5, style="italic", fill=SOFT)
    P.text(gx + 4, wing_top - 27, "(map VIII–5)", size=9.5, style="italic", fill=SOFT)
    # the garden walk, the terraces, the lower garden, the river
    P.rect(-gw, L, t["wide"], G["walk"], fill=GARDEN)
    tints = [GARDEN, GARDEN2, GARDEN3]
    for k in range(t["count"]):
        ty = G["terr0"] + k * t["deep"]
        P.rect(-gw, ty, t["wide"], t["deep"], fill=tints[k % 3], id=f"terrace-{k + 1}",
               data_fact_w="terraces.wide", data_fact_h="terraces.deep")
    P.rect(-gw, lo, t["wide"], t["lower_garden"], fill=LAWN, id="lower-garden",
           data_fact_h="terraces.lower_garden")
    P.rect(x0, gate_y, x1 - x0, y1 - gate_y, fill=WATER)
    if grid:
        svg.open(id="grid", stroke=GRID, stroke_width=0.4, opacity=0.7)
        for k in range(t["count"]):
            P.grid(-gw, G["terr0"] + k * t["deep"], t["wide"], t["deep"])
        P.grid(-gw, L, t["wide"], G["walk"])
        svg.close()
    # walls and balustrades
    P.walls([(-gw, L), (gx, L)], closed=False)
    P.rail(-gw, L + G["walk"], gx, L + G["walk"])
    for k in range(t["count"]):
        P.rail(-gw, G["terr0"] + (k + 1) * t["deep"], gx, G["terr0"] + (k + 1) * t["deep"])
    P.walls([(-gw, L), (-gw, gate_y), (gx, gate_y), (gx, wing_top)], closed=False, width=1.6)
    P.door(8, L, 10, double=True, fill=GARDEN)
    P.door(W_ - 18, L, 10, double=True, fill=GARDEN)
    # the river gate, in the far wall
    P.line(W_ / 2 - 5, gate_y, W_ / 2 + 5, gate_y, stroke=ACCENT, stroke_width=3.2)
    # a stair at either end of each terrace (down to the next), and the flights from the walk
    for k in range(t["count"] + 1):
        edge = L + G["walk"] if k == 0 else G["terr0"] + k * t["deep"]
        for sx in (-gw + 1.5, gx - 16):
            P.stairs(sx, edge, 6, 12, up="s", treads=7)
    # the garden stair, down the wing's west wall to the upper terrace (O33, O55)
    P.stairs(gx - 7, G["terr0"] + 14, 6, wing_top - G["terr0"] - 16, up="n", treads=18)

    # labels
    P.text(2, L + 3.3, "garden walk (ground level), railed", size=9.5, style="italic", halo=True)
    names = ["the upper terrace", "the second terrace", "the third terrace"]
    for k in range(t["count"]):
        ty = G["terr0"] + k * t["deep"]
        P.text(W_ / 2 - 6, ty + t["deep"] / 2 + 2, names[k], size=11, anchor="middle", weight="bold", halo=True)
        sub = ("below the walk's rail" if k == 0 else "10 ft below the one above")
        P.text(W_ / 2 - 6, ty + t["deep"] / 2 - 4, sub, size=9.5, anchor="middle", style="italic", halo=True,
               data_fact="terraces.drop" if k == 1 else None)
    P.text(W_ / 2, lo + 84, "B5", size=20, anchor="middle", weight="bold", halo=True)
    P.text(W_ / 2, lo + 76, "THE LOWER GARDEN", size=12, anchor="middle", weight="bold", halo=True)
    P.text(W_ / 2, lo + 69, "about 150 ft to the river gate", size=9.5, anchor="middle",
           style="italic", halo=True, data_fact="terraces.lower_garden")
    P.text(W_ / 2, gate_y + 5, "the river gate (locked; Agenda 6)", size=9.5, anchor="middle",
           style="italic", halo=True)
    P.text(W_ / 2, gate_y + 14, "THE RIVER WALK, AND THE RIVER", size=10.5, anchor="middle",
           weight="bold", fill=SOFT)
    P.text(gx - 9, G["terr0"] + 33, "the garden", size=9, anchor="end", style="italic", halo=True)
    P.text(gx - 9, G["terr0"] + 29, "stair, from", size=9, anchor="end", style="italic", halo=True)
    P.text(gx - 9, G["terr0"] + 25, "the east wing", size=9, anchor="end", style="italic", halo=True)
    P.dim(-gw - 5, G["terr0"], -gw - 5, G["terr0"] + t["deep"], "40 ft", fact="terraces.deep", side=-1)
    P.dim(-gw, lo + 20, gx, lo + 20, "120 ft", fact="terraces.wide", side=1)
    P.dim(-gw - 5, lo, -gw - 5, gate_y, "about\n150 ft", fact="terraces.lower_garden", side=-1)
    P.tag(10, G["terr0"] + 33, "S6")
    P.tag(W_ - 26, G["terr0"] + 33, "S9")
    P.tag(W_ - 6, L + 5, "S9")
    P.text(W_ + 1, L + 3.3, "the rail crowd", size=9, style="italic", halo=True)

    # profile: the drops, Court to river gate (drops to scale, lengths not)
    ps = 2.4
    px0, py0 = PAD + 16, TOP + 10 + mh + 24
    svg.open(id="profile", data_px_per_ft=n(ps))
    svg.text(px0, py0, "Profile, Court to river gate (drops to scale; lengths are not)", size=10.5,
             weight="bold")
    yb = py0 + 22
    xs = [0, 60, 130, 200, 270, 400]
    labels = ["walk", "upper terrace", "second", "third", "lower garden"]
    yy = yb
    pts = [(px0, yy)]
    for i in range(5):
        if i > 0:
            drop = 6 if i == 1 else t["drop"]               # walk → upper terrace: not given
            if i > 1:
                svg.line(px0 + xs[i] + 6, yy, px0 + xs[i] + 6, yy + drop * ps, stroke=ACCENT,
                         stroke_width=0.9, data_fact_len="terraces.drop", data_px_per_ft=n(ps))
            pts.append((px0 + xs[i], yy))
            yy += drop * ps
            pts.append((px0 + xs[i], yy))
        svg.text(px0 + xs[i] + 4 + (8 if i > 0 else 0), yy - 4, labels[i], size=9, style="italic", fill=SOFT)
    pts.append((px0 + xs[5], yy))
    svg.polyline(pts, stroke=WALL, stroke_width=1.6)
    svg.line(px0 + xs[5], yy, px0 + xs[5], yy - 18, stroke=ACCENT, stroke_width=2.4)
    svg.text(px0 + xs[5] + 6, yy - 6, "river gate", size=9, style="italic", fill=SOFT)
    svg.text(px0 + 140, yb - 2, "each terrace 10 ft below the last",
             size=9, style="italic", fill=SOFT)
    svg.close()

    legend = [("wall", "Wall"), ("door", "Door"), ("stairs", "Stairs (arrow points up)"),
              ("rail", "Rail or waist-high balustrade (a 10-ft drop beyond)"),
              ("fill", "Garden walk (ground level)", GARDEN),
              ("fill", "Terraces, each 10 ft lower", GARDEN2), ("fill", "Lower garden", LAWN),
              ("fill", "Context, other maps", CONTEXT), ("grid", "5-foot grid"),
              ("tag", "Fight card (chapter IX)"), ("dim", "Measured distance")]
    key = [("B5", "The garden terraces and the river gate"),
           ("S6", "The quiet word, on the upper terrace"),
           ("S9", "The appointment, on the upper terrace, watched from the walk's rail")]
    caption = ["Distances from chapter V; other positions approximate."]
    frame(svg, "Map VIII–4: The Terraces and the River Gate", "B5 — Court to river, down three terraces",
          legend, caption, mw, scale_ft=50, scale=scale, key=key)
    return svg.render("Map VIII–4: The Terraces and the River Gate")


# --------------------------------------------------------------------------- map VIII–5

def map_east_wing(d: dict, grid=True) -> str:
    w, sr = d["east_wing"], d["service_run"]
    G = geometry(d)
    W_, L, gw, gx = G["W"], G["L"], G["gw"], G["gx"]
    scale = 3.6
    sx, sy, sw, sh = G["stair"]
    cx, cy, cw, ch = G["cleared"]
    ix, iy, iw, ih = G["inner"]
    rw = G["room_w"]
    top = iy + ih
    ex = ix + iw                                       # the wing's corridor east wall
    land = 4                                           # the service stair's landing (O55)
    r0 = iy + land                                     # the rooms start beside the landing
    ss_y, ss_len = cy + ch - 28, 28                    # the service stair hall, beside the doors
    x0, x1, y0, y1 = W_ - 26, ex + rw + 60, -6, top + 10
    mw, mh = int((x1 - x0) * scale), int((y1 - y0) * scale)
    W, H = mw + PAD * 2 + LEGEND_W, TOP + mh + 124
    svg = Svg(W, H, scale)
    svg.rect(0, 0, W, H, fill="#ffffff")
    P = Plan(svg, PAD, TOP + 10, x0, y1, scale)
    P.grid_on = grid

    # context: the Court's east edge, the east gallery, the walk and terraces
    P.rect(x0, y0, W_ - x0, L - y0, fill=CONTEXT)
    P.rect(W_, y0, gw, L - y0, fill="#e9e4d8")
    P.rect(x0, L, gx - x0, G["walk"], fill=GARDEN)
    P.rect(x0, G["terr0"], gx - x0, 40, fill=GARDEN2)
    P.rect(x0, G["terr0"] + 40, gx - x0, y1 - G["terr0"] - 40, fill=GARDEN3)
    P.rail(x0, L + G["walk"], gx, L + G["walk"])
    P.rail(x0, G["terr0"] + 40, gx, G["terr0"] + 40)
    P.walls([(W_, y0), (W_, sy)], closed=False, width=1.2)
    P.walls([(W_, sy + G["east_door_w"]), (W_, L), (x0, L)], closed=False, width=1.2)
    P.text(W_ - 3, 12, "B2, the Court", size=9.5, anchor="end", style="italic", fill=SOFT)
    P.text(W_ - 3, 8.5, "(map VIII–3)", size=9.5, anchor="end", style="italic", fill=SOFT)
    P.text(W_ + gw / 2, 12, "B3 east", size=9.5, anchor="middle", style="italic", fill=SOFT)
    P.text(W_ + gw / 2, 8.5, "gallery", size=9.5, anchor="middle", style="italic", fill=SOFT)
    P.text(W_ + gw / 2, 5, "(12 ft up)", size=9.5, anchor="middle", style="italic", fill=SOFT)
    P.text(x0 + 2, L + 3.3, "garden walk", size=9, style="italic", fill=SOFT, halo=True)
    P.text(x0 + 2, G["terr0"] + 3, "upper terrace", size=9, style="italic", fill=SOFT, halo=True)
    P.text(x0 + 2, G["terr0"] + 43, "second terrace", size=9, style="italic", fill=SOFT, halo=True)
    # the garden below the east wing (S10)
    gxe = ex + rw
    P.rect(gx, ss_y + 6, x1 - gx, y1 - ss_y - 6, fill=LAWN)
    # the approach and the wing (gallery level)
    P.rect(W_, sy, gw, G["east_door_w"], fill=FLOOR)
    P.rect(cx, cy, cw, ch, fill=UPPER, id="cleared-corridor",
           data_fact_w="east_wing.cleared_corridor.wide", data_fact_h="east_wing.cleared_corridor.long")
    P.rect(ix, iy, iw, ih, fill=UPPER, id="inner-corridor",
           data_fact_w="east_wing.inner_corridor.wide", data_fact_h="east_wing.inner_corridor.long")
    rooms = ["Veier's rooms", "Raunu's rooms", "the nursery"]
    room_len = 30
    room_boxes = []
    for i, name in enumerate(rooms):
        ry = r0 + i * room_len
        P.rect(ex, ry, rw, room_len, fill=UPPER, id=f"room-{i + 1}", data_room_across="width")
        room_boxes.append((name, ry))
    P.rect(ex, ss_y, 10, ss_len + land, fill=STAIR)
    if grid:
        svg.open(id="grid", stroke=GRID, stroke_width=0.45, opacity=0.8)
        P.grid(cx, cy, cw, ch)
        P.grid(ix, iy, iw, ih)
        for name, ry in room_boxes:
            P.grid(ex, ry, rw, room_len)
        svg.close()
    P.stairs(sx, sy, sw, sh, up="n")
    P.stairs(ex, ss_y, 10, ss_len - 2, up="n", treads=12)
    # the service run (schematic), 5 ft wide, to the foot of the service stair
    run_x = ex + 10
    P.rect(run_x, y0, sr["wide"], ss_y + 6 - y0, fill="#ffffff", stroke=SERVICE, stroke_width=1.6,
           stroke_dasharray="6 3", id="service-run", data_fact_w="service_run.wide")
    # the garden stair, outside the wing's west wall
    P.stairs(gx - 7, G["terr0"] + 14, 6, top - G["terr0"] - 16, up="n", treads=18)
    # walls
    P.walls([(sx, sy + G["east_door_w"]), (sx, top), (ex, top), (ex, r0 + 3 * room_len),
             (ex + rw, r0 + 3 * room_len), (ex + rw, r0), (ex + 10, r0), (ex + 10, ss_y),
             (ex, ss_y), (ex, sy), (sx, sy)], closed=False)
    P.line(W_, sy, gx, sy, stroke=WALL, stroke_width=1.4)
    P.line(W_, sy + G["east_door_w"], gx, sy + G["east_door_w"], stroke=WALL, stroke_width=1.4)
    for name, ry in room_boxes[1:]:
        P.line(ex, ry, ex + rw, ry, stroke=WALL, stroke_width=1.8)
    P.line(ex, ss_y, ex, r0 + 3 * room_len, stroke=WALL, stroke_width=1.8)
    P.line(ix, iy, ex, iy, stroke=WALL, stroke_width=1.0)
    P.door(W_, sy, G["east_door_w"], horizontal=False, double=True, fill=FLOOR)
    P.door(ix, iy, iw, double=True, fill=UPPER)                              # the double doors
    P.door(ex, cy + ch - 7, 4, horizontal=False, fill=UPPER)                 # cleared corridor → service stair
    P.door(ex, iy + 0.2, land - 0.4, horizontal=False, fill=UPPER)            # the wing's service door
    for name, ry in room_boxes:
        P.door(ex, ry + room_len / 2 - 2, 4, horizontal=False, fill=UPPER)
    P.door(ix, top - 8, 4, horizontal=False, fill=GARDEN3)                    # to the garden stair
    P.door(ex + 10, ss_y + 1, 4, horizontal=False, fill=STAIR)                # from the service run
    P.door(ex + 10, ss_y + 12, 4, horizontal=False, fill=STAIR)               # out to the garden

    # labels: the approach (left, over the gallery)
    P.text(W_ + gw - 1, sy + 18, "stair up 12 ft from", size=9, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, sy + 15, "the Court's east doors", size=9, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, cy + 36, "cleared corridor,", size=9.5, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, cy + 32.5, "10 × 60 ft", size=9.5, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, iy + 1, "double doors →", size=9.5, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, iy + 22, "corridor,", size=9.5, anchor="end", style="italic", halo=True)
    P.text(W_ + gw - 1, iy + 18.5, "10 × 100 ft →", size=9.5, anchor="end", style="italic", halo=True)
    P.text(gx - 8, G["terr0"] + 34, "the garden stair", size=9, anchor="end", style="italic", halo=True)
    P.text(gx - 8, G["terr0"] + 31, "(the private stair),", size=9, anchor="end", style="italic", halo=True)
    P.text(gx - 8, G["terr0"] + 28, "down the outer wall", size=9, anchor="end", style="italic", halo=True)
    P.text(gx - 8, G["terr0"] + 25, "to the upper terrace", size=9, anchor="end", style="italic", halo=True)
    # the rooms
    for name, ry in room_boxes:
        P.text(ex + rw / 2, ry + room_len / 2 + 1, name, size=10, anchor="middle", weight="bold", halo=True)
    # the service stair and run (right)
    lx = run_x + 7
    P.text(lx, ss_y + 27, "service stair: up to the", size=9, style="italic", halo=True)
    P.text(lx, ss_y + 24, "doors, down and out to", size=9, style="italic", halo=True)
    P.text(lx, ss_y + 21, "the garden (S10)", size=9, style="italic", halo=True)
    P.text(ex + rw + 2, r0 - 2, "the wing's service door (S7)", size=9, style="italic", halo=True)
    P.line(ex + rw + 1.5, r0 - 1.5, ex + 1, iy + 2, stroke=SOFT, stroke_width=0.7)
    P.text(lx, 26, "service run, 5 ft", size=9, style="italic", fill=SERVICE, halo=True)
    P.text(lx, 23, "from the kitchens and the", size=9, style="italic", fill=SERVICE, halo=True)
    P.text(lx, 20, "passages behind the", size=9, style="italic", fill=SERVICE, halo=True)
    P.text(lx, 17, "Dance (B10)", size=9, style="italic", fill=SERVICE, halo=True)
    # the wing and its garden (right)
    P.text(gxe + 3, top - 6, "B9  THE EAST WING", size=12, weight="bold", halo=True)
    P.text(gxe + 3, top - 10.5, "gallery level, 12 ft up;", size=9.5, style="italic", halo=True,
           data_fact="east_wing.floor")
    P.text(gxe + 3, top - 14, "rooms 20–30 ft across", size=9.5, style="italic", halo=True)
    P.text(gxe + 3, r0 + 52, "the garden below", size=10, weight="bold", halo=True)
    P.text(gxe + 3, r0 + 48.5, "the east wing", size=10, weight="bold", halo=True)
    P.text(gxe + 3, r0 + 45, "dark past the last lantern;", size=9, style="italic", halo=True)
    P.text(gxe + 3, r0 + 42, "flower beds; 20 ft of", size=9, style="italic", halo=True)
    P.text(gxe + 3, r0 + 39, "crystal wall up to one", size=9, style="italic", halo=True)
    P.text(gxe + 3, r0 + 36, "lit window", size=9, style="italic", halo=True)
    P.tag(gxe + 10, r0 + 30, "S10")
    P.tag(cx + cw / 2, cy + 14, "S4")
    P.tag(run_x + 2.5, 40, "S7")
    P.tag(run_x + 2.5, 50, "S2")

    legend = [("wall", "Wall"), ("door", "Door or double doors"), ("stairs", "Stairs (arrow points up)"),
              ("rail", "Balustrade"), ("fill", "Gallery level, 12 ft up", UPPER),
              ("service", "Service run, 5 ft"), ("fill", "The garden below the wing", LAWN),
              ("fill", "Context, other maps", CONTEXT), ("grid", "5-foot grid"),
              ("tag", "Fight card (chapter IX)")]
    key = [("B9", "The east wing: Veier's rooms, Raunu's rooms, the nursery"),
           ("B10", "The service passages; they reach the garden stair too"),
           ("S2", "The service corridor behind the Dance"), ("S4", "The east wing doors"),
           ("S7", "The dark run to the wing's service door"),
           ("S10", "Over the wall, from the garden below")]
    caption = ["Distances from chapter V; other positions approximate."]
    frame(svg, "Map VIII–5: The East Wing and the Service Run", "B9 · B10 — upstairs, at gallery level",
          legend, caption, mw, scale_ft=20, scale=scale, key=key)
    return svg.render("Map VIII–5: The East Wing and the Service Run")


# --------------------------------------------------------------------------- map VIII–1

FLOOR_STYLE = {
    "street": (STREET, None, "Outside: the street"),
    "ground": (FLOOR, None, "Ground level"),
    "garden": (GARDEN, None, "Gardens, below the garden walk"),
    "gallery": (UPPER, None, "Gallery level, 12 ft up"),
    "second": ("#cdbfe0", None, "Second floor"),
    "cellar": ("#d8d2c8", None, "Beneath the cellars"),
    "unknown": ("#ffffff", "4 3", "Shown by connection"),
    "throughout": ("#eef2f6", "6 3", "Throughout the palace"),
}


def map_palace(d: dict, grid=True) -> str:
    mw, mh = 760, 760
    W, H = mw + PAD * 2 + LEGEND_W, TOP + mh + 96
    svg = Svg(W, H, 1)
    svg.rect(0, 0, W, H, fill="#ffffff")
    ox, oy = PAD + 10, TOP + 20

    def box(code, x, y, w, h, title, floor, notes=(), extra=None, big=14):
        fill, dash, _ = FLOOR_STYLE[floor]
        svg.rect(ox + x, oy + y, w, h, fill=fill, stroke=WALL, stroke_width=1.6,
                 stroke_dasharray=dash, data_room=code, data_floor=floor)
        svg.text(ox + x + 8, oy + y + 19, code, size=big, weight="bold")
        tx = ox + x + 8 + bold_w(code, big) + 4
        line = 0
        if title:
            if tx + bold_w(title, 11) > ox + x + w - 4:
                line = 1
                svg.text(ox + x + 8, oy + y + 34, title, size=11, weight="bold")
            else:
                svg.text(tx, oy + y + 19, title, size=11, weight="bold")
        for i, ln in enumerate(notes):
            svg.text(ox + x + 8, oy + y + 35 + 15 * line + 13 * i, ln, size=9.5, style="italic", fill=SOFT)
        if extra:
            code2, floor2, text = extra
            svg.text(ox + x + 8, oy + y + h - 9, f"{code2}  {text}", size=10.5, weight="bold",
                     fill=ACCENT, data_room=code2, data_floor=floor2)

    def link(pts, dashed=False):
        p = [(ox + x, oy + y) for x, y in pts]
        svg.polyline(p, stroke=SERVICE if dashed else INK, stroke_width=1.4 if dashed else 1.8,
                     stroke_dasharray="5 3" if dashed else None)

    def note(x, y, s, anchor="start", color=SOFT):
        svg.text(ox + x, oy + y, s, size=9, style="italic", fill=color, anchor=anchor, halo=True)

    # the river and the gardens
    svg.rect(ox + 120, oy, 300, 22, fill=WATER)
    svg.text(ox + 270, oy + 15, "THE RIVER", size=10.5, anchor="middle", weight="bold", fill=SOFT)
    box("B5", 120, 30, 300, 150, "The Garden Terraces & the River Gate", "garden",
        ["the river gate (locked; Agenda 6), on the river walk",
         "the lower garden, about 150 ft",
         "three terraces, each 10 ft below the last (S6, S9)",
         "the garden walk, railed, at ground level"])
    # the Court and its galleries
    box("B2", 160, 236, 220, 190, "The Crystal Court", "ground",
        ["ground level; about 140 × 80 ft", "the dais and high table at the", "far end; the Dance",
         "garden doors to the walk", "east doors: a stair up 12 ft"])
    for gx_ in (120, 380):
        box("B3", gx_, 236, 40, 190, "", "gallery", big=13)
        for i, ln in enumerate(["ban-", "quet", "gal-", "lery,", "", "12 ft", "up"]):
            svg.text(ox + gx_ + 20, oy + 300 + 13 * i, ln, size=9.5, anchor="middle", style="italic", fill=SOFT)
    box("B4", 0, 284, 106, 70, "Audience Hall", "unknown", ["off the Court"])
    box("B1", 160, 482, 220, 92, "The Gatehouse Court", "ground",
        ["the gatehouse: the cell, the stair", "to the gate-walk (15 ft up)"],
        extra=("B12", "ground", "after midnight, held (S3)"))
    box("B0", 160, 630, 220, 80, "The Street", "street", ["Gate Street: the hill, the line.", "Play starts here."])
    box("B9", 500, 110, 150, 180, "The East Wing", "gallery",
        ["gallery level, 12 ft up", "a 10 × 100-ft corridor:", "Veier's rooms, Raunu's",
         "rooms, the nursery; the", "private stair (the garden", "stair) at its far end;",
         "double doors (S4) at the", "head of the cleared corridor"])
    # connections the text gives
    link([(270, 482), (270, 426)])
    note(278, 458, "main doors (10 ft)")
    link([(270, 630), (270, 574)])
    note(278, 606, "the outer gate and its wicket (S3)")
    link([(270, 236), (270, 180)])
    note(278, 212, "garden doors, to the walk")
    link([(106, 318), (120, 318)])
    link([(420, 270), (500, 270)])
    for i, ln in enumerate(["east doors,", "a stair up", "12 ft; the", "cleared", "corridor", "(10 × 60 ft)"]):
        note(426, 262 + (0 if i == 0 else 22 + 12 * (i - 1)), ln)
    link([(575, 110), (575, 100), (420, 100)])
    note(585, 88, "the garden stair, down")
    note(585, 100, "to the upper terrace")

    # rooms placed only by connection
    px = 490
    svg.text(ox + px, oy + 372, "Rooms shown by connection", size=11.5, weight="bold")
    box("B6", px, 384, 270, 44, "The Chapel", "unknown", ["a public room; Mother Sella's, all night"])
    box("B7", px, 436, 270, 44, "The Trophy Gallery", "unknown", ["the private palace, off the gallery corridor"])
    box("B8", px, 488, 270, 44, "Raunu's Study", "second", ["the second floor, in the dark wing (S8)"])
    box("B13", px, 540, 270, 44, "The Room You Put Here", "unknown",
        ["off the lower gallery; from B7 and the service run"])
    box("B10", px, 592, 270, 56, "Kitchens & Service Passages", "throughout",
        ["the passages thread the whole palace: the east", "wing, the garden stair, the S11 door off B2"])
    box("B11", px, 656, 270, 56, "The Root of the House", "cellar",
        ["kitchens → wine cellar → the lower cellar", "stair → a sealed seam (Undercurrent A)"])
    link([(px, 620), (465, 620), (465, 340), (575, 340), (575, 290)], dashed=True)
    link([(465, 410), (420, 410)], dashed=True)
    note(457, 520, "service", anchor="end", color=SERVICE)
    note(457, 532, "passages", anchor="end", color=SERVICE)

    # the floors panel
    fy = 420
    svg.text(ox, oy + fy - 8, "Floors", size=11, weight="bold")
    rows = [("second", "2nd floor: B8"), ("gallery", "12 ft up: B3, B9"),
            ("ground", "Ground: B1, B2"), ("garden", "Below walk: B5"),
            ("cellar", "Cellars: B11"), ("unknown", "By connection: B4,"),
            (None, "B6, B7, B13")]
    for i, (fl, label) in enumerate(rows):
        if fl:
            fill, dash, _ = FLOOR_STYLE[fl]
            svg.rect(ox, oy + fy + i * 21, 16, 13, fill=fill, stroke=WALL, stroke_width=0.8,
                     stroke_dasharray=dash)
        svg.text(ox + 22, oy + fy + i * 21 + 10.5, label, size=9.5)

    legend = [("fill", FLOOR_STYLE[k][2], FLOOR_STYLE[k][0], FLOOR_STYLE[k][1])
              for k in ("street", "ground", "gallery", "second", "garden", "cellar", "throughout", "unknown")]
    legend += [("wall", "A way through"), ("service", "Service passages")]
    key = [("B0", "Street, approach, line"), ("B1", "Gatehouse Court"), ("B2", "Crystal Court"),
           ("B3", "Banquet Galleries"), ("B4", "Audience Hall"), ("B5", "Terraces, river gate"),
           ("B6", "Chapel"), ("B7", "Trophy Gallery"), ("B8", "Raunu's Study"), ("B9", "East Wing"),
           ("B10", "Kitchens, service passages"), ("B11", "Root of the House"),
           ("B12", "Gatehouse Court, held"), ("B13", "The Room You Put Here")]
    caption = ["Not to scale. Maps VIII–2 to VIII–5 draw the rooms to scale."]
    frame(svg, "Map VIII–1: The Palace", "B0–B13, keyed, floor by floor", legend, caption, mw,
          scale_ft=None, east=True, key=key)
    return svg.render("Map VIII–1: The Palace")


# --------------------------------------------------------------------------- build

MAPS = {
    "map_viii_1_palace": map_palace,
    "map_viii_2_gatehouse": map_gatehouse,
    "map_viii_3_court": map_court,
    "map_viii_4_terraces": map_terraces,
    "map_viii_5_east_wing": map_east_wing,
}


def rasterize(svg_path: Path, png_path: Path, density=150):
    """PNG preview through ImageMagick, with the font list collapsed to DejaVu Serif."""
    exe = shutil.which("convert") or shutil.which("magick")
    if not exe:
        raise RuntimeError("ImageMagick `convert` not found; build with --no-png")
    text = svg_path.read_text(encoding="utf-8").replace(esc(FONT), PNG_FONT)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "map.svg"
        src.write_text(text, encoding="utf-8")
        subprocess.run([exe, "-density", str(density), "-background", "white", f"MSVG:{src}",
                        "-flatten", "-strip", str(png_path)], check=True)


def build_one(name: str, out: Path, png=True, grid=True, dims=None) -> Path:
    fn = MAPS[name]
    dims = dims or load_dims()
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.svg"
    path.write_text(fn(dims, grid=grid), encoding="utf-8")
    if png:
        rasterize(path, out / f"{name}.png")
    return path


def build_all(out=HERE, png=True, grid=True) -> list[Path]:
    dims = load_dims()
    return [build_one(name, out, png=png, grid=grid, dims=dims) for name in MAPS]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the Oraga Night palace maps")
    ap.add_argument("--no-png", action="store_true", help="SVGs only")
    ap.add_argument("--no-grid", action="store_true", help="leave the 5-foot grid out")
    ap.add_argument("--out", default=str(HERE), help="output folder (default: this folder)")
    a = ap.parse_args(argv)
    for p in build_all(Path(a.out), png=not a.no_png, grid=not a.no_grid):
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
