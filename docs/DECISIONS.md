# DECISIONS

Tradeoffs, rejected alternatives, and rationale — recorded at whatever tier made the call.
Brain decisions (D-numbers) live in the BRIEF. Planner decisions carry P-numbers. Worker decisions carry W-numbers.

---

## v0.3 Ruleset Revision (2026-07-10)

### P1 — Extract `app/game/combat.py` before any D1/D2 work

**Decision:** Insert a workstream (WS-A0) that the BRIEF did not ask for: extract combat resolution into a single pure module consumed by both the WebSocket engine and the combat simulator.

**Why:** Combat resolution is currently implemented twice — `api/websocket.py` and `tools/combat_sim.py` — and the two copies disagree about armor. In the engine, light armor downgrades a Tier 1 condition to nothing (`websocket.py:626-656`); in the simulator, light armor affects Tier 2 only (`combat_sim.py:237-253`). The simulator also carries a 0-Endurance escalation rule that exists nowhere else in the project.

The BRIEF's validation strategy is *"simulation before prose — D1/D2 must be re-simulated before PHB text is rewritten."* That strategy is unsound while the simulator is a re-implementation rather than a measurement of the engine. Every number in `research/simulation_log.md` validated the simulator, not the game.

**Cost:** three tasks (A0.1–A0.3), one new test file, one refactor of two modules.
**Rejected:** patching D1/D2 into both copies in parallel. Cheaper now, but it doubles every subsequent rules change and guarantees the divergence recurs. The permanent parity test in A0.3 is the point.

---

### P2 — Characterize the *simulator's* semantics, not the engine's

**Decision:** The A0.1 characterization tests pin `combat_sim.py`'s behaviour as the pre-refactor baseline, even though the engine is the production code path.

**Why:** Everything in `research/simulation_log.md` — the encounter budget calibration, the chicken baselines, the Veteran Soldier series — was measured under simulator semantics. Pinning engine semantics would make G0 (behaviour preservation) unverifiable against the only recorded data we have.

**Consequence:** the engine's armor behaviour is treated as a defect from the outset rather than a baseline to preserve. It is replaced by D2 two tasks later, so nothing is lost.

---

### P3 — Retire the 0-Endurance rule outright

**Decision:** Delete `is_zero_end_absorb` (the rule that Absorbed conditions become persistent Tier 2 at 0 Endurance). Do not port it into `combat.py`.

**Why:** It was Option A of `research/armored_enemy_breaking_problem.md`, adopted into the simulator to give *armored enemies* a breaking condition. Under D1, enemies have no condition track and no breaking condition — the rule's reason for existing is gone. Under D2, armored PCs are breakable through the per-exchange downgrade cap. The rule survived by inertia and appears in no PHB chapter, no `facet.yaml` key, and no engine path.

**Consequence:** PC lethality drops relative to every recorded simulation. All PC-side win rates in `research/simulation_log.md` were measured with this rule active and are invalidated by its removal — independently of D1. Gate G2 re-baselines them.

**Interaction:** softer combat plus an explicit death policy (D4) is the intended combination, not an accident. But this stacks with the F6 fix (Broken now requires a second Tier 2 *of the same type*), and stacking three durability buffs blind risks unkillable PCs. G2 varies the three factors independently.

**Rejected:** keeping it as a `facet.yaml` variant flag. It would be a rule nobody can find, defaulting to a value nobody chose.

---

### P4 — Armor is a per-scene downgrade budget *(✅ approved by Brain, 2026-07-10 — BRIEF §Q2)*

**Decision:** Light armor downgrades the first **2** Conditions received per **scene** by one tier (T2→T1, T1→none). Heavy armor downgrades the first **4**. The budget does not reset between exchanges; it resets when the scene ends. Starting values for gate G2, not assertions.

**Terminology amendment (Brain):** the word is **scene**, not "fight." The first draft of this entry used both in the same paragraph, and they differ whenever a scene contains two fights — which then share one budget. `facet.yaml` key: `downgrades_per_scene`. Player text says scene.

**Brain accepted responsibility for the unsound candidate:** the BRIEF's per-exchange shape reasoned from the party-focus-fires-a-target threat model, which D1 had already moved to Resolve.

**Superseded first draft (recorded because the error is instructive):** light downgrades the first Condition *per exchange*, heavy the first two. **This does not work.** Broken is only reachable by taking a second Tier 2 while already holding one, and Tier 1 clears at end of exchange — so any rule that downgrades every incoming Tier 2 *within* an exchange prevents accumulation permanently. The question is how many Conditions a target receives per exchange, and `combat_sim.py:698-706` gives each enemy exactly one attack per exchange against one PC, with incoming tier set by enemy tier (Mook 1, Named/Boss 2). **In a boss fight — one enemy — a PC receives at most one Condition per exchange, so a one-per-exchange downgrade absorbs it forever.** The light-armored PC cannot be Broken by a boss.

The first draft reasoned from "a party focus-fires an armored target," which is the *enemy* threat model. Under D1 enemies no longer carry Conditions at all — their armor is flat bonus Resolve (P8). The counter only ever runs PC-side, where the incoming rate is ~1/exchange and it never binds. **The BRIEF's own candidate shape (light = first per exchange; heavy = that plus one per scene) has the identical flaw**, which is why this is escalated rather than decided.

The flaw is currently masked by `combat_sim.py:548-551`, which forces landed hits back to Tier 2 at 0 Endurance. **P3 retires that rule, so P3 plus the per-exchange shape would reopen the loop** — and PT03, the acceptance test for D1/D2, is a single-enemy boss fight: exactly the scenario that surfaces it.

**Why the per-scene budget meets the D2 constraints:** capacity is genuinely finite over the scene, so armored entities are breakable (against a boss landing Tier 2 each exchange: unarmored Broken ~exchange 2, light ~4, heavy ~6). Heavy strictly beats light. Heavy mitigates Tier 2 — it is the same downgrade, twice as often. IV.1's fictional weight is untouched. One integer, one clock, no mid-fight reset.

**Rejected — residue instead of depletion:** armor downgrades every Tier 2 to Tier 1, but a Tier 1 taken *through* armor persists past end of exchange and a second escalates back to Tier 2. Armor never "runs out," which is conceptually cleaner, but it requires tracking two distinct kinds of Tier 1 Condition at the table — the bookkeeping this game exists to refuse.

**Status:** ✅ **Approved by Brain** (BRIEF §Q2). Meets all four D2 constraints; one integer of state the digital layer absorbs; diegetic fiction (armor takes the first blows of a fight, then it is dented and hanging). The "residue" alternative stays rejected for exactly the reason given. **Task A5 is unblocked.**

---

### P5 — First Major Advancement lands at Facet level 3 (~session 12–15) *(✅ approved by Brain, 2026-07-10 — BRIEF §Q1)*

**Decision:** `facet_level_threshold: 6 → 5` and `major_advancement_threshold: 4 → 3`. Leave `session_skill_points: 4` and the cross-Facet cost of 2 SP alone.

**Why these two constants:** a Facet holds 15 rank advances (5 skills × 3). At threshold 5, that is exactly 3 Facet levels — so Tier 3 Techniques become reachable *inside* the primary Facet, which is what D3 needs. At `major_advancement_threshold: 3`, the first Major coincides with Facet level 3. Raising `session_skill_points` instead would inflate skill ranks as a side effect; raising the cross-Facet cost would attack the flavour rather than the math.

**The miss, stated plainly:** DESIGN §6.3 projects Tier 3 and the first Major both landing at session 12 (100% primary-SP efficiency) to session 15 (80%). The BRIEF asked for Tier 3 at 12–15 ✓ and the first Major at 10–12 ✗.

**Why not hit the target:** pulling Major to session 10–12 requires `major_advancement_threshold: 2`, which fires the first Major at Facet level 2 (~session 8) — too cheap for something the PHB describes as "the culmination of a long arc of play," and it decouples Major from the Tier 3 moment. Landing Tier 3 and the first Major together at ~session 12–15 is the stronger dramatic beat.

**Status:** ✅ **Approved by Brain** (BRIEF §Q1). The s10–12 figure was **illustrative**, meaning "much sooner than 25–27" — it could not have been derived from observation, because per P7/F3 no character has ever reached a Major Advancement in code. Brain's ruling: a converging payoff is one milestone session instead of two diluted ones. **`session_skill_points` stays at 4** — rank inflation is a worse cost than a three-session slip on an illustrative number. The BRIEF's pacing target is amended to *"Tier 3 and first Major Advancement land together, roughly session 12–15 for a dedicated character."* **Task B2 is unblocked.**

---

### P6 — Archive Guardian's TR is 14, not 16 *(DESIGN §12 Q3)*

**Decision:** Correct it during the A2/A3 migration.

**Why:** `enemies/archive_guardian.fof` shows `offense(5) + durability(5) + armor(2) + special(phase→2 + immune Tier1→2) = 16`. The `special` term was counted twice under two labels. Under the re-keyed formula (`durability_value = resolve`) the Guardian computes to `5 + 5 + 2 + 2 = 14`.

**Note:** the migration map (`resolve := the old durability_value`) was chosen precisely so that every *other* published TR is preserved exactly — City Watch Sergeant stays 8, Veteran Soldier stays 10. The Guardian is the only enemy whose TR moves, and it moves because it was wrong, not because the formula changed. Encounter Budget arithmetic is therefore stable across the migration.

---

### P7 — Ledger row 9: cross-Facet levels count toward Major Advancement

**Decision:** `II.4:89` ("Facet level advances outside your Primary Facet ... do not count toward your Major Advancement threshold") is the stale sentence. The Major Advancement section at `II.4:207–209` — which counts them and works through an example of primary 2 + secondary 2 = 4 — is canonical.

**Why:** D3 ("any Facet level, primary or cross-trained, grants a Technique pick") is incoherent unless cross-trained Facet levels exist as a tracked quantity. The engine never tracked them at all: `Character._check_facet_level_threshold` (`character.py:215-216`) returns `0` for any non-primary skill, which means `total_facet_levels` cannot exceed 2 and `major_advancement_threshold: 4` has **never fired for any character, in any campaign, at any length.**

This is a ninth row on the D5 contradiction ledger, discovered during code survey and not present in the BRIEF.

---

### P8 — Enemy armor grants flat Resolve; the TR formula keeps its shape

**Decision:** Enemy armor adds Resolve (light +1, heavy +2) rather than downgrading Conditions. Enemies get no Condition downgrade at all.

**Why:** the numbers already agree. `armor_bonus` in the Threat Rating formula is 1 for light and 2 for heavy, so `TR = offense + resolve_base + armor_bonus + technique_bonus` stays structurally correct with `durability_value := resolve_base`, and the Resolve armor grants in play is numerically the armor bonus already printed on the stat block. One number, two uses, no reconciliation.

**Consequence:** armor means different things on the two sides of the screen — flat durability for enemies, Condition mitigation for PCs. That asymmetry is D1's premise ("Conditions replace HP" applies to player characters only), not a new one.

**Status:** ✅ **Approved by Brain** (BRIEF §Q4) as ethos-*consistent*, not ethos-tolerated. The game is already asymmetric at its root: PCs roll, enemies don't; PCs have stories, enemies have stat blocks. "Conditions replace HP" was always a statement about whose body the fiction cares about.

