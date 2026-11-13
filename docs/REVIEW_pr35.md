# Review: PR #35 (`feat/mapgen` vs `feat/lean-facets`)

Reviewer: independent subagent, 2026-11-13. Scope: `git diff feat/lean-facets...feat/mapgen`
(76 files, about 10k lines). The suite was green when I ran it:
`python3 -m pytest tests/mapgen tests/test_map_board.py -q` gave 336 passed, and
`tests/test_no_private_canon.py` gave 5 passed. Reproduction scripts are in the session scratchpad
(`island.py`, `fuzz.py`, `los.py`, `css.py`). Nothing tracked was modified.

Severity counts: 1 high, 5 medium, 9 low. Policy: no images or image-derived data from the comparator
packs are in the diff (only paths, crops and metric numbers), contact sheets refuse to write inside
the repo, and the private-canon guard passes.

---

## Confirmed

### R1 (high): The board breaks on maps taller than the viewport. Fog leaks the hidden map and tokens sit in the wrong place.
- **Where:** `software/app/static/css/style.css` (`.map-board { max-height: 75vh; overflow: auto }`, `.map-fog { position:absolute; inset:0; height:100% }`), `software/app/static/js/map.js:37-41` (token `top:%`), `map.js:91-99` (drag and snap).
- **What's wrong:** Absolutely positioned children of a scroll container measure percentages against the container's visible box, not the scrolled content. Three things go wrong:
  1. A token at `top: y/squares.y*100%` is placed relative to the 75vh box, not the image.
  2. The fog SVG (`height:100%`) covers only the first 75vh of the image. When a player scrolls, everything below that is unfogged.
  3. On pointerup, `(e.clientY - rect.top)/sq` ignores `board.scrollTop`, so a token dropped on a scrolled board lands on the wrong square. During a drag, `top` uses `rect.height` while the snap uses `rect.width/squares.x`.
- **Reproduction:** I ran headless Chromium on the same CSS: an 800 px-wide board, `max-height:300px`, 1000 px of content. Result: `{boardH: 300, scrollH: 1000, tokenTop: 270 (for top:90%; should be 900), fogH: 300}`. The canon Crystal Court (150×172 ft, portrait) overflows 75vh at any normal panel width, so it hits this case.
- **Fix:** Put the image, fog and tokens in an inner `position:relative` wrapper sized to the image (`.map-stage { position:relative }` inside the scroller), and position everything against that wrapper. Compute drop coordinates from the wrapper's `getBoundingClientRect()`, which already includes the scroll. Use the same function for the drag preview and for the snap.

### R2 (medium): XSS from .dd2vtt contents. The image and map size go into HTML without escaping.
- **Where:** `map.js:57` `<img src="${m.image}" …>`; `map.js:17` `${x.squares.x}×${x.squares.y}`; `map.js:39-40` `style="left:…;width:${size}%"`; `map.js:46-49` `viewBox="0 0 ${m.squares.x} ${m.squares.y}"`. Server side: `websocket.py` `_map_set` copies `data["image"]` and `res["map_size"]["x"/"y"]` from the file verbatim, with no type or charset check. `_map_list` does the same with `squares`.
- **What's wrong:** The board takes any `**/mapgen/*.dd2vtt`, not only mapgen output. `.dd2vtt` is a sharing format, so a file downloaded from elsewhere is a realistic input. A file with `"image": "x\" onerror=\"…"` or `"map_size": {"x": "1\" onload=\"…"}` breaks out of the attribute. The CSP keeps `script-src 'unsafe-inline'`, so inline event handlers run, in every player's browser once the MM shows the map (the viewBox case needs fog on).
- **Fix:** On the server, require `image` to match `^[A-Za-z0-9+/=]+$` (and optionally that it decodes to PNG, JPEG or WebP magic bytes), and require `map_size.x/y` and `pixels_per_grid` to be finite positive numbers below a cap. Reject the map otherwise. On the client, wrap every interpolation in `esc()` or `Number()`, including `m.image`, `x.squares.*` and `m.squares.*`.

