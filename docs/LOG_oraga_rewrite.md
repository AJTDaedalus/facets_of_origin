# LOG — Oraga Night, Rebuilt

**Design:** `docs/DESIGN_oraga_rewrite.md` · **Tasks:** `docs/TASKS_oraga_rewrite.md`
**Depends on:** `LOG_lineage.md`, `LOG_valloh_facet.md`, `LOG_fun_second_act.md` — all complete
**Evidence:** `research/simulation_log.md` Series 13

---

## 2026-09-09 — O1 through O21

| Task | Status | Note |
|---|---|---|
| O1 Bought reskins | ✅ | Flavour fields only; **INV-18** now enforces it, and INV-18's sibling keeps setting names out of the Bestiary (B9). |
| O2 five pregens as `.fof` | ✅ | Built through the real model, so they cannot be invalid. Endurance 5/4/3/3/3; Dassa ungifted. 9 tests. |
| O3 generated pregen blocks | ✅ | `03`'s numbers are generated from the `.fof`; no-diff invariant. |
| O4 simulate S3 | ✅ | Captain **Resolve 6 → 5**, entering the clock's second segment. Hard band at every seed. |
| O5 simulate S2 | ✅ | 100% — the card was mislabelled. See below. |
| O6 Overture | ✅ | Six named hooks, the nudge paragraph, the format legend's card/enemy/clock notation, a signed designer's note, and the ending promise corrected to Facet level 1. |
| O7 prelude deleted | ✅ | Content survives as hooks, as facts in `02`, and as the mask-maker's aftermath scene. |
| O8 `02`/`03` trimmed | ✅ | The gazetteer moved to the Facet's `V3`; *Making Characters* rewritten to the seven steps; *How You Got In* now points at the Overture. |
| O9 B0 | ✅ | The approach and the line, with the first-roll MM Note. |
| O10 alert state | ✅ | Written once above the rooms. |
| O11 pointers + Q&A | ✅ | Card pointers both ways; Corval, Vorlain and Raunu's summons as Q&A blocks. |
| O12 night clock | ✅ | Table IX–2b, with the *what the players can move* column. |
| O13 the gate | ✅ | B12, the contract, the spoiler guardrails, the red-herring note. |
| O14 ⟨If History Breaks⟩ | ✅ | The Bought change sides; and the branch for a table that brings Veier to the front. |
| O15 advancement | ✅ | Four skill points and a reflection scene at the epilogue; Facet level 1 at the inquest; the gifted formalize there. |
| O16 scene cards | ✅ | `09_Scene_Cards.md`, five cards, generated stat lines. |
| O17 invariants | ✅ | **INV-19** cards regenerate to no diff; **INV-20** module chapter pointers resolve; **INV-21** read-aloud under 120 words; plus a TR-recomputes check. |
| O18 sidebars + abridged | ✅ | Four troubleshooting sidebars with two in-fiction answers each; the four-hour box. |
| O19 README | ✅ | Contents, and the "what you need" line pointing at the Facet. |
| O20 Revision 4 | ✅ | 18 numbered inventions for the owner's read. |
| O21 close-out | ✅ | Full suite **1731 passed**. |

### What the simulation actually said

**S3, the gate.** The Hard band is reachable and the captain's numbers are settled —
Resolve 5, entering on the clock's second segment, 42.5–53.0% across five seeds. But
**two of the brief's three acceptances were unreachable, and one of them was wrong**:

- *Median 3–4 exchanges* — it is **8**. The party's offense is +1/+1/+0 against an
  effective 11 Resolve plus four Mooks, and no legal tuning changes that. The scene is
  not meant to be fought to zero: it has a fire clock and three endings, one of which
  is "a party that only held has won". The card now prints the 8-exchange figure as
  the warning it is, rather than pretending the number is 4.
- *Phase in exchange 2 of the captain's presence, ≥70%* — **unreachable at any Resolve
  threshold.** Even at 6 of an effective 7, under 1% of runs saw it by exchange 3.
  **A Resolve-keyed phase cannot fire early in a long fight.** The Archive Guardian's
  fix (raise the threshold, T15) works only because that fight is three exchanges
  long. So the captain's phase is re-authored as a **conduct trigger** — his second
  exchange on the field, or the exchange after the party looks like winning — which
  is what the module's own fiction already said, and which cannot arrive too late.

  **Generalisable:** key a Boss's second act to *conduct* when the fight is long, and
  to *Resolve* only when it is short.

