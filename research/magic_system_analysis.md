# Magic System Analysis: Facets of Origin
## Synthesis of Market Research, Design Theory, and Player Psychology

*Created 2026-03-04. Informs design of the magic subsystem for the Facet of the Soul and any magic-adjacent mechanics in the PHB and setting Facets.*

---

## Design Goals (established constraints)

From CLAUDE.md and the dice system research:

- **Maximize player agency** — players should feel like architects of what magic does, not executors of a menu
- **Rule of cool** — magic should produce the "table sits up" moments, not be the thing everyone has looked up and memorized
- **Minimize reference friction** — no long spell lists; magic users should be able to play without stopping to look anything up
- **Adventure register** — wonder, discovery, heroism; magic should feel *surprising* even to the player using it
- **Digital-first** — the app absorbs bookkeeping, so the magic system can be slightly more complex mechanically as long as the *player-facing* interface stays clean
- **15 total skills** — magic must fit within the existing skill framework, not require a parallel system

---

## What the Research Says

### The Psychology of Magic in Games

**Magic works best when it produces stories, not transactions.**
The psychological appeal of magic in games is primarily about agency expansion — the sense that your character can do things outside normal physical possibility. Csikszentmihalyi's flow channel applies directly: magic that is too easy (infinite, costless) produces boredom; magic that is too restricted (spell slots, rigid lists) produces anxiety about resource management rather than narrative immersion. The sweet spot is magic that feels *consequential* without feeling *constrained*.

**Uncertainty is the soul of wonder.**
Green & Brock's narrative transportation research shows that the "what could happen?" state is more engaging than the "I know exactly what will happen" state. Spell lists destroy this for experienced players — they've seen every outcome. Freeform or open-ended magic preserves uncertainty even for veterans. The *surprise of the magic working in an unexpected way* is a social memory generator.

**Ownership drives engagement.**
Self-Determination Theory (Ryan & Deci) identifies autonomy as the primary driver of intrinsic motivation. A magic system where players describe what they want their magic to *do* — rather than selecting from a predetermined list — gives players authorship over their magic. This is structurally distinct from choosing between Fireball and Lightning Bolt: in the latter, someone else made the interesting choices; in the former, the player is the author.

**The "fiction-first" magic paradox.**
Fiction-first magic (Ars Magica, Mage: The Ascension) is maximally expressive but imposes enormous cognitive load on the MM — they must adjudicate every effect from scratch. This is the primary failure mode: creative freedom for one player generates creative labor for the MM. The research on GM burden is consistent: any mechanic that regularly puts the MM in a "now I must invent a ruling on the spot" position will eventually cause GM burnout or inconsistency.

**Cost and consequence create meaning.**
Without cost, magic is just a cheat code — and players unconsciously treat it as such. Brandon Sanderson's "First Law of Magic" (the degree to which a magic system can solve problems is proportional to how well the reader/player understands its costs and limitations) is well-grounded in motivation psychology: effort + constraint = meaning. The cost doesn't need to be large; it needs to be *legible* and *real*.

---

## What the Market Has Tried

### Approach 1: Spell Lists (D&D, Pathfinder, most OSR)

Players select spells from a fixed list. Spells have defined effects, ranges, and costs (spell slots, spell points, memorization).

**What works:**
- Crystal-clear: both player and MM know exactly what the spell does
- Balance is tractable: each spell has been designed to occupy a specific power niche
- Players can develop real expertise with their spell loadout

**What fails:**
- Requires the longest rulebook section in the game (over 300 pages of spells in D&D 5e PHB)
- Magic becomes a lookup problem, not a creative one — the interesting question is "which spell do I use?" not "what do I want to create?"
- Player agency is confined to selection from a menu someone else designed
- High-level magic users effectively have a spreadsheet problem, not a roleplaying one
- New players are paralyzed: "I have 23 spells, I don't know which one to use" is the single most common new-player complaint about D&D casters
- No room for the unexpected — a player who has Fireball cannot make fire do anything Fireball doesn't say it does

**Rule of Cool compatibility:** Low. The best moments happen when a player attempts something the rules don't cover; spell lists eliminate this space almost entirely.

---

### Approach 2: Freeform Narrative Magic (Mage: The Ascension, Unknown Armies)

Players describe what their magic does. The MM adjudicates success and cost. There is a broad framework of magical "spheres" or domains, but no spell list.

