# Playtest Report — The Silence of Ashenmoor (Playtest 02)

**Date:** 2026-03-13
**System Version:** Facets of Origin v0.2 (post-audit, data-driven dice, expanded combat/magic)
**Players:** 4 + 1 MM (up from 3+1 in Playtest 01)
**Experience Mix:** Experienced optimizer (Taylor), moderate (Casey), light (Morgan), first-timer (Drew)
**Scenario Type:** Folk horror, escalating difficulty
**Duration:** ~3 hours simulated

---

## Executive Summary

Playtest 02 tested the system under increased stress: more players, harder encounters, horror tone, mixed experience levels, and a brand new player. **The system held up well.** The changes made after Playtest 01 (pre-technique penalty removal, NPC Attack rules, Group Rolls) all functioned as intended. The digital tool successfully supported all session actions with 25/25 Playwright tests passing.

Key findings:
1. **Four-player combat works better than three-player** — more posture variety, genuine tactical options
2. **Domain magic is the star** — Resonance magic's lateral solution was the session highlight
3. **Pre-technique magic balance is correct** — removing the difficulty penalty was the right call
4. **The first-time player had a great experience** — the digital tool + Mook combat system were effective training wheels
5. **Encounter difficulty scaling needs attention** — the Husk Ambush was too easy, the Resonance encounter was skipped via lateral solution

---

## What Worked

### 1. Four-Player Posture Dynamics

With four players, posture combinations became genuinely tactical. The session featured:
- **Withdrawn + Aggressive synergy** — Rowan went Withdrawn to recover Endurance while Morgan went Aggressive to finish the Hollow. The free Intercept from Withdrawn protected the party while the aggressive character dealt damage.
- **Defensive casters** — Casey and Morgan used Defensive posture during the Husk fight to reduce reaction costs, preserving Endurance for magic.
- **Aggressive frontliners** — Taylor and Drew both went Aggressive in Exchange 2 of the Husk fight, creating a burst-damage turn that cleared reinforcements quickly.

In Playtest 01 with three players, posture choices were more constrained. Four players creates genuine "who does what" decisions.

### 2. Domain Magic as Lateral Problem-Solving

Morgan's Resonance magic + Maren's frequency map completely bypassed the Boss fight's conventional combat path. This is **the system working as designed** — Domain + Intent + Scope rewards creative application over raw power.

Key moments:
- Morgan's Specialty (sensing spiritual corruption) identified the structured nature of the silence without a roll
- Attune checks on Maren's drawings provided the counter-frequency data
- The final counter-song (Spirit +1, Attune +1, Hard -1, Spark → 3d6 drop lowest = 11) was dramatically appropriate and mechanically fair

Casey's Warding magic was less impactful but still meaningful — the partial-success ward that weakened the Hollow's Silence Aura changed the fight's trajectory.

### 3. Pre-Technique Magic Balance

After removing the +1 difficulty penalty in the Playtest 01 postmortem, pre-technique magic performed well:
- **Casey (Warding, Standard type):** 2d6+0 at Standard difficulty → 58% success rate expected. Actual: 1 partial success (7), 1 partial success (7), 1 failure (3). 2/3 = 67% — within expected variance.
- **Morgan (Resonance, Standard type):** 2d6+1 at Standard difficulty → 72% success rate expected. Actual: 1 failure (6), 1 full success (12), 1 partial success (8), 1 full success (10), 1 partial success (9), 1 full success (11). 5/6 = 83% — above expected due to Sparks and difficulty adjustments.

The scope limitation (Minor only) was sufficient restriction. Both casters could contribute meaningfully without feeling overpowered. Casey's ward against the Hollow's Silence Aura was appropriately limited — it weakened the effect rather than nullifying it.

### 4. New Player Experience

Drew (first TTRPG ever) had a successful session:
- **Character creation:** 10 minutes using the Builder tab with Taylor's guidance. The tool counted attribute points and showed modifiers automatically.
- **Combat comprehension:** Drew understood "declare posture, then strike or dodge" by the second exchange of the Husk fight. The Mook system (one Strike kills) provided immediate positive feedback.
- **Engagement:** Drew's snake-eyes failure (Roll #5, Wisdom 2) created the Husk ambush and made him central to the scene. Failures generating story rather than punishment is critical for new player retention.
- **Growth arc:** Drew went from "What's two-and-two formation?" to Aggressive posture against Husks in one scene. The Spark award for bravery reinforced the behavior.

