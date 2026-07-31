# Agentic Playtests — Design

**Date:** 2026-07-31
**Tier:** Planner
**Status:** Design complete, not yet implemented
**Motivating question:** does "NPCs never roll" hold up at a real table — and more
generally, can agentic playtests tell us anything about *fun*?

---

## 1. What the previous playtests actually measured

Before designing new ones, I checked what playtests 01–07 produced. The finding
changes the design, so it goes first.

**The dice in the session logs were not rolled.** Across the 20 `session_log_*.md`
files in `playtest/07_oraga_night_playtests/`, every reported 2d6 pair is written
into the prose by a language model rather than read from the engine. The
distribution gives it away:

```
session_log_01: (2,3) (3,3) (2,3) (2,3)
session_log_13: (3,3) (3,3) (3,3) (3,3)
session_log_04: (5,5) (6,6) (5,5) (5,6)
```

Across roughly 60 dice there is **not a single 1**, and almost no 6s. Sums cluster
hard on 6–7. This is the well-documented shape of an LLM writing numbers that look
like dice — biased to the middle, avoiding extremes — not of 2d6.

**Separately, the real dice were over-counted 4×.** `run_oraga_night_playtests_v2.py`
does drive the live engine, but it reads results wrong: each player's roll is sent,
then `read_until(ws, "roll_result")` reads from *that player's* socket — and
`roll_result` is **broadcast to everyone**. All four sockets receive the same first
broadcast. Hence `dice_rolls.txt`:

```
Session 01 | Serane | gate_check | Total: 7 -> partial_success
Session 01 | Pello  | gate_check | Total: 7 -> partial_success
Session 01 | Dassa  | gate_check | Total: 7 -> partial_success
Session 01 | Ilesse | gate_check | Total: 7 -> partial_success
```

Four identical totals in every session, in every batch. The outcome distribution in
`playtest_report.md` is drawn from a quarter of the real sample with each value
counted four times.

**And the "play" was a hardcoded script.** The runner's decision logic is:

```python
if idx in (11, 16):        # everyone rolls persuade
elif idx in (12, 17):      # everyone rolls stealth
```

No agent chose anything. No player could decline a hook, argue with the MM, or
solve a problem laterally.

### The actual failure

Previous playtests split into two artifacts that never touched:

| Artifact | Has | Lacks |
|---|---|---|
| `run_*.py` | Real engine, real dice | Any decision-making — a fixed script |
| `session_log_*.md` | Personalities, table talk, improvisation | Real dice, real rules |

That is not "too much mechanics." It is **two independent implementations of a
play session that silently diverged** — precisely the failure `CLAUDE.md` already
records for `combat_sim.py`:

> Combat resolution existed as two independent implementations that silently
> diverged, which invalidated a research corpus of recorded simulation numbers.

Same failure, one layer up. The narrative was not a record of a session; it was
fan-fiction about one. The MM agent also invented mechanics that don't exist —
`"You have the 'Watched' condition (Tier 1)"`, `"Noticed by Vorlain condition"` —
because nothing was checking it against the ruleset.

**Consequence for this plan:** every mechanical conclusion in
`playtest/07_*/playtest_report.md` should be treated as unverified until re-run.
The qualitative observations about MM behaviour may still be worth something; the
numbers are not.

---

## 2. The architectural rule

> **The agent decides. The engine resolves. The agent narrates what it was told.**

Concretely:

- An agent's only mechanical output is a **tool call** — a structured intent
  (`roll_skill`, `declare_posture`, `strike`, `land_enemy_attack`, `spend_spark`).
- The agent **never emits a number, an outcome tier, or a Condition name it made up.**
  The tool result is the fact; the agent's next turn narrates around it.
- The transcript is **generated from the event log**, not written alongside it. There
  is no path by which prose and mechanics can disagree, because the prose is
  rendered from the same events the engine emitted.

This is the same discipline `facet.yaml` and `combat.py` already enforce for the
software, applied to the playtest harness. It is non-negotiable: without it, the
harness reproduces the exact bug documented in §1.

