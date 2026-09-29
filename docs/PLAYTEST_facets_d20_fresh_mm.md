# Playtest: Facets d20 through a fresh MM's eyes

**Date:** 2026-09-28 · **Branch:** `feat/facets-d20` · **Reader:** an experienced 5e DM who had never seen this game.
**Rule:** read only `facets_d20/*.md`. No `docs/`, no `software/`, no yaml. Nothing in this file is canon; the NPC and encounter framing is placeholder test content.

SRD stat lines I quote are my own reading of SRD 5.2.1 blocks. Where I priced a monster the appendix already lists, my figure matched the appendix. That's the check that I read the blocks the same way the tool does.

---

## 0. Verdict up front

**Running it is clearly easier than 5e. Prepping it is about the same, and the boss rules are the weak joint.**

- Side initiative, fixed damage, 1-HP minions and the morale save are all good, easy to learn, and save real time at the table. I would steal all four for a normal 5e game tomorrow.
- The encounter method uses about the same arithmetic as the 2024 XP budget (one row lookup, one multiply, one sum). It carries more modifiers: role choice, lone boss ×1.2, the hard-hitter tier bump, the tired-party tier drop, and the one-tier-up rule for published adventures. It is **better calibrated** than CR/XP, because the numbers come from each block's HP × damage. Its edge cases are **worse specified**.
- The boss is the only new procedure a 5e DM hasn't met before. Its rules are split across 08, 09 and the appendix. Table 8–1 leaves it out, and so does the Quick Reference's HP line. The turn structure also produces an unannounced side effect: from round 2 on, **the boss always takes its two turns back to back.** That is the biggest thing I'd fix.

---

## 1. Lookup log

Times are honest estimates for an experienced DM reading these books for the first time, with an SRD open in another tab.

| # | Task | Where I looked | Time | Friction |
|---|---|---|---|---|
| 1 | Party HP at 4th (needed to sanity-check "% of party HP") | 02 presets → 02 *Hit points* + Table 2–6 | 4 min | Presets print only "At 1st"; 4th-level numbers have to be worked out by hand |
| 2 | Budget per character | 09 Table 9–1 | 20 s | None |
| 3 | Goblin Warrior, Goblin Boss, Wolf threat | Appendix Table 9–2 | 1 min | Alphabetical by CR, not by name. Fine once you know. |
| 4 | Who a minion's "leader" is | 09 *Morale*, 09 *Minions*, 08 *Bloodied and Morale* | 2 min | Three places; none covers minions with no leader, or a boss as leader |
| 5 | Boss rules (double HP, top of round, resolve, Bloodied change) | 08 *Kinds of Foe*, 09 *Bosses*, Appendix footnote | 4 min | Scattered. Table 8–1 has no boss step. The Quick Reference omits double HP and the Bloodied change. |
| 6 | Lone boss rule | 09 *Adjusting the budget*, Appendix footnote | 1 min | Undefined when the boss has one or two minions |
| 7 | Hard-hitter rule for a mixed group | 09 *Adjusting the budget*, 09 knight example, Appendix footnote | 5 min, unresolved | "A group of hard-hitting monsters" is never defined for a mixed fight |
| 8 | Party-size adjustment | 09 *Adjusting the budget* | 30 s | Clear. But the "Boss at levels" column silently assumes four PCs. |
| 9 | Conversion steps | 09 *Pricing Any SRD Monster* | 3 min per monster | Nothing on multiple attack options, area damage, save-for-half, spellcasting, resistance, regeneration or flight |
| 10 | "Mindless or bound" (does a ghoul ever break?) | 08, 09 | 1 min, unresolved | Only examples are zombies, constructs and a guardian |
| 11 | Boss's reaction count | 08 *Reactions*, 09 *Fixed Damage* | 2 min, unresolved | The two chapters give different rules for a creature with two turns |
| 12 | Short-rest recovery | 06 *Rest*, 02 *Hit points*, 03–05 per feature | 5 min | Clear per feature. Nothing in 09 gathers it, and "you never roll" (01) makes you wonder whether Hit Dice roll |
| 13 | NPC starting attitude | 06 *Attitude*, 09 *Social Scenes* | 2 min, unresolved | No default and no guidance |
| 14 | Influence action mid-fight: what a Neutral enemy does | 08 *Actions*, 06 | 2 min, unresolved | Not covered |

