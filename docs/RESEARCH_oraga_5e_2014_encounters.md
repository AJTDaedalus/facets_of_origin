# RESEARCH: Oraga Night 5e encounters, for a 4p / 2014-rules rebalance

Status: COMPLETE, data extraction only. No module file was edited and no rebalancing was done.

**Source:** `conversions/dnd5e/oraga_night/` (read-only). Line refs are `file:line` relative to that folder. Nothing under `references/` was read.

**Baseline the module prints against:** every number is for **three 4th-level characters**, SRD 5.2.1 budget, summed XP with no multiplier: Low 750 / Moderate 1,125 / High 1,500 (`09_The_Snakes.md:93-123`; Table IX–1 at `09_The_Snakes.md:155-163`; `10_Bestiary.md:16-19`). Adjustment lines are **not cumulative**, one line per table (`09_The_Snakes.md:104-106`).

**Table IX–1 as printed (SRD 5.2.1)** `09_The_Snakes.md:155-163`: Three@4th 750/1,125/1,500 · Four@4th 1,000/1,500/2,000 · Five@4th 1,250/1,875/2,500 · Four@3rd 600/900/1,600 · Four@5th 2,000/3,000/4,400.

**The module already flags the 2014 gap:** `10_Bestiary.md:82-87` ("At a 2014 table" box) says the 2014 multiplier rates most cards one or two bands harder, cites S3 850→1,700 "past Deadly" and S14 "more than twice Deadly", and tells the DM to keep printed rosters. A 2014 rebalance would have to rewrite that box too.

**2014 method used here (DMG p. 82):**
- Thresholds, 4th level per character: Easy 125 / Medium 250 / Hard 375 / Deadly 500.
  - 3 × 4th: **Easy 375 · Medium 750 · Hard 1,125 · Deadly 1,500**
  - 4 × 4th: **Easy 500 · Medium 1,000 · Hard 1,500 · Deadly 2,000**
- Multiplier by monster count (party of 3–5): 1 ×1 · 2 ×1.5 · 3–6 ×2 · 7–10 ×2.5 · 11–14 ×3 · 15+ ×4.
- Band = highest threshold the adjusted XP meets. Below Easy is written "trivial".
- CR→XP for every CR in this module is the same in 2014 and SRD 5.2.1 (1/8=25, 1/4=50, 1/2=100, 1=200, 2=450, 3=700, 4=1,100, 8=3,900), so raw sums carry over unchanged. Table X–2 at `10_Bestiary.md:113-123`.
- **Reinforcements:** the 2014 DMG counts every monster in the encounter. Where creatures arrive mid-fight, I give both the opening roster and the full roster.
- **Low-CR caveat:** the DMG lets you leave out of the count any monster whose CR is far below the rest of the group. That applies to Pellin Corro (CR 1/8 beside CR 1 bodyguards) on S11. Both versions are shown.

---

## 1. Stat-block reference (chapter X)

No creature in the module casts spells; there is no Spellcasting trait anywhere in `10_Bestiary.md`. Offense below is per turn. "Breaks" is the morale line. All blocks have a Wants / Tells / Breaks / Nastier quartet.