A validator asserts the property directly: **no agent free-text may contain a dice
result, an outcome label, or a Condition ID that isn't present in the event log for
that beat.** If an agent writes "I rolled a 9", the run fails, not the analysis.

---

## 3. What makes a table a table

The previous logs weren't mechanical because the *engine* was over-represented —
they were mechanical because everything that isn't mechanics was missing. Real
tables are made of the parts that aren't rules.

### 3.1 Player agents have wants, not just stats

Each player agent gets a **private agenda** the MM cannot see. Examples:

- "You want your character's fear of water to come up. Steer toward it."
- "You think the MM's plot is boring. You'd rather rob the place."
- "You want to make the table laugh at least twice."
- "You want Zulnut to like your character."
- "You are quietly competing with Mordai's player for the spotlight."

Agendas are what produce the friction, tangents, and side-quests that make a
session feel like a session rather than a decision tree.

### 3.2 Play personalities, not skill levels

Playtest 07 used "Novice/Expert", which mostly generated rules-lawyering — a
correction loop, not a table. Replace with the **player-type taxonomy this project
already cites** (Laws 2002, *Robin's Laws of Good Game Mastering*, in
`research/dice_system_analysis.md` sources):

| Type | Wants | Failure mode it surfaces |
|---|---|---|
| Power Gamer | Mechanical advancement, optimal builds | Advancement pacing, build traps |
| Butt-Kicker | To fight things | Combat that's boring or too rare |
| Tactician | Clever plans that beat the odds | Systems with no interesting decisions |
| Specialist | To use their one signature thing | Specialty/Technique that never applies |
| Method Actor | To stay in character | Mechanics that break immersion |
| Storyteller | The plot to move | Sessions that stall |
| Casual | To hang out; low engagement | Rules that punish inattention |

Each archetype detects a *different* class of design problem. A table of four
identical engaged optimizers finds one.

### 3.3 The MM agent must be able to be wrong

The MM agent gets prep — a scene, a front, three NPCs, a threat clock — and an
explicit instruction that **prep is disposable**. It must be willing to abandon the
planned scene when players go sideways, and it must not railroad them back.

It is also given the actual PHB and MM Manual sections as context, and told: *if the
rules don't cover this, rule it and say you ruled it.* Every such ruling is logged
as a **rules gap** — that list is one of the most valuable outputs.

### 3.4 Players may refuse

Explicit in the player system prompt: *You are not required to follow the MM's hook.
If your character wouldn't do it, don't.* Without this, agents are agreeable and
every session becomes a rail.

### 3.5 Out-of-character talk is first-class

Agents may speak as themselves, not just as characters: jokes, "wait, what's my
modifier", snack breaks, arguing about what to do next, recalling a previous
session. A transcript with zero OOC content is not a table transcript. The OOC/IC
ratio is measured (§4).

---

## 4. Measuring fun without trusting self-report

This is the part that decides whether the exercise is worth anything.

**LLM agents are agreeable.** Ask "was that fun, 1–10?" and answers cluster at 8
regardless of what happened. Absolute self-report is worthless here. The design
works around that in three ways.

### 4.1 Behavioural metrics — computed from the log, no self-report

| Metric | Computed from | What it detects |
|---|---|---|
| **Spotlight share** | decisions + rolls + lines per player | One player dominating; another starved |
| **Longest idle streak** | consecutive beats with no action by player X | The "I sat there for 20 minutes" problem |
| **Decision:roll ratio** | choices offered vs dice thrown | Play that's mechanical rather than dramatic |
| **Proposal length trend** | words per player action, first third vs last third | **Disengagement** — the strongest available behavioural proxy |
| **Lateral solution rate** | non-combat resolutions of combat-capable scenes | Whether the fiction actually has give |
| **Callback rate** | references to earlier events | Investment in the story |
| **OOC:IC ratio** | tagged speech | Whether it reads as a table at all |
| **Zero-dice exchanges** | exchanges where nobody rolled | Direct measure for the §5 question |
| **Rules gaps** | MM "I ruled it" markers | Where the PHB is silent |
| **Rule violations** | validator diffs vs engine state | Where the PHB is unclear enough to misread |

