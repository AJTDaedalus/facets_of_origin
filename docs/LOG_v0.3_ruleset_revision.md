# LOG — v0.3 Ruleset Revision

**Tier:** Worker (Sonnet 5) execution log
**Tasks:** `docs/TASKS_v0.3_ruleset_revision.md`

---

## WS-C — Consolidation pass (D5)

**Scope:** C1–C11, run as a single session, landed as one commit per the task's own instruction ("Target: one commit"). User approved this scope explicitly before starting (WS-C only, then stop and report) rather than a strict one-task-per-checkpoint cadence.

- **C1** — Added the two repo rules to `CLAUDE.md` under Software-PHB Synchronization: quick refs compress/never paraphrase; simulator may only drive `app/game/combat.py`.
- **C2** — Fixed II.5's stale pre-technique magic text (removed the invented difficulty penalty). Verified II.3, MM5, Quick_Start.md, and `facet.yaml` already state the canonical rule (Minor scope only, no penalty) — no fix needed there.
- **C3** — Fixed the "same or different" → "same type" Broken-stacking language in III.3's quick-ref card and MM5.
- **C4** — Fixed `_handle_apply_condition` in `websocket.py` to escalate to Broken only when the incoming Tier 2 condition id already exists on the character (was: escalating on *any* second Tier 2, regardless of type). Reads the Tier 2 id set from `ruleset.combat.conditions.tier2` instead of a hardcoded literal. Rewrote the existing `test_tier2_stacking_to_broken` (which encoded the buggy behavior) into three tests: same-type escalation, different-type coexistence, third-application idempotence. All pass; full suite green.
- **C5** — Deleted the invented "deflect and counter (attacker takes T1)" Parry effect from III.3's quick-ref and MM5 — Parry outcomes are now identical to Dodge everywhere, matching the already-correct body text.
- **C6** — Generalized the Strike/Parry roll formulas in III.3 (body text + quick ref), MM5, and Quick_Start.md from hardcoded "Strength + Combat" to "weapon attribute + relevant skill" (Combat for melee/unarmed, Finesse for ranged), matching IV.1's weapon-category table. Confirmed the engine (`websocket.py:472-479`) already accepts any attribute/skill — no code change needed.
- **C7** — Fixed MM5: attribute rating 1 label "Poor" → "Weak" (matches `facet.yaml`); PvP tie rule "ties go to defender" → "both achieve partial success" (matches III.1).
- **C8** — Deleted the "Spent ally" ghost-text reference from Intercept in III.3 (Spent was cut in the 2026-03-04 simplification). Rewrote the ambiguous Maneuver wording ("target's next roll is Easy") to the canonical "rolls **against** the target are Easy."
- **C9** — Example-character continuity, the largest task in this batch:
  - **Escalated a real discrepancy to the user first**: BRIEF/DESIGN (both dated today) said Zulnut's background is "Wandering Disciple" / pronoun "he", but the actual `characters/Zulnut.fof`, II.5's Background section, and II.4's worked example currently said "Street Performer" / "she". Asked the user directly rather than guessing; confirmed "Wandering Disciple / he" is canonical (also matches the untouched `README.md` and `Quick_Start.md`, which were never drifted). Rewrote `characters/Zulnut.fof` (background block + top-level skill from `perform`→`stealth`), fixed II.5's closing "In Play" analysis paragraph, and fixed II.4's pronoun in the Stealth/Finesse point-spend example.
  - Rewrote II.3's "Example: A Mage, a Beam, a Problem" — previously described Zahna as a "Focused Fire mage" rolling Spirit; rewrote to Inscription domain (fracture-glyph on structural joints) rolling Knowledge, with correct "he" pronoun throughout.
  - Found and fixed two *additional* errors in III.3's "Example pools" block while verifying against source-of-truth `.fof` files (not explicitly named in the ledger row but caught by the "all four files agree with `characters/*.fof`" accept criterion): Zahna's Constitution was listed as 2 (actual: 1, pool should be 3 not 4); Mordai's Endurance skill was listed as Practiced (actual: Novice, pool should be 5 not 6). Traced the pool-6 error through the downstream boss-fight vignette and corrected three dependent Endurance-tracking numbers (lines ~456, 522, 536) that had been built on the wrong starting value.
  - Verified via `combat_sim.py`'s `mordai_def()`/`zulnut_def()` fixtures that the engine already used the correct pool values — only the PHB prose was stale.
- **C10** — Rewrote II.4 line 89, which said cross-Facet Facet-level advances "do not count toward your Major Advancement threshold" — directly contradicted the Major Advancement section's own worked example two paragraphs later (lines 207–209), which sums levels across Facets. Canonical (per BRIEF D3): cross-Facet levels **do** count. Left the Zulnut worked example at line 87 and the 6/12 threshold numbers untouched — those are B5's job (WS-B) once B2/B3 land the new 5/10/15 thresholds.
- **C11** — Manual continuity pass across `player_handbook/`, `mm_manual/`, and `Quick_Start.md` (the `continuity-check` skill's tooling targets World Anvil campaigns via MCP calls, not applicable here — did the equivalent by hand: grepped for remaining pronoun/background/formula drift for all three example characters, found none outstanding). Full test suite: **722 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000` — fails identically on a clean stash of the branch before any of this session's changes; caused by a local `.env` setting `PORT=8010`, not touched by WS-C).

**Files changed (10):** `CLAUDE.md`, `characters/Zulnut.fof`, `mm_manual/MM5_Quick_Reference.md`, `player_handbook/II.3_Magic.md`, `player_handbook/II.4_Character_Creation_Facets.md`, `player_handbook/II.5_Character_Creation_Backgrounds.md`, `player_handbook/III.3_Combat.md`, `player_handbook/Quick_Start.md`, `software/app/api/websocket.py`, `software/tests/test_websocket.py`.

**Note for whoever runs `git status` next:** an e2e Playwright test (`test_playtest_02.py`) regenerates `playtest/02_silence_of_ashenmoor/digital_tool_log.md` with new random dice rolls every time the full suite runs. This is pre-existing test behavior, not a WS-C change — it was reverted twice during this session and is not part of the commit.

---

## WS-A0 — Combat extraction

