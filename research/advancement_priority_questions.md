# Advancement System — Priority Questions & Topics

*Created 2026-03-03 after initial advancement system design session.*

This document tracks open questions and topics to address in future design sessions, in priority order. Grouped by urgency (must resolve before writing depends on it) and type.

---

## Priority 1 — Blockers for Further Writing

These must be resolved before the system is complete enough to write dependent chapters.

---

### 1. Mind and Soul Facet Skill Lists

**Why urgent:** II.6 (Skills) currently stubs out Mind and Soul skills with "defined in Chapter II.5." That stub will need to be filled before the PHB is coherent. Every downstream chapter that touches skill rolls needs the full skill list.

**What to design:**
- ~5 broad skills for Facet of the Mind (governing Intelligence, Wisdom, Knowledge)
- ~5 broad skills for Facet of the Soul (governing Spirit, Luck, Charisma)
- Associated Minor Attribute for each skill
- Coverage check: do the 15 total skills cover everything players will want to do?

**Design constraint:** Skills should be broad enough to cover wide fictional ground but narrow enough that Expert rank in one means something. Body's five skills are the template.

---

### 2. Backgrounds (II.5)

**Why urgent:** Backgrounds grant the only starting skill advantage (one skill at Practiced). Until Backgrounds exist, character creation is incomplete and the skill system has an unanchored exception.

**What to design:**
- What is a Background? (Prior life, not class — occupation, origin, or formative experience)
- How many Backgrounds? (Suggest 8–12 for a core PHB)
- What does each grant beyond one Practiced skill? (Narrative hooks? Starting equipment? MM prompts?)
- Do Backgrounds interact with Facets? (A soldier Background + Body Facet vs. a soldier Background + Mind Facet should feel different)

**Design constraint:** Backgrounds should encourage RP and suggest character history, not just grant mechanical bonuses.

---

### 3. Pinnacle Techniques — Design Framework

**Why urgent:** Major Advancement offers "+1 attribute OR a Pinnacle Technique." Pinnacle Techniques are currently defined only as "powerful, requires MM approval, culmination of long arc." That is not enough for players or MMs to work with.

**What to design:**
- What is the power ceiling of a Pinnacle Technique vs. a Tier 3 Technique?
- Are Pinnacle Techniques from a list, or fully freeform? (List = consistent; freeform = more personal but harder to balance)
- What does MM approval actually mean in practice? (Veto? Collaborative design? Checklist?)
- Should each Facet have suggested Pinnacles, or is this entirely narrative?

---

## Priority 2 — Calibration (Requires Playtesting, But Needs Estimates Now)

These are numbers that will need adjustment after play, but we need working estimates to write examples and vignettes.

---

### 4. Session Skill Point Economy

**The question:** Is 4 skill points per session the right number?

**What it affects:**
- 4 points, all in Primary Facet successes (cost 1 each) = 4 skill marks per session
- 4 points, all outside Primary Facet failures (cost 4 each) = 1 skill mark per session
- At 3 marks per rank: a Primary Facet skill advances roughly every session. An out-of-Facet skill advances roughly every 4 sessions (success) to 12 sessions (failure).

**The tension to calibrate:** Advancement should feel frequent enough to be satisfying but not so fast it feels cheap. The research says PbtA flattens — we want the crawl to feel like growth, not like grinding.

**Suggested playtesting benchmark:** A character should reach Practiced in their two or three most-used skills within 5–8 sessions. Expert rank should feel like a genuine achievement at ~15+ sessions.

---

### 5. Facet Level Threshold (6 advances per level)

**The question:** At 6 skill rank advances per Facet level, how long does a Facet level take?

**Math:**
- 5 skills × 2 advances each (Novice→Practiced→Expert) = 10 total advances per Facet
- At 6 advances per level: Facet level 1 at advance 6, Facet level 2 at advance 12 (impossible — only 10 advances available)
- **Problem:** With 5 skills and 2 ranks each, a fully-developed Body Facet only produces 10 advances — meaning a character can only ever reach Facet level 1 in a single Facet under the current math.

**This is a blocker.** Options:
- Lower threshold (e.g., 4 advances per Facet level → levels 1 and 2 reachable, level 3 requires cross-training or a third rank tier)
- Add a third skill rank (Master: +3, 9 marks total) so 5 skills × 3 advances = 15 total advances → Facet levels 1, 2 possible; level 3 requires nearly maxing the Facet
- Add more skills per Facet (7–8 instead of 5)
- Reframe: Facet levels count all marks, not just rank advances (more granular but harder to track)

