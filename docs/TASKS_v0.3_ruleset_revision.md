# TASKS — v0.3 Ruleset Revision

**Tier:** Planner (Opus) output — Worker (Sonnet) executes
**Design:** `docs/DESIGN_v0.3_ruleset_revision.md`
**Brief:** `docs/BRIEF_v0.3_ruleset_revision.md`
**Log:** `docs/LOG_v0.3_ruleset_revision.md` (Worker creates on first task)

## Worker protocol

1. Read `DESIGN` §-references cited by your task. Do **not** read the whole repo.
2. Pick **one** task. TDD: write the test, watch it fail, implement, watch it pass.
3. Update this file (mark `[x]` done / `[!]` blocked) and append to `LOG_v0.3_ruleset_revision.md`.
4. **Stop and report.** Do not start the next task without confirmation.
5. Escalate to Planner after 2 failed attempts, or if the task spec is ambiguous.

Sync order per `CLAUDE.md`: `facet.yaml` → engine / character model → websocket events → tests → commit referencing the PHB section.

**Baseline:** 721 tests green on `feature/data-driven-dice`.

---

## WS-C — Consolidation pass (D5) — **DO FIRST**

Target: one commit, message `Consolidate contradictory rules (PHB D5 ledger)`.
DESIGN §7. Do not touch armor text (WS-A owns it) or "Advancement at a Glance" (WS-B owns it).

- [x] **C1 — Repo rules into CLAUDE.md.** *(two clauses)*
  Files: `CLAUDE.md`.
  Add under *Software-PHB Synchronization*:
  1. Quick references may only **compress** canonical text, never paraphrase it; any rules change must update body text, all quick refs, `facet.yaml`, and the engine in one commit.
  2. *(Brain, Q3)* **The simulator may only drive `app/game/combat.py`. It must never re-implement a rule.** This is the process guarantee that F1 — combat resolution implemented twice, diverging silently, invalidating every recorded number — cannot recur.
  Accept: both rules present; no other section altered.

