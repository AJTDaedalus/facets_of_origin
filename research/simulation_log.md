# Combat Simulation Log

This file records all playtest simulations run during design. Entries are added chronologically. Each entry documents the encounter, party state, results, and design conclusions.

**⚠ SUPERSEDED (v0.2 semantics) — every PC-side figure below (win rate, Broken
rate, exchange count, lethality) is invalidated.** All of it was measured with
the `is_zero_end_absorb` house rule active — a rule that only ever existed in
`combat_sim.py`, never in `facet.yaml` or the PHB (DESIGN F5) — and under the
pre-D1/D2 enemy-Endurance and PC-armor rules WS-A is about to replace. DESIGN
§4.3: *"PC lethality drops relative to every recorded simulation... Gate G2
must re-baseline them."* The chicken baselines and the Encounter Budget
difficulty multipliers derived from these numbers fall with them (WS-A task
A10 / gate G4 re-derives both from scratch). Kept, not deleted — this is the
record of how the 0-Endurance rule and the armor divergence were found (Brain
ruling, BRIEF §Q3). **Not superseded:** enemy-side Threat Rating arithmetic
(the TR labels used throughout to describe test fixtures) survives the WS-A
migration by construction — `resolve := old durability_value` — not by luck.

---

## Series 1 — Three Chickens (2026-03-05)

**SUPERSEDED (v0.2 semantics)** — pre-simulator hand run, 0-End house rule not yet even formalized; see top-of-file notice, DESIGN §4.3.

**Encounter:** Party (PS 3) vs. 3 Chickens (Mooks, TR 1 each = TR 3 total)
**Nominal difficulty:** Skirmish (budget = PS 3 × 1 = 3)
**With ×1.0 multiplier (2–3 enemies):** effective TR 3
**Simulations run:** 4 (parallel agents)

### Results

| Run | Winner | Exchanges | Broken | Sparks Spent | Notes |
|-----|--------|-----------|--------|--------------|-------|
| 1 | Party | 3 | 0 | 0 | Clean sweep, no Tier 2s landed |
| 2 | Party | 3 | 0 | 0 | Zahna took Cornered once; recovered cleanly |
| 3 | Party | 3 | 0 | 0 | Party untouched, Zulnut spent 1 End |
| 4 | Party | 3 | 0 | 0 | Chicken rolled 12 vs Zahna; dodged on 10+ |

**Win rate: 4/4 (100%)**

### Conclusions

- Behaves as intended Skirmish — party wins cleanly with resources mostly intact.
- Cornered/Staggered spiral (second Tier 2 → Broken) was the only genuine threat vector, and the chickens die too fast to compound it.
- Confirms ×1.0 multiplier is appropriate for 2–3 enemies.

---

## Series 2 — Five Chickens (2026-03-05)

**SUPERSEDED (v0.2 semantics)** — see top-of-file notice, DESIGN §4.3.

**Encounter:** Party (PS 3) vs. 5 Chickens (TR 5 total)
**Nominal difficulty:** Standard (budget = PS 3 × 2 = 6), with ×1.25 multiplier: effective TR 6.25
**Simulations run:** 4 (parallel agents)

### Results

| Run | Winner | Exchanges | Broken | Sparks Spent | Notes |
|-----|--------|-----------|--------|--------------|-------|
| 1 | Party | 3 | 0 | 0 | Zahna took Cornered; party killed 3 in Ex1, fight ended Ex3 |
| 2 | Party | 3 | 0 | 0 | Zahna Cornered Ex1; Zulnut took Off-Balance + Winded; cleared |
| 3 | Party | 4 | 0 | 0 | Zulnut took Staggered Ex1; stayed Staggered through Ex3; Zahna took Winded |
| 4 | Party | 3 | 1 (Zahna) | 0 | Zahna Broken in worst-case run |

**Win rate: 4/4 (100%)**

### Conclusions

- The encounter plays closer to a Skirmish than a Standard despite meeting the TR budget.
- Key reason: Mook action economy advantage collapses when 3+ die in Exchange 1. The ×1.25 multiplier assumes sustained pressure, but Mook swarms are self-cancelling — each dead Mook reduces future attack volume immediately.
- Cornered spiral confirmed as the primary threat vector: the one Broken (Zahna, run 4) resulted from Absorbed Tier 2 Cornered → forced second Tier 2 Absorb. Still validates the design intention.
- **Provisional finding:** For Mook-only swarms, ×1.25 multiplier may slightly overstate difficulty. Recommend ×1.1 as a working hypothesis for Mook swarms (4–6 enemies). Named NPC and mixed-composition encounters are unaffected.

---

## Series 3 — Seven Chickens (2026-03-05)

**SUPERSEDED (v0.2 semantics)** — see top-of-file notice, DESIGN §4.3.

**Encounter:** Party (PS 3) vs. 7 Chickens (TR 7 total)
**Nominal difficulty:** Above Standard, approaching Hard (budget: Standard=6, Hard=9)
**With ×1.5 multiplier (7+ enemies):** effective TR 10.5 — nominally Hard-to-Deadly territory
**Simulations run:** 4 (parallel agents)

### Results

| Run | Winner | Exchanges | Broken | Sparks Spent | Notes |
|-----|--------|-----------|--------|--------------|-------|
| 1 | Party | 4 | 0 | 0 | Zulnut took Staggered from Chicken G (Absorb); held; Mordai hit 0 End in Ex4 but survived |
| 2 | Party | 3 | 0 | 0 | Zahna took Cornered from Absorb in Ex1; survived because Mordai cleared flock fast |
| 3 | Party | 6 | 2 (Zahna, Zulnut) | 3 (Mordai) | Mordai soloed final 3 chickens after both allies Broken; spent all 3 Sparks |
| 4 | Chickens | 5 | 3 (all) | 0 | Chickens won via Tier 2 stacking; double-6 in Ex1 on Zulnut, double-6 follow-up in Ex2 |

**Party win rate: 3/4 (75%)**

### Key findings

**Run 3 (bad luck):** Zulnut Cornered Exchange 1 on failed dodge vs 12 roll. Zahna Staggered by Absorb. By Exchange 2 Zulnut Broken, by Exchange 3 Zahna Broken. Mordai soloed Chickens C–G across 4 exchanges using all 3 Sparks, finishing on 0 Endurance, Cornered. Party technically won. Six exchanges total — the longest fight in all simulations.

**Run 4 (chicken luck):** Chicken C rolled double-6 against Zulnut (Ex1); Zulnut's dodge failed on [1,2]. Exchange 2: Chicken D rolled 11 vs Cornered Zulnut, dodge came up [1,2] again — Zulnut Broken. Zahna Broken same exchange (Cornered → Absorb second Tier 2). Mordai fought solo 1v4, eliminated D, E, F before Chicken G landed a Tier 2 at 1 Endurance with Aggressive posture — reaction cost was 2 End, impossible to react. Mordai Broken. **The entire party Broken to a single surviving chicken.**

**Tactical error identified (Run 4):** Mordai going Aggressive at 1 Endurance made all reactions cost 2 End minimum. Had he switched to Measured (reaction cost 1 End), he could have attempted a Parry on Chicken G's final attack. That single posture decision was the difference between survival and defeat.

### Conclusions

