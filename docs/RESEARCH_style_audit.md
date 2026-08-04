# Style Audit — Facets of Origin vs. `style/STYLE_GUIDE.md`

**Date:** 2026-08-01
**Auditor:** Claude (Opus 5), read-only pass — no source files modified
**Guide audited against:** `style/STYLE_GUIDE.md` + all six `style/analysis/*.md` files
**Corpus audited:** `player_handbook/` (21 files, 4,340 lines), `mm_manual/` (5 files, 2,222 lines),
`adventures/oraga_night/` (10 files, 2,556 lines), `enemies/*.fof` (5), `adventures/oraga_night/enemies/*.fof` (7)

---

## Verdict

The corpus is **strong on prose discipline and weak on apparatus**. The things the guide
says are hardest — confident unhedged voice, no summary codas, no throat-clearing, no
moralizing, a real recurring cast, failure branches that continue the story — are largely
already right. Hedging words appear four times in 6,500 lines of rules and advice. That is
professional-grade.

What is missing is almost entirely *structural*: the repeatable, self-documenting scaffolding
that the guide identifies as the actual "professionally published" signal. Law 1 of the guide
says template consistency, more than prose quality, is what reads as published. That is
precisely the axis where the corpus is thinnest.

**Scorecard against the ten laws:**

| # | Law | Grade | Note |
|---|---|---|---|
| 1 | Invariant templates, self-documented | **Fail** | One format legend exists (Backgrounds); Techniques, Skills, enemies, domains have none, and Techniques drift mid-catalog |
| 2 | Teach twice; legislate once | **Partial** | Teaching pass is good; the legislative pass often never arrives as labeled fields. One duplication bug (skill descriptions) |
| 3 | Quarantined voice registers | **Partial** | Registers are mostly clean; two fourth-wall breaches inside mechanics; designer voice sits in body text |
| 4 | Confidence; hedge only in-world | **Pass** | Four hedges corpus-wide. Best-performing law |
| 5 | Semantic typography | **Partial** | Field labels are italic in Background instances, bold in the legend; ~100 capitalizations of undefined terms |
| 6 | Numbered tables, typed sidebars | **Fail** | ~50 tables, **zero** numbered; ~40 sidebars, **zero** declared species |
| 7 | Everything exits into play | **Pass (PHB/MM)** / **Partial (Oraga)** | Oraga prints 4 Spark awards in 2,556 lines |
| 8 | Failure continues the story | **Pass** | Graceful Fail, ⟨If History Breaks⟩ sidebars, no fail-and-stop states found |
| 9 | Organize by moment of use | **Partial** | Book-level order is right; enemy stat blocks are not grouped by table-moment |
| 10 | Page space is an editorial signal | **Partial** | No worked artifact ships with any advice chapter |

**32 findings**, graded: **11 High** (systemic, cheap to fix, high signal), **14 Medium**,
**7 Low**.

> **Status (2026-08-02): remediated.** All six waves of the plan below have been
> executed, plus a seventh — the Bestiary, commissioned as a third core book,
> which closed E1, P6, and M2. Execution detail, deviations, and the open rules questions the work
> surfaced are in `docs/LOG_style_audit.md`. Seven new invariants (INV-9 through
> INV-15) in `software/tests/test_docs_consistency.py` and `test_enemy.py` now
> enforce the mechanical findings; full suite 1297 passing.
>
> **One finding was overstated and is corrected here: S8.** The count of ~100
> mid-sentence capitalizations of undefined terms included Title Case headings and
> bold field labels, where Title Case is correct (`rulebooks.md` §2). After
> excluding those, the corpus had **zero** genuine prose offenders. The invariant
> was added anyway; the defect was not real.

---

## What is already right (do not "fix" these)

Worth recording so remediation doesn't regress them:

- **`II.5` Backgrounds is the model.** Lines 19–60 are a real format legend (Title /
  Description / Starting Skill / Secondary Skill / Specialty), and all 15 instances obey it
  in the same order. This is the exact shape Law 1 asks for. Every other catalog should be
  rebuilt to match this file.
- **Glossary and Index have distinct, declared jobs.** `Index.md:5` carries the scope note
  the guide calls for ("sections that define or rule on it — not every passing mention"),
  and the index is machine-generated from the glossary term list with a no-diff invariant.
  This is better than the source books' practice.
- **Character sheet is physically last.** Matches `rulebooks.md §1`.
- **Hedging is near-zero.** `perhaps` ×3, `somewhat` ×1 across the PHB and MM Manual. No
  "you might consider", no "as appropriate", no "generally speaking".
