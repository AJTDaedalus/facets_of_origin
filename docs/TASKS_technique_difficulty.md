# TASKS — Technique difficulty, domain pricing, and licensed overrides

**Design:** `docs/DESIGN_technique_difficulty.md`. **Ruling:** `docs/DECISIONS.md` B4.
**Brief:** `docs/BRIEF_technique_difficulty.md`.

Worker protocol: pick **one** task, open only the files it names, write the test
first, run it red, implement, run it green, run the full suite, update this file
and append to `docs/LOG_technique_difficulty.md`, then **stop and report**.

Every task below is self-contained. Do not rely on chat history.

---

## Q2 — pricing and the wording defect *(do first: independent, closes a live defect)*

### TD-1 — Pin the two domain grant routes

**Files:** `software/tests/test_ascendant_domain.py` (add), read-only:
`software/app/game/character.py:406–410`, `software/app/game/engine.py:330–338`.

**Do:** add three tests pinning B4 Q2 as canon.

1. Ascendant Domain's prismatic territory resolves on the **Broad** table with **no**
   additional step, at all three scopes.
2. A Second Domain grant resolves on **its own domain type's** table, one step harder.
3. **The Focused-primary case**: a character whose primary domain is Focused and whose
   Second Domain grant is Standard prices at *Standard-plus-one-step*, not at
   *Focused-plus-one-step*. This is the case the old wording broke.

**Acceptance:** all three pass against the **current** engine without engine changes.
If any fails, the engine does not implement B4 Q2 — stop and escalate to Planner;
do not "fix" the engine to match the test.

---

### TD-2 — Re-anchor the Second Domain wording on five surfaces

**Files:** `player_handbook/II.4b_Character_Creation_Facet_Mind.md`,
`player_handbook/II.4c_Character_Creation_Facet_Soul.md`,
`software/facets/base/facet.yaml` (`second_domain_mind.roll`, `second_domain.roll`),
`mm_manual/MM5_Quick_Reference.md`.

**Do:** replace "one difficulty step harder **than your primary domain**" with
"one difficulty step harder **than normal for that domain**" everywhere it appears —
body prose, both `roll:` strings, and the MM5 compression. **One commit, all five.**

Do not touch the `Normal:` fields; they already read correctly.

**Acceptance:** TD-1 still green. `grep -rn "harder than your primary domain"`
returns nothing across `player_handbook/`, `mm_manual/`, and `facet.yaml`. INV-6
(MM5 typographic dashes) and INV-14 (Technique headers vs facet.yaml) still pass.

**Test:** add to `software/tests/test_docs_consistency.py` — no book or `facet.yaml`
surface contains the old anchoring. This is the regression guard; the string is
short and will otherwise creep back in a copy-paste.

---

### TD-3 — Record the Q2 defect as closed

**Files:** `docs/LOG_technique_difficulty.md` (create).

**Do:** open the log with the Q2 entry — what the defect was, why it was invisible
(it only bites Focused-primary casters), the five surfaces, and the tests that now
pin it.

**Acceptance:** log exists and names TD-1's three tests by function name.

---

## Q1 — the composition mechanism

### TD-4 — Schema: `difficulty_step` and `step_trigger`

**Files:** `software/app/facets/schema.py` (`TechniqueDef`, line ~86),
`software/tests/test_facet_schema.py`.

**Do:** add two optional fields, documented in the class docstring in the existing
style:

- `difficulty_step: Literal["easier", "harder"] | None = None`
- `step_trigger: StepTriggerDef | None = None`, where `StepTriggerDef` is a new
  model: `kind: Literal["auto", "declared"]`, `match: str | None`,
  `against: str | None` (`"choice"` or a literal value).

Both optional, so every existing Technique parses unchanged.

**Acceptance:** `facet.yaml` loads with no change to it. Three tests: a Technique
with no step parses; one with an auto trigger parses; an invalid `kind` raises.

---

### TD-5 — The composition rule in `combat.py`

**Files:** `software/app/game/combat.py`, `software/tests/test_combat.py`.

**Do:** add `apply_character_difficulty_step(declared_label, character, context,
ruleset) -> tuple[str, str | None]` per DESIGN §2.2.

