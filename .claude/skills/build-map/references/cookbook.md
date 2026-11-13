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
  - {op: finish, floor: floor}
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
  - {op: grid, alpha: 0.7, weight: 0.09, color: "#1f1b16"}
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

## Fixing common defects

| Defect | Fix |
|---|---|
| Water pokes through a wall | Draw it before the walls and clip it to the walkable mask |
| Trees swallow a building | `grow` the buildings' mask by about half a tree's size and pass it as `avoid` |
| Walls look like black sausages | `weight: bold` inside, `outer_weight: fine`, a lighter wall material |
| Floor looks flat | More `contrast`, add `grain`, a wider inner `shadow` (4–5 ft in caves) |
| Grid fights the floor | Lower its `alpha`, or clip it with `mask:` |
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
  - {op: grid, shape: hex, orientation: pointy, alpha: 0.3}
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

Use `unit: ft` with `feet_per_square: 50` (or 25 or 100), and usually no grid.
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
