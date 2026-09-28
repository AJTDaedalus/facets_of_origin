# FIXPLAN — Oraga Night 5e, pass 2

*Brain output, 2026-09-28. Resolves `docs/AUDIT_oraga_5e.md` with the owner's rulings
(2026-09-28). Every fixer conforms to the names and rules below exactly.*

## Owner rulings (2026-09-28)

| # | Ruling |
|---|---|
| R1 | **One session, the night itself.** The party starts **in the street, approaching the palace** (B0). Everything before that — session-zero hooks prose, prelude/"story so far" set-up played at the table, the aftermath wing — is cut or reduced to MM background. Target runtime **4½–5 hours** at a 4-player table. |
| R2 | **Four players is the design baseline.** Every fight is balanced for four 3rd-level PCs. Scaling lines are secondary ("three PCs: …", "five PCs: …", "4th level: …"). |
| R3 | **Knocked-out characters come back; the crowd and the party help.** See §1. |
| R4 | **Against the Uninvited, creativity beats direct force.** See §2. |
| R5 | **The gate fight gets a battlefield.** See §3. |
| R6 | **The heir stays secret.** No faction, NPC or clock learns of the pregnancy or the child unless a player character discovers it first and tells them. (Audit A-4; source canon: only players who reach the east wing may ever know.) |
| R7 | Remove the pre-scrub inventions text from branch history (Brain will squash-rewrite `feat/oraga-5e` after the fixes land). |

## §1 Down, Not Out (replaces "out of the scene")

Printed once in 05 (Movement VI rules) and referenced from 10's Uninvited blocks, 09, 08.

- **Not the quarry.** When an Uninvited reduces a creature other than its quarry
  (Raunu, Veier) to 0 HP, the creature falls **unconscious and Stable** — no death
  saves. The Uninvited are not here for you; they are moving you out of the way.
- **Help them up.** Any creature within 5 feet can take an action to rouse a Stable
  creature: it regains **1 HP** and may stand. No check. A healing spell or potion does
  the same and more, as normal.
- **The crowd.** The palace is full of people. If a Stable character is still down at
  the **end of the next round** and no one has helped, a guest or servant drags them
  clear and rouses them (1 HP) at the start of the round after. The MM names who —
  that person is now owed something. Nobody is benched longer than two rounds.
- **The party pays for each other.** The first time in the night a character hauls an
  ally up at midnight, that character gains **Heroic Inspiration**.
- **Leashed's throw** (the "last blow" rule): the striker makes a **DC 15 Strength or
  Dexterity saving throw** (their choice) at the start of the Uninvited's next turn,
  not on the spot; on a failure they are pushed 15 feet and knocked prone. No damage.
- Snake fights, the gate and everything not involving an Uninvited use the normal
  5e dying rules — **but** the crowd rule applies anywhere in the palace after midnight.

## §2 Buying Time (replaces "force buys time")

The Uninvited cannot be killed. They can be **delayed**, and delay is what saves people.

- Each Uninvited has a **Delay** count, starting at 0. Show it to the players (a die on
  the table). Each point of Delay = the Uninvited **loses its next turn's movement
  toward its errand** (it spends the turn recovering, choosing a route, or dealing with
  the problem you made). The MM spends Delay at the Uninvited's turn, one point per turn.
- **Earn Delay by being clever, not by hitting harder.** A creative action that uses
  the room, the crowd, the wards, a lie, a mask, a door, fire, water or light earns
  **1 Delay** on a success (DC 13; DC 15 if it repeats a trick that already worked on
  that Uninvited tonight; the same trick never works a third time). A **Fracture**
  earns **2 Delay** plus its printed effect. Examples printed as a d8 menu of room
  tricks per Movement VI/VII location (chandeliers, ward-doors, the crystal wall
  seams, the river terrace, the service lifts, the fountain, the kitchen fires, the
  panicking crowd).
- **Damage** counts only in lumps: if the party deals **30 or more damage to one
  Uninvited in a single round**, it gains **1 Delay** (at most 1 per round). Damage
  never reduces Delay and never threatens death (Leashed).
- **What Delay buys** is printed: each point spent while the party is evacuating a room
  saves that room's people; Delay on the Hollow keeps a door shut one beat; Delay on
  the Radiant widens the river-gate margin (canon: the margin is made of its slowness);
  Delay on the Wept buys Veier's steps. Rescues pay Inspiration/XP as already printed.
- History still bends by default: Delay changes *how many* are saved and *who* reaches
  the river gate, not whether the Uninvited can be beaten. ⟨If History Breaks⟩ sidebars
  say what happens when a table stacks enough Delay to change an outcome.
