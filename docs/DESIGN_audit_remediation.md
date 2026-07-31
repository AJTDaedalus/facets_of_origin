# DESIGN — Completeness Audit Remediation

**Tier:** Planner (Opus) output — hand to Worker (Sonnet)
**Date:** 2026-07-30
**Input:** `docs/BRIEF_audit_remediation.md` (decisions D1–D12 all resolved)
**Finding inventory:** `docs/RESEARCH_completeness_audit.md` + the five detail reports
**Companion files:** `docs/TASKS_audit_remediation.md`, `docs/DECISIONS.md`, `docs/LOG_audit_remediation.md` (Worker creates on first task)
**Branch context:** `main`, clean working tree apart from the untracked audit docs and the untracked `adventures/`, `references/oraga_night/`, `playtest/07_*`, and two `run_oraga_night_playtests*.py` tools.

---

## 1. Survey Findings

Eight facts established by reading the repo, not assumed from the reports. Four of them change the shape of the work the BRIEF describes.

**S1 — `facet.yaml` gives Guild Apprentice a *third* Specialty variant.**
`software/facets/base/facet.yaml:1424` reads:
> `specialty: "Formal training in a structured discipline — can identify when methods, materials, or approaches follow an established tradition versus improvisation."`

The sync audit recorded Background specialties as "✓ all … specialties" because it compared yaml against II.5 — and II.5's Guild Apprentice has no Specialty line to disagree with (rules-H1). So D4 is a **three-way** propagation (II.5 ← Quick Start text, and `facet.yaml` overwritten to match), not the two-way one the BRIEF describes. The yaml text is *not* user-established canon in the way `Quick_Start.md:36` is; D4 names the Quick Start text as the winner, so the yaml string is replaced, not merged.

**S2 — The test baseline is 1026, not 613.**
`python -m pytest --collect-only -q` on `main` collects **1026 tests**. README's "613 tests" (twice: features list and project tree) is stale by ~413. Every wave re-derives the number rather than copying it; W1 fixes the README with the count measured at that commit.

**S3 — INV-2 hard-binds the character sheet to the `Character` model, and every field D7 needs already exists.**
`software/tests/test_docs_consistency.py:173` (`CHARACTER_SHEET_FIELDS`) maps each sheet label to a `Character` attribute and fails if either side drifts. On the model side, D7's new fields are all already present: `endurance_current:117`, `armor:120`, `armor_downgrades_remaining:121`, `conditions`, `magic_domain:96`, `inventory:112`, `career_advances:82`. **One gap:** there is no stored Endurance *maximum* — `endurance_max()` (`character.py:202`) is a ruleset-dependent method, and `endurance_max_base` is a plain `@property` (not a Pydantic computed field), so neither is visible to INV-2. Design ruling: the sheet's Endurance row is labelled so that it maps to `endurance_current`; the maximum is written on the sheet as a player-computed value from the printed formula, and **no stored max field is added to the model** (it is derived, and storing it would create a second source of truth). D7 must update `CHARACTER_SHEET_FIELDS` in the same commit as the appendix, or the suite goes red.

**S4 — INV-4 makes `Index.md` a same-commit obligation for a large share of Wave 1 and Wave 3.**
`test_index_is_up_to_date` requires `Index.md` to be byte-identical to a fresh `python -m tools.build_index` run. The Index is generated from the Glossary term list and from headings in both books. Therefore **any** task that adds a Glossary entry, renames a heading, or fixes the slugger must regenerate `Index.md` in the same commit. The slugger fix alone moves 33 anchors. Wave 1 sequences all Glossary/heading work *before* the slugger fix so the regeneration happens on settled content, but each intermediate task still regenerates (the invariant does not permit deferral).

**S5 — `CombatDef.press` already exists in the schema; the yaml key does not.**
`software/app/facets/schema.py:376` declares `press: dict[str, Any]`. So sync M-2 (Press cost) is a yaml key plus a `websocket.py:528` de-hardcode, with only an optional typed-model upgrade — the cheapest of the twelve sync items, and a good first Wave 4 task.

