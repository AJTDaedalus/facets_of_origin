# Style Audit — Remediation Log

Execution log for `docs/RESEARCH_style_audit.md`. Waves as defined in that
document's remediation plan. Full suite: **1297 passed**.

---

## Wave 1 — mechanical, testable (COMPLETE)

**S1 — numbered tables.** 78 tables captioned `**Table <chapter>–<n>: <Title>**`
across 18 files (72 in the two books, 6 in Oraga Night). New generator
`software/tools/build_table_register.py` writes `player_handbook/List_of_Tables.md`
(72 entries, links resolved to each table's nearest enclosing heading). ToC gained a
List of Tables line, and the Glossary/Index lines gained the job labels the guide's
"navigation aids reference each other" convention asks for.

Excluded by design and recorded in the test: `Appendix_Character_Sheet.md` (blank
form grids, not lookup tables), `Table_of_Contents.md`, `Index.md`,
`List_of_Tables.md`, `List_of_Boxes.md` (the finding aids themselves).

**S6 — cross-reference idiom.** Six unresolvable pointers replaced with
section-name-plus-number citations (`II.4:79`, `III.1:35`, `MM1:11`, `MM1:165`,
`MM2:34`, Oraga `03:20`). Enforced going forward by INV-11.

**S8 — capitalization.** *Downgraded on measurement.* The audit's count of ~100
mid-sentence capitalizations of undefined terms was wrong: it counted Title Case
headings and bold field labels, where Title Case is correct (`rulebooks.md` §2).
After excluding those, the corpus had **zero** genuine prose offenders — `Skill`
is glossary-defined, and every hit for `Scene` / `Roll` / `Action` was a heading.
The invariant (INV-12) was still added, because the discipline is worth pinning.

**S9 — typography in Background entries.** 78 field labels converted from italic
(`*Description:*`) to bold across all 15 pre-built Backgrounds, matching the legend
that defines them. Bold now means "field label" and italics mean "named game
object" everywhere in II.5, with no overlap.

**P4 — skill-description duplication.** Dropped the Description column from
Table II.6–1, leaving it a Skill/Facet/Attribute lookup, and added a line naming
*The Skill List* as the single definition home. INV-1 (facet.yaml ↔ II.6 prose)
still passes, and there is now one copy of each description instead of two.

**O5 — Oraga area codes.** The Audience Hall was B11 sitting between B3 and B4.
Renumbered to B4 with B4–B10 shifting up one; 111 code references updated across
four module files. Codes now ascend in reading order, which is the only thing a
shared identifier has to do.

**O8 — path citations.** Four `in \`enemies/\`` directory pointers replaced with the
specific `.fof` files they meant. These become anchors once the bestiary chapter
exists (Wave 6).

**New invariants** in `software/tests/test_docs_consistency.py`:

| INV | Guards |
|---|---|
| INV-9 | every lookup table has a numbered caption; designations unique and 1..n per chapter |
| INV-10 | `List_of_Tables.md` is byte-identical to a fresh regeneration |
| INV-11 | no "see below" / "as mentioned above" pointers |
| INV-12 | no capitalized term the Glossary does not define |

---

## Wave 2 — declare the formats (COMPLETE)

**S2 — sidebar taxonomy.** `Front_Matter.md` gained a "The Boxes" section
declaring five species: *Through the Mirror*, *MM Note*, *Example*, *Variant*,
*Reading the Entries*. All 43 existing boxes retagged into exactly one; four boxes
that held baseline rules were **unboxed** into body text instead, per the rule the
declaration now states ("a rule the game always uses is never in a box at all") —
III.3's full-reaction case, MM1's TR minimums, II.3's Graceful Fail note and
pre-Technique scope cap.

Current distribution: 18 Example, 16 MM Note, 14 Through the Mirror,
2 Reading the Entries. *Variant* is declared but unused — the optional Facet
modules are its eventual home.

**S3 — Through the Mirror boxes.** Six written, all stating recorded design
intent rather than invented rationale (sourced from `docs/DECISIONS.md` P8/P11 and
the 2026-03-13 playtest ruling):

1. Why NPCs never roll — III.3, *Enemy Attacks*
2. Why enemies lose Resolve and characters take Conditions — III.3, *Conditions*
3. Why Tier 1 Conditions clear so fast — III.3, *Tier 1 Conditions*
4. Why armor is a budget and not a subtraction — IV.1, *Armor*
5. Why early magic is capped by scope, not difficulty — II.3, *Acquiring a Domain*
6. Why a quick reference may never introduce a rule — MM5, opener

Each names what breaks if the rule is house-ruled away, which is the field
`gm_books.md` §5 identifies as the point of the device.

**S4 / P1 / P2 — Technique entries.** All 57 Techniques rebuilt to one field order:

```
**Name** *(Branch, Tier N — Attribute)*
**Use:**     Passive / At will / Once per scene / Once per session (+ any cost)
**Choose:**  the one-time decision, where there is one
**Roll:**    the roll the Technique itself calls for, where it calls for one
<the rule, in prose>
**Normal:**  the baseline it departs from
```

`facet.yaml` gained `use`, `normal`, and (where applicable) `roll` for all 57, so
the data and the book carry the same fields. A "Reading the Entries — Techniques"
legend was added to II.4 ahead of the three trees.

Every `Normal:` line restates a baseline the books already publish and cites where
it lives. **None settles an open question** — where a Technique's interaction with
another rule is genuinely unwritten (see Open Questions below), the Normal line
states the baseline and stops.

**Bug found and fixed during this work.** `Second Domain` and `Ascendant Domain`
exist in both the Mind and Soul trees. The first pass keyed Technique metadata by
name, so the Soul entries silently overwrote the Mind ones and II.4b briefly told
Mind casters to choose from the Domains of the *Soul* list and roll *Spirit*.
Corrected, and pinned by `test_technique_headers_match_facet_yaml`, which compares
each printed header against facet.yaml per-Facet rather than per-name.

**P3 — Skill entries.** All 15 entries gained a `*(Facet — Attribute)*` header and
a `**Roll:**` field, plus a "Reading the Entries — Skills" legend.

*Delivered narrower than the audit specified, deliberately.* `rulebooks.md` §4's
skill shape includes **Time:**, **Retry:**, and **Untrained:** fields. FoO has no
per-skill time cost, no per-skill retry rule (retries are one standing ruling in
III.1), and no untrained state at all — every character holds every skill at
Novice, which is a real rank with a real modifier. Writing those three fields would
have meant inventing rules to fill them, which the project's iron law forbids. The
legend says so explicitly instead, so a reader looking for the missing fields is
told why they are missing rather than left wondering.

**New invariants:**

| INV | Guards |
|---|---|
| INV-13 | every box declares one of the five species; Front_Matter declares every species in use |
| INV-14 | every Technique has `use` + `normal` in facet.yaml, a full header in the book, a printed Normal line, and a header that agrees with facet.yaml |

---

## Wave 3 — the missing registers (COMPLETE)

**S5 — chapter hooks.** Fifteen chapters gained a 1–3 paragraph hook before the
first A-head, and every filler `## Overview` / `## Introduction` / `## Philosophy`
A-head was deleted and folded into it. `MM4_Running_the_Table.md` was already
correct and was used as the model.

**P7 — fourth-wall breaches.** Both fixed. III.3 no longer opens by comparing FoO
to other games; it opens on six guards coming through a door. IV.1's rope joke is
gone. The comparison in `I_Introduction.md` was left alone — the guide sanctions
positioning talk at introduction level.

**P8 — IV.1's Philosophy head.** Replaced by a hook; the designer-register content
moved into a Through the Mirror box where it belongs.

**S10 — cast vignettes.** Six added, all in the established Thornwall arc and using
`references/phb-examples.md` voices: III.1 (a front-desk scene running all three
outcome tiers with the difficulty called aloud before each roll), IV.1 (spending
an armor budget), MM1 (rating an enemy from scratch, both directions), II.1
(building Zulnut in six steps), II.4a (*Forcing Hand*), II.4b (*Sharp Analysis*).

The III.1 vignette is the one that mattered most — the chapter that owns 2d6,
Sparks, difficulty, and the three tiers had no worked example at all.

Files still without the cast — `Appendix_Character_Sheet`, `Appendix_Magic_Domains`,
`Glossary`, `Table_of_Contents`, `I_Introduction`, `MM5` — are legitimately exempt:
forms, catalogs, finding aids, and a scan card.

**P5 — difficulty benchmarks.** Table III.1–5 pairs each tier with a concrete task
and the rank that clears it most of the time, which is the fourth column
`gm_books.md` §5 identifies as the one that converts an abstract scale into social
knowledge.

**S7 — de-bulleting.** III.1's Spark triggers and saving-throw categories became
prose under run-in labels. 59 bold run-in bullets across five files became
paragraph leads. The domain appendix's italic field labels became bold, which was
also why it counted zero run-in labels in the audit.

*Correction applied during this work:* the first pass fragmented mixed lists — a
converted paragraph sitting in the middle of surviving bullets reads as a break in
the list, not as emphasis. Twelve items in MM5, MM4, and MM2 were put back. Genuine
checklists (observable table-energy signals, option menus) were left as bullets
throughout; MM5 is a scan card and keeps its bullets.

**P6 — tiered lore boxes.** Not done. The device needs per-subject canon to fill
(what a character notices at 6−, learns at 7–9, uncovers at 10+), and inventing
that is the iron law's territory. Flagged for the user rather than guessed at.

---

## Wave 4 — MM Manual apparatus (COMPLETE)

**M1 — sub-skill decomposition.** MM1, MM2, and MM3's hooks now name the chapter's
job and break it into 3–5 named sub-skills, which the chapters then follow.

**M3 — prep by the clock.** MM2 gained a cumulative, worst-case-first prep ladder:
twenty minutes / one hour / two hours / four-or-more (with a stated reason to stop),
plus the under-twenty-minutes technique and the instruction to cancel rather than
run a session you resent prepping.

**M4 — a 2d6 scene table.** Table MM2–2, weighted on the curve with the commonest
result at 7, every entry phrased as an active want, and four footnote expansions
turning the non-obvious rows into runnable scenes — including the instruction to
pay a Spark for the 7 and to let the 12 be genuinely real.

**M5 / M6 — MM5's opener and the registers.** MM5 gained a statement of what it is
and when to reach for it. `List_of_Boxes.md` joins `List_of_Tables.md` as a
generated finding aid; both are in the ToC.

**M2 — worked artifacts.** Partial. MM1 now ships a complete worked rating; MM2
ships the prep ladder and the scene table. Neither MM2 nor MM3 ships a full
finished session plan or campaign frame at production quality — Oraga Night is the
corpus's one complete worked artifact, and the honest fix is for MM2/MM3 to point
at it as their exemplar. Left for the user.

---

## Wave 5 — Oraga Night (COMPLETE)

**O1 — intro battery.** `01_Overture.md` restructured to the seven-part sequence:
what the adventure is (party size, expected Facet level, length) → what you need →
the story so far → a Movement-by-Movement synopsis, each ending with the
world-state → converging hooks that all begin at B1, Movement I → what the night
pays → a format legend documenting the module's own conventions. The duplicated
"What You Need" section was removed.

Deliberately not added: a one-page italic fiction prologue. Writing one means
inventing a scene in the user's setting.

**O2 — read-aloud.** Eight triggered blocks where the module previously had none:
the approach and the gatehouse (Movement I), the Audience Hall summons (III), the
Dead Dance (V), the lights dying mid-sentence (VI), and first entry into B2, B4,
B6, and B9. Every block has an explicit trigger line in MM voice, stays on
perception, never names a creature, and never says what anyone feels or does. All
detail is drawn from what the module already establishes — rose-lit crystal, the
worn dais, Elanna's tended niche, the inward-facing guard.

**O4 — printed rewards and morale.** The Overture gained *What the Night Pays*:
six named awards, including one for reading an omen before it is explained, one for
ending a fight without finishing it, and one per person carried out in Movement VII.
The module previously said "Spark" four times in 2,556 lines. Morale is handled
under E2 — every module enemy now carries a typed morale line.

**O3 / O6 / O7 — not done.** The keyed-area field battery, maps with scale lines
and terrain-as-rules, and one-page scene cards are all real gaps. They are also
substantial layout work on a module that reads well as prose, and O6 in particular
needs cartography this project does not yet have. Recorded, not attempted.

---

## Wave 6 — the bestiary (COMPLETE, with a stated boundary)

**E2 — typed conduct.** `Enemy` gained six fields ordered by the moment the MM
needs them: `disposition`, `first_target`, `triggers`, `morale`, `organization`,
`negotiation`. All twelve shipped `.fof` files migrated — the behaviour was already
written, in freeform `notes` blobs under per-file ALLCAPS labels (`CONDUCT:`,
`ENTIRELY WINNABLE:`, `Posture tendency:`), where nothing could find or render it.
Nothing was invented; every line traces to the file it came from or to the module
chapter that already stated it.

Wired through the REST body so the enemy builder can set them. `tactics` is
untouched and stays free prose. New tests pin that every shipped enemy states a
disposition and a morale line, that every Boss states a negotiation surface, and
that legacy files without any of it still load.

**E1 — first attempt, since superseded.** Wave 6 shipped a generated
`mm_manual/MM6_Bestiary.md`: stat blocks and finding aids from `enemies/*.fof`, with
the narrative layer (read-aloud openers, ecology, tiered Lore boxes) deliberately
left out on the grounds that it was canon rather than data.

**That boundary was drawn too conservatively, and Wave 7 replaced it.** The
narrative layer does not require the user's setting — it requires *a* setting, and
writing the creatures as deliberately placeless made it writable. MM6 was deleted;
see Wave 7 below for what shipped instead.

| INV | Guards |
|---|---|
| INV-15 | the Bestiary's stat blocks and `Finding_Aids.md` regenerate to no diff, and every family entry carries a complete Lore box |

---

## Verification

Full suite **1297 passed** (4m45s) at the close of Wave 6. Seven new invariants,
INV-9 through INV-15. Three generators produce files that must not be hand-edited:
`build_index.py` → `Index.md`; `build_table_register.py` → `List_of_Tables.md` and
`List_of_Boxes.md`; `build_bestiary.py` → `bestiary/Finding_Aids.md` and every
in-chapter stat block (see Wave 7 — this pointed at `MM6_Bestiary.md` until that
chapter was superseded).

---

## Wave 7 — the Bestiary (2026-08-02)

Commissioned by the user as a third core book, which closed three of the four
items the first pass had deferred.

**The book.** `bestiary/` — Front Matter, four chapters, and generated finding
aids. **Eighteen stat blocks across nineteen entries** (the hushfall has none by design), TR 1 through 17, in families that each ship
their ladder: Chalk Hounds, Glassbacks, Ledgerlice, the chicken, the Ordinary
Dangerous, the Bought, the Kindly, the Latchmen, the Waiting, the Unfinished, and
one hushfall that deliberately has no stat block at all.

Thirteen new `.fof` files; the five existing core enemies were folded in and given
the prose layer they never had. The Archive Guardian became the Latchmen's Boss
expression, which is what it always was.

**Copyright posture.** Every creature is original to this project. Nothing is
derived from, named after, or mechanically modelled on any proprietary bestiary,
and the Front Matter says so in its own section rather than burying it. The
design consequence is recorded there too: these were built backwards from FoO's
own mechanics — a chalk hound cannot strike from a standstill *because standing
still is a decision a player can make*, and a latchman states its instruction
aloud *because listening is a thing players do*.

**Setting posture.** Nothing in the book is Shattered Origin canon, and every
family carries an **Adaptation** line saying what to change and what to keep.
`docs/TODO.md` T6 records that the setting's author has not ruled on placement and
that nothing should be placed until they do.

**Prose hand-written, numbers generated.** Chapters carry
`<!-- statblock: chalk_hound -->` markers; `software/tools/build_bestiary.py`
fills them from `enemies/*.fof` and writes `Finding_Aids.md` whole. The book and
the stat files cannot disagree — `monster_books.md` §9's format-drift
anti-pattern is structurally impossible rather than merely discouraged.

**Findings this closed:**

- **E1** — the bestiary chapter, now with the narrative layer the generated MM6
  stub could not have: read-aloud openers, lore in confident present tense, tiered
  Lore boxes, labelled sample encounters, ecology, and Adaptation notes. MM6 was
  deleted; it was scaffolding for this.
- **P6, tiered lore boxes** — the device is now native and used eleven times, one
  per family, keyed to 6− / 7–9 / 10+ and written as sentences the MM reads aloud.
  INV-15 fails if a family lacks one or a box lacks a tier.
- **M2, worked artifacts** — MM1 now points at the Bestiary; MM2 and MM3 each gained
  an MM Note pointing at Oraga Night as the finished artifact their advice
  describes. Writing a second complete session would have duplicated it.

**One design rule the book enforces on itself:** every creature ships a way out.
Eight of the eighteen statted creatures carry a full **Negotiation** surface — what it wants, what
shifts it, what deal it honours — and the other ten carry a morale line written to
fire early and mean it. The one creature with no deal available at all, the Archive
Guardian, says so in its entry and explains why: the office that could have called
it off no longer exists. `Finding_Aids.md` carries a third table listing every
negotiable creature and what it wants, so an MM who wants a scene rather than a
fight can find one by looking rather than by reading.

**Books, not book.** The PHB Front Matter, `Table_of_Contents.md`, `README.md`,
and `CLAUDE.md` all now describe a three-book line, and
`test_docs_consistency.py::_book_files` includes `bestiary/` — so every apparatus
invariant applies to it.

---

## Still deliberately not done

- **O3, keyed-area field battery** — a large layout pass on Oraga Night prose that
  currently works. Recorded in `docs/TODO.md` **T5**.
- **O6, maps** — needs cartography. `docs/TODO.md` **T5**.
- **O7, one-page scene cards** — depends on O6. `docs/TODO.md` **T5**.
- **Oraga Night's fiction prologue** — one page of italic fiction in the user's
  setting. `docs/TODO.md` **T5**.
- **`visual_layout.md`'s print dress** — out of scope for markdown sources, as the
  audit already recorded.

All four Oraga items were **deferred by the user on 2026-08-02**, not dropped.

---

## Open questions for the user

Surfaced by the `Normal:` work, not created by it. Each is a real gap in the
published rules that the field format made visible. None has been resolved in the
text — the Normal lines state the baseline and stop.

1. **Do Technique difficulty steps stack with the MM's situational adjustment?**
   Six Techniques (*Weapon Mastery*, *Steady Hand*, *Acclimated*, *Field of
   Mastery*, *Pressure Point*, *The Uncanny Angle*) make a roll "one difficulty
   step easier". III.1 says the MM sets difficulty and adjusts one step from the
   situation. Nothing says whether a Technique's step is inside that one-step
   budget or additional to it — so a Weapon Mastery character against a Defensive
   opponent is either Standard or Easy depending on who is running the table.

2. **Does *Second Domain*'s one-step penalty stack with a Broad domain's table?**
   *Second Domain* is one step harder than the primary domain; *Ascendant Domain*
   uses the Broad table whose Major ceiling Sparks cannot move. A character holding
   both has no written answer for a second prismatic working.

3. **Is *The Final Blow* subject to the "riders never defeat" rule?** It removes a
   target "regardless of any remaining resources", which reads as an intentional
   override of Resolve depletion, but III.3's rider rule is stated absolutely.

These want a Planner or Brain ruling, not a Worker fix.

---

## ESCALATION — Planner → Brain (2026-08-02)

**Raised by:** style-audit remediation, Wave 2. Adding `**Normal:**` fields to all
57 Techniques required stating the baseline each one departs from. Three of those
baselines turned out not to exist.

**Why this blocks planning rather than merely being interesting.** Each question
has two or more readings that are individually defensible and that produce
*different numbers at the table*. A Planner can pick one; a Planner cannot tell
whether the pick holds up against the simulation corpus, the four-rung ladder, and
whatever advancement content lands next. All three touch the same underlying
mechanism, so they should be answered together or not at all.

### Q1 — Do Technique difficulty steps compose with situational adjustment?

Six Techniques make a roll "one difficulty step easier": *Weapon Mastery*,
*Steady Hand*, *Acclimated*, *Field of Mastery*, *Pressure Point*, *The Uncanny
Angle*. III.1 says the MM sets difficulty and the guide's guardrail is "one step,
never two."

Nothing states whether a Technique's step sits *inside* that budget or *on top of*
it. A Weapon Mastery character striking a Defensive opponent is Standard under one
reading and Easy under the other.

### Q2 — Does *Second Domain*'s penalty compose with the Broad table?

*Second Domain* is one step harder than the primary domain. *Ascendant Domain*
uses the Broad table, whose Major-scope ceiling Sparks cannot move. A character
holding both has no written answer for a second prismatic working.

### Q3 — Is *The Final Blow* subject to "riders never defeat"?

It removes a target "regardless of any remaining resources", which reads as a
deliberate override of Resolve depletion. III.3's rider rule is stated absolutely.

### Engine facts the Brain pass needs

1. **Difficulty is a four-rung labelled ladder, and it clamps.** Easy +1 /
   Standard 0 / Hard −1 / Very Hard −2 (`facet.yaml roll_resolution`).
   `engine._step_difficulty_harder` / `_easier` clamp at both ends
   (`min(idx+1, len-1)`, `max(idx-1, 0)`). There is no accumulator and no fifth rung.
2. **The engine never computes difficulty.** Every handler takes
   `difficulty_label` straight off the client message
   (`websocket.py:275, 310, 585, 728, 928, 1111`). The MM picks a label in the UI.
   **No Technique difficulty step is implemented anywhere in the engine** — all six
   are book-only instructions a human applies by choosing a different label.
3. **Three one-step shifts *are* implemented**, all in `combat.py`:
   `maneuver_target_difficulty`, `enemy_posture_reaction_difficulty`,
   `target_strike_difficulty`. These are the precedent for how a step is
   modelled, and they are all single, non-composing shifts off a base label.
4. **Order matters under clamping.** Two steps in opposite directions commute
   only away from the ends. From Easy, harder-then-easier returns Easy; from Very
   Hard, easier-then-harder returns Very Hard. Any ruling that permits composition
   has to say what order they apply in.
5. **The simulation corpus was calibrated at specific labels** (Series 7 and 9,
   `research/simulation_log.md`). A ruling that shifts typical Strike difficulty
   by one rung moves win rates the Encounter Recipe Table publishes as validated.

**Recommended:** switch to Fable to resolve this before any further Technique work.
Output belongs in `docs/BRIEF_technique_difficulty.md`.

### Resolution (Brain, Fable, 2026-08-02)

**Resolved in `docs/BRIEF_technique_difficulty.md`.** All three ruled; summary:

- **Q1 — compose, ordered, clamped.** The MM's situational label first, the
  character's step second, ladder clamps. Guardrail: character-side steps never
  stack with each other — at most one per roll, whatever the source. Decisive
  evidence: III.3:513 already prints exactly this pattern in a play example
  ("Standard difficulty, but Weapon Mastery makes this one step easier, so
  Easy"). The book had already ruled it and never said so.
- **Q2 — no stack; the penalty rides the grant route.** Ascendant Domain's
  prismatic territory prices off the Broad table alone. Ratifies what
  `character.py:406–410` and `engine.py:330–338` already deliberately implement.
  Also fixes a latent wording defect (see below).
- **Q3 — full override.** *The Final Blow* is not a rider, so III.3:140 is not
  about it and stays verbatim. Works on Bosses. Must be implemented as a defeat
  event through the canonical path, never a raw `resolve_current` write (P11).

**Corpus:** intact for all three. `standard_party()` carries no Techniques
(`combat_sim.py:973–981`), so Series 7 and 9 stand as published. One advisory
sentence goes in MM1; no re-run gated.

**Bug found in passing.** *Second Domain* reads "one difficulty step harder **than
your primary domain**" (II.4b, II.4c, `facet.yaml` ×2, MM5:258). Read literally, a
Focused-primary caster's second standard domain prices at Focused-plus-one, which
*is* the standard table — silently deleting the penalty. The engine's reading
("harder than normal for that domain") is the intended one and becomes canonical.
Five surfaces, one commit.

**Status:** ✅ Resolved by Brain. Return to Planner to plan the prose, `facet.yaml`,
engine, and test tasks per the brief's implementation posture.
