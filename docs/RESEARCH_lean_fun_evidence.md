# RESEARCH: What Makes a Light Fantasy RPG Fun, and What Simplicity Costs

**Date:** 2026-09-25
**Tier:** Brain-support research (run as a subagent). Informs the owner's clean-sheet question in `RESEARCH_complexity_audit.md` §7.
**Question:** What does the evidence say makes a light fantasy RPG fun for every player type? Why are D&D's familiar primitives (HP, damage dice, levels, loot, named spells, classes) fun as well as familiar? What does rules-light design put at risk?
**Owner constraints (arrived mid-task):** (1) Keep **Body / Mind / Soul** as broad parent Facets, each containing several concrete classes. (2) Model it on **Morrowind**: a Facet works like Morrowind's specialization (Combat/Magic/Stealth). A player may define a custom class inside a Facet, and preset classes are suggested builds.
**Read first:** `RESEARCH_complexity_audit.md` (whole file, including §7 "Lean Facets"), `RESEARCH_fun_audit_2026-09.md` §2/§4/§7, `research/dice_system_analysis.md`.

**Evidence grades used throughout**
- **E**: Empirical. Peer-reviewed or controlled study, or large platform telemetry.
- **S**: Survey or poll. Self-selected, but it has a sample size.
- **D**: Designer statement or publisher data release.
- **A**: Anecdote. A review, forum consensus, or blog.

**Copyright:** every summary below is in my own words. Quotes are short and attributed, and no rules text is reproduced. Morrowind and the other games appear only as design concepts.

**Method limits.** Quantic Foundry's pages returned HTTP 403, so its figures come from search-indexed abstracts. The session's web-search budget ran out partway through, and the last findings came from fetching known URLs. There is **no retention study** that compares rules-light with rules-heavy games for new players (see §3.4). Every poll is self-selected, and most are drawn from D&D-centric forums.

---

## Summary

1. **Social connection is the biggest single reason people play and keep playing.** The evidence here is empirical. Belonging to a D&D group predicts wellbeing and self-esteem (n=305). The design corollary comes from Quantic Foundry's board-game data: people who come mainly for social fun also prefer accessible, easy-to-teach games. So *light rules serve the most common motive*. They serve it as long as the game still hands out wins (competence) and choices (autonomy), which self-determination theory ties to enjoyment. (§1)
2. **HP, damage dice, levels and loot are not just familiar. Each one feeds a measured motive.** Power (a strong character with strong gear), Completion, and competence feedback all come through these primitives. The field's most successful recent light game, **Shadowdark**, kept all of them and cut everything around them. Its first two Kickstarters raised about $1.3M and then about $3M. (§2)
3. **What players reach for is simple combat and rich options outside it.** In Mearls' account of WotC survey data, the favourite classes had "the most simple combat options but the most complex options out of combat." That is almost exactly the Facets thesis. (§2.1)
4. **Most campaigns are short and low-level.** In D&D Beyond data, about 61% of characters sit at levels 1–5 and about 90% of games never pass level 10. In an OSR survey the median "longest campaign" was 24 sessions. **Design for 10 levels over roughly 20–25 sessions, and front-load the dings.** (§4)
5. **Advancement: players prefer the MM calling level-ups to XP bookkeeping, about 3:1** (Sly Flourish, n≈6,000, two polls). Of the level-up designs studied, meaningful *picks* (background feat at level 1 scored 87–90% in WotC's survey; subclass at level 3) beat random or small-number bumps. Shadowdark's random talents raise anticipation but draw "dull +2s" criticism. (§4)
6. **Removing advancement costs you the Power Gamer.** Cairn's own FAQ prefers "growth over advancement". Reviewers call the result anticlimactic, and one essayist argues that long rules-light campaigns need *something* heavy. (§4.3)
7. **Custom classes are fine *if presets are the default*.** Choice overload averages out to about zero across 50 experiments, but it grows with *preference uncertainty*, and that describes a new player exactly. When Bethesda watched players pick a class upfront, they regretted it about three hours later and restarted. Only 11% of D&D Beyond characters multiclass. **Presets for session one, with custom definition as an opt-in, and the defining commitment after 2–3 sessions.** (§4.4)
8. **Morrowind's *specialization* concept is sound. Its *use-based levelling* is the known failure.** Players gamed its skill-increase multipliers and held back skills to avoid "wasting" them. That is the same incentive flaw the complexity audit found in our marks-for-used-skills. Take the specialization idea and leave the use-tally behind. (§4.5)
9. **Combat: tables say they want far less than they play.** In a Sly Flourish poll only 18% named combat their favourite pillar, yet an EN World poll puts the median table's combat share at 51–60% of the session. Short fights feel meaningful when each exchange changes the fiction (the Dungeon World 2 designers' own post-mortem), and lethality is set by table culture more than by rules (OSR survey n=200). (§5)
10. **Fellowship mechanics fail when they depend on someone remembering them.** 5e Inspiration is widely reported as forgotten by DMs and players alike. Dungeon World bonds divide tables. What works is externally facing, actionable, and *visible*, which is a job the app can do. (§6)

---

## 1. Player motivation research

### 1.1 Findings

