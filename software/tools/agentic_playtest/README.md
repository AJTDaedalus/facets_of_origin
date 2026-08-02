# Agentic playtest harness

Agents play *Facets of Origin* on the real application — each with its own
account, over the real API — and the transcript is rendered from the engine's own
event log.

Design: `docs/DESIGN_agentic_playtests.md`. Tasks: `docs/TASKS_agentic_playtests.md`.

## The rule everything follows from

> The agent decides. The engine resolves. The agent narrates what it was told.

An agent's only mechanical output is a tool call. It does not know a result until
a tool returns one, and `validate.find_confabulations` fails the run if any agent
free-text claims a dice value, total, outcome label, or Condition the event log
does not contain for that beat.

This exists because playtest batch 07 produced a corpus of numbers that described
nothing — the narrative dice were written by a language model, and the rolls that
*were* resolved on the server were counted four times each. See DESIGN §1.

## Modules

| Module | Does |
|---|---|
| `client.py` | Accounts, connections, and the MM **observer socket** that is the sole source of the event log |
| `verbs.py` | The agent-callable surface; every verb is a real message on the caller's own socket |
| `tools_schema.py` | Anthropic tool definitions, one per verb, `strict: true` |
| `personas.py` | Archetypes (Laws 2002) and private agendas — what makes it a table |
| `context.py` | The cached shared prefix, generated from `facet.yaml` so it cannot drift |
| `agents.py` | The MM and player agents |
| `run.py` | Turn order, fan-out, budget ceilings, session assembly |
| `events.py` | The append-only log |
| `transcript.py` | Renders the log; agent text is quoted, never interpreted |
| `validate.py` | Confabulation check and batch dice-distribution check |
| `metrics.py` | Behavioural measures — spotlight, idle streaks, proposal-length trend |
| `debrief.py` | Forced-choice / forced-negative post-session survey |
| `judge.py` | Blind comparative judgement, both orderings |
| `scenarios.py` | The two scenarios, the party, and the enemy stat lines — all transcribed from canon |
| `rehearsal.py` | A scripted no-model client — the free wiring check |
| `cli.py` | `rehearse` / `pilot` / `batch` / `analyse`, and the throwaway server they run against |

## Running

Needs `ANTHROPIC_API_KEY` and `pip install anthropic websockets`. The CLI starts
its own server on a free port with its own data directory, so nothing needs to be
running first and no existing session data is touched.

```bash
cd software
python -m tools.agentic_playtest.cli pilot --arm A --seed 1
```

**Run `rehearse` first — it is free and needs no API key.** It plays the real
scenario, the real party, and the real server with a scripted stand-in for the
model, so anything that would break the pilot on *wiring* rather than on
judgement breaks here at zero cost:

```bash
python -m tools.agentic_playtest.cli rehearse
```

It has already paid for itself: it found that the transcript renderer matched
event kinds the server never broadcasts (so no die roll would have appeared in
any transcript), that `say_ooc` and `describe_scene` logged every utterance
twice, that speech raced its own echo and vanished from the log, and that
`spawn_enemy` renamed enemies to `"None"`.

**Then run `pilot`, and read the transcript.** That is the cost gate (TASKS
T4.2): one short session, capped at 12 beats, reporting wall-clock and token
spend before a batch is worth authorising. Then:

```bash
python -m tools.agentic_playtest.cli batch --sessions-per-arm 8
python -m tools.agentic_playtest.cli analyse
```

`batch` pairs every (scenario, seed) across both arms so the comparison is
within-pair. `analyse` runs the batch-level dice check first — **if that fails,
no number from the batch means anything** — then judges each pair blind in both
orderings, discarding any pair whose preference flips with the order.

## Tests

`tests/test_agentic_playtest.py` — 84 tests, no API key required. The three that
matter most:

- `TestConfabulationValidator::test_rejects_the_real_batch_07_line` — a verbatim
  line from `session_log_01.md` must be rejected.
- `TestDiceDistribution::test_the_batch_07_dice_fail` — the real batch-07 dice
  sequence must fail chi-square (it contains no 1s at all).
- `TestObserverDoesNotAlias` — four players rolling must produce four events with
  four distinct results.

`TestScenarioCanon` pins every scenario stat line to its `enemies/*.fof` and every
character to its `characters/*.fof`, so the experiment cannot be silently retuned
by a scenario file drifting from canon.

`TestTranscriptRendersWhatTheServerSends::test_every_rendered_kind_is_a_type_the_server_broadcasts`
reads the `manager.broadcast` calls out of `app/api/websocket.py` and fails if
`transcript.py` branches on any kind that is not among them. A renderer branch for
an event nothing emits is dead code that reads as coverage.
