# LOG — Fun & Ease-of-Play Fixes

**Upstream:** `docs/DESIGN_fun_ease_fixes.md`, `docs/TASKS_fun_ease_fixes.md`.
Worker execution log. One entry per task: files touched, commands run, results,
anything unexpected.

## Workstreams and branches (DESIGN §1)

| WS | Scope | Branch (per DESIGN) |
|---|---|---|
| WS-1 | Text integrity (no mechanic changes; kills drift) | `fix/text-integrity` |
| WS-2 | Rules unification (Sparks, difficulty precedence, clocks) | `feat/rules-unification` |
| WS-3 | Combat mechanics (rider merge, Withdrawn, enemy texture) + sim campaign | `feat/combat-open-and-tempo` |
| WS-4 | Magic & advancement (casting skill, ladders, points economy) + sim spot-checks | `feat/magic-advancement-arcs` |
| WS-5 | Apparatus & polish (Quick Start, MM5, sheets, terminology) | `feat/apparatus-polish` |
| WS-6 | App features (band display, Spark nudge, posture panel) | `feat/app-fun-ease` |

> **Deviation from DESIGN §1 (recorded at branch creation, 2026-08-08):** the
> orchestrator consolidated the one-branch-per-workstream plan into a SINGLE
> integration branch, `feat/fun-ease-fixes`, with one commit per task, for
> autonomous execution. The WS/branch table above is kept as the design record;
> no per-WS branches will be created.

## Baseline

- 2026-08-08 — `feat/fun-ease-fixes` created off `main` (e1271ad). Six pipeline
  docs committed first (`Add fun/ease-of-play review, design, and tasks`).
- Baseline full suite: `cd software && python -m pytest tests/ -q` →
  **1394 passed** in 341s. Green.

---

## Task entries

### T0.1 — Retired-phrase invariant scaffold (2026-08-08)

- **Files:** `software/tests/test_docs_consistency.py`.
- **Did:** added `RETIRED_PHRASES: list[tuple[str, str]]` (seeded empty) and
  `test_retired_phrases_do_not_reappear`, scanning `player_handbook/ mm_manual/
  bestiary/ facets/ software/facets/ enemies/ characters/ spec/` line-by-line
  for every registered phrase. Historical archives (`playtest/`, `docs/`,
  `research/simulation_log.md`, `research/advancement_priority_questions.md`)
  are excluded by scope — they are not in the scanned paths.
- **Commands:** dummy phrase `("Mirror Master", "DUMMY-RED-CHECK")` inserted →
  `pytest tests/test_docs_consistency.py::test_retired_phrases_do_not_reappear`
  **red** (offenders across the books, as intended). Dummy removed →
  `pytest tests/test_docs_consistency.py -q` → **32 passed**.
- **Notes:** a top-level `facets/` directory does not currently exist in the
  repo (only `software/facets/`); the scanner skips missing roots, so the path
  stays listed for future-proofing.

### T0.2 — Create this LOG (2026-08-08)

- **Files:** `docs/LOG_fun_ease_fixes.md` (this file).
- **Did:** WS/branch table from DESIGN §1, branch-consolidation deviation note,
  baseline record (1394 passed), empty escalation section.

---

## Escalations

(none)
