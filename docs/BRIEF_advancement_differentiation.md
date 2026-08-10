# BRIEF — Advancement Differentiation (rank caps + escalating marks)

**Tier:** Brain (Fable) output — hand to Planner (Opus)
**Date:** 2026-08-09
**Ruling worked under:** User, 2026-08-09 — *"'Everyone masters their primary' is wrong. A lot of different classes fall under each Facet — a ranger shouldn't be as good at hand-to-hand as a barbarian (equivalent, of course)."* Recorded in `docs/DECISIONS.md` by the user. This BRIEF decides *how*, not *whether*.
**Source evidence:** `docs/RESEARCH_advancement_benchmark.md` (§1 numbers, §3 fix shapes, §4 cross-training inversion, resolved ESCALATION), `player_handbook/II.4_Character_Creation_Facets.md`, `software/facets/base/facet.yaml` `advancement:` block, `docs/DESIGN_v0.3_ruleset_revision.md` §6.2 (superseded), `research/dice_system_analysis.md`.
**Supersedes:** DESIGN_v0.3 §6.2's `facet_level_threshold: 5`, which was chosen so all three Facet levels fit inside the 15-advance ceiling. That decision optimised for tidy Technique unlocks and did not weigh intra-Facet differentiation.

---

## Problem Statement and Motivation

A Facet is a *category* of archetypes, not an archetype. Body contains the brawler, the scout, the duellist, the acrobat — and today every one of them converges on the identical sheet: all five Body skills at Master, in ~11 sessions of primary-focused play. Verified numbers (RESEARCH §1): 4 SP/session, 3 marks/advance, 5 skills × 3 advances = 15 advances = 45 SP = 11.25-session floor for the whole Facet; one skill Novice→Master is 9 SP (2.25 sessions).

This is an **identity** problem first and a pacing problem second. Two structural symptoms share one root cause:

1. **No opportunity cost on skills** (RESEARCH §3). 15 advances buys everything the Facet sells. Players choose *ordering*, never *trade-offs*. Facets is the only system in the benchmarked field whose advancement track terminates in total completion — Call of Cthulhu asymptotes, Apocalypse World and Savage Worlds offer menus wider than the picks, 5e forks exclusively.
2. **The cross-training incentive runs backwards** (RESEARCH §4). The primary Facet grants exactly 3 Technique picks against a tree of 18–20, and the only road to a fourth pick — even one from your own tree — is cross-training to Facet level 4. The field's convention is that breadth *costs* depth; here breadth is the sole *source* of further depth.

Root cause of both: **the primary Facet is a finite checklist that completes, and skills and Techniques complete in the same session** (15th advance = Facet level 3 = third pick = full skill mastery, one event).

The ruling demands a ceiling that makes a Body character become a *particular* Body character — permanently, at any campaign length.

## Goals

- Two same-Facet characters who play the same 20+ sessions end with **visibly different sheets**, by their own choices, and never reconverge.
- The player-facing rule fits in **two sentences and one table row**. No new resource, no new track, no per-session bookkeeping.
- Facet levels 1/2/3 — and therefore all three Technique picks, including the magic formalization arc — remain reachable **inside the primary Facet alone**, at pacing consistent with the v0.3 targets (Tier 3 / first Major in roughly sessions 12–15).
- The digital layer absorbs the arithmetic (mark thresholds, remaining slots); the table absorbs nothing new.
- `facet.yaml`, engine, tests, PHB, and MM Manual all move in the same cycle, per the sync workflow.

## Non-Goals

- **No redesign of the Technique layer.** 3 picks from 18–20, branch-gated tiers, the single fungible pick pool — untouched. It is the game's one existing genuine exclusive choice; this change adds a second, in the skill layer, without disturbing the first.
- No change to marks, ranks (Novice/Practiced/Expert/Master), Facet levels, Techniques, or Major Advancement *as concepts*. This is a retune.
- No change to `session_skill_points: 4`, banking (≤2), the training mark, or the 18-point attribute buy.
- No change to skill lists, skill–attribute pairings, or the number of skills per Facet.
- No new fiction, lore, or setting terms.