- **7 chickens (TR 7, effective TR 10.5 at ×1.5) produces approximately 75% party win rate** — aligns with Standard difficulty target.
- The ×1.5 multiplier for 7+ Mooks appears reasonably calibrated, though the sample size is small.
- Two-person Broken result (runs 3 and 4) validates that 7 chickens is genuinely dangerous — significantly more pressure than 5 chickens.
- **Cornered spiral is the decisive threat vector in all loss/near-loss scenarios.** Once a party member is Cornered (Tier 2), all subsequent Strikes against them are Easy — the spiral self-reinforces if the party cannot eliminate fast enough.
- **Mordai at 0 Endurance** is a critical danger state. At 0 End with any posture costing ≥1 reaction End, the character is effectively reaction-locked. Aggressive + 0 End = catastrophic vulnerability.
- **Sparks matter at 7 chickens.** Mordai used all 3 Sparks in Run 3 to ensure Mook kills while Cornered at 0 End. No Sparks were used in runs 1 and 2 (fast resolution), but Run 3 would likely have been a party wipe without Spark expenditure.
- **The chicken did not need naming.** It strutted.

---

## Calibration Summary (all series, as of 2026-03-05)

**SUPERSEDED (v0.2 semantics)** — derived entirely from Series 1–3 above; see top-of-file notice, DESIGN §4.3.

| Encounter | TR | Effective TR | Exchanges (avg) | Win Rate | Nominal Difficulty |
|-----------|-----|-------------|-----------------|----------|--------------------|
| 3 Chickens | 3 | 3.0 | 3 | 100% | Skirmish (budget 3) |
| 5 Chickens | 5 | 6.25 | 3–4 | 100% | Standard (budget 6) |
| 7 Chickens | 7 | 10.5 | 3–6 | 75% | Hard (budget 9) |

### Observations

1. **The Mook action economy multiplier (×1.25 for 4–6) may overstate difficulty for pure Mook swarms.** Five chickens produced 100% win rate despite sitting at the effective TR budget for Standard. Possible correction: Mook-only swarms in the 4–6 range use ×1.1 rather than ×1.25.

2. **The ×1.5 multiplier for 7+ enemies appears well-calibrated for Mooks.** Seven chickens produced exactly the 75% win rate expected of Standard difficulty. However, if the ×1.25 correction above is applied, 7 chickens might be re-categorized as Hard — more simulation needed.

3. **Win rate of zero Broken vs. two/three Broken is extremely high variance.** The difference between a clean win (3 exchanges, 0 Endurance spent) and a grueling survival (6 exchanges, all 3 Sparks, two allies Broken) is almost entirely determined by whether the Cornered spiral triggers in Exchange 1. This is a design feature, not a bug — it creates dramatic variance from a small number of dice rolls — but MMs should understand that "75% win rate" conceals a bimodal distribution: easy wins or brutal attrition.

4. **All simulations unvalidated for parties larger than 3 or with different composition.** These results are specific to Mordai/Zahna/Zulnut (PS 3, career_advances 1 each). Results will shift with higher PS, different Facets, or armor.

---

*All multipliers remain working estimates pending further simulation. Adjust based on playtest results.*

---

## Series 4 — Seven Chickens ×20 (2026-03-06, partial)

**SUPERSEDED (v0.2 semantics)** — see top-of-file notice, DESIGN §4.3.

**Encounter:** Party (PS 3) vs. 7 Chickens (TR 7 total, effective TR 10.5 at ×1.5)
**Purpose:** Increase sample size from 4 to 20 to validate Series 3 win rate (~75%)
**Simulations completed:** 10 of 20 (C1–C8, C11, C12; C9/C10 lost to rate limits)

### Results

| Run | Winner | Exchanges | Broken | Sparks Spent | Notes |
|-----|--------|-----------|--------|--------------|-------|
| C1 | Party | 4 | 0 | 1 (Mordai) | Mordai at 0 End Ex4; spent Spark to guarantee kill |
| C2 | Party | 4 | 0 | 0 | Zulnut hit 0 End; Zahna recovered via Withdrawn |
| C3 | Party | 3 | 0 | 0 | Zahna Cornered Ex1; party killed fast enough to prevent cascade |
| C4 | Party | 3 | 0 | 0 | Clean sweep; chickens rolled mostly 5–6 |
| C5 | Party | 4 | 0 | 0 | Zulnut drained to 0 End Ex2 via Absorb; held |
| C6 | Party | 4 | 0 | 0 | Mordai spent 2 End on Parries; Zulnut recovered via Withdrawn Ex3 |
| C7 | Party | 3 | 0 | 0 | Fast sweep; Zulnut absorbed one Staggered, no cascade |
| C8 | Party | 4 | 0 | 0 | Zulnut absorbed Tier 2 Staggered Ex1; maintained 3 End throughout |
| C9 | — | — | — | — | Lost to rate limit |
| C10 | — | — | — | — | Lost to rate limit |
| C11 | Party | 4 | 0 | 0 | Mordai hit 0 End Ex3; Zulnut 0 End Ex4; no Tier 2 cascade |
| C12 | Party | 5 | 0 | 0 | Slower; Mordai burned End early; chickens had many consequence rolls |

**Party win rate (10 completed): 10/10 (100%)**

### Key findings

All 10 completed runs are party wins. This is a striking divergence from the Series 3 result (3/4, 75%). Possible explanations:

1. **Series 3 sample variance:** 4 runs is a small sample. The two losses in Series 3 (runs 3 and 4) both involved exceptional chicken rolls (double-6, back-to-back). With 10 additional runs, no such cascades occurred.

2. **Confirmed pattern — bimodal distribution:** All 10 wins were clean (3–5 exchanges, 0–1 Sparks). There are no "grueling survival" runs in this batch. This suggests the bimodal distribution is real but the "brutal" tail may be rarer than 25%.

3. **The Cornered spiral is the decisive variable.** In every win, the party killed chickens fast enough that any Cornered/Staggered condition on a party member resolved before a second Tier 2 could land. The loss condition requires both a high chicken attack roll AND a failed reaction in the same exchange — a 2-event chain.

4. **Mordai at 0 Endurance appeared in multiple runs without causing a loss.** As long as Mordai switches to Measured or Defensive posture at low End, reaction cost stays manageable. The tactical error (Series 3 Run 4) was Aggressive posture at 0 End.

### Revised win rate estimate

With 13 total runs (Series 3 + 4 completed): **12 wins / 1 loss = ~92% win rate.** This is higher than the initial 75% estimate. With the full 20 runs, expect something in the 80–95% range — which would reclassify 7 chickens from Standard-difficulty to a **Hard Skirmish** (harder than Skirmish, but not quite Standard).

---

## Series 5 — Veteran Soldier ×8 (2026-03-06, partial)

**SUPERSEDED (v0.2 semantics)** — the 0-End house rule this series explicitly documents ("House rule in effect") is the rule DESIGN §4.3/A6 retires; see top-of-file notice.

**Encounter:** Party (PS 3) vs. Veteran Soldier (Named NPC, TR 10, solo)
**Purpose:** Establish baseline win rate for solo Named NPC vs. same party; compare to Mook swarm
**Simulations completed:** 6 of 20 (V1–V4 from previous session, V6–V7; V5/V8 lost to rate limits)
**House rule in effect:** At 0 Endurance, Absorbed conditions become persistent Tier 2; second triggers Broken.

### Results

| Run | Winner | Exchanges | Broken | Sparks | House Rule | Notes |
|-----|--------|-----------|--------|--------|------------|-------|
| V1 | Party | 5 | Veteran | 1 (Zulnut) | N | Two Tier 2s stacked on Veteran at 1 End |
| V2 | Party | 10 | Zulnut (Ex4), Veteran (Ex10) | Mordai 1, Zahna 1 | Y (twice) | Longest fight; house rule broke Veteran at 0 End |
| V3 | Party | 7 | Veteran (Ex7) | Zulnut 2 | N | Two Tier 2 conditions stacked on Veteran at 5 End |
| V4 | Party | 7 | Veteran (Ex7) | Zulnut 2 | N | Two Tier 2s stacked; Veteran broke at 5 End |
| V5 | — | — | — | — | — | Lost to rate limit |
| V6 | Party | 5 | Veteran (Ex5) | 0 | Y | House rule: two Absorbs at 0 End → Broken |
| V7 | Party | 5 | Veteran (Ex5) | 0 | Y | House rule: two Absorbs at 0 End Ex5 → Broken |
| V8 | — | — | — | — | — | Lost to rate limit |