The digital tool was specifically effective for Drew:
- The Play Field's combat panel showed posture options, Endurance, and conditions without Drew needing to memorize rules
- The Rules Summary in the Tools tab was referenced for reaction costs
- The roll button abstracted the math — Drew clicked, the tool calculated

### 5. NPC Attack Resolution (New Rule)

The NPC Attack rules added after Playtest 01 worked cleanly:
- Mook attacks → Tier 1 incoming, Standard difficulty reaction → clear end of exchange. Simple, fast, predictable.
- Named NPC (Hollow) → Tier 2 incoming, posture-affected reaction difficulty. Created genuine threat without complexity.
- Boss (Resonance) → Tier 2 incoming + Voice Weaponization (Soul save instead of normal reaction). The Boss's special abilities layered naturally on top of the base NPC attack system.

No confusion about who rolls what. PC-facing rolls only — NPCs attack, PCs react.

### 6. Digital Tool Verification

25/25 Playwright e2e tests passed, covering:
- Session management (login, create, invite, join)
- Character creation with backgrounds
- Attribute rolls, skill rolls, Spark-enhanced rolls, group rolls
- Full combat WebSocket flow (posture → strike → react → end exchange → end combat)
- Magic casting (Resonance + Warding)
- Spark awards (MM + peer nomination)
- Enemy lifecycle (spawn/update/remove)
- Character export, inventory management
- Encounter budget verification
- Skill advancement

41 discrete actions verified. See `digital_tool_log.md` for the complete log.

---

## What Needs Work

### Issue 1: Husk Ambush Was Not Challenging Enough

**Severity:** Low (design issue, not system issue)
**Details:** The 4-Husk ambush was intended as an introductory encounter. Effective TR 4.4 against Party Strength 4 = below Standard budget. The party cleared it in 2 exchanges with no meaningful resource expenditure (Rowan spent 2 Endurance on Parry; everyone else was untouched).

The reinforcement wave (2 more Husks) raised effective TR to 6.6 but the party was in Aggressive posture and cleared them immediately. Total Endurance spent: 2. Total Sparks spent: 0.

**Root Cause:** Mooks are too fragile against a party with two Combat Practiced characters. One-hit kills mean the Mooks never meaningfully threaten the party.

**Recommendation:** For parties with career_advances of 4+, introductory encounters should use either:
- More Mooks (8-10) to create action economy pressure
- Mixed Mook + Named NPC from the start
- Environmental constraints that prevent the party from simply rushing and killing

This isn't a system problem — it's an encounter design lesson for MM Manual Chapter 2 (Session Design). Add a sidebar: *"Mooks are threatening through numbers and positioning, not individual power. Four Mooks against four Practiced characters is a speed bump. Eight Mooks with difficult terrain is a problem."*

### Issue 2: Arena Fighter Specialty Didn't Trigger

**Severity:** Low (scenario design issue)
**Details:** Drew's Arena Fighter specialty ("Reads an opponent's fighting style and general skill level within the first exchange of a fight") never triggered. The Husks have no fighting style (they grapple silently) and the Hollow is incorporeal. The Resonance is a crystal. None of the enemies presented a readable fighting style.

**Root Cause:** Horror scenarios with inhuman enemies don't create opportunities for reading-the-opponent specialties. The MM should have anticipated this and created at least one moment — perhaps a named Husk with distinct combat patterns, or a moment where the Hollow's approach pattern was readable.

**Recommendation:** MM Manual guidance: *"Review every PC's Specialty before the session. Each Specialty should have at least one moment where it could plausibly trigger. If an enemy type doesn't support a Specialty, create a social NPC, environmental detail, or exploration moment that does."*

### Issue 3: Warding Magic Felt Weak Against High-Tier Threats

**Severity:** Medium (design observation)
**Details:** Casey's Warding magic was useful against the Hollow (partial success weakened Silence Aura) but failed hard against the Resonance (failure on attempt to ward against Voice Weaponization). The Boss's power level made Minor-scope wards feel inadequate.

This is partially by design — pre-technique Minor scope shouldn't counter a Boss's primary ability. But the player experience was frustrating: Casey attempted warding three times and got one partial, one partial, one failure. The successes were flavor rather than mechanically decisive.

