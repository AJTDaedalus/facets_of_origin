# DESIGN — Fun & Ease-of-Play Fixes

**Date:** 2026-08-08
**Upstream:** `docs/RESEARCH_fun_ease_review.md` (synthesis) and its three cluster
reports (`RESEARCH_fun_review_core.md`, `RESEARCH_fun_review_combat.md`,
`RESEARCH_fun_review_progression.md`). Finding IDs below use `C-` (core), `K-`
(combat), `P-` (progression) prefixes against those reports' numbering.
**Scope:** implement fixes for all 40 findings. Where a report offered options, this
design settles one (rationale in §7). Three items are deliberately deferred (§8).
**Iron laws in force:** PHB change → `facets/base/facet.yaml` → engine → WebSocket →
tests, same cycle. Quick refs are compressions, never sources. Simulator drives
`app/game/combat.py` only. Generated files never hand-edited. TDD throughout.

---

## 1. Approach

Six workstreams, ordered so that **rules-text corrections that change no mechanics
land first** (they de-risk everything else), **mechanics changes that need
re-simulation land together** (one sim campaign, not four), and **app features land
last** (they encode rules that must be settled first). Each workstream is one feature
branch and one PR. Within a workstream, every commit that touches a rule carries its
facet.yaml/engine/test sync per the iron law.

```
WS-1 Text integrity      (no mechanic changes; kills drift)         → PR 1
WS-2 Rules unification   (Sparks, difficulty precedence, clocks)    → PR 2
WS-3 Combat mechanics    (rider merge, Withdrawn, enemy texture)    → PR 3 + sim campaign
WS-4 Magic & advancement (casting skill, ladders, points economy)   → PR 4 + sim spot-checks
WS-5 Apparatus & polish  (Quick Start, MM5, sheets, terminology)    → PR 5
WS-6 App features        (band display, Spark nudge, posture panel) → PR 6
```

WS-1/WS-2 are prerequisites for everything. WS-3 and WS-4 are independent of each
other. WS-5 depends on WS-2–4 (quick refs compress final text). WS-6 depends on WS-3
(band math) and WS-2 (Spark rules).

---

## 2. WS-1 — Text integrity (findings: K-1, P-15, K-11 partial)

Pure corrections to stale or false text. No rule changes, so no sim impact.

| # | Change | Files |
|---|---|---|
| 1.1 | Named-NPC bullet: "Resolve, Posture, Techniques" — delete "reactions, the works"; attack modifier described as authoring input; PCs react (K-1) | `player_handbook/III.3_Combat.md` |
| 1.2 | Delete `# same roll for Parry` comment from the `.fof` example; sweep MM1 for any other enemy-reaction remnant (K-1) | `mm_manual/MM1_Encounters_and_Enemies.md` |
| 1.3 | Fix the Defense line's false claim ("feeds the TR formula") ahead of its removal in WS-3 (K-11) | `mm_manual/MM1_Encounters_and_Enemies.md` |
| 1.4 | Supersession header on the stale advancement math (P-15): "RESOLVED figures superseded by shipped II.4 (5/10/15 thresholds, flat 2-point cross-Facet)" | `research/advancement_priority_questions.md` |
| 1.5 | Fix MM1 §Mooks' false "arrive worn down" claim: teach the true mechanism — Tier 1 chip degrades reactions against simultaneous Named Tier 2s; Absorb spends nothing (K §4.3) | `mm_manual/MM1_Encounters_and_Enemies.md` |

**Tests:** existing docs-consistency suite must stay green; add a grep-style invariant
(extend `software/tests/test_docs_consistency.py`) asserting the strings "same roll
for Parry" and "reactions, the works" do not reappear in III.3/MM1 — cheap drift
insurance for the exact regression that already happened once.

---

## 3. WS-2 — Rules unification (findings: C-2, C-3, C-4, C-5, C-7, C-9, K-8, P-1, P-9)

The two overloaded joints (Sparks, difficulty relabeling) plus small standing-ruling
clarifications. These are the highest-leverage sentences in the project.

### 3.1 The Spark economy — one home, three rules (C-2, P-1, P-9)

New canonical text in III.1 §Sparks (magic-specific sentence lives in II.3 but only
*restates* — II.3 becomes a compression per the quick-ref law):