**Binding presentation requirement (task A11):** the PHB and MM1 present these as **two different tools, never as one rule with an exception**. On a stat block, "armor" is a Resolve bonus; on a character sheet, it is a downgrade budget; the app displays each automatically. One sentence in each place, **no cross-reference**.

### P9 — G1 gates fight *length and cost*, not win rate; a solo Boss is not balanced for solo-viability *(Planner resolution of the A8 escalation, 2026-07-10)*

**Decision:** G1's pass condition is revised from "median ≥ 3 exchanges **and PC win rate 45–55%**" to "median ≥ 3 exchanges + defeatable + zero house rules + snowball-doesn't-collapse-below-3 + a recorded **cost signal** (Sparks spent, Endurance remaining, PC-Broken incidence) proving the fight was *survivable but expensive*." The Guardian's base Resolve is retuned upward (≈8, confirm by sim) to clear the length floor; the BRIEF's "working range 2–6" note widens to the confirmed ceiling.

**Why:** A solo, single-target, by-the-book Boss cannot produce a 45–55% *party-loss* rate at any Resolve value — Resolve is durability, and three PCs' aggregate offense grinds through any pool while a lone attacker never sustains the two-same-type-Tier-2-hits cadence Broken requires (Worker A8's proof, `simulation_log.md` Series 7). The 45–55% band was **void-derived** — it traces to the Encounter Budget "Hard ≈ 50% win" multiplier that Brain's Q3 voided wholesale — and the §4.1 napkin check only ever engineered the exchange-length half. The reframe also *conforms to existing canon*: `enemies/archive_guardian.fof:44-47` already says a straight fight is "survivable but very expensive… solved laterally." The coin-flip expectation contradicted canon the user set in March.

**Rejected:** a structural "Bosses act twice / must carry a Technique" rule (Worker Options 1 & 3) — a rules change against the minimize-complexity pillar. Boss-encounter difficulty is produced at the encounter layer (Encounter Budget adds/TR — Gate G4) and via the Boss's authored Techniques and lateral weaknesses (all in its `.fof`, all stripped by the G1 sim — so G1 tests a Boss *below* its TR-14).

**Consequence / handoff to Brain (non-blocking):** the mechanical fix is Planner-owned and canon-grounded; the *player-facing framing* — "a Boss baseline is not solo-viable; difficulty comes from the encounter layer" — is an ethos statement that must land in MM1/III.3 prose (A11, after G1/G2). Flagged for Brain to bless at prose time; blocks nothing now.

**Confirmed by Worker, 2026-07-10:** Resolve 8 is not just adequate but the *smallest robust* value — a 7-vs-8 boundary check across 7 seeds at n=200 shows Resolve 7 flips between median 2 and 3 depending on seed, while Resolve 8 holds median exactly 3.0 in all 7. Canonical n=200/seed=1 run: 100% win rate, median 3.0, mean Sparks spent 6.2/9, mean PC-Broken 0.03. Guardian TR moves 14 → 17 (offense 5 + resolve 8 + armor 2 + techniques 2). A8 is closed; full data in `research/simulation_log.md` Series 7.

**Status:** ✅ Resolved by Planner. A8 unblocked (re-run G1 under DESIGN §5-bis).

### P10 — Encounter difficulty is actor-count-gated; the Recipe Table is calibrated, the TR-budget formula is demoted to a rough check *(Planner resolution of the A10/G4 escalation, 2026-07-10)*

**Decision:** The MM1 **Encounter Recipe Table** (simulation-validated enemy compositions per band) is the authoritative encounter-building tool. The raw `TR × difficulty_multiplier` Encounter Budget formula is **demoted to an explicitly-non-predictive rough sanity check** — non-predictive for 3+ Named/Boss rosters and for Mook swarms. `encounter.py`'s constants are made *honest* (docstrings say "rough heuristic, see Recipe Table"), **not** retuned to hit only the four validated recipes.

**Why:** Worker A10 (Gate G4) proved — five named baselines + a ~20-config sweep, 3 seeds each, `simulation_log.md` Series 9 — that difficulty is a steep, **actor-count-gated threshold** (1–2 Named/Boss actors trivial at any TR; 3–5 a cliff; per-enemy TR only a second-order modulator past that gate; Mook swarms never dangerous). The current formula is linear and separable in weighted-TR-sum, and *no* choice of `difficulty_multiplier` / `action_economy_multiplier` / `group_size_modifier` / `TIER_WEIGHTS` reproduces a threshold that runs orthogonal to weighted TR (1 Guardian TR-17 trivial, 3 Sergeants TR-8 a real fight, 4 Sergeants Deadly — backwards from any TR-sum ordering). This is G1's §5-bis doctrine ("a Boss baseline is not solo-viable; difficulty comes from the encounter layer") confirmed at scale and extended to Named NPCs and multi-enemy math.

**Rejected:** rebuilding `calculate_effective_tr` around actor count (Worker's Option 2). The win-rate→multiplier mapping the formula encodes was **already void** (Brain Q3), so a rebuild resurrects a void artifact; it would fit a smooth continuous model to a cliff function on only ~20 validated configs; and it is an architecture change disproportionate to A10's "retune two constants" scope. **Also rejected:** retuning the constants to hit only the four listed recipes — that reproduces the exact "looks authoritative, silently mis-predicts every other composition" trap the whole ruleset revision exists to stop.

**Deferred (non-blocking, Brain/product-scope):** whether the digital layer should eventually grade an *arbitrary* roster's difficulty (a real actor-count-primary predictive model, with the validation budget that requires) is a product-ambition question for Brain/the user later. It does **not** gate A10.

**Consequence / handoff to Brain (non-blocking):** the prose framing — "multi-enemy difficulty is driven by simultaneously-acting Named/Boss actor count, not total TR; the Recipe Table is the tool, the budget formula is a rough check" — is an *extension of the §5-bis ethos note already handed to Brain*, blessed at A11 prose time. No new Brain round-trip is required to unblock A10.

**Status:** ✅ Resolved by Planner. A10 unblocked under revised scope + Accept (DESIGN §5-ter, TASKS A10).

---

### P11 — Enemies do not react; Boss phases change runtime state, not armor *(Planner resolution of the A13/PT03 escalation, 2026-07-11)*

**Decision:** Four rulings on the PT03 boss stress test (full text: DESIGN §5-quater):
1. **A13 Accept revised.** Drop the void-derived "won at ≈Hard rates" bar (§5-bis: a lone Boss vs. a full party is not an even fight). Gate instead on median ≥ 3 exchanges + cost signal + **the phase change actually firing in a meaningful fraction of by-the-book fights**. Win rate is reported, not gated. Keep it a lone-boss run; do not re-scope to a boss-in-an-encounter.
2. **Enemies do not spend a resource to react.** A Strike depletes enemy Resolve by outcome, full stop — no enemy reaction. Follows directly from settled asymmetry ("NPCs don't roll; PCs react") + Q4 ("Resolve is durability, not an action-economy pool").
3. **Boss phases change runtime state.** Supported effects: raise incoming-tier/offense, grant/revoke a Special (`special_ignores_tier1`-style), second wind (add Resolve), MM-narrated targeting. **Forbidden:** "reduce own armor" / "trade defense for danger" — a no-op under D1's flat one-time armor bonus.
4. **Phase-crossing invariant:** every `resolve_current` mutation routes through `phase_crossed`.

**Why:** A13 ran clean on D1/D2 (Resolve, rider→Easy, per-scene armor, retired 0-End — zero house rules) but exposed the Boss phase subsystem as incoherent: (F3) the canonical "armor cracks" phase pattern is mechanically hollow because enemy armor is a flat starting-Resolve bonus (`combat.py:372`) with nothing to reduce mid-fight; (F5) III.3 never states an enemy's reaction cost, so the sim invented a Resolve-paid Parry (`combat_sim.py:483`) — and that single invented cost swings phase-fire rate from ~0% to 100%; (F8) that Parry is strictly self-defeating (spends the durability pool to defend the durability pool — a partial parry is a wash, a failed one a net loss); (F4) the raw parry decrement stepped over `phase_crossed`, so the flagship phase change fired in ~none of the by-the-book fights. All four verified against source before ruling.

**Rejected:** giving enemies a separate reaction pool (adds an action-economy subsystem the asymmetric model deliberately omits); keeping enemy Parry and fixing only F4 (leaves F8's self-own and F5's ambiguity live); retuning Boss Resolve now to fix the 2.9-exchange borderline (the shortfall is entangled with the buggy parry/phase model — retune only *after* A14, and only if median still lands < 3, using the sanctioned `facet.yaml` scalar per §5-bis).

**Consequence:** new Worker task **A14** (F5/F8/F4 engine+sim cleanup + F3 MM1 rewrite); A13 re-runs against the revised Accept once A14 closes. No Brain round-trip required — every ruling extends already-ratified doctrine (§5-bis, Q4); Brain blesses the phase *feel* at A14 prose time.

**Status:** ✅ Resolved by Planner. Return to Worker at A14, then A13 re-run.

---

### W1 — Adopt K1 (Aggressive reaction surcharge, first reaction of the exchange only) *(Worker, Gate G3, 2026-07-10)*

**Decision:** Adopt K1 as the canonical rule. `facet.yaml`'s `combat.postures.aggressive.reaction_cost_modifier_applies: first_reaction_only`; `app.game.combat.reaction_cost` gains an `is_first_reaction` parameter (default `True`, so callers that don't track per-exchange reaction counts — an enemy's Parry — see unchanged behaviour); `Character.reactions_this_exchange` / `PCState.reactions_this_exchange` track it, reset at end of exchange. PHB III.3 and MM5 updated in the same pass (Aggressive's table entries and prose now say "first reaction only," not "per reaction").

**Why:** Gate G3 passed both required conditions, robustly across 7 seeds (n=3000 each): K1 cuts the Aggressive PC's Broken rate 15.7%–18.7% (bar: ≥15%) while the Aggressive-vs-Measured win-rate delta (the offense-edge check) stayed within 0.1–0.6pp of baseline (bar: ±5pp) in every seed. Full methodology in `research/simulation_log.md` Series 8.

