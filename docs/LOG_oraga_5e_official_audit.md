# LOG — Oraga Night 5e: Official-Module Audit

*Scope: `conversions/dnd5e/oraga_night/` only. The findings are written so they can be
applied to the Facets d20 version later. That version is out of scope for now.*

## 2026-09-30 — Session 1

**Request (owner):** Do a full audit of the 5e Oraga Night module against the 5e reference books.
Review prose, mechanics, styling and content, so the module reads and plays like an
official module without crossing copyright. Classify the books by title first. Keep a
good log of all findings.

- Found the 5e library at `/mnt/e/books/DandD 5E/` (234 PDFs). The 3.5 library is in OneDrive
  and serves as secondary phrasing evidence.
- Classified the library by title: `docs/RESEARCH_5e_reference_catalog.md`.
- Extracted the audit evidence set to text in the session scratchpad. Two copies are
  image-only scans (the core-folder LMoP and Death House). The alternate copies were used.
- Next: (1) distill conventions into `docs/RESEARCH_5e_module_conventions.md`, (2) audit each
  chapter against them into `docs/AUDIT_oraga_5e_official_style.md`, (3) fix plan.
- Phase A launched: two research agents distilling the yardstick →
  `docs/RESEARCH_5e_module_conventions_structure.md` (architecture, keyed scenes, boxed text,
  sidebars, NPC/encounter/stat-block/treasure/handout format) and
  `docs/RESEARCH_5e_module_conventions_voice.md` (DM-facing voice, sentence rhythm, SRD
  check/save/damage/condition grammar, grep-able smell→official-form table).
- Phase B (pending Phase A): chapter-partitioned audit agents → `docs/AUDIT_oraga_5e_official_style.md`,
  each reading prior audits (`AUDIT_oraga_5e*.md`, `FIXPLAN_oraga_5e*.md`, `LOG_oraga_5e_pass2.md`)
  to avoid re-reporting fixed items. Findings tagged `[d20-portable]` where they would apply to the Facets d20 version too.
- Phase A.1 done: `RESEARCH_5e_module_conventions_structure.md` — 52-item checklist C-S1…C-S52
  (always/usually/sometimes). Key: fixed intro order + format legend; AL scaling + Expected
  Duration; 5 social/timed scene patterns (CoS special events, HotDQ siege clock, RoT council
  scorecard, dinner set piece, AL social-tier→combat); boxed text median ~62 words, trigger
  clause, NPC dialogue OK, never PC actions/mechanics; no numbered tables / designer-note boxes
  in 5e (house-style deltas logged in its §12). Caveat: typography inferred (extracts lose bold/italic).
- Phase A.2 done: `RESEARCH_5e_module_conventions_voice.md` — C-V1…C-V26 + 40 grep smells S1…S40
  (18 adventures, ~1.13M words). Key: "the characters"; ~16–19-word sentences, 45–75-word paras;
  "DC N Ability (Skill) check" near-universal; saves state failure ~80%, checks ~11%; damage
  "7 (2d6)" 567:69; italics spells/items, bold stat-block creatures; DMG attitude scale.
  Caveats: scratchpad SRD is 5.1, so 5.2.1 term table is flagged [verify 5.2.1]; 2014 vs 2024
  encounter-difficulty vocab mixing flagged as hazard.
- NEEDS-RULING raised early: module uses "MM" 80× (+1 "Mirror Master") where official 5e says "DM". Not decided in BRIEF/FIXPLAN.
- Phase B launched: 6 slice auditors → `docs/audit_oraga_5e_official/{FRONT,BALL,NIGHT,SNAKES,BESTIARY,CAST}.md`
  (FRONT also owns whole-module architecture; BESTIARY + CAST verify math with scripts). Finding IDs `<SLICE>-n`,
  P1/P2/P3, checklist-cited, `[d20-portable]` tagged. Consolidation into `docs/AUDIT_oraga_5e_official_style.md` after.
- BALL done (26: 2 P1 / 14 P2 / 10 P3). P1: Agenda-4 east-wing access + dinner-for-two underwritten (BALL-1);
  Attendant "gone until Unmasking" vs per-Movement sightings (BALL-2). Rulings N1–N5.
- CORRECTION: party level is **4th → 5th** (FIXPLAN §6), not 3rd as the shared brief said. Sent to NIGHT/SNAKES/BESTIARY/CAST.
  FRONT and NIGHT had already used 4th (NIGHT checked both).
- FRONT done (23: 2 P1 / 9 P2 / 12 P3). P1: Ch III player-facing but carries MM-only "At midnight" lines incl. Vell reveal
  (FRONT-1); Ch III/XI send players to MM-only bestiary for crystal charges (FRONT-2). Arch: missing Adventure Background,
  legend late (01:320) + italics≠read-aloud, handouts mid-book, snake ground rules printed 3× with differing counts,
  ~25 lines of conversion talk. Drafts supplied (Background, Overview). Owner Qs: MM/DM, designer's note, pronunciations
  + "PG", Church favour size, renumber?, banner-vs-move agendas.
- NIGHT done (24: 2 P1 / 16 P2 / 6 P3). P1: two Attendant Focus triggers (§5 vs §5b) (NIGHT-1); Leashed Uninvited returns
  "within 60 ft of quarry" can leap past Crossing/doors (NIGHT-2, new). Also: no unified Midnight Clock, no scaling on the
  attack, 2014-DMG multipliers put S3/S13 at Deadly vs module's 5.2.1 labels; S8/S12 "Low" under the Low line;
  "the characters" 0× vs "the players" ~19×; contract-case holder continuity.
- BESTIARY done (24: 1 P1 / 10 P2 / 13 P3). All 25 blocks + 5 Nastier variants re-derive correctly (script check).
  P1: intro says contract-detain drop = Unconscious+Stable, Bought Blade trait says 1 HP + Grappled. Also: Wept's
  *She Arrives* gives a 3rd 28-dmg attack per Shadow-Step (≈CR 14–17, dial moot); Call the House can summon 12 from 9;
  Damaris CR 1 overstated (~0–1/8), inflating S8; mixed 2014/2024 layout; 9 bare DCs. Rulings: attacking Vell,
  "—" alignment for Uninvited/Vell, Circle coat GP value.
- Saved the stat-block math checker to `docs/audit_oraga_5e_official/bestiary_check.py` (scratchpad is temporary); rerun after any block edit. BESTIARY confirmed the 4th-level basis; S8 800 XP labelled Low < Low line 1,000 (→ SNAKES).
- NIGHT revised at 4th level: 5.2.1 labels correct; under 2014 multipliers every multi-foe card is +1 band (S3/S13/S14-Focused Deadly). DCs 10/13/15/18 (+25 deliberate Very Hard) fit — no DC finding. P1s unchanged.
- SNAKES done (28: 0 P1 / 13 P2 / 15 P3). Content strong (faction tables ≈ official council/cult presentation); math and
  bestiary refs all resolve. Issues: heat 4 no-op on S8-dark/S11, 4 heat changes only in card text, no surprise/detection
  terms + boxes that pre-spot the party, walk-away outs pay full XP, no 2014-multiplier warning, "player character" 74× /
  "the characters" 0×, 25/33 DCs drop "check", run-on option blocks. Cross-file: Phern Nastier "third bodyguard" vs base 3;
  Draunel Nastier vs S13 scaling. Rulings: Essin's "two bodies" (still open, INVENTIONS #13), unnamed man in S9 box,
  XP for walk-away outs (Table I–4).
- CAST done (27: 1 P1 / 13 P2 / 13 P3). P1: Attendant's truthful answers unwritten (CAST-1). Pregen math clean; all SRD.
  Saved `pregen_check.py` beside the bestiary checker.
- CONSOLIDATED → `docs/AUDIT_oraga_5e_official_style.md`: 152 findings (8 P1 / 75 P2 / 69 P3; 67 d20-portable),
  10 cross-cutting themes, work streams A–I, 20 owner rulings Q1–Q20 (deduped from slice lists).
- Status: audit complete. No module file edited. Next: owner rulings Q1–Q20 → Planner decomposes WS A–I into
  `docs/TASKS_oraga_5e_official.md` → fix passes. WS A and D are unblocked now.
