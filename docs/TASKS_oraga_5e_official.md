# TASKS — Oraga Night 5e: Official-Module Fix Pass

*Planner output, 2026-09-30. Read `docs/DESIGN_oraga_5e_official.md` first: the §3 style
sheet, the §2 line-drift rule, the §5 order and the §6 decisions all apply to every task.
Finding IDs refer to `docs/audit_oraga_5e_official/<SLICE>.md`. That file has the exact quoted
text and the proposed wording for each finding.*

**Paths.** `M/` = `conversions/dnd5e/oraga_night/`. `T/` = `M/tools/`.
**Chapters.** 01 Overture · 02 World · 03 Masks · 04 Ball · 05 Night · 06 Aftermath ·
07 Cast · 08 DM Sheet and Handouts · 09 Snakes · 10 Bestiary · 11 Pregens.

**Standard acceptance (SA), which every task that edits `M/` must also meet:**
1. `python T/lint_5e.py --check` exits 0. No hard rule has new hits, and no soft metric has regressed against the baseline.
2. `python T/bestiary_check.py` and `python T/pregen_check.py` exit 0.
3. No new fictional fact is introduced. Anything new that is derived from printed facts gets a row in `M/INVENTIONS_5e.md` citing its sources (the "Ledger" column below).
4. Mark the task done here, and append to `docs/LOG_oraga_5e_official_audit.md` the commands run, their results, and every site skipped with its reason.

**Status key.** ☐ open · ☑ done · ⛔ GATED(Qn), which waits on an owner ruling (AUDIT §5 / DESIGN §7).

---

## Phase 0: Tooling and baseline

### ☑ T0.1 Move the math checkers beside the module
- **Files:** move `docs/audit_oraga_5e_official/{bestiary_check,pregen_check}.py` → `T/`.
- **Do:** make the paths repo-relative (resolve `M/10_Bestiary.md` and `M/11_Pregenerated_Characters.md` from `__file__`). Give each script a non-zero exit code on any mismatch. Add a `--quiet` flag.
- **Accept:** both scripts exit 0 on the current text. Their stdout summaries (25 blocks + 5 Nastier; 5 pregens) are logged.
- **Time:** 15 min.

### ☑ T0.2 Write the style linter with tests first (TDD)
- **Files:** new `T/lint_5e.py`, `T/test_lint_5e.py`, `T/lint_5e_allow.txt`, `T/fixtures/*.md`.
- **Do:**
  1. Write `test_lint_5e.py` first, with a fixture per rule family listed in DESIGN §4 (hard, soft and structure). Each family needs at least 3 tests: a hit, a clean miss, and an edge case (a hit inside an indented read-aloud block is ignored where the rule says so; a whitelisted line is ignored). Run it and confirm it fails (red).
  2. Implement `lint_5e.py` until it passes (green).
  3. Output a per-file table of hard-rule hits (with file:line and the matched text) and the soft metrics. `--baseline` writes `T/lint_baseline.json`. `--check` compares against it.
  4. Sentence splitting: skip tables, headings, stat blocks (lines between a stat-block header and the next `---` or H2), and indented read-aloud. Treat `;` as a sentence end only for the "over 30 words" metric.
- **Accept:** `python -m pytest T/test_lint_5e.py -q` is all green. Report the test count (at least 3 × the number of rule families). The linter runs on `M/` in under 10 s.
- **Time:** 2 × 30 min (split: tests + hard rules / soft + structure rules).

### ☑ T0.3 Write the style sheet into the module folder
- **Files:** new `M/STYLE_5e.md`.
- **Do:** copy DESIGN §3's table, add one worked example per row, and add a "Do not touch" list: Handout 1's canonical invitation text, quoted NPC speech that is canon (it keeps its wording; only the surrounding DM text changes), and INVENTIONS_5e.md.
- **Accept:** the file exists. README's contributor section links to it once T2.3 lands.
- **Time:** 15 min.

### ☑ T0.4 Record the baseline
- **Do:** `python T/lint_5e.py --baseline`. Paste the per-file summary into LOG under "Baseline".
- **Also:** commit Phase 0 and tag the commit `pre-official-5e`, so T9.1 and the owner can diff the whole pass.
- **Accept:** `T/lint_baseline.json` is committed and the tag exists. The LOG has the table. This is the "before" picture for the owner.
- **Time:** 5 min.

---

## Phase 1: Rules contradictions and the owner rulings already given

### ☐ T1.1 One Focus trigger for the Attendant (NIGHT-1, O2)
- **Files:** 05 (*How to Run the Attack* bullet 2, "When the party becomes…"), 09 S14 *Enemy*, 08 Table VIII–1/VIII–2 Attendant line, 10 Attendant block (Focused/Idle text).
- **Do:** use the NIGHT-1 replacement text in 05. Check that 09, 08 and 10 say the same thing: the card fires Idle, and the Attendant is Focused at the start of any turn when one of the three in the scene has no Delay.
- **Accept:** only one trigger wording exists module-wide (grep "Focused"; every hit agrees). SA.
- **Time:** 20 min.

