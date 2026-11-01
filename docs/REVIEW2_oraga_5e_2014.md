# REVIEW2: Oraga Night 5e, 2014 conversion (PR #34)

An independent second review of `git diff origin/feat/lean-facets..feat/oraga-5e-2014`
(module root `conversions/dnd5e/oraga_night/`, written M/ below). Everything here was checked
against the files and the rules sources. The author's LOG and the first REVIEW were not relied on.
Status: COMPLETE (2026-11-01).

## What was run

- `python -m pytest tools -q` from M/: **680 passed, 1 skipped** (259 s).
- `tools/lint_5e.py`: exit 0. `tools/bestiary_check.py`: 28 blocks plus 1 variant, 0 mismatches.
  `tools/pregen_check.py`: 5 pregens, 0 issues. `tools/fact_check.py`: 0 hits (the baseline is empty).
- `tools/copyright_scan.py --refs cs_refs --srd cs_srd --check`: 0 hits to review. This passes only
  while SRD 5.2.1 is in the allowed corpus (see N6).
- My own cross-check script (scratchpad `rv/xcheck.py`) compared every block's printed ability
  scores, skills, Passive Perception, attack bonuses and damage with the hand-entered data in
  `bestiary_check.py`. They all agree today.

## Verified clean (so nobody re-checks it)

- **Card arithmetic.** I recomputed by hand every XP sum, foe count, multiplier, adjusted total
  and band on S1–S14, including every One/Three/Five/4@3rd/4@5th/Nastier line. I used the DMG
  2014 multipliers (p. 82: ×1, ×1.5, ×2 for 3–6, ×2.5 for 7–10, ×3 for 11–14; one step higher for
  a lone character) and the thresholds in the brief. **Every printed number is correct.** Table
  IX–1 matches the DMG per-character thresholds ×3, ×4 and ×5. The 2024 box's "Low 1,000 ·
  Moderate 1,500 · High 2,000" for four 4th-level characters is also correct.
- **Pregens (XI).** Each one's base scores reduce to the standard array after the human +1 and
  the ASI. HP, AC, Initiative (Jack of All Trades included for Serane), saves, every skill, PP,
  spell DC and attack, cantrip and spells-known/prepared counts, the spellbook size (12, with at
  most four 2nd-level spells), slots, Bardic Inspiration (4, d6), Sneak Attack 2d6,
  Second-Story Work (+4 ft. from Dex), Sculpt Spells, Arcane Recovery (2), Preserve Life (20),
  Disciple of Life, Life domain spells, Improved Critical, Second Wind 1d10+4: all legal and
  correct under SRD 5.1. Every subclass, spell, tool and the human are in SRD 5.1.
- **Stat blocks (X).** The math is all correct. The Attendant (144 = 17d8+68; Con +7, Int +9;
  +7, 9 (1d10+4); Put Aside DC 15) is correct, and by the DMG it comes out at CR ≈ 6. The 2014
  layout is consistent. The Sect Guard matches the SRD 5.1 Guard.
- **`build_print.SPELLS`.** Every line matches its SRD 5.1 spell (Cure Wounds 1d8, Healing Word
  1d4, Sleep 5d8 by HP, Guidance/Resistance as a single d4, Spiritual Weapon with no
  Concentration, Sanctuary's 2014 end condition, Vicious Mockery 1d4 "can hear you").
- **Licence notice.** README, IX, X and XI print the SRD 5.1 legal-page sentence verbatim.
- **2024 terms.** No Heroic Inspiration, Bloodied, Emanation, Magic/Utilize action, mastery,
  Nick/Sap/Steady Aim, origin feat or Resourceful appears outside *At a 2024 table* notes (the
  exceptions are N1 and N2 below).
- **Story and canon.** Nothing changed beyond roster counts, read-aloud head-counts and rules
  terms.

---

## Confirmed findings

### B1 (blocker) — the rule for which line to use still assumes three players, and contradicts itself
- **Where.** `09_The_Snakes.md:101-102` reads "Three or more characters face the printed roster,
  and two use the card's *Three characters* line." `09_The_Snakes.md:556-560` (DM Note, "Movement
  V has five cards") reads "a character alone gets the card's *One character* line, two or more
  the printed roster … if it has split three ways, it is three, one each, each on its solo line."
- **Problem.** The printed roster is now the four-character roster (09:92-94: "Every number … is
  printed for four"). Under 09:101, a three-character party gets the four-player roster and never
  uses its own *Three characters* line. Under 09:558, a pair gets the full four-player roster.
  "Split three ways … each on its solo line" is the old three-player arithmetic: four characters
  split three ways leaves a pair. Both lines were the old "Two or more face the printed roster"
  (old 09:100, 09:554), half-edited. This is the rule a DM reads to size every card, and the
  two passages give different answers.
- **Fix.** In both places: "Four or more characters face the printed roster (five or more, use
  the *Five characters* line); two or three use the *Three characters* line; one uses the *One
  character* line." In the DM Note: "if it has split three ways, that is three cards, each sized
  to its group."

### S1 (should-fix) — chapters IV and X give different potion counts
- **Where.** `04_The_Ball.md:448-449` says "four **Potions of Healing** (three if three characters
  are playing)". `10_Bestiary.md:2210-2211` (The Night's Loot) still says "Three **Potions of
  Healing** (four if four characters are playing)".