- OWNER RULINGS (2026-09-30): Q1 DM in 5e edition only · Q2 move agendas out of Ch III · Q5 REMOVE the Attendant's
  truthful/literal-answer habit ("weird mechanic I don't like"; it was 5e invention #55; CAST-1 void; S14 distraction
  trick at 09:1731 loses its basis — replacement habits/tricks would be new canon → ask, don't invent) · Q6 Agenda 4
  ring-at-doors + Chapter VII-only dinner, as proposed. Recorded in AUDIT §5a. Open: Q3, Q4, Q7–Q20.
- PLAN written (Planner): `docs/DESIGN_oraga_5e_official.md` (style sheet verified against SRD 5.2.1 — downloaded
  2026-09-30, CC BY 4.0; decisions O1–O8; order; risks) + `docs/TASKS_oraga_5e_official.md` (Phases 0–9, ~45 tasks,
  18 gated on Q3/Q4/Q7–Q22; owner checkpoints G0 baseline, G1 prose pilot on 04, G2 final). DECISIONS.md O1–O8 appended.
  New owner Qs: Q21 (redundancy cuts), Q22 (replacement Attendant habit). Corrections found while planning: SRD 5.2.1
  capitalizes everything (overrules FRONT-10), "Utilize" is a real 5.2.1 action (overrules SNAKES-17 part), the
  Mv III "literal answer" sighting (04) is the removed habit (O3). No module file edited yet.
- 2026-10-03 OWNER: Q21 approved (redundancy cuts → T2.4, fully ungated; T8.17 closed); Q22 no replacement habit (T8.18 closed, O3 confirmed). Open: Q3, Q4, Q7–Q20.

## 2026-10-03 — Phase 0 (Worker): tooling, style sheet, baseline

**T0.1 — math checkers moved.** `docs/audit_oraga_5e_official/{bestiary_check,pregen_check}.py`
→ `conversions/dnd5e/oraga_night/tools/` (untracked, so plain `mv`). Both now resolve the module
from `__file__`, cross-check their hand-entered numbers against the chapter text (bestiary: AC,
HP, hit dice, CR per block and the three Nastier lines that print numbers; pregens: AC, Hit
Points, Initiative, Passive Perception), exit 1 on any mismatch, and take `--quiet`. The DMG CR
estimate stays informational and never fails. One data-entry fix: the Nastier Sergeant inherits
the base block's Perception +3, so its Passive Perception 13 is correct (the old script reported
"13 vs 11" against itself). The AUDIT doc's path to the script was updated.
- `python T/bestiary_check.py --quiet` → `bestiary_check: 25 blocks + 3 Nastier checked; 0 mismatch(es)`, exit 0.
  (The plan said "25 blocks + 5 Nastier"; the script carries 3 Nastier variants with numbers. The other
  Nastier lines are narrative.)
- `python T/pregen_check.py --quiet` → `pregen_check: 5 pregens checked; 0 issue(s)`, exit 0.
- Detection verified on a scratch copy with HP edited (bestiary: 3 mismatches, exit 1; pregen: 1, exit 1).

**T0.2 — `T/lint_5e.py`, test-first.** `T/test_lint_5e.py` + `T/fixtures/` (hard_hits.md, clean.md,
module/ with mini 04/05/09/10) written first; red run = collection error (no module). Then implemented
to green.
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → **124 passed** (23 rule families:
  16 hard, 4 soft, 3 structure; ≥ 3 tests each, plus line classes, whitelist, CLI/baseline/check).
