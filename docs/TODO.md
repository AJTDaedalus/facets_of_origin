# TODO — Open Follow-Ups

Running list of known-open work that is not yet a task in a `TASKS_<feature>.md`.
Items here are **deliberately deferred**, not forgotten: each one records what is
wrong, why it was not fixed in the pass that found it, and what "done" looks like.

When an item grows into real scope, promote it into a `TASKS_<feature>.md` and
strike it here with a pointer.

---

## ~~T1 — PHB III.3 is silent on whether a redundant armor charge is spent~~

**Closed 2026-07-11** (editorial-fixes pass): PHB III.3 *Armor and Reaction
Downgrades* now states the charge-consumption rule ("a downgrade that softens
nothing costs nothing from the budget"), and MM5's Armor quick-ref compresses
it. `facet.yaml` and the engine already agreed — no code change was needed.

**Source:** PR #5 review (DECISIONS R1, 2026-07-11).

**What's wrong:** PHB III.3 says armor and reaction downgrades "do not stack —
apply the greater reduction only." That fixes the resulting *tier*, but says
nothing about whether the armor **charge** is consumed when the reaction has
already applied the greater (equal) reduction.

The engine now implements "the charge is **not** spent"
(`combat.resolve_incoming_condition`, `armor_spent=False` on the reaction path).
That reading follows from armor being "a finite number of incoming Conditions it
can soften" — a charge that softens nothing is not spent — and it preserves the
D2 budget's intended lifetime. But it is currently **code-only canon**: a table
reading the PHB cannot derive it, and would reasonably rule the other way.

**Why not fixed in the review pass:** writing the rule into PHB prose is
authoring, not fixing. Per the narrative iron law, a reviewer does not invent
rules text the user has not established.

**Done when:** PHB III.3's *Armor and Reaction Downgrades* section states the
charge-consumption rule explicitly, and MM5's Armor quick-ref reflects it (a
compression of the body text, never a new rule). `facet.yaml` and the engine
already agree — no code change expected.

---

## T2 — No MM UI for applying a Condition to a PC

**Source:** PR #5 review (DECISIONS R1, 2026-07-11).

**What's wrong:** the `apply_condition` WebSocket message is server-side only.
Nothing in `app/static/js/` ever sends it — the MM has no control for applying a
Condition to a player character. The handler is exercised by tests and the e2e
playtest harness, and by nothing else.

The `reaction_downgraded` flag added in R1 (which is what makes armor/reaction
non-stacking work) is therefore **wired but unreachable from the UI**: an MM
running a live session cannot currently tell the engine that a Dodge/Parry
partially succeeded.

**Done when:** the MM's play view can apply a Condition to a named PC, with a
"reaction partially succeeded" toggle that sets `reaction_downgraded`. The MM
sends the **raw** incoming Condition — the engine applies the reduction. The MM
must never pre-downgrade it themselves, or armor reduces it a second time.

---

## T3 — `resolve_strike` / `resolve_reaction` have no production caller

**Source:** PR #5 review (DECISIONS R1, 2026-07-11); originally LOG WS-A0,
judgment call #3.

**What's wrong:** the simulator drives the whole of `app/game/combat.py`. The
live engine drives only the lookups and consequences — its dice go through
`engine.resolve_roll`/`RollRequest`, because a Strike in play is split across two
player/MM actions rather than one call. So `resolve_strike` and `resolve_reaction`
run in simulation and never at a table.

This is a **standing divergence risk**, not a settled boundary. Any rule written
inside `resolve_strike` reaches the simulator and no real game. That has already
happened once: the Staggered −1 penalty lived there as a literal, so it was
applied in every recorded simulation and in no actual session (fixed in R1 by
moving it to `combat.offense_modifier`, which both callers use).

The specific divergence is closed. The shape that produced it is not.

**Interim mitigation (in place):** the module docstring says, in as many words,
put shared rules in the helpers and never inside `resolve_strike`. That depends
on a contributor reading it.

