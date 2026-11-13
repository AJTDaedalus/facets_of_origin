# Verification: PR #35 review fixes (commit `d0ea4c6`)

Verifier: independent subagent, 2026-11-13. Checked against the code, not against the "Resolution"
section of `docs/REVIEW_pr35.md`. No tracked file was modified. A temporary test file was created
under `software/tests/` and then deleted.

**Test runs**
- `python3 -m pytest tests/mapgen tests/test_map_board.py tests/test_websocket.py -q`: **649 passed** (151 s)
- `python3 -m pytest tests/e2e/test_ui_flows.py -q`: **13 passed** (15 s)

Scratch reproductions are in `/tmp/claude-0/-root-facets-of-origin/eb46f7a0-189d-4dd6-848a-6d5e583a84cc/scratchpad/`:
`island.py`, `los.py`, `fuzz.py` (re-run unchanged), `css2.py` (R1 against the real `style.css`),
`capture.py` (N1).

---

## Per-finding status

| ID | Status | Evidence |
|---|---|---|
| R1 | **RESOLVED** | `css2.py` loads the real `style.css` with an 800×1000 image in a 300 px `.map-scroll`. Result: canvas 1000, fog 1000, a token at `top:90%` centres at 900 px. After `scrollTop=500` the canvas rect top is −500 and the token is still at 0.9. The drag preview and the drop both use `MAPUI.el.getBoundingClientRect()` (`map.js:126,138`). Caveat: the e2e assertion never checks that the image is actually taller than `.map-scroll`. With a 32×32 ft map at 1440×1000 it may pass without testing anything (see N7). |
| R2 | **RESOLVED** | Server: `_load_board` (`websocket.py:~1543`) checks `_num` bounds on size and ppg, applies the base64 regex, caps length at 60 MB and checks PNG, JPEG or WebP magic. Client: the board is built with `createElement`, `.src`, `.textContent` and `setAttribute` with `Number()`. The remaining HTML strings in `mapBoardHtml` pass every server string through `esc()` and the squares through `Number()`. The `map_list` title is capped at 200 characters and escaped. |
| R3 | **RESOLVED** (one note) | `os.walk` prunes in place, runs in `asyncio.to_thread`, caches results, and `map_set` resolves from the cache. On this checkout one scan takes 0.8 s, off the event loop. Note: the walk still descends into the gitignored `software/tests/_test_data` (about 160k dirs here), so it hits `_MAX_DIRS=20000` every time. Today's maps are found only because `conversions/` and `maps/` sort before `software/`. See N5. |
| R4 | **RESOLVED** | `island.py`: island centre coverage is 1.0 in both part orders (was 0.0 / 1.0). |
| R5 | **RESOLVED** | `secret_door` no longer calls `_cut_los` and draws the S only with `mark: true`. `export.uvtt` skips portals with `secret`, which are still recorded in meta. `proof_cellar`'s secret door now shows as solid wall to everyone. Trade-off: the MM has no in-app marker for it. The decision is documented. |
| R6 | **PARTIAL** | Fixed: the board node persists, token moves patch only the token layer, there is a server throttle, and the image is decoded once. Not fixed: (a) any play-tab re-render during a drag still detaches the board node. That drops pointer capture and can leave `MAPUI.dragging` stuck at `true` (N1). (b) Fog changes now resend the full multi-MB `map_state` to every client and rebuild the tab (N2). |
| R7 | **RESOLVED** | Every parse in `_load_board` is wrapped and turned into a `WSError`. `_map_meta` returns `{}` for a non-dict top level, so a list in `meta.json` can't raise `AttributeError` in `map_list`. Parametrized tests confirm the socket survives. |
| R8 | **RESOLVED** | `fuzz.py` re-run: `wall offframe material` and `partition offframe material` now pass. `path_label empty` raises `RecipeError`. A zero-px map raises `RecipeError` in `Frame`. An include that isn't a mapping raises `RecipeError` (tested). The CLI catch-all returns 3. Small gap: a macro call with a non-integer `seed_offset` raises `ValueError` from `int()` (`recipe.py:202`), which reaches the catch-all rather than a `RecipeError`. |
| R9 | **RESOLVED** | `los.py`: partition B keeps `(10,10)→(30,10)`, and the host wall leaves 1e-3 ft stubs that meet the portal bounds `[[10,10],[10,20]]`. |
| R10 | **RESOLVED** | Stair door `width: 10`, the dais light removed (no `light` op left in the recipe), terrace `x:10 w:120`. These match `facts.yaml` (terraces 120 ft wide) and `east_door_w`. |
| R11 | **RESOLVED** (new leak, N3) | `fog_areas` is declared in recipes and validated in `export.meta`. The fallback uses a 4-square minimum. `player_map_view` strips unrevealed area names and fogged foes on the join `state` and on `map_state`. `_push_state` goes through `state_for`, which calls `to_player_state_dict`, which calls `player_map_view`, so no path sends players the full board. Bounding-box reveal is unchanged, but the curated lists make it acceptable. |
| R12 | **RESOLVED** (gaps) | 43 tests in `test_review_fixes.py`, plus new board tests (hostile files, NaN, reset, denial, throttle, privacy, scan). Gaps: no test covers a drag surviving a re-render, what players receive when a foe moves inside the fog, or a fog toggle's payload size. The R1 e2e check may test nothing (N7). |
| R13 | **PARTIAL** (minor) | Done: portcullis docstring, `.gitignore` anchored (`git check-ignore software/mapgen/foo.png` no longer matches), DECISIONS M6, `MAX_IMAGE_PIXELS` scoped, macro `seed_offset` propagates (no existing recipe uses it on a macro call, so no golden output changes). Not addressed: a macro call's `out` is still silently swallowed when the body doesn't use `${out}`. |
| S1 | **ACCEPTED-AS-DOCUMENTED** | The resolution gives its reasoning: the Foundry importer computes `map_size × ppg`. Reasonable. |
| S2 | **RESOLVED** | The far grid line is drawn when the map ends on a square boundary (`overlay.py` `grid`). The half-pixel offset is kept on purpose and documented. |

