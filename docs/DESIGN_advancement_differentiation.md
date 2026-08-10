# DESIGN — Advancement Differentiation

**Tier:** Planner (Opus) output — hand to Worker
**Date:** 2026-08-09
**From:** `docs/BRIEF_advancement_differentiation.md` (Brain), ruling D16 in `docs/DECISIONS.md`

---

## The change in one paragraph

In each Facet, at most **three** skills may rise beyond Practiced, and only **one** of
those may reach Master. Marks per rank advance escalate: **3 / 5 / 8**. Because a
fully-developed Facet now yields 9 rank advances instead of 15, `facet_level_threshold`
drops **5 → 3**, keeping Facet levels (and all three Technique picks) at 3 / 6 / 9.

---

## Resolved open questions

### Q1 — Cap enforcement semantics

**Slot occupancy is claimed on commitment, not on arrival.** A skill occupies a
beyond-Practiced slot the moment it has any progress past Practiced, not when it
finishes the rank:

- `occupies_beyond_practiced` — rank is `expert`/`master`, **or** rank is `practiced`
  with `marks > 0`
- `occupies_master` — rank is `master`, **or** rank is `expert` with `marks > 0`

This removes the race where two skills bank marks toward the last slot and one of them
strands. It also reads correctly at the table: you claim the slot when you start
training past Practiced, not when you arrive.

**Refuse, never absorb.** `advance_skill` raises `ValueError` when the skill's next rank
is forbidden by the caps. No marks are added and nothing mutates — a mark must never
accumulate toward a rank the cap forbids, or a player banks into a wall.

**SP is validated before it is spent.** `spend_skill_point` currently deducts SP and
*then* calls `advance_skill`. That order would burn a point on a refused advance, so the
cap check moves ahead of the deduction. The WebSocket handler surfaces the message and
the point is not spent (refuse, don't refund).

`rank_ceiling_for(skill_id)` is the single public predicate; both `advance_skill` and the
handler read it, so there is one implementation of the rule.

### Q2 — YAML shape

```yaml
  marks_per_rank:
    practiced: 3
    expert: 5
    master: 8
  rank_caps:
    beyond_practiced: 3
    master: 1
  facet_level_threshold: 3
```

**Back-compat** (the `endurance` → `resolve` precedent): a bare integer
`marks_per_rank: 3` still loads, expands to all three tiers, and emits a
`DeprecationWarning`. `rank_caps` omitted entirely means uncapped, so a homebrew Facet
with a different skill count is not silently constrained by base's numbers.

### Q3 — MM3 recompute

Floors are exact; realistic ranges assume the same SP-efficiency spread the existing
MM3–2 uses. Career ceiling drops 45 → 27 advances, so MM3–3/MM3–4 re-band.

| Milestone | Advances | SP floor | Sessions floor | Realistic |
|---|---|---|---|---|
| Facet level 1 | 3 | 9 | 2.25 | 3–5 |
| Facet level 2 | 6 | 20 | 5 | 6–10 |
| Facet level 3 + first Major | 9 | 38 | 9.5 | 12–16 |

New career bands: 0–2 fresh · 3–5 developing · 6–9 shaped (primary complete) ·
10–18 cross-training · 19+ veteran.

### Q4 — UI

The Skill Advancement card gains one line per Facet: *"Beyond Practiced: 2/3 · Master:
0/1."* No new jargon. The printable sheet gets the slot boxes; the mark track needs
**8** boxes now, not 3.

### Q5 — Terminology

No coined noun. The books say it plainly: *"at most three skills beyond Practiced, one
of them Master."* Nothing new enters the Glossary except amended `Mark` and `Rank`
entries.

### Q6 — Training mark at completion

It idles. Once a Facet's shape is finished the training point has no legal primary
target and simply goes unspent — banking already covers the overflow. No new rule.

### Q7 — Acceptance gates

`test_advancement_pacing.py` pins the new floors (2.25 / 5 / 9.5 sessions, 38 SP full
shape, 27-advance career ceiling) and gains a **differentiation invariant**: two maximal
same-Facet builds can differ, and no build exceeds 1 Master / 3 beyond-Practiced.

### Q8 — Prismatic / caster check

Verified as a text check, not a code change: II.3's Prismatic ladder is keyed to domain
type and scope, never to the caster's skill rank, so a caster who leaves Attune or Lore
at Expert is unaffected mechanically. The Master slot is a genuine identity choice for
casters, and II.4 should say so in one line rather than leaving it as a trap.

---

## Blast radius and order of work

See `docs/TASKS_advancement_differentiation.md`. Engine and schema first (the books
quote numbers the engine must already produce), then tests, then books, then finding-aid
regeneration.

---

*Handed to Worker. Start at T1.*
