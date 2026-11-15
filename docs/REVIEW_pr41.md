# Review: feat/mapgen-tavern engine diff (PR 41)

Scope: `git diff feat/lean-facets..feat/mapgen-tavern -- software/mapgen/`, reviewed at c950430 in a scratch worktree. The branch's 670 mapgen tests pass.
Each finding was reproduced. Line numbers refer to the branch.

## Findings

**R1. `colors` override rejects the prop palette names the docs promise** (`ops/props.py:626-628`, docstring at `:772`)
- `_color` resolves an override value with `resolve_color(ctx.style, ...)` only. It never falls back to the prop-local `COLORS` table (`cloth`, `wood_dark`, ...), which the non-override path does at `:631-632`.
- Input: `{op: prop, kind: rug, at: [20,15], colors: {rug: cloth}}`, which is the docstring's own example. Also `colors: {rug: wood_dark}`.
- Observed: `RecipeError: unknown colour 'cloth'` (and `'wood_dark'`). It works only when the style palette defines the name.
- Expected: both resolve through `COLORS`, as an un-overridden part's key does.
- The same override on a kind that has no `rug` part (e.g. `card_table`) is never looked up and passes silently. So the error appears or not depending on the kind, and typos are never flagged.
- Fix: factor out `_resolve(ctx, name)` (palette, then `COLORS`, then error) and use it for both the key and the override value.

**R2. `dunes` macro spills outside `within` and into `clear`** (`styles/mists_region.yaml`, `dunes` macro: the `roughen_geom` / `rasterize` / `blur` / `fill` steps, about lines 52-58)
- `within` and `clear` are applied before `trace` and `roughen_geom`. After roughening (0.5 ft), simplify and the 0.8 sigma `blur`, the output mask and fill are not clipped again.
- Input (40x30 ft, 8 px/ft, white canvas):
  - Land is `rect 0..20`, with `dunes {within: land_m, clear: <empty mask>, cover: -5}`.
  - Then a second case with `clear` = `rect x15..25` over land `0..40`.
- Observed, case 1: the `dunes` mask has 3 columns above 0.5 beyond x=20 ft. The canvas is darkened in 16 columns beyond the land edge, about 2 ft onto the sea.
- Observed, case 2: 280 px of the `dunes` mask is above 0.5 strictly inside `clear` (`clear > 0.99`). 5411 canvas px inside `clear` are darkened below 0.97, roughly a 1.4 ft intrusion per edge.
- Expected: dunes stay in `within` minus `clear`, as the doc says ("inside `within` (minus `clear`)"). The `rough_sea` macro's equivalent guarantee is tested.
- Fix: after the `rasterize`, add `combine ${name} = ${name} * ${within}` and `combine ... sub ${clear}`. Do the same for `${name}_soft`, or clip the fill with `${name}_soft * within * ~clear`.

**R3. `lit_mist` doc names a `reach` param that does not exist** (`styles/mists_region.yaml:61`)
- The doc says "reaching `reach` feet". The params are `mist`, `center`, `edge`, `name`, `strength`.
- Input: `{op: lit_mist, mist: mist_m, center: [38,2], reach: 30}`.
- Observed: `RecipeError: macro 'lit_mist' doesn't take reach`.
- A recipe that overrides only `center` keeps `edge` at the absolute default `[40,0]`, so the radius is silently the distance to that point. If `center` equals `[40,0]`, the gradient fails with `start and end must differ`.
- Fix: add `reach` (feet, default 40) and a unit direction, or compute `edge` from `center + [reach, 0]`. Otherwise fix the doc to describe `edge`.

**R4. `transform` skew accepts degenerate angles** (`ops/geometry.py:151-156,167-168`)
- The `skew` angles are unvalidated, and `affinity.skew` uses `tan`.
- Input: `skew: [90, 0]` on `rect 10x6`.
  - Observed: a valid polygon with bounds of about ±4.9e16 and area 48. It rasterizes to 0 px, with no error.
  - `skew: [0, -90]` gives bounds of about ±8e16 and area 0.
- Input: `skew: [45, 45]` (a singular matrix).
  - Observed: an invalid polygon with area 0, `is_valid` False. It rasterizes 18 stray px.
- Expected: a `RecipeError` for `|skew| >= 90` and for `tan(x)*tan(y) == 1`. Neither input should silently produce an empty or garbage shape.
- Fix: a pydantic validator on `skew`: each angle `abs(a) < 90`, and `abs(1 - tan(sx)*tan(sy)) > 1e-6`.

## Checked and found correct (no finding)
- `_Cutter` against `shapely.ops.substring`: identical rendered output (max diff 0.0) over rect, polygon, concave L and star outlines. Parameter combinations covered: dash, jitter, taper, double (0.2, 3, 14, 40), roughness, and side inside/outside. Raw pieces differ in two harmless ways. A piece that ends exactly on a vertex repeats that vertex. A zero-length piece is a 2-point `LineString` where `substring` returns a `Point`. Both are dropped or buffered identically, because the `o.length > 0` filter and the buffer ignore repeats. Ends past the line length are clamped by the caller (`min(pos+on, L)`), so they are unreachable.
- `rasterize_patch` holed-part rewrite against the old full-layer max method: 300 random MultiPolygons with holes, islands inside holes, and parts crossing or touching the patch edge. Patch origin, shape and alpha were identical, with max diff below 1e-6.
- `darkness`: no lights, off-map light, radius 0.01, intensity 0 and 1, supersample 3, draft, and `warmth` with a black colour. The output is finite and the VTT lights are unchanged. The maths is consistent with `light`'s glow.
- New prop builders: 11 kinds x 11 sizes (0.001 to 300 ft) x 300 seeds produced no exceptions, empty parts, invalid parts or `GeometryCollection`s. Drawing at sizes 0.01 to 200 ft, positions off and on the map, rotated, with `colors`, and in draft mode raised nothing.
- `transform` on empty geometry, a point-sized box, a MultiPolygon, and integer `about`: no crash, and the rotation sense matches the doc.
- Defaults: `colors={}` leaves every existing prop render unchanged (`colors and key in colors` is falsy). The `inked_parchment.yaml` change only adds materials.
- `rough_sea`, `dunes` and `lit_mist` run, in draft too, with no land, all land, no dunes and all dunes. Substitution is correct, `from` moves the band as documented, and two calls with the same `name` just overwrite each other's layers.
