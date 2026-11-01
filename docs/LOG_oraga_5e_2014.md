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
