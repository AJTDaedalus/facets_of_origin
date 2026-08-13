# RESEARCH — Have We Oversimplified? A Fun-Gap Analysis

**Date:** 2026-08-11
**Question (owner):** *"Investigate if we've oversimplified to the point of making it not
fun. If there's anything not a huge jump in complexity that would add a big payoff in
fun, we can entertain that. Compare our system to other popular systems and see if
there's anything standing out that we do in a different way that may be less fun."*
**Status:** Items 1, 2 and 5 **implemented** (2026-08-13, owner: *"implement these"*).
Item 3 still needs a ruling; item 4 waits on playtest. See *Outcome* at the foot.

---

## Verdict up front

**The core is not oversimplified.** 2d6, three tiers, one resolution mechanic, no
initiative, NPCs never roll, no spell lists — every one of those is a deliberate
subtraction that the market has validated, and `research/dice_system_analysis.md`
argues each of them well. Do not undo any of them.

The problem is not that we removed too much. It is that **we removed the ceiling and
never put anything back.** Three specific things the field uses to generate the moments
players actually remember are absent from our system, and two of them are named as
goals in our own research doc and then never built.

Ranked by payoff per unit of added complexity:

| # | Gap | Complexity to fix | Payoff |
|---|---|---|---|
| 1 | No critical success — a natural 12 is just a 10 | One table row. No new arithmetic | Highest |
| 2 | No player-authored complication (Devil's Bargain) | One paragraph, reuses the Spark dice rule | Highest |
| 3 | No post-roll agency outside combat | Moderate — and conflicts with a recorded decision | High, contested |
| 4 | Session-1 characters are barely distinctive, worst for Body | Moderate | Medium |
| 5 | Social is the thinnest pillar structurally | MM guidance only, no new rules | Medium |

---

## 1. There is no peak. A natural 12 is a natural 10.

**Verified:** `facet.yaml`'s `roll_resolution` has exactly two thresholds (10 and 7) and
three outcomes. `engine.py` carries the same. Nothing anywhere in the ruleset, engine, or
books reacts to the top of the dice. A player who rolls boxcars at the climax of a
campaign gets the identical text as a player who rolled 6+4.

**This is the one gap our own research predicted would hurt.**
`research/dice_system_analysis.md` §*The Psychology of Dice*:

> **Social memory generation is a design goal, not a side effect.** Near-TPKs,
> **critical successes at crucial moments**, and dramatic failures that everyone
> remembers are flashbulb memories (Brown & Kulik). They become group mythology and are
> the primary reason players keep returning to the same group for years.

We built the dramatic failures (Graceful Fail, the 6- templates, the Trouble Table). We
built the near-misses (the 7–9 band is the modal outcome). We never built the third one.

**What the field does.** Blades in the Dark resolves a critical as *"You do it with
**increased effect**"* — no new subsystem, just a better result. D&D 5e's natural 20 is
the single most recognisable moment in the hobby. PbtA games commonly add a 12+ band on
individual moves.

**Recommendation — natural 12, not total 12+.** A *total* 12+ tier scales with modifiers:
a character at +3 would crit on 28% of rolls, which both dilutes the moment and adds a
fourth tier to every difficulty call. A **natural 12 — both kept dice showing 6** — costs
nothing at the table (you already see boxcars), stays constant at any competence, and has
one property that makes it fit our system specifically:

| Roll | Chance of natural 12 |
|---|---|
| 2d6 | 1 in 36 — **2.8%** |
| 3d6 drop lowest (1 Spark) | 16 in 216 — **7.4%**, 2.7× more likely |

Spending a Spark nearly triples your chance at the table's best moment. That is a reason
to spend rather than hoard, which is the exact behavioural problem playtest 01 found.

**The symmetric case is free.** A natural 2 is already a 6-, so it needs no new tier — but
"on a natural 2, the Graceful Fail is automatically confirmed" turns the worst roll on the
table into a guaranteed reward, costs one sentence, and is precisely on-brand for a game
whose thesis is that the story always moves forward. Note that a Spark makes a natural 2
nearly impossible (1 in 216 — all three dice must show 1), so Sparks protect against the
floor as well as reaching for the ceiling.

---

## 2. There is no way to buy a die by accepting trouble

Our research doc, evaluating the Spark system it went on to recommend:

> **Market comparison:** Similar to Blades in the Dark's **devil's bargain** + stress
> system, but simpler.

We implemented the resource-spend half and not the bargain half. Sparks are earned for
good behaviour and spent for dice. There is no mechanism anywhere in the system for a
player to *manufacture* an advantage by accepting a complication.

**What Blades does.** The GM or any other player may offer a bonus die in exchange for a
complication; the player may accept or decline. Critically, **the complication happens
regardless of whether the roll succeeds** — you are not buying a chance, you are selling
a piece of your own future. The design commentary is consistent that this is one of the
game's strongest engines: it "mechanises table culture practices we love," and it lets
players "inject a complication into the story in order to augment their chances."

**Why it fits us unusually well.**

- It reuses our existing dice rule **exactly** — add a d6, drop the lowest. No new
  arithmetic, no new tier, nothing to memorise.
- It needs no economy. It is always available, so it does not compete with the Spark
  budget or require earning — which directly addresses the hoarding problem.
- It hands the MM a pressure valve that is *offered*, not imposed, so it never reads as
  the MM punishing a player.
- It generates fiction rather than consuming it, which is the stated project priority.

**Cost:** one paragraph in III.1 and a row on the MM5 card. This is the best
complexity-to-payoff ratio in the document.

---

## 3. Once the dice land, nothing can be done — outside combat

**Verified:** III.1 states *"Sparks are always spent **before** you roll — there is no
spending a Spark after you see the result."* In combat you have reactions, which mitigate
after a hit is declared. Outside combat there is no equivalent at all. A 6- on a social
or exploration roll is final the instant it lands.

**What Blades does.** The **resistance roll** happens *after* the GM announces a
consequence: you spend stress and reduce or avoid it. It is one of the most-praised
mechanics in modern design precisely because it puts a decision after the dice.

**The honest tension.** Our pre-roll-only rule is a recorded, well-grounded choice — the
research doc cites Ladouceur & Sévigny on pre-roll agency converting frustration into
drama. But read it again: it argues *for* pre-roll agency. It never argues *against*
post-roll agency. They are not alternatives; Blades has both.

**This is the one item I would not act on without a ruling.** Adding post-roll mitigation
would soften the tension the current rule buys. Options, cheapest first:

- **(a) Do nothing.** Combat reactions are the post-roll layer; other pillars accept
  finality as the price of tension.
- **(b) Devil's Bargain only** (item 2). Adds authored complications without touching
  the pre-roll rule. My recommendation if you want one change here.
- **(c) A Spark resists.** After a 6-, spend a Spark to downgrade it to a 7–9. One
  sentence, enormous power, and it does undercut the pre-roll tension by making Sparks
  strictly better held than spent — the opposite of what item 1 achieves.

---

## 4. A session-one character has almost nothing distinctive

At creation a character holds: attributes, one skill at Practiced, one at Novice with a
mark, and a one-line Specialty. The first Technique arrives at Facet level 1.

**The comparison is unflattering.** D&D 5e gives class features at level 1 — Rage, Sneak
Attack, Second Wind, spellcasting. PbtA playbooks give two to four unique moves at
creation. Blades gives a special ability plus action ratings. In each, a player's *first*
session includes something only their character can do.

**And it is uneven in a way that tracks the Facets.** Of fifteen Backgrounds, three grant
a magic domain — an open-ended creative toy from session one. All three are Mind or Soul.
**Every Body Background grants skills and a Specialty and nothing else**, and Body has no
magic by ruling, so this cannot self-correct.

| Facet | Backgrounds | Grant a domain at session 1 |
|---|---|---|
| Body | 5 | **0** |
| Mind | 5 | 2 |
| Soul | 5 | 1 |

**Mitigated, not solved, by D16a.** Facet level 1 now lands around session 2–4 rather
than 4–8, so the wait for a first Technique is much shorter than it was. That materially
reduces the severity — this is a session-one problem now, not a first-arc problem.

**If we act:** give the five Body Backgrounds a distinctive non-magical knack of
comparable weight to a domain origin, rather than granting everyone a Technique at
creation (which would disturb the Technique economy the D16 work just settled).

---

## 5. Social is the thinnest pillar

Combat has postures, reactions, conditions, Resolve, Press, and armor. Exploration has
Threat Clocks and hazards (III.2). Magic has domain, intent, and scope, plus six
templates for what a 6- looks like. **Social has the bare 2d6 and nothing else.**

This is where "one resolution mechanic, learn it once" is paying its real cost. It is not
that social rolls are broken — it is that nothing about them *feels* like a negotiation
rather than a lockpick.

**This needs no new rules.** Magic's 6- templates and MM5's Trouble Table already prove
the pattern: outcome texture, not subsystems. A short table of what a 7–9 costs in a
social scene — *they agree but now they know you needed it; you get the name but owe a
favour; the room believes you and one person in it does not* — would give the pillar
character at zero mechanical weight. This is MM Manual guidance, not a rules change.

---

## Things we do differently that are *correct* — do not revisit

Worth recording so a future review does not relitigate them:

- **NPCs never roll.** Modern, reduces MM load, keeps players' hands on the dice.
- **No initiative; simultaneous exchanges.** Removes the single worst pacing tax in
  traditional combat.
- **No spell lists.** Domain + Intent + Scope is more creative and vastly less to
  maintain.
- **Failure always advances the story.** Correct, and well-implemented.
- **One resolution mechanic everywhere.** The cost is item 5; the benefit is a game
  someone can teach in ten minutes. Keep it.
- **The 7–9 band as modal outcome.** Straight from the strongest finding in the research.

## Explicitly out of scope here

**Loot and magical items.** `IV.2 Magical Items` is marked *Planned*, and the gear layer
today is thin — weapons set an attribute, armor gives a downgrade budget. Finding
treasure is one of the largest fun drivers in the hobby and we have essentially none of
it. That is a scope gap on the roadmap rather than an oversimplification, so it is noted
and not analysed.

**Downtime, crafting, economy.** Deferred to Facet modules by the PHB scope decision.
Blades' downtime phase is a major fun engine; when those modules are written, that is the
comparison to make.

---

## Recommendation

Take **items 1 and 2** — natural 12 and the Devil's Bargain. Together they are perhaps
fifteen lines of rules text, add no new arithmetic, no new tier to any difficulty call,
and no new resource. They restore the peak the research doc predicted we would miss, and
they give players a way to author their own trouble.

Take **item 5** as MM guidance in the same pass — free, and it fixes the weakest pillar.

**Item 3 needs an owner ruling** before anything is written: it trades against a recorded
design decision, and my read is that (b) — Devil's Bargain only — captures most of the
value without paying that price.

**Item 4** is the most real of the remaining gaps but the most expensive, and D16a already
softened it. Worth doing after a playtest confirms Body characters actually feel flat in
session one, rather than on this analysis alone.

---

## Sources

- [Action Roll — Blades in the Dark](https://bladesinthedark.com/action-roll) (critical = increased effect)
- [Resistance & Armor — Blades in the Dark](https://bladesinthedark.com/resistance-armor) (resistance roll, post-consequence)
- [Devil's Bargains — Blades in the Dark G+ archive](https://bitd.gplusarchive.online/2015/06/22/devils-bargains/)
- [Devil's Bargains — Dice Exploder](https://diceexploder.substack.com/p/devils-bargains-blades-in-the-dark)
- [Powered by the Apocalypse — Wikipedia](https://en.wikipedia.org/wiki/Powered_by_the_Apocalypse) (three-tier baseline)
- Internal: `research/dice_system_analysis.md`, `docs/RESEARCH_advancement_benchmark.md`

**Sourcing caveat:** PbtA's 12+ band is real but implemented per-move rather than
system-wide, and I could not confirm a single authoritative statement of it, so it is
cited as general context and carries no weight in the recommendation. The natural-12
proposal stands on the Blades precedent and our own research doc, not on PbtA.

---

## Outcome (2026-08-13)

Owner: *"implement these."* Items **1, 2 and 5** are built. Items 3 and 4 are untouched.

### Item 1 — the natural 12 and the natural 2

**Natural 12** — both *kept* dice showing 6 — is a full success regardless of modifiers
or difficulty, plus something more that **the player names and the MM confirms**. It is
keyed to the dice rather than the total, so it never inflates with competence and never
adds a tier to a difficulty call.

**Natural 2** — both kept dice showing 1 — auto-confirms the Graceful Fail when the roll
failed, and **never lowers an outcome tier**. The asymmetry is the point and is written
into the schema as a comment: promoting rewards, demoting punishes competence, which is
the d20 failure mode `dice_system_analysis.md` rejects. `NaturalResultDef.max_outcome`
exists and is deliberately left unset.

Because both are read off the kept dice, extra dice help twice over — a Spark makes the
crit 2.7x more likely and the fumble nearly impossible. That is a reason to spend rather
than hoard, which is the behaviour playtest 01 flagged.

### Item 2 — Borrowed Trouble

Offered before a roll by the MM *or any player*; accepted, it adds a d6 and drops the
lowest, exactly as a Spark. It costs no Spark, one per roll, and **the complication lands
whether the roll succeeds or fails** — the player is selling a piece of their near future,
not gambling. Offering and declining are both free. Stacks with Sparks and Press.

Named for the game rather than borrowed from Blades: "Devil's Bargain" carries a
cosmology Shattered Origin has not established.

### Item 5 — social outcome texture

MM2 gains *What a Social 7-9 Costs* — six shapes a social partial success takes (they
know you needed it / the debt / the witness / the narrower yes / the wrong believer / the
record), plus the ruling that a social 6- is almost never a refusal but a worse
relationship than the one you walked in with. Compressed onto the MM5 card. **No new
rules** — this is the same job the Magic 6- Templates already do.

### Still open

- **Item 3 (post-roll agency)** — needs an owner ruling. It trades against the recorded
  pre-roll-only decision. Borrowed Trouble was the recommended partial answer and is now
  in, so the remaining question is narrower: does anything mitigate a consequence *after*
  the dice, outside combat?
- **Item 4 (session-one distinctiveness, worst for Body)** — D16a already softened it.
  Worth a playtest before acting, specifically watching whether Body characters feel flat
  in their first session next to a Mind or Soul character holding a domain.
