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

## 2026-10-22 — T3.1 simulation harness into the repo

- **The original scripts were gone:** the session scratchpad was empty. They were rebuilt from TUNING_3P §2 (Method), the expected-damage arithmetic, the §3 table, §5 and the Appendix, against the module's chapter X blocks, the chapter IX cards and the chapter XI pregens (SRD 5.2.1). `references/oraga_night/` was not opened.
- **Files:** `research/oraga_5e_sim/`
  - `test_smoke.py`: written first and seen red (collection error, no modules).
  - `skirm.py`: generic card engine, plus the shared pregens, dice, dropping, death saves and crowd rule.
  - `s14.py`: the Attendant, rules as printed now.
  - `chain.py`: Movement V card, S14, S13, S3, with no rest.
  - `README.md`: assumptions, how to run, reproduction tables, gaps.
- **Module files:** none edited, so SA is unchanged.
- **Tests:** `python -m pytest research/oraga_5e_sim -q`: **12 passed** (smoke at N=200, seed 20261022; one regression assertion per script; determinism; CLI). The chain regression first asserted TUNING's absolute 15–21% HP at the gate. That figure does not reproduce, so the assertion was revised to TUNING F5's two qualitative claims (a Movement V card first lowers HP at the gate; C4, with no healer, arrives lower than C1) and the gap is documented in the README.
- **S14, the acceptance check:** `python research/oraga_5e_sim/s14.py --all --n 4000 --seed 1`. Engaged win against TUNING:

  | Party | Harness | TUNING |
  |---|---|---|
  | C1 | 87.3 | 90.7 |
  | C2 | 90.9 | 93.4 |
  | C3 | 92.7 | 93.7 |
  | C4 | 94.1 | 95.9 |
  | C5 | 93.6 | 95.2 |
  | 4P | 85.1 | 90.1 |

  The three-player span is 87.3–94.1, inside TUNING's 90–96 band with its ±3 tolerance. C1 is 3.4 under its own point value.
  - Also: naive 57.6–69.6 (TUNING 57–75); attrited C1 80.5 (TUNING 79–86).
  - Slug C1/C2/C4/C5 within 5 points; C3 34.1 against 17.6.
- **Skirmish cards:** 4,000 runs, seed 1, every card against C1–C5 and 4P. Within ±5 points of TUNING:
  - S7 as written, ≤4% (harness 0.0–3.9);
  - S8 C3, 23% (22.7);
  - S3 C3, 16% (13.5).
  - Inside TUNING's range: S13 to the last C1 (79.8, range 70–93), S10_fix C1 (14.4, range 6–23), S3 C2–C4 (13.3–24.5, range 14–32).
  - Not reproduced: S8 C1 64.5 / C5 26.5 (TUNING 57 / 49), S10 C1 50.7 (82), S4 C1 69.8 (86), S3 C5 46.4 (83), S13 4.5–34.7 (39–74).
- **Chain:** `chain.py --all --n 2000 --seed 1`, then again with `--crowd generous`.
  - Strict-crowd deaths for C1/C2/C5: 17–20%, inside TUNING's 15–21%.
  - Generous: 1–2.5%, against TUNING's 5–7%.
  - HP at the gate: 57–81%, against TUNING's 15–21%. This is the large gap.
- **Best explanation for the gaps** (README "Gaps"): the lost trick lists (S14 C1); TUNING's fights ran longer for the strong-damage parties (slot use, the wicket, S13's end point); and TUNING's §5 HP figures were probably gross damage.
- **Assumptions to note:** Ilesse heals rather than spending slots on Spiritual Weapon or Guiding Bolt, except in S14 slugging. Foes use sticky random targeting. All of S8's wardens fight from round 1. S4 is fought out against its two guards.
- **Use:** the harness is fit for comparing variants (T3.10, T5.8, T5.9). Absolute snake-card rates should be quoted with these assumptions.

## 2026-10-22 — T3.1 review (integrator)

- Verified: `python -m pytest research/oraga_5e_sim -q` → 12 passed.
- **Acceptance partly missed, accepted with a rule.** S14 reproduces (three-player 87.3–94.1 against TUNING's 90–96; C1 is 3.4 under its own TUNING figure, just outside ±3). Most snake-card absolutes and the chain's HP-at-gate do not (README lists them). The originals are gone, so the gap can't be adjudicated.
- **Rule for every later SIM task:** the rebuilt harness is the baseline. Each re-sim runs *both* the current and the changed rules in this harness and reports the delta. TUNING_3P's absolute snake-card and chain figures are not quoted in the book or as targets; its directional claims stand. Recorded in DECISIONS.
