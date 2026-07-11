# HANDOFF — Planner → Brain, v0.3 Ruleset Revision

**From:** Planner (Opus)
**To:** Brain (Fable)
**Date:** 2026-07-10
**Artifacts produced:** `docs/DESIGN_v0.3_ruleset_revision.md`, `docs/TASKS_v0.3_ruleset_revision.md`, `docs/DECISIONS.md`
**Source:** `docs/BRIEF_v0.3_ruleset_revision.md` (D1–D8, all marked resolved)
**Branch:** `feature/data-driven-dice`, 721 tests green, no code changed yet

---

## What Brain is being asked for

Three rulings and one strategy call. Everything else in the BRIEF planned cleanly and needs nothing from you.

| # | Ask | Blocks | Planner's recommendation |
|---|---|---|---|
| **Q1** | The BRIEF's Major Advancement pacing target is not reachable without cheapening the beat. Confirm or overrule. | task B2 | Accept sessions 12–15 |
| **Q2** | The BRIEF's candidate armor shape (D2) does not work. Approve the replacement. | task A5 | Per-fight downgrade budget |
| **Q3** | How much of the existing simulation corpus should be treated as invalid? | G-gate baselines, MM1 budget claims | Treat all PC-side numbers as void; enemy-side TRs survive |
| **Q4** | D1 makes armor a different mechanic on each side of the screen. Is that acceptable ethos-wise? | nothing — informational, but it is your call | Yes, it follows from D1 |

The plan does **not** wait on these. WS-C (consolidation, 11 tasks) is unblocked and is where a Worker starts regardless.

---

## The BRIEF held up

Decomposed to 43 tasks across six workstreams. D1 (Resolve), D3 (Technique reachability), D4 (death + hazards), D5 (contradiction ledger), D6 (Sparks), D7 (content), D8 (K1 as a tested knob) all planned without friction. The workstream split you suggested survived intact, with WS-C first as you directed.

Two things you could not have known from the documents are in §3 below and they change the risk picture more than any single mechanic does.

---

## Q1 — Major Advancement pacing (P5)

**The BRIEF asks for:** Tier 3 Techniques reachable ~session 12–15; first Major Advancement ~session 10–12 (from ~25–27 today).

**What the math gives.** A Facet holds 15 rank advances (5 skills × 3). Two constants move: `facet_level_threshold` 6→5 (making 15 ÷ 5 = exactly 3 Facet levels reachable inside the primary Facet, which is what unlocks Tier 3), and `major_advancement_threshold` 4→3. Modelled across three assumptions about what fraction of the 4 SP/session a player actually spends in their primary Facet:

| Primary-SP efficiency | Facet level 1 | level 2 | **level 3 → Tier 3 + first Major** |
|---|---|---|---|
| 100% | s4 | s8 | **s12** |
| 80% | s5 | s10 | **s15** |
| 60% | s7 | s13 | **s19** |

Tier 3 lands at s12–s15. ✅ Your target.
First Major lands at s12–s15. ❌ Your target was s10–12.

**Why I did not hit it.** Pulling Major earlier means `major_advancement_threshold: 2`, firing the first Major at Facet level 2, around session 8. That is too cheap for something II.4 calls "the culmination of a long arc of play," and it decouples the Major from the Tier 3 moment. I judged that Tier 3 and the first Major landing *together* at s12–15 is a stronger dramatic beat than hitting s10–12 with a hollower one.

**What I need from you:** whether s10–12 was a load-bearing figure (a real pacing requirement derived from something) or an illustrative one meaning "much sooner than 25." If load-bearing, the lever is `session_skill_points` 4→5, which pulls everything in ~20% but inflates skill ranks as a side effect, and I'd want your read on whether that side effect is acceptable before I plan it.

---

## Q2 — The D2 armor shape does not work (P4, revised)

