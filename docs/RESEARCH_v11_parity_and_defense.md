# RESEARCH: v1.1 Facet parity, protection, reach and custom classes

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` · **Status:** complete (research tier; no repo code or book edited)
**Inputs:** `docs/REVIEW_lean_facets.md`; `docs/REVIEW_lean_design.md` §C1, M1, M4, M6; `software/facets/base/facet.yaml` (`facets`, `talents`, `classes`, `combat`, `equipment`); `player_handbook/III.3_Combat.md`; `player_handbook/II.4_Character_Creation_Facets.md`; `software/tools/combat_sim.py`.
**Decisions covered:** D1 Facet parity in a fight · D2 protection vs the telegraph · D3 reach and engagement · D4 custom classes and armor.

---

## 0. Summary

Well-regarded games answer all four problems with ideas we can take on without adding rules. In most cases we replace one sentence.

| # | Recommendation (the pick) | Rule count | Evidence it works (our engine) |
|---|---|---|---|
| **D1** | **Attack with your Facet's stat, not Body.** Also three number changes: Mind grit **d8**, light armor in the four unarmored kits, and a caster's staff blow as their "cantrip". | One sentence replaced, no rule added | Mind non-casters' solo win rate goes from 21/7/0% to 77/90/51% at L1/5/10. An all-Mind party goes from 77/66/61% to 100% in the standard fight. Body stays at 96–100%. |
| **D2** | **Intercept takes one telegraphed attack aimed at an ally. Sentinel takes one attack from each of two different foes.** | Two sentences reworded | Allies down vs a L5 Boss: Guardian attacking 53%, today's Sentinel 2%, pick 18%. The Boss's second attack still has to be answered. |
| **D3** | **Engaged is defined by the telegraph.** A foe that telegraphs a hand-to-hand attack at you closes and engages you unless the fiction stops it. Exposure hits your next incoming attack from any foe. Shooting or casting while engaged is Hard. Delete "casters out of reach are out of its attacks". | One definition added, one sentence deleted, three references reworded | This is how `combat_sim.py` already behaves, so MM1's calibration assumed it all along. Archers stop being untouchable. |
| **D4** | **Put armor in the Facet row**: Body heavy + shield, Soul light + shield, Mind light. Heavier armor than your Facet's makes your attacks and workings Hard; this replaces the heavy-armor Fatigue rule. **One of a custom class's two starting talents may come from any Facet's menu** (never a casting talent). | One rule replaced, one table row, one sentence | Once D1 lands, an ungated Mind Tactician in heavy armor and shield reaches 100/99/95%, level with a Warrior. The gate keeps it at 94/95/88%. |

**The four picks depend on each other. Adopt them together.**
- **D1 makes D4 mandatory.** Once Mind attacks with Mind, heavy armor is the only thing between a Mind build and a Warrior.
- **D2 and D3 share one concept.** "Engaged / can get there" is the word Intercept needs.
- **All four together make fights easier.** The default party's per-PC Boss drop rate falls from 18–42% to 6–9% for the casters, so MM1's monster numbers need retuning afterwards (§6, risks).

**Caveat on community evidence.** The session's WebSearch budget ran out, and Reddit, RPG.SE and ENWorld refused fetches. Play evidence therefore comes from designer blogs and columns (Strandberg, Heinsoo, Pelgrane), build guides (RPGBot), published reviews and award records. Forum sentiment is thin, and every such gap is marked below. The rules claims are all from SRDs or primary rules data.

---

## 1. How this was measured

**Engine and harness.** Every number comes from the real engine (`app.game.combat`, `app.game.magic`, `app.game.character`), driven by throwaway policy drivers in the session scratchpad:
- `lab.py`, `solo.py`, `solo2.py`, `party.py`, `guard.py`, `guard2.py`, `armor.py` and `math.py`;
- each is a deep copy of the ruleset or a policy parameter;
- the drivers add no repo code.

**How proposed rules were emulated.** Two things were emulated in *policy* only:
- the attack stat, passed through `resolve_attack(stat=...)`;
- Intercept targeting, done by redirecting the telegraphed attack.

This is exploration of a proposed rule. If a rule is adopted it must go into `combat.py`, and the simulator must not carry it (CLAUDE.md iron law).

**Setup.** 300–600 trials per cell. Solo tests run with morale off; Boss and party tests run with morale on, as in the design review.

**The same sim limits as the design review apply:**
- no Help, Sparks or Defend unless stated;
- random enemy targets;
- +1d6 on every 10+.

Variants marked "+knack" give every attack the +1 knack, which is how a fighting preset actually plays.

### 1.1 2d6 odds (Standard; Hard = −1, Easy = +1; an extra die = keep the best two)

| Modifier | 10+ | 7–9 | 6− | Hit (7+) | Hit with an extra die |
|---|---|---|---|---|---|
| −1 | 8% | 33% | 58% | 42% | 68% |
| +0 | 17% | 42% | 42% | 58% | 81% |
| +1 | 28% | 44% | 28% | 72% | 89% |
| +2 | 42% | 42% | 17% | 83% | 95% |
| +3 | 58% | 33% | 8% | 92% | 98% |
| +4 (cap) | 72% | 25% | 3% | 97% | — |

The attack-stat gap is the difference between +0 and +2 (+3 from level 4). That moves the hit rate from 58% to 83–92%, and the 10+ rate from 17% to 42–58%. On a three-tier chassis the stat is the biggest lever there is: it moves both thresholds at once.

### 1.2 Expected damage per attack vs armor 1 (Standard; the 10+ pick is +1d6; minimum 1)

| Level (bonus) | Die | Stat +0 | +1 | +2 | +3 |
|---|---|---|---|---|---|
| 1 (+0) | d6 | 2.11 | 2.85 | 3.61 | 4.39 |
| 1 (+0) | d8 | 2.68 | 3.56 | 4.43 | 5.29 |
| 1 (+0) | d10 | 3.25 | 4.27 | 5.25 | 6.20 |
| 5 (+1) | d6 | 2.62 | 3.50 | 4.38 | 5.25 |
| 5 (+1) | d8 | 3.21 | 4.22 | 5.21 | 6.17 |
| 5 (+1) | d10 | 3.79 | 4.94 | 6.04 | 7.08 |
| 10 (+3) | d6 | 3.79 | 4.94 | 6.04 | 7.08 |
| 10 (+3) | d8 | 4.38 | 5.67 | 6.88 | 8.00 |
| 10 (+3) | d10 | 4.96 | 6.39 | 7.71 | 8.92 |

**Preset damage per action, today vs the D1 pick.**
- Assumptions: the Facet stat is +2 at L1 and +3 from L4. The Warrior uses a d10 through Weapon Master. The Investigator and Physician use d6. The Thaumaturge's staff is d8.

| Preset | L1 | L5 | L10 | Share of the Warrior (today → pick) |
|---|---|---|---|---|
| Warrior (Body, d10) | 5.25 | 7.08 | 8.92 | 100% |
| Investigator / Physician, today (Body +0, d6) | 2.11 | 2.62 | 3.79 | 40% / 37% / 42% |
| Investigator / Physician, pick (Mind, d6) | 3.61 | 5.25 | 7.08 | **69% / 74% / 79%** |
| Thaumaturge staff, pick (Mind, d8) | 4.43 | 6.17 | 8.00 | **84% / 87% / 90%** |

Body keeps a real damage edge of 10–30% from its die, and on top of that it keeps HP, armor and its fighting talents.

**Monster side.** A monster has 5 + 3×level HP, deals 3 + level damage, and attacks at +1/+2/+4 (L1/5/10). Expected damage per Standard attack:

| Level | Armor 0 | Armor 0, exposed | Armor 1 | Armor 1, exposed | Armor 3 | Armor 3, Hard |
|---|---|---|---|---|---|---|
| 1 | 3.44 | 4.62 | 2.72 | 3.73 | 1.28 | 0.92 |
| 5 | 7.50 | 8.95 | 6.67 | 8.00 | 5.00 | 4.17 |
| 10 | 14.08 | 14.73 | 13.11 | 13.73 | 11.17 | 10.33 |

At L10 a +4 foe almost never misses. Exposure, Defend and cover are worth only about 0.6–1 HP there, compared with 1–1.5 HP at L1–5. This is design review M8's flattening, and it limits how much D2 and D3 can matter at high level.

---

## 2. Per-game findings

Each game gets: the concept (in our words), what keeps it simple, and evidence of play. Licences are in §7.

### 2.1 D&D 5e (2014 SRD 5.1 / 2024 SRD 5.2)

**Attack stats**
- Melee attacks use Str and ranged attacks use Dex. The **Finesse** tag lets a weapon use either, but the same stat goes on attack and damage. https://roll20.net/compendium/dnd5e/Weapons
- Every caster class has one fixed casting stat (Int, Wis or Cha), and it feeds both the spell attack and the save DC. https://roll20.net/compendium/dnd5e/Spellcasting

**Cantrips: the caster's always-on attack**
- A damage cantrip is free, unlimited, keyed to the casting stat, and scales with *character* level. Fire Bolt goes from 1d10 to 4d10. https://roll20.net/compendium/dnd5e/Fire%20Bolt
- RPGBot: a longbow beats a cantrip early, but later a cantrip outdamages most 1st and 2nd level spells against one target. https://rpgbot.net/dnd5/characters/classes/wizard/
- **Lesson:** a caster needs one reliable attack that costs nothing. Otherwise the resource economy decides whether the caster plays at all.

**Protecting others**
- **Protection (2014, in SRD 5.1):** a reaction that imposes disadvantage on one attack against an adjacent ally, and needs a shield. https://roll20.net/compendium/dnd5e/Fighter
- **2024 Protection** extends that to the ally until your next turn. **Interception** reduces one hit by 1d10 + proficiency. http://dnd2024.wikidot.com/feat:protection · http://dnd2024.wikidot.com/feat:interception
- **Sentinel** punishes the attacker with an opportunity attack and speed 0, and it spends the same **one reaction per round**. https://dnd5e.wikidot.com/feat:sentinel · http://dnd2024.wikidot.com/feat:sentinel
- **What limits all of them:** one reaction per round, plus 5-ft adjacency.
- **Play evidence (RPGBot):** Protection and Interception are "situational", because the ally has to stay next to the tank. Sentinel is "essential for defenders". Punishing the attacker is judged better than softening the hit. https://rpgbot.net/dnd5/characters/classes/fighter/
- **Lesson:** protection in a well-regarded design covers **one attack**. It never covers every attack.

**Armor**
- Armor is a hard class gate. Fighters get every armor; wizards get none. https://roll20.net/compendium/dnd5e/Fighter · https://roll20.net/compendium/dnd5e/Wizard
- Wearing armor you aren't proficient in gives disadvantage on Str/Dex rolls and **stops you casting**. https://roll20.net/compendium/dnd5e/Armor
- **Play evidence:** casters get around the gate with spells (Mage Armor, Shield), not with armor feats (RPGBot wizard guide, above). The gate holds, and nobody complains about it.

**Martial/caster disparity**
- The widely known complaints ("linear fighters, quadratic wizards"; cantrips outscaling weapons) **could not be sourced from forums this session.** Only RPGBot's cantrip note above is cited.

### 2.2 13th Age (Archmage Engine SRD)

**Attacks**
- Every class has basic melee and ranged attacks with the same shape: stat + level against a defense. Casters simply swap in their stat.
  - The cleric's Javelin of Faith rolls Wis against PD.
  - The wizard's Magic Missile always hits.
  - https://www.13thagesrd.com/classes/cleric/ · https://www.13thagesrd.com/classes/wizard/
- A melee miss still deals damage equal to your level, so a turn is rarely wasted. https://www.13thagesrd.com/classes/fighter/

**Armor**
- AC comes from a **per-class table**. A wizard in heavy armor gets AC 11 and −2 to attacks and spells: a *soft* gate. https://www.13thagesrd.com/classes/wizard/

**Engagement and range**
- There are three abstract states: **engaged, nearby and far away**. https://www.13thagesrd.com/combat-rules/
- Making a ranged attack or casting while engaged provokes an opportunity attack.
- Leaving an engagement takes a disengage save.

**Protecting others**
- The fighter's **Skilled Intercept** is an 11+ save that redirects *one* attack aimed at a nearby ally. In heavy armor that hit does half damage. https://www.13thagesrd.com/classes/fighter/

**Escalation die**
- It adds +1 per round, up to +6, to PCs only, and was built to stop fights dragging.
- https://pelgranepress.com/2015/11/13/13th-sage-secret-origins-of-the-escalation-die/ · https://pelgranepress.com/2014/08/07/13th-sage-escalation-for-everyone/

**Reception**
- 13th Age won the 2014 Silver ENnie for Best Rules. https://en.wikipedia.org/wiki/13th_Age

**Lessons**
1. Every class has a basic attack on its own stat.
2. Engaged is a binary, and shooting or casting while engaged has a cost.
3. Interception takes **one** attack.
4. Armor is gated by class, softly.

### 2.3 Dungeon World (SRD)

**Damage and attack stats**
- **The class sets the damage die**: fighter d10, wizard d4. Weapons contribute tags only (*precise* means you attack with Dex). Armor is flat damage reduction, the closest match to our system. https://www.dungeonworldsrd.com/playing-the-game/ · https://www.dungeonworldsrd.com/equipment/
- **Hack and Slash** (Str) costs you the enemy's counterattack on a 7–9. **Volley** (Dex) makes you choose on a 7–9: move into danger, deal −1d6, or use extra ammo. Ranged has its own price. https://www.dungeonworldsrd.com/moves/

**Protecting others: Defend**
- Defend (Con) gives a **budget** of 1 or 3 hold. You spend it to redirect, halve, retaliate or give an ally a bonus, and you lose it when you move away. https://www.dungeonworldsrd.com/moves/
- **Play evidence (Jeremy Strandberg, Stonetop's designer):**
  - The trigger and when you may spend hold are ambiguous.
  - GMs escalate threats when hold is spent.
  - One option is almost never used.
  - He rewrote the move as "Readiness", with explicit conditions for losing it.
  - https://spoutinglore.blogspot.com/2018/12/defend.html · https://spoutinglore.blogspot.com/2018/07/homebrew-world.html
- **Lesson:** a spendable protection pool is good in principle, but it is fiddly unless its limits are explicit. Our lighter version is "one attack".

**Range**
- Range tags (hand, close, reach, near, far) are yes/no checks against the fiction, not modifiers. https://www.dungeonworldsrd.com/equipment/
- Strandberg: positioning decides *whether* a move triggers at all. https://spoutinglore.blogspot.com/2020/03/running-fights-in-dungeon-world-stonetop.html

**Reception**
- ENnie Gold for Best Rules 2013, and Golden Geek RPG of the Year 2012. https://en.wikipedia.org/wiki/Dungeon_World

### 2.4 Shadowdark

**Rules**
- Str for melee, Dex for ranged, and the better of the two with a finesse weapon. https://github.com/Muttley/foundryvtt-shadowdark/blob/develop/system/src/models/PlayerSD.mjs
- The class hard-gates HP die and armor: fighter d8 and any armor; priest d6 and any armor; thief d4 and leather or mithral; wizard d4 and no armor. https://github.com/Muttley/foundryvtt-shadowdark/tree/develop/data/packs/classes.db
- Casting is a check. A failed cast loses the spell until rest.
- Ranges are three words: Close, Near and Far. https://github.com/Muttley/foundryvtt-shadowdark/blob/develop/i18n/en.yaml

**Evidence of play**
- Four gold ENNIEs in 2024, including Best Rules. https://en.wikipedia.org/wiki/Shadowdark
- The Quickstart is rated about 95% five-star. https://www.thearcanelibrary.com/products/shadowdark-rpg-quickstart-set-pdf
- No reachable critique of its armor gate was found.

**Lessons**
- A hard armor gate by class is accepted in the most successful recent old-school game.
- It does **not** solve D1: its wizards fight only with spells.

### 2.5 Knave (1e)

**Rules**
- Knave is classless, and anyone uses any gear. What you carry decides your role.
- Melee attacks use Str. **Ranged attacks use Wis**, a small precedent for a non-physical stat doing the attacking.
- Armor is priced in slots, and spellbooks compete for the same slots. https://questingbeast.itch.io/knave · https://rancourt.substack.com/p/analysis-knave-2e

**Evidence of play**
- Rancourt: slot management "feels like a hassle". https://rancourt.substack.com/p/analysis-knave-2e
- Gundobad praises 2e's wounds-in-slots rule. https://gundobadgames.blogspot.com/2023/04/lets-read-knave-2e-kickstarter-preview_27.html

**Lesson for D4.** Pricing armor in slots only works when slots are very tight. Ours aren't: the design review measured the Physician going from 49% to 90% in heavy armor and a shield.

### 2.6 Cairn (1e / 2e)

**Rules**
- There is no attack roll. The attacker rolls the weapon die and armor subtracts from it.
- Armor is capped at 3 for everyone.
- Anyone can cast by reading a spellbook, and each cast adds a Fatigue that fills a slot.
- https://cairnrpg.com/first-edition/cairn-srd/ · https://cairnrpg.com/second-edition/wardens-guide/combat/

**How it answers "who fights"**
- Because nobody rolls to hit, gear alone decides who is effective. That can't transfer to a 2d6 attack roll.

**Evidence of play**
- It is deadly: characters "drop like flies" if played casually. https://deathtrap-games.blogspot.com/2021/12/game-review-cairn.html
- Our Fatigue-in-slots comes from Cairn (the credits fix noted in the consolidated review).

### 2.7 The Black Hack

**Rules**
- Rolls are d20 roll-under. Players roll attacks (Str melee, Dex ranged) and also roll to **avoid** monster attacks.
- Classes set HP and damage.
- **Soft armor gate:** wearing armor your class doesn't allow adds its armor points to your attack and avoid rolls, which is a heavy penalty.
- Ranges are Close, Nearby, Far-Away and Distant.
- https://the-black-hack.jehaisleprintemps.net/english/

**Lesson for D4.** A soft gate that makes armor you aren't trained for a combat penalty is long-proven and costs one sentence.

### 2.8 Fate Accelerated / Fate Core

**Rules**
- In FAE, Attack is an *action*, and any of the six approaches can perform it if the description fits. https://fate-srd.com/fate-accelerated/how-do-stuff-outcomes-actions-and-approaches
- The SRD itself warns that players will reach for their best approach, and relies on the fiction to stop it.
- RPG.SE's top answer on shooting accepts Flashy or Forceful attacks depending on context. https://rpg.stackexchange.com/questions/50585
- Fate Core attacks only with the Fight and Shoot skills. https://fate-srd.com/fate-core/fight
- Zones replace distance. https://fate-srd.com/fate-core/setting-scene

**Evidence of play**
- A top RPG.SE answer blames slow fights on too much defense and too little offense. https://rpg.stackexchange.com/questions/26549

**Lesson for D1.** "Any stat the fiction supports" collapses into "your best stat", and it costs a negotiation on every roll. Naming the stat once, by Facet, gets the same result without the argument.

### 2.9 Daggerheart (SRD 2.0)

**Rules**
- **Every weapon names the trait it attacks with**, and every trait has a mundane weapon. The quarterstaff uses Instinct, the rapier Presence, the twisted dagger Knowledge.
- A damaging spell counts as an attack. Each subclass sets its spellcast trait.
- Armor has no class gate. Heavy armor costs Evasion, and Mage Robes scale with the spellcast trait.
- The Guardian's protective role comes from its features: soaking hits for nearby allies, and taking one near-fatal hit for an ally.
- Ranges are five bands.
- https://www.daggerheart.com/wp-content/uploads/2026/08/DH_SRD_2_2026_08_25.pdf (pp. 9, 18–19, 48, 55–57, 72)

**Evidence of play**
- One reviewer says open armor "heavily reduces combat roles", then says in play it is "only partially true". https://solottrpg.substack.com/p/daggerheart-my-thoughts-and-ramblings
- GamingTrend calls the armor and damage rules "overcomplicated". https://gamingtrend.com/reviews/daggerheart-review-more-than-a-heartbreaker/
- ENWorld's review thread praises the SRD's clear wording. https://www.enworld.org/threads/daggerheart-review-the-duality-of-robust-combat-mechanics-and-freeform-narrative.713471/

**Lesson for D1.** It is the strongest current precedent for letting every character attack with its own stat. Putting the stat on the weapon, though, costs a table column and a lookup per weapon; our Facets already provide one stat per character.

### 2.10 Blades in the Dark (SRD)

**Rules**
- **Position** (controlled, risky, desperate) replaces range and reach bookkeeping. The GM reads distance into each roll's position and effect. https://bladesinthedark.com/action-roll
- A mystic who hurts a foe with Attune rolls exactly as a brawler does with Skirmish. https://bladesinthedark.com/actions-attributes
- **Protect** moves a teammate's consequence onto you. Resisting it then costs stress, a finite track. https://bladesinthedark.com/teamwork · https://bladesinthedark.com/resistance-armor

**Lessons**
- Protection *transfers* harm and is paid for from a finite resource. It never deletes harm.
- Range is fiction read into each roll.
- Play evidence could not be fetched this session.

### 2.11 Cypher System (CSRD)

**Rules**
- There are three pools: Might, Speed and Intellect. Edge makes spending cheaper, and Effort eases a task.
- Heavy weapons use Might; light and ranged weapons use Speed. The Adept's Onslaught attacks from Intellect.
- Only players roll: they roll to attack and they roll to defend.
- Four range bands.
- Armor is gated by a running cost: it makes Speed Effort more expensive, and training eases that.
- https://callmepartario.github.io/og-csrd/ · https://www.montecookgames.com/cypher-system-open-license/

**Lesson.** Every type has a signature attack on its own pool. Pricing armor as a cost on a *different* resource is elegant, but it needs pools we don't have.

### 2.12 ICRPG

**Rules**
- Everyone rolls the same d20 + stat against the room's one Target number.
- **The tool sets the effect die**: basic d4, weapon d6, gun d8, magic d10, ultimate d12. Nobody lacks an attack.
- The build comes mostly from loot.
- The rules are proprietary; these references are fan tools. https://github.com/ClipplerBlood/icrpgme

**Lesson.** One roll for everyone, with the tool setting what a hit does. That matches our weapon-die model once the attack stat stops being Body-only.

### 2.13 Draw Steel (MCDM)

**Attacks**
- The power roll is 2d10 + characteristic with three tiers: ≤11, 12–16, 17+. Attacks can't miss.
- **Every class has a free signature ability on its own characteristic.** The Conduit rolls Intuition; the Censor's Judgment scales with Presence.
- https://github.com/SteelCompendium/data-unified (heroes: power-roll, signature-ability, conduit, censor)

**Protecting others**
- Protective abilities *reduce or redirect* damage and never erase it.
- The Tactician's Parry halves one hit on an adjacent ally.
- Taunted adds a penalty to attacking anyone else; it doesn't forbid it.
- Mark tracks one creature at a time.

**Engagement**
- Engagement is a binary (adjacent), with a free strike on a careless exit.

**Lessons.** A free attack on your own stat. Protection that reduces damage or covers one foe, never all of them. A binary engaged state.

### 2.14 Ironsworn (Datasworn, CC BY 4.0)

**Rules**
- **Strike** and **Clash** use Iron in close quarters and Edge at range. Shooting at a foe that is advancing on you is a Clash, so an archer under pressure still pays the price. https://github.com/rsek/datasworn/blob/main/source_data/classic/moves.yaml
- *Face Danger* and *Battle* accept any stat chosen by method.
- Initiative (in control vs in a bad spot) replaces range bookkeeping.

**Lesson for D3.** A foe that closes on you makes you pay, whatever weapon you hold. That is exactly "the telegraph engages you".

### 2.15 PbtA stat swaps (Monster of the Week)

**Rules (from the community sheet text)**
- A playbook move lets a character attack with a non-Tough stat: the Spooky's Big Whammy uses Weird, with a magical backlash on a miss.
- Protecting someone always costs the protector harm.
- https://github.com/Roll20/roll20-character-sheets/blob/master/Monster%20of%20the%20Week/translation.json

**Lesson.** The "keep Body, give a talent" route to D1 works, but it spends a playbook move (for us, a talent pick) on letting a character fight at all.

### 2.16 Cross-game patterns

1. **Every well-regarded game gives every character a reliable attack on a stat it actually invests in.** 13th Age, 5e cantrips, Draw Steel signatures, Daggerheart, FAE, Cypher and ICRPG all do. Only Shadowdark and The Black Hack keep casters on a spell roll, and their non-caster classes are all combat-capable.
2. **Protection is bounded per round**, by:
   - one reaction (5e);
   - one attack (13th Age);
   - a hold budget (Dungeon World);
   - finite stress (Blades);
   - halving (Draw Steel, 13th Age heavy armor).

   None of them lets one character absorb every attack on every ally.
3. **Range is one binary or a few bands, and ranged always has a price when a foe closes**: an opportunity attack (13th Age), Clash (Ironsworn), Volley's 7–9 menu (Dungeon World), position (Blades).
4. **Armor is gated by class almost everywhere.** It is hard in 5e and Shadowdark and soft in 13th Age and The Black Hack. Classless games price it instead: Knave and Cairn in slots, Cypher in Speed. Daggerheart is the open exception, and reviewers flag roles as the risk.

---

## 3. D1 — Every Facet contributes in a fight

**The problem.** `III.3:29` says "An attack is 2d6 + Body". Mind stacks four penalties on top of that: a d6 grit die, Body +0 on HP, no armor in its kits, and Body-rolled attacks.

### Options

**D1-A. Attack with your Facet's stat.** *(The pick.)* Replace "2d6 + Body" with "2d6 + your Facet's stat". Body still rolls Body.
- **Precedent:** 13th Age, Draw Steel, Cypher, ICRPG, and FAE in practice.
- **Rule count:** one sentence replaced.
- **Niche identity:** kept by the grit die, the armor gate (D4), Body's fighting talents (Weapon Master, Cleave, Marksman, Unstoppable, Whirlwind, Deadeye) and weapon dice.

**D1-B. The weapon names the stat** (Daggerheart, 5e Finesse, Dungeon World *precise*). For example:
- standard and heavy weapons use Body;
- light and ranged weapons use Body or Mind;
- staves and foci use Mind or Soul.

It gives flavourful hybrids (a Soul duelist with a rapier), but costs a table column and a lookup per weapon. It also leaves Soul's mapping arbitrary: Presence as a sword stat reads well in Daggerheart, but only because it has six traits.

**D1-C. Keep Body and give Mind and Soul fighting talents** (MotW's Big Whammy, the design review's "Studied attack" and "Rallying strike").
- It protects Body's niche most strongly.
- It adds one talent per Facet at least, and taxes every Mind or Soul custom class a pick just to be allowed to fight. That is the opposite of agency.

**D1-D. The fiction picks the stat** (FAE, Ironsworn Face Danger).
- The FAE SRD itself warns that players will reach for their best approach.
- It becomes D1-A with a negotiation on every roll.

### Measured (solo win rate vs one same-level Standard foe; L1 / L5 / L10)

| Variant | Warrior | Brawler | Thaum | Investigator / Physician | Tactician | Invoker | Speaker | Wanderer | Captain |
|---|---|---|---|---|---|---|---|---|---|
| Today (Body, no knack) | 100/100/100 | 93/98/99 | 61/33/8 | 21/7/0 | 73/36/37 | 87/63/46 | 29/10/2 | 55/30/22 | 90/64/66 |
| Today + knack | 100/100/100 | 96/99/100 | 61/33/8 | 32/15/2 | 80/47/56 | 87/63/46 | 49/20/6 | 65/48/39 | 96/82/84 |
| A: Facet stat + knack | 100/100/100 | 96/99/100 | 61/33/8 | 58/59/13 | 87/80/72 | 87/63/46 | 76/67/43 | 80/86/54 | 98/96/95 |
| A + casters use the staff blow | same | same | 82/75/42 | 58/59/13 | 87/80/72 | 94/95/87 | 76/67/43 | 80/86/54 | 98/96/95 |
| A + staff + light armor in the 4 unarmored kits | same | same | 82/75/42 | 76/61/24 | 87/80/72 | 94/95/87 | 77/90/51 | 91/92/76 | 98/96/95 |
| **Pick: the above + Mind grit d8** | 100/100/100 | 96/99/100 | **84/94/68** | **77/90/51** | **94/95/87** | 94/95/87 | 77/90/51 | 91/92/76 | 98/96/95 |

Scout and Guardian stay at 99–100% throughout.

**Party level (3 Standard + 2 Mooks, morale off; win / any PC down).**
- All-Mind: 77% / 79%, 66% / 82%, 61% / 90% today → **100% / 20%, 100% / 4%, 100% / 14%** with the pick.
- All-Soul: 98% / 37% → 100% / 10%.
- All-Body: unchanged at 100% / 0–1%.

**Default party vs a same-level Boss (per-PC down, today → pick).**
- Thaumaturge: 36 / 28 / 42% → 9 / 7 / 6%.
- Invoker: 18 / 18 / 17% → 7 / 8 / 7%.
- Warrior: 0–2% in both.

### Recommendation: D1-A plus three number changes

1. **Rule:** "An attack is 2d6 + your Facet's stat." Body still rolls Body for Hold On, climbing and forcing.
2. **Numbers** (in `facet.yaml`, no new rules):
   - Mind's grit die goes from d6 to **d8** (average 5). This is the design review's d10/d8/d8.
   - The Investigator, Physician, Speaker and Wanderer kits gain **light armor**.
3. **Casters' "cantrip":** say it in one line of III.3. *A caster's staff (a standard weapon, d8) attacks with the Facet stat like anyone's weapon.* That makes it the free, reliable basic attack of 13th Age, 5e and Draw Steel. The Fatigue-priced harmful working then has to be worth more than the staff blow. **This is a dependency on ruling 2 (the magic frame).** The recommended frame is: "A harmful working is an attack: the same table, the 10+ pick, exposure on a 7–9, and the level gap". That also resolves design review M5.

**Why this pick.** It meets the goal without adding a rule. The Facet already names a stat, so the sheet already carries the answer.

**Why it keeps niche identity.**
- Body keeps 100% solo, the only d10 grit die, heavy armor and a shield (D4), and every weapon talent.
- Body's damage stays 10–30% ahead (§1.2).

**Why it helps agency.** A Physician's player now chooses *whether* to fight. They no longer have to fight badly.

### Risks

1. **Fights get easier across the board**: Boss fights shorten by about one exchange, and caster drop rates fall to 6–9%. MM1–4's danger table and the monster level table must be re-derived by sim after adoption. The first lever is monster damage +1, or Boss attack +1. This retune is due anyway (design review M2).
2. **Mind and Soul now roll the same attack as Body.** That erodes Body's fantasy only if Body's talents are weak; watch the Brawler (96–100%, fine).
3. **Target.** The "≥60% solo" parity target is too strict for support presets at L10 (Investigator and Physician reach 51%). Proposed replacement, as a sim test:
   - every preset reaches ≥50% solo at every level;
   - presets whose concept is fighting reach ≥75%;
   - every single-Facet party wins ≥95% of the standard fight;
   - per-PC Boss drop rates stay within 3× of each other.
4. **D4 must ship with D1.** Otherwise a Mind build in heavy armor and a shield is a Warrior (§6).

---

## 4. D2 — Protection must not switch off the telegraph

**The problem.** `facet.yaml:114–126` says Sentinel lets you "take the attacks aimed at every ally within your reach". The improved form also attacks.

### Options

**D2-A. Intercept takes *one* telegraphed attack aimed at an ally you can get to. Sentinel: one attack from each of two different foes.** *(The pick.)*
- **Precedent:** 13th Age's Skilled Intercept (one attack); 5e (one reaction per round).
- Against a lone Boss, Sentinel adds nothing, by design: its second attack still needs an answer.
- The improved Sentinel keeps "you may still attack, at Hard".

**D2-B. Transfer with a cost** (Blades Protect, MotW). Take every attack, but you are exposed to each one and they aren't Hard.

**D2-C. Budget or hold** (Dungeon World Defend, Draw Steel resources). For example, Defend gives 1–3 intercepts. Strandberg's critique says this is fiddly unless the rules for losing hold are explicit, and it adds a counter.

**D2-D. Halve instead of redirect** (Draw Steel Parry, 13th Age heavy armor). Still unbounded in how many attacks it covers, so the telegraph is still irrelevant.

### Measured (Guardian, Warrior, Thaumaturge and Invoker, morale on; allies down / Guardian down)

| vs same-level Boss | L1 | L5 | L10 |
|---|---|---|---|
| Guardian attacks instead | 46% / 1% | 53% / 0% | 57% / 0% |
| **Sentinel today** (every attack, Hard) | 7% / 44% | 2% / 13% | 7% / 26% |
| D2-B: every attack, exposed | 14% / 65% | 4% / 16% | 7% / 24% |
| Base Intercept today (all attacks on one ally) | 24% / — | 24% / — | 22% / — |
| **D2-A: one attack** (= Sentinel vs a Boss) | 25% / 22% | 18% / 9% | 18% / 15% |

| vs 2 Elites + 3-Mook mob | L1 | L5 | L10 |
|---|---|---|---|
| Guardian attacks | 20% / 0% | 17% / 0% | 24% / 1% |
| Sentinel today | 0% / 3% | 1% / 4% | 2% / 9% |
| D2-B | 4% / 20% | 1% / 7% | 3% / 13% |
| D2-A: Intercept, one attack | 15% / 1% | 14% / 2% | 16% / 4% |
| **D2-A: Sentinel, one attack from each of two foes** | 8% / 1% | 3% / 2% | 7% / 7% |

Every win rate is 99–100%. The danger lives in who drops.

### Recommendation: D2-A

- **Intercept:** "Defend, and step in front of one attack the MM telegraphed at an ally you can get to. It comes to you instead, at Hard."
- **Sentinel:** "When you Intercept, you may take one attack from each of two different foes."
- **Improved Sentinel:** unchanged.

**Why.**
- It is a rewording, with no new counter.
- The telegraph stays the tactical centre: Intercept is now an *answer to one line* of the telegraph ("I stand in front of the ogre's club"), not a blanket.
- It roughly thirds the drop rate instead of zeroing it.

**Why not D2-B.** The sim shows it just shifts the drops onto the Guardian (65% at L1) and still near-zeroes ally drops. The telegraph remains irrelevant.

### Risks

- **Sentinel feels weaker against Bosses.** Mitigation: it still decides multi-foe fights, and the Guardian's *Bulwark* signature covers ranged attacks.
- **The app needs per-attack redirection.** Today `CombatState.interceptor_for` maps an ally to an interceptor, and it has to become "this attack goes to X" (a Phase-2 engine task).
- **"Can get to" needs D3's definition.**

---

## 5. D3 — Reach and engagement

**The problem.** "Reach" is undefined, yet five rules use it:
- exposure;
- Intercept;
- casters out of reach;
- Cleave;
- Whirlwind.

The consequence: an archer is never exposed and never attacked (design review M4).

### What being out of reach is worth

The table below is the expected damage per Standard attack you *don't* take (vs armor 1), next to what an exposure costs you:

| | L1 | L5 | L10 |
|---|---|---|---|
| Damage avoided per foe attack by being out of reach | 2.72 | 6.67 | 13.11 |
| Extra damage from one exposure | 1.01 | 1.33 | 0.62 |

The book-literal archer avoids the *entire attack*, which is worth 3–10 times the exposure penalty everyone else pays. That is the dominance, not the d8.

### Options

**D3-A. The telegraph defines engagement.** *(The pick.)* Proposed text, in our words:
- *Engaged:* you are engaged with a foe when either of you is fighting the other hand to hand this exchange.
- A foe the MM telegraphs a hand-to-hand attack at closes and engages you, unless the fiction stops it: an ally Intercepting, a wall, a chasm, a door.
- Nothing else tracks distance.

Consequential edits:
- **Exposure:** "your next incoming attack this exchange". Drop "if a foe can reach you".
- **Ranged attack or working while engaged:** Hard.
- **Cleave / Whirlwind:** "foes engaged with you".
- **Intercept:** "an ally you can get to".
- **Delete** III.3:142, "Casters out of a foe's reach are out of its attacks. Stand behind somebody." Standing behind somebody now works *through Intercept*.

Precedent:
- 13th Age: engaged, plus a price for shooting or casting while engaged.
- Draw Steel: an adjacency binary.
- Ironsworn: shooting an advancing foe is a Clash.
- Blades: the fiction sets position.

Rule count: one definition added, one sentence deleted, and five references pointed at the definition.

**D3-B. Named bands** (Shadowdark and 13th Age: Close / Near / Far; Daggerheart has five).
- More precise, but it adds tracked state per PC–foe pair and movement rules. The owner's "no grid" (III.3:3) is better served by one binary.

**D3-C. Position per roll** (Blades): the MM sets Standard or Hard for each attack from the fiction.
- It replaces rules with judgment, and it asks the most of a novice MM (design review M12).

**D3-D. Price ranged in the weapon table** (the design review's d6, or 2 slots with ammunition).
- It treats the symptom. The table above shows the die isn't the dominance.
- It can be combined with A if the sim still shows the Scout on top. The ammunition usage die already exists.

### Recommendation: D3-A

**It matches the calibration data.** `combat_sim.py` already lets every foe attack any PC (random targets), and `resolve_attack(within_reach=True)` exposes everyone on a 7–9. So the MM1 ladder numbers were produced under D3-A all along. Adopting D3-A makes the book agree with its own calibration.

**It gives melee and ranged different prices, not a winner.**
- Ranged characters get hit when a foe closes. They pay Hard when they shoot while engaged.
- An archer is safe only while an ally Intercepts, which is a party answer to the telegraph.
- DW's Volley has the same idea: ranged has its own 7–9 costs.

### Risks

- **"Closes and engages unless the fiction stops it" leaves the MM a judgment call.** Mitigations:
  - MM1 gives three examples (chasm, doorway, Intercept);
  - the Bestiary gives flying and ranged foes a one-word tag (*ranged*, *flies*).
- **Knock-on effect on the Scout.** *Marksman* ("ranged ignores cover") and the Scout's damage lead (7.9 vs 6.0 from L3) should be re-simmed once D1 and D3 are in. If it still leads, apply D3-D's ammunition cost first, before touching the die.

---

## 6. D4 — Custom classes and armor

**The problem.**
- A custom class is two picks from a menu of 11–12.
- Armor is the largest defensive number in the game, and no Facet owns it.
- The design review measured the Physician going from 49% to 90% solo in heavy armor and a shield.

**D1 makes this worse.** Under the D1 pick (Mind attacks with Mind, Mind grit d8), measured in `armor.py` (solo, L1 / L5 / L10):

| Build | Solo win |
|---|---|
| Physician, light armor (the gated kit) | 76 / 87 / 51% |
| Physician, heavy armor + shield (ungated) | 98 / 95 / 78% |
| Tactician, light armor + standard weapon (gated) | 94 / 95 / 88% |
| Tactician, heavy armor + shield (ungated) | **100 / 99 / 95%** |
| Warrior | 100 / 100 / 100% |

Without an armor gate, D1 turns every Mind fighter into a Warrior with a smaller die. **The gate is what makes D1 safe.**

### Options

**D4-A. Armor goes in Table II.4–1** ("the Facet owns the numbers"). *(The pick.)*
- **Body:** heavy armor and a shield. **Soul:** light armor and a shield. **Mind:** light armor.
- **Soft gate:** wearing heavier armor than your Facet allows makes your attacks and workings Hard.
- This *replaces* `magic.heavy_armor_extra_fatigue` and the II.3 text for it.
- **Precedent:** 13th Age (per-class AC, −2 to attacks and spells in the wrong armor) and The Black Hack (a roll penalty). Shadowdark and 5e use a hard version.
- **Presets:** every current preset kit already complies (the Captain wears light armor and a shield). No preset changes.

**D4-B. Price armor instead of gating it** (Knave slots, Cypher Speed cost, Daggerheart Evasion).
- Our 10 + Body slots are too loose to price armor. Tightening them hits every character's exploration kit.
- Knave players already call slot management a hassle.

**D4-C. Armor through a talent** (a Body-menu "Armored" talent that others learn from a teacher).
- It adds a talent, and it makes armor the default off-Facet pick.

**Custom classes, the other half of D4.**
- **D4-1. One cross-Facet starting talent.** *(The pick.)* "One of your two starting talents may come from any Facet's menu, never a casting talent. After level 1, off-Facet talents still need a teacher."
  - This delivers the Morrowind hybrids: a Mind duelist with Weapon Master, a Soul bruiser with Tough, a Body scout with Pathfinder.
  - It doesn't let Body cast, and it doesn't touch the Facet's numbers.
  - The pair space grows from 36–66 possible pairs to roughly 12 × 35 per Facet.
  - **Polymath** (Mind signature: two talents from any menu without a teacher) should become "two more", so it stays distinct.
- **D4-2. Off-Facet talents cost two picks instead of a teacher** (fun evidence §8.7, "never forbid, cost more"). A good *later* rule, but it doesn't widen level 1.
- **D4-3. The knack names the attack stat** (the review's "cross-Facet class knack"). Redundant once D1-A is in.

### Recommendation: D4-A + D4-1

The sheet gains one row (Armor) and one sentence (the cross-Facet starting pick). Two things are *removed*: the heavy-armor Fatigue rule, and "stay inside 3–6 slots and nobody will blink" as the only kit guard.

### Risks

- **The soft gate might be ignored by a Body build that doesn't attack** (a pure Intercept Guardian in heavier armor). That is already Body's own row, so it's fine.
- **Mind in light armor only** keeps Mind the frailest, which is its niche. Soul gets the shield because its four presets include the Captain.
- **Cross-Facet starting picks may converge on *Tough*** (+4 HP) for every Mind character.
  - Sim test: if more than half of the custom-class examples take Tough, make Tough's +4 Body-only ("your HP increases by your grit die maximum ÷ 2"), or exclude it from the cross-Facet pick.
  - Worth one owner decision; not blocking.

---

## 7. Licence table (what we may borrow in *wording*)

| Source | Licence | Wording OK? | Notes |
|---|---|---|---|
| D&D SRD 5.1 (2014) | CC BY 4.0 or OGL 1.0a (creator's choice) | **Yes, under CC BY 4.0, with attribution** | The 2014 Protection style is in it. Sentinel is not (PHB-only). https://www.dndbeyond.com/srd |
| D&D SRD 5.2 (2024) | CC BY 4.0 | **Yes, with attribution** | The 2024 Sentinel, Protection and Interception are **not** in the SRD (PHB, proprietary): ideas only. |
| 13th Age Archmage Engine | OGL 1.0a | Ideas only (house rule) | Mechanics are OGC; names and icons are Product Identity. Also avoid "NASTIER"-style labels. https://www.13thagesrd.com/legal/ |
| Dungeon World SRD | CC BY 3.0 | Ideas only (house rule) | https://www.dungeonworldsrd.com/ |
| Blades in the Dark SRD | CC BY 3.0 | Ideas only (house rule) | https://github.com/amazingrando/blades-in-the-dark-srd |
| Fate SRD (Core, FAE) | CC BY 3.0 or OGL | Ideas only | https://fate-srd.com/official-licensing-fate |
| Knave 1e | CC BY 4.0 | **Yes, with attribution** | https://questingbeast.itch.io/knave |
| Knave 2e | Not verified | Ideas only | |
| Cairn 1e / 2e | CC BY-SA 4.0 | **Yes, with attribution and share-alike.** Creative Commons lists GPLv3 as a one-way compatible licence for BY-SA 4.0, so adapted text may go into our GPLv3 books. The borrowed passage carries the share-alike duty, though, so prefer original wording. | https://cairnrpg.com/ |
| Ironsworn (Datasworn) | CC BY 4.0 | **Yes, with attribution** | https://github.com/rsek/datasworn |
| The Black Hack | OGL 1.0a (name and art reserved) | Ideas only | https://the-black-hack.jehaisleprintemps.net/ |
| Shadowdark | Proprietary third-party licence | Ideas only | https://www.thearcanelibrary.com/pages/shadowdark |
| Daggerheart | Darrington Press Community Gaming License (not open) | Ideas only | https://darringtonpress.com/license/ |
| Cypher System | Cypher System Open License (compatible products only) | Ideas only | https://csol.montecookgames.com/ |
| Draw Steel | Draw Steel Creator License (compatible products; not ORC) | Ideas only | https://www.mcdmproductions.com/draw-steel-creator-license |
| ICRPG | Proprietary | Ideas only | |
| Monster of the Week | Proprietary | Ideas only | |

**None of the four picks needs borrowed wording.** Each is a one-line rule we can write fresh.
- "Take one attack aimed at an ally" and "engaged" are generic game terms, not protected expression.
- The Credits should add 13th Age (the one-attack intercept, engaged), Daggerheart and Draw Steel (every class attacks on its own stat) and The Black Hack (the soft armor penalty) as inspirations. The corrected Credits draft in `REVIEW_lean_prose.md` Appendix C is where they go.

---

## 8. For the Planner: open questions and dependencies

1. **Magic frame (ruling 2) is coupled to D1.** Once a caster's staff attacks with Mind or Soul for free, a 1-Fatigue Significant bolt (1d8, no 10+ pick) is worse than the staff.
   - Recommended: "a harmful working is an attack" (same table, 10+ pick, exposure, level gap).
   - Significant harm then needs one edge over the staff: ignore armor, work at range while engaged without Hard, or a d10.
2. **Retune after D1–D4.** Re-run `--ladder` and the per-PC Boss tests. Expect monster damage or attack to rise by about 1, and MM1's danger table to be regenerated from the sim.
3. **Parity tests.** Put the four checks from §3 risk 3 into `test_combat_sim` or its equivalent as sim-level invariants. The fixed seed and trial counts are already in `combat_sim.simulate`.
4. **Engine work these rulings imply.**
   - `resolve_attack` already takes `stat`; the default must come from the character's Facet.
   - Intercept becomes per-attack.
   - An `engaged` flag feeds exposure (drop `within_reach`) and Hard for ranged attacks while engaged.
   - An armor-gate check goes in `armor_value` / `resolve_roll`.
   - The simulator must not carry any of this; it only calls the engine.
5. **Owner calls (not blocking the Planner).**
   - Mind grit d8: the review's d10/d8/d8. This retires "the Mind pays with the smallest die" (II.4:25), so that line needs rewriting.
   - Tough in the cross-Facet pick.
   - Whether Soul gets a shield.

**Status.** Resolved at the research tier. Return to the Brain for rulings 1 and 4 in `REVIEW_lean_facets.md`, then to the Planner.
