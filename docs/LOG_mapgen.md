# LOG — mapgen

Running execution log for `docs/TASKS_mapgen.md`. Newest at the bottom.

## 2026-11-13 — M0 + M1 (T1–T10)

- **T1–T6:** `software/mapgen/` skeleton: recipe models with field-named errors,
  includes (beside the recipe, then `mapgen/`), op defaults, macros with typed
  `${param}` substitution and a recursion guard, `Frame` units, typed layer
  store with `~mask` inversion, op registry, an engine with a dry validation pass,
  per-step seeds keyed by step `id` (stable when steps are inserted), and liveness
  freeing. CLI stubs for `render|ops|quality|sheet`.
- **Deviation (DESIGN §5): no opensimplex.** Without numba it's pure Python:
  `noise2array` took 0.32 s for 200² px, so ~30 s per octave at 2000². Replaced
  by `mapgen/noise.py`: vectorised numpy Perlin gradient noise (16 gradients,
  quintic fade), with low-frequency octaves sampled at 8 points per wavelength
  and cubic-upsampled. No new dependency, so `requirements.txt` is unchanged.
- **T7–T10:** geometry ops (rect, polygon with holes and repair, circle, ellipse,
  path with Chaikin smoothing / line mode, union, intersect, subtract, offset,
  roughen_geom), rasterize (4× or 2× AA, pixel-centre convention, so a 30×40 ft
  rect at 70 px/sq covers 420×560 px within 0.5%), mask ops on a signed distance
  field (grow, shrink, blur, threshold, invert, band, combine, roughen).
- Tests: `python -m pytest tests/mapgen -q` → **79 passed**.

## 2026-11-13 — M2 + M3 (T11–T18)

- **T11–T12:** `noise` op (fbm/ridged/billow, scale in feet), `gradient`
  (linear/radial), `distance` (outside/inside/signed, feet), `remap` (linear,
  smooth, pow), `field_to_mask`, `mix`. Test note: Perlin has a broad low-pass
  spectrum, so "frequency tracks scale" is tested on the power-weighted spectral
  centroid (scale 8 vs 32 gives a ratio of ~4.7), not the argmax.
- **T13:** `mapgen/color.py`: hex/palette/list colours with palette aliasing,
  colour ramps, premultiplied compositing with normal/multiply/screen/overlay/
  darken/lighten. `canvas` and `fill` (colour or material, opacity, blend).
- **T14–T16:** materials `flat`, `ramp_noise`, `dirt`, `bedrock_hatch`,
  `flagstone` (jittered-grid Voronoi with F1/F2 mortar, or ashlar), `planks`,
  `cobble`, `grass` (with tufts), `water` (depth from the shore, ripples). A
  shared `grain` adds fine grit so no surface is digitally flat (Q2).
- **T17–T18:** `stroke` (mask edge by SDF, or geometry outline with dash/double/
  roughness/side), `shadow` (inner/drop), `occlusion`, `hatch` (stroke clusters),
  `paper`, `vignette`. Roughness got a 2× gain so `amount`/`roughness` read as
  feet of wobble (fbm rarely nears ±1).
- Tests: **149 passed**.

## 2026-11-13 — M4 + M5 (T19–T26)

- **Patch rasterization:** `rasterize_patch` renders only a geometry's bounding
  box, so props and openings don't allocate a full frame each (a 120×160 ft map
  at 70 px/sq ×2 is 15 M px).
- **T19:** `wall`: band outside the floor (dressed / rough / ruined with
  noise-chosen gaps), filled and inked, LOS from the kept edges, registered by
  name for openings.
- **T20:** `door`, `double_door`, `secret_door` (red S, secret portal),
  `portcullis`, `window` (LOS kept: UVTT has no window type, so walls still
  block), `opening` (floor fill, LOS cut, no portal), `stairs`, `light`
  (+ glow). Openings snap to the nearest edge of the named wall, with the normal
  pointing away from the floor.
- **T21–T22:** 19 props built from shapely parts (fill + ink + soft shadow);
  `scatter` with Bridson Poisson disk, mask/region/avoid, count = density ×
  squares.
- **T23:** `grid` (lines on pixel columns, optional clip, mask kept for Q6),
  `compass`, `scale_bar`, `title` cartouche, `label` (halo or ring), `frame`,
  `legend`. DejaVu Serif via Pillow.
- **T24–T26:** `export.render_recipe` → PNG (LANCZOS from working res),
  `.dd2vtt` (format 0.3, units in squares, base64 image), `.meta.json` (declared
  vs actual measures, all named geometry). CLI `render` / `ops [--markdown]`
  (exit 2 with the step named). Three goldens hashed on pixels; update with
  `MAPGEN_UPDATE_GOLDENS=1`; stable across processes with different
  PYTHONHASHSEED.