A0.1–A0.4 were already `[x]` in `TASKS` at the start of this session (prior work, no LOG entry existed — not re-verified here since A2 doesn't touch `combat.py`).

## WS-A — Enemy durability & armor (D1 + D2)

- **A2 — `Enemy` model: Resolve, TR re-key, back-compat.** *(TDD)*
  - Wrote 46 tests in `tests/test_enemy.py` first (red step confirmed: 31 failed against unmodified code), then implemented `app/game/enemy.py`:
    - Renamed `endurance`→`resolve`, `endurance_current`→`resolve_current`; `init_combat` unchanged in behavior (non-Mook gets full pool).
    - `calculate_tr()`: deleted the 7-branch Endurance ladder; `durability_value = 0` for Mook else `= resolve`. Tier minimums untouched.
    - `from_fof`: added `_map_legacy_endurance_to_resolve()` per the DESIGN §4.1 table; emits `DeprecationWarning` only when `resolve` is absent and `endurance` is present (`resolve` always wins if both keys exist). `to_fof` writes only `resolve`.
    - Added `PhaseDef` (`resolve_threshold: int`, `description: str = ""`) and `Enemy.phases: list[PhaseDef]`; round-trips through `to_fof`/`from_fof`.
  - Verified against the DESIGN worked examples: Sergeant (resolve 3) → TR 8, Veteran Soldier (resolve 4) → TR 10 — both preserved exactly. Archive Guardian recomputes to **14** (offense 5 + resolve 5 + armor 2 + technique_bonus 2), matching the documented double-counting fix — not yet written to `enemies/archive_guardian.fof` (that's **A3**).
  - **Scope note — touched two files outside A2's stated `Files:` list, both required to keep "full suite green" (A2's own accept criterion), pure renames with no logic change:**
    - `app/api/routes/enemy.py` — `CreateEnemyRequest.endurance` → `.resolve`, and the `Enemy(...)` construction call.
    - `app/api/websocket.py` — `_handle_spawn_enemy`'s inline-data path (`enemy_data.get("endurance", 0)` → `"resolve"`) and `_handle_enemy_update` (`msg["endurance_current"]` / broadcast key → `resolve_current`). These are wire-format keys under active development, not the archival `.fof` format the DESIGN doc's back-compat clause is scoped to, so no shim was added.
    - Updated the two dependent test files accordingly: `tests/test_api_enemy.py` (2 spots) and `tests/test_websocket.py` (renamed `test_enemy_update_endurance` → `test_enemy_update_resolve`, updated keys in `test_enemy_update_conditions`).
  - **Deliberately left untouched (other tasks' scope):**
    - `enemies/*.fof` still use the legacy `endurance` key — loads fine via the back-compat path with a `DeprecationWarning` (not an error; `pytest.ini`'s `filterwarnings` only silences `jose`'s). **A3**'s job to migrate.
    - `app/static/js/play.js` and `components.js` still read `enemy.endurance` / `enemy.endurance_current` on the client — not exercised by pytest, so it didn't block "full suite green," but the live web UI's enemy tracker will now silently show nothing for Resolve until those are renamed. This is explicitly **A12**'s task ("Web app: enemy tracker shows Resolve") — flagging here so it isn't missed, not fixing it now to keep this task's diff scoped.
    - `tests/e2e/test_playtest_02.py` still sends `"endurance"` / `"endurance_current"` over the WebSocket wire in its MM-simulation steps; those assertions are non-strict (`msg.get(..., default)`, no equality check), so they don't fail — but the log line "MM: Updated The Hollow endurance to 4" will now always report the fallback default rather than a real value. Cosmetic only; not fixed, since this file isn't in A2's or any other WS-A task's `Files:` list.
  - **Result:** `pytest tests/test_enemy.py` → 46/46 pass. Full suite: **799 total, 798 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, same cause as noted in WS-C above — local `.env` `PORT=8010`).
  - **Files changed:** `software/app/game/enemy.py`, `software/tests/test_enemy.py`, `software/app/api/routes/enemy.py`, `software/app/api/websocket.py`, `software/tests/test_api_enemy.py`, `software/tests/test_websocket.py`.

**Status:** WS-C complete, ready to commit as `Consolidate contradictory rules (PHB D5 ledger)`. Per the user's chosen scope for this session, stopping here — WS-A0/WS-A/WS-B/WS-D/WS-E are not started.

---

## WS-A0 — Combat extraction (blocks WS-A)

**Scope:** A0.1–A0.4, run as a single session (user invoked "execute WS-A0" directly, mirroring the WS-C scope precedent). Full suite green throughout: 765 passed, 1 pre-existing unrelated failure (`test_default_port_is_8000`, caused by a local `.env` `PORT=8010`, unrelated to this branch).

- **A0.1** — New `software/tests/test_combat_characterization.py`. Pinned `tools/combat_sim.py`'s pre-refactor semantics: `armor_downgrade` (light gates Tier 2→1 only, heavy gates Tier 3→2 only), `apply_condition` stacking/zero-End-absorb, `cleanup_end_of_exchange`, and reaction Endurance cost by posture — plus 5 fixed-seed full `run_combat` scenarios asserting exact end-state (not aggregate win rate). 16 tests, all passing against unmodified code. This is the G0 baseline.

- **A0.2** — New `software/app/game/combat.py` + `software/tests/test_combat.py` (39 tests). Moved the rules into pure, synchronous functions (`roll`, `resolve_strike`, `resolve_reaction`, `armor_downgrade`, `apply_condition`, `end_exchange`) reading every constant from `MergedRuleset`. Added `facet.yaml`'s missing `combat.reactions` block (`dodge: 1, parry: 1, absorb: 0, intercept: 2` — canonical PHB values that were only ever hardcoded in `websocket.py`) and `postures.withdrawn.free_reactions: true` (an explicit flag, replacing the old code's `-99` sentinel trick for "free reactions"). Verified `combat.roll`'s dice draws are bit-exact against `combat_sim.combat_roll` and `engine.resolve_roll` for identical seeds before writing anything downstream of it.

  **Judgment calls made (DESIGN doesn't fully specify these — documented here for review):**
  1. **`armor_downgrade` keeps the simulator's gated one-step rule** (light only affects Tier 2, heavy only affects Tier 3), not the pre-extraction engine's subtractive rule (`max(0, tier - downgrades)`, which let light armor fully absorb Tier 1 and heavy fully absorb Tier 2 — DESIGN's F1/F2 finding, explicitly "not preserved"). `facet.yaml`'s existing `armor.light/heavy.downgrades` numbers encoded the *old* engine algorithm and are not read by the new `armor_downgrade` — flagged in its docstring as a residual for D2 (WS-A A5) to resolve properly.
  2. **`Combatant` protocol is intentionally minimal** (`conditions: list[str]` only). `Character.endurance_max` is a method, not a field; `Enemy` has no `posture`; `is_broken`/`is_removed` are booleans on the simulator's `PCState`/`EnemyState` but a literal `"broken"` condition string on `Character`. Rather than retrofit those models, `apply_condition` returns a `broken: bool` on its result and lets each caller apply that to its own representation. Endurance/posture/armor are taken as explicit parameters, not read off a combatant object.
  3. **`resolve_strike`/`resolve_reaction` resolve rolls and their immediate rule consequences only** — not the whole Strike (mook removal check, armor, condition choice). Production's `_handle_strike`/`_handle_apply_condition` are already two separate player/MM actions (PHB: "attacker chooses which Tier 2 Condition"), so bundling roll+condition into one function would have meant either forcing that choice into combat.py (wrong — it's not a rule) or building an API production couldn't use. `_handle_strike`/`_handle_react`'s actual dice rolls still go through `engine.resolve_roll`/`RollRequest` (unchanged, already ruleset-driven) — `combat.py`'s `roll`/`resolve_strike` primarily serve the simulator's flat-modifier callers.
  4. **`persistent_conditions` dropped from `PCState`/`EnemyState`.** Proved redundant before removing it: everything ever added to it was already Tier 2+ (`TIER2_CONDITIONS` membership), so `end_exchange`'s "survives cleanup" check via ruleset tier lookup produces identical results without it. Not in DESIGN's explicit G0 checklist (`conditions, Endurance, out/alive`), so this simplification doesn't touch the gate.

- **A0.3** — Rewired both consumers:
  - `websocket.py`: `_handle_strike`'s posture-offense lookup, `_handle_react`'s reaction-cost table (`websocket.py:559`), `_downgrade_condition_for_armor` (now the F1/F2 bug fix — gated, not subtractive), `_handle_apply_condition`'s Tier 2 stacking check (`~684`), and `_handle_end_exchange`'s Tier 1 clear + recovery amount (`~722`, `~727`) all now call `combat.py`. Preserved one pre-existing engine-only quirk not covered by G0 or DESIGN: `_handle_apply_condition` silently no-ops a duplicate *non-escalating* condition (e.g. a second "winded" does nothing) — this predates the extraction, is orthogonal to the simulator's list-based semantics, and DESIGN doesn't flag it, so it was kept as explicit glue in the handler rather than folded into `combat.apply_condition`.
  - `combat_sim.py`: deleted `apply_condition`, `_apply_broken`, `cleanup_end_of_exchange`, `armor_downgrade` per the task list. `resolve_pc_strike`/`resolve_enemy_attack` became private `_pc_strike`/`_enemy_attack`, orchestrating policy (unchanged: `should_spend_spark`, `should_press`, `should_enemy_react`, `choose_pc_reaction`, plus a new `_choose_condition` policy helper replacing the inline "prefer staggered, else cornered" logic) around calls into `combat.py`. `_mark_broken` (Boss phase-change + is_broken/is_removed bookkeeping) stays in `combat_sim.py`, renamed from `_apply_broken`, reacting to `apply_condition`'s `broken` return value — it's simulator-only state, not a rule, so it wasn't moved into `combat.py` (see A0.2 judgment call #2). `run_combat` now loads the ruleset once via a cached `_ruleset()` rather than taking a new parameter, so `run_simulation`/`get_series`/the CLI's public signatures are unchanged. Left `combat_roll` and its module constants (`TIER1_CONDITIONS`, `TIER2_CONDITIONS`, `POSTURE_OFFENSE`, `POSTURE_REACTION_COST`, `DIFFICULTY_MOD`) in place, unused by the new orchestration but still exercised by `TestCombatRoll`/`test_staggered_attacker_penalty` — deleting them wasn't in A0.3's explicit list and would have meant a larger, unrequested test rewrite; flagged as a residual duplication in a code comment.
  - Added `TestCombatRulesParity` to `test_websocket.py` (3 tests): heavy-armor downgrade, same-Tier-2-twice-escalates-to-Broken, and end-of-exchange Tier 1 clearing, each computed independently through `combat.py` and compared against the WebSocket handler's observable result on identical input. Permanent guard against F1 recurring.
  - **G0 re-verified exactly**: all 16 A0.1 characterization tests (armor/condition/cleanup pinned semantics now importing from `combat.py`, 5 fixed-seed `run_combat` scenarios still against `combat_sim`) pass unchanged after the rewire. `test_combat_sim.py`'s `TestConditions`/`TestArmorDowngrade` (11+3 tests) deleted as redundant with the new `test_combat.py`; `TestPCStrike`/`TestEnemyAttack`/`TestBossPhaseChange` rewritten to call `_pc_strike`/`_enemy_attack` with the new `ruleset` parameter, same assertions. CLI smoke-tested (`python -m tools.combat_sim --series A`) — runs cleanly.

- **A0.4** — `research/simulation_log.md`: added a top-of-file notice plus a `**SUPERSEDED (v0.2 semantics)**` one-liner after every Series/Calibration Summary/Master Calibration Table/Key Design Conclusions heading (10 total), each pointing to DESIGN §4.3. Noted that Series 6's methodology line mislabels the 0-End rule "per PHB" when DESIGN F5 found it was simulator-only. Nothing deleted. `research/armored_enemy_breaking_problem.md`'s "RESOLVED" marking is task A6 (WS-A), not in A0.4's scope — left untouched.

**Files changed:** `software/facets/base/facet.yaml`, `software/app/facets/schema.py` (none — no schema change needed, `reactions`/`postures` were already open dicts), `software/app/game/combat.py` (new), `software/app/api/websocket.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py` (new), `software/tests/test_combat_characterization.py` (new), `software/tests/test_combat_sim.py`, `software/tests/test_websocket.py`, `research/simulation_log.md`, `docs/TASKS_v0.3_ruleset_revision.md`.

**Test count:** 721 (WS-C baseline) → 765 passed (+ new `test_combat.py`/`test_combat_characterization.py`/`TestCombatRulesParity` tests, − obsolete `TestConditions`/`TestArmorDowngrade` in `test_combat_sim.py`).

**Status:** WS-A0 complete (A0.1–A0.4), not yet committed. G0 gate passes exactly. Stopping here per the user's "execute WS-A0" scope — WS-A is next (`docs/TASKS_v0.3_ruleset_revision.md` line 377 updated to point there), not started this session.

---

## WS-A — Enemy durability & armor (D1 + D2)

- **A1** — Schema + `facet.yaml`: Resolve and armor (DESIGN §4.1/§4.2).
  - `facet.yaml` `combat.armor`: replaced `light.downgrades: 1` / `heavy.downgrades: 2` with the per-scene budget shape — `light: {downgrades_per_scene: 2, tiers_reduced: 1}`, `heavy: {downgrades_per_scene: 4, tiers_reduced: 1}`. Deliberately `downgrades_per_scene`, never `_per_exchange`/`_per_fight` per Brain's Q2 ruling.
  - `facet.yaml` `combat.enemy_durability` (new): `strike_depletion` (2/1/0 by outcome tier), `armor_resolve_bonus` (0/1/2 by armor type — numerically the TR formula's `armor_bonus`), `mook_removed_on: partial_success`, `armored_mook_removed_on: full_success`.
  - `schema.py`: rewrote `ArmorEntryDef` (`downgrades_per_scene`, `tiers_reduced`, replacing the old `downgrades` field — no back-compat shim, since nothing outside this schema module referenced the field name; `combat.py:239`'s docstring comment still refers to the old key name as historical context on why `armor_downgrade` doesn't read it, left alone since A5 owns rewriting that function). Added `StrikeDepletionDef`, `ArmorResolveBonusDef`, `EnemyDurabilityDef` (all with docstrings matching existing style), and wired `EnemyDurabilityDef` onto `CombatDef.enemy_durability`.
  - Tests: 8 new in `test_facets_schema.py` (`TestArmorEntryDef`, `TestArmorDef`, `TestStrikeDepletionDef`, `TestArmorResolveBonusDef`, `TestEnemyDurabilityDef`) exercising defaults and custom construction; 2 new in `test_facet_loading.py` (`test_pc_armor_per_scene_budgets_loaded`, `test_enemy_durability_loaded`) asserting the real `facet.yaml` values load through `MergedRuleset`.
  - **Files changed:** `software/facets/base/facet.yaml`, `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`, `software/tests/test_facet_loading.py`.
  - **Test count:** 765 (WS-A0 baseline) → 775 passed, same 1 pre-existing unrelated failure (`test_default_port_is_8000`).
  - **Status:** A1 complete, not yet committed (per-task cadence — stopping to report before A2). A2 (`Enemy` model: Resolve, TR re-key, back-compat) is next.

- **A3** — Migrate `enemies/*.fof`.
  - `city_watch_sergeant.fof`: `endurance: 6` → `resolve: 3` (map: 5–6→3). `tr: 8` unchanged; inline comment and `notes:` reworded from "durability(Endurance 6 → value 3)" to "durability(Resolve 3)".
  - `veteran_soldier.fof`: `endurance: 7` → `resolve: 4` (map: 7–8→4). `tr: 10` unchanged; comment and `tactics`/`notes` wording updated the same way.
  - `archive_guardian.fof`: `endurance: 10` → `resolve: 5` (map: 9–10→5). **Found and fixed a latent load-breaking bug while migrating**, not caused by this task: `special:` held a nested `phase_change` dict, but `Enemy.special` is typed `Optional[str]` — the file has never loaded through `Enemy.from_fof` under the current schema (confirmed with a standalone repro before editing: `pydantic_core.ValidationError: special / Input should be a valid string`). Replaced the dict with the new structured `phases:` list (`[{resolve_threshold: 2, description: "Reduced Mode..."}]`, matching the `PhaseDef` shape A2 added) and set `special: null`. Moved the phase-change flavor text (attack_modifier drop to +1, Tier 1 immunity) into the phase's `description`; dropped the old "Endurance resets to 4 for the second phase" line — that was a house-rule detail of the retired Endurance/Broken track with no equivalent in the Resolve-depletion design, and nothing in DESIGN §4 or A2/A4 specifies a Resolve reset on phase change, so inventing one would be new mechanics, not a migration.
    To hit the task's specified `tr: 14`, gave the Guardian `techniques: [phase_change, tier1_immunity]` (two literal entries, +2 to `technique_bonus` under `calculate_tr()`'s `len(self.techniques)`) — this reproduces exactly the technique_bonus=2 that A2's `test_boss_archive_guardian_recomputes_to_14` fixture already established as canonical (`software/tests/test_enemy.py:76-78`), just written back into the `.fof` rather than only asserted in the test. Rewrote the `tr:` inline comment and the `notes:` TR-breakdown paragraph to "offense(5) + durability(Resolve 5) + armor(heavy→2) + techniques(2) = 14"; also corrected "Deadly encounter" → "Hard-to-Deadly" in `notes:` since budget 12 vs actual TR 14 is no longer the same margin as the old TR 16.
  - `chicken.fof`, `harbor_thug.fof`: both Mooks, neither ever had an `endurance:` key (Mook durability is always 0), so no key migration needed. **Found a second pre-existing, unrelated mismatch while verifying**: `harbor_thug.fof` published `tr: 1` but `attack_modifier: 0` computes to offense value 2 under the documented formula (`-2→0 ... 0→2 ... `), giving TR 2 — confirmed via `git diff HEAD` that this file is untouched by any prior session's work, so the error predates this branch. Fixed `tr: 1` → `tr: 2` with an inline breakdown comment, since A3's accept criterion is "`calculate_tr()` matches the published `tr:` in each file" for the full file list, not just the ones with an `endurance` key. `chicken.fof`'s `tr: 1` already matched (`attack_modifier: -1` → offense 1) — left untouched.
  - `spec/examples/encounter-example.fof`: checked, contains no `endurance:` key (it references enemies by `enemy_id` only, no inline stat block) — no change needed.
  - Verified all five `enemies/*.fof` files load through `Enemy.from_fof` with zero `DeprecationWarning`s and `calculate_tr()` matching the published `tr:` exactly (chicken 1, harbor_thug 2, sergeant 8, veteran 10, guardian 14) via a standalone script before running the suite.
  - **Files changed:** `enemies/city_watch_sergeant.fof`, `enemies/veteran_soldier.fof`, `enemies/archive_guardian.fof`, `enemies/harbor_thug.fof`. (`chicken.fof` and `spec/examples/encounter-example.fof` checked, not modified.)
  - **Test count:** 775 (A2 baseline) → 798 passed, same 1 pre-existing unrelated failure (`test_default_port_is_8000`) — unchanged, since A3 touches only data files with no test suite coverage of `enemies/*.fof` contents directly.
  - **Status:** A3 complete, not yet committed. A4 (`combat.py`: Resolve depletion and rider Conditions) is next.

- **A4 — `combat.py`: Resolve depletion and rider Conditions.** *(TDD)*
  - Wrote 23 tests in `tests/test_combat.py` first (red step confirmed: `AttributeError` on the not-yet-existing functions), then implemented `app/game/combat.py`:
    - `apply_resolve_damage(resolve_current, outcome, ruleset, phase_thresholds=None) -> ResolveDamageResult`. Depletion read from `enemy_durability.strike_depletion` by outcome tier, floored at 0 (`defeated`). **Took primitives, not an `Enemy` object** — the task text's shorthand signature (`apply_resolve_damage(enemy, outcome_tier, ruleset)`) would have broken the module's established pattern (see A0.2 judgment call #2: field names diverge across `Character`/`Enemy`/the simulator's `PCState`/`EnemyState`, so combatant-specific fields are always taken as explicit parameters, never read off an object). `phase_index` is detected by comparing `resolve_current` (before) against `new_resolve` (after) per threshold — crossing is a property of the monotonically-decreasing call sequence, so "fires exactly once" needs no extra state on the enemy, matching the module's no-side-state design.
    - `mook_removed(outcome, armored, ruleset) -> bool`. Threshold read from `mook_removed_on`/`armored_mook_removed_on`, compared via an outcome-tier ordering list rather than a hardcoded set.
    - `target_strike_difficulty(base_difficulty, target_conditions, ruleset) -> str`. Returns `"Easy"` when `target_conditions` holds any Tier 2 id, else `base_difficulty` unchanged — this is what makes a Tier 2 rider from a prior Strike matter (verified end-to-end against `resolve_strike` in `test_easy_flows_through_resolve_strike_as_a_bonus`).
    - `apply_condition` gained `is_rider: bool = False`: when set, the same-type-Tier-2-escalates-to-Broken check is skipped entirely (riders never produce Broken; Resolve is what defeats an enemy, per DESIGN §4.1). No separate `_apply_broken`-style function was written for enemies — none exists in `combat.py` to delete (A0.3 already removed `combat_sim.py`'s copy); confirmed via `grep -rn _apply_broken` that only a comment noting its removal remains.
    - Tier 1 riders need no special handling beyond `is_rider=True` at apply time — `end_exchange` already clears any Tier 1 id regardless of how it was added, verified in `test_tier1_rider_clears_at_end_exchange`.
  - **Scope note — touched `app/game/enemy.py` and `tests/test_enemy.py`, outside A4's stated `Files:` list.** DESIGN §4.1 states "Enemy armor adds flat Resolve at init_combat (light +1, heavy +2)" as a load-bearing requirement for G1 (`research/simulation_log.md`'s planned Archive Guardian run explicitly needs heavy armor → effective Resolve 7 = 5 base + 2 armor). A4's own accept-criteria test list doesn't name this behavior, and A2 (which owns `init_combat`) shipped it without the armor bonus — a real gap between the two task specs, not a implementation choice. Left unfixed, `apply_resolve_damage` would deplete from a pool that never reflected the bonus, silently invalidating G1 before it's even run. Fixed at the source (`Enemy.init_combat()`) rather than working around it in `combat.py`, using the same hardcoded `{"none": 0, "light": 1, "heavy": 2}` mapping style `calculate_tr()` already uses in that file (which isn't ruleset-driven either) — no `MergedRuleset` plumbed through, no call-site signature change (`websocket.py:1096`'s `enemy.init_combat()` is unaffected). 3 new tests added to `TestEnemyCombatTracker` in `test_enemy.py` (light +1, heavy +2, Mook armor grants nothing).
  - **Deliberately left untouched (other tasks' scope):** nothing in `websocket.py` or `combat_sim.py` calls the new functions yet — that's A7 (phase-change broadcast) and A8 (simulator gates). `armor_downgrade` is not invoked anywhere near enemy Conditions (D2's PC-only downgrade budget is A5); documented in `apply_condition`'s docstring that riders bypass it rather than adding a no-op guard with nothing yet calling it.
  - **Result:** `pytest tests/test_combat.py` → 63/63 pass (40 pre-existing + 23 new). Full suite: **825 total, 824 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, local `.env` `PORT=8010`, same as every prior WS-A entry).
  - **Files changed:** `software/app/game/combat.py`, `software/tests/test_combat.py`, `software/app/game/enemy.py`, `software/tests/test_enemy.py`.
  - **Status:** A4 complete, not yet committed. A5 (PC armor per-scene downgrade budget) is next.

- **A5 — `combat.py`: PC armor per-scene downgrade budget.** *(TDD; DESIGN §4.2)*
  - Wrote 17 new tests in `tests/test_combat.py` first (red step confirmed: old two-arg `armor_downgrade` call sites in `test_combat_characterization.py`/`test_websocket.py`/`tools/combat_sim.py` all `TypeError`'d against the new signature before those call sites were updated), then rewrote `app/game/combat.py`'s armor section:
    - `armor_budget(armor, ruleset) -> int` — starting per-scene budget from `combat.armor.<type>.downgrades_per_scene` (2 light / 4 heavy, from A1). Used both to initialise the counter and to reset it, since a fresh budget is the same value either way.
    - `armor_downgrade(tier, armor, downgrades_remaining, ruleset) -> ArmorDowngradeResult` — replaced the old "light only gates Tier 2, heavy only gates Tier 3, unlimited uses" shape (itself DESIGN §4.2's finding: unlimited per-hit downgrade meant an armored PC facing a single boss could never be Broken) with a finite counter: any nonzero tier is reduced by `tiers_reduced` (1) as long as budget remains, consumed one unit per call. Pure — the caller owns the counter (`Character.armor_downgrades_remaining`) and passes it in each time, same pattern as `apply_resolve_damage` reporting a new pool value instead of holding one itself.
  - `app/game/character.py`: added `armor_downgrades_remaining: Optional[int] = None`, persisted to/from `.fof` the same way as `endurance_current`/`conditions`/`posture`/`armor` (server restarts mid-combat can resume).
  - `app/api/websocket.py`: deleted `_downgrade_condition_for_armor` per the task instruction; replaced with `_apply_pc_armor_budget`, which calls the new `combat.armor_downgrade` and writes the returned `downgrades_remaining` back onto the character. `_handle_combat_start` now initialises `armor_downgrades_remaining` via `combat.armor_budget` **only if it is currently `None`** — a second `combat_start` for a second fight in the same scene must not top the budget back up (DESIGN §4.2: "two fights inside one scene share the budget"). `_handle_combat_end` was left untouched (it already doesn't reset `armor` or the new field), so the budget survives a `combat_end`/`combat_start` pair.
    - **Known gap, not closed here:** the app has no explicit "scene end" event anywhere (checked — `combat_start`/`combat_end`/`session_reset` are the only relevant handlers, and `session_reset` is a session-level boundary, not a scene-level one). `armor_budget` exists and is tested as the reset function DESIGN calls for, but nothing in `websocket.py` currently calls it at a scene boundary, because there is no scene boundary to call it at. Flagging this rather than inventing a new event outside A5's scope — it's the MM's job to know when a scene ends narratively, and wiring that is a UI/protocol design question for a later task, not a rules question A5 owns.
  - **Scope note — touched `tools/combat_sim.py`, outside A5's stated `Files:` list, to keep the accept criterion ("full suite green") true.** The old `armor_downgrade(tier, armor)` two-arg signature was called from three places in the simulator, not just the one D2 actually governs:
    - `_enemy_attack`'s two call sites (PC reacting to an enemy attack) are the genuine D2 case — added `PCState.armor_downgrades_remaining: int = 0`, initialised fresh at the top of `run_combat` via `combat.armor_budget` (one `run_combat` call is one scene's worth of combat for the simulator's purposes, so "fresh per run" *is* "reset at scene start" here), and wired both call sites to read/write it.
    - `_pc_strike`'s one call site (a PC's Strike landing on an armored **enemy**) was never D2's case at all — it's DESIGN §4.1's already-settled "enemy armor is a flat Resolve bonus, not a Condition-tier gate," which A4 established but didn't retrofit into this pre-D1 simulator function (A4's own LOG entry says as much: "nothing in `websocket.py` or `combat_sim.py` calls the new functions yet"). Deleted the call rather than parameterising it, since the new `armor_downgrade`'s uniform "-1 to any nonzero tier" shape can't reproduce the old tier-specific gate anyway, and CLAUDE.md's C1 rule forbids reimplementing rule logic locally in the simulator to paper over the mismatch. This is a full migration of `_pc_strike`'s enemy-durability model to Resolve — that's still A8's job for G1/G2; this only removes the one line that no longer type-checks and was already inconsistent with settled D1 design.
  - **Consequence — two `TestG0FixedSeedEndStates` pinned values changed** (`test_seed_1_named_sergeant_zahna_broken`, `test_seed_5_named_mordai_double_condition`): both fight a light-armored City Watch Sergeant, and both previously relied on `_pc_strike` silently downgrading the PCs' Tier 2 hits against it. With that line removed, the Sergeant now takes full-tier Conditions and goes down faster (exchange 5→3 and 13→5 respectively; Zahna no longer gets Broken in the first scenario). Recomputed both pinned tuples by running the scenario directly rather than guessing, and added an inline note on each explaining this is D1's settled design finally reaching this code path, not an unintended G0 divergence — the file's top-of-class note about "not part of the G0 baseline" (added to `TestArmorDowngradeSemantics` in this same pass) makes the boundary explicit: G0 pins the WS-A0 extraction, not subsequent intentional rule changes. Guardian-fighting G0 tests (heavy armor) were unaffected — checked why: a PC Strike's `condition_tier` is only ever 0/1/2 (Tier 3 is never a direct Strike outcome, only an escalation), so the old "heavy only gates Tier 3" branch was already inert for every `_pc_strike` call before this change; removing it changed nothing numerically for Guardian fights.
  - Also marked `test_combat_characterization.py`'s `TestArmorDowngradeSemantics` (the two-arg-signature pin from A0.1) superseded in place, same pattern as A0.4 used for `simulation_log.md` — explains why the old shape was itself the bug, points at `test_combat.py` for current coverage, does not delete the section.
  - **Breakability assertion (Brain, EF6):** wrote it exactly as specified — fixed policy (PC always Absorbs, enemy always lands the same Tier 2 type every exchange, both deterministic since Absorb doesn't roll and NPCs don't roll) — and asserted the *exact* exchange Broken lands on for each of none/light/heavy, not a band. Computed by hand first, then confirmed by running: **none → exchange 2, light → exchange 4, heavy → exchange 6** — matching DESIGN §4.2's own worked numbers exactly. `heavy > light > none` and `light ≤ 2×none` (4 ≤ 4) both hold, satisfying G2's pass condition shape ahead of A8 actually running G2.
  - Added 2 new integration tests to `test_websocket.py` (`TestCombatGameplayLoop`): budget exhausting after exactly 2 light-armor hits (3rd passes through unmodified), and budget surviving a `combat_end`/`combat_start` pair unchanged — the "two fights share the budget" behavior, not just the pure-function version of it in `test_combat.py`. Updated the existing `test_heavy_armor_downgrades_tier3_to_tier2` docstring (behavior unchanged for a single hit, since `tiers_reduced=1` applied once still gates Tier 3→2 — only the docstring's "one-step gate" framing was stale) and `TestCombatRulesParity`'s parity test to call the new signature via `armor_budget`.
  - **Result:** full suite **838 total, 837 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, same as every prior entry).
  - **Files changed:** `software/app/game/combat.py`, `software/app/game/character.py`, `software/app/api/websocket.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py`, `software/tests/test_combat_characterization.py`, `software/tests/test_websocket.py`.
  - **Status:** A5 complete, not yet committed. A6 (retire the 0-Endurance rule) is next.

- **A6 — Retire the 0-Endurance rule.** *(DESIGN §4.3)*
  - `app/game/combat.py`: removed the `is_zero_end_absorb` parameter and its escalation block from `apply_condition` (was: any Tier 1 hit taken at 0 Endurance was force-upgraded to a persistent Tier 2, using `_default_tier2_id` to pick which). Deleted `_default_tier2_id` outright — its only caller was the removed block. Rewrote the function's docstring to state the new behavior plainly: no special-casing for 0 Endurance, an Absorb at 0 End takes the incoming tier unmodified. `is_rider` (D1, A4) is untouched — a separate flag with no interaction with this one.
  - **Scope note — touched `tools/combat_sim.py`, outside A6's stated `Files:` list, for the same reason A5's LOG entry gives: the accept criterion is "no `is_zero_end_absorb` reference remains anywhere," and the simulator was the only real caller of the flag (`websocket.py` never passed it).** Two call sites relied on it:
    - `_pc_strike` (PC Strike landing on an enemy) computed `is_zero_end` from `target.endurance_current` and threaded it through to the condition/print logic. Deleted the computation and the kwarg; the `[persistent]` print annotation (which only ever fired under the retired rule) came out with it.
    - `_enemy_attack`'s `reaction == "absorb"` branch (PC absorbing an enemy attack) had the same shape, plus an explicit `if is_zero_end and final_tier > 0: final_tier = max(final_tier, 2)` override *after* `armor_downgrade` ran — this was the actual gameplay-affecting line (the other call site's target is an enemy, whose Condition-as-kill-track was already dissolved by D1/A4). Deleted the override; `armor_downgrade`'s returned tier now passes through to `apply_condition` unmodified.
  - **Consequence — pinned end-states changed again, this time by an actual lethality drop, not a bugfix reaching a new code path (contrast A5's note above).** DESIGN §4.3 predicts this explicitly: "PC lethality drops relative to every recorded simulation... Gate G2 must re-baseline them." Recomputed three `TestG0FixedSeedEndStates` scenarios by running them directly rather than guessing:
    - `test_seed_1_named_sergeant_zahna_broken`: same shape (win, 3 exchanges, nobody Broken), small numeric drift (sparks_spent 6→7, Sergeant takes a second `winded` instead of an escalated persistent Tier 2).
    - Seed 2 against the Archive Guardian **changed qualitatively**: previously hit the `MAX_EXCHANGES` safety cap with all three PCs Broken and the party losing (`party_wins=False`) — that outcome depended entirely on the 0-End escalation snowballing Absorbed hits into persistent Tier 2s across a long grind. With it retired, the party survives well enough (only Mordai Broken) that the Boss dies before the timeout, `party_wins=True`. Renamed the test from `test_seed_2_boss_timeout_party_wipe` to `test_seed_2_boss_defeated_zero_end_retired`, since the old name asserted a fact about the scenario that is no longer true — keeping a name that describes a loss on a test that now asserts a win would be actively misleading to the next reader, not just stale. Docstring explains the flip and points at A8/G2 as the task responsible for deciding whether the *new* numbers are the ones worth keeping.
    - `test_seed_3_boss_defeated_after_phase_change`: same shape (win, Boss reaches phase change and Broken), exchange count moved 8→11 and Mordai now carries a lingering `staggered` instead of clearing clean.
    - All three carry a docstring note pointing at this file's module-level explanation of why re-pinning a value after an intentional rule change is not a G0 regression — G0 (A0.3) pins the *extraction*, once, and stays pinned; it does not re-freeze after every subsequent task that legitimately changes what the simulator computes.
  - **`test_combat_sim.py` fixes, same "full suite green" necessity as above, not new scope:**
    - `test_mook_attack_is_t1`: previously forced `endurance_current = 0` specifically to trigger the escalation and then asserted the *escalated* Tier 2 id showed up — inverted to assert a Mook's Tier 1 attack now lands as Tier 1 even when Absorbed at 0 End (no `staggered`/`cornered`).
    - `TestBossPhaseChange._apply`: dropped the now-nonexistent `is_zero_end_absorb` kwarg from its two direct `apply_condition(..., "staggered", 2, ...)` calls — these always passed tier 2 explicitly, so the flag was already inert here (the retired block only ever fired for `tier < 2`); removing it is a pure signature fix, not a behavior change.
    - `test_seven_chickens_harder`: broke for a different reason than the others — Mooks only ever inflict Tier 1, and without the escalation a Mook swarm can no longer push a PC to a persistent Tier 2 at all, so both 3- and 7-chicken runs sit at the 1.0 win-rate ceiling (`assert result_7.win_rate < result_3.win_rate` now compares `1.0 < 1.0`). Dropped the win-rate assertion; kept `mean_exchanges` (1.6 vs 3.6, still strictly ordered) as the signal that 7 chickens are harder than 3 — added a docstring note that chicken-baseline *win rates* are superseded corpus per A0.4 and full recalibration is A10's job, this fix only keeps the suite honest about what the assertion can still prove.
  - `research/armored_enemy_breaking_problem.md`: marked **RESOLVED**, not deleted. Added a resolution section at the top explaining the problem is dissolved rather than fixed — D1 removes the enemy Condition kill-track this doc's "infinite loop" analysis depended on entirely, and D2's per-scene downgrade budget (A5) independently closes the player-side mirror of the same bug. Left the original Options A–E analysis below a horizontal rule as historical record, per this project's stated preference (see A0.4's precedent) for marking superseded material rather than deleting the trail that shows how an error was found and reasoned through.
  - **Result:** full suite **838 total, 837 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, local `.env` `PORT=8010`, same as every prior WS-A entry — confirmed unrelated by its presence on a clean stash before this session's changes, per C11's note).
  - **Files changed:** `software/app/game/combat.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py`, `software/tests/test_combat_characterization.py`, `software/tests/test_combat_sim.py`, `research/armored_enemy_breaking_problem.md`.
  - **Status:** A6 complete, not yet committed. A7 (phase changes end-to-end) is next.

- **A7 — Phase changes end-to-end.** *(TDD)*
  - Wrote 3 tests in `tests/test_websocket.py::TestEnemyTrackerWS` first (red step confirmed: `test_enemy_phase_change_fires_on_threshold_cross` hung on a `receive_json()` for an event the server never sent — no `pytest-timeout` is configured in this repo, so confirmed the hang was real and bounded it with a shell-level `timeout 30` rather than letting it block indefinitely, then implemented).
  - **Scope note — touched `app/game/combat.py`, outside A7's stated `Files:` list (`websocket.py`, `test_websocket.py`, `MM1_Encounters_and_Enemies.md`).** `apply_resolve_damage`'s existing phase-crossing loop (from A4) is keyed to an *outcome*-driven depletion, but `_handle_enemy_update` sets `resolve_current` directly from a client-supplied value — there is no "outcome" to hand it. Extracted the crossing check into a new pure function, `phase_crossed(resolve_before, resolve_after, phase_thresholds) -> Optional[int]`, and rewrote `apply_resolve_damage` to call it (identical behavior, confirmed by re-running its existing 3 tests unmodified). This keeps the crossing rule in `combat.py` rather than re-implementing the `old > threshold >= new` check inline in the WebSocket handler — CLAUDE.md's Software-PHB Synchronization section is explicit that engine logic belongs in the game module, not the handler, and A0–A6 have consistently treated `websocket.py` as a thin caller into `combat.py`.
  - `app/api/websocket.py`'s `_handle_enemy_update`: captures `resolve_before = enemy.resolve_current` ahead of applying the update, then (only when the enemy has `phases` and had a non-`None` prior Resolve) calls `combat_module.phase_crossed(...)` against `[p.resolve_threshold for p in enemy.phases]`. Broadcasts the existing `enemy_updated` message first, then a new `enemy_phase_change` message (`enemy_id`, `phase_index`, `description`) as a second broadcast only when a crossing was detected. `enemy_id` carries the **tracker_key** (the active-combat instance key, e.g. `"Boss 1"`), not `enemy.id` (the library id, e.g. `"archive_guardian"`) — the tracker_key is what already uniquely identifies an active enemy everywhere else in the tracker protocol (`enemy_spawned.tracker_key`, `enemy_updated.tracker_key`), and multiple instances of the same library enemy can be on the field at once.
  - "Fires once, not repeatedly" needs no dedup flag: because the caller's own `enemy.resolve_current` is the `resolve_before` for the *next* call, once a value has crossed a threshold, every subsequent call's `resolve_before` is already at-or-below it, so `phase_crossed` naturally returns `None` — verified by the second test driving three sequential updates (5→2 crosses, 2→1 and 1→0 do not).
  - No `phases` on the enemy (the ordinary case for every enemy in the repo except the Archive Guardian) short-circuits before calling `phase_crossed` at all — third test confirms only `enemy_updated` is broadcast, nothing else, for a Named enemy with an empty `phases` list.
  - **Test-setup gap found, not fixed:** `CreateEnemyRequest` (`app/api/routes/enemy.py`) and `_handle_spawn_enemy`'s inline `enemy_data` path both lack a `phases` field, so there is currently no way to give an active enemy phases through the API/WS surface — only by loading one from a `.fof` with `phases:` already in it (only `archive_guardian.fof` has this) or by writing to `session.active_enemies[...].phases` directly, which is what the test helper does. Not in scope here (A7's `Files:` list doesn't include the enemy route or spawn payload); flagging for A12 (web app enemy tracker) since a phased enemy is currently unreachable from the MM UI.
  - `mm_manual/MM1_Encounters_and_Enemies.md`: re-keyed only the phase-*trigger* language (per C8's deferral and DESIGN §1 ledger row 7) — the "Special:" line in the Boss stat-block example and the "Phase changes are narrative triggers..." paragraph plus its Archive Guardian vignette, both changed from "when first Broken" / "Endurance reduced past a threshold" to "when Resolve drops to 2 or below" / "keyed to a `resolve_threshold`... crossed when a Strike depletes their Resolve," matching `enemies/archive_guardian.fof`'s canonical `phases:` block exactly (`resolve_threshold: 2`, "Reduced Mode"). Did **not** touch the surrounding Endurance-pool stat-block fields, the durability/TR tables, or the stale `TR: 16` — those are full-chapter D1/D2 rewrites that A11 explicitly gates behind G1/G2/G4, and this task's scope note in TASKS says only "phase-change prose."
  - **Result:** full suite **840 total, 839 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, local `.env` `PORT=8010`, same as every prior WS-A entry).
  - **Files changed:** `software/app/game/combat.py`, `software/app/api/websocket.py`, `software/tests/test_websocket.py`, `mm_manual/MM1_Encounters_and_Enemies.md`.
  - **Status:** A7 complete, not yet committed. A8 (Gate G0 re-verify, then run G1 and G2) is next.

- **A8 — Gate G0 re-verify, then run G1 and G2.** *(DESIGN §5)* **BLOCKED on G1 — escalated below.**
  - **Pre-existing gap found before any gate could run:** `tools/combat_sim.py`'s `_pc_strike` still resolved PC-Strikes-against-Named/Boss entirely on the pre-D1 model — Condition-stacking toward Broken via `apply_condition`'s same-type-Tier-2 escalation, with no calls anywhere to `apply_resolve_damage`, `mook_removed`, `target_strike_difficulty`, or `is_rider=True`. A4's and A5's own LOG entries (lines 123, 137) had already flagged this as deliberately deferred to A8 ("this is A8's job for G1/G2"), so this wasn't a surprise — but it meant G1/G2 could not be run at all against the actual shipped `combat.py` API until the simulator caught up. Migrated first, gates second.
  - **`app/game/combat.py`: added `enemy_armor_resolve_bonus(armor, ruleset)`** (TDD — 4 tests written first, confirmed red on `AttributeError`, then implemented as a one-line `getattr` against `enemy_durability.armor_resolve_bonus`, mirroring `apply_resolve_damage`'s lookup style). `Enemy.init_combat()` in `app/game/enemy.py` was deliberately **not** switched to call it — A4's LOG already made the call not to plumb a ruleset through that method's signature, and revisiting that tradeoff is outside A8's scope. The new function exists for `combat_sim.py`'s use, which already threads a ruleset everywhere.
  - **`tools/combat_sim.py` — full migration of the enemy-durability model to D1:**
    - `EnemyState`: `endurance_max`/`endurance_current` → `resolve`/`resolve_current`; dropped `is_broken` (enemies have no Broken track under D1 — defeat is `is_removed`, same representation a Mook removal already used) and the old ad-hoc `has_phase_change`/`phase_changed`/`phase2_endurance`/`phase2_attack_mod`/`phase2_ignores_t1` fields, replaced with `phases: list[dict]` (the enemy's authored, purely-narrative `resolve_threshold`/`description` pairs, matching `Enemy.phases`/`PhaseDef` exactly) plus `phase_index` (informational, mirrors `ResolveDamageResult.phase_index`) and `special_attack_mod`/`special_ignores_tier1` — **not** a generic engine mechanic, these model an individual boss's authored "Special" stat-block text (Archive Guardian's Reduced Mode specifically) so the simulator's numbers reflect that published enemy, the same judgment call A4 made for enemy armor's flat Resolve bonus (LOG line 122: "boss-specific flavor, not a generic engine mechanic").
    - `_pc_strike` rewritten: Mook removal now calls `combat_module.mook_removed(outcome, armored, ruleset)` (armored Mooks need a full success — previously any success removed *any* Mook regardless of armor, an unexercised gap since no armored-Mook def existed yet). Named/Boss resolution: target may Parry (unchanged AI policy, `should_enemy_react`/`reaction_cost`/`roll` against `defense_modifier`) — a full-success Parry now fully deflects the Strike (no Resolve loss, no rider, matching DESIGN §4.1's napkin check: "the Boss's reactions negating roughly one Strike per exchange"); a partial-success Parry downgrades the Strike's *outcome* one step via a new `_downgrade_outcome` helper (full_success→partial_success→failure) rather than downgrading a Condition tier, since D1 keys both Resolve depletion and the rider off the outcome directly, not a tier number. `apply_resolve_damage` then depletes Resolve by the (possibly downgraded) effective outcome; a genuine (non-downgraded) full success may additionally impose a rider via a new `_choose_rider` AI-policy helper — **deliberately always prefers an unheld Tier 2 id** ("the most aggressive policy available, so G1 measures the worst-case rider→Easy snowball rather than an averaged one," per the function's docstring), falling back to a Tier 1 rider (`"winded"`, or nothing if the target's `special_ignores_tier1` flag is set and its phase has already changed) only once both Tier 2 ids are already present.
    - `_mark_broken` simplified to PC-only (a one-line `target.is_broken = True` plus docstring) — its old `isinstance(target, EnemyState)` phase-change branch is now dead code since enemy defeat comes from `apply_resolve_damage.defeated`, not a Condition escalation reaching this function at all.
    - `_choose_condition` (PC-side Broken-track picker, used by `_enemy_attack`) is untouched and still in play — D1 only retired the *enemy*-side Condition-as-kill-track, not the PC-side one. It now has a docstring note pointing at `_choose_rider` as its enemy-side, non-escalating counterpart, so a future reader doesn't conflate the two.
    - Canonical enemy defs (`city_watch_sergeant_def`, `veteran_soldier_def`, `archive_guardian_def`) rewritten to the exact base `resolve` values published in `enemies/*.fof` (3, 4, 5 respectively) rather than the stale legacy Endurance numbers (6, 6, 10) they still carried — those legacy values would have given every Named/Boss roughly double its correct Resolve pool had they gone untouched, silently invalidating both gates before they even ran. `veteran_soldier_def`'s `attack_modifier`/`defense_modifier` were also wrong (2/2, published file says 3/3) — fixed to match. `generic_named_def`/`generic_boss_def` (used only by Series A–F, not G1/G2) were rebased onto plausible post-D1 Resolve numbers reasoning back from their TR formula, with an explicit docstring disclaimer that full recalibration against these is Gate G4 / task A10's job, not this task's — deliberately not chasing exact TR precision for the `generic_boss_def(16)` branch, which was already imprecise pre-A8.
    - `run_combat`'s Withdrawn-recovery block for enemies renamed to the Resolve fields; the "Boss phase 2: ignore Tier 1 Conditions" end-of-exchange filtering block was **removed as dead code**, not ported — `_choose_rider` already refuses to add a Tier 1 rider once `special_ignores_tier1` and a phase change are both true, and the standard `end_exchange` call already clears any Tier 1 Condition every exchange regardless of phase, so the block could never produce an observable difference from omitting it.
  - **`tests/test_combat_sim.py` updates** (TDD where new behavior was added, direct fixes where only field names moved): `TestAI`/`TestPCStrike` field renames; three new `TestPCStrike` tests (`test_named_resolve_depletes_on_success`, `test_no_rider_on_partial_success`, `test_armored_mook_needs_full_success`) covering the D1 behavior the old tests couldn't exercise at all. `TestBossPhaseChange` rewritten from scratch — the old class drove `apply_condition`'s Broken escalation directly to trigger what it called a "phase change"; the new one drives `_pc_strike` end-to-end and asserts on `phase_index`/`attack_modifier`, plus a `test_defeat_is_removal_not_broken` test making the is_removed-not-is_broken representation explicit. `TestDefinitions` updated to the correct Resolve values (including the armor-bonus-adjusted `resolve_current`). Two `TestCalibration` tests hit a ceiling-effect exactly like A6's `test_seven_chickens_harder` (`test_named_npc_longer_than_mooks`/`test_boss_harder_than_named`, both driven by `generic_named_def`'s now much-smaller Resolve pool making it as fast to remove as a 3-Mook swarm): consolidated into one `test_boss_harder_than_named` comparing `mean_exchanges` (a signal that survives) instead of `win_rate` (pinned at the 1.0 ceiling for both), with a docstring pointing at A10 for the full recalibration this exposes.
  - **G0 re-verified — pinned values recomputed, not a regression** (same pattern A5/A6 established: G0 pins the WS-A0 *extraction*, once; it does not re-freeze after a subsequent task that legitimately changes what the simulator computes). `test_combat_characterization.py`'s `_enemy_state` helper updated to the new field/shape (`is_broken` dropped, `phase_changed`→`phase_index`). All four Named/Boss-fight fixed seeds recomputed by running the scenario directly (not guessed) — fights now resolve in 1–2 exchanges instead of 3–20, since Resolve pools (3–7) are far smaller than the Endurance pools (6–10) these seeds were originally pinned against. `test_seed_3_boss_defeated_after_phase_change` renamed to `test_seed_3_boss_defeated_no_phase_change` — this seed's Guardian is defeated before crossing its Resolve-2 phase threshold, unlike seed 2's, so the old name's guarantee no longer holds on this seed specifically. The Mook-only `test_seed_1_mook_wipe` was untouched and unaffected, as expected.
  - **Full suite: 848 total, 847 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, local `.env` `PORT=8010`, same as every prior WS-A entry).
  - **Gate G2 — PASSED.** Full results, methodology, and the F6/F5 independent-factor diagnostic in `research/simulation_log.md` Series 7. Summary: the deterministic worst-case proof from A5 (T_broken = 2/4/6 for none/light/heavy) still holds unchanged and is the primary evidence per Brain's EF6 ruling (a probabilistic assertion cannot prove breakability); a realistic n=200 `run_combat` sim against the actual Veteran Soldier corroborates it (Broken observed for none/light at n=200, for heavy at n=2000 — rare, not unreachable, as expected). F6 and F5 varied independently: neither, alone or combined, produces the over-correction DESIGN §11 worried about.
  - **Gate G1 — FAILED, escalated.** See `## ESCALATION` below.
  - **Files changed:** `software/app/game/combat.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py`, `software/tests/test_combat_sim.py`, `software/tests/test_combat_characterization.py`, `research/simulation_log.md`, `docs/TASKS_v0.3_ruleset_revision.md`.
  - **Status:** A8 blocked — G2 done and logged; G0 re-verified; G1 escalated. Do not proceed to A9–A12 or III.3/MM1 prose (DESIGN §5's ordering constraint: "G1/G2 before III.3 or MM1 prose") until the escalation resolves.

## ESCALATION — Worker (A8) → Planner/Brain (2026-07-10)

**What was attempted:** Gate G1 (Archive Guardian, Resolve 5 base / effective 7 with heavy armor, vs the standard 3-PC party — `standard_party()`: Mordai, Zahna, Zulnut). Riders confirmed modelled live per Brain's EF1 ruling (a verbose single-seed trace shows the exact snowball DESIGN worried about: Mordai's 10+ applies a Staggered rider → Zahna's Strike is Easy → her 10+ applies Cornered → Zulnut's Strike is also Easy → the Guardian is dead in exchange 1). At the DESIGN-specified starting value (Resolve 5), n=200/seed=1: **win rate 100%, median exchanges 2** — both pass conditions (45–55% win rate, ≥3 median exchanges) fail simultaneously.

Two retunes attempted within the task's sanctioned band (Boss Resolve 2–6, per BRIEF): Resolve 5→6 (top of the band). Result: win rate still 100%, median exchanges still 2.0. Per the task's own escalation trigger ("Escalate after 2 failed retunes"), stopped retuning and instead ran a **diagnostic sweep outside the sanctioned band** (Resolve 8/10/15/20) to understand whether the knob works at all, before writing this escalation — full table in `research/simulation_log.md` Series 7. Findings: the median-exchange floor does eventually clear (Resolve 8+), but **win rate never approaches 45–55% even at Resolve 20** (four times the sanctioned band's top) — it bottoms out at 95.5%.

**What specifically is wrong:** Boss Resolve is a *durability* knob — it controls how long the Guardian survives, not how much threat it poses per exchange. G1's pass condition needs both a survivable-length fight (median ≥ 3 exchanges) *and* a competitive win rate (45–55%) simultaneously. A diagnostic trace and a targeting-policy A/B (default lowest-Endurance-first targeting vs. a random-target patch, both tested — identical ceiling) show the actual bottleneck is the Guardian's **offense**, not its durability: it gets exactly one attack per exchange, against one PC, and that PC's incoming Tier 2 hit is frequently avoided (a full Dodge/Parry) or only partially lands; Broken requires *two* same-type Tier 2 hits (D5 ledger row 2 / F6) on a single target — a cadence a solo single-target attacker essentially never sustains against three independently-acting, independently-recovering PCs before the party's combined offense (three Strikes per exchange, every exchange) grinds through any Resolve value, however large. This is not a bug in the D1 migration (the rider/depletion mechanics trace correctly, per the verbose scenario above) — it is a genuine finding about whether a by-the-book solo Boss (no Techniques, no extra actions, no allies) can ever be a fair fight against a full starting party under the exchange structure as currently specified.

**Why it blocks A8 (and DESIGN §5's ordering constraint):** G1 gates III.3/MM1 Boss-fight prose and Gate G4's Encounter Budget recalibration (A10) — both would be re-deriving numbers from a Boss configuration that cannot mathematically reach the intended difficulty band, which is exactly the class of error (recording numbers under a game nobody will actually get, cf. Q3 / F1) this whole ruleset revision exists to stop repeating.

**Options considered, not decided (a Worker's job is to surface these, not choose):**
1. **Give Bosses more than one action per exchange** (e.g., two attacks, or an attack plus a Technique) — the MM1 Boss-design guidance already implies Bosses are meant to need "Techniques, if the MM wants them to have specific capabilities" (III.3) and multiple Condition tracks; G1's "by-the-book, no Techniques" configuration may itself be the wrong test — a Boss's *baseline* stat block was never meant to be solo-viable against a full party without at least one Technique.
2. **Loosen G1's win-rate band or redefine it against a different party size / Boss configuration** (e.g., 2 PCs, or a Boss with one canonical Technique active) — changes the gate's pass condition rather than the game.
3. **Give the Boss more actions structurally** (a generic "Bosses act twice per exchange" rule) — this is a rules change with PHB/MM1 consequences beyond A8's scope, and DESIGN doesn't currently specify it.
4. **Accept that a solo, by-the-book Boss is not meant to threaten a full starting party's win rate** and rewrite G1's pass condition to measure something other than win rate (e.g., resource attrition — Sparks spent, Endurance remaining — as the "was this a real fight" signal instead).

None of these are a Worker's call: 1 and 3 are rules-design questions (Brain/Planner territory, touching MM1 and possibly III.3); 2 and 4 revise the gate DESIGN itself set. **Recommend switching to Opus (Planner) to triage which of these — or another option — resolves the finding, escalating to Fable (Brain) if it turns out to be a strategy-level question about what a "Boss" is meant to be** (matches the Planner→Brain trigger: "downstream robustness or scalability concern emerges that changes the approach").

**Resolved by Planner, 2026-07-10.** Full ruling in `docs/DESIGN_v0.3_ruleset_revision.md` §5-bis; TASKS A8 updated; tradeoff logged in `docs/DECISIONS.md` (P9). Summary:

- **The finding is confirmed and is not a bug** — it is an action-economy truth, and it *matches existing canon*: `enemies/archive_guardian.fof:44-47` already states a straight fight is "survivable but very expensive… intended to be solved laterally." The 45–55% coin-flip expectation contradicted canon the user set in March.
- **The 45–55% win-rate criterion is dropped** — it was void-derived (BRIEF "winnable at ~Hard rates" → the Encounter Budget "Hard ≈ 50% win" multiplier, which Brain's Q3 ruling voided wholesale). The §4.1 napkin check only ever engineered the exchange-length half; the win-rate band was never designed.
- **G1 is reframed as length-plus-cost** (Worker's Option 4): median ≥ 3 exchanges + defeatable + zero house rules + snowball-doesn't-collapse-below-3 + a recorded **cost signal** (Sparks spent, Endurance remaining, PC-Broken incidence) proving the fight was survivable-but-expensive. This matches the BRIEF's *binding* criterion (3+ exchanges, no house rules) rather than the voided descriptor.
- **The exchange-length floor (which failed at Resolve 5) is cleared by retuning Boss Resolve to ≈8** — the pre-authorized scalar lever (risk register: "retune, don't redesign"; §5 committed to Boss Resolve as the snowball lever). Your own diagnostic already located the floor at Resolve 8+. Widen the BRIEF's "working range 2–6" note to the confirmed ceiling; confirming the range must extend is what G1 was *for*.
- **Options 1 & 3 (structural Boss multi-action / mandatory Techniques) rejected** — a rules change against the minimize-complexity pillar. Boss-encounter difficulty is produced at the encounter layer (Encounter Budget adds/TR — Gate G4) and via the Boss's authored Techniques and lateral weaknesses (all in the Guardian's `.fof`, and all stripped by the G1 sim, so G1 tests a Boss *below* its TR-14).
- **One item handed to Brain, non-blocking:** the *ethos framing* that "a Boss baseline is not solo-viable; difficulty comes from the encounter layer" must land in MM1/III.3 prose (A11, which runs after G1/G2 per §5). Flagged for Brain to bless at prose time; blocks nothing now.

**Return to Worker to continue A8** from the revised G1 pass condition in TASKS A8. No Brain round-trip required to proceed.

## A8 — Worker resumes and closes (2026-07-10)

**Retune:** `archive_guardian_def()` (`tools/combat_sim.py`) and `enemies/archive_guardian.fof` both moved base `resolve: 5 → 8`. Confirmed the exact minimum by sweeping 5/6/7/8/9 at n=500/seed=1 (median exchanges 2.0/2.0/3.0/3.0/3.0) and then stress-testing the 7-vs-8 boundary at n=200 across 7 seeds (1, 2, 3, 4, 5, 7, 42): Resolve 7 flips between median 2 and 3 depending on seed (seeds 1/4/5 → 2.0; seeds 2/3/7/42 → 3.0), while Resolve 8 holds median exactly 3.0 in all 7 — confirming 8, not 7, as the smallest value that *robustly* clears the floor rather than merely hitting it on the sanctioned seed. Published TR recomputed 14 → 17 (offense 5 + resolve 8 + armor 2 + techniques 2), verified against `Enemy.calculate_tr()` directly, not just by hand.

**Canonical G1 run** (n=200, seed=1, `run_simulation`): 100% win rate (95% CI 98.1–100%), median 3.0 exchanges, mean 2.8, mean Sparks spent 6.2/9, mean PCs Broken 0.03, Endurance remaining at fight end down to 0 for Zahna in the worst runs. All revised pass-condition elements met: median ≥ 3 ✓, every enemy defeatable (100% across 200 runs) ✓, zero house rules ✓, snowball does not drive median below 3 (held at exactly 3.0 across the 7-seed check) ✓, cost signal recorded (Sparks + Endurance + Broken incidence above) ✓. Full data and the seed-robustness table in `research/simulation_log.md` Series 7's new "G1 — RE-RUN under revised pass condition — PASSED" subsection.

**Files touched beyond the two named in TASKS A8:**
- `docs/BRIEF_v0.3_ruleset_revision.md` — D1's "working range 2–6" widened to 2–8, with a note that the extension is a Boss-tier finding (Named 3–4 unaffected).
- `docs/DESIGN_v0.3_ruleset_revision.md` — §4.1's "Starting values" paragraph gets a confirmation note (Resolve 8, not the original 5, with the napkin-check's blind spot named: it assumed Hard-difficulty Strikes throughout and didn't anticipate the rider→Easy snowball); §5-bis gets a short closing note recording the sim numbers and that A8 is closed.
- `software/facets/base/facet.yaml` — added a documentation comment under `enemy_durability` recording the confirmed Named/Boss Resolve band (this is guidance for enemy authors, not an enforced field; actual values stay per-enemy in each `.fof`, per the C1 "simulator/config may never reimplement a rule" boundary — the working range is documentation, not a new mechanic).
- `software/tests/test_combat_sim.py` (`test_guardian_is_boss`) and `software/tests/test_combat_characterization.py` (the two Guardian G0 fixed-seed pinned tests, renamed `test_seed_2_boss_defeated_no_phase_change` / `test_seed_3_boss_defeated_after_phase_change` since which seed crosses the phase threshold flipped) — recomputed and re-pinned against the new Resolve value. This is a content retune (the Guardian's authored stat changed), not an engine regression, matching that file's own module docstring guidance on when re-pinning is the correct response rather than "fixing" the test.

**Full suite: 847 passed, 1 pre-existing unrelated failure** (`test_config.py::TestSettingsDefaults::test_default_port_is_8000` — a local `.env`/environment PORT override, not touched by this task; matches the "1 pre-existing unrelated failure" already noted in A8's G0 re-verify line).

**A8 is CLOSED.** Per DESIGN §5's ordering constraint ("G1/G2 before III.3 or MM1 prose"), A11 (PHB III.3 + MM1 prose) and A10 (Gate G4) are now unblocked with respect to A8, and WD6's recovery section (which explicitly deferred to "after A8") may proceed. A9 (Gate G3, independent) was never blocked.

## A9 — Gate G3: Aggressive posture knob K1 (2026-07-10)

**DESIGN specified only the PC and the comparison ("Unarmored Endurance-3 PC, Aggressive vs Measured, baseline vs K1, n≥200") — enemy composition, fight length, and the win-rate definition were left to the Worker.**

- Zahna's canonical stat block (`zahna_def()`) already matches "Endurance-3 unarmored" exactly — reused directly rather than inventing a new PC.
- **First attempt (fight-to-conclusion) failed to find any signal.** 1 PC vs 2 weak Named enemies, run to a real conclusion (win = both defeated, loss = Broken): Aggressive and Measured baseline landed at statistically indistinguishable ~84% Broken (n=1000, seed=1). Diagnosed why: a reaction ROLL's success chance never depends on posture, only the Endurance to attempt one does, and over a multi-exchange war of attrition cumulative Tier 2 exposure converges every posture toward the same Broken ceiling regardless of how fast a posture burns Endurance early on. The "Aggressive death-spiral" PT01/BRIEF D8 describe is an opening-exchange alpha-strike phenomenon, not a long-run average — only visible in a bounded window.
- **Final design:** bounded to exactly 2 exchanges (`G3_EXCHANGES`), fixed posture throughout (bypasses `choose_pc_posture`), PC's own Strike made Press/Spark-free (`_g3_pc_strike` — `should_press` was confounding the experiment by pre-spending Endurance Zahna's Endurance-3 pool couldn't spare), "win" = both enemies cleared within the window (an offense-edge proxy, unaffected by K1 since K1 never touches the Strike modifier — a sanity check, not a real risk K1 threatens).
- Implemented as a fully self-contained harness (`_g3_pc_def`, `_g3_named_def`, `_g3_enemies`, `_g3_reaction_cost`, `_g3_pc_reacts`, `_g3_pc_strike`, `run_g3_fight`, `run_g3_gate`, `g3_verdict`, `print_g3_result`) rather than threading a flag through the shared `run_combat`/`_enemy_attack`/`choose_pc_reaction` — those are exercised by every other Series and already under test; a knob that might be rejected had no business touching them. Wired into the CLI as `--series G3`.
- **Result, n=3000/seed=1:** Broken-rate cut (Aggressive, baseline→K1) 15.7% (bar ≥15%); win-rate delta preserved within 0.6pp (bar ±5pp). Right at the pass boundary on the primary metric, so ran a **7-seed robustness check** (1,2,3,4,5,7,42) before trusting it — every seed cleared both bars with margin (cut 15.7%–18.7%, delta always ≤0.6pp). Full table: `research/simulation_log.md` Series 8.
- **Escalated the adoption decision to the user before proceeding**, given (a) the methodological latitude required to construct any measurable scenario at all and (b) adoption being a permanent core-combat rule change. Presented three options (adopt now / record-but-don't-adopt / redesign the gate) with the full caveat about the rejected fight-to-conclusion design. **User chose: adopt now.**
- **Adopted K1 as the canonical rule** (not just an experimental knob):
  - `facet.yaml`: `combat.postures.aggressive.reaction_cost_modifier_applies: first_reaction_only`.
  - `app/game/combat.py`: `reaction_cost(reaction, posture, ruleset, is_first_reaction=True)` — new optional param, defaults `True` so callers that don't track per-exchange reaction counts (an enemy's Parry in the simulator) see unchanged behaviour. `resolve_reaction` threads it through. TDD: 5 new tests in `TestReactionCost`, confirmed red (`TypeError: unexpected keyword argument`) before implementing.
  - `app/game/character.py`: `Character.reactions_this_exchange: int = 0` (ephemeral combat state, alongside `armor_downgrades_remaining`).
  - `app/api/websocket.py`: `_handle_react` computes `is_first_reaction` from the counter before incrementing it, passes it into `reaction_cost`; `_handle_end_exchange` resets the counter to 0 for every character alongside the existing Tier 1 clear. 3 new tests in `TestCombatGameplayLoop` (first reaction pays surcharge, second reaction in the same exchange doesn't, counter resets on `end_exchange`).
  - `tools/combat_sim.py`: `PCState.reactions_this_exchange` added and reset each exchange in `run_combat`; `_enemy_attack` (the **shared** function every other Series calls, not just G3) now computes `is_first_reaction` and passes it to `combat_module.reaction_cost` — K1 is live for the whole simulator, not just the gate that discovered it, per the C1 rule that the simulator must reflect the canonical ruleset. `_g3_reaction_cost` simplified to delegate to the now-canonical `combat_module.reaction_cost` for both branches — `k1_enabled=False` forces `is_first_reaction=True` unconditionally to reproduce the *pre-adoption* baseline through the same function, rather than keeping a second copy of the old rule. Re-ran the gate after this refactor to confirm it reproduces the exact same numbers (15.7% cut, seed=1) — it does.
  - `player_handbook/III.3_Combat.md`: Postures table + "Aggressive:" prose + Reactions section + combat quick-reference card all updated to "first reaction of the exchange only."
  - `mm_manual/MM5_Quick_Reference.md` and `player_handbook/Quick_Start.md`: matching one-line updates (compression, not paraphrase, per C1).
- **Full suite: 856 total, 855 passed, 1 pre-existing unrelated failure** (`test_config.py::TestSettingsDefaults::test_default_port_is_8000`, local `.env` `PORT=8010`, unchanged from every prior entry).
- **Files changed:** `software/facets/base/facet.yaml`, `software/app/game/combat.py`, `software/app/game/character.py`, `software/app/api/websocket.py`, `software/tools/combat_sim.py`, `software/tests/test_combat.py`, `software/tests/test_websocket.py`, `player_handbook/III.3_Combat.md`, `mm_manual/MM5_Quick_Reference.md`, `player_handbook/Quick_Start.md`, `research/simulation_log.md`, `docs/DECISIONS.md`, `docs/TASKS_v0.3_ruleset_revision.md`.

**Status:** A9 CLOSED — ADOPTED. Not committed yet. Per Worker protocol, stopping here to report before starting the next task (A10 or A11 — both independent of A9).

## ESCALATION — Worker (A10) → Planner (2026-07-10)

**What was attempted:** Gate G4. Re-ran the task's five named baselines — 3/5/7 chickens, a solo City Watch Sergeant (TR 8), a solo Archive Guardian (TR 17) — against `standard_party()` (Party Strength 3), n=200/seed, seeds 1–3. Full data in `research/simulation_log.md` Series 9.

**Result: all five baselines land at 100% win rate.** None reproduces its target band (chickens are fine at Skirmish; the Sergeant was meant to probe Standard ~75%, the Guardian Hard-or-Deadly — both came back at the ceiling). This is not a one-off: I swept enemy count and per-enemy TR independently (Part B of Series 9, ~20 additional configurations, 3 seeds each) to check whether it was a solo-enemy quirk. It is not:

- **A solo enemy of any TR is ~100% win**, including the Guardian at TR 17 — matches the already-resolved A8/G1 finding, now confirmed to generalize to Named NPCs of every tested TR, not just the Guardian specifically.
- **Two Named/Boss enemies of any tested TR are still ~97–100%** (only two *Bosses* specifically dip to ~82%).
- **Three Named-tier enemies is where a real fight starts** — but per-enemy TR dominates within that count: 3× TR8 → 81% win, 3× TR10 (only 25% more weighted TR) → 40% win, adding one TR-1 Mook to the 3× TR8 group → ~50% win.
- **Four Named-tier enemies of any tested TR is already ≤ 25% (Deadly-or-worse); five is ≤ 3.5%.**
- **Mook swarms cannot produce Standard/Hard/Deadly at all.** Mean PCs Broken stays exactly 0.00 through 30 Mooks — the party is never actually threatened. The only way a Mook swarm's win rate drops is hitting the `MAX_EXCHANGES = 20` safety-cap timeout (40+ Mooks), which is a simulator artifact, not a real defeat.

**What specifically is wrong:** the task frames retuning as adjusting `difficulty_multiplier` and/or `action_economy_multiplier` — both scalar constants in a linear, separable formula (`effective_tr = Σ(TR_i × tier_weight) × group_size_modifier(count)`, compared against `party_strength × multiplier`). The measured relationship is neither linear nor separable in the way that formula assumes: it's a steep, **actor-count-gated threshold** (flat ~100% for 1–2 Named/Boss enemies regardless of TR magnitude, a cliff across 3–5, TR mattering only as a second-order modulator once past the count gate). No values of `TIER_WEIGHTS`, `group_size_modifier`, or `difficulty_multiplier` can reproduce this: the current formula already assigns 1 Guardian (TR 17) a *higher* weighted TR (21.25) than 3 Sergeants (24.0 is close, but win rates are 100% vs 81% — not remotely comparable at that TR gap) and a *lower* one than 4 Sergeants (35.2, 20% win) — but "trivial / genuine fight / Deadly" is exactly backwards from the counts (1, 3, 4) if TR-weighted-sum were the real predictor. The independent variable that actually predicts difficulty is enemy count, which the formula only nudges via a 1.0–1.25 group-size modifier — nowhere near strong enough to dominate the way the data requires.

**I did find working recipes for all four bands** (Series 9 Part C, 3 seeds each): Skirmish = 3–7 Mooks; Standard = 3× Named(TR8), 81/81/75%; Hard = 3× Named(TR8) + 1 Mook, 48.5/57.5/57.5%; Deadly = 4× Named(TR8) or 3× Named(TR8) + 2 Mooks, ~20%. These satisfy the task's literal Accept criterion ("measured win rates inside the bands") as worked Recipe Table examples — which is already how MM1 instructs MMs to use the table (pick column, pick row, use the composition — not derive it from raw budget math). What I can't do as a Worker is decide whether the *budget formula itself* — the tool MM1 also publishes and calls "how you calibrate an encounter's difficulty before running it" — should keep claiming to be predictive for 3+ Named/Boss rosters, given it demonstrably isn't and no constant retune fixes that.

**Why it blocks A10 (and A11, gated on A10 per DESIGN's ordering constraint):** A11 is PHB/MM1 prose that must describe the Encounter Budget honestly. Shipping A10 by only patching the four numeric constants would either (a) fail to hit the bands (constants literally cannot, per the analysis above) or (b) hit the four *listed* recipes while silently mis-predicting every other composition an MM might build from the same table — repeating the exact class of error (a calibration tool that looks authoritative but measures the wrong thing) this ruleset revision exists to stop.

**Options considered, not decided (a Worker's job is to surface these, not choose):**
1. **Demote the raw TR-budget formula to a rough sanity check, non-predictive for 3+ Named/Boss enemies**, and make the Recipe Table (worked, simulated examples) the MM's actual tool — closest to current MM1 text, which already tells MMs to use the table directly and separately notes (line 356) "Named NPC count matters more than total TR." This mostly means rewriting the Encounter Budget section's framing/caveats, not the engine; `TIER_WEIGHTS`/`group_size_modifier` could stay as a loose heuristic or be left alone.
2. **Rebuild `calculate_effective_tr`'s formula around actor count as the primary term** (e.g., a steep multiplier keyed to the number of simultaneously-acting Named/Boss enemies, TR as a secondary adjustment) — more accurate, but a genuine engine/architecture change to what "Threat Rating" and "Encounter Budget" mean project-wide, with knock-on effects for every future enemy stat block and the MM1 chapters that explain TR. This is Planner-scope architecture, not a constant retune.
3. **Treat this as confirming, at scale, the already-Planner/Brain-resolved G1 finding** (`docs/DESIGN_v0.3_ruleset_revision.md` §5-bis: "Boss-encounter difficulty is produced at the encounter layer... via the Boss's authored Techniques and lateral weaknesses" and "a Boss baseline is not solo-viable; difficulty comes from the encounter layer" — the non-blocking ethos note handed to Brain for A11) and extend that same doctrine explicitly to Named NPCs and multi-enemy math, rather than treating G4 as a separate numeric-calibration problem.

Option 3 reads to me as consistent with what's already been ruled, but the exact MM1 wording change and whether to touch `encounter.py`'s formula at all (option 1 vs 2) is a judgment call the DESIGN doc doesn't currently make, and directly determines what A11's Encounter Budget prose is allowed to say. **Recommend switching to Opus (Planner) to rule on this before A10/A11 continue.**

**Data:** `research/simulation_log.md` Series 9 (full tables, all seeds, reproduction instructions). No code changed yet — `software/app/game/encounter.py` and `software/tests/test_encounter.py` are untouched pending the ruling, so the constants (and any new tests) can be written once a direction is chosen instead of guessed at twice.

**Resolved by Planner, 2026-07-10.** Full ruling in `docs/DESIGN_v0.3_ruleset_revision.md` §5-ter; TASKS A10 scope + Accept revised; tradeoff logged in `docs/DECISIONS.md` (P10). Summary:

- **The finding is confirmed and is Option 3 — G1's §5-bis doctrine confirmed at scale and extended to Named NPCs.** Simultaneously-acting Named/Boss actor count is the primary difficulty variable; weighted-TR-sum is not. No new doctrine ruling was needed — this is the stance §5-bis already established, now generalized past the solo Boss.
- **Option 2 (rebuild the formula around actor count) is rejected for A10.** The win-rate→multiplier mapping the formula encodes was *already void* (Brain Q3); rebuilding it resurrects a void artifact, tries to fit a smooth model to a cliff function, and rests on only ~20 validated configs. Recorded instead as a **deferred, non-blocking Brain/product-scope open question** (should the app eventually grade arbitrary rosters?) — it does not gate A10.
- **Option 1 is the mechanical execution.** The MM1 **Recipe Table** (simulation-validated compositions) becomes the MM's authoritative tool; the raw `TR × multiplier` budget is demoted to an explicitly-non-predictive rough check. This matches how MM1 already tells MMs to build encounters and how the line-356 note already hedges.
- **`encounter.py`: make the formula honest, not precise** — docstrings state it's a rough heuristic, non-predictive for 3+ Named/Boss rosters, pointing at the Recipe Table. **Do not** retune constants to hit only the four listed recipes (that is the mis-prediction trap this escalation named). Tests move to sim-level recipe characterization + formula-level rough-ordering assertions (revised Accept in TASKS A10).
- **Prose framing rides on the ethos note already handed to Brain in §5-bis** (extended by §5-ter to Named/multi-enemy), blessed at A11 prose time. **No Brain round-trip is required to unblock A10.**

**Return to Worker to execute A10** under the revised scope + Accept criteria in TASKS A10.

---

## A10 — Gate G4: Encounter Budget recalibration — CLOSED (2026-07-10, Worker)

Executed under the revised scope + Accept in TASKS A10 (DESIGN §5-ter). The escalation's own simulation work (Series 9) already produced the calibrated data; A10 shipped it as the honest deliverable and demoted the formula.

**1. `encounter.py` — formula made honest, not precise.** No constants retuned (per §5-ter's explicit "do not retune to hit the four recipes" instruction). Docstrings rewritten to state the TR budget is a rough ordering check, explicitly non-predictive for 3+ Named/Boss rosters and Mook swarms, superseded by the MM1 Recipe Table: class docstring, `difficulty_multiplier`, `calculate_budget`, `calculate_effective_tr`, `action_economy_multiplier`, and the `TIER_WEIGHTS` comment. The `calculate_effective_tr` docstring names the concrete mis-ranking (scores 2 Bosses above 4 Named while the sim has 4 Named far deadlier) so no future dev mistakes the non-predictivity for a bug.

**2. MM1 prose reframed honestly.** The Encounter Budget section now *leads* with "actor count drives difficulty, not total TR" (promoted from the old line-356 footnote), points MMs at the Recipe Table as the build tool, and presents the `×1/2/3/4` budget + action-economy multipliers as a rough ordering check only. Removed the false-precision "~95/75/50/25%" validated-win-rate column (void-derived, BRIEF Q3) — replaced with an "intended feel" column labelled as design intent, not validated output. The old 3-Sergeants worked example (which the raw budget flags "well above Deadly") is retained but re-purposed as the teaching example of the formula over-counting (sim: 3× TR-8 Named = Standard ~81%). Overview layer-3 bullet and the Quick-Reference build block both now front the Recipe Table + an actor-count rule of thumb.

**3. Recipe Table replaced with Series 9 Part C validated rosters (PS 3).** Skirmish = 3–7 Mooks (100%/100%/100%); Standard = 3× Named(TR8) (81/81/75%); Hard = 3× Named(TR8) + 1 Mook (48.5/57.5/57.5%); Deadly = 4× Named(TR8) or 3× Named(TR8) + 2 Mooks (~20%). Seeds 1/2/3 and n=200 cited. The old seed-42 PS-3 table (which claimed solo Named/Boss were Standard/Hard — directly contradicted by Series 9's "solo enemies are ~100% at any TR") was removed. PS-4 row is now explicitly flagged **un-simulated / unvalidated extrapolation** — Series 9 measured PS-3 only; per §5-ter I flagged the gap rather than guessing calibrated numbers. Scaling Notes corrected: the old "2 Named = Deadly" and "Mook difficulty peaks at 8–10" claims were both false per Series 9 (2 Named ≈ trivial; Mooks never threaten through 30) and are rewritten around actor-count-primacy.

**4. Tests.**
- `test_combat_sim.py::TestRecipeCalibration` (6 sim-level characterization tests): each of the four bands pinned to its recorded seed-1 win rate *and* asserted inside its target band, plus a monotonic actor-count-ladder test (Standard > Hard > Deadly). These guard the MM1 table against silent invalidation by a future engine/rules change.
- `test_encounter.py::TestFormulaIsRoughHeuristicNotPredictor` (4 formula-level tests): assert the demoted formula's *documented* rough-ordering behavior (monotonic in same-enemy count; boss > named > mook at equal TR; solo discounted) and pin the known actor-count mis-ranking (2 Boss scores 42.5 > 4 Named 35.2) as a deliberate limitation-guard against a future "fix" that retunes the constants into false precision. The old "≥3 tests on the changed multipliers" criterion is superseded (no multipliers changed).

**Verification:** `test_encounter.py` + `test_combat_sim.py` → 105 passed. Full suite → **865 passed, 1 failed** — the 1 failure is the pre-existing, unrelated `test_config.py::test_default_port_is_8000` (env `PORT=8010`), the same known failure logged at A8/A9; unrelated to this task. All 10 new A10 tests pass.

**A10 CLOSED.** A11 (PHB III.3 + MM1 prose) is now unblocked on the G4 side; its Encounter-Budget prose is written to the §5-ter framing (Recipe Table is the tool, budget is a rough check, actor count is the driver), Brain-blessed at prose time per §5-ter item 6.

---

## A11 — PHB III.3 + MM1 prose — CLOSED (2026-07-10, Worker; executed by Opus at user request)

All three prerequisite gates had passed (A8 = G1/G2, A9 = G3, A10 = G4), so A11 was unblocked. This task was the prose catch-up for the D1/D2 rules that already shipped in `facet.yaml`/engine during A1–A9; no code was changed. Files touched: `player_handbook/III.3_Combat.md`, `mm_manual/MM1_Encounters_and_Enemies.md`, `mm_manual/MM5_Quick_Reference.md`, `player_handbook/Quick_Start.md`.

**Grounding.** Every mechanic was read out of the shipped engine before writing, not from the DESIGN summary — `app/game/combat.py` (`apply_resolve_damage`, `target_strike_difficulty`, `armor_downgrade`, `mook_removed`, `phase_crossed`), `app/game/enemy.py` (`calculate_tr`: durability = base Resolve, `technique_bonus = len(techniques)`, offense = attack+2), `facet.yaml` `combat.enemy_durability`/`combat.armor`, and `tools/combat_sim.py`'s enemy-attack order. Two of my own drafts were corrected against the engine mid-task: (a) I first wrote the 10+ Strike as an either/or "take 2 Resolve *or* impose a rider" — the engine applies **both** (deplete 2, and *additionally* an optional rider), fixed; (b) I first claimed the armor budget is *not* spent when a partial reaction already downgraded — the engine (`combat_sim.py:616-623` and `websocket.py:_apply_pc_armor_budget`) **does** spend the point regardless (it takes `min` of the two, but consumes budget), so I removed the claim.

**III.3 (body):** "Conditions replace hit points" qualified to **player characters**, with a new paragraph introducing enemy **Resolve** as the asymmetric durability model. Retired-F5 text deleted (the "0 Endurance → Absorbed conditions persist as Tier 2" paragraph; 0 Endurance now = Absorb only, Conditions land at normal tier). Strike section reframed: vs enemies, deplete Resolve (2/1/0) + optional 10+ rider (Tier 2 rider → **Easy to Strike** until cleared, never escalates to Broken); vs another character, apply Conditions as before. Conditions section qualified to PCs with an enemy-rider note. **Armor section rewritten** to the per-scene downgrade budget (light = first 2/scene, heavy = first 4/scene, one tier each, resets at scene end, shared across fights). Mooks: any success (7+) removes; armored Mook needs 10+. Named NPCs: Resolve (3–4) not Endurance pool, armor = flat +Resolve. Bosses: larger Resolve + phase change keyed to a Resolve threshold, plus the "a lone Boss is not solo-viable; difficulty comes from the encounter layer" ethos (Brain §5-bis, blessed at prose time). Enemy-Attacks armor line fixed (heavy no longer "downgrades two tiers").

**III.3 (Archive Guardian vignette) fully reworked** to the Resolve model. The old version ended on "second Staggered → Broken" (the Condition-stacking kill that D1 abolishes for enemies) and ran 2 exchanges — mechanically impossible against effective Resolve 10. Rewrote to **3 exchanges** (matching G1's median 3.0), tracking effective Resolve 10 → 8 → 6→4 → 2 (**phase change to Reduced Mode at threshold 2, matching `archive_guardian.fof`**) → 0 (defeated, the kneeling — established ending preserved). Demonstrates: the 10+ deplete-2-plus-rider choice, rider→Easy (Mordai's Staggered opens the guardian for the party — EF1's key teaching), Support granting +1d6 (distinct from the rider's Easy), the K1 Aggressive first-reaction surcharge, and the cost signal (Mordai empties his Endurance and Presses on fumes; Zulnut carries the finish). All established fiction kept (joints, glyph + its broad patrol-boundary complication, light-eyes, banter); no new canon invented.

**III.3 quick-ref card:** Strike Outcomes split into enemy-Resolve and character-Condition tables; Armor rewritten to the per-scene budget; exchange-flow step 5 now names Resolve depletion. Added the **"Your Five Numbers On Screen"** table mandated by the Brain ethos requirement — Endurance (Endurance bar), Posture (badge/selector), Conditions (conditions row), Sparks (spark pips), Armor budget (applied automatically; the action log shows "(downgraded by armor)"). The armor budget has **no standing UI readout** today, so I mapped it to its real surface — the log annotation at `play.js:837` — rather than invent a display; a dedicated readout is a candidate for A12.

**MM1:** stat-block template + all three examples re-keyed Endurance→Resolve (Sergeant 3, Guardian 8/effective 10, **TR 16→17**); enemy Condition-track line replaced with the Resolve/rider/Mook summary. TR section reconciled to the **engine's actual formula**: durability = base Resolve (was a banded Endurance table), technique bonus = **count of Techniques** (was a qualitative 1/2/3 table that would have scored the Guardian at TR 20, contradicting its published 17). TR reference examples fixed (Veteran = Offense 5 / Durability 4 / Armor 1; Guardian = 17). Building-Named/Bosses sections and the asymmetric-encounter TR (16→17) updated. `.fof` format doc: `endurance`→`resolve`, deprecation note for legacy `endurance`, and a `phases`/`resolve_threshold` example.

**MM5:** Strike Outcomes, Offensive-Actions + Magic effect columns, Armor (PC budget), Endurance (retired-F5 line removed), exchange-flow step 5, and the Mooks common ruling all brought to the Resolve model. The TR block reconciled to the engine (durability = base Resolve; technique = count). **Also reconciled MM5's stale Encounter Budget/Recipe section to MM1's A10 state** (it still carried the void-derived "~95/75/50/25%" win rates and the pre-A10 rosters — "1 Boss = Hard, 2 Named = Deadly" — which directly contradicted A10's "3 Named = Standard, actor-count-driven" findings; a C1 quick-ref-must-match violation). Now shows the Series 9 Part C validated recipes and actor-count-primacy.

**Quick_Start.md:** the one combat paraphrase that was stale — "Two Tier 2 = Broken" — corrected to "Second Tier 2 **of the same type** = Broken" (D5/F6).

**Presentation requirement (Brain Q4) satisfied:** armor is presented as two separate tools with **no cross-reference** — PC side is a downgrade budget (III.3 §Armor, MM5 Armor block), enemy side is flat +Resolve (III.3 Named NPCs, MM1 stat block/TR, MM5 TR block). No "armor works differently for enemies" anywhere. Two draft cross-references (a III.3 quick-ref parenthetical and an MM5 Armor parenthetical) were caught and removed.

**Verification:**
- Cross-document fact check (continuity-check intent, applied to the four markdown files since the skill's campaign-DB tooling doesn't apply to rules docs): Strike depletion 2/1/0, rider→Easy, enemy armor +Resolve, PC budget 2/4 per scene, Mook 7+/armored 10+, and all Guardian numbers (Resolve 8 / effective 10 / TR 17 / phase at 2) read identically across III.3, MM1, MM5. No stray "TR 16", no retired-F5 text, no un-qualified "two Tier 2", no enemy-Broken remnants, no armor cross-references.
- Full test suite (prose-only change, so a regression guard): **865 passed, 1 failed** — the failure is the same pre-existing unrelated `test_config.py::test_default_port_is_8000` (env `PORT=8010`) logged at A8/A9/A10.

**Accept criteria — all met:** continuity clean across III.3/MM1/MM5/Quick_Start; no quick ref introduces a rule the body doesn't state; armor sections carry no cross-reference to each other; the quick-ref card locates all five PC numbers on screen.

**Follow-ups noted (not in A11's declared file set):**
- `software/app/static/js/tools.js:165` renders a stale in-app armor rules card ("Light (Tier 2→1), Heavy (Tier 3→2)") — the old permanent-downgrade model. This is app UI; fold into **A12** (enemy-tracker/UI pass) along with a possible standing armor-budget readout so the quick-ref's fifth number gets a real home.

**A11 CLOSED.** Per C1, body text + all quick refs + `facet.yaml` + engine belong in one commit; `facet.yaml`/engine already landed in A1–A9 on this branch, so committing now bundles them with this prose. Per Worker protocol, stopping here without committing to report first. A12 (web app: enemy tracker shows Resolve) and A13 (PT03 boss stress test) are the remaining WS-A tasks.

---

### A12 — Web app: enemy tracker shows Resolve — CLOSED 2026-07-11

**Problem fixed:** the client still spoke the retired `endurance` vocabulary for enemies after the backend renamed the field to `resolve`/`resolve_current` (A1–A9). The live enemy tracker sent `endurance_current` in `enemy_update` (backend now reads `resolve_current`, so the −1 button was a no-op) and read `enemy.endurance` (undefined → blank Resolve readout). The enemy builder POSTed `endurance` to `/api/enemies/`, which Pydantic silently dropped, defaulting every built enemy's `resolve` to 0. All three are now corrected.

**Changes:**
- `components.js` — new shared `renderEnemyCard(key, enemy, opts)` + `enemyResolveDisplay(enemy)`. Renders a Resolve bar (mirrors the character Endurance bar), the `Resolve current/max` readout, conditions, and — when `opts.showPhases` — phase markers positioned on the bar at each `resolve_threshold` plus a "Phases at Resolve: …" note. Mooks render "falls to one Strike" (no pool). `opts.mmControls` gates the −1 Resolve / +Cond / Remove buttons. `resolve_current` falls back to `resolve` before combat starts.
- `play.js` — `renderEnemyTracker()` is now role-aware: MM → `#play-enemy-tracker` with `{mmControls:true, showPhases:true}`; player → `#play-player-enemy-tracker` with both false (read-only Resolve, no phases). `enemyTakeDamage` reads `resolve_current`/`resolve` and sends `resolve_current`. `onEnemyUpdated` writes `resolve_current`. New `onEnemyPhaseChange` posts a system-chat phase announcement and re-renders. Player branch of `renderPlayField` now un-hides `#play-player-enemies` and renders the tracker.
- `app.js` — routes the `enemy_phase_change` broadcast to `onEnemyPhaseChange`.
- `builder.js` — `previewEnemyTR` reads `#builder-enemy-resolve`; the durability-value ladder is keyed on `resolve`; `saveEnemy` POSTs `resolve`.
- `index.html` — builder field label/id Endurance → Resolve (`#builder-enemy-resolve`); new read-only `#play-player-enemies` card holding `#play-player-enemy-tracker`.
- `css/style.css` — `.enemy-resolve` accent (replaces `.enemy-endurance`); new `.resolve-bar` / `.resolve-fill` (+ `.low`/`.critical`) / `.resolve-phase-marker`.
- `tests/test_api_enemy.py` — new `test_created_enemy_echoes_resolve`: asserts the created enemy serializes `resolve` and carries no `endurance` alias.

**Verification:**
- Enemy CRUD tests: `test_api_enemy.py` **23 passed**.
- Full suite: **866 passed, 1 failed** — the failure is the same pre-existing unrelated `test_config.py::test_default_port_is_8000` (env `PORT=8010`) logged at A8–A11. My new test accounts for the +1 vs A11's 865.
- `node --check` clean on all four changed JS files.
- Node render harness exercised `renderEnemyCard`: mook → "falls to one Strike"; named (4/6) → 67% bar + "4/6" + "−1 Resolve" button; player boss view → no phase markers, no controls, Resolve falls back to 8/8; MM boss view → phase marker at left:25% (threshold 2 / max 8).
- `grep` confirms zero enemy-facing `endurance` references remain in `js/` or `index.html`.

**Accept criteria — met:** enemy CRUD tests pass with `resolve`; no `endurance` references remain in enemy-facing UI; Resolve bar + phase markers render; player view shows Resolve, MM view shows Resolve + phases.

**Follow-up carried forward (NOT done here — out of A12's file set and a C1 concern):** `tools.js:165` still renders the stale permanent-downgrade armor card ("Light (Tier 2→1), Heavy (Tier 3→2)"). That is a *rules-summary* card, not enemy-tracker UI, and rewriting it to the A11 per-scene-budget model touches the C1 "all quick refs must match body text" contract — it belongs in a dedicated quick-ref pass, not this enemy-vocabulary task. Still open.

**A12 CLOSED.** Per Worker protocol, stopping here to report before committing. A13 (PT03 boss stress test) is the remaining WS-A task.

---

### A13 — PT03 Boss Stress Test — RUN COMPLETE, ACCEPT BLOCKED, escalated — 2026-07-11

**What was done.** Ran the Iron Crucible boss fight (`playtest/03_boss_stress_test/scenario.md`) by the book against the standard PS-3 party. New driver `playtest/03_boss_stress_test/run_pt03.py` routes every roll and rule through `app.game.combat` (C1-compliant — supplies only the Crucible's authored Forge Slam / Heat Surge / phase behaviour, no re-implemented rule). Modifiers reconciled against `characters/*.fof`. Full write-up: `playtest/03_boss_stress_test/results.md`.

**Data.** n=300, seed 1: win **99.7%**, exchanges mean 2.9 / median 3, PCs Broken/fight 0.20, Sparks 5.3/9. The scenario predates the D1 rewrite, so the Crucible was translated to Resolve (Endurance 10 → Resolve 10, eff. 12 heavy; TR 13 → 16; phase re-keyed to `resolve_threshold` 6). **The phase change — the flagship mechanic PT03 exists to validate — fired in almost none of the by-the-book fights.**

**Accept verdict (task line 247: ≥3 exchanges, ≈Hard win rate, no house rules):**
- *No house rules* — **PASS**. Ran entirely on current rules.
- *≥3 exchanges* — **borderline fail** (mean 2.9; many 2-exchange fights, min 1).
- *≈Hard win rate* — **fail at 99.7%**, but the criterion itself is void-derived (see escalation).

**D1/D2 held up.** Resolve depletion, rider→Easy (the fight's best beat), the per-scene armor budget, and the retired 0-Endurance rule all behaved correctly with zero house rules. The failure is one layer up, in the Boss phase-change subsystem and in the acceptance bar.

**Findings (full text in results.md):** F0 A13's "≈Hard rate" bar is the last live instance of the Q3-voided win-rate mapping, contradicting §5-bis / III.3:325; F1/F2 scenario.md durability, TR, and phase-trigger are pre-D1; **F3 the phase's "armor cracks, easier to hurt" effect is a no-op under D1 (enemy armor is a flat one-time Resolve bonus — nothing to "trade for danger"); this hits every Boss built on the MM1 "trade defense for offense" phase pattern; F4 `combat.phase_crossed` can be silently stepped over by a reaction-cost deduction landing Resolve exactly on the threshold (observed live); F5 III.3 never states an enemy's reaction cost — the sim invents a Resolve cost, and that single ambiguity swings phase-fire rate from ~0% to 100%; F8 as modelled enemy Parry is strictly self-defeating (costs more Resolve than the Strike it prevents).** F6 stock `zulnut_def()` undercounts Zulnut's Strike (+0 vs sheet Finesse +2), corrected in-run; F7 combat magic unmodelled (Zahna runs as a weak striker).

## ESCALATION — Worker (A13) → Planner (2026-07-11)

**Status:** ✅ **RESOLVED by Planner, 2026-07-11.** All four engine claims (F3/F4/F5/F8) verified against source before ruling. Rulings in DESIGN §5-quater + DECISIONS P11; A13 Accept revised and new task A14 opened in TASKS. Summary: F0 — drop the void-derived win-rate bar, gate on exchanges + cost + phase-fire, keep it a lone-boss run; F5 — enemies do not spend a resource to react (Strike depletes Resolve by outcome only), which dissolves F8 (no self-own) and the common-path F4; F4 — encode the "every `resolve_current` change routes through `phase_crossed`" invariant + a test; F3 — retire the "armor cracks" phase pattern, define a D1-native phase vocabulary (raise offense / grant-revoke Special / second wind), rewrite MM1. No Brain round-trip required — everything extends ratified doctrine (§5-bis, Q4). **Return to Worker at A14, then re-run A13.**

---

**Two blockers, both above the Worker tier; neither fixable without a house rule the task forbids.**

1. **A13's Accept criteria contradict settled canon (F0).** "Won at approximately Hard rates" is the same void-derived win-rate→difficulty mapping that G1 (§5-bis) and G4 (§5-ter) already had struck. A lone Boss vs. a focus-firing party is, by ratified doctrine and by III.3:325's own prose, *not* an even fight — which is precisely the matchup PT03 forces (no lateral solution, by design). The criteria need the same revision G1's did: drop the win-rate bar; substitute a length-plus-cost-plus-*phase-fires* gate, or re-scope PT03 to a Boss-in-an-encounter (allies/terrain/Technique) rather than a lone Boss. **Question for Planner:** revise A13's Accept, or re-scope the scenario?

2. **The Boss phase-change subsystem has no coherent D1 story (F3–F5, F8).** This is the real discovery. Under D1: (a) the canonical "trade durability for danger" phase pattern is mechanically hollow because enemy armor is a flat init bonus, not per-hit mitigation (F3); (b) `phase_crossed` misses threshold crossings caused by reaction costs (F4 — a real engine bug); (c) whether an enemy pays anything to react is *unspecified in III.3* (F5), and the answer determines whether phases fire at all; (d) enemy Parry as modelled is a strict self-own (F8). These interact: the boss Parries (F5/F8), self-depletes past its own phase threshold (F4/F8), and dies Intact having never triggered the second act. **Questions for Planner/Brain:** Does an enemy reaction cost Resolve, cost nothing, or do enemies not react (F5)? Should `phase_crossed` also fire on reaction-cost deductions (F4)? And does the Boss phase-change design need a D1-native rewrite so "the fight changes" survives the move off the condition-track model (F3)?

**Recommend switching to Opus (Planner) to resolve both before A13 can be marked done or the WS-A workstream closed.** The run itself is complete and reproducible (`run_pt03.py`); no further Worker action is possible without a ruling.

---

### A14 — Boss phase-change subsystem: coherent D1 story — COMPLETE (with a downstream escalation) — 2026-07-11

Resolves the A13 escalation's engine/sim/content findings per DESIGN §5-quater items 2–5.

**F5/F8 — enemies do not react (done).** Removed `should_enemy_react` and both enemy-Parry blocks (`combat_sim.py` `_pc_strike` and `_g3_pc_strike`). A Strike against a Named/Boss now depletes Resolve by its effective outcome only — no enemy reaction, no Resolve spent on defense. Dead helper `_downgrade_outcome` (only the Parry blocks used it) removed. Deleted the four `should_enemy_react` unit tests; added `test_enemy_never_reacts_depletion_is_outcome_only` (reproduces `_pc_strike`'s exact dice via the same Spark/Press policy, asserts depletion == the canonical `strike_depletion` value for the rolled outcome — never a parry-cost off-by-one, never a full deflect).

**F4 — phase-crossing invariant (done).** Verified every `resolve_current` mutation already routes through `apply_resolve_damage`/`phase_crossed` (sim depletion paths at `combat_sim.py:465,1410`; the websocket MM-set path at `websocket.py:1138-1144` computes `phase_crossed` explicitly; the only other writes are init and Withdrawn *recovery*, an upward move `phase_crossed` correctly ignores). Added two hardening tests in `test_combat.py`: a depletion landing Resolve *exactly on* a threshold fires the phase (`before > threshold >= after`), and a further depletion below it does not re-fire.

**F3 — D1-native phase vocabulary in MM1 (done).** Rewrote MM1 §Bosses phase guidance. Retired the implicit "trade defense for offense" framing; the supported effect vocabulary is now explicit — **raise danger / grant-revoke a Special / second wind (add Resolve) / change the space or target (MM-narrated)** — matched to what the engine actually honours (`special_attack_mod`, `special_ignores_tier1`, Resolve add, narration). Added an explicit prohibition on "crack its own armor / trade durability for danger via armor," with the D1 reason (armor is a flat one-time bonus baked into starting Resolve — nothing to reduce mid-fight). Archive Guardian's Reduced Mode kept as the worked example. No new `phases[].effect` schema field added (§5-quater made it a candidate, not a requirement; phases stay MM-narrated with the engine honouring the small supported set). C1: no rule changed — the prose was brought into line with the engine; no quick-ref (MM5 has no phase text) or `facet.yaml` touch required.

**G0 characterization re-pin (in-scope, documented precedent).** The 4 fixed-seed `TestG0FixedSeedEndStates` boss/named snapshots shifted (enemies no longer bleed Resolve defending themselves). Re-captured exact end-states and re-pinned, per the file's own "re-pinning after an intentional rule change is expected" precedent (pre-D1 → Resolve 5 → Resolve 8 → now no-enemy-Parry). Notable: **the Guardian now crosses its phase threshold on BOTH boss seeds (2 and 3); seed 2 previously did not.** That the phase-fire fraction rose after removing the self-defeating Parry is direct evidence for A13's revised Accept (c).

**Suite:** `pytest -q` → **861 passed, 4 xfailed, 1 failed**. The lone failure is the known-unrelated `test_config` port default (env `PORT=8010`), which A14's Accept explicitly excludes. The 4 xfailed are the recipe-calibration corpus — see escalation below.

## ESCALATION — A14 (Worker) → Planner (2026-07-11): the F5 fix invalidates the Series-9 recipe corpus

**Not a blocker for landing A14 — a scope boundary the plan did not foresee.** Removing the enemy Parry (F5) does not just re-pin A13's boss numbers; it shifts the entire **MM1 Encounter Recipe Table** (Series 9 / task A10 / Gate G4) up by ~one difficulty band:

| Recipe | Band | Pre-A14 | Post-A14 |
|---|---|---|---|
| Standard — 3 Named TR8 | 65–85% | 81% | **94.5%** |
| Hard — 3 Named + 1 Mook | 40–60% | 48.5% | **76%** |
| Deadly — 4 Named | 15–35% | 19.5% | **58.5%** |
| Deadly — 3 Named + 2 Mooks | 15–35% | 19% | **47.5%** |

The four `TestRecipeCalibration` band assertions tripped — **exactly as their docstring promised** ("any rules/engine change that shifts a recipe out of its band trips a test instead of silently invalidating the MM1 table"). The guard did its job.

Re-deriving the rosters and/or bands under the corrected model is a **Series-9 recalibration with player-facing MM1 content** (the Recipe Table at `MM1_Encounters_and_Enemies.md:329-344`, `research/simulation_log.md` Series 9, and the calibration tests). That is Planner-tier calibration work of the same class as G4/A10 — **not** part of A14's stated scope (F5/F8/F4/F3), and it carries the §5-ter Brain ethos note (actor-count-gated difficulty). Doing it silently inside "execute A14" would be precisely the unblessed player-facing recalibration the workflow forbids.

**Planner ruling (recorded here, acting in-session):** open a follow-on task **A15 — Series-9 recipe recalibration** (re-run the ladder under the corrected model, re-derive rosters/bands so Standard/Hard/Deadly land in-band, update the MM1 Recipe Table + simulation_log + the calibration tests). Until A15, the 4 out-of-band recipes are marked `@pytest.mark.xfail(strict=True)` with the measured post-A14 numbers recorded in-place — so the suite is green *and* the invalidation is loud, and the strict marker will XPASS (forcing its own removal) the moment A15 re-pins each recipe. The `test_ladder_is_built_by_adding_actors_not_tr` ordering (94.5 > 76 > 58.5) and the Skirmish recipe are model-agnostic and stay live.

**A14 CLOSED.** Per Worker protocol, stopping to report before committing. Next: **A13 re-runs against the revised §5-quater Accept** (now unblocked — the buggy parry/phase model is gone), and **A15** recalibrates the recipe corpus.

---

## A15 — Series-9 recipe recalibration (DONE 2026-07-11)

Re-ran the PS-3 actor-count ladder under the corrected (no-enemy-Parry) model to re-derive rosters that land back in band. Full sweep recorded in `research/simulation_log.md` Series 9 **Part D** (Part C marked SUPERSEDED, retained as pre-A14 history).

**The recalibrated ladder is cleaner than the pre-A14 one: a fixed 3-Named core, +1 Mook per difficulty step.** Seed-1 pins (n=200; avg of seeds 1/2/3 in parens):

| Band | Roster | seed-1 | avg |
|---|---|---|---|
| Skirmish (85–100%) | 3–7 Mooks | 100% | 100% |
| Standard (65–85%) | 3 Named (TR 8) + 1 Mook | 76.0% | 76.8% |
| Hard (40–60%) | 3 Named (TR 8) + 2 Mooks | 47.5% | 47.5% |
| Deadly (15–35%) | 3 Named (TR 8) + 3 Mooks | 20.0% | 20.8% |
| Deadly (alt) | 4 Named (TR 8) + 1 Mook | 20.0% | 19.2% |

Notable second-order facts recorded for future reference: under the corrected model **3 Named alone is a near-clean win (~96%)** — no longer the Standard headline it was pre-A14 — and **4 Named alone lands in the Hard band (55%)**, not Deadly (it was the Part-C Deadly headline). Five Named overshoots into near-certain loss (9.8%). The Deadly "4 Named + 1 Mook" alternative is the "upgrade a throwaway to a real threat" reading and measures identically at seed 1 (20.0%).

**Files updated (all consistent):**
- `software/tests/test_combat_sim.py::TestRecipeCalibration` — all four `@pytest.mark.xfail(strict=True)` markers **removed**; tests renamed to their new rosters and re-pinned to seed-1 values with band assertions live again. `test_ladder_is_built_by_adding_actors_not_tr` re-pointed to the new ladder (3N+1M > 3N+2M > 3N+3M). Class docstring's A14-CASCADE note rewritten as A14-CASCADE/A15-RESOLUTION.
- `mm_manual/MM1_Encounters_and_Enemies.md` — Recipe Table (PS-3) re-pinned to Part D; the three surrounding actor-count prose spots that cited pre-A14 numbers corrected (the "actor count drives difficulty" paragraph, the 3-Sergeants budget-over-count example, and the ASCII rule-of-thumb ladder).
- `mm_manual/MM5_Quick_Reference.md` — Recipe Table card + actor-count dial line re-pinned (C1: quick ref updated in the same pass).
- `research/simulation_log.md` — Part C flagged SUPERSEDED; Part D added with the full ladder sweep and reproduction recipe.

**Acceptance:** all four recipes in-band under the corrected model; `xfail` markers gone (strict markers would XPASS otherwise); MM1 table + MM5 quick ref + simulation_log + tests mutually consistent; consistency sweep found no surviving live pre-A14 numbers outside the explicitly-labelled `docs/` escalation history and Part C. Suite: `pytest -q` → **865 passed, 1 failed** (the known-excluded `test_config` port default, env `PORT=8010`); the 4 former xfails are now live passes (861+4=865).

**A15 CLOSED.**

---

## A13 re-run — PT03 boss stress test, revised §5-quater Accept — CLOSED (2026-07-11)

The first A13 run escalated two blockers (F0 void-derived Accept; F3–F5/F8 phase subsystem). Both were resolved above the Worker tier: the Accept was revised (§5-quater item 1 — win rate *reported, not gated*; gate on exchanges + cost + phase-fire) and **A14** rebuilt the phase subsystem (F5/F8 enemies don't react; F4 phase-crossing invariant + tests; F3 D1-native MM1 phase vocabulary). This re-ran the by-the-book fight against that revised bar.

**Driver change (`run_pt03.py`, metrics only — no rule logic):** `run_rate` now also reports **phase-fire fraction** (inspects the mutated `crucible.phase_index` after each fight — set-once-never-unset, so it reports whether the Resolve threshold was crossed) and **mean PC Endurance remaining at fight end**. Both were required by the revised Accept (b)/(c) and the old `run_rate` didn't track them. All rules still route through `app.game.combat`; C1 intact.

**Result (n=300 × 7 seeds {1,2,3,7,13,42,99}):**

| Accept (§5-quater) | Result | Verdict |
|---|---|---|
| (a) median ≥ 3 exchanges | median **3** every seed; min **3** (pre-A14 min was 1) | PASS |
| (b) cost signal recorded | Sparks **6.6–6.7/9** (~2.2/player); Endurance remaining **~1.6–1.7**; PC-Broken **0.20–0.33/fight** | PASS |
| (c) phase fires meaningful fraction | **100%** (pre-A14: ~0%) | PASS |
| no house rules | ran entirely by the book | PASS |
| win rate | 99.3–100%, *reported not gated* (lone Boss vs full party ≠ even fight, §5-bis / III.3:325) | reported |

**No Boss Resolve retune needed** — median ≥ 3 held without invoking the sanctioned §5-bis `facet.yaml` scalar. The phase now fires structurally (defeat requires depleting past the mid-Resolve threshold), landing ~exchange 2 of a 3-exchange fight — the mid-fight pivot the scenario was authored to test, and the reason A13 exists. The near-drained Endurance (~1.7) and ~2.2 Sparks/player are the "survivable but expensive" cost signal. Seed-1 verbose run captured in `results.md` shows all three D1 beats live: the rider→Easy chain (ex1), the phase-change/Heat-Surge pivot (ex2), and the drained finish (ex3).

**Findings status:** F0/F3/F4/F5/F8 confirmed RESOLVED by A14 + §5-quater; F1/F2 are cosmetic scenario-prose doc-debt (the driver runs the correct D1 translation); F6 (stock `zulnut_def()` Strike undercount) and F7 (combat magic unmodelled) remain minor and out of A13's scope — both make the measured cost a conservative floor, not a ceiling.

**Files changed:** `playtest/03_boss_stress_test/run_pt03.py` (metrics), `playtest/03_boss_stress_test/results.md` (re-run verdict + aggregate + narrative + findings status), `docs/TASKS_v0.3_ruleset_revision.md` (A13 → `[x]`).

**A13 CLOSED. WS-A (durability & armor, D1+D2) is now fully complete** — A1–A15 all done. Per Worker protocol, stopping to report before committing. Next open workstream: **WS-B (advancement math, B1)**.

---

## WS-B — Advancement math (D3) — COMPLETE (2026-07-11)

Executed B1–B6 in one session. Full suite: **896 passed, 1 failed** — the single
failure is the pre-existing `test_config::test_default_port_is_8000` (env sets
`PORT=8010`; fails on clean HEAD, unrelated to WS-B).

**B1 — Pacing regression test.** New `software/tests/test_advancement_pacing.py`
(11 tests): Facet levels land at 5/10/15 advances (engine-driven), first Major at
level 3 (incl. 2-primary + 1-cross), and the DESIGN §6.3 projections s12/s15/s19 at
100/80/60% primary-SP efficiency. Written red against the old 6/4 constants.

**B2 — `facet.yaml` constants.** `facet_level_threshold 6→5`,
`major_advancement_threshold 4→3`; `session_skill_points` left at 4 (per P5).
v0.3 changelog note added. Synced the partial `.fof` mirror
(`spec/examples/base-ruleset.fof:530`) and the two loader tests that hardcoded the
old numbers (`test_facet_loading`, `test_fof_loader`).

**B3 — Per-Facet level tracking.** Replaced the flat `facet_level` /
`total_facet_levels` / `rank_advances_this_facet_level` fields with
`facet_levels: dict` + `rank_advances_by_facet: dict`; the three old names are now
read-only `@computed_field` properties (so `to_client_dict`/model_dump and the UI
keep working). `_check_facet_level_threshold` now credits **every** Facet's own
track — the fix for F3 (Major Advancement had never fired in code). `from_fof`
migrates legacy flat `.fof` files. ≥9 new tests in `test_character.py`.

**B4 — Technique pick budget.** New `Character.technique_picks_available`,
incremented per Facet level (any Facet), spent by `technique_select`, persisted in
`.fof`. The selection rule was factored into `Character.select_technique()` (single
source of truth); `_handle_technique_select` now delegates to it, and the PT05
harness calls the same method — no rule re-implementation. Tests in
`test_websocket.py` (5) + `test_character.py` (4 direct + budget/roundtrip).

**B5 — II.4 advancement text + propagation.** Rewrote the 6→5 threshold, the
Zulnut worked example (now counts to 5/10), the "any tree whose prerequisites you
meet" Technique rule, "Advancement at a Glance", the career-advance tier table, and
Major Advancement (3 levels; first Major now lands *with* level 3). **The philosophy
sidebar was falsified by the change (level 3 no longer requires breadth) and was
rewritten** (EF2). Propagated to `II.1` (character-sheet glossary), `MM3` (advancement
timeline table), and `MM5` (quick-ref advancement block). `/continuity-check`-style
sweep clean: no file still states 6-per-level, 4-for-Major, or "your Facet's tree".

**B6 — PT05 technique showcase.** New `run_pt05.py` drives the real engine; a Soul
Communion character reaches Facet level 3 and takes `spiritual_domain` (T1, standard
first domain) → `the_language_beneath_language` (T2) → `second_domain` (T3, choosing
the Prismatic domain **Fate**). All three B6 targets (Tier 3 Technique, Prismatic
domain, Second Domain) land at s12 (100%) / s15 (80%), **exactly** the DESIGN §6.3
projection. `results.md` records each unlock's session. One follow-up noted (not
blocking): `second_domain`'s choice is stored in `technique_choices` but not yet
mirrored into `Character.secondary_magic_domain`.

**WS-B COMPLETE.** Per Worker protocol, stopping to report before committing.
Remaining open workstreams: WS-A0/WS-A were done previously; **WS-D** and **WS-E**
are not started.

---

## WS-D — Death, hazards, Sparks (D4 + D6) — 2026-07-11

Executed WD1–WD8 in one session. Full suite: **931 passed, 1 failed** — the
single failure is the pre-existing `test_config::test_default_port_is_8000`
(env sets `PORT=8010`; fails on clean HEAD, unrelated to WS-D).

**WD1 — `facet.yaml` hazards/death schema.** New `ThreatClockDef`/`HazardsDef`/
`DeathDef` schema classes (`app/facets/schema.py`), `hazards.threat_clock` and
`death` sections in `facet.yaml` matching the BRIEF's exact shape. `SparkEarnMethod`
gained `structured`/`target_per_session` fields (previously silently dropped by
Pydantic's default `extra=ignore`) and `SparkDef` gained a `variants` sub-model
(used by WD7). Wired `hazards`/`death` through `MergedRuleset._merge()` and
`to_client_dict()` (registry.py) — the DESIGN pattern already used for
`combat`/`magic`. 20 new schema/loader tests.

**WD2 — Threat Clock engine + events.** New `ThreatClock` dataclass
(`app/game/session.py`): `.advance()` returns True only on the exchange that
fills it (never re-fires while already full); `.wind_back()` is unconditional,
no roll, floor 0 — matches the Brain ruling (BRIEF §EF4) exactly: winding back
never advances, and advancing checks `outcome_tier` against
`hazards.threat_clock.advances_on` (data-driven, not hardcoded) before
incrementing. New WS events `clock_create`/`clock_advance`/`clock_wind_back`
(all MM-only, mirroring `spawn_enemy`'s `is_mm` gate) broadcasting
`clock_created`/`clock_advanced`/`clock_wound_back`, plus `clock_fill` fired
only on the filling transition. `session.threat_clocks` included in both
`to_state_dict` and `to_player_state_dict`. 9 new tests (`TestThreatClockWS`):
advances on 7-9 and 6-, no advance on 10+, wind-back unconditional and
idempotent at 0, fill fires once and doesn't re-fire, state survives a
session round-trip, unknown-id errors, player cannot create a clock.

**WD3 — Threat Clock UI in the Play Field.** `renderThreatClockCard`
(components.js) — segment dots (filled/empty), MM gets Advance (7-9) / Advance
(6-) / Wind Back buttons; players get the read-only card only (no buttons
rendered client-side, and the server independently rejects non-MM clock
events — belt and suspenders). New `#play-clock-tracker` (MM) /
`#play-player-clock-tracker` (player) containers in `index.html`; `state.threatClocks`
wired through `onStateReceived` and the four new WS-message switch cases in
`app.js`. **Verified in a real browser via Playwright** (no JS test framework
in this repo, per prior sessions' precedent): full flow — setup → login →
create session → create clock → advance twice → screenshot shows 2/4 filled
red dots with MM controls; separately, a player-invited session shows the
same clock read-only in the "THREAT CLOCKS" panel with zero mutate controls.
Screenshots and driver scripts were scratch-only, not committed.

**WD4 — Graceful Fail, player-initiated.** `facet.yaml`:
`graceful_fail.structured: false → true`, description rewritten to
player-initiated framing. New WS events `claim_graceful_fail` (any player;
scans `session.roll_log` in reverse for the caller's last roll, rejects if it
wasn't `failure`, rejects a second claim on the same roll via a
`graceful_fail_claimed` flag written onto the roll-log entry, otherwise
broadcasts `graceful_fail_claimed` for the MM to confirm) and `act_break`
(MM-only, broadcasts `act_break_opened`) — mirrors the existing
`spark_earn_peer` nomination shape exactly as specified (claim broadcasts;
MM confirms via the existing `spark_earn` event, no new confirm event
needed). 6 new tests (`TestGracefulFailWS`).

**WD5 — III.1 Spark text + propagation.** Added Act Break Nomination and the
player-initiated Graceful Fail to III.1's Earning Sparks list; added an
explicit "no post-roll spending" sentence to Spending Sparks. **Propagation
sweep** (repo rule: a rules change updates every place that touches it, same
commit) found three other stale MM-awarded-Graceful-Fail spots and fixed all
three: `II.3_Magic.md`'s magical-6- sidebar, III.1's own Outcome Guidance
Failure section (contradicted its own earlier bullet in the same file), and
`MM5_Quick_Reference.md`'s Spark bullets/table (both the compressed bullet
list and the earning-methods table said "MM may award" — now "player claims,
MM confirms"). `MM2_Session_Design.md`'s canonical Spark Cadence section
(§2 "Graceful Failure (organic, MM-awarded)") was still describing the
pre-D6 model in full prose, including a stale "digital tool prompts... Award
Spark for graceful failure?" line describing a UI that no longer matches
WD4's actual `claim_graceful_fail` event — rewrote the subsection and its MM
Checklist bullet to the player-initiated/MM-confirms shape.

**WD6 — III.2 Adventuring (new chapter).** Three sections only, per DESIGN
§8.1 scope: Hazards and Threat Clocks, Getting Hurt and Getting Better,
When a Character Would Die. States the 72%-of-nearby-rolls pacing claim as a
deliberate design statement (per Brain, EF4) rather than leaving it implicit.
Defines "treated" for Tier 2 recovery concretely (a scene, a relevant skill
roll, or MM-ruled downtime) — III.3's quick-ref table has always said
"Treated" without defining it; III.2 is the first place that spells it out.
Death rule adapted (not copied) from
`playtest/06_expert_novice_campaign/fun_and_consequence_review.md` Revision 1,
with its "below 0 Endurance" framing stripped per DESIGN's explicit
instruction — this ruleset has no Endurance-0 death state, only Broken.
Table of Contents' "III.2 Adventuring *(Planned)*" placeholder replaced with
the real description. No other file referenced "Threat Clock" or "III.2" as
planned/todo, so no further propagation was needed.

**WD7 — Spark refund variant flag.** `spark.variants.refund_on_failed_pretechnique_cast: false`
added to `facet.yaml` under the new `SparkVariantsDef` (WD1). New
`spark_refund_variant_enabled()` accessor in `combat_sim.py` — documented as
a no-op against `run_combat` today, since combat magic/pretechnique casting
isn't modelled in the simulator (the same scope gap PT03 logged as F7); the
flag exists and is readable, per Accept, but has nothing to act on until a
magic-casting model exists. 4 new tests (loader + combat_sim).

**WD8 — PT04 resource tax — RUN, ACCEPT NOT MET.** New `run_pt04.py`
(the Ashwood Trail's three sequential encounters, driving `run_combat`
directly per C1; PC Endurance/Sparks/Conditions carried across encounters
per `scenario.md`'s Recovery rules; two Nomination Round Sparks injected as
this driver's scripted stand-in for the table-level Act Break Nomination
event). **Measured mean Sparks spent/player = 1.51 (n=1,400: 7 seeds × 200
iterations)** — below the ≥2 Accept bar. The refund variant (WD7) produces
no measurable difference, as expected (no magic-cast model to act on).
**Root cause, traced via a verbose `--table` run:** `should_spend_spark`
(combat_sim.py, pre-existing, not part of WS-D's file scope) only spends
Sparks unconditionally against a **Boss**-tier target, on desperation
(Endurance ≤ 2), or to finish a Tier-2-conditioned target — none of which
fire reliably in a 100%-win-rate session against Mooks and one **Named**
(not Boss) Captain. Mordai spent 0 Sparks across all three encounters in the
traced run. This reproduces, in the AI heuristic, the exact hoarding
behavior `MM2_Session_Design.md`'s own Spark Cadence section already
documents as a known real-table problem — the new earning cadence (WD4/WD5)
adds Sparks to the pool correctly, but nothing in WS-D's scope changes
*spending* behavior. Full findings, the encounter-by-encounter trace excerpt,
and the "what this does/doesn't tell us" caveats are in
`playtest/04_resource_tax/results.md`.

**Files changed:** `software/app/facets/schema.py`, `software/facets/base/facet.yaml`,
`software/app/facets/registry.py`, `software/app/game/session.py`,
`software/app/api/websocket.py`, `software/app/static/{index.html,css/style.css,js/{app,play,components}.js}`,
`software/tools/combat_sim.py`, `player_handbook/III.1_Core_Resolution.md` (new
Sparks text), `player_handbook/III.2_Adventuring.md` (new),
`player_handbook/Table_of_Contents.md`, `player_handbook/II.3_Magic.md`,
`mm_manual/MM2_Session_Design.md`, `mm_manual/MM5_Quick_Reference.md`,
`playtest/04_resource_tax/{run_pt04.py,results.md}` (new), plus new/updated
tests in `test_facets_schema.py`, `test_facet_loading.py`, `test_websocket.py`,
`test_combat_sim.py`. `docs/TASKS_v0.3_ruleset_revision.md` WD1–WD7 → `[x]`;
WD8 → `[x]` (run, with its result recorded — the task was executed to
completion; the *result* is a miss, not an incomplete task).

## ESCALATION — WD8 (Worker) → Planner (2026-07-11): Sparks spent/player misses the D6 bar; the spend-side AI is out of WS-D's scope

**Not a blocker for landing WD1–WD7** — the engine, schema, UI, and text
changes are all correct and independently tested. The blocker is specific to
WD8's Accept clause, which the task itself anticipates ("Below that, D6 is
revisited — escalate to Planner").

**What was attempted:** `run_pt04.py`, 1,400 simulated sessions (7 seeds ×
200) of the Ashwood Trail's 3-encounter template, Sparks/Endurance/Conditions
carried across encounters, two Nomination Round Sparks injected as this
driver's stand-in for the table-level event. Measured mean 1.51 Sparks
spent/player against a ≥2 bar.

**What is unclear — the specific question for Planner:** WD8's file scope is
`playtest/04_resource_tax/` only. The actual cause of the shortfall is
`should_spend_spark` in `tools/combat_sim.py` — a pre-existing AI heuristic
that only spends Sparks against a Boss-tier target, on desperation, or to
finish a Tier-2-conditioned enemy. It was never revised as part of D6/WS-D,
and revising it is outside WD8's assigned files. Two options, and BRIEF/DESIGN
don't decide between them:

1. **Revise `should_spend_spark`** to reflect a less hoarding-prone spend
   policy consistent with the new earning cadence, then re-run PT04. This
   touches shared simulator code exercised by every other Series/Gate
   (G0–G4, A-series), not just WS-D.
2. **Treat the automated 1,400-run proxy as the wrong instrument** for a
   cadence/behavioral acceptance test, and require a human-played PT04
   session log instead (as PT01/PT02 did) — the AI's conservative spend
   policy may simply not be a valid stand-in for a real player's
   spend-when-it-matters judgment, which is the entire premise BRIEF D6 is
   trying to fix.

Either path is a strategy call about what "the acceptance test for D6" is
allowed to mean, not an implementation detail a Worker should decide alone.

**Recommend switching to Opus (Planner) to resolve before WS-D is marked
fully complete** — WD1–WD7 can land now; WD8's verdict awaits this ruling.

### RESOLUTION — Planner → Worker (2026-07-11): instrument invalid, D6 untouched, reopen as WD8-R

**Ruled in `docs/DECISIONS.md` P12 and `docs/DESIGN_v0.3_ruleset_revision.md` §8-bis.**

**D6 is not revisited.** The 1.51 figure is **void as evidence** — it measures the harness, not the cadence. WD8's Accept is *unmeasured*, not *unmet*. Three independent defects, any one of which alone voids it:

1. **The PT04 roster is stale (pre-P10).** `scenario.md` builds all three encounters from the `TR × multiplier` arithmetic P10 demoted as non-predictive. Against the calibrated Recipe Table, its "Standard" is Mook-only (Series 9: mean PCs Broken 0.00 through **30** Mooks) and its "coin-flip Hard" climax is a **1-Named** roster (Series 9: 1–2 Named/Boss of *any* TR are trivial). **The 100% win rate is not an anomaly to explain — it is exactly what Series 9 predicts for this roster.** Mordai finishing at 5/5 Endurance is the roster's doing before it is the AI's. A resource-tax session that levies no tax cannot measure a resource tax.
2. **The spend policy is tautological as an instrument.** D6 is a *behavioural* hypothesis; a hardcoded heuristic with no model of hoarding or scarcity can only return its own rule. Retuning it and re-running (Option 1 as posed) would trade one tautology for a differently-tuned one.
3. **The harness measures the wrong domain.** `combat_sim` spends Sparks only inside `resolve_strike`; in play they are spendable on *any* roll. The metric is a strict subset of what D6's Accept names — a floor, never the number.

**On your two options — both partly right, neither as posed.** Option 2 is what **DESIGN §5 line 206 already required**: "PT04 is the acceptance test for D6. Playtest data hygiene applies: real server rolls, per-player dice." A 1,400-run Monte Carlo touches no server and has no players. **The task was specified as a playtest and performed as a simulation — that substitution, not the 1.51, is what this escalation actually surfaced.** No fault to you: the task line said only "Run with the new Spark cadence…", in a workstream where every neighbouring task is code. It was underspecified about *how* — **a Planner defect, corrected in WD8-R.** Option 1 is genuinely needed but **must not be done in place**: every canonical PC starts `sparks=3` and spent Sparks add dice to Strikes, so editing `should_spend_spark` directly would silently re-baseline every recorded G0–G4/A-series/Series-9 number — **the exact failure A14 already recorded once** (the F5 fix voiding the Series-9 corpus). Hence WD10's selectable, default-preserving policy with a bit-reproducibility test.

**Stopping at your file boundary was correct.** The escalation protocol worked here; the fault was in the task spec, not the execution.

**Consequence:** WD1–WD7 **land now** (engine, schema, UI and text are correct and independently tested). WD8 → **voided** (banner on `results.md`, run and driver kept per Series-9 precedent). Three new tasks: **WD9** (recalibrate PT04 rosters to the P10 Recipe Table), **WD10** (selectable Spark spend policy, default-preserving), **WD8-R** (re-run PT04 as the agentic server playtest DESIGN always specified). **D6's Accept is amended:** ≥ 2 Sparks/player, measured **over a session, across all rolls, from a real server roll log** — the Monte Carlo reports a combat-only floor alongside it and is never the deciding number.

**WS-D is not complete until WD8-R closes.** Resolved. **Return to Worker (Sonnet) at WD9.**

---

## WD9 — Recalibrate the PT04 rosters to the P10 Recipe Table (DONE 2026-07-11)

**Files:** `playtest/04_resource_tax/scenario.md`, `playtest/04_resource_tax/run_pt04.py`.

Rebuilt all three Ashwood Trail encounters from **MM1's actual calibrated Recipe Table** (`mm_manual/MM1_Encounters_and_Enemies.md` lines 342–345) rather than DESIGN §5-ter's earlier draft numbers — the two differ (MM1 folds a Mook into Standard and Hard; DESIGN's `3× Named` / `3× Named + 1 Mook` phrasing was superseded by MM1's own calibration pass). Cited MM1 as the source of truth per the task's "cite the Recipe Table instead" instruction.

- **Encounter 1 (Skirmish)** — unchanged: 3 Bandit Scouts (Mooks), fits the "3–7 Mooks" row. Deleted the `PS 3 × 1 = 3` budget line.
- **Encounter 2, "The Bridge Ambush" (Standard)** — was 4 Mook Warriors + 2 Mook Archers (a pure Mook-swarm Skirmish per Series 9, not a Standard fight). Rebuilt as **3 Named Bandit Lieutenants (TR 8) + 1 Mook Archer**, matching the Standard row exactly. Deleted the inline tier-weighted arithmetic and the "if too easy" variant block (no longer needed — the roster now lands on the calibrated row directly).
- **Encounter 3, "The Bandit Captain" (Hard)** — was 1 Named TR-9 (with a Rally Technique) + 3 Mooks (a 1-Named roster, trivial per Series 9). Rebuilt as **3 Named (Captain + 2 Lieutenants, all TR 8) + 2 Mook Elites**, matching the Hard row exactly. Dropped the Captain's Rally Technique and her extra TR point — keeping her mechanically identical to the Lieutenants keeps the roster on the calibrated TR-8 core; her distinction is narrative (commands, offers terms) rather than a hidden TR bonus that would pull the roster off the validated row.
- Fiction preserved throughout: same three-day caravan-escort pitch, same beats (ridge ambush → bridge choke point → camp confrontation), same lateral solutions (ward-stones, negotiation). Only the stat blocks changed.
- No `TR × multiplier` derivation remains anywhere in `scenario.md`; each encounter now states its Recipe Table row and citation instead.

**`run_pt04.py` was also updated**, even though the task's Files list named only `scenario.md` — the Accept criterion ("a smoke run of `run_pt04.py` shows the session is no longer a 100% clean sweep") can only be satisfied if the driver's hardcoded `ENCOUNTERS` roster (a separate Python mirror of the scenario, not derived from the Markdown) matches. Replaced `bandit_warrior_def`/old `bandit_captain_def` with a shared `bandit_lieutenant_def()` (TR 8: Resolve 3, atk +2, def +2, light armor) reused for both the lieutenants and the reflavored Captain; updated `ENCOUNTERS` to the new counts. Also added `mean_pcs_broken` to `run_rate`'s aggregate output (previously only session win rate and Sparks were reported) — needed to actually observe the Accept's "non-zero mean PCs Broken" claim, not just assert it.

**Smoke run result** (`python run_pt04.py --rate --iterations 200`, 1,400 total runs):
- Session win rate: **100% → 5.5%**
- Mean PCs Broken: **0.00 → 2.91**

Both confirm the roster is no longer a clean sweep and the Hard climax now actually threatens. (The very low 5.5% is the *sequential, no-full-recovery* three-encounter session compounding three individually-calibrated fights — each encounter alone sits on its Recipe Table band, but chaining Skirmish → Standard → Hard without full recovery is more punishing than any single row in isolation. Tuning that compounding effect, if it needs tuning, is WD8-R's job with real per-player data, not WD9's — WD9's Accept is roster-calibration-to-the-table, not session-win-rate-tuning.)

**Full suite: 931 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000` — local `.env` sets `PORT=8010`; same failure noted at WS-C, not touched by this task).

`docs/TASKS_v0.3_ruleset_revision.md` WD9 → `[x]`.

**Next:** WD10 (selectable Spark spend policy), then WD8-R (re-run PT04 on these rosters as a real server playtest).

---

## WD10 — Spark spend policy becomes selectable, default-preserving (DONE 2026-07-11)

**Files:** `software/tools/combat_sim.py`, `software/tests/test_combat_sim.py`.

Added a `policy` parameter to `should_spend_spark` (default `"conservative"`, unedited pre-WD10 logic verbatim) and a `"player_like"` branch modelling BRIEF D6's "less hoarding-prone spender": spends on any Named-or-Boss target (not just Boss), in the same desperation (Endurance ≤ 2) and finishing-blow (Tier 2 rider) cases, and additionally when holding 2+ Sparks (a floor of 1 kept in reserve rather than hoarding the full allotment). `player_like` is a strict superset of `conservative` — every case the default spends, `player_like` also spends.

Threaded `spark_policy` through `_pc_strike` → `run_combat` → `run_simulation`, all defaulting to `"conservative"`, so no existing call site's behaviour changes without explicitly opting in.

**Did not edit `should_spend_spark` in place** — per the task's iron requirement and the A14 precedent it cites (editing shared AI policy in place silently re-baselined the Series-9 corpus once already). Confirmed via full suite run: **940 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`, same as WS-C/WD9 — untouched by this task).

**Tests added (9, `TestSparkSpendPolicy`):** default matches explicit `"conservative"` across all three old branches; `"conservative"` still returns 0 for a Named target at full Endurance (pins the exact behaviour the policy must not disturb); `"player_like"` spends on Named; `"player_like"` spends at a 2+ Spark floor where `"conservative"` doesn't; `"player_like"` still respects 0 Sparks; `"player_like"` is a superset of `"conservative"` across Boss/Named/Mook targets; `run_combat`/`run_simulation`'s default equals an explicit `"conservative"` call (`AggregateResult` dataclass equality, n=50/seed=1); `player_like` spends more in aggregate over a real encounter (n=200/seed=1, `mean_sparks_spent` 4.1 → higher); and the **characterization test** — the Recipe Table's Standard roster (3× Named TR8 + 1 Mook, `standard_party()`, seed=1, n=200 — the same scenario `TestRecipeCalibration.test_standard_three_named_plus_mook` already pins) reproduces its recorded `win_rate` (0.760) exactly under the default, with `mean_sparks_spent` (4.1) newly pinned as this task's own regression anchor.

`docs/TASKS_v0.3_ruleset_revision.md` WD10 → `[x]`.

**Next:** WD8-R (re-run PT04 on the WD9 rosters, using the WD10 `player_like` policy where the sim is used, as the real server-playtest acceptance test for D6).

---

## WD8-R — PT04 re-run as the real server playtest, D6 acceptance test (DONE 2026-07-11)

**Files:** `playtest/04_resource_tax/run_pt04_live.py` (new), `playtest/04_resource_tax/results.md` (rewritten).

**What WD8 got wrong, per Planner ruling P12:** DESIGN §5 (line 206) always specified PT04 as a *playtest* — real server rolls, per-player dice, per BRIEF §Validation. WD8 substituted a 1,400-run `combat_sim` Monte Carlo, which touches no server and has no players. WD8-R is the actual playtest: a new driver, `run_pt04_live.py`, that starts the real FastAPI/WebSocket server (`uvicorn`, fresh port + data dir), uploads Mordai/Zahna/Zulnut's unmodified `characters/*.fof` sheets via the real character-upload API, spawns the WD9-recalibrated Ashwood Trail roster via the real Enemy API, and plays all three encounters to conclusion through the real combat WebSocket events — `declare_posture`, `strike`, `react`, `apply_condition`, `enemy_update`, `remove_enemy`, `end_exchange`, `spark_earn`, `act_break`. Every roll is `random.randint` inside the live server process (`app/game/engine.py`) — genuinely random, not a fixed seed.

**What is, and is not, re-implemented.** No dice, modifier, or outcome math is duplicated anywhere in the driver — every roll is resolved server-side and read back off the wire, and the driver asserts (`_sheet_mismatch` check) that every roll's server-returned `attribute_modifier`/`skill_modifier` matches what each PC's own sheet predicts. The digital tool has no automatic NPC-attack resolver by design (NPCs don't roll; PCs react, A14/§5-quater) — a human MM decides postures, targets, and Tier lookups every exchange by reading the PHB's own numbers off the rulebook (enemy Resolve depletion per outcome, Tier 1/2 condition ids, Mook removal thresholds). The driver reads these same values read-only from `facet.yaml` via `build_ruleset` — the same source the server itself reads — and does exactly what a human MM manually operating the enemy tracker would do. This is MM bookkeeping standing in for a human, not a second combat engine (C1, CLAUDE.md); the driver is fully decoupled from `tools.combat_sim.py` (no import, no shared AI) even though its target/posture/reaction tactics are deliberately similar reasonable-play choices.

**Sparks-spend policy applied live:** the WD10 `player_like` rationale (spend on a Named/Boss target, in desperation, or when holding 2+ Sparks) is applied as this driver's own real-time decision at each Strike — not a call into `combat_sim.should_spend_spark`, to keep the live driver decoupled from the simulator.

**Ran 5 independent live sessions** (fresh real server + fresh random dice each time, no seed — the same "robustness across independent runs" practice as A8/A15's multi-seed checks, applied here across sessions since a live playtest has no seed to fix):

| Session | Result | Sparks (M/Z/Zu) | Mean Sparks/player |
|---|---|---|---|
| 1 | LOSS/INCOMPLETE | 4/2/4 | 3.33 |
| 2 | LOSS/INCOMPLETE | 4/2/4 | 3.33 |
| 3 | LOSS/INCOMPLETE | 5/2/3 | 3.33 |
| 4 | LOSS/INCOMPLETE | 4/3/3 | 3.33 |
| 5 | LOSS/INCOMPLETE | 4/2/3 | 3.00 |

**D6 Accept (amended per P12): Sparks spent per player ≥ 2, measured over the session across ALL rolls, from the server roll log — PASS.** Aggregate mean 3.27, worst single session 3.00 — both comfortably clear the bar, a sharp reversal from WD8's void 1.51. The roll log is captured in full via WebSocket broadcast as each entry is recorded (not a re-fetch of the `roll_log[-50:]` truncated snapshot, which would have lost early-encounter rolls on a session this long). Modifier reconciliation: all 133 rolls across all 5 sessions matched their sheet's expected `attribute_modifier`/`skill_modifier` — no drift.

**Honest caveat, logged in `results.md` itself:** 0 of 5 sessions won outright — all ended with the party Broken in Encounter 3, the Hard climax. This is independent confirmation of WD9's own Monte Carlo smoke run (5.5% session win rate for this three-encounter, no-full-recovery structure), not a driver defect — and it does not affect the D6 Accept, which measures Sparks spent, not win/loss. Flagged explicitly that this driver's tactics are a mechanical proxy and never attempt the lateral solutions `scenario.md` offers (ward-stone activation, negotiating with the Captain) that a real table has available.

**Spark refund variant (WD7):** not exercised — no pretechnique magic casting occurs in this pure-combat scenario (same finding as WD8's original run). Flag remains at its committed default (`false`).

Full test suite unaffected by this task (no production code touched, only a new standalone script under `playtest/`): **940 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000`).

`docs/TASKS_v0.3_ruleset_revision.md` WD8-R → `[x]`. **WS-D is now complete** — every task WD1–WD10 plus WD8-R has landed or been superseded; the PT04 gate (`≥ 2 Sparks spent/player`) is met.

**Note on WD1–WD6 (RESOLVED 2026-07-11):** these showed `[ ]` unchecked in `docs/TASKS_v0.3_ruleset_revision.md` even though the WS-D log entry above states they were executed and marked `[x]` in the same session as WD7/WD8 — a checkbox never got flipped, not missing work. Verified against the actual codebase before touching anything: `ThreatClockDef`/`HazardsDef`/`DeathDef` + `hazards:`/`death:` in `facet.yaml` (WD1); `ThreatClock` class + `clock_create`/`clock_advance`/`clock_wind_back` events + `TestThreatClockWS` (WD2); `renderThreatClockCard` + `#play-clock-tracker`/`#play-player-clock-tracker` (WD3); `graceful_fail.structured: true` + `claim_graceful_fail`/`act_break` events + `TestGracefulFailWS` (WD4); Act Break Nomination/player-initiated Graceful Fail language in `III.1_Core_Resolution.md` (WD5); `III.2_Adventuring.md` exists (WD6). All six confirmed present and matching the log's description — flipped WD1–WD6 to `[x]` in `docs/TASKS_v0.3_ruleset_revision.md`.

---

## WS-E — Content (D7): E1, E2, E3 (DONE 2026-07-11)

**Pure writing workstream, no engine impact.** All three tasks executed in one session per user request ("execute WS-E").

**E1 — Domain example intents, with an escalation resolved before writing.** Before touching the appendix, recounted the domain list against the task's own accept criterion ("18 domains × 3 scopes × 3 examples = 162 entries") and found it wrong: `BRIEF_v0.3_ruleset_revision.md`, `DESIGN_v0.3_ruleset_revision.md`, and this TASKS file all say 18, but `II.3_Magic.md`'s own Domain Quick Reference table and `Appendix_Magic_Domains.md` list **21** domains (Soul: 9 standard + 3 prismatic = 12; Mind: 6 standard + 3 prismatic = 9) — and the PHB's own "All 18 domains at a glance" / "Full descriptions of all 18 domains" lines were stale, never updated when Soul's standard list grew past 6 sometime before this task was written. This is the same class of bug WS-C's consolidation ledger was built to catch, just not caught there because nobody recounted. Asked the user rather than silently picking a count or dropping 3 domains from coverage; user chose to write to the real 21 and fix the stale PHB text alongside it.

Wrote all 21 domains' example-intent blocks into `player_handbook/Appendix_Magic_Domains.md` — one `**Example intents**` block per domain, three lines (Minor/Significant/Major), three semicolon-separated example clauses per line. Verified programmatically (regex over the file): 21 domain headers, 63 scope-lines, 189 individual example clauses (21 × 3 × 3). Added an explicit framing note ("design patterns, not a menu... If an example ever gets treated at the table as the one correct way to use a domain... flag it") directly under the existing "Reading the domain descriptions" callout. Every example is a verb-phrase intent (e.g. "seal a door shut by fusing its hinges"), never a named/castable spell, and stays within each domain's own stated "Beyond this domain's focus" boundary. Fixed the two stale "18 domains" lines in `II.3_Magic.md` to 21. Original content throughout — no proprietary IP referenced.

**E2 — MM Trouble Table.** Added a d6 table to `mm_manual/MM5_Quick_Reference.md` (new section before "Common Rulings"): Cost / Position / Attention / Equipment / Condition / Revelation, one line each, usable without a lookup. The Condition row was written carefully to avoid inventing a rule: it explicitly says the entry is *narrated flavor, not a mechanical Condition, unless already in combat* — Conditions are a combat-specific mechanic (III.3) and applying them mechanically to a non-combat 6- would be new rules content the PHB doesn't state, which the accept criterion forbids.

**E3 — Magic 6- templates into MM5.** Added a "Magic 6- Templates" subsection under MM5's existing Magic section, citing II.3, compressing each of II.3's six named patterns (wrong target / keeps working / attracts attention / domain bleeds / cost arrives early / nothing happens) plus the player Graceful-Fail option to one line each. Self-checked against C1 ("compression, not paraphrase"): two lines (`cost arrives early`, `nothing happens`) drifted into paraphrase on the first pass and were rewritten to match II.3's exact clauses ("the magic succeeded — but the mage carries a consequence that should have been deferred"; "the domain reaches and finds nothing — the rarest and most useful failure").

**Verification:** `grep -rln "18 domain"` across the repo now only matches the three planning docs (BRIEF/DESIGN/TASKS), which are historical record, not canon — confirmed clean. No tests to run (pure prose, no engine/schema/code touched); WS-E was never gated on the test suite.

`docs/TASKS_v0.3_ruleset_revision.md` E1/E2/E3 → `[x]`. **WS-E is now complete — all 45 tasks across all six workstreams (WS-C, WS-A0, WS-A, WS-B, WS-D, WS-E) are done.**