---

## Approach Selected

Four decisions. A1 is the mechanism; A2–A4 are its knock-ons.

### A1. Rank caps per Facet, with escalating marks per rank underneath

**The cap (the ceiling the ruling demands):** *In each Facet, at most **three** of your skills may rise beyond Practiced, and only **one** of those may reach Master.*

Final shape of a fully developed 5-skill Facet: **1 Master, 2 Expert, 2 Practiced** — 9 rank advances instead of 15. The cap binds every character in every Facet uniformly, primary and cross-trained alike: a Body-primary character developing Mind skills is under Mind's cap too. One rule, no asymmetry. Practiced is uncapped — everyone can be broadly competent; the ceiling starts where excellence starts. Cap choices are permanent, like Technique picks: you do not un-Master a skill to free the slot.

**The curve (escalating marks per rank):**

| Advance | Marks required |
|---|---|
| Novice → Practiced | 3 *(unchanged)* |
| Practiced → Expert | **5** |
| Expert → Master | **8** |

One skill Novice→Master becomes 16 marks (was 9). The full primary shape costs **38 SP** (5 Practiced ×3 + 3 Expert ×5 + 1 Master ×8), floor ≈ 9.5 sessions. The early game — the onboarding hook — is untouched: the first advances still cost 3 marks.

**Why both parts, not one.** The cap alone completes in 27 SP (~6.75 sessions) — *faster* than today, and Master costs the same 3 marks as Practiced, so the capstone feels cheap. The curve alone (RESEARCH §3 option A) delays completion to ~20 sessions but the track still completes, so a long campaign reconverges the ranger and the barbarian — already ruled insufficient. Together: the cap supplies permanent identity, the curve supplies pacing and weight. Pushing Expert→Master (8 marks) while two skills sit at Practiced (3 marks each) is a trade-off a player *feels* every session without tracking anything new — the app counts the marks, exactly as it does today.

**Why 1 Master + 2 Expert and not 2 Master + 3 Expert.** Under 2M+3E all five skills reach Expert (the two Masters pass through), so the only choice left is which two skills get +3 instead of +2 — ten possible shapes, and a +2..+3 spread that barely differentiates. Under 1M+2E the spread is +1..+3 across the sheet and there are thirty shapes: the barbarian's Combat is Master (+3) while the ranger's sits at Practiced (+1) — *equivalent characters, visibly different*, which is the ruling verbatim. 2M+3E also prices the full shape at 56 SP (~14-session floor, ~18 realistic), pushing Tier 3 Techniques past the v0.3 target window; 1M+2E lands inside it (A2).

### A2. Facet level threshold: 5 → 3

Nine available advances break `facet_level_threshold: 5` (only one level would ever land). New threshold **3**: Facet levels at 3 / 6 / 9 advances. `major_advancement_threshold` stays 3, so the first Major Advancement still arrives with Facet level 3 — now meaning "you have finished becoming *your* Body character," not "you have mastered everything Body sells."

Pacing (floor = all 4 SP into primary every session; realistic assumes normal spread):

| Milestone | Advances | SP floor | Sessions floor | Realistic | Current (floor / MM3–2) |
|---|---|---|---|---|---|
| Facet level 1 (first Technique) | 3 | 9 | 2.25 | ~3–5 | 3.75 / 4–8 |
| Facet level 2 | 6 | 20 | 5 | ~6–10 | 7.5 / 8–15 |
| Facet level 3 + first Major | 9 | 38 | 9.5 | ~12–16 | 11.25 / 12–20 |

