# TASKS: Oraga Night 5e, full 2014 conversion

Design: `DESIGN_oraga_5e_2014.md`. Paths are relative to `conversions/dnd5e/oraga_night/` unless noted.
Checks (run from M/): `python tools/lint_5e.py --check`, `python tools/fact_check.py --check`, `python -m pytest tools -q`; from `software/`: `python -m pytest tests/test_docs_consistency.py tests/test_no_private_canon.py -q`.
Status keys: [ ] open · [~] in progress · [x] done · [!] blocked. Blocked on rulings R1–R4 is marked per task.

## P0. Setup and tools (TDD)
- [x] T0.1 Create branch `feat/oraga-5e-2014`; local tag `oraga-5e-2024` at HEAD (never push it). Accept: `git tag -l` shows it; branch checked out.
- [x] T0.2 `lint_5e.py`: 2014 rule set (casing per R1; 2024-term ban list). Tests first in `test_lint_5e.py`. Accept: new tests red then green; lint over the *unconverted* text reports the expected 2024 terms.
- [x] T0.3 `bestiary_check.py`: 2014 block parser and 2014 CR→XP. Tests first with a 2014 fixture block. Accept: fixture passes; current ch X fails only on layout.
- [→T4.1] T0.4 `pregen_check.py`: 2014 tables and SRD 5.1 human; gift as bonus feat. Tests first.
- [→P6] T0.5 `build_print.py`: SRD 5.1 notice constant, 2014 spell lines; update its tests.
- [x] T0.6 `copyright_scan.py`: run config with the 2014 books as refs (local paths, not committed) and SRD 5.1 as srd. Accept: a clean scan of the current text is recorded in LOG.

## P1. Stat blocks (ch X)
- [x] T1.1 Convert all 29 blocks to the 2014 layout and wording. Accept: `bestiary_check` green; no 2024 terms in 10_Bestiary.md.
- [x] T1.2 Rewrite the "At a 2014 table" box, as an "At a 2024 table" box per R3, or remove it.
- [x] T1.3 Table X–2 → 2014 CR/XP/PB table (SRD 5.1 has it).

## P2. Encounter rebalance (ch IX, V and party-size numbers)
- [x] T2.1 Running the Snakes: four-character baseline; 2014 method stated in prose; remove Table IX–1's SRD 5.2.1 budgets.
- [x] T2.2 Per card S1–S14: new four-character roster at the target band; adjusted XP printed; adjusting lines (One, Three, Five, 4@3rd, 4@5th, Nastier) each with a total. Work order: S14, S3, S4, S13, S9, S10, then the rest. Accept: every card's printed XP and band re-derive from ch X; Xanathar's sanity check noted in LOG per card.
- [x] T2.3 Chapter V "Adjusting the Attack": four is now the baseline (Wept 3rd turn, lump 30); add a "Three characters" line.
- [x] T2.4 The 38 party-size numbers outside the cards (encounter research §4) move to four-character values. Accept: fact_check guards updated and green.

## P3. Character rules (ch I, III, README)
- [ ] T3.1 Chapter III build rules: SRD 5.1 human, Customizing a Background, gift as bonus feat, ungifted take no feat; drop the Magic Initiate and variant human pointers.
- [x] T3.2 (done in P2) Chapter I "Three at the Table" → "Four at the Table" (deal four pregens; who, and which agendas face up).

## P4. Pregens (ch XI)
- [ ] T4.1 Rebuild Serane, Pello, Andra, Dassa and Ilesse by SRD 5.1 (scores, features, spells, gear). Accept: `pregen_check` green.
- [ ] T4.2 Re-check the "plays X" lines on S-cards against the rebuilt pregens; adjust the lines, not the rosters, unless a fight flips band.

## P5. Terms sweep (ch I–VIII, X)
- [ ] T5.1 Heroic Inspiration → Inspiration (45 lines); Bloodied (26); actions; Emanation; condition wording; 2024 spell texts in 08 handouts and cards. Accept: lint reports zero 2024 terms.
- [ ] T5.2 Styling per R1.

## P6. Licence
- [ ] T6.1 SRD 5.1 attribution at every former SRD 5.2.1 site and in `build_print.SRD_NOTE`; README "Rules" line. Accept: grep finds no "5.2.1" outside DECISIONS and history notes.

## P7. Ledger and close
- [ ] T7.1 DECISIONS entry (2014 conversion, rulings R1–R4), INVENTIONS rows for any new numbers, facts.yaml guards, `docs/LOG_oraga_5e_2014.md`.
- [ ] T7.2 Full checks green; rebuild print packets if `build_print` output is tracked; update memory.
