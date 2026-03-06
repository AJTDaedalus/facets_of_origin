# Dice System Analysis: Facets of Origin
## Synthesis of Market Research & Psychology Research

*Brainstorming branch document. Knowledge base through August 2025.*

---

## Design Goals (from CLAUDE.md)

- **Prioritize**: fun, socializing, worldbuilding, storytelling
- **Minimize**: rules complexity, complicated mechanics, gameplay friction
- **Digital-first**: software absorbs bookkeeping so humans focus on narrative
- **Adventure register**: wonder, discovery, heroism — not trauma/darkness by default

---

## What the Research Says

### The Psychology of Dice

**Bell curves feel fairer and more skill-based than flat distributions.**
A d20's uniform distribution means a 5% chance of any number — a skilled character still fails catastrophically as often as a novice. 2d6's bell curve compresses extremes so that character competence actually shows up in outcomes. Players with internal locus of control (the dominant personality type drawn to TTRPGs) find high-variance flat dice more frustrating unless they have strong pre-roll agency to mitigate it.

**Partial success is the psychologically richest outcome space.**
Vincent Baker designed the 7-9 band in Apocalypse World specifically to keep narrative tension alive regardless of outcome. This maps directly onto Csikszentmihalyi's flow channel: the player succeeds enough to feel competent, but the complication ensures challenge remains. Clean success is anti-climactic; clean failure is demoralizing; partial success with a cost keeps everyone engaged.

