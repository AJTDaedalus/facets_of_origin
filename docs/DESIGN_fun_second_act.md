# DESIGN — The Second Act: Open That Expires, and a Strike That Chooses

**Date:** 2026-09-08 · **Tier:** Planner · **Brief:** `docs/BRIEF_fun_second_act.md`
**Tasks:** `docs/TASKS_fun_second_act.md` · **Log:** `docs/LOG_fun_second_act.md`
**Branch:** `feat/fun-second-act` off `main`
**Baseline at planning time:** 1579 tests collected, `open_clears: enemy_action` (facet.yaml:1781).

---

## 0. Where this sits in the program

Four briefs landed together. Their dependency order is fixed by `BRIEF_oraga_starter_module.md` §10 and ruling S1:

```
Track 1:  feat/lineage ──────────────► feat/valloh-facet ─┐
Track 2:  feat/fun-second-act ────────────────────────────┴──► feat/oraga-rewrite
```

This workstream is Track 2. It is independent of Lineage and Val'loh and may run in parallel with them.
It **must** be settled — adopted or rejected on the numbers — before `oraga_rewrite` §11 tunes S2 and S3,
because those scene cards are tuned against whichever rules result comes out of here. Tune once.

## 1. Approach

Two rules changes, each a gate. Each is implemented behind the data it already has a home for, simmed
against the Series-10 harness, and adopted or rejected on the published acceptance numbers before the
next one is built on top of it. Nothing reaches the books until both gates have returned a verdict.

The sequence is deliberate: R2 changes the *lifetime* of an existing tag; R3 adds *siblings* to that tag.
Building R3 first would measure riders against a snowball R2 is meant to remove, and the numbers would
not separate the two effects. So: baseline → R2 → verdict → R3 on top of the adopted R2 state → verdict
→ book sync in one commit → DECISIONS D20.

## 2. Module breakdown

### M1 — Baseline (no production code)

Re-run Series 10's method under today's data and record it as Series 12 Part A in
`research/simulation_log.md`. This is the regression floor: every later run is read against it, and the
engine's behaviour under `open_clears: enemy_action` must reproduce these numbers after M2 ships (the
mode is kept as a legal value precisely so this guard survives).

Harness, fixed for the whole workstream: `tools/combat_sim.py::run_simulation`, n=200, seeds 1/2/3/7/42,
default AI, PS-3 `standard_party()` (combat_sim.py:1021).

### M2 — R2: Open clears at end of exchange

**Data.** `combat.enemy_durability.open_clears` (facet.yaml:1781) gains `end_of_exchange` as a legal
value and the base ruleset takes it. `enemy_action` stays legal so a setting can choose it and so M1's
regression guard has something to run against. The schema field is already a string; it becomes a
`Literal["enemy_action", "end_of_exchange"]` so an unknown value fails at load, not at the table.

**Engine.** `combat.py` already publishes the mode through `open_clear_mode(ruleset)` (combat.py:670)
and documents that callers gate on it rather than hardcoding the lifecycle — that contract is what makes
this a small change. Two additions:

- `open_clears_at_end_of_exchange(ruleset) -> bool` — the one-line predicate every caller asks for.
- `expire_end_of_exchange(state, ruleset) -> list[str]` — the tag-expiry sibling of `end_exchange`.
  `end_exchange(conditions, ruleset)` (combat.py:918) takes a bare condition list and is called from
  several places; its signature is not changed. The new function takes the enemy/ally tag state, expires
  Open when the mode says so, and (after M3) expires the riders. It returns the tag names it cleared so
  the WS layer can narrate them.

**Consumers.** `websocket.py:1778` (the `open` flag on the enemy-update path) and the simulator's
`_should_clear_open` policy (combat_sim.py:444) read the mode instead of assuming the enemy-action
spend. Under `end_of_exchange` the enemy's action is no longer consumed by clearing Open, which is the
whole point: an Open enemy still acts.

**Fallout.** The Archive Guardian's Reduced Mode carries `special_no_clear_open`, which is meaningless
under the new mode. Re-authored in M5 to one of MM1's four legal phase levers — *raise its danger*.

**Gate G-R2 (adopt/reject).** From the brief §2, unchanged:
- Solo Archive Guardian median **3** exchanges (was 2), mean ≤ 4.5, win rate ~100%, Sparks spent ≥ 5/9,
  Endurance visibly drawn down.
- Recipe Table rows at PS-3 hold within ±5 pp: Standard 65–85%, Hard 40–60%, Deadly 15–35%.
- Guardian phase (Resolve ≤ 2) fires *before* the final exchange in ≥ 60% of runs.
- **Reject if** a row leaves its band after a one-point Resolve retune, or the Guardian median > 5.
  Fallback: keep persistent Open, move phase thresholds to half Resolve.

### M3 — R3: a 10+ Strike chooses one rider

**Data.** `combat.enemy_durability.strike_riders`, a list of `{id, label, effect, duration}` so the app
renders the confirm from data and a setting can add or remove one:

```yaml
strike_riders:
  - id: open
    label: Open
    effect: easy_tag
    duration: end_of_exchange
  - id: position
    label: Position
    effect: easy_tag_next_roll
    duration: next_roll_or_end_of_next_exchange
  - id: cover
    label: Cover
    effect: free_reaction_ally
    duration: end_of_exchange
```

**Schema.** `StrikeRiderDef` in `app/facets/schema.py` with the docstring discipline
`BackgroundDefinition` sets. Validator: `id` must be one of the effects the engine implements — an
unknown rider id is rejected at load. This is the brief's data test made structural.

