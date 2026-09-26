# BRIEF: Lean Facets (v1.0 ruleset overhaul)

**Date:** 2026-09-25
**Tier:** Brain (run on Opus 5.5, as the owner authorised).
**Status:** Proposal. Nothing here is canon until the owner rules on §9. Revised the same day: enemies roll their attacks (§4.6, §4.6a). Every number is a starting value for the Planner's simulation, not a settled figure.

**Owner direction (verbatim where it binds):**
- *"Something simple like earlier D&D with flexibility and MM-driven variety."*
- *"I am fine with a complete overhaul if it makes it more fun."*
- *"I don't care much about how close we are to other games (so long as we don't cross copyright/licensing lines)."*
- *"Keep the core concept of facets, being broad 'parents' of classes with multiple classes they can take the shape of, but move the system under them to something genuinely fun."*
- *"It doesn't have to be concrete classes, it could be something like Morrowind where you can define your own classes within the larger framework."*

**Evidence base (read these for citations; this brief cites them by section):**

| File | What it covers | Sources |
|---|---|---|
| `RESEARCH_complexity_audit.md` | Why the current build is ~85 player rules, ~55 of them novel | the repo |
| `RESEARCH_lean_oldschool.md` | Pre-3e D&D, the OSR's reading of it, retroclone licences | 55 |
| `RESEARCH_lean_2d6_lineage.md` | Dungeon World and descendants, DW2, 13th Age, Daggerheart, Draw Steel, Cypher; dice-core maths; licences | ~60 |
| `RESEARCH_lean_nsr.md` | Knave, Cairn, Into the Odd, Mausritter, Black Hack, Shadowdark, Whitehack, DCC and others | ~45 |
| `RESEARCH_lean_mm_variety.md` | Referee procedures, monster formats, loot, digital GM-tool evidence, novice scaffolding | ~45 |
| `RESEARCH_lean_fun_evidence.md` | Motivation research, why D&D's primitives are fun, progression and class-choice data | ~55 |

---

## 1. The problem

The current ruleset is fast at the table but expensive to learn and to write for. By count it has about 85 player-facing rules, most of them invented here. It replaced D&D's plain primitives with small systems (Endurance + reactions + Condition tiers + armor budget instead of HP; points → marks → ranks → Facet levels → Techniques → Majors instead of level; readied intents by purpose instead of a spell count). The fun audit found the resulting combat short but shallow, and the fun dependent on an expert MM. No human has played it.

The owner wants the opposite trade: plain, familiar primitives on the sheet; variety supplied by the MM's side and the app; flexibility in who you can be; and the three Facets kept as the frame.

## 2. Goals and non-goals

**Goals**
1. **About 25 player-facing rules**, fitting on one double-sided reference card. The one-roll core stays.
2. **Familiar primitives, where each one serves a known motive** (`fun_evidence` §2, §7): HP, damage dice, armor, levels 1–10, loot, named abilities.
3. **Facets as specializations, Morrowind-style.** Body, Mind and Soul each hold several preset classes, and any player may define their own class inside a Facet.
4. **Variety from the MM's side**, delivered by the app as procedures and tables. Players never have to learn them.
5. **A reward loop pointed at the game's pillars**: discovery, treasure, goals, table moments. Never kills or rolls.
6. **Ten minutes to a playable character** from presets, and 5–10 minutes for a custom one.
7. **Everything we publish is original text**, with borrowed *ideas* credited.

**Non-goals**
- Tactical depth on the player's side (a grid, action economies, option menus). Tactics come from the situation the MM builds, not from a menu on the sheet (`fun_evidence` §7; `oldschool` §5 "nothing to do but attack").
- Compatibility with any other game.
- Preserving current mechanics for their own sake. Canon (setting, cast, lore) is preserved; mechanics are salvage.
- Grim lethality. The adventure register stays: death is legible and rare, with the death choice kept.

## 3. Approach selected, and what it was chosen over

**Selected: a D&D-shaped chassis on our 2d6 three-tier roll, the approach Dungeon World pioneered, rebuilt with OSR/NSR durability tricks and old-school MM procedures, under Facet specializations.**

