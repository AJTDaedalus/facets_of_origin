# TASKS: Oraga Night 5e, review-fix pass

*Planner output, 2026-10-08. Read `docs/DESIGN_oraga_5e_review_fixes.md` first, then
`docs/DESIGN_oraga_5e_official.md` §2–§3 and `M/STYLE_5e.md`. Finding IDs (P1-n, P2-n,
P3-n) refer to `docs/REVIEW_oraga_5e_official_critical.md`, which has the line numbers, quotes
and proposed fixes. Locate everything by quote, because line numbers drift.*

`M/` = `conversions/dnd5e/oraga_night/`. `T/` = `M/tools/`.

**SA (standard acceptance) for every task that edits `M/`:**
1. `python T/lint_5e.py --check`
2. `python T/fact_check.py --check` (from R0 onward; plain `fact_check.py` lists every remaining hit)
3. `python T/bestiary_check.py` and `python T/pregen_check.py`
4. `python -m pytest T -q`
5. Rebuild the flow page if `flow.json` changed.
6. Add an INVENTIONS row for any new derived content, and an O-entry in DECISIONS for any Planner call.
7. Mark the task ☑ here and log it.

Commit once per phase, staging specific files. Push only at R6, after the private-canon guard
(`software/tests/test_no_private_canon.py`) passes and the unpushed range has been scanned.

**Status key:** ☐ open · ☑ done · ⛔ GATED(QRn), waiting on an owner ruling (DESIGN §4).

---

## R0: Tooling that sees continuity (TDD)

### ☑ R0.1 `facts.yaml` and `fact_check.py`
- **Do:**
  - Write `T/test_fact_check.py` first, with fixtures for each kind of contradiction: a count, a
    floor, a Movement and a size.
  - Then write `M/facts.yaml` covering the household, the guards (count, and positions per
    Movement), retinues, the Bought company, arrival Movements (the Attendant, the Uninvited,
    Vell, the Bought), elevations and floors (B2, B8, B9, the terraces, the gate), the stairs,
    and the O28 sizes.
  - Then write `T/fact_check.py`: it unwraps paragraphs, finds each fact's phrasings, and flags
    contradicting forms with context.
- **Accept:**
  - Tests green; at least 3 per check type.
  - The first run on the current text reports at least: the household (P1-1), the nine guards
    (P1-2), "forty blades" (P2-6), the Attendant's arrival (P1-4), the east wing's floor
    (P1-5), "Kovaun brought three" (P1-7), and Maiven alive in 06 (P2-5).
  - Paste that list into the LOG. It is the R2 worklist.
- **Time:** 3 × 30 min.

### ☑ R0.2 Linter upgrades
- **Do** (test-first, at least 3 tests per new rule):
  - unwrap paragraphs before the regex rules (fixes the wrapped-DC blind spot);
  - make the allowlist rule-scoped (`file|rule|text|reason`) and migrate the existing entries;
  - add the new rule families listed in DESIGN §2: emphasis italics, "(X or Y)" skills, HTML
    comments, repo file names, simulation jargon, wider conversion talk, trigger-line format,
    box-label format, anachronisms;
  - add the defined-terms check against `T/terms.txt`. Seed that file from canon glossaries
    (Orthaen, Thenya, Phern, Boranis, Draunel, Rekuzan, Val'loh, the Uninvited, Scora, Kshalo,
    Mazaa, the Blackwatch…), each with where it is defined.
- **Accept:**
  - Tests green.
  - Run `--report` and log the new hit counts per family; they are the R3/R5 worklists.
  - Re-baseline, so that `--check` passes while the hits are worked down, and log the new
    baseline.
- **Time:** 3 × 30 min.

### ☑ R0.3 Commit R0
- **Do:** commit "Oraga 5e review-fix pass: R0 continuity bible, fact checker, linter upgrades".

---

## R1: Rules and exploits

### ☑ R1.1 S14 argue-out (P1-3, P2-15, P2-16; O32)
- **Files:** 09 S14 (Outs, the hint list, Rewards); 10 Attendant (Tells/Breaks); 05 (the
  Attendant bullets); 07 (the Attendant); 08 (DM sheet lines).
- **Accept:** arguing is a distraction everywhere. The Idle "furniture" rule is stated once
  (in 10) and pointed to from the rest. The Rewards line lists three triggers. Hint 5 obeys the
  Focus rule. The out-slug claim is gone.

### ☑ R1.2 "Down, Not Out" in one home (P2-18; O36)
- **Files:** 05 (canonical); 08, 09 (two copies) and 10 become pointers plus local rules only.
- **Accept:** the fact checker's "rule-copy" entry finds no full restatement outside 05.
  S13 says "the round after".

### ☑ R1.3 Grapple, S3 ending, S4 out, the Bought route, the tracker trigger, the bell default (P2-14, P2-17, P2-10, P2-11, P2-12; O37, O40)
- **Files:** 05 Table V–5, the B12 and branch text; 09 S3, S4 and the tracker; 08 Table VIII–5.
- **Accept:** each item resolved as in O40/O37. The decisions are logged.