**Done when:** either (a) `_handle_strike`/`_handle_react` compose their rolls
through `resolve_strike`/`resolve_reaction` — which means plumbing skill ranks,
Spark dice and Press through a flat-modifier API — or (b) the two functions are
retired and the simulator composes its strikes from `offense_modifier` + `roll`
like the engine does, leaving exactly one strike path. Either way the goal is
one shape, not two. Pick deliberately; (b) is the smaller change.

---

## ~~T4 — `test_default_port_is_8000` reads the developer's real `.env`~~

**Closed 2026-07-12.** `TestSettingsDefaults` now takes a `default_settings` fixture that clears every
`Settings` field's env var and passes `_env_file=None`, so the class asserts the code's declared
defaults rather than the machine's configuration. `PORT=8010` in the local `.env` is intentional
(it avoids a port clash) and is no longer the suite's problem.

The leak was class-wide, not port-specific: `test_facets_dir_default` had already been patched by
hand to pass `facets_dir=` because `conftest` exports `FACETS_DIR` — a workaround for this same
cause, applied to one field. The fixture fixes it at the source. A companion test asserts the env
var still *wins* when present, so the isolation can't hide a real regression.

Full suite is green on a machine with a populated `.env`: **1026 passed, 0 failed.**

---

<details>
<summary>Original report</summary>

**Source:** PR #5 review (2026-07-11). **Pre-existing — predates the PR.**

**What's wrong:** `app/config.py` sets `model_config = SettingsConfigDict(env_file=".env")`,
so `Settings()` picks up the local untracked `.env` during tests.
`tests/test_config.py::TestSettingsDefaults::test_default_port_is_8000` asserts
the default port is 8000 and fails on any machine whose `.env` sets `PORT`
(e.g. `PORT=8010` → `assert 8010 == 8000`).

The whole file passes (21/21) once `.env` is moved aside, so the code is fine —
the test is environment-sensitive. It makes the suite's pass/fail depend on
developer-local state, which is exactly what a defaults test should not do.

**Done when:** the defaults tests construct `Settings` with the env file
suppressed (e.g. `Settings(_env_file=None)`), so they assert real defaults rather
than whatever the local `.env` happens to hold. Full suite should be green on a
machine with a populated `.env`.

</details>

---

## T5 — Oraga Night's presentation layer is deferred

