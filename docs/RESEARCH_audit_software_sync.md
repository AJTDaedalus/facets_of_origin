# RESEARCH: PHB ↔ facet.yaml Synchronization Audit

**Date:** 2026-07-30
**Auditor:** Brain-tier read-only audit (no files modified except this report)
**Scope:** `software/facets/base/facet.yaml` vs PHB chapters II.2, II.3 + Appendix_Magic_Domains, II.4/II.4a/II.4b/II.4c, II.5, II.6, III.1, III.3, IV.1 (plus III.2 for the yaml `hazards`/`death` blocks). Grep-level check of `software/app/game/` and `software/app/api/websocket.py` for mechanics referenced in code but absent from the yaml.

**Severity key:** High = numbers/rules actually differ · Medium = settled PHB mechanic missing from the yaml encoding (or orphaned in yaml) · Low = naming/cosmetic/description drift.

**Totals: 2 High · 12 Medium · 8 Low**

---

## Coverage Summary

| Category | PHB items | yaml items | Match | Mismatch/Missing |
|---|---|---|---|---|
| Attributes (II.2) | 3 major + 9 minor, ratings 1–3, 18-pt distribution | 3 + 9, ratings, distribution | ✓ names, counts, modifiers, points | Major-modifier derivation table & saving throws not encoded (M-8); description wording drift (L-6) |
| Skills (II.6) | 15 skills (5/5/5) | 15 skills | ✓ all names, Facets, attribute pairings; no extras | none |
| Magic domains (II.3 / Appendix) | 21 (Soul 9 core + 3 prismatic; Mind 6 core + 3 prismatic) | 21 (12 soul + 9 mind) | ✓ names, types (Focused/Standard/Broad), Facet, prismatic flags, difficulty tables | Spark scope-fuel rules engine-only (M-9); acquisition limits not encoded (L-7) |
| Techniques (II.4a/b/c) | Body 18, Mind 20 (incl. Second/Ascendant Domain), Soul 20 | same 58, same tiers/branches | ✓ every name present both directions, correct tier & Facet | Overwhelming Force rule stale (H-1); prerequisite model diverges (H-2); First Move drift (M-1) |
| Backgrounds (II.5) | 15 pre-built (5/5/5) | 15 | ✓ all starting skills, secondary skills, specialties, domain-origin replacement on Guild Apprentice / Hedge Scholar / Temple Acolyte | none |
| Combat parameters (III.3) | postures, reactions, Endurance, conditions, strike outcomes, armor, enemy rules | partial | ✓ postures & modifiers (incl. Aggressive first-reaction-only surcharge), reaction costs, Endurance base/recovery, condition tiers & names, Resolve depletion 2/1, mook rules, armor budgets 2/4, enemy armor Resolve +1/+2 | Press cost (M-2), riders (M-3), same-Tier-2→Broken (M-4), armor/reaction non-stacking (M-5), enemy attack tiers & posture-vs-reaction (M-6), Maneuver/Support (M-7) not encoded |
| Advancement (II.4) | 4 pts/session, 1/2 costs, 3 marks/rank, level per 5 advances, Major per 3 levels, rank mods 0/1/2/3 | same | ✓ all numbers | none |
| Difficulty ladder (III.1) | Easy +1 / Standard 0 / Hard −1 / Very Hard −2; tiers 10+/7–9/6− | same | ✓ names, modifiers, thresholds, labels | none |
| Hazards & death (III.2) | 4-segment clock, advance on 7–9/6−, wind-back = action no roll; Broken never lethal, scar/heroic-death gate | same | ✓ | Tier 1 out-of-combat clearing not encoded (L-2) |
| Core resolution extras (III.1) | Sparks, saving throws, contested rolls, group rolls | Sparks only | Spark base 3 ✓, spend mechanic ✓ | Saving throws (M-8), group rolls (M-10), contested rolls (M-11) missing; earn-method drift (L-1) |
| Equipment (IV.1) | weapon categories → attribute, armor budgets | armor only | ✓ armor matches III.3/yaml exactly | weapon table not encoded (M-12) |

---

## HIGH severity