Prep time, all three encounters: **~25 minutes including one 4-PC HP calculation.** A comparable 5e prep with the 2024 XP table takes me about 15. Most of the difference is items 4–7 above, and it would shrink on the second session.

---

## 2. Task 1: three encounters for four 4th-level PCs

### The party (presets from 02, worked to 4th)

HP = die max + 8 + Con at 1st, then half die + 1 + Con per level (02, Table 2–6).

| PC | Die | Con | HP at 4th | AC | Main attack |
|---|---|---|---|---|---|
| Fighter | d10 | +2 | 18 + 3×6 + 4×2 = **44** | 19 (chain 16, shield 2, *Weapon Expert* 1) | longsword +7, 1d8+4 |
| Rogue | d10 | +2 | **44** | 15 | rapier +6, 1d8+4 (+1d6 *Precision*) |
| Wizard | d6 | +2 | 14 + 3×4 + 8 = **34** | 12 | *Fire Bolt* +6, 1d10+4 (*Evoker*); Full table: 4×1st, 3×2nd |
| Priest | d8 | +2 | 16 + 3×5 + 8 = **39** | 16 | mace +3; *Channel*; Full table |

**Party HP: 161.** A Clash should cost 32–56 HP, a Battle 56–89, a Skirmish 8–24 (09 *The Four Tiers*).

Budgets (09 Table 9–1, level 4): Skirmish 19, Clash 30, Battle 34 per PC.

### Skirmish: goblin ambush (budget 19 × 4 = **76**)

| Foe | Role | Threat | × | Total |
|---|---|---|---|---|
| Goblin Boss | standard (the leader) | 14 | 1 | 14 |
| Goblin Warrior | minion | 7 | 8 | 56 |
| Wolf | standard | 7 | 1 | 7 |
| | | | | **77** (101%) |

Morale: the goblin boss checks at Bloodied, and when it falls, the eight minions check. Lookups: 3. Time: ~3 min.

- **3 players (57):** Goblin Boss 14 + 6 minions 42 = **56**.
- **5 players (95):** Goblin Boss 14 + 10 minions 70 + 1 wolf 7 = **91**, or add a Worg (13) instead of the wolf for **97**.

### Clash: ogre and its goblin handlers (budget 30 × 4 = **120**)

| Foe | Role | Threat | × | Total |
|---|---|---|---|---|
| Ogre | boss (appendix: boss at levels 3–5 ✓) | 99 | 1 | 99 |
| Goblin Warrior | minion | 7 | 3 | 21 |
| | | | | **120** (100%) |

The ogre boss has 68 × 2 = **136 HP** and is Bloodied at 68. It uses its greatclub (+6, fixed 13) or a javelin (fixed 11). Its Bloodied change: *it gets desperate*. Lookups: 5. Time: ~6 min, most of it gathering the boss rules.

- **3 players (90):** **the ogre can't be the boss.** At 99 it is 110% of the whole budget before the ×1.2 lone-boss factor. Rebuilt: Ogre standard 30 + Goblin Boss 14 + 6 minions 42 = **86**. The appendix's "Boss at levels 3–5" column told me the ogre fit, but that column assumes four PCs, and nothing says so.
- **5 players (150):** Ogre boss 99 + 7 minions 49 = **148**.

### Battle: bandit captain, worgs, bandits (budget 34 × 4 = **136**)

| Foe | Role | Threat | × | Total |
|---|---|---|---|---|
| Bandit Captain | boss | 83 | 1 | 83 |
| Worg | standard | 13 | 2 | 26 |
| Bandit | minion | 6 | 4 | 24 |
| | | | | **133** (98%) |

- **3 players (102):** Captain boss 83 + 3 minions 18 = **101**.
- **5 players (170):** Captain boss 83 + 3 Worgs 39 + 8 minions 48 = **170**.

