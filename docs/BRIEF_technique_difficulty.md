# BRIEF — Techniques and the Difficulty Ladder

**Tier:** Brain (Fable). **Input:** `docs/LOG_style_audit.md`, `## ESCALATION — Planner → Brain (2026-08-02)`.
**Scope:** three rules questions surfaced by the `**Normal:**` field pass on all 57 Techniques. All three concern how a Technique's printed exception interacts with a baseline rule that is stated absolutely.

---

## Problem statement

Adding a `Normal:` line to every Technique required stating the baseline each one departs from. Three baselines turned out not to exist in the text:

1. Whether a Technique's "one difficulty step easier" composes with the MM's situational difficulty call (Q1).
2. Whether *Second Domain*'s one-step penalty stacks onto the Broad table when a character also holds *Ascendant Domain* (Q2).
3. Whether *The Final Blow* is subject to III.3's absolute "riders never defeat an enemy on their own" (Q3).

Each has two or more individually defensible readings that produce different numbers at the table. The MM guide's own house standard (`style/STYLE_GUIDE.md:56` — discretion is delegated "with a default, a dial, and a guardrail") is currently unmet for all three.

**Motivation for answering now, together:** all three are instances of one underlying question — *when a Technique states an exception, what does it compose with, and what does it override?* Answering them piecemeal invites the same silent divergence that invalidated the pre-v0.3 simulation corpus. Answering them once gives every future Technique a template.

## Goals

- A table-usable ruling for each question: default, dial where warranted, guardrail. No arithmetic beyond "move one label."
- Rulings that leave the Series 7/9 simulation corpus (`research/simulation_log.md`) and the MM1 Encounter Recipe Table valid as published.
- A composition doctrine that survives more Techniques, more Facets, and setting Facets without re-litigation.
- An implementation posture for each ruling: engine-enforced, UI-assisted, or MM-facing prose only.

## Non-goals

- Wording the PHB/MM prose (Planner/Worker work; the one-sentence homes are named below).
- Task decomposition, tests, or code.
- Redesigning any Technique's effect. All six step-easier Techniques and *The Final Blow* keep their printed effects; the rulings define composition, not content.
- The Pinnacle Technique framework (still an open blocker in `research/advancement_priority_questions.md`); Q3's doctrine is written so it will extend there, but that framework is not designed here.

---

## Q1 — Technique steps compose with the MM's situational call