**S2, the knives.** 100% party win at every seed. The card claimed **Standard** and is
a **Skirmish** by the Recipe Table — one Named plus three Resolve-0 Mooks is nowhere
near Standard's 3 Named + 1 Mook. Rather than add a Named to hit the band, the card now
says so plainly: *Skirmish roster, Standard tension*, with the difficulty carried by
the shared noise clock that both sides lose. A card that claims a band it does not have
teaches the MM to distrust the bands.

**Party scaling is a cliff.** One extra Named actor takes a four-player party from 78%
to **8%**. The card's scaling line says add Blades and never a second Sergeant.

### New simulator capability

`EnemyState.enters_on_exchange`. The gate's Boss arrives mid-scene and the sim could
not say so — such an encounter could only be tuned by pretending everyone started
together, which is exactly wrong for a fight whose whole shape is *it gets worse*.
Default 1 is a no-op and every recorded corpus reproduces.

### A round-trip bug the pregens found

`to_fof`/`from_fof` did not carry `lineage`, `gifted` or `domain_source`. L8 added
the fields to the model and nothing to the serialization, so **a saved gifted
character reloaded as an ungifted human who happened to know a domain** — and the
formalization rule would then have applied the wrong route to them. Caught by the
pregen tests, fixed, and guarded three ways, including that a human sheet must not
grow a `lineage:` field so every `.fof` written before II.5 round-trips unchanged.

### Scope held

Untouched, as the standing rule required: the agendas, the omens, the undercurrents,
the cast's existing entries, the Fractures and the tell-table, the safety text, the
existing ⟨If History Breaks⟩ sidebars, the Crossing, and the epilogue question.

---

## O21 — the `style/analysis/adventures.md` §9 checklist, item by item

The acceptance list for the rewrite. Eighteen items, ticked honestly.