- Visual check of the goldens (scratchpad): correct but plain (no style yet).
  Defect noted for T30: rough walls spike at very sharp polygon corners (mitred
  buffer).
- Tests: **222 passed**.

## 2026-11-13 — M6 (T27–T29)

- **T27:** `mapgen/quality.py`: Q1–Q5 (Q5 split into Q5s mean saturation and
  Q5h hue families) on images normalised to 50 px/square with crop + exclude
  boxes; `q6` grid/wall contrast ratio for our renders.
- **T28:** `comparators.yaml` (C1–C7). Grid scales measured by spectral
  periodicity of edge energy and checked by eye on full-res crops with tick
  marks: C1 82, C2 150, C3 150 (10-ft squares), C4 77, C5 55 px/sq (the x-axis
  spectrum picked the half period; y and the eye give 55). C6 from its scale bar;
  C7 normalised by width. `python -m mapgen quality --baseline --research
  docs/RESEARCH_mapgen_comparators.md` wrote `quality_bands.yaml` and the
  RESEARCH table (numbers only; ~60 s to read the packs). The live-comparator
  test ran here (packs present) and matches the recorded values.
- **T29:** `make_sheet` / `python -m mapgen sheet` (refuses any path inside the repo).
- Tests: **239 passed**.

## 2026-11-13 — M7 (T30–T35)

- **T30:** `styles/inked_parchment.yaml`: palette, ink weights (bold/heavy/medium/
  fine), 18 materials (incl. `crystal_floor`/`crystal_wall` with veins, `meadow`,
  `thicket`, `earth`), and macros `base`, `beyond`, `floor_fill`, `stone_room`,
  `cave`(=`cave_floor`+`cave_walls`), `stream`, `ground_patches`, `brush`, `finish`.
  New engine pieces found while building the proofs: `trace` (mask → polygons via
  contourpy, holes kept), `partition` (interior wall that takes doors), wall
  `exclude` and `outer_weight`, stroke `jitter`, the `pebbles` prop, and ramp `veins`.
- **Dependencies:** mapgen's imports (numpy, scipy, shapely, Pillow, contourpy)
  weren't declared anywhere; they're now pinned in `software/requirements.txt`. All
  are permissively licensed.
- **Metric fix:** metrics now normalise per **foot** (10 px/ft). Before that,
  10-ft-square Thundertree compared at half scale. The baseline was re-run; only C3
  changed.
- **Performance:** noise upsampling moved from `map_coordinates` to Pillow bicubic
  (cave render 38 s → 23 s). A full render runs at about 1 s per 100 ft² at 70 px/sq.
- **T31:** `conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml`, canon
  only (facts.yaml plus what `build_maps.map_court` draws; TP74 colour).
  `tests/mapgen/test_m7_proofs.py` checks floor, aisles, terrace width, dais and its
  distance from the doors, musicians' gallery, main-door width and west-door stations
  against facts.yaml (no literals), and that no props beyond doors/stairs are drawn.
- **T32:** `maps/recipes/proof_cave.map.yaml`, `maps/recipes/proof_ruins.map.yaml`,
  each built from the TASKS description only, by the render → look → critique →
  revise loop the skill describes.
- **T34:** `.claude/skills/build-map/` (SKILL.md, generated `references/ops.md`
  with a no-diff test, `cookbook.md`, `rubric.md`).
- **T35 (partial):** CLAUDE.md generated-files list, regenerate line and trigger row.
  Full suite from `software/` (excluding e2e): **2109 passed**; mapgen alone **262
  passed**. The PR waits for the owner's T33 review.

### T33 quality gate — results (final renders, 2026-11-13)

| Proof | Category (comparator) | Q1 | Q2 | Q3 | Q4 | Q5s | Q6 | Rubric (self) |
|---|---|---|---|---|---|---|---|---|
| B cave | cave (C2 Cragmaw) | 0.759 ✓ | 0.077 ✓ | 0.112 ✓ | 0.168 ✓ | 0.170 ✓ | 0.49 ✓ | ≈3.8 (comparator 5) |
| C ruins | outdoor (C3 Thundertree) | 0.793 ✓ | 0.068 ✗ (≥0.074) | 0.174 ✓ | 0.130 ✗ (≥0.140) | 0.186 ✓ | 0.47 ✓ | ≈3.9 |
| A court | built_interior (C1 Redbrand) | 0.663 ✓ | 0.043 ✗ (≥0.054) | 0.123 ✓ | 0.051 ✗ (≥0.109) | 0.250 ✓ | 0.47 ✓ | ≈3.2 |

