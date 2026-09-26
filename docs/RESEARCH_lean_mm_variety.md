# RESEARCH: Lean MM Variety. Procedures, generators and scaffolding on the Mirror Master's side

**Date:** 2026-09-25
**Tier:** Research (literature review) feeding a Brain decision. Nothing here is a ruling. Rulings belong to the owner.
**Question:** The lean redesign (`RESEARCH_complexity_audit.md` §7) moves variety off the player sheet and onto the MM's side as procedures, tables and generators that the app delivers. What does the literature say those procedures should be, how should monsters and loot be written to carry variety cheaply, what does the evidence say about digital GM tools at the table, and how do beginner products teach refereeing?
**Inputs read:** `RESEARCH_complexity_audit.md` §1, §4, §7; `RESEARCH_fun_audit_2026-09.md` §6, §8; `mm_manual/MM1` conduct fields; `MM5` Trouble Table; `enemies/chalk_hound.fof`, `enemies/bought_sergeant.fof`; the app's Threat Clock card (`software/app/static/js/components.js`).
**Sources:** 40+ (listed inline and in the bibliography at the end).
**Copyright:** everything below is paraphrase. No table, stat block or rules text from any source is reproduced. Where a source is openly licensed, the licence is noted, since that decides whether we can later adapt *wording* as well as *ideas*. Ideas and procedures are free to borrow in any case. Wording is not.

---

## Summary

