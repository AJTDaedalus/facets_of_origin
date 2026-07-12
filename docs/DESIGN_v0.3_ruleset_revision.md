# DESIGN — v0.3 Ruleset Revision

**Tier:** Planner (Opus) output — hand to Worker (Sonnet)
**Date:** 2026-07-10
**Input:** `docs/BRIEF_v0.3_ruleset_revision.md` (all decisions D1–D8 resolved)
**Branch context:** `feature/data-driven-dice` (721 tests green)
**Companion files:** `docs/TASKS_v0.3_ruleset_revision.md`, `docs/DECISIONS.md`, `docs/LOG_v0.3_ruleset_revision.md` (Worker creates)

---

## 1. Code Survey Findings

Six facts established by reading the code, not assumed. Three of them change the shape of the work the BRIEF describes.

**F1 — Combat resolution is implemented twice, and the two copies disagree.**
`software/app/api/websocket.py` (`_handle_strike`, `_handle_react`, `_downgrade_condition_for_armor`, `_handle_apply_condition`, `_handle_end_exchange`) is the live engine. `software/tools/combat_sim.py` (`resolve_pc_strike`, `resolve_enemy_attack`, `armor_downgrade`, `apply_condition`, `cleanup_end_of_exchange`) is a parallel re-implementation. They diverge today:

| Behaviour | Engine (`websocket.py:626`) | Simulator (`combat_sim.py:237`) |
|---|---|---|
| Light armor vs Tier 1 | Downgrades to tier 0 → **condition fully absorbed** | No effect — Tier 1 lands |
| Heavy armor vs Tier 2 | Downgrades 2 tiers → **absorbed** | No effect — Tier 2 lands |
| 0-Endurance Absorb | No special rule | Absorbed conditions become persistent Tier 2 (`is_zero_end_absorb`) |

The BRIEF's core validation strategy — *"simulation before prose; D1/D2 must be re-simulated before PHB text is rewritten"* — is unsound while these are separate. Every simulation to date has validated the simulator, not the game. **This is the first thing to fix, before any D1/D2 mechanics land.** See §3 (WS-A0).

**F2 — The armor infinite-loop bug is worse on the engine side than `research/armored_enemy_breaking_problem.md` describes.** That doc analyses the simulator's semantics. In the engine, a light-armored *character* is immune to Tier 1 conditions outright and a heavy-armored character is immune to Tier 2. D2 must fix the player-facing case too, not only enemies.

**F3 — Cross-Facet levels are never tracked, and II.4 contradicts itself about whether they should be.**
`Character._check_facet_level_threshold` (`character.py:210`) returns `0` immediately when the advanced skill is outside the primary Facet, so `total_facet_levels` can only ever reach 2 (the 15-advance primary cap ÷ threshold 6). `major_advancement_threshold: 4` is therefore unreachable in code — Major Advancement **never fires**, in any campaign, at any length.

The PHB disagrees with itself in the same file:
- `II.4:89` — *"Facet level advances outside your Primary Facet ... do not count toward your Major Advancement threshold."*
- `II.4:207–209` — *"Every 4 Facet levels total — accumulated across any Facet ... A character who has reached level 2 in their Primary Facet and level 2 in a secondary Facet has accumulated 4 Facet levels total and qualifies."*

This is **ledger row 9**, unlisted in the BRIEF. Canonical answer: cross-Facet levels *do* count (the Major Advancement section and its worked example are the intended rule; `II.4:89` is the stale sentence). D3 depends on this — "any Facet level, primary or cross-trained, grants a Technique pick" is incoherent unless cross-trained levels exist.

**F4 — `technique_select` is already permissive; the PHB is the restrictive one.**
`_handle_technique_select` (`websocket.py:1035`) looks techniques up through the global `ruleset.get_technique()` and validates only the `prerequisites` list. It never checks the technique's tree against the character's primary Facet, and it never checks whether the character has an unspent pick. D3's rule is therefore *already* the engine's behaviour. What is missing is a **pick budget** (`technique_picks_available`) — without it the MM can grant unlimited techniques, and with the D3 text change there is nothing left to gate them.

**F5 — The 0-Endurance rule exists only in the simulator.** Option A of `research/armored_enemy_breaking_problem.md` was adopted into `combat_sim.py` and never into `facet.yaml`, the engine, or the PHB. Every "house rule triggered: Y" flag in `research/simulation_log.md` is this rule. D1/D2 must decide its fate explicitly rather than let it survive by inertia (§4.3).

**F6 — Broken stacking is already wrong in code.** `websocket.py:681–684` escalates on *any* second Tier 2 condition (`staggered` + `cornered` → Broken). D5's canonical answer is second Tier 2 **of the same type**. This is a code fix, not only a text fix — and it makes PCs meaningfully more durable, which interacts with the D2 and G3 simulation gates.

---

## 2. Architecture

### 2.1 The one structural change: `app/game/combat.py`

Extract a single, pure, synchronous combat-resolution module. Both consumers import it; neither reimplements it.

```
app/game/combat.py          ← new: the only place combat rules live
  ├── resolve_strike(attacker, target, opts, ruleset) -> StrikeOutcome
  ├── resolve_reaction(defender, incoming, ruleset)   -> ReactionOutcome
  ├── apply_condition(target, condition, ruleset)     -> ConditionResult
  ├── apply_resolve_damage(enemy, tier, ruleset)      -> ResolveResult
  ├── armor_downgrade(target, tier, ruleset)          -> int   (mutates per-scene budget)
  └── end_exchange(combatants, ruleset)               -> list[ExchangeUpdate]

app/api/websocket.py        ← thin: auth, validation, broadcast, persistence
tools/combat_sim.py         ← thin: policy (posture/target/spark choice) + statistics
```

Constraints on the module:
- **No I/O, no async, no session objects.** Takes combatant state + `MergedRuleset`, returns result dataclasses. This is what makes it testable and what makes the simulator trustworthy.
- **Reads every number from `facet.yaml`.** No literal `{"dodge": 1, "parry": 1, ...}` cost tables (currently hardcoded at `websocket.py:559`), no literal `{"staggered", "cornered"}` (`websocket.py:681`), no literal `recovery_amount = 2` fallbacks.
- **Combatant protocol, not a class hierarchy.** `Character` and `Enemy` both satisfy a small structural protocol (`conditions`, `armor`, `posture`, and either `endurance_current` or `resolve_current`). Asymmetric durability (D1) is expressed by which field is present, not by an `isinstance` branch.

Why this is worth the cost, in a plan whose brief did not ask for it: D1 and D2 both require simulation sign-off before prose. The simulator is currently a second opinion, not a measurement. Fixing that costs three tasks (A0.1–A0.3) and repays them across every gate in §5.

### 2.2 What does not change

Per BRIEF non-goals: `resolve_roll` / `resolve_magic_roll` in `engine.py`, the 2d6 three-tier resolution, the posture set, the reaction set, PC-facing-rolls-only, character creation, the 18-point buy. `combat.py` *calls* `engine.resolve_roll`; it does not reimplement it.

---

## 3. Workstream WS-A0 — Combat extraction (new; blocks WS-A)

Not in the BRIEF's split. Inserted because WS-A cannot be validated without it.

**Approach:** characterization-first. Write tests that pin the *simulator's* current semantics (not the engine's), because every number in `research/simulation_log.md` was produced under simulator semantics and we need the refactor to be provably behaviour-preserving against the recorded data. The engine's divergent armor behaviour (F1, F2) is recorded in `DECISIONS.md` as a defect and is deliberately **not** preserved — D2 replaces it in the next task group anyway.

**Test strategy:** `software/tests/test_combat.py` (new). ≥3 tests per public function per CLAUDE.md. Plus one *parity* test class that runs an identical seeded scenario through `combat.py` directly and through the WebSocket handler, asserting identical condition/Endurance end-state. That parity test is the permanent guard against F1 recurring.

