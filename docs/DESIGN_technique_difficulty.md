# DESIGN — Technique difficulty, domain pricing, and licensed overrides

**Tier:** Planner. **Input:** `docs/BRIEF_technique_difficulty.md` (Brain, 2026-08-02)
and the user's UX ruling of the same day. **Decision record:** `docs/DECISIONS.md` B4.
**Tasks:** `docs/TASKS_technique_difficulty.md`.

---

## 1. Scope

Three rulings to land, in one cycle, because they were escalated together and share
one mechanism:

| | Ruling | Where the work is |
|---|---|---|
| **Q1** | Technique difficulty steps compose with the MM's call; at most one character-side step per roll | schema, `combat.py`, three WS handlers, client, prose |
| **Q2** | Second Domain prices off its own domain's table; Ascendant prices off Broad alone | prose ×5 surfaces, tests only — **no engine change** |
| **Q3** | *The Final Blow* is a licensed override, resolved as a defeat event | schema, engine, WS handler, client, MM1 note |

**Non-goals this cycle.** No re-run of Series 7/9 (B4: corpus intact). No change to
III.3's rider sentence. No new difficulty rungs. No change to how the MM declares a
label — the MM stays authoritative for the *situational* call, and always will.

---

## 2. The mechanism (Q1)

### 2.1 Where the rule lives

**`software/app/game/combat.py`.** Non-negotiable: the project's iron law is that
the simulator may only drive `combat.py` and must never re-implement a rule
(`CLAUDE.md`). Difficulty composition is a rule. It goes in the shared module, and
the WS handlers and any future sim series both call it.

`engine.py` keeps `_step_difficulty_easier` / `_harder` — those are ladder
primitives, not the rule. `combat.py` composes them.

### 2.2 The function

```
apply_character_difficulty_step(
    declared_label, character, context, ruleset
) -> (final_label, applied_technique_id | None)
```

- `declared_label` is the MM's situational call, already resolved (including
  set-to-label effects like a Tier 2 rider making a target Easy). The function
  never second-guesses it.
