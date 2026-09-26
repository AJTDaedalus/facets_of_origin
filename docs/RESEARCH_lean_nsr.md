# RESEARCH: Lean NSR. How D&D-Shaped Games Stay Light

*Research agent, 2026-09-25. Companion to `docs/RESEARCH_complexity_audit.md` §5 and §7 (the clean-sheet "Lean Facets" question). Includes two owner constraints that arrived mid-research: (1) keep **Body / Mind / Soul** as broad parents of classes; (2) think of it like **Morrowind**, where the Facet is a *specialization*, a player can define their own class inside it, and preset classes are only suggested builds. Those are answered in §5.*

*Copyright: every mechanic below is described in my own words. No rules text or tables are reproduced. Where a source is openly licensed, the licence table (§4) says what reusing its actual wording would require.*

---

## Summary

- **The NSR's core discovery is that D&D gets light by removing rolls, not by removing numbers.** Into the Odd, Cairn and Mausritter delete the attack roll (attacks always hit), keep HP and damage dice, and put the drama in *what happens after HP is gone*. Two mechanics, save and damage, carry the whole game ([Bastionland: Oddular Mechanics](https://www.bastionland.com/2016/04/oddular-mechanics.html)).
- **HP as grit, wounds after.** HP is described as near-misses and fatigue. The first "real" hit is whatever overflows it, and that's where scars, wounds, stat loss and death live. This is the §5-B "grit" model, and it has a decade of play behind it.
- **The inventory is the character sheet.** Slots (Knave, Cairn, Mausritter, Shadowdark) do the job of encumbrance, class, spell slots and the condition track at once: wounds, fatigue and hunger take slots too. Most of the "build" happens here.
- **Usage dice kill ammo and torch bookkeeping** (The Black Hack): one die that shrinks when it rolls low. It's ideal for an app.
- **Competence without skills comes from words plus items.** Knave careers, Troika backgrounds, Whitehack groups and Tiny Dungeon traits all give a *named area* a small, fixed edge. The words are freeform. The edge is always the same size, which is why they're hard to break.
- **Advancement that feels good is plain numbers plus a pick**: more HP, +1 to a stat, a talent at some levels. Shadowdark's *rolled* talents are the commonly criticized part. Cairn's no-levels growth (Scars, training with masters) is the most flavourful and the hardest to feel.
- **Freeform magic stays in bounds when every cast has a cost paid from a shared pool**: HP in Whitehack and Macchiato Monsters, Fatigue in a slot in Cairn, spell lockout plus mishap in Shadowdark, corruption in DCC. Whitehack's playtesters found negotiated HP-cost miracles did *not* make casters stronger than other classes ([dieheart](https://www.dieheart.net/whitehack-2e-combat/)).
- **Fights are fast because of side initiative ("players go first"), no to-hit roll, and morale.** Morale is the most underrated one: enemies that flee end fights at about half the HP-grind and turn combat into a problem to solve ([Deathtrap: Lost Mechanics: Morale](https://deathtrap-games.blogspot.com/2020/11/lost-mechanics-morale.html)).
- **Recommendation:** adopt about 11 of these (§6.1). The key combination is **grit HP + weapon damage dice + a player-only 2d6 roll whose 7–9 means "you both land"**, with overflow becoming Wounds that take inventory slots, and morale rolled by the app. Under the Morrowind constraint, the **Facet owns the numbers** (HP die, stat lean, talent list, magic tradition, slot bonus), and the **class owns only words and items** (name, two knacks, a kit, a first talent pick). That makes custom classes a two-minute job and very hard to break.
- **Licence:** CC BY (Knave 1e, Maze Rats, Mausritter SRD, Dungeon World 3.0) and CC BY-SA 4.0 (Cairn, Errant) are safe even for *text*: BY-SA 4.0 is one-way compatible with GPLv3. OGL (Black Hack, Whitehack, DCC, OSE) and bespoke licences (Shadowdark, Troika, Mark of the Odd, Knave 2e) are **concept-only** for us. Shadowdark's licence explicitly excludes standalone games that reword its core rules.

---

## 1. Games surveyed (one line each)

| Game | Chassis in one line |
|---|---|
| **Into the Odd** (McDowall, 2014; Remastered 2022) | STR/DEX/WIL (d20 roll-under saves); attacks auto-hit; damage to HP, then STR plus a save or critical damage. PCs normally act first. |
| **Electric Bastionland** (McDowall) | ItO chassis; 100 "failed careers" keyed to your highest and lowest stat; the party starts with a shared debt ([Grognardia](http://grognardia.blogspot.com/2020/09/review-electric-bastionland.html)). |
| **Cairn** 1e/2e (Yochai Gal) | ItO + Knave. Classless, 10 slots, spellbooks cost Fatigue, Scars at exactly 0 HP, no XP; growth comes from the fiction ([Cairn 2e](https://cairnrpg.com/second-edition/)). |
| **Knave** 1e (Ben Milton) | Classless B/X. Slots equal CON defense; one spell per spellbook per slot; group d6 initiative; 2d6 morale; 10 levels (Knave 1e text, CC BY 4.0). |
| **Knave** 2e | 10+CON slots; 100 careers (pick two, gain their gear); wounds fill slots; gold for XP on a progressive scale ([Gundobad Games](https://gundobadgames.blogspot.com/2023/04/lets-read-knave-2e-kickstarter-preview_27.html)). |
| **Mausritter** (Isaac Williams) | Cairn/ItO with mice: paw/body/pack slots, conditions take slots, usage dots, spells are tablets you overcharge, background from HP × pips ([Glaucus Hauriant](http://glaucushauriant.blogspot.com/2019/11/a-review-of-mausritter.html)). |
| **Maze Rats** (Milton) | **2d6 + stat, 10+ succeeds.** Three stats; spells made from two random words, regenerated each rest ([Necropraxis](https://necropraxis.com/2017/01/02/maze-rats-review/)). |
| **The Black Hack** 2e | Player-facing d20 roll-under (players roll to hit and to dodge); usage die ([Wikipedia](https://en.wikipedia.org/wiki/The_Black_Hack)). |
| **Black Sword Hack** | TBH + origins/backgrounds/gifts instead of classes; the Doom die tracks the attention of Law and Chaos ([Grognardia](http://grognardia.blogspot.com/2023/07/review-black-sword-hack.html)). |
| **Shadowdark** (Arcane Library) | 5e-readable OSR: gear slots, a real-time torch, talents rolled on level-up, spell checks with lockout and mishaps ([Zarban](https://zarban.com/2024/08/04/shadowdark-review/)). |
| **Whitehack** (Mehrstam) | Three classes (Deft/Strong/Wise) plus freeform **groups** (species/vocation/affiliation) that give a double roll; Wise miracles cost negotiated HP ([dieheart](https://www.dieheart.net/whitehack-2e-char-creation/)). |
| **Troika!** (Daniel Sell) | d66 table of 36 backgrounds, each a skill-and-gear bundle; no classes or levels; a token bag for initiative ([Doomslakers](http://doomslakers.blogspot.com/2020/10/troika-rpg-review.html)). |
| **Macchiato Monsters** (Nieudan) | Whitehack + TBH. Player-written traits plus a small menu of trainings; name your spells and pay HP; risk die ([RPGnet](https://www.rpg.net/reviews/archive/17/17491.phtml)). |
| **Dungeon Crawl Classics** (Goodman) | 0-level funnel; per-spell result tables with misfire, corruption and spellburn; Mighty Deeds ([Iron Tavern](https://irontavern.com/2012/08/24/dcc-rpg-the-wizard/)). |
| **Errant** (Ava Islam) | Procedure-heavy: hazard die, chases, downtime; text CC BY-SA 4.0 ([EN World](https://www.enworld.org/threads/errant.716452/)). |
| **Five Torches Deep** | 5e bridge: **4 classes × 3 archetypes each**, supply die, gear durability ([Azathought](https://www.azathought.com/review-five-torches-deep/)). |
| **Index Card RPG** | Effort dice by tier; Hearts measure every obstacle; mostly loot-driven advancement ([Glyph & Grok](https://glyphngrok.substack.com/p/game-review-index-card-rpg)). |
| **Tiny Dungeon 2e** | 2d6, any 5–6 succeeds; heritage plus 3 traits; a trait adds a die ([Deathtrap](https://deathtrap-games.blogspot.com/2020/09/game-review-tiny-dungeon-2e.html)). |
| *Reference:* **Dungeon World / World of Dungeons** | The 2d6 10+/7–9/6− bridge. Monsters never roll; a 7–9 on an attack means both sides land ([DW SRD](https://www.dungeonworldsrd.com/moves/), CC BY 3.0). |

---

## 2. Trick catalogue

Format: **what it is** · games · **buys** · **costs** · evidence.

### 2.1 Durability

**D1. Attacks always hit; roll damage only.**
Games: Into the Odd, Electric Bastionland, Cairn, Mausritter.
**Buys:** removes the to-hit roll entirely, which is roughly half the dice in a D&D fight. No whiff turns. Every exchange changes the state.
**Costs:** it reads as deterministic unless the referee narrates HP loss as near-misses. Armor has to be flat reduction or it does nothing.
**Evidence:** McDowall says ItO has two essential mechanics, saves and damage ([Oddular Mechanics](https://www.bastionland.com/2016/04/oddular-mechanics.html)). He also argues the label "auto-hit" misleads: HP loss is plaster blown off the wall beside you or a dent in your armour, and only damage past HP is a real wound ([Describing the Auto-Hit](https://www.bastionland.com/2015/03/describing-auto-hit-in-into-odd.html)). Newcomers were "playing like pros" by mid-session after five minutes of creation ([Newbies play report](https://www.bastionland.com/2015/08/into-odd-with-newbies-play-report.html)). Cairn 2e gives the same reasoning: auto-hit is there to keep combat fast and hectic ([Cairn 2e combat](https://cairnrpg.com/second-edition/wardens-guide/combat/)).

**D2. HP is grit; the overflow is the real injury.**
Games: ItO and Cairn (overflow comes off STR, then a STR save or you go down, dying within an hour without help); Mausritter (the same, down to death at STR 0); Knave 2e (overflow becomes **wounds that take inventory slots**, and you die when every slot is a wound).
**Buys:** HP stays one number, but losing it isn't bleeding. It refills after a short rest, so attrition happens *per fight*, and lasting consequences only come from genuinely bad fights. The critical-damage save is a clear "oh no" moment.
**Costs:** stat damage is harsh when stats are also your modifiers. Knave 2e dropped stat damage for exactly this reason and moved the overflow into slots instead ([Gundobad](https://gundobadgames.blogspot.com/2023/04/lets-read-knave-2e-kickstarter-preview_27.html)). Wounds-in-slots adds its own friction: players reorder their inventory to shed the cheapest items first ([Rancourt analysis](https://rancourt.substack.com/p/analysis-knave-2e)). **The app removes that friction.**
**Evidence:** it's the defining NSR combat model, copied by dozens of Cairn and Mausritter hacks. Community add-ons mostly *extend* the injury layer (treatment kits, scar variants) rather than replacing it ([Pointless Monument](https://pointlessmonument.blot.im/expanding-injury-in-cairn-and-elsewhere)).

**D3. Scars: landing on exactly 0 HP gives a mixed result that often makes you better.**
Games: Cairn 2e. The damage amount indexes a table that includes lasting marks, stat changes (sometimes *up*), and higher max HP.
**Buys:** close calls become advancement. The character's body tells the story of the campaign. Cairn uses it as one of its few mechanical growth routes ([Cairn 2e growth](https://cairnrpg.com/second-edition/wardens-guide/growth/); [Deathtrap review](https://deathtrap-games.blogspot.com/2021/12/game-review-cairn.html)).
**Costs:** needs a table (MM-side, which the app can roll). It's a narrow trigger.

**D4. Armor is flat damage reduction, with a cap.**
Games: Cairn (max 3), Mausritter (−1), ItO, World of Dungeons.
**Buys:** one subtraction. No AC math, no stacking puzzle.
**Costs:** at low damage it can make weak enemies harmless (−1 against d4). The usual fixes are the cap plus impaired/enhanced dice, or letting some attacks ignore armor.

**D5. Impaired / enhanced damage (d4 / d12) instead of modifiers.**
Games: Cairn, Mausritter, ItO. Bad position means d4 whatever you hold; good position means d12.
**Buys:** situational advantage becomes one word and one die swap. No +2s to track.
**Costs:** swingy. It overrides the weapon's identity in exactly the moments that matter.

**D6. Several attackers on one target: keep the highest damage die.**
Games: Cairn 2e. **Buys:** fast arithmetic, and focus-fire stops being degenerate. **Costs:** reads oddly ("three of us hit him and only one counted?"); needs narration.

**D7. Deprivation and Fatigue take slots.**
Games: Cairn (hunger or no rest adds Fatigue to the inventory, and casting from a spellbook adds Fatigue too); Mausritter (conditions such as Hungry, Exhausted, Frightened are slot cards).
**Buys:** one track for every "you're worn down" effect: carrying capacity, exhaustion, spell cost and wounds all share it. No separate condition list to learn; you just see the sheet fill up.
**Costs:** you have to keep slots physically scarce (about 10) or it bites too rarely.

**D8. Luck as a spendable, shrinking stat.**
Games: Troika! (Luck drops by 1 each time you test it) and DCC (burn Luck). **Buys:** a clear push-your-luck resource. Our Sparks already fill this niche, so it's noted only for comparison.

### 2.2 Gear

**G1. Inventory slots as the core of the sheet.**
Games: Knave (slots = CON defense; about 5 lb or 100 coins per slot), Knave 2e (10 + CON), Cairn (10), Mausritter (2 paw + 2 body + 6 pack), Shadowdark (STR or a minimum).
**Buys:** encumbrance players will actually track. Knave's designer note says slots are *also the key to character customization*, because what you carry determines who you are (Knave 1e text, CC BY 4.0). Every future system (wounds, fatigue, spells, loot) has a place to live.
**Costs:** someone has to write a gear list with slot counts. Coins need a conversion rule. Slot-shuffling is fiddly on paper, **and trivial in an app.**

**G2. Item-based classes: you are what you carry.**
Games: Knave (no classes; a spellbook makes you a caster, a bow an archer), Cairn, Mausritter, ICRPG (loot is the main source of growth).
**Buys:** zero class rules. Role changes mid-campaign by picking up gear. Treasure becomes character advancement, which is a reward loop that serves exploration.
**Costs:** characters can feel samey at creation. Players who want an *identity* from level 1 get less. Knave 2e's answer is two careers that grant both gear and an edge on checks ([Rancourt](https://rancourt.substack.com/p/analysis-knave-2e)).

**G3. Usage die for consumables.**
Games: The Black Hack (d20 down to d4; a roll of 1–2 steps it down, and 1–2 on a d4 means you've run out), Black Sword Hack (the same die repurposed as Doom), Macchiato Monsters (risk die for armor, gear, even treasure), Five Torches Deep (supply).
**Buys:** no arrow counting. A reviewer called TBH 2e "one of the purest refinements of a D&D hack" ([Wikipedia summary of reviews](https://en.wikipedia.org/wiki/The_Black_Hack)). The same device can meter anything: torches, rations, a patron's patience.
**Costs:** occasional feel-bad streaks. On paper it's another die to own; **in the app it's one tap.**

**G4. Usage dots on items and spells (three marks, then depleted).**
Games: Mausritter. **Buys:** durability, ammo and spell charges on one visual. **Costs:** needs item cards (the app has them).

**G5. Gear durability / quality.**
Games: Knave 1e (quality loss on critical hits), Five Torches Deep. **Buys:** another resource clock. **Costs:** repair bookkeeping. Low priority.

**G6. Light as a clock (torch).**
Games: Shadowdark (1 real-time hour). Evidence is split: fans praise the tension ([Roll Stats](https://rollstats.com/2024/08/09/shadowdark-rpg-review-old-school-feel-modern-mechanics/)), critics call it a gimmick that punishes real-time combat and breaks with a second torch ([Awful Good Games](https://awfulgoodgames.substack.com/p/the-shadowderp-torch-gimmick-is-stupid)). Knave 2e instead gives light sources different radius and search speed, a real slot trade-off ([Rancourt](https://rancourt.substack.com/p/analysis-knave-2e)).

### 2.3 Character creation

**C1. Roll-and-go stats (3d6 in order, or best 2 of 3d6 with one swap).**
Games: ItO, Cairn, Mausritter. **Buys:** a character in 5 minutes ([Bastionland play report](https://www.bastionland.com/2015/08/into-odd-with-newbies-play-report.html)). **Costs:** less player ownership. Needs an equalizer (C3).

**C2. Background / career tables that grant gear and a competence.**
Games: Knave 2e (roll or pick 2 of 100 careers; each gives items and a basis for advantage on checks), Troika! (d66 over 36 backgrounds, each a bundle of skills, items and weirdness), Electric Bastionland (100 failed careers), Cairn/Mausritter (background from the HP × pips grid).
**Buys:** instant identity and hooks. "Spy: caltrops, poison, forged papers" tells you who you are with no skill list.
**Costs:** someone has to write 36–100 entries. That's content, not rules, and it's the sort of thing the community will write for us.

**C3. "Worse rolls get better stuff."**
Games: Mausritter and Electric Bastionland (backgrounds cross-indexed so weak stats get stronger starting kit) ([Glaucus Hauriant](http://glaucushauriant.blogspot.com/2019/11/a-review-of-mausritter.html)). **Buys:** random stats without resentment. **Costs:** little.

**C4. Freeform words with a fixed edge (the key to custom classes).**
- **Whitehack groups:** you write your own vocation, affiliation or species; when one applies, you roll twice and keep the better. The Wise's vocation also makes related miracles cheaper ([dieheart](https://www.dieheart.net/whitehack-2e-char-creation/)).
- **Macchiato Monsters traits:** player-written ("retired infantry sergeant", "elven illusionist") plus a menu of trainings (combat, magic, specialist) and extra hit dice ([RPGnet review](https://www.rpg.net/reviews/archive/17/17491.phtml)).
- **Tiny Dungeon traits:** heritage plus 3 traits from a closed list; a trait adds a die (from 2d6 to 3d6 looking for a 5–6), about 67% against 50%. The critique: builds only cover a slice of non-combat situations, and monsters differ only by HP ([Deathtrap](https://deathtrap-games.blogspot.com/2020/09/game-review-tiny-dungeon-2e.html)).
- **Black Sword Hack:** origin (barbarian, civilized or decadent) + background (berserker, diplomat, assassin) + gifts ([Grognardia](http://grognardia.blogspot.com/2023/07/review-black-sword-hack.html)).

**Buys:** unlimited concepts from one rule. **Why they don't break:** the edge is *always the same size* and *doesn't stack*. Whitehack's double roll is a double roll however many groups apply. The words decide *where* you're good, never *how* good.
**Costs:** the referee arbitrates whether a word applies. Overly broad words ("adventurer") need a ruling at creation; Whitehack's answer is that the referee approves the wording.

**C5. Player skill instead of a skill list.**
Every game above lets the fiction settle most things: describe how you search and you find it. Maze Rats' reviewer praised its referee advice as the real engine ([Necropraxis](https://necropraxis.com/2017/01/02/maze-rats-review/)). Knave's designer note on opposed saves shows the aim: resolve anything with one roll, and let players do all the rolling (Knave 1e text).

**C6. The funnel (DCC).** Four random 0-level peasants each; survivors graduate. **Buys:** kills min-maxing and makes death funny. **Costs:** a whole session, and many find it grating: a long EN World thread argues it's a bad concept ([EN World](https://www.enworld.org/threads/dcc-level-0-character-funnel-is-a-bad-concept.686990/)), while defenders say it pushes players toward the character's hopes and fears rather than the numbers ([Azathought](https://www.azathought.com/dcc-review/)). **Optional one-shot mode only.**

### 2.4 Advancement

**A1. XP for treasure, discovery or goals, not kills.**
Games: Knave 1e (50/100/200 XP for low/moderate/high-risk accomplishments; 1000 per level; the designer says milestone or gold-for-XP work equally well), Knave 2e (gold for XP, progressive), Mausritter (pips brought home, or spent on the community at 10:1).
**Buys:** points play at exploration and clever avoidance. **Costs:** gold-only XP can drag. Knave 2e is criticized for sluggish levelling, and for making wilderness encounters pure loss once monster XP is gone ([Rancourt](https://rancourt.substack.com/p/analysis-knave-2e)). Maze Rats' vague "overcoming challenges" XP was also criticized ([Necropraxis](https://necropraxis.com/2017/01/02/maze-rats-review/)). **Lesson: name the triggers explicitly.**

**A2. Level-up gives plain numbers.**
Knave 1e: roll your new level in d8s for max HP (take it if higher, otherwise +1), and +1 to three stats of your choice. Mausritter: roll d20 against each stat (it rises if you roll over), roll for HP, and gain Grit (a virtual slot that soaks conditions).
**Buys:** visible power growth with zero new rules. It's the old-D&D feeling.

**A3. Talents at some levels (chosen, or rolled).**
Shadowdark: a talent at every odd level, rolled on a class table. Reviews call the rolled bonuses "boring" ([Zarban](https://zarban.com/2024/08/04/shadowdark-review/)). Five Torches Deep: abilities at levels 3 and 7, with the proficiency doubling at 9 ([Wandering Gamist](https://wanderinggamist.blogspot.com/2020/05/five-torches-review-part-1-contents.html)).
**Lesson:** a *short closed list you pick from* beats a roll. Offer "roll for inspiration, pick if you prefer".

**A4. No levels; growth from the fiction.**
Cairn: no XP. Growth comes from Scars, training with a master in downtime, faction milestones and strange encounters. It's triggered by sustained behaviour, risk-taking, or contact with unique things ([Cairn 2e growth](https://cairnrpg.com/second-edition/wardens-guide/growth/)). Troika: skills improve by use.
**Buys:** everything that happens is in the fiction. **Costs:** growth is hard to *feel* and fully up to the referee. A reviewer notes Tiny Dungeon's lack of levels also loses campaign arcs ([Deathtrap](https://deathtrap-games.blogspot.com/2020/09/game-review-tiny-dungeon-2e.html)).

**A5. Loot as advancement.** ICRPG: character identity mostly comes from gear and relics ([Glyph & Grok](https://glyphngrok.substack.com/p/game-review-index-card-rpg)). It pairs perfectly with G1/G2 and costs the MM nothing but tables.

**What gives power-growth fun without complexity:** (1) a number the player *sees* going up (HP, a stat), (2) one *choice* at some levels from a short list, (3) *things*: loot and relics, (4) one flavourful surprise channel (Scars). Every successful game in the survey uses at least three of the four.

### 2.5 Magic without big spell lists

| Approach | Games | Limit that keeps it honest | Evidence / cost |
|---|---|---|---|
| **Spellbook as item**, one spell per book, one cast per book per day | Knave 1e | Slots: a varied caster is a mule. Books can't be copied, so they're found as loot | The designer turned "spell slots" into physical slots (Knave 1e text) |
| **Spellbook costs Fatigue** (a slot) per cast | Cairn | Fatigue fills the shared slot track; it only clears with real rest | Magic erodes your carrying capacity and your safety margin at once |
| **Spell tablets with usage dots, overchargeable** | Mausritter | Power = the number of d6 you commit; sixes mark usage and can hurt you; recharging needs a unique ritual | Praised as a Vancian alternative that adds texture ([Glaucus Hauriant](http://glaucushauriant.blogspot.com/2019/11/a-review-of-mausritter.html)) |
| **Random two-word spells**, regenerated every rest | Maze Rats; Knave (random 100-list) | You don't choose, so you can't optimize; the effect is ruled once, at casting | [Prismatic Wasteland](https://www.prismaticwasteland.com/blog/spell-lists-are-not-magical) groups this as the "hard-coded prompt" family |
| **Soft-coded prompt**: random name, variable effect, paid from a stat | Prismatic Wasteland house system | The theme of the name bounds the effect; cost is negotiated | [Prismatic Wasteland](https://www.prismaticwasteland.com/blog/spell-lists-are-not-magical) |
| **Negotiated HP cost** (freeform miracles) | Whitehack (the referee sets a 1 to about 2d6+2 HP cost, cheaper inside your vocation; that HP only heals naturally); Macchiato Monsters (name spells, pay HP) | The caster spends the same pool that keeps them alive | Playtesters found the Wise *not* stronger than other classes ([dieheart](https://www.dieheart.net/whitehack-2e-combat/)) |
| **Spell check with lockout** | Shadowdark (fail and the spell is gone until rest; a natural 1 means a mishap table) | Casting is unreliable; each failure removes options | Common complaint: failure rates around 50% at low level feel bad; a popular house rule makes failure a *weaker* effect ([Glyph & Grok](https://glyphngrok.substack.com/p/shadowdarks-roll-to-cast-system), [Zarban](https://zarban.com/2024/08/04/shadowdark-review/)) |
| **Spell check with per-spell result tables, misfire, corruption, spellburn** | DCC | Danger and body horror; spellburn trades stats for power | Loved for its drama; heavy on text (every spell has its own table) ([Iron Tavern](https://irontavern.com/2012/08/24/dcc-rpg-the-wizard/)) |
| **Relics with charges** | Cairn, ItO arcana | Limited uses, bespoke recharge conditions | Magic as loot. Pure MM variety |

**What keeps freeform magic from dominating (the common threads):**
1. **Cost from a shared pool the caster also needs to survive** (HP, slots). This is the strongest brake, because the more you cast, the more fragile you are.
2. **Cost scales with ambition**, and the scale is *decided before the roll* (Whitehack's negotiation, Mausritter's dice committed).
3. **A failure mode that removes options** (Shadowdark lockout) or **adds danger** (DCC misfire), not just "nothing happens".
4. **Thematic bounds** (vocation, spell name, domain). Our Domain already does this.
5. **Referee arbitration of scope, with precedent.** Whitehack fixes the miracle wording at creation.

**Compared with our Domain + Intent + Scope:** we already have (4) and (5), and scope is our version of (2). The current limit, three readied intents per session, is a *count* that sits apart from everything else on the sheet. The NSR would tie full-form magic to the **shared attrition track** (grit or slots) instead, so the limit and the danger are one thing. See §6.3.

### 2.6 Initiative and turn structure

| Method | Games | Notes |
|---|---|---|
| **Players go first**, unless ambushed | Into the Odd (on ambush, a save decides whether the enemy goes first) ([Bastionland](https://www.bastionland.com/2011/08/project-odd-running-fighting-and-dying.html?m=1)) | Zero rolls in the normal case. Rewards scouting |
| **Round 1: DEX save to act, then PCs first** | Cairn 2e | Actions declared, then resolved simultaneously ([Cairn 2e](https://cairnrpg.com/second-edition/players-guide/core-rules/)) |
| **Side initiative, d6, rerolled every round** | Knave 1e, Maze Rats | Designer note: speeds combat, keeps everyone engaged, avoids bookkeeping; rerolling lets a side go twice, which is dangerous (Knave 1e text) |
| **Individual DEX check** | Shadowdark | Familiar to 5e players; slower |
| **Token bag with an end-of-round token** | Troika! | Chaotic and fun; needs a bag ([Doomslakers](http://doomslakers.blogspot.com/2020/10/troika-rpg-review.html)). **In an app, free** |
| **No initiative; the fiction moves, players roll, monsters react** | Dungeon World / World of Dungeons | Monsters never roll; a 7–9 lets the enemy's blow land too ([DW SRD](https://www.dungeonworldsrd.com/moves/)) |

**Speed:** with auto-hit plus side initiative, NSR fights typically end in 2–4 rounds. Deadliness plus morale is what cuts them short.

### 2.7 Morale

Monsters get a morale number (Knave: usually 5–9). The referee rolls 2d6 when the enemy faces more danger than expected: the first death, half the group down, the leader down, or a lone enemy at half HP. Over the number means it flees, retreats or parleys (Knave 1e text; OSE has the same idea on 2–12 ([OSE SRD](https://oldschoolessentials.necroticgnome.com/srd/index.php/Morale_(Optional_Rule)))). Cairn uses a WIL save at the first casualty and again at half strength ([Cairn 2e](https://cairnrpg.com/second-edition/players-guide/core-rules/)).

**Why it makes fights short:** the fight ends when one side *breaks*, not when it's dead. That's about half the HP-grind. Players learn to kill the leader, show overwhelming force and make terrifying displays, which is tactics without rules. Rideout argues removing morale meant to simplify play but did the opposite: GMs now decide alone when enemies flee, fights run to the death, and they last longer ([Deathtrap: Lost Mechanics: Morale](https://deathtrap-games.blogspot.com/2020/11/lost-mechanics-morale.html)). DMDavid makes the same "fight rarely, fight dirty" point ([DMDavid](https://dmdavid.com/tag/morale-checks-does-wisdom-make-one-courageous-or-wise/)). PCs have no morale in Cairn: the players decide when to run.

---

## 3. Evidence quality note

Most "how it plays" evidence is reviews and designer blogs, not controlled data. The strongest signals: (a) a *designer changes the rule in a later edition* (Knave 2e dropping stat damage and switching to gold-for-XP; Cairn 2e adding Scars as growth); (b) *the same house rule turns up independently* (Shadowdark casters getting a weaker effect on failure; torch-timer alternatives); (c) *hack proliferation* (auto-hit/grit/slots across the Cairn, Mausritter and ItO families). I weighted those over single reviews.

---

## 4. Licence table

GPLv3 note: Creative Commons declared **CC BY-SA 4.0 one-way compatible with GPLv3**, so BY-SA 4.0 text can be adapted into a GPLv3 work. CC BY is compatible too (attribution only). **OGL 1.0a content is not GPL-compatible** in practice: it requires its own licence text, a Section 15 chain and Product Identity exclusions. Keep OGL text out of the books. Game *mechanics* as ideas aren't protected by copyright, but we don't lean on that; we describe everything in our own words anyway.

| Game | Licence (as verified) | Share-alike? | Borrow **text** into our GPLv3 books? | Borrow **concepts**? |
|---|---|---|---|---|
| Knave 1e | CC BY 4.0 (stated in the rulebook text) | No | **Yes**, with attribution (title, "Ben Milton", source link, licence link, "changes made") | Yes |
| Knave 2e | Has a third-party licence; **no CC statement found** on its store page | n/a | **No**: treat as all rights reserved | Yes |
| Cairn 1e / 2e | CC BY-SA 4.0 ([cairnrpg.com](https://cairnrpg.com/second-edition/players-guide/core-rules/); [GitHub](https://github.com/yochaigal/cairn)) | **Yes** | **Yes**: credit Yochai Gal, mark changes, and adapted passages carry BY-SA (fine inside GPLv3 via one-way compatibility) | Yes |
| Maze Rats | CC BY 4.0 ([itch](https://questingbeast.itch.io/maze-rats)) | No | Yes, with attribution | Yes |
| Mausritter | SRD under CC BY 4.0 since 2025 ([BoLS](https://www.belloflostsouls.net/2025/06/rpg-mausritters-rules-released-into-creative-commons-srd.html); [licence page](https://mausritter.com/third-party-licence/)) | No | Yes (SRD only; credit Losing Games / Isaac Williams) | Yes |
| Errant | Text CC BY-SA 4.0, art excluded ([EN World](https://www.enworld.org/threads/errant.716452/)) | Yes | Yes (as for Cairn) | Yes |
| Dungeon World | CC BY 3.0 ([DW SRD](https://www.dungeonworldsrd.com/moves/)) | No | Yes with attribution (3.0 → GPLv3 is less formally blessed than 4.0; **prefer paraphrase**) | Yes |
| Into the Odd / Electric Bastionland | Custom **Mark of the Odd** licence + MOTO SRD ([Bastionland](https://www.bastionland.com/2020/11/mark-of-odd-licence-and-srd.html)); terms are in a Drive folder I couldn't read | Unverified | **No** (unverified) | Yes |
| Troika! | Custom permissive SRD terms, roughly "credit me, don't pass it off as mine, don't resell my words unmodified" ([MAC devlog](https://melsonian-arts-council.itch.io/troika-numinous-edition/devlog/104412/srd)) | No (not CC) | **No**: not a GPL-compatible licence | Yes |
| The Black Hack 1e/2e | OGL 1.0a | OGL | **No** | Yes |
| Black Sword Hack | Built on TBH 2e; licence **not verified** (presumed OGL) | ? | **No** | Yes |
| Whitehack | OGL (2e) ([Adventuresmith attribution](https://github.com/stevesea/Adventuresmith/blob/master/content_attribution.md)) | OGL | **No** | Yes |
| DCC | OGL, with extensive Product Identity | OGL | **No** | Yes |
| Old-School Essentials | OGL SRD | OGL | **No** (reference only) | Yes |
| Shadowdark | Bespoke Third-Party Licence: verbatim only for monsters, spells and items; **explicitly excludes standalone games that reword or replace its core rules** ([FAQ](https://www.thearcanelibrary.com/blogs/shadowdark-blog/faq-on-the-shadowdark-rpg-third-party-license)) | n/a | **No** | Concepts only, generic ones (slots, spell checks exist in many games). **Do not present anything as Shadowdark-derived** |
| Five Torches Deep | 5e SRD/OGL-based; not verified | ? | No | Yes |
| Macchiato Monsters | **Not verified** | ? | No | Yes |
| Index Card RPG | Proprietary (Runehammer); not verified | n/a | No | Yes |
| Tiny Dungeon 2e | Gallant Knight Games; **not verified** | n/a | No | Yes |

**Practical rule for the project:** we write every mechanic in our own words (the house policy already requires it). The CC BY / BY-SA games are the *only* ones where a reused sentence or table would be defensible, and even then we should prefer paraphrase and add a credits line ("Grit/overflow and slot-based fatigue inspired by *Cairn* (Yochai Gal, CC BY-SA 4.0) and *Into the Odd* (Chris McDowall)"). Credit is good manners even where only an idea is used.

---

## 5. The Facet → class question (owner constraints)

**The constraint:** Body / Mind / Soul stay, as Morrowind-style **specializations** (Combat / Magic / Stealth). A player may define their own class inside a Facet; preset classes are just suggested builds.

### 5.1 How the surveyed games "build your own class", and how each would sit under a Facet

| Model | How it works | Under a Facet | Quick? | Hard to break? |
|---|---|---|---|---|
| **Knave item-classes** | No class: the gear you carry *is* the role | The Facet sets slot count / the HP die; the class is its *kit* | Very | Very (slots cap everything) |
| **Troika backgrounds** | Rolled bundle of skills, gear and oddity | A preset class is a Troika-style bundle; the Facet's table offers 12–36 of them | Very (roll one) | Depends on authored balance |
| **Whitehack groups** | Freeform vocation/affiliation words; the edge is a double roll that doesn't stack | Custom class = name + two freeform "knacks"; the Facet decides which *stat* they usually attach to | Very | **Very** (fixed edge size) |
| **Tiny Dungeon traits** | Pick 3 from a closed list; each adds a die | The Facet's talent list is the closed list | Quick | Yes, but narrow builds |
| **Maze Rats / Cairn background tables** | Rolled background → gear and hooks; Maze Rats picks abilities at level-up | Random-start option: the Facet table gives a background and kit | Very | Yes |
| **Black Sword Hack** | Origin + background + gifts | Origin ≈ Lineage/setting; background ≈ class; gifts ≈ Facet talents | Quick | Mostly |
| **Macchiato Monsters** | Freeform traits + a small training menu (combat, magic, specialist, extra HD) | **The closest Morrowind analogue**: the menu is the Facet-owned part, the traits are the class | Quick | Yes, if the menu is small |
| **Five Torches Deep** | 4 classes × 3 archetypes | The published precedent for exactly Facet → preset class | Quick | Yes |

### 5.2 The split I recommend: the Facet owns the numbers, the class owns words and things

**The Facet (specialization) owns everything balance-relevant:**
1. **Stat lean**: +2 in its own stat (Body/Mind/Soul), as in the §7.3 sketch.
2. **Grit die** (HP per level): Body d8, Soul d6, Mind d6 (or a fixed amount per level, which the app handles either way).
3. **Slot bonus**: Body +2 slots (the carrier); others base 10. This is the Knave "raise CON to carry more" lever, moved onto the Facet.
4. **Its talent list**: about 8–10 talents, each one sentence. **Morrowind rule:** your *own* Facet's talents are always available when you pick; an *off-Facet* talent costs your pick plus a condition (a trainer found in play, per Cairn's masters, or it's only available at even levels). That's the "specialization makes your own things cheaper" feel without skill-rate arithmetic.
5. **Magic tradition access**: Mind → Thaumaturgy, Soul → Invocation, Body → none (canon, per MEMORY). A Body character reaches magic only through off-Facet talents or relics.
6. **The kit allowance**: how much starting gear value and which armor classes (Body: any; Mind and Soul: light), which is the only restriction class-by-kit needs.

**The class (preset or custom) owns only:**
1. **A name and a one-line concept** ("Hedge-knight of the ferry roads"). Pure flavour.
2. **Two knacks**: freeform words (Whitehack groups / Macchiato traits), e.g. *"ferry roads"*, *"oaths and duels"*. When a knack covers the task, the roll gets **+1** (or roll 3d6 and keep the best 2; pick one and never stack). **Specialty = no roll** stays exactly as in the §7.3 sketch; a knack is the broader version.
3. **A starting kit** chosen within the Facet's allowance and **limited by slots** (Knave/Knave 2e careers: the items *are* the role).
4. **First talent pick** from the Facet list, and for casters the **domain** (which already works as a thematic bound, like Whitehack's vocation making related miracles cheaper).

**Preset classes** are then just filled-in examples of those four lines: Body → Warrior, Scout, Brawler, Hedge-knight; Mind → Scholar, Artificer-type, Tactician; Soul → Speaker, Wanderer, Luck-touched. Following Troika, Electric Bastionland and Knave 2e, each Facet can also carry a **d12 or d20 table of preset classes** for players who want to roll and go (with C3: the weaker your stat roll, the better the kit).

### 5.3 Why custom builds stay quick and hard to break

- **No custom numbers.** Custom classes write *words* and pick *things* from bounded lists. Every number (HP die, stat lean, slots, talent power) comes from the Facet. That's the whole Whitehack/Macchiato safety model.
- **Fixed-size, non-stacking edge.** Two knacks that both apply still give one +1. Knacks decide *where*, never *how much*.
- **Slots cap item power.** A class that wants everything carries nothing else, and wounds and fatigue eat into the same slots.
- **Closed talent lists, each balanced once** (by the sim, per the sync rule), rather than open design space.
- **MM approves the knack wording at creation** (Whitehack precedent), with one guideline: *a knack names a trade, a place, a people or a tradition, not a verb like "fighting" or "noticing".* The app can offer examples and flag single-verb knacks.
- **Time budget:** Facet (1 choice) → stats (fixed spread or roll) → class (pick a preset or write a name plus two knacks) → kit (tap items until slots fill) → one talent → (casters) domain. Five to ten minutes, which is the NSR benchmark.

---

## 6. Implications for a lean Facets of Origin

### 6.1 Adopt (11)

1. **Grit HP (D2) for PCs and monsters alike.** HP is near-misses and fatigue; it refills after a breather. This implements §7.1's "HP for everyone" and §5-B's grit model with a decade of NSR evidence behind it.
2. **Weapon damage dice + flat armor with a cap (D4).** One subtraction; armor 1–2 (a cap of 3 including a shield). Serves the Butt-Kicker the fun audit found underserved.
3. **Overflow becomes a Wound in an inventory slot (D2, Knave 2e; D7, Cairn).** The current Condition list becomes the Wound list. The app sorts which item gets dropped, which removes Knave 2e's known friction.
4. **Scars at exactly 0 (D3).** An MM-side table the app rolls. Close calls pay out in character: the flavourful growth channel.
5. **Inventory slots as the sheet (G1), about 10 + Facet bonus.** Wounds, Fatigue and full-form magic all share it (§6.3). This one track *replaces* Endurance, the armor budget and the Tier-1 conditions.
6. **Usage die for consumables (G3).** Torches, arrows, rations, bandages, even a patron's patience. One tap in the app.
7. **Class = Facet numbers + words + kit (§5).** Morrowind-style specialization with Whitehack-style knacks and Knave-style kits.
8. **Level-ups of plain numbers plus a pick from a short list (A2 + A3).** HP (roll or take the average), +1 to a stat every third level, and a Facet talent at odd levels, *chosen* ("roll for inspiration" optional). **XP from named triggers** (discovery, goal, treasure returned, a Spark-worthy moment), not kills or rolls. That keeps the §7.3 end-of-session questions and avoids Maze Rats' vague "challenges".
9. **Loot and relics as MM variety (A5, Cairn relics).** Relics with charges and bespoke recharge conditions are the cheapest content-driven power growth, and the app's tables make them free for the MM.
10. **Players go first; ambush by a single roll (2.6).** No initiative bookkeeping at all in the normal case.
11. **Morale, rolled by the app (2.7).** 2d6 against a morale number at the first death, half the group down, or the leader down; over means flee, surrender or parley. It's MM procedure, so players never learn it, and it's the single biggest combat-length lever.

### 6.2 Avoid (or make optional)

- **Ability-score damage** (ItO/Cairn). With three stats that are also the 2d6 modifiers, stat loss cripples. Knave 2e dropped it for this reason. Use Wounds in slots.
- **Real-time torch** (Shadowdark). Divisive, fragile, and it punishes slow players. At most an optional app timer toggle.
- **Rolled talents with no choice** (Shadowdark). Reviewed as boring. Pick from a list.
- **Per-spell result tables** (DCC). Great drama, far too much text. One shared **mishap table** is enough.
- **Spell lockout on a ~50% fail** (Shadowdark). It feels bad, and the most common house rule softens it. Our 7–9 already gives the "weaker effect" tier those house rules invent.
- **Gold-only XP** (Knave 2e). Criticized as slow. Use mixed, named triggers.
- **Funnel as default** (DCC). Keep it as an optional one-shot / convention mode; the app can generate four peasants per player.
- **Flat 1 damage** (Tiny Dungeon). Monsters become HP totals only. Keep damage dice plus one monster gimmick.
- **No-levels growth only** (Cairn). Keep Scars and trainers as *spice*, not as the whole advancement system.
- **Token-bag initiative** (Troika): fun, but it adds a subsystem. Players-go-first is lighter. (The app *could* offer it as a variant.)

### 6.3 Magic under the lean chassis

Keep **Domain + Intent + Scope** (it's a differentiator; §7.2) but **tie the limit to the shared attrition track** instead of the separate three-readied-intents count:

- **Minor:** free, as now (the D25 full-form rule stays: meaningful power or precision is not Minor).
- **Significant:** roll as now, and **take 1 Fatigue** into a slot (Cairn's spellbook model).
- **Major:** roll at the domain's difficulty and **take 2 Fatigue**, or 1 Fatigue plus *spend grit* equal to a die (Whitehack/Macchiato).
- **6−:** the MM picks from one shared **mishap table** (DCC/Shadowdark, collapsed to one page), and the effect still happens at the Minor-scope floor or not at all. **7–9:** the effect happens, weaker or with a cost (this *is* the popular Shadowdark house rule, built in).
- **Fatigue clears on real rest** (a night in safety), exactly as the readied intents refresh now.

**Why this limits freeform magic better than a count:** the caster's spell budget, carrying capacity and wound buffer are **the same 10 slots**. A caster who casts a lot is one bad hit from a Wound. That's the Whitehack evidence (HP-cost casters were not stronger), and it deletes one rule (the intent count and its purposes) rather than adding one. **Option to keep D23 instead:** readied intents become physical **foci** that take a slot each and are spent (Mausritter tablets / Knave spellbooks). That keeps the purposes and still ties magic to slots. Either way, it's the owner's ruling, since D23 is recent.

### 6.4 The central combination: grit HP + damage on a 2d6 10+ / 7–9 / 6− roll where only players roll

**The base odds (2d6 + modifier):**

| Mod | 6− | 7–9 | 10+ |
|---|---|---|---|
| +0 | 41.7% | 41.7% | 16.7% |
| +1 | 27.8% | 44.4% | 27.8% |
| +2 | 16.7% | 41.7% | 41.7% |
| +3 | 8.3% | 33.3% | 58.3% |

With a typical +2 attack, a hit (7+) comes up **83%** of the time. That's already almost "attacks always hit", so **the 2d6 roll is not deciding *whether* you hit. It decides *what it costs you*.** That's exactly the NSR insight in PbtA clothing, and it's why the combination works.

**Attack (a player strikes):**
- **10+:** deal your weapon die. Pick one: *+1d6 damage and take their blow* (the DW trade), **or** *enhanced: roll d12 instead* (only when your position justifies it; Cairn's D5) **or** *a stunt* (push, disarm, reposition, as in Knave).
- **7–9:** deal your weapon die, **and the foe's blow lands on you** (their fixed damage minus your armor).
- **6−:** the foe's blow lands, and the MM makes a move (a Trouble Table pull, a morale-shifting reinforcement, a separated ally).

**Defend (something is done *to* you and you aren't attacking; the MM says "the ogre swings at Mordai"):** roll 2d6 + the relevant stat: **10+** no damage; **7–9** take the damage minus armor (or half, pick one rule and tune in the sim); **6−** full damage, and armor still applies. *Intercept* = Defend for an ally.

**Monsters never roll:**
- **Fixed damage by tier** (Mook 2, Named 3, Boss 4 plus its gimmick), or a die the *player* rolls. Fixed is faster, and armor against a fixed number is easy to balance.
- **HP by tier** (Mook ~3 so one hit usually drops it; Named 8–12; Boss 20+ with a phase at half), **armor 0–2**, **one special thing**, **morale 5–9**. That's the whole stat block, and it replaces Resolve, riders and TR arithmetic.

**When PC HP runs out:**
- Excess damage past 0 → **roll 2d6 + Body** (the ItO critical-damage save in 2d6 form): **10+** a Wound in a slot, fight on; **7–9** a Wound, and you're *out of the fight* but conscious (you can crawl, talk, hand something over); **6−** a Wound, and you're **dying**: an ally has until the end of the scene (or an hour of fiction) to tend you. The existing death choice sits here.
- **Exactly 0** → roll on the **Scars** table instead of taking a Wound (D3).
- **All slots full of Wounds, or a second 6−, means death.** One track, visible on the sheet.

**Recovery:** a breather (a few minutes, a drink) restores grit to full (or the Facet die per breather if full-refresh sims too generous). **Wounds and Fatigue only clear with real rest** (a night in safety), and Wounds may need treatment. The consequence moves out of HP and into the sheet, just as in Cairn.

**Why it holds together:**
- **One player roll per exchange** settles both directions. No reactions, no Endurance economy, no postures. That's §7.1's goal, now with the NSR's proven durability layer under it.
- **Auto-hit feel with PbtA texture:** hits almost always happen; the tier tells you whether you paid for it.
- **Morale ends most fights** before HP does, so HP pools can stay small and fights stay 2–4 exchanges.
- **Armor matters every exchange** because damage always flows. The §5-B worry about Mooks becoming toothless is the old-school feature; tune it with Mook damage 2 against armor max 2 so a heavily armored PC can wade through Mooks, which is the fantasy, while Named foes still bite.

**Risks to simulate (the sim must drive `combat.py`):**
(a) A +0 attacker takes damage about 83% of the time on an attack; confirm that fixed Mook damage against starting grit gives the intended 3–4 exchanges of survivability.
(b) The 10+ "+1d6 and take their blow" option may be strictly dominant against Mooks; DW's known complaint is that "avoid damage" is less useful than "kill it" ([Spouting Lore](https://spoutinglore.blogspot.com/2018/09/hack-slash-part-ii.html)).
(c) Whether full grit refresh on a breather is too generous; Knave refreshes 1d8 + CON a night, while Cairn refreshes fully after a short rest *at the cost of exposure* (a wandering-monster check). The app can roll that.
(d) Defend's 7–9 rule: armor-only is simplest, half is gentler.

### 6.5 What this deletes from the current build

Endurance pool, the four reactions and their costs, postures, Tier-1 Conditions, rider rules, the armor downgrade budget and its no-stack exception, the Resolve/TR split for enemies, the D16 skill caps and the skill list, and (if §6.3 is taken) the readied-intents count. What survives: 2d6 three-tier resolution, Sparks / Graceful Fail / Borrowed Trouble, Domain + Intent + Scope, Specialty-means-no-roll, the Condition list (as Wounds), NPCs-never-roll, and the whole MM-side toolset. That's the set §7.2 already called our differentiators.

### 6.6 Next step

Consistent with §7.4: write **Lean Facets on two pages** using §5.2 and §6.4, encode three monsters (Mook, Named, Boss) and three presets per Facet in `facet.yaml`, run the sim on the §6.4 risks, and put it in front of a human table alongside the current rules.

---

## Sources

Primary/SRD: [Cairn 2e core rules](https://cairnrpg.com/second-edition/players-guide/core-rules/) · [Cairn 2e combat](https://cairnrpg.com/second-edition/wardens-guide/combat/) · [Cairn 2e growth](https://cairnrpg.com/second-edition/wardens-guide/growth/) · [Cairn GitHub](https://github.com/yochaigal/cairn) · Knave 1e rulebook text (CC BY 4.0; [itch](https://questingbeast.itch.io/knave)) · [Dungeon World SRD moves](https://www.dungeonworldsrd.com/moves/) · [OSE SRD morale](https://oldschoolessentials.necroticgnome.com/srd/index.php/Morale_(Optional_Rule)).
Designer blogs: [Bastionland: Oddular Mechanics](https://www.bastionland.com/2016/04/oddular-mechanics.html) · [Describing the Auto-Hit](https://www.bastionland.com/2015/03/describing-auto-hit-in-into-odd.html) · [ItO with Newbies](https://www.bastionland.com/2015/08/into-odd-with-newbies-play-report.html) · [How I Run ItO](https://www.bastionland.com/2015/09/how-i-run-into-odd.html) · [Running, Fighting and Dying](https://www.bastionland.com/2011/08/project-odd-running-fighting-and-dying.html?m=1) · [Mark of the Odd](https://www.bastionland.com/2020/11/mark-of-odd-licence-and-srd.html) · [Ben Milton interview (Thaumavore)](https://thaumavore.substack.com/p/ben-milton-sets-the-record-straight).
Licences: [Shadowdark TPL FAQ](https://www.thearcanelibrary.com/blogs/shadowdark-blog/faq-on-the-shadowdark-rpg-third-party-license) · [Mausritter licence](https://mausritter.com/third-party-licence/) · [Mausritter SRD news (BoLS)](https://www.belloflostsouls.net/2025/06/rpg-mausritters-rules-released-into-creative-commons-srd.html) · [Troika SRD devlog](https://melsonian-arts-council.itch.io/troika-numinous-edition/devlog/104412/srd) · [Maze Rats itch](https://questingbeast.itch.io/maze-rats) · [Knave 2e itch](https://questingbeast.itch.io/knave-second-edition) · [Adventuresmith attributions (Whitehack OGL)](https://github.com/stevesea/Adventuresmith/blob/master/content_attribution.md).
Reviews/analysis: [Gundobad: Knave 2e](https://gundobadgames.blogspot.com/2023/04/lets-read-knave-2e-kickstarter-preview_27.html) · [Rancourt: Knave 2e analysis](https://rancourt.substack.com/p/analysis-knave-2e) · [Glaucus Hauriant: Mausritter](http://glaucushauriant.blogspot.com/2019/11/a-review-of-mausritter.html) · [Necropraxis: Maze Rats](https://necropraxis.com/2017/01/02/maze-rats-review/) · [Prismatic Wasteland: Spell Lists](https://www.prismaticwasteland.com/blog/spell-lists-are-not-magical) · [dieheart: Whitehack creation](https://www.dieheart.net/whitehack-2e-char-creation/) · [dieheart: Whitehack magic](https://www.dieheart.net/whitehack-2e-combat/) · [dieheart: Macchiato Monsters](https://www.dieheart.net/lr-mmz-01/) · [RPGnet: Macchiato Monsters](https://www.rpg.net/reviews/archive/17/17491.phtml) · [Grognardia: Black Sword Hack](http://grognardia.blogspot.com/2023/07/review-black-sword-hack.html) · [Grognardia: Electric Bastionland](http://grognardia.blogspot.com/2020/09/review-electric-bastionland.html) · [Deathtrap: Tiny Dungeon 2e](https://deathtrap-games.blogspot.com/2020/09/game-review-tiny-dungeon-2e.html) · [Deathtrap: Cairn](https://deathtrap-games.blogspot.com/2021/12/game-review-cairn.html) · [Deathtrap: Morale](https://deathtrap-games.blogspot.com/2020/11/lost-mechanics-morale.html) · [DMDavid: Morale](https://dmdavid.com/tag/morale-checks-does-wisdom-make-one-courageous-or-wise/) · [Doomslakers: Troika](http://doomslakers.blogspot.com/2020/10/troika-rpg-review.html) · [Zarban: Shadowdark](https://zarban.com/2024/08/04/shadowdark-review/) · [Roll Stats: Shadowdark](https://rollstats.com/2024/08/09/shadowdark-rpg-review-old-school-feel-modern-mechanics/) · [Awful Good Games: torch](https://awfulgoodgames.substack.com/p/the-shadowderp-torch-gimmick-is-stupid) · [Glyph & Grok: Shadowdark casting](https://glyphngrok.substack.com/p/shadowdarks-roll-to-cast-system) · [Glyph & Grok: ICRPG](https://glyphngrok.substack.com/p/game-review-index-card-rpg) · [Iron Tavern: DCC wizard](https://irontavern.com/2012/08/24/dcc-rpg-the-wizard/) · [EN World: DCC funnel thread](https://www.enworld.org/threads/dcc-level-0-character-funnel-is-a-bad-concept.686990/) · [Azathought: DCC](https://www.azathought.com/dcc-review/) · [Azathought: Five Torches Deep](https://www.azathought.com/review-five-torches-deep/) · [Wandering Gamist: FTD](https://wanderinggamist.blogspot.com/2020/05/five-torches-review-part-1-contents.html) · [Pointless Monument: Cairn injury](https://pointlessmonument.blot.im/expanding-injury-in-cairn-and-elsewhere) · [Spouting Lore: Hack & Slash](https://spoutinglore.blogspot.com/2018/09/hack-slash-part-ii.html) · [EN World: Errant](https://www.enworld.org/threads/errant.716452/) · [Wikipedia: The Black Hack](https://en.wikipedia.org/wiki/The_Black_Hack).

*Verification gaps: Knave 2e, Black Sword Hack, Macchiato Monsters, Tiny Dungeon, ICRPG and Mark of the Odd licence terms were not confirmed (the web-search budget ran out). All are treated as concept-only, which is the safe default.*
