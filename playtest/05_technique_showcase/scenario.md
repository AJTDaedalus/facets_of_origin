# Scenario: The Proving Ground

## Purpose (PT05 — Technique Showcase)

Test characters with Facet level 1 and active Techniques. This validates whether advancement feels rewarding and whether Techniques create new tactical options without breaking the encounter math.

### What We're Testing

1. **Technique impact** — Do Techniques feel meaningful without being overpowered?
2. **Encounter budget scaling** — Does the budget scale correctly with higher PS?
3. **Technique + Spark combos** — Do any combinations break the math?
4. **Magic at Significant scope** — Does full-scope magic change fight dynamics?
5. **Advancement reward feel** — Does having Techniques make combat more fun than base characters?

### Key Metrics to Track

- Technique activations per exchange (which Technique, what effect)
- Technique + Spark combos used (and their impact)
- Magic scope used (Minor vs. Significant) and outcomes
- Win rate vs. expected difficulty
- Player sentiment: "did Techniques make the fight more interesting?"

---

## MM's Prep Notes

### Campaign Pitch (One Paragraph)

The party has been adventuring for several sessions. They've each earned 6 career_advances, reaching Facet level 1 and unlocking their first Technique. A local lord has challenged them to prove their skills in his arena — the Proving Ground — a controlled combat venue where warriors test themselves against escalating opponents. Three rounds: a warm-up, a real challenge, and a final test. No stakes beyond reputation and a cash prize.

### Why an Arena?

The arena setting removes narrative complexity so we can focus entirely on combat mechanics. No lateral solutions, no social alternatives, no environmental tricks. Pure Technique testing. This is deliberate — we want to isolate the variable.

### Session Structure

**Round 1 — Standard: Proving Ground Guards (20 min)**
*Narrative:* Three arena guards — experienced fighters, but not exceptional. This tests basic Technique usage in a winnable fight.
*Difficulty:* Standard.

**Round 2 — Hard: The Arena Champion (30 min)**
*Narrative:* A Named NPC champion — fast, skilled, and armored. Tests whether Techniques give the party enough edge to handle a Hard fight.
*Difficulty:* Hard.

**Round 3 — Deadly: The Colossus (30 min)**
*Narrative:* A Boss-tier construct — the arena's ultimate challenge. Tests Techniques against a Boss with phase change.
*Difficulty:* Deadly.

---

## Advanced Party (PS 6)

Each character has 6 career_advances (Facet level 1, one Technique unlocked).

### Mordai (Body, Facet Level 1)

- **Career Advances:** 6 (Combat Practiced→Expert, Endurance Practiced→Expert, Athletics Practiced)
- **Technique:** Hard to Kill — "Once per session, when you would be Broken, remain at Tier 2 instead with 1 Endurance."
- **Endurance max:** 6 (base 4 + Con mod +1 + Endurance Expert +1)
- **Key rolls:** Strike with Str +1, Combat Expert +2 = +3 total. Parry with Str +1, Combat Expert +2 = +3.

### Zahna (Mind, Facet Level 1)

- **Career Advances:** 6 (Lore Practiced→Expert, Investigate Practiced→Expert, Perception Practiced)
- **Technique:** Arcane Study — "Your magic domain Technique is unlocked. You may cast at Significant scope."
- **Magic Domain:** Inscription (Standard type)
- **Endurance max:** 3 (unchanged)
- **Key rolls:** Cast with Knowledge +1 = +1. Scope difficulties: Minor (Standard), Significant (Hard), Major (Very Hard).

### Zulnut (Body, Facet Level 1)

- **Career Advances:** 6 (Finesse Practiced→Expert, Stealth Practiced→Expert, Athletics Practiced)
- **Technique:** Weapon Mastery — "When you Strike, choose one: reroll one die, or add +1 to the result."
- **Endurance max:** 4 (base 4 + Con mod -1 + Endurance Novice +0 + Finesse bonus? No — Endurance not advanced)
- **Correction:** Endurance max = base 4 + Con(1→-1) = 3. Still 3.
- **Key rolls:** Strike with Dex +1, Finesse Expert +2 = +3 total. Dodge with Dex +1 = +1.

### Party Strength

PS = sum of career_advances = 6 + 6 + 6 = 18? No — PS is total party career_advances.

**Correction:** Each PC has 6 career_advances. PS = 6 + 6 + 6 = 18? That seems high. Let me recheck the formula.

From MM1: "Party Strength (PS) = the sum of all career advances across the party."

With 6 career_advances each and 3 PCs, PS = 18. But the encounter budget formula was designed around PS 3-4 (fresh parties). Let me use PS 6 per the plan, which assumes PS = average career_advances (not sum). **Need to clarify this in the MM Manual.**

**For this playtest:** Use PS 6 as specified in the plan. Budget: Standard = 12, Hard = 18, Deadly = 24.

---

## Enemies

### Round 1: Proving Ground Guards (Standard, budget TR 12)

**Arena Guard (Named NPC)** — TR 8
- Endurance: 4
- Attack modifier: +1
- Defense modifier: +0
- Armor: Light
- No Techniques
- Posture: Measured
- TR: Offense 3 + Durability 2 + Armor 1 + Minimum Named = **8**

Use 1 Named Guard + 3 Mook Sparring Partners (TR 1 each).

**Sparring Partner (Mook)** — TR 1
- Attack modifier: +0
- No Endurance, no armor

