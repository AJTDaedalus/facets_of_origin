# TASKS — Fun & Ease-of-Play Fixes

**Upstream:** `docs/DESIGN_fun_ease_fixes.md` (WS/decision/§ references below),
`docs/RESEARCH_fun_ease_review.md`.
**Worker protocol:** one task per sitting; open only listed files; run the task's
acceptance commands; mark done/blocked here; append to `docs/LOG_fun_ease_fixes.md`;
stop and report.

---

## Anti-fragment protocol (applies to EVERY task)

The review found that past contradictions came from changes landing in one file and
missing siblings (stale Parry text, quick refs diverging, superseded research docs).
Every task therefore obeys five rules:

1. **Touchpoints are exhaustive, not exemplary.** The Files list in each task was
   built by grepping the repo, not from memory. If you discover an unlisted file
   carrying the old rule, update it in the same task and note it in the LOG — never
   leave it "for later."
2. **Retire phrases into the register.** Any task that removes or rewrites rule
   wording adds the dead phrase to `RETIRED_PHRASES` in
   `software/tests/test_docs_consistency.py` (created by T0.1). The suite then fails
   forever if the phrase reappears. Historical archives are excluded by the test's
   scope (`playtest/`, `docs/`, `research/simulation_log.md`,
   `research/advancement_priority_questions.md`).
3. **The Glossary is a rules mirror.** `player_handbook/Glossary.md` restates many
   rules (Spark, Skill Point, Mark, Broad, Career Advance, Technique…). Any task
   changing a defined term MUST update its Glossary entry in the same task.
4. **Generated files are rebuilt, never edited:** `Index.md`, `List_of_Tables.md`,
   `List_of_Boxes.md`, `bestiary/Finding_Aids.md`, bestiary stat blocks (via
   `software/tools/build_bestiary.py`). Any task touching headings, tables, boxes,
   or `enemies/*.fof` ends by regenerating and committing the outputs.
5. **Quick refs move with body text, same task.** MM5/QS-4/in-chapter boxes that
   state a rule you are changing are touchpoints of THAT task (compressions may
   never disagree with canon, even mid-branch). WS-5's recompression pass (T5.10)
   is verification, not the fix vehicle.

**Standard acceptance (implied in every task):** `pytest software/tests/` green;
listed greps return the expected result; LOG updated.

---

## WS-0 — Scaffolding

- [x] **T0.1 — Retired-phrase invariant scaffold.**
  Files: `software/tests/test_docs_consistency.py`.
  Do: add `RETIRED_PHRASES: list[tuple[str, str]]` (phrase, reason/finding-id) and a
  test that greps `player_handbook/ mm_manual/ bestiary/ facets/ software/facets/
  enemies/ characters/ spec/` for each phrase and fails on any hit. Seed empty.
  Exclude the historical paths listed in protocol rule 2.
  Accept: suite green; adding a dummy phrase that exists makes it red (verify, then
  remove the dummy).

- [x] **T0.2 — Create `docs/LOG_fun_ease_fixes.md`** with the WS/branch table from
  DESIGN §1 and an empty escalation section.

## WS-1 — Text integrity (branch `fix/text-integrity`)

- [x] **T1.1 — III.3 Named-NPC bullet (K-1).**
  Files: `player_handbook/III.3_Combat.md` (lines ~348–356).
  Do: "use the full combat structure: Resolve, Posture, reactions, the works" →
  "Resolve, Posture, Techniques"; "A primary attribute and skill — the modifier they
  use for Strikes and Parries" → describe attack modifier as an authoring input;
  PCs react. Read the surrounding §Named NPCs section whole and fix any other
  enemy-rolls implication.
  Register: `reactions, the works`; `they use for Strikes and Parries`.
  Accept: `grep -n "Parr" player_handbook/III.3_Combat.md` shows only PC-side
  reaction text (Dodge/Parry as PC actions, vignette lines, reaction tables).