**Party win rate (6 completed): 6/6 (100%)**

### Key findings

**The party wins every run, but the fights are dramatically longer and more costly than chicken fights.**

- Average exchanges: ~6.5 (range 5–10) vs. ~3.7 for chickens
- Sparks spent: 0–4 per fight (vs. 0–1 for chickens)
- Party members Broken: 1 in 6 runs (Zulnut in V2, the 10-exchange grind)
- House rule triggered: 3 of 6 runs (V2, V6, V7)

**Two distinct victory paths emerged:**
1. **Dual Tier 2 stack (V1, V3, V4):** Party lands two Tier 2 hits on the Veteran in one exchange (or with one carried over). Since light armor converts Tier 2 → Tier 1, this requires the Veteran to have already accumulated one Tier 2 that armor didn't prevent — only possible if he's Staggered from a previous carry-over, or if the party Absorb-locks him. In practice, this happened when the Veteran's Parry failed at low Endurance.
2. **House rule attrition (V2, V6, V7):** Party grinds Veteran to 0 Endurance via forced Parries, then lands two more hits that he must Absorb (becoming persistent Tier 2s). This path takes longer but is more reliable.

**The house rule is doing significant work.** Without it, the Veteran's light armor would make him nearly unbreakable through attrition. With it, he's beatable in 5–10 exchanges. This strongly supports codifying the house rule as written law.

**TR 10 solo vs. TR 7 swarm — qualitative difference:**
- Chickens: fast, swingy, resolved in 3–5 exchanges. Loss risk comes from early Cornered spiral.
- Veteran: slow grind, 5–10 exchanges, consistently dangerous but not swingy. Loss risk comes from Endurance attrition on party side.
- Both feel appropriately different in texture. The Veteran fight is more of a "boss fight" even at the same effective TR.

---

## Calibration Summary (all series, as of 2026-03-06)

**SUPERSEDED (v0.2 semantics)** — derived from Series 1–5 above; see top-of-file notice, DESIGN §4.3.

| Encounter | TR | Effective TR | Exchanges (avg) | Win Rate | Assessed Difficulty |
|-----------|-----|-------------|-----------------|----------|---------------------|
| 3 Chickens | 3 | 3.0 | 3 | 100% (4/4) | Skirmish |
| 5 Chickens | 5 | 6.25 | 3–4 | 100% (4/4) | Light Standard |
| 7 Chickens | 7 | 10.5 | 3–5 | ~92% (12/13) | Hard Skirmish / Light Standard |
| Veteran Soldier | 10 | 7.5 (solo ×0.75) | 5–10 | 100% (6/6) | Standard (resource-draining) |

### Revised observations

1. **7 chickens is probably not Standard difficulty.** With 13 runs at ~92% win rate, it's sitting closer to Skirmish. The ×1.5 Mook multiplier may be too aggressive. Possible correction: Mook-only swarms of 7+ use ×1.25 rather than ×1.5, bringing effective TR to 8.75 — closer to a genuine Standard budget (6) at PS 3.

2. **The Veteran Soldier (TR 10, solo) is a Standard encounter for this party.** 100% win rate but at significant cost (fights lasting 5–10 exchanges, Sparks sometimes spent, occasional Broken). This matches the "~75% win" target for Standard if we define "win" as "party not wiped" — but since the party hasn't lost yet, we may need harder encounters to validate the Hard/Deadly multipliers.

3. **Solo multiplier (×0.75) appears appropriate.** The Veteran's effective TR of 7.5 feels like a Standard encounter, which matches the ~75% win rate target for Standard difficulty. His action economy disadvantage (one attack per exchange vs. three from the party) is real.

4. **The house rule (0 End Absorb → persistent Tier 2) is load-bearing.** It triggered in 3/6 Veteran fights. Without it, those fights would have been indefinite grinds with no resolution condition. Recommend codifying immediately.

5. **Bimodal distribution confirmed for Mook swarms; not confirmed for Named NPCs.** Veteran fights are more consistently costly — fewer "clean wins," but also no catastrophic collapses. Named NPC fights appear to have a tighter distribution around a moderate-difficulty outcome.

---

*Simulation series ongoing. 10 seven-chicken runs and 14 Veteran Soldier runs remain. Results above are interim.*

---

## Series 6 — Automated Combat Simulator (2026-03-15)

**SUPERSEDED (v0.2 semantics)** — see top-of-file notice, DESIGN §4.3. Note also: the methodology line below labels the 0-End rule "per PHB" — DESIGN F5 found it was never actually in `facet.yaml` or the PHB text, only in `combat_sim.py`; that mislabel is itself part of why this corpus needs a clean re-baseline.

**Tool:** `software/tools/combat_sim.py` — automated combat simulator using the game engine's dice mechanics
**Party (default):** Mordai (Body, Str+1, Combat+1, End 5), Zahna (Mind, Str-1, Dex+1, End 3), Zulnut (Body, Str+0, Dex+1, End 3). PS 3.
**Iterations:** 200 per configuration, seed 42
**Methodology:** Each exchange: all PCs declare posture (AI-driven: high End→Aggressive, mid→Measured, low→Defensive, 0 End→Withdrawn), PCs Strike enemies, enemies attack PCs (PC reacts). Named/Boss enemies Parry PC strikes spending Endurance. 0-Endurance Absorb = persistent Tier 2 (per PHB). Mooks: any successful strike removes. Named/Boss: same T2 condition twice → Broken. Boss phase change on first Broken.
**AI notes:** PCs always Strike (non-combat PCs use raw Strength — underestimates Support/Maneuver contributions). Enemy posture: Measured (Defensive at 0 End). Target selection: PCs focus Mooks first then wounded Named; enemies target lowest-End PC.
**Armor bug fixed:** Initial runs had heavy armor computed as T-2 (negating T2 entirely). Corrected to PHB rules: light T2→T1, heavy T3→T2 only. All results below use corrected armor.

### Series A — Mook Scaling (PS 3, standard party)

| Config | Enemies | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|---------|----------|--------|-------------|--------|--------|
| A1 | 3 Chickens (TR 3) | 100% | 98–100% | 1.6 | 0.2 | 0.00 |
| A2 | 5 Chickens (TR 5) | 100% | 98–100% | 2.5 | 1.0 | 0.04 |
| A3 | 7 Chickens (TR 7) | 100% | 98–100% | 3.9 | 1.4 | 0.57 |
| A4 | 10 Chickens (TR 10) | 66% | 59–72% | 6.3 | 3.7 | 2.23 |
| A5 | 15 Chickens (TR 15) | 98% | 95–99% | 14.5 | 5.0 | 2.00 |

