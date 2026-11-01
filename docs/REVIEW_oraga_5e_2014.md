# REVIEW: Oraga Night 5e, 2014 conversion (SRD 5.1, four 4th-level characters)

Reviewer pass, 2026-11-01. Scope: `git diff oraga-5e-2024..feat/oraga-5e-2014 -- conversions/dnd5e/oraga_night docs/DECISIONS.md`, read against `docs/DESIGN_oraga_5e_2014.md` (§2, §6, §7), the BRIEF and the LOG. Paths below are relative to `conversions/dnd5e/oraga_night/` unless they say otherwise.

Status: COMPLETE. No module or tool file was edited. `pytest tools` re-run: 680 passed, 1 skipped.

## Verdict

The conversion is in good shape. I checked these and found them correct:
- All five pregens: ability scores from the standard array, the SRD human's +1 to every score and a +2 ASI; HP, AC, saves, every skill value, Jack of All Trades (Initiative included), cantrip and known/prepared counts, the wizard's 12-spell lattice, and the 2014 class and subclass features.
- All 29 stat blocks: AC from the named armor, HP from the hit dice, saves and skills from scores and PB by CR, attack bonuses and damage averages, save DCs, and CR to XP.
- All 41 spell lines in `tools/build_print.py` match SRD 5.1.
- Every "N XP; adjusted M: Band" figure on cards S1–S14 except one (F1).
- Table IX–3 matches the cards.

The problems are one wrong number, one 2024 rule still in the text, a rogue language left over from 2024, a few spots still sized for the old party, the 2024 reaction/section layout left in the otherwise-2014 blocks, and one small story addition.

## Confirmed findings

### F1. S9 five-character line: wrong adjusted total when Essin joins (should-fix)
- **Where:** `09_The_Snakes.md:1537-1538`. The line reads "If Essin comes in hostile, 1,600 XP, adjusted 3,200: Deadly."
- **What is wrong:** with Essin, the roster is a Veteran Duelist, 2 Duelists, 3 Cousin's Blades and Essin. That is 7 foes, and the 2014 multiplier for 7–10 foes is ×2.5, so 1,600 × 2.5 = **4,000**. The figure 3,200 uses ×2, which covers only 3–6 foes. The band (Deadly, ≥2,500 for five) is still right.
- **Why:** 2014 DMG encounter multipliers (p. 82). SRD 5.1 has no encounter-building section.
- **Fix:** change it to "1,600 XP, adjusted 4,000: Deadly". This is the only one of the 83 printed pairs that fails a recheck. The LOG's audit-script claim ("each ratio is a legal 2014 multiplier") missed it because ×2 is a legal multiplier, just not for 7 foes.

### F2. "Inspiration can reroll this": a 2024 rule left in the text (should-fix)
- **Where:** `05_The_Longest_Night.md:222-223`, Sidebar "Crystals gutter".
- **What is wrong:** the T5.1 sweep changed "Heroic Inspiration" to "Inspiration" but kept the 2024 effect, a reroll. Under 2014, Inspiration gives Advantage on an attack roll, saving throw or ability check, and you spend it when you make the roll, not after seeing it. Chapter I:397-402 and IX:150 now state the 2014 rule, so this sidebar contradicts them.
- **Why:** SRD 5.1, "Inspiration", the paragraph "Using Inspiration" (p. 60).
- **Fix:** "Spending Inspiration gives Advantage on this check, and it is a fine thing to spend it on."

### F3. Pello gets an extra language from the 2024 rogue (should-fix)
- **Where:** `11_Pregenerated_Characters.md:175-176`. The line reads "**Thieves' Cant**, and one more language of his choice."
- **What is wrong:** the extra language comes from the 2024 rogue's Thieves' Cant feature. The 2014 rogue learns Thieves' Cant and nothing more. This line was not in the diff, so the rebuild never touched it. Pello's languages should be Common, the human's one extra, and Thieves' Cant (his background gives two tools, no language).
- **Why:** SRD 5.1, Rogue, "Thieves' Cant" (p. 39 area). `pregen_check.py` does not count languages, so nothing caught it.
- **Fix:** delete ", and one more language of his choice".