**S6 — New yaml blocks need Pydantic models, not free dicts.**
The schema is typed per the project's established pattern (`EnduranceDef`, `ArmorDef`, `ArmorEntryDef`, `EnemyDurabilityDef`, `StrikeDepletionDef`). Wave 4's twelve encodings each need: a yaml block, a schema sub-model on `CombatDef`/`MagicDef`/`RollResolutionDef`, a `test_facets_schema.py` case, and — where the engine reads it — the engine change plus behavioural tests. Adding raw `dict[str, Any]` fields is a shortcut this design rejects, except where the BRIEF's D11 explicitly caps depth at "encoding only" and no engine path consumes the block.

**S7 — README's factual claims are wrong in seven distinct places, and one of them is timing-sensitive.**
Verified against canon: skills are **15**, not 24; domains are **21** across **two** traditions (Resonance/Mind, Channeling/Soul — Body magic deferred), not "27 domains across three traditions"; Harbor Thug is **TR 2** per D2, not TR 1; Archive Guardian is **TR 17**, not TR 16; tests are 1026, not 613; `playtest/` holds **six committed** directories (`01`–`06`) with `07_oraga_night_playtests` still untracked, not "Two". The TR 2 claim is decided at Brain tier (D2) but is not yet true of MM1 until Wave 2 lands — W1 states the decided value and the W1 PR description says so explicitly.

**S8 — The audit docs themselves are untracked.**
`docs/BRIEF_audit_remediation.md`, the five `RESEARCH_audit_*.md` files, and `RESEARCH_completeness_audit.md` are untracked on `main`. Every wave's PR description cites finding IDs in those files, so they must be committed first (task W0-1) or the citations point at nothing for a reviewer. The other untracked trees (`adventures/`, `references/oraga_night/`, `playtest/07_*`, `software/tools/run_oraga_night_playtests*.py`) are **out of scope** — do not stage them, and do not count `playtest/07` in the README playtest figure.

---

## 2. Architecture

### 2.1 Four waves, four branches, four PRs

| Wave | Branch | Theme | Canon risk | Depends on |
|---|---|---|---|---|
| W0 | `docs/audit-remediation-plan` | Commit the audit corpus + this DESIGN/TASKS pair | none | — |
| W1 | `fix/audit-wave1-corrections` | Mechanical corrections; no canon judgment | low | W0 |
| W2 | `fix/audit-wave2-v03-migration` | Finish the v0.3 migration; D2; yaml H-1/H-2 | medium | W1 (README states the D2 value W2 makes true) |
| W3 | `feature/audit-wave3-canon` | D3–D10 canon-decision items; new canonical prose | **high** | W2 (D5 touches III.3 text W2 also edits) |
| W4 | `feature/audit-wave4-sync` | The twelve Medium yaml gaps per D11 | medium | W3 (D8's rule is encoded here; D5's floor rule is verified here) |

Waves are strictly sequential: each branches from `main` **after** the previous PR merges. The ordering is a dependency, not a preference — W3 writes body text that W4 encodes, and W2 rewrites III.3 paragraphs that W3's D5 clarification sits beside. Rebasing a later wave onto an unmerged earlier one is the escalation trigger, not the workaround.

### 2.2 Propagation discipline (the iron rule, made concrete)

Every rules-touching task carries a **propagation set** — the full list of files that must agree after the change. The Worker does not get to decide the set; it is written into the task. The canonical set for a combat rule is:

```
player_handbook/III.3_Combat.md   (body text)          ← the source
player_handbook/III.3_Combat.md   (in-chapter quick ref)
mm_manual/MM5_Quick_Reference.md
player_handbook/Quick_Start.md    (if the rule appears there)
player_handbook/Glossary.md       (if the term is glossed)
software/facets/base/facet.yaml
software/app/game/*.py + software/app/api/websocket.py (if the engine reads it)
software/tests/*                  (tests before or with the change)
player_handbook/Index.md          (regenerate if any heading or Glossary term moved)
```