### ☑ R1.4 Nastier as baseline (P1-7) (QR3: four)
- **Do:**
  - If the retinues become four: change INVENTIONS #1, 09:170, and 10's flavor lines.
  - In both cases, promote the used variants to named blocks (*Veteran Bought Sergeant* CR 4;
    *Cousin of 3160* CR 1, or the owner's names) or fold them into the base blocks.
  - Fix Table X–1 (S3's sergeant CR).
  - Give each affected card (S3, S6, S7, S8, S9) a real Nastier dial again.
- **Accept:**
  - `bestiary_check` covers the new blocks (extended test-first).
  - The fact checker agrees on the retinue sizes.
  - Every card's budget re-derives.

### ☑ R1.5 Commit R1

---

## R2: Continuity

### ☑ R2.1 Household (P1-1) (QR1: 60, 22 stayed)
- **Files:** 02:70 and 02:422; 04:38–39, 04:408 and 04:705–710; 07:196 and 07:225–229; 08
  (rumors and the truth note); `flow.json`; `facts.yaml`.
- **Accept:** the fact checker finds no household contradiction.

### ☑ R2.2 Honor-guard deployment (P1-2) (QR2: two of the nine)
- **Do:**
  - Add one deployment table to chapter VIII: where each of the nine stands, Movements I–V and
    midnight, plus the east-wing guard (per QR2).
  - Fix 04:83, 04:98–99 ("the two nearest"), 04:169–170, 04:305, 04:344 and 04:1347; 05:149,
    05:268, 05:336, 05:461 and 05:817; 08:43; 10:421.
- **Accept:** the fact checker's guard entries agree with the table.

### ☑ R2.3 The east wing's floor, stairs and terraces (P1-5; O33, O34)
- **Files:** 05 General Features (add an *Elevations* bullet), 05:142–150; 04 B2, B8, B9 and
  04:1391; 09 S9's box, 09:1355, and S10; 08's caption; `facts.yaml`.
- **Accept:** the fact checker's floor and stair entries agree everywhere. "Two terraces below"
  appears 0 times.

### ☑ R2.4 Arrival timing (P1-4; O35)
- **Files:** 01:62–64; 05 Table V–6 (the Hollow rows); `facts.yaml`.
- **Accept:** the fact checker's arrival entries agree.

### ☑ R2.5 Smaller continuity fixes (P2-5, P2-7, P2-8, P2-9; P3-7, P3-8, P3-11, P3-12, P3-16, P3-18)
- **Do:**
  - P2-5: Maiven's aftermath line becomes conditional.
  - P2-7: "before the boat clears" replaces "before midnight" for Vell, everywhere.
  - P2-8: gloss Scora ("the record-keepers attached to great houses") and Kshalo ("the eastern
    river country's people of dream and sleep-herbs") at first mention, from
    `settings/valloh/V3` and `V1`.
  - P2-9: "It is not long dark"; one size for B4, chosen by the majority of passages.
  - P3-7: Intimidation wording.
  - P3-8: the Wept's Fracture condition matches 05.
  - P3-11: Vell's blade is one weapon (the majority form).
  - P3-12: Tavva's crew count.
  - P3-16: "(the patron's pitch)" note.
  - P3-18: Second Clause gloss.
- **Accept:** the defined-terms check passes for Scora and Kshalo. Each item is fixed.

### ☑ R2.6 "Forty blades" (P2-6) (QR4: twenty)
- **Files:** 05:1173 and 05:1178. Log a Facets-edition follow-up in CARRYOVER §6.

### ☑ R2.7 Commit R2

---

## R3: Scaffolding and conversion artefacts

### ☑ R3.1 Simulation data (P2-1) (QR6: table advice)
- **Do (if approved):** move S14's table and every "one fight in N" or "in simulation" line to
  `research/oraga_5e_simulation_notes.md`. Replace each with table advice ("Expect one character
  to drop"). Budget lines keep their label, plus a plain-play clause.
- **Accept:** the simulation-jargon rule is at 0.

### ☑ R3.2 File names, the HTML comment, conversion talk, README claims, stale ledger (P2-2, P2-3, P2-4, P2-13, P3-24)
- **Do:**
  - Delete the file-name parentheticals (04:22–23).
  - Delete the INVENTIONS #11 comment (09:268); the ledger keeps the record.
  - Cut 03's Facets-edition sidebar.
  - Rewrite the README's opening sentence to drop conversion framing.
  - Drop *Inventions* from 01's prep box.
  - Correct the README's licensing claims as the review words them.
  - Mark INVENTIONS #18 and #38 superseded.
- **Accept:** the HTML-comment, file-name and conversion-talk rules are at 0 in body text.

### ☑ R3.3 "At a 2014 table" glossary box (P2-19)
- **Do:** add one boxed list in chapter X covering Emanation, Utilize, the Magic action,
  Bloodied, Study, Influence, the condition-line format and the 2014 encounter multiplier. Soften
  README:16–17 and 10:52–54.

### ☑ R3.4 Commit R3

---

## R4: Maps

### ☑ R4.1 Keyed maps (P1-6) (QR5: option a)
- **Option (a), I draw the maps:**
  - Write `M/maps/build_maps.py` to generate original SVG maps from `facts.yaml`. Use the O28
    sizes and the O33/O34 geometry, a 5-foot grid option, room codes, a scale bar, and styling
    that is legible in print and on screen.
  - Five maps:
    - B1/B12, the gate: wicket, gate-walk, arch;
    - B2/B3, the Court and galleries: dais, rails, east doors, stair;
    - B5, the terraces to the river gate;
    - B9 with B10's service run;
    - a whole-palace overview.
  - Embed them in 08, replacing the ASCII figure, and point to them from each card's Terrain line.
  - Accept: the maps build; every card's terrain feature appears on a map; the fact checker
    agrees with the map dimensions; and the owner reviews a render.
- **Option (b), relabel only:** retitle 08's figure "Flowchart of the palace" and note "maps to
  come".
- **Time:** (a) 4 × 30 min. (b) 10 min.

### ☑ R4.2 Commit R4

---

## R5: Layout and voice

### ☑ R5.1 One trigger-line format and one box-label format (P2-20, P2-21; P3-5, P3-6)
- **Do:** apply the format STYLE declares across 04, 05 and 09 (the bold-italic card triggers).
  Use heading-style box labels everywhere. Italicize Raunu's rite box. Fix the "*If you have
  time*" styling.
- **Accept:** the trigger-format and box-label rules are at 0.

### ☑ R5.2 Dossier dedupe (P2-22; O38)
- **Do:** chapter IX's Six Lines keep only the threat line plus "see chapter VII". Chapter X's
  lore tails shrink. Collapse the repeated "fight aimed at the noble-minded" passage to one home.
- **Accept:** a near-duplicate paragraph check (a new linter soft rule, or a one-off script)
  finds no paragraph pair over 80% similar across chapters.

### ☑ R5.3 Tic line-edit, pilot then calibrate (P2-23, P2-24; O39)
- **Do:**
  - Add a `tics` soft metric to the linter with targets: "exactly" ≤ 15, "the whole" ≤ 15,
    "quietly" ≤ 10, "out loud" ≤ 8, "genuinely" ≤ 4, "Say so" ≤ 5, the "permanent confusion"
    phrase once, and "not X… but Y" ≤ 8.
  - Pilot on 04, then do the rest of the book. Vary the DM Note forms (O39), rejoin the
    over-split sentences the review cites, and remove emphasis italics (the italicized "*Heroic
    Inspiration*" becomes roman).
- **Accept:** the tic targets and the emphasis rule are at 0, and the sample pairs are logged.

### ☑ R5.4 Remaining P3s (P3-1 to P3-4, P3-9, P3-10, P3-13 to P3-15, P3-17, P3-19 to P3-23)
- **Do:** each fix as the review words it.
  - P3-9: the three seal items. Add one clarifying line distinguishing them; don't rename canon
    items.
  - P3-14: Mage Armor's duration.
  - P3-15: the Hide rule and the 15-foot drop.
  - P3-17: the anachronisms.

### ☑ R5.5 Commit R5

---

## R6: Verification and push

### ☐ R6.1 Copyright phrasing check
- **Do:**
  - Re-extract the official modules from `/mnt/e/books/DandD 5E/` with PyMuPDF (into the
    scratchpad, never the repo).
  - Run an n-gram overlap scan: 8-word shingles of every module sentence against the extracts.
  - Review every hit, and rewrite any sentence that isn't stock SRD rules grammar.
- **Accept:** the overlap report is logged, and there are 0 non-SRD hits.

### ☐ R6.2 Fresh critical re-review
- **Do:** run one adversarial reviewer with the same brief as the 2026-10-06 review. Target:
  ≥ 9/10, 0 P1.
- **Accept:** the report is in `docs/REVIEW_oraga_5e_official_critical_2.md`. Any new P1 is fixed
  before the push.

### ☐ R6.3 Push
- **Do:** run the private-canon guard and scan the unpushed range (memory rule; no Windows user
  paths), then `git push origin feat/lean-facets`.

---

## Summary

| Phase | Tasks | Open now | Gated |
|---|---|---|---|
| R0 Tooling | 3 | 3 | — |
| R1 Rules | 5 | 4 | R1.4 (QR3) |
| R2 Continuity | 7 | 4 | R2.1 (QR1), R2.2 (QR2), R2.6 (QR4) |
| R3 Artefacts | 4 | 3 | R3.1 (QR6) |
| R4 Maps | 2 | 1 | R4.1 (QR5) |
| R5 Layout and voice | 5 | 5 | — |
| R6 Verify and push | 3 | 3 | — |

QR7 (whether "Shout" and "Make noise to lose" pay XP) is folded into R1.3: if the owner says no
XP, mark those two outs "(no XP)" as well.

**2026-10-08:** all QR rulings are answered (DESIGN §4), so every task is open. QR7 = no XP for "Shout" and "Make enough noise to lose" (do it in R1.3).
