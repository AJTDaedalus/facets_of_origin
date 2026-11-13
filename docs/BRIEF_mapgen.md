# BRIEF — Programmatic Map Building (`mapgen`)

*Brain tier, 2026-11-13. Hands off to Planner for `DESIGN_mapgen.md` / `TASKS_mapgen.md`.*

## Problem

The owner wants to run 5e from the Facets web app, the way the Oraga Night table
was prepped. Maps are the gap. The Oraga maps under
`conversions/dnd5e/oraga_night/art/maps/` are painted images: they look good,
but they are not to scale, they carry no wall or door data, and every fix means
another round of image generation. The owner wants to **describe a map in plain
language and have Claude build it** as an ordered pipeline of image operations
(shapes, masks, noise, contours, fills, strokes), the steps you'd take by hand
in GIMP, so a map can be rebuilt, adjusted, and kept under version control.

Both kinds are in scope eventually: **battle maps** and **world / region / city
maps**.

## What already exists (web survey, 2026-11-13)

| Option | What it is | Verdict |
|---|---|---|
| [dungeongen](https://pypi.org/project/dungeongen/) (benjcooley, MIT, Python + skia) | Random dungeon generator in a watabou-like hand-drawn style; PNG/SVG out | Generates *random* layouts, so it doesn't fit "describe this room". Worth reading for its noise-driven water and hatching. Not a dependency |
| watabou One Page Dungeon / Cave / City generators | The best-looking random generators around | Closed source, informal image terms, JSON export is flaky. Inspiration only |
| [Azgaar's Fantasy Map Generator](https://git.korz.dev/backups/Fantasy-Map-Generator/raw/commit/05c53d276aaa1153f8d61c6ab515f79fccd6744f/wiki/Home.md) (JS, MIT per mirror) | Full world generator (heightmap, rivers, states) | Random worlds, browser-bound. Its *methods* carry over |
| [Martin O'Leary, "Generating fantasy maps"](https://mewo2.com/notes/terrain) | The standard write-up of region terrain: heightmap, erosion, rivers, zero-contour coastlines | **Use as the method reference for the region op library** |
| WorldEngine, WorldSynth (Python, MIT) | Planet-scale simulation | Too heavy. A planet simulator is the wrong tool for "a valley with a river and two towns" |
| mimir-dm `mapgen` skill | Turns scene YAML into Dungeondraft maps | Closest in spirit (description → config → map), but it locks us into Dungeondraft. The local `mimir-dm` skill only uploads maps and places tokens |
| [generate2dmap](https://tessl.io/registry/skills/github/0x0funky/agent-sprite-forge/generate2dmap) and the text-to-image map sites | Image generation | Same problem as the current Oraga art: no scale, no walls |
| [Universal VTT (`.dd2vtt`/`.uvtt`)](https://dungeondraft-encyclopaedia.gitbook.io/guide/final-steps/exporting-your-map/universal-vtt) | De facto interchange format: image + grid + walls + doors + lights in JSON | **Adopt as our battle-map output format.** Roll20 and Foundry import it (Foundry through a community module) |
| Research: [LLM-proposes / generator-renders](https://arxiv.org/abs/2512.10501) (dual-agent PCG, 2025) | The LLM writes generator *parameters* and a critic refines them; the LLM never draws pixels | **This is the architecture we're choosing** |

**Gap:** nobody publishes *description → editable recipe → deterministic
renderer → scaled image + wall data*. Every random generator skips the
"describe" step, and every image generator skips "scaled and editable". That
gap is the job.

## Approach selected

**A recipe-driven layer compositor, with Claude as the recipe author.**

1. **Recipe** (`*.map.yaml`): a declarative, ordered list of operations on named
   layers. It is the version-controlled source of the map, the way `enemies/*.fof`
   is for the Bestiary. Claude writes and edits recipes. Nobody edits a PNG.
2. **Engine** (`software/mapgen/`): a pure-Python interpreter that runs the
   recipe deterministically (seeded) and writes a PNG plus metadata.
3. **Op library**: small, composable GIMP-like primitives:
   - *Geometry → mask:* `rect`, `polygon`, `circle`, `path` (with width), `boolean` (union/subtract/intersect)
   - *Mask ops:* `grow`/`shrink`, `blur`, `threshold`, `distance_field`, `roughen` (noise-displaced edge)
   - *Fields:* `noise` (fbm/ridged, seeded), `gradient`, `heightmap` (combined fields), `contour` (iso-lines)
   - *Paint:* `fill` (color or procedural texture through a mask), `stroke` (mask edge → wall/coast line), `hatch`, `shadow`, `scatter` (props/trees by density mask)
   - *Overlay:* `grid` (5-ft squares at N px/square), `label`, `compass`, `scale_bar`
   - *Semantic:* `wall`, `door`, `window`, `light`. These paint, **and** they emit UVTT geometry
4. **The skill** (`.claude/skills/build-map/`): tells Claude how to turn a prose
   description into a recipe, render it, **look at the PNG** (vision), critique
   it against the description, edit the recipe, and repeat until it matches.
   One agent plays both proposer and critic, which covers the dual-agent
   pattern without the extra cost.

**Why this over the alternatives:**
- *Over image generation:* exact scale, wall data, cheap edits ("move the
  door 10 ft east" is a one-line diff), reproducible.
- *Over adopting a random generator:* we need *authored* layouts. The Oraga
  rooms have exact canon dimensions.
- *Over Claude writing SVG directly:* SVG handles shapes but has nothing for
  noise, contours, or erosion. The recipe layer also keeps each map short
  and diffable.
- *Over driving real GIMP (Script-Fu):* fragile headless automation, and GIMP
  isn't installed. numpy is GIMP's raster maths without the GUI.

## First pass: battle maps

The owner said to pick whichever is easier to scope. **Battle maps come
first.**
- Bounded: one room or a few rooms, a fixed 5-ft grid, no hydrology.
- Checkable: dimensions can be tested against the text (for example, B7 is
  30×40 ft, so 6×8 squares).
- Useful at the table right away, through UVTT export into the web app or any VTT.
- Exercises every *core* primitive (shape, mask, noise, texture, stroke). The
  region pass adds field ops (heightmap, contour, rivers) on top of the same
  engine. Nothing gets thrown away.

**Phase 2: region / city maps.** Heightmap from layered noise plus hand-placed
"control shapes" (a ridge path, a lake polygon), zero-contour coastlines,
steepest-descent rivers (O'Leary), settlement markers, roads as paths, labels.
City maps sit between the two (walls, districts, street paths) and come after
region maps.

**Phase 3: web app.** A map view in the Facets SPA: show the image on its
grid, place tokens, optionally reveal by room. This belongs to the wider "5e
in the Facets app" initiative, which still needs its own BRIEF.

## Tool / library decisions

- **numpy + Pillow** for raster ops (both installed).
- **scipy.ndimage** for blur, distance transforms, morphology, and labeling (installed).
- **shapely** for polygon booleans and wall-segment extraction (installed).
- **opensimplex** (MIT) for seeded noise, added to `requirements.txt`. Don't
  hand-roll gradient noise.
- **PyYAML** for recipes (already a dependency).
- No skia, no GIMP, no image-generation API. Everything stays offline and deterministic.

## Downstream robustness

- **Determinism:** same recipe + seed gives a byte-identical PNG. Golden-image
  tests (small renders, hash or tolerance compare) catch regressions.
- **Scale is data:** `px_per_square` and `feet_per_square` live in the recipe
  header. Geometry is written in **feet** and the engine converts, so a recipe
  copied from book dimensions can't drift.
- **Walls come from the same source as the paint:** the UVTT walls come from the
  same `wall`/`door` ops that draw the lines, so the picture and the line-of-sight
  data can't disagree. This is the same rule the Bestiary follows: generated,
  never hand-edited.
- **Op registry with schema:** each op declares its parameters (Pydantic), so
  the skill can list the available ops and a bad recipe fails with a clear
  error, not a garbled image.
- **Performance:** a 40×40-square map at 70 px/square is 2800² px, which is
  fine for numpy. Region maps should render at a working resolution and upscale.
- **Licensing:** all code is original. Textures are procedural, not imported
  assets, so there's no asset-licence exposure. Any CC0 texture pack would be
  a later, explicit decision.

## Canon constraint (iron law)

Recipes for **canon places** (Oraga rooms, Shattered Origin regions) may only
contain features the book already states. The skill must tell Claude to ask
before adding furniture, props, or terrain that isn't in the source text.
Generic or homebrew maps described by the owner are fine to embellish within
what was asked.

## Non-goals (first pass)

- Random dungeon generation (dungeongen exists if wanted).
- Painterly or illustrated quality to match the Oraga art. Target is a "clean
  VTT battle map": readable, textured, gridded.
- Multi-floor maps, dynamic lighting simulation, isometric views.
- The web-app map view (Phase 3).

## Open questions for Planner

1. Where recipes live: per adventure (`conversions/dnd5e/oraga_night/maps/*.map.yaml`)
   or a central `maps/`? Recommendation: per adventure, with outputs next to them.
2. Exactly which UVTT fields to emit in v1 (walls, portals, lights, `resolution`)
   and how to test against a known-good file.
3. Texture approach: noise-modulated colour ramps per material (stone, wood,
   grass, water, crystal) defined in a palette YAML. How many materials for v1?
4. Acceptance fixture: ~~B7 Trophy Gallery~~. **Amended 2026-11-13 (Planner):**
   B7 has no canon dimensions in the 2014 module (only its contents are canon), so
   building it would invent a size. The canon proof is the **Crystal Court**
   instead: every dimension is in `facts.yaml`, and `maps/build_maps.py` already
   encodes it. Plus two generic proofs (a cave and an outdoor ruin), judged against
   the comparator maps in DESIGN §7. Resolved in `DESIGN_mapgen.md`.
5. Whether `software/mapgen/` ships inside the app package or as a sibling tool
   under `software/tools/`. It must be importable by the web app in Phase 3.