- Declared label first, character step second, ladder clamps via the existing
  `_engine._step_difficulty_easier` / `_harder`.
- **At most one** character-side step per roll.
- Precedence when several qualify: player-declared beats auto, then lowest
  technique id.
- Only Techniques the character has actually unlocked are eligible.
- Returns the final label and the technique id that moved it (or `None`).

**This is the rule's only home.** It must not be duplicated in `websocket.py` or in
the simulator (`CLAUDE.md` iron law).

**Acceptance — write these tests first**, they are DESIGN §5's list:
clamping from Easy; two qualifying Techniques yield one step and a deterministic id;
unlocked-only; absent context field does not fire; mismatched choice does not fire;
Hard + step → Standard; declared beats auto.

---

### TD-6 — Populate the step metadata in `facet.yaml`

**Files:** `software/facets/base/facet.yaml`, `software/tests/test_facet_schema.py`.

**Do:** add `difficulty_step` and `step_trigger` to exactly five Techniques, per
DESIGN §2.3: `weapon_mastery`, `acclimated`, `field_of_mastery` (auto, match against
`choice`), `steady_hand` (auto, `skill_id` against literal `finesse`),
`the_uncanny_angle` (declared).

**Do not** add them to `pressure_point` — it is deferred (DESIGN §2.5).

**Acceptance:** exactly five Techniques carry `difficulty_step`. INV-14 passes. A
test asserts the count is five and names them, so a sixth cannot be added without
a deliberate test change.

---

### TD-7 — Carry `weapon_category` on the Strike

**Files:** `software/app/api/websocket.py` (strike handler, ~585),
`software/app/static/js/play.js` (~1072), `software/app/static/index.html`,
`software/tests/test_websocket.py`.

**Do:** add an optional `weapon_category` to the strike message, one of the five
IV.1 categories (`heavy`, `standard`, `light`, `ranged`, `unarmed`). Add a picker in
the strike UI.

**Take the side benefit** (DESIGN §2.4): IV.1 says category sets the Strike
attribute, so the picker should drive the attribute selection — heavy → Strength,
light/ranged → Dexterity, standard/unarmed → player's choice of Strength or
Dexterity. Do **not** restrict what the client may send: INV-8 says the books may
not restrict a Strike pairing the engine permits, and the same applies here. The
picker is a default, not a gate.

**Acceptance:** a strike with no `weapon_category` behaves exactly as today.
Three tests: absent field is accepted; a valid category round-trips; an unknown
category is rejected with an error message rather than silently ignored.

---

### TD-8 — Carry `hazard_type` and `knowledge_field` on generic rolls

**Files:** `software/app/api/websocket.py` (generic roll handler, ~275/310),
`software/app/static/js/play.js`, `software/tests/test_websocket.py`.

**Do:** add two optional strings to the roll message. Both absent by default; an
absent field means the corresponding auto trigger does not fire.

**Acceptance:** existing roll messages are unaffected. Two tests: absent fields
accepted; values round-trip into the roll context.

---

### TD-9 — Wire the three handlers

**Files:** `software/app/api/websocket.py` (strike ~585, generic roll ~275/310,
reaction ~1111), `software/tests/test_websocket.py`.

**Do:** in each of the three handlers, after the difficulty label is known and
**before** `RollRequest` is built, call `apply_character_difficulty_step` and use the
returned label. Carry the returned technique id through to the broadcast payload.

Do **not** wire the magic handler (~950) — DESIGN §2.6.

**Acceptance:** three tests, one per handler: a qualifying Technique steps the label;
a non-qualifying one does not; the applied technique id appears in the payload.
A fourth test asserts the magic handler is unaffected.

---

### TD-10 — Show both moves in the roll banner

**Files:** `software/app/static/js/play.js`, `software/app/static/js/components.js`,
`software/tests/e2e/test_ui_flows.py`.

**Do:** when a payload carries an applied technique id, the banner reads
`Hard (MM) → Standard (Weapon Mastery)`. When it does not, the banner is unchanged.

This is required, not polish (DESIGN §2.7): auto-apply is only acceptable because
the step is visible.

**Acceptance:** an e2e test asserting both moves render when a Technique applies,
and that an ordinary roll's banner is unchanged.

---