**The question.** Six Techniques make qualifying rolls "one difficulty step easier" (*Weapon Mastery* II.4a:55, *Steady Hand* II.4a:135, *Acclimated* II.4a:201, *Field of Mastery* II.4b:195, *Pressure Point* II.4b:95, *The Uncanny Angle* II.4c:123). III.1 has the MM declare a difficulty label, moving at most one step from the benchmark and saying so out loud (III.1:62–84; the style guide's formulation is "one step, never two," `style/STYLE_GUIDE.md:56`). Nothing states whether the Technique's step sits inside that budget or on top of it.

### Options considered

- **(a) Inside the budget.** The Technique's step consumes the MM's one-step adjustment; net movement from Standard is at most one rung. Weapon Mastery against a Defensive opponent: Standard.
- **(b) On top, ordered, clamped.** The MM sets the situational label exactly as III.1 already instructs; the Technique then steps that label one easier; the four-rung ladder clamps. Weapon Mastery against a Defensive opponent: Hard (situational) → Standard (Technique).
- **(c) Free composition.** Every step-shaped effect (Techniques, Support, future sources) accumulates.

### Selected: (b), with a non-stacking guardrail on the character side

**Default.** Difficulty is resolved in two moves, in a fixed order: **the MM's call first, the character's step second.** The MM declares the situational label per III.1 — benchmark, moved at most one step, said out loud. Set-to-label effects that define the situation (a Tier 2 rider making a target Easy to Strike, III.3:140; a 10+ Maneuver, III.3 *Maneuver*) are part of that call, not additions to it. Then any character-side "one step easier" effect the fiction supports applies to the declared label. The ladder clamps at Easy and Very Hard — a step off the end is simply absorbed.

**Guardrail.** **Character-side steps never stack with each other.** A single roll benefits from at most one "one step easier" effect, whatever its source — Technique, Support's step option (III.3:173), or anything a future Facet prints. The player picks which if several apply. This is the exact shape of two guardrails already in canon: Support bonuses do not stack (III.3:175), and armor/reaction downgrades do not stack — "apply the greater reduction only" (III.3:410). Net result at any table: the MM moves one step, the character moves one step, never more. "One step, never two" remains true of the MM's own call, which is the sentence it was always about.

**Dial.** Applicability, not arithmetic. The MM's lever is whether the Technique's fictional trigger is met — the chosen weapon type is in hand, the work is precision-under-pressure, the hunch is genuinely an impulse (*The Uncanny Angle* already says "The MM decides whether you are acting on instinct or strategy," II.4c:123). Once it applies, the step is automatic and fixed.

### Why (b)

1. **It is already the printed play pattern.** III.3's extended example rules it in so many words: "Standard difficulty, but Weapon Mastery makes this one step easier, so Easy" (III.3:513) — the Technique applied *after* the base was set. And the three one-step shifts implemented in `combat.py` (`maneuver_target_difficulty`, `enemy_posture_reaction_difficulty`, `target_strike_difficulty`, per the escalation's engine facts) are all single, non-composing shifts applied off a base label — (b) makes book and engine one doctrine.
2. **Option (a) makes Tier 1 signatures evaporate exactly when they should matter.** Under (a), Weapon Mastery does nothing whenever the MM applies any hardship — the Technique's value would depend on the MM's difficulty call, which is feel-bad, litigable mid-scene, and contradicts the players-feel-competent register. It also makes Support's step option (identical wording) useless against any adjusted difficulty, which cannot be intended.
3. **Option (c) is arithmetic at the table and compounds as content grows.** More Facets means more step sources; free stacking trends every specialist roll toward Easy and re-opens calibration with every supplement. The non-stacking guardrail caps the system's total drift at one rung forever, regardless of how many Techniques ship. This is the robustness argument from `research/dice_system_analysis.md:34` (modifier calculation ejects players from the fiction) and :43 (on 2d6, each ±1 is heavy — the reason PbtA-family modifiers must stay small and few).
4. **Order is decidable and benign.** Clamping means opposite-direction steps only fail to commute at the ladder's ends (escalation fact 4). Fixing the order — situation first, character step last — resolves it, and since all six Technique steps are easier-direction, the only clamp interaction is at Easy, where the Technique harmlessly fizzles into an already-favorable position.

### Downstream robustness (Q1)

- **Simulation corpus: intact.** Series 7 and 9 ran `standard_party()`, which carries no step-easier Technique (skill modifiers only; `tools/combat_sim.py:973–981`). The ruling changes nothing the simulator models: base Strike difficulty stays Standard, rider→Easy stays a set. No recalibration required.
- **Calibration honesty note (hand to Planner):** the Recipe Table is calibrated for baseline parties. A party where every front-liner strikes one step easier runs the table roughly a band hot — that was already true under any reading of Q1, because it is Technique power, not composition. MM1 gets one advisory sentence; the corpus's claims are unchanged.
- **More content:** the guardrail is source-agnostic by construction ("at most one character-side step, whatever its source"), so new Facets and setting Facets inherit it without new rules text.
- **If a table house-rules it away:** allowing stacking is a pure buff with a known bound (Easy floor); the ladder clamps, so nothing breaks mechanically — fights just run easier than the Recipe Table predicts. Acceptable failure mode; the MM1 note covers it implicitly.

---

## Q2 — The Second Domain penalty rides the Technique, not the domain count