| Creature | `10_Bestiary.md` | CR | XP | AC | HP | Offense per turn | Breaks (morale) | Nastier |
|---|---|---|---|---|---|---|---|---|
| Feuding Kinsman | 1050 | 1/8 | 25 | 11 | 9 | 1 attack: Fists +3, 3 nonlethal, or push/prone; or Harvest Fruit +3, 1 dmg + Advantage | Any kinsman hit steps out and shouts. Brawl stops when an obeyed adult arrives | A second principal swings at the party; a 1 ticks the clock twice |
| — principal variant | 1102 | 1/8 | 25 | 11 | 22 | as kinsman | — | — |
| Gallery Knife | 1107 | 1/4 | 50 | 13 | 13 | 1 Knife +4 | Drops sack and runs; will not stand past the point Tavva would leave | One more knife behind the party |
| Rhaza Callun | 1574 | 1/4 | 50 | 11 | 22 | 1 Knife +3, 3 dmg | When her people's work would be seen as hers | — |
| Pellin Corro | 1329 | 1/8 | 25 | 11 | 13 | 1 Knife +3 (never fights) | Never fights; leaves | None |
| Sect Guard | 1627 | 1/8 | 25 | 16 | 11 | 1 Cudgel +3 | Never past compliance | Sergeant joins |
| Damaris Kovaun | 821 | 1/2 | 100 | 11 | 33 | Staff +2, 3 dmg | Calls wardens off at once | Lock clock starts at 1 |
| Boranis Cousin's Blade | 361 | 1/2 | 100 | 14 | 22 | 1 attack: Longsword +4, 6 dmg, or A Quiet Word +4, 3 dmg + hold | Essin's word; else half down or a crowd | Use the Cousin of 3160 block |
| Bought Blade | 535 | 1/2 | 100 | 16 | 22 | 1 attack: Company Blade +4, 6 dmg, or Cudgel (detain: 0 HP → 1 HP + Grappled) | Disengages in good order | Sergeant has set the boundary |
| Thenya Border Slinger | 1749 | 1/2 | 100 | 14 | 19 | 1 attack: Sling +5, 5 dmg, or Long Knife +5, 6 dmg | On Maiven's word, or when she is down or safe | One knows the window |
| Boranis Cousin of 3160 | 411 | 1 | 200 | 14 | 33 | **Multiattack 2** Longsword +4, 6 dmg (or A Quiet Word) | Essin's word; else half down or a crowd | Breaks only on a crowd |
| Church Warden | 709 | 1 | 200 | 16 | 33 | **Multiattack 2** Mace +4, 5 dmg, or Mace + Seize for Questioning | Prelate's word, or **two down** | No break at two down |
| Circle Hired Knife | 768 | 1 | 200 | 15 | 32 | **Multiattack 2** Knife +5; Step Aside (Disengage/Hide) | Callun's word, or **first knife Bloodied** | Break at half down |
| Draunel Duelist | 876 | 1 | 200 | 15 | 27 | Multiattack: **1** Rapier +5, 7 dmg + Provocation (Wis DC 12) | **First time one of them takes damage**, challenge refused, or Draunel withdraws them | Use the Veteran block |
| Phern Bodyguard | 1377 | 1 | 200 | 15 | 33 | **Multiattack 2**: Caravan Blade +4, 5 dmg, or Shove | When Corro is through the door; Corro's word | Crowd DC 15 |
| Boranis Honor Guard | 462 | 2 | 450 | 18 | 52 | **Multiattack 2** House Blade +5, 7 dmg, or 1 + Seize (Str DC 13); Warder charges; reaction **Call the House** (+4 guards at start of 2nd round after it) | Never flees; offers terms | A third guard; the way back shut |
| Bought Sergeant | 654 | 2 | 450 | 17 | 52 | **Multiattack 2** Company Blade +4, 6 dmg | Bloodied: calls Blades back, still fighting; surrenders when contract void | Use the Veteran block |
| Tavva | 1670 | 2 | 450 | 15 | 44 | **Multiattack 2** Knife +5, 5 dmg (or 1 + Furniture), **Sneak Attack 2d6**; Cunning Action; Uncanny Dodge; 2 crystal charges (escape) | Charge when first Bloodied; bargains when cornered | 3rd charge and one more knife |
| Veteran Draunel Duelist | 1854 | 2 | 450 | 15 | 44 | Multiattack: **2** Rapier +5, 7 dmg + Provocation | First time it takes damage, etc. | Breaks only when Bloodied |
| Essin Boranis | 989 | 2 | 450 | 14 | 45 | **Multiattack 2** Knife +5, **Sneak Attack 2d6**; Always Between | Stops when Vorlain is out of reach | Already knows what was said |
| Essar Draunel | 933 | 3 | 700 | 16 | 58 | **Multiattack 3** Rapier +5, 7 dmg | The moment the fight would be seen as his | Iron 3: a third duelist |
| Maiven Nolonaire | 1268 | 3 | 700 | 15 | 58 | **Multiattack 3**: Long Knife +5, 6 dmg, or Sling +5, 5 dmg (disarm) | **Never breaks**; stops on proof of Veier or with an ally | Already over the wall |
| Vorlain Boranis | 1911 | 3 | 700 | 15 | 60 | **Multiattack 2** Blade +5, 7 dmg; Brief and Efficient | Ends fights fast and walks away | Brief and Efficient pre-paid, Essin beside |
| Bought Captain | 582 | 4 | 1,100 | 17 | 97 | **Multiattack 2** Very Good Sword +5, 8 dmg **+ Command**; The Read | Calls withdrawal; won't resume | Reform the Line (1/day) |
| Veteran Bought Sergeant | 1795 | 4 | 1,100 | 17 | 78 | **Multiattack 3** Company Blade +5, 7 dmg; Hold the Terms | As Bought Sergeant | Hold the Terms already spoken |
| The Attendant | 222 | 8 | 3,900 | 17 | 178 (229 four, 260 five, 210 four@3rd; +30 "built to hit hard") | Focused: **two turns a round**. Turn 1 Multiattack 2 Joined Hands +7, 9 dmg (one can be Put Aside, Str DC 15, 2d8 in 20-ft emanation, recharge 5–6). Turn 2: Clears the Way or 1 Joined Hands (**full Multiattack with four or more**; none vs a lone character). Idle: 1 Joined Hands at Disadvantage | None: four broken focuses or 0 HP | Already Focused |
| The Hollow | 1155 | 9 | 5,000 | 16 | 157 | Multiattack 2 Bare Hands +9, 16 dmg + Turn Them Back (Str DC 17, 15-ft cone). *Leashed* | Never | None |
| The Radiant | 1436 | 10 | 5,900 | 17 | 162 | Multiattack 3 Offered Hands +9, 16 dmg. *Leashed* | Never | 4th attack |
| The Wept | 1972 | 11 | 7,200 | 18 | 187 | Multiattack 2 Strength Like a Fact +10, 28 dmg. *Leashed* | Never (Mercy ends her) | 3 attacks after the party's 3rd round |
| Master Vell | 2143 | — | 0 | 20 | 285 | Not fought; never drops before the boat clears | Leaves | — |

The Uninvited earn no XP in play (they cannot be beaten, `05_The_Longest_Night.md:819-878`). The noncombatants under "If It Comes to It" earn none (`10_Bestiary.md:2093`). Vell is worth 0 (`10_Bestiary.md:26, 2229`).

