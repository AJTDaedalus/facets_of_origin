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

### T1.4 — MM1 §Mooks "worn down" mechanism (K §4.3) (2026-08-08)

- **Files:** `mm_manual/MM1_Encounters_and_Enemies.md`, `player_handbook/Index.md`
  (regenerated), `software/tests/test_docs_consistency.py` (register).
- **Did:** replaced the false Endurance-attrition claim with the true mechanism:
  Absorb costs nothing; Mook Tier 1 chip (Winded −1 next roll, Off-Balance +1
  next reaction cost) degrades reactions against simultaneous Named Tier 2s.
  Register: `arrive at the Named NPC already worn down`. (Edit begun by the WS-1
  agent before its session ended; completed and verified by the orchestrator.)
- **Commands:** `grep -rn "worn down" mm_manual/ player_handbook/` → empty.
  Full suite → **1395 passed** (336s).

### T1.5 — Supersession header (P-15) (2026-08-08)

- **Files:** `research/advancement_priority_questions.md`.
- **Did:** top-of-file SUPERSEDED FIGURES note: item #5's 6/12 thresholds and
  4-point cross-Facet economy superseded by shipped II.4 (5/10/15, flat 2 points);
  pointer to II.4 and this pipeline.

### T1.6 — WS-1 sweep (2026-08-08)

- **Commands:** register invariant test → 1 passed. `grep -rn "Parr" mm_manual/
  enemies/ software/facets/` → 4 hits, all legitimate PC-side reaction text
  (MM5 reaction cards, armor-downgrade note, facet.yaml comment).
  `python -m tools.build_index` and `python -m tools.build_bestiary --check` →
  both idempotent ("Bestiary is up to date", no Index diff). Tree clean.
- **Result:** WS-1 complete. 8/8 WS-0+WS-1 tasks done, suite green at 1395.

### T2.1 — Spark reset + economy home (C-2, D1) (2026-08-08)

- **Files:** `player_handbook/III.1_Core_Resolution.md`, `player_handbook/Glossary.md`,
  `mm_manual/MM5_Quick_Reference.md`, `mm_manual/MM2_Session_Design.md`,
  `mm_manual/MM3_Campaign_Design.md` (unlisted touchpoint),
  `software/facets/base/facet.yaml`, `software/app/game/character.py`,
  `software/tests/test_websocket.py`, `software/tests/test_docs_consistency.py`.
- **Did:** III.1 §Sparks gains the canonical sentence "Sparks do not carry over.
  You start every session with **3**." (replacing "begins each session with 3
  Sparks"); Glossary Spark entry and MM5 session-start line mirror it. MM2
  §Target Economy rewritten to spend-what-you-earn (spend 2–4, earn 2–4 back);
  Table MM2–3 drops its "End" column (a carry-over concept) — Start/Earned/Spent
  numbers unchanged. facet.yaml `target_economy` description rewritten;
  `end_session_target: 2-4` removed (no code consumer — `SparkDef` never modeled
  `target_economy`). character.py `sparks` docstring now states the reset.
- **Lifecycle:** new-session reset ALREADY implemented at
  `software/app/api/websocket.py:1528` (`_handle_session_reset` sets sparks to
  `base_sparks_per_session`) but had no test — added
  `TestSparkSessionReset` (3 tests: depleted→3, hoard of 5→3, ruleset-base).
  Red not achievable (behavior pre-exists); tests are the missing verification.
