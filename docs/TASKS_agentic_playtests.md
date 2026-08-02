# Agentic Playtests — Tasks

Read `docs/DESIGN_agentic_playtests.md` first. Tasks are ordered; each is 20–60
minutes of Worker time. **Stop and report after each task.**

New code lives in `software/tools/agentic_playtest/`. Tests live in
`software/tests/test_agentic_playtest.py` unless noted.

Dependency: `anthropic` (add to `requirements-dev.txt` as an optional extra — the
main suite must still run without it, same pattern as `playwright` in
`tests/e2e/test_ui_flows.py`).

## Status — 2026-07-31

| Wave | State |
|---|---|
| 0 | Done. Batch-07 report carries its caveat banner; the two broken runners are archived under `playtest/07_oraga_night_playtests/runner_archive/` with deprecation headers. |
| 1 | Done, **re-scoped**: `table.py` was deleted. Agents play on a live server over real WebSockets, so the verbs are messages on each agent's own socket rather than calls into an in-process `GameSession`. T1.1's "no rule logic in this module" acceptance is satisfied more strongly — the module cannot contain rule logic, because the server resolves everything. |
| 2 | Done. |
| 3 | Done. |
| 4 | **T4.1 done** — scenario pack built and the fourth seat (Ilesse) approved 2026-07-31 as a *playtest fixture only*, deliberately not given a `characters/*.fof`. T4.2–T4.5 need API credits: the key authenticates, the account balance is zero, and a Max plan does not include API usage. Everything up to the API boundary is written and tested. |

84 harness tests pass without an API key.

### A gate before the gate — `rehearse`

T4.2 costs money, so `cli.py rehearse` runs the real scenario, party, and server
with a scripted stand-in for the model. It found five defects the pilot would
otherwise have hit *after* paying:

1. `transcript.py` matched event kinds (`roll`, `strike`, `enemy_attack`) the
   server never broadcasts — **no die roll would have appeared in any
   transcript**, the one artifact the whole experiment produces.
2. `say_ooc` and `describe_scene` appended locally *and* were echoed by the
   server: one utterance, two events. The batch-07 over-count in a new place,
   landing directly on the OOC:IC metric.
3. Speech was fire-and-forget and raced its own echo, so lines vanished from the
   log — more often the later in a turn they were sent.
4. `spawn_enemy` sent `instance_name: null`, which the server stringified to
   `"None"` and used to rename the enemy. Fixed on both sides.
5. `city_watch_sergeant`'s stat line in `scenarios.py` had drifted from its
   `.fof`. `TestScenarioCanon` now pins every stat line and every PC.

**Run order:**

```bash
cd software
python -m tools.agentic_playtest.cli rehearse                     # free
python -m tools.agentic_playtest.host --scenario guardian_chamber  # subagent path
python -m tools.agentic_playtest.cli pilot --arm A --seed 1        # T4.2 GATE
```

### The subagent path — half of T4.2, without the API

`host.py` + `broker.py` + `play_as.py` let Claude Code subagents play at a real
table through the shell. Same server, same verbs, same observer socket, same
validator — only the model layer changes. It **cannot** measure cost (subagents
report no token usage), so it answers the qualitative half of the gate and leaves
the budgeting half open.

Run 2026-07-31: `playtest/08_npc_variance/subagent_session/report.md`.
**Validator found zero confabulated mechanics**, and the transcript reads like a
table — players refused hooks, refused each other, and raised two design
complaints unprompted. Four findings, of which F1 is the important one: PHB
III.3:112 restricts Strike to Combat/Finesse by range while the engine accepts any
pairing, which misbuilds a monk-adjacent character. That is a live Software-PHB
desync and is worth fixing independently of Wave 4.

---

## Wave 0 — Contain the damage from the old corpus

### T0.1 — Mark the playtest 07 numbers as unverified
**Files:** `playtest/07_oraga_night_playtests/playtest_report.md`,
`research/simulation_log.md`
**Do:** Add a header block to the report recording the two defects found
(confabulated narrative dice; 4× broadcast over-count in the runner) with the
evidence from DESIGN §1. Do not delete the report — the qualitative MM
observations may survive. Cross-reference from `simulation_log.md` if any of its
numbers derive from batch 07.
**Acceptance:** Anyone reading the report sees the caveat before the statistics.
No numbers silently retained as valid.