| Finding | Grade | Source |
|---|---|---|
| **Self-determination theory in games.** Across four studies and seven games, felt **autonomy and competence** predicted enjoyment, wanting to play again, and short-term gains in mood and self-esteem. **Relatedness** added to this in the multiplayer study. This work became the PENS measure. | **E** | Ryan, Rigby & Przybylski 2006, https://selfdeterminationtheory.org/SDT/documents/2006_RyanRigbyPrzybylski_MandE.pdf ; PENS: https://selfdeterminationtheory.org/player-experience-of-needs-satisfaction-pens/ |
| **TTRPG belonging and wellbeing.** A stronger sense of belonging to a D&D group correlates with wellbeing and self-esteem. D&D groups were rated "among the most positive and supportive groups" in players' social networks, even though players spend less time with them than with family. n=305, NZ online community, *J. Community & Applied Social Psychology* 2026. | **E** (cross-sectional) | https://phys.org/news/2026-09-dungeons-dragons.html |
| A UCC study of frequent players found they valued a sense of control, creative co-authorship and camaraderie (*Int. J. of Role-Playing*, 2024). | **E** (qualitative) | https://www.ucc.ie/en/news/2024/playing-dungeons-and-dragons-can-support-mental-health-.html |
| A registered pilot that used offline D&D found reduced social anxiety and less problematic online gaming. A 2024 scoping review surveys TTRPGs as interventions. | **E** (small n) | https://royalsocietypublishing.org/rsos/article/12/4/250273/235815/ ; https://www.tandfonline.com/doi/full/10.2147/PRBM.S466664 |
| **Quantic Foundry video-game model** (400k+ respondents): 12 motivations in 6 pairs, among them **Power** (powerful character, powerful equipment), **Completion**, **Fantasy/Story** (immersion), **Destruction/Excitement** (action), **Challenge/Strategy** (mastery), and **Design/Discovery** (creativity). | **S** (very large) | https://www.gdcvault.com/play/1026464/A-Deep-Dive-into-the ; https://quanticfoundry.com/gamer-motivation-model/ |
| **Quantic Foundry board-game model** (40k+): people who care most about **Social Fun** also score high on **Accessibility** (easy to learn and teach). The other clusters are Conflict, Strategy and Immersion. Accessibility and Social Fun are the most common primary motives among women. | **S** (large) | https://quanticfoundry.com/2016/09/21/board-game-profile-v2/ ; https://quanticfoundry.com/wp-content/uploads/2017/01/Board-Game-Motivation-Model-Overview.pdf |
| **Robin Laws' seven types** (Power Gamer, Butt-Kicker, Tactician, Specialist, Method Actor, Storyteller, Casual Gamer). This is theory, but it is the hobby's most durable typology. | **D** | https://www.darkshire.net/jhkim/rpg/theory/models/robinslaws.html ; https://www.enworld.org/threads/robin-d-laws-the-7-gamer-types.318457/ |
| **Bartle** (Achievers, Explorers, Socialisers, Killers). Derived from MUD players and only partly empirical. The recurring cross-model finding is three themes: mastery/competition, immersion/exploration, and social. | **D** | https://mud.co.uk/richard/hcds.htm ; https://www.skeletoncodemachine.com/p/what-type-of-gamer-are-you |
| **Flow, near-miss, cognitive load and pre-roll agency.** These are already synthesised in `research/dice_system_analysis.md` (Csikszentmihalyi, Sweller, Green & Brock, Ladouceur & Sévigny). Their load-bearing claim for this file: a new player holds about 4 novel chunks, and each extra modifier to calculate pulls them out of the fiction. | **E** (general psych) | see that file's Sources |

### 1.2 What this means

- **Fun is plural, so a lean game has to cover every motive with *minimal* mechanics rather than cover one motive well.** Self-determination theory says every player needs some competence (visible wins, growth), some autonomy (real choices), and relatedness (the table). The typologies tell you *which flavour* of each a given player wants.
- **The social motive is the modal one, and it rewards accessibility.** That is the empirical case for going lean. Nothing here, though, says social players want *no* crunch. The Quantic Foundry data says they want crunch that is easy to *teach*.
- **The Power motive explicitly includes equipment.** That is a direct empirical hook for loot (§2.4), which the current game lacks entirely.

---

## 2. Why D&D's primitives are fun, and not just familiar

### 2.1 Evidence

