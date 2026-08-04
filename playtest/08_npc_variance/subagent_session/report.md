# Subagent playtest — qualitative read

**Date:** 2026-07-31 · **Scenario:** The Guardian Chamber · **Seed:** 1 · **Arm:** A
**Artifacts:** `transcript.md`, `events.jsonl`, `metrics.json`, `validation.txt`, `briefings/`

## What this is, and what it is not

Five Claude Code subagents — one Mirror Master, four players — played on a real
running instance of the application, each through its own authenticated account,
driving the table with `play_as.py`. The rules were resolved by the engine, the
event log was written by the observer socket, and this transcript was rendered
from that log.

**This is not the T4.2 gate.** The gate exists to measure cost per session so the
16-session A/B batch can be budgeted, and subagents do not report token usage.
This answers the other half — *does it read like a table?* — and leaves the
budgeting half open. The A/B experiment itself still needs the API path.

Two beats were played. That is short, and every number below should be read as a
single observation rather than a measurement.

## The headline

**Validation: no confabulated mechanics found.**

Every die value in the transcript came from the engine. In batch 07, ~60 dice
contained no 1s at all and the narrative rolls were written by a language model;
the same validator run over this session found nothing. The structural fix works
when real agents are pushing on it, not only when a scripted stand-in is.

It also reads like a table, which the batch-07 corpus did not:

- Sophia refused the MM's hook outright — *"I do not care what is making noise.
  Brost is paying us to file a complaint about a sound."*
- Luke then refused **Sophia** — *"Sophia, I hear you, and Mordai does not. He is
  a watchman. There are two body-shaped things on the floor and nobody has
  checked whether they are people."*
- Penny was confidently wrong, rolled a 6, and had her character own it in
  front of the party — *"I had a guess with a confident voice on it."*
- Toby held the party at the stair and refused to act on any of the three
  competing theories until someone produced information.

Nobody was steered. The MM abandoned its prep when the party went elsewhere, and
the Guardian — the scenario's centrepiece — never woke, because the MM
established its trigger was breach of the vault door and nobody touched it.

## Findings

### F1 — PHB III.3 forbids what the engine allows (Software-PHB desync)

`player_handbook/III.3_Combat.md:112`:

> the skill is **Combat** for melee and unarmed Strikes, **Finesse** for ranged ones.

`software/app/api/websocket.py`, `_handle_strike`:

```python
# Accept attribute/skill from client; default to strength/combat for backward compat
attribute_id = str(msg.get("attribute_id", "strength"))
skill_id = msg.get("skill_id", "combat")
```

The engine accepts any pairing. The book prescribes one. The v0.2 audit widened
the engine deliberately and III.3:112 was never updated to match — exactly the
divergence the Software-PHB sync rule exists to prevent, unnoticed until a player
tried to punch something with Finesse.

**It invalidates a character concept.** Zulnut is monk-adjacent: Finesse
Practiced, Combat Novice. Read literally, the book requires his unarmed strikes
to use his worst skill. Built strictly to the text, the concept is mechanically
wrong.

