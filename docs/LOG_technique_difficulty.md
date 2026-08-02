# LOG — Technique difficulty, domain pricing, and licensed overrides

**Tier:** Worker (Sonnet) execution log
**Design:** `docs/DESIGN_technique_difficulty.md` · **Tasks:** `docs/TASKS_technique_difficulty.md`
**Ruling:** `docs/DECISIONS.md` B4

---

## Q2 — pricing and the wording defect (TD-1, TD-2, TD-3)

**Date:** 2026-08-02
**Scope:** the Q2 block only, per assignment — TD-1 through TD-3. TD-4 onward (Q1's
composition mechanism, Q3's licensed override) are untouched by this pass.

### The defect

*Second Domain* (Soul Communion Tier 3, and Mind Archive Tier 3's mirror) read "one
difficulty step harder **than your primary domain**" across five surfaces. Read
literally, this anchors the penalty to the *caster's other domain's table*, not to
the *granted domain's own table*. For a Standard- or Broad-primary caster these
usually coincide, which is exactly why the defect went unnoticed. It only bites a
**Focused-primary caster**: Focused's table is Easy/Standard/Hard; stepping *that*
table one notch from its minor-scope value (Easy) lands on Standard — which is the
granted domain's own *unstepped* minor value if the grant is a Standard-type domain.
The penalty silently evaporates.

B4 ruled the correct anchor is "one difficulty step harder **than normal for that
domain**" — the grant's own domain-type table, stepped once. B4 also established
that `character.py:406–410` and `engine.py:330–338` already implement this correctly;
only the prose (and one `roll:`/`description:` pair per Facet in `facet.yaml`) said
the wrong thing.

### TD-1 — Pin the two domain grant routes

Added three tests to `software/tests/test_ascendant_domain.py`, all passing against
the **unmodified engine** — no engine changes were made, per the task's explicit
trap-avoidance instruction. This confirms B4's premise: the engine already
implements Q2 correctly, and only the wording needed fixing.

- `test_b4q2_ascendant_domain_prices_off_broad_table_no_step` (parametrized over
  minor/significant/major) — Ascendant Domain's prismatic territory (Chronomancy,
  Broad) resolves to Hard / Very Hard / Very Hard at all three scopes, with no
  extra character-side step layered on top of the Broad table.
- `test_b4q2_second_domain_prices_off_own_table_one_step_harder` — a Focused-primary
  Soul mage (Fire) taking Second Domain (Storm, Standard) resolves Storm/minor to
  Hard — Standard's own minor value (Standard) stepped once, not Fire's Focused
  table stepped once (which would give Standard, not Hard).
- `test_b4q2_second_domain_focused_primary_does_not_leak_into_pricing` — the case
  the retired wording broke, made explicit: a Focused-primary Mind mage
  (Inscription) taking Second Domain (Illusion, Standard) resolves Illusion/minor
  to **Hard**, and the test explicitly asserts it is *not* **Standard** — the value
  the literal "harder than your primary domain" reading would have produced
  (Focused-minor = Easy, stepped once = Standard).

All three ran green on the first pass; no escalation was needed.

Ran `pytest tests/test_ascendant_domain.py -q` afterward: 45 passed (42 pre-existing
+ 3 new — the file already carried adjacent coverage for the Broad table and the
one-step tax individually; these three are the dedicated B4 Q2 pin naming the
defect explicitly, including the previously-uncovered Focused-primary contrast).

### TD-2 — Re-anchor the Second Domain wording on five surfaces

One pass, all five surfaces, matching string replaced everywhere it appeared
(`"harder than your primary domain"` → `"harder than normal for that domain"`):

1. `player_handbook/II.4b_Character_Creation_Facet_Mind.md` — the `**Roll:**` line
   and the body-prose sentence for *Second Domain* (Archive, Tier 3).
2. `player_handbook/II.4c_Character_Creation_Facet_Soul.md` — same two spots for
   *Second Domain* (Communion, Tier 3).
3. `software/facets/base/facet.yaml` — `second_domain_mind`'s `description` and
   `roll` fields.
4. `software/facets/base/facet.yaml` — `second_domain`'s `description` and `roll`
   fields (the task named only the two `roll:` strings explicitly, but the
   `description:` prose carried the identical defect and was fixed in the same
   pass — the acceptance grep is on the string, not the field name, and a
   `description:` left unfixed would still fail it).
5. `mm_manual/MM5_Quick_Reference.md` — the Second Domain compression line. This one
   didn't carry the *exact* retired phrase ("...harder than **the primary**", not
   "...your primary domain") but stated the same wrong anchor and was re-anchored
   to match.

`Normal:` fields were not touched, per the task — they already read correctly.

**Regression test added:** `test_second_domain_wording_does_not_anchor_on_primary_domain`
in `software/tests/test_docs_consistency.py`, scanning every book file plus
`facet.yaml` for the retired string.

**Verification:**
- `grep -rn "harder than your primary domain" player_handbook/ mm_manual/ software/facets/base/facet.yaml`
  → no matches (the only remaining repo-wide hit is the task file itself, quoting
  the grep command).
- `pytest tests/test_docs_consistency.py -q` → 31 passed, including INV-6
  (`test_mm5_uses_typographic_dashes`) and INV-14 (`test_every_technique_has_use_and_normal_in_facet_yaml`,
  `test_every_technique_entry_states_branch_tier_and_attribute`,
  `test_technique_headers_match_facet_yaml`, `test_every_technique_entry_carries_a_normal_line`).
