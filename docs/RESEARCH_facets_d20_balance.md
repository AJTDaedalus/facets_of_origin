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