1. **Reset:** "Sparks do not carry over. You start every session with 3." (settles
   the hoarding ambiguity in the anti-hoarding direction — unspent Sparks are wasted
   Sparks.)
2. **Dice:** "A Spark improves the dice: +1d6, drop the lowest. Works on any roll,
   including every magic roll." (Explicitly legal on Broad-domain rolls — this
   sentence replaces the misreadable ceiling wording, see 5.2.)
3. **Reach (magic only):** "A Spark buys reach in exactly two cases: pre-Technique,
   one Significant-scope attempt; Focused domains, one difficulty step off a Major
   working." The "Pushing scope" paragraph (un-executable, P-1) is **deleted** — no
   scope tier exists beyond Major, so no rule may reference one.

### 3.2 Difficulty precedence — one printed rule (C-3, C-4, K-8)

New paragraph in III.1 §Difficulty, compressed onto the MM5 combat card:

> "Set the base difficulty from the situation. An **Easy tag** (a rider Condition, a
> Maneuver) overrides the base downward — it does not stack with itself. Then **at
> most one step** from all character abilities combined — Technique, Specialty,
> anything future — may shift the result, whichever single source the player picks.
> Support's step applies after that. Easy is the floor; Very Hard is the ceiling."

Consequences:
- **C-4 settled:** Specialty and Technique steps share one cap; a Hard roll can reach
  Standard via either, never Easy via both.
- **K-8 settled:** absolute tags override; relative steps shift; saturation at the
  ladder ends is explicit.
- **C-3 settled:** the Technique trigger taxonomy (auto-apply vs self-declare,
  ordering) **moves out of III.1** into II.4 §Reading the Entries, where Techniques
  are defined. III.1 keeps the one-sentence version. The digital roller auto-applies
  carried triggers.

**Engine:** difficulty resolution in `app/game/engine.py` must implement this exact
order (base → tag override → single character step → Support step → clamp) and treat
Specialty and Technique as one step pool. `facet.yaml` gains nothing new; the
Specialty definition text updates in II.5.

### 3.3 Standing-ruling clarifications (C-5, C-7, C-9)

- **Group rolls vs Threat Clocks (C-5):** one sentence in III.2 §Hazards: "A group
  roll advances a Threat Clock at most once, keyed to the group's overall result."
- **7–9 sequencing (C-7):** adopt **narration sequencing**, not the decline-offer:
  "the MM names the cost before narrating the success." Rationale §7-D3.
- **Fixed pairs principle (C-9):** one sentence in II.6 §Using Skills: "Skill–attribute
  pairs are fixed except where a rule explicitly says otherwise; the Strike is the
  named exception."

**Tests:** engine tests for the precedence order (≥3: tag-overrides-base,
two-sources-one-step, ladder clamp), Spark session-reset lifecycle test, Spark
eligibility tests (pre-Technique Significant purchase; Focused Major ease; Broad
dice-Spark legal / reach-Spark absent).

---

## 4. WS-3 — Combat mechanics (findings: K-2, K-3, K-4, K-5, K-6, K-7, K-9, K-10, K-12, K-13) + sim campaign

### 4.1 The rider merge — "Open" (K-6, part of K-12)

On a 10+ Strike **against an enemy**, the attacker may leave it **Open**: Easy to
Strike for everyone until it recovers. The player narrates what Open looks like
(staggered, cornered, blinded, disarmed) — fiction keeps the variety, mechanics keep
the one real choice. The five-option Condition menu vs enemies is removed; PC-vs-PC
Strikes keep the existing tier outcomes unchanged.

- **Enemy-side clear (K-12):** "An enemy clears Open only by spending its action doing
  so — visibly." This is the MM's legitimate anti-snowball move, and the players can
  see and answer it.
- **Schema:** enemy `tier1_immunity` retires (it was immunity to nothing); `.fof`
  loader accepts it with a deprecation warning, same pattern as `endurance`. The
  Archive Guardian's Reduced Mode re-expresses its phase behavior without it.
- **Bestiary:** regenerating stat blocks via `software/tools/build_bestiary.py` is
  mandatory in the same commit — never hand-edit.

### 4.2 Withdrawn cycling — the uncontested-exchange rule (K-2)

