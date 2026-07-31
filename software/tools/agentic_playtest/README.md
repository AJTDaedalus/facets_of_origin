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

## Running

Needs a running server and `ANTHROPIC_API_KEY` (or `ant auth login`):

```bash
pip install anthropic websockets
python run.py &                       # the app under test
python -m tools.agentic_playtest.cli pilot --arm A --seed 1
```

`cli.py --help` lists the batch and analysis commands.

## Tests

`tests/test_agentic_playtest.py` — 63 tests, no API key required. The three that
matter most:

- `TestConfabulationValidator::test_rejects_the_real_batch_07_line` — a verbatim
  line from `session_log_01.md` must be rejected.
- `TestDiceDistribution::test_the_batch_07_dice_fail` — the real batch-07 dice
  sequence must fail chi-square (it contains no 1s at all).
- `TestObserverDoesNotAlias` — four players rolling must produce four events with
  four distinct results.