**Methodological caveat, disclosed to the user before adopting:** DESIGN only specified "Unarmored Endurance-3 PC, Aggressive vs Measured, n≥200" — enemy composition, fight length, and the win-rate definition were Worker judgment calls. A fight-to-conclusion design (the first one tried) showed **zero** difference between Aggressive and Measured (~84% Broken either way — attrition swamps posture economics over a long fight); a signal only appeared once the test was bounded to a 2-exchange "opening alpha-strike" window, matching the real-play concern (PT01, BRIEF D8) but a narrower scenario than "a fight." The user was shown this tradeoff directly (three options: adopt now / record-but-don't-adopt / redesign the gate first) and chose to adopt on the 7-seed robustness evidence.

**Consequence:** `combat_sim.py`'s shared `_enemy_attack` (used by every other Series, not just G3) now applies K1 live via `PCState.reactions_this_exchange` — this is now the canonical rule, not an experimental knob, so the C1 "simulator may never reimplement a rule" boundary requires every consumer to reflect it, not just the gate that discovered it. `run_g3_gate`'s baseline/K1 comparison is retained as a historical record (not deleted, per this project's established practice) — its `k1_enabled=False` branch reproduces the pre-adoption rule by forcing `is_first_reaction=True` unconditionally through the *same*, now-canonical function, rather than carrying a second copy of the old rule.

**Status:** ✅ Adopted. A9 closed.

---

### P12 — The D6 acceptance instrument is invalid; D6 is not revisited; the sim's spend policy becomes selectable *(Planner resolution of the WD8/PT04 escalation, 2026-07-11)*

**Decision:** **D6 stands unchanged.** The PT04 result (mean 1.51 Sparks spent/player, n=1,400) is **void as evidence** — it measures the harness, not the Spark cadence. WD8's Accept is not "not met," it is **unmeasured**. WD1–WD7 land; WD8 is voided (banner, not deleted) and reopened as **WD8-R** behind two instrument-repair tasks: **WD9** (recalibrate the PT04 rosters to the P10 Recipe Table) and **WD10** (make the simulator's Spark spend policy selectable, default-preserving).

**Why:** three independent defects, any one of which alone voids the number. (1) **The roster is stale** — `scenario.md` builds all three encounters from the `TR × multiplier` arithmetic that **P10 demoted as non-predictive**, and against the calibrated Recipe Table its "Standard" is Mook-only (Series 9: mean PCs Broken 0.00 through 30 Mooks) and its "coin-flip Hard" climax is a 1-Named roster (Series 9: 1–2 Named/Boss of *any* TR are trivial). The 100% win rate is not an anomaly — it is what Series 9 predicts. A resource-tax session that levies no tax cannot measure a resource tax. (2) **The spend policy is tautological as an instrument** — D6 is a *behavioural* hypothesis ("a richer earning cadence loosens hoarding"); a hardcoded heuristic with no model of hoarding or scarcity can only hand back its own rule. (3) **The harness measures the wrong domain** — `combat_sim` spends Sparks only inside `resolve_strike`, but Sparks are spendable on *any* roll in play, so the metric is a strict subset of what D6's Accept names.

**The real finding:** DESIGN §5 (line 206) already required PT04 to be a **playtest under data hygiene** — "real server rolls, per-player dice, reconciled modifier columns." WD8 was executed as a **1,400-run Monte Carlo**, which touches no server and has no players. The task was *specified* as a playtest and *performed* as a simulation. That substitution — not the 1.51 — is what this escalation actually surfaced. The task text ("Run with the new Spark cadence…") was underspecified about *how*, in a workstream where every neighbouring task is code: **a Planner defect, corrected in WD8-R.**

**Rejected:** *Revisiting D6 on this data* — nothing about D6 was measured; revising a rule against a broken instrument is how a ruleset acquires superstitions. *Retuning `should_spend_spark` in place* (Worker's Option 1 as posed) — every canonical PC starts `sparks=3` and spent Sparks add dice to Strikes, so they move win rates; editing the policy in place silently re-baselines every recorded G0–G4, A-series and Series-9 number. **This project has already been burned by exactly this once** (A14: the F5 fix invalidated the entire Series-9 recipe corpus). Hence WD10's default-preserving, bit-reproducibility-tested design. *Deleting the run* — voided corpora are kept with a banner (Series 9 precedent). *Widening WD8's scope in place* — the Worker was right to stop at its file boundary; that is the escalation protocol working.

**Amended Accept for D6:** the **≥ 2 Sparks spent per player** bar stands, re-scoped — measured **over a session, across all rolls (not only Strikes), from a real server roll log**. The Monte Carlo may report a combat-only **floor** alongside it, labelled as such, and is never the deciding number.

**Status:** ✅ Resolved by Planner. WD1–WD7 land. **Return to Worker at WD9 → WD10 → WD8-R** (DESIGN §8-bis, TASKS WS-D). No Brain round-trip required — D6 is untouched; this ruling only repairs the instrument that was supposed to test it.

---

### R1 — Two canonical combat rules never reached the live engine; both wired through `combat.py` *(PR #5 review, 2026-07-11)*

**Decision:** Fix both, then merge. (1) The **Staggered −1 offensive penalty** becomes machine-readable (`facet.yaml` `combat.conditions.tier2.staggered.offense_modifier: -1`, new `CombatConditionDef.offense_modifier` field) and is applied through a new shared `combat.offense_modifier(posture, conditions, ruleset)` that **both** `_handle_strike` and `resolve_strike` call. (2) **Armor/reaction non-stacking** (PHB III.3) becomes a shared rule, `combat.resolve_incoming_condition(...)`, and the `apply_condition` WebSocket message gains an optional `reaction_downgraded` flag so the engine — not the MM — applies the single greater reduction. Both simulator enemy-attack paths and the live `_handle_apply_condition` now route through it.

**Why:** both rules were canon in the PHB *and* implemented in the simulator, but **never fired at a real table.** The Staggered penalty lived as a literal inside `combat.resolve_strike`, and `resolve_strike` **has no production caller** — `_handle_strike` re-derives the strike inline via `engine.resolve_roll`. So the simulator penalised a Staggered attacker and the live engine did not. Non-stacking was worse than absent: `_handle_apply_condition` received only `{player_name, condition}` and so had no way to know a reaction had already downgraded the hit — it always spent an armor charge, meaning a partial Parry in light armor against a Tier 2 was **negated entirely** (PHB says Tier 1 lands) *and* burned a charge from the D2 budget that is the whole reason an armored PC stays breakable. This is precisely the C1 failure mode ("two implementations that silently diverged") that the WS-A0 extraction existed to end — the extraction moved the rules but left the live strike path outside them.

**Interpretive call, flagged for the user:** when a partial reaction has already applied the greater (equal) reduction, the armor charge is **not** consumed. The PHB fixes the resulting *tier* ("apply the greater reduction only") but is **silent on whether the charge is spent**. Not spending it is the reading consistent with armor being "a finite number of incoming Conditions it can soften" — a charge that softens nothing is not spent — and it is the one that preserves the D2 budget's intended lifetime. **PHB III.3 does not yet say this in prose; it should.**

**Consequence — the calibration corpus is untouched.** Re-running `--series all --seed 42 -n 200` before and after is **byte-identical**: the non-stacking *tier* outcome was already correct in the simulator (`min(1, 1) == 1`), only the budget accounting was wrong, and no recorded series runs long enough for an armored PC to exhaust the budget differently. Gate G1/G3, Series 7–9, Boss Resolve 8 and the encounter multipliers all stand as recorded. The behaviour that changes is **live play**, which now matches the model the corpus was calibrated against instead of diverging from it.

**Rejected:** *Applying the Staggered penalty inline in `_handle_strike`* — that is a third copy of the rule, the exact thing C1 forbids. *Making the MM pre-downgrade the condition before sending it* — the MM cannot see the armor budget, and it puts a rule in a human's head instead of the ruleset.

**Still open:** `resolve_strike`/`resolve_reaction` remain without a production caller (the live strike is split across two player/MM actions; LOG WS-A0 judgment call #3). The offense modifier is now shared, so the divergence that mattered is closed, but the asymmetry itself is not — new rules placed inside `resolve_strike` will still reach the simulator and not the table. There is also **no MM UI for applying conditions to a PC**; `reaction_downgraded` is wired server-side and has no client control yet.

**Status:** ✅ Fixed. 964 tests pass (+24). Sim corpus unchanged.

---

## Production Apparatus (2026-07-12)

Planner-tier calls on `docs/DESIGN_production_apparatus.md` (editorial review §D).
None is a rules change; all are structural. Owner sign-off pending.

### P13 — The glossary and index are *derived* artifacts: generate the index, test both

**Decision:** `Index.md` is emitted by `software/tools/build_index.py` and guarded by an
up-to-date test (regeneration must produce no diff — the lockfile pattern). The glossary is
hand-written but bound by a test that every entry's chapter pointer resolves and the target
contains the term. Both ship with the machinery that keeps them true.

**Why:** an index is a pure function of the finished text and a glossary is, by this project's
own law, a quick reference — "a compression of canonical body text, never a new rule." Both go
stale the moment a chapter moves, and a stale index is *worse than no index*: it misdirects
with full confidence. This repo has already paid once for two copies of a rule drifting apart
(the `combat.py` extraction, P1/C1). Hand-maintaining derived artifacts in a ruleset that is
still moving is the same bet a second time.

**Rejected:** *hand-written index* — cheaper today, rots by the next content branch, and nothing
would catch it. *No index* — the review is right that the cross-references are one-directional;
for a digital-first book the term→section map is the whole navigation layer.

### P14 — Skill text has four copies, not three; the fix nominates two homes and binds them

**Decision:** prose home = II.6's Skill List; data home = `facet.yaml`'s per-skill `description`.
The three Facet chapters drop descriptions entirely and carry name + attribute + a pointer to
II.6. A test asserts the two surviving copies agree.

**Why:** the review's §D5 found three prose copies and prescribed "make II.6 canonical." It
missed the fourth — `facet.yaml:150+` carries a `description` per skill, in the file `CLAUDE.md`
names the single source of truth for mechanics. You cannot collapse to one home without either
stripping data the engine may want or making a doc the authority over `facet.yaml`. So: two
homes, one for prose and one for data, and a test in place of a promise. Four uncoupled copies
become two coupled ones.

**Also found:** II.6:69 and II.6:85 point at II.4b/II.4c for "full descriptions" that do not
exist there — those chapters carry a *shorter* table whose text is byte-identical to II.6's own.
The pointer sends a reader to a lesser copy of what they are already reading. PA-3 reverses it.

### P15 — Write the cross-reference resolver *before* the renumber

**Decision:** PA-1 (a test that every `Chapter X.Y` citation in both books resolves to a real
file) lands before PA-2 (the II.4 → II.4 + II.4a split). It passes on today's text; it is what
makes the renumber safe.

**Why:** renumbering a book by hand and hoping you caught all 26 citations is how a book ships
with dangling references. TDD applied to prose: the invariant exists before the change that
could break it. This turns PA-2 from a careful error-prone task into a mechanical one.

### P16 — Standardize roll markers on `→`, not `>`

**Decision:** roll resolutions use `→` in both books. `>` is reserved for advice callouts.

**Why:** the review framed this as an arbitrary consistency choice. It is not quite: the MM
manual already uses `>` for callout boxes (MM2:42, :70, :165), so `>` there means *two* things
and a reader cannot tell a roll from a sidebar by its marker. `→` is already the PHB's marker
and is unambiguous. Standardizing the other way would deepen the collision.

### P17 — Recommend growing III.2, not folding it *(escalated to Brain — Q1)*

**Planner recommendation, not a ruling.** III.2 is 46 lines and will look vestigial in print,
but both fold-targets are wrong. Threat Clocks exist *because* hazards are not combat — moving
them into III.3 undoes the chapter's own argument. And the death rules ("Broken never kills
you"; the player, never the MM, chooses the scar or the heroic death) are among the strongest
design statements in the book; folding them into a combat chapter buries them and implies death
is a combat outcome, which is precisely what they deny. Grow it with the two worked examples it
lacks. That is a vignette in the recurring cast's voice — Brain/Fable's call and Fable's pen.

### P18 — The index spec assumes digital-first *(escalated to Brain — Q2)*

If a physical print run is actually planned, a page-number index cannot be generated from
markdown and must come from the layout tool instead. PA-10 as specified would be the wrong
artifact. Everything upstream of it is unaffected either way. **Confirm before PA-10 starts.**

### B1 — III.2 grows; it does not fold *(Brain ruling on Q1, 2026-07-12 — resolves P17, unblocks PA-8)*

**Ruling:** grow. The Planner's analysis is correct and is adopted as written: both fold-targets
are self-defeating. Threat Clocks are the book's statement that hazards are not combat — filing
them under Combat erases the statement. And the death rules are the strongest promise the book
makes ("Broken never kills you"; the player, never the MM, chooses the ending). A promise about
how death works does not belong inside the chapter about how fighting works; a reader skimming
for "what happens when I die" must not have to wade through Strike outcomes to find it.

One consideration the Planner did not raise, which settles it independently: III.2 is the only
rules chapter a *novice MM* leans on harder than players do — clocks and recovery are MM-facing
machinery. Folding it into III.3 makes the MM's simplest tool look like a combat subsystem, which
is exactly the misreading MM1's hazard guidance exists to prevent. Short is not vestigial;
III.1 is short too, and nobody proposes folding the resolution system.

**Scope of the growth:** the two worked examples the chapter lacks (a Threat Clock filling; the
scar-or-heroic-death choice), In Play vignettes in the recurring cast's voice. No rules text
changes. Executed by Fable in the same pass as this ruling.

### B2 — Digital-first is confirmed; PA-10's generated index is the right artifact *(Brain ruling on Q2, 2026-07-12 — resolves P18, unblocks PA-10)*

**Ruling:** there is no print milestone. Digital-first is not an assumption this design made —
it is the project's founding constraint (CLAUDE.md, pillar 2; the Introduction's own philosophy
section), and no roadmap file, TODO, or handoff anywhere in the repo schedules a print run. The
review's "print/PDF milestone" phrasing imported an assumption from traditional publishing; it
has no referent here. PA-10 as specified (term → linked-section map, generated by
`build_index.py`, guarded by INV-4) is the correct artifact and may proceed once PA-9 lands.

**Reversal condition, recorded so nobody re-litigates this from scratch:** if the owner ever
schedules a physical print run, that milestone creates a *new* task — a page-number index
emitted by the layout tool — and does not modify PA-10. The linked term index remains the
digital navigation layer regardless. Nothing upstream is affected either way.

### B3 — The sheet gets a name line; II.1's canonical description grows one sentence *(Brain ruling on the PA-5 escalation, 2026-07-12)*

**Question (Worker, PA-5 log):** II.1's six-section sheet description names no Character Name or
Player Name field, and PA-5's rule was "no field II.1 does not name." The Worker correctly
shipped a nameless sheet and flagged it rather than inventing a field.

**Ruling:** add the name line — by amending the canonical text first, then the sheet, in that
order. The engine's `Character` model *requires* both fields (`name` and `player_name` are
non-optional, `character.py:69-70`); INV-2's own philosophy cuts both ways — a sheet that lets a
player record what the engine cannot store lies about the game, and a sheet with no home for
what the engine demands is equally a lie. The defect was never in the sheet; it was in II.1's
description, which specified the six sections and forgot the header every one of those sections
hangs off of.

**Execution:** II.1 gains one sentence naming the sheet's header (character name + player name)
above the six-section table — a header, not a seventh section, so PA-5's section count stands.
The sheet gains the matching header block; INV-2's mapping gains `Character Name → name` and
`Player Name → player_name`. Fable-executed with this ruling.

---

## Ascendant Domain — engine support (issue #8, PR #7 review, 2026-07-12)

Full design: `docs/DESIGN_ascendant_domain.md`. PR #7 added the Ascendant Domain Tier 3
Technique to the PHB, the Glossary, and `facet.yaml`, but the engine honored none of its
three clauses. The prose was right; the software never caught up — the exact failure the
Software-PHB Sync law in CLAUDE.md exists to prevent.

### D-A1 — The domain catalog is data, transcribed from the appendix

`facet.yaml`'s `magic:` section had **no domain catalog at all**, so `get_domain()` returned
`None` for every domain and the engine silently substituted a synthetic `type: "standard"`.
Every prismatic domain therefore rolled the Standard table. The 21 domains, their types, and
their prismatic status are fully specified in `Appendix_Magic_Domains.md`, and `MagicDomainDef`
was already purpose-built to hold them (`requires_tier3` is even documented for exactly this) —
so populating `soul_domains` / `mind_domains` is **transcription of existing canon, not
invention**, and needed no Brain ruling. Tradition follows from the Facet (Mind → `scholarly`,
Soul → `intuitive`, per II.4b/II.4c).

Guarded by **INV-7**: the appendix and `facet.yaml` must agree on the domain set and every
domain's type. A domain whose type differs between them rolls one difficulty at the table and
another in the engine.

### D-A2 — `ascendant_domain` is its own field, not a reuse of `secondary_magic_domain`

The one-step-harder penalty is a property of the *acquisition route*, not of the domain. Second
Domain costs +1 difficulty step; Ascendant Domain pays with the Broad table instead and takes no
step penalty. Reusing `secondary_magic_domain` would have leaked Second Domain's tax onto every
Ascendant cast. A field per route is the honest model.

**Rejected:** a general `domains: list[str]` refactor — it touches persistence, the API, the web
app, and the `.fof` spec, for no gain this change can use. Reconsider if a third route appears.

### D-A4 — The Broad "ceiling" was not a ceiling

`engine.py` ended `resolve_magic_roll` with `if domain_def.type == "broad": difficulty_label =
"Very Hard"`, labelled as ceiling enforcement. It enforced nothing: Very Hard is already the top
of the ladder and `_step_difficulty_harder` saturates there, while `push_scope` is refused
outright for Broad domains. What the line actually did was *raise* a Minor-scope Broad cast from
its canonical Hard to Very Hard. Deleted. This was dormant only because no domain had ever
resolved to `broad` — D-A1 would have made it live.

### D-A6 — Second Domain's choice now reaches `secondary_magic_domain`

Nothing outside `.fof` loading had ever written that field, so the penalty it gates could only
fire for a hand-authored character. Same class of bug as the Ascendant overwrite, same code
path, fixed alongside it — which is what makes the two Tier 3 routes symmetric.

### D-A7 — Cross-Facet Tier 1 grants a second domain, untaxed *(owner ruling, 2026-07-12)*

**Question:** a Mind/Soul mage who cross-trains into the *other* Facet's Tier 1 Technique gains a
domain from that Facet's list. II.3 permits cross-Facet characters to take these Techniques, but
its worked example is a *Body* character with no domain — it never says what happens when the
taker already practises one. The engine silently overwrote the original.

**Ruling:** they hold both, each at its own normal difficulty, neither taxed for the other. At most
one domain per Facet by this route. Written into II.3.

**Accepted consequence, recorded so nobody rediscovers it as a bug:** this makes **Second Domain**
(Soul Communion Tier 3, permanently one difficulty step harder) strictly worse than a Tier 1
cross-Facet pick for any character willing to pay the cross-Facet advancement rate. Second Domain's
value needs a second look — tracked separately, not silently patched here.

### D-A8 — One prismatic domain per character *(owner ruling, 2026-07-12)*

A character who reaches Tier 3 in two Facet trees could take Ascendant Domain twice; the second
prismatic silently overwrote the first. Ruled: the second is **refused**. A character masters one
prismatic territory, however many trees they climb. `ascendant_domain` stays a single field.

### Domain slots, after D-A7 and D-A8

One field per acquisition route, because the route is what sets the price:

| Field | Route | Cost |
|---|---|---|
| `magic_domain` | Background origin, formalized by that Facet's Tier 1 Technique | none |
| `cross_facet_domain` | The *other* Facet's Tier 1 Technique | cross-Facet advancement rate |
| `secondary_magic_domain` | Second Domain (Soul Communion, Tier 3) | one difficulty step, permanently |
| `ascendant_domain` | Ascendant Domain (Tier 3) — prismatic, max one | the Broad table |

Re-selecting the domain a Background already granted is *formalization*, not a duplicate — the
Tier 1 Technique unlocks full scope on a domain the character already has (II.3/II.5). That case
is exempt from the duplicate check; everything else is refused rather than overwritten.

### D-A9 — Mind gets a Second Domain; the +1 step stays *(owner rulings, issue #9, 2026-07-12)*

**Correction first.** Issue #9 was filed claiming Second Domain is *strictly dominated* by the
untaxed cross-Facet route of D-A7. That was wrong, and the error was ignoring which attribute each
route rolls. Soul domains are `intuitive` (roll **Spirit**); Mind domains are `scholarly` (roll
**Knowledge**). A Soul mage cross-training into Mind rolls their off-attribute, and that penalty
roughly cancels Second Domain's difficulty tax. For a typical Soul mage (Spirit 3 → +1,
Knowledge 1 → −1), a Standard domain at Minor scope:

