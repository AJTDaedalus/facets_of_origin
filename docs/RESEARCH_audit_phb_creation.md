# PHB Audit — Character Creation Chapters (I, II.1–II.4c)

**Date:** 2026-07-30
**Scope:** `player_handbook/I_Introduction.md`, `II.1_Character_Creation_Overview.md`, `II.2_Character_Creation_Attributes.md`, `II.3_Magic.md`, `II.4_Character_Creation_Facets.md`, `II.4a/b/c` Facet chapters. Cross-reference targets checked: III.1, III.2, III.3, II.5, II.6, IV.1, `Appendix_Magic_Domains.md`, `Glossary.md`, `Table_of_Contents.md`, `Quick_Start.md`, MM manual (reflection-scene promise).
**Method:** Read all eight scope files in full; verified every numeric claim against the actual enumerated items; followed every cross-reference to its target; compared the three Facet chapters section-by-section; searched for TODO/TBD/placeholder markers (none found).

---

## Summary

The chapters are in strong shape overall: no stubs or placeholder text exist, every "see Chapter X" pointer resolves to a real section that contains what was promised, and 27 of 30 count-claims verify exactly. The audit found **3 High**, **7 Medium**, and **6 Low** findings. The most important are: (1) a point-buy arithmetic example in II.2 that is mathematically wrong (claims "net zero" for a distribution that totals 20, not 18); (2) the exact class of issue the user spotted — II.3 and the Glossary both claim the Ascendant Domain / Second Domain Techniques exist "in each Facet's tree," but only two of the three trees (Mind and Soul) contain them, and the Body tree (II.4a) has neither; and (3) the II.2 "Scholar" example describes the character as "Strong in Luck" when its own stat line sets Luck to 2 (Average). Structurally, II.4a (Body) is missing the Facet intro section its Mind and Soul siblings have, and the three chapters use three different heading conventions.

---

## Findings

### High

**H1. Point-buy example arithmetic is wrong — claims "net zero" for a 20-point spread**
`player_handbook/II.2_Character_Creation_Attributes.md:102`
> "Four attributes at 3 with two attributes at 1 and three at 2 is also net zero: four extra points spent, two saved, three at baseline."

Four 3s cost +4, two 1s save −2 → net **+2**, for a total of **20 points**, not 18. The passage even states "four extra points spent, two saved" and then calls that net zero. This is the sidebar that teaches players how to verify their own point-buy, and its second worked example is illegal under the 18-point rule stated one paragraph earlier (line 98). A legal variant would be four 3s and **four** 1s (with one at 2), or three 3s and three 1s.

**H2. "Ascendant Domain (Tier 3, in each Facet's tree)" — only two of three trees have it**
`player_handbook/II.3_Magic.md:246`
> "Prismatic domains require the **Ascendant Domain** Technique (Tier 3, in each Facet's tree)…"

There are three Facet trees (II.4:9), but Ascendant Domain exists only in the Mind tree (Archive branch, `II.4b:140`) and the Soul tree (Communion branch, `II.4c:137`). The Body tree (`II.4a_Character_Creation_Facet_Body.md`) contains no Ascendant Domain — nor any magic-related Technique. Body magic's deferral is explained at II.3:250-252, but that explanation covers Body *domains*, not this sentence, which flatly asserts the Technique appears in every tree. This is the "claims three, delivers two" class the audit was asked to catch. Same wording problem is echoed in the Appendix framing (Soul: "Tier 3, Communion branch", Mind: "Tier 3, Archive branch" — those two are correct; only II.3's "each Facet's tree" is wrong).

**H3. Glossary: "Second Domain — A Tier 3 Technique, in each Facet's tree"**
`player_handbook/Glossary.md:90`
> "**Second Domain** — A Tier 3 Technique, in each Facet's tree, that grants a second standard magical domain…"

Second Domain exists only in the Mind tree (`II.4b:137`) and Soul tree (`II.4c:134`). The Body tree has no Second Domain. Same class as H2, and it violates the project rule that compressions may never state something the canonical text doesn't support — a Body-Facet reader sent to their tree by this entry finds nothing. ("in each Facet's tree" should be "in the Mind and Soul trees" or equivalent, here and in H2.)

### Medium