**Recommendation to discuss:** Add a Master rank (+3 modifier, 9 total marks) to create a genuine long-campaign ceiling. This gives 5 skills × 3 advances = 15 advances per Facet, supporting Facet levels 1, 2 (at 6 and 12 advances). Level 3 remains achievable only by cross-training or a dedicated campaign. Keeps the "rare and weighty" feel for major milestones.

---

### 6. Major Advancement Threshold (4 Facet levels)

**The question:** With the math problem above, this threshold may need to move in tandem with whatever fixes the Facet level threshold.

**Hold this question** until #5 is resolved.

---

## Priority 3 — Design Topics for Future Sessions

These are important but not blockers — they can be deferred until the relevant chapter is being written.

---

### 7. Cross-Facet Advancement Ceiling

**The question:** Should highly invested cross-Facet skill development ever unlock anything, or is specialization the ceiling?

**Options:**
- Hard ceiling: cross-Facet skills advance but never contribute to Facet levels or Techniques
- Soft ceiling: at very high cross-Facet investment (e.g., Expert in 3+ skills outside Primary Facet), you may declare a Secondary Facet and gain access to Tier 1 Techniques from it
- Multiclass-lite: characters can shift their declared Primary Facet after a Major Advancement, representing a genuine life change

**Design tension:** Cross-Facet growth should feel hard-won but not pointless. The current cost structure (4 points for an out-of-Facet failure) is steep — it needs to mean something.

---

### 8. The "Failure Outside Your Facet" Problem

**The question:** At 4 points per mark, failing outside your Primary Facet is economically near-useless. This might read as "failure teaches you nothing when you're out of your depth" — which is thematically coherent — or it might punish player curiosity.

**Design tension:** The research says the adventure register is wonder and discovery. A player who tries something new and fails repeatedly, gaining almost nothing for it, may stop trying new things. Consider:
- Does this need softening? (e.g., failure outside Facet costs 3, not 4)
- Or is this intentional gating that keeps characters from being generalists too easily?

---

### 9. Mind and Soul Facet Technique Trees

**The question:** Once the skill lists for Mind and Soul are designed (#1), their Technique trees need the same treatment as Body's three-branch tree.

**Design constraint:** Must fit the adventure register (wonder, discovery, heroism) — Mind Techniques should feel like *knowing things others don't* and *seeing what others miss*, not just "+1 to rolls." Soul Techniques should feel like *moving people* and *bending fate*, not just social buffs.

---

### 10. Reflection Scene Design (MM Guide)

**The question:** How do MMs run reflection scenes well? This was deferred to the MM Guide, but it needs thought before that chapter is written.

**What to address:**
- How long should a reflection scene be? (Brief aside vs. full scene for Major Advancement)
- Who narrates it — the player, the MM, or collaboratively?
- What makes one feel earned vs. procedural?
- How does the MM find the right fictional moment rather than forcing it at a mechanical threshold?
- How does a reflection scene interact with the rest of the party? (Witnessed, but how engaged are others?)

---

### 11. One-Shot Compatibility

**The question:** The current advancement system is campaign-oriented. A one-shot player will never see a Facet level or Major Advancement. Is that acceptable, or should there be a one-shot advancement variant?

**Research note:** The market gap analysis flags one-shot accessibility as a driver of initial adoption. If the advancement system is invisible in a one-shot, new players may not understand what they're building toward.

**Options:**
- Accept that advancement is a campaign feature; one-shots use pre-built characters
- Design a "compressed advancement" variant for one-shots (e.g., start at Practiced in 2 skills, gain 1 Technique at session midpoint)
- Write a one-shot character creation variant with pre-chosen Techniques

---

## Summary: What to Cover Next Session

**If mechanics-focused:**
1. Fix the Facet level math (question #5) — this is a blocker
2. Mind and Soul skill lists (#1)
3. Background design scope (#2)

**If narrative/RP-focused:**
1. Reflection scene design (#10)
2. Background concepts and hooks (#2)
3. Adventure register check on Technique writing

**If calibration-focused:**
1. Facet level math fix (#5)
2. Cross-Facet ceiling decision (#7)
3. Failure-outside-Facet cost check (#8)
