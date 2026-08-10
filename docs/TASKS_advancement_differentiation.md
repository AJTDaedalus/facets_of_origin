# TASKS — Advancement Differentiation

**From:** `docs/DESIGN_advancement_differentiation.md` · **Ruling:** D16

---

- [x] **T1 — Schema.** `MarksPerRankDef` (3/5/8, `for_rank`), `RankCapsDef`
      (`beyond_practiced`, `master`, both `None` = uncapped), `marks_per_rank`
      validator expanding a legacy integer with a `DeprecationWarning`,
      `facet_level_threshold` default 5 → 3.
- [x] **T2 — `facet.yaml`.** Per-tier marks, `rank_caps`, threshold 3, with the
      DESIGN_v0.3 §6.2 comments rewritten to cite D16.
- [x] **T3 — Engine.** `rank_ceiling_for` (single source of truth for the cap),
      `cap_refusal_reason`, `_occupies_beyond_practiced` / `_occupies_master`
      (slot claimed on commitment), `_try_advance_rank` takes a ceiling and
      re-reads the per-tier threshold as the rank climbs, `advance_skill`
      refuses rather than absorbing. Stale "Stops at expert rank" docstring
      fixed in passing.
- [x] **T4 — Spend ordering.** `Character.spend_skill_point` and the MM-driven
      `skill_advance` WebSocket handler both check the cap **before** deducting
      SP, so a refusal never strands a point.
- [x] **T5 — Tests.** `test_advancement_pacing.py` rewritten around the new
      invariants (29 tests): caps, curve, levels at 3/6/9, Major at level 3,
      and the differentiation invariant. `test_character.py`,
      `test_facets_schema.py`, `test_facet_loading.py`, `test_fof_loader.py`,
      `test_character_fof.py`, `tests/e2e/test_ui_flows.py` retuned.
- [x] **T6 — App.** Skill Advancement card shows the per-tier curve and the cap
      slots, both read from the ruleset.
- [x] **T7 — PHB.** II.4 (*Advancing Skills* cost table, new *How Far a Skill
      Can Go* section, *Facet Levels*, both *Through the Mirror* boxes, the
      counting example, *Advancement at a Glance*, *Career Advances*), II.6
      (Table II.6–2 + cap pointer), Glossary (Mark, Rank, Facet Level),
      Appendix Character Sheet (mark costs + Rank Slots table).
- [x] **T8 — MM Manual.** MM3–2 recomputed with a Fastest-Legal column,
      MM3–3/MM3–4 re-banded to the 27-advance ceiling, *Pacing Advancement*
      warned off raising the caps; MM5 *Skill Advancement* block.
- [x] **T9 — Spec and tooling.** `spec/types/ruleset.md`,
      `spec/examples/base-ruleset.fof`, `tools/agentic_playtest/context.py`.
- [x] **T10 — Finding aids.** `Index.md`, `List_of_Tables.md`,
      `List_of_Boxes.md` regenerated.

---

## W-1 — The creation-rank off-by-one (found during T5, fixed in T3)

**Discovered:** the BRIEF and DESIGN both assume a shaped Facet yields 9 rank
advances. Driving a real character through the engine showed **8** for anyone
with a Background, and Facet level 3 therefore unreachable inside the primary
Facet — 2 Technique picks, not 3.

**Cause, and it is older than D16.** A Background's starting skill is always in
the Primary Facet (II.5), and P-6 excluded creation ranks from the Facet-level
track. So the in-Facet ceiling was always one advance short of what the book
claimed: **14 of 15 under v0.3** (threshold 5 → level 3 needs 15) and 8 of 9
under D16. Facet level 3 has never been reachable in-Facet for any character
that has a Background, which is all of them. The guard that should have caught
it, `test_level_three_reachable_in_facet`, compared `3 × threshold` against the
raw skill count and never built a character.

**Fix:** credit the Background's starting rank to its Facet's level track
(`create_default_character` seeds `rank_advances_by_facet`). One banked advance
out of the three a level costs — a head start, not a free level; a fresh
character is still Facet level 0 and still needs two advances in play to reach
level 1. P-6's intent ("a Facet level is earned by growth in play") survives in
substance.

**Rejected:** dropping `facet_level_threshold` to 2 to fit the 8-advance
ceiling — it puts Facet level 3 and every Technique at ~5.5 sessions, far
inside the target window. Loosening the caps to 4-beyond-Practiced fits the
arithmetic exactly but collapses differentiation to 20 shapes with only one
skill left at Practiced, which is the ruling itself traded away for a rounding
error.

**Now guarded by:** `test_facet_level_three_is_reachable_inside_the_primary_facet`,
which builds a real character with a Background and drives it to the cap.

---

## Verified pacing (real engine, cheapest-advance-first)

| Character | In-play advances | Marks | Sessions (4 SP) | Facet level | Picks |
|---|---|---|---|---|---|
| No Background | 9 | 38 | 9.5 | 3 | 3 |
| City Watch Veteran | 8 | 35 | 8.75 | 3 | 3 |
| Guild Apprentice (magic) | 8 | 35 | 8.75 | 3 | 3 |

---

*All tasks complete. Open for playtest: A3's veteran revisit trigger and A4's
cross-Facet pacing, per the BRIEF.*
