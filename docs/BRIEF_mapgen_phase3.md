# BRIEF (DRAFT) — mapgen Phase 3: maps in the Facets web app

*Brain tier, draft, 2026-11-13. Written while the Phase 1 owner review (T33) is
pending, so the next step can start from a plan. **Nothing here is decided.**
The owner's answers to the open questions settle it.*

## Problem

mapgen now makes battle, region and town maps with Universal VTT data (walls,
doors, lights). The owner wants to run 5e from the Facets web app, but the app has
no map view. Its play tab handles rolls, chat, sparks and an enemy tracker
(`active_enemies`, `enemy_spawn` over the WebSocket), with no spatial board.

## Goal

The Mirror Master loads a map into a live session; players see it, with tokens
for characters and active enemies, and the MM can reveal it room by room.

## Non-goals (proposed)

- No rules automation on the map: no movement costs, auto line-of-sight
  combat, or initiative. The project philosophy is that the digital layer absorbs
  bookkeeping, not judgement.
- No dynamic lighting or vision simulation in v1. The `.dd2vtt` walls and lights
  are stored for later.
- Not a Foundry or Roll20 replacement. Exporting to them stays the supported route
  for tables that want a full VTT.

## Approach options

| Option | What it is | For | Against |
|---|---|---|---|
| **A. Map board in the SPA** (recommended) | A canvas in the play tab: map image, grid, draggable tokens synced over the existing WebSocket; MM fog by painted reveal mask | Fits the vanilla-JS SPA and session model; small; the whole table stays in the app | Fog and tokens are new state to sync and persist |
| B. Image-only map | Show the PNG; no tokens | Trivial | Hardly better than a shared image |
| C. Embed an open-source VTT | e.g. an iframe to a self-hosted tool | Rich features | A second system to run; licences; off the project's grain |

## Downstream considerations

- **State:** maps attach to a session (`session.active_map`: map id, revealed
  mask, token positions). Tokens reference characters and `active_enemies` keys,
  so the enemy tracker and the board can't drift apart.
- **Assets:** the session stores the recipe-rendered PNG and `.dd2vtt`. The app
  never renders recipes live (a full render takes a minute or more).
- **Reveal:** v1 fog is a mask the MM paints or reveals per room. Rooms come from
  `meta.json` named geometries, a cheap win the recipe format already provides.
- **Tests:** WebSocket handler tests in the existing style (`test_api*.py`) plus
  one e2e flow (Playwright is already an optional dev dependency).

## Open questions for the owner

1. Is the in-app board wanted at all, or is exporting `.dd2vtt` to Foundry or
   Roll20 enough for your table?
2. If wanted: tokens for player characters only, or enemies too, tied to the
   enemy tracker?
3. Fog of war in v1, room-by-room reveal, or none?
4. Does this belong to a wider "5e in the Facets app" brief (character sheets,
   2014 rules), which hasn't been written yet?

*Draft.*

## Status (2026-11-13): v1 built on defaults, all reversible

Option A was built as a minimal, rules-free v1 while these questions wait. Each
default below changes with a one-line edit if the owner answers differently:

- Q1 (wanted at all?): built. Deleting `app/static/js/map.js` plus the `map_*`/`token_*`
  handlers removes it cleanly.
- Q2 (whose tokens?): both PCs and active enemies; players move only their own
  token, and an enemy's token leaves when it leaves the tracker.
- Q3 (fog?): **none**. Not built, pending the answer.
- Q4 (wider 5e brief?): unanswered. The board is system-neutral plumbing.

Details: `docs/LOG_mapgen.md` (Phase 3 v1).
