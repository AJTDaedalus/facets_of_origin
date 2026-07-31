# Front-End Audit — Production Readiness

**Date:** 2026-07-31
**Scope:** `software/app/static/` (index.html, css/style.css, js/{app,play,tools,builder,components}.js)
against `software/app/api/websocket.py`, `software/app/api/routes/*`, and `software/facets/base/facet.yaml`.

**Question asked:** can the MM or a player do everything the ruleset and the
engine allow, and can they *find* where to do it?

**Method:** enumerated every WebSocket event the server dispatches and every REST
route it exposes, then traced each one to the UI control that triggers it and the
client handler that consumes its broadcast. Anything with no control, no handler,
or a mismatched payload is a finding.

---

## Summary

| Class | Count | Meaning |
|---|---|---|
| **A — Broken** | 9 | Feature exists on both sides but is mis-wired; looks present, does nothing |
| **B — Missing UI** | 20 | Backend capability with no way to reach it from the app |
| **C — UX / discoverability** | 17 | Reachable, but the user has to already know it's there |

The headline finding is **B1**: the MM has no way to apply a Condition to a
player character. Since enemies never roll (PHB III.3 — NPCs attack, PCs react),
`apply_condition` is the *only* path by which an enemy attack lands. The enemy
half of every fight is un-driveable from the UI.

---

## A. Broken — present but mis-wired

**A1. `condition_applied` payload key mismatch.**
Server broadcasts `{player, condition, all_conditions}` (`websocket.py:783`).
Client `onConditionApplied` reads `msg.player_name` and `msg.conditions`
(`play.js:876`). Both are `undefined`, so `conditions` is set to `[]` and the
condition badge never renders. Conditions are invisible to the whole table.

**A2. `condition_cleared` payload key mismatch.** Same shape, same failure
(`websocket.py:799` vs `play.js:890`).

**A3. Technique selection is unreachable.** `technique_select` is gated
`and is_mm` (`websocket.py:224`), but the only control that sends it is the
player-facing `selectTechnique()` in `builder.js:132`. A player clicking
"Select" gets `Unknown event type` back. No MM-side control exists either, so
**no character can ever gain a Technique** — which also means magic never
unlocks past Minor scope.

**A4. No client handler for `technique_selected`.** Even once A3 is fixed the
broadcast falls through `handleServerMessage`'s switch silently.

**A5. Two CSS custom properties are used but never defined.** `--surface`
(endurance bar, resolve bar, clock segment tracks) and `--accent` (posture/scope
hover borders, the "spending N Sparks" label). Undefined `var()` with no
fallback makes the declaration invalid, so bar tracks render with no background
and hover affordances are dead.

**A6. `.rank-master` has no style.** `facet.yaml:1065` defines a Master rank;
`style.css` styles novice/practiced/expert/stub only. A Master skill renders as
an unstyled inline word.

**A7. Campaign notes are write-only.** `saveCampaignNotes()` (`builder.js:356`)
writes to `sessionStorage`; nothing ever reads it back. The MM's notes are gone
on reload, and `sessionStorage` is cleared by `logout()` anyway.

**A8. Magic quick reference contradicts the ruleset.** Tools tab states
"Pre-Technique: Minor scope only, **+1 difficulty step**"
(`tools.js:181`). `facet.yaml:1097` sets `pre_technique_difficulty_penalty: 0`
— the scope restriction alone is the penalty. Violates the CLAUDE.md rule that a
quick reference may never introduce a rule the canonical text doesn't state.

**A9. Combat and Advancement quick references contradict the ruleset.**
- "Strike Outcomes: 10+ = Tier 2 Condition, 7-9 = Tier 1" — true for PvP only;
  against enemies v0.3 Strikes deplete **Resolve**.
- "Armor: Light (Tier 2→1), Heavy (Tier 3→2)" — the actual rule is a per-scene
  **downgrade budget** (Light 2 charges, Heavy 4), which is what
  `combat.armor_budget` implements.
- "Facet Level: every **6** primary skill rank advances" — `facet.yaml`
  `facet_level_threshold: 5`.
- "Major Advancement: every **4** total Facet levels" — `facet.yaml`
  `major_advancement_threshold: 3`.

---

## B. Missing UI — backend capability with no control

### Combat (the critical cluster)

**B1. `apply_condition` — no control. CRITICAL.** The MM cannot land an enemy
attack on a PC. Blocks the enemy half of combat entirely.

**B2. `clear_condition` — no control.** Tier 2 Conditions persist until treated;
nothing can treat them.

**B3. `reveal_postures` — no control.** Postures are declared secretly and then
never revealed, so the simultaneous-declaration mechanic never resolves. The
`#combat-postures-revealed` panel it feeds is dead markup.