**Blocks that hit harder than their XP (the module's own words):** three attacks (Essar Draunel, Maiven, Veteran Bought Sergeant) and Sneak Attack (Tavva, Essin), per `09_The_Snakes.md:113-117`. **Five CRs "read a step generous"** for their blocks: Veteran Bought Sergeant, Cousin's Blade, Cousin of 3160, Maiven, Vorlain (`09_The_Snakes.md:118-121`).

---

## 2. Fight cards S1–S14 (chapter IX)

Shared rules: every clock has 4 segments unless the card says otherwise. A "1 on a d20" ticks a clock at most once a round. Morale is checked at first drop, half down, leader down, and last one alone and hurt. After midnight the first check is half down (`09_The_Snakes.md:125-133`). An out pays full card XP unless it is marked (no XP) (`09_The_Snakes.md:134-139`). Before midnight nobody dies: a dropped character is Stable, and Table IX–4 sets the cost (`09_The_Snakes.md:597-616` (Table IX–4 at 602)).

### S1. The Seating Feud — `09_The_Snakes.md:618` (Mv II/III, B3)
- **Printed (3p):** 6 Feuding Kinsmen (CR 1/8, 25) + 1 principal variant (CR 1/8, 25) = **175 XP**, "under Low" (a quarter of Low). Table IX–3: "under Low; the clock is the fight".
- **Adjustments:** Nastier: second principal also swings, a 1 ticks the clock twice, **200 XP** (6×25 + 2×25) · Four: 8 kinsmen + principal, **225** · Five: 10 + principal (275, not printed) · Four@3rd: 6 kinsmen, no principal (150, not printed) · Four@5th: 10 + principal (275, not printed). No One-character line.
- **Reinforcements:** none.
- **Offense:** 1 attack each, nonlethal; the party is limited to unarmed or improvised 1d4. Bare steel voids the scene and brings S4.
- **Clock:** bench clock, 4. Ticks at the end of each round the principals swing, and on a 1. Full: honor guard for a Movement, and one agenda door closes.
- **Morale:** a kinsman who takes any damage steps out. The brawl stops when an obeyed adult arrives (a PC can be one: DC 15 Persuasion or Intimidation).
- **Optional/outs:** yes. DC 13 Persuasion; DC 13 Athletics to get between them; rank (no check).

### S2. The Service Corridor Job — `09_The_Snakes.md:704` (Mv V, B10)
- **Printed (3p):** Tavva (CR 2, 450) + 2 Gallery Knives (CR 1/4, 50) = **550 XP**, "under Low; plays Low, and the clock is the fight".
- **Adjustments:** One: Tavva + 1 knife a round behind, **500** ("High for one") · Four: Tavva + 3 knives, **600** · Five: Tavva Nastier (3rd charge, 4th knife behind the party) + S7's Circle Hired Knife, **850** · Four@3rd: as four, **600** · Four@5th: as five, and noise clock 3 segments (850).
- **Reinforcements:** One-character line: the knife arrives a round behind. Five line: the 4th knife is already behind the party.
- **Offense:** Tavva 2 Knife + Sneak Attack 2d6, Cunning Action, Uncanny Dodge, 2 escape charges (AC 15, HP 44). Knives 1 attack each (AC 13, HP 13).
- **Clock:** noise clock, 4, shared. Ticks on a 1, at the end of each round with a drawn blade, and on anything loud. Full: honor guard, both sides lose (S4 terms).
- **Morale:** knives break when a charge fires or Tavva is gone. Tavva fires a charge when first Bloodied.
- **Optional/outs:** yes. Let her go (no XP); trade information; take the proceeds; lose to noise (no XP). Stealth approach (vs PP 16) surprises.

### S3. The Gate at Midnight — `09_The_Snakes.md:797` (Mv VII, B12; chapter V B12 at `05_The_Longest_Night.md:1174`)
- **Printed (3p):** Bought Sergeant (CR 2, 450) + 4 Bought Blades (CR 1/2, 100) = **850 XP**, "between Low and Moderate". With the Bought Captain (CR 4, 1,100): **1,950**, "over High".
- **Adjustments:** Nastier: Veteran Bought Sergeant (CR 4, 1,100) + 4 Blades = **1,500**, captain at the start of round 2 → **2,600** · Four: Veteran + 4 Blades **1,500** (**2,600** with captain); four's Nastier = veteran's Nastier (Hold the Terms pre-spoken) and the captain a round sooner · Five: veteran + 6 Blades **1,700** (2,800 with captain, not printed for five) · Four@3rd: as printed **850** · Four@5th: veteran + 6 Blades, captain round 2, **1,700 / 2,800**. "Never a second sergeant." No One-character line.
- **Reinforcements:** captain at the start of round 3 (sect-guard clock 2 filled), or the round the sergeant falls. Out over the wall: **4 more Blades** (`09_The_Snakes.md:943-945`).
- **Offense:** Sergeant 2 attacks (AC 17, HP 52). Veteran 3 attacks (AC 17, HP 78). Blades 1 attack, detain to 1 HP + Grappled (AC 16, HP 22). Captain 2 attacks + Command (AC 17, HP 97).
- **Clocks:** fire clock, 4 (ticks on rounds of doing nothing; full means guests die each round). Sect-guard arrival, **6** (ticks every round at the gate; full means the captain withdraws, ending 3).
- **Terrain:** wicket 5 ft, one at a time. Grille gives three-quarters cover.
- **Morale:** Blades disengage when the sergeant falls **or** half are down. Sergeant: Bloodied, calls them back; void contract, surrenders. Captain negotiates when Bloodied or on his second round.
- **Optional/outs:** three endings, all wins: fight through, void or buy the contract (DC 13 Persuasion to the sergeant, none to the captain), outlast. Also the river gate.

### S4. The East Wing Doors (half-card) — `09_The_Snakes.md:966` (any Mv; also Mv I gate draw `04_The_Ball.md:102-106`; Palace on Alert `04_The_Ball.md:54-66`)
- **Printed (3p):** 2 Boranis Honor Guards (CR 2, 450) = **900 XP**, "between Low and Moderate; plays Moderate fought out". With the 4 reinforcements: **2,700**, "beyond High".
- **Adjustments:** One: 1 guard, **450**, four still come · Four: 2, as printed (**900**) · Five: 3 + a 4th a round behind (1,800, not printed) · Four@3rd: 2 (900) · Four@5th: 4 guards (1,800, not printed). "The reinforcements never change."
- **Reinforcements:** *Call the House*: +4 guards at the start of the 2nd round after the first guard is Bloodied. In Mv V the doors hold 4: 2 fight, 2 keep the doors.
- **Offense:** 2 attacks or attack + Seize; AC 18, HP 52.
- **Clock:** none printed. The reinforcement trigger acts as one.
- **Morale:** never flee; a broken guard offers terms. A dropped PC goes to the cell (Stable).
- **Optional/outs:** DC 15 Deception/Persuasion; a name (no check); go back (no XP); chase, 3 successes before 3 failures at DC 13.

### S5. The Looters (half-card) — `09_The_Snakes.md:1030` (Mv VI–VII, B7/B3; ch V beat `05_The_Longest_Night.md:650-670`)
- **Printed (3p):** Tavva + 2 Gallery Knives = **550 XP**, "under Low, and it plays that way".
- **Adjustments:** Four: Tavva + 3 knives **600** · Five: Tavva Nastier (4 knives) **650** · Four@3rd: as printed **550** · Four@5th: Nastier, 4 knives, **650**.
- **Reinforcements:** none. **Clock:** none. **Morale:** as S2.
- **Optional/outs:** yes. Let them go (no XP); take it back; point out the fire.

### S6. The Quiet Word — `09_The_Snakes.md:1075` (Mv II–III, B5)
- **Printed (3p):** 2 Boranis Cousins of 3160 (CR 1, 200) = **400 XP**, "under Low, and it plays easier than that".
- **Adjustments:** Nastier: break only on a crowd, third cousin in round 1, **600** · Four: all three (third comes through the garden doors), **600** · Five: three (600) · Four@3rd: 3 Cousin's Blades (CR 1/2), **300** · Four@5th: three, Essin watching (he steps in only to stop it). No One-character line.
- **Reinforcements:** the third cousin (four-character and Nastier lines).
- **Offense:** 2 Longsword or A Quiet Word (3 dmg + hold); fists unless a PC draws. AC 14, HP 33.
- **Clock:** none. A shout loud enough for the Court ends it.
- **Morale:** Essin's word; half down or a crowd.
- **Optional/outs:** declining the invitation avoids it entirely. Say nothing (no check, or DC 15 Deception); name Essin; shout (no XP); walk away (no XP).

### S7. The Second Plate — `09_The_Snakes.md:1162` (Mv IV social half; Mv V fight, B10)
- **Printed (3p):** 4 Circle Hired Knives (CR 1, 200) = **800 XP**, "Low". "Ends fast on its morale, plays High to the last knife."
- **Adjustments:** One: the 3 read-aloud knives, **600** · Nastier: break at half down, clock 3 segments, 800 · Four: all four, as printed, **800** ("under Low for four"; the Circle brought no more) · Five: four knives, plus an extra clock trigger (800) · Four@3rd: three knives **600** · Four@5th: four knives + Tavva's crew from S2 in the same run (total not printed: 800 + 550 = 1,350, or 1,400 with S2's four-character crew).
- **Reinforcements:** none timed. The fourth knife is placed ahead of or behind the party.
- **Offense:** 2 Knife attacks +5; Step Aside. AC 15, HP 32.
- **Clock:** service-door clock, 4. Ticks each round a knife moves unhindered, and when a knife gets past a PC. Full: Circle heat 4.
- **Terrain:** 5-ft run; dim light.
- **Morale:** **first knife Bloodied**, or Callun's word.
- **Optional/outs:** Callun's word; outbid (20 GP + DC 13); DC 13 Intimidation; DC 18 Deception. Stealth (vs PP 13) surprises.

