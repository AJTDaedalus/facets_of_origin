"""The agents: one MM, N players, each driving its own connection.

An agent's only mechanical output is a tool call. It is told, in the shared
prefix and again in its role block, that it does not know a result until a tool
returns one. `validate.find_confabulations` enforces that after the fact — the
instruction is guidance, the validator is the guarantee.

Model choice: `claude-opus-5` throughout. Cheaper models produce flatter table
talk, and table talk is the axis under test. Effort is the cost lever instead —
`high` for the MM, who improvises and adjudicates, `medium` for players.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from tools.agentic_playtest.context import SessionContext
from tools.agentic_playtest.personas import Persona
from tools.agentic_playtest.tools_schema import mm_tools, player_tools

MODEL = "claude-opus-5"


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0

    def add(self, usage: Any) -> None:
        self.input_tokens += getattr(usage, "input_tokens", 0) or 0
        self.output_tokens += getattr(usage, "output_tokens", 0) or 0
        self.cache_read += getattr(usage, "cache_read_input_tokens", 0) or 0
        self.cache_write += getattr(usage, "cache_creation_input_tokens", 0) or 0

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_read + self.cache_write + self.input_tokens
        return self.cache_read / total if total else 0.0


class Agent:
    """One participant. Holds its own message history and its own tool set."""

    def __init__(self, client: Any, name: str, context: SessionContext,
                 tools: list[dict], effort: str = "medium",
                 max_tokens: int = 4096) -> None:
        self.client = client
        self.name = name
        self.context = context
        self.tools = tools
        self.effort = effort
        self.max_tokens = max_tokens
        self.messages: list[dict] = []
        self.usage = Usage()

    def observe(self, text: str) -> None:
        """Add something that happened at the table to this agent's view.

        Consecutive observations are merged into one user turn — the API allows
        consecutive same-role messages, but merging keeps the history compact and
        keeps the cached prefix stable for longer.
        """
        if self.messages and self.messages[-1]["role"] == "user" \
                and isinstance(self.messages[-1]["content"], str):
            self.messages[-1]["content"] += "\n" + text
        else:
            self.messages.append({"role": "user", "content": text})

    def take_turn(self, dispatch: Callable[[str, dict], Any],
                  max_tool_calls: int = 6) -> list[tuple[str, dict, Any]]:
        """One turn: think, call tools, see results, stop.

        Returns the (tool_name, input, result) triples so the orchestrator can
        broadcast them to the other agents. The loop is written out rather than
        using the SDK tool runner because each result has to be fanned out to the
        rest of the table before the next agent moves.
        """
        if not self.messages:
            self.observe("It's your turn.")

        calls: list[tuple[str, dict, Any]] = []
        for _ in range(max_tool_calls):
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=self.max_tokens,
                system=self.context.system_blocks(),
                messages=self.messages,
                tools=self.tools,
                output_config={"effort": self.effort},
            )
            self.usage.add(response.usage)
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "refusal":
                # Safety classifiers declined. Record and end the turn rather
                # than retrying into the same wall.
                calls.append(("__refusal__", {}, {
                    "category": getattr(response.stop_details, "category", None)}))
                return calls

            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if not tool_uses:
                return calls

            results = []
            for block in tool_uses:
                try:
                    result = dispatch(block.name, dict(block.input))
                    is_error = False
                except Exception as e:  # TableRuling and anything the server refused
                    result, is_error = {"refused": str(e)}, True
                calls.append((block.name, dict(block.input), result))
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, default=str),
                    "is_error": is_error,
                })
            self.messages.append({"role": "user", "content": results})

        return calls


PLAYER_ROLE = """\
{persona}

**Your character sheet**
{sheet}

You are one player among several. Take short turns. You do not have to act every
time it comes round to you — reacting to what someone else just did, asking the
MM a question, or making a joke are all real turns.

You are **not required to follow the MM's hook**. If your character wouldn't do
it, don't. If the party is heading somewhere you find boring, say so and try to
steer. Disagreeing with the other players is fine and normal.

When you attempt something risky, call the tool — do not narrate the outcome.
You genuinely do not know whether you succeed until the tool answers.
"""

MM_ROLE = """\
You are the Mirror Master. Your job is to reflect the spotlight back onto the
players and keep them the stars of their own story.

**Your prep for tonight**
{prep}

**Prep is disposable.** If the players go somewhere you didn't plan, follow them.
Do not steer them back. A scene you improvise because they surprised you is worth
more than the one you wrote.

**Enemies never roll.** When an enemy attacks, call `land_enemy_attack` with the
Condition it lands — a Mook's at Tier 1, a Named NPC's or Boss's at Tier 2. When
a player's Strike hits, call `apply_strike_to_enemy` with the outcome they rolled
and let the engine decide what it costs.

**If the rules don't cover something, rule it and move on** — call `rule_it` to
say what you decided. Do not stall looking for a rule that may not exist. Those
rulings are one of the most valuable things this session produces.

Give every player something to do. If someone has been quiet for a while, turn
to them. Ask players what their characters do rather than telling them.
"""


def make_player(client: Any, persona: Persona, context_prefix: str,
                sheet: str, effort: str = "medium") -> Agent:
    context = SessionContext(
        shared_prefix=context_prefix,
        role_block=PLAYER_ROLE.format(persona=persona.describe_for_self(), sheet=sheet),
    )
    return Agent(client, persona.player_name, context, player_tools(), effort=effort)


def make_mm(client: Any, context_prefix: str, prep: str,
            effort: str = "high") -> Agent:
    context = SessionContext(
        shared_prefix=context_prefix,
        role_block=MM_ROLE.format(prep=prep.strip()),
    )
    return Agent(client, "MM", context, mm_tools(), effort=effort, max_tokens=6144)