**What works:**
- Maximum creative expression — players genuinely author their magic
- Every use of magic is potentially a "table sits up" moment because the outcome isn't predetermined
- The fiction leads entirely; the mechanic follows
- Magic feels *magical* — genuinely unpredictable even after hundreds of hours

**What fails:**
- Enormous MM burden — every effect requires live adjudication and implicit power-level assessment
- Wildly inconsistent between sessions and MMs — "can my magic do this?" has no stable answer
- Power creep is nearly uncontrollable — experienced players find ways to justify ever-escalating effects
- Creates adversarial dynamic between players and MM around "is this reasonable?"
- Not accessible to new MMs at all; requires experienced facilitators

**Rule of Cool compatibility:** Extremely high, but at unsustainable cost to the MM.

---

### Approach 3: Verb + Noun Free Magic (Ars Magica's Hermetic System)

Magic is constructed from combinations of **verbs** (Creo/create, Perdo/destroy, Muto/transform, Rego/control, Intellego/sense) and **nouns** (Forms: Animal, Aquam, Auram, Corpus, Ignem, etc.). Skill in each verb and noun is rated separately; combining them produces any effect within the fiction of "what this verb does to this noun."

**What works:**
- Genuinely generative: the system creates a large combinatorial space from a small set of elements
- Players can improvise confidently because they know their verb-noun competencies
- Effect scope is bounded by competency, not by a list
- MMs have a consistent framework for adjudicating improvised effects
- Scales elegantly — more verbs and nouns = more magic, fewer = a limited practitioner

**What fails:**
- Still requires learning a vocabulary (10 verbs + 10+ nouns in Ars Magica)
- The combination system can feel mechanical rather than magical — "I combine Creo and Ignem for fire creation" is still a lookup problem, just with fewer elements
- Calibrating the power level of any given combination requires experience
- Not designed for fast, session-length play — Ars Magica is built for campaign-years-long stories

**Rule of Cool compatibility:** High, once players internalize the vocabulary. The first few sessions have a learning curve.

---

### Approach 4: Flexible Spell Templates / Schools (13th Age, Numenera)

Rather than spell lists, players have broad **magical domains** or **schools** with flexible effects. A Fire Mage can do anything fire-related — the question is degree and consequence. 13th Age's "flexible attacks" and Numenera's "cyphers" both push in this direction.

**What works:**
- Much smaller cognitive footprint than full spell lists
- Players become specialists who feel genuinely expert in their domain
- Natural "rule of cool" space: if you're the fire mage, fire can do surprising things
- Domain expertise is easy to communicate: "I'm a storm mage" is enough for a new player to play

**What fails:**
- Domain boundaries create weird edge cases ("can an earth mage affect stone structures?")
- Power balance between domains is tricky — some domains (time, mind) are intrinsically more versatile than others
- Still somewhat list-like within domains in many implementations

**Rule of Cool compatibility:** High. Domain specialists naturally get interesting moments when they apply their domain creatively.

---

### Approach 5: Resource Pool + Fictional Outcomes (Blades in the Dark's Attune, Ironsworn's Rituals)

Magic is handled with the same resolution system as everything else. A relevant attribute or action (Attune in FitD, Ritual moves in Ironsworn) is rolled; the effect is described fictionally based on the tier of outcome. There is no spell list — the player describes what they're attempting, and the outcome tier determines how well it works.

**What works:**
- Zero additional mechanical overhead — magic is just fiction shaping the roll
- Partial success tiers are intrinsically well-suited to "magic works but with a cost/twist"
- Magic-users don't need a separate mechanical ruleset to learn
- Every magical effect is potentially surprising — the player describes intent, the dice describe outcome
- Scales naturally with the main resolution system's difficulty framework

**What fails:**
- Can feel undifferentiated — magic users don't feel *different* from non-magic users mechanically
- The "what can my magic do?" question has no clear answer in a new situation, throwing it back to the MM
- No built-in cost or consequence structure — magic can feel too easy (just roll Attune)
- Long-term: magic-users don't feel like they've *grown* as magical practitioners in the way fighters grow in combat competence

**Rule of Cool compatibility:** Very high when it works, but inconsistent — depends heavily on MM willingness to say yes to magical descriptions.

---

