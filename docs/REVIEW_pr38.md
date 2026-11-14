# Review: PR #38 `feat/mapgen-detail` (base `feat/lean-facets`)

Reviewer: independent agent, 2026-11-13. Scope: `git diff feat/lean-facets...feat/mapgen-detail`
(one commit, 08cf55b). I checked everything against the code and against renders and scripts. I did
not rely on the PR text. Nothing tracked was modified.

**Suite:** `cd software && python3 -m pytest tests/mapgen -q`: **405 passed** (72 s).

**Method:** I ran scratch scripts through the real `Engine` (`tests.mapgen.helpers.run`) and
rendered `proof_cave` both full and `--draft`. I also rendered a 16-prop contact sheet at 20 px/ft
with the inked_parchment style. Mutation checks on the new tests swap in a NW crescent, remove the
hatch, and remove the detail lines and the wall texture. The scripts are in the session scratchpad
and are not part of the repo.

Severity scale: **High** = wrong output on canonical or proof maps, or a feature that silently does nothing; **Medium** =
visible defect in a common case / test that cannot catch its own regression; **Low** = polish,
edge cases, perf notes.

---

## Summary table

| ID | Sev | Status | Where | One line |
|---|---|---|---|---|
| R1 | High | Confirmed | `ops/props.py:100-107` (`p_chest`) | Chest board lines are drawn *before* the chest fill and are painted over (3 px differ in a 6 ft chest) |
| R2 | High | Confirmed | `styles/inked_parchment.yaml:139-143` (`cave_walls`) | Rock texture is drawn inside an `exclude`d cave mouth (270 of 640 px in the mouth strip); hits `proof_cave` and every `cave` with `exclude` |
| R3 | Medium | Confirmed | `ops/props.py:29,366` (`NO_AUTO_SHADE`) | `mountain` and `hill` already shade themselves and get a second hatch; `mountain` is a side-view glyph, so an overhead SE crescent is the wrong projection |
| R4 | Medium | Confirmed | `ops/props.py:364-369` | Inner, highlight and sunken parts are hatched too: boulder/stalagmite highlights, hill `top`, the barrel lid, the brazier fire and coal, the statue star |
| R5 | Medium | Confirmed | `ops/props.py:308-327` (`shade_crescent`) | The crescent depth `k = 0.2·sqrt(area)` ignores how thin a part is. Thin axis-aligned parts are hatched all over; thin parts on a NW-SE axis are hatched only at one end cap; on a SW-NE axis the hatch runs parallel to the part |
| R6 | Medium | Confirmed | `ops/props.py:366-369` | Performance: auto-shading makes prop drawing 2-4x slower, about 12-22 ms more per prop (see table) |
| R7 | Medium | Confirmed | `tests/mapgen/test_detail.py` | 4 of the 7 test functions pass with the feature removed (mutation results below) |
| R8 | Medium | Confirmed | `styles/inked_parchment.yaml:24-27` | The heavier `ink:` weights change the canon `crystal_court` map (wall bold/heavy, partitions, dais, high table) with no owner note and no golden |
| R9 | Low | Confirmed | `styles/inked_parchment.yaml:139-140` | `cave_walls` band is a straight offset of the smooth `src`, not the rough wall band, so texture spills past the rough outer edge (by up to about 0.6·t where the wall narrows to 0.4·t) and misses the bulges |
| R10 | Low | Confirmed | `styles/inked_parchment.yaml:110-113,139-143` | Calling a macro twice with the same `wall` silently reuses the layer names `${wall}_inside`/`${wall}_band` and the ids `${wall}_*_cracks/grit`; equal ids give equal seeds |
| R11 | Low | Confirmed | `ops/props.py:87` (`p_crate`) | `.difference(i)` and the `is_empty` filter are dead code: the board lines at y = ±0.44·s never meet the inner box (±0.38·s). The boards sit on the N/S members only and read as a second outline |
| R12 | Low | Suspected | `styles/inked_parchment.yaml:24-27`, `ops/paint.py:86-93` | Weights are absolute map units. On the region proof (unit: miles, 25 px/mi) the forest edge goes from 6 px to 7.5 px |
| R13 | Low | Confirmed | `styles/inked_parchment.yaml:110` (`stone_room` band) | The distance band rounds at convex corners but the wall is mitred, so the outer corner of every room wall gets no weathering |
| R14 | Low | Note | `ops/props.py:322` | Half the hatch loop runs for nothing: `t ∈ [-span, span)` but only `t ∈ [-(h), w]` can hit |

