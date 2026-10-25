# Oraga Night 5e: simulation notes

*Moved out of the book in the review-fix pass, R3.1 (review finding P2-1; owner ruling QR6,
2026-10-08). The module now prints table advice ("expect one character to drop"); the
numbers behind that advice live here. Book: `conversions/dnd5e/oraga_night/`, chapter IX
(`09_The_Snakes.md`).*

## Where the numbers came from

- **Pass 2, Steel fixer (2026-09-28)** — `docs/LOG_oraga_5e_pass2.md`, "Steel fixer".
  Monte Carlo, 1,500–3,000 fights a cell. Party: four rebuilt 4th-level pregens (Dassa,
  Pello, Andra, Ilesse), plus variants, plus a typical optimized 4th-level party (paladin,
  rogue, sorcerer, cleric). "Drop" means at least one player character reaches 0 Hit Points.
  Source of every per-card drop rate below except S14's.
- **Pass 2, the Attendant re-simulation** — same log, "2 and 3. The Attendant, re-simulated
  and retuned". Rebuilt from scratch: pregens as printed in chapter XI, Heroic Inspiration
  once each, "Down, Not Out" with the crowd rule, six rounds, the card firing with the
  Attendant Idle. 5,000 fights a row for the main table, 2,000 a row for the scaling lines.
- **Official pass, SNAKES-27** — `docs/LOG_oraga_5e_official_audit.md`, Phase 5. Moved the
  numbers into one "DM Note — how it plays" per card, unchanged. Those notes are what R3.1
  removed from the book.
- **Never simulated:** the S3 wicket approach itself; S4 with its four reinforcements
  (logged *Unsimulated* in DECISIONS O21); S14 at 5th level. Rosters changed in R1.4 (the
  promoted Veteran blocks, the fourth retainer) were re-budgeted by arithmetic, not
  re-simulated: the base budgets did not move.

## General guide (Running the Snakes, "the label is the sum")

As printed before R3.1 (09, *Running the Snakes*): a fight that plays **Low** drops a character
in about one run in twenty to one in four; one that plays **Moderate** in one in four to one
in two; one that plays **High** more often than not. Distilled from the per-card table below;
not a separate run.

The 2014 DM Note (09, *Running the Snakes*) also said: "Where a budget line says how the
fight played in simulation, that is the better guide." That note now lives in chapter X's
"At a 2014 table" box, without the simulation clause.

## By card

Drop % = at least one PC hits 0 HP. "Before" is the pass-1 audit's four-pregen column at 3rd
level; "after" is four rebuilt pregens at 4th against the pass-2 base roster. The book's
wording before R3.1 is quoted where a card printed it.

| Card | XP · label (after) | Drop rate (after) | Printed before R3.1 | Before pass 2 |
|---|---|---|---|---|
| S1 | 200 · under Low | 0% | — | 150 · 0% |
| S2 | 600 · under Low, plays Low | ≤6% | "A character drops in about one fight in twenty before Tavva is Bloodied, and in fewer than one in ten if it goes to the last knife." | 600 · 26% (to Bloodied), 41% (to the last) |
| S3 | 1,500 · Moderate | 1% once through the wicket | "Once the party is through the wicket, a character drops in about one fight in fifty." | 850–1,950 · OR 22%, AND 77% all-down |
| S4 | 900 → 2,700 | not simulated | "*Unsimulated.*" | 900 → 2,700 · unwinnable by design |
| S5 | 600 · under Low | 6% | — | 550 |
| S6 | 600 · under Low | 0% | — | 200 |
| S7 | 800 · under Low, plays Low to the last | 12% (to the last) | "Fought to the last knife, about one fight in eight drops a character." | 600 · 23% (to the last) |
| S8 | 800 · under Low | 0% (detain) | — | 600 · 5% |
| S9 | 1,150 · between Low and Moderate | 3% (Draunel side); 49% if both sides go to the last | "Fought to the last against both sides at once, it plays Moderate: about half of those fights drop a character." | 600 · 4% |
| S10 | 1,000 · Low | 7% | — | 900 · 13% |
| S11 | 625 · under Low | 1% | — | 625 · 23% |
| S12 | 600–800 · under Low | 1–11% | — | 400 |
| S13 | 1,350 · between Low and Moderate, plays Moderate | 32%, 0% all-down (Draunel side) | "Against the Draunel side, a character drops in about one fight in three." | 1,100 · 71%, 10% all-down |

