# TASKS — The Second Act

**Design:** `docs/DESIGN_fun_second_act.md` · **Brief:** `docs/BRIEF_fun_second_act.md`
**Log:** `docs/LOG_fun_second_act.md` · **Branch:** `feat/fun-second-act` off `main`
**Baseline:** 1579 tests collected, all green, before task 1.

Workers: one task at a time. Read the DESIGN and this file; do not rely on chat history. Mark the task
done or blocked here and append to the LOG before stopping.

Legend: **[G]** = a gate task; its verdict decides whether the following tasks run as written.

---

## M1 — Baseline

**T1. Series 12 Part A: regression floor.** — 20 min
Files: `research/simulation_log.md`.
Run `tools/combat_sim.py::run_simulation`, n=200, seeds 1/2/3/7/42, default AI, PS-3
`standard_party()`, under today's data (`open_clears: enemy_action`). Record: solo Archive Guardian
median/mean exchanges, win rate, Sparks spent, Endurance drawn down; every Recipe Table row at PS-3;
Guardian phase-fire exchange distribution.
Accept: a Series 12 Part A section exists carrying every number G-R2 and G-R3 are read against, with the
exact command line recorded so it can be re-run verbatim.

## M2 — R2: Open clears at end of exchange

**T2. Data: `open_clears` becomes a closed set.** — 20 min
Files: `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`.
Tests first: `enemy_action` loads; `end_of_exchange` loads; a third value is rejected at load.
Change the field to `Literal["enemy_action", "end_of_exchange"]`. Do **not** change the base value yet.
Accept: 3 new tests green; full suite green; base ruleset still `enemy_action`.

**T3. Engine: the end-of-exchange expiry hook.** — 30 min
Files: `software/app/game/combat.py`, `software/tests/test_combat.py`.
Tests first. Add `open_clears_at_end_of_exchange(ruleset) -> bool` and
`expire_end_of_exchange(state, ruleset) -> list[str]`. Do not change `end_exchange`'s signature
(combat.py:918) — several callers depend on it.
Accept: Open clears under `end_of_exchange` and survives under `enemy_action`; the function returns the
tag names it cleared; ≥3 tests per new function.

**T4. Consumers read the mode.** — 30 min
Files: `software/app/api/websocket.py` (the `open` path, ~1778), `software/tools/combat_sim.py`
(`_should_clear_open`, :444), `software/tests/test_websocket.py`, `software/tests/test_combat_sim.py`.
Under `end_of_exchange` the enemy's action is **not** consumed by clearing Open.
Accept: no caller hardcodes the lifecycle; under `enemy_action` behaviour is byte-identical to T1's
baseline; tests cover both modes.

**T5. Flip the base ruleset.** — 10 min
Files: `software/facets/base/facet.yaml:1781` and its comment block.
Accept: `open_clears: end_of_exchange`; suite green; the comment says why and names D20.

**T6. [G] Series 12 Part B — gate G-R2.** — 45 min
Files: `research/simulation_log.md`, `docs/LOG_fun_second_act.md`.
Same harness as T1. Check every G-R2 threshold in DESIGN §2/M2.
Accept: a written verdict — **adopt**, **adopt after a one-point Resolve retune** (say which enemy), or
**reject**. On reject, stop and apply the brief's fallback (persistent Open, phase thresholds at half
Resolve) and re-plan T7–T13 with the Planner before continuing.

## M3 — R3: the rider menu

**T7. Data + schema: `strike_riders`.** — 40 min
Files: `software/app/facets/schema.py`, `software/facets/base/facet.yaml`,
`software/tests/test_facets_schema.py`.
Tests first. Add `StrikeRiderDef` (`id, label, effect, duration`) with a docstring in
`BackgroundDefinition`'s register, and `strike_riders` under `combat.enemy_durability` carrying the three
riders from DESIGN §2/M3. Validator rejects a rider id the engine does not implement.
Accept: loads; unknown id rejected; the three ids are exactly `open`, `position`, `cover`.

**T8. Engine: `apply_rider`.** — 60 min
Files: `software/app/game/combat.py`, `software/tests/test_combat.py`.
Tests first. Implement the state table in DESIGN §2/M3. Extend `expire_end_of_exchange` to expire
Position and Cover. `target_strike_difficulty` takes `easy_tag = enemy.open or enemy.has_position()` —
do **not** re-implement III.1 precedence; compose through `compose_difficulty`.
Accept: each rider applies exactly once and expires as specified; Open and Position do not stack; Cover
frees exactly one reaction, only for the named ally, and the roll still happens; a Mook 10+ takes no
rider; the PvP row is unchanged. ≥3 tests per new public function.