Things I checked that are **fine**:
- Crescent direction for rectangles, disks, L-shapes and MultiPolygons: the hatch midpoints sit SE of the centroid in every case, with more than 98% of the stroke inside the part.
- Rotation: the hatch is computed after rotation, so a crate at rotate 0 and at 180 gives the same SE result.
- Degenerate input: an empty or zero-area part returns `None`.
- Intersection handling: LineString, MultiLineString and GeometryCollection results are all flattened. Points are dropped by the `geom_type` check.
- A ring (polygon with a hole) is hatched on its outer SE rim and its inner NW rim, which is right for a raised ring. No builder makes holes today.
- Boulder cracks: across 300 seeds × all cracks, `intersection(b)` was always a non-empty LineString, never empty or Multi.
- Bed folds stay inside the blanket.
- Overdraw: the frame hatch under the blanket and pillow is covered by their opaque fills, so there is no visible double-hatching inside the bed.
- Determinism: `shade_crescent` uses no rng. Boulder cracks draw from the rng only after the blob and highlight are built, so existing boulder shapes are unchanged.
- `stone_room`: the `${name}` mask exists when `band` runs, because `floor_fill` rasterizes it.
- `crystal_court` uses no macros and no props, and its walls use `crystal_wall`, not `wall_stone`. Only the ink weights reach it (R8).
- No test asserts stroke widths. The whole suite passes.

---

## Findings

### R1 (High, confirmed): chest boards are invisible
`ops/props.py:100-107`
```python
boards = [(LineString([(-s / 2, y), (s / 2, y)]), None, INK_FINE * 0.5) for y in (-w * 0.32, w * 0.32)]
return boards + [(box(-s / 2, -w / 2, s / 2, w / 2), "wood_dark", INK_MED), ...
```
`draw_prop` paints the parts in list order. The boards come first, and the opaque `wood_dark` box then
covers them completely, because they lie inside the box.
**Repro:** render a 6 ft chest at 8 px/ft with and without the board parts. The max abs difference is
0.026 and only **3 pixels differ** (just the round end caps poking past the box edge).
`test_detail_lines_present[chest]` still passes (see R7).
**Fix:** use `[box, ...] + boards`, or put the boards after the box and before the metal band.

### R2 (High, confirmed): wall texture drawn inside the excluded cave mouth
`styles/inked_parchment.yaml:139-143`. `wall` removes `exclude` from its band
(`semantic.py:109-110`). The new steps rebuild a band from `rasterize ${src}` and never apply
`exclude`. Cracks and grit therefore land on whatever is in the mouth: stream, forest, path.
**Repro:** a 28×18 ft cave with a mouth rect across the south wall, `cave_walls … exclude: mouth`, 8 px/ft.
In the mouth strip (x 16-24 ft, y 24-25.5 ft) **0 of 640 px** are non-white with a bare `wall`
and **270 of 640** with `cave_walls`. `proof_cave` (`exclude: forest`, with the stream drawn under the walls)
and the `cave` macro are both affected.
**Fix (best):** have `wall` optionally emit its final band as a Mask (e.g. `out:`, or a
`wall_mask` op that reads `collector.walls[name]["band"]`). That band already has `exclude`, `ruined`
gaps and the rough outer edge applied, which also fixes R9. **Fix (minimal):** add `exclude` to the macro path,
`rasterize ${exclude}` and `combine … mode: sub` from `${wall}_band`, guarded for `exclude: null`.
Add a test that asserts no texture inside an excluded mouth.

### R3 (Medium, confirmed): mountain and hill get a second shading
`NO_AUTO_SHADE = {"tree", "rug", "banner", "pebbles", "rubble"}`. `p_mountain` already has a dark
right face plus hatch strokes. `p_hill` already has a dark `shade` crescent plus radial hatch. Both now
also get diagonal crescent hatch on every solid part:
- mountain: 31 lines on the light face, 45 on the already-hatched dark face;
- hill: 17 on the dome, 16 on its shade, 9 on the white `top` highlight.