### S8. The Study Door — `09_The_Snakes.md:1294` (Mv V; dark half Mv VI)
- **Printed (3p):** 2 Church Wardens at the door, a 3rd at clock segment 2 = **600 XP** (3 × 200), "under Low; plays Low (Moderate for a party light on damage)".
- **Adjustments:** One: 1 warden, the 2nd in round 3, breaks at one down, **400** · Nastier: no break at two down, 3rd already at the door, 600 · Four: 4th warden at segment 3, **800** · Five: as four, clock starts at 1 (800) · Four@3rd: as printed, **600** · Four@5th: as five, 3rd already at the door (800).
- **Reinforcements:** 3rd warden at segment 2; 4th at segment 3 (four/five/5th lines).
- **Offense:** 2 Mace or Mace + Seize; detain only. AC 16, HP 33.
- **Clock:** lock clock, 4. Ticks each round undisturbed and on a 1.
- **Morale:** **two down**, or the Prelate's word.
- **Optional/outs:** DC 15 Religion/Persuasion; Agenda 2 (DC 13 or none); fetch Kovaun; trade. Stealth (vs PP 13, with Advantage) surprises. The dark half has no clock and the same roster.

### S9. The Appointment — `09_The_Snakes.md:1412` (Mv V, B5)
- **Printed (3p):** Draunel side: 3 Draunel Duelists (CR 1, 200) = 600, "under Low". Boranis side: 3 Cousin's Blades (CR 1/2, 100) = 300, "far under Low". **Both: 900**, "between Low and Moderate". "Plays High if both sides fight to the last."
- **Adjustments:** One: 2 a side (2 duelists + 2 Blades), **600** · Nastier: Veteran Draunel Duelist + 2 duelists + 3 Cousins of 3160 = **1,450** "just under High" · Four: Veteran + 2 duelists **850**, + 3 Cousin's Blades **300**, both **1,150**; four's Nastier: the veteran's Nastier + 3 Cousins of 3160, **1,450** · Five: as four + Essin on the Boranis side from the start (+450 if hostile = 1,600, not printed) · Four@3rd: 2 duelists + 2 Blades, **600** · Four@5th: 2 Veterans + 1 duelist (**1,100**) + 3 Cousins of 3160 (**600**), Essin present, Draunel at the rail (1,700, or 2,150 if Essin is hostile; not printed).
- **Reinforcements:** **Essin** (CR 2, 450) arrives on clock segment 1 if a PC went to him, either as the Boranis leader or as the party's ally.
- **Offense:** duelist 1 Rapier + Provocation (AC 15, HP 27); veteran 2 Rapier + Provocation (HP 44). Blades 1 attack (AC 14, HP 22).
- **Clock:** circle clock, 4. Ticks each round the principals face off, and when a cousin fails vs Provocation. Duelists hold Provocation until a PC acts.
- **Morale:** duelists break **the first time one takes damage**. Cousins on Essin's word or when their man is off the grass.
- **Optional/outs:** yes. DC 15 refuse; DC 13 first blood; DC 15 shame; DC 13 stand between; Essin's word. Offstage default if not attended.