| # | Item | | Where / note |
|---|---|---|---|
| 1 | Page one states party size, starting level, ending level, play length | ✅ | Overture, *What This Adventure Is*: 3–5, Facet level 0, **Facet level 1 by the end of the aftermath**, 4–6 hours / 3 sessions |
| 2 | One-page italic fiction prologue, never referenced again | ✅ | **Added this pass.** The testament, the walk through the palace counting charge, the under-cook who was wrong about which part |
| 3 | Background → Synopsis (a paragraph per part ending with world-state) → 3–5 named converging hooks, each ending "begin with scene X" | ✅ | *The Story So Far* → *The Night in Seven Movements* (each ends in italic world-state) → **six** named hooks, each ending *"Begin at the Gatehouse Court, B1, Movement I."* |
| 4 | Format legend: field labels, italic = read-aloud, sidebar types, enemy notation | ✅ | *How This Module Is Written*, now carrying scene-card IDs, the tier·Resolve·attack·armor·TR notation, and the clock convention |
| 5 | Fixed field order per keyed area, bold labels, empty areas get a line | ✅ | Pre-existing and untouched; B0 and B12 written to it |
| 6 | Read-aloud 2–6 sentences, perception-only, second person, trigger clause, no creature names | ✅ | The three new blocks measure 60/68/76 words, 3–5 sentences. **INV-21** enforces the cap — and was rewritten this pass because it only saw single-line blocks (below) |
| 7 | Tactics: opening move, priority target, morale line, postures for Named/Boss | ✅ | Every scene card; generated from the `.fof` `triggers`/`first_target`/`morale` fields |
| 8 | Treasure has provenance and position; Development names Spark awards | ⚠️ **partial** | Sparks are printed on S1, S2 and S3. The module has almost no loot by design (the crystal charges are the exception and they are on the pregens' sheets), so "provenance and position" has little to attach to. Not judged a gap |
| 9 | A visible clock with indented conditional lines as the mission menu | ✅ | Table IX–2b, the night clock, with the *what the players can move* column |
| 10 | Alert-state paragraph once per site | ✅ | *The Palace on Alert*, above the keyed rooms |
| 11 | Paired branches; failure continues with a named cost; finale scores earlier missions | ✅ | S3's three endings are written as paired conditionals; the Fractures score the finale mechanically |
| 12 | One-page combat cards per chapter: ID, tier recipe, trigger read-aloud, tactics, stat lines, **map letter key**, terrain-as-rules, pointers both ways | ⚠️ **partial** | `09_Scene_Cards.md`, five cards, **generated** stat lines, INV-19 — every field except the map letter key, because the module ships no maps. Ticking this ✅ first time round was me grading my own homework generously; the honest mark is partial, and the fix is a map, not a card edit |
| 13 | Social set-pieces as italic-question / quoted-answer with "if friendly" tiers | ✅ | Corval at the gate, Vorlain by the wine, Raunu's summons |
| 14 | Settlements: stat line, authority figure, six NPCs, keyed sites | **n/a** | Single-site module. The palace *is* the settlement and is keyed |
| 15 | Second-person coaching, forecast mistakes, two-option troubleshooting, signed designer's note per part | ✅ | Four sidebars, each with two in-fiction answers; one signed note in the Overture |
| 16 | Honest difficulty: tier recipes, notes admitting a misleading rating, seams stating expected advancement | ✅ | **S2's card says it is a Skirmish labelled Standard**, and S3's prints its 8-exchange grind. `06` states the advancement seam |
| 17 | Names its own optional cuts, and reserves one location for the MM to fill | ✅ | **Both added this pass.** The abridged-run box, and **B13, The Room You Put Here** |
| 18 | Appendices hold what the table touches repeatedly | ✅ | `08` handouts, `09` cards, `characters/`, `enemies/` |

**15 of 18 met, 2 partial, 1 not applicable.** The two that were missing when I first
called this done — the prologue and the reserved room — are now written. The partial
(item 8) is a genuine mismatch between the checklist and this module rather than an
omission: an adventure with no dungeon has no floorboard to hide a ledger under. The
second (item 12's map letter key) is a real absence — the module has no maps at all,
which is a larger question than a rewrite should answer, and it is now recorded as
open rather than quietly ticked.

### Loose ends swept after the commit

Two stale references to the deleted prelude survived the first pass: `04`'s pointer
to Otta Vesh "(prelude wing)", and the README's running order telling a table to
start with `06`'s prelude nights. Both fixed. `06_Wings.md` is now `06_Aftermath.md`,
since it holds one wing and its chapter title says so. The rename swept
`adventures/` only — `docs/` records what was true when they were written, which is
the rule I broke once already this session and did not break again.

### Chapter numbering, fixed

Deleting Chapter VIII left the module numbered I–VII, IX, X. Handouts moved to
**VIII** and Scene Cards to **IX**, so the numerals are contiguous again, and `06`'s
title lost the "Prelude and" it no longer earns.

**The renumber went wrong the same way twice, and the second time was mine.** The
sweep was written to change `Chapter IX` → `Chapter VIII` and `Chapter X` → `Chapter
IX` in one pass — correct — but it was pointed at `docs/` and `references/` as well
as `adventures/`, and `docs/` is *history*. It rewrote nine historical records, and
worse, it mangled the placeholder `` `Chapter X.Y` `` — the invariant's own regex
pattern, not a reference to any chapter — into `` `Chapter IX.Y` `` in five files
including DECISIONS. Reverted the tracked records, restored the placeholder by hand
in the untracked ones.

`LOG_lineage.md` had already written the rule down: *`docs/`, `research/` and
`playtest/` are history — do not sweep them.* Having the rule and not applying it is
its own lesson, and the reason both are recorded here.

### Style pass

Scanned every new block against `style/STYLE_GUIDE.md`'s amateur/AI tells: no
"in conclusion", no "it is important to note", no section throat-clearing, no
"as mentioned above", no bulleted rule bodies, and no read-aloud that names a
creature or acts for the characters. Clean.

**INV-21 was defective and is fixed.** As first written it matched one line at a
time, which silently exempted every *multi-line* read-aloud — exactly the blocks most
likely to run long — while flagging one-line asides (Q&A questions, handout captions)
that are not read-aloud at all. It now joins consecutive blockquote lines before
measuring, and there is a test that the check can actually fail.

### Running time

**As written:** 4–6 hours. Movements I–V carry the ball; VI and VII carry the attack
and the gate. **Abridged:** 4 hours flat — cut Undercurrent A and the east-wing scene,
run S1 *or* S2, keep the gate. **With the aftermath:** three sessions, and a character
reaches Facet level 1.

### The acceptance question

*Can a table play this and come out having used every flagship mechanic once?*

| Mechanic | Where it is unavoidable |
|---|---|
| An exchange with Postures and reactions | S1 in Movements II–IV, S3 in VII |
| A Named enemy with a stated stance and a Technique | Tavva (S2); the Sergeant's *Hold the Terms* (S3) |
| A Boss whose phase the party sees | The captain, on his second exchange on the field — a conduct trigger, so it cannot arrive too late |
| A domain cast at Minor scope | Serane's and Ilesse's charges; Pello's Warning in Movement II's omen |
| A Spark spent, and one earned | Printed rewards throughout; every scene card prints its own |
| A Technique unlocked | Facet level 1 at the inquest, `06` |

**Yes.** That was the thing the module could not do before, and it is the reason all
four workstreams existed.
