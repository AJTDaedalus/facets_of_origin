# TASKS — Programmatic Map Building (`mapgen`), Phase 1: battle maps

*Planner tier, 2026-11-13. Design: `docs/DESIGN_mapgen.md`. Brief: `docs/BRIEF_mapgen.md`.*

**Worker rules:** one task per session turn. TDD (write the tests first and watch
them fail). Run from `software/`: `python -m pytest tests/mapgen -q` plus the
task's own command. Mark the task here and append to `docs/LOG_mapgen.md`, then stop.
Branch: `feat/mapgen`, cut from `feat/lean-facets` (main lacks the Lean ruleset and
the 5e Oraga module that T31 needs).

**Copyright guard (every task):** the comparator maps (DESIGN §7.1) are never
copied into the repo, a fixture, a texture or a commit. Only paths, measured
scales and metric numbers are committed.

Status: `[ ]` open · `[~]` in progress · `[x]` done · `[!]` blocked

---

## M0 — Skeleton

- [x] **T1 Package skeleton.** Create `software/mapgen/` (`__init__`, `__main__` with
  argparse subcommands `render|ops|quality|sheet` stubbed), `software/tests/mapgen/`
  (`__init__`, `conftest.py` with a `tmp_out` fixture). Add `opensimplex` to
  `software/requirements.txt`. Add `software/mapgen/.refcache/` to `.gitignore`.
  *Accept:* `python -m mapgen --help` lists 4 subcommands; 3 tests (import,
  help exit 0, unknown subcommand exits non-zero).
- [x] **T2 Recipe models.** `recipe.py`: `MapHeader` (title, width_ft, height_ft,
  feet_per_square ∈ {5,10}, px_per_square 10–300, supersample 1–4, seed, include),
  `Step` (op, out?, id?, seed_offset?, extra params kept), `Recipe`; `load_recipe(path)`.
  *Accept:* ≥6 tests: valid load, missing header, negative size, bad
  feet_per_square, unknown top-level key, and error messages that name the field.
- [x] **T3 Units.** `units.py`: `Frame(header, draft=False)` with `ft_to_px`,
  `px_shape`, the supersample factor and a draft override (35 px/sq, ss 1).
  *Accept:* ≥4 tests: a 60×40 ft map at 70 px/sq is 840×560 output and 1680×1120
  working at ss 2; draft shape; rounding.
- [x] **T4 Layer store and registry.** `layers.py` (the 4 typed layer classes,
  store with get/put/free), `registry.py` (`@op(name, params=Model, inputs={...},
  output=Type)`, lookup, list). *Accept:* ≥6 tests: register/lookup, duplicate name
  error, type mismatch error, free, list order stable.
- [x] **T5 Engine.** `engine.py`: run steps in order, resolve `~mask` inversion
  refs, validate types before execution (a dry pass), per-step RNG seeded by
  (map.seed, step id or index, seed_offset), a liveness pass that frees dead layers.
  *Accept:* ≥7 tests: missing ref names the step; dry pass catches a type error
  before any op runs; inserting a step with an `id` leaves later id'd steps'
  RNG unchanged; liveness frees.
- [x] **T6 Includes and macros.** Recipe `include:` merges style YAML (palette,
  materials, op defaults, macros). A macro is a named step list with `${param}`
  substitution, called as `{op: macro_name, ...}`. *Accept:* ≥6 tests: merge
  precedence (recipe wins), op defaults applied, macro expansion, unknown
  `${param}` error, recursion guard, include path relative to the recipe.

## M1 — Geometry and masks

- [x] **T7 Geometry ops.** `rect, polygon, circle, ellipse, path(width, caps), union,
  subtract, intersect, offset`. *Accept:* ≥3 tests per op group: exact areas in ft²,
  validity (`is_valid`), empty-result handling.
- [x] **T8 roughen_geom.** Densify to a `scale_ft/4` spacing, displace along the
  normals by opensimplex noise (amount_ft, scale_ft), repair with `buffer(0)`.
  *Accept:* ≥4 tests: deterministic per seed; area within ±10%; still valid;
  amount 0 is identity.
- [x] **T9 rasterize.** Geometry → Mask at working resolution with antialiasing
  (render at the working px with Pillow at an extra ×2, then box-downsample to
  coverage). *Accept:* ≥4 tests: a 30×40 ft rect at 70 px/sq covers 420×560 px
  within 0.5%; edge pixels fractional; holes stay holes; an off-canvas shape is clipped.
- [x] **T10 Mask ops.** `grow, shrink` (distance-transform based, in ft), `blur`
  (σ in ft), `threshold, invert, band(inner_ft, outer_ft), combine(max|min|mul|sub),
  roughen`(raster edge displacement). *Accept:* ≥3 tests each: grow by 5 ft
  widens a rect by 2×5 ft within one px; band area; idempotence where expected.

## M2 — Fields

- [x] **T11 Noise.** `noise(kind fbm|ridged|billow, scale_ft, octaves, persistence,
  lacunarity)` using `opensimplex.noise2array`, normalised to −1..1. *Accept:*
  ≥5 tests: deterministic; seed changes the output; range; the FFT peak shifts with
  scale_ft; runtime < 2 s at 2000² (mark `slow` if not).
