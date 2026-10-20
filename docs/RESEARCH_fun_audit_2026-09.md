# RESEARCH — Fun Audit: Did Chasing Simplicity Cost Us the Fun?

**Date:** 2026-09-08
**Tier:** Brain (Fable)
**Question (owner):** *"I fear that in chasing simplicity we've lost fun. I do not know that we have though; approach it impartially but critically. Review our game systems vs others out there, being mindful of copyright, and ensure that our system is fun while making combat not a slog like DnD where combat can easily be 70-80% of the game time. Include Oraga Night, both as a module and as an example of the game system in action."*
**Scope:** the game system (core resolution, combat, magic, advancement, backgrounds, equipment, encounter design, the MM tooling) and the Oraga Night module. Not the web UI.

**Companion files (written for this audit, read them for the evidence):**
- `docs/RESEARCH_fun_audit_evidence.md` — every playtest and simulation figure, graded for reliability, with `file:line` citations. 43-row issue ledger, 16 evidence gaps.
- `docs/RESEARCH_comparative_combat_landscape.md` — 21 systems, license status, what keeps their combat interesting, what their communities call un-fun, and a seven-cluster synthesis. Concepts only; no rules text reproduced.

**Prior work this audit re-tests rather than assumes:** `docs/RESEARCH_fun_ease_review.md` (2026-08-08, "the fun architecture is sound and validated") and `docs/RESEARCH_fun_gap_analysis.md` (2026-08-11, "the core is not oversimplified"). Both were written by this tier. Both are partly wrong about what "validated" means; see §1.

---

## Verdict up front

**You have not simplified the fun out of the core.** The one-roll engine, the three tiers, the naturals, Sparks with peer awards, Borrowed Trouble, the Graceful Fail, Conditions with names, the death choice, Threat Clocks, and the Technique trees are good, and the August work made them better. Nothing in the centre needs undoing.

**You have built a system whose fun is almost entirely supplied by the Mirror Master.** The rules produce very few moments on their own. That is a legitimate design bet (the whole PbtA and Forged family makes it), but the field has a name for the failure mode, "GM-load," and the evidence on record shows it: the same scenes run by the expert-MM persona read as rich and by the novice-MM persona read as "You learn nothing," four times in a row (`RESEARCH_fun_audit_evidence.md` §8). The system is only as fun as the person in the chair, and it gives that person less scaffolding than its peers do.

**Combat is not a slog. It is short and shallow, and nobody has yet asked a human which of those two words they would use.** Every fight measured under current rules runs one to three exchanges; a solo Boss has a median of two (`simulation_log.md:688-702`). Against D&D 5e's measured 27-32 minutes per fight and a 51-60% median share of the session, you have won the length argument outright. But a fight's decision structure is thin (about two real decisions per exchange, both keyed to the Endurance bar), the Open tag makes every Named and Boss fight the same shape, and the Boss's second act fires in the exchange the fight ends. The comparative landscape's finding is the audit's finding: "short" and "interesting" come from different mechanisms, and the system has most of the first set and little of the second (`RESEARCH_comparative_combat_landscape.md` §2.4).

**The largest single finding is not about a rule. No human has ever played this game.** Every quoted player in every playtest is a language model; the two "table" playtests ran on pre-rolled dice and v0.1/v0.2 rules; playtest 06 played an HP-and-damage ruleset that does not exist; playtest 07 is invalid by the project's own ruling; the only session with engine dice and free agents is one exchange against two Mooks. Every rule dated 2026-08-02 or later, which includes the Open tag, the D16 advancement curve, the natural 12, Borrowed Trouble, and the social 7-9 texture, has never been played by anything. The prior two fun reviews said "validated"; they meant "internally consistent and simulated." That distinction is the reason this audit's first recommendation is a playtest, not a rule.

**Oraga Night is an excellent adventure and a poor test of the system.** It sidesteps both of the mechanics the owner's question is about: it replaces domain magic with tribal gifts and makes every fight either opt-in or unwinnable by design. What it proves is that the core roll, Sparks, and Conditions can carry a five-hour social night when the *module* supplies the structure. What it also shows, quietly, is that the first time someone wrote real content for this game, they swapped out both flagship subsystems. That is worth sitting with (§8).

### The fun ledger

