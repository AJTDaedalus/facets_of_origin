# Oraga Night (5e): Three-Player Tuning Audit

*Scope: every fight card (S1–S14), the midnight pressure systems (Delay, the Attendant,
Down Not Out, the crowd rule, clocks, Snake Tracker heat), attrition across the night,
and agenda and role coverage, for **three 4th-level PCs**. Module files were read, not
edited. Simulation code lives only in the session scratchpad, not in the repo. Nothing
under `references/oraga_night/` was opened or cited.*

All paths below are relative to `conversions/dnd5e/oraga_night/`.

---

## 1. Verdict

**Score for 3-PC tuning: 7 / 10.** A three-player table can run it as written: nothing
in it breaks (no P0). The per-card "three characters" lines are better than what WotC
usually prints (most official adventures give one weak/strong sidebar, if that), and the
boss card, S14, holds its odds at three PCs. If anything it is slightly kinder at three
than at four.

It falls short of official quality in three places:

1. **Setup.** The book never says which three pregens to deal, or which agendas a
   three-player table cannot do without. The only guidance anywhere is for four players.
2. **Fights the lines do not reach.** First, a single PC who walks into a Movement V card
   alone faces the whole three-character roster and drops 70–100% of the time. Second,
   after midnight the dying rules are unclear, and in snake fights fought to the end that
   lets a PC actually die (simulated 5–21% across S13 + S3). Third, the night allows no
   rest after midnight, so a party with one healer or none reaches the gate at about
   15–20% of its Hit Points.