S3's pass-2 roster was later re-budgeted at 1,500 (sergeant and four Blades); the drop rate
was measured on the pass-2 roster and not re-run after R1.4's Veteran Bought Sergeant
promotion. S9 and S13 likewise.

## S14, the Attendant

Block as tuned in pass 2: HP 229 (27d8 + 108), AC 17, Joined Hands 9 (1d10 + 4), *Put Aside*
DC 14, 9 (2d8), CR 8 (3,900 XP). Rules as printed: one trick a round, Help doesn't apply,
leaning in +2/+2 to +4, DC 13 Idle / DC 19 Focused, four broken focuses to win.

**Main table** (5,000 fights a row; card fires with it Idle; six rounds; "Down, Not Out"
applied, so nobody dies). As printed in the book's S14 DM Note before R3.1:

| The party… | Pregens: out of the way | Pregens: whole party down at once | Optimized: out of the way | Optimized: whole party down |
|---|---|---|---|---|
| Only trades blows | 16% | 24% | 80% | 15% |
| Plays the distraction game, bare rolls | 43% | 10% | 58% | 12% |
| Plays it and leans in | 72% | 5% | 81% | 5% |

- With the pregens, at least one character hits 0 HP in four fights out of five even when the
  table leans in (pass-2 log: 78% lean-in, 89% bare, 97% blows-only).
- Help for Advantage would lift leaning in from 72% to 88%; that is why Help doesn't apply.

**Adjusting lines** (2,000 a row; pregens unless noted; blows-only win / blows-only all-down,
bare distraction win, lean-in win):

| Line | Change | Blows win / all-down | Bare | Lean in |
|---|---|---|---|---|
| Three characters (Dassa, Pello, Ilesse) | 180 HP; Focused second turn is one Joined Hands | 18% / 20% | 26% | 72% |
| Five characters (Serane added) | 260 HP; DC 20 Focused | 10% / 10% | 45% | 72% |
| Four at 3rd level (approximated) | 210 HP; DC 18 Focused; second turn one Joined Hands | 17% / 16% | 47% | 72% |
| Four at 5th level | use the five-character line | not simulated | — | — |
| A table built to hit hard (the optimized party) | 300 HP | 29% / 33% | 31% | 66% |

The book now says only: a slugging match usually goes the Attendant's way for the pregens;
the distraction game turns it, and a table that leans in usually wins; expect a character to
drop even then; a party built for damage can out-slug it, hence its Adjusting line; the
Adjusting lines keep the odds about level.

## Solo lines (three-player pass, T3.10)

Harness: `research/oraga_5e_sim/skirm.py`, cards `<card>_solo`. Seed 1, n = 2,000 per cell.
Each cell is the current rule (a lone PC walks into the printed three-character roster), then
the solo line, as a drop % (the PC goes to 0 HP at least once). Following the T3.1 review rule,
these are deltas inside the rebuilt harness, not absolute claims. Two PCs use the
three-character line.