- [x] **C2 — Ledger row 1: pre-technique magic.**
  Files: `player_handbook/II.5_Character_Creation_Backgrounds.md` (stale text). Verify-only: `II.3`, `MM5_Quick_Reference.md`, `Quick_Start.md`, `software/facets/base/facet.yaml:995-999`.
  Canonical: Minor scope only, **no** difficulty penalty.
  Accept: II.5 says no penalty; the four verify targets already agree (report any that don't — do not fix silently, add a task).

- [x] **C3 — Ledger row 2: Broken threshold — TEXT.**
  Files: `player_handbook/III.3_Combat.md` (quick ref), `mm_manual/MM5_Quick_Reference.md`.
  Canonical: a second Tier 2 Condition **of the same type** escalates to Broken. Staggered and Cornered coexist. Both files currently say "same or different".
  Accept: both files state same-type; no other rule text touched.

- [x] **C4 — Ledger row 2: Broken threshold — CODE.** *(TDD; DESIGN §1 F6)*
  Files: `software/app/api/websocket.py:680-684`, `software/tests/test_websocket.py`.
  Change `_handle_apply_condition` to escalate only when the incoming Tier 2 condition id **already exists** on the character. Read the Tier 2 id set from `ruleset.combat.conditions.tier2`, not the hardcoded `{"staggered", "cornered"}` literal.
  Tests (3): same-type second Tier 2 → `broken`; different-type second Tier 2 → both present, no `broken`; third application of an already-present type → `broken`.
  Accept: 3 new tests pass; full suite green.

- [x] **C5 — Ledger row 3: Parry has no counter.**
  Files: `player_handbook/III.3_Combat.md` (quick ref), `mm_manual/MM5_Quick_Reference.md`.
  Canonical: Parry outcomes are identical to Dodge. Both files invented a 10+ counter-attack. Delete it.
  Accept: no counter-attack language remains in either file. Body text of III.3 already correct — verify, don't rewrite.

- [x] **C6 — Ledger row 4: Strike formula and weapons.**
  Files: `player_handbook/III.3_Combat.md` (Strike + Parry sections), `mm_manual/MM5_Quick_Reference.md`, `player_handbook/Quick_Start.md`.
  Canonical: weapon category sets the attribute (per `IV.1_Equipment.md`); skill is Combat for melee/unarmed, Finesse for ranged; the formula generalises to **"2d6 + weapon attribute + relevant skill"**. The engine is already permissive (`websocket.py:473-479`) — no code change.
  Accept: all three files state the general formula; no file hardcodes Strength+Combat as the only Strike.

- [x] **C7 — Ledger rows 5 & 6: PvP ties and attribute label.**
  Files: `mm_manual/MM5_Quick_Reference.md`.
  Canonical: on a PvP tie both sides achieve partial success (per `III.1_Core_Resolution.md`) — MM5 currently says "ties go to defender". Attribute rating 1 is labelled **"Weak"** (per `facet.yaml:102`) — MM5 says "Poor".
  Accept: both corrected; `III.1` and `facet.yaml` unchanged (they are already canonical).

- [x] **C8 — Ledger row 7: ghost text.**
  Files: `player_handbook/III.3_Combat.md`.
  Delete the "Spent ally" clause from Intercept (Spent was cut in the 2026-03-04 simplification). Fix the Maneuver wording to *"rolls **against** the target are Easy"*.
  **Defer** the MM1 phase-trigger re-key to task A7 — it depends on Resolve existing.
  Accept: no reference to Spent, Weary, Bleeding, or Exposed survives in III.3; Maneuver reads correctly.

- [x] **C9 — Ledger row 8: example-character continuity.**
  Files: `player_handbook/II.3_Magic.md`, `player_handbook/II.4_Character_Creation_Facets.md`, `player_handbook/II.5_Character_Creation_Backgrounds.md`, `player_handbook/III.3_Combat.md`.
  Source of truth: `characters/Zahna.fof`, `characters/Mordai.fof`, `characters/Zulnut.fof` and `references/phb-examples.md`.
  - Zahna: Inscription domain, Knowledge attribute, Spirit 2, pronoun **he**. Rewrite the II.3 "Fire mage" example accordingly — it currently describes a character who does not exist.
  - Zulnut: Wandering Disciple (custom background), pronoun **he**. Fix the II.5 closing analysis and the II.4 pronoun.
  - Mordai: Endurance Novice +1 mark, Endurance pool 5. Fix the III.3 example pools.
  Accept: no invented details introduced (CLAUDE.md iron law); all four files agree with `characters/*.fof` and `Quick_Start.md`.

- [x] **C10 — Ledger row 9 (new): Facet level counting.** *(DESIGN §1 F3)*
  Files: `player_handbook/II.4_Character_Creation_Facets.md:89`.
  The sentence *"Facet level advances outside your Primary Facet ... do not count toward your Major Advancement threshold"* contradicts §Major Advancement at lines 207–209, which counts them and gives a worked example. Canonical: **cross-Facet levels DO count.** Delete or rewrite line 89.
  The corresponding code fix is **B3** — do not attempt it here.
  Accept: II.4 internally consistent; a `continuity-check` over II.4 reports no Facet-level contradiction.

- [x] **C11 — Consolidation verification.**
  Run `/continuity-check` across `player_handbook/`, `mm_manual/`, `Quick_Start.md`.
  Accept: no contradiction remains among the 9 ledger rows. Full test suite green. Commit WS-C as one commit.

---

## WS-A0 — Combat extraction (blocks WS-A) — DESIGN §2.1, §3

- [ ] **A0.1 — Characterization tests for current combat semantics.** *(no behaviour change)*
  Files: `software/tests/test_combat_characterization.py` (new).
  Pin the **simulator's** semantics (`tools/combat_sim.py`), because `research/simulation_log.md` was measured under them: `armor_downgrade` (light affects Tier 2 only; heavy affects Tier 3 only), `apply_condition` stacking, `cleanup_end_of_exchange`, `is_zero_end_absorb` escalation, reaction Endurance costs with posture modifiers.
  Use 5 fixed seeds; assert exact end-state (conditions list, Endurance, out/alive), not aggregate win rates.
  Accept: ≥ 12 tests, all passing against unmodified code. This is the **G0 gate baseline**.

- [ ] **A0.2 — Create `app/game/combat.py`.**
  Files: `software/app/game/combat.py` (new), `software/tests/test_combat.py` (new).
  Move — do not rewrite — the rules functions into pure, synchronous form per DESIGN §2.1: `resolve_strike`, `resolve_reaction`, `apply_condition`, `armor_downgrade`, `end_exchange`. No async, no session objects, no I/O. Every constant read from `MergedRuleset` (reaction costs, Tier-1 ids, recovery amount) — delete the hardcoded fallbacks at `websocket.py:559` and `websocket.py:681,720,725`.
  Define a structural `Combatant` protocol satisfied by both `Character` and `Enemy`.
  Tests: ≥ 3 per public function (happy path, edge case, error).
  Accept: A0.1 characterization tests still pass, now importing from `combat.py`.

- [ ] **A0.3 — Rewire both consumers; delete the duplicates.**
  Files: `software/app/api/websocket.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py`.
  `websocket.py` handlers become thin: auth → validate → call `combat.py` → persist → broadcast. `combat_sim.py` keeps only policy (`choose_pc_posture`, `choose_pc_target`, `should_spend_spark`, `should_press`, `choose_pc_reaction`, `should_enemy_react`) and statistics. Delete `combat_sim.resolve_pc_strike`, `resolve_enemy_attack`, `armor_downgrade`, `apply_condition`, `_apply_broken`, `cleanup_end_of_exchange`.
  Add a **parity test class**: one seeded scenario driven through `combat.py` directly and through the WebSocket handler, asserting identical end-state. This is the permanent guard against F1.
  Accept: **G0** — on the 5 fixed seeds from A0.1, the post-refactor run reproduces the pre-refactor end-state **exactly** (conditions list, Endurance, out/alive). This is the criterion, not a win-rate band: at n=200 and p≈0.5, ±3pp is about one standard error, so it would pass real regressions and fail clean refactors by chance *(Brain, EF5)*. The ±3pp aggregate check against `research/sim_result_V6.md` applies **only** if the refactor legitimately changed RNG draw order — if you invoke it, document in `LOG` why draw order changed. Full suite green (~745 tests).

- [ ] **A0.4 — Mark the superseded simulation corpus.** *(Brain ruling, Q3 — do not delete)*
  Files: `research/simulation_log.md`.
  Every PC-side win rate, Broken rate, and lethality figure was measured under simulator-only armor semantics plus the 0-Endurance house rule that A6 retires. The chicken baselines and the Encounter Budget difficulty multipliers fall with them.
  Mark each affected Series `**SUPERSEDED (v0.2 semantics)**` with a one-line reason and a pointer to DESIGN §4.3. **Do not delete them** — they are the record of how the error was found.
  Explicitly **not** superseded: enemy-side Threat Rating arithmetic, which survives by construction of the migration map (`resolve := old durability_value`), not by luck.
  Accept: no PC-side figure in the log is readable as current; G2/G4 have a clean slate; the enemy-side TR notes are untouched.

---

## WS-A — Enemy durability & armor (D1 + D2) — DESIGN §4

Requires WS-A0 complete. **No PHB prose until G1 and G2 pass.**

- [ ] **A1 — Schema + `facet.yaml`: Resolve and armor.**
  Files: `software/facets/base/facet.yaml`, `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`, `software/tests/test_facet_loading.py`.
  Add under `combat:`
  ```yaml
  enemy_durability:
    strike_depletion: {full_success: 2, partial_success: 1, failure: 0}
    armor_resolve_bonus: {none: 0, light: 1, heavy: 2}
    mook_removed_on: partial_success        # armored mook: full_success
    armored_mook_removed_on: full_success
  armor:
    light: {downgrades_per_scene: 2, tiers_reduced: 1}
    heavy: {downgrades_per_scene: 4, tiers_reduced: 1}
  ```
  The key is `downgrades_per_scene` — **not** `_per_exchange`, **not** `_per_fight` *(Brain, Q2: the budget resets when the scene ends; a fight is a combat scene; two fights in one scene share the budget)*. The values 2 and 4 are G2 tuning knobs, not literals.
  Replace the existing `armor.light.downgrades` / `armor.heavy.downgrades` keys. Add typed sub-models (`EnemyDurabilityDef`, rewrite `ArmorEntryDef`) with docstrings, matching the existing schema style.
  Accept: schema validates; ≥ 3 loading tests; full suite green.

- [ ] **A2 — `Enemy` model: Resolve, TR re-key, back-compat.** *(TDD)*
  Files: `software/app/game/enemy.py`, `software/tests/test_enemy.py`.
  - `endurance` → `resolve`; `endurance_current` → `resolve_current`; `init_combat` sets `resolve_current = resolve` for non-Mooks.
  - `calculate_tr()`: `durability_value = 0` for Mook, else `= resolve`. Delete the 7-branch Endurance ladder. Keep tier minimums (mook 1 / named 8 / boss 12).
  - `from_fof`: when `resolve` is absent but `endurance` is present, map via DESIGN §4.1 (≤2→1, 3–4→2, 5–6→3, 7–8→4, 9–10→5, 11–12→6, 13+→7) and emit `DeprecationWarning`. `to_fof` writes only `resolve`.
  - Add `phases: list[PhaseDef]` with `resolve_threshold: int` and `description: str`.
  Tests (≥ 9): TR preserved for Sergeant (8) and Veteran Soldier (10); Guardian recomputes to **14** (was 16 — `special` was double-counted; see DESIGN §12 Q3); legacy `endurance` read emits the warning and maps correctly; `resolve` key round-trips; Mook durability is 0; tier minimums hold.
  Accept: all tests pass; full suite green.

- [ ] **A3 — Migrate `enemies/*.fof`.**
  Files: `enemies/chicken.fof`, `harbor_thug.fof`, `city_watch_sergeant.fof`, `veteran_soldier.fof`, `archive_guardian.fof`; `spec/examples/encounter-example.fof`.
  Replace `endurance:` with `resolve:` per the map. Sergeant 6→3, Veteran 7→4, Guardian 10→5. Mooks: remove the key. Update the inline `tr:` comments to the new arithmetic. Set Guardian `tr: 14` and add a `phases:` block with `resolve_threshold: 2`.
  Accept: every file loads through `Enemy.from_fof` without a `DeprecationWarning`; `calculate_tr()` matches the published `tr:` in each file.

- [ ] **A4 — `combat.py`: Resolve depletion and rider Conditions.** *(TDD)*
  Files: `software/app/game/combat.py`, `software/tests/test_combat.py`.
  - `apply_resolve_damage(enemy, outcome_tier, ruleset)` → depletes per `strike_depletion`; Resolve 0 = defeated; emits phase-change when a `resolve_threshold` is crossed.
  - `resolve_strike` against an enemy: full success may additionally impose one attacker-chosen Tier 1 or Tier 2 Condition as a **rider**. Riders never escalate to Broken. Delete enemy-side `_apply_broken` entirely.
  - **A rider must have its normal table effect** *(Brain, EF1 — riders that do nothing are dead text, the disease D3 cures elsewhere).* A Tier 2 rider (Staggered / Cornered) makes subsequent Strikes against that enemy **Easy**. Tier 1 riders apply their normal effect and clear at end of exchange as usual. This is what makes the 10+ choice real: deplete 2 Resolve now, or set up your allies.
  - Mook: removed on any success; armored Mook on full success only. No Resolve pool, no Conditions.
  - Enemy armor adds flat Resolve at `init_combat` (light +1, heavy +2). Enemy armor does **not** downgrade Conditions.
  Tests (≥ 11): depletion 2/1/0 by tier; phase-change fires exactly once at threshold; rider condition applied on 10+ only; rider never produces Broken; **a Strike against an enemy holding a Tier 2 rider is resolved at Easy**; **a Tier 1 rider clears at `end_exchange` and its effect stops applying**; Mook removal on 7+; armored Mook survives a 7–9.
  Accept: full suite green. **A8's G1 run depends on rider→Easy existing here** — if it is stubbed out, G1 validates the wrong game.

- [ ] **A5 — `combat.py`: PC armor per-scene downgrade budget.** *(TDD; **UNBLOCKED** — Brain approved, BRIEF §Q2)*
  Files: `software/app/game/combat.py`, `software/app/game/character.py`, `software/tests/test_combat.py`.
  Light armor downgrades the first **2** Conditions received per **scene** by one tier (T2→T1, T1→none). Heavy downgrades the first **4**. Track `armor_downgrades_remaining` on the combatant; initialise at `combat_start`, decrement on use, **do not reset in `end_exchange`**. Reset at end of scene. Two fights inside one scene share the budget.
  Values live in `facet.yaml` (`armor.light.downgrades_per_scene: 2`, `heavy: 4`) — G2 tuning knobs, not literals. Say **scene** in code, keys, and tests; never "fight."
  Delete `_downgrade_condition_for_armor` from `websocket.py`.
  **Do not implement the per-exchange variant.** It cannot break an armored PC in a single-enemy boss fight — see DESIGN §4.2. If a per-exchange reset looks natural while writing this, that is the bug, not an improvement.
  Tests (≥ 9): light downgrades hits 1–2 and not hit 3; heavy downgrades hits 1–4 and not hit 5; T1 → absorbed; budget persists across `end_exchange`; budget resets at scene end; heavy strictly outlasts light over 100 seeded fights.
  **The breakability assertion, fully specified** *(Brain, EF6 — "Broken within 6 exchanges" is only deterministic under a stated policy; otherwise you ship a flaky test or quietly weaken it)*: fix the policy to **PC Absorbs every incoming attack** (no Dodge, no Parry, no Intercept) and **the lone Named enemy lands a Tier 2 every exchange** (no reaction, no miss). Under that policy assert Broken by exchange 6 for light armor — and, since the policy is deterministic, assert the *exact* exchange for each of {none, light, heavy}. This is the bug from `research/armored_enemy_breaking_problem.md`; a probabilistic assertion cannot prove it is gone.
  Accept: full suite green.

- [ ] **A6 — Retire the 0-Endurance rule.** *(DESIGN §4.3)*
  Files: `software/app/game/combat.py`, `software/tests/test_combat_characterization.py`, `research/armored_enemy_breaking_problem.md`.
  Remove `is_zero_end_absorb` escalation. Update the characterization tests that pinned it (they were pinning a house rule, not a rule) — replace with tests asserting it is **gone**: an Absorb at 0 Endurance applies the incoming tier unmodified.
  Mark `research/armored_enemy_breaking_problem.md` **RESOLVED** with a pointer to DESIGN §4.1/§4.3 — the problem is dissolved, not solved: enemies no longer have a condition kill-track.
  Accept: no `is_zero_end_absorb` reference remains anywhere; full suite green.

- [ ] **A7 — Phase changes end-to-end.** *(TDD)*
  Files: `software/app/api/websocket.py`, `software/tests/test_websocket.py`, `mm_manual/MM1_Encounters_and_Enemies.md`.
  New broadcast event `enemy_phase_change` carrying `enemy_id`, `phase_index`, `description`. Re-key MM1's phase-change prose to Resolve thresholds (completes ledger row 7, deferred from C8).
  Tests (3): event fires on threshold cross; fires once, not repeatedly; does not fire for enemies without `phases`.
  Accept: full suite green.

- [ ] **A8 — Gate G0 re-verify, then run G1 and G2.** *(DESIGN §5)*
  Files: `software/tools/combat_sim.py`, `research/simulation_log.md`.
  - **G1:** Archive Guardian (Resolve 5, heavy → effective 7) vs 3 starting PCs, n ≥ 200, seeded. **Riders must be modelled live** *(Brain, EF1)*: a Tier 2 rider makes subsequent Strikes against the Guardian Easy. A run that treats riders as inert validates a game nobody will play — the same class of error that voided the corpus in Q3. Pass: median ≥ 3 exchanges, PC win rate 45–55%, zero house rules. **Additionally measure the snowball:** does 2-Resolve depletion plus an Easy rider drive median exchanges below the 3-exchange floor? If so the lever is Boss Resolve, not the rider rule.
  - **G2:** 1 PC × {none, light, heavy} vs Veteran Soldier. Vary the F6 fix (C4) and the F5 removal (A6) as **independent factors** — DESIGN §11 flags the combined over-correction risk. Pass: Broken reachable in all three armor states; `T_broken(heavy) > T_broken(light) > T_broken(none)`; `T_broken(light) ≤ 2 × T_broken(none)`.
  Record both as new Series in `research/simulation_log.md` under its existing conventions.
  **If G1 fails:** Boss Resolve is a `facet.yaml` scalar. Retune within 2–6 and re-run. Do not redesign. Escalate after 2 failed retunes.
  Accept: both gates pass and are logged with seeds, n, and full parameters.

- [ ] **A9 — Gate G3: Aggressive posture knob K1.** *(D8; independent — may run any time after A0.3)*
  Files: `software/tools/combat_sim.py`, `research/simulation_log.md`, `docs/DECISIONS.md`.
  Implement K1 behind a sim flag: the Aggressive posture's +1 reaction surcharge applies to the **first reaction per exchange only**. Compare against baseline: unarmored Endurance-3 PC, Aggressive vs Measured, n ≥ 200.
  Pass (both required): K1 cuts PC Broken rate by ≥ 15% relative, **and** Aggressive retains a net offense edge over Measured (win-rate delta preserved within ±5pp).
  **Adopt only if both hold.** If adopted: `facet.yaml` `postures.aggressive.reaction_cost_modifier_applies: first_reaction_only`, engine, III.3 text. If not: record the negative result in `DECISIONS.md` and leave Aggressive unchanged with a sidebar noting the tradeoff.
  Accept: result recorded either way. A negative result is a passing task.

- [ ] **A10 — Gate G4: recalibrate the Encounter Budget.**
  Files: `software/app/game/encounter.py`, `software/tests/test_encounter.py`, `mm_manual/MM1_Encounters_and_Enemies.md`, `research/simulation_log.md`.
  Re-run the chicken baselines (3/5/7) plus Sergeant and Guardian at each difficulty. Target: Skirmish ~95%, Standard ~75%, Hard ~50%, Deadly ~25% (±10pp). Retune `difficulty_multiplier` and, if needed, `action_economy_multiplier`. Update the MM1 Encounter Recipe Table.
  Accept: measured win rates inside the bands; multipliers no longer flagged "unvalidated" in MM1; ≥ 3 new tests on the changed multipliers.

- [ ] **A11 — PHB III.3 + MM1 prose.** *(only after G1, G2, G4 pass)*
  Files: `player_handbook/III.3_Combat.md`, `mm_manual/MM1_Encounters_and_Enemies.md`, `mm_manual/MM5_Quick_Reference.md`.
  Write: Resolve (enemy durability), Conditions-as-riders **and what a rider does** (Tier 2 rider → Strikes against that enemy are Easy), the amended "Conditions replace HP → **for player characters**" statement (BRIEF Open Question 1), the new armor rules for both sides, Mook removal, phase changes. Update the combat quick-reference card. Update MM1 stat blocks and the enemy `.fof` format documentation.

  **Presentation requirement — armor is two tools, never one rule with an exception** *(Brain, Q4)*. Asymmetry here is ethos-*consistent*, not tolerated: the game is already asymmetric at its root — PCs roll, enemies don't; PCs have stories, enemies have stat blocks. On a stat block, "armor" is a Resolve bonus. On a character sheet, it is a downgrade budget. **One sentence in each place. No cross-reference between them.** The app displays each automatically. Do not write "armor works differently for enemies."

  **Ethos requirement for the quick reference** *(Brain)*. A PC in combat now tracks five things: Endurance, posture, Conditions, Sparks, armor budget. Digital-first makes that acceptable **only if** the quick reference names where each number lives on screen. Write it that way — the card maps numbers to UI locations, not just to rules.

  Per the new C1 repo rule: body text, all quick refs, `facet.yaml`, and engine in **one commit**.
  Accept: `/continuity-check` clean across III.3, MM1, MM5, Quick_Start; no quick ref paraphrases canonical text; the armor sections contain no cross-reference to each other; the quick-ref card locates all five PC numbers on screen.

- [ ] **A12 — Web app: enemy tracker shows Resolve.**
  Files: `software/app/static/js/play.js`, `builder.js`, `components.js`, `software/tests/test_api_enemy.py`.
  Rename Endurance → Resolve in the enemy tracker and enemy builder. Render the Resolve bar and phase markers. Player view shows Resolve; MM view shows Resolve + phases.
  Accept: enemy CRUD tests pass with `resolve`; no `endurance` references remain in enemy-facing UI.

- [ ] **A13 — PT03 boss stress test.** *(the human acceptance test for D1/D2)*
  Files: `playtest/03_boss_stress_test/` (scenario exists).
  Run by the book. Real server rolls, per-player dice, modifier columns reconciled against sheets. Zero house rules permitted — if the table needs one, **that is a finding, not a fix**.
  Accept: boss fight runs ≥ 3 exchanges, is won at approximately Hard rates, requires no house rules. Write `playtest/03_boss_stress_test/results.md`.

---

## WS-B — Advancement math (D3) — DESIGN §6. Independent of WS-A.

- [ ] **B1 — Pacing regression test.** *(TDD — write before B2/B3)*
  Files: `software/tests/test_advancement_pacing.py` (new).
  Encode DESIGN §6.3: at `facet_level_threshold: 5`, Facet levels land at exactly 5, 10, and 15 rank advances; at `major_advancement_threshold: 3`, the first Major fires with Facet level 3. Assert the 100% / 80% / 60% session projections (s12 / s15 / s19) with an explicit SP-efficiency parameter.
  This test is the guard against a future content addition (e.g. a 6th skill) silently changing pacing.
  Accept: tests written and **failing** against current constants. That is the red step — report and stop.

- [ ] **B2 — `facet.yaml` constants.** *(**UNBLOCKED** — Brain approved P5, BRIEF §Q1)*
  Files: `software/facets/base/facet.yaml:985,990`.
  `facet_level_threshold: 6 → 5`. `major_advancement_threshold: 4 → 3`. Leave `session_skill_points: 4` and `skill_point_costs` (primary 1 / cross 2) untouched — DESIGN §6.2 explains why, and Brain ruled explicitly that rank inflation is a worse cost than a three-session slip on an illustrative number. **Do not raise `session_skill_points` to hit an earlier Major.**
  Accept: B1's threshold assertions pass; session-projection assertions still fail (they need B3).

- [ ] **B3 — Per-Facet level tracking.** *(TDD; DESIGN §1 F3)*
  Files: `software/app/game/character.py:210-269`, `software/tests/test_character.py`.
  - Add `facet_levels: dict[str, int]` and `rank_advances_by_facet: dict[str, int]`. `total_facet_levels` becomes the sum.
  - `_check_facet_level_threshold` currently returns `0` for any non-primary skill (`character.py:215-216`) — the reason Major Advancement has never fired for anyone. Rewrite it to credit the advance to the skill's own Facet.
  - Keep `facet_level` as a read-only property = `facet_levels[primary_facet]` for backward compatibility with `.fof` files and the UI.
  Tests (≥ 9): cross-Facet advance increments that Facet's level; `total_facet_levels` sums across Facets; Major fires at 3 total levels reached via 2 primary + 1 cross; boundary at exactly 5/10/15; existing `.fof` round-trip preserves `facet_level`.
  Accept: B1 fully green; full suite green.

- [ ] **B4 — Technique pick budget.** *(TDD; DESIGN §1 F4, §6.4)*
  Files: `software/app/game/character.py`, `software/app/api/websocket.py:1035`, `software/tests/test_character.py`, `software/tests/test_websocket.py`.
  Add `Character.technique_picks_available: int`, incremented on every Facet level in **any** Facet, decremented by `technique_select`. `_handle_technique_select` rejects when the budget is 0.
  Prerequisite validation is already correct and already tree-agnostic (`ruleset.get_technique()`) — **do not add a tree-ownership check.** D3 makes the code canonical and the PHB the thing that changes.
  Tests (≥ 6): pick granted per Facet level; `technique_select` with 0 picks is rejected with an error broadcast; a technique from a non-primary tree with prerequisites met is **accepted**; Tier 3 accepted when the same-branch Tier 2 is held; Tier 3 rejected without it.
  Accept: full suite green.

- [ ] **B5 — II.4 advancement text.**
  Files: `player_handbook/II.4_Character_Creation_Facets.md`.
  Update: the 6→5 threshold everywhere (including the Zulnut worked example at line 87, which counts to 6 and 12); *"At each Facet level you unlock one Technique from **any** tree whose prerequisites you meet"* (line 95, currently "your Facet's tree"); "Advancement at a Glance" (lines 248–266); the career-advance tier table (lines 280–282); Major Advancement at 3 levels (lines 205–220) including the worked example at line 209, which assumes 4.
  **The philosophy sidebar becomes false and must be rewritten** *(Brain, EF2)*. Around line 85 it reads *"Facet level 3 isn't earned by going deeper; it's earned by going wider."* True at threshold 6; **false at threshold 5**, where level 3 is reachable entirely in-Facet. Honest new framing: *level 3 = you have mastered all five skills of your Facet; level 4+ is where breadth begins.* Skipping this makes it ledger row 10 the day B2 lands.
  Line 89 was already fixed by **C10** — verify, do not re-edit.
  Accept: every number in II.4 matches `facet.yaml`; the sidebar no longer claims level 3 requires breadth; `/continuity-check` clean.

- [ ] **B6 — PT05 technique showcase.**
  Files: `playtest/05_technique_showcase/`.
  Play a character to Facet level 3 using the new pacing. Confirm a Tier 3 Technique and a Prismatic domain are actually reachable, and that Second Domain (Soul Communion Tier 3) can be taken.
  Accept: `playtest/05_technique_showcase/results.md` records the session at which each unlock landed, measured against the DESIGN §6.3 projection.

---

## WS-D — Death, hazards, Sparks (D4 + D6) — DESIGN §8. Independent of WS-A/B.

**Tasks in this workstream are numbered `WD*`, not `D*`** *(Brain, EF7)*. The BRIEF's decisions are D1–D8; a project that just built a contradiction ledger about ambiguous cross-references cannot have task D2 and decision D2 mean different things in the same commit message.

- [ ] **WD1 — `facet.yaml`: Threat Clock, recovery, death.** *(TDD)*
  Files: `software/facets/base/facet.yaml`, `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`.
  ```yaml
  hazards:
    threat_clock:
      segments: 4
      advances_on: [partial_success, failure]
      wind_back_cost: 1_action
      wind_back_requires_roll: false
  death:
    broken_is_lethal: false
    doom_gate: [permanent_scar, heroic_death]
  ```
  Accept: schema validates with typed sub-models + docstrings; ≥ 3 tests.

- [ ] **WD2 — Threat Clock engine + events.** *(TDD)*
  Files: `software/app/game/session.py`, `software/app/api/websocket.py`, `software/tests/test_websocket.py`.
  Events: `clock_create` (MM), `clock_advance`, `clock_wind_back`, `clock_fill` (broadcast when full). Clocks live in session state.
  **Wind-back is automatic** *(Brain, EF4)*: spending the action winds the clock back one segment, **no roll**. If a roll were required, a 7–9 on the wind-back would advance the very clock being wound — a rules-lawyer loop, in a chapter written for novice MMs. `clock_wind_back` takes no roll result and never advances.
  **No new resolution mechanics** — the clock advances off existing outcome tiers (BRIEF non-goal).
  Tests (≥ 7): advance on 7–9; advance on 6-; no advance on 10+; wind-back succeeds unconditionally and never advances; fill fires once at segment 4; clock survives a session round-trip.
  Accept: full suite green.

- [ ] **WD3 — Threat Clock UI in the Play Field.** *(Brain, EF8 — the plan had engine events and no UI)*
  Files: `software/app/static/js/play.js`, `software/app/static/js/components.js`.
  Render every active clock in the Play Field for **all players** — segments filled/empty, name, and current state. MM view adds create / advance / wind-back controls.
  Rationale, not decoration: a clock that lives only in WebSocket frames is bookkeeping the digital layer **failed** to absorb — a direct ethos violation, in the one chapter whose purpose is stopping a novice MM from inventing subsystems. "Visible to the table" (DESIGN §8.1) is a UI requirement.
  Accept: a player-role client renders clocks and cannot mutate them; an MM-role client can create, advance, and wind back; `clock_fill` is visible to everyone.

- [ ] **WD4 — Graceful Fail becomes player-initiated.** *(TDD; D6)*
  Files: `software/facets/base/facet.yaml:920-930`, `software/app/api/websocket.py`, `software/tests/test_websocket.py`.
  `spark.earn_methods.graceful_fail.structured: false → true`; rewrite its description as player-initiated: on any 6-, the player may claim it by narrating how they make the failure worse or richer; the MM confirms.
  New event `claim_graceful_fail` — mirrors the existing `spark_earn_peer` nomination shape at `websocket.py:324` (broadcast claim → MM confirms → Spark). New event `act_break` (MM) opens a nomination window.
  Tests (≥ 6): claim rejected when the player's last roll was not a 6-; claim broadcasts for confirmation; MM confirmation awards exactly 1 Spark; double-claim on the same roll rejected; `act_break` broadcasts.
  Accept: full suite green.

- [ ] **WD5 — III.1 Spark text.**
  Files: `player_handbook/III.1_Core_Resolution.md`.
  Codify **Act Break Nomination** and the player-initiated **Graceful Fail** in the player-facing chapter — the BRIEF is explicit that these do not live in MM5 alone. Keep: 3 Sparks/session, spend-before-roll, add-die-drop-lowest. State plainly that there is **no post-roll spending**.
  Accept: text matches `facet.yaml`; MM5's Spark section compresses it rather than restating it (C1 rule).

- [ ] **WD6 — Write III.2 Adventuring.** *(strictly scoped — DESIGN §8.1)*
  Files: `player_handbook/III.2_Adventuring.md` (new), `player_handbook/Table_of_Contents.md`.
  **Three sections only:** Hazards and Threat Clocks; Getting Hurt and Getting Better (recovery); When a Character Would Die.
  Death rule, one paragraph: *Broken never kills you. When a Broken result would end your character's life in the fiction, the choice is yours: take a permanent scar — a lasting cost you and the MM name together — and stay down alive; or choose a heroic death, and take one final action that automatically succeeds.*
  Adapt, do not copy, from `playtest/06_expert_novice_campaign/fun_and_consequence_review.md` Revision 1. Strip its "below 0 Endurance" framing — that is not how our rules work.
  **State the clock's pacing on purpose** *(Brain, EF4)*: roughly 72% of nearby rolls advance a segment, so a 4-segment hazard strikes after about 3–4 party rolls. That is the intended feel of visible pressure — write it as a deliberate design statement, not leave it as an emergent accident of the tier probabilities. Say plainly that winding back costs an action and requires no roll.
  Recovery: state what "treated" means for Tier 2 (a scene, a successful relevant skill roll, or a rest).
  **Do not scope-creep** into exploration, travel, or downtime.
  Depends on WS-A landing, since lethality determines what recovery must carry. Write the death rule and hazards first; write recovery after A8.
  Accept: chapter ≤ 3 sections; vignette voice per `references/phb-examples.md`; ToC updated; `/continuity-check` clean.

- [ ] **WD7 — Spark refund variant flag.**
  Files: `software/facets/base/facet.yaml`, `software/tools/combat_sim.py`.
  Add `spark.variants.refund_on_failed_pretechnique_cast: false`. **Test, do not adopt** (BRIEF D6).
  Accept: flag exists, defaults off, is readable by the sim and PT04 harness.

- [ ] **WD8 — PT04 resource tax.** *(the acceptance test for D6)*
  Files: `playtest/04_resource_tax/` (scenario exists).
  Run with the new Spark cadence and the refund variant enabled for measurement.
  Accept: **Sparks spent per player ≥ 2**. Below that, D6 is revisited — escalate to Planner. Record whether the refund variant changed spending. Write `playtest/04_resource_tax/results.md`.

---

## WS-E — Content (D7) — DESIGN §9. Fully parallel. No engine impact.

- [ ] **E1 — Domain example intents.** *(large — split per Facet, or per 6 domains, if a session runs long)*
  Files: `player_handbook/Appendix_Magic_Domains.md`.
  **Three example intents per scope × three scopes (Minor / Significant / Major) × 18 domains = 162 entries** *(arithmetic corrected per Brain, EF3 — DESIGN §9 and this task previously computed "= 54," dropping a factor of 3; 3-per-scope stands)*.
  **Why three and not one:** variety within a scope is the anti-canonization mechanism. One example per scope becomes "the Minor Inscription spell" within two playtests, and the appendix turns into the spell list D7 exists to prevent.
  Entries stay **one line each**. Frame explicitly as **design patterns, not a menu**. Pre-set "spell packages" are rejected.
  **If the entries start reading like castable spells with fixed effects mid-writing, stop and escalate to Planner** — do not finish the appendix and hope the framing paragraph saves it.
  Copyright policy applies: original content only.
  Accept: 18 domains × 3 scopes × 3 examples = 162 entries; the framing paragraph is present and unambiguous; no entry reads as a castable spell with fixed effect.

- [ ] **E2 — MM Trouble Table.**
  Files: `mm_manual/MM5_Quick_Reference.md`.
  A d6 table of generic 6- consequences: cost / position / attention / equipment / condition / revelation. Each entry one line, usable mid-session without a lookup.
  Accept: table is d6, scannable, and contains no rule the PHB does not already state.

- [ ] **E3 — Magic 6- templates into MM5.**
  Files: `mm_manual/MM5_Quick_Reference.md`, source: `player_handbook/II.3_Magic.md`.
  Duplicate II.3's magic 6- consequence templates. Under the C1 rule this is **compression of canonical text**, which is permitted — a paraphrase is not. Copy the structure, cite II.3.
  Accept: MM5 and II.3 agree verbatim on every rule statement.

---

## Task count and gating summary

| Workstream | Tasks | Blocks | Gate |
|---|---|---|---|
| WS-C consolidation | 11 | everything (clean diffs) | `/continuity-check` |
| WS-A0 extraction | 4 | WS-A | **G0** (exact seeded end-state) |
| WS-A durability | 13 | PT03, PT05 budget | **G1, G2, G3, G4** + PT03 |
| WS-B advancement | 6 | PT05 | pacing regression test |
| WS-D death/hazards/sparks | 8 | PT04 | **PT04: ≥ 2 Sparks spent/player** |
| WS-E content | 3 | — | copyright + continuity |

**45 tasks** (was 43: +A0.4 supersede the sim corpus, +WD3 Threat Clock UI). Full suite must be green before any workstream is marked done.

**Nothing is blocked.** Brain resolved Q1–Q4 on 2026-07-10 (`docs/BRIEF_v0.3_ruleset_revision.md` §BRIEF AMENDMENT): A5 and B2 are unblocked, WS-A0 is retroactively authorised, and the eight editorial findings EF1–EF8 are patched into this file and into DESIGN. **Start at WS-C, task C1.**
