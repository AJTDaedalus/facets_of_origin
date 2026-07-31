# Completeness Audit — PHB + MM Manual (main branch)

**Date:** 2026-07-30
**Trigger:** User noticed a "says 3 magic types, lists only 2"-style gap on main and asked for a full completeness audit of the Player's Handbook and MM Manual.
**Method:** Five parallel audit passes, each with its own detailed report:

| Area | Report | High | Med | Low |
|---|---|---|---|---|
| PHB creation chapters (I, II.1–II.4c) | `RESEARCH_audit_phb_creation.md` | 3 | 7 | 6 |
| PHB rules chapters (II.5–IV.1, Quick Start) | `RESEARCH_audit_phb_rules.md` | 1 | 5 | 6 |
| PHB apparatus (ToC, Glossary, Index, appendices) | `RESEARCH_audit_phb_apparatus.md` | 2 | 7 | 6 |
| MM Manual (MM1–MM5) | `RESEARCH_audit_mm_manual.md` | 1 | 6 | 9 |
| PHB ↔ facet.yaml/engine sync | `RESEARCH_audit_software_sync.md` | 2 | 12 | 8 |
| **Total** | | **9** | **37** | **35** |

Full quotes, line numbers, and verification tables (including everything that *passed*) are in the five detail reports. This file is the prioritized synthesis.

---

## The original "3 magic types but only 2 listed" issue — resolved

No file literally claims "three types of magic" (repo-wide search). The PHB asserts exactly **two** magical traditions (Spirit-intuitive, Knowledge-scholarly, II.3:101). The real instances of the claims-3-delivers-2 pattern are:

1. **`II.3_Magic.md:246`** — "Prismatic domains require the **Ascendant Domain** Technique (Tier 3, **in each Facet's tree**)" — but only the Mind (Archive) and Soul (Communion) trees contain it; the Body tree (II.4a) has no Ascendant Domain and no magic Technique at all.
2. **`Glossary.md:90`** — "**Second Domain** — A Tier 3 Technique, **in each Facet's tree**" — same problem: Mind and Soul only.
3. (Softer, related) The II.3 Domain Quick Reference lists Soul and Mind domains only; the Body-magic deferral explanation arrives ~60 lines later with no forward pointer at the list itself (`II.3:186–223` vs `:250–252`).

**Fix:** change "in each Facet's tree" → "in the Mind and Soul trees" in both places; optionally add a one-line Body-magic forward pointer at the top of the Quick Reference.

---

## All High-severity findings (9)

1. **Point-buy sidebar teaches an illegal array as "net zero"** — `II.2:102`: "four at 3, two at 1, three at 2" totals 20 points against the 18-point budget.
2. **Ascendant Domain "in each Facet's tree"** — `II.3:246` (see above).
3. **Second Domain glossary "in each Facet's tree"** — `Glossary.md:90` (see above).
4. **Guild Apprentice has no Specialty** — `II.5:187–197` lists 4 of the promised 5 elements (`II.5:15`); the other 14 Backgrounds all have one, and `Quick_Start.md:36` gives Zahna a Guild Apprentice Specialty ("Artificers' Guild technical records") that II.5 never defines. *Needs a canon decision (likely: adopt the Quick Start Specialty into II.5).*
5. **Character sheet cannot run combat** — `Appendix_Character_Sheet.md` has no Endurance, Armor, or Conditions fields; III.3's "five numbers on screen" are represented only by Sparks. Root cause is II.1's six-section sheet spec, which the appendix faithfully mirrors — fixing requires amending II.1 too.
6. **Character sheet has no magic domain field** — Zahna (a pre-gen) cannot be transcribed onto it without losing her Inscription domain.
7. **Basic Mook TR contradiction (four-way)** — MM1 claims a +0-attack Mook is TR 1 (`MM1:55`, `:121`, `:293`) but MM1's own formula computes TR 2; `enemies/harbor_thug.fof` says `tr: 2` while its own notes claim "TR 1 minimum by rule". Chicken (attack −1) is the only true TR-1 baseline.
8. **facet.yaml carries the stale pre-v0.3 "Overwhelming Force"** — `facet.yaml:294–299` ("succeed by 3+ → staggered…") vs II.4a:39–40's current rule (once per scene, 10+ Strike → no offensive action next exchange).
9. **Technique prerequisite model mismatch** — yaml/engine enforce specific named-Technique chains; PHB (`II.4:83`) requires only "any Tier N−1 in the same branch" — the software rejects legal advancement picks.

---

## Medium-severity themes (37 findings — see detail reports)

**Rules text contradictions (PHB):**
- 0-Endurance "Absorb only" vs Withdrawn's free / Defensive's cost-0 reactions (`III.3:45,167` vs `:87–88`) — unresolved which wins.
- Combat quick-ref lists "Magic" and "Withdraw" as declarable actions the body text never defines (`III.3:646`) — violates the compression rule.
- "Reckless Press" (`III.3:395`) named once, defined nowhere.
- "Pushing scope" Spark rule (`II.3:170`) references a scope ceiling no rule defines — every domain type already has a difficulty at every scope.
- II.3:93 illustrates two Techniques (ease Minor magic; remove collateral) that exist in no tree.
- Soul Second Domain missing the domain prerequisite its Mind twin has (`II.4c:134` vs `II.4b:137`) — a Soul character could take a "second" domain without a first.
- Threat Clock vignette fills a 4-segment clock in 3 advances (`III.2:96`); the pacing math at `III.2:19` (72% rate → "3–4 rolls") is also wrong (~5.6 expected).
- Zulnut advancing Finesse to Practiced in II.4 examples when it's Practiced at creation (`II.4:59,73` vs `II.2:200`); also `II.4:116` "Knowledge rank ticks to Practiced" — Knowledge is an attribute, should be Lore.
- "The Scholar" example calls Luck 2 "Strong" (label for 3) — `II.2:118,121`.