**Proposed fix** (from the MM's own ruling): demote the melee/Combat,
ranged/Finesse line from rule to *example*, and let the fiction choose the
pairing. Requires III.3 body text, the III.3 quick-reference block,
`MM5_Quick_Reference.md`, and a check that `facet.yaml` states no narrower rule —
one commit, per the sync policy.

### F2 — Four of nine attributes carry exactly one skill

Raised unprompted by two players, from opposite sides: Penny has Luck 3 and had
never once rolled `gamble` in three sessions; Toby has Spirit 3 and only
`attune`.

| Skills | Attributes |
|---|---|
| 3 | charisma |
| 2 | dexterity, intelligence, strength, wisdom |
| **1** | **constitution, knowledge, luck, spirit** |

**The MM stated this as "6 of 9". That is wrong — it is 4 of 9.** It wrongly
counted strength and intelligence, which carry two each. The figure above is
computed from the ruleset; the MM issued a correction on the record when shown it.

The complaint survives the correction and arguably sharpens: both non-charisma
Soul attributes are on the single-axis list, so within one Facet a character
investing in spirit or luck gets one skill where one investing in charisma gets
three. The MM's mitigation — read `gamble` broadly, let players propose Luck as
the axis when the fiction is betting — is a table ruling, not a fix, and it said
so: *"a design load-bearing on GM generosity, which is exactly the kind of thing
this game says it does not want."*

**Not yet a recommendation.** Whether to add skills, merge attributes, or accept
the asymmetry is a design decision above this playtest.

### F3 — A Specialty has no defined behaviour when no skill fits

Luke attempted a formal Watch sentry challenge to a construct and asked, rather
than assuming, which axis it resolved on. A Specialty only shifts difficulty
(Standard → Easy), so it has nothing to attach to when there is no roll — and the
rules do not say what happens then.

The MM's ruling: do not manufacture a roll to have something to resolve; the
Specialty establishes for free that the character executed the thing correctly,
and the world answers rather than the dice. With a corollary worth keeping:
*"'it does nothing' is never the right answer to a well-aimed action. A correctly
executed procedure that gets no response has produced information."*

Candidate text for II.5 or III.1.

### F4 — Strike and enemy removal are a two-actor handshake

Penny rolled a Full Success on a Mook and wrote that it "should be gone". The
engine still listed both constructs: `strike` produces a roll, and removing the
enemy requires the **MM** to separately call `apply_strike_to_enemy`. Between
those two steps the player's model of the fight and the engine's state disagree,
silently.

**Checked: the seam is real for human tables too.** `onStrikeResult` in
`play.js` updates the roll log and the attacker's Endurance but never touches the
enemy tracker. The MM did get a toast saying "apply it on the enemy tracker", but
it was transient and left them to find the row.

**Fixed.** When the Strike's target is a tracked enemy, the prompt now carries an
**Apply** button that sends the outcome directly, and it is keyed so repeated
Strikes replace rather than stack. A PvP or untracked target still falls back to
the advisory text, because there is nothing to apply it to.

### F5 — One player fought the entire fight

The MM raised this itself at the act break: *"one player fought that entire fight
while three watched, and I don't know whether that's the system working or three
players idling."*

The metrics agree, with a caveat that matters: `spotlight_spread` is 0.60, and
Luke records **0 actions** — but 519 words. He talked, questioned, and positioned
for a whole beat without touching a mechanic. The metric counts mechanical
actions, so a player can be fully engaged and score zero. That is a limitation of
the instrument, and the A/B analysis must not read "0 acts" as "idle".

## Metrics

Two beats. Treat as one observation, not a measurement.

```
spotlight spread      0.60   (0 = even, 1 = one player)
decisions per roll    1.25
OOC : IC              0.76
callbacks             81
zero-dice exchanges   0 / 1
enemy attacks         1
rules gaps            4
refused actions       0
confabulations        0

player       acts  rolls  words  idle
Sophia          1      1    194     2
Luke            0      0    519     1
Penny           3      2    925     0
Toby            1      1    609     1
```

OOC:IC at 0.76 is the number to keep an eye on. A transcript with no
out-of-character talk is not a table, and this one has plenty — two of the four
findings above came out of it. `proposal_length_trend` is 0.00 for everyone
because two beats is far too short to compute a trend.

## What this session did not test

- **Boss severity.** The Guardian never woke. The experiment's actual question —
  whether a Named/Boss landing Tier 2 *every* time feels same-y — was not
  exercised. Only two Mooks acted, and Mooks land Tier 1.
- **Cost.** No token accounting is available on this path.
- **Arm B.** No comparison was run, so nothing here speaks to the A/B question.
- **Anything statistical.** n = 1, two beats.

## Disposition

| | Status |
|---|---|
| **F1** Strike pairing desync | **Fixed** — III.3 body text, `Quick_Start.md`, `MM5_Quick_Reference.md`. Pinned by INV-8. |
| **F2** Single-axis attributes | **Open — needs a design decision**, not a fix. |
| **F3** Specialty with no skill | **Fixed** — new subsection in II.5. |
| **F4** Strike/enemy handshake | **Fixed** — one-click Apply on the MM's prompt. |
| **F5** Spotlight metric counts only mechanics | **Noted** — the A/B analysis must not read "0 acts" as "idle". |
| **F6** e2e suite deadlocked its own server | **Fixed** — found while adding the F4 test; see below. |

### What was changed

**F1.** `facet.yaml` states no skill constraint on Strike and the engine accepts
any pairing (already pinned by `test_websocket.py`, "Strike can use any
attribute"). The engine was widened deliberately by the v0.2 audit and the book
was never updated, so the book was brought to the engine rather than the reverse.
III.3 now presents Combat/Finesse as defaults and invites the player to use the
skill that describes how they are striking; both quick references were updated in
the same pass, per the rule that a quick ref may only compress canonical text.

Parry was checked and is **not** affected — `_handle_react` hardcodes `combat`
and III.3:195 says Combat. Those agree, and neither was touched.

New invariant `INV-8` in `tests/test_docs_consistency.py` fails if any book line
naming both skills for a Strike states them without a hedge. It was verified
against the original wording: restore III.3:112 and the test fails.

**F3.** II.5's Specialty section gained a *When no skill fits* subsection: do not
invent a roll; the Specialty establishes for free that the character executed the
thing correctly, and the world answers. Including the corollary that "nothing
happens" is never that answer, because a correctly executed procedure that gets
no response has still produced information.

**F4.** See above.

### F6 — the browser suite could deadlock its own server (found while fixing F4)

Adding two e2e tests for F4 pushed `tests/e2e/test_ui_flows.py` past a threshold
and the last test began erroring in fixture setup. The cause was not the new
tests:

`live_server` launched the server with `stdout=subprocess.PIPE,
stderr=subprocess.STDOUT` and never read the pipe. uvicorn logs every HTTP
request at info level, so about fifty tests in the 64KB OS pipe buffer filled and
the server **blocked on write** — permanently wedged, serving nothing. Whichever
test was running at that moment got blamed, which is why it read as flakiness.

The server now logs to a file, which cannot fill; the fixture reads that file
when it needs to report a startup failure. Full suite: 52 passed, 0 errors.

Three wrong diagnoses preceded the right one — contention between concurrent
suites, session accumulation, and leaked WebSocket connections — each disproved
by measurement. The session-accumulation "fix" actively made it worse: one extra
HTTP request per test filled the pipe sooner. The reason none of the standalone
repro scripts ever reproduced it is that all of them used `stdout=DEVNULL`.

### Still open

**F2** is the one that needs you. Four of nine attributes carry exactly one skill
and charisma carries three; within the Soul Facet, spirit and luck each buy one
skill where charisma buys three. Adding skills, merging attributes, or accepting
the asymmetry are all defensible and none of them are a playtest's call.

The A/B batch still needs the API path and API credits. This session says the
agents are good enough to be worth running it with — which was the open question.