### 4.2 Elicited metrics — forced-choice and forced-negative only

Never "rate this". Always a comparison or a required criticism:

- *"Rank these three scenes best to worst."* (forces discrimination)
- *"Which single moment would you cut from the session?"* (forces a negative)
- *"Was there a point where you didn't know what your options were? Quote it."*
- *"Which other player had the best moment? Which had the worst session?"*
- *"You have one change to the rules. What is it?"*

Collected via **structured outputs** so the answers are analysable, and collected
**out of character** after the session ends.

### 4.3 Blind comparative judgement — the load-bearing one

For any A/B question, a fresh agent that took no part in either session is shown
**two transcripts with the variant labels stripped** and asked which table it would
rather have sat at, and why. Run it both ways round to control for order.

This is the only instrument here that produces a signal an agreeable model can't
inflate: it cannot say "both were great" — the answer format doesn't allow it.

---

## 5. The experiment: does deterministic enemy severity hold up?

From `research/dice_system_analysis.md` § Player-Facing Rolls, the open question is
not whether NPCs should roll — precedent is strong — but whether **fully
deterministic enemy severity** makes fights feel same-y, and whether variance
concentration ruins one player's night.

### Arms

| Arm | Enemy attack severity | Everything else |
|---|---|---|
| **A (control)** | Fixed by tier: Mook = Tier 1, Named/Boss = Tier 2 | Current rules |
| **B (variant)** | MM picks from a weighted list per tier (Named/Boss: 60% Tier 2, 40% Tier 1) | Identical |

Arm B preserves "NPCs never roll" completely — the MM is already choosing the
Condition from a list in the app; B just widens the list. That makes it the
cheapest possible fix if A shows a problem, and it means a positive result is
directly actionable.

### Design

- **Same scenario, same pre-built characters, same seed set** across both arms.
- **Paired runs:** each (scenario, party) pair is run once in each arm.
- **8 sessions per arm minimum** — enough for the behavioural metrics to separate,
  not enough for statistical significance. This is a signal-finding exercise, not a
  hypothesis test, and the write-up must say so.
- Player agents are **not told** which arm they're in.

### Pre-registered predictions

Written before the run so the analysis can't drift:

1. Arm A shows **more zero-dice exchanges** than B.
2. Arm A's debriefs mention boss/enemy **repetitiveness** more often than B's.
3. Blind comparative judgement **prefers B** in combat-heavy sessions and shows **no
   preference** in social-heavy ones.
4. Variance concentration (worst-luck player's spotlight share and proposal-length
   trend) is **equally bad in both arms** — because the reaction roll is unchanged,
   this is not what the arm manipulates.

Prediction 4 is the control: if it comes out differently, the harness is measuring
something other than what we think.

### Secondary questions the same runs answer for free

- Which Techniques and Backgrounds never get used?
- Which skills are dead weight?
- Where does the MM have to invent a rule?
- Does the Spark economy actually cycle, or do Sparks hoard? (Playtest 01 found
  hoarding; nothing has re-checked it since.)

---

## 6. Architecture

```
                  ┌──────────────────────────────────────┐
                  │  Orchestrator (tools/agentic_playtest)│
                  │  turn order, budget, logging          │
                  └───────┬───────────────────┬───────────┘
                          │                   │
              tool calls  │                   │  tool calls
                          ▼                   ▼
        ┌─────────────────────┐     ┌────────────────────────┐
        │  MM agent           │     │  Player agents ×3–4    │
        │  (claude-opus-5)    │     │  (claude-opus-5)       │
        │  prep, fronts, NPCs │     │  agenda, archetype     │
        └─────────┬───────────┘     └──────────┬─────────────┘
                  │                            │
                  └──────────┬─────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Table adapter       │   the ONLY path to mechanics
                  │  → app/game/*        │   (engine, combat, character)
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Event log (JSONL)   │  ← single source of truth
                  └──────────┬───────────┘
                             ▼
              ┌──────────────┴──────────────┐
              ▼                             ▼
      transcript.md (rendered)      metrics.json (computed)
```