### T0.2 — Fix or retire the broken runners
**Files:** `software/tools/run_oraga_night_playtests.py`, `..._v2.py`
**Do:** These are untracked working files. Either fix the `read_until` aliasing bug
(read each player's own broadcast by matching `player` in the payload) or delete
them in favour of the new harness. Recommend delete — the new harness supersedes
them and a half-fixed runner invites reuse.
**Acceptance:** No script remains that can silently over-count rolls 4×.
**Ask the user first** — these are their working files, not the audit's.

---

## Wave 1 — The table adapter (mechanics, no agents)

### T1.1 — `TableAdapter` skeleton and event log
**Files:** `tools/agentic_playtest/table.py`, `tools/agentic_playtest/events.py`
**Do:** A class that owns a `GameSession`, exposes the mechanical verbs the agents
will need, and appends one structured event per mechanical fact to a JSONL log.
Verbs (first pass): `roll_skill`, `saving_throw`, `declare_posture`,
`reveal_postures`, `strike`, `react`, `support`, `maneuver`, `cast`,
`land_enemy_attack`, `clear_condition`, `end_exchange`, `spawn_enemy`,
`deplete_resolve`, `award_spark`, `spend_skill_point`.
Every verb calls into `app/game/*` — **no rule logic in this module.**
**Acceptance:** ≥3 tests per verb (happy path, edge, error). A test asserts the
module contains no dice arithmetic and no outcome-tier comparison.

### T1.2 — Deterministic seeding
**Files:** `tools/agentic_playtest/table.py`
**Do:** Seed the RNG per session so a replayed event log reproduces identical
mechanical outcomes.
**Acceptance:** Test: same seed + same verb sequence → identical event log.

### T1.3 — Transcript renderer
**Files:** `tools/agentic_playtest/transcript.py`
**Do:** Render a human-readable Markdown transcript **from the event log plus agent
free-text**, never from agent-authored mechanics. Mechanical lines are rendered by
this module from events.
**Acceptance:** Test: an event log with a roll of 4 renders "4"; there is no code
path by which agent text can supply a die value.

### T1.4 — The anti-confabulation validator
**Files:** `tools/agentic_playtest/validate.py`
**Do:** Scan agent free-text for mechanical claims — dice pairs, `NdN` totals,
outcome labels ("Full Success", "Things Go Wrong"), Condition IDs from `facet.yaml`
— and fail the run if any claim has no corresponding event in that beat's log.
**Acceptance:** Test using a real line from `playtest/07_*/session_log_01.md`
("**Roll:** 2d6 (2, 3) + 2 = **7**") — the validator must reject it. This is the
regression test for the entire class of bug in DESIGN §1.

### T1.5 — Dice distribution check
**Files:** `tools/agentic_playtest/validate.py`
**Do:** Chi-square goodness-of-fit of all logged 2d6 results against the true
distribution, across a batch.
**Acceptance:** Test: the playtest-07 dice sequence fails; a real `random` 2d6
sequence of the same length passes.

---

## Wave 2 — Agents

### T2.1 — Tool schemas
**Files:** `tools/agentic_playtest/tools_schema.py`
**Do:** One Anthropic tool definition per `TableAdapter` verb, plus non-mechanical
verbs: `say` (in character), `say_ooc`, `ask_mm`, `describe_scene` (MM only),
`rule_it` (MM only — logs a rules gap), `end_scene` (MM only).
Use `strict: true` and prescriptive descriptions that state *when* to call each.
**Acceptance:** Every `TableAdapter` verb has a schema; a test asserts the two sets
match so a verb can't be added without exposing it.

### T2.2 — Shared prefix builder + prompt caching
**Files:** `tools/agentic_playtest/context.py`
**Do:** Build the stable prefix — ruleset digest from `facet.yaml`, relevant PHB/MM
sections, scenario, cast — with a `cache_control` breakpoint at its end. Volatile
content (beat number, recent events) goes strictly after.
**Acceptance:** Test asserts the prefix is byte-identical across two builds with the
same inputs (no timestamps, sorted keys). Pilot run asserts
`usage.cache_read_input_tokens > 0` on turn 2+.

### T2.3 — Player agent
**Files:** `tools/agentic_playtest/agents/player.py`,
`tools/agentic_playtest/personas.py`
**Do:** System prompt carrying: character sheet, **private agenda**, **archetype**
(DESIGN §3.2), and the explicit permission to refuse hooks and to speak OOC. Seven
archetypes; agendas as a sampleable pool.
**Acceptance:** Three tests: the agenda never appears in any tool call visible to
the MM; a player can emit `say_ooc`; a player presented with a hook it dislikes
declines at least once across five scripted probes.

### T2.4 — MM agent
**Files:** `tools/agentic_playtest/agents/mm.py`
**Do:** System prompt carrying prep (scene, front, NPCs, clock), the *prep is
disposable* instruction, the rules context, and `rule_it` for gaps. Enemy attacks
land via `land_enemy_attack` — the MM never rolls.
**Acceptance:** Tests: the MM has no roll verb in its tool set; `rule_it` writes a
rules-gap entry; the MM abandons prep when players go elsewhere (one scripted probe).

### T2.5 — Orchestrator
**Files:** `tools/agentic_playtest/run.py`
**Do:** Turn order, spotlight rotation, beat counter, per-session turn cap and token
budget with hard abort, event logging, transcript + metrics output.
**Acceptance:** Tests: budget abort produces a valid partial session; a session
runs end to end against a stub agent that returns canned tool calls (no API cost in
CI).

---

## Wave 3 — Measurement

### T3.1 — Behavioural metrics
**Files:** `tools/agentic_playtest/metrics.py`
**Do:** Compute the DESIGN §4.1 table from the event log: spotlight share, longest
idle streak, decision:roll ratio, proposal-length trend, lateral solution rate,
callback rate, OOC:IC ratio, zero-dice exchanges, rules gaps, rule violations.
**Acceptance:** ≥3 tests per metric against hand-built logs with known values.
Proposal-length trend specifically: a log with shrinking proposals must report a
negative trend.

### T3.2 — Debrief survey
**Files:** `tools/agentic_playtest/debrief.py`
**Do:** Post-session, out-of-character, **forced-choice and forced-negative only**
(DESIGN §4.2), via `output_config.format` with a Pydantic schema.
**Acceptance:** Test asserts the schema contains no absolute rating field — a
1–10 "was it fun" question must be impossible to add without failing the test.

### T3.3 — Blind comparative judge
**Files:** `tools/agentic_playtest/judge.py`
**Do:** Take two transcripts, strip arm labels and any variant tell, present in both
orders to a fresh agent, force a choice with a reason.
**Acceptance:** Tests: labels are stripped (fed a labelled transcript, the prompt
contains no label); both orderings are run; a tie/"both good" response is rejected
and re-prompted.

---

## Wave 4 — Run it

### T4.1 — Scenario pack
**Files:** `playtest/08_npc_variance/scenario.md`, `characters.md`
**Do:** Two scenarios — one combat-heavy, one social-heavy with an opt-in fight —
and a fixed 4-character party spanning Body/Mind/Soul. **Reuse existing canon**
(`characters/*.fof`, an existing adventure) rather than inventing setting material;
per `CLAUDE.md` the iron law is no invented canon.
**Acceptance:** User confirms the scenario introduces no new canonical facts.

### T4.2 — Instrumented pilot (1 session) — **GATE**
**Do:** One full session, Arm A. Measure wall-clock, token spend, cache hit rate,
and read the transcript end to end.
**Acceptance:** All five DESIGN §8 criteria pass on this single session; measured
cost per session recorded. **Report to the user with the cost figure and a
transcript excerpt before proceeding to T4.3.** If cost or quality is off, revise
before spending the batch.

### T4.3 — Batch run
**Do:** 8 sessions per arm, paired on (scenario, party, seed). Players not told the
arm.
**Acceptance:** Batch-level dice distribution passes T1.5. No validator failures.
Partial sessions recorded, not silently dropped.

### T4.4 — Analysis
**Files:** `playtest/08_npc_variance/report.md`
**Do:** Write up against the **pre-registered predictions in DESIGN §5** — including
the ones that failed. Include the §7 limits verbatim. Recommend on Q1/Q2.
**Acceptance:** Every prediction is addressed. No claim of statistical significance.
Anything actionable is stated as "check with humans", not "finding".

### T4.5 — Propagate
**Files:** `research/dice_system_analysis.md`, `docs/DECISIONS.md`, and — only if
the result changes a rule — `facet.yaml`, PHB, MM Manual, and every quick reference,
in one commit per the Software-PHB sync rule.
**Acceptance:** If no rule changes, the research doc's open question is updated with
the evidence and closed. If a rule changes, the sync checklist in `CLAUDE.md` is
satisfied in full.

---

## Sequencing

```
T0.1 ─┐
T0.2 ─┴─> T1.1 → T1.2 → T1.3 → T1.4 → T1.5 ─┐
                                             ├─> T2.1 → T2.2 → T2.3 → T2.4 → T2.5 ─┐
                                                                                    ├─> T3.1 → T3.2 → T3.3 ─┐
                                                                                                             ├─> T4.1 → T4.2 [GATE] → T4.3 → T4.4 → T4.5
```

Wave 1 is worth doing even if the rest is deferred: T1.4 and T1.5 alone would have
caught the playtest-07 defect, and they are useful against any future harness.