All of it in **one commit**. A task that cannot complete its whole propagation set is blocked, not partially done.

### 2.3 Where new canonical prose lands (D3, D8, D10)

Three tasks write rule text that does not exist anywhere today. Their homes, decided here per D3's "Planner picks":

- **Trouble Table** → `mm_manual/MM2_Session_Design.md`, in the **Improvisation** section. It is a mid-scene consequence-generation aid; MM2 is where scene-running lives, and MM2 already hosts the 3-Clue Rule in that same section. MM1 was considered and rejected — MM1 is enemy/encounter *construction*, and the table is not encounter-specific.
- **"Unnarrated details"** and **"Can I try again?"** → `player_handbook/III.1_Core_Resolution.md`, appended to the existing "when to call for a roll" material (III.1:129). Both are player-facing resolution rules, not MM-only craft; III.1 is where the roll-or-don't rules already live.
- **"Adjudicating Magic"** → `mm_manual/MM2_Session_Design.md`, new top-level section (D10). No new MM chapter.

Each of these three gets **flagged in its PR description for explicit user sign-off** (D12), and each is compressed into MM5 *after* the body text exists, never before.

### 2.4 Wave 4 depth ladder (D11, restated as a build rule)

| Item | yaml | schema model | engine | WS event | tests |
|---|---|---|---|---|---|
| M-8 saving throws | ✓ | ✓ | ✓ | ✓ | behavioural |
| M-2 Press cost | ✓ | ✓ | ✓ (de-hardcode `websocket.py:528`) | existing | behavioural |
| M-3/4/5/6/7 combat rules | ✓ | ✓ | read yaml instead of literals | existing | behavioural |
| M-9 Spark scope fuel (+ D8) | ✓ | ✓ | ✓ (`engine.py:230-256`) | existing | behavioural |
| M-1 First Move | ✓ | — (description fix) | — | — | text assertion |
| M-11 contested rolls | ✓ | ✓ | — (handler exists) | — | schema only |
| M-10 group rolls | ✓ | ✓ | — | — | schema only |
| M-12 weapon table | ✓ | ✓ | — (engine stays permissive) | — | schema only |

"Engine: read yaml instead of literals" is the whole point of M-3 through M-7 — the rules are already implemented correctly in `combat.py`; what is missing is that the numbers and tiers live as Python literals rather than as yaml the engine reads. These tasks must not change behaviour. Their tests are characterization-style: same outcomes, sourced from data.

---

## 3. Finding → Wave Traceability

All 81 findings plus the README audit. Report prefixes: `cre` = `RESEARCH_audit_phb_creation.md`, `rul` = `_phb_rules.md`, `app` = `_phb_apparatus.md`, `mm` = `_mm_manual.md`, `sync` = `_software_sync.md`.