**Key findings:**
- **A1–A3 (3–7 Mooks):** All 100% win rate. Mook swarms up to 7 are Skirmish difficulty at PS 3. Matches hand-simulated data direction but is more optimistic (hand sims showed ~92% at 7 — difference likely due to AI behavior and larger sample).
- **A4 (10 Mooks):** 66% win rate — a genuine Hard encounter. Non-combat PCs (Zahna, Zulnut) break consistently due to weak Strike and low Endurance.
- **A5 (15 Mooks) anomaly:** 98% win rate despite 15 enemies. Withdrawn posture cycling is the cause: PCs recover 2 End per exchange while dodging for free in Withdrawn. Mordai solos remaining Mooks over 14.5 exchanges. This reveals that Mook swarms have diminishing returns — the self-cancelling effect identified in Series 3 is real at scale.
- **Non-combat PC limitation:** Zahna (Str -1, no Combat) and Zulnut (Str +0, no Combat) contribute weak Strikes. In actual play they'd use Support/Maneuver to boost Mordai — simulator underestimates their contribution. Results are a lower bound.

### Series B — Named NPC Scaling (PS 3)

| Config | Enemies | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|---------|----------|--------|-------------|--------|--------|
| B1 | 1 Named (TR 8) solo | 99% | 96–100% | 5.2 | 6.6 | 0.12 |
| B2 | 1 Named (TR 10) solo | 95% | 91–97% | 7.6 | 8.2 | 0.35 |
| B3 | 1 Named (TR 12) solo | 78% | 72–84% | 10.6 | 8.7 | 0.83 |
| B4 | 1 Named TR 8 + 3 Mooks | 98% | 94–99% | 7.0 | 7.2 | 0.36 |
| B5 | 2 Named (TR 8) each | 21% | 16–27% | 11.0 | 6.0 | 2.37 |

**Key findings:**
- **Solo Named NPCs scale linearly:** TR 8 → 99%, TR 10 → 95%, TR 12 → 78%. Each 2 TR roughly costs 10-15% win rate.
- **Mixed encounters are slightly easier than their TR suggests:** B4 (Named + 3 Mooks, raw TR 11) has 98% win rate — the Mooks die quickly and the Named alone is manageable.
- **B5 (2 Named) is devastating:** 21% win rate. Two Named NPCs with action economy × 2 and sustained pressure is Deadly. This is the strongest evidence that Named NPC count matters more than total TR for difficulty.
- **Sparks heavily spent against Named:** 6.6–8.7 mean Sparks spent (out of 9 total). Named fights are resource-intensive.

### Series C — Boss Encounters (PS 3)

| Config | Enemies | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|---------|----------|--------|-------------|--------|--------|
| C1 | 1 Boss (TR 12) solo | 55% | 48–61% | 14.6 | 8.8 | 1.32 |
| C2 | 1 Boss (TR 16) solo | 65% | 58–71% | 12.8 | 8.8 | 1.15 |
| C3 | 1 Boss TR 12 + 2 Mooks | 46% | 39–52% | 15.8 | 8.6 | 1.48 |
| C4 | 1 Boss TR 16 + 4 Mooks | 50% | 44–57% | 14.1 | 8.2 | 1.43 |

**Key findings:**
- **Boss fights are Hard (40–65% win rate):** All Boss configurations land in the Hard difficulty range.
- **C2 (TR 16) higher win rate than C1 (TR 12) — counterintuitive:** The TR 16 Boss has heavy armor but higher attack modifier. With the corrected armor rules (heavy only blocks T3→T2), heavy armor does NOT prevent T2 conditions, so the Boss still accumulates Staggered/Cornered. The phase change with 4 Endurance is beatable. The higher attack modifier hurts PCs more but the phase 2 Boss is fragile.
- **Adding Mooks to Boss fights barely changes difficulty:** C3 vs C1 (46% vs 55%), C4 vs C2 (50% vs 65%). Mooks die quickly; the Boss is the real fight.
- **All Boss fights are resource-draining:** 8.2–8.8 Sparks spent (nearly all available), 1.1–1.5 PCs Broken.

### Series D — Party Size Scaling (vs Named TR 8 + 5 Mooks)

| Config | PCs | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|-----|----------|--------|-------------|--------|--------|
| D1 | 2 PCs | 12% | 9–18% | 12.0 | 3.8 | 1.74 |
| D2 | 3 PCs | 86% | 81–90% | 9.2 | 6.9 | 0.98 |
| D3 | 4 PCs | 100% | 98–100% | 5.2 | 5.0 | 0.29 |
| D4 | 5 PCs | 100% | 98–100% | 3.9 | 3.5 | 0.21 |

**Key findings:**
- **Party size is the dominant factor:** Same encounter goes from 12% (2 PCs) to 100% (4+ PCs). Each additional PC dramatically reduces difficulty.
- **3 PCs is the sweet spot for Standard difficulty** against this encounter (Named + 5 Mooks).
- **2 PCs cannot handle action economy:** Too many incoming attacks per PC per exchange. Endurance drains immediately.

### Series E — Advanced Party (PS 6, Techniques active)

| Config | Enemies | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|---------|----------|--------|-------------|--------|--------|
| E1 | Named (TR 8) | 100% | 98–100% | 4.6 | 4.7 | 0.23 |
| E2 | Boss (TR 12) | 88% | 82–91% | 12.6 | 8.7 | 0.58 |
| E3 | Boss (TR 16) | 86% | 80–90% | 11.1 | 8.6 | 0.60 |

**Key findings:**
- **Advanced party trivializes Named NPCs:** E1 at 100% win rate, 4.6 exchanges (vs 5.2 for standard party). Mordai with Combat Expert (+2) is significantly more effective.
- **Boss fights become Standard difficulty for advanced party:** 86–88% win rate. The encounter budget needs to scale up for higher PS.
- **Advancement feels meaningful:** Standard party at 55% vs Boss TR 12 → Advanced party at 88%. Clear power progression.

### Series F — Sequential Encounters (no full recovery)

| Config | Sequence | Win Rate | 95% CI | Exch (mean) | Sparks | Broken |
|--------|----------|----------|--------|-------------|--------|--------|
| F1 | Skirmish → Standard | 98% | 95–99% | 2.2 | 6.7 | 0.18 |
| F2 | Skirmish → Standard → Hard | 55% | 48–62% | 6.2 | 8.6 | 1.55 |
| F3 | Standard → Hard | 64% | 57–70% | 5.1 | 8.6 | 1.35 |

**Key findings:**
- **Skirmish → Standard is safe:** 98% survival. The Skirmish barely taxes resources (2 End recovery between fights helps).
- **Three-encounter sessions are genuine challenges:** F2 at 55% — adding a Hard fight after two earlier encounters creates meaningful tension. This is the "three encounter session" template working as designed.
- **Resource carry-over matters:** F3 (Standard → Hard) at 64% shows that entering a Hard fight with depleted resources is dangerous.

---

### Master Calibration Table (2026-03-15, automated, N=200 each)

**SUPERSEDED (v0.2 semantics)** — derived from Series 6; see top-of-file notice, DESIGN §4.3.

| Difficulty | Target Win Rate | Encounter Compositions (PS 3) |
|------------|----------------|-------------------------------|
| **Skirmish** (90–100%) | Warm-up | 3–7 Mooks; 1 Named (TR 8) solo |
| **Standard** (70–85%) | Real fight | 1 Named (TR 12) solo; 1 Named (TR 8) + 5 Mooks |
| **Hard** (40–60%) | Coin flip | 1 Boss (TR 12–16); 10 Mooks; 2 Named (TR 8) is actually Deadly |
| **Deadly** (15–30%) | Designed to lose | 2 Named (TR 8); encounters well above budget |

### Key Design Conclusions

**SUPERSEDED (v0.2 semantics)** — these conclusions are built on the win-rate/Broken-rate figures above; treat as historical direction, not current numbers, until G1/G2/G4 re-derive them. See top-of-file notice, DESIGN §4.3.

1. **Named NPC count is more important than total TR.** Two Named NPCs (combined TR 16) is Deadly (21% win rate), while a single Boss at TR 16 is Hard (65%). Named NPCs maintain pressure; Mooks self-cancel.

