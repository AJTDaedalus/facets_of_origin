# Mirror Master's Quick Reference

This chapter is for the middle of a session, not the week before one. Everything here is a compression of a rule that lives somewhere else — the section named beside each heading owns it. Nothing on these pages is new, and if a line here ever disagrees with the chapter it compresses, the chapter is right.

Keep it open. Look things up. Do not read it.

> **Through the Mirror — why a quick reference may never introduce a rule**
>
> We have already been bitten by this once. Two implementations of combat resolution drifted apart because both were treated as authoritative, and a corpus of recorded simulation numbers turned out to be measuring a rule set nobody had written down. A quick reference is the same hazard in prose: the moment a card states something its parent chapter does not, the game has two rules and the table is playing whichever one it read most recently.
>
> So this chapter compresses and never paraphrases, and a change to any rule updates the body text, every quick reference that touches it, `facet.yaml`, and the engine in the same commit. If you write your own reference card, inherit the discipline — a card that is allowed to say something new is a house rule with no author.

---

## Core Resolution

**Roll: 2d6 + Attribute Modifier + Skill Modifier + Difficulty Modifier**

**Table MM5–1: Outcome Tiers**

| Roll Total | Outcome |
|---|---|
| **10+** | **Full Success** — achieve goal cleanly |
| **7–9** | **Success with Cost** — succeed, but complication |
| **6-** | **Things Go Wrong** — story advances, not in player's favor |

**Natural 12** (both kept dice show 6): full success whatever the modifiers say, **plus something more the player names** and you confirm. Ignores difficulty.

**Natural 2** (both kept dice show 1): if the roll failed, the Graceful Fail is confirmed without the player asking. **Never lowers a tier** — a natural 2 that totalled 7 is still a partial success.

---

## Borrowed Trouble

Before a roll, you — or any player — may offer a complication. Accepted, it adds 1d6 drop lowest, exactly as a Spark. **It costs no Spark, and it happens whether the roll succeeds or fails.** One per roll; offering and declining are both free.

- Make it **specific and genuinely bad** — "you get seen" is an offer; "something bad happens later" is not
- Never take away the player's next choice; give them a new problem instead
- Once or twice a session, at moments already tense. Every roll turns a bargain into a tax
- Stacks with Sparks and Press (Press + Spark + Borrowed Trouble = 5d6 drop three)

---

## Modifiers at a Glance

### Attribute Ratings

**Table MM5–2: Attribute Ratings**

| Rating | Label | Modifier |
|---|---|---|
| 1 | Weak | -1 |
| 2 | Average | +0 |
| 3 | Strong | +1 |

### Difficulty

**Table MM5–3: Difficulty**

| Difficulty | Modifier | When |
|---|---|---|
| Easy | +1 | Clear advantage, weak opposition |
| Standard | +0 | Default — uncertain outcome |
| Hard | -1 | Skilled opposition, poor conditions |
| Very Hard | -2 | Extraordinary opposition, nearly impossible |

Adjustments apply in a fixed order: base from the situation → an Easy tag (an Open enemy, a Maneuver) overrides downward, never stacking with itself → at most **one** character-side step (Technique OR Specialty, whichever the player picks) → Support's step → Easy is the floor, Very Hard the ceiling. Carried triggers auto-apply; judgment-call triggers are player-declared (III.1 *Difficulty*; II.4 *Reading the Entries*).

### Skill Ranks

**Table MM5–4: Skill Ranks**

| Rank | Modifier |
|---|---|
| Novice | +0 |
| Practiced | +1 |
| Expert | +2 |
| Master | +3 |

---

## Sparks

- Earned via MM award, Act Break Nomination, peer nomination ("Spark?"), or a player-claimed Graceful Fail
- Spend **before** rolling: each Spark adds 1d6, drop lowest; no post-roll spending
- 1 Spark = 3d6 drop lowest; 2 Sparks = 4d6 drop two lowest
- Start of session: 3 Sparks per character — Sparks do not carry over
- **Graceful Fail:** player-initiated — on any 6-, the player may claim it by narrating how they make the failure worse or richer; MM confirms

