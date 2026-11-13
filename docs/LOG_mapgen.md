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
