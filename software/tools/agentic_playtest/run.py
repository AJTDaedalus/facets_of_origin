"""Run one session.

Turn order rotates the spotlight: the MM opens a beat, each player takes a turn,
the MM responds. Everything any agent does is fanned out to every other agent, so
they are all watching the same table.

Two hard limits, because a runaway agentic loop is the main cost risk: a beat cap
and a token budget. Hitting either ends the session cleanly and records a partial
run rather than burning the budget silently.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from tools.agentic_playtest.agents import Agent, Usage, make_mm, make_player
from tools.agentic_playtest.client import LiveTable, TableRuling
from tools.agentic_playtest.context import build_shared_prefix
from tools.agentic_playtest.personas import Persona, assign
from tools.agentic_playtest.transcript import render, render_event
from tools.agentic_playtest.validate import find_confabulations
from tools.agentic_playtest.verbs import Verbs


@dataclass
class Budget:
    """Hard ceilings. A partial session is a result; an unbounded one is a bill."""

    max_beats: int = 30
    max_output_tokens: int = 250_000
    spent_output: int = 0
    stopped_because: str | None = None

    def spend(self, agents: list[Agent]) -> None:
        self.spent_output = sum(a.usage.output_tokens for a in agents)

    def exhausted(self, beat: int) -> str | None:
        if beat >= self.max_beats:
            return f"beat cap ({self.max_beats}) reached"
        if self.spent_output >= self.max_output_tokens:
            return f"token budget ({self.max_output_tokens}) reached"
        return None


@dataclass
class SessionResult:
    session_id: str
    arm: str
    seed: int
    beats: int
    usage: dict[str, Usage]
    stopped_because: str | None
    transcript: str
    validation_ok: bool
    validation_report: str
    rules_gaps: list[dict] = field(default_factory=list)

    def write(self, directory: Path, name: str) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{name}.md").write_text(self.transcript, encoding="utf-8")
        (directory / f"{name}.summary.json").write_text(json.dumps({
            "session_id": self.session_id, "arm": self.arm, "seed": self.seed,
            "beats": self.beats, "stopped_because": self.stopped_because,
            "validation_ok": self.validation_ok,
            "validation_report": self.validation_report,
            "rules_gaps": self.rules_gaps,
            "usage": {k: vars(v) for k, v in self.usage.items()},
        }, indent=2), encoding="utf-8")


class Session:
    """One playtest session on a live server."""

    def __init__(self, table: LiveTable, mm: Agent, players: list[Agent],
                 budget: Budget | None = None) -> None:
        self.table = table
        self.verbs = Verbs(table)
        self.mm = mm
        self.players = players
        self.budget = budget or Budget()
        self.agents = [mm] + players

    # ------------------------------------------------------------------

    def _dispatch_for(self, actor: str) -> Callable[[str, dict], Any]:
        """Bind an agent's tool calls to its own connection.

        The actor is fixed here, not taken from the tool input — an agent cannot
        act as somebody else by naming them.
        """
        def dispatch(tool_name: str, tool_input: dict) -> Any:
            method = getattr(self.verbs, tool_name, None)
            if method is None:
                raise TableRuling(f"No such action '{tool_name}'.")
            return method(actor, **tool_input)
        return dispatch

    def _broadcast(self, speaker: str, calls: list[tuple[str, dict, Any]]) -> None:
        """Show every other agent what just happened.

        Rendered from the event log where possible, so what an agent sees is what
        the transcript will say — the same discipline applied one layer up.
        """
        if not calls:
            return
        lines = []
        for tool_name, tool_input, result in calls:
            if tool_name == "__refusal__":
                continue
            if tool_name in ("say", "describe_scene"):
                lines.append(f"{speaker}: {tool_input.get('text', '')}")
            elif tool_name == "say_ooc":
                lines.append(f"({speaker}, out of character): {tool_input.get('text', '')}")
            elif tool_name == "rule_it":
                lines.append(f"[MM ruling] {tool_input.get('question')} — "
                             f"{tool_input.get('ruling')}")
            elif isinstance(result, dict) and "refused" in result:
                lines.append(f"[{speaker} tried {tool_name}; the rules said: "
                             f"{result['refused']}]")
            else:
                lines.append(f"[{speaker} used {tool_name}] "
                             f"{json.dumps(result, default=str)[:400]}")

        text = "\n".join(lines)
        for agent in self.agents:
            if agent.name != speaker:
                agent.observe(text)

    def _take(self, agent: Agent) -> None:
        calls = agent.take_turn(self._dispatch_for(agent.name))
        self._broadcast(agent.name, calls)
        self.table.pump()

    # ------------------------------------------------------------------

    def play(self) -> SessionResult:
        beat = 0
        self.mm.observe(
            "The session is starting. Open the scene: describe where the "
            "characters are and what is in front of them, then ask what they do."
        )

        while True:
            self.budget.spend(self.agents)
            reason = self.budget.exhausted(beat)
            if reason:
                self.budget.stopped_because = reason
                break

            self.table.log.next_beat()
            beat += 1

            self._take(self.mm)
            for player in self.players:
                self._take(player)

        # Give the MM a closing beat so the session ends rather than stopping.
        self.table.log.next_beat()
        self.mm.observe(
            "Wrap the session up: close the current scene, then open an act break "
            "so the players can nominate each other for Sparks."
        )
        self._take(self.mm)

        return self._result()

    def _result(self) -> SessionResult:
        report = find_confabulations(self.table.log, self._ruleset())
        gaps = [e.data for e in self.table.log.of_kind("rules_gap")]
        return SessionResult(
            session_id=self.table.session_id,
            arm=self.table.log.arm,
            seed=self.table.log.seed or 0,
            beats=self.table.log.beat,
            usage={a.name: a.usage for a in self.agents},
            stopped_because=self.budget.stopped_because,
            transcript=render(self.table.log,
                              title=f"Playtest — arm {self.table.log.arm}"),
            validation_ok=report.ok,
            validation_report=str(report),
            rules_gaps=gaps,
        )

    def _ruleset(self):
        from app.facets.registry import build_ruleset
        return build_ruleset([])


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def build_session(
    client: Any,
    base_url: str,
    mm_token: str,
    scenario: str,
    prep: str,
    cast_blurb: str,
    party: list[dict],
    enemies: list[dict],
    seed: int,
    arm: str = "A",
    session_name: str = "agentic playtest",
    budget: Budget | None = None,
) -> Session:
    """Wire a live table, its agents, and their accounts together.

    `party` entries are dicts of player_name, character_name, primary_facet,
    attributes, and optionally background_id / magic_domain.
    """
    from app.facets.registry import build_ruleset

    table = LiveTable(base_url, None, session_name, arm=arm, seed=seed,
                      mm_token=mm_token)
    prefix = build_shared_prefix(build_ruleset([]), scenario, cast_blurb)

    for enemy in enemies:
        table.add_enemy(enemy)

    personas = assign([(p["player_name"], p["character_name"]) for p in party], seed)

    players: list[Agent] = []
    for spec, persona in zip(party, personas):
        table.join_as_player(spec["player_name"])
        character = table.create_character(
            spec["player_name"], spec["character_name"], spec["primary_facet"],
            spec["attributes"], spec.get("background_id"), spec.get("magic_domain"),
        )
        players.append(make_player(client, persona, prefix, _sheet(character)))

    mm = make_mm(client, prefix, prep)
    return Session(table, mm, players, budget)


def _sheet(character: dict) -> str:
    attrs = ", ".join(f"{k} {v}" for k, v in sorted(character["attributes"].items()))
    skills = ", ".join(
        f"{sid} ({s['rank']}, {s['marks']} marks)"
        for sid, s in sorted(character["skills"].items())
        if s["rank"] != "novice" or s["marks"]
    ) or "all Novice"
    lines = [
        f"{character['name']} — {character['primary_facet'].title()} Facet, "
        f"level {character['facet_level']}",
        f"Attributes: {attrs}",
        f"Skills above baseline: {skills}",
        f"Sparks: {character['sparks']} · Skill Points this session: "
        f"{character['session_skill_points_remaining']}",
    ]
    if character.get("background_id"):
        lines.append(f"Background: {character['background_id']}")
    if character.get("specialty"):
        lines.append(f"Specialty: {character['specialty']}")
    if character.get("magic_domain"):
        active = "" if character.get("magic_technique_active") else " (pre-Technique: Minor scope only)"
        lines.append(f"Magic domain: {character['magic_domain']}{active}")
    return "\n".join(lines)