### Spark Flow (MM Guidance)

The Spark economy works when Sparks flow — earned and spent regularly, not hoarded.

- **Target:** Confirm **1–2 Graceful Fail claims per session**, across the whole table.
- **Graceful Fail is your best tool.** Every 6- is an opportunity for the player to claim it. When a player leans into the consequence with commitment, confirm the Spark immediately. This creates a virtuous cycle: players spend Sparks because they expect to earn more.
- **Midpoint diagnostic:** If a player hasn't spent a Spark by the session's midpoint, design a moment that rewards it.
- **Hoarding is a behavioral problem, not a mechanical one.** Players who don't earn enough Sparks during play won't feel comfortable spending them — structured earning moments (Act Break Nomination, Graceful Fail) are the fix.

### Spark Earning

**Table MM5–5: Spark Earning**

| Trigger | Who Awards | Target/Session |
|---|---|---|
| **MM award / peer "Spark?"** (remarkable moments) | MM, or any player calls it and MM confirms | As they happen |
| **Act Break Nomination** | Players nominate each other | 2–3 per player |
| **Graceful Failure** (6- played for story) | Player claims, MM confirms | 1–2 across table |
| **Spark for Weakness** (played into flaw) | MM | 0–1 across table |

**Target economy** (by session type, everyone starting at 3): Low-activity — earn 1–2, spend 1–2. Standard — earn 2–3, spend 3–4. High-combat — earn 3–4, spend 4–6. Spend-what-you-earn: an unspent Spark at session end is simply gone (MM2, *Target Economy*).

---

## Combat: Exchange Flow

```
1. MM describes the situation
2. State enemy stances openly (from their `triggers:`); PCs declare Postures simultaneously, blind
3. Declare and resolve Actions (Strike / Maneuver / Support / Magic)
4. Targets declare and resolve Reactions
5. Apply results: deplete enemy Resolve (2 / 1 / 0), apply Conditions to characters, name the rider taken on a 10+
6. End of exchange: Tier 1 Conditions clear, Withdrawn recover 2 Endurance Pool points (up to the maximum)

An exchange with **no PC offensive action** is uncontested — the situation advances for free: reposition, reinforce, progress a clock, or take the objective. No roll.
```

---

## Postures

**Table MM5–6: Postures**

| Posture | Offense | Reaction Cost | Special |
|---|---|---|---|
| **Aggressive** | +1 | +1 Endurance Pool cost, first reaction of the exchange only | — |
| **Measured** | +0 | +0 | Baseline |
| **Defensive** | -1 | -1 Endurance Pool cost (min 0) | — |
| **Withdrawn** | No offense | Free (0) | Recover 2 Endurance Pool points end of exchange, up to the maximum |

PC Posture is declared blind. Enemy stances are **stated, not concealed** — announce them as the exchange opens, driven by the stat block's `triggers:`. Insight reads past a stated stance (a feint, a shift about to happen).

---

## Offensive Actions

**Table MM5–7: Offensive Actions**

| Action | Roll | Effect |
|---|---|---|
| **Strike** | 2d6 + weapon attribute + Combat or Finesse (default melee/ranged; the fiction may say otherwise) | Deplete enemy Resolve (10+: −2, 7–9: −1); 10+ also chooses one rider — Open or Position |
| **Maneuver** | 2d6 + relevant skill | 10+: rolls against the target are Easy until the situation changes. 7–9: rolls against the target stay Standard. 6-: backfire |
| **Support** | 2d6 + relevant skill | Grant ally +1d6 drop lowest OR difficulty one step easier on next roll |
| **Magic** | 2d6 + Spirit + Attune, or Knowledge + Lore (by tradition) | Domain + Intent + Scope; Significant/Major spends a readied intent. **A magical Strike is always a full form** — Significant or Major, never free, and not available at all before the Technique. Free Minor magic fights as a Maneuver or Support |