### Wave 1 (mechanical)
| Finding | Task | Decision |
|---|---|---|
| cre-H1 point-buy "net zero" | W1-2 | — |
| cre-H2 II.3:246 "each Facet's tree" | W1-3 | D1 |
| cre-H3 Glossary:90 "each Facet's tree" | W1-3 | D1 |
| cre-M1 Scholar "Strong in Luck" | W1-2 | — |
| cre-M2 Soul Second Domain prereq | W1-4 | — |
| cre-M4 II.3:93 nonexistent Techniques | W1-3 | — |
| cre-M5 Zulnut Finesse + II.4:116 Knowledge→Lore | W1-5 | — |
| rul-M4 Threat Clock vignette (3 of 4) | W1-6 | — |
| rul-M5 72% → "3–4 rolls" | W1-6 | — |
| rul-L1 Named NPC rider tier | W1-7 | — |
| rul-L2 IV.1 armor Technique promise | W1-7 | — |
| rul-L3 Quick Start Graceful Fail mislabel | W1-7 | — |
| rul-L6 Mordai Weapon Mastery grounding | W1-7 | — |
| mm-M1 MM5 Maneuver direction | W1-7 | — |
| app-M5 Glossary missing "Saving Throw" | W1-8 | — |
| app-L1 Glossary citation format | W1-8 | — |
| app-L2 / cre-L4 dual-home citations | W1-8 | — |
| app-L3 Tier 1 Condition glossary entries | W1-8 | — |
| app-L4 Pinnacle/Party Strength/weapon terms | W1-8 | — |
| app-M6 Index slugger (33 anchors) | W1-9 | — |
| cre-L1 "same structure as Soul" | W1-10 | — |
| cre-L2 Body-magic forward pointer | W1-10 | — |
| cre-L3 Ascendant-once-only in tree entries | W1-10 | — |
| cre-L5 duplicate II.3 pointer sentence | W1-10 | — |
| cre-L6 / app-L6 ToC titles & appendix letters | W1-10 | — |
| README (7 stale claims) | W1-11 | D2 (TR value) |

### Wave 2 (v0.3 migration)
| Finding | Task | Decision |
|---|---|---|
| mm-M2 + III.3:379/391 magic → Resolve | W2-1 | — |
| rul-M2 quick-ref invents Magic/Withdraw actions | W2-2 | — |
| mm-M4 enemy Attack/Defense modifier semantics | W2-3 | — |
| mm-H1 Mook TR four-way contradiction | W2-4 | **D2** |
| mm-M5 MM1:411 superseded sim citation | W2-5 | — |
| mm-L4 MM2:165 Skirmish by TR budget | W2-5 | — |
| mm-L5 `veteran_soldier.fof` stale note | W2-5 | — |
| mm-L1 MM3 advancement double-count | W2-6 | — |
| mm-L6 MM1 "(see *Armor*, above)" | W2-6 | — |
| mm-L7 MM1 "three things" vs 4 steps | W2-6 | — |
| sync-H-1 Overwhelming Force stale in yaml | W2-7 | — |
| sync-H-2 Technique prerequisite model | W2-8, W2-9 | — |

### Wave 3 (canon decisions)
| Finding | Task | Decision |
|---|---|---|
| rul-H1 Guild Apprentice Specialty (+ S1 yaml) | W3-1 | **D4** |
| app-H1 sheet: Endurance/Armor/Conditions | W3-2, W3-3 | **D7** |
| app-H2 sheet: magic domain | W3-2, W3-3 | **D7** |
| app-M1 sheet: "or Domain Origin" | W3-2, W3-3 | **D7** |
| app-M2 sheet: "marks toward next level" | W3-2, W3-3 | **D7** |
| app-M3 sheet: inventory | W3-2, W3-3 | **D7** |
| app-M4 sheet: Career Advances | W3-2, W3-3 | **D7** |
| rul-M1 + rul-L4 0-Endurance absolute | W3-4 | **D5** |
| rul-M3 Reckless Press | W3-5 | **D6** |
| cre-M3 pushing scope | W3-6 | **D8** |
| mm-L8 MM5 omits pushing-scope | W3-6 | D8 |
| app-M7 Shattered Origin promise + ToC | W3-7 | **D9** |
| mm-M3 Trouble Table + 2 Common Rulings | W3-8, W3-9 | **D3** |
| mm-M6 MM magic adjudication | W3-10, W3-11 | **D10** |
| mm-L9 Specialty / hazards / death coverage | W3-11 | D10 |
| mm-L2, mm-L3 MM5 Spark drift | W3-12 | — |
| cre-M6 II.4a missing Facet intro | W3-13 | — |
| cre-M7 Communion Tier 3 asymmetry | W3-14 | ruled as-designed |
| rul-L5 Survival granted by no Background | W3-14 | ruled as-designed |

