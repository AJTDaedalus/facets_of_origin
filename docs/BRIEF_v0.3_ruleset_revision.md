# BRIEF — v0.3 Ruleset Revision

**Tier:** Brain (Fable) output — hand to Planner (Opus)
**Date:** 2026-07-10
**Source evidence:** `docs/REVIEW_editorial_2026-07-10.md` (full editorial review), playtests 01–06, `research/armored_enemy_breaking_problem.md`, `research/simulation_log.md`
**Branch context:** `feature/data-driven-dice` (v0.2, 721 tests)

---

## Problem Statement

Ten playtests validate the core engine (three-tier 2d6, postures/reactions, Domain+Intent+Scope, Backgrounds) but expose three structural defects and a contradiction debt:

1. **Enemies have no coherent durability model.** Enemy Endurance is a dead stat (NPCs never roll, so never spend it), Named/Boss enemies fall to two full-success Strikes, and light armor makes enemies literally unbreakable. Result: every playtest table — including the expert-MM persona — independently reinvented hit points, and both "zero fun" TPKs happened inside that house-ruled system.
2. **Tier 3 Techniques are mathematically unreachable** (max 2 Technique picks per Facet tree, Tier 3 requires both picks spent in one branch first). Prismatic domains and Second Domain are dead text. First Major Advancement lands ~session 25–27.
3. **No hazard rules and no stated death policy** — MMs improvise per-exchange damage taxes and "0 Endurance = dead," producing the documented TPK failure mode.
4. **Contradiction debt:** the same rule is answered differently across PHB body text, quick references, and MM5 in at least 8 places. One stale rule (pre-technique magic penalty in II.5) demonstrably corrupted playtest 06.

For a game whose pitch is "rules never get in the way," these defects manufacture exactly the friction the ethos forbids.

## Goals

- Every enemy is defeatable, and boss fights are runnable by the book for 3+ exchanges without house rules.
- Every printed Technique is reachable in realistic campaign play.
- A novice MM can resolve hazards and character death without inventing subsystems.
- One canonical answer per rule, propagated to every file; quick references compress rules, never restate them.
- Spark economy produces observed *spending*, not hoarding, in the next playtest.
- All settled mechanics land in `facets/base/facet.yaml` + engine + tests in the same cycle (per Software–PHB sync workflow).

## Non-Goals

- No redesign of core resolution (2d6 three-tier), posture set, reaction set, or the PC-facing-rolls-only principle. These are validated; do not touch.
- No changes to character creation flow or the 18-point attribute buy.
- No new subsystems beyond the Threat Clock (which reuses existing outcome tiers).
- Deferred modules (Downtime, Crafting, Economy, Feats, Technology) stay deferred.
- GUI work beyond what changed mechanics require.

---

## Approach — Decisions

### D1. Enemy durability: Resolve pool for enemies; Conditions remain PC-only damage language ✅ *user-approved 2026-07-10*

**Selected:** Asymmetric durability. PCs keep the Condition system unchanged (it playtested well as *player-facing* fiction). Enemies (Named/Boss) get a small **Resolve pool** (working range 2–6, **widened to 2–8 by Gate G1**, see below) that PC Strikes deplete by outcome tier (10+ = 2, 7–9 = 1), with Conditions becoming attacker-chosen **riders** on full successes rather than the kill-track. Resolve 0 = defeated. Phase changes trigger at Resolve thresholds — finally giving MM1's phase-change language a real mechanism. Mooks unchanged (one Strike removes).

**Range confirmed by Gate G1 (task A8, 2026-07-10, DESIGN §5-bis; full data in `research/simulation_log.md` Series 7):** a solo, single-target Boss cannot be tuned to a 45–55% party-loss rate at any Resolve value — that criterion was void-derived from the Encounter Budget's "Hard ≈ 50%" multiplier, which Brain's Q3 already voided, and is dropped. G1 was reframed as a length-plus-cost gate (median ≥ 3 exchanges, defeatable, zero house rules, cost signal recorded). Under that gate, the Archive Guardian's base Resolve needed retuning from 5 to **8** (confirmed by sim, robust across 7 seeds at n=200) to clear the median-3-exchange floor against the rider→Easy snowball. Named-tier Resolve (3–4, confirmed stable in the same Series 7 data) remains well inside the original 2–6 band — the ceiling extension is a **Boss-tier finding**, not a shift of the whole range. The working range is therefore **2–8**, with Boss-tier durability sitting at the top.

