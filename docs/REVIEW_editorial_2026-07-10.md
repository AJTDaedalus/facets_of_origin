# Editorial Review — Facets of Origin (v0.2, feature/data-driven-dice)

**Date:** 2026-07-10
**Scope:** PHB (all chapters), MM Manual (MM1–MM5), playtests 01–06 (including the 9-adventure agentic batch and the live unscripted session), open research files.
**Lens:** The stated ethos — maximize fun/socializing/worldbuilding/storytelling; minimize rules complexity, complicated mechanics, and gameplay friction.

---

## Verdict

The core of this game is genuinely good and the playtests prove it: the 2d6 three-tier engine, the posture/reaction combat loop, freeform Domain+Intent+Scope magic, and the Specialty/Background design all produce the play experience the ethos promises. Every playtest — scripted, live, expert, novice — praised the same things, and they're the right things.

But the game currently has **one load-bearing structural hole** (enemies have no coherent durability model, and every playtest table independently drifted back to hit points because of it), **one broken progression path** (Tier 3 Techniques are mathematically unreachable as written), and **a contradiction problem serious enough that it corrupted your own playtests** (the deleted pre-technique magic penalty survives in II.5 and was applied by the playtest-06 MMs, poisoning that data). For a game whose pitch is "you'll never dig through rules," internal contradictions are a first-order product defect: they *manufacture* rules-digging.

---

## What's Working — Keep and Protect

1. **The three-tier resolution engine is validated. Repeatedly.** ~50% of all rolls across playtests landed in 7–9, and both reports and agent quotes confirm partials are "the engine of the game's narrative drive." No playtest produced a dead-end roll. This is the heart of the game and it beats.

