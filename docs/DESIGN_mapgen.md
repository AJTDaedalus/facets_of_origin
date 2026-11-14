# DESIGN — Programmatic Map Building (`mapgen`)

*Planner tier, 2026-11-13. Implements `docs/BRIEF_mapgen.md`. Tasks: `docs/TASKS_mapgen.md`.
Log: `docs/LOG_mapgen.md` (Worker creates it on the first task).*

## 1. Where we stand

There are two kinds of Oraga map today, and each does half the job:

| | Painted (`art/maps/*.png`) | Keyed SVG (`maps/build_maps.py`) |
|---|---|---|
| Looks like a published module | yes | no: flat fills, diagram style |
| Exact canon scale | no | yes (`data-fact-*`, measured back by `tools/test_maps.py`) |
| Wall / door data for a VTT | no | no |
| Cheap to edit | no (regenerate) | yes (code) |

`mapgen` is meant to have every column: build_maps' exact scale and editability,
with a finish good enough to sit next to the reference maps in §7.

## 2. Architecture

```
 prose description ──(skill: Claude)──▶  recipe.map.yaml  ──▶  mapgen engine  ──▶  map.png
        ▲                                     │ edit                          ├──▶  map.dd2vtt (walls, portals, lights)
        └──── Claude views PNG, critiques ◀───┘                               └──▶  map.meta.json (geometry in feet, for tests)
```

Package `software/mapgen/` (importable by the web app in Phase 3; same pattern
as `software/facets/`). Tests in `software/tests/mapgen/`.

```
software/mapgen/
  __init__.py
  __main__.py        # CLI: render | ops | quality | sheet
  recipe.py          # Pydantic models: MapHeader, Step, Recipe; YAML loader; includes
  units.py           # feet <-> px transform, supersampling factor
  layers.py          # typed layer store: Geometry | Mask | Field | Image
  registry.py        # @op decorator: name, param model, input/output layer types, docs
  engine.py          # executes steps in order, type-checks references, seeds RNG per step
  ops/
    geometry.py      # rect, polygon, circle, path, union/subtract/intersect, offset
    masks.py         # rasterize, grow, shrink, blur, threshold, invert, roughen, band
    fields.py        # noise (fbm, ridged), gradient, distance, combine, remap
    paint.py         # canvas, fill, stroke, shadow, occlusion, hatch, blend
    materials.py     # material fills: ramp+noise, flagstone, planks, cobble, grass, water
    semantic.py      # wall, door, window, secret_door, light (paint + emit VTT data)
    props.py         # prop library + place + scatter (Poisson disk)
    overlay.py       # grid, compass, scale_bar, title, label, frame
  styles/
    inked_parchment.yaml   # default style: palette, ink weights, material params (recipe include)
  export.py          # PNG, UVTT (.dd2vtt) writer, meta.json
  quality.py         # image metrics + comparator bands (§7)
  comparators.yaml   # manifest of local reference maps (paths only, never images)
```

### 2.1 Layer types

| Type | Storage | Produced by | Notes |
|---|---|---|---|
| `Geometry` | shapely (Multi)Polygon / LineString, **in feet** | geometry ops | Source of truth for walls and measurement |
| `Mask` | `float32` H×W in 0..1 | rasterize, mask ops | Antialiased coverage |
| `Field` | `float32` H×W, unbounded | noise, distance, gradient | Remap to a mask or colour |
| `Image` | `float32` H×W×4, premultiplied RGBA | canvas, paint ops | One named `canvas` is the final image; others are composited into it |

The engine type-checks every reference: a step that asks for a `Mask` and gets
a `Field` fails before anything renders, with the step index and op name.

### 2.2 Coordinates and scale

- Recipe coordinates are **feet**. The origin is the **north-west corner** and y runs
  **south** (screen order), with north up. Recipes copied from `facts.yaml` (y north)
  flip once in the recipe, and the recipe comment says so.
- Header: `width_ft`, `height_ft`, `feet_per_square` (5, or 10 for big outdoor maps),
  `px_per_square` (default 70, the common VTT size; 140 for print).
- `supersample` (default 2): every raster op runs at `px × supersample`, and
  `export` downsamples with LANCZOS. Pillow's `ImageDraw` has no antialiasing,
  so this is how inked lines come out smooth. Use `--draft` (supersample 1,
  px_per_square 35) for fast previews while iterating.