- [x] **T12 Other fields.** `gradient(linear|radial)`, `distance(from mask, ft)`,
  `remap(in, out, curve)`, `field_to_mask(lo, hi)`. *Accept:* ≥3 tests each.

## M3 — Paint and materials

- [x] **T13 Canvas and fill.** `canvas`, `fill(color|material, mask, opacity,
  blend normal|multiply|screen|overlay)`, compositing of premultiplied RGBA.
  *Accept:* ≥6 tests: an opaque fill through a half mask gives a 50% mix; the blend
  modes match the reference formulas on 1-px images; `~mask` works.
- [x] **T14 Style file v0 and materials A.** `styles/inked_parchment.yaml` with
  palette + ink weights; materials `flat`, `ramp_noise`, `dirt`, `bedrock_hatch`.
  *Accept:* ≥3 tests per material: deterministic; Q2 local σ above a floor
  (no flat fill); colours inside the ramp.
- [x] **T15 Materials B.** `flagstone` (jittered-grid Voronoi via `scipy.spatial`,
  mortar lines, per-stone tone jitter, stone size in ft), `planks` (direction,
  width, staggered seams), `cobble`. *Accept:* ≥3 tests each: mortar fraction in
  a band; stone count ≈ area / stone area ±25%; plank seams align to direction.
- [x] **T16 Materials C.** `grass` (noise + speckle + tufts), `water` (depth from
  distance-to-shore, ripple lines). *Accept:* ≥3 tests each.
- [x] **T17 stroke.** Mask or Geometry edge → ink line: width (ft or style weight
  name), roughness, `double` (two parallel lines), dash pattern. *Accept:* ≥5 tests:
  line pixels lie within width of the edge; dash duty cycle; roughness 0 is
  straight; geometry and mask sources agree within 1 px.
- [x] **T18 Shadow, occlusion, hatch, paper.** `shadow(drop|inner, offset, blur,
  strength)`, `occlusion(from walls, falloff_ft)`, `hatch(band outside a mask:
  block hatching à la stone-mass, line spacing, angle jitter)`, `paper` (parchment
  grain, 2-scale fbm multiply), `vignette`. *Accept:* ≥3 tests each: shadow
  darkest next to the edge, monotone falloff; hatch only inside its band.

## M4 — Semantic, props, overlay

- [x] **T19 wall.** From Geometry: wall band (thickness ft, centred/outer), styles
  `dressed` (straight, block texture), `rough` (cave, roughened), `ruined` (gaps by
  noise, rubble); paints ink + fill; **emits LOS polylines** (in feet) into the
  export collector. *Accept:* ≥6 tests: LOS covers the full boundary length
  within 1%; ruined walls emit gaps; holes (pillars) emit closed loops.
- [x] **T20 Openings.** `door, double_door, window, secret_door, portcullis` placed by
  `{wall: id, at: [x,y]}` (snapped to the nearest wall edge), carve the wall, draw
  the symbol, split the LOS segment, emit a portal (closed state, rotation).
  `stairs(direction)`, `light(radius_ft, colour, intensity, glow paint optional)`.
  *Accept:* ≥3 tests per op: the portal sits on the right square; the LOS gap equals
  the door width; a secret door is a portal with `closed: true` that renders an `S`.
- [x] **T21 Prop library.** `props.py` with a drawing-function registry; kinds
  per DESIGN §2.4 (19). Each prop: fill + ink outline at style weights + cast
  shadow, size in ft, rotation. *Accept:* every kind renders inside its bounds,
  is deterministic, and differs from an empty canvas (parametrised test over all
  kinds); `prop` op places it at ft coordinates.
- [x] **T22 scatter.** Poisson-disk sampling (Bridson) in a mask/region, density
  per square, min spacing ft, random rotation/scale jitter, `avoid` masks.
  *Accept:* ≥5 tests: no two points closer than spacing; all inside the mask;
  count tracks density ±20%; deterministic.
- [x] **T23 Overlay.** `grid(mask clip, alpha, weight)`, `compass`, `scale_bar`
  ("1 square = 5 feet"), `title`, `label`, `frame`, `legend` (auto from the ops
  used). *Accept:* ≥3 tests each: grid lines at exact multiples of px/square;
  grid clip respected; the legend lists only the kinds present.

## M5 — Outputs and CLI

- [x] **T24 Export.** PNG (LANCZOS down from working res), `.dd2vtt` (DESIGN §3),
  `.meta.json` (named geometries + recipe `measure:` block). *Accept:* ≥6 tests:
  dd2vtt matches a pinned minimal schema (hand-written fixture in
  `tests/mapgen/fixtures/uvtt_min.json`); coordinates are in squares; image
  base64 round-trips to the PNG; meta lists the declared measures.
  *Owner check (non-blocking):* import one proof into Foundry (Universal
  Battlemap Importer) or Roll20 and confirm the walls line up.