**B4. `saving_throw` — no control.** Full handler (`websocket.py:851`), zero UI.

**B5. `contested_roll` — no control.** Full handler (`websocket.py:1038`),
zero UI, and no client handler for `contested_roll_result`.

### Session and Spark cadence

**B6. `session_reset` — no control.** Nothing resets per-session Sparks or
once-per-session Technique use between sessions.

**B7. `act_break` — the real event is unused.** The "Nomination Round" button
(`play.js:1136`) fakes it by posting a chat line instead of sending `act_break`.
No client handler for `act_break_opened`.

**B8. `claim_graceful_fail` — no control.** Players cannot claim their own 6-.
Only the MM-side prompt exists. No handler for `graceful_fail_claimed`.

### Library and content management

**B9. Encounters are write-only.** `saveEncounter()` posts them and
`state.encounterLibrary` is populated from session state, but nothing renders,
loads, edits, deletes, or *runs* an encounter. `DELETE /api/encounters/...`
(B12) is likewise unreachable. An MM who builds an encounter cannot use it.

**B10. `POST /api/characters/upload` — no import UI.** Export exists; import
doesn't. `.fof` characters cannot be brought into a session.

**B11. `notes_mm` — no control.** The character model and the notes endpoint
both carry MM-private per-character notes; nothing writes them.

**B13. Enemies cannot be edited.** Save-new and delete only — changing one stat
means retyping the whole stat block.

**B14. Enemy spawn has no quantity.** Spawning five Mooks is five round-trips
through a two-field form.

**B15. Enemy tracker is `-1 Resolve` only.** No arbitrary damage, no heal/undo,
no way to remove a Condition once added (`prompt()`-added, never removable).

**B16. Threat Clocks: no segment count at creation, no delete.** The backend
accepts `segments` (`websocket.py:1306`); the UI always takes the default.

**B17. The MM cannot see player Sparks.** Nowhere in the app. The MM runs the
Spark economy blind.

**B18. Player Sparks are only spendable via pip-clicking.** Works, but there is
no numeric control and no way to spend on a Strike/Cast except by remembering to
click pips in a different panel first (the Strike form says so in 11px grey).

**B19. MM dashboard: no session delete or archive.**

**B20. Invite generation on the dashboard takes a pasted session ID** rather
than a picker over the sessions listed directly above it.

**B21. No character deletion or rebuild.** A misbuilt character is permanent.

**B22. Players cannot see each other's sheets.** Only the MM gets
`all_characters` rendering. Party-facing information (who has what skill) is
invisible.

**B23. No connection status indicator.** Disconnection appears as one italic
line in a scrolling chat log.

**B24. Invite links have no copy button** — they render as selectable 11px text.

---

## C. UX and discoverability

**C1.** The combat panel is entirely hidden until the MM starts combat, so a
player cannot see their Endurance pool, armor budget, or reaction costs while
planning.

**C2.** The Roll button is disabled until an attribute is clicked, and the only
hint is `-- click an attribute above --` inside a 0.85rem grey line.

**C3.** `strike-target` and `maneuver-target` are free-text inputs. Active
enemies and characters are both already in client state — this should be a
picker.

**C4.** Every MM control that addresses a player takes a **free-typed player
name**: spark award, peer nomination, mark-skill-used, award-advancement. A typo
is a silent no-op — the server returns nothing at all.

**C5.** No notification surface. Errors, spark awards, and combat results all go
into the same scrolling chat log with no visual weight.

**C6.** `alert()` and `prompt()` are used for enemy conditions and every failure
path.

**C7.** No pending/disabled state on async buttons; double-submits are possible.

**C8.** No in-app help. Nothing tells a first-time MM that enemy attacks are
resolved by applying Conditions, or where any given task lives.

**C9.** Truncated copy in the skills footnote: "outside primary Facet. Click
Roll to roll with skill bonus." — the legend for the `●` marker is missing.

**C10.** Rules explanations live only in `title` attributes (postures,
reactions), which are invisible on touch devices.

**C11.** Roll log and chat are capped at 300px/200px inside an already-scrolling
right panel.

**C12.** Nothing shows which phase of the exchange the table is in.

**C13.** No empty states — a player with no character sees blank cards on the
Tools and Builder tabs.

**C14.** MM controls are one long undifferentiated card: Spark cadence, invites,
combat, enemies, and clocks stacked with no grouping.

**C15.** Character creation offers no explanation of what a Facet is, and
background details render as a `textContent` blob with a literal `\n`.

**C16.** Skills table hides the Progress column on mobile with no alternative.

**C17.** Attribute selection state is not announced; no focus ring, no ARIA.

---

## Deliberate non-features

