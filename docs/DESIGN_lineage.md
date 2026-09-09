# DESIGN — Lineage: a Core Creation Step

**Date:** 2026-09-08 · **Tier:** Planner · **Brief:** `docs/BRIEF_lineage.md`
**Tasks:** `docs/TASKS_lineage.md` · **Log:** `docs/LOG_lineage.md`
**Branch:** `feat/lineage` off `main` · **Decision of record:** D18
**Baseline at planning time:** PHB runs I → II.1–II.6 → III.1–III.3 → IV.1; 1579 tests collected.

---

## 0. Where this sits in the program

Track 1, first. `valloh_facet` loads through this and cannot start until it merges. Independent of
`fun_second_act`, which runs in parallel on Track 2. `oraga_rewrite` needs both tracks.

## 1. Approach

The chapter renumber is the risky part and it carries no new content, so it ships **first, alone, on a
green suite**. Everything after it is additive: one merged collection, one schema model, three character
fields, one validation rule, one advancement hook, one chapter, and a picker.

The renumber is deliberately not avoided. A `II.4d` insertion would have saved a one-time sweep and cost
the book forever — Lineage would read as part of the Facets chapter. The tooling for exactly this sweep
exists (the cross-reference resolver, INV-4/5/9/10), so the sweep is a task, not a hazard. Measured
blast radius: 94 `Chapter II.5` / `Chapter II.6` / filename references across 12 shipping files, of which
`Index.md`, `List_of_Tables.md` and `List_of_Boxes.md` are generated.

## 2. Module breakdown

### M1 — The renumber (its own commit, nothing else in it)

`II.5_Character_Creation_Backgrounds.md` → `II.6_…`; `II.6_Character_Creation_Skills.md` → `II.7_…`.
**Rename II.6 → II.7 first**, then II.5 → II.6, or the second rename overwrites the first.

Sweep, then regenerate, then resolve:
1. `git mv` both files in that order.
2. Rewrite references across `player_handbook/`, `mm_manual/`, `bestiary/`, `adventures/`, `spec/`,
   `references/`, `software/` (`test_docs_consistency.py`, `build_table_register.py`), `characters/`,
   `style/`. Highest-numbered first, always, in every sweep.
3. Regenerate `Index.md`, `List_of_Tables.md`, `List_of_Boxes.md`.
4. INV-4/5/9/10 green, full suite green, and **no other change in the diff**.

`docs/` is history and is not swept; `research/` and `playtest/` are records of what was true then.

### M2 — Data, schema, merge

**`software/facets/base/facet.yaml`** gains a top-level `lineages` collection merged by `id`, exactly as
`backgrounds` is:

```yaml
lineages:
  - id: human
    name: Human
    variants: [folk, people]
    description: >
      The default of the core rules and of Shattered Origin ...
    gift_domains: []                    # empty list = ungifted
    gift_rate: null                     # fiction only; a string when present
    heritage: null
    playable: true
    formalizes_on: first_facet_level    # D18 option 1; ignored when gift_domains is empty
```

**`software/app/facets/schema.py`** gains `LineageDefinition`, mirroring `BackgroundDefinition`'s
docstring discipline. `formalizes_on: Literal["first_facet_level", "technique"] = "first_facet_level"`
— option 2 stays reachable as data so a setting could choose it, per the owner's ruling that §3.4 is
settled but the field stays.

**Merge.** `MergedRuleset._merge` gains the same loop it runs for backgrounds, plus a `_lineage_map`.

**INV-16 (new).** Every id in every lineage's `gift_domains` resolves in the merged domain catalog. This
is INV-7's sibling and it is what stops the Val'loh Facet from shipping a gift that points at nothing.

**`spec/`.** `FOF-SPEC-v0.1.md` §4.3 gains `lineages[]` under collection sections keyed by `id`;
`spec/types/ruleset.md` gains the section.

### M3 — Character model and creation validation

`software/app/game/character.py`:

| Field | Type | Why |
|---|---|---|
| `lineage` | `str = "human"` | defaulted, so every existing `.fof` in `characters/` and `playtest/` loads unchanged and the loader never requires the field |
| `gifted` | `bool = False` | ungifted member of a gifted lineage is a real and common case |
| `domain_source` | `Optional[Literal["lineage","background","technique"]]` | recorded when `magic_domain` is set, so the formalization hook knows which rule applies |

`magic_domain` stays the single primary-domain field. **No parallel `lineage_domain`** — two fields
meaning the same thing is how the Strike/`combat_sim` divergence started.

