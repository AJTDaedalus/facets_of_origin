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
