# RESEARCH — Facets d20 balance pass (tuning log and final tables)

*Balance tuner, 2026-09-28, branch `feat/facets-d20`. Owner brief: "work on balance… do
the math to make sure everyone is moderately balanced"; "combat not overly long" (a
standard fight 3–4 rounds); "it must be simple". Rules and data changed are recorded as
DESIGN v0.2 §12 decisions **V32–V42**; engine changes as `DESIGN_facets_d20_engine.md`
§4a (E-D16–E-D25). Every number here comes from `software/facets_d20/` through
`software/tools/d20_sim.py` (the full report: `RESEARCH_facets_d20_sim.md`; raw:
`software/research/facets_d20_sim_results.json`). Iteration numbers come from a scratch
harness that calls the same package functions (`analysis.task_fit`, `task_eval`,
`task_swap`, `sim.run_day`) at smaller n (150 fits, 150 days a cell); the final tables are
the tool's full run.*

## 1. Outcome

| Target | Before the pass | After |
|---|---|---|
| Primary measure | PI (power index) | **Swap test** on standard days (V32); PI secondary |
| Every preset and sim build within ±15% (L1/4/7/10) | PI: 2–3 of 12 presets in band; 19 misses on the first swap run | **All 12 presets and 17 sim builds inside ±15% at every level** (range −11% to +12%) |
| Hybrids ≤ best pure build of their Facet (from 4th); pure builds best at their job | Tinker +161% (PI) at 4th | **Every hybrid at or below; no DPR₁/DPR₃ job beaten by > 5%** |
| E-9 (hybrid's 4th/8th +2) | open | **Main track's ability** (V33); presets pin it |
| Clash 3–4 rounds at 1st–10th | 2.6–2.7 rounds at 5th–10th, wins 86–96% | **2.97–3.58 rounds**, 99–100% wins |
| 1st-level Clash lethality | a PC dies in 15.1% | **1.4%** (drops 19%) |
| Skirmish about 2 rounds | 1.8–2.1 | **1.9–2.4** |
| Battle wins 85–95% | 77–87% | **85–95%** |
| Day survived ≥ 80% | 25–65% (four Clashes) | **90–99%** (the day is three Clashes, V34); four Clashes 41–78% |
| MM arithmetic | table + four adjustment rows | Table 9–1 × players, Table 9–2, three one-line rules (boss ×2 HP, lone boss ×1.2, tired → one tier down) |

## 2. The balance measure (V32)

**Adopted: the swap test, primary; PI secondary.** The reference party (Fighter, Rogue,
Wizard, Priest) with the build swapped in for each member in turn plays standard days at
the level's Clash budget; the score is the party's share of HP lost per fight, reported
as `median ÷ build − 1`. Every build at a level plays the same dice (common random
numbers), 250 days × 4 positions (≈ 3,000 fights) a cell.

Why:
- **It measures the owner's question.** "Is everyone moderately balanced" at a table means
  "does the party do about as well with this character in it". PI multiplies a build's own
  damage by its own toughness, so a self-sufficient duelist squares its strengths and a
  healer or controller (whose value lands on allies) reads low. The engine measured the
  two disagreeing (Spearman 0.46–0.82, E-9); PI had Body at +19–44% while the swap test put
  Body builds mostly inside ±10%.
- **Days, not single fights.** A single Clash at "a third of each daily pool, rounded up"
  gives a two-slot 1st-level caster a slot every fight (1.5× its real rate) and a one-use
  feature one use every fight. Playing the day paces pools as at the table. Moving from
  single fights to days changed the picture (healers and 1st-level casters down 3–8
  points, Body martials up 3–7), which is why Second Wind and Martial Arts were trimmed
  late (§4, iterations 10–12).
- **Its unit is the tier.** ±15% HP lost per fight is about ±6% of the party's Threat
  capacity (HP lost grows like Threat^2.5 near a Clash), i.e. one member of four being
  roughly a quarter stronger or weaker — about as strict as ±15% PI.
- **Noise.** With common random numbers two identical builds score identically (the Monk
  and *monk_stunner* agree to the point); an equivalent pair (Wizard and *armored_caster*)
  agree within 1 point. Item 7's hybrid check allows +3 points for sampling noise.
- **PI stays** as a diagnostic, because it separates damage from durability (eDPR\*,
  eHP) and flags a build whose party value hides a solo weakness. Final Spearman PI vs
  swap: 0.93 / 0.81 / 0.69 / 0.79 at 1st/4th/7th/10th.

## 3. Encounters and the day

Iterations e0–e11 (scratch harness; clash rounds / wins across 1st–10th; 1st-level
Clash drop and death rates; three-Clash day survival from e2 on):

| Step | Change | Clash rounds | Clash wins | L1 drop / death | Day |
|---|---|---|---|---|---|
| start | engine report | 2.6–3.6 | 86–99% | 71% / 15.1% | 25–65% (4 Clashes) |
| e0 | fitting shapes: minions ≤ half a standard's CR (E-D20); Clockwork Guardian 5-ft (E-D16) | 2.85–3.76 | 96–99% | 67% / 14.7% | 33–81% (4) |
| e1 | 1st-level HP twice the hit die (later +8, V35); foes attack a random PC (E-D19) | 2.98–3.69 | 97–100% | 37% / 3.8% | 38–78% (4) |
| e2 | **the day = three Clashes, share ⅓** (V34) | 3.03–3.69 | 98–100% | 37% / 3.8% | **76–98%** |
| e3–e5 | talent and preset round 1–2; AI takes the higher EV (E-D18) | 3.00–3.47 | 97–100% | 32% / 3.4% | 85–99% |
| e7 | generic foes deal 15% non-weapon damage (E-D20) | 2.86–3.43 | 99–100% | 25% / 1.3% | 83–100% |
| e10 | 1st-level HP = hit die + 8 + Con (V35), Second Wind 1 use | 2.84–3.39 | 98–100% | 23% / 1.4% | 90–100% |
| e11 | **a boss has twice its HP** (V37) | 2.97–3.67 | 98–100% | 21% / 2.3% | 81–99% |
| final | full run (n 700 an evaluation cell) | **2.97–3.58** | **99–100%** | **19% / 1.4%** | **90–99%** |

What each did and why:
- **Minion cap (e0).** The fitting shapes let minion Threat (√(H × damage)) buy a few
  very-high-CR minions (a CR 13 "minion" at 7th level dealing 69 a turn). That, not the
  PCs, made 5th–10th-level Clashes 2.6 rounds and swingy. Capped at half a standard's CR,
  the count rises instead (up to 10).
- **1st level (e1, e10).** 8-HP wizards against 8-damage hits: a PC dropped in 71% of
  1st-level Clashes and died in 15%. Twice the hit die fixed lethality but gave Body +10
  HP against Mind +6 and left the Body caster +17% at 1st; **+8 HP for everyone** (V35)
  fixes lethality the same and helps the d6 as much as the d10.
- **The day (e2).** With a Clash at the middle of its band (27.5% HP), four in a row were
  survived 33–81% of the time; better Hit Dice (roll the maximum) moved it 2–10 points; a
  day of four only passes 80% with Clashes at ~16% HP, below the tier. **Three Clashes
  with a short rest after the 1st and 2nd** (V34) is survived 90–99%. A four-Clash day is
  now a hard day (41–78%), which the tired-party line covers.
- **Boss HP (e11).** Boss fights ran 2.1–2.6 rounds (the boss dies before it matters) and
  dragged 5th–6th-level Clashes under 3 rounds. ×1.5 gave 2.96–3.46; **×2** gives
  2.97–3.58 and cuts the lone-boss mispricing (a lone boss at the Clash budget cost
  34–69% HP at ×1; 32–58% at ×2). The boss column of Table 9–2 already includes it (boss =
  3.34 standards).
- **Lone boss (V42).** Measured mark-up that makes a lone boss a Clash: ×1.11–1.15 at
  1st–4th, ×1.20–1.24 at 5th–8th, ×1.33–1.35 at 9th–10th; median **×1.2**. ×1.5 (the
  engine's first idea) would make a lone boss a Skirmish at low levels.
- **Party size.** The budget is per character, so it already scales: measured −26% /
  +24% / +43% for three / five / six players against −25 / +25 / +50% by the rule. Six
  players get a slightly harder fight than a four-player Clash; noted, no line.
- **Tired party.** A party at half HP and half resources needs the Clash budget cut only
  6% to lose the same *share* of what it has left — so "build one tier down" is the safe
  one-line rule.

**Final encounter table for the baseline party (four 4th-level PCs).**

| Tier | Budget / character | Party budget | Rounds | HP lost | Wins | PC drops | PC dies |
|---|---|---|---|---|---|---|---|
| Skirmish | 19 | 76 | 2.15 | 10% | 100% | 0% | 0.0% |
| **Clash** | **30** | **120** | **3.46** | **27%** | **99.7%** | **2%** | **0.3%** |
| Battle | 34 | 136 | 4.62 | 48% | 88% | 23% | 3.4% |
| Desperate | 41 | 164 | 5.11 | 62% | 72% | 43% | 6.6% |

Adjustment lines: (1) **players**: budget × the number of players; (2) **a boss has
twice its stat block's HP** (priced in the boss column); (3) **a lone boss counts ×1.2**;
(4) **a tired party: one tier down**. Threat by CR (standard / minion / boss) at the CRs
a 4th-level party meets: CR 1/2 12/9/39, CR 1 18/11/60, CR 2 28/13/94, CR 3 37/15/124,
CR 4 46/17/154. Example Clash: one CR 3 boss (124 × 1.2 lone = 149 — too much) → a CR 2
boss (94) + three CR 1/2 minions (27) = 121.

## 4. Build tuning log (swap test)

Range = lowest to highest swap score among presets and sim builds; misses = cells outside
±15% (of 116). Earlier rows were measured on single fights, later on days (row 10).

| # | Change (decision) | Why | Range | Misses |
|---|---|---|---|---|
| 1 | Swap test primary (single fights); Clockwork Guardian 5 ft, Study on spell attacks (E-D16, E-D17) | measure; the Tinker's guard covered every ally every round | −24…+35 | 19 |
| 2 | Monk focus = half level; Channel 1 use (2 at 5th, 3 at 9th); Evoker's damage bonus from 1st; Guardian loses its 9th-level doubling; Loremaster Hardy at 7th (V39, V40) | Monk +33% at 7th; 1st-level healers +15–25%; Mind casters −15–41% at 1st | −25…+30 | 14 |
| 3 | Martial Arts die d4/d6/d8; Monk Alert → 9th; Druid Wider Study → The Tide; Field Kit half level (V39, V40) | Alert alone was worth ~10 points at 7th (side initiative in 3-round fights); Verdance/Beasts have little the Druid can use in a fight | −26…+17 | 7 |
| 4 | AI: area, aura and disable spells only when they beat the Attack action (E-D18); Anatomist +Int vs studied target; Master Plan two rounds from 5th; Mage Armor to the Common list; Loremaster Evoker at 9th, no armor, Con 14; Investigator Weapon Expert at 7th; spellblade takes Turn the Odds (V36, V39, V40) | Soul hybrids cast DC-14 Fireballs instead of attacking; Mind martials and the Loremaster (AC 12, 22 deaths per 500 days at 10th) −13…−26% | −21…+16 | 3 |
| 5 | `attack_ev` counts what the attack really does (E-D18); Weapon Expert's crit heal = half level; spellblade Dex 16 / Int 15 | the spellblade still chose Burning Hands over an attack worth more; the raging tank at 10th | −16…+15 | 1 |
| 6 | Common random numbers | two copies of the same build differed by 5 points | −17…+17 | 2 |
| 7 | **Swap test plays days** (E-D21) | pacing: see §2 | −14…+19 | 3 |
| 8 | Generic foes 15% non-weapon damage (E-D20) | rage resisted 100% of generic damage vs 85% of real monsters' | −17…+18 | 4 |
| 9 | Flurry costs 2 focus; Second Wind 1 use (2 at 5th); +8 HP at 1st instead of twice the die (V35, V39) | Monk +18% at 4th; Body at 1st–4th; the Body caster +15% at 1st | −12…+15 | 0 |
| 10 | Guardian reduces by half your level (V39) | the raging tank +15% at 10th (redirect, then resistance) | −12…+14 | 0 |
| 11 | Boss HP ×2 (V37); Investigator Anatomist at 3rd; spellblade takes Clockwork Guardian | fight length; the spellblade out-hit the Investigator at 4th (DPR₁ +9%) | −12…+12 | 0 |
| — | *tried*: a 9th-level scaling depth of 2 (lifted hybrids 4 points at 10th) | not needed after row 11, and it let two Soul hybrids out-hit the Soul pure martial (+9–10% DPR₁) — dropped, V28 kept | | |
| — | *tried*: casting-ability ASI for Steel-main hybrids (E-9 alternative) | Soul hybrids +1–3 at 10th, Body hybrids −4–12 — rejected (V33) | | |
| — | *tried*: no Stunning Strike; a Study buff (advantage every turn); rage +1; Channel 1d4 | little effect or not needed | | |
| final | full tool run | | **−11…+12** | **0** |

## 5. Final band table (swap test vs the preset median)

| Build | Kind | L1 | L4 | L7 | L10 | PI L1/4/7/10 |
|---|---|---|---|---|---|---|
| Fighter | preset | +5% | +1% | +2% | −1% | +42/−9/+30/−1 |
| Rogue | preset | −3% | −5% | +8% | +8% | +13/−20/+60/+31 |
| Barbarian | preset | +9% | +10% | +10% | +6% | +49/+29/+27/+2 |
| Monk | preset | +9% | +12% | +6% | +11% | +25/+7/+21/+7 |
| Wizard | preset | −6% | −1% | −2% | +1% | −19/+9/+27/+6 |
| Investigator | preset | +0% | −6% | −7% | −4% | +1/−22/−1/+1 |
| Loremaster | preset | −5% | −11% | −9% | −3% | −36/−29/−21/−29 |
| Tinker | preset | −1% | −1% | −6% | −7% | −12/−1/−15/−30 |
| Priest | preset | −0% | +7% | +6% | +4% | −1/+8/+1/+6 |
| Druid | preset | −10% | −7% | +7% | +6% | −31/−14/−2/−18 |
| Oracle | preset | +2% | +9% | −9% | −7% | −9/+1/−15/−22 |
| Oathsworn | preset | +6% | +1% | −4% | −10% | +52/+20/−1/−17 |
| *armored_caster* | sim | −6% | −1% | −2% | +1% | −26/+6/+19/+2 |
| *battle_priest* | sim | −3% | +5% | +4% | −7% | +2/+13/+9/−22 |
| *battle_priest_deep* | sim | +6% | −1% | −1% | +0% | +47/−5/−0/−5 |
| *body_battlemage* | sim | +5% | +3% | +4% | −5% | +38/+15/+4/−24 |
| *body_caster* | sim | +9% | −8% | +4% | −10% | +63/−25/−25/−25 |
| *body_ranger* | sim | +1% | +5% | +2% | +12% | −3/+5/+32/+30 |
| *double_cross* | sim | −6% | +1% | −4% | −2% | −23/+7/+13/+1 |
| *healer_engine* | sim | −0% | +11% | +6% | +5% | +4/+12/+0/+5 |
| *mind_controller* | sim | −8% | −4% | −1% | −1% | −38/−21/−15/−26 |
| *monk_stunner* | sim | +9% | +12% | +6% | +11% | +32/+7/+21/+8 |
| *paladin_max* | sim | +6% | +1% | −3% | −10% | +42/+19/+3/−15 |
| *reckless_striker* | sim | +6% | +7% | +6% | +6% | +34/+26/+51/+29 |
| *soul_blaster* | sim | −5% | +2% | −4% | −5% | −14/+7/+10/−2 |
| *soul_champion* | sim | +6% | −1% | −4% | −4% | +57/+2/−11/−13 |
| *spellblade* | sim | −0% | −2% | −6% | −8% | +4/+2/−17/−23 |
| *summoner* | sim | −1% | −8% | −2% | −5% | −8/−22/−28/−28 |
| *unbreakable* | sim | +8% | +6% | +12% | +12% | +54/+19/+35/+13 |

Facet means (swap): Body +4…+7%, Mind −3…−6%, Soul −2…+2% (±10% wanted). Hybrids
(item 7) are at or below their Facet's best pure build at 4th, 7th and 10th; no
Steel-main hybrid's DPR₁ beats its Facet's best pure martial by more than 5%, and no
hybrid's DPR₃ beats its tradition's best caster by more than 5% (full tables:
`RESEARCH_facets_d20_sim.md` §8). PI, the secondary measure, still spreads −38…+63%: it
is the solo measure and ranks Body tanks high and support casters low, as §2 explains.

## 6. SRD baselines (honesty check)

Each preset against its SRD 5.2.1 analogue on the swap test (how much *less* HP the party
loses with the preset than with the SRD class, same engine and combat rules; the SRD
builds keep SRD hit points):

| Preset vs SRD analogue | L1 | L4 | L7 | L10 |
|---|---|---|---|---|
| Fighter vs Champion | +13% | +8% | +10% | +17% |
| Rogue vs Thief | +24% | +16% | +37% | +33% |
| Barbarian vs Berserker | +23% | +11% | +8% | +20% |
| Wizard vs Evoker | +30% | +23% | +15% | +14% |
| Priest vs Life Cleric | +31% | +12% | +11% | +14% |
| Oathsworn vs Devotion Paladin | +25% | +25% | +16% | +18% |

The SRD baselines' median sits 11–19% below the preset median (−19% at 1st). **Where we
are deliberately stronger:** +8 HP at 1st level (V35; most of the 1st-level gap); five
broad talents with 5th/9th-level lines against one subclass; Mage Armor for every caster;
Evoker's damage bonus from 1st (SRD: 10th). **Largest gap:** the Rogue (+33–37% at
7th–10th): Precision + Marksman + Weapon Expert + Cunning is stronger than the SRD Thief,
whose own features the sim barely uses (Fast Hands, Use Magic Device). **Weaker than the
SRD in places, deliberately:** the Monk (half the SRD's focus, a smaller die, Flurry at 2
focus), Channel (one use at 1st), Guardian and Weapon Expert (halved), Second Wind (one
use at 1st).

## 7. Owner questions

- **OQ-1 — Is a day of three Clashes right?** *Background:* at a Clash that costs about a
  quarter of the party's HP, four Clashes with two short rests are survived only 41–78% of
  the time; three are survived 90–99%. A stronger short rest barely helps, because the
  losses come from fights 3 and 4 back to back. *Recommendation:* adopt three (done, V34):
  it suits short fights and roleplay-heavy sessions; the book tells the MM that a fourth
  Clash makes a hard day, and a tired party gets fights one tier down.
- **OQ-2 — Real monsters of one kind.** *Background:* the table is fitted on smoothed
  "average" monsters. Built from real SRD stat blocks, boss encounters land right (85–93%
  inside the Clash band) but groups of a single standard kind land in the Clash band only
  32–47% of the time and cost 40–45% HP — some real stat blocks hit harder than their HP
  suggests. *Recommendation:* a follow-up pass that prices each SRD monster's Threat from
  its own block in Table 9–2's appendix (the engine already can), rather than a new rule;
  until then the book says "a group of hard-hitting monsters counts as the next tier".
- **OQ-3 — Presets stronger than their SRD analogues.** *Background:* every preset beats
  its SRD class by 8–37% on party outcomes, mostly from +8 HP at 1st and broad talents.
  *Recommendation:* accept (the game is pitched at heroic, low-lethality tables); if the
  owner wants SRD parity, trim the Rogue first (Marksman's +2 from 5th).
- **OQ-4 — Boss hit points doubled.** *Background:* without it, bosses died in two rounds
  and 5th–6th-level fights ran under three rounds. The MM doubles a boss's HP when it
  appears (one line); Table 9–2 already prices it. *Recommendation:* keep — it is the
  simplest rule that fixed fight length and lone-boss pricing together.

## 8. Limits of the measurement

- Generic foes attack with weapons (plus a 15% non-weapon strike); save-based monster
  abilities appear only in the real-monster validation, so *Warden*, *Iron Mind*,
  *Indomitable* and *Evasion* are undervalued, and builds holding them (Priest, Oracle,
  Druid, the Soul hybrids) are, if anything, measured low.
- Not simulated: *Wild Shape* (the Druid fights as a caster), movement and positioning
  (Cunning's mobility, Guardian's and the construct's 5-ft reach are proxies), summoning
  spells, most utility spells, knacks other than *Field Medic*, Sparks from roleplay.
- Clash at 5th level is 2.97 ± 0.05 rounds — at the lower edge of 3–4.
- Noise: swap scores ±2 points (CRN), which is why item 7 allows +3 points.

## Book simplicity count

*Player-book writer, 2026-09-28. Recounted from the chapters as written (README, 01–08,
10; 09 is the MM's), by DESIGN §2's method: one pick = one decision, N picks from a list =
N, a free-text line = 1, accepting a printed value = 0. Where the book and DESIGN §2
disagree, the book's number is the one that stands.*

| Measure (DESIGN §2 target) | DESIGN §2.1 said | **Book as written** | Where |
|---|---|---|---|
| Creation from a preset (≤ 12) | 6 | **7**: card, name, Drives ×2, Specialty, language, keep/swap background | 02 *The Quick Way* |
| Creation, custom, listed background (≤ 18) | 12 non-caster · 13 caster · 14 Body caster | **12 · 13 · 14**: name/concept 1, Drives 2, Facet 1, background 1, Specialty 1, array 1, skills 2, talent 1, domain 0–1, Body tradition 0–1, kit 1, language 1 | 02 Table 2–1 |
| Creation, custom, written background (≤ 18) | 16 · 17 · 18 | **16 · 17 · 18** (+ three abilities as one pick, two skills, a knack; no tool) | 02 Table 2–1, 06 *Writing Your Own* |
| Choices at a level-up (≤ 1) | ≤ 1 | **1 at every level 2–10** (knack, talent or ability-or-knack); a Spell talent that brings a domain names it as part of the pick | 02 Table 2–5 |
| Choices over levels 2–10 | 9 + 0–2 domain namings | **9** + 0–2 domain namings (*Wider Study*, Deep Magic) | 02 Table 2–5 |
| Exception rules a player applies (≤ 5) | 3 | **3**: E1 one rider a turn (08), E2 one controlled creature (08), E3 Body names a tradition and counts +2 Steel (02, 03, 07). 01 item 13 names them as the only three | 01, 02, 03, 08 |
| MM rules described in the player book (not counted, DESIGN §2.4) | — | 4, all on §2.4's MM list, printed in 08 so the table knows what bosses and minions do: boss top-of-round turn; boss loses at most one turn a round to a disabling effect; minions die to any damage; mindless and bound foes never break | 08 *Kinds of Foe*, *Bloodied and Morale* |
| Mechanics per job | 1 / 1 / 1 / 1 | **1 / 1 / 1 / 1**: add a die = the Spark die (*Turn the Odds* spends it); roll twice = SRD advantage only (06 says a Spark never grants it); reroll = *Indomitable* only; resource-paid weapon damage = *Sworn Strike* only (05, 07 "No smite spells") | 03, 05, 06, 07 |
| Gates ("you can't take X") | 0 | **0**. Caps only: two cross-Facet talents, one tradition, d12 largest hit die | 02 |
| Chassis reading | 3-column Facet table, 7-rank table, main-track and upgrade sentences | Table 2–2, Table 2–3 (the seven ranks), one main-track paragraph, one upgrade paragraph, one lapse paragraph, the Soul worked example (Table 2–4) | 02 *Steel and Spell* |
| Talent entries a player reads | 26 + 13 knacks | **26 talents** (6 shared in 02, 6 Body in 03, 7 Mind in 04, 7 Soul in 05) + **13 knacks** (06) + 6 Facet features; menus 10 / 13 / 12. Each printed once (tested) | 02–06 |
| Spells a caster tracks | Common 14 + ~12 | Common list **15** (with *Mage Armor*, V36) + one domain (8–15 spells); +1 per *Wider Study*; +1 at Spell 3; no preparation | 07 |

**Reading 01 + 02 alone.** A preset player needs only 01 and 02: the card is the whole
sheet, and 02 explains Drives, Specialty and languages in the steps (06 has the longer
treatment). A custom build needs 02 plus its Facet's chapter for the talent text (the six
shared talents are in 02), 06 for the background list, and 07 if its first talent is a
Spell talent.

**Differences from DESIGN §2.** (1) The preset count is 7, not 6: DESIGN folded the name
into choosing the card; the book lists it as its own line. (2) The custom count matches.
(3) The chapter test (`software/tests/test_facets_d20_chapters.py`, 34 tests) holds the
counted material to the data: every talent, feature, knack, background and preset printed
once with the yaml's numbers, the preset cards' 1st-level HP/AC/attack/DC from the engine,
Chapter 07's slot tables, Common list and all 21 domain lists.


## Playtest fix pass

*Fix-pass lead, 2026-09-28, branch `feat/facets-d20`. Source: `docs/PLAYTEST_facets_d20_fresh_mm.md`
(MM #n = its ranked table, G = its guesses, §8 = its contradictions) and
`docs/PLAYTEST_facets_d20_fresh_player.md` (P #n = its ranked table, C = contradictions).
Decisions V43–V49 (below). Talent count, knacks and the even-level structure untouched
(owner question pending; Amendment 5 edges will slot into Table 2–5 beside the existing
pick). Every number re-derived with `python tools/d20_sim.py all --write` after the rule
changes; Table 9–2 regenerated with `python -m tools.build_d20_threat_table`.*

### Decisions

| # | Decision | Playtest ref | Where |
|---|---|---|---|
| **V43** | **Ties keep the main track you had** (was "Steel wins a tie"). Main track is walked talent by talent in the order taken; the track that pulls ahead wins, a tie changes nothing. | P #3 (the Full→Half trap), C2 | `build.main_track_history`, yaml `tracks.main_track.tie: existing`, 01, 02, 10 |
| **V44** | **Boss turn**: top of the round, and right after the first character's turn in the party's half; none in its side's half, so never back to back. One reaction a round and one Recharge roll a round (both at the top turn); a surprised boss loses its round-1 top turn; durations count the top turn; resolve triggers "with a save or without one"; Bloodied = half the doubled HP, immediate; reinforcements are budgeted (a fifth kept back) and act from the foes' next half. All boss rules in one list in 09; a boss step in Table 8–1; a worked boss round. | MM #1, #7, G1–G4, G6, G7, G10, G11, §8.1–3, §8.6 | `combat.round_order`, `turns_in_side_half`, `boss_turn_refreshes`, `begin_turn`; sim; 08, 09, 10 |
| **V45** | **Monster crit** = fixed damage + one roll of the dice (same mean as doubled dice, never below the fixed hit). | MM #13 | `combat.monster_damage`; 08, 09, 10 |
| **V46** | **Sparks after the call**: the MM says hit/miss (success/failure); a Spark may then be spent on a miss or failure (Turn the Odds: subtract from a hit or success) before consequences. Hidden AC/DC stays. | P #1 | `combat.spark_may_spend`; sim; 01, 06, 08, 10 |
| **V47** | **Hard hitters priced in Table 9–2** (× the measured mark-up in every role; the generator measures it every run), and **Recharge abilities add a quarter of their damage** (area doubling first). The "next tier up" rule is gone from 09 and the appendix. This implements owner Amendment 4 item 2 more precisely: the ruling's intent (hard hitters cost more) with the measured amount instead of a tier cliff. | MM #2, §8.5, OQ-2 | `analysis.hits_hard`, `ThreatModel.hard/price`, `task_monster_factor`, `monsters.turn_damage`; d20_sim 2b; appendix; 09 |
| **V48** | **Morale edges**: a boss can lead (minions check when it falls); leaderless minions check once at half down; a broken foe stops at once and flees on its next turn (provoking); "mindless and bound" given examples (intelligent undead and fiends break unless bound). | MM #5, G5, P #7 | `combat.leaderless_minions_check`; sim; 08, 09, 10 |
| **V49** | **Social defaults**: a stranger starts Neutral, the crossed Wary; one roll per character per person per scene; Intimidation fades one step toward Hostile; Influence in a fight stops a foe at Neutral or better. | MM #6, task 5 | new `software/facets_d20/social.py` (+ `tests/test_facets_d20_social.py`); 06, 08, 09, 10 |

### Conversion rules (MM #3), engine and 09 step 1–3

`monsters.turn_damage`, `monsters.effective_hp`, `ThreatModel.price`, each tested
(`TestConversionRules`): two routines → the higher; a save counts as a failed save
(half-on-success or not); damage that can catch more than one creature counts twice;
casters count their every-turn attack or cantrip, and spells with uses a day are spikes
(left out); Recharge adds a quarter (V47); resistance or immunity to what most of the party
deals doubles HP (× √2 on Threat); regeneration adds three rounds of it. A line on what the
number doesn't know (unreachable flyers, total immunity, take-out conditions such as a
ghoul's paralysis).

### The rest, by reference

- **MM #4, #8**: an MM half of 10 (Table 10–6 budget, generated-tested against the yaml;
  Table 10–7 tiers; adjustments; the boss list; morale; the day; social defaults). 10 only
  restates 08/09.
- **MM #4, #9, #11**: "*Boss at levels* is for four characters" (09 and the appendix
  text); a boss over three-quarters of the budget is flagged swingy; a lone boss ×1.2 and
  a boss whose company is under a fifth of it ×1.1 (measured: ×1.16 alone, ×1.06 at a
  fifth, ×0.99 at half; `analysis.boss_markup`).
- **MM #10**: *survive* defined (win every fight of the day; deaths reported separately);
  what a short rest gives back listed; 01 #6 now says Hit Dice still roll.
- **MM #12**: each preset card prints HP/AC (and DC) at 5th and 10th, tested against the engine.
- **MM "what I'd cut"**: *Heroic by Default*'s "one tier tougher" is now an MM Note dial, not a rule.
- **§8.7** "paralyse" → "paralyze". **§8.8 / P #10** *Soul modifier* defined wherever it's used and in 02 *Talents from Other Facets* (with *Study*-dependent talents and *Clockwork Guardian*'s Int).
- **P #2, C2**: rank gates as three numbered rules in 02 and 10; "all but the first rank" and "every rank after the first" gone; a boxed after-every-pick checklist in 02.
- **P #3**: hit points recalculated when the die shrinks, Hit Dice change size, lost armor training means no casting in that armor; a lapse example in the other direction (Steel-first Soul going Spell at 9th); engine tests (`test_lapse_shrinks_the_hit_die…`, `test_lapsed_armor_training…`).
- **P #4**: "a talent's own ability is not a spell" (02 *Reading a talent entry*, 03 *Rage*, 10), naming *Counterspell*, *Silence*, *Rage*, *Wild Shape* and the bonus-action spell rule.
- **P #5**: Steel depth ≥1 → a held weapon or shield is a focus and does somatic components (07, 03, 10).
- **P #6, C1**: skill overlap stated one way (02 step 6 and 06).
- **P #8** *Kindle* can target you. **P #11** *Wider Study* first = two domains. **P #12, C4** Body's +2 is "for the main track, not for depth" in 01, 02, 03, 10. **P #13** a Body dabbler tip in 03. **P #14** "(max 20)" moved. **P #15** 02 step 9 heading includes language. **P #16, C5** "talents grow on their own" fixed. **C3** the prismatic line in 05 now names all three pure casters. **C6** *Ensnaring Strike* removed from Verdance (the rule now says no list spell triggers on your next weapon hit); tested with the other smites.
- **P runners-up**: Help and "in a position to help" in 10; late arrivals act with their side from its next half (08); the preset names annotated in 02 as familiar shapes, not classes (Amendment 5 note; renaming is PQ-1).
- **Tinker (consequence of V43)**: *Weapon Expert* 1st, *Clockwork Guardian* 3rd, breastplate and shield from 1st; *battle_priest* keeps Spell main at 7th (no heavy armor).

### V43 measured: "ties to the existing main track" against "Steel wins ties"

Swap test, all 29 presets and sim builds, n = 250 days × 4 positions a cell (scratch harness
on `analysis.task_swap`, same seeds). Only two builds ever tie with Spell ahead first: the
Tinker (3rd–10th) and *battle_priest* (7th–10th).

| Variant | L1 range | L4 | L7 | L10 | Tinker L4/7/10 | *battle_priest* L7/L10 |
|---|---|---|---|---|---|---|
| A: Steel wins ties (old) | −10…+11 | −12…+9 | −8…+10 | −12…+13 | −2/−4/−7 | +4/−6 |
| B: existing, Tinker unchanged | −10…+11 | −11…+11 | **−16**…+10 | −12…+13 | −11/**−16**/−12 | +8/+5 |
| C: existing, Tinker Steel-first (adopted) | −10…+11 | −12…+9 | −8…+10 | −12…+13 | −2/−4/−7 | +8/+5 |

The band holds under C, and the trap is gone: a Spell-first hybrid keeps the Full table when
its second Steel talent ties the tracks. Adopted.

### Re-derived numbers (full tool run after V43–V49)

| | Before | After |
|---|---|---|
| Threat model | minion √(10.5 × d), boss × 3.34, never × 1.16 | minion **√(8.4 × d)**, boss **× 3.51**, never × 1.16, **hard hitter × 1.06** |
| Table 9–1, 4th level | 19 / 30 / 34 / 41 | **18 / 29 / 34 / 40** (every level within ±3 of before; 10th 66/95/110/120 → 63/92/109/118) |
| Clash, 1st–10th | 2.97–3.58 rounds, 99–100% wins | **2.96–3.51** rounds, 27–29% HP, **96–100%** wins (9th–10th 96.5%, just under the yaml's 97) |
| Baseline (four 4th) | Clash 3.46 rds, 27%, 99.7% | Skirmish 2.22 rds 11% · **Clash 3.51 rds, 27%, 99.7%, 0.3% death** · Battle 4.77, 51%, 86% · Desperate 5.28, 66%, 68% |
| Lone boss mark-up (measured) | ×1.20 | ×1.16 (the printed ×1.2 stands) |
| Party size (three / five / six) | −26 / +24 / +43% | −26 / **+23 / +40%** |
| Standard day survived | 90–99% | **86–99%** (1st, 9th, 10th at 86–87%; a PC death on 13% of 1st-level days, as before) |
| Hard day (four Clashes) | 41–78% | 38–77% |
| Swap band (±15%) | −11…+12, 0 misses | **−11…+15, 0 misses** (Monk +14.7% at 4th, *unbreakable* +13.6% at 10th are the edges) |
| Table 9–2 examples | Bandit Captain boss 83, Ogre boss 99, Knight 38, Owlbear boss 136 | 88, 104, **40** (hits hard), **151** (hits hard) |

Why the boss factor rose: with its second turn after the party's first character instead of
in its own half, a boss acts later on average when the foes win initiative and the party
gets a turn in before it acts twice; the boss is worth 3.51 standards instead of 3.34, and
the minion's measured durability fell (8.4). The Clash still lands at 3–3.5 rounds.

Test counts: `tests/test_facets_d20_*.py tests/test_no_private_canon.py` 683 passed; full suite
(`--ignore=tests/e2e`) 1774 passed.

### Deferred

- **P #9** preset cards listing 1st-level spells, saves and skill totals: a presentation
  pass (the cards stay the whole *decision* list; the numbers are one read of 07).
- **MM #3 flight/range and condition pricing**: guidance only ("what the number doesn't
  know"); pricing them needs positioning and conditions the simulator doesn't model.
- **Clash wins at 9th–10th 96.5%** against the yaml's 97% floor, and the 1st-level day
  death rate (13%): next balance pass.


## Playtest fixes — owner questions

*Fix-pass lead, 2026-09-28. Findings from the two fresh-eyes playtests that need a ruling
rather than a fix. Each has the background in plain words and a recommendation; nothing
here is changed in the books until the owner answers, unless it says "done, reversible".*

- **PQ-1 — Preset names that read as 5e class names.** *Background:* the player tester
  felt the twelve cards (Fighter, Rogue, Barbarian, Monk, Wizard, Priest, Druid, plus
  Investigator, Loremaster, Tinker, Oracle, Oathsworn) signal "5e classes, reassembled"
  and undercut "Facets, not classes". Renaming is not cheap: the names are ids across
  the yaml, the sim builds, the engine's pinned numbers, the balance tables and three
  chapters. *Done now (cheap):* 02 *Presets* says the names borrow familiar shapes so a
  player can find what they're after, and that every card is five picks anyone could make.
  *Recommendation:* keep the familiar names for the first human table (they are the
  fastest way in for a 5e player), and revisit after it; if the owner wants new names now,
  rename the seven that are SRD class names in one pass (display names only; ids can stay).
- **PQ-2 — The hard-hitter rule had it backwards.** *Background:* Amendment 4 item 2 said
  "a group of hard-hitting monsters counts as the next tier up". The fix pass measured
  every SRD monster as a group against the generic foes the budgets were fitted on (the
  generator now does this every run). Measured, hard hitters play about 6% above their square-law price, not a whole tier (a tier is +13–40%): median ratio 0.53 against 0.50 for the rest (×1.06). What made real single-kind groups play hot in OQ-2 was mostly the Recharge monsters (the young dragons, hell hound: +28–40%), whose breath the old pricing left out entirely; those now add a quarter of the breath. *Recommendation:* keep the measured
  factor in Table 9–2 (it is generated, like never-breaks) and the Recharge pricing; drop
  the interim rule for good (done).
- **PQ-3 — The Tinker's first level.** *Background:* with ties keeping the main track you
  had (V43), a Tinker that took *Clockwork Guardian* first would stay Spell main at 3rd and
  never get medium armor, shields or the d8 (−16% at 7th, outside the band). The card now
  takes *Weapon Expert* at 1st and *Clockwork Guardian* at 3rd, and starts in breastplate
  and shield. Its numbers are back where they were (−4% to −7%). *Recommendation:* accept;
  the guardian arriving at 3rd is the one visible change.
- **PQ-4 — Influence ends a fight.** *Background:* the MM tester asked what a Neutral
  enemy does mid-fight. The fix pass wrote "a foe moved to Neutral or better stops
  fighting, as if it had broken". That makes talking a real combat option (one Influence
  action at DC 10–20 against a Bloodied foe can end its part in the fight), which is on
  brand but untested in the simulator (Influence isn't simulated). *Recommendation:* keep
  it, and watch it at the first human table; if it proves too strong, require the foe to
  be Bloodied first.


## Edges pass

*Edges designer, 2026-09-28, branch `feat/facets-d20`. Owner ruling: BRIEF Amendment 5
(an edge at 2nd/4th/6th/8th/10th beside the knack or ability pick; even levels become two
small picks; creation unchanged; ≤5 exceptions and one mechanic per job stand). Design:
DESIGN v0.2 §1.3b, §1.4b, §2.3, §3.6; decisions **V50–V56**. Every number re-derived with
`python tools/d20_sim.py all --write` after the last change; Table 9–2 regenerated with
`python -m tools.build_d20_threat_table`; the printed encounter numbers in 09 and 10 synced
from the yaml. Iteration numbers come from a scratch harness driving the same package
functions (`analysis.party_for`, `day_encounters`, `sim.run_day`) at n = 150–500 days × 4
positions, same seeds as the tool (common random numbers).*

### What shipped

- **26 edges in one shared list** (9 Steel, 8 Spell, 9 general), yaml `edges:`, each 1–2
  sentences, SRD-5.2.1-safe (fighting styles, weapon masteries, the Grappler feat,
  Metamagic, a monster reaction, species-trait concepts, the rules glossary; the rest
  original). Three have a level minimum (*Steady Focus* and *Lasting Spell* 4th,
  *Piercing Spell* 6th).
- **Tags are flavour.** No `track` field; `track_depth` reads talents only; a test builds
  the Wizard with five Steel edges and gets Spell 3, Spell main, the Full table and the
  same ranks.
- **Nothing a talent or rank gives**, nothing that adds a die to a d20, rerolls or adds
  damage dice (V51; enforced at load, `data.EDGE_FORBIDDEN_TYPES`, and by a test that
  compares every edge effect with every talent and rank effect).
- **Engine**: five effect types (`damage_die_floor`, `miss_damage`, `ac_reaction`,
  `hit_dice_max`, `keep_concentration`), extended fields (`impose_disadvantage` with
  `trigger: weapon_hit` / `your_spell`, `advantage` on `death_save`, `temp_hp` with
  `trigger: first_bloodied`), one condition keyword (`two_handed`); `Picks.edges`;
  `check()` enforces the slots (one per even level reached, each once, minimum level,
  not a talent or knack); `combat.death_save(advantage=)`, `combat.stabilize()`; the sim's
  AI plays each simulated edge (documented in `sim.py`). Tests:
  `software/tests/test_facets_d20_edges.py` (63) plus edge tests in the data and chapter
  suites.
- **Every preset and sim build names an edge at each even level** (yaml; printed as each
  card's *Edges* line, tested).

### Iterations

Swap test against the preset median (n = 150–250), the pre-edges clash budgets:

| Step | Change | L4 range | L7 range | L10 range | Misses |
|---|---|---|---|---|---|
| 0 | pre-edges (fix pass, full run) | −10…+15 | −10…+10 | −11…+14 | 0 |
| 1 | first list; Parry with a shield; casters' early edges utility | −15.6…+5.9 | −10.2…+13.0 | −10.1…+13.5 | 1 (Loremaster L4) |
| 2 | V56 stabilizing; Parry spent under hidden AC, after *Shield* | −15.3…+8.4 | −9.7…+11.7 | −10.0…+10.9 | 1 (Loremaster L4) |
| 3 | V54: fragile casters take *Second Breath* at 2nd, *Steady Focus* at 4th | −13.0…+8.4 | −10.6…+8.0 | −9.8…+10.4 | 0, but item 7 fails: Tinker and spellblade +4–5 over the best pure Mind build at 4th |
| 4 | **V52: Parry needs no shield**; shield users take *Sap* | −8.7…+11.3 | −9.2…+12.3 | −10.3…+12.1 | 0; item 7 holds |
| final | full tool run (Table 9–1 re-fitted) | −11.9…+11.7 | −10.1…+9.4 | −11.3…+9.3 | **0** |

Edges on every build cost the party only a little HP: the median preset loses 0–5% less HP
per fight than without (step 1, same budgets), and Table 9–1 rose about 3% (below).

### Must-take check (V55)

Each simulated edge replaces a narrative filler on each reference-party member at 4th, 7th
and 10th; the two-handed ones also on the Barbarian (whose own edges were all set to
fillers). 500 days × 4 positions, final budgets. Points = how much less HP the party loses
per fight with the edge (swap score). Flag above ~5.

| Edge | Fighter L4/7/10 | Rogue | Wizard | Priest | Barbarian |
|---|---|---|---|---|---|
| *Sap* | +3.5/+3.4/+3.6 | +0.4/+4.0/+1.3 | 0 | +1.4/0/0 | +2.7/+1.1/+1.4 |
| *Parry* (no shield) | 0 (shield) | **+4.5**/0/0 (bow from 5th) | +2.1/−0.2/−1.1 | 0 (shield) | +2.4/+0.1/+0.7 |
| *Second Breath* | +2.3/+1.0/+1.9 | +0.3/+1.6/+2.5 | +2.1/+1.9/+2.3 | +2.8/+2.4/+0.6 | +2.7/+2.4/+1.5 |
| *Piercing Spell* (6th) | — /0/0 | — /0/0 | — /+3.0/+2.9 | — /−0.9/+1.0 | — |
| *Steady Focus* (4th) | 0 | 0 | 0/−0.3/+0.1 | +2.3/−0.4/+3.3 | — |
| *Graze* | 0 | 0 | 0 | 0 | +4.4/+0.2/+1.1 |
| *Heavy Hands* | 0 | 0 | 0 | 0 | +0.6/−0.5/+1.8 |
| *Die Hard* | −0.2/0/−0.2 | −0.8/−0.1/−1.8 | −1.0/−0.8/+0.7 | +1.7/−0.7/+1.0 | — |
| *Hale* | +0.4/+0.7/−1.1 | −1.1/−0.1/−2.1 | +1.1/−0.6/−0.9 | +1.3/+0.2/−0.9 | — |
| *Hardened* | 0 | 0 | 0 | 0 | 0 |

Noise on a single cell is about ±1.5 points (CRN, but builds diverge after the first
different roll). **No edge passes 5; none was cut.** One was **redesigned**: *Parry* with a
shield allowed, and spent by the sim only when +2 would turn the hit (perfect knowledge),
measured up to +6.8 on the Fighter and +8.5 on the Priest (n = 250). Under hidden AC it
fell to +4.7 on the Fighter at 4th but was still the first pick of every sword-and-board
build and, at 4th, lifted the Mind hybrids over their pure builds (item 7). It now needs
no shield (V52). The zeros are real: *Hardened* meets no poison from
the generic foes (the real-monster validation has some), *Die Hard* and *Hale* matter only
on days someone goes down or runs out of Hit Dice. The 16 narrative edges are zero by
construction (a test holds that they leave the combat profile unchanged).

### Final band table (swap test vs the preset median; PI secondary)

| Build | Kind | L1 | L4 | L7 | L10 | PI L1/4/7/10 |
|---|---|---|---|---|---|---|
| Fighter | preset | +4% | +4% | +4% | +0% | +46/−3/+27/+4 |
| Rogue | preset | −6% | −2% | +2% | +4% | +8/−11/+47/+22 |
| Barbarian | preset | +8% | +9% | +6% | +1% | +52/+28/+25/+0 |
| Monk | preset | +9% | +10% | +7% | +6% | +19/+5/+22/+9 |
| Wizard | preset | −7% | −4% | −1% | +3% | −16/+2/+25/+15 |
| Investigator | preset | +1% | −8% | −10% | −6% | −0/−26/−2/−0 |
| Loremaster | preset | −6% | −12% | −10% | −5% | −36/−33/−24/−24 |
| Tinker | preset | −1% | −1% | −8% | −8% | −8/−2/−22/−29 |
| Priest | preset | −1% | +7% | +1% | +0% | +0/+22/−6/+6 |
| Druid | preset | −10% | −5% | +4% | −0% | −29/−15/−6/−19 |
| Oracle | preset | +1% | +7% | −10% | −7% | −11/+9/−22/−16 |
| Oathsworn | preset | +6% | +1% | −3% | −10% | +41/+20/+2/−17 |
| *body_caster* | sim | +9% | −6% | −1% | −11% | +64/−27/−27/−23 |
| *soul_champion* | sim | +6% | −0% | −5% | −8% | +44/+5/−8/−7 |
| *body_ranger* | sim | −1% | +2% | −0% | +6% | −7/−1/+16/+32 |
| *body_battlemage* | sim | +4% | +7% | +1% | −7% | +27/+14/+1/−17 |
| *spellblade* | sim | −1% | −2% | −7% | −7% | −0/+4/−13/−11 |
| *armored_caster* | sim | −7% | −4% | −1% | +2% | −25/−4/+19/+10 |
| *battle_priest* | sim | −2% | +6% | +3% | −0% | +5/+19/+10/+6 |
| *battle_priest_deep* | sim | +6% | +0% | +2% | −0% | +41/−2/−1/+10 |
| *paladin_max* | sim | +6% | +4% | −5% | −9% | +51/+21/+1/−3 |
| *unbreakable* | sim | +9% | +8% | +9% | +9% | +58/+22/+26/+22 |
| *reckless_striker* | sim | +6% | +9% | +6% | +5% | +36/+26/+44/+31 |
| *healer_engine* | sim | −1% | +12% | +1% | −1% | +5/+5/−6/−1 |
| *soul_blaster* | sim | −7% | −0% | −4% | −4% | −12/+9/+11/−0 |
| *mind_controller* | sim | −9% | −8% | −1% | −4% | −39/−17/−11/−18 |
| *summoner* | sim | −3% | −8% | −5% | −9% | −6/−25/−31/−30 |
| *monk_stunner* | sim | +9% | +10% | +7% | +6% | +21/+2/+24/+12 |
| *double_cross* | sim | −7% | −3% | −7% | −3% | −23/+1/+5/−2 |

Range −10…+9 (L1), −12…+12 (L4), −10…+9 (L7), −11…+9 (L10): **0 misses of ±15%**.
Facet means (swap): Body +3…+5%, Mind −3…−7%, Soul −4…+3% (±10% wanted). Item 7:
every hybrid at or below its Facet's best pure build (+3 tolerance) at 4th, 7th and 10th;
no Steel-main hybrid's DPR₁ beats its Facet's best pure martial by more than 3.3% (Soul at
7th), no hybrid's DPR₃ beats its tradition's best caster by more than 0.1%. SRD baselines'
median −13…−20% against the preset median (was −10…−17%: the SRD classes get no edges).
Spearman PI vs swap 0.92 / 0.82 / 0.79 / 0.87.

### Encounter derivation (re-fitted with edges on every preset)

| | Before (fix pass) | After (edges + V56) |
|---|---|---|
| Threat model | minion √(8.4 × d), boss × 3.51, never × 1.16, hard × 1.06 | minion **√(8.6 × d)**, boss **× 3.43**, never **× 1.17**, hard **× 1.07** |
| Table 9–1, 4th | 18 / 29 / 34 / 40 | **19 / 30 / 35 / 42** |
| Table 9–1, 10th | 63 / 92 / 109 / 118 | **66 / 95 / 113 / 123** (every level within +5 of before) |
| Clash, 1st–10th | 2.96–3.51 rds, 27–29% HP, 96–100% wins | **2.96–3.62** rds, 26–29% HP, **96–100%** wins |
| Baseline (four 4th) | Clash 3.51 rds, 27%, 99.7% | Skirmish 2.20 rds 10% · **Clash 3.62 rds, 29%, 99.5%, 0.1% death** · Battle 4.72, 47%, 91% · Desperate 5.33, 65%, 69% |
| Standard day survived | 86–99% | **84–100%** |
| PC death on a standard day, 1st / 2nd / 3rd+ | 13.2% / 6.4% / 0.8–3.2% | **4.2% / 2.0% / 0–0.8%** |
| Hard day (four Clashes) | 38–77% | 47–83% |
| Party size (three / five / six) | −26 / +23 / +40% | −26 / **+24 / +41%** |
| Lone boss mark-up (measured) | ×1.16 | ×1.13 (the printed ×1.2 stands) |
| Table 9–2 examples | Bandit Captain boss 88, Ogre boss 104, Knight 40, Owlbear boss 151 | 86, 102, 41, 149 |

Table 9–1 in 09 and 10, Table 9–3, the constants, the worked examples and the day
paragraph in 09 were re-synced from the yaml; Table 9–2 regenerated.

### The two deferred misses

- **1st-level day death rate — fixed (V56).** Diagnosis (1,500 days, reference party,
  1st level): every death was three failed death saves, 152 of 213 in the day's third
  fight, with nobody able to heal. The simulator never stabilized anyone. Options
  measured: nobody (13.7% of days), the SRD's Help + DC 10 Medicine at the second failure
  (6.9%, wins 95.0%), **an action and no check at the second failure (4.4%, wins 95.4%,
  day survival 86.4% vs 87.1%)**, either as soon as a friend drops (0.1–1.0%, but Clash
  wins fall to 90–92%: the action is worth more in the fight). Adopted: stabilizing is an
  action and needs no check (08, 01 item 6, 10); the AI does it at two failures. Full run:
  **4.2%**, three Clashes' worth of the V35 per-fight target. Not an exception rule (it
  applies to everyone); *Field Medic* keeps its bonus-action stabilize.
- **Clash wins at 9th–10th — still open.** 96.1% / 96.7% after the refit, against the
  yaml's 97% floor (was 96.5%). Edges don't reach it: the losses are swingy boss-heavy
  Clashes at 9th–10th (the day's survival is 84–87% there too), which is Table 9–1's and
  the boss rules' business, not the characters'. Battle wins at 9th also dipped to 84.1%
  (floor 85%; 85.4% before), inside noise of the same cause. Left logged for the next
  balance pass; candidate fix: price bosses at 9th–10th a little higher (their measured
  factor is 4.3–5.0 standards there against the 3.43 median).

### Test counts

`tests/test_facets_d20_*.py tests/test_no_private_canon.py`: **756 passed** (was 683; the
new `test_facets_d20_edges.py` has 63). Full suite (`--ignore=tests/e2e`): **1847 passed**.
`python -m tools.build_d20_threat_table --check`: up to date.


## Book simplicity count (with edges)

*Edges designer, 2026-09-28. Recounted from the book as written (README, 01–08, 10), by
DESIGN §2's method: one pick = one decision, N picks from a list = N, a free-text line = 1,
accepting a printed value = 0.*

| Measure (target) | Before edges | **With edges (book as written)** | Where |
|---|---|---|---|
| Creation from a preset (≤ 12) | 7 | **7** (edges start at 2nd; the card's *Edges* line is read, not chosen) | 02 *The Quick Way* |
| Creation, custom (≤ 18) | 12 · 13 · 14 listed background; 16 · 17 · 18 written | **unchanged** | 02 Table 2–1 |
| Choices at a level-up (Amendment 5: odd 1, even 2 small) | 1 every level | **odd levels 1** (a talent, + a domain naming if it brings one); **even levels 2** (knack or ability pick, and an edge; *Cantrip Adept* names its cantrip as part of the pick). A preset: 0 (read the card) | 02 Table 2–5, 10 Table 10–3 |
| Choices over levels 2–10 | 9 + 0–2 domain namings | **14** (4 talents, 3 knacks, 2 ability picks, 5 edges) + 0–2 domain namings + 0–1 cantrip naming | 02 Table 2–5 |
| Exception rules a player applies (≤ 5) | 3 | **3** (E1–E3). The edge rules (each once; a few minimum levels; the tag is flavour and never counts toward depth) and V56 (stabilizing: an action, no check) apply to everyone alike; none is a carve-out | 01 item 13, 02 *Edges*, 08 |
| Mechanics per job (≤ 1 each) | 1 / 1 / 1 / 1 | **1 / 1 / 1 / 1**: no edge adds a die to a d20 (*Heavy Hands* raises low damage dice, not a d20 test), rerolls, or adds damage dice to a hit; edges that change a roll use advantage or disadvantage (*Die Hard*, *Hardened*, *Sure-Footed*, *Watchful*, *Grappler*, *Sap*, *Piercing Spell*) | 02 *Edges* |
| Gates ("you can't take X") | 0 | **0 build gates**; 3 level minimums on edges (Amendment 5 allows them). Spell edges do nothing until you cast, but nothing forbids them | 02 *Edges* |
| Entries a player reads | 26 talents + 13 knacks + 6 features | **+ 26 edges** (all in 02, each printed once, tested) | 02 |
| Chassis reading | Table 2–2, Table 2–3, three rank rules, lapse paragraph, checklist | **+ one "Edges don't count" paragraph** in *Steel and Spell*, and an *Edges* section: five rules, Table 2–7, 26 one-to-three-sentence entries (1,135 words) | 02 |
| Book length | 02: 5,425 words · 01: 874 · 10: 1,750 | 02: **6,882** · 01: **934** · 10: **1,861** | |

**Reading it.** Edges cost reading, not decisions at creation: a new player still makes 7
(preset) or 12–14 (custom) decisions before the first session. What grows is the list a
levelling player reads at even levels (26 short entries) and five more small picks over
ten levels, which is what Amendment 5 asked for: an even level now always holds something
for a fight or the road. The ≤ 5 exceptions and one-mechanic-per-job targets hold.
