# RESEARCH: PHB Front/Back Matter Audit (Apparatus Completeness & Consistency)

**Date:** 2026-07-30
**Scope:** `player_handbook/` — Front_Matter.md, Table_of_Contents.md, Glossary.md, Index.md, Appendix_Character_Sheet.md, Appendix_Magic_Domains.md
**Mode:** Read-only audit. No content fixed; findings only.

---

## Summary

The apparatus is in strong shape structurally: the ToC and the file set match in both directions, the Magic Domain appendix and II.3's quick-reference tables agree exactly (21 domains, all names/types/territories, and both files' count-claims — 9 core + 3 prismatic Soul, 6 core + 3 prismatic Mind — are accurate), every one of the 21 domain entries is complete per the appendix's own stated structure, the Glossary's 54 terms match the Index's 54 sections one-for-one, the Index passes its own `--check` freshness invariant, and all 15 glossary citations spot-checked resolve to chapters that genuinely define the term. No "says 3, lists 2" count errors were found in the six files.

The significant problems cluster in two places. (1) **The character sheet appendix is missing the combat-facing half of a character**: it has no Endurance, Armor, Conditions, magic domain, or inventory fields — III.3 itself enumerates five tracked combat numbers and the sheet carries only one of them (Sparks). The root cause is upstream: II.1's six-section sheet specification omits these, and the appendix explicitly binds itself to II.1 ("Every field below is one II.1 already named"), so a fix must touch both files. (2) **The Index's anchor slugs deviate from GitHub's algorithm** for headings containing punctuation flanked by spaces (em dashes, "+"): 33 of 552 links will not jump on GitHub rendering. Secondary issues: the Glossary lacks a **Saving Throw** entry (a core III.1 mechanic, which also keeps it out of the generated Index), the sheet's "marks toward next level" label conflates skill marks with the rank advances that actually drive Facet levels, and I_Introduction promises a Shattered Origin setting chapter that exists nowhere in the ToC or files.

**Finding counts:** High 2 · Medium 7 · Low 6.

---

## Findings

### High

**H1. Character sheet is missing Endurance, Armor, and Conditions fields**
`player_handbook/Appendix_Character_Sheet.md` (whole file; sections at lines 13–95), `player_handbook/II.1_Character_Creation_Overview.md:11–24`, `player_handbook/III.3_Combat.md` ("Your Five Numbers On Screen").
III.3 enumerates the five numbers every combatant tracks: "**Endurance** … **Posture** … **Conditions** … **Sparks** … **Armor budget**." The sheet provides only Sparks. There is no field for the Endurance pool (III.3:717: "Base: 4 + Constitution modifier + Endurance skill rank"), no armor type / downgrade-budget field (III.3:280–281), and no Conditions track. A character on this sheet cannot fight. Root cause: II.1's six-section sheet spec (Attributes / Facet / Background / Skills / Techniques / Session Resources) omits combat stats, and the appendix states "Every field below is one II.1 already named; nothing here is new" (line 3) — so it faithfully inherits the gap. Fixing the sheet requires amending II.1's section list too.

**H2. Character sheet has no magic domain field**
`player_handbook/Appendix_Character_Sheet.md` (no field anywhere), vs `player_handbook/II.3_Magic.md:227–246` ("Acquiring a Domain") and `player_handbook/II.5` (magic-granting Backgrounds).
A domain (name, type Focused/Standard/Broad, and whether it is still pre-Technique Minor-scope-only) is a character-creation element agreed at creation and consulted on every magical roll. The sheet has nowhere to record it. Zahna, one of the three pre-generated characters, could not be transcribed onto this sheet without losing her Inscription domain.

### Medium

**M1. Background section lacks the "or Domain Origin" alternative**
`player_handbook/Appendix_Character_Sheet.md:45` — "| Secondary Skill (Novice, 1 mark) | |".
II.5 rules that magic-granting Backgrounds *replace* the Secondary Skill with a domain origin (Glossary confirms: "Magic-granting Backgrounds replace it with a domain origin instead," Glossary.md:92). The sheet presents Secondary Skill as unconditional, with no alternate field or label for the domain-origin case.

