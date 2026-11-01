# DESIGN: Oraga Night 5e, full 2014 conversion, four-player baseline

Inputs: `BRIEF_oraga_5e_2014.md`, `RESEARCH_oraga_5e_2014_inventory.md`, `RESEARCH_oraga_5e_2014_encounters.md`.
Module root: `conversions/dnd5e/oraga_night/` (M/). The Facets edition is untouched.

## 1. What changes

| Layer | 2024 today | 2014 target |
|---|---|---|
| Licence | SRD 5.2.1 notice (README:117, 09:8, 10:7, 11:9, `build_print.SRD_NOTE`) | SRD 5.1 notice, verbatim from its legal page |
| Stat blocks (29) | 5.2.1 layout: Initiative score, Save row, Gear, single Immunities line, "Melee Attack Roll:", save-as-list, "CR n (XP; PB)" | 2014 layout: Saving Throws line, Damage/Condition Immunities lines, "*Melee Weapon Attack:* +n to hit", "must succeed on a DC n Strength saving throw", "Challenge n (XP)" |
| Terms | Heroic Inspiration, Bloodied, Magic/Utilize/Study/Influence actions, Emanation, D20 Test, "has the X condition" | Inspiration; "at or below half its hit points"; Cast a Spell/Use an Object/action + check; sphere/aura; "ability check, attack roll or saving throw"; "is prone/charmed" |
| Character rules (ch III) | Species + background ASIs + origin feat via *Versatile*; four SRD backgrounds | SRD 5.1 human (+1 to every score); background by "Customizing a Background"; gift as a **bonus feat at 1st level** (ch III's existing 2014 rule); ungifted take no feat |
| Pregens (5) | 2024 builds (mastery, origin feats, 2024 class tables) | Rebuilt by SRD 5.1. Subclasses are already the SRD 5.1 ones (Lore, Thief, Evocation, Champion, Life) |
| Encounters | 3 PCs baseline, SRD 5.2.1 budget (Low/Moderate/High), Table IX–1 | **4 PCs baseline**, 2014 DMG adjusted XP printed per card; Xanathar's ratios used only in design |
| Notes | "At a 2014 table" notes | Reversed into short "At a 2024 table" notes (pending ruling R3) |
| Tools/tests | 2024-hardwired (lint casing and banned words, bestiary parser, pregen tables, print spell lines) | Converted in place to 2014; the 2024 state is pinned by a local tag |

## 2. Encounter method

1. **Baseline party:** four 4th-level characters. 2014 DMG thresholds for four: Easy 500, Medium 1,000, Hard 1,500, Deadly 2,000 (adjusted XP, multiplier for a party of 3–5).
2. **Design check (internal only, never printed):** Xanathar's multiple-monster ratios at 4th level (CR ½ = ½ character, CR 1 = 1, CR 2 = 2, CR 3 = 4, CR 4 = 6). Four "character-equivalents" is a fair fight; about 2.7 is easy; 6 is the deadly ceiling.
3. **Target band per card:** keep each card's intended *play*, mapped as follows (ruling R2):
   - SRD 5.2.1 "under Low" / "Low" → 2014 **Easy–Medium**
   - "Low–Moderate" / "Moderate" → **Medium–Hard**
   - S14 (the Attendant, the night's climax) → **Deadly**, at about 1–1.25 × Deadly, down from 1.95 ×
4. **Levers, in order of preference:** cut a retinue body; move a body to a clock or reinforcement beat; break earlier (morale); lower a block's CR or HP only as a last resort, because the blocks are shared across cards.
5. **What a card prints:** the roster, then "*N XP; adjusted N for four: Band.*" and the play line. Adjusting lines, in order: One character · Three characters · Five characters · Four at 3rd level · Four at 5th level · Nastier. Every line carries a total, which fixes the research file's missing totals for S1, S4, S7 and S9. **No reproduction of the DMG threshold or multiplier tables.** Chapter IX's "Running the Snakes" names the method and gives the party's four thresholds in one sentence.
6. **Overshoots to fix first** (adjusted XP on today's four-character line): S3 with captain 5,200; S4 with the four 5,400; S14 3,900; S13 2,700; S9 2,300; S10 2,000.
7. **Party-size numbers outside the cards** (38, listed in the encounter research §4) move to the four-character values: potions 4, the Wept on her 3rd turn, lump 30, and so on. The three-character values move into the adjusting lines.

## 3. Copyright guardrails

- The book uses SRD 5.1 content only. It may *name* non-SRD books ("the variant human in the *Player's Handbook*") but never reproduce their text or tables.
- Remove or neutralise current pointers to non-SRD options: variant human (README:134, 03:51, 11:48), Magic Initiate (03:58), Alert, Skilled, Savage Attacker and Steady Aim on pregens.
- Re-run `copyright_scan.py` with the 2014 books as `--refs` and SRD 5.1 as `--srd` before each commit.

## 4. Tooling (TDD: tests first, red, then green)

- `lint_5e.py`: replace the 5.2.1 casing rules and banned words ("Deadly", "on a failed saving throw" become legal); add a ban on 2024 terms (Heroic Inspiration, Bloodied, Emanation, D20 Test, Magic action, Utilize action).
- `bestiary_check.py`: parse the 2014 block layout; check CR→XP by the 2014 table; check that save and skill bonuses follow from scores and PB.
- `pregen_check.py`: 2014 class tables (bard spells known, cleric/wizard prepared = mod + level, cantrips), standard human +1, no origin feats, gift bonus feat, 2014 Jack of All Trades scope (Initiative included).
- `build_print.py`: SRD 5.1 notice, 2014 spell lines; its tests drop "Resourceful".
- `fact_check.py` and `facts.yaml`: add guards for the new baseline (potions 4, Wept turn 3, lump 30) and the licence string.

## 5. Risks

- **Test churn:** 668 module tests. Convert the tools before the text so failures point at real regressions.
- **Pregen power drop:** 2014 humans can't reach the 19s, and spells are weaker. Re-run the "plays X" lines after the pregens are rebuilt, not before.
- **Shared blocks:** changing a block's numbers moves every card that uses it. Prefer roster changes.
- **Size:** about eight packages. Commit each on the owner's word; no push.

## 6. Open rulings (asked as questions)

- **R1 Styling:** keep the SRD 5.2.1 Title Case for spells, conditions and equipment (cheap), or switch to 2014 lower case (touches nearly every line of IV, V and IX–XI).
- **R2 Difficulty mapping** in §2.3.
- **R3 Keep a short "At a 2024 table" note set**, reversing today's 2014 notes, or drop 2024 support entirely.
- **R4 The gift rule:** confirm "bonus feat at 1st level" for all gifted characters, and decide whether the owner-table sheets (Taven, the Knight) stay variant humans as a house choice.

**Resolved by the owner, 2026-11-01:**
- **R1:** keep the current Title Case styling. Only the rules change.
- **R2:** use the mapping in §2.3 as written.
- **R3:** keep short "At a 2024 table" notes: one box in chapter X, plus a line or two in chapters III and XI.
- **R4:** the book grants the gift as a bonus feat at 1st level. At the owner's table, Taven (a gifted variant human) gets the gift *and* a variant-human feat, which is the player's pick. The Knight is unchanged.

Defaults taken without asking (reversible): work on a new local branch `feat/oraga-5e-2014`; pin today's state with a local tag `oraga-5e-2024` (never pushed); convert tools in place rather than forking.

## 7. P2 card plan (four 4th-level characters; Easy 500 · Medium 1,000 · Hard 1,500 · Deadly 2,000)

Each entry gives the new printed roster, its XP, the adjusted total and the band; then the target band from R2; then the adjusting lines (adjusted totals use each party's thresholds, and the next-higher multiplier for a lone character). A creature far weaker than the rest (Pellin Corro) is left out of the multiplier, as the DMG allows.

- **S1 Seating Feud**: 8 kinsmen + the principal. 225 XP; 9 foes ×2.5 = 562, Easy. Target: Easy. Lines:
  - One character: none.
  - Three characters: 6 kinsmen + the principal, 175 / 437, Easy.
  - Five characters: 10 kinsmen + the principal, 275 / 825, Easy.
  - Four at 3rd level: 6 kinsmen, 150 / 300, Easy.
  - Four at 5th level: 10 kinsmen + the principal, 275 / 825, under Easy.
  - Nastier: a second principal, 250 / 625.
- **S6 Quiet Word**: 3 Cousins of 3160. 600 / 1,200, Medium. Target: Easy–Medium. Lines:
  - Three characters: 2 cousins, 400 / 600, Easy.
  - Five characters: 3 cousins, 600 / 1,200, Easy.
  - Four at 3rd level: 3 Cousin's Blades, 300 / 600, Medium.
  - Four at 5th level: 3 cousins with Essin watching, 600 / 1,200, Easy.
  - Nastier: they break only on a crowd.
- **S2 Service Corridor**: Tavva + 3 knives. 600 / 1,200, Medium. Target: Easy–Medium. Lines:
  - One character: Tavva + 1 knife a round behind, 500 / 1,000, Deadly for one.
  - Three characters: Tavva + 2 knives, 550 / 1,100, Medium.
  - Five characters: Tavva (Nastier) + 4 knives + a Circle Hired Knife, 850 / 1,700, Medium.
  - Four at 3rd level: Tavva + 1 knife, 500 / 750, Medium.
  - Four at 5th level: as five, 850 / 1,700, Easy.
- **S4 East Wing Doors**: 2 Honor Guards. 900 / 1,350, Medium. With the four reinforcements, 2,700 / 5,400. That is beyond Deadly on purpose: the house does not lose its doors, guards detain and nobody dies, so the card's outs are the play. Target: Medium–Hard. Lines:
  - One character: 1 guard, 450 / 675, Deadly for one.
  - Three characters: 2 guards, 900 / 1,350, Hard.
  - Five characters: 2 guards, with Call the House a round sooner, 900 / 1,350, Medium.
  - Four at 3rd level: 2 guards, 900 / 1,350, Hard.
  - Four at 5th level: 4 guards, 1,800 / 3,600, Hard.
- **S7 Second Plate**: the 3 knives in the read-aloud. 600 / 1,200, Medium. This is down from 4 knives (1,600, Hard). Target: Easy–Medium. Lines:
  - One character: 1 knife, 200 / 300, Medium for one.
  - Three characters: 2 knives, 400 / 600, Easy.
  - Five characters: 4 knives, 800 / 1,600, Medium.
  - Four at 3rd level: 2 knives, 400 / 600, Medium.
  - Four at 5th level: 4 knives + S2's crew in the same run, 1,400 / 3,500, Hard.
  - Nastier: the fourth knife, and they break at half down, 800 / 1,600.
- **S8 Study Door**: 2 wardens at the door and a 3rd at segment 2. 600 / 1,200, Medium. This is down from 4 wardens (1,600, Hard). Target: Easy–Medium. Lines:
  - One character: 1 warden, 200 / 300, Medium for one.
  - Three characters: 2 wardens, 400 / 600, Easy.
  - Five characters: 4 wardens (the 4th at segment 3), 800 / 1,600, Medium.
  - Four at 3rd level: 2 wardens, 400 / 600, Medium.
  - Four at 5th level: 4 wardens, the 3rd and 4th already at the door, 800 / 1,600, Easy.
  - Nastier: as printed.
- **S9 Appointment**: 3 Draunel Duelists, 600 / 1,200, Medium; 3 Cousin's Blades, 300; both sides 900 / 1,800, Hard. This is down from 1,150 / 2,300 Deadly. Target: Medium–Hard. Lines:
  - One character: one a side, 300 / 600, Deadly for one, though each side's man is fighting the other.
  - Three characters: 2 a side, 600 / 1,200, Hard.
  - Five characters: a Veteran + 2 duelists + 3 Blades, 1,150 / 2,300, Hard. If Essin is hostile, +450, which makes it Deadly.
  - Four at 3rd level: 2 a side, 600 / 1,200, Hard.
  - Four at 5th level: 2 Veterans + 1 duelist + 3 Cousins of 3160, 1,700 / 3,400, Hard.
  - Nastier: a Veteran + 2 duelists + 3 Cousins of 3160, 1,450 / 2,900.
- **S10 Over the Wall**: Maiven (at segment 2) + 2 slingers. 900 / 1,800, Hard. This is down from 3 slingers (2,000). Target: Medium–Hard. Lines:
  - One character: Maiven alone with 2 attacks, 700 / 1,050, Deadly for one.
  - Three characters: Maiven + 1 slinger, 800 / 1,200, Hard.
  - Five characters: Maiven + 3 slingers, 1,000 / 2,000, Hard.
  - Four at 3rd level: Maiven + 1 slinger, pulling her blows, 800 / 1,200, Hard.
  - Four at 5th level: Maiven (Nastier) + 3 slingers, 1,000 / 2,000, Medium.
- **S11 Phern Door**: 3 bodyguards (+ Corro, uncounted). 600 / 1,200, Medium. Target: Easy–Medium. Lines:
  - Three characters: 2 bodyguards, 400 / 600, Easy.
  - Five characters: 3 bodyguards, crowd DC 15, 600 / 1,200, Easy.
  - Four at 3rd level: 2 bodyguards, 400 / 600, Medium.
  - Four at 5th level: 3 bodyguards, clock starts at 1, 600 / 1,200, Easy.
- **S12 Corval in the Kitchens**: 2 knives, 400 / 600, Easy; at heat 4, 3 knives, 600 / 1,200, Medium. This is down from 3 / 4 knives. Target: Easy–Medium. Lines:
  - Three characters: 2 knives at either heat, 400 / 600, Easy.
  - Five characters: 3 knives, or 4 at heat 4, 1,200 / 1,600, Easy / Medium.
  - Four at 3rd level: 2 knives at either heat, Medium.
  - Four at 5th level: 4 knives, smoke DC 13, 800 / 1,600, Easy.
- **S13 Arrest in the Fire**: Draunel + a Veteran Draunel Duelist. 1,150 / 1,725, Hard. This is down from 1,350 / 2,700 Deadly. The Boranis side, if run instead: Essin + 2 Blades, 650 / 1,300, Medium. Target: Medium–Hard. Lines:
  - One character: Draunel alone, 700 / 1,050, Deadly for one.
  - Three characters: Draunel + 1 duelist, 900 / 1,350, Hard.
  - Five characters: Draunel + 2 duelists, 1,100 / 2,200, Hard.
  - Four at 3rd level: Draunel + 1 duelist, 900 / 1,350, Hard.
  - Four at 5th level: Draunel + 2 Veterans, 1,600 / 3,200, Hard.
- **S3 Gate**: Bought Sergeant + 4 Blades. 850 / 1,700, Hard. This is down from the Veteran + 4 Blades (3,000 Deadly). The captain, if he fights, makes it 1,950 / 3,900: beyond Deadly, and he negotiates when hurt or on his second round. Target: Medium–Hard. Lines:
  - Three characters: Sergeant + 2 Blades, 650 / 1,300, Hard.
  - Five characters: Sergeant + 5 Blades, 950 / 1,900, Hard.
  - Four at 3rd level: Sergeant + 2 Blades, 650 / 1,300, Hard.
  - Four at 5th level: the Veteran Sergeant + 4 Blades, 1,500 / 3,000, Hard.
  - Nastier: the Veteran + 4 Blades, the captain at round 2.
  - The Veteran Bought Sergeant is no longer the four-player default (05, 07, Table X–1).
- **S5 Looters**: Tavva + 3 knives. 600 / 1,200, Medium. Target: Easy–Medium. Lines:
  - Three characters: Tavva + 2 knives, 550 / 1,100, Medium.
  - Five characters: Tavva (Nastier, 4 knives), 650 / 1,300, Medium.
  - Four at 3rd level: Tavva + 1 knife, 500 / 750, Medium.
  - Four at 5th level: the Nastier crew, 650 / 1,300, Easy.
- **S14 Attendant**: the only lever is the block, because there is one foe and no roster. CR 8 → **CR 6** (2,300 XP; ×1 = 2,300, **1.15 × Deadly**). HP 178 → **144 (17d8 + 68)**; everything else is unchanged (AC 17, +7, Put Aside DC 15, PB +3). The DMG CR estimate: defense HP 144 / AC 17 ≈ 6.0, offense DPR 40 / +7 ≈ 6.5, average 6.25. With four characters as the baseline, the full Multiattack on its second Focused turn is the default. Lines:
  - One character: the second turn makes no attack.
  - Three characters: 120 HP, and the second turn is one Joined Hands.
  - Five characters: 170 HP, distraction DC 19.
  - Four at 3rd level: 125 HP, distraction DC 17.
  - Four at 5th level: the five line or Nastier.
  - "Built to hit hard": +30 HP.
  - XP is 2,300 on every line.
- **Chapter V**: four is the baseline (the Wept on her 3rd turn, lump 30). Lines:
  - Three characters: Wept on her 4th turn, lump 20.
  - Five characters: lump 40.
  - Four at 3rd level and four at 5th level: as now.