| Route | Attribute | Difficulty | Net |
|---|---|---|---|
| Second Domain (same Facet, +1 step) | Spirit +1 | Hard (−1) | **0** |
| Cross-Facet Tier 1 (other Facet, untaxed) | Knowledge −1 | Standard (0) | **−1** |

Second Domain rolls one better and costs one more Technique pick. A real trade, not a dead option.
It is dominated only for a mage who *invested in the off-Facet attribute* — which reads as a
legitimate build payoff, not a flaw.

**Ruling 1: the +1 difficulty step stays.** No rules change. The routes are near-balanced and the
tax is doing real work.

**Ruling 2: Mind gets a Second Domain.** The genuine defect the corrected math surfaced was an
*asymmetry*, not an imbalance: Second Domain existed only in Soul's Communion branch. A Soul mage
could deepen within Soul or branch into Mind; **a Mind mage could not deepen within Mind at all**,
and their only second-domain route — cross-training into Soul — rolled Spirit, their own
off-attribute. One Facet had two routes; the other had one, and it was the worse-rolling one.

`second_domain_mind` now sits in Archive at Tier 3 (prerequisite `cross_reference`), mirroring
Soul's Communion exactly: a second *standard* Mind domain, rolling Knowledge, one difficulty step
harder.

**One Second Domain per character.** Both trees now offer the Technique, so a cross-trained mage can
reach two Tier 3 gates. The second is **refused**, not silently written over the first — the same
refuse-don't-overwrite rule as the prismatic cap (D-A8), and `secondary_magic_domain` stays a single
field. Stated in II.4b, II.4c, and the Glossary.

## Completeness Audit Remediation — Wave 3 (2026-07-31)

Two findings ruled as-designed rather than fixed, per `docs/BRIEF_audit_remediation.md`'s
Non-goal boundary (no new Technique content, no Background skill-grant changes) and the task's
explicit instruction to record rather than patch. Both are sign-off items — the user may veto
either, which escalates to Brain per the standing D12 veto.

### cre-M7 — Communion Tier 3's non-magic pick count, accepted as-is

**Finding:** Soul's Communion branch offers one fewer non-magic Tier 3 pick than Mind's Archive
branch. Archive Tier 3 has two non-magic Techniques (The Knowledge That Saves, Deep Archive)
*plus* the two magic-extension Techniques (Second Domain, Ascendant Domain) — four total. Communion
Tier 3 has one non-magic Technique (Hold the Line) plus the same two magic-extension Techniques
(Second Domain, Ascendant Domain) — three total.