- [x] **T1.2 — MM1 stale Parry + Defense-line claim (K-1, K-11 prep).**
  Files: `mm_manual/MM1_Encounters_and_Enemies.md` (line ~315 `.fof` example; the
  minimal stat block's Defense line).
  Do: delete `# same roll for Parry`; rewrite the Defense line to stop claiming it
  "feeds the TR formula" (full removal happens in T3.7 — here only the false claim
  dies). Sweep MM1 for any other enemy-reaction phrasing.
  Register: `same roll for Parry`; `feeds the TR formula`.

- [x] **T1.3 — Enemy `.fof` conduct text contradicting no-roll (K-1 sweep).**
  Files: `enemies/veteran_soldier.fof` ("Reaction preference: Parry over Dodge
  (higher modifier)…") and any other hit from
  `grep -ln "Parry\|Dodge\|reaction" enemies/*.fof`.
  Do: rewrite conduct lines that imply the enemy rolls reactions into no-roll
  authoring language (defensive behavior expressed as posture/difficulty guidance).
  Keep existing flavor wording wherever possible — minimal-touch, no new fiction.
  Accept: the grep returns no roll-implying lines; bestiary regenerated if any
  listed enemy feeds a stat block.

- [x] **T1.4 — MM1 §Mooks "worn down" mechanism (K §4.3).**
  Files: `mm_manual/MM1_Encounters_and_Enemies.md`.
  Do: replace the Endurance-attrition claim with the true mechanism: Absorb costs
  nothing; Mook Tier 1 chip degrades reactions against simultaneous Named Tier 2s
  (Winded −1 next roll, Off-Balance +1 next reaction cost).
  Register: the exact "worn down" clause after reading it in situ.

- [x] **T1.5 — Supersession header (P-15).**
  Files: `research/advancement_priority_questions.md`.
  Do: top-of-file note: item #5 figures superseded by shipped II.4 (5/10/15
  thresholds, flat 2-point cross-Facet cost); pointer to II.4 and this pipeline.

- [x] **T1.6 — WS-1 sweep.**
  Do: run the full register grep; rebuild generated files; full suite;
  `grep -rn "Parr" mm_manual/ enemies/ facets/` — verify every remaining hit is
  legitimate PC-side text. LOG the sweep output.

## WS-2 — Rules unification (branch `feat/rules-unification`)

- [x] **T2.1 — Spark reset + economy home (C-2, D1).**
  Files: `player_handbook/III.1_Core_Resolution.md` (~line 92),
  `player_handbook/Glossary.md` (Spark entry, line ~108),
  `mm_manual/MM5_Quick_Reference.md` (~line 72),
  `mm_manual/MM2_Session_Design.md` (lines ~768, ~793 — **the flow targets
  contradict reset-to-3 as written**: "end a session with 2–4 unspent Sparks" must
  become spend-what-you-earn guidance),
  `software/facets/base/facet.yaml` (~line 1315 duplicates the MM2 target text;
  `base_sparks_per_session: 3` at ~1272 already correct),
  `software/app/game/character.py` (docstring ~line 39),
  engine/websocket session lifecycle (verify new-session reset; add test if absent).
  Do: add "Sparks do not carry over. You start every session with 3." to III.1;
  propagate to every listed mirror.
  Register: `end a session with 2-4 unspent Sparks` (and the en-dash variant).
  Accept: `grep -rn "unspent Spark" player_handbook mm_manual software/facets`
  returns only reset-consistent text; lifecycle test green.

- [x] **T2.2 — Magic-Spark fold + ceiling rewrite (P-1, P-9, P-3, D8).**
  Files: `player_handbook/II.3_Magic.md` (delete "Pushing scope" ~line 178; rewrite
  §Sparks and Magic to the two rules of DESIGN §3.1; rewrite the ceiling sentences
  at ~99 and ~184 to "Reach-Sparks cannot move a Broad working's difficulty;
  dice-Sparks work normally"), `player_handbook/Glossary.md` (Spark/Broad entries),
  `mm_manual/MM5_Quick_Reference.md` (magic card, if it restates Spark-magic rules),
  `software/facets/base/facet.yaml` + engine (add/verify eligibility: pre-Technique
  Significant purchase; Focused Major ease; Broad reach-block — TDD if the engine
  models Spark-reach at all; if it doesn't, add the two eligibility functions with
  tests so the app can enforce silently).
  Register: `Pushing scope`; `natural ceiling`; `pushed beyond Very Hard under any
  circumstances`; `Their ceiling is their ceiling`.

- [ ] **T2.3 — Difficulty precedence text + taxonomy relocation (C-3, C-4, K-8, D2).**
  Files: `player_handbook/III.1_Core_Resolution.md` (§Difficulty — new precedence
  paragraph per DESIGN §3.2; Technique trigger taxonomy reduced to one sentence),
  `player_handbook/II.4_Character_Creation_Facets.md` (§Reading the Entries receives
  the taxonomy), `player_handbook/II.5_Character_Creation_Backgrounds.md` (Specialty
  definition gains the shared-cap sentence), `player_handbook/Glossary.md`
  (Technique, Specialty entries), `mm_manual/MM5_Quick_Reference.md` (combat card
  precedence line).
  Do: text only (engine is T2.4). Read the II.2 vignette and QS pregen Specialty
  lines afterward and confirm no example now demonstrates a double relabel.
  Register: the III.1 taxonomy paragraph's distinctive clause (pick after reading,
  e.g. `something the roll already carries`).

- [ ] **T2.4 — Engine precedence order (TDD).**
  Files: `software/app/game/engine.py` (`_step_difficulty_*`, resolve paths),
  `software/app/game/combat.py` (`target_strike_difficulty`,
  `maneuver_target_difficulty`, Support handling), tests.
  Do: red first — ≥4 tests: Easy-tag overrides base downward; Technique+Specialty
  share one step (two sources → one step); Support step applies after; ladder
  clamps both ends. Then implement base → tag override → single character step →
  Support step → clamp.
  Accept: new tests green; existing combat/magic tests green or updated with
  reasons in LOG.

- [ ] **T2.5 — Group rolls vs Threat Clocks (C-5).**
  Files: `player_handbook/III.2_Adventuring.md` (§Hazards), MM5 group-roll card if
  it mentions hazards.
  Do: "A group roll advances a Threat Clock at most once, keyed to the group's
  overall result."

- [ ] **T2.6 — 7–9 narration sequencing (C-7, D3).**
  Files: `player_handbook/III.1_Core_Resolution.md` (§Partial Success),
  `player_handbook/II.2_Character_Creation_Attributes.md` (duplicated outcome table
  / any restatement), `mm_manual/MM5_Quick_Reference.md`.
  Do: "the MM names the cost before narrating the success" — remove the
  decide-how-to-proceed implication everywhere it is mirrored.
  Register: `before the player decides how to proceed`.

- [ ] **T2.7 — Fixed-pairs principle (C-9).**
  Files: `player_handbook/II.6_Character_Creation_Skills.md` (§Using Skills).
  Do: one sentence; Strike named as the explicit exception; verify QS-4's Strike
  line and III.3 §Strike agree with the phrasing.

- [ ] **T2.8 — WS-2 sweep.** Register grep; Glossary diff review (every entry
  touched this WS reread against its body-text source); regenerate; full suite.

## WS-3 — Combat mechanics (branch `feat/combat-open-and-tempo`)

- [ ] **T3.1 — Open tag engine (K-6, D4; TDD).**
  Files: `software/app/game/combat.py` (`can_apply_rider`, `rider_tier_eligible`,
  `apply_condition`, `target_strike_difficulty`), `software/app/facets/schema.py`
  (enemy state; `tier1_immunity` → deprecation warning, pattern of `endurance`),
  `software/facets/base/facet.yaml` (`strike_outcomes` ~1634), tests
  (`test_enemy.py`, combat tests).
  Do: red first — Open applied on 10+ vs enemy (attacker's option), Easy-to-Strike
  for everyone, cleared only by enemy spending its action, PvP tier outcomes
  unchanged, `tier1_immunity` load warns. Then implement.

- [ ] **T3.2 — Open tag body text (K-6, K-12).**
  Files: `player_handbook/III.3_Combat.md` (§Strike outcomes vs enemies, §Named
  NPCs, any conditions-on-enemies passage — read the whole chapter for "Condition"
  applied to an enemy), `mm_manual/MM5_Quick_Reference.md` (strike card),
  `player_handbook/Glossary.md` (new Open entry; Condition entry scoped to
  characters).
  Do: replace the five-option menu vs enemies with Open + player narration + the
  visible enemy clear action.
  Register: `a Tier 1 or Tier 2 Condition of your choice` (confirm exact wording in
  situ first).

- [ ] **T3.3 — Open tag transport.**
  Files: `software/app/api/websocket.py` (enemy tracker events carry Open state),
  static js that renders enemy conditions (`play.js`, `components.js`), tests
  (≥3: set, clear, broadcast).

- [ ] **T3.4 — Archive Guardian + agentic scenarios + bestiary regen.**
  Files: `enemies/archive_guardian.fof` (remove `tier1_immunity`; re-express
  Reduced Mode per DESIGN §4.1 without it),
  `software/tools/agentic_playtest/scenarios.py` (references it),
  `mm_manual/MM1_Encounters_and_Enemies.md` (immunity documentation),
  regenerate bestiary stat blocks + `bestiary/Finding_Aids.md`.
  Accept: `grep -rn "tier1_immunity" enemies/ mm_manual/ bestiary/ facets/` → only
  the schema deprecation path remains.

- [ ] **T3.5 — Uncontested-exchange rule + Withdrawn cap (K-2, D5).**
  Files: `player_handbook/III.3_Combat.md` (new rule + Withdrawn "up to your pool"),
  `mm_manual/MM5_Quick_Reference.md` (card line),
  `mm_manual/MM1_Encounters_and_Enemies.md` (Mook-only encounters must carry a
  clock/objective), `software/facets/base/facet.yaml` (`recovery_withdrawn` ~1586
  gains pool cap), `software/app/game/combat.py`
  (`withdrawn_recovery_amount` clamp; `exchange_uncontested()` helper),
  `software/app/api/websocket.py` (MM prompt event on uncontested exchange), tests
  (≥3 clamp/helper/event).

- [ ] **T3.6 — Cut budget & multiplier tables (K-5, D6).**
  Files: `mm_manual/MM1_Encounters_and_Enemies.md` (§Encounter Budget, lines
  ~158–183, tables MM1-5/MM1-6 + caveat prose), `mm_manual/MM5_Quick_Reference.md`
  (~lines 311–315), `docs/DECISIONS.md` (historical record + Series 9 citation),
  `player_handbook/Glossary.md` + `mm_manual/MM3_Campaign_Design.md` if either
  references the budget (grep `[Bb]udget` across both books).
  Do: also add the MM1 "sharpest dial — one Mook is one difficulty band
  (76% → 47% → 20%)" sentence (K-3). Keep TR, TR minimums, Recipe Table,
  actor-count rule. Renumber/regen `List_of_Tables.md`; check
  `test_docs_consistency.py` table invariants.
  Register: `x multiplier` in the budget formula wording (confirm exact string).

- [ ] **T3.7 — `defense_modifier` retirement (K-11).**
  Files: `software/app/facets/schema.py` (deprecation warning on load),
  all shipped `enemies/*.fof` (remove the field — ~16 files; TR values unchanged),
  `mm_manual/MM1_Encounters_and_Enemies.md` (drop from minimal block and `.fof`
  format doc), `spec/examples/*.fof` if present, `software/tests/test_enemy.py`.
  Do NOT touch `playtest/**` (historical archives).
  Accept: `grep -rln "defense_modifier" enemies/ mm_manual/ spec/ facets/` → empty;
  loader-warning test green; bestiary regenerated.

- [ ] **T3.8 — Enemy posture: triggers instead of ceremony (K-4, K-10, D12).**
  Files: `player_handbook/III.3_Combat.md` (§Postures: enemy blind-reveal dropped —
  the MM states enemy stance; PC-side blind declaration explicitly kept; Insight
  pre-read named as the counter-tool), `mm_manual/MM1_Encounters_and_Enemies.md`
  (conduct-field `triggers:` documentation), one shipped enemy
  (`enemies/city_watch_sergeant.fof` or `veteran_soldier.fof`) gains a worked
  trigger, `mm_manual/MM5_Quick_Reference.md` (posture card), Glossary (Posture).
  Register: the enemy-reveal ceremony's distinctive clause (read III.3 first;
  likely `player characters and significant antagonists alike`).

- [ ] **T3.9 — Enemy Techniques + incoming-Condition selection (K-9, K-7).**
  Files: `mm_manual/MM1_Encounters_and_Enemies.md` (three mechanical templates per
  DESIGN §4.4 with stat-block-ready `techniques:` entries),
  `player_handbook/III.3_Combat.md` + MM5 (one sentence each: MM chooses the
  incoming Condition; repeating a carried type is the telegraphed finisher).
  Constraint: templates are setting-agnostic mechanics — no new lore, no names
  implying Shattered Origin canon.

- [ ] **T3.10 — Paper fallback + Intercept card (K-13, K-12).**
  Files: `player_handbook/III.3_Combat.md` (sidebar: armor = N per-scene
  checkboxes; first-reaction = flip a token, clear at exchange end),
  `mm_manual/MM5_Quick_Reference.md` (Intercept row gains once-per-exchange and
  "the protected ally decides who steps in").

- [ ] **T3.11 — Sim campaign (DESIGN §4.7).**
  Files: `software/tools/combat_sim.py` (drives `combat.py` ONLY — the iron law),
  `research/simulation_log.md` (append), `mm_manual/MM1` + `MM5` Recipe Tables
  (same commit, only if a row moves a band).
  Do: rerun Series 9 Part D rows (3 seeds × 200/row) + A5 (15-Mook Withdrawn
  cycling) + boss-median check under Open/uncontested/triggers.
  Accept: bands within ±10pp or tables updated; A5 no longer 98%-by-cycling; boss
  median 2–4 exchanges. Escalate to Planner if any acceptance fails twice.

- [ ] **T3.12 — WS-3 sweep.** Register grep; regenerate bestiary + PHB lists; full
  suite; reread MM5 combat cards against final III.3 (rule 5).

## WS-4 — Magic & advancement (branch `feat/magic-advancement-arcs`)

- [ ] **T4.1 — Casting adds tradition skill (P-2, D7). ⛔ BLOCKED on DESIGN §9.1**
  (Channeling → Attune, Resonance → Lore — user must confirm the mapping).
  Files: `player_handbook/II.3_Magic.md` (§Rolling Magic + BOTH worked examples
  re-rolled showing the skill), `player_handbook/Glossary.md`,
  `mm_manual/MM5_Quick_Reference.md` (magic card),
  `software/facets/base/facet.yaml` (magic def: tradition→skill),
  `software/app/game/engine.py` (`resolve_magic_roll` adds rank; TDD ≥3),
  `software/app/api/websocket.py` (magic roll handler),
  `characters/Zahna.fof` (verify Lore feeds her casting; numbers in QS/II.3
  examples consistent), `player_handbook/Quick_Start.md` (pregen spell lines gain
  the skill — coordinate format with T5.1).
  Accept: an example roll in II.3, the QS pregen line, and an engine test all show
  the same total for the same character.

- [ ] **T4.2 — Second Domain expiry (P-7, D9).**
  Files: `player_handbook/II.4b` + `II.4c` (both Technique entries; Choose-field
  note that Focused suffers the penalty least while it lasts),
  `software/facets/base/facet.yaml` (`second_domain_mind` ~853, `second_domain`
  ~1163: expiry-at-next-Facet-level field), engine difficulty calc (TDD: penalty
  applies, then lifts on level gain), `software/tests/test_ascendant_domain.py` +
  `test_character.py`, `player_handbook/Glossary.md`,
  `software/app/static/js/builder.js` + `app.js` (grep `Second Domain` — update
  any displayed penalty text).

- [ ] **T4.3 — Points economy: banking + training mark (P-5, D10).**
  Files: `player_handbook/II.4_Character_Creation_Facets.md` (rule ~line 61 and the
  Zulnut example ~line 71 — the example must demonstrate banking, not forfeiture),
  `player_handbook/Glossary.md` (Skill Point entry ~106: "unspent points do not
  carry over" dies), `software/facets/base/facet.yaml` (advancement),
  engine `spend_skill_point` path (TDD: bank ≤2; 1 training mark to unused
  Primary-Facet skill; both capped), websocket handler + tests,
  `software/app/static/js/builder.js` if it enforces used-only/forfeit.
  Register: `unspent points are lost`; `unspent points do not carry over`.

- [ ] **T4.4 — Facet-level counting sentence (P-6).**
  Files: `player_handbook/II.4_Character_Creation_Facets.md` (§Facet Levels:
  "Ranks granted at character creation count toward career advances but not toward
  Facet levels"; verify Table II.4-3 benchmark prose no longer misleads),
  `software/facets/base/facet.yaml` + engine counters (verify existing behavior
  matches; add the missing test either way).

- [ ] **T4.5 — Never Surprised → warning beat (P-8, D11).**
  Files: `player_handbook/II.4b_Character_Creation_Facet_Mind.md`,
  `software/facets/base/facet.yaml` (`never_surprised` ~664),
  `player_handbook/Glossary.md`, tests referencing it (grep
  `never_surprised` in `software/tests/`).
  Register: the entry's absolute clause (`you automatically succeed` scoped — use
  a longer unique substring from the entry).

- [ ] **T4.6 — Casting-curve spot-checks (DESIGN §5.6; after T4.1).**
  Files: sim tooling (shared rules module only), `research/simulation_log.md`.
  Accept: pre-Technique Minor success unchanged-or-better; curves recorded for
  Focused + Broad at ranks 0/2/4.

- [ ] **T4.7 — Four prose notes (P-4, C-10, C-12, C-8).**
  Files: `player_handbook/II.4` + `II.5` (mage's first Technique owned as
  formalization; first free choice at level 2), `player_handbook/III.1` (Graceful
  Fail confirm calibration, cross-ref the II.2 award vignette),
  `player_handbook/III.2` (clock-janitor MM sidebar),
  `mm_manual/MM4_Running_the_Table.md` (Luck/Spirit MM-invoked-roll note).

- [ ] **T4.8 — WS-4 sweep.** Register grep; Glossary reread; regenerate; full
  suite; verify II.3 examples, QS pregens, Zahna.fof, and facet.yaml all state the
  same casting math (the classic four-way drift point).

## WS-5 — Apparatus & polish (branch `feat/apparatus-polish`; after WS-2/3/4 merge)

- [ ] **T5.1 — Quick Start pregens (C-1a/c/d).**
  Files: `player_handbook/Quick_Start.md`.
  Do: Major Attributes line (three modifiers, derived per II.2 Table II.2-2 — show
  your derivation in the LOG); spell line resolved per pregen (with skill, per
  T4.1); strip "(Novice, 1 mark)", scope caveats, secondary-skill annotations.
  Accept: every number on a pregen sheet is derivable from chapters II.2–II.6; a
  reader needs no term the document doesn't define.

- [ ] **T5.2 — QS-4 combat primer (C-1b).**
  Files: `player_handbook/Quick_Start.md`.
  Do: replace Postures/Conditions rows with the five-line primer (exchange,
  reaction, posture — one clause each) + "everything else: Chapter III.3 — the
  same 2d6 roll." Every remaining QS-4 term must be defined in-document or
  pointered.

- [ ] **T5.3 — "Endurance Pool" qualifier (C-6, D13).**
  Files: everywhere the POOL is meant: `player_handbook/III.3_Combat.md`,
  `Quick_Start.md`, `Appendix_Character_Sheet.md`, `Glossary.md`,
  `mm_manual/MM5_Quick_Reference.md`, `software/facets/base/facet.yaml` (display
  name only — no identifier rename), app labels (`grep -n "Endurance"
  software/app/static/js/*.js software/app/static/index.html`).
  Do: build the checklist from `grep -rn "Endurance" player_handbook mm_manual |
  grep -v "skill\|rank"` and disposition every hit (pool → "Endurance Pool";
  skill stays bare). Record the disposition list in the LOG.

- [ ] **T5.4 — One word: Prismatic (P-11, D14).**
  Files: `player_handbook/II.3_Magic.md` (12 hits), `Appendix_Magic_Domains.md`
  (8), `II.4b`/`II.4c` (2+2), `II.1` (1), `Glossary.md` (2),
  `software/facets/base/facet.yaml` (5), MM5 if present, static js (grep `Broad`).
  Do: "Prismatic" player-facing; "Broad" survives in exactly one definitional
  sentence in II.3. Table headers II.3-2/3 updated; regen Lists/Index.
  Register: `Broad (Prismatic)`.

- [ ] **T5.5 — Career Advances off the paper sheet (P-13).**
  Files: `player_handbook/Appendix_Character_Sheet.md`, `II.1` (sheet table),
  `II.4` (Table II.4-3 moves to `mm_manual/MM3_Campaign_Design.md`), `Glossary.md`
  (entry stays — it's still a live app/MM concept), MM1 (Party Strength still sums
  `career_advances` — unchanged, verify wording), `test_docs_consistency.py`
  (references), regen Lists/Index. App keeps the field.

- [ ] **T5.6 — Weapon vocabulary join (P-14).**
  Files: `player_handbook/IV.1_Equipment.md` (Table IV.1-1 gains a type column
  with examples: longsword = standard / blades), `II.4a` cross-ref check.

- [ ] **T5.7 — II.3 signpost + domain table consolidation (P-12).**
  Files: `player_handbook/II.3_Magic.md` (top-of-chapter "skip ahead unless your
  concept is magical" note), `Appendix_Magic_Domains.md` (quick-ref tables
  consolidated here; II.3 keeps prose + pointer), regen Lists/Index.
  Accept: no domain data exists in two places with independent wording.

- [ ] **T5.8 — Background pair divergence (P-10). ⛔ BLOCKED on DESIGN §9.2.**
  Do first: draft the two skill-slot diffs (Road Guard/Dockworker; Guild
  Apprentice/Hedge Scholar) as a proposal in the LOG for user approval — skill
  slots only, no new fiction. On approval: `II.5`, `software/facets/base/facet.yaml`
  (backgrounds block ~1771+), background-validation tests, any affected pregen.

- [ ] **T5.9 — Modifier-first rendering (C-11).**
  Files: `player_handbook/Appendix_Character_Sheet.md`,
  `software/app/static/js/components.js` (sheet rendering leads with the modifier;
  rating shown as secondary), tests if rendering is tested.

- [ ] **T5.10 — Quick-ref recompression audit (protocol rule 5, verification).**
  Files: `mm_manual/MM5_Quick_Reference.md`, `Quick_Start.md` QS-4, in-chapter
  quick-ref boxes.
  Do: line-by-line against final body text; fix divergences; confirm II.2's
  duplicated tables match III.1 verbatim (default: keep them — DESIGN §9.3).
  LOG a table: quick-ref line → canonical source section.

- [ ] **T5.11 — WS-5 sweep.** Full register grep; regenerate everything; full
  suite; INV-9..15 green.

## WS-6 — App features (branch `feat/app-fun-ease`)

- [ ] **T6.1 — Band computation backend (K-3; TDD).**
  Files: encounter model/logic + `software/tests/test_encounter.py`.
  Do: `compute_band(enemies, party_strength)` from Recipe-Table logic
  (actor-count of Named/Boss + Mook steps). ≥3 tests keyed to published sim rows.

- [ ] **T6.2 — Band display + spawn warning.**
  Files: `software/app/api/websocket.py` (band in encounter/tracker payloads),
  `software/app/static/js/builder.js` (live band in encounter builder),
  `play.js` (warning badge when a mid-combat spawn crosses a band), tests.

- [ ] **T6.3 — Spark-flow nudge (C-2 app-side).**
  Files: session state (per-player last-earn/last-spend), websocket MM-only prompt
  event, `play.js` MM display, tests (≥3).

- [ ] **T6.4 — Enemy posture panel (K-10).**
  Files: enemy tracker (posture field), auto-labels: reaction difficulty players
  face (Table III.3-9) + Strike difficulty hint, conduct-trigger text display;
  websocket + `play.js`/`builder.js`; tests (≥3).

- [ ] **T6.5 — Printable sheet artifacts.**
  Files: printable sheet template(s): armor checkboxes per scene, "Endurance
  Pool" label, modifier-first — consistent with T5.3/T5.9.

- [ ] **T6.6 — WS-6 close.** Full suite; report pass/fail counts in LOG.

## WS-7 — Global close-out

- [ ] **T7.1 — Global contradiction audit.**
  Do: (a) full `RETIRED_PHRASES` run — must be empty outside excluded archives;
  (b) cross-book keyword sweep for every changed rule (Sparks, Open, Withdrawn,
  precedence, banking, Prismatic, Endurance Pool, casting skill) — each hit
  dispositioned in the LOG; (c) Glossary read END-TO-END against body text (it
  mirrors ~every changed rule); (d) `docs/DECISIONS.md` gains D1–D14 from DESIGN
  §8; (e) regenerate all generated files one final time; (f) full suite + INV
  suite; report counts.
  Accept: zero undispositioned hits; suite green; LOG closed with a summary.

---

**Blockers to resolve before their tasks:** §9.1 casting-skill mapping (T4.1);
§9.2 Background divergence approval (T5.8). Everything else is unblocked.
**Escalation:** per the house protocol — 2 failures on a task → `## ESCALATION`
block in the LOG, stop, recommend Planner.
