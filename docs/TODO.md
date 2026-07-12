# TODO — Open Follow-Ups

Running list of known-open work that is not yet a task in a `TASKS_<feature>.md`.
Items here are **deliberately deferred**, not forgotten: each one records what is
wrong, why it was not fixed in the pass that found it, and what "done" looks like.

When an item grows into real scope, promote it into a `TASKS_<feature>.md` and
strike it here with a pointer.

---

## T1 — PHB III.3 is silent on whether a redundant armor charge is spent

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

## T4 — `test_default_port_is_8000` reads the developer's real `.env`

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