**Press:** Spend 1 Endurance Pool point before a Strike to add 1d6 drop lowest (stacks with Sparks).

---

## Strike Outcomes

**Against an enemy (usual case) — deplete Resolve:**

**Table MM5–8: Strike Outcomes**

| Roll | Resolve | Rider (10+ only) |
|---|---|---|
| **10+** | **−2** | **choose one** — **Open** (Easy to Strike for everyone, until the end of this exchange; the player narrates what it looks like) or **Position** (the next roll against it is Easy, this exchange or next) |
| **7–9** | **−1** | — |
| **6-** | 0 | consequence for the **attacker** |

Enemy at **0 Resolve = defeated**. A rider never defeats — Resolve does. Open and Position are both Easy and do not stack. Open clears at the end of the exchange, and an Open enemy still acts. Mook: removed on any success (7+); armored Mook needs 10+, and a removed Mook takes no rider.

**Against another character (duel/PvP):** 10+ = Tier 2 Condition, 7–9 = Tier 1 Condition, 6- = consequence for attacker.

Default Strike difficulty: **Standard**. Adjust for posture and situation; an Open enemy is Easy for everyone, until the end of the exchange.

---

## Reactions (1 per incoming action)

**Table MM5–9: Reactions**

| Reaction | Cost (Endurance Pool points) | Roll | 10+ | 7–9 | 6- |
|---|---|---|---|---|---|
| **Dodge** | 1 | Dexterity | Avoid entirely | Downgrade 1 tier | Full hit |
| **Parry** | 1 | Weapon attribute + Combat | Avoid entirely | Downgrade 1 tier | Full hit |
| **Absorb** | 0 | No roll | — | — | Take hit at full tier |
| **Intercept** | 2 | — | Protect ally, then Dodge/Parry — once per exchange; if two would step in, the protected ally decides who | — | — |

At **0 Endurance Pool**: Absorb only.

---

## Enemy Attacks

**Table MM5–10: Enemy Attacks**

| Enemy Type | Incoming Tier | Posture? |
|---|---|---|
| Mook | Tier 1 | No (MM sets difficulty) |
| Named NPC | Tier 2 | Yes |
| Boss | Tier 2 | Yes (Techniques may escalate) |

**Aggressive enemy:** PC reactions one step **harder**

- **Defensive enemy:** PC reactions one step **easier**
- Armor and reaction downgrades **do not stack** — apply the greater reduction
- The MM chooses the incoming Condition; repeating a carried type is the telegraphed finisher (a landed repeat of a Tier 2 = Broken — telegraph it an exchange ahead)

---

## Group Rolls

- Each character rolls; **majority success** = group succeeds
- Partial (7–9) counts as success for majority calculation
- Or: designate a **lead roller**, others Support

---

## Conditions

**Table MM5–11: Conditions**

| Tier | Conditions | Effect | Duration |
|---|---|---|---|
| **1** | Winded | -1 to next roll | Clears end of exchange |
| **1** | Off-Balance | +1 Endurance Pool cost on next reaction | Clears end of exchange |
| **1** | Shaken | MM directs next action | Clears end of exchange |
| **2** | Staggered | -1 to offensive rolls | Persists until treated |
| **2** | Cornered | Cannot take Aggressive posture | Persists until treated |
| **3** | Broken | Out of the fight | End of scene |

**Stacking:** 2nd Tier 2 Condition **of the same type** = **Broken**. (Staggered + Cornered coexist without escalating.)

---

## Armor (PC downgrade budget)

**Table MM5–12: Armor**

| Type | Softens incoming Conditions |
|---|---|
| None | — |
| Light | first **2** per scene, one tier each (T2→T1, T1→none) |
| Heavy | first **4** per scene, one tier each |

Resets at **end of scene**, not exchange; shared across fights in one scene. When spent, Conditions land at full tier.