1. **The old-school variety engine was a handful of referee dice rolls, and none of them is a player rule.** Reaction roll, morale check, the wandering-encounter/pressure die, treasure and rumor tables. Each one takes a single roll and answers a question the MM would otherwise have to invent an answer to under pressure. All of them port to our 2d6 engine with almost no translation, and the app can make each one a single click.
2. **Treat every result as a prompt, not a verdict.** Necropraxis, The Perilous Wilds, the Alexandrian and Mythic all say the same thing: the MM interprets the roll, may defer it, and should never let it contradict the fiction. The app should show a result with a short "why this could be happening" line and a reroll/defer button. It should never auto-apply one.
3. **The pressure die is the best single import.** One d6 per exploration turn or scene change, with every face meaning something (encounter, sign of an encounter, local hazard, fatigue, supply, lucky break). It merges four bookkeeping timers into one roll and has no null results. A per-site face list is cheap to write and very flavourful.
4. **Monsters get variety from *behaviour*, not numbers.** The strongest formats (Dungeon World, Cairn, Mausritter, The Black Hack, the Monster Overhaul) give each monster a want or instinct, one or two special things, a morale value, and tables of variants or twists. Our current `.fof` conduct fields (disposition, first target, triggers, morale, negotiation) are already ahead of most OSR formats. The lean redesign should keep them, drop the Threat Rating arithmetic, and add a **d6 twist table** per monster.
5. **Loot is the cheapest carry-forward reward, and the fun is in situational items, not +1s.** Cyphers (use-it-or-lose-it consumables), Into the Odd's arcana (items that do something strange, not something bigger) and Knave 2e's relics (power tied to obligation) all beat stat-boosting items. Treasure-as-XP is the historically proven way to aim the reward loop at exploration.
6. **The digital evidence says: context, speed and ownership.** In CALYPSO (AIIDE 2023), DMs used an LLM assistant for an average of 2.3 turns per consult during live play, against 45 when they had no time pressure. Expert GMs build personal "repertoires" of readymade artifacts: name lists, generators, table stacks (Tchernavskij & Webb, C&C 2022). One found an iPad tracker slower than paper and dropped it. The GMs Acharya interviewed wanted condensed references, faction goals with next steps, and "what could happen next" prompts, and they said the prompts would help beginners most.
7. **So the in-session MM toolbox needs:** at most two clicks from the thing on screen; results scoped to the current site/scene; private by default; logged automatically so they feed recaps, rumors and clocks; every table editable, importable and printable. No setup mid-session.
8. **Beginner boxes teach refereeing by embedding procedures in the first adventure**, one per scene (Pathfinder Beginner Box, Lost Mine's goblin ambush). They fail when they drop the procedure: the Alexandrian faults the D&D Starter Set for giving no dungeon procedure, and critics note Lost Mine leaves new DMs with a sandbox and no guidance. Shadowdark teaches through one visible pressure mechanic, the torch timer.
9. **Our novice-MM failure modes are known** (fun audit §8.3: every social roll set to Hard, 7–9 read as a penalty, fights slipping back into turn order, the table stalling in Movement II). Each one maps to a specific app nudge. The strongest is a **"Stuck?" button** that offers three moves drawn from the MM's own prep: a threat advances, an NPC arrives with a want, a secret surfaces.
10. **Priority for the lean build (P0):** reaction roll, morale, pressure die, per-pillar d66 complication tables, the lean monster card with its twist table, a loot generator with one-use curios, an NPC card generator, a 2d6 yes/no oracle. **P1:** prep card (Lazy-DM-style secrets list with reveal tracking), threats with portents on the existing Threat Clocks, a simple faction turn that writes rumors, a site generator, a journey procedure. **P2:** optional AI assist that stays inside the MM's own content.

---

## 1. Procedure catalogue

Each entry covers: the problem it solves, how it runs (in our words), what the app can automate, sources, and licence notes. "2d6 fit" says how it maps onto our three-tier engine (6− / 7–9 / 10+, with naturals 2 and 12 as the extremes).

### 1.1 Reaction roll

- **Problem.** The MM meets a creature or NPC the prep didn't anticipate and has to decide on the spot whether it's hostile. Novices default to hostile, and every meeting turns into a fight.
- **How it runs.** When the party meets someone whose attitude isn't already fixed by the fiction, the MM rolls 2d6. Low means hostile, the middle bands mean wary or uncertain, high means talkative or helpful. Because the curve is bell-shaped, the most common result is *uncertain*, so most meetings open as a conversation and the initiative stays with the players. Variants: the party's speaker adds a modifier; the roll is split so players roll "their half"; the two dice are read as a d66 to give 36 finer shades of attitude.
- **2d6 fit.** Exact. Suggested bands: natural 2 = attacks or flees at once; 3–6 = hostile or unfriendly; 7–9 = wary, wants something first; 10–11 = open to talk or trade; natural 12 = unexpectedly helpful. That reuses the players' own tier boundaries, so the MM learns one scale.
- **App.** A **React** button on every NPC or enemy card and on the encounter panel. The result shows the band plus a one-line want pulled from the creature's `wants` field or a generic d66 "what they want right now" table. It can be rerolled and is private by default.
- **Sources.** Reaction rolls unpacked and the d66 variant: https://eucatastrophic.bearblog.dev/unpacking-reaction-rolls/ ; editions compared: http://osrsimulacrum.blogspot.com/2020/09/across-editions-reaction-table.html ; two-tier variant: https://dicegoblin.blog/the-two-tiered-reaction-roll/ ; in practice: http://methodsetmadness.blogspot.com/2023/05/reaction-rolls-in-practice-osr.html ; Knave's version (CC BY 4.0): https://questingbeast.itch.io/knave
- **Licence.** The idea is 1970s–80s D&D and free as a procedure. Knave 1e is CC BY 4.0 if we ever want to adapt its wording. Our own band names are safer.

### 1.2 Morale check

- **Problem.** Fights run to the last hit point, which is slow, bloody and unrealistic, and makes every fight a war of attrition. The fun audit found combat short but shallow. Morale adds the question "will they break?" at no player-side cost.
- **How it runs.** Each monster has a morale value. At trigger points (first casualty, half the group down, leader down, a lone foe badly hurt, a frightening display) the MM rolls 2d6 against it; over the value, they flee, surrender or bargain. Hirelings check too.
- **2d6 fit.** Could be re-expressed as a three-tier roll for consistency: the MM rolls 2d6 + the creature's nerve modifier; 10+ they fight on, 7–9 they waver (fall back, offer terms, grab the wounded), 6− they break. Our current enemy files already have a prose `morale:` line, which says *how* they break. Keep that, and add the number that says *when*.
- **App.** When the MM marks enemy casualties in the tracker, the app watches the triggers (half down, leader down) and puts a **Morale?** chip on the group; one click rolls it and shows the creature's own morale prose. Mooks inherit their group's roll.
- **Sources.** Knave morale triggers (CC BY 4.0): https://questingbeast.itch.io/knave ; the Alexandrian's hexcrawl-at-table uses reaction tables for hireling loyalty: https://thealexandrian.net/wordpress/17464/roleplaying-games/hexcrawl-part-12-at-the-table
- **Licence.** Procedure is free. Knave CC BY 4.0.

### 1.3 The overloaded pressure die (encounter die)

- **Problem.** Classic wandering-monster checks mostly return "nothing", and meanwhile the MM is tracking light, rations and fatigue separately. Exploration either drags or has no clock.
- **How it runs.** One d6 whenever the party enters a new area or spends a chunk of time. Every face is keyed: one face is an encounter, one is a *sign* of an encounter (tracks, noise, spoor), one is a local hazard specific to the place (rising water, a collapsing passage), one is fatigue, and the last two drain supplies (light, food). There are no null faces. The designer's own advice is to treat results as prompts that can be deferred a limited number of times, and to ignore the attrition faces for the first several turns so nothing absurd happens. Extensions: a "peril" version used as the whole game's core; per-location "gimmick" faces; an escalating die that shrinks as time passes; encounter tables where each entry is itself overloaded (monster *plus* what it's doing).
- **2d6 fit.** It's a d6 roll by the MM and doesn't touch the player engine. For our game, replace the resource faces with things that matter to us. We don't track torches. Suggested generic faces: 1 encounter, 2 sign/omen, 3 local hazard (site-keyed), 4 cost (a supply, a favour, time), 5 **opportunity** (a lucky find, a shortcut, an NPC in need), 6 quiet (but it tips the next roll toward trouble). Keeping a positive face matters for our adventure register, where wonder and discovery are part of the tone and dread isn't the default.
- **App.** A **Pressure** button in the scene bar. Faces 1 and 3 pull from the current site's own tables; face 2 shows the omen that belongs to the face-1 result the app pre-rolls (so a sign always precedes its monster); face 4 can tick a Threat Clock. The log records each roll.
- **Sources.** Necropraxis original: https://necropraxis.com/2014/02/03/overloading-the-encounter-die/ ; overloading the table itself: https://www.prismaticwasteland.com/blog/overloading-the-random-encounter-table ; gimmick-laden tables: http://tenfootpolemic.blogspot.com/2017/08/improving-your-encounter-tables-with.html ; as core mechanic: https://wasitlikely.blogspot.com/2019/07/the-peril-system-overloaded-encounter.html ; escalating die for pointcrawls: https://theadventuringday.wordpress.com/2021/04/05/pointcrawls-applied-the-escalating-encounter-die/
- **Licence.** Blog posts, no open licence stated. Borrow the procedure only, in our own words (which is what this is).

### 1.4 Random encounters, redesigned

- **Problem.** Long lists of monster names produce encounters with no dramatic question, and most prepped entries never get used.
- **How it runs.** The Angry GM's argument: make the *timing* random and the *content* designed. Prep three or four rich encounters per session instead of a dozen thin ones. Each one should do a job: drain a resource, move a roving plot element closer, force a two-good-options choice, or impose a complication. The Alexandrian's hexcrawl adds a sequence: check whether the result is tracks, then a lair, then a wandering group. Encounters thereby generate *places*, and those places cluster where the players spend their time. He batches a whole day's checks in one handful of dice.
- **App.** Encounter entries carry a **job** tag (drain / plot / choice / complication) and a dramatic question. The app can pre-roll a day's checks for a journey and show them as a timeline. A "tracks or lair?" follow-up turns a wandering result into a findable place and offers to pin it to the map.
- **Sources.** https://theangrygm.com/redesigning-random-encounters-2/ ; dramatic question: https://theangrygm.com/four-things-youve-never-heard-of-that-make-encounters-not-suck/ ; https://thealexandrian.net/wordpress/17333/roleplaying-games/hexcrawl-part-4-encounter-tables ; https://thealexandrian.net/wordpress/48697/roleplaying-games/hexcrawl-addendum-special-encounter-tables ; https://thealexandrian.net/wordpress/46498/roleplaying-games/hexcrawl-errata-using-encounter-tables
- **Licence.** Proprietary blogs. Ideas only.

### 1.5 Hexcrawl / journey procedure

- **Problem.** Travel is either skipped ("you arrive") or becomes a slog.
- **How it runs.** Split the day into watches. Pre-roll the encounter checks. Resolve navigation, then movement, then encounters; say "uneventful" fast when nothing happens. At session start, roll a rumor check per PC. The Perilous Wilds (a Dungeon World supplement) adds journey roles (scout, navigator, quartermaster), each with a move, plus discovery and danger generators whose results are explicitly prompts.
- **2d6 fit.** Give each journey role one roll per leg: 10+ a benefit, 7–9 as planned, 6− the MM pulls a danger or complication. That's three player rolls a day, one per role, which keeps players active without adding rules.
- **App.** A **Journey** panel: pick a route and pace; the app lays out legs, pre-rolls the pressure die per leg, asks for the role rolls, and offers one discovery and one danger per leg from region tables.
- **Sources.** https://thealexandrian.net/wordpress/17464/roleplaying-games/hexcrawl-part-12-at-the-table ; https://thealexandrian.net/wordpress/48033/roleplaying-games/5e-hexcrawl-part-7-hex-exploration ; Perilous Wilds reviews: https://save.vs.totalpartykill.ca/review/the-perilous-wilds/ , https://seedofworlds.blogspot.com/2022/09/review-perilous-wilds.html
- **Licence.** The Perilous Wilds is a commercial product. DW itself is CC BY 3.0; the supplement's own text is not open, so ideas only.

### 1.6 Three Clue Rule and node-based design

- **Problem.** Investigations stall because the one clue that mattered was missed. The fun audit named this concern for Oraga Night ("no single failed roll closes a thread"), and the module solved it by hand.
- **How it runs.** For any conclusion the players must reach, place at least three clues to it. Distinguish *leads* (which point to a place or person to investigate next) from *evidence* (which supports a conclusion). Invert it for structure: if each node holds three leads to other nodes, players with any three leads will reach at least one next node. Nodes can be places, people, organisations, events or activities. Prep is building tools, not writing a script.
- **App.** The prep editor tracks **conclusions** and the clues that point to them, and warns when a conclusion has fewer than three. During play, the MM ticks clues as found; the app shows which conclusions are now reachable and which clues are still in play. This is the single most useful mystery aid a digital tool can give, and it costs almost nothing to build.
- **Sources.** https://thealexandrian.net/wordpress/1118/roleplaying-games/three-clue-rule ; https://thealexandrian.net/wordpress/1105/roleplaying-games/three-clue-rule-part-4-corollaries ; https://thealexandrian.net/wordpress/50095/roleplaying-games/running-mysteries-the-two-types-of-leads ; https://thealexandrian.net/wordpress/8122/roleplaying-games/node-based-scenario-design-collectors-edition ; https://thealexandrian.net/wordpress/7985/roleplaying-games/node-based-scenario-design-part-3-inverting-the-three-clue-rule
- **Licence.** Proprietary essays. The principle is universal and free to use; don't borrow the prose.

### 1.7 Secrets and clues / Lazy prep checklist

- **Problem.** Prep takes too long and most of it goes unused. Novices don't know what to prep.
- **How it runs.** Sly Flourish's eight-step checklist: review the characters, write a strong start, sketch possible scenes, list secrets and clues, sketch a few fantastic locations (each with three evocative features), list important NPCs, choose monsters, choose rewards. The core trick is **secrets and clues**: about ten one-sentence facts the players could learn, *not* tied to where they're found. The MM decides mid-play which NPC, fresco or dream delivers one. Roughly half get revealed per session; the rest roll forward. Later essays stress that the steps are a menu and that only a few are needed each session.
- **Relation to 1.6.** These are complementary. The Three Clue Rule makes sure a *conclusion* can't be missed; free-floating secrets make sure the MM always has *something true to reveal* in whatever scene the players choose.
- **App.** A **Prep card** per session: strong start, secret list with a reveal checkbox and a "revealed via" note, NPC shortlist, location list, rewards. Unrevealed secrets carry into next session's card automatically. During play the secret list sits one click away in the side panel.
- **Sources.** https://slyflourish.com/eight_steps_2023.html ; https://slyflourish.com/using_the_8_steps_at_the_table.html ; https://slyflourish.com/choosing_the_right_steps.html ; Lazy GM's Resource Document: https://slyflourish.com/lazy_gm_resource_document.html
- **Licence.** The **Lazy GM's Resource Document is CC BY 4.0**, and it includes name, location, monument, trap, trinket and town-event tables plus monster templates. That's usable wording with attribution. Its tables are D&D-flavoured, so we'd rather adapt the structure than copy the entries.

### 1.8 Fronts, dangers and grim portents (Dungeon World)

- **Problem.** The world feels static between sessions; villains only act when the players are watching.
- **How it runs.** A *front* groups two or three *dangers* that share a theme. Each danger has an *impulse* (what it wants, in a verb), a short chain of *grim portents* (the steps by which it gets worse), and an *impending doom* (what happens if nobody stops it). The MM writes a few *stakes questions* they genuinely want answered in play and a small cast. Portents get marked either because the players' actions caused them or because the MM advanced one as a hard move after a miss.
- **2d6 fit.** Portents are just a Threat Clock with named segments. **We already have Threat Clocks in the app** (`components.js`, PHB III.2, D4). A front is a Threat Clock whose segments have text, and each segment tick reveals its portent line to the MM.
- **App.** A Threat Clock gains an optional *impulse* and *per-segment portent text*. The "Advance (6−)" button already exists. Add a between-scenes reminder: "Nothing has advanced for three scenes. Offer a portent?"
- **Sources.** https://www.dungeonworldsrd.com/gamemastering/fronts/ ; retrospective by Sly Flourish: https://slyflourish.com/looking_back_on_fronts.html
- **Licence.** **Dungeon World text is CC BY 3.0 Unported** (Koebel & LaTorra). Wording could be adapted with attribution. Before putting CC BY 3.0 text into a GPLv3 repo, check compatibility; the FSF lists CC BY 4.0 as GPL-compatible, and 3.0 should be checked rather than assumed.

### 1.9 GM moves and principles (Apocalypse World / Dungeon World)

- **Problem.** On a 6− the novice MM doesn't know what to *do*. The fun audit found the novice persona reading 7–9 as "−1 next roll" and answering 6− with "you learn nothing".
- **How it runs.** The GM has a short *agenda* (make the world seem real, keep the characters' lives interesting, play to find out) and a list of *moves* for when the players look to them or miss a roll: reveal an unwelcome truth, show signs of an approaching threat, deal damage, use up their resources, turn their move back on them, separate them, offer an opportunity with a cost, put someone in a spot. Soft moves warn; hard moves bite. Moves never announce their own name.
- **2d6 fit.** This is exactly what our Trouble Table is. The d6 Trouble Table in MM5 (Cost / Position / Attention / Equipment / Condition / …) is a compressed move list. The lean redesign should grow it into one list per pillar (see §7).
- **App.** When a player rolls 6−, the MM's panel lights up with **three suggested moves** filtered by the current scene type and threats, each with a one-line example. Hard vs soft is marked. The same panel answers 7–9 with "pick a cost" options.
- **Sources.** https://www.dungeonworldsrd.com/moves/ ; AW agenda and principles discussed: https://gnomestew.com/the-gms-agenda-and-principles/ , http://www.diceexploder.com/blog/2024/4/10/more-on-apocalyptic-principles
- **Licence.** DW CC BY 3.0. Apocalypse World is proprietary (© D. Vincent Baker); use the idea of an agenda + principles + moves, not AW's lists.

### 1.10 Progress clocks (Blades in the Dark)

- **Problem.** Complex obstacles and approaching dangers need visible, gradual progress.
- **How it runs.** A circle with 4, 6 or 8 segments depending on how daunting the obstacle is. Actions, consequences and time tick it; when full, the thing happens. The key design advice: name the clock after the *obstacle* ("interior patrols"), not the *method* ("sneak past the guards"), so players can attack it any way they like.
- **Status.** Already in Facets (Threat Clocks, D4). The lean redesign should keep them, add the naming advice to the MM text, and use clocks as the common currency behind fronts and factions (1.8, 1.11).
- **Sources.** https://bladesinthedark.com/progress-clocks ; https://thealexandrian.net/wordpress/40424/roleplaying-games/blades-in-the-dark-progress-clocks ; ICRPG's visible scene timers (dice that count down) are a close cousin: https://www.creativegamelife.com/index-card-rpg-master-edition-guide
- **Licence.** **Blades SRD is CC BY 3.0 Unported** with a required attribution line and a clause against use prejudicial to One Seven Design. Same GPL check as DW.

### 1.11 Faction turns

- **Problem.** The campaign world needs motion between sessions without the MM hand-authoring every development.
- **How it runs (Sine Nomine family).** Each faction has a few ratings (Worlds Without Number uses Cunning, Force, Wealth and Magic), a pool of hit points and treasure, a list of assets, and a goal. On a faction turn (roughly once per in-game month, or between sessions) each faction takes one action: attack a rival's asset, expand, build, move, hide, sell, or push a multi-turn project. Contests are opposed rolls on the relevant rating. The output is *news*: things that have happened in the world, which then become rumors and hooks.
- **Simplify for us.** Full asset management is too much bookkeeping even for the MM. A lean version: each faction is a name, an impulse, one goal as a 6-segment clock, and one rival. Between sessions the app rolls 2d6 per faction: 10+ ticks 2, 7–9 ticks 1 *and* costs the faction something visible, 6− a setback (the rival ticks instead, or the faction loses a named asset). Each result writes one line into the **rumor table**.
- **App.** A **Between Sessions** screen: one button runs the faction turn, shows the resulting headlines, lets the MM veto or edit each, and pushes the survivors into rumors and clocks. Acharya's interviewees specifically asked to track faction goals and "the next steps they will take".
- **Sources.** WWN free edition (faction rules included): https://www.drivethrurpg.com/en/product/348809/worlds-without-number-free-edition ; faction mechanics summary: https://grokipedia.com/page/Factions_Worlds_Without_Number ; https://takeonrules.com/2018/12/27/lets-read-stars-without-number-factions/ ; https://glyphngrok.substack.com/p/creating-factions-in-an-open-world
- **Licence.** WWN is free to download but **not** openly licensed as far as I could verify. (A 2024 "Core Rules and SRD" release exists; I couldn't confirm its licence. Check before adapting any wording.) Ideas only.

### 1.12 Rumor tables

- **Problem.** Players don't know where to go, and hooks feel imposed.
- **How it runs.** A short table per region or site (d6–d12), mixing true, partly true and false rumors. PCs get one when they arrive somewhere, carouse, ask around, or (in the Alexandrian's version) by a per-PC chance at session start. Oraga Night already has one; the fun audit wanted the pattern generalised.
- **App.** Rumors are a table type. The faction turn and the Threat Clocks *write* into it automatically. The MM can mark each rumor true or false privately; the app tracks who heard what.
- **Sources.** https://thealexandrian.net/wordpress/17464/roleplaying-games/hexcrawl-part-12-at-the-table ; Oraga Night (our own).

### 1.13 NPC generator

- **Problem.** Improvised NPCs come out nameless and interchangeable. Naming on the spot is hard: an expert GM in the C&C 2022 study kept hand-collected name lists in his notebook for exactly this reason.
- **How it runs.** Roll a name, one visible trait, one want, one fear or secret, and (for our game) the difficulty the NPC imposes on persuasion. Oraga Night's cast chapter shows the target quality: want / fear / secret per NPC.
- **App.** **New NPC** gives a card in one click from culture-specific name tables. It can be locked into the session's cast with one more click, and after that it's searchable and appears in the recap.
- **Sources.** Tchernavskij & Webb 2022 (see §4); Lazy GM Resource Document name tables (CC BY 4.0); donjon (free web tool, proprietary): https://donjon.bin.sh/

### 1.14 Oracles and GM emulators (solo tools as MM aids)

- **Problem.** The MM faces a yes/no question about the world ("Is the gate locked? Is anyone home?") and has no principled way to decide, so the answer is always whatever is most convenient. Solo tools solve exactly this.
- **How it runs.** *Ironsworn's Ask the Oracle*: set the odds (almost certain / likely / even / unlikely / small chance), roll, read yes or no, with extreme results giving "yes, and" or "no, and". Other tables are prompts to interpret (action + theme, descriptor + focus). *Mythic GM Emulator*: the odds are cross-indexed with a **Chaos Factor** that rises when scenes go out of the protagonists' control, so later questions tilt toward "yes, something happens". Scene setups can be altered or interrupted by random events.
- **2d6 fit.** A 2d6 oracle falls straight out of our engine: roll 2d6 + an odds modifier (+2 likely, 0 even, −2 unlikely); 10+ yes, 7–9 yes but (or "yes, with a catch"), 6− no; naturals give "and". It uses the same scale the players already read, and it's also a solo/duo mode for free.
- **App.** An **Ask** button that takes a typed question, an odds pick, and optionally a two-word prompt (action + theme) from a d66/d66 pair. Logged.
- **Sources.** https://ironsworn-rpg.fandom.com/wiki/Ask_the_Oracle ; Ironsworn licensing: https://tomkinpress.com/pages/licensing ; Mythic: https://www.wordmillgames.com/page/mythic-gme.html , review: https://glyphngrok.substack.com/p/review-mythic-game-master-emulator
- **Licence.** **Ironsworn's SRD and oracle-table text are CC BY 4.0**, which is the most permissive oracle source available. Mythic is proprietary: borrow the chaos-factor *concept* only.

### 1.15 Site (dungeon) generator

- **Problem.** The MM needs a place to explore on short notice, and a novice doesn't know what a good site contains.
- **How it runs (Mausritter).** Roll a site's construction (what it was built as), what ruined it, who lives there now, what they want, and a secret. Then generate a handful of rooms from a room-type-plus-feature table, and place creatures, treasure and the secret among them. It teaches the anatomy of a site (history → ruin → inhabitants → goal → secret) while generating one.
- **App.** **New Site** gives a skeleton: 6–12 rooms as nodes with a pressure die face list, a local rumor table, two clues to the secret, and a treasure hoard. Everything is editable before play.
- **Sources.** https://mausritter.com/adventure-site/ ; Mausritter licence (CC BY 4.0): https://mausritter.com/ ; Lazy GM "fantastic locations with three features": https://slyflourish.com/eight_steps_2023.html
- **Licence.** **Mausritter and its generator are CC BY 4.0.** Mouse-scale content wouldn't fit anyway; adapt the *structure*.

### 1.16 Scene-level encounter design: dramatic question, information–choice–impact

- **Problem.** Scenes and fights that aren't *about* anything.
- **How it runs.** The Angry GM: an encounter poses and answers a dramatic question; tension lasts only while the answer is uncertain; name the cost of failure up front. McDowall's ICI doctrine: give the players **information** (clear signals of danger and opportunity), a real **choice**, and a visible **impact** that they can point back to later. Both are checklists the MM can apply in five seconds.
- **App.** Encounter and scene cards carry a "question" and a "cost of failure" field. The builder warns when either is blank. The Stuck? panel (see §5) draws on them.
- **Sources.** https://theangrygm.com/four-things-youve-never-heard-of-that-make-encounters-not-suck/ ; https://theangrygm.com/how-to-build-awesome-encounters/ ; https://www.bastionland.com/2018/09/the-ici-doctrine-information-choice.html

### 1.17 GM resources that escalate (Daggerheart Fear, Draw Steel Malice)

- **Problem.** Monster threat is fixed at the start of the fight, and a lone survivor is boring.
- **How it runs.** The GM has a pool (Fear, Malice) that fills as the players act, sometimes by the dice and sometimes per round, and spends it to trigger monster features: an extra action, a special attack, a spotlight interrupt. Draw Steel's stated goal is that even the last goblin can do something surprising.
- **Fit for us.** We already have the mirror of this: **Borrowed Trouble** and the 6− result give the MM leverage. A lean alternative that avoids another currency is to make every monster's *special thing* trigger on a player's 6− or natural 2 rather than on an MM pool. The monster card says "on a miss against it: …". The variety arrives without a second economy to track.
- **Sources.** Daggerheart SRD adversaries: https://daggerheartsrd.com/rules/adversaries/ ; https://daggerheart.org/gm/core-gm-mechanics ; Draw Steel resources: https://www.mcdmproductions.com/draw-steel-resources
- **Licence.** Both proprietary (Darrington Press community licence; MCDM creator licence). Concept only.

### 1.18 Campaign-frame structures (Stonetop, Brindlewood Bay)

- **Stonetop.** The home village has its own sheet (fortunes, prosperity, population, defense) and moves. Each season its state feeds what threats and opportunities arrive, and the GM keeps threats, sites and relationship maps on tabbed prep sheets with both core loops flowcharted. The lesson for us: **a campaign has one shared "home" object whose state drives the MM's tables.** Sources: https://stonetop-wiki.github.io/ ; https://indiegamereadingclub.com/indie-game-reading-club/deep-dive-stonetop/ . Proprietary.
- **Brindlewood Bay.** The Keeper holds a list of evocative clues *not tied to a solution*, places them as players investigate, and the players theorize the answer; a roll adjusted by clues held and mystery complexity decides whether the theory is right. It's prep-light and puts the solve in the players' hands, at the cost of a fixed truth. For Facets it's a useful *optional* mode for social/mystery Facets, not the default. Sources: https://thealexandrian.net/wordpress/47226/roleplaying-games/review-brindlewood-bay ; https://www.domainofmanythings.com/blog/what-do-you-think-happened-a-plug-and-play-mystery-mechanic-from-brindlewood . Proprietary.

### 1.19 Not covered: Delta Green-style opposition moves

The brief named "Delta Green-style opposition moves". I couldn't find an open, citable description of a specific DG procedure in the time available, so I have left it out rather than guess. The nearest verified equivalents are DW fronts (1.8) and WWN faction turns (1.11), which together cover "the opposition acts off-screen on a schedule".

---

## 2. Monster format

### 2.1 Comparison

| Format | Numbers | Behaviour | Variety device | Licence |
|---|---|---|---|---|
| **B/X-style (via Knave, OSE)** | HD, AC, attack, damage, morale, # appearing | Reaction roll + morale do the behaviour | Encounter tables; lairs | Knave CC BY 4.0; OSE OGL |
| **The Black Hack** | HD only; armour, damage and attack difficulty all *derived* from HD | A few ability notes | Monsters stronger than your level make *your* rolls harder | OGL (verify) |
| **Shadowdark** | One line: AC, HP, attacks, move, six modifiers, alignment, level | Short trait list | Tables in adventures | Proprietary (third-party licence) |
| **Cairn** | HP, armour, three stats, weapon die | One or two specials; a named *critical damage* effect | The crit effect makes each monster's "worst moment" unique | **CC BY-SA 4.0** |
| **Mausritter** | HP, armour, three stats, attack | *Wants* and variants tables per creature | Per-creature d6 variants | **CC BY 4.0** |
| **Dungeon World** | HP, armour, damage die | **Instinct** (a verb) + 1–3 **moves** + tags | Moves make the monster act differently; stat-less use possible | **CC BY 3.0** |
| **13th Age** | Full d20 block | Triggered specials on natural die results | **"Nastier specials"**: an optional extra ability for a harder version | OGL SRD (verify) |
| **ICRPG** | Modifier + Hearts (10 HP units) + one defining feature | Scene timers | Fast build from 3 choices | Proprietary |
| **Daggerheart / Draw Steel** | Full blocks | Actions, reactions, passives | GM resource (Fear/Malice) unlocks features | Proprietary |
| **Monster Overhaul (Skerples)** | Light stats | Tables around each entry: names, twists, lairs, variant forms, encounter prompts | The *tables around the monster* are the product | Proprietary |
| **Facets now (`enemies/*.fof`)** | tier, attack mod, armour, Resolve, TR breakdown | disposition, first_target, triggers, morale prose, negotiation, organisation, special | One named special; Boss phases | Ours (GPLv3) |

Three findings:

1. **Everyone who is light derives numbers from one value.** The Black Hack derives everything from HD; ICRPG uses Hearts plus a modifier; DW uses a size/tag checklist. Nobody light makes the referee compute a rating by adding four components, as our Threat Rating formula does.
2. **The behaviour line is the thing that plays.** DW's instinct and moves, Mausritter's wants, and our own `disposition`/`first_target`/`triggers` are what the MM actually uses at the table. The fun audit (§8) and MM1 both show our conduct fields are already better than most OSR blocks. **Keep them.**
3. **Variety comes from a small table attached to each monster**: Mausritter's variants, the Monster Overhaul's twists, 13th Age's nastier special. Same monster, different fight, no new stat block. McDowall's advice to "go big" on monster ideas and to build monsters around what they want points the same way (https://www.bastionland.com/2009/04/brief-thoughts-on-monster-design.html ; https://www.bastionland.com/2020/01/inverted-monsters.html ; https://bastionland.substack.com/p/creating-creatures). So does Skerples' framing of a monster book as a toolbox of prompts that are hard to invent under pressure (https://coinsandscrolls.blogspot.com/2023/02/osr-monster-overhaul-megapost.html).

### 2.2 Recommended minimal monster card for Lean Facets

Assuming the clean-sheet chassis in complexity-audit §7.3 (HP for everyone, weapon damage dice, NPCs never roll, morale on 2d6):

```
NAME                       Level N  (sets HP = N×d-something, damage, and how hard it is to hit)
HP  __   Armor 0/1/2   Hits for dX   Morale N (or "never")
WANTS      one verb phrase — what it's doing when you meet it
SPECIAL    the one thing that makes it not a generic brute (fiction + effect)
ON A MISS  what it does when a player rolls 6− against it (its signature hard move)
TELLS      how the players can learn about the special before it bites (ICI: information)
BREAKS     how it flees / surrenders / bargains when morale fails
TWISTS d6  six one-line variants: where it is, what's wrong with it, who's with it
```

- **Level is the only dial.** The app derives HP, damage and hit difficulty from it (the Black Hack/ICRPG lesson). Threat Rating goes away. Encounter building is "how many levels vs. the party", with the MM's judgment and the recipes as guidance.
- **WANTS replaces disposition + first_target + negotiation** in one line. Keep `triggers` inside SPECIAL/ON A MISS.
- **ON A MISS** is our equivalent of Fear/Malice with no pool: the monster's surprise lands when the dice turn, which keeps the MM's variety tied to the core roll.
- **TELLS** is a formalisation of what Oraga Night already does with Fractures. Information before impact.
- **TWISTS d6** is where the variety lives. Eighteen current creatures × 6 twists = 108 fights from 18 cards.
- **Nastier option:** one extra line, "NASTIER:", for a boss-grade version (13th Age's idea). It replaces the need for separate Named/Boss tiers in most cases; Bosses keep phases.

Card length: 7–9 lines. That fits an app card and a printed index card. Our current `.fof` fields map across almost one-to-one, which makes migration mechanical.

---

## 3. Loot and reward loops

### 3.1 What the sources agree on

1. **Point the reward at the behaviour you want.** In early D&D most XP came from treasure recovered, not monsters killed, so players scouted, sneaked, negotiated and fled, and fights became obstacles rather than piñatas. The same sources warn that starving the game of treasure freezes advancement and flooding it bores the players. The reward still needs pacing. Sources: https://princeofnothingblogs.wordpress.com/2023/02/16/on-treasure-pt-i/ ; http://dreamsinthelichhouse.blogspot.com/2015/03/campaign-treasure-osr-vs-5e.html ; https://osrdread.blogspot.com/2019/11/osr-gold-as-xp-12-theory.html ; https://www.realmbuilderguy.com/2025/11/treasure-xp-and-player-choice.html ; https://kateplays.substack.com/p/xp-for-gold .
   *For us:* the complexity audit already moves XP to "discovered something / pursued a goal / changed the world". The lean equivalent of treasure-as-XP is **XP for treasure *brought home or spent on a goal***, which also gives coins a sink.
2. **Situational beats cumulative.** Skerples argues that items which give a constant bonus are dull, while items that invite creative misuse generate play, and that a treasure book needs curation and themed, findable sections to avoid being "sponge cake" (https://coinsandscrolls.blogspot.com/2024/01/osr-treasure-overhaul.html). Into the Odd's arcana are strange devices whose effects are described narratively rather than as bonuses, and they're the game's *only* magic, which pushes players toward danger to get it (https://en.wikipedia.org/wiki/Into_the_Odd ; https://www.rpg.net/reviews/archive/19/19108.phtml).
3. **One-use items beat hoarding.** Numenera's cyphers are abundant, weird and one-use, with a carry limit that punishes stockpiling, so players use them and there's always a new one to find (https://numenera.fandom.com/wiki/Cyphers ; https://pretendo.games/2019/06/02/decyphered-simplified-house-rules-for-numenera-the-strange/). The fun audit (§7) already named this "the cheapest known way to get 'what do I have this time?'", and our own Oraga Night crystals are consumables in exactly this vein.
4. **Power with strings attached creates story.** Knave 2e's relics are bound to a patron's domain and are revoked if misused; a quest earns one (https://rancourt.substack.com/p/analysis-knave-2e). Drawbacks and obligations turn an item into a plot hook.
5. **Loot tables are one of the things GMs actually use at the table.** Two of the eight expert GMs in the C&C 2022 study used designer- or community-made loot tables to improvise rewards after encounters.

### 3.2 A lean loot loop for Facets

- **Coin** is one number. It buys things and, when spent on a goal or brought home, pays XP.
- **Curios** (one-use, cypher-like): every hoard has one; **carry limit = 3** (a fourth makes one misfire, which is the table's comedy, in our adventure register rather than grimdark). Effects are narrative with a clear mechanical hook ("once: a Standard roll becomes Easy"; "once: ignore one hit"; "once: ask the oracle and treat the answer as true").
- **Relics** (permanent, rare): each has one *strange* power (not a +1), one **quirk** (a drawback or obligation), and a **wants** line if it's the aware kind. That ties them to our domain magic, since a relic can hold a readied intent or a domain at Minor scope, which gives Body characters a route to magic without violating "Body gets no magic" as a character rule. That last point needs an owner ruling.
- **Trinkets** (flavour only): a d66 table so every body searched yields *something*. It costs nothing and players love it.
- **Hoard generator**: the MM picks the site's level and theme, and the app rolls coin + 0–1 curio + a trinket + a 1-in-6 relic, all rerollable, with the result dropped into a character's inventory by drag.

---

## 4. Digital tool evidence

### 4.1 What the research says

- **Live play allows about two exchanges with a tool.** CALYPSO (Zhu, Martin, Head, Callison-Burch; AIIDE 2023): DMs used an LLM assistant inside Discord to understand monsters and brainstorm encounters. Unconstrained, a user iterated for about 45 turns; in live games the average was **2.3 turns**. DMs wanted both *low-fidelity* ideas to build on and *high-fidelity* text they could read out with light edits, and the system worked because it already had the encounter context and didn't make the DM paste it. One participant said running a game felt like laying track and fuelling the train at once. Sources: https://arxiv.org/abs/2308.07540 ; https://ar5iv.labs.arxiv.org/html/2308.07540
- **Expert GMs build personal "repertoires" of readymade artifacts.** Tchernavskij, Webb et al. (C&C 2022) interviewed eight expert GMs and catalogued 152 artifact uses. Seven of the eight used artifacts to offload improvisation (names, NPC concepts, what a vendor sells); five used random tables; one kept a one-keypress NPC generator always open beside him. GMs value artifacts they can search, skim, jump to, and consult or edit **without interrupting the flow**. One GM tried a map web-app and an iPad character tracker and found both *worse* than paper: the app forced standard components, and the tracker was slower to consult. Tools are highly idiosyncratic, and GMs are the gatekeepers of what reaches the table. Sources: https://dl.acm.org/doi/fullHtml/10.1145/3527927.3532798 ; PDF: https://csc.lsu.edu/~webb/articles/tchernavskijReadymades-2022.pdf
- **GMs want condensed references, faction goals, and "what next" prompts.** Acharya, Mateas & Wardrip-Fruin (ICIDS 2021) showed GMs a digital condensation of a beginner module. They liked having many pages boiled down to something usable during play; they wanted sort/filter/tag on NPCs, relationship views, **faction goals with next steps**, easy swapping of content (moving a clue to a different NPC when players skip the first), framing questions for how a faction would act on its beliefs, and **improvisational prompts for what could happen next**, which one GM said would help beginners most. Sources: https://eis.ucsc.edu/papers/Acharya_ICIDS2021.pdf ; https://dl.digra.org/index.php/dl/article/view/1310 ; thesis: https://escholarship.org/uc/item/7db84255
- **What DMs actually use.** Sly Flourish's 2016 survey of 800+ D&D DMs: the most-cited tools were an encounter *calculator* (Kobold Fight Club), the core books, a *generator* suite (donjon), a VTT (Roll20) and a notes app (OneNote). Two of the top four are digital utilities for the MM's side of the screen. Source: https://slyflourish.com/2016_dm_survey_results.html
- **Builder vs generator.** Kobold Fight Club is a calculator the GM drives and keeps creative control of; donjon hands over a finished encounter. The community's framing is "speed versus control". Sources: https://gmhub.roll20.net/resources/kobold-plus-fight-club/ ; https://twodollardm.com/blog/best-free-encounter-generators-2026
- **Rollable tables in VTTs.** Foundry treats rollable tables as a core document type with draw tracking and links, and the ecosystem adds GM-only rolling, player-requested rolls with hidden results, and a tabbed **GM Screen** grid where tables, notes and actors sit in cells for one-click use. This is the closest existing thing to an in-session MM toolbox, and it's all generic (no system knowledge). Sources: https://foundryvtt.com/article/roll-tables/ ; https://foundryvtt.com/packages/gm-screen ; https://foundryvtt.com/packages/better-rolltables/ ; https://foundryvtt.com/packages/rolltable-requester
- **Table engines.** Chartopia and Perchance host community tables and nested generators; reviewers find Chartopia cleaner but building full generators cumbersome, and table formats are fragmented (Necropraxis's "format wars" post). Lesson: **a table format that a non-programmer can write** matters more than generator power. Sources: https://chartopia.d12dev.com/ ; https://necropraxis.com/2018/07/22/random-table-format-wars/ ; https://www.randroll.com/building-rpg-random-generators/
- **AI GM assistants (2025–26).** The market moved from "prompt a chatbot" to campaign-aware assistants that remember sessions, open quests and decisions. The recurring value claims are recall ("what did we establish?") and brainstorming, and CALYPSO's time budget still applies. Sources: https://www.myarchivist.ai/ai-dungeon-master/ai-tools-for-ttrpgs ; https://arcanumrpgs.com/blog/ai-tools-for-dungeon-masters/ (vendor sources, treat as marketing).
- **Timers that everyone can see teach the game.** Shadowdark's real-time torch has spawned VTT extensions (Owlbear's Dark Torch) that show a countdown to the GM or the whole table. A visible pressure mechanic teaches the loop by itself. Sources: https://extensions.owlbear.rodeo/darktorch ; https://tabletop-thoughts.com/2026/01/09/getting-new-players-gms-up-to-speed-with-shadowdark/

**Evidence quality:** thin. Three small qualitative HCI studies (8, 8 and 71 participants), one self-selected survey, and practitioner writing. No study measures MM cognitive load directly; the educational TTRPG literature only notes that load exists. The design principles below are consistent across all of it, which is the best we can say.

### 4.2 Design principles for the in-session MM toolbox

1. **Two clicks from context, zero typing.** Every procedure is a button on the thing it applies to: React/Morale on an NPC or enemy card, Pressure on the scene bar, Trouble on a roll result, Ask in the header. (CALYPSO's 2.3 turns; C&C's "without interrupting the flow".)
2. **Context-scoped results.** The app knows the current site, scene type, active threats and cast, and filters tables to them, so the MM never picks a table. (CALYPSO: context preservation; Acharya: condensed reference.)
3. **Prompt, not verdict.** Show the result, a one-line interpretation hint, and **Reroll / Defer / Accept**. Accepting logs it; deferring keeps it in a "pending" tray (Necropraxis's deferral).
4. **Private by default, reveal on demand.** Every result goes to the MM first, with a "show the table" option (Foundry's GM-only tables; Rolltable Requester's hidden results).
5. **Everything feeds the log.** Accepted results, revealed secrets, clues found and NPCs created go into the session record. That record then fuels the recap, next session's prep card, the rumor table and the faction turn. The MM never re-types.
6. **MM-owned, editable, importable tables.** Every table is a plain list the MM can edit and extend in the app or import from a simple text/CSV format, and Facet modules can ship tables. That respects the GM's own repertoire (C&C) and the homebrew-first stance. It's one format, and it's human-writable.
7. **Printable parity.** Every table and card prints to a one-page MM sheet. Some GMs find paper faster (the C&C GM with the iPad tracker), and some tables have no screen.
8. **Suggest three, never one.** For moves, complications and "stuck" prompts, offer three filtered options. The MM chooses, which keeps creative agency with them (CALYPSO's low-fi vs hi-fi finding; AW's principle that the MM makes the move).
9. **Builder, not generator, for anything big.** For encounters, sites and factions, the app drafts and the MM edits before play. A finished product handed over mid-session is the donjon trade-off, and it loses the MM's control.
10. **Visible pressure for the table.** Threat Clocks and any pressure/timer the MM chooses to show are visible to players. Seeing the world move is itself information (ICI).

---

## 5. Novice-MM scaffolding

### 5.1 What beginner products do

- **Pathfinder Beginner Box:** the adventure teaches one subsystem per encounter (initiative in the first, then exploration, skill checks, traps). The GM guide then covers terms, duties, adapting a module and, unusually well, how to build your own adventure, backed by a bestiary, random encounter tables and a sample town. The gap reviewers note is the transition to the full game. https://www.sarahdarkmagic.com/content/pathfinder-beginner-box-teaching-new-gms ; https://www.enworld.org/threads/review-pathfinder-beginner-box.661460/
- **D&D Starter Set (Lost Mine of Phandelver):** strong step-by-step coaching for its first scene (marching order, the ambush, tracking), and it teaches responding to player choice. Weaknesses: little guidance beyond combat, linear chapters followed by an unguided sandbox, and (per the Alexandrian's review of the 2022 set) no dungeon-running procedure at all. https://thealexandrian.net/wordpress/49910/roleplaying-games/review-dd-starter-set ; https://www.domainofmanythings.com/blog/i-ran-lost-mines-of-phandelver-is-it-worth-the-hype ; https://slyflourish.com/running_phandelver.html
- **DCC funnel:** each player runs several disposable zero-level peasants through a deadly site. Death is cheap, so learning is cheap, and the survivors become the real characters. But DCC itself assumes an experienced judge and says so, and judges lean on a web generator to make the peasants. https://www.azathought.com/dcc-review/ ; https://dragonpeakpublishing.substack.com/p/the-teaching-adventure
- **Shadowdark:** teach rolls, combat and light first; add other rules only when they come up; the torch timer carries the core loop by itself. https://tabletop-thoughts.com/2026/01/09/getting-new-players-gms-up-to-speed-with-shadowdark/ ; https://www.enworld.org/threads/shadowdark-tips-for-a-new-gm.709758/
- **Mausritter:** the adventure site generator *is* the lesson in site design: history, ruin, inhabitants, goal, secret. Rolling one teaches what a site needs. (§1.15)
- **Lazy DM:** the eight steps give a novice a finite prep list and permission to skip most of it. (§1.7)

### 5.2 Recommendations for Facets

1. **The starter module is the MM tutorial.** Each scene introduces exactly one MM procedure in a boxed "MM move" sidebar, and the app pops the same tip the first time the MM meets that situation: *first scene: reaction roll; second: the 7–9 cost menu; third: morale; fourth: pressure die; fifth: a Threat Clock; sixth: a clue with three routes.* Oraga Night is social-heavy (fun audit §8.2), so the tutorial module should exercise all three pillars, or come as a short companion to Oraga that does.
2. **Ship a dungeon/site procedure in the starter**, which is the specific failure the Alexandrian names in the D&D Starter Set.
3. **Default settings that prevent the three observed novice errors** (fun audit §8.3):
   - *Everything Hard:* the difficulty picker defaults to Standard, and choosing Hard asks for a one-word reason that is shown to players. That's cheap friction in the right direction.
   - *7–9 read as −1:* on a 7–9 the MM panel shows "They succeed. Now pick one cost:" with three options. There's no "penalty" option.
   - *Turn order creeping back:* the fight tracker has no initiative list; it prompts "Who's doing what?" to the whole table, then collects rolls.
4. **A "Stuck?" button.** One click offers three things drawn from the MM's own prep: advance a portent (from the fronts/clocks), bring in an NPC with a want (from the cast or generator), or surface an unrevealed secret (from the prep card). This is Acharya's "what next" prompt, grounded in prep, and it answers the fun audit's "a novice will run out of Movement II" concern for every module rather than one.
5. **A one-page MM loop card**: the procedures in the order they come up (scene → pressure die → encounter → reaction → roll → 7–9 cost / 6− move → morale → loot → XP questions). Print and screen versions.
6. **Pregens with hooks, plus a funnel option.** Pregens carry one-line hooks the app surfaces to the MM for spotlight (C&C's GM P8 kept exactly such a list). A funnel variant (two disposable commoners per player for the first session) teaches lethality and play-to-find-out cheaply. Optional, because our register isn't grimdark.
7. **Graduation path.** Each tutorial tip has a "don't show again". A Settings page lists which procedures are on, so a growing MM can turn on factions, journeys and oracles when ready. This fixes the Beginner Box's missing transition.

---

## 6. How this lines up with what we already have

| Existing | Status in lean view |
|---|---|
| **Trouble Table** (MM5, d6 generic 6− consequences) | Keep as the top level; grow it into per-pillar d66 lists |
| **Threat Clocks** (app, D4) | Keep; add impulse + portent text (fronts) and use them for factions |
| **Enemy conduct fields** (disposition, first_target, triggers, morale, negotiation) | Keep, compressed into WANTS / SPECIAL / ON A MISS / BREAKS |
| **Encounter Recipes / TR budget** | Replace with level-vs-party guidance; drop TR arithmetic |
| **Oraga Night patterns** (agenda cards, omens, redundant trails, rumor table, cast with want/fear/secret, printed Spark rewards, tells→Fractures) | Promote to reusable MM Manual patterns and app objects: omens = pressure-die face 2; redundant trails = three-clue check; cast cards = NPC generator target; tells = monster TELLS line |
| **Sparks, Borrowed Trouble, Graceful Fail** | Untouched. Player-side economy |
| Reaction roll, morale number, pressure die, oracle, loot, site generator, faction turn, prep card, Stuck? | **New** |

---

## 7. Implications for a lean Facets of Origin

Prioritised. Content counts are rough targets for v1; "d66" = 36 entries. Every table ships in the app, prints to a sheet, and is editable/importable in one plain format. All content is original. Borrowed *structures* are credited in an MM Manual acknowledgements page, and any adapted *wording* from CC sources carries the required attribution (Ironsworn, Knave, Mausritter and Lazy GM are CC BY 4.0; DW and Blades CC BY 3.0, pending a GPL-compatibility check; Cairn CC BY-SA 4.0, which is one-way compatible with GPLv3).

### P0: ship with the lean ruleset (the MM's core loop)

1. **Reaction roll.** A 2d6 band table (5 bands aligned to our tiers) plus a **d66 "what they want right now"** table. App: React button on every NPC/enemy. *~41 entries.*
2. **Morale.** One number per monster, standard triggers (first casualty, half down, leader down, lone and hurt), three-tier result (fight / waver / break). App: automatic Morale? chip from the tracker. *1 rule, 3 outcomes, trigger list.*
3. **Pressure die.** A generic 6-face key (encounter, sign, local hazard, cost, opportunity, quiet) + **4 pillar/terrain variants** (underground, wild, settlement, social occasion) × 6 faces, + a per-site "local hazard" slot. App: Pressure button; sign pre-links to its encounter. *~30 entries + per-site 1–3.*
4. **MM moves / complication tables.** Keep the d6 Trouble Table as the index; add **one d66 complication table per pillar**: fight, exploration, social, magic (magic covers the cost on a 7–9 casting and trouble on a 6−). Each entry is a one-line soft/hard move with an example. App: three filtered suggestions on every 6− and a "pick a cost" menu on every 7–9. *4 × 36 = 144 entries.*
5. **Lean monster card** (§2.2): level, HP, armour, damage, morale, WANTS, SPECIAL, ON A MISS, TELLS, BREAKS, TWISTS d6, optional NASTIER. Migrate the 18 existing creatures; target **40–60 in the lean Bestiary**, each with a **d6 twist table** (*240–360 twist lines*). App: card view with React/Morale buttons; level auto-derives the numbers.
6. **Loot generator.** **d66 trinkets** (flavour), **d66 curios** (one-use, carry limit 3), **d20 relics** (strange power + quirk + optional want), coin by site level. App: Hoard button, drag into inventory. *~92 entries.*
7. **NPC card generator.** **d66 names × 3 cultures** (Shattered Origin cultures need an owner decision: *don't invent canon*; ship setting-neutral lists first), **d66 visible traits**, **d66 wants**, **d36 secrets/fears**, plus the persuasion difficulty. App: New NPC → card → lock into cast. *~250 entries.*
8. **2d6 oracle.** Odds modifiers, three-tier answer with naturals as "and", plus **d66 action × d66 theme** prompt pair. App: Ask button. *~72 prompt words.* (Ironsworn's CC BY 4.0 oracles are a licensed fallback if we want more.)
9. **Novice defaults** (§5.2.3): Standard default difficulty, 7–9 cost menu, no initiative list. *Software only.*

### P1: first expansion (world motion and prep)

10. **Session prep card** (Lazy-DM-style): strong start, **10 secrets** with reveal tracking and carry-forward, cast shortlist, 3 locations × 3 features, monsters, rewards. App: prep screen and side panel.
11. **Three-clue checker** for investigations: conclusions ↔ clues graph with a warning below three; in-play tick-off. Pairs with 10.
12. **Threats (fronts) on Threat Clocks**: impulse, 3–6 named portents as clock segments, impending doom, 1–3 stakes questions. **12 sample threats** across the three pillars. Idle-scene reminder.
13. **Stuck? button** (§5.2.4). Draws from 10–12. *Software only.*
14. **Faction turn (lean)**: faction = name, impulse, goal clock, rival; between-session 2d6 roll per faction writes headlines. **6 sample factions** (setting-neutral until the owner rules on Shattered Origin factions).
15. **Rumor tables** as first-class objects: **d6–d12 per site/region**, written into by factions and clocks, true/false flag, "who heard it" tracking.
16. **Site generator**: **d20 former purpose, d12 ruin cause, d20 current inhabitants, d12 inhabitant goal, d20 secret, d66 room + feature**; produces 6–12 room nodes with a pressure die, rumors, two clues to the secret, one hoard. *~120 entries.*
17. **Journey procedure**: legs, three journey roles each with one 2d6 roll, pressure die per leg, **d12 discoveries + d12 dangers per terrain** (4 terrains ≈ 96 entries), weather d6.
18. **Tutorial layer**: in-app first-time tips that mirror the starter module's MM-move sidebars; Settings toggles for each procedure.

### P2: later, only after a human table has played P0

19. **Optional AI assist**, constrained to the campaign's own log and tables: "suggest 3" for a move, NPC line or room description; low-fi (bullets) and hi-fi (read-aloud) modes; one-turn use. Never generates canon into the setting files without MM acceptance (the project's iron law against invented lore applies to the tool too).
20. **Solo/duo mode** packaging the oracle, pressure die and site generator for play without an MM (Ironsworn/Mythic lesson): a marketing hook as well as a design test harness.
21. **Seasonal/home-base layer** (Stonetop): a shared "home" object whose state biases the tables. Only if the campaign mode wants it.

### Rough total for P0

About 600–800 table entries plus 40–60 monster cards. That's a sizeable writing job, comparable to a single adventure module, but every entry is reusable across every session and every module. It's where the complexity audit says the words saved from the player side should go. Order of writing: complication tables (4) and reaction/morale first, because they fix the novice failures the fun audit observed; then monsters and loot; then generators.

### Decisions this hands to the owner

- Whether XP is paid for treasure brought home or spent on goals (treasure-as-XP), alongside the discovery/goal questions.
- Whether relics may give Body characters access to magic through an item (§3.2) or whether "Body gets no magic" extends to items.
- Which Shattered Origin cultures, factions and names may appear in shipped generator tables. Until ruled, ship setting-neutral lists.
- Whether monster specials trigger on player misses (no MM currency) or on a Fear/Malice-style pool.

---

## Bibliography (grouped)

**Procedures:** Necropraxis, overloaded encounter die: https://necropraxis.com/2014/02/03/overloading-the-encounter-die/ · Prismatic Wasteland, overloading the table: https://www.prismaticwasteland.com/blog/overloading-the-random-encounter-table · Ten Foot Polemic, gimmick tables: http://tenfootpolemic.blogspot.com/2017/08/improving-your-encounter-tables-with.html · Peril system: https://wasitlikely.blogspot.com/2019/07/the-peril-system-overloaded-encounter.html · Escalating encounter die: https://theadventuringday.wordpress.com/2021/04/05/pointcrawls-applied-the-escalating-encounter-die/ · Alexandrian Three Clue Rule: https://thealexandrian.net/wordpress/1118/roleplaying-games/three-clue-rule · corollaries: https://thealexandrian.net/wordpress/1105/roleplaying-games/three-clue-rule-part-4-corollaries · two types of leads: https://thealexandrian.net/wordpress/50095/roleplaying-games/running-mysteries-the-two-types-of-leads · Node-based design: https://thealexandrian.net/wordpress/8122/roleplaying-games/node-based-scenario-design-collectors-edition · Hexcrawl encounter tables: https://thealexandrian.net/wordpress/17333/roleplaying-games/hexcrawl-part-4-encounter-tables · Hexcrawl at the table: https://thealexandrian.net/wordpress/17464/roleplaying-games/hexcrawl-part-12-at-the-table · special encounter tables: https://thealexandrian.net/wordpress/48697/roleplaying-games/hexcrawl-addendum-special-encounter-tables · 5E hex exploration: https://thealexandrian.net/wordpress/48033/roleplaying-games/5e-hexcrawl-part-7-hex-exploration · Alexandrian on clocks: https://thealexandrian.net/wordpress/40424/roleplaying-games/blades-in-the-dark-progress-clocks · Sly Flourish eight steps: https://slyflourish.com/eight_steps_2023.html · at the table: https://slyflourish.com/using_the_8_steps_at_the_table.html · choosing steps: https://slyflourish.com/choosing_the_right_steps.html · Lazy GM Resource Document (CC BY 4.0): https://slyflourish.com/lazy_gm_resource_document.html · Looking back on fronts: https://slyflourish.com/looking_back_on_fronts.html · Nastier specials in D&D: https://slyflourish.com/nastier_specials.html · DW SRD fronts: https://www.dungeonworldsrd.com/gamemastering/fronts/ · DW moves: https://www.dungeonworldsrd.com/moves/ · DW licence: https://acodispo.github.io/Dungeon-World-HTML-SRD/license/ · AW agenda/principles: https://gnomestew.com/the-gms-agenda-and-principles/ · http://www.diceexploder.com/blog/2024/4/10/more-on-apocalyptic-principles · Blades clocks: https://bladesinthedark.com/progress-clocks · Blades licensing: https://bladesinthedark.com/licensing · Ironsworn Ask the Oracle: https://ironsworn-rpg.fandom.com/wiki/Ask_the_Oracle · Tomkin Press licensing: https://tomkinpress.com/pages/licensing · Mythic GME: https://www.wordmillgames.com/page/mythic-gme.html · Mythic review: https://glyphngrok.substack.com/p/review-mythic-game-master-emulator · ICI doctrine: https://www.bastionland.com/2018/09/the-ici-doctrine-information-choice.html · Angry GM, encounters: https://theangrygm.com/four-things-youve-never-heard-of-that-make-encounters-not-suck/ · https://theangrygm.com/how-to-build-awesome-encounters/ · random encounters redesigned: https://theangrygm.com/redesigning-random-encounters-2/ · Reaction rolls: https://eucatastrophic.bearblog.dev/unpacking-reaction-rolls/ · http://osrsimulacrum.blogspot.com/2020/09/across-editions-reaction-table.html · https://dicegoblin.blog/the-two-tiered-reaction-roll/ · http://methodsetmadness.blogspot.com/2023/05/reaction-rolls-in-practice-osr.html · Knave (CC BY 4.0): https://questingbeast.itch.io/knave · WWN free edition: https://www.drivethrurpg.com/en/product/348809/worlds-without-number-free-edition · WWN factions: https://grokipedia.com/page/Factions_Worlds_Without_Number · https://glyphngrok.substack.com/p/creating-factions-in-an-open-world · Perilous Wilds reviews: https://save.vs.totalpartykill.ca/review/the-perilous-wilds/ · https://seedofworlds.blogspot.com/2022/09/review-perilous-wilds.html · Stonetop: https://stonetop-wiki.github.io/ · https://indiegamereadingclub.com/indie-game-reading-club/deep-dive-stonetop/ · Brindlewood Bay: https://thealexandrian.net/wordpress/47226/roleplaying-games/review-brindlewood-bay · https://www.domainofmanythings.com/blog/what-do-you-think-happened-a-plug-and-play-mystery-mechanic-from-brindlewood

**Monsters:** DW monsters: https://www.dungeonworldsrd.com/monsters/ · Cairn SRD (CC BY-SA 4.0): https://cairnrpg.com/first-edition/cairn-srd/ · Cairn creating monsters: https://cairnrpg.com/second-edition/wardens-guide/creating-monsters/ · Mausritter (CC BY 4.0): https://mausritter.com/ · https://mausritter.com/adventure-site/ · The Black Hack: https://the-black-hack.jehaisleprintemps.net/english/ · 13th Age SRD monsters: https://www.13thagesrd.com/monsters/ · Daggerheart adversaries: https://daggerheartsrd.com/rules/adversaries/ · https://daggerheart.org/gm/core-gm-mechanics · Draw Steel: https://www.mcdmproductions.com/draw-steel-resources · Shadowdark stat format: https://www.enworld.org/threads/lets-make-shadowdark-monsters.713537/ · ICRPG: https://www.creativegamelife.com/index-card-rpg-master-edition-guide · Monster Overhaul: https://coinsandscrolls.blogspot.com/2023/02/osr-monster-overhaul-megapost.html · McDowall on monsters: https://www.bastionland.com/2009/04/brief-thoughts-on-monster-design.html · https://www.bastionland.com/2020/01/inverted-monsters.html · https://bastionland.substack.com/p/creating-creatures

**Loot:** Treasure Overhaul: https://coinsandscrolls.blogspot.com/2024/01/osr-treasure-overhaul.html · Cyphers: https://numenera.fandom.com/wiki/Cyphers · Decyphered: https://pretendo.games/2019/06/02/decyphered-simplified-house-rules-for-numenera-the-strange/ · Into the Odd: https://en.wikipedia.org/wiki/Into_the_Odd · https://www.rpg.net/reviews/archive/19/19108.phtml · Knave 2e analysis: https://rancourt.substack.com/p/analysis-knave-2e · Treasure-as-XP: https://princeofnothingblogs.wordpress.com/2023/02/16/on-treasure-pt-i/ · http://dreamsinthelichhouse.blogspot.com/2015/03/campaign-treasure-osr-vs-5e.html · https://osrdread.blogspot.com/2019/11/osr-gold-as-xp-12-theory.html · https://www.realmbuilderguy.com/2025/11/treasure-xp-and-player-choice.html · https://kateplays.substack.com/p/xp-for-gold

**Digital tools and research:** CALYPSO: https://arxiv.org/abs/2308.07540 · Readymades & Repertoires: https://dl.acm.org/doi/fullHtml/10.1145/3527927.3532798 · Acharya et al. ICIDS 2021: https://eis.ucsc.edu/papers/Acharya_ICIDS2021.pdf · DiGRA requirements paper: https://dl.digra.org/index.php/dl/article/view/1310 · Acharya thesis: https://escholarship.org/uc/item/7db84255 · Sly Flourish 2016 DM survey: https://slyflourish.com/2016_dm_survey_results.html · Kobold+ Fight Club: https://gmhub.roll20.net/resources/kobold-plus-fight-club/ · encounter generators compared: https://twodollardm.com/blog/best-free-encounter-generators-2026 · Foundry roll tables: https://foundryvtt.com/article/roll-tables/ · GM Screen: https://foundryvtt.com/packages/gm-screen · Better Rolltables: https://foundryvtt.com/packages/better-rolltables/ · Rolltable Requester: https://foundryvtt.com/packages/rolltable-requester · Chartopia: https://chartopia.d12dev.com/ · Table format wars: https://necropraxis.com/2018/07/22/random-table-format-wars/ · Building generators: https://www.randroll.com/building-rpg-random-generators/ · Dark Torch: https://extensions.owlbear.rodeo/darktorch · AI assistants: https://www.myarchivist.ai/ai-dungeon-master/ai-tools-for-ttrpgs · https://arcanumrpgs.com/blog/ai-tools-for-dungeon-masters/

**Novice scaffolding:** Pathfinder Beginner Box: https://www.sarahdarkmagic.com/content/pathfinder-beginner-box-teaching-new-gms · https://www.enworld.org/threads/review-pathfinder-beginner-box.661460/ · D&D Starter Set: https://thealexandrian.net/wordpress/49910/roleplaying-games/review-dd-starter-set · https://www.domainofmanythings.com/blog/i-ran-lost-mines-of-phandelver-is-it-worth-the-hype · https://slyflourish.com/running_phandelver.html · DCC funnel: https://www.azathought.com/dcc-review/ · https://dragonpeakpublishing.substack.com/p/the-teaching-adventure · Shadowdark onboarding: https://tabletop-thoughts.com/2026/01/09/getting-new-players-gms-up-to-speed-with-shadowdark/ · https://www.enworld.org/threads/shadowdark-tips-for-a-new-gm.709758/
