# BRIEF: Lean Facets v1.1, the strategic fixes

**Date:** 2026-09-26 · **Tier:** Brain (Opus 5.5, as the owner authorised)
**Status:** Recommendations for owner approval. Nothing here changes the game until approved; `docs/TASKS_lean_facets_v1_1.md` Phase 2 implements whatever is approved.
**Answers:** the strategic findings of `docs/REVIEW_lean_facets.md`. These are the ones that break the owner's expectations: half the presets can't fight, magic has no frame, one talent turns off the telegraph, rules are unstated or undefined, and the game isn't simple.
**Owner guidance applied:** *"make a suggestion that keeps things simple while maintaining player agency/fun"* and *"we don't have to hold a 2 page rules budget as hard and fast, so long as it is still 'simple'."*

**Research behind each decision:** each file has game-by-game findings with sources, options, simulations driven through the real engine, and a licence table.

| File | Decisions |
|---|---|
| `RESEARCH_v11_parity_and_defense.md` | D1–D4 |
| `RESEARCH_v11_magic_frame.md` | D5–D7 |
| `RESEARCH_v11_modifiers_and_budget.md` | D8–D10, and the draft cards |

---

## The shape of the answer

The review's strategic problems share a root. v1.0 copied early D&D's **primitives** (HP, damage, levels) but not its **guarantees**. In early D&D:
- every class could swing a weapon;
- every spell had a stated limit;
- a turn meant one action;
- a player learned about a dozen things before play.

The fixes below restore those guarantees. Each one **replaces or defines** an existing rule rather than adding a new subsystem.

| # | Decision | Recommendation, one line | Rules delta |
|---|---|---|---|
| D1 | Every Facet can fight | **Attack with your Facet's stat.** Mind's grit die goes d6 → d8. Light armor goes into the support presets' kits. | replaces one |
| D2 | Protection must not turn off the telegraph | **Intercept takes one attack aimed at an ally. *Sentinel* takes one from each of two foes.** | reworded |
| D3 | "Reach" is undefined | **The telegraph defines engagement.** A foe that telegraphs a melee attack at you is engaged with you. A ranged attack or working made while engaged is Hard. | defines one (was missing) |
| D4 | Armor has no owner; custom classes are thin | **Armor goes in the Facet table.** Wearing heavier armor than your Facet's makes your attacks and workings Hard. **A custom class may take one of its two starting talents from any Facet.** | replaces one (heavy-armor Fatigue) |
| D5 | Control magic is unbounded | **Stopping effects stop Mooks and Standard foes, but only hinder an Elite or Boss for one exchange,** unless the foe is Bloodied and the working is Major. | +1 sentence |
| D6 | Is a working an attack? | **A working aimed at a foe is an attack** for everything that makes rolls Easier or Harder. On a 7–9, one of the two offered costs is always "you are exposed". | defines one (was missing) |
| D7 | The caster budget doesn't grow; *Arcane Mastery* is free forever | **The casting talent grants a Fatigue-only slot at levels 3, 5, 7 and 9.** *Arcane Mastery* becomes once per scene. | lives in talent text (opt-in) |
| D8 | How modifiers combine is unstated | **One step, one cap, one clock** (below). | replaces about six |
| D9 | ~85 rules against "simple" | **A felt-simplicity budget:** ≤5 concepts before the first roll, a player card of about 35 rules plus a caster box of 8, no "unless/except" on the card, and about 40 rules moved to the MM's side. | about −40 player-facing |
| D10 | No turn bookkeeping | **One action each per exchange. Foes make exactly the attacks on their card, at the targets they telegraphed.** The app tracks both. | defines one (was missing) |

**Net:** the player-facing count falls from about 85 to about 35, plus 8 for casters. The novel-rule count stays at about 20. No subsystem is added. Nothing players enjoy is cut: Borrowed Trouble, peer Sparks, the Graceful Fail, Hold On, the death choice, the 10+ picks, foes rolling in the open, and freeform magic all stay.

---

## D1. Every Facet can fight

**Problem (review X2).** Attacks always roll Body. Mind and non-casting Soul presets lose to a single same-level Standard foe: 21% solo wins at level 1 and 0% at level 10 for the Physician and Investigator, against 100% for the Warrior. The gap widens with level because a Mind character's HP grows by +4 a level while monster damage grows by +1.

