# Oraga Night (5e): rules-lawyer audit, three-PC focus

*2026-10-20. Repo at `b254fb0` (feat/lean-facets, clean). Module folder:
`conversions/dnd5e/oraga_night/`. No module file was edited. Paths below are relative to
that folder, and line numbers are from today's files.*

**Rules source.** I used **SRD 5.2.1**, downloaded from media.dndbeyond.com to
`/tmp/claude-0/-root-facets-of-origin/407a720b-0f36-453e-bd9b-cec22a9c9c7f/scratchpad/srd/SRD_CC_v5.2.1.pdf`
and extracted with PyMuPDF. I checked these against its text: Sleep, Hideous Laughter,
Command, Guidance, Vicious Mockery, Grappled, Grappling (one grapple per hand), Help,
Heroic Inspiration, Hide, Incapacitated, Influence, Initiative score, Invisible, Knocking
Out a Creature, the Fighter table, the Starting Equipment at Higher Levels table, armor
prices, and every pregen spell's class list. SRD 5.2.1 has no procedure for building a
monster's CR, so CRs are re-derived with the 2014 DMG offense/defense method (HP, AC,
DPR, attack bonus, save DC, resistance multiplier). Treat those as yardstick estimates.

**The repo's checkers** (run, not trusted):
- `bestiary_check.py`: 28 blocks plus 1 variant, 0 mismatches.
- `pregen_check.py`: 5 pregens, 0 issues.

I re-derived everything by hand. On arithmetic I agree with both tools. Every finding
below is one the tools cannot see.

---

## 0. Verdict: 6.5 / 10 for rules robustness

**What is clean:**
- The arithmetic. Every block's hit-dice average, AC from gear, attack bonus, save DC,
  damage average, save and skill proficiency, passive Perception and Initiative score
  re-derives correctly.
- All five pregens are legal 2024 builds at 4th level: standard array, background
  ASIs, ASI at 4, Human traits, skill counts, cantrips and prepared counts, class
  features, HP and AC. There is one equipment-cost exception (Dassa's breastplate,
  P3-1).
- The SRD wording is used correctly almost everywhere (Grappled escape DC 8+Str+PB,
  Emanation, Bloodied, Initiative scores with Advantage folded in as +5).

**What fails.** The module's own midnight subsystem (Delay, the Attendant's
Idle/Focused switch, Down Not Out, and "a spell is a trick") can be broken by an
optimizing party. Three PCs break it more easily than four:
- **P1-1.** A three-PC party can freeze any Uninvited in place for as long as it likes
  and grind the Attendant to 0 Hit Points at almost no risk, for its full 3,900 XP.
- **P1-2.** Cantrips and other no-save spells generate Delay with no roll at all.
- Six P2s are ambiguities a rules lawyer will litigate at the table: Hideous Laughter
  against the Uninvited, Clears the Way's timing, speed against turn-count, social
  spells against NPCs with no saves, damage to Down-Not-Out characters, and how far
  success-at-a-cost reaches. One more P2 says saving Raunu is near-automatic.

None of this is new to the arithmetic, and none of it appears in REVIEW 2. REVIEW 2
saw the furniture exploit (N1) but not the Idle-lock equilibrium underneath it.

**Counts:** P0 **0** · P1 **2** · P2 **7** · P3 **17**.

---

## 1. Stat blocks: listed vs derived

Key:
- **HP** = average of the listed hit dice.
- **Hit** = ability mod + PB.
- **DC** = 8 + mod + PB.
- **CR(d)** = derived defensive / offensive CR, then their average. BPS = resistance to
  bludgeoning, piercing and slashing (×1.5 effective HP at CR 5–10, ×1.25 at CR 11+).
- ✓ means the block is correct. "+1 step" means the listed CR sits one step above the
  derived one. That over-rates the XP and makes card labels read harder than the fights
  play, which is safe for the table.