- **Fix.** Make chapter X read "Four … (three if three characters are playing)". Add a facts.yaml
  guard (see S6).

### S2 (should-fix) — the Boranis line still counts three Draunel men in S13
- **Where.** `09_The_Snakes.md:364` (the House Boranis line, VI–VII, "What the party can see")
  reads "standing between Vorlain and three Draunel men".
- **Evidence.** S13's Draunel side is now Draunel plus one Veteran Draunel Duelist, "the two men
  in good coats" (09:1867-1868). The Draunel line was updated to "Two men in good coats"
  (diff of 09:~315). The Boranis line was missed. It was correct before, when the roster was
  Draunel plus two duelists.
- **Fix.** "…between Vorlain and two Draunel men".

### S3 (should-fix) — S9's read-aloud shows one second a side, but the card fields two
- **Where.** `09_The_Snakes.md:1448-1449` reads "Another man stands a little behind each of them,
  the way seconds stand." `09:1474-1479` says each side is "the principal and his two seconds",
  and "(the box's seconds are two a side)".
- **Problem.** The box shows four men on the terrace. The default roster is six, and the card
  says the box agrees. This predates the PR, but the PR re-sized S9 and kept the false
  cross-reference.
- **Fix.** Box: "Two more men stand a little behind each of them, the way seconds stand." Or keep
  the box and drop "(the box's seconds are two a side)".

### S4 (should-fix) — Pello's Fast Hands releases crystal charges, which the 2014 DMG forbids
- **Where.** `11_Pregenerated_Characters.md:177-179` (Fast Hands: "…or the Use an Object action
  — a crystal charge included"). `08_Handouts.md:438` and `10_Bestiary.md:2157` ("Releasing a
  charge takes an action (Use an Object)").
- **Evidence.** DMG 2014 p. 141, "Activating an Item": if an item needs an action to activate,
  that action is not a function of Use an Object, so Fast Hands can't activate it. The 2024
  sheet worked because 2024 Fast Hands names the Magic action. The conversion kept that ability
  by calling a release "Use an Object". A rules lawyer at a 2014 table will challenge it.
- **Fix.** Pick one:
  - (a) Remove "— a crystal charge included" from Pello and keep "takes an action".
  - (b) Keep it as a deliberate exception, and say so once in the charge rules: "Releasing a
    charge is a Use an Object action, so Fast Hands can do it (an exception to the usual rule
    for magic items)".
  
  Either way, also update the 2024 box line "releasing a crystal charge, is the 2024 Magic
  action" (10:71-72) to match.

### S5 (should-fix, maintainer) — `pregen_check.py` was rewritten for 2014, but none of its tests changed
- **Where.** `tools/test_pregen_check.py` is not in the diff. Its 13 tests cover only
  `focus_issues`, and one fixture still says "Heroic Inspiration" (test file line 22).
  `pregen_check.py` changed by 112 lines: new CANTRIPS/KNOWN/PREP_ABIL tables, the human +1,
  the Jack of All Trades Initiative and the spellbook count.
- **Problem.** DESIGN §4 promised TDD for this. Nothing tests that a wrong cantrip count,
  prepared count, spellbook size, standard array or JoAT Initiative is caught.
- **Also.** `text_issues` (pregen_check.py:118-133) cross-checks only AC, HP, Initiative and PP
  against the text. Skills, saves, spell DC and attack, the spell lists and the attack lines
  are checked only against the hand-entered `PCs` dict, so the chapter can drift without the
  tool noticing. Andra's `printed_sk` holds Nature +4, Religion +4 and Perception +1, which the
  sheet never prints.
- **Also.** Line 111 prints "Life domain spells always prepared" for the wizard Andra as well
  as Ilesse.
- **Fix.** Add red/green tests for each 2014 table: a bad cantrip count, a bad prepared count,
  a bad spellbook size, a non-array base and JoAT Initiative. Extend `text_issues` to parse the
  **Skills**, **Saving Throws** and spell-DC lines. Make the message depend on the class.

### S6 (should-fix, maintainer) — the facts.yaml guards DESIGN §4 promised are missing, and S1 shows the cost
- **Where.** `facts.yaml`, `party_baseline`. DESIGN §4: "`fact_check.py` and `facts.yaml`: add
  guards for the new baseline (potions 4, Wept turn 3, lump 30) and the licence string."
- **Problem.** The lump, the Wept's turn and the Attendant HP are guarded. There is no potion
  guard (`grep -i potion facts.yaml` is empty), and no guard that every chapter carrying SRD
  material prints the SRD 5.1 notice and no "5.2.1". S1 is exactly the regression a potion
  guard would have caught.
- **Fix.** Add a `sentence` check: `\bPotions? of Healing\b` together with `\bThree\b|\bthree\b`,
  unless `three characters`. Add a `forbid` of `System Reference Document 5\.2\.1` in module
  chapters, and a `require` of the SRD 5.1 notice in README, IX, X and XI.

### S7 (should-fix, maintainer) — most of each block's printed numbers are never compared with `bestiary_check.py`'s data
- **Where.** `tools/bestiary_check.py` `text_problems`/`layout_problems`. They compare the text
  with the data `B` only for AC, HP/HD, CR/XP, armor-derived AC and the Saving Throws line.
- **Problem.** Ability scores, skills, Passive Perception, attack bonuses and damage are checked
  only inside `B`. An edit to the text (say "+6 to hit") passes silently. They all agree today
  (verified by my script), but nothing keeps them in step, and the 2014 conversion re-typed
  every block.
- **Fix.** Parse the ability table, the **Skills** line, **Passive Perception** and each "+n to
  hit … *Hit:* N (XdY + Z)" in the text, and compare them with `B`. My
  `scratchpad/rv/xcheck.py` is a 40-line starting point. Its attack regex needs to handle a
  `*Hit:*` that wraps to the next line (the Bought Blade's Cudgel and the Wept).

### S8 (should-fix) — the Boranis Heat 4 row fields two cousins; S6 now fields three
- **Where.** `09_The_Snakes.md:365` reads "Two cousins on the same terrace (B5) … **S6** (without
  Essin)".
- **Evidence.** S6's roster is now three Cousins of 3160 (09:1115). The row was written when S6
  had two (old 09:1102), and it now gives a different count from the card it points to.
- **Fix.** "Three cousins on the same terrace…". Or keep two and add "(S6's *Three characters*
  line)" if the smaller heat-4 fight is intended.