D2 delegated the mechanism to me with constraints and a candidate shape: *"downgrade the first incoming Condition per exchange (light) / per exchange plus one more per scene (heavy)."*

**The candidate fails its own primary constraint** — "armored entities must be breakable."

Broken is only reachable by taking a second Tier 2 Condition while already holding one. Tier 1 clears at end of exchange. So any rule that downgrades *every* incoming Tier 2 within an exchange prevents accumulation forever. The question is therefore how many Conditions a target receives per exchange.

`combat_sim.py:698-706` gives each enemy exactly one attack per exchange, at one PC. `resolve_enemy_attack` sets incoming tier by enemy tier: Mook 1, Named/Boss 2. **In a boss fight — one enemy — a PC receives at most one incoming Condition per exchange.** A "first Condition per exchange" downgrade absorbs it, every exchange, forever. The light-armored PC cannot be Broken by a boss.

This is the same infinite loop from `research/armored_enemy_breaking_problem.md`, relocated from the enemy side to the player side. My own first draft of P4 (light = 1 downgrade/exchange, heavy = 2) had the identical flaw: I reasoned from "a party focus-fires an armored target," which is the *enemy* threat model — and under D1 enemies no longer use Conditions at all. Their armor is flat bonus Resolve. The counter only ever runs PC-side, where the incoming rate is ~1/exchange and it never binds.

**It is currently masked.** `combat_sim.py:548-551` forces landed hits back up to Tier 2 once a PC is at 0 Endurance (`final_tier = max(final_tier, 2)`) — the Option A house rule from the armor research doc, which lives in the simulator and nowhere else. DESIGN retires it (P3), because under D1 its reason for existing is gone. **P3 and the candidate D2 shape together would reopen the loop**, and PT03 — your acceptance test for D1/D2, a boss fight, one enemy — is exactly the scenario that surfaces it.

**Replacement:** budget the downgrades **per fight, not per exchange**. Light armor downgrades the first 2 Conditions of a scene; heavy the first 4. One integer, one clock, never resets mid-fight, so capacity is genuinely finite.

Against a boss landing a Tier 2 each exchange: unarmored PC Broken ~exchange 2, light ~exchange 4, heavy ~exchange 6. Breakable ✅. Heavy strictly beats light ✅. Heavy mitigates Tier 2 ✅ (it is the same downgrade, twice as often). IV.1's fictional weight is untouched ✅. And it reads better at the table — armor absorbs the first telling blows of a fight and then stops helping, rather than resetting to pristine every few seconds. The 2 and 4 are starting values for G2, not assertions.

**Rejected alternative:** residue instead of depletion — armor downgrades every Tier 2 to Tier 1, but a Tier 1 taken *through* armor persists past end of exchange and a second escalates back to Tier 2. Conceptually prettier (armor never "runs out") but it means tracking two kinds of Tier 1 at the table, which is the bookkeeping this game exists to refuse.

---

## Q3 — The evidence base is weaker than the BRIEF assumes

This is the finding that should most change your confidence, and it is not about any mechanic.

**Combat resolution is implemented twice in this repo and the two copies disagree.** `software/app/api/websocket.py` is the live engine. `software/tools/combat_sim.py` is a parallel re-implementation. Diffs found:

| Behaviour | Engine (`websocket.py:626`) | Simulator (`combat_sim.py:237`) |
|---|---|---|
| Light armor vs Tier 1 | downgrades to nothing — condition **absorbed** | no effect — Tier 1 lands |
| Heavy armor vs Tier 2 | downgrades 2 tiers — **absorbed** | no effect — Tier 2 lands |
| 0-Endurance Absorb | no such rule | absorbed conditions forced to persistent Tier 2 |

The BRIEF's validation doctrine is *"simulation before prose — D1/D2 must be re-simulated before PHB text is rewritten."* That doctrine is unsound while the simulator is a re-implementation rather than a measurement. **Every number in `research/simulation_log.md` validated the simulator, not the game.** So did the Encounter Budget calibration built on top of it, and MM1's multipliers already carry an "unvalidated" flag for a different reason.

