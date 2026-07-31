# PHB Rules Audit — Completeness & Internal Consistency

**Date:** 2026-07-30
**Scope:** `player_handbook/` — II.5 Backgrounds, II.6 Skills, III.1 Core Resolution, III.2 Adventuring, III.3 Combat, IV.1 Equipment, Quick_Start. Cross-reference targets (II.2, II.3, II.4/a/b/c, Appendix_Magic_Domains, ToC, mm_manual) consulted read-only for verification.
**Method:** Every numeric claim counted against its list; every cross-reference resolved to its target; all 15 Backgrounds checked for all five elements and for skill/domain existence; all skills referenced in scope checked against II.6; all combat subsystems and condition names traced; vignette arithmetic recomputed.

## Summary

The chapters are in strong shape overall: 30+ count claims and cross-references verify cleanly, all 15 skills match between summary table and full list, all skills and domains referenced by Backgrounds exist, all combat vignette Resolve/Endurance arithmetic is correct, and no TODO/TBD stubs exist. Twelve findings: **1 High** (Guild Apprentice is missing its Specialty — the "claims five elements, lists four" issue), **5 Medium** (0-Endurance vs. free-reaction contradiction, quick-ref exchange flow inventing action categories, the undefined "Reckless Press" mechanic, and two Threat Clock math errors in III.2), and **6 Low**.

---

## Findings

### High

**H1. Guild Apprentice Background is missing its Specialty — the five-elements claim fails for it.**
- `player_handbook/II.5_Character_Creation_Backgrounds.md:15` — "Every Background — pre-built or custom — has five elements." (Title, Description, Starting Skill, Secondary Skill/domain origin, Specialty.)
- `II.5:187–197` — Guild Apprentice lists only four: Title (189), Description (191), Starting Skill (193), Secondary Skill/Domain origin (195/197). **No Specialty line.** The other 14 Backgrounds all have one — including the other two magic-capable Backgrounds, Hedge Scholar (`II.5:255`) and Temple Acolyte (`II.5:289`), proving magic-granting does not waive the Specialty.
- Confirmed as an omission rather than a design choice by `Quick_Start.md:36`, where Zahna (Background: Guild Apprentice) **has** a Specialty: "Artificers' Guild technical records — Standard becomes Easy when directly applicable." That Specialty exists nowhere in II.5.

### Medium

**M1. 0-Endurance rule contradicts free/zero-cost reactions from Posture.**
- `III.3_Combat.md:45` — "with nothing in the tank you cannot pay the cost — **Absorb** is your only reaction option."
- `III.3:167` — "Each reaction costs Endurance **unless your Posture reduces the cost**. If your Endurance is at 0, only Absorb is available."
- `III.3:88` — Withdrawn: "All reactions are free"; `III.3:87` — Defensive: "−1 Endurance cost per reaction (min 0)", making Dodge/Parry cost 0.
- The stated rationale for the 0-Endurance restriction is inability to pay — but Withdrawn makes all reactions free and Defensive makes them cost 0, so a 0-Endurance character in those postures *can* pay. Whether they may Dodge/Parry is unresolved; the two sentences at line 167 point in opposite directions.

**M2. Combat Quick Reference invents action categories the body text never defines.**
- `III.3:646` — Exchange flow step 2: "Declare actions (Strike / Support / Maneuver / **Magic** / **Withdraw**)".
- Body text: offensive actions are Strike, Maneuver, Support (`III.3:102–161`); "Withdrawn" is a **Posture** declared in step 1 (`III.3:65`, `III.3:88`), not an action, and magic "has the same action economy as a Strike" (`III.3:375`) rather than being its own action type. Body step 3 (`III.3:67`) says "an offensive action, a support action, or passes." Under the project's own rule that quick refs may only compress, never introduce wording the canonical section doesn't state, this listing is out of bounds — and "Withdraw" as a declarable action contradicts the posture model.

**M3. "Reckless Press" is a named mechanic used once and defined nowhere.**
- `III.3:395` — "**Gamble (Luck):** Spend a Spark and take a Reckless Press — add a die to a risky action the way Press adds a die through Endurance."
- Grep of the whole repo: the term appears only on this line. It is indistinguishable from an ordinary Spark spend (III.1:76 already grants +1d6-drop-lowest per Spark to *any* character), no Gamble roll is actually involved despite appearing under the Gamble entry, and no rules text says what "Reckless" adds. Either a dangling concept from an earlier draft or an unwritten mechanic.

