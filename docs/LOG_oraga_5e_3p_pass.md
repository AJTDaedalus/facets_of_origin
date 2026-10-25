# LOG: Oraga Night 5e, three-player pass

*Scope: `conversions/dnd5e/oraga_night/` (5e edition), plus lore/canon propagation to
`adventures/oraga_night/` (Facets edition). Tasks: `docs/TASKS_oraga_5e_3p_pass.md`. Design:
`docs/DESIGN_oraga_5e_3p_pass.md`. Findings: `docs/LEDGER_oraga_5e_3p.md`. Rulings: `docs/DECISIONS.md`
TP1–TP26.*

## 2026-10-21: TASKS file written (Planner)

- `docs/TASKS_oraga_5e_3p_pass.md` written: 129 tasks across WP1–WP11, which cover all 111 ledger
  rows (or list them as needing no task).
- 10 tasks are blocked:
  - owner wording or ruling: T7.8, T7.13, T7.14, T8.4, T11.11;
  - confirm items: C1 (T4.11, T7.4, T7.21) and C2 (T6.12);
  - escalation E1 (T7.6).
- **Open questions for the owner:**
  - **C1:** only the east-stair double doors seal at midnight. C1b: do the inner doors still
    lock behind Veier?
  - **C2:** is the S4 roster cut withdrawn?
  - **C3:** TP13's table numbers read as V–4/V–5.
  - **E1:** TP13 versus the owner-ruled *Dinner for Two*.
- **Baseline checks before any edit**, all green:
  - from `conversions/dnd5e/oraga_night/`: lint 0, fact_check 0, bestiary_check 0 mismatches,
    pregen_check 0 issues, `pytest tools` 422 passed;
  - from `software/`: `test_docs_consistency.py` 37 passed.
- **Note:** the simulation harness is still only in a session scratchpad. T3.1 moves it into
  `research/oraga_5e_sim/`.
- No module file was edited.

## 2026-10-21 — WP1 tells on the run path (T1.1–T1.3)

- **T1.1** (`08_Handouts.md`): the tells went in as a "Tells to show" block under Table VIII–1's checkpoints, by Movement (III, IV, V, midnight), not as a seventh column: the table already has six wide columns and a seventh would not print. Every Table V–6 tell appears under the Movement where chapter IV stages it; none invented. The L-096 note (the Movement V glint repeats the crystal-and-light habit) went into 04's "The quiet guest" paragraph, which now names all three habits by sighting.
- **T1.2** (`04_The_Ball.md`): a *Tells to show* sentence in each of the Movement III, IV and V time boxes, matching the sheet block; Movement III adds the target "each of the three should have shown at least one tell to someone at the table".
- **T1.3** (`01_Overture.md`): prep step 4 now names "The Fractures" and points to the sheet's tells block. Kept the current term "Fractures"; WP4 renames to Slow / Stop / End.
- **Checks** (from `conversions/dnd5e/oraga_night/`): `lint_5e.py --check` OK 0; `fact_check.py --check` OK 0; `pytest tools -q` 422 passed. No Facets edit (5e usability only).
- **T1.4** not run: the owner has not asked for commits yet.
- **Also:** TP13's table refs corrected in DESIGN §6 and DECISIONS (Table V–4 tricks 1 and 5, Table V–5 trick 3; TASKS C3 was right).

## 2026-10-22 — owner answers to TASKS C1, C2, E1

- TP27 cut Dinner for Two (E1 option C); TP28 only the east-stair double doors seal at the lights, inner doors still lock behind Veier on Raunu's charge; TP29 S4 cut withdrawn. T4.11, T6.12, T7.4, T7.6, T7.21 unblocked. Owner: commit per package on feat/lean-facets, no push.

## 2026-10-22 — T3.1 simulation harness into the repo

- **The original scripts were gone:** the session scratchpad was empty. They were rebuilt from TUNING_3P §2 (Method), the expected-damage arithmetic, the §3 table, §5 and the Appendix, against the module's chapter X blocks, the chapter IX cards and the chapter XI pregens (SRD 5.2.1). `references/oraga_night/` was not opened.
- **Files:** `research/oraga_5e_sim/`
  - `test_smoke.py`: written first and seen red (collection error, no modules).
  - `skirm.py`: generic card engine, plus the shared pregens, dice, dropping, death saves and crowd rule.
  - `s14.py`: the Attendant, rules as printed now.
  - `chain.py`: Movement V card, S14, S13, S3, with no rest.
  - `README.md`: assumptions, how to run, reproduction tables, gaps.
- **Module files:** none edited, so SA is unchanged.
- **Tests:** `python -m pytest research/oraga_5e_sim -q`: **12 passed** (smoke at N=200, seed 20261022; one regression assertion per script; determinism; CLI). The chain regression first asserted TUNING's absolute 15–21% HP at the gate. That figure does not reproduce, so the assertion was revised to TUNING F5's two qualitative claims (a Movement V card first lowers HP at the gate; C4, with no healer, arrives lower than C1) and the gap is documented in the README.
- **S14, the acceptance check:** `python research/oraga_5e_sim/s14.py --all --n 4000 --seed 1`. Engaged win against TUNING:

  | Party | Harness | TUNING |
  |---|---|---|
  | C1 | 87.3 | 90.7 |
  | C2 | 90.9 | 93.4 |
  | C3 | 92.7 | 93.7 |
  | C4 | 94.1 | 95.9 |
  | C5 | 93.6 | 95.2 |
  | 4P | 85.1 | 90.1 |

  The three-player span is 87.3–94.1, inside TUNING's 90–96 band with its ±3 tolerance. C1 is 3.4 under its own point value.
  - Also: naive 57.6–69.6 (TUNING 57–75); attrited C1 80.5 (TUNING 79–86).
  - Slug C1/C2/C4/C5 within 5 points; C3 34.1 against 17.6.
- **Skirmish cards:** 4,000 runs, seed 1, every card against C1–C5 and 4P. Within ±5 points of TUNING:
  - S7 as written, ≤4% (harness 0.0–3.9);
  - S8 C3, 23% (22.7);
  - S3 C3, 16% (13.5).
  - Inside TUNING's range: S13 to the last C1 (79.8, range 70–93), S10_fix C1 (14.4, range 6–23), S3 C2–C4 (13.3–24.5, range 14–32).
  - Not reproduced: S8 C1 64.5 / C5 26.5 (TUNING 57 / 49), S10 C1 50.7 (82), S4 C1 69.8 (86), S3 C5 46.4 (83), S13 4.5–34.7 (39–74).
- **Chain:** `chain.py --all --n 2000 --seed 1`, then again with `--crowd generous`.
  - Strict-crowd deaths for C1/C2/C5: 17–20%, inside TUNING's 15–21%.
  - Generous: 1–2.5%, against TUNING's 5–7%.
  - HP at the gate: 57–81%, against TUNING's 15–21%. This is the large gap.
- **Best explanation for the gaps** (README "Gaps"): the lost trick lists (S14 C1); TUNING's fights ran longer for the strong-damage parties (slot use, the wicket, S13's end point); and TUNING's §5 HP figures were probably gross damage.
- **Assumptions to note:** Ilesse heals rather than spending slots on Spiritual Weapon or Guiding Bolt, except in S14 slugging. Foes use sticky random targeting. All of S8's wardens fight from round 1. S4 is fought out against its two guards.
- **Use:** the harness is fit for comparing variants (T3.10, T5.8, T5.9). Absolute snake-card rates should be quoted with these assumptions.

## 2026-10-22 — T3.1 review (integrator)

- Verified: `python -m pytest research/oraga_5e_sim -q` → 12 passed.
- **Acceptance partly missed, accepted with a rule.** S14 reproduces (three-player 87.3–94.1 against TUNING's 90–96; C1 is 3.4 under its own TUNING figure, just outside ±3). Most snake-card absolutes and the chain's HP-at-gate do not (README lists them). The originals are gone, so the gap can't be adjudicated.
- **Rule for every later SIM task:** the rebuilt harness is the baseline. Each re-sim runs *both* the current and the changed rules in this harness and reports the delta. TUNING_3P's absolute snake-card and chain figures are not quoted in the book or as targets; its directional claims stand. Recorded in DECISIONS.

## 2026-10-22 — T3.2 three-player baseline guard

- `facts.yaml`: new fact `party_baseline` (TP10; values: lump 20/30, Wept 4th/3rd turn, Radiant stair at the fall + 3 beats, Attendant 180/229). Checks: a `30 damage` / `30+` / `30-damage` sentence without "four"; a Wept/she "third turn" sentence without "four"; any `229` sentence without "four"; forbid "built/written/tuned for four"; require `**HP** 180 (` in 10; require the Wept's "4th turn" and the Radiant's "fall + 3 beats" in 08 (Table VIII–2). No new check shape, so no fixture test.
- `python tools/fact_check.py --report`: **20 hits**, all `party_baseline` (every other fact 0). The guard fires on the current text. Worklist for T3.3–T3.7:
  - 03:197 "built for four" (T3.4) · 11:29 "built for four" (T3.4)
  - 05:78 Wept third turn · 05:260 30+ lump · 05:272 Table V–1 Wept third turn · 05:287 sidebar "built for four" · 05:681 30 damage · 05:706 30-damage (T3.6)
  - 08:45 Table VIII–2 lacks the Wept's 4th turn and the Radiant's fall + 3 beats · 08:82 "30+ damage" (T3.7)
  - 09:92 "Every card is built for four" (T3.3) · 09:1798, 1804, 1910 S14's 229 (T3.7, with 09:1920)
  - 10:16 "built for four" · 10:145 30+ lump · 10:195/200 the Attendant's 229 · 10:1953 the Wept block's third turn (T3.5)
- `python -m pytest tools -q`: 421 passed, 1 failed — `TestRealModule::test_module_agrees_after_r2`, which asserts the real module has 0 fact hits. Expected red with fact_check until T3.7; not re-baselined.

## 2026-10-22 — T3.3 party-size rule, once; Table IX–1

- `09_The_Snakes.md` ("Running the Snakes"): the "built for four" bullet became **Party size**, the one full statement: every number in the module is printed for three 4th-level characters; any other table uses one adjustment line, in the order four, five, four at 3rd / 5th; Table IX–1 gives the budget; chapter V's sidebar carries the same lines for the attack. The five-at-5th rule is unified: "use the 5th-level line, and on a card add one of the weakest foes as well" (chapter V's version lacked the foe; the foe clause is scoped to cards, since the attack has no foes to add). The Nastier line is "one dial for a table that wants it harder" (it is a block-level dial, not a party size). The budget bullet now quotes three: Low 750 · Moderate 1,125 · High 1,500.
- Table IX–1: the three-at-4th row is bold (it was already first; the four row was the bold baseline).
- `05_The_Longest_Night.md`, sidebar "Adjusting the Attack": the rule sentence is now a pointer to chapter IX, "Running the Snakes", and Table IX–1. Its lines are reordered in T3.6.
- Checks: lint OK 0; fact_check FAIL 18 hits (was 20; the two cleared are 09:92 and 05:287; expected until T3.7); bestiary_check 0 mismatches; pregen_check 0 issues; `pytest tools` 421 passed, 1 failed (the same real-module fact test).

## 2026-10-22 — T3.4 "Three at the Table" box

