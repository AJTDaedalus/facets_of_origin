# Audit — Oraga Night 5e: Combat and Rules Quality

*2026-09-27. Read-only audit of `conversions/dnd5e/oraga_night/` on `feat/oraga-5e`
(PR #33). Focus: 09 (S1–S13, Snake Tracker), 10 (24 blocks, Items of the Night),
11 (pregens), 05 (the attack, Fractures, B12), and `docs/REVIEW_oraga_5e.md`. The
lens is an experienced 5e designer and an optimising player. Nothing in the module
was edited.*

---

## Executive verdict

The arithmetic is clean. Every HP value, attack bonus, save DC, PB, XP sum and pregen
number I re-derived matches (the integration review's claim holds, see Appendix D).
The blocks are readable, the Wants/Tells/Breaks/Nastier lines are the best thing in
the chapter, and there is no non-SRD content. **Most snake cards are well tuned for
what they are:** short, morale-capped fights (1–4 rounds) where the clock is the
real opponent. Six of the thirteen are trivial by design and say so.

The problems are in three places:

1. **S3, the one fight the night can't avoid, can't be run as written.** It has no
   battlefield (the gate is shut and the Bought are on the far side), its "fight
   through" condition says *or* in one place and *and* in another, and its own fire
   clock ends the fight by ending 3 in about three rounds, so waiting is the
   dominant strategy. Which reading the MM picks swings the outcome from "won by
   force in 2.9 rounds, 14% chance a PC drops" to "never won by force, 75–85%
   chance a PC drops". (C1)
2. **The scaling is broken for the default table.** The module ships **five**
   pregens. Every card sends "five characters" to the same scaling line as "4th–5th
   level", but those parties differ by up to 2.7× in XP budget. So the default
   table is over-scaled (scaled S13: 39% chance the whole party is down, after
   midnight, in a fire), and a true 5th-level table is under-scaled (scaled S3 is
   about half of Low). (C2)
3. **The Uninvited are hard to *kill*, but not to *stop*.** Their condition
   immunities hold, and Leashed holds. But the "the table tries" list misses the
   tools a 3rd–5th-level table actually has: Web and grapples on a Witnessed
   Radiant, *blindness/deafness*, *sanctuary*, *invisibility* on the quarry,
   *slow*, and *tiny hut* at 5th. The one cross-reference that was supposed to
   answer this points at nothing. Ward-steering has no limit on uses or duration,
   and the Orthaen Gift's advantage stacks on it. That combination can hold the
   Wept off Raunu indefinitely, against the text's fiat "then the Wept is through
   the last barrier". (M2, M3)

None of these is a rewrite. Each has a one-paragraph fix (below).

**Counts:** 2 Critical · 9 Major · 17 Minor.

---

## Method

- **Budgets** use SRD 5.2.1 XP per character (3rd: 150/225/400) summed with no
  multiplier, as the module does.
- **CR sanity** uses the DMG-style offense/defense guideline (HP/AC for defensive
  CR; DPR over three rounds and attack bonus for offensive CR; ±1 CR per 2 points of
  AC or attack off-baseline; resistance multiplies effective HP). The SRD has no
  creation table. This is the industry yardstick, not a rule.
- **Simulation.** I ran a Monte Carlo, 4,000–5,000 fights per cell, with three
  parties:
  - **pregen5**: the five pregens as statted.
  - **pregen4**: Dassa, Pello, Andra, Ilesse.
  - **opt4**: a typical optimised 3rd-level party. Paladin (AC 18, Dueling, 3
    smites); Rogue (rapier + Steady Aim); Sorcerer (2× *scorching ray* with Innate
    Sorcery, then *fire bolt*); Cleric (AC 18, *bless*, *spiritual weapon*).

  Tactics:
  - PCs focus the weakest foe. Andra opens with *magic missile* and uses *shield*
    on about half of qualifying hits. Ilesse opens with *bless* on the melee PCs.
    Healers use 2024 *healing word* (2d4 + mod) on downed allies.
  - Enemies pick targets at random, weighted 2:1 toward melee PCs (1:1 for ranged
    foes).
  - Every morale, arrival, parry, Uncanny Dodge, Sneak Attack, advantage and
    To-the-Terms clause is modelled as printed. Movement, cover and outs are not
    modelled.

  "Drop%" is the chance at least one PC hits 0 HP. "All-down%" is the chance the
  whole party does. Full table in Appendix A.

**Reference DPR** (sustained, against AC 15; opening round with slots in brackets):

| Party | Math | Sustained | Nova |
|---|---|---|---|
| Dassa | 1d10+3 two-handed, Savage Attacker: best of 2d10 = 7.15 + 3 = 10.15 × .55, + crit 19–20 (.10 × 5.5) | 6.1 | 12.2 (Action Surge) |
| Pello | .55 × 5.5 + .55 × 2.5 (Nick, no mod) + (1 − .45²) × 7 SA | 10.0 | 10.0 |
| Andra | *fire bolt* .55 × 5.5 + .45 × 2.75 (Potent Cantrip) | 4.3 | 10.5 (*magic missile*) |
| Ilesse | *sacred flame* vs Dex +1: .55 × 4.5 | 2.5 | 7.7 (*guiding bolt*) |
| Serane | *vicious mockery* vs Wis +0: .60 × 3.5 | 2.1 | 2.1 |
| **pregen5** | | **≈ 25** | **≈ 42** |
| **opt4** | Paladin 10.2 (5.2 after smites), Rogue 11.6, Sorcerer 3.0 (16.8 with *scorching ray*), Cleric 6.6 | **≈ 26–31** | **≈ 45** |

The pregens hit about as hard as an optimised party. What they lack is
**defence**: three of five are at AC 11–12 with 20–21 HP (M7).

---

## Findings (ranked)

### Critical

**C1 — S3 *The Gate at Midnight* has no battlefield, contradictory win conditions,
and a clock that makes waiting the dominant strategy.** *(09 S3; 10 Bought
Sergeant/Blade/Captain; 05 B12)*

*Evidence.*
- **(a) No battlefield.** The trigger says "The outer gate is shut, and it was shut
  from the far side. Through the grille: matched grey coats." The objective is
  "open the way out". But no text says:
  - how the gate opens (bar, winch, lock DC, Strength DC, AC/HP);
  - where the Blades stand;
  - how melee happens through a shut gate;
  - what the "gatehouse stair" connects.

  The grille gives Three-Quarters Cover, so the default fight is two lines poking
  through bars. 04 explicitly has no B12 map ("B12 is … Chapter V"), and 05 B12
  defers back to the card.
- **(b) Contradictory end condition.**
  - Morale: "The Blades disengage … when the sergeant falls **or** half of them are
    down."
  - Ending 1: "Drop the sergeant **and** half the Blades."
  - Sergeant block, Breaks: "When Bloodied it calls the Blades back to the
    boundary".
  - Captain: "arrives … the round the sergeant falls" and invokes the Second
    Clause "the round after the party looks like winning".
- **(c) The clock ends the fight.** The fire clock advances every round plus on
  any natural 1 or check failed by 5. With about ten d20s rolled per round that is
  ≈ 1.45 segments a round, so it fills in about **3 rounds**. Ending 3 ("on the
  clock's last segment … the captain calls the withdrawal … if the party has held
  even one round") then ends the fight in the party's favour. The captain arrives
  on segment 2 and spends its first turn on *The Read* (no attacks), so it
  usually never swings.

*Simulation (Appendix A).*

| Reading | pregen5 | pregen4 | opt4 |
|---|---|---|---|
| OR (morale), +1 round for the Second Clause | won by force in 2.9 rds, 14% drop | 3.0 rds, 22% drop | 2.8 rds, 13% drop |
| AND (ending 1), no clock cap | 72% won by force, 6.4 rds, 92% drop, **28% all-down** | 23% won, **77% all-down** | 67% won, 33% all-down |
| AND, capped at the clock's round 4 | 4% won by force, 75% drop | 1% won, 85% drop | 24% won, 66% drop |

The Blades' *To the Terms* floors their damage at 1 HP and grapples, so **Blades can
never drop a PC** and a PC at 1 HP keeps fighting. Every drop comes from the
sergeant and captain, who have no *detain* clause. A PC they drop makes death saves
beside a filling fire clock.

*Why it matters.* This is the night's only unavoidable scene and the one the
designer's note says a table "most needs" to answer with a sword. As written, the
MM must invent the geometry, choose between two rules that differ by roughly 60
points of drop chance, and the players' best play is to stand still.

*Fix.*
1. Add a three-line battlefield. For example: the gate is barred on the far side
   (AC 15, 30 HP, or DC 18 Strength to lift the bar through the grille). The
   sergeant and four Blades stand **inside** the court, between the crowd and the
   gatehouse door. The gatehouse stair (inside the court) leads to the winch room
   above the arch, and the winch raises the grille.
2. Make "fight through" one condition, "sergeant down **or** half the Blades down",
   and delete the conjunctive wording.
3. Decouple ending 3 from the fire clock. Give the sect guard its own 6-segment
   clock (1 per round), so holding costs the crowd rounds and isn't free.
4. Add *detain* to the sergeant and captain ("Nobody in the Bought is paid to
   kill"), or say plainly that they are lethal.

---

**C2 — The scaling line lumps "five characters" with "4th–5th level", and the module
ships five pregens.** *(every card's *Scaling*; 09 Table IX–1; 11 header)*

*Evidence.* Table IX–1's own numbers put five 3rd-level characters at Low 750,
Moderate 1,125, High 2,000, and four 5th-level characters at 2,000 / 3,000 / 4,400.
Every card nonetheless says "*4th–5th level, or five characters:*" and gives one
roster.

| Card, scaled | XP | vs five 3rd | vs four 4th | vs four 5th |
|---|---|---|---|---|
| S3 (+2 Blades) | 1,050 (2,150 with captain) | Low–High | Low–High | about ½ Low |
| S7 (4 knives) | 800 | ≈ Low | under Low | 40% of Low |
| S13 (Draunel + 3 duelists, one Nastier) | 1,550 | Moderate–High | ≈ Moderate | under Low |

Simulated against the five pregens:
- **Scaled S13:** 99% drop, **39% all-down** (**89%** for pregen4). This is after
  midnight, where damage is lethal and the burning gallery deals 2d6 fire a turn to
  anyone lying in it.
- **Scaled S3:** 88% all-down under the AND reading.

A true 5th-level party (Extra Attack, *fireball*, *spirit guardians*) crushes every
scaled card in one or two rounds.

*Why it matters.* The default table (the five pregens) reads the card, sees "or five
characters", and runs the version tuned for a party roughly twice as strong. The only
real 5th-level table gets a version tuned for one roughly half as strong.

*Fix.* Split every Scaling line into three: *Five at 3rd:* add one retainer (never
a leader). *Four at 4th:* add one retainer plus the Nastier line. *Four at 5th:* the
card's roster ×2 retainers plus Nastier, or "keep it as is; at 5th the clock is the
fight". Say at the top of Chapter IX that **the pregen party is five, and the base
cards are already tuned for it** (the sim bears this out; see Appendix A).

---

### Major

**M1 — The Radiant's *The Rite* can never be used.** *(10 The Radiant)*

The Rite is a separate action that targets "one creature within 5 feet **that the
Radiant hit this turn**". Multiattack (three Offered Hands) doesn't include it, and
the Radiant has no Bonus Action or Reaction attack. If it uses The Rite, it has made
no attack this turn, so the target clause can never be met. The signature "staged
kill, offered upward" is dead text.

*Fix:* "Multiattack. The Radiant makes three Offered Hands attacks. It can replace
the last with The Rite if it is available." The Rite's DC 17 stays.

**M2 — The Uninvited's "the table tries" table misses the tools a 3rd–5th-level
table has, and the cross-reference that should cover them points at nothing.** *(10
"The Uninvited, Before You Read Their Blocks"; 05 sidebar "Crystals gutter", *You
Cannot Beat Them*)*

05's sidebar says: "What the Uninvited do to player characters' own spells is in
their stat blocks, Chapter X. It is less than this, and it is never nothing." It
isn't there. *Unraveling Presence* affects only crystal charges and great wards.

Attempts that break or bend the design (full detail in Appendix C):
- **Web, a grapple, or any restraint on the Radiant while Witnessed.** Shadow-Step
  is forbidden while Witnessed, so the table's "Grapple it → It steps into shadow"
  row is **wrong for the Radiant**. It must spend its action on the escape check
  (Web DC 13 Str: 55%; Dassa's grapple DC 13: 85% on Acrobatics).
- ***Blindness/deafness*** (bard/cleric 2nd). Blinded isn't in their immunities.
  The target attacks with disadvantage and **can't Shadow-Step** (needs "a space it
  can see"), so the Wept loses *She Arrives*. Con saves: Wept +8 (fails 25%),
  Radiant +2 (fails 50%), Hollow +7 (30%), plus a save at the end of each turn.
- ***Sanctuary*** on Raunu or Veier (Ilesse has it prepared). Each attack needs a
  DC 13 Wisdom save (Wept/Radiant +7, so it loses about 25% of attacks). Whether
  this counts as "compelled" under *Held by Something Else* is unstated.
- ***Invisibility*** on Veier (bard/wizard/sorcerer 2nd). The Radiant has only
  darkvision. Nothing addresses it.
- ***Darkness*** (Andra has it). It **speeds the Radiant up**: not Witnessed means
  full 40 ft and Shadow-Step. It also earns the Fracture check. The interaction is
  good, but the MM needs to be told.
- ***Slow*** (5th). No listed immunity: one attack, half speed, −2 AC.
- ***Tiny hut*** (5th, ritual or 1-minute cast; SRD name *Tiny Hut*). A force dome,
  not an "ordinary barrier", and opaque from outside, so Shadow-Step can't target
  inside. As written it is **a safe room for Veier or Raunu until the last bell**.
  05's catch-all ("holds it for no longer than the leash allows") is ambiguous:
  the leash allows until the last bell.

*Why it matters.* Every one of these is SRD and plausible at the pregens' level or at
the 5th level Table IX–1 supports. Only tiny hut breaks canon. The rest buy time,
which the design welcomes, but the MM will rule on each mid-combat with no guidance.

*Fix.* Replace the dangling sentence with one universal rule in *Leashed*: "**Any
effect that would hold, block, hide from, or wall off an Uninvited — spell, grapple,
barrier or blindness — works for 1 round, then fails. Deep Boranis ward-crystal is
the only exception.**" Then add three table rows: *Web, grapple, restraint (the
Radiant while Witnessed can't step out of it: 1 round)*; *Blindness, invisibility,
sanctuary (1 round)*; *Darkness (denies the Radiant its witnesses: faster, and the
Fracture check)*.

**M3 — Ward-steering has no limit on uses or duration, and stacks with the Orthaen
Gift's advantage.** *(05 "The palace fights back", default beats "the dais", ⟨They
trap one⟩; 03 Orthaen Gift)*

- **At Raunu's side** the check is DC 10, and "each success is a ward between the
  Wept and the crowd, and **costs the Wept a round**." There is no count of wards.
- **Gift Knack** gives advantage on checks "to coax, shape, read, or judge grown
  crystal and any working held in it". Three of the five pregens are gifted
  Orthaen. Andra: Arcana +5 with advantage against DC 10 is 96% per round.
- The general DC 13 steer (seal a corridor, shelter a dozen guests from the snakes)
  has **no duration**.
- **Trapping** an Uninvited is DC 18 (51% for Andra with advantage), or DC 13 from
  the Root (88%), and holds until the last bell.

So a table can keep the Wept off Raunu indefinitely, and the text resolves it by
fiat ("Then the Wept is through the last barrier"). Players who succeed every round
will feel cheated.

*Fix.*
- Give Raunu a visible **ward pool**: 3 + 1 per player character at his side, each
  success spending one. Say the number out loud.
- Give general steers a duration: a sealed corridor holds 10 minutes against
  snakes, and 1 round against an Uninvited.
- Rule on Gift Knack: either it applies to steering (and the DCs rise to 15/20), or
  it doesn't.

**M4 — "Death before midnight" lets a character die in-scene.** *(09 "The Fight
Cards")*

The rule says "a player character who drops in a snake fight before the bells is
**Stable when the scene ends**". Until then they roll death saves. The chance of
three failures in the first three saves (a natural 1 counting double) is about 10%,
and it rises over a 4–5 round fight. That contradicts rule 2 ("no snake is the reason
a player character dies before midnight"). S1, S4, S6 and S8 are safe because of
*detain*/*Honest Brawl*. S2, S7, S9 and S10 are not.

*Fix:* "…is **Stable at once**, and wakes with 1 HP when the scene ends."

**M5 — S9's circle clock fills before the party can act.** *(09 S9; 10 Draunel
Duelist *Provocation*)*

The clock advances "by **two** whenever a Cousin's Blade fails its save against
Provocation and draws". Provocation is DC 12 against Wis +0, so each save fails 55%
of the time, and it is part of every duelist Multiattack. With two duelists acting
before the party (likely: Init +3 vs +1–4), the chance a cousin draws before any PC
acts is 1 − .45² ≈ **80%**, which fails the card's first objective ("nobody draws")
and its Heroic Inspiration. The clock is usually full by the end of round 2.

*Fix:* the duelists don't use Provocation until the round after a player character
steps onto the grass. Each cousin can draw once (+2 once per cousin). Essin arrives
on segment 1, not 2.

**M6 — S13 is labelled "between Moderate and High" but plays High, in a room where
the fire kills downed characters.** *(09 S13; 10 Essar Draunel)*

- Draunel's three rapier attacks at +5 are 14.6 DPR against the pregens' mean
  AC 13.
- Fought to the last: pregen5 **61%** drop, pregen4 **71%** drop with **10%**
  all-down, opt4 42% drop.
- "A creature that … starts its turn in [the fire] takes 2d6", and damage at 0 HP
  is an automatic failed death save. A PC who drops near the far end dies in about
  two turns. "No snake finishes a downed character" doesn't cover the fire.

*Fix:* add "a creature that drops in the gallery is dragged clear by a guest at the
end of the round". Cut Draunel to two attacks plus Parry (still CR 3 by the
guideline), or label the card High.

**M7 — The SRD 5.2.1 budget undershoots multiattack humanoids, and the pregen party is
softer than the budget assumes.** *(09 budgets; 10 CRs; 11)*

The budget labels and what actually happens (Appendix A, fought to the last):

| Card | Label | pregen4 drop | Reading |
|---|---|---|---|
| S2 | "Low" (600) | 41% | Tavva's two knives plus Sneak Attack is 13.3 DPR, more than her CR 2 by the guideline |
| S13 | "Moderate–High" | 71%, 10% all-down | High |
| S7, S11 | "Low" | 23% | Low, correctly |

Contributing causes:
- **Pregen defence.** The pregens' mean AC is ≈ 13 (Serane 12, Ilesse 11, Andra 12
  or 15 with *mage armor*). The opt4 party (two AC 18s) drops about half as often
  on every card.
- **Dassa's AC.** The "frontliner" is AC 14 (studded leather + Defense), though the
  module allows "armor included if they can dance in it". A chain shirt gives 15
  (+1 Defense); the SRD Fighter kit's chain mail gives 17.

*Fix:*
- Give Dassa a chain shirt (AC 15) or breastplate (AC 15 + Defense = 16), and
  Serane leather (AC 13, bard proficiency).
- Add one line to "How to Read This Chapter": "Blocks with three attacks or Sneak
  Attack run a step hotter than their XP."
- Re-label S2 "Low; Moderate if fought to the last".

**M8 — No crowd or mass-combat rules, in a module whose big scenes happen in a crowd
of 200.** *(05 attack; 09 S3, S11; 10 Hollow *The Post*)*

Missing:
- **A guest line.** No commoner-like stat (AC 10, HP 4) and no density rule. What
  do *shatter*, *thunderwave*, *sleep*, a Dark-Burst, *fireball* at 5th, or the
  Hollow's cone do in the Crystal Court?
- **Collateral.** A caster who kills a guest with an area spell is unaddressed.
- **The Post.** A DC 17 Strength save per creature: does each of 200 guests roll?
- **Retinues at the gate.** After midnight Essin's cousins, Draunel's duelists,
  Maiven's slingers and Corro's bodyguards are all in the crowd at S3. Can the
  party recruit them? The sim shows one extra ally removes most of S3's drop risk.
- **The perimeter.** "Twelve hold the perimeter" but only four are placed.

*Fix:* a half-page sidebar in 05:
- "*A crowd:* each 5-ft square of the Crystal Court holds one guest (AC 10, HP 4,
  no attacks). An area effect catches one guest per square. A guest killed by a
  player character is seen, and Chapter VI hears of it."
- "*The Post:* the crowd doesn't pass; guests leave only by the service doors or
  the gate."
- "*Allies at the gate:* each retinue the party brings removes one Blade from the
  fight, or holds the gate one round after the sergeant falls."

**M9 — Fracture and Leashed edge cases an MM will hit mid-combat.** *(10 *Leashed*,
the Wept's *When Bloodied*, the Fractures; 05)*

- **Leashed's "last blow" is ambiguous and punishing.** It "removes whoever dealt
  the last blow — that creature drops to 0 HP". Who takes it if the last blow is
  the burning gallery, falling masonry, *spiritual weapon*, a web fire, or a single
  area spell from two casters? And the player who lands the finishing point of 187
  loses the rest of the night: Stable 0 HP regains 1 HP after 1d4 hours.
  *Fix:* "…is thrown 30 ft clear, has the Prone condition and loses its next turn";
  if no creature dealt it, nobody.
- **The Wept's Bloodied phase is unreachable in a fair fight.** Resisted damage
  against AC 18 at the pregens' DPR is 10–15 a round; she needs 94. The one way
  there is degenerate: 05 principle 1 says an Uninvited "never targets a creature
  that is not between it and its errand", so ranged PCs behind her take no risk and
  get there in about 8 rounds. *Fix:* key the DC 15 drop to "after she has broken
  through three wards" or "once Raunu has spent his first crystal", not to HP.
- **Stacking speed halves.** Witnessed halves the Radiant's speed and its Fracture
  halves it "whether or not it is Witnessed". Is it 40 → 10?
- **Undefined jargon.** "The MM makes a move" is PbtA, not 5e. Spell it out: one
  attack against the speaker, or the scene gets worse.

---

### Minor

| ID | Location | Finding | Fix |
|---|---|---|---|
| m1 | 11 Serane | "every other skill +1 (Jack of All Trades)" is wrong. JoAT adds +1 to the *ability modifier*: Acrobatics/Sleight/Stealth +3, Athletics +0, Medicine/Survival/Animal Handling +2, Arcana/Nature +1 | List the real numbers |
| m2 | 11 Pello | The Nick attack is listed as 1d4 + 3. The Light-property extra attack adds no ability modifier: the second dagger is 1d4. Vex (shortsword) is chosen but he carries no shortsword | "second dagger 1d4"; swap Vex for Slow (shortbow/sling) or give him a shortsword |
| m3 | 11 Ilesse | *Warding bond* needs a pair of platinum rings worth ≥50 GP each; she carries 50 GP and no rings, so she can't cast her one non-domain 2nd | Give her the rings, or swap to *spiritual weapon* (SRD) |
| m4 | 11 Dassa | Int 8, Cha 10, no social proficiency beyond Insight/Intimidation, in a social-heavy night. Tactical Mind (+1d10 to a failed check) partly saves her | Swap Savage Attacker for Skilled (Persuasion, Perception, Investigation) and note that Tactical Mind is her social tool |
| m5 | 10 CRs | Guideline check (Appendix B). Overrated: Cousin's Blade (≈ 1/4 vs 1/2), Border Slinger (≈ 1/4 vs 1/2), Draunel Duelist (≈ 1/2 vs 1), Callun (≈ 1/8 vs 1/4), Nastier Sergeant (≈ 3 vs 4). Underrated: Honor Guard (≈ 2.5–3 vs 2; it is the SRD Knight's chassis, CR 3). Uninvited: Wept ≈ 13 vs 11 (cosmetic, no XP) | Adjust, or note "XP pays the scene, not the danger" |
| m6 | 09 S11 | Base roster already has three bodyguards (600 XP), and the Scaling "Nastier line — a third" adds nothing; 09's Phern line says "two or three" | Base two (400 XP, Low for five), Nastier adds the third |
| m7 | 09 S1, S2, S3, S8 | "Whenever anyone rolls a 1 on a d20" is ambiguous: do initiative, saves and a Heroic Inspiration reroll count? It also scales with head-count (eight kinsmen tick faster than six) | "An attack roll or ability check (not initiative or saves); once per round at most" |
| m8 | 09 S2, S7; 10 Hired Knife | "Dim Light … Step Aside (Hide) at its best here". Under 2024 Hide you need Heavily Obscured or ¾/total cover; Lightly Obscured isn't enough. Stealth advantage in dim light is a house rule | Give the run crates/doorways (¾ cover), or say it's a house rule |
| m9 | 05 attack; 11 | All-human party, no darkvision, in corridors that are "darkness except where a ward flares". Witnessed needs the pursuer to see the Radiant; the chase rule (DC 13 per beat) ignores light; a Steady Light within 30 ft needs DC 13 Cha | One line: "pursuing the Radiant in the dark needs a light; a failed charge means it is not Witnessed" |
| m10 | 10 Honor Guard | Warder "releases one **instead of attacking**": the action, or one Multiattack attack? The 2024 form is "(1/Day Each)". No Gear lines on NPC blocks | "…in place of one House Blade attack" |
| m11 | 10 Items; 05 | Do *running* charges (a Steady Light already lit, a Sealed Door) gutter when an Uninvited comes within 30 ft, or only releases? | "Active charges within 30 ft go dark for as long as it is near" (or not) |
| m12 | 03 Grow a Charge | Free, one day per common charge (worth 50 GP), against the SRD crafting baseline for a common item (5 days, 50 GP of materials). A money printer in the aftermath wing | Add "and 25 GP of crystal", or once per week |
| m13 | 09 all pre-midnight cards | 2024 *Knocking Out* is melee-only. A *fire bolt* or *magic missile* that drops a snake's retainer kills a guest at a ball, and no card says what that costs | "At this ball any attacker may declare a blow nonlethal", or list the consequence |
| m14 | 09 outs; 11 Serane | *Suggestion*, *charm person*, *calm emotions* and *hideous laughter* are Serane's best tools, and 04 prices covert casting at DC 13 Sleight of Hand. No card says whether a landed enchantment is an out (2024 *charm person*: the target knows afterward) | One line in "Running the Snakes": "A charm or suggestion that lands is an out; the target knows by morning" |
| m15 | 09 S2, S7, S8 with 10 Items | A *Veil of Quiet* (Serane and Ilesse each carry one) should silence "anything loud", but the noise clock also ticks on "each round anyone attacked with a drawn blade" | Say whether the Veil stops that tick |
| m16 | 01 Table I–1; 09 | "Heroic Inspiration per person carried out": 2024 allows only one at a time (extras must be given away) | "…or give it to a companion who has none" |
| m17 | 09 S7, S12 | Knives break "when the first of them is Bloodied" (16 damage). The sim ends the fight in round 1 in ~100% of runs for every party. The two-attack CR 1 block is over-built for a one-round presence (the design intends the clock to carry it, which is fine) | Use the Gallery Knife chassis (CR 1/4), or break at "half down" |

**Non-SRD content (lens 7): none found.** I scanned for proprietary names
(Leomund, Tasha, Otiluke, Bigby, Mordenkainen, Melf, *silvery barbs*, *toll the dead*,
*booming blade*, *hex*, *eldritch blast*, *hunter's mark*, setting names). Every spell,
feat, class feature, weapon mastery, condition and area term the module uses is
SRD 5.2.1, matching the review's verification. All creatures are original blocks.
Crystal-charge prices (common 50 GP, uncommon 200 GP) match the 2024 rarity values at
consumable half-price. If the module ever names the dome spell (M2), use *Tiny Hut*,
not *Leomund's*.

---

## Appendix A — Per-card simulation

Win ends as each card prints (morale/breaks) unless "to the last". "Rds" is mean
rounds. Budgets are the cards' own.

| Card | XP · label | pregen5: end / rds / drop / all-down | pregen4 | opt4 | Verdict |
|---|---|---|---|---|---|
| S1 six kinsmen (nonlethal; hurt = steps back) | 150 · trivial | 100% / 1.8 / 0% / 0% | 100 / 2.0 / 0 / 0 | 100 / 2.0 / 0 / 0 | Trivial as stated; the bench clock (≈1.4 segments/round) is the fight |
| S1 scaled, eight kinsmen | 200 | 100 / 2.0 / 0 / 0 | 100 / 2.2 / 1 / 0 | 100 / 2.2 / 1 / 0 | Trivial at any level |
| S2 until Tavva is Bloodied | 600 · Low | 100 / 2.7 / 18 / 0 | 100 / 2.9 / 26 / 0 | 100 / 2.3 / 12 / 0 | Low; noise clock ≈ 1.34/round, so it fills before she breaks ≈ 30–40% of the time |
| S2 to the last | — | 100 / 3.6 / 32 / 0 | 99 / 4.1 / 41 / 1 | 100 / 2.9 / 19 / 0 | Moderate in practice (M7) |
| S2 scaled (+1 knife) | 650 | 100 / 3.3 / 31 / 0 | 99 / 3.7 / 40 / 1 | 100 / 2.7 / 21 / 0 | OK for five at 3rd |
| S3 as morale says (OR), +1 round | 850–1,950 | 100 / 2.9 / 14 / 0 | 100 / 3.0 / 22 / 0 | 100 / 2.8 / 13 / 0 | Easy (C1) |
| S3 as ending 1 says (AND) | — | 72 / 6.4 / 92 / **28** | 23 / 6.2 / 98 / **77** | 67 / 5.3 / 77 / 33 | Deadly (C1) |
| S3 AND, capped at round 4 (fire clock) | — | 4 / — / 75 / 0 | 1 / — / 85 / 1 | 24 / — / 66 / 0 | The clock ends it (C1) |
| S3 to the last, captain included | 1,950 · over High | 17 / 9.3 / 100 / 83 | 0 / 6.8 / 100 / 100 | 10 / 7.4 / 100 / 90 | "Honest warning" is honest |
| S3 scaled (6 Blades), AND | 1,050–2,150 | 12 / 7.0 / 100 / 88 | 0 / 5.5 / 100 / 100 | 12 / 5.9 / 99 / 88 | Over-scaled for five (C2) |
| S4 two guards, +4 on *Call the House* | 900 → 2,700 | 0 / 6.2 / 100 / 93 | 0 / 5.0 / 100 / 100 | 0 / 5.8 / 100 / 95 | Unwinnable by design; *detain* keeps it safe |
| S6 two cousins | 200 | (not simmed: 44 HP of AC 14, +4 one attack each) | — | — | Trivial |
| S7 three knives, break at first Bloodied | 600 · Low | 100 / **1.0** / 0 / 0 | 100 / 1.0 / 0 / 0 | 100 / 1.0 / 0 / 0 | Combat trivial; the clock and the chase are the card (m17) |
| S7 to the last | — | 100 / 3.6 / 14 / 0 | 100 / 4.0 / 23 / 0 | 100 / 3.0 / 7 / 0 | Low |
| S7 scaled, four to the last | 800 | 100 / 5.1 / 55 / 0 | 89 / 5.8 / 71 / 11 | 99 / 4.1 / 35 / 1 | Moderate for five |
| S8 wardens (third on round 3), break at 2 down | 600 · Low | 100 / 2.5 / 3 / 0 | 100 / 2.7 / 5 / 0 | 100 / 2.2 / 1 / 0 | Low; *detain* |
| S8 scaled, four wardens | 800 | 100 / 2.6 / 24 / 0 | 98 / 2.8 / 34 / 2 | 100 / 2.2 / 14 / 0 | Fine |
| S9 both sides, with morale | 600 · Low | 100 / 2.2 / 3 / 0 | 100 / 2.3 / 4 / 0 | 100 / 2.0 / 2 / 0 | Trivial as a fight; the clock is too fast (M5) |
| S10 Maiven (round 3) + two slingers, to the last | 900 · Moderate | 100 / 4.5 / 8 / 0 | 100 / 4.7 / 13 / 0 | 100 / 4.1 / 4 / 0 | Low in practice; the half-bell clock (1/round) fills at round 4, so S4 lands mid-fight |
| S10 scaled, three slingers | 1,000 | 100 / 4.7 / 16 / 0 | 100 / 5.0 / 25 / 0 | 100 / 4.1 / 9 / 0 | Fine |
| S11 three bodyguards, to the last | 625 · Low | 100 / 3.8 / 16 / 0 | 100 / 4.0 / 23 / 0 | 100 / 3.0 / 7 / 0 | Low; the crowd check (DC 13, prone + 1d6 a turn) is the real cost |
| S12 two knives, break at Bloodied | 400 | 100 / 1.0 / 0 / 0 | 100 / 1.0 / 0 / 0 | 100 / 1.0 / 0 / 0 | Trivial |
| S13 Draunel + two duelists, to the last | 1,100 · Mod–High | 100 / 4.8 / **61** / 0 | 90 / 5.4 / **71** / **10** | 98 / 3.9 / 42 / 2 | High (M6) |
| S13, duelists break at Bloodied | — | 100 / 3.8 / 40 / 0 | 97 / 4.3 / 53 / 3 | 100 / 3.1 / 24 / 0 | Moderate–High |
| S13 scaled (three duelists, one Nastier) | 1,550 | 61 / 7.2 / 99 / **39** | 11 / 5.6 / 100 / **89** | 54 / 5.7 / 93 / 46 | TPK risk for the default table (C2) |

**Summary.**
- **Trivial, and say so:** S1, S6, S9, S12, plus S7/S8 as fights.
- **Low and honest:** S2 to Bloodied, S7 and S11 to the last, S8, S10.
- **Mislabelled hot:** S2 to the last, S13.
- **Broken:** S3 (C1).
- **Scaled for five:** S13 and S3 turn into TPK risks (C2).
- **None are TPK risks before midnight**, because of *detain* and morale.

---

## Appendix B — CR by the guideline (selected)

DCR is defensive CR from HP (×1.25–1.5 for BPS resistance) and AC (±1 per 2 off
baseline). OCR is offensive CR from 3-round DPR and attack bonus. The reading is the
average.

| Block | Listed | DCR | OCR | Reading |
|---|---|---|---|---|
| Honor Guard (AC 18, 52 HP, 2 × +5 7.5) | 2 | 2–3 | 3 | 2.5–3 (SRD Knight chassis) |
| Bought Captain (AC 17 + Parry, 97 HP, ≈ 21 DPR) | 4 | 4–4.5 | 3.5 | 4 ✓ |
| Bought Sergeant (AC 17 + Parry, 52 HP, 13 DPR) | 2 | 2.5 | 1.5 | 2 ✓ |
| Nastier Sergeant (78 HP, 3 × 7.5) | 4 | 3 | 3.5 | ≈ 3 |
| Tavva (AC 15, 44 HP, Uncanny Dodge, 18 DPR) | 2 | 1 | 3 | 2 ✓ (offence-heavy) |
| Essar Draunel (AC 16 + Parry, 58 HP, 22.5 DPR) | 3 | 2.5 | 3.5 | 3 ✓ (offence-heavy) |
| Vorlain (AC 15 + Parry, 60 HP, 22 DPR) | 3 | 1.5 | 3.5 | 2.5–3 ✓ |
| Essin (AC 14, 45 HP, 18 DPR) | 2 | 0.5 | 3 | 2 ✓ |
| Maiven (AC 15, 58 HP, 19.5 DPR) | 3 | 1 | 3 | 2–3 ✓ |
| Hired Knife (AC 15, 32 HP, 2 × 5.5 + 1d6) | 1 | 0.5 | 2 | 1 ✓ |
| Church Warden (AC 16, 33 HP, 2 × 5.5) | 1 | 0.5 | 1.5 | 1 ✓ |
| Phern Bodyguard (AC 15, 33 HP, 2 × 5.5) | 1 | 0.5 | 1 | ½–1 |
| Draunel Duelist (AC 15, 27 HP, 1 × 7.5 + Riposte) | 1 | ¼ | 1 | ½ |
| Cousin's Blade (AC 14, 22 HP, 1 × 6.5) | ½ | ⅛–¼ | ½ | ¼ |
| Border Slinger (AC 14, 19 HP, 1 × 5.5) | ½ | ¼ | ¼–½ | ¼ |
| The Hollow | 9 | 11 | 6 | 8.5 ✓ |
| The Radiant (Rite fixed) | 10 | 12 | 9 | 10.5 ✓ |
| The Wept (84 DPR with *She Arrives*) | 11 | 12 | 15 | ≈ 13 (cosmetic) |

Pattern: the weak retainers are over-rated, so the budget inflates. The two- and
three-attack leaders are rated at the top of their band, so they run hot against a
soft party. That is the 5.2.1 "undershoots multiattack NPCs" effect, and it shows up
cleanly in S2 and S13.

---

## Appendix C — Trying to break the Uninvited (3rd–5th level, SRD 5.2.1)

| Attempt | Result as written | Clean? |
|---|---|---|
| Kill it (5th-level party ≈ 45–60 DPR, halved by BPS resistance, vs 157–187 HP) | Leashed: back next turn at full HP; the last-blow dealer drops to 0 | Clean. Last-blow edge cases undefined (M9) |
| *Hold person*, *sleep*, *command*, *hideous laughter*, *calm emotions*, *suggestion* | Immune (Incapacitated/Paralyzed/Unconscious/Charmed/compelled) | Clean |
| *Banishment*, *plane shift*, a teleport it didn't choose | The leash pulls it back | Clean (and out of level) |
| Shove, *thunderwave* push | A nonmagical shove works (Radiant Dex +9 saves 85%); magical forced movement is "pulled back" | Clean |
| Grapple (Hollow/Wept) | Shadow-Step as a bonus action ends it | Clean |
| **Grapple or *web* on the Radiant while Witnessed** | It can't Shadow-Step; it must use its action to escape (Web DC 13 Str: 55%) | **Contradicts the table's row** (M2) |
| ***Blindness/deafness*** | Not immune. Disadvantage on attacks, no Shadow-Step (needs sight), no *She Arrives* | **Unaddressed** (M2) |
| ***Sanctuary*** on Raunu/Veier | DC 13 Wis per attack; loses ≈ 25% of attacks. "Compelled"? | **Unaddressed** |
| ***Invisibility*** on Veier | The Radiant has only darkvision | **Unaddressed** |
| *Darkness* / Dark-Burst | Blocks sight (no Shadow-Step inside), but ends Witnessed (full speed), and earns the Radiant's Fracture | Partly addressed; the speed-up isn't |
| *Slow* (5th) | No immunity: one attack, half speed, −2 AC | Unaddressed; buys time |
| ***Tiny hut*** (5th) | Force dome, opaque from outside; Shadow-Step can't see in. **Safe room to the last bell** | **Breaks canon** (M2) |
| *Counterspell*, *dispel magic* | Nothing to target | Clean |
| Readied actions, focus fire, "last blow" games | Nothing to gain; the dealer loses the night | Clean but punishing (M9) |
| Crystal charge at the Uninvited | DC 13 Cha within 30 ft; failure spends it | Clean. Running effects unclear (m11) |
| Ward-steering at Raunu's side | DC 10 (96% for Andra with Gift advantage), each success "costs the Wept a round", no limit | **Unbounded** (M3) |
| Trap one with ward-crystal | DC 18 (51% with advantage) or DC 13 from the Root (88%), holds to the last bell | Intended, but cheap with Gift advantage (M3) |
| Ranged chip damage from behind the Wept | She never targets non-blockers: free damage, Bloodied in ≈ 8 rounds | Degenerate but legal (M9) |

**The Fracture is clear and usable mid-combat.** It takes one action within 30 ft,
DC 18 with one tell or 15 with two. The "fail by ≤4 still lands" band makes it
reliable:
- Serane (+7) lands it 70% at one tell, 85% at two, and 91% / 98% with Heroic
  Inspiration.
- Dassa (+0) lands it 35% / 50%.
- Bardic Inspiration (added after a failure, 2024) and *guidance* both help, as
  they should.

Two blemishes: the undefined "MM makes a move", and the Radiant's speed-halving
stack (M9).

---

## Appendix D — Arithmetic spot-checks (all pass unless noted)

- **HP from hit dice:** all 24 blocks and the four Nastier variants are correct.
  For example, Wept 22d8 + 88 = 187; Captain 13d8 + 39 = 97; Maiven 9d8 + 18 = 58.
- **Attack bonus = PB + ability, and save DCs = 8 + PB + ability:** all correct.
  Honor Guard Seize 13; Warden 12; Duelist Provocation 12 (Cha); Kovaun 14 (Wis);
  Hollow 17 (Str); Rite 17; Tavva Furniture 13; Maiven disarm 13.
- **Budgets:** every card sum and Table IX–1 match SRD 5.2.1.
- **Pregens:**
  - Standard array plus background +2/+1: correct for all five.
  - HP: Serane 21, Pello 24, Andra 20, Dassa 28, Ilesse 21. All correct.
  - Skill counts: class + background + Skillful (+ Skilled / Lore bonus) all
    reconcile. Ilesse's Religion +3 is Thaumaturge (Wis mod), not proficiency.
  - Slots 4/2. Cantrips: bard 2, cleric 3 + 1 (Thaumaturge), wizard 3, each plus
    the gift cantrip. Prepared 6 each, plus the Life domain's 4.
  - Andra's lattice: 12 spells. Evoker Potent Cantrip is 3rd level in 2024.
  - Errors are m1–m3 only.
- **Items:** prices match the 2024 rarity values (consumables at half). No
  consumable is broken. The Dark-Burst is *darkness* without concentration, usable
  by anyone, which is fine at uncommon.
