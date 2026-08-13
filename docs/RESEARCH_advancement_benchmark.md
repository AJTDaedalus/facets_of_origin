# RESEARCH — Advancement Pacing Benchmarked Against the Field

**Date:** 2026-08-09
**Trigger:** User observation that progression "feels weird — leveling a facet almost
every session and maxing out your facet when you get your first technique seems very
counterintuitive. This seems way too rapid and maximizing everything over hard choices."
**Status:** Findings only. The remedy is a Brain-tier call — see *Escalation*.

---

## 1. What our numbers actually are

Computed directly from `software/facets/base/facet.yaml` (`advancement:` block), not
from the prose:

| Input | Value |
|---|---|
| Skill points per session | 4 |
| Marks per rank advance | 3 |
| Primary-Facet cost | 1 SP per mark |
| Cross-Facet cost | 2 SP per mark |
| Facet level threshold | 5 rank advances |
| Major Advancement threshold | 3 Facet levels |
| Skills per Facet | 5 |
| Rank advances per skill | 3 (Novice → Practiced → Expert → Master) |

Derived:

| Milestone | Advances | SP | Sessions (all points on primary) |
|---|---|---|---|
| Facet level 1 (first Technique) | 5 | 15 | **3.75** |
| Facet level 2 | 10 | 30 | **7.5** |
| Facet level 3 + first Major Advancement | 15 | 45 | **11.25** |
| One skill Novice → Master | 3 | 9 | **2.25** |

**The primary Facet's ceiling is 15 advances — and Facet level 3 is at 15 advances.**
Those are the same number. Reaching the top Facet level and mastering every skill the
Facet has are not two achievements; they are one event.

### The observation, corrected and sharpened

Facet levels do not arrive "almost every session" — the floor is one per **3.75**
sessions. But the second half of the observation is exactly right, and is the more
serious problem:

**There is no opportunity cost on skills.** Fifteen advances buys the entire primary
Facet. A player never chooses *between* skills, only the order they buy them in. Every
character who plays ~11 sessions in one Facet arrives at the identical sheet: five
skills at Master. The differences between two Body characters at that point are their
attributes, their Background, and their three Techniques — nothing the advancement
system did.

### A related soft inconsistency

`MM3–2: Advancement Thresholds` publishes Facet level 1 at "sessions 4–8" and Facet
level 3 at "sessions 12–20." The mathematical floor is 3.75 and 11.25. The table
describes a player splitting points across Facets; it does not state the fastest legal
line, and a table optimising will beat the book's stated earliest by a session at every
threshold. Worth a footnote whatever else changes.

### What is already working

The **Technique layer is well designed and should not be touched.** Each Facet carries
18–20 Techniques (Body 18, Mind 20, Soul 19) across three branches, and the primary
Facet grants exactly **3** picks — one per Facet level. Tier 2 requires a Tier 1 in the
same branch and Tier 3 requires a Tier 2, so reaching a Tier 3 Technique costs you all
three picks in a single branch. That is a genuine, exclusive, irreversible choice, and
it is the only place in the system where one currently exists.

The magic-granting Background makes this sharper still: your level 1 pick is spoken
for, so your Tier 3 has to live in that same branch or you never reach one.

---

## 2. How the field handles this

The question is not "how fast" — it is "what stops you having everything." Every system
checked has an answer. We do not.

**Apocalypse World** (PbtA, the tradition our 2d6 core comes from). Improvements cost 5
XP each; a playbook is designed around roughly 12 improvements before a character moves
to endgame options, and the first five must come from a restricted list. The menu is
larger than the picks. You leave things on the table permanently.

**Savage Worlds Adventure Edition.** Four Advances per Rank, five Ranks — 20 Advances
from Novice to Legendary. Each Advance is *one* pick from a menu (raise an attribute,
raise two skills, take an Edge). The menu never empties; a Legendary character is a
character who made 20 exclusive choices, not one who bought everything.

**Call of Cthulhu 7e** — structurally the closest relative we have, and the most
instructive. Its improvement loop is nearly identical to ours: mark the skills you
used, resolve improvement at the end of the scenario. The difference is the brake. You
roll d100 and must roll **over** the skill's current value to improve it. A skill at 45%
improves 55% of the time; a skill at 80% improves 20% of the time. Mastery *asymptotes*
— the closer you get, the slower you go, and nobody ever finishes the sheet.

