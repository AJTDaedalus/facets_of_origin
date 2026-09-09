# DESIGN — Oraga Night, Rebuilt as the Starter Module

**Date:** 2026-09-08 · **Tier:** Planner · **Brief:** `docs/BRIEF_oraga_rewrite.md`
**Tasks:** `docs/TASKS_oraga_rewrite.md` · **Log:** `docs/LOG_oraga_rewrite.md`
**Branch:** `feat/oraga-rewrite`, off `main` with `feat/lineage`, `feat/valloh-facet` and
`feat/fun-second-act` all merged.
**Acceptance list:** `style/analysis/adventures.md` §9 checklist.

---

## 0. Where this sits in the program

The join. It needs Lineage (the pregens are built through it), the Val'loh Facet (their gifts are its
domains), and the Second Act (its scene cards are tuned against whatever R2/R3 became). Three hard
dependencies, and the reason the other three briefs exist.

**Do not tune twice.** If `fun_second_act` has not returned both verdicts, this workstream's simulation
tasks wait. Everything in M1, M3, M4, M6 and M7 can proceed meanwhile — only M2's numbers are blocked.

## 1. Approach

Most of the prose survives. What changes is the architecture, the opening, the combat arc, the
characters, and the magic chapter. So the work is organised as *apparatus around good prose*, not as a
rewrite: every task that would edit the agendas, omens, undercurrents, Fractures, the Crossing, or the
epilogue beyond a pointer line is out of scope and comes back to Planner. That constraint is what keeps
the module's quality — it is the reason it is the starter module rather than a replacement.

The module currently fails one test: a new table that runs it learns the core roll, Sparks, and
Specialties, and learns nothing about exchanges, domains, or growth. Every module below is aimed at that
one sentence. The acceptance question for the whole workstream: *can a table play this and come out
having used an exchange with postures and reactions, a Named enemy with a stance and a Technique, a Boss
whose phase they saw, a domain cast at Minor scope, a Spark spent and one earned, and a Technique
unlocked?*

## 2. Planner rulings made here

1. **Pregens ship as `.fof` files** at `adventures/oraga_night/characters/`, and `03`'s prose entries are
   generated from them into `<!-- statblock -->`-style markers the way the Bestiary already works. Five
   pregens hand-written in prose *and* five sheets is two sources for one truth, and this repo has
   already been burned once by that (the combat/simulator divergence). One source: the `.fof`.
2. **Scene-card stat lines are generated** by a new `software/tools/build_scene_cards.py`, sibling to
   `build_bestiary.py` and reusing its stat-block renderer. `09_Scene_Cards.md` gets a no-diff invariant.
   Hand-editing a generated stat line is forbidden here exactly as it is in the Bestiary.
3. **The Bought reskins are module-local.** `adventures/oraga_night/enemies/bought_{blade,sergeant,
   captain}.fof` carry Val'loh `description` and `organization`; `enemies/bought_*.fof` in the Bestiary
   stay setting-agnostic (B9). The reskin overrides flavour fields only — never Resolve, attack, armor,
   or Techniques, so `fun_second_act`'s settled numbers cannot be forked here.
4. **`08_Appendix_Tribes_of_Valloh.md` is already gone** (deleted in `valloh_facet` V14), as are the
   retired "no domains / gifts are flair" lines. This workstream's `02`/`03` work is the trim and the
   repoint, not the correction.
5. **The gate's Boss enters on a clock segment, not an exchange count.** The brief says "the clock's
   third segment or when the sergeant falls, whichever is first"; the simulation models it as an exchange
   index because the sim has no clock. The card prints the fiction; the sim's exchange-3 entry is the
   calibration proxy, and the LOG must say so, or a later reader will think the rule is "exchange 3".

## 3. Module breakdown

### M1 — Data first

- Module-local Bought reskins (ruling 3).
- Five pregens as `.fof` through Lineage and the Val'loh Facet (brief §8.2): Serane (Orthaen/Crystal,
  Soul, End 3), Pello (Phern/Warning, Body, End 4, Constitution 2), Andra (Orthaen/Crystal, Mind, End 3),
  Dassa (Orthaen **ungifted**, Body, End 5), Ilesse (Orthaen/Crystal, Soul, End 3). Two at Endurance 4–5;
  one gifted caster whose Minor-scope intents appear in the module's own examples.