- `context` is a small dict of roll facts the app already holds or newly sends:
  `skill_id`, `weapon_category`, `hazard_type`, `knowledge_field`, and
  `declared_technique_ids` (the player's toggles).
- Returns the stepped label **and which Technique did it**, because the roll banner
  has to show both moves and the transcript has to be auditable.

**Order:** declared label first, character step second, ladder clamps. **Guardrail:**
at most one character-side step per roll. If several qualify, the function picks
deterministically — a player-declared Technique wins over an auto one, then lowest
`id` — and reports the one it used. Determinism matters more than cleverness here:
two Techniques that both apply produce the same label either way (one step), so the
only thing the choice affects is what the banner names, and a stable answer is
easier to test and to explain at a table.

### 2.3 Applicability: two trigger kinds

New `TechniqueDef` fields, both optional so every existing Technique is unaffected:

- `difficulty_step: "easier" | "harder" | null`
- `step_trigger:` one of
  - `{kind: "auto", match: <field>, against: "choice" | <literal>}` — the app
    evaluates it from data it holds. Per B4's UX ruling, these apply **without
    asking**.
  - `{kind: "declared"}` — the player toggles it on the roll, because the trigger
    is a judgement no data settles.

Assignments for this cycle:

| Technique | Step | Trigger |
|---|---|---|
| *Weapon Mastery* | easier | auto — `weapon_type` == `technique_choices["weapon_mastery"]` — see §8, this started as `weapon_category` and was wrong |
| *Acclimated* | easier | auto — `hazard_type` == `technique_choices["acclimated"]`, **and** `skill_id == endurance` |
| *Field of Mastery* | easier | auto — `knowledge_field` == `technique_choices["field_of_mastery"]`, **and** `skill_id == lore` |
| *Steady Hand* | easier | auto — `skill_id` == `finesse` |
| *The Uncanny Angle* | easier | declared |
| *Pressure Point* | — | **out of scope this cycle** (see §2.5) |

**On *Steady Hand*.** Its printed trigger is "precision work under pressure",
which is fiction. `skill_id == finesse` is a proxy, and a slightly generous one —
not every Finesse roll is precision under pressure. Planner's call: take the
generous reading. The alternative is a toggle on the commonest skill in the game,
which is friction on every roll to save the MM from a step the guardrail already
caps at one rung. If play shows it firing where it should not, the MM's lever is
the situational label, which is one step in the other direction and already exists.

### 2.4 The new data the app must carry

`weapon_category` does not exist anywhere today — not on `Character`, not in the
strike message, not in `play.js` (`inventory` is `list[str]` free text). It must be
added to the strike message, sourced from a picker in the strike UI listing the five
IV.1 categories.

Side benefit worth taking: IV.1 already says a weapon's category **sets the Strike
attribute**. The category picker can drive the attribute selection, which removes a
step the player currently does by hand. That is a UX improvement, not scope creep —
it is the same picker.

`hazard_type` and `knowledge_field` are similarly new but cheaper: both are optional
strings on the generic-roll message, set by the MM or player when relevant, absent
otherwise. An absent field simply means the auto trigger does not fire.

### 2.5 *Pressure Point* is deferred, deliberately

*Pressure Point* is not a self-buff. It makes a difficulty one step easier **for any
character who follows the instructions, for the rest of the scene** — party-wide,
scene-scoped state, not roll-time metadata. It needs a scene-effect store the app
does not have.

Deferring it is honest and keeps this cycle atomic. Until it lands, it stays
MM-applied: the MM lowers the label, exactly as today. **The guardrail must be
documented at the point of the MM's call** so an MM applying Pressure Point by hand
and a Technique auto-applying do not both land on the same roll. That documentation
is a task, not a nice-to-have.

Follow-up recorded in `docs/TODO.md`.

### 2.6 Which handlers call it

Three call sites, all in `websocket.py`, all after the label is known and before
`RollRequest` is built: the **strike** handler (~585), the **generic roll** handler
(~275/310), and the **reaction** handler (~1111). The magic handler (~950) is
excluded — magic difficulty comes from the domain/scope table, and no Technique in
this cycle steps it.

### 2.7 What the client shows

The roll banner shows both moves: `Hard (MM) → Standard (Weapon Mastery)`. This is
the whole reason auto-apply is acceptable rather than spooky. A step nobody sees is
a step nobody trusts; the banner is what makes the automation legible, and it is a
required part of the feature, not a polish item.

---

## 3. Q2 — pricing, and the wording defect

**No engine change.** `character.py:406–410` and `engine.py:330–338` already
implement the ruling; the work is to make canon say what the code does, and to pin
it so a future refactor cannot quietly reverse it.

**The defect.** *Second Domain* reads "one difficulty step harder **than your primary
domain**". For a Focused-primary caster, Focused-plus-one *is* the standard table —
the penalty silently vanishes. Five surfaces re-anchor to **"one difficulty step
harder than normal for that domain"**:

`II.4b_...Mind.md` · `II.4c_...Soul.md` · `facet.yaml` (`second_domain_mind.roll`,
`second_domain.roll`) · `MM5_Quick_Reference.md`.

All five in one commit, per the sync iron law. `II.4b`/`II.4c` bodies are
hand-written; the `Normal:` fields already read correctly and need no change.

**Tests to add** (they are the deliverable — the prose is a consequence):
one pinning Ascendant → Broad table with no step, one pinning Second Domain → own
table, one step, and one specifically covering the Focused-primary case the old
wording broke.

---

## 4. Q3 — the licensed override

**Data.** `TechniqueDef` gains `removes_target_from_conflict: bool`, set true for
`the_final_blow` only. A flag, not a mechanism — the point is that overrides are
explicit at the site of the exception and greppable.

**Engine.** A new `combat.py` function that resolves the removal as a **defeat
event**, routed through the same path a Resolve-0 defeat takes. It must never write
`resolve_current = 0` directly — P11's invariant is that every `resolve_current`
mutation routes through `phase_crossed`, and a raw write would skip phase logic and
corrupt transcripts. The removal must also be distinguishable in the transcript
from an ordinary defeat, so a future sim series can count capstone removals.

**Frequency.** `Character.techniques_used_this_session` already exists and is the
right store. No new field.

**Flow.** Player declares Final Blow with their Strike → Spark spent, Combat roll
resolved → **on 7+** (both success tiers, per the brief) the target is removed →
MM confirmation required before the removal commits, because it deletes an actor
from the MM's encounter. Auto-apply governs *difficulty steps*, not actor removal;
these are different questions and the user answered the first.

**Prose.** II.4a's entry gains one precision sentence (7+ is a success; the
partial's cost shapes the aftermath, never the removal). III.3 changes **not at
all** — that is the point of the ruling. MM1 gains the encounter-design note.

---

## 5. Testing strategy

TDD, per the project ethos: test first, red, implement, green. Minimum three tests
per new public function (happy path, edge, error).

**The edges that actually matter here** — write these before the implementation:

1. **Clamping.** A step easier from Easy stays Easy. A step must never produce a
   label outside the four-rung ladder.
2. **The guardrail.** Two qualifying Techniques on one roll produce **one** step,
   and the reported technique id is deterministic.
3. **Non-firing.** Weapon Mastery (blades) with `weapon_category: "unarmed"` does
   not fire. An absent `weapon_category` does not fire. A Technique the character
   has not unlocked does not fire.
4. **Order.** The MM's Hard plus a Technique step yields Standard, not Easy —
   proving the step composes with the call rather than replacing it.
5. **Precedence.** A declared toggle beats an auto match, and the banner names the
   one that applied.
6. **Q3 invariant.** A Final Blow removal produces a defeat event and routes
   through `phase_crossed`; no test may observe a raw `resolve_current` write.
7. **Sim boundary.** A test asserting the simulator calls the shared composition
   function rather than carrying its own copy — the regression that invalidated a
   corpus once already.

**Docs invariants.** INV-14 already pins every Technique's `use`/`normal` and its
header against `facet.yaml`; the new fields must not break it. The Q2 wording fix
touches MM5, so INV-6 (typographic dashes) and the quick-ref compression law apply.

---

## 6. Sequencing

TD-1 → TD-3 are Q2: prose and tests only, no engine, and they close a live defect.
Do them first — they are independent of everything else and lowest risk.

TD-4 → TD-11 are Q1, in dependency order: schema, then the shared rule, then data
plumbing, then handlers, then client, then prose.

TD-12 → TD-15 are Q3.

TD-16 is the MM1 calibration sentence, shared by Q1 and Q3, and lands last because
it describes the finished behaviour.

---

## 7. Open questions handed to Worker

None blocking. Two things a Worker should escalate rather than decide:

1. If `skill_id == finesse` proves too broad for *Steady Hand* during
   implementation — e.g. it fires on ranged Strikes, which are Finesse — escalate
   rather than inventing a narrower predicate. The Strike case is real and §2.3's
   generous reading may need a carve-out.
2. If routing the Q3 removal through the canonical defeat path turns out to
   require changing that path's signature, stop. That path is P11-invariant
   territory and a signature change is a Planner decision.

---

## 8. Amendment — the two weapon vocabularies *(Planner, 2026-08-02)*

**Raised by:** Worker escalation during TD-7 (`docs/LOG_technique_difficulty.md`).
**Cause:** a Planner error in §2.3/§2.4. TD-7 was specified against IV.1's weapon
*categories* without checking what *Weapon Mastery* actually asks the player to
choose. It asks for something else.

### The finding

Two vocabularies exist and they are **not** the same list:

| | Values | Job |
|---|---|---|
| `weapon_category` (IV.1, `facet.yaml equipment.weapon_categories`) | heavy · standard · light · ranged · unarmed | **Mechanical** — sets which attribute a Strike uses |
| *Weapon Mastery*'s choice (II.4a, `choice_prompt`) | blades · blunt · polearms · unarmed | **Shape** — what the character has mastered |

Only `unarmed` appears in both. As shipped, *Weapon Mastery* can auto-fire for one
of its four choices, and the case B4 cites as its flagship justification — Mordai
with Weapon Mastery (blades), III.3:513 — can never fire at all.

### The ruling: they are orthogonal axes, and both stay

A longsword is `standard` category **and** `blades` type. A greatsword is `heavy`
**and** `blades`. The lists cut across each other, so collapsing them breaks one job
or the other:

- Retiring `blades/blunt/polearms` and re-anchoring Weapon Mastery to the
  mechanical categories would make "Weapon Mastery (standard)" the printed choice —
  mastery of a *stat bucket* rather than of a kind of weapon. Rejected: it reads as
  a spreadsheet and it silently changes what the Technique means.
- Retiring the categories would take the attribute default with them. Rejected.

**So:** the Strike message carries **both**. `weapon_category` keeps its TD-7 job
(defaulting the attribute). A new `weapon_type` — blades · blunt · polearms ·
unarmed — carries shape, and *Weapon Mastery*'s `step_trigger.match` retargets to
it. Both stay optional; absent means the trigger does not fire.

### Second finding: there is no choice picker

`builder.js::pickTechniqueChoice` only knows how to build **domain** lists. For
*Weapon Mastery*, *Acclimated*, and *Field of Mastery* it produces an empty option
set, so those choices cannot currently be made in the app at all — which means the
`against: "choice"` triggers have nothing to match even once the vocabulary is fixed.

**Fix:** `TechniqueDef` gains `choices: list[str] | None`. The three choice-bearing
non-domain Techniques enumerate their options as data instead of burying them in
`choice_prompt` prose, and the builder renders a picker from it. `choice_prompt`
stays as the human-readable label.

### Content gap — not fixed here, referred to the user

*Weapon Mastery*'s four types have **no option covering ranged weapons**. An archer
cannot meaningfully take the Technique. That is canon as printed in II.4a, not a
defect this cycle introduced, and adding a fifth option is a content decision for
the setting's author. Recorded in `docs/TODO.md`; do not fix it in code.

### Tasks

TD-18 through TD-20, below.