Levels 1 and 2 arrive somewhat earlier (cheap Practiced advances front-load), level 3 lands in the same realistic window as today — the escalating curve back-loads the cost, so the three Technique picks spread across the campaign instead of bunching. First Technique by roughly session 3–5 is a deliberate onboarding win (the research is explicit that early competence growth is the hook), and it shortens the pre-technique Minor-scope window for magic Backgrounds — the direction playtest 01 already pushed. Tier 3 / first Major at ~12–16 sessions matches the v0.3 BRIEF's D3 targets. Level 3 still coincides with completing the primary track, but under the cap that coincidence is now *thematically correct*: the track completes into a chosen shape, not into everything.

### A3. The §4 cross-training inversion: deferred — and materially reframed by A1

Do not decouple Technique picks from Facet levels, and do not add primary Facet levels beyond 3, in this change.

**Why deferral is now defensible rather than evasive.** The §4 critique — "breadth is the only road to more depth" — presupposed that the primary road was an unfinished checklist being tolled. Under the cap, the primary road genuinely *ends*, by design, at your chosen shape; growth after that point **is** breadth, which is exactly what II.4's *Through the Mirror* box already claims ("at the highest levels, experts grow by absorbing adjacent disciplines"). The fungible pick pool is the feature that lets that veteran buy a fourth Technique from their original tree. The structure stops being an inversion and becomes the stated design, finally load-bearing.

Two side effects of A2 also shrink the residual pain: a cross-Facet level now needs 3 advances instead of 5 (cheapest: 3 Practiced = 9 marks = 18 SP ≈ 4.5 sessions, versus 30 SP ≈ 7.5 before), so the fourth pick arrives around sessions 14–17 for a dedicated character instead of ~19+; and total career ceiling becomes 27 advances / 9 Facet levels / 3 Majors across all three Facets (~190 SP, ~47-session floor) — ample runway, still finite, still differentiated at the very end because Master choices differ per Facet.

**Rejected direct fixes:** granting picks from career advances or milestones either floods the pick supply (destroying the 3-from-18 exclusivity the constraints protect) or requires a new trigger track (forbidden). Uncapped primary levels 4+ have nothing left to drive them once the skill track is complete — any driver invented would be a new track.

**Hand to Planner instead:** MM3's veteran-play guidance must *say* the reframe out loud — "your primary shape is finished; levels 4+ are breadth, and breadth is how you reach deeper into your own tree" — so no table reads the endgame as a toll. Revisit §4 only if post-change playtests show veterans stalling.

### A4. Cross-Facet cost stays 2 SP per mark

The 2× toll was priced when the primary Facet was an 11-session well; now the primary completes at ~38 SP and all veteran spending is cross-Facet. Keep the price anyway. Its function shifts from "premium versus primary" to **veteran-pace governor**: post-shape advancement slows naturally (the CoC-asymptote effect achieved without dice), which is what MM3–4 already assumes of veterans ("difficulty alone will not challenge them"). Combined with the curve, an off-Facet Master advance costs 16 SP — four full sessions for one rank — which is the correct price for the deepest possible off-spec commitment and is the multiclass fantasy priced the conventional way at last: breadth now costs *time*, since depth is capped. No number changes; flag for the first post-change playtest rather than pre-tuning.

---

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Escalating marks alone (RESEARCH §3-A) | Track still completes (~20 sessions); long campaigns reconverge the ranger and the barbarian. Already ruled insufficient in the resolved ESCALATION. |
| Cap alone, flat 3 marks | Primary track completes in ~6.75 sessions — accelerates the very "too rapid" feel the user flagged; Master costs no more than Practiced, so the capstone feels cheap. |
| Cap at 2 Master + 3 Expert (12 advances, threshold 4) | All five skills reach Expert; differentiation collapses to which two get +3 (ten shapes, +2..+3 spread). 56 SP full shape pushes Tier 3 to ~18 realistic sessions, missing the v0.3 window. |
| CoC-style improvement rolls (roll over current value) | Adds dice to advancement — randomized progression is a documented feel-bad shape, and a failed improvement roll is friction the philosophy forbids, even if the app rolls it. |
| Decouple Facet levels from advance counts (§3-C) | Needs a new trigger (milestones, career totals) = a new track and MM bookkeeping. Forbidden by constraint. |
| Widen the Facet to 6+ skills (§3-D) | Largest blast radius (II.6, all Facet chapters, every character file), dilutes each skill's identity, and still completes eventually unless capped anyway — so it doesn't remove the need for this change. |
| Decouple Technique picks / primary levels 4+ (§4 direct fixes) | Floods pick supply or requires a new track; see A3. Deferred with an explicit revisit trigger, not ignored. |