- Each sheet prints **"At Facet level 1 you would likely take:"** with one named Technique, so a
  first-night table sees the road ahead. A gifted pregen's gift formalizes at that same level, free
  (D18).
- Dassa is the proof of the ungifted case: no gift, keeps her Background's secondary skill, and her
  Heritage (reads crystalwork) is in play.

### M2 — Simulate, then fix the numbers *(blocked on `fun_second_act`)*

`tools/combat_sim.py` driving `app/game/combat.py`. The simulator may never re-implement a rule.

| Card | Setup | Acceptance |
|---|---|---|
| **S3 The Gate** | PS-3 party; 1 Named (sergeant, Resolve 3, light, *Hold the Terms*) + 4 Mook blades; Boss captain (Resolve 6, heavy, *The Second Clause*, *Reform the Line*, phase at Resolve 3) entering exchange 3 | Win rate in the Hard band 40–60% counting **any** of the three endings as a win; the phase fires in exchange 2 of the captain's presence in ≥70% of runs; median fight 3–4 exchanges |
| **S2 Knives in the Dark** | Tavva (Named, Vanisher, stance triggers) + 2–3 gallery knives | Standard band 65–85% |
| **S1 The Seating Feud** | — | No sim; Tier 1 only |

Tune the captain's Resolve and entry point, **not the recipe** — the recipes are Recipe-Table shapes and
changing them would mean the module is not demonstrating the MM1 budget it teaches.

### M3 — The Overture rebuilt (front-matter battery)

Eight elements in the brief's order: what this adventure is (party 3–5; Facet level 0 → 1 by the end of
the aftermath wing; 4–6 hours as written, 3 sessions with the aftermath) · what you need (core rules +
`settings/valloh/`; every enemy's Resolve, stance and Techniques are on its scene card) · the story so
far · a synopsis paragraph per Movement each ending with the world-state · **six named converging
hooks** (The Invited · The Entourage · The Discarded Invitation · Hired for the Night · The Patron's
Errand · The Wrong Place, Deliberately), each 3–6 sentences, each naming which agendas fit it, each
ending *"Begin at the Gatehouse Court, B1, Movement I."* · running the night, plus a new paragraph on
nudging a restless table toward one of the three fights without forcing anyone · the format legend
(`**B1.**` keys, italic read-aloud with trigger lines, three sidebar species, scene-card IDs S1–S5, the
enemy notation, the clock column) · safety, unchanged.

One signed designer's note per Part. The Overture's says why the Uninvited cannot be beaten and what the
fights are *for*.

The prelude wing is deleted; its content survives as hooks and as facts stated in the introduction (the
extra swords every house hired; the mask-maker becomes one aftermath paragraph).

### M4 — Movement I as the first scene

New key **B0. The Approach and the Line**, before B1. Read-aloud on first sight of the lit palace (the
existing block). Then the line as the year's best gossip hour, with the approach loop beginning here:
Corval receiving by name; the Thenya delegation's thinning patience; the burned-invitation footman
selling a card two places ahead (the Discarded Invitation hook made visible); every great house's hired
swords idling at the court's edge, *House Boranis hired none*; a tall pale factor already inside. The
omen — nine honor guards, facing inward — unchanged. Rumor Table rolls legal from the first minute.

**The first roll of the night is a social one at Standard**, with the 7–9 named from the MM2 table, and
the designer's note says why: the first roll teaches the tier the game lives in.

### M5 — The clock and the alert state

- **The night clock**, one page in `09`, as a table with a column per actor (the Uninvited, the Bought)
  and a fourth column of indented conditional lines that *are* the mission menu: what the players can
  move at each bell. Brief §5.1 has the content.
- **The palace on alert**, one paragraph above the keyed rooms in `04`: what the honor guard does when
  steel is bared, when the east wing is forced, when the lights die; what the Bought do at each bell.
  Room entries then say *if alerted* and stop.

### M6 — The gate at midnight (B12) and the Bought

The module's Hard fight and its only beatable, talkable antagonist. Contract per brief §6.1; scene,
clock, objective and three endings per §6.2; the ⟨If History Breaks⟩ branch where the company is bought
out before midnight per §6.4; the aftermath thread per §6.5.

The three endings are written as paired conditionals: **fight through** (morale disengagement, the
captain placing blades and watching who the party protects, the Second Clause invoked the exchange after
the party looks like winning, negotiation opening at Resolve 3), **void the contract** (proof of broken
terms, the named target already gone, or a better offer made in front of the sergeants — the
Persuade-ends-the-fight route III.3 promises), **the sect guard** (a party that only *holds* has won).

Constraints that are not negotiable: the Bought never learn who hired them and the module never says;
"old coin" stays a deliberate red herring the aftermath can untangle but never confirms (S3); the Second
Clause must never succeed — Veier leaves by the river, and the branch where a table brings her to the
front is written with the captain's honour clause and the sect guard as the outs.

### M7 — Scene cards, characters, apparatus

- `09_Scene_Cards.md`: S1–S3 full cards, S4–S5 half-cards, fixed field order per brief §7 (ID and title →
  *Use with* pointer → recipe line → trigger read-aloud → objective and clock → generated stat lines →
  tactics with opening move, priority target and a morale line each → two or three terrain-as-rules lines
  → outs → Sparks printed → Development). Pointer lines both ways.
- `03` *Making Characters* rewritten to the seven steps with the Val'loh Facet loaded: Orthaen (gifted or
  not; four in five are gifted) or, rarely and with MM agreement, Phern. One page; must not restate the
  Facet.