- `pytest tests/test_ascendant_domain.py -k b4q2 -v` → still 5 passed after the
  prose edits (TD-1's pin is unaffected by a wording-only change, as expected).

One incidental bug caught and fixed during this task: my first edit to
`test_docs_consistency.py` appended the new test function in a way that orphaned
the previous test's trailing `assert not problems, ...` line outside its own
function body (a `NameError: name 'problems' is not defined` inside the *new*
test). Caught immediately by running the suite before moving on; fixed by moving
the assert back into `test_every_bestiary_creature_has_a_lore_box`, its rightful
owner. Not a design defect — a self-inflicted edit-tool slip, corrected before
this log entry was written.

### TD-3 — this entry

Log created. Q2 tests named above: `test_b4q2_ascendant_domain_prices_off_broad_table_no_step`,
`test_b4q2_second_domain_prices_off_own_table_one_step_harder`,
`test_b4q2_second_domain_focused_primary_does_not_leak_into_pricing`.

### Status

TD-1, TD-2, TD-3 done. TD-4 (Q1 schema work) and beyond are **not started** —
out of scope for this assignment. `docs/TASKS_technique_difficulty.md`'s progress
table updated accordingly.

Full suite run from `software/`: **`python3 -m pytest -q`** — see the parent
session's report for the final pass/fail count (this log was written before that
run completed; the count is not fabricated here).

---

## Q1 wiring — TD-7 through TD-11

