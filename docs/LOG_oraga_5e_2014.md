# LOG: Oraga Night 5e, 2014 conversion

## 2026-11-01: P0 setup and tools

- **T0.1** Branch `feat/oraga-5e-2014` created from `feat/lean-facets` at 2bb8954. Local tag `oraga-5e-2024` pins the 2024 state (never push it).
- **T0.2** `lint_5e.py`, TDD:
  - Tests first: `TestBudget2024`, `TestRules2024`. 6 failed, then all green.
  - `deadly_budget` was replaced by `budget_2024`, which bans the SRD 5.2.1 labels Low/Moderate/High/under Low/beyond High, on XP paragraphs only. "Deadly" is now legal.
  - New family `rules_2024` bans Heroic Inspiration, Bloodied, Emanation, D20 Test, the Magic/Utilize/Study/Influence actions, Weapon Mastery and origin feat. A paragraph that names "2024" is exempt.
  - `ACTIONS` and the lowercase-terms list no longer carry the 2024-only names.
  - Fixture `hard_hits.md` updated. `test_lint_5e.py`: 249 passed.
  - Module report on the unconverted text: 201 hard hits (budget_2024 93, rules_2024 108). This is the conversion's to-do counter, and it must reach 0 by P5.
- **T0.3** `bestiary_check.py`, TDD. It now expects the 2014 layout:
  - `**Armor Class** n (armor)`, with AC computed from the armor;
  - a `**Saving Throws**` line matching the data's save proficiencies;
  - `**Challenge** n (XP)` with no PB;
  - `*Melee Weapon Attack:* +n to hit`;
  - and it flags leftover Initiative or Gear lines.
  
  New tests: 13 written and failing, now passing. Four module-level tests fail until P1 converts chapter X (`fixed_values_clean`, `catch_wrong_xp`, `main_exits_zero`, `layout_clean`). This is expected red.
- **T0.4** moved into T4.1, because the pregen data depends on the rebuilt builds. **T0.5** moved into P6, with the licence and print spell lines.
- **T0.6** Copyright scan with 2014 references. Extracts are in the session scratchpad, never committed:
  - refs: PHB 2014, MM 2014, DMG 2014, Xanathar's, Tasha's;
  - srd: SRD 5.1, SRD 5.2.1.
  
  Result: (a) 37, (b) 3, (c) 3.
  - The three (c) hits are generic rules phrasing that came up only because the 2014 books are now references:
    - 10_Bestiary.md:606 and :962, "can use its reaction to move up to its speed without provoking opportunity attacks";
    - 11_Pregenerated_Characters.md:91, "must succeed on a DC 14 Wisdom saving throw or take".
  - Re-check after P1/P4 rewrite those lines, then allowlist or rephrase.

## 2026-11-01: P1 stat blocks (chapter X)