**Rationale:** Every table already ran this; it makes the TR durability table and phase thresholds coherent; it keeps enemy bookkeeping to one small number (lower MM load than per-enemy named-condition tracking); it preserves "Conditions replace HP" where it matters — the players' own bodies and stories.

**Rejected alternative:** Pure condition-track boxes for enemies (Named = 2 Tier 2 boxes, Boss = 3–4). More ethos-pure on paper, but playtest drift shows tables want a number for enemies, and it leaves phase-change triggers awkward. Viable fallback if the user vetoes Resolve.

**Consequences the Planner must handle:** enemy Endurance field is retired or renamed → `facet.yaml`, Enemy model, TR durability table re-keyed to Resolve, MM1 stat blocks, all `enemies/*.fof`, combat simulator, engine strike handler, encounter-budget recalibration sims.

### D2. Armor redesign (both sides)

Constraint-driven; exact mechanism is Planner's to design and **validate by simulation**:
- Armored entities must be breakable (kills the documented infinite-loop bug).
- Heavy armor must do something against Tier 2 attacks (currently it is strictly worse than light).
- Heavy > light in protection; both retain fictional weight per IV.1.
- Candidate shape: downgrade the **first** incoming Condition per exchange (light) / per exchange plus one more per scene (heavy) — but any design meeting the constraints is acceptable. For enemies under D1, armor plausibly becomes flat bonus Resolve; simulate.

### D3. Technique acquisition fix

Any Facet level (primary or cross-trained) grants a Technique pick from **any tree whose prerequisites the character meets**. Tier gating (T2 needs same-branch T1, T3 needs same-branch T2) unchanged.
**Pacing targets** (Planner tunes thresholds/SP-rates to hit them, then verifies with advancement-math tables in the DESIGN):
- Tier 3 Technique reachable by roughly session 12–15 for a dedicated character.
- First Major Advancement by roughly session 10–12 (current: ~25–27). Adjusting the "every 4 Facet levels" threshold is on the table.
- Update the II.4 "Advancement at a Glance" block, career-advance tier table, and engine advancement logic together.

### D4. Death policy + hazards

- **Death rule (one PHB paragraph):** Broken never kills by default. Death enters the fiction only by player choice. Adopt a Doom-Gate-style choice at the moment a Broken result would be fatal in fiction: permanent scar/cost and stay down safely, **or** heroic death with one automatically successful final action. (Source: `playtest/06_expert_novice_campaign/fun_and_consequence_review.md`, Revision 1 — adapt, don't copy verbatim; strip the "below 0 Endurance" framing, which isn't how our rules work.)
- **Threat Clocks (hazards):** 4-segment visible clock; advances on party 7–9/6- results near the hazard; when full, the hazard strikes (Condition or forced save); players can spend actions to wind it back. Goes in III.2 Adventuring (new chapter — this brief authorizes starting it minimally: hazards + clocks + death rule + recovery; do not scope-creep III.2 into a full chapter).

### D5. Contradiction consolidation — canonical rulings

One pass, one commit, every file (PHB, MM manual, Quick Start, `facet.yaml`, engine, character/enemy files). Canonical answers:

| Rule | Canonical | Fix locations |
|---|---|---|
| Pre-technique magic | Minor scope only, **no difficulty penalty** | II.5 "Magic and Backgrounds" (stale text), verify II.3/MM5/QS/engine agree |
| Broken threshold (PCs) | Second Tier 2 **of the same type** escalates; Staggered+Cornered coexist | III.3 quick ref, MM5 (both currently say "same or different") |
| Parry | Outcomes identical to Dodge — **no counter** | III.3 quick ref, MM5 (both invented a 10+ counter) |
| Weapons/Strike | Weapon category sets attribute (per IV.1); skill = Combat (melee/unarmed), Finesse (ranged); Strike formula generalized to "2d6 + weapon attribute + relevant skill" | III.3 Strike/Parry text, MM5, QS quick ref; engine already permissive |
| PvP ties | Both achieve partial success (III.1) | MM5 "ties go to defender" |
| Attribute label | Rating 1 = "Weak" | MM5 says "Poor" |
| Ghost text | Delete "Spent ally" (Intercept); fix Maneuver wording to "rolls **against** the target are Easy"; MM1 phase triggers re-keyed to D1 Resolve | III.3, MM1 |
| Example-character continuity | Zahna: Inscription / Knowledge / Spirit 2 / he — rewrite the II.3 "Fire mage" example accordingly. Zulnut: Wandering Disciple / he — fix II.5 closing analysis and II.4 pronoun. Mordai: Endurance Novice+1 mark, pool 5 — fix III.3 example pools | II.3, II.5, II.4, III.3 vs QS + character files |