**Date:** 2026-08-02
**Scope:** TD-7 (weapon_category on the Strike), TD-8 (hazard_type/knowledge_field
on the generic roll), TD-9 (wire the three handlers to
`combat.apply_character_difficulty_step`), TD-10 (the roll banner), TD-11
(III.1 legislation + III.3/MM5/MM2 compression). TD-4–TD-6 (schema, the
composition function, the five Techniques' metadata) were already done —
built on, not redone. TD-12 and later (Q3, the licensed override) were not
started, per assignment boundary.

### TD-7 — `weapon_category` on the Strike

`software/app/api/websocket.py::_handle_strike` accepts an optional
`weapon_category` string. If present it is validated against
`session.ruleset.equipment.weapon_categories` (the IV.1:13-19 reference table
already in `facet.yaml` from an earlier, unrelated sync task — `EquipmentDef`,
sync-M-12) and rejected with an error message if unrecognised; if absent the
field is simply `None` downstream and nothing about the roll changes. Per
INV-8 and the task's explicit instruction, this validation is against the
five-category *vocabulary*, never against the attribute/skill pairing the
client sends — the docstring on the validation block says so explicitly, and
`test_strike_with_dexterity_attribute` / `test_strike_with_intelligence`
(pre-existing) still pass unmodified, proving no new gate reached the
attribute check.

Client side (`index.html`, `play.js`): a `#strike-weapon-category` select
listing the five IV.1 categories, wired to a new `onStrikeWeaponCategoryChange()`
that reads `state.ruleset.equipment.weapon_categories[category].attributes[0]`
and sets `#strike-attribute` — the *default*, never a lock; the player can
still change the attribute select afterward, and the server never checks that
the two agree. This reads the attribute mapping from the ruleset at runtime
rather than hardcoding a second copy of IV.1's table in JS.

**Tests** (`software/tests/test_websocket.py`, class `TestCombatGameplayLoop`):
`test_strike_without_weapon_category_behaves_as_today`,
`test_strike_with_valid_weapon_category_round_trips`,
`test_strike_with_unknown_weapon_category_returns_error`.

### TD-8 — `hazard_type` / `knowledge_field` on the generic roll

`_handle_roll` accepts both as optional strings, folded into the same
composition context as `skill_id`. Absent means the corresponding auto
trigger cannot fire — no error, no behaviour change from today.

Client side: two optional text inputs on the Roll Dice card
(`#play-roll-hazard-type`, `#play-roll-knowledge-field`), sent as `null` when
blank. Added because without *some* way to set these, Acclimated and Field of
Mastery could never fire outside a Strike — DESIGN §2.4 says they are "set by
the MM or player when relevant," which presupposes a place to set them. Kept
as free-text rather than a fixed dropdown because Acclimated's and Field of
Mastery's `technique_choices` values are themselves free text chosen at
Technique-select time (see the Escalation below for why that choice path is
itself broken today).

**Tests:** `test_roll_without_hazard_or_knowledge_field_behaves_as_today`,
`test_roll_hazard_type_and_knowledge_field_round_trip_without_error` (class
`TestWebSocketRoll`).

### TD-9 — wiring the three handlers

Added one shared wrapper, `_apply_difficulty_step(character, declared_difficulty,
context, ruleset)`, in `websocket.py` — it calls
`combat_module.apply_character_difficulty_step` (never re-derives a step) and
only adds a display-name lookup so the broadcast payload can carry
`{technique_id, technique_name, from, to}` for the banner. All three handlers
call it after the declared label is known and before `RollRequest` is built,
per DESIGN §2.6:

- **Strike** (`_handle_strike`): context = `{skill_id, weapon_category,
  declared_technique_ids}`.
- **Generic roll** (`_handle_roll`): context = `{skill_id, hazard_type,
  knowledge_field, declared_technique_ids}`.
- **Reaction** (`_handle_react`): only Dodge/Parry roll at all; context =
  `{skill_id, declared_technique_ids}` (`skill_id` is `"combat"` for Parry,
  `None` for Dodge — Steady Hand's `skill_id == "finesse"` trigger structurally
  cannot fire on either, which is correct: reactions aren't Finesse checks).
  Absorb/Intercept never build a `RollRequest`, so `technique_step` is simply
  `None` on their payload — the key is always present so the client never has
  to special-case a missing key.

The **magic handler is untouched** — confirmed by
`test_cast_ignores_a_technique_that_would_fire_on_a_strike`, which gives the
character an unlocked, matching-context Technique and asserts `cast_result`
carries no `technique_step` key at all.

**Tests:** `test_strike_weapon_mastery_steps_difficulty_when_matched`,
`test_strike_weapon_mastery_does_not_fire_on_mismatch`,
`test_roll_acclimated_steps_difficulty_when_hazard_matches`,
`test_roll_field_of_mastery_does_not_fire_on_mismatched_field`,
`test_react_declared_technique_steps_difficulty`,
`test_react_technique_not_toggled_does_not_fire`,
`test_react_absorb_carries_no_technique_step_key`,
`test_cast_ignores_a_technique_that_would_fire_on_a_strike`.

### TD-10 — the roll banner

Broadcast payloads (`roll_result`, `strike_result`, `react_result`) all carry
a `technique_step` key — `None` when nothing fired, otherwise `{technique_id,
technique_name, from, to}`. `buildRollResultHtml` (`play.js`, shared by Roll
and Strike results) renders a line reading `Hard (MM) → Standard (Weapon
Mastery)` when `msg.technique_step` is present and renders nothing otherwise;
`onReactResult` appends the same two moves to its chat line, since reactions
have no result-box banner to hang it on. `onStrikeResult` had to be updated
to actually forward `technique_step` into the object it hands to
`showRollResultBox` — it builds a fresh `{player, character_name}` object
rather than passing the whole `msg` through, and that reconstruction would
silently have dropped the field.

e2e tests use the same direct-`onStrikeResult`-injection pattern already
established by `test_a_strike_on_a_tracked_enemy_can_be_applied_from_the_prompt`
(pre-existing) rather than driving a full Technique-grant round trip through
the advancement UI — that flow requires reaching a Facet-level threshold
(5 rank advances) which is impractical to stage in a browser test, and this
suite already has a precedent for testing pure client-rendering behaviour by
calling the handler function directly with a synthetic payload.

**Tests** (`software/tests/e2e/test_ui_flows.py`, class `TestCombatLoop`):
`test_technique_step_banner_shows_both_moves`,
`test_ordinary_strike_banner_has_no_technique_step`.

### TD-11 — prose

- **III.1 *Difficulty*** (the legislative home): one new paragraph after "The
  MM declares difficulty before you roll," stating the fixed order (MM's call,
  then at most one character-side step, then the ladder clamps) and the
  auto/declared split, without naming implementation details (no "banner," no
  "context dict" — "the roll result names it").
- **III.3** *Strike*: one compressing sentence appended to the existing
  difficulty paragraph — "A Technique may then move the MM's call one step
  further, exactly as any roll's difficulty can (see *Difficulty*, III.1)."
  The Weapon Mastery vignette (III.3:513, "Standard difficulty, but Weapon
  Mastery makes this one step easier, so Easy") and the "riders never defeat"
  sentence are both untouched — verified by not editing those lines and by
  the full suite staying green.
- **MM5**: one line under the Difficulty table, matching the manual's existing
  "compressed from X — see X for full text" register without literally using
  that phrase (short enough not to need it): "A Technique may then move your
  call one step further — at most one per roll, auto-applied when its trigger
  is data the app already holds, player-declared otherwise (see *Difficulty*,
  III.1)."
- **MM2**: new `### Difficulty and Technique Steps` subsection under
  *Pacing Toolkit*, plus the DESIGN §2.5 guardrail as an **MM Note** box
  ("Pressure Point does not stack with an auto-applied step") — the exact
  point-of-the-MM's-call documentation DESIGN said was "a task, not a
  nice-to-have."

INV-9 through INV-14 all pass. `Index.md`, `List_of_Tables.md`,
`List_of_Boxes.md` were regenerated (`python -m tools.build_index` then
`python -m tools.build_table_register` then `build_index` again — the first
`build_index` pass runs before the table/box registers reflect the new MM2
box and briefly disagrees with itself; a second pass after
`build_table_register` is required for both to agree, and is worth flagging
for anyone who hits the same false failure) and are part of this commit's
changes, not hand-edited.

### Test count

15 new tests: 3 (TD-7) + 2 (TD-8) + 8 (TD-9, includes the strike/roll cases
that also serve TD-7/TD-8's "values reach the composition context" proof) +
2 (TD-10, e2e). `python3 -m pytest -q` from `software/`: **1340 passed**
(1325 baseline + 15), zero failures, zero skips beyond the suite's existing
Playwright-conditional skip guard. Ran in the foreground, ~4m52s.

## ESCALATION — Weapon Mastery's own choice vocabulary cannot fire through `weapon_category`

**What was attempted:** TD-7 as specified — `weapon_category` on the wire is
one of IV.1's five mechanical categories (`heavy`, `standard`, `light`,
`ranged`, `unarmed`), sourced from `ruleset.equipment.weapon_categories`,
matching DESIGN §2.4 ("sourced from a picker in the strike UI listing the
five IV.1 categories") and TD-7's literal instruction.

**What is wrong:** *Weapon Mastery*'s own `choice_prompt` — both in
`facet.yaml` and in `player_handbook/II.4a_Character_Creation_Facet_Body.md:53`
("Choose: A weapon type: blades, blunt, polearms, or unarmed.") — uses a
**different, fictional taxonomy**, not IV.1's mechanical one. TD-6's
`step_trigger` for `weapon_mastery` is `{match: weapon_category, against:
choice}`, meaning it compares the wire's `weapon_category` against whatever
string the player recorded in `technique_choices["weapon_mastery"]` at
selection time — which, per the existing choice prompt, is one of `blades`,
`blunt`, `polearms`, `unarmed`. Only `unarmed` overlaps with IV.1's five
categories (`heavy`, `standard`, `light`, `ranged`, `unarmed`). A character
who takes Weapon Mastery in blades, blunt, or polearms — three of the four
choices — can **never** have it auto-fire, because a Strike's `weapon_category`
will never equal `"blades"`.

This is not a hypothetical edge case. It breaks the canonical example B4
itself cites as ratifying Q1: III.3:513 — *"Mordai: 'I want to test it... I
have Weapon Mastery in blades.' MM: 'Standard difficulty, but Weapon Mastery
makes this one step easier, so Easy.'"* Under this cycle's implementation,
Mordai's Strike would carry `weapon_category` in {`heavy`, `standard`,
`light`, `ranged`, `unarmed`} (whatever the dagger/sword/etc. he is actually
using resolves to under IV.1), which never equals his recorded choice
`"blades"` — the auto-apply would silently **not fire**, and the MM would
have to apply the step by hand, exactly as before B4. The two taxonomies are
not just differently spelled — they are orthogonal: a greatsword is
simultaneously `heavy` (IV.1, attribute-setting) and a `blade` (Weapon
Mastery's own vocabulary), so there is no simple rename that reconciles them;
a "blade" specialist should arguably fire regardless of whether the specific
blade in hand is Light (dagger) or Heavy (greatsword).

**A second, compounding defect found while investigating the first:**
`builder.js::pickTechniqueChoice` — the only client code that prompts for a
Technique's `choice` when `has_choice` is true — **only knows how to offer
magic domain lists** (`magic.mind_domains` / `magic.soul_domains`). For a
non-domain `has_choice` Technique like Weapon Mastery, Acclimated, or Field of
Mastery, it computes `facetForDomains = def.requires_domain ||
state.character.primary_facet` and offers that Facet's *domain list* as the
"choices" — a Body-Facet character selecting Weapon Mastery would be shown
Soul domain names (Storm, Fire, ...) as candidate weapon types. This means
there is currently **no working choice picker at all** for any of the three
Techniques this cycle's auto-apply exists to serve, independent of which
vocabulary `weapon_category` uses.

**Why this was not silently fixed:** reconciling the two taxonomies is a
content/architecture decision, not a wiring bug — plausible directions
include (a) migrating Weapon Mastery's `choice_prompt` to IV.1's five
categories, which breaks the existing II.4a text and the III.3:513 vignette
and needs re-writing both; (b) keeping Weapon Mastery's own vocabulary and
adding a second reference table mapping weapon-family choices to the set of
IV.1 categories they can appear as, so the trigger checks membership rather
than equality; (c) something else. Any of these is a Planner-level call, and
TD-7's files list (`websocket.py`, `play.js`, `index.html`,
`test_websocket.py`) does not include `II.4a`, `builder.js`, or a new
reference table — inventing a fix here would be scope creep past what TD-7
asked for and would very likely collide with a decision Planner should make
deliberately.

**What ships regardless:** the composition mechanism (`combat.py`,
already-done TD-5) is generic and correct — it was tested with `weapon_category:
"blades"` directly in `test_combat.py` before this pass, and this pass's
websocket tests use compatible values (`"light"`/`"light"`) precisely to
route around this defect rather than depend on it being fixed. TD-7 through
TD-11 are complete and tested as specified; only Weapon Mastery's *real-play*
auto-fire rate is affected (3 of its 4 choices), and only once
`pickTechniqueChoice` is also fixed does a player have any way to make that
choice through the UI at all today, auto-apply or not.

**The specific question for Planner:** how should Weapon Mastery's
`choice_prompt` vocabulary (`blades`/`blunt`/`polearms`/`unarmed`) relate to
`weapon_category`'s vocabulary (`heavy`/`standard`/`light`/`ranged`/`unarmed`)
so the Technique can auto-fire for all four of its choices, not just
`unarmed`? And, separately but in the same area: `pickTechniqueChoice` needs
a non-domain code path for `has_choice` Techniques — should it read the
choices from `step_trigger` (e.g. a `choices:` list you'd add to the schema),
or elsewhere?

**Recommend:** *"Switch to Opus to resolve this escalation before continuing
to TD-12 onward."* This does not block Q3 (TD-12–TD-15), which is unrelated
machinery, but it should land before anyone treats Weapon Mastery's auto-apply
as working end-to-end in play.

**Resolved.** Planner ruled in `docs/DESIGN_technique_difficulty.md` §8
(2026-08-02): the two vocabularies are orthogonal axes and both stay —
`weapon_category` keeps its TD-7 job, a new `weapon_type` field carries
Weapon Mastery's own fictional taxonomy, and `TechniqueDef.choices` fixes the
second, compounding defect (`pickTechniqueChoice`'s missing non-domain code
path). Implemented as TD-18/TD-19/TD-20 below. Return to Worker to continue
from `docs/TASKS_technique_difficulty.md` TD-18.

---

## DESIGN §8 amendment — TD-18, TD-19, TD-20

Resolves the escalation above. Full ruling in
`docs/DESIGN_technique_difficulty.md` §8 — summary: `weapon_category` (IV.1,
mechanical, sets the Strike attribute) and `weapon_type` (II.4a, fictional,
what *Weapon Mastery* masters) are orthogonal and both ship on the Strike
message; a longsword is `standard` category and `blades` type at once, so
neither list can be collapsed into the other without breaking one job.

### TD-18 — `weapon_type` on the Strike, `weapon_mastery` retargeted

**`app/facets/schema.py`:** `EquipmentDef` gains `weapon_types: list[str]`
(mirrors `weapon_categories` but is a flat list — there is no attribute to
default from this vocabulary). `TechniqueDef` gains `choices: list[str] |
None` (TD-19, but added here since both land in the same class).

**`facets/base/facet.yaml`:** `equipment.weapon_types: [blades, blunt,
polearms, unarmed]` (no ranged entry — content gap, docs/TODO.md T8, not
fixed here). `weapon_mastery.step_trigger.match` retargeted from
`weapon_category` to `weapon_type`; `weapon_mastery`, `acclimated`, and
`field_of_mastery` each gain a `choices` list matching their
`choice_prompt` prose word-for-word.

**`app/game/combat.py`:** no logic change — `apply_character_difficulty_step`
already reads whatever field name `trigger.match` names out of the `context`
dict generically; only its docstring gained a `weapon_type` mention. This is
worth stating explicitly since it is the reason the fix is data-only: the
"generic composition, no hardcoded field names" property the function was
built with (TD-6) is exactly what let the escalation be closed without
touching the one file `CLAUDE.md` says may carry this rule.

**`app/api/websocket.py`** (`_handle_strike`): a second optional field,
`weapon_type`, alongside `weapon_category` — same validation shape (checked
against `ruleset.equipment.weapon_types`, rejected with an error message if
present but unrecognised, silently absent if not sent), added to both the
difficulty-composition context dict and the `strike_result` broadcast.
`weapon_category` is untouched — same code, same job, still in both places.

**`app/static/index.html` / `play.js`:** a second picker,
`#strike-weapon-type`, beside the existing category picker. Deliberately no
`onchange` handler — TD-18's constraint #1 is that `weapon_category` alone
still defaults the attribute; `weapon_type` sets nothing.

**Tests** (`tests/test_websocket.py`, `TestCombatGameplayLoop`): rewrote the
two TD-7-era tests that fired Weapon Mastery through `weapon_category` — that
route only ever worked because both tests used `"light"` as a stand-in value
for both fields at once, which is exactly the bug the escalation found —
into the acceptance criteria's five: fires on matching `weapon_type`, doesn't
fire on mismatched `weapon_type`, doesn't fire when `weapon_type` absent,
doesn't fire on `weapon_category` alone (proving the axes are separate), and
the III.3:513 regression (Mordai, Weapon Mastery in blades, Standard →
Easy, `weapon_category: "standard"` + `weapon_type: "blades"` both present,
matching how a real Strike would actually be sent). Added round-trip and
unknown-value error tests for `weapon_type` mirroring the pre-existing
`weapon_category` coverage. Updated `test_strike_without_weapon_category_
behaves_as_today` to also assert `weapon_type is None`, and
`TestCastHandlerUnaffectedByDifficultyStep`'s technique_choices/context values
from `"light"` to `"blades"`/`weapon_type` so the test still proves what it
claims to (a Technique that *would* fire on a Strike) now that `"light"`
alone can no longer make Weapon Mastery fire at all.

**`tests/test_facets_schema.py`:** updated the one integration assertion that
pinned the old match field (`TestDifficultyStepMetadataInBaseFacet
.test_auto_triggers_match_declared_fields`); updated the isolated unit test
`test_auto_trigger_technique_parses` for consistency (it used
`weapon_category` as a stand-in value, unrelated to real facet.yaml data, but
leaving it stale next to the real fix would mislead a future reader). Added
`TestWeaponCategories.test_weapon_types_present_and_orthogonal_to_categories`.

### TD-19 — `choices` as data

**`app/facets/schema.py`:** documented above; `choices` defaults to `None` so
every pre-existing Technique parses unchanged.

**`facets/base/facet.yaml`:** `weapon_mastery` → `[blades, blunt, polearms,
unarmed]`; `acclimated` → `[extreme cold, extreme heat, altitude,
deprivation]`; `field_of_mastery` → `[history, arcane theory, natural
sciences, theology, law, languages, geography]`, with a comment noting these
are suggestions, not a closed set (II.4a: "or another domain with MM
approval") — nothing in the schema or the engine enforces membership
(INV-8), by design; there is no "closed vs. open" flag anywhere, `builder.js`
special-cases `field_of_mastery` by id instead (TD-20).

**Tests** (`tests/test_facets_schema.py`): unit tests
`test_no_choices_parses_unchanged` / `test_technique_with_choices_parses`
(`TestTechniqueDef` or wherever the existing TD-4 class lives — placed next
to `test_invalid_difficulty_step_raises`). New integration class
`TestNonDomainTechniqueChoices` against the real ruleset: all three
Techniques carry `choices`; an ordinary Technique (`forcing_hand`) still
parses without it; `choices` values individually appear (case-insensitively)
in the corresponding `choice_prompt` — the acceptance test TD-19 names as
the one that matters, since it is what keeps the book and the data from
silently drifting apart; and one assertion each pinning the three lists by
exact/partial value.

### TD-20 — the picker's non-domain fallback

**`app/static/js/builder.js`:** `pickTechniqueChoice` now checks `def.choices`
first — if present and non-empty, delegates to a new `pickFromChoicesList`
that renders a `selectDialog` straight from the list (`value === label`, no
transformation), with one addition: for `field_of_mastery` specifically
(matched by id, since there is no schema-level "open-ended" flag — DESIGN §8
was explicit that adding one wasn't warranted for a single Technique) an
`"Other (type your own)..."` option drops into `promptDialog` for free text.
Weapon Mastery and Acclimated are closed sets and offer only what `choices`
lists. The pre-existing domain-list branch is unchanged and only runs when
`def.choices` is absent — which, after TD-19, is true of every
domain-granting Technique and false of exactly the three this cycle touches.

**Tests** (`tests/e2e/test_ui_flows.py`, new class
`TestTechniqueChoicePicker`): two tests. `test_weapon_mastery_choice_reaches_
technique_choices_on_the_character` grants a real Technique pick (two Body
skill advances via a direct `skill_advance` WS call — the MM's "Advance
Skill" button in `index.html` never sends its `marks` field at all, a defect
independent of this cycle and not fixed here since it isn't in scope; calling
`sendWS` directly is the same class of workaround the file already uses),
reads the real `weapon_mastery` Technique definition out of the correctly-
shaped nested `ruleset.techniques.body.branches[].tiers[].techniques[]`, and
calls `pickTechniqueChoice` on it directly rather than through
`selectTechnique`/a button click. `test_domain_granting_technique_keeps_the_
domain_list_behaviour` does the same against `arcane_study` (a real
domain-granting Technique with no `choices`) and asserts the picker still
offers domain-shaped options (`"Name (type)"` labels), proving the new branch
is additive, not a replacement.

**Why not driven through the real "Select" button.** While staging this test,
found that `builder.js::renderBuilderTechniques`/`selectTechnique` read
`state.ruleset.character_facets.find(...).techniques` — a field that does not
exist on the wire (`CharacterFacetDef` is `id`/`name`/`description`/
`major_attribute` only; the real Technique tree is the separate top-level
`ruleset.techniques[facet_id]`). The "Available" Technique list in the
Builder tab is therefore always empty, and the button the acceptance
criteria describes clicking does not currently render. This is a real,
independent bug (`docs/TODO.md` T9) — not something TD-18/19/20 touches or
was asked to fix, and fixing `renderBuilderTechniques`, `selectTechnique`,
and `app.js::techniqueDisplayName` (same root cause, third call site) is new
scope across two files outside all three tasks' file lists. The test instead
calls `pickTechniqueChoice` directly with a correctly-sourced Technique
definition, which is exactly what TD-20 asked to fix and is sufficient to
prove it, using the same direct-injection precedent TD-10's Strike-banner
tests already established in this file for an analogous situation (full
round trip via another path is separately broken or impractical to stage).

**Two more pre-existing gaps found staging the same test, also out of scope
and also filed** (`docs/TODO.md` T10, T11): the `skill_advanced` broadcast
never carries `technique_picks_available` and `app.js` never applies it
(so a granted pick is invisible client-side until a reload); and
`onTechniqueSelected` never writes `msg.choice` into
`state.character.technique_choices` (so a made choice is likewise invisible
client-side until a reload), and separately sets `magic_technique_active =
true` unconditionally for every Technique, not just magic-granting ones. Both
are proven real (not test error) because the *server-side* character state
is correct in both cases — verified by reloading the page (which re-fetches
full session state via `onStateReceived`, carrying the true values) rather
than trusting the incremental broadcast handlers. The test routes around
both rather than fixing them.

### Test count

Backend (`test_websocket.py`, `TestCombatGameplayLoop`): the 2 TD-7-era
weapon-mastery tests were replaced by 5 (net +3), plus 2 new round-trip/
unknown-value `weapon_type` tests (net +2) — net **+5**. The `weapon_type is
None` addition to the existing backward-compat test and the cast-handler
value fix are edits in place, not new tests.
`test_facets_schema.py`: 2 new unit tests + 1 new integration test
(`TestWeaponCategories`) + 6 new tests (`TestNonDomainTechniqueChoices`) —
net **+9**. E2e: 2 new tests (`TestTechniqueChoicePicker`) — net **+2**.

`python3 -m pytest -q` from `software/`: **1356 passed**, zero failures, zero
unexpected skips. Ran in the foreground, full suite including the Playwright
e2e module, ~4m52s. (1340 baseline + 5 test_websocket.py + 9
test_facets_schema.py + 2 e2e = 1356.)

### Discovered, filed, not fixed (all out of TD-18/19/20 scope)

- **T9** — `character_facets[].techniques` doesn't exist; the Builder tab's
  Technique list is always empty.
- **T10** — `skill_advanced` broadcast omits `technique_picks_available`;
  `app.js` never applies it.
- **T11** — `onTechniqueSelected` never writes the choice into
  `technique_choices`; also sets `magic_technique_active` unconditionally.

None of these were introduced by this cycle — all three predate TD-18/19/20
and were only surfaced because TD-20's acceptance criteria required actually
driving the Technique-selection flow, which nothing had exercised
end-to-end before.

---

## Q3 — the licensed override (TD-12, TD-13, TD-14, TD-15, TD-16)

**Date:** 2026-08-02
**Scope:** the whole Q3 block plus the shared MM1 calibration sentence (TD-16),
per assignment. TD-1 … TD-11 and TD-18 … TD-20 were already done (see above);
TD-17 was already recorded in `docs/TODO.md` T7. This entry closes the cycle.

### TD-12 — schema and data for the override flag

`TechniqueDef` (`software/app/facets/schema.py`) gains
`removes_target_from_conflict: bool = False`, documented in the class
docstring in the existing style (same pattern as `difficulty_step`/
`choices`). `facet.yaml`'s `the_final_blow` entry is the only Technique that
sets it `true`.

`TestFinalBlowOverrideFlag` (`test_facets_schema.py`) pins the count at
exactly one and names it, mirroring `TestDifficultyStepMetadataInBaseFacet`'s
pattern from TD-6: `test_exactly_one_technique_carries_the_flag`,
`test_the_final_blow_carries_the_flag`,
`test_an_ordinary_technique_does_not_carry_the_flag`.

### TD-13 — resolve the removal as a defeat event

New `combat.py` function `apply_final_blow_removal(resolve_current,
phase_thresholds=None) -> FinalBlowResult`. Deliberately a **new dataclass**
(`FinalBlowResult`), not a reuse of `ResolveDamageResult` — the two must be
distinguishable at the *type* level, not just by field values, so a future
sim series or a transcript reader can tell a licensed-override removal apart
from an ordinary Strike that happened to zero an enemy's Resolve, without
relying on a caller remembering to check a string. `FinalBlowResult` also
carries `cause: str = "final_blow"` for callers (the WS broadcast) that want
a machine-readable label rather than a type check.

The function always sets `resolve_current = 0` and `defeated = True`
(the removal works on any target, Bosses included, per the BRIEF), and — the
P11-invariant part — routes the crossing check through the shared
`phase_crossed` primitive, the same one `apply_resolve_damage` uses, so a
Boss phase sitting between the target's prior Resolve and 0 still fires
exactly as it would from an ordinary Strike. It never does `resolve_current
= 0` as a bare assignment outside of building the result.

`TestApplyFinalBlowRemoval` (`test_combat.py`): 4 tests —
`test_removal_produces_a_defeat_event`,
`test_removal_routes_through_phase_crossed` (including the "already at/under
threshold: no re-fire" case, mirroring `TestApplyResolveDamage`'s existing
phase tests), `test_transcript_entry_is_distinguishable_from_a_resolve_zero_defeat`
(asserts both `isinstance`/type difference and the `cause` field),
`test_no_raw_resolve_current_zero_write_in_source` (inspects the function's
source text for `phase_crossed(` and the absence of a bare
`resolve_current = 0` assignment — a structural guard against a future edit
reintroducing the bypass).

The once-per-session gate, the Spark spend, the "succeed" (7+) check, and
whether the removal *commits* are all left to the caller (websocket.py) —
`apply_final_blow_removal` only resolves the mechanical consequence once a
caller has already decided the Technique fires. No escalation was needed:
routing through the canonical path did not require changing
`apply_resolve_damage`'s or `phase_crossed`'s signature — a sibling function
with the same shape was sufficient.

### TD-14 — wire Final Blow through the strike handler

Two-phase flow, matching DESIGN §4's "auto-apply governs difficulty steps,
not actor removal":

1. **Offer** — the player declares Final Blow with their Strike (`final_blow:
   true` on the `strike` message). `_handle_strike` (`websocket.py`) checks
   preconditions *before* the roll resolves and *before* `_spend_sparks` is
   called, so a rejected declaration costs the player nothing: the Technique
   must be unlocked (`"the_final_blow" in character.techniques`), unused this
   session (`character.techniques_used_this_session` — the existing field,
   no new one added, per the assignment's constraint), the roll must be a
   Combat roll (`skill_id == "combat"`, the Strike handler's own default), and
   a Spark must be requested on this roll (`sparks_spent >= 1`). Once the
   roll resolves, `final_blow_available` on the `strike_result` broadcast is
   `true` only if `final_blow_requested` and the outcome is `full_success` or
   `partial_success` (7+, both success tiers, per the BRIEF) — never on
   `failure`. Firing only offers the removal; nothing about any enemy changes
   and the Technique is not yet marked used.
2. **Commit** — a new MM-gated WS event, `final_blow_confirm` (`player`,
   `tracker_key`), dispatched to a new handler `_handle_final_blow_confirm`.
   It re-validates (technique unlocked, not already used — defense in depth
   against a stale or replayed confirm), looks up the tracked enemy, calls
   `combat.apply_final_blow_removal` through the same `before`-Resolve
   pattern `_handle_enemy_strike` already uses, sets
   `enemy.resolve_current = result.resolve_current`, and **only here**
   appends `"the_final_blow"` to `character.techniques_used_this_session` and
   persists it (`session.save_character_to_disk`). The broadcast is
   `enemy_updated` extended with `cause: "final_blow"`, `player`, and
   `technique_id` — reusing the existing message type (so the client's
   existing `onEnemyUpdated` handling of `defeated` keeps working
   unmodified) while staying distinguishable via the extra fields, matching
   TD-13's transcript-distinguishability requirement one layer up.

Client (`play.js`, `index.html`): a "The Final Blow" checkbox on the Strike
sub-form (cleared after each Strike, matching the once-per-session gate
being enforced server-side); an MM-only `notify(...)` prompt on
`strike_result` when `final_blow_available` is true, mirroring the existing
"Apply" prompt for ordinary Strike outcomes, with a "Confirm Final Blow"
action that sends `final_blow_confirm`; and a distinguishing chat line in
`onEnemyUpdated` when `msg.cause === 'final_blow'` ("removed from the
conflict — The Final Blow" rather than "is defeated"). No e2e test was
added for this — TD-14's acceptance criteria list only WS-level tests, and
the wiring is exercised end-to-end by the WS test suite; the client changes
are the minimum needed for the feature to be usable at a table.

`TestFinalBlowLicensedOverride` (`test_websocket.py`): 8 tests —
`test_fires_on_full_success`, `test_fires_on_partial_success`,
`test_does_not_fire_on_failure` (dice pinned via
`patch("random.randint", ...)`, values chosen against Zahna's known +1
Strength modifier and Standard difficulty to land deterministically in each
outcome band — see the class docstring for the arithmetic),
`test_second_use_in_same_session_is_refused`,
`test_removal_does_not_commit_without_mm_confirmation` (asserts the enemy's
`resolve_current` is untouched and the Technique is not marked used after a
firing Strike with no confirm),
`test_mm_confirm_commits_the_removal`, `test_second_mm_confirm_is_refused`,
`test_non_mm_cannot_confirm_final_blow` (a player token gets "Unknown event
type" — `final_blow_confirm` is dispatch-gated `and is_mm`, same pattern as
`enemy_strike`).

### TD-15 — Q3 prose

II.4a's *The Final Blow* entry gains one sentence between the description
and `Normal:`: "'Succeed' means a **10+ or a 7–9** — both success tiers
count. On a 7–9, the partial's usual cost still applies and shapes how the
removal happens in the fiction, but never whether it happens: the target is
gone either way." The `Normal:` field ("A Spark adds a d6 and drops the
lowest. A Strike depletes Resolve, and riders never defeat an enemy on their
own") still reads true afterward — it describes the baseline the Technique
departs from, which the new sentence doesn't touch.

MM1 gains an **MM Note** box in the *Bosses* section ("build for the early
exit, not against it"): a capstone landing early doesn't just skip a phase,
it skips the encounter, so front-load anything a phase change was protecting
rather than gating it behind Resolve grinding.

**III.3 verified byte-identical.** `md5sum player_handbook/III.3_Combat.md`
before and after this pass: `45556c573be382c27af8ae6523674d61` both times.
`grep`-confirmed the rider sentence is untouched: "Riders never defeat an
enemy on their own — **Resolve does that; a rider only shapes the blows that
follow.**" (III.3:140).

### TD-16 — the MM1 calibration sentence

One bullet added to *Scaling Notes* (end of the Encounter Recipe Table
section): "The recipes above are calibrated for a baseline party —
`standard_party()` in the simulation corpus carries no Techniques. A party
fielding step-easier Strike Techniques ... or a Tier 3 capstone like *The
Final Blow* runs a Recipe Table encounter about a band hot — treat the
difficulty row you picked as one notch easier than printed." Advisory prose
only — the Recipe Table's numbers (Tables MM1–7 and MM1–8) are byte-for-byte
unchanged; no simulation was re-run.

### Generated finding aids

Regenerating `List_of_Boxes.md`/`List_of_Tables.md` (`tools.build_table_register`)
and `player_handbook/Index.md` (`tools.build_index`) was required to pick up
the new MM Note box and keep INV-9/INV-10 green — `test_table_register_is_up_to_date`
failed until the register was regenerated. The Index diff (176 insertions)
is larger than this pass's own edits account for; it was already stale
before this session started (from TD-18…TD-20's prose changes, which
predate this Worker's involvement) and the regeneration caught that
staleness too, which is expected and correct — `Index.md`/`List_of_*.md`
are never hand-edited (`CLAUDE.md`). `tools.build_bestiary` was also run for
completeness; it reported 0 files changed.

### Test count

`test_facets_schema.py`: +3 (`TestFinalBlowOverrideFlag`).
`test_combat.py`: +4 (`TestApplyFinalBlowRemoval`).
`test_websocket.py`: +8 (`TestFinalBlowLicensedOverride`).
Net **+15** over the TD-18…TD-20 baseline of 1356.

`python3 -m pytest -q` from `software/`: **1371 passed**, zero failures, zero
unexpected skips, run in the foreground to completion (full suite including
the Playwright e2e module). `test_docs_consistency.py` (31 tests, including
INV-6, INV-9, INV-11, INV-12, INV-13, INV-14) green after the finding-aid
regeneration.

---

## Cycle closed

TD-1 through TD-20 are all done. Q1 (composition), Q2 (pricing/wording
defect), and Q3 (licensed override) — all three rulings in `DECISIONS.md`
B4 — are implemented, tested, and documented, including the DESIGN §8
amendment (the two weapon vocabularies) raised and resolved mid-cycle.
`docs/TASKS_technique_difficulty.md`'s progress table is updated to reflect
the whole cycle complete. No outstanding escalations. Two follow-ups remain
recorded in `docs/TODO.md` for future work, neither blocking this cycle:
T7 (*Pressure Point*'s scene-effect store, deliberately deferred per DESIGN
§2.5) and T9/T10/T11 (pre-existing Builder-tab Technique-selection gaps,
found but out of scope while staging TD-20's e2e test).