**D&D 5e.** Class features are largely fixed, but the exclusive choice is preserved
where it matters — an Ability Score Improvement and a feat compete for the same slot,
and subclass is a one-time fork. You cannot hold two subclasses.

### Where that leaves us

Our *rate* is defensible. Eleven sessions to the top of one Facet is comparable to
SWADE's 20 Advances or AW's ~12 improvements, and Facets is explicitly a
low-complexity, fast-onboarding game — brisk is on-brand.

Our *shape* is the outlier. Facets is the only system on this list whose advancement
track **terminates in total completion**. Everyone else either asymptotes (CoC), or
offers a menu wider than the number of picks (AW, SWADE), or forks exclusively (5e).
We do all our exclusion in the Technique layer and none of it in the skill layer, and
the skill layer is the one players touch every single session.

That is the mechanism behind "maximizing everything over hard choices." It is not a
pacing bug. It is a missing constraint.

---

## 3. The shape of a fix (options, not a recommendation)

Each of these adds opportunity cost to the skill track without disturbing Techniques.

**A. Escalating mark cost per rank tier.** Novice→Practiced stays 3 marks;
Practiced→Expert costs 5; Expert→Master costs 8. One skill to Master becomes 16 marks
instead of 9. Full Facet mastery moves from 45 SP (11 sessions) to 80 SP (20 sessions),
and — more importantly — a player choosing to push one skill to Master is visibly
declining to raise two others. This is CoC's diminishing return expressed in our
currency, and it needs no new concepts at the table.

**B. Cap Masters per Facet.** At most one or two skills in a Facet may reach Master.
Crisp, immediately legible, and creates a real "which one is *the* thing I am best at"
moment — but it is an arbitrary wall rather than a curve.

**C. Decouple Facet level from advance count.** Facet levels currently fall out of skill
purchases automatically, which is why level 3 and total mastery coincide. Tying levels
to something else (career advances across all Facets, or story milestones) separates the
two milestones.

**D. Widen the Facet.** More than 5 skills per Facet, so 15 advances no longer buys
everything. Largest blast radius — touches II.6, all three Facet chapters, `facet.yaml`,
and the skill tables.

**A** is my read of the best value-to-disruption ratio: it is one table change in
`facet.yaml`, it preserves every existing concept, and it converts the flat track into a
curve the way the closest comparable system already does.

---

## 4. Addendum — the cross-training incentive runs backwards

**Question raised:** does going vertical (Tier 1 → 2 → 3 in one branch) require
cross-training, and don't most systems penalise primary-class unlocks for cross-training?

**Answer to the first: no, and the rules are correct as written.** A primary Facet grants
Technique picks at levels 1, 2, and 3. Tier 2 requires any Tier 1 in the same branch;
Tier 3 requires any Tier 2 in the same branch (`character.py:select_technique`, PHB
II.4). Three levels, three picks, one clean vertical. Nothing is cross-gated.

**The odd part is what that vertical costs, and what it forecloses.** Those three picks
are everything your primary Facet will ever grant. Each Facet carries 18–20 Techniques
across three branches:

| Facet | Branches | Techniques | Reachable on primary Facet levels alone |
|---|---|---|---|
| Body | Might / Grace / Iron | 18 | 3 |
| Mind | Clarity / Instinct / Archive | 20 | 3 |
| Soul | Presence / Fortune / Communion | 19 | 3 |

A vertical consumes all three, so a vertical character has **zero** breadth, and any
character who takes even one Technique outside their line can never reach Tier 3 at all
within their own Facet. Buying a fourth Technique from your *own* tree requires Facet
level 4, which the ruleset only reaches through another Facet — II.4 says so outright:
"Later Major Advancements... do require cross-training, since a single Facet caps at
level 3."

And `technique_picks_available` is a **single fungible pool**: `select_technique`
validates tier and branch but never checks that the Technique's Facet matches any Facet
you hold levels in. A level earned in Mind buys a Body Technique.

Put together: **cross-training is the only road to more of your own Facet's tree.**

### That is the inverse of the convention

The near-universal pattern is that breadth *costs* depth:

- **D&D 5e** — multiclass levels do not advance your first class, so its high-tier
  features arrive late or never. The dip is paid for in primary progression.
- **Pathfinder 2e** — archetype feats compete for the same slots as class feats.
- **D&D 3.5** — multiclassing delays every class's progression and can break prestige
  prerequisites outright.

