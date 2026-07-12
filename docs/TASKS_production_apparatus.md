# TASKS — Production Apparatus (PHB + MM)

**Tier:** Planner (Opus) output — Worker (Sonnet) executes, except tasks marked **[FABLE]**
**Design:** `docs/DESIGN_production_apparatus.md`
**Review source:** `docs/RESEARCH_editorial_review.md` §D
**Log:** `docs/LOG_production_apparatus.md` (Worker creates on first task)

## Worker protocol

1. Read the DESIGN §-references cited by your task. Do **not** read the whole repo.
2. Pick **one** task. TDD where a test is named: write it, watch it fail, implement, watch it pass.
3. Update this file (`[x]` done / `[!]` blocked) and append to `LOG_production_apparatus.md`.
4. **Stop and report.** Do not start the next task without confirmation.
5. Escalate to Planner after 2 failed attempts, or if the task spec is ambiguous.

## Hard rules for this workstream

- **No rules changes.** This is apparatus. If a task seems to require deciding what
  happens at a table, the spec is defective — stop and escalate. Do not rule.
- **Quick refs compress, never paraphrase.** The glossary is a quick ref.
- **Skip [FABLE] tasks.** They create new canonical prose; a Worker must not attempt them.
- **Baseline: 965 passed, 1 failed.** The failure (`test_config.py::test_default_port_is_8000`)
  is pre-existing and environment-caused (`docs/TODO.md` T4). Do not fix it. Do not count it as yours.
- Running the full suite regenerates `playtest/02_silence_of_ashenmoor/digital_tool_log.md`
  (RNG churn). **Revert it before committing.**

---

## WAVE 0 — Test harness

### [x] PA-1 — Doc-consistency test module *(TDD; DESIGN §4.2, §5)*

Create `software/tests/test_docs_consistency.py`. This module is the safety net for
every task after it; it lands before any content moves.

**Files:** `software/tests/test_docs_consistency.py` *(new)*.

Implement two invariants now (the other four arrive with their tasks):

- **INV-5 — `test_cross_references_resolve`.** Walk every `Chapter <N>` citation
  (regex `Chapter ([IVX]+\.\d+[a-c]?)`) in `player_handbook/*.md` and `mm_manual/*.md`.
  Map each number to its file by filename prefix. Fail with the citing file, line,
  and unresolved number for any that has no file. **Must pass on today's text** —
  all 26 current references resolve. If one does not, that is a find: report it,
  do not fix it here.
- **INV-6 — `test_mm5_uses_typographic_dashes`.** `mm_manual/MM5_Quick_Reference.md`
  contains no ASCII `--` or `-->`. Regression guard on the closed D8 fix.

**Accept:** both tests pass against unmodified content; suite is 967 passed, 1 failed.

---

## WAVE 1 — Structure *(blocks all of Wave 2 and 3)*

### [x] PA-2 — Chapter renumber: II.4 → II.4 + II.4a *(DESIGN §4.1, §2.4)*

**Files:** `player_handbook/II.4_Character_Creation_Facets.md` (cut from),
`player_handbook/II.4a_Character_Creation_Facet_Body.md` *(new)*,
`player_handbook/Table_of_Contents.md`, `software/facets/base/facet.yaml` (header comment only).

**The cut.** Move exactly two spans out of II.4 into the new II.4a:
- `### Skills of the Body` — lines 44–57
- `### Facet of the Body — Technique Tree` through the end of the Iron branch — lines 103–204

Everything else stays in II.4. Do **not** rename `II.4_Character_Creation_Facets.md`;
retitle its H1 to `# Character Creation: Facets and Advancement`.

Give II.4a the H1 `# Character Creation: Facet of the Body` and the same shape as
II.4b/II.4c: skills table, then the Technique tree. Where II.4's Body-skills table
says *"(Skills of the Mind and Soul are defined in their respective Facet chapters.)"*,
keep the parallel wording II.4b/II.4c already use.

Then sweep the references:
- **ToC:** `II.4 Facets & Advancement (Body)` → four lines: II.4 Facets & Advancement,
  II.4a (Body), II.4b (Mind), II.4c (Soul).
- **`facet.yaml:9`** — header comment cites II.4 for the *Body Technique tree*; that
  moved. Retarget to II.4a. **Comment only — change no data.**
- Leave `websocket.py:308`, `websocket.py:1053`, `builder.js:362`,
  `test_websocket.py:1648` alone: they cite II.4 for the "only skills used this
  session" rule, which stays in II.4. Verify each still points at live text.
- Grep both books for any other `II.4` citation that means the Body tree; retarget it.

**Accept:** PA-1's INV-5 still passes; every Body-tree reference resolves to II.4a;
no rules text altered (`git diff` on II.4 + II.4a shows moves only, no rewording);
`facet.yaml` data unchanged; suite still 967/1.

---

## WAVE 2 — Content *(parallel; all unblock once PA-2 lands)*