A charge is consumed only when armor provides the reduction actually applied — if a partial reaction (Dodge/Parry 7-9) already delivers the downgrade, the armor charge is kept (III.3, *Armor and Reaction Downgrades*).

---

## Endurance Pool

**Pool:** 4 + Constitution modifier + Endurance skill rank bonus

**Range:** 3 (Con 1, no skill) to 8 (Con 3, Master)

**0 Endurance Pool:** Absorb only, regardless of Posture (Conditions land at their normal tier — no extra penalty)

**Recovery:** Withdrawn posture restores 2 per exchange, up to the maximum

---

## Magic: Domain + Intent + Scope

**Table MM5–13: Magic Difficulty by Scope**

| Scope | Focused | Standard | Prismatic |
|---|---|---|---|
| Minor | Easy | Standard | Hard |
| Significant | Standard | Hard | Very Hard |
| Major | Hard | Very Hard | Very Hard (ceiling) |

- **The roll:** casting with Spirit adds the Attune rank; casting with Knowledge adds the Lore rank (Novice +0 if untrained)
- **Meaningful power or finesse is a full form.** Minor magic lights, snuffs, marks, stings, trips. Real force or real precision is **Significant** — and a blow aimed at putting someone down is always meaningful power, so a magical Strike is never Minor. A Mook still falls to one Strike; the caster's Strike just costs an intent to make. Repetition does not make it free either: when a string of small workings adds up to one large result, price the result.
- **Readied intents:** Minor is free. **Significant and Major spend one readied intent of their purpose** (Harm · Ward · Mend · Shape · Reveal). A formalized caster readies **3** at the start of each session, spread as they like; domain and effect are still chosen when cast. Nothing readied for the purpose → costs **a Spark** instead. They come back after a **full rest — your call** — or at the next session. A spent intent stays spent whatever the roll.
- **Pre-technique:** Minor scope only, at the domain's normal difficulty (no extra penalty — the scope restriction *is* the limitation). No readied intents until the Technique formalizes the domain.
- **Sparks and magic** — dice-Sparks work on any roll, including every magic roll. An off-purpose Significant or Major working costs a Spark that buys the working and nothing else. A Spark buys **reach** in exactly two cases, player-declared before the roll:
  - **Pre-Technique Significant:** a pre-Technique caster may spend a Spark to attempt **one** Significant-scope effect at the domain's normal Significant difficulty. One effect per Spark — not an unlock; Major stays closed until the Tier 1 Technique.
  - **Focused eases Major:** a Focused domain may spend a Spark to shift a Major effect one step easier (Hard → Standard). Focused only.
  - **Prismatic:** reach-Sparks cannot move a Prismatic working's difficulty; dice-Sparks work normally.
- **Second domain** (Tier 3, Mind and Soul trees): a second **standard** domain only — prismatic territories require Ascendant Domain. Effects in the second domain are one difficulty step harder than normal for that domain until the character earns their next Facet level; then the penalty lifts.

### Adjudicating Magic (compressed from MM2 — see MM2 for full text)