| Block | HP listed / dice avg | AC (source) | Hit / dmg avg | DCs | CR listed → derived (def / off) | Verdict |
|---|---|---|---|---|---|---|
| Attendant | 229 / 27d8+108 = 229.5 ✓ | 17 nat | +7 (Str 4+3) / 1d10+4 = 9 ✓ | Put Aside DC 15 (8+4+3) ✓ | 8 → 11 / ~6 (Focused, 2 turns ≈ 39 DPR, +7) → 8.5 ✓. Idle: 11 / ~0 → ~5 ✓. **3-PC line (180 HP, 3 attacks a round): 8 / ~4 → ~6, but it still pays 3,900 XP** | ✓ math; see P1-1, P2-2 |
| Wept | 187 / 22d8+88 = 187 ✓ | 18 nat | +10 / 4d10+6 = 28 ✓ | — | 11 → ~11.5 (BPS) / ~9.5 (56 DPR, +10) → ~10.5 ✓ | ✓ |
| Radiant | 162 / 25d8+50 = 162.5 ✓ | 17 nat | +9 (Dex finesse-style) / 2d10+5 = 16 ✓ | Rite DC 17 ✓ | 10 → 12 / ~8 → 10 ✓. Weak Con save (+2) | ✓ |
| Hollow | 157 / 21d8+63 = 157.5 ✓ | 16 nat | +9 / 2d10+5 = 16 ✓ | Post and Turn Them Back DC 17 (8+5+4) ✓ | 9 → ~10.5 / ~6 → ~8–8.5 (control traits push it to 9) ✓ | ✓ |
| Master Vell | 285 / 30d8+150 = 285 ✓ | 20 | — | — | — (0 XP) | ✓ math; P3-5 |
| Bought Captain | 97 / 13d8+39 = 97.5 ✓ | 17 (half plate 15 + Dex 2) ✓ | +5 / 1d10+3 = 8 ✓ | — | 4 → 4 / 3.5 → ~4 ✓ | ✓ |
| Veteran Bought Sergeant | 78 / 12d8+24 = 78 ✓ | 17 (chain shirt 13+2+shield 2) ✓ | +5 / 7 ✓ | — | 4 → 3 / 3 → **3** | +1 step |
| Bought Sergeant | 52 / 8d8+16 ✓ | 17 ✓ | +4 / 6 ✓ | — | 2 → 2 / 1 → 1.5 ✓ | ✓ |
| Bought Blade | 22 / 4d8+4 ✓ | 16 ✓ | +4 / 6; cudgel 5 ✓ | escape DC 12 ✓ | 1/2 → ~1/2 ✓ | ✓; P3-2 |
| Boranis Honor Guard | 52 / 8d8+16 ✓ | 18 (chain mail + shield) ✓ | +5 / 7 ✓ | Seize DC 13 ✓ | 2 → 2 / 2 ✓ | ✓; P3-2 |
| Church Warden | 33 / 6d8+6 ✓ | 16 ✓ | +4 / 5 ✓ | Seize DC 12 ✓ | 1 → 1/2 / 1 → ~3/4 ✓ | ✓; P3-2 |
| Damaris Kovaun | 33 ✓ | 11 ✓ | +2 / 3 ✓ | DC 14 (Wis) ✓ | 1/2 (controller) ✓ | ✓ |
| Circle Hired Knife | 32 / 5d8+10 = 32.5 ✓ | 15 (studded 12+3) ✓ | +5 / 5 (+1d6) ✓ | — | 1 → ~1 ✓ | ✓ |
| Rhaza Callun | 22 / 5d8 ✓ | 11 ✓ | +3 / 3 ✓ | — | 1/4 ✓ | ✓ |
| Draunel Duelist | 27 / 5d8+5 ✓ | 15 ✓ | +5 / 7 ✓ | Provocation DC 12 (Cha) ✓ | 1 → ~1 ✓ | ✓ |
| Veteran Draunel Duelist | 44 / 8d8+8 ✓ | 15 ✓ | +5 / 7 ✓ | DC 12 ✓ | 2 → ~1.5–2 ✓ | ✓ |
| Essar Draunel | 58 / 9d8+18 = 58.5 ✓ | 16 (breastplate) ✓ | +5 / 7 ×3 ✓ | — | 3 → ~2.5 | ✓ (slightly high) |
| Essin Boranis | 45 / 10d8 ✓ | 14 ✓ | +5 / 5 (+7 SA) ✓ | — | 2 → ~1.5–2 ✓ | ✓ |
| Vorlain Boranis | 60 / 11d8+11 = 60.5 ✓ | 15 ✓ | +5 / 7 (+7) ✓ | — | 3 → ~2–2.5 | +1 step (borderline) |
| Boranis Cousin's Blade | 22 ✓ | 14 ✓ | +4 / 6 ✓ | escape DC 12 ✓ | 1/2 → **1/4** | +1 step |
| Boranis Cousin of 3160 | 33 / 6d8+6 ✓ | 14 ✓ | +4 / 6 ×2 ✓ | DC 12 ✓ | 1 → **1/2** | +1 step |
| Maiven Nolonaire | 58 ✓ | 15 ✓ | +5 / 6, 5 ✓ | sling disarm DC 13 ✓ | 3 → **2** | +1 step |
| Thenya Border Slinger | 19 / 3d8+6 = 19.5 ✓ | 14 ✓ | +5 / 5, 6 ✓ | — | 1/2 → ~1/4–1/2 ✓ | ✓ |
| Pellin Corro | 13 ✓ | 11 ✓ | +3 / 3 ✓ | Init 16 = 10+1+5 (Adv) ✓ | 1/8 ✓ | ✓ |
| Phern Bodyguard | 33 ✓ | 15 ✓ | +4 / 5 ✓ | Shove DC 12 ✓; Init 19 = 10+4+5 ✓ | 1 → ~3/4 ✓ | ✓ |
| Tavva | 44 / 8d8+8 ✓ | 15 ✓ | +5 / 5 (+7) ✓ | Furniture DC 13 (Dex) ✓ | 2 → ~2 ✓ | ✓ |
| Gallery Knife | 13 / 3d8 = 13.5 ✓ | 13 ✓ | +4 / 4 ✓ | — | 1/4 ✓ | ✓ |
| Feuding Kinsman, and the principal | 9 / 2d8 ✓; 22 / 4d8+4 ✓ | 11 ✓ | +3 / 3 ✓ | — | 1/8 ✓ | ✓ |
| Sect Guard | 11 / 2d8+2 ✓ | 16 ✓ | +3 / 4 ✓ | — | 1/8 ✓ (the SRD guard) | ✓ |