**Alternative rejected:** Author a fourth Communion Tier 3 Technique to match Archive's non-magic
count. Rejected — authoring new Technique content is outside this cycle's Non-goals (mechanical
correctness and canon-consistency fixes, not new content).

**Ruling: accepted as-is.** The asymmetry is real at the *non-magic* pick count, but both trees
offer the same Tier 3 pick count *overall* once the shared magic-extension Techniques are counted
— a character in either branch who wants a third Technique has exactly as many Tier 3 doors open.
No fix needed to reach parity; the trees were never meant to mirror each other pick-for-pick
outside that shared pair.

### rul-L5 — No pre-built Background grants Survival, accepted as-is

**Finding:** Survival (Mind) is one of the 15 skills but no pre-built Background (II.5) grants it
as a Starting or Secondary Skill.

**Alternative rejected:** Change an existing pre-built Background's skill grant to Survival.
Rejected — this is a content change with real knock-on cost: it would touch the Background's PHB
entry, `facet.yaml`, any test asserting that Background's current grant, and the pre-generated
Quick Start characters that reference it. A one-line "fix" is not actually one line once every
consumer is accounted for, and the Non-goal boundary (no content changes this cycle) applies here
too.

**Ruling: accepted as-is.** The custom Background path (II.5:83 — five steps, choose any skill
from your Primary Facet) already covers a character who wants Survival from the start. No pre-built
Background is required to reach it.

## Completeness Audit Remediation — Wave 4 (2026-07-31)

### sync-L5 — `second_domain` / `second_domain_mind` id asymmetry, accepted as-is

**Finding:** The Soul Communion Tier 3 "Second Domain" Technique uses id `second_domain`, while
the Mind Archive Tier 3 equivalent uses id `second_domain_mind` — an inconsistent naming scheme
(one is bare, the other is facet-suffixed) for what is otherwise the same Technique concept.

**Alternative rejected:** Rename `second_domain` → `second_domain_soul` (or `second_domain_mind`
→ `second_domain`) for symmetry. Rejected per the task's own instruction: both ids are directly
referenced by id string in `tests/test_ascendant_domain.py` and `tests/test_character.py` — over
15 call sites between them (`select_technique("second_domain", ...)`,
`select_technique("second_domain_mind", ...)`, plus assertions on `char.techniques`). A rename
is not a one-line id swap; it is a mechanical find-and-replace across two test files with no
behavioral upside, since Technique ids are looked up per-branch and never collide today.

**Ruling: accepted as-is.** The asymmetric naming is cosmetic, not functional — both Techniques
resolve correctly within their own Facet tree. No fix needed this cycle.

---

### B4 — Technique difficulty composes; the app applies mechanically-scoped steps automatically *(Brain ruling on the style-audit escalation, 2026-08-02; user ruling on the UX question, same day)*

**Source:** `docs/BRIEF_technique_difficulty.md`, escalated from `docs/LOG_style_audit.md`
after the `Normal:` pass found three baselines that did not exist.

**Decision — three rulings and one UX call:**

1. **Q1. Technique difficulty steps compose with the MM's situational call**, in a
   fixed order: the MM declares the situational label per III.1, then any
   character-side "one step easier" effect applies to that label, then the
   four-rung ladder clamps. **Guardrail:** character-side steps never stack with
   each other — at most one per roll, whatever its source.
2. **Q2. The Second Domain penalty rides the grant route, not the domain count.**
   Ascendant Domain's prismatic territory prices off the Broad table alone. The
   Second Domain penalty is one step harder *than normal for that domain*, not
   than the primary domain.
3. **Q3. *The Final Blow* is a licensed override, not a rider.** III.3's "riders
   never defeat" governs rider Conditions and stays verbatim. The removal works on
   any target including Bosses, and is implemented as a **defeat event** through
   the canonical path — never a raw `resolve_current` write (P11 invariant).
4. **UX. Mechanically-scoped Technique steps auto-apply.** Where the trigger is
   data the app already holds — *Weapon Mastery*'s weapon type, *Acclimated*'s
   hardship type, *Field of Mastery*'s field, *Steady Hand*'s Finesse rolls — the
   server applies the step without asking, and the roll banner shows both moves
   ("Hard (MM) → Standard (Weapon Mastery)"). Fiction-scoped Techniques remain a
   player toggle, because their trigger is a judgement call and no data the app
   holds can settle it. **Only *The Uncanny Angle* ships as a toggle.**
   *Pressure Point* was deferred entirely — it is party-wide scene state, not
   roll-time metadata, and needs a store the app does not have (DESIGN §2.5,
   `docs/TODO.md` T7). Five Techniques carry a step, not six.

   Two Techniques the book scopes to one skill — *Acclimated* ("Endurance rolls
   against your chosen hardship") and *Field of Mastery* ("Lore rolls that fall
   within your chosen field") — carry a `requires_skill` conjunct. Without it the
   engine implemented a wider rule than the printed one; caught in review, fixed
   before merge.

**Why:** the full argument is in the BRIEF. The load-bearing points:

- Q1 was **already ruled in print** and never stated as a rule: III.3:513's play
  example reads "Standard difficulty, but Weapon Mastery makes this one step
  easier, so Easy" — the Technique applied *after* the base was set. The ruling
  ratifies existing text rather than choosing against it. The non-stacking
  guardrail is the exact shape of two guardrails already in canon (III.3:175,
  III.3:410), so it costs no new concept.
- Q2 ratifies working, tested code (`character.py:406–410`, `engine.py:330–338`),
  which keeps the two grant routes apart *because the routes cost differently*.
  The alternative prices a prismatic cantrip like the hardest acts in the game.
- Q3's alternative makes a once-per-session Tier 3 capstone do nothing a
  successful Strike does not already do.
- Auto-apply is the bookkeeping-absorption pillar doing its job. A step the app
  can derive from `technique_choices` is a step no human should be asked to
  remember mid-exchange, and the banner keeps it visible rather than silent.

**Rejected:**

- *Q1, inside the budget* — makes Tier 1 signatures evaporate whenever the MM
  applies any hardship, so a Technique's value would depend on the difficulty call.
- *Q1, free composition* — arithmetic at the table, and it compounds with every
  Facet shipped. The guardrail caps total drift at one rung forever.
- *Q3, Boss carve-out* — requires the MM to consult a hidden number and announce a
  diminished result at the most cinematic beat in the game.
- *One-tap confirm for every step* — rejected by the user in favour of auto-apply.
  The confirm survives only where the trigger is genuinely fictional.

**Latent defect fixed in the same ruling:** *Second Domain* reads "one difficulty
step harder **than your primary domain**." Read literally, a Focused-primary
caster's second standard domain prices at Focused-plus-one — which *is* the
standard table, silently deleting the penalty. Five surfaces re-anchor to "harder
than normal for that domain": II.4b, II.4c, `facet.yaml` ×2 roll-texts, MM5.

**Corpus:** intact for all three. `standard_party()` carries no Techniques
(`combat_sim.py:973–981`), so Series 7 and 9 stand as published. MM1 gains one
advisory sentence; no re-run gated.

**Status:** ✅ Resolved by Brain, UX resolved by the user. Planner has produced
`docs/DESIGN_technique_difficulty.md` and `docs/TASKS_technique_difficulty.md`.
Return to Worker at TD-1.

---

### B5 — The Strike's skill is a default, not a restriction *(ratified 2026-08-03, backfilled)*

**Decision:** III.3 names **Combat** for melee and unarmed Strikes and **Finesse**
for ranged ones as *defaults*, not restrictions. Where the fiction supports it, a
player may Strike with the skill that describes what they are doing, and where two
pairings both fit, the player chooses. The MM may name a different attribute where
the fiction clearly supports one.

**Why:** the engine has always accepted any attribute/skill pairing the client
sends (`_handle_strike`). The book said the skill *is* Combat or Finesse, which
read as a restriction the engine does not enforce — and which made a
Finesse-based unarmed character, exactly the monk-adjacent build Zulnut is,
unbuildable by the book while being buildable in the app.

Found by an agentic playtest on 2026-07-31
(`playtest/08_npc_variance/subagent_session/report.md`, finding F1) when a
monk-adjacent PC struck with Dexterity + Finesse, the engine allowed it, and the
book forbade it.

**Status:** ✅ Landed with the style-audit commit and pinned by **INV-8**
(`test_books_do_not_restrict_the_strike_pairing`), which fails if any book line
states the pairing without hedging.

**Backfilled.** This entry is written after the fact. The ruling was recorded in
the INV-8 test docstring and the playtest report but never in `DECISIONS.md`,
which is where a rules change belongs — a reviewer reading only the decision log
would have found a rules change with no ruling behind it. Recording the gap
rather than quietly closing it.

---

### B6 — The scene is a real boundary, and the engine gets one *(2026-08-04)*

**Decision:** add an MM-gated `scene_end` event. On it the engine resets every
character's armor downgrade budget and drops standing Final Blow offers.

*Scene-scoped Technique effects are named in the "Scope held deliberately narrow"
paragraph below and are **not** part of this decision — an earlier draft of this
sentence said they were, which contradicted the same entry three paragraphs
later. There is no scene-effect store yet; `docs/TODO.md` T7 still owns it.*

**Why — this started as T7 and turned up a live rules bug.** Three published rules
are scoped "per scene": armor's downgrade budget (III.3, IV.1), the *Once per
scene* frequency on fourteen Techniques, and *Pressure Point*'s party-wide step.
The engine had no scene boundary at all.

The consequence was not theoretical. `_handle_combat_start` initialises
`armor_downgrades_remaining` **only if it is `None`** — deliberately, so a second
fight inside one scene cannot top the budget back up. Nothing anywhere sets it
back to `None`. So the budget is initialised once per character, ever, and a rule
the PHB prints as refreshing every scene **never refreshes**. A character who
spends light armor's two charges in the first fight of a session plays the rest
of it in effectively no armor.

`tools/combat_sim.py:680` does reset the budget at the start of every simulated
fight, so the two implementations disagree in source.

**Corrected after review — the consequence claimed here was false.** An earlier
version of this entry said "the recipes in MM1 were calibrated against a party
whose armor refreshed; the app gave players one that never did", and escalated the
disagreement to "the exact divergence class that invalidated a research corpus".
Neither holds. **Every PC definition in `combat_sim.py` is `armor="none"`** —
`mordai_def`, `zahna_def`, `zulnut_def`, `drew_def`, all three `advanced_*` defs,
and `_g3_pc_def` — and `armor_budget()` returns 0 for anything that is not light
or heavy. Line 680 assigns 0 to a field already 0. **It has been a no-op in every
simulation ever run**, so no recorded number in `research/simulation_log.md` moves
in either direction.

The honest statement is close to the reverse: MM1's recipes have **no armored-PC
data behind them at all**, because the instrument that produced them has never
modelled an armored PC. The Recipe Table's repeated "fresh party" hedge is doing
more work than it looks like.

The residual divergence is real but declared: the app now resets per *scene*, the
simulator per *fight*, and `combat_sim.py:136-138` documents the
one-encounter-is-one-scene simplification in source. It becomes a live problem the
first time a simulated PC wears armor — recorded in `docs/TODO.md`.

**Bounding the bug's reach, also from review:** `Character.armor` is written in
exactly one place (`from_fof`) and set by no REST route, no WebSocket event, and
no UI control. A character created through the app has `armor = None` forever, so
only an uploaded `.fof` can produce an armored PC today. The bug is real and the
fix is right; the population currently able to hit it is small.

**Rejected:** resetting armor at `combat_start`. That is what the code used to do
and the `is None` guard was added on purpose — two fights in one scene must not
each hand out a fresh budget, because the budget is what makes armor a decision
rather than a number. The bug was never that the guard existed; it was that
nothing ever cleared the flag the guard reads.

**Rejected:** inferring scene end from `combat_end`. A scene is not a fight —
III.3's own armor text says a second fight can happen inside one scene, and plenty
of scenes contain no combat at all. Tying the two would re-introduce the bug the
`is None` guard prevents.

**Scope held deliberately narrow.** *Once per scene* Technique frequency stays
MM-tracked. Most such Techniques have no engine invocation path — they are
narrated, not clicked — so enforcing a counter would police the few that happen to
be wired and ignore the rest. The boundary now exists for whenever that changes.

**Status:** ✅ Decided and implemented. Closes the armor bug; unblocks
`docs/TODO.md` T7.

---

### B7 — A Technique's difficulty step applies on every roll the MM prices *(2026-08-04, resolves T13)*

**Decision:** `apply_character_difficulty_step` is called from every handler that
resolves a roll against an MM-declared difficulty label — Strike, generic roll,
reaction, **Support, Maneuver, and contested rolls**. Magic stays excluded.

**Why:** the printed text says *rolls*. *Weapon Mastery* eases "Rolls using your
chosen weapon type", not Strikes. Under the old three-call-site implementation
Mordai Struck with his sword at Standard and got Easy, then Maneuvered with the
same sword in the same exchange and stayed Standard — same Technique, same weapon,
two labels, and nothing on screen explaining the difference.

**Rejected: narrowing the printed text to "Strikes".** That is a rules change made
to accommodate an implementation gap, and it would quietly weaken a Tier 1
Technique that four other Techniques' scoping already depends on being read
plainly. Fixing the code is cheaper than editing the book, `facet.yaml`, and two
quick references to describe something smaller than what was designed.

**Magic remains excluded**, and this is not an oversight: a magical working's
difficulty comes from the Domain-Type × Scope table (II.3), not from a label the
MM declares. There is no MM call for a character-side step to compose *with*. If a
Technique is ever printed that eases magic, it needs its own rule, not this one.

**The guardrail is unchanged and is what makes widening safe:** at most one
character-side step per roll, whatever the source. Widening the call sites cannot
compound, because the cap is enforced inside the shared function rather than at
each call site.

**Status:** ✅ Decided and implemented. Closes `docs/TODO.md` T13.

---

### B8 — *Weapon Mastery* stays melee-shaped; ranged specialists are served by *Steady Hand* *(2026-08-04, resolves T8)*

**Decision:** no fifth option is added to *Weapon Mastery*. Its four choices
(blades, blunt, polearms, unarmed) stand.

**Why:** the apparent gap dissolves on inspection. *Weapon Mastery* is a **Might**
Technique, and Might is the Strength branch. Ranged weapons are Dexterity (IV.1),
ranged Strikes default to **Finesse** (III.3), and Finesse is the **Grace** branch
— which prints its own step-easier Tier 1 Technique, *Steady Hand*, triggering on
exactly that skill.

So an archer is not short a Technique. They take the Dexterity branch's step, in
the Dexterity branch, for the Dexterity weapon. Adding "bows" to a Strength
Technique would let a ranged specialist take their step from the branch their
build does not use, and would make Might the only branch easing every weapon in
the game.

**Rejected:** adding the option anyway "for completeness". Completeness across a
list is not a design goal; the branch structure is. The plumbing added in the B4
cycle will carry a fifth `weapon_type` the day the setting's author wants one, so
this stays a one-line change if the reading above is ever overruled.

**Consequence, enlarged after review.** The first attempt added only a pointer
sentence to II.4a — and review showed the premise did not hold *in the book*.
*Steady Hand*'s trigger is `skill_id == finesse`, so in the engine it does ease a
ranged Strike; but its printed text read "precision work under pressure (picking
locks, threading a needle, disabling a mechanism mid-crisis)", which covers no
such thing. A player reading the entry got "no" while the engine said "yes", and
the pointer sentence asserted the engine's answer without changing the entry.

