# mapgen cookbook

Working patterns. The three proofs are complete examples:

- `maps/recipes/proof_cave.map.yaml`: a natural cave with a stream, a bridge, rubble,
  stalagmites, and a mouth onto a forest edge
- `maps/recipes/proof_ruins.map.yaml`: an outdoor clearing with a path, two ruined
  cottages, brush and trees
- `conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml`: a canon
  interior built from `facts.yaml`, with a custom palette, partitions and double doors

## Skeleton

```yaml
map:
  title: Name
  width_ft: 60
  height_ft: 40
  feet_per_square: 5     # 10 for big outdoor maps
  px_per_square: 70      # VTT standard; 50 for very large maps
  supersample: 2
  seed: 1
  include: [styles/inked_parchment.yaml]
measure:                 # optional: sizes tests can check (named geometries)
  room: {w: 30, h: 20}
steps:
  - {op: base}           # parchment canvas named `canvas`
  # ... geometry, floors, walls, props ...
  - {op: finish}
  - {op: compass, at: ne}
  - {op: scale_bar, at: nw}
  - {op: title, text: Name, position: bottom}
```

## A single stone room with a door

```yaml
  - {op: rect, out: room, x: 10, y: 8, w: 30, h: 20}
  - {op: stone_room, src: room, name: floor, wall: w}
  - {op: door, wall: w, at: [25, 8], width: 5}
  - {op: prop, kind: table, at: [25, 18], size: 6}
```

## Several rooms joined by corridors

Union the floors first, then wall them once. Walls drawn per room would
overlap where the rooms touch.

```yaml
  - {op: rect, out: hall, x: 10, y: 10, w: 30, h: 20}
  - {op: rect, out: cell, x: 50, y: 12, w: 15, h: 15}
  - {op: path, out: corridor, points: [[40, 20], [50, 20]], width: 5, cap: flat}
  - {op: union, out: rooms, of: [hall, cell, corridor]}
  - {op: rasterize, out: rooms_pre, src: rooms}
  - {op: beyond, floor: rooms_pre, depth: 4}
  - {op: floor_fill, src: rooms, name: floor, material: flagstone}
  - {op: wall, src: rooms, name: w, thickness: 1.5, material: wall_stone}
  # a door between corridor and cell needs a wall there: use a partition
  - {op: path, out: cell_wall, points: [[50, 17.5], [50, 22.5]], line: true}
  - {op: partition, src: cell_wall, name: cellw, thickness: 1, material: wall_stone}
  - {op: door, wall: cellw, at: [50, 20], width: 4}
```

## Cave with water under the walls

```yaml
  - {op: polygon, out: shape, points: [...]}
  - {op: roughen_geom, out: cave, src: shape, amount: 1.1, scale: 6, id: rough}
  - {op: cave_floor, src: cave}                    # mask: floor
  - {op: stream, points: [...], width: 5, clip: floor}
  - {op: cave_walls, src: cave, wall: rock}
  - {op: prop, kind: bridge, at: [x, y], size: 10, rotate: 0}
  - {op: scatter, kind: rubble, region: [[...]], avoid: [stream], density: 0.9, spacing: 2.6}
```

A cave mouth onto the outside: draw the outside region, then
`cave_walls ... exclude: outside_geometry`.

## Outdoors

```yaml
  - {op: canvas, out: canvas, material: earth}
  - {op: ground_patches, name: grass, material: meadow, scale: 14, cover: 0.0}
  - {op: path, out: road, points: [...], width: 6, smooth: 3}
  - {op: roughen_geom, out: road, src: road, amount: 0.7, scale: 5}
  - {op: rasterize, out: road_m, src: road}
  - {op: fill, mask: road_m, material: dirt_path}
  - {op: stroke, src: road, width: 0.16, dash: [1.4, 0.5, 0.25, 0.5], jitter: 0.6}
  # brush at the edges, trees standing in it, a clear margin round buildings
  - {op: brush, name: brush, within: edges, clear: clear, scale: 16, cover: -0.15}
  - {op: scatter, kind: tree, mask: brush, avoid: [clear], density: 0.55, spacing: 7, size: 10, shadow: 0.6}
```

`cover` sets how much ground a noise region takes: lower values cover more
(−0.3 is most of the map, 0.3 a few patches).

## Ruins

`wall ... style: ruined, gaps: 0.2` breaks the walls with noise and emits LOS
only where wall stands. A fallen wall is `exclude: <rect over that side>` plus
rubble scattered outside it.

## Canon interiors