**Source:** style audit remediation, 2026-08-01 (`docs/RESEARCH_style_audit.md`
findings O3, O6, O7, and the module's fiction prologue). **Deferred by the user,
2026-08-02:** "leave the Oraga question for later."

**What's open.** Waves 1, 2, and 5 of the audit landed the module's intro battery,
eight triggered read-aloud blocks, printed Spark awards, typed enemy conduct, and
sequential area codes. Four presentation items were left:

- **O3 — the keyed-area field battery.** `04_The_Ball.md`'s rooms are `**B1. Name.**`
  plus prose plus an italic `*(Agenda relevance: …)*` parenthetical doing the job of
  a Development field informally. `adventures.md` §2 wants one fixed order — header
  facts → read-aloud → explanation → creatures → tactics → treasure → development —
  with bold labels, and even empty areas getting a line plus their return-visit
  change. The *content* is mostly present; the invariant *shape* is not.
- **O6 — maps.** No map, no scale line, no terrain-as-rules lines, no
  starting-position key. `04_The_Ball.md` currently tells the MM to "know this
  geography cold" instead of shipping the geography. Needs cartography this project
  does not have yet.
- **O7 — one-page scene cards.** `adventures.md` §5 Stage 3, which the guide notes
  is *cheap* for FoO because the stat lines are light. Depends on O6 for the map
  key.
- **The fiction prologue.** One page of italic in-world fiction that dramatizes the
  stakes for the MM and is never referenced again (`adventures.md` §1). Not written,
  because writing one means inventing a scene in the user's setting.

**Why deferred:** O3 is a large layout pass over prose that currently reads well;
O6/O7 need art the project has not commissioned; the prologue needs canon that is
the user's to establish.

**Done when:** every keyed area in `04_The_Ball.md` and `05_The_Longest_Night.md`
follows one printed field order; a palace map exists with a scale line, a letter key
matching the enemy roster, and one rules-line per named terrain feature; each opt-in
fight has a one-page scene card with pointer lines both ways to the narrative flow;
and the module opens on a one-page italic prologue.

---

## T6 — Bestiary entries need their Adaptation notes reviewed against Shattered Origin

**Source:** Bestiary drafting, 2026-08-02.

**What's open.** The Bestiary is written as a **setting-agnostic core module** — every
creature in it is portable, and every entry carries an *Adaptation* line telling an MM
how to refit it. None of them has been placed in Shattered Origin, and none should be
until the setting's author decides where (or whether) they belong. The one exception is
the Latchmen family, whose Boss expression is the Archive Guardian, which was already
canon.

**Done when:** the setting's author has ruled, per family, whether it exists in
Shattered Origin, and the Shattered Origin setting Facet carries whatever placement,
renaming, or exclusion that ruling implies.

---

## T7 — *Pressure Point* is not covered by the Technique step machinery

**Source:** Planner design for B4 Q1, 2026-08-02
(`docs/DESIGN_technique_difficulty.md` §2.5). Tracked as **TD-17**.

**What's wrong.** *Pressure Point* (Mind, Clarity, Tier 3) makes a difficulty one
step easier "for any character who follows your instructions, for the rest of the
scene". Every other step-easier Technique is a self-buff evaluated at roll time.
This one is **party-wide, scene-scoped state**, and the app has no scene-effect
store to hold it.

**Why it was not built this cycle.** Adding a scene-effect store is a real feature —
lifetime, visibility, who it applies to, how it ends — and folding it into the
difficulty-step cycle would have made that cycle non-atomic. The other five
Techniques are roll-time and ship cleanly without it.

**What happens meanwhile.** *Pressure Point* stays MM-applied: the MM lowers the
declared label, exactly as before this cycle. The risk this creates is double-
counting — an MM applying Pressure Point by hand while a Technique also
auto-steps the same roll would move it two rungs, which B4's guardrail forbids.
TD-11 puts that warning in MM2 where the MM will meet it.

**Done when:** a scene-effect store exists; *Pressure Point* writes into it on use;
`apply_character_difficulty_step` reads it and counts it as **the** one permitted
character-side step for any qualifying roll; and the double-counting warning in MM2
is removed because it can no longer happen.

---

## T8 — *Weapon Mastery* has no option for ranged weapons

**Source:** Worker escalation during TD-7, resolved by Planner in
`docs/DESIGN_technique_difficulty.md` §8, 2026-08-02.

**What's wrong.** *Weapon Mastery* (Body, Might, Tier 1) reads "Choose one weapon
type: blades, blunt, polearms, or unarmed" (II.4a, `facet.yaml`
`weapon_mastery.choice_prompt`). None of the four covers a bow, crossbow, sling, or
thrown weapon — all of which IV.1 lists as a weapon category in their own right.
An archer cannot meaningfully take the Technique, and III.3 explicitly blesses
ranged Strikes as ordinary Strikes.

**Why it was not fixed.** Adding a fifth option changes what a printed Technique
offers, which is a content decision for the setting's author, not a Worker or
Planner call. The mechanical plumbing added this cycle (`weapon_type` on the Strike
message) will carry a fifth value the day one is chosen — no code change needed.

**Done when:** the author has ruled whether *Weapon Mastery* gains a ranged option
(and what it is called), and if so it lands in II.4a, `facet.yaml`'s `choice_prompt`
and `choices`, and the client picker in one commit.

---

## ~~T9 — The Builder tab's "Available" Technique list is always empty~~

**Source:** discovered while implementing TD-20
(`docs/TASKS_technique_difficulty.md`), 2026-08-02.