**What works elsewhere.** Every well-liked class-based light game lets every class attack with its own key stat, while keeping *what each class is best at* separate from *whether it can take part*:
- 13th Age: every class has a basic attack with its key ability.
- Daggerheart: every class attacks with its spellcast trait or weapon trait.
- Draw Steel: each class attacks with its characteristic.
- Cypher: each type spends its own pool.
- ICRPG: one stat per action type.
- 5e: finesse weapons and spellcasting ability make cantrips the always-on attack.

Fate Accelerated goes furthest: any approach can attack if the fiction supports it. Dungeon World kept STR/DEX for attacks and is the game most often criticised for weak non-fighters in a fight.

**Options.**
- (a) Attack with your Facet's stat.
- (b) The class knack names the attack stat.
- (c) Keep Body and give support presets combat talents.

(b) adds a choice at creation. (c) adds talents to every menu and still leaves Mind rolling +0.

**Recommendation: (a).** One rule changes: "an attack is 2d6 + Body" becomes "an attack is 2d6 + your Facet's stat". In the fiction, a Body character overpowers, a Mind character reads the opening, and a Soul character has the nerve and the luck. Two data changes come with it:
- Mind's grit die goes d6 → d8, which closes the HP growth gap.
- The Investigator, Physician, Speaker and Wanderer kits gain light armor.

A caster's staff is simply their always-on attack, and a Significant harm working is the costly bigger swing.

**Evidence (engine-driven simulation, solo against a same-level Standard foe).**

| Preset | Level 1, before → after | Level 5, before → after | Level 10, before → after |
|---|---|---|---|
| Mind non-casters | 21% → 77% | 7% → 90% | 0% → 51% |
| Thaumaturge | 61% → 84% | 33% → 94% | 8% → 68% |
| Body | 96–100% → unchanged | | |

An all-Mind party now wins the standard fight 100% of the time.

The review's target of "≥60% solo for every preset" is too strict for support presets at level 10. Adopt the research's replacement parity test instead:
- every preset solo ≥50% at level 10 and ≥70% at levels 1 and 5;
- per-PC drop rates in a Boss fight within 2× of each other.

**Knock-on.**
- Fights get easier. After D1–D4, casters drop to a Boss 6–9% of the time. Monster numbers must be re-simulated and retuned, probably +1 monster damage or attack. This is a Phase 2 task, and the books print whatever the simulation settles.
- A free staff blow at Mind +2 now competes with the 1-Fatigue 1d8 bolt, which is why D6 makes harm workings attacks with a real edge. Harm working damage should read "your weapon die +1 step" or 1d10. The simulation decides.

---

## D2. Protection must not turn off the telegraph

**Problem (review, design M1).** *Sentinel* plus Intercept lets one Guardian take every attack on every ally. Against a level 5 Boss, allies dropping falls from 56% to 2%, and the enemy's telegraph stops mattering.

**What works elsewhere.**
- 5e's Protection style and Sentinel feat each work once per round, off one reaction.
- 13th Age's intercept talents are limited per round.
- Dungeon World's Defend spends a limited hold.
- Blades lets you "protect" at a cost to yourself, one action.

In every case, protection is a *choice with a limit*, never a blanket.

**Recommendation.** **Intercept: take one telegraphed attack aimed at an ally you can reach. *Sentinel*: take one attack from each of two different foes.** No new counter is needed; it's a rewording. Allies down against a level 5 Boss:

| Rule | Allies down |
|---|---|
| Guardian attacks instead | 53% |
| Current Sentinel | 2% |
| Recommended | 18% |

The telegraph matters again, and the Guardian's choice of *which* attack to take becomes the interesting decision.

---

## D3. What "reach" means

**Problem (design M4).** Five rules hang on "within reach": exposure, Intercept, cover, the out-of-reach 7–9 costs, and Cleave. None of them defines it, so ranged characters dodge attacks by fiat and strictly dominate melee.

**What works elsewhere.**
- 13th Age: *engaged*, where moving away draws an opportunity attack.
- Dungeon World: ranges as tags (hand, close, reach, near, far).
- Daggerheart: range bands.
- Shadowdark: close, near and far.