2. **Postures + reactions + Intercept is the best mechanical loop you have.** Independently praised in playtests 01, 02, and 06 ("Defensive posture felt amazing… I felt like an active guardian, not a passive target"; Kael's 4-Endurance Intercept called "the best moment of the session"). Simultaneous exchanges genuinely eliminated turn-waiting — novices stayed engaged. This is your marketing demo.

3. **Domain + Intent + Scope magic creates the moments the game is for.** Five distinct effects from two domains in playtest 01; the counter-frequency lateral solution in playtest 02; "vibrate the valves" in playtest 06. No "I cast Fireball" anywhere. The concept is validated — onboarding is the problem (see below).

4. **Backgrounds and Specialties punch far above their word count.** Specialty repeatedly delivered mechanical relevance from pure backstory (Kael's Watch protocols). The secondary-skill-with-one-mark design is elegant, cheap, and flavorful. The 15 pre-built Backgrounds are well-written and genuinely distinct.

5. **Character creation speed.** 10–15 minutes, confirmed three times, including a first-time TTRPG player. This is a real competitive advantage — protect it from feature creep.

6. **The vignettes are load-bearing pedagogy, not decoration.** The Thornwall thread (archive → keyring → lower archive → guardian) running across II.2/II.3/III.3 teaches the rules better than the rules text does, and the voice (the MM sighing at Zahna's cross-referencing, "Mordai was very loud") is the most distinctive writing in the book.

7. **"When Not to Roll" and MM-facing lateral-play guidance.** The three-conditions rule, the "MM must answer honestly" Technique designs (Sharp Analysis, Read the Room, Working Theory), and MM1's asymmetric-encounter section all enforce the ethos structurally rather than just aspirationally. The Mind/Soul Technique trees are quietly the most ethos-aligned content in the book — they mechanize *spotlight*, not damage.

---

## What's Broken — Structural (fix before anything else)

### 1. Enemies have no coherent durability model, and every table converts Endurance into HP

This is the single most important finding of the playtest corpus, and no report states it directly.

The rules as written:
- III.3 "Enemy Attacks": **"NPCs do not roll dice."**
- MM1 stat block: **"Defense: same modifier used for Parry"** — a Parry the NPC can apparently never roll.
- Named NPCs/Bosses have Endurance pools — but Endurance is only ever spent on reactions and Press, and NPCs roll neither. **Enemy Endurance has no rules function.** It exists only to feed the TR durability table and phase-change triggers ("when their Endurance is reduced past a threshold" — reduced by what? No rule reduces it).
- Meanwhile the actual enemy defeat mechanic — two Tier 2 Conditions = Broken — means any Named NPC or Boss falls to **two full-success Strikes**. Your own III.3 vignette demonstrates this: the fight "planned for three exchanges" ended in two.
- And light armor makes enemies **unbreakable** (Tier 2 → Tier 1 → clears each exchange → Broken is unreachable), which you've already documented in `research/armored_enemy_breaking_problem.md` and patched with the 0-Endurance house rule — a patch that only works if enemies spend Endurance, which per III.3 they never do.

The result, visible in every later playtest: **every MM — including your "Expert MM" persona — reinvented hit points.** The live unscripted session ran the TR 9 boss as "strike deals 2 damage, golem drops from 10 to 8 Endurance," complete with invented double-six crits. The agentic batch invented Nauseated, Confused, Singed, Scorched, and Deafened conditions and dealt direct Endurance damage. The two TPKs ("zero fun," "mathematically oppressive") happened inside this house-ruled HP system, not your actual rules. Nobody, in ten playtests, ran a Boss fight by the book — because the book's Boss fight is either two hits long or literally unwinnable, and it hands the MM a big Endurance number that begs to be used as HP.

**Recommendation:** Decide what enemy durability *is*, on purpose. Three honest options:

- **(a) Lean into conditions:** delete enemy Endurance entirely. Named NPCs have a condition track with N boxes (Named = 2 Tier 2 boxes, Boss = 3–4 + phase change at each box). Armor becomes "the first Tier 2 each scene/exchange downgrades" instead of "all of them" (kills the unbreakable-enemy bug). Cheapest change, most faithful to the ethos.
- **(b) Legitimize what every table already did:** give enemies a small Resolve/Integrity pool that Strikes deplete by tier (10+ = 2, 7–9 = 1), keep Conditions as *rider effects* the attacker picks. This is HP, honestly labeled and kept small (2–6). It matches observed play and makes phase-change thresholds finally mean something.
- **(c) Make enemies react** (roll or fixed-cost Endurance spends), restoring Endurance's function — but this adds MM dice-rolling you deliberately removed. I'd advise against; the PC-facing-rolls-only decision playtested well.

Either (a) or (b) is defensible. What's not defensible is the current text, which is (a)'s fiction stapled to (c)'s stat block and played as (b).

### 2. Tier 3 Techniques are mathematically unreachable

- 5 skills × 3 advances = 15 max advances per Facet → Facet level 2 is the ceiling in any single Facet (level 3 needs 18).
- One Technique per Facet level, drawn from *that Facet's* tree → **maximum two Techniques from any tree, ever.**
- Tier 3 requires a Tier 2 in the same branch, which consumes both of your picks — so you qualify for Tier 3 exactly when you can no longer take one.

Every Tier 3 Technique — The Vanishing, Fated, The Deduction, Hold the Line — is dead text. **Prismatic domains ("require a Tier 3 Technique") and Second Domain are unreachable.** Also note the compounding slowness: at 4 SP/session the first Major Advancement (4 total Facet levels) lands around **session 25–27**, so the II.2 promise that Minor Attributes "grow through play" is effectively false for any normal campaign.

**Recommendation:** Decouple Technique picks from Facet-of-the-level (any qualifying tree), or grant a Technique at 6/12 advances *and* at every 6 cross-Facet advances, or lower the level threshold (e.g., every 4 advances → levels 1/2/3 at 4/8/12, within the 15 cap). Then re-check the Major Advancement clock — first attribute bump should plausibly arrive by session ~10–12, not ~27.

### 3. There are no rules for hazards, ongoing threats, or PC death — so MMs invent bad ones

The two "zero fun" TPKs both came from MMs improvising per-exchange environmental damage because the book is silent on hazards. The book is also silent on what Broken means for *mortality* — III.3 gestures at "defeated, unconscious, fled, captured" but never states the death policy, so agent MMs defaulted to "0 Endurance = dead."

**Recommendation:**
- Adopt the **Threat Clock** proposal from `fun_and_consequence_review.md` (hazards advance a visible 4-segment clock on 7–9/6-, players can act to wind it back). It's telegraphed, interactive, uses your existing outcome tiers, and adds no new subsystem — very on-ethos.
- State the death rule in the PHB in one paragraph: Broken never kills by default; death enters the fiction only when the player accepts it (the **Doom Gate / heroic sacrifice** proposal is a strong, ethos-perfect version — death becomes a *choice* that buys an automatic legendary moment). "Death is a math problem" is the exact failure your ethos exists to prevent; close the door on it explicitly.

---

## The Contradiction Ledger — friction the game inflicts on itself

These aren't nitpicks; playtest 06 demonstrably ran on stale rules because of the first one. Every entry below is a moment where an MM stops the game to dig.

| # | Contradiction | Locations |
|---|---|---|
| 1 | **Pre-technique magic penalty.** II.5 still says Minor scope *and* one step harder; II.3 and MM5 say scope restriction only (the post-playtest-01 fix). Playtest 06's MMs applied the penalty — it was their "biggest cognitive bottleneck" and skewed a 50% magic failure rate. | II.5 (Magic and Backgrounds) vs II.3 "Acquiring a Domain" / MM5 |
| 2 | **What Broken takes.** Body text: second Tier 2 *of the same type* escalates ("Staggered and Cornered stack… genuine trouble"). III.3 quick ref and MM5: "2nd Tier 2 (same or different) = Broken." These produce different fight lengths. | III.3 body vs III.3 quick ref vs MM5 |
| 3 | **Heavy armor.** Armor section & IV.1: Tier 3→Tier 2 only. Enemy Attacks section: "heavy armor downgrades by two (Tier 3 becomes Tier 1)." Note also that under the strict reading, heavy armor does *nothing* against the Tier 2 hits that are 100% of enemy attacks — heavy armor is currently worse than light armor. | III.3 "Armor" vs III.3 "Enemy Attacks"; IV.1 |
| 4 | **Parry counter.** Body: Parry outcomes "same as Dodge." Both quick refs: "10+: deflect and counter (attacker takes T1)." | III.3 body vs III.3 quick ref & MM5 |
| 5 | **Weapon attributes.** IV.1: "Weapons determine which attribute you use for a Strike" (Dex for light/ranged). III.3 Strike: always Strength + Combat. And is a ranged Strike Combat or Finesse (II.6 puts ranged under Finesse)? Undefined. The engine already accepts any attribute/skill — the PHB should say so. | IV.1 vs III.3 vs II.6 |
| 6 | **PvP ties.** III.1: "both achieve partial success." MM5: "ties go to defender." | III.1 vs MM5 |
| 7 | **Character continuity.** II.3's extended example makes Zahna a *Fire* mage rolling *Spirit (3→+1)*, gendered "she" — canonically he's Inscription/Knowledge with Spirit 2. II.5's closing analysis gives Zulnut the *Street Performer* Background (he's Wandering Disciple; also "she" in II.4, "he" elsewhere). III.3's Endurance example gives Mordai Endurance Practiced (pool 6); his sheet and the Quick Start say Novice+1 mark (pool 5). | II.3, II.5, II.4, III.3, Quick Start, character files |
| 8 | **Ghost mechanics.** Intercept references "a Spent ally" — Spent was cut in the simplification. MM5 labels attribute 1 "Poor" vs "Weak" everywhere else. Maneuver's "the target's next roll is Easy" reads backwards (it means rolls *against* the target). MM1's phase-change trigger references Endurance reduction that no rule performs. | III.3, MM5, MM1 |

**Recommendation:** One consolidation pass with a single canonical answer per row, propagated to every file in the same commit (your own CLAUDE.md lore rule, applied to mechanics). Then adopt a rule for the repo: **quick references may never restate a rule differently — they compress, they don't paraphrase.** Rows 2–4 exist because a quick ref "improved" the rule in passing.

---

## Recurring Playtest Signals — real, but tuning rather than surgery

### Spark hoarding is behavioral and structural, and it's in every single playtest
Playtest 01: 2 of 9 spent. Playtest 02: 2 earned across 4 players in 3 hours. Playtest 06: "hoarding paralysis" named explicitly. MM5's guidance ("award 1–2 mid-session," midpoint diagnostic) is good but it's advice, and advice loses to loss-aversion every time. The pattern in every log: players spend Sparks *only after* watching someone else's Spark rescue a roll.

**Recommendation:** Make earning *structural, player-facing, and in the PHB* (not buried in MM5):
- Codify the **Act Break Nomination** (each player nominates another between acts; MM confirms) in III.1 — it's already designed and slated for PT04 testing.
- Make the **Graceful Fail player-initiated**: on any 6-, the player may lean in and *claim* it ("I make it worse: …"); MM confirms → Spark. Failure feeding the resource is the proven PbtA loop for killing hoarding, and it turns your best rule (6- always moves the story) into an economy.
- Playtest-06's proposed **Spark refund on failed magic casts** is worth testing for pre-technique casters specifically — it directly attacks "I wasted my safety net" trauma.

### Aggressive posture is a trap for the people most tempted by it
Batch data and expert review agree: +1 reaction cost on a 3–4 Endurance unarmored character means one Aggressive exchange can eat half your pool, while against Mooks (who threaten nothing individually) Aggressive is strictly optimal. So the posture is simultaneously a noob trap and an auto-pick, depending on enemy mix.
**Recommendation:** Cheapest fix: Aggressive's surcharge applies to the *first* reaction only, or is waived while at 3+ Endurance… test one knob. Also consider printing the intended pairing ("Aggressive wants a Defensive guardian nearby") as a one-line sidebar — playtests show the Alaric/Pippa pairing is the fun the mechanic wants to create.

### Freeform magic needs training wheels, not rules
"Spell list anxiety" appears in three separate documents with the same fix requested each time: **3–5 example intents per domain per scope** in the Domain Catalog (Resonance: *vibrate a lock / silence a room / shatter a wall*). The appendix's prose and "beyond this domain's focus" lists are excellent for boundaries but give a nervous novice nothing to *grab*. This is the highest-value, lowest-risk content addition in the backlog. Frame them explicitly as design patterns, not a menu — the moment they read as a spell list, you've lost the point. (Resist playtest-06's "pre-set spell packages" suggestion — that *is* a spell list.)

### The MM carries the cognitive load the players shed
The system's simplicity for players is partly purchased with MM improv: inventing every 7–9 complication, adjudicating every scope call, and (per Arthur, the novice-MM persona) freezing on 6- ("nothing happens" — the exact anti-pattern). III.1's partial/failure pattern lists are good; the novice MM needs them *at the table*.
**Recommendation:** Arthur's own ask is correct: a **Trouble Table** (d6-able generic consequences: cost / position / attention / equipment / condition / revelation) in MM5, plus the 6- magic templates from II.3 duplicated there. MM5 is currently a rules mirror; it should be an *improv prosthetic*.

---

## A Note on Playtest Data Quality

Weight playtests 01, 02, and the structured parts of 06 heavily — they're careful, quantified, and honest. Treat the agentic batch (adventures 2–10) as **directional only**: the roll logs show identical dice across different players in the same scene, modifier columns that don't match the stated stats, invented conditions, TR-2 "Named" enemies that violate your own TR minimums, and wholesale HP houseruling. Its *qualitative* signal (where agents drifted from RAW is where the rules are weakest) is the most valuable thing in it — that's a genuinely clever diagnostic — but none of its numbers should calibrate anything. The PT03/04/05 scenario designs (boss-to-completion, resource tax, technique showcase) are exactly the right next tests and appear not to have been run faithfully yet; PT03 in particular will be unrunnable until the enemy-durability question is answered, which is a nice forcing function.

---

## Priority Order

1. **Settle enemy durability** (structural §1) — everything combat-related is blocked behind it, including PT03.
2. **Fix the Technique/advancement math** (structural §2) — Tier 3, Prismatic, Second Domain, and Major Advancement pacing.
3. **Contradiction consolidation pass** (the ledger) — one commit, all files, including the II.5 pre-technique line.
4. **Codify Spark earning cadence in the PHB** and re-run a session to see if hoarding breaks.
5. **Threat Clocks + explicit death rule** — one page total, kills the entire "zero fun TPK" failure class.
6. **Domain example-intent tables** in the appendix.
7. **MM Trouble Table** in MM5.

None of this is a redesign. The engine, the postures, the magic framework, the Backgrounds, and the voice are all working — the playtests keep proving it. What's failing is the connective tissue: enemy math nobody finished, progression math nobody totaled, and five documents that answer the same question four ways. Fix the tissue and the game underneath is already the one the ethos describes.