### Approach 6: Intent + Effect + Cost (Powered by the Apocalypse variants, Avatar Legends)

When you use magic, you declare **intent** (what you want to do), **effect** (what you think it looks like), and then roll. The outcome tier determines how much of your intent is achieved. A cost (Sparks, stress, a condition) is always paid on a partial success. Some games (Avatar Legends, Masks) tie this to specific narrative moves ("When you redirect an incoming attack using your bending...").

**What works:**
- Moves ensure consistency without a spell list — the move trigger tells you when to roll, the outcome tier tells you how well it worked
- Player describes the *what*; the dice and moves describe the *how much*
- Partial success is perfect for magic — "you redirect the fire, but it catches something you didn't intend" is a natural tier-2 outcome
- Cost structure is built in (7-9 always has a complication)

**What fails:**
- Still requires writing a meaningful set of moves for each magical tradition — moves are not spell lists, but they're still a design artifact that players must learn
- Avatar Legends ties magic to bending styles (earth/water/fire/air) — works for that setting, but the framework needs adaptation for other settings
- Without moves, the system degrades to Approach 5 (just roll the relevant stat)

**Rule of Cool compatibility:** High. The move trigger is often broad ("when you bend with intent"), leaving the specific effect in the player's hands.

---

## The Core Design Tension for Facets of Origin

The tension is:

**Left pole — Maximum Agency (Freeform):** "My magic can do anything I can imagine, within the fiction."
- Pro: true player authorship, maximum rule-of-cool moments
- Con: MM adjudication burden, inconsistency, power creep

**Right pole — Maximum Clarity (Spell Lists):** "My magic does exactly what the spell says."
- Pro: zero ambiguity, predictable balance
- Con: reference friction, no creative space, menus instead of authorship

The research says the right answer is in the middle, **biased toward the agency end** — because:
1. The digital layer can absorb adjudication consistency (the app can give the MM reference examples and guidelines)
2. The adventure register depends on surprise and wonder — spell lists kill both
3. The three-tier outcome system already provides a natural cost/consequence structure for partial success
4. The Facet system's Technique trees are the natural home for player-specific magical capabilities

The design goal is: **a player should be able to describe what they want their magic to do, know roughly how hard it is, roll, and have the outcome be narratively interesting — without looking anything up**.

---

## Design Approaches That Best Fit Facets of Origin

Ranked by compatibility with Facets' established design:

### Tier 1: Strong Fit

**A. Domain + Intent Model (Recommended starting point)**

Each magic-capable character has a **Magical Domain** — a broad thematic territory (fire, time, beasts, death, light, illusion, etc.). Within their domain, players describe what they want to do and roll the appropriate attribute. The domain *licenses* the effect: it tells both the player and the MM what's on the table without prescribing specific spells.

Domains are wide enough that creative applications are always possible. The MM's job shifts from "is this on the list?" to "is this within your domain?" — a much lower-burden question with an obvious fictional answer.

- **Player cognitive load:** Low. "What does fire do?" is a question a player can answer themselves.
- **MM burden:** Low. Domain scope adjudication is a one-time conceptual conversation at character creation, not session-by-session lookup.
- **Rule of cool:** High. Domain-based magic naturally rewards creative thinking about what fire, time, or sound *can do* that nobody's tried yet.
- **Fits Facet system:** Yes. Domains can be selected at character creation as part of a Soul Facet Technique, or as a Background element. Technique trees can then represent depth of domain mastery.

**B. Intent + Scope System (Well-suited as a layer on top of A)**

When a player invokes their domain, they declare **scope** — how significant the effect is:

| Scope | Description | Difficulty |
|---|---|---|
| Minor | Small effect, limited area, brief duration | Standard |
| Significant | Meaningful effect, moderate area or duration | Hard |
| Major | Scene-changing effect, large area or long duration | Very Hard |

The MM sets difficulty based on declared scope (using the existing difficulty table from II.2). The player rolls their magical attribute. The outcome tier determines how cleanly the intent is achieved:
- **10+:** The effect works as described.
- **7–9:** The effect works, but with a complication — it affects more than intended, costs more, or creates an unexpected consequence.
- **6−:** Something goes wrong. The magic misfires, is insufficient, or draws unwanted attention. Story advances.

This keeps the core mechanic unchanged and produces three interesting outcome flavors for magic rather than a binary hit/miss.

