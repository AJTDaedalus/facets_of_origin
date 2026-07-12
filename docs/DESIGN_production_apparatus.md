# DESIGN — Production Apparatus (PHB + MM)

**Tier:** Planner (Opus)
**Source:** `docs/RESEARCH_editorial_review.md` §D (items D1–D10)
**Handoff:** `.claude/handoffs/2026-07-11-editorial-followup.md` §Next Steps 2
**Tasks:** `docs/TASKS_production_apparatus.md`
**Status:** awaiting owner sign-off; two questions escalated to Brain (§7)

---

## 1. Scope

Section D of the editorial review lists ten production gaps — the apparatus a
published book ships with and this one does not. None is a rules error. All are
structural, and several are coupled hard enough that doing them in list order
would mean doing some of them twice.

**In scope:** glossary, index, character sheet appendix, chapter renumbering,
skill-text deduplication, branch intro paragraphs, roll-marker standardization,
front matter, III.2's fate.

**Out of scope:** the deferred deep prose rewrite (owner ruling, still deferred);
any rules change. If a task in this design appears to require a rules decision,
that is a spec defect — escalate, do not rule.

**D8 (MM5 ASCII dashes) is already closed** — the editorial pass normalized them.
It is dropped from the work list; a regression guard replaces it (§5, INV-6).

---

## 2. Survey — corrections to the review's §D

The review's §D was written from a read of the books. Four things look different
once you also read `facet.yaml` and grep the cross-references.

**2.1 Skill text is quadruplicated, not triplicated (corrects D5).** The review
found three copies: the Facet chapters, II.6's table, and II.6's prose list.
There is a fourth — `software/facets/base/facet.yaml` carries a `description`
field per skill (`facet.yaml:150-155` et seq.), and its text tracks II.6's prose
list. That changes the fix. With only prose copies, "make II.6 canonical" is
enough. With a data copy in the file `CLAUDE.md` already names the single source
of truth for mechanics, the dedup has to nominate *two* canonical homes and bind
them together — see §4.3.

**2.2 II.6's pointers to the Facet chapters are false.** II.6:69 and II.6:85 say
"Full descriptions are in Chapter II.4b / II.4c." They are not. II.4b and II.4c
carry a *table* whose text is byte-identical to II.6's own dash-list. The pointer
sends a reader to a shorter version of what they are already reading. II.6's Body
section carries no pointer at all. Whatever the dedup decides, these three
sections must end up consistent with each other.

**2.3 The `>` marker is already load-bearing in the MM (sharpens D7).** The review
frames D7 as "`→` in the PHB, `>` blockquote in MM2/MM4." True, but the MM also
uses `>` for *callouts* — MM2:42, MM2:70, MM2:165 are advice boxes, not rolls.
So in the MM, `>` means two different things, and a reader cannot tell a roll
resolution from a sidebar by its marker. That is an argument for standardizing on
`→`, not on `>` (§4.4).

**2.4 Renumbering reaches into `software/` (extends D4).** Six comment and
docstring lines cite `PHB II.4` as the authority for the "only skills used this
session" advancement rule (`websocket.py:308`, `websocket.py:1053`,
`builder.js:362`, `test_websocket.py:1648`, plus two `facet.yaml` header
comments). That rule stays in II.4 under the new scheme, so the citations stay
correct — but `facet.yaml:9` cites II.4 for the *Body Technique tree*, which
moves. Renumbering is not a docs-only change.

---

## 3. Architecture — three waves, not ten items

The ten items are not independent. Two facts drive the whole shape:

**Renumbering invalidates every cross-reference.** Any artifact that points at a
chapter — glossary entries, index, ToC, the software comments in §2.4 — is
written against a numbering scheme. Build them before the renumber and you build
them twice.

**The glossary and the index are derived artifacts.** A glossary is, by this
project's own law, a quick reference: *"a compression of canonical body text,
never a new rule."* An index is a pure function of the finished text. Both go
stale the moment a chapter changes, and a stale index is worse than none —
it sends readers to the wrong place with full confidence. Hand-maintaining them
in a living ruleset is a losing bet, and this project has already been bitten
once by two copies of a rule drifting apart (the `combat.py` extraction).

So: **the index is generated, not written** (§4.9), and **both are covered by
invariant tests** (§5). The apparatus ships with the machinery that keeps it true.

