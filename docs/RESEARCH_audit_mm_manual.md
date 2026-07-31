# RESEARCH: MM Manual Completeness & Consistency Audit

**Date:** 2026-07-30 · **Branch:** main · **Auditor:** Brain-tier read-only audit
**Scope:** `mm_manual/MM1–MM5` cross-checked against `player_handbook/III.1`, `III.2`, `III.3`, `II.3`, `II.4`, `II.4c`, `II.5`, `enemies/*.fof`, `software/facets/base/facet.yaml`, `research/simulation_log.md`.

---

## Summary

The MM manual is in strong shape overall: MM5's numbers match the PHB in the large majority of cases, MM1's TR formula is internally consistent for Named/Boss tiers, all cross-references resolve, and no TODO/TBD stubs exist. The audit found **1 High**, **6 Medium**, and **9 Low** findings. The High finding is a Harbor Thug / "Basic Mook" TR contradiction: MM1 twice states TR 1 for a +0-attack Mook while its own formula (and the real `.fof` file) computes TR 2, and the `.fof` file contradicts itself internally. The Medium findings cluster into three classes: (a) MM5 quick-ref entries that drift from or have no canonical source (Maneuver outcome wording, magic-vs-Resolve, the MM Trouble Table, two Common Rulings), (b) MM1 stat-block language implying enemies roll dice, contradicting III.3's "NPCs do not roll" model, and (c) MM1 citing superseded v0.2 simulation data as confirmation. Coverage gaps: no MM-side guidance exists for magic adjudication, Specialties, hazards/threat clocks, or the death choice.

---

## Findings

### HIGH

**H1. Harbor Thug / Basic Mook TR: claimed 1, formula computes 2 (four-way contradiction)**
- `mm_manual/MM1_Encounters_and_Enemies.md:55` — Harbor Thug stat block: `TR: 1` with `Attack: +0`. Per MM1's own offense table (`MM1:92`, +0 → offense value 2), TR = 2 + 0 + 0 + 0 = **2**.
- `mm_manual/MM1_Encounters_and_Enemies.md:121` — "Basic Mook (unskilled, no armor) | 1 | Offense 2, Durability 0 — minimum 1". Offense 2 + Durability 0 = 2, not 1. "Minimum 1" is a floor (MM1:127) and cannot reduce a computed 2 to 1.
- `mm_manual/MM1_Encounters_and_Enemies.md:293` — the `.fof` example block shows `tr: 1` for harbor_thug.
- `enemies/harbor_thug.fof:18` — actual file says `tr: 2` with a correct formula comment ("offense(0→2) + durability(Mook→0) + armor(0) + techniques(0) = 2"), but its own notes at `enemies/harbor_thug.fof:29` say "TR 1 minimum by rule", contradicting the `tr: 2` field two lines of logic away.
- Impact: MM1's teaching examples and the canonical enemy file disagree on the baseline Mook TR; the chicken (`enemies/chicken.fof`, attack −1 → offense 1 → TR 1) is the only correct TR-1 baseline. Either the formula's +0→2 mapping or the "basic Mook = TR 1" claim must be corrected everywhere in the same pass.

### MEDIUM

**M1. MM5 Maneuver outcome reverses direction and shortens duration vs. canon**
- `mm_manual/MM5_Quick_Reference.md:107` — "Maneuver … 10+: target's next roll Easy. 7–9: Standard. 6-: backfire"
- `player_handbook/III.3_Combat.md:146` — "on a 10+, rolls **against** the target are Easy until the situation changes. On a 7–9 … rolls against the target stay at Standard"
- The MM5 wording reads as the *target's own* next roll becoming Easy (a buff to the enemy), where canon makes rolls *against* the target Easy; and "next roll" replaces "until the situation changes". A quick-ref wording change that alters the rule.

**M2. MM5 states "magic vs enemy depletes Resolve"; canonical III.3 Magic-in-Combat text still speaks only in Condition tiers**
- `mm_manual/MM5_Quick_Reference.md:109` — "Magic … vs enemy depletes Resolve like a Strike"
- `player_handbook/III.3_Combat.md:379` — "Magical Strikes apply Conditions on the same tier table as physical Strikes: a 10+ applies a Tier 2 Condition, a 7–9 applies a Tier 1 Condition…" (no mention of Resolve); likewise `III.3:391` (Attune: "the Condition tier follows the Strike outcome table").
- MM5's reading is almost certainly the intended v0.3 rule (consistent with `III.3:124` Strike-vs-enemy), but the canonical Magic-in-Combat and Attune paragraphs were never migrated to the Resolve model, so the quick ref currently states a rule the canonical section doesn't. Fix belongs in III.3 body text, then MM5 is a legitimate compression.

