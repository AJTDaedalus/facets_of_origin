# REVIEW — Facets d20 integration pass

*Integration reviewer (Planner tier), 2026-09-27, branch `feat/facets-d20`. Nothing
committed. Scope: the three drafters' `facets_d20/*.md`, `facets_d20/data/*.yaml`,
`software/tests/test_facets_d20_*.py`, against `docs/BRIEF_facets_d20.md` and
`docs/DESIGN_facets_d20.md`. Every ruling below is also logged in DESIGN §7 under
"Planner (integration review)".*

## 1. Planner rulings applied

| # | Ruling | Where it landed |
|---|---|---|
| a | Full-caster slots read by **caster level** (levels held since taking the tradition talent, the level taken counting as 1), same as Half. Full prepared spells = mod + caster level. Cantrips stay by character level. | DESIGN §2; 01 item 4; 04 *Thaumaturgy*; 05 *Invocation* and the Oathsworn sidebar; 07 (new "Everyone reads their table by caster level" paragraph, Table 7–2 header, Table 7–4); 10; both yaml files (`casting.full_table_index: caster_level` and friends; talent summaries). Tests: `TestCasterLevel` (spells), `TestCasterPresetsUnaffectedByRulingA` (data). |
| b | Mindless and bound creatures never check morale. | DESIGN §3. 08, 09, 10 already said it; no text change. |
| c | Talents may grant Sparks; cap 3 holds. | DESIGN §4. 06 already agreed (*Prophecy* is the one talent that grants them). |
| d | A stunned boss loses one of its two turns, not both: it skips its next turn and the stun ends. | DESIGN §3; 09 Bosses; 03 *Stunning Strike*; yaml summary. |
| e | *Master Plan* / *Seen It Coming* skipping the initiative contest are allowed exceptions. | DESIGN §3; 08 "Who Goes First" now says a couple of signatures do this. |
| f | Oathsworn is a non-caster preset. | Checked README, 01, 02, 07: none calls it a caster. No change needed. BRIEF §4.3 still reads "Paladin-style Oathsworn" / "paladin-ish Soul warrior" half caster; left as the Brain's record. |

Ruling (a) doesn't move the §6 balance table: every caster preset takes its tradition
at 1st level (now tested).

## 2. SRD 5.2.1 verification

Full record: `docs/RESEARCH_facets_d20_srd_check.md`. Sources: the official SRD 5.2.1
PDF (https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf) and the
Open5e `srd-2024` spell list. They agree exactly.

- **All 189 of C's spells are in SRD 5.2.1 at the listed level.** Nothing removed.
- **13 added back** that C had left out as uncertain: Hunter's Mark, Giant Insect
  (Beasts); Divine Smite, Spiritual Weapon (Presence); Searing Smite (Fire); Ensnaring
  Strike (Verdance); Enthrall (Resonance); Find Traps (Divination); Hallow (Warding);
  Aura of Life (The Tide); Elementalism (Storm), Sorcerous Burst (The Arcane), Starry
  Wisp (Fate). All lists stay within 8–15.
- **Confirmed not SRD** (stay out): every smite except Divine, Searing and Shining;
  Thorn Whip, Toll the Dead, Word of Radiance, Hail of Thorns, Zephyr Strike, Summon
  Beast/Fey, among others.
- New test class `TestSrdWhitelist` pins all 202 names and levels, so a non-SRD spell
  or a wrong level fails the suite.
- **Monsters:** five of the six conversions in 09 were right. The **Young Red Dragon's
  Multiattack is 48** (three Rends at 13 + 3 fire), not "about 45"; fixed, boss total
  96, still a 9th-level Standard fight. Its Bloodied line said "instead of biting";
  the 5.2.1 dragon has no bite, so it now says Rend. Added standard-foe HP for the
  Bandit (11) and Zombie (15), and the Goblin's advantage damage (7).

## 3. Consistency pass

Checked and clean:

- Every italicised talent, signature, feature and spell name in all eleven chapters
  resolves to the yaml (script check; 03–05 are also held by `TestChaptersMatchData`).
