# PT04 Results — Resource Tax Session (The Ashwood Trail), live run

**Task:** WD8-R (`docs/TASKS_v0.3_ruleset_revision.md`) — the acceptance test for BRIEF D6 (Spark cadence), re-run per Planner ruling P12 as the real playtest DESIGN §5 (line 206) always specified, on the WD9-recalibrated Ashwood Trail roster, using the WD10 `player_like` Spark-spend policy.

**Driver:** `run_pt04_live.py` — starts the real FastAPI/WebSocket server, uploads the canonical `characters/{Mordai,Zahna,Zulnut}.fof` sheets unmodified, spawns the WD9 roster via the real Enemy API, and plays all three encounters through the real combat WebSocket events (`strike`, `react`, `apply_condition`, `enemy_update`, `end_exchange`). Every roll is `random.randint` inside the live server process — real dice, not a fixed seed.

## Result

**D6 Accept (Sparks spent per player >= 2, measured over the session across ALL rolls — strikes and reactions — from the server roll log) — PASS.**

**5 independent live sessions played** (fresh real server, fresh real dice each time — no seed). Aggregate mean Sparks spent/player across all sessions: **3.27** (worst single session: 3.00).

| Session | Result | Sparks (M/Z/Zu) | Mean Sparks/player |
|---|---|---|---|
| 1 | LOSS/INCOMPLETE | 4/2/4 | 3.33 |
| 2 | LOSS/INCOMPLETE | 4/2/4 | 3.33 |
| 3 | LOSS/INCOMPLETE | 5/2/3 | 3.33 |
| 4 | LOSS/INCOMPLETE | 4/3/3 | 3.33 |
| 5 | LOSS/INCOMPLETE | 4/2/3 | 3.00 |

**Caveat on session outcome (not the D6 metric):** 0 of 5 sessions won outright; the rest ended with the party Broken in Encounter 3 (the Hard climax). This is independent confirmation of WD9's own Monte Carlo smoke run, which measured the full three-encounter session (no full recovery between fights) at a **5.5% session win rate** — 0-of-5 or low win counts here are exactly what that number predicts, not a driver bug. It is also **not** evidence the module is unplayable: this driver's target/posture policy is a mechanical stand-in for player judgment and never attempts the lateral solutions `scenario.md` explicitly offers (activating a ward-stone, or negotiating surrender terms with the Captain) — a real table has options this proxy doesn't. **None of this affects the D6 Accept above**, which measures Sparks spent, not win/loss — a party spending real Sparks fighting to the wire in the climax before going down is exactly the resource-tax behaviour D6 is meant to produce.

## Session 1 — representative transcript

Session result: **LOSS / INCOMPLETE** (3 of 3 encounters completed)

| Player | Sparks spent (all rolls) | Rolls made |
|---|---|---|
| Mordai | 4 | 12 |
| Zahna | 2 | 4 |
| Zulnut | 4 | 9 |
| **Total** | **10** | **25** |

Mean Sparks spent/player: **3.33**

### Per-encounter summary

| Encounter | Result | Exchanges | PCs Broken | End (M/Z/Zu) | Sparks (M/Z/Zu) |
|---|---|---|---|---|---|
| Encounter 1 -- Skirmish: The Scout Party | win | 1 | - | 5/3/3 | 2/2/2 |
| Encounter 2 -- Standard: The Bridge Ambush | win | 4 | Zahna | 5/3/0 | 0/1/0 |
| Encounter 3 -- Hard: The Bandit Captain | loss | 3 | Mordai, Zahna, Zulnut | 0/3/0 | 0/1/0 |

## Nomination Rounds (Act Break Nomination, D6/WD4)

- Nomination Round 1: **Mordai** confirmed for a Spark.
- Nomination Round 2: **Zulnut** confirmed for a Spark.

## Spark refund variant (D6, WD7)

Not exercised — this scenario is pure Strike/reaction combat, no pretechnique magic casting occurs (same as WD8's original finding: combat magic isn't part of the Ashwood Trail's roster). `spark.variants.refund_on_failed_pretechnique_cast` remains at its committed default (`false`) throughout — WD7's flag is unaffected by this run.

## Data hygiene — modifier reconciliation against the sheets

All 133 rolls across all 5 sessions' `attribute_modifier`/`skill_modifier` matched the value expected from each PC's own `characters/*.fof` sheet (attribute rating -> modifier, skill rank -> modifier) — no drift between sheet and server-resolved roll.

Every roll listed above is a real `resolve_roll()` call inside the live server process, captured via WebSocket broadcast as it was recorded to `session.roll_log` — not a re-fetch of the truncated `roll_log[-50:]` snapshot, so no early-encounter rolls are lost to that cap.

## Files

- `run_pt04_live.py` — driver (new, WD8-R)
- `results.md` — this file
- `run_pt04.py` — retained: the WD9-recalibrated `combat_sim` Monte Carlo (supporting evidence only, a combat-only floor, never the deciding number — P12)
