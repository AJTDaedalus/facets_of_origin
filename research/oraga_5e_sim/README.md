# Oraga Night 5e: simulation harness (three-player pass)

These are Monte Carlo scripts for the 5e conversion of *Oraga Night*
(`conversions/dnd5e/oraga_night/`). The TUNING_3P audit
(`docs/audit_oraga_5e_3p/TUNING_3P.md`) used three scripts that lived only in a
session scratchpad, and that scratchpad is gone. TASKS T3.1 rebuilt them here from
the audit's §2 "Method", its expected-damage arithmetic, the §3 per-card table, §5
and the Appendix. The stat numbers come from the module's own blocks (chapter X)
and cards (chapter IX), and the party from the chapter XI pregens. The rules base
is D&D 5e SRD 5.2.1. Nothing under `references/oraga_night/` was used.

The scripts use pure Python 3 standard library: no numpy and no dependencies.
Every script is importable (the logic lives in functions) and deterministic for a
given `--seed`.

| File | What it models |
|---|---|
| `skirm.py` | Generic snake-card skirmish: a card's roster against the party, run until the card's morale trigger fires or one side is down. It also holds what the other two share: dice, the five pregens, the party codes, PC offence and healing, dropping, death saves and the crowd rule. |
| `s14.py` | Card S14, the Attendant, **with the distraction rules as printed now** (before WP5). |
| `chain.py` | The night's attrition chain, with HP and resources carried forward and no rest: an optional Movement V card, then S14, then S13, then the S3 gate fight. |
| `test_smoke.py` | Written first (TDD). Each script runs at N=200 with a fixed seed and returns a sane structure, and each carries one regression assertion. It also checks determinism and the CLI. |

## How to run

```bash
python -m pytest research/oraga_5e_sim -q              # smoke tests, about 5 s

python research/oraga_5e_sim/s14.py --party C1 --policy engaged --n 4000 --seed 1
python research/oraga_5e_sim/s14.py --all --n 4000 --seed 1            # Appendix table
python research/oraga_5e_sim/s14.py --all --n 4000 --seed 1 --clock tight
python research/oraga_5e_sim/s14.py --party C1 --n 4000 --seed 1 --attrited

python research/oraga_5e_sim/skirm.py --card S8 --party C1 --n 4000 --seed 1
python research/oraga_5e_sim/skirm.py --card S2 --solo Dassa --n 2000 --seed 1
python research/oraga_5e_sim/skirm.py --all --n 2000 --seed 1          # slow (~3 min)

python research/oraga_5e_sim/chain.py --party C1 --n 4000 --seed 1
python research/oraga_5e_sim/chain.py --all --n 2000 --seed 1 --crowd generous
```

From Python, call `s14.simulate(party, policy, n, seed, clock, attrited)`,
`skirm.simulate(card, party, n, seed, solo, crowd)` or
`chain.simulate(party, n, seed, crowd, mv5_card, ...)`. Each returns a dict of
rates. The SIM rule in TASKS asks for 2,000 runs or more per cell, with the seed
logged; every CLI run prints its `seed=` and `n=`.

**Party codes** (TUNING §2): C1 Dassa/Ilesse/Serane · C2 Dassa/Ilesse/Andra ·
C3 Dassa/Pello/Ilesse · C4 Dassa/Pello/Andra (no healer) · C5 Serane/Andra/Pello
(no front line) · 4P Dassa/Ilesse/Serane/Andra.

## What each script assumes

### Common (`skirm.py`)