Worse, `mountain` is drawn as a **profile glyph** (peak up, base along the bottom). An overhead SE
crescent hatches the base line and the ridge of the *lit* face, which matches no light model. The
`mountain_range` macro scatters these by the dozen on region maps.
**Repro:** contact sheet. Or count: `shade_crescent` on each solid part of `p_mountain(4)` and
`p_hill(3)` gives the numbers above.
**Fix:** add `"mountain", "hill"` to `NO_AUTO_SHADE`. Consider `"brazier"` too (R4). Add a
parametrized test that self-shading kinds draw exactly as they did before (hash or pixel equality with
`shade_crescent` patched to None).

### R4 (Medium, confirmed): inner, highlight and sunken parts are hatched
Every part with a colour is hatched, including:
- the boulder highlight `hl` and the stalagmite `mid`/`tip`, which sit on the lit NW side: a hatch arc ends up in the middle of the rock;
- the hill `top` and the brazier `linen` coal;
- the brazier `fire` ring: hatch across flames;
- the barrel lid. Per `linework.py`'s own docstring, a sunken area is shaded inside its NW edge, not SE;
- the statue star and the chair back.

The contact sheet shows these clearly (brazier, hill, boulder).
**Fix:** a simple rule that matches the builders: auto-shade only parts with an ink outline
(`iw > 0`). That drops `hl`, `tip`, hill `shade`/`top`, the brazier `fire`/`linen` and the bush inner
highlight. Optionally shade only the first, outermost solid part of each prop. That also cuts the cost in R6
roughly in half for multi-part props (bed: 3 hatched parts, bridge: 3, barrel: 2).

### R5 (Medium, confirmed): thin parts and the hatch direction
`k = 0.2·sqrt(area)` sets the crescent depth by area, not by thickness. Measured with `shade_crescent`:
| part | lines | mean midpoint offset from centroid |
|---|---|---|
| 10×0.5 box, axis-aligned (bridge rail) | 51 | (+0.03, +0.03): hatched **all over**, not a crescent |
| same, rotated 45° (long axis NW-SE) | 4 | (+3.3, +3.3): only the SE **end cap** |
| same, rotated -45° (long axis SW-NE) | 4 | ≈0: 4 long lines **parallel** to the rail |

The hatch direction is (1, -1), from SW to NE. On a SE-facing edge that runs SW-NE, the strokes are therefore parallel
to the edge and look like a doubled outline, not hatching. The same happens on the thickest part of a disk's
crescent. This is consistent with `p_tree`'s own shading, so it may be intended, but it degrades badly
on bridges, which are routinely rotated to cross a river (rails and deck: see the -45° bridge on the sheet).
**Fix:** cap the depth by thickness, e.g. `k = min(0.2*sqrt(A), 0.35*short_side)` using
`g.minimum_rotated_rectangle`. Skip parts whose short side is under about 2 gaps. Optionally choose the hatch
angle per part so it crosses the crescent, for example perpendicular to the dominant SE-facing edge.

### R6 (Medium, confirmed): performance
`scatter` of **752 props** (200×150 ft at 8 px/ft, supersample 1), timed with auto-shade on and with
the kind added to `NO_AUTO_SHADE`:

| kind | with | without | per prop extra |
|---|---|---|---|
| crate | 13.7 s | 4.2 s | 12.7 ms |
| barrel | 24.7 s | 11.2 s | 18.0 ms |
| boulder | 18.4 s | 4.6 s | 18.4 ms |
| stalagmite | 23.5 s | 8.6 s | 19.9 ms |
| bed | 22.7 s | 6.1 s | 22.1 ms |

A 300-prop scatter costs about 4-7 s more, and more again at full resolution with supersampling. The cost has two parts:
- about 90 Python-level `LineString.intersection` calls per part (R14: half of them cannot hit);
- `stroke_geometry_alpha` buffering every hatch line and running `unary_union` over them before rasterizing.

