# Visual brief: the mists region (battle maps)

Source: the owner's concept art, `references/mists_concept.jpg` (added 2026-11-15). The tents, camp, fires
and figures are out of scope for the beach map. Region maps that show a camp will need their own ruling.
This brief covers only the look. Names, history and inhabitants are the owner's canon, and nothing here
adds any.

## What the concept shows

| Element | In the concept | Our `mist_coast` today |
|---|---|---|
| **Palette** | Nearly monochrome cold green-greys (green and blue just above red). Mean RGB ≈ (0.42, 0.45, 0.44), saturation 0.18 | A cold cyan-blue cast, mean RGB ≈ (0.46, 0.51, 0.53). Reads "blue sea" where the concept reads "grey murk" |
| **Value range** | Very wide: near-black silhouettes (5th pct 0.04) against glowing mist (95th pct 0.86) | Compressed (0.19–0.74). Everything mid-grey, nothing truly black or truly bright |
| **Light** | One diffuse, bright source (a pale sun or moon) seen through the mist. The mist is *lit*: brightest near the source, falling off away from it | Uniform haze and an even glow. No source, no falloff |
| **Sand** | Grey, not white. Pale and wet only at the waterline. Dark hummocky dunes and ridges inland, darkest in the foreground | White sand everywhere, with a pale berm |
| **Sea** | Rough: grey-white churn, whitecaps scattered right across it, wide broken surf, rocks awash | Calm dark water with a few smooth crests. Foam only at the waterline |
| **Wood** | Everywhere, all black: lines of sharpened stakes and palisades, leaning poles, rickety piers on stilts running out into the surf, posts standing in the water | None |
| **Trees** | Thin palms behind the beach, black against the mist | None |
| **Stones** | Black rocks on the sand and awash in the surf | Black stones: matches |
| **Mist** | Thick, luminous banks hugging the ground, densest round structures and along the shore, thinning out to sea and upward | Banks and wisps, but blue-tinted, and similar density everywhere |
| **Texture** | Vertical streaks (drizzle or falling mist) over the whole picture | None. In plan view this could be a fine directional grain, not literal streaks |

## Targets for every map in this region

1. **Palette:** cold green-grey, with green and blue a touch above red. Never warm or yellow, never
   cyan-blue. The values are in `styles/mists_region.yaml`. Only the light source's centre goes faintly
   warm (`mist_glow`).
2. **Values:** wood, rocks and palms near-black (`#141513`). Mist and foam near-white. Let the light
   source blow out a little.
3. **One light source per map,** placed off one edge: a broad radial glow, plus mist that is brighter
   on that side.
4. **Dark dunes inland,** hatched heavily, with the pale beach only at the waterline.
5. **Rough sea:** whitecaps across the whole sea and a wider band of broken surf.
6. **Black timber:** stake lines, palisades, leaning poles, piers on pilings into the surf, posts awash.
   Palms at the back of the beach.
7. **Mist** thick at ground level and round every structure, thinning toward the open sea.

## Toolset gaps this brief needs (gap check)

- Props: `stake`, `piling` (a post seen from above), `palm` (fronds from above), `driftwood`.
- An op that places props along a line at a spacing, with lean and gap jitter. It would serve fences,
  palisades, pier pilings and stake rows, and is useful well beyond this region.
- Whitecaps: a cookbook pattern (small noise blobs on the sea, white with a shadow) or a macro.
- A region style, `styles/mists_region.yaml` (done 2026-11-15): palette, materials (`ash_sand`, `wet_ash`,
  `dune_dark`, `grey_sea`) and macros (`rough_sea`, `dunes`, `lit_mist`). Every map in the region includes
  it, so they match. Stake lines and piers wait for the camp maps (owner, 2026-11-15: the first map is
  the beach only, with no stakes, palisades, piers or palms).