**Pregens** (all checked against SRD 5.2.1):

| Pregen | Array + bg + ASI | HP | AC | Init | Saves / skills (count) | Spells | Verdict |
|---|---|---|---|---|---|---|---|
| Serane (Bard Lore 4) | 15/14/13/12/10/8 → Cha 18, Con 14 ✓ | 31 ✓ | 14 ✓ | +4 (Alert) ✓ | 9 profs = 2 bg + 3 class + 1 Skillful + 3 Lore ✓; Expertise and Jack of All Trades math ✓ | 3 cantrips + gift, 7 prepared, 4/3 slots, DC 14 ✓; all on the Bard list ✓ | ✓; P3-3, P3-4 |
| Pello (Rogue Thief 4) | → Dex 19 ✓ | 31 ✓ | 16 ✓ | +4 ✓ | 9 ✓ | — | ✓ (Nick, Steady Aim, Fast Hands and Second-Story Work all match 2024) |
| Andra (Wizard Evoker 4) | → Int 19 ✓ | 26 ✓ | 15 (Mage Armor) ✓ | +2 ✓ | 8 ✓; Scholar on History ✓ | 4 cantrips + gift, 7 prepared, book 14 (6 + 2×3 + Savant 2; Darkness and Magic Missile are both Evocation) ✓ | ✓ |
| Dassa (Fighter Champion 4) | → Str 18, Con 16 ✓ | 40 ✓ | 16 (breastplate 14+1+Defense 1) ✓ | +3, Adv ✓ | 5 ✓ (Medicine via Skillful; not on the Fighter list, which is legal) | — | ✓ build; **P3-1 equipment** |
| Ilesse (Cleric Life 4) | → Wis 18, Con 14 ✓ | 31 ✓ | 14 / 16 ✓ | +3 ✓ | 5 ✓; Arcana and Religion +4 come from Thaumaturge, not proficiency ✓ | 5 cantrips (4 + Thaumaturge) + gift, 7 + 4 domain, DC 14 ✓ | ✓ |

---

## 2. P1: exploits that break the climax

### P1-1. The Idle-lock: three PCs can freeze an Uninvited indefinitely and grind the Attendant for full XP with almost no risk

**The rules that combine** (each is clear on its own):
1. **The Attendant is Focused only if "any one of the three in the scene has no Delay"**,
   checked at the start of each of its turns (10:217–224; 05:411–413; 09:1789–1793).
   Otherwise it is Idle. *Rusty* then gives it **one Joined Hands attack, with
   Disadvantage** (10:231–233).
2. **Clears the Way is off whenever an enemy is within 5 feet** (10:256–260). An
   "enemy" is anyone who has attacked it or interfered since the end of its last turn
   (*Literal Orders*, 10:226–229).
3. **Delay is uncapped** (05:242–262). An Uninvited spends exactly 1 a turn. A party
   gains it from:
   - one damage lump a round: 30 for four PCs, but **20 for three**, and the three-PC line
     also gives the Wept an extra turn (05:291–292);
   - unlimited tricks, each type twice, plus any trick the table invents (05:250–258);
   - four dais ward-points at Raunu's side, each at **DC 10** (05:484–487; Table V–2,
     row 1).
4. **The Uninvited attack only creatures that are "between them and their errand"**
   (05:27–28). A PC flanking from the side, or attacking at range, is never a target.
5. **Down, Not Out** makes any drop a two-round inconvenience (05:204–235).

**The line, with the pregens, three PCs at the dais.** Each round:
- **Dassa attacks the Idle Attendant.** She is now an enemy within 5 feet, so Clears
  the Way is off. Its one disadvantaged swing at +7 against AC 16 hits about 36% of
  the time, about 3.4 damage a round, against 40 HP and three Second Winds.
