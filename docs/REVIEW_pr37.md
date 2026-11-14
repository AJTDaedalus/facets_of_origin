# Review: PR #37 `feat/mapgen-shading` (base `feat/lean-facets`)

Reviewer: independent agent, 2026-11-13. Scope: `git diff feat/lean-facets...feat/mapgen-shading`
(commit `b0fe059`). Verified against the code and by running scripts; `tests/mapgen` is green
(376 passed). Nothing tracked was modified.

Severity: **High** = wrong output / broken contract; **Medium** = visible inconsistency or real cost;
**Low** = cleanup, docs, test gaps.

## Summary

| ID | Sev | Status | One line |
|---|---|---|---|
| R1 | High | confirmed | `stipple` density depends on the frame size, not on the mask: same room gives 258 / 57 / 9 dots in a 12 / 40 / 120 ft frame |
| R2 | Medium | confirmed | `floor_fill` now has two depth cues pointing opposite ways: inner `shadow` darkens the S/E floor, `shade_lines` makes N/W strokes longest |
| R3 | Medium | confirmed | `forest_mass` / `brush` hatch the N/W interior of a raised canopy (the lit side); tree props shade the S/E crescent |
| R4 | Medium | confirmed | Tree shading crescent rotates with `scatter`'s default `rotate_jitter: 180`, so it lands on random sides while the drop shadow stays S/E |
| R5 | Low | confirmed | Cost: each line-work op works over the full frame (EDT + contour + composite). Whole-recipe cost is modest (+0 to +30 %), but it adds up per macro instance and is easy to cut |
| R6 | Medium | confirmed | Rubric criterion 6 ("Grid: present ... Missing = 2") now fails every default map; DESIGN §7 and cookbook still assume a grid |
| R7 | Low | confirmed | `finish` keeps dead params `floor`, `alpha`; recipes still pass `alpha:` and it is silently ignored |
| R8 | Low | confirmed | `crystal_court`: `walkable` combine is now unused (dead full-frame layer); header comment "grid, keys, frame" stale |
| R9 | Low | confirmed | Tests: nothing pins absolute stipple density, the `outside`+`shadow` case, holes/border/multi-part masks, `cracks` `branch`/`length`, or macro wiring (`finish` has no grid, `floor_fill` hatches); goldens don't touch line-work |
| R10 | Low | confirmed | `coastline` re-rasterizes `${land}` into `${name}_landm` when `${name}_land` already is that mask |
| R11 | Low | suspected | `stream` bank hatch (spacing 0.22 ft, length 1 ft) is sub-pixel at town scale (3.3 px/ft): strokes merge into a solid band |
| R12 | Info | confirmed | Inserting/removing macro steps shifts `#i` seeds for every later id-less step (pre-existing design; this PR re-rolls all id-less randomness downstream of each changed macro) |

Checked and found **correct** (no finding): see the end of this file.

---

## R1 (High, confirmed): `stipple` density is frame-dependent

`software/mapgen/ops/linework.py:168-175`

```python
area_ft2 = h * w / (fr.scale ** 2)
n = int(p.density * area_ft2 * float(prob_map.mean()) * 2)
ys = rng.integers(0, h, n * 2); xs = rng.integers(0, w, n * 2)
keep = rng.random(n * 2) < prob_map[ys, xs]
ys, xs = ys[keep][:n], xs[keep][:n]
```

With μ = `prob_map.mean()` and A the frame area, the intended count is D·A·μ (density × the
probability-weighted area). The code draws 2n = 4·D·A·μ candidates uniformly over the **whole frame**
and keeps each with probability `prob`, so the expected kept count is 4·D·A·μ², capped at n = 2·D·A·μ.
For μ < 0.5 the result is the intended count × 4μ. μ is the share of the frame the mask's band covers,
so the same room gets fewer dots the bigger the map around it.

Reproduction (`falloff: null`, density 2, 10×10 ft room, 100 ft²; intended ≈ 200 dots):