### TD-11 — Legislate Q1 in III.1, compress everywhere else

**Files:** `player_handbook/III.1_Core_Resolution.md` (*Difficulty*),
`player_handbook/III.3_Combat.md` (Strike difficulty note),
`mm_manual/MM5_Quick_Reference.md`, `mm_manual/MM2_Session_Design.md`.

**Do:** one legislative paragraph in III.1 *Difficulty* — the MM's call first, the
character's step second, ladder clamps, at most one character-side step per roll.
Every other surface **compresses** it; none restates it (quick-refs iron law).

MM2 gets the guardrail note from DESIGN §2.5: an MM applying *Pressure Point* by
hand must not also let a Technique step the same roll.

**Acceptance:** INV-9 through INV-14 pass. `docs`-consistency stays green. No surface
other than III.1 states the rule in full.

---

## Q3 — the licensed override

### TD-12 — Schema and data for the override flag

**Files:** `software/app/facets/schema.py`, `software/facets/base/facet.yaml`,
`software/tests/test_facet_schema.py`.

**Do:** add `removes_target_from_conflict: bool = False` to `TechniqueDef`; set it
true for `the_final_blow` and nothing else.

**Acceptance:** a test asserts exactly one Technique in `facet.yaml` carries the
flag, and names it. Overrides must stay greppable and countable.

---

### TD-13 — Resolve the removal as a defeat event

**Files:** `software/app/game/combat.py`, `software/tests/test_combat.py`.

**Do:** a function that resolves a Final Blow removal through the **canonical defeat
path**, never a raw `resolve_current` write.

**P11 invariant:** every `resolve_current` mutation routes through `phase_crossed`.
The removal must be distinguishable in the transcript from an ordinary defeat so a
future sim series can count capstone removals.

**Escalate rather than decide** if this requires changing the defeat path's
signature (DESIGN §7.2).

**Acceptance:** three tests — removal produces a defeat event; it routes through
`phase_crossed`; the transcript entry is distinguishable from a Resolve-0 defeat.
A fourth asserts no code path writes `resolve_current = 0` directly for this case.

---

### TD-14 — Wire Final Blow through the strike handler

**Files:** `software/app/api/websocket.py`, `software/app/static/js/play.js`,
`software/tests/test_websocket.py`.

**Do:** the player declares Final Blow with their Strike. Spark spent, Combat roll
resolved; **on 7+** the removal is offered. **MM confirmation is required** before it
commits — auto-apply governs difficulty steps, not actor removal.

Frequency uses the existing `Character.techniques_used_this_session`. No new field.

**Acceptance:** four tests — fires on 10+; fires on 7–9; does not fire on 6−;
a second use in the same session is refused. One more: the removal does not commit
without MM confirmation.

---

### TD-15 — Q3 prose

**Files:** `player_handbook/II.4a_Character_Creation_Facet_Body.md`,
`mm_manual/MM1_Encounters_and_Enemies.md`.

**Do:** one precision sentence in the *Final Blow* entry — "succeed" means 7+, and
on a 7–9 the partial's cost shapes the aftermath, never the removal itself. Then
check the entry's `Normal:` field still reads true.

MM1 gains the encounter-design note: build Bosses so an early exit is a win, not a
broken script — phase material is forfeit the moment a capstone lands.

**III.3 changes not at all.** That is the ruling.

**Acceptance:** INV-14 passes. `grep` confirms III.3's "riders never defeat"
sentence is byte-identical to before this cycle.

---

## Shared

### TD-16 — The MM1 calibration sentence

**Files:** `mm_manual/MM1_Encounters_and_Enemies.md`.

**Do:** one advisory sentence near the Recipe Table: the recipes are calibrated for
baseline parties, and a party fielding step-easier Strike Techniques or a Tier 3
capstone runs about a band hot.

**Advisory prose only.** Do **not** change the Recipe Table, and do **not** re-run
Series 7 or 9 — B4 established the corpus is intact. An optional Series 10 to
quantify "a band hot" is sanctioned but nothing gates on it.

**Acceptance:** the table's numbers are unchanged; INV-9 passes.

---

### TD-17 — Record the *Pressure Point* deferral

**Files:** `docs/TODO.md`.

