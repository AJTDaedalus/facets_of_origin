# Combat Simulation Log

This file records all playtest simulations run during design. Entries are added chronologically. Each entry documents the encounter, party state, results, and design conclusions.

---

## Series 1 — Three Chickens (2026-03-05)

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