3. **The DM sheet.** The two-page sheet the DM is told to run from prints only the
   four-player numbers (the 30-damage lump, the Wept's third turn). Three cards, S8, S10
   and S4, get three-character lines that keep 4P morale or rosters, so the card's "plays
   Low" claim is false at three.

None of the fixes below is large; together they are about two pages of edits.

> Correction to the brief: the SRD 5.2.1 "XP Budget per Character" table (SRD p. 202,
> fetched and checked) gives **4th level: Low 250 · Moderate 375 · High 500** per
> character. "500/750/1,100" is the **5th-level** row. For **three 4th-level PCs** the
> budget is **Low 750 · Moderate 1,125 · High 1,500**. The module's Table IX–1
> (`09_The_Snakes.md:137-145`) and `10_Bestiary.md:16-19` are correct.
>
> SRD p. 203's own troubleshooting matters here. "More than two creatures per character"
> means more than **6** at three PCs, and only S1 (7 brawlers, nonlethal) goes over. The
> SRD also warns about a creature whose CR is above party level (the Attendant, CR 8).

---

## 2. Method

**SRD check.** The SRD 5.2.1 PDF was downloaded from media.dndbeyond.com and the budget
and troubleshooting text read directly (pp. 202–203).

**Monte Carlo (scratchpad only):**

- `s14.py`: the Attendant fight. It models Idle/Focused, Two Turns, Clears the Way,
  Put Aside, Down Not Out, the crowd rule, and the distraction rule (DC 13/19, +2/+2,
  repeats at Disadvantage, one trick a round, success-by-5 loses a turn). It also models
  Heroic Inspiration, Bardic Inspiration and Cutting Words, Tactical Mind, Shield, Sap,
  Vicious Mockery, Healing Word, and the Wept's Delay clock and progress, with optional
  Wept strikes on PCs in reach.
- `skirm.py`: a generic engine for S2, S3, S4, S7, S8, S9, S10 and S13, using every
  block's real numbers and its morale trigger. It covers To the Terms, Parry, Sneak
  Attack, smoke and fire, wicket single-file entry, the captain's arrival and The Read,
  death saves, and two readings of the crowd rule.
- `chain.py`: the post-midnight run of S14, then S13, then the S3 fight, with Hit Points
  and slots carried forward and no rest.
- Each cell is 2,000–6,000 runs.

**Parties tested** (the three likeliest, plus the two weakest):

| Code | Party | Shape |
|---|---|---|
| C1 | Dassa / Ilesse / Serane | front, healer, talker |
| C2 | Dassa / Ilesse / Andra | front, healer, arcane |
| C3 | Dassa / Pello / Ilesse | front, striker, healer |
| C4 | Dassa / Pello / Andra | **no healer** |
| C5 | Serane / Andra / Pello | **no front line, no cleric** (worst) |
| 4P | Dassa / Ilesse / Serane / Andra | 4P baseline (the book's "leave out Pello") |

**Policies for S14:**

- *slug*: everyone hits it.
- *distract, engaged*: the best trick each round, played out in character and using a
  habit the table has seen.
- *distract, naive*: bare rolls, rarely leaning in.
- *smart*: distract, keep one PC adjacent, and buy Delay when the initiative order makes
  it free.
- *delay-max*: one tank, everyone else runs room tricks.

**The errand clock.** By default the card fires with 1 Delay on the Wept and her moves
left at 6 (3P) or 5 (4P), which gives the book's "about six rounds". The *tight* variant
(3 or 2 moves left) models a card that fires late.

**Caveats.** Fights run to their morale trigger, with no outs taken. Real tables take
outs, which pay the same XP, so snake-fight numbers are a ceiling on danger. Positioning
is abstract. The distraction bonuses assume a generous but rules-legal DM: the Orthaen
gift gives Advantage on a crystal trick, and Dassa may use Athletics for a thrown light.

### Key expected-damage arithmetic (hit chance × average)

| Attacker | vs AC 14 (Serane, Ilesse) | vs AC 16 (Dassa, Pello) | Notes |
|---|---|---|---|
| Attendant, Joined Hands (+7, 9.5) | 0.70 × 9.5 ≈ **6.9** | 0.60 × 9.5 ≈ **6.0** | Focused 4P: 4 attacks ≈ 24–28/rd. **3P line: 3 attacks ≈ 18–21/rd.** Idle: 1 attack at Disadvantage ≈ 3.4–4.7 |
| Put Aside (2d8 = 9, DC 15 Str) | ≈ 7.9 per PC caught (Str save −1) | Dassa ≈ 6.3 | Recharge 5–6 Focused |
| The Wept (2 × +10, 28) | 0.85 × 28 × 2 ≈ **48** | 0.75 × 28 × 2 ≈ **42** | Drops a squishy PC in one turn 69–82% of the time (Down Not Out) |
| Essar Draunel (3 × +5, 7.5) | ≈ 13.5/rd | ≈ 11.3/rd | S13 |
| Maiven (3 × +5, 6.5) + 2 slingers | ≈ 12.2 + 6.6 = **18.8/rd** | ≈ 16/rd | S10; she never breaks |
| Tavva (2 × +5, 5.5, +SA 7) | ≈ 6.6 + 5.9 = **12.5/rd** | ≈ 11/rd | S2/S5 |
| Veteran Bought Sergeant (4P) / Bought Sergeant (3P) | 13.5 / 7.2 | 11.3 / 5.9 | S3 |

**Round-one drop chance when the Focused Attendant puts everything on one PC (Put Aside
included):**

| Target | 3P line (3 attacks) | 4P (4 attacks) |
|---|---|---|
| Serane or Ilesse | 24% | 49% |
| Andra with Shield | 18% | 36% |
| Pello | 18% | 36% |
| Dassa | 4% | 14% |

The 3P line roughly halves the nova risk.

---

## 3. Per-card table (three 4th-level PCs: Low 750 · Moderate 1,125 · High 1,500)

"Sim" is the chance at least one PC drops if the fight runs to its morale trigger. Where
a range is given it spans C1–C5; C1 is usually the high end, because its damage is low
and fights last longer.

| Card | 3P line, as written | 3P label by XP (4P label) | Real danger at 3P | Verdict | Fix |
|---|---|---|---|---|---|
| **S1** Seating Feud | 6 kinsmen + principal, 175 XP | under Low, 0.23× (0.23×) | Nonlethal brawl; the clock is the fight | **OK** | — |
| **S2** Service Corridor | Tavva + 2 knives, 550 | under Low, 0.73× (0.60×) | Sim 13–37%; 25–63% if the crew focus-fires the softest PC. **A solo PC drops 71–100%** | OK together; **P1 when alone** (F2) | Solo line (F2); box says "Four people" (F11) |
| **S3** Gate | Bought Sergeant + 4 Blades, 850; captain 1,950 | Low–Mod 1.13× (Mod 1.0×); with captain 1.3× High (1.3×) | Fight-through, single file, lethal: C1–C4 14–32%, deaths ≤0.5%. **C5 83%, whole party down 26%, deaths 2.9%.** To the last with the captain: 99%, deaths 6–9% | OK for parties with a front line; harsh without | 3P: captain arrives at the start of round 4 (F9) |
| **S4** East Wing Doors | 2 Honor Guards, "as printed", 900 (+4 = 2,700) | Low–Mod 1.2× (0.9×); 1.8× High with the four | Fought before the reinforcements: C1 86%, 3.0 drops. Nonlethal, not meant to be won | Only card with no 3P reduction | 3P: one guard at the door, the second arrives at the start of round 2 (F12) |
| **S5** Looters | Tavva + 2, 550 | under Low, 0.73× | As S2, no clock | **OK** | — |
| **S6** Quiet Word | 2 cousins, 400 | under Low, 0.53× | Fists and Quiet Word, 3 damage plus a grapple | **OK** | — |
| **S7** Second Plate | 3 knives, 600 | under Low, 0.8× (0.8×) | Over in about 1 round, ≤4%. Nastier: 21–59% | **OK** | — |
| **S8** Study Door | 3 wardens, 600 | under Low, 0.8× (0.8×) | **20–57%** (C1 57%; 4P 41%). "Break when two are down" is 2 of 3 at 3P, 2 of 4 at 4P | Plays Low–Moderate for low-damage parties; the card says "well under Low" | 3P: they break when **one** is down → 5–16% (F7) |
| **S9** Appointment | 2 duelists + 2 cousins, 600 | under Low, 0.8× (1.15×) | To the last: 23–59%. Duelists break on first damage | **OK** (easier than 4P) | Clarify the one-side rosters (F13) |
| **S10** Over the Wall | Maiven + 2 slingers, 900 | **Low–Mod 1.2× (exactly Low)** | **44–82%, up to 2.5 drops** (4P: 74%). Maiven never breaks | **Plays Moderate, not Low** (P2) | 3P: Maiven + 1 slinger (800), and she pulls her blows (two attacks) → 6–23% (F6) |
| **S11** Phern Door | 2 bodyguards, 425 | under Low, 0.57× | The crush is the fight; the "hold the door" out is DC 13 Athletics | **OK** | — |
| **S12** Minister in Smoke | 2 knives, 400 | under Low, 0.53× | Break on first Bloodied | **OK** | — |
| **S13** Arrest in the Fire | Draunel + 1 duelist, 900 | Low–Mod 1.2× (1.35×) | To Draunel Bloodied, with smoke and fire: 39–74%; **PC death 2.7–6.4%** (strict crowd reading). To the last: 70–93%, deaths 7–13% | XP fine; "plays Moderate" holds. **Lethality is a rules gap** (F3) | Dying-rule fix (F3); box says "three men" (F11) |
| **S14** Attendant | 180 HP; second Focused turn is one Joined Hands; 3,900 XP | **2.6× High** (4P 1.95×; the card text says "nearly twice") | Win odds: engaged distraction **90–96%** (4P 90–91%); naive **57–75%** (4P 54–61%); slugging 0–34% (4P ≈0%). At least one drop: 24–32% fresh, 55–64% attrited. Party all down at once: <1% fresh. Round-1 focus-fire drop: 18–25% (4P 36–49%) | **Well tuned**; slightly kinder than 4P | Label (F14); 3P "built to hit hard" = 235 HP (F8) |

---

## 4. Findings

### P0: unplayable

None.

### P1: real defects at a three-player table

**F1. No three-player setup guidance: pregens, agendas, the Agenda 4 dependency.**

*Where:* `README.md:8-10`, `01_Overture.md:219-221`, `03_Masks_and_Agendas.md:196-199`,
`11_Pregenerated_Characters.md:29-31`. Each says only "with four players, leave out
Andra or Pello; leave out Ilesse only if another player takes Agenda 4."

*At the table:* three players pick the fun trio, Dassa, Pello and Andra. Nobody carries
Agenda 4. The east-wing scene is cut by the runtime rules
(`01_Overture.md:204-207`), Undercurrent C is skipped, and nobody stands beside Veier
when the Crossing comes. Chapter V "leans on" exactly that. There is also no healer. The
chain sim gives that party no healing beyond Second Wind across S14, a snake card and
the gate, and it reaches the gate at about 20% of its Hit Points. Alternatively, a table
deals agendas face-down (the book allows this) and Agenda 4 never comes up.

*Fix:* add a "With three players" paragraph to ch. I step 1, ch. III and ch. XI:

> **With three players,** deal **Ilesse (Agenda 4), Dassa and Serane**, and leave out
> Andra and Pello. Give Dassa *The Vanished Servant* (Agenda 8: the service passages at
> midnight) and Serane *The Prelate's Question* (Agenda 2) or *A House's Long Game*
> (Agenda 3). Do not deal agendas face-down at three: Agenda 4 must be in play. A table
> that wants more steel can swap Serane for Pello; keep Ilesse either way.

**F2. A lone PC in a Movement V card faces the whole three-character roster.**

*Where:* `09_The_Snakes.md:505-512` ("run one card per group of characters … if it has
split three ways, it is three, one each"); `04_The_Ball.md:1324-1327`;
`08_Handouts.md:22` ("One per group"); `04_The_Ball.md:446` ("Four players will be in
four rooms by Movement II. That is the design"). No card has a line for one or two
characters in the scene.

*At the table:* the Dead Dance splits a three-PC party three ways, and Serane follows
the gray robes alone. Simulated drop rates for one PC against the 3P line:

| Lone PC vs | Dassa | Pello | Serane | Andra | Ilesse |
|---|---|---|---|---|---|
| S2 (Tavva + 2) | 71% | 91% | 100% | 100% | 99% |
| S8 (3 wardens) | 89% | 99% | 100% | 100% | 100% |
| S10 (Maiven + 2) | 97% | 100% | 100% | 100% | 100% |
| S7 (3 knives) | 19% | 33% | 100% | 51% | 52% |

Before midnight that is nonlethal, but the card's objective is lost, its clock fills
(S7 sends Circle heat to 4), and the PC carries the damage into midnight with one
optional Short Rest. The same flaw exists at four players, but three is where a solo PC
is likeliest.

*Fix:* one rule in "Running the Snakes" (`09_The_Snakes.md:91-97`), with a mirror on
the DM sheet:

> **Size a card to who walks in, not to the table.** Use the three-character line for
> two characters. For **one character**: S2, Tavva alone. S7, one knife, and the clock
> advances only when he gets past. S8, one warden at the door and one on the stair; they
> break when one is down. S9, it is the formal duel: one duelist, one cousin. S10,
> Maiven alone, pulling her blows (two attacks).

**F3. After midnight, the "crowd rule" does not clearly save a dying PC, so snake fights
can kill.**

*Where:*

- `05_The_Longest_Night.md:215-219`: "If a **Stable** character is still down…"
- `05_The_Longest_Night.md:232-235`: "Everything else tonight (the snakes, the Bought)
  uses the ordinary rules for dying, except that the crowd rule holds…"
- `09_The_Snakes.md:549-552`
- `09_The_Snakes.md:1698-1704`: S13 fire, whose "Stable" applies only to fire drops.

A PC dropped by a snake's blade is *dying*, not Stable. Read literally, the crowd rule
never touches them.

*At the table:* in S13, in the smoke, the duelist drops Serane. Dassa is coughing (DC 10
Con or lose the action) and Ilesse is the only other PC standing. With nobody free,
unaided death saves kill **40%** of the time, and every "come round with 1 HP" puts a PC
back on its feet next to an enemy. Over a fought S13 plus the S3 fight, a PC died:

| Reading of the crowd rule | 3P | 4P (bigger rosters) |
|---|---|---|
| Strict (as written) | 15–21% | 24–26% |
| Generous (dying PCs dragged clear like Stable ones) | 5–7% | 8–10% |

That contradicts the book's own register ("no fight in this module is to the death by
default", `01_Overture.md:147-148`) at exactly the moment a one-shot cannot absorb a
dead PC.

*Fix:* replace the sentence at `05_The_Longest_Night.md:232-235`:

> Everything else tonight (the snakes, the Bought) uses the ordinary rules for dying,
> with one mercy: **after midnight, a character who drops to 0 Hit Points in a snake
> fight is dragged clear by the crowd at the end of that round and is Stable**, and the
> crowd rule gets them up as above. A character dropped twice in one scene stays down
> until the scene ends.

The last clause stops the 1-HP pinball. Mirror it on the DM sheet and at
`09_The_Snakes.md:549-552`.

**F4. The DM sheet prints only four-player numbers for midnight.**

*Where:* `08_Handouts.md:64-70` ("30+ damage to one in a round → 1 Delay"); Table
VIII–2 and page two have no Attendant HP and no Wept turn count. The three-character
values live only in `05_The_Longest_Night.md:285-297` (Wept on her **fourth** turn,
**20** damage for a lump) and the S14 card (`09_The_Snakes.md:1920-1921`, 180 HP, single
second-turn attack). Chapter I says to run the night from the sheet
(`01_Overture.md:3-6`; `README.md:98-99`).

*At the table:* mid-attack, the DM reads "30+" off the sheet. The trio deals 24 to the
Wept and earns nothing, and the Wept reaches Raunu a turn early, so the three-character
compensation for the dais is silently lost. If the DM also misses the S14 line, the
Attendant runs at 229 HP with 4 attacks a round. That doubles the round-one drop risk
(24% → 49% on Serane) against a party with three bodies.

*Fix:* add one line under "Midnight rules" on page two:

> **Three characters:** Wept reaches Raunu on her 4th turn · a lump is **20** damage ·
> Attendant **180 HP**, Focused second turn = one Joined Hands · S3: Bought Sergeant, not
> the veteran.

Add a "3P" column to Table IX–3 (`09_The_Snakes.md:520-535`).

**F5. Attrition: no rest after midnight, healer-dependent, and the "steel dial" has no
three-PC cap.**

*Where:*

- `01_Overture.md:285-286` and `04_The_Ball.md:286-287`: the only Short Rest costs a
  whole Movement in the chapel.
- `09_The_Snakes.md:493-503`: "three or four fights in sight at once"; "show two or
  three [lines]".
- `05_The_Longest_Night.md:895-898`: the combat dial.
- `10_Bestiary.md:2155-2232`: no healing items of any kind.

*At the table:* this is a realistic night for a three-PC party that likes a fight. One
Movement V card, then S11 (the default live card), then S14, then one dark snake card
(S13), then the gate. Simulated party HP on reaching the gate:

| Path | 3P | 4P |
|---|---|---|
| S14 + S13, no Movement V fight | 15–21% | 10–12% (bigger rosters) |
| Movement V card + S14 + S13 | 5–9% | 4–5% |

The party then starts S3 one hit from the floor. A three-player table feels this more
because the whole healing pool sits on one PC (Ilesse). Without her (C4, C5) there is no
healing at all beyond Second Wind or Serane's four Healing Words. Spending a Movement in
the chapel takes a third of the party out of the social game for 35–45 minutes of play.
At four players that is a quarter.

*Fix (all three):*

- (a) At `09_The_Snakes.md:498`: "**At a three-character table, no more than one snake
  card is live after midnight besides S11**; the rest happen offstage."
- (b) At `01_Overture.md:285`: "**With three characters,** the chapel's Short Rest takes
  half a Movement, and at the toast each character may spend one Hit Die."
- (c) In F1's pregen guidance: always include Ilesse.

The gate stays safe whatever the HP. Ending 2 (void the contract, DC 13) and ending 3
(hold) need no fight, and the book already says so at `09_The_Snakes.md:835-864`. The
risk is a tired table choosing to fight through.

### P2: rough edges a careful DM will catch, and a careless one won't

**F6. S10's three-character line plays Moderate, not the Low the card claims.**

*Where:* `09_The_Snakes.md:1449-1455` ("it plays Low") and `09_The_Snakes.md:1494`
(*Three characters: Maiven and two slingers, 900 XP*).

900 XP is 1.2× Low at three PCs, and the 4P card is exactly Low. Maiven's three attacks
are unchanged and she never breaks (*Thirty Degrees Hotter*). Simulated: 44–82% at least
one drop, up to 2.5 drops (C1). Even the 4P card runs 74%, so "plays Low" is optimistic
at any size.

*Fix:* "*Three characters:* Maiven and one slinger (800 XP), and she pulls her blows:
Multiattack is two attacks." Simulated: 6–23%, which is Low by the module's own
definition at `09_The_Snakes.md:105-109`.

**F7. S8's morale trigger does not scale.**

*Where:* `09_The_Snakes.md:1242-1243` and `09_The_Snakes.md:1262` ("break when two are
down"); `09_The_Snakes.md:1298-1299` (3P: three wardens).

Two of three at 3P is far harder than two of four at 4P. Simulated: C1 57% at least one
drop and C5 49% (4P 41%), while the card promises "well under Low".

*Fix:* "*Three characters:* the two at the door and the third on the stair; the fourth
never comes, and they break when **one** is down (600 XP)." Simulated: 5–16%.

**F8. S14's "A table built to hit hard: 300 Hit Points" is not scaled by party size, and
its "use one line" rule is ambiguous.**

*Where:* `09_The_Snakes.md:1808-1812` and `09_The_Snakes.md:1927`. Since
`09_The_Snakes.md:96` says to use one line only, a DM with three damage-built PCs must
choose between 180 HP and 300 HP.

Simulated slugging by Dassa / Pello / Andra:

| Attendant HP | Wins by blows |
|---|---|
| 180 | 34% |
| 235 | 1.6% |
| 300 | 0% |

For comparison, the 4P damage party wins 10.6% at 229 HP and 0.1% at 300, so "can
out-slug it" is also loose at four.

*Fix:* "*A table built to hit hard:* 300 Hit Points with four characters, **235 with
three**, 340 with five; it combines with the party-size line's other changes."

**F9. S3 leaves the captain untouched at three PCs, and the wicket punishes a party with
no front line.**

*Where:* `09_The_Snakes.md:793-795` and `09_The_Snakes.md:883-884`.

A party that goes through single file meets five foes one PC at a time. C5 (Serane,
Andra, Pello) drops someone 83% of the time and goes entirely down 26%. With the captain
fought to the last, PC death is 6–9% at any size.

*Fix:* "*Three characters:* a **Bought Sergeant** and four Blades (850 XP); the captain
arrives at the start of the **fourth** round (three bell segments filled)." Also add to
the field: "A party of three that holds the court and talks through the grille loses
nothing by waiting." That is already true; say it at three.

**F10. The Delay economy weakens at three, and an exploit holds at every size.**

*Where:* `05_The_Longest_Night.md:237-283` and `09_The_Snakes.md:1782-1793`.

*Weaker at three.* The Wept spends 1 Delay a round and Clears the Way removes 1 a round.
Both are fixed costs that do not shrink with the party. In the S14 scene a "smart" table
banks about **1.5–2.0 Delay at three PCs against about 3.0 at four** (−40%). The Wept's
fourth-turn line repays one turn, once. So at three, ⟨They save Raunu⟩ and the Wept's
easy Fracture DC (15 at 2+ Delay) come up less often. That is acceptable, but the book
should say so.

*Exploit, at any size.* One PC stands next to the Attendant, so it is blocked from
Clears the Way and stays Idle. The other two spam room tricks (8 printed tricks × 2 uses,
plus ward-points, plus invented tricks "worth the same"). That stalls the Wept for **5.3
of 6 rounds at three PCs and 5.9 of 6 at four**. It holds even when she strikes every
trick-doer in reach (2–4 Down Not Out drops per scene, none of which costs anything).
Down Not Out makes the stall free, and nothing in the rules caps it except the DM's sense
of pacing.

*Fix:* "**An Uninvited loses at most four turns in one scene to Delay (three with three
characters).** Delay she would spend beyond that is spent on lives instead: a dozen
guests out, per Table V–1." Add to "Adjusting the Attack": "*Three characters:* expect
fewer hallways; that is the night bending toward the record."

**F11. Midnight in initiative order is under-specified, and the result depends on
initiative.**

*Where:* `10_Bestiary.md:217-224` and `10_Bestiary.md:256-260`. The rules do not say on
which of the Attendant's two turns Clears the Way happens, and Focus is checked at the
start of its turn while the Wept spends Delay at the start of hers.

So the order in which the Wept and the Attendant act changes the result. Simulated at
3P, tight clock: Wept first, win 35% and 5.2 Delay bought; Attendant first, 24% and 4.5.
At 4P, book clock: 82% against 75%. A table cannot see why the same play worked one
night and not the next.

*Fix:* "Clears the Way happens at the start of its first turn each round, before the
Focus check," and "if the Wept and the Attendant tie or are adjacent in initiative, the
Wept acts first."

### P3: polish

**F12. S4 is the only card whose three-character line changes nothing.**
`09_The_Snakes.md:943` ("two guards, as printed"). Before the reinforcements it is 1.2×
Low at 3P and drops someone 54–86% of the time if fought. Nobody dies, but HP is lost
before midnight. *Fix:* "*Three characters:* one guard at the door, the second at the
start of round 2."

**F13. Read-aloud head counts contradict the three-character lines.**

- S2: "Four people" (`09_The_Snakes.md:649`), but the 3P line is Tavva + 2.
- S11: "three big men" (`09_The_Snakes.md:1519`), but 3P is two bodyguards.
- S13: "three men in good coats" (`09_The_Snakes.md:1661`), but 3P is Draunel + 1.
- S9's 3P line (`09_The_Snakes.md:1406`) removes the veteran, but its Nastier line
  (`09_The_Snakes.md:1403`) still refers to "the principal's" Veteran block. It also
  never says what a one-side fight is at three: 2 duelists (400) or 2 cousins (200).

*Fix:* add "*(with three characters, three / two / two)*" after each count. For S9:
"*Three characters:* Draunel side, two Draunel Duelists (400); Boranis side, two
Cousin's Blades (200); both, 600."

**F14. S14's budget label is false at three.** "Nearly twice High"
(`09_The_Snakes.md:531`, `09_The_Snakes.md:1798-1799`, `10_Bestiary.md:312-313`) is
**2.6× High** at three PCs. *Fix:* "(about 2½× High for three)". Also, the "DM Note —
how it plays" says slugging fights "fairly" often end with the whole party down
(`09_The_Snakes.md:1816-1818`). The sim never reproduced that above 4% at either size,
because Down Not Out and the "interferers only" targeting prevent it. Soften to "it
usually goes the Attendant's way."

**F15. The runtime and spotlight text assume four.** `01_Overture.md:180` ("minutes
below are for four players") and `04_The_Ball.md:446` ("four rooms"). *Fix:* "With three
players, Movements I–V run 10–15% shorter; spend the slack on one Undercurrent." In
practice three players get about 33% more spotlight each, which is good for agendas.

**F16. Role gates at three: none are hard, but three are soft.**

- Carrying Veier needs Str 13+ (`05_The_Longest_Night.md:587-590`), and only Dassa has
  it. The Help route works, so this is no gate.
- Thieves' Tools: only Pello is proficient. Serane's Jack of All Trades gives +3, so the
  study lock is 30% and private doors 45%. Alternate routes exist (S8, the keys,
  Undercurrent A's improvised route).
- The service passages without a guide: DC 15 Survival (`08_Handouts.md:115`), which
  Agenda 8 removes.

*Fix:* covered by F1's pregen and agenda picks.

---

## 5. Night structure and attrition at three PCs

**How many fights?**

- *Before midnight:* one of S1/S6 (Movements II–III) and one Movement V card per group.
- *After midnight:* S11 is live by default (Phern heat 3, `09_The_Snakes.md:475-481`).
  S14 fires almost every time, because Delay is the night's main game and earning any
  fires it. Add 0–1 more snake card (only lines the table let slide) and the gate.

A typical three-PC night is **5–6 encounters, 3–4 of them fought**, two or three after
midnight with no rest possible. An optional Short Rest costs a Movement.

**Is there enough to go round?** Party C1 has about 102 HP. Its healing pool is roughly
140 HP: Ilesse's 7 slots at about 11 each, plus Preserve Life × 2, plus Serane's
Healing Words. Second Wind adds about 28. A combat-hungry path loses about 200 HP:

| Fight | HP lost (C1) |
|---|---|
| Movement V card | ~48 |
| S14 | 40–60 |
| S13 | ~60 |
| S3 fight | ~41 |

That is survivable only if Ilesse spends almost everything on healing (so no Spiritual
Weapon). Without Ilesse it is not survivable, which is why F1 and F5 rate P1. Hit Dice
are effectively dead weight unless the party takes the chapel Movement.

**Down, Not Out at three.** It kills nobody, so the lethality is toothless. The action
economy is not: each drop takes a third of the party out for up to two rounds, and
rousing costs another action unless someone casts Healing Word. In S14, drops per fight
run 0.3–1.3, and the whole party is down at once in under 1% of fresh fights and 0.3–4%
of attrited ones. That is swingy but safe, which is the design intent. The real
lethality is in the snake fights (F3).

**The dark hour's "three or four fights in sight".** At three PCs this means the party
can take at most one of them. The cards are concurrent: S11 fires in the first seconds,
S14 at the dais, Maiven in the east wing, Agenda 4 at Veier's side. A three-PC party
covering two of those places has one PC alone in a scene. Card S14 alone, against a solo
PC, is still won by the distraction game (one trick a round is a solo-friendly limit),
but the lone PC takes the full Focused offense. Apply F2's "size to who walks in" to S14
as well: with **one character** in the scene, the Focused second turn makes no attack.

## 6. Non-combat pressure at three PCs

- **Clocks** count rounds, not people, so they do not scale with party size, and the
  outs are single checks. One exception: in S13's gallery clock (one guest per segment)
  and S11's "hold the door", every PC who fights is a PC not carrying or holding. At
  three, more guests are lost. That is acceptable and thematic.
- **Snake Tracker heat** scales itself. It rises only for lines the table was shown, and
  three PCs see fewer. The default midnight state (Circle 2, Church 2, Draunel 2,
  Boranis 1, Phern 3, Thenya 3) leaves only S11 live, the same at any size. The catch is
  cooling. Three of the "to 0" exits are agendas (1, 2, 3), and at three players at most
  one or two are in play, so at least one snake can only be cooled by its −1 boxes.
- **Agendas: 8 written, 3 dealt.**
  - Must-have: **4** (the east wing and the Crossing; chapter V leans on it).
  - High value: **8** (the service passages: S11's out, carrying guests without a check,
    Movement VII) and **2** (watching Raunu; the Kovaun lever in S8).
  - Agenda 5's benefit, ward steering at DC 13, is also open to any Orthaen PC who reads
    the wards by hand (`05_The_Longest_Night.md:37-41`), so losing it costs little.
  - **6** goes unused harmlessly: Vell unlocks the gate himself
    (`04_The_Ball.md:1362-1365`).
  - **1, 3, 5, 7** go unused harmlessly; their snake lines run on tells alone.
- **Skill density** per player rises by about a third. Social outs (DC 13–15 Charisma)
  rest almost entirely on Serane (+8). Without her, the party's best Persuasion is
  Ilesse's +4, and the outs turn into coin flips. That is why F1 keeps Serane by default.
  Fracture checks (DC 15–18; Persuasion, Performance, Religion, Insight) are covered by
  Serane and Ilesse.

## 7. Rules clarity of the scaling

Good: every fight card carries a three-character line, and "use one line only" is stated
in three places (`01_Overture.md:45-46`, `09_The_Snakes.md:96-97`,
`05_The_Longest_Night.md:287-289`). Missing or unclear:

- The DM sheet (F4).
- Pregen and agenda guidance (F1).
- Solo or partial-party sizing (F2).
- Party-size scaling for the "built to hit hard" line (F8).
- Read-aloud counts (F13).
- The labels at three PCs (F14).
- S9's one-side fights (F13).
- The dying rule (F3).

Nothing on Delay or the Radiant is party-size dependent except the Wept and lump lines,
and that is correct.

---

## 8. Recommended 3-player configuration

**Pregens.** **Dassa (Fighter), Ilesse (Cleric), Serane (Bard)**, with Andra and Pello
left out.

- This party's S14 numbers are as good as any: 90% engaged win, lowest drops.
- It is the only trio that covers Strength (carrying Veier, holding doors), healing, and
  the social outs.
- Its weakness is damage output, so grindy fights run long (S8 57%, S10 82% as written).
  Fixes F6 and F7 close that, and the table should be told plainly that **outs pay full
  XP**.
- **Combat-leaning alternative:** Dassa / Pello / Ilesse. It is the most robust in
  fights (S8 23%, S10 45%, S3 16%) but weak socially.
- **Never** run a trio without Ilesse unless someone else plays a healer.

**Agendas.** Ilesse **4** (Cousin's Errand) · Dassa **8** (Vanished Servant) · Serane
**2** (Prelate's Question). Deal them openly, not face-down.

**Adjustments to apply.** Use every card's *Three characters* line, plus:

- **F2**: size each card to the PCs actually present; one PC gets the solo roster.
- **F3**: after midnight, a PC dropped by a snake is dragged clear and Stable at the end
  of the round; dropped twice, they stay down.
- **F5**: at most one snake card after midnight besides S11. The chapel rest takes half a
  Movement, and each PC may spend one Hit Die at the toast.
- **F6**: S10 is Maiven + 1 slinger, and Maiven makes two attacks.
- **F7**: S8 wardens break when one is down.
- **F8**: a damage-built trio faces a 235-HP Attendant.
- **F9**: at S3 the captain arrives at the start of round 4.
- **F10**: an Uninvited loses at most three turns per scene to Delay; spare Delay saves
  guests instead.
- **F12**: S4 is one guard plus one in round 2.

### One-page cheat: three characters

```
PARTY        Dassa + Ilesse + Serane.  Agendas 4 / 8 / 2, dealt openly.
BUDGET       3 × 4th: Low 750 · Moderate 1,125 · High 1,500 (SRD 5.2.1).
EVERY CARD   Use its "Three characters" line. Size to who walks in:
             2 PCs = 3P line; 1 PC = S2 Tavva alone · S7 one knife ·
             S8 one warden (+1 on stair), break at one down · S9 the formal duel ·
             S10 Maiven alone, two attacks.
S3 GATE      Bought Sergeant + 4 Blades (850). Captain at start of ROUND 4.
             Void (DC 13) or hold = win. Never a second sergeant.
S8           Three wardens; break when ONE is down.
S10          Maiven + 1 slinger (800); Maiven makes 2 attacks; never breaks.
S4           One honor guard; the second at the start of round 2.
MIDNIGHT     Wept reaches Raunu on her 4th moving turn.
             Lump = 20 damage to one Uninvited in a round → 1 Delay.
             Max 3 Wept turns lost to Delay per scene; spare Delay = a dozen guests out.
S14          Attendant 180 HP (235 if the trio is built to hit hard).
             Focused: 2 turns; 2nd turn = ONE Joined Hands (none if only 1 PC present).
             Distract: action, one try/round, DC 13 Idle / 19 Focused, +2 played out,
             +2 seen habit (max +4); repeat = Disadvantage, never a 3rd time.
             4 broken focuses = it leaves. Say "locked on you" / "drifting" every round.
DYING        Uninvited/Attendant drops: Stable; up within 2 rounds (Down, Not Out).
             Snake drops after midnight: dragged clear, Stable at end of round;
             dropped twice in a scene = stays down till scene ends.
STEEL CAP    After midnight: S11 + S14 + at most ONE other snake card + the gate.
REST         Chapel Short Rest = half a Movement. One Hit Die each at the toast.
XP           Card XP for the party ÷ 3. Outs pay the same. 5th level at dawn.
```

---

## Appendix: headline simulation numbers

**S14, fresh, book clock (win% / at least one drop / Delay bought):**

| Party | Engaged distraction | Naive | Smart | Slug |
|---|---|---|---|---|
| 4P D/I/S/A | 90.1 / 30.7 / 0.83 | 53.8 / 50.5 | 80.5 / 25.3 / 3.06 | 0.3 / 68.4 |
| C1 D/I/S | 90.7 / 25.3 | 63.4 / 39.9 | 89.8 / 23.0 / 1.90 | 0.2 / 63.8 |
| C2 D/I/A | 93.4 / 29.7 | 57.1 / 51.3 | 94.2 / 25.5 / 1.70 | 16.4 / 72.9 |
| C3 D/P/I | 93.7 / 29.9 | 65.9 / 48.7 | 94.0 / 30.2 / 1.60 | 17.6 / 79.4 |
| C4 D/P/A | 95.9 / 23.7 | 67.8 / 42.0 | 95.5 / 23.8 / 1.57 | 34.0 / 70.2 |
| C5 S/A/P | 95.2 / 26.0 | 75.0 / 44.9 | 92.7 / 29.8 / 1.84 | 9.0 / 78.0 |

**S14, attrited** (70% HP, half slots, Heroic Inspiration 50%): engaged distraction wins
79–86% at both sizes; at least one drop 55–64%; round-one drop 1.5–5.7%.

**S14, tight clock** (the card fires late): distraction-only wins at most 6%. Smart play
that also buys Delay wins 22–39% at three PCs, against 8–11% at four. The three-character
Wept turn helps.

**The chain** (S14, then S13, then the S3 fight, no rest): see F5 for party HP on
reaching the gate and F3 for PC death rates. Those figures are a ceiling: they assume no
outs taken.
