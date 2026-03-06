# Design Issue: Armored Enemy Breaking Condition

**Discovered:** 2026-03-05, during Veteran Soldier simulation design
**Status:** Open — needs ruling before armored Named NPC sims are authoritative

---

## The Problem

Light armor converts all incoming Tier 2 conditions to Tier 1. Tier 1 conditions clear at end of exchange. This means:

- A light-armored Named NPC **can never accumulate a Tier 2 condition** from standard Strikes.
- Broken requires receiving a Tier 2 while already having one.
- Therefore, a light-armored Named NPC **cannot be Broken through standard combat**.

At 0 Endurance, the enemy can only Absorb — but Absorbed Tier 1 conditions still clear at end of exchange. The fight enters an infinite loop: party hits, armor reduces to Tier 1, character Absorbs, condition clears, repeat.

Heavy armor has the same issue, just shifted one tier.

---

## Options Considered

### Option A: 0 Endurance house rule (used in current simulations)
At 0 Endurance, any Absorbed condition (even Tier 1) is treated as a persistent Tier 2.

**Pros:** Simple. Gives armored enemies a meaningful end state. Preserves the "grind them to the floor" fantasy.
**Cons:** Introduces a special case. Slightly unintuitive — why does Endurance affect whether a condition persists?

### Option B: Armor reduces by one tier, not to minimum Tier 1
Light armor: Tier 2 → Tier 1. Tier 3 (if it existed) → Tier 2. But Tier 1 attacks still land as Tier 1.
This doesn't solve the problem — the enemy still can't receive a Tier 2.

### Option C: Armor only applies when the enemy actively reacts
Armor functions as a passive mitigation only when the enemy Absorbs — it has no effect on Parried or Dodged attacks (those are already mitigated). If the enemy has no reaction available (0 End), armor doesn't help.

**Pros:** Elegant — armor protects people who can't dodge. At 0 End (all Absorbs), the first Absorbed Tier 2 sticks, and the second Breaks them. Creates a natural "armor is for people who run out of options" feel.
**Cons:** Slight complexity — armor behavior is context-dependent on reaction availability.

### Option D: Armor reduces the FIRST Tier 2 each exchange, not all of them
Each exchange, the first Tier 2 the character receives is downgraded to Tier 1. Subsequent Tier 2s in the same exchange land fully.

**Pros:** Against single attacker (like the Veteran Soldier scenario reversed) doesn't matter. Against parties with 3 attackers, the second Tier 2 lands. Creates meaningful armor interaction with focus fire.
**Cons:** Adds an exchange-level tracking requirement. Slightly more complex.

### Option E: Treat armor as a flat Endurance bonus instead
Light armor = +2 Endurance (effectively). Heavy = +4. No condition reduction. Simpler mental model, closer to how armor actually works (absorbing hits before they debilitate you).

**Pros:** Eliminates the breaking condition problem entirely. Simpler.
**Cons:** Changes armor from a qualitative system (condition reduction) to a quantitative one (pool extension). Loses the "light armor can't save you from a devastating blow" feel.

---

## Recommendation

**Option A** (0 Endurance house rule) is cleanest for immediate simulation use. It's intuitive enough at the table: "when you're completely spent, even a glancing blow puts you down."

**Option C** is the most elegant long-term design: armor protects you when you're defending; when you're out of options, it doesn't. This creates interesting tactical incentives (keep your Endurance up or your armor stops working).

**Suggested resolution:** Present both to the user. Use Option A for current simulations to get data. Decide Option A vs C for the final ruleset.

---

## Impact on Current Simulations

The Veteran Soldier simulations (V1–V20) use Option A. Results are flagged with "house rule triggered: Y/N." If Option C were used instead:
- Most fights would resolve identically (Option A triggers at 0 End; Option C triggers when enemy has 0 End AND absorbs a Tier 2 — same moment, since armor converts all Tier 2s to Tier 1, so at 0 End the first hit is Tier 1 Absorbed = persistent Tier 2 under Option A, but under Option C it's Tier 2→Tier 1 absorbed = persistent Tier 1... still doesn't Break).

Actually on reflection: **Option C alone doesn't fully solve the problem either.** At 0 End with no reactions, armor still converts the Tier 2 to Tier 1. The persistent Tier 2 still requires a Tier 2 to land.

**Option A is the only option that creates a clean breaking condition for armored enemies at 0 Endurance.** The others either don't solve it or introduce more complexity.

**Recommend adopting Option A as the official rule:**
> *At 0 Endurance, all Absorbed conditions are treated as Tier 2 (persistent). A second Absorbed condition at 0 Endurance triggers Broken.*

This also applies to unarmored characters at 0 End (they could only Absorb Tier 1 before; now those become persistent Tier 2s too). This slightly increases lethality at 0 End for everyone — which is appropriate. Running on empty should be genuinely dangerous.
