# RESEARCH: v1.1 magic frame (D5 control, D6 working-as-attack, D7 casting budget)

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` · **Tier:** research for Brain (strategy input, not a ruling)
**Inputs read:** `REVIEW_lean_facets.md` (X3), `REVIEW_lean_design.md` C2 / M5 / M7, `II.3_Magic.md`, `III.3_Combat.md` (Archive Guardian), `facet.yaml` (`magic`, `talents`, `advancement`, `slots`, `monsters`), `app/game/magic.py`, `tools/combat_sim.py`.
**Math:** analytic 2d6 odds plus Monte Carlo runs that drive the real engine (`combat.py`, `magic.py`, `character.py`) through throwaway scripts in the session scratchpad (`magic_math.py`, `magic_math2.py`). Each proposed control rule is **emulated at the policy level in the scratch script only**. No repo code was changed.

---

## Summary

Every well-regarded game that keeps flexible magic fun bounds it in one of three ways:

1. **The target resists.** The foe gets a save, and in 5e a Boss can turn failures into successes (Legendary Resistance). This covers B/X, 5e and Ars Magica.
2. **The effect is sized by the foe's rank.** 13th Age sets HP thresholds, Ironsworn marks less progress against higher ranks, Blades limits effect by scale, Cypher compares levels, and B/X *Sleep* counts Hit Dice.
3. **The budget is visible and grows by level.** Knave ties spells per day to level, Maze Rats and DW prepare more with level, and 13th Age grows daily slots.

The resistance route adds a roll, and in this chassis it scales the wrong way. A same-level Boss rolling 2d6 + attack ≥ 10 shrugs 42% of control at level 1 and 83% at level 9, so control is either a coin-flip fight-ender or a dead option. The Alexandrian's "craps game" critique of save-or-die applies to both halves of that.

The rank-sizing route fits Facets best. It reuses states the table already tracks (role, Bloodied, Hard), adds no roll, and leaves Domain + Intent + Scope untouched. The MM still rules *what* a working does; the rule only says *how long* it holds against someone important.

**Recommendations (one sentence of rule each):**

| # | Pick | The sentence |
|---|---|---|
| **D5** | Rank-sized control | *A working that would stop a foe outright (bind, blind, charm, sleep) stops a Mook or Standard foe, but only hinders an Elite or Boss for one exchange (its attacks are Hard) unless the foe is Bloodied and the working is Major.* |
| **D6** | Attack for difficulty, magic for cost | *A working aimed at a foe is an attack for everything that makes it Easier or Harder, and on a 7–9 one of the two costs offered is always that you are exposed.* |
| **D7** | Fatigue slots by level | *A caster gains one slot that holds only Fatigue at levels 3, 5, 7 and 9.* Paired with a text-only rewrite of *Arcane Mastery*: "Once per scene, one signature working costs 1 less Fatigue." |

**Headline numbers:**

- **D5, today:** a signature control working takes a same-level Boss out on the first exchange 97% of the time. The fight averages 1.0–1.04 exchanges and the party loses 0–0.7% of its HP.
- **D5, under the pick:** a Boss fight at level 1 takes 3.6 exchanges and costs 43% of party HP, against 3.0 and 38% when the caster throws bolts. Control is worth about one bolt.
  - At levels 5 and 9, a Major working that finishes a Bloodied Boss shortens the fight by about one exchange.
  - A PC drops in 12–19% of those fights, against 38–43% for bolts. That is the price of the climax (see Risks).
- **D7:** today a Thaumaturge's 5 free slots cover 56% of their actions in a day at level 1, 37% at level 5 and 30% at level 9. From level 3, *Arcane Mastery* makes that 100%: the engine run shows **0.0 Fatigue paid** in Boss fights at levels 5 and 9.
  - The pick holds the share at 51–56% from level 1 to 9.
  - The two alternatives overshoot, one to 61% and the other to 85%.

---

## Part 1: Findings, game by game

Legend: **F** = the page was fetched this session and the notes come from it. **K** = from the published rules as I know them; the page was not fetched (fetches failed or were blocked). Verify any **K** item before citing it in the books.

### 1. OD&D / B/X (Old-School Essentials and Basic Fantasy as the open restatements)
- **Concept:** Monsters save as a fighter whose level equals their Hit Dice, so bigger things resist more. *Sleep* rolls a pool of Hit Dice, affects the weakest creatures first, and never touches anything above a small HD cap, with no save. *Hold person* allows a save, and a lone target saves at a penalty. *Charm* lets the victim re-save on a schedule set by its intelligence. (K)
- **How it stays simple:** there is one save table, indexed by HD. Control power is sized against HD, so a level 1 *Sleep* ends a goblin fight and does nothing to an ogre.
- **Evidence of play:** *Sleep* is famous for deciding low-level fights, and that is why it is capped by HD. The Alexandrian argues that save-or-lose effects turn tactics into "a craps game", and that later editions only watered them down (F).
- **Licence:** OSE and BFRPG are published under the OGL 1.0a. **Ideas only.**
- URLs: https://thealexandrian.net/wordpress/7022/roleplaying-games/save-or-die (F) · https://oldschoolessentials.necroticgnome.com/srd/ (fetch returned HTTP 500) · https://basicfantasy.org/srd/ (fetch returned 403)

### 2. D&D 5e (SRD 5.1)
- **Concept:**
  - Control spells allow a save and let the target repeat it at the end of each of its turns ("save ends").
  - They need **concentration**, which breaks on damage (a Con save) and is limited to one spell at a time.
  - Legendary monsters have **Legendary Resistance**: three times a day they may turn a failed save into a success. (F)
- **How it stays simple:** it doesn't, quite. There are three layers: save, repeated save and concentration. Legendary Resistance is a flat patch for Bosses.
- **Evidence of play:** Legendary Resistance exists because *hold monster* and *banishment* ended solo fights. It is widely disliked as a "you wasted your turn" moment. The complaint is common, but the specific critique pages I tried returned 404, so I have no citation for it.
- **Licence:** SRD 5.1 is **CC BY 4.0**. Wording is usable with attribution, though no wording was needed here.
- URLs: https://www.5esrd.com/spellcasting/all-spells/h/hold-person/ (F) · https://www.dnd5eapi.co/api/monsters/adult-red-dragon (F, Legendary Resistance 3/day) · https://www.dndbeyond.com/sources/dnd/free-rules/rules-glossary (F, Concentration, Incapacitated, Paralyzed)

### 3. 13th Age
- **Concept:**
  - Saves are one d20 against 6+, 11+ or 16+ (a hard save). "Save ends" effects roll at the end of each turn. (F)
  - Its control spells are gated by **the target's current HP**:
    - *Color Spray* weakens only foes at 10 HP or fewer after its damage.
    - *Charm Person* needs a target at 40 HP or fewer.
    - *Hold Monster* needs 60 or fewer.
    - *Sleep* rolls an HP budget and puts the weakest to sleep first.
    - All the thresholds rise with spell level. (F)
  - The **escalation die** (+1 per round, PCs only) pushes fights toward an end. (F)
- **How it stays simple:** HP is already on the table, so "is it hurt enough to be held?" needs no extra roll. Control grows stronger as the fight goes on, which gives the climax to magic without handing it the opening.
- **Evidence of play:** HP-gating is the part of 13th Age most often borrowed. It is the direct ancestor of "Major only on a Bloodied Boss" below.
- **Licence:** 13th Age SRD, **OGL**. **Ideas only.** Do not reuse the thresholds as numbers, and note that "NASTIER" is already flagged.
- URLs: https://www.13thagesrd.com/classes/wizard/ (F) · https://www.13thagesrd.com/combat-rules/ (F)

### 4. Dungeon World
- **Concept:**
  - On a 7–9 a spell works, but the caster picks a cost: draw unwelcome attention, take −1 ongoing to cast, or forget the spell. (F)
  - Ongoing spells burden later casting. (F)
  - Spells prepared total the caster's level + 1. (F)
  - Control is fragile: the cleric's *Hold Person* breaks the moment the target takes damage, *Charm Person* breaks on damage, and *Sleep* breaks on noise or pain. (F)
  - On a miss, the GM "makes a move". (K)
- **How it stays simple:** control spells carry their own end condition in the fiction, so no save is needed. Costs are chosen by the player, not rolled.
- **Evidence of play:** the "pick your cost on a 7–9" pattern is what Facets already uses for magic (II.3 complications). DW proves it is fun. It also shows that "one cost is always exposure" is a natural fit.
- **Licence:** **CC BY 3.0**. Treat as **ideas only**: the brief admits only 4.0 wording, and III.1 already has a verbatim-phrase finding against it.
- URLs: https://www.dungeonworldsrd.com/classes/wizard/ (F) · https://www.dungeonworldsrd.com/classes/cleric/ (F)

### 5. Ars Magica (concept only)
- **Concept:** magic is a **Technique** (create, perceive, transform, destroy, control) plus a **Form** (fire, mind, body, and so on) (F). Spontaneous magic is freeform but weaker than prepared formulae (F), and costs fatigue at full strength (K). A supernatural being's **Might** grants **Magic Resistance**, which a spell must *penetrate* (K).
- **How it stays simple:** a verb plus a noun is exactly Domain + Intent. Resistance is a single number on the creature.
- **Evidence of play:** Penetration against Might is the standard answer to "why can't I just control the dragon?" It is the resistance route, and it takes bookkeeping.
- **Licence:** Atlas released the 5th-edition texts under an open licence (F). I believe it is CC BY-SA 4.0, but that is unverified. **Concept only**, as the brief asks.
- URL: https://en.wikipedia.org/wiki/Ars_Magica (F)

### 6. Mage: the Ascension / Awakening (concept only)
- **Concept:** the player proposes an effect and the GM adjudicates it by the caster's rating in the relevant Sphere (F). Effects that are obvious (vulgar) or large build **Paradox**, a backlash that grows with the size of what you did; subtle (coincidental) effects are cheaper (K).
- **How it stays simple:** it doesn't. It has a reputation for adjudication arguments. The lesson is that freeform magic needs a *size* price, not only a *kind* check.
- **Licence:** proprietary (Paradox Interactive / Onyx Path). **Ideas only.**
- URL: https://en.wikipedia.org/wiki/Mage:_The_Ascension (F)

### 7. Whitehack
- **Concept:** the Wise pays for miracles in **HP**, at a price negotiated with the referee. Miracles that fit the Wise's vocation or wises cost less; those that don't cost more (K). Wikipedia confirms that reviewers singled out its magic/miracle system for praise (F).
- **How it stays simple:** one resource, and "fits your identity" is a discount. That is Facets' signature working, one step Easier.
- **Licence:** proprietary. **Ideas only.**
- URLs: https://en.wikipedia.org/wiki/Whitehack (F) · https://whitehackrpg.wordpress.com/ (F, no rules text)

### 8. Cairn
- **Concept:** a spellbook holds one spell and fills one slot, and anyone can read it. Each cast adds one **Fatigue**, which takes an inventory slot. Casting while deprived or in danger needs a WIL save, and failure can mean more Fatigue, a lost book or injury. With time and safety, effects can be amplified. (F)
- **How it stays simple:** the budget is the inventory, which is where Facets took Fatigue-in-slots from (the Credits misattribute this; see REVIEW X8). Cairn's budget does not grow with level, because Cairn has no levels.
- **Licence:** **CC BY-SA 4.0**. Wording usable with attribution and share-alike.
- URL: https://www.cairnrpg.com/first-edition/cairn-srd/ (F)

### 9. Knave
- **Concept:** 100 level-less spells, each in a spellbook that takes a slot (F). How many spells a caster casts per day scales with their level (K, per the brief and the 1e/2e texts as I recall them).
- **How it stays simple:** the budget number *is* the level, with no table to read.
- **Licence:** **CC BY 4.0** (F).
- URL: https://questingbeast.itch.io/knave (F)

### 10. Maze Rats
- **Concept:** spells are generated at random from 2d6 tables and refill each night (F). Spell slots are a feature characters can gain as they level, so a caster's capacity widens by choice (K).
- **How it stays simple:** the size of an effect is fixed by how a spell is generated; its creativity comes from the tables.
- **Licence:** no open licence stated (F). **Ideas only.**
- URL: https://questingbeast.itch.io/maze-rats (F)

### 11. Shadowdark
- **Concept:** a spell check is d20 + stat against 10 + the spell's tier. On a failure you lose that spell until you rest, and a natural 1 on a wizard's check brings a mishap. Focus spells must be maintained with checks. (K)
- **How it stays simple:** the budget is the success rate. Casters cast until they fail, so there are no slots to count, and bigger spells fail more often.
- **Licence:** Shadowdark Third-Party License (F), not CC. **Ideas only.**
- URL: https://www.thearcanelibrary.com/pages/shadowdark (F)

### 12. Dungeon Crawl Classics
- **Concept:** the spell check is d20 + caster level. The result reads off a per-spell table, so the effect's *size* scales with the roll. A low roll loses the spell for the day. **Spellburn** spends ability points for a bonus, and **corruption** comes on a disaster. (K)
- **How it stays simple:** it isn't simple, since every spell has its own table. The takeaway is that the roll sets the size of the effect, and paying with yourself is dramatic.
- **Licence:** OGL-based; Goodman Games joined the ORC Alliance in 2023 (F). **Ideas only.**
- URL: https://en.wikipedia.org/wiki/Dungeon_Crawl_Classics_Role_Playing_Game (F, company page; no mechanics)

### 13. Troika!
- **Concept:** casting costs **Stamina**, which is also your health, and is a roll-under skill test. Double results trigger an "Oops!" table (K).
- **How it stays simple:** the price is your HP, as in Whitehack. Magic and survival compete.
- **Licence:** a Troika third-party licence (F), not CC. **Ideas only.**
- URL: https://www.troikarpg.com/ (F)

### 14. Cypher System (and Numenera)
- **Concept:** everything has a level from 1 to 10, and the target number is 3 × the level (F). A creature's level is both how hard it is to hit and how hard it is to affect (F). **Effort** spends pool points to ease a task one step each (F). Abilities are typically written as "affects a creature of level N or lower", so control is sized by level (K).
- **How it stays simple:** one number compared against one number. Level gating is the cleanest form of "sized by rank".
- **Licence:** Cypher System Open License (F), not CC. **Ideas only.**
- URLs: https://callmepartario.github.io/og-csrd/ (F) · https://www.montecookgames.com/cypher-system-open-license/ (F)

### 15. Fate Core
- **Concept:**
  - **Create an advantage** puts an aspect on the scene with one free invoke, or two on a success with style. (F)
  - If the target is a character, it defends. (F)
  - A failure hands the opponent a free invoke. (F)
  - A "bound" aspect is leverage, not a win: taking someone out still takes stress and consequences. (K)
  - Contests are first to three victories. (F)
- **How it stays simple:** a control effect is a **bonus on a later roll**, not a removal. That is the model for "hinders an Elite or Boss".
- **Licence:** Fate SRD, **CC BY 3.0** (F). Ideas only under the brief's 4.0 rule.
- URLs: https://fate-srd.com/fate-core/four-actions (F) · https://fate-srd.com/fate-core/contests (F)

### 16. Blades in the Dark
- **Concept:** the GM sets **position** (danger) and **effect** (how much you achieve) before the roll. Effect is cut by **scale, potency and quality**, so a lone scoundrel has limited effect on a gang. (F) PCs **resist** consequences for stress equal to 6 minus their highest die (F). GM guidance says never to inflict a complication that negates a success (F).
- **How it stays simple:** effect size is judged once, before the roll, which matches Facets' "the MM sets the scope before the roll". Big threats get clocks, so one roll ticks progress and does not end them (K).
- **Licence:** CC-licensed per the site (F); I believe it is CC BY 3.0. Ideas only.
- URLs: https://www.bladesinthedark.com/action-roll (F) · https://www.bladesinthedark.com/resistance-armor (F) · https://www.bladesinthedark.com/consequences-harm (F)

### 17. Ironsworn
- **Concept:** momentum builds on success and can be burned to replace the action die with it (F, partly; the burn itself is K). A foe's **rank** sets how much progress each hit marks, from several boxes against a troublesome foe to a single tick against an epic one (K).
- **How it stays simple:** the same action does less against a bigger foe. No resistance roll is needed, because the rank is the resistance. That is the D5 pick exactly.
- **Licence:** the Ironsworn SRD and asset/oracle text are **CC BY 4.0**; the full rulebooks are CC BY-NC-SA 4.0 (F).
- URLs: https://tomkinpress.com/pages/ironsworn (F) · https://tomkinpress.com/pages/licensing (F)

### 18. Daggerheart
- **Concept:** duality dice generate Hope for the player or Fear for the GM, and the GM spends Fear on moves (F). **Spellcast rolls count as attack rolls when the spell can damage** (F). Spells end when you choose, at story moments, or as written (F). Temporary conditions such as Restrained clear through an action roll (F).
- **How it stays simple:** "a spell that hurts is an attack" means one set of modifiers. That is the precedent for D6.
- **Licence:** Darrington Press Community Gaming License (F), not CC. **Ideas only.**
- URLs: https://en.wikipedia.org/wiki/Daggerheart (F) · https://raw.githubusercontent.com/seansbox/daggerheart-srd/main/README.md (F, SRD mirror) · https://www.darringtonpress.com/license/ (F)

### 19. Invisible Sun / Numenera
Nothing beyond Cypher's level gating is useful here. Both are proprietary: **ideas only**.

**Sources fetched successfully this session:** 30 URLs, as listed above.
**Research limits:** WebSearch was unavailable (its session budget was spent), so every source is a direct fetch. Several OSR and rules pages were blocked or returned 404/500. Those findings are marked **K**.

---

## Part 2: Patterns that transfer

| Pattern | Games | Cost at the table | Fit for Facets |
|---|---|---|---|
| Foe resists with a save | B/X, 5e, 13th Age, Ars Magica | +1 roll per control, sometimes every turn | Poor: adds a roll, and the Boss attack bonus grows, so resistance scales the wrong way (see D5 option A) |
| Boss-only patch (LR, hard save) | 5e, 13th Age | Tracks uses; players feel robbed | Poor on its own |
| **Effect sized by the foe's rank or HP** | 13th Age thresholds, Ironsworn rank, Blades scale, Cypher level, B/X *Sleep* HD | No roll; reads a state already on the card | **Best**: role and Bloodied already exist |
| Control breaks on a trigger | DW (damage breaks hold), 5e concentration | A fictional end condition | Good as MM texture; not a rule sentence |
| Control as a bonus, not a removal | Fate aspects, Blades clocks | None | Good: "its attacks are Hard" reuses Defend/cover |
| A spell that hurts is an attack | Daggerheart, 5e spell attacks | None | **Best for D6** |
| Budget = level | Knave, DW prep, 13th Age slots, Maze Rats slots | Read the level | **Best for D7** |
| Identity discount | Whitehack vocation, Facets signatures | None | Already present; keep, but cap it |

---

## Part 3: The decisions

The numbers come from the level table (`monsters.level_table`) and the Boss role (×5 HP, +2 damage, +1 attack, 2 attacks):
- level 1 Boss: 40 HP, attack +2, damage 6;
- level 5 Boss: 100 HP, attack +3, damage 10;
- level 9 Boss: 160 HP, attack +5, damage 14.

The caster rolls with Mind +2 and a knack at level 1, and at the +4 cap from level 4. The Monte Carlo runs use the default sim party against one same-level Boss, 2,000 trials each. The Thaumaturge's policy varies; everything else is the engine.

### D5. Control workings are unbounded

**The problem, measured.** A signature working is Easy, so the level 1 caster rolls at +4 and it succeeds 97.2% of the time (72.2% on 10+). From level 4 it is +5, which is 100%. Under today's rules, a control working that lands takes the Boss out:

| Level | Policy | Win | Exchanges | Any PC down | Party HP lost |
|---|---|---|---|---|---|
| 1 | caster throws bolts | 99.3% | 2.95 | 47.6% | 38.1% |
| 1 | control, today's rules | 99.9% | **1.04** | 0.4% | 0.7% |
| 5 | bolts | 100% | 4.55 | 43.0% | 48.0% |
| 5 | control, today | 100% | **1.00** | 0.0% | 0.0% |
| 9 | bolts | 100% | 5.43 | 38.0% | 54.0% |
| 9 | control, today | 100% | **1.00** | 0.0% | 0.0% |

A Boss fight is one roll. The bolt rows show a second issue (D7): at levels 5 and 9 the Thaumaturge paid **0.0 Fatigue** across the fight, because *Arcane Mastery* makes the signature bolt free.

**Option A: the foe resists (B/X save, 5e, Ars Magica).** An Elite or Boss rolls 2d6 + its attack bonus and shrugs the control on 10+.

| Level | Boss attack | Boss shrugs | Signature control lands |
|---|---|---|---|
| 1 | +2 | 41.7% | 56.7% |
| 3 | +3 | 58.3% | 40.5% |
| 5 | +3 | 58.3% | 41.7% |
| 7 | +4 | 72.2% | 27.8% |
| 9–10 | +5 | 83.3% | 16.7% |

- Simulated: 1.77 exchanges at level 1 and 2.32 at level 5.
- Still swingy: about 40–57% of the time a single roll ends the Boss fight.
- It adds a roll and inverts with level. At high level, control stops being worth casting.
- **Rejected.**

**Option B: the effect is sized by the foe's role (13th Age, Ironsworn, Blades, Cypher, Fate). THE PICK.**

> *A working that would stop a foe outright (bind, blind, charm, sleep) stops a Mook or Standard foe, but only hinders an Elite or Boss for one exchange (its attacks are Hard) unless the foe is Bloodied and the working is Major.*

- **How often a same-level Boss shrugs it:** never outright. The working lands on the caster's own roll (97% signature, 92% otherwise at level 1), and then it is *capped*, not resisted.
- **Why "Hard" is the right size:** Hard is the game's existing unit of defense (Defend, Intercept, cover, Warding), and it does not stack with them. A Significant control on a Boss is worth about one bolt:
  - At level 1, one exchange of Hard on both Boss attacks saves about 1.7 HP of party damage. A bolt takes 3.5 HP off a 40 HP Boss.
  - Across a whole fight, the simulation puts the two side by side:

| Level | Policy | Win | Exchanges | Any PC down | Party HP lost |
|---|---|---|---|---|---|
| 1 | B, hinder only (Major not yet available) | 98.7% | 3.58 | 53.9% | 43.2% |
| 5 | B as written (Major finishes a Bloodied Boss) | 100% | 3.33 | 11.9% | 29.0% |
| 9 | B as written | 100% | 4.26 | 18.7% | 39.8% |
| 5 | B′ (strict dial: Major hinders too, never ends it) | 100% | 5.08 | 37.9% | 45.4% |
| 9 | B′ | 100% | 6.17 | 45.0% | 57.3% |

  - B′ is statistically the same as the bolt lane. B shortens a Boss fight by about one exchange at levels 5–9, because a 2-Fatigue Major working on a Bloodied Boss is the climax. That is the book's own III.3 ethos: a clever answer should matter more than a hit.
- **Why not "loses one attack"?** I tested it too. It is worth 5–15 HP per cast, 1.5–3× a bolt. Chained every exchange, it cut PC drops from 43% to 9% at level 5.
- **Mook and Standard** get the full effect, as in B/X *Sleep* against small HD. A bound Standard foe is worth about two fighter hits (8 HP at level 1) for 1 Fatigue. As in DW, the MM may say it breaks if it is harmed, which is fiction, not a new rule.
- **Engine:**
  - Add an intent flag (`control`) to `resolve_cast`.
  - On success against an Elite/Boss, set `state.hindered[enemy_key]` for this exchange.
  - `resolve_enemy_attack` treats `hindered` like `cover` (Hard, non-stacking).
  - `end_exchange` clears it.
  - A Major control on a Bloodied Elite/Boss sets `enemy.defeated = True` with `taken_out="working"`.
  - Mook and Standard: defeated or held, as today's MM ruling.
  - Tests: four role × Bloodied × scope cases, plus the non-stacking rule.

**Option C: HP threshold (13th Age, B/X *Sleep*).** A control working stops a foe only if its current HP is at most the scope's harm maximum (8 for Significant, 16 for Major) plus the damage bonus.
- It is elegant for mobs and M9.
- For Bosses it works only in the last 5–20% of their HP, and it needs arithmetic at the table.
- Keep it as a candidate for the M9 area-effect ruling, not for D5.

**Risks of the pick:**
1. The Bloodied-Major finish makes a level 5+ caster the Boss-closer. That costs 2 Fatigue at Hard, or Standard for a signature, and 29–40% of a Thaumaturge's daily budget. Strict tables can use B′. The recommendation is to print B and give B′ as the MM Note's dial.
2. "Stop outright" versus "just a stunt" is still an MM call. The full-form rule already says the MM rules scope before the roll, and this rule only adds duration.
3. The Elite rows were not simulated separately. The Elite has the same two attacks and 2× HP, so it should sit between Standard and Boss.

### D6. Is a working aimed at a foe an attack?

**Today:**
- The book is silent.
- `magic.resolve_cast` applies no level gap, cover, opening, stunt or Studied Foe.
- `combat_sim.py:175–176` privately exposes a caster on a 7–9. That breaks the CLAUDE.md iron law.

**Option A: fully an attack (REVIEW M5).** Level gap, cover, openings, stunts, **and** exposure on a 7–9, on top of the magic complication.
- A caster on 7–9 (25–42% of casts) pays twice: exposure plus a complication, when a fighter pays once.
- Mind presets are already the weakest (C1). **Rejected.**

**Option B: an attack for difficulty, magic for cost (Daggerheart, 5e spell attacks). THE PICK.**

> *A working aimed at a foe is an attack for everything that makes it Easier or Harder, and on a 7–9 one of the two costs offered is always that you are exposed.*

- **Level gap, openings, stunts, Studied Foe, Anatomist:** all apply, to harm *and* control, since "aimed at a foe" covers both.
  - Against a Boss 3+ levels up, a signature working drops from Easy to Standard. That is 91.7% at level 1 instead of 97%, and a non-signature working is at Hard, 83%.
  - The world is telling casters something too, which restores the level-gap rule's meaning.
- **Exposure becomes a choice, not a tax.**
  - Exposed, a Boss at attack +2 hits 94.9% (was 83.3%) and hard-hits 68.1% (was 41.7%).
  - A caster with a friend intercepting, or out of reach, can take exposure for free. That turns III.3's "Stand behind somebody" into a mechanical decision.
  - It also lets `combat_sim.py` delete its private rule: the engine offers the option and the sim's *policy* picks it.
- **Mooks:** a harming working that rolls 7+ drops a Mook, as an attack does. This settles M5's first bullet. Major against a mob is still M9's ruling.
- **Engine:**
  - `resolve_cast(enemy=…)` calls the same difficulty builder `resolve_attack` uses (level gap, opening, stunt, Studied Foe) before `resolve_roll`.
  - On a partial success, `complication_options = [EXPOSED] + roll_distinct(…, 1)`.
  - Choosing `EXPOSED` calls `state.expose(caster, enemy_key)`.
  - Tests: gap applied to a cast, opening consumed by a cast, exposure only when chosen, and the sim no longer calls `expose` itself.
- **Risks:**
  1. Studied Foe or a stunt now makes signature workings trivially Easy. The +4 bonus cap and the level gap limit this.
  2. *Counterspell* against foes stays moot, because foes don't cast. That is a separate minor ruling.

**Option C: not an attack (codify the engine).** Magic uses its scope difficulty only.
- Casters ignore the level gap and become the answer to "a foe six levels up". That contradicts III.3's Foe Level section.
- It is simple, but it keeps C2's hole. **Rejected.**

### D7. The casting budget doesn't grow with level

**Demand.** I assumed three fights a day, at the sim's mean Boss-fight length: 3.0 exchanges at level 1, 4.5 at level 5 and 5.5 at level 9. That gives about 9, 13.7 and 16.5 actions a day. Free slots come from the engine (`slots_free` on the built presets): the Thaumaturge has 5 at every level and the Invoker 7–8.

| Level | Today (Thaum) | A: +1 at 3/5/7/9 | B: +⌈level/2⌉ | C: +level |
|---|---|---|---|---|
| 1 | 5 (56%) | 5 (56%) | 6 (67%) | 6 (67%) |
| 3 | 5, **∞ with Arcane Mastery** | 6 | 7 | 8 |
| 5 | 5 (37%), **∞** | **7 (51%)** | 8 (58%) | 10 (73%) |
| 7 | 5, **∞** | 8 | 9 | 12 |
| 9 | 5 (30%), **∞** | **9 (55%)** | 10 (61%) | 14 (85%) |

The percentage is the share of the day's actions that can be Significant workings. Add 2–3 for the Invoker in every column. Wounds each take a slot, so a caster who drops loses one working, which is intended.

**Option A: one Fatigue-only slot at levels 3, 5, 7 and 9 (Knave, 13th Age slots, Maze Rats). THE PICK.**

> *A caster gains one slot that holds only Fatigue at levels 3, 5, 7 and 9.*

- **What it does:** it keeps the caster's share of the day at about 50–55% from level 1 to 9, which is the level 1 feel preserved as fights lengthen. There is nothing new to track: the sheet shows up to 4 extra boxes marked "Fatigue only".
- **Paired change (talent text, not a new rule):** *Arcane Mastery* becomes "Once per scene, one signature working costs 1 less Fatigue."
  - With about 3–4 scenes a day, that is worth about 3–4 Fatigue a day.
  - The Invoker's *Miracle* saves 2 Fatigue once a session.
  - The two traditions are near parity at level 3 and neither is infinite.
- **Engine:**
  - `magic.fatigue_slot_levels: [3,5,7,9]` in `facet.yaml`.
  - `Character.fatigue_capacity = slots_free + fatigue_only`, with Fatigue filling the Fatigue-only slots first.
  - `plan_cast` checks against that capacity.
  - *Arcane Mastery* gets `use: once_per_scene`, and the "improved casting talent" reduction does not stack with it on one working (one `steps` guard).
  - Tests: capacity by level, fill order, the Arcane Mastery once-per-scene limit, and no stacking.
- **Risks:**
  1. It widens the gap between casters and non-casting Mind/Soul presets. C1 must be fixed on its own track.
  2. If the MM runs more than three fights a day, casters are scarcer. That is the dial, and it is OSR-correct.

**Option B: +1 Fatigue-only slot per two levels (+⌈level/2⌉).** This works too, but it gives a level 1 caster a sixth working, and the stated problem is growth, not the starting budget. It is a bit rich at level 9 (61%).

**Option C: the breather clears 1 Fatigue.** It doesn't scale with level. Breathers are also unlimited today (the REVIEW engine finding), so this would make Fatigue infinite until that is fixed. **Rejected.** A slot count equal to the level (column C) overshoots to 85% at level 9 and is also rejected.

---

## Part 4: The Archive Guardian beat, rewritten so the rules reproduce it

These are changes only to III.3's *In Play: The Archive's Guardian*. It introduces no new canon: same room, same card (level 1 Boss scaled down, 32 HP, armor 2, attack +1, damage 4, two attacks, morale 12, Bloodied at 16), same characters, same objects. Exchange 1 is unchanged (32 → 23 → 20; Mordai 16 → 15; Zulnut 12 → 7). Exchange 3 is unchanged apart from the lines noted.

**Exchange 2.** From Zahna's working onward, replace with:

> **Zahna:** "I seal its knee. It's a hinge. A hinge is just a door that doesn't know it."
>
> (The MM laughs, which is a ruling of sorts.)
>
> **MM:** "That's your signature working, the sealing glyph. Significant, and aimed at it, so it's an attack: you're both level 1, no gap. One step Easier for the signature. *Arcane theory* fits. One Fatigue. And it's a Boss: a glyph will hold it for this exchange, not for good."
>
> → Zahna rolls **2d6 + Mind (+2) + knack (+1)** at Easy (+1) and gets a **10**. Full success.
>
> **MM:** "The glyph closes over the joint like a lock clicking home. It can swing. It cannot step, not this exchange. Its blows are Hard, though Mordai's guard had already made them Hard, so what you've really bought is that it can't reach you." *Zahna fills a slot with Fatigue.*

The Guardian's two attacks on Mordai follow as printed: the natural 12 splits the shield, and the natural 2 gives the opening.

**Exchange 3.** Replace the opening line with:

> **MM:** "Third exchange. The glyph cracks off its knee at the turn of the exchange. A Boss doesn't stay bound. It can step again, but Mordai is standing between it and Zahna, so it swings at what it can reach: Mordai, and Zulnut."

In the Bloodied narration, replace "The sealed knee tears free of your glyph with a sound like a vault door, and it abandons its post" with: "It stops guarding and abandons its post."

**Exchange 4.** Replace from "Fourth exchange" to the end of the fight with:

> **MM:** "Fourth exchange. It's free, and it knows who sealed the knee. Both arms, at Zahna."
>
> **Zulnut:** "I climb it. I get on its back and hold the chest plate open for Zahna. That's Help."
>
> **Zahna:** "And I rewrite the instruction. Not *hold this room*. *Your watch is over.*"
>
> **MM:** "A person bound, near enough, so Significant. It's Bloodied, but to end a Boss with one working you'd need Major, and that's level 3. At Significant it takes for one exchange: it hesitates, and its blows come in Hard. Not a signature, so Standard. *Arcane theory* fits, Zulnut's Help adds a die, and it's another point of Fatigue."
>
> → Zahna rolls **3d6 + Mind (+2) + knack (+1)**, keeping the best two, at Standard and gets a **13**. Full success.
>
> *The glyphs across its chest rearrange under Zahna's hand, and the light in its eyes dims. Not out. Dimmed.*
>
> **Mordai:** "Then I finish the argument. The shoulder."
>
> → Mordai rolls **2d6 + Body (+2) + knack (+1)** at Standard and gets a **9**. Partial success.
>
> *The d10 shows 6, less 2: 4 damage. 11 down to 7. Mordai is exposed, but it isn't swinging at him.*
>
> *It swings at Zahna, twice, at Hard (+1 −1): 3 and 2, a 5; then 4 and 2, a 6. Two misses. Without the rewrite, the second would have been a 7 and a hit.*
>
> ---
>
> **MM:** "Fifth exchange. It's slow now, but it still has one instruction left, and it's pointed at Zahna."
>
> **Mordai:** "Same shoulder."
>
> → Mordai rolls **2d6 + Body (+2) + knack (+1)** at Standard and gets an **11**. Full success.
>
> **Mordai:** "Extra d6."
>
> *The d10 shows 5 and the d6 shows 4: 9, less 2 is 7. The guardian goes from 7 to 0.*
>
> **MM:** "It never gets to swing. Your blow happened first. And because of what Zahna wrote, it doesn't break. It settles to one knee, then both, with the deliberate patience of something that has reached the end of its instructions."

The existing dialogue follows unchanged ("Is it safe to get down?" … "extremely on brand").

**The arithmetic line** becomes:

> *The arithmetic, for anyone checking: the guardian went 32, 23, 20, 11, 7, 0, and was Bloodied at 16 on the way. Mordai went 16, 15, 12, 8, and lost his shield. Zulnut went 12 to 7 and lost his knife. Zahna was never hit, and carries 2 Fatigue in his slots until he sleeps.*

**What it teaches:**
- A working aimed at a foe is an attack (D6).
- Control on a Boss holds one exchange and makes its blows Hard, and Hard doesn't stack (D5).
- Ending a Bloodied Boss with a working is a level 3+ Major (D5).
- The telegraph still matters.
- The magic still gets the story's last word through the narration, without a rule granting it the kill.

---

## Part 5: Licence table

| Game | Licence (as found) | Use in Facets |
|---|---|---|
| D&D 5e SRD 5.1 | CC BY 4.0 | Wording usable with attribution (none used) |
| Knave | CC BY 4.0 | Wording usable with attribution |
| Ironsworn SRD / assets | CC BY 4.0 (books CC BY-NC-SA 4.0) | SRD wording usable; books ideas only |
| Cairn | CC BY-SA 4.0 | Wording usable with attribution and share-alike; credit Fatigue-in-slots |
| Ars Magica 5e | Open licence (I believe CC BY-SA 4.0; unverified) | Concept only, per the brief |
| Dungeon World | CC BY 3.0 | Ideas only (brief admits 4.0 only; III.1 already has a verbatim finding) |
| Fate Core SRD | CC BY 3.0 | Ideas only |
| Blades in the Dark SRD | CC-licensed (I believe CC BY 3.0) | Ideas only |
| OSE / BFRPG (B/X), 13th Age, DCC | OGL 1.0a (DCC also ORC-aligned) | Ideas only |
| Shadowdark | Shadowdark Third-Party License | Ideas only |
| Troika! | Troika third-party licence | Ideas only |
| Cypher / Numenera / Invisible Sun | CSOL / proprietary | Ideas only |
| Daggerheart | DPCGL | Ideas only |
| Mage, Whitehack, Maze Rats | Proprietary / none stated | Ideas only |

All three recommended sentences and the vignette rewrite are original wording. The borrowed ideas should be credited in the corrected Credits: 13th Age (HP-gated control), Ironsworn (rank-sized progress), Daggerheart (a spell that hurts is an attack), Knave (budget by level) and Cairn (Fatigue in slots).

---

## Open questions for Brain / the owner
1. Should B or B′ (a Major working ends a Bloodied Boss, or only hinders it) be the printed default? The research favours B, with B′ as the MM dial.
2. Is *Arcane Mastery* once per scene enough, or should it also become shared with Soul, like *Wider Domain*? M7 notes the Invoker can't reach it without a teacher.
3. Area control against mobs (M9): Option C's HP threshold is a candidate there.
4. These picks do not fix C1 (non-caster Mind/Soul presets). D7 slightly widens the caster versus non-caster gap.