- **Fits Facet system:** Yes, directly uses existing difficulty and outcome tier framework.
- **MM burden:** Low — scope adjudication is collaborative and explicit before the roll, not after.

---

### Tier 2: Partial Fit (Useful for specific applications)

**C. Verb + Noun (Ars Magica-inspired, simplified)**

Could be used for *learned/scholarly* magic (Mind Facet) versus *intuitive/spiritual* magic (Soul Facet). A scholar mage might construct effects from a small vocabulary (4–5 verbs: create, destroy, shape, sense, compel; 4–5 nouns tied to domains). Intuitive magic uses Domain + Intent only.

This creates meaningful differentiation between magical traditions without requiring full Ars Magica complexity. Worth developing if two distinct magical traditions are wanted in Shattered Origin.

**D. Ritual Framework**

For significant magical workings — anything Major scope or more — a **ritual** structure could apply: requires preparation time, specific materials or conditions, and a collaborative roll (multiple players contributing, or sequential rolls). This gates the most powerful magic behind investment and drama rather than a power ceiling rule.

- Borrowing from Ironsworn's Ritual moves and Ars Magica's lab work
- Highly compatible with the "wonder and discovery" register — rituals are inherently set-piece moments
- Digital layer can track ritual conditions and preparation status

---

### Tier 3: Weaker Fit (Note why and set aside)

**E. Spell Slots / Memorization** — Eliminated by design goals. Maximum reference friction, minimum player agency.

**F. Pure Freeform** — Eliminated by MM burden concern. The digital layer helps but cannot fully replace clear adjudication guidelines.

**G. Class-locked magic** — Eliminated by Facets structure. Magic should be accessible to any character through the Soul Facet, not locked to a class role.

---

## Recommended Design Direction

### Core Principle: Domain + Intent + Scope

Magic in Facets of Origin works through three elements:

1. **Domain** — The thematic territory of your magic. Selected at character creation (Soul Facet), defined broadly. Examples: *fire, beasts, illusion, time, healing, death, storms, shadow, resonance*. Your domain licenses what you can attempt.

2. **Intent** — What you want your magic to do in the fiction, described in natural language. "I want to pull the heat out of the room so their breath fogs and their fingers stiffen." Intent is the player's authorship moment.

3. **Scope** — How ambitious the effect is (Minor/Significant/Major). Determines difficulty. Declared before the roll.

**The roll:** 2d6 + relevant Minor Attribute (Spirit for intuitive magic, Knowledge for scholarly magic, depending on tradition). Use the existing difficulty framework. Outcome tier determines how cleanly the intent resolves.

**Cost:** Built into the three-tier outcome system — no separate resource needed unless the Facet Techniques add one (e.g., a Technique that lets you achieve Major effects without rolling, but costs a Spark).

### Where Techniques Come In

The Mind and Soul Technique trees are the place to encode *specific magical capabilities* — not as spells, but as expansions of what's possible within a domain. For example:

- **Tier 1:** "Your Minor effects in your domain are treated as one difficulty step easier."
- **Tier 2:** "You can shape your domain effects with precision — no unintended collateral within your declared intent."
- **Tier 3:** "Once per session, you may achieve a Major effect in your domain without declaring scope — it simply happens."

This means the Technique tree handles the "getting better at magic" arc without ever specifying individual spells. Players grow in *how* they use their domain, not in *which spells they've unlocked*.

### What This Solves

| Problem | Solution |
|---|---|
| Long spell lists | Eliminated — domain licenses effects; no list required |
| Reference friction | Eliminated — "is this within my domain?" is answered from imagination |
| Player agency | Maximized — player describes the effect; dice and tiers shape the outcome |
| MM burden | Managed — scope declaration before the roll; domain adjudication is a one-time setup |
| Rule of cool | Maximized — any creative application within a domain is valid |
| System coherence | High — uses existing dice, difficulty, and outcome tier framework |
| Advancement arc | Via Technique tree — no separate magic advancement system needed |
| New player accessibility | High — "what does fire do?" is a question anyone can answer |

---

## Open Design Questions

*To be resolved before writing the Soul Facet Technique tree and any magic-related PHB content.*

---

### 1. How Are Domains Acquired?