---

## New findings in `d0ea4c6`

### N1 (medium): A play-tab re-render during a drag drops pointer capture, and can freeze the token layer on that client
- **Where:** `software/app/static/js/play.js:17,25` (`root.innerHTML = ...` on every play refresh), `software/app/static/js/map.js:154-170` (`slot.appendChild(MAPUI.el)`), `map.js:118-146` (drag code, no `lostpointercapture` handler), `map.js:87` (`if (MAPUI.dragging) return;`).
- **What's wrong:** The board node persists, but every `refresh(['play'])` replaces the tab's `innerHTML`, which detaches `MAPUI.el` for a moment before `wireMapBoard` re-appends it. When the capture target leaves the document, Chromium releases pointer capture and fires `lostpointercapture`. map.js listens only for `pointerup` and `pointercancel`. After one fast pointer movement the pointer is no longer over the token, so `pointerup` lands elsewhere and `finish()` never runs. The move is lost, and `MAPUI.dragging` stays `true`. From then on `updateBoard()` returns before redrawing tokens, so every token move from anyone is invisible on that client. This lasts until that user starts another drag, or a different map is loaded (`ensureBoard` reuses the node, and its stale flag, for the same map).
- **Triggers that refresh the play tab mid-drag:** any roll or chat line that refreshes the tab, any `token_removed` (including N3's hidden-foe moves, which reach every player), a newly placed token (`isNew`), every fog change (N2), enemy updates and `danger`.
- **Reproduction:** `capture.py` mirrors the structure (`innerHTML` rebuild, then re-append the persistent node). Output: `capture before rerender: True`, `capture after rerender: False ['lost']`, then after a fast move and mouse-up, `dragging still true: True`.
- **Fix:** Handle `lostpointercapture` with the same `finish` (and send the move from the last known position). Don't detach the board on re-render: keep the board slot outside the re-rendered `innerHTML`, or have `renderPlay` skip re-rendering (or defer) while `MAPUI.dragging`. Reset `MAPUI.dragging` whenever the map changes or `ensureBoard` runs.

### N2 (medium): Every fog toggle or reveal resends the whole map image to every client and posts "The map is up" into everyone's feed
- **Where:** `websocket.py` `_fog_set` and `_fog_reveal` call `_push_board` (a full `map_state`). `app.js:357` `map_state(m) { state.map = m.map; if (m.map) feedSys(\`The map is up: …\`); refresh(['play']); }`.
- **What's wrong:** Before this commit, fog changes sent a small `fog_state`. Now each checkbox click sends the full board, including the multi-MB base64 image, to every connection. On the client each one posts a new "The map is up: …" line to the feed for everyone, and runs a full play-tab rebuild (a trigger for N1). An MM revealing five rooms produces five multi-MB broadcasts and five feed lines per client. The image node is still reused, because the `src` string compares equal, so the cost is bandwidth, the feed noise and the re-render.
- **Reproduction:** A temporary WS test: after `map_set`, `fog_set {enabled:true}` gives P1 `['map_state']` with `"image"` present.
- **Fix:** Send a light message without the image, e.g. `{"type":"map_view","fog":…,"tokens":…}`, split per role: the MM gets the full fog and tokens, players get `player_map_view` minus `image`. Have the client merge it into `state.map` and call `mapRefresh`. Call `feedSys` only when `m.map.id` changes.

### N3 (low): A foe moving inside the fog sends players `token_removed` on every move
- **Where:** `websocket.py` `_token_move` → `broadcast_split(moved, {"type":"token_removed", …})` whenever the token isn't visible to players.
- **What's wrong:** The visible-to-hidden transition is handled correctly. But a foe that is already hidden and moves again sends players `token_removed foe:<key>` every time. Players learn that an unseen foe exists, its key, and when the MM moves it. Each message also runs `mapRefresh(true)`, a full play-tab rebuild on every player client (feeding N1).
- **Reproduction:** A temporary WS test: fog on, the MM moves a foe twice, both outside revealed areas. P1 receives `[{'type':'token_removed','token':'foe:standard_1'}, {'type':'token_removed','token':'foe:standard_1'}]`.
- **Fix:** Compute visibility before and after the move. Send players `token_removed` only when it changes from visible to hidden, and `token_moved` only when visible after the move. Otherwise send players nothing (use `send_to_identity(…, "mm", moved)`).

### N4 (low): The throttle is keyed per identity, not per token, and drops moves instead of coalescing them
- **Where:** `websocket.py` `_token_move`, `key = (ctx.session_id, ctx.identity)`, with an early `return` when inside 33 ms. `_last_move` is module-level and never pruned.
- **What's wrong:** An MM who moves pc:Player1 and then places pc:Zahna within 33 ms has the second move dropped with no error. In the reproduction the board ended with only `pc:Player1`. A player's dropped final drop leaves their token drawn at the unsnapped drag position (map.js sets `left`/`top` during the drag and never gets an echo), which disagrees with the server until the next redraw. The dict grows by one entry per (session, identity) forever; that's negligible but unbounded across sessions.
- **Fix:** Key by `(session, identity, token)`. Better, coalesce: keep the latest position and apply it at the end of the window, or apply it and suppress only the broadcast. When a move is throttled, echo the authoritative position to the sender. Clear entries in `map_set`, `map_clear` and session teardown.

### N5 (low): The map scan hits the directory cap on a normal dev checkout and can silently miss maps
- **Where:** `websocket.py` `_scan_maps_sync`, `_MAX_DIRS = 20000`, with `maps_dir` defaulting to the repo root (`config.py:58`).
- **What's wrong:** Here the pruned walk would visit about 160k dirs, nearly all of them under the gitignored `software/tests/_test_data`. It stops at 20k and finds nothing beyond that point, without warning. The repo's own maps are found only because of sort order (`conversions` and `maps` come before `software`). Rendering to a folder that sorts after a large tree, or a deployment with a big `sessions`-style folder that sorts first, would make maps disappear from the list with no error.
- **Fix:** Default `maps_dir` to the recipe trees (`maps/` and `conversions/`), or prune gitignored and test-output dirs (`_test_data`, `_output`, `tests`). Log or notify the MM when the cap is hit.

### N6 (low, pre-existing, carried over): `touch-action: none` covers the whole board, so touch users can't scroll the map
- `.map-canvas { touch-action: none }` (style.css) now covers the full scrolled content of `.map-scroll`. On a phone or tablet, a portrait map taller than 75vh can't be scrolled by swiping over it. The old `.map-board` had the same problem, so this isn't a regression, but the restructure was the moment to fix it: put `touch-action: none` on `.map-token` only.

### N7 (low, test quality): The R1 e2e assertion may test nothing
- `tests/e2e/test_ui_flows.py` asserts `fog height ≈ img height`, with a comment saying the board is taller than its scroll box. The fixture map is `stone_room` (32×32 ft, square) at a 1440×1000 viewport, and the test never asserts `img > .map-scroll` height. If the image fits, fog equals image whether or not the bug exists. Add `assert dims["img"] > dims["box"]`, using a tall fixture or a narrower viewport. The layout fix itself is confirmed independently by `css2.py`.

---

## Checked and found OK
- No path sends players the unfiltered board. Join `state`, `_push_state` (via `state_for`) and `map_state` all use `player_map_view`. `map_clear` sends `null`. `token_moved` for a PC or a revealed foe is safe. `_drop_token`'s broadcast reveals only removals.
- `fog_state` is no longer emitted, and its client handler was removed. No dead code is left behind.
- `_MAP_CACHE` is global but keyed on the resolved root. A map deleted after caching fails cleanly in `_load_board` with a `WSError`. Concurrent `map_list` calls only race to write identical results.
- Persistent node across a map change, `map_clear` or reconnect: `ensureBoard` rebuilds when the id or image changes and reuses the node otherwise. The only stale state it can carry is the `dragging` flag (N1).
- `fog_areas` validation: `export.meta` rejects undeclared names. `_fog_areas` type-checks the list, the geometry dict, the bounds and the numbers. Only declared names that exist are offered.
- The secret-door change: `proof_cellar` is the only recipe that uses `secret_door`, and the full suites pass, including the proofs and conformance tests.
- `_B64` uses `$`, which also matches before a trailing newline. That is harmless here, because the image goes in through a DOM property, not markup.

---

## Resolution of the verification round (2026-11-13, by the PR author)

| ID | Resolution |
|---|---|
| N1 / R6 | `refresh()` defers any play-tab re-render while a token drag is active (`MAPUI.pendingRefresh`), and runs it when the drag ends. `map.js` also handles `lostpointercapture` by committing the last position seen (an explicit `pointercancel` discards). The e2e test forces a re-render mid-drag (the MM places another token), then checks that the move lands and that the deferred refresh ran afterwards. |
| N2 / R6 | `fog_set` and `fog_reveal` send the MM a `fog_state` (the full fog) and players a `board_patch` (their fog view plus the tokens they may now see), never the image. `map_state` posts "The map is up" only for a new map id. Tested: no message contains the image. |
| N3 | Visibility is computed before and after each move. Unseen before and after goes to the MM only; visible to hidden sends players `token_removed`; hidden to visible sends `token_moved`. A token newly placed straight into the fog counts as unseen. Tested. |
| N4 | The throttle is keyed per (session, token) and coalesces: one broadcast per 33 ms per token, plus a trailing broadcast of the latest position, so the final position always goes out. State clears on `map_set` and `map_clear`. Tests cover the burst's last position and two tokens moved back to back. |
| N5 | The walk prunes `_test_data`, `_output`, `print` and `art` as well. The cap rose to 100k directories; hitting it logs a warning and sets `truncated: true` on `map_list`, which the MM sees as a notice. Tested (pruning, and truncation with the cap patched to 1). |
| N6 | `touch-action: none` now sits on tokens only, so the map scrolls with a finger. |
| N7 | The e2e test asserts the image is taller than its scroll box before checking the fog height. |
| R13 (partial) | A macro call that passes `out` to a macro whose body never uses `${out}` raises `RecipeError`. A macro that does use `${out}` works as before. Tested both ways. |

Tests: full suite (excluding e2e) **2267 passed**; e2e **13 passed**.

---

## Round 2 verification (commit `e3fb2d8`, independent verifier, 2026-11-13)

Checked against the code. Reproductions are in the session scratchpad: `capture2.py` loads the real
`map.js` and `style.css` with stubbed globals, and the board WebSocket checks ran from a temporary
test file under `software/tests/`, deleted afterwards. The only tracked file touched is this section.

**Test runs:** `tests/mapgen tests/test_map_board.py tests/test_websocket.py`: **656 passed**. `tests/e2e/test_ui_flows.py`: **13 passed**.

### Status

| ID | Status | Evidence |
|---|---|---|
| N1 / R6 | **RESOLVED** | `capture2.py` (real map.js): a `refresh(['play'])` during a drag is deferred (`dragging true, pending true`). A direct `renderTab()` mid-drag, which the `state` handler still does on reconnect or `next_session`, now drops capture. `lostpointercapture` then commits the last position (`sent [{token_move … x 5.5, y 4.5}]`), clears `dragging`, and runs the pending refresh. Nothing stays stuck. The `done` guard stops the implicit `lostpointercapture` after `pointerup` from committing twice. The e2e test covers the deferred path. |
| N2 | **RESOLVED** | After `fog_set` the MM gets `['fog_state']` and P1 gets `['board_patch']`. No message carries the image. `map_state` posts "The map is up" only when the map id changes. |
| N3 | **RESOLVED** | A foe moved twice inside the fog: P1 receives nothing (`[]`). Moving into an unrevealed area: nothing. Reveal: a `board_patch` with the foe. Moving from visible to hidden: one `token_removed`. |
| N4 | **RESOLVED** | Eight player moves in one burst: the MM gets x = `[0.0, 7.0]` (leading plus trailing, final position kept). Throttle keys are (session, token). A pending flush followed by `map_clear`, or by `map_set` with tokens reset, sends nothing and doesn't bring the token back (`_broadcast_move` re-reads `session.active_map` and returns when the token is absent). No exception or unraisable warning appeared. |
| N5 | **RESOLVED** (note R2-2) | A scan of this checkout takes 0.003 s, is not truncated, and finds no maps (none rendered). `truncated` reaches the MM as a notice. |
| N6 | **RESOLVED** | `touch-action: none` is on `.map-token` only. |
| N7 | **RESOLVED** | The e2e test asserts `img > box + 50` before comparing the fog. |
| R13 | **RESOLVED** | `out` on a macro call raises unless the macro body contains `${out}`. Body values are the only place `_subst` substitutes (param defaults are not substituted), and nested calls pass `out: ${out}` through the parent body, so the check has no false positive for macros that pass `out` along. No macro in the repo uses `${out}` today, and no recipe passes `out` to a macro. |

### Remaining notes from round 2 (all low, none blocking)

- **R2-1 (low): flush tasks are fire-and-forget.** `asyncio.get_running_loop().create_task(flush())` in `_token_move` keeps no reference. In practice the sleeping task is kept alive through its timer handle, and `_broadcast_move` can't raise (manager sends swallow errors), so I saw no leak or lost exception. A module-level `set()` of tasks with `add_done_callback(discard)` would follow the asyncio docs. `_last_move` is cleared on `map_set` and `map_clear`, but not when a session ends with a map still up. That's one small dict per token, so it's negligible.
- **R2-2 (low): the scan prunes the names `print` and `art` at any depth.** Today these match only the gitignored `conversions/dnd5e/oraga_night/print/` and `/art/` (painted art, PDFs), which is the intent. But a recipe kept in, say, `maps/art/` or `adventures/x/print/` would render to `…/art/mapgen/` and never appear in `map_list`, and since this isn't a cap hit, `truncated` stays false. Prefer anchored paths (e.g. skip `conversions/*/*/art` relative to `maps_dir`), or document the reserved names in the build-map skill.
- **R2-3 (low): a `state` message mid-drag ends the drag early.** The `state` handler calls `renderTab()` directly rather than `refresh()`, on reconnect and after `next_session`'s `_push_state`. The move commits at the last seen square and the board stays consistent, so the user only has to drag again. Routing that call through `refresh()` would defer it like everything else.
- **R2-4 (low): a map change mid-drag commits against the old map.** `finish()` closes over the old `m` and the old `MAPUI.el` box. If the MM swaps or clears the map while a player is dragging, the drop sends a `token_move` sized for the old map: on the new map the token reappears, clamped; after a clear the player sees a "No map on the board" error. Fix: in `finish()`, skip the commit when `state.map` is not `m` or the map id changed.

### Verdict

No R- or N-finding remains open, and no medium-or-higher regression came in with `e3fb2d8`. R2-1 to R2-4 are low-severity polish and can be follow-ups. **Clean to merge.** Both suites are green (656 + 13).

### Round 2 follow-ups: resolved before merge (2026-11-13)

- **Trailing tasks:** strong references kept in `_move_tasks` (discarded when done). Throttle records are cleared when a session is deleted (tested).
- **Pruned names:** `print` and `art` removed from the scan's skip set (the scan is fast now). A map folder named `art` is listed (tested).
- **Reconnect mid-drag:** the `state` handler re-renders through `refresh()`, which defers during a drag.
- **Map change mid-drag:** the drop is discarded if the map id changed since the drag began.

Tests: full suite (excluding e2e) **2269 passed**; e2e **13 passed**.