New scene-level rule in III.3 (and MM5 card): "An **uncontested exchange** — no PC
took an offensive action — lets the situation advance for free: the MM may reposition,
reinforce, progress a clock, or take the objective, no roll." Withdrawn's recovery
becomes "recover 2 Endurance, up to your pool." This converts the loop into the tempo
trade the existing MM Note already claims it is, with zero per-character bookkeeping.
MM1 additionally states: Mook-only encounters must carry a clock or objective,
because pure attrition cannot lose (sim-proven).

### 4.3 Encounter dial honesty (K-3, K-5)

- **Cut** Table MM1-5 (TR budget ×1–×4) and Table MM1-6 (action-economy multipliers)
  and their MM5 compressions. TR itself stays (per-enemy build/ordering number); the
  Recipe Table and actor-count rule stay. The budget math and its 40 lines of caveats
  move to `docs/DECISIONS.md` as a historical record with the Series 9 citation.
- **Add** the sharpest sentence in MM1 §Five-Minute Method: "Adding enemies mid-fight
  is the sharpest dial you own — one Mook is one difficulty band (76% → 47% → 20%)."
- App-side live band display is WS-6.

### 4.4 Enemy threat texture (K-4, K-9, K-10)

- **Conduct-field postures:** Named/Boss postures become rule-driven via `triggers:`
  in the `.fof` conduct fields (e.g., "Aggressive while X; Defensive once Open").
  The enemy-side blind-reveal ceremony is dropped — the MM states enemy stance;
  PC-side blind declaration stays (it is load-bearing for the simultaneity feel).
  Insight pre-read (III.3 MM Note) is named as the counter-tool.
- **Three worked enemy Techniques in MM1** (mechanical templates, setting-agnostic):
  (a) a Tier-1 flurry hitting multiple PCs in one action; (b) a telegraphed
  finisher that repeats a Condition type the target already carries (see 4.5);
  (c) an attack that drains Endurance instead of landing a Condition. Each gets a
  stat-block-ready `techniques:` entry and one usage paragraph.
- One of the three example enemies (`enemies/*.fof`) is updated to carry a posture
  trigger and one of the new Techniques, so the pattern has a canonical instance.

### 4.5 Incoming-Condition selection (K-7)

One sentence in III.3 §Incoming Condition Tier and the MM5 card: "The MM chooses the
incoming Condition. Repeating a type the character already carries is how an enemy
deliberately finishes someone — telegraph it." The hidden lethality knob becomes a
visible dramatic beat.

### 4.6 Small combat items

- `defense_modifier` removed from the MM1 minimal stat block and the TR authoring
  path; loader deprecation warning; TR formula untouched (K-11).
- Paper fallback sidebar (K-13): armor = N checkboxes per scene; first-reaction flag =
  flip a token, clear at exchange end. Two sentences.
- MM5 additions (K-12): Intercept once-per-exchange + "the protected ally decides who
  steps in" on the reaction card.

### 4.7 Sim campaign (one pass, after 4.1–4.4 land in `combat.py`)

Re-run Series 9 Part D recipe rows (3 seeds × 200 iterations per row) under: rider
merge, uncontested-exchange rule, posture triggers. Acceptance: Skirmish/Standard/
Hard/Deadly bands hold within ±10pp of current published win rates; the A5
Withdrawn-cycling scenario (15 Mooks) drops from 98% win to a finite loss/stall rate
via the escalation rule; boss-fight median stays 2–4 exchanges. If a recipe row moves
a band, the Recipe Table updates in the same PR — the table is measured, and stays
measured. Results appended to `research/simulation_log.md`.

---

## 5. WS-4 — Magic & advancement (findings: P-2, P-3, P-4, P-5, P-6, P-7, P-8, C-8, C-10, C-12) + sim spot-checks

### 5.1 Casting rolls take a skill (P-2) — **the one open canon question, see §9**

Ruling adopted: **a casting roll adds the skill your tradition trains**, giving
casters the same +0→+4 arc as everyone else. Proposed mapping — Channeling (Soul) →
Attune; Resonance (Mind) → Lore — **requires user confirmation** before
implementation (it touches canon naming; the Iron Law forbids inventing it).
Once confirmed: one sentence in II.3 §Rolling Magic, both worked examples re-rolled
with the skill shown, `facet.yaml` magic def updated, engine casting path adds the
rank, character files (`Zahna.fof`) re-checked, API tests updated.