- **Unexpected touchpoint:** MM3_Campaign_Design.md:210 ("the Spark they spent…
  wish they had saved") listed Sparks as a *cross-session* resource tax —
  contradicts reset-to-3; sentence removed (single-session Spark tax at line
  208 is untouched and remains correct).
- **Register:** `end a session with 2-4 unspent Sparks` (hyphen, facet.yaml
  form) + `end a session with **2–4 unspent Sparks**` (en-dash+bold, MM2 form)
  + plain en-dash variant.
- **Commands:** `grep -rn "unspent Spark" player_handbook mm_manual
  software/facets` → 2 hits, both reset-consistent. Docs suite 32 passed;
  `TestSparkSessionReset` 3 passed. `python -m tools.build_index` → no diff.

### T2.2 — Magic-Spark fold + ceiling rewrite (P-1, P-9, P-3, D8) (2026-08-08)

- **Files:** `player_handbook/II.3_Magic.md`, `player_handbook/III.1_Core_Resolution.md`
  (unlisted but DESIGN-mandated: §3.1 makes III.1 the canonical home; II.3 restates),
  `player_handbook/Glossary.md` (Spark, Domain Type, Ascendant Domain),
  `player_handbook/II.4b`/`II.4c` (Ascendant Domain entries — "ceiling cannot be
  moved by Sparks"), `player_handbook/Appendix_Magic_Domains.md` (§Prismatic
  preamble), `mm_manual/MM5_Quick_Reference.md` (magic card recompressed),
  `mm_manual/MM2_Session_Design.md` ("Check the ceiling" MM Note — said
  Significant is flatly unavailable pre-Technique, omitting the D8 Spark
  purchase), `software/app/game/engine.py`, `software/app/facets/schema.py`,
  `software/facets/base/facet.yaml`, `software/app/api/websocket.py`,
  `software/app/static/index.html`, tests, `player_handbook/Index.md` (regen).
- **Did (text):** II.3 §Sparks and Magic folded to the two rules of DESIGN §3.1
  (dice + reach); the un-executable "Pushing scope" paragraph deleted; ceiling
  sentences at II.3:99/:184 and the §Broad blurb rewritten to "Reach-Sparks
  cannot move a Broad working's difficulty; dice-Sparks work normally." III.1
  §Spending Sparks gains the canonical "works on any roll, including every
  magic roll" + two-case reach pointer.
- **Did (engine, TDD):** engine DOES model Spark-reach — `resolve_magic_roll`
  had `push_scope`/`ease_focused_major`/`pre_technique_push`. Red first (10
  failed): push_scope now rejected for every domain type; unknown spark_use
  rejected; ineligible ease (Standard/Broad) raises instead of silently
  no-opping; new eligibility functions `can_spark_ease_major` +
  `can_spark_pre_technique_reach` exported for app-side enforcement.
  `SparkPushScopeDef` removed from schema + yaml. Websocket `cast` reordered:
  Spark availability checked pre-resolve, SPENT only post-accept (old order
  burned a Spark on a refused reach). index.html loses the Push Scope radio.
- **Tests updated with reasons:** `test_standard_domain_cannot_ease_major`
  (no-op → raises: silent no-op still cost the Spark at the handler);
  `test_d8_push_does_not_permit_major_scope` (new refusal message);
  `test_sparks_cannot_push_scope_on_a_prismatic_domain` → renamed
  `test_reach_sparks_cannot_move_a_prismatic_working` (covers retired push,
  refused ease, legal dice-Spark). `TestPushScopeResolution` (3 tests of the
  dead rule) replaced by `TestPushScopeRetired` (4). New:
  `TestSparkReachEligibility` (4), `TestCastSparkNotBurnedOnRefusedUse` (3).
- **Unexpected:** first websocket test draft assumed Zahna's Inscription was
  Standard-type; it is Focused (facet.yaml) — test switched to Storm.
- **Register:** `Pushing scope`; `natural ceiling`; `pushed beyond Very Hard
  under any circumstances`; `Their ceiling is their ceiling` (all verified
  present pre-edit, absent post-edit).
- **Commands:** red run → 10 failed as intended; post-implementation
  `test_roll_engine + test_ascendant_domain + test_websocket + test_character`
  → 449 passed. Docs suite 32 passed after `python -m tools.build_index`
  (III.1/II.3 wording feeds index terms). FULL suite → **1405 passed** (308s;
  baseline 1395: +13 new, −3 dead-rule tests).

### T2.3 — Difficulty precedence text + taxonomy relocation (C-3, C-4, K-8, D2) (2026-08-08)

- **Files:** `player_handbook/III.1_Core_Resolution.md`,
  `player_handbook/II.4_Character_Creation_Facets.md`,
  `player_handbook/II.5_Character_Creation_Backgrounds.md`,
  `player_handbook/Glossary.md` (Technique, Specialty),
  `mm_manual/MM5_Quick_Reference.md` (difficulty card + Specialty quick line),
  `mm_manual/MM2_Session_Design.md` (unlisted touchpoint),
  `player_handbook/Index.md` (regen), `software/tests/test_docs_consistency.py`.
- **Did:** III.1 §Difficulty's Technique paragraph replaced by the DESIGN §3.2
  precedence paragraph (base → Easy-tag override, non-stacking → at most ONE
  character-side step from Technique/Specialty/anything future → Support step →
  Easy floor / Very Hard ceiling) + a one-sentence pointer to II.4 for trigger
  kinds. The trigger taxonomy MOVED (not duplicated) into II.4 §Reading the
  Entries as a new "Triggers and the difficulty step" paragraph, reworded
  ("a fact the roll brings with it") so the old III.1 clause dies cleanly.
  II.5 §Specialty + both Glossary entries gain the shared-allowance sentence.
  MM5 difficulty-card line and Specialty line recompressed from the new canon.
- **Unexpected touchpoint:** MM2 §Difficulty and Technique Steps (line 89)
  restated the old taxonomy verbatim enough to trip the register — recompressed
  against the new precedence paragraph. (Its neighboring Pressure Point MM Note
  already teaches the one-character-side-step cap and stands unchanged.)
  Also fixed pre-T2.3: MM5:266 "capped at Minor, full stop" contradicted D8's
  Spark purchase — corrected and amended into the T2.2 commit (a379517).
- **Double-relabel check:** II.2 vignette has no Specialty demonstration; QS
  pregen Specialty lines state only "Standard becomes Easy when directly
  applicable"; no MM5 card shows Technique step + Specialty on one roll.
- **Register:** `something the roll already carries` (verified: present at
  III.1:73 and MM2:89 pre-edit, absent everywhere post-edit).
- **Commands:** `python -m tools.build_index`; docs suite → 32 passed (register
  caught the MM2 hit on first run — fixed, re-ran green).

### T2.4 — Engine precedence order (TDD) (2026-08-08)

- **Files:** `software/app/game/combat.py`, `software/app/api/websocket.py`,
  `software/tests/test_combat.py`, `software/tests/test_websocket.py`.
- **Discovery (how the engine modeled Specialty):** it didn't — `specialty`
  was a display-only text field on `Character` (character.py:98); no roll path
  read it. Easy tags existed as absolute assignments (`target_strike_difficulty`
  → "Easy" on a Tier 2 rider; `maneuver_target_difficulty` → "Easy" on 10+),
  correct override semantics individually but never composed with the character
  step in one place. Support's ease-difficulty mode was broadcast
  (`support_result`) but never mechanically applied to the ally's next roll.
  The one-step cap lived in `apply_character_difficulty_step` for Techniques
  only.
- **Did (red first — 8 failed of 10 new):** new `TestDifficultyPrecedence`
  (10 tests): tag overrides Very Hard → Easy; tag + character step clamps at
  the floor (non-stacking); Specialty alone steps (Hard → Standard, id
  `"specialty"`); undeclared / specialty-less negatives; Technique+Specialty
  → ONE step (player's pick beats auto); Support step lands after the
  character step (Hard → Standard → Easy); clamps at both ladder ends; full
  chain. Then implemented: `apply_character_difficulty_step` gains the
  Specialty candidate in the SAME pool (ranks: declared Technique 0 <
  Specialty 1 < auto Technique 2, then lowest id); new `compose_difficulty()`
  = base → Easy-tag override → single character step → Support step → clamp
  (ladder primitives already saturate — engine.py needed no change).
- **App wiring (unlisted but needed for enforcement):** the four WS contexts
  (`_build_roll_request`, roll, strike, reaction) pass
  `specialty_declared`; `_apply_difficulty_step` banners a Specialty step as
  "Specialty". 2 live-play WS tests (declared steps + names the source;
  undeclared doesn't). First WS run failed because the generic `roll` handler
  builds its own context — a fifth context site the grep list missed.
- **Commands:** red run 8/10 failed → post-implementation
  `test_combat.py` 153 passed, WS class 2 passed. FULL suite →
  **1417 passed** (319s; +12 over T2.2's 1405). No existing test needed
  updating — the Technique-only behavior is byte-identical when no Specialty
  is declared.

### T2.5 — Group rolls vs Threat Clocks (C-5) (2026-08-08)

- **Files:** `player_handbook/III.2_Adventuring.md`, `player_handbook/Index.md`
  (regen).
- **Did:** the clock-advance bullet in §Hazards and Threat Clocks gains "A
  group roll (Chapter III.1) advances a Threat Clock at most once, keyed to
  the group's overall result." MM5's Group Rolls card does not mention
  hazards, so per the task's own condition it takes no change.
- **Unexpected:** the first phrasing cross-referenced the *Group Rolls*
  heading verbatim and tripped INV `test_capitalized_terms_are_glossary_defined`
  ("Rolls" capitalized mid-sentence) — reworded to "(Chapter III.1)".
- **Commands:** `python -m tools.build_index`; docs suite → 32 passed.

### T2.6 — 7–9 narration sequencing (C-7, D3) (2026-08-08)

- **Files:** `player_handbook/III.1_Core_Resolution.md` (§Partial Success),
  `player_handbook/Glossary.md` (Partial Success — carried the retired phrase
  verbatim), `mm_manual/MM2_Session_Design.md` (magic 7–9 guidance),
  `mm_manual/MM5_Quick_Reference.md` (magic 7–9 card),
  `software/tests/test_docs_consistency.py`.
- **Did:** III.1: "The MM must name the cost *before* the player decides how
  to proceed" → "The MM names the cost *before* narrating the success — the
  cost is part of the outcome, not an offer to weigh." Glossary mirrors it.
  II.2's outcome table (II.2–3) restates only tier labels, no sequencing —
  no change needed there.
- **Unexpected touchpoints:** MM2:471 and MM5:268 (magic 7–9) instructed the
  OPPOSITE order — "confirm the success in the fiction first, before anything
  else." Their real point (a partial is a success, never a near-miss) is kept;
  the ordering clause now matches III.1 (cost named as part of/before the
  success narration).
- **Register:** `before the player decides how to proceed`.
- **Commands:** `grep -rn "decides how to proceed" player_handbook mm_manual`
  → empty. `python -m tools.build_index` (no diff). Docs suite → 32 passed.

### T2.7 — Fixed-pairs principle (C-9) (2026-08-08)

- **Files:** `player_handbook/II.6_Character_Creation_Skills.md` (§Using
  Skills).
- **Did:** one sentence appended to the §Using Skills roll paragraph:
  "Skill–attribute pairs are fixed except where a rule explicitly says
  otherwise; the Strike (Chapter III.3) is the named exception."
- **Verified agreement:** III.3 §Strike already frames its pairings as
  "defaults, not restrictions" with the MM naming a different attribute where
  the fiction supports it — exactly the licensed exception. QS Mordai's Strike
  line (2d6 + Strength + Combat) is a plain valid pairing; no QS-4 wording
  conflicts.
- **Commands:** `python -m tools.build_index` (no diff); docs suite →
  32 passed.

### T2.8 — WS-2 sweep (2026-08-08)

- **Register grep:** all 6 WS-2 phrases (+ the 3 T2.1 variants) absent from
  every live surface; invariant test green. One grep hit — "unspent points do
  not carry over" (Glossary, Skill Point) — is WS-4 T4.3's registered target
  and still-live canon until banking lands; correctly untouched by WS-2.
- **Glossary diff review (each entry reread against its body source):**
  Spark ↔ III.1 §Sparks/§Spending Sparks + II.3 (dice + two reach cases +
  reset) ✓; Domain Type ↔ II.3 §Broad + :99 ✓; Ascendant Domain ↔ II.4b/c
  entries ✓; Specialty ↔ II.5 §Specialty (shared allowance) ✓; Technique ↔
  II.4 box + III.1 precedence ✓; Partial Success ↔ III.1 §Partial Success
  (narration sequencing) ✓.
- **Regeneration:** `python -m tools.build_index` idempotent (no diff);
  `python -m tools.build_bestiary --check` → "Bestiary is up to date."
- **Straggler fix:** test_roll_engine.py section header still claimed
  push_scope was "implemented, not dead code" — reworded to the T2.2 truth.
- **Full suite:** **1417 passed** (311s). WS-2 complete: baseline 1395 →
  1417 (+22 net: 3 Spark-reset, +11/−3 magic-Spark, +10 precedence, +2
  live-play Specialty, −1 replaced ascendant test folded into a wider one).

---

## Escalations

(none)