**Acceptance:** full suite green (721 → ~745); `combat_sim.py` loses its private rules functions; and **G0 as amended by EF5** — the post-refactor run reproduces the pre-refactor end-state *exactly* on the 5 fixed seeds. Aggregate win-rate comparison against `research/sim_result_V6.md` is a secondary check, valid only where RNG draw order legitimately changed.

---

## 4. Workstream WS-A — Enemy durability & armor (D1 + D2)

### 4.1 D1 — Resolve pool

**Data model.** `Enemy.endurance` → `Enemy.resolve` (`int`, `ge=0`). Ephemeral tracker field `endurance_current` → `resolve_current`.

**Depletion.** PC Strike outcome depletes the target's Resolve: full success (10+) = 2, partial (7–9) = 1, failure = 0 (and a consequence for the attacker, unchanged). Resolve 0 = defeated. Values live in `facet.yaml` under `combat.enemy_durability.strike_depletion`, keyed by outcome tier id — not hardcoded.

**Conditions become riders.** On a full success only, the attacker may additionally impose one Tier 1 or Tier 2 Condition on the enemy as a narrative rider. Riders never kill; Resolve does. Enemy Conditions no longer stack toward Broken. `_apply_broken` for enemies is deleted.

**What a rider does** *(Brain ruling, BRIEF §EF1 — riders must not be dead text).* A rider keeps the Condition's existing table effect. A Tier 2 rider (Staggered or Cornered) makes subsequent Strikes against that enemy **Easy**; a Tier 1 rider likewise applies its normal effect and clears at end of exchange as usual. This is what makes the 10+ choice real: deplete 2 Resolve now, or spend the rider on setting up the rest of the party. **G1 must simulate rider→Easy** — a simulation that models riders as inert validates a game nobody will play, which is the same class of error that cost us the evidence corpus (Q3).

**Mooks.** Unchanged in spirit, formalised: a Mook is removed by any success (7+). An **armored Mook** requires a full success (10+). Mooks have no Resolve pool and no Conditions.

**Armor on enemies = flat bonus Resolve.** Light +1, heavy +2. This is the BRIEF's own suggestion and it produces a property worth naming:

> **The TR identity.** `armor_bonus` in the Threat Rating formula is numerically equal to the Resolve armor grants. So `TR = offense_value + resolve_base + armor_bonus + technique_bonus` remains structurally correct with `durability_value := resolve_base`.

**TR re-key (the durability table dies).** `Enemy.calculate_tr()` currently maps Endurance → durability_value through a 7-branch ladder. Replace with `durability_value = resolve` for non-Mooks, `0` for Mooks. This is not a coincidence — set the migration map so that **`resolve = the old durability_value`**:

| Legacy Endurance | Old durability_value | New Resolve |
|---|---|---|
| ≤2 | 1 | 1 |
| 3–4 | 2 | 2 |
| 5–6 | 3 | 3 |
| 7–8 | 4 | 4 |
| 9–10 | 5 | 5 |
| 11–12 | 6 | 6 |
| 13+ | 7 | 7 |

Consequence: **every existing TR is preserved exactly.** City Watch Sergeant (End 6 → Resolve 3): `4 + 3 + 1 = 8` ✓ matches its published TR 8. Veteran Soldier (End 7 → Resolve 4): `5 + 4 + 1 = 10` ✓ matches TR 10. Archive Guardian (End 10 → Resolve 5): `5 + 5 + 2 + special 2 = 14` vs published 16 — the Guardian's `special` bonus was double-counted at authoring time; correct it to 14 and note the change in `MM1`. Encounter Budget arithmetic is therefore stable across the migration and only needs recalibrating for the *play* effect of Resolve, not for a TR discontinuity.

**Starting values (to be confirmed by G1, not asserted):** Named Resolve 3, Boss Resolve 5, +1/+2 armor. Effective Boss durability = 7 for a heavy-armored Boss.

*Napkin check the simulation must confirm.* A starting Strike PC (Strength 3 → +1, Combat Practiced → +1) rolls 2d6+2. Against a Boss imposing Hard (−1): P(10+) = 10/36 = 27.8%, P(7–9) = 16/36 = 44.4%. Expected depletion = `0.278×2 + 0.444×1 = 1.00` per unopposed Strike. Three PCs, with the Boss's reactions negating roughly one Strike per exchange, gives ~2.0 Resolve/exchange against an effective pool of 7 → **~3.5 exchanges**. That clears the PT03 gate with margin, which is why 5/+2 is the starting point rather than the top of the BRIEF's 2–6 band.

**Confirmed by G1 (task A8, 2026-07-10):** the napkin check's ~3.5-exchange estimate assumed Hard-difficulty Strikes throughout — it did not anticipate the rider→Easy snowball (EF1's mandated worst-case rider policy), which collapses the real simulated fight to a median of 2 exchanges at Resolve 5. The simulation raised the Boss starting value to **Resolve 8** (effective 10 with heavy armor) to clear the median-3 floor under that snowball; Named Resolve 3–4 is unaffected and confirmed stable. See §5-bis and `research/simulation_log.md` Series 7 for the full result. `enemies/archive_guardian.fof` and `archive_guardian_def()` are updated; its published TR moves 14 → 17.

**Back-compat.** `Enemy.from_fof` accepts a legacy `endurance` key when `resolve` is absent, maps it through the table above, and emits a `DeprecationWarning`. Keep for one cycle; remove in v0.4. Rationale: user-authored `.fof` files exist outside the repo. `to_fof` only ever writes `resolve`.

**Phase changes.** `MM1`'s phase-change language finally gets a mechanism: `Enemy.phases: list[PhaseDef]`, each with a `resolve_threshold` and a `description`. Crossing a threshold on depletion emits an `enemy_phase_change` WebSocket event. Archive Guardian's existing phase text is re-keyed to `resolve_threshold: 2`.

### 4.2 D2 — Armor for player characters

Constraints from the BRIEF: armored entities must be breakable; heavy must beat light; heavy must do something against Tier 2; both keep IV.1's fictional weight.

**Why the BRIEF's candidate shape fails.** D2 suggests *"downgrade the first incoming Condition per exchange (light) / per exchange plus one more per scene (heavy)."* Broken is reachable only by taking a second Tier 2 while already holding one, and Tier 1 clears at end of exchange. So any rule that downgrades every incoming Tier 2 *within* an exchange prevents accumulation permanently. The binding question is how many Conditions a target receives per exchange — and `combat_sim.py:698-706` gives each enemy exactly one attack per exchange, at one PC, with incoming tier set by enemy tier (Mook 1, Named/Boss 2).

**In a boss fight — one enemy — a PC receives at most one Condition per exchange.** A one-per-exchange downgrade absorbs it every time. The light-armored PC cannot be Broken by a boss: the same infinite loop from `research/armored_enemy_breaking_problem.md`, relocated to the player side. It is masked today only by the 0-Endurance override at `combat_sim.py:548-551`, which §4.3 retires. PT03 — the acceptance test for D1/D2 — is a single-enemy boss fight, i.e. precisely the scenario that surfaces it.

**Selected shape — the per-scene downgrade budget** *(approved by Brain, Q2; the word is **scene**, never "fight")*:

- **Light armor:** the first **2** Conditions you receive per scene are each downgraded one tier (Tier 2 → Tier 1; Tier 1 → none).
- **Heavy armor:** the first **4**.
- The budget does not reset between exchanges. It resets when the **scene** ends. Two fights inside one scene share the budget.

**Terminology is load-bearing.** Player text and `facet.yaml` both say *scene* (`downgrades_per_scene`). A combat is a scene; "per fight" and "resets at end of scene" cannot both be written, because they differ whenever a scene contains two fights.

