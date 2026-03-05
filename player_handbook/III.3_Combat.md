# Rules: Combat

## The Shape of a Fight

Most TTRPG combat systems hand you a turn. You wait. You act. You wait again. The monster acts. You wait some more. This is not how fights feel, and it is not how this system works.

Combat in Facets of Origin is structured around **exchanges** — dramatic beats where everyone acts and reacts simultaneously. There is no initiative order, no waiting for your moment while someone else's moment stretches on. Every participant in a fight is present every exchange: choosing a posture, taking action, responding to incoming threats. The whole thing resolves as a single beat of fiction, then the MM narrates what actually happened.

The central resource in combat is **Endurance** — your physical stamina, the reserve of effort that lets you press hard or react quickly when it matters. Endurance is not hit points. It is not how much damage you can absorb. It is how much you have in the tank. A character with no Endurance left is not bleeding out — they are exhausted, overextended, outmaneuvered. They can still fight. They are simply fighting on grit alone.

**Conditions** replace hit points as the measure of how a fight is going. They are named states with immediate mechanical and fictional weight: you are not "at 14 HP," you are Staggered — your offensive rolls suffer. Conditions are concrete, narratively rich, and temporary by design. They resolve when the fiction resolves them, not on a countdown.

The goal is a combat system where every participant is engaged every moment, where the choices feel real, where a mage and a warrior and a nimble rogue all have meaningful roles — and where the fiction of the fight is always more interesting than the arithmetic.

---

## Endurance

**Endurance** is your combat stamina. You spend it to react to incoming attacks and to press hard on offense. When you run out, your options narrow sharply.

### Calculating Your Endurance Pool

| Component | Value |
|---|---|
| Base | 4 |
| Constitution 1 (Weak) | −1 |
| Constitution 2 (Average) | +0 |
| Constitution 3 (Strong) | +1 |
| Endurance skill: Novice | +0 |
| Endurance skill: Practiced | +1 |
| Endurance skill: Expert | +2 |
| Endurance skill: Master | +3 |

A character with no particular investment in Constitution or the Endurance skill has a pool of 4. A heavily invested character tops out at 8. The range in practice is 3 (fragile but fast) to 8 (a deliberate, durable choice).

> **Example pools:**
> Mordai — Constitution 3 (+1), Endurance Practiced (+1): **6 Endurance**
> Zahna — Constitution 2 (+0), Endurance Novice (+0): **4 Endurance**
> Zulnut — Constitution 1 (−1), Endurance Novice (+0): **3 Endurance**

### Running Out of Endurance

When your Endurance hits 0, you cannot spend it on reactions. You may still declare Postures and attempt to Dodge or Parry, but with nothing in the tank you cannot pay the cost — **Absorb** is your only reaction option. You remain in the fight until Conditions remove you.

### Recovering Endurance

**Withdrawn posture** restores 2 Endurance at the end of the exchange. This requires giving up all offensive action for that beat — you are catching your breath, finding your footing, creating space between yourself and the pressure.

---

## The Exchange

A combat **exchange** is one dramatic beat — a moment of the fight where every participant is choosing their approach simultaneously and the action resolves together.

### How an Exchange Runs

1. **The MM describes the situation.** Where is everyone? What has just happened? What does the opposition look like right now?

2. **All participants simultaneously declare Posture.** In a live session, the digital app handles blind reveal — everyone declares at the same time, then the table sees all Postures together. At a physical table, players can write postures on slips of paper and reveal them at once.

3. **Actions and reactions are declared and resolved.** Each participant takes an offensive action, a support action, or passes. Targets of those actions may declare reactions. Rolls happen.

4. **End-of-exchange cleanup.** Tier 1 Conditions clear. Withdrawn characters recover 2 Endurance.

5. **The MM narrates the exchange as a single dramatic beat.** The dice have told you what happened mechanically; the MM tells you what it looked like.

Exchanges are fast in the fiction. A full exchange — everyone acting, everyone reacting, the whole beat — represents a few seconds of intense, chaotic activity. The fight's pacing should feel like that.

---

## Postures

Before actions are declared each exchange, every participant (player characters and significant antagonists alike) simultaneously declares a **Posture**: the broad tactical stance they are taking for this beat of the fight.

Posture is declared blind. You do not know what your opponent has declared until everyone reveals at once. Reading the situation, anticipating the opposition, and matching your posture to the moment is half the tactical game.