**Do:** add an item in the file's existing format — what is deferred, why (it is
party-wide scene state, not roll-time metadata), what happens meanwhile (the MM
applies it by lowering the label), and what "done" looks like (a scene-effect store
plus the guardrail counting it as the one character-side step).

**Acceptance:** entry follows the file's what's-wrong / why-deferred / done-when shape.

---

## Amendment — the two weapon vocabularies *(added 2026-08-02, DESIGN §8)*

### TD-18 — Add `weapon_type` and retarget *Weapon Mastery*

**Files:** `software/app/api/websocket.py` (strike handler),
`software/facets/base/facet.yaml` (`weapon_mastery.step_trigger`, and a
`equipment.weapon_types` list), `software/app/static/js/play.js`,
`software/app/static/index.html`, `software/tests/test_websocket.py`.

**Do:** add an optional `weapon_type` (`blades`, `blunt`, `polearms`, `unarmed`) to
the strike message and a picker beside the existing category picker. Retarget
`weapon_mastery.step_trigger.match` from `weapon_category` to `weapon_type`.

`weapon_category` keeps its TD-7 job — defaulting the attribute — and is **not**
removed. The two axes are orthogonal (DESIGN §8).

**Acceptance:** a strike with neither field behaves exactly as today. Four tests:
Weapon Mastery (blades) + `weapon_type: "blades"` fires; + `weapon_type: "blunt"`
does not; absent `weapon_type` does not; `weapon_category` alone does **not** fire
Weapon Mastery, proving the axes are separate. Plus one regression test asserting
the III.3:513 case — Mordai, Weapon Mastery (blades), Standard → Easy — now works
end to end, since that is the case B4 cites and the escalation found broken.

---

### TD-19 — Enumerate non-domain Technique choices as data

**Files:** `software/app/facets/schema.py` (`TechniqueDef`),
`software/facets/base/facet.yaml`, `software/tests/test_facets_schema.py`.

**Do:** add `choices: list[str] | None = None` to `TechniqueDef`. Populate it for
`weapon_mastery` (blades/blunt/polearms/unarmed), `acclimated` (extreme cold/extreme
heat/altitude/deprivation), and `field_of_mastery` (the II.4a list, which is
open-ended — mark it as suggestions, not a closed set).

`choice_prompt` stays as the human-readable label; `choices` is the machine-readable
option list. Optional, so every other Technique parses unchanged.

**Acceptance:** three tests — the three Techniques carry `choices`; a Technique
without `choices` parses; the values match the printed `choice_prompt` text so book
and data cannot drift. INV-14 passes.

---

### TD-20 — Render a picker for non-domain choices

**Files:** `software/app/static/js/builder.js` (`pickTechniqueChoice`),
`software/tests/e2e/test_ui_flows.py`.

**Do:** `pickTechniqueChoice` currently builds **only** domain lists, so
`weapon_mastery`, `acclimated`, and `field_of_mastery` offer an empty option set and
their choices cannot be made at all. Fall back to `def.choices` when the Technique
is not domain-granting. For `field_of_mastery`, whose list is open-ended, allow a
free-text entry alongside the suggestions.

**Acceptance:** an e2e test selecting Weapon Mastery and choosing "blades", then
asserting `technique_choices["weapon_mastery"] == "blades"` on the character. Domain
Techniques keep their existing behaviour — one test proving that.

---

## Progress

| Task | Status |
|---|---|
| TD-1 … TD-3 (Q2) | done — see `docs/LOG_technique_difficulty.md` |
| TD-4 … TD-6 (Q1 core) | done — see `docs/LOG_technique_difficulty.md` |
| TD-7 … TD-11 (Q1 wiring/prose) | done — see `docs/LOG_technique_difficulty.md`; escalation resolved by DESIGN §8, see TD-18…TD-20 |
| TD-12 … TD-15 (Q3) | done — see `docs/LOG_technique_difficulty.md` |
| TD-16, TD-17 (shared) | done — see `docs/LOG_technique_difficulty.md` |
| TD-18 … TD-20 (DESIGN §8 amendment) | done — see `docs/LOG_technique_difficulty.md` |

**Cycle complete.** All of TD-1 through TD-20 are done. Q1, Q2, and Q3 (B4) are
fully implemented, tested, and documented.