**The question.** *Second Domain* prices its granted domain "one difficulty step harder" (II.4b:259, II.4c:237). *Ascendant Domain* prices its prismatic territory off the Broad table — Hard / Very Hard / Very Hard, Major ceiling unmovable by Sparks (II.4b:271, II.4c:249; II.3:85, II.3:184). A character holding both Techniques has no written answer for workings in the prismatic domain: is it "a second domain," and therefore one step harder on top of the Broad table?

### Options considered

- **(a) Stack.** Any non-primary domain takes the step: prismatic Minor becomes Very Hard; Significant and Major clamp at Very Hard (no visible change).
- **(b) No stack.** The one-step penalty is a property of the domain *granted by the Second Domain Technique*, priced on that domain's own table. Ascendant Domain's territory prices off the Broad table alone — the Broad table *is* the price of breadth.

### Selected: (b)

**Default.** A character's domains are priced by their grant route: the primary domain on its own type's table; the *Second Domain* grant on its own table, one step harder; the *Ascendant Domain* grant on the Broad table, with no additional step. Nothing in the system ever stacks a difficulty step onto the Broad table. Spark rules are untouched: dice-improvement Sparks work everywhere, and the Broad Major ceiling never moves (II.3:184).

**Guardrail.** One prismatic territory per character, ever — already printed ("Ascendant Domain is taken once, however many Facet trees they eventually climb," II.4b:271/II.4c:249) — so "a second prismatic working" in the sense of a second prismatic *domain* has no route to exist. The composition question only ever arises in the one shape ruled on here.