So the entry was widened to say what it does — **Finesse rolls** are eased, with
the old examples kept as illustration — in II.4a and `facet.yaml` in the same
commit. That is a rules change, small and in the direction the engine already
went, and B8 depends on it: without it, T8 would have been closed on a premise
true only in code.

**Status:** ✅ Decided. Closes `docs/TODO.md` T8.

---

### B9 — The Bestiary is permanently setting-agnostic *(2026-08-04, resolves T6)*

**Decision:** no creature in the Bestiary is placed in Shattered Origin, now or
later. The book stays portable by design, and the **Adaptation** line on each
family entry is the mechanism by which an MM seats one in any setting — including
this project's own.

**Why:** the Bestiary is a *core* module, shipped alongside the PHB and MM Manual,
not a setting Facet. Its value is that any table can use it. Placing the creatures
would convert a core book into setting canon, oblige every future entry to
justify itself against Shattered Origin's history, and hand the project a
compatibility burden for no play benefit — an MM who wants chalk hounds on the
roads of Svara can put them there in one sentence today.

It also keeps the copyright and canon postures clean: every creature is original
to the project *and* owned by no setting, so nothing in the book can contradict
canon the author has not written yet.

**The one exception stands and is not a precedent:** the Archive Guardian was
already canon before the Bestiary existed, and appears as the Latchmen's Boss
expression because that is what it is.

**Status:** ✅ Decided. Closes `docs/TODO.md` T6. If the author later wants a
creature seated in Shattered Origin, that belongs in the Shattered Origin setting
Facet, which can name and adapt anything here without the Bestiary changing.

---

## Fun & Ease-of-Play Fixes — WS-3 (2026-08-08)

### D6 — The TR budget and action-economy multiplier tables are cut (K-5)

**Decision:** MM1's Encounter Budget section — Table MM1-5 (TR budget, Party
Strength × 1/2/3/4) and Table MM1-6 (action-economy multipliers ×0.75/×1.0/
×1.25/×1.5) — and MM5's compression of both are removed from the books. TR
itself, the TR minimums, the Recipe Table, and the actor-count rule stay.

**Why:** the budget was proven structurally non-predictive by simulation
(`research/simulation_log.md` Series 9): difficulty is gated by the **actor
count of Named/Boss enemies**, not by summed TR. Three TR-8 Named enemies
(24 total TR, "well above Deadly" by budget) are a ~96% party win; the same
roster becomes Standard only once a Mook is added. No set of multipliers can
reproduce the actor-count-gated curve — the earlier "~95/75/50/25%" win-rate
presentation was already withdrawn once, and the tables survived only behind
40 lines of caveats telling the reader not to use them. Tables outlive prose:
a table on the page gets used, whatever the paragraph above it says. The
Recipe Table already does the budget's job with measured numbers.

**Historical record (so the numbers are not lost):**

The cut budget: Skirmish = PS × 1, Standard = PS × 2, Hard = PS × 3,
Deadly = PS × 4, where Party Strength = sum of participating characters'
`career_advances`. The cut action-economy adjustment: single enemy × 0.75,
2–3 enemies × 1.0, 4–6 enemies × 1.25 (Mook-only swarms × 1.1),
7+ enemies × 1.5. Both were rough ordering aids for simple/solo rosters and
explicitly non-predictive for 3+ Named/Boss rosters and Mook swarms.

**Citation:** Series 9 (`research/simulation_log.md`) — Part C measured the
actor-count ladder; Part D re-pinned the recipe rosters after the A14 enemy-
Parry correction (Standard 3×Named+1 Mook 76.0%, Hard +2 Mooks 47.5%, Deadly
+3 Mooks 20.0% / 4×Named+1 Mook 20.0%, seed 1, n=200).

**Status:** ✅ Decided (DESIGN_fun_ease_fixes.md D6). Implemented by T3.6.

## Fun & Ease-of-Play Fixes — design decisions D1–D14 (2026-08-09)

Recorded from `docs/DESIGN_fun_ease_fixes.md` §8 on pipeline completion (Brain
tier; findings and evidence in `docs/RESEARCH_fun_ease_review.md`).

| # | Decision | Chosen over | Rationale |
|---|---|---|---|
| D1 | Sparks reset to 3 each session | carry-over / floor | Anti-hoarding lever; playtest-confirmed hoarding; unspent = wasted drives engagement |
| D2 | One-step cap unified across Techniques + Specialties + future sources | separate caps | Future-proofs the ladder; kills the read-carefully advantage |
| D3 | 7–9 = narration sequencing, no decline-offer | PbtA-style offer | 7–9 fires on ~46% of rolls; a decision point on the most common outcome taxes pace; "never a dead end" already guarantees motion. Revisit on playtest evidence |
| D4 | Rider menu vs enemies → single "Open" tag | keep menu + honesty note | 4 of 5 options mechanically null vs non-rolling enemies; fiction keeps variety at zero rules cost |
| D5 | Withdrawn fixed via uncontested-exchange escalation | recovery nerf / pressure conditionals | Scene rule, applied once by the MM, no per-character bookkeeping; converts the loop into a tempo trade |
| D6 | TR budget + multiplier tables cut to DECISIONS.md | keep with caveats | Proven structurally non-predictive; tables outlive prose; the Recipe Table already does the job |
| D7 | Casting adds the tradition's skill (Spirit→Attune, Knowledge→Lore) | attribute-only | Gives mages the fighter's +0→+4 arc; research names attribute-only's failure explicitly; rehabilitates the Prismatic ladder and Second Domain without touching tables. Wording stays attribute-keyed — no tradition proper nouns in the core PHB |
| D8 | Prismatic ladder numbers unchanged; ceiling sentence rewritten as reach-only | soften to Hard/Hard/VH | Skills-apply restores growth; identity kept; the "Sparks don't work here" misread killed |
| D9 | Second Domain penalty expires at next Facet level | permanent + label | Arc beats tax; permanent difficulty taxes on defining traits are the documented feel-bad shape |
| D10 | Bank ≤2 points + 1 training mark to an unused Primary-Facet skill | forfeit as-is | The banked-pool abuse cannot occur at 4/session; the forfeit's only output was its own example's feel-bad |
| D11 | Never Surprised → warning beat | absolute at a higher tier | Preserves the fantasy at full strength; returns a scene genre to the MM |
| D12 | Enemy blind posture reveal dropped; conduct triggers instead | keep ceremony | A ritual that never surprises is pure overhead; rule-driven stances are cheaper and more readable |
| D13 | "Endurance Pool" print qualifier, no identifier rename | full rename | A full rename churns code/data/YAML for the same table clarity; revisit on playtest evidence |
| D14 | Prismatic is the player-facing term | Broad | The evocative word wins the player-facing slot; Broad survives in one definitional II.3 sentence naming the data type key |

### D15 — The traditions get their setting names: Invocation and Thaumaturgy *(owner ruling, 2026-08-09)*

**Decision:** The two magical traditions of Shattered Origin are named at the
setting layer: **Invocation** is the intuitive tradition (Spirit, Soul-aligned,
casting adds Attune) and **Thaumaturgy** is the scholarly tradition (Knowledge,
Mind-aligned, casting adds Lore). These replace the displaced working names
Channeling and Resonance — "Resonance" is now a Soul *domain* and cannot be
reused as a tradition name.