### Wave 4 (sync)
| Finding | Task |
|---|---|
| sync-M-2 Press cost | W4-1 |
| sync-M-3 Strike riders / Easy-to-Strike | W4-2 |
| sync-M-4 same-Tier-2 → Broken | W4-3 |
| sync-M-5 armor/reaction non-stacking | W4-4 |
| sync-M-6 enemy attack tiers + posture | W4-5 |
| sync-M-7 Maneuver / Support | W4-6 |
| sync-M-8 saving throws + Major derivation | W4-7, W4-8 |
| sync-M-9 Spark scope fuel (+ D8) | W4-9 |
| sync-M-10 group rolls | W4-10 |
| sync-M-11 contested rolls | W4-10 |
| sync-M-12 weapon → attribute table | W4-11 |
| sync-M-1 First Move timing | W4-12 |
| sync-L-1…L-8 | W4-13 (opportunistic) |

**Not fixed, logged as accepted:** app-L5 (ToC IV.2 "(Planned)" — correct as-is, informational only).

---

## 4. Per-Wave Design Notes

### 4.1 Wave 1

The only wave with no canon exposure. Two things make it non-trivial anyway:

**Ordering around the Index.** Do Glossary content (W1-8) before the slugger (W1-9), so the 33-anchor regeneration happens once on final content. Every task in between that touches a heading still regenerates.

**Vignette arithmetic is load-bearing.** Three fixes (cre-H1, cre-M5, rul-M4/M5) are worked examples a reader uses to check their own understanding. The Worker recomputes rather than patching the visible number:
- cre-H1: the legal replacement is *four at 3, four at 1, one at 2* = 18 (4 spent, 4 saved, 1 at baseline). Do not keep the "three at 2" shape — it cannot be made legal with four 3s.
- cre-M5: II.4's advancement examples must not advance Finesse Novice→Practiced (canon: Practiced at creation, `characters/Zulnut.fof`). The clean swap is **Stealth**, which Zulnut holds at Novice with 1 Background Mark — recompute the whole example including the Background Mark rule (II.5:43) and the "unspent points are lost" line (II.4:53) before writing a number.
- rul-M5: keep the 72% figure (it is derived from the outcome table) and fix the conclusion — 4 ÷ 0.72 ≈ 5.6, so "five or six party rolls". rul-M4 adds the missing fourth advance beat to the vignette rather than redefining "restarting".

**cre-M1 fixes the prose, not the stat line** — the Scholar's point total balances at 18 only as written, so "Strong in Luck" is the error. Surgical: the clause loses its "Strong" claim and keeps its voice.

### 4.2 Wave 2

**W2-1 is the wave's spine.** `III.3:379` (Magic in Combat) and `III.3:391` (Attune) are the last two paragraphs still resolving enemy damage in Condition tiers. The correct target model is already stated three places away (`III.3:124` Strike, `MM5:109`): against an enemy, 10+ depletes 2 Resolve and may hang a rider; 7–9 depletes 1; against another character the PvP tier table applies. The migration must **not** introduce a magic-specific number — magic uses the Strike table, full stop. That is what makes MM5's existing line a legal compression afterwards.

**W2-3 (mm-M4) is the one Wave 2 item with a canon-adjacent judgment.** MM1's stat-block note says the Defense modifier is "used for Parry", which cannot be true under "NPCs do not roll dice" (III.3:331). The fix states only what III.3 already rules: attack/defense modifiers are **authoring inputs** — they feed the TR formula and the simulator, and they inform the difficulty the MM sets for PC Strikes and reactions (III.3:114, :335–355). Nothing new is invented. Flag it in the PR anyway; it is the only Wave 2 line a reader could mistake for a new rule.

**W2-4 (D2) has a wide blast radius.** Three MM1 sites (`:55`, `:121`, `:293`), the `harbor_thug.fof:29` note, and any encounter recipe, budget worked example, or test that assumes Harbor Thug = TR 1. The Worker greps for `TR 1`, `tr: 1`, and `harbor_thug` across `mm_manual/`, `enemies/`, `spec/`, `playtest/` (committed dirs only), and `software/tests/` before editing, and reports the full hit list in the LOG. MM1:127's "minimum 1" floor text **stays** — it is still correct for attack −2 (offense 0). The chicken remains the TR-1 baseline and must not be renamed.