| Card | Solo line | Dassa | Pello | Andra | Ilesse | Serane |
|---|---|---|---|---|---|---|
| S2 | Tavva, one knife a round behind; she goes when either is Bloodied | 78.8 → 48.4 | 97.8 → 64.5 | 72.2 → 15.0 | 100.0 → 99.8 | 100.0 → 99.7 |
| S4 | One honor guard | 98.9 → 37.2 | 99.7 → 58.1 | 100.0 → 58.8 | 100.0 → 100.0 | 100.0 → 100.0 |
| S7 | As printed (three knives) | 16.6 → 17.4 | 23.0 → 23.8 | 15.7 → 16.7 | 99.9 → 99.9 | 99.8 → 99.7 |
| S8 | One warden, the second up the stair in round 3; they break when one is down | 99.2 → 35.8 | 99.6 → 24.8 | 100.0 → 26.1 | 100.0 → 99.8 | 100.0 → 100.0 |
| S9 | As printed (two a side; the duelists break when hurt) | 15.3 → 15.4 | 31.0 → 30.2 | 23.9 → 23.3 | 94.2 → 93.0 | 91.8 → 93.0 |
| S10 | Maiven alone, from round 3, pulling her blows (two attacks) | 88.5 → 19.7 | 94.8 → 37.8 | 100.0 → 68.2 | 100.0 → 100.0 | 100.0 → 100.0 |
| S13 | Draunel alone; he breaks when Bloodied | 73.4 → 35.4 | 70.2 → 47.2 | 42.2 → 27.4 | 100.0 → 99.9 | 100.0 → 100.0 |

- **Band (resolved escalation, option (a)):** Dassa, Pello and Andra fall between 15% and 70%
  on every line. The edges are S2 Andra (15.0; 15.8 and 18.0 at seeds 2 and 3, n = 4,000), S9
  Dassa (15.4; 14.8 and 15.4) and S10 Andra (68.2; 67.4 and 68.0).
- **Ilesse and Serane** lose nearly every solo fight in this harness. It gives them only
  cantrip offence and no outs, so they are on record but outside the band. The cards send a
  lone talker or healer to the outs first.
- **S7 and S9 need no solo roster.** S7's knives break at the first Bloodied knife and S9's
  duelists at first damage, so a lone fighter already sits in the band against the printed
  line.
- **Not modelled:** the cards' clocks and outs, Tavva's charges, and Help.

## S14 under WP5: the lethal Attendant (three-player pass, T5.8–T5.9)

Harness: `research/oraga_5e_sim/s14.py`. Every WP5 rule is a switch on `Rules`; `OLD` (all off)
reproduces the T3.1 table draw for draw (checked: `--all --n 4000 --seed 1` is byte-identical),
`NEW` (all on) is the WP5 text. Per the T3.1 review rule these are **current → WP5 deltas inside
the rebuilt harness**, not absolute claims. The WP5 run also fixes a T3.1 bug: *Put Aside*'s
recharge was never rolled (`put_aside_recharge`). Block: 178 HP (three), 229 (four); the Wept's
clock as printed (6 moves at three, 5 at four, 1 Delay when the card fires).

**Main table** (seed 1, n = 4,000 a cell; `python s14.py --wp5 --n 4000 --seed 1`). Win % /
PC death % / any drop % / whole party down %. "Current" is the old rule (nobody can die).