- **Andra or Ilesse and Pello make the 20-point lump.** For example:
  - Magic Missile at 2nd level: 14 force, no resistance applies;
  - Pello's daggers plus Sneak Attack from the Wept's flank: about 8 after BPS;
  - or Guiding Bolt, 4d6 radiant.

  That is **+1 Delay**, and nobody involved stands between her and Raunu.
- **Serane** turns a ward-point (DC 10) or plays a room trick (DC 13): **+1 Delay**.

Net: +2 against a spend of −1 a round. **The Wept never reaches Raunu**, and the
Attendant never comes back to Focused. While the ward-points and table tricks last,
everyone except Dassa can then switch to the Attendant. Its 180 HP (the three-PC line)
falls in roughly 8–10 rounds, and it pays **3,900 XP** (09:1915–1917). Even after the
tricks run out, the lump alone holds the Wept at net 0 while Dassa blocks.

**Why it is a P1:**
- It inverts the boss card's stated play. The card says "Played as a slugging match,
  this fight usually goes the Attendant's way" (09:1816–1819) and calls it "the hardest
  fight of the night". Here it is harmless.
- It contradicts a core promise: "**Delay changes how many, not whether**" (05:276–279).
- No rule says what happens when the Wept is held until the leash.
  - ⟨They save Raunu⟩ (05:1090–1094) lists only the Fracture route.
  - The Midnight Clock's "count from the beat he would have fallen" (05:85–86) has no
    beat to count from.
- There is a second vacuous case. With **no Uninvited in the scene**, "any one of the
  three in the scene has no Delay" is false, so the Attendant is Idle forever. That
  happens if the party pulls it away, or if the Wept has finished. The card's own
  line, "When the Uninvited it guards is done with this room, so is it" (09:1786),
  is not a rule that removes it.

**Fix** (all three are needed):
1. **Cap Delay.** "An Uninvited can't have more than 3 Delay. Delay gained above that is
   lost." Also add a **hard ceiling** to the Midnight Clock: "However much Delay she
   has, the Wept reaches Raunu by her 8th turn (9th with three characters), unless her
   Fracture or a trap has landed." That makes ⟨They save Raunu⟩ the only exit and
   keeps "how many, not whether" true.
2. **Rewrite the Attendant's state test** as "Focused at the start of its first turn
   each round **unless every Uninvited it has seen this round has Delay**; with no
   Uninvited in the scene it follows the nearest one, or leaves (*Not Here*), and the
   card ends with **no XP**."
3. **Pay Idle damage at half XP.** "Driven to 0 Hit Points while it was Idle for most
   of the fight, it pays half XP." Or make *Rusty* end after two rounds of being
   attacked: "Attacked on two consecutive turns, it becomes Focused regardless."

Add a `fact_check` entry so the cap prints the same way in 05, 08, 10 and the S14 card.

### P1-2. "A spell is a trick … if it lands, that is the success": no-save spells and cantrips buy Delay with no roll

**The rule.** "A spell is a trick like any other: if it lands, that is the success"
(05:254–255; repeated at 10:164–166). A trick earns Delay on a success and works twice
per Uninvited (DC 13, then DC 15), "never a third time".

**The problem.** Many spells have no attack and no save, so they always "land". Andra
and Serane alone carry these, at will or from slots:
- *Minor Illusion*: a wall, a crying child, a voice.
- *Mage Hand*: drop a candle into the linen, tip a sconce.
- *Prestidigitation*: a snuffed lantern, a sound.
- *Silent Image*, *Message*, *Darkness*, a *Held Image* charge, *Fire Bolt* into the
  canopy (fire is a listed trick).

Each is a separate "trick" and lands **twice** per Uninvited. Andra's four cantrips
plus the gift give about **10 free Delay per Uninvited before anyone rolls a die**. It
feeds P1-1 directly. It also makes Table V–2's checks pointless for a caster, and it
breaks "Earn it by being clever, not by hitting harder" in the other direction: a
caster earns it by spending an action.