**M3. MM5 introduces content with no canonical source (violates "quick refs are compressions, not sources")**
- `mm_manual/MM5_Quick_Reference.md:284–293` — the **MM Trouble Table** (d6 generic 6- consequences) exists nowhere in the PHB or MM1–MM4. `player_handbook/Index.md:111,135,154` link to MM5 as its home, cementing a quick reference as the only source of a table.
- `mm_manual/MM5_Quick_Reference.md:299` — "Unnarrated details: Players cannot act on details the MM has not described." No canonical text anywhere states this rule.
- `mm_manual/MM5_Quick_Reference.md:302` — "'Can I try again?': Only if the fiction changes — new approach, new info, or time passes." No canonical text anywhere states this rule.
- Per CLAUDE.md's iron rule, each needs a canonical home (III.1 or an MM chapter body) or removal from MM5.

**M4. MM1 stat-block language implies enemies roll dice, contradicting III.3's "NPCs do not roll" model; Attack/Defense modifiers have no stated table-side use**
- `mm_manual/MM1_Encounters_and_Enemies.md:25–26` — "Attack: [roll modifier] … Defense: [roll modifier] — same modifier used for Parry; Dodge uses Dex modifier if different"; `MM1:197` — "Defense modifier (what they use to Parry; or note if they Dodge instead)"
- `player_handbook/III.3_Combat.md:331` — "NPCs do not roll dice. When an enemy attacks a PC, the PC rolls a reaction." PC Strikes against enemies are likewise resolved by the PC's roll against MM-set difficulty (`III.3:114`).
- Under the canonical model, an enemy's attack/defense modifiers are never rolled; they feed only the TR formula and the simulator. MM1 never tells the MM how (or whether) to translate these modifiers into play — e.g., into Strike/reaction difficulty. Both the contradictory "used for Parry" wording and the missing usage guidance need resolution.

**M5. MM1 cites superseded v0.2 simulation data as confirmation of the session arc**
- `mm_manual/MM1_Encounters_and_Enemies.md:411` — "Simulation data confirms this arc: Skirmish → Standard survives at 98%. Skirmish → Standard → Hard survives at 55%…"
- Source is Series 6/Series F (`research/simulation_log.md:352–353`), whose section is explicitly marked "**SUPERSEDED (v0.2 semantics)**" (`research/simulation_log.md:365`), and those runs defined Skirmish/Standard/Hard via the TR-budget multipliers that MM1 itself declares non-predictive (`MM1:155`). The numbers do not reflect the current Recipe-Table difficulty definitions (under which Hard alone is ~47%).

**M6. No MM-side guidance for adjudicating magic**
- Domain + Intent + Scope is the game's second-largest player-facing subsystem (II.3, ~300 lines), and adjudicating it is heavily MM-dependent: scope classification, domain boundary calls ("lean toward yes", `II.3:25`), 7–9 complication design, active-opposition difficulty (`III.3:381`). MM1–MM4 contain zero guidance on any of this — no section, no sidebar (MM5 only compresses the II.3 tables/templates). Given MM chapters exist for encounters, sessions, campaigns, and table-running, the absence of magic adjudication guidance is the largest coverage gap in the manual.

### LOW

**L1. MM3 advancement table double-counts the third Technique**
- `mm_manual/MM3_Campaign_Design.md:218` — Facet Level 2 row: "a second and third Technique deepen their specialty". Level 2 grants only the second Technique; `MM3:219`'s Level-3 row correctly says "a third Technique unlock and the Major Advancement … land together" (per `II.4`: one Technique per Facet level).