### S10. Over the Wall — `09_The_Snakes.md:1530` (Mv V, garden; only if heat ≥ 3 **and** provoked)
- **Printed (3p):** Maiven Nolonaire (CR 3, 700; arrives at clock segment 2) + 2 Thenya Border Slingers (CR 1/2, 100) = **900 XP**, "between Low and Moderate; plays Low (Moderate for a party light on damage)". Guard branch: S4 (900 / 2,700).
- **Adjustments:** One: Maiven alone, down in round 3, 2 attacks not 3, **700** · Four: Maiven + 3 slingers, **1,000** · Five: Maiven + 3 slingers + slingers' Nastier (1,000) · Four@3rd: as printed, **900**, she pulls her blows (2 attacks) · Four@5th: Maiven's Nastier + 3 slingers (1,000).
- **Reinforcements:** Maiven at segment 2 (round 3 for one character).
- **Offense:** Maiven **3 attacks** (AC 15, HP 58). Slingers 1 attack (AC 14, HP 19).
- **Clock:** half-bell, 4, ticks every round. Full: the climb, and S4 with the Thenya as offenders. At heat 4 it starts at 1.
- **Morale:** Maiven never breaks; the slingers stay with her. The fight ends the instant the party stops standing in the way.
- **Optional/outs:** a fight **only if provoked**. Go with them; proof (no check); DC 13 promise; DC 13 Insight warning. Stealth (PP 13) surprises.

### S11. The Phern Door — `09_The_Snakes.md:1631` (Mv VI, B2)
- **Printed (3p):** 2 Phern Bodyguards (CR 1, 200) + Pellin Corro (CR 1/8, 25) = **425 XP**, "under Low; the crush is the fight".
- **Adjustments:** Four: 3 bodyguards (+Corro), **625** · Five: 3 bodyguards, crowd DC 15 (625) · Four@3rd: as four, **625** · Four@5th: as five, crush clock starts at 1 (625). No One-character line.
- **Reinforcements:** none.
- **Offense:** bodyguards 2 attacks (blade or Shove), shove first (AC 15, HP 33). Corro never fights.
- **Clock:** crush clock, 4, ticks each round the door is held for Corro alone. At heat 4 it starts at 1. The crowd is a hazard: DC 13 Athletics/Acrobatics or prone + 1d6.
- **Morale:** gone the moment Corro is through; Corro's word.
- **Optional/outs:** Corro's word (no check, or DC 15); hold the door (DC 13 each round); follow Corro; another door. Not hostile unless crossed.

### S12. Corval in the Kitchens (half-card) — `09_The_Snakes.md:1713` (Mv VI–VII, B10; Circle heat 3–4)
- **Printed (3p):** 2 Circle Hired Knives = **400 XP**, "under Low". At heat 4, a third knife: **600**, "still under Low". Table IX–3: "400–600".
- **Adjustments:** Four: 3 knives **600**; at heat 4, 4 knives **800** · Five: 4 knives (800) · Four@3rd: 2 knives **400**, 3 at heat 4 · Four@5th: 4 knives, smoke DC 13 Con (800).
- **Reinforcements:** none timed. Four Bought Blades are outside the yard gate (terrain, not foes of the party).
- **Offense:** as S7. Smoke: DC 10 Con or lose the action.
- **Clock:** **none**; the Bought at the yard gate are the timer.
- **Morale:** **half down** (holds longer than S7), or Callun's word.
- **Optional/outs:** Callun; DC 13 Persuasion; let them (no XP); outbid.

### S13. The Arrest in the Fire — `09_The_Snakes.md:1803` (Mv VII, B3; Draunel heat 3–4)
- **Printed (3p):** Draunel side: Essar Draunel (CR 3, 700) + 2 Draunel Duelists = **1,100 XP**, "between Low and Moderate; plays Moderate". Boranis side: Essin (CR 2, 450) + 3 Cousin's Blades = **750**, "Low". Both: 1,850, "beyond High" ("do not run both"). Vorlain (CR 3) only frees his arm.
- **Adjustments:** One: Draunel alone, **700** · Four: Draunel + Veteran Draunel Duelist + Draunel Duelist, **1,350** · Five: Draunel + 2 Veterans, **1,600** · Four@3rd: Draunel + 1 duelist, **900** · Four@5th: as five + a third duelist (Iron 3), **1,800**.
- **Reinforcements:** none.
- **Offense:** Draunel **3 Rapier** (AC 16, HP 58). Duelist 1 + Provocation; Veteran 2 + Provocation.
- **Clock:** gallery clock, 4, ticks every round (a guest lost per segment). At heat 4 it starts at 1. Fire: DC 13 Dex, 2d6. Smoke as S12.
- **Morale:** Draunel breaks the moment it is seen as his fight; duelists with him or at half down. Essin's side breaks when Vorlain is safe.
- **Optional/outs:** shame (no check); hand to the law (DC 15); let Vorlain go back (DC 13 Insight); broker a trade (DC 15). Not taking the fight leaves the default (`05_The_Longest_Night.md:1073-1074`).

### S14. The Attendant — `09_The_Snakes.md:1914` (Mv VI–VII; ch V `05_The_Longest_Night.md:493-533`)
- **Printed (3p):** The Attendant (CR 8, 3,900). "2.6 times High while Focused; plays High while Idle."
- **Adjustments:** One: Focused second turn makes no attack · Four: **229 HP**, Focused second turn is the full Multiattack · Five: 260 HP, full Multiattack on the second turn, distraction DC 19 · Four@3rd: 210 HP, distraction DC 17 · Four@5th: the five line or the block's Nastier · "Built to hit hard": +30 HP (208 for three, 259 for four). XP stays 3,900 on every line.
- **Reinforcements:** none. Its state flips between Idle and Focused each turn according to Delay on the Uninvited.
- **Offense:** see section 1. Focused it takes two turns a round. AC 17.
- **Clock:** the errand. Clears the Way removes Delay, about 6 rounds.
- **Morale:** none. **Four broken focuses** (distraction checks DC 13 Idle / 18 Focused) or 0 HP ends it.
- **Optional/outs:** a party that never interferes never meets it. Stepping back (no XP).