**Creation validation**, at the `domain_replaces_secondary` site (~character.py:1004):
- `gifted` **and** the Background carries `domain_origin` → reject, quoting the one-domain rule.
- `gifted` → the lineage's `gift_domains` must be non-empty, the chosen domain must be in it,
  `magic_domain` is set, `domain_source = "lineage"`, and the secondary-skill mark is skipped exactly as
  `skip_secondary` does today.
- ungifted member of a gifted lineage → keeps the secondary skill, holds no domain, keeps the Heritage.

### M4 — The formalization hook

Where a Facet level increments (the `advance_skill` path that sets Facet level): if
`domain_source == "lineage"` and `formalizes_on == "first_facet_level"` and the magic Technique is not
active, set the active flag **without recording a Technique pick**.

The existing `formalizing = tech_def.magic_granting and choice == self.magic_domain` branch must not fire
for a lineage-source domain that is already active — it would try to consume a pick to re-formalize a
gift that has already arrived. This is the one genuinely delicate edit in the workstream and it gets its
own task and its own regression test.

The Technique economy is untouched: no pick is spent, and a three-pick career is still three picks.

### M5 — The chapter and its amendments

New `player_handbook/II.5_Lineage.md`: *Reading the Entries — Lineages* (Name / Description / Gift /
Heritage, never printed empty) · the Human entry · the *Why the core lineage is empty* Through-the-Mirror
box · *The Gift is a domain* (birth not study; one domain at creation; Minor scope until it formalizes) ·
*Formalization* with the *Why blood formalizes for free* box · *Creating a custom lineage* (MM-labelled,
five steps) ending on the standing warning that a lineage is not a stat bonus.

Amendments, one sentence each, same commit: II.1 *The Six Steps* → *The Seven Steps* with Lineage at step
3 and the Zulnut example line · II.3 *Acquiring a Domain* third origin + *Before the Technique* exception
pointer · II.4 *Techniques* the free-formalization sentence · II.6 Backgrounds' one-domain rule in *Magic
and Backgrounds* · Quick Start one line under step 2 · MM3 a paragraph pointing MMs at the custom-lineage
steps and the setting-Facet pitch format · Glossary: Lineage, Gift, Heritage · Character sheet appendix:
a Lineage line under Background · `references/phb-examples.md`: the cast is human and the step is one
word for them.

**Heritage is not a second Specialty in the arithmetic.** It draws from the same one-step allowance;
III.1 *Difficulty* already says "anything future" and needs no change, but the Heritage paragraph must
say it out loud.

### M6 — API and app

Creation request model gains `lineage` (default `"human"`) and `gifted` (default `false`); the WS
`create_character` path validates through the character model so no rule logic lives in the handler.
Session-state payload serializes lineages beside backgrounds. The builder gains a Lineage picker between
Facet and attributes, **hidden when the merged ruleset holds only `human`**, so a Shattered Origin table
never sees a one-option choice. One task.

## 3. Testing strategy

TDD; three tests per public function.

- **Schema:** loads; rejects a gift domain that does not exist (INV-16); `playable` defaults true.
- **Merge:** a second module adds a lineage; a collision replaces by id; `human` survives.
- **Character:** default lineage on old files; gifted creation sets the domain and skips the secondary;
  gifted + domain-granting Background rejected; ungifted member of a gifted lineage keeps the secondary
  and holds no domain; formalization fires on the first Facet level with **no pick consumed**; the
  `formalizes_on: technique` path leaves the old behaviour intact.
- **Docs:** INV-4/5/9/10 after the renumber; INV-2 for the new sheet line; INV-12 for the three glossary
  terms; INV-16 new.
- **Regression:** every `.fof` under `characters/` and `playtest/` loads unchanged.

## 4. Risks and mitigations

- **The renumber lands with content in the diff.** Mitigation: M1 is its own commit and its own PR-sized
  review; a reviewer must be able to read it as a pure rename.
- **Gift becomes a stat.** The custom-lineage guidance's closing warning is load-bearing; it exists to
  stop the first homebrew lineage from adding +1 Constitution.
- **The formalization branch double-fires.** M4's regression test is the guard.
- **Old character files.** The loader must not require `lineage`; tested explicitly.
- **The Bestiary stays setting-agnostic (B9).** Nothing in it references lineage, and nothing in this
  workstream touches it.

## 5. Open questions

None blocking. The one rule the brief left to the owner (formalization) is ruled: option 1, D18.