- Bloodied is no longer a Fracture gate. Replace "the Wept's Fracture drops to DC 15
  when Bloodied" with "**when she has 2 or more Delay**".
- **The Rite** is added to the Radiant's Multiattack options so it can fire.
- The "the table tries…" spell table in 10 adds: *tiny hut* (the Hollow's door rule —
  it opens what it is set against; the hut buys 1 Delay, once), *web*/grapple on a
  Witnessed Radiant (works: 1 Delay), *blindness/deafness*, *sanctuary*, *invisibility*
  on Veier (works once: 2 Delay on the Wept), *slow* (1 Delay, no stacking with the
  Radiant's guilt), ward-steering (1 use per ward per night, 1 Delay).

## §3 The Gate (S3)

- The gatehouse has a **wicket** (a person-sized door in the gate) and a **stair to the
  gate-walk**. Getting through: DC 15 Strength (Athletics) to force the wicket bar, DC 13
  Dexterity (Thieves' Tools), a key from a Bought (on a dropped Blade), climbing the
  gate-walk (DC 13 Athletics), or it opens on a parley — the Sergeant will speak through
  the wicket grille.
- **Morale: "or".** The Blades quit when the Sergeant falls **or** half of them are down.
  Ending 1 text changes to match.
- The **fire clock advances only on rounds when the party is neither fighting nor
  negotiating** — standing still is the worst play, not the best.
- The **last bell** (end of the Bought's contract) rings **after** the gate is decided,
  not before. Fix the ordering in 05, 08 and flow.json.
- Outs stay: void the contract (DC 13 to the sergeant; proof → no check to the captain),
  buy them out, outlast them to the last bell.

## §4 Other fixes (all from AUDIT_oraga_5e.md)

- Timing: the Crossing is in Movement VI everywhere; the Draunel appointment is "at the
  first quarter-bell" (before midnight).
- Canon default ending: Vell's escape succeeds by default unless the players actively
  interfere; ⟨The child is taken⟩ fires only if a player choice causes it.
- Crowds: a short "Two Hundred People" rule block in 05 — area spells in a crowd hit
  guests (say how many), the crowd rule, other retinues at the gate.
- Fights spread through the night: move one snake card into Movement II–III; lower
  default heat so no more than two factions are hot at midnight by default.
- S9: Provocation cannot fill the clock on its own before the party's first turn.
- S13: retune to Moderate for four; the fire never kills a downed character (they are
  dragged — §1 crowd rule).
- Pregens: raise the soft ACs where the class allows (shield, armor choice); re-check.
- Inspiration: Heroic Inspiration stays binary (5e rule); the printed awards become a
  shorter list, and a character who already has Inspiration may **give** a new award
  to another player instead.
- A-2 pronouns: the Uninvited are people — use the source's pronouns (the Wept *she*;
  the Radiant and the Hollow as the source has them), never "it".
- A-3: stop calling Tavva's S5 "the one winnable fight"; it is "the fight aimed at the
  noble-minded". The Bought are "the one foe at the gate who can be beaten or bought".
- Log the seven unlogged inventions (audit A-list) in INVENTIONS_5e.md.
- Licence: SRD attribution on 11 and the flow page; add a "Changes from the SRD" note in
  README (CC BY 4.0 asks for an indication of changes); no "D&D" in titles/headers —
  use "fifth edition" / "compatible with fifth-edition rules (SRD 5.2.1)".
- Reference books at `/mnt/e/books/DandD 5E/` (owner-provided, 2014 PHB/MM/SRD 5.1 etc.)
  may be consulted to check rules; **never** copy text or non-SRD mechanics into the repo.

## File ownership for pass 2

| Fixer | Files | Scope |
|---|---|---|
| **Midnight** | `05_The_Longest_Night.md`, `10_Bestiary.md` | §1, §2, crowds, timing in 05, Uninvited blocks/spell table, A-2 pronouns in 10, The Rite, items (Grow a Charge money-printer, ward-steering limits) |
| **Steel** | `09_The_Snakes.md`, `11_Pregenerated_Characters.md`, `INVENTIONS_5e.md` | §3 gate, R2 scaling on every card, S9, S13, back-loading/heat defaults, R6 heir, A-3, pregens, unlogged inventions |
| **Night** | `README.md`, `01`–`04`, `06`–`08`, `flow/` | R1 one-session restructure (street start, cuts, runtime table, one-page MM sheet in 08, map-substitute: a keyed room diagram), Inspiration list, A-3 wording, licence housekeeping, then cross-file sync of every §1–§4 name, and rebuild the flow page |

## §5 The Attendant (a Namak-Zai) — owner canon addition (2026-09-28)

Owner: a sealed servant of the Uninvited's master came through with them — "highly
intelligent constructs lacking all human emotion/motivation. They do what is asked of
them mostly, but can easily get distracted or lose interest. They have powerful magic,
but rarely feel the need to do it... it would make sense for the seal on this night to be
weak enough for one to come with them. They could use it to deal with any direct combat
threats, and protecting them/removing distractions should be narrowly scoped enough of a
task it could handle it while being something the party may be able to handle, especially
since they're rusty having spent hundreds of years doing nothing."

**Naming rule (hard, revised again 2026-09-28):** the module calls it **the Attendant**
(its epithet, like the Hollow or the Bought). MM-only text states once, plainly, that it is
**a Namak-Zai** (owner canon; owner: "the name likely won't be used in game"). Players
never hear the kind-name unless the MM chooses. Never write the Uninvited's true names,
the master's name, the name of the people the Namak-Zai were modelled on, or how/where
it was made. (Private canon stays private — never read or cite
/root/facets_of_origin/references/.)

**Before midnight — the quiet guest (owner, 2026-09-28):** "a quiet guest that looks like a
noble's attendant, but the noble they attend to is nowhere to be found. They could be there
to spy ahead of midnight, without being very effective." It arrives with the guests in
Movement I–II dressed as a great house's attendant, carrying a cloak and a cup for a master
who never appears. It is sent to watch ahead of midnight, and it is bad at it: it loses
interest mid-task, watches the wrong people, stares at the crystal walls, answers questions
literally and truthfully about trivia. It is a **visible oddity the players can notice and
pursue** (an omen-grade detail: reading it before it is explained pays like an omen). It
will not fight before midnight — its order is to watch; confronted or attacked, it simply
walks into a shadow and is gone until the Unmasking (drawing steel on it is still drawing
steel at the ball). Asked whom it serves, it names no one and looks, briefly, for the
master it is supposed to have. At the Unmasking it stops pretending and takes up its real
order.

**Role:** has been at the ball all night as the quiet guest above; at the Unmasking it drops the pretence and takes position by the Uninvited. It has one narrow order: **keep the three from being interrupted.**
It is the climax's fightable, beatable, outwittable threat: the answer to the player who
wants a big fight at midnight. It is **not** Leashed and it can be driven off.

**Mechanics (Midnight fixer writes the block in 10; exact names):**
- Stat block ~**CR 5** (High for four 3rd-level PCs), humanoid-shaped construct, no
  emotions (immune to charmed and frightened), intelligent, speaks only when asked, and
  answers literally.
- **Literal Orders.** It acts only against a creature that attacked, hindered or
  interfered with an Uninvited since the Attendant's last turn. Everyone else is
  furniture. A creature that stops interfering stops being its business.
- **Rusty.** Centuries idle. For its first 2 rounds in any scene it has disadvantage on
  attack rolls and cannot use its magic.
- **Loses Interest.** A creative distraction (DC 13 check fitting the trick: a question it
  must answer, a puzzle, music, a crystal display, a lie about its orders) makes it
  **Distracted** until the end of its next turn (it does nothing). The third time it is
  distracted in a night, it **wanders off** — out of the fight, standing at a window
  watching the fires. That is a win. *(Superseded: §5b — the fourth broken focus.)*
- **Rarely Bothers.** One powerful spell-like action (Recharge 6), usable only once it is
  Bloodied or has been distracted twice — the magic is real, it just rarely cares.
- **Clears the Way.** Once per round, if it is neither Distracted nor engaged in melee,
  it removes **1 Delay** from one Uninvited (§2): it moves the obstacle. This is why
  dealing with the Attendant matters to Buying Time.
- Creatures it drops are **Stable** (§1 applies: it removes interruptions; it does not
  hunt).
- At 0 HP it does not die on the floor: it **loses interest in being here** and steps
  back into the shadow. No body, no evidence (same logic as the Uninvited's masks).

**Fight card (Steel fixer, 09):** **S14 — The Attendant** (Movements VI–VII, wherever the
party interferes with an Uninvited). Visible (it arrives where everyone sees it) and
optional (it ignores anyone who is not interfering). Objective: get it out of the way —
drive it off, distract it three times, or talk its orders into irrelevance. Clock and
outs per the house card format; four 3rd-level PCs; scaling lines per R2.

**Night fixer:** a cast entry for the Attendant in 07 (MM-only line: it is a Namak-Zai);
its sightings as the quiet guest in 04's Movements I–V (one visible, deniable beat per
Movement, plus how it reacts if pursued); the one-page MM sheet; the Movement VI
read-aloud when it drops the pretence (perception only); 01's list of threats; and
flow.json (a pre-midnight "quiet guest" thread + S14).

**Inventions log:** the Attendant is owner canon; its *mechanics* and
every behavioural detail beyond the owner's quote go in INVENTIONS_5e.md.

### §5a Revision — the Attendant is the midnight boss (owner, 2026-09-28)

Owner: "While I've downplayed their capabilities a lot, when they do focus they can be
devastating. It should be the 'boss' of sorts they have to deal with when (if) the
Uninvited want the party distracted." This supersedes the ~CR 5 sizing above.

- **Two states.** *Idle* (its default: Rusty, easily Distracted, magic it can't be
  bothered with) and **Focused**. It becomes Focused when an Uninvited **turns it on the
  party** — the moment the party becomes a real interruption (they earn Delay, strike an
  Uninvited, or stand between one and its errand). The MM says it out loud: one of the
  three glances at the Attendant and at the party, and it stops being idle.
- **Focused is devastating.** Stat it as a true boss for four 3rd-level PCs — roughly
  **CR 7 while Focused** *(now CR 8 at 4th level — §5b)* (deadly by the XP table on purpose): it drops Rusty, attacks
  several times a round, and its powerful magic is usable every round it is Focused
  (Recharge 5–6), plus a boss rule (acts twice per round or a lair-free extra action —
  keep it to one simple rule).
- **Focus is the dial the party controls.** A successful distraction (DC 15 while
  Focused, DC 13 when Idle) knocks it from Focused back to Idle until an Uninvited
  refocuses it (at most once per round, and only while that Uninvited is not being
  delayed — so Buying Time and handling the Attendant feed each other). Third
  distraction of the night: it wanders off (a win), as before. *(Superseded by §5b:
  DC 19 while Focused, refocus at the start of its turn, the fourth broken focus.)* Driving it to 0 HP: it
  loses interest in being here and steps into the shadow (a win).
- **Deadly but not lethal.** §1 Down, Not Out applies to its drops (it removes
  interruptions; it does not hunt). The fight can flatten the party; it cannot end a
  character.
- **S14 is the climax boss card** — it fires only if the party interferes enough to be
  worth distracting, which is the table's choice. It is visible and optional by
  construction. Budget line should say "Deadly while Focused; High while Idle" and show
  the math; scaling lines per R2. Simulate it (expected value or Monte Carlo) so a party
  that plays the distraction game wins more often than not, and a party that only trades
  blows usually gets flattened.

### §6 Revision — party level 4 (owner, 2026-09-28)

**R2 is now: four 4th-level PCs.** The whole module moves to 4th level: every fight card,
every XP budget, the pregens (rebuilt at 4th — SRD 5.2.1 4th-level features, ability
score improvement or an SRD feat at 4th), the level/XP lines in 01 and the epilogue (the
night ends at 5th). SRD 5.2.1 XP budget per character at 4th: **Low 250 / Moderate 375 /
High 500** → for four: **1,000 / 1,500 / 2,000**. *(Corrected by the integrator,
2026-09-28: this line first printed 250 / 500 / 750 and 1,000 / 2,000 / 3,000, which
are not the SRD's 4th-level figures — 750 per character is Moderate at 5th. Steel's
S-10 caught it; every card and table in the book uses the corrected figures.)* Scaling lines become "three PCs",
"five PCs", "3rd level", "5th level".

**The Attendant (S14), owner:** "extremely challenging, but not a guaranteed death
sentence at 4 party members at lvl 4." Tune Focused to beyond High for four 4th-level
PCs, and verify by simulation against the rebuilt 4th-level pregens **and** a typical
optimised 4th-level party:
- Party that engages the distraction game: **wins ≥ 55%** (drives it off or makes it
  wander) — hard, sweaty, several PCs dropped along the way.
- Party that only trades blows: wins **15–30%** — possible, not likely.
- Chance the whole party is down at once: **≤ 35%** even for blow-traders — and since §1
  applies, "down" is never death.
Report the numbers on the card and in the log.

*Targets refined by the coordinator (2026-09-28), after Steel's simulation found leaning
in won almost every time in three or four rounds: a party that leans in wins **~60–75%**
with at least one PC dropped in most fights; bare distraction **~40–55%**; blow-traders
**15–30%**; whole party down at once **≤ 35%**. The integrator's retune in §5b meets
them for the pregens; see the log for the optimised party.*

### §5b The Distraction mechanic (owner, 2026-09-28)

Owner: "a distraction mechanic for it, something d20 based with bonuses if players lean
into it, with MM instructions on how to hint that it can be distracted." Printed in
full on S14 and summarised in the Attendant's block in 10. Exact rules:

*Revised by the integrator (2026-09-28). The first version (DC 13 / 16, advantage for
playing it out, +2 per habit to +4, +2 for novelty, +6 cap, any number of tries a round,
three distractions of either kind to wander) was far too easy: in simulation a party
that leaned in won 99–100% of the time, and even bare rolls won 86%. What changed, and
why: one try a round (otherwise the table just rolls until it lands); flat +2s instead
of advantage (advantage on top of a +8 skill made the DC irrelevant); only a broken
focus counts, and four of them; a broken focus lasts only until its next turn (the
quicker refocus); DC 19 while Focused. The block moved with it (HP 229, Joined Hands
1d10 + 4, Put Aside DC 14 for 2d8, CR 8). Numbers in the log (Integrator).*

**Distract the Attendant** (**an action**). Describe what you do, then roll **d20 + the
ability and skill that fit the trick** (Performance for music, Deception for a false
order, Arcana to show it a working crystal, Persuasion to ask it a question it must
answer, Sleight of Hand to take its cup, and so on) against **DC 13 while it is Idle,
DC 19 while it is Focused**.

**One trick a round.** It watches one thing at a time: once anyone has tried a trick on
it in a round, win or lose, nobody else can until the next round, and Help doesn't
apply.

**Leaning in — +4 at most:**
- **In character, specific, vivid** — the player performs or plays out the distraction
  rather than naming it ("I hold the lamp crystal up to the fire so it throws colours
  across its mask and say, 'Your master asked me to show you this'") → **+2**.
- **Uses a habit the party has seen** → **+2** (the payoff for noticing it before
  midnight). Its four habits, each shown once before midnight (see Hints): *it stares
  at worked crystal and light*; *it answers any direct question literally, and cannot
  leave one unanswered*; *it keeps a cup and cloak ready for a master who is not there*;
  *it follows music that changes*.
- **Repeats:** a trick already tried on it tonight gets no bonus and has
  **disadvantage** (it learns). The same trick never works a third time.

**Refocus.** It is Idle until the party first becomes a real interruption. From then
on, at the start of each of its turns, it is Focused if any one of the three in the
scene has no Delay (a glance is enough). Delay on every Uninvited in the scene keeps
it Idle.

**Results:**
- **Success while Focused:** its focus **breaks** — Idle until the start of its next
  turn. Counts.
- **Beat the DC by 5 or more while Focused:** its focus breaks **and** it loses its next
  turn. Counts.
- **Success while Idle:** it does nothing on its next turn. Does **not** count.
- **Failure:** the trick is spent. If it was Focused, its next attack targets the
  distractor.
- **Natural 20:** as beat-by-5, and the distractor gains Heroic Inspiration.
- **Fourth broken focus of the night:** it wanders off — a win (§5, §5a).

**MM — how to hint it can be distracted (print on S14 and in 04's sightings):**
1. **Show every habit before midnight, once each, plainly.** One sighting per Movement
   (04): Movement I it holds a cup for someone who never takes it; Movement II it stops
   dead in front of a crystal wall and watches the light for a full minute; Movement III
   a guest asks it the time and it answers precisely, then answers the follow-up, then
   the next, until the guest walks away; Movement IV the band changes tune and it turns
   to follow the sound; Movement V it is trying to watch the party and keeps losing them
   because something shiny passes. A player who says any of these out loud earns the
   omen reward.
2. **The hitch.** The first time anything unexpected happens within its sight during the
   fight (a thrown light, a shout, a crashing tray), describe a visible half-second hitch
   — its head turns, its strike stalls — and then it recovers. Do this once, for free,
   in round 1. That is the tell.
3. **Say its state out loud.** "It's locked on you" (Focused) / "It's drifting" (Idle).
   Players can't use a dial they can't see.
4. **Reward the attempt, not only success.** The first player to try distracting it gets
   Heroic Inspiration whether or not it works.
5. **If nobody tries by round 3:** one of the Uninvited says something to it — a curt
   word, the way you'd call a dog back to heel — and it snaps from a fixation back to
   Focused. Let the players see that it *needed* calling back.

**Inventions log:** the four habits, the hitch and the heel-call are new; log them.