- **Rule out loud, before the dice.** Say the scope, say the difficulty, then roll. A ruling delivered after the result sounds like an adjustment.
- **Scope = scale of change + duration + precision.** Not how impressive it looks, not how well it was described, not target count (a dozen torches lit at once is still Minor). "And it stays that way" moves the tier on duration alone — catch it before the roll. When you correct scope upward, name the new difficulty and *pause*; scaling the intent back down is the player's call.
- **Check the ceiling before you price the roll.** A pre-technique caster is capped at **Minor** — except that a Spark buys one Significant-scope attempt at normal difficulty. Beyond that it is an availability question, not a difficulty one. Tell them what their magic can do now and let them re-aim.
- **Domain boundaries — lean toward yes.** The test is substance vs. rhyme: does it run through the domain's actual material, or only share its mood? Fire burning the breathable content out of the air = yes; fire commanding the weather = no. Shadow muffling sound = yes; shadow granting invisibility = no. Don't surcharge a creative stretch — if the reach is more ambitious, that shows up as scope. A "no" is a **"No, but..."**. A "yes" is precedent — you are setting it permanently.
- **7–9: the magic worked.** Pick the cost first — **affects more than intended** / **costs something unexpected** / **creates a consequence nobody planned** — then name it while narrating the success it rides on; the complication is added to a success, never a discount on one. Mine the player's stated intent for the specifics. Rotate categories — four costs in a row and 7–9 becomes a flat fee. Test: does the table now have something to *do*?
- **Full rests are your call** (compressed from MM2, *Calling a Full Rest*). Default: a night's sleep somewhere safe; most sessions have none. Grant them freely and readied intents stop being a guess. Say the call before anyone readies.
- **Active opposition = Standard floor.** A floor, not a surcharge. It only ever moves the **Easy** cell (Focused domain, Minor scope); every other combination already meets it, so raising a Hard roll "because combat" applies it twice. Opposition = something with its own will resisting *this working, right now* — a sealed door is difficulty, the rival holding it shut is opposition. Specific circumstances (distracted, wounded, constrained) may still adjust; "it is a battle" is not a circumstance.

### Social 7–9 Costs (compressed from MM2 — see MM2 for full text)

**They know you needed it** — you get it; they learn its price to you.
**The debt** — a favour owed, unspecified, callable.
**The witness** — someone who should not have heard it did.
**The narrower yes** — you get the part that costs them least.
**The wrong believer** — it lands too well on the wrong person.
**The record** — it is written down somewhere other people read.

Pick before you narrate; name the cost as part of the success; rotate the shapes. A social **6-** is almost never a refusal — it is a worse relationship than the one you walked in with.

---

### Magic 6- Templates (compressed from II.3 — see II.3 for full text)

**Wrong target:** the effect manifests on the wrong target.

**Keeps working:** the effect works — and keeps working.

**Attracts attention:** the working attracts attention.

**Domain bleeds:** the effect lands in the right place but with the wrong character.

**Cost arrives early:** the magic succeeded — but the mage carries a consequence that should have been deferred.

**Nothing happens:** the domain reaches and finds nothing — the rarest and most useful failure.

**Player option:** a magical 6- is a Graceful Fail opportunity — the player describes the response and claims the Spark; the MM confirms.

---

## Encounter Building

### Threat Rating (TR)

```
TR = offense_value + durability_value + armor_bonus + technique_bonus
```

**Table MM5–14: Threat Rating Components**

| Attack Mod | Offense | | Component | Value |
|---|---|---|---|---|
| -2 or lower | 0 | | **Durability** | base Resolve (Mook 0; Named ~3–4; Boss ~8) |
| -1 | 1 | | **Armor** | None 0 / Light +1 / Heavy +2 |
| +0 | 2 | | **Technique** | +1 per Technique or special (count them) |
| +1 | 3 | | | |
| +2 | 4 | | | |
| +3 | 5 | | | |
| +4 | 6 | | | |

**TR Minimums:** Mook >= 1, Named >= 8, Boss >= 12

### Encounter Recipe Table (PS 3 — simulation-validated)

**Actor count drives difficulty, not total TR.** The number of Named/Boss enemies acting at once is the real dial — there is no TR budget (MM1, *Sizing an Encounter*). Party Strength = sum of `career_advances`. Adding enemies mid-fight is the sharpest dial you own: one Mook is one difficulty band (76% → 47% → 20%).

**Table MM5–15: Encounter Recipes (Party Strength 3)**

| Difficulty | Suggested Enemies | Sim Win Rate |
|---|---|---|
| **Skirmish** | 3–7 Mooks | ~100% |
| **Standard** | 3 Named (TR 8) + 1 Mook | ~75–80% |
| **Hard** | 3 Named (TR 8) + 2 Mooks | ~47–48% |
| **Deadly** | 3 Named (TR 8) + 3 Mooks, or 4 Named + 1 Mook | ~17–22% |