**Engine.** `combat.py` gains `apply_rider(rider_id, *, target, attacker, ally=None, exchange_no,
ruleset)`. No new model fields on Character or the enemy beyond tag state:

| Rider | State written | Expiry |
|---|---|---|
| Open | `enemy.open = True` | end of this exchange (M2's rule) |
| Position | `enemy.position = {uses: 1, expires_after_exchange: n+1}` | first roll against the target, else end of the next exchange |
| Cover | `ally.free_reaction = True` (one-shot) | consumed by one reaction, else end of this exchange |

Precedence is not re-implemented here. Open and Position are both Easy-tag sources, and
`target_strike_difficulty` (combat.py:681) already composes through `compose_difficulty` with
`easy_tag=`; it takes `easy_tag = enemy.open or enemy.has_position()`. III.1's precedence rule makes
Easy absolute and non-stacking, and this design must not carry a second copy of it.

Cover is a *free reaction*, not a free success: the reaction roll still happens, the Endurance cost does
not. Against a Mook a 10+ removes it and no rider applies. PvP is untouched.

**App.** `websocket.py`'s existing 10+ Open confirm becomes a `rider` field (the sibling path to
`final_blow_confirm`); relay events carry `rider` and `open_until`. Rule logic stays in `combat.py` —
the handler validates through the engine, per the standing iron law.

**Simulator.** Two selectable rider policies:
- `mixed` — `open` if the target is not Open; else `cover` on the lowest-Endurance ally if an attack is
  incoming; else `position`.
- `always_open` — worst case, so the snowball is still measured at full strength.
Plus decision-count instrumentation: log rider choices per exchange so the DESIGN can report
*decisions per exchange* as a number rather than a claim.

**Gate G-R3 (adopt/reject/trim).**
- Bands hold as in G-R2.
- Under `mixed`, mean PCs-Broken in the Hard row rises no more than 0.1 over `always_open` and falls no
  more than 0.15 below it. (Cover must not make the party unbreakable; Cover must matter.)
- **Reject Cover if** it breaks Hard/Deadly by more than the band tolerance after one Resolve retune.
  Then ship two riders (Open, Position) and note Cover as a future Technique.

### M4 — Book sync (one commit with M2/M3's data and engine)

Per the brief §4, and the iron law that a rules change touches body text, every quick ref, `facet.yaml`,
and the engine together:

III.3 *Strike* (enemy paragraph + Table III.3-3), *Maneuver* (one sentence), *Reactions* (Cover under
Intercept), Quick Reference Table III.3-12, exchange-flow step 5 · III.1 *The Natural 12* example ·
MM1 *Enemy Stat Blocks* anti-snowball paragraph, rewritten · MM5 Strike Outcomes and Reactions rows ·
Quick Start combat primer line 3 · II.4a *Overwhelming Force* and *The Final Blow* Normal lines ·
Glossary: Open (duration), Rider, Cover, Position · INV-9/10/14 regenerate.

### M5 — R7: show it

Rewrite *In Play: The Archive's Guardian* (III.3) so the Boss changes stance once on a stated conduct
trigger, acts while Open, and lands one telegraphed Technique; at least one 7–9 and one 6− per the style
guide's example-of-play rule. Re-author Reduced Mode to *raise its danger*. Update
`enemies/archive_guardian.fof`, `combat_sim.py::archive_guardian_def` (combat_sim.py:1227), the
generated Bestiary marker, and the TR.

Then sweep `bought_captain`, `glassback_bull`, `the_unfinished` for phases or Techniques that assume
persistent Open, and re-author any that do. `bought_captain` matters twice: it is the gate fight's Boss
in `oraga_rewrite`, so its numbers must be settled here before that module tunes S3.

## 3. Testing strategy

TDD throughout; three tests per public function minimum.

| Layer | What proves it |
|---|---|
| Data | `open_clears` accepts both values and rejects a third; `strike_riders` loads; unknown rider id rejected |
| Engine | Open set on a 10+ clears at end of exchange under the new mode and does not under `enemy_action`; each rider applies once and expires as specified; Open + Position do not stack; Cover frees exactly one reaction and only for the named ally; Mooks take no rider; PvP row unchanged |
| Simulator | Rider policies selectable; the Series-10 harness reproduces Part A's numbers under `enemy_action` before any new number is recorded |
| App | The strike confirm offers riders from data; relay events carry `rider` and `open_until` |
| Docs | INV-9/10/14 green; the Guardian vignette's arithmetic reconciles with its printed modifiers (extend the existing PHB worked-arithmetic test) |

## 4. Risks and mitigations

- **Fixing length with Resolve.** The audit's do-not list and Series 7 both showed it buys exchanges, not
  tension. Retune by at most one point, and only to hold a recipe band.
- **A fourth rider.** Three is the cap. A fourth option on the most common outcome is where PbtA
  pick-lists stop being fast; the schema permits more so a setting can, and the base ruleset must not.
- **Cover.** Intercept for free. G-R3's PCs-Broken gate exists to catch it.
- **Enemy stances now matter more,** because an Open enemy acts. Every Named/Boss in the core examples
  needs a `triggers:` line before the vignette is rewritten (audit R7) — this is a task, not an
  assumption.
- **Double-tuning the module.** If this workstream slips, `oraga_rewrite` waits. It does not tune against
  provisional numbers.

## 5. Open questions

None blocking. Both gates are numeric and both have a written fallback, so this workstream can complete
without escalation. If both R2 and R3 reject, that is a result: record it in D20 and hand
`oraga_rewrite` the unchanged rules.