| frame | dots (connected components) |
|---|---|
| 12×12 ft | 258 |
| 40×40 ft | 57 |
| 120×120 ft | 9 |

In `cave_floor` on a full-size cave map the documented "6 dots per sq ft at the edge" is a small
fraction of that, and changes whenever the map is resized.

Fix: sample candidates only from the region (`idx = np.flatnonzero(prob_map > 0)`), draw
`n = rng.poisson(D * prob_map.sum() / scale²)` positions with probability ∝ `prob_map[idx]`
(`rng.choice(idx, n, p=prob/prob.sum())`), or do rejection sampling over the mask's bbox with
`n = D·Σprob/scale²` proposals ÷ mean acceptance. Add a test: a fixed room in two frame sizes gives
the same dot count within ±20 %, and that count ≈ D × area.

## R2 (Medium, confirmed): `floor_fill` shadow and hatching disagree on where the light is

`software/mapgen/styles/inked_parchment.yaml:97-100` (and `crystal_court.map.yaml:66-67`).

The `shadow` inner mode shifts the mask by `-offset` (`paint.py:203`), so `offset: [0.6, 0.8]` darkens
the **south/east** interior. `shade_lines` with the default `shadow: [0.6, 0.8]` makes strokes longest on
the **north/west** interior (it treats walls as casting shadow south-east onto the floor, which is the
physically consistent reading). Measured on a 30×20 ft room (mean darkness in a 2 ft band):

| op | north band | south band |
|---|---|---|
| `shadow inner offset [0.6, 0.8]` | 0.058 | 0.314 |
| `shade_lines` default | 0.175 | 0.085 (west 0.142, east 0.083) |

So every `floor_fill`/`stone_room`/`cave_floor` floor, and the canon Crystal Court, now carries soft
shading on one side and ink hatching on the other. Whether it reads badly is the owner's call (he liked
the renders), but it is not deliberate in the code or the log.

Fix: pick one convention. Either pass `shadow: [-0.6, -0.8]` to `shade_lines` in `floor_fill`/the court
(match the existing soft shadow), or flip the inner `shadow` offsets to `[-0.6, -0.8]` (match the
physics and the drop shadows). Add a test that the inner shadow and `shade_lines` darken the same side
for the macro's defaults.

## R3 (Medium, confirmed): raised masses are hatched on their lit side

`inked_parchment.yaml:183-184` (`brush`), `:224-225` (`forest_mass`).

`shade_lines side: inside` scales strokes by `dot(inward_normal, shadow)`. That is right for a sunken
area (floor next to a wall). For a raised mass (a canopy) the shadowed faces are the ones whose
**outward** normal points along the shadow, i.e. the S/E interior. With the default shadow the canopies
get long strokes on the N/W interior, the side facing the light, while their own drop shadow
(`offset: [0.3, 0.4]` / `[0.6, 0.7]`) falls S/E and the tree prop's new crescent sits S/E
(`props.py:159`).

Fix: pass `shadow: [-0.6, -0.8]` in those two macros, or add `relief: sunken|raised` to `ShadeLinesP`
(raised uses `out` instead of `dirv` in the share). Test: a raised square gets longer strokes inside its
south edge than its north edge.

## R4 (Medium, confirmed by code): tree shading rotates with the prop

`props.py:159-165` builds the shading in prop space; `draw_prop` (`props.py:300-303`) rotates every part
by `rotate`, and `scatter` defaults `rotate_jitter: 180` (`props.py:405`, used at `:442-444`). The drop
shadow is computed after rotation (`props.py:305-307`) and always falls S/E. So scattered trees
(`proof_ruins` passes no `rotate_jitter`) get shading strokes anywhere in a ±90° arc, sometimes on the
side opposite their shadow. (The older `mid`/`top` highlight offsets have the same flaw; the dark
strokes make it much more visible.)