| What players come for | What delivers it here | State |
|---|---|---|
| Story that moves on every roll | Three tiers, Trouble Table, Graceful Fail, "never a dead end" | **Strong** |
| Peak moments the table remembers | Natural 12/2, Intercept, the death choice, Borrowed Trouble | **Strong, unplayed** |
| Fellowship at the table | Peer Spark calls, act-break nominations, any-player Borrowed Trouble | **Strong, hoarding unretested** |
| Fast fights that do not eat the night | Exchanges, no initiative, Mooks fall to one hit, NPCs never roll, morale lines | **Delivered** |
| Fights with an arc and real decisions | Posture, Press, reactions, Open, phases | **Thin**; posture is a script, Open flattens the shape, phases fire as the fight ends |
| Enemies that feel different | Conduct fields, three worked Techniques, Bestiary (10 of 12 Named/Boss carry a Technique) | **Built, unshown**; the PHB's own Boss vignette is "Measured. It always is." |
| Creative magic without a spell list | Domain + Intent + Scope, 162 example intents | **Strong for confident players**; blank-page problem for novices; absent from the first module |
| Social play that feels like fencing, not lockpicking | One roll at the pivot, social 7-9 table, Specialty | **Thin as system, rich as module** (Oraga's agendas, omens, tells) |
| Growth you can feel | Ranks +0→+3, three Techniques, D16 caps | **Real but slow and qualitative**; nothing distinctive in session one, worst for Body |
| Something to carry out of a fight | Marks, Sparks, scars | **Thin**; no loot, no downtime, nothing that pulls play forward |

---

## 1. Method, and how much to trust the evidence

I read the current rules text in full (III.1, III.2, III.3, II.3, II.4, II.4a/b/c, II.5 Body, IV.1, Quick Start, MM1, MM2 §Scene Types/§Trouble Table/§Spark Cadence, MM3 §Campaign Clock, DECISIONS D1-D16a) and every Oraga Night file including the seven enemy stat files. Two subagents produced the evidence digest and the comparative landscape; I read both in full. I computed the outcome probabilities below myself.

**Evidence grades, from the digest §1.** PT01/02: LLM-written fiction on pre-rolled dice, v0.1/v0.2 rules (B-). PT03/04: Monte Carlo and scripted drivers whose posture, reaction and Spark "choices" are Endurance-ratio heuristics (A for arithmetic, nothing for feel). PT05: advancement formula only, superseded by D16. PT06: played with invented HP, damage-reduction armor and death-at-zero (D). PT07: invalid numbers by the project's own ruling. PT08: real dice, real free agents, one exchange, two Mooks, three of four players never declared a posture (A- for two beats). Simulation Series 7-11 are sound for what they model, and they do not model Maneuver, Support, combat magic, or any Technique in a PC's hands.

**What that means for this audit.** Any sentence below of the form "players found X fun" is a sentence about what a language model wrote that a player would say. I use those quotes only where the *mechanism* they point at is visible in the rules text independently. The quantitative claims (exchange counts, win rates, posture dominance) are sound. The qualitative claims are hypotheses for a human table to confirm.

---

## 2. Fun for whom

"Have we lost fun" has no answer until you say whose. The most durable working taxonomy in the hobby (Robin Laws' seven player types, used here as a general concept) sorts players by what they came for. Scored against the current rules:

| Player type | Comes for | What the system gives them | Served? |
|---|---|---|---|
| **Storyteller** | The plot, the world, consequence | Every roll moves the story; Trouble Table; Graceful Fail; Borrowed Trouble; Oraga Night | **Yes, well** |
| **Method Actor** | Being the character | Sparks for weakness play; Specialty; Techniques as fiction permissions (*Read the Room*, *Forcing Hand*); reflection scenes | **Yes, well** |
| **Casual Gamer** | Company, low friction | One rule; ten-minute Quick Start; the app absorbs bookkeeping | **Yes** |
| **Specialist** | One thing done superbly | Master slot under D16; one-step Techniques; Specialty | **Mostly**; the +4 ceiling and one-step cap mean "superbly" is qualitative, not numerical |
| **Power Gamer** | Growth, options, a build | +0→+3 over ~10 sessions; three Technique picks; no loot; no numerical scaling of anything | **Weakly** |
| **Butt-Kicker** | Hitting things and having it matter | Mooks fall to one hit (good); every hit is 2 or 1 Resolve; no big-hit moment beyond Open; fights end in two exchanges | **Weakly** |
| **Tactician** | Meaningful choices under pressure | Posture (a script); Press vs. save (real); reaction (a lookup); Maneuver (dominated by Strike); no position | **Weakly** |

Three of seven types get little, and two of those three are the types whose preferences drive D&D's combat share to 70%. That is the honest shape of the answer: **the game has not lost fun in general; it has deliberately not built for the players who make combat the main course, and it has not yet decided whether that is a choice or an accident.** The recommendations in §9 assume the owner wants to keep the game's centre of gravity where it is and give the underserved three *enough* to stay at the table, not to win them outright.

---

## 3. What is fun and should be protected

Recorded so the next review does not relitigate them.

- **The one roll and its three tiers.** 2d6 + a small modifier, 10+/7-9/6-. Teachable in one sentence, and the 7-9 band being the modal outcome is the single strongest finding in `research/dice_system_analysis.md`.
- **The naturals.** Keyed to the kept dice, so they never inflate with competence, and the asymmetry (12 promotes, 2 never demotes) is exactly right. Extra dice help twice. Unplayed, but correct on paper.
- **Sparks earned by peers.** The peer call and act-break nomination are a fellowship machine few published games match. Sparks resetting to 3 is the right anti-hoarding lever. Whether it works is untested (§7).
- **Borrowed Trouble.** Reuses the dice rule, costs nothing to offer or decline, any player may offer, the complication lands regardless. This is the best rule added this year.
- **The Graceful Fail.** Player-claimed, MM-confirmed, with a real bar. It turns the worst outcome into the one that pays.
- **NPCs never roll; the defender holds the dice.** The reaction roll is the inverse of "roll to be hit" and every LLM report, whatever its provenance, reached for it as the tense moment. The design note in III.3 defends it well.
- **Endurance as a tempo pool, not hit points.** Press competes with Dodge for the same point. That is the one genuinely good resource tension in combat.
- **Intercept.** The single mechanic every report, of every grade, calls a peak. Two Endurance to take an ally's hit and then roll your own reaction is the right price.
- **Conditions with names, Tier 1 clearing per exchange.** The "Weary/Spent/Bleeding/Exposed" retrospective in III.3 is the right lesson, correctly learned.
- **The death choice.** Broken never kills; when the fiction would, the player picks the scar or the heroic last action. This is better than any death rule in the comparison set.
- **Threat Clocks with a free wind-back.** Four segments, advance on any non-full success, wind back for an action with no roll. Simple, visible, and the "nobody plays the janitor" note shows the failure mode was considered.
- **Domain + Intent + Scope.** A three-decision casting loop with no list to maintain. The scope-cap-not-difficulty-penalty ruling for pre-Technique magic is the right call and the playtest that forced it was the one useful thing PT01 did.
- **Techniques as permissions rather than bonuses.** *Read the Room*, *Forcing Hand*, *Convenient Coincidence*, *Working Theory*, *The Turning*, *Hard to Kill*: these are the most expressive things on the sheet and the reason the game will have build identity at all. The `Normal:` line on every entry is excellent apparatus.
- **D16.** Rank caps so two Body characters end a campaign with different sheets. The right fix for the right problem.
- **The Trouble Table and the social 7-9 table.** Both exist to get the MM from silence to a sentence. They are the scaffolding this audit says the system needs more of.
- **Oraga Night's Fractures.** Facts learned in play become difficulty on the climax roll. That is a mechanic, it is good, and it should not stay module-local (§9 R6).

---

## 4. Combat: short, not slow, and shallow

### 4.1 Length: the argument is won

| Source | Fight | Length |
|---|---|---|
| D&D 5e, EN World actual-play log | 5-6 round fight, levels 2-3, grid | 27-32 minutes, ~6.9 min/round |
| D&D, EN World poll (89 votes) | share of session in combat | median band 51-60%; 24% of tables report 71%+ |
| FoO, Series 9/10 sims (current rules) | Skirmish / Named solo / Boss solo | median 2-4 / 1 / 2 exchanges |
| FoO, PT03 (n=300 × 7 seeds) | Boss with heavy armor, post-A14 | median 3, min 3, max 6-8 |
| FoO, PT04 live driver | Skirmish / Standard / Hard | 1 / 4 / 3 exchanges |
| FoO, narrator estimates (PT01/06, never clocked) | Mook fight / Guardian | "~10 min" / "~20 min" |

Under current rules no measured fight has exceeded four exchanges except Mook-swarm tails. MM2's own target is 15-25 minutes for a three-exchange fight. Nothing rewards fighting: marks go to any skill used, Sparks go to fiction, and every Bestiary and Oraga enemy carries a morale line. Combat will not become 70% of this game's session by accident. If anything the risk is the inverse one the landscape names for loot-less narrative games: "combat feels like a scene like any other."

### 4.2 Decisions per exchange: about two, both resource-keyed

| Decision | Is it a decision? | Evidence |
|---|---|---|
| **Posture** (blind, 4 options) | **A script.** Correct posture is a function of your own Endurance bar, not a read of the enemy. Over a full fight Aggressive and Measured produce the same Broken rate (~84%, n=1000); K1 made Aggressive's offense edge worth 1.1-1.7 points of win rate. A PC not being targeted this exchange pays nothing for Aggressive at all. The sim AI plays "high End → Aggressive, low → Defensive" verbatim and wins with it. | `simulation_log.md:488, :494-515`; `combat_sim.py:267-282`; PT08's one reasoned declaration is the same arithmetic done aloud (`08/transcript.md:93`); three of four PT08 players never declared |
| **Strike vs Maneuver vs Support** | **Strike dominates against enemies.** A 10+ Strike depletes 2 *and* may leave the enemy Open (Easy for everyone). A 10+ Maneuver makes rolls against the target Easy, and an Easy tag does not stack with itself. So against any enemy Open can be inflicted on, Maneuver's best outcome is a strict subset of Strike's. Support is "roll so someone else rolls better," the aid-another tax every d20 game learned to dislike. | Rules: III.3 §Strike, §Maneuver, III.1 §Difficulty precedence. Usage: Maneuver and Support appear twice each in v0.1/v0.2 fiction and **never since**; no sim models them (`simulation_log.md:271, :390`) |
| **Press** (1 Endurance for a die) | **Real.** It competes with the Dodge you may need. | PT08: "I am spending a Spark rather than Pressing, because Press costs Endurance and Endurance is the exact thing I have none of. Which, for the record, is the system working." |
| **Spark** (before the roll) | **Real, and hoarded.** Free-agent sessions spent 2 of 9, 2 of 12, 1 of 12. Scripts spend 6-9. | digest §3.5 |
| **Reaction** (Dodge/Parry/Absorb/Intercept) | **Half a decision.** Dodge vs Parry is a lookup (whichever modifier is higher). Absorb vs pay is real only when the pool is low; against Mooks Absorb is strictly correct (Tier 1 clears at exchange end, Absorb is free). Intercept is real and the game's best moment. | `combat_sim.py:395-414`; digest §3.3 |
| **Target** | Rarely a decision: focus fire opens every PT03 fight and the sims say concentrating on one enemy is right at any TR. | `03/results.md:47`; `simulation_log.md:570` |

That leaves Press-or-save and Spark-or-hold as the two live decisions in a normal exchange, plus Intercept when an ally is threatened. Both live decisions are "spend a resource or not." Neither is "what kind of thing do I do." That is the landscape's cluster 2 gap, and its community symptom is the sentence PT01's narrator already worried about: *"Will it just be 'I Strike, I Strike, I Strike' with occasional posture switches?"* (`01/playtest_report.md:255`). Nothing since has answered it.

### 4.3 The Open snowball makes every Named and Boss fight the same fight

Probability of each tier, 2d6 + modifier (computed for this audit):

| Modifier | Plain 2d6 (full / partial / fail) | With one extra die (Spark, Press, Support, or Trouble) |
|---|---|---|
| +2 (a starting fighter at Standard) | 42% / 42% / 17% | 68% / 27% / 5% |
| +3 (same, Aggressive) | 58% / 33% / 8% | 81% / 18% / 2% |
| +4 (same, Aggressive, enemy Open) | 72% / 25% / 3% | 89% / 10% / 0% |

A fresh party's first 10+ hangs Open on the enemy. Every subsequent Strike from anyone is at +4 or better, so 72% of them are full successes without spending anything, 89% with any die. Each full success takes 2 Resolve. A Named NPC at Resolve 3-4 is gone the exchange after it is Opened; a Boss at 10 needs five such hits, which three PCs supply in two exchanges. The enemy's one answer, spending its action to close Open, costs it the only attack it makes that exchange, so both branches favour the party. This is why the Recipe Table finds a solo enemy trivial "at any TR" and why the solo-Boss median sits at 2, "flagged for playtest attention rather than retuned" (`simulation_log.md:694-702`).

The shape is always: land the tag, then chain. Three consequences:

1. **The Boss has no second act.** Phase thresholds sit at Resolve 2. In a two-to-three-exchange fight that is the final exchange. PT03's first run said it plainly: the phase "arrived in the final exchange or two and changed nothing the party did" (`03/results.md:149`). The Archive Guardian's Reduced Mode makes it *stop* clearing Open, which is a phase change the party cannot feel because it was never clearing Open anyway.
2. **The first 10+ is the fight's only peak.** After it, each roll is a formality with a high number attached. The PHB's own Guardian vignette shows it: six consecutive rolls of 10-13, every one a full success, the fight over in three exchanges, and the narration doing all the work.
3. **The escalation only runs one way.** The landscape's cluster 1 (a visible curve that makes each later exchange more decisive) is here, accidentally, as Open. But it only steepens for the party. Nothing steepens for the enemy, so the fight has a slope but no tension on it.

### 4.4 The enemy side: built, not shown

NPCs never roll and land a fixed tier, so all enemy texture has to come from conduct fields, Techniques, and stances. The tooling exists and is good: `disposition/first_target/triggers/morale/negotiation`, three worked Techniques in MM1 (Flurry, Telegraphed Finisher, Sapping Strike), telegraphed finishers, and a Bestiary where 10 of 12 Named and Boss entries carry a Technique and every Oraga enemy carries conduct and a morale line. None of it has been run at any table (`digest` §6).

What *has* been shown is the PHB's showcase fight, and it advertises the flat version: the Guardian "is Measured. It always is," never changes stance, never clears Open, uses no Technique, and its phase change makes it worse at the one thing it was not doing. A reader learns the exchange structure from that vignette and learns that the enemy is a number that runs down. The three worked Techniques exist to prevent exactly that reading and they are two chapters away in another book.

### 4.5 Against the field

The comparative landscape sorts how fast-combat systems stay interesting into seven clusters (`RESEARCH_comparative_combat_landscape.md` §2.1). Scored:

| Cluster | Principle | Facets of Origin has |
|---|---|---|
| 1. Escalation | Time in the fight is a rising curve everyone can see | Open (one-directional); uncontested-exchange rule; Threat Clocks *can* run in a fight. **Half** |
| 2. Decision per action | The same roll means different things depending on a choice made before it | Posture (a script); Press. Strike is always the same sentence. **Weak** |
| 3. Post-roll agency | Pay, after seeing the dice, for a better result | Absorb-or-react in combat only. Nothing outside it. **Weak** |
| 4. Outcome-texture dice | Every roll narrates; the "what else" has a menu | Three tiers, naturals, Trouble Table, magic 6- templates, social 7-9 table. Combat 7-9 resolves to "one less Resolve." **Good outside combat, thin inside it** |
| 5. Enemy-side texture | The enemy does things, not only has numbers | Conduct fields, Techniques, phases, morale. **Built, unshown** |
| 6. Danger and avoidance | Whether to fight is the decision | Morale lines everywhere; Oraga's opt-in steel; Deadly = "solve, don't fight." **Yes** |
| 7. Reward loops | What reward attaches to is what the table does more of | Sparks for fiction; marks for use; no loot; no carry-forward. **Pulls away from combat, which is the intent; gives fights nothing to carry out** |

The landscape's rule of thumb: every well-liked fast system has at least one of clusters 1-3 fully, and the most praised have two. Facets has half of one. The games with cluster 6 and little else (Cairn, Shadowdark, Mörk Borg) are the ones whose communities use the words "flat," "weightless," and "powerless," and those games are explicit that flatness is intended because the fight is not the point. That is a coherent position. It is not the position III.3 takes, which promises "choices that feel real" and "half the tactical game."

### 4.6 So: is combat fun?

On paper it is fast, legible, low-load, and it has three genuine peaks (Intercept, the first 10+, the death choice). It is not a slog and cannot become one. It is also, by the numbers, a fight with two live decisions per exchange, one shape, and no second act, and the rules text promises more than that. Whether a two-exchange Boss fight reads as *fast* or *flat* to a person is exactly the question the evidence cannot answer, and it is the first thing to ask a human (§9 R1).

---

## 5. Magic

The loop is good and the pre-Technique ruling was the right one. Three things to name:

- **The blank-page problem is real and half-solved.** PT06's novice personas asked "Can I do X?" instead of declaring intent, and one felt "like I was cheating by making up my own spells." The 162 example intents (c0553ed) are the right fix and have not been played since. A caster's first session should probably open with the intents table in hand, not the domain description.
- **A mage in combat is a fighter with a different attribute.** A magical Strike depletes 2/1 Resolve exactly as a sword does; the caster's other option is Support, the weakest action (§4.2). The "Mind and Soul in a Fight" section lists Insight, Investigate, Persuade as combat verbs and that is the right instinct, but each resolves to a difficulty modifier on somebody else's Strike. The mage's fiction is more interesting than the fighter's; the mechanics are not.
- **The first module removed the domain system.** Val'loh has "no magic domains"; gifts are always-on Easy tags and crystals are consumable charges. That is legitimate mini-Facet design, and it is also the case that when the setting author sat down to write real content, Domain + Intent + Scope was not what they wanted. One data point, but the only one (§8.2).

---

## 6. Social and exploration: the pillars that carry the time

Under this design, four fifths of a session is not combat. What the *system* offers those hours: one roll at the pivot, a difficulty called out loud, a cost named on a 7-9 from a six-row table, a Trouble Table on a 6-, Specialty as a no-roll or an Easy, Threat Clocks for hazards, and Techniques from level 1. That is the PbtA amount of scaffolding without PbtA's moves, and it works precisely as well as the MM does. PT07's paired runs, invalid as they are for numbers, show the mechanism cleanly: the same social scene run by the "expert" MM produces debts, doubled guards, restricted movement; run by the "novice" it produces four Hard checks, four failures, "You learn nothing."

Oraga Night is what the missing scaffolding looks like when a module supplies it: eight agenda cards (ask / catch / at-midnight), one omen per Movement, four undercurrents with redundant trails, a rumor table, fifteen NPCs with wants/fears/secrets and the difficulty each imposes, printed Spark rewards for peaceful play, and tells that convert into difficulty on the climax. None of that is rules; all of it is structure; and none of it is in the MM Manual as a reusable pattern. MM2's scene-type section is good advice. It is not a night-tracker.

---

## 7. Growth, distinctiveness, and what you carry out

- **Session one.** A new character holds attributes, one Practiced skill, one Novice skill with a mark, and a Specialty. Three of fifteen Backgrounds add a domain (all Mind or Soul). Every Body Background is skills plus a sentence. This is the fun-gap analysis's item 4, still open and correctly deferred "until a playtest confirms Body characters feel flat." D16a moved the first Technique to sessions 2-4, which is the right partial answer.
- **The arc.** Ranks +0 to +3 in roughly ten sessions; three Technique picks; a Major Advancement at Facet level 3. The Technique layer is where identity lives, and it is genuinely good, and no PC has ever used one at a table (`digest` §9). Nobody has advanced a character and played it again.
- **Sparks.** Hoarded in every free-agent session on record. The reset-to-3 rule and the natural-12 incentive are the designed answers, both unplayed. Do not add a third lever until those two are measured.
- **Nothing carries out of a fight.** No loot (IV.2 is *Planned*), no downtime, no Victories, no scar except the death scar. The landscape's cluster 7 note is the gentle version of the complaint: fights become "a scene like any other." Cypher's rotating one-use consumables are the cheapest known way to get "what do I have this time?" without a permanent +1 economy.
- **Four attributes carry one skill each** (Constitution, Knowledge, Luck, Spirit), so Luck is dead weight on a Body sheet. PT08's finding, no decision recorded. A Planner-tier design question.

---

## 8. Oraga Night

### 8.1 As a module

This is very good adventure writing, and the best argument in the repository that the game's centre of gravity is in the right place. What it does well:

- **Structure that runs itself.** Seven Movements with scheduled events, one omen each, and a one-page night-tracker with every NPC's position per Movement. A tired MM at Movement V has the whole night on one sheet.
- **Player-facing engines.** Eight agenda cards with an ask, a catch, and a private turn at midnight; two players may share one. The "at midnight" line is the module's best trick: every errand becomes a role in the crisis. Agenda 6 (the hired traitor who turns out to have saved the child) is the kind of reversal tables retell.
- **Investigation done right.** Four undercurrents, each with a spark, a redundant trail, a find, and a midnight payoff, and the explicit rule that no single failed roll closes a thread. The Root of the House is a genuinely great reveal.
- **Peaceful play is paid on the page.** Sparks for agendas, omens, closed rooms without a fight, ending a fight without finishing it, carrying someone out, telling the truth at cost. "A reward you have to remember to invent is a reward that does not happen" is the right design principle and the MM Manual should say it too.
- **Fractures.** Tells witnessed in play become difficulty on the climax; one tell is Hard, two is Standard. It converts attention into leverage, it makes the unwinnable fight fair, and each of the three has a different emotional key (sorrow / devotion / despair) with a different answer.
- **Opt-in steel.** Three visible troubles, one winnable fight aimed at the players' better natures, guards as "a scene, not a sentence." This is how a social module keeps a restless sword hand at the table without forcing anyone else to draw.
- **The crossfire rule** (a 10+/7-9/6- consequence ladder for standing in the duel's path) is a custom move in the PbtA sense, written for one scene, and it is exactly the shape the core rules could use for hazards generally.

Concerns, in order of weight:

1. **The hour count rests entirely on MM improvisation.** Four to six hours, a roll or two per player per Movement, and everything between rolls is conversation with fifteen NPCs. The cast chapter is strong enough to carry a confident MM; a novice will run out of Movement II. The module could use a short "if the table stalls in Movement II" panel with three approaches per agenda.
2. **"You cannot beat them" is fair only because the module works hard at it.** Tells are salted through three Movements, the tell-table is printed, and the text promises "a table that arrives at midnight with nothing can still earn a Fracture in the fire." Keep every one of those safeguards; remove any and the climax becomes a fight the players are told they lost before rolling.
3. **Pregens carry Endurance 3 and three Sparks into a night with two opt-in fights.** Fine for the module's shape; the Tavva fight is calibrated for it (Resolve 3, fights to leave). A table that goes at the honor guard will be Broken in two exchanges, which the guard sidebar handles by making detain-and-expel the outcome. Good.
4. **Nothing mechanical happens to the characters across five hours.** The Overture says so on purpose ("characters end the night mechanically where they began; what they leave with is Sparks, obligations, three or four people who now know their names"). For a one-shot that is right. For the three-to-four-session version, one skill advance somewhere in the wings would let the aftermath feel like a campaign.

### 8.2 As a test case for the system

What Oraga Night exercises: the core roll and difficulty ladder (heavily), Specialties (well: Dassa's is built for the Movement I omen), Sparks as a reward economy, the Conditions ladder via the crossfire rule, Mook and Named conduct fields and morale lines, enemy Techniques (Vanisher, Warder), Bosses with phases (the Wept), the group's ability to talk instead of fight.

What it sidesteps:

| Flagship mechanic | In Oraga Night |
|---|---|
| Domain + Intent + Scope | **Replaced.** "There are no magic domains in Val'loh." Gifts are always-on Easy tags; crystals are consumables; "nobody casts in a crisis. Ever." |
| Exchange-structured combat | **Opt-in only**, and the only winnable set piece is a thief crew that fights to leave. The three antagonists reset Resolve at 0 by design |
| Techniques in a PC's hands | **Absent.** First-session module, Facet level 0 |
| Advancement | **None** across one to four sessions |
| Encounter Recipe Table | **Not used**; the fights are authored by fiction, correctly |

So the module proves the *floor*: that the core roll, Sparks, Specialties, and Conditions can carry a long social night when a module supplies agendas, omens, and a cast. It proves nothing either way about whether the exchange structure or domain magic is fun, because it does not use them. As "the test case for what gameplay currently looks like," it is the test case for one of the three pillars.

And it is a data point about the other two. The first time real content was written for this game, its author replaced the magic system with something closer to Fate aspects (a standing Easy when the gift applies) and made combat a thing that happens to you rather than a thing you do. Either Val'loh's canon simply demanded that, which is entirely plausible, or the domain system is harder to write setting content *for* than to play, and the exchange structure is not what a writer reaches for when they want a set piece. The honest reading is: unknown, and worth one conversation with the author before the second module is scoped.

### 8.3 What the Oraga playtests say

Nothing usable about numbers; the project ruled PT07 invalid (LLM-invented dice, engine rolls over-counted four times) and the digest confirms it. The qualitative residue is one useful pattern: the novice-MM persona defaulted to Hard on every social roll, read a 7-9 as "-1 to your next roll," and reverted to turn order in fights. Those are the three most likely real-table MM errors, and none of them has a sidebar yet.

---

## 9. Recommendations

Ranked by payoff against added complexity. "Rules change" items go through the sync workflow (facet.yaml, engine, quick refs, same commit) and each needs a Series-10-style sim before the book changes.

### R1. Run a human playtest before any further rules work. *(No rules change; highest priority.)*

Everything above §9 is analysis of text and arithmetic. Two sessions, real people, engine dice, clocked:

- **Session A, social:** Oraga Night as written, one table, four to six hours. Clock minutes per Movement; count rolls per player; note every point the MM has to invent a cost from nothing. After: which Movement dragged, and did anyone miss having a mechanic to reach for?
- **Session B, combat-forward:** MM2's three-encounter template (Skirmish → Standard → Hard from the Recipe Table) with a PS-3 party that includes a Focused-domain caster and one Body character with *Weapon Mastery* (Facet level 1, D16a says that is session 2-4). Boss with a phase at the end. Clock each fight. Count decisions per exchange that were not "spend or don't." Then ask each player one question about the Boss fight: *fast, or flat?*
- Also run PT08's unrun Arm B (variable enemy severity), which was pre-registered and designed for exactly the "do Bosses feel same-y" question.

Until this exists, "validated" should not appear in a design document about fun.

### R2. Give the fight a second act. *(One-line rules change; sim first.)*

Open currently persists until the enemy spends its action. Change it to **clear at the end of the exchange, like a Tier 1 Condition.** Effects: the tag becomes "exploit it *now*," which is a tempo decision each exchange rather than a switch flipped once; the enemy gets its action back, so it can change stance or use a Technique instead of forfeiting a turn; Boss fights lengthen toward the 3-4 band without adding Resolve; phase changes have room to land mid-fight. Re-run Series 10 Part C; expect solo-Boss median to move from 2 toward 3 and be prepared to trim Boss Resolve by 1-2 to hold the cost curve. Alternative if the sim says fights get grindy: keep persistent Open but move phase thresholds to half Resolve so the second act arrives at the midpoint.

### R3. Make the Strike a sentence, not a number. *(One table row; sim first; the largest fun gain available inside the current system.)*

The landscape's most consistent lesson (PbtA's pick-list, DW2's diagnosis, DCC's deeds, PF2e's diminishing repeat) is that a successful attack should present a small menu. Proposal, shaped as a general principle rather than any game's text: on a **10+**, deplete 2 Resolve **and choose one**: leave the enemy Open; take position (the Maneuver result, so Maneuver folds into the Strike and stops being dominated); or cover an ally (their next reaction is free). On a **7-9**, deplete 1 and the MM names the cost, as now. The choice is made after the roll, which is the first post-roll decision in combat that is not "pay or don't," and it gives Body characters the expressive beat their sheet currently lacks. Complexity: one row on Table III.3-3 and the MM5 card; the app already offers Open as a confirm. Pairs with R2: if Open expires per exchange, "Open now or position now" is a real fork.

### R4. Settle post-roll agency outside combat with the player-chosen cost, not a Spark resist. *(Ruling needed; conflicts with D3; A/B it in R1.)*

The fun-gap analysis's item 3 is still open. The cheapest form is not "spend a Spark to downgrade a 6-" (which makes Sparks better held than spent, the opposite of what natural 12 is for). It is: **on a 7-9 outside combat, the MM offers two costs, from the pillar's table, and the player picks.** D3 rejected the PbtA-style "offer" because a decision on 46% of rolls taxes pace. The counter-evidence is PT01's MM persona naming invention as its biggest burden and PT07's novice MM producing "-1 to your next roll" when asked to invent; picking two rows from a printed table is faster than inventing one, and it hands the player a choice at the most common outcome. Test both sequencings in Session A.

### R5. Session-one Body distinctiveness. *(Defer until R1 confirms it; then one sentence per Background.)*

If Body characters do feel flat next to a domain-holder, the cheapest fix that does not disturb D16's Technique economy: give each Body Background's Specialty a **once-per-scene "no roll" mode** in addition to its Easy mode (the Arena Fighter's "reads an opponent's style in the first exchange" already reads that way). It makes the Specialty a thing you *do*, on the model of *Read the Room*, without granting a Technique. Do not act on this before a human table says the flatness is real.

### R6. Promote Oraga's structures into the MM Manual, and write the combat-forward counterpart. *(MM Manual additions; no rules change.)*

- An **Agenda card** pattern (ask / catch / turn) for any module or campaign opener.
- **Tells as leverage**: a general rule of thumb in MM2 that established facts about an antagonist step its difficulty down, one tell = one step, capped at Easy. This is the Fracture mechanic generalised and it is already how the difficulty ladder is supposed to be used.
- **Printed rewards**: a module template that lists its Spark triggers on the page.
- **Opt-in steel** and **guards are a scene, not a sentence** as named MM patterns.
- The three novice-MM errors from §8.3 as a sidebar: default to Standard, a 7-9 is a cost not a penalty, there is no turn order.
- Then scope a **second module that is the combat and magic test case**: a three-encounter night with a domain caster in the pregens, a Boss whose phase the party will see, Techniques in hand by the second session. Until that exists the flagship mechanics have no flagship content.

### R7. Show the enemy texture you already built. *(Prose only.)*

Rewrite the III.3 Guardian vignette so the Boss changes stance once (a conduct trigger), visibly clears Open once (the anti-snowball move MM1 describes), and lands one Technique. Require every Named or Boss in a core-book example to carry at least one trigger and one Technique. The Bestiary already does this for 10 of 12; the book that teaches the exchange does not.

### R8. Schedule IV.2 as consumables first. *(Roadmap.)*

The largest unbuilt fun driver in the hobby. The version that fits this game's "no arithmetic" rule is one-use items with a named effect that rotate through the party (Cypher's principle, not its text): a charge that makes one reaction free, a draught that treats a Tier 2 Condition mid-scene, a token that lets you offer yourself Borrowed Trouble. Oraga's crystal charges are already this. Permanent +1 gear is the thing to keep refusing.

### R9. Measure Spark flow before adding a third lever. *(No change.)*

Reset-to-3 and the natural-12 incentive are both designed to fix hoarding and both are unplayed. R1 measures them.

### R10. The four single-skill attributes. *(Planner question.)*

Constitution, Knowledge, Luck and Spirit each govern one skill; Luck is dead on a Body sheet. Either accept it as the cost of nine attributes, or let Gamble be a Body-rollable skill in the fiction it already describes. Hand to Planner with PT08's F2 as the brief.

### Do not do

- Do not add hit points, damage dice, initiative, a grid, enemy rolls, a fourth outcome tier, or a persistent Tier 1 Condition. Every one of these was considered and rejected for reasons the books record well.
- Do not lengthen fights by raising Resolve. The sims already showed that buys exchanges, not tension.
- Do not add a Spark-resist rule (R4's rejected form).
- Do not build for the Tactician at the Storyteller's expense. R2 and R3 are the size of change that gives the Tactician a reason to stay without changing who the game is for.

---

## 10. What to hand down

If the owner wants to act, the Brain output that constrains the next tier is:

- **`docs/BRIEF_fun_second_act.md`** covering R2 + R3 (+ R7 as the prose that shows them), with the sim acceptance bands (solo Boss median 3, Standard recipe win rate held at 65-85%, decisions-per-exchange counted in the sim log) and the explicit non-goal of touching anything in §3.
- **R1** needs no brief; it needs a table. The instrumented scenario for Session B can be a Planner task off `docs/DESIGN_agentic_playtests.md`'s harness.
- **R4** is an owner ruling; the two options are stated above.
- **R6** is MM Manual work a Worker can take from this document directly.

**Resolved.** This audit changes no rules text. Return to the owner for the R1/R4 decisions; then to Planner for the BRIEF if R2/R3 are adopted.