### R3 (medium): `_scan_maps` walks the whole repository synchronously on the event loop, on every `map_list` and `map_set`.
- **Where:** `websocket.py` `_scan_maps` (`sorted(root.glob("**/mapgen/*.dd2vtt"))` with `maps_dir` defaulting to the repo root, `config.py`); `_map_list` (`json.loads(path.read_text())` on every map).
- **What's wrong:** The glob descends into `.git`, `data/` and everything else before `_SKIP_DIRS` filters the results. The skip set doesn't prune the walk, and the 200 cap is applied after `sorted()` has walked everything. On this checkout (59k files) one scan took **4.9 s wall-clock**, during which every session on the server is frozen. `map_set` re-scans just to resolve one id. `_map_list` then fully parses every `.dd2vtt`, each holding a multi-MB base64 PNG, only to read `map_size`.
- **Fix:** Walk with `os.walk` and prune `_SKIP_DIRS` and dot-directories in place, cap the number of directories or files visited, cache the result (refresh only on `map_list`), and resolve `map_set` from the cache. Read `map_size` from `meta.json` (small) or stream-parse it. Run the scan in `asyncio.to_thread`. Consider defaulting `maps_dir` to a dedicated folder rather than the repo root.

### R4 (medium): Rasterizing a MultiPolygon drops an island that sits inside another part's hole, depending on part order.
- **Where:** `software/mapgen/ops/masks.py` `rasterize_patch`. The loop draws each polygon's exterior, then fills its holes with 0, polygon by polygon.
- **What's wrong:** If the island comes before the holed polygon in `geoms`, the later hole fill erases it. Shapely doesn't guarantee part order out of `difference`, `make_valid` or `buffer`.
- **Reproduction:** A ring (`box(0,0,50,50) - box(10,10,40,40)`) plus an island `box(20,20,30,30)`. With order `[island, ring]` the island's centre coverage is **0.0**; with `[ring, island]` it is 1.0.
- **Fix:** Draw every exterior first and then every hole, rasterizing islands after holes. Simpler: rasterize each polygon into its own layer and take the max, or sort parts so the containing polygons come first.