**Root Cause:** Minor scope wards are personal-scale effects. Boss encounters operate at room scale. The scope mismatch is intentional but can feel bad for the caster.

**Recommendation:** No rules change needed. This is an MM guidance issue:
- Create opportunities for Minor wards to be decisive in non-Boss contexts (warding a door, protecting a specific person from a specific effect)
- When a Minor ward partially succeeds against a Boss ability, make the partial success mechanically meaningful (as was done with the Silence Aura reduction)
- Remind MMs: pre-technique casters are investigators and support, not combat powerhouses. Their magic shines in lateral solutions, not direct confrontation.

### Issue 4: The Boss Encounter Was Bypassed

**Severity:** Medium (expected behavior but worth documenting)
**Details:** The Resonance Boss (TR 14, Deadly encounter) was destroyed via the counter-frequency lateral solution in Exchange 2. The party never experienced:
- The Cacophony ability (once-per-fight Hard Soul save for all characters)
- The Phase Change (wave of stored memories, Mind saves, condition clear)
- The full combat resource tax of a Deadly encounter
- The "2 Husks emerge from walls" post-phase complication

Morgan's successful counter-frequency roll (3d6 drop lowest = 10, +2 modifiers, -1 Hard = 11 full success) ended the fight before the Boss could use its most interesting abilities.

**Root Cause:** The lateral solution was designed to be available. A party that investigates can bypass the Deadly fight. This is working as intended — but it means the Boss design was never stress-tested.

**Recommendation:**
- The Boss design should be preserved and tested in a future playtest where the party either doesn't find the frequency map or fails the counter-frequency roll
- Consider whether the Boss should have a defense against the counter-frequency — perhaps a partial success on the counter-song weakens the crystal but triggers the Phase Change, requiring both the lateral solution AND combat to finish it
- For MM Manual: *"Lateral solutions should feel earned, not easy. If the party does the investigation work and spends resources (Sparks, skill rolls, NPC consultation), they deserve to bypass the fight. If they haven't done the work, the lateral path shouldn't be available."*

### Issue 5: Spark Economy Needs More Earning Opportunities

**Severity:** Medium (recurring from Playtest 01)
**Details:** Starting Sparks: 3 each (12 total). Sparks earned during session: 2 (1 MM award to Drew, 1 peer nomination Taylor). Sparks spent: 2 (Morgan, on the two critical Attune rolls). Net change: 0 for the party overall, but Morgan ended at 1 Spark while others ended at 3-4.

The Spark earning rate of 2 Sparks across 4 players in a 3-hour session feels low. Morgan's two Spark expenditures were dramatically perfect but left her nearly empty. If the counter-frequency had failed, she'd have had limited resources for a second attempt.

**Root Cause:** Spark earning is still vague. The MM awarded one Spark and confirmed one peer nomination. The playtest didn't test:
- Multiple peer nominations per exchange
- Whether the Spark earning rate should be faster
- Whether there should be a "between-scenes" Spark refresh

**Recommendation:**
- Add MM Manual guidance on Spark earning rate: *"Aim for 1-2 Sparks earned per player per session. If a player ends the session at 0, that's fine — they made impactful choices. If a player ends at their starting value, consider whether you're being too stingy with awards."*
- Consider a rule: *"At the start of each Act (or after a major scene transition), each player may nominate one other player for a Spark. The MM confirms or denies."* This creates a natural earning cadence.
- This remains an open design question from the research document. Needs resolution before v1.0.

### Issue 6: Group Roll Not Used in Session

