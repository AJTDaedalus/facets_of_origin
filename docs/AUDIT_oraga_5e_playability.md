# Audit — Oraga Night 5e: Can You Prep It, Run It, and Will the Table Have Fun?

*2026-09-27. Read-only playability audit of `conversions/dnd5e/oraga_night/` (README,
01–11, INVENTIONS_5e.md, flow/) plus `docs/BRIEF_oraga_5e.md` and
`docs/REVIEW_oraga_5e.md`, on branch `feat/oraga-5e` (PR #33). Source compared:
`adventures/oraga_night/`. Method: a full prep simulation (one evening, first session
next day), then a mental run of the night with four typical 5e players: a murder-hobo,
a talker, a lore-seeker, and one who wants big fights. Nothing in the module was edited.*

---

## Executive Verdict

**Playable, and in places the best-built social adventure I have audited for a 5e
table. It is not yet ready for a 5e group on one evening of prep.** The core holds up:
seven Movements, visible and optional fights with real outs and clocks, a snakes layer
that does deliver "he invited the snakes into the chicken pen," a thoughtful answer to
the 5e spell list, and consistent encounter math (verified against SRD 5.2.1). A
patient MM who reads for a weekend will run a memorable night.

Three things will hurt game night if they are not fixed first:

1. **The midnight climax makes a 5e table feel cheated.** The Uninvited's *Leashed* /
   *Not Its Quarry* rules take any character they drop out of the scene, with no rule
   for when that character comes back (C1). The module says "force buys time" but
   gives the MM nothing to spend the time on: no dais clock, no hunt clock, and damage
   has no mechanical effect at all (C2). The player who came for big fights spends
   the best hour of the night rolling damage that only turns into narration, and then
   sits out.
2. **It is not one session.** 84k words, about 2.3 times the source's 37k, with the
   same "4–6 hours" claim. A realistic unabridged run is **6.5–8 hours** (C3).
3. **Prep and bookkeeping outrun one evening.** The advertised running order is about
   48k words (3+ hours of reading), and the "one page" night-tracker is six dense
   tables (M1). The MM also tracks six heat tracks, up to 13 clocks, and per-character
   Fracture tells.

After those come a timeline contradiction around the last bell (M2), a gate fight
that has no way to physically reach the enemy (M3), a canon ending that fails by
default if no player happens to be at the river gate (M4), and thin guidance for a
murder-hobo who draws in Movement I or goes for the host (M5).

**Counts:** 3 Critical · 10 Major · 12 Minor. A focused fix pass of about a day
(mostly C1–C3, M1–M5) makes it table-ready. Every recommendation below is a rules or
guidance change. None of them adds lore.

---

## Answers to the Eight Questions

### 1. Prep burden

- **Reading load.** The README running order asks for 01 and 02 in full (7.9k words),
  a skim of 04 and 05 (24.8k), then 09 (15.1k). That is about 48k words. The Overture
  also says to reread 07 (5.6k), and 05 says to read the Uninvited blocks in 10 before
  running. Total: about 56k words, **3.5–4 hours of reading** before any notes. One
  evening does not cover it.
- **Running order.** It exists (README) and is sensible. It never says what to skip on
  a first read, or what to have physically open at which Movement.
- **Night-tracker.** 08 calls it "One page. Run the ball from here." It is actually
  Tables VIII-2 through VIII-8 plus a crisis panel, about six printed pages. It is
  genuinely good: the Night Clock's "what the players can move" column, *Where
  Everyone Stands*, the Snake Tracker, *Costs to Hand*, and the crisis panel are all
  excellent. It does not suffice alone, though. It has no fight-card digest (enemy
  names, the outs, the top-of-scene sentence), no DC-ladder strip, no read-aloud
  triggers, and no real-time budget.
- **Where I got lost.** (a) When the last bell rings relative to the gate fight (M2).
  (b) What happens to a character the Wept drops (C1). (c) How the party physically
  engages the Bought through a gate barred from the far side (M3). (d) How many
  rounds Raunu has on the dais before he crushes the crystal. There is no number
  (C2). (e) Which of the five Movement V cards to run when the party is split (M6,
  M9). (f) Which pregen to drop at a table of four (m4). (g) No map, so the MM has to
  build the geography in their head (M8).

### 2. Structure under 5e pressure

- **Ignoring agendas.** Survives well. Scheduled events, omens and snake tells keep
  arriving whatever the players do ("the Undercurrents are the depth, not the floor").
- **Splitting up.** The module is designed to split the party: eight agendas in eight
  rooms, and one-on-one summonses. Chapter V handles the split with beats. Movements
  I–V have no spotlight-rotation or idle-player guidance (M9).
- **Starting fights early.** *The Palace on Alert* and S4 cover bare steel mechanically.
  What happens next is punishing: the offender is knocked out, "wakes after 1d4 hours"
  in the gatehouse cell, and the player is benched for most of the night. There is no
  guidance for a snake leader killed in Movement I (Callun is CR 1/4 with a trivial
  HP total) (M5).
- **Going straight for the host.** Raunu is behind S4 in the east wing all night, then
  alone with a summoned character in B4 (Movement III), then at the high table (IV).
  His *If It Comes to It* line says only "He will not fight a guest." There is no
  sidebar for a character who stabs Raunu at the summons or the toast, and no word on
  what the Uninvited do if the host is already dead (M5).
- **Refusing the hooks.** Every hook converges on B0/B1, and session zero is told to
  set expectations. That is adequate. It is a table-contract problem, not a module
  problem.

### 3. The snakes layer

- **Does it deliver?** Yes. The Movement-by-Movement boxes, the tells, the Movement IV
  escalation after the two plates, and *Knives in the Dark* make the host's enemies
  a tangible, readable pressure. Callun's knife leaning on Anha (S7) and Draunel's
  appointment (S9) are standout scenes. *Every fight is visible and optional* holds on
  every card I checked.
- **Frequency.** The fights are **back-loaded.** Movements I–IV offer one fight a
  big-fights player will want: S1, a nonlethal fist-brawl against CR 1/8 kinsmen. S6
  only triggers for whoever pressed Vorlain, and S7's first half is not a fight.
  Movement V then fires five cards at once (S2, S7, S8, S9, S10). The fight-seeker
  waits about three real hours and is then offered more than one evening can hold (M6).
- **Drowning the masquerade?** Not structurally: "show one or two" is repeated
  everywhere. The heat math does run hot by default, though. With **no player action**,
  midnight arrives with Church 3 (S8 dark), Phern 3 (S11) and Thenya 3 (S10 already
  fired in Movement V), plus S5 and S3, which always run. Most rises are automatic,
  so "heat rises when a line goes unanswered" is really a clock (M6).
- **Consequential?** Yes. Heat changes what happens at midnight and what comes to the
  inquest, and the ⟨A snake gets what it came for⟩ sidebar is a smart way to keep
  canon.

### 4. The unbeatable Uninvited

- **Telegraphing.** Good in the fiction (omens, tells, Corval's slipping memory). There
  is no player-facing line at session zero telling 5e players that some threats are
  won by people and time rather than hit points. The Overture tells the MM *not* to
  say how the night goes wrong. That is right for the plot, and wrong for the genre
  contract (folded into C2).
- **Is Leashed clear and fair?** Clear, and closed against the SRD spell list:
  Table *The table tries* in 10 is excellent. It is **not fair to the player.** Dealing
  the last blow gets *your* character dropped to 0 HP and removed from the scene (C1).
  Every other drop is also "out of the scene" with no return rule. The Fracture's
  "at a cost" result is an attack from a CR 9–11 creature (+10 to hit, 28 damage),
  which reliably drops a 3rd-level speaker (C1).
- **Things to do at midnight.** A rich list: steer wards (DC 10 at Raunu's side),
  Fractures, keep the Radiant *Witnessed*, carry guests, hold doors (S11), the snakes,
  the Crossing, and the gate. The *verbs* are there. What is missing is a **ledger**.
  "Time bought" has no clock to fill, so the players cannot see their purchase (C2).

### 5. Pacing

| Movement | Realistic real time (4 players, pregens) | Notes |
|---|---|---|
| Session zero (pregens, hooks, agendas) | 20–30 min | 60–90 min if characters are built fresh |
| I. Receiving Line | 30–45 min | B0 line, first check, Corval, the gate |
| II. Empty Rooms | 60–90 min | "The longest Movement"; S1 alone is 20–30 min |
| III. Summons | 40–60 min | 1–2 one-on-one summonses at 10–15 min each; S6 |
| IV. Toast | 25–40 min | Toast, dinner-for-two or east wing, S7 first half |
| V. Hour of Spirits | 45–75 min | Any one Movement V card is a 30–45 min 5e combat |
| VI. Unmasking | 60–90 min | Beats across split characters, dais, hunt, Crossing, S11/S5 |
| VII. Longest Night | 45–75 min | Rescue, S12/S13, S3 (30–45 min) |
| Epilogue | 10–15 min | |
| **Total** | **~5.5–8 h, typically 6.5–7.5 h** | The Abridged Run brings it to about 4.5–5.5 h with a strict MM |

**The claim of "one session (4–6 h)" holds only with the Abridged Run and a timebox.**
The midnight read-aloud, which breaks off at *"House Boranis has been silent
because—"*, is a perfect session break. Sell it as two sessions (C3).

### 6. Rewards, level-ups, pregens

- **Milestone to 4th at the epilogue** is fine for a mini-campaign, and harmless in a
  one-shot. The Aftermath's 5th-level-at-the-inquest beat is lovely.
- **Heroic Inspiration** is binary in 5e: you have it or you don't, and the surplus
  passes on. Every pregen starts with it (*Resourceful*). The module prints roughly
  20 award points: per omen, per room, per agenda, per Undercurrent, several per
  card, and "per person carried out." Most will evaporate. Omens "are how they afford
  to act before midnight," but Inspiration does not buy action (M7).
- **XP.** Table I-1 says "each character," and an out pays "the fight's full XP." If
  that means per character, voiding the S3 contract alone is worth 1,950 each, which
  overshoots 4th level (m2).
- **Pregens.** Mechanically verified in REVIEW. The mix is sound for this night: a
  talker bard, a Fracture-capable cleric, and a wizard carrying *darkness*, which
  denies the Radiant its congregation. There are five pregens for a four-player table
  and no guidance on whom to drop. Dropping Ilesse loses Agenda 4, which Chapter V
  "leans on" (m4).

### 7. Handouts, tools, flow

- **Handouts.** The invitation is fine, the rumor table is good (2d6 on purpose), and
  the agenda cards are evocative. The cards omit the *Pays* line and the parts of *the
  catch* the character already knows (m9).
- **Night-tracker.** See question 1 above and M1.
- **flow/.** `flow.json` is clean: 110 nodes and 194 edges, no dangling edges, no
  orphans, and the generated HTML is byte-identical to a fresh `build_flow_page.py`
  run. It matches 05 on the Crossing (Movement VI) and places the gate after the last
  bell. That **disagrees with the 08 Night Clock** (Crossing in Movement VII, the gate
  before the last bell), and neither version squares with the Bought's contract
  ending at the last bell (M2). As a prep visual it is very good. At the table it is
  too dense (no print view). S4 is linked only from B9, Undercurrent C and S10, not
  from the S1, S2, S7 and S8 outcomes that also end in guards. There is no node for
  early violence or a jailed character (m8).

### 8. Top 10 things that would go wrong on game night

1. **The fighter Action-Surges the Wept, is hit twice for 28, and is "thrown clear,
   out of the scene."** By the rules as written the character is unconscious at 0 HP,
   stable, for 1d4 hours. The player watches the Crossing and the gate from the couch
   (C1).
2. **The big-fights player realizes damage does nothing.** 187 HP, resistance to
   bludgeoning, piercing and slashing, and "you bought a round" is narration with no
   ledger. The player concludes the module cheated (C2).
3. **Hour five, and the table is in Movement IV.** The MM rushes midnight, so the
   payoff the whole night built toward lands flat, or never lands (C3).
4. **By Movement III the MM has stopped ticking heat.** Six factions, automatic rises,
   and 13 clocks are too much, so the snakes become background noise or the MM
   improvises the midnight cards (M1).
5. **The murder-hobo draws on Mistress Callun in the receiving line.** Four CR 2
   guards (AC 18) knock the character out, and the player sits out 1d4 hours. Callun,
   CR 1/4, may already be dead, and nothing says what the Circle's line does next (M5).
6. **Nobody took Agenda 4 or chased Undercurrent C.** No character is at the Crossing.
   By the rules as written the Radiant breaks past Vell, "nobody does anything," and
   ⟨The child is taken⟩ fires: the darkest non-canon branch, triggered by absence (M4).
7. **At the front gate a player asks, "It's barred from the far side. How do we even
   fight them?"** There is no breach mechanic. And if the MM already rang the last
   bell to end the Uninvited, the Bought's contract has expired and they should be
   leaving (M2, M3).
8. **Movement V, party split three ways.** S2, S8 and S9 all tick round-clocks at
   once. The MM either runs three initiatives in parallel or silently drops two of
   them, and the Snake Tracker then records "not stepped on" for lines the players
   never saw (M6).
9. **Four players, four agendas, four rooms.** During each 10–15 minute summons or
   east-wing scene, three players are idle, for three hours (M9).
10. **Inspiration handed out a dozen times to people who already have it.** The
    "printed rewards" feel like nothing, and players hoard the one they hold (M7).

*Honorable mention:* the table asks where the river gate is relative to the dais and
the east-wing stair, and there is no map (M8).

---

## Findings, Ranked

### Critical

#### C1 — Characters dropped by the Uninvited are removed from the climax with no return rule, and the last blow is punished

- **Location:** `10_Bestiary.md`: *The Hollow* (*Leashed*, *Not Its Quarry*), with the
  Wept and Radiant "as the Hollow"; *How to Read This Chapter* ("Not their quarry").
  `05_The_Longest_Night.md`: *You Cannot Beat Them*; *The Fractures*. `08_Handouts.md`:
  *Crisis Panel*.
- **Evidence:**
  - *Leashed*: "it instead removes whoever dealt the last blow — that creature drops to
    0 Hit Points and is out of the scene."
  - *Not Its Quarry*: "is Stable, is thrown up to 30 feet clear, and is out of the
    scene."
  - Nothing says when "out of the scene" ends. By 5e rules a stable creature at 0 HP
    regains 1 HP after 1d4 hours, and the detain rule in 10 says exactly that for the
    guards.
  - The Wept hits at +10 for 28 damage, twice (three times on the *Nastier* line). The
    Radiant makes three attacks at +9 for 16. Pregen HP runs 20–28.
  - A Fracture missed by 4 or less "answers first with one attack against the
    speaker."
  - Massive damage (remaining damage ≥ HP max means death) is not overridden
    explicitly, and a 28-damage hit on a wounded wizard can trigger it.
- **Why it matters at the table:** The module actively invites characters into the
  Uninvited's path: stand between the Wept and Raunu, be a body in the way at the river
  gate, invoke Fractures within 30 feet. Each of those one-shots a 3rd-level character
  and benches that player for the rest of the session: the Crossing, the snakes in the
  dark, the gate. The player who "wins" the damage race is the one knocked out. That is
  the textbook recipe for 5e players feeling cheated, and it lands in the best hour of
  the night.
- **Recommended fix:** Rewrite *Not Its Quarry* and *Leashed* together, and mirror the
  change in 05 and the 08 crisis panel:
  - *Not Its Quarry*: "…is thrown clear, Stable, and **regains 1 Hit Point and is back
    in the fight at the start of the next beat**, somewhere the MM chooses, with one
    level of Exhaustion if you want a cost. This overrides massive-damage death."
  - *Leashed*: replace "that creature drops to 0 Hit Points" with "that creature is
    pushed 15 feet and knocked Prone, **and the Uninvited loses its next turn**
    stepping into shadow." The last blow then *buys* something concrete.
  - Fracture "at a cost": make the parting blow hit automatically for a fixed moderate
    amount (for example 10), rather than a CR 11 attack roll.

#### C2 — "Force buys time" has no mechanical ledger; midnight has verbs but no clocks

- **Location:** `05_The_Longest_Night.md`: *How to Run the Attack* (principles 1–3),
  *The default beats* (the dais, the east wing), *You Cannot Beat Them* ("Time is the
  real currency"), ⟨They save Raunu⟩. `10_Bestiary.md`: the Wept (*When Bloodied*),
  the Radiant (*Witnessed*). `08_Handouts.md`: *Crisis Panel*. `flow/flow.json` (only
  `clk-leash`).
- **Evidence:**
  - The module uses four-segment clocks on every fight card, but the attack has none
    except the leash.
  - The dais: "Each success is a ward… and costs the Wept a round… Then the Wept is
    through the last barrier." There is no count of how many rounds or barriers Raunu
    has, so ⟨They save Raunu⟩ ("while Raunu still has his twin crystal") has no
    trigger the MM can read.
  - The hunt: "every player character who chases it… is buying Veier hallway after
    hallway." There is no hallway count.
  - Damage: 157–187 HP with resistance to bludgeoning, piercing and slashing. A 3rd-level
    party deals about 15–25 effective damage a round to one, so reaching the Wept's
    Bloodied (93) takes 4–6 rounds of the whole party, and 0 HP takes 8–12. The Wept's
    "DC 15 once Bloodied" Fracture is practically unreachable.
  - Damage has no other mechanical output. The MM Note tells the MM to *narrate*
    "You bought Raunu a round."
- **Why it matters at the table:** 5e players understand clocks and HP bars. Here they
  can see neither. The talker and the lore-seeker have Fractures, but the big-fights
  player's whole contribution becomes MM narration. "The Uninvited cannot be beaten"
  is a fine spine. "Nothing you roll changes a number" is what reads as cheating.
- **Recommended fix:**
  - Add three four-segment clocks to the 08 crisis panel and to 05:
    - **The Dais** (the Wept reaches Raunu). The Wept fills 1 per round. Each steered
      ward, each character who takes a Wept attack meant for Raunu, and each 20 damage
      dealt in a round **removes** 1.
    - **The Hunt** (the Radiant reaches Veier before the garden stair). It fills 1 per
      beat. A *Witnessed* round, a sealed door, or a successful chase check removes 1.
    - **The Doors** (the Hollow's herd). Guests out through the service passages or
      the Phern door remove segments.
  - Make "20 damage in a round" or "a hit of 10 or more" an explicit purchase, so
    damage matters without the monster ever dying.
  - Tie ⟨They save Raunu⟩ to "the Wept's Fracture lands while the Dais clock is not
    full."
  - Lower the Wept's "Bloodied" trigger for the Fracture to "has taken 50 damage
    tonight."
  - Add one session-zero line for the players: *"Some of what comes tonight is not won
    by hit points. It is won by time and by people. The game will always show you what
    your time bought."*

#### C3 — The one-session claim is not credible for a 5e table

- **Location:** `README.md` (Length); `01_Overture.md`: *What This Adventure Is*, *The
  Abridged Run*; `06_Aftermath.md`: *Advancement*.
- **Evidence:** The source is about 37k words and the 5e edition about 84k (2.3×), with
  the same "4–6 hours." The simulation in question 5 gives 5.5–8 h, typically 6.5–7.5.
  Movement II alone is "the longest Movement." A 5e combat of 4–6 creatures runs 30–45
  real minutes, and the book offers 4–7 of them. Nothing in the module gives
  per-Movement time targets.
- **Why it matters at the table:** A one-shot that runs out of time before midnight
  loses the entire payoff. MMs who fall behind rush Movements VI–VII, which are
  exactly the part the night exists for.
- **Recommended fix:**
  - Change README and 01 to: "**Two sessions of 3–4 hours** (break at midnight, on
    *'House Boranis has been silent because—'*), or **one long session (5–6 h) using
    The Abridged Run**."
  - Add a real-time budget column to Table VIII-2: I 30 · II 60 · III 40 · IV 30 · V
    45 · VI 60 · VII 45 minutes.
  - Add an "if you are behind at the top of Movement IV, skip to the Dead Dance" rule.
  - In the Abridged Run, keep the east-wing scene when a character carries Agenda 4
    (see m4).

### Major

#### M1 — Prep load and bookkeeping exceed one evening; the "one page" tracker is about six pages

- **Location:** `README.md` (*Running Order*); `08_Handouts.md` (Handout 4, Tables
  VIII-2 to VIII-8 and the crisis panel); `09_The_Snakes.md` (Table IX-2);
  `01_Overture.md` ("know the cast… reread Chapter VII").
- **Evidence:** The running order adds up to about 48k words, and about 56k with 07 and
  10's Uninvited section. Handout 4 says "One page" and spans six tables plus a panel.
  Live state to track: 6 heat tracks (several with automatic rises), up to 13 fight
  clocks, Fracture tells per character per Uninvited, agenda status, Undercurrent
  status, and Inspiration.
- **Why it matters at the table:** An MM with one evening will skim 04, 05 and 09. The
  first thing to decay under load is the heat bookkeeping, which is exactly what
  decides which snake cards go live at midnight.
- **Recommended fix:**
  - Add a **true one-page MM Sheet** at the front of 08. One row per Movement: time
    budget, the scheduled beat, the omen, the one snake to show by default, and the
    fight card(s) available with their one-line outs. Add a strip with the DC ladder
    and *success at a cost*.
  - Add a **"First-read path" (about 20k words)** to README: 01 *Checks* through *What
    the Night Pays*; 02 *The Truth of the Night*; 04 *The Program of the Night* only;
    05 *How to Run the Attack*, *The default beats*, *You Cannot Beat Them*; 09
    *Running the Snakes* plus the cards you plan to show.
  - Pre-compute the default heat outcome ("with no player action, midnight has S8, S11
    and S5 live; S10 fired in V") so the MM only tracks *deviations*.

#### M2 — Timeline contradiction: the last bell, the Bought's contract, the Crossing and the gate

- **Location:**
  - `05_The_Longest_Night.md`: principle 3 ("the last bell… takes them"), *The Crossing*
    beat 3 ("Then the bell"), Movement VII ("The Uninvited are gone… one long hour
    before the sect guards"), B12 (contract term "to the last bell of Oraga").
  - `08_Handouts.md` Table VIII-3 ("The Crossing (Mv VII)"; gate before "Last bell…
    contract expires").
  - `09_The_Snakes.md`: *Not Snakes* ("to the last bell of Oraga"); S3 ("On the
    clock's last segment… sect guard"), which gives a 4-round fight.
  - `07_Cast_of_the_Ball.md`: *The Bought*.
  - `flow/flow.json`: the edge `ev-bell → sc-rescue → ev-word → b12 → S3`.
- **Evidence:** 05 and the flow ring the last bell (the Uninvited leave) *before*
  Movement VII and the gate. The Bought's contract runs only "to the last bell of
  Oraga," and 08 says that at the last bell "the contract expires; the company
  withdraws." 08 also places the Crossing in Movement VII, while 05 and the flow place
  it in VI. Movement VII promises "one long hour" before the sect guard, but S3's
  clock brings them in 4 rounds.
- **Why it matters at the table:** The MM is told to "ring the bell when the table needs
  the end." Doing so, by the rules as written, dissolves the gate fight the Abridged
  Run calls "the only fight the ending needs." Players who listen to the contract terms
  will catch the contradiction on the spot.
- **Recommended fix:**
  - Distinguish two bells. **The leash bell** (the Oraga bell, which takes the
    Uninvited) and **the dawn bell** (the Bought's term: "from the first bell of
    midnight until dawn").
  - Put the Crossing in Movement VI everywhere (fix Table VIII-3).
  - Replace "one long hour" with "until the sect guard breaks through (S3's clock)".

#### M3 — S3 gives no way to physically engage an enemy behind a gate barred from the far side

- **Location:** `09_The_Snakes.md` S3 (trigger, *Terrain as rules*, *Outs*);
  `05_The_Longest_Night.md` B12.
- **Evidence:** The gate is "shut… from the far side. Through the grille: matched grey
  coats." Terrain gives three-quarters cover through the grille, and a gatehouse stair
  whose position is ambiguous. The objective is "open the way out," but there are no
  rules for the bar, the gate (AC/HP, a Strength DC, a lever in the gatehouse), a
  wicket door, or who stands on which side. "Fight through" assumes melee contact the
  terrain doesn't provide.
- **Why it matters at the table:** This is the climactic fight for the big-fights player,
  and the first question the table asks will be "how do we get at them?"
- **Recommended fix:** One paragraph in S3. For example: "The gatehouse has a wicket
  door and a winch room reached by the gatehouse stair; four Blades and the sergeant
  hold the winch room *on the palace side*, and the bar is outside. Taking the winch
  room (or forcing the wicket, DC 18 Strength) is how a party fights through; the
  grille is for talking." Mirror it in 05 B12 and the flow's `gate-fight` summary.

#### M4 — The canon default fails if no character happens to be at the river gate

- **Location:** `05_The_Longest_Night.md`: *The Crossing*, beat 3 ("If the Radiant
  breaks past Vell — and it does, exactly once… If nobody does anything at all, see ⟨The
  child is taken⟩"); ⟨The child is taken⟩ ("because nobody stood at the gate").
- **Evidence:** The recorded outcome (Veier and the child out on Vell's arm) requires a
  character action at the gate. Nothing in the text says what happens if *no character
  is there at all* — the fighters at the front gate, the talker on the dais, the rogue
  looting B7. That is a very plausible table if nobody took Agenda 4 or Undercurrent C.
- **Why it matters at the table:** The module promises that history "bends toward the
  recorded outcome through play." Here it bends *away* from canon because of absence,
  into the darkest branch. A table that never met Veier gets a tragedy it had no part
  in.
- **Recommended fix:** Add to beat 3: "*If no player character is at the Crossing at
  all, run it offstage as history records it: Vell holds, the boat clears, and the
  table sees only the pale man rowing into the dark from wherever they stand. ⟨The
  child is taken⟩ is for a table that was there and chose otherwise.*"

#### M5 — Early violence and attacks on the host: the offender is benched, and there is no downstream guidance

- **Location:** `04_The_Ball.md`: *The Palace on Alert*; `09_The_Snakes.md`: S4;
  `10_Bestiary.md`: *Boranis Honor Guard* (*Detain and Expel*), *How to Read* ("wakes
  after 1d4 hours"), *If It Comes to It* (Raunu); `05_The_Longest_Night.md`: ⟨If History
  Breaks⟩.
- **Evidence:**
  - The offender "spends the next hour in the gatehouse cell." A guard's knockout wakes
    them "after 1d4 hours… without its mask or its invitation."
  - There is no rule for a snake *leader* killed before midnight (Callun CR 1/4,
    Corro CR 1/8). A 3rd-level party kills either in one round.
  - Raunu is alone at the far end of B4 with a summoned character, and at the high
    table during the toast. His block says only "He will not fight a guest." There is
    no ⟨A player character kills Raunu early⟩ sidebar, and nothing on what the Wept
    does then.
- **Why it matters at the table:** The murder-hobo test is exactly the Movement I draw.
  As written, it removes a player from the game for hours and leaves the MM improvising
  the consequences for the snake lines and the canon.
- **Recommended fix:**
  - (a) Make the cell a scene, not a sentence. "A detained character wakes at the start
    of the next Movement in the gatehouse cell; someone comes (Essin, Sella, Tavva
    posing as staff, or their patron) and the price of release is a favor. The player
    is never out longer than one Movement."
  - (b) Add a short sidebar: "*A snake's leader falls early*". The retinue withdraws
    with the body. That faction's heat goes to 4 with the party named as the target.
    The inquest has its scapegoat.
  - (c) Add ⟨They kill Raunu before midnight⟩. The Uninvited go straight for Veier at
    the bells, the Wept joins the hunt, and the pillars shift: no one is charged
    becomes someone is, the party. Also have Raunu's block say what his wards do when
    attacked: seal the attacker in, or flare, so the attack visibly fails without a
    fight.

#### M6 — The fights are back-loaded, Movement V collides, and the default heat runs hot

- **Location:** `04_The_Ball.md` (*The Snakes This Movement* I–V; *Trouble You Can Walk
  Into*); `09_The_Snakes.md` (Table IX-3; Table IX-2 rises); `08_Handouts.md` (Table
  VIII-6).
- **Evidence:**
  - Before Movement V the only generally available fight is S1, a nonlethal brawl with
    fists and improvised weapons (1d4) against six CR 1/8 kinsmen. S6 needs a
    character to have pressed Vorlain, and S7's first half "is not a fight."
  - Movement V then offers S2, S7 (second half), S8, S9 and S10 in the same hour, each
    with a per-round clock.
  - Default heat with no party action ends at Church 3, Phern 3 and Thenya 3.
- **Why it matters at the table:** The big-fights player waits about three real hours,
  then faces an overflowing Movement the MM cannot run in parallel. The rest of the
  table loses Movement V's slow-dance atmosphere to three initiatives.
- **Recommended fix:**
  - Move one real fight earlier. Candidates: make S6 generally available as "Essin's
    cousins warn off whoever is working Vorlain or the east corridor," or promote the
    Tavva scout in Movement III to an optional short scrap (Tavva plus one knife, the
    noise clock).
  - In Movement V, print a **priority rule**: "Run at most one Movement V card per
    split group; the others resolve by their *If nobody stops it* default, and heat
    does not rise for a line the table never saw."
  - Change the automatic Church rise "S8 not stepped on by midnight" to apply only if
    S8's tell was shown.

#### M7 — The Heroic Inspiration economy does not survive the conversion from Sparks

- **Location:** `01_Overture.md` (*Checks, Inspiration…*, Table I-1, *The omens*);
  every "Heroic Inspiration printed" line in `09_The_Snakes.md` (13 mentions);
  `05_The_Longest_Night.md` (*Carrying somebody out*); `11_Pregenerated_Characters.md`
  (all pregens start with it).
- **Evidence:** 5e Heroic Inspiration is binary, and the surplus passes to someone who
  lacks it. The source's Sparks accumulated. The module prints roughly 20 award points
  (per omen, per room, per agenda, per Undercurrent, several per card, per person
  carried out). "A party that catches all five [omens]… the Inspiration is how they
  afford to [act before midnight]." Inspiration does not buy actions.
- **Why it matters at the table:** After the first hour everyone holds Inspiration, so
  every printed reward is a no-op. The module's "pay clever play on the page" promise
  quietly breaks, and players hoard instead of spending.
- **Recommended fix:** Pick one of these:
  - **(a)** A shared **Omen pool** of d6 tokens (cap 5), spendable by anyone to add a
    d6 to a check or to invoke a Fracture at one step lower DC. This keeps the Sparks
    design.
  - **(b)** Keep Heroic Inspiration, cut the triggers to five (agenda, Undercurrent,
    ending a card by an out, a Fracture landing, the omen read aloud), and add "if the
    whole table already has it, the MM lowers the next Fracture DC by 2 instead."
  - Either way, drop "per person carried out," which pays at the end of the session.

#### M8 — There is no map

- **Location:** The module as a whole. `04_The_Ball.md` B13 ("It is on the plan, it is
  reachable from B7 and from the service run"); B5 ("know this geography cold — Court →
  terraces → lower garden → river gate").
- **Evidence:** No palace plan, flowchart or even a node diagram of B0–B13 anywhere. The
  flow graph is narrative, not spatial.
- **Why it matters at the table:** 5e fights are terrain fights, and the Crossing is
  "three beats down the garden's three levels." The service passages are "the other way
  through everything." Players ask "where is X from here?" constantly at a masquerade.
- **Recommended fix:** A one-page schematic (boxes and lines are enough) in 08. Show
  B0–B13; the service passages as a dashed overlay; the east-wing private stair to the
  garden stair; the three garden terraces; the river gate; the gatehouse with the winch
  room (see M3). It can be generated as a small SVG alongside the flow page.

#### M9 — No spotlight guidance for a scattered party in Movements I–V

- **Location:** `04_The_Ball.md` (*Running the Room*; Movement III *Summons*);
  `03_Masks_and_Agendas.md` (*The Agenda System*).
- **Evidence:** Eight agendas route characters to different rooms (B4 one-on-one,
  B9 behind guards, B10, B7, B8). A summons is a solo walk. Chapter V has beats, but
  Movements I–V have no rotation rule, no scene-length target, and no idle-player
  tools.
- **Why it matters at the table:** Four 5e players who normally move as a group will sit
  idle for three quarters of three hours. The talker gets the summons, and the fighter
  checks their phone.
- **Recommended fix:** Add *Running a Scattered Party* to 04 *Running the Room*:
  - Cut every 5–10 minutes.
  - Never leave a player unaddressed for two cuts.
  - Deal agendas in pairs (the text already allows two players to share one) so no one
    is ever alone.
  - Let idle players voice gossiping guests or the rumor table.
  - Summon two characters together once.

#### M10 — "Palace on Alert" and S4 disagree on the guards' response

*(REVIEW open Q3, still open, and it matters because it sets how lethal an early draw
is.)*

- **Location:** `04_The_Ball.md` *The Palace on Alert* ("four Boranis Honor Guards
  converge within 2 rounds"); `09_The_Snakes.md` S4 ("Two… Call the House brings four
  more… second round after the first guard is Bloodied"); `10_Bestiary.md` *Call the
  House*.
- **Evidence:** Two different numbers and triggers for the same response. Each guard is
  CR 2, AC 18, 52 HP, so four is 1,800 XP (over High) and six is 2,700.
- **Why it matters at the table:** It is the first fight a murder-hobo will trigger, and
  the MM will read the wrong one.
- **Recommended fix:** Use S4's version everywhere. In *The Palace on Alert*, write "two
  guards at once; four more per *Call the House* (S4)."

### Minor

#### m1 — The DC ladder contradicts itself on masks

- **Location:** `01_Overture.md`: ladder ("13 behind a mask") vs *Troubleshooting* ("a
  masked approach is Easy… DC 10"). `03`/`04`: "far above your station: DC 10."
- **Why it matters:** MMs will split the difference differently every scene.
- **Fix:** In Troubleshooting, write "approaching someone *far above your station*
  behind a mask is DC 10."

#### m2 — XP for outs is ambiguous

- **Location:** `01_Overture.md` Table I-1 ("XP, each character… The fight's full XP");
  `09` *Running the Snakes* ("Ending a fight by an out pays its full XP").
- **Evidence:** If an out pays per character, voiding S3 alone is 1,950 each, and a
  night can exceed 5,000 XP.
- **Fix:** "Full XP *for the party*, split as usual."

#### m3 — Death and stability edge cases are unstated

- **Location:** `09_The_Snakes.md` *Death before midnight* ("Stable when the scene ends")
  and `10_Bestiary.md` *Not Its Quarry*.
- **Evidence:** It is unclear whether death saves are rolled mid-scene before midnight,
  and whether massive damage is overridden.
- **Fix:** "Before midnight, a character at 0 HP in a snake fight is Stable at once."
  Also add the massive-damage override from C1.

#### m4 — Five pregens for four players, and the Abridged Run cuts Agenda 4

- **Location:** `11_Pregenerated_Characters.md` intro; `01_Overture.md` *The Abridged
  Run* ("Cut… the east-wing scene"); `03_Masks_and_Agendas.md` Agenda 4 ("Chapter V
  leans on it").
- **Why it matters:** Dropping Ilesse, or running the abridgement, removes the only
  built-in route to Veier and the Crossing, which feeds M4.
- **Fix:**
  - "At four players, drop Andra or Pello, never Ilesse, unless another player takes
    Agenda 4."
  - Abridged Run: "cut the east-wing scene only if nobody carries Agenda 4."

#### m5 — The tracker disagrees with the text on Essin

- **Location:** `08_Handouts.md` Table VIII-4 (Essin "with Vorlain" in every
  Movement) vs `04_The_Ball.md` Movement V ("Essin, alone, which he never is") and S9.
- **Fix:** Movement V cell: "B5 edge, alone — the S9 appointment."

#### m6 — "After the bells" vs Movement V for the appointment

- **Location:** `04_The_Ball.md` Movement IV Draunel ("*after the bells, on the
  terraces*"); S9 is set in Movement V.
- **Evidence:** "After the bells" reads as "after midnight" to players.
- **Fix:** "At the first quarter-bell."

#### m7 — Stale or inconsistent references

- **Location:** `07_Cast_of_the_Ball.md` Otta Vesh ("her workshop is Night One's best
  scene": the prelude was cut); `04` "fourteen of them named" vs `07` "Fifteen named
  guests"; `04` B13 "on the plan" (see M8); REVIEW open Q1 and Q2 (the testament's
  witnesses; Corval's gate line "there used to be sixty of you" vs Undercurrent B's
  "eighty").
- **Why it matters:** The sixty/eighty line is spoken aloud in Movement I, and a
  lore-seeker will catch it.
- **Fix:** Resolve the owner questions. Drop "Night One." Align the count.

#### m8 — Flow viewer gaps

- **Location:** `flow/flow.json`, `flow_page.template.html`.
- **Evidence:**
  - S4 is linked only from `b9`, `uc-c` and `S10`, not from S1/S2 clock-full, S7/S8
    "reaches the door," or bare steel generally.
  - No node for the jailed character or for early violence.
  - The phase of the Crossing disagrees with Table VIII-3 (M2).
  - No print or static view for the table; 110 nodes is prep-only density.
- **Fix:** Add the edges and a `sc-cell` node. After M2 is fixed, align the phase. Add
  a print stylesheet that lists nodes by phase.

#### m9 — Agenda cards omit what the character would know

- **Location:** `08_Handouts.md` Handout 2 vs `03_Masks_and_Agendas.md`.
- **Evidence:** The cards drop *Pays*, which is the player's motivation, and the known
  parts of *the catch*, such as "Corval is incorruptible by money" and "she never comes
  down."
- **Fix:** Add a one-line *Pays* to each card, plus the character-known catch.

#### m10 — 41 unapproved inventions, and one is load-bearing for the fights

- **Location:** `INVENTIONS_5e.md` (*Review These First*, #1).
- **Evidence:** "If struck, the snakes shrink to their leaders… and most snake fights
  move to Mv VII."
- **Fix:** The owner should rule on #1, #9, #11, #13 and #17 before game night.
  Everything else can wait.

#### m11 — "The Palace on Alert" says spells count as steel, but no card applies it

- **Location:** `04_The_Ball.md` sidebar *Steel at the ball* ("A spell with a visible
  effect cast at a guest is brandishing") vs S1/S6/S9 terrain and outs, which mention
  only drawn blades.
- **Evidence:** The Evoker pregen carries *sleep* and *darkness*, and the bard carries
  *hideous laughter*.
- **Fix:** In S1, S6 and S9 add "a visible spell at a guest counts as bare steel."

#### m12 — The Crossing's carry rule is garbled

- **Location:** `05_The_Longest_Night.md` *The Crossing*, beat 2: "a character helping
  her — or carrying her, with the Help action or a Strength of 13 or better — moves at
  half speed but moves her at theirs."
- **Evidence:** The sentence cannot be parsed into a rule.
- **Fix:** "A character can carry Veier (Strength 13+) or support her (the Help
  action). Either way the pair moves at half the helper's Speed, which is still faster
  than her 15 feet."

---

## What Is Already Excellent

*So the fix pass does not break these:*

- Every fight card has a visible trigger, a clock that is not a body count, two or more
  outs, a morale line, and a scaling line. The encounter math is right, and the
  "honest note" on each card is exactly what a 5e MM needs.
- Table *The table tries* in 10 closes the SRD spell list against the Uninvited in the
  fiction instead of by veto.
- ⟨A snake gets what it came for⟩ and ⟨The party turns one snake on another⟩ are
  clean ways to let the snakes matter without breaking canon.
- The Bought's negotiation surfaces and the *void the contract* out.
- *Costs to Hand*, the Night Clock's "what the players can move" column, and the rumor
  table.
- The pregens are mechanically correct and suit this night: the bard is the Fracture
  engine, *darkness* denies the Radiant its congregation, and Dassa counts the guards.
