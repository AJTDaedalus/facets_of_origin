"""Stand up a table for subagents to play at, and write everyone's briefing.

This is the no-API path. The agents are Claude Code subagents driving
`play_as.py` through the shell rather than SDK agents calling tools, so the
model layer is replaced but nothing below it is: same server, same verbs, same
observer socket, same event log, same validator.

What it cannot do is measure cost — subagents do not report token usage — so it
answers the qualitative half of the T4.2 gate ("does this read like a table?")
and not the budgeting half. See docs/TASKS_agentic_playtests.md.
"""
from __future__ import annotations

import json
import signal
import sys
import threading
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parents[2]
if str(SOFTWARE_DIR) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_DIR))

from tools.agentic_playtest.broker import Broker, serve  # noqa: E402
from tools.agentic_playtest.cli import MM_PASSWORD, AppServer  # noqa: E402
from tools.agentic_playtest.client import LiveTable, login_mm  # noqa: E402
from tools.agentic_playtest.context import build_shared_prefix  # noqa: E402
from tools.agentic_playtest.personas import assign  # noqa: E402
from tools.agentic_playtest.play_as import ENDPOINT_FILE  # noqa: E402
from tools.agentic_playtest.run import _sheet  # noqa: E402
from tools.agentic_playtest.scenarios import CAST_BLURB, PARTY, SCENARIOS  # noqa: E402
from tools.agentic_playtest.verbs import MM_VERBS, PLAYER_VERBS  # noqa: E402

HOW_TO_ACT = """\
## How you act at this table

You act by running shell commands. Nothing else you write reaches the table.

```
cd {software}
python -m tools.agentic_playtest.play_as {actor} state
python -m tools.agentic_playtest.play_as {actor} <verb> '<json args>'
```

`state` shows your sheet, everyone's conditions, the live enemies, and the last
few things that happened. Run it whenever you are unsure.

**You never decide an outcome.** You ask for one and read what comes back. If you
want to know whether you hit, roll and look at the answer. Writing "I rolled a 9"
in prose is meaningless here — the transcript is built from the engine's log, not
from anything you say, and a claim with no roll behind it is flagged as a defect.

If a command prints `REFUSED:`, the rules said no. Read why, and choose again.

Your verbs: {verbs}

Speak in character with `say`. Speak as yourself, at the table, with `say_ooc` —
use it: real tables talk out of character constantly, and a transcript with none
of that is not a table.
"""

PLAYER_BRIEF = """\
# You are {player}, playing {character}

{persona}

## Your character sheet

{sheet}

{how_to_act}

## Your turn

Take your turn when the session host tells you to. A turn is usually one to four
commands: say something, do something, react to what just happened.

Do not narrate what other people's characters do. Do not resolve your own action's
consequences — the MM does that.

You are allowed to refuse a hook, argue with the plan, do something the MM did not
expect, or spend a turn on something that does not advance the plot. A table where
everyone always cooperates is not a table.
"""

MM_BRIEF = """\
# You are the Mirror Master

You run this session. The players are {players}.

{how_to_act}

## Your prep

{prep}

**Prep is disposable.** If the players go somewhere else, follow them. Do not
steer them back.

## Running it

Enemies never roll. When an enemy hits someone, you call `land_enemy_attack` with
the Condition it inflicts — a Mook lands Tier 1, a Named NPC or Boss lands Tier 2.
The player's reaction and armour are applied by the engine, not by you.

When a player's Strike lands on an enemy, call `apply_strike_to_enemy` with the
outcome tier and the engine decides what it costs the enemy.

If the rules do not cover something, call `rule_it`, say what you decided, and
move on. Those rulings are among the most valuable things this session produces —
each one marks a place the rulebook is silent.

Give everyone something to do. If a player has been quiet, turn to them.
"""


def build(scenario_key: str, seed: int, out_dir: Path) -> dict:
    """Start the server and the table, write the briefings, serve the broker."""
    scenario = SCENARIOS[scenario_key]
    app = AppServer().__enter__()
    token = login_mm(app.base_url, MM_PASSWORD)

    table = LiveTable(app.base_url, None, f"subagent-{scenario_key}",
                      arm="A", seed=seed, mm_token=token)
    for enemy in scenario.enemies:
        table.add_enemy(enemy)

    personas = assign([(p["player_name"], p["character_name"]) for p in PARTY], seed)
    prefix = build_shared_prefix(_ruleset(), scenario.briefing, CAST_BLURB)

    out_dir.mkdir(parents=True, exist_ok=True)
    briefs = out_dir / "briefings"
    briefs.mkdir(exist_ok=True)

    for spec, persona in zip(PARTY, personas):
        table.join_as_player(spec["player_name"])
        character = table.create_character(
            spec["player_name"], spec["character_name"], spec["primary_facet"],
            spec["attributes"], spec.get("background_id"), spec.get("magic_domain"))
        (briefs / f"{spec['player_name']}.md").write_text(
            prefix + "\n\n" + PLAYER_BRIEF.format(
                player=spec["player_name"], character=spec["character_name"],
                persona=persona.describe_for_self(), sheet=_sheet(character),
                how_to_act=HOW_TO_ACT.format(
                    software=SOFTWARE_DIR, actor=spec["player_name"],
                    verbs=", ".join(sorted(PLAYER_VERBS)))),
            encoding="utf-8")

    (briefs / "MM.md").write_text(
        prefix + "\n\n" + MM_BRIEF.format(
            players=", ".join(p["player_name"] for p in PARTY),
            prep=scenario.prep,
            how_to_act=HOW_TO_ACT.format(software=SOFTWARE_DIR, actor="MM",
                                         verbs=", ".join(sorted(MM_VERBS)))),
        encoding="utf-8")

    broker = Broker(table, out_dir, PARTY)
    server = serve(broker)
    ENDPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    ENDPOINT_FILE.write_text(json.dumps({
        "url": f"http://127.0.0.1:{server.server_address[1]}",
        "session_id": table.session_id, "scenario": scenario_key,
        "briefings": str(briefs), "out_dir": str(out_dir),
    }, indent=2), encoding="utf-8")

    return {"app": app, "table": table, "broker": broker, "server": server}


def _ruleset():
    from app.facets.registry import build_ruleset
    return build_ruleset([])


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="guardian_chamber")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--out", default=str(
        SOFTWARE_DIR.parent / "playtest" / "08_npc_variance" / "subagent_session"))
    args = parser.parse_args()

    parts = build(args.scenario, args.seed, Path(args.out))
    endpoint = json.loads(ENDPOINT_FILE.read_text(encoding="utf-8"))
    print(json.dumps(endpoint, indent=2), flush=True)
    print("Table open. Briefings written. POST /finish to close it.", flush=True)

    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    try:
        parts["server"].serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        parts["table"].close()
        parts["app"].__exit__(None, None, None)
        ENDPOINT_FILE.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
