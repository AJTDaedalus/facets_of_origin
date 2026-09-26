# RESEARCH: The D&D-Chassis-on-a-Light-Engine Lineage, and the Resolution-Core Question

**Date:** 2026-09-25 · **Status:** complete (research agent) · **Tier:** research input to a Brain-tier decision. Every recommendation here is a proposal. The rulings are the owner's.
**Question:** Which games put a D&D-shaped fantasy chassis (classes, HP, damage, spells, levels) on a light narrative engine, what went right and wrong for them, which dice core fits a lean Facets of Origin, and what do we legally get to borrow?
**Read first:** `docs/RESEARCH_complexity_audit.md` §1 and §7 (the "Lean Facets" sketch), `research/dice_system_analysis.md` ("NPCs never roll").
**Siblings (not duplicated here):** `RESEARCH_comparative_combat_landscape.md` (21-system combat survey), `RESEARCH_lean_nsr.md` (Cairn/Knave/Into the Odd/Shadowdark), `RESEARCH_lean_mm_variety.md` (MM procedures and generators).

**Copyright discipline.** Every mechanic below is described in my own words. No move text, class sheet, stat block or table has been copied from any game, open or closed. Where a text is openly licensed I say what attribution reuse would need, but the file itself only paraphrases. Game *mechanics* as such are generally not protected by copyright; their *expression* is. That is the working rule here. It is not legal advice, and any verbatim reuse should get a proper licence check first.