**Options:**
- **At character creation:** Choose one domain from an open list (or describe your own). This is the simplest approach.
- **Through Soul Facet Techniques:** Domain access is a Tier 1 Technique. Non-Soul characters can never develop a domain. Cleaner separation, but harder to explain in onboarding.
- **Through Backgrounds:** A Background (scholar, hedge witch, temple initiate) grants domain access plus thematic context. Gives magic a narrative origin, not just a mechanical one.
- **Hybrid:** Background provides domain concept; Soul Facet Technique activates it mechanically.

**Design tension:** If domains are free at character creation, every character can be magical. If they're locked behind Techniques, magic-users feel more distinct but the Facet and Background systems need to coordinate.

**Recommendation to discuss:** Hybrid — Background provides the concept and narrative legitimacy ("you were raised in a fire temple"), Soul Facet Tier 1 Technique provides the mechanical activation. Non-Soul characters who want magic face the cross-Facet cost penalty, which is thematically appropriate (magic as a developed art).

---

### 2. How Many Domains Does a Character Have?

**Options:**
- **One domain, always.** Maximum focus; magic users feel genuinely specialized. Prevents "I know every type of magic" generalism.
- **One primary, one secondary (via Techniques).** Allows for interesting hybrid practitioners (a storm-mage who also touches death). Secondary domain is harder to use (one difficulty step harder?).
- **Unlimited within the fiction.** A powerful enough practitioner can attempt anything magical — domain just determines where they're Strong.

**Design tension:** One domain feels limiting in a long campaign (10+ sessions). Unlimited feels like a spell list without the list. One-plus-secondary is a compromise with real mechanical weight.

**Recommendation to discuss:** One domain at Tier 1 Technique, with a second domain available as a Tier 3 Technique (requires significant advancement). Secondary domain always treated as one difficulty step harder. Keeps specialization meaningful while allowing epic-level breadth.

---

### 3. How Are Domains Scoped?

If a player picks "fire" as a domain, what exactly is licensed? Warmth? Combustion? Light? Smoke? Passion and anger (metaphorical fire)?

**Options:**
- **Physical only:** Domain covers literal manifestations (fire = heat, flame, combustion).
- **Physical + thematic:** Domain covers physical manifestations and closely associated themes (fire = heat, flame, transformation, purification, destruction, warmth/comfort).
- **Player-defined at creation:** Player and MM agree on domain scope during character creation. Written down. Used consistently.

**Design tension:** Physical-only is consistent but feels narrow. Player-defined thematic scope creates the most memorable magic but can produce scope creep over time ("fire also means passion, and passion is why my fire magic affects charm rolls").

**Recommendation to discuss:** Physical + closely associated thematic — broad enough for creative play, narrow enough to adjudicate consistently. "Is this within your domain?" should have a clear answer 90% of the time. The 10% gray area is where good moments happen, and the MM's call should default to yes (adventure register: wonder and discovery over restriction).

---

### 4. What Is the Cost Structure?

The three-tier outcome system provides a cost on partial success (7–9). Is that sufficient, or does magic need an additional cost mechanic?

**Arguments for additional cost:**
- Magical effects can be more powerful than mundane actions — Significant and Major effects should feel more expensive than a normal roll
- Cost creates meaningful decision-making about when to use magic versus mundane solutions
- Thematic: magic as a taxing or consequential act fits almost every fictional tradition

**Arguments against:**
- Adding a separate cost system increases cognitive load and contradicts the simplicity goal
- The difficulty framework already prices scope (Major = Very Hard = net -2); extra cost double-penalizes
- Sparks already provide a resource economy; magic can interact with that instead of having its own

**Options:**
- **No additional cost** — the three-tier system is sufficient; Major effects are hard to pull off, and 6- results are their own cost
- **Sparks as magical fuel** — spending Sparks powers magical effects (maybe Significant requires 1 Spark, Major requires 2), with the normal Spark effect also applying. Integrates with existing economy.
- **Fatigue/Condition track** — Major magical effects impose a Condition (Drained, Strained) that the MM can invoke as a complication later. Adds a debt structure. The digital layer tracks it.
- **Ritual requirement for Major effects** — Major scope always requires ritual preparation, never an improvised roll. Hard gates the highest-power effects behind investment.

**Recommendation to discuss:** Sparks as optional fuel for scope upgrades, with ritual requirement as an option for Major effects rather than a hard rule. This integrates magic with the existing economy, keeps the base mechanic simple, and gives players a meaningful choice when the stakes are highest.

