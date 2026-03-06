# Simulation Prompt: Veteran Soldier (TR 10) vs Party

Use this prompt to run a single combat simulation of the Veteran Soldier solo encounter.

---

You are simulating a full combat encounter in the Facets of Origin TTRPG. Play both sides trying to win. Walk through every exchange step by step with specific varied dice results, and resolve the fight to completion.

## THE SYSTEM

**Exchange structure:** All participants simultaneously declare Posture, then take actions/reactions. Resolve all rolls, apply conditions, end-of-exchange cleanup, repeat until one side is out.

**Postures:**
- Aggressive: +1 to offensive rolls, +1 Endurance cost per reaction
- Measured: no modifier, standard costs
- Defensive: −1 to offensive rolls, −1 Endurance cost per reaction (min 0)
- Withdrawn: no offensive action, all reactions free, recover 2 Endurance at end of exchange

**Strike roll:** 2d6 + modifiers vs difficulty
- 10+: Tier 2 Condition (Staggered or Cornered, attacker chooses)
- 7–9: Tier 1 Condition (Winded, Off-Balance, or Shaken, attacker chooses)
- 6−: Consequence for attacker

**Difficulty:** Easy +2 to roll, Standard +0, Hard −2, Very Hard −4

**Press:** Spend 1 Endurance before rolling to add 1d6, drop lowest.

**Reactions** (1 per incoming action):
- Dodge: costs 1 End, roll 2d6+Dex. 10+=miss, 7-9=downgrade condition one tier, 6−=full condition
- Parry: costs 1 End, roll 2d6+Str+Combat rank. Same outcomes.
- Absorb: costs 0, take full condition.
- Intercept: costs 2 End, protect ally, then Dodge or Parry.

**Conditions:**
- Tier 1 (Winded/Off-Balance/Shaken): clear end of exchange. Winded=−1 next roll. Off-Balance=next reaction costs +1 End. Shaken=MM directs next action.
- Tier 2 (Staggered/Cornered): persist until treated. Staggered=−1 offensive rolls. Cornered=cannot go Aggressive, AND incoming Strikes against you are Easy difficulty.
- Broken: out of fight. Triggered by receiving a Tier 2 when you already have one.

**Armor:** Light=incoming Tier 2 becomes Tier 1 instead. Heavy=incoming Tier 3 becomes Tier 2.
**Mooks:** One Strike (any tier, 7+) removes. No Endurance. No reactions.
**Endurance floor:** 0 = Absorb only.
**Sparks:** 3 each. Spend before rolling: add 1d6, drop lowest. Each character has 3 Sparks total for the fight.

## THE PARTY

**Mordai** — End 5, Strike/Parry 2d6+2, Dodge 2d6+0, Sparks 3, no armor. Weapon Mastery (blades): Strike difficulty is Easy (+2 to roll).

**Zahna** — End 3, magical Strike 2d6+0 at Hard difficulty (−2 to roll), Dodge 2d6+1, Sparks 3, no armor. Fragile — prefers Withdrawn when threatened.

**Zulnut** — End 3, Strike 2d6+2, Dodge 2d6+1, Sparks 3, no armor.

## THE ENEMY

**Veteran Soldier** — Named NPC, TR 10
- Endurance: 7/7
- Attack: 2d6+3 (Strength +2, Combat Expert +1), Standard difficulty against party
- Parry: 2d6+3 (same modifier)
- Armor: Light (incoming Tier 2 conditions become Tier 1 instead)
- No Techniques
- TR: 10

**Veteran Soldier tactics:**
- Default posture: Measured
- Goes Aggressive if a party member is Cornered or Staggered (presses the advantage)
- Goes Defensive if he is Staggered (protects his attack output by cutting reaction cost)
- Reaction preference: Parry (2d6+3) over Dodge — his Parry is strong. Will Parry the highest incoming threat each exchange; Absorbs lower ones if Endurance is tight.
- Targeting: Focuses on the highest-Endurance party member first (Mordai). Shifts focus to a Cornered or Staggered party member to compound conditions. Does NOT spread attacks — he picks one target per exchange and commits.
- Light armor: any Tier 2 condition the party lands on him is downgraded to Tier 1 (which then clears end of exchange). To Break him, the party must land Tier 2 conditions in TWO DIFFERENT EXCHANGES (he must already have a Tier 2 carried over, which his armor normally prevents — so actually the party must first get a Tier 2 to stick, then land another while that one persists... wait: armor turns incoming Tier 2 → Tier 1, so Tier 2 conditions NEVER land on him. The party must find another path to Breaking him).