**M4. Second Threat Clock in the vignette fills after only 3 advances on a 4-segment clock.**
- `III.2_Adventuring.md:11` — "A **Threat Clock** is a four-segment tracker."
- `III.2:96` — "I'm **restarting** the water's clock… It advances on Zahna's scramble up the millrace — a partial. It advances on Zulnut's. It **fills** on the beam itself settling deeper." A restarted (empty) clock shown advancing exactly three times and filling. Either an advance is missing or "restarting" secretly means something other than resetting; the first vignette (`III.2:43–57`) counts its four segments correctly, so this one reads as an error.

**M5. Threat Clock pacing math contradicts itself within one paragraph.**
- `III.2:19` — "Roughly 72% of rolls made near a hazard land on partial success or failure… A 4-segment clock, **at that rate**, fills in roughly 3–4 party rolls."
- At a 72% advance rate, 4 segments take ~5.6 rolls on average (4 ÷ 0.72); the chance of filling within 4 rolls is only ~27% (0.72⁴). "Roughly 3–4 party rolls" does not follow from the stated rate. One of the two numbers (the 72% or the 3–4 rolls) needs to change, or the derivation needs different wording.

### Low

**L1. Named NPC section narrows riders to Tier 2 only, contradicting the Strike rule.**
- `III.3:124` — a full-success rider is "a **Tier 1 or Tier 2** Condition of your choice."
- `III.3:317` — "A Named NPC can carry rider Conditions hung on it by a full-success Strike — **Staggered or Cornered**" (Tier 2 only; Winded/Off-Balance/Shaken not mentioned). Quick ref (`III.3:677`) agrees with line 124. Line 317 should acknowledge Tier 1 riders or state why Named NPCs ignore them.