**W2-8/W2-9 (sync-H-2) is the riskiest software change in the whole cycle** and is deliberately split in two: encode first (W2-8: schema + yaml + the explicit domain prerequisite that the chain-based model was silently providing), then enforce (W2-9: `character.py:338` switches from a literal prerequisite list to the branch/tier rule). Splitting matters because the sync report's own note is the trap — Second Domain and Ascendant Domain's "requires an existing domain" prerequisite is currently satisfied *only* as a side effect of the strict chain. Loosen the chain without encoding the domain requirement first and the game silently permits a second domain with no first. W2-8 lands the guard; W2-9 removes the chain.

Test shape for W2-9, per the BRIEF's robustness note — both directions:
1. Weapon Mastery (Might Tier 1) → Overwhelming Force (Might Tier 2) **now legal** (was rejected).
2. The mirror case in a second branch, and in a second tree.
3. Tier 2 with **no** Tier 1 in that branch → still rejected.
4. Tier 1 in branch A → Tier 2 in branch B → still rejected.
5. Tier 3 with only Tier 1 in the branch → still rejected.
6. Second Domain with no existing domain → rejected (this is the guard from W2-8).
7. Second Domain with an existing domain → legal.

### 4.3 Wave 3

**D7 (W3-2/W3-3) is spec-then-artifact.** II.1's six-section table is the specification; the appendix binds itself to it in its own first line ("Every field below is one II.1 already named; nothing here is new"). So II.1 changes first (W3-2), then the appendix mirrors it plus the INV-2 mapping (W3-3). The amended shape:

| Section | Change |
|---|---|
| Attributes | unchanged |
| Facet | relabel "Advancement Track (marks toward next level)" → **rank advances** toward the next level (app-M2); add **Career Advances** (app-M4) |
| Background | Secondary Skill row becomes "Secondary Skill (Novice, 1 mark) **or Domain Origin**" (app-M1) |
| Skills | unchanged |
| Techniques | unchanged |
| **Magic** *(new)* | Domain name, type (Focused/Standard/Broad), and pre-Technique Minor-only flag (app-H2) |
| **Combat** *(new)* | Endurance (current / max, with the printed formula), Armor type + downgrade budget, Conditions track (app-H1); **Sparks moves here from Session Resources** |
| **Inventory** *(new)* | equipment list, incl. the armor whose type drives the budget (app-M3) |
| Session Resources | keeps Skill Points; loses Sparks |

Counts to update in the same commit: II.1:11 "six sections" → nine; `Appendix_Character_Sheet.md:3` "six sections" → nine. Per S3, the Endurance row maps to `endurance_current`; no new model field. The web app's read-only sheet (`software/app/static/js/tools.js`) is checked for parity and updated only if it renders a section list — a rendering gap is a separate task, not a silent extension of this one.

**D5 (W3-4) has a code dimension the BRIEF does not spell out.** "Absorb only is absolute" must be true in the engine, not just in prose: verify whether `software/app/game/combat.py`'s reaction path permits Dodge/Parry at 0 Endurance while Withdrawn (free reactions) or Defensive (cost 0). `CombatDef.endurance_floor_rule` already exists in the schema as a string field — encode the rule there and have the engine read it. If the engine already refuses, the task is text + a regression test; if it permits, it is a behaviour fix. Either way the test is written first. rul-L4 rides along: the quick-ref line "0 Endurance = Absorb only (Conditions land at full tier)" is wrong for an armored character — armor still downgrades (III.3:47).