- `01_Overture.md`, "The First Five Minutes": new **Sidebar — Three at the Table** after the four steps. Deal Dassa, Ilesse, Serane with Agendas 8 / 4 / 2 face up (8 The Vanished Servant, 4 The Cousin's Errand, 2 The Prelate's Question: each pregen's suggested agenda); swap Serane for Pello for more steel, agendas unchanged; never leave out Ilesse unless somebody else heals; Agenda 4 always dealt, never face down, described as "the route to the east-wing door" (TP13). Four players: add Andra or Pello. Step 1's four-player line is now a pointer to the sidebar.
- Pointers: `03_Masks_and_Agendas.md` "The Ready-Made Guests" (also drops "somebody reaching Veier"); `11_Pregenerated_Characters.md` (the "With four players" paragraph became "Which to deal"); `README.md` Players line (three at 4th; cards carry four/five and 3rd/5th lines).
- Checks: lint OK 0 (a first draft tripped the soft "the players" count; reworded); fact_check FAIL 16 hits (03:197, 11:29 cleared; expected until T3.7); pregen_check 0 issues; bestiary_check 0; `pytest tools` 421 passed, 1 failed (real-module fact test, as before).

## 2026-10-22 — T3.5 chapter X blocks print three-player numbers

- `10_Bestiary.md`:
  - "How to Read This Chapter": blocks built for three 4th-level characters; budget for three 750 · 1,125 · 1,500, other tables Table IX–1.
  - Spell table, "Damage, a lot of it": 20 or more damage, pointer to chapter V's "Adjusting the Attack" for more characters.
  - **The Attendant:** HP 180 (24d8 + 72). 180 is not reachable with d8s at Con 18, so Con 18 → 16 (mod +3, save +6): **TPN-1** in DECISIONS, for Planner review. *Two Turns*: the second Focused turn is one Joined Hands (the old S14 three-character line), full Multiattack with four or more (card S14). Footnote: "more than twice High for three" (3,900 vs 1,500), plus "With four characters it has 229 Hit Points (card S14)".
  - The Wept's *Delay* trait: fourth turn, pointer to "Adjusting the Attack".
  - Master Vell: "even four 5th-level characters land roughly 15 damage a round" (the estimate kept, no new number).
- `tools/bestiary_check.py`: the Attendant's hand-entered data follows the block (hd 24, hp 180, Con 16). Yardstick line: def 9, off 7, ~CR 7 against stated 8 (−0.5 step, informational).
- Not changed: `research/oraga_5e_sim/s14.py` still carries `con_save=7`; nothing in it rolls the Attendant's Con save.
- Checks: lint OK 0; bestiary_check 0 mismatches; pregen_check 0; fact_check: no hits left in 10 (11 remain, 05/08/09, expected until T3.7); `pytest tools` 421 passed, 1 failed (real-module fact test).

## 2026-10-22 — T3.6 chapter V numbers, three first

- `05_The_Longest_Night.md`: The Midnight Clock step 3 (the Wept on her fourth turn; third with four); "Damage counts only in lumps" (20); Table V–1's Wept row (fourth turn); *How Leashed plays* (20 damage a round); the DM Note "the table that will not stop trying" (every 20-damage round).
- Sidebar "Adjusting the Attack": lines now *Four characters* (third turn, 30 lump) · *Five* (as for four, 40 lump) · *Four at 3rd* (as for four, plus the 3rd-level crossfire) · *Four at 5th* (as for four, 40 lump, 5th-level crossfire). The level and five lines used to inherit the four-player Wept turn and lump from the baseline; now they say so explicitly, so no line changes its old values.
- B12's pointer to card S3 now names the three-player roster: the **Bought Sergeant**, the Veteran for four or more at 4th level or higher (follows S3's existing lines; S3 itself swaps in T3.8).
- Checks: lint OK 0; fact_check: 05 clean (6 hits left, in 08 and 09, for T3.7); bestiary_check 0; pregen_check 0; `pytest tools` 421 passed, 1 failed (real-module fact test).

## 2026-10-22 — T3.7 DM sheet numbers; Wept turn and Radiant beat

