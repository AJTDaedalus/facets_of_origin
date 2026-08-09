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

### T3.1 — Open tag engine (K-6, D4; TDD) (2026-08-08)

- **Files:** `software/app/game/combat.py`, `software/app/game/enemy.py`
  (unlisted but canonical: enemy state + the `endurance` deprecation pattern
  live HERE, not in `schema.py` — the task's schema.py pointer covered the
  `EnemyDurabilityDef` rider fields), `software/app/facets/schema.py`,
  `software/facets/base/facet.yaml`, `software/tools/combat_sim.py`
  (unlisted but load-bearing: it drives the changed combat.py API),
  `software/tests/test_combat.py`, `test_enemy.py`, `test_combat_sim.py`,
  `test_combat_characterization.py`.
- **Red first:** 16 failed of 19 new tests (`TestOpenTag`,
  `TestPvPOutcomesUnchanged`, `TestEnemyOpenState`,
  `TestTier1ImmunityDeprecation`).
- **Did (engine):** `can_apply_rider`/`rider_tier_eligible` retired →
  `can_apply_open` (reads new `enemy_durability.open_on`) + `open_clear_mode`
  (reads `open_clears: enemy_action` — cleared ONLY by the enemy visibly
  spending its action; never at end of exchange). `target_strike_difficulty`
  now takes `target_open: bool` and routes through `compose_difficulty` as an
  Easy-tag source (WS-2's pipeline, per the operational lesson — no bypass).
  `apply_condition` loses `is_rider` (character-target only now; PvP
  escalation unchanged). `Enemy` model gains ephemeral `open` tracker state
  (reset by `init_combat`, sent in `to_client_dict`, never saved to .fof).
  yaml `strike_outcomes` gains a PvP-scope comment; `rider_on`/`rider_tiers`
  → `open_on`/`open_clears`; `EnemyDurabilityDef` mirrors it.
- **tier1_immunity:** loader warns (DeprecationWarning, endurance pattern)
  but KEEPS the entry — first draft dropped it on load, which churned the
  generated Guardian stat block (TR 17→16) ahead of T3.4's proper .fof
  re-expression; warn-and-keep matches the endurance pattern (file still
  loads as published) and leaves exactly one cleanup site for T3.4. An
  xfail guard (`test_no_shipped_enemy_lists_tier1_immunity_after_t3_4`)
  flips to enforcement when T3.4 lands.
- **Sim (drives combat.py, no forked rules):** `EnemyState.open`;
  `_choose_rider` → `_should_leave_open` (attacker always takes the option —
  worst-case pressure, mirroring the old worst-case rider policy);
  `_should_clear_open` MM-side policy: **Boss clears (visible action spend),
  Named fights on** — rationale in the docstring (a 3–4-Resolve Named's value
  is its attacks; the tempo trade favors the pool that can afford it). With
  the all-enemies-always-clear policy the four Recipe rows moved +13..+22pp
  (0.76→0.895, 0.475→0.695, 0.20→0.36/0.325); under Boss-only clear the
  recorded seed-1 Recipe values reproduce EXACTLY (Open-not-cleared is
  behaviourally identical to the old permanent staggered rider at fixed
  seeds). T3.11 re-measures with 3 seeds × 200 regardless.
  `special_ignores_tier1` removed from `EnemyState` (dead with riders gone;
  scenarios.py reference is T3.4). Target/Spark AI keys on `open` instead of
  enemy Tier 2 Conditions.
- **Re-pins (documented in each docstring):** 4 G0 fixed-seed end states —
  sergeant seeds 1/5 identical dice, Condition tuple → Open tag; guardian
  seed 2 shortens 3→2 exchanges (Boss trades attacks for clears under Easy
  pressure); seed 3 same result shape. 3 sim tests rewritten rider→Open.
- **Commands:** red 16 failed → post-implementation targeted suites 586
  passed + 1 xfail. FULL suite → **1421 passed** + 1 xfail (317s; +5 net
  over 1417: +19 new, −9 rider tests, −5 folded/rewritten). Bestiary
  `--check` up to date (no stat-block churn).

### T3.2 — Open tag body text (K-6, K-12) (2026-08-08)

- **Files:** `player_handbook/III.3_Combat.md`, `player_handbook/Glossary.md`,
  `mm_manual/MM5_Quick_Reference.md`, plus unlisted carriers found by the
  rider sweep: `player_handbook/III.1_Core_Resolution.md` (:73 precedence
  paragraph's "(a rider Condition, a Maneuver)" tag example),
  `player_handbook/II.4a_Character_Creation_Facet_Body.md` (Overwhelming
  Force + The Final Blow "Normal:" lines), `mm_manual/MM1` (:39 rider
  paragraph → Open + the K-12 anti-snowball sentence; :260 "rider limit"),
  `mm_manual/MM2` (:89 tag example; :200 "carrying a Staggered rider"),
  `software/facets/base/facet.yaml` (both Technique `normal:` mirrors +
  the :1704 calibration comment), `player_handbook/Index.md` (regen),
  `software/tests/test_docs_consistency.py` (register).
- **Did:** III.3 §Strike vs-enemy paragraph rewritten to the single Open
  tag (attacker's option on 10+; Easy to Strike for everyone; player
  narrates; cleared ONLY by the enemy visibly spending its action);
  §Conditions intro — enemies now carry no Conditions at all; §Named NPCs
  rider paragraph → Open + visible-recovery cost; magical Strikes line;
  the Boss vignette re-voiced (Mordai now narrates what Open looks like,
  the MM notes the guardian *choosing* not to spend its action closing
  up — the fiction's grinding-seam line survives untouched); both
  quick-ref tables (III.3–12 + exchange-flow step 5). PvP paragraph and
  PvP tier text untouched everywhere. Glossary: Rider entry replaced by
  an Open entry (alphabetical slot after Off-Balance); Condition entry
  scoped to characters; Named NPC entry's stale "Resolve, Posture,
  reactions" (a K-1 survivor) fixed to "Techniques" + never-rolls.
- **Register:** `a Tier 1 or Tier 2 Condition of your choice` (verified in
  situ pre-edit) + `rider Condition` (broad drift guard). Remaining
  "rider" hits in scope: `enemies/archive_guardian.fof` historical
  calibration comments only — T3.4 touches that file and rewords them.
- **INV catch:** first draft's "(see below)" pointer at III.3:128 tripped
  `test_no_vague_cross_references` — pointer dropped (the rule follows in
  the same section).
- **Commands:** `python -m tools.build_index`; docs suite → **32 passed**;
  rider-phrase grep over both books → empty.

### T3.3 — Open tag transport (2026-08-08)

- **Files:** `software/app/api/websocket.py`, `software/app/static/js/play.js`,
  `software/app/static/js/components.js`, `software/app/static/js/tools.js`
  (unlisted: its in-app rules card restated the rider rule),
  `software/tests/test_websocket.py`.
- **Red first:** 3 failed of 4 new (`enemy_spawned` already carried `open`
  via T3.1's `to_client_dict`).
- **Did (server):** `enemy_update` accepts an `open` boolean (set = the
  attacker's 10+ option; clear = the enemy visibly spending its action —
  a choice the MM relays, so it lives on the manual-update handler, not
  `enemy_strike`, which resolves outcomes). All four `enemy_updated`
  broadcast sites (update, mook strike, named strike, final blow) carry
  `open`. A Strike broadcast preserves the tag — only the enemy's action
  clears it (tested).
- **Did (client):** `onEnemyUpdated` applies `open` and announces both
  edges in chat ("left Open — Easy to Strike for everyone" / "spends its
  action recovering"); enemy card renders an OPEN badge (players and MM);
  MM controls swap the retired "+ Condition" prompt for a Leave Open /
  Clears Open (action) toggle (`enemyToggleOpen`). `enemyAddCondition`
  deleted (enemies take no Strike Conditions); legacy condition badges
  still render and remain MM-removable so a stale tracker entry can be
  cleaned. tools.js rules card updated rider→Open.
- **Server keeps `add_condition`/`remove_condition`** on `enemy_update`
  as a manual-correction path (remove is still wired in the UI); only the
  UI affordance for adding died with the rule.
- **Commands:** red 3 → `test_websocket.py` **222 passed**;
  `test_api_enemy + test_agentic_playtest` 128 passed; `node --check` on
  all three JS files OK.

### T3.4 — Archive Guardian + agentic scenarios + bestiary regen (2026-08-08)

- **Files:** `enemies/archive_guardian.fof`,
  `software/tools/agentic_playtest/scenarios.py`,
  `mm_manual/MM1_Encounters_and_Enemies.md` (stat-block example, Table
  MM1-4 row, phase-change example + Special lever, asymmetric-encounter
  TR, `.fof` format yaml example), `bestiary/B3_The_Made.md` (hand prose
  "TR of 17" → 16; stat block regenerated), `bestiary/Finding_Aids.md`
  (regen), `software/tools/combat_sim.py` (unlisted:
  `archive_guardian_def` mirrors the .fof), `software/tests/test_enemy.py`
  (TR test re-derived).
- **Re-expression (character kept, mechanism changed):** Reduced Mode
  keeps "attack drops to +1, blows land as Tier 1" verbatim. The
  "ignores Tier 1 Conditions — sensory subsystem shut down" clause (now
  vacuous: enemies take no Strike Conditions) becomes "it stops
  registering harm — left Open, it will not spend an action recovering,
  because the sensory subsystem that would notice has shut down." Same
  fiction, live mechanic. `techniques: [phase_change]`; **TR 17 → 16**
  (the retired technique's +1 came off; breakdown updated in .fof notes,
  MM1 example, MM1-4 table, MM1 asymmetric section, B3 hand prose).
- **Sim modeling:** `special_no_clear_open` added to `EnemyState`
  (mirrors the modeling depth `special_ignores_tier1` had) — after the
  Guardian's phase fires it never spends the action to clear Open; set
  in `archive_guardian_def`. Characterization pins unchanged (both
  guardian seeds defeat it while Open pre-clear).
- **Gotcha:** the .fof historical note first said "tier1_immunity"
  verbatim, tripping both the acceptance grep and the shipped-file
  guard — reworded to describe the retirement without the token. The
  T3.1 xfail guard (`test_no_shipped_enemy_lists_tier1_immunity_after_t3_4`)
  now passes as a real pass.
- **Commands:** `python -m tools.build_bestiary` (2 files), `--check` up
  to date; `grep -rn "tier1_immunity" enemies/ mm_manual/ bestiary/
  spec/ software/facets/` → **empty** (only the loader deprecation path
  in `app/game/enemy.py` remains); enemy/docs/sim/characterization/
  agentic suites → 97 + 90 + 128 passed.

### T3.5 — Uncontested-exchange rule + Withdrawn cap (K-2, D5) (2026-08-08)

- **Files:** `player_handbook/III.3_Combat.md`, `mm_manual/MM5_Quick_Reference.md`,
  `mm_manual/MM1_Encounters_and_Enemies.md`, `software/facets/base/facet.yaml`,
  `software/app/facets/schema.py` (EnduranceDef docstring),
  `software/app/game/combat.py`, `software/app/game/session.py`,
  `software/app/api/websocket.py`, `software/tools/combat_sim.py` (recovery
  clamp callers), plus unlisted quick-ref carriers of "recover 2 Endurance":
  `player_handbook/Glossary.md` (Posture), `player_handbook/Quick_Start.md`
  (QS-4 posture row), `software/app/static/js/tools.js`,
  `software/app/static/index.html`; `player_handbook/Index.md` (regen);
  tests in `test_combat.py` + `test_websocket.py`.
- **Red first:** 7 engine tests failed (`TestWithdrawnRecoveryCap` 4,
  `TestUncontestedExchange` 3); the 3 WS tests hung on `receive_json` for
  the not-yet-existing prompt (red by absence).
- **Did (engine):** `apply_withdrawn_recovery(current, pool_max, ruleset)`
  — recovery up to the pool, the clamp now a combat.py rule (WS handler and
  both sim recovery sites switched off their inline `min()` copies);
  `exchange_uncontested(offensive_actions)` — the rule's only home.
- **Did (WS):** `Session.offensive_actions_this_exchange` set; marked by
  the strike handler (post-validation — a missed Strike still contests),
  the maneuver handler, and `enemy_strike` (an MM-recorded off-app Strike
  contests too); cleared at `combat_start` and every `end_exchange`. On an
  uncontested exchange the MM's own socket (only) receives
  `uncontested_exchange` with the advance-for-free prompt.
- **Did (text):** III.3 §Recovering Endurance gains "up to your pool" + the
  new **uncontested exchange** rule paragraph; the Withdrawn MM Note
  re-grounded on the rule (spend the exchange visibly, no punishing);
  posture table, exchange step 4, and both in-chapter quick-ref spots
  updated; MM5 exchange flow + posture card; MM1 §Mooks gains "A Mook-only
  encounter must carry a clock or an objective" with the
  attrition-cannot-lose rationale. facet.yaml `recovery_withdrawn` comment
  states the cap (engine reads the clamp from `apply_withdrawn_recovery`).
- **Register:** none — no phrase died; the old wording was extended, not
  replaced ("recover 2 Endurance" remains true).
- **Commands:** red 7+3 → engine 7 passed, WS 3 passed; docs suite 32
  passed after `python -m tools.build_index`. FULL suite → **1436 passed**
  (441s; 1421 at T3.1 → +4 T3.3 WS, +1 T3.4 xfail→pass and net test
  changes, +7 T3.5 engine, +3 T3.5 WS).
- **Session note:** execution was interrupted mid-T3.5 by a usage limit and
  resumed; the in-flight diff was reviewed against the task spec before
  completion. T3.6 text edits begun while the T3.5 full suite ran were
  reverse-staged out (stash + inverse edits) so this commit stays
  single-task; they are replayed in T3.6's own commit.

### T3.6 — Cut budget & multiplier tables (K-5, D6) (2026-08-08)

- **Files:** `mm_manual/MM1_Encounters_and_Enemies.md`,
  `mm_manual/MM5_Quick_Reference.md`, `docs/DECISIONS.md`, plus carriers
  found by the `[Bb]udget` grep: `player_handbook/Glossary.md` (Encounter
  Budget entry), `player_handbook/Table_of_Contents.md` (MM1 blurb),
  `mm_manual/MM2_Session_Design.md` (prep checklists ×2), MM1's intro
  tour and lateral-solution MM Note; regenerated `Index.md`,
  `List_of_Tables.md`, `List_of_Boxes.md`;
  `software/tests/test_docs_consistency.py` (register).
- **Cut:** Table MM1-5 (TR budget ×1–4), Table MM1-6 (action-economy
  multipliers), their caveat prose, the cheat-block budget lines, and
  MM5's whole budget compression. §Encounter Budget renamed **§Sizing an
  Encounter** (actor-count rule + Party Strength + a rewritten
  summed-TR-cannot-size example box that keeps the 3-Sergeants teaching
  case without referencing a budget that no longer exists).
- **Kept (per task):** TR itself, TR minimums, the Recipe Table, the
  actor-count rule, Party Strength (the Recipe Table's key).
- **Added:** the K-3 sentence in §Five-Minute Method Step 3 and MM5's
  Recipe intro: "adding enemies mid-fight is the sharpest dial you own —
  one Mook is one difficulty band (76% → 47% → 20%)."
- **DECISIONS.md:** D6 record with the full retired numbers (budget rows
  + multipliers) and the Series 9 citation (Parts C/D, seed-1 n=200 row
  values), so nothing is lost.
- **Glossary:** Encounter Budget entry replaced by an Encounter Recipe
  Table entry (same alphabetical slot; INV-3 pointer resolves).
- **Renumber:** MM1-7/MM1-8 → MM1-5/MM1-6; `python -m
  tools.build_table_register` regenerated both Lists (76 tables /
  70 boxes — the "why the budget is only a rough check" box died, the
  new example box registered).
- **Register:** `x multiplier` (exact MM5 string, verified pre-edit) +
  `Action Economy Multipliers`.
- **Commit hygiene:** these edits were begun while T3.5's full suite ran,
  then reverse-staged out of the T3.5 commit and replayed here — see the
  T3.5 session note.
- **Commands:** docs + build_index suites → **47 passed** (INV-9/INV-10
  table invariants green on the renumbered captions); acceptance greps
  clean (no `x multiplier`, no MM1-5/6 budget captions; the only MM1-5/6
  hits are the renumbered Recipe tables).

### T3.7 — `defense_modifier` retirement (K-11) (2026-08-08)

- **Files:** `software/app/game/enemy.py` (field removed; `from_fof` warns
  on the legacy key and ignores it — endurance pattern),
  `software/app/api/routes/enemy.py` (CreateEnemyRequest),
  `software/app/api/websocket.py` (inline spawn),
  `software/app/static/js/builder.js` + `index.html` (Defense Mod input
  removed), `software/tools/build_bestiary.py` (stat-block template's
  "· defense +N" segment removed), `software/tools/combat_sim.py`
  (EnemyState field + every def), `software/tools/agentic_playtest/
  scenarios.py`, 16× `enemies/*.fof`, **9× `adventures/oraga_night/
  enemies/*.fof`** (unlisted but shipped — anti-fragment rule 1; the
  spec/examples files carried no defense fields), `enemies/chicken.fof`
  notes (prose referenced the field by name — reworded, joke intact),
  `mm_manual/MM1` (minimal stat block Defense line, all three example
  blocks, the Named build list bullet, the `.fof` format doc line),
  regenerated bestiary (all 4 B-files' stat blocks lose the defense
  segment) + `Finding_Aids.md`; tests: `test_enemy.py` (6 new),
  `test_api_enemy.py`, `test_agentic_playtest.py` (canon-drift field
  list). `playtest/**` untouched.
- **Red first:** 4 failed of 6 new (`TestDefenseModifierDeprecation`).
- **TR values unchanged** — the field was never a TR term
  (`test_tr_unchanged_by_retirement` pins the Sergeant at 8); a
  shipped-files guard (`test_no_shipped_enemy_lists_defense_modifier`)
  covers enemies/ AND adventures/.
- **Register:** `defense_modifier` (scanned scope now clean; the loader
  warning text lives in `app/`, outside scope by design).
- **Commands:** red 4 → 539 passed across
  enemy/api/api_enemy/websocket/agentic/docs suites; `python -m
  tools.build_bestiary` (4 files) then `--check` clean; `node --check
  builder.js` OK; acceptance grep over enemies/ mm_manual/ spec/
  software/facets/ bestiary/ characters/ adventures/ → **empty**.

### T3.8 — Enemy posture: triggers instead of ceremony (K-4, K-10, D12) (2026-08-08)

- **Files:** `player_handbook/III.3_Combat.md` (§Postures rewritten — PC
  blind declaration explicitly KEPT, enemy stances stated openly from
  conduct `triggers:`; exchange step 2; Strike-difficulty parenthetical;
  §Enemy Posture and Reaction Difficulty lead; Insight combat-skill entry
  and the "Reading the opponent" MM Note recast as the counter-tool for
  what a stated stance does not say; vignette posture beats re-voiced —
  the MM names the guardian's stance before declarations),
  `mm_manual/MM1` (§Enemy Conduct Fields: `triggers:` now documents
  posture explicitly — "write the stance as a rule the table can learn"),
  `enemies/city_watch_sergeant.fof` (worked trigger: "Defensive once left
  Open" — its old trigger read "Defensive if Staggered", a Condition an
  enemy can no longer take; notes synced), `enemies/veteran_soldier.fof`
  (unlisted: same stale "Defensive if Staggered themselves" in tactics —
  PC-side Cornered/Staggered references kept, they are still real),
  `mm_manual/MM5_Quick_Reference.md` (exchange-flow line 2 + posture-card
  note), `player_handbook/Glossary.md` (Posture entry), bestiary
  regenerated (sergeant's block renders the new trigger), Index +
  List_of_Boxes regenerated (the MM Note title changed).
- **Also fixed (T3.4 leftover found by the sweep):** the vignette's
  Reduced-Mode narration still described the dead ignores-small-hurts
  mechanic — now "the subsystem that would notice it is Open has shut
  down; it will never stop to close it."
- **Register:** `player characters and significant antagonists alike`
  (the ceremony's distinctive clause, verified in situ pre-edit).
- **Commands:** `build_bestiary` (1 file) + `--check` clean;
  `build_index`; `build_table_register` (box title change); docs suite →
  **32 passed**.

### T3.9 — Enemy Techniques + incoming-Condition selection (K-9, K-7) (2026-08-08)

- **Files:** `mm_manual/MM1_Encounters_and_Enemies.md` (new §Three Worked
  Enemy Techniques under Named NPCs), `player_handbook/III.3_Combat.md`
  (§Incoming Condition Tier gains the K-7 sentence),
  `mm_manual/MM5_Quick_Reference.md` (enemy-attack card line),
  `enemies/veteran_soldier.fof` (canonical instance: gains
  `telegraphed_finisher`; TR 10 → 11, breakdown + tactics synced),
  MM1 Table MM1-4 row, `software/tools/combat_sim.py` (docstring TR),
  bestiary + Index regenerated.
- **Templates (DESIGN §4.4 a/b/c, setting-agnostic, no proper nouns):**
  Flurry (once/scene, hits every engaged PC at Tier 1 — reaction-economy
  pressure), Telegraphed Finisher (once/scene, repeats a carried Tier 2
  type — landed repeat is Broken; named one full exchange before it can
  land, always), Sapping Strike (drains 2 Endurance instead of a
  Condition; partial reaction halves to 1). Each is a stat-block-ready
  `techniques:` yaml snippet + one usage paragraph, each +1 TR.
- **K-7 canon:** "The MM chooses which Condition the tier delivers.
  Repeating a type the character already carries is how an enemy
  deliberately finishes someone — telegraphed, never sprung." The
  veteran's fiction already pressed Cornered/Staggered targets; the
  Finisher formalizes it as the worked instance.
- **Sim note:** the simulator's `_choose_condition` policy has ALWAYS
  preferred repeating a carried Tier 2 (worst-case finisher-every-time
  MM). Left unchanged deliberately — changing selection policy would
  silently re-baseline Series 9 ahead of T3.11's measured rerun; the
  policy now reads as the harshest legal use of the K-7 rule.
- **Commands:** `build_bestiary` (2 files: B2 block + Finding_Aids TR
  re-sort) + `--check` clean; enemy/docs/sim suites → 179 passed.

### T3.10 — Paper fallback + Intercept card (K-13, K-12) (2026-08-08)

- **Files:** `player_handbook/III.3_Combat.md` ("Variant — running it on
  paper" box after §Armor: armor = one checkbox per downgrade, ticked as
  spent, fresh row at scene end; Aggressive first-reaction surcharge =
  flip a token on first paid reaction, clear at exchange end; plus the
  in-chapter quick-ref Intercept row), `mm_manual/MM5_Quick_Reference.md`
  (Intercept row gains once-per-exchange + "the protected ally decides
  who steps in" — both clauses already canonical in III.3 §Intercept
  body text, so the compression stays a compression), Index +
  List_of_Boxes regenerated (new Variant box).
- **Commands:** docs suite → 32 passed.

### T3.11 — Sim campaign (DESIGN §4.7) (2026-08-08)

- **Files:** `software/tools/combat_sim.py` (the `objective_clock` hook on
  `run_combat`/`run_simulation` — reads K-2/D5 from
  `combat.exchange_uncontested`, never re-derives; `SimResult` gains
  `uncontested_exchanges` + `objective_lost`, both default-preserving so
  every recorded corpus reproduces bit-identical),
  `software/tests/test_combat_sim.py` (`TestObjectiveClockHook`, 3 tests),
  `research/simulation_log.md` (**Series 10** appended in the file's
  format). MM1/MM5 Recipe Tables: **no change needed** — see below.
- **Results vs acceptance (full numbers in Series 10):**
  - **Recipe rows (3 seeds × 200/row):** every Part D row reproduces its
    published value to the decimal — Skirmish 100/100/100, Standard
    76.0/74.5/80.0, Hard 47.5/48.0/47.0, Deadly 20.0/20.0/22.5 and
    20.0/16.5/21.0 — **+0.0pp across the board** (band: ±10pp). The
    Named-fights-on-while-Open sim policy is behaviourally identical at
    fixed seeds to the old permanent Tier-2 rider, which is why; the
    rejected always-clear policy had moved rows +13..+22pp (T3.1 LOG).
  - **A5 (15 Mooks):** the default-AI win is 100% with **0 uncontested
    exchanges** — a fighting win (enemy fire concentrates, two strikers
    stay topped up), not a cycling one; settled Mook-swarm doctrine, not
    an exploit. The stall itself is dead: a pure-turtle party under the
    MM1-mandated 4-segment clock loses the objective in exactly 4
    exchanges, **100% of runs, all seeds** (vs an unresolvable 20-exchange
    timeout without the rule). Acceptance met in substance: no win happens
    *via cycling*, and cycling now loses.
  - **Boss median:** Archive Guardian median **2** exchanges (means
    2.27/2.29/2.32, seeds 1/2/3) — inside the 2–4 band at its floor;
    the shortening vs G1's 3 is Open pressure by design. Flagged in
    Series 10 for playtest attention; Resolve retuning out of scope.
- **Commands:** hook tests red→green (first clock test's scenario
  corrected: the default AI un-cycles after one Withdrawn exchange, so
  the deterministic test monkeypatches the posture policy — the exploit
  is a policy, not the shipped AI); `test_combat_sim.py` 79 passed;
  campaign script in the session scratchpad (reproduce lines in
  Series 10). FULL suite: see T3.12.

### T3.12 — WS-3 sweep (2026-08-09)

- **Commands (orchestrator-run after the agent's second session ended):**
  register invariant + full suite → **1445 passed** (337s). Bestiary
  `--check` → up to date. `build_index` → idempotent, no diff. Sweep greps:
  budget/multiplier remnants in both books → empty; `tier1_immunity` outside
  the schema deprecation path → empty; Open present in MM5 cards (7 refs).
- **Note:** T3.11's builder.js straggler (form reset touching the removed
  defense field — would have thrown a TypeError on clearEnemyForm) was folded
  into the T3.11 commit with a note.
- **Result:** WS-3 complete. 12/12 tasks, suite 1417 → 1445, no escalations.

---

## Escalations

(none)