**L2. MM5 "Spark Flow" adds guidance not in MM2, and flips MM2's midpoint diagnostic**
- `mm_manual/MM5_Quick_Reference.md:59` — "Confirm at least 1-2 Graceful Fail claims **mid-session**, not just at session end" — MM2 (`MM2:502`) targets "1–2 per session across the whole table" with no mid-session timing rule.
- `MM5:61` — "If no Spark has been **earned** by the session's midpoint, you are being too conservative" vs `MM2:536` — "If a player hasn't **spent** a Spark by the session's midpoint, design a moment that rewards it." Earned≠spent; the quick ref invents a different diagnostic.
- `MM5:62–63` ("model it yourself by awarding one conspicuously", "Hoarding is a signal") — new guidance with no MM2 source.

**L3. MM5 target-economy "earn 2–4" drifts from MM2's table**
- `mm_manual/MM5_Quick_Reference.md:74` — "Spend 2–4, earn 2–4, end session with 2–4 unspent" vs `mm_manual/MM2_Session_Design.md:519–523` — earned column runs 1–2 / 2–3 / 3–4 and spent runs up to 4–6 (high-combat). Minor compression drift.

**L4. MM2 still defines Skirmish by the deprecated TR budget**
- `mm_manual/MM2_Session_Design.md:165` — "A Skirmish-budget fight (Party Strength × 1) against Mooks…" — MM1 (`MM1:155`) demoted the ×1/×2/×3/×4 budget to a non-predictive ordering check; the current definition of a Skirmish is a Mook-only roster (Recipe Table). MM2's framing predates the recalibration.

**L5. veteran_soldier.fof notes contradict MM1's actor-count doctrine**
- `enemies/veteran_soldier.fof:41–42` — "Solo encounter vs PS 3 party: effective TR 10 × 0.75 = 7.5. Expected difficulty: between Standard (~75% win) and Hard (~50% win)" — MM1 (`MM1:136`, `MM1:363`) states a solo Named is a near-certain clean win at any TR. Stale pre-Series-9 note in a reference file MM1's TR table points at.

**L6. MM1 internal pointer "(see *Armor*, above)" has no target section**
- `mm_manual/MM1_Encounters_and_Enemies.md:220` — MM1 has no section titled "Armor"; the nearest referents are the stat-block field note (`MM1:27`) and the TR "Armor bonus" table (`MM1:107`). Reader must guess.

**L7. MM1 "Mooks need only three things" vs. a four-step build list**
- `mm_manual/MM1_Encounters_and_Enemies.md:176` — "three things: an attack modifier, a fictional description, and a number"; the build procedure at `MM1:180–185` has four steps (armor decision added). Cosmetic counting mismatch of the claimed-vs-listed class.

**L8. MM5 magic section omits the "pushing scope" Spark use while including the other two Spark-magic rules**
- `player_handbook/II.3_Magic.md:170` defines three Spark-magic interactions (push scope one tier beyond ceiling; Focused eases Major; prismatic hard ceiling). `mm_manual/MM5_Quick_Reference.md:214–217` lists only the latter two. As a compression this is legal, but since MM5 enumerates Spark-magic rules, the omission reads as "this rule doesn't exist". Also: MM5:217 omits II.4c's "standard domains only" restriction on Second Domain (`II.4c:135`) — benign omission, noted for completeness.

**L9. MM coverage gaps beyond magic (no guidance where guidance is clearly needed)**
- **Specialties** — `II.5:49–51` gives the MM an adjudication rule (directly applicable → Standard becomes Easy; tangential → free information). Zero mentions in MM1–MM5, including MM5's Common Rulings, where it plainly belongs.
- **Hazards / threat clocks and the death choice** — `III.2` (Hazards and Threat Clocks; "When a Character Would Die": permanent scar vs. heroic death) is entirely MM-operated, yet no MM chapter references it; MM2's Session Zero lethality note (`MM2:317`) covers Broken-is-non-lethal but never points at the actual death rules.
- **Pinnacle Techniques** — `II.4` requires "MM approval" and earned-arc judgment; the MM manual offers no criteria (known open blocker in `research/advancement_priority_questions.md`).
- Adequately covered elsewhere (no finding): Sparks awarding (MM2), group rolls / contested rolls / saving throws (MM5 compressions of III.1), enemy attacks/reactions (III.3 + MM5), armor (III.3 + MM1 + MM5).

---

## MM5 Quick-Reference Rules vs. Canon (section-by-section)

