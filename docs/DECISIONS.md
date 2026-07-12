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