- **T1.1** All 29 blocks converted to the 2014 layout:
  - Scripted:
    - Armor Class with the armor in parentheses (from the old Gear line, now removed);
    - Hit Points;
    - a one-row ability table plus a Saving Throws line computed from the old Save row;
    - Damage/Condition Immunities and Damage Resistances split;
    - `**Challenge** n (XP)`;
    - 35 attack lines as `*Melee/Ranged Weapon Attack:* +n to hit, reach/range …, one target.`
  - By hand:
    - ten save-list traits as 2014 prose (Put Aside, Seize ×2, In the Church's Name, Provocation ×2, Turn Them Back, Shove, The Rite, Furniture);
    - every Bloodied as "half its Hit Points". The traits named "Bloodied" are renamed **Wounded** (the Hollow, the Radiant, Tavva, the Wept).
    - Emanation becomes a radius around the crystal (Flare, House Flare);
    - "has the X condition" becomes "is X / knocked Prone";
    - the charge release becomes "an action (Use an Object)".
  - Fix during the pass: the attack regex had dropped the period in "ft."; restored on all 35.
- **T1.2** The 2014 box became a "DM Note — at a 2024 table" box (R3). The intro paragraph now states the four-player baseline and the 2014 thresholds for four (500/1,000/1,500/2,000).
- **T1.3** Table X–2 is recaptioned SRD 5.1; its values are identical.
- **Tool follow-ups:**
  - `lint_5e.classify` now recognises `**Armor Class**` as a stat-block opener (test first). Without it, the converted blocks counted as prose, inflating word counts to 95k and unmasking two near-duplicates.
  - The budget rule got the same 2024-note exemption as the terms rule (test first).
  - The escape-DC allowlist entry now matches "Grappled (escape DC".
  - Bestiary tests updated to the new strings; the wrapped-trait test is made non-vacuous.
  - The `facts.yaml` Attendant HP guard pattern is now `**Hit Points** 178 (`.
- **State:**
  - `bestiary_check` reports 0 mismatches. Chapter X has 0 lint hits apart from the Attendant XP note at line 344, which belongs to S14 in P2.
  - Module lint is at 172 hard hits (budget_2024 89, rules_2024 83).
  - `pytest tools`: 676 passed, 1 skipped, 1 failed.
- **Known red:** `test_fact_check::test_module_agrees_after_r2`. The `party_baseline` guard still forbids "built for four", and chapter X now says it. P2 (T2.3/T2.4) rewrites that guard for the four-player baseline.

## 2026-11-01: P2 encounter rebalance

- **T2.1** Chapter IX "Running the Snakes":
  - The four-player baseline. Two characters walking into a card use its *Three characters* line.
  - Budgets use the 2014 DMG method, named but not reprinted (no multiplier table). The four thresholds are given in one sentence.
  - Table IX–1 now gives party thresholds by size, derived sums only.
  - Heroic Inspiration becomes Inspiration.
- **T2.2** Every card S1–S14 follows DESIGN §7:
  - Each budget now prints "*N XP; adjusted M for four: Band.*"
  - Each adjusting line carries a total, in the order One · Three · Five · 4@3rd · 4@5th · Nastier.
  - Table IX–3 is rewritten.
  - Rosters reduced:
    - S3: the Veteran Sergeant is no longer the four-player default (chapters V and VII and Table X–1 updated);
    - S7: three knives;
    - S8: three wardens;
    - S9 and S10: the old three-player rosters;
    - S12: two knives, three at heat 4;
    - S13: Draunel and a Veteran Duelist; the Boranis side is Essin and two Blades.
  - S1, S2, S5, S6 and S11 take their old four-player lines. Read-alouds now say "Four people" (S2) and "three big men" (S11).
  - **S14:** the Attendant is now **CR 6, 144 HP (17d8 + 68)**. The block, `bestiary_check` data and the XP table (CR 5–7 added) are updated.
    - Its Two Turns trait now defaults to the full Multiattack. Three characters get one Joined Hands; a lone character gets no attack.
    - Simulator check, `research/oraga_5e_sim/s14.py --party 4P --rules new`, N=2000, seed 1, **using the 2024 pregens** (the 2014 rebuild is P4):
      - distraction game: 94.2% win / 51.2% drop at 229 HP, and 92.5% / 54.1% at 144 HP;
      - slugging: 0.1% win at 229 HP and 45.0% at 144 HP.
    - The play note is updated to "a coin flip at best" for slugging. Re-run after P4.
  - **Audit script:** all 83 "XP; adjusted" pairs in chapter IX re-derived. Each ratio is a legal 2014 multiplier, and each band matches the party's thresholds. The five S11 flags are Corro's DMG-allowed exclusion.
  - Mistake caught and reverted: S13's 4@5th line had turned Iron 3 into a non-fighting witness, an unasked story change. Restored to a third duelist; the line stays Hard (3,600).
- **T2.3** Chapter V: four is the baseline (the Wept on her 3rd turn, lump 30). "Adjusting the Attack" now carries a Three characters line (4th turn, lump 20); Table V–2 and the Delay-from-damage advice are updated.
- **T2.4** The party-size numbers outside the cards:
  - Chapter I: the four-player baseline statement, card description, runtime note, XP totals and the sidebar "Four at the Table" (pulled forward from T3.2).
  - Chapter III and chapter XI dealing lines; README.
  - Chapter IV: four potions (three for three), and "four players in three or four rooms".
  - Chapter VIII: Wept turn, lump, tracker, agenda deck.
  - Chapter IX agenda deck note; chapter X damage line.
  - **XP totals**, recomputed by the method in LOG_oraga_5e_3p_pass (fight share anchored at 2,200 against the old four-player 14,650 card total):
    - New four-player card total 11,250, giving about 6,000 each. Bottom-up plausible night: 5,981.
    - Three-player card total 9,450, giving about 6,200.
    - Both are short of 6,500, and the milestone rounds up.
  - `facts.yaml` `party_baseline` rewritten for four. It forbids "built/balanced for three" and the 178/229 HP, and checks that three-player values appear only on three-player lines.
- **Copyright:** five generic 2014 stat-block phrases in chapter X allowlisted as class (b), 14 allowlisted in all. One (c) hit remains, at 11:91, a pregen line P4 rewrites.
- **Checks:**
  - fact_check 0; bestiary_check 0.
  - `pytest tools`: 677 passed, 1 skipped.
  - software docs and canon tests: 42 passed; simulator smoke tests: 34 passed.
  - `lint --check` still FAILS on 53 rules_2024 hits outside chapters IX and X. P5 sweeps them. budget_2024 is at 0.

## 2026-11-01: P3 character rules (and early P5/P6 pieces)

- **T3.1** Chapter III:
  - The SRD human (+1 to every score).
  - Backgrounds in the SRD 5.1 shape: two skills, two tools or languages, equipment and a feature, with the Acolyte and the customizing rule.
  - The gift is a **bonus feat at 1st level** (R4). A table using the variant human gives the gift on top of the variant's feat.
  - The gift headings now read "Feat, taken as a bonus feat at 1st level".
  - Ungifted characters take no feat.
  - The Magic Initiate pointer is removed. A short "At a 2024 table" note keeps the origin-feat reading.
- **README:**
  - Rules line (2014, SRD 5.1, *At a 2024 table* notes).
  - Contents rows.
  - The SRD 5.1 attribution, verbatim from the SRD 5.1 legal page.
  - The "Changes from the SRD" paragraph: gift feats and Inspiration.
  - The WotC paragraph now says the 2014 DMG method is named, not reprinted.
- **Chapter I:**
  - The rules line.
  - Inspiration rules: Advantage; everyone starts with it as a module rule; *At a 2024 table* Heroic Inspiration.
  - Table I–3 renamed "Inspiration, Printed".
- Checks: fact_check 0; pytest tools 677 passed, 1 skipped. Chapters I and III and the README have no lint hits.

## 2026-11-01: P4 pregens, P5 terms sweep, P6 licence

- **T4.1 / T0.4** `pregen_check.py` rewritten for SRD 5.1, test-first: the five new builds entered, legality passing, text red. Its rules:
  - human +1 to every score, the standard array, a 2-point ASI;
  - background two skills, no origin feat or Skillful;
  - 2014 cantrip and known/prepared tables (bard 3/7; cleric and wizard cantrips 4, prepared = modifier + level);
  - wizard spellbook 6 + 2 per level;
  - Jack of All Trades counts on Initiative.
  
  Then chapter XI rebuilt, keeping each concept, gear, specialty and story text:
  - **Serane** (Bard, Lore): 9/14/15/11/13/18, AC 14, HP 31, Init +3. Intimidation becomes Jack of All Trades. 7 spells known; Vicious Mockery 1d4; Cutting Words and Bardic Inspiration in SRD 5.1 wording; Song of Rest.
  - **Pello** (Rogue, Thief): 9/18/14/13/15/11, AC 16, HP 31. Six skills (Investigation and Deception dropped). The off-hand dagger is a bonus action. Fast Hands covers Use an Object (charges). Second-Story Work is 2014. Steady Aim and Weapon Mastery dropped.
  - **Andra** (Wizard, Evocation): 9/15/14/18/13/11, AC 15 (Mage Armor), HP 26, PP 11. 4 skills. No Scholar and no Potent Cantrip. Ritual Casting, Arcane Recovery, Evocation Savant and Sculpt Spells. Lattice of 12 spells (Alarm and Feather Fall dropped); 8 prepared (Hold Person added).
  - **Dassa** (Fighter, Champion, ungifted): 18/14/15/9/13/11, AC 17 (scale mail + Defense), HP 36, Init +2. Medicine dropped. Savage Attacker, Alert, Tactical Mind, Remarkable Athlete and Weapon Mastery dropped. Second Wind and Action Surge once per Short Rest; crits on 19–20.
  - **Ilesse** (Cleric, Life): 9/13/15/11/18/14, AC 14, HP 31, Init +1. 4 skills. 4 cantrips (Mending dropped). Domain spells are SRD 5.1 (Lesser Restoration and Spiritual Weapon at 3rd). 8 prepared (Aid and Prayer of Healing added). Channel Divinity once per rest; Spiritual Weapon without Concentration; heavy armor proficiency.
  - The chapter's shared sections are updated: header, SRD 5.1 notice, "Common to all five", the "can stand in a fight" numbers (Dassa AC 17 / 36 HP), and the 2024 note.
- **T0.5** `build_print.py`, test-first:
  - Spell lines rewritten from SRD 5.1 (Healing Word 1d4, Cure Wounds 1d8, Sleep 5d8, Spiritual Weapon without Concentration, and so on); Prayer of Healing and Hold Person added.
  - "Spells known" is parsed; "(once per …)" features get a tracker box; the tracker reads **Inspiration**.
  - Turn lines for Pello and Dassa drop Nick, Sap and Steady Aim.
  - SRD_NOTE names SRD 5.1.
  - Tests: preamble, Inspiration tracker, once-per box, spells known, SRD note.
- **T4.2** The "plays" lines were left as they are. The rebuilt pregens differ little in HP and AC, and the per-card play lines are qualitative. A simulator re-run with 2014 pregens is a follow-up: the research harness hard-codes the 2024 pregens.
- **T5.1** Sweep:
  - 16 × Heroic Inspiration becomes Inspiration (chapters II, IV, V, VIII).
  - Chapter IV's Bloodied becomes half its Hit Points.
  - Chapter VIII's charge release becomes "an action (Use an Object)"; the matching allowlist entry is updated.
  - Lint: rules_2024 at 0; `--check` OK.
- **T6.1** SRD 5.1 attribution, verbatim, in chapters IX, X and XI and the README. The README subtitle, the chapter X subtitle and the commoner line no longer name SRD 5.2.1. Chapter I's casing note no longer cites SRD 5.2.1 (R1 keeps the capitals). The near-duplicate allowlist now has the SRD 5.1 notice.
- **Copyright scan:** (a) 83, (b) 14, (c) **0**.
- **Checks:** fact_check 0, pregen_check 0, bestiary_check 0, lint OK, pytest tools 680 passed, 1 skipped (before the last attribution edits; re-run below).

## 2026-11-01: P7 ledger and close

- **DECISIONS** "The 2014 conversion and the four-player baseline": scope, baseline, yardstick, R1–R4, defaults, and two notes for a later pass (re-simulate S14 with 2014 pregens; four-player runtimes).
- **INVENTIONS** #141 (four-player rosters and party-size numbers), #142 (the Attendant at CR 6), #143 (the SRD 5.1 pregens; supersedes #31's 4th-level choices and #124's numbers).
- **STYLE_5e** now states the 2014/SRD 5.1 declaration, the kept Title Case (R1), the 2014 stat-block layout and the 2014 difficulty vocabulary. The charge example is updated.
- **Memory:** project_oraga_5e_2014_conversion.md.
- **Final checks:** lint OK (0/0), fact_check 0, pregen_check 0, bestiary_check 0, copyright scan (c) 0, pytest tools 680 passed / 1 skipped.

## 2026-11-01: Independent review and fixes

- An independent reviewer agent read the diff `oraga-5e-2024..feat/oraga-5e-2014` cold. Report: `docs/REVIEW_oraga_5e_2014.md`.
  - No blockers.
  - Confirmed: all five pregens, all 29 blocks, all 41 spell lines against SRD 5.1, 82/83 card totals, and Table IX–3.
- **Fixed:**
  - S9 five-character line with Essin: 7 foes ×2.5 = 4,000, not 3,200.
  - Chapter V: Inspiration gives Advantage on the chancy release (was a reroll).
  - Pello: dropped the 2024 rogue's extra language.
  - Veteran Bought Sergeant footer: "four characters at 5th level".
  - 14 reactions rewritten from the 2024 *Trigger:/Response:* form to 2014 prose.
  - Chapter XI: the common charge line is a plain rules note again (dropped "the night's gift to every guest", which was new fiction).
  - Chapter X damage line: 20 with three, 40 with five.
  - S13 "his duelist"; the chapter IX Draunel line now has one duelist and "Two men in good coats".
  - S14 "Fewer than half of tables get through 144 Hit Points" (matches the 45% slugging figure).
  - Table VIII–1 caption.
  - S9 4@5th line now prints the Essin-fighting total (2,150 / 5,375, Deadly).
  - The Attendant's AC shows "(Natural Armor)".
- **Kept:**
  - The **Traits** and **Bonus Actions** headings. They change no rule and help a DM scan; **Reactions** is a 2014 heading anyway.
  - Natural Armor *not* added to Vell or the three Uninvited. They are written up as humans, and the label would hint at their nature (canon).
  - Table IX–1's derived party thresholds: a deliberate DESIGN §2.5 choice; numbers only, no table text.
  - S11's Corro exclusion as stated.
  - The Attendant at CR 6: `bestiary_check`'s DMG estimate is defense 6, offense 7, average 6. The reviewer's defense-7 reading would still round to CR 6–7.
- **Checks:** lint OK, fact_check 0, pregen_check 0, bestiary_check 0, copyright (c) 0, pytest tools 680 passed / 1 skipped.

## 2026-11-01: PR #34 opened; second critical review and fixes

- The owner allowed the push. `feat/lean-facets` was fast-forwarded (27 commits) and `feat/oraga-5e-2014` pushed; tags stayed local. PR #34 targets feat/lean-facets.
- The owner asked for a critical review agent, with a push once its findings are resolved. Report: `docs/REVIEW2_oraga_5e_2014.md`. It found 1 blocker, 8 should-fixes, 11 nits and 3 uncertain items, and confirmed every card total, pregen and block. All are resolved; see the report's "Resolution" section. Tests: 703 passed (+23).
