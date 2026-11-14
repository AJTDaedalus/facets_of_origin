# Review of PR #39 (feat/mapgen-prop-detail vs feat/lean-facets)

Scope: props.py, test_prop_detail.py, golden hash. Checked by sweeping crate, chest, barrel, bridge and table
over sizes 0.3..100 and 60 seeds each (shapely validity, empty or odd geometry types, plank bounds and overlap),
rendering every kind at 5 sizes x 5 rotations (no exceptions, byte-identical on a re-render), and probing
`_facet_tone` under rotation. `tests/mapgen` passes (446).

Verdict: no high-severity defects. The facet tone, `_merge_line_runs` and determinism all hold up. Findings are
cosmetic or about test strength.

R1. LOW (reproduced). props.py:314-318, `_plank` with rag=0.04. The ragged ends are applied on the plank's
across-deck axis, and `lo` / `hi` are already up to 1.0 x the deck half-width. So planks poke up to about
0.04 ft past the deck edge. A sweep of 600 bridges found a maximum overshoot of 0.039 ft, in the 1370 cases
of a plank with a part outside the deck rectangle. The overshoot is the same at every size, so it is
invisible on big bridges and noticeable on small ones. Fix: clamp `lo` / `hi` to
`0.9..0.96 x hw` or clip the plank to the deck box.

R2. LOW (reproduced). props.py:301 and :314. For s < ~0.1 ft the single plank has zero or negative width
(`x+gap/2` ~ `x+pw-gap/2`), giving an invalid Polygon (s=0.05: `is_valid` False). The gap floor
(0.05 ft) is absolute and does not scale with s. s >= 0.15 is fine, and the `size` param is presumably a
PosFt with no minimum. Fix: `gap = min(max(s*0.008, 0.05), pw*0.2)`, or skip the gap when the plank is
narrower than about 0.2 ft.

R3. LOW (reproduced), design. props.py:301-313. Plank width (0.55-0.95 ft), gap, post size
(floor 0.18 ft) and nail size (floor 0.05 ft) are absolute while the deck is s x 0.42 s. A 100 ft bridge
makes 673 parts (467 after merge) in about 0.14 s. A 1 ft bridge is one plank with 0.18 ft post circles on a
0.42 ft deck, so the posts cover about 40% of the deck width. Not a bug, but worth a size cap or a post_r
cap such as `min(post_r, w*0.2)`.

R4. LOW (reproduced). props.py:155-176 (crate, NW face) and :194-203 (chest). The lid colour equals one of the
facet tones. Crate lid is `wood_light`, which is also the NW face tone. Chest lid is `wood`, which is the
"base" tone used for faces roughly side-on to the light (rotations near 53 and 135 degrees: two of four faces
come out as `wood`). Those faces merge into the lid, so the bevel survives only as mitre lines. For the
crate the NW bevel is invisible by design, since the ink outline carries it. Fix: give the lid a distinct key
(e.g. `wood_light` for the chest, `linen`/`wood` for the crate lid) or accept it.

R5. LOW (reproduced). props.py:480-481 and :486-494. `_facet_tone` uses a hard 3-way threshold (+-0.35) on the
face centroid direction, so at about 53 and 135 degrees a face can flip tone discontinuously, and a
face can read "base" while its opposite reads dark/light. Probe output:
crate@53 = [wood, dark, wood, light]. The result is correct (light NW, shadow SE) but the bevel
looks lopsided at those angles. Optional fix: use a continuous blend or only two tones with the
0 crossing as the split.

R6. LOW (PLAUSIBLE). props.py:513-528 `_merge_line_runs`. It only merges same-width uncoloured runs, so
paint order is kept, and no geometry type is dropped: GeometryCollection and Point results are not merged,
they pass through unchanged. But the merge builds `LineString(x.coords)` per member. A member that is a
Point or Polygon cannot get there (the type guard covers it). Barrel grain is `LineString.intersection(circle)`
and could in principle return a `Point` or `GeometryCollection` on a tangent hit. A sweep of 5 sizes x
60 seeds never produced one, so the barrel grain is safe in practice. The `is_empty` guard exists for grain
but not for the seams filter ordering. Nothing to fix; consider `if g.geom_type in (...)` on grain too.

R7. LOW (reproduced), pre-existing. draw_prop passes the same `ctx.seed` to every prop, so every crate in a
map has the same style (X, single diagonal or plain), the same grain and the same knot. The PR's "styles
vary with seed" only helps across maps. Fix: mix `at` into the seed (`seed ^ hash(round(at))`) in draw_prop.

R8. LOW (tests). test_prop_detail.py, weak assertions:
- `test_planks_cover_the_deck_end_to_end` only checks x bounds. It would pass with planks overlapping the
  rails, planks outside the deck (R1), or gaps in the middle. Assert union area / deck area > 0.85, and that
  each plank is within `deck.buffer(0.05)`.
- `test_short_bridge_still_builds` (s=1.0) only checks that a wood_light part exists; it never checks
  validity, so R2 is not caught. Parametrize over s in (0.2, 0.5, 1, 40, 100) x seeds and assert
  `g.is_valid and not g.is_empty` for every part of every PROPS kind.
- `test_deterministic_per_seed` compares only geometry, not colour keys or widths.
- The rotation test uses only multiples of 90 degrees on a square crate, where "dark on the south-east" is
  hard to tell from a coarse local-space mapping. Add 45 and 30 degrees and the chest (non-square).
- `south < north` is a bare inequality on mean luminance over a 2 x 20 px window, so any shading from
  the hatch could satisfy it. Assert a margin (e.g. > 0.03 in luminance).
- No test for `_merge_line_runs` with MultiLineString inputs (only LineString and ring) or for an
  empty geometry in a run.

## Outcomes (fix pass)

- R1 fixed: each bridge plank is clipped to the deck; test `test_planks_stay_on_the_deck`.
- R2, R3 fixed: plank width, gap, raggedness and minimum lengths scale by `min(1, s/6)`; posts are capped at 0.2 × deck width; test `test_small_bridges_are_valid_and_posts_fit` (0.05–3 ft).
- R4, R5 fixed: facet tone is now a continuous blend of the base colour, toward white for faces turned north-west and toward black for faces turned south-east (`FACET_SHADE`), so nothing flips at a threshold. The chest lid is now `wood_light`, distinct from its side faces. Tests: `test_tone_changes_continuously_with_direction` and the side-face/base tests.
- R6 fixed: barrel grain keeps only line pieces.
- R7 no change needed: each `prop` step gets its own per-step seed, and `scatter` seeds each prop with `ctx.seed + 31*i + 1` (props.py scatter). The storeroom render shows mixed crate styles. The review's repro reused one ctx seed across calls.
- R8 fixed:
  - The rotation test now requires a margin, and a 45° case was added.
  - The determinism test also compares colour keys and ink widths.
  - New all-kinds validity sweep: 5 kinds × 5 sizes × 8 seeds.

mapgen suite: 482 passed.
