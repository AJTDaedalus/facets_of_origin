# RESEARCH: v1.1 modifiers, the rules budget, and exchange accounting (D8, D9, D10)

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` · **Tier:** Brain question (strategy). The rulings are the owner's.
**Status:** COMPLETE (research, options, picks, two draft cards, disposition list, licence table).

**Owner update folded in (mid-task):** the two-page budget is a guide, not a limit, "so long as it is still simple". So this memo optimises the card and the disposition list for **felt simplicity**. That means few concepts before play, one way to do each thing, and no exception-handling rules. It does not optimise for page count, and nothing players enjoy is cut to save space.

**Repo inputs:** `REVIEW_lean_facets.md`, `REVIEW_lean_design.md` (C3, M1, M9, M11, m1–m13, verdict), `REVIEW_lean_consistency.md` (M4–M7, m1, m2, m18), `RESEARCH_complexity_audit.md`, `Quick_Start.md`, `III.1`, `III.2`, `III.3`, `II.3`, `MM5`, and the talent list in `facet.yaml`.

**Copyright:** everything below is paraphrase. No text is copied from any source. Wording could legally come from CC BY 4.0 or CC BY-SA 4.0 sources (SRD 5.1/5.2, Knave, Cairn), but none was needed. Both draft cards are original.

**Method note:** the session's web-search quota was used up before this task began. All evidence therefore comes from **direct fetches of known primary sources** (SRDs, publisher sites, designers' blogs), plus open rules text pulled from GitHub mirrors. Three claims could not be checked against a primary source this session. Each is marked **[unverified]** where it appears.

---

## 0. Summary

| Decision | Pick | What it removes |
|---|---|---|
| **D8** Combination rules | **One step, one cap, one clock.** The MM sets the base difficulty. Rule effects are only ever *Easier* or *Harder*. If any Easier meets any Harder they cancel; otherwise the roll moves **one step at most**. No roll ever has **more than two extra dice**. Doubles work the same for everyone: double six is always 10+ and something more; double one is always 6−. **Everything a fight creates ends at the end of the exchange.** Against a mob, damage drops Mooks at one per 4 points. | Stacking questions; "as many Sparks as you like"; one-Help and one-Trouble limits; the 5d6 claim; the +4 ceiling; the lasting natural-2 opening; the Very Hard level-gap band; the separate "Easy beats a gap?" rulings |
| **D9** The budget | **Measure felt simplicity, not pages.** The table uses one player card (about 1½ pages, plus a caster box and a level-up box) and one MM card. Target: **≤5 concepts before the first roll**, **≤35 rules on the player card** (casters +8), and **zero exception clauses** on the card, enforced by a docs test. Everything else is **MM-side** (procedures the MM runs, which players never learn) or **OPTIONAL** (dials). | About 50 rules leave the player's head. Most move MM-side rather than disappearing. |
| **D10** Action accounting | **One action each, one attack count per foe, set by the telegraph.** Keep the five-step exchange. Each PC has **one action** per exchange. Free things are listed, and a talent that grants more says so. Each foe makes exactly **the attacks on its card**, at the targets telegraphed; Intercept is the only redirect. The app shows an action token per PC, attack pips per foe, and state chips (Defending, Intercepting, Exposed, Covered, Opened). All of it clears at step 5. | The 8-attack and extra-Elite-attack abuse, and invisible state, with no initiative added |

**"Simple", as a measurable target (the owner asked for this plainly):**
1. **Concepts before the first roll: ≤5.** They are: 2d6 + stat; the three bands; difficulty; the knack +1; the extra die. The card's first block teaches exactly these.
2. **Rules a new player must hold: ≤35**, counted at the complexity audit's granularity and taken from the player card alone. A caster adds ≤8. Talents are self-describing and aren't counted, as in the audit.
3. **Exception clauses on the card: 0.** No "unless", "except", "only if … but" or "does not count toward". This can be an invariant in `test_docs_consistency.py`.
4. **At G0 (the human session):** a new player takes a legal action in the first exchange without asking what they may do, and makes the first roll within 10 minutes using a preset.

Metric 3 is the one I'd hold hardest. Tables feel exceptions far more than they feel page count.

---

## 1. Per-game findings

Each entry gives the concept in my words, how it stays simple, evidence of play, the licence, and what it means for us.

### 1.1 D&D 5e / 2024: advantage and disadvantage
- **Concept.** A favourable circumstance means two d20s, keep the higher; an unfavourable one means keep the lower. Several favourable circumstances still give just one extra d20. If there is any advantage *and* any disadvantage, the roll has neither, however lopsided the count.
- **Why it stays simple.** Nobody counts sources. A situational modifier becomes a yes/no question on each side. The cancel rule settles every "does X stack with Y" argument in one sentence. The 5e article describes the mechanic as streamlining situational modifiers into a single one.
- **Evidence.** The core mechanic of the best-selling edition, carried unchanged into the 2024 rules. Knave, The Black Hack and Shadowdark all adopted it, which is the strongest peer endorsement a mechanic gets.
- **Licence.** SRD 5.1 and SRD 5.2 are **CC BY 4.0**, so wording is usable with attribution. (The mirror fetched still shows an older OGL notice. The dndbeyond SRD page confirms 5.2 is CC BY 4.0 only.)
- **Sources:** https://www.5esrd.com/using-ability-scores/ · https://www.dndbeyond.com/srd · https://en.wikipedia.org/wiki/Dungeons_%26_Dragons_5th_edition
- **Take.** Presence/absence plus cancel is the proven way to make many sources cheap. We already have steps (±1) instead of a second d20, so we apply the same logic to steps.

### 1.2 Shadowdark
- **Concept.** The 5e-style advantage/disadvantage, in a game marketed as fast, familiar and deadly. Torches burn in real time.
- **Why it stays simple.** One modifier currency, no stacking, and a physical real-time clock instead of bookkeeping. **[unverified]** From memory: Shadowdark uses 5e's rules for advantage stacking and cancelling, and initiative is a single highest roll that then passes around the table in seat order. I couldn't fetch the core text this session.
- **Evidence.** Won four 2024 ENNIEs (Product of the Year, Best Game, Best Rules, Best Layout & Design) and the 2024 Three Castles Award; raised $1.3M. The free quickstart is rated about 4.9/5 from 188 reviews.
- **Licence.** Shadowdark's **Third-Party License is not CC**. Verbatim reprint is limited to monster stat blocks, spells and magic items, and standalone games that rewrite the core are prohibited. **Ideas only.**
- **Sources:** https://www.thearcanelibrary.com/pages/shadowdark · https://www.thearcanelibrary.com/ · https://www.thearcanelibrary.com/blogs/shadowdark-blog/faq-on-the-shadowdark-rpg-third-party-license
- **Take.** A 2020s design won "Best Rules" with 5e's modifier scheme and nothing added. Our cancel rule doesn't need to be clever.

### 1.3 Daggerheart: advantage dice
- **Concept.** Advantage adds a d6 to the total, and disadvantage subtracts one. Advantage and disadvantage dice in the same pool cancel one-for-one, so you never roll both. Help from another player is a separate die that stacks. The GM text advises granting advantage or disadvantage *instead of* changing the Difficulty, because a die feels more visceral than a number. Adversaries mostly don't roll; the PCs roll reactions instead.
- **Why it stays simple.** One kind of object (a d6) for most situational edges, and one cancel rule. The cost is a second modifier track (dice and Difficulty) with guidance on which to use.
- **Evidence.** Critical Role's Darrington Press flagship (2025), with a full SRD.
- **Licence.** **Darrington Press Community Gaming License (DPCGL). Ideas only.**
- **Sources:** https://daggerheartsrd.com/ · https://daggerheartsrd.com/rules/ · SRD text (mirror): https://github.com/seansbox/daggerheart-srd
- **Take.** A die-for-die cancel is a good second option for us (§2, D8 option B). Its own GM advice shows the tax: two tracks need a rule for choosing between them. It also has an **optional spotlight tracker**: a few tokens per player, one spent per action, refilled when everyone is out. That is a direct precedent for D10.

### 1.4 Powered by the Apocalypse: +1 forward, +1 ongoing, hold
- **Concept.** *+1 forward* applies to your next roll and is then gone. *+1 ongoing* lasts until a stated condition ends it. *Hold* is a small spendable count (the *Defend* move gives hold that you spend when attacks come). Aid or Interfere gives one +1 or −2 regardless of how many allies aid.
- **Why it stays simple.** Every lasting effect says when it ends, in the words *forward* or *ongoing*. Help doesn't stack.
- **Evidence.** Dungeon World and dozens of PbtA games. Our three bands come from this family.
- **Licence.** Dungeon World SRD is **CC BY 3.0**. That's outside the brief's "CC BY 4.0 / BY-SA 4.0 only" rule, so **ideas only**. (III.1 currently carries two verbatim DW phrases; see REVIEW P.)
- **Sources:** https://www.dungeonworldsrd.com/moves/ · https://www.dungeonworldsrd.com/gamemastering/ · https://www.dungeonworldsrd.com/playing-the-game/
- **Take.** Our "one step Easier" *is* +1, so a stunt is +1 forward for an ally. PbtA's lesson is that **every effect names its expiry in one of two words**. We can go further with a single expiry for everything a fight creates: the end of the exchange.

### 1.5 Blades in the Dark: position/effect, and the two-bonus-dice cap
- **Concept.** The GM judges **position** (how dangerous: controlled, risky, desperate) and **effect** (how much it achieves: limited, standard, great) before the roll. A roll gets **at most two bonus dice**: one from a teammate's assist, and one from *either* pushing yourself (paying stress) *or* a Devil's Bargain (accepting a complication that happens whatever the result). Only one character may assist. *Set up* lets one character improve a teammate's position or effect for their follow-up.
- **Why it stays simple.** Two judgments made once, out loud, and a hard cap on dice. The cap is a list of the only two ways to get dice, not a general limit.
- **Evidence.** Golden Geek RPG of the Year 2015, Indie RPG of the Year 2016, ENNIE nominee 2018. Over 300 "Forged in the Dark" games use the SRD.
- **Licence.** SRD is **CC BY 3.0** Unported, with required attribution text. **Ideas only** under the brief.
- **Sources:** https://bladesinthedark.com/action-roll · https://bladesinthedark.com/teamwork · https://bladesinthedark.com/progress-clocks · https://bladesinthedark.com/licensing · https://en.wikipedia.org/wiki/Blades_in_the_Dark
- **Take.** This is **the closest precedent for our extra dice**. Our Borrowed Trouble is the Devil's Bargain idea, and Help is assist. Blades caps the total at two, and players don't feel robbed, because the cap is where the fun choice lives: *which* two. Our Spark is Blades' "push" paid in a different currency. A two-dice cap copies a proven ceiling. Blades' *set up* is also our stunt, and it lasts for the teammate's follow-up and no longer.

### 1.6 ICRPG: one target per room, Easy/Hard
- **Concept.** The GM sets one **target number** for the whole room or scene, and all rolls use it. Individual tasks are marked **Easy** or **Hard**, which shift the roll by a fixed amount **[unverified: ±3 on a d20]**. Hazards run on visible countdown **timers**.
- **Why it stays simple.** One number on the table that everyone can see, two words to shift it, and no fiddly modifiers.
- **Evidence.** A long-running indie line with a large community and multiple VTT implementations. The Foundry system exposes "targets and timers" and Easy/Hard as first-class controls.
- **Licence.** Proprietary (Runehammer). **Ideas only.**
- **Sources:** https://www.runehammer.online/ · https://github.com/ClipplerBlood/icrpgme (Foundry system: targets, timers, Easy/Hard)
- **Take.** A visible base difficulty that the app shows, with rule effects as Easier/Harder words and never as arithmetic. Our Threat Clock is already a timer.

### 1.7 The Black Hack
- **Concept.** Roll-under d20 on an attribute. Only players roll: when a monster attacks, the player tests to avoid it. Advantage and disadvantage are the GM's only situational tool. Initiative: every PC tests DEX, those who pass act before the foes as a group in any order they like, and those who fail act after. Consumables use a **usage die** that shrinks.
- **Why it stays simple.** It's about 6,000 words for a complete game. One modifier currency, side-based turns with player-chosen order, and a usage die instead of counting.
- **Evidence.** Hugely influential in 2016–2018 (it spawned many "Hacks"). Our usage die comes from this lineage.
- **Licence.** Released as **OGL 1.0a** open game content. **Ideas only.**
- **Sources:** text mirror https://github.com/brunobord/the-black-hack (english/the-black-hack.md) · https://en.wikipedia.org/wiki/Old_School_Renaissance
- **Take.** "The players act as a group, in any order they choose, then the foes" is our exchange already. Its simplicity comes from **one action each**, which TBH states and we don't.

### 1.8 13th Age: the escalation die
- **Concept.** From the second round, a visible d6 counts up by one each round, to +6. PCs (not monsters) add it to attacks. It resets if the heroes stop fighting.
- **Why it stays simple.** One shared, visible number that only goes up. It pushes fights to end and rewards pressing on.
- **Evidence.** Widely borrowed. It's the signature mechanic of a well-regarded d20 game.
- **Licence.** 13th Age SRD (Archmage Engine) is **OGL. Ideas only.**
- **Source:** https://www.13thagesrd.com/combat-rules/
- **Take.** **Not adopted.** It adds a rule. It is the model for how the app should *show* shared fight state: one visible indicator the whole table reads, and nobody tracks privately. Our *Bloodied* line already does its narrative job.

### 1.9 Cairn (2e)
- **Concept.** Attacks auto-hit, and damage is weapon die minus armor. Rounds are **side-based**: PCs act, then foes, and results within a side happen at the same time. In round one each PC must pass a DEX save or lose that turn. **One move and one action per turn.** Actions are declared before dice roll. **If several attackers target one foe, roll all damage and keep only the highest.** Impaired attacks drop to d4 and Enhanced attacks rise to d12 (conditions change the *die*, not a number). Blast rolls separately per target. A large group is a **Detachment**: individuals' attacks against it are Impaired, and its attacks are Enhanced and Blast. The Warden should telegraph serious danger, and the more dangerous, the more obvious.
- **Why it stays simple.** One kind of modifier (die size), one action each, side-based order, and crowds as one unit. The procedures and principles live on the Warden's side.
- **Evidence.** A leading "NSR" game, with an active open repository of hacks and adventures, and a 2e that refined but didn't grow the rules. The core rules page is about 2,200 words.
- **Licence.** **CC BY-SA 4.0**, so wording is legally usable, but ShareAlike would attach to derived text. CC BY-SA 4.0 is one-way compatible with GPLv3. Not needed; paraphrased only.
- **Sources:** https://cairnrpg.com/second-edition/ · https://github.com/yochaigal/cairn (second-edition/players-guide/core-rules.md, overview-and-principles.md, wardens-guide/combat.md) · https://cairnrpg.com/first-edition/cairn-srd/
- **Take.** Three ideas for D10: **one action**, **declare before dice**, and an **anti-pile-on** rule (keep the single highest). The last one I reject for us: focus fire is fun, and our damage follows a roll. Cairn's treatment of a crowd as one unit validates our mob. Its answer to "area vs a crowd" is that blast damage is the tool that works on crowds, which supports making area attacks strong against mobs (D8).

### 1.10 Knave (1e)
- **Concept.** Seven pages. Advantage/disadvantage as 2d20 better or worse. The designer notes that players enjoy it and it simplifies the math. **Group initiative is re-rolled on a d6 each round** (1–3 foes first, 4–6 PCs first), with a note that this speeds combat and keeps everyone engaged. One move and one combat action per turn. **Advantage in combat can be spent another way**: take the advantage, *or* make an attack and a stunt together without it.
- **Why it stays simple.** Everything is a d20 against an ability; one action; side initiative; the referee has the last word on stunts and advantage.
- **Evidence.** A staple NSR toolkit, designed to be hacked. Its 2e continued the line.
- **Licence.** **CC BY 4.0**, so wording is usable with attribution. Not needed; paraphrased only.
- **Sources:** https://questingbeast.itch.io/knave · text mirror https://github.com/lskh/Knave (Knave.md)
- **Take.** One action per turn is universal across the light games. Knave's "take the bonus *or* do two things" is a neat idea for the 10+ pick; it's noted, not adopted.

### 1.11 Into the Odd / Bastionland
- **Concept.** Saves (d20 roll-under) do almost everything, attacks auto-hit, and damage goes to HP and then an ability. Enhanced and Impaired change the damage die. A detachment ignores small attacks. Players act, then enemies; a DEX save decides whether a PC acts before the foes at the start **[unverified: exact Remastered wording]**. McDowall argues for rules that are **"light but strong"**: few, but each one genuinely shapes play (reaction and morale rolls are his examples). A rule earns its place only if removing it would change play. On rulings: be transparent about how you're ruling.
- **Why it stays simple.** One roll type, and procedures (reaction, morale) instead of player rules.
- **Evidence.** The ancestor of Cairn, Electric Bastionland and a whole family of "Odd-likes". Sold by Free League as an "ultralite system that keeps the game moving".
- **Licence.** Proprietary. **Ideas only.**
- **Sources:** https://www.bastionland.com/2022/05/graphene.html · https://www.bastionland.com/2016/04/oddular-mechanics.html · https://www.bastionland.com/2023/02/only-roll-initiative.html · https://www.bastionland.com/2020/10/kitbash-attitude.html · https://www.bastionland.com/2023/07/how-many-polearms.html · https://www.bastionland.com/2018/07/expose-your-prep.html · https://freeleaguepublishing.com/games/into-the-odd/
- **Take.** "Light but strong" is the right test for every line on our card. The +4 ceiling fails it: removing it changes nothing.

### 1.12 Maze Rats
- **Concept.** 2d6 resolution. **One page of rules**, one page of character creation, eight pages of random tables, two pages of referee advice. It relies on player ingenuity more than on mechanics.
- **Why it stays simple.** The ratio says it all: rules are about 8% of the book, and tables and referee advice are most of the rest.
- **Evidence.** A frequently cited example of rules-on-one-page design.
- **Licence.** Not stated on the storefront. **Ideas only.**
- **Source:** https://questingbeast.itch.io/maze-rats
- **Take.** Our MM Toolbox (MM6) is the right kind of mass. It belongs MM-side, and moving it there costs players nothing.

### 1.13 B/X and Old-School Essentials
- **Concept.** Side initiative, a fixed order of phases each round, one action, morale and reaction rolls on the referee's side, and many optional rules clearly labelled as such.
- **Why it stays simple.** The player-facing load is single numbers; procedure and tables are referee-side (the complexity audit, §1).
- **Evidence.** OSE is the dominant B/X restatement and is known for its layout: one topic per spread, with reference-card-like density.
- **Licence.** B/X is proprietary. The **OSE SRD site now states its material is not open content** and can't be copied or adapted without permission, while noting it incorporates SRD 5.1 (CC BY 4.0) material. **Ideas only.** (The Credits already owe OSE/B-X a mention; see REVIEW P.)
- **Source:** https://oldschoolessentials.necroticgnome.com/srd/index.php/Main_Page (the Combat page returned a server error this session).
- **Take.** OSE's "optional rule" labelling is the model for our OPTIONAL list: each is a named, self-contained paragraph whose default is stated.

### 1.14 "Rulings, not rules"
- **Concept.** The referee's ruling in the moment outranks a rule that tries to foresee every case. Players succeed through clever plans the referee adjudicates, not through character options. Finch's *Quick Primer* (2008) set out four pillars: rulings over rules, player skill over character abilities, heroic rather than superheroic, and balance not being the point.
- **Why it stays simple.** Edge cases never enter the book; the referee handles them at the table.
- **Evidence.** The organising slogan of the OSR.
- **Licence.** The Primer is proprietary and free to download. **Ideas only.**
- **Sources:** https://en.wikipedia.org/wiki/Old_School_Renaissance · https://www.bastionland.com/2020/10/kitbash-attitude.html
- **Take (and a counterweight).** McDowall (*Graphene*, *Kitbash Attitude*) warns that a game made *only* of rulings feels absent, and that some rules are stronger for being unbreakable. The balance for us: **a rule that the app must enforce, or that players plan around, belongs on a card** (the cancel rule, the dice cap, one action). **An edge case the MM can settle in five seconds belongs MM-side as a principle** (trying again, unnarrated details, when not to roll).

### 1.15 How games signal optional rules ("dials")
- **Evidence seen this session:**
  - Daggerheart boxes *Optional: Spotlight Tracker Tool* inside the core rule it modifies.
  - Draw Steel boxes *Alternative Turn Order* in the same way.
  - Knave uses *Designer's Notes* to say what to change.
  - Cairn keeps a `hacks/` folder separate from the core.
  - OSE labels optional rules separately.
- **Pattern.** The default is in the body text. The option is a boxed, named variant next to it, with one line on *why* you'd switch. We already have this pattern: our "MM Note" boxes use **Default / The dial / The cost**. The recommendation is simply to use it for every OPTIONAL item and to keep dials off the player card.

### 1.16 Initiative-less and side-based structures
| Game | Structure | How it limits a player | Notes |
|---|---|---|---|
| Dungeon World | No turns or rounds; the GM moves the spotlight in conversation and answers each move with a GM move | GM judgment only | Worked for DW. **It's what our app does now, and it let one player attack eight times.** |
| Blades | No combat turns; the GM frames and moves the spotlight; teamwork is explicit | GM judgment; each roll has a consequence | Same risk without a GM watching |
| Daggerheart | No initiative and no fixed action count; the spotlight follows the fiction, whoever hasn't had it, or a trigger | Optional **token tracker** (about 3 per player, one per action, refilled when all are spent) | A soft cap, offered because some tables want it |
| Into the Odd / Cairn | Side-based: PCs, then foes, results simultaneous; a DEX save to act in round one | **One action** per turn | Cairn adds declare-before-dice |
| Knave | Side-based, d6 each round for which side goes first | One action | Re-rolling is for danger |
| Black Hack | DEX test sorts PCs before or after the foes; each group picks its order | One action | |
| Draw Steel | **Sides alternate one creature at a time**; the players choose who goes next (a d10 decides which side starts); a flip-token marks who has acted; an argument timer | One main action, one maneuver, one move per turn | An *Alternative Turn Order* sidebar for tables that dislike choosing. The flip-token is a physical "has acted" marker. Licence: **Draw Steel Creator License, ideas only.** Sources: https://github.com/SteelCompendium/data-rules-md (Chapters/Combat.md, Chapters/The Basics.md), https://steelcompendium.io/v2, https://en.wikipedia.org/wiki/Matt_Colville |
| 13th Age | Cyclic d20 initiative plus the escalation die | One standard action | Included for the escalation die |
| **Facets (current)** | Telegraph → players act in any order → foes attack in the open → narrate → effects end | **Nothing stated** | The telegraph is our distinctive strength |

**Draw Steel on edges and banes** (relevant to D8): an edge is +2 and a bane is −2. Two or more edges make a *double edge*: no bonus, but the result moves up a tier. They cancel pairwise, a double against a single leaves a single, and the cap is two because each extra circumstance should matter less and counting past two slows play. This is a **third published "cap and cancel" scheme** after 5e and Daggerheart. It is the most complex of the three, and it still caps at two.

**What the light games agree on, and what we lack:** every one of them states **one action per turn**, and every one has **a single rule for combining circumstances** (presence/cancel, or cancel with a cap). We have neither in writing.

---

## 2. D8: Combination rules

### The questions to close (from the reviews)
Stacking of Hard and Easy sources (Defend, cover, Warding, level gap, stunt, natural-2 opening, Studied Foe, signature, Specialty, knack); Sparks per roll; III.1's "5d6 is the most" against unlimited Sparks, *Inspiring*, *Rallying Cry* and the Lucky-tooth curio; one Help against "each helper adds a die"; enemy naturals (whether they force a tier); how long a stunt's opening lasts and who may use it; area workings against a mob; the +4 ceiling (a dead rule).

### Probability check (2d6, keep best two; computed this session)
| Dice | +0: 10+ / 7+ | +2: 10+ / 7+ | +3: 10+ / 7+ |
|---|---|---|---|
| 2d6 | 17% / 58% | 42% / 83% | 58% / 92% |
| 3d6 (1 extra) | 36% / 81% | 68% / 95% | 81% / 98% |
| 4d6 (2 extra) | 52% / 91% | 83% / 98% | 91% / ~100% |
| 5d6 (3 extra) | 65% / 96% | 91% / ~100% | 96% / ~100% |
| Foe with an extra die, 3d6 keep *best* (exposed) | as the 3d6 row | | |
| For reference: 3d6 keep *lowest* two | 5% / 32% | 19% / 64% | 32% / 80% |

**Reading.** One extra die is worth about +1½ steps at 10+. At a typical +2, a third extra die takes a roll from "very likely" to "can't fail", so a cap at **two** extra dice keeps a sliver of risk. That matches Blades' ceiling. One step (±1) is worth about 11–16 points at 10+, so letting steps pile up to ±3 would swing a roll by more than a Spark. That's why rule effects stop at one step.

### Options

**A. One step, one cap, one clock (the 5e cancel applied to steps).** *Recommended.*
1. **The MM sets the base difficulty from the fiction**: Easy, Standard, Hard or Very Hard. The level gap becomes part of the base: a foe 3+ levels above you makes attacks on it Hard. The Very Hard band is cut (see D9).
2. **Rule effects never set a difficulty; they make a roll *Easier* or *Harder*.** These are: stunt, Studied Foe, signature working, Specialty, Defend, Intercept, cover, *Warding Presence*, a Wound, heavy armor on stealth, the Dust-fall curio. **If any make it Easier and none Harder, move one step Easier. If any make it Harder and none Easier, move one step Harder. If both, they cancel.** There's no row past Easy or Very Hard.
3. **The knack stays +1** and is part of your bonus, not a step. It never stacks. The +4 ceiling is cut.
4. **Extra dice: no roll has more than two**, from any mix: Spark, Help, Borrowed Trouble, *Inspiring*, *Rallying Cry*, curios. Foes follow the same cap (exposure, a Bloodied Boss). **Dice and steps never cancel each other.**
5. **Doubles, for everyone.** Kept double six: 10+ whatever the total, and something more (the player names it; for a foe, the MM does). Kept double one: 6− whatever the total. A player also takes a Spark (it's the Graceful Fail without the narration test). The lasting "opening" from a foe's double one is cut.
6. **One clock.** Everything a fight creates (Defend, Intercept, cover, stunt, exposure, Studied Foe, a ward) ends at step 5 of the exchange. A stunt helps **the next attack on that foe by anyone but you, this exchange**. Because players choose their order in step 2, the stunter simply goes first.
7. **Mobs.** A hit on a mob drops one Mook for every 4 damage (at least one). An area attack (a Major harm working, *Whirlwind*) drops one Mook per 2 damage. *(Sim-check the ÷2 before printing; M9 measured splitting and area problems at levels 1 and 5.)* A mob is 3–5 Mooks; a bigger crowd is several mobs.
- **Rules count:** 7 lines replace about 14 current rules and rulings (stacking, three kinds of "is Easy/Hard", one Help, one Trouble, uncapped Sparks, 5d6, +4 ceiling, the knack not stacking, two sets of naturals, the lasting opening, the Very Hard gap, stunt duration, the mob-vs-area gap).
- **App fit:** trivial. The engine already treats enemy-side Hard sources as non-stacking (`combat.py:462`). Generalise that to "collect Easier/Harder flags → net one step", and enforce `max_extra_dice: 2` in `facet.yaml`.
- **Agency:** kept. Players still pick *which* two dice to take, and a stunt or opening still visibly beats a bigger foe's gap (Easier cancels Hard → Standard). That's a better story than "Easy doesn't help against a big foe".
- **Cost:** a second Easier source is wasted. That's intended, and it's the same thing 5e players accepted.

**B. Everything situational is a die (Daggerheart-style).** Easier becomes +1 die (keep best two), and Harder becomes a trouble die (keep *lowest* two); the two cancel die for die. Difficulty stays as the MM's base only.
- **For:** one currency with exposure, which is already a die, and very tactile.
- **Against:** it adds a new concept (keep the worst two). Removing the steps is a large rewrite, and "Hard" is how the MM talks at the table. The table above shows a trouble die is far harsher than −1 (at +2, 10+ falls from 42% to 19%), so every Hard source would need retuning. **Rejected:** it adds a concept to save a rule.

**C. Free stacking with a clamp (roughly what the engine does now).** Each source moves a step, clamped to Easy…Very Hard.
- **For:** "fair" to every source.
- **Against:** arithmetic at the table. Defend + cover + ward = Very Hard, which the sim would need to re-tune, and the stacking arguments stay. **Rejected.**

### D8 pick: **A**
Sub-rulings bundled with the pick, for the owner to confirm:
- Cap at **two** extra dice (not one Spark per roll). Three Sparks are still spendable over a session, and a player facing a big moment chooses Spark + Help or Spark + Trouble.
- Unify doubles so they force the band for foes and players alike, and cut the opening. This changes one existing player rule: a kept double one now always fails. With keep-best-two, a kept double one means *every* die came up 1, so it's rare, and it pays a Spark.
- **Dependency:** "a working aimed at a foe is an attack" (so the level gap, cover, stunts and exposure apply to it) is owner ruling 2. The cancel rule makes that ruling cheap, because nothing new has to be defined.

---

## 3. D9: The budget

### Options
**A. A hard two-page card, everything else optional.** The BRIEF's original G0 promise. It forces cuts players might enjoy (the death choice, Borrowed Trouble), and the owner has now lifted it. **Rejected as a limit**, kept as a guide.

**B. A felt-simplicity budget.** *Recommended.* Three measured targets (§0): ≤5 concepts before the first roll, ≤35 card rules (casters +8), and zero exception clauses on the card. Rules the MM runs become MM procedures that players never learn. Dials are optional and default-off where they're a cost, default-on where they're a toy. The player card runs about 1½ pages. That's acceptable because each line on it is "light but strong".

**C. Accept "familiar, ~85 rules".** It's honest, but it abandons "simple like earlier D&D", which the owner still wants. **Rejected.**

### D9 pick: **B**
Why it works: the audit's own lesson from early D&D (§1 there) is that **the complexity sat on the referee's side**. About 40 of the 85 rules are procedures the MM runs: morale, mobs, Bloodied, the level gap, the Pressure die, clocks, reaction rolls, group and PvP rolls, trying again, costs on a 7–9. Moving them MM-side doesn't delete them. It takes them out of the new player's head, which is exactly how B/X, OSE, Cairn and Maze Rats stay light.

Card count (my count, audit granularity):
- **The Roll** 9 (roll, bands, difficulty, Easier/Harder cancel, knack, extra dice + cap, doubles, Avoid, Specialty)
- **Sparks, Help, Trouble** 5
- **The Fight** 15 (exchange, one action, free things, attack bands, three picks, exposure, reach, foe bands, Defend, Intercept, Mooks drop, weapons, armor, damage bonus, one clock)
- **Hurt and rest** 5 (Wound, Hold On, dying/tend, death choice, rest)
- **Slots** 1

That totals **35**. The caster box adds **8** (cast roll, scope table, bands, Fatigue in slots, no-slot limit, signature, Minor = stunt, a working is an attack). The level-up box is read at level-up only, so it isn't counted in the at-table load (5 lines). Exception clauses: **0**.

---

## 4. D10: Per-exchange action accounting

### The problem
Nothing states how much one character does in an exchange (one player attacked 8 times). Nothing binds a foe to its telegraph or its attack count (an Elite attacked 3 times). The MM can't see Defending, Exposed or Covered.

### Options
**A. One action each, attacks bound to the telegraph, state on screen.** *Recommended.*
- Keep the five-step exchange: no initiative, players in any order, foes in the open.
- **Each PC gets one action per exchange.** The card lists them: attack, cast, Defend, Intercept, Help, study, a risky move, use the room, wind back a clock. **Free**: talking, a short step, drawing or passing an item, and anything a talent calls free (*Tactician*'s Help, *Fast Hands*, *Second Wind*). A talent that gives a second action says so.
- **Each foe makes exactly the attacks on its card**: Standard 1, Elite 2, Boss 2, a mob 1. They go at the targets named in the telegraph. **Intercept is the only thing that moves an attack.** If a target has left the foe's reach, that attack goes to someone in reach or is lost (the MM's call, said aloud).
- **App:**
  - A per-exchange ledger. Each PC has one **action token**, spent when they act; the MM can grant an extra one with a logged reason.
  - Each foe shows **attack pips** equal to its count, filled in by the telegraph.
  - **State chips** sit on each portrait: *Defending*, *Intercepting → ally*, *Exposed*, *Covered*, *Opened (stunt)*, *Studied*.
  - Step 5 clears every token, pip and chip in one click.
  - The app refuses a second attack from a spent token (fixing M4 "Defend doesn't stop attacking" for free) and a fourth foe pip.
- **Precedents:** one action each (Cairn, Knave, TBH, ITO); Draw Steel's flip token for "has acted"; Daggerheart's optional per-player tokens; Cairn's declaring before dice, which our telegraph already does for the foes.
- **Rules added:** 1 ("one action each"). **Rules replaced:** the undefined state, plus M4 and "Defend doesn't stop attacking".

**B. Spotlight tokens across the scene (Daggerheart optional).** Each player gets about 3 tokens per fight, spending one per action, refilled when everyone is out.
- **For:** it lets a player act twice now and sit out later, which is flexible.
- **Against:** it breaks the exchange rhythm (the telegraph is "what happens this exchange"), it's harder to read, and the foes' attack counts still need a separate rule. **Offer as an OPTIONAL dial only if G0 shows players want it.**

**C. Alternating sides (Draw Steel).** A player acts, then a foe, then the players pick who's next.
- **For:** tactical, and it lets foes react.
- **Against:** it replaces the telegraph with interleaving, so foes' attacks happen mid-step 2 and the "answer the telegraph" play loses its shape. It's also a new structure to learn. **Rejected.**

(Rejected outright: DW/Blades pure spotlight. That's the current state, and it produced the abuse. Also rejected: Cairn's keep-highest damage against a foe hit by several attackers. It punishes focus fire, which is fun, and our hits already follow a roll.)

### D10 pick: **A**
It keeps the owner's "no initiative, everyone acts". It adds a single card line. It gives the app something concrete to enforce and display, and it closes M4 and the MM-visibility finding as side effects.

---

## 5. Draft PLAYER CARD

*Original wording. `[R1]` and `[R2]` mark lines that wait on owner rulings 1 (attack stat) and 2 (magic frame).*

> ### THE ROLL
> - Roll **2d6 + the stat the MM names**. Add **+1 if one of your knacks fits**. It is only ever +1.
> - **10+** you do it. **7–9** you do it, at a cost. **6−** it goes wrong, and the story moves on.
> - **Difficulty.** The MM says it before you roll: **Easy +1 · Standard 0 · Hard −1 · Very Hard −2.**
> - **Easier and Harder.** Some things make a roll Easier or Harder. If anything makes it Easier and nothing makes it Harder, it is one step Easier. If anything makes it Harder and nothing makes it Easier, it is one step Harder. If both, they cancel. Never more than one step.
> - **Extra dice.** A Spark, Help or Borrowed Trouble each adds a d6. Keep the best two. **No roll has more than two extra dice.**
> - **Doubles.** Keep two sixes: it's a 10+ whatever the total, and you name something more. Keep two ones: it's a 6− whatever the total, and you take a Spark.
> - **Avoid.** When something happens *to* you, roll 2d6 + **Body** (your flesh), **Mind** (your senses) or **Soul** (your will). 10+ you avoid it · 7–9 you avoid the worst · 6− it takes hold.
> - **Specialty.** When your Specialty covers it, you simply know it, or the roll is Easier.
>
> ### SPARKS, HELP, TROUBLE
> - You start each session with **3 Sparks**. Spend one before a roll for an extra die.
> - **Earn a Spark** when the MM gives you one, when another player calls "Spark?" and the MM agrees, or when you roll 6− and narrate how it gets worse or more interesting (the **Graceful Fail**).
> - **Help.** Spend your action to give an ally an extra die. You share whatever their roll costs.
> - **Borrowed Trouble.** Before your roll, anyone may offer you a complication. Accept it for an extra die. The complication happens whatever you roll.
>
> ### THE FIGHT
> **Each exchange:** 1. The MM says what each foe is about to do, and to whom. 2. **Each player takes one action**, in any order you like. 3. The foes roll their attacks in the open. 4. The MM narrates. 5. **Everything from this exchange ends.**
>
> **Your action:** attack · cast · Defend · Intercept · Help · a risky move · use the room · wind a clock back one segment (no roll). **Free:** talking, a short step, drawing or passing something.
>
> **Attack:** 2d6 + Body `[R1]`, +1 if a knack fits.
> - **10+** Deal your weapon die, and pick one: **+1d6 damage** · **stunt** (the next attack on that foe by someone else, this exchange, is Easier) · **cover** (attacks on an ally you name are Harder).
> - **7–9** Deal your weapon die. You are **exposed**: each foe that can reach you rolls an extra die when it attacks you.
> - **6−** You miss, and the MM makes a move.
>
> **Defend:** you don't attack; attacks on you are Harder. **Intercept:** Defend, and the attacks aimed at one ally in your reach come to you instead.
> **Reach:** a foe can reach you if it could strike you this exchange. A foe with a ranged weapon reaches anyone it can see.
> **Foes' attacks:** 10+ a hard hit (damage +2) · 7–9 a hit · 6− a miss. **Mooks** drop to any hit of 7 or better.
> **Weapons:** unarmed d4 · light d6 · standard d8 · heavy d10 (2 slots) · ranged d8. **Damage bonus:** +1 from level 3, +2 from 6, +3 from 9.
> **Armor:** light 1 · heavy 2 · shield +1 · 3 at most. It subtracts from every hit. Every hit does at least 1.
>
> ### HURT AND REST
> - **At 0 HP** you take a **Wound**: it fills a slot, and rolls that strain it are Harder. Then roll **Hold On**, 2d6 + Body: **10+** you're up at 1 HP · **7–9** you're out of the fight, awake · **6−** you're dying. An ally who tends you before the scene ends saves you.
> - **If nobody does, you choose:** a **Scar** you carry for good, or a **last action** that succeeds without a roll, and then your character dies.
> - **Breather** (a few quiet minutes): half your max HP back. **Night's rest** in safety: all HP, all Fatigue and one Wound.
>
> ### SLOTS
> You have **10 + Body** slots. Each item, each point of Fatigue and each Wound fills one; a heavy item fills two. When they're full, you carry nothing more.
>
> ---
> #### CASTER BOX (read this only if you cast)
> - Name your **domain**, **intent** and **scope**. The MM confirms the scope before you roll. Roll **2d6 + Mind** (Thaumaturgy) or **2d6 + Soul** (Invocation), +1 if a knack fits.
> - **Minor:** Standard, costs nothing, never harms; in a fight it counts as a stunt. **Significant:** Standard, 1 Fatigue, 1d8 harm to one target. **Major** (level 3+): Hard, 2 Fatigue, 2d8 harm to a group.
> - **10+** it works · **7–9** it works, and you pick one of two costs · **6−** the MM rolls a mishap. Pay the Fatigue whatever the result.
> - **Fatigue** fills a slot until a night's rest. With no free slot you can cast only Minor.
> - **Signature workings** are Easier.
> - A working aimed at a foe **is an attack** `[R2]`.
>
> #### LEVEL-UP BOX (read at level-up)
> - **Every level:** roll your grit die for HP, or take its average (at least 1). Then make **one pick**: a new talent, or the improved form of one you've held for a level.
> - **Level 3:** your signature talent is the pick. **Levels 4 and 8:** +1 to a stat, to a maximum of +3. **Levels 5 and 9:** casters name another signature working.
> - Each talent says when it refreshes.

---

## 6. Draft MM CARD

*Original wording. Everything here is something **the MM** runs. Players never need to learn it.*

> ### CALLING A ROLL
> - Roll only when the outcome is uncertain and both results matter. Otherwise say yes.
> - Name the **stat, the difficulty and the reason** before any dice move. Default: **Standard**. A foe **3 or more levels above** the character makes attacks on it Hard, as the base difficulty. If it is 6 or more above, tell them head-on won't work.
> - **7–9:** name one cost: it takes longer, costs something, exposes them, draws attention, or the gain is smaller. **6−:** make a move: a new danger, something taken, an unwelcome truth, someone put on the spot. Never "nothing happens".
> - **Trying again** needs a changed situation. Ask "what's different this time?"
> - **Group roll:** everyone rolls; if most get 7+, the group succeeds. **Player against player:** both roll, and the higher wins. A tie is a 7–9 for both.
> - Players act on what you've described. Answer their questions, and lean toward yes.
>
> ### SPARKS AND TROUBLE
> - Hand Sparks out freely, and confirm peer calls. At each act break, ask every player to nominate one other; confirm almost always.
> - Offer **Borrowed Trouble** once or twice a session, at tense moments. Make it specific and genuinely bad, and never a dead end.
>
> ### RUNNING A FIGHT
> - **Telegraph** every foe's attacks and targets. Each foe makes exactly the attacks on its card: **Standard 1 · Elite 2 · Boss 2 · a mob 1**. Only Intercept moves an attack. If a target has moved out of reach, the attack goes to someone in reach, or is lost. Say which.
> - **Foe attack:** 2d6 + attack, in the open. Doubles as for players: two sixes are a hard hit and something more; two ones are a miss.
> - **Easier/Harder** works for foes exactly as for players (Defend, cover and a ward make a foe's roll Harder, one step at most). An exposed target gives the foe an extra die. **At most two extra dice** for a foe too.
> - **Mobs:** one attack, +1 damage per Mook beyond the first (up to +4). A hit drops one Mook per 4 damage (at least one); an area attack drops one per 2 damage *(pending a sim check)*. Keep a mob to 3–5 Mooks; a bigger crowd is several mobs.
> - **Bloodied** (half HP or less): read the WHEN BLOODIED line at once. A Boss changes phase.
> - **Morale:** when the first foe falls, half are down, the leader drops, or one is left alone and hurt, roll 2d6 once for the group. Higher than their morale means they break. Morale 12 never breaks.
> - **Control workings** on an Elite or Boss last one exchange `[R2]`. **Scope:** meaningful power or precision is never Minor, and a chain of small workings is priced as its result. Decide before the roll.
> - End the exchange: clear everything.
>
> **Monster levels and roles:** Tables MM5–6 and MM5–7, unchanged. **Reading a fight:** *hold until regenerated from the sim (REVIEW M2). The current table is wrong in both directions.*
>
> ### THE WORLD
> - **Pressure die** (d6), each exploration turn, journey leg, or breather in danger: 1 encounter · 2 sign · 3 hazard · 4 cost · 5 opportunity · 6 quiet.
> - **Reaction** (2d6): 2–4 hostile · 5–6 wary · 7–9 wants something first · 10–11 open · 12 friendly.
> - **Threat Clock:** four segments, in view. A 7–9 or 6− near the hazard advances it, a group roll at most once. When it fills, the hazard strikes; say how before anyone rolls.
> - **Usage die:** d8 → d6 → d4 → gone. Roll after a scene of use; a 1 or 2 steps it down.
> - **Oracle:** 2d6 with odds as difficulty. 10+ yes · 7–9 yes, but · 6− no. Doubles: "and".
> - **Stuck?** A threat moves, someone arrives wanting something, or a secret surfaces.
> - **Hoards:** as MM5.
>
> ### LEVELS
> You call the level: 2 after session 1, 3 after session 3, then every two or three sessions. At every session's end, ask the five questions.

---

## 7. Rule disposition (every current player-facing rule)

Numbering follows the ~86 rules of REVIEW_lean_design C3, extended with MM-side items so nothing is lost. **CHANGED** means the rule survives in the new form shown.

### ON THE CARD
| Rule | Note |
|---|---|
| Roll 2d6 + stat | |
| Three bands | |
| Four difficulties | |
| "One step" shifting | **CHANGED** into the Easier/Harder cancel rule (D8-A.2) |
| Knack +1, knacks never stack | Folded into one line ("only ever +1") |
| Extra dice, keep best two | |
| Spark spending | **CHANGED:** cap of two extra dice |
| Help (costs your action, shares the cost) | "One per roll" replaced by the cap. Help on an attack shares exposure (the cost is the exposure) |
| Borrowed Trouble | "One per roll" replaced by the cap |
| Natural 12 | **CHANGED:** doubles, the same for everyone |
| Natural 2 | **CHANGED:** always 6−, and pays a Spark |
| Spark sources: MM award, peer call, Graceful Fail | |
| Graceful Fail content test | One clause ("worse or more interesting") |
| Avoid, with the stat map | |
| Specialty | |
| The five-step exchange | |
| **One action each** | **NEW** (D10) |
| Attack stat | `[R1]` |
| Attack bands | |
| The three 10+ picks, stunt and cover defined inline | |
| Exposure (reach, extra die, this exchange) | |
| Miss = MM move | |
| Reach | **NEW definition** |
| Foe attack bands | |
| Defend | |
| Intercept | |
| Mooks drop to any 7+ | The player-visible half of mobs |
| Weapon dice | |
| Armor (subtract, cap 3, minimum 1) | |
| Damage bonus 3/6/9 | |
| Wound (slot, strain Harder) | |
| Hold On | |
| Dying and tending | |
| The death choice | |
| Breather and night's rest | |
| Slots (10 + Body; items, Fatigue and Wounds fill them; heavy = 2; full is full) | |
| One clock (combat effects end at step 5) | **NEW**, and it replaces several expiry rules |
| Wind a clock back (costs your action, no roll) | The player-visible half of clocks |
| *Caster box:* casting talent/tradition stat, domain/intent/scope, scope table, cast bands, Fatigue paid regardless, Fatigue in slots and the no-slot limit, signature workings Easier, Minor = stunt, a working is an attack `[R2]` | Only casters read it |
| *Level-up box:* HP per level, one pick, talent vs improved (held a level), signature at 3, stats at 4/8 (max +3), caster signatures at 5/9, talents self-describe their refresh | Read at level-up only |

### OPTIONAL (dials; boxed next to the rule they modify, default stated)
| Dial | Default | Why it's a dial |
|---|---|---|
| Hidden difficulty | Off | It's already a dial in III.1 |
| Win on HP only (no clever-answer bonus) | Off | It's already a dial in III.3 |
| Heavy armor costs a caster +1 Fatigue | Off, pending ruling 1 | It's an exception clause. If ruling 1 gives armor allowances per Facet, it's redundant |
| Free rebuild before level 3 | On | Rarely needed on the card |
| Rebuild after level 3 (swap one talent in place of a pick) | Off | REVIEW m6 |
| Teachers and off-Facet talents | Off | Campaign-level |
| Lineage gifts (Minor, cast with Soul) | Setting Facets only | A setting module |
| Retainers and companions (Captain, Beast Friend) | Rules live in the talent text | Needs m7 fixed |
| Spotlight tokens across a fight (D10 option B) | Off | Only if G0 asks for it |
| Player-facing foe attacks (players roll to avoid) | Off | The BRIEF's G0 comparison |
| Morale | On | It's MM-side, but a table may prefer fights to the last foe |

### MM-SIDE (procedures the MM runs; never taught to players)
| Rule | Note |
|---|---|
| Act-break nomination | The MM prompts it |
| Group rolls (majority) | |
| Player against player (contest and tie) | |
| Trying again | |
| Unnarrated details (ask, don't assume) | A principle |
| When not to roll | |
| Reading 7–9 costs and 6− moves | |
| Level gap | Now part of base difficulty. The Very Hard band becomes guidance: "tell them head-on won't work" |
| Foe roles and attack counts (Standard/Elite/Boss) | The player sees them only as pips |
| Mobs: attack and damage bonus | |
| Mobs: damage and area drops | **NEW** |
| Bloodied | |
| Morale | |
| Monster level and role tables | |
| Reading a fight | Pending sim regeneration |
| Full-form and chaining (scope decided before the roll) | |
| Control workings on Elites and Bosses last one exchange | `[R2]` |
| Magic complications and mishap tables | The app offers two costs |
| Relics | The item text carries the rule |
| Curio limit, trinkets, hoards | |
| Coin per slot | |
| Usage die | The app tracks it |
| Heavy armor makes stealth Hard | The item text carries it |
| Hazard damage and armor where armor would help | |
| Pressure die | Players only need "time costs" |
| Threat Clock advance and fill | |
| Reaction roll | |
| Oracle and "stuck" | |
| Levels pacing and the five questions | |
| Surprise | **NEW one-liner:** a surprised side makes no attacks in the first exchange. It makes *Scout's Eye* mean something (REVIEW m10) |

### CUT
| Rule | Why |
|---|---|
| **The +4 ceiling** | It never changes a roll (REVIEW m4). Keep it as a note for Facet authors only |
| "Spend as many Sparks as you like" | Replaced by the two-dice cap |
| "One Help per roll" / "each helper adds a die" | Both replaced by the cap, which settles III.1's contradiction |
| "One Borrowed Trouble per roll" | Replaced by the cap |
| "5d6 is the most a roll can be" | False today. Replaced by the cap |
| The foe's natural-2 "opening, until you use it" | A lasting state that crossed scenes (m13). The double one is now just a miss |
| "A natural 2 does not force a failure" (players) | Replaced by the unified doubles |
| Very Hard band of the level gap (6+ levels) | MM guidance instead. One band is enough |
| Separate expiry text per effect (Studied Foe "next exchange", stunt "next attack", etc.) | One clock |
| "Easy"/"Hard" written as *set* difficulties in talents and picks (Defend, cover, Warding, stunt, Studied Foe, opening) | Reworded as Easier/Harder. The words stay; the stacking questions go |

**What is *not* cut, on purpose:** Borrowed Trouble, the peer Spark call, the Graceful Fail, the death choice, Hold On, the three 10+ picks, and foes rolling in the open. Players enjoy these. Each is one line, and each is "light but strong".

---

## 8. Consequences to carry into DESIGN (for the Planner)

1. `facet.yaml`:
   - add `roll_resolution.max_extra_dice: 2`;
   - replace `max_per_roll` on Help and Trouble;
   - add `difficulty.rule_effects: net_one_step`;
   - drop `bonus_cap`;
   - change `natural_low` for foes (a miss, no opening) and for players (6−, +1 Spark);
   - add `combat.actions_per_exchange: 1` and `combat.effects_expire: exchange_end`;
   - mob drop rates.
2. Engine:
   - one `net_difficulty(base, easier_flags, harder_flags)` used by PC attacks, foe attacks, casts and avoids;
   - enforce the dice cap;
   - enforce the action token and foe attack counts;
   - a stunt benefits others only;
   - the mob damage→drops rule;
   - `resolve_cast` goes through the attack path if ruling 2 lands.
3. App: the action token, attack pips, state chips and a one-click end of exchange (D10).
4. Books:
   - III.1 gets the cancel rule and the cap, and loses the +4 ceiling and the 5d6 line;
   - III.3 gets one action, reach, the one clock and doubles;
   - MM1 gets the mob rules;
   - MM5 is replaced by the MM card;
   - Quick Start's Combat in Five Lines is replaced by the card's Fight block;
   - every "is Easy/Hard" in talent text becomes "Easier/Harder".
5. A new docs invariant: the player card has no exception clauses (grep for "unless|except|does not count").
6. Sim: re-run the pacing ladder and the parity suite under the dice cap and the one-step rule, and check the ÷2 area drop.
7. G0: time the first roll and log every "am I allowed to…?" question in the first fight.

---

## 9. Licence table

| Source | Licence | Wording usable here? | Used for |
|---|---|---|---|
| D&D SRD 5.1 / 5.2 | CC BY 4.0 | Yes, with attribution (not used) | Presence/cancel logic |
| Knave (1e) | CC BY 4.0 | Yes, with attribution (not used) | One action, side initiative, spending advantage another way |
| Cairn (1e/2e) | CC BY-SA 4.0 | Legally yes, but ShareAlike attaches (not used) | One action, declare first, detachments, telegraphing, anti-pile-on (rejected) |
| Blades in the Dark SRD | CC BY 3.0 | **No** (outside the brief's 4.0 rule) | Two-bonus-dice cap, set up, Devil's Bargain lineage, clocks |
| Dungeon World SRD | CC BY 3.0 | **No** | Forward/ongoing, spotlight, Defend hold |
| 13th Age SRD | OGL 1.0a | **No** | Escalation die (not adopted) |
| The Black Hack | OGL 1.0a | **No** | Side order, usage die |
| OSE SRD / B/X | Site states "not open content" (incorporates SRD 5.1 CC BY material); B/X proprietary | **No** | Optional-rule labelling, referee-side procedure |
| Daggerheart SRD | DPCGL | **No** | Advantage die, die-for-die cancel, optional spotlight tokens |
| Draw Steel | DRAW STEEL Creator License | **No** | Edge/bane cap and cancel, flip-token, alternating sides (rejected) |
| Shadowdark | Shadowdark Third-Party License (not CC) | **No** | Evidence for the 5e scheme, awards |
| ICRPG | Proprietary | **No** | Visible target, Easy/Hard words, timers |
| Into the Odd / Bastionland | Proprietary | **No** | "Light but strong", saves-first, rulings transparency |
| Maze Rats | Not stated | **No** | Rules-to-tables ratio |
| Matt Finch, *Quick Primer* | Proprietary (free) | **No** | Rulings over rules |

**Credit implications:** the Credits should name Blades (Devil's Bargain lineage and the dice cap), 5e (the cancel concept), Knave/Cairn/ITO/TBH (one action, side order) and Daggerheart/Draw Steel (tokens and the cap, as influence). This fits the corrected Credits draft in `REVIEW_lean_prose.md` Appendix C.

---

## 10. Source list (URLs fetched this session)

1. https://www.5esrd.com/using-ability-scores/
2. https://www.dndbeyond.com/srd
3. https://en.wikipedia.org/wiki/Dungeons_%26_Dragons_5th_edition
4. https://www.thearcanelibrary.com/pages/shadowdark
5. https://www.thearcanelibrary.com/
6. https://www.thearcanelibrary.com/blogs/shadowdark-blog/faq-on-the-shadowdark-rpg-third-party-license
7. https://daggerheartsrd.com/ and https://daggerheartsrd.com/rules/
8. https://github.com/seansbox/daggerheart-srd (SRD 2025-09-09 text)
9. https://www.dungeonworldsrd.com/moves/
10. https://www.dungeonworldsrd.com/gamemastering/
11. https://www.dungeonworldsrd.com/playing-the-game/
12. https://bladesinthedark.com/action-roll
13. https://bladesinthedark.com/teamwork
14. https://bladesinthedark.com/progress-clocks
15. https://bladesinthedark.com/licensing
16. https://en.wikipedia.org/wiki/Blades_in_the_Dark
17. https://www.13thagesrd.com/combat-rules/
18. https://github.com/brunobord/the-black-hack
19. https://cairnrpg.com/second-edition/
20. https://cairnrpg.com/first-edition/cairn-srd/
21. https://github.com/yochaigal/cairn (2e core rules, principles, combat)
22. https://questingbeast.itch.io/knave
23. https://github.com/lskh/Knave (Knave 1e text, CC BY 4.0)
24. https://questingbeast.itch.io/maze-rats
25. https://freeleaguepublishing.com/games/into-the-odd/
26. https://www.bastionland.com/2022/05/graphene.html
27. https://www.bastionland.com/2016/04/oddular-mechanics.html
28. https://www.bastionland.com/2023/02/only-roll-initiative.html (via search listing)
29. https://www.bastionland.com/2020/10/kitbash-attitude.html (via search listing)
30. https://www.bastionland.com/2023/07/how-many-polearms.html
31. https://oldschoolessentials.necroticgnome.com/srd/index.php/Main_Page
32. https://en.wikipedia.org/wiki/Old_School_Renaissance
33. https://github.com/SteelCompendium/data-rules-md (Draw Steel Combat and The Basics chapters)
34. https://steelcompendium.io/v2
35. https://en.wikipedia.org/wiki/Matt_Colville
36. https://github.com/ClipplerBlood/icrpgme (ICRPG Foundry system)
37. https://www.runehammer.online/

**[unverified] items** (primary text not reachable this session): Shadowdark's exact stacking and initiative wording (§1.2); ICRPG's ±3 (§1.6); Into the Odd Remastered's exact first-round wording (§1.11). None of them changes a recommendation.