---

## Downstream Robustness Considerations

- **Reconvergence at any length:** with caps binding all three Facets, even a tri-Facet-complete 47-session veteran differs from another by three Master choices and six Expert choices. The ruling holds at every campaign length, which curve-only fixes could not guarantee.
- **Engine:** `advance_skill` must enforce caps (reject marks that would require a forbidden rank — marks must never accumulate toward a rank the cap forbids, or players will bank into a wall) and read per-tier mark thresholds. Note while in there: `_try_advance_rank`'s docstring says "Stops at expert rank" but the code correctly stops at Master — stale docstring, fix in passing. `select_technique` itself needs no logic change (threshold flows through `advance_skill`); verify only.
- **Schema/back-compat:** `marks_per_rank: 3` becomes per-tier (map or list) and the caps need YAML expression as *counts* (e.g. `max_master: 1`, `max_beyond_practiced: 3`) so homebrew Facets with ≠5 skills inherit sane behavior. Follow the `endurance`→`resolve` precedent: accept the legacy integer with a `DeprecationWarning` for one cycle.
- **Existing characters:** Zahna, Mordai, Zulnut are early-career (nothing above Practiced); no migration. The `.fof` loader should still validate loaded characters against the caps for out-of-repo files.
- **Backgrounds:** starting skill at Practiced and the secondary skill's 1 recorded mark are below the cap line and cost line (Novice→Practiced stays 3 marks) — untouched by construction.
- **Magic arc intact:** levels 1/2/3 all reachable inside the primary Facet, so the magic-granting Background's spoken-for level 1 pick and a Tier 3 vertical (Archive for Mind, Communion for Soul) survive unchanged. Casters note: Mastering the casting skill (Attune or Lore, per D7) consumes the Facet's single Master slot — an intended identity choice, not a trap; Planner should confirm the Prismatic ladder remains satisfying at Expert (+2).
- **Endurance pools:** Body characters who leave Endurance at Practiced carry smaller pools than today's all-Master veterans. Recorded sim corpus used fixed starting PCs and is unaffected; veteran-tier encounter calibration is flagged for Planner as non-blocking.
- **MM pacing apparatus:** MM3–2/3/4 re-key entirely (career ceiling drops 45→27; "16+ veteran" band compresses). Add the RESEARCH §1 footnote — publish the fastest legal floor alongside the realistic range so the tables can't be beaten by an optimizer.
- **Digital-first holds:** the table-facing rule is two sentences plus one three-row table; the app tracks marks-to-next-rank and remaining Expert/Master slots per Facet, exactly the bookkeeping the toolset exists to absorb.

## Blast Radius

Rules source of truth, engine, and tests:
- `software/facets/base/facet.yaml` — `advancement:` block (per-tier marks, caps, `facet_level_threshold: 3`; comments citing DESIGN_v0.3 §6.2 rewritten)
- `software/app/facets/schema.py` — `AdvancementDef` (per-tier marks, cap fields, back-compat)
- `software/app/game/character.py` — `advance_skill`, `_try_advance_rank` (+ stale docstring), `select_technique` (verify only)
- `software/app/api/websocket.py` — `spend_skill_point` handler (surface cap-rejection messages)
- `software/tests/test_advancement_pacing.py` (primary), `test_character.py`, `test_facets_schema.py`, `test_facet_loading.py`, `test_fof_loader.py`, `tests/e2e/test_ui_flows.py`
- `software/tools/agentic_playtest/context.py` — advancement rules summary given to playtest agents

