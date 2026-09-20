# TASKS — Lineage

**Design:** `docs/DESIGN_lineage.md` · **Brief:** `docs/BRIEF_lineage.md` · **Decision:** D18
**Log:** `docs/LOG_lineage.md` · **Branch:** `feat/lineage` off `main`
**Baseline:** 1579 tests collected, all green, before task 1.

Workers: one task at a time; the DESIGN and this file are the only state you need. Mark done/blocked
here and append to the LOG before stopping.

---

## M1 — The renumber (its own commit; no content changes in it)

**L1. Rename the two chapter files.** — 15 min
Files: `player_handbook/II.6_Character_Creation_Skills.md`,
`player_handbook/II.5_Character_Creation_Backgrounds.md`.
`git mv` **II.6 → II.7 first**, then II.5 → II.6. Reversing the order overwrites a file.
Accept: both renames staged; no content edited; suite red only where references now dangle.

**L2. Sweep every reference.** — 45 min
Files: `player_handbook/` (II.3, II.4, II.4a, II.4b, II.4c, II.7, Quick_Start, Glossary,
Table_of_Contents, Front_Matter, Appendix_Character_Sheet), `mm_manual/MM5_Quick_Reference.md`,
`bestiary/`, `adventures/`, `spec/`, `references/`, `software/tests/test_docs_consistency.py`,
`software/tools/build_table_register.py`, `characters/`, `style/`.
Always rewrite the highest number first. `docs/`, `research/` and `playtest/` are history — do not sweep
them.
Accept: no `Chapter II.5` means Backgrounds anywhere; no `II.5_Character_Creation_Backgrounds` path
survives; INV-5 green.

**L3. Regenerate and prove the sweep.** — 20 min
Files: `player_handbook/Index.md`, `List_of_Tables.md`, `List_of_Boxes.md` (all generated — never
hand-edit).
Run the generators and the cross-reference resolver.
Accept: INV-4/5/9/10 green; **full suite green**; `git diff --stat` reads as a pure rename plus
regenerated files. Commit here, alone.

## M2 — Data, schema, merge

**L4. `LineageDefinition` schema.** — 40 min
Files: `software/app/facets/schema.py`, `software/tests/test_facets_schema.py`.
Tests first. Fields per DESIGN §2/M2, docstrings in `BackgroundDefinition`'s register.
Accept: loads; `playable` defaults true; `formalizes_on` rejects an unknown value; ≥3 tests.

**L5. `lineages` in the base ruleset + merge loop + `_lineage_map`.** — 40 min
Files: `software/facets/base/facet.yaml`, `software/app/facets/loader.py` (or wherever
`MergedRuleset._merge` lives), `software/tests/test_facet_loading.py`.
Tests first: a second module adds a lineage; a collision replaces by id; `human` survives.
Accept: `human` present with empty `gift_domains`; merge mirrors `backgrounds` exactly; ≥3 tests.

**L6. INV-16 — every gift domain resolves.** — 30 min
Files: `software/tests/test_docs_consistency.py` (or the schema validator, whichever INV-7 uses),
`software/tests/test_facets_schema.py`.
Accept: a lineage whose `gift_domains` names an unknown domain fails at load with a readable message;
`human` (empty list) passes; the invariant is numbered and described like its siblings.

**L7. `spec/` catches up.** — 20 min
Files: `spec/FOF-SPEC-v0.1.md` §4.3, `spec/types/ruleset.md`.
Accept: `lineages[]` documented as a collection section keyed by `id`, in the format `backgrounds` uses.

## M3 — Character model and creation validation

**L8. Three character fields.** — 30 min
Files: `software/app/game/character.py`, `software/tests/test_character.py`,
`software/tests/test_character_fof.py`.
Tests first. `lineage: str = "human"`, `gifted: bool = False`,
`domain_source: Optional[Literal["lineage","background","technique"]]`. Keep `magic_domain` as the single
primary-domain field — no `lineage_domain`.
Accept: every existing `.fof` under `characters/` and `playtest/` loads with `lineage == "human"` and no
file edited; ≥3 tests.