**Fix.** Add to 05:254 and 10:164: "A spell with no attack roll or saving throw is a
trick like any other, and still needs the trick's check, made with the caster's
spellcasting ability (the fitting skill's proficiency applies). A spell that forces a
save lands if the Uninvited fails it (*Centuries of Practice* applies). Each spell is
one trick: casting it again is the same trick." Optionally add: "Cantrips buy Delay
only once per Uninvited each."

---

## 3. P2: ambiguities and balance a rules lawyer will litigate

### P2-1. Hideous Laughter on an Uninvited, by the rules as written, leaves them Prone and unable to stand; the table says "nothing bought"
- **The table** (10:148) lists *Hideous Laughter* with Hold Person and Sleep as
  "Condition immunities; nothing bought".
- **The spell.** SRD 5.2.1 *Hideous Laughter* applies **Prone and Incapacitated**, and
  "it can't end the Prone condition on itself" for up to a minute.
- **The immunities.** The Uninvited are immune to Incapacitated, not to Prone (10:1127,
  1399, 1924). *Held by Something Else* (10:1145) covers charm, fear, sleep, compulsion,
  command and transformation. Laughter is none of those.
- **Result, by the rules as written:**
  - a failed Wisdom save (the Wept at +7 against DC 14 fails 30% of the time,
    Centuries aside) leaves her **Prone for up to a minute**;
  - attacks within 5 feet of her have Advantage;
  - her attacks have Disadvantage;
  - Shadow-Step does not end Prone.

  A 1st-level slot from Serane does more than the table admits.
- **Fix.** Add "laughter, or any effect that would knock them helpless" to *Held by
  Something Else*, or add **Prone** to the effects that "simply fail". Better still, list
  the spell by name in the trait.

### P2-2. Clears the Way has no timing, and still works while the Attendant is Incapacitated or Commanded; control spells on the Attendant go unaddressed
- **No timing.** "Once each round, if it hasn't lost its turn to a distraction and no
  enemy is within 5 feet" (10:256; 09:1782) never says *when* the condition is checked.
  - Focused, its *Joined Hands* pushes the adjacent blocker 5 feet (10:279–280). On its
    second turn, at Initiative −10, it can push the last blocker away. Is the check made
    at the end of the round, when nobody is adjacent? Or at some point during it? Each
    reading flips the clock.
- **Not tied to a turn.** Clears the Way isn't an action, so RAW it keeps working while
  the Attendant is **Incapacitated** (*Hideous Laughter*; Serane has it prepared, and the
  Attendant is Int 22 with Wis +1 and **not immune** to Incapacitated, Paralyzed,
  Stunned, Prone, Grappled or Restrained), or under *Command* "Halt" or "Grovel"
  (Ilesse has it).
- **Sleep auto-fails** against it (Exhaustion immunity, 10:210). That is correct by the
  SRD, but the card never says so, and a player will cast it.
- **Hold Person can't target it** (Construct). The card should say that too, because
  the Uninvited, as Humanoids, *are* legal targets.
- **Two Turns doubles the repeat saves** against *Hideous Laughter* (end of each turn).
  The card doesn't note it.
- **Fix.**
  - "*Clears the Way* happens at the end of its first turn each round, and only if it
    took that turn. It doesn't happen while it is Incapacitated or when a spell or
    effect stops it acting."
  - Add a two-line control note to S14: "*Sleep* fails (it doesn't sleep). *Hold Person*
    can't target it. *Command*, *Hideous Laughter*, *Web* and *Slow* work as written; a
    turn it loses to one of them counts as a turn lost to a distraction, but not toward
    the four."

### P2-3. Two progress systems that never meet: turn-count (Delay, Midnight Clock) and Speed (Witnessed, Slow, guilt, Ray of Frost)
- **Turn-count.** The Wept reaches Raunu on "her third turn of moving" (05:78–80), the
  Radiant reaches the stair "three beats after" (05:84), and Delay costs "one turn of
  movement" (05:244–246). Progress is counted in **turns**.
- **Speed.** *Witnessed* halves the Radiant's Speed (10:1444–1449). The Fracture sets
  him to 20 feet. *Slow* "doesn't stack with *Witnessed*" (10:158). Andra's *Ray of
  Frost* (−10 feet) isn't addressed, and "never slower than 20" is stated only for
  Witnessed with guilt.
- **The gap.** Nothing says how many feet are a "turn of moving", or whether halving his
  Speed adds beats. The default beats sell Witnessed as "hallway after hallway" (05:506)
  but give it no clock value. DMs will run it two ways.
- **Fix.** One sentence in Buying Time: "On a map, a creature whose Speed an effect
  halves (or cuts to 20 feet or less) for a whole turn makes half a turn's progress;
  two such turns are 1 Delay." Then add "nothing slows him below 20 feet" as a global
  clause on the Radiant.

### P2-4. Social spells on NPCs who have no saving throws, under "NPCs don't make checks"
- **No saves to roll.** "NPCs don't make checks outside a fight" (01:275–276), but
  spells force **saves**, not checks. The "If It Comes to It" lines (10:2026–2057) give
  Raunu, Veier, Corval, Anha, Sella and Otta AC and HP only: **no ability scores and no
  saves**.
  - Corval is "impossible" to bribe, with "no check" (10:2042–2043). A 2nd-level
    *Suggestion* ("show us to the chief's study") or *Charm Person* from Serane has no
    Wisdom save to roll against.
  - The card rules say "A charm or a *Suggestion* that lands is an out too" (09:119–120).
    That invites it.
- **Steel at the ball** (09:123–124) counts only "a spell with a **visible effect**".
  In 2024, casting with Verbal or Somatic components is itself perceptible, but
  Suggestion and Charm Person have no visible effect. Is casting Suggestion on a
  minister in the Receiving Line bare steel or not?
- **Fix.**
  - Give each noncombatant one save line: "Raunu: Wis +6, Cha +4; immune to Charmed
    tonight (two years of wards)"; "Corval: Wis +5"; and so on.
  - Add to 01:275: "Saving throws are not checks; NPCs roll them as usual."
  - Add to Steel at the ball: "Casting a spell with Verbal or Somatic components in view
    of a guest is noticed: a DC 13 Wisdom (Perception) check from the nearest guard or
    snake, and if they notice, it is steel."

### P2-5. Down, Not Out doesn't say what later damage does to a Stable character; S13's fire clause contradicts the lethal-after-midnight rule
- **Later damage.** "That creature is Unconscious and Stable: no Death Saving Throws"
  (05:206–209). But a Stable creature at 0 HP that takes damage suffers a Death Saving
  Throw failure by the rules as written, two on a melee critical hit, and stops being
  Stable. Downed PCs are routinely inside:
  - the Crossing's crossfire (05:631–647);
  - *Put Aside*'s 20-foot Emanation (10:283);
  - a snake's area or knife after midnight;
  - the trample rule (05:377–379).

  Down, Not Out doesn't say whether that damage counts.
- **S13's fire clause.** "A creature that drops in the gallery … is Stable" (09:1700–1704)
  covers *any* cause of the drop, against 09:549 "After midnight damage is lethal as
  written".
- **Fix.**
  - Add to 05:209: "While Stable under this rule, it takes no damage, and nothing
    makes it roll Death Saving Throws, until it is up again."
  - In S13, say "A creature the fire drops …".

### P2-6. Success at a cost has no scope, and chapter I gives it two strengths
- **Two strengths.** 01:269–273 says "you **may** offer". The troubleshooting box
  (01:513–516) says "the thing they wanted **always** arrives".
- **No exclusions.** Nothing excludes it from:
  - Delay tricks (DC 13, so a 9 succeeds);
  - ward-steering;
  - Attendant distractions (DC 19 becomes 15, and with lean-in +4 that is an 11 on the
    die, about 70% for Serane even before Guidance);
  - the S3 gate checks;
  - Very Hard DCs (moving Vell at 21).
- The Fracture has its own built-in fail-by-4 band (05:755), so a DM may also stack the
  generic one on top.
- **Fix.** Add to 01:269: "Success at a cost is for talk and exploration before
  midnight. It doesn't apply to Delay tricks, ward-steering, distracting the
  Attendant, Fractures (which have their own), or any check against a Very Hard DC."
  Then change 01:515 from "always arrives" to "arrives, if you offer it".

### P2-7. Saving Raunu is near-automatic for a party at the dais, and the "real sacrifice" it asks for can't happen
- **The requirement.** ⟨They save Raunu⟩ requires the Wept's Fracture to land before she
  reaches him, with a PC between them (05:1090–1094).
- **The cost of meeting it:**
  - At Raunu's side, four ward-points steer at **DC 10** (05:484–487), so 2 Delay comes
    by round 1–2. That drops her Fracture to **DC 15** (05:780–781).
  - "Everything the Uninvited do openly counts as tells" during the attack (05:739), so
    the tell requirement is met on the spot.
  - The Fracture lands on a **fail by 4 or less** too (05:755). Serane (Persuasion +8)
    lands it on a 3 or better, 90%, or 99% with Heroic Inspiration.
  - With three PCs she arrives on her **fourth** turn (05:291), even more slack.
- **No sacrifice.** The PC "between them" is protected by Down, Not Out and is back in
  two rounds.
- **Fix:**
  1. Make the dais ward-points DC 13 at his side (DC 10 only for a character who
     studied the wards).
  2. Make the Wept's 2-Delay discount a one-step drop (18 → 15 needs two tells; Delay
     drops it one step only, to a floor of 15).
  3. Give ⟨They save Raunu⟩ a real price that Down, Not Out can't erase. For example:
     "the PC between them takes her blow, which ignores Down, Not Out: it is dropped
     and makes Death Saving Throws as normal."