**New repo rule (add to CLAUDE.md):** quick references may only compress canonical text, never paraphrase it; any rules change must update body text, all quick refs, `facet.yaml`, and engine in one commit.

### D6. Spark economy — structural earning, in the PHB (not MM5-only)

- **Act Break Nomination** codified in III.1: at each act break, each player nominates one other player; MM confirms.
- **Graceful Fail becomes player-initiated:** on any 6-, the player may claim it by narrating how they make the failure worse/richer; MM confirms → Spark. (Turns failure into resource income — the proven anti-hoarding loop.)
- **Test, don't yet adopt:** Spark refund when a pre-technique magic cast fails despite a spent Spark. Include as a variant flag in the next playtest.
- Keep: 3 Sparks per session, spend-before-roll, add-die-drop-lowest. Do not add post-roll spending.

### D7. Content additions (writing tasks, no mechanics)

- **Domain example intents:** 3 examples per scope (Minor/Significant/Major) per domain, all 18 domains, in the Appendix. Framed explicitly as design patterns, not a menu. (Requested independently in three playtest documents.) Rejected: pre-set "spell packages" — that is a spell list by another name.
- **MM Trouble Table** in MM5: d6-able generic 6- consequences (cost / position / attention / equipment / condition / revelation) + duplicate II.3's magic 6- templates into MM5.

### D8. Aggressive posture — instrument, don't redesign ✅ *user-approved 2026-07-10: test K1*

Evidence (batch report, Valerie retro, PT01) shows Aggressive is a trap for unarmored low-Endurance PCs and an auto-pick against Mooks. Do **not** change it blind. Planner schedules a sim + playtest comparing **K1 — the +1 reaction surcharge applies to the first reaction per exchange only** — against the current baseline. Adopt K1 only if the sim/playtest shows it softens the unarmored death-spiral without erasing the Aggressive tradeoff. (Rejected without testing: K2 surcharge-waived-at-3+-Endurance, adds a conditional; K3 sidebar-only, doesn't address the math.)

---

## Validation & Playtest Plan (downstream robustness)

- **Simulation before prose:** D1/D2 must be re-simulated (combat simulator + `research/simulation_log.md` conventions) before PHB text is rewritten. Encounter Budget multipliers and the Encounter Recipe Table will shift; recalibrate and record.
- **PT03 (boss stress test) is the acceptance test for D1/D2:** a by-the-book boss fight must run 3+ exchanges, be winnable at ~Hard rates, and require zero house rules. It is currently unrunnable — that's the forcing function.
- **PT04 (resource tax) is the acceptance test for D6:** Sparks spent per player ≥ 2 with the new cadence, or D6 gets revisited.
- **Playtest data hygiene (constraint on all future agentic playtests):** roll logs must come from the actual server with per-player dice; modifier columns must reconcile with sheets; invented conditions/mechanics are flagged as drift findings, never adopted silently. Adventures 2–10 of PT06 are directional evidence only — never calibrate numbers from them.

## Constraints (standing, from project rules)

- TDD: tests first; ≥3 tests per public function; full suite green before any workstream is "done."
- Sync order per CLAUDE.md: `facet.yaml` → engine/character model → websocket events → tests → commit referencing PHB section.
- Copyright policy applies to all new content (D7 especially).
- Vignette voice and established character canon per `references/phb-examples.md` for any rewritten examples.

## Open Questions — RESOLVED (user, 2026-07-10)

1. **D1:** Approved — Resolve pool for enemies; PCs keep Conditions unchanged. "Conditions replace HP" is hereby amended to apply to player characters only.
2. **D8:** Approved — test knob K1 (surcharge on first reaction per exchange only) via sim + playtest before adopting.
3. **D4 scope:** Approved — write minimal III.2 Adventuring this cycle (hazard Threat Clocks + death rule + recovery only; strictly scoped).

No open questions remain. The BRIEF is Planner-ready.

## Suggested Workstream Split for the Planner

1. **WS-A Combat durability** (D1 + D2 + sims + PT03) — largest, blocks PT03/05.
2. **WS-B Advancement math** (D3) — independent; pure math + text + engine.
3. **WS-C Consolidation pass** (D5 + CLAUDE.md rule) — do **first**; it's cheap, unblocks clean diffs for A/B, and ends the stale-rules contamination of playtests.
4. **WS-D Sparks + death/hazards** (D4 + D6 + PT04) — medium.
5. **WS-E Content** (D7) — parallelizable writing work, no engine impact.

---

*All decisions D1–D8 are resolved. Next step: switch to Opus (Planner), produce `DESIGN_v0.3_ruleset_revision.md` (or one DESIGN per workstream) + `TASKS_*.md`, planning WS-C (consolidation pass) first.*

---

## BRIEF AMENDMENT — Brain rulings on the 2026-07-10 escalation

**Tier:** Brain (Fable). **Input:** `docs/HANDOFF_v0.3_planner_to_brain.md` (Q1–Q4), `docs/DESIGN_v0.3_ruleset_revision.md`, `docs/TASKS_v0.3_ruleset_revision.md`, `docs/DECISIONS.md` (P1–P8). All load-bearing code claims (F1, F3, F6, the 0-Endurance override, the II.4 contradiction) were independently re-verified against the source before ruling.

### Q1 — Major Advancement pacing: **s10–12 was illustrative. Accept P5.**

The figure meant "much sooner than 25–27"; it was not derived from anything — it *could not* have been, since (per Q3/F3) no character has ever reached a Major Advancement in code. The Planner's substitute is better than the target: Tier 3 and the first Major landing together at s12–15 is a converging payoff — one milestone session instead of two diluted ones. Do **not** touch `session_skill_points`; rank inflation is a worse cost than a three-session slip on an illustrative number. The BRIEF's pacing target is hereby amended to *"Tier 3 and first Major Advancement land together, roughly session 12–15 for a dedicated character."*

### Q2 — Armor shape: **approved. Per-fight downgrade budget (light 2 / heavy 4, as G2 knobs).**

The Planner is correct that the BRIEF's candidate was unsound — Brain owns that error: I reasoned from the party-focus-fires-a-target threat model, which D1 had already moved to Resolve. The per-fight budget meets all four D2 constraints, is one integer of state the digital layer absorbs, and its fiction is genuinely diegetic (armor takes the first blows of a fight, then it's dented and hanging). The rejected "residue" alternative stays rejected for exactly the reason given — two flavours of Tier 1 is the bookkeeping this game exists to refuse.