Rubric detail (self-scored by vision from the contact sheets; owner to confirm):
- **Cave:** legibility 4, surface 4, depth 4, line 3.5, palette 4, grid 4, props 3.5,
  shelf 3.5. Weakest: props and the wall band (plain next to Schley's).
- **Ruins:** 4, 4, 4, 4, 4, 4, 3.5, 3.5. Weakest: the path's tone sits too close to
  bare earth; trees are a step below Schley's.
- **Court:** legibility 4, surface 3.5, depth 2.5, line 3, palette 3, grid 3.5,
  props 3, shelf 3.

The ruins pass all five Q bands with a Thundertree-strength grid (alpha 0.7), but
then Q6 = 1.07. With a quiet grid (alpha 0.26, kept) Q6 = 0.47, while Q2/Q4 fall
5–7% short. The grid was carrying that ink. Adding ground detail instead didn't
recover it (tried and reverted).

No proof reaches the ≥ 4.0 rubric bar. The cave and ruins are close. The court
is not.

## ESCALATION (T33 → owner; per TASKS "category below 3.5 after 3 rounds")

**What was attempted:** three tuning rounds on the Crystal Court (veined crystal
material, desaturation, heavier walls, darker grid, then a quieter grid).
Q2 (fine detail) and Q4 (ink density) stay well under the built-interior band,
and the rubric is ≈3.2.

**What's specifically wrong:**
1. **The yardstick doesn't fit.** The built-interior comparators (Redbrand,
   Carnath) are stone dungeons packed with furniture and block texture. The canon
   Crystal Court is a 120×140 ft empty ballroom with no furniture or mortar joints
   (TP60/TP74), so it can't reach their detail density without inventing content.
2. **Canon palette vs metrics.** Pushing Q5s into band desaturated the floor from
   TP74's "deep, dusky purple-pink glowing out of violet-charcoal shadow" toward
   grey mauve marble. I stopped there, not drifting further from canon.

**Questions for the owner:**
- (a) Is the court judged on its own (canon look, legibility, VTT data) and dropped
  from the metric bands? Or should we pick a different canon interior with
  furniture text as the built-interior proof?
- (b) Should the court's floor go back to stronger purple-pink glow (TP74 over
  Q5s)?
- (c) Grid: Thundertree-loud (passes Q1–Q5, fails Q6) or quiet (passes Q6, misses
  Q2/Q4 slightly)? The VTT can draw its own grid either way.
- (d) Do the cave and ruins clear your eye at ≈3.8–3.9, or what's missing first:
  props, trees, wall texture?

Review images (scratchpad, never committed, since the sheets contain comparator crops):
`/tmp/claude-0/-root-facets-of-origin/eb46f7a0-189d-4dd6-848a-6d5e583a84cc/scratchpad/final/`
(`proof_cave.png`, `proof_ruins.png`, `crystal_court.png`, and `sheet_*.png` beside the
comparators). Rebuild any time with `cd software && python -m mapgen render <recipe>`.

## 2026-11-13 — T33 round 2 (independent work while the court escalation waits)

- **Proof D added:** `maps/recipes/proof_cellar.map.yaml`, a furnished generic
  dungeon (guard room, storeroom, barracks, corridor, partitions with doors, a
  secret door, stairs, keyed rooms), so the built-interior category has a fair
  proof alongside the empty canon court. It renders in `test_m7_proofs.py`.
- **Engine/style:** grass `tuft_length`/`tuft_width` (the old sub-pixel tufts
  vanished on downscale); trees with more interior ink; rounder stalagmites with
  cracks; a darker tan `dirt_path` that stands out from bare earth; a slightly
  brighter `earth` highlight; textured `thicket` for the cave's forest edge;
  quieter grids so Q6 < 0.5 everywhere.

| Proof | Q1 | Q2 | Q3 | Q4 | Q5s | Q6 | Rubric (self) |
|---|---|---|---|---|---|---|---|
| B cave (C2) | 0.757 ✓ | 0.079 ✓ | 0.117 ✓ | 0.167 ✓ | 0.165 ✓ | 0.49 ✓ | ≈3.9 |
| C ruins (C3) | 0.794 ✓ | 0.076 ✓ | 0.166 ✓ | 0.148 ✓ | 0.197 ✓ | 0.47 ✓ | ≈4.0 |
| D cellar (C1) | 0.778 ✓ | 0.086 ✓ | 0.137 ✓ | 0.192 ✓ | 0.164 ✓ | 0.48 ✓ | ≈4.0 |
| A court (C1) | 0.663 ✓ | 0.043 ✗ | 0.123 ✓ | 0.051 ✗ | 0.250 ✓ | 0.47 ✓ | ≈3.2 (escalated) |