### F4. Veteran Bought Sergeant flavour line still assumes the old party size (should-fix)
- **Where:** `10_Bestiary.md:1784-1785`. The line reads "*Card: S3, with four or more characters or on the Bought Sergeant's Nastier line.*"
- **What is wrong:** DESIGN §7 S3 says the Veteran is no longer the four-player default. The card (`09:961-965`), Table X–1 (`10:94`), chapter V (`05:1215`) and chapter VII (`07:843, 876`) all now say "four characters at 5th level, or Nastier". This line still says "four or more characters", which is exactly the leftover the brief asked about.
- **Fix:** "*Card: S3, for four characters at 5th level or on the Bought Sergeant's Nastier line.*"

### F5. Uninvited damage note says "with more characters" (nit)
- **Where:** `10_Bestiary.md:143-144`. The note reads "(with more characters, see chapter V, 'Adjusting the Attack')".
- **What is wrong:** at the four-player baseline, the three-character line lowers the lump to 20, so the threshold changes for fewer characters too.
- **Fix:** "(for other party sizes, see chapter V …)".

### F6. The "2014 layout" blocks still use the SRD 5.2.1 reaction format and section headings (should-fix, layout only)
- **Where:**
  - 14 reactions in `10_Bestiary.md` are still in the 5.2.1 "*Trigger:* … *Response:* …" form: lines 495, 610, 667, 723, 881, 937, 994, 1366, 1558, 1671, 1770, 1826, 1884, 2135.
  - The blocks also keep the 5.2.1 headings **Traits** (27 blocks) and **Bonus Actions** (11 blocks).
