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

### Phase 4c — T4.3 check, save and damage grammar; numerals; O16 equipment names (Worker, 2026-10-03)

**Commands:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --report` (before and after), `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`, `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`, `python conversions/dnd5e/oraga_night/tools/pregen_check.py`, `python -m pytest conversions/dnd5e/oraga_night/tools -q`. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 145 passed (one new test). No re-baseline. flow.json not touched.

**Hard hits: 210 → 48.** T4.3 families: bare_dc 134 → 0, roll_check 5 → 0, save_damage 10 → 0, spelled_distance 13 → 0 (S3–S13, S37), outside the whitelist. The 48 left are conversion_talk 33, narrator_voice 11, designer_we 2, pcs 1, designers_note 1 (later tasks). Structure hits stay at 1 (05 gate box, Phase 5). Soft metrics did not regress (one transient 07 "not…but" regression from "not even a high DC" was reworded away).

**Whitelist** (`tools/lint_5e_allow.txt`, 11 entries, 19 hits suppressed): ten open-skill checks written "an ability check using the skill that fits, DC N" (01, 03, 04 approach across station; 05 room trick and Attendant distraction; 08 DM-sheet compressions of the room trick, the distraction and the Fracture; 09 and 10 Attendant distraction), and one SRD form, `10_Bestiary.md|Grappled condition (escape DC` (the SRD's own "(escape DC N)", 28 uses in the extract; 4 hits).

**Method.** Quoted-phrase replacements, each asserted to match exactly once before writing (a small apply script in the scratchpad), file by file from the lint hit list. No global sed. Plus greps the lint does not cover: alternatives missing their second DC (wrapped across lines), damage types on wrapped lines, skills named without an ability, "roll" meaning a check, "beat/miss the DC", spelled-out distances and counts.

**Edits by kind:**
- *Checks:* "DC N Ability (Skill)" → "a DC N Ability (Skill) check" throughout 01, 03–10 (SNAKES-14's 25 sites, BALL-18, BESTIARY-8's 9 sites, FRONT-14, CAST-14). Alternatives spell out both DCs (04 B3, B5 sidebar, Root Arcana/Medicine; 05 chase and smoke carry; 09 S1 crowd, S5 chase, S8 law, S10 wall, S11 crowd and Adjusting line). Ladder statements: 01 and 04 read "a DC 15 Wisdom (Insight) check", 04's 5e box gives the ladder as "Easy 10 · Standard 13 or 15 · Hard 18 or 20 · Very Hard 25" (no range), "the DC of a Standard check is 13". 04 B0 note and 01 Troubleshooting name "a DC 13 Charisma (Persuasion) or DC 13 Wisdom (Insight) check" (CAST-14's B0 source); the Troubleshooting lead is now "you keep setting every DC at 20". 04 open-skill cases (help Corval, get summoned): "a DC 13 Charisma (Persuasion) or DC 13 Intelligence (Investigation) check, or another skill if the help calls for one". 04 craft-eye: "a DC 13 Intelligence check, adding the Proficiency Bonus for anyone proficient with any Artisan's Tools". Fracture DCs written "The DC is 18 … 15" / "her Fracture's DC is 15", because the check form (skill that fits the words) is stated in the sentence before. 09 S14 Adjusting lines: "a distraction DC of 20/18". 08 Table VIII–3 cells now all name abilities ("13 / 18 Charisma (Deception)", "15 Dexterity (Stealth) · 10 Charisma (Deception) · 13 Charisma (Persuasion)", "15 Wisdom (Survival)", "20 Charisma (Deception) · impossible", "25 Charisma (Deception) · 25 Charisma (Deception, Intimidation, or Persuasion)", and "15 / 20 Wisdom (Insight or Perception)" to follow FRONT-14's 03 wording). 08's midnight-rules bullets: written out in the short check form despite CAST-14's "leave it", because T4.3's acceptance is 0 lint hits; bullets reflowed.
- *Roll / beat:* "misses its DC by 4 or less" → "fails by 4 or less" (01, 04); "beat the DC by 5" → "succeed(s) by 5 or more" (08, 09, 10); 05 Fracture results "Meet the DC / Miss by …" → "Success / Failure by …" (matching 10); "roll the ability and skill" → "make an ability check with whatever skill fits it" (10, BESTIARY-8); "no roll" → "no check" (05 ×3, 08, 10); "Guests/The crowd don't roll" → "make no saving throw(s)" (05, 10); "needs to roll to believe it" → "needs a check" (10 Callun); "Vell does not roll" → "makes no check" (10); "NPCs don't/never roll" → "make checks" (01, 04, README).
- *Saves and damage:* 09 S13 fire → SNAKES-18 template ("must make a DC 13 Dexterity saving throw, taking 7 (2d6) Fire damage on a failed save, or half as much damage on a successful one"); 09 S11 crowd → "take 3 (1d6) Bludgeoning damage"; 05 crossfire "bludgeoning" → "Bludgeoning" ×2; 05 carry "fire or bludgeoning" → Title Case; 09 "no more fire damage" → "Fire"; 09 "the smoke's Constitution save is DC 13" → "calls for a DC 13 Constitution saving throw". 10: Nastier sergeant "7 (1d8 + 3) Slashing damage" (Company Blade); untyped extra damage typed from the creature's only weapon: Paid Extra, Essin's and Tavva's Sneak Attack, Vorlain's Brief and Efficient → Piercing (SRD 5.2.1 types extra damage). 10 Put Aside reflowed so "*Strength Saving Throw:* DC 14" sits on one line. 11: pregen damage types Title Case (Piercing, Psychic, Fire, Slashing, Radiant, Force); Pello's Nick "deals 1d4 piercing" → "its damage is 1d4 Piercing"; Divine Spark → "makes a Constitution saving throw, taking Radiant damage equal to 1d8 + 4 on a failed save, or half as much damage on a successful one" (SRD wording). Falls keep bare dice.
- *Numbers:* distances to numerals in DM text: 01 and 05 "20 feet away", 05 "5 feet wide", 09 "12-foot", "5 feet wide" ×3, "15 feet above", "15-foot drop", "10 feet out", "10-foot drop" ×2, "20 feet of grown crystal"; 04 "10 minutes studying"; "3 successes before 3 failures" (04, 09). Read-aloud and table-time minutes ("the first five minutes") left as words.
- *Social traits (BESTIARY-8):* Kovaun, Essin, Maiven, Callun, Raunu, Corval, Vell now name "Charisma (Deception)" / "(Persuasion)" / "(Deception, Intimidation, or Persuasion)" with "check" in 07 and 10.
- *O16 equipment names (scope addition):* test-first. `test_pregen_check.py` changed to "Arcane Focus" plus a new test that the lowercase form is reported → 5 red; `pregen_check.py` FOCUS updated → 2 red (module text); 11 updated → green. Title Case in 11 (Spellcasting "Component Pouch", "a crystal as Arcane Focus"; Carrying: Fine Clothes, Studded Leather Armor, Component Pouch, Two Daggers, Disguise Kit, Jeweler's Tools, Breastplate, Chain Shirt, Dagger; Armor Class parentheticals; Tools and Origin-feat lines; Weapon Mastery lines; the TODO-Q16 comment), 03 "a Disguise Kit", 04 "Thieves' Tools find nothing", 09 "three Rapier attacks", 10 Draunel's Parry "his Rapier", and the 10 stat-block AC parentheticals (Chain Shirt, Chain Mail, Shield, Half Plate Armor, Studded Leather Armor, Breastplate; T4.4 will move them to Gear lines, already cased). Left lowercase: description ("a sling and shot", "his second dagger", "a greatsword on a factor's back"), non-SRD names ("crystal focus", "vehicles (land)", "chalk and a wiping slate"), "spellbook" (03, a class-feature noun). O16 added to DECISIONS.md and to STYLE_5e.md's rules-term row; STYLE's Checks row now gives the open-skill form.

**Found and fixed while here (outside the lint list):**
- 10 *Terrifyingly Numerate* still said Callun's money DC was 25; O13 set it to 20 and 07 already says 20. 10 now says "a DC 20 Charisma (Deception) check".
- 09 S14 *Distracting the Attendant* still listed "Charisma (Persuasion) to ask it a question it must answer", the habit owner Q5 removed (O3). The example was cut from the list; nothing replaced it.

**Skipped sites:** none. Every quoted phrase was found. Not done: 07 Vell's "let even a success buy honesty…" line and a few other long lines left unwrapped where the edit lengthened them (no rendering effect).

### Phase 4d — T4.4 SRD 5.2.1 stat-block layout; T4.5 cross-references and provenance (Worker, 2026-10-03)

**Commands (after each task):** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`, `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`, `python conversions/dnd5e/oraga_night/tools/pregen_check.py`, `python -m pytest conversions/dnd5e/oraga_night/tools -q`, plus `--report` before and after. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 159 passed (14 new). xref structure hits 0. `(source Ch` hits 0. No re-baseline. Flow page rebuilt (`flow/build_flow_page.py`).

**Hard hits: 48 → 36** (conversion_talk 33 → 21: the twelve SNAKES-24 provenance hits in 09). Structure hits stay at 1 (05 gate box, Phase 5). Soft metrics did not regress (one transient 09 long-paragraph regression, from "(Ch. IV, B8)" growing into "(see chapter IV, area B8)", was cut back to "(area B8)").

**T4.4 tooling, test-first.** `test_bestiary_check.py` got 13 cases (parse_gear ×2, Gear armor gives the printed AC / mismatch reported, AC parenthetical reported, parse_initiative ×2 including the 2014 "with Advantage" suffix, folded Advantage clean / suffix reported / unfolded score reported, score = 10 + bonus, bonus must be Dex or Dex + PB, and the module is clean). Red: 13 failed. `bestiary_check.py` gained `ARMOR`, `INIT_ADVANTAGE`, `parse_gear`, `parse_initiative` and `layout_problems` (wired into `text_problems`): an AC line with a parenthetical fails, a Gear line's armor (+ Dex, capped; + Shield) must equal the printed AC, and the Initiative score must be 10 + bonus (+5 for Pellin Corro and the Phern Bodyguard). Then 23 mismatches on the module text, then 0 after the edits. `test_lint_5e.py` got one classify case (an epithet line, blank, type line and a TODO comment put the AC line seven lines below the heading); red, then `classify`'s look-ahead went from 5 to 7 lines.

**T4.4 edits (10_Bestiary.md).**
- *Gear:* AC parentheticals moved to a **Gear** line before Senses on 20 blocks (armor and Shield only; weapons stay named in Actions, and How to Read now says so). "(leather)" → Leather Armor. "(vestments)" and "(festival finery)" dropped: both are AC 10 + Dex, not armor. The costume notes ("under a festival coat", "under a plain good coat", "under silk" ×2, "under border wool", "under Boranis livery") moved to each block's italic lore tail, unchanged in substance.
- *Immunities:* the Attendant's two lines → "**Immunities** Poison, Psychic; Charmed, Exhaustion, Frightened, Poisoned"; the three Uninvited "Condition Immunities" → "Immunities".
- *Senses:* semicolon before Passive Perception on the four Darkvision blocks.
- *Initiative:* Corro "+1 (11), with Advantage" → "+1 (16)"; Phern Bodyguard "+4 (14), with Advantage" → "+4 (19)". How to Read says Advantage is folded in.
- *Commentary out of numeric fields:* the Attendant's CR line is now bare; its "Focused / Idle about CR 5 / award the full XP" note moved to the block's lore tail, wording kept (the unclear "and High by the clock" dropped, BESTIARY-5). "— *but see Leashed*" cut ×3 (the trait says it). The Wept's Resistances commentary moved to her lore tail. Vell "**CR** — *(not a combatant; no XP)*" → "**CR** —", and the line under it now says he is not a combatant and is worth no XP.
- *Usage tags:* Warder "(Each 1/Scene)" → "(1/Day Each)"; Hold the Terms and the Captain's Nastier *Reform the Line* "(1/Scene)" → "(1/Day)"; Centuries of Practice "(3/Night)" → "(3/Day)" ×3; Callun "as a free action" → "at any time, no action required". How to Read defines "until the scene ends" (fight ends or the Movement changes), per BESTIARY-12, for the Sergeant's Hold the Terms and *House Seal*.
- *Bloodied:* the four "When Bloodied" sections became ***Bloodied.*** traits under Traits: the Hollow, the Radiant ("When … first Bloodied"), Tavva (BESTIARY-13's wording: Release a Charge on her next turn, a Bonus Action), and the Wept as "***Bloodied: The Sorrow Slips.***". The Fracture run-ins stay after the blocks.
- *Epithets:* split onto their own italic line above the type line on all 17 blocks that had one (Vell included).
- *BESTIARY-14:* *Blood, Not Hire* → the Cousin's Blade lore tail; *Pays Her Debts* → Kovaun's lore tail; *Stones Before Steel* → a Tell ("In a fight, uses the sling first, and aims at hands.") plus the hall-of-knives sentence in the lore tail. *The Wrapped Sword* kept.
- *Spot check vs SRD 5.2.1* (Guard, Guard Captain, Knight in the extract): field order Skills → Resistances → Immunities → Gear → Senses → Languages → CR matches on the Bought Blade, the Attendant and the Hollow. The house keeps AC and Initiative on one line with "·", and the 2014-table note stays in How to Read.

**T4.5 edits.**
- *Provenance (SNAKES-24):* all ten "(source Ch. …)" citations in 09 → "(see chapter N)" (two wrapped across a line). The "(with the source section it comes from)" clause and the "The words 'the source' mean…" sentence cut from the Six Lines note. "(Val'loh, V3)" cut (the fact is stated inline). The other 09 "(Ch. N …)" pointers → "(see chapter N …)".
- *Scripted pass, reviewed line by line* (`scratchpad/xref.py`, dry run first, 334 changes): "(Chapter N)" → "(see chapter N)" (47); "(Chapter N, *Title*)" and "(*Title*, Chapter N)" → '(see chapter N, "Title")' (30); "(B0, Chapter IV)" / "(Chapter IV, B8)" → "(see chapter IV, area B0)" (6); italic section names that match a module heading → quotation marks (46; agenda titles and the gift feats keep their italics, whole-line italics skipped); "Chapter(s)" lowercased in running text and parentheses unless it starts a sentence, a list item, a table cell or a parenthetical full sentence (206). Headings, read-aloud and code skipped; Handout 1 untouched.
- *By hand, where `classify` reads a DM box as read-aloud:* 01's prep box (items 1, 4, 5, 6) and 04's Snakes This Movement boxes (→ "*the Circle's line, chapter IX.*" ×17, "(see chapter V)", "see chapter V:"). 10 How to Read "**If It Comes to It**", "**Items of the Night**" → quotation marks. 04 "See* The Palace on Alert. *" → 'See "The Palace on Alert."'. 07 ×3 "noncombatant — *If It Comes to It*, Chapter X" → 'noncombatant (see chapter X, "If It Comes to It")'. 01 'in *What the Module Never Says* (Chapter II)' → 'in chapter II, "What the Module Never Says"'.
- *flow.json:* "contradiction of Chapter II" → "chapter II"; label "After dawn (Chapter VI)" → "(see chapter VI)"; "(Ch. IX, Table IX-2)" → "(see chapter IX, Table IX–2)". "Chapter IV says" stays (sentence start). Page rebuilt.
- *FRONT-22 / NIGHT-19:* already fixed by Phase 3 (05 now says "as Table I–4 pays a fight ended by an out", "Carrying somebody out pays as Tables I–3 and I–4 print it … 100 XP … (Table I–4)", and the ward trick cites '(see "How to Run the Attack", principle 2)'). Verified, nothing left to change. INVENTIONS #25's Where column re-pointed to 04 Undercurrent A ("A Scora reads the figure without a check"), with the retired 03 section noted.
- *Resolver:* the lint already resolves '(see chapter N, "Title")' with straight, curly or italic titles (existing fixture tests); no extension needed. All quoted titles resolve (xref 0).

**Left, on purpose:** table-header and table-cell abbreviations "*(Ch. IX)*", "*(Ch. VII)*", "(Ch. I)", "Ch. V read-aloud" in 04 Table IV and 08's runtime table (compressed table form). Tail labels "Card: S14." / "Cards: S9, S13." (labels, and the lint resolves them). "Cast: chapter VII" lowercased as a label continuation. Other conversion talk in 09 that is not provenance ("which the source leaves to the DM's invention … This edition names", "the source's plain fact", "the source notes with a straight face") and the rest of the conversion_talk/narrator family: Phase 7. Vell's "**Speed** 30 ft., and some other way" left (canon hint on a non-combat block). Some lines lengthened past the wrap width (no rendering effect).

**Skipped sites:** BALL-25 is moot (Knives renamed earlier). FRONT-22's first bullet and NIGHT-19's items: already fixed; nothing found to change.

## Phase 5

### T5.1–T5.4 — read-aloud, boxes and scannability (Worker, 2026-10-03)

**Commands (after each task):** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check`, `python conversions/dnd5e/oraga_night/tools/bestiary_check.py`, `python conversions/dnd5e/oraga_night/tools/pregen_check.py`, `python -m pytest conversions/dnd5e/oraga_night/tools -q`, plus `--report` before and after. Final results: lint `--check` OK, exit 0. bestiary_check: 25 blocks + 3 Nastier, 0 mismatches. pregen_check: 5 pregens, 0 issues. pytest: 159 passed. flow.json not touched (no flow rebuild needed). No re-baseline. No whitelist entries added.

**Hard hits: 36 → 35** (04's "unchanged" conversion talk cut with BALL-23). **Structure hits: 1 → 0** (the untriggered 05 gate box now has a trigger). Soft metrics did not regress; long paragraphs 69 → 62, "player character" 135 → 134, "you" 286 → 278, rhetorical questions 22 → 21 (module totals). Transient regressions fixed during the work: the summons questions counted as rhetorical questions in roman DM text until they were set as quoted bold run-ins; unboxing the Snakes This Movement sections exposed 5 "player character", 3 "not…" and one 124-word bullet to the soft count, fixed by "a character", light rephrasing ("and ignore the gate", "without a smile", "instead of dancing") and a paragraph break in the Movement V Thenya bullet.

**T5.1 (04).**
- BALL-3: B2, B4, B6 and B9 headers now sit above their trigger lines (header line, trigger, box, DM text). B2's DM text cut to function ("The grand hall, and the room where nearly every scheduled event happens… The walls are the palace's oldest work."; the warmth and "vault of rose-lit crystal" repeats cut). B4 drops "A smaller crystal chamber off the Court" and "Dark for two years; tonight it is lit" (both in the box); the dais clause kept as "generations of petitioners wore the dais down". B6 drops "Fraden's niche grandest as everywhere" (in the box). B9 had no re-description.
- BALL-4: the chapel box ends on the seven ordinary niches; the offerings went to DM text as "A successful DC 10 Wisdom (Perception) check notices that the eighth niche, Elanna's, holds fresh offerings, tended recently and with care… A successful DC 13 Intelligence (Religion) check knows what it means for a chief's chapel to tend Elanna's niche." (Emphasis italics on *Elanna's* dropped.)
- BALL-5: the summons box became a DM subsection, **#### Raunu's Summons: the Questions, and What He Says**, at the end of Movement III (before its Snakes section, so the Agenda beats and omen stay directly under Movement III; "Checks in the summons" points to it). Roman text, the guest's questions as bold quoted run-ins, Raunu's replies in quotation marks, stage cues in roman. Its intro sentence that repeated the paragraph above it was cut to the "If friendly" definition; the closing line is a **The closing line.** run-in. "the way you would mention the weather" → "the way a man mentions the weather" ("you" outside read-aloud means the DM). Toast: one italic read-aloud block, each speech segment in quotation marks, the two stage cues in roman parentheses, the closing narration italic; "**two plates**" lost its bold inside the box. Speech wording unchanged.
- BALL-23: "Masks go on at the door" → "Masks are on before the gate"; "*(unchanged, and the one thing…)*" → "*(the one thing…)*"; the B0 Corval bullet → "**Corval receives by name**, from memory (see B1)." (the sentence stays at B1); the cup trigger and box now come before the head-of-the-line box, with the trigger pointing at "The quiet guest", below.
- Every indented italic block in 04 has a trigger (lint structure rule: 0).

**T5.2 (05, 07).**
- NIGHT-10: the *table that will not stop trying to kill them* DM Note now instructs ("say plainly what just happened: she stopped, looked at the character almost patiently, without anger, and the character went through the wall…; Then say what the round bought…"). The original's "through the wall" kept in place of the audit's "threw the character clear".
- NIGHT-11: epilogue box italicized; its inner italic line became a quotation ("You dance like my daughter would have.", the capital matching 04, 08, 10 and the Facets .fof). Set in roman: "Five short rules…" (Midnight Rules), "Not the midnight attack…" (The Snakes in the Dark), the "*None of it is ambush.*" lead, the Movement VII "(The snakes' knives…)" paragraph (its italic-toggled pointer now '(see "The Snakes in the Dark")'), and the emphasis italics on "*trapping* one". The 05 chapter dek (line 3) stays italic: every chapter has one, and 01's legend already defines non-indented italics as notes to the DM, so no legend change was needed.
- Gate box (the one remaining structure hit): trigger "**When the party reaches the Gatehouse Court and can see through the grille, read:**", in the module's bold "When…, read:" form.
- CAST-17: "**Vorlain by the wine — …**" → "**What Vorlain Says — …**"; "**Corval at the gate — …**" → "**What Corval Says — …**" (the species 01 declares). Inside both, the BALL-5 treatment: intro and stage cues roman, questions as bold quoted run-ins (Corval's "**DC 18 Wisdom (Insight)**" lost its bold). "**DM Note — the factor.**" already carried the declared species (T4.1); nothing to change.
- CAST-18: 07's copy of the Attendant box replaced by "(chapter V has the read-aloud)". The prose copy of Vorlain's drunk line cut; the sentence now uses CAST-7's split ("Getting him drunk takes… Drunk, he says one true thing (see "What Vorlain Says", below)."), and "says *nothing* — sober" lost its emphasis italics.

**T5.3 (05).** Two new boxes, sources only from 05 and 04's receiving line; ledger rows **#66** and **#67**.
- *The Crossing* (75 words), trigger "**When the Radiant steps out of the smoke onto the terrace, read:**", after the opening paragraph (whose last sentence now reads "Then the Radiant catches them on the terrace, and…Vell stops being unmemorable."). Beat 1 keeps only function (Vell is the same order of thing; the sword stays wrapped; the forces are unnamed; the Radiant's word is wary, with an apostate-hatred under it). NIGHT-9's "between you and the mask, without having crossed the space" was not used (a position the text does not give); the box uses the text's own "arriving instead of running".
- *Movement VII* (61 words), trigger "**When the Uninvited have gone, read:**", after the run box. **Verified "the minister who greeted you at the gate" against 04:** Corval does receive every guest by name at the Gatehouse Court, but 04's head-of-the-line box presents him only as "A thin old man in Boranis livery… greets them by name", never as a minister. The clause became "The thin old man who greeted you by name at the gate". NIGHT-9's "near the stairs", "upright", "out loud", "rose-bright" and "over a knot of guests" dropped as new detail. The DM paragraph below keeps function ("the player characters are the only order in the palace… **people are brave.** The box shows it, and the table should see more of it."); its fire/smoke/Corval imagery now lives only in the box.

**T5.4 (04, 05, 07, 09).**
- BALL-24: the five *Snakes This Movement* boxes are now H4 sections ("#### The Snakes This Movement — I" to "— V"), unboxed, with their parenthetical as an italic DM-note lead ("*Optional; show one or two, then let them be.*"). Inside them: "*Tell:*" → "**Tell:**"; the "→ *…*" pointers roman; emphasis italics dropped (who came, prepared, them, the missing year, accepted, filed, goes with them); spoken lines quoted ("take the air on the terraces", "What did he say?", "At the first quarter-bell…"); "(DC 13 Wisdom (Perception))" → "(a DC 13 Wisdom (Perception) check)" (it became a bare_dc hit once out of the box). The italic "*No card…*" notes stay as DM notes. Pointers updated: 04 "The Snakes in the Pen" ("…that Movement's "The Snakes This Movement" section"), 04 B8 ('"The Snakes This Movement — V"', italic toggles removed), 09 ("chapter IV's section", "the Movement V section").
- SNAKES-13: every mid-line or run-on **Turn it.** and **Snake on snake.** label starts its own paragraph in all six lines (11 labels). No wording change.
- SNAKES-16: the six *Who they brought* lines now bold the leaders by stat-block name (**Rhaza Callun**, **Damaris Kovaun**, **Essar Draunel**, **Vorlain Boranis**, **Essin Boranis**, **Pellin Corro**, **Maiven Nolonaire**) and end the group with "(see chapter X)"; all CRs cut from the prose (they are in the blocks). No other CR remains in prose outside budget lines.
- NIGHT-23 (05): "his **Phern Bodyguards** (see chapter X)", "The nine **Boranis Honor Guards** (see chapter X)", Table V–7 "The **Church Wardens** come down", "sixteen **Bought Blades**, four sergeants and a captain (see chapter X)". Later common nouns lowercased: "The Draunel duelists" and "a warden's arms" in ⟨The party turns one snake on another⟩. The audit's "his three" bodyguards was not used (09 says "two or three").
- CAST-15 (07): appositions on Kovaun ("Prelate of the Church; Agenda 2's patron."), Callun ("Mistress of the Merchant's Circle; Agenda 1's patron."), Corro ("The Phern magnate."), Draunel ("Lord of House Draunel; Agenda 3's patron."), Essin ("Vorlain's cousin."), Maiven ("Veier's cousin; Agenda 4's patron."), all from chapter X's epithet lines and 02's agenda patrons (Maiven as Veier's cousin: 06 "her cousin", 02 "The Cousin's Errand"). Sergeant: "**If it comes to steel:** stat block **Bought Sergeant** (see chapter X); card S3." Captain: the section's closing steel line now opens "stat block **Bought Captain** (see chapter X); card S3." ("*are*" lost its emphasis italics).
- CAST-16 (optional, done): all 17 "**Play him/her/it:**" labels → "**Roleplaying [Name]:**" (Raunu (the summons), Veier, Vorlain, Corval, Anha, Kovaun, Sella, Callun, Corro, Draunel, Essin, Maiven, Vell, the Attendant, Tavva, the Sergeant, the Captain). **Quote:** lines from existing quotes only, moved rather than copied: Veier ("I am well. I am watched over…"), Sella ("The dead were sent home tonight…", still flagged as her epilogue line), Vell ("You are observant. Enjoy the ball."). Vorlain gets no Quote line: his signature line is now only in "What Vorlain Says", and a Quote line would recreate the duplicate CAST-18 removed. No new dialogue.
- SNAKES-27 (optional, done): one **DM Note — how it plays** per card that printed simulation numbers: S2, S3, S7, S13 (one or two sentences each, numbers unchanged; each budget line keeps its qualitative verdict and points to the note), and S14 (the method, the table, the "four fights out of five" line, and the Adjusting lines' percentages and the "not simulated at 5th" note, all unchanged). S14's Adjusting lines now carry only their rules. The *Running the Snakes* budget bullet and the 2014 DM Note point to the new notes. The bullet's rough guide ("one run in ten to one in four…") is general guidance, not a card's number, and stays.

**Skipped sites:**
- NIGHT-23: "his Duelists" (old 05:792) and the Bodyguards/bodyguards and Duelists/duelists capitalization pairs other than the two lowercased: the quoted "his Duelists" was not found (05's remaining mentions are "Draunel's duelists", already lowercase, in the crowd list); "gray/grey", "its sight", "the pale factor" and "the others" were done in T4.6.
- BALL-24's parenthetical about cutting *The Snakes in the Pen*: owner's call, not done.
- CAST-15's Corro apposition repeats his header epithet; kept as the audit wrote it (no other existing label for him).


## Phase 6

### T6.1 — "What [Name] Knows" lists (Worker, 2026-10-03)

*CAST-2, CAST-23, BALL-11. Every site was located by quoted text (DESIGN §2).*

**Commands:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check` → OK (0 problems; 35 hard and 0 structure hits remain; no regression, no re-baseline). `bestiary_check.py` → 25 blocks + 3 Nastier, 0 mismatches. `pregen_check.py` → 5 pregens, 0 issues. `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 159 passed.

**07.** Each of the eleven entries gets a run-in label, **What [Name] Knows:**, a trigger sentence and bullets. It is set as plain text, not a box, so the 01 legend needs no new species. Placement: after *Roleplaying* (or the *Quote* where one follows it), before *At the Unmasking* / *If it comes to steel*. Bullet counts: Raunu 6 + a paragraph of refusals (the five Never-Says items; he refuses or deflects; *Detect Thoughts* and *Speak with Dead* lines from 04 and 02); Veier 5 + TODO-Q7; Anha 8 (CAST-2's model, plus "paid triple and forbidden to send word home" from 02 Agenda 8 and the pack confirmation from 04 B9); Kovaun 3; Sella 5; Callun 4 (one marked "(untrue)": the Tithe as the midnight pronouncement); Corro 4; Draunel 3; Essin 2 + TODO-Q11; Maiven 4 (one marked "(untrue)": Veier as a prisoner); Tavva 6. Sources for every bullet are in INVENTIONS #68.

**Gated (HTML comment, no answer):** Veier on the pregnancy, `TODO-Q7` (R6 holds); Essin's "two bodies", `TODO-Q11`.

**08 Table VIII–7.** The rumor numbering was rechecked against CAST-23 (6 = the bride dead, 8 = Vorlain never stopped ruling, 11 = the staff still inside). Italic truth notes went on those three only: 6 → chapter VII; 8 → chapter VII; 11 → chapter IV, "Undercurrent B — The Household That Wasn't". Rumors 1–5, 7, 9, 10 and 12 are unmarked.

**04 (BALL-11).** Both "tall, pale factor" sites were still present. B0 bullet: "*(This is Master Vell; see chapter VII.)*" added after "unremarkably". Movement V, House Draunel: "a tall pale factor is standing" → "Master Vell is standing". Line 1322's "the tall one" is the Wept, so it was not touched. 09 S2's "a tall pale factor who walked to the river gate" is Tavva's own words and stays (it is quoted in her 07 list).

**Omitted for lack of a printed source (not written):**
- Corro and the Phern intermediaries who sold Raunu relics (04 Undercurrent A never says Corro knows).
- Whether Essin knows Vorlain has no plot.
- The contents of Kovaun's memo from the east.
- Draunel's other three irons as something he would tell (INVENTIONS #11; they are inventions, not knowledge to share).
- Callun's prices (TODO-Q15, unchanged).
- Callun's own Secret (the Vorlain-chieftaincy arithmetic): nothing printed shows her telling it, so it stays in her Secret line. Maiven's instruction is listed, because it is the errand she hands Agenda 4.

**Skipped sites:** none.


## Phase 7 — T7.1 pilot (chapter 04)

*Worker, 2026-10-03. BALL-13, -14, -20, -21; FRONT-7 (04 L17, L393). Every site was located by quoted text. Wording only: no fact, number, DC or rule changed. A script diff of every `DC n`, dice expression and numeral before and after shows one added numeral, the "(Table VIII–7)" that BALL-21's own fix supplies.*

**Metrics** (`lint_5e.py --report --file 04_The_Ball.md`, DM prose):

| metric | target | before | after |
|---|---|---|---|
| words | — | 13,690 | 13,613 |
| mean words per sentence | ≤ 19 | 15.42 | 13.46 |
| sentences over 30 words | ≤ 12% | 9.01% | 5.28% |
| em dashes per 1,000 words | ≤ 8 | 13.66 | 1.54 |
| paragraphs over 120 words | ≤ 3 | 16 | 0 |
| "the players" (S2) | 0 | 6 | 0 |
| "perhaps" (S25) | 0 | 1 | 0 |
| rhetorical questions (S27) | 0 | 6 | 0 |
| S26, S28, S29, S30 | 0 | 0 | 0 |
| "player character" | — | 16 | 2 |
| "not X but Y" / ", not" | — | 12 | 11 |
| hard hits (conversion talk 3, narrator 1) | — | 4 | 0 |

The `designer_we` hit is "To the ones we lost", in Raunu's canon toast, inside read-aloud. The only `!` lines are the `<!-- TODO-Q… -->` comments.

**What was done.**
- **Em-dash and semicolon chains** split into sentences, colons or parentheses throughout. The 23 em dashes left in DM prose are in section titles cited by name ("The Snakes This Movement — V", "Undercurrent A — The Root of the House"), the declared box labels (**Sidebar —**, **DM Note —**), the ***Card Sn, chapter IX*** — pointers, run-in labels such as **The quiet guest — the music.**, and canon speech. Read-aloud and table cells were not touched. 1.54 per 1,000 is well under target. If the owner finds the result too clipped, the easiest place to put dashes back is the description (Palace Boranis, B9's rooms, the Dead Dance).
- **Long paragraphs**: B8 now has a bold run-in for each find (BALL-13's model). Undercurrent D's trail and find are bullets. The rest were split at a natural turn (the seating brawl, Undercurrent A's skeleton, orrery and "shape of it", Undercurrent B's trail, the summons, Movement IV's agenda beats, Movement V's scheduled beats, the Steel sidebar, the Raunu-attacked case).
- **BALL-14 fixes as written:** "The gatehouse cell is a scene." (68). "This is the first scene of the adventure, not a transition into it." (134). "In hindsight… devastating" cut. "…no torture-vault, no horror." "(a superb scene: …)" cut, and the image kept as plain instruction. "(They are wrong.)" "Then the room boils with the *promise* of news." Undercurrents sidebar: "If a table chases none of them, the night still works. The Undercurrents are depth, not the floor." Also cut: "a door left ajar on something vast", "let the table feel the floor tilt", "which is, afterward, the part nobody can stop thinking about". The second "holding its breath" (Undercurrent C) became "a household on watch". The Movement V one stays.
- **BALL-21:** "perhaps two dozen" → "about two dozen". "What then?" → "If the characters act on it:". "Sit with what that implies" cut. "Not even you." → "…and every rumor is told with total confidence (Table VIII–7)." "the module intends tables to discover it" → "The shape of it is discoverable." "Let the table sit with it." cut. Two street prompts went into quotation marks, "What does your mask look like?" and "What do you do?" (DM-to-player speech). The Undercurrent B epigraph became a statement.
- **BALL-20 / party:** every "the players" that meant the characters → "the characters" or "a character". "Agenda N's player" → "the character with Agenda N". "Player character" → "character" except where it separates PCs from NPC guests: "should be player characters" (the summons) and "Any player character who comes back out of B4". "the players should be told" (custom demands the host lead the Unmasking) → "the table should be told", because it means the people. "Four players will be in four rooms" stays (people, not caught by S2).
- **Conversion and narrator talk (FRONT-7):** "replaces the original's Sparks" → "**Heroic Inspiration.** Table I–3…"; "A third rule for this edition" → "Three rules… *(And the third: …)*"; "**the source of the gifts**" (in-world, but a lint hit) → "**the origin of the gifts**"; "The module does not explain the instruments" → "Nothing here explains…"; "Whose bones these are, the module does not know" → "…is left open"; "a fact the module states and does not explain" → "nothing in this adventure explains why"; "What the module still does not give" → "What the room still does not give"; "The module's best nights" → "The best nights"; "ordinary 5e combat" → "ordinary combat"; "the module's scheduled events" → "the scheduled events".
- **Italics fix found on the way:** Undercurrent D's spell list sat inside an italic aside, which flipped the spells to roman. That sentence now sits outside the aside, as plain DM text.

**Kept on purpose.** Canon speech (the toast, the summons answers, Raunu's "Enjoy the ball — and stay near the walls", Veier's lines, the lattice's "Wrong verb"). Every read-aloud box, unchanged. Jokes that earn their place: "which is a fine way to spend a masquerade", the chicken pen, "Remember them like this", "rarest of all at Oraga, *unsurprised*", "the terror of the Orthaen learning his wife's weapon, badly, in private, presumably to laughter", the wine-cellar stair. Functional contrasts that carry a rule or a fact: "grown, not built", "crystal, not iron", "End a scene on a choice, not on its resolution", "they fight to leave, not to kill", "a *playable fight* (card S4), not a fail state", "the palace doors, not the gates", "not by rank", "depth, not the floor", and the sidebar slogan "Guards are a scene, not a sentence" (kept at that one site, per BALL-14). One judgment call: B7's Orthaen ward-reading still says "automatically" and still leaves open whether the 10 minutes apply. The original was ambiguous, and the rewrite does not settle it.

**Before → after samples (for owner review, checkpoint G1).**

*1. B8, Raunu's Study (BALL-13's model).*

> **Before:** Locked, dark wing, second floor (opening it takes a DC 18 Dexterity check using Thieves' Tools; the lock is crystal, not iron). Two years of a genius's solitude, and — players will look for papers and find none, because there are none anywhere — the room thinks in crystal: instruments nobody can name, a grown relief of the eastern coast on the great table with its mist-lines remembered in colored lattice, the recent lines reworked many times; a work-slate bearing a half-erased lattice diagram (temporary scratch-work, the one grudging medium even the law cannot police); and, the detail that should follow players home, a drawer of duplicate invitation cards, one for every guest, a certain few with a corner deliberately scorched, as if he had been deciding something about each one. *(Copying or memorizing the slate's diagram takes a minute and a DC 13 Intelligence check, or none at all for anyone who draws it straight onto their own slate. The module does not explain the instruments or the scorch-marks. …)*
>
> **After:** Locked, dark wing, second floor. Opening it takes a DC 18 Dexterity check using Thieves' Tools; the lock is crystal, not iron. Two years of a genius's solitude. The characters will look for papers and find none, because there are none anywhere. The room thinks in crystal.
> - **The instruments.** Nobody can name them.
> - **The great table.** A grown relief of the eastern coast, its mist-lines remembered in colored lattice. The recent lines have been reworked many times.
> - **The work-slate.** A half-erased lattice diagram: temporary scratch-work, the one grudging medium even the law cannot police. Copying or memorizing the diagram takes a minute and a DC 13 Intelligence check, or none at all for anyone who draws it straight onto their own slate.
> - **The drawer.** The detail that should follow the characters home: duplicate invitation cards, one for every guest, a certain few with a corner deliberately scorched, as if he had been deciding something about each one.
>
> *(Nothing here explains the instruments or the scorch-marks. …)*

*2. The Seating Feud, the brawl.*

> **Before:** This is an honest brawl, and anyone can join it: fists, elbows, harvest fruit, someone's ceremonial staff — run it as ordinary 5e combat with one mercy: nobody here has a weapon worth the name, so player characters fight with unarmed strikes and improvised weapons, and **all damage in the brawl is nonlethal** — anyone dropped to 0 Hit Points is simply out of it, bruised, Unconscious and Stable, and no one makes a Death Saving Throw. The one line is the ball's own: **bare steel** turns a scuffle into a scandal and brings guards at a run (see the sidebar "Guards are a scene, not a sentence", below). Player characters can pick a side, shield the innocent, or end it — hauling the principals apart, a voice that expects to be obeyed, a well-timed joke at both houses' expense. Ending it *well* earns Corval's open gratitude, which is worth more than either house's: he is the man who opens doors. Letting it run costs nothing but bruises and reputations — and fills the galleries with guards for a Movement, which some agendas will find inconvenient and one crew (below) finds very interesting indeed.
>
> **After:** This is an honest brawl, and anyone can join it: fists, elbows, harvest fruit, someone's ceremonial staff. Run it as ordinary combat with one mercy. Nobody here has a weapon worth the name, so the characters fight with unarmed strikes and improvised weapons, and **all damage in the brawl is nonlethal**. Anyone dropped to 0 Hit Points is simply out of it, bruised, Unconscious and Stable, and no one makes a Death Saving Throw. The one line is the ball's own: **bare steel** turns a scuffle into a scandal and brings guards at a run (see the sidebar "Guards are a scene, not a sentence", below).
>
> The characters can pick a side, shield the innocent, or end it: hauling the principals apart, a voice that expects to be obeyed, a well-timed joke at both houses' expense. Ending it *well* earns Corval's open gratitude, which is worth more than either house's: he is the man who opens doors. Letting it run costs nothing but bruises and reputations. It also fills the galleries with guards for a Movement, which some agendas will find inconvenient and one crew (below) finds very interesting indeed.

*3. Undercurrent A, after "Both rivers, one spring."*

> **Before:** The shape of it is discoverable, and the module intends tables to discover it: the chief of the Orthaen believed the gifts of two tribes were one gift, long ago — that his marriage carried both halves — and that he has spent eight months *watching the proof grow.* What the module still does not give: the lattices' deeper contents, the name burned from the junction, what the restored gift is or does, or what the mists have to do with any of it. No check, spell, or divination reaches past that line tonight — *Legend Lore*, *Commune* and their kin return rumor and contradiction, the way the world answers everything else about this house. The find is a door left ajar on something vast — and it is also, quietly, why rumors 2 through 12 all exist: everyone senses he was *doing something*. Nobody guessed this.
>
> **After:** The shape of it is discoverable. The chief of the Orthaen believed the gifts of two tribes were one gift, long ago. He believed his marriage carried both halves, and he has spent eight months *watching the proof grow.*
>
> What the room still does not give: the lattices' deeper contents, the name burned from the junction, what the restored gift is or does, or what the mists have to do with any of it. No check, spell, or divination reaches past that line tonight. *Legend Lore*, *Commune* and their kin return rumor and contradiction, the way the world answers everything else about this house. The find is also, quietly, why rumors 2 through 12 all exist: everyone senses he was *doing something*. Nobody guessed this.

**Commands.** `lint_5e.py --check` → OK (0 problems; 31 hard and 0 structure hits remain). `bestiary_check.py` → 25 blocks + 3 Nastier, 0 mismatches. `pregen_check.py` → 5 pregens, 0 issues. `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 159 passed.

**Re-baseline.** `lint_5e.py --baseline` was re-run after the pass, so T7.2 onward are held to the new numbers. The old baseline still carried Phase-0 counts for every file. The new one records the current state of all twelve files: 31 hard hits module-wide, and 04 at 0 hard hits and 0 long paragraphs. `--check` passes against it.

**STOP: checkpoint G1.** T7.2–T7.7 wait until the owner approves the tone of these samples or adjusts the approach.

## Phase 7 — T7.2–T7.7 (parallel prose workers)

*Coordinator, 2026-10-03. Checkpoint G1:* the owner's `/goal` said to execute the plan, so the coordinator reviewed the
pilot samples and judged them acceptable (the voice is kept, and no fact or number changed). Work continued with one
calibration: keep about 3–8 em dashes per 1,000 words and a mean of 14–19 words, without atomizing. The owner can revert
any chapter, because Phase 7 is its own commit. Workers edited separate files in parallel and recorded their work in
`docs/audit_oraga_5e_official/prose_T7.{2,3,4-5,6-7}.md`. Each record has before/after metrics, kept items, judgment
calls and sample pairs.
- All files: 0 hard hits, 0 structure hits. Each worker's script diff found DCs, dice, XP and GP unchanged and read-aloud untouched.
- Whitelist additions: 01 Designer's note (gated on Q4); 08 Draunel's "we" on a canon agenda card (please confirm).
- Kept on purpose: canon card wording ("perhaps four times"), the Mask prompt questions in 11, and "player character" only where it separates the characters from NPCs.
- Leftovers for T9.3: 01's DC-ladder table has no title; emphasis italics in DM prose still need a sweep.
- Checks: lint --check OK (0/0), bestiary 0, pregen 0, pytest 159 passed, flow build OK. Re-baselined after the pass.

## Phase 9

### T9.1, T9.2 and the two Phase 7 leftovers (Worker, 2026-10-03)

**Commands:** `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check` → OK (0 problems; 0 hard and 0 structure hits). `bestiary_check.py` → 25 blocks + 3 Nastier, 0 mismatches. `pregen_check.py` → 5 pregens, 0 issues. `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 159 passed. `python conversions/dnd5e/oraga_night/flow/build_flow_page.py` → built without errors. No re-baseline, no whitelist entries. Nothing republished.

**T9.1 — ledger sync.** Method: `git diff pre-official-5e..HEAD -U0 -- 'conversions/dnd5e/oraga_night/*.md'` (INVENTIONS and STYLE excluded), every added H1–H4 heading, every boxed species line (Sidebar, DM Note, Troubleshooting, What [Name] Says) and every new card run-in (Detection, Treasure, Rewards, Tactics, Morale, Development, Adjusting, At heat 4, Topics, Overview, Quote, What [Name] Knows), each checked against the baseline text for a renamed original. #55 already carries the Q5 amendment (Phase 1); unchanged. **Rows added: #69** (chapter IX rulings: heat-4 lines incl. the new S10 one, tracker rows, S10 heat gate, S4 two guards, budget labels, the 2014 DM Note, Inspiration rows, the how-it-plays notes as relocation), **#70** (chapter X rulings: Kovaun CR 1/2, *She Arrives*, *Call the House* trigger, *Two Turns*, the "until the scene ends" definition, the CR line, *Stones Before Steel* as a Tell), **#71** (front matter and 06: the level-range line, the chapel Short Rest line, the 2014 claim and gift rule, *Reading This Book*, 06 *Rewards*).

| New block since `pre-official-5e` | Ledger / status |
|---|---|
| 01 Adventure Background | #60 |
| 01 Overview (seven Movements) | #61 |
| 01 Reading This Book (legend) | relocation of *How This Module Is Written*; #71 |
| 01 range line, chapel Short Rest line, 2014 claim; README 2014 gift rule | #71 (#47 for the Short Rest fact) |
| 01 Troubleshooting ×2, retitled ("you keep setting every DC at 20", "the table rolls Initiative") | rename (T4.1/T4.2) |
| 01 **The DC Ladder** caption (this phase) | title only, no fact |
| 02 The Eight Agendas + 8 agenda H3s | relocation from 03 (T2.1) |
| 02 DM Note, 03 Sidebar, 04 DM Note/Sidebar, 05 Crossfire/Gutter/Fractures-and-magic Sidebars, 05 three DM Notes, 06 Going east, 07 What Vorlain/Corval Says, 07 DM Note — the factor, 09 heat / Movement V / hint DM Notes | renames of baseline boxes (MM → DM, T4.1; species, T5.2) |
| 04 The Snakes This Movement — I–V (H4) | relocation (unboxed, T5.4) |
| 04 Raunu's Summons: the Questions (H4) | relocation of the summons box (T5.1) |
| 04 Dinner for Two (B9), Topics | #58 |
| 04 Seating Feud timing; gate-failure, B0/B3/summons results | #64 |
| 05 The Midnight Clock (O9 default) | #63 |
| 05 General Features; Sidebar — Adjusting the Attack (O11); trample 5 (2d4) (O10); B12 Treasure; carry award | #63 |
| 05 Sidebar — Characters who attack Vell | rename of "Players who attack Vell" |
| 05 The Snakes in the Dark (rename), card pointer list | rename + cut (T2.4); cards hold the substance |
| 05 The Crossing box; Movement VII box | #66, #67 |
| 06 Rewards | #71 (recap only) |
| 07 What [Name] Knows ×11; 08 rumor truth notes | #68 |
| 07 Quote lines ×3 | relocation from existing quotes (T5.4) |
| 07 default DC, Voiding the contract, Vell's checks, Callun DC 20 | #65 |
| 08 Page One / Page Two; Player Handouts group; Rumors at the Ball *(DM table)* | relocation / rename (T2.5) |
| 08 Player Handout 3 + Table VIII–8 | #59 |
| 09 S2 rename | rename (T2.4) |
| 09 Detection ×4, Treasure, Tactics, Morale, Development lines | #62 |
| 09 At heat 4 ×5, tracker rows, S10 gate, S4 two guards, budget labels, DM Note — at a 2014 table | **#69 (new)** |
| 09 DM Note — how it plays ×5 | relocation (T5.4); noted in #69 |
| 09 DM Note — how many snakes to show | relocation from 04 (T2.4) |
| 10 Kovaun CR 1/2 (O20); She Arrives (O24); Call the House; Two Turns; scene-end definition; CR line; Stones Before Steel Tell | **#70 (new)** |
| 10 Gear lines, costume notes, *Blood, Not Hire*, *Pays Her Debts* to lore tails | relocation (T4.4) |
| README For Contributors / Before the Night / The Night / Appendices | regroup (T2.3) |

**T9.2 — flow page.** `flow.json`, 61 edits, each asserted against its old text (script in the session scratchpad). No node referenced a removed section; qg-3 stays removed and its edge stays rejoined (qg-2 → qg-4); the S2 label already read "The Service Corridor Job"; the eight agenda nodes already pointed to chapter II; no "MM" left.
- *Anchors:* 19 refs to the Movement I–V and Undercurrent A–D headings carried slugs without the heading's italic parenthetical (e.g. `#movement-iv--the-toast`); now the full slugs (`#movement-iv--the-toast-later--dinner`, `#undercurrent-a--the-root-of-the-house-if-you-have-time`, …).
- *Snake lines:* the six `snk-*` nodes pointed to 04 "The Snakes in the Pen", now one pointer sentence (Q21). They now point to their 09 *Six Lines* entry plus "04_The_Ball.md (The Snakes This Movement — I to V)".
- *The Snakes in the Dark:* the five `kd-*` labels "Knives: …" → "Snakes in the dark: …"; each ref adds its card (S12, S8, S13, S13, S11); kd-thenya → `#the-thenya--toward-the-fire`. kd-circle lost "Corval is on the stairs, untouched" (cut from 05 in T2.4) and now says "a Tithe-carrying minister" (S12). kd-phern's check is spelled out.
- *Midnight Clock:* ev-raunu and ev-bell refs lead with `#the-midnight-clock`; beat-east adds the O9 default ("he reaches the garden stair three beats after Raunu falls") and the clock ref; the leash clock reads "half an hour at most" and names the default leash moment and the last bell as the latest, pointing to "The Midnight Clock"; the m6 phase summary points to it.
- *Buying Time:* fight-uninvited's ref → `#buying-time` and `#down-not-out` (it pointed to "You Cannot Beat Them"); the trick DC adds "15 the second time, never a third". fr-wept: "DC 15 whatever the tells once she has 2 or more Delay".
- *DM wording and house style:* "PC(s)" → "character(s)" (b4, beat-dais, sc-wards, sc-rescue, end-default); full check forms (b4 DC 25 Charisma (Deception), sc-wards DC 13 Intelligence (Arcana), gate-void DC 13 Charisma (Persuasion), gate-wicket Thieves' Tools and Strength (Athletics), cross-2 "saving throw"); b6 "Short Rest"; sc-rescue adds "100 XP for each" (05 *Carrying somebody out*).
- *Left alone:* "Hired Knives" (a creature name); "⟨A player character dies⟩" (a section title).

**Leftover 1 — 01's DC ladder.** A bold caption line **The DC Ladder** above the table, in the module's bold-caption form, unnumbered so Tables I–1 to I–4 keep their numbers.

**Leftover 2 — emphasis italics.** 129 emphasis spans set roman across 9 files: 01 ×5, 02 ×10, 04 ×33, 05 ×30, 06 ×3, 07 ×12, 08 ×4, 09 ×20, 10 ×12 (plus the two italic fixes below, not counted). Each replacement was asserted unique before writing, and a paragraph-level asterisk-parity check shows no broken italics. Two meaning-carrying cases were reworded rather than just set roman: "whether the man who returned is *the man who returned*" → "…is the man who left" (07 Kovaun, 09 Church line), Agenda 2's own wording. Also fixed in the same pass: 04's Callun aside had its roman-toggled section name, now '"The Snakes This Movement"' in quotation marks (the italic aside stays italic, and its inverted "dynasty" toggle is gone); 09 S14's stale "the *hard-hitting* line under Scaling" → 'the "A table built to hit hard" line under Adjusting the Encounter' (Scaling was renamed in T3.3); "optimised/Optimised" → "optimized/Optimized" ×4 in 09 (spelling missed by the lint list).
- *Kept, by rule:* spells, items and charges; read-aloud; whole italic DM-note paragraphs; card and run-in labels (*Lanterns*, *At heat 4:*, *Failure:*); invented or game terms (*detain* ×8, *brandishing*, *steer*, *Impossible*, *common*/*uncommon* rarity, *under Low*/*beyond High*, *to 4*, *plant the doubt*, *the missing year*); words to say aloud or speech (*locked on you* / *drifting*, *what did he say?*, *nobody made them*, *someone is editing you.*, the rumor text in Table VIII–7); "success at a cost" vocabulary (*with a cost attached*, *at a cost*, which 04 defines as a term); *if you have time* (a heading tag); table-row labels (*the Attendant distracted*); and chapter references (*A guest*).
- *Skipped:* 01's Designer's note (*works*, *the designers*), gated on Q4 (T8.2); 03 and 11, which are player-facing, not DM prose (*shows itself*, Andra *is*).

## Phase 9 — final-review fixes

### T9.3 follow-up (Worker, 2026-10-03)

Scope: every NEW-* issue in the six slice files' §6, plus the "partly" leftovers in their §5 tables. Every site was found by its quoted text and changed through a script that asserts exactly one match before writing. No site was missing. Each slice file now has a **§6a Resolved** table.

**Counts.** 53 NEW-* issues: **51 fixed** (3 of them by Planner decisions O25–O27), **2 gated** (NEW-CAST-2 → Q20, NEW-CAST-3 → new Q24), **0 skipped**. The 9 partly-fixed leftovers are all fixed: FRONT-5 (the code span and the box-list claim), FRONT-19 (the rest cost), NIGHT-8, NIGHT-13, NIGHT-14, SNAKES-15 (the five pointers), SNAKES-25 (the rename), BESTIARY-15 (two lines), CAST-24 (Table VIII–1 and 07's italics).

**Planner decisions** (DECISIONS.md, *Phase 9 final-review decisions*):
- **O25:** S3's bell clock counts only rounds at the gate (05 step 8, S3).
- **O26:** S9 fills offstage only if the table saw the appointment made. This keeps the default arithmetic (Draunel 2, Boranis 1). Sites: S9, the Mv V DM Note, Tables IX–2 and VIII–5, flow `clk-circle`.
- **O27:** the ring's answer comes after the toast. Q23 stays open.

**Notable edits.**
- **Restoration (NEW-NIGHT-7).** Text restored from `git show ef02a28:…/05_The_Longest_Night.md`, the old "Knives in the Dark" Phern and Draunel subsections:
  - "every guest brought through that door counts" → S11 Development (with Table I–4);
  - "no check for a Phern" → S11 Corro's word;
  - the fourth iron → 05's card list, in the old words ("take Vorlain in the chaos and hand him to the first sect guard through the gate as the culprit").
- **Prep box (NEW-FRONT-3/4).** Step 2 is now chapter II "The Truth of the Night" plus "The Eight Agendas" (15 min), step 4 is 25 and step 5 is 15. The total is unchanged at 90. Step 5 now names "The Snakes at the Ball".
- **Rename (SNAKES-25).** 09 "The Snakes in the Pen" → **"The Snakes at the Ball"**. 04's heading, now a table plus a pointer, → **"The Snakes at a Glance"**, so that no heading keeps the old name (the joined-line zero check covers both). Pointers updated: 01 ×2 and INVENTIONS #1. flow.json had none. The 04 Undercurrent C tag changed, so its flow.json anchor was updated.
- **Pregens (NEW-CAST-1).** "snake", "chapter IX", "the Uninvited", "when the lights die" and the undead spoiler are off the player sheets. *Turn Undead* now prints the SRD effect. Handouts 1–3 were checked and are clean.
- **Bestiary (NEW-BESTIARY-1).**
  - Five tests went into `test_bestiary_check.py` first and failed red: 5 failed / 24 passed.
  - Then `trait_dc_problems` (a TRAIT_DC table tying *Put Aside* to Strength) and the data row `dc=[(15,0)]`. The checker reported "Attendant: Put Aside DC 14 vs 8+3+4 = 15".
  - Then the text went to DC 15, and the suite was green. INVENTIONS #55 is amended.
- **Kept on purpose.** "*House Boranis hired none.*" stays italic in 01 (canon emphasis, Facets 04:90, and italic in 04 and 09 too). The two lint regressions this pass caused along the way (07's default-DC sentence read as a bare DC; the epilogue question counted as rhetorical in 06) were reworded rather than whitelisted. Two "not the count" contrasts became "only the warning".

**New owner question.** **Q24:** Veier's canon "Tell my uncle…" against her being the chief's cousin. It is in AUDIT §5a with background, with a `TODO-Q24` in 07. The quote is not edited. Open: Q3, Q4, Q7–Q20, Q23, Q24.

**Commands.**
- `python conversions/dnd5e/oraga_night/tools/lint_5e.py --check` → OK (0 problems; 0 hard, 0 structure). No re-baseline, and no new whitelist entries.
- `bestiary_check.py` → 25 blocks + 3 Nastier, 0 mismatches.
- `pregen_check.py` → 5 pregens, 0 issues.
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 164 passed.
- `build_flow_page.py` → built.
- Joined-lines grep over M/*.md: "Knives in the Dark" 0, "chapter III, Agenda" 0, "Chapter III, Agenda" 0, "Snakes in the Pen" 0. "MM" is 0 in the module text, but INVENTIONS_5e.md has 4 (history rows) and STYLE_5e.md has 3 (the rule that bans it). "direct question" is 0, except 1 in INVENTIONS #55's history. Both files are outside the linter's scope by design (STYLE "Do not touch" #3).

## Phase 9 — closeout (coordinator, 2026-10-03)
- T9.3: six final reviewers appended a status table (§5) and new issues (§6) to each slice file. The final-review fixes are commit 186fcc1. Totals are in AUDIT §0: 137 fixed, 3 partly (the remainder gated), 11 gated, 1 void, out of 152.
- T9.4: `docs/CARRYOVER_d20_oraga_official.md` (71 rows). There is no d20 Oraga adventure yet, so it covers both starting points.
- T9.5: one commit per phase, 10acb0f…186fcc1, plus this closeout commit. Nothing pushed. Before any push, scan main..branch for private canon (memory rule).
- Side task (the owner's /goal): `docs/RESEARCH_coc_for_facets.md`, the Call of Cthulhu open-content review, is committed separately.
- Remaining work is all owner-gated: Phase 8 (T8.1–T8.16) on Q3, Q4, Q7–Q20, Q23, Q24.
- 2026-10-05 OWNER: none of the CoC review's recommendations will be brought into Facets; memo kept as reference, its questions closed.
- 2026-10-05 OWNER answered all remaining questions (Q3, Q4, Q7–Q20, Q23, Q24, plus the Vell follow-up). Rulings are in AUDIT §5b. Phase 8 can proceed.

## Phase 8 — owner rulings applied (Worker, 2026-10-05)

Rulings from AUDIT §5b, applied to `conversions/dnd5e/oraga_night/` (M/). Every site was
found by quote; no site was skipped. Ledger rows: INVENTIONS #72–#82 (plus the R6 note and
an amendment to #58). Decisions left to the Worker: DECISIONS O28–O31.

- **Q23 / Q7 (T8.3, T8.19).** 04 *Dinner for Two*: the ring is shown and kept at the doors, Veier sends for the character after the toast (O27), and a new **A minute alone** paragraph has Raunu step out so the ring and message reach her alone. The child topic now confirms the pregnancy to a character she trusts, and says this counts as discovery. 07 *What Veier Knows* gets two bullets, and *What Raunu Knows* gets one line. INVENTIONS R6 is noted and #58 amended. flow `sc-dinner` updated.
- **Q24.** "Tell my uncle" → "Tell my cousin" in 04 and 07 (the only two sites). The TODO-Q24 ambiguity note is removed.
- **Q9 (T8.5).** 05 ⟨They trap one⟩ gets one paragraph covering the three Uninvited (Wept → ⟨They save Raunu⟩; Radiant → easy escape; Hollow → the doors open early). flow `ihb-trap` updated.
- **Q8 / Q8b / Q25 (T8.4).** 10 Master Vell is now a full SRD 5.2.1 block: AC 20, Initiative +4 (14), HP 285 (30d8 + 150), scores 16/18/20/18/20/18, saves Dex/Con/Wis/Cha at PB +4, Insight +13 and Perception +9, resistance to all thirteen damage types, Immunities Charmed/Frightened/Grappled/Restrained, *Magic Resistance*, and the Reaction ***Not Where It Landed*** (a hit deals no damage). CR — (XP 0; PB +4), and still no attacks. The "cannot be fought" paragraph now explains the numbers (about 15 damage a round from four 5th-level characters against 285 HP). How to Read, the 05 Crossing sidebar and the 07 *If it comes to steel* line are updated. There is no death branch. `bestiary_check.py` needed no change: it skips blocks it has no data for, and Vell has no CR for its estimator (O29).
- **Q18 (T8.14).** "—" alignment on the Hollow, the Radiant, the Wept and Vell. The cast is left untagged.
- **Q10 (T8.6).** 05 B12: the case is carried by the sergeant who holds the gate, and the Second Clause is "sealed". 09 S3 *Where the Bought stand* now names the case and the two read-aloud tasks. 10 Captain **Tells** ("It alone has read the contract's sealed third task; the sergeant carries the case") and the loot entry ("Chained to the sergeant's hip") are fixed. 08 had no site.
- **Q11 (T8.7).** 09 S13 *Broker a trade* is glossed ("the two cousins Vorlain killed in his year of rule"), and 07 *What Essin Knows* gets a bullet. Both TODOs are removed.
- **Q12 (T8.8).** The good-coat clause is cut from the S9 box. The box still parses and runs about 53 words.
- **Q14 (T8.10).** **(no XP)** on S2 "Let her go", S4 "Going back the way they came", S5 "Let them go", S6 "Walk away", S12 "Let them" and S14 "Stop interfering" (O30 says which were left unmarked and why). S4 Rewards now reads "any out except going back the way they came". S14 Rewards gives the three paying conditions. 09 *Running the Snakes* gets an Outs clause, and 01 Table I–4 gets the "(no XP)" clause.
- **Q15 (T8.11).** 04 Mv III Circle beat: "with 10 GP behind it". Undercurrent C: "Her price for the nursery is 250 GP." 02 Agenda 2 **Pays**: one favor the Prelate can grant without scandal (the DM may make it larger). 06 Rewards: the favor default, plus a new **Sales to the Circle** line (10 GP, 250 GP). 10 loot: "a coat worth 10 GP". Handout 2's card keeps its "of frightening size" pitch.
- **Q13 (T8.9, O28).** 05 *General Features* gets a **Sizes** bullet for B2, B5 and B9. 04 B2/B5/B9 get one-line pointers, and 08's diagram caption is updated. All sizes were checked against every printed distance (O28).
- **Q16 (T8.12).** Q16a: no sheet change. Q16b was done test-first: `pregen_check.py` FOCUS got an Ilesse row and failed red (2 issues). 11 then reads "a sliver of her own warding crystal as Holy Symbol, for her spells and her Channel Divinity", Carrying reads "warding crystal (Holy Symbol)", and the check went green. `test_pregen_check.py`: two minimal-sheet tests were scoped to Andra, and three Ilesse tests were added.
- **Q3 (T8.1):** closed, nothing to do. **Q4 (T8.2):** 01's note is now the unsigned **DM Note — what the fights are for** (FRONT-6 wording, "DM"). Its `lint_5e_allow.txt` entry is removed, and STYLE_5e.md's box-species row is updated.
- **Q17 (T8.13).** README "the year 3164" ("PG" occurs nowhere else in M/). Blackwatch glossed at its first mention (02 *the recent wound*); Mazaa glossed at its first mention (06, "Mazaaian"). No pronunciations.
- **Q19 (T8.15).** "— R.C.", "— D.K.", "— E.D." and "— M.N." are removed from Handout 2 (08). 02's agendas carried no initials.
- **Q20 (T8.16, O31).** Undercurrent B now reads "The household was sixty. Two years ago it was cut four-fold, and every servant let go had to go somewhere." and "recite every one of the placements". 07 already said sixty. 08 and flow.json had no "eighty". The TODO-Q20 witness note is removed (Q20b: Sella and Corval).
- **Carryover.** `docs/CARRYOVER_d20_oraga_official.md` §6 lists Q10, Q11, Q19, Q20 and Q24 with their Facets sites, including `F:07` L63 for "my uncle". `adventures/` was not edited.

**Commands.**
- `grep -rn "TODO-Q" conversions/dnd5e/oraga_night/*.md` → only INVENTIONS history rows (none in chapters, README or STYLE).
- `python tools/lint_5e.py --check` → OK (0 problems; 0 hard, 0 structure). No re-baseline. One whitelist line removed (Q4).
- `bestiary_check.py` → 25 blocks + 3 Nastier, 0 mismatches. `pregen_check.py` → 5 pregens, 0 issues (red first, as above).
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 167 passed (164 + 3 Ilesse tests).
- `python flow/build_flow_page.py` → built (`sc-dinner` and `ihb-trap` summaries changed).
- `python -m pytest software/tests/test_docs_consistency.py -q` → 37 passed.
- 2026-10-06 PUSHED feat/lean-facets (439d69e..e95d326) + tag pre-official-5e, after redacting one owner-username path from the unpushed range (guard test caught it); guard 42 + tools 167 passed.

## Review-fix pass: plan (Planner, 2026-10-08)
- The critical review (`docs/REVIEW_oraga_5e_official_critical.md`, 6.5/10, P1 ×7) is planned into
  `docs/DESIGN_oraga_5e_review_fixes.md` and `docs/TASKS_oraga_5e_review_fixes.md`.
- Phases: R0 tooling (`facts.yaml` continuity bible, fact checker, linter upgrades), R1 rules, R2 continuity, R3 artefacts, R4 maps,
  R5 layout and voice, R6 copyright check, re-review and push.
- Planner decisions proposed: O32–O40 (DESIGN §3). Owner questions: QR1–QR7 (DESIGN §4).
- 2026-10-08 OWNER answered QR1–QR7 (rulings recorded in DESIGN_oraga_5e_review_fixes §4); the plan is fully ungated.

## Review-fix pass — R0

*Worker, 2026-10-10. Tasks R0.1–R0.3 of `docs/TASKS_oraga_5e_review_fixes.md`. Tooling only:
no module chapter text was edited. `STYLE_5e.md` gained the O41 pins.*

**R0.1 — continuity bible and fact checker (TDD).**
- `M/facts.yaml`: 10 facts at their TARGET truth (QR1–QR4, O28, O33–O35): household (sixty,
  twenty-two stayed, "cut by nearly two-thirds", no "four-fold"); honor guards (nine; at
  midnight two at the east-wing doors, seven to the dais; Movements I–V left to R2.2's table;
  S4 = "the two nearest"); retinues (Circle 4, Church 4; Draunel 3, Boranis 3, Phern 2–3,
  Thenya 2–3 per INVENTIONS #1); the Bought (16 + 4 + 1 = 21, "twenty blades", "twenty sworn
  witnesses"); arrivals (Attendant Mv I, Uninvited Mv III crush, Vell Mv I, the Bought at
  dusk / the gate from midnight); east-wing floor (gallery level, +12 ft, stair from the
  Court's east doors); stairs (private stair = the garden stair); terraces (O34); O28 room
  sizes; Maiven dies by default.
- `T/fact_check.py`: unwraps paragraphs (shared `lint_5e.unwrap`), six check types (forbid,
  sentence, count, size, movement, require) with `files`/`unless` filters and noun windows
  (a count never crosses a table cell; "servants of" and "one" are not counts). Modes: default
  (every hit, exit 1 if any), `--report` (counts per fact, then hits; exit 1 if any),
  `--baseline`, `--check` (fails only on hits above `T/fact_baseline.json`).
- `T/test_fact_check.py`: 50 tests (≥3 per check type, plus unwrapping, validation, the real
  module's expected hits, the CLI and the baseline). Red first (import error), then green.

**Fact-check first run: 24 hits. This is the R2 worklist.**

| fact | hits |
|---|---|
| household | 4 |
| honor_guards | 6 |
| retinues | 3 |
| bought_company | 2 |
| arrivals | 3 |
| east_wing_floor | 1 |
| stairs | 1 |
| terraces | 3 |
| room_sizes | 0 |
| maiven_fate | 1 |

| where | fact/check | match |
|---|---|---|
| 01_Overture.md:63 | arrivals/sentence | "at midnight something comes through with the Uninvited" (P1-4) |
| 02_The_World_and_the_Night.md:70 | household/forbid | four-fold (P1-1) |
| 02_The_World_and_the_Night.md:422 | household/forbid | four-fold (P1-1) |
| 04_The_Ball.md:38 | household/count | a hundred servants (P1-1) |
| 04_The_Ball.md:83 | honor_guards/sentence | "the nine go to the dais" (P1-2) |
| 04_The_Ball.md:99 | honor_guards/sentence | S4 "two guards", not "the two nearest" (P1-2) |
| 04_The_Ball.md:705 | household/forbid | four-fold (P1-1) |
| 04_The_Ball.md:1391 | terraces/forbid | Two terraces below (P1-5, O34) |
| 05_The_Longest_Night.md:440 | east_wing_floor/require | General Features lacks the 12-foot stair / gallery level (P1-5, O33) |
| 05_The_Longest_Night.md:443 | stairs/require | private stair not named as the garden stair (P1-5, O33) |
| 05_The_Longest_Night.md:461 | honor_guards/sentence | "The nine Boranis Honor Guards … die or fall" at the dais (P1-2) |
| 05_The_Longest_Night.md:753 | arrivals/movement | Hollow "(any Movement)" (P1-4) |
| 05_The_Longest_Night.md:753 | arrivals/movement | Hollow "Mv II–V" (P1-4) |
| 05_The_Longest_Night.md:817 | honor_guards/forbid | only guards left are dying on the dais (P1-2) |
| 05_The_Longest_Night.md:1173 | bought_company/sentence | forty blades (P2-6) |
| 05_The_Longest_Night.md:1178 | bought_company/sentence | forty sworn witnesses (P2-6) |
| 06_Aftermath.md:43 | maiven_fate/sentence | "Maiven Nolonaire will not leave the city…" unconditional (P2-5) |
| 08_Handouts.md:43 | honor_guards/sentence | "The nine honor guards | To the dais" (P1-2) |
| 09_The_Snakes.md:170 | retinues/sentence | Callun "and three Circle Hired Knives" (P1-7) |
| 09_The_Snakes.md:218 | retinues/sentence | Kovaun "and three Church Wardens" (P1-7) |
| 09_The_Snakes.md:1331 | terraces/forbid | rail of the upper terrace (S9 box; O34) |
| 09_The_Snakes.md:1355 | terraces/forbid | Two terraces below (O34) |
| 10_Bestiary.md:421 | honor_guards/sentence | "There are nine. At midnight they die or fall on the dais" (P1-2) |
| 10_Bestiary.md:656 | retinues/forbid | Kovaun brought three (P1-7) |

Every item R0.1's acceptance names is present: household, nine guards, forty blades, the
Attendant's arrival, the east wing's floor, "Kovaun brought three", Maiven alive in 06. No
false positive on 04:877 ("should field forty blades in ceremony", the honor guard), on
05:368 ("up to nine people"), or on the O28 sizes (0 size hits). Not built in R0: a
"Down, Not Out" rule-copy entry; R1.2 adds it when it fixes the canonical wording in 05.

**R0.2 — linter upgrades (TDD).**
- Hard rules now run on unwrapped paragraphs (`unwrap()`); hits report the line where the
  match starts. The wrapped-DC sites the review named (04:243 etc.) were already handled by the
  old next-line read-ahead, so bare_dc stays at 0; the unwrap closes the general case (save
  demands, conversion talk, any rule split by a wrap).
- Allowlist is rule-scoped, `file|rule|text|reason`, and exempts only where the quoted text
  overlaps the hit. Migrated 18 entries: Handout 1's six → rule `*` (fixed canonical text);
  eleven generic-check and grapple lines → `bare_dc`; the Handout 2 card → `designer_we`. The
  old 3-field form now raises.
- New hard families: emphasis_italics, or_skills, html_comment, repo_filename (README exempt),
  sim_jargon, conversion_wide, anachronism. New structure rules: trigger_format (the pinned
  "**Read this when …:**"), box_label (heading style), defined_terms (against `T/terms.txt` and
  the canon vocabulary read from `settings/valloh` V0/V1/V3).
- `T/terms.txt` seeded with 23 terms, each with its canon source and module gloss site. Scora
  and Kshalo are canon (V1, V3) but unglossed in the module, so they are listed with gloss `-`
  and flagged until R2.5.
- `STYLE_5e.md` pins the trigger form and heading-style box labels; DECISIONS O41.
- Tests: `test_lint_5e.py` grew from 125 to 185 tests (≥3 per new rule; unwrap, scoped allowlist, wrapped
  rules). Fixtures: `hard_hits.md` gained one line per new hard family; `clean.md` uses the
  pinned trigger and box-label forms.

**New lint hit counts (`lint_5e.py --report`). These are the R3/R5 worklists.**

| family | hits | phase |
|---|---|---|
| emphasis_italics | 50 | R5 (incl. 14 italic *Heroic Inspiration* on Rewards lines, P2-24) |
| or_skills | 12 | R5 |
| html_comment | 1 | R3 (09:268, P2-3) |
| repo_filename | 2 | R3 (04:22–23, P2-2) |
| sim_jargon | 8 | R3 (P2-1, QR6) |
| conversion_wide | 4 | R3 (01:35 *Inventions*, 03:82, 03:84, README:42; P2-4) |
| anachronism | 4 | R5 (07:296, 07:311, 09:215 "memo"; 07:750 "businessperson"; P3-17) |
| trigger_format | 30 | R5 (P2-20) |
| box_label | 16 | R5 (P2-21) |
| defined_terms | 2 | R2.5 (04:677 Scora, 08:256 Kshalo; P2-8) |
| all other families | 0 | — |

Totals: 81 hard, 48 structure. Soft metrics moved slightly (words 70,063 → 70,230) because the
migrated `bare_dc` lines are no longer excluded from the soft metrics; no soft target regressed.

**Re-baseline.** `lint_5e.py --baseline` rewrote `T/lint_baseline.json` (81 hard + 48 structure
hits recorded); `fact_check.py --baseline` wrote `T/fact_baseline.json` (24 hits). Both
`--check` runs pass. Later phases re-baseline after fixing hits and say so here.

**Commands.**
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 277 passed.
- `python T/lint_5e.py --check` → OK (0 problems; 81 hard, 48 structure remain).
- `python T/fact_check.py --check` → OK (0 problems; 24 hits remain).
- `python T/bestiary_check.py --quiet` → 25 blocks + 3 Nastier, 0 mismatches.
- `python T/pregen_check.py --quiet` → 5 pregens, 0 issues.

## Review-fix pass — R1

*Worker, 2026-10-10. Tasks R1.1–R1.5 of `docs/TASKS_oraga_5e_review_fixes.md`. Decisions
O42–O47 in DECISIONS.md; INVENTIONS #1 amended (QR3) and #83 added.*

**R1.1 — S14's argue-out (O32, P1-3, P2-15, P2-16).** Arguing its orders is a distraction
everywhere: in chapter X's *Can Be Distracted* and Breaks line, in S14 (folded into the first
out, the separate "Argue its orders" out deleted), and in 07, 08 and `flow.json`. The Idle
result is stated once, in chapter X: the distractor becomes *furniture* for the rest of the
scene and the Attendant keeps acting (the old "does nothing on its next turn" lock is gone).
S14's Results bullet, 05's first Attendant bullet, 08's Page Two line and `flow.json` point
to it. S14's Objective names two wins; its Rewards line lists three triggers (two XP, one
Heroic Inspiration; see O45). Hint 5 shows the Focus glance when one of the three next has no
Delay. Chapter X's out-slug claim is dropped.

**R1.2 — "Down, Not Out" in one home (O36, P2-18).** Test-first: `test_fact_check.py` gained
`TestRuleCopy` (7 tests: a hit outside home, a miss in home, a pointer with its local rule,
each element counted once, elements split across paragraphs, the match text, validation)
and two real-module tests; red (unknown check type), then green. `fact_check.py` gained the
`rule_copy` check type; `facts.yaml` gained the `down_not_out` fact (8 elements, max 2, plus a
`forbid` on "round after next"). First run: 08:63 (7 elements), 10:45 (6), 09 S13 (3) and
S13's "round after next". Fixed: 08's DM-sheet line, 10's mercy bullet and 09's
after-midnight paragraph are pointers plus their local rule; S13 says "the round after".
Now 0 hits.

**R1.3 — the rules fixes (O37, O40, QR7).**
- P2-14: Table V–5 row 6, the grapple works as the Radiant's saving throw; the grip is the
  1 Delay and points to chapter X's table.
- P2-17: S3 ending 1 (09 and 05): the Second Clause pulls the Bought back to watch the crowd,
  and the gate is open; the captain fights on only if the party blocks the search.
- P2-10: S4's Objective and first out end the fight, not the door (escort back, no
  expulsion). The out's "(Deception or Persuasion)" is now spelled out, so or_skills drops
  from 12 to 11.
- P2-11: ⟨The Bought change sides⟩ gets an in-palace door, a sergeant's runner at the
  Gatehouse Court (B1) in Movement V; `flow.json` matches.
- P2-12: the tracker's "second card" list says "Callun's coin refused".
- O37: the bell default is in 05's Midnight Clock step 8, pointed to from S3, 05's "The last
  bell", 08 and `flow.json`.
- QR7: S2 "Make enough noise to lose" and S6 "Shout" are **(no XP)**, and both Rewards lines
  say so.
- The flow page was rebuilt (`flow/build_flow_page.py`).

**R1.4 — Nastier as baseline (P1-7, QR3: four).**
- Retinues: 09 "Who they brought" says four Circle Hired Knives and four Church Wardens.
  Chapter X's flavor lines say "Kovaun brought four" and "The Circle brought four". S7, S8
  and S12 no longer call the fourth a Nastier line. INVENTIONS #1 is amended. The fact
  checker's retinue hits fell 3 → 0.
- Promoted, not folded (O42): **Veteran Bought Sergeant** (CR 4), **Boranis Cousin of 3160**
  (CR 1), **Veteran Draunel Duelist** (CR 2), as full blocks in chapter X. Their base blocks'
  Nastier lines point to them. Table X–1 lists them, with the veteran at the gate for S3.
- New Nastier dials on six blocks (O43). A real *Nastier* line on S3, S6, S7, S8 and S9
  (O44). S13's roster and scaling lines are renamed to the veteran block.
- Budgets re-derived against SRD 5.2.1 for four 4th-level characters (Low 1,000, Moderate
  1,500, High 2,000). Every base budget is unchanged (S3 1,500; S6 600; S7 800; S8 800; S9
  1,150; S13 1,350). New: S9 Nastier 1,450.
- Test-first: `test_bestiary_check.py` gained 8 tests (data, text blocks, `variant_problems`
  clean, a missing block, a missing card line, a base line that doesn't name the variant, a
  base line that reprints numbers, a variant's HP checked like any block). Red (8 failed),
  then green. `bestiary_check.py` now reads 28 blocks + 1 Nastier (was 25 + 3).

**Commands (after R1.4).**
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 294 passed (was 277).
- `python T/lint_5e.py --check` → OK (0 problems; 80 hard, 48 structure remain; or_skills
  12 → 11). The lint baseline was not rewritten.
- `python T/fact_check.py --check` → OK. 21 hits remain: retinues 0, down_not_out 0, and the
  rest is the R2 worklist. Re-baselined with `--baseline` (24 → 21).
- `python T/bestiary_check.py --quiet` → 28 blocks + 1 Nastier, 0 mismatches.
- `python T/pregen_check.py --quiet` → 5 pregens, 0 issues.

## Review-fix pass — R2

*Worker, 2026-10-10. Tasks R2.1–R2.7 of `docs/TASKS_oraga_5e_review_fixes.md`. Decisions
O48–O51 in DECISIONS.md; INVENTIONS #84; CARRYOVER §6 gains the QR4, QR1 and QR2 rows.
Every site was located by quote; none was missing.*

**R2.1 — household (QR1).** 02 timeline and Agenda 8, and 04 Undercurrent B: "cut by nearly
two-thirds". 04's opening: "Two years ago this palace kept a household of sixty; tonight…
about two dozen". 07 Corval header: "runs the whole ball with the twenty-two who stayed". B13's
twenty-two, Corval's "sixty"/"Twenty-two" and 08's rumor 11 truth note already agreed.
Undercurrent B's "simple arithmetic" spark now adds up (60 → 22).

**R2.2 — honor guard (QR2, O48).** New **Table VIII–7: The Honor Guard, Post by Post** in
chapter VIII's "Where Everyone Stands" (Rumors → VIII–8, Crystal Charges → VIII–9; 04's three
rumor pointers updated). Posts: the gate (all nine while the line comes in), the east-wing
doors (two; four in Mv V; two at midnight), B7 (three), with the household (four; two in Mv V),
the dais (seven at midnight). Sites: 04 Palace on Alert ("seven of the nine… two hold the
east-wing doors"), Steel in Movement I ("the two nearest guards"), B7, B9's box, Mv V (Corval
doubles from two to four); 05 Radiant sign (lanterns, no "guards'"), default beats ("Seven of
the nine"), The Snakes in the Dark; 08 Table VIII–2; 10 honor guard lore line; `flow.json`
(the dais node, the doubled guard). Table V–1's "a guard at the doors" and V–4's "the guards
off the east wing doors" now agree as printed. `facts.yaml` records the posts per Movement;
the `unless` on the guard check is now case-insensitive ("Seven of the nine").

**R2.3 — east wing and terraces (O33, O34, O49).** 05 General Features: the east wing is
upstairs (12-foot stair from the Court's east doors, corridor at gallery level, the private
stair is the garden stair) and a new *Elevations* bullet. 04 B2 and B9 notes and 08's caption
match. S9's box: "at the rail of the Court's garden walk… On the upper terrace below them";
the Draunel tells in 04 and 09 match; "Two terraces below" (04, 09) → "Down at the river gate".
S10 unchanged (already agrees); its rope-versus-garden-stair question is logged in O49 for R6.

**R2.4 — arrivals (O35, O50).** 01: the quiet attendant "who has been at the ball all evening
takes its place beside the Uninvited". Table V–6: the Hollow "(any Movement from III)", "(B10
edges, Mv III–V)", and both "(any social scene)" cells gain "Mv III–V".

**R2.5 — smaller fixes (O51).** P2-5 Maiven conditional (06). P2-7 Vell "before the boat
clears" (07, 10 ×2). P2-8 Scora (04 Undercurrent A) and Kshalo (08 rumor 9) glossed from V1/V3;
`tools/terms.txt` updated; `test_lint_5e.py`'s real-module test now asserts no Scora/Kshalo
hit. P2-9 "It is not long dark"; B4 "A vast crystal chamber". P3-7 "Intimidation never works on
this check". P3-8 the Wept's Fracture needs a witnessed tell, DC 15 at 2+ Delay (Table V–1).
P3-11 broadsword. P3-12 Tavva's three knives. P3-16 the patron's pitch (02 Agenda 2 Pays).
P3-18 the Second Clause gloss (05 B12).

**R2.6 — twenty blades (QR4).** 05 B12 branch: "twenty blades", "twenty sworn witnesses";
`flow.json` likewise. CARRYOVER §6: QR4 (F:05 L474, L479–480), QR1 (F:02 L68, F:03 L180, F:04
L17, L491, L503) and QR2 (F:04 L45, F:05 L103, F:enemies/boranis_honor_guard.fof L55, L59).
`adventures/` not edited.

**Tests.** `test_fact_check.py`: the first-run test became `test_module_agrees_after_r2` (0 hits)
plus `test_guard_posts_recorded` (each Movement's posts sum to nine; midnight 7 + 2; Mv V
doubles the doors).

**Commands.**
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 295 passed.
- `python T/lint_5e.py --check` → OK (80 hard, 46 structure remain; defined_terms 2 → 0). Lint
  baseline not rewritten.
- `python T/fact_check.py` → 0 hits (was 21). Re-baselined with `--baseline` to 0.
- `python T/bestiary_check.py --quiet` → 28 blocks + 1 Nastier, 0 mismatches.
- `python T/pregen_check.py --quiet` → 5 pregens, 0 issues.
- Flow page rebuilt (`flow/build_flow_page.py`). `software/tests/test_no_private_canon.py` → 5 passed.
