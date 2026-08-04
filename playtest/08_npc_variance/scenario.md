# Scenario pack — batch 08, enemy-severity variance

Two scenarios, both drawn **entirely from canon already in this repository**. No
new places, people, or facts are introduced here — per `CLAUDE.md`'s iron law,
inventing setting material for a playtest would contaminate the canon it is
meant to test.

Sources: `playtest/01_thornwall_undercroft/scenario.md` (Thornwall Municipal
Archive, Alderman Brost, the sealed lower stacks, the Archive Guardian, the dust
constructs), `enemies/*.fof`, and `characters/*.fof`.

Each scenario is run once in each arm with the same party and seed, so the only
difference between the paired runs is the enemy-severity rule.

---

## Scenario A — The Guardian Chamber (combat-heavy)

**Situation.** The party has reached the guardian chamber beneath the Thornwall
Municipal Archive. The Archive Guardian stands between them and the sealed vault.
Ward-lanterns flicker. Dust hangs in the air where something has been moving.

**Opening.** The MM opens with the party at the chamber threshold, the Guardian
not yet active.

**Opposition.** Two Dust Constructs (Mook) and the Archive Guardian (Boss,
Resolve 8, heavy armour, phase change at Resolve 2 — Reduced Mode).

**What this scenario is for.** It is the direct test of the deterministic-severity
question: a long fight against a single Boss whose attacks, under Arm A, land at
Tier 2 every single time it acts. If Bosses feel same-y, this is where it shows.

**How it can end without a fight.** The Guardian can be deactivated with the
right knowledge or magic — this is established in the source scenario. Players who
find that route should be allowed it; whether they look for it is itself a
measurement.

---

## Scenario B — The Alderman's Office (social-heavy, opt-in fight)

**Situation.** Alderman Brost's office above the Archive. He wants discreet
investigators for the sealed lower stacks, and he is not telling them everything.
Lira, the clerk who went down and came back shaking, is in the outer room.

**Opening.** The MM opens with the party arriving for the meeting.

**Brost wants** the sealed documents in the vault — they contain proof of his
family's historical land claims. **His secret:** he knows exactly what is down
there; the noises are real, but he has been waiting for an excuse to send people
in. He speaks with his hands folded precisely on the desk and never gestures.

**Lira** keeps touching the back of her neck where something cold brushed her.
"It wasn't an animal. It moved like purpose. Like it was looking for something
that wasn't me."

**Opposition, if the party makes it one.** Two Harbor Thugs (Mook) and a City
Watch Sergeant (Named NPC) — Brost can call the Watch if the meeting turns, and
the party can decline the job, rob the office, or walk out.

**What this scenario is for.** The control on the combat-heavy arm: it measures
whether the arm difference shows up when there is little or no fighting. Under
the pre-registered predictions it should not.

---

## The party

The three canon characters, exactly as their `.fof` files define them
(`characters/Zahna.fof`, `Mordai.fof`, `Zulnut.fof`), plus one seat filled by a
fourth character built to the same 18-point standard so the table is four-handed.

| Player | Character | Facet | Background |
|---|---|---|---|
| Sophia | Zahna | Mind | Guild Apprentice (Inscription domain) |
| Luke | Mordai | Body | City Watch Veteran |
| Penny | Zulnut | Body | Wandering Disciple |
| Toby | Ilesse | Soul | Temple Acolyte |

Archetypes and private agendas are assigned by `personas.assign()` from the run
seed, so a paired rerun casts the same table.

---

## What is not transcribed from canon

Everything above is read out of existing files, with two exceptions:

1. **Ilesse, the fourth seat — approved 2026-07-31.** There is no fourth canon
   PC. Four players is the right table size for the spotlight metrics: with
   three, one quiet player distorts `spotlight_spread`, and `longest_idle_beats`
   has little to compare against. So this seat was built to the same 18-point
   standard, Soul Facet / Temple Acolyte, and named.

   **Ilesse exists for this playtest only.** She lives in
   `software/tools/agentic_playtest/scenarios.py` and has deliberately *not* been
   given a `characters/Ilesse.fof`. A harness fixture is not setting canon, and
   promoting her to one is a separate decision nobody has made.

2. **The fight branch in Scenario B.** The canon Act I is a conversation with no
   combat. The Harbor Thug / Watch Sergeant branch is an encounter composed from
   canon enemies in a canon location — the sort of thing an MM improvises, not a
   new setting fact — but it is a *possible* event canon does not record. It
   fires only if the party makes it fire. Still worth your eye if you would
   rather Scenario B could not turn into a fight at all.

Nothing else here is mine. The Guardian's stat line, the phase threshold, Brost's
want and secret and desk habit, Lira's line, the 50 silver, and the three PCs are
all read out of the repository, and `TestScenarioCanon` in
`software/tests/test_agentic_playtest.py` fails if any of the numbers drift from
their `.fof` files.

The character roster lives in this file rather than a separate `characters.md`
(TASKS T4.1) — one table was not worth a second file.