**What's wrong.** `builder.js::renderBuilderTechniques` and `selectTechnique`
look up a Technique's definition via
`state.ruleset.character_facets.find(cf => cf.id === char.primary_facet).techniques`.
`character_facets` entries never carry a `techniques` field — `EquipmentDef` aside,
`CharacterFacetDef` (`app/facets/schema.py`) is `id`/`name`/`description`/
`major_attribute` only. The real, nested Technique tree is a separate top-level
key, `ruleset.techniques[facet_id].branches[].tiers[].techniques[]`. The result:
`facetDef.techniques` is always `undefined`, `renderBuilderTechniques`'s
`available` list is always empty, and the player's Builder tab always reports
"Every Technique in this Facet is learned" regardless of what is actually true.
`app.js::techniqueDisplayName` has the identical bug and always falls back to
its id-based-formatting default. `selectTechnique` itself degrades gracefully —
`def` comes back `undefined`, the `has_choice` branch is skipped, and it fires
`technique_select` with no `choice` — but the player can never reach that path
because the button that calls it never renders.

**Why not fixed here.** TD-20's scope was `pickTechniqueChoice`'s fallback for
non-domain choices (DESIGN §8) — a narrower, already-scoped fix. This bug sits one
layer above it (the list that would let a player click through to
`pickTechniqueChoice` at all) and touches `renderBuilderTechniques`,
`selectTechnique`, and `techniqueDisplayName` across two files, which is new
scope a Worker should not absorb into an unrelated task without a Planner call.
TD-20's e2e test routes around it by calling `pickTechniqueChoice` directly with a
Technique definition read from the real nested `ruleset.techniques` structure,
which is sufficient to prove TD-20's own fix but does not exercise the button a
player would actually click.

**Closed 2026-08-04.** `app.js` gained `techniquesForFacet(facetId)` and
`allTechniques()` — one flattener over the real nested tree, shared rather than
re-derived three times. `renderBuilderTechniques`, `selectTechnique`, and
`techniqueDisplayName` all use it. Covered by
`test_available_technique_list_is_populated` and
`test_technique_display_name_resolves_from_the_real_tree`, which assert against
the rendered panel and the live function rather than a stub.

---

## ~~T10 — `skill_advanced` never tells the client a Technique pick was earned~~

**Source:** discovered while implementing TD-20
(`docs/TASKS_technique_difficulty.md`), 2026-08-02.

**What's wrong.** `Character.advance_skill` correctly increments
`technique_picks_available` server-side when a rank advance crosses a Facet's
5-advance level threshold (`app/game/character.py:324`). But the `skill_advanced`
broadcast built in `_handle_skill_advance` (`app/api/websocket.py`) never includes
`technique_picks_available`, and `app.js`'s `case 'skill_advanced'` handler never
applies it to `state.character` even though it does apply `new_rank` and
`new_facet_level`. A player who levels a Facet via the MM's "Advance Skill"
control sees their rank and Facet level update live, but the Technique-pick
counter silently stays at its old value until the next full page load /
reconnect (`onStateReceived`), which fetches the true server value.

**Why not fixed here.** Out of TD-18/19/20's scope (none of the assigned files
are `_handle_skill_advance` or the `skill_advanced` client handler). Found only
because TD-20's e2e test needed a real Technique pick to exist before it could
exercise the picker at all; the test routes around it with a full page reload
(`player.goto(live_server)`) rather than trusting the incremental broadcast.

**Closed 2026-08-04.** The broadcast carries `technique_picks_available`; the
client applies it and re-renders the advancement panel. Covered by
`test_skill_advanced_broadcast_carries_the_technique_pick`.

---

## ~~T11 — `onTechniqueSelected` never applies the choice to `technique_choices`~~

**Source:** discovered while implementing TD-20
(`docs/TASKS_technique_difficulty.md`), 2026-08-02.

**What's wrong.** `Character.select_technique` correctly records
`self.technique_choices[technique_id] = str(choice)` server-side
(`app/game/character.py:402`), and the `technique_selected` broadcast carries
`choice`. But `onTechniqueSelected` (`app/static/js/app.js`) reads `msg.choice`
only to build a chat line — it never writes it into
`state.character.technique_choices`. A player who picks Weapon Mastery (blades)
sees "learned Weapon Mastery (blades)" in chat and the Technique itself appear in
their list, but `state.character.technique_choices.weapon_mastery` stays
`undefined` client-side until the next full reload. The same handler also sets
`state.character.magic_technique_active = true` unconditionally for *every*
Technique selection, not only magic-granting ones — a second defect in the same
function, same root cause (the handler was written for the domain-granting case
and never generalized).