| Posture | Offense | Reactions | Other |
|---|---|---|---|
| **Aggressive** | +1 to offensive rolls | +1 Endurance cost per reaction | You are pressing hard — and exposed for it |
| **Measured** | No modifier | Standard cost | The baseline — flexible and uncommitted |
| **Defensive** | −1 to offensive rolls | −1 Endurance cost per reaction (min 0) | Trading offensive presence for resilience |
| **Withdrawn** | Cannot make offensive actions | All reactions are free | Recover 2 Endurance at end of exchange |

**Aggressive:** You are driving the action. Everything you do this exchange hits harder and faster. Everything done to you finds you slightly over-committed. Useful when you have momentum and Endurance to spend; dangerous when you don't.

**Measured:** The default. You have not handed your opponent an advantage. You have not bought yourself a discount, either. Measured posture is for when you want options.

**Defensive:** You are absorbing pressure and waiting for your moment. Your reactions cost less, but your offense is blunted. Useful when you're taking heavy fire and need to last longer than you need to hit harder.

**Withdrawn:** You are out of the press entirely — creating space, catching breath, declining to engage. You can still react to incoming attacks, and those reactions are free. But you are going nowhere. The fight is happening without you for this beat.

> **Reading the opponent:** Posture is declared blind, but it is not declared blind of all information. A character with high Wisdom or the Insight skill can read body language, stance, and the micro-signals an opponent broadcasts before they commit. Before declaration, a player can ask the MM: *"Does anything about how they're carrying themselves suggest what posture they're about to declare?"* The MM is not obligated to answer precisely — but they should give an honest read of what an attentive character would notice. A skilled fighter telegraphs less. A wounded one telegraphs more. A creature built for ambush telegraphs nothing at all, and that too is information.

---

## Offensive Actions

On your action in an exchange, you may do one of the following. You may only take an offensive action if your Posture allows it (Withdrawn cannot attack).

---

### Strike

The foundational offensive action. You bring force to bear on a target — weapon, fist, magic, momentum.

**Roll:** `2d6 + Strength modifier + Combat skill rank modifier`

**Difficulty** is Standard by default. The MM adjusts based on the situation: an opponent in Defensive Posture, or with strong Constitution, may push it to Hard. A Staggered, Cornered, or Spent opponent may make it Easy. When in doubt, Standard.

| Result | Outcome |
|---|---|
| **10+** | Full success. Apply a **Tier 2 Condition** to the target. |
| **7–9** | Partial success. Apply a **Tier 1 Condition** to the target. |
| **6−** | Something goes wrong. The MM narrates a consequence for the attacker — a stumble, an opening left, a weapon out of position. |

The attacker chooses which Condition to apply, within the appropriate tier. The choice should fit the fiction of the moment — a blade-fighter landing a precise blow might apply Staggered; one forcing an opponent into a corner might apply Cornered.

---

### Press

Before rolling a Strike, you may spend **1 Endurance** to add 1d6 to the roll and drop the lowest die. This is the same mechanical effect as spending a Spark, drawing from a completely different resource — going in hard costs stamina.

**Press and Sparks stack.** You may spend 1 Endurance for Press and also spend a Spark on the same roll. A character who Presses and Sparks rolls 4d6 and drops the two lowest.

Pressing when your Endurance is already low is a calculation. The dice improvement is real. So is the cost.

---

### Maneuver

You use your action to reshape the fight rather than deal damage directly. Force a disadvantage, create an opening, change the terrain, outflank an opponent, disarm.

**Roll:** The relevant skill for the action — Athletics to bull rush someone into a bad position, Finesse to disarm, Stealth to vanish and reposition, an appropriate attribute for improvised environmental play.

A successful Maneuver does not apply Conditions directly. Instead, it shifts difficulty: on a 10+, the target's next roll is Hard (or the party's next roll against them is Easy). On a 7–9, the repositioning works but at a cost — you may be exposed, or the effect is smaller. On a 6−, the attempt backfires.

Maneuvering well opens fights. It is the action for characters who think geometrically about combat, and for anyone helping a hard-hitting ally land the blow that matters.

---

### Support

You use your action to aid another participant rather than act directly. You grant an ally an extra die (they roll an extra d6 and drop the lowest on their next roll), or reduce the difficulty of their next roll by one step.

**Roll:** The relevant skill for the manner of support — Insight to read the fight and pass critical information, Attune to channel force through an ally, Persuade to issue a command that breaks a target's concentration. Mind and Soul characters provide most of their combat value through Support and the creative application of their domains. This is not a lesser option. An ally with a boosted roll is more effective than two characters swinging blind.