| Party | Policy | Current | WP5 Gentle | WP5 Sharp | WP5 Merciless |
|---|---|---|---|---|---|
| C1 | engaged | 87.3 / 0 / 24.1 / 0.0 | 97.1 / 0.0 / 38.4 / 0.0 | 97.6 / 0.3 / 38.1 / 0.0 | 96.8 / 3.6 / 36.5 / 0.0 |
| C2 | engaged | 90.9 / 0 / 24.9 / 0.0 | 97.5 / 0.0 / 45.1 / 0.1 | 97.2 / 3.8 / 44.9 / 0.1 | 96.4 / 13.7 / 45.2 / 0.2 |
| C3 | engaged | 92.7 / 0 / 28.2 / 0.0 | 93.8 / 0.0 / 49.0 / 0.2 | 93.6 / 5.7 / 50.2 / 0.8 | 92.5 / 12.7 / 49.6 / 0.7 |
| C4 | engaged | 94.1 / 0 / 20.3 / 0.0 | 97.5 / 0.0 / 38.6 / 0.1 | 96.2 / 5.5 / 40.0 / 0.7 | 96.5 / 15.3 / 39.3 / 0.4 |
| C5 | engaged | 93.6 / 0 / 25.1 / 0.1 | 96.6 / 0.0 / 48.5 / 0.2 | 95.7 / 3.4 / 49.8 / 0.5 | 95.6 / 11.8 / 49.5 / 0.4 |
| 4P | engaged | 85.1 / 0 / 29.1 / 0.0 | 92.9 / 0.0 / 51.3 / 0.0 | 92.2 / 0.5 / 52.0 / 0.0 | 92.4 / 10.0 / 50.2 / 0.0 |
| C1 | slug | 0.8 / 0 / 75.5 / 0.0 | 0.6 / 0.0 / 87.3 / 0.5 | 0.9 / 2.3 / 86.8 / 0.2 | 0.4 / 20.8 / 88.2 / 0.5 |
| C2 | slug | 15.3 / 0 / 80.5 / 0.1 | 13.1 / 0.0 / 91.7 / 1.4 | 8.6 / 5.9 / 92.2 / 0.2 | 9.1 / 36.0 / 91.5 / 1.0 |
| C3 | slug | 36.5 / 0 / 82.0 / 0.1 | 30.5 / 0.0 / 92.0 / 4.8 | 25.7 / 21.5 / 92.5 / 10.4 | 24.2 / 36.5 / 92.5 / 8.8 |
| C4 | slug | 36.4 / 0 / 74.2 / 0.2 | 27.4 / 0.0 / 90.2 / 8.0 | 17.2 / 19.8 / 89.9 / 7.1 | 17.0 / 47.4 / 90.5 / 6.4 |
| C5 | slug | 7.0 / 0 / 86.2 / 0.6 | 5.5 / 0.0 / 98.1 / 9.5 | 3.7 / 6.6 / 97.9 / 0.7 | 4.0 / 44.2 / 98.0 / 3.2 |
| 4P | slug | 0.3 / 0 / 83.0 / 0.0 | 0.2 / 0.0 / 94.0 / 0.0 | 0.1 / 2.8 / 94.2 / 0.0 | 0.1 / 32.4 / 93.9 / 0.0 |

Naive (bare rolls), current → Sharp: C1 57.6 → 69.6 (death 1.6), C2 67.7 → 77.9 (5.3), C3 58.0
→ 66.0 (12.3), C4 70.3 → 74.1 (11.9), C5 60.9 → 69.5 (8.7), 4P 60.1 → 71.5 (1.2). Smart, current
→ Sharp: 91–96 → 94–98, deaths 0.1–5.3 (4P 0.6). Mean rounds 4.7–5.3 engaged, 7.1–7.4 slugging.
Full output, every dial and policy: run the command above.

**Targets at Sharp (DESIGN §4): met in the first round, no tuning.** Engaged win 92–98% (≥ 85);
PC death for an engaged party 0.3–5.7% (≤ 10); slugging wins 0.1–26% with deaths 2–22%.

**Where the change comes from** (C1 engaged at Sharp; one switch on from OLD / one off from NEW;
n = 4,000, seed 1, win % / any drop %): Help +8.0 win (87.3 → 95.3; NEW without it 92.7); DC 18
+3.7 (→ 91.0; NEW without it 94.8); *Literal Orders* since the start of its previous round
nearly doubles drops (24.1 → 42.9; NEW without it 14.8) and is what makes the fight dangerous;
*Put Aside* recharging +2 drop points; the cap, *Clears the Way* as an action, the tie rule,
spells-roll Delay and TP30's tricks each move win by 1 point or less here.

**L-042 (the extra Wept turn at three) holds.** NEW at Sharp, n = 2,000, clock 6 (printed) → 5:
engaged C1 97.1 → 86.8, C2 97.2 → 87.2, C3 93.2 → 80.3, C4 96.7 → 87.2, C5 95.0 → 85.8; naive
falls 13–20 points. Without the extra turn the engaged trios drop to the target line.

**L-041 (the timeout claim).** On the printed clock the errand beats an engaged party 2–6% of the
time (current: 6–13% for the trios at n = 4,000, all of their losses). It is true only when the
card fires late (`--clock tight`, n = 2,000): engaged wins 3–10% (current 3–9%), smart 25–29%
(current 34–40%: Delay is capped at three turns and the Attendant clears it with its action).

**L-003 (Idle-grind XP).** No cell, at any dial or policy, wins by Hit Points while the Attendant
was Idle for half its turns or more (0.0% everywhere). No halving.

