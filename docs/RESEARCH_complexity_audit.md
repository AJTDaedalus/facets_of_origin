# RESEARCH: Complexity Audit. Does Being Different Carry Its Weight?

**Date:** 2026-09-25
**Tier:** Brain question, run on Opus. The rulings it asks for are the owner's.
**Question (owner):** *"Review our system against industry best practices and our goals of a simplified tabletop RPG with flexibility. I feel like we've made something nearly as complicated just to be 'different'. Review it from a lens of if what we're doing differently from a generic open d20 system carries its weight."* Follow-up: *"In particular look back at D&D historically. Earlier versions before 3.0 were much more roleplay heavy without the huge burden of rules, but still had HP, spells, etc."*

**What I read:** Quick Start; III.1, III.3 (rules body), II.3, II.4, IV.1 and II.2 in full or in their rules sections; the DECISIONS index; `RESEARCH_fun_audit_2026-09.md` §1–7; the `advancement` block of `facet.yaml`. The Technique trees (II.4a/b/c) I only counted, not audited.

**Copyright note:** pre-3e D&D is proprietary. Its ideas are discussed here as ideas, and none of its text or tables are reproduced. The mechanics the OSR has re-published under open licences (Old-School Essentials/OGL, Knave CC BY, Cairn CC BY-SA, Into the Odd's open derivatives) can be adopted *as concepts*. Where we borrow a concept it should be re-expressed in our own words.

---

## Verdict up front

**Your instinct is half right, and the half that's right is important.**

- **The core is simpler than d20 and earns every bit of its difference.** One 2d6 roll with three outcomes, the extra-die mechanic reused everywhere (Spark, Press, Borrowed Trouble), NPCs never rolling, Mooks dropping to one hit, magic with no spell list. None of that exists for its own sake. Each piece does something d20 does worse.
- **Around that core we've added about 85 player-facing rules, and roughly half of them are ours alone.** Nobody arrives already knowing them. Combat is the worst offender. It's the longest chapter in the PHB, at 10,856 words (more than Core Resolution and Adventuring put together). The last audit found it gives about two real decisions per exchange, so it has the complexity of a tactical game without the depth of one.
- **Old-school D&D is the right yardstick, and it points somewhere specific.** Early D&D had HP, spells, AC, classes and levels and still stayed light, because each of those was *one simple number or list*, and all the complexity lived in the referee's judgment and tables. We replaced several single numbers (HP, level, a spell count) with small interlocking systems: Endurance + reactions + three Condition tiers + an armor budget, and points → marks → ranks → Facet levels → Techniques → Majors. The replacements do cost less arithmetic. They also ask the player to understand much more. The digital layer can take over the bookkeeping. It can't do the understanding for them.

**Recommendation:** keep the core and the magic idea, and cut the novel machinery around them back toward old-school plainness. Order: **advancement → combat → attributes → magic's limit layer.** Then play it with humans *before* adding anything back. The fun audit's R1 still stands, and everything below will be easier to judge after one real table has played the lighter version.

---

## 1. The yardstick: why early D&D felt light

Early D&D's player-facing load was small. From the player's side, the basic sets came down to six ability scores (most giving no modifier at all), a class, a level, an XP total, HP, AC, a to-hit number, a damage die, a handful of save categories, and a per-day spell count off a list. Combat was side initiative, one roll to hit, one subtraction, and a morale check the referee made. Everything else was **"rulings, not rules"**: the referee decided, often by consulting a table.

Four features made that work, and they're the lessons worth taking:

1. **Primitives were single numbers.** HP is one number going down. Level is one number going up. "Three spells per day" is a count. A number is cheap to learn even when the arithmetic is tedious, and here the app does the arithmetic anyway.
2. **The complexity sat on the referee's side, as procedure.** Reaction rolls, morale, wandering-monster checks and random tables were tools for the referee, and players never had to learn them. That's where old-school depth lived.
3. **The reward loop pointed at what the game was about.** Treasure-for-XP pushed play toward exploration, risk-weighing and avoiding fights. The loop and the goal lined up.
4. **Familiarity was free.** Even then, "roll high, subtract HP" needed no teaching. Today that's even more true: most of our likely audience already knows d20 conventions. **Every rule we invent has to pay a novelty tax** that a familiar rule doesn't.

And the honest counterweight: early D&D wasn't uniformly light. The advanced line carried weapon-vs-armor tables, weapon speed, grappling and a to-hit matrix; 2e added kits and non-weapon proficiencies. The light experience came from the basic line **and from tables quietly ignoring rules**. So the lesson isn't "copy old D&D." It's this: **a few plain primitives, lots of referee procedure, and a reward loop aimed at the goal.**

Measured against those four:

| Lesson | Facets of Origin | Grade |
|---|---|---|
| Primitives are single numbers | Resolve (enemy HP) and Sparks, yes. Player durability, advancement and the magic limit are small systems | **Weak** |
| Complexity on the referee side | NPCs never roll; Trouble Table; Threat Clocks; Encounter Recipes; conduct fields: **good**. But in combat, the most rules sit on the *player* side (postures, four reactions, riders, Press, armor budget) | **Mixed** |
| Reward loop aimed at the goal | Sparks for fiction: **good**. Marks for *skills you used*: this rewards calling for rolls, which contradicts III.1's "When Not to Roll" and its "fewer rolls per session" design note | **Mixed** |
| Familiar where it costs nothing | Resolve is HP by another name (fine). Otherwise about 70 glossary terms, most of them coined | **Weak** |

---

## 2. The inventory

I counted the distinct rules a *player* has to hold to play a character from creation through a fight, a spell and a level-up. Techniques aren't counted, because each player takes on only their own (see §4, *opt-in complexity*). The counts are mine and approximate; the list behind them is in the appendix.

| Subsystem | Rules a player must hold | Of which novel (not in d20 or PbtA) |
|---|---|---|
| Core resolution (III.1) | ~12 | ~4 (difficulty order of operations, Borrowed Trouble, natural-2 auto-confirm, Graceful Fail) |
| Character creation | ~12 | ~5 (9 Minor + 3 derived Major attributes, bracket table, pre-marked secondary skill, Endurance formula) |
| Advancement (II.4) | ~16 | ~12 |
| Combat (III.3) | ~27 | ~20 |
| Magic (II.3) | ~18 | ~14 |
| **Total** | **~85** | **~55** |

A player of the old basic game held perhaps **15–20**. A 5e player's core (not counting class features and spells) is perhaps **35–40**, and most of it is already familiar. **The "one rule" game asks for more rules than the core of the d20 system it's pushing back against, and most of them are brand new.** That's the whole of the owner's worry, made measurable.

Two symptoms that the load is already too big for the people who wrote it:

- **The book contradicts itself on advancement.** II.4 §*Major Advancement* still says a finished Facet is "15 total skill rank advances". The same chapter's §*Facet Levels* and `facet.yaml` (`facet_level_threshold: 3`) say 9. The note survived D16 because nobody can hold the whole chain in their head. (Fix: one line. See §6.)
- **Patch rules.** "Aggressive's surcharge applies to the *first* reaction only." "Armor and partial reactions don't stack, *and the charge isn't spent* when the reaction did the work." "At 0 Endurance only Absorb is available, *absolutely*, regardless of Posture." "Easy tags override, then *at most one* character step, then Support's step." Each patch closes a hole opened by two other rules meeting. A rule that needs a patch to live alongside its neighbours is usually a rule too many.

There's also a cost the players never see. Under this repo's sync rule, every mechanic lives in the PHB body, every quick ref that touches it, the MM Manual, `facet.yaml`, the engine and the tests. **Each rule costs about six artifacts**, and the 1,700-test suite is partly a measure of how many rules there are.

---

## 3. The ledger: each divergence, weighed

**Keep:** the difference pays for itself. **Simplify:** keep the idea, drop the machinery. **Cut:** remove it. **Revert:** use the familiar convention.

### 3.1 Core resolution

| Divergence from d20 | What it buys | Verdict |
|---|---|---|
| 2d6 + mod, three tiers instead of d20 vs DC | Modifiers matter on a bell curve; the 7–9 band is the story engine; one table for everything | **Keep.** This is the game |
| Four named difficulties instead of numeric DCs | Faster calls, stated aloud | **Keep** |
| Sparks = +1d6 drop lowest | Like advantage, but earned by the table; one mechanic reused by Press and Borrowed Trouble | **Keep.** Reuse is exactly right |
| Peer call, act-break nomination, Graceful Fail | Fellowship; turns failure into currency | **Keep** |
| Borrowed Trouble | Player-chosen risk; spreads invention around the table | **Keep** |
| Natural 12 / natural 2 | Memorable peaks | **Keep.** Cheap |
| Difficulty order of operations (Easy tag → one character step → Support step) | Exists only because there are too many sources of "Easy" | **Simplify.** It goes away once Position and Support's step option are cut (§3.3) |
| Saves on the three Major attributes | Cleaner than the old five categories | **Keep.** It becomes the *only* use of attributes once §3.2 lands |

### 3.2 Character

| Divergence | What it buys | Verdict |
|---|---|---|
| **9 Minor attributes (1–3) + 3 derived Majors via a bracket table** | Flavour granularity (a strong but clumsy fighter) | **Simplify.** Twelve numbers where the old game had six and PbtA has five. Minors only ever give −1/0/+1, which is noise next to skills. Four of them govern one skill each (the fun audit found Luck is dead weight on a Body sheet). And every roll is two lookups. **Candidate:** three attributes, Body/Mind/Soul, rated −1 to +2. Each skill uses its Facet's attribute. The bracket table, the weapon-category→attribute table and the "which attribute?" question all disappear; skills carry the specificity (Combat vs Finesse *is* strong vs deft). Fallback if familiarity matters more than economy: the standard six |
| Three Facets instead of classes | Broad archetypes plus Technique trees | **Keep.** It's a light class system under a new name, and that's fine |
| Background with Specialty | Story-first capability; Specialty is a great no-roll lever | **Keep** |
| Secondary skill "at Novice with 1 mark already" | A head start on one skill | **Simplify.** Two concepts (mark and threshold) just to explain a head start. Goes away under §3.4 |
| Lineage defaulting to Human | Keeps onboarding small | **Keep** |

### 3.3 Combat, where the ratio is worst

What earns its keep, so it's protected: **exchanges without initiative, NPCs never rolling, Mooks dropping to one hit, Resolve as enemy HP, Press competing with defence for Endurance, Intercept, the death choice, morale lines.** Those give the fight its speed. **None of the speed comes from postures, riders or the armor budget.** Old-school fights were fast for the same reason ours are: one roll per action, very little bookkeeping per hit.

| Divergence | What it buys | Verdict |
|---|---|---|
| **Four Postures, declared blind** (slips of paper at a physical table; a token for Aggressive's first-reaction surcharge; a separate enemy-posture table for reaction difficulty) | Promised as "half the tactical game". Found to be a script keyed to your own Endurance bar (fun audit §4.2); Aggressive and Measured give the same Broken rate across 1,000 sims | **Cut.** Keep Withdrawn as an *action*: "Catch your breath: no offence this exchange, reactions free, recover 2." Aggressive's job is already done by Press. An enemy's stance becomes a line of conduct the MM states ("hits hard: reactions against it are Hard"), which is referee-side procedure, the old-school way |
| Dodge vs Parry | Flavour; the choice is really a lookup of whichever is higher | **Simplify.** One reaction, **Defend**: roll your better of Dex or weapon + Combat. The fiction still says whether it was a dodge or a parry |
| Open **and** Position riders, **and** Maneuver, **and** Support's two options | Enough "Easy" sources that III.1 needs an order-of-operations rule | **Simplify.** One tag, **Open**. A 10+ Strike *or* a 7+ Maneuver opens the target. That also fixes the audit's finding that Strike dominates Maneuver, because Maneuver now opens on a 7. Support = +1d6 drop lowest, the same die as everything else |
| Three Tier-1 Conditions (Winded / Off-Balance / Shaken), cleared each exchange | Texture | **Simplify** to one ("Winded: −1 on your next roll"), or keep only Shaken for its fiction. Off-Balance exists to tax Endurance, which the Posture cut already reduces |
| **Armor as a per-scene downgrade budget, plus no-stack with partial reactions, plus charge-not-spent, plus a different rule for enemy armor** | Avoids per-hit subtraction | **Simplify.** Three rules and an exception to avoid one subtraction. See §5 for two candidate replacements |
| Conditions for PCs and Resolve for enemies | The MM tracks one number per enemy | **Keep the asymmetry.** It's the old-school "monsters are simple" instinct. But see §5: the PC side is where HP would earn its place |
| Magical Strike spends a readied intent (D25) | Stops free magic from outclassing swords | **Keep the principle**, carried by the simpler limit in §3.5 |

Net effect: combat goes from ~27 player rules to ~14 and keeps every mechanic the fun audit called a peak.

### 3.4 Advancement: five layers where the old game had one

The chain today: **4 points per session → spend only on skills you used (1 training-point exception, 2 bankable, cross-Facet costs double) → marks (3/5/8 per rank) → ranks (capped: 3 beyond Practiced, 1 Master, slot claimed on commitment) → every 3 advances a Facet level → a Technique per level (branch/tier prerequisites; magic Backgrounds spend the first on formalization; Lineage gifts are an exception) → every 3 Facet levels a Major Advancement → career advances as a separate running total.**

The old game had XP → level. The D16 caps are the one piece of this that clearly earns its keep: two Body characters end a campaign with different sheets.

**Candidate: Advances, one layer.**
- At the end of each session every PC gains **one Advance** (the MM may give a second after a milestone).
- An Advance raises one skill one rank, within the D16 caps. A cross-Facet skill takes two Advances.
- **Every third Advance in a Facet** also grants a Technique from that tree. This is the Facet level, unchanged.
- The Advance count *is* the career-advances clock. A Major Advancement arrives at 9 total, as now.

Deleted: points, marks, per-rank mark costs, banking, the training point, the "used this session" rule, pre-marked secondary skills, and the separate career-advances counter. Pace is almost unchanged: a finished Facet is 8 sessions after the Background's free advance, against today's "roughly ten". It does lose the rising cost of Master. If that matters, make Master cost two Advances. That's one rule, not a table.

The reason this is more than tidying: **use-based marks reward rolling**, and III.1 asks the MM to roll less. The game's own reward loop is working against its own best advice. Per-session Advances stop paying for dice and let the reflection scene be what makes growth real.

### 3.5 Magic: keep the idea, cut the accretion

**Domain + Intent + Scope with no spell list is the strongest case in the whole system for being different.** In every edition of d20 the spell list is the single largest body of player-facing rules, and we replaced it with three questions. Keep.

The trouble is how much has accreted around it in two weeks (D17 → D23 → D25): five purposes, three readied intents per session, off-purpose costs a Spark, spent whatever the roll, refresh on an MM-called full rest, the full-form judgment, the chained-Minor rule, a 3×3 domain-type table, two special cases for "reach" Sparks, pre-formalization Minor-only, the Lineage-gift exception, second domain, cross-Facet domain, and one Prismatic via Ascendant.

| Piece | Verdict |
|---|---|
| Domain, Intent, Scope; the full-form rule ("how much did you ask of the world?"); the chained-Minor ruling | **Keep.** These are rulings, and rulings are cheap. Fold the chained-Minor note into the full-form paragraph |
| **Readied intents by purpose** | **Simplify to a count.** "Three full-form workings per full rest; more cost a Spark each." That's the old per-day limit in its simplest form, a single number. The purpose guess is meant to be the fun ("a story about preparation"). In practice it punishes exactly the new player who can't yet predict a session, and it adds a planning step plus the off-purpose rule. If the owner wants it kept, make purposes an optional flavour choice with no mechanical lock |
| 3×3 Domain type × Scope table | **Restate as a rule, same maths.** "Scope sets the base: Minor Easy, Significant Standard, Major Hard. Standard domains are one step harder, Prismatic two (never past Very Hard)." One sentence replaces a table |
| Reach Sparks (Significant before the Technique; Focused eases Major) | **Cut both.** The first is already covered by the general rule "no intent available? pay a Spark". The second is a niche perk that a Focused-domain Technique could carry as opt-in |
| Pre-formalization Minor-only; formalization spending the first Technique pick | **Keep.** Legible in the fiction, and it's the arc the magic Backgrounds promise |
| Second domain, cross-Facet domain, one Prismatic | **Keep, but as Technique text only.** It's high-level and opt-in, and doesn't belong in the chapter every caster reads on day one |

---

## 4. Best practices the cuts follow

1. **Opt-in complexity.** Complexity a player *chooses* (a Technique, a domain, a Pinnacle) is fine, because only the player who wants it pays for it. Complexity in the core is paid by every player at every table. **Move exceptions out of the core and into Techniques.** Our Technique trees, with their `Normal:` lines, are already the right container. The core has been carrying exceptions that belong there.
2. **Complexity goes on the referee's side as procedure.** A table the MM consults (Trouble Table, social 7–9, conduct lines, Encounter Recipes) costs the players nothing. That's where the fun audit said the system is short, and it's where the words saved here should go.
3. **One mechanic, reused.** "+1d6, drop the lowest" and "Easy" are the game's two verbs. Every new source of a bonus should use one of them, and none should need an order-of-operations rule.
4. **Pay the novelty tax only for what's distinctive.** Where a familiar convention does the job, use it: HP-like durability, a spell count, one level-like number. Spend novelty on the three things nobody else does this way: the three-tier roll with the table's economy around it, spell-list-free magic, and NPCs who never roll.
5. **A reward loop pointed at the goal.** Sparks for fiction are good. Advancement should stop paying for dice (§3.4).
6. **Cut first, playtest, then add back.** Adding a rule a real table asks for is cheap. Removing one that players, tests and six artifacts depend on is expensive. And nothing past 2026-08-02 has been played by a human.

---

## 5. The HP question, reopened because the owner asked

D26 declined hit points "for now". The follow-up asks why early D&D could carry HP and stay light. The answer: **HP was never the heavy part.** HP is one number. What we built to avoid it on the PC side is Endurance, four reactions with costs, posture cost modifiers, three Condition tiers with five named Conditions, the same-Tier-2 escalation, and an armor budget with a no-stack rule. That's about ten rules standing in for one.

The OSR's own answer to "HP is boring" is worth taking as a *concept*: HP is not wounds but **grit, the capacity to avoid real harm**. It refills after a breather, and only once it's gone do hits become lasting injuries. That's close to what our Endurance Pool already claims to be. Two candidates, both needing a simulation pass (the sim must drive `combat.py`, per the sync rule):

**A. Conservative (keeps D26).** Apply §3.3 as written: Postures cut, Defend merged, one rider, Support simplified, Tier 1 collapsed. For armor, let armor and a partial reaction stack, with the budget halved (Light 1, Heavy 2), which deletes the no-stack and charge-not-spent rules. Endurance stays as the tempo pool.

**B. Grit (revisits D26).** Endurance *becomes* the PC's durability.
- An enemy hit costs Endurance: Mook 1, Named/Boss 2.
- **Defend** is free: 10+ takes nothing, 7–9 takes 1 less, 6− takes it all. Intercept means you Defend for someone else.
- **Armor** takes 1 off every hit (heavy: plus one free re-roll of Defend per scene, or similar. A knob to tune, not a design).
- **Press** still spends Endurance, so pushing hard makes you easier to break. That's the tension the fun audit praised, now with real stakes.
- At 0 Endurance, the next hit is a **Condition** (the current Tier 2 list); a second of the same kind, or a hit while Conditioned and empty, is **Broken**. The death choice is unchanged.
- *Catch your breath* restores 2, and a scene's end refills it.

B deletes reaction costs, the armor budget and its exceptions, posture cost modifiers and Tier-1 Conditions. It turns "Conditions replace HP" into "Conditions are what happens after HP", which is the plain version of the book's own promise that "an empty pool is not bleeding out". Its risks: armor at −1 may make Mooks toothless against a heavily armored PC (arguably very old-school), and Endurance becomes a number people will call HP. **My view is that B carries its weight better than the current model.** It's the owner's call, because it reverses a ruling made five days ago.

---

## 6. Recommended sequence

| # | Action | Tier | Size |
|---|---|---|---|
| 0 | Fix the stale "15 total skill rank advances" line in II.4 §*Major Advancement* (should be 9) | Worker | 1 line |
| 1 | **Owner rulings** on: Advances (§3.4); the combat cuts (§3.3); A vs B (§5); three attributes vs nine (§3.2); a count vs purposes for readied intents (§3.5) | Owner | one sitting |
| 2 | Write `BRIEF_lean_core.md` from those rulings: goals, non-goals, and a **rule budget** (target ≤ 50 player-facing rules; every future addition names what it replaces) | Brain | small |
| 3 | Planner: DESIGN/TASKS. Sim first for combat (A/B against the Recipe Table targets), then PHB → Quick Start/MM5 → `facet.yaml` → engine → tests, per the sync rule | Planner → Worker | large; attributes are the biggest blast radius (II.2, every `.fof`, Bestiary attack modifiers) |
| 4 | **Human playtest of the lean core** (fun audit R1) before any rule is added back | Owner | one session |

If only one thing gets done: **§3.4 (Advances) and the Posture cut.** Together they remove about 20 rules, reverse the incentive to roll, and cost the least in canon churn.

---

## Appendix: the rule count

**Core (12):** 2d6+mod · three tiers · four difficulties · difficulty order of operations · natural 12 · natural 2 · Spark spend · Spark earning (MM/peer/act-break) · Graceful Fail · Borrowed Trouble · saving throws · contested and group rolls.

**Character (12):** three Facets · nine Minor attributes (1–3) · 18-point buy · derived Majors and bracket table · 15 skills with governing attributes · four ranks · Background's five elements · pre-marked secondary skill · Specialty · Lineage · Endurance formula · three Sparks per session.

**Advancement (16):** 4 points/session · used-skill rule · cross-Facet double cost · banking 2 · training point · marks 3/5/8 · beyond-Practiced/Master caps · slot-on-commitment · Facet level per 3 advances · Technique per level with branch/tier prerequisites · formalization spends the first pick · Lineage-gift exception · Major per 3 levels · Pinnacle · reflection scenes · career advances.

**Combat (27):** five-step exchange · blind posture declaration · four postures · Aggressive first-reaction surcharge · Withdrawn recovery · uncontested exchange · Strike attribute by weapon category · skill default · Resolve 2/1 · Open · Position · Press · Maneuver tiers · Support's two options and no-stack · four reactions and costs · 0-Endurance absolute rule · Intercept limits · three Tier-1 Conditions · two Tier-2 Conditions · same-Tier-2 → Broken · Broken · armor budget 2/4 · armor/reaction no-stack · charge-not-spent · incoming tier by enemy type · enemy posture → reaction difficulty · PvP Condition table.

**Magic (18):** domain · intent · five purposes · three scopes · full-form rule · chained-Minor rule · domain type × scope table · two traditions (attribute + skill) · three readied intents · refresh on full rest · off-purpose Spark · spent whatever the roll · pre-formalization Minor-only · reach Spark (early Significant) · reach Spark (Focused Major) · second domain · cross-Facet domain · one Prismatic via Ascendant.

---

## 7. The clean-sheet view (owner follow-up, 2026-09-25)

**Question:** *"If I was entirely unattached to what we have so far, and wanted something simple like earlier D&D with flexibility and MM-driven variety, how would this change our view?"*

### 7.1 What changes

§1–6 ask *which of our rules survive*. A clean sheet asks *what is the smallest plain chassis, and which of our few genuinely distinctive ideas get bolted onto it*. The answer moves a long way:

| Question | Trim view (§3–5) | Clean-sheet view |
|---|---|---|
| Rule budget | ≤ 50 player rules | **≈ 25**: one page per side of a sheet |
| Where variety comes from | Player options (Techniques, postures, riders) | **The MM's side**: tables, monster gimmicks, loot, procedures, and the app rolls them. That's the old-school source of variety |
| Durability | Keep the Conditions/Resolve asymmetry, or "grit" | **HP for everyone.** PCs and monsters use the same number. HP is grit, refilled by rest; injuries only once it's gone |
| Damage | No damage numbers | **Weapon damage dice.** One subtraction, familiar, and it serves the Butt-Kicker the fun audit found underserved |
| Skills | 15 skills × 4 ranks with D16 caps | **No skill list.** Your Background says what you're good at (+1); your Specialty means no roll at all. Old D&D had no general skills and didn't miss them |
| Character build | Facets + Technique trees (~69) | **Facet = class.** Three short lists of ~8 abilities each; pick one per level |
| Advancement | One Advance per session | **XP → level** (1–10). Level gives HP, an ability, and every third level +1 stat. XP is paid for discovery and goals, not fights or rolls |
| Combat | Exchanges trimmed to ~14 rules | **One roll per player per exchange.** Your attack roll also settles whether you get hit (the PbtA "7–9, you both land" pattern). No reactions, no Endurance, no postures. NPCs still never roll |
| Magic | Domain + Intent + Scope; count-based limit | **Unchanged in spirit**: Minor free; full workings a small per-rest count; 7–9 picks a cost |
| Loot | None | **Yes.** Treasure and magic items are the cheapest carry-forward reward and pure MM variety |

### 7.2 The honest problem: this has been built

A clean-sheet "early D&D feel on a 2d6 three-tier engine" lands very close to **Dungeon World** (and its descendants: Homebrew World, Freebooters on the Frontier), which is the best-known existing answer to exactly this brief. Nearby OSR games (Knave, Cairn, The Black Hack, Old-School Essentials) cover the plain-chassis half. Several are openly licensed (Dungeon World CC BY 3.0, Knave 1e CC BY 4.0, Cairn CC BY-SA 4.0, The Black Hack and OSE via OGL; **verify each licence before borrowing wording**). So building on them is legal, and borrowing *concepts* is always fine.

That changes the strategic question. If the rules converge on an existing open game, **the rules can't be the project's reason to exist.** Our differentiators would be:

1. **The digital toolset as the MM's variety engine.** Tables, generators, monster gimmicks, reaction and morale rolls, clocks, all one click away. This is where old-school depth lived, and nobody has made it frictionless.
2. **Spell-list-free domain magic.** Dungeon World kept class spell lists; we wouldn't.
3. **The table economy**: Sparks with peer awards, the Graceful Fail, Borrowed Trouble. None of the old-school games has it.
4. **Shattered Origin**, the Facet/module format, and the open-source, homebrew-first stance.

Those four are also exactly what survives from the current build. Most of what gets thrown away is the machinery §2 already called novel-without-weight.

### 7.3 Sketch: "Lean Facets" (for comparison, not a spec)

- **Stats:** Body, Mind, Soul, spread +2 / +1 / 0.
- **Facet (class):** Body (warriors, scouts), Mind (scholars; Thaumaturgy), Soul (speakers, the luck-touched; Invocation). Each sets the HP die and offers ~8 abilities.
- **Background:** two freeform lines; +1 when it covers the task. **Specialty:** no roll.
- **Roll:** 2d6 + stat (+1 background) ± difficulty, with three tiers. Naturals, Sparks, Borrowed Trouble, Graceful Fail as now.
- **Fight:** everyone says what they do, then players roll. Attack 10+: deal your weapon die. 7–9: deal it, and the enemy's blow lands too. 6−: it lands, and the MM makes a move. When something happens *to* you, roll the stat: 10+ avoid, 7–9 take half, 6− take it all. Armor subtracts 1–2. At 0 HP you take an Injury (the current Condition list); a second makes you Broken, and the death choice is kept.
- **Monsters:** HP, damage, armor, **one special thing**, and a morale number (the MM rolls 2d6 when they're losing).
- **Magic:** as now, with the limit as a count per rest that rises with level.
- **Advancement:** end-of-session XP questions (*did we discover something? pursue a goal? change the world?*) → level thresholds.
- **MM side:** reaction roll, morale, Trouble Table, omens, rumors, loot tables, Threat Clocks, all in the app.

That comes to about 25 player-facing rules.

### 7.4 What it costs, and how to decide

A true clean sheet discards most of the PHB's rules text (~55k words), `facet.yaml`, the engine and most of the 1,700 tests, and the stat layers of the Bestiary and Oraga Night. The prose, vignettes, characters, setting, module structure, app shell and MM advice mostly survive.

**Recommendation:** decide this *before* starting the §6 trim, because trimming a system you may replace is wasted work. The cheap way to decide is the one the fun audit already asked for: **write Lean Facets on two pages (a day's work) and put it and the current game in front of the same humans.** Two pages of rules and one evening will settle more than another audit.