- Memory budget: a 120×160 ft map at 70 px/sq ×2 is 3360×4480, about 60 MB per
  float32 layer. The engine frees layers that no later step reads (it does a
  liveness pass over the step list).

### 2.3 Recipe format

```yaml
map:
  title: Example Cave
  width_ft: 60
  height_ft: 40
  feet_per_square: 5
  px_per_square: 70
  seed: 11
  include: [styles/inked_parchment.yaml]   # defines palette, materials, ink weights, and macros

steps:
  - {op: polygon, out: cave, points: [[5,5],[40,3],[55,15],[50,35],[20,38],[4,25]]}
  - {op: roughen_geom, in: cave, out: cave, amount_ft: 1.5, scale_ft: 6}
  - {op: path, out: stream, points: [[28,0],[30,15],[26,40]], width_ft: 6}
  - {op: rasterize, in: cave, out: floor}
  - {op: rasterize, in: stream, out: water}
  - {op: fill, mask: ~floor, material: bedrock_hatch}      # "~" = inverted mask
  - {op: fill, mask: floor, material: cave_floor}
  - {op: fill, mask: water, material: water_shallow}
  - {op: shadow, mask: floor, inside: true, width_ft: 2.5, strength: 0.55}
  - {op: wall, in: cave, style: rough, emit_los: true}
  - {op: prop, kind: bridge, at: [29,14], rotate: 80, length_ft: 12}
  - {op: scatter, kind: rubble, mask: floor, region: [[5,10],[18,30]], density: 0.08}
  - {op: compass, at: ne}
```