**Where it stalled:** my first draft used two Scouts (standard 14, marked *hits hard*) in place of the worgs. Does that make the fight "a group of hard-hitting monsters", bumping a Battle to Desperate? Or does the rule only mean a fight made mostly of them? The knight example is a pure group, and a mixed fight isn't covered. I dropped the scouts rather than guess. **Ten minutes on one line.**

**Side check, the lone owlbear:** as a boss it is 136, exactly the Battle budget. Lone, it is ×1.2 = **163**, which is Desperate (164). It is also marked *hits hard*. Does one monster count as "a group"? If so, it becomes a tier above Desperate, and no such tier exists.

---

## 3. Task 2: converting two monsters not in the appendix

I used 09 *Pricing Any SRD Monster* and checked the results against Table 9–3 by CR.

### Ghoul (CR 1)

SRD 5.2.1 as I read it: AC 12, HP 22. Multiattack: Bite (5 piercing + 3 necrotic) and Claw (4 slashing; a non-elf target makes a DC 10 Con save or is paralyzed until the end of the ghoul's next turn).

1. Damage per turn: 5 + 3 + 4 = **12**.
2. Standard: √(22 × 12) = √264 = **16.2 → 16**. Minion: √(10.5 × 12) = √126 = **11.2 → 11**. Boss: 16.25 × 3.34 = **54**.
   - **Guess:** is a ghoul "mindless or bound"? Int 7, ravenous, not controlled. I said no, so it can break. If it never breaks: standard 16.25 × 1.16 = **19**, minion 13.
3. Morale: flees toward the dark to feed later.
4. Boss Bloodied change: calls for help, and two ghoul minions climb out of the crypt.

Table 9–3 at CR 1 gives 18 / 11 / 60. That's close.

**Unpriced:** the paralysis is the whole point of a ghoul, and the formula ignores it. "Paralyzed until the end of the ghoul's next turn" is also shorter than it looks on a boss ghoul, which has two turns a round.

### Manticore (CR 3)

SRD 5.2.1 as I read it: AC 14, HP 68, flies. Multiattack: three melee attacks (about 7 + 6 + 6 = 19) *or* three Tail Spikes at range (7 each = **21**).

1. Damage per turn: **guess.** The book says "everything it does on an ordinary turn", but the ordinary turn has two options. I took the higher, 21.
2. Standard: √(68 × 21) = √1428 = **37.8 → 38**. Minion: √220.5 = **14.8 → 15**. Boss: 37.79 × 3.34 = **126**.
3. Morale: bargains. It will sell out whoever set it on the road for its life.
4. Boss Bloodied change: *it gets worse*, with a second volley of spikes.

Table 9–3 at CR 3 gives 37 / 15 / 124. That's close.

**Unpriced:** flight plus 100-foot spikes means a party without ranged damage can't reach it. That can double the fight's length, and nothing in the Threat number knows.

### What the conversion steps don't cover

| Case | What the book says | What I had to guess |
|---|---|---|
| Two alternative attack routines | "everything it does on an ordinary turn" | take the higher? the one it'll use? |
| Area or multi-target damage (breath, *Fireball* from a Mage) | "if it all hits", which assumes one target | count one target? two? |
| Save-for-half damage | nothing | full average? |
| Spellcasting monsters | nothing, though Mage and Priest are priced in 9–2 | which spell is "an ordinary turn"? do slots run out? |
| Resistance, immunity, regeneration | nothing | a gargoyle or wight with B/P/S resistance against a 4th-level party without magic weapons plays well above its number |
| Recharge on a boss | left out as "a spike", yet a boss rolls Recharge **twice a round** (09 *Bosses* rule 2) | a boss breath weapon comes back about twice as often as the spike assumption expects |
| "Never breaks" | mindless or bound | whether intelligent undead, fiends and fanatics count |

---

## 4. Task 3: the Clash, three rounds from behind the screen

**Setup:** ogre boss (136 HP, AC 11, fixed 13) and three goblin minions (AC 15, +4, fixed 5). Party as above. No one is surprised.

**Initiative:** party d20 + 4 (the rogue's Dex) = 7 + 4 = **11**. Foes use the best among them, a goblin's +2: 12 + 2 = **14**. **Foes first.**

**Round 1**
- *Top of round, ogre:* moves 40 ft to the fighter and clubs him (21 vs AC 19, hit): **13**. Fighter 31/44.
- *Foe half:* per 09's "spread the attacks", the ogre swings at the priest (15 vs 16, miss). Two goblins shoot the wizard: one hits (**5**, wizard 29/34), one misses. The third stabs the rogue (20 vs 15, hit): **5**, rogue 39/44.
  - This was the ogre's **second consecutive turn**. See G1.
- *Party half:* the wizard casts *Shatter* on two goblins; both fail their Con saves and die. The rogue kills the third. The fighter hits the ogre for 9 (127). The priest's mace misses.
  - **All minions are gone in round 1.** The "crowd" that was 18% of the budget did 10 damage, and from here the fight is a lone boss that was priced *without* the ×1.2 lone-boss factor (G9).

**Round 2**
- *Top, ogre:* walks from the fighter to the wizard. That provokes the fighter's opportunity attack, which hits for 8 (119). Club on the wizard (20 vs 12): **13**, wizard 16/34.
- *Foe half, ogre again:* clubs the wizard again: **13**, wizard **3**/34. The wizard took 26 in two enemy turns with no party turn in between.
- *Party half:* the priest casts *Healing Word* (bonus action) plus *Channel*'s rider (2 + slot level): 11, wizard 14. The wizard backs off. Fighter 10, rogue 12 with *Precision* (ally adjacent). Ogre 97.

**Round 3**
- *Top, ogre:* clubs the fighter: 13, fighter 18/44.
- *Foe half:* clubs the rogue: 13, rogue 26/44.
- *Party half:* fighter 10, rogue 12, wizard *Scorching Ray* 18, priest 5. The ogre drops to 52 and is **Bloodied** partway through the wizard's rays. It *gets desperate*: advantage on its attacks, and attacks against it have advantage.

**After three rounds:** the party has taken 75 of 161 (47%) before healing, and the ogre still has 52. With advantage it lands about 75% of 26 a round, so two more rounds is roughly another 40, for **~70% of party HP over five rounds.** That's Desperate numbers, not a Clash. My dice favored the ogre (5 hits in 6 swings). Expected values: the ogre hits a mean AC of 15.5 about 55% of the time, so ~14 a round; the party does ~31 a round against AC 11. That gives ~5 rounds and **~50% of party HP**, still the Battle band, not the Clash band. Tighter play (fighter's *Action Surge*, the wizard's 2nd-level slots on the ogre) probably gets it to 4 rounds and 35%. A **boss-heavy** Clash is much swingier than a Clash of standards, and the book doesn't warn about it.

### Every rule I had to guess (G = guess)

| # | Guess | Source of the gap |
|---|---|---|
| G1 | **Boss turns are consecutive.** With foes first, the order is top (boss), foe half (boss), party. With the party first, the boss's foe-half turn is followed at once by next round's top turn. Either way, once its allies are dead the boss acts twice in a row every cycle. I allowed it; it nearly dropped the wizard. | 08 *Kinds of Foe*, 09 *Bosses* rule 2; Table 8–1 doesn't show the boss at all |
| G2 | Boss reaction: **one per round** (09 *Fixed Damage*) or refreshed **at the start of each of its turns** (08 *Reactions*)? I used one per round. | 08 vs 09 |
| G3 | Boss Bloodied threshold is half the **doubled** HP (68, not 34). | Implied, never stated |
| G4 | The Bloodied change takes effect immediately, mid-party-turn. | Not stated |
| G5 | The ogre boss is the goblins' "leader" for minion morale. A boss leader never breaks, so its minions only check once it's dead. | 09 *Morale*, *Minions* |
| G6 | Surprise vs a boss: a surprised side "goes second", but the boss's top-of-round turn happens "before either side". I'd let a surprised boss keep its top turn, which makes ambushing a boss nearly worthless. | 08 *Who Goes First* vs *Kinds of Foe* |
| G7 | Durations on a boss: "until the end of its next turn" effects (the ghoul's paralysis, a boss's own buffs) end twice as fast. I left it. | Not addressed |
| G8 | Minions in the area of a spell that isn't a save (e.g., *Magic Missile* on three): each dart kills one. Fine, clear. | 08 *Minions* ✓ |
| G9 | Once the minions die, a boss fight priced at 99 + 21 plays as a lone boss at 99 with no ×1.2. I didn't adjust mid-fight. | 09 *Adjusting the budget* |
| G10 | Boss resolve: 09 says it triggers when the boss "fails a save"; 08 says when an effect "would" stun etc. They differ for no-save effects. Didn't come up. | 08 vs 09 |
| G11 | "Calls for help" Bloodied change: do those minions come out of the budget? Which half do they act in? | 09 *Bosses* rule 4 |

Fixed damage, side initiative, minions and the morale DC worked with no lookup after the first read, which is exactly as advertised.

---

## 5. Task 4: the day (three Clashes and rests)

**Plan** (09 *The Day*):

1. Clash A: Ogre boss + 3 goblin minions (120).
2. **Short rest** (1 hour, 06 *Exploration, Travel and Rest*).
3. Clash B: 3 Bugbear Warriors (17 × 3 = 51) + 2 Worgs (26) + Goblin Boss (14) + 4 goblin minions (28) = **119**.
4. **Short rest.**
5. Clash C: Bandit Captain boss (83) + 6 bandit minions (36) = **119**. This is the book's own example.

**What the party gets back on a short rest.** I had to assemble this from four chapters:

| PC | Short rest | Long rest only |
|---|---|---|
| Fighter | Hit Dice (4 × d10+2), one *Second Wind* use, *Action Surge* | — |
| Rogue | Hit Dice (4 × d10+2) | — |
| Wizard | Hit Dice (4 × d6+2); *Study* uses; *Studied Recovery* once per long rest (2 slot levels) | spell slots |
| Priest | Hit Dice (4 × d8+2); *Channel* (1 use) | spell slots, *Kindle* |

**Is it clear?** Per feature, yes: every feature says which rest returns it. For the MM, **no**:

- 09 *The Day* never says what a short rest restores, so the MM can't judge "a tired party (about half its hit points and half its daily resources)" without polling the table.
- 01 #6 says "You never roll" for hit points; 02 says Hit Dice "are still spent on short rests as the SRD says". A 5e DM will work out that Hit Dice still roll, but the sentence in 01 makes them stop and check.
- "Parties survive that nine or ten times in ten" doesn't define survive. No deaths? No TPK? If it means one in ten standard days kills a PC, that doesn't fit a game that is "heroic by default".
- The sums work: 4 Hit Dice each of about 7–8 HP covers a 20–35% Clash easily, so the short rests really do reset HP. The squeeze is caster slots, which is the 5e norm.

---

## 6. Task 5: a social scene

**Setup** (placeholder): a harbor clerk holds a cargo manifest the party wants to see. Showing it puts the clerk at some risk, so the party needs **Friendly** (Table 6–2).

- **Starting attitude:** I chose Wary. **The book gives no default and no guidance** (06 *Attitude*, 09 *Social Scenes*). Wary vs Neutral is the biggest single dial in the scene, and it's a coin flip for the MM.
- **DC:** the clerk has reasons to refuse, so **15** (06 *Making Your Case*). Clear.
- The priest argues duty to the harbor (Persuasion +3, with advantage from leverage: the party saw the clerk take a bribe). Roll 17: meets the DC. **Wary → Neutral.**
- The rogue offers coin (a different argument, Persuasion +2). Roll 16, then a Spark: 16 + 4 = 20, beating the DC by 5. One step: **Neutral → Friendly.** The manifest is shown. Two rolls, about three minutes.
- **Drives and Sparks:** the priest's line (placeholder: *won't lie to the faithful*) is a compel when the rogue's pitch needs the priest to vouch for something false. The priest declines to vouch, the clerk hesitates, and the priest takes a Spark. The MM "pays" attitude steps, Sparks for honest compels (once a scene per player), and an MM's-call Spark for a great moment.

**What was clear:** the DC ladder, the results table, advantage from leverage or Specialty, the "no social HP" limit, compels, and the Spark economy.

**What wasn't clear:**

1. No starting-attitude guidance (above).
2. **How many tries?** On a success, can another PC roll right away? The only brake is "that argument won't work again" on a miss by 1–4. Four PCs rotating arguments can walk anyone from Wary to Ally in one scene.
3. **Intimidation moves someone toward Ally.** A clerk who has been threatened is now "Friendly" and "helps at some cost to themselves"? That reads wrong.
4. **Influence in a fight** (08 *Actions*): what does a Neutral or Friendly *enemy* do mid-fight? Stop attacking? Break? It needs a line tying it to morale, e.g. "a foe moved to Neutral breaks as if it failed morale".

---

## 7. Confusions ranked by how badly they'd stall a session

| Rank | Stall | Where | Problem | Suggested fix |
|---|---|---|---|---|
| 1 | **High**, every boss fight | 08 *The Round* Table 8–1 and *Kinds of Foe*; 09 *Bosses* | Boss procedure is split across three places. Table 8–1 has no boss step, and its step 4 literally skips one. The boss always gets back-to-back turns (G1). Reaction count (G2), surprise (G6) and Bloodied threshold (G3) are undefined. | Add "0. Boss turn" to Table 8–1. State: the boss's Bloodied is half its doubled HP; one reaction per round; a surprised boss loses its top-of-round turn in round 1. Consider moving the boss's second turn to **after any one PC's turn in the party half** (MM's pick) so its turns never land back to back. |
| 2 | **High**, prep | 09 *Adjusting the budget* ("Hard hitters"); Appendix footnote | "A group of hard-hitting monsters" is undefined for mixed fights or a single hard hitter. "Next tier up" is a cliff: at level 4, Clash to Battle is +13%, but the fix drops two budgets (to Skirmish, −37%). | Bake it into the number, like never-breaks already is: price hard hitters ×1.2 in Table 9–2 and delete the tier rule. |
| 3 | **High**, conversion | 09 *Pricing Any SRD Monster* step 1 | No rule for alternative attack routines, area or multi-target damage, save-for-half, spellcasters, resistances or regeneration. Recharge is excluded yet fires twice a round on a boss. | Add five one-line rules: take the higher routine; area counts two targets; save-for-half counts ¾; a spellcaster's ordinary turn is its best at-will plus one slot spell; resistance to common damage ×1.25 on HP. For bosses, count Recharge as ½ its damage. |
| 4 | **Medium** | Appendix "Boss at levels" column; 09 party size | The column assumes four PCs and doesn't say so. At three PCs a "fits" boss can overshoot the whole budget (ogre: 110% of a 3-PC Clash). | Say "for four characters" in the column header. Add: "with three players, a boss that fits is one row higher in level". |
| 5 | **Medium** | 09 *Morale* / *Minions*; 08 *Bloodied and Morale* | Minions with no leader never check. A boss leader never breaks, so its minions only check after it's dead. "Mindless or bound" gives no guidance for ghouls, fiends or fanatics. | "If a group has no leader, its minions check when half of them are down." List three or four example "never breaks" types. |
| 6 | **Medium** | 06 *Attitude*, *Making Your Case*; 09 *Social Scenes* | No starting attitude, no limit on attempts, Intimidation sits oddly on the track, and Influence mid-fight has no effect in combat terms. | Default a stranger to Neutral and anyone the party has crossed to Wary. "One roll per PC per scene per person." Intimidation moves toward Ally now but one step toward Hostile once the threat is gone. "A foe moved to Neutral in a fight breaks." |
| 7 | **Medium** | 09 *Bosses* rule 4 ("It calls for help") | Unclear whether reinforcements are budgeted, and when they act. | "Reinforcements cost up to 20% of the budget and act in the foes' next half." |
| 8 | **Medium** | 10 *Quick Reference* | No MM side. The boss line omits double HP and the Bloodied change; no budget table, tiers or morale results. An MM at the table flips to 09 every fight. | Add a half-page MM box: Table 9–1, the tier descriptions, the boss's four rules, morale outcomes, and the day. |
| 9 | **Medium** | 09 *The Baseline Fight* / *The Four Tiers* | A boss-heavy Clash plays much hotter than a Clash of standards (my run: 50–70% of party HP). Not flagged. | Add one line: "A boss that is more than ¾ of the budget is swingy; give it more minions, or build one tier down." |
| 10 | Low | 09 *The Day* | "Survive" undefined; nowhere lists what a short rest restores; "tired party" can't be judged without asking the table. | Define survive. Add a two-line "what a short rest gives back" list. |
| 11 | Low | 09 *Adjusting the budget* ("lone boss") | ×1.2 applies only with "nobody else". A boss with one minion is a cliff, and it becomes a lone boss mid-fight once its minions die. | "Counts as lone if its allies are under 20% of the budget." |
| 12 | Low | 02 *Presets* | Cards print only "At 1st". An MM checking party HP at level N does the arithmetic. | Add an HP-and-AC line at 5th and 10th to each card. |
| 13 | Low | 08 *Attacks and Damage* | A rolled monster crit can come in under the fixed average (ogre crit 4d8+4 minimum 8, against a fixed 13). | "A crit deals the fixed damage plus the rolled dice once." |