---

## 3. Chapter V and other creature scenes

| Scene | file:line | Foes | XP | Party-size numbers | Notes |
|---|---|---|---|---|---|
| The dais, the Wept → Raunu | `05_The_Longest_Night.md:74-90`, `233-388` | The Wept (CR 11, AC 18, HP 187, 2 × 28 dmg), Leashed | none | Wept reaches Raunu on her **4th** turn (**3rd with four**); lump **20** damage/round (**30** four, **40** five or 4@5th) | Cannot be won by force. Delay at most 3 turns a scene. Down, Not Out: a non-threat is set aside Stable |
| The doors, the Hollow | same; Table V–3 `05:410` | The Hollow (CR 9, AC 16, HP 157, 2 × 16 + Turn Them Back) | none | lump as above | Herds the crowd |
| East wing, the Radiant → Veier | `05:79-90`, Table V–4 | The Radiant (CR 10, AC 17, HP 162, 3 × 16) | none | lump as above | Garden stair at Raunu's fall + 3 beats + Delay |
| The Crossing (Vell vs Radiant) + crossfire | `05_The_Longest_Night.md:672-818`; crossfire sidebar `05:783-802` | Hazard: DC 13 Dex save per beat, 7 (2d6), or 14 (4d6) on a fail by 5+ | none | 4@3rd: 3 (1d6) / 7 (2d6); 4@5th: 10 (3d6) / 21 (6d6) (`05:385-388`). Level-based, not size-based | Initiative only for the PCs. Vell untouchable (AC 20, 285 HP) |
| The Thenya, toward the fire | `05_The_Longest_Night.md:1088-1106` | Maiven + slingers as **allies** vs the Radiant | none | — | No card; fighting Maiven here is ruled out |
| The Attendant | `05_The_Longest_Night.md:493-533` | → S14 | 3,900 | → S14 | |
| Snakes in the Dark (Table V–7) | `05_The_Longest_Night.md:1046-1086` | → S8, S11, S12, S13 | per card | per card | Heat 0–2: no fight |
| The looters | `05_The_Longest_Night.md:650-670` | → S5 | 550 | per S5 | |
| B12, the Gatehouse Court | `05_The_Longest_Night.md:1174-1265` | → S3; Veteran Sergeant "for four or more characters at 4th level or higher" (`05:1215`) | per S3 | per S3 | |
| Carrying people out | `05_The_Longest_Night.md:1154-1161` | hazard: DC 13 Athletics/Con per beat, 5 (2d4) on a fail | 100 per person | — | Not a fight |
| Palace on Alert (any Mv) | `04_The_Ball.md:54-66` | 2 Honor Guards, +4 on Call the House → S4 | 900 | per S4 | |
| Steel in Movement I at the gate | `04_The_Ball.md:102-106` | S4 in the Gatehouse Court, the two nearest guards | 900 | per S4 | |
| A snake's leader dropped before midnight | `04_The_Ball.md:108-115` | Callun or Corro, who "fall to one bad round" | none printed | — | Leads to S4 if killed |
| The host attacked | `04_The_Ball.md:116-121` | Raunu won't fight; ward wall, then S4 | none | — | |
| Guards are a scene (sidebar) | `04_The_Ball.md:676-684` | → S4; chase 3/3 at DC 13 | — | — | |
| Chapter VI (Aftermath) | `06_Aftermath.md` | no creature fights | — | — | |

---

## 4. Party-size numbers outside the cards' Adjusting lines

| file:line | What changes with party size |
|---|---|
| `01_Overture.md:89-92` | Module statement: designed for 3–5 characters of 3rd–5th level, built for three at 4th |
| `01_Overture.md:161-162` | Every card has a one-character line and lines for four or five, four@3rd, four@5th |
| `01_Overture.md:273` | Session minutes are for three players |
| `01_Overture.md:325-339` | Sidebar "Three at the Table": which pregens to deal; with four players, add Andra or Pello |
| `01_Overture.md:405` | Kitchens hold one Potion of Healing **per character** |
| `01_Overture.md:439` | XP: holding S11's door counts as one person per character who held it |
| `01_Overture.md:442-444` | XP totals: a party of three ends near **6,700 XP** each, a party of four near **6,500** |
| `README.md:8-10` | Built for three; cards have lines for four or five |
| `11_Pregenerated_Characters.md:29-30` | Built for three players; points to "Three at the Table" |
| `04_The_Ball.md:449` | Kitchen remedy box: **three Potions of Healing (four if four characters are playing)** |
| `10_Bestiary.md:2294-2297` | Same box: three potions (four if four) |
| `04_The_Ball.md:559` | "Three players will be in three rooms by Movement II" (design assumption) |
| `04_The_Ball.md:1198-1200` | Raunu's summons: at least two PCs; **with four or more players, a second summons can bring two more** |
| `05_The_Longest_Night.md:80-83` | Midnight Clock: the Wept reaches Raunu on her 4th turn (**3rd with four characters**) |
| `05_The_Longest_Night.md:340-342` | Lump threshold: 20+ damage to one Uninvited in a round = 1 Delay (base for three) |
| `05_The_Longest_Night.md:376-388` | Sidebar "Adjusting the Attack": four, Wept 3rd turn + lump 30; five, lump 40; 4@3rd, crossfire 1d6/2d6; 4@5th, lump 40, crossfire 3d6/6d6 |
| `05_The_Longest_Night.md:800-802` | Crossfire sidebar repeats the 3rd/5th-level damage |
| `05_The_Longest_Night.md:1215` | Veteran Bought Sergeant for four or more characters at 4th level or higher |
| `07_Cast_of_the_Ball.md:843`, `:876` | Same Veteran Bought Sergeant rule |
| `08_Handouts.md:17` | Table VIII–1, the night's timeline, is for three players |
| `08_Handouts.md:62` | Wept: 4th turn (3rd with four) |
| `08_Handouts.md:102` | Lump: 20+ (30+ with four, 40+ with five or at 5th level) |
| `08_Handouts.md:149` | With three players, five agendas stay in the deck |
| `08_Handouts.md:503` | Midnight tracker: numbers for three, four in parentheses |
| `08_Handouts.md:510` | Wept arrival boxes: 4 (3 with four) |
| `08_Handouts.md:525` | Attendant HP 178 (229 with four) |
| `09_The_Snakes.md:93-106` | Party-size rule; one-character rule (S2, S4, S7, S8, S9, S10, S13); lines not cumulative; five@5th = 5th line plus one weakest foe |
| `09_The_Snakes.md:107-112` | SRD 5.2.1 budget statement for three |
| `09_The_Snakes.md:155-163` | Table IX–1 |
| `09_The_Snakes.md:518-525` | "With three players", most agendas stay in the deck; factions cool on −1 boxes instead |
| `09_The_Snakes.md:550-565` | Mv V DM note: one card per group of characters, a solo group uses the One-character line |
| `09_The_Snakes.md:572-588` | Table IX–3 budget column is for three 4th-level characters |
| `10_Bestiary.md:16-19` | Blocks built for three; SRD per-character budget |
| `10_Bestiary.md:82-87` | "At a 2014 table" multiplier box (S3 1,700; S14 more than twice Deadly) |
| `10_Bestiary.md:104` | Table X–1: Veteran Bought Sergeant for four or more |
| `10_Bestiary.md:306-311` | Attendant Two Turns: full Multiattack on the second turn with four or more; no attack vs a lone character |
| `10_Bestiary.md:354-357` | Attendant: 2.6 × High for three; 229 HP with four |