- `08_Handouts.md`: Table VIII–2's Wept row gains "she reaches him on her **4th turn** (3rd with four characters)"; the Radiant row gains "Private stair, which he reaches at the **fall + 3 beats**" (the private stair is the garden stair, per `facts.yaml` `stairs`). Page Two's Buying Time line: "20+ damage to one in a round → 1 Delay (30+ with four characters, 40+ with five or at 5th level)". The sheet had no Attendant HP to change.
- `09_The_Snakes.md`, card S14: budget text recomputed for three (offense ~CR 4 with three blows a round by the DMG damage bands, defense ~CR 9 at 180 HP, matching `bestiary_check`'s yardstick; 3,900 XP "more than twice High for three (1,500)"; Idle ~CR 5, 1,800 XP "just over High"); the DM Note's line list names four/five/3rd; Outs "180 Hit Points"; Adjusting lines (09:1920): *Four characters* 229 HP, full Multiattack on the second Focused turn · *Five* 260 HP, full Multiattack, DC 20 · *Four at 3rd* 210 HP, DC 18 (the single second turn is now the baseline). *A table built to hit hard* (300 HP) and *Four at 5th* left as printed; WP5's S14 re-sim (T5.9–T5.10) should confirm 300 at three.
- Not changed: Table VIII–1's "(four players; minutes from Table I–1)". Those are runtime minutes, not a party-size mechanic, and no three-player runtime exists to print.
- Checks: lint OK 0; **fact_check --check OK 0** (the T3.2 guard is satisfied everywhere); bestiary_check 0 mismatches; pregen_check 0 issues; **`pytest tools` 422 passed** (the real-module fact test is green again).

## 2026-10-22 — T3.8 card format S1–S7

- `09_The_Snakes.md`: in each card the old *Three characters* roster became the printed **Enemies** roster; the old base roster moved to a *Four characters* line; budgets, labels (against Low 750 · Moderate 1,125 · High 1,500) and **Rewards** XP follow the new roster. No roster was re-tuned (WP6 does that).
  - S1: six kinsmen + principal, 175 XP (under a quarter of Low); Nastier 200 XP (was 250 = base + 25); four: eight + principal (225).
  - S2: Tavva and two of her knives, 550 XP; read-aloud "Three people" (was "Four"); four: all three knives (600); four at 3rd: as for four.
  - S3: **Bought Sergeant** + four Blades, 850 XP, between Low and Moderate (1,950 with the captain, over High). Nastier: the Bought Sergeant's own Nastier line (the veteran holds the gate, 1,500, High) plus the captain a round sooner (2,600); four: the veteran (1,500 / 2,600) with its own Nastier as before; five and four at 5th now name the veteran (they inherited it from the old base).
  - S4: roster unchanged (the old three line was "as printed"); 900 XP relabelled "between Low and Moderate"; the line list now leads with four.
  - S5: Tavva and two of her knives, 550 XP; four: all three (600).
  - S6: two cousins on the terrace, the third stays inside, 400 XP; Nastier brings the third out through the garden doors in round 1 (600 XP); four: all three as the old base.
  - S7: three of the Circle's four knives (the three in the read-aloud), 600 XP; the fourth knife and his DM placement moved from Tactics to the four line (800 XP).
  - Table IX–3: header "three 4th-level characters"; rows S1–S7, S5, S3 and S14 updated (S8–S13 in T3.9).
  - Read-aloud head counts S1–S7 now match: S2 three; S6 two (companion + the man at the balustrade); S7 three (the man + two coats); S1, S3, S4, S5 give no count.
- Consequential pointers outside the file list (the S3 swap would otherwise contradict them): `05_The_Longest_Night.md` B12 (done in T3.6), `07_Cast_of_the_Ball.md` the Bought's two stat-block pointers, `10_Bestiary.md` the faction table row and the Veteran Bought Sergeant's footnote ("the veteran among them. Card: S3, with four or more characters or on the Bought Sergeant's Nastier line"; it said "the one the contract puts at the gate").
- Retinue canon kept: the Circle still "brought four" (S7 fields three of them), Tavva's crew is still three knives (S2/S5 field two).
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed.

## 2026-10-22 — T3.9 card format S8–S14; read-aloud head counts; S9

- `09_The_Snakes.md`, same swap as T3.8 (old three line → printed roster; old base → *Four characters*; XP, labels and Rewards follow):
  - S8: two wardens at the door, the third on the clock's second segment, the fourth never comes; 600 XP; four: the fourth on the third segment (800); five: as for four + a filled lock segment; "Kovaun brought four" kept.
  - S9: **one-side rosters stated**: Draunel side two Draunel Duelists, principal and second (400 XP); Boranis side two Cousin's Blades (200 XP); both 600 XP, under Low. Read-aloud: "Another man stands a little behind each of them" (was "Two more"). **Nastier fixed** (it used the dropped veteran): at three the principal becomes a Veteran Draunel Duelist via the duelist block's own Nastier line, and the Boranis side two Cousins of 3160 (1,050 XP, just under Moderate). The four line keeps the old roster, its 1,150 XP, the box's two-a-side seconds and the old Nastier (1,450). TPN-2.
  - S10: Maiven and the two slingers under the window, 900 XP, between Low and Moderate; Detection now names "the slinger watching the corner" (the box's second figure), since the corner slinger exists only at four; four: the third slinger at the corner (1,000).
  - S11: two bodyguards (box: "two big men", twice), 425 XP; four: three (625), with the box note on the line. Phern's retinue is "two or three" (`facts.yaml` retinues), so two is canon-safe.
  - S12: two knives, both carrying (box already two), 400 XP; at heat 4 a third knife a few paces ahead (600; follows the old four-at-3rd line "three at heat 4"); four: three knives, the fourth at heat 4 (600 / 800).
  - S13: Draunel and one Draunel Duelist (box: "two men in good coats"), 900 XP; "Draunel and his duelists" in What is happening; Boranis side 750 XP relabelled "Low"; both sides 1,650 XP, over High; four: + the veteran (1,350), with the box note.
  - S14: done in T3.7 (no read-aloud head count).
  - S2 four line also notes the box ("Three people" are four).
  - Table IX–3 rows S8–S13 updated; the table now reads entirely at three.
- `flow/flow.json`: S13's summary "Lord Draunel and two duelists" → "his duelists"; `python build_flow_page.py` rebuilt `oraga_night_flow.html`.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed.

## ESCALATION — T3.10 solo-line simulations (blocks T3.11)

**What was tried (two passes, `research/oraga_5e_sim/skirm.py --solo`, seed 1; scratch scripts only, no harness or module file changed):**

1. *Current rule* (a lone PC walks into the printed three-character roster, "one card per group"), n=2000, drop % per pregen:

   | Card | Dassa | Ilesse | Serane | Pello | Andra |
   |---|---|---|---|---|---|
   | S2 | 78.8 | 100.0 | 100.0 | 97.8 | 72.2 |
   | S4 | 98.9 | 100.0 | 100.0 | 99.7 | 100.0 |
   | S7 | 16.6 | 99.9 | 99.8 | 23.0 | 15.7 |
   | S8 | 99.2 | 100.0 | 100.0 | 99.6 | 100.0 |
   | S9 | 15.3 | 94.2 | 91.8 | 31.0 | 23.9 |
   | S10 | 88.5 | 100.0 | 100.0 | 94.8 | 100.0 |
   | S13 | 73.4 | 100.0 | 100.0 | 70.2 | 42.2 |

2. *Candidate solo rosters*, n=2000 (one or two foes from each card's own blocks, card morale unchanged), e.g. S2 Tavva alone 5.1 / 93.0 / 95.2 / 42.1 / 6.0; S4 one guard 37.4 / 100 / 100 / 56.9 / 58.0; S7 one knife 0.1 / 69.0 / 60.6 / 0.4 / 0.1; S8 one warden 1.3 / 82.3 / 98.4 / 4.9 / 5.8; S9 duelist + cousin 0.9 / 43.0 / 38.2 / 5.0 / 3.1; S10 Maiven alone 54.4 / 100 / 100 / 75.1 / 92.0; S13 Draunel alone 35.8 / 100 / 100 / 45.1 / 27.8 (order Dassa / Ilesse / Serane / Pello / Andra).
   Then a grid at n=400: every roster of one or two foes from each card's blocks × morale {first Bloodied, first down, to the last}. **No roster on any card puts all five pregens inside 15–70%.** The best on each card reach three of five, with Ilesse and Serane at 100%.

**What is wrong:** T3.10's acceptance ("each solo roster's drop rate … for every pregen; none under 15% or over 70%") can't be met with one solo roster per card in this harness. The harness gives solo Ilesse and Serane only cantrip offence (Sacred Flame 1d8, Vicious Mockery 1d6) and no outs, so any foe that threatens Dassa, Pello or Andra at all beats them almost every time. Any foe weak enough for them makes the others a token fight. The spread on a single roster runs 40–100 points.

**Question for the Planner:** which of these should T3.10 use?
- (a) **Tune each solo line on the fighting pregens** (Dassa, Pello, Andra in the band) and print a line on each card that a lone talker or healer is offered the card's outs first: the fight is their last resort.
- (b) **Model outs in `skirm.py`** for solo Serane and Ilesse (a per-round chance to end the card through its printed out, using their real skill bonuses), then re-run the band test. This changes the harness, so it needs a spec.
- (c) **Relax the band** to the median pregen, or to three of the five.

T3.10 and T3.11 are marked ⛔. T3.12 and T3.13 are independent and went ahead.

**Resolved (coordinator, 2026-10-22):** option (a). Tune each solo line on Dassa, Pello and Andra (15–70%); each card prints that a lone talker or healer is offered the printed outs first, the fight their last resort (R4); the five-pregen table is logged anyway. T3.10's acceptance amended in TASKS. Resolved. Return to Worker to continue from T3.10.

## 2026-10-22 — T3.12 Movement V time budget

- `09_The_Snakes.md`, DM Note "Movement V has five cards and one hour": new paragraph **Past 2:40, at most one card on screen**: more than one card walked into after 2:40 → run one, resolve the others offstage with their consequence (the clock fills, the heat moves, tell the table what it cost); the same at Gentle, Sharp and Merciless, because it cuts table time and leaves the risk where it was.
- `04_The_Ball.md`, Movement V run box: the same rule as its own paragraph inside the box ("clock filled, heat moved"; Gentle, Sharp and Merciless alike).
- Dependency: the dial's names are used before WP6's T6.1 "How Hard to Go" box exists; T6.1 should keep those three names.
- Lint: a first draft italicised "with their consequence" (hard `emphasis_italics`) and pushed the 04 run box over the 120-word paragraph limit; fixed by dropping the italics and splitting the box.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0; pregen_check 0; `pytest tools` 422 passed.

## 2026-10-22 — T3.13 four-player assumptions in passing

- `04_The_Ball.md`, Movement III summons: "**At least one should be a player character** (with four or more players, by default two)". It said "at least one, and by default two", which is two-thirds of a trio.
- `01_Overture.md`, "Milestone is how this module is built": "a party of three that plays the night fully lands close to **6,700 XP** each … a party of four, close to 6,500".
- **XP arithmetic** (Table I–4; anchored on the printed four-player 6,500 so the same night is compared):
  - Start 2,700. Four-player gain 6,500 − 2,700 = 3,800 per character.
  - Non-fight share, the same at any party size: agenda 200 + omen 100 + closed room 100 + two carried out 200 + dawn 1,000 = 1,600. So the fight share at four is 3,800 − 1,600 = 2,200.
  - Card XP is split evenly, so the fight share scales with card XP per character. Over all fourteen printed cards (base rosters; S3 without the captain; S12 low end; S14 3,900): three 11,750 / 3 = 3,916.7; four 14,650 / 4 = 3,662.5; ratio 1.0694.
  - Three: 2,200 × 1.0694 = 2,352.7; 2,700 + 1,600 + 2,352.7 = **6,652.7 → "close to 6,700"**.
  - Bottom-up cross-check, one plausible full night (S6, S7, S8, S11, S14, S13, S3): four 9,575 / 4 = 2,394, giving about 6,694; three 7,675 / 3 = 2,558, giving about 6,858. Same direction. At three each character takes a bigger share of S14's fixed 3,900.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0; pregen_check 0; `pytest tools` 422 passed.
- **T3.14 (commit WP3) not run:** this session's brief says not to commit. T3.10 and T3.11 are blocked (escalation above), so WP3 is not complete anyway.

## 2026-10-22 — T3.10 solo-line simulations (after the escalation)

- TASKS: T3.10's acceptance amended to option (a); T3.11's acceptance now names the outs-first line. LOG: the escalation is marked resolved.
- `research/oraga_5e_sim/test_smoke.py`: two tests written first and seen red (no `<card>_solo` cards). One checks that each of S2, S4, S7, S8, S9, S10 and S13 has a solo card and runs for all five pregens. The other is a regression: for Dassa, Pello and Andra a solo line is never harder than the current rule (+8 points slack at N=200) and lies between 5% and 85%.
- `skirm.py`: solo cards `S2_solo` … `S13_solo` (the rosters in the notes table). `README.md` gains the run line.
- Results: `research/oraga_5e_simulation_notes.md`, new section "Solo lines (three-player pass, T3.10)". Seed 1, n=2000, current → solo, drop %:
  - Dassa / Pello / Andra: S2 48.4 / 64.5 / 15.0 · S4 37.2 / 58.1 / 58.8 · S7 17.4 / 23.8 / 16.7 · S8 35.8 / 24.8 / 26.1 · S9 15.4 / 30.2 / 23.3 · S10 19.7 / 37.8 / 68.2 · S13 35.4 / 47.2 / 27.4. All inside 15–70%.
  - Ilesse and Serane stay 93–100% on every line, logged as asked.
  - Edge cells checked at seeds 2 and 3, n=4000: S2 Andra 15.8 / 18.0; S9 Dassa 14.8 / 15.4; S10 Andra 67.4 / 68.0.
  - S9 Dassa sits right on the 15% line; the printed roster is kept rather than adding a foe a lone PC wouldn't face.
- Derived solo morale, printed on the cards in T3.11: S2 Tavva goes when she or her knife is Bloodied (from her printed charge-when-Bloodied); S8 the wardens break when one is down; S13 keeps its printed morale (the harness models it as Draunel leaving when Bloodied, as for the full card); S10 "pulls her blows" (from the old four-at-3rd line), modelled as two attacks.
- Checks: `python -m pytest research/oraga_5e_sim -q` 14 passed. No `M/` edit.

## 2026-10-22 — T3.11 solo lines in the cards

- `09_The_Snakes.md`: a *One character* line now leads *Adjusting the Encounter* on S2, S4, S7, S8, S9, S10 and S13 (T3.10's rosters: S2 Tavva + one knife a round behind, she goes when either is Bloodied, 500 XP · S4 one guard, the four still come, 450 · S7 as printed, 600 · S8 one warden + the second in round 3, break at one down, 400 · S9 as printed, 600 · S10 Maiven alone from round 3, two attacks, 700 · S13 Essar Draunel alone, 700). Each line adds "Alone, a talker or healer is offered the outs first; the fight is the last resort."
- "Running the Snakes": new bullet **Size each card to who walks in** (two or more: printed roster; one: the *One character* line; the cards listed; a lone talker or healer, meaning Ilesse, Serane, or any character without real weapon damage, goes to the outs first). The Movement V DM Note's "one card per group" now sizes each card to the group.
- `04_The_Ball.md`: the Movement V run box says "sized to who walks in"; "Running a Scattered Party" opens with three players in three rooms (was four in four) and gains the bullet **A character alone gets a smaller fight**, pointing to chapter IX.
- `08_Handouts.md`: Table VIII–1's Movement V cell reads "One per group, sized to who walks in (alone: the card's *One character* line)".
- S14's solo rule waits for T5.5 (WP5), as the task says.
- Lint: the first draft put the 04 run box back over 120 words; trimmed.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0; pregen_check 0; `pytest tools` 422 passed; `pytest research/oraga_5e_sim` 14 passed; Facets docs + private-canon tests 42 passed.
- T3.14 (commit) still not run, per the brief.

## 2026-10-22 — T2.1 "The east-wing doors" fix

- `08_Handouts.md`, Table VIII–6, the Uninvited's Movement V cell: "Wept: east doors" → "Wept: the east-wing doors" (matches the tell at 05:769, the cradle-song at the east wing doors, and 05:838's "east-wing doors").
- Noted, not changed (outside the task's file): 05:769 spells it "east wing doors" without the hyphen.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed.

## 2026-10-22 — T2.2 Bell glossary; S3 clock wording

- `08_Handouts.md`, Page One after the checkpoints: new paragraph **The bells, in order** (quarter-bells through Movement V, the first for S9 and the half-bell for S10; the bells of midnight at the break; the bells of Oraga tolling as a warning once guests reach the Gatehouse Court; the last bell when the gate is decided or S3's clock fills, end of Movement VII if nobody gets there; the leash's hard limit). Table VIII–1 Movement VII: "(at the latest, when S3's sect-guard clock fills)".
- `09_The_Snakes.md`, S3: "The last bell — six segments" → **The sect guard's arrival — six segments**; on the sixth segment the sect banners come up Gate Street and the last bell rings as their signal; if the gate is decided sooner, the bell rings then. The captain's arrival line and ending 3 now say "the sect guard's clock". Rules unchanged.
- `05_The_Longest_Night.md` (needed for the acceptance's consistency across 05:62–95): the Midnight Clock step 8 and Movement VII's last-bell paragraph and S3 pointer now name "the sect guard's arrival" instead of "the bell clock".
- `04_The_Ball.md`: the pointer to a Bought schedule the DM sheet lacked is replaced by the schedule itself (dusk in the trade district; the runner in Movement V, pointing to ⟨The Bought change sides⟩; the fires at the quarter-bells; the gatehouse from the first bell of midnight; done at the last bell), with a pointer to the DM sheet's bell glossary.
- `flow/flow.json`: S3 summary, `ev-lastbell` summary, `clk-lastbell` label ("Sect guard's arrival (S3)"; id kept). `python build_flow_page.py` rebuilt the page.
- Bell terms checked against 02:131–133 ("by the last bell of Oraga they must go") and 10:131–132 ("at the last bell"): consistent, no change needed.
- INVENTIONS #89 (summary and renaming; the derived reading that the Bought's fires go up during Movement V is flagged for owner review).
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed.

## 2026-10-22 — T2.3 Midnight Tracker, first version

- `08_Handouts.md`: new closing section **The Midnight Tracker (DM)**, 38 lines (limit about 45):
  - an italic DM line (print it, write on it from the lights; the rules live in chapter V, S14 and S3; three-player numbers, four in parentheses);
  - **Tonight's setting:** ☐ Gentle · ☐ Sharp · ☐ Merciless (the dial word);
  - **Table VIII–10: The Midnight Tracker — the Three**, one column per Uninvited: errand; arrival line (the Wept at Raunu on her 4th turn, 3rd with four, plus a turn per Delay spent; the Radiant at the garden stair at the fall + 3 beats, then the Crossing's three beats; the Hollow holding until Raunu falls or his Fracture lands); Delay earned (six circles, crossed when spent); tricks that worked (DC 15 the second time); tells seen (every Table V–6 tell as a box, the witness's initial written in it, so the grid is per character); Fracture landed (with the Wept's DC 15 at 2+ Delay); last blow;
  - **Table VIII–11: The Midnight Tracker — Everything Else**: the Attendant (fired, four broken-focus circles, HP 178 with 229 for four, habits seen, tricks tried, furniture); ward-points (dais four, doors two, sealed doors held, the Root); Raunu falls / saved; the leash; snakes live in the dark; S3's fire clock (4) and the sect guard's arrival (6, captain at the second circle), Blades taken off by retinues.
  - Chapter opening: the tracker closes the chapter on its own page; print it with the first three pages.
- **Placement (TPN-3, Worker call for Planner review):** the tracker is Tables VIII–10/11 at the end of the chapter, not a third DM page, to avoid renumbering Tables VIII–5…9, which TP23 and later tasks cite by number.
- First run: fact_check flagged a bare "229" (party_baseline: a four-player value only on a line saying four); fixed to "178 (229 with four)".
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed.
- **For T2.6 and WP4/WP5/WP6 (not written here):**
  - *Fracture (once each)* row → split into **Stop used** (one box per scene, per Uninvited) and **End tried / landed** once WP4 (T4.5–T4.8) settles the terms; drop "DC 15 while she has 2+ Delay" if T4.5 retires the Wept's DC switch (DESIGN §3.7: +2 per tell).
  - *Last blow* row → **threat marks** (who is marked this scene) once T5.2 lands the threat rule; keep the last-blow throw only if WP5 keeps it.
  - *Delay earned* row: WP4's cap (three turns lost per scene, DESIGN §3.2) and the threat trigger ("earns Delay three times in one scene") both read off it; add a per-scene reset note then.
  - *Tells seen* row: the run-path tells are WP1's; if WP4 changes Table V–6, re-sync the box labels.
  - The Hollow's errand cell says "The main doors (B2)"; T7.3 (TP9) adds the garden doors.
  - The Radiant's Crossing row needs the Last Rite's "rite kept this round" box (T4.8 / T2.6).
  - *Snakes live in the dark* row: T6.7's two default live cards go here.
  - The Attendant row: WP5 changes Focused DC (18) and *Clears the Way*; the tracker prints no DC on purpose, so only HP needs checking after T5.9.
  - The dial word: T6.1 must keep the names Gentle / Sharp / Merciless.

## 2026-10-22 — T2.4 Beats that vanish at three

- `08_Handouts.md`, Page Two before Table VIII–3: new paragraph **Beats that need an agenda**: Anha and her sibling clearing the galleries in Movement VII (Agenda 8); S11's other door (Anha's or Agenda 8's); S8's Prelate's Question (Agenda 2); DC 13 ward-steering (Agenda 5, or an Orthaen who read the wards by hand tonight, per 05:37–41); the truth of the unlocked river gate (Agenda 6); agenda-only snake exits cool on their −1 boxes (Table VIII–5); the Root's key without Thieves' Tools: S8's wardens open the study door (and wipe the slate a round later), or the DC 18 Intelligence (Arcana) improvisation.
- `09_The_Snakes.md`, after "If the table does nothing at all": new paragraph **When nobody carries the agenda**. The three agenda exits (Agenda 1 Circle, 2 Church, 3 Draunel) fall back on their printed −1 boxes: the Circle per knife turned or caught (its two non-agenda ways to 0 still stand), the Church for Kovaun's true thing to file or the wardens turned back at the study door, Draunel for being embarrassed in front of guests. No new mechanic.
- **Not used:** the ledger's "the keys" as a non-Pello route to the Root. No printed key opens B8 (the only keys in the module are the Bought's wicket keys and Corval's key to a guard's *Seal*), so the note names only S8's wardens and the DC 18 check. Planner may confirm.
- First lint run: a bare "DC 13" (hard `bare_dc`) and a fourth "quietly" (soft tic) in 09; both reworded.
- Checks: lint OK 0; fact_check OK 0; bestiary_check 0 mismatches; pregen_check 0; `pytest tools` 422 passed; software Facets docs + private-canon tests 42 passed (no `F/` edit; run as a guard).
- **For WP7 (not done here):** the Thenya's "to 0" (proof of Veier: "the ring delivered and an answer brought back, or anyone who has been in B9") depends on Agenda 4 and B9 access; TP13/TP27 rework it.
- **T2.5 (commit WP2) not run:** this session's brief says not to commit. T2.6 stays open until WP4–WP6.
- **Spotted in passing, not changed (outside WP2):** Table VIII–1's caption still reads "*(four players; minutes from Table I–1)*" after WP3; check whether Table I–1's minutes are now three-player and fix the caption (WP9 runtime or a WP3 follow-up).
- Integrator (2026-10-22): Table VIII–1 caption → three players; 05 'east wing doors' → 'east-wing doors' (3). INVENTIONS #89's 'derived' reading is composed from printed facts (05:959 contract task 1, fires at the quarter-bells; Table VIII–1 puts the quarter-bells in Movement V); left flagged for owner review. TPN-3 (tracker at chapter end) accepted.

## 2026-10-24 — Story-beat review with the owner
- The WP4 phase-A worker (T4.1–T4.4, T5.1–T5.2) stopped when the previous session ended; its partial edits to 05, 10, facts.yaml, tools/lint_5e_allow.txt and tools/test_fact_check.py are uncommitted and unreviewed. Hold until reviewed against TP41–TP43.
- Owner walked every beat (premise, Movements I–VII, the Crossing, the snakes in the dark, epilogue, ⟨If History Breaks⟩, aftermath). Rulings TP30–TP46 recorded in DECISIONS; TASKS status updated (T4.8, T4.15 withdrawn; T4.10 narrowed; T7.8, T7.14 unblocked) and the new work listed at the end of TASKS.
- Noticed in passing, not yet ledgered: 01 "What This Adventure Is" still says "built for four characters… Every fight in it is balanced for four", and Table I–1's minutes are "for four players" (contradicts TP10/WP3).

## 2026-10-24 — WP4 phase A: T4.1, T5.1, T4.2, T4.3, T4.4, T5.2

- **Run order:** T5.1–T5.2 (threat rule, WP5) were pulled forward into WP4 because the run order puts them before T4.5. Order worked: T4.1 → T5.1 (guards) → T5.2 → T4.2 + T4.4 → T4.3 + T4.4. Resumed after the session break; checked against TP41–TP43 (story-beat review): nothing written touches the Crossing, and nothing names or points to a Last Rite.

### T4.1 `facts.yaml`: Slow / Stop / End guards
- `fracture_rule` extended: forbids "nothing bought", "if it lands, that is the success", "Each Fracture works once", "DC 18 with one tell"; `require` the spells-roll sentence word for word in 05 and in 10; `require` "at most three turns per scene" in 05; a second `rule_copy` (home 05) for Buying Time (DC 15 the second time, never a third, the cap, once per Uninvited, half a turn's progress, named people out, nature → 2 Delay).
- `python tools/fact_check.py --report` on the old text: **10 hits**: 05:237 ×2 (both requires missing), 05:254 ("if it lands, that is the success"), 05:763 ("Each Fracture works once"), 08:106 ("DC 18 with one tell"), 10:138 (require missing), 10:148, 149, 150, 152 ("nothing bought").
- `tools/test_fact_check.py`: new class `TestThreePlayerGuards` (7 tests: each new forbid fires on the retired wording, the spells-roll sentence is not a hit, Buying Time and the threat rule restated outside 05 are copies) and `TestRealModule::test_slow_rule_agrees`.
- **Left for T4.5 (not this task's files):** 05:808 "Each Fracture works once" and 08:106 "DC 18 with one tell". `test_slow_rule_agrees` excludes those two matches; `test_module_agrees_after_r2` stays red until T4.5 clears them (TPN-5a; note added to T4.5's body).

### T5.1 `facts.yaml`: threat rule guard
- `down_not_out` replaced by `threat_rule`: the old `rule_copy` elements kept (the crowd rule is still printed once) plus four threat elements (the mark line, three times in one scene, still in the way, the mark lasts the scene); `round after next` forbid kept; new forbids "only ever in mortal danger by choice" and "deadly(,) but not lethal"; `require` the mark line in 05. The coverage test now expects `threat_rule` and asserts `down_not_out` is gone; `test_down_not_out_has_one_home` → `test_threat_rule_has_one_home`.
- `--report` on the old text: **2 hits**: 05:27 (mortal danger by choice), 05:29 (mark line missing). "deadly but not lethal" has no hit in today's text (it never reached the module); kept as a guard.

### T5.2 The threat rule (05)
- Principle 1 (05:24–32): the "mortal danger by choice" sentence is retired; the in-rules note now says a dropped character is set aside, not killed, unless it has become a threat.
- *Down, Not Out* (05:206–260): **Threats.** paragraph (three triggers; the line said aloud, with "He" for the Radiant and the Hollow; the mark lasts until the scene ends); bullets *Not a threat* (the old Stable text), *A threat* (ordinary dying rules; finished only if still between them and their errand on their next turn), *Their quarry* (unchanged); a dial paragraph (Sharp printed; Gentle and Merciless lines, TPN-4). The help-up, crowd, hauling and last-blow bullets are unchanged. The Attendant line now reads "sets people aside the same way" (no rule change; T5.5 makes it lethal).
- Judgment calls: the heading "Down, Not Out" is kept because 01, 08, 09, 10 and STYLE point to it (T5.4 renames); the trigger says "Fracture" until T4.5 renames it to Stop (TPN-4).

### T4.2 Buying Time rewrite (05)
- 05:276–307: **Earn it by being clever** (any creative action that lands: a trick, an attack aimed at the moment, a spell; DC 13 / DC 15 the second time / never a third, wording kept so the existing lint allowlist entry still matches); **Spells roll** (the sentence word for word, then: a landed spell buys Delay through condition immunities, the effect ends at once; each spell once per Uninvited; pointer to chapter X, "What spells buy"); **Their nature pays double** (2 Delay; sorrow / devotion / despair from each printed Truth, pointer to "The Fractures"); the lump paragraph unchanged; **Three turns a scene, at most** (later points still buy Table V–1's "each point", the Uninvited makes its progress anyway).
- 05:322–325: "Delay changes how many, not whether" now ends "Delay alone never changes an outcome; ⟨If History Breaks⟩ … says what does" (was "stack enough of it to change an outcome"). Crystals gutter sidebar: "a spell that lands buys Delay" (was "most spells used well").
- `tools/lint_5e_allow.txt`: two `bare_dc` entries for the spells-roll sentence's "spellcasting ability, DC 13." (05 and 10), with reasons.
- For T4.13: Table V–1 says Delay the Radiant still has at the Crossing is spent at the river gate; whether that counts against the scene cap is not settled here (TPN-5c).
- Not changed (not my files): 08's DM-sheet Buying Time and Down, Not Out lines still compress the old rules (T5.4 / T2.6).

### T4.3 Chapter X "What spells buy" (10)
- 10:128: "Then every door a clever table tries opens a little, and no further." The next paragraph now opens "The reason is in the fiction".
- 10:144–189: the 18-row table is replaced by **What spells buy.** (lands → 1 Delay, nature → 2, once per spell on each; the spells-roll sentence word for word; immunities stay, the effect ends at once) and a 13-item list. Dropped: *Invisibility* and *Sanctuary* on Veier (TP13/TP41), "Just save the saving throw" (in the sentence) (TPN-5d). The following paragraph now points tricks to chapter V.
- *Held by Something Else* (Hollow 10:1171, Radiant 10:1445, Wept 10:1976): adds "or left helpless by laughter or anything else", a spell or effect of that kind that would give the Prone condition ends at once, and if it landed it still buys Delay. The *Hideous Laughter* Prone contradiction is gone. Immunities lines unchanged.
- Lint: `not_but` soft count rose (Sanctuary's "A ward, not a compulsion" moved out of a table); reworded to "It is a ward rather than a compulsion".

### T4.4 Speed-to-turn rule; the Radiant's 20-ft floor
- 05:300–303 **Slowing them**: halved Speed or 20 feet or less for a whole turn is half a turn's progress; two such turns are 1 Delay, within the cap; *Slow*, *Ray of Frost*, *Witnessed* and the Radiant's Fracture all run through it.
- 10:1478–1481 *Witnessed*: "Nothing slows the Radiant below 20 feet" made global (Witnessed, his guilt, *Slow*, *Ray of Frost*, anything else; a whole slowed turn is half a turn's progress). The chapter X list's *Slow* item says the same (10:173–175).

### Checks (end of phase A, from `M/`)
- `python tools/lint_5e.py --check`: OK, 0 problems.
- `python tools/fact_check.py --check`: 2 problems, both T4.5's (05:808, 08:106), as agreed with the coordinator.
- `python tools/bestiary_check.py`: 28 blocks + 1 variant, 0 mismatches. `python tools/pregen_check.py`: 5 pregens, 0 issues.
- `python -m pytest tools -q`: 429 passed, 1 failed (`test_module_agrees_after_r2`, red only for the two T4.5 hits). It was 422 before; 8 tests added.
- INVENTIONS #90; DECISIONS TPN-4 (dial readings, heading kept), TPN-5 (T4.5 worklist, the sentence, the cap, list drops, Held scope).
- No commit or staging, per the brief.

## 2026-10-24 — Story-beat rulings TP30–TP38, TP44, TP46 and the WP3 leftover (all chapters except 05, 10, facts.yaml)
- **TP30 (the cup goes):** 04 Mv I run line, read-aloud heading and read-aloud (cloak over one arm, apart, staring as if someone is expected; nobody comes), the habits sentence, Mv II sighting ("the cloak over its arm"); 07 Attendant (italic head, habits, Unmasking sets down the cloak only); 08 Table VIII–1 (Mv I and VI quiet-guest cells), Table VIII–11 habit box ("the waiting"); 09 S14 skill list (take its cup → Deception or Performance to pose as, or announce, the master it awaits, "your master is here"), habit list, hint 1; 01 Attendant bullet; flow.json (`quiet guest` nodes). F/ has no Attendant (F/05's cup is Raunu's). `tools/lint_5e_allow.txt` line for the 09 S14 DC sentence re-anchored to its new text (one line).
- **TP31 (Corval's third tray):** 04 Undercurrent C italic lead and a new spark (a guest sees Corval carry a tray up himself, alone, in Mv II); 07 Corval (Secret paragraph), Anha (Secret, and the bullet: three plates come back down for washing, together); F/04 Undercurrent C, F/07 Corval and Anha; flow `uc-c` summary.
- **TP32 (the Church's motive):** one sentence in 04 Mv II Church line and the B8 note; 07 Kovaun (after Secret); 09 the Church's *What they came for*.
- **TP34 (mews omen):** 04 Mv IV omen, a DM aside; 07 the Uninvited (new short paragraph); F/04 omen aside (MM), F/07 the Uninvited; flow `omen-4`.
- **TP35 (Thenya wall):** 04 Mv V Thenya ("competent company" sentence replaced); 09 the Thenya's *Walk into it* (the "escort" sentence) and S10's *Go with them* out; flow S10 summary.
- **TP36 (Circle motive and trigger):** 04 Mv II Circle (the knife sees Corval carry a third tray), Mv IV guessing paragraph (Circle fears an heir for its margins; Draunel for the seat), Mv IV Circle line (the chain); 07 Callun (Fears); 09 the Circle's *What they came for*, line rows II and IV, S7 (new *Why Anha, and why now* paragraph).
- **TP37 (the duel):** 04 Mv IV and Mv V Boranis lines; 07 Essin (What Essin Knows bullet); 09 Boranis line row IV, S9 *Where and when*.
- **TP38 (drawer cut):** 04 B8 (drawer bullet cut; "follow the characters home" moved to the great table; note rewritten: the wardens write the map down, wipe the slate); 09 the Church's line row VI–VII, *What is in the study*, *Snake on snake* (what the Prelate learns about the mists), S8 (contents, objective, clock Full, tactics, *Turn the law on them*, *Trade*, *In the dark*, heat 4, treasure, development); F/04 B8; flow (b8, kd-church, S8, ihb-expose summary, two edge labels, S8 clock). B0's half-burned card stays. 06 and 08 never listed the drawer.
- **TP44 (old coin is Vell's):** 09 S3 treasure (the purse is "in ordinary coin"); F/05 B12 (paid half up front, in ordinary coin; the "And the coin" MM paragraph cut). 07 Bought entries and M/06 carried no coin-age test; 02/08/11 old coin is Agenda 6 (Vell) and stays. INVENTIONS #28 retired in part.
- **TP46 (T7.14):** 06 and F/06, the same sentence in both, as the exception beside "the pregnancy never gets out". T7.14 ☑ in TASKS; its `facts.yaml` fact `pregnancy_secret` is still to write.
- **WP3 leftover:** 01 *What This Adventure Is* (built for three, balanced for three, lines for four or five and a party of four at 3rd or 5th), *Fight cards* paragraph (same), Table I–1 lead-in ("for three players"). The minutes were not re-measured: they were budgeted for four, and a three-player table probably runs Mv II a little short (one agenda beat per player). Numbers kept; flag for WP9 runtime.
- **INVENTIONS:** #7, #28, #55, #71 amended; new **#91** (derived wording for this pass). #90 was already taken by the WP4 worker's row.
- **For the Planner:** S9's out "Essin's word ends the Boranis side at once" now sits beside TP37's "Essin cannot call it off without the house being seen to run". It still reads as "he can, at a price" (Draunel's Iron 2 wins), but confirm. Flow nodes `kd-church` and `ihb-expose` now describe the map record although 05 still says "scorched invitations".
- **Checks** (final run): lint OK 0 (first run: a soft not_but, a `tic_quietly`, three long paragraphs I made and the S14 allow line, all fixed); fact_check OK 0; bestiary_check 0; pregen_check 0; `pytest tools` 430 passed; software docs-consistency + private-canon 42 passed; flow rebuilt. A mid-run fact_check hit in 08 ("DC 18 with one tell", 08 Page One) and the 05 hits came from the other worker's in-progress facts.yaml/05 edits and cleared by the final run; 08's line was not touched here.
- **Left for the next worker (05, 10, facts.yaml), locate by quote:**
  - TP30 — 05 Mv VI Attendant read-aloud "a folded cloak and a full cup, set down neatly"; 05 "attendant, holding a cloak and a cup for a master nobody saw"; 05 "the cup and cloak for a missing master" (habits list); 05's distraction rule if it lists a cup trick. 10 Attendant: "carrying a cloak and a cup for a master nobody ever sees" (intro), "it keeps a cup and a cloak ready" (habits), "carrying a cloak and a cup for a" (block lead), Tells "holds a cup for someone who never takes it" and "the cup down on the nearest table". (05's trick "Hand him something… Give him a cup" is the Hollow's, not the Attendant's: leave.) Raunu's "sets down the cup" stays.
  - TP34 — no garden-silence echo found in 05's Crossing.
  - TP35 — 05 Table of the snakes in the dark, Thenya row "She dies there, unless somebody competent went with her", and 05 "she dies there unless somebody competent goes with" (midnight, probably fine; check against TP13/TP35); 10 Maiven *Breaks* "someone competent is going the same way she is" (same).
  - TP38 — 05 snakes-in-the-dark Church row "wardens coming down the dark-wing stair with their arms full" / "The scorched invitations are gone"; 05 Epilogue evidence "the drawer of scorched invitations (if the Church's…" → the wardens' record of the map (or the map seen first-hand); 05 ⟨They expose the truth⟩/history "The Church filing the scorched invitations"; 10 *The Night's Loot* "Whatever the wardens were carrying… It is evidence, and it is heavy" (a written record is not heavy).
  - TP44 — 05 B12 "paid half in old coin" → half up front in ordinary coin; 05 B12 DM note "**And the coin.** … Never confirm it." cut; 10 *The Night's Loot* "The half-fee, paid in old coin — 3d6 × 10 GP by weight. Chapter V says what the coin means" → ordinary coin, drop the pointer.
  - TP46 — `facts.yaml` fact `pregnancy_secret` (T7.14): require the exception beside "never gets out" in 06 and F/06.

## 2026-10-24 — WP4 phase B: T4.5, T4.6, T4.7, T4.9, T4.16

Read against TP41–TP43 first: no Last Rite anywhere (T4.8 withdrawn), the Radiant's only End is the trap, and the party carries Veier at the Crossing. Only 05, 08 (rule lines only), 10 and F/05's Crossing were edited; 01–04, 06, 07, 09 and the rest of F/ belong to the concurrent worker.

### T4.5 Stop; Table V–6
- 05 *The Fractures* (05:774–931) rewritten to DESIGN §3.3: **Stop** (05:793) has three roads: words (an action within 30 ft where they can hear, any fitting skill, the DC is 15, +2 per tell, +4 at most; Intimidation and Deception allowed except Intimidation on the Hollow; a voice carried by *Message* from farther doesn't count, L-075), the third nature trick in a scene, and a printed freeze (the child crying for the Wept). Every Stop: 2 Delay, marks whoever landed it, once per scene per Uninvited. The bands kept: by 4 or less lands after a blow or word (the speaker is already a threat), by 5 or more misses and the scene's Stop is not spent. "**End once; Stop once per scene.**" replaces "Each Fracture works once". Table V–6 is now *Tells*, with its rows unchanged; the 18/15 DC paragraph became +2 per tell. Sidebar renamed *Stops, Ends and magic*: control spells buy Delay and are never the words; *Thaumaturgy* may amplify a speaker within 30 ft.
- Threat trigger renamed: 05:214 "lands a Stop on that Uninvited"; Gentle line "only a landed Stop".
- Other 05 sites: Midnight Clock step 4 (the Hollow "if his End has not already sent him home"), Buying Time (a Stop earns 2 Delay; *Witnessed* and his Stop), Table V–1 (the Wept's "DC 15 at 2+ Delay" cut, DESIGN §3.7), Table V–4 note (lights out as a Stop), default beats ("His weakness (below)"; the looters "no tells, leash, or ward-lore"), the Crossing (a Stop "comes easiest", "a Stop finally landed", "If any character stopped her tonight"), *You Cannot Beat Them* ("Stops and Ends"), ⟨They save Raunu⟩ (terms only: "the Wept's End, Mercy"; T4.14 rewrites the sidebar), ⟨They expose the truth⟩ ("a confession won by a Stop or an End").
- 08 (rule lines only): tells line (08:41), Table VIII–2's Hollow cell ("His End opens the doors"), Page Two Buying Time ("A Stop → 2 Delay") and the old *Fractures* bullet split into **Stop** and **End** (08:105–113), Table VIII–10's Hollow arrival cell and the *Fracture* row → **Stop** (once a scene) · **End** boxes. The rest of the tracker refresh stays with T2.6.
- `facts.yaml` `fracture_rule`: truth rewritten for Stop/End; the `rule_copy` drops "or Deception" and "works once", adds +2 per tell, once per scene, two or more tells, "read the check as a Stop"; a new forbid (05/08/10 only) for "Fracture check/attempt" and "lands/earns/invokes … Fracture" (4 hits in HEAD's 05 and 1 in 10, 0 now). `tools/test_fact_check.py`: the `t45` exclusion in `test_slow_rule_agrees` is removed, and 4 tests are added (the forbid fires in 05/08, the heading pointer is not a hit, files outside the scope are not scanned, a Stop restatement outside 05 is a copy). `tools/lint_5e_allow.txt`: the stale 08 "DC 18 with one tell" entry is removed.
- Lint's first run flagged a bare "DC 15" in the words bullet; it now reads "the DC is 15".

### T4.6 Themes and Stop effects per Uninvited
- 05:852–921: each entry keeps its printed Truth, then *nature* (DESIGN §3.5's list, drawn from the Truth and Table V–6), *Stop* and *End*. The Wept freezes one full round, as printed, and three nature tricks in a scene are her "easier road". The Radiant keeps both printed roads to guilt; the effect is scoped to the scene, including "does not break past Vell" when it lands at the Crossing (TPN-6d). The Hollow steps off the doors for one round. "Cannot be turned" is unchanged.

### T4.7 End: Mercy, Permission, the trap
- 05:825–842: **End** needs two or more tells plus the method and uses the words check. **On success:** out for the night or the errand forfeit, Heroic Inspiration, and the matching ⟨If History Breaks⟩ entry if there is one. **On failure:** it is read as a Stop attempt, and the End can be retried after a new tell. *Mercy* (the Wept; it points to ⟨They save Raunu⟩) and *Permission* (the Hollow; Intimidation never works) are in the per-Uninvited entries. **The trap is an End for all three** (it points to ⟨They trap one of the Uninvited⟩, which T7.2 rewrites) and is the Radiant's only End: "none that words can reach… held there, still hunting, until the last bell", so "cannot be turned" stays literally true. No Last Rite text was written.

### T4.9 TP15: the Radiant at the Crossing
- 05:664: "What the Radiant means to do when he reaches her, the module does not say. Never narrate an attack on Veier herself: his violence goes to whoever is a threat to him ("Down, Not Out") and stands in his way."
- 10:1469 (the Radiant's *Down, Not Out*): a pointer to the same line.
- F/05:199 (Crossing, lore only): "…its violence goes to whoever has made themselves its enemy and stands in its way" (no threat-rule wording; TPN-6g). Printed steps untouched (TP41).

### T4.16 Chapter X Uninvited blocks aligned
- 10:179 (*Darkness* item: "a try at his Stop"). 10:193 *What changes the night* ("Stop and End"; deep crystal "the Radiant's only End"). 10:201 **Stop and End.** pointer paragraph (no DCs; it replaces the 18/15 paragraph). Hollow 10:1207 ***Stop and End — Despair.***, *Breaks* "Only his End". Radiant: *Cannot Be Turned* and *Witnessed* point to "his Stop"; 10:1491 ***Stop — Devotion.*** (for the scene; no End but the trap). Wept: *Delay*'s DC-15 clause cut; 10:2019 ***Stop and End — Sorrow.*** (the child crying needs no check; Mercy); *Breaks* "Mercy does". 10:2241 *Dark-Burst* note "(his Stop)". *Centuries of Practice* 3/Day, the Speed floor and *Held by Something Else* were already aligned (T4.3–T4.4). There is no Last Rite pointer (TP43). *The Post* / *Only the Doors* are left for T7.3; the Root's "will not cross" wording (10:195–196, 08:112) is left for T7.2.

### Checks (from `M/`, end of phase B)
- `python tools/lint_5e.py --check`: OK, 0. `python tools/fact_check.py --check`: OK, 0. `python tools/bestiary_check.py`: 0 mismatches. `python tools/pregen_check.py`: 0 issues. `python -m pytest tools -q`: **434 passed** (up from 429 + 1 failed). From `software/`: `pytest tests/test_docs_consistency.py -q` 37 passed.
- INVENTIONS **#92** (#91 was taken by the concurrent worker). DECISIONS **TPN-6** (a–h).
- No commit or staging.

### Not changed, for later tasks
- 05 *You Cannot Beat Them* still says "A character one of them drops to 0 Hit Points does not die… This mercy covers only the Uninvited and the Attendant" (05:732), and 08's Page Two *Down, Not Out* line says "Nobody an Uninvited… drops dies tonight". Both contradict the threat rule (T5.4 / T6.6).
- TP34's mews omen as a possible Table V–6 tell: not added.

### Remaining "Fracture" sites outside my files (for the sweep; the section name *The Fractures* is kept, so pointers to it may stay)
- 5e: 01:19 (pointer, OK), 01:419; 04:426, 04:829, 04:854, 04:1275; 07:320, 07:355 (pointers, OK), 07:582, 07:606, 07:613; 09:231; README:66 (chapter summary, can stay).
- Facets edition: F/01:136; F/04:279, 570, 571, 588; F/05:122, 144, 185, 192, 206, 234, 237, 249, 252, 254, 257, 260, 278, 415, 450 (F/05's own Fracture rule is Facets mechanics and may stay as it is); F/07:355, 378; F/08:114, 115, 155, 181, 189; F/README:38.

## 2026-10-24 — WP4/WP7 phase C: T7.4, T7.21, T7.8, T4.11, T4.10, T4.12, T4.13, T4.14, and the 05/10 leftovers

Read first: TASKS (header, SA, the task bodies, the story-beat section), DESIGN §3.1 and §6, DECISIONS TPN-4–TPN-6 and TP30–TP46, the previous LOG entries. Rulings applied over older task text: TP41 (the Crossing is printed as is; only pre-midnight and east-wing sites changed), TP42, TP43 (no Last Rite anywhere), TP45 (T4.15 withdrawn), TP39/TP40 (Corval). Locate by quote; line numbers below are today's.

### T7.4 `facts.yaml`: midnight wing routes
- New fact `midnight_wing_routes`: forbids "east wing corridor booms shut", "spent sealing the corridor", a sealed service/garden stair, and Anha's passages as a way in (04, 07); requires the named double doors in Movement VI and a General Features bullet. `--report` on HEAD's text: 6 hits (04:358, 07:93, 05:145, 05:492, two requires); 0 now.
- 05 Movement VI step 2: "The double doors at the head of the east stair boom shut". 05 the dais beat: the first crystal "spent sealing the double doors". 05 General Features: new bullet **The ways into the east wing** (only the double doors seal; the service stair with the wing's service door and the garden stair stay open; the inner doors lock behind Veier on Raunu's last charge).
- 09 S7 terrain, the service door: a parenthesis that it does not seal at midnight and its Movement V guard has gone to the dais or the double doors (Table VIII–7).
- Anha's passages struck as a way to Veier: 04 B9 note (now: they reach the service door, guard doubled, card S7) and 07 Veier; F/07 Veier mirrored. F/04's Undercurrent C trail ("through them needs … Anha's passages") left for T7.6 (dinner complex).
- F/05: the same seal wording (double doors; "spent sealing the double doors").

### T7.21 The Radiant's chase line
- 05 Midnight Clock step 5: the doors locking behind Veier are worth **two** of the three beats and *Witnessed* the third; if Raunu is saved the doors never lock and he reaches the stair one beat after the beat Raunu would have fallen. The east-wing beat's rules note repeats the split. TPN-7a.

### T7.8 Acting early: which door Corval opens (TP39)
- 04 Undercurrent D, *Warning Corval*: a Corval the warning convinces gives them the wing's service door (the key, or he opens it himself); they start the chase there, never with Veier. Same in F/04. The 05 Corval paragraph and 07 Corval carry the payoff. T7.7's other sites (01 promise, Table I–1, 02:383) are T7.7's.

### T4.11 Table V–4 tricks 1 and 5; the east-wing bullet (with TP40)
- 05 Movement VI: new paragraph **"Corval. The stairs."** (05:180–194): sent to the stairs, gathers the characters nearest him (those who helped him first), the service stair and the garden stair, a guide and never a fighter, never to Veier, never meets Vell; the household moves her and Vell takes her at the garden stair out of everyone's sight; a convinced Corval has already given them the service door; his survival is Agenda 1's payoff.
- 05 the east-wing beat: "Nobody reaches her here. The household moves her a door ahead of him…", and a rules note on the routes in.
- Table V–4 trick 1: held from the Radiant's side. Trick 5: the household takes her into the run; a character holds the door (Athletics) or leads him into the run (Survival; Corval added to the no-check list).
- TP40 mirrors: 07 Corval *At the Unmasking*; 02 Agenda 1 DM parenthesis; 08 Table VIII–2 new Corval row; F/05 (Corval paragraph, east-wing line), F/07 Corval, F/08 crisis panel.
- Lint split two over-long paragraphs I made.

### T4.10 (narrowed) the healing line and `veier_unmet`
- 05 the Crossing step 2 (05:668): "The Radiant's cut will not close. Healing magic eases her and keeps her on her feet… the wound does not knit, and nothing in this book says why." 07 Veier *At the Unmasking*; F/05 Crossing step 2 and F/07 Veier (narrative). No text says she is dying.
- New fact `veier_unmet` (04, 05, 07, 08, 09, 11): forbids "carry her", "support her", "take Veier", "with/beside Veier"; `unless` for the household moving her, the Crossing's carry note (Strength 13 / the Help action), Table V–5 trick 3 ("off the gravel"), the boat, Vell in the read-aloud ("pale man") and Raunu's row; a `require` for the healing line. `--report` on HEAD's text: 3 hits (the require, 05 Table V–4 trick 5 "Take Veier", 11:437 "beside Veier"); 0 now. No temporary T7.6 `unless` was needed. Printed Crossing steps, the Speed 15 / carry / Help note, Table V–5 trick 3 and the #66 read-aloud are unchanged.

### T4.12 Sweep for Veier in reach
- Swept 04, 05, 07, 08, 09, 11 and F/04, F/05, F/07, F/08. Changed: 05 Table V–4 trick 5 and the east-wing beat (T4.11), 11 Ilesse's hook ("reach the east wing's door, and the one whose voice Veier listens for through that door at midnight"). Left as printed: every Crossing site (TP41); Maiven's midnight lines (she goes toward the wing, never to Veier); 08 Table VIII–2's Veier row ("on Vell's arm"). Left for T7.6: 04 B9 note, Undercurrent C (04:588 "a way to Veier"), the dinner, 07 Veier's reach list and dinner bullets, 08 Table VIII–6 "dinner for two", F/04:532 and F/04:809, F/07:56. Left for T7.5: 02 Agenda 4's "beside Veier at the Unmasking" and F/03:135.

### T4.13 Crossing rules paragraph; Vell into the boat
- 05 step 3: "the margin should be the characters, not luck" deleted; Vell "already at the oars", his *Elsewhere* action, the boat pulls out with him in it (L-053; north per TP12 is untouched). Rules: carried Delay spent at the gate is one lost turn inside the cap (TPN-5c closed); with none, his one turn goes under the threat rule: unmarked set aside, a marked creature he drops is dying and can die there, no next turn to finish it; the escape fails only by a player character's choice (⟨The child is taken⟩, list unchanged, TP45). DIAL paragraph (Gentle / Sharp / Merciless). TP9 reward (a crowd in the gardens makes him *Witnessed* at the gate) and TP16 pointer (two beats sooner if Raunu lived). No Last Rite.
- VOICE R13 ("decides what the night costs them") and R16 ("at the Crossing it keeps him off the gate altogether") fitted. F/05: Vell at the oars, one sentence (canon).

### T4.14 Saving Raunu (TP16)
- 05 ⟨They save Raunu⟩ (05:1239–1258): four numbered steps: 1 Mercy lands (conditions as printed); 2 Raunu spends the twin crystal on himself and lives, by his own choice, nobody makes it for him; 3 the doors never lock, the Radiant gains the two beats (TPN-7a), the household still moves her and the party is all that stands between; 4 the Midnight Clock counts from the beat he would have fallen (the Hollow turns east, the doors open, the bells), and the Crossing runs as written two beats sooner. The trap route now enters at step 2.
- Dais ward-steering at his side: DC 10 for a character who studied the wards, DC 13 otherwise (05 dais beat, Table V–2 trick 1). The shielding note ("takes them out of the fight… Stable… up within two rounds") now points to the threat rule.
- F/05 ⟨They save Raunu⟩: the narrative (twin crystal on himself, by his own choice; the doors behind her never seal; the players are all that stand between them). No mechanics.

### Leftover sites (lore worker's list)
- TP30: 05 Movement VI box (the folded cloak only), *The Attendant* lead and habit line; 10 Attendant intro, habits, block lead, Tells. The Hollow's "Give him a cup" and Raunu's "sets down the cup" stay.
- TP38: 05 Table V–7 Church row (a written record of the mist map, the slate wiped), ⟨They expose the truth⟩ (the wardens' record of the map, or the map seen first-hand), ⟨A snake gets what it came for⟩ ("The Church writing down the mist map"); 10 *The Night's Loot* ("The wardens' record of the map"). Matches the flow page's `kd-church`; flow.json not changed.
- TP44: 05 B12 "paid half up front, in ordinary coin"; the "And the coin" DM paragraph cut; 10 purse in ordinary coin, pointer gone. INVENTIONS #28 note updated.
- TP46: new fact `pregnancy_secret`: two `require`s, the Circle exception beside "never gets out" in 06 and (by relative path) F/06. Removing the F/06 sentence fires it (checked, then restored).

### Tests, records, checks
- `tools/test_fact_check.py`: 9 new tests in `TestThreePlayerGuards` (the seal forbids, the open-stair non-hit, Anha's passages, Take Veier, beside Veier, the two exemptions, the pregnancy requires).
- INVENTIONS **#93** (wing routes, beats, Corval), **#94** (Crossing, healing, save-Raunu steps, dais DC), **#95** (TP30/TP38/TP44 wording); #28 note updated. DECISIONS **TPN-7** (a–h).
- From `M/`: `lint_5e.py --check` OK 0 (first runs: two long paragraphs and a bare DC 13, fixed); `fact_check.py --check` OK 0; `bestiary_check.py` 0 mismatches; `pregen_check.py` 0 issues; `pytest tools -q` **443 passed** (434 before). From `software/`: `test_docs_consistency.py` + `test_no_private_canon.py` 42 passed. flow.json unchanged, so no rebuild.
- Not touched, for WP5: 05 *You Cannot Beat Them* "does not die" line, 08 Down, Not Out copy, 10 the Radiant's *Down, Not Out* trait, and 05 ⟨A player character dies⟩ ("Neither the Uninvited nor the Attendant ever kills a player character"), which now contradicts the gate rule and the threat rule (T5.4/T5.5).
- No commit or staging.

## 2026-10-24 — WP7: T7.5, T7.6, T7.7, and the "Fracture" sweep outside 05/08/10

Read first: TASKS (header, SA, E1, T7.5–T7.7, the story-beat section), DECISIONS TP11, TP13, TP14, TP27, TP33, TP35, TP39, TP41, TPN-6, TPN-7, and the two LOG entries above. Only 01, 02, 04, 07 (not the Attendant), 09 (line IV of the Church table only), flow, facts.yaml (append), INVENTIONS and F/ were edited; 05, 08, 10 and 09 S14 belong to the concurrent worker.

### T7.6 Dinner for Two cut (TP27, TP33)
- 04 *Dinner for Two (B9)* replaced in place by **The Ring at the Door (B9)**: any Movement before midnight; a guard carries word to her; by default she chooses, the door opens a hand's width, her hand takes the ring, face unseen, answer back through the door (Raunu's "If she chooses you, you will know" kept); she does not speak of a child, the heir is found only through Undercurrent C; a character who gets into the wing another way does not meet her either.
- 04 pointers: B9 note (Agenda 4 "is done at these doors and goes no farther"; Undercurrent C is the way behind them), Veier's rooms ("before meeting her" cut), nursery ("Agenda 8 and Undercurrent C"), the Undercurrents box (C "is the only way to the heir"), Undercurrent C trail ("Only real ingenuity gets through them; the ring opens them a hand's width"; Anha's passages dropped, B9 already says they reach only the service door), Movement IV run box (dinner cut), Movement IV agenda beats (the doors are as near as anyone gets).
- 07 Raunu: the two dinner clauses cut. 07 Veier: *Where she is* rewritten to the door errand, "Guests who come to her door", *What Veier Knows* trimmed to what she says through the door (quote, happy and chose this, fear); the pack, slings and nursery are B9 finds; the child, the two plates and the minute alone cut. 07 Maiven's "for Veier alone" kept (TPN-20d).
- 09 S10: already clear of the escort (no change needed); S10's "Go with them" out matches TP35.
- flow.json: `sc-dinner` → `sc-ring-door` ("The ring at the door", phase m2, ref `#the-ring-at-the-door-b9`), the ev-toast → dinner edge removed, `a4` and `b9` summaries and the a4 → b9 label ("at the door"). `build_flow_page.py` rebuilt.
- INVENTIONS #58 and #72 marked superseded (TP27/TP33, → #96).
- Facets edition: F/04 Movement IV (the door errand as a parenthesis, no mechanics), F/04 B9 Veier's rooms and nursery, F/04 Undercurrent C trail, F/07 Veier *Where she is* and "come to her door", F/08 Table (Veier row: "Agenda 4 at the door only", dinner cut).

### T7.5 Agenda 4's midnight note (TP13)
- 02 Agenda 4 *At midnight*: "yours is the one voice … she will listen for you"; DM parenthesis: done at the east wing door, her hand takes the ring, face unseen, at midnight she listens for that character's voice through the door. F/03 the same, in Facets wording.
- 01:30, 03, 11 (fixed in T4.12), 04's old Undercurrents line (now the heir) and 09's Thenya line: checked. flow.json edge a4 → cross-1 "beside Veier" → "the voice she listens for".
- `facts.yaml`: new fact `veier_door_errand` appended (not an edit of `veier_unmet`, per the append-only rule): forbids "beside Veier", "Dinner for Two", "at dinner" in 01–07, 09, 11 (08 left out, see below); requires the hand-through-the-door line in 04 and "Nobody meets her face to face before the Crossing" in 07. On HEAD's text it fires 11 times (02:357; 04:361, 1197, 1248, 1249, 1304; 07:57, 59, 94, 96, 109), 0 now. `tools/test_fact_check.py`: new class `TestVeierDoorErrand`, 5 tests. "beside Veier": 0 in both editions.

### T7.7 Acting early (TP14)
- 04 Undercurrent D, after "Confronting the three": **Getting Veier out early** refused (Raunu keeps her in the palace until the birth, TP11; she refuses bluntly through the door; she leaves at midnight and not before); **Moving guests early** (not among the dead; tell the table when the night is counted); **Getting ready** (a character who acts on the warning starts midnight wherever they chose to stand). The Corval payoff was already there (T7.8).
- 01 promise: "and to see it pay when the lights die (chapter IV, Undercurrent D)"; Table I–1 Movement V "it pays at midnight"; 01 cut list: "B9's rooms, unless somebody is on Undercurrent C" (the east-wing scene was the dinner). 02 Agenda 6 catch: DM line, an early exit through the gate is refused.
- Facets edition: F/01 Movement V line and the promise; F/04 Undercurrent D, the same refusals and payoffs as narrative.

### "Fracture" sweep (outside 05/08/10)
- 5e: 01:419 "Stops and Ends change outcomes"; 04 B13 "holds no way to Stop or End the Uninvited"; 04 Undercurrent D tells parenthesis (Table V–6) and *At midnight* ("Tells … are this thread's currency"); 04 Church line and 09 Church table IV "(a tell; see chapter V)"; 07 Uninvited lead ("Stops, Ends and full tell-tables"), "tells that arm a Stop or an End", "ward-fire, the leash, Stops and Ends". Kept as names: 01:19 (prep box pointer), 07's two *The Fractures* pointers (Mother Sella, Kovaun), README:66.
- Facets edition: no change. F/01:136, F/04:279/570/571/591, F/05, F/07:364/387, F/08:114/115/155/183/191 and F/README:38 are the Facets edition's own Fracture rule (Soul roll, Hard/Standard by tells, once each) and contradict no canon ruling. TPN-20f.

### Records and checks
- INVENTIONS **#96**. DECISIONS **TPN-20** (a–g).
- From `M/`: `lint_5e.py --check` OK 0 (first run: one long paragraph in Undercurrent C's trail and a "say so" tic, both fixed); `fact_check.py --check` OK 0; `pregen_check.py` 0 issues; `bestiary_check.py` 0 mismatches; `pytest tools -q` **448 passed** (443 before). From `software/`: `test_docs_consistency.py` + `test_no_private_canon.py` 42 passed. flow page rebuilt.
- No commit or staging.

### Left for the 05/08/10 worker (or a later task)
- **08 Table VIII–6**, Veier row: "B9 — dinner for two" (Movement IV cell) and "B9 (Agenda 4 / Und. C only)" (Movement III). Once fixed, add "08" to `veier_door_errand`'s forbid files.
- **05** "And then the counting" (05:1200): T7.7's "guests moved early are not among the dead" points here; the count could name them. No 05 dinner pointer found.
- **Facets canon drift (not in scope):** F/07 Veier's quote says "Tell my **uncle**"; the 5e edition says "cousin" (owner ruling Q24, INVENTIONS #73). Owner to confirm which edition is right.

## 2026-10-25 — WP5: T5.3–T5.11, and the 08 Table VIII–6 follow-up

Read first: TASKS (header, SA, SIM, DIAL, T5.3–T5.11), DESIGN §2.1, §3.1, §4, DECISIONS TP5, TP6, TP17, TPN-1–TPN-7, TP30–TP46, the T3.1 review rule. Locate by quote; lines below are today's. Calls for Planner review: **TPN-8 (a–k)**. INVENTIONS **#97**.

### Follow-up from the lore worker (before T5.3)
- 08 Table VIII–6, Veier row: III "B9, behind the door (Agenda 4: her voice)", IV "B9, behind the door (Agenda 4: her hand takes the ring)" (TP27, TP33). `facts.yaml` `veier_door_errand` forbid now lists "08"; its why no longer excuses 08. `test_08_is_out_of_scope` became `test_08_dinner_row_is_forbidden` (the guard fires on the old row).

### T5.3 Damage to a set-aside creature, per dial
- 05 *Down, Not Out*: new paragraph **Hitting someone who is down** (05:255): Sharp and Merciless, the ordinary rules (a failure, two on a crit; Stable ends); the Uninvited never aim at the set-aside, the Attendant only as its block says; crossfire, trampling and area spells reach a body on the floor; Gentle, no damage until up. Pointers: *Two Hundred People* trampling bullet and the Crossing's crossfire sidebar (its own paragraph, to keep the sidebar under 120 words). 10's side is in the Attendant's *Removes Interruptions* (T5.5).

### T5.4 Rule copies become pointers
- 10 How to Read: the *Down, Not Out* bullet is now a pointer (set aside unless a threat; the Attendant Idle / Focused). The three Uninvited traits renamed ***Threats Only*** (10:1197, 1480, 2016), each a pointer plus its own rule (the Hollow's 30 feet; the Radiant's Veier line; the Wept's shielding mercy, now for a creature that is no threat to her). 08 Page Two *Down, Not Out*: the threat triggers, the line, Sharp's finishing, the Attendant, the last-blow throw (two `rule_copy` elements, under the max). 09 needed no change beyond S14 (its snake-fight crowd pointers are the crowd rule, not a copy).
- Also fixed (named in the brief): 05 *You Cannot Beat Them* "does not die" bullet → "set aside, not killed, unless … a threat"; 05 ⟨A player character dies⟩ (05:1351) now lists a Focused Attendant and an Uninvited finishing a threat (TPN-8k).

### T5.5 Attendant: lethal, *Clears the Way*
- 10 the Attendant: ***Removes Interruptions*** (10:290) replaces *Down, Not Out* (Idle drops set aside; Focused drops dying; Sharp / Gentle / Merciless). ***Clears the Way*** (10:282): a turn's action at its start, no adjacency; Idle when nobody attacked it since its last turn; Focused on its second turn, or it attacks if there is no Delay to take (TPN-8a); a lost turn clears nothing. *Two Turns*: the second turn clears or makes one Joined Hands (full Multiattack at four, no attack against a lone character).
- 05: the Attendant paragraph in *Down, Not Out*, *Buying Time*'s "The Attendant takes Delay away", *The Attendant* bullets ("It and Delay feed each other", "It can kill", 05:501). 07 the Attendant: "Whoever it drops while it is Idle is only set aside … Focused, it can kill". 08 the Attendant line ("its drops are dying") and *Clears the Way*. 09 S14 *Tactics*, the clock paragraph, *Development* (the dying make saves). Solo line in S14 *Adjusting* (09:2017).
- "Deadly but not lethal" appears 0 times; `bestiary_check` 0 mismatches.

### T5.6 Distraction at three; edge rules
- 10 *Can Be Distracted*, 09 S14 full rule, 05 bullet, 08 line: DC 18 Focused; the Help action applies; a trick tried while Idle isn't spent ("a trick already tried … while it was Focused"); a natural 20 while Idle costs its next turn (TPN-8b); 09 *Failure while it is Idle: nothing happens*. *Literal Orders*: "since the start of its previous round". Four `lint_5e_allow.txt` bare-DC entries re-anchored from 19 to 18.

### T5.7 S14 control note, tie, scene binding, the Root
- 09 S14: **One scene at a time** (09:1844, the ledger's sentence), the tie rule in *Enemy* (09:1871), **Spells that stop it** (09:1954: *Sleep* fails, *Hold Person* can't target, a turn lost to *Command* or *Hideous Laughter* is lost but not a break). 10: ***Where the Three Go*** (10:297) points to the scene binding and carries TP17 ("the Root included: nothing there touches it").
- `facts.yaml`: no `root` fact existed (T7.2's); a minimal `root` fact with the TP17 `require` in 10 was added (TPN-8i). Two tests (`TestRootAttendant`): the require fires without the line, not with it.

### T5.8 Update `s14.py` to the new rules
- `research/oraga_5e_sim/s14.py`: a frozen `Rules` dataclass with 13 switches (`lethal` with the dial, `clears_action`, `solo_line`, `help`, `dc18`, `idle_free`, `nat20_idle`, `orders_window`, `tie`, `cap3`, `spells_roll`, `tp30_tricks`, `put_aside_recharge`); `OLD` all off, `NEW` all on; `--rules`, `--dial`, `--hp`, `--dc`, `--moves`, `--solo`, `--level3`, `--wp5`; parties `5P` and `4S` for the adjusting lines. Found and fixed (as a switch) a T3.1 bug: *Put Aside*'s recharge was never rolled.
- **OLD reproduces T3.1 draw for draw:** `s14.py --all --n 4000 --seed 1` before and after is byte-identical (the seed string is unchanged under OLD).
- `test_smoke.py`: 10 new tests (OLD = baseline; every switch runs; lethal only kills when lethal, ordered by dial; Idle drop set aside vs Focused dying; damage to the downed by dial; *Clears the Way* as an action, blocked when struck or on a lost turn; Help, DC 18, Idle try not spent, the orders window; the cap; the solo line and TP30 tricks; the Sharp targets). `python -m pytest research/oraga_5e_sim -q`: **24 passed** (14 before).

### T5.9 S14 re-simulation
- Seed 1; n = 4,000 a cell for the main table (`s14.py --wp5 --n 4000 --seed 1`), 2,000 for the side runs. Full tables in `research/oraga_5e_simulation_notes.md`, "S14 under WP5". Current → WP5 Sharp, engaged win / PC death: C1 87.3 → 97.6 / 0.3, C2 90.9 → 97.2 / 3.8, C3 92.7 → 93.6 / 5.7, C4 94.1 → 96.2 / 5.5, C5 93.6 → 95.7 / 3.4, 4P 85.1 → 92.2 / 0.5. Slugging wins 0.1–25.7%, deaths 2.3–21.5%. Gentle: no deaths anywhere. Merciless: engaged deaths 3.6–15.3%, slugging 20.8–47.4%.
- **Targets at Sharp met in the first round; no tuning** (TPN-8g). Main movers: Help (+8 win), DC 18 (+4), the *Literal Orders* window (drops nearly double).
- L-042: the extra Wept turn holds (clock 5 instead of 6 costs engaged trios 8–13 points). L-041: on the printed clock the errand beats an engaged party 2–6%; "usually times out" is true only for a late card (engaged 3–10%, smart 25–29%). L-003: Idle-grind wins 0.0% in every cell; no XP halving (TPN-8h).
- Adjusting lines (n = 2,000): five 260 / DC 19, four at 3rd 210 / DC 17, hit hard +30 (208 at three, 259 at four; proxy method TPN-8f). The block's 178 (21d8 + 84) and 229 are unchanged (TPN-1).

### T5.10 S14 text from the re-sim
- 09 S14 *DM Note — how it plays* (09:1892) rewritten as table advice per dial (no rates; the first draft's "one fight in ten" tripped `sim_jargon` and was reworded). *Budget*: "hard, close, and dangerous, because a Focused Attendant can kill". *Adjusting the Encounter* (09:2016): One character (no second-turn attack; outs first); Four 229; Five 260, full Multiattack, DC 19; Four at 3rd 210, DC 17; Four at 5th the five line; hit hard "30 more Hit Points, on top of whichever line above fits the table (208 for three characters, 259 for four)". Idle-grind XP unchanged.

### T5.11 Vell's immunities
- 10 Master Vell: Immunities now Charmed, Frightened, Grappled, Incapacitated, Paralyzed, Restrained, Stunned, Unconscious (TPN-8e). *Beyond Reach* already points to them. *Hold Person* at the Crossing can't land, so it can't open ⟨The child is taken⟩.

### Checks (from `M/` unless noted)
- `lint_5e.py --check` OK 0; `fact_check.py --check` OK 0; `bestiary_check.py` 28 blocks + 1 variant, 0 mismatches; `pregen_check.py` 0 issues; `pytest tools -q` **450 passed** (443 before). Repo root: `pytest research/oraga_5e_sim -q` **24 passed**. `software/`: `test_docs_consistency.py` + `test_no_private_canon.py` **42 passed**.
- Swept 01–04, 11 and README (the other worker's files) for the Attendant's old DC 19, "no Help", "does not die" and "never kills": no hits.
- No commit or staging. T5.12 (commit) left open.

## 2026-10-25 — Polish review A (01–04, 06, 07, 11, README, F/) and owner rulings TP47–TP55

Read first: REVIEW_oraga_polish_A (all), REVIEW_oraga_polish_B (P10, the only finding in these files), DECISIONS TP1–TP55 and TPN notes, TASKS SA and T7.2/T7.9/T7.11. Another worker had 05, 08, 09, 10 at the same time. Planner calls: **TPN-40 (a–l)**. INVENTIONS **#98**.

### What changed
- **Owner rulings applied:** TP47 (Root a trap, not a refuge: 04 Undercurrent A *At midnight*; F/04, F/05, F/08), TP48 (Undercurrent C "(if you have time)": 01 prep box, 04 box and heading), TP49 + TP53 (Veier behind her own shut door, voice only; B9's *Veier's rooms* bullet and the Agenda 4 aside cut; two finds; pack story to a B10 note and 07/F/07 Anha; 04 Undercurrent C and *Inside*; 07/F/07 Veier; flow `b9`), TP50 (Maiven's gift in 07 and F/07; 03:119 stands), TP51 (Agenda 6's darker seam cut, 02 and F/03), TP52 (Raunu's line cut in 04 summons, 04 door scene "kept" seam, 07 *What Raunu Knows*, F/04), TP54 (04 B8: Orthaen Gift in place of Thieves' Tools, same DC; no other pointer in my files names the lock), TP55 (04 B7 and Undercurrent A sparks, Movement II *Agenda beats*, DC 18 → 15 to improvise; 07 Anha and Corval; F/04, F/07 lore only; flow `uc-a`).
- **Review A:** TP21 Second Clause (07, F/05, F/07), TP19 Vell's sword (07, F/07), safety note (01, F/01), "no fight to the death" (01), TP41 (02, F/02), "on Vell's arm" (01, 02, 07, F/02, F/07), summons at three (04), nursery-sale pointer (04 Undercurrent C and Movement V Circle), Midnight Tracker in 01's prep box and print list, prep-box section list (P2), dinner-era leftovers (P3), dial pointer and one-line dial (S13), "both rivers" DM note (T7.10), duplicated TP32/TP37 sentences (04 second sites point back), "factor" DM note retitled (07, F/07), map pointer form (04, and `test_maps` regex updated to accept "and map VIII–n"), P9 voice items, P10 xrefs (03, 11), P12, P13, P15 (02, 06), S10 (01). Review B P10: Table I–3 gains an End row.
- **Guards** (appended to `facts.yaml`): `tp47_root_trap`, `tp21_second_clause`, `tp19_vell_sword`, `tp52_raunu_line`, `tp48_undercurrent_c`, `tp53_veier_room`; 19 tests in `TestPolishRulings`.
- **Tasks:** T7.2, T7.9, T7.10 ☑. T7.11 stays open (the 05/09 captain reword is not in yet); T7.16 stays open (the 05 gate beat).

### Skipped / OWNER
- P14 (the writing law's second exception): OWNER. P15's 07:493 Maiven "dies there": waits on T7.20. P7 (Table VIII–6): 08, other worker.

### Left for the 05/08/09/10 worker
- TP53: 08:221 "its three finds"; 09:446 and 09:1543 send Maiven the pack as a B9 find (now Anha's story; the two slings still work). TP54: 09 S8 names the crystal lock (09:1296). TP50: the Maiven block in 10 may note her gift. P6: S7's title. T7.11's captain reword in 05/09; T7.16's 05 gate beat.

### Checks (from `M/` unless noted)
- `lint_5e.py --check` OK 0 (first run: six new long paragraphs and a not…but tic, split or reworded); `fact_check.py --check` OK 0 (first run caught two 04 edits that an aborted batch had not applied; redone); `pregen_check.py` 0 issues; `bestiary_check.py` 0 mismatches; `pytest tools -q` **481 passed** (first run: three `test_maps` failures from the new map-pointer form; regex updated). Flow page rebuilt. `software/`: `test_docs_consistency.py` + `test_no_private_canon.py` **42 passed**.
- No commit or staging.

## 2026-10-25 — Polish review B (05, 08, 09, 10), with T2.6, T6.6, T7.11, T7.16 (05/09 halves)

Read first: REVIEW_oraga_polish_B (main list) and _A (findings in 05/08/09/10), DECISIONS TP1–TP55, TPN-1–TPN-20, TASKS SA and T2.6/T6.6/T7.2/T7.11/T7.16, this LOG's tail. Only 05, 08, 09, 10, facts.yaml (append), tools tests, the lint allowlist, INVENTIONS and docs were edited; 01–04, 06, 07, 11 and F/ belong to the concurrent worker. Calls: **TPN-30 – TPN-37**. INVENTIONS **#99**.

### Rules
- **TP47 Root (B1):** 05 principle 2 (shelter because errands don't go there; TP18 line; the Attendant unaffected; pointer to the trap), 08 Wards line, 10 "What changes the night". Guard `root_trap` (sentence check, 05/08/09/10) fires on HEAD's 05, 08, 10 text; 0 now.
- **T6.6 (B3):** 05 crowd rule scoped to the set-aside (Uninvited, Idle Attendant); "Nobody is out for longer than two rounds" cut; new *Everyone else's steel* (Sharp / Gentle / Merciless; detains exception; fire the exception) and the say-it line; Two Hundred People bullet and 09 "After midnight" and 10's two mercies are pointers; S13 and 05 General Features "a creature the fire drops". Guard `crowd_rule_scope` (5 hits on HEAD, 0 now). TPN-35.
- **B4 Radiant beats (TPN-30), B5 faked cry (TPN-31; guard `wept_freeze`), S1 cap (TPN-32), S4 deny the congregation (TPN-33), S18 Attendant second turn clarified to match `s14.py` (TPN-34).**
- S2, S3 (08 Buying Time line: nature, spells, slowing, cap), S5–S9, S13 (2014 box re-derived), S14, S15, S16, S17, S19, S21; P1–P9, P11–P15.
- **T2.6 tracker (S11):** Table VIII–10 rows for turns lost to Delay this scene, Delay earned this scene by whom (third = threat), threats this scene, End tries; arrival cells carry the Delay beats. T6.7's live-card row and the void Last Rite box left out.
- **TP21 / T7.11:** the clause ends at "hold her" (05); captain reword in 05 and 09 S3; guard `second_clause` (05/08/09/10). **T7.16:** 05 gate beat (Vell looks back; pointer to 07). **TP19:** 10 Vell "sword still on his back". **TP50:** 05 Thenya line and 10 Maiven *Thenya Gift* trait (feat wording only; bestiary_check 0). **TP53:** 09 Thenya proof (pack = Anha's story; slings in Raunu's rooms); 08 map caption "its rooms". **TP54:** 08 Table VIII–3 and Page Two, 09 S8 lock bullet. **TP55:** 08 Root key improvised at DC 15. 10:33 "to the death" line cut.

### Skipped / owner
- S12 (WP6: T6.2, T6.5, T6.7). S20 (OWNER, T8.4). A-P6 S7's title stands (TPN-37c). 07:493 waits on T7.20.

### Checks (from `M/` unless noted)
- First runs: three bare DCs (ward-steering rewritten; one 08 allowlist entry for the spells compression; 09 lock line names the check), the Deadly allowlist anchor updated for the new 2014 numbers, two long paragraphs split (05 Corval, *Everyone else's steel*), one S13 rule-copy hit (rephrased), a YAML double-quote `\b` bug in my own guard (fixed, then confirmed firing on HEAD text).
- Final: `lint_5e.py --check` OK 0; `fact_check.py --check` OK 0; `bestiary_check.py` 0 mismatches; `pregen_check.py` 0 issues; `pytest tools -q` **481 passed** (450 before; 12 new in `TestPolishReviewB`, the rest the other worker's). Repo root `pytest research/oraga_5e_sim -q` 24 passed. `software/` docs-consistency + private-canon 42 passed. flow.json not touched by this pass.
- Tasks marked ☑: T2.6, T6.6, T7.11, T7.16. Review files marked per finding. No commit or staging.

## 2026-10-25 — TP56, the quiet rooms ("The Rest of the Palace")

Read first: DECISIONS TP56 (*Palace brief and the quiet rooms*), the visual brief §0.1, §1.2–§1.7, *The rooms the brief adds* and B4–B10 entries; 04 *The Private Palace*, Undercurrent C, Movement IV omen, *What the Bought do*; 05 B12 contract; 02 Agenda 6 and 8. INVENTIONS **#100**. (A first attempt was interrupted before any edit reached disk; this is the full redo.)

### Done
- **M/04:** new `#### The Rest of the Palace` (04:440) at the end of *The Private Palace*, after B13 and its B12 note, before *Running the Room*. Italic DM-note opener (shut since the cut to 22; where wanderers end up; nothing worth staying for; don't steer; one detail each), then nine run-in entries in TP56's order and one *Everything else* line for the no-detail rooms. Unnumbered: no B-areas added, so the B0–B13 key, maps and flow are untouched. Locations from the brief's §1.4 placements (servants' hall and laundry beside/near B10; state rooms beyond B4 and B6; dark wing on the way to B8; drawing rooms beside B7; bell tower at the Court's north-east corner; stable yard off the West Lane). Cords and tokens carry no writing. The bell tower points to chapter V, area B12 (the contract lives inside B12; there is no "The Contract" heading). The dark-wing door cites the printed Movement V lamplight (card S8).
- **Undercurrent C spark (04:833):** "or finds them in the East Range laundry".
- **F/04:** same section (275), lore only, words for numbers, "Chapter V, B12"; the dark-wing entry omits the lamplight (F/ doesn't print it). Same laundry clause in F's Undercurrent C spark.
- **Visual brief:** §0.1 gains the **[APPROVED TP56]** tag line; *The rooms the brief adds* heading re-tagged, each TP56 room tagged with its **Detail:** line (cords and tokens marked "no writing"); no-detail rooms tagged "no detail"; the gallery corridor stays [VX] (not in TP56); roofscape approved as a place, materials still VX. §1.4 rows for the bell tower, West Range rooms, garden wing, mews, stable yard and East Range re-tagged APPROVED TP56. §7 gets one note that TP56 settled those placements, sizes and decor still proposals. "Never visited in play" (stable yard) became "Rarely".
- **Guard:** facts.yaml `tp56_quiet_rooms` (section before *Running the Room* in both editions; the laundry clause; a sentence forbid on writing on the rota cords or carters' tokens in 04). `TestTP56QuietRooms`, 8 tests.
- flow.json: no node added (non-story rooms; the DM is told not to steer there).

### Checks (from `M/` unless noted)
- `lint_5e.py --check` OK 0; `fact_check.py --check` OK 0; `pregen_check.py` 0 issues; `bestiary_check.py` 0 mismatches; `pytest tools -q` **489 passed** (481 + 8). `software/`: `test_docs_consistency.py` + `test_no_private_canon.py` **42 passed**.
- No commit or staging. M/art/ and references/house_raunu.jpeg untouched.
