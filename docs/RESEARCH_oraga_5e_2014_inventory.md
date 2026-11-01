# RESEARCH — Oraga Night 5e: 2024 → 2014 conversion inventory

Status: COMPLETE (2026-10-31). Survey only; no module file was edited.
Read-only survey of `conversions/dnd5e/oraga_night/` (paths below are relative to it).
Nothing under `references/` was read. `player_characters/` ignored as instructed.
Counts are `grep -c` line counts over chapters 01–11 + README unless stated.

## 0. Existing 2014 notes in the module (starting list)

- `README.md:16-17` — "written against the SRD 5.2.1. A 2014 table can play it with the short glossary in chapter X ... and rebuilt pregens."
- `README.md:134`, `03_Masks_and_Agendas.md:51`, `11_Pregenerated_Characters.md:48` — gifted human takes the gift as a bonus feat at 1st level ("the variant human's feat"). **Licence flag, §6.**
- `01_Overture.md:134-136` — claims the module runs at a 2014 table with the *At a 2014 table* notes; "Only the pregenerated characters need rebuilding." (This survey says that understates it; see Biggest risks.)
- `01_Overture.md:399-400` — Heroic Inspiration → plain Inspiration (Advantage instead of reroll).
- `10_Bestiary.md:57-87` — **DM Note — at a 2014 table**: Emanation, Utilize, Magic action, Bloodied, Study/Influence, Immunities line, "has the Prone condition", save-as-list, Initiative score, Heroic Inspiration, encounter multiplier.
- `10_Bestiary.md:2241`, `08_Handouts.md:438` — releasing a crystal charge = Magic action ("an action, at a 2014 table").
- `11_Pregenerated_Characters.md:46-48` — rebuild ability scores and class features.
- `09_The_Snakes.md:113-114` — read chapter X's box first; 2014 guide rates fights harder.
- `STYLE_5e.md:27` — "One DM Note explains the 2014 multiplier."

Gaps in the existing box: it does not cover the pregen-only terms (D20 Test, Weapon Mastery, origin feats, Resourceful/Skillful/Versatile, Divine Order, Tactical Mind, Steady Aim timing), the changed spells (Vicious Mockery, Spiritual Weapon, Cure Wounds…), the PC grapple rule (Unarmed Strike (Grapple)), the Potion of Healing action economy, Hit Dice/rest differences, or the 2014 Lore-bard/Thief/Evoker/Life/Champion feature differences.

---

## 1. Term / mechanic inventory