**Actor count is the dial:** 1–3 Named/Boss = clean win at any TR (3 Named ~96%); a fixed 3-Named core climbs Standard → Hard → Deadly by adding one Mook at a time (1/2/3); 5 Named = near-certain loss. Mook swarms alone only ever make a Skirmish. Each additional PC shifts the thresholds up ~1 Named.

---

## Skill Advancement

- **4 skill points** per session — up to 2 unspent bank into the next session; 1 per session may train an unused Primary-Facet skill
- Marks to advance one rank: **3** to Practiced, **5** to Expert, **8** to Master
- **Rank caps, per Facet:** at most **3** skills beyond Practiced, only **1** of them Master. A finished Facet is 1 Master / 2 Expert / 2 Practiced. A slot is claimed the moment a mark goes past Practiced, and is never freed
- Primary Facet skills: **1 SP per mark**
- Cross-Facet skills: **2 SP per mark**
- Every **3** skill rank advances in a Facet = +1 Facet Level (that Facet); the Background's starting rank counts as one
- Facet Level = unlock 1 Technique from any tree whose prerequisites you meet
- A finished Facet = **9** advances = Facet level 3; level 4+ is cross-training
- Every **3** total Facet levels (any Facet) = Major Advancement

---

## MM Trouble Table (compressed from MM2 — see MM2 for full text)

Roll or pick a d6 for a generic 6- consequence when nothing specific comes to mind. Any roll, magical or not.

**Table MM5–16: Generic 6− Consequences**

| d6 | Category | The 6- consequence |
|---|---|---|
| 1 | **Cost** | Something spent, broken, or used up that can't be easily replaced — a resource, a favor, an opportunity. |
| 2 | **Position** | Somewhere worse — cornered, separated from the group, or committed to a course they can't undo. |
| 3 | **Attention** | Something notices that wasn't paying attention before — guard, rival, nearby threat. Better if it only starts looking. |
| 4 | **Equipment** | Gear fails, jams, or is lost — not gone forever, just unavailable right now. Keep it recoverable. |
| 5 | **Condition** | Worse for wear — winded, shaken, off-balance. Narrated flavor, **not** a mechanical Condition unless already in combat (III.3). |
| 6 | **Revelation** | New information that complicates things. Decide whether it helps or hurts first; make it cost something. |

- **Pick over roll** unless you want to be surprised too. The category is a prompt, not the line you say out loud.
- **Size the trouble to the risk**; never pick the row that halts the story.
- **Magic:** pair a category with the Magic 6- Templates above — template = how the domain misbehaved, category = what it cost.

**Graceful Fail:** hand the player the category, let them narrate the specifics, confirm the Spark.

---

## Common Rulings

**Unnarrated details:** Players cannot act on details the MM has not described. A player may always ask — and the default answer leans yes — but cannot declare an action that assumes the answer (III.1, *Acting on Unnarrated Details*).

**Contested roll (PvP):** Both sides roll; higher total wins. On a tie, both achieve partial success.

**Contested roll (vs NPC):** Only the player rolls. NPC capability sets difficulty.

**"Can I try again?":** Only if the fiction changed — new approach, new information, or time passing that cost something. Otherwise the first result stands. A new approach gets a freshly declared difficulty (III.1, *Trying Again*).

**When not to roll:** Only roll when outcome is uncertain, stakes matter, and both success and failure move the story.

**Specialty:** A Background Specialty that *directly* applies turns a Standard roll Easy — its step shares the single character-side step with Techniques (III.1, *Difficulty*). When it is only tangential, hand over the information free — no roll (II.6, *Specialty*).

**Saving throws:** 2d6 + Major Attribute modifier (Body / Mind / Soul). Same three-tier outcomes. Use when something happens *to* the character, not something they choose.

**Mooks:** No Resolve, no Condition track. Any successful Strike (7+) removes one; an armored Mook needs a full success (10+).