| Finding | Grade | Source |
|---|---|---|
| **Simple in combat, rich out of it.** Mearls, citing WotC survey data: the favourite classes had "the most simple combat options but the most complex options out of combat". New players pick classes that "sound cool" rather than optimising. | **D** (citing internal survey) | https://slyflourish.com/three_years_with_5e_with_mearls.html |
| **Fighter is the most played class in every tier**, with Rogue second (D&D Beyond telemetry across millions of characters). The simplest *mechanical* class is the most chosen, so a plain "hit things well" option is not a niche. | **E** (telemetry, includes unplayed builds) | https://www.enworld.org/threads/90-of-d-d-games-stop-by-level-10-wizards-more-popular-at-higher-levels.666097/ ; https://www.belloflostsouls.net/2020/07/dd-and-the-most-popular-class-is.html |
| **Background feat at level 1** was the top-scoring item in the first One D&D survey (87–90%, 39k completions). WotC counts ≥70% as a pass and ≥80% as "keep exactly". The d20-Test rule glossary was one of only three items in the 60s. | **S/D** (very large) | https://www.enworld.org/threads/wotc-on-one-d-d-playtest-survey-results-nearly-everything-scored-80.693544/ ; https://www.wargamer.com/dnd/one-dnd-playtest-satisfaction-scores |
| **Class identity through distinctive mechanics.** In Playtest 5, Wizards scored only 70% when spell lists were shared, because players felt the shared list diluted identity. Warlock lost Pact Magic and scored so poorly the number wasn't published. Weapon Mastery, which gives martial characters one cheap signature option, scored 80%. | **S/D** | https://mike.pirnat.com/2023/08/one-dd-playtest-5-survey-results/ |
| **Shadowdark's success**: Kickstarter 1 raised about $1.3M from 12k+ backers (2023), and *Western Reaches* raised about $3M. Dionne describes it as "fifty years of D&D design" distilled into "two pages of core rules", approachable from 5e and recognisable to old-schoolers. It keeps HP, damage dice, levels 1–10, classes, named spells and XP-for-treasure. Timing helped: it came out during the OGL crisis. | **D** + sales | https://www.enworld.org/threads/shadowdark-rpg-an-interview-with-kelsey-dionne.696487/ ; https://ttrpgfans.com/shadowdark-the-western-reaches/ ; https://www.forbes.com/sites/robwieland/2025/03/19/shadowdarks-second-million-dollar-kickstarer-creates-a-full-setting/ |
| **Daggerheart**: released 20 May 2025, sold out in about two weeks against a year's forecast, and won Gold ENNIEs for Best Game and Best Rules. The criticism is mostly about *tracking load* (Hope, Stress, HP, Armor, gold, class currencies) and "too chunky" for narrative players. It is a D&D-shaped game with HP thresholds, classes, subclasses at level 1 and domain cards. | **D** + sales, **A** reviews | https://www.enworld.org/threads/daggerheart-sold-out-in-two-weeks-has-three-year-plan-in-place.716975/ ; https://www.thepopverse.com/gaming-critical-role-daggerheart-campaign-books-darrington-press-ed-lopez-ben-van-der-fluit ; https://www.enworld.org/threads/daggerheart-review-the-duality-of-robust-combat-mechanics-and-freeform-narrative.713471/ |
| **Pathfinder and 3.5 compatibility.** The legend that "Pathfinder outsold 4e" rests on partial ICv2 store data. Staff from both companies say 4e outsold it by a large factor. The *real* lesson is narrower: enough players preferred the familiar 3.5 chassis to keep Paizo's line going for a decade. | **D** | https://alphastream.org/index.php/2023/07/08/pathfinder-never-outsold-4e-dd-icymi/ ; https://www.rpg.net/columns/designers-and-dragons/designers-and-dragons10.phtml |
| **Loot and variable reward.** Unpredictable reward schedules produce the most persistent engagement. Diablo-style drops are the textbook game case. This is a well-established behavioural principle (and the one loot boxes abuse). | **E** (general) / **A** (game application) | https://www.futurelearn.com/info/courses/game-psychology/0/steps/428456 ; https://arxiv.org/pdf/2307.04549 |
| **Crits, big dice and the social near-miss.** Shared witness amplifies the emotional peak (Lazzaro's "people fun"), and flashbulb memories come from public, high-stakes rolls. See `research/dice_system_analysis.md`. | **E** (general) | see that file |

### 2.2 What this means, primitive by primitive

- **HP** is one number going down. It is the cheapest possible durability model, and every audience in the market already knows it. Its fun is *attrition you can see*, which makes decisions like "do I push on?" legible. The complexity audit's point stands: HP was never the heavy part of old D&D.
- **Damage dice** give the Butt-Kicker a big-number moment on every hit and scale the Power fantasy (d4 dagger → d12 greataxe) with no rules text. Their weakness is the one DW2's designers name: "damage alone" does not change the fiction enough (§5). **Pair a damage die with a fictional outcome, never damage alone.**
- **Levels** deliver the "ding": a discrete, public, celebrated competence signal (self-determination theory). Removing them removes the Power Gamer's main reward (§4.3).
- **Loot** serves Power (equipment), Completion and Discovery at once, and it is pure MM-side variety. It is the cheapest carry-forward reward available.
- **Spells by name** carry identity ("my fireball"). The One D&D survey shows players *punish* attempts to homogenise lists. Our domain magic has no list, which is a real differentiator, but it has to give players *named signature workings* to carry that identity (see §7).
- **Classes** give instant identity, niche protection and a short menu (the Fighter's dominance shows how much a clear "shape" is worth). The owner's Facet→class model keeps that benefit (§4.4).

---

## 3. Complexity and onboarding

### 3.1 Findings

| Finding | Grade | Source |
|---|---|---|
| **Choice overload is real only under certain conditions.** A meta-analysis of 50 experiments (N=5,036) found a mean effect of about zero, with large variance. A later meta-analysis identifies **choice-set complexity, task difficulty, preference uncertainty and decision goal** as the moderators. A new player at character creation has high preference uncertainty, which is exactly where overload bites. | **E** | https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf ; https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf |
| **Upfront commitment before understanding causes regret.** In Oblivion, players picked a class after about 30 minutes and about 3 hours later decided "I picked the wrong skills" and restarted. Skyrim removed the class question. | **D** (telemetry-informed) | https://gamerant.com/elder-scrolls-5-skyrim-character-classes-removed/ |
| WotC moved **every subclass choice to level 3** in 2024 (Cleric had been level 1) so players experience the class first, with subclass features at 3/6/10/14. | **D** | https://comicbook.com/gaming/news/dungeons-dragons-subclasses-3rd-level-2024-core-rulebooks/ ; https://www.cbr.com/dnd-5e-2024-players-handbook-jeremy-crawford-interview/ |
| **Templates for newcomers.** The GURPS *Dungeon Fantasy RPG* was "built to bring in new gamers first". It swapped point-buy for templates and cut "newbie-scaring rules". | **D** | https://gamingballistic.com/2016/09/07/dungeon-fantasy-boxed-set-word-of-kro/ |
| **Pregens are coming back**, and character-creation "homework" is described as a barrier. | **A** | https://grinningrat.substack.com/p/the-future-of-rpgs-is-pregenerated |
| Cypher's one-sentence character ("an *Adjective Noun* who *Verbs*") can be built in about 10 minutes from long menus, because the menu is structured as a sentence. | **A/D** | https://startplaying.games/blog/posts/how-to-make-cypher-system-character-ten-minutes |
| Knave is laid out so each two-page spread works as a "control panel" (a DM-screen panel). | **D** | https://dreamingdragonslayer.wordpress.com/2020/03/30/ben-milton-interview-part-ii-questing-beast-maze-knights-and-osr/ |
| **The biggest barrier to entry is finding a group, not the rules.** WotC's product response has been group-finding (the D&D Beyond event finder, StartPlaying). Players have DMed at roughly 15–20% rates, and player-seeking posts outnumber GM-seeking ones about 5:1 on r/lfg. The second figure comes from a vendor blog, so it is weak evidence. | **D / A** | https://dungeonsanddragonsfan.com/dnd-beyond-group-finding-features/ ; https://aidungeonmaster.ai/blog/dm-shortage-data/ |
| **The rules-light GM-burden argument.** Without mechanics to lean on, "that lands on the GM", who is then "more prone to burning out". | **A** (designer essay) | https://irregularshapes.substack.com/p/prevent-burnout-with-crunchy-bits |
| **Dungeon World criticisms**: the GM must "work very hard" to fill gaps. Combat collapses into repeating one move until the monster falls. Terminology ("hold", "+1 forward") sends newcomers to the index. | **A** | https://mythcreants.com/blog/dungeon-world-is-a-game-to-skip/ |
| **Bounded accuracy** (5e): flat DCs and flat accuracy let low-level threats stay relevant and spare the DM scaling tables. It is a *simplicity-for-the-referee* principle. | **D/A** | https://olddungeonmaster.com/2014/08/30/bounded-accuracy/ |

### 3.2 The sweet spot

The evidence converges on this: **simplicity for new players comes from few decisions at the start and familiar primitives, not from fewer mechanics overall.** GURPS, Skyrim and the 2024 PHB each fixed onboarding by *deferring or pre-packaging* choice, not by deleting depth.

### 3.3 Where going lighter risks losing fun

The risk is not "too few rules for players". It is **(a) the GM carrying everything** (DW, the burnout essay, and this repo's own fun-audit finding that the fun is "almost entirely supplied by the Mirror Master") and **(b) repetitive combat** once the one attack move is the only move. Both are answered by *MM-side procedure plus app tooling* (monster gimmicks, tables, clocks), not by adding player rules.

### 3.4 Evidence gap

I found **no study** that measures retention by rules complexity for tabletop newcomers. The "three-session rule" in `dice_system_analysis.md` comes from cognitive-load theory by analogy, not from a tabletop study. Treat the complexity→retention claim as plausible, not proven. **The human playtest (fun audit R1) is the only way to close this gap.**

---

## 4. Progression design

### 4.1 Findings

| Finding | Grade | Source |
|---|---|---|
| **Where characters sit** (D&D Beyond, reported Dec 2019): L1 11%, L2 9%, L3 15%, L4 12%, L5 14%, L6 9%, L7 7%, L8 6%, L9–10 4% each, L11–12 2% each, L13–15 1% each, L20 2%. So **about 61% are at L1–5 and about 90% of games stop by L10**. The source article's claim that "60% reach 7+" is arithmetically wrong; the real figure is about 31%. Caveat: the data includes builds that were never played. | **E** (telemetry, noisy) | https://www.thegamer.com/dungeons-dragons-player-level-campaign-statistics/ ; https://www.enworld.org/threads/90-of-d-d-games-stop-by-level-10-wizards-more-popular-at-higher-levels.666097/ |
| **Campaign length**: in an OSR survey of *longest* campaigns (n=200), the mean was 45 sessions and the median **24**. Sly Flourish runs about 50 three-hour sessions over 12–14 months. Most sessions last 2–4 hours (n=2,152). | **S** | https://valerialoves.com/how-deadly-is-the-osr-actually/ ; https://slyflourish.com/lack_of_satisfying_conclusions.html ; https://slyflourish.com/facebook_surveys.html |
| **Pacing**: the 5e DMG assumes about 2.5 sessions per level. In an EN World thread, most posters wanted *slower* (3–6 sessions per level mid-tier), while tier 1 at 1–2 sessions per level is common. One group reported about 1 session per level for levels 2–4, then about 2.5. Players need time to "grasp" new abilities. | **A** (forum) | https://www.enworld.org/threads/5e-recommended-2-5-sessions-level-rate.660373/ ; https://www.enworld.org/threads/how-often-should-pcs-level-up.484883/ |
| **Milestone vs XP**: Feb 2020 (n=6,009): milestone 66%, XP 21%, per-session 10%. May 2022 (n=6,008): "DM decides" 69%, XP 15%, DMG milestone 14%. | **S** (large) | https://slyflourish.com/facebook_surveys.html |
| **Shadowdark random talents** (roll 2d6 at level 1 and each odd level) are praised for variety between same-class characters and for anticipation ("snake eyes" wand moments), and for removing "dead levels". A 6/10 review calls the talents "dull and unimaginative", mostly numeric bumps. XP comes from treasure on a coarse scale (a normal find 1 XP, a hoard 3). | **A** | http://dreamsinthelichhouse.blogspot.com/2025/01/shadowdark-good-bad-ugly.html ; https://scholomance.substack.com/p/tabletop-review-shadowdark-rpg-by |
| **The meaningful-choice moments that score best**: a level-1 background feat (87–90%) and a signature martial option (Weapon Mastery, 80%). | **S/D** | §2 sources |
| **Growth without numbers**: Cairn prefers "growth over advancement". A reviewer says progression eventually "purely relies on gear" and that players used to power curves "might find it anticlimactic". A design essay argues that a long rules-light campaign needs "an aspect of play which is heavy". | **D / A** | https://cairnrpg.com/first-edition/frequently-asked-questions/ ; https://intoindiegames.com/walkthroughs/tips-tricks/a-beginners-guide-to-cairn/ ; https://monstersandmanuals.blogspot.com/2024/12/the-fiction-becomes-system-for.html |

### 4.2 Horizontal vs vertical

5e's bounded accuracy is vertical growth held in check. Shadowdark is vertical (HP, talents) with a hard cap at 10. Cairn is horizontal-only. The Power Gamer needs *some* vertical signal: numbers that go up (HP, damage, a bonus). Specialists and Method Actors are served by horizontal *new verbs* (a technique, a signature working). **A lean game should give both on each level: one small number and one new thing to do or know.**

### 4.3 What players say they miss

Where levels are missing, the complaint is always the same: no *moment*. Nothing to celebrate, nothing to plan toward, and gear becomes the only growth. Where levels come slowly, players forget new abilities before they use them (this argues against *fast* mid-tier levels), and early levels drag (this argues for fast tier 1).

### 4.4 Class count, archetype identity and subclass timing (owner's Facet→class constraint)

| Evidence | Grade | Source |
|---|---|---|
| 5e has 12–13 classes, but Fighter and Rogue lead every tier. The classes below the top 10 sit within about 1% of each other. | **E** | https://www.belloflostsouls.net/2020/07/dd-and-the-most-popular-class-is.html |
| **Only 11% of D&D Beyond characters at level 2+ multiclass** (27% at level 20). Most players stay in the preset shape even when a custom build is on offer. The minority who customise do it late. | **E** (telemetry) | https://www.enworld.org/threads/whos-multiclassing-with-who-more-d-d-beyond-stats.666122/ |
| **PF2e's Free Archetype** (a second, customisable track on top of the class) is by far the most-used variant. About 45% of posters in a Paizo thread said they use it. Reasons given: characters "come online sooner", with less pressure to give up concept for party needs. | **S** (thread, self-selected) | https://paizo.com/threads/rzs433wo&page=2 |
| **Dungeon World** has 8 playbooks, each one per party. Niche protection is one rule, and the playbook is a single sheet with everything on it. | **D/A** | http://thehopelessgamer.blogspot.com/2012/11/dungeon-world-classes-and-niche.html ; https://daegames.blogspot.com/2015/06/dungeon-world-evolution-of-playbook.html |
| **Shadowdark** has 4 core classes. **Daggerheart** has 9 classes with 2 subclasses each, chosen at level 1. **2024 5e** chooses subclass at level 3. | **D** | above |
| **GURPS DF** puts templates over a point-buy engine: presets for newcomers and full custom for veterans. **Cypher** builds a character from a sentence of three menus. | **D/A** | §3 sources |
| Game Rant/Bethesda: players *regretted* a class choice made before they understood the skills. Skyrim's answer was no class question at all. | **D** | §3 sources |

**Reading.** The evidence supports exactly the owner's Morrowind-style shape, *provided the preset is the default path*:
- **Parent + child is a proven pattern.** It is how 5e class→subclass, PF2e class→archetype, and Cypher type→focus work. Players read the parent as a broad aptitude and the child as identity.
- **Custom builds are for a minority, and that is fine.** About 11% multiclass. A custom path costs nothing *if it is opt-in and uses the same menu as the presets* (GURPS DF's lesson). It is expensive if it becomes the default creation flow (choice overload under preference uncertainty).
- **Timing.** The identity *label* can be chosen at creation, because a preset is cheap to take. The *defining mechanical commitment* belongs after 2–3 sessions (level 2–3), as in 5e 2024 and Skyrim. Let a player respec freely until then.
- **Count.** Aim for about 3–4 suggested classes per Facet (9–12 total). That matches the density of Dungeon World, Daggerheart and 5e and keeps one class per player in a party of 4–5 (Sly Flourish n=4,400: 39% of parties have 4 PCs, 28% have 5).

### 4.5 Morrowind: what to take, what to leave

| Morrowind element | Evidence | Take? |
|---|---|---|
| **Specialization** (Combat/Magic/Stealth). It gives a flat bonus to every skill in that group and makes them advance faster. | A clean "broad aptitude" signal that never forbids anything. https://en.uesp.net/wiki/Morrowind:Classes | **Yes.** It maps directly onto Facets. In tabletop terms: Facet abilities are cheaper to take, or the Facet's stat rises first. |
| **21 preset classes, or build your own** (pick specialization, 2 favoured attributes, 5 major and 5 minor skills) | No usage data exists. Community practice treats presets as starter templates. https://en.uesp.net/wiki/Morrowind:Classes ; https://icehair.wordpress.com/morrowind/character-creation/class/ | **Yes, in miniature.** A custom class = Facet + a name + N picks from the Facet list (the same menu the presets draw from). |
| **Use-based levelling** (10 major/minor skill increases → a level; attribute multipliers depend on which skills rose) | The well-known failure: players "hold back" skills and grind to game the multipliers, which "reduces the incentive to just play". Oblivion's level-scaling made it worse, and Bethesda simplified it and then dropped classes. https://en.uesp.net/wiki/Morrowind:Level ; https://rpgcodex.net/forums/threads/oblivion-vs-morrowind-re-level-attribute-skill-system.9886/ | **No.** Our current "marks for skills used" is the tabletop version of this, and the complexity audit already found it rewards rolling. |
| **Class chosen before you understand the game** | Oblivion regret data, above | **Mitigate** with presets plus free respec before level 3. |

---

## 5. Combat share and pacing

### 5.1 Findings

| Finding | Grade | Source |
|---|---|---|
| **Stated preference**: Sept 2018, n=2,103, favourite pillar was roleplay 59%, exploration 23%, **combat 18%**. | **S** | https://slyflourish.com/facebook_surveys.html |
| **Actual share**: EN World poll (89 votes) on combat's share of the session has a median band of **51–60%**, with 24% of tables at 71%+. One poster sums it up: "as played… 30–40%. D&D as written, between 70–100%." | **S** (small) | https://www.enworld.org/threads/so-what-of-d-d-is-combat.686195/ |
| "Is combat too slow?" (Nov 2017, n=1,165): **29% yes**, 71% no. Most D&D players *tolerate* long fights. | **S** | https://slyflourish.com/facebook_surveys.html |
| 5e actual-play timing: about 27–32 minutes per 5–6 round fight, about 6.9 minutes per round. Already in `RESEARCH_fun_audit_2026-09.md` §4.1. | **A** (logged) | https://www.enworld.org/threads/length-of-combat-time-taken-per-round-collecting-data-from-my-games-updated-3-13-with-an-hour-30-minute-11-round-battle.701556/ |
| **Grid use**: 78% play on a 5-foot grid (May 2024, n=2,800), against 14% theatre of the mind. The majority audience associates "real combat" with a map. | **S** | https://slyflourish.com/facebook_surveys.html |
| **Combat as sport vs combat as war** (Daztur, 2012): balanced "fun fights" against winning before initiative is rolled. Old-school play is *war*: fights are avoided or rigged, and supply and time are the pressure. | **A** (canonical essay) | https://www.enworld.org/threads/very-long-combat-as-sport-vs-combat-as-war-a-key-difference-in-d-d-play-styles.317715/ |
| **Dungeon World 2's designers on DW1 fights**: "inflict a condition doesn't feel like enough of a change"; a move can end with "nothing at all" happening. Their fix is one Fight move with fictional options (take something, exhaust or intimidate, hurt), plus NPC escalation when conditions land. | **D** (post-mortem) | https://www.dungeon-world.com/think-dangerously-fighting-in-dungeon-world-2/ |
| **Lethality**: OSR longest campaigns (n=200) had a median of 24 sessions and 3 deaths, and 21.5% had zero deaths. There are two cultures, "meatgrinder" (about 1 death per 5 sessions, Shadowdark and OSE lean this way) and "picaresque" (about 1 per 12). "Table culture matters most." In the 138-session Nightwick Abbey campaign, deaths fell from about 40% of characters in the first 50 sessions to under 10% later, as players learned. | **S / A** | https://valerialoves.com/how-deadly-is-the-osr-actually/ ; https://icastlight.substack.com/p/the-osr-is-deadly |
| **5e baseline**: 54% of tables report 1–3 deaths and no TPK in a campaign, and 15% report none (n=74). | **S** (small) | https://www.enworld.org/threads/how-often-do-characters-die-in-your-campaigns.676980/ |
| Shadowdark is "fairly forgiving compared to old school games" because of its death mechanics and luck tokens. That softening is part of its broad appeal. The level-0 "gauntlet" funnel is a beloved way to *front-load* lethality where it hurts least. | **A** | http://dreamsinthelichhouse.blogspot.com/2025/01/shadowdark-good-bad-ugly.html |

### 5.2 What this means

- **Players say they want less combat than D&D gives them, but they still want it to feel like a *real fight*.** Most use maps, and the most-played class is the Fighter. Short does not have to mean thin. The FoO fun audit found fights that were short but shallow. DW2's lesson is that *every exchange must change the fiction*, and our three-tier roll is built for that.
- **Danger vs powerlessness.** Deadly OSR play works when death is legible and players learn (Nightwick: 40% early, under 10% later). It fails when outcomes feel arbitrary. The Graceful Fail, the death choice and "Broken never kills" already sit on the picaresque side, which fits the adventure register.
- **Combat as war suits a lean game**, because it moves depth off the player sheet and into situation, supply and choice of battlefield. Those are MM-side procedures.

---

## 6. Social and fellowship mechanics

| Finding | Grade | Source |
|---|---|---|
| **5e Inspiration** is widely described as "almost always forgotten" by DMs and players alike. The DM has 20–25 traits to watch, and the reward isn't tied to the choice that earned it. Groups skip it out of forgetfulness, a "don't reward what they should do anyway" stance, or because it is too weak. Physical tokens and **player-to-player awarding** are the common fixes. | **A** (strong consensus) | https://theangrygm.com/take-the-suck-out-of-inspiration/ ; https://www.enworld.org/threads/does-your-group-use-inspiration-if-not-why-not.673033/ ; https://adeptplay.com/2022/02/08/5e-and-inspiration/ |
| **Dungeon World bonds** divide tables. They are praised where they drive inter-party drama and dropped where characters already know each other or setting drama matters more ("dull and artificial" to resolve for XP). Rob Donoghue's diagnosis is that replacements must be "externally facing and actionable". The usual substitutes are Flags, Keys, and 13th Age-style icon relationships. | **A** | https://dungeonworld.gplusarchive.online/2016/01/21/bonds-dont-work-for-our-group/ |
| **Fate compels** are the known under-used half of the Fate point economy ("nobody compels"). This is already recorded in `research/dice_system_analysis.md`. | **A** | see that file |
| Daggerheart's session-zero *connections* questions and collaborative worldbuilding are the most-praised parts of its onboarding in the review cited. | **A** | https://www.enworld.org/threads/daggerheart-review-the-duality-of-robust-combat-mechanics-and-freeform-narrative.713471/ |
| The belonging→wellbeing link (Matthews 2026, §1) is about *the group*, not about a mechanic. | **E** | §1 |

**Reading.** Peer-awarded currency beats DM-awarded currency on the one failure everyone reports, which is forgetting. Our peer Sparks already get this right. What remains is *visibility*: a physical token or an app button. Relationship mechanics work when they point *outward* at shared goals and threats. They work less well as inward-facing relationship bookkeeping.

---

## 7. Fun requirements by player type (lean-game minimum)

| Player type (Laws) | Motive (research anchor) | Minimum mechanic in a lean game | Evidence |
|---|---|---|---|
| **Power Gamer** | Power, Completion (Quantic Foundry); competence (SDT) | **Levels** with a visible number going up (HP, a bonus) **plus loot** (magic items, one-use treasures) **plus one build pick per level** | DDB tier data; One D&D feat scores; Cairn "anticlimactic"; QF "powerful equipment" |
| **Butt-Kicker** | Destruction/Excitement | **Damage dice that scale with weapon and level**, and one "big hit" peak (natural 12 or a max-damage die) | Fighter is most played; DW2 "damage alone" caveat → pair damage with fiction |
| **Tactician** | Challenge/Strategy; combat as war | **Situational advantage the MM rewards** (terrain, surprise, preparation → Easy) and **monsters with one gimmick each**. Not a player-side option menu | Mearls "simple combat options"; combat-as-war essay; DW criticism of repeating one move |
| **Specialist** | Fantasy (a specific archetype) | **A named preset class** inside a Facet, and a **signature ability** no one else in the party has (niche protection) | DW one-per-party playbooks; One D&D identity scores (Warlock, Wizard lists) |
| **Method Actor** | Fantasy/Story; autonomy | **Background + Specialty (no roll)**, a personal drive the MM hooks, and Sparks for playing the flaw | Angry GM: tie the reward to the choice; bonds must be actionable |
| **Storyteller** | Story; co-authorship (UCC) | **Three-tier roll where 7–9 changes the story**, Trouble Table, Borrowed Trouble, session-zero world questions | `dice_system_analysis.md`; Daggerheart session-zero praise |
| **Casual Gamer** | Social Fun + Accessibility (QF); relatedness | **A preset and a one-sentence rule**, so play starts in about 10 minutes. **Peer-awarded Sparks** make them part of the table without the spotlight | QF social/accessibility cluster; Cypher 10-minute creation; Matthews belonging data |
| *(all)* | Relatedness | **Visible, peer-driven table currency**, and fellowship hooks aimed at shared goals | Inspiration-forgotten evidence; bonds critique |

---

## 8. Implications for a lean Facets of Origin

These are opinionated requirements. They sit alongside `RESEARCH_complexity_audit.md` §7 ("Lean Facets") and mostly confirm it. Where they diverge, the difference is marked.

**Chassis**
1. **HP for everyone: yes.** It is one number, universal familiarity, and the evidence gives no reason to avoid it. The Condition list becomes *Injuries at 0 HP*, with the death choice kept. Stay on the picaresque side of lethality: death is legible and rare, and at most about one per 10+ sessions by default. The MM can dial it up.
2. **Damage dice: yes, always paired with a fictional result.** Weapon dice from d4 to d10/d12 give the Butt-Kicker a number and the Power Gamer a scale. Keep the "7–9 you both land" pattern so every exchange changes the fiction (DW2's post-mortem). Damage alone is the known dead end.
3. **Levels: 10.** About 90% of games end by level 10, and Shadowdark's success proves 10 is enough. **Pacing: level 2 after session 1; levels 3–4 about one per session or two; levels 5–10 about 2–3 sessions each.** That puts level 10 at around session 20–25, close to the median real campaign length (24). Front-load, because 61% of characters live at levels 1–5.
4. **Level-up trigger: the MM calls it, with app-tracked prompts.** Players prefer DM-called or milestone levelling to XP bookkeeping at about 3:1. The early-D&D goal (reward discovery and treasure, not kills) survives as the *prompts*: *discovered something? recovered treasure? changed the world?* The app counts and suggests, and the MM confirms. **Divergence from §7.3:** do not make players track XP totals.
5. **Every level gives a number and a new thing.** HP rises every level. Each level also gives **one pick from the class or Facet list** (not a random roll by default). Offer Shadowdark-style "roll on your Facet table" as an optional mode for players who enjoy the gamble. Every few levels, add +1 to a stat.
6. **Loot: yes, from day one.** Magic items and **one-use treasures** (the Cypher lesson in the fun audit §7) are the cheapest carry-forward reward, they are pure MM-side variety, and they serve Power, Completion and Discovery. The app rolls the tables.

**Facet → class (owner's Morrowind model)**
7. **The Facet is a specialization.** It gives the Facet's stat a head start, makes the Facet's ability list the cheap one, and sets the HP die. It *never forbids* cross-Facet picks; they cost more (for example, one pick in two levels), as Morrowind's "non-specialization skills advance slower" does.
8. **3–4 preset classes per Facet (9–12 total).** Each fits on one card: a name, a starting kit, a signature ability, a suggested pick order, and one "you're the party's…" line for niche protection. **Presets are the default creation flow**, and the Quick Start offers *only* presets.
9. **Custom class = Facet + name + picks from the same list.** It is opt-in, on the same menu, with no extra rules (the GURPS DF pattern). About 11% of D&D players multiclass, so expect most players to use presets and design for the few who don't.
10. **The commitment point is level 3.** Until then a player may swap any pick or re-choose the preset (the Skyrim and 5e-2024 lesson). At level 3 the class takes its **defining signature** (the subclass moment), after two or three sessions of play.
11. **Do not advance on use.** Morrowind's use-tally created optimisation play that fought immersion, and our marks-for-used-skills repeats that flaw. Advancement comes from level-ups, and choices come from picks.

**Magic**
12. **Keep spell-list-free domains, but give casters *named* signature workings.** The One D&D survey shows players protect class identity and distinct spell lists. Let a caster *name and write down* a handful of favourite workings that are always Easy or always available. That gives the "my fireball" identity without a list, and keeps the per-rest count from the complexity audit.

**Combat and the MM side**
13. **Aim for combat at about 25–35% of session time, which is what tables *say* they want.** Hold it there with morale, reaction rolls and "combat as war" advice. Keep the exchange structure, one roll per player per exchange, and NPCs never rolling.
14. **Depth goes on the MM side.** Each monster gets **one gimmick** and a morale number, and there are tables for terrain, complications and treasure. The app surfaces all of it. This answers both rules-light failure modes (GM burnout, repetitive combat) without adding player rules.
15. **The Tactician gets rewarded situations, not a menu.** Preparation, positioning and surprise step difficulty down (Easy). That one verb already exists.

**Fellowship**
16. **Keep peer Sparks and make them visible.** A token or an app button, with an app nudge each scene if nobody has awarded one. Inspiration's failure is forgetting, and peer awarding plus visibility is the known fix.
17. **Put bonds on the outside.** At session zero, ask connection questions aimed at shared goals and threats (Daggerheart and DW critique). Don't make relationship resolution an XP chore.

**Where going lean would lose fun (guardrails)**
- *No levels or loot* → the Power Gamer leaves (Cairn evidence). Do not cut these to save rules.
- *One attack move and HP only* → "hack and slash until it falls over" (DW criticism). Keep the 7–9 fictional outcome and monster gimmicks.
- *Everything is a ruling* → MM burnout (Monsters & Manuals; the burnout essay; our own fun audit). The app must carry tables and procedures, or the lean rules just move the weight onto the MM.
- *A custom build as the default* → choice overload and regret for new players (meta-analyses, Oblivion). Presets first.
- *Thin level-ups* ("+2 to a stat" talents) → dull (Shadowdark critique). Each level needs one *new verb*.

**Open questions to hand upward**
- The owner's pick between §7.3's "roll a stat to avoid harm" and a free Defend roll. The evidence here has nothing specific to say about it.
- Whether to ship an optional level-0 funnel as the Quick Start (the evidence favours it for OSR-leaning tables, and it front-loads lethality where it costs least).
- No study settles the complexity→retention claim (§3.4). The human playtest is still the deciding instrument.