**Why not fixed here.** Out of TD-18/19/20's scope (`app.js` is not in any of the
three tasks' file lists). TD-20's e2e test routes around it with the same
full-reload approach as T10.

**Closed 2026-08-04.** The handler now writes the choice into
`technique_choices` and only sets `magic_technique_active` when the Technique's
own definition grants magic — checked via `allTechniques()` against
`magic_granting` / `grants_secondary_domain` / `grants_prismatic_domain`. The
second defect mattered more than it looked: learning Weapon Mastery was telling
the Magic panel the character had unlocked full-scope magic.

---

## ~~T12 — `final_blow_confirm` is not bound to the Strike that offered it~~

**Source:** review of PR #21, 2026-08-03.

**What's wrong.** The commit handler re-checks only *unlocked* and *not used this
session*. The 7+ requirement and the Spark cost live in `_handle_strike`'s
advisory `final_blow_available` flag; the confirm handler holds no reference to a
roll, an outcome, or a pending offer. `final_blow_available: false` is a client
hint, not a server gate — so a stale toast, a replayed message, or a hand-crafted
one could commit a removal after a 6−.

**Why deferred.** The handler is MM-gated and the MM is the game's authority, so
this is a state-machine gap rather than a privilege escalation. Closing it means
holding pending-offer state per session, which is a small feature rather than a
patch.

**Closed 2026-08-04, corrected the same day after review.**
`GameSession.pending_final_blows` holds the open offers **keyed by attacker**
(tracker key + offer id). A Strike that offers Final Blow records one; a Strike
that requests it and fails clears that attacker's own; committing consumes it.
The confirm handler refuses anything without a matching live offer, and the offer
id — broadcast on the `strike_result` and echoed back by the client — is
**required**, pinning the confirm to *that* Strike.

Offers are cleared at `exchange_end`, `combat_end`, and `session_reset`, so one
cannot outlive the exchange that made it.

**Two things the first attempt got wrong**, both caught in review of PR #24:

- The offer was a single **session-wide** slot, so any Final Blow Strike
  overwrote or cleared whoever else's was open. Two characters can both hold the
  Technique; one player spending a Spark on a successful capstone Strike lost it
  because someone else swung and missed. That was a regression, not a
  pre-existing gap — the confirm succeeded before this work.
- Nothing cleared the offer at any lifecycle boundary, so one made in a previous
  combat — or a previous *session*, after once-per-session use was reset — was
  still committable. The original note claimed "a stale one cannot outlive the
  exchange that made it" and used that to argue against an expiry. The claim was
  false when written; the code now makes it true, which is why no timer is
  needed.

Covered by `test_confirm_without_an_offer_is_refused` and
`test_a_failed_strike_clears_any_standing_offer`. `test_mm_confirm_commits_the_removal`
was rewritten: it used to confirm without ever Striking, which is exactly the hole
this closes — the test was encoding the bug.

---

## T13 — The Technique step composes on three of six roll paths

**Source:** review of PR #21, 2026-08-03.

**What's wrong.** `apply_character_difficulty_step` is called from the strike,
generic-roll, and reaction handlers (DESIGN §2.6 named exactly those three).
Support, Maneuver, and contested rolls never call it. But the book prints
*Weapon Mastery* as "**Rolls** using your chosen weapon type", not "Strikes".

So Mordai Strikes with his sword at Standard and gets Easy; he Maneuvers with the
same sword in the same exchange and stays Standard. Same Technique, same weapon,
two labels, and nothing on screen explains the difference. *Steady Hand* has the
same shape: a Finesse lockpick sent as a `roll` steps, the same attempt sent as a
`contested_roll` does not. `weapon_type` is also only read by the strike handler,
so a generic roll with a blade can never fire *Weapon Mastery* at all.

**Why deferred.** It is a scope question, not a bug in what shipped: the design
deliberately named three call sites, and widening it touches three more handlers
plus the client fields that feed them.

**Done when:** either every roll path that can carry a Technique's trigger calls
the shared function, or the printed Technique text is narrowed to match the paths
that do — decided deliberately, not by default.
