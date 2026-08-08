# RESEARCH — Mechanics Review: Fun & Ease of Play

**Date:** 2026-08-08
**Tier:** Brain (Fable) — synthesis of three parallel cluster reviews
**Yardstick:** Project philosophy (fun/socializing/worldbuilding/storytelling over rules
complexity/friction) + `research/dice_system_analysis.md` + MDA framing (mechanics →
table dynamics → target aesthetics: Fellowship, Narrative, Fantasy, Discovery).

## Status

- [x] Cluster review: Core resolution, skills, adventuring → `docs/RESEARCH_fun_review_core.md` (1 High, 5 Medium, 6 Low)
- [x] Cluster review: Combat & encounters → `docs/RESEARCH_fun_review_combat.md` (3 High, 6 Medium, 4 Low)
- [x] Cluster review: Magic, advancement, backgrounds, equipment → `docs/RESEARCH_fun_review_progression.md` (3 High, 6 Medium, 6 Low)
- [x] Cross-cutting synthesis (§1–§4)
- [x] Prioritized recommendations (§5)

**Total: 40 findings — 7 High, 17 Medium, 16 Low.** No finding requires a redesign.
Nearly every High is one to three sentences of rules text plus the same-commit
facet.yaml/engine sync the iron law already prescribes.

---

## 1. Overall verdict

**The fun architecture is sound and validated.** All three reviewers independently
confirmed that the game's central bets deliver the aesthetics they were designed for:

- The 2d6 three-tier engine is the research's Option A taught in one sentence, and
  modifier weight is deliberately small enough that the dice stay the star (dodging
  PbtA's documented stat-weight failure).
- Sparks are Option D implemented verbatim, and the earning channels — peer call,
  act-break nomination, Graceful Fail — are a Fellowship machine few published games match.
- Exchanges keep their "no waiting" promise: playtest-measured fights run 2–3 exchanges
  in 10–20 minutes, and the defender holds the dice on the enemy's "turn."
- Domain + Intent + Scope casting is a genuinely light three-decision loop that delivers
  wonder without a spell list, with the MM-burden problem (the classic freeform-magic
  killer) mitigated three separate ways.
- Conditions-instead-of-HP and the one-number Resolve model produce story on the PC side
  and near-zero tracking on the MM side.
- Equipment is the best subtraction-design chapter in the book, and character creation is
  20–30 minutes with no trap options.
- The project's feedback loops demonstrably work: every playtest Must-Fix landed, the
  armored-enemy bug was dissolved rather than patched, K1 is a sim-validated fun repair,
  and the Recipe Table is honestly labeled measured-vs-guessed.

**The problems are at the joints, not the centers.** The findings concentrate where
subsystems meet: where Sparks touch magic, where Techniques and Specialties both touch
difficulty, where PC-condition text is borrowed by enemies, where the Quick Start touches
combat. That is a very good place for a design of this maturity to be — joints are fixed
with sentences, centers only with redesigns.

## 2. Cross-cutting patterns (what no single cluster sees)

**P1 — The Spark economy is the single most overloaded joint in the game.** Sparks are
the one currency that crosses every subsystem, and each crossing added its own
conditional: session-start ambiguity feeding the playtest-confirmed hoarding problem
(core F2), an un-executable "pushing scope" rule referencing a ceiling that no longer
exists (progression F1 — High), and four magical sub-rules keyed to domain type and
Technique status where the rest of the game refuses to build conditional stacks
(progression F9). One rewrite fixes all three: Sparks reset to 3 each session; a Spark
improves the dice anywhere; a Spark buys reach in exactly two defined cases. The app
enforces eligibility silently.

**P2 — The difficulty-relabel layer is where all remaining ambiguity lives.** The flat
modifier layer is disciplined (2 chunks per roll, max +5/+6) and earned every reviewer's
credit. But *relabeling* difficulty has four uncoordinated sources — Technique step,
Specialty, rider Easy-tags, Maneuver/Support — with no stated stacking or precedence rule
(core F4, combat F8, and the dense taxonomy paragraph core F3). One unified rule, stated
once in III.1 and compressed onto the MM5 card, closes all three findings: *set the base
from the situation; an Easy tag overrides downward; at most one character-side step from
any source ever applies; the ladder's ends hold.*

**P3 — Stale text is a live drift risk the project has already been burned by.** Enemy
"Parry" remnants in III.3/MM1 contradict the settled no-roll model whose removal shifted
every recipe a full band (combat F1 — High); a superseded advancement-math research doc
is still listed as live reference (progression F15); Quick Start references terms the
document never defines (core F1 — High). The dual-implementation war story in MM5's own
box is the argument: fix these before someone rebuilds the drift from stale text.

**P4 — The flagship fantasy has a growth-curve hole.** Whether casting rolls take a
skill modifier is unstated, and the examples-as-written reading caps every mage at +1
forever while the fighter climbs to +4 (progression F2 — High). Downstream of that same
ambiguity: the Broad/Prismatic ladder re-imports at Tier 3 the exact roll-punishment
feel-bad the pre-Technique playtest removed (F3 — High), and Second Domain's permanent
penalty prices a standard domain like a prismatic one (F7). Ruling "skills apply"
substantially rehabilitates all three without touching the domain tables.

**P5 — Several rules exist only to police abuses no real table would attempt.** The
unspent-points forfeit (its own worked example demonstrates the feel-bad), the
dual-domain cross-Facet legalese, the disproven TR budget/multiplier tables surviving
wrapped in 40 lines of warnings, four-of-five mechanically-null rider options against
enemies. The Weary/Spent/Bleeding/Exposed knife applies to all of them.

**P6 — The digital layer's absorption is working, but three prescribed features are
unbuilt:** Spark-flow nudges for the MM, a live encounter-difficulty band display in the
encounter builder (the one-Mook-per-band cliff makes this safety equipment, not polish),
and the enemy posture tracker with auto-labeled reaction difficulty.

## 3. Resource & concept census (verified)

The draft census held up with corrections. Per-roll cognitive load is **2 chunks**
outside combat ("my number" + declared difficulty) — comfortably inside the research's
working-memory budget. A combat exchange on paper is ~10 tracked items of which 4–6 are
decisions; **with the app, everything but the decisions vanishes**, which is the design
intent, met (combat §3). Casting is 3 decisions + 1 memorizable lookup best case; the
worst case doubles to 6 decisions + 2 recalled exceptions *entirely because of the Spark
sub-rules* (progression §3) — confirming P1 as the load concentration point. The MM
tracks 1–4 items per enemy; the real MM cost is adjudication (improv), not arithmetic,
and the remaining reducible arithmetic is enemy-posture bookkeeping.

## 4. Consolidated cut list (fun lost: none)

1. TR budget table + action-economy multipliers (MM1-5, MM1-6, MM5 copy) — proven
   structurally non-predictive; demote to DECISIONS.md as history.
2. The "Pushing scope" paragraph as written (II.3) — un-executable; fold per P1.
3. Rider menu vs enemies → one "Open (Easy to Strike)" tag; fiction keeps the variety.
4. Technique trigger taxonomy out of III.1 → Facet chapters; III.1 keeps one sentence.
5. Advancement metadata + undefined combat terms out of Quick Start pregens/QS-4.
6. Unspent-points forfeit (II.4) — the abuse it prevents cannot occur at 4 pts/session.
7. `defense_modifier` on enemy stat blocks — no job; delete or give it its one sentence.
8. Career Advances off the paper sheet (keep in app); benchmark table to MM Manual.
9. Dual-domain cross-Facet paragraph → one sentence + MM discretion.
10. "Broad (Prismatic)" dual naming → one player-facing term.

Explicitly protected (small rules earning their keep): the four Spark earning channels,
Threat Clocks, the Normal: fields, the 6− template box, "Do You Have It?", the
pre-Technique scope cap, Secondary Skill marks, the three distinct Tier 1 conditions,
Dodge/Parry as separate identities.

## 5. Prioritized recommendations

**Tier 1 — before the next playtest (all are sentences + sync, except 1c which is a ruling):**

1. **(a)** Fix Quick Start's combat/save holes: Major Attribute line per pregen, resolve
   the spell fork per pregen, five-line combat primer or honest pointer to III.3, strip
   advancement metadata (core F1). **(b)** Purge stale enemy-Parry text from III.3 §Named
   NPCs and the MM1 `.fof` example, same-commit with facet.yaml (combat F1). **(c)** Rule
   whether skills apply to casting rolls — recommend **skills apply** (gives casters the
   same +0→+4 arc as everyone else, rehabilitates the Broad ladder and Second Domain
   pricing for free) — print one sentence in II.3, sync engine (progression F2).
2. **Unify the Spark economy** (P1): reset-to-3 sentence in III.1; rewrite II.3
   *Sparks and Magic* down to two rules; app nudges for stalled Spark flow.
3. **Print the one difficulty-precedence rule** (P2) in III.1 + MM5 card.
4. **Close the two sim-proven combat holes:** an uncontested-exchange escalation rule so
   Withdrawn cycling becomes the tempo trade the MM Note claims (combat F2), and the
   "one Mook = one difficulty band" warning in MM1 plus the live band display in the
   encounter builder (combat F3).

**Tier 2 — design decisions to weigh (each is real but survivable as-is):**

5. Soften the Broad ladder one cell or clarify dice-Sparks work there (progression F3);
   consider letting Second Domain's penalty expire at the next Facet level (F7).
6. Merge the enemy rider menu to "Open"; state who picks incoming Conditions and that
   type-repeat is the telegraphed kill move; give enemies a visible clear-the-rider
   action (combat F6, F7, F12).
7. Advancement friction pair: bank up to 2 points or let 1 point train an unused skill
   (progression F5); one sentence settling whether creation ranks count toward Facet
   levels (F6).
8. Feed the posture mind-game via conduct-field triggers so enemy postures vary by
   design; if they stay constant, drop the enemy-side blind reveal (combat F4/F10).
9. Downshift Never Surprised to warning-beat strength (progression F8); own the mage's
   forced first Technique in prose, or give the activator an internal Choose (F4).

**Tier 3 — polish:** apply the cut list §4 items not already covered; rename or
consistently qualify the Endurance pool (core F6); pick one of "offer vs narration
sequencing" for the 7–9 beat (core F7 — the offer reading adds meaningful choice for
free); ship 2–3 worked enemy Techniques that vary the incoming threat picture (combat
F9); the weapon-vocabulary join column (progression F14); supersession header on the
stale research doc (F15).

---

*Companion reports with full evidence and citations:*
`docs/RESEARCH_fun_review_core.md` · `docs/RESEARCH_fun_review_combat.md` ·
`docs/RESEARCH_fun_review_progression.md`

*Adopting Tier 1 items 1b/1c and several Tier 2 items implies engine/facet.yaml sync
work in the same cycle, per the Software-PHB sync iron law. This review changes no
rules text itself — it is Brain-tier assessment; adoption decisions belong to the user,
then Planner decomposition.*