---

## 8. Contradictions and inconsistencies

1. **Reactions:** 08 *Reactions* says "one reaction per round, and it comes back at the start of your turn"; 09 *Fixed Damage* says "one reaction a round". These differ for a boss with two turns.
2. **Boss resolve trigger:** 08 *Kinds of Foe* says "when an effect would stun…"; 09 *Bosses* rule 3 says "when a boss fails a save against something that would…". They differ for no-save effects.
3. **Table 8–1 vs the boss rule:** step 4 says "Back to step 2", which skips a top-of-round turn the table never lists.
4. **01 #6 "You never roll"** vs 02 and 06, where Hit Dice are still spent on short rests "as the SRD says" (i.e. rolled). Not a real contradiction, but it reads like one.
5. **Hard-hitter compensation is asymmetric:** 09's knight example builds a "Clash" of hard hitters at the Skirmish budget (76), yet the next-tier-up rule implies only ~13% extra at level 4 (Clash 120 to Battle 136).
6. **10 Quick Reference, Bosses line:** omits double HP and the Bloodied change. The page says "chapters win", but at the table the page is what gets read.
7. Spelling: 08 uses "paralyze", 09 uses "paralyse".
8. Aside (player side): 05 *Sworn Strike* grants uses "equal to your Soul modifier". No ability or modifier by that name exists anywhere I read. The Oathsworn preset takes this talent.

