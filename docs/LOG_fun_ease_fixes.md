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

### T1.1 — III.3 Named-NPC bullet (K-1) (2026-08-08)

- **Files:** `player_handbook/III.3_Combat.md`, `player_handbook/Index.md`
  (regenerated), `software/tests/test_docs_consistency.py` (register).
- **Did:** §Named NPCs — "Resolve, Posture, reactions, the works" → "Resolve,
  Posture, Techniques"; the "primary attribute and skill … Strikes and Parries"
  bullet rewritten as "**An attack modifier** — an authoring input … The NPC
  never rolls it: when it attacks, the PCs roll reactions (see *Enemy
  Attacks*)"; the veteran-soldier example line restated as "Attack +3
  (Strength +2, Combat Practiced +1)" instead of a rollable attribute+skill
  pair. Read the whole §Facing Mooks and Named Antagonists section — no other
  enemy-rolls implication found (§Enemy Attacks already states NPCs never
  roll). Register: `reactions, the works`; `they use for Strikes and Parries`.
- **Commands:** `grep -n "Parr" player_handbook/III.3_Combat.md` → all
  remaining hits are PC-side reaction rules, MM notes, vignette lines, and the
  reaction table. `python -m tools.build_index` (Index lost the Named-NPCs
  anchor under two index terms whose wording the bullet no longer carries —
  legitimate regen). `pytest tests/test_docs_consistency.py -q` → 32 passed.
  Full suite → 1394 passed.
- **Unexpected:** none.

### T1.2 — MM1 stale Parry + Defense-line claim (K-1, K-11 prep) (2026-08-08)

- **Files:** `mm_manual/MM1_Encounters_and_Enemies.md`, `player_handbook/Index.md`
  (regenerated), `software/tests/test_docs_consistency.py` (register).
- **Did:** `.fof` example — `# same roll for Parry` → `# authoring input — NPCs
  don't roll (Chapter III.3)`. Minimal stat block Defense line — dropped the
  false "feeds the TR formula and" claim (field removal itself is T3.7).
  Sweep hits fixed in the same pass: `Attack: [roll modifier]` and
  `Defense: [roll modifier]` → `[modifier]` (template); "the enemy's attack
  roll modifier" (§Calculating TR) and "best offensive roll modifier" (§Named
  NPCs build list) rewritten as authoring-input phrasing. Line 229's Defense
  bullet already reads no-roll and keeps its (true) difficulty claim until
  T3.7. Register: `same roll for Parry`; `feeds the TR formula`.
- **Commands:** `grep -rn "same roll for Parry|feeds the TR formula|roll
  modifier" mm_manual/` → empty. `python -m tools.build_index` (index terms
  shifted with the reworded lines). `pytest tests/test_docs_consistency.py -q`
  → 32 passed. Full suite → 1395 passed.
- **Unexpected:** Index regeneration needed for an MM1-only wording change —
  the index harvests both books, worth remembering for later WS-1 tasks.

### T1.3 — Enemy `.fof` conduct text contradicting no-roll (K-1 sweep) (2026-08-08)

- **Files:** `enemies/veteran_soldier.fof`, `enemies/city_watch_sergeant.fof`,
  `enemies/chicken.fof`, `software/tests/test_docs_consistency.py` (register).
- **Did:** veteran_soldier `tactics:` — "Reaction preference: Parry over Dodge
  (higher modifier). Will Absorb Tier 1 attacks if Endurance is low…" (both
  mechanically null: enemies have no reactions, Endurance, or Absorb) →
  no-roll authoring guidance keeping the meets-force-with-the-blade flavor:
  "Defends by meeting force with the blade, not by giving ground — while set
  (Measured or Defensive), lean toward Hard difficulty for Strikes against
  them (Chapter III.3)." `# Parry: same roll` comments (veteran_soldier,
  city_watch_sergeant) → `# authoring input — NPCs don't roll (Chapter
  III.3)`. chicken `# Dodges erratically` comment → `# Erratic movement` (its
  notes already deny dodging and stay). Register: `Parry: same roll`;
  `Reaction preference: Parry over Dodge`; `Dodges erratically`.
- **Commands:** `grep -ln "Parry\|Dodge\|reaction" enemies/*.fof` → no files.
  `python -m tools.build_bestiary --check` → up to date (tactics/comments are
  not rendered into stat blocks, so no regen diff). Docs suite → 32 passed.
  Full suite → 1395 passed.
- **Unexpected:** veteran_soldier's attack comment said "Combat Expert +1" —
  a mislabel (Expert is +2; the +3 total is Strength +2 + Practiced +1, which
  is what PHB III.3's example states). Corrected to "Combat Practiced +1" in
  the same pass; `attack_modifier: 3` and TR unchanged.

---

## Escalations

(none)
