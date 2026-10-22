# LOG: Oraga Night 5e, three-player pass

*Scope: `conversions/dnd5e/oraga_night/` (5e edition), plus lore/canon propagation to
`adventures/oraga_night/` (Facets edition). Tasks: `docs/TASKS_oraga_5e_3p_pass.md`. Design:
`docs/DESIGN_oraga_5e_3p_pass.md`. Findings: `docs/LEDGER_oraga_5e_3p.md`. Rulings: `docs/DECISIONS.md`
TP1–TP26.*

## 2026-10-21: TASKS file written (Planner)

- `docs/TASKS_oraga_5e_3p_pass.md` written: 129 tasks across WP1–WP11, which cover all 111 ledger
  rows (or list them as needing no task).
- 10 tasks are blocked:
  - owner wording or ruling: T7.8, T7.13, T7.14, T8.4, T11.11;
  - confirm items: C1 (T4.11, T7.4, T7.21) and C2 (T6.12);
  - escalation E1 (T7.6).
- **Open questions for the owner:**
  - **C1:** only the east-stair double doors seal at midnight. C1b: do the inner doors still
    lock behind Veier?
  - **C2:** is the S4 roster cut withdrawn?
  - **C3:** TP13's table numbers read as V–4/V–5.
  - **E1:** TP13 versus the owner-ruled *Dinner for Two*.
- **Baseline checks before any edit**, all green:
  - from `conversions/dnd5e/oraga_night/`: lint 0, fact_check 0, bestiary_check 0 mismatches,
    pregen_check 0 issues, `pytest tools` 422 passed;
  - from `software/`: `test_docs_consistency.py` 37 passed.
- **Note:** the simulation harness is still only in a session scratchpad. T3.1 moves it into
  `research/oraga_5e_sim/`.
- No module file was edited.

## 2026-10-21 — WP1 tells on the run path (T1.1–T1.3)

- **T1.1** (`08_Handouts.md`): the tells went in as a "Tells to show" block under Table VIII–1's checkpoints, by Movement (III, IV, V, midnight), not as a seventh column: the table already has six wide columns and a seventh would not print. Every Table V–6 tell appears under the Movement where chapter IV stages it; none invented. The L-096 note (the Movement V glint repeats the crystal-and-light habit) went into 04's "The quiet guest" paragraph, which now names all three habits by sighting.
- **T1.2** (`04_The_Ball.md`): a *Tells to show* sentence in each of the Movement III, IV and V time boxes, matching the sheet block; Movement III adds the target "each of the three should have shown at least one tell to someone at the table".
- **T1.3** (`01_Overture.md`): prep step 4 now names "The Fractures" and points to the sheet's tells block. Kept the current term "Fractures"; WP4 renames to Slow / Stop / End.
- **Checks** (from `conversions/dnd5e/oraga_night/`): `lint_5e.py --check` OK 0; `fact_check.py --check` OK 0; `pytest tools -q` 422 passed. No Facets edit (5e usability only).
- **T1.4** not run: the owner has not asked for commits yet.
- **Also:** TP13's table refs corrected in DESIGN §6 and DECISIONS (Table V–4 tricks 1 and 5, Table V–5 trick 3; TASKS C3 was right).

## 2026-10-22 — owner answers to TASKS C1, C2, E1

- TP27 cut Dinner for Two (E1 option C); TP28 only the east-stair double doors seal at the lights, inner doors still lock behind Veier on Raunu's charge; TP29 S4 cut withdrawn. T4.11, T6.12, T7.4, T7.6, T7.21 unblocked. Owner: commit per package on feat/lean-facets, no push.
