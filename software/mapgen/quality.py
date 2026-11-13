"""Quality bar (T27-T29): image metrics, comparator bands, contact sheets.

The comparator maps are read in memory from the owner's zips and never written
anywhere inside the repo. Only metric numbers are committed (quality_bands.yaml).
"""
from __future__ import annotations

import io
import json
import os
import zipfile
from pathlib import Path

import numpy as np
import yaml
from PIL import Image as PImage, ImageDraw
from scipy import ndimage

PImage.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
MANIFEST = HERE / "comparators.yaml"
BANDS = HERE / "quality_bands.yaml"
NORM_PPS = 50          # px per 5-ft square after normalisation (10 px per foot)
NORM_PPF = NORM_PPS / 5
SHEET_LABEL_H = 28
METRICS = ("Q1", "Q2", "Q3", "Q4", "Q5s", "Q5h")


def _lum(rgb):
    return (rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114).astype(np.float32)


def prepare(img: PImage.Image, px_per_square=None, crop=None, exclude=None, normalize_width=None,
            feet_per_square: float = 5):
    """Crop, build the valid mask and rescale to NORM_PPF px per foot (NORM_PPS per 5-ft square).
    Returns (rgb 0..1, valid)."""
    img = img.convert("RGB")
    W, H = img.size
    valid = np.ones((H, W), bool)
    for b in exclude or []:
        valid[int(b[1] * H):int(np.ceil(b[3] * H)), int(b[0] * W):int(np.ceil(b[2] * W))] = False
    if crop:
        box = (int(crop[0] * W), int(crop[1] * H), int(np.ceil(crop[2] * W)), int(np.ceil(crop[3] * H)))
        img = img.crop(box)
        valid = valid[box[1]:box[3], box[0]:box[2]]
    w, h = img.size
    if normalize_width:
        f = normalize_width / w
    elif px_per_square:
        f = NORM_PPF / (float(px_per_square) / float(feet_per_square))
    else:
        f = 1.0
    if abs(f - 1) > 1e-6:
        size = (max(1, round(w * f)), max(1, round(h * f)))
        img = img.resize(size, PImage.LANCZOS if f < 1 else PImage.BICUBIC)
        valid = np.asarray(PImage.fromarray(valid.astype(np.uint8) * 255).resize(size, PImage.NEAREST)) > 127
    return np.asarray(img, np.float32) / 255.0, valid


def _hsv_sat_hue(rgb):
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    d = mx - mn
    s = np.divide(d, mx, out=np.zeros_like(d), where=mx > 1e-6)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(mx)
    nz = d > 1e-6
    rm = nz & (mx == r)
    gm = nz & (mx == g) & ~rm
    bm = nz & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    return s, h / 6.0