| MM5 section (line) | Rule stated | Canonical source | Verdict |
|---|---|---|---|
| Core Resolution (7–14) | 2d6 + attr + skill + difficulty; 10+/7–9/6- tiers | III.1:5–11, 19 | **Pass** |
| Attribute Ratings (21–25) | 1/2/3 → −1/+0/+1 | III.1:25–29 | **Pass** |
| Difficulty (29–34) | Easy +1 / Standard 0 / Hard −1 / Very Hard −2 | III.1:52–55 | **Pass** |
| Skill Ranks (39–43) | Novice +0 … Master +3 | III.1:37–42 | **Pass** |
| Sparks earn/spend (49–53) | 4 earn routes; pre-roll only; +1d6 drop lowest; 3/session; Graceful Fail player-claimed | III.1:63–80; facet.yaml:956 | **Pass** |
| Spark Flow (57–63) | Mid-session GF target; earned-by-midpoint diagnostic; modeling nominations | MM2:498–536 | **Drift** (L2 — diagnostic keyed to earning vs MM2's spending; new guidance) |
| Spark Earning table (67–74) | Targets 2–3/player, 1–2 GF, 0–1 weakness; economy 2–4/2–4/2–4 | MM2:493–523 | **Partial pass** (L3 — "earn 2–4" vs table 1–4) |
| Exchange Flow (80–87) | 6-step flow, Resolve 2/1/0 | III.3:63–71, 644–651 | **Pass** |
| Postures (93–98) | Agg +1/+1-first-reaction-only; Def −1/−1 (min 0); Withdrawn free + recover 2 | III.3:85–88; facet.yaml:1267–1273 | **Pass** |
| Strike (106) | weapon attr + Combat (melee) / Finesse (ranged); Resolve −2/−1; 10+ rider | III.3:112, 124 | **Pass** |
| Maneuver (107) | "target's next roll Easy / Standard / backfire" | III.3:146 | **FAIL** (M1 — direction + duration drift) |
| Support (108) | +1d6 drop lowest OR difficulty one step easier, next roll | III.3:154–159 | **Pass** (non-stacking omitted; legal compression) |
| Magic action (109) | Knowledge/Spirit by tradition; vs enemy depletes Resolve | II.3:101; III.3:379 | **FAIL** (M2 — Resolve depletion not in canonical text) |
| Press (111) | 1 End pre-Strike, +1d6 drop lowest, stacks with Sparks | III.3:132–134 | **Pass** |
| Strike Outcomes (117–129) | −2/−1/0; rider rules; PvP T2/T1; default Standard | III.3:124–126, 114 | **Pass** |
| Reactions (135–143) | Dodge 1/Dex; Parry 1/weapon+Combat; Absorb 0; Intercept 2; 0 End = Absorb only | III.3:173–219, 45 | **Pass** |
| Enemy Attacks (148–156) | Mook T1 / Named T2 / Boss T2; posture shifts reaction difficulty; no stacking | III.3:335–359 | **Pass** |
| Group Rolls (161–164) | majority success, partial counts; lead roller + Support | III.1:115–121 | **Pass** |
| Conditions (170–179) | all six conditions, effects, durations; same-type stacking → Broken | III.3:229–272 | **Pass** |
| Armor (185–193) | Light 2 / Heavy 4 per scene; scene reset; charge kept when reaction supplies downgrade | III.3:278–287, 357–363 | **Pass** |
| Endurance (199–202) | 4 + Con + skill; range 3–8; 0 End Absorb-only, no extra penalty | III.3:25–45 | **Pass** |
| Magic scope table (208–217) | Focused/Standard/Broad grid; pre-technique Minor only; prismatic ceiling; Focused Spark ease; Second Domain +1 step | II.3:83–91, 170–174, 229; II.4c:134–135 | **Pass** (L8 — pushing-scope rule omitted; "standard domains only" omitted) |
| Magic 6- templates (219–227) | 6 templates + Graceful Fail option | II.3:124–140 | **Pass** (all six match) |
| TR formula/minimums (233–249) | formula, offense map, durability, armor, technique; minimums 1/8/12 | MM1:81–130 | **Pass** (inherits H1 at the Mook baseline) |
| Encounter Budget/Recipes (251–266) | budget = ordering check; recipes + win rates | MM1:134–166, 341–348 | **Pass** (Deadly "~17–22%" vs sim 16.5–22.5 — rounding) |
| Skill Advancement (272–278) | 4 SP use-it-or-lose-it; 3 marks/rank; 1/2 SP; 5 advances = Facet level; Technique per level; Major every 3 levels | II.4:46–108; facet.yaml:1037–1049 | **Pass** |
| MM Trouble Table (284–293) | d6 generic 6- consequences | — none — | **FAIL** (M3 — no canonical source) |
| Common Rulings (299–305) | unnarrated details; contested PvP/NPC; try again; when not to roll; saving throws; Mooks | III.1:104–135, 86–99; III.3:299–301 | **Partial** (M3 — "Unnarrated details" and "Can I try again?" have no canonical source; other four Pass) |

---

## Enemy TR Recomputation

Formula (`MM1:82`): TR = offense_value + durability(base Resolve) + armor_bonus + technique_bonus. Offense map: −2→0, −1→1, +0→2, +1→3, +2→4, +3→5, +4→6.

| Enemy | Attack mod | Offense | Durability | Armor | Techniques | **Computed TR** | `.fof` tr | MM1 states | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Chicken | −1 | 1 | 0 (Mook) | 0 | 0 | **1** | 1 (`chicken.fof:17`) | not in MM1 | ✓ consistent (the true TR-1 baseline) |
| Harbor Thug | +0 | 2 | 0 (Mook) | 0 | 0 | **2** | 2 (`harbor_thug.fof:18`) | **1** (MM1:55, MM1:293) | ✗ **H1** — MM1 wrong vs formula and file; file's own notes (line 29) also claim 1 |
| "Basic Mook" (MM1 row) | +0 | 2 | 0 | 0 | 0 | **2** | — | **1** (MM1:121) | ✗ **H1** — "minimum 1" cannot lower 2 to 1 |
| Skilled Mook (MM1 row) | +1 | 3 | 0 | 1 (light) | 0 | **4** | — | 4 (MM1:122) | ✓ |
| City Watch Sergeant | +2 | 4 | 3 | 1 (light) | 0 | **8** | 8 (`city_watch_sergeant.fof:13`) | 8 (MM1:44, 123) | ✓ (meets Named min 8) |
| Veteran Soldier | +3 | 5 | 4 | 1 (light) | 0 | **10** | 10 (`veteran_soldier.fof:13`) | 10 (MM1:124) | ✓ (stale solo-difficulty note in file — L5) |
| Archive Guardian | +3 | 5 | 8 | 2 (heavy) | 2 | **17** | 17 (`archive_guardian.fof:19`) | 17 (MM1:70, 125) | ✓ (meets Boss min 12; Resolve 8, phase at threshold 2 all match MM1 and III.3's in-play example) |

Resolve model check: MM1 uses the current Resolve model throughout (stat blocks, durability = base Resolve, armor adds flat Resolve, Mooks poolless, phase `resolve_threshold`) — fully consistent with III.3 and `facet.yaml:1342–1346` (`enemy_durability`), including the deprecation note for legacy `endurance` fields (MM1:266). No Endurance-based enemy language survives in MM1–MM5.

## Cross-Reference Check (all resolve)

- MM1:58/228 "from Chapter III.3" → Archive Guardian appears in III.3 In Play ✓; MM1 `#encounter-recipe-table` anchor ✓; MM1:139/339 `research/simulation_log.md` Series 9 / Part D exist (log lines 523, 591) ✓
- MM2:161 "Chapter III.3 … and MM1" ✓; MM2:155 "3-Clue Rule in the Improvisation section" ✓
- MM3:231 "PS-3 Recipe Table (MM1)" ✓; MM3:257 Techniques Weapon Mastery / Sharp Analysis / Commanding Presence all exist (`facet.yaml:284, 463, 729`) ✓; MM3:255 "reflection scene" defined in II.4 ✓
- MM5:193 "(III.3, *Armor and Reaction Downgrades*)" — section exists (III.3:357) ✓; MM5:219 "compressed from II.3" ✓; `Index.md` → `#mm-trouble-table` anchor exists ✓
- Only broken pointer: MM1:220 "(see *Armor*, above)" — no Armor section in MM1 (L6)

## Stubs / Placeholders

No TODO, TBD, FIXME, empty headings, or promised-but-missing subsections in any MM file. MM1's PS-4 table is explicitly and honestly labeled unvalidated (not a stub).

---

**Counts:** High 1 · Medium 6 · Low 9