Put the source citations and any coordinate flip in the header comment. Name
every measured shape and list it under `measure:`, then add a test that reads
`facts.yaml` and compares (see `software/tests/mapgen/test_m7_proofs.py`).
Interior walls with doors are `partition`s. Don't draw furniture the text doesn't state.

## Mood, mist and weather

Full example: `maps/recipes/mist_coast.map.yaml`.

- **The recipe's own colours and materials:** put `palette:`, `materials:` or `ink:` at the top
  level of the recipe, beside `map:`. They win over the included style, entry by entry.
- **Grain and drift:** give `noise` `stretch` (features that many times longer) and `angle`
  (0 = east, 90 = south) for wind ripples, drifting fog, strata or wood grain. `warp` drags any field
  or mask through a noise flow; its `drift` smears it downwind. For swirls, blur the mask first, then
  `warp` with `curl: true, iterations: 4-5` (eddies like smoke), and optionally a second `warp` with
  `iterations: 2` to fold the edges into filaments.
- **Surf:** a broken foam line at the break plus a net of lace behind it: `cells` (scale ~1 ft), `remap`
  small edge distances to 1, `field_to_mask`, then multiply by a band off the shore and a noise mask
  that fades with `distance` from the beach, so the net breaks up seaward. `combine` with the sea so it
  stays on the water, and a `shadow` (`mode: drop`) south-east under it.
- **Wave crests:** offsets of the shore, each closed again (`offset` by D + R, then by −R, with R growing
  with D) so the far crests forget the shore's corners. Stroke them white with `taper: 0.9`, and add
  a thin dark line just on the shore side of each (the shadow under the lip). `clip: sea_m` keeps the
  near ones off the sand.
- **Sand that reads as sand:** (1) `roughen_geom` the sea with `mode: cusps` (period 4-5 ft, amount ~0.5)
  for a scalloped waterline; build the beach as frame minus that sea, and draw the land shape past
  the frame so no slivers of sea are left at the map's edges. (2) A berm: a band 6-11 ft up from the
  sea, `shade_lines` with `shadow: [-0.6, -0.8]`, plus a tapered dashed scarp line. (3) A wrack line: a
  thin noise-broken band at the berm's foot, dark fill, `hatch` with `angle_jitter: 180` for weed,
  pebbles scattered along it. (4) Ripples: `isolines` of stretched noise stroked with `clip` set to
  `facing` of the same noise (the shadow side only), times a dry-sand mask. (5) Grain: `stipple` with
  a `weight` mask of noise, so the dots clump, and a second pass weighted by the ripple shadows.
  (6) Beached stones: their `footprints` get a pale drop shadow on the lee side (a sand tail) and a dark
  one on the sea side (a scour hollow).
- **Shelving beach:** `stipple` from the sea mask (`side: outside`, `falloff` 5-7 ft): densest at the water.
- **Hugging the props:** `footprints` is a mask of the props drawn so far (by `of` step ids or
  `kinds`). Band it for a ring of mist, snow or grime round each stone, subtract it so the stones stand
  out of the fog, or pass it to a later `scatter` as `avoid`.
- **Mark mood layers `atmosphere: true`** (dimming, mist, rain, darkness). `quality --recipe` then also
  measures the map with them left out and checks the bands on that, so fog can't hide thin line-work
  underneath. Steps that only make layers still run; only paint is dropped.

```yaml
  - {op: noise, out: mist_a, scale: 12, stretch: 2.5, angle: 170, id: mist_a}
  - {op: warp, out: mist_a, src: mist_a, amount: 4, scale: 9, curl: true, iterations: 5, drift: [-2.5, 0.4], id: mist_curl}
  - {op: footprints, out: stones_m, kinds: [boulder, rubble]}
  - {op: band, out: stone_pool, src: stones_m, inner: 0.3, outer: 2.2}
  - {op: mix, out: mist_f, of: [mist_a, stone_pool], weights: [1, 0.45]}
  - {op: field_to_mask, out: mist_m, src: mist_f, lo: -0.1, hi: 0.6}
  - {op: combine, out: mist_m, of: [mist_m, stones_m], mode: sub}
  - {op: fill, mask: mist_m, color: "#cfe7ee", blend: screen, opacity: 0.6, atmosphere: true, id: mist}
```

## A building of many wings (inns, taverns, compounds)

Full example: `maps/recipes/painted_lantern.map.yaml`.

- **Wall each wing on its own** so the joins show: put wings flush, so the walls sit side by side, then cut
  one `opening` through each wing's wall at the same spot (`floor_material` set to that wing's floor).
  Give each wing its own wall material and thickness: `wall_wattle` (with `style: rough`) for the
  oldest part, `wall_timber`, or a recipe-level painted one (`ramp_noise`, ridged, scale ~1.5).