```
WAVE 0 — test harness (enables everything; no content change)
  PA-1  doc-consistency test module + cross-reference resolver
           ↓ (must be red on today's text, green after PA-2)
WAVE 1 — structure (blocks everything downstream; one file split)
  PA-2  chapter renumber: II.4 → II.4 (shared) + II.4a (Body tree)
           ↓
WAVE 2 — content (parallel; independent of each other)
  PA-3  skill dedup          PA-6  branch intros      [FABLE]
  PA-4  roll markers         PA-7  front matter       [FABLE]
  PA-5  character sheet      PA-8  III.2's fate       [BRAIN → FABLE]
           ↓
WAVE 3 — derived (must be last; a function of the finished text)
  PA-9  glossary  →  PA-10  generated index  →  PA-11  ToC + final sweep
```

Wave 2 is where the tier split lands. PA-3/4/5 are mechanical — Worker (Sonnet).
PA-6/7/8 create new canonical prose in a voice the owner has ruled on twice, and
per the handoff they lean Brain/Fable. The Worker must **skip** them, not attempt
them.

---

## 4. Per-item design

### 4.1 PA-2 — Chapter renumbering (D4)

Adopt the review's scheme, with the minimum file churn that achieves it.

| | Now | After |
|---|---|---|
| Shared rules | II.4 (mixed with Body tree) | **II.4** — Facets & Advancement |
| Body tree | II.4 (§§ "Skills of the Body", "Facet of the Body — Technique Tree") | **II.4a** — Facet of the Body *(new file)* |
| Mind tree | II.4b | II.4b *(unchanged)* |
| Soul tree | II.4c | II.4c *(unchanged)* |

**The cut.** `II.4_Character_Creation_Facets.md` is 287 lines. Move out exactly
two spans — `### Skills of the Body` (44–57) and `### Facet of the Body —
Technique Tree` through the end of the Iron branch (103–204). Everything else
(What Is a Facet, the Skills concept + rank table, Advancing Skills, Facet Levels,
the Techniques concept, Major Advancement, Reflection, Advancement at a Glance,
Career Advances) is shared and stays.

**Filenames.** Keep `II.4_Character_Creation_Facets.md` on its existing path —
retitle the H1 to "Facets and Advancement", do not rename the file. Create
`II.4a_Character_Creation_Facet_Body.md`, matching the `b`/`c` naming. Renaming
II.4 would churn git history and every existing reference to buy nothing.

**Why this split and not "fold the trees into one chapter":** the three trees are
what a player reads *once*, at character creation, for the Facet they picked. The
shared rules are what the whole table re-reads at every level-up. They have
different readerships and different lifespans. Splitting them is what the ToC has
been quietly claiming since it was written ("II.4 Facets & Advancement (Body)").

### 4.2 PA-1 — The cross-reference resolver comes first

Renumbering a book by hand and hoping you caught every "see Chapter II.4" is how
a book ships with dangling references. There are 26 `Chapter X.Y` citations across
the PHB and MM. So: **write the resolver before the renumber.**

`test_cross_references_resolve` walks every `Chapter <num>` mention in
`player_handbook/` and `mm_manual/`, maps the number to a file, and fails on any
that does not exist. Today it passes (all refs resolve). The instant PA-2 creates
II.4a and moves the Body tree, any reference that should have been updated and
wasn't will point at a section that no longer says what it claims — so PA-2's
acceptance criterion is that the resolver *still* passes, plus a stronger check:
every reference to the Body tree resolves to II.4a specifically.

This is TDD applied to prose. It is the only reason PA-2 is a safe, mechanical
task instead of a careful, error-prone one.

### 4.3 PA-3 — Skill-text dedup (D5, revised per §2.1)

Four copies. Two canonical homes, one binding test.

- **Data home: `facet.yaml`'s `description`.** Per `CLAUDE.md`, `facet.yaml` is
  the machine-readable encoding of every mechanic. It already holds a full
  description per skill. It stays as-is.
- **Prose home: II.6's "The Skill List".** The long-form descriptions, all 15,
  Body/Mind/Soul, in one consistent format. Today the Body entries are full prose
  and the Mind/Soul entries are dash-lines — normalize all 15 to the Body format.