- **Advancement happens** (`06`): the one-shot ends with the standard 4 skill points and a reflection
  scene at the epilogue question; the aftermath wing over two sessions lands Facet level 1 under D16a's
  floor, and `06` places the reflection scene at the inquest. This is the single largest change to what
  the module *proves*.
- Three Q&A dialogue blocks in `07` (Corval at the gate, Vorlain by the wine, Raunu's summons) plus cast
  entries for the Bought's sergeant and captain with their negotiation surface printed.
- Four troubleshooting sidebars and the abridged-run box (four hours: cut Undercurrent A and the east-wing
  scene; run S1 or S2, not both; the gate as written).

## 4. Testing strategy

- `build_scene_cards.py` generates every stat line on the cards from the module's `.fof` files into
  `<!-- statblock: id -->` markers; a no-diff invariant, the Bestiary's rule applied here.
- Pregen prose in `03` regenerates from the `.fof` files to no diff (ruling 1).
- INV-5's `Chapter X.Y` resolution extended to `adventures/`, so the module's PHB pointers resolve.
- Read-aloud blocks under 120 words, by test: a word count over italic blocks carrying a trigger line.
- Every scene-card enemy exists as a `.fof` and its TR recomputes.
- The humanizer pass and the style guide's amateur-tells list over every new block. The recurring PHB cast
  does not appear — this is a module — but the read-aloud rules do.
- Full suite green with a reported pass count.

## 5. Risks and mitigations

- **Scope creep into good prose.** The out-of-scope rule in §1 is the mitigation, and it is written into
  the task file so a Worker can invoke it.
- **Lengthening the one-shot.** Every addition is a card the MM can skip; the abridged box protects the
  four-hour promise; the acceptance for M7 includes a stated running time.
- **The read-aloud discipline slipping on new blocks.** B0 and B12 are new prose in a module whose
  existing blocks are good. Nothing in a read-aloud names a creature or resolves an action.
- **The spoiler boundary.** The factor has no face and no name. Any draft that gives him one is rejected.
- **Double-tuning.** M2 waits for `fun_second_act`'s verdicts. There is no provisional number worth the
  rework.

## 6. Open questions for the owner (non-blocking; tracked in `INVENTIONS_FOR_REVIEW.md` Revision 4)

Every new invention here: the Bought's contract and its three tasks, the factor, the old coin's dynasty,
the six hooks' details, B0's line scenes, every Q&A answer line not already in the module, and the
Heritage/gift material inherited from the Val'loh Facet.