**L9. Creation validation: one domain, from one source.** — 45 min
Files: `software/app/game/character.py` (~:1004, the `domain_replaces_secondary` site),
`software/tests/test_character.py`.
Tests first, all four cases in DESIGN §2/M3.
Accept: gifted + domain-granting Background rejected with a message quoting the one-domain rule; gifted
creation sets `magic_domain`, `domain_source="lineage"`, and skips the secondary mark exactly as
`skip_secondary` does; ungifted member of a gifted lineage keeps the secondary and holds no domain.

## M4 — The formalization hook

**L10. Free formalization at the first Facet level.** — 50 min
Files: `software/app/game/character.py` (the `advance_skill` path that sets Facet level),
`software/tests/test_character.py`, `software/tests/test_advancement_pacing.py`.
Tests first. On the first Facet level in **any** Facet, a `domain_source == "lineage"` domain with
`formalizes_on == "first_facet_level"` goes active and **no Technique pick is recorded**.
Guard the existing `formalizing = tech_def.magic_granting and choice == self.magic_domain` branch so it
does not fire for a lineage domain that is already active.
Accept: pick count after formalization is unchanged; a three-pick career is still three picks; the
`formalizes_on: technique` path reproduces today's behaviour exactly; ≥3 tests including the
double-fire regression.

## M5 — The chapter and its amendments

**L11. Write `player_handbook/II.5_Lineage.md`.** — 90 min
Sections per DESIGN §2/M5, in that order. The Heritage paragraph must state that it shares the one-step
allowance with Specialties and Techniques. Both Through-the-Mirror boxes declare their species.
Accept: INV-9/10/13 green; prose passes the humanizer and the style guide's amateur-tells list; no
mechanic appears here that `facet.yaml` does not carry.

**L12. The amendments.** — 60 min
Files: `player_handbook/II.1_Character_Creation_Overview.md` (six steps → seven, Lineage at 3, the
Zulnut line), `II.3_Magic.md` (third origin; *Before the Technique* exception pointer),
`II.4_Character_Creation_Facets.md` (*Techniques*: a Gift leaves the pick free),
`II.6_Character_Creation_Backgrounds.md` (one-domain rule in *Magic and Backgrounds*),
`Quick_Start.md` (one line under step 2), `mm_manual/MM3_Campaign_Design.md` (a paragraph pointing at
the custom-lineage steps and the setting-Facet pitch format), `Glossary.md` (Lineage, Gift, Heritage),
`Appendix_Character_Sheet.md` (a Lineage line under Background), `references/phb-examples.md`.
Accept: one sentence each where the brief says one sentence; INV-2/3/11/12 green; Table of Contents and
Front Matter updated; registers regenerate to no diff.

## M6 — API and app

**L13. Creation API fields.** — 30 min
Files: `software/app/api/` (the create-character request model), `software/app/api/websocket.py`,
`software/tests/test_api.py`, `software/tests/test_websocket.py`.
Tests first. `lineage` (default `"human"`), `gifted` (default `false`); validation happens in the
character model, not the handler. Session-state payload serializes lineages beside backgrounds.
Accept: no rule logic in the handler; ≥3 tests including the rejection path.

**L14. The builder's Lineage picker.** — 45 min
Files: `software/app/static/js/builder.js`, `software/tests/e2e/`.
Between Facet and attributes. **Hidden when the merged ruleset holds only `human`.**
Accept: with only `base` loaded the picker does not render; with a second module supplying a lineage it
does, and a gifted choice offers that lineage's `gift_domains`.

## Close-out

**L15. Suite, log, handoff.** — 20 min
Files: `docs/LOG_lineage.md`, `docs/DECISIONS.md` (D18 amended with what shipped).
Accept: full suite green with a reported pass count (baseline 1579 + new); every `.fof` in the repo still
loads; `valloh_facet` is unblocked and the LOG says so.

---

## STATUS: COMPLETE (L1–L15) — 2026-09-09

Every task in this file is done. Full suite green.

II.5 shipped, Backgrounds → II.6 and Skills → II.7, data + schema + merge + character fields + free formalization + API + builder picker. Decision D18, amended with what shipped.

Execution record, including what the numbers changed and what went wrong on the way: `docs/LOG_lineage.md`.
