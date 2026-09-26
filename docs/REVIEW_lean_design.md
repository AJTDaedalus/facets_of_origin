# REVIEW: Lean Facets v1.0, an adversarial design review

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` (HEAD `ec370f7`) · **Baseline:** tag `pre-lean-facets`
**Brief:** judge whether the overhaul meets the owner's goals: *"something simple like earlier D&D with flexibility and MM-driven variety"*, *"a complete overhaul is fine if it makes it more fun"*, Facets as Morrowind-style broad parents with custom classes, and enemies rolling their attacks. Be adversarial and cite everything.

**Read in full:** BRIEF, DESIGN, `facet.yaml`, Quick Start, II.1, II.3, II.4, III.1, III.2, III.3, MM1, MM5, `RESEARCH_lean_fun_evidence.md` §4–8, and `RESEARCH_complexity_audit.md` §2, §7 and its appendix.
**Read in part:** II.4a/b/c (talent entries), IV.1, IV.2, MM3 *Retainers*, `tables.yaml` (magic, wound and fight tables), `combat.py`, `magic.py`, `character.py`, `combat_sim.py`, and the WebSocket handler list.

---

## 0. Method, and how far to trust the numbers

Every number below comes from the real engine (`app.game.combat`, `app.game.magic`, `app.game.character`), driven either by `python3 -m tools.combat_sim` or by small policy-only drivers that import `tools.combat_sim` and pass it other parties. The drivers make no rule decisions. They live in this session's scratchpad (`sim2.py`, `sim3.py`, `solo.py`, `perpc.py`, `guard.py`, `study.py`, `dmg.py`), and each is a 10–30 line wrapper around `cs.build_party` and `cs.run_fight`. Trials are 600–1,000 per cell.

**The simulator's policy is thin, and every limit below understates the gaps this review reports:**
- It never applies a knack, so real fighters roll +1 better than simulated ones: *Soldiering* "fits most fights" (III.3:29).
- It never uses Defend, Help, Sparks or Borrowed Trouble.
- It picks enemy targets at random, so it ignores telegraphs and "reach".
- Casters cast a Significant signature every exchange.
- Non-casters always take +1d6 on a 10+.
- **It adds a rule the book doesn't have.** A caster who rolls 7–9 is exposed (`combat_sim.py:175-176`). This is noted as its own finding (M5).

Baseline ladder, `python3 -m tools.combat_sim --ladder --trials 1000`. The party is the default Warrior, Scout, Thaumaturge and Invoker:

| Level | 4 Mooks | 3 Standard + 2 Mooks | Boss |
|---|---|---|---|
| 1 | 100% win, 1.4 exch, 0% any PC down | 100%, 2.2 exch, 4% down | 99.5%, 3.0 exch, 51% down |
| 5 | 100%, 1.2, 0% | 100%, 2.5, 2% | 100%, 4.6, 45% |
| 10 | 100%, 1.2, 0% | 100%, 2.8, 2% | 100%, 6.0, 50% |

The ladder looks healthy. **It is healthy only for this party.** The findings below are about what happens off it.

---

## CRITICAL

### C1. Facets aren't balanced in the fight, and the gap widens with level. Half the presets can't fight.

**Claim.** Body characters are close to invulnerable against same-level foes. Mind characters, and the Mind and Soul presets that don't cast, lose to *one* Standard foe of their own level, and they lose more often as they level up. The Quick Start's promise that the twelve presets "are balanced against each other" is false.

**Evidence.**
- Quick_Start.md:17: *"They are ready-made, they are balanced against each other, and every one of them is a fine first character."*
- II.1:5: *"None of those three can make a character stronger than another at the same level."*

Solo test: each preset alone against one Standard foe of its own level, morale off (`solo.py`, 600 trials each):

| Level | Warrior | Scout | Guardian | Brawler | Thaum | Investigator | Physician | Tactician | Invoker | Speaker | Wanderer | Captain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 100% | 99% | 100% | 93% | 60% | 21% | 21% | 73% | 81% | 56% | 56% | 90% |
| 5 | 100% | 100% | 100% | 98% | 31% | 7% | 7% | 35% | 62% | 31% | 31% | 64% |
| 10 | 100% | 100% | 100% | 99% | **7%** | **0%** | **0%** | 38% | 45% | 25% | 25% | 67% |

Single-Facet parties against the "standard" ladder fight (3 Standard + 2 Mooks), morale off (`sim2.py`):

| Party | L1 win / any PC down | L5 | L10 |
|---|---|---|---|
| All Body (the four Body presets) | 100% / 1% | 100% / 0% | 100% / 0% |
| All Soul | 99% / 31% | 100% / 29% | 100% / 27% |
| All Mind | **73% / 77%** | **69% / 82%** | **61% / 90%** |

Damage per action against a Standard foe of the same level (armor 1, no knack, `dmg.py`):

| Level | Warrior | Scout | Brawler | Thaum (signature, Easy) | Investigator / Physician | Speaker / Wanderer |
|---|---|---|---|---|---|---|
| 1 | 5.2 | 5.3 | 3.6 | 3.4 | 2.0 | 2.8 |
| 10 | 8.9 | 11.5 | 7.0 | 6.4 | 3.7 | 6.0 |

Against a Boss, the Thaumaturge drops in 30–42% of fights at every level from 1 to 10, while the Warrior drops in 0–2% (`perpc.py`).

**Mechanism.** The Mind Facet stacks four penalties:
- the smallest grit die;
- Body +0 on HP;
- attacks rolled on Body (III.3:29, *"An attack is 2d6 + Body"*);
- light armor or none on all four of its presets.

Its "most flexible tools" (II.4:25) are exploration and support talents that do nothing to a foe's HP. On top of that, monster damage grows +1 per level while a Mind character's HP grows +4 per level. Monster HP grows +3 per level (×5 for a Boss) while caster damage grows only through the +1/+2/+3 damage bonus. The distance between the Facets therefore widens every level.

**Why it matters.** Most of Laws' types feel this at the table:
- A Casual Gamer who takes the Physician or the Speaker from the Quick Start's "balanced" table spends every fight rolling 2d6+0 with a dagger for 2 damage.
- They drop first, then sit out the rest of the fight.
- The death choice keeps them alive, but it can't make the fight fun for them.

This is the one outcome the fun evidence warned about in §7 ("a named preset… niche protection").

**Fix.**
- Give every Facet a way to attack with its own stat. Mind could attack with Mind using a *Studied* attack, and Soul with Soul using a *Rallying* strike. Alternatively, let the class knack choose the attack stat.
- Narrow the grit dice to d10 / d8 / d8, or give every character a flat +4 HP at level 1.
- Give each non-casting Mind or Soul preset one talent that works inside a fight, for example *Physician*: "once per exchange, heal d6 as your action".
- Add a parity target to the sim tests. For example: every preset solo against a Standard foe of its level wins at least 60%, and per-PC drop rates in a Boss fight stay within 2× of each other.
- Delete the "balanced" claim until the sim supports it.

### C2. Magic has no ceiling where it matters most. Non-harm workings end Boss fights, and Arcane Mastery makes one working free forever.

**Claim.** Harmful workings are priced and weak, but control workings are neither priced nor bounded. The fight the book uses to showcase combat is won by one Significant working on a Boss, at the same 1-Fatigue price as a 1d8 bolt. From level 3, the Thaumaturge's signature Significant working costs nothing, so the Fatigue economy disappears for the thing the caster does most.

**Evidence.**
- **Scope text.** II.3:54: *"Significant is meaningful power or precision: a door fused, a person bound, one foe struck."* All three effects cost the same 1 Fatigue.
- **The showcase fight.** III.3:274–282: Zahna "rewrite[s] the instruction" on a Boss. It is Significant, and the Boss "never gets to swing". III.3:296 adds that the fight ended "with 11 still on the card".
- **An earlier working in the same fight.** III.3:232–236: a signature Significant working ("It can swing. It cannot step.") pins a Boss for 1 Fatigue.
- **The book leans in.** III.3:140: *"Workings that don't harm… often do more than damage does. The MM rules on what a working accomplishes."* No rule lets a foe resist a working. NPCs roll only to attack (III.1:143), and neither MM1 nor MM5 gives any guidance on control effects against Elites or Bosses (`grep` of MM1 for "working/magic/caster" returns one unrelated MM note).
- **Casting almost never fails.** A signature working is Easy. With Mind +2 and *Arcane theory*, which the book applies to every one of Zahna's rolls, that is +4, so 97% succeed and 72% land on 10+.
- **Arcane Mastery.** `facet.yaml:434` says *"One of your signature workings costs 1 less Fatigue (minimum 0)."* `plan_cast` at level 3 confirms it: `scope='significant' … fatigue=0 … steps=['signature working: one step Easier', 'Arcane Mastery: -1 Fatigue']`. The improved *Thaumaturgy* talent (−1 once per scene) stacks with it, which makes a **Major** signature working free once per scene as well.
- **Workings skip the combat modifiers.** `magic.resolve_cast` never calls `level_gap_difficulty`, cover, openings or Studied Foe (magic.py:207–218; `grep level_gap app/` finds only `combat.py`). A caster ignores the level gap, which makes a caster's attacks Hard only when the fighter's are.

**Why it matters.** This produces one of two tables:
- The MM says yes, and casters solve Bosses for free, which is the problem the Fatigue economy was built to prevent (II.3 *Through the Mirror*: "or the caster solves every problem in the first five minutes").
- The MM says no, arbitrarily, and the caster's player feels cheated.

Neither is "simple like earlier D&D". Old D&D bounded *hold person* with a saving throw and a level.

**Fix.**
- **Treat a working aimed at a foe as an attack.** Apply the level gap and cover to it, and let openings apply too.
- **Bound control by role.** Against an Elite or Boss, a Significant control effect lasts one exchange or costs the foe one attack, never the fight. A Major effect is needed to take a Boss out of a fight, and only once it is Bloodied.
- **Rewrite Arcane Mastery** as "once per scene, a signature working costs 1 less Fatigue", or "your signature workings are two steps Easier".
- **Fix the vignette** so the rules can reproduce it.

### C3. The ~25-rule promise isn't met. The player-facing load is about 75–85 rules, roughly v0.3's count, though it is much more familiar.

**Claim.** BRIEF §2 Goal 1 (BRIEF:36) promises *"About 25 player-facing rules, fitting on one double-sided reference card."* BRIEF §5 (BRIEF:282) reaches 25 by bundling. Counted at the granularity the complexity audit used for v0.3's "~85" (`RESEARCH_complexity_audit.md` appendix), the books ask a player to hold about the same number of rules as before.

**Evidence.** The rules a player needs, from Quick Start, III.1–III.3, II.3, II.4 and IV.1, excluding talents:

| Area | Rules (audit granularity) | Count |
|---|---|---|
| Core (III.1) | roll, tiers, 4 difficulties + "one step" shifting, knack non-stacking, +4 ceiling, extra dice keep-best-two, Spark spend, Help (action, one per roll, shares cost), Borrowed Trouble, natural 12, natural 2 (failed rolls only), 4 Spark sources, Graceful Fail content test, Avoid + stat map, PvP contest and tie, group majority, trying again, unnarrated details, Specialty | ~19 |
| Character and advancement (II.1–II.6) | +2/+1/+0, stat raises at 4/8 capped at +3, HP formula (max + Body, die or average, minimum 1), slots, coin, knacks (2–3), class = 5 parts, talent vs improved (hold one level), signature at 3, one pick per level, damage bonus at 3/6/9, signature workings at 5/9, respec before 3, teachers, casting never crosses, use periods (scene/session/rest/at will) | ~16 |
| Combat (III.3, III.2) | 5-step exchange, attack stat, attack tiers, 3 picks (with stunt and cover each defined), exposure (reach, next attack, this exchange), miss = MM move, 5 weapon dice, armor (subtract, cap 3, minimum 1), enemy tiers, enemy naturals and a lasting opening, Defend, Intercept (reach), level gap (2 bands), Mooks, mobs, Bloodied, morale, out of reach, Wound (slot, strain = Hard), Hold On, dying/tending/saved at 0, death choice, breather, night's rest | ~24 |
| Magic (II.3) | casting talent, domain boundary, intent, scope table (difficulty/Fatigue/level/harm), full-form and chaining, cast roll, 7–9 choice, 6− mishap + Graceful Fail, Fatigue paid regardless, harm dice + bonus − armor, Fatigue in slots / no slot, heavy armor, signature workings, Wider Domain and prismatic, Minor = stunt, lineage gift (Minor, cast with Soul), relics | ~17 |
| Gear, exploration, treasure | slot sizes and coin per slot, drop-on-overflow, usage die, curio limit, trinkets, heavy-armor stealth, Pressure die ("time is never free"), clock advance, clock wind-back, hazard armor | ~10 |
| **Total** | | **~86** |

A fairer framing: the count of *novel* rules fell a long way. Roughly 20–25 of these are ours: knacks, Sparks, Graceful Fail, Borrowed Trouble, exposure, the 10+ picks, openings, mobs, Hold On, the death choice, Fatigue in slots, scope and full-form, signature workings, teachers, the Pressure die and clocks. The audit counted about 55 novel rules in v0.3. The rest are HP, damage dice, armor, levels and saves, which a D&D player arrives already knowing. On top of this sit 36 talents, 36 improved forms and 18 signatures, about 90 opt-in texts. A level 10 character holds about 11 of them.

**Why it matters.** The owner asked for *simple like earlier D&D*, and the audit put early D&D at 15–20 rules. Lean Facets feels familiar, but it isn't light. MM5, the quick reference, is still 173 lines and eight sections, not one card. If the owner judges it on "simple", it fails to impress.

**Fix.** Write the actual two-page card the BRIEF called for (G0, BRIEF:370) and let it be the budget. Anything that doesn't fit becomes an optional rule or an MM-side procedure. Cut candidates are in the verdict and in m4, m6 and M11.

---

## MAJOR

### M1. *Sentinel* plus Intercept-all is a dominant party strategy that makes the telegraph irrelevant.

**Claim.** A Guardian with *Sentinel* can Intercept every attack aimed at every ally, every exchange, with no limit. Improved *Sentinel* (level 2) still attacks. The rest of the party never gets hit.

**Evidence.**
- `facet.yaml:114–126`: *"you may take the attacks aimed at every ally within your reach"*. The improved form reads *"While you Defend or Intercept you may still attack, at Hard."*
- `guard.py`: Guardian, Warrior, Thaum and Invoker against a same-level Boss, morale on:

| Level | Guardian attacks: any down (Thaum down) | Guardian Intercepts all: any down (Thaum down) |
|---|---|---|
| 1 | 51% (40%) | 38% (5%) |
| 5 | 56% (44%) | **10% (0%)** |
| 10 | 57% (47%) | **15% (2%)** |

The fight's length is unchanged: 5.3 vs 5.4 exchanges at level 5.

**Why it matters.**
- For the Tactician player, the telegraph is "where the tactics are" (III.3:21). Once one character soaks every blow, there is nothing left to answer.
- Improved *Sentinel* is the right pick for every Guardian. It kills Defend as a choice for anyone else, and it makes *Bulwark* ("ranged attacks can't target allies behind you") near-absolute.

**Fix.**
- Intercept takes the attacks of *one foe*, whatever its target.
- *Sentinel* lets you Intercept for two allies.
- Improved *Sentinel* lets you attack while Intercepting, but you are always exposed.

### M2. The MM's fight-reading table (MM1–4) is wrong in both directions, and it ignores party composition.

**Claim.** MM1 tells the MM to count threats (Standard 1, Elite 2, Boss 4, four Mooks 1). A total up to the party's headcount is a "real fight, someone gets hurt", and 1.5× the headcount is "hard". The simulation disagrees throughout.

**Evidence.**

| Level-1 default party (4 PCs), morale on | Threats | MM1 says | Simulation (`sim3.py`) |
|---|---|---|---|
| 4 Standard | 4 | real fight | 100% win, **5%** any down |
| 6 Standard | 6 | hard | 99.9% win, 21% down |
| 8 Standard | 8 | deadly | 96.5% win, 46% down |
| Boss, level 2 ("within the two-level band", MM1:124) | 4 | real fight | 83% win, **84%** down, 1.8 PCs down |
| Boss, level 3 | 4 | real fight | **30% win**, 98% down |
| Level 5 party, Boss level 7 | 4 | real fight | 97% win, 85% down |

MM1:202 reads *"Three level 1 characters against the Toll Ogre face 2 threats: a real fight."* In the sim, a level 3 Elite against a Warrior, Scout and Thaumaturge gives 97.5% win and 47% down. The same ogre against an Investigator, Speaker and Wanderer gives **23% win and 95% down**.

MM1:93 reads *"a level 5 foe is a fair match for one level 5 character."* Solo, it is 100% for the Warrior and 7% for the Physician (C1).

**Why it matters.** This is the one tool a novice MM will actually use, and it will produce padded fights with Standard foes and wipes with Bosses a level or two up. MM-driven variety depends on the MM trusting the dial.

**Fix.** Regenerate MM1–4 from the sim:
- Standard foes are worth about ½.
- A Boss at level +1 is worth about 6.
- Add a column for "the party's fighters" (Body characters and casters) versus the rest.
- Replace the two-level-band promise with the true one: at level 1, one level up for a Boss is already hard.
- Commit the sim cells as a regression test, so the table and the engine cannot drift apart.

### M3. MM1's worked examples use superseded monster numbers and contradict its own tables and the Quick Start.

**Evidence.**
- MM1:93: *"a level 3 foe that hits deals 4"*. Table MM1–1, `facet.yaml:1031` and MM5 all give level 3 damage as **6**.
- MM1:108: *"Five Mooks at level 2 roll once at +0 and deal 2 + 4 = 6… the survivors deal 2 + 1 = 3."* The level 2 Mook damage is 5 − 1 = **4**, so the mob deals **8**, and 5 once three are down (`Enemy.damage`: `max(1, row.damage + role.damage_mod)`).
- MM1:288, the Toll Ogre (damage 6 on its own card, MM1:45): *"a hard hit, 4 + 2 = 6… It deals 4… Zahna… is on 3 of his 6 HP."* The correct numbers are 8 − 3 = 5 to Mordai, and 6 − 1 = 5 to Zahna, leaving him on **1**.
- MM1:278: *"His longsword deals 1d8"*. Mordai has *Weapon Master* (blades), so the Quick Start (Quick_Start.md:81) and III.3:200 both say **d10**.

**Why it matters.**
- A novice MM learns the monster math from these examples, and every one is wrong in the direction that makes foes softer than the table says. The Zahna example understates his fragility by 2 HP out of 6.
- It is also a CLAUDE.md sync failure. The quick-reference rule exists to stop exactly this drift, and INV-26 checks tables, not prose.

**Fix.** Correct the four passages. Add an invariant that parses "level N … deals X" and the worked arithmetic, or move the examples into generated blocks.

### M4. "Reach" is undefined, and five rules hang on it. Ranged attacks strictly dominate melee.

**Claim.** The book never defines reach, yet each of these rules depends on it:
- exposure: "if a foe can reach you" (III.3:45);
- Intercept: "an ally within your reach" (III.3:87);
- *"Casters out of a foe's reach are out of its attacks"* (III.3:142);
- *Cleave* and *Whirlwind*: "within your reach".

**Evidence.**
- Grepping III.3, IV.1 and the Glossary for a definition of reach finds none. The Glossary uses the word only inside other definitions.
- A ranged weapon is d8 for 1 slot (IV.1, Table IV.1–1), the same as a longsword.
- An archer at range is never exposed, because exposure needs a foe that can reach you, and is out of every melee foe's attacks.
- Marksman and Deadeye add to this. The Scout is the highest-damage preset from level 3 (7.9 per action against the Warrior's 6.0, `dmg.py`).
- III.3:142 grants "out of reach" safety only to *casters*, so tables will argue whether it covers archers.
- Whether a melee foe can close the distance as its telegraphed action is left entirely to the MM.

**Why it matters.** "No grid" (III.3:3) is a good call, but theatre of the mind needs one binary state, or every exchange starts with an argument. The cost of a 7–9 is the only thing that makes melee attackers think, and a longbow removes it.

**Fix.**
- Define **engaged / not engaged** in one sentence: you are engaged with a foe if either of you could hit the other with a hand weapon this exchange.
- Exposure and Intercept work on engaged foes.
- Ranged attacks made while engaged are Hard.
- Ranged weapons are d6, or cost 2 slots with ammunition.
- A foe may spend its attack to engage.

### M5. "Is casting an attack?" has no answer in the book, the engine answered it silently, and the simulator invented a third answer.

**Evidence.**
- **The book.** II.3 gives a working's 7–9 result as "it works; pick one of two costs" (II.3:76), with no mention of exposure.
- **The engine.** `magic.resolve_cast` applies no level gap, cover, opening, stunt or Studied Foe, and it exposes nobody.
- **The simulator.** `combat_sim.py:175–176` does this:
  ```python
  if res.outcome == "partial_success":
      state.expose(ch.name, target.key)
  ```
  That is a rule that exists in neither the PHB nor `combat.py`. It breaks the CLAUDE.md iron law: *"Simulation tooling calls the shared rules module; it does not carry its own copy of rule logic."*
- **Undefined interactions.** The book doesn't say whether:
  - a harmful working "hits" a Mook (III.3:112: "a 7 or better on an attack");
  - a Major "2d8 to a group" drops one Mook or the whole mob (the engine applies one hit to the mob object, so a fireball kills **one** goblin);
  - Help on a working shares its mishap;
  - Studied Foe or a stunt makes a working Easy;
  - *Counterspell* works on foes, who never roll workings.

**Why it matters.** A table will argue these on the first night a caster is present, and the answers decide whether casters are strong (C2) or useless against mobs.

**Fix.** Add one line to II.3: *"A working aimed at a foe is an attack: difficulty, level gap, cover, openings and exposure apply as for weapons. A Major working against a mob drops one Mook per 4 damage."* Delete the simulator's private rule, or move it into `magic.py` along with the matching book text.

### M6. The custom-class promise (Morrowind) comes down to picking 2 of 11 or 12 talents. The biggest build lever, armor, belongs to nobody.

**Claim.** II.4:47 says *"a custom class can never out-muscle a preset… the Facet owns every number."* In practice a custom class differs from a preset only in its two starting talents, and those come from the same menu. The one choice that really changes balance, the kit, has no allowance at all. Armor is the largest defensive number in the game, and it isn't Facet-owned.

**Evidence.**
- **Menu size.** The menus hold 12 talents for Body, 11 for Mind (including *Wider Domain*) and 12 for Soul (its 11 own plus the shared *Wider Domain*). The `facet.yaml` count is `('mind','talent'): 11, ('soul','talent'): 11`. A non-caster has only 9 (Mind) or 10 (Soul) usable picks. That gives 66 (Body) and 36 or 45 (non-caster Mind or Soul) possible starting pairs; a caster has only one free pick, because the casting talent fills the other.
- **No hybrids.** The stat spread is forced (Facet +2), casting never crosses (II.4:174), and attacks always use Body. Morrowind's own hybrids (spellsword, nightblade, battlemage) are therefore impossible (Body) or bad (Mind with a weapon at +0).
- **Teachers.** The teacher gate is binary and in the MM's hands (II.4:172). The fun evidence recommended "never forbids, costs more" (`RESEARCH_lean_fun_evidence.md` §8.7).
- **The kit decides.** II.4:67 says *"The presets carry between 3 and 6 slots of kit. Stay inside that and nobody will blink."* Nothing stops a Mind custom class from starting in heavy armor and a shield (armor 3, 3 slots). The Physician preset with its kit swapped for a standard weapon, heavy armor and a shield, solo against a level 1 Standard foe (`create_character(..., kit=[...])`), goes from **49% to 90% win**. For a non-caster it costs nothing: the only penalties are Hard stealth and caster Fatigue. II.1:5 and II.1:24 ("steps 1 to 3 are the only ones with real consequences") are both false, because step 7 has the biggest consequence.
- **Presets overlap.** The Investigator and the Tactician share *Studied Foe*, so two of the four Mind presets have the same combat verb, and it is the weak one (m10).

**Why it matters.** The owner's Morrowind promise was flexibility inside a broad parent. What exists is a menu with a fence around it, and the one real lever (armor) undermines the claim that "the Facet owns every number".

**Fix.**
- Put armor in the Facet row: Body up to heavy plus shield, Soul up to light plus shield, Mind light only. Alternatively, make armor cost HP dice.
- Replace the teacher gate with a price: an off-Facet talent costs two picks, or needs a teacher *or* a pick.
- Allow one "cross-Facet class knack" that lets a class attack with its Facet stat. This is also a C1 fix, and it gives Morrowind-style hybrids without letting a Body character cast.
- Make the Tactician's second talent *Tactician* improved, or something new.

### M7. The caster budget doesn't grow with level, the two traditions diverge at level 3, and fighters' HP resets for free.

**Claim.** Fatigue lives in slots, and slots are 10 + Body. They never grow with level, and Mind characters typically have Body +0.

**Evidence.**
- `dmg.py`: the Thaumaturge has 10 slots and 5 free (5 Significant workings a day) at level 1, level 5 and level 10. The Invoker has 7 or 8 free.
- Each Wound fills a slot, and only one clears per night (III.2 Table III.2–1), so every drop costs a caster future workings.
- Meanwhile a breather restores half HP and can be taken "whenever the fiction allows a few quiet minutes" (III.2:92), so Body characters come into every fight fresh.
- At level 3, *Arcane Mastery* (Mind-only) makes one Thaumaturgy working free (C2). The Invoker's signature, *Miracle*, is one free Major a session. From level 3 the Thaumaturge's sustainable output is infinite and the Invoker's is capped.
- II.4b's *Arcane Mastery* says *"Requires: Thaumaturgy or Invocation"*. An Invoker can reach it only through a teacher for a signature, which the book never allows in words, though the engine does (`_menu_errors` accepts `teacher=True` for signatures).

**Why it matters.** For the Power Gamer, every level of a caster's growth goes into talents and HP, never into more magic. For balance, a Mind character is as limited on day 1 as on day 200, until *Arcane Mastery* removes the limit altogether.

**Fix.**
- Casters get +1 slot at levels 3, 5, 7 and 9 that can hold only Fatigue.
- Or a breather clears 1 Fatigue.
- Rewrite *Arcane Mastery* as in C2.
- Add a Soul-side equivalent, or make *Arcane Mastery* shared like *Wider Domain*.

### M8. Scaling flattens the dice at the top and stretches the fights.

**Evidence.**
- **The player roll saturates.** A Body fighter is at +3 from level 1 (Body +2 plus *Soldiering*, "fits most fights", III.3:29) and at +4 from level 4. Against a Standard foe that means a 97% hit chance and a 72% chance of a 10+, so the 7–9 exposure band shrinks to 25%. BRIEF §3 chose 2d6 because "partial success is the most common result", but that stops being true for the game's most common roll by level 4.
- **The enemy roll saturates too.** A Standard foe's attack is +4 at levels 9–10, and a Boss's is +5. That gives a 97% hit chance, with 72% hard hits for the Standard and 83% for the Boss. Defend's −1 still leaves 92% and 58% for the Standard. Defend and cover become nearly pointless at high level.
- **Monster HP outgrows PC damage.** Monster HP grows 4.4× (8 → 35, Boss 40 → 175), while PC damage per action grows 1.7× (Warrior 5.2 → 8.9). Exchanges to kill a Standard foe for one Warrior rise from about 1.5 to about 3.9. The ladder's Boss fight runs 3.0 → 4.6 → 6.0 exchanges (6.8 with a Guardian). At 4–5 PC rolls and 2 Boss rolls an exchange, that's 35–40 rolls, which is the "hack until it falls over" the evidence file warns about (§8 guard rails).
- **The Elite-to-Boss cliff.** A single Elite of the party's level is trivial: 1.4–2.6 exchanges and about 1% any-down at levels 1, 5 and 10. Two Elites give 24–41% any-down. A Boss gives about 50%. MM1 calls the Elite "the foes a scene is built around" (MM1:112), yet in the sim it dies before the scene begins.

**Fix.**
- Scale monster HP by +2 a level, not +3.
- Scale attack bonuses +1 / +1 / +2 / +2 / +2 / +3 across the ten levels, capped at +3, so Defend keeps its bite.
- Make Elite ×3 HP.
- Stop the class knack applying to every attack. Write "a knack fits a *kind of opponent or place*", so *Soldiering* fits a shield wall and not every fight.

### M9. Mook mobs reward splitting, turn big crowds into a slog, and make area effects dead.

**Evidence.** Default party, morale off (`sim2.py`):

| Mooks at level 1 | Exchanges | Any PC down |
|---|---|---|
| 12 as one mob | 4.0 | 32% |
| 12 as 3 mobs of 4 | 4.2 | **45%** |
| 20 as one mob | **7.0** | 62% |

At level 5 the gap is starker: 1% against 10.5%.
- **The damage cap.** A mob's damage caps at +4 at five Mooks, but it still needs one hit per Mook. A crowd of 20 is 20 attack rolls with one enemy roll an exchange.
- **No area answer.** *Cleave* improved drops 2–3. Major workings, *Whirlwind* and base *Cleave* have no stated interaction with a mob. The engine treats a mob as one target and drops one Mook (M5), and the text of base *Cleave* ("the damage left over") has no meaning against a foe with no HP.

**Fix.** A hit on a mob drops one Mook, plus one more per 4 damage, and area effects drop one per target. The book should say that mobs are 3–5 strong and that bigger crowds are several mobs.

### M10. The human playtest gate (G0) was skipped. The sim can't stand in for it, and its policy is thin.

**Evidence.**
- BRIEF:335 and BRIEF:370 set Gate G0: a two-page draft and one human session *"before the full rewrite"*.
- DESIGN:4 records the owner's `/goal` to build it all the way through. The owner authorised that, but no draft or playtest record exists (`ls docs | grep -i draft` finds nothing).
- The only fun test is the pacing ladder (`tests/test_combat_sim.py:103–120`). It asserts exchange counts and ">= 25% any-down for a Boss". It tests one party and no class parity.
- See §0 for what the sim policy leaves out.

**Why it matters.** The fun audit's R1, "a human table before rules work" (memory: `project_fun_audit_2026_09.md`), is still undone, now on top of a ~50k-word rewrite. Every "fast or flat" question in BRIEF:370 is still open.

**Fix.** Run G0 now against the current build, using the three BRIEF questions and one fight each way (enemies rolling vs not). Before that, add knacks, Defend, telegraph targeting and a parity suite to the sim policy.

### M11. Three talents the rules depend on don't work in the app, and one works incorrectly in the engine.

**Evidence.**
- **Studied Foe expires an exchange early.** The text says *"Until the end of the next exchange"* (II.4b:177). `combat.expire_exchange_effects` sets `enemy.studied = False` at the end of *this* exchange (combat.py:113–117).
- **Studied Foe and Anatomist can't be triggered.** No WebSocket handler sets `enemy.studied`. `grep studied app/api` finds nothing, and the only handler is `talent_use`, which ticks a counter. *Anatomist*, the Tactician's signature, therefore can't trigger in the app.
- **Warding Presence doesn't reach the attack.** It makes an enemy roll Hard, but `state.warded` is never set by any handler.
- **The Tactician gets nothing from it anyway.** Even with a studying policy, a Tactician who studies every exchange does no better than one who just attacks (`study.py`, Tactician first in order): about 32% against 36% any-down at level 1 against a Boss, and 17% against 15% at level 5.

**Why it matters.** The BRIEF's thesis is that the app absorbs the bookkeeping (BRIEF §6), and here the app can't do what the book prints. The Tactician preset's signature does nothing in the app, and its core verb is a trap.

**Fix.**
- Wire `study` and `ward` events.
- Fix the expiry to match the text.
- Buff *Studied Foe*: allies' attacks on the studied foe are Easy **and** deal +2 damage, or studying is free once per exchange.

### M12. Onboarding: what will confuse a new player and a novice MM first.

**New player, in reading order.**
1. **"Knack fits."** Quick Start line 9 gives +1 "if one of your knacks fits". II.4:55 says a good knack "fits about one roll in four". The vignettes apply the class knack to almost every roll: Zahna's *Arcane theory* on every Mind roll and working in III.3, Mordai's *Soldiering* on every attack. Players will argue about it every roll. (See also m3.)
2. **"Exposed."** It appears in Combat in Five Lines (Quick_Start.md:128) without a definition. So do stunt and cover.
3. **The caster step.** Pick 1 of 21 domains and *invent* two signature workings before you have seen a scope in play. This is the step most likely to break the ten-minute goal, and it's the one that decides the character's power (C2).
4. **Two things called "signature".** There is a signature talent at level 3 and there are signature workings, and a signature (*Arcane Mastery*) modifies signature workings. "Facet" means both a Facet and a rules module (Glossary:53), and "Body" is both a Facet and a stat.

**Novice MM.**
1. The Quick Start gives the MM nothing to run: no foe, no numbers, no pointer to MM5.
2. The first encounter they build from MM1–4 will be mis-sized (M2), and the worked examples teach the wrong damage (M3).
3. "Reach" (M4) and "what can a Significant working do to my Boss?" (C2) are the first two rulings they'll be asked for, and the books answer neither.

**Fix.**
- Add a one-paragraph "Your first fight" to the Quick Start: a named Standard foe and 4 Mooks, with numbers.
- Define "exposed", stunt and cover inline.
- Let casters defer naming signature workings until their first session, or take two from a list of examples per domain.
- Rename the level 3 pick to **Mark** or **Calling**.

---

## MINOR

**m1. The extra-dice ceiling contradicts itself.** III.1:60 says *"rolls 5d6 and keeps the best two. That is the most one roll can be made into."* III.1:95 says *"spend as many Sparks as you like"*. *Inspiring* and *Rallying Cry* each add a d6 too. The real maximum is 3 Sparks + Help + Borrowed Trouble + *Inspiring* = 8d6. **Fix:** cap Sparks at one per roll, and state it.

**m2. Help contradicts itself, and its cost-sharing is undefined in a fight.**
- III.1:56 says *"One Help per roll."*
- III.1:149 says *"the lead rolls, and each helper adds a die."*
- The book never says whether a helper on a 7–9 attack is exposed, which matters for retainers (MM3:228) and the *Tactician* talent.

**Fix:** choose one and say that Help on an attack shares exposure.

**m3. Knack scope contradicts itself.**
- II.4:55 says a knack is *"never a bare verb… 'Fighting' … would fit every roll of that kind forever."*
- III.3:29 says *"Soldiering fits most fights for a soldier."*

*Soldiering* is "Fighting" under another name. It pushes fighters to the ceiling (M8) and widens C1. **Fix:** class knacks name a context ("shield walls", "sieges"), and the book's examples obey the one-in-four guidance.

**m4. The +4 ceiling is a dead rule.** III.1:21 and `facet.yaml:772` (`bonus_cap`) cap stat + knack + talent bonuses at +4. The highest stat is +3 and a knack adds +1, so the total can never exceed +4. No talent gives a roll bonus (II.4:97: "Talents are not +1 bonuses"), and no relic or curio does either (a `grep` of `tables.yaml` for bonuses finds nothing). Every player learns a rule that never changes a roll. **Fix:** delete it, or keep it only as a design note for Facet authors.

**m5. Stacking of difficulty sources is undefined.**
- Defend + cover + *Warding Presence*; a stunt opening + *Studied Foe*; the level gap + an opening.
- The engine decides that Hard sources don't stack (`resolve_enemy_attack` docstring) and that one opening eases once. The book doesn't say either.

**Fix:** add one line: *"Difficulty moves at most one step easier and one step harder from Standard, whatever the sources."*

**m6. Rebuilding and teachers leave questions open.**
- II.4 Table II.4–3 says level 3 is where *"rebuilding stops being free"*, which implies a paid rebuild. II.4:168 describes no mechanism. It doesn't say whether a player can ever swap a dead talent.
- For teachers (II.4:172), the book doesn't say whether learning costs the level pick (the engine says yes), whether signatures and improved forms can be taught, or what happens if the MM never provides a teacher.

**Fix:** after level 3, a player may swap one talent at a level-up in place of the pick. A teacher lets you spend a pick off-menu, and signatures can't be taught.

**m7. Companions and retainers contradict each other.**
- *Beast Friend* improved gives *"a Standard foe of your level, fighting at your side"* (II.4c:149).
- MM3:228 says an ally's only combat action is Help, and the engine docstring for `retainer_morale` agrees.
- The *Captain* talent's "Normal: Hirelings are NPCs with their own morale" and MM3's open hiring mean that anyone can keep retainers. The talent's base form only adds morale and *caps* retainers at two.

**Fix:** a companion or retainer gives Help, or attacks in place of its owner's action. The *Captain* talent should grant the retainers, not restrict them.

**m8. Menu counts are misstated.** II.4:25 says *"Every Facet gets a menu of twelve talents."* Mind has 11, counting *Wider Domain* (II.4b has 11 entries, and `facet.yaml` has 11 Mind talents). A non-caster Mind character has 9 usable picks.

**m9. Signatures are uneven.**
- *Polymath* (II.4b:243) gives **two** talents, from any Facet, with no teacher. Every other signature gives one effect.
- *Voice of Command* works on a Boss of your level.
- *Iron Lungs* improved ("a breather restores all your HP") is nearly nothing, because breathers are unlimited.

**Fix:** *Polymath* gives one talent, and *Voice of Command* excludes Bosses.

**m10. Some talents are dead, dominated or dull.**
- *Studied Foe* is worse than attacking (M11).
- *Scout's Eye* negates "surprise", which no rule defines. III.3 has no surprise mechanic.
- *Pathfinder* skips Pressure die rolls. That also skips face 5, "opportunity", so its effect is nearly neutral.
- *Counterspell* works against foe workings, which have no rules.
- *Captain* base is covered in m7.
- Five improved forms are just "twice" or "two": *Lucky*, *Warding Presence*, *Hunch*, *Alchemist* and *Captain*. Those are the "thin level-ups" the evidence file warns against (§8 guard rails).

**Fix:** give each of these a new verb, and define surprise in one line (a surprised side loses its first exchange's attacks).

**m11. The 10+ pick has a dominant option: +1d6.** A rough expected value at level 1 against a Standard foe:
- +1d6 is about 3.5 damage.
- A stunt is worth about 1 damage (it moves one ally from 83% to 92% and from 42% to 58% on 10+).
- Cover prevents about 0.8 damage per incoming attack, or about 2 against a Boss's pair.

The sim hard-codes +1d6. Stunt and cover win only against Mooks (where extra damage is worthless) or to protect someone about to drop. At level 4, with a 72% chance of 10+, it's picked almost every exchange. **Fix:** make the stunt "+ the ally's next attack deals +1d6", or let cover redirect one attack to the attacker.

**m12. The Threat Clock pacing claim is off for skilled rollers.** III.2:43 says *"A four-segment clock fills in five or six rolls."* That's true at +1 or +2. At +3 or +4, where most characters have a fitting knack, 7–9 or worse comes up only 42% or 28% of the time, so the clock takes 10–14 rolls.

**m13. One rule quietly applies across scenes.** A natural-2 "opening lasts until you use it" (III.3:73). The engine keeps named openings indefinitely, so an opening from last week's fight still applies if the same foe returns. **Fix:** make openings last until the end of the scene.

---

## NIT

- **n1.** Quick_Start.md:79, *"Eleven years on the watch."* It isn't in `characters/Mordai.fof` ("years of service") or at `pre-lean-facets`. It is new canon introduced in an example, against CLAUDE.md's iron law.
- **n2.** The "Rules: Contested" section (III.1:143) says the MM's characters "roll only to attack in combat", but morale and reaction rolls are MM rolls that PCs see. Say "roll only to attack, or on the MM's own procedures".
- **n3.** III.3:282, *"It never gets to swing. Your working happened first."* Players always act before enemies, so this is always true, and the line reads as a special ruling.
- **n4.** The *Arcane Mastery* entry says "Requires: *Thaumaturgy or Invocation*", but the talent is only on the Mind menu (II.4b:201). Either share it or drop "or Invocation".
- **n5.** III.1:52 says *"Three things add a die."* Five do (see m1).
- **n6.** The level gap has two bands ("Very Hard at 6+"), but at the ceiling a fighter still hits a foe 6 levels up 83% of the time, and a caster ignores the band entirely (C2). Keep one band, or apply it to HP instead.

---

## What works (so the verdict is fair)

- **Enemies rolling in the open is implemented cleanly.** It is one function, and the app rolls with one click. The prose explains why, and MM1's *Through the Mirror* makes a good case for it. It meets the owner's instinct.
- **The monster card** (WANTS, SPECIAL, WHEN BLOODIED, TELLS, BREAKS, TWISTS) is the best artifact on the branch. It's genuinely MM-driven variety, and it's what the owner asked for.
- **The table numbers agree across the core sources.** MM5, MM1 Table MM1–1, III.3 and `facet.yaml` agree (the prose examples in M3 don't). The generated toolbox and Bestiary pipeline is the right shape.
- **The death choice, Hold On, the Graceful Fail and peer Sparks** keep the adventure register and the social economy intact.
- **Novelty load fell** from about 55 to about 20–25 rules (C3). A D&D player will recognise most of the sheet.

---

## Verdict

**Does it impress?** Not yet. It impresses as *execution*: books, engine, app, Bestiary and module all rebuilt in a day, and they agree with each other on the numbers. As *design* it doesn't meet the owner's four goals:
- **Simple like early D&D.** It's familiar, but not simple: about 85 rules against a promise of about 25 (C3).
- **Flexibility and custom classes.** A custom class is two picks from one menu. Hybrids are blocked, and kit, which nobody owns, outweighs the class (M6).
- **More fun.** Half the presets are spectators in a fight, and the gap grows with level (C1). One talent turns the telegraph off (M1). Casters are either weak blasters or unbounded controllers, depending on the MM (C2).
- **MM-driven variety.** It's the strongest part. The MM-side dial that sets difficulty is miscalibrated, and its examples are wrong (M2, M3).

None of this is fatal to the chassis. The core (2d6 three tiers, HP, damage, armor, enemies roll, monster cards, the toolbox) is sound. The problems are in tuning, in a few missing definitions, and in the Facet numbers.

**The three highest-leverage changes:**

1. **Make every Facet able to fight, and prove it in the sim.**
   - Attacks use your Facet's stat, or the class knack names it.
   - Narrow the grit dice to d10 / d8 / d8, or add +4 HP at level 1.
   - Put armor allowances in the Facet row.
   - Add a preset-parity suite: each preset solo against a Standard foe of its level at levels 1, 5 and 10; per-PC drop rates in a Boss fight within 2×.

   This one change fixes C1, most of M6, and the "balanced" and "no class is stronger" claims.
2. **Give magic a frame.**
   - A working aimed at a foe is an attack: level gap, cover, openings and exposure all apply.
   - Control effects on an Elite or Boss last one exchange or cost it one attack.
   - *Arcane Mastery* works once per scene.
   - Casters get a slot budget that grows with level.

   This fixes C2, M5 and M7, and it removes the most likely first-night argument.
3. **Cut to the card, define the missing words, then put it in front of humans (G0).**
   - Write the two-page player and MM card the BRIEF promised, and let everything else become optional or MM-side. Candidates:
     - delete the +4 cap and the Very Hard level-gap band;
     - cap Sparks at one per roll;
     - collapse Wider Domain and prismatic into one line;
     - drop the natural-2 opening.
   - Define **engaged**.
   - Fix *Sentinel* to one foe.
   - Fix mob damage and area effects.
   - Regenerate MM1–4 from the sim and correct the four worked examples.
   - Then run the G0 session the BRIEF required, with its three questions, before touching another chapter.