In each, going wide is a sacrifice you make knowingly. In Facets, going wide is
*mandatory* for anyone who wants a fourth Technique, including one from the tree they
started in. The 2 SP-per-mark cross-Facet cost makes that road expensive (30 SP for a
cross-Facet level against 15 for a primary one) — but expensive is not the same as
optional. It is a toll on the only road, not a price for leaving the main one.

The design intent is stated and coherent — II.4's *Through the Mirror* box argues that
"at the highest levels, experts grow by absorbing adjacent disciplines." The tension is
that the Technique trees are *built* like browsable menus, 18–20 entries deep, and a
single-Facet character sees 3 of them (about 17%) before the tree closes.

### How this interacts with §3

This is the same root cause as the skill-track finding: **the primary Facet is a finite
checklist that completes.** Skills complete at 15 advances; Techniques complete at 3
picks; both land in the same session. Any fix that lengthens the skill track (§3 option
A, escalating mark costs) also spreads the three Technique picks over ~20 sessions
instead of ~11, which softens this without addressing it. Addressing it directly means
either decoupling Technique picks from Facet levels, or allowing a fourth+ primary level
that grants picks without granting skill mastery.

**Not resolved here** — it belongs in the same Brain decision below.

---

## ESCALATION — RESOLVED

**Question raised:** Should the skill track carry opportunity cost at all, or is
"everyone eventually masters their Facet" the intended feel?

**Ruling (user, 2026-08-09):** *"'Everyone masters their primary' is wrong. A lot of
different classes fall under each Facet — a ranger shouldn't be as good at hand-to-hand
as a barbarian."*

**The reasoning, and why it is the decisive argument.** A Facet is not an archetype; it
is a *category* of archetypes. Body holds the brawler, the scout, the duellist, the
acrobat. Under the current rules every one of them arrives at the identical sheet —
Athletics, Combat, Stealth, Finesse, and Endurance all at Master — in about eleven
sessions. The Facet therefore cannot express the difference between the archetypes it
contains, which is the one job a broad category most needs to do. This reframes §3: the
missing constraint is not primarily a *pacing* problem, it is an **identity** problem.
Opportunity cost is the mechanism by which a Body character becomes a *particular* Body
character.

This reverses the recorded choice in `DESIGN_v0.3_ruleset_revision.md §6.2`
(`facet_level_threshold: 5`, chosen so all three Facet levels fit inside the 15-advance
ceiling). That decision optimised for the three Facet levels landing tidily; it did not
weigh intra-Facet differentiation. Superseded — see `DECISIONS.md`.

**Consequence for §3's options.** Option A alone (escalating mark costs) is now known to
be insufficient on its own: it delays completion to ~20 sessions but the track still
*completes*, so a long campaign reconverges the ranger and the barbarian. Delivering the
ruling requires a genuine ceiling — option B, a cap on how many skills may reach the top
ranks — with option A supplying the cost curve underneath it. See the worked proposal in
`docs/DESIGN_advancement_differentiation.md` (pending).

*Resolved. Return to Planner to design the cap + cost curve, then to Worker for the
`facet.yaml` / engine / book changes.*

---

## Sources

- [Apocalypse World: Custom Advancement — lumpley games](https://lumpley.games/2022/05/28/apocalypse-world-custom-advancement/)
- [Apocalypse World — Wikipedia](https://en.wikipedia.org/wiki/Apocalypse_World)
- [Savage Worlds — Wikipedia](https://en.wikipedia.org/wiki/Savage_Worlds)
- ["Leveling" in Savage Worlds — Savage Tales of Eberron](https://www.savagetalesofeberron.com/leveling-in-savage-worlds/)
- [Rewards of Success — Call of Cthulhu RPG Wiki (Chaosium)](https://cthulhuwiki.chaosium.com/rules/rewards-of-success.html)
- [Skills in Call of Cthulhu 7th Edition — RPG Stack](https://rpgstack.com/rules/coc7e/skills)
- [Advancement — Blades in the Dark SRD](https://bladesinthedark.com/advancement)

**Sourcing caveat:** Blades in the Dark is structurally relevant (individually-advanced
action ratings plus a selective special-ability menu) but I could not confirm its exact
XP-track box counts or ability totals from an authoritative page, so it is not used as a
numeric comparison above.