Fix: build shading/highlight parts after rotation (return them flagged "unrotated", or have `draw_prop`
rotate only the silhouette parts), or have `scatter` default `rotate_jitter: 0` for `tree`. Test: render
one tree at rotate 0 and 180; the shading pixels' centroid stays S/E of the canopy centre in both.

## R5 (Low, confirmed): full-frame cost per line-work call

Each call does, over the whole working frame: `signed_distance` (two EDTs), `np.gradient` (two float64
frames), `contourpy` on the full mask, a full-frame PIL image, and `composite_inplace` over the whole
frame even though alpha is zero almost everywhere. `cracks` adds `np.argwhere` of the whole mask
(N×2 int64; ~65 MB for a 4 Mpx floor).

Profiled on 150×172 ft at 50 px/sq ×2 (3000×3440 = 10.3 Mpx, the Crystal Court frame), one rough
polygon mask:

| op | wall time | dominant cost |
|---|---|---|
| `shade_lines` (spacing 0.28, length 3) | ~9–14 s | EDT 4.6 s, contourpy ~5 s, composite 2.5 s; the per-stroke Python loop is minor (~0.2 s) |
| `stipple` (density 6) | ~4–7 s | EDT + composite |
| `cracks` (density 0.25) | <1 s | |

Python-traced peak memory for the run ~1.25 GB. `floor_fill` now does three EDTs (occlusion, shadow,
shade_lines) and `cave_floor` four.

Whole-recipe timings (full render, `--only-png`, base `feat/lean-facets` vs this branch, same machine):

| recipe | base | PR | change |
|---|---|---|---|
| crystal_court (3000×3440) | 263.3 s | 262.7 s | ±0 (the `shade_lines` cost is offset by the removed grid) |
| proof_cave | 17.1 s | 22.1 s | +5 s (+30 %) |
| proof_town | 128.3 s | 131.2 s | +3 s |
| proof_region | 110.5 s | 122.7 s | +12 s (+11 %) |

Peak RSS is unchanged (1.37 GB court, 2.2 GB region). The isolated profile above overstates the share in a
real recipe. Not a blocker, but the cost scales with the number of `floor_fill`/`brush`/`forest_mass` calls
and frame size.

Town (900×600 ft, 166 px/sq at 50 ft squares, ss 1) is only 2988×1992 px, so it is cheap; size is
driven by working pixels, not feet.

Fix: crop to the mask's bbox grown by `length` (+2 px) before EDT/contour/composite, and composite only
that window. Normals can come from the contour polyline itself (perpendicular to the local tangent,
oriented by sampling the mask a pixel away), which removes the EDT from `shade_lines` entirely. In
`cracks`, draw start points by rejection sampling in the bbox instead of `argwhere`.

## R6 (Medium, confirmed): docs that still require a grid

- `.claude/skills/build-map/references/rubric.md:13`: criterion 6 "**Grid** | Present, aligned ... | Missing,
  or louder than the walls". "Missing" scores 2, and the pass rule is "no criterion below 3", so every map
  built with the new default fails the rubric.