- `out` names a layer, and reusing a name overwrites it (GIMP's "replace layer").
- `include` merges style YAML: palette, materials, defaults per op, and **macros**
  (named step sequences with parameters, such as `stone_room` or `cave_room`).
  The skill mostly writes macro calls, and the raw ops are for detail.
- Every op takes an optional `seed_offset`. Its RNG is `hash(map.seed, step index,
  seed_offset)`, so inserting a step doesn't reshuffle the noise of every step after it
  (seed by the step's `id:` when one is given, else by index).

### 2.4 Op catalogue (v1, battle maps)

| Group | Ops |
|---|---|
| Geometry | `rect`, `polygon`, `circle`, `ellipse`, `path` (polyline + width, round/flat caps), `union`, `subtract`, `intersect`, `offset` (grow/shrink in feet), `roughen_geom` (noise-displace vertices after densifying) |
| Masks | `rasterize`, `grow`, `shrink`, `blur`, `threshold`, `invert`, `band` (ring between two distances from a mask), `roughen` (raster edge displacement), `combine` (max/min/mul/sub) |
| Fields | `noise` (fbm/ridged/billow; scale_ft, octaves, persistence; opensimplex `noise2array`), `gradient` (linear/radial), `distance` (from mask, in feet), `remap` (in-range → out-range, curve), `field_to_mask` |
| Paint | `canvas` (base colour or material), `fill` (colour/material through a mask, blend mode, opacity), `stroke` (mask or geometry edge → ink line; width, roughness, double), `shadow` (drop or inner, offset, blur), `occlusion` (darken by distance to walls), `hatch` (cross-hatch or stone-block band outside walls), `tint`, `vignette`, `paper` (parchment grain overlay) |
| Materials | `flat`, `ramp_noise`, `flagstone` (jittered Voronoi cells, mortar lines, per-stone tone), `planks` (direction, width, seams, knots), `cobble`, `grass` (noise + speckle + tufts), `dirt`, `water` (depth ramp + ripple lines), `bedrock_hatch` |
| Semantic | `wall` (from geometry: band width, style `dressed`/`rough`/`ruined`, ink + fill + emits LOS), `door`, `double_door`, `window`, `secret_door` (S glyph, emits a hidden portal), `portcullis`, `stairs` (direction arrow), `light` (emits a UVTT light, optional glow paint) |
| Props | `prop` (place one), `scatter` (Poisson-disk by density mask); kinds v1: `table`, `round_table`, `chair`, `bed`, `bunk`, `crate`, `barrel`, `chest`, `rubble`, `stalagmite`, `boulder`, `tree`, `bush`, `bridge`, `brazier`, `pillar`, `statue`, `rug`, `banner` |
| Overlay | `grid` (optional mask clip, colour, alpha, weight), `compass`, `scale_bar`, `title` (cartouche), `label`, `frame` (border + margin), `legend` (from the props/semantic ops used) |

Each op is one function with a Pydantic param model and a docstring. `python -m
mapgen ops --markdown` renders the catalogue from the registry into the skill's
`references/ops.md`. That file is **generated**, and a no-diff test keeps it in step
(the house rule for generated files).

### 2.5 The look: how we get near the reference maps

What the reference maps do (§7), and the op that answers each:

| Technique in the references | mapgen answer |
|---|---|
| Parchment/paper base with low-frequency blotches | `canvas` + `paper` (fbm at 2 scales, multiply) |
| Ink wall lines with a weight hierarchy (outer heavy, detail thin) | `stroke` widths from style: `ink.heavy/medium/fine` |
| Hand-drawn wobble on natural edges, ruled edges on built walls | `roughen_geom` on caves/ruins; `dressed` walls stay straight |
| Soft inner shadow where floor meets wall | `shadow inside:true` + `occlusion` |
| Stone/rock texture or hatching beyond the walls | `hatch` band and `bedrock_hatch` material (Schley-style block hatching) |
| Floor texture never flat: flagstones, planks, cave grit | materials with per-cell tone jitter + fbm modulation |
| Water with depth ramp and ripple strokes | `water` material + `stroke` of offset contours |
| Tree canopies: scalloped clumps, rim shadow, inner highlight | `tree`/`bush` props built from noise-scalloped circles + cast shadow |
| Grid | **None by default** (owner, 2026-11-13: "I prefer no gridlines on my maps"); `grid` exists for a printed grid on request |
| Ink shading lines (hatching along walls, cliffs, banks; cracks; grit) | `shade_lines`, `cracks`, `stipple` (`ops/linework.py`); light from the NW, shadows fall SE |
| Legend, compass, title, "1 square = 5 feet" | `legend`, `compass`, `title`, `scale_bar` |

**What we can and can't reach (honest estimate):**
- Walls, floors, water, shadows, grid, cave outlines, ledges: **comparable** to the
  Schley-style references. These are inked lines plus texture plus shadow, and
  that's tractable procedurally.
- Tree and brush canopy: **close**, about a step below. Clumps read well, but the
  hand variation in each leaf mass is hard to match.
- Furniture and props: **legible but plainer**. Parametric clip-art is the biggest
  gap, and the prop library is where later polish goes.
- Lettering and cartouches: **plainer**. Font-based (DejaVu Serif is on the system),
  with no ornament.
- Painted, illustrated style (Blando's Roadhouse, the Oraga paintings): **out of
  reach** procedurally, and not a target.

## 3. Outputs

- `<name>.png`: the map at `px_per_square`.
- `<name>.dd2vtt`: Universal VTT JSON with `format`, `resolution {map_origin,
  map_size (squares), pixels_per_grid}`, `line_of_sight` (wall polylines, in
  squares), `portals` (doors/windows: position, bounds, rotation, closed,
  freestanding), `lights`, and `image` (base64 PNG). It's built from the same
  `Geometry` the `wall`/`door` ops painted, so the image and the walls can't
  disagree.
- `<name>.meta.json`: named geometries in feet, plus each declared measurement
  (`measure: {floor: {w: 80, h: 140}}` in the recipe). Tests assert against it,
  the same way `tools/test_maps.py` reads `data-fact-*` today.

Outputs are generated, so nobody edits them by hand. Recipes live per adventure
(`conversions/dnd5e/oraga_night/maps/recipes/*.map.yaml`), and outputs go next to
them under `maps/mapgen/`. Generic and homebrew recipes live in `maps/` at the repo root.

## 4. The skill: `.claude/skills/build-map/`

```
SKILL.md                 # workflow below
references/ops.md        # GENERATED from the registry
references/cookbook.md   # worked recipes: stone room, cave, ruin clearing, tavern; how to fake common features
references/rubric.md     # the §7.3 rubric
```

**Workflow in SKILL.md:**
1. **Pin the brief:** size, grid scale, map type, features, mood. If it's a
   canon place, read the source text and `facts.yaml` first. Every feature must
   cite a line, and anything else is asked about (the iron law). Ask at most 3
   questions, or none if the description is complete.
2. **Block out:** write geometry only (rooms, walls, paths) and render `--draft`.
   Check the layout against the description.
3. **Dress:** add the style include, materials, shadows, props and overlay. Render `--draft`.
4. **Look and critique:** open the PNG (Read tool), score it against `rubric.md`,
   and list concrete defects ("door on the east wall reads as a gap; bridge
   floats over the bank").
5. **Revise:** edit the recipe and re-render. Stop when the rubric average is 4 or
   higher, or after **5 iterations**, then report the remaining defects.
6. **Final:** a full-resolution render, `python -m mapgen quality <png> --category
   <cat>` metrics, and a report to the owner with the PNG path and the dd2vtt path.

## 5. Dependencies

`numpy`, `Pillow`, `scipy`, `shapely`, `PyYAML`, `pydantic` (all present), plus
**`opensimplex`** (MIT), added to `software/requirements.txt` (T1). No skia, cairo
or GIMP. Fonts are DejaVu, with the path resolved via `PIL.ImageFont`, and a
recipe-level override.

## 6. Test strategy

| Layer | What proves it | Kind |
|---|---|---|
| Recipe/registry/engine | valid/invalid recipes, unknown op, wrong layer type, missing ref, include merge, macro expansion, seed stability under step insertion | unit |
| Geometry | areas/bounds exact in feet; booleans; roughen keeps area within ±10% and stays valid | unit |
| Rasterize | rect coverage = expected px within 0.5%; AA edges have fractional values; supersample downscale | unit |
| Fields | same seed gives identical arrays; different seed differs; range; scale_ft changes dominant frequency (FFT peak) | unit |
| Materials | determinism; flagstone mortar fraction in band; no flat fill (local std > floor) | unit |
| Semantic | wall emits LOS covering every edge of the geometry; door splits the LOS segment and emits one portal at the right square | unit |
| Export | dd2vtt validates against a pinned minimal schema; image round-trips; units are squares | unit |
| Golden | 3 tiny recipes (32×32 ft at 20 px/sq): PNG hash match; `--update-goldens` flag regenerates on purpose | regression |
| Canon proof | Crystal Court meta.json: floor 80×140 ft, aisles 20 ft (from `facts.yaml`, not literals) | invariant |
| Generated docs | `references/ops.md` == registry render | no-diff invariant |
| Quality | metrics on synthetic images behave (§7.2); proofs fall in comparator bands | proxy, skips without refs |
| Look | rubric scored from a side-by-side contact sheet; owner signs off | human/vision |

Minimum 3 tests per public function (CLAUDE.md). TDD: every task writes its tests first.

## 7. Quality bar: the comparator set

### 7.1 Comparators (local only, never committed)

These are the owner's own WotC map packs under `E:/books/DandD 5E/`. They're
copyrighted, so they are **used only as yardsticks**: metrics are computed from
them and they're viewed side by side. They are never traced, never sampled for
texture, never copied into the repo or a test fixture, and never published.
`software/mapgen/comparators.yaml` stores relative paths (zip + member),
category and grid scale. Tests that need them read `MAPGEN_REF_DIR`
(default `/mnt/e/books/DandD 5E`) and **skip** when it's absent. Extracted
copies live only in the session scratchpad or a git-ignored
`software/mapgen/.refcache/`.

| ID | Map (pack) | Category | Why it's the bar |
|---|---|---|---|
| C1 | Redbrand Hideout, DM version (*Lost Mine of Phandelver*, Mike Schley) | built interior | Dressed stone walls, doors, secret doors, flagstone floors, furniture, a natural chasm through the middle: nearly every v1 op in one map |
| C2 | Cragmaw Hideout, player version (*LMoP*, Schley) | cave | Rough cave walls, rapids, pool, bridge, rubble, stalagmites, briar/forest edge, escarpment hatching |
| C3 | Ruins of Thundertree, player version (*LMoP*, Schley) | outdoor battle | 10-ft grid, tree clumps, brush, dirt paths, intact vs ruined walls, contour dashes |
| C4 | Carnath Roadhouse (*Hoard of the Dragon Queen*, Blando) | built interior (painted style) | Different hand: wood floors, plank walls, stalls. Checks that metrics aren't tuned to one artist |
| C5 | Dragon Hatchery (*HotDQ*, Blando) | cave/dungeon (painted style) | Cobbled rock mass, cut rooms inside caves, stairs |
| C6 | Phandalin, player version (*LMoP*, Schley) | town (Phase 2) | Contour hills, roads, roofs, fields, tree clusters |
| C7 | North Sword Coast, player version (*LMoP*, Schley) | region (Phase 2) | Coast, hex overlay, forest mass, hills/mountain glyphs, rivers, labels |

Secondary, if needed: Raider Camp (cliffs, outdoor; HotDQ), Wave Echo Cavern (large
cave), Greenrest (town), the Rise of Tiamat packs.

### 7.2 Automated metrics (proxies)

`quality.py` normalises each image to **50 px per 5-ft square** (by the manifest's
measured px/square) and computes metrics on the map body (frame and legend
cropped by a manifest box):

| ID | Metric | Catches |
|---|---|---|
| Q1 | Tonal range: luminance P98 − P2 | washed-out or muddy maps |
| Q2 | Fine detail: mean local σ of luminance in 5-px windows | flat digital fills (the main weakness of the current SVGs) |
| Q3 | Mid-scale variation: σ of per-square mean luminance | no blotch/weathering, monotone floors |
| Q4 | Ink density: fraction of pixels with Sobel magnitude > t | too few or too many lines |
| Q5 | Palette: mean saturation and hue-cluster count (k-means, k ≤ 8, clusters > 2%) | garish or monochrome palettes |
| Q6 | Grid subordination (only if a grid is printed on request): ratio of grid-line contrast to wall-line contrast | grid shouting over walls |

**Bands:** for each category, `[min, max]` across its comparators, widened by
15%. A proof passes a metric if it lands in its category band. Bands are recorded
as numbers in `docs/RESEARCH_mapgen_comparators.md` (numbers only, no images), so
CI-style tests can use the recorded bands even where the reference packs are
absent. Metrics are proxies: passing them is necessary, not sufficient.

### 7.3 Rubric (vision + owner)

Contact sheet: our map beside the comparator of its category, at the same scale
(`python -m mapgen sheet`, written to the scratchpad, never committed). Score 1–5:

1. **Legibility:** walls, doors, elevation and hazards read at a glance, at VTT zoom
2. **Surface:** no flat fills; materials read as stone, wood, water, grass
3. **Depth:** shadows/occlusion separate floor, wall, raised and sunken
4. **Line:** ink weight hierarchy; natural edges organic, built edges true
5. **Palette:** cohesive, period-plausible, matches the category's references
6. **Grid:** none by default; if printed on request, aligned and subordinate
7. **Props:** recognisable at 1 square, consistent with the line style
8. **Shelf test:** could sit in a published module beside the comparator

**Pass:** average ≥ 4.0, no score below 3, and the owner agrees. The comparator
is scored too, so the gap is explicit.

## 8. Phase 2 and 3 (milestones only, decomposed later)

- **Region:** heightmap = fbm + control shapes (ridge paths, basin polygons) →
  light thermal/hydraulic erosion → sea level → zero-contour coastline (marching
  squares, `skimage`-free via a small implementation or `matplotlib.contour` if
  added) → flow accumulation and steepest-descent rivers (O'Leary) → biome masks →
  glyph scatter (mountain, hill, tree-mass) → hex/square overlay → curved labels.
  Comparator C7.
- **City/town:** district Voronoi, street graph along paths, lot subdivision,
  roofs with ridge shading, walls, fields (striped material). Comparator C6.
- **Web app (Phase 3):** load a `.dd2vtt` into a map view, tokens, room reveal.
  It needs its own BRIEF under the "5e in the Facets app" initiative.

## 9. Open questions (none blocking Phase 1)

1. Foundry import check: the owner runs one manual import of a proof dd2vtt (T20 acceptance note).
2. Do proofs replace any Oraga art? Not proposed. The Crystal Court proof sits
   alongside the painted map and the SVG until the owner rules.
3. Print resolution (140 px/sq) for the book. Deferred until the owner wants print maps.