**Required amendment (terminology):** the DESIGN says "per fight" and "resets at end of scene" in the same paragraph. Pick one word. Canonical: **per scene** — the budget resets when the scene ends, and a fight is a combat scene. Two fights inside one scene share the budget. Player text and `facet.yaml` key must both say scene (`downgrades_per_scene`, not `downgrades_per_fight`).

### Q3 — Evidence corpus: **rule as the Planner recommends, with the boundary made explicit.**

- **Void:** every PC-side win rate, Broken rate, and lethality figure in `research/simulation_log.md`; the chicken baselines; the Encounter Budget difficulty multipliers. All measured under simulator-only armor semantics plus a house rule that P3 retires. G2/G4 re-baseline from zero. Mark the affected Series in `simulation_log.md` as `SUPERSEDED (v0.2 semantics)` rather than deleting them.
- **Survives:** enemy-side TR arithmetic — by *construction* of the migration map (`resolve := old durability_value`), not by luck. P6's Guardian correction (16→14) approved.
- **Survives as behaviour, not as numbers:** playtest observations about Spark hoarding, MM cognitive load, and Aggressive-as-perceived-trap. Any *quantitative* playtest claim about lethality or advancement pacing is directional at best.
- **WS-A0 is retroactively authorised and is the most valuable item in the plan.** Extracting `combat.py` with a permanent parity test is the correct spend of three unbudgeted tasks. Add a second clause to the C1 repo rule: *the simulator may only drive `app/game/combat.py`; it must never re-implement a rule.* That is the process guarantee that F1 cannot recur.

### Q4 — Asymmetric armor: **approved. It is ethos-consistent, not ethos-tolerated.**

The game is already asymmetric at its root: PCs roll, enemies don't; PCs have stories, enemies have stat blocks. "Conditions replace HP" was always a statement about whose body the fiction cares about — the players'. Enemy armor as flat Resolve and PC armor as Condition mitigation each put the bookkeeping on the side of the screen that can carry it. **Presentation requirement:** the PHB and MM1 must present these as two different tools, never as one rule with an exception. On a stat block, "armor" is a Resolve bonus; on a character sheet, it is a downgrade budget; the app displays each automatically. One sentence in each place, no cross-reference.