**Dial.** None. This is a fixed price, and should be — magic difficulty is the one place the game runs on published tables rather than MM judgment (MM2's whole magic-adjudication chapter depends on that).

### Why (b)

1. **Stacking is a rule that mostly doesn't exist and hurts when it does.** Under (a), two of three scopes clamp invisibly at Very Hard — a printed penalty with no effect, the precise anti-pattern MM2 already warns MMs against creating ad hoc (MM2:495, on accidentally applying the combat floor twice). The one visible effect, Minor at Very Hard, prices a prismatic *cantrip* like the hardest acts in the game — punitive, anti-fun, and hostile to the Technique that Tier 3 characters paid most for.
2. **The Broad table already is the breadth surcharge.** II.3:85 frames it exactly so: "You trade reliability for range." Charging a second premium for the same breadth double-counts.
3. **The engine already implements (b), deliberately.** `character.py:100–106` keeps `ascendant_domain` apart from `secondary_magic_domain` precisely because "the routes cost" differently, and `character.py:408–409` documents it: "ascendant_domain — prismatic, Broad table, no step penalty; secondary_magic_domain — Second Domain, one step harder." `engine.py:330–338` penalizes only `secondary_magic_domain`. Ruling (b) ratifies working, tested code; ruling (a) re-opens engine, tests, and canon to install the anti-pattern in point 1.

**Latent wording defect, resolved in the same ruling:** *Second Domain*'s sentence "one difficulty step harder **than your primary domain**" (II.4b:259, II.4c:237) is anchored to the wrong table. Read literally, a Focused-primary character's second (standard) domain would price at Focused-table-plus-one — which equals the standard table, silently deleting the penalty. The engine's reading — the second domain's **own** table, one step harder — is the intended one and becomes canonical. The sentence in both chapters, `facet.yaml`'s roll text (`facet.yaml:830–833` and the Soul twin), and MM5:258 re-anchor to "one difficulty step harder than normal for that domain."

### Downstream robustness (Q2)

- **Simulation corpus: untouched.** Magic difficulty is not in the combat corpus.
- **More content:** "the penalty rides the grant route" scales cleanly — any future acquisition route (a setting Facet's third tradition, a Pinnacle grant) declares its own price on arrival instead of inheriting an ambient your-Nth-domain tax. That is also why (b) survives the Body-magic tradition landing later.
- **If a table house-rules it away:** stacking anyway is self-limiting (the clamp), and no engine invariant breaks — the app would simply show a different label than the MM announces, which the UI posture below avoids by making the app's label authoritative for domain rolls.

---

## Q3 — The Final Blow overrides; the rider rule is about riders

**The question.** *The Final Blow* (Might Tier 3, once per session): spend a Spark on a Combat roll, succeed, and the target "is removed from the conflict entirely — defeated, fled, or broken — regardless of any remaining resources or abilities they had" (II.4a:93–97). III.3:140 states absolutely: "Riders never defeat an enemy on their own — Resolve does that." Which sentence wins?

### Options considered

- **(a) Full override.** The removal is real, Resolve notwithstanding, against any target.
- **(b) Subordinate to the rider rule.** The Technique cannot remove a target with Resolve remaining.
- **(c) Boss carve-out.** Overrides against Mooks and Named NPCs; against a Boss it instead depletes Resolve to the next phase threshold, or by some large fixed amount.

### Selected: (a)

**Default.** *The Final Blow* is not a rider and is not governed by the rider rule. III.3:140 constrains **rider Conditions** — the free Tier 1/Tier 2 hitchhikers on a 10+ Strike — and remains absolutely true as written: a rider still never defeats. *The Final Blow* is a Technique whose entire effect is a licensed exception to Resolve depletion, and its `Normal:` field already marks the departure ("A Strike depletes Resolve, and riders never defeat an enemy on their own," II.4a:99). It works on any target, Bosses included: that is what a Tier 3 capstone is for, and the adventure register wants the payoff to be real when it lands. **No body text in III.3 changes.** The system's existing costs are the balance: Tier 3 gating, once per session, a Spark spent, a Combat roll that must succeed at whatever difficulty the fiction sets — an MM facing a fresh Boss will rightly be calling that roll Hard.

**Precision (Planner to word into the entry):** "succeed" means 7+. On a 7–9 the removal still happens — the partial's cost shapes the aftermath (what the removal costs, what it looks like, what it stirs up), never the removal itself. The three printed removal shapes — defeated, fled, or broken — are narrated under the table's usual division of labor and register: the blow is the player's, the aftermath is the MM's.

**Guardrail.** Once per session, one target, *this* conflict — all already printed. Plus one MM1 design note: build Boss encounters so that the party deleting the Boss is a *win*, not a broken script — phase material is forfeit the moment a capstone lands, and an encounter that cannot survive its Boss's early exit was over-scripted by MM3's own standards.

### Why (a)

1. **(b) makes the Technique a trap option.** Subordinated to the rider rule, *The Final Blow* does nothing a successful Strike doesn't already do — a once-per-session Tier 3 capstone with zero effect. Printing a dead capstone is the single worst outcome for the players-feel-competent pillar.
2. **(c) is arithmetic bolted to the game's most cinematic moment.** "Deplete to the phase threshold" requires the MM to consult a hidden number and announce a diminished result at the exact beat the table is leaning in. It converts a capstone into an asterisk. The protections it buys already exist as costs (above).
3. **The absolutist sentence survives untouched.** The clean doctrine — *the rider rule governs riders; Techniques that override a baseline say so in their own text, and their `Normal:` field marks it* — resolves the collision with zero churn to III.3, MM1, MM5, or the Glossary, all of which keep their "riders never defeat" lines truthfully. This is also the template Pinnacle Techniques will need: overrides are explicit, costed, frequency-capped, and marked at the site of the exception.

### Downstream robustness (Q3)

- **Simulation corpus: intact, with the same honesty note as Q1.** `standard_party()` carries no Techniques; Series 7's Guardian gate and Series 9's recipes are calibrated for baseline parties and remain valid as published. A Tier 3 party with *The Final Blow* deletes roughly one Named/Boss actor per session — and Series 9 proved actor count *is* the difficulty dial — so the MM1 advisory sentence ("recipes are calibrated for baseline parties; step-easier Strike Techniques and Tier 3 capstones run the table about a band hot") covers Q1 and Q3 in one line.
- **Engine invariant (P11):** every `resolve_current` mutation routes through `phase_crossed`. A Final Blow removal must therefore be implemented as an explicit **defeat event** through the canonical defeat path — never a `resolve_current = 0` write — so phase logic, logging, and any future sim series stay coherent, and capstone removals are distinguishable in transcripts.
- **More content:** future capstones inherit the doctrine, not the exception — each new override is licensed by its own entry and marked in its own `Normal:` field. Nothing accumulates.
- **If a table house-rules it away:** running (b) merely wastes one Technique slot at that table; nothing else depends on the override existing. Cheap to ignore, which is the right failure mode for a capstone.

---

## Implementation posture (direction, not tasks)

**Shared principle:** the engine keeps its current shape — the MM chooses a difficulty label; the engine never computes situational difficulty (escalation fact 2). What changes is that **character-side steps become data the digital layer can apply silently after the MM's label**, which is the bookkeeping-absorption lever working as designed.

- **Q1 — engine-assisted, MM-authoritative.** Add machine-readable step metadata to Technique definitions in `facet.yaml` (a `difficulty_step: easier` field plus an applicability descriptor). Mechanically-scoped Techniques (*Weapon Mastery*'s weapon type, *Steady Hand*, *Acclimated*'s hardship type, *Field of Mastery*'s field) can be auto-suggested by the client when their trigger data matches; fiction-scoped ones (*The Uncanny Angle*, *Pressure Point*) are a one-tap player toggle the MM sees. The server applies the step through the existing `_step_difficulty_easier` (engine.py:386) *after* the MM's label and **enforces the non-stacking guardrail** (at most one character-side step per roll). The roll banner shows both moves: "Hard (MM) → Standard (Weapon Mastery)." Prose home for the rule: III.1 *Difficulty* (the one legislative paragraph); III.3's Strike difficulty note and MM5 compress it per the quick-reference iron law.
- **Q2 — already engine-enforced; ratify and pin.** No engine change. Add tests pinning the two behaviors as canon (ascendant → Broad table, no step; secondary → own table, one step). One-sentence wording fix in II.4b, II.4c, both `facet.yaml` technique roll-texts, and MM5:258 ("harder than normal for that domain"), all in the same commit per the sync iron law.
- **Q3 — engine-enforced event, MM-confirmed in UI.** Mark the Technique in `facet.yaml` (an explicit override flag on the definition). The app offers the once-per-session action, tracks its use, requires MM confirmation, and resolves it as a defeat event through the canonical defeat path (P11 invariant). MM1 gets the encounter-design note and the shared calibration sentence.

## Constraints and open questions handed to Planner

1. **One legislative home per rule** (style law 2): Q1's composition paragraph lives in III.1 *Difficulty*; every quick ref that touches difficulty (III.3:128 area, MM5) compresses it in the same commit, per the "compressions, not paraphrases" iron law.
2. **The MM1 calibration sentence** (Q1+Q3 shared) is advisory prose, not a Recipe Table change. The corpus and the table stand as published; do not re-run Series 7/9 for these rulings. An *optional* Series 10 (baseline party + step-easier Strikes + capstone, to quantify "a band hot") is sanctioned if Planner wants the number, but nothing gates on it.
3. **Q2's wording fix touches five surfaces** (II.4b, II.4c, facet.yaml ×2 roll-texts, MM5:258) — one Worker task, one commit.
4. **Q3's entry gains the 7+ precision sentence**; check the `Normal:` field still reads true afterward. No III.3 change.
5. **Sim boundary reminder:** any Series 10 party flag must drive `combat.py` difficulty stepping through the shared module — the simulator may not carry its own copy of the Q1 guardrail.
6. **Open question (non-blocking, user's taste, surfaced not decided):** whether the client should *auto-apply* mechanically-scoped Technique steps by default or always require the one-tap confirm. Both respect the ruling; it is a UX-trust question about how much the app decides silently. Default to one-tap confirm until the user weighs in.

**Resolved. Return to Planner to continue from `docs/LOG_style_audit.md`: the three `Normal:`-pass open questions (Q1–Q3), now ruled; plan the prose, yaml, engine, and test tasks per the implementation posture above.**
