# Review: PR #40 engine code (`feat/lean-facets..feat/mapgen-gaps`, `software/mapgen/`)

Scope: correctness only. Every item below was reproduced with `tests.mapgen.helpers.run/layer` on the
`H` map from `tests/mapgen/test_coast_tools.py` (40x30 ft, 8 px/ft). `tests/mapgen` passes (549). Checked and found clean:
atmosphere skipping and macro propagation (skip == recipe with the step removed), layer freeing for the new
`clip` / `weight` refs, footprint tag alignment, directional-noise orientation and stretch=1 identity,
recipe-level style keys, `facing` maths, nested `warp`, noise-mode `roughen_geom` unchanged, defaults unchanged.

## R1. `footprints` `of:` cannot name a macro call (medium)
`ops/props.py:691-696`. Macro body steps get ids `"<call id>/<n>"`, so the id the author wrote on the call never matches.
- Input: macro `rocks` (one `scatter`), steps `[{op: rocks, id: r1}, {op: footprints, of: [r1], out: f}]`.
- Observed: `RecipeError: footprints: no earlier step has id r1`. The tags really are `('r1/0','boulder')`.
- Expected: `of: [r1]` selects the footprints of every step the call expanded into.
- Fix: match with `sid == i or sid.startswith(i + "/")`, and use the same test in the `earlier` existence check.

## R2. `cells` allocates without bound for a sub-pixel `scale` (medium, pathological)
`ops/fields.py:65`. `scale` is only `gt=0`, and the point lattice is `(w/s) x (h/s)`.
- Input: `{op: cells, scale: 0.003}` on the 40x30 ft map (0.024 px cells): about 51 s and 6.2 GB RSS. `scale: 0.001` is about 1.2e9 points, which is OOM.
- Expected: a validation error, or a clamp.
- Fix: reject or clamp `fr.px(scale) < ~1` (e.g. `s = max(s, 1.0)`), or cap `nx*ny` and raise `RecipeError`.

## R3. `_tapered` samples at `n <= 200` equally spaced points, so corners get cut (low-medium)
`ops/paint.py:91-93`. The original vertices are dropped, so any polyline longer than `200 x width` loses its sharp corners.
- Input: `LineString([(0,0),(500,0),(500,500),(0,500)])`, width 0.3, taper 0.0001.
- Observed: the polygon stops 2.1 ft short of the corner (500,0), and area is 448 against 450 expected. Short lines are fine (0.0 ft).
- Expected: corners reproduced like the untapered buffered stroke.
- Fix: build `t` from the union of the original vertex arc-lengths and the uniform samples, then cap the count.

## R4. `_cusp_ring` phase is discontinuous at the ring seam (low, visual)
`ops/geometry.py:169-172`. `s` starts at 0 on vertex 0 and never wraps to a multiple of `period`, so the last vertex jumps to the first.
- Input: `box(0,0,19,10)` (perimeter 58, 58 mod 4 = 2), segmentized at 0.25, `amount=1, period=4, jitter=0`.
- Observed: last-to-first vertex gap is 1.02 ft, against 0.25 ft spacing: a one-segment spike or step in the outline. A 20x10 box (perimeter divisible by 4) shows 0.45.
- Fix: for closed rings, rescale `s` so the perimeter is a whole number of periods (`s *= round(P/period)*period / P`).

## R5. Cusps on a polygon with holes leave sliver holes (low, visual)
`ops/geometry.py:229` and `polygonal()`. Pushing a hole's ring into the void at sharp corners self-intersects.
- Input: 20x15 rect minus 6x5 rect (hole area 30), `mode: cusps, amount: 0.8`.
- Observed: the hole becomes three rings with areas 0.17, 18.1 and 0.04. At `amount: 0.3` there is a 0.0 area ring. Noise mode gives one hole (30.8).
- Fix: `make_valid`/`buffer(0)` then drop interior rings under a small area. Alternatively clamp `amount` to under half the narrowest hole width.

## R6. `facing` and curl `warp` crash on a 1-pixel-tall or 1-pixel-wide map (low, edge)
`ops/fields.py:87` and `:125`. `np.gradient` needs at least 2 samples per axis.
- Input: `noise` then `facing` on a map with `width_ft: 0.1, height_ft: 0.1`.
- Observed: raw `ValueError: Shape of array too small to calculate a numerical gradient`, not a `RecipeError`.
- Fix: return a zero mask when either side is under 2 px (or raise `RecipeError`).

## Outcomes

All six are fixed, each with a regression test in `tests/mapgen/test_coast_tools.py::TestReviewFixes` (8 tests). The R4 and R5 tests were checked to fail on the old code.
- **R1:** `footprints` `of:` matches a macro call's body steps (`id/n`). A longer id with the same start, such as `r10` for `r1`, does not match.
- **R2:** `cells` raises a `RecipeError` when `scale` is under one pixel.
- **R3:** `_tapered` samples every original vertex as well as the uniform points.
- **R4:** the cusp phase on a closed ring is rescaled to a whole number of periods.
- **R5:** cusped polygons go through `buffer(0)`, which drops holes smaller than `amount²`.
- **R6:** `facing` returns an empty mask, and curl `warp` returns its input, when the map is under 2 px on a side.