### 5.2 The Broad ladder and its ceiling (P-3)

With skills-apply landing, the Broad table's numbers stay **unchanged** (Hard/VH/VH)
— reliability now grows with advancement, which was the actual hole. The
"cannot be pushed beyond Very Hard, including Sparks" sentence is rewritten to say
only what it means: "Reach-Sparks cannot move a Broad working's difficulty;
dice-Sparks work normally" (dovetails with 3.1's rule 2). The frustration read
("Sparks don't work here") dies without moving a number.

### 5.3 Second Domain penalty expires (P-7)

The one-step penalty on the second domain **lifts at the character's next Facet
level** after acquiring it — Second Domain becomes an arc, not a permanent tax. One
sentence at the Technique entry (II.4b/II.4c), `facet.yaml` technique def gains the
expiry, engine difficulty calc honors it, plus a Choose:-field note that Focused
picks suffer the penalty least while it lasts.

### 5.4 Skill-point economy (P-5) and Facet-level counting (P-6)

- "Unspent points are lost" is **deleted**; a character may bank up to 2 points
  across sessions, and 1 of the 4 session points may go to an unused Primary-Facet
  skill ("training between sessions"). Kills the forfeit sting and the
  shoehorned-Gamble incentive; the used-skills principle survives where it matters.
- One sentence in II.4 §Facet Levels: "Ranks granted at character creation count
  toward career advances but not toward Facet levels" (codifying what the Zulnut
  example already implies). `facet.yaml` advancement def + engine counters synced;
  `spend_skill_point` handler and tests updated for banking + training-mark.

### 5.5 Technique adjustments (P-4, P-8, and C-10/C-12 notes)

- **Never Surprised (P-8):** downshifted to warning-beat strength — "you always get a
  warning beat before an ambush, trap, or sudden threat lands; what you do with it is
  yours." The absolute auto-success version is removed. facet.yaml + II.4b text.
- **Mage's forced first pick (P-4):** owned in prose, not redesigned — one sentence
  at II.4's Technique introduction and II.5 §Magic and Backgrounds: "your first
  Technique is your formalization; your first free choice comes at Facet level 2."
- **Graceful Fail calibration (C-10):** one MM line in III.1 — what earns the confirm
  vs a restated failure, cross-referencing the II.2 vignette's award.
- **Clock janitor (C-12):** MM sidebar note in III.2 — rotate the winder, narrate the
  wind-back as vividly as any roll. No rules change.
- **Dump-stat note (C-8):** MM-facing sentence (MM1 or MM4): Luck and Spirit earn
  their points through MM-invoked rolls — call for them. Watch playtests for
  Luck-1/Spirit-1 monocultures before any rules response.

### 5.6 Sim spot-checks

Casting with skill rank changes magic success rates: spot-check a Focused and a
Broad caster at ranks 0/2/4 against the II.3 difficulty table and record the curves
in `research/simulation_log.md` (uses the shared rules module — no new
implementation). Acceptance: Minor-scope pre-Technique success stays in the
"succeeds at small magic from session one" range; Very Hard at Master rank lands
near the Practiced-at-Standard feel the benchmarks table promises.

---

## 6. WS-5 — Apparatus & polish (findings: C-1, C-6, C-11, P-10..P-14, cut-list; quick-ref recompression)

### 6.1 Quick Start (C-1) — the High

- Add a **Major Attributes line** (Body/Mind/Soul modifiers — three numbers) to each
  pregen block.
- Resolve the spell fork per pregen ("Zahna casts with Knowledge (+1)" — plus skill
  per 5.1 once confirmed).
- Replace QS-4's Postures/Conditions rows with a **five-line combat primer** (what an
  exchange is, what a reaction is, posture in one clause each) ending with "everything
  else: Chapter III.3 — the same 2d6 roll."
- Strip advancement metadata from pregens: "(Novice, 1 mark)", scope caveats,
  secondary-skill notes.

### 6.2 Terminology & sheets

- **Endurance collision (C-6):** minimum-touch resolution — the pool is printed
  **"Endurance Pool"** everywhere the pool is meant (III.3, sheets, QS, MM5, app
  labels, facet.yaml display name). No identifier rename in code/data (churn without
  player benefit); revisit a true rename only if playtests still show confusion.
