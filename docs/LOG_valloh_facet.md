# LOG — The Val'loh Setting Facet

**Design:** `docs/DESIGN_valloh_facet.md` · **Tasks:** `docs/TASKS_valloh_facet.md`
**Depends on:** `docs/LOG_lineage.md` (complete)

---

## V1 — the counted-novelty line

Written first. Every later task is read against it, and it goes into `V0` verbatim:

> *The core 2d6, Sparks, Conditions, exchanges, advancement, magic, and the three
> Facets are unchanged. Val'loh adds exactly: ten Lineages (two playable in Oraga
> Night), ten Gift domains, and crystal charges as one-use items. It removes
> nothing and it changes no rule.*

Three additions: **lineages, gift domains, items**. INV-17 (task V15) machine-checks
the counts in that sentence against the merged ruleset, so the pitch cannot drift
from the file. If any task finds itself wanting to write into `roll_resolution`,
`spark`, `advancement`, the `magic` rules, or `combat`, it is out of scope and
comes back to Planner.

## V9 — the Bond's reaction clause: **CUT**

The drafted clause (`BRIEF_valloh_facet.md` §5) let a Thenya invoke the Bond as a
reaction on a loved one's behalf — *Intercept's fiction without Intercept's
Endurance cost, at the Bond's difficulty*. DESIGN §2 ruling 4 said to simulate it
before it printed, because it is the one place a gift touches combat rules.

Standard harness (PS-3, n=200, seeds 1/2/3/7/42), modelled at its most generous:
a standing free Intercept-shaped reaction, refreshed each exchange.

| Row | Bond clause | Win | Median exch | Mean | PCs-Broken |
|---|---|---|---|---|---|
| Solo Archive Guardian | off | 100% | **3** | 2.68 | 0.079 |
| Solo Archive Guardian | **on** | 100% | **2** | 2.28 | 0.026 |
| Hard: 3 Named + 2 Mooks | off | 41.0% | 5 | 5.70 | 2.361 |
| Hard: 3 Named + 2 Mooks | **on** | **74.9%** | 5 | 5.76 | 1.635 |

It is Cover again, with a wider footprint. On the Boss it does exactly what Cover
did — median 3 back to **2**, undoing R2 — and on the Hard recipe row, where Cover
was inert, this one is not: **41.0% → 74.9%**, which takes a Hard fight past the
*Standard* band. One lineage's gift would have made every encounter in the module
a category easier.

**Verdict: the clause is cut. The Bond is an ordinary domain.**

Nothing is lost in the fiction, which is the test that matters. A Thenya can still
put themselves between a loved one and a blade — that is a Significant-scope Bond
working, declared and *rolled* at the Bond's difficulty, and it is exactly the
kind of thing the domain exists for. What is cut is the free, unrolled, always-on
version. `V2_Magic_of_Valloh.md` prints no rules note on the Bond, and the domain
entry in `facet.yaml` carries territory and beyond-the-focus only, like the other
nine.

**Pattern worth naming.** This is the third free-reaction mechanic measured in two
days (R3's Cover, the Guardian's old Reduced Mode, the Bond's clause) and the
second one cut. Free reactions do not read as defensive in this system: they
preserve Endurance, high Endurance drives aggressive postures, and aggressive
postures shorten fights. **Anything that waives a reaction cost should be assumed
to be an offensive buff until a simulation says otherwise.**

## 2026-09-09 — V1 through V17, complete

Full suite **1713 passed**, 0 failed (1676 before this workstream).

| Task | Status | Note |
|---|---|---|
| V1 counted-novelty line | ✅ | Written first; machine-checked by V15. |
| V2 schema | ✅ | `ItemDefinition`, `lineage_gift`, `draft`. 9 tests. |
| V3 items merge | ✅ | By id, with `_item_map`. 5 tests. |
| V4 ten lineages | ✅ | Krenn and Tyndi `playable: false`. |
| V5 ten gift domains | ✅ | All Focused, intuitive, `lineage_gift: true`, `draft: true`. |
| V6 six crystal charges | ✅ | All Minor consumables. |
| V7 gift filtering | ✅ | Gifts never appear on a Technique's domain list. 5 tests. |
| V8 `use_item` + event | ✅ | 6 model tests, 2 WS tests. |
| V9 **the Bond's clause** | ✅ | Simulated and **CUT** — see above. |
| V10–V13 book | ✅ | `settings/valloh/V0`–`V4`. |
| V14 retired canon | ✅ | Chapter VIII deleted; `01`, `03`, README repointed; no dangling reference. |
| V15 invariants | ✅ | INV-17 plus five siblings. 7 tests. |
| V16 inventions table | ✅ | `references/valloh/INVENTIONS_FOR_REVIEW.md`, eight sections. |
| V17 close-out | ✅ | IV.1 gained a *One-Use Items* section as the pattern's home in the core. |

### The bug this workstream found before it could bite

**`magic:` was a singleton section, replaced wholesale by the last module to declare
it.** The Val'loh Facet as briefed — "the merge appends them to the base list" —
would instead have *deleted* the core's twenty-one domains, both traditions, and
every domain type the moment it loaded. Nothing would have failed. The ruleset would
simply have come back empty of magic, and INV-7 would have compared an empty catalog
against an appendix and had nothing to say.

Fixed by splitting the section the way the spec's own vocabulary already does:
`soul_domains` and `mind_domains` are **collections** keyed by id, like `skills`;
everything else in `magic` stays **singleton**. The rules half also needed
field-level merging via `model_fields_set` — a setting that lists domains and says
nothing about traditions is not asking for traditions to be blank, but a bare
`model_copy` of its magic block says exactly that, because every field it left alone
is sitting at a schema default. Seven tests, including a regression guard that
`base` alone still yields 12 soul and 9 mind domains.

**Generalisable:** any schema section that mixes rules with catalogs has this bug
latent in it. `combat` is the next candidate — it holds `conditions` and
`strike_riders` (catalogs) beside `endurance` and `enemy_durability` (rules).
Nothing needs it today because no setting Facet writes into `combat`, and INV-17
now forbids Val'loh from doing so. Worth fixing the first time one wants to.

### The pattern V9 confirms

Three free-reaction mechanics measured in two days — R3's Cover, the Guardian's old
Reduced Mode, the Bond's clause — and two of the three cut. **Free reactions do not
read as defensive in this system.** They preserve Endurance; high Endurance drives
`choose_pc_posture` aggressive; aggressive postures shorten fights. Anything that
waives a reaction cost should be assumed an offensive buff until a sim says
otherwise.

**Resolved. Return to `TASKS_oraga_rewrite.md` O1 — all three dependencies are met.**