**Adjusting lines** (NEW, Sharp, n = 2,000, seed 1; engaged win / death, slug win / death):

| Line | Setting tried | Engaged | Slug | Printed |
|---|---|---|---|---|
| Four characters | 229, full Multiattack, DC 18 | 92.2 / 0.5 | 0.1 / 2.8 | 229 (unchanged) |
| Five characters (all five pregens) | 229 / 260 / 280 at DC 18 and 19 | 93–95 / 0.6–0.8 | 23–25 → 5–6 → 1–2 | **260, DC 19** |
| Four at 3rd level (80% HP, one fewer 2nd-level slot) | 178 / 195 / 210 / 229 at DC 17 and 18 | 92–94 / 0.9–1.8 | 4 → 0.1 | **210, DC 17** |
| Hit hard, three (proxy C3 / C4 slugging) | 178 / 200 / 215 / 230 | 93–96 / 5–6 | C3 23.8 → 11.6 → 4.5 → 2.1; C4 16.7 → 6.9 → 2.6 → 0.6 | **+30 (208)** |
| Hit hard, four (Dassa/Pello/Andra/Ilesse) | 229 / 259 / 280 / 300 | 90–91 / 3–4 | 7.3 → 1.5 → 0.2 → 0.0 | **+30 (259)** |

The engaged route barely moves with Hit Points or a point of DC; the lines set the slugging odds.
The harness has no optimized party, so "built to hit hard" uses the strongest pregen sluggers as a
proxy (TPN-8f): +30 brings them to the other trios' slugging level.

**Solo** (NEW, Sharp, engaged, n = 2,000; without the solo line → with it; win / death / drop):
Dassa 38.7 / 18.2 / 44.0 → 47.8 / 6.2 / 14.2; Pello 12.2 / 34.4 → 15.3 / 33.2; Andra 33.6 / 25.9 →
42.6 / 19.2; Ilesse 12.8 / 33.2 → 19.0 / 33.8; Serane 39.7 / 22.1 → 53.2 / 17.0. Alone, nobody is
safe at Sharp (a dying lone character has no one to reach them), so the line also sends a lone
character to the outs first.

**Not modelled:** the Wept's strikes (the engaged party keeps out of her reach), so the
Uninvited's own threat rule never bites in S14; control spells; Idle tricks (no policy tries
one; the switches are unit-tested). After the card, standing allies stabilise the dying; with
the whole party down, the dying roll it out unaided (Gentle: the crowd reaches everyone).

## WP6: three-player budgets, lethal after midnight, resources (T6.9–T6.13)

*Harness: `research/oraga_5e_sim/` with the T6.9 switches (`skirm.WP6`, `chain.ChainWP6`).
Seed 1, n = 2,000 a cell. "Drop" = at least one character at 0 HP; "death" = at least one
character dead. Parties C1 Dassa/Ilesse/Serane, C2 Dassa/Ilesse/Andra, C3 Dassa/Pello/Ilesse,
C4 Dassa/Pello/Andra, C5 Serane/Andra/Pello, 4P = C1 + Andra. TP57 (2026-10-25) left one
difficulty level (the old Sharp rules), so there is one column per card, not three.*

**Rosters are capped by printed headcounts.** The Circle brought four knives, the Church four
wardens, Draunel three duelists, Boranis three cousins, Tavva a crew of four, Phern "two or
three" bodyguards. No roster below adds a person the book doesn't already put at the ball.
That cap means several cards cannot reach DESIGN §2.2's target (before midnight Low 750 or
Moderate 1,125; after midnight Moderate 1,125 or High 1,500): S1, S2, S6 before midnight, and
S5, S8's dark half, S11, S12 after. They keep their sums and say so.

### Before midnight (T6.10): drop % / mean drops