- **One word for Prismatic (P-11):** "Prismatic" is the player-facing term; "Broad"
  survives only in the one definitional sentence in II.3. Tables II.3-2/3, Appendix,
  and both Tier 3 Technique entries updated.
- **Rating/modifier dual encoding (C-11):** every printed sheet and app view leads
  with the modifier; rating demoted to chargen bookkeeping. Character sheet appendix
  + app rendering.
- **Career Advances (P-13):** off the paper sheet (stays in `.fof` and app);
  benchmark Table II.4-3 moves to the MM Manual.
- **Weapon vocabulary join (P-14):** add a type column with examples to Table IV.1-1
  (longsword = standard / blades). No rule change.
- **II.3 signpost (P-12):** half-page "skip ahead unless your concept is magical"
  note at the chapter top; domain quick-reference tables consolidate in the Appendix.
- **Background duplicate pairs (P-10):** diverge one skill in one member of each pair
  (Road Guard/Dockworker, Guild Apprentice/Hedge Scholar) — **only** the skill slot,
  no new fiction invented; flagged for user eyes in PR review since it touches
  Background definitions.

### 6.3 Recompression

After WS-2–4 text settles: MM5 cards, Quick_Start QS-4, and in-chapter quick-ref
boxes re-derived from final body text (compressions, never sources). II.2's
duplicated outcome/difficulty tables reduce to one-sentence + pointer **only if**
the style invariants tolerate it — otherwise keep (teaching-order duplication is
defensible; this is the one soft item in the cut list).

**Tests:** regenerate Index/List_of_Tables/List_of_Boxes; full docs-consistency +
style invariant suite (INV-9..15) green; the quick-ref compression rule audited
manually against the new MM5 cards.

---

## 7. WS-6 — App features (K-3, K-10, C-2 app-side, F13 app-side)

1. **Live encounter band** in the encounter builder: computed difficulty band
   (recipe-table-derived, actor-count logic) displayed as enemies are added; warning
   badge when a mid-combat spawn crosses a band. REST/WS: extends existing encounter
   endpoints; MM-only.
2. **Spark-flow nudge:** session-state tracks per-player Spark earn/spend timestamps;
   MM gets a quiet prompt when a player hasn't earned or spent in ~an act. WS event,
   MM-only display.
3. **Enemy posture panel:** posture field on the active-enemy tracker auto-labels the
   reaction difficulty players face (Table III.3-9) and the Strike difficulty hint;
   conduct-trigger text displayed next to it.
4. **Sheet/label updates** from WS-5: "Endurance Pool", modifier-first rendering,
   armor checkboxes on the printable sheet.

**Tests:** ≥3 per new handler/endpoint (happy, edge, error), per the coverage law.

---

## 8. Decision log (to append to `docs/DECISIONS.md` on adoption)

| # | Decision | Chosen over | Rationale |
|---|---|---|---|
| D1 | Sparks reset to 3 each session | carry-over / floor | Anti-hoarding lever; playtest-confirmed hoarding; unspent = wasted drives engagement |
| D2 | One-step cap unified across Techniques + Specialties + future sources | separate caps | Future-proofs the ladder; kills the read-carefully advantage |
| D3 | 7–9 = narration sequencing, no decline-offer | PbtA-style offer | 7–9 fires on ~46% of rolls; adding a decision point to the most common outcome taxes pace, and "never a dead end" already guarantees story motion. Revisit only on playtest evidence of feel-bad |
| D4 | Rider menu vs enemies → single "Open" tag | keep menu + honesty note | 4 of 5 options mechanically null vs non-rolling enemies; fiction keeps variety at zero rules cost |
| D5 | Withdrawn fixed via uncontested-exchange escalation | recovery nerf / pressure conditionals | Scene rule, applied once by the MM, no per-character bookkeeping; converts loop into tempo trade |
| D6 | TR budget + multiplier tables cut to DECISIONS.md | keep with caveats | Proven structurally non-predictive; tables outlive prose; Recipe Table already does the job |
| D7 | Casting adds tradition skill | attribute-only | Gives mages the fighter's +0→+4 arc; the research names attribute-only's failure explicitly; rehabilitates Broad ladder and Second Domain without touching tables |
| D8 | Broad ladder numbers unchanged; ceiling sentence rewritten as reach-only | soften to Hard/Hard/VH | Skills-apply restores growth; identity ("grandest effects are desperate rolls") kept; misread killed |
| D9 | Second Domain penalty expires at next Facet level | permanent + label | Arc beats tax; permanent difficulty taxes on defining traits are the documented feel-bad shape |
| D10 | Bank ≤2 points + 1 training mark to unused skill | forfeit as-is | The banked-pool abuse cannot occur at 4/session; forfeit's only output is its own example's feel-bad |
| D11 | Never Surprised → warning beat | absolute at higher tier | Preserves the fantasy at full strength; returns a scene genre to the MM |
| D12 | Enemy blind posture reveal dropped; conduct triggers instead | keep ceremony | A ritual that never surprises is pure overhead; rule-driven postures are cheaper and more readable |
| D13 | "Endurance Pool" print qualifier, no identifier rename | full rename | Full rename churns code/data/YAML for the same table clarity; revisit on playtest evidence |
| D14 | Prismatic is the player-facing term | Broad | The evocative word wins the player-facing slot; Broad stays as the one-line type definition |

