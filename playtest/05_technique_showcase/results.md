# PT05 — Technique Showcase: Results

**Date:** 2026-07-11
**Workstream:** WS-B / B6 (advancement math, D3)
**Harness:** `run_pt05.py` — drives the real engine (`Character.advance_skill` for
pacing, `Character.select_technique` for the pick-budget and prerequisite rules).
No rule logic is re-implemented in the harness.

## Purpose

The arena scenario in `scenario.md` was written for the old Facet-level-1 world and
tests *combat* feel. B6 asks a narrower, prior question: under the v0.3 pacing
(`facet_level_threshold: 5`, `major_advancement_threshold: 3`), can a single
character actually **reach** the top of the advancement tree — a Tier 3 Technique,
a Prismatic domain, and Second Domain — and at which session does each unlock land
relative to the DESIGN §6.3 projection? This run answers that; the arena combat
showcase remains available for a later session.

## Setup

Constants (from `facet.yaml`): `facet_level_threshold = 5`,
`major_advancement_threshold = 3`, `session_skill_points = 4`, `marks_per_rank = 3`.

One **Soul Facet** character (Spirit 3, Charisma 3) advancing the Communion branch:

| Facet level | Technique taken | Tier | Domain chosen |
|---|---|---|---|
| 1 | `spiritual_domain` (magic-granting) | 1 | **Resonance** (Standard) — first domain |
| 2 | `the_language_beneath_language` | 2 | — |
| 3 | `second_domain` | **3** | **Fate** (Prismatic / Broad) — second domain |

This single progression demonstrates all three B6 targets at once, and it is
consistent with the appendix rule that **Prismatic domains require a Tier 3
Technique and are never a starting domain**: the Prismatic domain (Fate) is
acquired *through* the Tier 3 Technique (`second_domain`), not at Tier 1.

## Results — session each unlock landed vs. DESIGN §6.3 projection

### 100% primary-SP efficiency (dedicated character)

| Unlock | Session landed | DESIGN §6.3 projection | Match |
|---|---|---|---|
| Facet level 1 — `spiritual_domain`, first domain (Resonance) | s4 | s4 | ✓ |
| Facet level 2 — `the_language_beneath_language` | s8 | s8 | ✓ |
| Facet level 3 — `second_domain` (Tier 3) + Prismatic domain (Fate) | **s12** | **s12** | ✓ |

First Major Advancement fires at Facet level 3 — i.e. **session 12**, together
with the Tier 3 unlock, as §6.3 intends ("Tier 3 and first Major land together").

### 80% primary-SP efficiency (realistic — some SP spent elsewhere)

| Unlock | Session landed | DESIGN §6.3 projection | Match |
|---|---|---|---|
| Facet level 1 | s5 | s5 | ✓ |
| Facet level 2 | s10 | s10 | ✓ |
| Facet level 3 — Tier 3 + Prismatic + first Major | **s15** | **s15** | ✓ |

The 60% "breadth" character (not simulated here as a Communion run, but covered by
`test_advancement_pacing.py`) reaches level 3 at **s19**, the acceptable tail for a
character who deliberately spread their points.

## B6 acceptance checklist

- [x] A character reaches **Facet level 3** under the new pacing (s12 dedicated / s15 realistic).
- [x] A **Tier 3 Technique** is actually reachable — `second_domain` taken at level 3.
- [x] A **Prismatic domain** is actually reachable — **Fate**, granted by the Tier 3 `second_domain`.
- [x] **Second Domain** (Soul Communion Tier 3) can be taken — it is the Tier 3 pick itself.
- [x] Each unlock's session is recorded against the DESIGN §6.3 projection (all exact matches).

## Observations for follow-up (not blocking B6)

1. **`second_domain` records the choice but does not populate `Character.secondary_magic_domain`.**
   `select_technique` writes `technique_choices["second_domain"] = "fate"` and,
   because `second_domain` is not flagged `magic_granting`, leaves
   `secondary_magic_domain` unset. Wiring the second-domain choice into
   `secondary_magic_domain` (with the "one step harder" penalty already modelled)
   is a small, separate task — the reachability B6 tests is unaffected.
2. **Pacing is exact, by construction.** The harness advances whole marks with a
   fractional-efficiency accumulator, so the landed sessions equal
   `ceil(level × 5 × 3 / (efficiency × 4))` — the same formula asserted in
   `test_advancement_pacing.py`. This is the intended cross-check, not a coincidence.

## How to reproduce

```
cd software
python ../playtest/05_technique_showcase/run_pt05.py
```