- **One floor per wing**, recipe-level for bright paint (`planks` in a loud colour), then fill a noise
  mask of `wood_floor_rough` over it to wear the paint through where the crowds walk. `rushes` over
  `wood_floor_rough` for an old taproom. `clay_floor` (`dirt`, terracotta) for a cheap shop floor.
- **Colours per prop:** `prop` and `scatter` take `colors: {part: colour}`, which repaints named parts
  for that step only. Felt on card tables, blankets on beds, rugs and banners per wing. Put the
  defaults in the recipe `palette`.
- **Gaming and shop props:** `card_table` (felt, cards, chips), `dice_table` (rail, felt, dice),
  `wheel` (painted wedges), `counter` (long, mugs), `stool`, `shelf` (coloured goods), `hearth`.
  Ring stools round a table by computing positions; a short generator script is fine, but the recipe
  it writes is the source.
- **Dark but colourful:** keep the hues and drop their value: oxblood, bottle green, smoky teal,
  tarnished mustard, dull indigo. Place the lamps (`light`, no glow), then one `darkness` step
  (`strength` ~0.6, `pool` ~0.6, `warmth` ~0.35, `atmosphere: true`). Everything goes dark except warm
  pools round the lamps, so the corners stay black. Override `earth` darker at recipe level for a
  night yard.
- **Chaos, not order** (owner, 2026-11-15: "far too ordered ... a very chaotic place"):
  - Draw each wing straight, then knock it askew by 5-15°. Use the `transform` op, or compute the
    points, then place props in the wing's own coordinates and rotate them the same way.
  - Give wings bump-outs, slanted sides and lean-tos, never plain rectangles.
  - **Tack newer wings onto older ones** (owner, 2026-11-15: "one structure tacked together", not
    separate buildings). Work oldest first. Each newer wing reaches into the one it joins (add an
    extension if needed), and is cut along everything older (`difference` with each older floor grown
    by its wall thickness). Then wall it with `exclude` set to the older floors grown the same way, so
    each join is the older building's wall alone. Put one `opening` (or `secret_door`) through that wall
    at the join, and check it lands in a common space (corridor, landing, aisle, taproom), never in
    someone's room.
  - Keep a separate outbuilding for a **plank walk over mud**: a door in each wall, a `mud` strip with
    puddles (noise ∩ mud filled with `water`), and a `boards` prop laid square from door to door.
  - Pack tables by random rejection sampling (minimum spacing, keep-outs round rugs and bars), with
    random rotation, and shove the odd stool back.
  - `scatter` `clutter` over every floor, plus `sack`, crates and barrels in heaps. Add patch planks
    on floors and repairs in walls: `wall_band` ∩ a region, filled with another material.

## Region styles (a shared look across many maps)

When the owner supplies concept art for a region, write a visual brief (`docs/REFERENCE_<region>_visual_brief.md`)
and a region style (`software/mapgen/styles/<region>.yaml`) that includes `inked_parchment.yaml` and adds the
region's palette, materials and macros. Every map in the region then puts `include: [styles/<region>.yaml]` in
its header, so all of them share one look.

- **Measure the concept, don't eyeball it:** mean RGB (the colour cast), mean saturation, and the 5th/95th
  percentile of brightness (the value range). Compare your render with the same numbers. The comparator bands
  in `quality` come from bright commercial maps and don't apply to a deliberately murky region.
- **The mists region** (`styles/mists_region.yaml`, example `maps/recipes/mist_coast.map.yaml`):
  - cold green-grey materials (`ash_sand`, `wet_ash`, `dune_dark`, `grey_sea`)
  - `dunes`: dark hummocks inland, hatched as raised masses
  - `rough_sea`: whitecaps across the open sea, plus swell strokes
  - `lit_mist`: one light source through the mist, a radial glow that brightens the mist near it
  - dim with `murk` (neutral, never blue), and keep haze off the stones so they stay near-black

## Fixing common defects