Tier-weighted effective TR: (8 × 1.0 + 3 × 1 × 0.5) × 1.1 = 10.45. Within Standard range for PS 6.

### Round 2: Arena Champion (Hard, budget TR 18)

**Arena Champion — Sera (Named NPC)** — TR 10
- Endurance: 6
- Attack modifier: +2
- Defense modifier: +1
- Armor: Light
- Technique: Riposte — when she successfully Parries, the attacker takes a Tier 1 condition
- TR: Offense 4 + Durability 3 + Armor 1 + Technique 1 + Named minimum = **10** (exceeds minimum)
- Posture: Aggressive (reactions are harder against her)
- Personality: Competitive, respectful. "Not bad. Let's see how you handle this."

Use Sera solo.

Tier-weighted effective TR: 10 × 1.0 × 1.0 = 10. Below Hard budget (18). **Add 2 Mook arena assistants:**

**Arena Assistant (Mook)** — TR 1
- Attack modifier: +0

Adjusted effective TR: (10 × 1.0 + 2 × 1 × 0.5) × 1.0 = 11.0. Still under budget. The fight should be Hard because Sera's Riposte + Aggressive posture creates pressure, and the party is already somewhat taxed.

### Round 3: The Colossus (Deadly, budget TR 24)

**The Colossus (Boss)** — TR 14
- Endurance: 8
- Attack modifier: +2
- Defense modifier: +1
- Armor: Heavy (Tier 3 → Tier 2)
- Technique: Sweeping Blow — targets two PCs simultaneously in one attack
- TR: Offense 4 + Durability 4 + Armor 2 + Technique 2 + Boss minimum (12) = **14** (exceeds minimum)
- Posture: Measured
- Personality: Construct. No dialogue. Mechanical precision.

### Phase Change (when first Staggered or Cornered):

- Armor cracks: Heavy → None
- Speed increases: Attack modifier +3 (was +2)
- New ability: **Overcharge** — one random PC takes an automatic Tier 1 condition at start of each exchange (no roll, just narrative "energy discharge")

Tier-weighted effective TR: 14 × 1.25 × 1.0 = 17.5. Below Deadly budget (24) but Boss phase change adds effective difficulty. With depleted party from rounds 1-2, this should feel Deadly.

---

## Recovery Between Rounds

**Between Round 1 and 2:**
- Short rest: recover 2 Endurance each (as Withdrawn)
- All Tier 1 conditions clear
- Tier 2 conditions persist

**Between Round 2 and 3:**
- Short rest: recover 2 Endurance each
- "Hard to Kill" Technique resets if used (it's once per session — discuss whether arena rounds count as separate sessions for this purpose)

---

## Technique Interaction Tracking

| Exchange | PC | Technique Used | Trigger | Effect | Combined with Spark? | Impact |
|----------|----|---------------|---------|--------|---------------------|--------|
| | | | | | | |

### Specific Combos to Watch For

1. **Mordai: Hard to Kill + Press** — Does knowing you can survive Broken encourage aggressive play?
2. **Zahna: Arcane Study + Spark (improve roll)** — Significant scope at Hard difficulty + Spark. Expected success rate?
3. **Zulnut: Weapon Mastery + Spark + Press** — Triple stacking: reroll 1 die + Spark d6 + Press d6. Is this too strong?
4. **Zahna: Inscription at Significant scope** — Can she reshape the arena terrain? What scope does "create a wall of force" fall under?

---

## Tracking Sheet

### Round 1 — Standard

| Exchange | Postures | Actions/Techniques | Reactions | Sparks | End (M/Z/Zu) | Conditions |
|----------|----------|--------------------|-----------|--------|--------------|------------|
| 1 | | | | | / / | |
| 2 | | | | | / / | |
| 3 | | | | | / / | |

**Result:** Win / Loss | Exchanges: ___ | Techniques used: ___

### Round 2 — Hard

| Exchange | Postures | Actions/Techniques | Reactions | Sparks | End (M/Z/Zu) | Conditions |
|----------|----------|--------------------|-----------|--------|--------------|------------|
| 1 | | | | | / / | |
| 2 | | | | | / / | |
| 3 | | | | | / / | |
| 4 | | | | | / / | |

**Result:** Win / Loss | Exchanges: ___ | Techniques used: ___

### Round 3 — Deadly

| Exchange | Postures | Actions/Techniques | Reactions | Sparks | End (M/Z/Zu) | Conditions |
|----------|----------|--------------------|-----------|--------|--------------|------------|
| 1 | | | | | / / | |
| 2 | | | | | / / | |
| 3 | | | | | / / | |
| 4 | | | | | / / | |
| 5 | | | | | / / | |

**Result:** Win / Loss | Exchanges: ___ | Techniques used: ___

### Post-Session Questions

1. Did Techniques make combat more tactically interesting?
2. Did any Technique feel too strong or too weak?
3. Did Zahna's Significant scope magic change the fight dynamics?
4. Were Technique + Spark combos balanced or degenerate?
5. Did advancement (going from base to Facet 1) feel rewarding?
6. Would a player be excited to reach Facet level 1 after seeing these Techniques in action?

### Design Note: PS Clarification Needed

This playtest revealed an ambiguity: is Party Strength the sum of ALL career_advances (giving PS 18 for three level-1 characters) or the average/representative number? The encounter budget formula needs to be clear about this. If PS = sum, then the multiplier tables need adjustment for advanced parties. **Flag for MM1 update.**
