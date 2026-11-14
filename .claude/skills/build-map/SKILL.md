---
name: build-map
description: Build a battle map (VTT-ready PNG + Universal VTT walls/doors/lights) from a plain-language description, by writing a mapgen recipe, rendering it, looking at it and revising. Use when the user asks to make, draw, build or fix a map for a session, adventure or the Facets/5e web app.
---

# build-map

You turn a description into a **recipe** (`*.map.yaml`), render it with
`software/mapgen`, look at the PNG, and revise until it matches. The recipe is
the source: never edit a rendered PNG. Design: `docs/DESIGN_mapgen.md`.

## Before you start

1. **Read `references/ops.md`** (the op catalogue, generated from the code) and
   **`references/cookbook.md`** (worked patterns). Skim `references/rubric.md`.
2. **Pin the brief.** You need: size in feet, grid (5 or 10 ft), indoor/cave/outdoor,
   every feature, and the mood. Ask at most three questions, and none if the
   description already covers it.
3. **Canon places (iron law).** If the map is a place in an adventure or
   Shattered Origin, read its source text and `facts.yaml` first. Every feature you
   draw must trace to a line there, and put the citation in the recipe's header
   comment. Anything the text doesn't state (furniture, props, extra doors, terrain)
   you **ask about before adding**. Colour follows the approved art brief if one
   exists (Oraga: `docs/REFERENCE_oraga_palace_visual_brief.md`, TP74). Generic or
   homebrew maps may be embellished within what was asked.
4. **Where files go.** Adventure maps: `<adventure>/maps/recipes/<name>.map.yaml`.
   Generic maps: `maps/recipes/<name>.map.yaml`. Outputs land in a `mapgen/`
   folder beside the recipe and are git-ignored (they rebuild from the recipe).

## The loop

Run everything from `software/`.

1. **Block out:** header plus geometry only (rooms, cave outline, paths), with
   `include: [styles/inked_parchment.yaml]` and `- {op: base}` first. Render a draft:
   `python -m mapgen render <recipe> --draft --out <scratchpad>`.
   Open the PNG with Read and check the layout against the brief: sizes, where
   the doors are, what connects to what.
2. **Dress:** materials, shadows, walls, openings, props, scatter, then `finish`,
   compass, scale bar, title. Prefer the style's macros (`stone_room`, `cave`,
   `cave_floor`+`cave_walls`, `stream`, `ground_patches`, `brush`, `finish`) and drop to
   raw ops only for detail. Draft again.
3. **Look and critique:** Read the PNG. Score it against `references/rubric.md`,
   then list concrete defects ("the bridge floats past the bank", "the door on the
   east wall reads as a gap", "trees cover the cottage").
4. **Revise:** edit the recipe, re-render the draft, look again. Stop at a rubric
   average ≥ 4 with nothing under 3, or after **5 iterations**, then report what's
   left.
5. **Final:** a full render (drop `--draft`), then the metrics:
   `python -m mapgen quality <png> --recipe <recipe> --category <built_interior|cave|outdoor>`.
   If the owner's comparator packs are present you may also build a contact
   sheet (`python -m mapgen sheet <png> --vs C2 --out <scratchpad>/sheet.png`).
   Sheets and comparator images go **only** to the scratchpad, never into the repo
   (the command refuses repo paths).
6. **Report:** the recipe path, the PNG and `.dd2vtt` paths, the metric line,
   your rubric scores, and the defects you couldn't fix. For a canon map, also
   list every feature with its source line, plus anything you left out pending a ruling.

## Rules of thumb

- **Shading convention:** light from the north-west, shadows fall south-east. A sunken area
  (a floor inside walls) is shaded inside its north and west edges (`shade_lines` default; inner
  `shadow` with a negative offset such as `[-0.6, -0.8]`). A raised mass (forest, brush, hill)
  is shaded inside its south and east edges (`shade_lines` with `shadow: [-0.6, -0.8]`; inner `shadow`
  with a positive offset). Ink line-work carries the depth: the owner wants hatching, not soft gradients.

- **Coordinates are feet**, origin north-west, y runs **south**. If a source uses
  y-north, flip once and say so in the header comment.
- **Name things you'll measure or reference:** the `out` of a room geometry,
  the wall's `name:` (doors snap to the named wall nearest `at`), and `measure:`
  entries for canon sizes (they land in `meta.json` for tests).
- **Give scatter/noise steps an `id:`** so inserting a step later doesn't
  reshuffle them.
- **Walls go around the walkable floor** (`wall`, band outside the edge).
  Interior walls between rooms are `partition` (centred on a line). `exclude`
  leaves a wall open (a cave mouth onto a forest).
- **Order matters:** ground → floors → water/paths → walls → openings → props →
  line-work (`shade_lines`, `cracks`, `stipple`) → overlay. No grid unless asked: the owner
  prefers gridless maps and the VTT draws its own. Water drawn before walls tucks under them; clip it to the
  walkable mask (`stream ... clip: walk`).
- **Draft renders are quick:** a few seconds. A full render of a 100×70 ft map
  takes about a minute.
- **The VTT data is generated with the art.** Walls emit line of sight, doors
  emit portals, `light` emits lights. Windows keep the wall's LOS (UVTT has no
  window type).
- **New ops or materials:** the catalogue is generated. After changing the code,
  regenerate `references/ops.md` with `python -m mapgen ops --markdown >
  ../.claude/skills/build-map/references/ops.md` (a test checks they match).
