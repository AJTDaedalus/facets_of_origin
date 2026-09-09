# LOG — Lineage

**Design:** `docs/DESIGN_lineage.md` · **Tasks:** `docs/TASKS_lineage.md` · **Decision:** D18

---

## 2026-09-08 — L1 through L14, complete

| Task | Status | Note |
|---|---|---|
| L1 rename | ✅ | II.6 Skills → II.7 first, then II.5 Backgrounds → II.6. |
| L2 sweep | ✅ | See the correction below — the first attempt was wrong and was reverted. |
| L3 regenerate | ✅ | Index, table/box registers, Bestiary all regenerate to no diff; INV-4/5/9/10 green. |
| L4 schema | ✅ | `LineageDefinition`; 7 tests. |
| L5 data + merge | ✅ | `lineages` merged by id with a `_lineage_map`, mirroring `backgrounds`; `human` in the base ruleset; serialized to clients so the picker can render. 6 tests. |
| L6 INV-16 | ✅ | Every gift domain resolves in the merged catalog. 3 tests. |
| L7 spec | ✅ | `lineages[]` in FOF-SPEC §4.3's collection list and a full section in `types/ruleset.md`. |
| L8 character fields | ✅ | `lineage` (defaulted), `gifted`, `domain_source`. No parallel `lineage_domain`. |
| L9 creation validation | ✅ | Unknown lineage, gifted-on-ungifted, wrong gift domain, and the one-domain rule all rejected with the reason. 9 tests. |
| L10 formalization | ✅ | `_formalize_lineage_gift`, called from `advance_skill` when a Facet level lands. 8 tests. |
| L11 II.5 chapter | ✅ | Reading the Entries, Human, the Gift-is-a-domain rules, Formalization, and the MM-facing custom-lineage steps, with two Through-the-Mirror boxes and one MM Note. |
| L12 amendments | ✅ | II.1 (six steps → seven), II.3 (third origin + the formalization exception), II.4 (the pick stays free), II.6 (one domain at creation), Quick Start, MM3, Glossary (Lineage, Gift, Heritage), character sheet, `references/phb-examples.md`, ToC, Front Matter. |
| L13 API | ✅ | `lineage`/`gifted` on the create request, defaulted; every rule stays in the character model. 3 tests. |
| L14 builder picker | ✅ | Between Facet and attributes, hidden when the ruleset holds only `human`. |

### The renumber went wrong once, and the way it went wrong is worth keeping

The first sweep matched `Chapter II.5` and `Chapter II.6`, which is what the
DESIGN said to sweep. It missed every reference that was not in that exact form:
`Chapters II.6, II.4` (plural, in the Glossary's *Rank* entry), `Table II.6–1`
and `Table II.6–2` (captions inside the Skills chapter), the Table of Contents'
bare list entries, II.1's chapter index, `(see *Magic and Backgrounds*, II.5)`,
and MM5's `(II.5, *Specialty*)`. Worse than missing them: the Glossary's *Rank*
entry pointed at Skills, and leaving it at `II.6` silently repointed it at
**Backgrounds**. Nothing failed. Every test stayed green, because a chapter
reference that resolves to the wrong existing chapter resolves.

Reverted and redone with the rule that is actually exact: at the moment of the
sweep, **every `II.6` means Skills and every `II.5` means Backgrounds**, so a
blanket `II.6 → II.7` followed by `II.5 → II.6` is correct by construction and
catches every reference form at once. 94 references across 12 files.

Two files were clobbered by the revert because they also carried unrelated
Second Act changes (`schema.py`, `character.py`, `II.4a`); re-applied.

**For the next renumber:** sweep the bare number, in descending order, and do it
before anything else touches the same files. INV-5 cannot catch a
reference that resolves to the wrong chapter, and no test in this repo can. That
gap is worth an invariant of its own if a third renumber is ever on the table.

### Design notes worth keeping

- **`domain_source` earns its place.** Without it the formalization hook cannot
  tell a Gift from a Background domain, and the existing `formalizing` branch in
  `_validate_domain_choice` would let a later Facet level spend a pick
  re-formalizing a Gift that had already arrived. There is a test named for
  exactly that.
- **The picker hides itself.** A step with one possible answer is not a choice.
  A setting Facet that adds lineages makes it appear with no JS change.
- **The gifted paths are tested against a synthesised gifted ruleset**, not
  against Val'loh, so this workstream does not depend on the next one.

### L14's acceptance named `tests/e2e/` and I did not go there

Marked done on the strength of the JS being written and the Python suite being
green. The task file said the picker's tests live in `software/tests/e2e/`, and
the Python suite cannot see the failure the front-end audit was full of: a control
that exists, looks enabled, and is wired to nothing.

Added afterwards (with the R3 rider menu, which had the same gap): **five e2e tests
for the Lineage picker** — hidden on the core ruleset, a guard that the core really
does ship one lineage so "hidden" stays the right assertion, the picker appearing
and rendering variants when a Facet supplies lineages, a gifted lineage offering its
domains with the rate and Heritage shown, and `selectedGift()` returning null while
the control is hidden so a core-rules character is never submitted as gifted.

**Resolved. Return to `TASKS_valloh_facet.md` V1 — the Val'loh Facet is unblocked.**