**D10 (W3-10/W3-11) is the largest new-prose task and is split.** W3-10 writes the MM2 section (scope classification, domain boundary calls with the "lean toward yes" posture from II.3:25, designing 7–9 complications, active-opposition difficulty from III.3:381) — all four topics are *compressions of existing PHB rules into MM-facing guidance*, which is what keeps this inside the no-new-mechanics non-goal. W3-11 does the companion coverage pointers (Specialty ruling into MM5 Common Rulings, MM2 hazard/Threat Clock pointers to III.2, MM4 safety → III.2 death choice) and the MM5 compression of the new section. Both drafts go to the user for voice review **before** merge (D12); the LOG records the draft as sent.

**W3-14 rules two findings as-designed rather than fixing them**, with rationale in `DECISIONS.md`:
- cre-M7 (Communion Tier 3 has one fewer non-magic pick than Archive): fixing means authoring a new Technique — a Non-goal. Record the asymmetry as accepted, with the observation that both trees offer the same *number* of Tier 3 picks once magic Techniques are counted.
- rul-L5 (no pre-built Background grants Survival): fixing means changing a Background's skill grant — a content change with knock-on effects in yaml, tests, and the pre-gens. Record as accepted; the custom-Background path (II.5:83) covers it.

If the user rejects either ruling at PR review, it escalates to Brain, not to an in-wave fix.

### 4.4 Wave 4

Twelve encodings, each following the same five-step shape (yaml → schema model → engine read → tests → commit citing the PHB section). Two notes:

**W4-7/W4-8 (saving throws) is the only genuinely new software capability** in the cycle. It needs the Major Attribute modifier derivation first (`II.2:106-113`: minor sum 3–4 → −1, 5–7 → +0, 8–9 → +1) because a saving throw *is* 2d6 + that derived modifier (III.1:84-99). W4-7 encodes and implements the derivation on `Character`; W4-8 adds the roll path and the WebSocket event. Do not collapse them — the derivation is independently testable and is also what M-8's yaml block is for.