def metrics(img: PImage.Image, px_per_square=None, crop=None, exclude=None, normalize_width=None,
            feet_per_square: float = 5) -> dict:
    rgb, valid = prepare(img, px_per_square, crop, exclude, normalize_width, feet_per_square)
    L = _lum(rgb)
    v = valid
    if not v.any():
        raise ValueError("no valid pixels after crop/exclude")
    q1 = float(np.percentile(L[v], 98) - np.percentile(L[v], 2))
    m = ndimage.uniform_filter(L, 5)
    m2 = ndimage.uniform_filter(L * L, 5)
    ls = np.sqrt(np.clip(m2 - m * m, 0, None))
    q2 = float(ls[v].mean())
    hh, ww = (L.shape[0] // NORM_PPS) * NORM_PPS, (L.shape[1] // NORM_PPS) * NORM_PPS
    if hh and ww:
        blk = L[:hh, :ww].reshape(hh // NORM_PPS, NORM_PPS, ww // NORM_PPS, NORM_PPS)
        bv = v[:hh, :ww].reshape(blk.shape).mean(axis=(1, 3)) > 0.8
        means = blk.mean(axis=(1, 3))[bv]
        q3 = float(means.std()) if means.size > 1 else 0.0
    else:
        q3 = 0.0
    mag = np.hypot(ndimage.sobel(L, 1), ndimage.sobel(L, 0)) / 8.0
    q4 = float((mag[v] > 0.1).mean())
    s, h = _hsv_sat_hue(rgb)
    q5s = float(s[v].mean())
    sat = v & (s > 0.15)
    hist = np.bincount(np.minimum((h[sat] * 18).astype(int), 17), minlength=18) / max(v.sum(), 1)
    q5h = int((hist > 0.02).sum())
    return {"Q1": round(q1, 4), "Q2": round(q2, 4), "Q3": round(q3, 4), "Q4": round(q4, 4),
            "Q5s": round(q5s, 4), "Q5h": q5h}


def q6(L: np.ndarray, grid_mask: np.ndarray, wall_mask: np.ndarray) -> float:
    """Grid-line contrast over wall-line contrast (lower = grid more subordinate)."""
    bg = ndimage.gaussian_filter(L, 3)
    g = grid_mask > 0.5
    w = wall_mask > 0.5
    if not g.any() or not w.any():
        return 0.0
    gc = np.abs(L - bg)[g & ~w].mean() if (g & ~w).any() else 0.0
    wc = np.abs(L - bg)[w].mean()
    return float(gc / max(wc, 1e-6))


# ---------- comparators and bands ----------

def load_manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text())


def ref_dir() -> Path:
    return Path(os.environ.get("MAPGEN_REF_DIR", load_manifest()["ref_dir_default"]))


def load_comparator(cid: str, base: Path | None = None) -> tuple[PImage.Image, dict]:
    man = load_manifest()
    c = man["comparators"][cid]
    base = Path(base) if base else ref_dir()
    with zipfile.ZipFile(base / c["pack"]) as z:
        data = z.read(c["member"])
    return PImage.open(io.BytesIO(data)).convert("RGB"), c


def comparator_metrics(cid: str, base: Path | None = None) -> dict:
    img, c = load_comparator(cid, base)
    return metrics(img, c.get("px_per_square"), c.get("crop"), c.get("exclude"), c.get("normalize_width"),
                   c.get("feet_per_square", 5))


def bands_from(values: dict, ids: list[str], widen: float = 0.15) -> dict:
    out = {}
    for k in ("Q1", "Q2", "Q3", "Q4", "Q5s"):
        xs = [values[i][k] for i in ids if i in values and k in values[i]]
        if xs:
            out[k] = [round(min(xs) * (1 - widen), 4), round(max(xs) * (1 + widen), 4)]
    return out


def load_bands() -> dict:
    return yaml.safe_load(BANDS.read_text())


def check_bands(m: dict, bands: dict, category: str) -> dict:
    out = {}
    for k, (lo, hi) in bands[category].items():
        if k.startswith("_") or k not in m:
            continue
        out[k] = (m[k], [lo, hi], bool(lo <= m[k] <= hi))
    return out


def write_baseline(base: Path | None = None, research: Path | None = None) -> dict:
    man = load_manifest()
    values = {cid: comparator_metrics(cid, base) for cid in man["comparators"]}
    bands = {cat: bands_from(values, ids) for cat, ids in man["categories"].items()}
    data = {"_note": "Generated by `python -m mapgen quality --baseline` from the comparator manifest. "
                     "Numbers only; no comparator image is stored.",
            "_values": values, **bands}
    BANDS.write_text(yaml.safe_dump(data, sort_keys=False))
    if research:
        _write_research(research, man, values, bands)
    return data


def _write_research(path: Path, man, values, bands):
    lines = ["# RESEARCH — mapgen comparator metrics", "",
             "*Generated by `python -m mapgen quality --baseline --research docs/RESEARCH_mapgen_comparators.md`. "
             "Numbers only: the comparator maps are the owner's local WotC packs and are never copied.*", "",
             "## Method", "",
             f"Each map is cropped to its body (legend, title, compass and scale note excluded), rescaled to "
             f"{NORM_PPF:g} px per foot ({NORM_PPS} px per 5-ft square; from the measured px/square and feet/square "
             "in `software/mapgen/comparators.yaml`; the region map by width), and measured:", "",
             "- **Q1** tonal range: luminance P98 − P2",
             "- **Q2** fine detail: mean local σ of luminance in 5-px windows",
             "- **Q3** mid-scale variation: σ of mean luminance per 5-ft cell",
             "- **Q4** ink density: fraction of pixels with Sobel magnitude/8 > 0.1",
             "- **Q5s** mean HSV saturation; **Q5h** hue families (18 bins with > 2% of pixels, s > 0.15)",
             "- **Q6** (ours only) grid-line contrast ÷ wall-line contrast", "",
             "Bands are [min × 0.85, max × 1.15] over a category's comparators.", "",
             "## Values", "", "| ID | Map | Category | Q1 | Q2 | Q3 | Q4 | Q5s | Q5h |", "|---|---|---|---|---|---|---|---|---|"]
    for cid, v in values.items():
        c = man["comparators"][cid]
        lines.append(f"| {cid} | {c['title']} | {c['category']} | " + " | ".join(str(v[k]) for k in METRICS) + " |")
    lines += ["", "## Bands", "", "| Category | Q1 | Q2 | Q3 | Q4 | Q5s |", "|---|---|---|---|---|---|"]
    for cat, b in bands.items():
        lines.append(f"| {cat} | " + " | ".join(f"{b[k][0]}–{b[k][1]}" for k in ("Q1", "Q2", "Q3", "Q4", "Q5s")) + " |")
    path.write_text("\n".join(lines) + "\n")


# ---------- contact sheet ----------

def _inside_repo(p: Path) -> bool:
    try:
        Path(p).resolve().relative_to(REPO_ROOT.resolve())
        return True
    except ValueError:
        return False


def make_sheet(ours: PImage.Image, ours_pps, theirs: PImage.Image, theirs_pps, out: Path,
               theirs_crop=None, labels=("mapgen", "comparator"), max_h: int = 1400,
               ours_fps: float = 5, theirs_fps: float = 5) -> Path:
    """Ours beside a same-size region of the comparator, both at NORM_PPS px/square."""
    out = Path(out)
    if _inside_repo(out):
        raise ValueError("refusing to write a contact sheet inside the repo (comparator images stay out of git)")
    a, _ = prepare(ours, ours_pps, feet_per_square=ours_fps)
    b, _ = prepare(theirs, theirs_pps, crop=theirs_crop, feet_per_square=theirs_fps)
    A = PImage.fromarray((a * 255).astype(np.uint8))
    B = PImage.fromarray((b * 255).astype(np.uint8))
    if A.size[1] > max_h:
        A = A.crop((0, 0, A.size[0], max_h))
    w = min(A.size[0], B.size[0])
    h = min(A.size[1], B.size[1])
    bx = (B.size[0] - w) // 2
    by = (B.size[1] - h) // 2
    B = B.crop((bx, by, bx + w, by + h))
    gap = 20
    sheet = PImage.new("RGB", (A.size[0] + gap + w, A.size[1] + SHEET_LABEL_H), "white")
    sheet.paste(A, (0, SHEET_LABEL_H))
    sheet.paste(B, (A.size[0] + gap, SHEET_LABEL_H))
    d = ImageDraw.Draw(sheet)
    d.text((4, 6), labels[0], fill="black")
    d.text((A.size[0] + gap + 4, 6), labels[1], fill="black")
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


# ---------- CLI ----------

def cli_quality(args) -> int:
    if getattr(args, "baseline", False):
        research = Path(args.research) if args.research else None
        data = write_baseline(research=research)
        print(json.dumps({k: v for k, v in data.items() if not k.startswith("_")}, indent=2))
        return 0
    if not args.png:
        print("mapgen quality: give a PNG or --baseline")
        return 2
    pps, fps = args.px_per_square, 5
    if args.recipe:
        from .recipe import load_recipe
        hdr = load_recipe(args.recipe).map
        pps = pps or hdr.px_per_square
        fps = hdr.feet_per_square
    m = metrics(PImage.open(args.png), pps or 70, feet_per_square=fps)
    print(json.dumps(m))
    if args.category:
        res = check_bands(m, load_bands(), args.category)
        bad = [k for k, (_, _, ok) in res.items() if not ok]
        for k, (val, band, ok) in res.items():
            print(f"{k}: {val} in {band} {'ok' if ok else 'OUT'}")
        return 0 if not bad else 1
    return 0


def cli_sheet(args) -> int:
    theirs, c = load_comparator(args.vs)
    make_sheet(PImage.open(args.png), args.px_per_square or 70, theirs, c.get("px_per_square"),
               Path(args.out), theirs_crop=c.get("crop"), labels=("mapgen", f"{args.vs} {c['title']}"),
               theirs_fps=c.get("feet_per_square", 5))
    print(args.out)
    return 0