**Fix:** use vectorised `shapely.intersection(np.array(lines), cres)`. Restrict `t` to `[-h, w]`. Draw the
thin hatch lines straight to a PIL patch, as `shade_lines` does, instead of buffer and union. Combined
with the R4 rule this should bring the overhead under 2x.

### R7 (Medium, confirmed): the tests mostly cannot catch their own regressions
Mutation results:
- `test_crate_shaded_south_east_even_rotated`: **does catch** a NW-crescent mutant (SE 192 < NW 239).
  But with the hatch removed entirely it still **passes** (SE 192 > NW 143), because the quarter windows
  are asymmetric even without hatching: the outline pixels fall on one side of the slice bounds. So
  it does not prove a hatch exists.
- `test_crescent_helper`: good. It catches a NW crescent, and its geometry assertions are meaningful.
- `test_markers_and_flat_props_are_not_hatched`: **vacuous**. It renders `city` twice with different
  ids and asserts equality. `p_city` uses no rng, and a regression that hatches markers would hatch both
  renders the same way, so the test still passes. It never renders a rug or banner.
- `test_detail_lines_present[*]`: **vacuous**. With all new detail lines *and* the hatch removed,
  the dark-pixel sums are barrel 1095, bed 1169, chest 1430, boulder 246, pillar 281, all above the
  `> 200` threshold. It passes for the chest, whose boards are invisible (R1).
- `test_stone_room_walls_get_weathering`: **vacuous**. Without the band/cracks/stipple steps the
  window still holds 340 dark px (the darker mortar alone), above the `> 50` threshold.
- `test_cave_walls_get_rock_texture`: meaningful (it compares against a bare `wall`). Nothing tests
  `exclude` (R2).
- `test_heavier_ink_weights`: only restates the config.

The CLAUDE.md rule asks for at least 3 tests per public function: `shade_crescent` has 1 direct test, and the
new builder geometry has none. **Suggested tests:**
- compare each feature on vs off: render with `shade_crescent` monkeypatched to `None`, assert the SE window gains ink and the NW window does not change (or changes by less than ε);
- check a rug, a banner and a marker are pixel-identical with and without `shade_crescent` patched to None;
- check part order: every `None`-colour line part in `p_chest`/`p_crate`/`p_bed` comes after the fill it decorates, or more simply, the line pixels differ from a render without the line;
- `shade_crescent` on a disk, a MultiPolygon, a thin or rotated part (after R5) and a tiny part (below 1 gap returns None);
- `cave_walls` with `exclude`: no extra ink inside the mouth;
- `stone_room`: compare against the macro steps with the texture removed, not a fixed threshold.

### R8 (Medium, confirmed): the canon `crystal_court` changes
`conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml` includes
`styles/inked_parchment.yaml` and sets no `ink:` override. Its `wall` (weight bold, outer_weight heavy),
four `partition`s (medium by default) and the `stroke weight: medium`/`fine` on the dais and high table all resolve
through the style's `ink:` map, so they get about 20-25% heavier on the next render. Nothing pins the court's
output (`test_m7_proofs` checks structure, not pixels), and the PR text and LOG do not mention it. The
court's colours and look were approved by the owner (TP74). The mortar change does *not* reach it
(it uses `crystal_wall`).
**Fix:** either tell the owner and re-render the court for sign-off, or pin the old weights in the
court recipe (a recipe-level `ink:` override, if the recipe schema allows it).

