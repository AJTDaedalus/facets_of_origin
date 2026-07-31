# BRIEF — Completeness Audit Remediation

**Tier:** Brain (Fable) · **Date:** 2026-07-30
**Inputs:** `docs/RESEARCH_completeness_audit.md` (synthesis) + five detail reports (`docs/RESEARCH_audit_phb_creation.md`, `_phb_rules.md`, `_phb_apparatus.md`, `_mm_manual.md`, `_software_sync.md`)

## Problem statement

A five-pass completeness audit of the PHB, MM Manual, and PHB↔software sync on `main` found **81 findings (9 High / 37 Medium / 35 Low)**, plus a stale top-level `README.md` (audited separately after the user traced their original complaint to it: "27 domains across three traditions", "24 skills", "613 tests", "TR 1 Harbor Thug / TR 16 Guardian", "Two playtests" — all wrong against current canon). The materials read as complete but contain: claims-N-delivers-fewer enumerations, un-migrated v0.3 text, quick-reference rules with no canonical source, a character sheet that cannot run combat, a four-way TR contradiction, and a software layer that lags the PHB on ~14 mechanics. Left unfixed, these erode the project's core promise (rules never get in the way) and will invalidate future playtest data the way the earlier combat-sim divergence did.

## Goals

1. Every High and Medium finding resolved or explicitly ruled "as designed" with rationale recorded in `docs/DECISIONS.md`.
2. Canon single-sourcing restored: every rule stated in a quick ref, MM5, README, or `facet.yaml` traces to canonical body text; all propagation done same-commit per CLAUDE.md sync rules.
3. v0.3 migration completed everywhere (Magic-in-Combat → Resolve model; enemy-modifier semantics; superseded sim citations retired).
4. `facet.yaml` fully encodes all settled mechanics (the 12 Medium sync gaps); engine/tests updated where mechanics are player-interactive.
5. README factual claims regenerated from canon.
6. Low findings fixed opportunistically when touching the same file; otherwise logged, not chased.

## Non-goals

- **No new mechanics.** Nothing beyond what v0.3 already settled. Open design questions (Spark earning, Pinnacle framework, Body magic tradition) stay open.
- **No Body-tree magic Techniques.** Body magic remains deferred to setting content; the fix is wording, not new content (see D1).
- **No prose re-voicing.** Vignette fixes are surgical (numbers, names, one-line grounding), preserving the human voice per standing feedback.
- **No index/glossary feature expansion** beyond correcting the slugger bug, adding the missing terms named in findings, and regenerating.
- README stays a summary — no auto-generation tooling for it in this cycle.

## Approach

**Four sequenced waves, one feature branch + PR each.** Chosen over one mega-branch (unreviewable, high canon risk) and over per-finding micro-PRs (81 findings; overhead swamps value). Waves order by dependency: wording fixes can't precede the canon decisions they encode, and yaml encoding can't precede the body text it mirrors.

- **Wave 1 — mechanical corrections** (no canon judgment): the "each Facet's tree" wordings (II.3:246, Glossary:90), II.2:102 point-buy math, Soul Second Domain prereq line, MM5 Maneuver direction, Named-NPC rider tier, Zulnut/Scholar/Lore vignette errors, Threat Clock vignette + pacing math, glossary citation fixes, Index slugger fix (`build_index.py:110–113`) + regenerate, README factual claims, Low fixes in touched files.
- **Wave 2 — v0.3 migration completion**: III.3 Magic-in-Combat and Attune → Resolve model (MM5 already states it; body text lags); MM1 enemy Attack/Defense modifier table-side meaning reconciled with "NPCs do not roll"; superseded v0.2 sim citations retired (MM1:411, MM2:165, veteran_soldier notes); Mook TR contradiction resolved per D2; `facet.yaml` Overwhelming Force + prerequisite model (H8/H9) with tests.
- **Wave 3 — canon-decision items** (decisions D7–D12 below): Guild Apprentice Specialty, character sheet + II.1 spec amendment, canonical homes for MM5 orphan rules, pushing-scope rule, Reckless Press, Shattered Origin promise in I_Introduction, MM magic-adjudication + Specialty/hazard/death coverage.
- **Wave 4 — sync backlog**: encode the 12 Medium yaml gaps per the Software-PHB Sync workflow; engine + WebSocket + tests for player-interactive ones; Press cost moved from `websocket.py:528` hardcode into yaml.

TDD throughout; every rules change updates body text + every touching quick ref + yaml + engine in the same commit (existing iron rule). Each wave's PR description lists the finding IDs it closes.

## Decisions taken at this tier

