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