2. **Mook swarms have strongly diminishing returns.** 7 Mooks (100%) vs 10 Mooks (66%) vs 15 Mooks (98% via Withdrawn cycling). Mook difficulty peaks around 8–10 Mooks and then stabilizes or even decreases due to the self-cancelling effect.

3. **Boss fights feel right at Hard difficulty.** Phase changes create interesting mid-fight pivots. Boss fights are long (12–16 exchanges) but not grindy — the condition spiral creates rising tension.

4. **Party size is the strongest lever.** Each additional PC adds ~20-30% win rate. Encounter budgets must scale linearly with party size to maintain intended difficulty.

5. **The Spark economy works under pressure.** Sparks are spent heavily against Named/Boss enemies (8+ of 9 per fight), confirming they are a genuine resource. Hoarding in playtests was a behavioral issue, not a mechanical one.

6. **Sequential encounters create good tension arcs.** Skirmish → Standard is safe; Skirmish → Standard → Hard creates genuine late-session danger.

7. **Non-combat PCs are underrepresented.** The simulator models everyone as Strikers. In play, Support/Maneuver PCs (Zahna, Zulnut) amplify combat PCs, likely increasing real win rates by 5-10%.

---

## Series 7 — Gates G1 and G2 (D1/D2 post-migration) (2026-07-10)

Task A8. `tools/combat_sim.py` migrated to the Resolve model (D1: `apply_resolve_damage`, `mook_removed`, `target_strike_difficulty`, rider Conditions via `is_rider=True`) and the per-scene armor budget (D2, already landed in A5). All runs below are against that migrated simulator — **not** superseded-corpus semantics.

### Gate G1 — Archive Guardian vs 3 starting PCs — **FAILED, ESCALATED (see re-run below)**

**Configuration:** `standard_party()` (Mordai/Zahna/Zulnut) vs 1 Archive Guardian (`archive_guardian_def()`: Resolve 5, heavy armor → effective Resolve 7), riders modelled live (Tier 2 rider → Easy on subsequent Strikes against the Guardian). n=200, seed=1, via `run_simulation`.