**Severity:** Low (rule exists but wasn't triggered)
**Details:** The Group Roll rules added after Playtest 01 were tested in the Playwright e2e test (Test 23: group Stealth check) but were never used in the actual session narrative. The scenario didn't present a natural "whole party attempts the same thing" moment — the mine descent was narrated without a group check, and combat is individual.

**Recommendation:** Future playtests should intentionally design moments that require Group Rolls — a group stealth approach, a group Athletics challenge (crossing difficult terrain), a group social check (convincing a hostile crowd). The rule exists and passes automated testing, but it hasn't been narratively stress-tested.

---

## Comparison with Playtest 01

| Aspect | Playtest 01 | Playtest 02 | Change |
|--------|------------|------------|--------|
| Players | 3 + 1 MM | 4 + 1 MM | +1 player |
| Experience mix | All moderate | Mixed (expert to newbie) | Better diversity |
| Scenario tone | Standard adventure | Folk horror | Broader register |
| Encounters | 3 (all easy-standard) | 3 (standard, hard, deadly) | Harder, more varied |
| Total rolls | 24 | 32 | +33% |
| Combat exchanges | 4 | 5 | Slightly longer fights |
| Magic uses | 2 (both flavor) | 6 (4 mechanically impactful) | Magic is core gameplay |
| Sparks spent | 0 | 2 | Spark system engaged |
| Pre-technique penalty | +1 step harder | No penalty | Fixed per Playtest 01 |
| Lateral solutions used | 0 | 1 (counter-frequency) | Investigation rewarded |
| PC casualties | 0 | 0 | System is survivable |
| Worst PC state | Endurance 2 | Endurance 1 (Rowan) | Closer calls |
| New player success | N/A | Yes (Drew had great time) | System is accessible |
| Digital tool used | Not tested | 25/25 tests passing | Tool supports full session |

### Key Improvements Since Playtest 01

1. **Pre-technique magic is usable.** Casey and Morgan both contributed meaningfully with magic. The scope restriction (Minor only) provides sufficient limitation without the frustrating +1 difficulty penalty.

2. **NPC Attack rules work.** PC-facing rolls only. Clean, fast, no confusion. Posture-affected reaction difficulty creates tactical depth without complexity.

3. **Harder encounters are survivable.** The Hard encounter (Hollow, TR 11) was won in 2 exchanges through smart play. The Deadly encounter (Resonance, TR 14) was bypassed through investigation. The system creates tension without TPKs.

4. **The digital tool works.** All 25 Playwright tests pass. The Builder handles character creation, the Play Field handles combat, the Tools tab handles reference. The first-time player successfully used the tool as training wheels.

### Remaining Concerns

1. **Spark earning rate** — still too low and too vague. Needs structured earning cadence.
2. **Encounter design guidance** — MMs need more help designing encounters that challenge specific party compositions.
3. **Boss stress-testing** — the Resonance Boss's most interesting abilities were never triggered. Need a combat-focused playtest.
4. **Specialty coverage** — MMs need to audit PC Specialties against scenario content pre-session.

---

## System Suggestions

### For Immediate Implementation
1. Add Spark earning guidance to MM Manual (rate: 1-2 per player per session; between-act nomination window)
2. Add Specialty audit reminder to MM Manual Session Prep checklist
3. Add "Mooks are threatening through numbers" sidebar to MM Manual

### For Future Playtests
4. Run a combat-heavy playtest where lateral solutions are unavailable — stress-test the Boss Phase Change mechanic
5. Run a social/investigation-heavy playtest — stress-test Specialties, Group Rolls, and non-combat magic
6. Run a playtest with a party at career_advances 8-12 — test how the encounter budget scales with advancement

### For v1.0
7. Resolve the Spark earning mechanism (Open Design Question #2 from research document)
8. Add encounter design guidelines to MM Manual Chapter 2 (Session Design) — party composition analysis, Specialty integration, pacing through encounter difficulty curves
9. Consider whether Boss Phase Change should interact with lateral solutions — a partial lateral success triggering Phase Change would create hybrid encounters

---

## Conclusion

Playtest 02 validates the core system under more challenging conditions. The 2d6 resolution system produces appropriately dramatic results (28% full success, 44% partial, 28% failure — matching statistical expectations). Domain magic, specifically the Domain + Intent + Scope framework, creates emergent gameplay that rewards creative thinking. The combat system's exchange-based structure with postures creates genuine tactical decisions, especially with four players.

The first-time player's experience confirms the system's accessibility goals — Drew could participate meaningfully from the first combat exchange, using the digital tool as training wheels. The horror scenario demonstrates the system's tonal range beyond the default register of wonder/heroism/discovery.

The main open question remains Spark economy — earning rate and structured cadence need resolution before v1.0. Everything else is either working as designed or addressable through MM Manual guidance rather than rules changes.

---

*Playtest 02 complete. System version: v0.2 (post-audit). Total tests: 274 (249 unit + 25 e2e).*