---

## Reactions

When an opponent takes action against you, you may **react**. You may declare a maximum of **one reaction per incoming action**. Each reaction costs Endurance unless your Posture reduces the cost. If your Endurance is at 0, only Absorb is available.

The choice to react, and which reaction to use, is made after the attacker rolls but before any Condition is formally applied.

---

### Dodge

**Cost:** 1 Endurance

You move — out, aside, low — using speed and awareness to take yourself out of the path of what's coming.

**Roll:** `2d6 + Dexterity modifier`

| Result | Outcome |
|---|---|
| **10+** | The attack misses entirely. No Condition applied. |
| **7–9** | Partially avoided. Downgrade the incoming Condition by one tier (Tier 2 becomes Tier 1; Tier 1 has no mechanical effect). |
| **6−** | The dodge fails. Full Condition applies. |

---

### Parry

**Cost:** 1 Endurance

You meet force with force — interposing weapon, shield, or forearm to deflect rather than avoid.

**Roll:** `2d6 + Strength modifier + Combat skill rank modifier`

Outcome tiers are the same as Dodge, flavored as deflection rather than avoidance.

---

### Absorb

**Cost:** 0 Endurance

You do not react. You take the hit, accept the Condition, and remain composed. Absorb is the reaction for when Endurance is gone or better spent elsewhere. It is not failure; it is calculation.

---

### Intercept

**Cost:** 2 Endurance

You step in front of an attack targeting an ally. You take the incoming action instead of them, then roll Dodge or Parry as normal.

Intercepting is how you protect someone who cannot protect themselves — a Spent ally, a mage mid-cast, someone whose low Endurance pool is about to become a serious problem.

---

## Conditions

Conditions replace hit points as the measure of how a fight is going. A character is not at "14 HP" — they are **Staggered**, and that means something concrete in both the mechanics and the fiction.

### Tier 1 Conditions

Applied by partial Strike successes (7–9). **Tier 1 Conditions clear automatically at the end of the exchange.**

| Condition | Effect |
|---|---|
| **Winded** | −1 to your next roll |
| **Off-Balance** | Your next reaction costs 1 additional Endurance |
| **Shaken** | The MM may direct your next action — you flinch, hesitate, or briefly retreat |

Tier 1 Conditions are the texture of a fight — they shift the next beat without defining the outcome.

---

### Tier 2 Conditions

Applied by full Strike successes (10+). **Tier 2 Conditions persist until a narrative action addresses them** — binding a wound, catching full breath during a Withdrawn exchange, receiving aid from an ally, or any fictional activity that genuinely resolves the condition's cause.

| Condition | Effect |
|---|---|
| **Staggered** | −1 to offensive rolls |
| **Cornered** | Cannot take Aggressive posture; the MM has narrative authority over your positioning |

Tier 2 Conditions stack. A character who is both Staggered and Cornered is in genuine trouble — their offense is blunted and they have lost control of the ground they're fighting on.

**Stacking the same Condition:** If a character receives a Tier 2 Condition they already have, it escalates immediately to **Broken**.

---

### Tier 3: Broken

**Broken** means out of the fight. The fiction determines exactly what this looks like — defeated, unconscious, fled, captured, surrendered, collapsed. The character is no longer a participant in this conflict.

Broken persists until the end of the scene. Full recovery requires meaningful downtime.

---

### Condition Summary

| Tier | Conditions | Duration | Applied By |
|---|---|---|---|
| **Tier 1** | Winded, Off-Balance, Shaken | Clears end of exchange | Partial Strike (7–9) |
| **Tier 2** | Staggered, Cornered | Persists until treated | Full Strike (10+) |
| **Tier 3** | Broken | End of scene; downtime to recover | Second of same Tier 2; specific Techniques |

---

## Armor

**Armor** reduces the severity of incoming Conditions. It does not eliminate Conditions — it softens them.

- **Light armor:** Incoming Tier 2 Conditions become Tier 1 Conditions. A Strike that would apply Staggered applies Winded instead.
- **Heavy armor:** Incoming Tier 3 (Broken) becomes Tier 2 instead. A strike that would break an unarmored character leaves an armored one Staggered and Cornered — still badly hurt, but still in the fight.

Armor affects incoming severity, not the roll itself. An attacker still rolls Strike and interprets their result normally; the Condition they apply is simply reduced one tier before it lands.