| Boss Resolve (base / effective w/ heavy) | Win Rate | Median Exchanges | Mean Exchanges |
|---|---|---|---|
| 5 / 7 (DESIGN §4.1 starting value) | 100% | 2.0 | 2.0 |
| 6 / 8 (top of BRIEF's 2–6 band) | 100% | 2.0 | 2.3 |
| 8 / 10 (diagnostic, outside sanctioned band) | 100% | 3.0 | 2.8 |
| 10 / 12 (diagnostic) | 100% | 3.0 | 3.4 |
| 15 / 17 (diagnostic) | 100% | 4.0 | 4.6 |
| 20 / 22 (diagnostic) | 95.5% | 6.0 | 6.4 |

**Pass condition:** median ≥ 3 exchanges, PC win rate 45–55%, zero house rules, rider→Easy snowball not driving median below the floor.

**Result: median-exchange floor eventually clears (at Resolve far outside the sanctioned band), but win rate never approaches the 45–55% target — it barely drops below 100% even at Resolve 20, four times the DESIGN starting value and outside the BRIEF's 2–6 Boss Resolve band the task authorized retuning within.**

**Root-cause diagnosis (not a Resolve-tuning problem):** a verbose single-seed run at the starting value (Resolve 5/+2 armor) shows the rider→Easy snowball firing exactly as DESIGN's EF1 concern predicted — Mordai's 10+ Strike applies a Staggered rider, which makes Zahna's subsequent Strike Easy, whose Cornered rider makes Zulnut's Easy in turn, defeating the Guardian in exchange 1. Retuning Resolve upward (diagnostic sweep to 20, four times the sanctioned band's top) delays *when* the Guardian dies but does not meaningfully change *whether* the party wins, because:
- The Guardian has exactly one attack per exchange, against one PC (`choose_enemy_target` picks the lowest-Endurance PC — confirmed via a diagnostic random-target patch that this targeting policy is not the cause; random targeting produced the same ceiling).
- A PC's incoming Tier 2 hit is frequently avoided outright (a full-success Dodge/Parry) or only partially lands, and a single PC needs *two* same-type Tier 2 hits to Broken (D5 ledger row 2 / F6) — a cadence a solo, single-target attacker essentially never sustains against three independently-acting, independently-recovering PCs before its own Resolve (however large) is ground down by three PCs' combined offense every exchange.
- This is an **offense/action-economy problem, not a durability problem.** Retuning the one sanctioned knob (Boss Resolve, `archive_guardian_def()`'s `resolve` / `enemies/archive_guardian.fof`'s `resolve:`) only ever controls how long the Guardian survives, not how much threat it poses per exchange — and G1 needs both dials to reach 45–55%.

**Two retunes attempted per the task's escalation trigger** (5→6, both within the sanctioned 2–6 band; a further diagnostic sweep to 8/10/15/20 confirms the ceiling holds well outside it too) — **escalated to Planner/Brain rather than redesigned**; see `docs/LOG_v0.3_ruleset_revision.md`'s `## ESCALATION` block. A8 is otherwise complete; G1 is the sole blocking item.

### Gate G1 — RE-RUN under revised pass condition — **PASSED**

Planner resolved the escalation (DESIGN §5-bis, 2026-07-10): the 45–55% win-rate band is void-derived (traced to the Encounter Budget's "Hard ≈ 50%" multiplier, itself voided by Brain's Q3) and is dropped. G1 is reframed as a length-plus-cost gate: median ≥ 3 exchanges, every enemy defeatable, zero house rules, the rider→Easy snowball does not drive median below 3, and a cost signal (Sparks spent, Endurance remaining, PC-Broken incidence) evidences "survivable but expensive" per the Guardian's own authored notes.

**Retune:** Guardian base Resolve **5 → 8** (effective 10 with heavy armor) — the smallest value whose pool clears the median-3 floor under the worst-case rider policy already in the diagnostic sweep above. `enemies/archive_guardian.fof` and `tools/combat_sim.py`'s `archive_guardian_def()` both updated; published TR recomputed **14 → 17** (offense 5 + resolve 8 + armor 2 + techniques 2).

**Canonical run** (`standard_party()` vs `archive_guardian_def()`, riders modelled live, n=200, seed=1, via `run_simulation`):

| Metric | Result |
|---|---|
| Win rate | 100% (200/200), 95% CI 98.1–100% |
| Median exchanges | **3.0** |
| Mean exchanges | 2.8 |
| Mean Sparks spent | 6.2 of 9 |
| Mean PCs Broken | 0.03 |
| Endurance remaining at fight end | Mordai 2.2 (1–3), Zahna 1.3 (0–2), Zulnut 2.0 (2–2) |

**Pass condition met:** median ≥ 3 ✓; every enemy defeatable (100% win rate across 200 runs) ✓; zero house rules ✓; cost signal recorded — 6.2/9 Sparks and meaningful Endurance drawn down (Zahna as low as 0) is the "expensive" half of "survivable but very expensive" (the Guardian's own `.fof` notes), matching canon rather than the voided 45–55% descriptor.

**Snowball-floor robustness check:** the median-3 result is not a seed artifact. Re-run at n=200 across 7 seeds (1, 2, 3, 4, 5, 7, 42): median exchanges landed at exactly 3.0 in all 7 runs (mean exchanges 2.8–2.9, win rate 100% in all 7). A parallel sweep one step lower (Resolve 7, effective 9) is markedly less stable — median flips between 2.0 and 3.0 depending on seed at the same n=200 (seeds 1/4/5 → median 2.0; seeds 2/3/7/42 → median 3.0) — confirming 8 as the smallest value that robustly clears the floor rather than merely hitting it on the sanctioned seed.

**Widened range:** the BRIEF's "working range 2–6" for enemy Resolve (`docs/BRIEF_v0.3_ruleset_revision.md`, D1 decision) is widened to **2–8**, with a note that Boss-tier durability sits at the top of the band while Named-tier (Resolve 3–4, confirmed stable in Series 7 G2 and the migrated `.fof` files) remains well inside it. See BRIEF for the updated note.

**A8 CLOSED.** G1 (revised) and G2 both pass, logged with seeds, n, and full parameters. Full suite green (847 passed, 1 pre-existing unrelated failure in `test_config.py`'s port default, tracked separately).

### Gate G2 — Armor breakability vs Veteran Soldier — **PASSED**

**Configuration:** 1 PC (Mordai's stat block, armor varied) vs 1 Veteran Soldier (`veteran_soldier_def()`: Resolve 4, light armor). Two independent lines of evidence, per Brain's EF6 ruling that a probabilistic win-rate assertion cannot prove breakability on its own:

**1. Deterministic worst-case proof** (`test_combat.py::TestArmorBreakability`, landed in A5, re-confirmed unchanged by this task): fixed policy — PC always Absorbs, enemy always lands the same Tier 2 type every exchange. Exact exchange Broken lands on:

| Armor | T_broken |
|---|---|
| None | 2 |
| Light | 4 |
| Heavy | 6 |

`heavy (6) > light (4) > none (2)` ✓. `light (4) ≤ 2 × none (2)` ✓ (exactly at the boundary). Broken reachable in all three by construction.

**2. Realistic AI-driven simulation** (`run_combat`, n=200, seed=1, active Dodge/Parry/Absorb policy, real Endurance spend):

| Armor | Win Rate | Broken Count (of 200) | Median T_broken (when it happens) |
|---|---|---|---|
| None | 88.0% | 24 | 4 |
| Light | 97.5% | 5 | 5 |
| Heavy | 100.0% | 0 | — (see below) |

Heavy-armor Broken was not observed at n=200/seed=1 but is confirmed reachable at larger n (3/2000, seed=7) — expected: heavy armor plus active reactions plus the Veteran Soldier's own limited Resolve (dying to the PC's return offense) make it rare, not impossible, matching the deterministic proof's guarantee.

**F6 (C4) and F5 (A6) varied independently, per DESIGN §11's over-correction concern:**
- **F6 alone** (old "any second Tier 2" vs new "same-type only" escalation), tested against the deterministic worst-case policy: **identical** T_broken (2/4/6) when the attacker repeats the same Condition type every hit — the sanctioned worst-case assumption. When the attacker instead *alternates* Tier 2 types (Staggered, then Cornered), old-F6 breaks the target exactly 1 exchange sooner than new-F6, uniformly across all three armor tiers, with `heavy > light > none` and `light ≤ 2×none` holding under both. F6 only ever adds a small delay; it cannot be the source of an over-correction into unkillable.
- **F5 alone** (old 0-Endurance-Absorb escalation, reintroduced via a diagnostic monkeypatch of `_enemy_attack` — not shipped), tested against the realistic Veteran Soldier sim at n=200/seed=1: **zero measurable difference** in Broken count for any armor tier (26/26 none, 5/5 light, 0/0 heavy, with-vs-without). F5's earlier significant effect (seen in the G0 fixed-seed 3-PC-vs-Boss scenarios) is specific to longer, multi-PC grinds where a PC actually reaches and stays at 0 Endurance; it does not materialize in this single-PC-vs-one-Named matchup.

**Conclusion:** F6 and F5 do not combine to over-correct PCs into unkillable within G2's scenario. Gate G2 passes on both lines of evidence.

---

## Series 8 — Gate G3: Aggressive posture knob K1 (BRIEF D8, DESIGN §5) (2026-07-10)

**Question:** does K1 — the Aggressive posture's +1 reaction surcharge applying to the first reaction of the exchange only, instead of every reaction — soften the "Aggressive death spiral" (a low-Endurance PC facing several simultaneous attacks burns Endurance on the surcharge alone and has nothing left to react with) without erasing Aggressive's offense tradeoff over Measured?

**Methodology, in full (DESIGN only specified "Unarmored Endurance-3 PC, Aggressive vs Measured, baseline vs K1, n ≥ 200" — enemy composition, fight length, and the win-rate definition were Worker judgment calls, documented here for scrutiny):**

- **PC:** Zahna's canonical stat block (`zahna_def()`) — Endurance 3, unarmored — already matches "Endurance-3 unarmored PC" exactly. Posture fixed for the whole scenario (bypasses `choose_pc_posture`'s Endurance-ratio logic, which G3 needs to hold constant to isolate the posture variable).
- **Enemies:** two identical weak Named enemies (`_g3_named_def()`: Resolve 2, attack/defense modifier 0, unarmored) — not tied to any TR formula, since this experiment measures posture economics, not encounter balance. Two are required, not one: with a single attacker there is only ever one reaction per exchange, and "first reaction" is the *only* reaction, making K1 indistinguishable from baseline by construction. Both must be Tier 2 capable (Named, not Mook): `incoming_tier` is fixed at 1 for Mooks, and Tier 1 alone never escalates to Broken (D5 ledger row 2) — a pure Mook swarm literally cannot produce a measurable PC Broken rate under the current rules, however many Mooks attack at once.
- **PC's own Strike:** Press/Spark-free (`_g3_pc_strike`). `should_press`'s policy spends 1 Endurance *before* reactions are even resolved for the exchange — with Zahna's Endurance-3 pool exactly large enough that one pre-spent point changes whether K1's discount ever crosses an affordability threshold, this confounds the posture experiment. Press/Spark spending is an orthogonal resource decision the gate isn't testing.
- **Fight-to-conclusion was tried first and rejected.** Running this same 1-PC-vs-2-weak-Named matchup to a real conclusion (win = both enemies defeated, loss = PC Broken, no window) produced **no measurable difference between Aggressive and Measured at all**: both landed at ~84% Broken (n=1000, seed=1). A reaction ROLL's success chance never depends on posture, only the Endurance to attempt one does — and over a multi-exchange war of attrition, cumulative Tier 2 exposure converges every posture toward the same Broken ceiling regardless of how fast any one posture burns Endurance early on. The "Aggressive death-spiral" PT01 and BRIEF D8 describe is specifically an **opening-exchange alpha-strike** phenomenon (burn Endurance reacting to the first attack of a multi-attacker exchange, then have nothing left for the second) — a signal only visible in a short, bounded window, not a long-run average.
- **Final design: bounded to exactly 2 exchanges** (`G3_EXCHANGES = 2`), not fight-to-conclusion. `party_wins` = "cleared both enemies within the window" (the offense-edge proxy for the win-rate-delta pass condition — this metric is not affected by K1 at all, since K1 only touches reaction cost, never the Strike offense modifier; it is a sanity check that Aggressive's genuine advantage survives, not a risk K1 was expected to threaten). `pcs_broken`/Broken rate is the safety signal K1 is meant to improve.
- All rule computations (dice, condition tiers, Resolve, reaction cost) still route through `app.game.combat` — only the orchestration (fixed posture, bounded window, Press/Spark removed) is new, sim-only glue, per C1.

**Results — n=3000, seed=1:**

| Configuration | Win rate (cleared both) | Broken rate |
|---|---|---|
| Aggressive, baseline | 1.7% (95% CI 1.3%–2.2%) | 89.0% |
| Measured, baseline/K1 (identical — K1 only affects Aggressive) | 0.5% (95% CI 0.3%–0.8%) | 52.0% |
| Aggressive, K1 | 1.6% (95% CI 1.2%–2.1%) | 75.0% |

- **Broken-rate cut (Aggressive, baseline → K1):** (0.890 − 0.750) / 0.890 = **15.7%** (pass bar: ≥ 15%).
- **Win-rate delta (Aggressive − Measured):** baseline +1.7pp, K1 +1.1pp → **preserved within 0.6pp** (pass bar: ±5pp).

**Robustness check across 7 seeds (1, 2, 3, 4, 5, 7, 42), n=3000 each** — the baseline result landed close enough to the 15% bar (15.7%) to warrant checking it wasn't a seed artifact, matching this project's established practice (cf. Series 7's Resolve-8 robustness check):

| Seed | Broken cut | Delta preserved |
|---|---|---|
| 1 | 15.7% | yes (0.6pp) |
| 2 | 17.8% | yes (0.4pp) |
| 3 | 18.0% | yes (0.1pp) |
| 4 | 17.6% | yes (0.1pp) |
| 5 | 18.7% | yes (0.5pp) |
| 7 | 16.7% | yes (0.1pp) |
| 42 | 18.0% | yes (0.3pp) |

Every seed clears both bars, with margin (broken cut never drops below 15.7%, delta never exceeds 0.6pp) — the seed=1 result was not a lucky outlier.

**Verdict: ADOPT K1.** Both pass conditions hold robustly. This was surfaced to the user before adoption given (a) the methodological latitude required to construct any measurable scenario at all (DESIGN specified only the PC and the postures being compared) and (b) adoption being a permanent core-combat rule change; the user confirmed adopting on this evidence. K1 is now the canonical rule: `facet.yaml`'s `combat.postures.aggressive.reaction_cost_modifier_applies: first_reaction_only`, `app.game.combat.reaction_cost`'s `is_first_reaction` parameter, `Character.reactions_this_exchange` / `PCState.reactions_this_exchange` (reset each exchange, incremented per incoming attack reacted to), and PHB III.3 + MM5 text all updated in the same pass. `combat_sim.py`'s shared `_enemy_attack` (used by every other Series) now applies K1 live, not just the G3 harness — `run_g3_gate`'s `k1_enabled=False` branch is retained only to reproduce the **pre-adoption baseline** for this historical record, via `combat_module.reaction_cost(..., is_first_reaction=True)` unconditionally rather than a second copy of the rule.

**Reproduce:** `python -m tools.combat_sim --series G3 -n 3000 --seed <seed>`, or `combat_sim.run_g3_gate(iterations=3000, seed=<seed>)` / `combat_sim.g3_verdict(results)` directly.

---

## Series 9 — Gate G4: Encounter Budget recalibration (task A10) (2026-07-10) — **FINDING, ESCALATED**

**Question:** do the chicken baselines (3/5/7 Mooks) plus a solo Sergeant and a solo Guardian, re-run against the fully-migrated D1/D2/K1 engine, still land at Skirmish ~95% / Standard ~75% / Hard ~50% / Deadly ~25% (±10pp)? If not, retune `Encounter.difficulty_multiplier` and/or `action_economy_multiplier`.

**Configuration throughout:** `standard_party()` (Mordai/Zahna/Zulnut, Party Strength 3) vs the named enemy roster, `run_simulation`, n=200 per seed, seeds 1/2/3 unless noted (win-rate list is seed 1→2→3; CI quoted is seed 1's Wilson 95% interval).

### Part A — the five baselines named in the task

| Configuration | Win rate (seeds 1/2/3) | Median exchanges | Mean PCs Broken |
|---|---|---|---|
| 3 chickens | 100% / 100% / 100% | 2.0 | 0.00 |
| 5 chickens | 100% / 100% / 100% | 2.5 | 0.00 |
| 7 chickens | 100% / 100% / 100% | 4.0 | 0.00 |
| Sergeant (TR 8) solo | 100% / 100% / 100% | 1.0 | 0.00 |
| Archive Guardian (TR 17) solo | 100% / 100% / 100% | 3.0 | 0.07 |

All five sit at the ceiling. None reproduces its assigned band (chickens: Skirmish ~95% — fine; Sergeant/Guardian: Standard ~75% / Hard-or-Deadly ~50–25% — both wildly missed).

### Part B — is this a solo-enemy artifact? (it is not)

Swept enemy **count** and **per-enemy TR** independently against the same PS-3 party:

| Configuration | Win rate (seeds 1/2/3) | Weighted eff. TR (current formula) | Eff.TR ÷ PS |
|---|---|---|---|
| Mook swarm, 10/15/20/25/30 (single seed sweep) | 100% at every size through 30 | 5.0–15.0 | 1.7–5.0 |
| Mook swarm, 40 / 50 | 55.5% / 0% | 20.0 / 25.0 | 6.7 / 8.3 |
| Named(8) solo | 100% | 8.0 | 2.67 |
| Named(10) solo | 100% | 10.0 | 3.33 |
| Named(12) solo | 100% | 12.0 | 4.0 |
| Boss(12) solo | 100% | 15.0 | 5.0 |
| Boss(17) solo [Guardian] | 100% | 21.25 | 7.08 |
| Named(8) + 5 mooks | 100% | 11.55 | 3.85 |
| Guardian + 15 mooks | 84.0% / 77.0% / 79.0% | 30.0 | 10.0 |
| 2× Named(8) | 100% / 100% / 99.0% | 16.0 | 5.33 |
| 2× Named(10) | 97.5% / 97.5% / 99.5% | 20.0 | 6.67 |
| 2× Boss(17) | 83.5% / 81.0% / 83.0% | 42.5 | 14.17 |
| **3× Named(8)** | **81.0% / 81.0% / 75.0%** | 24.0 | **8.0** |
| **3× Named(10)** | **41.5% / 43.5% / 36.5%** | 30.0 | **10.0** |
| **3× Named(8) + 1 mook** | **48.5% / 57.5% / 57.5%** | 25.5 | **8.5** |
| **3× Named(8) + 2 mooks** | **19.0% / 21.0% / 22.0%** | 27.0 | **9.0** |
| **4× Named(8)** | **19.5% / 25.5% / 16.5%** | 35.2 | **11.7** |
| 5× Named(8) | 3.5% / 3.0% / 1.0% | 44.0 | 14.7 |
| 4× Named(10) | 5.0% / 1.5% / 0.5% | 44.0 | 14.7 |
| 3× Boss(17) | 5.5% (all 3 seeds) | 63.75 | 21.25 |

**Mean PCs Broken confirms mook swarms never threaten the party at all:** even at 30 Mooks, mean Broken = 0.00 across 200 runs — the 40/50-Mook drop in win rate is the `MAX_EXCHANGES = 20` safety-cap timeout counted as a loss, not a real defeat (party is never in danger, the fight is just too long to finish inside the cap). Mook count is not a usable Standard/Hard/Deadly lever under the current rules — only a Skirmish one.

**The dominant variable is simultaneous Named/Boss-tier actor count, not weighted TR.** A solo enemy is ~100% regardless of TR (Guardian at TR 17, eff. TR÷PS = 7.08, is as trivial as a TR 8 Sergeant at eff. TR÷PS = 2.67). Two Named/Boss enemies of moderate TR are still ~100%; only two *Bosses* specifically (eff. TR÷PS 14.17) crack 90%. Three Named enemies is where a real fight starts — and even there, per-enemy TR matters enormously: 3× TR8 (eff. TR÷PS 8.0) gives 81%, while 3× TR10 (eff. TR÷PS 10.0, only 25% more weighted TR) gives 40% — a 40-point win-rate swing for a 2-TR-per-enemy difference. Adding a single TR-1 Mook to 3× TR8 Sergeants (eff. TR÷PS 8.0 → 8.5, a 6% TR increase) drops the win rate from ~81% to ~50%. Four Named enemies of any tested TR is already Deadly-or-worse (≤25%), and five is a near-certain loss (≤3.5%).

**This is not resolvable by retuning `difficulty_multiplier`/`action_economy_multiplier`/`TIER_WEIGHTS` as scalar constants.** Those three constants define a *linear, separable* model — `effective_tr = Σ(TR_i × tier_weight) × group_size_modifier(count)`, compared against `party_strength × difficulty_multiplier`. The measured relationship is neither linear nor separable: the true win-rate curve is a **steep, count-gated threshold** (flat at ~100% for 1–2 Named/Boss actors of *any* TR, a cliff through 3–5 actors, modulated second-order by per-enemy TR only once past that gate) rather than a smooth function of a single weighted-TR scalar. No choice of the three constants reproduces both "1 Guardian (TR 17) is trivial" and "3 Sergeants (TR 8 each, lower total weighted TR than 1 Guardian) is a genuine fight" simultaneously, because the current formula's weighted-TR sum for 1 Guardian (21.25) already exceeds 3 Sergeants' (24.0 — close, but the *win rates are 100% vs 81%, not comparable at all*) and is far below 4 Sergeants' (35.2, win rate 20%) despite the Guardian alone being unconditionally trivial and 4 Sergeants being Deadly. The independent variable that actually predicts difficulty (Named/Boss actor count) isn't a term the current formula's group-size modifier represents strongly enough to dominate the way the data shows it must.

### Part C — validated recipes that DO land in the target bands (PS 3 party) — **SUPERSEDED by Part D**

> **Model correction (task A14, 2026-07-11):** the win rates in this table were measured against a model in which enemies could Parry. A14 (§5-quater F5) established that enemies never react — depletion is outcome-only — and removed the enemy Parry. That correction moved every recipe below ~one difficulty band easier, taking all of Standard/Hard/Deadly out of their intended windows. The rosters here are **retained as a historical record of the pre-A14 model**; the calibrated recipes now in force are in **Part D**. Do not build the MM1 Recipe Table from this table.

| Difficulty | Target | Composition found | Win rate (seeds 1/2/3) |
|---|---|---|---|
| Skirmish (~95%) | 85–100% | 3–7 Mooks | 100% (all) |
| Standard (~75%) | 65–85% | 3× Named (TR 8) | 81% / 81% / 75% |
| Hard (~50%) | 40–60% | 3× Named (TR 8) + 1 Mook | 48.5% / 57.5% / 57.5% |
| Deadly (~25%) | 15–35% | 4× Named (TR 8), or 3× Named (TR 8) + 2 Mooks | 19.5–25.5% / 19–22% |

These four rosters are real, reproducible (3 seeds each), and satisfy the task's stated bands. **They do not, however, fit any smooth retuning of the existing linear budget formula** — see Part B. Using them as the MM1 Recipe Table's worked examples (which is already how MM1 instructs MMs to use the table — "pick your column, pick the difficulty row, use the suggested composition," not derive from raw TR-budget arithmetic) satisfies the task's Accept criterion for *measured win rates inside the bands*. Whether the raw `TR × multiplier` budget formula should be (a) left as a rough, explicitly-non-predictive sanity check for 3+ Named/Boss rosters, (b) restricted to Mook-only/solo-enemy composition, or (c) rebuilt around actor-count as the primary term, is a design-doctrine call beyond re-running simulations — escalated to Planner, see `docs/LOG_v0.3_ruleset_revision.md`.

**Reproduce:** the definitions and `run_simulation` calls above use `combat_sim.standard_party()`, `chicken_def()`, `city_watch_sergeant_def()`, `veteran_soldier_def()`, `archive_guardian_def()`, `generic_named_def(tr)`, `generic_boss_def(tr)` at n=200, seeds 1/2/3.

---

## Series 9 Part D — Recipe recalibration under the corrected (no-enemy-Parry) model (task A15) (2026-07-11)

A14 (§5-quater F5) removed the enemy Parry — enemies never react; depletion is outcome-only. Re-running the Part-C rosters under the corrected model confirmed the predicted ~one-band shift (Standard `3× Named` 81→94.5%, Hard `3× Named + 1 Mook` 48.5→76%, Deadly `4× Named` 19.5→58.5% / `3× Named + 2 Mooks` 19→47.5% at seed 1). Every recipe was now too easy. A15 re-ran the actor-count ladder to re-derive rosters that land back in band.

**The actor-count ladder under the corrected model** (`standard_party()` PS-3, n=200, seeds 1/2/3):

| Roster | Win rate (seeds 1/2/3) | avg |
|---|---|---|
| 3× Named (TR 8) | 94.5% / 97.0% / 96.0% | 95.8% |
| 3× Named + 1 Mook | 76.0% / 74.5% / 80.0% | 76.8% |
| 3× Named + 2 Mooks | 47.5% / 48.0% / 47.0% | 47.5% |
| 3× Named + 3 Mooks | 20.0% / 20.0% / 22.5% | 20.8% |
| 4× Named (TR 8) | 58.5% / 54.5% / 52.0% | 55.0% |
| 4× Named + 1 Mook | 20.0% / 16.5% / 21.0% | 19.2% |
| 5× Named (TR 8) | 8.0% / 12.0% / 9.5% | 9.8% |

**The finding is unchanged and, if anything, cleaner: difficulty is an actor-count ladder, and per-enemy TR is a second-order knob.** Under the corrected model the ladder resolves to a fixed **3-Named core with one Mook added per difficulty step** — the throwaway Mook is now the whole dial from Standard through Deadly:

### Recalibrated recipes that land in the target bands (PS 3 party)

| Difficulty | Target | Composition | Win rate (seeds 1/2/3) |
|---|---|---|---|
| Skirmish (~95%) | 85–100% | 3–7 Mooks | 100% (all) |
| Standard (~75%) | 65–85% | 3× Named (TR 8) + 1 Mook | 76.0% / 74.5% / 80.0% |
| Hard (~50%) | 40–60% | 3× Named (TR 8) + 2 Mooks | 47.5% / 48.0% / 47.0% |
| Deadly (~20%) | 15–35% | 3× Named (TR 8) + 3 Mooks, or 4× Named (TR 8) + 1 Mook | 20.0% / 20.0% / 22.5% · 20.0% / 16.5% / 21.0% |

The `4× Named + 1 Mook` Deadly alternative is the "upgrade a Mook to a Named" reading of the same roster (swap a throwaway for a real threat, then trim one Mook) and measures identically at seed 1 (20.0%). `4× Named` alone lands in the Hard band (55%), not Deadly, under the corrected model — worth noting because it was the Part-C Deadly headline; a fifth Named overshoots Deadly into near-certain loss (9.8%). The Skirmish Mook-swarm is model-agnostic (enemies that fall to one Strike never had a reaction to remove) and is unchanged.

These recipes are pinned in `software/tests/test_combat_sim.py::TestRecipeCalibration` at their seed-1 values and asserted to fall inside their bands; the pre-A14 `xfail(strict)` markers were removed as each recipe re-entered band. The MM1 Recipe Table (`mm_manual/MM1_Encounters_and_Enemies.md`) is built from this Part D.

**Reproduce:** same helpers as Part C; `run_simulation(standard_party(), [(generic_named_def(8), 3), (chicken_def(), k)], iterations=200, seed=s)` for `k` in 1/2/3 and `s` in 1/2/3.