### ☐ T1.2 The Attendant vanishes for one Movement only (BALL-2, O2)
- **Files:** 04 ("The quiet guest" rule paragraph); 07 ("It is gone until the Unmasking"); 09 S14 "A habit the party has seen: +2".
- **Do:** 04 before→after as in BALL-2. Make 07 say the same. In S14, add "Only habits the table actually saw count."
- **Accept:** grep "gone until the Unmasking" = 0. SA.
- **Time:** 15 min.

### ☐ T1.3 Remove the Attendant's truthful-answer habit (owner Q5, O3)
- **Files and sites (locate by quote):**
  - 07: the four-habits sentence ("*it answers any direct question literally, and cannot leave one unanswered*"); the *Play it* line "answers exactly the question asked".
  - 04: the Movement III sighting "**The quiet guest — the literal answer.**" (cut the whole paragraph; keep the italic line about the three gray masks by moving it to the Movement III Uninvited note if it isn't already there); the rule paragraph ("one sighting per Movement" → "one sighting in Movements I, II, IV and V").
  - 08: Table VIII–1 "The quiet guest" column, Movement III cell → "—".
  - 09: S14 habit list (four → three habits); the "Argue its orders" bullet (cut "A direct question it must answer is a habit.").
  - 10: the Attendant **Languages** line ("speaks only when asked, and answers literally and truthfully" → "Common; speaks only when spoken to"); the "Its habits" line.
  - 01: Table I–3 omen row, if it names the literal answer.
  - `M/INVENTIONS_5e.md` #55: add "habit 'answers any direct question' removed by owner ruling 2026-09-30 (Q5)".
- **Do:** keep the Attendant's surviving personality ("names no one, and looks around for the master"). It is not the removed mechanic, but check each kept line against the ruling.
- **Accept:** grep -i "direct question|literally and truthfully|literal answer" in `M/*.md` = 0 (INVENTIONS history excepted). Every habit count says three. Every "one habit per Movement" line matches O3. SA.
- **Time:** 30 min.

### ☐ T1.4 Leashed return point (NIGHT-2, O4)
- **Files:** 05 (*The last blow*; the second "come back on their next turn" site); 10 the Radiant and the Wept *Leashed* traits.
- **Do:** apply the NIGHT-2 wording. Leave the Hollow's "within 60 feet of the doors he holds" as it is.
- **Accept:** grep "within 60 feet of (his|her|its) quarry" = 0. SA.
- **Time:** 15 min.

### ☐ T1.5 The detain mercy defers to *To the Terms* (BESTIARY-1, O5)
- **Files:** 10 *How to Read*, "Knocked out, not killed"; also 05 *Midnight Rules* and 08's midnight-rules bullet, if either lists the Bought.
- **Do:** apply the BESTIARY-1 before→after.
- **Accept:** every mention of what the Bought do on a detain contract reads "1 Hit Point and the Grappled condition". SA.
- **Time:** 10 min.

### ☐ T1.6 Agenda 4: the east-wing doors and "Dinner for Two" (BALL-1, owner Q6)
- **Files:** 04 (Movement IV time box; new subsection **Dinner for Two (B9)** under Movement IV; B9's "ways in" line; Undercurrent C's door line); 07 (Veier and Raunu entries, for consistency); 03/Handout 2 card 4 (check only).
- **Permitted sources (no other facts):** the grandmother's ring (03, Handout 2); Raunu's line "If she chooses you, you will know"; 07's Veier *Wants/Fears/Secret/Play her* and quote; 07's Raunu entry; Agenda 4's three questions and the answers 07 already gives; the B9 room description (the two plates, the midwife, the traveling pack); Corval's door duties.
- **Do:**
  1. Move the dinner from *If you have time* to *Run* ("…if anyone carries Agenda 4").
  2. Access: a character who shows the ring to the door guards and asks for Veier by name is asked to wait; the ring goes in; by default Veier chooses them, and a guard walks them up.
  3. Scene: a trigger line plus a 60–90-word read-aloud box made only from seeded B9 details; an envelope for Veier and for Raunu; a **Topics** bullet list, with the answer to each from 07; the line "Raunu does not say what he will announce at the Unmasking"; a length cap of about 10 minutes of table time; an exit (Corval comes to the door as the lamps lower, and the guest is shown out → Movement V).
  4. Veier's answer on the pregnancy follows R6 and is ⛔ GATED(Q7). Until Q7 is ruled, write "she does not speak of it; see chapter II, R6" and mark the line TODO-Q7.
- **Accept:** the scene can be run from the page (checklist C-S16: arrival box, envelope, topics, interruption or exit). Ledger rows are added for the box and the topics list. SA.
- **Time:** 30 min.

### ☐ T1.7 Player-safe crystal-charge handout (FRONT-2)
- **Files:** 08 (new **Player Handout 3 — Crystal Charges**; the old Handout 3 becomes a DM table in T2.5); 03 (*Crystal Charges* pointers); 11 (the "read *Items of the Night*, chapter X" pointer).
- **Do:** copy the six common charges' rules text exactly from 10 *Items of the Night* (relocation, not new text). Leave out the "something that eats magic" line, or replace it with "Some things at this ball smother a charge; the DM will tell you." Use item names in the §3 style. Point 03 and 11 at the handout.
- **Accept:** no player-facing chapter (03, 11, handouts) points into chapter X. SA.
- **Time:** 20 min.

---

## Phase 2: Architecture

### ☐ T2.1 Move the agendas out of the player chapter (owner Q2, O6; FRONT-1)
- **Files:** 03 (*The Agenda System*, *The Eight Agendas*: cut); 02 (paste as `## The Eight Agendas` inside the DM-only half, after *The Truth of the Night*); 01 (the routing line "Chapter III (only if players build their own characters…)"); 11 intro ("as Chapter III requires"); every pointer to "Chapter III" that means the agendas (grep `Chapter III|chapter III`); `M/flow/flow.json` (node text and refs).
- **Do:**
  1. Move the text unchanged.
  2. In 03, leave one player-safe paragraph: "At the start of the night the DM deals each player one agenda card (Handout 2). Your card is all your character knows about it."
  3. Fix FRONT-8's count ("Three of the eight agendas…") in the moved text.
  4. Re-point every agenda reference to chapter II.
- **Accept:** 03 contains no "At midnight" line and no agenda body text. grep "The Eight Agendas" points only to 02. `python M/flow/build_flow_page.py` succeeds. SA.
- **Time:** 30 min.

### ☐ T2.2 Front matter: Background, Overview, legend, range, rests, 2014 claim (FRONT-3, -4, -5, -16, -17, -18, -19)
- **Files:** 01, README.
- **Do:**
  1. Add `## Adventure Background` after *What This Adventure Is*, using the FRONT-3 draft (sources: chapter II only). Shorten prep-box step 2 as FRONT-3 says.
  2. Add an **Overview** (the seven one-liners from FRONT-4) before Table I–1.
  3. Move *How This Module Is Written* to just after *What You Need*, retitle it **Reading This Book**, and rewrite it to the §3 read-aloud and box-species rules. Remove the code spans, and correct the clock sentence (FRONT-5 items 1–6).
  4. Party-range sentence and the "not cumulative" line (FRONT-16).
  5. The chapel short-rest line (FRONT-19).
  6. Soften the 2014 claim and add the 2014 gift house rule to *Changes from the SRD* (FRONT-18).
  7. Remove "Mirror Master" here, since T4.1 does the global swap.
- **Accept:** 01's first four H2s are, in order: What This Adventure Is, Adventure Background, (Overview inside or next to the Movements section), Reading This Book, What You Need. The legend matches STYLE_5e.md. Ledger rows exist for the Background and the Overview. SA.
- **Time:** 2 × 25 min.

### ☐ T2.3 Regroup the README and split out contributor text (FRONT-11, -20; O8)
- **Files:** README; 08 H1.
- **Do:**
  1. Group the contents table under **Before the Night** (I–III), **The Night** (IV–VI) and **Appendices** (VII–XI, each with a line saying when to open it).
  2. Move the INVENTIONS and flow rows under `### For Contributors`, and link STYLE_5e.md there.
  3. Add the four missing house rules to *Changes from the SRD*: success at a cost, NPCs don't roll outside a fight, nonlethal ranged and spell attacks, and the DC ladder.
  4. Retitle 08 to "VIII. The DM Sheet, the Palace and the Handouts".
- **Accept:** README reads as product front matter first. SA. (If Q3 rules "renumber", T8.1 supersedes step 1.)
- **Time:** 20 min.

### ☐ T2.4 Remove duplicated rule text (FRONT-9, SNAKES-28, NIGHT-8, SNAKES-25, BESTIARY-19). Q21 approved 2026-10-03
- **Files:** 01, 04, 05, 08, 09, 10, `flow.json`, INVENTIONS #5/#7/#11/#15.
- **Do now (not gated):**
  - (a) Rename 05's section "Knives in the Dark" → **The Snakes in the Dark**, and rename card S2 → **S2. The Service Corridor Job**. Update every pointer: 04 ×3, 05 ×3, 08, 09 Table IX–3, INVENTIONS and flow.json.
  - (b) Make 09's three rules the only ground-rules list. 01 keeps its framing paragraph plus the Attendant bullet, points to chapter IX, and drops its three duplicate bullets (FRONT-9).
  - (c) Make 10's Fracture copy a strict compression of 05's, or cut it to the DCs plus a pointer (BESTIARY-19).
- **Also do (Q21 approved):** trim 04 *The Snakes in the Pen* to Table IV–1 plus one pointer sentence, and trim 05 *The Snakes in the Dark* to Table V–7 plus card pointers. Reconcile 04 Table IV–1's Movement V posts with 09 (SNAKES-28 last bullet).
- **Accept:** "Knives in the Dark" occurs 0 times. There is one rules list for the snakes. The Fracture text in 10 is a subset of 05's. The flow page rebuilds. SA.
- **Time:** 30 min (now) + 20 min (after Q21).

### ☐ T2.5 Handouts: the DM table, triggers and placement (CAST-8, -9, -25, -26, -27)
- **Files:** 08.
- **Do:**
  - Old Handout 3 → "**Rumors at the Ball** *(DM table)*" (Table VIII–7 unchanged).
  - Add a trigger and recipient line to Handout 1 (CAST-9 wording; do **not** touch the invitation text).
  - Rename the headings "Player Handout 1: The Invitation", "Player Handout 2: Agenda Cards", "Player Handout 3: Crystal Charges" (from T1.7), and group them in one closing section of 08, "Player Handouts".
  - Split the DM sheet into two pages at *The pillars* and retitle it "The Night on Two Pages" (CAST-26).
  - The palace diagram gets one B5 box, with the gate, lower garden and terraces as labels inside it (CAST-27).
- **Accept:** no DM-only text (parentheticals, "Roll", instructions) inside any player handout. Each handout has a trigger line. SA.
- **Time:** 25 min.

### ☐ T2.6 Chapter 06: dedupe and add a rewards recap (FRONT-15, -23)
- **Files:** 06.
- **Do:** cut steps 2–3 to the FRONT-15 pointer, fix the trail check skill, and add `## Rewards` with the four pointer lines. The Church's favor stays a pointer until Q15 is ruled.
- **Accept:** SA.
- **Time:** 15 min.

---

## Phase 3: Mechanics fixes, one task per chapter (these can run in parallel)

Each task: rerun both math scripts and the linter's structure rules. Mirror sites are listed, and must be changed in the same task.

### ☐ T3.1 Chapter 04 mechanics
- **Findings:** BALL-6 (gate fail by 5+), BALL-7 (4 checks with no result), BALL-8 (the Seating Feud, O7; also fix "see the sidebar below"), BALL-9 (summons: four guests, audience length, *friendly* trigger), BALL-10 (the orrery), BALL-16 (04 side: the guard trigger → Bloodied, card S4), BALL-17 (the toast and the Dead Dance for absent characters), BALL-18 (thieves' tools grammar, open-skill defaults), BALL-19 (one DC ladder), BALL-26 (the Undercurrent A retry).
- **Gated item:** BALL-12 (Callun's prices) ⛔ Q15. Leave "TODO-Q15" in place.
- **Mirrors:** 09 S1 (feud timing), 09 S4 (see T3.3), 08 Table VIII–1 (the toast and feud rows).
- **Accept:** every check in 04 has a stated result where failure matters (spot-check the list of 14 checks in BALL-7/18). SA.
- **Time:** 2 × 30 min.

### ☐ T3.2 Chapter 05 mechanics
- **Findings:**
  - NIGHT-3: the beat/round unit, "until the scene ends", and a new **The Midnight Clock** block. Set the Radiant's default and log it in DECISIONS as O9 after checking it against the 05 and 08 sequence.
  - NIGHT-4: Fracture partial success, and skills with their abilities.
  - NIGHT-5: **Adjusting the Attack** sidebar with the NIGHT.md values; mark them *unsimulated* in LOG.
  - NIGHT-6: the "win outright" line.
  - NIGHT-7: the lanterns rule.
  - NIGHT-16: cut "the mask of an Uninvited left behind in a trap".
  - NIGHT-19: the cross-references and the 100 XP carry award.
  - NIGHT-20: the Evasion sentence.
  - NIGHT-21: the push direction, the Radiant's gate turn, no surprise at midnight, trampling (the damage value is a proposal: log it as an O-decision).
  - NIGHT-22: DCs in the trick tables.
  - NIGHT-24: Expected Duration lines and B12 **Treasure**.
- **General Features:** add **The Palace After Midnight: General Features** now, *without* dimensions (NIGHT-18: light, crowd, smoke, fire, taken from the book's own rules). The dimensions are ⛔ Q13.
- **Mirrors:** 08 (midnight rules and the clock line), 10 (the Fracture text, if T2.4c didn't already cover it), 01 Table I–4 (the carry award).
- **Accept:** the clock is stated in exactly one place and other sites point to it. No "perhaps" in 05's rules text. SA.
- **Time:** 3 × 30 min.

### ☐ T3.3 Chapter 09 mechanics
- **Findings:**
  - SNAKES-1: per-card *At heat 4* lines.
  - SNAKES-2: tracker rows (mirror in 08 Table VIII–7).
  - SNAKES-3: one morale trigger (mirror in 10's Duelist *Breaks*).
  - SNAKES-4: detection lines on S2, S7, S8 and S10, plus the "nobody is surprised unless" rule. Use the real passive Perception values from 10.
  - SNAKES-6: Inspiration tied to Table I–3 rows.
  - SNAKES-7: the 2014 DM Note.
  - SNAKES-8: remove "Deadly".
  - SNAKES-9: the S10 heat gate.
  - SNAKES-12: inline **Treasure** values from 10 *The Night's Loot*.
  - SNAKES-20: "not cumulative", and rename *Scaling* → **Adjusting the Encounter**.
  - SNAKES-21: the missing Tactics, Morale and Development fields.
  - SNAKES-23: the card-level fixes.
  - SNAKES-26: "divided equally".
  - BALL-16, 09 side: S4's base matches its scaling line, add *Where and when* for the Movement I gate, and route Development to the current Movement.
  - S8 and S12 budget labels against the Low line, including S8's new total once Kovaun is CR 1/2 (T3.4).
- **Gated:** SNAKES-5 (XP for walk-away outs) ⛔ Q14; SNAKES-22's S9 figure ⛔ Q12 (do the S13 half now: "The man reaching for his knife is Essin Boranis."); S13 *Broker a trade* ⛔ Q11.
- **Accept:** every card has Tactics, Morale, Development (win and lose), Treasure, Rewards and Adjusting lines. Every budget label is arithmetically true against the SRD 5.2.1 budget for four 4th-level characters. SA.
- **Time:** 4 × 30 min.

### ☐ T3.4 Chapter 10 mechanics
- **Findings:**
  - BESTIARY-2: the Wept's *She Arrives*.
  - BESTIARY-3: the *Call the House* cap.
  - BESTIARY-4: Kovaun CR 1/2, and hand the S8 figure to T3.3.
  - BESTIARY-6: the success clause on *The Post*.
  - BESTIARY-9: the base Delay-trick DC.
  - BESTIARY-17: the save-effect clauses.
  - BESTIARY-18: the edge cases on *Two Turns*.
  - BESTIARY-20: note the SRD base creatures (guard, commoner).
  - BESTIARY-22: Veier's line.
  - BESTIARY-23: the item-type caption, and the coat's value (⛔ Q15 for the coat only).
  - BESTIARY-24: an optional one-liner.
  - SNAKES-1/-23 mirrors: Phern Bodyguard *Nastier* to S-3's wording; Draunel's *Nastier* agrees with S13's 5th-level line.
- **Gated:** BESTIARY-11 (Vell under attack) ⛔ Q8; BESTIARY-21 (alignment dash) ⛔ Q18.
- **Accept:** `bestiary_check.py` exits 0. Extend the script to assert Kovaun's new XP and PB, and the Wept's attack count per turn. SA.
- **Time:** 2 × 30 min.

### ☐ T3.5 Chapters 07, 08 and 11 mechanics
- **Findings:**
  - CAST-3: the default-DC sentence in the 07 intro, and the Sergeant's DC.
  - CAST-4: Vell's DCs with abilities (mirror in 08 Table VIII–3).
  - CAST-11: Andra's crystal as an arcane focus. Ilesse ⛔ Q16.
  - CAST-12: the 2014 note.
  - CAST-14: Key DCs rows.
  - CAST-19: Callun DC 20; 04's "Hard DC 18–20".
  - CAST-21: the pregen intro claim.
  - CAST-22: SRD 5.2.1 wording for Arcane Recovery, Fast Hands (use the verified 5.2.1 text: Bonus Action; *Sleight of Hand* or *Use an Object*) and Veier's *For Them* range.
  - CAST-20: the snake count in 07's intro.
- **Accept:** `pregen_check.py` exits 0. Extend it to assert Andra's focus is listed. SA.
- **Time:** 30 min.

---

## Phase 4: Module-wide mechanical sweeps

These rules are mechanical, but a worker makes every edit with the linter's hit list in hand. No blind global `sed`. Read-aloud and quoted speech are skipped unless a rule says otherwise.

### ☐ T4.1 MM → DM (owner Q1)
- **Scope:** every `M/*.md` file, `flow.json` and `flow_page.template.html`.
- **Rules:** "the MM" in instructions → "you" where the sentence is addressed to the DM, otherwise "the DM". "MM Note" → "DM Note". "MM sheet" → "DM sheet". "MM-only" → "DM-only". "Mirror Master (MM)" → delete, and the README defines nothing (DM needs no definition). The pregen sheets say "the DM".
- **Accept:** lint's role-name rule = 0 hits. The flow page rebuilds. The Facets edition is untouched (`git diff --stat adventures/` is empty).
- **Time:** 2 × 30 min.

### ☐ T4.2 5.2.1 capitals, spells, items, coin (O1; FRONT-10, BALL-15, NIGHT-12, SNAKES-17, BESTIARY-16, CAST-13)
- **Scope:** every `M/*.md` file.
- **Rules:** DESIGN §3 rows: *Rules-term capitals*, *Spells*, *Magic items*, *Coin*. Keep "Utilize" (it is 5.2.1). Condition phrasing becomes "has the Prone condition" / "is Unconscious and Stable".
- **Accept:** lint's lowercase-term and coin rules = 0 hits.
- **Time:** 2 × 30 min.

### ☐ T4.3 Check, save and damage grammar; numerals (C-V15–19; SNAKES-14/18/19, BESTIARY-8, FRONT-14, BALL-18, NIGHT-4/22, CAST-14)
- **Scope:** every `M/*.md` file.
- **Rules:** DESIGN §3 rows: *Checks*, *Saves and damage*, *Numbers*. Use the slice audits' before→after wording where it is given (BESTIARY-8 has 9 sites; SNAKES-14 has 25).
- **Accept:** lint smells S3–S13 and S37 = 0 hits outside the whitelist.
- **Time:** 2 × 30 min.

### ☐ T4.4 Stat-block layout to 5.2.1 (BESTIARY-5, -12, -13, -14)
- **Files:** 10.
- **Do:** DESIGN §3 *Stat blocks* row. Armor goes on a **Gear** line; one **Immunities** line; the Senses semicolon; Initiative folded; commentary moved out of the numeric fields; usage tags; ***Bloodied.*** traits; the epithet line; traits with no rule moved to lore or Tells (BESTIARY-14; keep *The Wrapped Sword*).
- **Accept:** `bestiary_check.py` still exits 0. Update its parser for the Gear line and the folded Initiative, test-first, adding a case for each. A spot check of 3 blocks matches the SRD 5.2.1 layout.
- **Time:** 2 × 30 min.

### ☐ T4.5 Cross-references and provenance (SNAKES-15, -24; CAST-24; FRONT-22; NIGHT-19; BALL-25)
- **Scope:** every `M/*.md` file and flow.json.
- **Rules:** DESIGN §3 *Cross-references* row. Remove "(source Ch. …)" and "(Val'loh, V3)". Fix FRONT-22's broken targets and INVENTIONS #25.
- **Accept:** the lint structure rule "all references resolve" passes. Zero `\(source Ch`.
- **Time:** 30 min.

### ☐ T4.6 Spelling and small consistency (BALL-22, NIGHT-23 part)
- **Do:** American spelling. "Gray", with the INVENTIONS #43 "grey robes" exception checked first and whitelisted if it is canon. "Its sight" → "his sight"; the Vell sentence at the Crossing; Tavva's knife count (NIGHT-23).
- **Accept:** the lint spelling rule = 0 hits.
- **Time:** 15 min.

---

## Phase 5: Read-aloud and styling

### ☐ T5.1 Box placement and the italics legend in 04 (BALL-3, -4, -5, -23)
- **Do:**
  - Move the B2, B4, B6 and B9 headers above their triggers and cut the re-descriptions (BALL-3).
  - Chapel box: move the offerings sentence to DM text with its checks (BALL-4).
  - Summons: convert it to a DM subsection with bold questions and quoted replies. Toast: one italic read-aloud block, with the speech in quotes and the stage cues in roman (BALL-5).
  - Continuity leftovers (BALL-23): masks, "unchanged", the duplicated Corval sentence, and the cup box order.
- **Accept:** every indented italic block in 04 is read-aloud and has a trigger line (lint structure rule). SA.
- **Time:** 30 min.

### ☐ T5.2 Italics and boxes in 05 and 07 (NIGHT-10, -11; CAST-17, -18)
- **Do:**
  - NIGHT-10: MM Note narration → instruction.
  - NIGHT-11: italicize the epilogue box, and set the five italic DM paragraphs in roman.
  - CAST-17: box labels to the declared species ("What Vorlain Says", "What Corval Says", "DM Note — the factor").
  - CAST-18: replace 07's copy of the Attendant box with a pointer, and cut the duplicate Vorlain quote.
- **Accept:** the lint structure rule passes for 05 and 07. SA.
- **Time:** 25 min.

### ☐ T5.3 New read-aloud: the Crossing and the opening of Movement VII (NIGHT-9)
- **Do:** use NIGHT-9's two drafted boxes. Before using the Movement VII box, verify "the minister who greeted you at the gate" against 04's receiving line. Cut the matching imagery from the DM text so it keeps only function.
- **Permitted sources:** 05's own text at the Crossing and at Movement VII's opening, and 04's receiving line.
- **Accept:** each box is 50–110 words, has a trigger, and contains only facts from its sources. Ledger rows are added. SA.
- **Time:** 20 min.

### ☐ T5.4 Scannability: sidebars, paragraphs, first mentions (BALL-24, SNAKES-13, -16, NIGHT-23, CAST-15, -16)
- **Do:**
  - Each *Snakes This Movement* box becomes an H4 subsection (BALL-24).
  - Start the *Walk into it / Turn it / Snake on snake* labels on new paragraphs (SNAKES-13).
  - Bold stat-block names at first mention with "(see chapter X)", and move CR out of prose (SNAKES-16, NIGHT-23).
  - 07 appositions for the six faction entries, and stat-block pointers for the Sergeant and Captain (CAST-15). Optionally rename *Play him* → **Roleplaying [Name]** and add **Quote:** lines from existing quotes only (CAST-16).
- **Optional (DM choice, house):** move S14's simulation table and the percentage asides into one "How it plays" DM Note per card (SNAKES-27).
- **Accept:** the lint first-mention rule passes. SA.
- **Time:** 2 × 30 min.

---

## Phase 6: NPC knowledge

### ☐ T6.1 "What they know" lists (CAST-2, -23; BALL-11)
- **Files:** 07 (11 entries: Raunu, Veier, Anha, Kovaun, Sella, Callun, Corro, Draunel, Essin, Maiven, Tavva); 08 Table VIII–7 (truth notes); 04 (name Vell at the two "tall pale factor" sites, BALL-11).
- **Do:**
  - For each entry: a trigger sentence plus bullets, **assembled only from facts already printed**. Cite the source line for each bullet in the ledger row. Use CAST-2's Anha list as the model.
  - Raunu's list states what he will not answer.
  - Mark false beliefs "(untrue)".
  - Rumors 6, 8 and 11 get truth notes. Rumors touching *What the Module Never Says* stay unmarked.
- **Gated:** Veier's pregnancy line ⛔ Q7. Essin's "two bodies" bullet ⛔ Q11.
- **Accept:** every talkable NPC has a list. Every bullet's source is in the ledger. SA.
- **Time:** 3 × 25 min.

---

## Phase 7: Prose voice (light touch; keep the voice)

**Rules for every chapter task:**
- Use the slice audit's before→after examples first, then apply the same moves elsewhere.
- Moves:
  - "the characters" for the party, and "you" only for the DM;
  - remove conversion talk and narrator voice;
  - split sentences at em-dash and semicolon chains;
  - undo "not X but Y" flourishes and tricolons that exist only for rhythm;
  - cut self-praise ("a superb scene") and winks;
  - keep one functional contrast where it carries a rule.
- **Keep:** jokes the audits said earn their place (03 "nobody and everybody", "load-bearing wall", Corval's character comedy), canon quotes, the read-aloud (polish it only if the audit names it).
- **Metric targets (lint soft rules, DM prose):** mean ≤ 19 words per sentence; ≤ 12% of sentences over 30 words; ≤ 8 em dashes per 1,000 words; ≤ 3 paragraphs over 120 words; S2, S25–S30 = 0.
- **Accept (each):** targets met or the variance explained in LOG, SA, and a before/after sample of 3 paragraphs pasted into LOG for the owner.

### ☐ T7.1 PILOT: Chapter 04 (BALL-13, -14, -20, -21; FRONT-7 04 sites)
- **Time:** 3 × 30 min. **Then STOP for owner review of tone** (checkpoint G1). Tasks T7.2–T7.9 don't start until the owner approves or adjusts the approach.

### ☐ T7.2 Chapter 05 (NIGHT-13, -14; FRONT-7 05 sites, including the "*(New in this edition.)*" tags)
- **Time:** 3 × 30 min.

### ☐ T7.3 Chapter 09 (SNAKES-10, -11; FRONT-7 09 sites)
- **Note:** SNAKES-10 option (b) was chosen: convert the imperative *Walk into it* blocks to the official voice.
- **Time:** 2 × 30 min.

### ☐ T7.4 Chapter 07 (CAST-5, -6, -7; FRONT-7 07 site)
- **Time:** 30 min.

### ☐ T7.5 Chapter 10 (BESTIARY-10, -15; FRONT-7 10 site)
- **Time:** 30 min.

### ☐ T7.6 Chapters 01, 02, 03, 06 (FRONT-7, -21)
- **Time:** 2 × 25 min.

### ☐ T7.7 Chapters 08 and 11 and the README
- **Scope:** "player" → "character" on the sheets where it means the character. Pregen personality prose is light-touch only.
- **Time:** 25 min.

---

## Phase 8: Tasks gated on owner rulings (slot in as rulings arrive)

| Task | Gate | Findings | Files | What happens once ruled |
|---|---|---|---|---|
| ⛔ T8.1 | Q3 | FRONT-11 | all, flow | If "renumber": Introduction, Parts 1–3, Appendices A–E; rewrite about 420 references with a script plus the lint resolver. If "regroup": nothing (T2.3 did it) |
| ⛔ T8.2 | Q4 | FRONT-6 | 01 | Convert the designer's note to the unsigned **DM Note — what the fights are for** (FRONT-6 draft), or keep it and whitelist it |
| ⛔ T8.3 | Q7 | CAST-2, BALL-1 | 04, 07 | Veier's pregnancy line in the dinner topics and her knowledge list |
| ⛔ T8.4 | Q8 | BESTIARY-11 | 10, 05 | Add Vell's ***Not There*** or ***Not Worth It*** trait (or the owner's own) |
| ⛔ T8.5 | Q9 | NIGHT-17 | 05 | One sentence per Uninvited in the trap sidebar |
| ⛔ T8.6 | Q10 | NIGHT-15 | 05, 10 | Fix the carrier of the contract case. Log a Facets follow-up in the carryover doc |
| ⛔ T8.7 | Q11 | SNAKES N2, CAST N9 | 07, 09 | Essin's "two bodies": keep literal, or rewrite S13's out and the Boranis line |
| ⛔ T8.8 | Q12 | SNAKES-22 | 09 | Name or cut the S9 figure |
| ⛔ T8.9 | Q13 | NIGHT-18 | 05, 04, 08 | Add dimensions to General Features, or the "no fixed plan" line |
| ⛔ T8.10 | Q14 | SNAKES-5 | 09, 01 | "(no XP)" on walk-away outs; S14's Rewards line; Table I–4 clause |
| ⛔ T8.11 | Q15 | BALL-12, FRONT-13, BESTIARY-23 | 04, 03→02, 06, 10 | Print the amounts: Callun Mv III and the nursery, the Church's favor default, the coat |
| ⛔ T8.12 | Q16 | CAST-10, -11 | 11 | Ideal from the source `.fof`, agenda hook → **Bond**; flaws if written; Ilesse's holy symbol or pouch |
| ⛔ T8.13 | Q17 | FRONT-12 | README, 02, 06, 07 | Pronunciations at first mention; the "PG" decision; the Blackwatch and Mazaa glosses |
| ⛔ T8.14 | Q18 | BESTIARY-21, CAST N6 | 10, 07 | The "—" alignment on the Uninvited and Vell; cast tags if chosen |
| ⛔ T8.15 | Q19 | CAST N7 | 08 | Card initials: keep them, or "delivered in person" |
| ⛔ T8.16 | Q20 | CAST N9 | 07, 04 | Sixty or eighty servants; the testament's witnesses |
| ☑ T8.17 | Q21 | FRONT-9, SNAKES-28 | 04, 05 | **Approved 2026-10-03.** Merged into T2.4 |
| ☑ T8.18 | Q22 | O3 | — | **Closed 2026-10-03:** no replacement habit. O3 stands |

Each T8 task: SA, a ledger row citing the ruling, and a DECISIONS entry.

---

## Phase 9: Closeout

### ☐ T9.1 Ledger sync
- **Do:** every block added from printed facts (Background, Overview, the dinner scene, the charge handout, knowledge lists, new boxes, detection DCs, Adjusting values, Midnight Clock default, trample damage) has an `INVENTIONS_5e.md` row with its sources. Mark #55 amended per Q5.
- **Accept:** the ledger reviewer's check: every new H3/H4 or boxed block since the baseline commit (`git diff pre-official-5e..HEAD`) either maps to a row or is pure relocation.

### ☐ T9.2 Flow page
- **Do:** update `flow.json` for the renames, the moved agendas, DM wording and the Midnight Clock. Run `python M/flow/build_flow_page.py`. Republish the published artifact only if the owner asks.
- **Accept:** the build succeeds, and no node references a removed section.

### ☐ T9.3 Final verification
- **Do:**
  1. Run `lint_5e.py --check`, `pytest T/`, and both math scripts.
  2. Run one fresh-eyes read-through agent per slice against the C-S/C-V checklists, reporting only regressions or misses.
  3. Update each finding's status in the six slice files (fixed / skipped with reason / gated), and the §1 counts in `AUDIT_oraga_5e_official_style.md`.
  4. Post the before/after lint table in LOG.
- **Accept:** there are no P1s open. Every P2 is fixed or gated. The P3s are fixed, gated, or skipped with a reason.

### ☐ T9.4 d20 carryover record
- **Files:** new `docs/CARRYOVER_d20_oraga_official.md`.
- **Do:** list the 67 `[d20-portable]` findings with how each was solved in 5e, plus the Facets-affecting rulings (Q10, the FRONT-21 aphorisms, Q5's analog if the Facets edition has the habit). This is not applied now; the d20 edition is out of scope.
- **Accept:** the file exists and is linked from LOG.

### ☐ T9.5 Commits
- **Do:** one commit per phase, with specific `git add` paths. Messages like "Oraga 5e official pass: Phase 1 rules contradictions". No push without the owner's say-so. Before any push, scan main..branch for private canon (memory rule).
- **Accept:** `git status` is clean, and the LOG lists the commit hashes.

---

## Summary

| Phase | Tasks | Open now | Gated | Est. time |
|---|---|---|---|---|
| 0 Tooling | 4 | 4 | 0 | ~2 h |
| 1 Contradictions + rulings | 7 | 7 (T1.6 has one TODO-Q7 line) | 0 | ~2.5 h |
| 2 Architecture | 6 | 6 | 0 | ~3 h |
| 3 Mechanics | 5 | 5 (with named TODO lines) | parts of Q8/11/12/14/15/16/18 | ~6.5 h |
| 4 Sweeps | 6 | 6 | 0 | ~5 h |
| 5 Read-aloud and styling | 4 | 4 | 0 | ~2.5 h |
| 6 NPC knowledge | 1 | 1 | Q7, Q11 lines | ~1.25 h |
| 7 Prose | 7 | T7.1 pilot, then owner gate G1 | T7.2–T7.7 wait on G1 | ~7 h |
| 8 Rulings | 18 (2 closed) | 0 | 16 | ~4 h in total |
| 9 Closeout | 5 | after all | | ~2 h |

**Checkpoints for the owner:** G0 after Phase 0 (baseline numbers); G1 after the T7.1 pilot (tone); G2 at T9.3 (final audit table).
