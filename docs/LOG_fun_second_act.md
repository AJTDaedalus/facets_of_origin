# LOG — The Second Act

**Design:** `docs/DESIGN_fun_second_act.md` · **Tasks:** `docs/TASKS_fun_second_act.md`
**Decision:** D20 · **Evidence:** `research/simulation_log.md` Series 12 A/B/C

---

## 2026-09-08 — T1 through T18, complete

Both gates returned verdicts. **R2 adopted. R3 adopted with two riders; Cover cut.**

### Task status

| Task | Status | Note |
|---|---|---|
| T1 baseline | ✅ | Series 12 Part A. Seeds 1/2/3 reproduce Series 10 to the decimal, which is what makes the floor usable. Needed new instrumentation first (`SimResult.phase_fires`, `EnemyState.phase_fired_exchange`) — additive, gate-only, never read by a decision branch. |
| T2 `open_clears` closed set | ✅ | `Literal["enemy_action","end_of_exchange"]`; 5 tests. |
| T3 engine hooks | ✅ | `open_clears_at_end_of_exchange`, `expire_end_of_exchange`. `end_exchange`'s signature untouched — it has several callers and takes a bare condition list, not enemy state. (The brief assumed otherwise.) |
| T4 consumers | ✅ | Sim and WS both route through the predicate. Added under `enemy_action` first, so the suite proved them no-ops before the flip. |
| T5 flip the base | ✅ | Cascaded into 7 pinned tests, by design. |
| T6 **[G]** gate G-R2 | ✅ | **Adopt, unretuned.** See below. |
| T7 `strike_riders` data+schema | ✅ | `StrikeRiderDef`; effects are a closed set. |
| T8 `apply_rider` | ✅ | Open/Position/Cover implemented; `has_easy_tag` is the single place Open-and-Position-don't-stack stays true. 17 tests. |
| T9 app | ✅ | `strike_rider` event; menu rendered from data; `notify` extended to multiple actions; expiry announced on `exchange_ended`. 9 WS tests. |
| T10 sim rider policies | ✅ | `always_open` (default, reproduces pre-R3 bit-identical) and `mixed`; per-exchange rider log. |
| T11 **[G]** gate G-R3 | ✅ | **Adopt two riders; cut Cover.** See below. |
| T12–T13 book sync | ✅ | III.3 (Strike, Table III.3-3, Maneuver, Table III.3-12, exchange flow), III.1 (natural 12, Easy-tag precedence), MM1 (anti-snowball paragraph rewritten), MM5, Quick Start, II.4a, Glossary (Open rewritten; Rider and Position added). |
| T14 enemy triggers | ✅ | Two "once left Open" stance triggers tightened to name the exchange; the Guardian gained a stance-change trigger. |
| T15 Reduced Mode | ✅ | Threshold 2 → 4, *raise its danger*. Phase now lands before the final exchange in 99–100% of runs (was 20–27%). |
| T16 vignette | ✅ | Rewritten. Also **wrote the worked-arithmetic test the brief assumed existed** — it did not. |
| T17 boss sweep | ✅ | Clean: no Boss phase or Technique assumed persistent Open. |
| T18 D20 + handoff | ✅ | D20 recorded with the numbers; `BRIEF_oraga_rewrite.md` §11 now names the settled rules. |

### The two decisions worth remembering

**The prescribed Resolve retune does not exist.** G-R2's acceptance said to repair a drifting recipe row by retuning Named/Boss Resolve by −1. Measured: at Resolve 2 a Named NPC dies to one full-success Strike, so it loses its second exchange entirely, and every row overshoots (Standard 88.5–97.0%, Hard 61.5–73.0%). MM1's Named band of 3–4 has no interior to tune within. Adopted unretuned; Hard sits at its floor (38.0–45.0% against 40–60%) rather than its middle.

**Cover's gate was blind, and Cover had to go anyway.** The acceptance measured Cover by mean PCs-Broken in the Hard row. In any multi-enemy encounter the party always has a target that is not yet Open, so the menu collapses to Open and no other rider ever fires — the metric could not move. Re-measured where the riders actually operate (solo Boss): Cover took the median from 3 back to 2 and phase-before-final from 51–58.5% to 19–23%, undoing R2 exactly. Not too strong; a length-shortener in defensive clothing. Cut, with `free_reaction_ally` left implemented for a setting or a future Technique.

### Corrections to the brief

1. `end_exchange(conditions, ruleset)` takes a condition list, not enemy state — R2 needed a sibling function, not an edit.
2. There is no existing worked-arithmetic test for PHB examples. Written as part of T16: outcome tiers vs. stated results across both books, the Guardian vignette showing all three outcome bands, and its Resolve countdown descending by exactly 2 to 0.
3. Cover's failure mode was not the one the brief anticipated (breaking the Hard/Deadly rows). It cannot break them; it breaks the Boss fight.

### T9's browser coverage, added late

Same gap as L14: the strike confirm was written and unit-tested over the socket, but
nothing drove it in a browser. **Five e2e tests** now do — a full success offering
the riders the ruleset prints, an empty menu offering no dead button, a third rider
rendering with no JS change (the promise the data-driven menu makes), the button
actually reaching the engine, and the log telling the table that Open expires at the
end of the exchange rather than letting them keep playing it as the permanent tag it
used to be.

### Files changed

Data/engine: `facets/base/facet.yaml`, `app/facets/schema.py`, `app/game/combat.py`, `app/game/enemy.py`, `app/game/character.py`, `app/api/websocket.py`, `app/static/js/{app,play}.js`, `tools/combat_sim.py`.
Books: `player_handbook/{III.3_Combat,III.1_Core_Resolution,Quick_Start,II.4a_…,Glossary}.md`, `mm_manual/{MM1,MM5}.md`, regenerated `Index.md`/`List_of_Tables.md`/`List_of_Boxes.md`/`bestiary/B3_The_Made.md`.
Enemies: `archive_guardian.fof`, `city_watch_sergeant.fof`, `veteran_soldier.fof`.
Records: `research/simulation_log.md` (Series 12 A/B/C), `docs/DECISIONS.md` (D20).

**Resolved. Return to Track 1 (`TASKS_lineage.md` L1) — `oraga_rewrite` is unblocked on this track.**