**M1. "The Scholar" example contradicts its own stat line — "Strong in Luck" with Luck 2**
`player_handbook/II.2_Character_Creation_Attributes.md:118,121`
> "Spirit 2, Luck 2, Charisma 1 → Soul sum: 5 → **Soul +0**" … "Strong in Luck despite everything — perhaps they survive on cleverness and fortune in equal measure."

The example sets Luck to 2, which the game's own table (line 61) labels **Average**, then describes the character as "Strong in Luck" — "Strong" being the defined label for rating 3. (The sentence reads like a residue of Zahna's actual build, which has Luck 3.) Either the stat line or the prose is wrong; the point total (18) only balances as written.

**M2. Soul "Second Domain" is missing the prerequisite line its Mind twin has**
`player_handbook/II.4c_Character_Creation_Facet_Soul.md:134-135` vs `II.4b_Character_Creation_Facet_Mind.md:137-138`
The Mind version opens "*Requires an existing Mind domain (Arcane Study).*" The Soul version has no prerequisite line at all — it jumps straight to "You have grown into a second intuitive magical domain…" (Soul's *Ascendant Domain* at II.4c:138 **does** carry the parallel prereq line, so the omission is clearly accidental.) As written, the only gate on Soul Second Domain is the generic "one Communion Tier 2" branch rule — a character who never took Spiritual Domain could legally take a "second" domain without a first.

**M3. "Pushing scope" references a scope ceiling that no rule defines**
`player_handbook/II.3_Magic.md:170`
> "**Pushing scope:** By spending a Spark, a character may attempt an effect one scope tier beyond their domain's natural ceiling. A Standard domain character whose Major effects are normally Very Hard may spend a Spark to push to a scope that would otherwise be unavailable…"

The base difficulty table (II.3:85-89) gives **every** domain type a difficulty at **every** scope — Minor, Significant, Major are all already available to all three types, and no scope above Major exists. So "one scope tier beyond their domain's natural ceiling" has no referent: the rule cannot be applied as written. (The only place a scope ceiling exists is the pre-Technique Minor-only limit at II.3:229, which this paragraph does not mention.) Either a scope-ceiling concept was removed from an earlier draft without updating this rule, or the rule intends something like "beyond Major" that is never defined.

**M4. II.3 promises Technique effects that no Technique provides**
`player_handbook/II.3_Magic.md:93`
> "A Tier 1 Soul Technique might make Minor effects in your domain one step easier; a Tier 2 Technique might remove unintended collateral within your declared intent."

Both examples are phrased as illustrations, but neither exists anywhere: no Technique in II.4a/b/c eases Minor-scope magic difficulty, and none removes collateral from a declared intent. The Soul Tier 1 Techniques are Read the Room, Lasting Impression, When It Matters, The Uncanny Angle, Sense the Unseen, Spiritual Domain — none matches. A reader who goes hunting for these "example" Techniques comes up empty.

**M5. Zulnut's Finesse contradicts itself across II.2 and II.4**
`player_handbook/II.4_Character_Creation_Facets.md:59,73` vs `II.2_Character_Creation_Attributes.md:200`
II.2's vignette (early play) has Zulnut roll "**Finesse Practiced (+1)**" — Finesse is his Background Starting Skill (also confirmed by `characters/Zulnut.fof`). But II.4's advancement examples show him advancing Finesse *to* Practiced through play: line 59 ("Next session, one more mark advances Finesse to Practiced") and line 73 ("Finesse to Practiced (5)"). Novice→Practiced can only happen once, and canonically it happened at creation. Additionally, the line-59 example only works arithmetically if the "1 point left" is also spent on Finesse (giving 2 marks + 1 next session = 3), but the text never says he spends it — and line 53 says unspent points are lost, so the example as written leaves Finesse one mark short.

**M6. II.4a (Body) is missing the Facet introduction section its siblings have**
`player_handbook/II.4a_Character_Creation_Facet_Body.md:1-3`
II.4b opens with "## The Mind Facet" (5 lines of framing prose, II.4b:3-7) and II.4c with "## The Soul Facet" (II.4c:3-5). II.4a has no "The Body Facet" section at all — it jumps from the chapter title straight to "### Skills of the Body." The Body Facet's only descriptive prose lives back in II.4:13, which is one sentence, not parallel to the sibling intros. II.4a is also the shortest of the three (124 lines vs 143/140) purely because of this missing section.

**M7. Technique-count asymmetry across the three trees is unexplained**
`II.4a` (Body): 18 Techniques — every branch is 2/2/2 per tier.
`II.4b` (Mind): 20 — Archive Tier 3 has **4** (The Knowledge That Saves, Deep Archive, Second Domain, Ascendant Domain).
`II.4c` (Soul): 19 — Communion Tier 3 has **3** (Hold the Line, Second Domain, Ascendant Domain).
The magic Techniques (Second/Ascendant Domain) explain Mind and Soul exceeding Body, but Mind's magic branch also has **two** non-magic Tier 3 picks where Soul's has one — so a Communion character has strictly fewer Tier 3 options than an Archive character for no stated reason. If intentional, nothing marks it as such; if not, Soul's Communion Tier 3 is one Technique short of parallel.

### Low

**L1. "Following the same structure as Soul" — the structures differ**
`player_handbook/Appendix_Magic_Domains.md:189`
> "The mind domain list includes six core domains and three prismatic domains, following the same structure as Soul."

Soul has **nine** core + three prismatic (Appendix:15); Mind has six + three. Both individual counts verify against the lists, but "same structure" is only true of the core/prismatic split, not the counts — misleading phrasing in exactly the count-claim category.

**L2. Body-magic deferral is explained *after* the reader hits the two-Facet domain list**
`player_handbook/II.3_Magic.md:186-223` vs `II.3:250-252`
The Domain Quick Reference ("All 21 domains") lists only Soul and Mind sections. The explanation that Body domains are deferred to the Shattered Origin setting Facet arrives ~60 lines later ("A Brief Note on Body Magic"). A reader who knows there are three Facets sees a 2-of-3 enumeration with no signpost; a one-line forward pointer in the Quick Reference intro would close the gap. (The deferral itself is explicit and well-written — this is ordering, not a missing explanation.)

**L3. The "Ascendant Domain is taken once" restriction lives only in II.3**
`player_handbook/II.3_Magic.md:246` vs `II.4b:140-141`, `II.4c:137-138`
"Ascendant Domain is taken once, however many Facet trees they eventually climb" appears only in II.3. Neither Technique entry states or points to the once-only rule (by contrast, both Second Domain entries do carry their own "A character holds one Second Domain" line). A reader working from the tree chapters alone would miss it.

**L4. Glossary source pointers cite only one of each Technique's two homes**
`player_handbook/Glossary.md:12,90`
Ascendant Domain cites *(II.4b)* only; Second Domain cites *(II.4c)* only. Each exists in both II.4b and II.4c.

**L5. Duplicate pointer sentence in II.3**
`player_handbook/II.3_Magic.md:188` and `:223`
"Full descriptions of all 21 domains … are in the **Appendix: Magic Domain Catalog**" appears nearly verbatim at both the top and bottom of the 35-line Quick Reference section.

**L6. ToC titles for II.4a-c don't match the chapter files**
`player_handbook/Table_of_Contents.md:13-15`
ToC lists "II.4a Facets & Advancement (Body)" etc.; the files are titled "Character Creation: Facet of the Body" etc. Cosmetic, but the ToC is the first place a reader looks up a chapter name.

---

## Non-findings worth recording

- **No stubs or placeholders anywhere in scope**: zero hits for TODO/TBD/placeholder/FIXME/"to be written" across all of `player_handbook/`. No empty sections or headings without bodies.
- **The suspected "three magic traditions" issue does not exist as such**: II.3:101 introduces exactly two magical traditions (Spirit-governed intuitive, Knowledge-governed scholarly) and never claims a third; no scope file claims "three traditions." The real instances of the user's issue class are H2/H3 ("in each Facet's tree" — three implied, two delivered).
- **All cross-references resolve and deliver what they promise**: II.2→III.1 (Sparks, saving throws, contested rolls, difficulty all present); II.3→III.3 "Magic in Combat" (III.3:371-381 covers all four promised topics: casting time, reactions, Conditions, scope difficulty); II.3→II.5 (domain-origin Backgrounds exist and use "replaces secondary skill" wording consistently); II.3→Appendix (catalog matches the quick-reference lists exactly — every domain name and type agrees); II.4a/b/c→II.6 (all 15 skills described, tables agree with the Facet chapters skill-for-skill and attribute-for-attribute); II.4:128→MM guide (MM3 covers reflection scenes); I_Intro→Quick Start (exists, contains the promised pre-gen characters, one-rule summary, and example scene).
- **Rules consistency across scope files is otherwise good**: skill rank modifiers (II.4:33-38 vs II.6:108-115), mark thresholds (3/6/9), Broad-domain difficulty and Spark ceiling (II.3 table vs both Ascendant Domain entries vs Appendix:142), Minor-scope pre-Technique rule (II.3:229 vs Quick Start Zahna), branch/tier prerequisites (II.4:83 vs every tree's tier notes), and Facet-level math (5 advances/level, 15 cap, Major every 3 levels) all agree.

---

## Count-Claim Verification Table

| File:Line | Claim | Actual | Verdict |
|---|---|---|---|
| II.1:11 | sheet "has six sections" | 6 rows in table | PASS |
| II.1:15 | "nine Minor Attributes" (named) / "three Major Attributes" | 9 named / 3 named | PASS |
| II.1:18 | "All 15 skills across the three Facets" | 15 in II.6 (5+5+5) | PASS |
| II.2:9-11 | 3 Major Attributes; "three beneath each Major" | 3; 3×3 | PASS |
| II.2:24 | Major "derived from its three Minor Attributes" | 3 per Major | PASS |
| II.2:56 | "three-point scale" | ratings 1/2/3 | PASS |
| II.2:98 | "18 points … nine Minor Attributes" | consistent | PASS |
| II.2:102 | "Four at 3, two at 1, three at 2 is also net zero" | totals **20**, net **+2** | **FAIL (H1)** |
| II.2:117-119 | Scholar example "Total points spent: 18 ✓" | 4+9+5 = 18 | PASS (but see M1: "Strong in Luck" vs Luck 2) |
| II.2:129-142 | 3 outcome tiers; 4 difficulty steps | 3 rows; 4 rows | PASS |
| II.3:13 | "The Three Elements" | Domain, Intent, Scope = 3 | PASS |
| II.3:43-49 | 3 scopes | Minor/Significant/Major | PASS |
| II.3:71 | "There are three domain types" | Focused, Standard, Broad = 3 | PASS |
| II.3:111 | "same three outcome tiers" | 10+ / 7-9 / 6− | PASS |
| II.3:188 | "All 21 domains at a glance" | 12 Soul + 9 Mind = 21 | PASS |
| II.3:223 | "all 21 domains" in Appendix | 21 in Appendix | PASS |
| II.3:246 | Ascendant Domain "in each Facet's tree" (3 trees) | in **2** of 3 trees | **FAIL (H2)** |
| II.4:9 | "There are three Facets" | 3 described | PASS |
| II.4:31 | "Skills have four ranks" | 4 rows | PASS |
| II.4:46 | "4 skill points" per session | examples spend 4 | PASS |
| II.4:57 | advance at "3 marks" | matches II.6 (3/6/9) | PASS |
| II.4:69 | "5 skills and 3 possible advances each … 15 total" | 5 skills/Facet; 15 | PASS |
| II.4:83 | "The Technique tree has three tiers" | Tiers 1-3 in all trees | PASS |
| II.4:91 | Major Advancement "every 3 Facet levels" | internally consistent (:93) | PASS |
| II.4a:19 | Body tree "has three branches" | Might, Grace, Iron = 3 | PASS |
| II.4b:27 | Mind tree "has three branches" | Clarity, Instinct, Archive = 3 | PASS |
| II.4c:25 | Soul tree "has three branches" | Presence, Fortune, Communion = 3 | PASS |
| Appendix:3 | "all 21 magic domains" | 9+3+6+3 = 21 | PASS |
| Appendix:7 | "three example intents per scope" | 3 per scope, all 21 domains (spot-checked all) | PASS |
| Appendix:15 | Soul: "nine core domains and three prismatic" | 9 core + 3 prismatic listed | PASS |
| Appendix:189 | Mind: "six core … three prismatic, following the same structure as Soul" | 6+3 listed; Soul is 9+3 | counts PASS / phrasing **FAIL (L1)** |
| Glossary:90 | Second Domain "in each Facet's tree" | in **2** of 3 trees | **FAIL (H3)** |