| Card | XP (label) | C1 | C2 | C3 | C4 | C5 | 4P |
|---|---|---|---|---|---|---|---|
| S2 printed (Tavva + 2) | 550 (under Low) | 44.4/0.71 | 23.7/0.26 | 24.3/0.28 | 10.1/0.10 | 25.6/0.28 | 17.1/0.19 |
| S4 fought out (2 guards; TP29 keeps the roster) | 900 (between Low and Moderate) | 68.9/1.67 | 46.3/0.62 | 42.5/0.56 | 28.0/0.32 | 53.1/0.72 | 28.7/0.39 |
| S4 ended by *Call the House* | 900 | 28.1/0.42 | 14.9/0.16 | 17.8/0.20 | 10.2/0.10 | 17.8/0.20 | 9.3/0.11 |
| S7 printed (3 knives) | 600 (under Low) | 3.8/0.05 | 0.5/0.01 | 0.5/0.01 | 0.0/0.00 | 0.2/0.00 | 0.4/0.00 |
| **S7 WP6 (all 4 knives)** | **800 (Low)** | 7.3/0.10 | 1.2/0.01 | 1.1/0.01 | 0.2/0.00 | 0.7/0.01 | 0.2/0.00 |
| S7 WP6, to the last knife | 800 | 84.5/3.07 | 58.8/1.07 | 50.0/0.76 | 45.0/0.58 | 76.5/1.53 | 39.7/0.60 |
| S8 printed (2 wardens + 1) | 600 (under Low) | 65.0/1.71 | 26.8/0.34 | 22.2/0.27 | 11.2/0.13 | 27.1/0.33 | 29.5/0.43 |
| S9 printed (2 + 2) | 600 (under Low) | 1.2/0.01 | 0.3/0.00 | 0.2/0.00 | 0.1/0.00 | 0.3/0.00 | 1.8/0.02 |
| **S9 WP6 (3 duelists + 3 blades)** | **900 (between Low and Moderate)** | 6.7/0.07 | 3.1/0.03 | 3.8/0.04 | 0.9/0.01 | 3.6/0.04 | 1.5/0.02 |
| S9 WP6, both sides to the last | 900 | 91.6/4.62 | 72.5/1.70 | 64.0/1.29 | 61.3/1.20 | 88.3/2.56 | 94.2/3.80 |
| S10 printed (Maiven + 2) | 900 (between Low and Moderate) | 51.9/0.86 | 24.9/0.29 | 19.3/0.21 | 6.7/0.07 | 20.6/0.23 | 24.3/0.30 |