### [x] PA-3 — Skill-text dedup *(TDD; DESIGN §4.3, §2.1, §2.2)*

Four copies of every skill description → two coupled homes.

**Files:** `player_handbook/II.6_Character_Creation_Skills.md` (canonical prose),
`player_handbook/II.4a_...Body.md`, `II.4b_...Mind.md`, `II.4c_...Soul.md` (drop
descriptions), `software/tests/test_docs_consistency.py` (INV-1).

1. **II.6 "The Skill List" becomes canonical.** Normalize all 15 entries to the
   long-prose format the five Body entries already use. Mind and Soul are currently
   one-line dash entries — expand them from the text that exists in II.4b/II.4c and
   `facet.yaml`. **Compress and merge existing text; write no new claims about any skill.**
2. **Delete the false pointers.** II.6:69 and II.6:85 claim full descriptions live in
   II.4b/II.4c. They do not (DESIGN §2.2). Remove both.
3. **The three Facet chapters drop their description columns.** Each keeps a table of
   skill name + governing attribute only, under: *"Full descriptions are in Chapter
   II.6 — Skills."*
4. **II.6's "Complete Skill Reference" table stays** — it is a legitimate quick ref.
   It must now be a strict compression of the prose list below it.
5. **`facet.yaml` is untouched.** Its `description` field is the data home.

**INV-1 — `test_skill_descriptions_match_facet_yaml`:** for each of the 15 skills,
the `description` in `facet.yaml` matches the skill's canonical prose entry in II.6.
(Normalize whitespace; assert the yaml description is contained in the II.6 entry —
II.6 prose may add a usage sentence, but must not contradict.)

**Accept:** each skill described in exactly one prose place (II.6) and one data place
(`facet.yaml`); INV-1 passes; the three Facet chapters carry name+attribute+pointer only.

### [x] PA-4 — Standardize roll markers *(DESIGN §4.4, §2.3)*

**Files:** `mm_manual/MM2_Session_Design.md`, `mm_manual/MM4_Running_the_Table.md`.

Roll-resolution lines in MM vignettes use a `>` blockquote; the PHB uses `→`. The MM
*also* uses `>` for advice callouts, so `>` currently means two things. Standardize
roll resolutions on `→`; leave callouts as `>`.

Convert lines matching `> <Name> rolls **2d6 + …**` to `→ <Name> rolls **2d6 + …**`
(known: MM2:404, MM2:424, MM2:458, MM4:193, MM4:203 — **grep, do not trust this list**).
Do not touch advice blockquotes (MM2:42, MM2:70, MM2:165 and kin). The inner notation
is already identical across both books — only the line marker changes.

**Accept:** no `> …rolls **2d6` remains in either file; every advice blockquote intact;
`git diff` shows only leading-marker changes.

### [x] PA-5 — Character sheet appendix *(TDD; DESIGN §4.5)*

**Files:** `player_handbook/Appendix_Character_Sheet.md` *(new)*,
`player_handbook/Table_of_Contents.md`, `software/tests/test_docs_consistency.py` (INV-2).

Build the sheet II.1:9-23 has always described: exactly six sections — Attributes,
Facet, Background, Skills, Techniques, Session Resources. Fillable markdown (blank
tables a player can print or copy). **Transcription, not design:** no seventh section,
no field II.1 does not name.

**INV-2 — `test_character_sheet_fields_map_to_model`:** every field on the sheet maps
to a field on `software/app/game/character.py`'s `Character` model. Assert the mapping
explicitly (a dict in the test); fail on any sheet field with no model home.

**Accept:** six sections, matching II.1; INV-2 passes; ToC lists the appendix.

### [x] PA-6 — Branch intro paragraphs — **[FABLE]** *(DESIGN §4.6)*

Six of nine Technique branches have no intro; Clarity/Instinct/Archive do. Write the
six missing ones (Might, Grace, Iron in II.4a; Presence, Fortune, Communion in II.4c)
to the Clarity template — ~2 sentences, names the attribute's character and what the
branch is for. New canonical prose. **Worker: skip.**

### [x] PA-7 — Front matter — **[FABLE]** *(DESIGN §4.7)*

`player_handbook/Front_Matter.md` *(new)*: credits/license page (GPLv3, repo URL,
TTRPG Safety Toolkit attribution, any SRD-derived material), "how to read this book"
(player path vs. MM path vs. optional modules), and the novice on-ramp — the
Introduction courts a first-time player and never points them at Quick Start. **Worker: skip.**

### [x] PA-8 — III.2's fate — **[BRAIN → FABLE]** *(DESIGN §4.8, §7 Q1)*

**Ruled and executed (Brain B1, 2026-07-12): grown, not folded.** Planner recommended *grow, do not fold*: Threat Clocks
exist because hazards are not combat, and folding the death rules into III.3 implies
death is a combat outcome — the opposite of what they say. Growing it means the two
worked examples it lacks (a clock filling; a scar-or-heroic-death choice). **Worker: skip.**