One integer per combatant (`armor_downgrades_remaining`), one clock, no mid-fight reset. Capacity is genuinely finite over the scene, so armored entities are breakable: against a boss landing Tier 2 each exchange, an unarmored PC is Broken around exchange 2, light around exchange 4, heavy around exchange 6. Heavy strictly beats light. Heavy mitigates Tier 2 — it is the same downgrade, twice as often. IV.1's fictional weight is untouched. The 2 and 4 are starting values for gate G2, not assertions.

**Rejected — residue instead of depletion:** armor downgrades every Tier 2 to Tier 1, but a Tier 1 taken *through* armor persists past end of exchange and a second escalates back to Tier 2. Armor never "runs out," which is conceptually cleaner, but it requires tracking two distinct kinds of Tier 1 Condition at the table.

Recorded in `DECISIONS.md` as **P4**; escalated to Brain as **Q2** and **approved** (BRIEF §Q2). A Worker should not silently revert to the per-exchange shape.

**Interaction with F6.** Fixing Broken stacking to *same-type* Tier 2 already makes PCs harder to drop (Staggered + Cornered no longer combine). Landing F6 and D2 together without measurement risks over-correcting into unkillable PCs. Gate G2 measures the combined effect and the sim matrix in §5 varies them independently.

### 4.3 The 0-Endurance rule (F5) — retire it

`combat_sim.py`'s `is_zero_end_absorb` escalation was Option A of `research/armored_enemy_breaking_problem.md`, adopted to give *armored enemies* a breaking condition. Under D1, enemies have no condition track and no breaking condition — the rule's entire reason for existing is gone. Under D2, armored PCs are breakable without it.

**Decision:** delete it. Do not port it into `combat.py`. The existing PHB rule (0 Endurance = Absorb only) stands alone.

Consequence: PC lethality drops relative to every recorded simulation. All PC-side win rates in `research/simulation_log.md` were measured with this rule active and are **invalidated by this change**, independent of D1. Gate G2 must re-baseline them. This interacts directly with D4's death policy — softer combat plus an explicit death rule is the intended combination, not an accident.

---

## 5. Simulation matrix & acceptance gates

All runs via `software/tools/combat_sim.py` against `combat.py`, seeded, n ≥ 200, logged to `research/simulation_log.md` under its existing Series conventions.

| Gate | Question | Configuration | Pass condition |
|---|---|---|---|
| **G0** | Did the extraction preserve behaviour? | Pre-refactor sim vs post-refactor sim, identical seeds, old rules | **Exact end-state match on the 5 fixed seeds** (conditions, Endurance, out/alive). The ±3pp aggregate band is *not* the criterion — see below. |
| **G1** | Is a by-the-book Boss fight runnable *and expensive*? *(D1 acceptance — pass condition revised, Planner 2026-07-10, see §5-bis)* | Archive Guardian (Resolve retuned to clear the floor — see §5-bis; heavy) vs 3 starting PCs, **riders modelled: Tier 2 rider → subsequent Strikes vs that enemy are Easy** | Median ≥ 3 exchanges; **every enemy defeatable**; **zero house rules invoked**; the rider→Easy snowball does not drive median exchanges below 3; **cost signal recorded** (mean Sparks spent, mean PC Endurance remaining at fight end, PC-Broken incidence) as evidence the fight is *survivable but expensive*. ~~PC win rate 45–55%~~ **dropped — void-derived, see §5-bis.** |
| **G2** | Is an armored PC breakable, and is heavy > light? *(D2 acceptance)* | 1 PC × {none, light, heavy} vs Veteran Soldier; F6 fix on/off as a factor | Broken reachable in all three; `T_broken(heavy) > T_broken(light) > T_broken(none)`; `T_broken(light) ≤ 2 × T_broken(none)` |
| **G3** | Does K1 soften the Aggressive death-spiral without erasing the tradeoff? *(D8)* | Unarmored Endurance-3 PC, Aggressive vs Measured, baseline vs K1 | K1 cuts PC Broken rate ≥ 15% relative **and** Aggressive retains a net offense edge over Measured (win-rate delta preserved within ±5pp). Adopt only if both hold. |
| **G4** | Do the Encounter Budget multipliers still mean what they say? | Chicken baselines (3/5/7) + Sergeant + Guardian, at each difficulty | Skirmish ~95%, Standard ~75%, Hard ~50%, Deadly ~25% (±10pp). Retune multipliers if not. |

**G0 is not a statistical gate** *(Brain ruling, BRIEF §EF5).* A behaviour-preserving refactor run on identical seeds must produce **identical** outcomes; that is the whole test. At n=200 and p≈0.5, ±3pp is roughly one standard error — a band that would pass real regressions and fail clean refactors by chance. Exact seeded end-state match is therefore primary. The ±3pp aggregate band applies **only** if the refactor legitimately changes RNG draw order, and the Worker must document *why* it did before invoking it.

**G1 must model riders as live** *(BRIEF §EF1).* A Tier 2 rider makes subsequent Strikes against that enemy Easy. Simulating riders as inert would validate a game nobody will play. G1 additionally measures whether 2-Resolve depletion *plus* an Easy rider snowballs boss fights below the 3-exchange floor — if it does, the lever is Boss Resolve (a `facet.yaml` scalar), not the rider rule.

### 5-bis. G1 pass-condition revision (Planner resolution of the A8 escalation, 2026-07-10)

Worker A8 ran G1 and hit a wall that is **not a tuning failure but a structural finding**: a solo, single-target, by-the-book Boss cannot produce a 45–55% *party-loss* rate at any Resolve value. Full evidence in `research/simulation_log.md` Series 7 and `docs/LOG_v0.3_ruleset_revision.md`'s A8 escalation block. Planner triage:

1. **The 45–55% win-rate band was void-derived and is dropped.** It traces to BRIEF §"winnable at ~Hard rates" → the Encounter Budget's "Hard ≈ 50% win" multiplier — and Brain's Q3 ruling **voided every Encounter Budget difficulty multiplier** (BRIEF §Void). The win-rate band could not survive on a foundation Brain already declared void. Independently, the §4.1 napkin check only ever engineered the *exchange-length* half of G1; it never derived a win-rate prediction. So the band was carried in as a descriptor, not designed.

2. **A win-rate band is the wrong shape for a solo Boss.** Resolve is a *durability* knob (how long the Boss survives), not an *offense* knob (how much threat it poses). Against three independent PCs delivering three Strikes every exchange, the party's aggregate offense grinds through any Resolve pool; a lone single-target attacker never sustains the two-same-type-Tier-2-hits cadence Broken requires (D5 ledger row 2 / F6). No durability value moves party-loss toward 50%. This is action economy, not a bug in the D1 migration.

3. **This matches existing canon, not a new stance.** The Archive Guardian's own stat block (`enemies/archive_guardian.fof:44-47`, authored 2026-03-05) already states: *"A straight fight is survivable but very expensive… intended to be solved laterally."* "Survivable" ⇒ the party usually wins; "very expensive" ⇒ it costs exchanges, Sparks, and Endurance. The 45–55% coin-flip expectation *contradicted* canon the user had already established; conforming G1 to canon is the correct fix.

4. **G1 is reframed as a length-plus-cost gate.** Pass = median ≥ 3 exchanges + defeatable + zero house rules + snowball-doesn't-collapse-below-3 + a **cost signal** (Sparks spent, Endurance remaining, PC-Broken incidence) proving the fight was survivable-but-expensive. This is the Worker's Option 4, aligned with the BRIEF's *binding* success criterion (§"boss fights are runnable by the book for 3+ exchanges without house rules") rather than the voided descriptor.