- **No summary codas, no recap paragraphs, no "in conclusion".** Zero hits.
- **One throat-clearing opener only** (`III.2_Adventuring.md:3`), and it is a promise
  paragraph, which the guide sanctions at chapter level.
- **Oraga Night's MM-facing candor.** `01_Overture.md:62–73` ("Where the module says *the
  module does not say*, that is a load-bearing sentence, not a gap") is exactly the
  high-trust designer register `adventures.md §6` describes. The ⟨If History Breaks⟩ device
  is a textbook paired-conditional branch grammar (Law 8).
- **`tavva.fof` notes** carry a morale line, a negotiation surface, and an explicit
  "this fight is winnable, give the table the win" designer instruction — the substance
  `monster_books.md §5` demands, even though the container is wrong (see E2).

---

## HIGH severity — systemic, cheap, highest signal

### S1. Zero numbered tables in the entire corpus
**Guide:** Law 6; `rulebooks.md §5, §8.6`; `gm_books.md §8.8`; `visual_layout.md §3`.
Every real table gets a designation and title (`Table III.3–2: Reaction Costs`), is cited by
full designation, and appears in a register.

**Actual:** ~50 markdown tables across 21 files. **None** has a designation, a title line, or
a caption. Body text cites them positionally or not at all. `Table_of_Contents.md` has no
List of Tables. Grep for `Table [A-Z0-9]` across the whole corpus returns exactly one hit,
and it is the words "Table of Contents".

Heaviest concentrations: `MM5_Quick_Reference.md` (97 table lines), `III.3_Combat.md` (89),
`Appendix_Character_Sheet.md` (74), `09_Handouts.md` (52), `MM1_Encounters_and_Enemies.md` (50).

**Fix:** Add a caption line above every table — `**Table III.3–2: Reaction Costs**` —
numbered chapter-locally with an en dash. Convert every in-text reference to the full
designation. Add a "List of Tables" register to `Table_of_Contents.md`. This is the single
highest-ratio fix in the audit: mechanical, verifiable by a test, and it lights up Law 6,
`gm_books §8.8`, and the cross-reference laws simultaneously.

---