| Alternative | Why rejected |
|---|---|
| **Trim the current system** (audit §3–6) | Still leaves ~50 mostly-novel rules and keeps the pieces the owner is questioning. The owner opened a full overhaul. |
| **d20 roll-high (5e-like)** | Most familiar, but a partial-success band has to be bolted on and is a flat 25%. 2d6 is the only core where partial success is the most common result (`2d6_lineage` Part 2). Our social economy (Sparks, Borrowed Trouble, Graceful Fail) is built on 2d6 and the +1d6-drop-lowest verb. |
| **2d10 / 2d12 duality (Draw Steel, Daggerheart)** | Heavier, proprietary licences, and adds a GM resource layer we don't need. |
| **Classless NSR (Knave, Cairn)** | Conflicts with the Facet → class constraint, and the evidence says growth-hungry players miss levels (`fun_evidence` §4.3). We borrow their *tricks*, not their structure. |
| **Straight Dungeon World** | Its documented failures (Defy Danger catch-all, move jargon, monotonous Hack & Slash, fiddly magic, expensive playbooks; `2d6_lineage` §1.1) are exactly what our Sparks, domain magic and Facet menus fix. And DW2's own designers went back to HP and six-stat familiarity (`2d6_lineage` §1.2). |

**The one-sentence thesis:** plain numbers on the sheet, rich procedures behind the screen, a reward loop that makes fighting optional, and a class system where the Facet owns every number and the class owns only words, things and picks.

---

## 4. The design

### 4.1 Core resolution *(kept, simplified)*

- **Roll 2d6 + stat (+1 if a knack applies).** 10+ full success; 7–9 success with a cost; 6− things go wrong and the story moves.
- **Difficulty:** Easy +1 / Standard / Hard −1 / Very Hard −2. The Easy-tag order of operations is gone.
- **One extra-die verb:** a Spark, a friend's help, or Borrowed Trouble each add +1d6, keep the best two.
- **Naturals, the Graceful Fail, and Sparks** (3 per session, earned from the MM, peers and act breaks) stay unchanged. The app makes peer awards visible, because Inspiration failed in 5e by being forgotten (`fun_evidence` §6).
- **Avoiding harm** (the old saving throw) is 2d6 + the stat that fits, with explicit, narrow triggers so it can't become Defy Danger (`2d6_lineage` §5.6).
- **Bonuses stay bounded:** stat at most +3, total at most +4. Characters grow through HP, options and loot, not bigger roll numbers (`2d6_lineage` Part 2).

### 4.2 Stats: three, named for the Facets

**Body, Mind, Soul.** At creation, your Facet's stat is **+2**; set one other to **+1** and the last to **+0**. At levels 4 and 8, add +1 to a stat (maximum +3).

This deletes nine Minor attributes, the derived-Major bracket table and the weapon-category → attribute table. Differences within a Facet (Mordai's strength against Zulnut's nimbleness) are carried by **knacks, kit and talents**. Morrowind puts the same distinction into skills, not attributes.

### 4.3 The Facet → class structure (Morrowind model)

**The Facet is a specialization. It owns every number that affects balance** (`oldschool` §6.2 on the 2e class-group precedent; `nsr` §5.2; `2d6_lineage` §5.3):

| The Facet owns | Body | Mind | Soul |
|---|---|---|---|
| Stat lean | Body +2 | Mind +2 | Soul +2 |
| Grit (HP) die | d10 | d6 | d8 |
| Talent menu | ~12 talents, each with an improved form | ~12 | ~12 |
| Signature list (level 3 picks) | ~6 | ~6 | ~6 |
| Magic tradition | none (canon) | **Thaumaturgy** (scholarly) | **Invocation** (intuitive) |
| Slots | 10 + Body | 10 + Body | 10 + Body |

