# DESIGN — Facets d20

*Planner contract for `docs/BRIEF_facets_d20.md`. Every drafter conforms to the numbers
and names in §1–§4 exactly; anything not fixed here is the drafter's call and gets a
line in §7. Balance comparison lives in §6 and is filled in by the Facets drafter.*

## 1. Fixed numbers

| | Body | Mind | Soul |
|---|---|---|---|
| Hit die | d10 | d6 | d8 |
| HP at 1st | 10 + Con | 6 + Con | 8 + Con |
| HP per level after | 6 + Con (fixed) | 4 + Con | 5 + Con |
| Saving throws | Str, Con | Int, Wis | Wis, Cha |
| Armor | all armor, shields | light | light, medium, shields |
| Weapons | simple, martial | simple | simple |
| Facet skills (from Facet list) | 3 | 4 | 3 |
| Talents at 1st | **3** | 2 | 2 |
| Facet feature at 1st | exactly one (drafter names it) | exactly one | exactly one |
| Extra Attack | automatic at 5th | via talent only | via talent only |
| Tradition | none (canon: Body has no magic) | **Thaumaturgy** (Int) | **Invocation** (Wis or Cha, chosen once) |

- Levels **1–10**. Proficiency bonus +2 (1–4), +3 (5–8), +4 (9–10).
- **+1 talent at every level 2–10.** Talent tiers: **T1** from 1st, **T2** from 3rd,
  **T3** from 6th. At most one prerequisite per talent.
- **Ability Score Improvement** is a talent available in all three menus (T1, repeatable,
  +2 to one or +1 to two, max 20). No separate ASI levels.
- **Signature** at 3rd: one of six per Facet. Not a talent pick.
- Abilities: standard array 15,14,13,12,10,8 printed; SRD 5.2.1 point buy allowed.
- Background (SRD 5.2.1 shape): +2/+1 or +1/+1/+1 to three listed abilities, two skill
  proficiencies, one tool, one **origin talent** = any T1 talent from any Facet menu
  flagged `origin: true`, plus a **Specialty** (advantage when it applies).

## 2. Spellcasting contract

- Caster talents (T1, exact names): **Thaumaturgy** (Mind menu), **Invocation** (Soul
  menu). Taking your own Facet's tradition talent → **full caster**; slots by
  **caster level** on the Full table. *Caster level* = levels held since taking the
  tradition talent, counting the level taken as 1 (Planner ruling (a), 2026-09-27: closes
  the late-caster loophole; a character who takes their own tradition at 1st has caster
  level = character level, so is unaffected).
- Taking the *other* Facet's tradition talent as a cross-Facet pick, or Body taking
  either (Body may take Invocation or Thaumaturgy only as a cross-Facet pick from 2nd
  level) → **half caster**: slots by **caster level** on the Half table (the SRD half
  rows, which equal the Full row at `ceil(caster level / 2)`). A character never has two slot tables;
  a second tradition talent adds its domains to the same pool.
- **Full table** (1st–5th level slots) = SRD full caster rows 1–10.
  **Half table** = SRD half caster (paladin) rows 1–10 (1st–3rd level slots).
- On taking a caster talent: choose **two domains** of that tradition; cantrips known 2
  (+1 at 4th, +1 at 10th, by character level); **prepared spells** = casting mod +
  caster level (half casters: casting mod + half caster level, round down, min 1),
  chosen from your domains' lists after each
  long rest. The talent **Wider Study** (Mind and Soul menus, T2) adds a third domain.
- Domains are the project's canon domain names from
  `player_handbook/Appendix_Magic_Domains.md`, each assigned to Thaumaturgy or
  Invocation (a domain may be in both). Each domain lists 8–15 **SRD 5.2.1** spells,
  levels 0–5, and at least 2 cantrips. The Magic drafter owns these lists.
- Rituals: any prepared spell with the ritual tag. Concentration: SRD rule, unchanged.
- Spellcasting focus: any tradition-appropriate object; no component pouch bookkeeping
  unless a component has a gp cost.

## 3. Combat contract (the Combat drafter writes it; others reference by these names)