- **II.6's "Complete Skill Reference" table stays.** It is a legitimate quick ref
  (scan-and-find), not a duplicate — but it is now explicitly a *compression* of
  the prose list, subject to the project's quick-ref law.
- **The Facet chapters (II.4a / II.4b / II.4c) drop their descriptions.** Each
  keeps a bare table — skill name, governing attribute, and nothing else — under
  a one-line pointer: *"Full descriptions are in Chapter II.6 — Skills."* This is
  the pointer II.6 currently claims runs the other way; PA-3 reverses it and makes
  it true.
- **Delete II.6's false pointers** (II.6:69, II.6:85) and give the Body section
  the same treatment as Mind and Soul.

**INV-1 binds it:** a test asserts every skill's `description` in `facet.yaml`
matches its II.6 prose entry. Two copies survive because one is data and one is
prose; the test is what stops them from becoming two *different* rules. Four
uncoupled copies become two coupled ones.

### 4.4 PA-4 — Roll markers (D7, per §2.3)

Standardize on `→` for roll resolutions, everywhere, both books. Leave `>` to
mean "callout" exclusively.

Mechanical: in MM2 and MM4, vignette lines of the form `> <Character> rolls
**2d6 + …**` become `→ <Character> rolls **2d6 + …**`. Advice-box blockquotes are
untouched. The inner notation (`**2d6 + Knowledge (3 → +1) + Lore Practiced
(+1)**`) is already identical across both books — only the line marker moves.

### 4.5 PA-5 — Character sheet appendix (D3)

`player_handbook/Appendix_Character_Sheet.md`. II.1 has described a six-section
sheet since it was written; the sheet has never existed. Build exactly those six
sections (Attributes, Facet, Background, Skills, Techniques, Session Resources) —
this is transcription, not design. Do not invent a seventh, and do not add a field
II.1 does not name.

**INV-2 binds it:** every field on the sheet maps to a field on the engine's
`Character` model. A sheet that lets a player record something the engine cannot
store is a sheet that lies about the game. The test is also the guard against the
sheet drifting as the model grows.

### 4.6 PA-6 — Branch intros (D6) — **FABLE**

Nine branches; three (Clarity, Instinct, Archive) have a flavor intro, six do not.
Clarity's is the template:

> *Clarity Techniques represent the trained precision of a disciplined mind — the
> ability to take a situation apart, find the load-bearing piece, and know exactly
> what to do with it.*

One paragraph, ~2 sentences, names the attribute's character and what the branch
is *for*. Write six to match: Might, Grace, Iron (II.4a); Presence, Fortune,
Communion (II.4c). New canonical prose in an established voice — Fable, not Worker.

### 4.7 PA-7 — Front matter (D9) — **FABLE**

Three pieces, one new file (`player_handbook/Front_Matter.md`) plus one edit:

1. **Credits and license page.** GPLv3, the repo URL, attribution for the TTRPG
   Safety Toolkit (already credited in MM4) and any SRD-derived material. This
   part is mechanical and could be Worker-done; it is bundled here because it
   ships with the other two.
2. **"How to read this book."** Which chapters a player needs (II.*, III.1), which
   the MM needs (all + MM1–5), what is optional (Facet modules).
3. **The novice on-ramp.** The Introduction courts a reader who has never played
   a TTRPG and then does not tell them where to go. It must point, explicitly, at
   Quick Start. Whether it also needs a "what is a roleplaying game" passage is a
   voice call — Fable's.

### 4.8 PA-8 — III.2's fate (D10) — **BRAIN, then FABLE**

Escalated. See §7 Q1. Do not touch III.2 until it is ruled on.

### 4.9 PA-9 / PA-10 — Glossary, then generated index (D1, D2)

**Glossary** (`player_handbook/Glossary.md`) — 40–50 entries, every proper noun
the system defines. Each entry is: **term** — a one- or two-sentence definition —
*(Chapter X.Y)*. It is a quick reference and inherits the law: **it may only
compress canonical body text.** If a term turns out to have no canonical
definition anywhere in the books, that is a finding — report it, do not define it.

**INV-3 binds it:** every entry's chapter pointer resolves to a file that exists
and contains the term.

**Index** (`player_handbook/Index.md`) — **generated**, by
`software/tools/build_index.py`. For a digital-first book, a page-number index is
meaningless; the right artifact is a term → section map with links, which is also
exactly the "bidirectional cross-reference layer" the review asks for. The
generator reads the glossary's term list, walks both books, and emits, per term,
every chapter-and-heading where it appears.