- `docs/DESIGN_mapgen.md:152` ("Grid present but subordinate"), `:276` (Q6), `:294` ("Grid: present,
  aligned, subordinate").
- `.claude/skills/build-map/references/cookbook.md:92` (outdoor example ends in `{op: grid, alpha: 0.7}`),
  `:154` (region example keeps the hex grid that this PR removed from `proof_region`), `:119` ("Grid
  fights the floor" defect row is fine but now unusual).
- `.claude/skills/build-map/SKILL.md:72` order "props → grid → overlay".

Fix: rubric 6 becomes "No printed grid by default (owner, 2026-11-13); if one is asked for: aligned,
subordinate"; drop the grid lines from the cookbook examples (or mark them optional); note the default in
SKILL.md and DESIGN §7.

## R7 (Low, confirmed): `finish` keeps dead params

`inked_parchment.yaml:243-244`: `params: {floor: floor, alpha: 0.28}` but no step uses them;
`ops.md:918` still documents them; `proof_cellar.map.yaml:74` passes `alpha: 0.16` and `proof_cave.map.yaml:48`
passes `floor: walk`, both now silently ignored. Fix: drop them, or turn them into an opt-in
(`grid: false`, `floor`, `alpha`) so `{op: finish, grid: true}` restores the old behaviour.

## R8 (Low, confirmed): Crystal Court leftovers

`crystal_court.map.yaml:164-165`: the section is still headed "grid, keys, frame" and
`{op: combine, out: walkable, ...}` is now computed for nothing (a full-frame layer at 10 Mpx). Remove it,
or keep it only if `measure:` or a test needs it (none does; `grep walkable` finds only this line).

Canon check: the added `shade_lines` (`:67`) is styling on the existing `ground_m`; it draws no new
feature, uses no cracks (which would contradict "seamless grown crystal, no mortar joints"), and stays
inside the canon floor. OK. It inherits R2's opposite-sides issue with the court's inner shadow.

## R9 (Low, confirmed): test gaps

`software/tests/mapgen/test_linework.py`. What the tests do catch: a reversed outward normal (strokes
would be masked away, `test_strokes_hug...` fails), a swapped or reversed shadow vector
(`test_longer_on_the_shadow_side` fails), non-determinism. What they miss:

1. Absolute stipple density / frame independence (R1 would have been caught).
2. `side: outside` with a shadow vector (only `shadow: None` is tested); the outside test's
   `a[:19, 30:130].any()` is satisfied by one pixel.
3. Masks with holes (a pillar: the floor south of it should get the long strokes; it does, 55 vs 31 px,
   but nothing pins it), masks touching the border, multi-part masks, empty/full masks for
   `shade_lines`/`stipple` (only `cracks` has an empty-mask test). All of these run without error today
   (checked), so these are regression guards, not bugs.
4. `cracks`: `branch` and `length` have no effect test; nothing checks cracks stay inside a mask with a hole.
5. Macro wiring: no test that `finish` draws no grid or that `floor_fill` emits hatching; the three
   goldens use no macros and no line-work ops, so a regression in `linework.py` changes no golden.
6. Different `id`s give different strokes (seed actually keyed by id).

## R10 (Low, confirmed): redundant rasterize in `coastline`

`inked_parchment.yaml:210`: `${name}_landm` is the same rasterization as `${name}_land` (`:192`). Use
`${name}_land` (it simply lives a few steps longer) and save one full-frame rasterize.

## R11 (Low, suspected): bank hatch at town scale

`stream` (`inked_parchment.yaml:151-152`) hard-codes `spacing: 0.22, length: 1.0, width: 0.07` in feet. In
`proof_town` (3.3 px/ft) that is a stroke every 0.73 px, 3.3 px long, so the bank becomes a solid 3 px band
rather than hatching. Expose `bank_spacing`/`bank_length` params or scale them from the stream width.
(Not visually verified here.)

## R12 (Info, confirmed): seed keys shift with step count

`engine.py:139-141` keys id-less steps by index (`#i`). Adding steps to `floor_fill`, `cave_floor`, `brush`,
`forest_mass`, `coastline`, `stream`, and removing `grid` from `finish` and three recipes, renumbers every
later id-less step, so their randomness re-rolls. Expected and pre-existing; mention it in the log so the
owner knows unrelated noise changed between v1 and v2 renders.

---

## Checked and correct

- **Coordinates.** `contourpy` returns (x, y) in array-index space (pixel centre = integer), which is the
  space PIL draws in; `rasterize_patch` maps feet to `x*s - 0.5` in the same convention. No half-pixel
  offset. The `int()` truncation for the gradient lookup is ≤1 px and harmless.
- **Normal sign.** `signed_distance` is positive outside, so `np.gradient` points outward; `dirv = -out`
  for `inside` is correct.
- **Shadow vector.** `[0.6, 0.8]` with y south is south-east, matching the docstring; north-wall floor gets
  long strokes for `shadow: [0, 1]`, as intended.
- **Holes / border / tiny / empty / full masks.** All run cleanly (contourpy emits no contour along the
  frame border; constant `signed_distance` gives zero gradient and is skipped). Pillar holes are handled
  right.
- **Jitter.** `jitter` and `min_share` are bounded to [0, 1], so `L ≥ 0`, and `L < 1 px` is skipped.
- **RNG.** All three ops use only `ctx.rng` (seeded per step from map seed + id); macro ids
  (`${name}_hatch`, `_cracks`, `_grit`, `_bank`, `_shore_hatch`) don't collide across different macros.
  Duplicate ids are accepted by the engine (pre-existing), so two `floor_fill` calls with the same `name`
  share seeds, but they would also overwrite the same mask.
- **`cracks` maths.** `density` is per grid square (pixels → ft² → squares is right). Per-step fork
  probability `branch·step/length` gives ≈ `branch × 0.85` expected forks per crack (mean length factor
  of U(0.5, 1.2)), so "forking with chance `branch`" is a fair description.
- **`ops.md`** matches `python -m mapgen ops --markdown` exactly.
- **Macro param types.** `${hatch}`/`${cracks}` substitute as numbers: proof_cave, proof_town, proof_region
  and crystal_court all render cleanly on this branch.

---

## Resolution (2026-11-13, by the PR author)

One shading convention for the whole style, documented in `linework.py`, SKILL.md and DESIGN §2.5: **light from the north-west, shadows fall south-east.** A sunken area is shaded inside its north and west edges; a raised mass inside its south and east edges.

| ID | Resolution |
|---|---|
| R1 | `stipple` samples only inside the weighted area: dots = density × Σweight ft². The same 10×10 ft room gives the same count in 12, 40 and 120 ft frames (tested), and ~100 dots for 100 ft² at density 1 (tested). |
| R2 | The inner `shadow` offset is now `[-0.6, -0.8]` in `floor_fill` (and `[-0.8, -1.0]` in the court, `[-0.5, -0.6]` and `[-0.6, -0.8]` in the ruins and cellar recipes), so the soft shadow and the hatching both darken the north/west floor. Measured first: a positive offset darkens the south (0.54 vs 0.15). Tested via `floor_fill`. |
| R3 | `brush` and `forest_mass` hatch with `shadow: [-0.6, -0.8]`, and their inner shadows flip to positive offsets, so raised masses are shaded on their south-east side. Tested via `brush`. |
| R4 | Trees and bushes ignore `rotate` (round canopies), so their shading crescent always sits south-east. Tested. |
| R5 | All three ops crop to the mask's bounding box plus the stroke margin (`_crop`) and composite a patch. |
| R6 | Rubric criterion 6: no grid by default; a printed grid only on request. SKILL order line, a shading-convention rule, cookbook examples and the defects table, and DESIGN §2.5, §2.3, §7.2 and §7.3 all updated. |
| R7 | `finish` takes no params, and the recipes were updated. The engine now rejects any param a macro doesn't declare (tested), so silent ignoring can't recur. |
| R8 | The unused `walkable` layer and the stale "grid" comment are gone from the court recipe. |
| R9 | Added tests: absolute stipple density; `side: outside` with a shadow vector; a mask with a hole; a mask at the border; crack length and branching; macro wiring (`floor_fill`, `brush`, `stream bank`); tree orientation; macro param validation. New golden `linework_room` exercises all three ops. |
| R10 | `coastline` reuses its `${name}_land` mask. |
| R11 | `stream` takes a `bank` length param, so town-scale recipes can lengthen the bank strokes. |
| R12 | Documented: every line-work step inside the style's macros carries an `id`, and the cookbook already tells authors to give scatter and noise steps one. |

Tests: full suite (excluding e2e) **2293 passed**.