### H-1. "Overwhelming Force" — yaml carries a stale, different rule
- **PHB** `player_handbook/II.4a_Character_Creation_Facet_Body.md:39-40`:
  > "**Overwhelming Force** — Once per scene, when your Strike scores a full success (10+) against a single target, you may drive the blow home: the target takes no offensive action in the next exchange."
- **yaml** `software/facets/base/facet.yaml:294-299`:
  > "When you succeed on a Combat roll against a single target by 3 or more above the threshold, the target is staggered — they act last in the next exchange and cannot take reactions until they do."
- Trigger differs (10+ vs "3+ above threshold"), effect differs (no offensive action vs act-last + no reactions), and the yaml is missing the once-per-scene limit. This is the pre-v0.3 wording; the PHB was rewritten to Strike/exchange terminology and the yaml never followed.

### H-2. Technique prerequisite model: yaml/engine are stricter than the PHB rule
- **PHB** `player_handbook/II.4_Character_Creation_Facets.md:83`:
  > "Tier 2 requires at least one Tier 1 Technique in the same branch. Tier 3 requires at least one Tier 2 Technique in the same branch."
- **yaml**: every Tier 2/3 Technique lists one *specific* prerequisite Technique (e.g. `overwhelming_force` → `prerequisites: [forcing_hand]` at `facet.yaml:300`; `shadow_walk` → `[fleet_step]` at :360; `hold_the_line` → `[formed_bond]` at :877; etc. — the pattern runs through all three trees).
- **Engine** enforces the yaml list literally: `software/app/game/character.py:338` (`missing = [p for p in tech_def.prerequisites if p not in self.techniques]`).
- Consequence: a character holding Weapon Mastery (Might Tier 1) is PHB-legal for Overwhelming Force but the software refuses it; same for every Tier 2/3 pick whose "other" Tier 1/2 was taken. This is a real rules difference affecting advancement legality, in both directions of the branch pairs.
- Note: for Second Domain / Ascendant Domain the PHB's extra requirement ("requires an existing Mind/Soul domain", II.4b:138/141, II.4c:138) *is* transitively satisfied by the yaml chains (`second_domain_mind` ← `cross_reference` ← `arcane_study`; `second_domain`/`ascendant_domain_soul` ← `the_language_beneath_language` ← `spiritual_domain`), but only because of the stricter chaining — if H-2 is fixed to "any same-branch Tier N−1," the domain prerequisite must be encoded explicitly or it is lost.

---

## MEDIUM severity

### M-1. "First Move" — timing drift between yaml and PHB
- **PHB** `II.4b_Character_Creation_Facet_Mind.md:96`: "**This exchange**, the opposition does not act until every party member's action has resolved — no ambush springs, no prepared trap goes off…"
- **yaml** `facet.yaml:569-574`: "Everyone in the party acts first **in the next exchange**."
- Which exchange the effect governs differs (this vs next), and the yaml lacks the ambush/trap-negation clause.

### M-2. Press cost not encoded in facet.yaml
- **PHB** `III.3_Combat.md:132`: "you may spend **1 Endurance** to add 1d6… drop the lowest."
- **yaml combat block** (`facet.yaml:1262-1354`): no `press` key at all.
- The cost is hardcoded in `software/app/api/websocket.py:528-534` ("# Press costs 1 Endurance … `character.endurance_current -= 1`"). Violates the "facet.yaml is the single source of truth for every mechanic the engine needs" rule.

### M-3. Strike rider rules not encoded
- **PHB** `III.3_Combat.md:124` (and quick ref :675-681): on a 10+ the attacker may hang a Tier 1 or Tier 2 rider Condition; a Tier 2 rider makes the enemy **Easy to Strike** until cleared; riders never defeat an enemy.
- **yaml** `strike_outcomes` (`facet.yaml:1297-1303`) and `enemy_durability` (:1342-1354) contain no rider fields.
- The engine implements it in code (`software/app/game/combat.py:512` easy-to-strike helper; :543-547 riders never escalate to Broken).

