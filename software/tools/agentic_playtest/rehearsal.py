"""A no-model client that runs the whole harness for free.

Every wiring fault the pilot could hit — a scenario stat line the server rejects,
a verb whose arguments changed, a broadcast that never arrives — is a fault this
finds without spending a token. The pilot is the *quality* gate; this is the
gate before it, and it costs nothing to run twice.

The rehearsal deliberately does not stub the server. Agents still hold real
accounts, the engine still rolls the dice, and the transcript and validator still
run over the real event log. The only thing replaced is the model's judgement.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class _Block:
    name: str
    input: dict
    type: str = "tool_use"
    id: str = "stub"


@dataclass
class _Response:
    content: list
    stop_reason: str = "end_turn"
    usage: Any = None


class ScriptedClient:
    """Returns canned tool calls, one scripted turn per agent invocation.

    Agents are told apart by the tool set they were handed rather than by name,
    because the orchestrator does not pass a name into the API call.
    """

    def __init__(self, script: dict[str, list]) -> None:
        self.script = {k: list(v) for k, v in script.items()}
        self.calls = 0

    class _Messages:
        def __init__(self, outer: "ScriptedClient") -> None:
            self.outer = outer

        def create(self, *, system, messages, tools, **kwargs):
            self.outer.calls += 1
            names = {t["name"] for t in tools}
            key = "MM" if "land_enemy_attack" in names else "player"
            queue = self.outer.script.get(key, [])
            if not queue:
                return _Response([])
            name, tool_input = queue.pop(0)
            return _Response([_Block(name, tool_input)])

    @property
    def messages(self):
        return self._Messages(self)


def rehearsal_script(enemy_id: str, first_player: str) -> dict[str, list]:
    """A turn sequence that touches every part of the loop that can break.

    Scene description, an enemy spawned from the scenario's own stat line, a
    posture, a skill roll, a strike resolved against the enemy's Resolve, an
    enemy attack landing a Condition, and the exchange closing. If the pilot
    would fail on wiring, it fails here first.
    """
    return {
        "MM": [
            ("describe_scene", {"text": "The chamber is cold and the dust has "
                                        "not settled."}),
            # No instance_name: the server uses it to rename the instance
            # ("Thug A"), which would hide the canonical name in the transcript.
            ("spawn_enemy", {"enemy_id": enemy_id}),
            ("start_combat", {}),
            ("reveal_postures", {}),
            ("land_enemy_attack", {"target_player": first_player,
                                   "condition": "winded"}),
            ("end_exchange", {}),
            ("end_scene", {"summary": "The rehearsal ends here."}),
        ],
        "player": [
            ("say", {"text": "I move up where I can see it."}),
            ("declare_posture", {"posture": "measured"}),
            ("roll_skill", {"attribute_id": "wisdom", "skill_id": "insight",
                            "difficulty": "Standard"}),
            ("say_ooc", {"text": "Checking I've read that right."}),
        ],
    }