| # | 2024-only term or mechanic | Lines (by file) | Examples | 2014 equivalent |
|---|---|---|---|---|
| 1 | **Initiative score** "+3 (13)" in stat blocks | 29, all `10_Bestiary.md` | 10:228 Attendant "+3 (13)"; 10:1631 Sect Guard "+1 (11)" | 2014 blocks have no Initiative line; DEX mod rolls. Strip "(NN)"; any Advantage folded into the score (10:54-55) must be re-expressed as a trait or dropped |
| 2 | **Save row** in the ability table (`\| Save \|`) | 29, all ch. X | 10:236 Attendant; 10:1640 Sect Guard | 2014 lists only proficient saves on a **Saving Throws** line; the Mod row becomes "18 (+4)" format |
| 3 | **Gear** line, bare AC | 20, ch. X | 10:1642 Sect Guard "Chain Shirt, Shield"; STYLE_5e.md:28 | 2014: "**Armor Class** 16 (chain shirt, shield)"; no Gear line |
| 4 | **Immunities** single line (damage; conditions) | 5 in ch. X (Attendant 238, Hollow 1172, Radiant 1453, Wept 1989, Vell) | 10:238 "Poison, Psychic; Charmed, Exhaustion, Frightened, Poisoned" | Split into **Damage Immunities** and **Condition Immunities**; Resistances → **Damage Resistances** (4 blocks) |
| 5 | **"*Melee Attack Roll:* +7, reach 5 ft. *Hit:*"** | 27 Melee + 8 Ranged, ch. X | 10:320 Joined Hands; 10:1661 Cudgel | "*Melee Weapon Attack:* +7 to hit, reach 5 ft., one target. *Hit:*" (and Ranged Weapon / Melee Spell Attack) |
| 6 | **Save as list**: "*Strength Saving Throw:* DC 15, … *Failure:* … *Success:* Half damage." | 11 save lines (ch. X), *Failure:* 12 (ch. X 11, ch. V 1), *Success:* 6 | 10:325-327 Put Aside; 10:500 Honor Guard; 05_The_Longest_Night.md (1 Failure, 2 Success) | "Each creature … must make a DC 15 Strength saving throw. On a failed save, … On a successful save, it takes half as much damage." |
| 7 | **CR line "CR 8 (XP 3,900; PB +3)"** | 29, ch. X (10:241 … 10:2165) + **Table X–2** (10:113) labelled SRD 5.2.1 | 10:241; 10:2165 Vell "CR — (XP 0; PB +4)" | 2014: "**Challenge** 8 (3,900 XP)"; PB not printed in SRD 5.1 blocks (it is in later books). CR→XP values are identical in both editions, so only the format changes |
| 8 | **Bloodied** | 26 lines: ch. X 14, ch. IX 10, ch. IV 1, ch. XI 1 | 10:1224 ***Bloodied.*** trait (Hollow); 09:1248 knives break at first Bloodied; 11:416 Preserve Life "Bloodied creatures" | No term in 2014; write "at or below half its hit point maximum" (box already says so). 2014 Preserve Life wording is "no more than half its hit point maximum" — same effect |
| 9 | **Heroic Inspiration** | 45 lines in 9 files: ch. IX 17, ch. II 9, ch. V 5, ch. XI 5, ch. I 3, README 2, ch. IV 2, ch. VIII 1, ch. X 1 | 01:395-400 rule + **Table I–3** (01:415); 02:278/304 agenda **Pays** lines; 11:33 Resourceful | 2014 **Inspiration** (DM-awarded, Advantage on one attack/save/check, chosen before the roll; may be given to another PC). Table I–3 still works; the "reroll" text (01:395) and Resourceful start/regain do not exist in 2014 |
| 10 | **Magic action** | 4: 08:438, 10:68, 10:2241, 11:185 | 10:2241 releasing a charge; 11:185 Fast Hands | "Use an Object" (magic item) / "Cast a Spell". Fast Hands 2014 cannot use a magic item (only Sleight of Hand, thieves' tools, Use an Object) — see §4 |
| 11 | **Utilize action** | 4: 09:815, 09:823, 10:67, 11:184 | 09:815 lifting the bar "a Utilize action"; 09:823 searching through the grille | **Use an Object** action |
| 12 | **Study / Influence / Search** actions | Only named in the glossary (10:72). No body text uses "the Study action"/"Influence action"/"Search action" (B8 "Raunu's Study" and card S8 "The Study Door" are place names, not the action) | 10:72 | 2014: plain ability checks; Search is a 2014 action too. Glossary line can be shortened |
| 13 | **Emanation** | 4: 10:64 (glossary), 10:325 Put Aside, 10:508 Honor Guard *Flare*, 10:2271 *House Flare* row; also 08 Handout 3 *House Flare* row | 10:325 "20-foot Emanation originating from it" | "each creature within 20 feet of it" (sphere centred on self, self excluded) |
| 14 | **D20 Test** | 1: 11:99 (Bardic Inspiration) | 11:99 | "ability check, attack roll, or saving throw" |
| 15 | **"has the X condition"** wording | 10 strict "has the X condition" (ch. X 8, ch. IX 2); 28 lines "Prone condition"/"Grappled condition" (ch. X 20, ch. IX 6, ch. I 1, ch. V 1); also Blinded/Invisible/Frightened+Incapacitated condition forms | 10:391 "has the Grappled condition (escape DC 12)"; 05:289 "have the Prone condition"; 01:171-172 style rule | "is grappled (escape DC 12)", "is knocked prone". Lower-case conditions in 2014 house style |
| 16 | **Exhaustion** | 4, all condition-immunity lists (10:238, 1172, 1453, 1989). No 2024 −2/level exhaustion rule anywhere | 10:1172 | 2014 condition immunity "exhaustion" — no rules change needed |
| 17 | **Weapon Mastery** (Nick, Vex, Sap, Graze) | 9 lines, all ch. XI (Pello 168, 178; Dassa 326, 338). "Slow"/"Push" hits elsewhere are the *Slow* spell and prose, not mastery | 11:168 Nick; 11:178 Pello mastery list; 11:338 Dassa list | Does not exist in 2014. Delete; Pello's off-hand dagger becomes two-weapon fighting as a **bonus action** (competes with Cunning Action) |
| 18 | **Origin feats / background ASIs / background-granted feat** | origin feat: 16 lines (ch. III 7, ch. XI 6, README 2, ch. I 1); background "Abilities: … (+2, +1)" on all 5 pregens; 03:16-21 build rules | 03:16-18 "three ability scores to raise … an origin feat"; 11:76-77 Minor Scion; 03:49 gifts "is an origin feat" | 2014: background gives skills/tools/languages/feature + equipment, no ASI, no feat. ASIs come from race. See §6 for the feat problem |
| 19 | **Species traits Resourceful / Skillful / Versatile** | 11 lines (ch. XI 8, ch. III 3) | 11:32-34 common block; 03:22-23, 03:50, 03:134 | SRD 5.1 human: +1 to all six scores, Common + one language, nothing else. Variant human (feat + skill) is **PHB-only, not SRD 5.1** (§6) |
| 20 | **Gift feats as origin feats, Thenya/Orthaen/Phern** | ch. III 45–135 (whole "The Gifts" section); pregen Feats lines | 03:49-80; 11:82, 159, 235, 393 | Module's own content (GPL). Needs a 2014 delivery route that does not rely on variant human (§6) |
| 21 | **2024 feats named**: Alert (origin version: swap Initiative), Savage Attacker, Skilled, Magic Initiate | ch. XI 7, ch. III 1 (Magic Initiate 03:58) | 11:81 Alert; 11:315 Savage Attacker; 11:159 Skilled | SRD 5.1 contains **only Grappler**. 2014 Alert (+5 init, can't be surprised) / Savage Attacker / Skilled / Magic Initiate are PHB-only and differ in text |
| 22 | **2024 spell versions** | ch. XI sheets; ch. III gift list; ch. V/IX/X spell-answers | 11:91-93 *Vicious Mockery* 1d6 (2014: 1d4 at 4th); 11:405 *Spiritual Weapon* "Concentration" (2014: not concentration, 1d8+mod); *Guiding Bolt*/*Cure Wounds* dice (2014 Cure Wounds 1d8 vs 2024 2d8 — check sheets that compute healing); *Sleep* (2024 save-based vs 2014 5d8 HP pool; 09:2039, 10:162, 05:469, 05:845); *Guidance*/*Resistance* (2024 reworded; gift list 03:75-77); *Hideous Laughter*, *Tiny Hut* names are SRD 5.1 names too | Re-check every spell line against SRD 5.1 text; SRD 5.1 uses the un-named forms (*Hideous Laughter*, *Tiny Hut*) so names survive |
| 23 | **Spell styling** (italic Title Case: *Mage Armor*) and **equipment Title Case** (Longsword, Chain Shirt, Thieves' Tools, Component Pouch; O16) | Pervasive: STYLE_5e.md:21-22; 01:169-172 states it | 11:105 "Dagger · Fine Clothes · Studded Leather Armor"; 10:1642 Gear | 2014 house style: lower-case italic spells (*mage armor*), lower-case equipment, lower-case conditions/advantage. Purely stylistic; owner choice whether to change (linter enforces current form) |
| 24 | **Rules-term Title Case** (Advantage, Hit Points, Short Rest, Difficult Terrain, Dim Light, Bonus Action…) | Pervasive: ~150 lines of Advantage/Hit Points/etc. alone (ch. X 53, ch. IX 35, ch. XI 25, ch. V 18…) | 01:171; 04:308 "Short Rest"; 05:473 "Difficult Terrain" | 2014: lower case. Stylistic |
| 25 | **Hit Point Dice** | 0 uses. Module writes **Hit Dice** (11:64 etc., 5 lines) and "Hit Die" (01:405, 04:1378) | — | Already 2014-compatible (only casing) |
| 26 | **Short / Long Rest** | 8 + 8 lines | 01:402-405 no Long Rest, one chapel Short Rest; 04:1378 spend one Hit Die at the toast; 11:333 Second Wind "one back on a Short Rest" | Rest rules are near-identical; differences live in class features (2014 Second Wind 1/short rest; Channel Divinity 1/short rest at 4th; Bardic Inspiration long rest until 5th — same) |
| 27 | **Encounter budget Low/Moderate/High** (no multiplier), "beyond High" | 61 lines (ch. IX 59, ch. X 2); every card's *Budget:* line (09:642, 733, 863, 975, 1037, 1107, 1223, 1331, 1655, 1962 …); **Table IX–1** (09:155) and 4 references (05:380, 09:95, 10:19); per-character numbers 10:16-19, 09:108-110 | 09:863 "850 XP — between Low and Moderate"; 09:1962 S14 "beyond High while Focused" | 2014 DMG thresholds (4th: Easy 125 / Medium 250 / Hard 375 / Deadly 500 per PC) **with group multiplier**. 2024 Low/Mod/High for 4th (250/375/500) = 2014 Medium/Hard/Deadly *before* multiplier. Every card label shifts. The DMG threshold table is **not in SRD 5.1** (§6) |
| 28 | **"Deadly"** banned in budget lines | 1 (10:85 in the 2014 box) | STYLE_5e.md:27 | 2014 vocabulary is Easy/Medium/Hard/Deadly — style rule and linter must flip |
| 29 | **PC grapple as Unarmed Strike (Grapple)** with escape DC | 05:453 Table (Hold him in the shallows); also "escape DC" on PC-facing effects | 05:453 | 2014: grapple is a special Attack-action option, contested Athletics vs Athletics/Acrobatics |
| 30 | **Potion of Healing** (2024: Bonus Action to drink; 2d4+2) | 01:405, 04 B10, 10:2293-2297 | 10:2296 "the SRD's Potion of Healing" | 2014: action to drink, same 2d4+2. Module does not state Bonus Action anywhere found; only casing changes |
| 31 | **Knocking Out a Creature** | 09:139-141, 10:43 | — | Same rule in 2014 (melee only); house extension stands |
| 32 | **"the SRD's table calls a DC of 15 Medium"** | 01:373 | — | True in both editions |
| 33 | **Bastion** | 0 | — | Not used |
| 34 | **SRD 5.2.1 attribution / version strings** | 20 lines "5.2.1" in 5 files + STYLE_5e.md + tools | Attribution blocks: **README.md:117-120**, **09_The_Snakes.md:8-11**, **10_Bestiary.md:7-10**, **11_Pregenerated_Characters.md:9-12**. Version mentions: README:3, README:16; 01:134, 01:171; 09:108, 09:155; 10:3, 10:17-18, 10:62, 10:113; 11:3 | SRD 5.1 attribution: "This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode." |

---

## 2. Per-file summary

| File | 2024 load | What kind |
|---|---|---|
| `README.md` | A few lines (but load-bearing) | SRD 5.2.1 rules line (3, 16), attribution (117-120), *Changes from the SRD* (122-135): origin feats, Heroic Inspiration, "four SRD backgrounds", pregen "class-feature text adapted from the SRD", the variant-human 2014 line |
| `STYLE_5e.md` | A section (rules table) | The whole Title-Case convention is declared as SRD 5.2.1 (line 4, row "Rules-term capitals", "Spells", "Stat blocks", "Difficulty vocabulary"). Rewriting for 2014 means rewriting rows 20–28 |
| `01_Overture.md` | A section | *What You Need* (132-136), *Reading This Book* style line (171), Heroic Inspiration rule + Table I–3 (395-430), rests (402-405). Everything else is setting/procedure |
| `02_The_World_and_the_Night.md` | A few lines ×9 | Every agenda **Pays:** line awards Heroic Inspiration (278, 304, 322, 366, 389, 436, 455, 498, 517). Word swap only |
| `03_Masks_and_Agendas.md` | A section, structural | Character-build rules (11-27: SRD Human, "background in the SRD's shape" with ASIs + origin feat, four SRD backgrounds), *The Gifts* as origin feats via *Versatile* (45-135), ungifted take any origin feat. Needs a real 2014 redesign, not a gloss |
| `04_The_Ball.md` | A few lines | Heroic Inspiration (17, 704), Bloodied (61), Short Rest (308), Hit Die at the toast (1378-1379). Style casing throughout |
| `05_The_Longest_Night.md` | A few lines | One save-as-list (*Failure:*/*Success:*), Prone condition (289), Unarmed Strike (Grapple) (453), Table IX–1 ref (380), Heroic Inspiration (5), Advantage/Difficult Terrain casing (18) |
| `06_Aftermath.md` | Negligible | Rewards point at Table I–4/XP; no 2024 terms found |
| `07_Cast_of_the_Ball.md` | Negligible | Hit Points casing (2). Names a 2024-free DC system |
| `08_Handouts.md` | A few lines | Handout 3 crystal charges (Magic action 438, *House Flare* Emanation row ~457), Heroic Inspiration on DM sheet (126), budget tracker Table VIII–5 references |
| `09_The_Snakes.md` | Pervasive (budget) | Attribution (8-11); *Running the Snakes* rules (93-152); **Table IX–1** (155-163); 59 Low/Moderate/High lines — every card's *Budget:* label and "plays X" line; 17 Heroic Inspiration award lines; Bloodied morale triggers (10); Utilize (815, 823); Prone/Grappled forms |
| `10_Bestiary.md` | Pervasive (format) | Attribution (7-10); per-character budget (16-19); glossary box (57-87); Table X–2 "(SRD 5.2.1)"; all 29 blocks in 5.2.1 layout (Initiative score, Save row, Gear, Immunities, Attack Roll phrasing, save lists, CR/PB line, ***Bloodied.*** traits, Emanations); items table (Magic action, Emanation) |
| `11_Pregenerated_Characters.md` | Pervasive | Built entirely on 2024 character creation (species traits, background ASIs, origin feats, 2024 class features, Weapon Mastery, 2024 spell texts). Attribution (9-12). See §4 |
| `INVENTIONS_5e.md` | References only | Ledger rows cite "SRD 5.2.1" wording (e.g. row 65 Fast Hands/Arcane Recovery, row 69 budgets, row 71). Style sheet says never sweep it; a conversion adds rows, does not edit old ones |
| `facts.yaml` | Two strings | Only `Heroic Inspiration` inside two `rule_copy` element regexes (facts.yaml:342, 385). No budgets, SRD version or class data |

---

## 3. Stat blocks (`10_Bestiary.md`)

All 29 blocks plus Master Vell use the 5.2.1 layout (items 1–7 of §1 apply to every one). "Custom" = original creature written in SRD format (README:131-133 says the same). Feature columns: **Bl** Bloodied trigger/trait, **Em** Emanation, **SL** 5.2.1 save-list format, **Im** single Immunities line, **Cond** "has the X condition".

| Line | Block | CR (XP) | Built from | 2024-only features beyond the common layout |
|---|---|---|---|---|
| 222 | The Attendant | 8 (3,900; PB +3) | Custom construct | Bl (Rusty/Put Aside gate), Em (Put Aside 20-ft), SL, Im (incl. Exhaustion), Recharge; two turns per round |
| 361 | Boranis Cousin's Blade | 1/2 (100) | Custom | Cond (Grappled, escape DC 12), Gear |
| 411 | Boranis Cousin of 3160 | 1 (200) | Custom | Cond (Grappled), Gear |
| 462 | Boranis Honor Guard | 2 (450) | Custom | Bl (*Call the House* trigger 514), Em (*Flare* 508), SL (500), Cond (Grappled, Invisible), Gear, Reaction |
| 535 | Bought Blade | 1/2 (100) | Custom | Cond (Grappled at 1 HP, 560), Gear |
| 582 | Bought Captain | 4 (1,100) | Custom | Bl (*Talks While It Fights* 617), Gear, Reaction |
| 654 | Bought Sergeant | 2 (450) | Custom | Bl (Breaks 700), Gear, Bonus Action, Reaction |
| 709 | Church Warden | 1 (200) | Custom | SL, Gear, Reaction |
| 768 | Circle Hired Knife | 1 (200) | Custom | Bl (Breaks/Nastier 812-815), Gear, Bonus Action |
| 821 | Damaris Kovaun | 1/2 (100) | Custom | SL, Recharge, Bonus Action |
| 876 | Draunel Duelist | 1 (200) | Custom | SL, Gear, Reaction |
| 933 | Essar Draunel | 3 (700) | Custom | Gear, Reaction |
| 989 | Essin Boranis | 2 (450) | Custom | Gear, Bonus Action, Reaction |
| 1050 | Feuding Kinsman | 1/8 (25) | Custom (commoner-scale) | Cond (Prone, 1084) |
| 1107 | Gallery Knife | 1/4 (50) | Custom | Gear, Bonus Action |
| 1155 | The Hollow | 9 (5,000; PB +4) | Custom (Uninvited) | ***Bloodied.*** trait (1224), SL, Im + Resistances, Cond (Prone), Exhaustion immunity |
| 1268 | Maiven Nolonaire | 3 (700) | Custom | Gear |
| 1329 | Pellin Corro | 1/8 (25) | Custom | Bonus Action |
| 1377 | Phern Bodyguard | 1 (200) | Custom | SL, Cond, Gear, Reaction |
| 1436 | The Radiant | 10 (5,900; PB +4) | Custom (Uninvited) | ***Bloodied.*** re-stage (1512), SL, Im + Resistances, Cond, Recharge, Exhaustion |
| 1574 | Rhaza Callun | 1/4 (50) | Custom | Reaction only |
| 1627 | Sect Guard | 1/8 (25) | **Adapts SRD Guard** (1666 "Built on the SRD guard") — numbers match SRD 5.1 guard (AC 16 chain shirt+shield, HP 11 (2d8+2)); attack swapped spear→cudgel | Gear; otherwise layout only |
| 1670 | Tavva | 2 (450) | Custom | ***Bloodied.*** (1707, releases a charge), SL, Cond, Gear, Bonus Action, Reaction |
| 1749 | Thenya Border Slinger | 1/2 (100) | Custom | Cond, Gear |
| 1795 | Veteran Bought Sergeant | 4 (1,100) | Custom | Bl (Breaks 1842), Gear, Bonus Action, Reaction |
| 1854 | Veteran Draunel Duelist | 2 (450) | Custom | Bl (1906), SL, Gear, Reaction |
| 1911 | Vorlain Boranis | 3 (700) | Custom | Gear, Reaction |
| 1972 | The Wept | 11 (7,200; PB +4) | Custom (Uninvited); mentions SRD in text | ***Bloodied: The Sorrow Slips.*** (2024), Im + Resistances, Cond, Exhaustion, Bonus Action |
| 2143 | Master Vell | — (XP 0; PB +4) | Custom, non-XP | Im + Resistances, Reaction; "CR —" has no 2014 analogue (use "Challenge —" or omit) |
| ~2137 | (a guest) | — | **SRD commoner** without its attack | Commoner exists in SRD 5.1 (CR 0, 10 XP) |

No block uses Weapon Mastery, 2024 exhaustion levels, or Legendary Actions. The Bloodied triggers are the main *mechanical* rewrite (ten blocks); everything else is layout.

Note: the 2014 SRD has no PB in stat blocks, and CR math is the same table, so all CR/XP values stay valid. The blocks were tuned against the 2024 budget, not 2024 monster math, so a 2014 table keeps the numbers.

---

## 4. Pregens (`11_Pregenerated_Characters.md`)

Common to all five (11:3-7, 11:32-41): "built by the SRD 5.2.1 rules"; Human with **Resourceful** (start with/regain Heroic Inspiration), **Skillful** (extra skill), **Versatile** (origin feat); custom backgrounds with **+2/+1 ASIs, an origin feat, two skills, one tool** (2024 background shape); standard array + 4th-level ASI reaching 18–19 (11:46-47 already says a 2014 standard-array human can't); one common magic item "the SRD gives a character who starts above 1st level" (2024 DMG/SRD 5.2.1 starting-equipment rule); every sheet carries Heroic Inspiration; Title-Case equipment. The 2014 fallback text (11:46-48) uses the variant human — **PHB-only** (§6).

| Pregen | 2024-only features on the sheet |
|---|---|
| **Serane Vaskarin**, Bard (College of Lore) 4 (11:52-127) | Background Minor Scion with ASI (+2 Cha +1 Wis) and origin feat **Alert** (2024 origin version: Initiative swap); Orthaen Gift via Versatile; Skillful skill; **Expertise at 2nd** (2014: 3rd — at 4th she still has it, but the source is different); **Jack of All Trades** listed against Initiative-less skills (2024 JoAT also applies to Initiative; 2014 to any check incl. Initiative — +4 Initiative includes Alert, check); **Bardic Inspiration** "fails a D20 Test … within the next hour" (11:96-100; 2014: 10 minutes, roll before DM says success, ability check/attack/save); **Cutting Words** 2024 trigger "succeeds on an ability check or attack roll" (2014: when it makes the roll, before result known); **Lore Bonus Proficiencies** fixed Investigation/Perception/Religion (2014: any three skills — fine as a choice); *Prepared* list of 7 (2014 bards **know** 7 spells at 4th — same count, different mechanic); **Vicious Mockery 1d6** (2014: 1d4 until 5th); Studded Leather "Armor" casing |
| **Pello**, Rogue (Thief) 4 (11:130-192) | Background Factor's Nephew with ASI (+2 Dex +1 Wis) and origin feat **Skilled** (not SRD 5.1); Phern Gift (The Prickle); Dex 19 (2024 ASI math); **Weapon Mastery** (Nick on daggers, Vex on shortsword; 11:168-170, 178) — Nick makes the off-hand attack free of a Bonus Action, so Cunning Action + two attacks is a 2024-only turn; **Steady Aim** (Tasha's in 2014, **not SRD 5.1**; 2024 core); **Fast Hands** using Utilize and Magic action to use a magic item (11:183-185; 2014 Fast Hands: Sleight of Hand, thieves' tools, Use an Object — "use a magic item" via Use an Object is a DM call; 2014 Thief gets Use Magic Device only at 13th); Second-Story Work as Climb Speed (2014: climbing costs no extra movement; no Climb Speed; jump distance increase by Dex mod rather than "jumps use Dexterity"); Thieves' Cant + extra language (2024 wording) |
| **Andra Tessarin**, Wizard (Evoker) 4 (11:196-262) | Background Lattice-Scholar (+2 Int +1 Con), origin feat **Skilled**; Orthaen Gift; **Ritual Adept** (2024 name; 2014 Ritual Casting — same effect); **Scholar** (Expertise in History, 2024 wizard 2nd-level feature; **does not exist in 2014** — History +8 must drop to +6); **Evocation Savant** 2024 version (two free spells added; 2014 halves copy cost/time); **Potent Cantrip** at 3rd (2024 Evoker 3rd; **2014 Evoker gets it at 6th**) — Fire Bolt "half on a miss" must go (note 2014 Potent Cantrip only applied to saves anyway); *Prepared* 5+2 = 7? (sheet lists 7; 2014 wizard prepares Int mod + level = 4+4 = 8); 4 cantrips + gift (2014 wizard: 4 cantrips at 4th — same); *Mage Armor* before ball, Arcane Recovery (same); "crystal (Arcane Focus)" Title Case |
| **Dassa**, Fighter (Champion) 4 (11:266-357) | Background City Watch Veteran (+2 Str +1 Con), origin feat **Savage Attacker** (not SRD 5.1); **Alert** via Versatile — she is ungifted (11:316-318); **Second Wind 3 uses** (2014: 1 per short rest); **Tactical Mind** (2024-only); **Weapon Mastery** ×4 (Sap, Nick, Graze, Vex; 11:326-327, 338-340); **Remarkable Athlete** 2024 version (Advantage on Initiative and Athletics, move after crit; **2014: half-proficiency to uncoded Str/Dex/Con checks and longer running jump, at 7th level — not available at 4th**); Improved Critical (same); Fighting Style Defense (same); Action Surge (same); Initiative "+3, with Advantage" (Alert + Remarkable Athlete) |
| **Ilesse Kethaun**, Cleric (Life Domain) 4 (11:361-441) | Background Border Courtier (+2 Wis +1 Cha), origin feat **Alert**; Orthaen Gift (*Resistance*); **Divine Order: Thaumaturge** (2024-only: extra cantrip, Wis to Arcana/Religion — her Arcana/Religion +4 depends on it; 11:407-409); **Channel Divinity 2 uses, one back on Short Rest** (2014: 1 use per short rest at 2nd–5th); **Divine Spark** (2024-only Channel Divinity option); **Preserve Life** (both editions; 2024 "Bloodied" phrasing); **Turn Undead** 2024 wording (Frightened + Incapacitated; 2014: turned, must spend turns moving away); **Life Domain** 2024: bonus proficiency Heavy armor removed — 2014 Life cleric gets heavy armor proficiency (sheet wears Chain Shirt by choice, fine); always-prepared domain spells 2024 list (*Bless*, *Cure Wounds*, *Aid*, *Lesser Restoration*; 2014 Life: *bless*, *cure wounds*, *lesser restoration*, *spiritual weapon*) — so 2014 Spiritual Weapon becomes a domain spell and *Aid* would need a slot; prepared count 7 (2014: Wis 4 + level 4 = 8, plus domain); **5 cantrips + gift** (2014 cleric: 4 at 4th; Thaumaturge is the 5th); **Spiritual Weapon "Concentration"** (2024 change; 2014 not concentration); *Guiding Bolt* 4d6 same; Disciple of Life same |

Rebuild arithmetic: an SRD 5.1 human (+1 to all six) on the standard array reaches 15 → 16, then 18 with the 4th-level ASI. So 18 in the main stat works (Serane Cha 18, Dassa Str 18, Ilesse Wis 18). The 19s do not (Pello Dex 19, Andra Int 19). Every other score also moves by +1, which changes the derived numbers on all five sheets (HP, AC, saves, skills, spell DC, Initiative).

Pregen spell/feature text that build_print.py also copies (§5) needs the same changes: *Vicious Mockery* 1d6 → 1d4; *Healing Word* 2d4 → 1d4 + mod; *Cure Wounds* 2d8 → 1d8 + mod; *Spiritual Weapon* loses Concentration; *Sleep* → 5d8 HP pool; *Guidance*/*Resistance* → 2014 text (d4 to one check/save, no named skill or damage type); *Command* option list; *Calm Emotions* "Indifferent" wording; *Mage Hand*/*Silent Image* "Magic action" → action.

---

## 5. Tooling impact (`tools/`)

Test counts are `def test` counts per file. The current suite is green against the 2024 text. "Breaks" means it would fail as soon as the text is converted.

| File | 2024 assumptions hard-coded | Breaks when text changes |
|---|---|---|
| `lint_5e.py` (1,166 lines) | **`lowercase_terms`** family (≈l.300-313) makes 2014 lower-case style a *hard* error: advantage, hit points, short/long rest, difficult terrain, dim/bright light, bloodied, heroic inspiration, opportunity attacks, "X condition", "knocked prone", "is stable", "<action> action" over `ACTIONS` = attack…**influence, magic, search, study, utilize** (l.~78), "its speed". **`deadly_budget`** (l.336, line filter `_BUDGET_LINE` l.380 = XP/budget/Low/Moderate/High/multiplier) forbids "Deadly" in budget lines. **`save_damage` S9** forbids "on a failed saving throw" (the 2014 stat-block phrasing) and **S10** forbids "half as much on". `_DC_SAVE_FORM` accepts "Saving Throw:*" (5.2.1 list form). `_RULES_TERMS` (l.385) treats italic Title-Case rules terms as emphasis. `conversion_talk` forbids "this edition"/"the original". Baseline `lint_baseline.json` has **hard = {}** (zero tolerance), so every 2014-style lowercase term fails `--check` at once | Every 2014-style sentence. `test_lint_5e.py` (214 tests): `TestLowercaseTerms` (l.93), `TestSaveDamage` (l.178), `TestBareDC` (l.149 uses the "*Strength Saving Throw:*" form), `TestDeadlyBudget` (l.246), `TestEmphasisItalics` (l.694 Heroic Inspiration), `TestConversionTalk` (l.203 Heroic Inspiration example), CLI/baseline tests. Soft metrics (sentence length, words) shift too, so `--baseline` must be rewritten |
| `lint_5e_allow.txt` (53 lines) | 4 entries tied to 5.2.1: the "Grappled condition (escape DC" SRD 5.2.1 grapple form; the 2014 box's "past Deadly" exemption; the **near_duplicate** exemption keyed on the exact text "This work includes material from the System Reference Document 5.2.1"; Serane's "take 1d6 Psychic damage" Vicious Mockery wording | Changing the attribution text, the box, or Vicious Mockery orphans these, and the attribution near-duplicate exemption stops matching (4 identical SRD 5.1 notices would then fail `near_duplicate`) |
| `terms.txt` (50 lines) | No edition terms (setting glossary only) | Nothing |
| `bestiary_check.py` (415 lines) | Docstring says CR estimate uses **DMG 2014** ch. 9 table (`T`, l.24) — this part is edition-neutral and survives. Hard-coded 5.2.1: `XP` dict and `pb()` (same numbers in 2014); `_CR_LINE` regex `**CR** n (XP n; PB +n)` (l.201); `**AC** (\d+)` and an error if the AC line has a parenthetical (l.304, "armor goes on a Gear line" — the exact opposite of 2014 format); `parse_gear` `**Gear**` line (l.281); `ARMOR` table keyed on Title-Case 5.2.1 names ("Studded Leather Armor", "Half Plate Armor", "Splint Armor"); `_INIT` `**Initiative** +n (nn)` with an error on the 2014 "with Advantage" suffix and a required score (l.276-322); Save row check (l.368); `**HP** n (nd8` regex; `INIT_ADVANTAGE` set | Converting any block to 2014 layout fails every block. `test_bestiary_check.py` (43 tests): CR-line fixtures (l.16, 66, 73, 102), T4.4 Gear/Initiative tests (l.108-143) |
| `pregen_check.py` (162 lines) | Docstring "SRD 5.2.1 (2024 rules) legality check". `CANTRIPS={'bard':3,'wizard':4,'cleric':4}`, `PREP={'bard':7,'wizard':7,'cleric':7}` (2024 tables; 2014: bard 7 **known**, wizard 8 = Int+level, cleric 8 = Wis+level + domain); legality model = standard array + **background +2/+1** (`bg`, `bg_opts`, `ok_bg` requires values [1,2]) + ASI; `skillsrc` includes `skillful=1` (Resourceful/Skillful human) and `feat` (Skilled = 3); `alert` adds **PB** to Initiative (2014 Alert is +5); `thaumaturge` adds Wis to Arcana/Religion (Divine Order); `joat` half-PB to non-proficient skills; Andra spellbook `6 + 2/level + Evocation Savant 2` (2014 Savant adds no spells); `defense` +1 AC; `FOCUS` requires Title-Case "Arcane Focus"/"Holy Symbol" (O16) | Any 2014 rebuild fails ability, skill, cantrip, prepared, spellbook, Initiative checks. `test_pregen_check.py` (13 tests) — mostly the focus rules; l.81-87 asserts lowercase "arcane focus" is **reported** (2014 style fails); `test_main_exits_zero_on_the_module` |
| `fact_check.py` (406 lines) + `facts.yaml` + `fact_baseline.json` | Edition-neutral engine. facts.yaml has two `Heroic Inspiration` regexes in `rule_copy` elements (342, 385) | Renaming Heroic Inspiration → Inspiration silently weakens those two rule_copy elements (no failure, lost coverage). `test_fact_check.py` (127), `test_wp6/7/8.py` (16/48/10) run facts against real chapters; test_wp7 l.52 and l.248 use card budget strings ("1,100 XP — plays Moderate", "400 XP") |
| `copyright_scan.py` (220 lines) + `copyright_allow.txt` | No version string; allowed corpus = whatever `--srd DIR` holds ("the CC BY 4.0 SRDs"); refs = `--refs DIR`. The 16 allowlist entries are SHA-1s of runs judged SRD boilerplate (Legendary Resistance, Regeneration, teleport grammar) | For a 2014 pass, the **SRD 5.1** extract must be in `--srd`, and the **2014 PHB/DMG/XGE/TCE/MM** extracts must be in `--refs`, or 2014 PHB wording will go unflagged. Changed sentences produce new hashes, so old entries go stale (harmless). `test_copyright_scan.py` (13) is synthetic, not edition-bound |
| `build_print.py` (776 lines) | `SPELLS` dict (l.504-546): 40 one-line spell summaries "from the SRD 5.2.1 text" — 2024 values for Cure Wounds 2d8, Healing Word 2d4, Vicious Mockery 1d6, Sleep (Wisdom save), Spiritual Weapon (Concentration), Guidance/Resistance (named skill/damage type), Command list, Calm Emotions "Indifferent", Mage Hand/Silent Image "Magic action", Spare the Dying 15 ft. `ON_YOUR_TURN` (l.549-555): Pello "Nick attack comes free", Dassa "Sap". `trackers()` (l.477-501): always adds "**Heroic Inspiration** ☐"; regex `**Hit Dice** (\d+)(d\d+)`; `(\d+) uses?` for Second Wind 3 / Channel Divinity 2 / Bardic Inspiration 4. `SRD_NOTE` (l.687-689): SRD 5.2.1 attribution on every pregen sheet | Stale-but-passing: spell lines and turn lines would print 2024 rules next to 2014 sheets. `test_build_print.py` (73): l.239 and l.367 assert **"Resourceful"** and "Heroic Inspiration" appear on each built sheet; l.247-260 tracker tests; spell_lines raises KeyError for a spell not in `SPELLS` (any 2014-only spell added to a sheet breaks the build) |
| `test_maps.py` (40) | None | Nothing |
| `test_wp9.py` (19) | Runtime/prep box/cast cues | Nothing edition-specific found |

`software/tests/test_docs_consistency.py`: **no reference** to this module. `software/tests/test_no_private_canon.py`: no explicit reference, but it scans **every git-tracked text file** (`git ls-files`, l.43-60), so any new or converted module text is scanned for private-canon words automatically. (Other software tests touch `adventures/oraga_night/`, the Facets edition, not this folder.)

---

## 6. Copyright / licence notes

**What changes in the notice.** The four attribution blocks (README:117-120, 09:8-11, 10:7-10, 11:9-12), the `SRD_NOTE` in build_print.py, every "SRD 5.2.1" version mention (§1 row 34), and README *Changes from the SRD* become SRD 5.1. Both SRDs are CC BY 4.0; the 5.1 notice wording and URL differ (see §1 row 34). Note README:131 "the four SRD backgrounds" and 03:18-19 "The four SRD backgrounds work as written": **SRD 5.1 has one background (Acolyte)**.

**What SRD 5.1 contains, for the pieces this module uses.**
- Races: **human, standard only** (+1 to every score, two languages). No variant human, no feat at 1st.
- Classes: all five pregen classes, with **one subclass each**, and the module's picks are exactly those: College of Lore, Thief, School of Evocation, Champion, Life Domain. Good: no subclass swap needed.
- Backgrounds: **Acolyte** only.
- Feats: **Grappler** only.
- Spells: every spell the module names was checked against the 2014 names. The forms used (*Hideous Laughter*, *Tiny Hut*) are the SRD 5.1 names, not *Tasha's…*/*Leomund's…*. Keep it that way.
- Monsters: guard and commoner (used by the Sect Guard and the guest) are in SRD 5.1.
- Magic items: Potion of Healing is in SRD 5.1.
- **Not in SRD 5.1**: the DMG encounter-building chapter's XP threshold table and multiplier table (the 5.1 SRD has no encounter-building section, only the CR→XP table in the monster chapter); Xanathar's encounter tables and solo/group guidance; Tasha's options (Steady Aim, optional class features, custom lineage).

**Where a 2014 conversion would tempt someone to copy closed text.**
1. **Variant human for the gifts.** README:134, 03:51 and 11:48 already say "the variant human's feat". Variant human is PHB-only. Naming it as a rules reference is fine (the owner's table has the PHB), but printing its rules text (+1 to two scores, one skill, one feat) is not. The safe route: present the gift as the module's own rule ("a gifted human also gains its tribe's gift at 1st level"), built on the SRD 5.1 standard human, so the module never depends on PHB text.
2. **2014 feats on the pregens.** Alert (2014: +5 Initiative, can't be surprised, no hidden-attacker Advantage), Savage Attacker (2014: reroll melee damage once per turn), Skilled (three proficiencies), Magic Initiate (03:58) are **PHB feats, not SRD 5.1**. A 2014 sheet should not print their text. Options: drop them (the SRD 5.1 human has no feat anyway), name them only ("Alert (PHB)") for the owner's table with no rules text, or use Grappler.
3. **Custom backgrounds.** The module's Minor Scion, Factor's Nephew, Lattice-Scholar, City Watch Veteran and Border Courtier are its own. Rebuilt in 2014 shape (two skills, two tools/languages, a feature, equipment), they stay original. Do not borrow PHB background features (e.g. Noble's Position of Privilege, Guild Artisan's membership) as wording.
4. **Encounter difficulty.** Reprinting the DMG's 2014 threshold table (Easy/Medium/Hard/Deadly per level) and multiplier table would reproduce DMG content outside the SRD. Labels ("Hard", "Deadly") and the bare idea are fine; the existing 2014 box (10:82-87) states the result without the table. A full 2014 Table IX–1 would be the risky line.
5. **Class-feature text.** README:132-133 says pregen class-feature text is "adapted from the SRD". For 2014, adapt from SRD 5.1 text only (SRD 5.1 has all the 2014 core features the five classes need through 4th level). Steady Aim (Tasha's) is not in SRD 5.1 and should be dropped, not paraphrased.
6. **Monster stat-block conventions.** 2014 layout ("Melee Weapon Attack: … to hit, reach … one target") is SRD 5.1 boilerplate and safe. Monster Manual 2014 flavour or named monsters beyond the SRD are not.
7. **Xanathar's at the owner's table.** Nothing in the module uses XGE now. A 2014 pass should not add XGE content (encounter tables, tool proficiency rules, Spell list additions, Shadow Blade etc.).

`copyright_scan.py` needs the 2014 closed books in `--refs` and the SRD 5.1 extract in `--srd` before the 2014 text is trusted (§5).

---

## Biggest risks

1. **The "only the pregens need rebuilding" claim (01:134-136, README:16-18) understates the job.** The chapter text is mostly swappable by glossary, but chapter III's character-build rules (origin feat via *Versatile*, background ASIs, four SRD backgrounds) and the gift delivery need a real 2014 rule, and the pregens are a full rebuild (2024 class features at 4th: Weapon Mastery, Tactical Mind, 3× Second Wind, Divine Order, Divine Spark, 2 Channel Divinity, Scholar, Potent Cantrip at 3rd, Remarkable Athlete at 3rd, Steady Aim). Andra and Pello also lose their 19s.
2. **Encounter balance.** Every card's label is 2024 arithmetic. Under 2014 math with the multiplier, most cards jump one or two bands (the box's own examples: S3 850 → 1,700 XP, past Deadly; S14 > 2× Deadly). The rosters were tuned by play, not by label, so keep rosters and relabel. But the pregens also get weaker in 2014 (no mastery, fewer Second Winds, no Potent Cantrip), so the fights get harder in fact, not just on paper. Needs a re-check of the "plays X" lines.
3. **Tooling is locked to 2024 and will fail loudly.** `lint_5e.py` (zero-tolerance hard baseline enforcing 5.2.1 casing, banning "Deadly" and "on a failed saving throw"), `bestiary_check.py` (5.2.1 layout parser), `pregen_check.py` (2024 creation and prep tables) and `build_print.py` (2024 spell lines, Resourceful/Heroic Inspiration asserts) all need a 2014 mode or a fork. Decide that before editing text, or the suite cannot guard the conversion.
4. **Licence creep.** The easy 2014 fixes (variant human, 2014 Alert/Savage Attacker/Skilled text, DMG threshold table, Steady Aim) are all non-SRD. The variant-human pointer is already printed three times.
5. **Stealth 2024 rules that read fine but play differently**: Bloodied triggers on ten blocks (fine), but also PC grapple via Unarmed Strike (05:453), Fast Hands using a magic item (11:183-185), Bardic Inspiration's 1-hour/D20 Test window, Spiritual Weapon concentration, Healing Word/Cure Wounds dice, *Sleep* (the 2014 HP-pool version is far stronger against the CR ≤ 1 retinues at 4th level, which could trivialise several snake cards).
6. **Style choice is a scope decision.** Converting rules-term casing, italic spell casing and equipment casing to 2014 house style touches nearly every line of chapters IV, V, IX, X and XI. It is cosmetic, but the linter enforces the current form. The owner should rule whether a 2014 edition keeps the SRD 5.2.1 casing (cheapest, still readable) or adopts 2014 lower case.