### M-4. Same-Tier-2-condition stacking → Broken not encoded
- **PHB** `III.3_Combat.md:254`: "If a character receives a Tier 2 Condition they already have, it escalates immediately to **Broken**."
- **yaml** conditions block (`facet.yaml:1305-1332`): no escalation rule.
- Implemented only in code: `software/app/game/combat.py:536,552-553`; `software/app/api/websocket.py:747`.

### M-5. Armor/reaction non-stacking + "charge not spent" rule not encoded
- **PHB** `III.3_Combat.md:357-363`: armor downgrades and partial-reaction downgrades do not stack (apply the greater); when the reaction provides the reduction, the armor charge is **not spent**.
- **yaml** armor block (`facet.yaml:1334-1340`) encodes only budgets and `tiers_reduced`.
- Implemented only in code (`software/app/game/combat.py:131-137` `IncomingConditionResult`, `armor_spent` flag).

### M-6. Enemy attack rules not encoded
- **PHB** `III.3_Combat.md:333-355`: incoming Condition tier by enemy type (Mook = Tier 1, Named NPC = Tier 2, Boss = Tier 2); Named/Boss posture shifts PC reaction difficulty (Aggressive = one step harder, Defensive = one step easier); Mooks don't declare postures.
- **yaml**: nothing under `combat` encodes incoming tiers or the posture→reaction-difficulty mapping. (Settled mechanic since 2026-03-13.)

### M-7. Maneuver and Support action rules not encoded
- **PHB** `III.3_Combat.md:141-161`: Maneuver — 10+ makes rolls against the target Easy, 7–9 works at a cost (stays Standard), 6− backfires. Support — grant +1d6-drop-lowest **or** one difficulty step, next roll only, non-stacking (most recent applies).
- **yaml**: no encoding. Handlers exist in code only (`software/app/api/websocket.py:886-961`).

### M-8. Saving throws & Major Attribute modifier derivation not encoded anywhere
- **PHB** `II.2_Character_Creation_Attributes.md:106-113`: Major modifier from sum of three minors (3–4 → −1, 5–7 → +0, 8–9 → +1). `III.1_Core_Resolution.md:84-99`: saving throws roll 2d6 + Major Attribute modifier.
- **yaml**: `attributes.ratings` covers minors only; no derivation table, no saving-throw rules.
- Engine: no Major-modifier derivation or saving-throw path found (`grep -i major app/game/` shows only Major Advancement). Software lags the PHB here entirely.

### M-9. Spark-as-scope-fuel rules encoded only in engine code, not yaml
- **PHB** `II.3_Magic.md:168-176`: push scope one tier with a Spark; Focused domains may Spark a Major from Hard → Standard; Broad ceiling immovable by Sparks.
- **yaml** `magic` block (`facet.yaml:1054-1076`): domain-type difficulty tables only.
- Rules are hardcoded in `software/app/game/engine.py:230-256` (`ease_focused_major`, `push_scope`, Broad refusal).

### M-10. Group Rolls not encoded and not implemented
- **PHB** `III.1_Core_Resolution.md:113-123`: majority-success group roll; lead-roller + Support alternative.
- **yaml**: absent. **Engine/websocket**: no `group` handler found. A settled III.1 mechanic (2026-03-13) with zero software presence.

### M-11. Contested roll rules not encoded in yaml
- **PHB** `III.1_Core_Resolution.md:104-109`: vs NPC only the PC rolls (NPC informs difficulty); PC-vs-PC both roll, higher wins, tie = both partial.
- **yaml**: absent. Handler exists in code only (`software/app/api/websocket.py:970-1025`), so the tie/higher-wins rule lives outside the source of truth.

### M-12. Weapon category → attribute table (IV.1) not encoded
- **PHB** `IV.1_Equipment.md:13-19`: Heavy = Strength; Standard = Str or Dex; Light = Dex; Ranged = Dex; Unarmed = Str or Dex. `III.3:112`: the weapon's category sets the Strike/Parry attribute; skill is Combat (melee/unarmed) or Finesse (ranged).
- **yaml**: no weapons section. The engine deliberately accepts any attribute/skill on a Strike, so nothing machine-checks the weapon rule.

---

## LOW severity