Armor has fictional weight beyond its mechanical effect. Heavy armor announces your presence, imposes noise and heat, and affects how you move through the world outside of combat. The Equipment chapter covers specific armor types, weights, and any relevant Technique interactions.

---

## Facing Mooks and Named Antagonists

Not every fight deserves the same structure. The rules scale to the significance of what you are facing.

### Mooks

**Mooks** are minor antagonists: guards, hired muscle, ordinary soldiers, common bandits. They exist to create pressure and numbers, not to require sustained individual attention.

- Mooks have no Endurance pool and no Condition track.
- One successful Strike — at any tier — removes a Mook from the fight.
- Mooks do not react. They apply pressure through volume and positioning, not through the full exchange structure.

The MM narrates Mook combat efficiently. Mordai cutting through two guards on his way to the named antagonist across the room is not two separate Strike exchanges — it is one action, one roll, two Mooks handled. Save the full mechanical weight for fights that deserve it.

> **Mooks as roleplay opportunities:** Mooks fall fast, but they can still talk. A guard who drops their weapon and holds up their hands is a Mook who has just become a source of information, a witness, a potential ally, or a moral complication. The party's decision about what to do with a surrendering Mook is often more interesting than the Strike that got them there. Give the table a beat to make that choice.

### Named NPCs

**Named NPCs and significant antagonists** use the full combat structure: Endurance pool, Posture, Condition track, the works. They are opponents whose defeat means something and whose capabilities should be genuinely felt.

A Named NPC is defined by:
- **Endurance pool** — built the same way as a player character
- **A primary attribute and skill** — the modifier they use for Strikes and Parries
- **Armor**, if any
- **Techniques**, if the MM wants them to have specific capabilities

Named NPCs do not need a full character sheet. A veteran soldier might be: Endurance 6, Strength +1, Combat Practiced (+1), Light armor. That is enough to run the full exchange structure against a party.

### Bosses and Climactic Antagonists

**Bosses** — the antagonists at the center of major conflicts — may have higher Endurance, multiple Condition tracks, or **phase changes**: narrative triggers when a specific Condition is applied that shift the nature of the fight. A creature that becomes more dangerous when Cornered, or that reveals a second form when first Broken, is following this structure.

Boss construction is covered in the Mirror Master's chapter. For now: a climactic antagonist should not fall to the same two-exchange sequence that ends a Mook. Build them to last, and build the moment of their defeat to matter.

---

## Magic in Combat

Magical effects in combat use the **Domain + Intent + Scope** framework from Chapter II.3. Roll Spirit (intuitive magic) or Knowledge (scholarly magic); the MM sets difficulty based on scope and the opposition. Magical Strikes apply Conditions using the same tier framework as physical Strikes. Full integration rules are in **Chapter II.3**.

---

## Mind and Soul in a Fight

A character whose primary development is in Mind or Soul is not helpless in combat. They are playing a different game in the same space — one that is often more decisive than trading Strike for Strike.

**Insight (Wisdom):** Read the opposition's likely Posture before it is revealed. A successful Insight roll at the start of an exchange gives you information — their body language, their positioning, the tension in their stance. That information is genuinely useful when Posture is declared blind.

**Attune (Spirit):** Channel your domain's force as a direct Strike. Spirit is the roll for intuitive magical attacks. Domain + Intent + Scope sets the difficulty; the Condition tier follows the Strike outcome table.

**Investigate (Intelligence):** Find the structural weakness in the fight — a bad angle, a compromised footing, an environmental factor the enemy hasn't noticed. A successful Investigate roll translates directly into a difficulty modifier on the party's next actions against that target.

**Gamble (Luck):** Spend a Spark and take a Reckless Press — add a die to a risky action the way Press adds a die through Endurance. Luck-touched characters bend probability; they should lean into that in combat as much as anywhere.

**Persuade (Charisma):** End the fight before it ends you. A successful Persuade during a combat exchange can demoralize, redirect, or straight-out stop an opponent who has a reason to stop. This requires a genuine in-fiction basis — an enemy who has no reason to listen will not listen — but talking your way out of a fight is a full, valid, mechanically supported option.