The three generic proofs now pass every automated band and sit at about the 4.0
rubric bar on my reading; the owner's eye is the final gate. The ESCALATION above
(court yardstick, TP74 palette) still stands; its question (c) about the grid is
answered provisionally by the quiet grid now passing all bands on B, C and D.
Tests: mapgen **263 passed**.

## 2026-11-13 — Phase 2 region maps (R1–R7) and the court colour variant

- **Court colour (for escalation question b):** a TP74 glow variant was rendered
  next to the committed dusky one, at
  `/tmp/claude-0/-root-facets-of-origin/eb46f7a0-189d-4dd6-848a-6d5e583a84cc/scratchpad/final/court_palette_compare.png`
  (left: committed, Q5s 0.25; right: glow, Q5s 0.43). No recipe change: this is
  the owner's call.
- **R1:** header `unit: ft|mi` (ft keeps 5/10-ft squares; mi allows any hex
  size), hex grid (flat/pointy, sized across the flats), scale note "1 hex = 5 miles".
- **R2:** `isolines` (contourpy lines at levels or an interval), `erode` (thermal,
  exactly mass-conserving).
- **R3:** `rivers`: priority-flood depression fill, D8 receivers, accumulation;
  rivers end at the sea, the edge or a larger river, and taper wider downstream.
  New module `ops/terrain.py`.
- **R4:** glyphs `mountain` (lit and shaded faces, hatching), `hill` (radially
  hatched dome), `peak`, `city`, `town`, `village`, `ruin_marker`, `conifer`;
  markers cast no shadow. `scatter sort_y` for north-to-south overlap.
- **R5:** materials `sea`, `lowland`, `upland`, `marsh`, `forest_canopy` (dome-shaded
  cells read as tree crowns); macros `coastline` (shore ink, shallows, five wave
  lines, sea hatching), `forest_mass`, `mountain_range`. `quality --category
  region` compares at the comparator's width.
- **R6:** `maps/recipes/proof_region.map.yaml` from the generic description; it
  renders in 2 minutes at 1500 px wide. The first measurement ran at 600 px wide,
  and upscaling for comparison erased the fine detail, so the resolution was raised
  to print scale (125 px per hex).

| Proof | Q1 | Q2 | Q3 | Q4 | Q5s | Rubric (self) |
|---|---|---|---|---|---|---|
| E region (C7 North Sword Coast) | 0.770 ✗ (≥0.797) | 0.077 ✗ (≥0.099) | 0.109 ✗ (≥0.117) | 0.154 ✗ (≥0.263) | 0.319 ✓ | ≈3.7 |

  Rubric: legibility 4.5, surface 3.5, depth 3.5, line 3.5, palette 4, grid 4,
  glyphs 3.5, shelf 3.5. It's legible and reads as a hand-drawn region map; the
  Schley region map is far denser (fine hatching on every surface, labels along
  curves). Next levers: curved labels, mountain-range shading masses under the
  glyphs, forest edge trees, marsh glyphs.
- **R7:** cookbook region section; ops.md regenerated; mapgen **289 passed**.

**City maps (2b)** and the **web-app map view (3)** are next. Both need owner
input on priority (see BRIEF Phase 3: it belongs to the wider 5e-in-the-app
initiative).

## 2026-11-13 — Phase 2b town maps (C1–C4)

- `feet_per_square` 25/50/100 for town maps; `ops/city.py`: `frontage` (lots
  along streets) and `buildings` (gabled roofs); `field_tilled`/`field_green`
  (planks as plough rows) and `town_grass` materials; cookbook town section.
- **Proof F** `maps/recipes/proof_town.map.yaml`, generic description in the
  header, 900×600 ft at 3.3 px/ft (the comparator's scale). A full render takes about 2 minutes.

| Proof | Q1 | Q2 | Q3 | Q4 | Q5s | Rubric (self) |
|---|---|---|---|---|---|---|
| F town (C6 Phandalin) | 0.740 ✓ | 0.034 ✓ | 0.118 ✗ (≥0.145) | 0.052 ✓ | 0.255 ✓ | ≈3.6 |

  Five tuning rounds. Round 4 got every metric within 5% but turned the map
  dark green, so I backed off: Q3 is out and the look is kept. The rubric's job
  is exactly this kind of call. Gap: the layout is too regular (straight streets,
  houses in rows); Phandalin is organic. That's task C5.
- mapgen tests: **300 passed**.