5. **The exchange-length floor is cleared by the pre-authorized scalar lever, not a redesign.** At Resolve 5 the snowball (EF1's mandated rider→Easy, worst-case policy) collapses the fight to median 2 exchanges — the napkin check assumed Hard-difficulty Strikes throughout, but the first 10+ makes every subsequent Strike Easy for the rest of the fight. The Worker's diagnostic shows the median-3 floor clears at Boss Resolve ≈ 8. The risk register already pre-authorized this exact move ("Boss Resolve is a `facet.yaml` scalar — retune, don't redesign") and §5's note committed to Boss Resolve as the snowball lever. **A8 retunes the Guardian's base Resolve to the smallest value whose effective pool yields median ≥ 3 under the worst-case rider policy (≈8, confirm by sim) and widens the BRIEF's "working range 2–6" note to the confirmed ceiling.** The BRIEF flagged 2–6 as a *working range* and DESIGN §4.2 said starting values were "to be confirmed by G1, not asserted" — discovering the range must extend is precisely G1's job.

6. **Rejected: giving Bosses a structural second action / mandatory Techniques (Worker Options 1 & 3).** That is a rules change with MM1/III.3 consequences and cuts against the "minimize complexity/bookkeeping" pillar. The game already produces Boss-encounter difficulty at the correct layer — the **Encounter Budget** (adds, higher-TR configuration; Gate G4's domain) and the Boss's authored **Techniques** and **lateral weaknesses** (the Guardian's joint Maneuver, phase change, Tier-1 immunity, all in its `.fof`). Note the G1 sim strips Techniques, so it tests a Boss *below* its canonical TR-14; the length-plus-cost floor is therefore a genuine worst-case, and the real published Boss is harder than G1 certifies.

**A8 confirmation (Worker, 2026-07-10):** Resolve 8 confirmed by sim — n=200/seed=1 canonical run: 100% win rate, median 3.0 exchanges, 6.2/9 mean Sparks spent, mean PC-Broken 0.03. Robustness re-check across 7 seeds at n=200 holds median exactly at 3.0 in every seed (Resolve 7 was tried first and found seed-sensitive, flipping between median 2 and 3). `enemies/archive_guardian.fof`, `archive_guardian_def()`, and the BRIEF's D1 working-range note are all updated; TR moves 14 → 17. Full detail in `research/simulation_log.md` Series 7. G1 and G2 both pass; **A8 is closed.**

**Handed to Brain (non-blocking — does not gate A8; prose comes after G1/G2 per §5 ordering):** items 3–4 encode an ethos stance — *"a Boss's baseline stat block is not balanced for solo-viability against a full party; Boss-fight difficulty is produced at the encounter layer (adds, Techniques, lateral solutions), not the stat block."* That stance must be stated explicitly in MM1 Boss-design guidance and III.3 so an MM doesn't drop a lone by-the-book Boss and get a 100%-party-win non-fight. The mechanical resolution above is Planner-owned and canon-grounded, but the *player-facing framing* is Brain's ethos call. Flagged for Brain to bless when A11 prose is written; it blocks nothing now.

**Resolved. Return to Worker to continue A8** from the revised G1 pass condition (this section + the updated §5 table + TASKS A8).

**Ordering constraint:** G0 before any rules change. G1/G2 before III.3 or MM1 prose. G4 after G1/G2 (budget depends on durability). G3 is independent and may run in parallel.

**PT03 (`playtest/03_boss_stress_test/`) is the human acceptance test for G1** and runs after the sims pass. **PT04 (`playtest/04_resource_tax/`) is the acceptance test for D6.** Playtest data hygiene per BRIEF §Validation applies to both: real server rolls, per-player dice, reconciled modifier columns, drift findings flagged not adopted.

---

### 5-ter. G4 resolution — the Recipe Table is the calibrated tool; the TR-budget formula is demoted to a rough check (Planner resolution of the A10 escalation, 2026-07-10)

Worker A10 ran G4 and hit the same *class* of wall A8 hit at G1, now generalized: none of the five named baselines reproduces its target win-rate band (all land at ~100% win), and a ~20-configuration sweep (enemy count × per-enemy TR, 3 seeds each — `research/simulation_log.md` Series 9 Parts A–B) shows the real difficulty curve is **not the smooth, separable function the Encounter Budget formula assumes**. It is a steep, **actor-count-gated threshold**: 1–2 Named/Boss actors are trivial at *any* TR; 3–5 is a cliff; per-enemy TR is only a second-order modulator once past that gate; Mook swarms never produce real danger (mean PC-Broken 0.00 through 30 Mooks — the only win-rate dip past ~40 is the `MAX_EXCHANGES` timeout artifact). No values of `difficulty_multiplier`, `action_economy_multiplier`, `group_size_modifier`, or `TIER_WEIGHTS` reproduce this — the formula already assigns 1 Guardian (weighted 21.25) a higher score than 3 Sergeants (24.0, but 100% vs 81% win — not comparable) and far below 4 Sergeants (35.2, 20% win), i.e. exactly backwards from the counts (1/3/4) that actually predict difficulty. Planner triage:

1. **This is not a new finding — it is G1's §5-bis doctrine, confirmed at scale and extended to Named NPCs and multi-enemy math.** §5-bis already ruled "a Boss baseline is not solo-viable; Boss-encounter difficulty is produced at the encounter layer." G4 shows the same is true of Named NPCs, and names the mechanism precisely: **simultaneously-acting Named/Boss actor count is the primary difficulty variable, weighted-TR-sum is not.** Worker's Option 3 is therefore the correct *doctrine*, and it needs no new ruling — it is the one already blessed for §5-bis.

2. **The win-rate → multiplier mapping the formula encodes was already void.** Brain's Q3 ruling (BRIEF §Void) voided *every* Encounter Budget difficulty multiplier and their "~95/75/50/25% → ×1/×2/×3/×4" win-rate promises. A10 was scoped as "retune two constants" before that void's full consequence was visible; the constants it would retune are the very artifact Brain declared non-authoritative. **Rebuilding the formula (Worker's Option 2) would resurrect a Brain-voided artifact** — and try to fit a smooth continuous model to a cliff function, on only ~20 validated configurations. Rejected for A10.

3. **The mechanical execution is Worker's Option 1: the Recipe Table is the MM's authoritative, simulation-validated tool; the raw TR-budget formula is demoted to an explicitly-non-predictive rough check.** This is already how MM1 instructs MMs to build encounters ("pick your column, pick the difficulty row, use the composition" — not derive from budget arithmetic), and how the line-356 scaling note already hedges ("Named NPC count matters more than total TR"). A10 makes that hedge the *primary* framing rather than a footnote.

4. **Concrete scope for A10 under this ruling:**
   - **MM1 Encounter Recipe Table** becomes the calibrated deliverable — populated with A10's validated PS-3 rosters and their measured win rates + seeds (Series 9 Part C): Skirmish = 3–7 Mooks; Standard = 3× Named(TR8); Hard = 3× Named(TR8) + 1 Mook; Deadly = 4× Named(TR8) *or* 3× Named(TR8) + 2 Mooks. PS-4 row extended where Series 9 covers it; gaps flagged as un-simulated, not guessed.
   - **MM1 Encounter Budget / Action Economy sections** are reframed honestly: the `TR × multiplier` budget is a rough ordering sanity check, **explicitly non-predictive for 3+ Named/Boss rosters and for Mook swarms**, superseded by the Recipe Table. The "~95/75/50/25%" win-rate column must not be presented as validated (it was void-derived). Promote "actor count, not total TR, drives difficulty" to the section's lead.
   - **`encounter.py`**: **do not** retune constants to hit only the four listed recipes — that is the exact "looks authoritative, mis-predicts everything else" trap A10 escalated. Make the formula *honest*, not *precise*: update `calculate_effective_tr` / `calculate_budget` / `TIER_WEIGHTS` docstrings to state the formula is a rough heuristic, non-predictive for 3+ Named/Boss rosters, and point authors at the Recipe Table. Constants may be left as-is (loose ordering for simple/solo/Mook cases) or lightly adjusted only where that improves the *rough* ordering without implying false precision.
   - **Tests** (revised Accept, see TASKS A10): the calibrated artifact is now the Recipe Table, measured in the *simulator*, not the formula. Add sim-level characterization tests (in the `combat_sim`/calibration path) pinning that the four validated recipes reproduce their bands at the recorded seeds; add formula-level tests asserting the demoted formula's *documented* behavior (rough ordering; no false-precision claims) rather than "the multipliers hit the bands." The old "≥3 tests on the changed multipliers" criterion is superseded — we are not changing the multipliers to be predictive.

5. **Deferred, non-blocking, Brain/product-scope (does NOT gate A10):** whether the digital layer should eventually be able to grade an *arbitrary* roster's difficulty (a genuine actor-count-primary predictive model — Option 2 done properly, with the validation budget it needs) is a product-ambition question, not an A10 retune. Recorded as an open question for Brain/the user to weigh later. A10 ships the honest table + demoted formula now; nothing waits on this.

6. **Prose framing rides on the ethos note already handed to Brain in §5-bis.** That note ("a Boss baseline is not solo-viable; difficulty comes from the encounter layer") is extended by G4 to: *"multi-enemy difficulty is driven by simultaneously-acting Named/Boss actor count, not total TR; the Recipe Table is the tool, the budget formula is a rough check."* Same ethos bucket, same A11 prose pass, same Brain blessing at prose time — **no new Brain round-trip is required to unblock A10.** A11's Encounter-Budget prose is written to this framing.

**Resolved by Planner. Return to Worker to execute A10** under the revised scope + Accept criteria in TASKS A10. No Brain round-trip required to proceed.

---

### 5-quater. PT03 resolution — Boss phase-change subsystem + A13 Accept (Planner resolution of the A13 escalation, 2026-07-11)

Worker A13 ran PT03 by the book (n=300, seed 1: win 99.7%, mean 2.9 exch, PC-Broken 0.20/fight, zero house rules) and escalated two blockers. D1/D2 held up with zero house rules — Resolve depletion, rider→Easy, the per-scene armor budget, and the retired 0-Endurance rule all behaved. The failures are one layer up: the Accept bar (F0) and the Boss phase-change subsystem (F3–F5, F8). All four engine findings were verified against source before this ruling (`combat.py:368/372/483`, `combat_sim.py:480–494`, `facet.yaml:1052/1097`). Planner triage:

1. **F0 — A13's "≈Hard win rate" Accept is void-derived; drop it, do not re-scope PT03.** This is the last live instance of the win-rate→difficulty mapping Brain voided in Q3 and §5-bis already struck for G1. A lone Boss vs. three focus-firing PCs is, by ratified doctrine (§5-bis action-economy argument, III.3:325 prose), *not* an even fight — which is exactly the matchup PT03 forces by design. 99.7% is the expected, doctrine-consistent outcome, not a failure. **Revised A13 Accept (replaces the win-rate bar with the §5-bis shape):** (a) median ≥ 3 exchanges; (b) cost signal recorded — mean Sparks spent, mean PC Endurance remaining at fight end, PC-Broken incidence — as evidence the fight is *survivable but expensive*; (c) **the phase change fires in a meaningful fraction of by-the-book fights** (this is the real content PT03 exists to certify — a Boss whose second act never triggers is not a validated Boss). Keep it a **lone-boss** run: that is precisely what stress-tests the phase subsystem. A boss-in-an-encounter (allies/terrain/Technique) is a *different*, later playtest — do not fold it into A13.

2. **F5 — enemies do not spend a resource to react. Rule: an enemy has no reaction; a Strike against it depletes Resolve by outcome, full stop.** This is not a new ethos call — it is the *already-settled* asymmetric-combat doctrine ("NPCs don't roll; PCs react") plus Q4's "Resolve is durability, not an action-economy pool." The sim invented an enemy Parry paid out of Resolve (`combat_sim.py:483`) because `reaction_cost` was written for the PC Endurance pool and enemies have none. Remove `should_enemy_react` and the entire enemy-Parry block from `combat_sim.py`. Enemy durability is Resolve + phases, never out-defending the party. Same doctrine bucket as §5-bis; Brain blesses at execution time, no round-trip required.

3. **F8 dissolves under (2).** Enemy Parry as modelled is strictly self-defeating (cost 1 Resolve to prevent a 2-Resolve Strike, but a partial parry is a wash and a failed parry is a net loss — the enemy spends its durability pool to defend its durability pool). Removing enemy reactions (2) removes the mechanism entirely. No separate fix.

4. **F4 — real engine bug, mostly dissolved by (2); encode the invariant anyway.** Once enemies never react, `resolve_current` moves *only* through `apply_resolve_damage`, which already routes every change through `phase_crossed` — so the missed-crossing path is closed on the common path. Regardless, encode the invariant: **any mutation of `resolve_current` must run through phase-crossing detection**, never a raw decrement. One hardening test: a Strike (or any depletion) that lands Resolve exactly *on* a threshold fires that phase exactly once.

5. **F3 — "reduce armor" is dead under D1; define a D1-native Boss-phase effect vocabulary.** Under D1 armor is a flat one-time Resolve bonus baked into the starting pool (`combat.py:372`); a mid-fight "armor cracks / trade defense for danger" phase has nothing to reduce, so every MM1 Boss on that pattern is mechanically hollow. A D1-native phase must change *runtime* state. Supported phase effects:
   - **raise offense** — increase the incoming-tier the Boss inflicts, or its attack posture/modifier ("grows more dangerous");
   - **grant/revoke a Special** — e.g. the Archive Guardian's Reduced Mode = Tier 1 rider immunity, already modelled as `special_ignores_tier1` gated on `phase_index`;
   - **second wind** — add Resolve (a genuine durability spike, legible because it moves the bar the players are watching);
   - **change targeting / add a standing effect** — narrated by the MM, engine-optional.
   Explicitly **not** supported: "reduce own armor," or any "trade durability for danger" framed through armor. Today a phase's mechanical effect is ad hoc (`special_ignores_tier1` is the only engine-honoured one; the rest is `phase_index`-informational). This ruling makes that set the *documented* vocabulary; a `phases[].effect` schema field to carry it machine-readably is a **candidate**, not required — phases may stay MM-narrated with the engine honouring only the small supported set. MM1's Boss phase-design guidance and the "trade defense for offense" pattern text are rewritten to this vocabulary. Brain blesses the phase *feel* at prose time (same pattern as §5-bis/§5-ter); no hard round-trip.

6. **Sequencing after this ruling.** F5/F8/F4 are a `combat_sim.py` + engine cleanup with tests (a Worker task — call it **A14**). F3 is an MM1 prose rewrite + optional schema field (fold into the same A14, or a dedicated content task). A13 re-runs against the revised Accept *after* A14 lands (the current 2.9-exchange borderline-fail is entangled with the buggy parry/phase model — do **not** retune Boss Resolve until enemy reactions are removed and the phase subsystem is coherent; if median still lands below 3 then, Boss Resolve is the sanctioned `facet.yaml` scalar per §5-bis / the Risk table, not a redesign).

**Resolved by Planner. Return to Worker: open A14 (F5/F8/F4 engine+sim cleanup + F3 MM1 rewrite), then re-run A13 against the revised Accept above.** No Brain round-trip required to proceed — every ruling follows from doctrine already ratified (§5-bis, Q4). Brain blessing rides on the A14/A11-class prose pass, at prose time.

---

## 6. Workstream WS-B — Advancement math (D3)

### 6.1 The current pacing, derived

Constants: `session_skill_points: 4`, `skill_point_costs` primary 1 / cross 2, `marks_per_rank: 3`, `facet_level_threshold: 6`, `major_advancement_threshold: 4`. A Facet holds 5 skills × 3 rank advances = **15 advances maximum**.

At 4 SP/session all into the primary Facet: 4 marks/session → 1.33 rank advances/session. A Facet level costs 6 advances = 18 marks = **4.5 sessions**. Level 1 ≈ session 5, level 2 ≈ session 9. Level 3 needs 18 advances against a 15-advance ceiling — **impossible in-Facet**. Cross-Facet marks cost 2 SP, so 2 marks/session → one rank advance per 1.5 sessions → a cross-Facet level costs ~9 sessions on top. First Major Advancement (4 levels) lands ~session 25–27, matching the BRIEF. Tier 3 Techniques need three same-branch picks and therefore three Facet levels: same wall.

### 6.2 The fix

Two constants move. `session_skill_points` and the cross-Facet cost of 2 do **not** — the cross-Facet cost is the flavour, and raising SP inflates skill ranks as a side effect.

| Constant | Now | v0.3 | Effect |
|---|---|---|---|
| `facet_level_threshold` | 6 | **5** | 15 ÷ 5 = **3 levels reachable inside the primary Facet** — Tier 3 unlocks without cross-training |
| `major_advancement_threshold` | 4 | **3** | First Major lands with Facet level 3 |

Plus the F3 code fix (per-Facet advance tracking; `total_facet_levels` = sum across Facets) and the D3 rule (any Facet level grants one pick from any tree whose prerequisites are met).

### 6.3 Pacing table — the DESIGN's verification of its own numbers

Real players do not funnel 100% of SP into one Facet. Modelled at three efficiencies (fraction of the 4 SP/session spent on primary-Facet marks):

| Primary-SP efficiency | Marks/session | Advances/session | Sessions per level (5 advances = 15 marks) | Level 1 | Level 2 | **Level 3 → Tier 3 + first Major** |
|---|---|---|---|---|---|---|
| 100% | 4.0 | 1.33 | 3.75 | s4 | s8 | **s12** |
| 80% | 3.2 | 1.07 | 4.69 | s5 | s10 | **s15** |
| 60% | 2.4 | 0.80 | 6.25 | s7 | s13 | **s19** |

Original BRIEF targets: Tier 3 by session 12–15; first Major by session 10–12. The 100%–80% band lands Tier 3 at s12–s15 ✓. First Major coincides with level 3 at s12–s15 — later than the original s10–12. The 60% column shows the dedicated-but-broad character at s19, which is acceptable for a character who chose breadth.

**Ruled by Brain (Q1): accept s12–s15 for both. The BRIEF's pacing target is amended to *"Tier 3 and first Major Advancement land together, roughly session 12–15 for a dedicated character."*** The s10–12 figure was illustrative, meaning "much sooner than 25–27" — it could not have been derived from observation, because per F3 no character has ever reached a Major Advancement in code. Pulling Major earlier means `major_advancement_threshold: 2`, which fires it at level 2 (~session 8) — too cheap for a "culmination of a long arc" beat, and it decouples Major from the Tier 3 moment. A converging payoff is one milestone session instead of two diluted ones. **`session_skill_points` stays at 4**: rank inflation is a worse cost than a three-session slip on an illustrative number. Recorded as P5.

**Brittleness note:** with threshold 5, level 3 lands on advance 15 of 15 — the very last primary advance available. A character who reaches level 3 has, by construction, mastered all five primary skills. This is intentional and readable ("Facet level 3 = you have taken this Facet as far as it goes"), but it means level 4+ still requires cross-training, as `II.4:83` already says.

**The sidebar this falsifies** *(BRIEF §EF2).* II.4's philosophy sidebar (~line 85) reads *"Facet level 3 isn't earned by going deeper; it's earned by going wider."* That is true at threshold 6 and **false at threshold 5**, where level 3 is reachable entirely in-Facet. Task B5 must rewrite it — honest new framing: *level 3 = you have mastered all five skills of your Facet; level 4+ is where breadth begins.* Left unrewritten, it is ledger row 10 the day B2 lands.

### 6.4 Technique pick budget (F4)

Add `Character.technique_picks_available: int`, incremented on every Facet level in any Facet, decremented by `technique_select`. `_handle_technique_select` gains: reject when `technique_picks_available == 0`. Prerequisite checking is already correct and already tree-agnostic — D3 needs no change there, only the PHB text catches up to the code.

**Test strategy:** `test_character.py` — per-Facet level tracking, cross-Facet levels counting, threshold boundaries at exactly 5/10/15 advances, Major at 3 levels, pick budget increment/decrement, pick-budget-zero rejection. `test_websocket.py` — `technique_select` rejected with no picks; accepted from a non-primary tree with prerequisites met.

---

## 7. Workstream WS-C — Consolidation pass (D5)

**Runs first.** It is cheap, it produces clean diffs for A and B, and it ends the stale-rules contamination that corrupted playtest 06. One commit.

Ledger — the BRIEF's eight rows plus row 9 from F3, and the two rows below that are code fixes, not text fixes:

| # | Rule | Canonical | Fix locations | Code? |
|---|---|---|---|---|
| 1 | Pre-technique magic | Minor scope only, **no** difficulty penalty | `II.5` (stale); verify `II.3`, `MM5`, `Quick_Start`, `facet.yaml:998` | verify only |
| 2 | Broken threshold (PC) | Second Tier 2 **of the same type**; Staggered + Cornered coexist | `III.3` quick ref, `MM5` | **yes — `websocket.py:681`** (F6) |
| 3 | Parry | Outcomes identical to Dodge — no counter | `III.3` quick ref, `MM5` | no |
| 4 | Weapons / Strike | Weapon category sets attribute (IV.1); skill = Combat (melee/unarmed) or Finesse (ranged); formula "2d6 + weapon attribute + relevant skill" | `III.3`, `MM5`, `Quick_Start` | engine already permissive |
| 5 | PvP ties | Both achieve partial success (III.1) | `MM5` | no |
| 6 | Attribute label | Rating 1 = "Weak" | `MM5` | `facet.yaml:102` already correct |
| 7 | Ghost text | Delete "Spent ally" (Intercept); Maneuver reads "rolls **against** the target are Easy"; MM1 phase triggers re-keyed | `III.3`, `MM1` | phase re-key deferred to WS-A |
| 8 | Example continuity | Zahna: Inscription / Knowledge / Spirit 2 / he. Zulnut: Wandering Disciple / he. Mordai: Endurance Novice +1 mark, pool 5 | `II.3`, `II.4`, `II.5`, `III.3` vs `Quick_Start` + `characters/*.fof` | no |
| **9** | **Facet level counting** | **Cross-Facet levels DO count toward Major Advancement** | **`II.4:89` (stale sentence)** | **yes — WS-B (F3)** |

**New repo rule** (D5, into `CLAUDE.md`): quick references may only compress canonical text, never paraphrase it; any rules change must update body text, all quick refs, `facet.yaml`, and the engine in one commit.

**Scope discipline:** WS-C fixes rows whose canonical answer is already settled. It does **not** touch armor text (WS-A owns it) or the "Advancement at a Glance" block (WS-B owns it). Row 2's *code* fix lands in WS-C because it is a one-line predicate; its *simulation* consequence is measured in G2.

**Test strategy:** row 2 gets three tests (same-type second Tier 2 → Broken; different-type second Tier 2 → both coexist, no Broken; third Tier 2 of a coexisting type → Broken). Text rows get a `continuity-check` pass, not unit tests.

---

## 8. Workstream WS-D — Death, hazards, Sparks (D4 + D6)

### 8.1 III.2 Adventuring — minimal chapter, strictly scoped

Three sections only: **Hazards and Threat Clocks**, **Getting Hurt and Getting Better** (recovery), **When a Character Would Die**. No exploration procedures, no travel, no downtime. The BRIEF authorises the chapter's existence, not its expansion.

**Threat Clock.** Four segments, visible to the table. Advances one segment on any party 7–9 or 6- result taken near the hazard. When full, the hazard strikes: a Condition, or a forced roll against a stated difficulty. Players may spend an action to wind it back one segment — **this is automatic, and costs no roll** *(Brain ruling, BRIEF §EF4)*. A rolled wind-back would let a 7–9 advance the very clock being wound: a rules-lawyer loop, in a chapter written for novice MMs. No new resolution mechanics — it reuses the existing outcome tiers, per BRIEF non-goals.

**Stated pacing, on purpose.** Roughly 72% of nearby rolls advance the clock, so a 4-segment hazard strikes after about 3–4 party rolls. That is the intended feel of "visible pressure" — III.2 must **say so deliberately** rather than leave it as an emergent accident of the tier probabilities.

`facet.yaml` gains `hazards.threat_clock: {segments: 4, advances_on: [partial_success, failure], wind_back_cost: 1_action, wind_back_requires_roll: false}`.

**Death rule** (one paragraph, adapted — not copied — from `playtest/06_expert_novice_campaign/fun_and_consequence_review.md` Revision 1; strip its "below 0 Endurance" framing, which is not how our rules work):

> Broken never kills you. When a Broken result would end your character's life in the fiction, the choice is yours and no one else's: take a **permanent scar** — a lasting cost the MM and you name together — and stay down, alive; or choose a **heroic death**, and take one final action that automatically succeeds.

**Recovery.** Tier 1 clears at end of exchange (existing). Tier 2 clears when treated (existing) — III.2 states what "treated" means: a scene, a successful relevant skill roll, or a rest. Tier 3 (Broken) clears at end of scene (existing).

### 8.2 D6 — Spark economy

`facet.yaml`'s `spark.earn_methods` already contains `act_break_nomination` and `graceful_fail`. Two changes:
- `graceful_fail.structured: false` → **`true`**, with a description that makes it **player-initiated**: on any 6-, the player may claim it by narrating how they make the failure worse or richer; MM confirms.
- Both methods get PHB text in **III.1 Core Resolution** — the BRIEF is explicit that this belongs in the player-facing chapter, not MM5 alone.

Engine: new WebSocket event `claim_graceful_fail` (player-initiated → broadcasts a claim for MM confirmation, mirroring the existing `spark_earn_peer` nomination shape at `websocket.py:324`). `act_break` event for the MM to open a nomination window. Keep 3 Sparks/session, spend-before-roll, add-die-drop-lowest. **No post-roll spending.**

`spark_refund_on_failed_pretechnique_cast` ships as a **variant flag**, default off, tested in PT04. Not adopted.

### 8.3 Threat Clocks are player-facing UI, not WebSocket frames

*(Brain ruling, BRIEF §EF8.)* A clock that exists only in the engine is bookkeeping the digital layer **failed** to absorb — a direct ethos violation, in the one chapter whose whole purpose is to keep a novice MM from inventing subsystems. Task WD8 renders clocks in the Play Field for every player, with create / advance / wind-back controls for the MM. "Visible to the table" is a UI requirement, not a prose flourish.

### 8-bis. WD8/PT04 resolution — the D6 acceptance instrument is invalid; D6 is not revisited (Planner resolution of the WD8 escalation, 2026-07-11)

**Ruling: D6 is NOT revisited. The measured 1.51 Sparks/player is void as evidence — it is not a measurement of D6.** WD8's Accept is not *not met*; it is **unmeasured**. WD1–WD7 land now. WD8 is voided (banner, not deleted) and reopened as **WD8-R**, behind two instrument-repair tasks (**WD9**, **WD10**). WS-D is not complete until WD8-R closes.

**Three independent instrument defects. Any one of them alone voids the number.**

1. **The PT04 roster is stale — it predates P10 and is built on the demoted budget formula.** `scenario.md` derives all three encounters from `TR × multiplier` arithmetic it shows inline ("Tier-weighted: (9 × 1.0 + 3 × 1 × 0.5) × 1.1 = 11.55 effective TR. Above Hard budget — good"). P10 demoted that formula as explicitly non-predictive for exactly these compositions. Re-read against the calibrated Recipe Table: Encounter 1 (3 Mooks) is a true Skirmish; Encounter 2 (6 Mooks) is **Mook-only — Series 9 measured mean PCs Broken at 0.00 through 30 Mooks**, so it is not Standard, it is a second Skirmish; Encounter 3 (1 Named TR-9 + 3 Mooks) is a **1-Named roster — Series 9's headline finding is that 1–2 Named/Boss actors of *any* TR are trivial**, so the "coin-flip Hard climax" is trivial. **The 100% win rate at every encounter is not an anomaly needing explanation; it is precisely what Series 9 predicts for this roster.** A resource-tax session that levies no resource tax cannot measure a resource tax. Mordai finishing at 5/5 Endurance is the roster's doing before it is the AI's.

2. **The spend policy is pre-D6, and tautological as an instrument.** `should_spend_spark` fires only against a Boss, on desperation (End ≤ 2), or as a T2 finisher — and this session has no Boss and never pressures anyone. But the deeper defect survives any retuning: **a hardcoded spend rule cannot be evidence for or against a claim about spend *behaviour*.** D6 is a behavioural hypothesis — *a richer earning cadence loosens hoarding*. Run it through a heuristic with no model of hoarding, scarcity, or incentive, and it returns the heuristic's own rule back to us. Worker's Option 1 as posed (retune the heuristic, re-run) trades one tautology for a differently-tuned one: we would be picking the spend rate we want and then "measuring" it.

3. **The harness measures the wrong domain.** `combat_sim` can only spend Sparks inside `resolve_strike`. In real play Sparks are spendable on **any** roll — investigation, social, magic scope. "Mean Sparks spent per player per session" measured on a combat-only harness is a strict subset of the quantity D6's Accept names. Even with defects 1 and 2 repaired, this harness yields a **floor**, never the metric.

**On the Worker's two options — both are partly right, neither as posed.**

- **Option 2 is what DESIGN §5 (line 206) already required, and WD8 silently substituted away from.** That line reads: "**PT04 is the acceptance test for D6.** Playtest data hygiene per BRIEF §Validation applies: real server rolls, per-player dice, reconciled modifier columns." A 1,400-run Monte Carlo through `combat_sim` is not a playtest under that rule — it never touches the server and it has no players. WD8 was *executed as a simulation of a task specified as a playtest*. **That substitution, not the 1.51, is the real finding here.** No fault to the Worker: the task line said only "Run with the new Spark cadence…", and WD8 sits in a workstream where every neighbouring task is code. The task was underspecified about *how*. That is a Planner defect and it is corrected in WD8-R.
- **Option 1 is genuinely needed — but not in place.** Every canonical PC in `combat_sim` starts `sparks=3`, and spent Sparks add dice to Strikes, so they move win rates. Editing `should_spend_spark` in place would silently re-baseline every recorded G0–G4, A-series, and Series-9 number. **This project has already been burned by exactly this once** — the A14 escalation records the F5 fix invalidating the whole Series-9 recipe corpus. We do not repeat it by hand. The spend policy therefore becomes **selectable**, default = today's exact behaviour, so every recorded corpus stays bit-reproducible (WD10).

**Rejected:** *Revisiting D6 on this data* — nothing about D6 was measured, and revising a rule against a broken instrument is how a ruleset acquires superstitions. *Deleting the run* — this project keeps voided corpora with a void banner (Series 9 precedent); a recorded negative result about the harness is worth more than a clean slate. *Widening WD8's file scope in place to reach into `combat_sim.py`* — the Worker was right to stop at its scope boundary; that instinct is the process working, not failing.

**Accept criterion, amended.** The **≥ 2 Sparks spent per player** bar stands, but is re-scoped: it is measured **over a session, across all rolls (not only Strikes), from a real server roll log**, per playtest hygiene. The Monte Carlo may report a combat-only floor *alongside* it, labelled as such, and is never the deciding number.

---

## 9. Workstream WS-E — Content (D7)

Pure writing, no engine impact, parallelisable with everything after WS-C.

- **Domain example intents** → `player_handbook/Appendix_Magic_Domains.md`. Three examples **per scope**, three scopes (Minor / Significant / Major), 18 domains = **162 entries** *(corrected per BRIEF §EF3; the earlier "= 54" miscounted, dropping a factor of 3)*. Framed explicitly as *design patterns*, not a menu. Variety within a scope is the anti-canonization mechanism: one example per scope becomes "the Minor Inscription spell" within two playtests. Entries stay one line each. Pre-set "spell packages" rejected — that is a spell list by another name. **If the entries start reading like castable spells mid-writing, stop and escalate.**
- **MM Trouble Table** → `MM5`. A d6 of generic 6- consequences: cost / position / attention / equipment / condition / revelation.
- **Magic 6- templates** duplicated from `II.3` into `MM5` — under the new repo rule this is compression of canonical text, which is permitted; a paraphrase is not.

Copyright policy applies. Vignette voice per `references/phb-examples.md`.

---

## 10. Sequencing

```
WS-C  consolidation ──┬─→ WS-A0 extraction ──→ WS-A durability ──→ G1,G2,G4 ──→ PT03
  (first, one commit) │        (G0 gate)         (D1,D2,F5)
                      │
                      ├─→ WS-B advancement (D3,F3,F4) ────────────────────────→ PT05
                      │        (independent)
                      │
                      ├─→ WS-D death/hazards/sparks (D4,D6) ──────────────────→ PT04
                      │        (independent of A; III.2 text after A settles lethality)
                      │
                      └─→ WS-E content (D7)
                               (fully parallel)

G3 (Aggressive K1) runs any time after WS-A0.
```

Hard dependencies: **A0 before A** (F1). **C before everything** (clean diffs). **G1/G2 before III.3 and MM1 prose** (simulation before prose). **A before III.2's recovery section** (lethality changes what recovery must do).

Soft: WS-B, WS-D, WS-E are mutually independent and may be worked in any order by separate Worker sessions.

---

## 11. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The A0 extraction changes behaviour silently and G0 hides it behind Monte Carlo noise | Medium | **Closed by EF5.** Exact seeded end-state match is now G0's primary criterion; the ±3pp band is demoted to a secondary check used only when draw order legitimately changed. |
| A Worker implements riders as inert flags, and G1 certifies a game nobody will play | **High** | EF1 makes rider→Easy a tested behaviour in A4 (two dedicated tests) *before* A8 runs G1, and A8 restates the dependency. |
| F6 + D2 + F5-removal together make PCs unkillable | **High** | G2 varies the three factors independently. If PC Broken rate at Hard drops below 30%, tighten Resolve/armor before touching Conditions. |
| Resolve 5 Boss + heavy armor overshoots and the Boss fight drags past 5 exchanges | Medium | G1 measures median exchanges. Boss Resolve is a `facet.yaml` scalar — retune, don't redesign. |
| `facet_level_threshold: 5` puts Tier 3 on the literal last primary advance; any content addition (a 6th skill) silently changes pacing | Low | The pacing table in §6.3 is a regression test: `test_advancement_pacing.py` asserts levels land at 5/10/15 advances. |
| WS-C's text edits collide with WS-A/WS-B text edits in `III.3` / `II.4` | Medium | Scope discipline in §7 — C does not touch armor text or the at-a-glance block. |
| Legacy `.fof` files with `endurance` break for users | Low | One-cycle back-compat read with `DeprecationWarning`; `to_fof` writes only `resolve`. |

---

## 12. Open questions — ALL RESOLVED (Brain, 2026-07-10)

1. **D2 armor shape.** ✅ **Approved** (Brain Q2). Per-scene budget, light 2 / heavy 4, `downgrades_per_scene`. The BRIEF's per-exchange candidate cannot break an armored PC in a single-enemy boss fight — §4.2. **A5 unblocked.** *(P4)*
2. **Major Advancement timing.** ✅ **Approved** (Brain Q1). s10–12 was illustrative; Tier 3 and first Major land together at s12–15. `session_skill_points` stays 4. **B2 unblocked.** *(P5)*
3. **Archive Guardian TR.** ✅ **Approved** (Brain Q3). Corrected to 14. *(P6)*
4. **0-Endurance rule.** ✅ **Approved** (Brain Q3). Retired; PC-side win rates in `research/simulation_log.md` marked `SUPERSEDED (v0.2 semantics)`, not deleted; G2/G4 re-baseline from zero. *(P3)*
5. **Asymmetric armor.** ✅ **Approved** (Brain Q4) as ethos-*consistent*, not merely tolerated. Presentation requirement now binding on A11 — two tools, never one rule with an exception. *(P8)*

Nothing remains blocked. Brain's eight editorial findings (EF1–EF8) are patched into this DESIGN and into `TASKS_v0.3_ruleset_revision.md`.

---

---

## ESCALATION — Planner → Brain (2026-07-10)

**Status:** ✅ **RESOLVED by Brain, 2026-07-10.** Rulings recorded in `docs/BRIEF_v0.3_ruleset_revision.md` §BRIEF AMENDMENT. Summary: Q1 accepted (P5 stands; s10–12 was illustrative). Q2 approved (per-fight budget — renamed **per-scene**; `downgrades_per_scene` in `facet.yaml`). Q3 ruled per recommendation (PC-side numbers void, TRs survive, behavioural playtest findings survive as behaviour; WS-A0 retroactively authorised; simulator-may-never-reimplement-rules added to the C1 repo rule). Q4 approved (asymmetry is ethos-consistent; present as two tools, never one rule with an exception). **A5 and B2 are unblocked.** Brain's editorial review also found eight plan defects (EF1–EF8 in the BRIEF amendment — most critically: rider Conditions have no defined effect, and G1 must simulate rider→Easy or it validates the wrong game). Return to Planner for a small TASKS patch, then Worker at C1; C1 may start in parallel.

**Full packet:** `docs/HANDOFF_v0.3_planner_to_brain.md`

Four items require Brain:

1. **Q1 — Major Advancement pacing.** The BRIEF's "first Major by session 10–12" is not reachable without firing it at Facet level 2 (~session 8), which cheapens the beat and decouples it from Tier 3. DESIGN §6.3 lands both at s12–15. Need to know whether s10–12 was load-bearing or illustrative.

2. **Q2 — D2's candidate armor shape is unsound.** "Downgrade the first incoming Condition per exchange" cannot break an armored PC, because a boss fight delivers ~1 Condition per PC per exchange (`combat_sim.py:698-706`), so the downgrade never binds. It is the same infinite loop from `research/armored_enemy_breaking_problem.md`, moved to the player side, and it is currently masked by the 0-Endurance house rule that P3 retires. Planner substitutes a per-fight downgrade budget (light 2, heavy 4). Needs approval — Planner is replacing a mechanism the BRIEF proposed, not merely filling one in.

3. **Q3 — The evidence base is weaker than the BRIEF assumes.** Combat resolution is implemented twice and the copies disagree (DESIGN §1 F1), so `research/simulation_log.md` validated the simulator, not the game. Separately, Major Advancement has never fired in code (§1 F3) — every advancement-pacing observation was made against an engine that could not advance. Brain should rule on how much of the recorded corpus survives. Planner's read: PC-side lethality figures and Encounter Budget multipliers are void; enemy-side TRs survive intact.

4. **Q4 — Armor becomes asymmetric** (flat Resolve for enemies, Condition mitigation for PCs). Follows from D1's "Conditions replace HP → PCs only," but it is an ethos call and Brain owns the ethos.

**Recommendation:** *Switch to Fable to resolve Q2 and Q3 before task A5. Q1 and Q4 have safe defaults recorded in `docs/DECISIONS.md` (P5, P8); a Worker may proceed on those. Begin Worker at WS-C task C1 in parallel — it is unblocked by all four.*

---

*Planner output complete. Task decomposition: `docs/TASKS_v0.3_ruleset_revision.md`. Rationale and rejected alternatives: `docs/DECISIONS.md`. Begin with WS-C.*