---

## Nits (confirmed, low impact)

- **N1** `03_Masks_and_Agendas.md:6` reads "It only narrows the **species** step". Species is the
  2024 word. Fix: "the race step" (SRD 5.1 "Races"), or "the ancestry step".
- **N2** `09_The_Snakes.md:142` and `10_Bestiary.md:45` read "the SRD's Knocking Out a
  Creature". That is the SRD 5.2.1 heading. SRD 5.1 calls it **"Knocking a Creature Out"**
  (SRD 5.1 p. 98–99). Fix the name in both places.
- **N3** `09_The_Snakes.md:523-524` reads "With four players, at least one of them [Agendas 1–3]
  stays in the deck." That isn't guaranteed: four players can draw Agendas 1, 2, 3 and 4.
  Fix: "usually at least one".
- **N4** `09_The_Snakes.md:2139` (S14, *One character*) prints no XP or adjusted total. DESIGN §2.5
  says every line carries one. Fix: "(2,300 XP; adjusted 3,450 for one: far beyond Deadly)".
- **N5** `10_Bestiary.md:144` reads "(20 with three characters, 40 with five…)". It leaves out
  "or at 5th level", which 05:388 and 08:102 both include. Fix: add it.
- **N6** `tools/copyright_scan.py` passes with no hits to review only because SRD 5.2.1 is in the
  `--srd` corpus. With SRD 5.1 alone, three hits appear (10:1200, 10:1493, 10:1986, "teleports
  up to 60 feet to an unoccupied space", mm2014 p. 313–314 and phb2014 p. 105/110). The book now
  attributes only SRD 5.1. The phrase is generic, so the fix is to allowlist it as class (b)
  and run the scan with SRD 5.1 alone, or to reword it.
- **N7** `tools/lint_5e_allow.txt:44` still allowlists the old SRD 5.2.1 notice text. It is
  stale; delete it.
- **N8** Bonus Action casing is inconsistent after R1 ("keep Title Case"). The pregens and
  `ON_YOUR_TURN` for Pello, Dassa and the spell lines changed to "bonus action". Serane's,
  Andra's and Ilesse's `ON_YOUR_TURN` lines and chapter IX still say "Bonus Action". Pick one.
- **N9** (pre-existing) `build_print.trackers` misses Serane's crystal charge, because her
  Carrying line wraps between "crystal" and "charge" (11:114-115). Use `re.search(r"crystal\s+charge", …)`.
- **N10** (pre-existing) `09_The_Snakes.md:104-106` lists the cards with a *One character*
  line as "S2, S4, S7, S8, S9, S10 and S13", but S14 has one too.
- **N11** (pre-existing) S13 *Rewards* (09:1924) gives only 1,150 XP. Fighting the Boranis side
  is worth 650. S9 states both sides; S13 should too.

## Uncertain (needs a ruling or a run, not a text fix)

- **U1** The S14 odds in the DM Note "how it plays" (09:2013-2031) come from simulations of the
  **2024** pregens, which have higher stats and Weapon Mastery (DECISIONS 2014 conversion,
  note (a)). The weaker 2014 pregens (Dassa one attack at +6, Andra and Ilesse with 2014
  spells) probably slug worse than "a coin flip at best". The text states the odds as fact.
  Suggest softening to "roughly" until the harness is re-run, or re-running before merge.
- **U2** The 2014 *Player's Handbook* and *Dungeon Master's Guide* are named in III and the
  README. DECISIONS allows naming them. The SRD 5.1 legal page also asks that no other
  attribution to Wizards be included. Naming a book is not attribution, and I think this is
  fine, but it is worth one look by the owner.
- **U3** `lint_5e.py` `rules_2024` skips any sentence containing "2024". That works for the
  notes, but a sentence that mentions the year for any other reason is skipped too. Its term
  list also leaves out *species*, *Versatile* and the mastery property names (Sap, Nick, Vex,
  Topple, …), so N1 got through. Consider adding those, with the same "2024" exemption.

---

## Resolution (author, 2026-11-01)

Every finding is resolved. The text fixes are in chapters III, VIII, IX, X and XI; the tool fixes come with tests.

- **B1** Chapter IX "Size each card" and the Movement V DM Note now read:
  - Four characters face the printed roster.
  - Five or more use the Five line.
  - Two or three use the Three line.
  - One uses the One line.
  - A three-way split is three cards, each sized to its group.
- **S1** Chapter X's remedy box: four potions (three if three characters).
- **S2** Boranis line: "two Draunel men".
- **S3** S9's read-aloud: "Two more men stand a little behind each of them."
- **S4** Option (a): Fast Hands no longer releases charges. The charge rule (chapters VIII and X, and the STYLE example) is "takes an action", with no "Use an Object" label. The 2024 box line ("releasing a crystal charge is the 2024 Magic action") is right for 2024 and stays.
- **S5** 12 new tests in `test_pregen_check.py`:
  - one per 2014 table: cantrips, spells known, prepared count, spellbook size, array/ASI, Jack of All Trades Initiative;
  - text drift: skills, a skill not in the data, saves, spell DC.
  
  `text_issues` now cross-checks every printed skill, the Saving Throws line and the spell DC and attack. Andra's data holds only the skills her sheet prints. The "Life domain" message is printed only for clerics. The fixture's "Heroic Inspiration" is gone.
- **S6** `facts.yaml` `potions_and_licence`: a potion-count sentence check, a forbid of SRD 5.2.1, and a require of the SRD 5.1 notice in the README and chapters IX, X and XI. Mutation-tested on a scratch copy, with three regression tests.
- **S7** `bestiary_check.stat_text_problems` compares each block's printed ability scores, skills, Passive Perception, attack bonuses and damage with the data. Six tests; it runs inside `text_problems`, so `main` fails on drift.
- **S8** Boranis Heat 4: "Three cousins".
- **N1** "race step".
- **N2** "Knocking a Creature Out", in both places.
- **N3** "usually at least one".
- **N4** S14's One line: 2,300 / 3,450, far beyond Deadly.
- **N5** "or at 5th level" added.
- **N6** The scan run with SRD 5.1 alone: the teleport phrase is allowlisted as class (b), and (c) is 0.
- **N7** The stale SRD 5.2.1 allowlist entry is deleted.
- **N8** "Bonus Action" in Title Case everywhere (R1): chapter XI and `build_print`.
- **N9** `crystal\s+charge` in the trackers.
- **N10** S14 added to the list of cards with a One line.
- **N11** S13 Rewards states both sides (1,150 / 650).
- **U1** The S14 slugging line is softened to "worse than a coin flip … and a party of pregens in fewer still". The simulator re-run with 2014 pregens remains a logged follow-up.
- **U2** No change. Naming a book is not attribution; DECISIONS allows it.
- **U3** `rules_2024` now also bans *species*, *Resourceful*, *Skillful* and *Versatile trait*, test first; the weapon property "versatile" stays legal. The mastery property names are ordinary English words (Push, Slow, Nick), so they are left to the existing *Weapon Mastery* term.

Checks: lint OK, fact_check 0, pregen_check 0, bestiary_check 0, copyright (c) 0 with SRD 5.1 alone, pytest tools 703 passed / 1 skipped, software docs+canon 42 passed.