---

## 5. 2014 DMG arithmetic

Format: count of creatures → raw XP × multiplier = adjusted → band.

### 5a. Printed three-character rosters vs 3p thresholds (375 / 750 / 1,125 / 1,500)

| Fight | Roster (count) | Raw | × | Adjusted | 2014 band (3p) |
|---|---|---|---|---|---|
| S1 | 6 kinsmen + principal (7) | 6×25 + 25 = 175 | 2.5 | 437.5 | Easy |
| S2 | Tavva + 2 knives (3) | 450 + 100 = 550 | 2 | 1,100 | Medium (25 short of Hard) |
| S3 | Sergeant + 4 Blades (5) | 450 + 400 = 850 | 2 | 1,700 | **Deadly** |
| S3 + captain | 6 | 850 + 1,100 = 1,950 | 2 | 3,900 | Deadly (2.6 × Deadly) |
| S4 | 2 guards (2) | 900 | 1.5 | 1,350 | Hard |
| S4 + 4 | 6 | 2,700 | 2 | 5,400 | Deadly (3.6 ×) |
| S5 | Tavva + 2 knives (3) | 550 | 2 | 1,100 | Medium |
| S6 | 2 cousins of 3160 (2) | 400 | 1.5 | 600 | Easy |
| S7 | 4 knives (4) | 800 | 2 | 1,600 | **Deadly** |
| S8 opening | 2 wardens | 400 | 1.5 | 600 | Easy |
| S8 full | 3 wardens | 600 | 2 | 1,200 | Hard |
| S9 Draunel side | 3 duelists | 600 | 2 | 1,200 | Hard |
| S9 Boranis side | 3 Blades | 300 | 2 | 600 | Easy |
| S9 both | 6 | 900 | 2 | 1,800 | **Deadly** |
| S9 both + hostile Essin | 7 | 1,350 | 2.5 | 3,375 | Deadly |
| S10 opening | 2 slingers | 200 | 1.5 | 300 | trivial |
| S10 full | Maiven + 2 slingers (3) | 700 + 200 = 900 | 2 | 1,800 | **Deadly** |
| S11 | 2 bodyguards + Corro (3) | 400 + 25 = 425 | 2 | 850 | Medium |
| S11 (Corro not counted) | 2 | 400 | 1.5 | 600 | Easy |
| S12 | 2 knives | 400 | 1.5 | 600 | Easy |
| S12 heat 4 | 3 knives | 600 | 2 | 1,200 | Hard |
| S13 Draunel side | Draunel + 2 duelists (3) | 700 + 400 = 1,100 | 2 | 2,200 | **Deadly** |
| S13 Boranis side | Essin + 3 Blades (4) | 450 + 300 = 750 | 2 | 1,500 | Deadly (exactly) |
| S13 both (not to be run) | 7 | 1,850 | 2.5 | 4,625 | Deadly |
| S14 | Attendant (1) | 3,900 | 1 | 3,900 | Deadly (2.6 ×) |

### 5b. Four-character rosters vs 4p thresholds (500 / 1,000 / 1,500 / 2,000)