- [x] **T25 CLI.** `python -m mapgen render <recipe> [--out DIR] [--draft]
  [--only-png]`, `python -m mapgen ops [--markdown]`. *Accept:* ≥5 tests via
  subprocess or the main(argv) function: render writes 3 files; draft is smaller;
  `ops --markdown` contains every registered op; bad recipe exits 2 with the step named.
- [x] **T26 Goldens.** Three tiny recipes in `tests/mapgen/goldens/` (stone room
  with a door, cave with water, grass clearing with trees) at 20 px/sq; hash
  compare; `--update-goldens` pytest option. *Accept:* goldens pass twice in a row
  (determinism across processes); changing one op param fails the right golden.

## M6 — Quality bar

- [x] **T27 Metrics.** `quality.py`: normalise to 50 px/square, crop box, compute
  Q1–Q5 (DESIGN §7.2); Q6 for our own renders using the grid mask. *Accept:*
  ≥3 tests per metric on synthetic images (flat grey has Q2≈0; a checkerboard has
  high Q4; a two-colour image has 2 hue clusters).
- [x] **T28 Comparator manifest and baseline.** `comparators.yaml` for C1–C7 (zip
  path, member, category, px_per_square measured by counting grid lines over
  ≥10 squares, crop box excluding frame/legend). A script computes metrics and
  writes per-category bands to `docs/RESEARCH_mapgen_comparators.md` (numbers +
  method only) and `mapgen/quality_bands.yaml`. *Accept:* the test computing live
  comparator metrics skips without `MAPGEN_REF_DIR`; the bands file is loaded by
  `quality` and has every Phase-1 category; nothing image-derived but numbers is committed.
- [x] **T29 Contact sheet.** `python -m mapgen sheet <our.png> --vs C2` → side-by-side
  at matched scale, written only to a scratch path given by `--out` (refuses a
  path inside the repo). *Accept:* ≥3 tests (with a synthetic comparator): the
  output shape, matched scale, refusal of a repo path.

## M7 — Style, proofs, skill

- [x] **T30 Style preset + macros.** Fill out `inked_parchment.yaml`: defaults per op
  and macros `stone_room(rect, door_sides)`, `cave_room(points)`,
  `corridor(path, width)`, `stream(path, width)`, `tree_clump(region, count)`.
  *Accept:* each macro renders in a golden-sized test; the macros are documented in
  `ops --markdown`.
- [x] **T31 Proof A, canon: the Crystal Court.** Recipe
  `conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml` built only
  from `facts.yaml` and the chapter V/VIII text that `maps/build_maps.py`
  `map_court` already encodes (floor 80×140, aisles 20 ft, dais, main doors 10 ft,
  east doors, stairs, galleries). No new furniture or props beyond what that
  function draws; ask the owner before adding any. *Accept:* a test reads
  facts.yaml and asserts the meta.json measures (no literals); the dd2vtt walls
  enclose the floor; the render is checked by the T33 gate.
- [x] **T32 Proofs B and C, generic.** (B) Cave, owner-neutral description: "60×40 ft
  natural cave; a stream cuts north–south with a plank footbridge; rubble in the
  west lobe; three stalagmites; the entrance opens south onto forest edge." (C)
  Outdoor: "100×70 ft at 5-ft grid: a dirt path crosses a clearing; two ruined
  stone cottages, one roofless with a fallen wall; tree clumps and brush on the
  edges." Built **through the skill workflow** (T34 draft first if ready, else by
  hand). *Accept:* both render; dd2vtt valid; checked by the T33 gate.
- [!] **T33 Quality gate.** *(2026-11-13: B, C and the added D pass all bands at ≈4.0 self-scored; A escalated to the owner, see LOG; awaiting owner review)* For A (category: built interior → C1/C4 bands),
  B (cave → C2/C5) and C (outdoor → C3): run `quality`, build contact sheets,
  score the rubric for ours and the comparator, tune the style/material params,
  repeat. Log every iteration's metrics + scores. *Accept:* all Q1–Q5 in band, Q6
  < 0.5, rubric average ≥ 4.0 with no score below 3 for each proof; then
  **stop for owner review** of the three PNGs beside their comparators. If after 3
  tuning rounds a category stays below 3.5, escalate per CLAUDE.md with the gap named.
- [x] **T34 Skill.** `.claude/skills/build-map/SKILL.md` (workflow from DESIGN §4,
  canon rule, iteration cap 5, rubric), `references/ops.md` (generated),
  `references/cookbook.md` (the macros + the three proofs as worked examples),
  `references/rubric.md`. Add `references/ops.md` to the CLAUDE.md generated-files
  list and the regenerate line. *Accept:* the no-diff test of `ops.md` against
  `python -m mapgen ops --markdown`; a dry run: the skill builds a fresh owner
  description end to end in ≤5 iterations (logged).
- [~] **T35 Wrap-up.** CLAUDE.md Reference Trigger Index row ("Build a map →
  `/build-map`"); full suite run from `software/` with the pass/fail count in the LOG;
  PR to `main` via `gh`, after scanning main..branch for private canon (memory rule).

---

**Phase 2 (region/city) and Phase 3 (web app)** are decomposed after T33 passes
and the owner has reviewed it (DESIGN §8).