Reading (the book's own scale: Low drops a character now and then, Moderate fairly often, High
usually): S2 plays Low (Moderate for C1, the party light on damage). S4 fought out plays
Moderate; ended by its clock it plays Low. S7 and S9 end in a round or two on their printed
morale whatever the roster, and fought to the last they play High; the four-knife and
three-and-three rosters raise the sums to Low and between Low and Moderate. S8 plays Low
(Moderate for C1); nobody dies (the wardens detain). S10 plays Low (Moderate for C1).
**S1 and S6 are not modelled:** both are fist fights (no steel on either side), which the
harness's weapon offence can't represent; their sums stay 175 and 400. All before-midnight
drops are Stable at once (the palace's mercies), so no death column.

### After midnight (T6.13): drop % / death %

| Card | XP (label) | C1 | C2 | C3 | C4 | C5 | 4P |
|---|---|---|---|---|---|---|---|
| S3 printed (sergeant + 4; captain round 3) | 850 / 1,950 | 39.1/2.2 | 23.1/0.8 | 13.1/0.6 | 12.6/0.6 | 46.9/1.8 | 43.8/0.8 |
| S3 to the last | 1,950 | 100/48.5 | 99.9/45.0 | 97.6/25.4 | 97.4/32.9 | 100/43.4 | 100/47.9 |
| S5 printed (Tavva + 2) | 550 | 45.9/7.0 | 24.0/2.6 | 24.7/2.2 | 10.0/0.7 | 24.5/2.1 | 14.9/1.1 |
| S5, morale at half down | 550 | 20.9/0.5 | 7.0/0.2 | 5.5/0.4 | 1.9/0.1 | 5.7/0.1 | 5.2/0.1 |
| S8 dark (3 wardens, half down) | 600 | 66.1/0.0 | 27.8/0.0 | 23.4/0.0 | 11.3/0.0 | 26.8/0.0 | 30.9/0.0 |
| S12 printed (2 knives, first Bloodied) | 400 | 1.2/0.0 | 0.1/0.0 | 0.1/0.0 | 0.0/0.0 | 0.0/0.0 | 0.1/0.0 |
| **S12, half down** | 400 | 6.1/0.1 | 1.8/0.0 | 0.7/0.1 | 0.3/0.0 | 0.9/0.0 | 0.5/0.0 |
| **S12 heat 4 (3 knives), half down, finish** | 600 | 39.6/11.7 | 17.8/10.2 | 14.1/6.0 | 6.3/4.2 | 19.4/9.7 | 7.8/1.2 |
| S13 printed (Draunel + 1, Draunel Bloodied) | 900 | 35.1/0.4 | 11.1/0.2 | 12.8/0.5 | 4.7/0.1 | 9.0/0.1 | 14.6/0.1 |
| **S13 WP6 (Draunel + 2, half down)** | **1,100 (between Low and Moderate)** | 66.4/2.2 | 43.0/1.6 | 39.9/2.0 | 22.9/1.2 | 40.8/2.0 | 74.7/1.9 |
| S13 WP6 at heat 4 (finish) | 1,100 | 65.2/27.0 | 41.2/19.6 | 40.0/16.2 | 22.1/14.0 | 40.9/20.6 | 73.1/27.3 |
| S13 WP6 at heat 4, potions | 1,100 | 63.4/20.8 | 40.5/11.8 | 39.8/9.0 | 19.6/5.1 | 36.4/11.3 | 70.7/17.9 |
| S7 in the dark (nursery sold; 3 knives, heat 4, finish) | 600 | 38.8/12.8 | 17.6/11.8 | 14.0/6.7 | 6.2/3.9 | 17.2/8.9 | 21.0/6.7 |

S11 is not modelled (the crush clock is the fight; its Phern bodyguards don't press an
attack). **The heat-4 finish is the deadliest rule in the night.** Without it, every
after-midnight card kills a character 0–2% of the time (S5 printed 1–7%). With it, a heat-4
card kills 4–27%: the foes that finish attack a downed character with Advantage, every hit
is two failed death saves, and the party has to get to the fallen in the same round.

### The chain (T6.13): S14 → S13 → S3, HP at the gate / any PC death / S14 win

| Party | Old rules (T3.1) | S14 at WP5 only | + resources (potions, Hit Die, chapel) | + WP6 cards (S13 Draunel + 2, half down) | + heat-4 finish in S13 (all of WP6) | all of WP6, after S2 in Movement V |
|---|---|---|---|---|---|---|
| C1 | 80.6 / 18.2 / 87.5 | 78.7 / 18.9 | 82.6 / 15.0 | 69.2 / 26.7 | 60.6 / 46.6 / 97.4 | 39.6 / 69.0 / 97.0 |
| C2 | 76.4 / 19.5 / 91.4 | 73.4 / 20.7 | 78.6 / 16.7 | 64.9 / 27.0 | 58.2 / 45.2 / 96.9 | 45.4 / 58.8 / 96.8 |
| C3 | 78.9 / 4.7 / 92.6 | 70.7 / 10.9 | 78.0 / 7.3 | 64.8 / 13.9 | 62.0 / 26.4 / 94.2 | 53.3 / 36.9 / 92.0 |
| C4 | 58.2 / 12.4 / 94.2 | 48.8 / 19.1 | 58.5 / 12.3 | 44.7 / 24.4 | 45.0 / 36.4 / 96.5 | 39.0 / 46.0 / 95.7 |
| C5 | 66.8 / 17.2 / 93.5 | 59.9 / 21.2 | 70.4 / 13.7 | 52.4 / 26.1 | 50.0 / 42.0 / 95.5 | 38.3 / 57.6 / 95.9 |
| 4P | 82.2 / 16.7 / 84.5 | 80.7 / 18.0 | 85.9 / 10.0 | 55.9 / 43.8 | 48.8 / 63.4 / 92.5 | 36.2 / 74.7 / 92.6 |

TUNING's "5–21% of HP at the gate" was never reproduced by the rebuilt harness (it gave 57–82%
for the old rules, T3.1). The WP6 resources buy back about 5–10 points of HP at the gate and a
few points of death. The heavier S13 and its heat-4 finish take far more: with everything on,
the party reaches the gate with 45–62% of its HP, and **a character dies somewhere in the
chain 26–63% of the time** (37–75% after a Movement V fight). The chain is a worst case: it
runs S13 at heat 4 every time, the party always fights it rather than taking an out, the gate
is fought, and nobody runs. Even so, that is well past the TP57 aim ("approximately in line
with other D&D modules"). The death toll comes from two rules the text already carries: the
strict crowd rule (no help for the dying in a snake fight) and the heat-4 finish. Both were
kept as the old Sharp wording by TP57; whether to soften either is an owner call (LOG, WP6
OWNER questions).

### TP61: the heat-4 finish cut (T7.23, 2026-10-25)

*Owner ruling TP61: no snake deliberately finishes a downed character, at any heat. The finish
stays in the harness behind `skirm.WP6.heat4_finish` / `chain.ChainWP6.finish` so the rows above
reproduce; the current rules are `heat4_finish` off, and `chain.ChainWP6.tp61()` (every WP6
switch except `finish`). Seed 1, n = 2,000. Script: `skirm.simulate` / `chain.simulate` looped
over the parties (the scratchpad `t723.py`).*

Heat-4 cards, drop % / death %, finish off:

| Card | XP | C1 | C2 | C3 | C4 | C5 | 4P |
|---|---|---|---|---|---|---|---|
| S13 WP6 at heat 4, potions | 1,100 | 64.5/1.6 | 40.2/0.2 | 38.0/0.8 | 20.0/0.3 | 34.6/0.8 | 68.3/0.9 |
| S12 heat 4 (3 knives), half down | 600 | 40.5/0.5 | 18.9/0.1 | 14.1/0.5 | 6.2/0.2 | 16.1/0.4 | 8.3/0.1 |
| S7 in the dark (nursery sold; 3 knives, heat 4) | 600 | 38.6/0.9 | 18.4/0.1 | 14.3/0.1 | 5.5/0.2 | 17.3/0.2 | 21.1/0.4 |

S13 at heat 4 is back to 0–2% deaths (TP61's target "about 1–2%"); S12 and S7 in the dark to
0–1%. Every after-midnight snake card now kills a character 0–2% of the time (S5 printed 1–7%).

The chain under the current rules (`ChainWP6.tp61()`), HP at the gate / any PC death / S14 win:

| Party | Current rules | after S2 in Movement V |
|---|---|---|
| C1 | 69.2 / 26.7 / 97.2 | 47.3 / 45.9 / 97.1 |
| C2 | 64.9 / 27.0 / 97.4 | 51.3 / 40.0 / 97.0 |
| C3 | 64.8 / 13.9 / 92.1 | 56.7 / 18.8 / 92.7 |
| C4 | 44.7 / 24.4 / 95.9 | 40.7 / 27.9 / 95.9 |
| C5 | 52.4 / 26.1 / 95.0 | 40.0 / 40.4 / 94.9 |
| 4P | 55.9 / 43.8 / 93.0 | 41.8 / 57.9 / 92.7 |

The HP and death columns match the "+ WP6 cards" column above (the same switches). With the
finish gone, **a character dies somewhere in the chain 14–44% of the time** (19–58% after a
Movement V fight), down from 26–63%. What is left comes from S14 (a Focused Attendant can
kill, TP5) and S3 at the gate, with the strict crowd rule leaving the dying unhelped; the
chain's worst-case caveats above still apply (S13 fought every time, no outs, the gate fought).
Recorded for the owner; no rule changes follow from it here.

**Not modelled:** control spells; outs and clocks (fights run to morale); S1, S6, S11; S14's
own use of potions (they are used between scenes and in the snake fights only); the chapel's
cost (one heat per shown line) is a table effect, not a chain effect.