The glossary is the generator's input, which is why it must land first.

**INV-4 binds it:** `Index.md` is up to date — regenerating it produces no diff.
Same pattern as a lockfile check. This is the invariant that makes an index
survivable in a ruleset that is still moving.

---

## 5. Test strategy

New module: `software/tests/test_docs_consistency.py`. Prose is not usually
testable, but *apparatus* is — every item in this design has an invariant that a
machine can check, and each one guards a specific way this work rots.

| | Invariant | Guards | Lands in |
|---|---|---|---|
| INV-1 | Every skill's `facet.yaml` `description` matches its II.6 prose entry | the dedup silently re-diverging | PA-3 |
| INV-2 | Every character-sheet field maps to a `Character` model field | a sheet that lies about the game | PA-5 |
| INV-3 | Every glossary term's chapter pointer resolves, and the target contains the term | a glossary pointing at nothing | PA-9 |
| INV-4 | `Index.md` is byte-identical to a fresh regeneration | a stale index confidently misdirecting | PA-10 |
| INV-5 | Every `Chapter X.Y` reference in either book resolves to an existing file | the renumber dangling a reference | PA-1 |
| INV-6 | MM5 contains no ASCII `--` or `-->` | the closed D8 fix regressing | PA-1 |

Per `CLAUDE.md`'s coverage rule, `build_index.py` is a new module and needs its
own tests beyond INV-4 — happy path, a term appearing in zero sections, a term
appearing in a heading vs. body.

**Baseline:** 965 passed, 1 failed (`test_config.py::test_default_port_is_8000`,
pre-existing, environment-caused — `docs/TODO.md` T4). Do not fix it here. Every
task below must leave that number at 965 + its own additions.

**Watch-out:** running the full suite regenerates
`playtest/02_silence_of_ashenmoor/digital_tool_log.md` (RNG churn). Revert it
before committing.

---

## 6. What this does not change

No rules text. No `facet.yaml` mechanics (only its header comments, in PA-2). No
engine behavior. If a task starts to look like it changes what happens at a table,
it has gone wrong — stop and escalate.

---

## 7. Open questions — escalated to Brain

### Q1 — III.2's fate (blocks PA-8)

III.2 *Adventuring* is 46 lines: Threat Clocks, recovery, and the death rules. It
is the only rules chapter with no In Play vignette, and next to III.3 (731 lines)
it will read as vestigial in a bound book. The review offers: fold it, or grow it.

**Planner's recommendation: grow it.** Folding is tempting on length alone, but
the two candidate homes are both wrong. Threat Clocks exist precisely *because*
hazards are not combat — moving them into III.3 undoes the chapter's own argument.
And the death rules ("Broken never kills you"; the player, never the MM, chooses
the scar or the heroic death) are among the strongest design statements in the
book. Folding them into a combat chapter buries them and implies death is a combat
outcome, which is the opposite of what they say.

Growing it means the two worked examples it lacks: a Threat Clock filling, and a
character taking the scar-or-heroic-death choice. That is a vignette in the
recurring cast's voice — Fable's, not a Worker's.

**Cost of the recommendation:** a vignette in the established voice, plus whatever
prose the growth needs. **Cost of folding:** cheaper now; loses the through-line;
hard to reverse once the death rules are inside III.3.

### Q2 — Is there a print milestone, and does it change the index?

The review says to schedule §D "against the print/PDF milestone." This design
assumes **digital-first** and builds a linked term index accordingly (§4.9). If a
physical print run is actually planned, the index needs page numbers, which means
it cannot be generated from markdown at all and has to come out of the layout
tool — a completely different task. **If print is real, PA-10 as specified is the
wrong artifact.** Confirm before PA-10 starts. Everything upstream of it is
unaffected either way.

---

## 8. Handoff

Wave 0 and Wave 1 (PA-1, PA-2) are unblocked and Worker-ready now. Wave 2's
mechanical tasks (PA-3, PA-4, PA-5) unblock the moment PA-2 lands. PA-6, PA-7, and
PA-8 are Fable's and are marked as such in the TASKS file — a Worker picking up
this file must skip them. Wave 3 is blocked on all of Wave 2, and PA-10 is
additionally blocked on Q2.
