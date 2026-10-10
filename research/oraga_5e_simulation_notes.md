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