### S2. Sidebars have no declared taxonomy and three competing label syntaxes
**Guide:** Law 6; `rulebooks.md §5`; `gm_books.md §5, §8.2` ("never introduce an undeclared
box species later"); `setting_books.md §7` (five types, flavor and rules never share a box).

**Actual:** ~40 blockquote boxes across 13 files, using at least three incompatible
conventions and no declared species:

- `> **Sidebar: The Same Intent at Three Scopes**` (colon form, `II.3`)
- `> **Sidebar — Steel at the ball:**` (em-dash form, `04_The_Ball.md:44`)
- `> **Why they don't stack:**` / `> **The golden rule:**` / `> **Practical test:**` /
  `> **TR minimums by tier:**` — bare bold labels, no species marker at all

`Front_Matter.md §How to Read This Book` declares reading order but no box taxonomy.

**Fix:** Declare 5 species in `Front_Matter.md` — *Through the Mirror* (designer), *Variant*
(optional rule), *Example* (worked play), *In-World* (flavor), *MM Technique* — then retag
every existing box to exactly one. Any box currently mixing a rule and a flavor beat gets split.

---

### S3. Zero "Through the Mirror" designer boxes exist
**Guide:** This is an explicit **FoO-specific commitment** in `STYLE_GUIDE.md` ("roughly one
per major system"), derived from `gm_books.md §5` — named the single most distinctive
GM-book device.

**Actual:** Grep for "Through the Mirror" / "Behind the Curtain" / "Designer" across
`player_handbook/`, `mm_manual/`, `adventures/` returns **zero hits**.

The rationale exists in the repo — it is scattered through `docs/DECISIONS.md`,
`research/`, and commit messages — but none of it has been surfaced to readers.

**Fix:** Write six boxes, one per major system, in first-person-plural designer voice, each
stating balance intent and what breaks if house-ruled away:
1. Why NPCs never roll (`III.3`) — the guide even drafts this one for you, `gm_books.md §5`
2. Why enemies have Resolve and PCs have Conditions (`III.3`)
3. Why Tier 1 Conditions clear at end of exchange (`III.3`)
4. Why armor is a per-scene downgrade budget, not damage reduction (`IV.1`)
5. Why pre-Technique magic is scope-limited rather than difficulty-penalized (`II.3`)
6. Why quick references may never introduce a rule (`MM5` or `Front_Matter`)

---

### S4. No format legend before any catalog except Backgrounds
**Guide:** Law 1; `rulebooks.md §8.3`; `monster_books.md §8.15`; `adventures.md §9.4`.
"Before the first catalog of Techniques/Backgrounds/skills, include a 'how to read these
entries' section defining every field, its order, and the meaning of its absence."

**Actual:** `II.5_Character_Creation_Backgrounds.md:19–60` is a proper legend. Nothing else
has one:
- Technique trees (`II.4a`, `II.4b`, `II.4c`) — no legend, and no fixed fields to legend (see P1)
- Skill entries (`II.6`) — no legend
- Magic domains (`Appendix_Magic_Domains.md`) — no legend
- Enemy `.fof` files — no legend anywhere in `MM1`
- Oraga Night keyed areas — no legend in `01_Overture.md`

**Fix:** One legend per catalog, written *before* the fields are finalized, per the guide's
workflow step 2.

---

### P1. Technique entries have no field skeleton, and drift mid-catalog
**Guide:** Law 1 ("the 100th entry has exactly the shape of the 1st"); `rulebooks.md §4`
(spell/power entry: invariant-order stat line); `rulebooks.md §9` ("no mid-catalog format
drift"). The guide's own FoO mapping: *Name → Facet/Tier → Cost → Roll → Scope → body*.

**Actual:** Techniques are `**Name** *(Attribute)*` followed by free prose, with no labeled
fields at all. And the attribute tag is applied inconsistently within a single file:

- `II.4a:37` **Forcing Hand** *(Strength)* — tagged
- `II.4a:41` **Weapon Mastery** *(Strength)* — tagged
- `II.4a:48` **Overwhelming Force** — untagged
- `II.4a:53` **Lift the World** — untagged
- `II.4a:60` **Unstoppable** — untagged

Tier 1 entries carry the tag; Tier 2 and Tier 3 do not. That is textbook mid-catalog drift,
in the first catalog a reader meets.

Frequency of use ("Once per scene", "Once per session"), activation cost, and roll are all
buried in prose where a reader has to parse a sentence to find them mid-session.

**Fix:** Fixed field order for every Technique, legend published first:
`**Name**` → `*(Facet, Tier N)*` → `**Attribute:**` → `**Use:**` (once per scene/session/at will)
→ `**Roll:**` → body prose → `**Normal:**`.

---

### P2. No `**Normal:**` field on any Technique
**Guide:** Called out twice — `rulebooks.md §4` ("a masterstroke worth stealing for FoO
Techniques") and again in `STYLE_GUIDE.md` FoO commitments ("anything that breaks a default
rule restates the baseline it breaks").

**Actual:** Zero occurrences of `**Normal:**` corpus-wide.

Several Techniques plainly break defaults and don't say what they break. `II.4a:41`
*Weapon Mastery* — "treated as one difficulty step easier" — never restates that the default
is Standard and that the MM's own adjustment is capped at one step, so a reader cannot tell
whether Weapon Mastery stacks with a Defensive posture's shift. `II.4a:65` *The Final Blow*
removes a target "regardless of any remaining resources" — the baseline it overrides (Resolve
depletion, riders never defeat) is not restated.

**Fix:** Add `**Normal:**` to every Technique that alters difficulty, action economy,
Resolve, Conditions, or scope. This will also surface stacking ambiguities that currently
have no written answer.

---

### P3. Skill entries have no field skeleton
**Guide:** `rulebooks.md §4` gives the FoO analog explicitly: *Skill name (Facet) →
what it covers → **Roll:** → **Time:** → **Retry:** → **Sparks:** → **Untrained:***.

**Actual:** `II.6:47+` entries are `**Athletics** *(Strength)*` + one prose paragraph.
No Roll, no Time, no Retry policy, no Untrained behaviour. Retry policy is the notable gap —
`III.1:210` states a retry rule for one worked case (the lock) in an italic aside, but no
skill entry carries it, so "can I try again?" has no lookup home.

---

### P4. Skill descriptions are duplicated in two places
**Guide:** Law 2 ("a rule is *defined* in exactly one home location"); `rulebooks.md §9`
("no repeated re-explanation… the classic amateur divergence bug").

**Actual:** `II.6:15–30` "Complete Skill Reference" table carries a Description column for
all 15 skills. `II.6:47+` "The Skill List" then repeats the same descriptions as prose. Two
copies of the same text, already drifting — the table says Finesse covers "picking locks,
sleight of hand, ranged weapons, acrobatics, disabling mechanisms"; the prose section is a
separate wording of the same list.

This is already logged as open in `docs/RESEARCH_editorial_review.md` ("skill-text dedup").
The style guide raises it from a nit to an iron-law violation.

**Fix:** Table becomes a lookup index (Skill / Facet / Attribute only, no Description
column); prose section is the single definition home.

---

### S5. No chapter opens with a hook; most open with a throat-clearing A-head
**Guide:** `rulebooks.md §8.1` ("Open every chapter with a hook, not a rule — 1–3 paragraphs
of second-person scene or a 'this chapter gives you…' promise; the first A-head comes
after"); `gm_books.md §8.1` (half-page framing essay decomposing the chapter into 3–6 named
sub-skills). Anti-pattern list: "section openers that throat-clear".

**Actual:** 0 of 18 PHB chapters and 1 of 5 MM chapters do this. Every chapter's first
element is an A-head, and the A-head is usually a filler word:

| File | First A-head |
|---|---|
| `II.2` | `## Introduction` |
| `II.6` | `## Overview` |
| `IV.1` | `## Philosophy` |
| `MM1` | `## Overview` |
| `MM2` | `## Overview` |
| `MM3` | `## Overview` |
| `MM5` | *(none — straight to `## Core Resolution`)* |

`MM4_Running_the_Table.md:3` (`## The Mirror Master Philosophy`, opening "You are not the
author of the story…") is the one file that does it right and should be the template.

**Fix:** 1–3 paragraphs before the first A-head in every chapter; delete every
`## Overview` / `## Introduction` A-head and fold its content into the hook.

---

### S6. Cross-reference idiom is inconsistent and often unresolvable
**Guide:** Law 2 and `rulebooks.md §8.11` — `(see Postures, III.3)`, section name + number,
every time. `gm_books.md §9`: "no unnumbered, unanchored references ('as mentioned above')".

**Actual:** 17 distinct pointer forms. Only 3 carry a chapter number:

- Resolvable: `(see II.3, *Acquiring a Domain*)`, `(see Combat, Chapter III.3)`, `(see Chapter III.1)`
- Unresolvable: `(see below)` ×2, `(see the next section)`, `(see the example below)`,
  `(see Armor)`, `(see *Strike*, above)`, `(see *Armor bonus*, above)`,
  `(see *Facing Mooks and Named Antagonists*)`, `(see *Magic and Backgrounds*)`

Plus four bare `see below` outside parentheses (`MM1:11`, `III.1:31`, `II.4:75`,
`03_Masks_and_Agendas.md:20`). In a digital-first book with anchors, a bare "below" is
strictly worse than a page number — it has no target at all.

**Fix:** Standardize on `(see <Section Name>, <Chapter>)`. Add a docs-consistency test that
fails on `see below` / `see above` / `as mentioned` / `see the next section`.

---

### S7. Rules bodies delivered as bullet lists
**Guide:** `rulebooks.md §9` ("No bullet-point rules bodies. Bullets appear only for genuine
checklists. Rules are prose paragraphs under labels"); `gm_books.md §8.4` (boldface run-in
lists for advice; numbered lists only for true sequences).

**Actual:** bullet-to-run-in-label ratios, worst first:

| File | Bullets | Run-in labels | Verdict |
|---|---|---|---|
| `Appendix_Magic_Domains.md` | 63 | 0 | Catalog with no field structure at all |
| `MM2_Session_Design.md` | 129 | 37 | Advice as bullet dump |
| `MM4_Running_the_Table.md` | 61 | 28 | |
| `MM5_Quick_Reference.md` | 57 | 6 | Defensible — it's a scan card |
| `III.1_Core_Resolution.md` | 21 | 4 | Core mechanic chapter, rules as bullets |
| `II.1_Character_Creation_Overview.md` | 16 | 0 | |
| `IV.1_Equipment.md` | 11 | 0 | |

`III.1:69–72` is the clearest case: the four Spark-earning triggers — a genuine rule with
mechanical consequences — are four bullets. Under the guide these are four run-in bold
labels in prose paragraphs. `III.1:90–97` (saving throw categories and outcome tiers) is the
same shape.

Counter-example done right: `III.3_Combat.md` (95 run-in labels, 14 bullets) and
`Quick_Start.md` (31/0). Combat is the best-formatted chapter in the book.

---

### O1. Oraga Night has zero read-aloud text
**Guide:** `adventures.md §3` and §9.6 — the most heavily specified convention in that file.
Also `visual_layout.md §7`, `STYLE_GUIDE.md` Law 3 (read-aloud is a quarantined register).

**Actual:** Grep for read-aloud markers across all 10 module files: **zero hits**. No area,
event, or NPC entrance carries a boxed or italic perception-only block. Every first-contact
description is GM-facing prose the MM must improvise from cold.

For a module whose entire premise is atmosphere — a masquerade that curdles at midnight —
this is the highest-value gap in the corpus. `01_Overture.md:37` even instructs the MM to
"change your voice. Shorter sentences. Fewer adjectives." at the Unmasking, without supplying
a single sentence to say.

**Fix:** One triggered read-aloud block per keyed area and per scheduled event: explicit
trigger clause in GM voice, then 2–6 sentences, second person present tense, perception verbs
only, no mechanics, no creature identification, exits omitted. Sensory formula from
`adventures.md §3`: dominant visual + one secondary sense + one wrongness cue. The Movement
omens are already written as wrongness cues — they are read-aloud blocks waiting to be
formatted.

---

### E1. There is no bestiary document — enemies exist only as YAML
**Guide:** all of `monster_books.md`, especially §8 (15-point checklist) and the
`STYLE_GUIDE.md` FoO commitment ("Enemy entries ship the ladder").

**Actual:** 12 `.fof` files, no prose entries anywhere. Consequently missing, corpus-wide:
- read-aloud opener (§8.1) — 0
- Tactics as a first-class field with disposition / first-target priority / morale (§8.7) —
  present only as freeform `notes:` prose in some files
- Organization line (§8.10) — 0
- labeled sample encounters (§8.10) — 0
- Lore tier sidebar keyed to 6−/7–9/10+ (§8.11) — 0
- tier ladder per family, Mook → Named → Boss sharing one lore section (§8.9) — 0
- TR-sorted and tier-sorted finding aids before the entries (§8.15) — 0

`MM1_Encounters_and_Enemies.md` covers *how to build* an enemy (TR formula, budget) but
never documents the entry format or ships a catalog.

**Fix:** This is the largest net-new writing item in the audit. Scope it as an `MM6 Bestiary`
chapter: a "how to read these entries" legend, TR-sorted and tier-sorted tables up front,
then family entries at the checklist's page budget (Mook ⅓ page, Named ~1 page, Boss 2 pages).
The `.fof` files stay as the machine-readable layer the chapter points into — the guide's
"digital-first citations" commitment says `facet.yaml` and the software play the role print
books give a statistics appendix.

---

## MEDIUM severity

### S8. Capitalization drift on undefined terms
**Guide:** Law 5 — "capitalize only formally defined terms; 'roll', 'check', 'scene' stay
lowercase."

**Actual:** mid-sentence capitalizations of terms **not** in `Glossary.md`:
`Skill`/`Skills` ×66, `Scene` ×11, `Roll`/`Rolls` ×12, `Action`/`Actions` ×11.
(`Facet`, `Domain`, `Spark`, `Resolve`, `Background`, `Strike`, `Endurance`, `Condition`,
`Technique`, `Attribute`, `Posture`, `Reaction`, `Difficulty`, `Exchange` are all glossary-
defined and correctly capped — the discipline is 90% there.)

**Fix:** Lowercase the four offenders, or add them to the glossary if they are genuinely
defined terms. Add a docs-consistency test: any capitalized term not in `Glossary.md` fails.

### S9. Semantic typography inverted in Background instances
**Guide:** Law 5 — bold = field labels; italics = named game objects and narration.

**Actual:** The legend uses bold field labels (`**Description**`, `II.5:25`) but all 15
instances use italic labels (`*Description:*`, `II.5:121`). Same fields, opposite typography,
in the same file. Italics are simultaneously being used for their correct purpose (Technique
and domain names) elsewhere, so the signal is genuinely ambiguous.

**Fix:** Bold in both places.

### S10. Example-of-play coverage has holes at the worst points
**Guide:** FoO commitment — "the recurring cast carries the examples… book-wide"; `rulebooks.md
§8.7` ("at least once per subsystem"); §8.13 (every example includes a failed roll with
consequences and one visible MM ruling explained aloud).

**Actual:** 8 files carry cast vignettes (`III.3` leads with 74 speaker tags). Missing entirely:

| File | Why it matters |
|---|---|
| `III.1_Core_Resolution.md` | **The core mechanic chapter.** No worked arithmetic with the cast anywhere |
| `II.4a` / `II.4b` Facet chapters | Technique trees with no worked use |
| `IV.1_Equipment.md` | No example of armor's downgrade budget in play |
| `II.1_Character_Creation_Overview.md` | The walkthrough chapter |
| `MM1_Encounters_and_Enemies.md` | TR arithmetic never worked through with a named party |

`III.1` is the serious one — Law 2 says teach twice, and the chapter that owns 2d6, Sparks,
difficulty, and the three outcome tiers currently only legislates.

### P5. No difficulty benchmark table
**Guide:** `rulebooks.md §5, §8.8`; `gm_books.md §5` (the four-column device: number,
concrete fictional task, the check, *who could plausibly pull it off*); named again in
`STYLE_GUIDE.md` FoO commitments.

**Actual:** `III.1:50–55` gives Easy/Standard/Hard/Very Hard against abstract conditions
("Clear advantage, weak opposition, favorable conditions"). No concrete task, no
"who succeeds most of the time" column. An MM setting difficulty at the table gets a
definition, not a calibration.

**Fix:** Add a benchmark table pairing each tier with a one-line vivid task and the rank that
succeeds most of the time (Novice / Practiced / Expert / Master-with-a-Spark).

### P6. No tiered lore boxes
**Guide:** FoO commitment — "Tiered lore boxes ('what you notice / learn / uncover') keyed to
6− / 7–9 / 10+"; `visual_layout.md §4`; `monster_books.md §8.11`.

**Actual:** Zero. The device is native to a 2d6 three-tier system and currently unused
anywhere — PHB, MM Manual, or Oraga Night, where the Undercurrents are begging for it.

### P7. Fourth-wall breaches inside mechanics
**Guide:** Law 3; `rulebooks.md §9` ("the book never mocks its own genre"); anti-tells list
("fourth-wall snark inside mechanics").

**Actual, two instances:**
- `IV.1_Equipment.md:64` — "Rope (50 feet is the standard TTRPG unit of rope, and we see no
  reason to change this)" — a joke about the hobby, inside an equipment list.
- `III.3_Combat.md:5` — the chapter opens by comparing FoO to other games: "Most TTRPG
  combat systems hand you a turn. You wait. You act. You wait again. The monster acts."

`I_Introduction.md:13` makes a similar comparison, but that is the introduction and the guide
sanctions positioning there. `III.3` is a rules chapter.

**Fix:** Rewrite `III.3`'s opener as an in-world scene (the guide's canonical example for a
combat chapter is clashing steel). Cut the rope aside or move it to a flavor box.

### P8. `IV.1` opens in designer register as body text
**Guide:** Law 3 (designer notes are boxed and labeled); `setting_books.md §7` (statblock and
meta quarantine).

**Actual:** `IV.1_Equipment.md:3` — `## Philosophy`, "Equipment in Facets of Origin is
narrative, not numerical… The system cares about what your equipment *means* for the fiction,
not how many decimal points it contributes to your roll." That is Through-the-Mirror content
sitting in the body as the chapter's first A-head.

### P9. `IV.1` has no prose entry layer
**Guide:** `rulebooks.md §4` (equipment: master table per category, then an alphabetical prose
section where only items needing explanation get a run-in bold entry, one to three sentences,
flavor clause + rules clause) and §8.16.

**Actual:** Three master tables and bulleted gear lists. No item anywhere gets a prose entry,
so no item has an evocative identity or a special rule with a home. The chapter is 92 lines
for the entire equipment compendium.

### M1. MM chapters do not decompose into named sub-skills
**Guide:** `gm_books.md §8.1` — open with a framing essay naming the chapter's job and
decomposing it into 3–6 named sub-skills, "then follows that structure exactly"; §3a (role
decomposition — "naming the sub-roles makes an unteachable job teachable").

**Actual:** MM1/MM2/MM3 open on `## Overview` prose that states the topic without naming its
parts. MM4 does it correctly.

### M2. No worked artifact ships with any advice chapter
**Guide:** Law 10; `gm_books.md §1` ("don't just teach the template, ship one finished
instance of it") and §8.11 — one complete worked artifact per advice chapter at full
production quality.

**Actual:** None. MM1 teaches TR and encounter budgets but never prints a finished encounter.
MM2 teaches session structure but never prints a finished session plan. MM3 teaches campaign
design but never prints a campaign frame. Oraga Night is arguably the corpus's one worked
artifact, but it lives in another directory and no MM chapter points at it as an exemplar.

### M3. No time-budgeted prep checklists
**Guide:** `gm_books.md §3f, §8.13` — "Meeting the reader at their real constraint rather than
the ideal one is the single most 'professional' gesture in either book." Cumulative,
worst-case first.

**Actual:** Zero. MM2 covers session design with no "30 minutes / 1 hour / 2 hours" ladder.

### M4. No 2d6-weighted random tables with footnote expansions
**Guide:** `gm_books.md §8.9` — scene menus, commonest result at 7, every entry an active want
or unfolding situation, non-obvious entries expanded in footnotes below the table, social
resolutions worth full rewards stated in the expansion. Named again in `STYLE_GUIDE.md` FoO
commitments.

**Actual:** The rumor table in `09_Handouts.md` is the only random table in the corpus, and it
carries no footnote expansions. No 2d6-weighted table exists anywhere.

### E2. `.fof` enemy files drift in field presence and bury tactics in freeform notes
**Guide:** Law 1; `monster_books.md §8.2` ("one stat block format, identical field order,
everywhere"), §8.4 (group fields by table-moment), §8.7 (mandatory Tactics section).

**Actual, comparing `enemies/city_watch_sergeant.fof` and
`adventures/oraga_night/enemies/tavva.fof`:**
- `phases: []` present in tavva, absent in city_watch_sergeant
- `special: null` vs. a prose paragraph — no legend states what absence means
- Tactics live in a freeform `notes:` blob with ad-hoc pseudo-labels that differ per file:
  `Posture tendency:` in one; `CONDUCT:` / `ENTIRELY WINNABLE:` / `CAUGHT AND HELD:` in the
  other. Two files, two invented labelling schemes, in a five-file corpus.
- Fields are ordered by data taxonomy, not by table-moment. `monster_books.md §3` is emphatic
  that this was the 2003→2007 revision's whole point.

**Fix:** Add typed schema fields — `tactics:` (with `disposition`, `first_target`, `triggers`,
`morale`), `organization:`, `negotiation:` for Bosses — so behaviour stops living in an
untyped notes blob. Then order the schema encounter-start → when-PCs-Strike → when-it-acts →
bookkeeping. This is a `facet.yaml` / schema change and belongs in the software sync cycle.

### O2. Oraga Night's intro battery is incomplete and out of order
**Guide:** `adventures.md §1, §9.1–9.4` — the fixed front-matter sequence.

**Actual:**

| Required element | Status |
|---|---|
| Party size, starting/ending Facet level, play length, *first* | In `README.md:6–10`, not in `01_Overture.md`. Facet level is never stated anywhere |
| One-page italic fiction prologue | Absent |
| Adventure Background (villain's story to now) | In ch. 02, not the intro |
| Synopsis, one paragraph per part, each ending with the world-state | Absent |
| 3–5 named bold hooks, all converging, each ending "begin with scene X" | Absent — `03_Masks_and_Agendas.md` has eight *player agendas*, which is a different device |
| Running-the-adventure advice | Present and strong (`01_Overture.md`) |
| Format legend (field labels, italic = read-aloud, sidebar types, TR notation) | Absent — ⟨If History Breaks⟩ is used before it is ever defined |

**Fix:** Restructure `01_Overture.md` to the seven-part battery, moving the README's stat line
into it and adding the missing synopsis, hooks, and legend.

### O3. Keyed areas lack the fixed field battery
**Guide:** `adventures.md §2, §9.5` — header facts → read-aloud → explanation → creatures →
tactics → treasure → development, in that order, with bold labels; even empty areas get a
line plus their return-visit change.

**Actual:** `04_The_Ball.md:37+` areas are `**B1. Name.**` + prose + an italic parenthetical
`*(Agenda relevance: …)*`. The parenthetical is doing the job of Development, informally and
inconsistently — B2 gets `*(Nearly every scheduled event happens here.)*`, B4 gets a
mixed agenda/geography/MM-instruction blob. No area has `Light:` / `Creatures:` header
fields, a Tactics label, a Treasure label with provenance and a find difficulty, or a stated
change after the party acts.

The content is often present in prose; it is the invariant shape that is missing.

### O4. Spark awards for clever and peaceful resolution are essentially unprinted
**Guide:** Law 8 ("the award is printed, not left to MM generosity"); `adventures.md §6, §9.8,
§10` ("no unpaid clever play" — the amateur tell these modules never commit).

**Actual:** the string "Spark" appears **4 times in 2,556 lines** of module text. For a module
built around social maneuvering, agendas, trespass, and a midnight rescue — where nearly every
win is non-combat — the reward layer is nearly absent. Morale/flee/surrender language appears
7 times total, which also under-serves `adventures.md §9.7` (every Tactics entry needs a
morale line).

---

## LOW severity

### O5. Area-code ordering drift
`04_The_Ball.md`: B1 (37) → B2 (57) → B3 (62) → **B11 (67)** → B4 (76) → B5 (81) → B6 (97) →
B7 (103) → B8 (117) → B9 (147) → B10 (152). B11 sits between B3 and B4. Codes are the shared
identifier between text, map, and contents (`adventures.md §8`), so out-of-sequence numbering
breaks the one thing the code exists to do. Either renumber, or state in the legend that
public rooms are grouped ahead of private rooms regardless of number.

### O6. No maps, no scale line, no terrain-as-rules lines, no starting-position key
`adventures.md §8, §9.12`. The module tells the MM to "know this geography cold — Court →
terraces → lower garden → river gate" (`04:79`) instead of shipping a map. The guide's FoO
translation asks for terrain expressed as reaction/posture modifiers or difficulty shifts
rather than movement squares, which suits this system and is cheap to add.

### O7. No one-page scene cards for combat
`adventures.md §5 (Stage 3), §9.12`. The guide explicitly notes FoO's light stat blocks make
this format *cheap*. Currently combat material is dispersed through narrative chapters with
pointers to `enemies/` as a filesystem path.

### O8. Cross-references by filesystem path
`04_The_Ball.md:60` — "(guard stat blocks are in `enemies/`)". Digital-first citation policy
(`STYLE_GUIDE.md`, FoO commitments) asks for anchors, not paths.

### P10. `Appendix_Magic_Domains.md` is a catalog with no entry format
63 bullets, 0 run-in labels, no legend (already counted in S4/S7 but worth naming separately —
it is the corpus's largest unstructured catalog at 316 lines).

### M5. `MM5_Quick_Reference.md` has no chapter opener or usage statement
`gm_books.md §1` — GM books declare their own architecture. MM5 jumps straight to
`## Core Resolution` with no statement of what it is, when to reach for it, or the iron law
that it may never introduce a rule the body text doesn't state.

### M6. Table_of_Contents has no List of Tables and no List of Sidebars
`rulebooks.md §1`, `gm_books.md §1` — both are first-class finding aids in the source books.
Blocked on S1 and S2.

---

## Remediation plan

Sequenced so that each wave unblocks the next, and so that the mechanical wins land first.

**Wave 1 — mechanical, testable, no new prose (highest ratio).**
S1 (number every table + ToC register), S6 (cross-reference idiom), S8 (capitalization),
S9 (bold field labels in `II.5`), P4 (skill-description dedup), O5 (area-code order),
O8 (path citations). Every item here is verifiable by a `test_docs_consistency.py` rule,
which also prevents regression. Estimate: one focused pass.

**Wave 2 — declare the formats (unblocks everything downstream).**
S2 (sidebar taxonomy in `Front_Matter.md`), S4 (format legends for Techniques, Skills,
domains, enemies), P1 (Technique field skeleton), P3 (Skill field skeleton), P2 (`**Normal:**`
fields). Do the legends *before* filling instances, per the guide's workflow step 2.
Note: P2 will surface real rules ambiguities (Technique stacking with posture and MM
difficulty shifts) that currently have no written answer — expect this to generate rules work,
not just editorial work, and route those through the PHB↔`facet.yaml`↔engine sync.

**Wave 3 — the missing registers.**
S3 (six Through the Mirror boxes), S5 (chapter hooks; delete `## Overview` A-heads),
S10 (cast vignettes for `III.1`, `II.4a`, `II.4b`, `IV.1`, `II.1`, `MM1`), P5 (benchmark
table), P7/P8 (fourth-wall fixes, `IV.1` philosophy → box), S7 (de-bullet `III.1`, `MM2`,
`Appendix_Magic_Domains`).

**Wave 4 — MM Manual apparatus.**
M1 (sub-skill decomposition), M2 (one worked artifact per chapter), M3 (time-budgeted prep),
M4 (2d6-weighted scene-menu tables), M5, M6, P6 (tiered lore boxes).

**Wave 5 — Oraga Night.**
O2 (intro battery), O1 (read-aloud throughout — largest single writing item in the module),
O3 (keyed-area field battery), O4 (printed Spark awards + morale lines), O6, O7.

**Wave 6 — the bestiary.**
E1 (`MM6 Bestiary` chapter with legend, finding aids, and family entries shipping the tier
ladder), E2 (`.fof` schema: typed `tactics` / `organization` / `negotiation` fields, ordered
by table-moment). E2 touches the schema and belongs in a software sync cycle with tests.

**Not recommended:** `visual_layout.md`'s print-dress conventions (two-column justified type,
zebra striping, drop caps, edge tabs, art credits) are out of scope for markdown sources.
They belong to a future print/HTML rendering layer, and several — running headers,
breadcrumbs — are already the web app's job rather than the manuscript's.

---

## Method note

Findings were derived by reading `STYLE_GUIDE.md` and all six `analysis/` files in full, then
combining full reads of representative chapters (`I`, `II.4a`, `II.5`, `II.6`, `III.1`,
`IV.1`, `Front_Matter`, `Glossary`, `Index`, `Table_of_Contents`, `01_Overture`,
`04_The_Ball`, two `.fof` files) with mechanical pattern counts across the whole corpus
(table designations, hedge words, throat-clearing openers, cross-reference forms,
bullet-vs-run-in-label ratios, sidebar labels, capitalization of undefined terms, cast
speaker tags, read-aloud markers). Counts in this document are reproducible by grep; file:line
citations were verified individually. No source file was modified.