- Every "Chapter NN" and "Table N–k" reference resolves.
- Numbers in 02, 03, 04, 05 and 10 match DESIGN §1.
- 10 restates only rules stated in 02, 06, 07 or 08.
- "Mirror Master (MM)" throughout; no GM/DM anywhere in `facets_d20/`.
- SRD 5.2.1 attribution in README (Legal section) and as a footer in every chapter.
- Canon: Zahna "he", Zulnut's cigarette and Mordai's defender streak match
  `references/phb-examples.md`. The cigarette in 08 is lit from a lamp the MM had
  already described.
- SRD facts in 08 (actions list, conditions, death saves, longsword's Sap mastery)
  match the PDF.

Fixed:

- 07 opening said "The Body has no magic" right before explaining how a Body character
  becomes a half caster; now "no magic of its own".
- 01's weapon-mastery line was merged into the talents item (see §4).

## 4. Felt simplicity

01 listed **21** numbered differences from the SRD. It now lists **12**, by merging,
not by cutting: presets folded into Facets, ASI and weapon mastery into talents,
domains into spellcasting, fixed HP into levels, lineage into backgrounds, the
opportunity-attack rule into side initiative, fixed damage with Bloodied and morale,
and the MM line moved out of the list. No mechanic was removed. A 5e player who reads
01 now meets 12 things, and 4 of them (Sparks, the attitude track, side initiative,
the monster rules) are small.

## 5. Tests

- `tests/test_facets_d20_data.py` + `tests/test_facets_d20_spells.py`: **193 passed**
  (163 before this pass; +20 `TestCasterLevel`, +3 `TestCasterPresetsUnaffectedByRulingA`,
  +7 `TestSrdWhitelist`).
- Full suite (`--ignore=tests/e2e`): **1284 passed, 0 failed** (7 min 31 s). That run started before the last 3 data tests (`TestCasterPresetsUnaffectedByRulingA`) were added; those pass in the d20 run above, so the suite now stands at 1287.

## 6. Owner questions still open

1. **Mordai's Drives** (protect those who can't protect themselves / won't leave a
   fight while someone weaker is still in it) were derived by drafter A from his
   "defender of the weak" note. Canon for the cast?
2. **Zulnut's Wandering Disciple** in 06 gives him Dexterity/Wisdom/Constitution,
   Acrobatics and Sleight of Hand, and a gaming set. Mechanical detail, but it's the
   first time his background has d20 numbers. Confirm.
3. **Prismatic domains open at 1st level** in this option only (drafter C), departing
   from the core PHB's rule. Needed for the Oracle's Fate. Keep?
4. **Late casters' cantrips** still follow character level, so a character who takes
   Invocation at 6th gets three cantrips at once. Ruling (a) left that alone; cheap, but
   say so if you want cantrips on caster level too.
5. ***Studied Recovery*** still keys on "half your level". Every preset that takes it is
   a 1st-level caster, so it doesn't matter yet; for a late Thaumaturge it should
   probably read caster level.
6. **Unplaced SRD spells**: Divine Favor, Shining Smite and Moonbeam are in SRD 5.2.1
   but every list they fit is at 15. **Starry Wisp in Fate** is the loosest fit of the
   additions (it's there so the Oracle pair has a damaging cantrip); swap if it grates.
7. **Encounter budget** (Table 9–1) is arithmetic, not play. It needs a table before
   release, like everything else in the project.
8. ~~**Dominant-pick review** (BRIEF §6) wasn't part of this pass and hasn't been done.~~
   **Done 2026-09-27** — `docs/RESEARCH_facets_d20_dominance.md`, logged in DESIGN §7
   ("Audit: …"). Five fixes: *Sworn Strike* uses on Soul modifier (Body dip),
   *Radiant Strikes* once a turn, *Aura of Resolve* needs *Interpose* (all four Soul
   presets took it), *Anticipate* unlimited (was dominated by *Glimpses*), *Unarmored
   Defense* (Con) gains advantage on Dex saves (was a trap). Priest/Druid/Oracle late
   picks adjusted; §6 unchanged. Four watch items left for the owner (that file's open
   questions). d20 tests: 206 passed.

Resolved. Return to Worker (or owner review) to continue from `docs/REVIEW_facets_d20.md` §6.