**Method note.** About 45 web sources: SRDs and licence pages, designer blogs (including DW2's own development posts, which turned out to be the single most relevant source), reviews, forum threads. I computed the probabilities myself (`python`, scripts in the session scratchpad). The web-search quota ran out near the end, so a few details are marked *unverified* rather than guessed.

---

## Summary

1. **Our exact brief has been attempted in public for the past 14 months, and the result is directly usable evidence.** Dungeon World 2's designers first dropped HP and damage dice (Blue alpha, July 2025), then restored six stats, HP and damage dice (Red alpha, September 2025). Their playtesters split roughly 50/50. The beta (September 2026) keeps HP and damage dice. Their stated conclusion was that "the feel of D&D" comes mostly from **familiar vocabulary**, not from particular mechanics. This supports the audit's §7 move back to HP.
2. **HP's known weakness in narrative games is that "only the last hit point matters."** DW2's diagnosis is that a middling hit changes a number but not the story. The fix that stuck is not removing HP. It is making **each successful hit also change the fiction**: pick an effect from a short menu, and have a hurt enemy *escalate*.
3. **Dungeon World's real failures were specific and avoidable.** Defy Danger was a catch-all whose 7–9 result gave the GM nothing to work with. Jargon ("+1 forward", "hold") put people off. There was no difficulty scaling, so a landslide was as hard as an avalanche. Magic was fiddly and Vancian. Repeated Hack & Slash was monotonous. Trading blows on a 7–9 made fragile characters spiral into failure. Every descendant (Homebrew World, Chasing Adventure, Stonetop, DW2) fixed some subset of these, and they converged on the same fixes: **advantage dice instead of +1s, fewer and sharper basic moves, backgrounds instead of race/alignment, conditions or injuries alongside HP, and concrete 7–9 menus.**
4. **Our current core (2d6, three tiers, Spark as +1d6 keep best 2) matches what that lineage converged on.** Homebrew World and Chasing Adventure both replaced ±1 with an extra die, keep best/worst. **Keep 2d6 three-tier.** Its hard limit is that flat bonuses must stay small (≤ +3), so character growth has to come from options, HP and loot, not from +N.
5. **d20 is the familiarity winner but the partial-success loser.** A d20 check can grow a "missed by ≤4 = partial" band, but that band is a flat 25% at every skill level, and the flat distribution is swingy. 2d10 (Draw Steel) and d6-pool (Blades) both give native three tiers. Neither beats 2d6 for this project once our existing Spark economy and sunk work are counted. See the comparison table.
6. **Player-facing rolling works, and the lineage shows how to express threat without enemy dice.** A monster's level or HD makes the player's *defence* roll harder (Black Hack, Cypher). Its fixed damage number or damage die is rolled by the player (DW). One gimmick per monster, plus an escalation when it gets hurt (DW2). The recorded failure modes are variance piling onto one player, underpowered monsters (Black Hack), armour stalemates (Numenera), and GM intrusions that feel like "gotcha" moments (Numenera).
7. **The "trade blows" pattern (7–9: both sides deal damage) is lethal to fragile characters.** In my simulation, a d4, 5-HP wizard meleeing a single 3-HP goblin goes down 71–78% of the time, while a fighter at +2 finishes it in ~1.6 rolls. Any lean combat built on this pattern needs non-melee options for fragile Facets and small, fixed monster damage.
8. **Licences.** Text we could legally fold into GPLv3 rules text: **WWN SRD (CC0)**, **Knave 1e / Ironsworn & Starforged SRD (CC BY 4.0)**, and **Stonetop / Cairn (CC BY-SA 4.0**, one-way into GPLv3 only). Dungeon World, World of Dungeons and Blades (CC BY 3.0) are usable with attribution but not formally declared GPL-compatible. Homebrew World and Freebooters (CC BY-SA 3.0) are not GPL-compatible for text. **13th Age and Black Hack (OGL 1.0a), Daggerheart (DPCGL), Draw Steel (Creator License), Cypher (CSOL), Troika, ICRPG, Savage Worlds and GURPS: concepts only.** Recommendation: **paraphrase everything anyway**, and keep one ATTRIBUTIONS file for concept debts.
9. **Facet → class (owner constraint, Morrowind model).** The chassis fits cleanly if **the Facet owns the durable, balance-critical numbers** (its stat, HP die, ability menu, magic tradition, one Facet move) and **the class is just a named selection from that menu**: a sentence, three picks, a background, a kit, and at most one pick from outside the Facet. Preset classes are saved selections. This is how 13th Age talents, Cypher's sentence and Daggerheart's domain pairs already work, and it avoids the two proven traps: GURPS-style point-buy under a template veneer, and Morrowind-style use-based levelling that can be gamed.
10. **Net recommendation.** For the *engine*, take concepts from **Homebrew World** (leanest DW). For *combat that changes the fiction*, take them from **DW2**. For *MM-side procedure*, from **Freebooters / WWN**. For *advancement and backgrounds*, from **13th Age**. For *escalation and making threat legible without enemy rolls*, from **13th Age and Black Hack**. The dice stay as they are.

---

## Part 1: Per-game entries

Format for each: **core loop**, **what makes it light**, **what makes it fun**, **community complaints (with evidence)**, **licence and what we could borrow**.

### 1.1 Dungeon World (LaTorra & Koebel, 2012)

**Core loop.** The conversation runs until someone's action triggers a *move*. The player rolls 2d6 + stat: 10+ they get what they wanted, 7–9 they get it with a cost or a choice, 6− the GM makes a move *and the player marks XP*. The GM never rolls. Players roll the monster's damage die when they get hurt.

- **Basic moves (paraphrased):** *Hack & Slash* (melee: 10+ you deal your damage and avoid the counter, or you can deal extra damage and expose yourself; 7–9 you deal damage and the enemy hits you too). *Volley* (ranged: on 7–9 choose a cost, such as moving into danger, a weaker shot, or using up ammo). *Defy Danger* (act despite a threat, with the stat depending on *how* you do it; 7–9 means a worse outcome, a hard bargain or an ugly choice). *Defend*, *Spout Lore*, *Discern Realities* (ask questions from a list), *Parley* (needs leverage; on 7–9 they want a concrete assurance first), *Aid/Interfere* (via Bonds).
- **Chassis:** six D&D stats (3–18 turned into −3…+3). Classes set HP (base + CON score) and a **damage die** (wizard d4 up to fighter/paladin d10). **Armour** subtracts a flat 1–2 (+1 for a shield). Monsters have HP (around 3 for hordes, 6 for groups, 12 for solitary), a damage die and armour, plus "monster moves" and instincts.
- **Magic:** the Wizard prepares spells Vancian-style from a spellbook (level +1 worth of spell levels) and rolls INT to cast. On a 7–9 they choose a drawback: draw attention, take −1 ongoing, or forget the spell. The Cleric is granted spells by communing and has a parallel drawback list (lose favour, spell revoked).
- **Identity:** race (one move), alignment (one XP-earning behaviour), Bonds (sentences about other PCs; resolving one earns XP).
- **Advancement:** XP from misses, alignment, resolved bonds and the end-of-session questions (learned something important about the world? beat a notable foe? looted memorable treasure?). A level costs current level + 7 XP. Each level gives one new class move and +1 to a stat.
- **GM side:** agenda, principles, a list of GM moves (reveal an unwelcome truth, show signs of a threat, deal damage, use up resources, separate them, put someone in a spot, offer an opportunity at a cost…), and **Fronts** (dangers with grim portents counting down to an impending doom).

**What makes it light.** One roll, three outcomes, no GM dice, no initiative, and classes on one double-sided sheet. The GM-move list turns "what happens on a miss" into a menu.

**What makes it fun.** A D&D-literate player can sit down in five minutes. Misses drive the story (and pay XP). Fronts give the GM a living world. HP and damage let a fighter feel like a fighter.

**Community complaints (evidence).**
- **Defy Danger is a vague catch-all.** DW2's own designers said its 7–9 is too ambiguous to give the GM anything to work with, its trigger lets people roll when nothing is at stake or when danger acts *on* them rather than them acting, and it trips inexperienced GMs ([DW2: Stats, Conditions and Defying Danger](https://www.dungeon-world.com/stats-conditions-and-defying-danger-in-dungeon-world-2/)).
- **HP and damage are "accounting".** Hack & Slash, Volley, Defend, Cure Light Wounds and similar moves mostly shift a number without changing the scene, so only the *last* HP matters dramatically ([DW2: The Problem with Hit Points](https://www.dungeon-world.com/the-problem-with-hit-points/)). Volley in particular can succeed with nothing happening ([DW2: Think Dangerously](https://www.dungeon-world.com/think-dangerously-fighting-in-dungeon-world-2/)).
- **Monotony and no difficulty scaling.** Mythcreants' critique: fights become repeated Hack & Slash rolls, and since task difficulty doesn't move the odds, escaping a small landslide is exactly as hard as outrunning an avalanche. It also objects to the jargon ("+1 forward", "hold", "ongoing"), the arbitrary race/alignment restrictions, and rules that are both intrusive and vague ([Mythcreants](https://mythcreants.com/blog/dungeon-world-is-a-game-to-skip/)).
- **Fiction-first and GM moves confuse new GMs.** Recurring "am I running it wrong?" threads ([RPGnet](https://forum.rpg.net/threads/im-running-dungeon-world-pbta-wrong-please-help-me-run-it-right.854513/), [EN World](https://www.enworld.org/threads/reading-through-dungeon-world-questions-for-gms-re-initiating-a-gm-move.556764/)).
- **Too D&D and too dated.** Helena Real (DW2 co-designer): the original feels out of step with modern PbtA and unfocused, "like how D&D feels" ([Rascal](https://www.rascal.news/helena-real-speaks-candidly-about-dungeon-world-2/)). Spencer Moore wrote Chasing Adventure to fix three gripes: magic poorly executed, a few bad rolls spiralling, and the game trying too hard to be D&D in a different medium ([Troy Press](https://troypress.com/chasing-adventure-a-fantasy-pbta-without-the-ddisms/)).
- **Playbook bloat.** The Commons now holds roughly 400 third-party playbooks and 165 compendium classes ([Troy Press: PbtA Commons](https://troypress.com/the-pbta-commons/)). It shows how fertile the format is, and also that each class is a full design job.
- **Balance holes** (the paladin's immunity quest was the famous one; Mythcreants).

**Licence.** Text under **CC BY 3.0 Unported**, © Sage LaTorra and Adam Koebel ([repo](https://github.com/Sagelt/Dungeon-World), [Wikipedia](https://en.wikipedia.org/wiki/Dungeon_World)). Reuse of text would need a notice along the lines of *"Contains material from Dungeon World by Sage LaTorra and Adam Koebel, licensed under CC BY 3.0 (link), modified"*. **Borrow:** concepts (three-tier moves, GM-move menu, Fronts, player-rolled monster damage, XP-on-miss, end-of-session questions). Paraphrase, don't paste.

### 1.2 Dungeon World 2 (Moore & Real; publishers Crane & Dimatos; beta Sept 2026)

The most directly relevant case study, because it is running our design question live.

- **Blue alpha (July 2025):** conditions instead of HP, no damage dice, evocative stat adjectives, and "Resistance/Defiance" points spent to say no to a consequence instead of rolling Defy Danger.
- **Red alpha (Sept 2025):** six classic stats, HP and rolled damage dice back ([Alpha Testing and Looking Ahead](https://www.dungeon-world.com/alpha-testing-and-looking-ahead/)).
- **What they learned** ([Calibrating DW2](https://www.dungeon-world.com/calibrating-dungeon-world-2/)): feedback split about evenly between a "D&D side" and a "PbtA side". The feel of D&D depends more on familiar language and terms than on specific mechanics. Blue had too many moves. Defiance was counterintuitive. Players want loot as a reward. Red's desperate combat was engaging but needed more player tools. There have to be accessible on-ramps for new players.
- **Combat redesign** ([Think Dangerously](https://www.dungeon-world.com/think-dangerously-fighting-in-dungeon-world-2/)): melee and ranged merged into one Fight move. A hit lets you *choose effects from a short list* (avoid retaliation, wear the enemy down, take something, inflict a condition, deal heavy harm), and the rule is that "something in the fiction should always change". A **hurt enemy escalates** with a tailored dramatic response (the idea comes from *Masks*).
- **Beta (Sept 2026):** HP and damage dice kept *for accessibility to D&D players*, the familiar stats kept (CON dropped, then restored per [Year One](https://www.dungeon-world.com/dungeon-world-2-year-one/)), plus Conditions, Struggles and Bonds ([Welcome to Beta](https://www.dungeon-world.com/welcome-to-beta/)).

**Licence.** The designers say DW2 will stay Creative-Commons compatible ([Troy Press summary](https://troypress.com/dungeon-world-2/)). The beta's licence is *unverified*, so treat it as concepts only until the final text states one.

**For us:** this is almost a replay of our D26 ("no HP for now") debate, run with hundreds of playtesters, and it came down on the side of HP plus fiction-changing hit effects.

### 1.3 World of Dungeons (John Harper, 2012, "1979 edition")

A two-page thought experiment: what would DW have been in 1979? Basically one universal 2d6 risk roll (Defy Danger as the whole game), attributes, a few skills, classes as a couple of abilities, and HP. It was a Kickstarter stretch goal, **CC BY like DW** according to the designer ([itch](https://johnharper.itch.io/world-of-dungeons); exact version *unverified*). **Lesson:** a D&D chassis on 2d6 fits on two pages, which supports the audit's "Lean Facets on two pages" test. The cost is a single catch-all roll, the same Defy Danger problem at full scale.

### 1.4 Homebrew World (Jeremy Strandberg)

**Core loop:** DW, trimmed for one-shots and short campaigns.
**Changes** ([Spouting Lore](https://spoutinglore.blogspot.com/2018/07/homebrew-world.html)): advantage/disadvantage (an extra die, drop lowest/highest) replaces ±1s. Parley becomes partly an information move and works on PCs. Supplies are condensed into one resource. Only three debilities, each covering two stats and easier to clear. XP on a miss or at Make Camp, with 5 XP per advance. No big 3–18 scores, just modifiers. **HP is a fixed number per class.** Backgrounds and Drives replace race and alignment. Bonds removed.
**Why it matters:** it's the best-regarded "DW minus the D&D friction" and matches our Lean sketch closely. The ±1 → extra-die change is *already* our Spark.
**Licence:** **CC BY-SA 3.0 US** ([PDF notice](https://i.4pcdn.org/tg/1656401386330.pdf)). SA 3.0 is **not** GPL-compatible, so concepts only.

### 1.5 Freebooters on the Frontier (Jason Lutes; 2e in playtest)

**Core loop:** DW moves wrapped around OSR procedure. Random character generation (funnel of 2–3 villagers each in 2e), hexcrawl and wilderness tables, and a retirement goal of treasure.
**Light / fun:** four classes (Fighter, Thief, Cleric, Magic-User, with more in playtest), each with **its own resource** (Mettle, Cunning, Favor, Power). A **Luck** stat. Attributes have current and max values that wear down. Weapon damage by type. Saving throws by attribute ([Troy Press](https://troypress.com/freebooters-on-the-frontier-2e-is-the-osr-pbta-homage-to-odd/)). The procedures (in the companion *Perilous Wilds*) are its lasting contribution: MM-side variety.
**Complaints:** tracking current attribute scores to recompute modifiers is tedious (Troy Press), and the "frontier" framing has been criticised.
**Licence:** 1e **CC BY-SA 3.0**, building on DW's CC BY 3.0 ([attribution record](https://github.com/stevesea/Adventuresmith/blob/master/content_attribution.md)). Not GPL-compatible text, so concepts only. 2e licence *unverified*.
**Lesson:** *attribute attrition as damage costs arithmetic*. Avoid it.

### 1.6 Stonetop (Jeremy Strandberg & Jason Lutes)

**Core loop:** DW rebuilt around a home village that is effectively a shared character. Expeditions out, homefront scenes back. Three move families (basic, expedition, homestead) ([Indie Game Reading Club](https://indiegamereadingclub.com/indie-game-reading-club/deep-dive-stonetop/)).
**Fun:** setting-specific playbooks, **arcana** (magic items with to-do lists that unlock over play, a long-term motivation engine), followers, and harm richer than HP (conditions, injuries needing treatment, disarms: "trade harm" covers more than numbers).
**Complaints:** scale. Around 1,200 pages ([Rascal](https://www.rascal.news/from-blog-posts-to-mighty-1-200-page-books-stonetops-creators-reflect-on-a-decade-long-journey/)), a ten-session campaign can't see most of it, and the homefront/expedition balance is left to the GM.
**Licence:** **CC BY-SA 4.0**, one-way compatible with GPLv3. **Borrow (concept):** magic items as quests with checklists, which fits "loot as MM variety" and the app well.

### 1.7 Chasing Adventure (Spencer Moore)

**Core loop:** DW with the D&D-isms removed. No ability scores, no HP, no encumbrance or gold or race or alignment. Uses advantage/disadvantage ([Troy Press](https://troypress.com/chasing-adventure-a-fantasy-pbta-without-the-ddisms/), [comparison table](https://troypress.com/table-comparing-dungeon-world-to-5-hacks/)).
**Mechanics** ([Deathtrap review](https://deathtrap-games.blogspot.com/2025/06/game-review-chasing-adventure.html)): harm puts a *condition on a stat* (disadvantage on it); when all are conditioned the character crumbles and chooses injury, a class change or death. Armour is a *spendable* resource that returns after rest and maintenance. Magic always carries a cost on 7–9, and misses can go wild. "Ominous Forces" are threat timers.
**Complaints:** weapon tags have little mechanical meaning; needs more monster examples.
**Licence:** now part of the PbtA Commons under a CC licence (version *unverified*).
**Lesson:** the pure-conditions route exists and is liked. But DW2, which Moore co-designs, still ended up re-adding HP for its broader audience. That is strong evidence for which way the mass market leans.

### 1.8 Ironsworn / Starforged (Shawn Tomkin)

**Core loop:** roll an action die (d6 + stat) against two challenge dice (d10s). Beat both for a strong hit, one for a weak hit, neither for a miss. Doubles amplify the result. **Momentum** builds up and can be burned to replace your action die. **Progress tracks** (vows, journeys, fights) fill in ticks and resolve with a progress roll that can't use momentum. Oracles replace the GM ([Gnome Stew](https://gnomestew.com/ironsworn-review/), [SRD](https://tedtschopp.github.io/Ironsworn-SRD/Ironsworn%20SRD.html)).
**Fun:** solo/co-op play. XP comes from fulfilling vows, so the reward loop points at the story.
**Complaints:** the tick-within-box progress notation confuses at first, progression feels stingy, and safety guidance is thin (Gnome Stew and others).
**Licence:** SRD, moves, oracles and assets under **CC BY 4.0**; the full books under CC BY-NC-SA 4.0 ([Tomkin Press](https://tomkinpress.com/pages/licensing)). Required notice for commercial or open use: *"This work is based on [titles], created by Shawn Tomkin, and licensed for our use under the Creative Commons Attribution 4.0 International License"* plus the licence URL.
**Borrow:** progress tracks (our Threat Clocks already sit close), oracles as app features, momentum as a concept. Oracle *table text* could legally be reused under CC BY 4.0, but writing our own is better.

### 1.9 Worlds Without Number (Kevin Crawford)

**Core loop:** OSR/B/X-shaped. d20 attack vs AC, **2d6 skill checks**, saves. **Shock** means melee does minimum damage even on a miss against lightly armoured foes. Three classes (Warrior, Expert, Mage) plus **half-classes** to mix, and Foci as feat-like picks. Mages have Arts (from an Effort pool) and Spells (slots). **Huge GM toolset:** tags for ruins, courts, communities and wilderness, and faction turns ([Eldritch Exarch review](https://eldritchexarchpress.substack.com/p/a-reviewcritique-of-worlds-without)).
**Complaints:** information is scattered across the book, and the mages depend heavily on GM interpretation.
**Licence:** the WWN **SRD is CC0** ([DriveThru SRD](https://www.drivethrurpg.com/en/product/473939/worlds-without-number-system-reference-document); [Tenkar](https://www.tenkarstavern.com/2024/11/free-osr-worlds-without-number-core.html)). No attribution is legally required; just don't present derived work as official. **The most borrowable text in this survey.** The free edition of the full book is free to download but is *not* itself open.
**Borrow:** tag-based world generation and faction turns (MM variety), Shock as a damage floor (it prevents armour stalemates), and half-classes as the model for "one ability from another Facet".

### 1.10 13th Age (Heinsoo & Tweet; 2e shipped Dec 2025)

**Core loop:** d20 D&D descendant tuned for story. **Escalation die:** a visible die starting at +1 in round two and rising each round to +6, added to PC attacks, with class abilities keyed to it. **Backgrounds instead of skills:** 8 points spread over freeform backgrounds, max 5 in any one. A check is d20 + stat + level + the *single* best-fitting background ([Archmage Engine SRD](https://pelgranepress.com/media/SRD/13thAgeArchmageEngineSRD.pdf)). **Icon relationships:** points in relationships with the setting's great powers, rolled as d6s at session start (6 = a benefit, 5 = a benefit with complications). **One Unique Thing:** a sentence with no mechanics that changes the setting. **Incremental advance:** one piece of the next level after each session. **Talents:** each class picks three from a class list, and that pick defines its build.
**Fun:** character creation produces story hooks. The escalation die ends fights and discourages opening with your best ability ([EN World pros/cons](https://www.enworld.org/threads/13th-age-pros-and-cons.352410/), [Scroll for Initiative](https://scrollforinitiative.com/2023/03/11/13th-age-the-best-rpg-ive-never-played-review/), [Sly Flourish on porting the escalation die](https://slyflourish.com/escalation.html)).
**Complaints:** combats still run 2+ hours for some groups despite the pitch. Magic items feel thin to 3.5e veterans. Freeform rituals need GM improvisation. Worry about one catch-all background (the SRD's answer: max 5 points, one background per check, GM picks the stat).
**Licence:** Archmage Engine SRD under **OGL 1.0a** (© Fire Opal Media), with a separate compatibility licence and community-use policy ([Pelgrane](https://pelgranepress.com/2014/02/19/13th-age-archmage-engine-licensing-overview/)). OGL is not GPL-compatible, so **concepts only**.
**Borrow:** escalation die (app-tracked, zero player load), backgrounds-as-skills with the one-per-check cap, incremental advance, "pick three talents" as the class-build pattern, and icon rolls as a session-start hook generator.

### 1.11 Daggerheart (Darrington Press, 2025)

**Core loop:** roll 2d12, one Hope and one Fear, add them plus a trait and compare to a difficulty. The higher die decides *who gets a token*: Hope (player resource) or Fear (GM resource). Doubles are a critical. Classes are each built from **two of nine domains**, with domain *cards* as abilities ([Wikipedia](https://en.wikipedia.org/wiki/Daggerheart)). The GM does roll for adversaries.
**Probabilities (mine):** Hope and Fear each win 45.8% of rolls, crit 8.3%. At +1 vs 12: success with Hope 32%, success with Fear 32%, failure with Hope 14%, failure with Fear 14%, crit 8%. That's a **five-way outcome** that players read at a glance.
**Fun / complaints:** Fear is praised for giving the GM a transparent budget for bad things, which calms "the GM is out to get us" worries ([Drolleries](https://drolleries.substack.com/p/how-to-use-fear-in-daggerheart-and)). The criticism is the economy: players only gain Hope when the Hope die is higher, so every roll risks feeding the GM ([solo review](https://solottrpg.substack.com/p/daggerheart-my-thoughts-and-ramblings)).
**Licence:** **DPCGL.** A royalty-free licence for *Daggerheart-compatible* content with a set attribution line and logo ([license](https://darringtonpress.com/license/), [FAQ](https://www.daggerheart.com/faq/)). It is a compatibility licence, not an open one: no standalone-system provision and no relicensing. **Concepts only.**
**Borrow (concept):** a visible, earned MM-side budget. This is the mirror image of our Sparks economy, and with Borrowed Trouble we already have a version. Also *class = two domains*, which is a useful Facet→class pattern (Part 5).

### 1.12 Draw Steel (MCDM, 2025)

**Core loop:** the **power roll** is 2d10 + characteristic into three tiers: ≤11, 12–16, 17+. Abilities mostly *always do something*, with the tier scaling the effect. Heroic resources build during a fight. Tactical grid combat. Monsters also roll.
**Probabilities (mine):** at +2, tier 3 21%, tier 2 43%, tier 1 36%. It's flatter than 2d6 and tolerates bonuses up to about +5.
**Complaints:** fights run D&D-length. One actual-play level-1 fight of 5 PCs against 10 foes took close to two hours ([Dice Society review](https://thedicesociety.com/draw-steel-review/)).
**Licence:** **Draw Steel Creator License.** Proprietary and revocable, requires an independence disclaimer, and covers only the listed documents ([MCDM](https://www.mcdmproductions.com/draw-steel-creator-license)). **Concepts only.**
**Lesson:** "every roll does something, tiered" is the right *feel*. Draw Steel's weight comes from the tactical layer, not from its dice.

### 1.13 Blades in the Dark / Forged in the Dark (contrast only)

A d6 pool: take the highest, 6 = full success, 4–5 = partial, 1–3 = bad, two 6s = critical. Position and effect are set before the roll, and stress buys resistance. It's the best "set the stakes before rolling" procedure in the hobby, but it is heist-shaped, not D&D-shaped. **Licence:** SRD **CC BY 3.0 Unported.** Notice text: *"This work is based on Blades in the Dark (bladesinthedark.com), product of One Seven Design, developed and authored by John Harper, and licensed for our use under the Creative Commons Attribution 3.0 Unported license"* ([Blades licensing](https://bladesinthedark.com/licensing)).

### 1.14 The Black Hack (David Black; OSR, player-facing)

**Core loop:** d20 **roll under** stat to succeed. PCs roll to hit, and **monsters never roll**: to avoid a blow you roll under STR (melee) or DEX (ranged). **For every HD a monster has above your level, your rolls against it get worse by 1.** Monster damage is set by HD (from a d4 at 1 HD, rising steeply; a fixed average is also given). The **usage die** (d20→d12→…→d4, stepping down on a 1–2) replaces ammo and supply counting ([Black Hack English SRD](https://the-black-hack.jehaisleprintemps.net/english/)).
**Complaints:** the text is vague; monsters hit weakly next to PCs (a 1-HD monster does d4); weapon choice barely matters because damage is by class; first-level casters are thin ([dieheart](https://www.dieheart.net/the-black-hack/)).
**Licence:** **OGL** (1e), so concepts only.
**Borrow:** *monster level as a penalty to the player's roll* is the cleanest known way to show threat without enemy dice. The usage die (an app can hide it entirely). Note that `RESEARCH_lean_nsr.md` covers Cairn and Knave's roll-under saves.

### 1.15 Cypher System / Numenera (Monte Cook Games)

**Core loop:** the GM sets a task level 1–10 and the target is level × 3 on a d20. Players spend **Effort** from their Might, Speed or Intellect pools to lower the level. Pools are also your HP. **All rolls are player-facing:** defence against a level-4 attacker is a Speed defence roll against 12. **GM intrusions:** the GM offers a complication and pays XP for it, and the player can refuse by spending XP. Character = the sentence **"I am an [adjective] [noun] who [verbs]"** (descriptor, type, focus).
**Complaints** ([Deathtrap Numenera review](https://deathtrap-games.blogspot.com/2022/06/game-review-numenera-original-edition.html), [Nerdist on intrusions](https://nerdist.com/article/why-numeneras-gm-intrusions-are-the-best-worst-thing-for-your-rpg-character/)): announcing intrusions breaks immersion for traditional players, and some players refuse to engage with them. Light weapons against armour grind into stalemate. Recovery is too fast. Easy treasure removes economic pressure. Player intrusions were later added because players asked why only the GM got them.
**Licence:** **Cypher System Open License (CSOL).** Allows standalone Cypher-powered games, but requires a "Compatible with the Cypher System" cover logo and an independence notice, bans some content categories, and terminates on breach ([CSOL](https://www.montecookgames.com/cypher-system-open-license/), [CSRD licence page](https://cyphersrd.quest/100-license/)). Those extra restrictions make it **not GPL-compatible**, so concepts only.
**Borrow:** the character sentence (Part 5), and the level-sets-the-target-number idea for defence rolls.

### 1.16 Others referenced for Part 5 (class-building)

- **Troika!** (Daniel Sell): randomly rolled **backgrounds** are the whole character (skills, possessions, a special ability), mostly odd and setting-flavoured. Published under a free compatibility licence ([Wikipedia](https://en.wikipedia.org/wiki/Troika!_(role-playing_game))). Concepts only.
- **ICRPG** (Runehammer): light d20 against one room target, **Effort dice** for damage and progress, and **advancement mostly through loot**. Runehammer's third-party licence terms are *unverified*, so concepts only ([Deathtrap](https://deathtrap-games.blogspot.com/2021/12/game-review-index-card-rpg-master.html)).
- **GURPS templates / Savage Worlds archetypes:** pre-spent point packages sitting on top of a point-buy system. SJG's online policy and Pinnacle's fan licence both forbid reproducing rules text ([SJG](https://www.sjgames.com/general/online_policy.html), [Pinnacle](https://peginc.com/licensing/)). Concepts only.
- **Morrowind** (the owner's model): specialization (Combat/Magic/Stealth) adds a bonus to its nine skills and speeds their growth. A class = 2 favoured attributes + 5 major + 5 minor skills, and a custom class is built from those same parts. **Only major and minor skill increases count toward levelling** ([UESP](https://en.uesp.net/wiki/Morrowind:Classes)). That last rule is the famous exploit: players choose rarely used majors, or grind particular skills, to control level-ups and attribute multipliers.

---

## Part 2: Resolution-core comparison

### 2.1 Probability tables (computed)

**2d6 + mod, 10+ / 7–9 / 6−** (current Facets). *Spark* = 3d6 keep best 2. *Trouble* = 3d6 keep worst 2.

| Mod | Plain full / partial / miss | With Spark | With disadvantage |
|---|---|---|---|
| −1 | 8 / 33 / 58 | 20 / 48 / 32 | 2 / 18 / 81 |
| 0 | 17 / 42 / 42 | 36 / 45 / 19 | 5 / 27 / 68 |
| +1 | 28 / 44 / 28 | 52 / 37 / 11 | 11 / 37 / 52 |
| +2 | 42 / 42 / 17 | 68 / 27 / 5 | 19 / 45 / 36 |
| +3 | 58 / 33 / 8 | 81 / 18 / 2 | 32 / 48 / 20 |

The biggest effect of +1 is ~14 points on "at least a partial" around the middle of the curve. Above +3 there's almost nothing left to gain, **so flat bonuses must be capped around +3.**

**2d10 + mod, 17+ / 12–16 / ≤11** (Draw Steel):

| Mod | T3 / T2 / T1 |
|---|---|
| 0 | 10 / 35 / 55 |
| +1 | 15 / 40 / 45 |
| +2 | 21 / 43 / 36 |
| +3 | 28 / 44 / 28 |
(+3 on 2d10 ≈ +1 on 2d6, so the scale takes about 2.5× the bonus range.)

**d20 + mod vs DC, with a partial band of "missed by 1–4"**:

| DC / mod | full / partial / miss |
|---|---|
| 12 / +0 | 45 / 25 / 30 |
| 12 / +2 | 55 / 25 / 20 |
| 12 / +5 | 70 / 25 / 5 |
| 15 / +2 | 40 / 25 / 35 |
The partial band stays a flat 25% until the miss chance runs out. Skill shifts misses into full successes but never changes how often you *partially* succeed.

**d20 roll-under stat** (Black Hack: strictly under; Cairn: equal or under): stat 10 → 45% / 50%, 12 → 55 / 60, 14 → 65 / 70, 16 → 75 / 80. Two tiers only, unless you bolt on a band.

**d6 pool, take highest** (Blades): 1 die 17 / 33 / 50; 2 dice 31 / 44 / 25; 3 dice 42 / 45 / 12; 0 dice (roll 2, keep lowest) 3 / 22 / 75.

**2d12 Hope/Fear** (Daggerheart): see 1.11. The success line alone (sum + mod ≥ 12) is 62% at +0 and 75% at +2.

### 2.2 Comparison

| Core | D&D familiarity | Probability feel | Partial success | HP / damage fit | Player-only attack rolls | Bonus range tolerated |
|---|---|---|---|---|---|---|
| **d20 roll-high vs DC** | Highest: everyone knows it | Flat and swingy; a +1 is always 5% | Has to be bolted on (flat 25% band) | Native: to-hit then a damage die | Awkward. Needs a *defence* roll against the monster's attack bonus (a 5e variant rule), which means two numbers to reconcile | Wide (+10 fine) |
| **d20 roll-under stat** (Black Hack, Cairn) | Medium: the stat *is* the target, but "under" confuses d20 veterans | Flat | Poor (two tiers) | Good with auto-hit (Cairn) or a monster-HD penalty | **Best**: "roll under DEX to dodge" with no second number | Stat-bounded |
| **2d6 three-tier** (PbtA, Facets now) | Medium: PbtA players know it; D&D players learn it in one sentence | Bell curve; most results in the middle | **Native.** 7–9 is the most common result | Good (DW proved it); damage is a separate die | Good: player rolls, 7–9 means you trade blows, 6− gives the MM a move | **Narrow (≤ +3)** |
| **2d10 three-tier** (Draw Steel) | Medium | Gentler bell | Native | Good (tiers scale damage) | Designed with GM rolls; would need adapting | Medium (~+5) |
| **2d12 duality** (Daggerheart) | Medium-high (it's "roll high vs DC") | Near-triangular | Native plus a Hope/Fear axis | Good | GM rolls in RAW | Medium |
| **d6 pool** (Blades) | Low | Pool size is the lever | Native | Weak (no HP culture) | Native | Pool ≤ 4–5 dice |

### 2.3 Recommendation

**Stay on 2d6, three tiers.** Reasons, in order:
1. It's the only core where the partial (the result that creates story) is the *most likely* outcome at typical bonuses. That's the whole point of the audit's "rulings over rules" shift.
2. The lineage converged on 2d6 with **an advantage die instead of +1s**, and our Spark *is* that die (with Borrowed Trouble as the matching disadvantage), so the table economy keeps working unchanged.
3. It handles HP and damage fine (DW, Freebooters and the DW2 beta all do it), and player-only rolling is native.
4. d20 would buy familiarity, but it costs the native partial and tolerates bonus inflation, and bonus inflation is exactly the complexity creep we're trying to escape.

**Design constraints that come with it:** (a) the total flat modifier is capped at +3, and "better" means Spark or advantage, not +N. (b) Growth comes from options, HP and loot, not from the number on the roll. (c) Difficulty scaling (DW's landslide/avalanche gap) comes from the **advantage/disadvantage die and a ±1 step**, and for threat from **monster level** (Black Hack's pattern). (d) Keep the naturals as they are.

---

## Part 3: Player-facing-only rolling. How threat is expressed, and what goes wrong

| Game | How enemy threat reaches the dice | What goes wrong |
|---|---|---|
| **Dungeon World** | GM moves on a player's 6− or 7–9 trade. The **player rolls the monster's damage die**. Armour subtracts. Monster moves and instincts give flavour | Threat depends on how well the GM uses moves (new GMs struggle). Damage is accounting. Trading blows spirals for weak characters (see 3.1) |
| **Black Hack** | Player rolls under STR/DEX to avoid damage. **Monster HD above your level makes your rolls worse.** Damage by HD | Monsters too weak next to PCs. The text is vague |
| **Cypher / Numenera** | **Defence roll against level × 3.** GM intrusions pay XP for complications | Variance piles onto one player. Intrusions read as "gotcha" to some tables. Armour stalemates |
| **Ironsworn** | Enemy rank sets how much progress each hit makes. Misses and weak hits trigger "pay the price" or damage moves | Solo-shaped; a fight is a progress track, not HP |
| **DW2 (beta)** | Hurt enemies **escalate** (a tailored response once damaged). Conditions and HP both apply | New; not yet road-tested at scale |
| **Facets now** | The MM declares the incoming Condition tier by enemy type, the PC reacts | Flagged in `dice_system_analysis.md`: a Boss lands the same tier every time, an exchange can pass with zero dice, and variance piles onto one player |

### 3.1 The "trade blows" calibration (simulated, 40k fights each)

A lean attack using the Lean-sketch rule: 10+ deal damage; 7–9 deal *and take*; 6− take (tested with the miss hurting 100% and 50% of the time):

| Matchup | Rolls to win | Damage taken | PC dropped |
|---|---|---|---|
| Fighter +2, d10, HP 12, armour 1 vs goblin (HP 3, d6, armour 1) | 1.6 | 2.1–2.4 | 0–1% |
| same vs orc (HP 6, d8, armour 1) | 2.2 | 3.8–4.3 | 6–9% |
| same vs ogre (HP 12, d10, armour 2) | 3.7–4.0 | 8–8.7 | 40–48% |
| **Wizard +0, d4, HP 5 vs goblin** | 1.9–2.3 | 4.1–4.3 | **71–78%** |

At +1, about 72% of your attacks also get you hit. That's fine for a fighter and fatal for a caster. **Implications:** fragile Facets need a way to act that isn't melee (spells as ranged "Volley"-style moves whose 7–9 is a *cost*, not a counter-blow). Monster damage should be small and fixed (or a small die the player rolls). Armour should be 1–2 at most. A damage floor (WWN's Shock idea) prevents stalemates.

**Synthesis.** The rules that work are (1) the *player's own roll* gates whether the blow lands, which is Apocalypse World's economy and fixes our "Boss always lands Tier 2", (2) **monster level shifts the roll** instead of the MM rolling, (3) the monster's **one gimmick** plus an **escalation when hurt** keep NPCs from feeling inert, and (4) the MM's complications go through a visible, bounded budget (Daggerheart's Fear, Numenera's paid intrusions, our Borrowed Trouble), so they don't feel arbitrary.

---

## Part 4: Licence table

"GPLv3 text?" asks whether the *rules text itself* could be copied into our GPLv3 books. Compatibility for CC BY 4.0, CC BY-SA 4.0 and CC0 is from the [FSF licence list](https://www.gnu.org/licenses/license-list.html) and [Creative Commons](https://creativecommons.org/share-your-work/licensing-considerations/compatible-licenses/). CC BY-SA 4.0 is one-way, into *GPLv3 only* (not "or later"). CC BY 3.0 isn't on the FSF list.

| Game | Licence | Share-alike? | GPLv3 text? | Attribution if text reused |
|---|---|---|---|---|
| Dungeon World | CC BY 3.0 Unported | No | Probably usable (permissive), **not formally listed**; keep reused text in a separately noticed file | "Dungeon World © Sage LaTorra & Adam Koebel, CC BY 3.0", link, note changes |
| World of Dungeons | CC BY (version unverified) | No | As DW | John Harper |
| Homebrew World | CC BY-SA 3.0 US | Yes | **No** | Jeremy Strandberg |
| Freebooters (1e) | CC BY-SA 3.0 | Yes | **No** | Jason Lutes, plus DW credit |
| Stonetop | CC BY-SA 4.0 | Yes | **Yes, one-way** (GPLv3-only) | Jeremy Strandberg & Jason Lutes |
| Chasing Adventure | CC (PbtA Commons; version unverified) | ? | Check | Spencer Moore |
| Ironsworn/Starforged SRD | CC BY 4.0 (full books BY-NC-SA) | No (SRD) | **Yes** (SRD only; NC books no) | "This work is based on …, created by Shawn Tomkin, … CC BY 4.0" |
| Worlds Without Number SRD | **CC0** | No | **Yes** | None required; don't claim it's official |
| Knave 1e | CC BY 4.0 | No | **Yes** | Ben Milton |
| Cairn | CC BY-SA 4.0 | Yes | Yes, one-way | Yochai Gal |
| Blades / FitD SRD | CC BY 3.0 Unported | No | As DW | One Seven Design / John Harper (set text above) |
| 13th Age Archmage Engine | OGL 1.0a | OGL terms | **No** | OGL §15 notice |
| The Black Hack | OGL 1.0a | OGL terms | **No** | OGL §15 |
| Daggerheart | DPCGL | n/a (compatibility licence) | **No** | Set attribution line and logo |
| Draw Steel | Creator License (revocable) | n/a | **No** | Independence disclaimer |
| Cypher / Numenera | CSOL | n/a | **No** (extra restrictions) | Compatibility logo and notice |
| Troika!, ICRPG, Savage Worlds, GURPS | Bespoke or fan policies | n/a | **No** | n/a (concepts only) |
| Apocalypse World (PbtA root) | All rights reserved; "hack it" permission culture | n/a | **No** | Concepts only |

**Practical rule:** paraphrase everything, copy no text, and keep a `ATTRIBUTIONS.md`-style credit page naming the games whose *ideas* we used (the hobby expects this, even where no licence requires it).

---

## Part 5: Implications for a lean Facets of Origin

Opinionated. It builds on the audit's §7 "Lean Facets" sketch and includes the owner's constraints: **the three Facets remain as parents of classes, and classes are not fixed. The model is Morrowind: a Facet is like a specialization, players can define their own class inside it, and preset classes are suggested builds.**

### 5.1 Which chassis to take concepts from

| Need | Take the concept from | Why |
|---|---|---|
| Engine and dice | **Homebrew World / DW** (what we already have) | Tested for a decade on exactly this brief; our Spark is their advantage die |
| Combat that changes the fiction | **DW2's Fight move + escalations** | Their fix for "HP is accounting": every hit also picks an effect; hurt enemies escalate |
| Threat without enemy dice | **Black Hack** (level shifts the player's roll), **DW** (player rolls the monster's damage) | The simplest ways known |
| Pacing fights | **13th Age escalation die** | App-tracked; shortens fights with no new player rules |
| Skills | **13th Age backgrounds** (one applies, capped) | Freeform, story-first, tested |
| Advancement | **13th Age incremental advance + DW end-of-session questions** | The reward loop points at discovery and goals; the app handles increments |
| MM variety | **WWN tags and factions** (CC0!), **Freebooters/Perilous Wilds procedures**, **Stonetop arcana** | Old-school depth on the MM side |
| MM consequence budget | **Daggerheart Fear** (concept) → our Borrowed Trouble | A visible budget calms "the MM is out to get us" |

### 5.2 Pitfalls to design around (each with the evidence behind it)

1. **No catch-all move.** Give each basic action a clear trigger and a concrete 7–9 menu (DW2's Defy Danger diagnosis). "When something happens *to* you" should be the rare defence roll, not a way to call for rolls without stakes.
2. **No jargon.** No "forward/ongoing/hold". Say "+1 on your next roll" (Mythcreants). Use D&D words where they fit: HP, damage, armour, level, spell (DW2: "the feel is the vocabulary").
3. **Difficulty must scale.** A disadvantage die for a harder task and a level gap for a stronger foe, so the avalanche really is harder than the landslide.
4. **Every hit changes the fiction.** On a 10+ hit, pick one: extra damage, push or disarm, protect someone, create an opening. That way even a hit that doesn't kill moves the scene.
5. **Trading blows needs guards:** small fixed monster damage, armour ≤ 2, non-melee magic for fragile Facets, and a Shock-style floor so armour never creates a stalemate.
6. **Don't let misses spiral** (Chasing Adventure's diagnosis). Keep the Graceful Fail and Spark-on-a-miss style relief. Pay XP on misses sparingly, or not at all (see 5.4).
7. **No per-class resource zoo** (Freebooters' four resources, Draw Steel's heroic resources). Magic keeps *one* limit (a count per rest). Everyone else has none.
8. **Don't track attrition on stats** (Freebooters, Numenera pools). HP is the only number that goes down.
9. **Bound the MM's complications.** They go through a visible budget, not announced "intrusions" (Numenera's immersion complaint).
10. **Content scale.** Each class written in full is expensive (DW's 400 playbooks, Stonetop's 1,200 pages). That's the strongest argument for the menu model in 5.3.

### 5.3 How the chassis fits a Facet → class hierarchy (Morrowind model)

**Principle:** the Facet owns everything balance-critical and long-lived. The class is a **named selection** from the Facet's menu. Preset and custom classes are built the same way, so a custom class can't be more complicated than a preset one.

| Owned by the **Facet** (Body / Mind / Soul) | Owned by the **class** (preset or custom) |
|---|---|
| **Its stat.** The Facet is your favoured stat (+2), like Morrowind's specialization bonus. With stats named Body/Mind/Soul, the parent *is* the stat | **Name and sentence** ("I am a ___ ___ who ___") |
| **HP die** (e.g. Body d10, Soul d8, Mind d6). Set once per Facet so custom builds can't game durability | **Three picks** from the Facet's ability menu (13th Age's "three talents") |
| **The ability menu** (~12 abilities, each a *permission or option*, never a flat +N) | **One background line** (+1 when it applies; one per roll) and a **Specialty** (no roll) |
| **Magic tradition.** Mind = Thaumaturgy, Soul = Invocation, **Body has no magic** (settled canon) | **Starting kit** (weapon damage die, armour 0–2, one signature item) |
| **One Facet move** everyone in the Facet has (Body: soak or push; Mind: know or prepare; Soul: read or sway; exact wording is design work) | **Optional:** one pick from *another* Facet's menu (a Morrowind "minor", a WWN half-class) |
| The **level track** (HP per level, when a new pick arrives) | Nothing numeric beyond the above |

Levelling is the same for every class: each level gives HP, and every other level a new pick from your Facet menu (or a cross-Facet pick), plus a +1 stat at set levels. **Preset classes** (e.g. Body → warrior, scout, brawler; Mind → scholar, artificer, thaumaturge; Soul → speaker, invoker, the luck-touched; the list itself is an owner ruling, and I propose no names as canon) are **saved three-pick bundles with a sentence and a kit**. In the app, "custom class" is just the preset screen with the picks unlocked.

### 5.4 The class-building analogues, and how each would sit under a Facet

| Model | How it builds a class | Under a Facet it becomes | What it teaches about keeping builds simple |
|---|---|---|---|
| **Morrowind** (owner's model) | Specialization + 2 favoured attributes + 5 major + 5 minor skills; custom classes from the same parts | Facet = specialization. Class = favoured stat plus picks. "Minor" = the one cross-Facet pick | **Its failure is use-based levelling** (choose majors you never use to control level-ups). Our current skill *marks* reward using a skill in the same way, which the audit already flagged. **Don't grow characters by use.** Use end-of-session questions |
| **Cypher sentence** ("I am an [adjective] [noun] who [verbs]") | Descriptor (small bonus plus flaw), type (4 archetypes), focus (an ability track) | **Noun = Facet**, **adjective = background**, **verb = class** (the three picks, named). "I am a *stubborn* **Body** who *fights with two blades*" | It gives players a coherent identity in one sentence. The trap is foci: each is a separate multi-tier tree to write and balance. Keep the verb a *label for three menu picks*, not its own tree |
| **13th Age** backgrounds + talents | Class gives a list of talents, pick 3; backgrounds are freeform, 8 points, max 5 each, only the best one applies | **Talents = the Facet menu, pick 3.** Background = one freeform line (+1) | **Caps defeat optimisation:** only one background per roll, a small cap, and the MM rules on relevance. Adopt all three |
| **GURPS templates / Savage Worlds archetypes** | Pre-spent point packages over a point-buy system | *Don't.* A template on top of point-buy hides the complexity without removing it, and custom builds fall back to full point-buy optimisation | **No point-buy.** Custom and preset builds must use the *same small menu* |
| **Troika! backgrounds** | Rolled randomly; one weird background *is* the character | A **d66 "odd classes" table per Facet** for one-shots or quick starts | **Random selection can't be optimised**, and it's pure MM/setting flavour. A good option to offer alongside building |
| **ICRPG** | Light class shell; power comes mainly from **loot** | Facet sets the starting kit; growth comes partly from MM-placed loot and relics | **Put growth in the MM's hands.** The MM controls the power curve, and it's the variety source the owner wants |
| **Daggerheart domains** | Class = two domain decks | Class = your Facet's menu plus *one* other Facet's short list (a "hybrid" preset such as Body+Soul paladin) | Pairing two lists makes a combinatorial variety of classes from a small amount of content |
| **DW playbooks / Stonetop** | Fixed, fully written sheets with starting and advanced moves | A Facet is a **playbook family**: one shared sheet listing the menu, and class presets as highlighted picks | Full per-class sheets are the bloat trap. One sheet per Facet is enough |

### 5.5 Guardrails that keep custom classes simple and hard to over-optimise

1. **One menu per Facet (~12 entries), and every class is "pick three".** No points, no trees, no prerequisites beyond "level N".
2. **Menu entries are options and permissions, not bonuses** (e.g. "you can fight two foes at once", "you may Volley with spells", "once per rest, reroll a miss"). The 2d6 cap (+3 total) makes stacked bonuses pointless anyway.
3. **At most one ability from outside your Facet**, and it costs a level's pick. That's Morrowind's minor skill without the maths.
4. **Durability and magic belong to the Facet, not the class**, so no custom build can take a d10 HP wizard or a Body caster.
5. **Growth is not use-based.** XP comes from the end-of-session questions (discovered, pursued a goal, changed the world), and advances arrive in 13th Age-style increments.
6. **The sentence plus MM sign-off at session zero.** A custom class needs a coherent sentence. The MM can veto a "background: everything" line (13th Age's catch-all worry).
7. **The app builds the class.** Menus, the three-pick limit, the cross-Facet rule and the level track are all enforced in software, so "custom" costs the player no more thought than "preset". Bookkeeping stays in software, as the project's second pillar says.

### 5.6 What this means for the audit's §7 "Lean Facets" sketch

It holds up, with four amendments from this research:
- **Keep HP and damage.** DW2's round trip is the strongest external evidence we have. Pair them with a **10+ effect menu** and **enemy escalations** so hits change the fiction, which answers D26's original concern.
- **Monster threat without enemy rolls = level/HD shifts the player's roll, damage is small and fixed or player-rolled, one gimmick, one escalation, one morale number.**
- **Replace "when something happens to you, roll the stat" with explicit, narrow defence triggers** so it can't become Defy Danger.
- **Class = Facet menu × three picks**, as above, which makes the owner's Morrowind model concrete and cheap to write.

**Next step (unchanged from the audit):** write Lean Facets on two pages with these amendments, and put it and the current game in front of the same humans.

---

## Sources

**Dungeon World / DW2:** [DW repo & licence](https://github.com/Sagelt/Dungeon-World) · [Wikipedia: Dungeon World](https://en.wikipedia.org/wiki/Dungeon_World) · [DW SRD: Gamemastering](https://www.dungeonworldsrd.com/gamemastering/) · [DW2: The Problem with Hit Points](https://www.dungeon-world.com/the-problem-with-hit-points/) · [DW2: Stats, Conditions, and Defying Danger](https://www.dungeon-world.com/stats-conditions-and-defying-danger-in-dungeon-world-2/) · [DW2: Think Dangerously](https://www.dungeon-world.com/think-dangerously-fighting-in-dungeon-world-2/) · [DW2: Alpha Testing and Looking Ahead](https://www.dungeon-world.com/alpha-testing-and-looking-ahead/) · [DW2: Calibrating](https://www.dungeon-world.com/calibrating-dungeon-world-2/) · [DW2: Year One](https://www.dungeon-world.com/dungeon-world-2-year-one/) · [DW2: Welcome to Beta](https://www.dungeon-world.com/welcome-to-beta/) · [DW2 Beta](https://www.dungeon-world.com/beta/) · [Spencer Moore roadmap](https://spencermoore.ca/2025/04/04/dungeon-world-2-an-optimistic-roadmap/) · [Troy Press: DW2 so far](https://troypress.com/dungeon-world-2/) · [Rascal: Helena Real on DW2](https://www.rascal.news/helena-real-speaks-candidly-about-dungeon-world-2/) · [Mythcreants critique](https://mythcreants.com/blog/dungeon-world-is-a-game-to-skip/) · [RPGnet: running DW wrong](https://forum.rpg.net/threads/im-running-dungeon-world-pbta-wrong-please-help-me-run-it-right.854513/) · [EN World: GM moves](https://www.enworld.org/threads/reading-through-dungeon-world-questions-for-gms-re-initiating-a-gm-move.556764/)

**Descendants:** [World of Dungeons](https://johnharper.itch.io/world-of-dungeons) · [Homebrew World v1.5.1](https://i.4pcdn.org/tg/1656401386330.pdf) · [Spouting Lore: Homebrew World](https://spoutinglore.blogspot.com/2018/07/homebrew-world.html) · [Troy Press: Freebooters 2e](https://troypress.com/freebooters-on-the-frontier-2e-is-the-osr-pbta-homage-to-odd/) · [Adventuresmith attributions](https://github.com/stevesea/Adventuresmith/blob/master/content_attribution.md) · [Stonetop deep dive](https://indiegamereadingclub.com/indie-game-reading-club/deep-dive-stonetop/) · [Rascal: Stonetop](https://www.rascal.news/from-blog-posts-to-mighty-1-200-page-books-stonetops-creators-reflect-on-a-decade-long-journey/) · [Troy Press: Chasing Adventure](https://troypress.com/chasing-adventure-a-fantasy-pbta-without-the-ddisms/) · [Deathtrap: Chasing Adventure](https://deathtrap-games.blogspot.com/2025/06/game-review-chasing-adventure.html) · [Troy Press: DW vs 5 hacks](https://troypress.com/table-comparing-dungeon-world-to-5-hacks/) · [Troy Press: PbtA Commons](https://troypress.com/the-pbta-commons/)

**Ironsworn:** [Tomkin Press licensing](https://tomkinpress.com/pages/licensing) · [Gnome Stew review](https://gnomestew.com/ironsworn-review/) · [Ironsworn SRD](https://tedtschopp.github.io/Ironsworn-SRD/Ironsworn%20SRD.html)

**WWN:** [WWN SRD (CC0)](https://www.drivethrurpg.com/en/product/473939/worlds-without-number-system-reference-document) · [Tenkar's Tavern](https://www.tenkarstavern.com/2024/11/free-osr-worlds-without-number-core.html) · [Eldritch Exarch review](https://eldritchexarchpress.substack.com/p/a-reviewcritique-of-worlds-without)

**13th Age:** [Archmage Engine SRD (PDF)](https://pelgranepress.com/media/SRD/13thAgeArchmageEngineSRD.pdf) · [Pelgrane licensing overview](https://pelgranepress.com/2014/02/19/13th-age-archmage-engine-licensing-overview/) · [EN World pros/cons](https://www.enworld.org/threads/13th-age-pros-and-cons.352410/) · [Scroll for Initiative review](https://scrollforinitiative.com/2023/03/11/13th-age-the-best-rpg-ive-never-played-review/) · [Sly Flourish: escalation die](https://slyflourish.com/escalation.html)

**Daggerheart / Draw Steel:** [DPCGL](https://darringtonpress.com/license/) · [Daggerheart FAQ](https://www.daggerheart.com/faq/) · [Wikipedia: Daggerheart](https://en.wikipedia.org/wiki/Daggerheart) · [Drolleries on Fear](https://drolleries.substack.com/p/how-to-use-fear-in-daggerheart-and) · [Solo TTRPG on Daggerheart](https://solottrpg.substack.com/p/daggerheart-my-thoughts-and-ramblings) · [Draw Steel Creator License](https://www.mcdmproductions.com/draw-steel-creator-license) · [Dice Society: Draw Steel review](https://thedicesociety.com/draw-steel-review/) · [Steel Compendium: power roll](https://steelcompendium.io/v2/Browse/rule/dice/power-roll/)

**Player-facing / OSR / Cypher:** [Black Hack English SRD](https://the-black-hack.jehaisleprintemps.net/english/) · [dieheart: Black Hack](https://www.dieheart.net/the-black-hack/) · [Deathtrap: Numenera](https://deathtrap-games.blogspot.com/2022/06/game-review-numenera-original-edition.html) · [Nerdist: GM intrusions](https://nerdist.com/article/why-numeneras-gm-intrusions-are-the-best-worst-thing-for-your-rpg-character/) · [CSOL](https://www.montecookgames.com/cypher-system-open-license/) · [CSRD licence](https://cyphersrd.quest/100-license/) · [Cairn repo](https://github.com/yochaigal/cairn) · [Knave](https://questingbeast.itch.io/knave)

**Class-building:** [UESP: Morrowind classes](https://en.uesp.net/wiki/Morrowind:Classes) · [Wikipedia: Troika!](https://en.wikipedia.org/wiki/Troika!_(role-playing_game)) · [Deathtrap: ICRPG](https://deathtrap-games.blogspot.com/2021/12/game-review-index-card-rpg-master.html) · [Pinnacle licensing](https://peginc.com/licensing/) · [SJG online policy](https://www.sjgames.com/general/online_policy.html)

**Licence compatibility:** [FSF licence list](https://www.gnu.org/licenses/license-list.html) · [CC compatible licences](https://creativecommons.org/share-your-work/licensing-considerations/compatible-licenses/) · [Blades licensing](https://bladesinthedark.com/licensing)