- **D1 — "each Facet's tree" → "the Mind and Soul trees."** Fix the claim, don't add Body magic Techniques. Body magic deferral is settled design; the sentence is simply wrong. (Closes H2/H3.)
- **D2 — Mook TR: the formula wins; a +0-attack Mook is TR 2.** `harbor_thug.fof`'s computed `tr: 2` is correct; MM1's three "TR 1" claims and the .fof's own "TR 1 minimum" note are the errors; chicken (attack −1 → TR 1) remains the canonical TR-1 baseline. Rationale: the formula is sim-calibrated and load-bearing (encounter recipes, budget tooling); redefining the floor semantics to rescue three prose claims has far larger blast radius. (Closes H7 + README TR claim.)
- **D3 — MM5 orphan rules get canonical homes, not deletion.** Trouble Table + "unnarrated details" + "try again" are good rules the Index already treats as real; write them into canonical body text (III.1 for the two rulings; MM2 or MM1 for the Trouble Table — Planner picks the section) and let MM5 compress them. Exception: if the user rejects any as non-canon, it is deleted from MM5 instead. (Closes MM-M3.)
- **D4 — Guild Apprentice adopts the Quick Start Specialty** ("Artificers' Guild technical records — Standard becomes Easy when directly applicable"). This is already user-established text in the repo, so it is propagation, not invention. (Closes rules-H1.)
- **D5 — 0-Endurance rule: "Absorb only" is absolute.** At 0 Endurance only Absorb is available regardless of posture; Withdrawn/Defensive cost reductions apply only while Endurance ≥ 1. Rationale: preserves 0-Endurance as a real floor state (the design explicitly replaced depletion tiers with this single threshold); the alternative (free reactions still work) makes Withdrawn erase the floor entirely. Body text gets one clarifying sentence; quick refs follow. (Closes rules-M1.)
- **D6 — Reckless Press is cut.** It is used once (III.3:395), defined nowhere, and indistinguishable from an ordinary Spark spend; the Gamble entry is rewritten to reference the plain Spark rule. Minimize-mechanics philosophy: a named mechanic must earn its name.
- **D7 — Character sheet: full amendment.** II.1's section spec gains a **Combat** block (Endurance pool + formula, Armor type/downgrade budget, Conditions track, Sparks moves there from Session Resources), a **Magic Domain** field (name, type, pre-Technique Minor-only flag), an **Inventory** section, and a **Career Advances** counter. The appendix follows the amended spec. Rationale: the sheet must carry III.3's "five numbers on screen" and the book's own progression metric, and every pre-gen (Zahna) must be transcribable onto it. (Closes apparatus H1/H2, M1–M4.)
- **D8 — "Pushing scope" is redefined against the one ceiling that exists: the pre-Technique Minor cap.** New rule: a pre-Technique caster may spend a Spark to attempt a single **Significant**-scope effect at their domain's normal Significant difficulty; the Technique remains the only path to routine full scope and to Major. Rationale: this is the only reading with a real referent; it preserves the settled "Sparks as scope fuel" intent, gives pre-Technique casters an earned dramatic moment (consistent with the 2026-03-13 playtest softening), and keeps the Tier 1 Technique clearly worth taking. Existing companions unchanged: Focused-domains-Spark-to-ease-Major stays; Broad's hard ceiling stays. Encode in yaml/engine in Wave 4. (Closes creation-M3.)
- **D9 — I_Introduction's Shattered Origin promise: both fixes.** Soften the sentence (the handbook is *set in* Shattered Origin; the full setting Facet is forthcoming) **and** add "Shattered Origin (setting Facet)" to the ToC's planned-modules list, giving II.3's Body-magic deferral a ToC destination. (Closes apparatus-M7.)
- **D10 — MM magic adjudication lives in MM2 as a new top-level section** ("Adjudicating Magic": scope classification, domain boundary calls with the "lean toward yes" posture, designing 7–9 complications, active-opposition difficulty), compressed into MM5 afterward. No new MM chapter — the manual's five-chapter shape holds, and adjudication is scene-running, MM2's territory. Companion coverage fixes: Specialty ruling added to MM5 Common Rulings (compressing II.5's canonical rule), MM2 session-design gains Hazard/Threat Clock pointers to III.2, MM4's safety section points at III.2's death choice, and Pinnacle-approval guidance stays deferred (open blocker, out of scope per Non-goals). All new prose drafts go to the user for voice review before merge. (Closes MM-M6, MM-L9.)
- **D11 — Wave 4 depth is split by player-facing surface.** **Saving throws**: full implementation — yaml encoding + engine + WebSocket event + tests (it is a core III.1 mechanic with zero software presence). **Contested rolls**: yaml encoding only (the engine handler already exists; sync gap M-11 is encoding). **Group Rolls**: yaml encoding only, no engine work until a playtest demands it. Everything else in the Wave 4 list: encode in yaml and wire to the existing engine paths per the sync workflow.
- **D12 — Standing veto.** All of D1–D11 are Brain-tier calls made at the user's direction; the user retains veto at PR review, and any prose that states new canonical rule text (D3, D8, D10) is flagged in its PR description for explicit sign-off.

## Robustness considerations

- The Index slugger fix changes 33 anchors — regenerate `Index.md` in the same commit and keep `--check` green; add a slugger unit test pinning GitHub's double-hyphen behavior.
- Wave 2's yaml prerequisite-model change (H9) loosens validation; add tests asserting previously-rejected legal picks now pass *and* genuinely illegal picks still fail.
- Any TR or rules change re-runs the affected simulations via `app/game/combat.py` only (standing rule: the simulator never re-implements rules); superseded sim series stay labeled, never cited.
- README counts (tests, playtests, TRs) drift by nature — Wave 1 fixes them and adds a one-line comment in the README source marking them as derived-from-canon so future edits know to verify.

## Handoff

**Next tier: Planner (Opus).** All decisions are made (D1–D12); nothing blocks planning. Produce `DESIGN_audit_remediation.md` + `TASKS_audit_remediation.md` decomposing all four waves, in wave order. Finding IDs in the five detail reports are the task inventory; each task cites the finding ID(s) it closes and the decision(s) it implements.

**Resolved. Return to Planner (Opus) to produce DESIGN/TASKS from this brief.**