- **No MM dice roller.** NPCs do not roll in this system (PHB III.3) — PCs react.
  Adding a general MM roll invites re-implementing enemy attacks as rolls. The
  Contested Roll tool (B5) covers the legitimate MM-initiated case.

---

## Remediation — applied 2026-07-31

All three classes are closed. Everything below was verified by driving the real
app in a browser, not by reading the diff.

### A — Broken

| # | Fix |
|---|---|
| A1, A2 | Client now reads `player` / `all_conditions`, the keys the server actually sends. Conditions render, and the "absorbed by armour vs. by the reaction" case is reported distinctly. |
| A3 | `technique_select` un-gated: a player selects for themselves (`player_name` is ignored for non-MM callers so nobody can spend another character's pick); the MM may still select on anyone's behalf. |
| A4 | `technique_selected` handled — sheet, Builder, and Magic panel all refresh, and a magic-granting pick lifts the scope cap immediately. |
| A5 | `--surface` and `--accent` defined. |
| A6 | `.rank-master` styled. |
| A7 | Campaign notes load on tab init, autosave on idle, and live in `localStorage` (which `logout()` does not clear). |
| A8, A9 | Quick references corrected against `facet.yaml`, and the advancement numbers are now *read from the loaded ruleset* rather than hard-coded, so they cannot drift again. |

Two further drifts surfaced while fixing A9:

- `AdvancementDef` still defaulted to the pre-v0.3 `facet_level_threshold: 6` /
  `major_advancement_threshold: 4`. Corrected, with a parametrised test pinning
  every default to `facets/base/facet.yaml`.
- `builder.js` carried **its own copy of the MM1 Threat Rating formula**, and it
  had already drifted — its durability table bucketed Resolve (`<=4 → 2`,
  `<=6 → 3`, …) where the engine simply uses Resolve, so an 8-Resolve Boss
  previewed at 10 and saved at 14. The JS formula is deleted; `POST
  /api/enemies/preview-tr` scores unsaved stat lines, and `tr` now ships with
  every enemy payload (it is derived, so `model_dump()` had been dropping it and
  the library rendered "TR ?").

### B — Missing UI

**The MM Combat Console** (B1, B2, C3) is the centrepiece: a roster of every
character with Endurance, Posture, Sparks, armour charges remaining, and their
Conditions as removable chips. Landing an enemy attack is picking the incoming
Condition and pressing **Land Hit**; a checkbox reports a partial Dodge/Parry so
the engine — not the MM's arithmetic — applies the single greater reduction.

Also added: Reveal Postures (B3), Saving Throw panel (B4), Contested Roll (B5),
session reset (B6), a real Act Break that sends `act_break` (B7), player-side
Graceful Failure claim (B8), the **encounter library with Run** which spawns a
whole recipe into the tracker (B9, B12), `.fof` import (B10), MM per-character
notes (B11), enemy editing (B13), spawn count (B14), −2/−1/+1 Resolve and
removable enemy Conditions (B15), clock segment count and deletion (B16), Sparks
visible on every roster (B17), session (B19) and character (B21) deletion,
a session picker for invites (B20), party sheets for players (B22), a connection
indicator (B23), and copy-to-clipboard invites (B24).

New server endpoints and events, each test-first:
`clock_delete`, `character_created` / `character_removed` broadcasts,
`DELETE /api/sessions/{id}`, `DELETE /api/characters/{session}/{player}`,
`POST /api/enemies/preview-tr`.

`character_created` closed a bug the audit had not predicted: character creation
is a REST call that broadcast nothing, so an MM sitting in the session watched an
empty roster while players built characters in front of them.

### C — UX

Toasts with keyed de-duplication and inline actions replace `alert()`/`prompt()`
and silent chat-log errors; every player-addressing control is a picker; the
combat panel stays readable out of combat as a readiness view; an exchange-phase
banner says what the table is waiting for; a Help drawer maps every task to where
it lives; empty states explain what to do next; async buttons disable while
pending; focus rings, `aria-expanded`, and `prefers-reduced-motion` are handled.

Two presentation bugs found only by looking at the rendered page:

- The blanket `input { width: 100% }` rule caught radios and checkboxes, so the
  Posture, Scope, and Spark-use controls were scattered across their rows with
  labels floating away from them.
- The MM was shown the *player's* character sheet — an empty Attributes grid, a
  dead Roll Dice form, an empty Skills table — down the whole main column. The MM
  now gets that column for the combat console and enemy tracker, which never fit
  usably in the 340px rail.

### Regression cover

`software/tests/e2e/test_ui_flows.py` drives the real app in Chromium and
asserts that a player's or MM's action changes what they see. It skips cleanly
unless Playwright is installed (`pip install playwright && playwright install
chromium`). The Python suite could not have caught any finding in class A or B:
every one of them was a control that existed, looked enabled, and was wired to
nothing.