---

## 4. P3: polish and edge cases

1. **Dassa's breastplate is unaffordable.** A breastplate costs **400 GP** (SRD
   equipment table). Fighter starting equipment is option A, B or C (155 GP), plus a
   background's 50 GP. The SRD's "Starting Equipment at Higher Levels" for levels 2–4 is
   "normal starting equipment, 1 Common" magic item. So the breastplate is out of reach
   (11:293, 11:342). Meanwhile Serane, Andra and Ilesse each carry **three** common
   charges and Pello and Dassa carry none, against the guide's one each. **Fix:** give
   Dassa chain mail with no Stealth note (AC 17), or scale mail (AC 16, Stealth
   Disadvantage). Or state the breastplate as a house gift of her last employer. Even
   out the charges.
2. **Grapples without a free hand.** The SRD's "One Grapple per Hand" applies however a
   grapple is started. Three blocks break it:
   - the Honor Guard's *Seize* (blade and shield, 10:456);
   - the Church Warden's *Seize for Questioning* (mace and shield, 10:701);
   - the Bought Blade's *To the Terms* grapple (cudgel and shield, 10:514–517).

   **Fix:** "It lets go of its weapon to do this" or "It grapples with its shield arm",
   or give each grapple a "(the guard has a free hand while it holds a creature)" line.