**Scope:** D7 stands — the core PHB keeps its attribute-keyed wording and
introduces no tradition proper nouns. Invocation and Thaumaturgy live in the
setting layer (the Shattered Origin setting Facet, when written) and in
project-level descriptions.

**There is no third tradition** *(correction, 2026-08-09)*. This entry
originally closed by calling the Body tradition's name "the one open naming
question." That was wrong, and it inherited the error from a stale
open-questions list carrying a shortlist (Wildcraft / The Root / Bloodcraft /
The Waking) for a tradition the ruleset does not have. Verified: the Facet of
the Body has no domains, no domain-granting Technique, and no magic-granting
Background, and `magic.traditions` holds exactly the two entries above. A Body
character who wants magic cross-trains into the Mind or Soul Tier 1 Technique
at the standard cross-Facet cost (II.3, *Acquiring a Domain*). The question is
void, not open.

**Status:** ✅ Decided. Recorded in `research/magic_system_analysis.md` §6
naming note; README project description updated.

---

### D16 — A Facet is a category of archetypes, not an archetype: the primary Facet must not be exhaustible *(owner ruling, 2026-08-09)*

**Decision:** "Everyone masters their primary Facet" is wrong and is retired as a
design goal. Skill advancement must carry opportunity cost inside a single Facet,
so that two characters sharing a Facet end a campaign with different sheets.

**The argument (owner):** *"A lot of different classes fall under each Facet — a
ranger shouldn't be as good at hand-to-hand as a barbarian."* A Facet is a
*category* of archetypes, not an archetype. Body contains the brawler, the scout,
the duellist, the acrobat. Under the rules as written, every one of them arrives at
the identical sheet — Athletics, Combat, Stealth, Finesse and Endurance all at
Master — in roughly eleven sessions. The Facet therefore cannot express the
difference between the archetypes it contains, which is the one job a broad
category most needs to do.

**This is an identity problem before it is a pacing problem.** The measured rate
(one Facet level per 3.75 sessions; full primary mastery at ~11.25) is defensible
against the field — comparable to Savage Worlds' 20 Advances or Apocalypse World's
~12 improvements. What is *not* defensible is the shape: Facets is the only system
surveyed whose advancement track terminates in total completion. Call of Cthulhu 7e
asymptotes (improve only on a d100 roll *over* the current skill value), Apocalypse
World and Savage Worlds offer menus wider than the available picks, D&D 5e forks
exclusively. Evidence and sources: `docs/RESEARCH_advancement_benchmark.md`.

**Supersedes:** `DESIGN_v0.3_ruleset_revision.md` §6.2, which set
`facet_level_threshold: 5` specifically so all three Facet levels would fit inside
the 15-advance ceiling. That choice optimised for the Facet levels landing tidily
and did not weigh intra-Facet differentiation. The coincidence of "Facet level 3"
and "every skill at Master" was deliberate; it is now the defect.

**Known insufficient:** an escalating mark cost per rank tier *alone*. It delays
completion to roughly twenty sessions but the track still completes, so a long
campaign reconverges the ranger and the barbarian. Delivering this ruling needs a
genuine ceiling, with a cost curve underneath it rather than instead of it.

**Explicitly out of scope:** the Technique layer. Three picks from a tree of 18–20,
branch-gated so that reaching Tier 3 costs all three picks in one branch, is the
only genuine exclusive choice the game has today and is preserved intact.

**Also on the table, same root cause:** the cross-training incentive runs backwards
(`RESEARCH_advancement_benchmark.md` §4). A fourth Technique *from your own tree*
requires Facet level 4, which only cross-training reaches — so breadth is the sole
source of further depth, the inverse of the 5e/PF2e convention where breadth costs
depth. Whether to fix this in the same change is handed to Brain.

**Status:** ✅ Decided (whether). Brain holds the *how* —
`docs/BRIEF_advancement_differentiation.md`.

### D16a — The first Technique arriving early is the intent, not a side effect *(owner ruling, 2026-08-11)*

**Decision:** Facet level 1 landing sooner under D16 — a floor of 2.25 sessions
against v0.3's 3.75 — is accepted and intended. *"Facet lvl 1 makes sense to be
faster."*

**Why it was an open question.** D16 was adopted to answer "this seems way too
rapid," and level 1 is the one threshold that moved in the *faster* direction.
Everything else slowed: level 2 from 7.5 to 5 sessions of cheap advances but
then a longer climb, and level 3 from 11.25 to 9.5 (8.75 with a Background) at
the floor, with the realistic window running to 14. The escalating 3/5/8 curve
front-loads the cheap ranks and back-loads the expensive ones, so the opening
accelerates and the endgame lengthens.

**Why the acceleration is worth keeping.** The three advances that buy level 1
cost 3 marks each — they are reachable before a new player has finished working
out what their character is for, and the Technique is what turns the sheet from
arithmetic into a person. The pacing complaint that produced D16 was never about
the first Technique; it was about every character ending identical. The caps fix
that, and they fix it in the back half of the track where Expert and Master are
decided.

**Recorded in the books** so a future MM does not read it as a defect and slow it
down: MM3, *Through the Mirror — the first Technique is supposed to arrive
early*, which also names the correct lever for a longer campaign (stretch the
middle, not the opening).

**Status:** ✅ Decided. Still open from D16: the §4 cross-training inversion
(deferred with a playtest revisit trigger) and veteran pacing under the 2 SP
cross-Facet cost.


## Oraga Night as Starter Module, Lineages, Val'loh (2026-09-08)

Recorded from the Brain fun audit (`docs/RESEARCH_fun_audit_2026-09.md`) and the same-day scoping session. Briefs: `BRIEF_oraga_starter_module.md` (umbrella), `BRIEF_lineage.md`, `BRIEF_valloh_facet.md`, `BRIEF_oraga_rewrite.md`.

### D17 — Magic has no daily limit; it is balanced by per-roll cost, not by counting *(owner ruling, 2026-09-08)*

**Decision:** "Remove the spell complexity entirely; let magic users use magic freely, as is written." No spell slots, no uses per day, no mana, and no setting-level tempo rule for Val'loh's spellforms. The core's II.3 stands unchanged and every setting Facet inherits it.

**Why it holds against the field.** Games that count spells (D&D, 13th Age, Savage Worlds) need the count because a cast spell there is a guaranteed effect. Here nothing is guaranteed: scope sets difficulty (Focused: Easy/Standard/Hard; Standard and Prismatic worse), the 7–9 band costs something on roughly half of all castings and the 6− templates hurt, active opposition floors combat magic at Standard, a magical Strike depletes 2/1 Resolve exactly as steel does, pre-Technique casting is Minor only, and a Background caster spends their first Technique pick formalizing. Free-use magic balanced by consequence is the choice Fate, Forged in the Dark, and Ars Magica's spontaneous casting make; their communities do not report caster supremacy.

**Numbers at +2:** a fighter's Standard Strike is 42/42/17 (full/partial/fail); a Focused caster's Minor at Easy is 58/33/8; any caster in combat is 42/42/17. Casters do *small* things more reliably than fighters hit and do not hit better.

**Where the gap is:** versatility outside combat, not power. If a human playtest shows casters holding more spotlight than martials, the fix is on the martial side (audit R3 Strike riders, R5 Body signatures), never a limit on magic. MM2's adjudication guidance (name the 7–9 cost; judge scope honestly) is load-bearing and goes on every scene card.

**Status:** ⛔ **Superseded by D23** (owner, 2026-09-18). Kept for its reasoning, which D23 answers rather than discards: D17's own "where the gap is" paragraph named the problem D23 fixes.

### D18 — Lineage is a core creation step; a lineage Gift is a domain that formalizes free at the first Facet level *(owner rulings, 2026-09-08)*

**Decision:** Lineage becomes step 3 of seven (II.5; Backgrounds → II.6, Skills → II.7, renumbered). The core ships Human only. A gifted lineage's Gift is a domain (intuitive, Focused, Minor until formalized) that replaces the Background's secondary skill; one domain at creation from Lineage or Background, never both. **A lineage Gift formalizes at the character's first Facet level in any Facet and spends no Technique pick** ("blood is not study"). The tribes of Val'loh are human and are the first non-default lineages. Detail: `BRIEF_lineage.md`.

**Shipped (2026-09-09).** II.5 written; Backgrounds → II.6 and Skills → II.7; `lineages` merged by id with `LineageDefinition`; `lineage` / `gifted` / `domain_source` on the character, defaulted so every pre-existing `.fof` loads and round-trips unchanged; the one-domain rule enforced at creation; `_formalize_lineage_gift` fires on the first Facet level and records no pick; INV-16. The builder's picker hides itself when the ruleset holds only Human. `LOG_lineage.md` carries the renumber post-mortem — a `Chapter II.6`-shaped sweep silently repointed the Glossary's *Rank* entry from Skills to Backgrounds, and **no invariant in this repo can catch a reference that resolves to the wrong existing chapter.**

**Status:** ✅ Decided and shipped.

### D19 — Oraga Night scoping rulings *(owner, 2026-09-08)*

| Ruling | Decision |
|---|---|
| Val'loh has domains | Yes. "No domains / gifts are flair / nobody casts in a crisis" (prior model) retired. ~~Gifts are custom Focused domains~~ — **superseded by D24: a gift is the player's choice of an existing domain.** Spellforms are the scholarly tradition as written; crystal charges are one-use items. |
| The Bought hold the gate | Yes. The Bestiary's contract company, hired through an intermediary, set the diversion fires and hold the gatehouse from first bell to last, with a Second Clause about a woman in Thenya wool. New canon. |
| "Old coin" | Kept as a deliberate red herring pointing at Vell; the aftermath can untangle it, never confirm it. |
| The prelude | Cut. The module opens on the approach and the line, Movement I. |
| One world | Val'loh is a continent of Shattered Origin's world. No rename of the PHB example character: the Gambit's Zahna is never named player-side. |
| Written-word ban | Canon, with both carve-outs (formal invitations; private slates). |
| Krenn and Tyndi | In Facet data, MM-only, never player-facing in 3164. |
| Sequence | Audit R2/R3 are simmed and settled (`BRIEF_fun_second_act.md`) before the module's fights are tuned. |

**Status:** ✅ Decided.

### D20 — Open expires; a 10+ Strike chooses a rider; Cover was cut at the gate *(simulated and settled, 2026-09-08)*

**Source:** `docs/BRIEF_fun_second_act.md`, from the fun audit's §9 R2/R3/R7.
**Evidence:** `research/simulation_log.md` Series 12 Parts A, B, C.
**Problem:** every Named and Boss fight had one shape. The first 10+ hung Open on the enemy, Open came off only when the enemy forfeited its one attack to clear it, so in practice it never came off, and every later Strike from anyone was Easy. A solo Boss had a median of **two** exchanges, and its Resolve-2 phase fired in the exchange the fight ended in three runs out of four — a second act nobody played against.