**M2. "Advancement Track (marks toward next level)" mislabels the unit**
`player_handbook/Appendix_Character_Sheet.md:35` — "| Advancement Track (marks toward next level) | |".
Facet levels advance per **skill rank advances**, not marks: II.4:65 "Your **Facet level** … advances every time you accumulate **5 skill rank advances** within it." A "mark" is canonically defined (Glossary.md:62, II.4:57) as progress toward a *skill rank* (3 marks = 1 rank advance). Tracking "marks toward next level" as written would triple-count progress (5 rank advances = 15 marks). II.1:16 says only "advancement track toward the next level" — the parenthetical is the appendix's own addition, and it contradicts canonical terminology.

**M3. No inventory/equipment section on the sheet**
`player_handbook/Appendix_Character_Sheet.md` (absent), vs `player_handbook/IV.1_Equipment.md` (weapons, armor, specialized gear) and the digital character model (which has an `inventory` field).
The sheet has no place to record equipment at all — including the armor whose type drives the downgrade budget (see H1).

**M4. No Career Advances field on the sheet**
`player_handbook/Appendix_Character_Sheet.md` (absent), vs `player_handbook/II.4_Character_Creation_Facets.md:155–161` ("It is the progression metric for Facets of Origin") and MM1's Party Strength tiers, which are keyed to per-PC career advances.
The book's stated progression gauge is not recordable on the sheet.

**M5. Glossary (and therefore Index) missing "Saving Throw"**
`player_handbook/Glossary.md` (no entry), vs `player_handbook/III.1_Core_Resolution.md:86` — "the MM calls for a **saving throw**. You roll 2d6 + the relevant **Major Attribute modifier**."
A core, bolded, rule-defining mechanic; the ToC advertises it (Table_of_Contents.md:20 "*(… contested rolls, saving throws)*") and the Glossary's own Attribute entry leans on it ("Major Attributes … ground saving throws," Glossary.md:14). Because Index.md is generated from the Glossary term list, the omission propagates: there is no Index entry for saving throws either.

**M6. 33 of 552 Index links use anchors that do not resolve on GitHub**
`player_handbook/Index.md` (e.g., lines 61–63 `Quick_Start.md#zahna-the-scholar`, line 207 `MM5_Quick_Reference.md#magic-domain-intent-scope`, line 276 `II.4a…#facet-of-the-body-technique-tree`); generator: `software/tools/build_index.py:110–113`.
The slugger claims to be "GitHub-flavored-markdown-style" but collapses whitespace to a single hyphen after stripping punctuation (`re.sub(r"\s+", "-", slug)`). GitHub emits one hyphen per space, so the heading "Zahna — The Scholar" anchors as `#zahna--the-scholar` (double hyphen) on GitHub, while the Index links `#zahna-the-scholar`. Every heading containing an em dash, "+", or similar space-flanked punctuation is affected (33 links, verified by script against all target files). Note: `python -m tools.build_index --check` passes — the file is fresh; the bug is in the slug algorithm, not staleness. All 552 links point to files that exist; the other 519 anchors are valid.

**M7. I_Introduction promises a Shattered Origin setting chapter that does not exist; ToC's module list omits the "Shattered Origin setting Facet" that II.3 defers to**
`player_handbook/I_Introduction.md:29` — "This handbook includes the **Shattered Origin** setting — a primary world created as a home for the game's first adventures and campaigns." No setting chapter appears in `Table_of_Contents.md` or in the `player_handbook/` file set. Separately, `player_handbook/II.3_Magic.md:252` defers Body magic to "the Shattered Origin setting Facet," a module the ToC's Facets list (Table_of_Contents.md:51–58: Downtime, Crafting, Economy, Feats, Technology) never mentions. Readers are pointed at content with no ToC destination.

### Low

**L1. Glossary citation style inconsistency**
`player_handbook/Glossary.md:12` "*(II.4b)*" and `:90` "*(II.4c)*" vs the "*(Chapter X.Y)*" format used by all 52 other entries.