---

## WAVE 3 — Derived artifacts *(blocked on all of Wave 2)*

### [x] PA-9 — Glossary *(TDD; DESIGN §4.9)*

**Files:** `player_handbook/Glossary.md` *(new)*, `player_handbook/Table_of_Contents.md`,
`software/tests/test_docs_consistency.py` (INV-3).

40–50 entries — every proper noun the system defines. Format:
`**Term** — one- or two-sentence definition. *(Chapter X.Y)*`

Seed list (extend by grepping for bolded proper nouns; this is not exhaustive):
Attribute (Major/Minor) · Facet · Primary Facet · Cross-Facet · Facet Level · Technique ·
Branch · Tier · Major Advancement · Career Advance · Skill · Rank (Novice/Practiced/
Expert/Master) · Mark · Skill Point · Background · Starting Skill · Secondary Skill ·
Specialty · Spark · Graceful Fail · Exchange · Posture (Aggressive/Measured/Defensive/
Withdrawn) · Strike · Press · Reaction (Dodge/Parry/Absorb/Intercept) · Endurance ·
Condition (Tier 1/2/3) · Staggered · Cornered · Broken · Resolve · Rider · Armor ·
Mook · Named NPC · Boss · Threat Rating · Encounter Budget · Threat Clock · Difficulty
(Easy/Standard/Hard/Very Hard) · Full success · Partial success · Domain · Intent ·
Scope (Minor/Standard/Major) · Focused/Standard/Prismatic domain · Ascendant Domain ·
Second Domain · Contested Roll · Group Roll · Support · Maneuver · Mirror Master ·
Reflection Scene

**This is a quick reference — it may only compress canonical body text.** If a term has
no canonical definition anywhere in either book, that is a finding: **report it, do not
define it.** Inventing a definition is inventing a rule.

**INV-3 — `test_glossary_pointers_resolve`:** every entry's `(Chapter X.Y)` pointer
resolves to an existing file, and that file contains the term.

**Accept:** every system proper noun has an entry; INV-3 passes; any term with no
canonical source is reported, not invented; ToC lists the glossary.

### [ ] PA-10 — Index generator *(TDD; DESIGN §4.9; **blocked on Q2**)*

**Q2 resolved (Brain B2, 2026-07-12): digital-first confirmed, no print milestone exists.**
This task is the right artifact as specified. If a print run is ever scheduled, the
page-number index is a *new* layout-tool task; it does not modify this one.

**Files:** `software/tools/build_index.py` *(new)*, `player_handbook/Index.md`
*(generated)*, `software/tests/test_build_index.py` *(new)*,
`software/tests/test_docs_consistency.py` (INV-4).

The index is **generated, not written** — a hand-maintained index in a moving ruleset
goes stale, and a stale index misdirects with confidence. It doubles as the
"bidirectional cross-reference layer" the review asks for.

`build_index.py` reads the term list from `Glossary.md`, walks `player_handbook/` and
`mm_manual/`, and emits per term every chapter + heading where it appears, sorted,
with links.

**INV-4 — `test_index_is_up_to_date`:** regenerating produces no diff (lockfile pattern).

Per `CLAUDE.md`'s 3-tests-per-public-function rule, `test_build_index.py` also covers:
happy path; a term appearing in zero sections; a term appearing in a heading vs. body text.

**Accept:** `Index.md` generated and committed; INV-4 passes; `build_index.py` has ≥3 tests.

### [ ] PA-11 — ToC and final sweep

**Files:** `player_handbook/Table_of_Contents.md`, plus anything the sweep finds.

Final pass: ToC reflects the new II.4/II.4a split, Front Matter, Glossary, Index, and
the Character Sheet appendix. Run the whole suite. Confirm INV-1 through INV-6 green.

**Accept:** ToC lists every shipped file; full suite green except the known T4 failure;
`playtest/02_silence_of_ashenmoor/digital_tool_log.md` reverted.

---

## Status

| Task | Tier | Blocked on | State |
|---|---|---|---|
| PA-1 test harness | Worker | — | **done** |
| PA-2 renumber | Worker | PA-1 | **done** |
| PA-3 skill dedup | Worker | PA-2 | **done** |
| PA-4 roll markers | Worker | PA-2 | **done** |
| PA-5 character sheet | Worker | PA-2 | **done** |
| PA-6 branch intros | **Fable** | PA-2 | **done** |
| PA-7 front matter | **Fable** | — | **done** |
| PA-8 III.2 | **Brain → Fable** | Q1 ruled (B1) | **done** |
| PA-9 glossary | Worker | all of Wave 2 | **done** |
| PA-10 index | Worker | PA-9 (Q2 ruled, B2) | **ready** |
| PA-11 ToC + sweep | Worker | PA-10 | — |