**W4-9 carries D8.** The new pushing-scope rule (a pre-Technique caster may spend a Spark to attempt a single Significant-scope effect at the domain's normal Significant difficulty) is encoded alongside the two existing Spark-magic rules currently hardcoded in `engine.py:230-256`. The Broad-domain hard ceiling stays immovable; the Focused ease-Major rule stays. The engine's `push_scope` is rewritten against the yaml, not extended in place.

---

## 5. Test Strategy

**Baseline:** 1026 tests green on `main` (S2). Every wave reports its own collected count in the LOG and in the PR description.

**Standing invariants that gate these waves** (`software/tests/test_docs_consistency.py`):
- INV-1 skill descriptions ↔ II.6 — touched if any skill prose changes (none planned).
- INV-2 sheet fields ↔ `Character` — **W3-3 must update the mapping**.
- INV-3 Glossary pointers resolve and contain the term — **W1-8 must keep every new entry's pointer valid**.
- INV-4 `Index.md` byte-identical to regeneration — **every Glossary/heading task regenerates**.
- INV-5 `Chapter X.Y` references resolve — W1-10 and W3-7 touch the ToC.
- INV-6 MM5 typographic dashes — W1-7, W3-6, W3-11, W3-12 all edit MM5.
- INV-7 domain catalog ↔ appendix — W1-10 touches the appendix.

**New tests this cycle (minimum):**

| Task | Tests |
|---|---|
| W1-9 slugger | 3 — em-dash heading emits `--`; "+"-in-heading case; plain heading unchanged. Plus INV-4 green after regeneration. |
| W2-7 Overwhelming Force | 2 — yaml text carries the once-per-scene limit and the 10+ trigger; no "3 or more above the threshold" string survives anywhere in yaml. |
| W2-8 domain prerequisite | 3 — Second Domain refused without a domain; permitted with one; Ascendant Domain likewise. |
| W2-9 branch/tier rule | 7 — the list in §4.2. |
| W3-1 Guild Apprentice | 2 — yaml specialty equals the II.5 text; a background-consistency assertion covering all 15. |
| W3-3 sheet | INV-2 updated + 1 new assertion that every new sheet section label maps to a real model field. |
| W3-4 0-Endurance | 3 — Dodge refused at 0 End while Withdrawn; refused while Defensive; Absorb permitted. |
| W4-1…W4-6 | ≥3 each (happy/edge/error per CLAUDE.md), characterization-style: identical outcomes, values sourced from yaml. |
| W4-7 Major modifier | 4 — the three bands plus an out-of-range guard. |
| W4-8 saving throw | 3 — engine path, WS event happy path, WS error on unknown attribute. |
| W4-9 Spark scope fuel | 4 — Focused ease-Major; Broad refusal; D8 pre-Technique Significant push permitted once; Major still refused pre-Technique. |
| W4-10/11/12 | schema-load assertions, ≥1 each, plus a facet.yaml round-trip. |

**Simulation:** only W2-4 (D2) could move a simulated number, and it does not — TR is an authoring/ordering figure, not a combat input. No re-simulation is required this cycle. If any task believes it needs one, that is an escalation: the rule is that simulations run through `app/game/combat.py` only, and superseded series stay labeled and uncited.

---

## 6. Items Requiring User Sign-Off Before Merge

Per D12, flagged in the PR description of the wave that contains them:

| Item | Wave | Why |
|---|---|---|
| Trouble Table canonical text in MM2 | W3-8 | new canonical rule text (D3) |
| "Unnarrated details" + "try again" in III.1 | W3-9 | new canonical rule text (D3) |
| Pushing-scope rewrite (II.3:170) | W3-6 | new canonical rule text (D8) |
| "Adjudicating Magic" MM2 section | W3-10 | new MM-facing prose (D10) |
| Companion coverage prose (MM5/MM2/MM4) | W3-11 | new MM-facing prose (D10) |
| II.4a Body Facet intro | W3-13 | new prose in the book's voice |
| Vignette edits (Scholar, Zulnut, Threat Clock) | W1-2, W1-5, W1-6 | prose touched; voice must survive |
| cre-M7 and rul-L5 ruled as-designed | W3-14 | closing a Medium/Low without a fix |
| MM1 enemy-modifier semantics wording | W2-3 | reads like a rule statement even though it isn't |

---

## 7. Escalation Triggers

**Worker → Planner** (append `## ESCALATION` to `docs/LOG_audit_remediation.md`, stop):
- Any task's propagation set turns out to be incomplete — a fifth file states the rule and the task lists four.
- A finding's fix would require a new mechanic, a new Technique, or a new Background grant (Non-goal boundary).
- W2-9's branch/tier rule breaks a test that is *not* in the seven-case list — it means a prerequisite was carrying meaning nobody catalogued.
- W3-3's INV-2 update needs a new `Character` field (S3 says it should not).
- Two failed attempts on the same task.

**Planner → Brain:**
- The user vetoes a D-decision at PR review (D12) — the replacement decision is Brain-tier.
- W2-4's grep surfaces a TR-1 dependency with real mechanical weight (an encounter recipe or budget calibration keyed to Harbor Thug = 1), which would reopen D2.
- Wave 4 reveals that a "settled" mechanic is not actually settled enough to encode.

---

## 8. Open Questions (non-blocking)

1. **Sheet format.** D7 makes the sheet nine sections. Whether the printed appendix should also gain a one-page condensed layout is a production question, not a rules one — out of scope, worth a future BRIEF.
2. **README drift guard.** The BRIEF explicitly rules out auto-generation this cycle. W1-11 adds the derived-from-canon comment; a `--check`-style test over README counts is the natural next step and is *not* in scope here.
3. **`playtest/07_oraga_night_playtests` and `adventures/`** are untracked work in progress. They are excluded from every wave. Once committed, README's playtest figure needs another pass — noted, not scheduled.

---

**Resolved. Return to Worker (Sonnet) to execute from `docs/TASKS_audit_remediation.md`, starting at W0-1.**