- **What is wrong:** SRD 5.1 blocks write a reaction as one prose sentence (e.g. the marilith's Parry: "adds 5 to its AC against one melee attack that would hit it. To do so, … must see the attacker and be wielding a melee weapon"). They have no "Traits" heading, and they put bonus actions among the traits or actions; SRD 5.1 has no "Bonus Actions" section. DESIGN §1 and STYLE_5e "Stat blocks" both promise the 2014 layout, and LOG T1.1 lists everything it converted but leaves these out. The rules still work; only the layout is mixed.
- **Fix:** rewrite each reaction as a sentence ("*Parry.* The sergeant adds 2 to its AC against one melee attack that would hit it. To do so, it must see the attacker and be holding its blade."). Drop the **Traits** heading, and fold **Bonus Actions** into Actions with "As a bonus action, …" (or keep the heading and say in STYLE_5e that it is a deliberate deviation). Add a check to `bestiary_check.py`.

### F7. Natural-armor ACs have no source in parentheses (nit)
- **Where:**
  - `10:217`: the Attendant, AC 17 with Dex +3.
  - `10:1116`: the Hollow, AC 16 with Dex +3.
  - `10:1389`: the Radiant, AC 17 with Dex +5.
  - `10:1907`: the Wept, AC 18 with Dex +3.
  - `10:2076`: Master Vell, AC 20 with Dex +4.
- **What is wrong:** under the 2014 layout, an AC that is not 10 + Dex names its source, "(natural armor)". STYLE_5e says "Armor Class with the armor in parentheses".
- **Fix:** add "(natural armor)", or the trait that grants the AC.

### F8. The common charge's origin is new fiction (should-fix; story change)
- **Where:** `11_Pregenerated_Characters.md:39`. The line reads "Each sheet carries one common charge, **the night's gift to every guest**."
- **What is wrong:** before, the line was a rules justification ("the one Common magic item the SRD gives a character who starts above 1st level"). The new text makes an in-world claim that every guest is given a charge tonight. Nothing else in the module says so: chapter IV's gate and receiving line have no gift-giving, and INVENTIONS #124/#143 record no such fact. It falls under the canon iron law and the brief's "rules and numbers only".
- **Why the old line had to change:** the 2014 DMG's starting-equipment table gives no magic item at 1st–4th level in a low-magic campaign, so the 5.2.1 justification no longer holds. The replacement should be a rules statement, not fiction.
- **Fix:** "Each sheet carries one common charge (a module choice; drop it for a stricter table)." Or ask the owner whether the gift is canon.

### F9. S13: "Draunel and his duelists" now has one duelist (nit)
- **Where:** `09_The_Snakes.md:1853`, "Draunel and his duelists are taking the man …".
- **What is wrong:** the baseline roster is now Draunel and one Veteran Duelist, the box's "two men in good coats" (which now fits). The plural only fits the five-character line.
- **Fix:** "Draunel and his duelist", or "Draunel and his man".

### F10. S14 prose understates the new slugging odds (nit)
- **Where:** `09_The_Snakes.md:2003-2004` says "Few tables get through 144 Hit Points in the rounds an errand takes". The DM Note at `09:2022-2027` says slugging is "a coin flip at best … fewer than half".
- **What is wrong:** the LOG's simulator figure is 45% at 144 HP. "Few" was true at 178/229 HP and is not now. (Both figures come from the 2024 pregens; DECISIONS note (a) already records that.)
- **Fix:** "Many tables don't get through 144 Hit Points …", or match the DM Note's wording.

### F11. Runtime tables are still the three-player budget (nit; already deferred)
- **Where:** `01_Overture.md:273-274` (it now says so openly) and `08_Handouts.md:17` ("Table VIII–1: The Night *(three players; minutes from Table I–1)*").
- **What is wrong:** these are the only party-size numbers outside the cards that are still three-player. The owner deferred them (DECISIONS note (b)), so this is only a reminder: Table VIII–1's caption is the one place a DM reading the night-tracker at the table will see "three players" with no qualifier.
- **Fix (now):** caption it "minutes from Table I–1, set for three players; four run a little long".

## Uncertain findings (judgement calls; check before acting)

### U1. S9 four-at-5th: is Essin fighting? (should-fix if he is)
- **Where:** `09_The_Snakes.md:1539-1542`. The line reads "… Essin is there from the start, and Draunel watches from the rail (1,700 XP; adjusted 3,400: Hard)".
- **The question:** the 1,700 total leaves Essin out. The old five-character line put "Essin on the Boranis side from the start" as a combatant, and the new five line adds his 450 XP "if Essin comes in hostile". If Essin fights here, the roster is 2,150 XP and 7 foes, ×2.5 = 5,375: Deadly for four at 5th (4,400), not Hard.
- **Fix:** either say he doesn't fight ("Essin is there from the start, watching, and his word still ends the Boranis side"), or count him and rebalance.

### U2. S11: how Corro is left out (nit)
- **Where:** `09:1683-1685` and the S11 adjusting lines.
- **The question:** the card keeps Corro's 25 XP in the sum (625) but builds the adjusted total from 600 × 2 = 1,200, so he is out of both the count and the XP being multiplied. The DMG's rule for ignoring a much weaker monster (p. 82) can be read either way. If he is dropped only from the head count, the five-character line becomes 1,250, which is *Medium* for five, not Easy.
- **Fix:** say "(Corro's 25 XP and head left out of the adjusted total)" so the method is explicit. As written, the reward and the band can't both be rebuilt from the printed numbers.

### U3. The Attendant's CR 6 (nit; only internal docs are affected)
- **Where:** DESIGN §7 S14 says "defense HP 144 / AC 17 ≈ 6.0".
- **The question:** by DMG pp. 274–275, 144 HP is CR 6 with expected AC 15, and AC 17 is two higher, which moves defense to **7**. Offense (about 40 DPR with both Focused turns, +7) is 6. The average is 6.5, so CR 6 or 7 are both defensible and the printed CR 6 can stand. The DESIGN arithmetic is wrong, though, and should not be cited as proof. (The Poison and Psychic immunities don't change this.)

### U4. Table IX–1 prints 2014 DMG thresholds multiplied out (nit; copyright)
- **Where:** `09:159-167`.
- **The question:** the table prints the DMG's per-character thresholds (not in SRD 5.1) multiplied out for five party shapes. These are derived facts, not the DMG's table or wording. DESIGN §2.5 and DECISIONS accept it, and the README says the method is "named but not reprinted". I think this is fine, but the owner should know these numbers are the only non-SRD rules data in the book.

### U5. Smaller one-line gaps (nit)
- **S10, three characters** (`09:1639`): "Maiven and one slinger under the window", but the box (`09:1566`) shows "Two figures … standing under" the window. Unlike S2 and S11, the line doesn't say what happens to the box's second figure.
- **Pello's Sneak Attack** (`11:171-172`): the line omits the 2014 conditions that the ally within 5 feet must not be incapacitated and the dagger must be a finesse or ranged weapon (it is). Harmless, but it is a compression of the rule.
- **STYLE_5e "Rules-term capitals"** still says "Write conditions as 'has the Prone condition'", while chapter X now writes "knocked Prone" and "is Grappled". This is an internal-doc contradiction.

## Checked and clean (no finding)
- **Pregens.** All five scores are standard array + 1 + ASI:
  - Serane 15/14/13/12/10/8 → CHA 18;
  - Pello → DEX 18;
  - Andra → INT 18;
  - Dassa → STR 18;
  - Ilesse → WIS 18.

  HP 31/31/26/36/31. AC 14/16/15/17/14 (+2 from *Shield of Faith*). Skill counts:
  - Serane: 2 background + 3 class + 3 Lore, with Expertise ×2;
  - Pello: 2 + 4, with Expertise ×2;
  - Andra, Dassa and Ilesse: 2 + 2 each.

  Every printed skill value and passive Perception is right. Spell counts: bard 3 cantrips and 7 known; cleric 4 cantrips and 8 prepared plus domain spells; wizard 4 cantrips, 8 prepared and a 12-spell book. Second Wind, Action Surge, Channel Divinity (one use), Preserve Life (20), Turn Undead (2014 text), Arcane Recovery (2 levels), Sculpt Spells, Evocation Savant, Fast Hands, Second-Story Work (+4 ft.), Cutting Words and Bardic Inspiration all match SRD 5.1. No Weapon Mastery, origin feats, Remarkable Athlete, Potent Cantrip or other 2024-only feature remains.
- **Stat blocks.** All 29 checked for AC from armor, HP from dice, save and skill bonuses (PB +2 up to CR 4, +3 at CR 6, +4 at CR 9–11), attack bonuses, damage averages, save DCs and CR→XP. Table X–2 values are right, and both of its tables exist in SRD 5.1.
- **Spells** (`tools/build_print.py` SPELLS): all 41 match SRD 5.1 (ranges, durations, dice, Concentration, Spiritual Weapon without Concentration, Healing Word 1d4, Sleep 5d8, Vicious Mockery 1d4).
- **Encounter math:** every other card line, Table IX–1 and Table IX–3 recomputed with 2014 multipliers, the lone-character step up, and each party's thresholds.
- **Leftover sweep:** no "Heroic Inspiration", "Bloodied", "Emanation", "Utilize" or "Magic action" outside the *At a 2024 table* notes. The Attendant's 178/229 HP and CR 8 are gone. Lump 30 and the Wept's 3rd turn are consistent across chapters V, VIII and X. Four potions. S2 "Four people", S11 "three big men" and S13 "two men" all match their rosters.
- **Copyright:** non-SRD books are named only (the variant human, the DMG). No non-SRD rules text or tables are reproduced (but see U4). The SRD 5.1 attribution appears in the README and chapters IX, X and XI, and in the print SRD_NOTE.