**ARMOR CLARIFICATION:** Light armor means every incoming Tier 2 result is reduced to Tier 1. Tier 1 conditions clear end of exchange. This means the Veteran Soldier effectively CANNOT be put into a Tier 2 condition by standard Strikes alone. To Break him, the party needs either: (a) a Spark-boosted attack that somehow forces a Tier 2 through armor — which light armor still reduces to Tier 1, OR (b) accumulation of Tier 1 conditions within one exchange to degrade his Endurance through reaction costs. The Veteran Soldier can only be Broken if he takes a Tier 2 condition that persists — which requires his armor to be bypassed somehow. Given the current rules, light armor means the party grinds him down via Endurance attrition: force him to spend Endurance on reactions until he's at the floor, then he can only Absorb and conditions start stacking.

**CORRECTION — RE-READ THE RULES:** Broken is triggered by receiving a second Tier 2 condition while already having one. Light armor turns Tier 2 → Tier 1 on incoming hits. So the Veteran Soldier can never receive a Tier 2 from incoming Strikes (armor reduces them all). He can ONLY be Broken if he already has a Tier 2 condition from some other source (there is none in this encounter). Effectively, **the Veteran Soldier cannot be Broken through standard combat** — the party must grind his Endurance to 0 and then rely on Absorbs of Tier 1 conditions... but Tier 1 clears end of exchange and being at 0 End just means Absorb-only, not Broken.

**REVISED BREAKING CONDITION:** Actually, re-reading: the party can still Break him if they can land a Tier 2 somehow. His armor reduces incoming Tier 2→Tier 1 — but if they land a 10+ and he has NO armor reduction (none — he has light armor, always reduces), then they cannot land a Tier 2 on him. This means the Veteran Soldier as written may be effectively unbreakable through normal Strikes. The fight ends when his Endurance hits 0 — but at 0 End he just Absorbs forever and Tier 1s clear each exchange. **This is a design issue to flag.**

**FOR SIMULATION PURPOSES:** Treat the fight as ending when one of these happens:
1. Party is all Broken (Veteran wins)
2. Veteran's Endurance hits 0 AND the party can demonstrate they can maintain sustained Tier 1 pressure forcing Absorbed conditions every exchange indefinitely — at that point, call it a party win (he's effectively neutralized)
3. Party surrenders/flees (Veteran wins by default)

**ALTERNATIVELY — HOUSE RULE FOR THIS SIM:** A character at 0 Endurance who Absorbs a Tier 1 condition takes it as a persistent Tier 2 (the condition has nowhere to go without Endurance to resist). This makes the Veteran breakable at 0 End. Use this rule for the simulation and flag it.

## STRATEGY

**Party:** Focus fire on the Veteran — all three attack him every exchange. Mordai is the primary striker (Weapon Mastery, Easy difficulty). Zulnut supports. Zahna stays Withdrawn unless clearly safe. Goal: force him to spend Endurance on reactions every exchange, deplete his pool, then break him when he can no longer react. Land Tier 2 conditions early if possible (his armor reduces them to Tier 1, but that still forces a reaction from him).

**Veteran Soldier:** One attack per exchange against the highest-threat party member (Mordai first). He cannot force Absorbs (only one attacker), but his +3 modifier and Endurance 7 make him durable. He wins by grinding down Mordai through sustained damage while outlasting the party's offensive output.

## KEY DYNAMIC

Unlike Mook swarms, this fight is a sustained attrition contest. The Veteran cannot force Absorbs (solo enemy), but the party cannot land Tier 2 conditions (armor). The fight is decided by Endurance attrition on both sides, with Sparks as the tiebreaker.

## FORMAT

Exchange-by-exchange:
1. All Postures declared
2. All actions and targets listed
3. Specific dice for every roll (2 dice shown separately, then total with modifier)
4. Reactions declared and resolved for each attack
5. End-of-exchange cleanup (Tier 1 conditions clear, Withdrawn recovery)
6. Full status table after each exchange

**FINAL SUMMARY (required):**
- Winner
- Exchange count
- Party members Broken (names)
- Sparks spent (by whom, how many)
- Final Endurance of all participants
- Whether the armor/Broken issue was triggered

Use varied dice — include highs, lows, and middles. Do not average everything.