- Full module run: ~3.5 s.
- Implementation decisions (Worker level, within DESIGN §4):
  - Scopes. Role name, gp, British spelling, grey, Designer's note and the Attendant habit apply
    everywhere, read-aloud included. The other hard rules skip read-aloud; lowercase terms, designer
    "we" and spelled distances also skip quoted speech. Bare-DC and missing-"check" hits skip tables
    (the compression rule); DC ranges hit even in tables. Stat blocks are linted for hard rules
    (that is where the 5.2.1 grammar matters) but are skipped for the soft metrics.
  - Read-aloud = a blockquote whose first line starts with a single `*`, or an italic paragraph
    inside another blockquote. Bold-led blockquotes (sidebars, DM Notes, Wants/Tells) are DM prose.
  - Lowercase terms are narrowed to forms that are rules terms in context ("the dash action", "its
    speed", "knocked prone", "the prone condition", "and stable"), so English "speed", "help",
    "darkness" and the idioms "take advantage of", "to their advantage", "at a disadvantage" do not fire.
  - Bare DC reads on into the next line, so a wrapped "DC 15 Strength / saving throw" is not a hit.
  - Trigger lines: the nearest non-blank line within 2 lines above a box must be a prose line ending
    in a colon (§3 "Read this when…:"). A heading never counts.
  - Creature names: bold spans in a `**Enemies.**`/`**Enemy.**` paragraph, or followed by
    "(Chapter X)", shaped like a name (Title Case, no digits), first mention per file; matched to any
    H2/H3 in chapter X after dropping counts and "the" and singularizing.
  - `--check`: a hard or structure hit fails if its (file, family, matched text) count rises above the
    baseline. Soft: a targeted metric fails if it worsens by more than its tolerance (wps 0.3, long-
    sentence share 0.5 pt, em dashes 0.3/1k, long paragraphs 0) while above target; counts fail on any
    rise, except "you", which is reported only, because the §3 DM swap adds legitimate "you".
    **After a task that moves text between files (T2.1, T2.4, T2.5), re-run `--baseline` and log it.**
- Whitelist `T/lint_5e_allow.txt` (`file|quoted text|reason`): the six lines of Handout 1's
  canonical invitation. "grey robes" is NOT pre-whitelisted: §3 says check INVENTIONS #43 first.

**T0.3 — `M/STYLE_5e.md`** written from DESIGN §3: every row with a "Write / Not" example drawn from
text already printed in the module, a one-paragraph voice note, the "Do not touch" list (Handout 1,
canon NPC speech, INVENTIONS_5e.md), and the check commands.

**T0.4 — baseline.** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --baseline` → wrote
`T/lint_baseline.json`; `--check` immediately after → OK, exit 0.

## Phase 0 — Baseline

*The "before" picture for the owner (gate G0). Counts as of the pre-official-5e tag. "hard" and
"struct" are hit counts; wps = mean words per sentence in DM prose; >30% = share of sentences
(split at ; too) over 30 words; —/1k = em dashes per 1,000 words; paras>120 = paragraphs over
120 words outside background sections; rq = rhetorical questions. Chapter X's word count is low
because stat blocks (heading to the next `---`) are outside the prose metrics.*

| file | hard | struct | words | wps | >30% | —/1k | paras>120 | players | pl.char | you | perhaps | rq | not…but |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01_Overture.md | 35 | 0 | 4084 | 14.91 | 6.1 | 5.88 | 1 | 12 | 4 | 35 | 0 | 0 | 10 |
| 02_The_World_and_the_Night.md | 2 | 0 | 2462 | 15.68 | 10.37 | 14.62 | 1 | 2 | 4 | 7 | 0 | 0 | 6 |
| 03_Masks_and_Agendas.md | 17 | 0 | 3497 | 14.39 | 7.12 | 14.58 | 7 | 0 | 4 | 93 | 1 | 2 | 4 |
| 04_The_Ball.md | 77 | 0 | 11984 | 16.71 | 10.31 | 16.44 | 17 | 8 | 17 | 32 | 2 | 7 | 12 |
| 05_The_Longest_Night.md | 52 | 1 | 12085 | 17.77 | 13.43 | 17.21 | 25 | 16 | 37 | 29 | 1 | 2 | 18 |
| 06_Aftermath.md | 5 | 0 | 952 | 13.8 | 4.17 | 7.35 | 0 | 1 | 0 | 8 | 0 | 2 | 2 |
| 07_Cast_of_the_Ball.md | 29 | 0 | 5220 | 16.78 | 8.06 | 19.16 | 8 | 1 | 2 | 4 | 0 | 0 | 8 |
| 08_Handouts.md | 20 | 0 | 1471 | 10.01 | 0.6 | 17.0 | 0 | 1 | 1 | 10 | 1 | 2 | 1 |
| 09_The_Snakes.md | 106 | 1 | 15487 | 13.86 | 5.56 | 10.2 | 15 | 3 | 71 | 33 | 1 | 1 | 16 |
| 10_Bestiary.md | 67 | 0 | 2351 | 15.78 | 8.33 | 12.34 | 0 | 1 | 1 | 2 | 0 | 0 | 4 |
| 11_Pregenerated_Characters.md | 46 | 0 | 3145 | 11.23 | 3.12 | 11.76 | 0 | 0 | 2 | 1 | 0 | 6 | 2 |
| README.md | 3 | 0 | 753 | 17.93 | 6.52 | 11.95 | 1 | 0 | 1 | 4 | 0 | 0 | 1 |
| TOTAL | 459 | 2 | 63491 |  |  |  | 75 | 45 | 144 | 258 | 6 | 22 | 84 |

Targets: wps ≤ 19, >30-word sentences ≤ 12%, em dashes ≤ 8/1k, paragraphs > 120 words ≤ 3 per file.

| family | hits |
|---|---|
| role_name | 76 |
| lowercase_terms | 90 |
| bare_dc | 146 |
| roll_check | 5 |
| save_damage | 10 |
| conversion_talk | 34 |
| narrator_voice | 11 |
| designer_we | 2 |
| deadly_budget | 2 |
| pcs | 1 |
| spelled_distance | 13 |
| gp | 10 |
| british_spelling | 37 |
| grey | 16 |
| designers_note | 1 |
| attendant_habit | 5 |
| xref | 1 |
| creature_bold | 0 |
| readaloud_trigger | 1 |


Hard-rule detail: role_name is 75 "MM" + 1 "Mirror Master". bare_dc 146 = bare "DC N" with no ability, DC ranges, skill-only checks, and "DC N Ability (Skill)" without "check". The two structure hits: 05 untriggered read-aloud ("The outer gate is shut…") and 09's '(Chapter IV, "The Snakes This Movement — IV and V")', which matches no box in chapter IV (it has separate "— IV" and "— V" boxes).
- CoC REVIEW done (parallel side task) → `docs/RESEARCH_coc_for_facets.md`: Facets already covers CoC dice ideas; value is adventure craft (vital-clue maps, original chase rule, time-not-dead-end failure, per-act rewards, pregen 'hate to lose' line). Licence: BRP ORC SRD excludes CoC signatures; ORC vs GPLv3 treated as incompatible → ideas only in own words, no Chaosium text. 6 owner Qs in the memo. Not committed with 5e phases (separate topic).

## Phase 1

*2026-10-03, Worker. Rules contradictions and the owner rulings already given (Q2 prep, Q5, Q6, Q21/Q22 confirmations). Every edit was located by quoted text (DESIGN §2).*

**Commands, after every task:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`; and, after T1.3 and T1.6, `python conversions/dnd5e/oraga_night/flow/build_flow_page.py`. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 124 passed. The flow page rebuilt without errors. No re-baseline was needed.

**Hard hits: 459 → 452** (attendant_habit 5 → 0; lowercase_terms 90 → 88). Structure hits stay at 2, the same two as the baseline. Soft metrics did not regress. Two near-regressions in 04 were fixed during the work. First, the quiet-guest rule paragraph went over 120 words, so its *If anyone follows or confronts it* half became its own paragraph. Second, the Dinner topics were first written as questions and tripped the rhetorical-question count, so they were rephrased as noun phrases.

**T1.1 (NIGHT-1, O2).** 05 *How to Run the Attack*, bullet "Idle and Focused": swapped in the NIGHT-1 replacement wording (card S14 fires Idle; Focused at the start of any turn when one of the three in the scene has no Delay). Bullet 3 kept. 07 *If it comes to steel*: the Focused clause now states the same start-of-turn, no-Delay trigger. 09 S14 *Enemy*, 08 Table VIII–2 and the S14 sheet bullet, and 10 *Idle and Focused* already matched, so they were not changed. 01's overview line ("When one of the three turns it on the party, it is Focused") is compatible and was left for the Phase 7 prose pass.

**T1.2 (BALL-2, O2).** 04 quiet-guest rule: "It never fights before midnight. It is gone for the rest of that Movement and turns up in the next one as printed." 07 now says the same, with a pointer to chapter IV. 10 *Before Midnight* had the same contradiction in other words ("gone until midnight") and was fixed too. 09 S14 "+2" bullet: added "Only habits the table actually saw count." flow.json: all four remaining quiet-guest node summaries said "gone until midnight" and now say "gone for the rest of that Movement". grep "gone until the Unmasking" = 0.

**T1.3 (Q5, O3, Q22).** Removed the habit everywhere. In 07: the four-habits sentence (now three, shown in Movements I, II, IV and V); *Play it* becomes "it speaks only when spoken to". In 04: cut the "The quiet guest — the literal answer" paragraph. Its italic line about the three gray masks is now a separate italic note directly after the Movement III Uninvited note (folding it into that note pushed the paragraph over 120 words). The rule paragraph now reads "One sighting in Movements I, II, IV and V … one of its three habits". In 05 the habit list has three items. 08 Table VIII–1: the Movement III quiet-guest cell is "—". In 09 S14 the habit list has three items and the hint list drops the Movement III sighting. The *Argue its orders* out keeps its check but drops "A direct question it must answer is a habit." In 10: Languages reads "Common; speaks only when spoken to", the distraction trait says "three habits", the habit list has three items, the *Tells* drop the question-answering sighting, and the *Breaks* drop the direct-question clause. In flow.json the node qg-3 ("the literal answer") is removed, its edges are rejoined qg-2 → qg-4, and the S14 edge label reads "the three habits". 01 Table I–3 does not name the habit, so it is unchanged. INVENTIONS #55 has the amendment note. Kept as surviving personality: "names no one, and looks around for the master" (07, 10), and 10's *Wants* line "if asked what the order is, it repeats it word for word". That line is about its one order, not a general compulsion to answer truthfully, so it does not fall under the Q5 ruling. Flagged for the owner in case they read it otherwise. grep -i "direct question|literally and truthfully|literal answer" in `M/*.md` = 0, INVENTIONS history excepted.

**T1.4 (NIGHT-2, O4).** 05 *The last blow* and *How Leashed plays*: an Uninvited returns at the start of its next turn at full Hit Points in the space where it dropped (or the nearest unoccupied space). The first site also notes the Hollow's exception. 10 Radiant and Wept *Leashed*: same wording. The Hollow's "within 60 feet of the doors he holds" is left as it was. grep "within 60 feet of (his|her|its) quarry" = 0. 10's "Table tries" row ("back at full HP on their next turn") gives no location, so it does not contradict the fix and was left alone.

**T1.5 (BESTIARY-1, O5).** 10 *How to Read*, "Knocked out, not killed": the Bought come out of the list, with "the Bought leave a creature at 1 Hit Point and the Grappled condition instead, see *To the Terms*". 09 S3 *Tactics* ("left at 1 and held") was aligned to "left at 1 Hit Point and the Grappled condition". 05 *Midnight Rules* and 08's midnight-rules bullets don't list the Bought, so neither needed a change.

**T1.6 (BALL-1, Q6).** In 04: the Movement IV time box moves the dinner into *Run* ("and, if anyone carries Agenda 4, dinner for two in the east wing (B9)"). The *If you have time* clause and its self-contradiction are gone. New `#### Dinner for Two (B9)` at the end of Movement IV, containing: the staging line (moved from the agenda-beats parenthetical); the Q6 access step; the trigger line plus a 78-word read-aloud built only from seeded details (two plates, warm light, Raunu at ease, the midwife, the empty traveling pack); the Veier and Raunu envelopes from 07; "Raunu does not say what he will announce at the Unmasking"; a **Topics** list with each answer taken from 07, 03 or B9; a 10-minute cap; and the exit (Corval at the door as the lamps lower → Movement V). The agenda-beats parenthetical, B9's "ways in" line and Undercurrent C's door line now point to it or name the ring. In 07, Veier's *Where she is* names the ring and points to the new section. 03 Agenda 4 and Handout 2 card 4 are consistent, so they were checked only. flow.json `sc-dinner` has a new summary and its ref points to `#dinner-for-two-b9`. INVENTIONS #58 records the scene and its sources. **TODO-Q7:** the "midwife, or a child" topic reads "She does not speak of it (see chapter II, "Why the Ball")". An HTML comment `<!-- TODO-Q7 … -->` sits under it. *Deviation:* the task's wording "see chapter II, R6" was not used, because R6 lives in INVENTIONS_5e.md, not in chapter II. A printed pointer to it would not resolve. "Why the Ball" is chapter II's section on the announcement. Veier's *Want* "her child born safe" is left out of the Topics list for the same Q7 reason. **Open (logged, not invented):** Agenda 4 and Handout 2 say "no husband". The dinner puts Raunu at the table, and the page does not say whether the character can have Veier alone. That would be new canon, so it goes to the owner.

**T1.7 (FRONT-2).** New `## Player Handout 3 — Crystal Charges` at the end of 08, with a trigger line. The intro and the three player-relevant bullets are copied word for word from 10 *Items of the Night*, along with the six Common rows as **Table VIII–8**, with item names in italic Title Case. The *Near the Uninvited* bullet is replaced by "Some things at this ball smother a charge; the DM will tell you." The uncommon charges stay in chapter X only, since no pregen carries one. Chapter X's Warmth row now reads "Advantage", so both copies stay identical. 03 (*Orthaen Gift* "Grow a Charge" and *Crystal Charges*) and 11's intro now point to Player Handout 3 (chapter VIII). 03's six charge names are reset to italic Title Case. No player-facing chapter (03, 11, the handouts) points into chapter X. INVENTIONS #59 records the relocation. *Note:* until T2.5 renames the old "Handout 3 — The Rumor Table" to a DM table, 08 has both "Handout 3 — The Rumor Table" and "Player Handout 3 — Crystal Charges". This is as the task specifies.

**Skipped sites:** none. Every quoted phrase was found.
- Phase 1 committed ef02a28 (459→452 hard hits). New owner Q23: Agenda 4 'Veier alone' vs Raunu at the dinner.

## Phase 2

*2026-10-03, Worker. Architecture: T2.1–T2.6. Every edit was located by quoted text (DESIGN §2). New sentences say "the DM"; existing "MM" is left for T4.1.*

**Commands, after every task:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`; and, after T2.1 and T2.4 (flow.json changed), `python conversions/dnd5e/oraga_night/flow/build_flow_page.py`. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 124 passed. The flow page rebuilt without errors.

**Hard hits: 452 → 436** (T2.1 452 → 452; T2.2 → 446; T2.3 → 444; T2.4 → 440; T2.5 → 437; T2.6 → 436). **Structure hits: 2 → 1** (the broken 09 xref is fixed; the untriggered 05 gate box remains for Phase 5). **Re-baselined twice**, both after legitimate moves, and both times after confirming the total hard count had not gone up: after T2.1 (452 before, 452 after; the moved agendas carried 2 MM and 2 gp hits and their soft counts from 03 to 02), and after T2.4 (440; the MM Note moved from 04 to 09 carried 1 MM and 1 "the players" into 09, and the cut in 05 raised its em-dash rate from 16.96 to 17.29/1k because the cut text had fewer dashes than the rest).

**T2.1 (Q2, O6, FRONT-1, FRONT-8).** 03 *The Agenda System* and *The Eight Agendas* cut and pasted unchanged as `## The Eight Agendas` at the end of 02, after *What the Module Never Says* (inside the DM-only half). The *Agenda System* text is the section's opening; its own heading is dropped (nothing pointed to it). FRONT-8 fixed in the moved text: "Three of the eight agendas have a patron who is also one of the night's snakes, and a fourth, the Thenya's, has a patron who can become a fight. That overlap gives the player a vantage point." 03 keeps `## Agendas` with the player-safe paragraph (pointing at "Player Handout 2, chapter VIII", since T2.5 renames the handout), and its *Making Characters* bullet now ends "the agenda cards are in chapter VIII" instead of "the agendas are below". Re-pointed: 08 Handout 2 note, 09 S12 ×2 (now '(see chapter II, "The Eight Agendas"…)'), the 01 prep-box routing line (adds "the full agendas are in chapter II"), README rows for 02 and 03, the 8 agenda nodes in flow.json (→ `02_The_World_and_the_Night.md#the-eight-agendas`), and INVENTIONS source cites #29, #33, #58. *Checked, not changed:* 11's intro "as Chapter III requires" is about the tribe rule in 03 *Making Characters*, not the agendas; 01's "the table at the end of Chapter III" is the Ready-Made Guests table, still in 03; 06/07/08/10/11's other Chapter III pointers are about gifts. 03 now has no "At midnight" line; "The Eight Agendas" heading exists only in 02.

**T2.2 (FRONT-3, -4, -5, -16, -17, -18, -19).** In 01: `## Adventure Background` after *What This Adventure Is*, FRONT-3's draft with one change ("his last ward" → "the one charge left in his last and best preparation", 02's own words) and the pointer '(see chapter II, "The Truth of the Night")'. Prep-box step 2 now reads Chapter II "What the Module Never Says" and "The Eight Agendas" (5 minutes), with the truth pointed at *Adventure Background*. **Overview**: seven one-liners before Table I–1, from FRONT-4, with two corrections against the sources: IV "is served on two plates" → "gathers two plates" (04 Mv IV), VII "hold the front gate until the last bell" → "hold the outer gate (S3) until it is decided, and then the last bell rings" (08 midnight rules); III "at least one player character" → "at least one of the characters" (soft count). *How This Module Is Written* moved to just after *What You Need* and rewritten as **Reading This Book** to STYLE_5e: read-aloud = indented italic after a plain trigger line, non-indented italics are DM notes; bold creature = Chapter X block; keyed rooms B0–B13; fight cards S1–S14 (FRONT-7's wording, "the original five" gone); clocks "most have four segments; each card says how many"; italic Title Case spells and items; 5.2.1 capitals; full check form; the §3 cross-reference form; the box list (Sidebar, DM Note, Troubleshooting, ⟨If History Breaks⟩, What [Name] Says, Wants/Tells/Breaks/Nastier, the run box); no code spans. Designer's note left out of the legend (Q4). FRONT-16: "designed for three to five characters of 3rd to 5th level, and built for four characters of 4th level" plus "Use the one line nearest your table; the lines are not cumulative" (09 states no stacking rule; this matches SNAKES-20's "use one line only", and the 5th-level-and-five-characters case is left to T3.3); README "The night ends at 5th level." FRONT-19: chapel Short Rest line after "which tonight they will not get" (INVENTIONS #47 already covers the fact). FRONT-18: "runs at a 2014 table with the notes marked *At a 2014 table*; only the pregenerated characters need rebuilding"; the 2014 gift rule added to README *Changes from the SRD*, and 03's aside set to FRONT-18's wording ("a gifted human takes the gift as a bonus feat at 1st level", dropping "in place of whatever else the MM allows a human") so the two agree. "Mirror Master (MM)" removed ("the DM calls 5th level"). INVENTIONS **#60** (Background) and **#61** (Overview) added with sources. *Deviation:* the task's accept list puts *Reading This Book* before *What You Need*; its step 3 and FRONT-5 say "just after What You Need". Step 3 was followed. 01's H2 order now: What This Adventure Is, Adventure Background, What You Need, Reading This Book, The Night in Seven Movements (with the Overview).

**T2.3 (FRONT-11, -20, O8).** README *Contents* is now three tables under **Before the Night** (01–03), **The Night** (04–06) and **Appendices** (07–11, with an "Open it when…" column and a line saying VII–XI are the appendices), then `### For Contributors` holding README, STYLE_5e.md (new row), INVENTIONS and flow/. *Changes from the SRD* now also lists the four table rules: one DC ladder, success at a cost, NPCs don't roll outside a fight, nonlethal blows from any attack. 08's H1 is "VIII. The DM Sheet, the Palace and the Handouts".

**T2.4 (FRONT-9, SNAKES-28, NIGHT-8, SNAKES-25, BESTIARY-19; Q21).** Renames: 05 `## Knives in the Dark` → `## The Snakes in the Dark` (and the chapter lead "the knives in the dark" → "the snakes in the dark"); 09 card → `## S2. The Service Corridor Job`, Table IX–3 row too; 01 *The Fights* "Knives in the dark (S2)" → "The service corridor job (S2)". Pointers updated: 04 ×3 (two rewritten, the third went with the trim), 05 ×3, INVENTIONS #5/#7/#11/#15, flow.json (S2 label; six `kd-*` refs → `#the-snakes-in-the-dark`). 08 had no pointer to the section. The broken 09 S7 xref now reads '(Chapter IV, "The Snakes This Movement — IV", points here, and so does the Movement V box.)'. Rules list: 01 keeps its framing paragraph, then "Chapter IX runs them by three rules (see chapter IX, "The Snakes in the Pen"), and one more thing holds tonight:" and only the Attendant bullet; the other three bullets are gone, and the prep box says "the rules for steel" (was "the four rules"). 09's "(the same three Chapter IV runs them by)" was dropped, since 04 no longer lists them. Fracture: 10's copy is now a compression of 05's ("an action in a fight, or one beat out of one"; "carry for the rest of their life. The DM chooses which."; retry "once the party has witnessed a new tell") with a pointer to chapter V, "The Fractures". **Q21 cuts:** 04 *The Snakes in the Pen* is now one pointer sentence plus Table IV–1; its MM Note "how many snakes to show" (table craft found nowhere else) was **moved unchanged** to 09 *Running the Snakes* rather than lost. Table IV–1's Movement V posts reconciled with 09: Draunel "in B3; his duelists on the upper terrace (B5) for the appointment"; Boranis "Vorlain in B3, drinking harder; the cousins' blades on the upper terrace (B5)". 05 *The Snakes in the Dark* keeps its intro, the heat paragraph, Table V–7, a four-line card pointer list (S12, S8, S13, S11), the Thenya subsection (no card exists for it, so it stays) and the MM Note "which knives to show" (unique table craft). Cut: the Circle, Church, Draunel/Boranis and Phern subsections (~1,200 words). The cards carry their substance. A few narrative lines that were only in 05 are now gone: Corval on the stairs counting his staff (Movement VII has it); the inquest finding an empty drawer; "That is how his offer in the aftermath starts" (06 *Vorlain's offer* has the offer). The cut text is kept in the session scratchpad and recoverable from git (ef02a28). *Left alone:* 04 "A fight here is knives in the dark" (prose, not a title); the linter test fixture `tools/fixtures/module/09_The_Snakes.md` keeps its old S2 title. flow.json node labels "Knives: …" were not renamed.

**T2.5 (CAST-8, -9, -25, -26, -27).** Old "Handout 3 — The Rumor Table" → `## Rumors at the Ball *(DM table)*`, Table VIII–7 unchanged. The DM sheet → `## The DM Sheet — the Night on Two Pages *(the night-tracker)*` (alias kept, since 05 and 09 point to "the night-tracker"), split into `### Page One: The Night and Midnight` (Tables VIII–1, VIII–2, the pillars) and `### Page Two: Rules, DCs and Costs` (midnight rules, Tables VIII–3, VIII–4). *Deviation:* the task says split "at *The pillars*", and CAST-26 says page 1 = Tables VIII–1 and VIII–2, page 2 = midnight rules, DCs, costs. The pillars line sat after the midnight rules, so it was moved up to close page 1, which meets both. The palace diagram's three B5 boxes are now one "B5 THE GARDENS" box with the river gate, lower garden and terraces as labels inside; the garden-stair link and the B2 joint are kept. Handouts grouped at the end of 08 under `## Player Handouts` (with an italic line saying only the italic trigger lines are DM text): `### Player Handout 1: The Invitation` (CAST-9 trigger line added above the existing italic line; invitation text untouched), `### Player Handout 2: Agenda Cards` (its note now reads as a trigger: deal in the first five minutes, one card to each player), `### Player Handout 3: Crystal Charges`. Pointers: 01 "one-page MM sheet" ×2 → "two-page DM sheet"; 08 intro rewritten (two sheet pages, then the palace, tracker, standings, rumor table, handouts); STYLE_5e.md's Handout 1 reference renamed. 03 and 11's "Player Handout 3" pointers still resolve. The handouts carry no DM parentheticals or "Roll" text (the rumor table, which did, is now a DM table).

**T2.6 (FRONT-15, -23).** 06 *Ending the Session*: steps 2–3 cut to "2. If you ran the epilogue in chapter V, you have already asked the question and called 5th level. If you skipped it, do both now." The 5th-level paragraph is kept as its own paragraph. The trail's carter check → "a DC 15 Charisma (Persuasion) or DC 15 Intelligence (Investigation) check". New `## Rewards`: Table I–4 / 5th level by milestone; agenda **Pays** lines (100 GP, 30 GP, the Church's favor as a pointer only pending Q15, the grandmother's crystal); chapter X "The Night's Loot"; the carried-out answer as the story award.

**Skipped sites:** none. Every quoted phrase was found. **TODOs:** none new. Open, for the owner: the narrative lines lost in the 05 cut (listed under T2.4) — say if any should be restored to a card.

## Phase 3

### Phase 3a — T3.4 (chapter X), then T3.3 (chapter IX)

*2026-10-03, Worker. Every edit was located by quoted text (DESIGN §2). New sentences say "the DM"; existing "MM" is left for T4.1. SNAKES-17's "drop Utilize" is overruled by DESIGN §3, so Utilize stays.*

**Commands, after each task:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`. flow.json was not touched, so the flow page was not rebuilt. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 135 passed (124 + 11 new). No re-baseline.

**Hard hits: 436 → 432** (T3.4 436 → 435; T3.3 → 432, with deadly_budget 2 → 0). Structure hits stay at 1 (the untriggered 05 gate box, for Phase 5). Soft metrics did not regress. 09: "player character" 71 → 66, em dashes 10.22 → 9.18/1k. One near-regression was fixed during the work: a TODO comment phrased as a question tripped 09's rhetorical-question count.

**T3.4 — test first.** `bestiary_check.py` gained `fixed_value_problems()`. It checks that every CR line's XP and PB match the SRD table, that Kovaun's data and text carry CR 1/2 (XP 100; PB +2), and that the Wept's base block makes no more than 2 attacks a turn (`attacks_per_turn()`: Multiattack count plus any trait attack that does not "count toward" it). It also gained a `--file` option, and the run code moved into `main()` so pytest can import it. Red first: against the Phase 2 text (`git show HEAD:…/10_Bestiary.md`) it reported 3 mismatches (Kovaun data, Kovaun text, the Wept at 3 attacks). Green after the edits. The data was updated: Kovaun `cr="1/2"`, and the Wept's DPR is 56 (2 × 28), not 84. New `tools/test_bestiary_check.py` has 11 tests (hit, miss and edge for both helpers, plus `main()` exit codes).

**T3.4 edits (10):**
- BESTIARY-2: *She Arrives*. One of her Multiattack's two attacks on arrival, which counts toward it and is never a third (O24).
- BESTIARY-3: the *Call the House* trigger is "Bloodied, and no guard has called the house this scene".
- BESTIARY-4: Kovaun is CR 1/2 (XP 100; PB +2), in the block and in Table X–1 (O20). Mirror: the 09 *Who they brought* line reads "(CR 1/2)".
- BESTIARY-6: *The Post* now gives the success clause.
- BESTIARY-9: "A trick earns Delay when its check succeeds (the DC is 13, or 15 if it has already worked on that Uninvited tonight), and never a third time (see chapter V, "Buying Time")". *Note:* the check is "whatever skill fits", so it has no fixed ability. It is phrased "the DC is 13" so as not to add a bare-DC lint hit; T4.3 settles the generic-check form module-wide.
- BESTIARY-17: the Attendant's *Put Aside* reads "*Success:* Half damage." "Its magic is real; it rarely cares to use it" moved to *Before Midnight*. Kovaun's flavor Success clause is dropped (2024 omits it).
- BESTIARY-18: *Two Turns*. The second turn falls last in the round if its count is below 1, and *Put Aside* recharges only at the start of its first turn.
- BESTIARY-20: "*Built on the SRD guard.*" on the Sect Guard. "A guest" uses the SRD 5.2.1 **commoner** without its attack.
- BESTIARY-22: Veier's line is now on format (Speed 30 ft. (15 ft. tonight); *Ranged Attack Roll* … *Hit:* … damage).
- BESTIARY-23: Table X–3 caption "All are consumable Wondrous Items; none requires attunement." **TODO-Q15** comment on the coat.
- BESTIARY-24: the optional one-liner ("Their challenge ratings describe how hard they hit; nothing tonight stops them.").
- SNAKES-1/-23 mirrors: the Phern Bodyguard *Nastier* is S-3's wording ("the crowd check's DC rises to 15"). Draunel's *Nastier* now has a third duelist, which matches S13's 5th-level line (1,800 XP). Was "two duelists".
- **Gated, left as is:** BESTIARY-11 Vell (**TODO-Q8** comment under the "cannot be fought" line); BESTIARY-21 (**TODO-Q18** comment under the type lines of the Hollow, the Radiant, the Wept and Vell).
- *Not done here, by design:* the stat-block layout (BESTIARY-5/12/13/14, T4.4), capitals and item italics (BESTIARY-7/16, T4.2), bare DCs (BESTIARY-8, T4.3), "you" (BESTIARY-10, T7.5).

**Kovaun → S8.** S8's total **does not change: 800 XP, now labelled under Low.** Kovaun is in the chapel, not in the fight; the roster is four wardens. BESTIARY-4's "700" assumed she was one of the four. Logged as O20.

**T3.3 edits (09; mirror in 08 Table VIII–5, which is the tracker; the task's "VIII–7" is the rumor table since T2.5):**
- SNAKES-1: the heat-4 bullet points to each card. *At heat 4* lines on S8 (dark), S10 (new, O23), S11, S12 and S13. 08's tracker note says "each card's *At heat 4* line says how".
- SNAKES-2: the tracker rows (Boranis: a cousin beaten in public (S6), S9's clock filled, "Vorlain baited, or got drunk, by one of the characters"; Church: −1 if the wardens are turned back (S8); Draunel: "Agenda 3, if one of the characters carries it", S9's clock filled). Mirrored in 08.
- SNAKES-3: the duelists (S9, S13, and 10's *Breaks*) break "the first time one of them takes damage". S7's budget line now says "when the first of them is Bloodied", which matches its Morale. grep "real wound" = 0.
- SNAKES-4: *Detection* lines on S2 (Tavva, Passive Perception 16), S7 Movement V (knives, 13), S8 (wardens, 13, with Advantage in the dark) and S10 (the corner slinger, 13). A *Surprise* bullet in *Running the Snakes*.
- SNAKES-6: every Inspiration award names its Table I–3 row. The S3 wicket fallback and the S9 "answered Essin" award are cut. S8 reads "by an out". S13 reads "without a fight".
- SNAKES-7: **DM Note — at a 2014 table**. SNAKES-8: "Deadly" is gone (Table IX–3, the S14 budget).
- SNAKES-9: the S10 heat gate in *Where and when*. The Table IX–2 header is "What heat 3–4 sets off".
- SNAKES-12/-21/-26: a **Treasure** line on every card, with values inlined from chapter X (Tavva's sack 2d6 × 25 GP, the purse 3d6 × 10 GP, a knife's advance 2d6 GP). Missing Tactics and Morale added on S4, S5, S6 and S12. The losing-side Development added on S4, S5, S6, S11 and S14. Every Rewards line reads "divided equally among the characters". The field-order line is updated.
- SNAKES-20: "Use one line only; the lines are not cumulative", plus the 5th-level-and-five-characters rule. All 14 *Scaling* blocks are renamed **Adjusting the Encounter** (Table IX–1's title is kept).
- SNAKES-22 (S13 half): "The man reaching for his knife is Essin Boranis."
- SNAKES-23: S7's fourth knife (the DM places him out of sight; the audit's "at the far door" was not used, because it is a new detail); S5's 3rd-level line says why it differs from S2; "Tavva's two Knife attacks"; S14's "ability check with the skill that fits the trick" and the "Argue its orders" check form.
- BALL-16 (09 side): S4's base is **two** guards, matching 04 (O21). Movement I gate added to *Where and when*; Development reads "Return to the current Movement"; Table IX–3 reads "Mv I–V". S10's guard bullet follows.
- **Budget labels (O22)** against Low 1,000 / Moderate 1,500 / High 2,000: S1 200 under Low; S2 600 under Low; S3 1,500 Moderate, 2,600 over High; S4 900 under Low (2,700 with the four); S5 600 under Low; S6 600 under Low; S7 800 under Low; S8 800 under Low; S9 850 under Low / 300 far under / 1,150 between Low and Moderate; S10 1,000 Low; S11 625 under Low; S12 600 / 800 under Low; S13 1,350 between Low and Moderate (plays Moderate), 750 under Low, 2,100 over High; S14 3,900 beyond High, nearly twice High. A *Running the Snakes* sentence gives the vocabulary, and the "label" bullet now says the label is the sum and the following line is the play.
- STYLE_5e.md: the difficulty example "800 XP — Low" was arithmetically false and now reads "1,000 XP — Low" / "800 XP, under Low".
- **Gated, left as is:** SNAKES-5 (**TODO-Q14** comments in *Running the Snakes* (Outs), S4 and S14); the S9 figure (**TODO-Q12** under the S9 box); S13 *Broker a trade* (**TODO-Q11**).
- Ledger: INVENTIONS **#62**. Decisions: DECISIONS **O20–O24**, numbered from O20 to leave O9–O19 for the other Phase 3 tasks.

**Skipped sites:** none. Every quoted phrase was found. *Left for later phases:* SNAKES-10/-11 (voice, T7.3), -13/-16 (T5.4), -14/-18/-19 (T4.3), -15/-24 (T4.5), -17 capitals (T4.2), -25 (done in T2.4), -27 (a house choice), -28 (T2.4).

### Phase 3b — T3.2 (chapter V), then T3.1 (chapter IV)

*2026-10-03, Worker. Every edit was located by quoted text (DESIGN §2). New sentences say "the DM"; existing "MM" is left for T4.1.*

**Commands, after each task:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`. flow.json was not touched (no heading was renamed, and S1's flow node is already phase m2), so the flow page was not rebuilt. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 135 passed. No re-baseline.

**Hard hits: 432 → 424** (T3.2 432 → 431; T3.1 → 424, mostly bare DCs gone with the 04 ladder pointer and the thieves' tools checks). Structure hits stay at 1 (the untriggered 05 gate box, for Phase 5; not touched). Soft metrics did not regress. Near-regressions fixed during the work: 05's *Invoking a Fracture* went over 120 words (split at "Intimidation never works"). In 04, B1, the feud, and the summons paragraph went over 120 words (the gate failure, the feud timing and the audience length each became their own paragraph). The ladder ranges "DC 13–15 / DC 18–20" tripped bare_dc, so the line now points to chapter I (BALL-19's second option).

**T3.2 edits (05):**
- NIGHT-3: the beats box now says "A beat and a round cost an Uninvited the same thing: one turn" (the minute and thirty-beat scale is cut). Ward seals and floods last "until the scene ends". "perhaps" cut ("half an hour of story-time at most"; 05 *perhaps* count is now 0). New `### The Midnight Clock` after principle 4, eight steps built only from 05 and 08, plus the O9 default. Pointers to it from the beats box, principle 3, *Buying Time* ("a point is a beat"), the dais parenthetical (it no longer repeats the third-turn rule), *The last bell* and ⟨They save Raunu⟩. Table V–1 keeps the Wept's third-turn rule, because it is the Delay mechanic and not the clock. 08 page one has a one-line pointer to the clock above the pillars.
- NIGHT-4: the miss-by-4 line gives 2 Delay. A Fracture needs at least one witnessed tell. Skills carry their abilities. *Mirrored* in 10's Fracture rule and in 08's *Fractures* line.
- NIGHT-5: **Sidebar — Adjusting the Attack** at the end of *Buying Time* (O11). The crossfire sidebar's "halve / add half again" is replaced by the dice. **The values are unsimulated**; run them through the pass-2 sim before print.
- NIGHT-6: "fights the party can end on its own terms". The 2014 line was not added, because 09 already has **DM Note — at a 2014 table** (SNAKES-7).
- NIGHT-7: the lanterns note is plain text. Darkness speeds the Radiant up, except as a Fracture attempt.
- NIGHT-16: the trap-mask evidence is cut.
- NIGHT-19: the carry award reads "100 XP to the carrier for each person they bring out (Table I–4)". "as Table I–4 pays a fight ended by an out". Table V–3's "(principle 2)" → '(see "How to Run the Attack", principle 2)'. *Mirror:* 01 Table I–4 "100 to the carrier, for each person they bring out". *Not found:* the old "(*Carrying somebody out*, Chapter I)" pointers (already rewritten before this pass) and a second "principle 2" pointer at the audit's 05:1076.
- NIGHT-20: the Evasion sentence.
- NIGHT-21: the push goes "in a direction the DM chooses", with the Prone condition (mirrored in 08). The Radiant's gate turn comes at the end of the round, after every character. "nobody is surprised: everyone saw the lights die". Trampling (O10).
- NIGHT-22: the room-trick tables' column is **Check (DC 13; DC 15 the second time)**; per-row exceptions kept.
- NIGHT-24: *About 50 / 40 minutes* boxes on Movements VI and VII in 04's time-box form (from Table I–1), not the audit's italic "Expected duration" line, so both chapters match. B12 **Treasure** line (from 09 S3 and 10). The looters bullet points to '(see chapter X, "The Night's Loot")'.
- NIGHT-18: `### The Palace After Midnight: General Features` (light, crowd, smoke, fire), after *The Attendant* and before *The default beats*. It is not inside *Midnight Rules*, whose lead says "Five short rules". Sources: the lights list, *Two Hundred People*, S12, S13. **TODO-Q13** comment in place of dimensions.
- **Gated, left as is:** NIGHT-15 (**TODO-Q10** under the contract paragraph in B12); NIGHT-17 (**TODO-Q9** at the end of ⟨They trap one of the Uninvited⟩).
- *Left for later phases:* NIGHT-9/-10/-11 (T5.2, T5.3), -12 (T4.2), -13/-14 (T7), -23 (T4.6/T5.4). 10's mirror for the Fracture text was needed (T2.4c had not covered the partial-success Delay).

**T3.1 edits (04):**
- BALL-6: a failure by 5 or more at the gate, as its own paragraph. **Skipped part:** the audit's "on another guest's arm" and "he sends for a guard" are new detail. Only the printed route is used (Movement I: "staff hires slip in through the kitchens (B10)").
- BALL-7: results for the B0 first check, the B3 alcove, helping Corval well (his open gratitude, as for the feud; the audit's "see Agenda 1" was not used, because Agenda 1 doesn't say what helping *well* buys) and angling for a summons.
- BALL-8: the feud heading is "(Movement II, or III; the Banquet Galleries)", with timing per O7. "see the sidebar below" → 'see the sidebar "Guards are a scene, not a sentence", below'. *Mirrors:* 09 S1 *Where and when*, Table IX–3 "Mv II (or III)", 08 Table VIII–1 Movement III "S1 if held from II".
- BALL-9, -10, -26: O12.
- BALL-16: "four more come at the start of the second round after the first guard is Bloodied". 09 S4 already matched (T3.3).
- BALL-17: the toast can be held, and the two plates' news travels. The Dead Dance trigger line says who hears the whole box.
- BALL-18: thieves' tools as "a DC 15/18 Dexterity check using thieves' tools" (B5, *Trespass*, B8). 08 Table VIII–3 "15 / 18 Dexterity (thieves' tools)". The open-skill checks get a default ("usually Charisma (Persuasion) or Intelligence (Investigation)").
- BALL-19 / CAST-19: see the ladder note above. 04's header box already reads "Hard DC 18–20".
- **Gated:** BALL-12 (**TODO-Q15** comments at Callun's Movement III coin and the nursery sale; there were none in 04 before).
- **Phase 1 leftover fixed:** the Movement III time box still listed "the quiet guest answering the time", the habit cut by Q5/O3. It now ends "and the gray masks".
- Ledger: INVENTIONS **#63** (T3.2) and **#64** (T3.1). Decisions: **O9–O12**.

**Skipped sites:** listed above (BALL-6's two new details; NIGHT-19's two pointers no longer present; NIGHT-6's 2014 line, already in 09). **TODOs added:** Q9, Q10, Q13 (05); Q15 ×2 (04).

### Phase 3c — T3.5 (chapters VII, VIII and XI)

*2026-10-03, Worker. Every edit was located by quoted text (DESIGN §2). New sentences say "the DM"; existing "MM" is left for T4.1.*

**Commands:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`. flow.json was not touched. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 144 passed (135 + 9 new). No re-baseline.

**Hard hits: 424 → 418.** Structure hits stay at 1 (the 05 gate box, for Phase 5). Soft metrics did not regress. Near-regressions fixed during the work: Callun's line moved a bare "**DC 25**" to a bare "**DC 20**", which the per-key comparison counts as a new hit, so it now reads "takes a DC 20 Charisma (Deception) check". Veier's *At the Unmasking* paragraph went over 120 words with the 60-foot clause, so *At the table* became its own paragraph. The 2014 note's "18, not 19" tripped the not…but count in 11 and was rephrased.

**Test first.** `pregen_check.py` was refactored so pytest can import it (argparse moved into `main(argv)`, a `--file` option, the legality loop into `legality_issues()`), and gained `focus_issues()`: the pregens in `FOCUS` (Andra) must print "a crystal as arcane focus" in the Spellcasting line and "crystal (arcane focus)" on the Carrying line. New `tools/test_pregen_check.py` has 9 tests (clean module, clean minimal sheet, missing from Carrying, lattice as focus, wrapped lines, missing section, another pregen's Carrying doesn't count, `main()` exit 0 and exit 1). Red first: the two module-dependent tests failed on the Phase 3b text ("the lattice as focus"; no focus carried). Green after the 11 edits.

**T3.5 edits:**
- CAST-3: 07's intro gives the default ("Where an entry gives no DC, the DC to move that guest is 13 behind a mask (the ladder in chapter I); the entries below note only the exceptions"); "The MM sheet (Chapter VIII)" → "The DM sheet (chapter VIII)". The Sergeant's negotiation surface gains "**Voiding the contract:** a DC 13 Charisma (Persuasion) check; see card S3" (from 09 S3, out 2). O14.
- CAST-4: Vell: "every Charisma check to move Vell (Deception, Intimidation or Persuasion) **DC 25**, and let even a success buy honesty"; the nudge: "A character who studies him directly can make a DC 25 Wisdom (Insight) check to notice the nudge; on a success, they learn…". "An exceptional will" is gone. 08 Table VIII–3: "25 · 25 Charisma".
- CAST-11: Andra's Spellcasting line reads "a crystal as arcane focus"; "crystal (arcane focus)" added to Carrying. O15. **Ilesse gated:** `<!-- TODO-Q16 … -->` under her Spellcasting paragraph.
- CAST-12: the 2014 note rebuilds ability scores too ("a 2014 standard-array human cannot reach the 19s on these sheets") and says "The gift is the variant human's feat (chapter III)", matching 03 and README.
- CAST-14: Table VIII–3 rows: B0 "13 Charisma (Persuasion) or Wisdom (Insight)" (04 B0 DM Note); "10, the check that fits the approach" (04 *Social checks*); "15 / 20 Wisdom (Insight)" (03). The thieves' tools row was already done in T3.1.
- CAST-19: Callun's money DC 25 → 20 (O13). 04's "Hard DC 18–20" was already done in T3.1.
- CAST-20: "Five factions came as Raunu's enemies (the snakes), and a sixth, the Thenya, came as his wife's kin; each has a threat line and fight cards in chapter IX".
- CAST-21: "**Dassa (AC 16, 40 Hit Points) and Pello (AC 16, 31)**".
- CAST-22: Arcane Recovery "Once per Long Rest, when she finishes a Short Rest, recovers spell slots totalling 2 levels". Fast Hands in the verified SRD 5.2.1 wording: "Bonus Action: a Dexterity (Sleight of Hand) check to pick a lock, disarm a trap with Thieves' Tools or pick a pocket; or the Utilize action; or the Magic action to use a magic item, a crystal charge included". Veier's *For Them*: "while within 60 feet of her" (03).
- Ledger: INVENTIONS **#65**. Decisions: **O13–O15**.

**Skipped sites:** none. Every quoted phrase was found. **TODOs added:** Q16 (11, Ilesse). *Note:* "Thieves' Tools" is capitalized in Fast Hands as the SRD prints it; the rest of the module still has "thieves' tools" lowercase (for T4.2 to settle).

## Phase 4

### Phase 4a — T4.1 MM → DM (owner Q1) and T4.6 spelling (Worker, 2026-10-03)

**Commands, after each task:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`; `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`; `python conversions/dnd5e/oraga_night/tools/pregen_check.py`; `python -m pytest conversions/dnd5e/oraga_night/tools -q`; `python conversions/dnd5e/oraga_night/flow/build_flow_page.py` (flow.json changed in both tasks). Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 144 passed. Flow page rebuilt without errors. `git diff --stat adventures/` empty. No re-baseline.

**Hard hits: 418 → 355 (T4.1) → 304 (T4.6).** role_name 63 → 0; british_spelling 36 → 0; grey 15 → 0. Structure hits stay at 1 (05 gate box, Phase 5). Soft metrics did not regress. No whitelist entries added.

**T4.1 edits** (62 lines, each edited by quoted phrase from the lint hit list, no global sed):
- "MM Note" → "DM Note" (02, 04, 05 ×2, 09 ×3); "MM sheet" → "DM sheet" (01 ×4, 04 ×2, 05, README); "MM ONLY" → "DM ONLY" (02 *The Truth of the Night* heading); "MM only" → "DM only" (07 Attendant); "(MM: …" / "(MM truth: …" → "(DM: …" / "(DM truth: …" (02 agenda 8, 03 Thenya Gift, 07 Vell ×2).
- Third person kept as "the DM" in player-facing text (03 ×4, 11 ×7, 02 agenda cards) and in Chapter X traits (10 ×4), in 01's heading (now "What the DM Knows (And What the DM Doesn't)", with its pointer "*What the DM Knows*"), 05's "the DM's choice" (after "their choice" for the characters), 07 "left them to the DM", 09 "the DM's invention" and 09 Tavva's trade ("the DM picks two", where "you" already meant the characters), and flow.json node 205.
- "You" where the sentence instructs the DM: 01 Troubleshooting head ("you keep defaulting to DC 20"); 04 B11 parenthetical ("Know this geography cold"); 05 ("you pick", "you say which", "You choose which", "you choose", "you should welcome that"); 07 ("so you know what she does"); 09 ("You name who did it", "you pick which, and say which, out loud", "(your call)", "you do not have to be subtle", "you say who did not get out", "you describe the sound", "(you roll who, in the open)", "you narrate who").
- Undeclared "**MM —**" leads became the declared species "**DM Note —**" (05 B12 "what you must not say", 07 factor box, 09 Attendant "how to hint that it can be distracted"). 01 "One MM tip above all others" → "One tip above all others".
- INVENTIONS #55: "MM-only" → "DM-only" (describes current text). Historical mentions (R1 "MM background", #10, #23) left as ledger history.
- No "Mirror Master" occurred in M/. flow_page.template.html had no hits.

**T4.6 edits** (63 word changes across 01, 04–07, 09–11, README, flow.json):
- Lint list: colour(s) → color(s), rumour → rumor, centre/centred → center/centered, labelled → labeled, recognise(s) → recognize(s), organised → organized, honour(s) → honor(s), favour/favourite → favor/favorite, defence/self-defence/offence → defense/self-defense/offense. Also beyond the lint list: totalling → totaling (11), fulfil → fulfill (07), licence/Licence → license/License (README, incl. the heading; no anchor points to it), pretence → pretense (01, 07, flow.json), savours → savors (10), memorise → memorize (09 ×2). Read-aloud was included: the spelling rule says "everywhere" and the lint grey/spelling rules scope ALL. No hit was in canon NPC speech (09's "throws colours" is a player example line). Handout 1's canonical text had no hits.
- **Gray, and INVENTIONS #43:** #43 is an edition invention awaiting owner review ("Nothing here is settled until the owner approves"); its Canon column cites the written-word law and Kovaun's role, not the robes. The Facets edition (`adventures/oraga_night/`) never says "grey robes" and itself mixes "gray masks" and "grey coats". So "grey robes" is not fixed canon wording: "gray" everywhere (robes, coats, Callun's iron-gray, the Bought's Gray wool), no whitelist entry. INVENTIONS itself was not swept (STYLE "Do not touch" #3).
- NIGHT-23 slips (05, located by quote): "slingers standing in its sight" → "his sight" (Maiven/Radiant); "the pale factor stops being unmemorable" → "Master Vell stops being unmemorable"; "Two of her knives hit the trophy gallery (B7); the others work the" → "…; she and the third work the" (S5 and 09 give Tavva three Gallery Knives). 09's "within its sight" is the Attendant and stays.

**Skipped sites:** none. Every quoted phrase was found.

### Phase 4b — T4.2 SRD 5.2.1 capitals, spells, items, coin (Worker, 2026-10-03)

**Commands:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --report` (before and after), `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`, `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`, `python conversions/dnd5e/oraga_night/tools/pregen_check.py`, `python -m pytest conversions/dnd5e/oraga_night/tools -q`. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 144 passed. flow.json not touched. No re-baseline. No checker parser depended on a casing that changed (pregen_check reads `**Armor Class**`, `**Hit Points**`, `**Initiative**`, `**Passive Perception**`, the Spellcasting focus and the Carrying line; none of those strings changed), so no tool or test edits.

**Hard hits: 304 → 210.** lowercase_terms 84 → 0; gp 10 → 0. Structure hits stay at 1 (05 gate box, Phase 5). Soft metrics did not regress. No whitelist entries added.

**Method.** About 185 explicit quoted-phrase replacements in 01–05 and 07–11 (06 and README had no hits). Each one was checked to match exactly once (or a stated count) before it was written. The lint hit list was the starting point, plus greps the lint does not cover: condition phrasing, Speed, action names, Darkness as a light term, Thieves' Tools, every SRD 5.2.1 spell name (pulled from the SRD extract and matched against the module), and every crystal-charge name. No global sed.

**Edits by kind:**
- *Rules terms:* Advantage/Disadvantage, Hit Points/Hit Point, Short Rest/Long Rest, Speed/Climb Speed, Difficult Terrain, Dim/Bright Light, Darkness (as the light term: 05 "the corridors are Darkness", 10 "Magical Darkness"), Darkvision. I also capitalized these SRD 5.2.1 Title Case terms when they are used as rules: Initiative (01, 05, 11), Death Saving Throw(s) (04, 05, 08, 09, 10), Bonus Action, Reaction(s), Concentration, Critical Hit, Opportunity Attacks, Proficiency Bonus (11, 05).
- *Conditions:* "falls unconscious and is Stable" → "is Unconscious and Stable" (04; 05 "is **Unconscious and Stable**"); "unconscious and stable" → "Unconscious and Stable" (04 brawl). "lands Prone", "and Prone unless…", "(1d6 Bludgeoning, Prone…)" → "…with the Prone condition" / "…and the Prone condition" (08, 09 ×5). 10: "While Blinded" → "While they have the Blinded condition"; "knocked Prone" → "given the Prone condition"; "is Grappled or Prone" → "has the Grappled or Prone condition"; "can't be charmed, frightened, put to sleep…" (×3) → "can't be Charmed, Frightened, put to sleep…"; Vell "can't be grappled, restrained, charmed, frightened" → capitalized.
- *Spells:* italic Title Case everywhere they occur (01, 02, 03, 04, 05, 09, 10, 11), including 02's bare "a counterspell" → "*Counterspell*", the 03 gift list (one italic run split into eleven spells) and the 03 pregen table, and the 11 spell lists (they were roman lowercase; now each spell is italic Title Case). *Power Word* and *Dominate* (10, not SRD spell names as printed) follow the same form.
- *Crystal charges* (BESTIARY-7, CAST-13): one form, italic Title Case. 10's Table X–3 first column went from bold to italic (10 rows). Italicized: 10 "Steady Light" ×2, "a Dark-Burst" (spell table), *dark-burst*/*door-seal* → *Dark-Burst*/*Door-Seal* (×5); 05 House Seal/House Flare (×3, NIGHT-12); 11 every charge on the Carrying lines (*steady light* → *Steady Light*, etc.). 03 and 08 already matched. 10's italic DM note "*A Dark-Burst released where…*" keeps the name roman inside the italics.
- *Coin:* "gp" → "GP" (02 ×2, 03, 08 ×2, 11 ×5).
- *Thieves' Tools:* 04 ×3, 05, 08 ×2, 09, 11 ×2.
- "Utilize" kept (09, 11).

**Left alone, on purpose:** read-aloud boxes and quoted speech (no rules term in them was used as a rule); ordinary English: "darkness" in description (01 "darkness, fire, terror", 04 "near-darkness", 05/10 "not by darkness or doubt"), "speed" meaning haste (02), "frightened"/"charmed"/"poisoned" as plain adjectives (02, 04, 05, 07, 09), "can be charmed into" (04 cellar hand, 05 errand), "a sealed door" and "Hold a sealed door" meaning a door Veier's wards sealed (05), "silence", "fear", "light" and the like where they are not spells. "can't be surprised" stays lowercase (SRD 5.2.1 uses both forms). Damage types in the pregens ("1d4 + 2 piercing") and the bare skills in Table VIII–3 belong to T4.3. Stat-block AC parentheticals belong to T4.4.

**Noted, not done (scope):** SRD 5.2.1 also Title-Cases equipment and tool names (Longsword, Studded Leather, Disguise Kit, Gaming Set, Jeweler's Tools, Component Pouch, Arcane Focus). DESIGN §3 lists only Thieves' Tools, so the rest stay lowercase. Changing "arcane focus" would also need `pregen_check.py`'s FOCUS string changed, test-first. A candidate for a later sweep, if the Planner wants it.

**Skipped sites:** none. Every quoted phrase was found.