> **MM guidance: rewarding creative lateral play**
>
> When a player does something genuinely unexpected with the environment, their domain, or the fictional situation — rather than the optimal tactical move — the MM has a responsibility to make it work *better* than the obvious choice, not just equally well.
>
> Practical patterns:
> - When a player uses the environment (a chandelier, a barrel of pitch, a collapsing railing), drop the difficulty one step. They earned it by paying attention.
> - When a player's creative approach makes the situation *stranger* rather than simpler, award a Spark.
> - When an approach solves the fight in a way you didn't plan — let it. The encounter you improvise from the wreckage will be better than the one you had prepared.
>
> The 7–9 on a creative lateral action should almost always be *the thing works, but it changes the situation in a new direction* — not *the thing is partially blocked*.

---

## In Play: The Archive's Guardian

*The party has entered the lower archives of the Thornwall Municipal Archive. The door is open behind them. The light inside has been waiting.*

---

**MM:** "The room is maybe thirty feet across. Stone floor, shelves on three walls, all of them empty — whatever was filed here has long since been moved or destroyed. In the center of the room there is a figure. Humanoid shape, iron-jointed, standing exactly as still as something that has been standing in the same spot for fifteen years. It is watching the door. It is watching you. It has the proportions of a person and the material certainty of a vault."

*The guardian's eyes — if they are eyes — don't reflect the light. They are the light.*

**MM:** "It says nothing. It takes one step toward you. The floor does not shake. It doesn't need to."

**Mordai:** "I draw my blade."

**Zahna:** "I'm reading its structure. Does it look like something I've seen in an archive record? Knowledge check?"

(The MM does not begrudge Zahna this reflex. Zahna will always try to understand the thing before anyone hits it.)

**MM:** "Hard — fifteen-year-old notes about a sealed room, not a standard catalog entry. Roll it."

→ Zahna rolls **2d6 + Knowledge (3 → +1)** against Hard difficulty (net +0) and gets a **7**. Partial success.

**MM:** "It's a Constructed guardian — you recognize the joint configuration from the Artificers' Guild technical records, the series that was commissioned by the city before the Guild dissolved. They were designed to hold a position. Not to pursue. But the one thing you couldn't get from those records is whether it can tell the difference between an authorized visitor and a not-authorized one."

**Zahna:** "Is that the encouraging or discouraging reading of this situation?"

**MM:** "Yes. It takes another step. Combat this exchange. Declare Postures."

---

**MM:** "Postures — simultaneously."

**Mordai:** "Aggressive."

**Zulnut:** "Defensive." *(Quietly, to nobody in particular:)* "I have three Endurance."

**Zahna:** "Measured. I'm looking for an opening — something I can use."

*All three Postures revealed. The guardian's flat approach gives away nothing.*

---

**MM:** "Mordai, it's moving straight at you. It reads you as the threat in the room — you're the one with the drawn blade. Your action."

**Mordai:** "I want to test it — a strike at the joint between its shoulder and arm. I have Weapon Mastery in blades."

**MM:** "Standard difficulty, but Weapon Mastery makes this one step easier, so Easy. Roll Combat."

→ Mordai rolls **2d6 + Strength (3 → +1) + Combat Practiced (+1)** against Easy difficulty (+1) and gets a **12**. Full success.

**MM:** "The blade finds the seam. Exactly the seam. There is a sound like a key turning in a lock that has not been oiled in fifteen years — grinding, then a kind of hollow click. The arm does not fall off. But it is not doing what it was doing before. The guardian is **Staggered**: its strikes take −1."

*The guardian rotates toward Mordai with the patience of something that was not designed to feel surprise. It reaches for him anyway.*

**MM:** "It's striking back, Mordai. Declare a reaction."

**Mordai:** "Parry."

**MM:** "1 Endurance — you're at 5. Roll Combat."

→ Mordai rolls **2d6 + Strength (3 → +1) + Combat Practiced (+1)** and gets a **9**. Partial success.

**MM:** "You catch the blow — the blade turns it — but the force behind that arm is not organic. Your whole side rings. You take **Off-Balance**: your next reaction costs 1 additional Endurance."

*Mordai staggers half a step. His arm is still working. He is not sure for how long.*

---

**MM:** "Zulnut. The guardian hasn't registered you yet as a threat — you're behind Mordai's noise. What are you doing?"

**Zulnut:** "I'm watching. Waiting. Where is it weakest — the joints, the chest, something at the base?"

**MM:** "You're supporting — Insight to read the fight?"

**Zulnut:** "Finesse, actually. I'm looking at how it moves. Where it's compensating."

**MM:** "I'll take that. Standard. Roll Dexterity plus Finesse."

→ Zulnut rolls **2d6 + Dexterity (3 → +1) + Finesse Practiced (+1)** at Standard difficulty and gets an **11**. Full success.