---

### Editorial findings (Brain review of the full plan — these need a Planner patch to TASKS before WS-A0)

**EF1 — Rider Conditions have no defined effect. Blocks A4 and A11; would silently corrupt G1.** D1 makes Conditions "riders" on enemies, but neither DESIGN §4.1 nor task A4 says what a rider *does*. If riders do nothing, they are dead text — the disease D3 cures elsewhere. Canonical answer: **riders keep their existing table effect — Strikes against a Staggered or Cornered enemy are Easy; Tier 1 riders clear at end of exchange as normal.** That makes the 10+ choice real (depletion now vs. setting up allies). Critically: **the G1 simulation must model rider→Easy**, or it validates a game nobody will play — the exact class of error Q3 just cost us the corpus over. Also measure in G1 whether 2-Resolve-plus-Easy-rider snowballs boss fights below the 3-exchange floor.

**EF2 — B5 misses the sentence that becomes false.** II.4's philosophy sidebar (~line 85: *"Facet level 3 isn't earned by going deeper; it's earned by going wider"*) is true at threshold 6 and false at threshold 5, where level 3 is reachable in-Facet. B5 must rewrite that sidebar (the honest new framing: level 3 = you have mastered all five skills of your Facet; level 4+ is where breadth begins) or it is ledger row 10 the day B2 lands.

**EF3 — E1's arithmetic contradicts the BRIEF.** D7 asks for 3 examples per scope per domain (3×3×18 = **162**); DESIGN §9 and E1 compute "= 54." Ruling: **3 per scope stands.** Variety per scope is the anti-canonization mechanism — one example per scope becomes "the Minor Inscription spell" within two playtests. Entries stay one line each; if they start reading like castable spells mid-writing, stop and escalate.

**EF4 — Threat Clock wind-back needs one word: automatic.** If winding back requires a roll, a 7–9 on the wind-back advances the clock being wound — a rules-lawyer loop in a chapter aimed at novice MMs. Canonical: spending the action winds the clock back, no roll. Separately, sanity-check pacing in review: ~72% of nearby rolls advance a 4-segment clock, so hazards strike after ~3–4 party rolls. Probably right for "visible pressure," but say it on purpose in III.2, not by accident.

**EF5 — G0's acceptance criterion is statistically wrong.** A behaviour-preserving refactor with identical seeds must produce **identical** outcomes — that is the test. ±3pp at n=200 is roughly one standard error at p≈0.5, so the gate would both pass real regressions and fail clean refactors by chance. Amend A0.3: exact end-state match on the 5 fixed seeds is the primary criterion; the ±3pp aggregate band applies only if the refactor legitimately changes RNG draw order (document why, if so).

**EF6 — A5's breakability test is underspecified.** "Broken within 6 exchanges" is only deterministic under a stated policy. Specify: PC forced to Absorb every incoming attack, enemy lands Tier 2 each exchange. Otherwise the Worker ships a flaky test or quietly weakens the assertion.

**EF7 — WS-D task IDs collide with BRIEF decision IDs.** Tasks D1–D7 vs decisions D1–D8, in a project that just built a contradiction ledger about ambiguous cross-references. Renumber the tasks WD1–WD7.

**EF8 — Threat Clocks have engine events but no UI task.** Task "D2" (WD2) creates `clock_*` events and says "players see them," but no task touches `play.js`. A clock that lives only in WebSocket frames is bookkeeping the digital layer *failed* to absorb — a direct ethos violation. Add a UI task to WS-D (render clocks in the Play Field for all players; MM gets create/advance/wind-back controls).

**Ethos note for A11/III.3 prose:** a PC in combat now tracks five things (Endurance, posture, Conditions, Sparks, armor budget). Digital-first makes this fine *only if* the quick reference shows where each number lives on screen. Write it that way.

---

**Resolved. Return to Planner for a small TASKS patch (EF1–EF8; ~30 minutes), then to Worker at WS-C task C1.** WS-C is unblocked by everything above — a Worker may start C1 in parallel with the Planner patch. A5 and B2 are now unblocked (Q2, Q1 resolved). Nothing in Q1–Q4 changes the workstream structure, the sequencing, or the gates.
