# AUDIT — Oraga Night 5e against Official 5e Modules

*2026-09-30. Scope: `conversions/dnd5e/oraga_night/` (5e only). The Facets d20 edition
is out of scope for now, but every finding marked `[d20-portable]` should be carried to it
later. Consolidated from six slice audits in `docs/audit_oraga_5e_official/`. Process
record: `docs/LOG_oraga_5e_official_audit.md`.*

**Yardstick.**
- `docs/RESEARCH_5e_module_conventions_structure.md`: checklist C-S1–52.
- `docs/RESEARCH_5e_module_conventions_voice.md`: checklist C-V1–26 and grep smells S1–S40.
- Both were distilled from 18 official adventures, listed in `docs/RESEARCH_5e_reference_catalog.md`.

**Basis.** Four 4th-level characters, ending the night at 5th (FIXPLAN §6). SRD 5.2.1 terms,
with 2014 compatibility claimed.

## 1. Verdict

| Dimension | Verdict |
|---|---|
| **Mechanics: arithmetic** | **Clean.** Scripts re-derived every number in the 25 stat blocks, the 5 Nastier variants and the 5 pregens. There are no arithmetic errors, and every subclass and feat is SRD. DCs (10/13/15/18, plus a deliberate 25) fit the 4th-level ladder. XP sums are correct against 5.2.1 budgets. |
| **Mechanics: rules logic** | **Five P1 contradictions or holes** (§2). Several triggers never fire, several checks have no result, and the "runs unchanged at a 2014 table" claim doesn't hold: under 2014 multipliers every multi-foe card reads one or two bands harder (S3, S13 and S14 come out Deadly). |
| **Content** | **Strong spine.** The faction lines match official council and cult presentation. Every "always" front-matter block exists. Gaps: no Adventure Background, 11 talkable NPCs with no "what they know" list, two scenes with nothing written for them to run from (the Agenda 4 dinner and the Attendant's answers), and spoilers in player-facing chapters. |
| **Styling** | **Off-standard in consistent ways.** The format legend comes late and is contradicted (italics are used for both read-aloud and MM notes). 2014 and 5.2.1 capitalization and stat-block layout are mixed. Many DCs are written bare. Some read-aloud boxes sit above their headers, and handouts are filed mid-book. |
| **Prose** | **Readable but not yet official.** "The characters" is almost never used ("player character" appears 74× in 09, and "the players" stands in for the party). The book slips into conversion talk and speaks about itself ("the module would prefer…"). Sentences run long in 04 (25-word mean) and 05 (20.9), against an official 16–19. There are about 560 em dashes and a cluster of AI-rhythm turns. 09's rhythm (15.2) is already in band. |

**Counts.** 152 findings: 8 P1, 75 P2, 69 P3. 67 are tagged `[d20-portable]`.

| Slice | File(s) | Total | P1 | P2 | P3 | d20 |
|---|---|---|---|---|---|---|
| FRONT (+ architecture) | README, 01, 02, 03, 06 | 23 | 2 | 9 | 12 | 9 |
| BALL | 04 | 26 | 2 | 14 | 10 | 16 |
| NIGHT | 05 | 24 | 2 | 16 | 6 | 9 |
| SNAKES | 09 | 28 | 0 | 13 | 15 | 8 |
| BESTIARY | 10 | 24 | 1 | 10 | 13 | 4 |
| CAST | 07, 08, 11 | 27 | 1 | 13 | 13 | 21 |

## 2. P1 findings (break play)

| ID | Problem | Fix owner |
|---|---|---|
| **NIGHT-1 + BALL-2** | The Attendant has contradictory rules. Two Focus triggers (FIXPLAN §5 against §5b) exist, and "gone until the Unmasking" conflicts with "one habit per Movement", which card S14's +2 depends on. | Planner. Recommend §5b, and vanishing for the rest of the Movement only |
| **NIGHT-2** | A dropped (Leashed) Uninvited returns "within 60 ft of its quarry", so it can leap past Vell or sealed doors and break the Crossing. | Planner. Return it where it dropped (05 plus 3 blocks) |
| **BESTIARY-1** | Detain mercy (Unconscious and Stable) contradicts the Bought Blade's *To the Terms* (1 HP and Grappled). | Planner. Pick one |
| **BALL-1** | The Agenda 4 character has no written way through the east-wing doors, and the not-optional dinner for two is two sentences long. Chapter V depends on it. | **Owner ruling Q6** |
| **CAST-1** | The Attendant must answer any direct question truthfully, and none of its answers are written. The first obvious questions land on *What the Module Never Says*. | **Owner ruling Q5** |
| **FRONT-1** | Player-facing Chapter III carries MM-only "At midnight" lines, including the Vell reveal. | **Owner ruling Q2** (banner or move) |
| **FRONT-2** | Chapters III and XI send players to the MM-only bestiary for the crystal-charge rules. | Fixer. A player-safe charge handout |

## 3. Cross-cutting themes (fix once, module-wide)

These recur in three or more slices. Fix each with one sweep, not per chapter.

1. **Edition vocabulary** (FRONT-10, BALL-15, NIGHT-12, SNAKES-8/17, BESTIARY-5/16, CAST-13). Pick **5.2.1 capitals** (Unconscious, Advantage, Hit Points). The module already leans that way, and it targets 5.2.1. Put the 2014 translation in a single sidebar. Normalize the stat-block layout to 5.2.1 throughout.
2. **Check grammar** (BALL-7/18, SNAKES-14/18, BESTIARY-8/9, CAST-3/4/14, FRONT-14, NIGHT-4/22). Write every check as "DC N Ability (Skill) check". State a failure result wherever failure matters. Use the SRD save and damage template "7 (2d6)".
3. **Party naming** (NIGHT-13, SNAKES-10, BALL-20, CAST-6, BESTIARY-10). Use "the characters" by default and "you" only for the MM. Drop "player character" and "the players" wherever the fiction is meant.
4. **Italics and the format legend** (FRONT-5, BALL-5, NIGHT-10/11, CAST-17). Move the legend to the README or intro. Reserve italics and boxes for read-aloud, and turn MM notes set in italics into labeled sidebars.
5. **Conversion talk and designer voice** (FRONT-6/7, CAST-5, SNAKES-11/24, BALL-21, BESTIARY-14). Remove "the source says", "new in this edition" and "the module would prefer", plus provenance citations outside the 5e book.
6. **AI rhythm and length** (BALL-13/14, NIGHT-14, BESTIARY-15, CAST-7, FRONT-21, SNAKES-11). Light-touch per the memory rule. Split the 30+-word sentences, cut em-dash chains, and undo "not X but Y". Target a 16–19-word mean in 04 and 05.
7. **2014-table honesty** (FRONT-18, NIGHT-6, SNAKES-7). Soften the "runs unchanged" claim, add one sidebar with the 2014-multiplier bands, and remove "Deadly" from 5.2.1 budget lines.
8. **Duplicated rules text that has drifted** (FRONT-9: snake ground rules printed 3×; BESTIARY-19: the Fracture rule printed 2×; NIGHT-8: "Knives in the Dark" names two things; SNAKES-28, CAST-18). Keep one canonical home and point to it.
9. **Crystal-charge naming** (BESTIARY-7, CAST-13, FRONT-2). There are five typographic forms. Pick one and define it once, in the new player handout.
10. **Cross-reference form** (SNAKES-15, BALL-25, NIGHT-19, FRONT-22, CAST-24). Use "(see chapter X)" and make sure every named target resolves.

## 4. Fix plan (Planner to decompose into TASKS)

| WS | Work stream | Findings | Blocked by |
|---|---|---|---|
| **A** | P1 rules contradictions | NIGHT-1, BALL-2, NIGHT-2, BESTIARY-1 | none |
| **B** | Player-facing hygiene | FRONT-1, FRONT-2, CAST-8, CAST-9, BALL-4, CAST-7 (N8: MM on the sheets) | Q1, Q2 |
| **C** | Front matter and architecture: Adventure Background (draft in FRONT.md), Overview, legend, party range, rest economy, rewards recap, README grouping, handouts to an appendix | FRONT-3/4/5/9/11/16/19/20/22/23, CAST-25/26 | Q3, Q4 |
| **D** | Module-wide grammar sweep (themes 1, 2, 10). Scriptable with grep smells S1–S40 | see §3 | none |
| **E** | Encounter and rules fixes: heat 4 no-ops, the tracker, morale, surprise and detection, scaling, the Wept, Call the House cap, Kovaun CR, the Post save, the Delay-trick base DC, the midnight clock, Fracture partial success, lanterns, orrery, gate failure, the seating feud, S4 guard sync, and Phern/Draunel Nastier sync | SNAKES-1–9/20/21/23, BESTIARY-2/3/4/6/9/18/24, NIGHT-3/4/5/7/20/21, BALL-6–10/16/17/26, CAST-11/12/21/22 | Q14 (XP for outs) |
| **F** | Read-aloud and styling: box placement, missing boxes for the Crossing and Movement VII, sidebar lengths, CR-in-prose, bold first mentions, Expected Duration and Treasure lines | BALL-3/24, NIGHT-9/10/11/23/24, SNAKES-12/13/16/19/22/25, BESTIARY-12/13/17/22/23, CAST-15/16/27 | none |
| **G** | Prose voice sweep (themes 3, 5, 6) | see §3 | Q1 |
| **H** | NPC knowledge: "what they know" lists with truth notes, and rumor truth notes | CAST-2, CAST-23, BALL-11 | Q5, Q7 |
| **I** | Canon-dependent content | BALL-1, CAST-1, BESTIARY-11, NIGHT-15/16/17/18, SNAKES-9, FRONT-8/13/15, CAST-20 | Q5–Q13 |

After any edit to a stat block or pregen, re-run `conversions/dnd5e/oraga_night/tools/bestiary_check.py`
and `pregen_check.py`. Once A–I are complete, rebuild the flow page (`flow/`).

## 5. Owner rulings needed (consolidated from all slices)

Planner-level defaults (capitalization, Attendant timings, the seating feud's Movement,
the Leashed return point, the midnight clock count) are decided in §2/§3 and are not asked here.

**Book-level**
- **Q1. MM or DM?** Official 5e says "you" in instructions and "the DM" otherwise. The module uses "MM" 80×, including on the player-facing pregen sheets. Options: keep MM and define it at first use, or use DM in the 5e edition only. (FRONT R1, CAST N8)
- **Q2. The agendas in Chapter III:** an "MM Only" banner, or move the eight agendas out of the player chapter? (FRONT R6)
- **Q3. Book organization:** regroup the README into Introduction, Parts and Appendices, or fully renumber (about 420 cross-references)? (FRONT R5)
- **Q4. The signed designer's note:** keep it as a house signature, or convert it to an unsigned MM note? (FRONT R2)

**Story and canon**
- **Q5. What does the Attendant say** to the questions the module never answers ("Who is your master?")? Options: literal but useless answers; it doesn't know; it answers with its missing master; something else. And may it admit it came through *with* the three? (CAST N1, P1)
- **Q6. Agenda 4:** may the character show the grandmother's ring at the doors, with Veier sending for them? And at the dinner, may Raunu and Veier keep to Chapter VII's topics, with Raunu refusing to name the midnight announcement? (BALL N1, P1)
- **Q7. Veier:** may she confirm the pregnancy to a character she trusts, or must they find the nursery? (CAST N2)
- **Q8. Attacking Master Vell:** what does the table see? The blow always misses unseen; the attacker doesn't go through with it; he shrugs it off (which needs numbers); or something else. (BESTIARY N1)
- **Q9. Trapping an Uninvited in ward-crystal:** if the Wept is trapped, does Raunu live? If the Radiant or the Hollow is trapped, is it simply "the escape is easy"? (NIGHT N2)
- **Q10. The contract case:** the sergeant carries it (the captain alone has read it all), or the captain carries it? The recommendation keeps the box: the sergeant carries it. (NIGHT N1, which affects both editions)
- **Q11. Essin's "two bodies":** real corpses, or a figure of speech for secrets? (SNAKES N2, still open since pass 2 / INVENTIONS #13)
- **Q12. The man between the duellists in S9:** Draunel at the terrace's edge, a second, or cut the line (the canon-safe default)? (SNAKES N3)
- **Q13. Room sizes after midnight:** may the 5e edition set approximate dimensions for B2, B5 and B9, or should it say "no fixed plan; use the diagram"? (NIGHT N3)
- **Q14. XP for walk-away outs:** should leaving a scene pay the card's full XP? The recommendation is no: pay for outs that resolve a scene. (SNAKES N4)
- **Q15. Prices and values:** Callun's fee for a Movement III answer (10 gp proposed) and for the nursery; the Church's favor in Agenda 2; the Circle knife's coat. (BALL N2, FRONT R4, BESTIARY N3)
- **Q16. Pregens:** write a one-line flaw each, or leave them without? Does Ilesse's crystal count as her holy symbol? (CAST N3, N4)
- **Q17. Names:** pronunciations for the main invented names; spell out or drop "PG" in "3164 PG"; confirm the Blackwatch and Mazaa glosses taken from the Val'loh setting file. (FRONT R3, CAST N5)
- **Q18. Alignment:** print "—" on the Uninvited and Vell (per INVENTIONS #44), and tag the cast or leave it untagged (the recommendation is untagged)? (BESTIARY N2, CAST N6)
- **Q19. Initials on the agenda cards** ("— R.C.") when only the Church writes: a table convenience, or change to "delivered in person"? (CAST N7)
- **Q20. Pass-2 leftovers:** sixty or eighty servants; the testament's witnesses. (CAST N9)

## 5a. Owner rulings received (2026-09-30)

- **Q1 → DM, 5e edition only.** Replace "MM"/"Mirror Master" with "DM" throughout
  `conversions/dnd5e/oraga_night/` (and "you" in instructions per C-V). The Facets editions keep MM. This resolves FRONT-17 and CAST N8.
- **Q2 → Move the agendas out of Chapter III.** Players get the agenda cards (handouts). The MM-only
  "At midnight" lines move to a DM-facing chapter. This resolves FRONT-1 and feeds WS B/C.
- **Q5 → Remove the mechanic.** Owner: *"The attendant doesn't answer any direct question truthfully,
  that's a weird mechanic I don't like."* This is a 5e-edition invention (INVENTIONS #55), not Facets canon.
  It drops the habit "answers any direct question literally, and cannot leave one unanswered" and
  the Languages clause "answers literally and truthfully". Sites: 07:462–463, 09:1669–1670, 09:1731 (the S14
  distraction trick built on it), 10:194, 10:226–227. CAST-1 is **void**; replace it with a removal task.
  Knock-ons: the Attendant is left with two habits for the "one habit per Movement" sightings and the S14 +2.
  S14 loses one distraction option. If either needs a replacement, that is new canon and must go back to the owner.
  Don't invent one.
- **Q6 → Yes, as described.** Agenda 4 shows the grandmother's ring at the east-wing doors, and Veier sends for
  the character by default. At dinner Raunu and Veier keep to Chapter VII's topics, and Raunu refuses to name the
  midnight announcement. No other new facts. This resolves BALL-1's canon block.
- Still open: Q3, Q4, Q7–Q20.
- Added by the plan (`docs/DESIGN_oraga_5e_official.md` §7):
  - **Q21:** approve pass 2's pending redundancy cuts, trimming 04 *The Snakes in the Pen* and the 05 snakes section.
  - **Q22:** removing the habit leaves the Attendant with three habits, and Movement III has no sighting. Do you want to supply a replacement (new canon)? The default is no replacement.
- **2026-10-03:** Q21 → approved (make the redundancy cuts). Q22 → no replacement habit.
- **Q23 (found in Phase 1):** Agenda 4 and Handout 2 say the message is for Veier alone ("no husband"), but the Dinner for Two puts Raunu at the table. Can the character get a moment with her alone, and how? (Answering this is new canon.)
- Fix plan: `docs/DESIGN_oraga_5e_official.md` + `docs/TASKS_oraga_5e_official.md`.

## 6. Already at official standard (don't break)

- Box trigger clauses and most box lengths.
- Movement durations and the runtime table (it sums to 4 h 50 min).
- Losing never ends the game, and failures move the story forward.
- The *Knives in the Dark* event structure and *Down, Not Out*.
- The faction escalation tables, the heat tracker concept, and all the stat-block and pregen arithmetic.
- SRD-only subclasses and feats.
- The DC ladder.
- 09's sentence rhythm.
- The canon checks: the heir stays secret, and "House Boranis hired none".

See the "What already meets the official standard" section of each slice file for detail.
