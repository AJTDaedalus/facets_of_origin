"""The verbs agents may call, each one a real message on that agent's own socket.

Every verb here sends over the caller's authenticated connection and waits for
the engine's broadcast on the MM observer socket. Nothing in this module decides
a mechanical outcome; if a verb looks like it is computing something, that is a
bug.

Permission is the server's job, not this module's. A player agent calling
`land_enemy_attack` sends `apply_condition` on a player token, the server answers
`Unknown event type`, and the agent gets a `TableRuling` back. We do not
pre-check — the point of playing on the real tool is that the real boundary is
the one under test.
"""
from __future__ import annotations

from typing import Any

from tools.agentic_playtest.client import (
    OOC_TAG,
    RULING_TAG,
    SCENE_TAG,
    LiveTable,
    TableRuling,
)

#: Sentinel for `_act(match_actor=...)`. `None` means "any actor"; omitting the
#: argument means "match the caller". They are different, and conflating them
#: made every MM-side verb wait forever on a broadcast keyed to "MM".
_CALLER = object()


class Verbs:
    """Bound to one LiveTable; dispatches by actor identity."""

    def __init__(self, table: LiveTable) -> None:
        self.table = table

    def _send(self, actor: str, payload: dict) -> None:
        connection = self.table.connections.get(actor)
        if connection is None:
            raise TableRuling(f"'{actor}' is not connected to this table.")
        connection.send(payload)

    def _act(self, actor: str, payload: dict, *await_kinds: str,
             match_actor: Any = _CALLER, timeout: float = 10.0) -> dict:
        """Send on the caller's socket, wait for the engine's broadcast.

        Errors are sent to the *acting* socket rather than broadcast, so this
        watches the caller's own inbox alongside the observer. That is how a
        player agent calling an MM verb surfaces as a TableRuling: the server
        refuses on the player's connection and nothing is ever broadcast.
        """
        self._send(actor, payload)
        who = actor if match_actor is _CALLER else match_actor
        return self.table.await_broadcast(
            *await_kinds, timeout=timeout, actor=who,
            also_watch=self.table.connections.get(actor),
        )

    # ------------------------------------------------------------------
    # Talking (no mechanics)
    # ------------------------------------------------------------------

    def _speak(self, actor: str, text: str) -> dict:
        """Send a chat line and wait for the server to echo it back.

        Speech must wait like every other verb. `pump()` only drains what has
        already arrived, so a fire-and-forget send raced the echo and dropped
        lines from the transcript — silently, and more often the later in a turn
        they were sent.
        """
        self._act(actor, {"type": "chat", "text": text}, "chat")
        return {"ok": True}

    def say(self, actor: str, text: str) -> dict:
        return self._speak(actor, text)

    def say_ooc(self, actor: str, text: str) -> dict:
        """Table talk. Logged separately so the OOC:IC ratio is measurable —
        a transcript with no out-of-character content is not a table.

        Sent tagged and *not* appended locally: the server echoes every chat
        message back to the observer socket, so appending here too would log one
        utterance twice — once as OOC and once as in-character speech, which is
        precisely the ratio this verb exists to measure. `LiveTable._record`
        reads the tag.
        """
        return self._speak(actor, f"{OOC_TAG}{text}")

    def describe_scene(self, actor: str, text: str) -> dict:
        """MM narration. Tagged for the same reason as `say_ooc`."""
        return self._speak(actor, f"{SCENE_TAG}{text}")

    def rule_it(self, actor: str, question: str, ruling: str) -> dict:
        """The MM had to invent a rule. One of the most valuable outputs of a
        run: it marks exactly where the PHB is silent or unclear.

        The structured event is appended here because the server has no concept
        of a rules gap; the echoed chat is tagged so `_record` drops it rather
        than logging the same ruling a second time as speech.
        """
        self.table.log.append("rules_gap", actor, question=question, ruling=ruling)
        return self._speak(actor, f"{RULING_TAG}{question} — {ruling}")

    def end_scene(self, actor: str, summary: str) -> dict:
        self.table.log.append("scene_ended", actor, summary=summary)
        return {"ok": True}

    # ------------------------------------------------------------------
    # Rolling
    # ------------------------------------------------------------------

    def roll_skill(self, actor: str, attribute_id: str, skill_id: str | None = None,
                   difficulty: str = "Standard", sparks_spent: int = 0,
                   description: str = "") -> dict:
        message = self._act(actor, {
            "type": "roll", "attribute_id": attribute_id, "skill_id": skill_id,
            "difficulty": difficulty, "sparks_spent": sparks_spent,
            "description": description,
        }, "roll_result")
        return message["roll"]

    def saving_throw(self, actor: str, major_attribute_id: str,
                     difficulty: str = "Standard", sparks_spent: int = 0) -> dict:
        message = self._act(actor, {
            "type": "saving_throw", "major_attribute_id": major_attribute_id,
            "difficulty": difficulty, "sparks_spent": sparks_spent,
        }, "saving_throw_result")
        return message["roll"]

    def cast(self, actor: str, domain_id: str, scope: str, intent: str,
             spark_use: str | None = None) -> dict:
        message = self._act(actor, {
            "type": "cast", "domain_id": domain_id, "scope": scope,
            "intent": intent, "spark_use": spark_use,
        }, "cast_result")
        return message["roll"]

    # ------------------------------------------------------------------
    # Combat — player side
    # ------------------------------------------------------------------

    def declare_posture(self, actor: str, posture: str) -> dict:
        # posture_declared is sent only to the declaring socket, so this one
        # verb reads its own connection rather than the observer.
        self._send(actor, {"type": "declare_posture", "posture": posture})
        connection = self.table.connections[actor]
        import time
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            for message in connection.drain():
                if message.get("type") == "error":
                    raise TableRuling(message["message"])
                if message.get("type") == "posture_declared":
                    self.table.log.append("posture_declared", actor,
                                          posture=message["posture"])
                    return {"posture": message["posture"]}
            time.sleep(0.05)
        raise TimeoutError("posture not acknowledged")

    def strike(self, actor: str, target: str, attribute_id: str,
               skill_id: str | None = None, difficulty: str = "Standard",
               press: bool = False, sparks_spent: int = 0) -> dict:
        message = self._act(actor, {
            "type": "strike", "target": target, "attribute_id": attribute_id,
            "skill_id": skill_id, "difficulty": difficulty, "press": press,
            "sparks_spent": sparks_spent,
        }, "strike_result")
        return {"roll": message["roll"], "target": message.get("target"),
                "endurance_remaining": message.get("endurance_remaining")}

    def react(self, actor: str, reaction: str, difficulty: str = "Standard") -> dict:
        message = self._act(actor, {
            "type": "react", "reaction": reaction, "difficulty": difficulty,
        }, "react_result")
        return {"reaction": message["reaction"], "endurance_cost": message["endurance_cost"],
                "endurance_remaining": message["endurance_remaining"],
                "roll": message.get("roll")}

    def support(self, actor: str, target: str, bonus_type: str, attribute_id: str,
                skill_id: str | None = None) -> dict:
        message = self._act(actor, {
            "type": "support", "target": target, "bonus_type": bonus_type,
            "attribute_id": attribute_id, "skill_id": skill_id,
        }, "support_result")
        return {"roll": message["roll"], "target": message.get("target")}

    def maneuver(self, actor: str, target: str, attribute_id: str, description: str,
                 skill_id: str | None = None) -> dict:
        message = self._act(actor, {
            "type": "maneuver", "target": target, "attribute_id": attribute_id,
            "skill_id": skill_id, "description": description,
        }, "maneuver_result")
        return {"roll": message["roll"], "target": message.get("target")}

    def nominate_for_spark(self, actor: str, player_name: str) -> dict:
        self._send(actor, {"type": "spark_earn_peer", "player_name": player_name})
        return {"ok": True}

    def claim_graceful_fail(self, actor: str) -> dict:
        self._send(actor, {"type": "claim_graceful_fail"})
        return {"ok": True}

    def spend_skill_point(self, actor: str, skill_id: str) -> dict:
        message = self._act(actor, {"type": "spend_skill_point", "skill_id": skill_id},
                            "skill_point_spent")
        return {k: v for k, v in message.items() if k != "type"}

    def select_technique(self, actor: str, technique_id: str,
                         choice: str | None = None) -> dict:
        message = self._act(actor, {"type": "technique_select",
                                    "technique_id": technique_id, "choice": choice},
                            "technique_selected")
        return {k: v for k, v in message.items() if k != "type"}

    # ------------------------------------------------------------------
    # Combat — MM side. Enemies never roll (PHB III.3).
    # ------------------------------------------------------------------

    def start_combat(self, actor: str) -> dict:
        message = self._act(actor, {"type": "combat_start"}, "combat_started",
                            match_actor=None)
        return {"characters": message.get("characters", {})}

    def reveal_postures(self, actor: str) -> dict:
        message = self._act(actor, {"type": "reveal_postures"}, "postures_revealed",
                            match_actor=None)
        return {"postures": message.get("postures", {})}

    def land_enemy_attack(self, actor: str, target_player: str, condition: str,
                          reaction_downgraded: bool = False) -> dict:
        message = self._act(actor, {
            "type": "apply_condition", "player_name": target_player,
            "condition": condition, "reaction_downgraded": reaction_downgraded,
        }, "condition_applied", match_actor=None)
        return {"condition_applied": message.get("condition"),
                "armor_absorbed": message.get("armor_absorbed", False),
                "all_conditions": message.get("all_conditions", [])}

    def clear_condition(self, actor: str, target_player: str, condition: str) -> dict:
        message = self._act(actor, {"type": "clear_condition",
                                    "player_name": target_player, "condition": condition},
                            "condition_cleared", match_actor=None)
        return {"all_conditions": message.get("all_conditions", [])}

    def end_exchange(self, actor: str) -> dict:
        message = self._act(actor, {"type": "end_exchange"}, "exchange_ended",
                            match_actor=None)
        return {"characters": message.get("characters", {})}

    def end_combat(self, actor: str) -> dict:
        message = self._act(actor, {"type": "combat_end"}, "combat_ended",
                            match_actor=None)
        return {"ok": True}

    def spawn_enemy(self, actor: str, enemy_id: str,
                    instance_name: str | None = None) -> dict:
        payload = {"type": "spawn_enemy", "enemy_id": enemy_id}
        if instance_name:
            payload["instance_name"] = instance_name
        message = self._act(actor, payload, "enemy_spawned", match_actor=None)
        return {"tracker_key": message["tracker_key"], "tr": message.get("tr"),
                "enemy": message.get("enemy", {})}

    def apply_strike_to_enemy(self, actor: str, tracker_key: str, outcome: str) -> dict:
        """Send the Strike *outcome*; the engine applies the D1 depletion rule."""
        message = self._act(actor, {"type": "enemy_strike", "tracker_key": tracker_key,
                                    "outcome": outcome},
                            "enemy_updated", match_actor=None)
        return {"resolve": message.get("resolve_current"),
                "depletion": message.get("depletion"),
                "defeated": message.get("defeated", False)}

    def award_spark(self, actor: str, player_name: str, reason: str) -> dict:
        message = self._act(actor, {"type": "spark_earn", "player_name": player_name,
                                    "reason": reason}, "spark_earned", match_actor=None)
        return {"sparks_now": message.get("sparks_now")}

    def open_act_break(self, actor: str) -> dict:
        self._send(actor, {"type": "act_break"})
        return {"ok": True}

    def mark_skill_used(self, actor: str, player_name: str, skill_id: str) -> dict:
        message = self._act(actor, {"type": "mark_skill_used",
                                    "player_name": player_name, "skill_id": skill_id},
                            "skill_marked_used", match_actor=None)
        return {"skills_used": message.get("skills_used", [])}

    def create_clock(self, actor: str, name: str, segments: int | None = None) -> dict:
        payload: dict[str, Any] = {"type": "clock_create", "name": name}
        if segments:
            payload["segments"] = segments
        message = self._act(actor, payload, "clock_created", match_actor=None)
        return {"clock_id": message["clock"]["id"], "name": message["clock"]["name"],
                "segments": message["clock"]["segments"]}

    def advance_clock(self, actor: str, clock_id: str, outcome_tier: str) -> dict:
        message = self._act(actor, {"type": "clock_advance", "clock_id": clock_id,
                                    "outcome_tier": outcome_tier},
                            "clock_advanced", match_actor=None)
        clock = message["clock"]
        return {"filled_segments": clock["filled_segments"],
                "segments": clock["segments"], "is_full": clock["is_full"]}

    def table_roll(self, actor: str, notation: str, label: str = "") -> dict:
        message = self._act(actor, {"type": "table_roll", "notation": notation,
                                    "label": label}, "table_roll_result",
                            match_actor=None)
        return {"dice": message["dice"], "total": message["total"],
                "notation": message["notation"]}


#: Verbs a player agent may call. Anything else is refused by the server.
PLAYER_VERBS = (
    "say", "say_ooc", "roll_skill", "saving_throw", "cast", "declare_posture",
    "strike", "react", "support", "maneuver", "nominate_for_spark",
    "claim_graceful_fail", "spend_skill_point", "select_technique",
)

#: Verbs the MM agent may call. Note the absence of any roll verb for NPCs:
#: enemies never roll, so an enemy attack is `land_enemy_attack`.
MM_VERBS = (
    "say", "say_ooc", "describe_scene", "rule_it", "end_scene", "start_combat",
    "reveal_postures", "land_enemy_attack", "clear_condition", "end_exchange",
    "end_combat", "spawn_enemy", "apply_strike_to_enemy", "award_spark",
    "open_act_break", "mark_skill_used", "create_clock", "advance_clock",
    "table_roll", "select_technique",
)