**L2. Promised armor "Technique interactions" never appear in the Equipment chapter.**
- `III.3:287` — "The Equipment chapter covers specific armor types, weights, and any relevant Technique interactions."
- `IV.1_Equipment.md:31–50` — Armor section covers types and fictional weight but contains no Technique interactions (the chapter's only Technique note is Weapon Mastery for weapons, `IV.1:27`). Either trim the promise or add the content.

**L3. Quick Start example conflates the peer "Spark?" call with the Graceful Fail.**
- `Quick_Start.md:121–123` — another player calls "Spark?" and the MM responds "'you cannot tell which' is exactly the graceful failure."
- `III.1_Core_Resolution.md:72` — the Graceful Fail is explicitly "player-initiated. On any 6-, *you* may claim it — narrate how you make the failure worse." In the example, the failing player neither claims it nor narrates; what happens is the peer call (`III.1:70`), which the MM mislabels. Harmless in play but teaches the mechanism wrong in the one document meant for brand-new players.

**L4. Quick-ref "0 Endurance = Conditions land at full tier" overstates the body text.**
- `III.3:718` — "0 Endurance = Absorb only (Conditions land at full tier — no extra penalty)"; likewise `III.3:668` Absorb: "Take the hit at full tier."
- `III.3:47` — "Your armor still helps (see Armor)" at 0 Endurance, i.e., Conditions may still be downgraded by remaining armor budget. Minor compression drift, but "full tier" is literally wrong for an armored character.

**L5. Survival is the only skill no pre-built Background can grant.**
- `II.6:83` defines Survival (Mind/Wisdom). Across all 15 Backgrounds in II.5, every other skill appears as a Starting or Secondary Skill at least once; Survival never does. The thematically closest Background (Wilderness Scout, `II.5:155–165`) is Body-Facet and therefore barred from it by the Primary-Facet rule, even though its Specialty is tracking — Survival's signature use. Not a rules violation (custom Mind Backgrounds can take it), but an unexplained gap worth a deliberate decision.

**L6. Vignette gives Mordai a Technique with no on-page grounding.**
- `III.3:458–460` — Mordai declares "I have Weapon Mastery in blades" and the MM applies the one-step-easier effect. The effect matches II.4a:32 exactly (pass), but nothing in the scope files establishes that Mordai has reached Body Facet level 1; the Quick_Start version of Mordai lists no Techniques. Fine if the vignette is set later in a campaign; a half-sentence saying so would prevent readers from assuming starting characters have Techniques.

### Out-of-scope observation (found while verifying II.6's cross-reference)

- `II.4_Character_Creation_Facets.md:116` — "His **Knowledge rank ticks to Practiced**" (and `II.4:120` "A Knowledge advancement…"). Knowledge is an *attribute* (rated 1–3); only *skills* have Novice/Practiced ranks. Almost certainly should read **Lore**. II.4 is outside this audit's scope; noting for a future pass.

---

## Verification Table — Count Claims and Cross-References Checked

| # | Claim / Reference | Location | Claimed | Actual | Result |
|---|---|---|---|---|---|
| 1 | "three things the fiction made true about you" | II.5:7 | 3 | 3 (skill, second skill, specialty) | PASS |
| 2 | "Every Background… has five elements" | II.5:15 | 5 | 14 of 15 Backgrounds have 5; Guild Apprentice has 4 | **FAIL (H1)** |
| 3 | Custom Background "process is five steps" | II.5:83 | 5 | 5 (plus documented magic swap of step 4) | PASS |
| 4 | Pre-built Backgrounds per Facet (structural) | II.5:109–331 | 5 Body / 5 Mind / 5 Soul | 5 / 5 / 5 = 15 | PASS |
| 5 | Every Background skill exists in II.6, from own Primary Facet | II.5 all | — | Combat, Endurance, Athletics, Finesse, Stealth, Lore, Investigate, Craft, Insight, Perform, Persuade, Deceive, Attune, Gamble — all exist, all Facet-legal | PASS |
| 6 | Background domain lists exist ("Domains of the Mind/Soul list") | II.5:197,253,287 | — | Appendix_Magic_Domains.md:185 (Mind), :11 (Soul); Inscription (Focused) at :223 and II.3:213 | PASS |
| 7 | "Arcane Study" Technique exists | II.5:77 | — | II.4b:114 | PASS |
| 8 | II.2 archive vignette matches II.5's recap (Lore +1 / Charisma Hard / Easy keyring lift) | II.5:347–355 | — | II.2:166, II.2:180–182, II.2:196 | PASS |
| 9 | Skill summary table vs. full skill list | II.6:15–31 vs 49–102 | 15 = 15 | Same 15 skills, same Facets/attributes, descriptions consistent | PASS |
| 10 | Skill ranks (4) and marks 3/6/9; "two marks rather than three" with Background Mark | II.6:108–113, II.5:43 | — | Consistent; also matches II.4:57 (3 marks per rank) | PASS |
| 11 | Max combined modifier +4 (Strong +1 + Master +3) | II.6:115 | +4 | +1 + 3 = +4 | PASS |
| 12 | II.6 → II.4 advancement / skill-point economy / reflection scenes; → II.4a/b/c Technique trees | II.6:9 | — | All present in II.4 (:46, :57, :110–128) and II.4a/b/c | PASS |
| 13 | Three-tier outcome table (10+/7–9/6-) | III.1:7–11 | 3 | 3; identical everywhere it recurs (III.1:94–97, III.3:116–120, Quick_Start:9) | PASS |
| 14 | Attribute ratings 1–3 → −1/0/+1; 9 Minor Attributes; Majors Body/Mind/Soul | III.1:25–31 → II.2 | — | II.2:32,40,48,68–92 match; Quick_Start tables conform | PASS |
| 15 | Difficulty ladder (4 steps) | III.1:50–55 | 4 | 4; matches Quick_Start:147 and III.3 usage | PASS |
| 16 | "begins each session with 3 Sparks" | III.1:63 | 3 | Quick_Start pregens all list Sparks: 3 | PASS |
| 17 | Spark-earning methods (no count claimed) | III.1:69–72 | — | 4 listed, each defined | PASS |
| 18 | "only call for a roll when three conditions are met" | III.1:129 | 3 | 3 (also mirrors II.6:129–132's 3 bullets) | PASS |
| 19 | Group rolls → "Support (see Combat, Chapter III.3)" | III.1:121 | — | III.3:153–161 defines Support | PASS |
| 20 | "This chapter covers three things" | III.2:3 | 3 | 3 sections (Hazards / Recovery / Death); travel, downtime, exploration explicitly deferred | PASS |
| 21 | Threat Clock = 4 segments; first vignette fill count | III.2:11, 43–57 | 4 | 4 advances (1,2 → wind-back → 2,3,4) | PASS |
| 22 | Second vignette clock fill count | III.2:96 | 4 | 3 narrated advances | **FAIL (M4)** |
| 23 | "72% … fills in roughly 3–4 party rolls" | III.2:19 | 3–4 rolls | 4 ÷ 0.72 ≈ 5.6 rolls | **FAIL (M5)** |
| 24 | "Treated means one of three things" | III.2:70 | 3 | 3 | PASS |
| 25 | Condition tiers/names consistent III.2 ↔ III.3 | III.2:69–71 | — | Winded/Off-Balance/Shaken; Staggered/Cornered; Broken — identical | PASS |
| 26 | Endurance pool formula; range "3 … to 8"; example pools 5/3/3 | III.3:25–41 | — | 4−1+0=3 min, 4+1+3=8 max; Mordai/Zahna/Zulnut match Quick_Start attributes | PASS |
| 27 | Postures (4) — body table, quick ref, Quick_Start | III.3:83–88, 655–660, QS:151 | 4 | 4, effects consistent (incl. revised Aggressive first-reaction surcharge) | PASS |
| 28 | Reactions (4 defined); "all three active reactions" | III.3:173–219, 377 | 3 active | Dodge, Parry, Intercept named = 3 (Absorb passive) | PASS |
| 29 | Tier 1 = 3 conditions, Tier 2 = 2, Tier 3 = 1 | III.3:233–262, 266–272, 687–693 | 3/2/1 | 3/2/1, consistent incl. Quick_Start:153 | PASS |
| 30 | Strike depletion 2/1/0; PvP T2/T1; Mook 7+ (armored 10+) | III.3:124–126, 300, 671–683; IV.1:21 | — | Consistent across body, quick ref, Equipment | PASS |
| 31 | Armor budgets: Light 2 / Heavy 4, per scene | III.3:280–283, 710–713; IV.1:40–43 | 2/4 | 2/4 everywhere; no-stack + charge-not-spent rules consistent | PASS |
| 32 | Enemy armor = flat Resolve +1/+2; guardian 8+2=10 | III.3:314, 452 | — | Arithmetic correct | PASS |
| 33 | Enemy attack tiers Mook T1 / Named T2 / Boss T2; posture shifts reaction difficulty | III.3:337–355, 697–703 | — | Body and quick ref agree; vignette conforms | PASS |
| 34 | Vignette Resolve track 10→8→6→4→2→0; Endurance 5→3→1→0; net modifiers | III.3:452–598 | — | All recomputed, correct (incl. Hard/Easy net mods) | PASS |
| 35 | "Your Five Numbers On Screen" | III.3:721–731 | 5 | 5 rows | PASS |
| 36 | Strike/Parry weapon attribute → Chapter IV.1 | III.3:112, 195 | — | IV.1:13–19 weapon category table (5 categories) | PASS |
| 37 | Boss construction → "Mirror Master's chapter" | III.3:325 | — | mm_manual/MM1_Encounters_and_Enemies.md exists; explicit deferral | PASS |
| 38 | "Weapon Mastery from the Body Facet tree"; vignette effect | IV.1:27, III.3:460 | — | II.4a:32 — "one difficulty step easier" matches | PASS |
| 39 | Magical items "covered in a future chapter" | IV.1:75 | — | ToC:26 lists "IV.2 Magical Items *(Planned)*" — explicit deferral | PASS |
| 40 | Economy Facet module "(planned)" | IV.1:92 | — | Matches documented deferred modules; explicit | PASS |
| 41 | Quick_Start pregens: 18 attribute points each; modifiers; Endurance 3/5/3; skills match canon (.fof/memory) | QS:21–89 | — | Zahna 18, Mordai 18, Zulnut 18; all modifiers and pools correct | PASS |
| 42 | Quick_Start scene rolls (Knowledge+Lore +2; Strength Hard net +0; Wisdom +0; Easy +3) | QS:101–129 | — | All correct | PASS |
| 43 | "Cast a spell: Spirit or Knowledge (by tradition)" | QS:143 | — | Consistent with III.3:391 (Attune/Spirit) and Knowledge-rolled Mind magic (III.3:516, II.4b) | PASS |
| 44 | Quick_Start → "Wandering Disciple (custom — see Chapter II.5)" | QS:84 | — | II.5:355 names it as the custom five-step example | PASS |
| 45 | Stubs: TODO / TBD / placeholder / empty headings | all 7 files | — | None found | PASS |