---

## 9. Task 6: judgment against 5e

**Easier to run?** Yes, clearly. Fixed damage and side initiative cut my enemy-side time per round roughly in half. Minions and morale end fights early and hand you prisoners, which is good for play. The alley example in 08 is a fair picture of how it feels.

**Easier to prep?** About equal. For monsters in Table 9–2 it's one lookup per monster plus a role choice, which is no heavier than the 2024 XP method. For monsters not in the table it's heavier: a square root per monster, or the rougher CR table. The boss rules and the budget modifiers add a first-time cost of about 10 minutes.

**Encounter math, simpler or heavier than XP?** Same shape (a per-PC budget times party size, then add up the monster numbers), with **more modifiers** (four vs zero in the 2024 DMG) and **better numbers**, since they come from HP × damage rather than CR. Make the modifiers disappear into the table values and it would be strictly better than XP.

**What I'd cut:**

- The *hard hitters → next tier* rule. Bake it into the numbers.
- The "Standard at levels / Boss at levels" columns, or relabel them. They confused me more than they helped, and they are wrong for 3 or 5 players.
- "Heroic by Default: make each published fight one tier tougher". A per-fight tier conversion on top of everything else. Move it to a sidebar.

**What's missing:**

- An MM half of the quick reference.
- A worked **boss** fight. The only worked fight (the alley) has no boss, and the boss is the one new procedure.
- Conversion rules for spellcasters and area damage.
- Starting attitude and a cap on attempts in social scenes.
- One line making the boss's back-to-back turns deliberate or removing them.