### Decisions

**D1 — Drive `app/game/*` directly, not the WebSocket API.** The v2 runner's 4×
over-count was a WebSocket-broadcast aliasing bug. Calling the engine in-process
removes that whole class of error, is far faster, and needs no running server. The
engine is already the single source of truth (`CLAUDE.md`: *the simulator may only
drive `app/game/combat.py`*). The web app has its own regression suite
(`tests/e2e/test_ui_flows.py`) — the playtest harness does not need to double as
an API test.

**D2 — Tool use, not prose parsing.** Every agent action is a typed tool call with
a JSON schema. An agent that wants to roll calls `roll_skill(skill_id=..., ...)`;
it cannot state an outcome. Use the SDK's tool runner (`client.beta.messages.tool_runner`)
rather than a hand-written loop.

**D3 — `claude-opus-5` for every agent.** Cheaper models produce flatter table talk,
which is precisely the axis under test. Effort is the cost lever, not model tier:
MM at `high`, players at `medium`, the blind judge at `high`.

**D4 — Prompt caching is load-bearing.** The shared prefix (ruleset digest, scenario,
cast) is large and identical across every agent and every turn. Put a
`cache_control` breakpoint at the end of it; without caching this is roughly 5×
more expensive. Keep volatile content (turn number, recent events) strictly after
the breakpoint — see `shared/prompt-caching.md`.

**D5 — Structured outputs for debriefs.** Post-session surveys use
`output_config.format` with a schema so answers are analysable rather than prose to
be re-parsed.

**D6 — Budget ceiling per session, enforced.** A runaway agentic loop is the main
cost risk. Hard cap on turns per session and total tokens per run; the orchestrator
aborts and records a partial session rather than burning the budget.

### Cost estimate (order of magnitude, must be re-measured)

A 4-agent, ~40-beat session with an aggressive cached prefix is roughly
**$3–8 per session** at Opus-5 rates. 16 sessions (8 per arm) plus judging is on
the order of **$60–150**. Task 1 pins this down with a single instrumented pilot
before committing to a batch.

---

## 7. Honest limits

State these in any write-up produced from this harness.

1. **Agentic playtests cannot validate fun.** They can find *structural* problems —
   spotlight starvation, dead exchanges, rules that never fire, options nobody
   understands. Whether the game is enjoyable to humans is not measurable here.
2. **Agents are not players.** They don't get bored, don't have a bad week, don't
   care about their character between sessions, and can't be surprised in the way
   that makes a table moment land.
3. **8 sessions per arm is signal-finding, not significance.** Report differences as
   observations to check with humans, never as findings.
4. **The blind judge is one model judging its own family's output.** It is the
   strongest instrument here and still a weak one.
5. **A confirmed problem is real; an unconfirmed one is not evidence of absence.**
   If the harness finds Bosses feel same-y, that is worth acting on. If it doesn't,
   that does not mean they don't.

---

## 8. Success criteria for the harness itself

The harness is done when:

- [ ] Every die in every transcript is traceable to an engine call in the event log
- [ ] The validator fails a run if any agent free-text contains an unlogged mechanic
- [ ] Re-running with a fixed seed reproduces the mechanical outcomes exactly
- [ ] The dice distribution across a full batch passes a chi-square goodness-of-fit
      test against 2d6 (the specific check that would have caught playtest 07)
- [ ] A transcript reads like a table — OOC talk present, at least one refused hook,
      at least one lateral solution — verified by reading three of them

The fourth item is deliberately the test that the previous corpus fails.

---

## 9. Open questions for Brain

None blocking. Two worth a decision before the batch run:

- **Q1.** Is 8 sessions per arm the right spend, or should the pilot inform it? The
  plan assumes pilot-then-decide (Task 1 gates Task 9).
- **Q2.** If Arm B wins, is widening the MM's Condition list acceptable, or does the
  fixed tier mapping carry design weight this document hasn't captured?