| Fight | Four-character roster (count) | Raw | × | Adjusted | 2014 band (4p) |
|---|---|---|---|---|---|
| S1 | 8 kinsmen + principal (9) | 8×25 + 25 = 225 | 2.5 | 562.5 | Easy |
| S2 | Tavva + 3 knives (4) | 450 + 150 = 600 | 2 | 1,200 | Medium |
| S3 | Veteran Sergeant + 4 Blades (5) | 1,100 + 400 = 1,500 | 2 | 3,000 | **Deadly** (1.5 ×) |
| S3 + captain | 6 | 1,500 + 1,100 = 2,600 | 2 | 5,200 | Deadly (2.6 ×) |
| S4 | 2 guards (2) | 900 | 1.5 | 1,350 | Medium |
| S4 + 4 | 6 | 2,700 | 2 | 5,400 | Deadly (2.7 ×) |
| S5 | Tavva + 3 knives (4) | 600 | 2 | 1,200 | Medium |
| S6 | 3 cousins of 3160 (3) | 600 | 2 | 1,200 | Medium |
| S7 | 4 knives (4) | 800 | 2 | 1,600 | Hard |
| S8 opening | 2 wardens | 400 | 1.5 | 600 | Easy |
| S8 after segment 2 | 3 | 600 | 2 | 1,200 | Medium |
| S8 full (segment 3) | 4 | 800 | 2 | 1,600 | Hard |
| S9 Draunel side | Veteran + 2 duelists (3) | 450 + 400 = 850 | 2 | 1,700 | Hard |
| S9 Boranis side | 3 Blades | 300 | 2 | 600 | Easy |
| S9 both | 6 | 1,150 | 2 | 2,300 | **Deadly** |
| S9 four's Nastier, both | Vet + 2 duelists + 3 Cousins of 3160 (6) | 450 + 400 + 600 = 1,450 | 2 | 2,900 | Deadly |
| S9 both + hostile Essin | 7 | 1,600 | 2.5 | 4,000 | Deadly |
| S10 opening | 3 slingers | 300 | 2 | 600 | Easy |
| S10 full | Maiven + 3 slingers (4) | 700 + 300 = 1,000 | 2 | 2,000 | **Deadly** (exactly) |
| S11 | 3 bodyguards + Corro (4) | 600 + 25 = 625 | 2 | 1,250 | Medium |
| S11 (Corro not counted) | 3 | 600 | 2 | 1,200 | Medium |
| S12 | 3 knives | 600 | 2 | 1,200 | Medium |
| S12 heat 4 | 4 knives | 800 | 2 | 1,600 | Hard |
| S13 | Draunel + Veteran + duelist (3) | 700 + 450 + 200 = 1,350 | 2 | 2,700 | **Deadly** |
| S14 | Attendant, 229 HP (1) | 3,900 | 1 | 3,900 | Deadly (1.95 ×) |

### 5c. Things the arithmetic does not capture (the module's own play notes)
- **Early morale:** S7 (first knife Bloodied), S9 duelists (first damage), S2 knives (first charge), S3 (sergeant down or half the Blades), S8 (two down), S13 (Draunel the moment it is seen as his). These plus 4-segment clocks are why the module labels fights below their sum.
- **Detain-only foes:** S4, S8, S3 Blades (to 1 HP + Grappled); before midnight nobody dies (Table IX–4).
- **Never break:** Maiven (S10), Honor Guards (S4; they offer terms instead), the Attendant.
- **Action-economy outliers:** Essar Draunel and Maiven (3 attacks), the Veteran Bought Sergeant (3), Tavva and Essin (Sneak Attack), and the Focused Attendant (two turns a round; the full Multiattack on both for four).
- **Not foes of the party:** S11 bodyguards are not hostile unless crossed; S10 only if provoked; S12's four yard-gate Blades are terrain.

---

## 6. Summary

| Fight | Printed 3p label (SRD 5.2.1) | 3p 2014 band (printed roster) | Four-char roster raw / adjusted | 4p 2014 band |
|---|---|---|---|---|
| S1 Seating Feud | 175, under Low | Easy (437.5) | 225 / 562.5 | Easy |
| S2 Service Corridor | 550, under Low (plays Low) | Medium (1,100) | 600 / 1,200 | Medium |
| S3 Gate | 850, Low–Moderate (1,950 w/ captain, over High) | Deadly (1,700); 3,900 w/ captain | 1,500 / 3,000 (2,600 / 5,200 w/ captain) | Deadly |
| S4 East Wing Doors | 900, Low–Moderate (2,700 beyond High) | Hard (1,350); 5,400 with the four | 900 / 1,350 (2,700 / 5,400 with the four) | Medium; Deadly with the four |
| S5 Looters | 550, under Low | Medium (1,100) | 600 / 1,200 | Medium |
| S6 Quiet Word | 400, under Low | Easy (600) | 600 / 1,200 | Medium |
| S7 Second Plate | 800, Low (plays High fought out) | Deadly (1,600) | 800 / 1,600 | Hard |
| S8 Study Door | 600, under Low | Hard (1,200 full) | 800 / 1,600 (full) | Hard |
| S9 Appointment (both) | 900, Low–Moderate | Deadly (1,800) | 1,150 / 2,300 | Deadly |
| S10 Over the Wall | 900, Low–Moderate (plays Low) | Deadly (1,800 full) | 1,000 / 2,000 | Deadly (exactly) |
| S11 Phern Door | 425, under Low | Medium (850); Easy if Corro not counted | 625 / 1,250 (600 / 1,200 without Corro) | Medium |
| S12 Corval in Kitchens | 400–600, under Low | Easy (600); Hard at heat 4 (1,200) | 600 / 1,200 (800 / 1,600 at heat 4) | Medium (Hard at heat 4) |
| S13 Arrest in the Fire (Draunel side) | 1,100, Low–Moderate (plays Moderate) | Deadly (2,200) | 1,350 / 2,700 | Deadly |
| S14 Attendant | 3,900, 2.6 × High | Deadly (3,900, 2.6 ×) | 3,900 / 3,900 (229 HP) | Deadly (1.95 ×) |
| Ch V Uninvited / Crossing | no XP (Leashed; hazard only) | n/a | n/a: lump 30, Wept 3rd turn | n/a |

**Headline:** on the printed four-character lines, 2014 rates **6 fights Deadly** (S3, S9 both sides, S10, S13, S14, and S4 once the reinforcements arrive), **3 Hard** (S7, S8 full, S12 at heat 4), and the rest Medium or Easy. Over 4p Deadly by a wide margin: S3 with the captain (5,200), S4 with the four (5,400), and S14 (3,900).

**Discrepancies to note:**
- S7's printed four-character line keeps 800 XP ("under Low for four").
- S1's printed totals for Five, 4@3rd and 4@5th are missing (computed here: 275 / 150 / 275).
- S4's Five and 4@5th totals are missing (1,800 each).
- S9's Five and 4@5th totals don't include Essin (+450 if he is hostile).
- S7's 4@5th line adds S2's crew without a total.