| Defect | Fix |
|---|---|
| Water pokes through a wall | Draw it before the walls and clip it to the walkable mask |
| Trees swallow a building | `grow` the buildings' mask by about half a tree's size and pass it as `avoid` |
| Walls look like black sausages | `weight: bold` inside, `outer_weight: fine`, a lighter wall material |
| Floor looks flat | More `contrast`, add `grain`, a wider inner `shadow` (4–5 ft in caves) |
| Looks flat or "digital" | Add line-work: `shade_lines` along walls and edges, `cracks` on floors, `stipple` grit near walls |
| A grid appears | Remove the `grid` step: maps are gridless by default (the VTT draws its own) |
| Door snaps to a corner | The edge you meant isn't a wall boundary (the rooms were unioned): add a `partition` |
| Render too slow | Use `--draft` while iterating; a full render at 70 px/sq takes about 1 s per 100 ft² of map |

## Region maps (miles and hexes)

Set `unit: mi` in the header. Then `width_ft`/`height_ft` are miles and
`feet_per_square` is the hex size in miles (the field names are kept from battle
maps). Render at about 125 px per hex, which is print resolution; `--draft` is
fine for layout. Full example: `maps/recipes/proof_region.map.yaml`.

```yaml
map: {title: The Coast, unit: mi, width_ft: 60, height_ft: 80, feet_per_square: 5, px_per_square: 125,
      include: [styles/inked_parchment.yaml]}
steps:
  - {op: canvas, out: canvas, material: sea}
  - {op: polygon, out: coast_shape, points: [...]}              # draw the coast you want
  - {op: roughen_geom, out: land, src: coast_shape, amount: 1.1, scale: 4}
  - {op: rasterize, out: land_m, src: land}
  # height = distance inland + noise + hand-placed ridges, then weathered
  - {op: distance, out: inland, src: land_m, side: inside}
  - {op: remap, out: inland, src: inland, in_range: [0, 38], out_range: [0.05, 0.55]}
  - {op: path, out: ridge_line, points: [...], width: 9}
  - {op: rasterize, out: ridge_m, src: ridge_line}
  - {op: blur, out: ridge_m, src: ridge_m, sigma: 3.5}
  - {op: mix, out: height, of: [inland, ridge_m], weights: [1, 0.5]}
  - {op: mix, out: height, of: [height, land_m], mode: mul}      # sea = 0
  - {op: erode, out: height, src: height, iterations: 15}
  - {op: fill, mask: land_m, material: lowland}
  - {op: coastline, land: land}                                  # shore ink, shallows, waves, sea hatching
  - {op: forest_mass, src: forest_polygon}
  - {op: rivers, out: creeks, src: height, sea_level: 0.03, threshold: 0.012, width: [0.15, 0.45]}
  - {op: mountain_range, src: height, level: 0.56, within: land_m}
  - {op: scatter, kind: hill, mask: hill_band, density: 2.4, spacing: 1.9, size: 2.3, sort_y: true}
  - {op: prop, kind: city, at: [x, y]}                           # also town, village, ruin_marker, peak
  - {op: legend, at: sw}
```

- **Rivers:** draw the river a story needs as a `path`, and let `rivers` add the
  tributaries from the height field. They run downhill, end at the sea, the map
  edge or a larger river, and widen downstream.
- **Contour lines:** `isolines` on the height field (`interval: 0.1`), then
  `stroke` them fine.
- **Overlap:** `sort_y: true` on glyph scatters draws north to south, so nearer
  mountains overlap farther ones.
- **Metrics:** `quality --category region` compares at the comparator's width (1500 px).

## Town maps

Use `unit: ft` with `feet_per_square: 50` (or 25 or 100). Like every map, no grid.
Render at about 3.3 px per foot (`px_per_square: 166` at 50 ft) to match print
town maps, with `supersample: 1`, because these maps are large. Full example:
`maps/recipes/proof_town.map.yaml`.

```yaml
  - {op: canvas, out: canvas, material: lowland}
  - {op: noise, out: relief, scale: 380, octaves: 3}
  - {op: isolines, out: contours, src: relief, interval: 0.12}
  - {op: stroke, src: contours, width: 1.2, dash: [14, 5, 3, 5], jitter: 0.5, opacity: 0.55}
  - {op: path, out: road, points: [...], width: 24, smooth: 3}       # streets as polygons for paint
  - {op: path, out: road_line, points: [...], line: true, smooth: 3}  # the same street as a line for lots
  - {op: frontage, out: houses, roads: [road_line], road_width: 28, avoid: keep_clear}
  - {op: buildings, src: houses}                                     # gabled roofs, shadows, ink
  - {op: buildings, src: temple, roofs: ["#6b6f7c"]}                 # a landmark in its own colour
  - {op: fill, mask: field_m, material: field_tilled}                # also field_green
```

`frontage` keeps lots clear of every road, of `avoid`, and of each other. Put
squares, landmarks, water and fields in `avoid`, and use `within` for a walled town.
