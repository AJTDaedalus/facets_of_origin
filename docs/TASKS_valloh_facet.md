# TASKS — The Val'loh Setting Facet

**Design:** `docs/DESIGN_valloh_facet.md` · **Brief:** `docs/BRIEF_valloh_facet.md`
**Log:** `docs/LOG_valloh_facet.md` · **Branch:** `feat/valloh-facet` off a merged `feat/lineage`
**Blocked until:** `TASKS_lineage.md` L15 is done. Do not start otherwise — `LineageDefinition` and
INV-16 must exist.

---

## M0 — First

**V1. Write the counted-novelty line.** — 15 min
Files: `docs/LOG_valloh_facet.md`.
Copy DESIGN §1's sentence into the log as the acceptance test every later task is read against. It goes
into `V0` verbatim at V13.
Accept: the sentence is recorded and names exactly three additions.

## M1 — Data

**V2. Schema: `ItemDefinition`, `lineage_gift`, `draft`.** — 45 min
Files: `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`.
Tests first. `ItemDefinition{id, name, kind, scope, effect}`; `lineage_gift: bool = False` and
`draft: bool = False` on the domain definition. Docstrings in `BackgroundDefinition`'s register.
Accept: loads; unknown `kind` rejected; `scope` restricted to minor/significant/major; ≥3 tests each.

**V3. Merge `items` by id.** — 30 min
Files: the `MergedRuleset._merge` module, `software/tests/test_facet_loading.py`.
Mirror the `backgrounds`/`lineages` loop; add `_item_map`.
Accept: a second module adds an item; a collision replaces by id; ≥3 tests.

**V4. `software/facets/valloh/facet.yaml` — the ten lineages.** — 60 min
`id: valloh`, `priority: 1`, `requires: [base]`. Brief §3's table. `playable` per DESIGN §3/M1.
Nothing in `roll_resolution`, `spark`, `advancement`, `magic` rules, or `combat`.
Accept: loads with `base`; INV-16 passes for all ten gifts once V5 lands; without `valloh`, the merged
base is byte-identical to today.

**V5. The ten gift domains.** — 75 min
Files: the same yaml, `magic.soul_domains`.
All Focused, intuitive tradition, `requires_tier3: false`, `lineage_gift: true`, `draft: true` on every
example intent. Territories, *beyond-the-focus*, and three intents per scope from brief §5, verbatim.
Accept: ten entries; INV-16 green; every intent carries `draft: true`.

**V6. Crystal charges as items.** — 30 min
Files: the same yaml, `items`.
Six Minor consumables: steady light, seal a door, veil of quiet, chime at a threshold, warmth, held
image.
Accept: six entries; each is a valid `inventory` string id.

## M2 — Engine

**V7. `lineage_gift` filters the Tier 1 Technique's domain list.** — 45 min
Files: `software/app/game/character.py`, `software/tests/test_character.py`.
Tests first. A Soul or Mind character's Tier 1 magic Technique cannot pick a `lineage_gift` domain; a
lineage-gifted character's free formalization (Lineage L10) can.
Accept: both directions tested; a core-only ruleset is unaffected; ≥3 tests.

**V8. `use_item` and the `item_used` event.** — 45 min
Files: `software/app/game/character.py` (or `engine.py`, wherever inventory lives),
`software/app/api/websocket.py`, `software/tests/test_character.py`,
`software/tests/test_websocket.py`.
Tests first. Removes the entry, emits the event, no roll, no arithmetic.
Accept: a second use of a spent charge is rejected; an unknown id is rejected; the event carries the item
name and effect; ≥3 tests per function.

**V9. Sim the Bond's reaction clause.** — 45 min
Files: `software/tools/combat_sim.py`, `research/simulation_log.md`, `docs/LOG_valloh_facet.md`.
A free Intercept at the Bond's difficulty on a loved one, PS-3, the standard harness.
Accept: a written verdict — the clause prints in `V2`, or it is cut and the Bond is an ordinary
reaction-shaped intent. Either way the reason and the numbers are recorded.

## M3 — The book

**V10. `settings/valloh/V1_Lineages.md`.** — 90 min
Ten entries in II.5's four-field format, never printed empty. Krenn is not listed among the tribes a
player meets. State the ungifted rule once.
Accept: entry format matches II.5 exactly; INV-9/10/13 green; new invention flagged for V16.

**V11. `V2_Magic_of_Valloh.md`.** — 60 min
Gifts as domains; spellcraft as the scholarly tradition in one paragraph (D17: no tempo rule, no per-day
limit); the crystal charge. **Must not restate II.3.**
Accept: no rule appears here that `facet.yaml` or II.3 does not already carry; INV-7 extended and green.

**V12. `V3_Rekuzan_and_the_Tribes.md` and `V4_Adaptation.md`.** — 75 min
`V3`: gazetteer compressed from Oraga `02`'s public section, timeline as a table at the end including
the 3164 mist-tides. `V4`: adaptation within one world (S2), what the Facet changes, counted.
Accept: `V4`'s counts equal `V0`'s; no MM-only truth from `02` leaks into either.

**V13. `V0_Ten_Things.md`.** — 60 min
Fragment-triplet opener, tone tied to Sparks, one-page summary, the Ten Things from brief §6, the
counted-novelty line from V1, reading order. First page states Val'loh is a continent of Shattered
Origin's world.
Accept: three pages; INV-17 (V15) passes against it.

**V14. Retire the retired canon in the module.** — 30 min
Files: delete `adventures/oraga_night/08_Appendix_Tribes_of_Valloh.md`; one-line pointer in
`adventures/oraga_night/README.md`; strike "there are no magic domains in Val'loh", "nobody casts in a
crisis", and "gifts are flair" from `02_The_World_and_the_Night.md` and `03_Masks_and_Agendas.md`.
Nothing else in the module changes here — the rest is `oraga_rewrite`.
Accept: no file in the repo asserts that Val'loh has no domains; the module still reads coherently;
`git diff` touches exactly these four files.

## M4 — Invariants and close-out

**V15. INV-17: the pitch cannot drift from the file.** — 45 min
Files: `software/tests/test_docs_consistency.py`.
Parse `V0`'s counts (lineages, `lineage_gift` domains, items) and compare against the merged ruleset with
`valloh` loaded.
Accept: changing a count in the yaml without changing `V0` fails the suite, and vice versa.

**V16. `INVENTIONS_FOR_REVIEW` entry.** — 30 min
Files: `references/oraga_night/INVENTIONS_FOR_REVIEW.md` (or a new
`references/valloh/INVENTIONS_FOR_REVIEW.md` if the Oraga file is module-scoped).
Table every invention: ten Heritages, thirty example intents, the *beyond-the-focus* lines, Fthala's
drafted rate, the Bond's clause verdict.
Accept: the owner can read one table and rule on the lot; each row points at its file and line.

**V17. Suite, log, handoff.** — 20 min
Files: `docs/LOG_valloh_facet.md`, `docs/DECISIONS.md`.
Accept: full suite green with a reported pass count; merge-without-`valloh` regression green;
`oraga_rewrite` is unblocked on Track 1 and the LOG says which Planner rulings (DESIGN §2) shipped.

---

## STATUS: COMPLETE (V1–V17) — 2026-09-09

Every task in this file is done. Full suite green.

Ten lineages, ten gift domains, six crystal charges, `settings/valloh/V0`–`V4`. The Bond's reaction clause was simulated and **cut**. Found and fixed the singleton-`magic` bug (D21) before it could delete the core's catalog.

Execution record, including what the numbers changed and what went wrong on the way: `docs/LOG_valloh_facet.md`.
