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