The light games all define engagement by **who is fighting whom**, not by squares.

**Recommendation: the telegraph defines engagement.** When the MM telegraphs a melee attack at you, that foe closes and is **engaged** with you, unless the fiction stops it. Then:
- Exposure (a 7–9) applies to the next attack on you from any foe.
- A ranged attack or working you make while engaged is Hard.
- Cleave, Whirlwind and Intercept refer to "engaged".
- The line "out of a foe's reach, you are out of its attacks" is deleted.

This costs zero bookkeeping, because the telegraph already exists and the simulation already behaved this way when MM1 was calibrated. Staying back is still possible, but only by making the fiction stop the foe: a line of defenders, a doorway, a Studied Foe, or a stunt.

---

## D4. Armor belongs to the Facet; custom classes gain real breadth

**Problem (design M6).**
- Armor is the biggest build lever and nobody owns it, so any class can wear plate.
- A custom class is "pick 2 of the same 12" as a preset, which is thin for the Morrowind promise.

**What works elsewhere.**
- Early D&D, 5e and 13th Age tie armor to class. The idea in all of them: heavier armor than your training costs you.
- Morrowind let a custom class take major skills from any specialization. Its specialization only made its own skills cheaper.

**Recommendation.**
- **Armor row in the Facet table.** Body: heavy and shield. Soul: light and shield. Mind: light. Wearing heavier armor than your Facet's makes your attacks and workings Hard. This **replaces** the heavy-armor-costs-Fatigue rule, so it's net zero.
- **A custom class may take one of its two starting talents from any Facet's menu,** never a casting talent. That is the Morrowind move: your Facet sets your numbers, while your identity can reach across. Later off-Facet picks still need a teacher.

**Evidence.**
- With D1, an ungated Mind Tactician in heavy armor and a shield wins 100/99/95% (level 1/5/10) against the Warrior's 100%.
- With this armor gating, it wins 94/95/88%, so niches survive.
- Every current preset kit already complies.

---

## D5. Control magic is framed by the foe's role

**Problem (review X3).** "A person bound" costs the same 1 Fatigue as a 1d8 bolt, and no rule lets a foe resist it. A signature control working ends a same-level Boss fight in 1.0 exchanges with 0–0.7% party HP lost. The book's showcase fight is won that way.

**What works elsewhere.** Two families:
- **Resist rolls:** B/X saves by Hit Dice, 5e save-ends and Legendary Resistance, Ars Magica Penetration.
- **Rank sizing:** 13th Age HP thresholds ("stunned if it has ≤ N HP"), Blades scale, Ironsworn rank, Cypher level against effect.

**On our chassis a resist roll scales the wrong way.** A same-level Boss shrugs 42% of control at level 1 and 83% at level 9, and when it fails, one roll still ends the fight. It also adds a roll. Rank sizing is simpler and fits "enemies roll only to attack".

**Recommendation (one sentence in II.3 and on the caster box).** *A working that would stop a foe outright (bind, blind, charm, sleep) stops a Mook or a Standard foe; an Elite or a Boss is only hindered for one exchange (its attacks are Hard) unless it is Bloodied and the working is Major.*

**Evidence.**
- At level 1, control now plays like bolts: 3.6 exchanges and 43% party HP lost, against 3.0 and 38%.
- At levels 5 and 9, a 2-Fatigue Major that finishes a Bloodied Boss shortens the fight by about one exchange, which is a real payoff for a big spend.

The strict alternative (Major only hinders a Boss, never ends it) is an **MM dial**, printed beside the rule. Rejected: "the Boss loses an attack", which is worth 1.5–3× a bolt.

**The Archive Guardian vignette** is rewritten to a beat the rules reproduce: five exchanges, no new canon, arithmetic checked (in the research file).

---

## D6. A working aimed at a foe is an attack

**Problem (design M5).** The book is silent on whether a working is an attack. The engine says it isn't, and the simulator invented a third answer: exposure on a 7–9. That breaks the CLAUDE.md rule.

**What works elsewhere.** Daggerheart treats a damaging spell as an attack. 5e spell attacks use the same advantage rules as weapons. 13th Age spells are attacks against defenses.