## 9. Open questions (block only their own tasks)

1. **Casting-skill mapping (blocks 5.1 only):** Channeling → Attune, Resonance →
   Lore — confirm or correct. This is a canon naming decision the Iron Law reserves
   to you.
2. **Background pair divergence (blocks the P-10 task only):** which member of each
   duplicate pair changes its skill slot, and to what — proposal to be shown as a
   diff in PR review, not invented silently.
3. **II.2 duplicated tables (soft):** cut to pointer or keep as teaching-order
   duplication — default is keep unless you say cut.

## 10. Deferred (explicitly out of scope, with reasons)

- **Perform skill merge (C cut-list #6):** wait for playtest data (does Perform get
  rolled?) — a rules change touching Backgrounds and facet.yaml on no evidence yet.
- **Defensive posture removal (K cut-list):** keep, watch; re-examine if playtests
  show it unpicked.
- **Luck/Spirit roll-surface widening (C-8):** MM-note only now; mechanics response
  only if the dump-stat monoculture materializes.

## 11. Test strategy summary

- **Engine (TDD, red-green):** difficulty precedence order; Spark lifecycle +
  eligibility; casting skill rank; Second Domain expiry; banking/training-mark
  advancement; Open tag lifecycle + enemy clear action; uncontested-exchange
  escalation hook; deprecation warnings (`tier1_immunity`, `defense_modifier`).
  ≥3 tests per public function touched.
- **Sim (shared rules module only):** WS-3 campaign (§4.7) with published acceptance
  bands; WS-4 casting curves (§5.6). Results into `research/simulation_log.md`.
- **Docs invariants:** full `test_docs_consistency.py` + INV-9..15 suite green on
  every PR; new anti-drift greps (§2); regenerated files rebuilt, never edited.
- **Quick-ref audit:** manual pass confirming MM5/QS-4 introduce no wording absent
  from body text.

## 12. Risks

- **R1 — Sim shifts recipe bands (WS-3).** The rider merge and escalation rule touch
  measured numbers. Mitigation: acceptance bands in §4.7; the Recipe Table updates in
  the same PR if a row moves — the table's honesty is the asset being protected.
- **R2 — Casting-skill change alters magic feel.** Mitigation: §5.6 curves reviewed
  before the PHB text merges; pre-Technique Minor success rate is the guarded number.
- **R3 — Scope creep via polish.** WS-5 is a long tail of small edits; the workstream
  is capped to the enumerated findings — anything new found en route goes to
  `docs/TODO.md`, not into the branch.
- **R4 — Cross-branch drift.** WS-3 and WS-4 both touch engine + facet.yaml.
  Mitigation: land WS-3 before WS-4 begins engine work, or rebase WS-4 on WS-3's
  merge; never parallel-edit `engine.py` difficulty code.

---

**Next step:** decompose into `docs/TASKS_fun_ease_fixes.md` (atomic 5–30 min tasks
with acceptance criteria) — Planner work, or I can generate it on request. Open
question §9.1 should be answered before WS-4 task execution reaches 5.1.