**The near-miss effect is real — and socially amplified.**
Rolling one short of a threshold triggers the same dopamine response as winning. At a table, this effect is multiplied by shared witness (Lazzaro's "People Fun multiplier"). This means dice with visible tension — a roll that could go either way — are more socially bonding than dice whose outcome is obvious before the result.

**Pre-roll agency converts frustration into drama.**
Without it, bad rolls feel unjust (Ladouceur & Sévigny, 2005). With it — positioning, resource spending, preparation — the same bad roll feels like bad luck within a frame the player influenced. Every narrative game that works has a pre-roll agency layer: Fate's Invokes, D&D 5e's Advantage, Blades in the Dark's Position/Effect.

**Cognitive load kills narrative transportation.**
The moment a player calculates modifiers, they've left the fictional world (Sweller's Cognitive Load Theory + Green & Brock's transportation research). Working memory holds ~4 novel chunks; any resolution requiring more than that for a new player disrupts immersion. Three-session rule: systems need to automate within 3 sessions or dropout risk spikes.

**Social memory generation is a design goal, not a side effect.**
Near-TPKs, critical successes at crucial moments, and dramatic failures that everyone remembers are flashbulb memories (Brown & Kulik). They become group mythology and are the primary reason players keep returning to the same group for years. High-variance dice + dramatic public resolution + real stakes = social memory generators.

### What the Market Has Tried

| System | Game | Outcome Tiers | Accessibility | Narrative Integration | Key Problem |
|---|---|---|---|---|---|
| 2d6 + stat | PbtA (Apocalypse World, Dungeon World) | 3 (10+/7-9/6-) | Very High | Excellent | Stat modifier weight too large; GM burnout in long play |
| d6 pool, take highest | Blades in the Dark | 3 (6/4-5/1-3) | Moderate | Excellent (Position/Effect) | Counterintuitive; not a beginner system |
| 4 Approaches + dice pool | Fate Accelerated | Pass/Fail + Aspect economy | Low (Aspect economy) | High when working | "Nobody compels" — meta-layer rarely engaged |
| Multiple dice (d4-d20) by stat | Kids on Bikes | Pass/Fail | High (D&D-familiar) | Low (no outcome tiers) | Binary result misses the partial success opportunity |
| 2d10 challenge + 1d6/d10 action | Ironsworn | 3 + "Match" twist | Moderate | Excellent (solo/async) | Explanation overhead for 2-challenge-dice |
| d20 + modifier | D&D 5e | Binary + crits | Extreme (cultural) | Poor (built for combat) | Dead-end failures; no narrative complication structure |

### Market Gaps Directly Relevant to Facets of Origin

The research identifies these unmet needs, all aligned with our goals:

1. **Adventure-register narrative game** — rules-light, story-first design applied to *fun* (wonder, heroism, discovery) rather than trauma/darkness. Avatar Legends and Kids on Bikes partially fill this, but neither has deep mechanical support for long campaigns.
2. **Digital-native design** — games built from the ground up for online/async play with companion apps, clear text-friendly triggers, and fewer physical-component dependencies.
3. **Beginner-clear capability design** — players know what their character can do without reducing it to an action menu. The "what do I say?" problem for new players.
4. **Long-campaign mechanical support** — PbtA advancement flattens; FitD characters retire. Nobody has solved 30-50 session narrative-first arc design cleanly.
5. **GM-easy that actually is** — games claiming reduced GM burden often still require elite improv skills. Built-in situation generators, NPC frameworks, and pacing tools, not just a "no prep needed" promise.

---

## Candidate Dice Systems

### Option A: 2d6 + Approach (PbtA-Standard)
Roll 2d6, add an Approach modifier. 10+ = full success. 7-9 = success with cost/complication. 6- = things go wrong, but the story advances (never a dead end).

- **Psychological profile**: Optimal. Bell curve, three tiers, partial success as modal outcome.
- **Market validation**: The most tested and community-validated narrative-first mechanic in the hobby.
- **Accessibility**: Very high. Two dice, one addition, three memorable outcome bands.
- **Risk**: Perception of being "another PbtA game." Differentiation must come from everything around the mechanic, not the mechanic itself.

### Option B: d6 Pool, Take Highest (FitD-Style)
Assemble a pool of d6s equal to your relevant trait (1-4 dice). Take the single highest result. 6 = full success. 4-5 = partial. 1-3 = bad outcome.

- **Psychological profile**: Strong. Pool size communicates competence visually and tactilely. Dramatic visual of many dice.
- **Market validation**: Well-validated but skews toward experienced players. Not a beginner system.
- **Accessibility**: Moderate. "Take highest" is counterintuitive; pool assembly requires explanation.
- **Risk**: Higher onboarding cost; feels more mechanical than conversational.

### Option C: 2d6 + Momentum Die (Novel Hybrid)
Roll 2d6 for outcome tier (same bands as PbtA). Separately, roll a "Momentum Die" (d6) whose result adds a narrative flourish or resource gain on success, or a complication flavor on failure — independent of whether you succeeded. This separates *did it work?* from *how did it feel / what else happened?*

- **Psychological profile**: Strong. The Momentum Die extends the anticipation window, generates more dice-rolling social performance, and produces a second narrative beat per roll.
- **Market validation**: Unvalidated — novel. Related to Ironsworn's "Match" concept and Fate's Invoke system.
- **Accessibility**: Moderate. Two types of dice with different meaning requires careful onboarding.
- **Risk**: Added complexity may violate the "minimize friction" goal. Needs playtesting to confirm it reads as "more interesting" rather than "more complicated."

### Option D: 2d6 + Spark (Simplified Hybrid)
Roll 2d6 for outcome. If you spend a "Spark" (a narrative resource), add a third d6 and drop the lowest. The Spark system provides pre-roll agency without changing the core mechanic — spending Sparks is the agency layer.

- **Psychological profile**: Excellent. Preserves the clean 2d6 bell curve, adds pre-roll agency (addressing the locus-of-control problem), and makes resource management feel like a genuine player choice.
- **Market comparison**: Similar to Blades in the Dark's devil's bargain + stress system, but simpler. Closest existing analog is D&D 5e's Advantage but with an economy attached.
- **Accessibility**: High. The base mechanic is identical to PbtA. Sparks are a simple layer on top.
- **Risk**: Spark economy needs careful calibration — too scarce and players hoard rather than engage; too plentiful and the pre-roll tension disappears.

---

## Recommendation: Option D with Option A Foundation

**Core mechanic: 2d6 + Approach**

The 2d6 three-tier outcome system is the optimal foundation. The research is unambiguous:
- Bell curve provides fairness feel and skill-outcome correlation
- Three tiers (full/partial/bad) eliminate the "nothing happens" whiff problem
- Partial success as modal outcome keeps flow channel active
- Two dice is the lowest cognitive load for meaningful variance
- The market has validated this design across dozens of successful games

**Differentiation: Spark System for Pre-Roll Agency**

Before rolling, a player may spend one or more Sparks (earned through play — roleplay moments, compelling complications, group consensus on a great idea) to add +1d6 per Spark spent and drop an equal number of lowest dice. This:
- Solves the pre-roll agency problem (locus of control research)
- Creates a narrative-economy layer that rewards engagement without the "nobody compels" Fate problem (Sparks are earned through positive action, not by accepting complications)
- Extends the dice-rolling performance window (more dice on the table = more anticipation)
- Remains invisible as a base layer — players who don't spend Sparks experience a clean 2d6 game

**Differentiation: Outcome Advancement**

Never a dead end. Ever. The 6- result should explicitly be framed as "the story advances — at a cost." The digital tool handles suggesting what that cost looks like based on context (a GM-assist oracle), reducing the improvisation burden that burns out GMs in standard PbtA.

**Differentiation: Adventure Register**

The specific moves, playbooks, and oracle tables are tuned to adventure-forward fiction: discovery, camaraderie, heroism, wonder. This is not a mechanical distinction from PbtA — it's a tonal and content one. The game doesn't mechanize grief or trauma; it mechanizes *doing cool things together and telling stories about them*.

**Digital Integration Points**

The companion app (core to the digital-first design) handles:
- Spark tracking and award prompting
- Outcome suggestion on 6- results (oracle assist)
- Move trigger display (solves "when do I roll?" problem for new players)
- Session chronicle logging (automatic capture of key dice moments for group mythology)
- Character advancement tracking across long campaigns

---

## Resolved Design Decisions

### Advancement System (resolved 2026-03-03)

**Advancement model:** Three-track system inspired by Morrowind (skill use → Facet levels → Major Advancement).

**Skills:** ~5 broad skills per Facet (15 total). All skills start at Novice. Three ranks: Novice (+0), Practiced (+1), Expert (+2). Skill modifier stacks with attribute modifier; maximum combined +3.

**Session skill economy:** 4 skill points per session, spent on skills used that session only. Cost matrix:
- Primary Facet + success: 1 point
- Primary Facet + failure: 2 points
- Outside Primary Facet + success: 2 points
- Outside Primary Facet + failure: 4 points

**Marks to advance a skill rank:** 3 marks per rank (Novice→Practiced, Practiced→Expert). Marks carry between sessions.

**Facet levels:** Every 6 skill rank advances within a Facet = 1 Facet level. Each Facet level unlocks one Technique from the Facet's tree.

**Technique trees:** Three branches per Facet (mirroring the three Minor Attributes). Three tiers; tier 2 requires one tier 1 in the same branch, tier 3 requires one tier 2. Body tree designed (Might/Grace/Iron branches). Mind and Soul trees pending.

**Primary Facet:** Declared at character creation.

**Major Advancement:** Every 4 Facet levels in Primary Facet. Choice of +1 Minor Attribute (max 3) or Pinnacle Technique. Requires significant reflection scene.

**Reflection scenes:** Once per session. Advancement is potential until the reflection scene makes it real in the fiction. MM guide will cover running them. Major Advancements require a full scene; standard advancements are a brief witnessed moment.

**Research alignment:** This system directly addresses the market gap identified in the research — "nobody has solved 30–50 session narrative-first arc design cleanly." The Morrowind-style model provides organic long-campaign growth without the PbtA flattening problem (stats max out) or FitD retirement problem (advancement = countdown). The fiction-first trigger (reflection scene) and use-based skill growth both reinforce the RP-rewards-mechanics design goal.

**Open calibration questions (not yet playtested):**
- Is 4 skill points per session the right economy? (Too few = players feel stuck; too many = advancement feels cheap)
- Is 3 marks per rank right? (Affects how fast skills move)
- Is 6 advances per Facet level right? (Affects how often Techniques unlock)
- Is 4 Facet levels per Major Advancement right? (Affects how rare attribute increases feel)

---

## Open Design Questions for Next Phase

1. **Approach vs. Stat naming**: Should character traits be named as fictional roles ("Brave," "Clever," "Swift") or narrative approaches ("Forcefully," "Carefully," "Cleverly")? Approaches map better to fiction-first play; stats map better to D&D-adjacent player expectations.

2. **Spark economy calibration**: How are Sparks earned? Per session? Through specific moves? Through group acclaim? The earning mechanism defines what behavior the game rewards.

3. **Move trigger specificity**: PbtA-style explicit triggers ("When you attempt something risky...") vs. lighter guidance ("Roll when the outcome is uncertain and the stakes matter"). Specific triggers solve the "when do I roll?" problem but require more design work per situation.

4. **GM role**: Full GM (reduced burden via tools), rotating GM, or GM-optional? The market gap is a game that genuinely eases the GM role. The digital assistant oracle is one lever; GMless design is another. These require different structural decisions early.

5. **Session length target**: One-shot-friendly structure (For the Queen, Kids on Bikes) vs. campaign arc design (Blades, Ironsworn)? The market gap is long-campaign narrative design, but one-shot accessibility drives initial adoption. Both are achievable but require explicit arc-pacing design.

6. **Advancement calibration (playtesting needed)**: The numbers in the advancement system (4 points/session, 3 marks/rank, 6 advances/Facet level, 4 Facet levels/Major Advancement) are design estimates. All four thresholds need playtesting to confirm they produce the right pacing feel.

7. **Cross-Facet advancement ceiling**: Currently, cross-Facet skill development is possible but expensive and does not contribute to Primary Facet levels or Major Advancement thresholds. Should there be any cross-Facet Technique access at high investment, or is specialization the intended ceiling?

8. **Backgrounds and starting skills**: Backgrounds (II.5, not yet written) can grant one skill at Practiced rank. The scope and list of Backgrounds needs design — this affects starting character differentiation and how "prior life" is mechanized.

9. **Mind and Soul Facet trees**: Body is fully designed. Mind and Soul Facet trees (skill lists and Technique trees) need the same treatment.

10. **Pinnacle Techniques**: The Major Advancement alternative to +1 attribute. These are deliberately left vague ("requires MM approval, should feel like culmination of a long arc") — but they need a design framework and examples before the system is complete.

---

## Sources

**Psychology:**
Ryan & Deci (2000), Self-Determination Theory; Lazzaro (2004), 4 Keys to Fun (GDC); Csikszentmihalyi (1990), Flow; Griffiths (1991), near-miss effect; Schultz (1997), dopamine and prediction; Green & Brock (2000), narrative transportation; Sweller (1988), cognitive load theory; Seligman & Maier (1967), learned helplessness; Edmondson (1999), psychological safety; Rotter (1966), locus of control; Baker (2010), Apocalypse World design notes; Harper (2017), Blades in the Dark; Laws (2002), Robin's Laws; Koster (2005), A Theory of Fun.

**Market:**
Training knowledge synthesis through August 2025 covering: r/rpg, r/PBtA, r/bladesinthedark, r/Ironsworn, r/narrativegames, r/FATErpg community patterns; ICv2 industry reporting; EN World; Dicebreaker; The Gauntlet Gaming Community; Deeper in the Game (Chris Chinn); Gnome Stew; published game texts for Apocalypse World, Dungeon World, Blades in the Dark, Ironsworn, Starforged, Masks, Monsterhearts, Kids on Bikes, Fate Core, Fate Accelerated, Wanderhome, For the Queen, Microscope, Trophy Dark/Gold, Avatar Legends.

*Note: Live verification recommended for post-August 2025 releases, current DriveThruRPG/Itch.io rankings, and Kickstarter outcomes from 2024-2025.*