**Recommendation.** **A working aimed at a foe counts as an attack for everything that makes a roll Easier or Harder:**
- level gap, openings, stunts, Studied Foe;
- casting while engaged (D3).

**On a 7–9 it offers two costs as now, and one of them is always "you are exposed".** A caster is never charged twice, and standing behind a Guardian makes exposure the free choice. That's a real tactical reason to protect the caster. The simulator drops its private rule.

---

## D7. The caster budget grows; *Arcane Mastery* stops being free forever

**Problem (design M7).**
- A caster's Fatigue budget is fixed by slots, so their share of a day's actions falls from 56% at level 1 to 30% at level 9.
- From level 3, *Arcane Mastery* makes a signature working cost 0 forever, which is unlimited.

**What works elsewhere.** Every durable caster design grows its budget with level:
- Knave and Maze Rats add spell slots by level.
- Dungeon World adds spells by level.
- 13th Age adds daily spells by level.

**Recommendation.**
- **The casting talent (Thaumaturgy or Invocation) grants one extra slot that holds only Fatigue, at levels 3, 5, 7 and 9.** This lives in the talent text, so only casters learn it: opt-in complexity, not a core rule.
- ***Arcane Mastery*: "once per scene, one signature working costs 1 less Fatigue."** That puts it on par with *Miracle*.

**Evidence.**
- The Thaumaturge's budget goes 5 → 7 → 9 casts, and their share of a day's actions holds at 51–56% at every level.
- Rejected: Fatigue clearing on a breather, because breathers are frequent. Also rejected: "extra slots equal to level", which overshoots to 85% at level 9.

---

## D8. One step, one cap, one clock

**Problem (consistency K, design m).** How Hard and Easy sources combine is unstated, and the engine silently decides. Sparks are uncapped, and III.1 contradicts itself on maximum dice and on Help. Enemy naturals, stunt duration and area effects against mobs are unruled.

**What works elsewhere.**
- 5e's advantage/disadvantage cancel-and-never-stack is the single most-praised simplification in modern D&D, adopted by Shadowdark and The Black Hack.
- Blades caps a roll's extra dice (one push plus one assist, plus a Devil's Bargain).
- Most light games scope temporary effects to "until the end of the round".

**Recommendation.**
1. **One step.** The MM sets the base difficulty; a foe 3+ levels above you makes the base Hard. After that, rule effects only ever make a roll **Easier or Harder by one step**. Any Easier and any Harder **cancel**, and several of the same kind still move the roll **one step**. That one sentence replaces six scattered stacking questions.
2. **One cap.** **At most two extra dice on any roll**, from any mix of Spark, Help, Borrowed Trouble or talents, keeping the best two. This replaces uncapped Sparks, the one-Help and one-Trouble limits, and III.1's false "5d6 max". Beyond two dice, gains are marginal: one die is worth about 1½ steps, and a third takes +2 to 91% for a 10+.
3. **One clock.** **Everything a fight creates (exposed, covered, opened, studied, defending) ends at the end of the exchange.** A stunt's opening benefits **someone else's** next attack on that foe this exchange.
4. **Doubles.**
   - **For anyone:** a kept double six is a full success (for a foe, a hard hit) and something more.
   - **For players:** a kept double one on a failed roll pays a Spark (Graceful Fail), and **a natural 2 never turns a success into a failure**. That player-side floor was a deliberate design principle (III.1 *Through the Mirror*), and the case it covers is rare, so it stays. On this one point I'm deliberately departing from the research pick, which made doubles symmetric.
   - **For foes:** a double one is simply a miss. The lasting "opening" is cut.
5. **Mobs.** A hit on a Mook mob drops one Mook per 4 damage; an area working drops one per 2 damage. Simulate before printing.
6. **Cut:** the +4 bonus ceiling (moot under the one-step rule and a two-dice cap) and the Very Hard level-gap band.

---

## D9. A felt-simplicity budget