**A class, preset or custom, owns only words, things and picks:**
1. **A name and a one-sentence concept** (Cypher's "I am an ___ who ___" pattern).
2. **Two knacks**: one from the class ("what you trained as") and one from your background ("where you come from"). A knack is a trade, place, people or tradition, never a bare verb. When one covers the task, add +1. Two knacks never stack (Whitehack model; `nsr` §5.3).
3. **A Specialty**: one narrow thing you never roll for *(kept)*.
4. **A starting kit**, chosen from the Facet's allowance and limited by slots (Knave's idea: the items *are* the role).
5. **Two talents** from the Facet menu at level 1, and **a signature** at level 3.
6. **For casters, a domain.** Casters are the Mind and Soul classes that take the *Domain* talent.

**Presets are saved bundles made from the same menu**, so a custom class can never be more complicated than a preset (`2d6_lineage` §5.5). Suggested three to four per Facet, names to be ruled by the owner:
- **Body:** Warrior, Scout, Guardian, Brawler
- **Mind:** Scholar-mage (Thaumaturge), Investigator, Tactician
- **Soul:** Invoker, Speaker, Wanderer (luck-touched)

**Evidence-driven defaults:**
- **Presets are the default path.** The Quick Start offers only presets, because choice overload hits people who don't yet know what they want (`fun_evidence` §4.4). Only 11% of D&D Beyond characters multiclass.
- **Free respec until level 3.** At level 3 the class takes its signature, which is the commitment moment, as with 5e 2024 subclasses and Bethesda's class-regret finding.
- **Off-Facet talents need a teacher found in play.** Morrowind's "outside your specialization is slower" becomes a story gate the MM controls, with no arithmetic. Durability and magic tradition never cross: no custom build gets a d10 caster or a Body mage.

**The cast as examples** (canon only, no new facts):
- Zahna: Mind, a preset Scholar-mage; background knack *Guild Apprentice*; domain *Inscription*.
- Mordai: Body, a preset Warrior; background knack *City Watch*.
- Zulnut: Body, a **custom** class, *Wandering Disciple*. This is the model custom build for the book.

Mordai's canon shoulder becomes a **Scar** (§4.5), which the new rules express directly.

### 4.4 Levels and growth

- **Levels 1–10.** About 90% of D&D games stop by level 10, and Shadowdark proves ten is enough (`fun_evidence` §4).
- **Every level:** roll your Facet's grit die (or take the average) for HP, plus one pick:
  - a new talent from your menu, **or**
  - the improved form of a talent you already have.
  - Level 3 is always your signature. Levels 4 and 8 also give +1 stat.

  Every level-up therefore gives a number and a new thing to do (`fun_evidence` §4.2).
- **The MM calls level-ups**, prompted by the app at session end. Players prefer that to tracking XP by about 3:1 (`fun_evidence` §4.1). The prompts are the reward loop:
  - *Did we discover something?*
  - *Bring treasure home?*
  - *Pursue a goal?*
  - *Change the world?*

  Kills and rolls count for nothing (`oldschool` §6.1). An optional **treasure-XP mode** serves tables that want the old-school loop.
- **Pacing target:** level 2 after session 1, level 3 after session 2 or 3, then one level every 2–3 sessions, reaching level 10 around session 22–25. That matches the median real campaign length of 24 sessions (`fun_evidence` §4.1). Advancement by use is gone; it's the known Morrowind failure mode.
- **Name level (9–10), optional:** a hold, a following, a school, a chapter house. This is the old-school endgame, and it runs on the faction procedure (§6).

### 4.5 Durability, damage and death

- **HP is grit:** near-misses, stamina and nerve. Level 1 HP = your grit die's maximum + Body. A **breather** of a few minutes restores half your max HP, and resting in the open risks a Pressure die roll. **A night's rest** restores everything (`nsr` §6.4c).
- **Weapons:** unarmed d4, light d6, standard d8, heavy (two-handed) d10, ranged d6 or d8. Heavy weapons are loud, light ones are hidden.
- **Armor subtracts from each hit:** light 1, heavy 2, shield +1, cap 3, and every hit does at least 1 (`nsr` §6.1). Heavy armor makes stealth Hard, and **a caster in heavy armor takes 1 extra Fatigue per full-form working**, an old-school trade with no prohibition.
- **At 0 HP you take a Wound** and roll **Hold On** (2d6 + Body):
  - **10+:** stand at 1 HP.
  - **7–9:** out of the fight but conscious.
  - **6−:** dying. An ally who tends you before the scene ends saves you; otherwise, **the death choice** *(kept)*.

  Wounds are the old Condition list renamed. Each fills an inventory slot and clears one per night of rest with treatment.