- **Side initiative** — one contest (each side's best Dex check, or surprise) decides
  who goes first; each side acts in any order it likes; then the other side.
- **Bloodied** — at or below half HP. Non-boss enemies check **Morale** when first
  Bloodied and when their leader falls: DC 10 Wisdom save; fail = flee, surrender, or
  bargain (MM's pick fitting the creature). **Mindless and bound creatures never check
  morale** (mindless undead, constructs, oozes, a guardian bound to its post); they count
  HP × 1.25 in the encounter budget (Planner ruling (b)).
- **Fixed damage** — monsters deal the SRD average; roll only on a crit (double the
  dice then add).
- **Minion** — 1 HP; a hit kills; a successful save takes no damage; fixed damage.
- **Boss** — acts twice per enemy phase; Bloodied triggers a phase change. No legendary
  or lair actions. A **stunned** boss (Stunning Strike or any stun) loses one of its two
  turns, not both: it skips its next turn and the stun then ends (Planner ruling (d)).
- Signatures that let a side skip the initiative contest (*Master Plan*, *Seen It
  Coming*) are allowed exceptions, printed in the signature (Planner ruling (e)).
- **One reaction** per round. Leaving an enemy's reach provokes one opportunity attack.
- **Death**: SRD death saves, unchanged.
- **Target**: a Standard fight ends in 3–4 rounds for four PCs.

## 4. RP contract

- **Sparks**: start each session with 1, max 3. Earn: a Drive costs you something; you
  narrate a natural 1 as a complication with flair; the MM's call for a great moment.
  Spend: advantage before rolling; reroll after; or add 1d6 to an ally's roll you
  describe helping with. Replaces Heroic Inspiration. **Talents may also grant Sparks**
  (e.g. *Prophecy*); the cap of 3 holds (Planner ruling (c)).
- **Drives**: two per character — one want, one line they will not cross.
- **Attitude track**: Hostile / Wary / Neutral / Friendly / Ally. A successful social
  check moves one step (two on beating the DC by 10); leverage or a fitting Specialty
  grants advantage; a failure by 5+ moves one step down.
- **Mirror Master (MM)** always; never GM/DM.

## 5. File ownership

| Drafter | Files |
|---|---|
| Core (A) | `facets_d20/README.md`, `01_What_Is_Different.md`, `02_Characters.md`, `06_Backgrounds_Sparks_and_Social.md`, `08_Combat.md`, `10_Quick_Reference.md` |
| Facets (B) | `03_Facet_of_the_Body.md`, `04_Facet_of_the_Mind.md`, `05_Facet_of_the_Soul.md`, `data/facets_d20.yaml` (facets, talents, presets, signatures), `software/tests/test_facets_d20_data.py`, §6 below |
| Magic & MM (C) | `07_Magic.md`, `09_Mirror_Masters_Guide.md`, `data/facets_d20_spells.yaml` (domains → SRD spells, caster tables) |

Cross-file references use chapter file names and the exact names in §1–§4.

## 6. Balance comparison (Facets drafter fills in)

*Preset vs nearest SRD class at levels 1, 5, 10: HP, attack bonus, expected damage per
round vs AC 14, slots, notable features. Target within ±10%.*

**Method (B, 2026-09-27).** Standard array + background +2/+1, ASIs taken where the preset
takes them (the retuned presets take ASIs at the SRD pace: 4th/6th/8th for the Fighter,
4th/8th/10th for the Rogue, 4th/8th for the Wizard and Priest). Hit chance
p = (21 − (14 − attack bonus)) / 20, clamped 5–95%. Expected damage per round
E = p × (average dice + modifier) + crit chance × average dice (crit 5%, 10% on 19–20);
once-per-turn riders (Sneak Attack, Exploit Weakness) added the same way. Save cantrips:
target has +2 on the save, fail chance (DC − 3) / 20. HP is **without** the origin talent,
because the SRD character gets an origin feat too (Tough is one in both). Slots: the Full
table is the SRD full-caster table, so slot counts are identical by construction
(L1 2 · L5 4/3/2 · L10 4/3/3/3/2).

**Table 6–1: Presets against SRD 5.2.1 classes**

| | Lvl | HP ours / SRD | Attack | Dmg/round ours / SRD | Notes |
|---|---|---|---|---|---|
| **Fighter** (Dueling, longsword + shield) vs SRD Fighter (Champion) | 1 | 12 / 12 | +5 | 5.9 / 5.9 | Ours has *Tough* on top (+2/level) — the Body 3rd talent at 1st; SRD has no equivalent until its origin feat |
| | 5 | 49 / 49 | +7 | 15.2 / 15.2 | Both: Extra Attack, Action Surge, Second Wind. Ours has a 2nd Fighting Style (SRD Champion: 7th) |
| | 10 | 104 / 104 | +9 | 19.3 / 19.3 | *Champion's Edge* = Improved Critical. With *Tough* ours is 124 HP (+19%); an SRD fighter taking Tough as origin feat matches it |
| **Rogue** (rapier) vs SRD Rogue | 1 | 12 / 10 | +5 | 7.0 / 7.0 | Body d10 vs rogue d8 |
| | 5 | 49 / 43 | +7 | 14.1 / 14.1 | Sneak Attack 3d6 on one attack; ours may instead make two plain attacks (12.4). Ours gets *Uncanny Dodge* at 3rd, *Evasion* at 5th (SRD 5th/7th) |
| | 10 | 104 / 93 | +9 | 22.7 / 22.7 | HP +12% — the Body hit die. SRD rogue has Cunning Strike/Steady Aim; ours has Extra Attack as a fallback and heavier armor available |
| **Wizard** (Fire Bolt) vs SRD Wizard (Evoker) | 1 | 8 / 8 | +5 | 3.6 / 3.6 | *Studied Recovery* = Arcane Recovery. Ours adds *Studied Eye* |
| | 5 | 32 / 32 | +7 | 8.3 / 8.3 | *Careful Casting* = Sculpt Spells (3rd, both). Slots identical |
| | 10 | 62 / 62 | +9 | 13.4 / 13.4 | Ours via *Potent Cantrips* (7th); SRD via Empowered Evocation (10th). *Arcane Mastery* ≈ a free 1st/2nd spell per short rest from 3rd |
| **Priest** (Sacred-Flame-type cantrip) vs SRD Cleric (Life) | 1 | 10 / 10 | DC 13 | 2.3 / 2.3 | *Font of Life* = Disciple of Life. SRD cleric may choose heavy armor (Protector); ours can't without *Martial Training* |
| | 5 | 38 / 38 | DC 15 | 5.4 / 5.4 | *Channel* = Divine Spark (2nd, both). Slots identical |
| | 10 | 73 / 73 | DC 17 | 9.8 / 9.8 | *Potent Cantrips* at 7th = Potent Spellcasting at 7th. *Miracle* at 3rd is a smaller Divine Intervention (only levels you have slots for) seven levels early; *Wellspring* = Preserve Life at 6th (SRD 3rd) |
| *Investigator* (non-caster Mind, rapier) vs SRD Rogue | 1 | 8 / 10 | +5 | 7.0 / 7.0 | Parity check: the non-caster Mind hits like an SRD rogue on a studied target |
| | 5 | 32 / 43 | +7 | 14.1 / 14.1 | Needs a *Studied Eye* use per target (proficiency bonus per short rest) |
| | 10 | 62 / 93 | +9 | 23.8 / 22.7 | *Anatomist* 19–20 crits; *Anticipate* and medium armor + shield offset the d6 |

**Verdict.** Damage and slots match the SRD at 1st, 5th and 10th for all four presets (0%
difference by construction of the retuned picks). HP matches for Fighter, Wizard and
Priest; the Rogue is +12–14% because Body's hit die is d10 (deliberate: Body pays for no
magic with durability). The Body Facet as a whole sits one talent above the SRD fighter
at 1st level (BRIEF §7 Q2 default confirmed). Two things got pulled back to hit the band:
*Potent Cantrips* is gated at 7th (at 3rd it put Wizard/Priest cantrips +34%/+44% at 5th),
and the Fighter/Rogue/Monk/Wizard cards no longer take an ASI at 2nd (it put the Fighter
+17% at 5th). A player who front-loads ASIs can still beat the SRD curve by one ability
point for a few levels; the cost is the talent they didn't take.

## 7. Drafter decisions log

*(Each drafter appends: decision — reason.)*

**Drafter A (Core) — 2026-09-27**

- A: decision — Side-initiative contest = every player rolls a Dex (initiative) check, party uses its best; MM rolls one check for all enemies using their best Dex modifier; ties go to players; one roll per fight. — Reading of §3 "each side's best Dex check" that keeps players rolling and the MM to one die.
- A: decision — Within a side, each creature takes a whole SRD turn before the next begins (no interleaving half-turns); every creature keeps its own turn so "until your next turn" durations work unchanged. — Stops side initiative from breaking SRD duration text.
- A: decision — Monster crit = roll double the damage dice and add the modifier (SRD crit), otherwise fixed average. — §3 wording made concrete.
- A: decision — Minion: a failed save against damage kills; a successful save takes none. Bosses do not check morale (§3 only says "non-boss enemies check"). — Spelled out in 08.
- A: decision — Sparks: reset to 1 at session start (unspent do not carry over); one Spark per roll per player (two players may each spend on one roll); the ally +1d6 costs no action and is spent after the ally rolls, before the MM narrates the outcome. — "Start each session with 1" read as a reset; answers the v0.3 Spark-hoarding playtest finding.
- A: decision — Specialty also keeps the core PHB clause "routine/informational tasks inside it need no roll" on top of §1's advantage. — Keeps parity with the core PHB Specialty; no conflict with the contract.
- A: decision — Drives: a player may rewrite one Drive at the end of any session. — Lets characters change without a rule for it.
- A: decision — Attitude-track DCs 10/15/20 set by how hard the NPC is to move (not by the size of the ask); asks inside the current attitude need no roll; a miss by 1–4 spends that argument for the scene. Skills: Persuasion/Deception/Intimidation/Performance usually; Influence action in combat. — §4 gave the step rules but no DC guidance.
- A: decision — Backgrounds give their tool + 25 gp; Facet starting kits (Table 2–3) or 100 gp instead. — SRD 5.2 background equipment/50 GP option simplified; kits drawn from SRD packs.
- A: decision — Eight backgrounds adapted from the project's own core PHB backgrounds (City Watch Veteran, Wilderness Scout, Dockworker, Guild Apprentice, Physician's Assistant, Temple Acolyte, Street Performer, Traveling Merchant), not SRD backgrounds. — Original text; lets the example cast keep their established backgrounds.
- A: decision — Origin talent does not use a talent pick, may come from any Facet, and counts toward the "two talents from that Facet" cross-Facet requirement. Ability Score Improvement always counts as own-Facet. — BRIEF §4.3/§4.4 read together.
- A: decision — **Invocation and Thaumaturgy are never origin talents** (B: do not flag them `origin: true`). — Otherwise a Body character gets a caster talent at 1st, contradicting §2's "only as a cross-Facet pick from 2nd level", and a Mind/Soul caster gets a free third talent.
- A: decision — Signature always comes from your own Facet's six. — §1 says "one of six per Facet", read as own Facet.
- A: decision — Lineage: human by default with no traits; if the MM's setting has other peoples, SRD 5.2.1 species (human included) apply as written, or setting lineages. — Mirrors core PHB Lineage; the contract is silent on species.
- A: decision — Weapon Mastery (SRD 5.2.1) is off unless a talent grants it. — Easy-to-pick-up goal; B may write a talent that grants it.
- A: decision — Languages: Common + two from the MM's setting. — SRD 5.2 shape, setting-neutral.
- A: decision — SRD 5.2.1 attribution printed in README and as a footer in each A-owned chapter. — BRIEF §4.6 "every book"; cheap insurance.
- A: decision — Worked example builds Mordai (Body/City Watch Veteran, Str 17 Con 15 Cha 13 Wis 12 Int 10 Dex 8, HP 12, AC 18, longsword +5 / 1d8+3); his Drives (protect those who can't protect themselves / won't leave a fight while someone weaker is still in it) are derived from his established "defender of the weak" personality. — Owner may want to confirm the Drives as canon for the cast.
- A: decision — Combat vignette is a new, lore-free alley ambush (three minion thugs + a leader) so it can show side initiative, Bloodied, morale on both triggers, minions and fixed damage in two rounds. No town is named.
- C: decision — All 21 canon domains are listed; none excluded. Divination is the one domain on both traditions (Oracle = Fate + Divination); every other domain keeps its canon tradition. — §2 allows "both"; Divination is the only fit for an Oracle's second domain without inventing lore.
- C: decision — The six catalog "prismatic" domains are open at 1st level in Facets d20 (flagged `prismatic: true` in the yaml, no extra cost). — Their d20 lists are no longer than any other; slot levels bound power. Needed so the Oracle can start with Fate. Departs from core-PHB "no character starts with one" for this option only.
- C: decision — Recommended Soul pairs: Priest = The Tide + Presence (Wis); Druid = Verdance + Beasts (Wis); Oracle = Fate + Divination (Wis or Cha). Variants named in 07: storm druid (Storm), graveside oracle (The Undying), battle priest (Binding). — Matches B's presets in facets_d20.yaml.
- C: decision — Half-caster "caster level" = levels held with the talent, counting the level taken as 1; the Half table (SRD paladin rows) is read by caster level. Half-caster prepared spells = casting mod + half caster level (round down), min 1. Cantrips known follow character level for both. — §2's "ceil(level/2) … counting from the level the talent was taken" read as: Half table row = Full row ceil(caster level/2), which is what the SRD half-caster rows already are (test enforces).
- C: decision — A spell on two of your domains counts once; one cantrip may be swapped per level gained; each spell uses the ability of the tradition it came through. — SRD 5.2.1 cantrip-swap shape; keeps a dual-tradition character to one slot table.
- C: decision — Spell lists use only spells present in both SRD 5.1 and SRD 5.2.1 under their 5.2.1 names (e.g. Tiny Hut, Black Tentacles, Resilient Sphere, Arcane Hand, Faithful Hound, Private Sanctum, Secret Chest). Left out as uncertain SRD 5.2.1 status: Hunter's Mark, Enthrall, Giant Insect, Find Traps, Hallow, smite spells, and all non-5.1 cantrips. Revivify and Raise Dead sit in The Tide per the catalog's "at its absolute limits" note. Resonance tops out at 3rd level (no fitting 4th/5th SRD spells). — "If unsure, leave it out."
- C: decision — Encounter budget uses two sums, HP (how long) and fixed damage per round (how dangerous); stop at whichever fills first. Party damage/round 18,20,25,27,40,42,46,50,58,64 (L1–10); HP budget = that × 2 / 3.5 / 4.5 / 6 (Easy/Standard/Hard/Deadly). Damage ceiling = 25/40/55/75% of party HP (40 at L1, +28/level). Minion counts 7 HP (L1–4) / 10 (L5–10); never-breaks foes HP × 1.25; boss damage counts twice; recharge abilities excluded from the sum; party-size multipliers 0.75/1.25/1.5. — Morale and overkill treated as cancelling; tuned to a 3.5-round Standard fight. Needs a playtest.
- C: decision — Boss Recharge abilities roll to recharge once per enemy half-round (not per turn). — Otherwise two turns doubles breath-weapon frequency.
- C: decision — Levelling: MM-called milestones, 1/1/2/2/3/3/3/3/3 sessions per level (≈20 sessions to 10th). Treasure: SRD 5.2.1 items; coin ~50/250/1,000 gp per character per level by band (1–4/5–8/9–10); rarity by band; ≤1 very rare per party. — House guidance, not SRD text.
- C: flag — Worked conversions quote SRD 5.2.1 block numbers from memory (Bandit, Goblin Warrior, Zombie, Ogre, Owlbear, Young Red Dragon; the dragon's Multiattack given as "about 45"). A reviewer with the SRD PDF should verify before release.
- A: decision — After B/C drafts landed: 01/02 name the Facet features (Second Wind / Studied Eye / Inspiring Word) and the twelve presets from 03–05; 06 background origin-talent suggestions use B's origin-flagged talents (Alert, Wild Kin, Tough, Gadgeteer, Field Medic, Magic Initiate, Silver Tongue, Skilled); Mordai's worked example follows B's Fighter card (Defense, Weapon Mastery, Tough, origin Alert → HP 14, AC 19); 08 vignette uses his longsword's Sap mastery. Weapon Mastery line in 01 now points to B's Body talent.
- A: decision — 08 and 10 now say "the mindless and the bound never break", matching C's 09 (morale "never" line). §3 said only "non-boss enemies check"; this is an extension of the contract by C that A adopted rather than contradict. Owner may want §3 amended.
- A: decision — 06 notes "some talents grant Sparks too; cap 3 holds" because B's Oracle prophecy talent (05) hands allies Sparks, an earn route not in §4.

**Drafter B (Facets) — 2026-09-27**

- B: decision — Talents carry a `facets` list; a shared talent (Ability Score Improvement; Expertise Body+Mind; Martial Training, Extra Attack, Magic Initiate, Wider Study, Potent Cantrips Mind+Soul) is one entry with one id. `prereq` is null, one id, or a list meaning "any one of" (used only for "Thaumaturgy or Invocation"). — Keeps ids unique and still satisfies "at most one prerequisite".
- B: decision — Facet features: Body **Second Wind** (bonus action, 1d10 + level HP, 2 uses/3 from 5th, one back on a short rest); Mind **Studied Eye** (bonus action, studied target until fight ends: learn resistances/immunities/vulnerabilities, advantage on next attack this turn; prof-bonus uses per short rest); Soul **Inspiring Word** (bonus action, Heart die d6/d8 from 5th added after a d20 test; prof-bonus uses per long rest, short rest too from 5th). — One each per §1; Studied Eye is the hook for Mind's non-caster damage.
- B: decision — Facet skill lists (not given in §1): Body 8 (Acrobatics, Animal Handling, Athletics, Intimidation, Perception, Sleight of Hand, Stealth, Survival); Mind 8 (Arcana, History, Insight, Investigation, Medicine, Nature, Perception, Religion); Soul 10 (Animal Handling, Deception, Insight, Intimidation, Medicine, Nature, Performance, Persuasion, Religion, Survival). In yaml `facets.<f>.skills`.
- B: decision — "Soul modifier" = your Invocation casting ability if you have it, otherwise the higher of Wis and Cha. — Honours C's "Wis or Cha chosen when you take Invocation" while letting non-caster Soul talents work.
- B: decision — **Oathsworn is a non-caster preset.** Own-tradition Invocation is full-caster by §2, and full slots + heavy armor + Extra Attack + a smite on one card was too much. Its smite is *Sworn Strike* (2d8/3d8/4d8, prof-bonus uses), its lay-on-hands *Mending Hands*, its aura *Aura of Resolve* (T3). Every Facet therefore has a non-caster preset (Body all four, Mind Investigator, Soul Oathsworn); tested.
- B: decision — *Sneak Attack* (Body) and *Exploit Weakness* (Mind, studied target only) use the SRD rogue dice (ceil(level/2)d6) but can't be used on a turn you make more than one attack, and never combine. — Body gets Extra Attack free; without this clause the Body Rogue was +34% over the SRD rogue at 5th. With it, rogue damage equals the SRD exactly.
- B: decision — *Martial Training* gives martial weapons + one armor step: Mind gains medium armor and shields, Soul gains heavy armor. *Extra Attack* (Mind/Soul) requires *Martial Training* and 5th level. *Potent Cantrips* is T2 with min level 7. *Stunning Strike* is T2 with min level 5.
- B: decision — Weapon Mastery exists as a Body T1 talent (three weapon kinds, swap one per long rest), per A's "off unless a talent grants it".
- B: decision — Presets carry a suggested `origin_talent` (several deliberately cross-Facet: Wizard *Tough*, Loremaster *Silver Tongue*, Priest *Field Medic*, Oracle/Oathsworn *Alert*) and a full 2nd–10th pick list in yaml; the cards print picks to 5th and a "Later" line. Two presets show cross-Facet picks (Investigator *Cunning Action* at 7th, Oathsworn *Tough* at 10th). Book text and yaml are held together by `TestChaptersMatchData`.
- B: decision — Tinker is the fourth Mind preset (Thaumaturgy with Inscription + Transmutation, *Gadgeteer*, *Infuse Item*, signature *Clockwork Companion*). Physician appears as the custom-build example in 04 instead. — Tinker exercises two talents nothing else uses; the Physician shows a non-caster, non-preset build.
- B: decision — The Oracle's foresight mechanic is original: *Glimpses* (prof-bonus per long rest, once per round give any visible creature's d20 test advantage or disadvantage), *Prophecy* (T2: a spoken sentence each morning; when it comes true, glimpses refill and each ally who heard it gets a Spark), *Twist of Fate* (T3: spend after the roll to force a reroll). No text from non-SRD portent mechanics.
- B: flag — **Late own-tradition casting.** §2 reads the Full table by *character* level, so a Soul character who takes Invocation at 6th (or a Mind character Thaumaturgy) gets 6th-level full-caster slots at once. An Oathsworn with Extra Attack, heavy armor and *Sworn Strike* who adds Invocation at 6th is the strongest thing in the game. No preset does it. Recommend the Planner either read the Full table by levels held (as the Half table already is), or make own-tradition casting after 2nd level a half caster.
- B: flag — *Stunning Strike* on a boss (two turns per enemy phase): suggest 09 say a stunned boss loses one of its two turns rather than both, if C agrees. Not changed in 03.
- B: flag — *Seen It Coming* (Soul signature) and *Master Plan* (Mind signature) let a side go first without the contest; both sit under A's "surprise decides it, otherwise one contest" as an exception printed in the talent.