---

### 5. How Does Magic Interact With Combat?

The current combat rules (Chapter III.3, not yet written) presumably use the same 2d6 resolution system. Magic in combat needs to be considered:

- Can a fire mage attack in combat with their magic? (Almost certainly yes — this is a core fantasy)
- Does magical combat use the Combat skill (Strength) or a magical skill (Spirit/Knowledge)?
- Is there a distinction between *magical attack* and *magical effect* in combat?

**Design tension:** If magic uses Spirit and Combat uses Strength, magic-focused characters need Soul Facet for offense and Body Facet for defense — which may be the intended design. But a pure soul mage with no Body investment might feel too fragile or unable to participate meaningfully in physical combat.

**Recommendation to discuss:** Magical effects in combat are resolved like any other intent — declare domain, intent, and scope; roll the appropriate attribute; outcome tier determines effect. The Combat skill specifically covers *fighting technique*, not damage output — a mage firing flame at an opponent rolls Spirit (or Knowledge), not Combat. The opponent's evasion informs the difficulty the MM sets, exactly as with physical attacks. This keeps magic in combat consistent with the rest of the system and means magic users don't need a separate ruleset.

---

### 6. Magical Traditions and the Setting

Shattered Origin presumably has some internal logic for why magic exists and what forms it takes. The domain system is setting-agnostic — but the specific domains available, and whether there are distinct magical *traditions* (arcane vs. divine vs. natural vs. innate), has both mechanical and narrative implications.

**Design tension:** Setting-specific traditions create flavor and narrative hooks (a character trained in a specific tradition has a backstory baked in). But over-specifying traditions risks recreating the "class = magic type" problem in disguise.

**Recommendation:** Define 2–3 broad magical traditions in Shattered Origin at the setting level (e.g., Resonance — the study of fundamental harmonic forces in the world; Channeling — drawing on spiritual entities or divine power; Wild — magic that flows from living things and the natural world). Each tradition suggests domains and offers a narrative hook, but does not restrict which domains a character can access — that's determined by character history and the domain system. Traditions are flavor, not ceilings.

---

## Summary and Next Steps

**Recommended design:**
1. Domain + Intent + Scope model as the core magic mechanic
2. Domains acquired via Background (narrative origin) + Soul Facet Tier 1 Technique (mechanical activation)
3. One domain at creation; second domain as Tier 3 Technique
4. Scope (Minor/Significant/Major) maps to difficulty (Standard/Hard/Very Hard)
5. Sparks as optional scope fuel; ritual as an option for Major effects
6. Magic in combat uses Spirit or Knowledge (domain-appropriate), not Combat
7. Soul Facet Technique tree encodes magical growth without spell lists

**Before writing Magic-specific PHB content:**
- Resolve open questions 1–4 above (domain acquisition, count, scope, cost)
- Write the Soul Facet skill list (the blocker for all Soul-adjacent content)
- Write the Soul Facet Technique tree (magic growth arc lives here)
- Coordinate with Chapter III.3 (combat) on how magical actions resolve in combat
- Design 2–3 Shattered Origin magical traditions as setting flavor (not mechanical ceilings)

---

## Sources

**Design theory:**
Sanderson (2007–2013), Laws of Magic (Sanderson's blog/lectures); Baker (2010), *Apocalypse World*; Harper (2017), *Blades in the Dark*; Hicks (2016), *13th Age*; Tweet, Cook, Williams (2014), *D&D 5e Player's Handbook*; Rein-Hagen (1993), *Mage: The Ascension*; Link, Junge, van Belle (1987), *Ars Magica*; Cypher System (Monte Cook Games); *Ironsworn* (Shawn Tomkin, 2019).

**Psychology:**
Ryan & Deci (2000), Self-Determination Theory; Csikszentmihalyi (1990), Flow; Green & Brock (2000), narrative transportation; Sweller (1988), cognitive load theory; Lazzaro (2004), 4 Keys to Fun.

**Community research:**
r/rpg, r/worldbuilding, r/magicbuilding threads on freeform vs. structured magic systems; Dungeon World community discussion on magic without spell lists; Ironsworn community on ritual mechanics; the Alexandrian (Justin Alexander) on scenario design and magic adjudication.

*Note: Live verification recommended for post-August 2025 releases and community discussion.*