### R9 (Low, confirmed by reading the code): texture band does not match the rough wall
`wall style: rough` builds the outer edge as `_rough_ring(...)` ∪ `floor.buffer(0.4·t)`, so the outer edge
wanders roughly t±0.35 ft and never comes closer than 0.4·t. The texture band is the clean ring between
0.15 ft and t, so stipple and cracks spill past the inked outer edge onto the beyond-hatching where the wall
is thin, and leave the bulges bare. This is mostly invisible on rock-on-rock, but it is wrong in principle.
The fix in R2 (rasterize the wall's own band) solves it too.

### R10 (Low, confirmed): name and id reuse
Two `cave_walls` with the same `wall:`, or two `stone_room`s with the same `wall:`, run without error.
`${wall}_inside`/`${wall}_band` are overwritten, which is harmless in sequence, but the duplicate ids
`${wall}_rock_cracks` etc. hash to the same `step_seed`, so the crack and grit placement is correlated
between the two. The `wall` op already overwrites `collector.walls[name]` (doors attach to the last one),
so this is pre-existing behaviour. Worth a recipe-level duplicate-id warning.

### R11 (Low, confirmed): crate boards
`LineString(...).difference(i)` never changes anything (y = ±0.44·s is outside `i` = ±0.38·s), so
the `not bd[0].is_empty` filter is dead too. Visually the boards are a single line 0.06·s inside the
N and S outer edges and none on the E and W members, which reads as a doubled outline rather than plank seams.
Suggest dropping the difference, and either putting seams on all four members or using a different board pattern.

### R12 (Low, suspected): absolute weights on non-foot maps
`_width_ft` returns style weights in *map units*. On `proof_region` (unit: miles, 125 px per 5-mile
square), `forest_mass`'s `stroke weight: medium` goes from 0.24 mi (6 px) to 0.3 mi (7.5 px), and rivers
(`fine`) from 2.5 to 3 px. The prop inks (`INK_FINE`/`INK_MED`, +25%) behave the same way for region mountains
and conifers. This is pre-existing, but this PR makes it heavier. Worth a look at the region render before merging.

### R13 (Low, confirmed by reading the code): stone_room corner gap
The `wall` outer edge uses `buffer(t, join_style=2)` (mitred). `band` uses Euclidean signed distance, so
its outer edge is rounded at convex corners and the outer corner square of each wall (up to about 0.29·t²
in area) gets no cracks or grit. This is cosmetic. R2's "use the wall's own band" fix covers it.

### R14 (Low, note): wasted iterations
`for t in np.arange(-span, span, gap)` with `span = w + h`. A line hits the bbox only for
`t ∈ [-h, w]`, so roughly half the iterations do an intersection that cannot hit. This folds into R6.

---

## Recommended before merge
1. R1 (reorder the chest parts) and R2 (exclude in `cave_walls`): one-line or few-line fixes, each with a test.
2. R3 and R4: exclude self-shaded kinds, and shade only inked parts.
3. R7: replace the vacuous tests with feature on/off comparisons.
4. R8: tell the owner that the court's line weight changes, or pin it.
5. R5 and R6 can follow, but R6 is noticeable on large scatters.

---

## Resolution (2026-11-13, by the PR author)

| ID | Resolution |
|---|---|
| R1 | Chest boards are drawn after the chest box. The chest body is mid-tone wood, so ink boards read. |
| R2, R9, R13 | New op **`wall_band`** rasterizes the band a named wall actually painted, with the rough edge, ruined gaps, excluded mouths and corners. `cave_walls` and `stone_room` texture that band (with a small inset). Tested: no texture lands in an excluded mouth. |
| R3 | `mountain` and `hill` are in `NO_AUTO_SHADE`. |
| R4 | Only parts with an ink outline (`iw > 0`) are auto-shaded: highlights, hill tops, fire and coal are skipped. Tested: the brazier gets exactly one shaded part. |
| R5 | The crescent depth is `min(0.2·√area, 0.3·short side)`, and parts thinner than 1:4 get no hatch. Tested with a rail at 0°, +45° and −45°. |
| R6 | Vectorised `shapely.intersection` over only the offsets that can reach the crescent, and a single `buffer` for uniform strokes in `stroke_geometry_alpha`. Measured: shading now adds ~2.6 ms per prop (1600 crates: 19.3 s, against 15.1 s without shading), down from 12–22 ms. |
| R7 | Tests rewritten to fail when the feature is removed: shading must add ink (compared with the hatcher patched out); excluded kinds must never reach the hatcher; detail lines must change the drawing (compared with them stripped) for barrel, bed, chest, boulder, pillar and crate; stone_room weathering compared with a plain wall; the excluded mouth; 4 direct `shade_crescent` tests; `wall_band` tests. |
| R8 | **Documented, intended:** the canon Crystal Court's walls, partitions, dais and table pick up the heavier style ink (~20–25%). That's styling only, with no new feature, in line with the owner's "more detail / shading lines" direction. |
| R10 | A second `wall` or `partition` with an existing name raises `RecipeError` (it would also have broken door placement). Tested. |
| R11 | The no-op `difference` is gone; crate boards are plain lines. |
| R12 | Style ink weights are scaled ×0.25 on `unit: mi` maps (the weights are in feet). Tested. |
| R14 | The hatch loop only generates offsets that can cross the crescent's bounding box. |
| — | Detail lines (staves, folds, boards, cracks, flutes) use `DETAIL = 0.075` ft, so they're at least a pixel at VTT scale. They were sub-pixel before, which is why R7's strip test first failed on barrel, chest and boulder. |

Tests: full suite (excluding e2e) **2319 passed**.

---

## Verification of 50e71d0 (independent reviewer, 2026-11-13)

Every item below was checked against the code at 50e71d0, re-running the original reproduction scripts.

**Test suite:** `cd software && python3 -m pytest tests/mapgen -q`: **415 passed** (61 s).

**Draft renders:** I draft-rendered all 6 recipes with `python3 -m mapgen render <r> --draft`: `proof_cave`, `proof_cellar`, `proof_region`, `proof_ruins`, `proof_town` and `crystal_court`. All 6 rendered with no errors.

### R1 to R14

| ID | Verdict | Evidence |
|---|---|---|
| R1 | **RESOLVED** | Chest drawn with vs without its board lines: 147 px differ, max difference 0.28 (it was 3 px and 0.026). The boards are visible on the contact sheet. |
| R2 | **RESOLVED** | Excluded-mouth strip: 0 of 640 px non-white with `cave_walls`, the same as a bare `wall` (it was 270). The `wall_band` op reads `collector.walls[name]["band"]`, which already has `exclude` applied. |
| R3 | **RESOLVED** | `mountain` and `hill` are in `NO_AUTO_SHADE`. The contact sheet shows only their own shading. |
| R4 | **RESOLVED** | Shading now needs `iw` (an ink outline). On the brazier, only the outer metal disk is hatched; the fire and coal are not. Boulder `hl`, hill top and bush highlight are skipped. Two inner parts with an outline are still hatched (barrel lid, statue star). That matches the rule as written and is acceptable. |
| R5 | **PARTIAL** | Thin parts are fixed. Rails at 10×0.5 return `None` at 0°, +45° and −45°. Parts with a short:long ratio of 0.25 or more still degenerate on the diagonals, because the crescent shift (−k, −k) runs along a NW–SE axis and the hatch direction (1, −1) runs along a SW–NE axis. On a 10×3 box: 26 lines at 0°, **3 lines at the SE end cap only** at +45°, and **4 long lines parallel to the side** at −45°. 10×5 behaves the same (24 / 4 / 4). On the contact sheet, a bridge rotated 45° is hatched only at its SE end. This matters because `scatter` rotates props randomly by default (`rotate_jitter: 180`), so beds, tables, chests and bridges often land on a diagonal. Not a blocker; worth a follow-up, e.g. pick the hatch angle per part, or measure the crescent depth along the part's short axis. |
| R6 | **PARTIAL (improved)** | I re-ran the same 752-prop scatter, with shading vs without. Extra cost per prop: crate 5.6 ms, barrel 8.6, boulder 5.7, stalagmite 7.4, bed 13.6 (it was 12.7 / 18.0 / 18.4 / 19.9 / 22.1). Overall prop drawing is 1.6–3.8× slower than without shading (it was 2–4×). The author's figure of about 2.6 ms is not reproduced on this machine, though absolute timings are noisy here. The bed costs most because it still hatches 3 outlined parts (frame, blanket, pillow), and the frame's hatch is then painted over by the blanket. Not a blocker. |
| R7 | **RESOLVED** | Each feature test now compares against a render with the feature patched out (hatcher removed, detail lines stripped, plain wall) and would fail if the feature were deleted. There are 4 direct `shade_crescent` tests, plus mouth, `wall_band` and duplicate-name tests. Gaps: no test covers the new stroke fast path (see below), and no `wall_band` test uses a partition or a ruined wall (I checked both by hand). |
| R8 | **RESOLVED (documented)** | Recorded as intended. The court renders with no errors. The owner should still be told when the court is next re-rendered. |
| R9, R13 | **RESOLVED** | `wall_band` uses the painted band itself, including the rough edge and mitred corners. |
| R10 | **RESOLVED** | Two `cave_walls` with the same `wall:` name, and two `stone_room`s with the same name, now raise `RecipeError: … already exists`. |
| R11 | **RESOLVED** | The no-op `difference` call is removed. |
| R12 | **RESOLVED, with a note** | The ×0.25 scaling applies on `unit: mi` maps. Note that this is a much bigger change than undoing this PR's +25%. In `proof_region` at full resolution, the coastline (`heavy`) goes from 10.5 px (on `feat/lean-facets`) to 3.25 px, and the river ink (`fine`) from 2.5 px to 0.75 px, which is under a pixel. In the draft render the coastline is a thin line that is still visible, and the river ink edge is barely visible. Ask the owner to look at the region proof. If it's too light, a factor of about 0.5, or setting `ink:` in the region recipe, would restore it. |
| R14 | **RESOLVED** | Hatch lines are only generated for offsets that can reach the crescent's bounding box (`[minx − h, maxx]`), and the intersection is vectorised. |

### Regressions from 50e71d0

**`wall_band` op.** No regressions found. Edge cases checked by script:

| Case | Result |
|---|---|
| partition | correct band (sum 1002) |
| partition, `inset` larger than half the thickness | empty mask, sum 0. `cracks` and `stipple` then do nothing, with no error |
| ruined wall | band follows the gaps (2108 vs 5128 dressed) |
| wall fully excluded | empty mask, no error |
| `wall_band` before its wall | clean `RecipeError: … not defined yet` |
| `stone_room` with `thickness: 0.15` and inset 0.08 | almost empty, no error |

**Stroke fast path in `stroke_geometry_alpha`.** Buffering one MultiLineString gives a pixel-identical result to the old union of per-line buffers (max diff 0.0) in every case I tried:
- overlapping and duplicate lines;
- a polygon with a hole;
- the hatch MultiLineString;
- a self-touching line.

Other inputs:
- a GeometryCollection with an empty member works;
- zero-length lines alone still return `None`;
- dashed and jittered strokes (where `wm ≠ 1`) still take the old path, and dashed strokes without jitter have `wm == 1.0` and use the fast path with the same cap style.

**Duplicate-name error.** No recipe in the repo reuses a wall name:
- `proof_ruins`: `wall_a`, `wall_b`;
- `proof_cellar`: `w` plus 3 uniquely named partitions;
- `crystal_court`: `shell` plus 4 uniquely named partitions;
- `proof_cave`: a single `cave_walls rock`;
- the goldens and the build-map cookbook: unique names;
- no `wall` or `partition` call without a name (which would default to `wall` / `partition`).

The check runs *after* the wall is painted. That does no harm, because the error aborts the render.

**`iw`-only rule and `DETAIL` width.** The contact sheet looks right: chest boards, barrel staves and boulder cracks now read clearly at 20 px/ft. `DETAIL` (0.075 ft) is still in absolute map units, so on a mile-scale map it would be 0.075 mi. No mile-scale prop currently uses detail lines (mountain and hill have none), so this has no effect today.

### Verdict

**Clean to merge.** Nothing blocks. Three follow-ups, none required for merge:
1. R5: thick parts on a diagonal are still hatched only at an end cap, or with lines parallel to the edge.
2. R6: shading still costs about 6–14 ms per prop. Shading only the outermost outlined part would help the bed.
3. R12: ask the owner whether the region proof's 3× thinner coastline and sub-pixel river ink are acceptable.

### Verification follow-ups: resolved before merge (2026-11-13)

- **R5 (diagonals):** hatch strokes now run perpendicular to a part's long axis, in a frame rotated so they're vertical. Near-square parts keep the classic diagonal. Tested at 0°, 30°, 45°, −45° and 90°: strokes never run along a side.
- **R12:** the mile-scale ink factor is 0.5, not 0.25, so the coastline and river outlines stay above a pixel. Tested.
- **R6:** left as is (shading makes prop drawing 1.6–3.8× slower; acceptable for now, noted for a later pass).
- **R8:** the owner will be told the court's lines are heavier when it's next rendered.

Tests: full suite (excluding e2e) **2324 passed**.