**MM:** "It's leading with the left. Right arm is structurally compromised — Mordai's hit moved something inside the joint — and the thing is routing its force through the left side to compensate. Whoever goes for the left joint next rolls at Easy."

**Zulnut:** "I tell Mordai. Very quietly, while it's not looking at me."

**Zulnut:** "Left side. Next time."

---

**MM:** "Zahna. You are in the back of the room with your Inscription domain and you have been waiting for me to get to you."

**Zahna:** "Fifteen years this thing has been standing here. It was given a set of instructions at the beginning and it has been running on them. I want to write a counter-instruction — a glyph that interferes with its trigger condition. Minor scope. Focused domain — Easy difficulty."

**MM:** "What's the intent?"

**Zahna:** "I inscribe a glyph on the floor between it and the door. The trigger condition is: if the guardian crosses this line while moving toward the exit, it interprets its own movement as unauthorized departure from the protected space and stops."

(The MM stops. This is either extremely clever or the kind of thing that escalates a fight in an interesting direction. Probably both.)

**MM:** "I love this. Hard — not because the magic is complicated, but because you're writing this during an active fight with thirty seconds of prep time. Roll Knowledge."

→ Zahna rolls **2d6 + Knowledge (3 → +1)** against Hard difficulty (net +0) and gets an **8**. Partial success.

**MM:** "The glyph takes. But you had to compromise — the instruction is less specific than you wanted. It will stop the guardian from leaving, but it reads 'unauthorized departure from position' broadly. Right now, that includes the guardian and also anyone standing in the rough area of the room it considers its patrol zone." *A beat.* "Which is the room you are all currently in."

**Zahna:** "I may have made our retreat more complicated."

**Zulnut:** "How much more."

**Zahna:** "Measurably."

*End-of-exchange cleanup: Off-Balance on Mordai clears. Mordai's Staggered on the guardian persists.*

---

**MM:** "Second exchange. Postures."

**Mordai:** "Aggressive. I have the left side open."

**Zulnut:** "Still Defensive. Three Endurance."

**Zahna:** "Measured."

**MM:** "The guardian is Measured. It is learning you. Mordai — left joint, Easy difficulty from Zulnut's read. Roll Combat."

→ Mordai Presses: spends 1 Endurance (now at 4) and rolls **3d6 + Strength (3 → +1) + Combat Practiced (+1)** at Easy difficulty (+1), drops the lowest die, and gets a **13**. Full success.

**MM:** "The left joint goes the way the right one went, but worse. There is a grinding sound that the room holds for a moment, and then the guardian's movement pattern simply — stops. Not falls. Stops. It is standing. It is looking at you. It is **Staggered** again — which means a second Staggered on top of an existing Staggered."

*Second Tier 2 Condition of the same type.*

**MM:** "That escalates. The guardian is **Broken**."

*The light in its eyes does not go out. It dims. The figure settles — not collapses, settles — to one knee, and then to both, with the deliberate patience of something that has decided to stop.*

*It has not surrendered. It has reached the end of the instructions it was given fifteen years ago and has no further direction.*

---

**MM:** "The room is quiet. The guardian is kneeling. It is still watching the door — your door, the one you came in through. Mordai, you are at 4 Endurance. Zahna, the glyph is on the floor."

**Zahna:** "I inspect the glyph. Can I refine the patrol boundary now that the fight is over?"

**MM:** "Yes. Easy. Take your time."

**Zulnut:** "Good. I'll be outside." *He looks at the kneeling figure.* "Probably."

**Mordai:** "We cannot just leave it."

**Zulnut:** "It kneeled."

**Mordai:** "It also tried to crush my arm."

**Zahna:** "It was doing its job. Fifteen years, faithfully. That is actually somewhat admirable."

(The MM has been waiting for Zahna to say something like this. It is extremely on-brand.)

**Zulnut:** "Can we come back to the disappearances."

**Zahna:** "Yes. Right. The records." *He steps carefully around the guardian, which does not move.* "The answers we came for are in this room. I am going to find them. And then I am going to understand what this thing was protecting and why the Governor's office sealed it, and then I am going to make a very carefully considered decision about what we do with both."

*He begins searching the shelves.*

*Behind him, the guardian watches the door.*

*The light in its eyes has steadied.*

---

*(The MM had planned for this fight to last three exchanges. It lasted two because Mordai hit the same joint twice and Zahna locked the room. The glyph on the floor will matter later. These things always do.)*
