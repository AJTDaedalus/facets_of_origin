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