Player-facing app:
- `software/app/static/js/tools.js` — Skill Advancement card (per-tier costs, slots remaining)
- `software/app/static/js/builder.js`, `components.js`, `play.js` — rank/marks rendering (verify, likely light)

Books (same-commit propagation; quick refs compress, never restate):
- `player_handbook/II.4_Character_Creation_Facets.md` — *Advancing Skills* (new cost table), *Facet Levels* (threshold 3, counting example rewritten), both *Through the Mirror* boxes, *Major Advancement*, *Advancement at a Glance*, *Career Advances*
- `player_handbook/II.6_Character_Creation_Skills.md` — rank framing ("eventually Master" paragraph), Table II.6–2 pointer text
- `player_handbook/Quick_Start.md` — advancement mention
- `player_handbook/Glossary.md` — Mark, Rank, Facet Level, Master entries
- `player_handbook/Appendix_Character_Sheet.md` — mark track (max 8 boxes) and cap slots
- `player_handbook/Index.md`, `List_of_Tables.md` — **regenerate, never hand-edit**
- `mm_manual/MM3_Campaign_Design.md` — Tables MM3–2/3/4 + *Pacing Advancement Faster or Slower* + veteran-play reframe (A3)
- `mm_manual/MM5_Quick_Reference.md` — *Skill Advancement* block

Spec and records:
- `spec/types/ruleset.md`, `spec/types/campaign.md` — advancement field docs
- `docs/DECISIONS.md` — **user records the ruling; not written by this pipeline**

## Constraints and Open Questions Handed to Planner

Binding constraints (restated from above): Technique layer untouched; no new resources/tracks/per-session bookkeeping; concepts retained; magic-Background vertical reachable; no invented fiction; quick refs are compressions; all files in the blast radius move in the same cycle.

Open questions for the DESIGN:
1. **Cap enforcement semantics.** Exact `advance_skill` behavior at the wall (error message text, partial-spend handling when a mark purchase would cross into a forbidden rank), and whether the WebSocket handler refunds or refuses the SP.
2. **YAML shape.** Map vs list for per-tier marks; field names for the caps; deprecation mechanics for the legacy integer.
3. **MM3 table recompute.** Produce the new session-range tables from the A2 arithmetic (floor + realistic), including the fastest-legal-line footnote, and re-band career-advance benchmarks against the 27-advance ceiling.
4. **UI expression.** How the Skill Advancement card shows "2 of 3 beyond-Practiced slots used, Master slot free" without inventing jargon; whether the printable sheet needs cap checkboxes or the app alone carries it.
5. **Terminology.** The rule needs no new noun; confirm the books can state it plainly (recommend: no coined term — "at most three skills beyond Practiced, one of them Master").
6. **Training mark at completion.** Once the primary shape is finished the 1-per-session training mark has no legal primary target; confirm it simply idles (recommended) rather than extending to cross-Facet.
7. **Acceptance gates.** Update `test_advancement_pacing.py` to pin the new floors (2.25 / 5 / 9.5 sessions; 38 SP full shape; 27-advance career ceiling) and add a differentiation invariant (two maximal same-Facet builds can differ; no build exceeds 1M/2E per Facet). Define the post-change playtest that watches A4's veteran pacing and A3's revisit trigger.
8. **Prismatic/caster check.** Confirm the Prismatic ladder and Second Domain remain satisfying when the casting skill stops at Expert in builds that spend the Master slot elsewhere.

---

*Resolved at Brain tier. Return to **Planner (Opus)** to produce `docs/DESIGN_advancement_differentiation.md` and `docs/TASKS_advancement_differentiation.md` from this BRIEF — starting with open questions 1–2 (enforcement semantics and YAML shape), which gate the engine tasks.*