**T9. App: the three-way confirm.** — 40 min
Files: `software/app/api/websocket.py`, `software/app/static/js/play.js`,
`software/tests/test_websocket.py`.
The 10+ Open confirm becomes a `rider` field; the menu renders from data, not a hardcoded list; relay
events carry `rider` and `open_until`.
Accept: no rule logic in the handler; adding a fourth rider to the yaml would render without a JS change.

**T10. Simulator: rider policies and decision counting.** — 45 min
Files: `software/tools/combat_sim.py`, `software/tests/test_combat_sim.py`.
Add `mixed` and `always_open` policies (DESIGN §2/M3) and per-exchange rider-choice logging.
Accept: policy selectable from the run config; the log yields *decisions per exchange* as a number.

**T11. [G] Series 12 Part C — gate G-R3.** — 45 min
Files: `research/simulation_log.md`, `docs/LOG_fun_second_act.md`.
Run both policies on top of the adopted R2 state. Check G-R3's thresholds.
Accept: a written verdict — **adopt three riders**, **adopt two** (Open, Position; Cover deferred to a
future Technique), or **reject**. Report decisions per exchange.

## M4 — Book sync (one commit with the data and engine)

**T12. III.3 and the combat quick refs.** — 60 min
Files: `player_handbook/III.3_Combat.md` (Strike + Table III.3-3, Maneuver, Reactions, Table III.3-12,
exchange-flow step 5), `player_handbook/III.1_Core_Resolution.md` (The Natural 12 example).
Only the riders the gates adopted. A quick ref is a compression, never a new rule.
Accept: INV-9/10 regenerate to no diff; body text and quick ref say the same thing in different lengths.

**T13. MM1, MM5, Quick Start, II.4a, Glossary.** — 45 min
Files: `mm_manual/MM1_Encounters_and_Enemies.md` (the anti-snowball paragraph, rewritten: Open expires
on its own; the enemy's answers are stance, Technique, and target), `mm_manual/MM5_Quick_Reference.md`,
`player_handbook/Quick_Start.md` (combat primer line 3),
`player_handbook/II.4a_Character_Creation_Facet_Body.md` (*Overwhelming Force*, *The Final Blow* Normal
lines), `player_handbook/Glossary.md` (Open with its duration, Rider, Cover, Position).
Accept: INV-6/11/12/14 green; regenerate Index and registers.

## M5 — R7: show it

**T14. Enemy `triggers:` lines for the core examples.** — 30 min
Files: `enemies/*.fof` for every Named/Boss appearing in a PHB or MM example.
Accept: each has a stated conduct trigger; Bestiary markers regenerate; INV-15 green.

**T15. Re-author the Guardian's Reduced Mode.** — 40 min
Files: `enemies/archive_guardian.fof`, `software/tools/combat_sim.py::archive_guardian_def` (:1227),
`bestiary/B*.md` marker (generated), TR.
`special_no_clear_open` is meaningless under the new mode. Replace with *raise its danger*: blows land
Tier 2 again and it fixes on whoever Opened it.
Accept: the generated stat block regenerates to no diff; TR recomputed; sim def and `.fof` agree.

**T16. Rewrite *In Play: The Archive's Guardian*.** — 60 min
Files: `player_handbook/III.3_Combat.md`.
The Boss changes stance once on a stated trigger, acts while Open, lands one telegraphed Technique; the
party's exchange-two decision is damage vs. Cover for Mordai. At least one 7–9 and one 6−.
Accept: the worked-arithmetic test covers this vignette and passes; prose passes the humanizer and the
style guide's amateur-tells list.

**T17. Boss sweep.** — 30 min
Files: `enemies/bought_captain.fof`, `enemies/glassback_bull.fof`, `enemies/the_unfinished.fof`,
`bestiary/`.
Re-author any phase or Technique that assumes persistent Open. `bought_captain` is `oraga_rewrite`'s
gate Boss — settle it here.
Accept: no Boss in the Bestiary depends on a tag that now expires; markers regenerate.

## Close-out

**T18. D20 and the handoff.** — 30 min
Files: `docs/DECISIONS.md` (D20, with the numbers from Parts A/B/C and both verdicts),
`docs/LOG_fun_second_act.md`, `docs/BRIEF_oraga_rewrite.md` §11 (a line naming the adopted rules).
Accept: full suite green with a reported pass count (baseline 1579 + the new tests); D20 records what was
adopted, what was rejected, and the number that decided each; `oraga_rewrite` can read one file to know
what it tunes against.

---

## STATUS: COMPLETE (T1–T18) — 2026-09-09

Every task in this file is done. Full suite green.

**R2 adopted. R3 adopted with two riders; Cover cut at the gate.** Decision D20; evidence `research/simulation_log.md` Series 12 A/B/C.

Execution record, including what the numbers changed and what went wrong on the way: `docs/LOG_fun_second_act.md`.