**Un-migrated v0.3 text:**
- III.3's Magic-in-Combat and Attune paragraphs still resolve magical Strikes in Condition tiers, not Resolve (`III.3:379,391`); MM5 already states the Resolve version — the canonical text lags its own quick ref.
- MM1 stat blocks say enemies "use" Attack/Defense modifiers "for Parry", contradicting "NPCs do not roll" (`MM1:25–26` vs `III.3:331`); no guidance on what the modifiers mean at the table.
- MM1:411 cites superseded v0.2 simulation survival numbers; MM2:165 still defines Skirmish by the deprecated TR budget.

**Quick-refs as sources (violations of the compression rule):**
- MM5's Trouble Table and two Common Rulings ("unnarrated details", "try again") exist in no canonical body text — and the Index links MM5 as their home (`MM5:284–302`).
- MM5's Maneuver line reverses canon direction ("target's next roll Easy" vs "rolls *against* the target are Easy") (`MM5:107` vs `III.3:146`).

**Apparatus gaps:**
- Sheet: no "or Domain Origin" alternative for Secondary Skill; "marks toward next level" mislabels the unit (should be rank advances); no inventory; no Career Advances field.
- Glossary missing "Saving Throw" (propagates to the generated Index); `I_Introduction:29` promises a Shattered Origin setting chapter that exists nowhere; ToC's module list omits the Shattered Origin setting Facet that II.3 defers Body magic to.
- 33 of 552 Index links use anchors GitHub won't resolve — slugger bug in `software/tools/build_index.py:110–113` (collapses spaces around em dashes to one hyphen; GitHub emits two).

**Coverage gaps (MM manual):**
- **Zero MM-side guidance on adjudicating magic** (scope classification, domain boundary calls, 7–9 complications) — the largest coverage gap in the manual.
- Specialties never mentioned in any MM file despite II.5 giving the MM an adjudication rule; Hazards/Threat Clocks and the death choice (III.2) never referenced by any MM chapter; Pinnacle Technique approval criteria absent (known open blocker).

**Software sync (12 Medium):** newer settled mechanics live only in engine code or nowhere — Press cost (hardcoded in `websocket.py:528`), Strike riders / Easy-to-Strike, Tier-2-stacking→Broken, armor/reaction non-stacking, enemy attack tiers & posture-vs-reaction difficulty, Maneuver/Support, contested rolls, Spark scope-fuel, weapon→attribute table; saving throws and Group Rolls have **no software presence at all**.

---

## Low-severity (35) — see detail reports

Naming/citation drift (Glossary citation formats, dual-home Techniques cited once, appendix letters only in ToC, ToC chapter titles), compression drift in MM5 Spark economy numbers, stale notes in `veteran_soldier.fof`, MM1 "three things" vs 4-step list, Survival being the only skill no pre-built Background grants, vignette grounding issues (Mordai's Weapon Mastery, Quick Start's Graceful Fail mislabel), and 8 Low sync items.

---

## What verifiably passed

- All 21 domains: II.3 quick ref ↔ Appendix ↔ facet.yaml agree exactly (names, types, territories, difficulty tables). The 9+3 Soul / 6+3 Mind split is stated accurately in both files.
- ToC ↔ files match both ways (only IV.2 "(Planned)" lacks a file, correctly marked). No stubs, TODOs, or empty sections anywhere in PHB or MM.
- All cross-references resolve (PHB and MM). Glossary's 54 terms = Index's 54 sections; `build_index.py --check` passes.
- ~70 count-claims verified across the PHB; all but those listed above pass. MM5 matches canon on ~25 of 29 rule blocks. All enemy TRs except Harbor Thug recompute correctly (Chicken 1, Sergeant 8, Veteran 10, Guardian 17).
- Sync: attributes, all 15 skills, all 58 Technique names, all 15 Backgrounds, postures/reactions/conditions/armor numbers, advancement math, difficulty ladder — all match exactly.

---

## Suggested fix order

1. **Wave 1 — mechanical text fixes, no canon decisions needed:** H1–H3 wording/math, Soul Second Domain prereq line, Maneuver quick-ref line, Named-NPC rider tier, Zulnut/Scholar/Lore vignette fixes, glossary citations, Index slugger bug + regenerate.
2. **Wave 2 — v0.3 migration completion:** III.3 Magic-in-Combat → Resolve model; MM1 enemy-modifier table-side meaning; retire superseded sim citations; MM2 Skirmish definition; facet.yaml Overwhelming Force + prerequisite model (+ tests).
3. **Wave 3 — canon decisions required (user):** Guild Apprentice Specialty (adopt Quick Start's?), character sheet redesign (amend II.1 spec + appendix), canonical home for MM5's Trouble Table / Common Rulings, "pushing scope" rule intent, "Reckless Press" define-or-cut, Body-tree magic Technique stance, Shattered Origin setting-chapter promise in I_Introduction, MM magic-adjudication section (new content).
4. **Wave 4 — sync backlog:** encode the 12 Medium yaml gaps per the Software-PHB Sync workflow.