**Planner (integration review) — 2026-09-27**

- Planner: ruling (a) — **Full caster slots are read by caster level** (levels held since taking the tradition talent, counting that level as 1), same as Half. Prepared spells for full casters = casting mod + caster level. Cantrips known stay by character level. A character who takes their own tradition at 1st is unaffected. Closes B's late-caster flag. Applied to §2, 01, 04 (*Thaumaturgy*), 05 (*Invocation*, Oathsworn sidebar), 07 (Full/Half text, Table 7–2 header, Table 7–4), 10, both yaml files (`casting.full_table_index: caster_level`); tests `TestCasterLevel` in `test_facets_d20_spells.py`.
- Planner: ruling (b) — morale exemption adopted into §3: mindless and bound creatures never check morale (and count HP × 1.25 in the budget). 08, 09 and 10 already said so; no text change needed.
- Planner: ruling (c) — talents may grant Sparks, cap 3 holds. Added to §4; 06 already says it (and 05's *Prophecy* is the one talent that does).
- Planner: ruling (d) — a stunned boss loses one of its two turns, not both: it skips its next turn and the stun ends. Added to §3, 09 (Bosses), 03 (*Stunning Strike*) and the yaml summary.
- Planner: ruling (e) — *Master Plan* and *Seen It Coming* skipping the initiative contest are allowed exceptions. Added to §3 and to 08 (Who Goes First).
- Planner: ruling (f) — Oathsworn is a non-caster preset (B's call accepted). Checked README, 01, 02, 07: none calls it a caster. BRIEF §4.3 still says "Paladin-style Oathsworn" and "paladin-ish Soul warrior" half caster; BRIEF is Brain output and left as the historical record.
- Planner: SRD check — every spell on every domain list (189) verified against the SRD 5.2.1 PDF and the Open5e srd-2024 list: all present, all at the right level. C's "uncertain" omissions that ARE in SRD 5.2.1 added back: Hunter's Mark and Giant Insect (Beasts), Divine Smite and Spiritual Weapon (Presence), Searing Smite (Fire), Ensnaring Strike (Verdance), Enthrall (Resonance), Find Traps (Divination), Hallow (Warding), Aura of Life (The Tide, its first 4th-level spell), and the 5.2.1 cantrips Elementalism (Storm), Sorcerous Burst (The Arcane), Starry Wisp (Fate). Not in SRD 5.2.1 and still out: Thunderous/Wrathful/Branding/Blinding/Staggering/Banishing Smite, Thorn Whip, Toll the Dead, Word of Radiance, Hail of Thorns, Zephyr Strike, Summon Beast/Fey. Supersedes C's "left out as uncertain" line. A pinned whitelist test (`TestSrdWhitelist`) now enforces it. Record: `docs/RESEARCH_facets_d20_srd_check.md`.
- Planner: 09 conversions checked against SRD 5.2.1 blocks. All six were right except the Young Red Dragon's Multiattack: three Rends at 16 (13 slashing + 3 fire) = **48**, not "about 45"; boss total 96, still inside the 9th-level Standard budget. Resolves C's flag.
- Planner: 01 tightened from 21 numbered differences to 12 by merging (presets into Facets; ASI and weapon mastery into talents; domains into spellcasting; fixed HP into levels; lineage into backgrounds; opportunity attacks into side initiative; fixed damage with Bloodied/morale; the MM line moved out of the list). No mechanic cut.

**Dominant-pick audit (BRIEF §6) — 2026-09-27.** Full record: `docs/RESEARCH_facets_d20_dominance.md`.

- Audit: *Sworn Strike* uses = **Soul modifier (minimum 1)**, not proficiency bonus. — With PB uses it was a must-take cross-Facet dip for Body melee (+32% at 5th, +40% at 10th over the SRD fighter for one pick). A low-Cha dip now gets 1 use (≈ +20%, a *Fighting Style*'s worth); the Oathsworn (Cha +2, rising with its later ASIs) keeps about its old count. Supersedes B's "prof-bonus uses" line above.
- Audit: *Radiant Strikes* is **once on each of your turns**. — Every-hit +1d8 from 6th (SRD 11th) put the Oathsworn +11% over the SRD paladin at 10th and made Sworn + Radiant a +54% Body dip. Now ≈ paladin parity.
- Audit: *Aura of Resolve* gains **Prerequisite: *Interpose*** (the protector capstone). — All four Soul presets took it; it was the only open Soul T3 and nothing else touches party saves. Presets: Priest 9th *Interpose*, 10th *Aura of Resolve* (was *Aura*/ASI; §6 models the Priest's ASIs at 4th/8th only, so §6 stands); Druid 10th *Interpose*; Oracle 10th *Channel*. Oathsworn unchanged (*Interpose* 3rd, *Aura* 6th).
- Audit: *Anticipate* has **no use limit** beyond the reaction. — With PB uses per long rest it was strictly worse than *Glimpses* (Soul T1, a legal cross pick) and, in practice, *Well-Timed Word*. Now the narrow-but-unlimited option; one attack a round against one studied creature, so not the Lean *Sentinel* problem.
- Audit: *Unarmored Defense* (Constitution) also gives **advantage on Dexterity saves while unarmored**. — For a Body character with every armor, the Con version bought less AC than 50 gp of scale mail (Barbarian card: 13 vs 15). The rider is the SRD barbarian's Danger Sense; the Wisdom version is unchanged.
- Audit: *Potent Cantrips* yaml summary now says "one of its damage rolls", matching 04/05.
- Audit: tests — `TestDominanceAudit` pins the fixes; `TestMenuTablePrerequisites` checks every menu table's prerequisite column and every entry's **Prerequisite** line against the yaml.
- Audit: left as **watch**, owner's call — level-scaled *Sneak Attack*/*Exploit Weakness* on cross picks and casters; *Weapon Mastery* as a Body tax; *Martial Training* giving Mind casters Soul's armor; *Alert* duplicated across four presets' origin talents; *Glimpses*, *Survivor*. No change.
