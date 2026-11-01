# REVIEW3: Oraga 5e 2014 conversion (PR #34), final pre-merge review

Reviewer: independent final pass, 2026-11-01. PR head `66c2bec` (`origin/feat/oraga-5e-2014`), base `origin/feat/lean-facets`.
I formed this view from the module files and the rules sources (SRD 5.1, 2014 DMG pp. 82–83). I read the earlier REVIEW and REVIEW2 files only at the end, to avoid re-reporting items they had already resolved.

## Verdict

**I would approve the merge once F1 is fixed.** F2–F9 are nits and can go in the same commit or a follow-up. I found **no blockers**: no wrong budget, no illegal pregen, no 2024 rule left in rules text, no copyright problem and no hygiene problem in the diff.

**Cannot be fixed in text** (needs data or an owner ruling):
- **D1.** The S14 odds (DM Note "how it plays", `09_The_Snakes.md` ~2036–2060), the "fewer than half of tables get through 144 Hit Points" line (~2027), and the per-card "plays Easy/Medium/Hard" lines all come from simulations of the **2024** pregens (INVENTIONS #142; LOG T4.2; DECISIONS note (a)), and the per-card lines from rosters that have since changed. The 2014 pregens are weaker: Dassa makes one attack, there is no Weapon Mastery, and the cantrips do less. The printed odds are probably optimistic for slugging. Re-run the harness with the 2014 pregens and the four-player rosters, then reword. REVIEW2 U1 softened one sentence; the rest still read as measured fact.
- **D2.** Table I–1 and Table VIII–1 are still the three-player minutes (DECISIONS note (b)). This also makes `09:96–97` ("Every number in this module, on the cards and off them, is printed for four 4th-level characters") untrue as worded. Fix needs a real four-player timing. Until then, add "except the runtime minutes (Table I–1)" to that sentence.

## Tooling results (all green)

| Command | Result |
|---|---|
| `python -m pytest tools -q` | 703 passed, 1 skipped |
| `python tools/lint_5e.py --check` | OK, 0 |
| `python tools/fact_check.py --check` | OK, 0 |
| `python tools/pregen_check.py` | 5 pregens, 0 issues |
| `python tools/bestiary_check.py` | 28 blocks + 1 variant, 0 mismatches |
| `software/: pytest tests/test_docs_consistency.py tests/test_no_private_canon.py -q` | 42 passed |
| `copyright_scan.py --refs cs_refs --srd <SRD 5.1 only> --check` (my run) | (a) 80, (b) 17, **(c) 0** |

## What I verified and found correct

- **Every card budget, S1–S14, recomputed with the 2014 DMG method:** the XP sum, the multiplier by foe count (next-higher for a lone character), and the band against each party's thresholds. All 80-odd printed "N XP; adjusted M: Band" pairs are right, and so is every line of Table IX–1. The S11 Corro exclusion is legitimate under DMG p. 82. Table IX–3 agrees with every card.
- **Every card read end to end against chapter X:** read-aloud headcounts (S2 "Four people", S3, S6, S7, S8, S9, S10, S11, S12, S13), Detection Passive Perceptions (Tavva 16; knives, wardens and slingers 13), morale and *Breaks* lines, Call the House timing, the Provocation and *Seconds and Circles* clock, and the Nastier and variant pointers. All agree. S13's half-down morale, which differs from the Veteran Duelist's "first time it takes damage", is covered by the after-midnight rule at `09:136–137`.
- **Snake tracker:** the default-midnight heats (3/2/2/1/3/3) follow from the starts and the automatic boxes, and Table VIII–5 matches Table IX–2.
- **Chapter V and VIII:** lump 30/20/40, the Wept's 3rd/4th turn, the 144/120 HP tracker, potions 4/3, and "four agendas stay in the deck" all agree across 05, 08, 10 and facts.yaml.
- **Pregens:** every number re-derived (standard array, +1 human, the 4th-level ASI, HP, AC, saves, skills with expertise and Jack of All Trades, Initiative, Passive Perception, spell DC and attack, cantrip, known, prepared and spellbook counts, slots, and the 2014 class features at 4th level). All legal and correct. Backgrounds fit SRD 5.1 "Customizing a Background" (2 skills, plus 2 tools or languages).
- **Stat blocks:** the Attendant (CR 6, PB +3: saves, skills, +7, DC 15, 17d8 + 68) is right, and the checker's DMG estimate gives CR 6. Armor-derived ACs and the Sect Guard (the SRD guard) are right. The 2024 box's budget conversion (Low 1,000 · Moderate 1,500 · High 2,000 for four) matches the old SRD 5.2.1 table.
- **Spell lines** (`build_print.SPELLS`) and Serane's Bardic Inspiration, Cutting Words and Vicious Mockery match SRD 5.1. Inspiration (SRD 5.1 p. 60) and Knocking a Creature Out (melee only, so the house rule is declared) are described accurately.
- **Licence and hygiene:** the SRD 5.1 notice is in README, IX, X, XI and the print note. The diff has no secrets, no scratch paths beyond "session scratchpad" prose, no generated files, and no private canon (the guard test passes).

## Findings

### F1 (should-fix): S6 has no *One character* line, though it is the card most likely to be walked into alone
- **Where:** `09_The_Snakes.md:1157–1168` (S6 Adjusting); the list at `09:103–104`; `01_Overture.md:160–162`.
- **Problem:** the S6 invitation is explicitly one-on-one ("*just the two of you*", `09:1095`, and the Boranis line row III). The Running-the-Snakes rule sends a lone character to the card's *One character* line. S6 has none and is not in the list "(S2, S4, S7, S8, S9, S10, S13 and S14)". The Movement V DM Note doesn't cover Movement II–III either.
  - The printed roster is three Cousins of 3160 (two on the terrace, the third "behind anyone who followed"). If nobody followed, it is unclear whether the third comes at all.
  - Two cousins against one 4th-level character is 400 XP, adjusted 800 (next-higher multiplier), against a solo Deadly of 500.
  - Separately, `01:161` claims every card carries "a line for one character alone". S1, S3, S5, S6, S11 and S12 don't.
- **Fix:** add, for example: "*One character:* the two on the terrace; the third comes out only behind someone who followed, and they break the first time one is hurt (400 XP; adjusted 800 for one: Deadly on paper, and *A Quiet Word* does 3 damage). Alone, a talker or healer is offered the outs first." Add S6 to the list at `09:103–104`. Change `01:161` to "a line for one character alone where one can walk in".

### F2 (nit): capitalisation slip from the Bloodied sweep
- **Where:** `09_The_Snakes.md:918–919`, "The captain fights on only if the party blocks the search. Then, / At half his Hit Points or on his second round…".
- **Fix:** "Then, at half his Hit Points…".

### F3 (nit): the Hollow becomes "its" in the converted trait
- **Where:** `10_Bestiary.md:1175`, "While at or below half its Hit Points, the Hollow gives ground". Every other line of the block says "he".
- **Fix:** "half his Hit Points".

### F4 (nit): stale allowlist entry, and no check for unused entries
- **Where:** `tools/lint_5e_allow.txt:41`, `10_Bestiary.md|deadly_budget|S3's 850 XP becomes 1,700, past Deadly…`.
- **Problem:** the `deadly_budget` family was removed from `lint_5e.py` in this PR, and the text it whitelists no longer exists. The linter never reports unused allow entries, so dead entries pile up and could later mask a real hit if a family name is reused.
- **Fix:** delete the line. Optionally add a `--check` failure (with a test) for allow entries that match nothing.

### F5 (nit): the "five generous CRs" list is incomplete by its own yardstick
- **Where:** `09_The_Snakes.md:122–125`.
- **Evidence:** `bestiary_check.py`'s DMG estimate rates Essin Boranis −0.8 and the Phern Bodyguard −0.8 steps. That is as generous as Vorlain (−0.8) and the Cousin's Blade (−0.5), which are listed.
- **Fix:** list all seven combat blocks, or say "several CRs, among them…".

### F6 (nit): two S14 adjusting lines print no total
- **Where:** `09_The_Snakes.md`, S14 *Four at 5th level* and *A table built to hit hard*.
- **Problem:** DESIGN §2.5 says every line carries a total.
- **Fix:** "(2,300 XP; about half of Deadly for four at 5th level)"; "(XP unchanged: 2,300)".

### F7 (nit): README promises 5th level; chapter I says the party lands short of it
- **Where:** `README.md:11` "The night ends at 5th level"; `01_Overture.md:445–447` "close to 6,000 XP … a little short of 5th level (6,500) … round up".
- **Fix:** README: "The night ends at 5th level (a milestone; see chapter I)".

### F8 (nit): S2 and S7 describe different "both jobs in one run" rosters at 5th level
- **Where:** S2 *Four at 5th level* is "as for five": Tavva (Nastier) plus 4 Gallery Knives plus 1 Circle knife, 850 / 1,700. S7 *Four at 5th level* is 4 Circle knives plus Tavva and 3 Gallery Knives, 1,400 / 3,500.
- **Problem:** both describe the same merged scene.
- **Fix:** make both lines name the same merged roster, or say each card's line holds only when the party enters by that card.

### F9 (nit): the INVENTIONS ledger keeps superseded 2024 rows with no pointer forward
- **Where:** `INVENTIONS_5e.md` row 24 ("every Val'loh gift is an origin feat taken only through the Human's *Versatile* trait"), row 126 (Serane's text "follow[s] the SRD 5.2.1"), row 134 (spell lines "cut from the SRD 5.2.1"), and rows 54/106 (old rosters and Low/Moderate labels).
- **Problem:** this ledger is the owner's approval list. Rows 142 and 143 say what they supersede, but nothing supersedes #24, #126 or #134, so the owner would be reviewing claims that are no longer true.
- **Fix:** append "Superseded by #141 / #143 (2014 conversion)" to those rows, or add one row listing them.

## Hygiene caution (not in the PR, but in the working tree)
The local checkout has uncommitted `player_characters/taven_olmarin.md` and `docs/REFERENCE_oraga_palace_visual_brief.md` edits. It also has untracked `references/house_raunu.jpeg`, `references/house_raunu.jpeg:Zone.Identifier`, `art/`, and the Knight and Taven `.html`/`.md` files. None is part of PR #34. Whoever applies these fixes should `git add` only the named files, and must never stage anything under `references/`.

## Overlap with earlier reviews
None of F1–F9 was raised in REVIEW or REVIEW2. REVIEW2 U1 (the S14 odds) is only partly resolved, and I carry it as D1.

---

## Resolution (author, 2026-11-01)

Every finding is resolved, including D1 and D2, which were resolved with data and an honest text exception rather than left open.

- **F1** S6 gains a *One character* line (two cousins, 400 / 800 for one, Deadly on paper; they break early, and the outs come first). S6 is added to the list of cards a lone character can walk into. Chapter I now says a lone-character line exists "wherever one can walk in".
- **F2** "Then, at half his Hit Points".
- **F3** The Hollow's trait uses "his".
- **F4** The dead `deadly_budget` allowlist entry is removed. A report of allowlist entries that match nothing is not added; that is a tool feature beyond this PR.
- **F5** The list is now "Seven CRs read a step generous", adding Essin and the Phern Bodyguard.
- **F6** S14's 4@5th line (2,300 / 2,300, Medium) and its built-to-hit-hard line (still 2,300 XP) carry totals.
- **F7** The README says "The night ends at 5th level, by milestone."
- **F8** The S2 and S7 4@5th lines describe one merged scene: Tavva's Nastier crew and all four Circle knives, 1,450 / 3,625, Hard.
- **F9** INVENTIONS #24, #126 and #134 are marked superseded by the 2014 conversion.
- **D1** The research simulator gained a 2014 mode (smoke tests first; 38 pass): SRD 5.1 pregens, no 2024-only features, and the four-player rosters. Results are in `research/oraga_5e_sim/README.md`. They move S8's play line to Medium (Hard for a party light on damage) and S13's to Medium, since Draunel lets go the moment it is seen as his fight; Table IX–3 is updated. They confirm S2, S3, S7, S9 and S10. For S14 they confirm the note: the distraction game wins 91% with a drop in about half the fights, and slugging wins 25% with the 2014 pregens.
- **D2** Chapter IX's party-size rule now names the one exception: the runtime minutes (Tables I–1 and VIII–1) were set for three players. Chapter I already says so. A real four-player timing remains a follow-up, now stated rather than hidden.
- Caught in re-audit: S14's 4@5th band is Medium (2,300 < 3,000), not Hard. Fixed. All 84 budget pairs re-derived.

Checks: lint OK, fact_check 0, pregen_check 0, bestiary_check 0, pytest tools 703 passed / 1 skipped, simulator 38 passed, software docs+canon 42 passed.