**R2 — Open clears at the end of the exchange. ADOPTED.**
`combat.enemy_durability.open_clears: end_of_exchange`. Open expires with the Tier 1 Conditions; nothing is spent to end it; and an Open enemy **still acts**. Open becomes a window to crowd into rather than a switch that stays flipped.
Solo Guardian median 2 → **3**, mean 2.68, win rate still 100%, Sparks 5.87, party Endurance drawn further down. Every recipe row moved down and every one held its band within the acceptance's ±5pp: Standard 73.0–78.0%, Hard 38.0–45.0% (now at its floor rather than its middle), Deadly 17.5–26.5%.

> **The prescribed repair was tried and rejected.** The acceptance said to retune Named/Boss Resolve by −1 before touching anything else. At Resolve 2 a Named NPC dies to a single full-success Strike, so it stops having a second exchange at all, and every row overshot on the high side (Standard 88.5–97.0%, Hard 61.5–73.0%). **The Named tier has no −1 step** — MM1's 3–4 authoring band has no interior. Worth remembering the next time an acceptance assumes a one-point Resolve dial: a Boss at 8 has that room, a Named does not.

**R3 — a 10+ Strike chooses one rider. ADOPTED WITH TWO.**
`strike_riders: [open, position]`. A full success depletes 2 Resolve **and** chooses: **Open** (Easy to Strike for everyone until the end of the exchange) or **Position** (the next roll against the target is Easy, this exchange or next). Both are Easy tags and do not stack; neither defeats; the choice is made after the roll, which is the first post-roll decision in combat that is not "pay or don't". Against a Mook a 10+ removes it and no rider applies. PvP is unchanged.

**Cover was cut.** The drafted third rider — a named ally's next reaction is free — undid R2. Waiving reaction Endurance keeps the party's pool high, which drives postures aggressive, which took the solo-Boss fight from a median 3 exchanges back to **2** and dropped phase-lands-before-the-final-exchange from 51–58.5% to **19–23%**. It was not too strong or too weak; it was a length-shortener wearing a defensive rider's clothes. The `free_reaction_ally` effect stays implemented and tested so a setting Facet or a future Technique can offer it deliberately, and the core ruleset refuses it.

> **A note on the acceptance itself.** Cover's gate was "mean PCs-Broken in the Hard row". That metric turned out to be blind: in any multi-enemy encounter the party always has a target that is not yet Open, so the menu collapses to Open and no other rider ever fires. **The riders are a Named/Boss-fight mechanic**, and a gate on a multi-enemy row cannot see them. The cut was made on the solo-Boss numbers instead. Future acceptances for rider-shaped mechanics should measure where the mechanic actually operates.

**R7 — the Archive Guardian re-authored.** Its Reduced Mode used to read "once Open, it stays Open", which under R2 is inert — the simulator returned numbers identical to the decimal with the flag on and off. Re-authored to MM1's *raise its danger* lever (blows land Tier 2 again; it fixes on whoever last opened it) and the threshold moved **2 → 4**, so the phase lands before the final exchange in **99–100%** of runs instead of 20–27%, at no cost in length or win rate. The Guardian now also changes stance once, on a stated conduct trigger: Measured until it is first left Open, Aggressive thereafter. Its III.3 vignette was rewritten to show all of it — the stance change, the enemy acting while Open, both riders being chosen for different reasons, Open expiring unused, a telegraphed Technique that makes Intercept matter, the phase landing mid-fight, and (per the style guide) a 7–9 and a 6− alongside the good rolls.

**Swept and clean:** no other Bestiary Boss (`bought_captain`, `glassback_bull`, `the_unfinished`) had a phase or Technique that assumed persistent Open. Two Named stance triggers that said "once left Open" were tightened to name the exchange.

**Status:** ✅ Decided by simulation. Shipped in `facets/base/facet.yaml`, `app/game/combat.py`, `app/api/websocket.py`, the app, III.3, III.1, MM1, MM5, Quick Start, II.4a, and the Glossary, in one change. `BRIEF_oraga_rewrite.md` §11 tunes S2/S3 against these rules.

### D21 — A setting Facet is additive by construction, and the schema now enforces it *(2026-09-09)*

**Source:** building `software/facets/valloh/facet.yaml`, the game's first setting Facet.

**The bug.** `magic` was a **singleton** section, replaced wholesale by the last module to declare it. The Val'loh Facet as briefed — "the merge appends them to the base list" — would instead have *deleted* the core's twenty-one domains, both traditions, and every domain type the moment it loaded. Nothing would have failed: the ruleset would simply have come back empty of magic, and INV-7 would have compared an empty catalog against the appendix and had nothing to say.

**The fix.** `magic` mixes two kinds of thing, and the merge now treats them as the spec's own vocabulary already distinguishes. `soul_domains` and `mind_domains` are **collections** keyed by id, exactly like `skills`. Everything else — traditions, domain types, the pre-Technique cap, the Spark rules — stays **singleton**. The rules half merges field-by-field on `model_fields_set`, because a setting that lists domains and says nothing about traditions is not asking for traditions to be blank.

**Generalisable, and worth checking before the next setting Facet.** Any schema section that mixes rules with catalogs has this latent. `combat` is the next candidate: it holds `conditions` and `strike_riders` (catalogs) beside `endurance` and `enemy_durability` (rules). Nothing needs it today because no Facet writes into `combat`, and INV-17 forbids Val'loh from doing so — fix it the first time one wants to.

**And the promise is now testable.** A setting Facet's counted-novelty line is a promise about how much a reader has to learn, and it is the first thing to rot. **INV-17** counts the lineages and gift domains claimed in `V0_Ten_Things.md` against the merged ruleset; siblings check that the Facet writes into no rules section, and that loading it leaves every core skill, Background, domain and rule identical. Adding a lineage without updating the pitch fails the suite, and so does the reverse.

**Status:** ✅ Decided and enforced.

### D22 — Key a Boss's second act to conduct when the fight is long, to Resolve when it is short *(2026-09-09)*

**Source:** `research/simulation_log.md` Series 12 Part B (the Archive Guardian) and Series 13 (the Bought captain).

**The pattern.** A phase keyed to a Resolve threshold fires when the arithmetic reaches it, which is reliably later than the author imagined.

- **Archive Guardian**, a three-exchange fight: phase at Resolve 2 of an effective 10 fired *in the exchange the fight ended* in three runs out of four. Fixable by raising the threshold to 4 — 99–100% of runs then see it land before the last exchange (D20/T15).
- **The Bought captain**, an eight-exchange fight: **no threshold works.** Even at 6 of an effective 7, under 1% of runs saw the phase by exchange 3, because the party needs six exchanges to grind him down. Re-authored as a stated conduct trigger — *his second exchange on the field, or the exchange after the party looks like winning* — which is MM1-legal, was already what the module's fiction said, and cannot arrive too late.

**The rule.** Short fight: a Resolve threshold is fine, set it near half the effective pool. Long fight: use a conduct trigger, because a threshold in a long fight is a phase the party reads about rather than plays against. **A second act nobody sees is not a second act.**

**Corollary, from the same two series:** free reactions are not defensive in this system. Three were measured — R3's Cover, the Guardian's old no-clear-Open Special, the Thenya Bond's reaction clause — and two were cut. Waiving a reaction cost preserves Endurance, high Endurance drives aggressive postures, and aggressive postures shorten fights. **Assume anything that waives a reaction cost is an offensive buff until a simulation says otherwise.**

**Status:** ✅ Decided.

### D24 — A gift is the player's choice of an existing domain *(owner ruling, 2026-09-18)*

**Decision:** "No need to map tribes to domains, let players choose." A gifted lineage carries one line saying how its gift **shows itself** in that people — *through grown crystal*, *as a prickle before danger* — and the **player chooses which domain it is**: any Soul or Mind domain in the core catalog that is not Prismatic. Gifts are always cast in the **intuitive** tradition (Spirit + Attune), whatever the chosen domain's own tradition, because blood is not study.

**What this reverses.** The ten custom Val'loh domains (Crystal, Warning, The Bond, Blade-bond, Stone-flesh, Dream, Wildspeech, The Weave, Mindshare, Resonance of Stone), their thirty example intents, and the `lineage_gift` / `draft` domain flags are gone. The owner's reasoning: one domain per tribe counters the flexibility the magic system was built for — it turns ten peoples into ten fixed classes. D19's row "Gifts are custom Focused domains" is superseded; D18 stands otherwise.

**What remains a setting's option.** `gift_domains` survives as an optional restriction list. Empty is the default and the norm; a setting that genuinely wants a people narrower may name a short list, and it is data rather than a special case.

**Effect on Val'loh:** the counted-novelty line is now *ten Lineages and crystal charges; no new domains, no rule changes*, machine-checked (INV-17). Val'loh writes nothing into `magic` at all.

**Status:** ✅ Decided and shipped.

### D23 — Significant and Major magic is prepared for; Minor is free *(owner ruling, 2026-09-18 — supersedes D17)*

**Problem, in the owner's words:** "If players can use magic indiscriminately they can use it to fix anything. Let's find a way to limit its use without the complexity of preparing spells." D17 had already located it — *"the gap is versatility outside combat, not power"* — and chose to fix it on the martial side. The owner reopened it on the magic side.

**Decision — readied intents** (the owner's own idea, refined):

- Every intent has one of five broad **purposes**: Harm · Ward · Mend · Shape · Reveal.
- **Minor scope is free** and unlimited. Small magic is what makes a caster feel like one, and it is not what breaks a campaign.
- A caster whose magic has formalized **readies three intents** at the start of each session, spread across the purposes as they choose. A **Significant or Major** working spends one of its purpose. The domain and what the magic actually does are still chosen in the moment — only the *shape* was committed.
- Nothing readied for the purpose → the working costs **a Spark** instead, and that Spark buys nothing else.
- Readied intents return after a **full rest, which the MM calls**, or at the next session. They cannot be re-readied until then.
- A spent intent stays spent whatever the roll: the commitment is what is paid for.
- **Formalization is what grants them**, so pre-Technique casters are unaffected (Minor only, with the existing Spark push to Significant) and the Tier 1 Technique finally has a concrete payoff beyond scope.

**Alternatives weighed** (mechanics are not copyrightable; licences noted for quoting): a shrinking *usage die* (The Black Hack, OGL) — the runner-up, zero prep but a random budget; *Endurance as cost* (Cairn CC BY-SA 4.0, Blades stress CC BY 3.0) — rejected because Endurance has no out-of-combat refresh, so it limits fights and not the problem; *spells as charged items* (Knave, CC BY 4.0) — Val'loh's crystals already do this; *7–9 backlash menus* (Dungeon World, CC BY 3.0) — price each cast but do not cap them; *spell slots* (SRD 5.1, CC BY 4.0) — the complexity the owner ruled out.

**Why it holds.** The limit comes from guessing: a party that readied Harm and Ward and walks into a negotiation has no Reveal. That preserves every bit of the in-the-moment invention Domain + Intent + Scope was built for — the thing slots would have destroyed — while making "the caster fixes everything" cost a prediction.

**What it does not change.** Per-roll difficulty, the 7–9 costs, and the Series 11 casting curves are untouched; this limits how *many* large workings happen, not how well each one goes. No combat simulation was run, because the simulator models no casters — the effect is on session-level versatility, and **three is a design number to be tested at a human table**, not a simulated one.

**Data:** `magic.prepared_intents` in `facet.yaml` — purposes, capacity, free scopes and the off-purpose price are all data, and a setting may drop the section to restore the unlimited game.

**Status:** ✅ Decided and shipped.