3. **Serane's Bardic Inspiration** (11:94–96). It omits "**another** creature" and says
   "can hear her" where the SRD says "can see or hear". Copy the SRD wording.
4. **Serane's Vicious Mockery** (11:90–91). "Disadvantage on the target's next attack
   roll" should add "before the end of its next turn" (SRD).
5. **Vell's immunities don't match "Nothing holds Vell"** (10:2084, 10:2110). He is a
   Humanoid without Paralyzed, Stunned, Incapacitated or Unconscious immunity. *Hold
   Person* at the Crossing fails only about 4% of the time (Wis +9 with Magic
   Resistance), but it can land, and it opens ⟨The child is taken⟩ by accident. **Fix:**
   add those four immunities, or give *Beyond Reach* "and no spell or effect stops him
   taking his action".
6. **Message against the Fracture's range.** "A spell can carry the words (a
   *Message*…)" (05:826) and *Message* reaches 120 feet, but invoking needs "within 30
   feet … where they can hear" (05:742–743). Say whether a carried voice counts. The
   suggested answer: no, the speaker must be within 30 feet.
7. **Sleep's timing in a crowd.** In 2024, *Sleep* first makes targets
   **Incapacitated** (standing). They fall Unconscious only on a second failure at the
   end of their next turn. "Drops them into a crush … still on the floor at the end of
   the round" (05:376–379) fires a round early. **Fix:** "anyone left Unconscious on the
   floor at the end of a round".
8. **The midnight charge text contradicts itself.** "Any character holding a charged
   crystal feels it go cold and quiet" (05:139–142) reads as if charges die at midnight.
   The sidebar (05:183–189) says only releases within 30 feet are at risk. Add "(it
   still works; see the sidebar)".
9. **Moving charges.** *A Veil of Quiet* and *Dark-Burst* (10:2189, 10:2195) don't say
   whether the effect moves with a carried crystal. A moving silence bubble is a Stealth
   engine; a moving darkness is a Radiant-Fracture engine. **Fix:** "The effect stays
   where it was released."
10. **Still open from REVIEW 2:** N27 (09:1859, "Natural 20: as succeeding by 5 or
    more" does nothing while Idle) and N28 (03:110–111, the Prickle and an unseen
    attacker's Advantage). Neither has been touched.
11. **An Idle distraction is now nearly a trap.** *Literal Orders* already treats anyone
    who hasn't interfered since its last turn as furniture (10:226–229). So the O60
    "furniture until they next interfere" buys at most one turn of being ignored, yet it
    burns the trick: later repeats get Disadvantage, no bonus, and "never a third time"
    (10:240–241). Players who attempt it while Idle (as the hints encourage, 09:1878)
    are spending their variety for almost nothing. **Fix:** "A trick tried while it is
    Idle isn't spent."
12. **Literal Orders with Two Turns creates targeting windows.** "Since the end of its
    last turn" (10:228) resets twice a round while Focused. A PC who interferes just
    before its first turn can't be targeted on its second. Say "since the start of its
    previous round".
13. **The three-PC attack line double-dips** (05:291–292). The Wept gets a whole extra
    turn *and* the lump drops to 20. Twenty is 6.7 per PC, against 7.5 per PC for four,
    so the lump is easier per head. **Fix:** 22, or keep 20 and drop the extra turn.
14. **The river gate can't be lost, yet the text sells it as the margin.** "Either way,
    the escape holds" (05:605–611). Against that:
    - "The margin at the river gate is meant to be made of this" (05:806–807);
    - "one point is enough" (05:273; 10:1432);
    - the Radiant's Fracture effect "does not break past Vell" (10:1469–1470).

    All of these are mechanically inert. That is fine if intended, but say so in a DM
    Note, so a DM doesn't invent a failure state: "The gate can't be lost; what the
    characters buy is who sees it, and who is hurt."
15. **The non-lethal house rule has no result** (09:125–128). "May say a blow is meant
    to knock out" names no outcome. Is it the SRD's 1 HP, Unconscious and a Short Rest,
    or the palace's "0 HP, Unconscious and Stable" (10:36–42)? And does it reach save
    or area spells? Say "as the SRD's Knocking Out a Creature, for any attack roll;
    never for an area effect".
16. **The balustrade is a one-shove removal** (09:1365–1366, S9). "1d6 … Prone, and out
    of the scene" means one 2024 Shove (Dassa's save DC 14 against duelists at Str +0
    fails 65%) removes a foe and earns their XP. Add "can climb back next round" or
    "unless it makes a DC 13 Strength (Athletics) check to catch the rail".