**The owner's standard:** "still simple", not a page count. **Measurable targets:**
- **≤5 concepts before the first roll:** the roll, your stats, your knacks, difficulty, Sparks.
- **Player card of about 35 rules**, plus a **caster box of 8** and a **level-up box**. Draft cards are in `RESEARCH_v11_modifiers_and_budget.md`.
- **No "unless" or "except" clauses on the card.** This can become a docs test.
- **G0 check:** a new player acts legally in the first exchange without asking.

**How the count falls from about 85 to about 35:** about 40 rules move to the MM's side. They still exist, but players meet them through the MM and the app:
- morale;
- mob mechanics;
- Bloodied phases;
- the level gap's effect;
- the Pressure die;
- Threat Clocks;
- group and player-vs-player rolls;
- trying again.

Dials (optional rules) are boxed beside the rule they change, with the default stated. Talents remain opt-in texts: each player reads only their own. **Nothing players enjoy is cut.**

---

## D10. One action each; foes attack as telegraphed

**Problem (app M, review).** Nothing counts actions: one player attacked 8 times in an exchange, and an Elite attacked 3 times. The MM can't see who is defending or exposed.

**What works elsewhere.**
- Every initiative-less structure still gives each participant one action per beat: Dungeon World's spotlight, Blades, Into the Odd's "players act, then enemies", and Cairn/Knave side turns.
- Daggerheart's optional spotlight tokens add a visible pacing aid.
- Draw Steel's alternating sides is rejected because it breaks the telegraph.

**Recommendation.** Keep the five-step exchange:
- **Each character gets one action per exchange.** Free things (talking, drawing a weapon, a knack's no-roll uses) are listed.
- **Each foe makes exactly the attacks on its card** (Standard 1, Elite 2, Boss 2, mob 1) **at the targets it telegraphed.** Intercept is the only way to move an attack.
- **The app:**
  - an action token per character;
  - attack pips per foe;
  - state chips (Defending, Intercepting, Exposed, Covered, Opened, Studied, Engaged);
  - one click to end the exchange and clear them.

**Dial:** spotlight tokens, only if G0 asks for them.

---

## Why this keeps it simple *and* fun

- **Agency goes up.** Every player can act meaningfully in a fight (D1). Protecting someone is a choice with a limit (D2). Standing behind the Guardian is real tactics (D3, D6). A custom class can reach across Facets (D4). Casters get a budget that grows (D7), and a big Major on a Bloodied Boss is a real finishing move (D5).
- **Rules go down.** The six stacking questions collapse into one sentence (D8). About 40 rules move to the MM's side (D9). Three definitions that were *missing* now exist (D3, D6, D10), so tables stop arguing.
- **Early-D&D guarantees are back:** anyone can swing, spells have limits, a turn is one action, and the MM runs the procedures.

## Risks and how Phase 2 handles them

| Risk | Handling |
|---|---|
| Fights get easier after D1–D4 | Re-simulate the whole ladder; retune monster damage/attack in `facet.yaml`; regenerate MM1–4 and the Bestiary from the simulation. The parity suite and the ladder suite become permanent tests. |
| "Attack with Mind" feels odd to some tables | The fiction line in III.3 (reading the opening), and a **dial**: "attack with Body, as in early D&D" for tables that prefer it. |
| Rank-sized control feels restrictive | The strict/lenient dial beside the rule. Non-stopping workings stay fully freeform. |
| The two-dice cap disappoints Spark-hoarders | Sparks still do the most dice work of anything, and the cap is the Blades-proven size. G0 checks it. |
| The mob rate is untested | The simulation settles it before print (Phase 2 task). |

## Decisions for the owner

1. **Approve D1–D10 as a package**, or name the ones to change. They interlock: D1 without D4 lets heavy-armored Mind builds match Warriors, D2 needs D3, and D1 forces D6.
2. **D5 dial default:** should a Major working on a Bloodied Boss *end* the fight (recommended) or only hinder it?
3. **D7:** should *Arcane Mastery* also be available to Soul casters? Recommended: yes, shared like *Wider Domain*.
4. **D8 doubles:** keep the player's natural-2 floor (recommended), or make doubles fully symmetric?
5. **D1 dial:** print the "attack with Body" variant for traditional tables? Recommended: yes, as a boxed dial.

**Resolved at Brain tier, pending owner approval. Return to Planner: `docs/TASKS_lean_facets_v1_1.md` Phase 2.**