### R5 (medium): Secret doors are baked into the only image, which goes to players. Foundry receives them as ordinary doors.
- **Where:** `ops/semantic.py` `secret_door` (draws a red "S" onto `into`, default `canvas`); `export.py` `uvtt` (drops the portal's `secret` key); `_map_set` (sends that image to every client).
- **What's wrong:** No player version of the image exists. Any map with a secret door, including the `proof_cellar` recipe, shows the "S" to every player on the board, and on Foundry after import. In the `.dd2vtt` the secret portal is just a closed portal, so Foundry creates a visible, normal door.
- **Fix:** Either render a player PNG without the S markers (secret-door glyphs on a separate layer composited only into the MM image), or document this clearly and have the board refuse or warn. Decide whether to emit secret doors as plain wall in the UVTT LOS, since UVTT has no secret flag.

### R6 (medium): Every map event rebuilds a multi-MB `innerHTML` for every client, and an incoming event cancels a drag in progress.
- **Where:** `app.js` `token_moved` / `token_removed` / `fog_state` → `refresh(['play'])`; `play.js` `renderPlay` rebuilds `mapBoardHtml()`, which embeds the `data:` URI each time; `map.js:85-101`.
- **What's wrong:** Any token move by anyone, and any other play-tab refresh (rolls, chat, enemy updates), re-serializes the multi-MB image string into the DOM on every client. `token_move` has no rate limit, so a player dragging or spamming moves makes every client re-parse that string. If any message arrives mid-drag, the dragged element is replaced, the pointer capture is lost and the move is dropped.
- **Fix:** Render the board once per `map_state` into a persistent node. On `token_moved`, update only that token's `style`. Convert the data URI to a `Blob` object URL once. Skip re-renders while a drag is active, or patch the board instead of rebuilding it. Add a server-side throttle on `token_move`.

### R7 (low): A malformed .dd2vtt kills the MM's WebSocket connection.
- **Where:** `websocket.py` `_map_set` (`res["map_size"]["x"]`, `"data:image/png;base64," + image`); `_dispatch` catches only `WSError`, `ValueError` and `KeyError`.
- **What's wrong:** If `resolution` or `map_size` is a list or string, or `image` is not a string, the handler raises `TypeError`. That escapes `_dispatch`, reaches the endpoint's catch-all `except Exception`, and closes the MM's socket. `_map_list` would also crash on `json.loads(...).get` when the top level is a list (`AttributeError`).
- **Fix:** Validate the structure and catch `TypeError`/`AttributeError` in `_map_set` and `_map_list`, turning them into a `WSError` (overlaps with the validation in R2).

### R8 (low): Uncaught non-`RecipeError` exceptions on edge inputs. The CLI only catches `RecipeError`.
- `wall` or `partition` with `material:` set, on geometry entirely outside the frame: `rasterize_patch` returns `None`, then `m[patch.slices]` raises **AttributeError** (`ops/semantic.py`, both ops). Without `material` it passes, because `composite_patch` handles `None`.
- `path_label` with an empty `src` geometry raises **IndexError** (`ops/overlay.py` `path_label`).
- A map whose width or height rounds to 0 px (e.g. `width_ft: 0.2` at 10 px/square): `Engine.run` succeeds, then export raises **ValueError: height and width must be > 0** (`export.to_pil`).
- `_load_style`: an include file whose YAML top level isn't a mapping raises `AttributeError` on `data.get`.
- **Reproduction:** `fuzz.py` in the scratchpad (outputs above).
- **Fix:** Guard `patch is None` in both ops. Raise `RecipeError` for an empty `path_label` source. Validate in `MapHeader` that `out_size` is at least 1 px. Type-check include data.

### R9 (low): A door cuts 0.08 ft off any neighbouring LOS wall that touches its jamb, leaving a hairline gap in the VTT walls.
- **Where:** `ops/semantic.py` `_cut_los`. It buffers the door segment by 0.08 ft and subtracts that from **every** LOS line it touches, not only the host wall.
- **Reproduction (`los.py`):** Partition A from (10,10) to (10,20), partition B from (10,10) to (30,10), and a 10 ft double door filling A. B's LOS becomes `(10.08,10)→(30,10)`, while the portal ends at (10,10). Its endpoint no longer meets the door, so Foundry vision can leak through. The Crystal Court has exactly this layout: the `east_doors` double door fills its partition, and `passage_n` starts at that jamb.
- **Fix:** Cut only lines that belong to the named wall (keep the wall's LOS lines in `collector.walls[name]` and cut those), or subtract a zero-width segment and snap endpoints. Add a test asserting that LOS endpoints coincide with the portal endpoints.

### R10 (low): Canon recipe differs from its cited source and adds a feature.
- **File:** `conversions/dnd5e/oraga_night/maps/recipes/crystal_court.map.yaml` checked against `facts.yaml` and `maps/build_maps.py` `map_court`/`geometry()`. Most coordinates check out exactly under the stated (x+30, 160−y) transform: piers, dais, high table, all six ward points, garden, main, west, service and east doors, gallery stairs, east stair, corridor and rails.
  - **Stair door width:** the recipe has `door, wall: stair_w, at: [130,125], width: 8`. The SVG uses `P.door(sx, sy, G["east_door_w"])` = **10 ft**, spanning Y 120–130.
  - **Invented light:** `{op: light, at: [70,30], radius: 30, color: "#f0a8d4", glow: true}` puts a VTT light source with a 30 ft range at the dais. Neither `facts.yaml` nor `map_court` has one, and "the lights" are a plot point in the module (they die at midnight). This contradicts the recipe's own header ("Nothing else is drawn … ask the owner before adding any").
  - **Terrace width:** the terrace rect spans the full 150 ft width (X 0–150). The SVG terrace is `gw*2+W_` = 120 ft (X 10–130). This is minor, since it falls in the margin.
- **Fix:** Set the door width to 10, remove the light (or get an owner ruling), and clip the terrace to X 10–130.

### R11 (low): The fog exposes data to players, and its area list is noisy.
- **Where:** `_fog_areas`, `session.to_player_state_dict` (`"map": self.active_map`), `token_moved` broadcasts.
- **What's wrong:** Players receive every area name (recipe `out` names, which may be spoilers such as `secret_vault`), every foe position and the full image, whatever the fog shows. The code comments say this is a visual screen, but the MM UI doesn't. `_fog_areas` also offers **every** named geometry with area: in the Crystal Court that means `p1`…`q7` (piers), `wd1`…`wd6` (wards), `high_table`, `terrace` and so on, up to a cap of 60 in insertion order. Reveals use bounding boxes, so an L-shaped room uncovers its neighbours.
- **Fix:** Use only geometries the recipe explicitly marks as areas (for example `area: true`, or a `fog_areas:` list). Tell the MM in the UI that fog is cosmetic. Optionally strip foe tokens and unrevealed area names from player payloads.

### R12 (low): Tests are below the project's 3-per-public-function rule and miss the bugs above.
- In `tests/mapgen`, 20 ops are exercised exactly once: `double_door`, `ellipse`, `frame`, `grow`, `invert`, `label`, `legend`, `occlusion`, `opening`, `paper`, `path_label`, `portcullis`, `roughen`, `scale_bar`, `secret_door`, `stairs`, `threshold`, `title`, `vignette`, `window`. No edge or error test exists for most of them. That is why the R8 crashes went unnoticed.
- The door/LOS tests (`test_m4_semantic_props.py`) assert only the **total** LOS length after a door. A cut in the wrong place, or the jamb trim in R9, still passes.
- `test_map_board.py` has 1 test each for `map_clear` and `token_remove`, with no player-denied case for either. It has no tests for a malformed `.dd2vtt` (R7), non-numeric or hostile `image`/`map_size` values (R2), a non-numeric or NaN `x` (the `_float` NaN branch is untested), a player without a character, or `map_set` resetting tokens. The e2e fog check counts `<rect>` elements but never checks what is actually visible (R1).
- `test_no_path_traversal` can't fail with the current dict-lookup design. It is harmless, but it says nothing about symlinks or the walk.

### R13 (low): Smaller issues.
- `ops/semantic.py` `portcullis`: the docstring says "sight passes", but the op emits a **closed** portal, which blocks sight in Foundry until opened.
- `.gitignore`: `**/mapgen/*.png` (and `.dd2vtt`, `.meta.json`) also matches the package dir `software/mapgen/`. A future texture or fixture PNG there would be silently untracked.
- `docs/DECISIONS.md` M6 says the new dependency is `opensimplex`. The code doesn't use it (`noise.py` explains why) and `requirements.txt` doesn't list it. The doc is stale.
- `quality.py` sets `PImage.MAX_IMAGE_PIXELS = None` at import, which turns off Pillow's decompression-bomb guard for the whole process. Scope it to the comparator load.
- A macro call's `seed_offset` (and `out`, unless the macro body uses `${out}`) is silently swallowed into the macro environment (`recipe._expand`). An author who sets `seed_offset` on a macro call gets no effect and no error.

---

## Suspected (not reproduced)

### S1 (low): UVTT `map_size` can be fractional.
`export.uvtt` writes `round(width_ft/fps, 4)` when the width isn't a multiple of the grid (for example 52 ft gives 10.4 squares), and `MapHeader` doesn't require whole squares. The repo's conformance test rounds `map_size*ppg` to the PNG size, so this passes. Some importers and VTTs assume integer squares and may misalign the grid. Consider requiring whole squares for `unit: ft` battle maps.

### S2 (low): The square grid is offset by half a working pixel.
`ops/overlay.py` `grid` measures distance from the pixel's left edge (`arange(n) % sq`), not its centre. The line occupies working pixel `[k*sq, k*sq+1]`, about ¼ output pixel right/down of the true boundary at supersample 2, and the right and bottom border lines never draw. This is cosmetic. I have not checked whether VTT grid overlays visibly disagree.

---

## Checked and found OK
- Path traversal in `map_set`: ids resolve only through the scanned dict. In Python 3.12, `Path.glob("**")` did not follow symlinks in my test, so neither a symlink loop nor a link out of the tree was reached.
- MM-only enforcement for `map_*`, `fog_*` and `token_remove` uses the decorator. Players can move only `pc:<own identity>`. Token coordinates are clamped and NaN is rejected.
- Map titles, area names, token labels and character names are escaped with `esc()`, which escapes quotes. The CSP adds only `img-src 'self' data:`, with no `data:` in `script-src`.
- Engine determinism: per-step crc32 seeds, no `hash()`, no set iteration, `default_rng` throughout. The golden test passes across `PYTHONHASHSEED` values.
- The y axis is consistent: the NW origin with y south in `units.Frame`, the rasterizer's pixel-centre convention, `trace`'s contour offsets, the light glow, the UVTT points and the fog bounds all agree.
- Repo policy: no image files in the diff. The comparator data is paths, crops and metric numbers only. `make_sheet` refuses output paths inside the repo. `ops.md` regeneration is tested.

---

## Resolution (2026-11-13, by the PR author)

| ID | Resolution |
|---|---|
| R1 | The board is now a persistent `.map-canvas` (image, fog layer, token layer) inside a separate `.map-scroll`. Fog and tokens are positioned against the image box, and the drag uses the canvas rect, so scrolling can't skew it. The e2e test asserts the fog height equals the image height on a board taller than its scroll box. |
| R2 | Server: `_load_board` requires a finite size (0.5–2000) and a pixels-per-grid of 10–1000, and an image of base64 charset whose magic bytes are PNG, JPEG or WebP. Anything else is a `WSError`. Client: the board is built with DOM properties, `textContent` and `Number()`, never HTML strings. Eight hostile-file tests. |
| R3 | `os.walk` prunes `.git`, `data`, venvs and dot-directories in place, with directory and result caps. The result is cached (refreshed on `map_list`, reused by `map_set`) and runs in `asyncio.to_thread`. `map_list` reads sizes from the small `meta.json` and skips files without one. Tests cover pruning and the no-meta skip. |
| R4 | `rasterize_patch` draws each part on its own layer and combines them by max when there are several parts with holes. Tested in both part orders. |
| R5 | `secret_door` paints no mark by default (`mark: true` for a DM-only print). It keeps the wall's LOS and is left out of the UVTT portals, but stays in `meta.json`. Three tests. |
| R6 | Token moves and fog changes patch the persistent board, and only tray changes re-render the tab. The image node is reused across renders. Drags are never interrupted. `token_move` has a 33 ms per-player throttle, applied after validation, with a burst test. |
| R7 | All parsing and structural errors in `_load_board` become a `WSError`. The socket stays up (parametrized tests). |
| R8 | `None`-patch guards in `wall`/`partition`; an empty `path_label` source or zero-length line raises `RecipeError`; `Frame` rejects maps under 1 px; a non-mapping include raises `RecipeError`; the CLI turns any other exception into an "internal error" message with exit code 3. Tests for each. |
| R9 | The door cut stops 1e-3 ft short of each jamb, so walls meeting the jamb keep their endpoint. Tests check the perpendicular wall and that the LOS ends coincide with the portal bounds. |
| R10 | Stair door 10 ft (`east_door_w`); the dais light removed (no light without a source); terrace X 10–130 = `terraces.wide`. Canon tests for all three, plus a "no lights" test. |
| R11 | Recipes can declare `fog_areas` (court: floor, aisles, garden walk, stairwell; cellar: rooms and halls). Without them, only shapes of at least 4 squares are offered. Player payloads (join state, `map_state`) omit unrevealed area names and foes in the fog. A foe moving into the fog sends players `token_removed`. The MM UI states that the picture itself still reaches players. Four privacy tests. |
| R12 | About 45 tests added for the twenty thinly covered ops (edge and error cases), plus LOS-endpoint, hostile-file, NaN, reset, denial, throttle and fog-privacy tests. |
| R13 | Portcullis docstring corrected; `.gitignore` anchored to `maps/**/mapgen/` and `conversions/**/mapgen/`; DECISIONS M6 corrected; `MAX_IMAGE_PIXELS` raised only for the duration of a comparator load; a macro call's `seed_offset` propagates to its body (tested). |
| S1 | **Kept.** The Foundry importer (moo-man/FVTT-DD-Import) computes the scene size as `map_size × pixels_per_grid` and handles fractional squares. Requiring whole squares would only constrain authors. Documented here. |
| S2 | The far grid line is drawn when the map ends on a square boundary. The half-pixel offset is deliberate (lines sit on whole pixel columns for crispness) and amounts to ¼ output px at supersample 2. |

Tests after the fixes: full suite (excluding e2e) **2260 passed**; e2e **13 passed**.