17. **Minor format and labels:**
    - CR over-rated by one step on the Veteran Bought Sergeant, the Cousin's Blade, the
      Cousin of 3160, Maiven and Vorlain (see table), so labels read harder than the
      fights play.
    - S4 at three PCs keeps 900 XP, which is now **above** the three-PC Low of 750 though
      the card says "under Low" (09:906, 09:943).
    - The "—" alignment on the Uninvited and Vell isn't an SRD form: use "Neutral" or
      "Unaligned".
    - Whether the Orthaen *Gift Knack* gives Advantage on a crystal-based Attendant
      distraction is unstated (03:90–91 against 09:1830). Answer it.

---

## 5. Stress tests with three PCs (Serane, Pello, Dassa; Andra or Ilesse as the third)

**The Attendant, played as the designer intends.** Focused DC 19, one trick a round,
four needed:
- Serane: +8 Persuasion, +4 lean-in, plus Guidance from Pello's gift or Ilesse, needs
  about a 5–7 on the die (≈ 70–80%).
- Andra: Arcana with crystal; the Gift Knack may give Advantage (P3-17).
- Expect four breaks in 5–6 rounds against about 16 DPR incoming on the three-PC line
  (three Joined Hands a round). One or two PCs drop and are up again in two rounds
  under Down, Not Out.

**Verdict:** a reliable win, which is fine. The Idle-lock (P1-1) makes it a
*guaranteed* win with no drops, which is not.

**The Wept at the dais, three PCs.** Run P1-1's line: she never arrives. Run P2-7's
line: she is Fractured on round 2–3 and Raunu lives. Either way, "Possible, but it
takes … real sacrifice" (05:1090) doesn't describe play.

**The Radiant in the east wing.** Witnessed costs nothing: a cantrip *Light* on a coin,
or a *Steady Light*. *Darkness* makes him faster but sets up his Fracture.
- With P1-2, Andra's cantrips feed his Delay with no check. Each point is "one more
  person gets clear", so Maiven survives at almost any table with a caster present.
- Note that Table V–4 row 5 (the service door) needs Wisdom (Survival), DC 15 first
  time, which no pregen has (Pello has Wis +2 but no Survival proficiency). It needs
  Anha. That is fine.

**The Hollow.** His Fracture (DC 15 with two tells; Intimidation and Deception barred)
lands for Serane about 90% of the time with the fail-by-4 band. Delay on him empties
the hall a dozen guests at a time. No exploit beyond P1-2.

**Down, Not Out as a free resource.** Since no Uninvited or the Attendant can kill a PC,
"stand between" is always free, and so is "a body in the way" (05:363). That is
intended, but it is why P1-1's blocker costs nothing. Healing Word (Serane, Ilesse) gets
a body up as a Bonus Action at range.

**Crystal charges.** The prices match the 2024 consumable scale (Common 50, Uncommon
200). *Grow a Charge* (25 GP and a day, one a week) is break-even at resale, so not a
mint. *House Flare* (no Invisible condition, no Hide) is strong for an Uncommon but
fine. Only the two movement ambiguities (P3-9) matter.

**Origin-feat gifts.** These are balanced against Magic Initiate: one cantrip from a
utility list plus Advantage in a narrow field.
- *Thenya*'s *For Them* is a once-per-Long-Rest Relentless Endurance for an ally. That
  is strong but fine for an origin feat that does nothing for its bearer.
- *Phern*'s Guidance self-buff (concentration, 1 minute) quietly adds +1d4 to every
  distraction and Delay check in a fight. That is worth knowing for P2-6.

---

## 6. Priority fix list

1. P1-1: cap Delay, give the Midnight Clock a ceiling, fix the Attendant's state test
   and its Idle XP.
2. P1-2: no-save spells still need the trick's check; each spell is one trick.
3. P2-1, P2-2: add Laughter and Prone to *Held by Something Else*; time Clears the Way
   and make Incapacitated stop it; add an S14 control-spell note.
4. P2-5, P2-6: say damage is ignored while a character is down; give success at a cost
   a scope.
5. P2-3, P2-4, P2-7: the speed-to-clock line; noncombatant saves and casting as steel;
   a real price for saving Raunu.
6. The P3s, Dassa's armor first (it is the only pregen legality issue).

With 1–4 done, the subsystem holds against a three-PC optimizer, and the score rises
to about 8.5.