- **Scars (optional table, app-rolled):** landing on *exactly* 0 rolls a Scar instead of a Wound, and it's permanent (Cairn's idea). Mordai's shoulder is the canon example.

### 4.6 Combat: players roll to act, enemies roll to attack *(revised 2026-09-25 after owner feedback)*

The first draft kept "NPCs never roll". The owner's instinct is that players would rather enemies roll, and on review the case for switching is stronger than the case for keeping it. See §4.6a. The project's CLAUDE.md asks that `research/dice_system_analysis.md` not be overridden without documented reasoning; §4.6a is that reasoning.

1. **The MM sets the scene and telegraphs** what each foe is about to do and to whom ("the ogre swings at Mordai; the archers draw on Zahna"). This is still where the tactics come from.
2. **Players say what they do** (any order, no initiative) **and roll**:

| Result | If you attacked |
|---|---|
| **10+** | Deal your weapon die **and pick one**: +1d6 damage; a **stunt** (push, disarm, pin, or open it up so an ally's next attack on it is Easy); or **cover** an ally (attacks on them are Hard this exchange) |
| **7–9** | Deal your weapon die, **but you're exposed**: the next enemy attack on you this exchange rolls **an extra die, keep the best two**, the same verb as a Spark, turned against you |
| **6−** | You miss, and the MM makes a move |

3. **Then the enemies roll, in the open.** The app rolls **2d6 + the foe's attack bonus** (set by its level) for each attack, and a Mook mob rolls once:

| Enemy roll | Result |
|---|---|
| **10+** | A hard hit: damage **+2**, or its special |
| **7–9** | A hit: damage |
| **6−** | A miss |
| **Natural 12** | The MM names *something more* (the player's own rule, mirrored) |
| **Natural 2** | The target gets an opening: their next attack on that foe is Easy |

   Armor subtracts from damage (§4.5).
4. **Defend:** skip your attack, and every attack on you this exchange is **Hard** (−1). **Intercept:** as Defend, but you also take the attacks aimed at an ally.
5. **Foe level cuts both ways.** Your attacks on a foe **3+ levels above you are Hard**, and its attack bonus rises with its level.
6. **Spark, Borrowed Trouble and help work on your rolls as before.** The MM may offer Borrowed Trouble on an enemy roll ("the ogre's swing lands on your shield, and the shield splits").

Casters out of reach take no counter-blows by construction, which fixes DW's "trading blows kills the wizard" (`2d6_lineage` §3.1). The Tactician's depth lives in the 10+ pick, Defend, Intercept, cover, Easy for preparation, and monsters with gimmicks, not in a menu.

#### 4.6a Why enemies roll: the reasoning that overrides "NPCs never roll"

| | Player-facing only (first draft) | Enemies roll (adopted) |
|---|---|---|
| Familiarity | Novel to most D&D players | What every D&D player expects, and what early D&D did. That's the owner's target. |
| Table drama | Loses the shared moment of the MM's dice in the open (`dice_system_analysis.md` names this cost itself) | The MM's natural 12 against Mordai is a moment the whole table watches |
| Enemies feel alive | NPCs "read as inert unless the MM narrates hard" (same file) | Foes visibly try and fail. A goblin can whiff; an ogre can crush. |
| Variance | Concentrated on the player, who rolls both to act and to avoid (Cypher's most-cited complaint) | Spread across the table |
| MM load, the original reason for the rule | Lowest | **The app rolls every enemy attack in one click** and shows it to the table. In 2026 the bookkeeping cost that justified the rule is mostly gone for a digital-first game. |
| Player agency when attacked | High: your roll decides | Lower. Answered by Defend, Intercept, cover, armor, and the 7–9 exposure being your own choice to attack |
| Dice per fight | Fewer | About 40% more (scratch model), nearly all of them app clicks |
| Rule count | ~25 | ~25 (the "attacks aimed at you" rule becomes "enemy rolls"; Defend is simpler) |

**Evidence caveat:** the research found **no survey data** on whether players prefer the GM to roll. This is a judgment call on familiarity and table drama, not a measured preference. It's also the cheapest thing to test: **G0 can run one fight each way** and ask the table.

**What stays player-facing:** outside combat, NPCs still don't roll against players. A guard's alertness sets the difficulty of your Stealth roll. The MM-side procedures (reaction, morale, Pressure die) are MM rolls by nature. Only attacks change.

**Scratch pacing check.** This is a throwaway back-of-envelope model, deliberately not committed, because project simulations must drive `combat.py`. The Planner re-runs it properly. Four level-1 PCs with +2 attacks, d6–d8 weapons, 6–10 HP. Enemy attack bonus +0 for Mooks, +1 for standard foes, +2 for elites and Bosses.

| Encounter | Median exchanges | Chance any PC drops | Party HP lost | Dice per fight |
|---|---|---|---|---|
| 4 Mooks | 1 | 0% | 3% | 5 |
| 2 standard foes (HP 8, dmg 3) | 1 | 2% | 6% | 6 |
| 3 standard + 2 Mooks | 3 | 34% | 33% | 14 |
| 1 elite (HP 16, dmg 4, attacks twice) + 3 Mooks | 2 | 45% | 34% | 10 |
| Boss (HP 32, dmg 5, attacks twice, armor 1), no morale | 3 | 73% | 55% | 13 |

The ladder keeps the right shape: Mooks are trivial, mixed groups are real, and a level-1 Boss is deadly. Under the player-facing draft the same encounters ran 1 / 2 / 3 / 3 / 4 exchanges with somewhat higher danger. Standard foes are now a touch soft (the Planner raises their damage or bonus). Morale ends most non-Boss fights early.

### 4.7 Monsters: one card, one dial

**Level** (1–10) sets HP, damage and attack bonus from a single app table. **Role** multiplies: Mook (drops to any hit, fights in mobs), Standard, Elite (×2 HP, acts twice), Boss (×4 HP, acts twice, a phase when Bloodied). The card then holds the texture (`mm_variety` §2.2; `2d6_lineage` Part 3):

**WANTS · SPECIAL** (one gimmick) **· WHEN BLOODIED** (the escalation at half HP) **· TELLS · BREAKS** (morale number + what it does) **· TWISTS** (d6) **· NASTIER** (optional).

The Threat Rating arithmetic and the Resolve/Condition asymmetry are gone. The existing `.fof` conduct fields (`disposition / triggers / morale / negotiation`) migrate almost unchanged; they were already better than most OSR stat blocks (`mm_variety` §6).

### 4.8 Magic: keep Domain + Intent + Scope, make the limit physical

- **Casting:** 2d6 + Mind (Thaumaturgy) or Soul (Invocation), +1 if a knack applies. State intent and scope.
- **Scope sets cost** (D25's full-form rule is kept: meaningful power or precision is never Minor):

| Scope | Difficulty | Cost | Notes |
|---|---|---|---|
| Minor | Standard | free | Never deals damage and never decides anything; in a fight it's a stunt |
| Significant | Standard | **1 Fatigue** | A harmful working deals d8 to one target |
| Major | Hard | **2 Fatigue** | Level 3+. 2d8 to a group, or a scene-changing effect |

- **Fatigue fills an inventory slot** and clears with a night's rest. The caster's spell budget, carrying capacity and wound buffer are **the same ten-odd slots**, so a caster who casts a lot is one bad hit from trouble. Whitehack's playtests found HP-cost casters were not stronger than the other classes (`nsr` §6.3). This **replaces readied intents and their purposes** (D23), and ties into the heavy-armor rule in §4.5.
- **Signature workings:** a caster names two favourite workings at creation (one more at levels 5 and 9), and they're one step Easier. That gives casters a "my fireball" identity without a spell list (`fun_evidence` §8.12). It **replaces domain types** (Focused/Standard/Prismatic); breadth is now a talent (*Wider Domain*: a second domain, one step Harder).
- **7–9:** it works; the player picks one of two costs the app offers from the magic complication table. **6−:** a roll on one shared mishap table, and the Graceful Fail applies.
- **Before level 3** a caster can't attempt Major workings. That's the whole formalization rule now.

### 4.9 Gear, slots and loot

- **About 10 + Body slots.** Most items take 1 slot, and small items bundle. **Wounds and Fatigue take slots too**, so one track replaces encumbrance, Endurance, the armor budget and Tier-1 Conditions (`nsr` §6.1.5). The app handles the bookkeeping, and it still works on paper.
- **Usage die** for torches, arrows and rations: roll after a scene of use, and on 1–2 the die steps down (d8 → d6 → d4 → out).
- **Loot from session one** (`fun_evidence` §8.6; `mm_variety` §3.2):
  - **Coin** buys gear and carousing.
  - **Curios** are one-use wonders; carry 3.
  - **Relics** have a strange power and a quirk.

  All three come from app tables. This is the Power Gamer's carry-forward reward, and it's pure MM-side variety.

### 4.10 Lineage and setting Facets

Human is the default *(kept)*. A setting's lineage gift is a **third knack** or a **Minor-only domain**. Val'loh's gifts are already always-on Easy tags, which is a knack in all but name, so the Oraga material converts cleanly. A setting Facet can add classes (one card each), talents, relics and tables. It never adds core rules.

---

## 5. The player's rule count

Here are the rules a player must know, which is the budget the Planner defends:
1. The 2d6 roll and its tiers.
2. Difficulty.
3. The extra die (Spark, help, Borrowed Trouble).
4. Naturals.
5. Earning Sparks.
6. The Graceful Fail.
7. Borrowed Trouble.
8. Knacks and Specialty.
9. Avoiding harm.
10. Exchanges.
11. Attacks and damage.
12. The 10+ pick.
13. Enemy attack rolls (read, not rolled, by the player).
14. Defend and Intercept.
15. Armor.
16. Foe level shifts difficulty.
17. 0 HP: Wound and Hold On.
18. The death choice.
19. Rest and recovery.
20. Slots and the usage die.
21. Magic scope and Fatigue.
22. Magic 7–9 and 6− results.
23. Signature workings.
24. Levels and picks.
25. Curios and relics.

That's **25**, against about 85 today. Talents are opt-in complexity, so each player learns only their own (`complexity_audit` §4.1).

## 6. The MM's toolbox (where the variety lives)

This is the P0 list from `mm_variety` §7, adopted as the MM-side content target. **None of it is a player rule.** All of it is one or two clicks away in the app, private by default, logged, editable and printable. Every suggestion offers **three options, not one** (`mm_variety` §4.2).

| # | Tool | Content | Why |
|---|---|---|---|
| 1 | **Reaction roll** (2d6, five bands) + *what they want right now* (d66) | ~41 entries | Most encounters stop being binary (`oldschool` §1.5) |
| 2 | **Morale** (one number per monster; triggers: first to fall, half down, leader down) | 1 procedure | The single biggest lever on fight length (`nsr` §2.7) |
| 3 | **Pressure die** (overloaded encounter die): generic plus 4 terrain variants | ~30 entries | One roll per exploration turn replaces several timers (Necropraxis) |
| 4 | **Complication tables**: the d6 Trouble Table as index, plus a d66 per pillar (fight, explore, social, magic) | 144 entries | Fixes the novice-MM "invent a cost from nothing" failure (fun audit §8.3) |
| 5 | **Monster cards** (§4.7), each with a d6 twist table | 40–60 cards | The enemy texture that was "built, unshown" |
| 6 | **Loot**: trinkets d66, curios d66, relics d20 | ~92 entries | The carry-forward reward |
| 7 | **NPC generator** (setting-neutral until the owner rules on Shattered Origin names) | ~250 entries | Instant cast |
| 8 | **2d6 oracle** (yes / yes-but / no, with naturals as "and") | ~72 prompts | Also enables solo and duo play later |
| 9 | **Novice defaults**: Standard is the preset difficulty; 7–9 shows the cost menu; no turn order anywhere; a **Stuck?** button offering three options from the MM's own prep | software | The three observed novice errors |
| 10 | **Threat Clocks** *(kept)* with named portents per segment (fronts) | 12 samples | World motion |

P1 (prep card, three-clue checker, faction turn, rumor tables, site generator, journey procedure) and P2 (optional AI assist confined to the campaign's own tables and log, and solo mode) follow as in `mm_variety` §7. The iron law against inventing canon applies to generated content as well: nothing enters setting files without the MM accepting it.

**Guard rail (`oldschool` §6.4):** the app automates *procedures written in the MM Manual*. It never adds player-side options the book doesn't have. That's the existing "the simulator may only drive `combat.py`" principle, extended.

---

## 7. Licensing and copyright

- **Ideas are free; wording is licensed.** Game mechanics aren't copyrightable in the US; text, and the creative arrangement of tables, is (`oldschool` §4). **Policy: every sentence and table we publish is original.** Borrowed ideas are credited on one acknowledgements page in the PHB and MM Manual (Dungeon World, Knave, Cairn, Into the Odd, Whitehack, Black Hack, 13th Age, Necropraxis, The Alexandrian, Sly Flourish, Morrowind, and others).
- **Wording we *could* adapt if ever needed**, with attribution:
  - CC BY 4.0: SRD 5.x, Knave 1e, Ironsworn/Starforged, the Mausritter SRD, the Lazy GM Resource Document.
  - CC0: the Worlds Without Number SRD, per `2d6_lineage` (verify first).
  - CC BY-SA 4.0: Cairn, Stonetop, Basic Fantasy 4e. These are one-way compatible into GPLv3, and adapted files become GPLv3. Our `LICENSE.txt` is GPLv3.
- **Ideas only:**
  - CC BY 3.0 (Dungeon World, World of Dungeons, Blades SRD): not formally GPL-compatible.
  - CC BY-SA 3.0 (Homebrew World, Freebooters).
  - Anything under the OGL (Black Hack, Whitehack, 13th Age, DCC, OSE, OSRIC, Labyrinth Lord).
  - Proprietary or custom licences (Daggerheart, Draw Steel, Cypher, Shadowdark, Troika!, Into the Odd).
  - CC BY-NC (Principia Apocrypha).
- **Unverified licences** (the agents' search budget ran out): Knave 2e, Black Sword Hack, Macchiato Monsters, Tiny Dungeon, ICRPG, the Mark of the Odd terms, the DW2 beta, and the exact CC version of World of Dungeons. **Treat them all as ideas-only.**
- **Names:** no product names or trademarks in rules text ("Hack & Slash", "Defy Danger", "cypher" and similar). Our terms stay our own: Mirror Master, Spark, Graceful Fail, Borrowed Trouble, knack, grit, curio, relic, Pressure die.

## 8. Robustness and risks

| Risk | Mitigation |
|---|---|
| **Sunk cost and churn.** The PHB rules text (~55k words), `facet.yaml`, the engine, most of the ~1,700 tests, Bestiary stat blocks and Oraga statlines all get rewritten | What survives is what sets the game apart (setting, cast, prose voice, vignettes, the MM Manual's advice, Oraga's structures, the app shell, Threat Clocks, the Spark economy, domain magic). Tag the current state `v0.3-final` first. |
| **Lethality creep** (HP + damage + 7–9 trades) | The out-of-reach rule, Defend and Intercept, Hold On, the death choice, morale, and a Planner lethality target (for example, ≤1 PC death per 10 sessions at default). |
| **Monotonous attacking** (DW's Hack & Slash complaint) | The 10+ pick, monster gimmicks and Bloodied escalations, terrain Easy, morale. Measure it at the playtest by asking *fast or flat?* |
| **Bounded 2d6 vs growth over 10 levels** | Growth comes through HP, talents and their improved forms, signatures, loot and name level. Foe level shifts difficulty. The roll bonus stays ≤ +4. |
| **Fatigue slots make casters too weak, or too strong with few items** | The sim tests casts per day against gear load; the dial is slot count or Major cost. |
| **Custom classes break things** | No custom numbers: the Facet owns durability and magic, talents are options rather than +N, off-Facet needs a teacher, and the app enforces the build. |
| **More dice per fight** now that enemies roll | The app rolls each enemy attack in one click, a mob rolls once, and morale shortens fights. The playtest clocks it. |
| **App dependence** | Every procedure also prints as a table. Slots, usage dice and HP work on paper. |
| **Still no human playtest** | **Gate G0 (below): a two-page draft played by a human table before the full rewrite.** |

## 9. Decisions the owner must make (blocking, in this order)

1. **Go / no-go on the overhaul**, with gate G0: a two-page Lean Facets draft plus a four-player human session before the books are rewritten.
2. **Enemies roll their attacks** (§4.6a), overriding the player-facing "NPCs never roll" rule in `dice_system_analysis.md`. Recommended: yes, and A/B it in G0.
3. **HP and damage dice for PCs.** This reverses **D26**. Recommended: yes.
4. **Three stats (Body/Mind/Soul)** replacing nine Minor attributes. Recommended: yes.
5. **Magic limit: Fatigue in slots** (replacing **D23** readied intents) versus keeping readied intents as slot-taking foci. Recommended: Fatigue.
6. **Domain types replaced by signature workings.** Recommended: yes.
7. **Inventory slots as the unifying track** (gear, Wounds, Fatigue). Recommended: yes.
8. **Levels by MM call with prompts**, with optional treasure-XP mode. Recommended: yes.
9. **Preset class names and counts per Facet** (§4.3 list is a draft).
10. **Can relics give a Body character magic, or does "Body has no magic" extend to items?** (Also the fate of II.3's *A Brief Note on Body Magic* paragraph, already an open question.)
11. **Scars table: in or out.** Recommended: in, as optional.
12. **Which Shattered Origin names, cultures and factions may appear in generator tables.** Until then, tables ship setting-neutral.
13. **Branch hygiene:** merge PR #30 (Lineage, Val'loh, Oraga canon) first, then build Lean on a fresh branch. Recommended: yes, and stop work on `fix/engine-housekeeping`, whose engine is about to be replaced.

## 10. Handed to the Planner

- **Constraints:** the 25-rule player budget (§5); the Facet owns every number; no advancement by use; enemies roll attacks in the open via the app, NPCs never roll against players outside combat; `combat.py` stays the single rules module the sim drives; all text original; nothing invented for canon.
- **First deliverables (after owner rulings):**
  1. **`docs/DRAFT_lean_facets_two_page.md`**: the player card and the MM card.
  2. A `facet.yaml` v1 schema.
  3. Talent menus (~12 per Facet, each with an improved form) and signature lists (~6 per Facet).
  4. 3–4 presets per Facet.
  5. The level → HP/damage monster table.
  6. Three monster cards (Mook, Elite, Boss).
  7. Simulation of §4.6 and §8's risks: lethality, caster Fatigue, boss tuning, mob scaling, and whether the 10+ pick has a dominant option.
- **Open technical questions:**
  - Does a breather restore half HP or a grit die?
  - Is Defend's 7–9 half damage, or armor-only?
  - Mook mob scaling.
  - HP by die or fixed per level.
  - How the Oraga pregens and the existing `.fof` characters migrate.
- **Gate G0 → G1:** two-page draft → one human session (clocked; ask *fast or flat*, *did anyone miss a rule*, *could the MM keep up*) → only then the PHB / MM Manual / Bestiary / engine rewrite, following the sync workflow in CLAUDE.md.

**Resolved at Brain tier, pending owner rulings in §9. Return to Planner to continue from §10 once the owner has ruled.**