I inserted a workstream the BRIEF did not authorise (WS-A0, three tasks) to extract a single pure `app/game/combat.py` that both consume, with a permanent parity test asserting identical end-state through both paths. Without it, the G-gates you asked for measure nothing. I judged this inside Planner scope — it is architecture serving a strategy you already set, not a change of strategy. Flagging it because it spends three tasks the BRIEF did not budget, and because it means:

**What I think survives, and what I think does not:**
- **Void:** every PC-side win rate, Broken rate, and lethality figure in `research/simulation_log.md`. They were measured under simulator armor semantics *and* under the 0-Endurance house rule, both of which are being removed. G2 must re-baseline from zero.
- **Void:** the Encounter Budget difficulty multipliers (×1/×2/×3/×4). G4 re-derives them.
- **Survives:** the enemy-side Threat Rating arithmetic, because the migration map is chosen so `resolve := the old durability_value` and every published TR is preserved exactly (Sergeant 8, Veteran Soldier 10). Only the Archive Guardian moves, 16→14, because its `special` bonus was double-counted at authoring time (P6).
- **Uncertain, needs your call:** the playtest observations. PT01–06 conclusions about Spark hoarding, Aggressive posture as a trap, and MM cognitive load are *behavioural* and don't depend on the engine. But any playtest claim about combat lethality or advancement pacing does. Which brings me to:

**A third finding.** `Character._check_facet_level_threshold` (`character.py:215-216`) returns 0 for any skill outside the primary Facet. So `total_facet_levels` cannot exceed 2, and `major_advancement_threshold: 4` **has never fired for any character, in any campaign, at any length.** Major Advancement is not late — it is unreachable, and always has been. Any playtest observation about advancement pacing was made against an engine that could not advance. The BRIEF's "first Major lands ~session 25–27" is a paper calculation, not an observation.

Related: II.4 contradicts itself about whether cross-Facet levels count toward Major Advancement — line 89 says no, lines 207–209 say yes and work an example. Canonical answer is yes (D3 is incoherent otherwise). That is a **ninth row** on your D5 contradiction ledger, which listed eight.

---

## Q4 — Armor now means two different things (P8)

Under D1, enemy armor is flat bonus Resolve (light +1, heavy +2 — which happens to equal the `armor_bonus` term already in the TR formula, so the stat block needs no new number). Under D2, PC armor is Condition mitigation. Same equipment, two mechanics, chosen by which side of the screen you sit on.

This follows directly from your D1 ruling that "Conditions replace HP" applies to player characters only, and I think it is right: the asymmetry buys a very small enemy bookkeeping surface (one integer) and keeps Conditions as player-facing fiction where they playtested well. But asymmetric equipment is an ethos question, not an engineering one, and you own the ethos. If you want symmetry, the fallback is the rejected D1 alternative (condition-track boxes for enemies) and I would replan WS-A around it.

---

## What is not blocked

WS-C — the consolidation pass, 11 tasks, one commit — needs nothing from you and should start now. It is cheap, it produces clean diffs for everything downstream, and it ends the stale-rules contamination that corrupted playtest 06. WS-A0 (the extraction) and WS-E (content) are also unblocked. Q1 blocks exactly one task (B2); Q2 blocks exactly one task (A5).

---

## Recommended next step

Rule on Q1–Q4. Q2 and Q3 are the ones I would not proceed past without you: Q2 because your own candidate shape is unsound and I am substituting my own, and Q3 because it determines how much of this project's recorded evidence you still trust. Q1 and Q4 have safe defaults already recorded in `docs/DECISIONS.md` (P5, P8) and a Worker can proceed on them if you would rather not spend the turn.

Then hand back to Planner only if Q1 or Q4 changes the plan; otherwise hand straight to Worker at **WS-C, task C1**.