### L-1. Spark earn-method drift
- **PHB** `III.1_Core_Resolution.md:69-72` lists four: MM award, **"Spark?" peer call**, Act Break Nomination, Graceful Fail. The peer call is absent from `facet.yaml:964-997`.
- **yaml** has `spark_for_weakness` (:983-990) as a distinct method; III.1 folds weakness-play into the MM award instead — mild orphan.

### L-2. Tier 1 Conditions out of combat clear at end of scene
- **PHB** `III.2_Adventuring.md:69`: outside combat, Tier 1 clears at end of scene. **yaml** `facet.yaml:1307-1315` encodes only `clears: end_of_exchange`.

### L-3. Intercept once-per-exchange limit not encoded
- **PHB** `III.3_Combat.md:219`. **yaml** `facet.yaml:1291-1295` encodes only the cost (2).

### L-4. Defensive posture "min 0" clamp implicit
- **PHB** `III.3_Combat.md:87` states "(min 0)". yaml has no floor field; the clamp exists only in `combat.py:237` (`max(0, …)`). No behavioral difference — noting for completeness.

### L-5. Second Domain id inconsistency
- Soul: `second_domain` (`facet.yaml:879`); Mind: `second_domain_mind` (:657). Cosmetic but asymmetric; both PHB Techniques are named "Second Domain".

### L-6. Minor-attribute description drift (II.2 vs yaml)
- e.g. **Luck** — PHB II.2:90 "Bending fate in your favor. Drawing on innate or wild magic…" vs yaml:96 "The world's tendency to bend in your direction. Not wishful thinking — an actual, observable pattern." Similar wording drift on Knowledge, Spirit, Charisma, Dexterity, Constitution (yaml truncates PHB clauses). No mechanical effect.

### L-7. Domain acquisition limits not encoded
- **PHB** `II.3_Magic.md:244-246`: at most one domain per Facet via cross-training; Ascendant Domain is taken **once** ever across all trees; prismatics never a starting domain. Not represented in yaml (and not obviously validated in the engine).

### L-8. Technique description micro-drift
- Grinding Advance yaml (:422-428) drops the PHB's "a Spark, a second wind, a reserve of will" clause (II.4a:111); several other yaml descriptions trim PHB parentheticals (Sharp Analysis's observability restriction, II.4b:40; Commanding Presence's override clause, II.4c:51; Unforgettable's "glad to see you" clause, II.4c:63). Effects are unchanged; only flavor/clarifying text is missing.

---

## Code-vs-yaml quick check (as requested, not deep-dived)

- `websocket.py` **Press** cost hardcoded (see M-2); `combat.py` rider/easy-to-strike and Broken-escalation logic (M-3/M-4/M-5) reference no yaml fields; **Support/Maneuver/contested** handlers carry their rules in code (M-7/M-11). All condition ids the code references (`winded`, `off_balance`, `shaken`, `staggered`, `cornered`, `broken`) exist in the yaml ✓; reaction ids (`dodge/parry/absorb/intercept`) ✓; posture keys ✓; `mook_removed_on`/`armored_mook_removed_on` read from yaml ✓; Endurance formula reads `combat.endurance.base` from yaml with Con/skill modifiers composed in `character.py:202-210` ✓ (matches III.3).
- No engine reference to a skill, domain, Technique, posture, reaction, or condition name that is **absent** from facet.yaml was found.

## What is fully in sync (verified, no findings)

Attribute names/counts/ratings/distribution; all 15 skills with Facet + attribute pairings; all 21 domains with types, Facets, prismatic flags, and the three difficulty-by-scope rows; pre-Technique magic (Minor-only, no penalty); all 58 Technique names at correct tier/branch/Facet including both Second Domains and both Ascendant Domains; all 15 Backgrounds including the three domain-origin replacements; posture table incl. the K1 first-reaction-only Aggressive surcharge; reaction costs; Endurance base/recovery; condition names, tiers, clear timings, Staggered −1; armor budgets Light 2 / Heavy 4; enemy Resolve depletion 2/1/0 and armor +1/+2; mook removal rules; advancement numbers (4 pts, 1/2 cost, 3 marks, threshold 5, Major every 3); difficulty ladder; Spark base 3 and spend mechanic; hazard clock and the death gate.