**L2. Single-Facet citations for dual-Facet Techniques**
`player_handbook/Glossary.md:12` (Ascendant Domain → II.4b only) and `:90` (Second Domain → II.4c only). Both Techniques exist in both trees — Ascendant Domain in II.4b (Archive) *and* II.4c:137 (Communion); Second Domain in II.4c *and* II.4b:137–138 (Arcane Study) — and the Second Domain entry itself says "in each Facet's tree." Each citation names only one of the two defining chapters.

**L3. Tier 1 Conditions have no individual glossary entries while Tier 2's do**
`player_handbook/Glossary.md` — Staggered (:102) and Cornered (:30) have standalone entries; Winded, Off-Balance, and Shaken appear only inside the Condition entry (:26). Asymmetric treatment of the same class of term (and it keeps them out of the generated Index).

**L4. Other missing glossary/Index topics**
`player_handbook/Glossary.md` — no entries for **Pinnacle Technique** (defined II.4:98 and referenced by the glossary's own Major Advancement entry, :58), **Party Strength** (MM1 — the Glossary already includes the MM1 terms Threat Rating and Encounter Budget), or any **Weapon/Equipment** term (IV.1 is reachable in the Index only via Armor). All propagate to Index.md.

**L5. ToC lists IV.2 with no file — correctly marked**
`player_handbook/Table_of_Contents.md:26` — "IV.2 Magical Items *(Planned)*". No `IV.2` file exists; the "(Planned)" marker makes this acceptable. Informational: it is the only ToC entry without a file.

**L6. Appendix letters exist only in the ToC**
`player_handbook/Table_of_Contents.md:32–33` names "Appendix A: Magic Domain Catalog" and "Appendix B: Character Sheet"; the files title themselves "Appendix: Magic Domain Catalog" and "Appendix: Character Sheet" with no letters. Cross-references elsewhere (e.g., II.3:188) also use the letterless form. Harmless today, but the A/B labels are load-bearing nowhere except the ToC.

---

## Verification Tables

### 1. Table of Contents ↔ player_handbook/ files

| ToC entry | File | Status |
|---|---|---|
| Front Matter | Front_Matter.md | OK |
| I — Introduction | I_Introduction.md | OK |
| II.1 Overview | II.1_Character_Creation_Overview.md | OK |
| II.2 Attributes | II.2_Character_Creation_Attributes.md | OK |
| II.3 Magic | II.3_Magic.md | OK |
| II.4 Facets & Advancement | II.4_Character_Creation_Facets.md | OK |
| II.4a (Body) | II.4a_Character_Creation_Facet_Body.md | OK |
| II.4b (Mind) | II.4b_Character_Creation_Facet_Mind.md | OK |
| II.4c (Soul) | II.4c_Character_Creation_Facet_Soul.md | OK |
| II.5 Backgrounds | II.5_Character_Creation_Backgrounds.md | OK |
| II.6 Skills | II.6_Character_Creation_Skills.md | OK |
| III.1 Core Resolution | III.1_Core_Resolution.md | OK (description accurate: dice, difficulty, Sparks, contested rolls, saving throws all present) |
| III.2 Adventuring | III.2_Adventuring.md | OK (hazards/Threat Clocks, recovery, death all present) |
| III.3 Combat | III.3_Combat.md | OK |
| IV.1 Equipment | IV.1_Equipment.md | OK |
| IV.2 Magical Items *(Planned)* | — | No file; marked Planned (L5) |
| Quick Start | Quick_Start.md | OK |
| Appendix A: Magic Domain Catalog | Appendix_Magic_Domains.md | OK (letter mismatch, L6) |
| Appendix B: Character Sheet | Appendix_Character_Sheet.md | OK (letter mismatch, L6) |
| Glossary | Glossary.md | OK |
| Index | Index.md | OK |
| MM1–MM5 | ../mm_manual/MM1…MM5 | All five exist |
| Facet modules (Downtime, Crafting, Economy, Feats, Technology) | — | Matches Front_Matter.md:20 and PHB scope policy; **omits** the "Shattered Origin setting Facet" that II.3:252 references (M7) |

**Orphan files not in ToC:** none. Every file in `player_handbook/` (21 files) is a ToC entry or the ToC itself.

### 2. II.3 Domain Quick Reference ↔ Appendix_Magic_Domains.md

Both sources: **21 domains** (II.3:188 "All 21 domains"; appendix:3 "all 21 magic domains"). Appendix count-claims verified: Soul "nine core domains and three prismatic" (:15) → 9+3 listed; Mind "six core and three prismatic" (:189) → 6+3 listed. Every appendix entry has a description, a "*Beyond this domain's focus*" boundary block, and exactly 3 example intents at each of Minor/Significant/Major (script-verified).

| Domain | II.3 type | Appendix type | Territory agrees | Entry complete |
|---|---|---|---|---|
| Fire | Focused | Focused | Yes | Yes |
| Shadow | Focused | Focused | Yes | Yes |
| Storm | Standard | Standard | Yes | Yes |
| Beasts | Standard | Standard | Yes | Yes |
| Resonance | Standard | Standard | Yes | Yes |
| Verdance | Standard | Standard | Yes | Yes |
| Binding | Standard | Standard | Yes | Yes |
| Presence | Standard | Standard | Yes | Yes |
| The Tide | Standard | Standard | Yes | Yes |
| The Undying † | Broad | Broad | Yes | Yes |
| Fate † | Broad | Broad | Yes | Yes |
| The Living World † | Broad | Broad | Yes | Yes |
| Illusion | Standard | Standard | Yes | Yes |
| Warding | Standard | Standard | Yes | Yes |
| Inscription | Focused | Focused | Yes | Yes |
| Transmutation | Standard | Standard | Yes | Yes |
| Divination | Standard | Standard | Yes | Yes |
| Constructed Force | Focused | Focused | Yes | Yes |
| The Arcane † | Broad | Broad | Yes | Yes |
| The Constructed Mind † | Broad | Broad | Yes | Yes |
| Chronomancy † | Broad | Broad | Yes | Yes |

Prismatic difficulty text (appendix:142 "Hard at Minor … Very Hard at Significant … Very Hard at Major … no ceiling movement through Sparks") matches II.3's Broad row and hard-limit rule (II.3:89, :174). No discrepancies.

### 3. Glossary citations spot-checked

| Term | Cited | Verified against | Result |
|---|---|---|---|
| Mirror Master | Chapter I | I_Introduction.md:9 (defines the role) | Correct |
| Career Advance | Chapter II.4 | II.4:155 ("## Career Advances") | Correct |
| Rank (+1/3, +2/6, +3/9 marks) | Chapter II.6 | II.6:111–113 (table matches exactly) | Correct |
| Skill Point (4/session, no carry-over) | Chapter II.4 | II.4:46 ("**4 skill points**"), II.4:53 ("unspent points are lost") | Correct |
| Mark (3 marks/rank, carries over) | Chapter II.4 | II.4:57 | Correct |
| Facet Level (per 5 rank advances) | Chapter II.4 | II.4:65 | Correct |
| Major Advancement (every 3 levels; +1 Minor Attr or Pinnacle) | Chapter II.4 | II.4:93, :148–149 | Correct |
| Spark (3 per session) | Chapter III.1 | III.1:63 | Correct |
| Difficulty (Easy +1 … Very Hard −2) | Chapter III.1 | III.1:52–55 | Correct |
| Contested Roll (tie → both partial) | Chapter III.1 | III.1:109 | Correct |
| Group Roll (majority, partial counts) | Chapter III.1 | III.1:117 | Correct |
| Threat Clock (four-segment) | Chapter III.2 | III.2:11 | Correct |
| Endurance (4 + Con + rank; 0 = Absorb only) | Chapter III.3 | III.3:717 | Correct |
| Armor (light 2 / heavy 4, per scene) | Chapter III.3 | III.3:280–281 | Correct |
| Mook (7+ removes; armored needs 10+) | Chapter III.3 | III.3:300 | Correct |

Also confirmed structurally: Ascendant Domain is defined in II.4b and Second Domain in II.4c as cited (though each also exists in the sibling file — L2). Threat Rating and Encounter Budget correctly cite MM1. **Glossary term count = 54; Index section count = 54; the two term lists match exactly** (script-verified). `python -m tools.build_index --check` exits 0 (Index fresh per INV-4).

### 4. Index link verification

Script-checked all **552** links in Index.md: **0 missing files**, **519 valid anchors**, **33 anchors that deviate from GitHub's slug algorithm** (M6) — all caused by headings containing space-flanked punctuation ("Zahna — The Scholar", "Magic: Domain + Intent + Scope", "Facet of the Body — Technique Tree", "Encounter Recipe Table (PS 3 — simulation-validated)"). Topical spot-checks (Armor, Endurance, Resolve, Spark, Facet, Background, Strike, Exchange, Posture, Condition, Domain, Scope, Threat Rating, Mook, Difficulty) all point at sections that genuinely define or rule on the term.

### 5. Character sheet field coverage (per II.1–II.6, III.3)

| Needed field | Source | On sheet? |
|---|---|---|
| Character/player names | II.1 | Yes |
| 9 Minor Attributes (1–3) under 3 Majors | II.2 | Yes |
| Primary Facet, Facet level, advancement track | II.4 | Yes (but label wrong — M2) |
| Background title/origin, Starting Skill, Specialty | II.5 | Yes |
| Secondary Skill **or Domain Origin** | II.5 | Partial — no domain-origin alternative (M1) |
| All 15 skills with rank + marks | II.6 | Yes (15 rows: 5 Body / 5 Mind / 5 Soul) |
| Techniques + unlock choices | II.4 | Yes |
| Sparks | III.1 | Yes |
| Skill points | II.4 | Yes |
| **Endurance pool** | III.3 | **No (H1)** |
| **Armor type / downgrade budget** | III.3, IV.1 | **No (H1)** |
| **Conditions track** | III.3 | **No (H1)** |
| **Magic domain (name/type/scope status)** | II.3, II.5 | **No (H2)** |
| Inventory/equipment | IV.1 | No (M3) |
| Career Advances | II.4 | No (M4) |

### 6. Count-claims audit

| Claim | Location | Actual | Result |
|---|---|---|---|
| "all 21 magic domains" | Appendix_Magic_Domains.md:3 | 21 | OK |
| "nine core … three prismatic" (Soul) | Appendix_Magic_Domains.md:15 | 9 + 3 | OK |
| "six core … three prismatic" (Mind) | Appendix_Magic_Domains.md:189 | 6 + 3 | OK |
| "three example intents per scope" | Appendix_Magic_Domains.md:7 | 3 per scope, every domain (scripted) | OK |
| "All 21 domains at a glance" | II.3:188 | 12 + 9 = 21 rows | OK |
| "three domain types" | II.3:71 | Focused, Standard, Broad = 3 | OK |
| "two names … six sections" | Appendix_Character_Sheet.md:3 | 2 names, 6 sections | OK (internally; completeness issues are H1/H2) |
| "six sections" | II.1:11 | 6 table rows | OK |
| "All 15 skills" | II.1 (Skills row) | 15 rows on sheet | OK |
| MM1–MM5 (five manuals) | Front_Matter.md:18, ToC:43–47 | 5 files exist | OK |
| Five Facet modules | Front_Matter.md:20, ToC:54–58 | 5 listed in both, lists identical | OK |

No "says N, lists M" mismatches found in the six audited files.

---

*Audit performed read-only. Scripts used: index link/anchor checker and domain-completeness checker (scratchpad, not committed). Recommend routing H1/H2/M1–M4 to Planner as a character-sheet + II.1 amendment task, and M6 as a one-line fix in `software/tools/build_index.py` `_slugify` (emit one hyphen per whitespace character) followed by regeneration.*