- **Pregens** are as printed in chapter XI: HP, AC, initiative (Dassa's with
  Advantage), saves and attacks.
  - Dassa: two-handed longsword 1d10+4, Savage Attacker, crits on 19–20, Sap,
    Action Surge, Second Wind.
  - Pello: dagger and Nick dagger, Steady Aim for Advantage, Sneak Attack 2d6.
  - Andra: Magic Missile from her 2nd-level slots, Fire Bolt with Potent Cantrip,
    Shield from her 1st-level slots.
  - Ilesse: Sacred Flame, Healing Word, Cure Wounds and Preserve Life, with
    Disciple of Life. Spare the Dying on a dying ally when she has no slot.
  - Serane: Vicious Mockery (Disadvantage on the target's next attack), Healing
    Word, and Cutting Words when a hit is within 2 of missing.
- **Heroic Inspiration**: one each, spent on a failed death save in the skirmish
  and on a failed trick in S14.
- **Policy switches** (`skirm.OPTIONS`):
  - `ilesse_attack_slots=False`. Ilesse keeps every slot for healing: no
    Spiritual Weapon, no Guiding Bolt. TUNING §5 describes the healer spending
    "almost everything on healing (so no Spiritual Weapon)", and its C1 reads as a
    low-damage party. S14's *slug* policy turns this on, because slugging means
    everyone hits it.
  - `targeting="sticky"`. Each foe picks a random standing PC and keeps on it
    until that PC drops. The alternatives are `random` (a new target for every
    attack), `front` (the front line draws twice the attention) and `soft`
    (TUNING's "focus-fires the softest PC" variant).
- **Dropping.**
  - Before midnight, and for anything that detains, a dropped PC is Stable at
    once. Healing can still raise them.
  - After midnight (S3, S13): death saves, with no snake attacking a downed PC.
  - **Crowd rule.** `strict` (as written): only a Stable PC is dragged clear,
    then is up with 1 HP at the start of the round after next. `generous` (the
    F3 reading): a dying PC is dragged clear and is Stable at the end of the round
    it dropped.
  - Bought Blades use their cudgels: *To the Terms* leaves a PC at 1 HP.
- **What is not modelled.**
  - Control spells: Sleep, Hideous Laughter, Command, Hold Person. TUNING §2
    lists none of them. They would make every snake fight easier.
  - Grapples and Seize, Furniture, pushes and prone in snake fights.
  - The noise clocks, and the outs: fights run to morale, as in TUNING's caveat.
  - Positioning is abstract. Melee PCs are "adjacent" once they attack.

### Cards (`skirm.CARDS`)

Each card uses the printed "Three characters" line for parties of three or fewer
and the four-player roster for 4P.

| Card | Roster (3P) | Ends when |
|---|---|---|
| S2 | Tavva + 2 Gallery Knives | Tavva Bloodied: next turn she strikes, fires a charge, and the crew is gone |
| S3 | Bought Sergeant + 4 Blades; captain from round 3 | sergeant down or half the Blades down. PCs come through the wicket one per round, front line first. `S3_fix`: captain in round 4. `S3_last`: no morale |
| S4 | 2 Honor Guards | both down ("fought before the reinforcements"). `S4_clock`: ends when *Call the House* brings the four |
| S7 | 3 Circle Knives | first knife Bloodied. `S7_nasty`: half down |
| S8 | 3 Church Wardens, all from round 1 | two down; *Interpose* gives Disadvantage. `S8_fix`: one down. `S8_staggered`: the third arrives in round 3 |
| S9 | 2 Draunel Duelists + 2 Cousin's Blades | duelists leave on first damage, cousins at half down. `S9_last`: no morale |
| S10 | Maiven (arrives round 3) + 2 slingers | Maiven down. `S10_fix`: Maiven + 1 slinger, two attacks |
| S13 | Essar Draunel + 1 Draunel Duelist | Draunel Bloodied, with smoke (50% a turn: DC 10 Con or lose the action) and fire (10% a turn: DC 13 Dex, 2d6; never finishes anyone). `S13_last`: no morale |

Two numbers are approximations. The Veteran Draunel Duelist (4P S9 and S13 only)
is set at 58 HP, AC 16 and two +6 1d8+4 attacks. S8's later wardens arrive on a
lock clock that advances only while they work the lock undisturbed. In a fight
that is a DM call, so the default puts them all in from round 1, as TUNING's
"3 wardens" does.

### `s14.py`

- Modelled **as printed now**:
  - Idle and Focused (focus checked at the start of each of its turns,
    including a turn it then loses), and Two Turns at initiative − 10.
  - The 3P line (180 HP; the second Focused turn is one Joined Hands) and the 4P
    block (229 HP).
  - Rusty, Put Aside's recharge, and Literal Orders. In round 1 the whole party
    counts as interferers, because the card fires on their interference.
  - Clears the Way: once a round, after the focus check, if no non-furniture PC
    is adjacent.
  - The full distraction rule: DC 13/19, +2/+2 capped at +4, repeats at
    Disadvantage, one trick a round, success by 5 or a natural 20 costs its next
    turn, furniture on an Idle success, four broken focuses wins.
  - Down, Not Out with the crowd rule, Heroic Inspiration (hint 4 grants it to
    the first PC who tries, after that roll), Bardic Inspiration on a failed
    trick, Tactical Mind, Cutting Words, Shield, Sap, Vicious Mockery, Healing
    Word.
- **The Wept's clock.** The card fires with 1 Delay on the Wept and 6 moves left
  (5 at 4P). `--clock tight` sets 3 moves (2 at 4P). The Wept's strikes are not
  modelled: the engaged party stays out of her reach.
- **Tricks.** Each pregen has one trick per habit it can credibly stage, plus
  arguing its orders (listed in `skirm.PREGENS[...]["tricks"]`). Andra and Ilesse
  get Advantage on crystal tricks from the Orthaen gift, and Dassa gets it on a
  thrown light with Athletics (TUNING's "generous but rules-legal DM").
- **Policies.**
  - *engaged*: the best fresh trick each round with +2 played out and +2 habit,
    taken by whichever PC still to act this round has the best chance. Everyone
    else attacks.
  - *naive*: bare rolls (+2 one time in four). Each player uses their character's
    best skill even on a repeat, without Bardic Inspiration or Tactical Mind.
  - *smart*: engaged, plus one melee PC stays adjacent, and Delay is bought (DC
    13) only when the Wept has none and acts before the Attendant's next turn. A
    Delay bought then is spent before the Attendant ever sees it.
  - *slug*: everyone hits it, the cleric's slots included.
- **Losses.** The Wept's moves run out (the Attendant leaves with her), or the
  whole party is down at once.

### `chain.py`

- **Order:** optional Movement V card, then S14 (engaged), then S13, then S3.
  HP, slots, Heroic and Bardic Inspiration, Second Wind and Channel Divinity carry
  forward.
- **Between scenes:** everyone down stands with 1 HP. Each healer spends one
  1st-level slot on the most-hurt ally if anyone is below 75%, and Dassa takes a
  Second Wind if she is below half. `--no-between-heal` turns that off.
- **Outputs:** "HP at the gate" is the party's HP on reaching S3 as a share of
  maximum (a dead PC counts 0). `pc_death` is any death across the whole chain.

## Which TUNING numbers it reproduces

All runs below are at the current (old) rules with `--seed 1`. S14 is at 4,000
runs a cell, the skirmish cards at 4,000, and the chain and solo tables at 2,000.

### S14 engaged distraction, the T3.1 acceptance check

| Party | TUNING win / drop | This harness, 4,000 runs |
|---|---|---|
| C1 D/I/S | 90.7 / 25.3 | **87.3** / 24.1 |
| C2 D/I/A | 93.4 / 29.7 | **90.9** / 24.9 |
| C3 D/P/I | 93.7 / 29.9 | **92.7** / 28.2 |
| C4 D/P/A | 95.9 / 23.7 | **94.1** / 20.2 |
| C5 S/A/P | 95.2 / 26.0 | **93.6** / 25.1 |
| 4P | 90.1 / 30.7 | 85.1 / 29.1 |

The three-player engaged wins span 87.3–94.1%. TUNING's band is 90–96%, so they
sit inside the band with its ±3 tolerance (87–99). The order matches: C1 is the
lowest trio and the no-healer trios the highest. C2–C5 are each within 2.5 points
of their TUNING value. **C1 is 3.4 points under its own TUNING value (90.7)**, and
4P is 5.0 under.

Other S14 figures:

- **Naive:** 57.6–69.6% at three PCs. TUNING gives 57–75%.
- **Slug:** C1 0.7, C2 13.9, C3 34.1, C4 34.0, C5 6.0. TUNING gives 0.2, 16.4,
  17.6, 34.0, 9.0. All but C3 are within 5.
- **Smart:** wins 91–96%, against TUNING's 90–95%. It banks less Delay than
  TUNING (about 1.0 at three PCs and 1.3 at four, against TUNING's 1.6–1.9 and
  3.1).
- **Attrited C1:** 80.5% win, 55.1% at least one drop. TUNING gives 79–86% and
  55–64%.
- **Tight clock:** distraction-only wins 3–8%, against TUNING's "at most 6%".
  Smart wins 34–40% at three PCs, against TUNING's 22–39%, and **42.7% at four,
  against TUNING's 8–11%** (a gap).

### Skirmish cards (any PC drops; 4,000 runs)

Three per-card figures reproduce within ±5 points. These are the T3.1 acceptance
figures:

| Figure | TUNING | Harness |
|---|---|---|
| **S7** as written, every party | ≤ 4% | 0.0–3.9% |
| **S8** as written, C3 | 23% | 22.7% |
| **S3** fight-through, C3 | 16% | 13.5% |

These are inside TUNING's range:

| Figure | TUNING | Harness |
|---|---|---|
| S13 to the last, C1 | 70–93% | 79.8% |
| S10_fix, C1 | 6–23% | 14.4% |
| S3, C2–C4 | 14–32% | 13.3–24.5% |

These do **not** reproduce:

| Figure | TUNING | Harness |
|---|---|---|
| S8, C1 / C5 / 4P | 57 / 49 / 41 | 64.5 / 26.5 / 30.0 |
| S10, C1 / C3 | 82 / 45 | 50.7 / 19.9 |
| S4, C1 | 86%, 3.0 drops | 69.8%, 1.66 |
| S3, C5 | 83% | 46.4% |
| S13 to Draunel Bloodied | 39–74% | 4.5–34.7% |
| S2, C1 | ≤ 37% | 44.1% |

Lone PC (F2; 2,000 runs, any drop %):

| Card | Dassa | Pello | Serane | Andra | Ilesse | TUNING |
|---|---|---|---|---|---|---|
| S2 | 79 | 98 | 100 | 72 | 100 | 71 / 91 / 100 / 100 / 99 |
| S8 | 99 | 100 | 100 | 100 | 100 | 89 / 99 / 100 / 100 / 100 |
| S10 | 88 | 95 | 100 | 100 | 100 | 97 / 100 / 100 / 100 / 100 |
| S7 | 17 | 23 | 100 | 16 | 100 | 19 / 33 / 100 / 51 / 52 |

The verdicts carry over, though the cells do not match exactly. S2, S8 and S10
alone are near-certain drops for everyone. S7 alone is survivable only for the
armored or the Shield-casters.

### Chain (2,000 runs)

| Measure | TUNING (3P) | Harness |
|---|---|---|
| PC death across the chain, strict crowd rule | 15–21% | C1 18.2, C2 19.5, C5 17.2; C3 4.7, C4 12.9 |
| PC death, generous crowd rule | 5–7% | 1.1–2.5% |
| HP at the gate, S14 + S13 | 15–21% | **57–81%** (with between-scene healing); 49–57% without |
| Same, after a Movement V card (S2) first | 5–9% | 44–70% |

## Gaps, and the best explanations

Nothing was tuned to force a match. The policy choices above were made from the
TUNING text and the rules, and where a choice moved a number the README says so.

1. **S14 C1 is 3.4 points low (87.3 against 90.7).** The original trick lists are
   lost, and the S14 win rate turns on how many distinct high-bonus tricks a party
   can field before it must repeat. This harness gives each pregen one trick per
   habit. Giving each habit two stagings pushed every trio to 96–99%, well above
   TUNING, so one per habit is the closer reading. Ilesse's cup trick uses
   Persuasion (+4) and Dassa's cloak uses Charisma (+0), which is where C1 loses
   ground. TUNING's original may have scored those tricks more generously.
2. **The skirmish cards run softer for strong-damage parties (C3–C5, 4P) and about
   right or harder for C1.** TUNING's numbers imply longer fights for every party
   (S10 C1 at 2.5 drops; S3 C5 at 83%, the whole party down 26%). Likely
   differences:
   - TUNING's casters may have spent fewer slots on damage. Andra's Magic
     Missile from 2nd-level slots ends fights fast here.
   - Pello's Steady Aim is used every turn here.
   - The wicket may have been modelled with more friction (the grille's cover,
     or PCs behind it unable to attack).
   - S13 may not have ended at Draunel Bloodied for every party. Here the party
     focuses Draunel, so fights end in about 2–5 rounds.
3. **The chain's HP at the gate is far higher than TUNING's 15–21%.** S14 here
   costs C1 about 28 HP net and S13 about 29, against TUNING §5's 40–60 and about
   60 (TUNING's may be gross damage taken, before healing). Even without
   between-scene healing the party reaches the gate at about half HP. TUNING's
   chain probably ran S13 longer (see 2) and let less healing land. Death rates
   under the strict crowd rule do land in TUNING's band for C1, C2 and C5,
   because most deaths come at the S3 wicket.
4. **The tight-clock smart win at four PCs (42.7% against 8–11%).** With 229 HP
   and full Multiattack on both turns, TUNING's 4P party fared much worse. Here
   the free-Delay rule lets a 4P party buy about 1.3 Delay even on a tight clock.
   TUNING's 4P smart policy may have bought Delay differently: it reports 3.06
   Delay on the book clock but a lower win rate.

Use the harness for **comparisons between rule variants** (old against new, a fix
against as written, one party against another); that is what T5.8–T5.9, T3.10 and
the other SIM rows need. Quote absolute snake-card rates only alongside the
assumptions above.
