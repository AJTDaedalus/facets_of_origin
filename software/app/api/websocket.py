"""WebSocket connection manager and event dispatcher."""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError

from app.auth.tokens import decode_token
from app.game import combat as combat_module
from app.game.engine import RollRequest, resolve_roll, resolve_magic_roll, roll_result_to_dict
from app.game.session import ThreatClock, session_store

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Tracks active WebSocket connections per session."""

    def __init__(self) -> None:
        # session_id -> list of (websocket, player_name | "mm")
        self._connections: dict[str, list[tuple[WebSocket, str]]] = {}

    async def connect(self, websocket: WebSocket, session_id: str, identity: str) -> None:
        await websocket.accept()
        if session_id not in self._connections:
            self._connections[session_id] = []
        self._connections[session_id].append((websocket, identity))
        logger.info("WS connected: %s in session %s", identity, session_id)

    def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        connections = self._connections.get(session_id, [])
        self._connections[session_id] = [(ws, ident) for ws, ident in connections if ws is not websocket]

    async def broadcast(self, session_id: str, message: dict) -> None:
        """Send a message to all connections in a session."""
        dead: list[WebSocket] = []
        for ws, _ in self._connections.get(session_id, []):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, session_id)

    async def send_to(self, websocket: WebSocket, message: dict) -> bool:
        """Send a message to a single WebSocket. Returns True on success, False on failure."""
        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            logger.warning("Failed to send to websocket: %s", e)
            return False


manager = ConnectionManager()

# Maximum allowed WebSocket message size in bytes (M-03).
WS_MAX_MESSAGE_BYTES = 8_192
# Seconds to wait for the auth message before closing unauthenticated connections (L-03).
WS_AUTH_TIMEOUT_SECONDS = 30


async def handle_websocket(websocket: WebSocket) -> None:
    """Main WebSocket handler — authentication then event loop."""
    session_id: str | None = None
    identity: str = "unknown"

    try:
        # Step 1: Authenticate via token in the first message
        # (Not in the URL query string — avoids logging the token)
        await websocket.accept()

        # L-03: close unauthenticated connections that never send their auth message.
        try:
            auth_text = await asyncio.wait_for(
                websocket.receive_text(), timeout=WS_AUTH_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            await websocket.send_json({"type": "error", "message": "Authentication timeout."})
            await websocket.close(code=1008)
            return

        # M-03: enforce message size on the auth message too.
        if len(auth_text) > WS_MAX_MESSAGE_BYTES:
            await websocket.send_json({"type": "error", "message": "Message too large."})
            await websocket.close(code=1009)
            return

        try:
            auth_msg = json.loads(auth_text)
        except (json.JSONDecodeError, ValueError):
            await websocket.send_json({"type": "error", "message": "Invalid JSON."})
            await websocket.close(code=1008)
            return

        token = auth_msg.get("token", "")
        try:
            token_data = decode_token(token)
        except JWTError as e:
            await websocket.send_json({"type": "error", "message": f"Authentication failed: {e}"})
            await websocket.close(code=1008)
            return

        session_id = token_data.session_id if token_data.role == "player" else auth_msg.get("session_id")
        if not session_id:
            await websocket.send_json({"type": "error", "message": "Missing session_id."})
            await websocket.close(code=1008)
            return

        session = session_store.get(session_id)
        if not session:
            await websocket.send_json({"type": "error", "message": "Session not found."})
            await websocket.close(code=1008)
            return

        identity = "mm" if token_data.is_mm else (token_data.player_name or "player")

        # Register connection (already accepted above)
        if session_id not in manager._connections:
            manager._connections[session_id] = []
        manager._connections[session_id].append((websocket, identity))

        # Send initial state
        if token_data.is_mm:
            await manager.send_to(websocket, {"type": "state", "data": session.to_state_dict()})
        else:
            await manager.send_to(websocket, {"type": "state", "data": session.to_player_state_dict(identity)})

        # Announce join to all
        await manager.broadcast(session_id, {"type": "player_joined", "player": identity})

        # Step 2: Event loop — enforce message size on every incoming message (M-03).
        while True:
            text = await websocket.receive_text()
            if len(text) > WS_MAX_MESSAGE_BYTES:
                await manager.send_to(websocket, {"type": "error", "message": "Message too large."})
                continue
            try:
                raw = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                await manager.send_to(websocket, {"type": "error", "message": "Invalid JSON."})
                continue
            await _dispatch(websocket, raw, session_id, identity, token_data.is_mm)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.exception("Unexpected WS error for %s: %s", identity, e)
    finally:
        if session_id:
            manager.disconnect(websocket, session_id)
            await manager.broadcast(session_id, {"type": "player_left", "player": identity})


async def _dispatch(
    websocket: WebSocket,
    msg: dict,
    session_id: str,
    identity: str,
    is_mm: bool,
) -> None:
    """Route an incoming WebSocket message to the appropriate handler."""
    event_type = msg.get("type")
    session = session_store.get(session_id)
    if not session:
        return

    if event_type == "roll":
        await _handle_roll(websocket, msg, session, session_id, identity)
    elif event_type == "spark_earn" and is_mm:
        await _handle_spark_earn(msg, session, session_id)
    elif event_type == "spark_earn_peer":
        await _handle_spark_earn_peer(msg, session, session_id, identity)
    elif event_type == "chat":
        await _handle_chat(msg, session_id, identity)
    elif event_type == "skill_advance" and is_mm:
        await _handle_skill_advance(msg, session, session_id)
    elif event_type == "mark_skill_used" and is_mm:
        await _handle_mark_skill_used(msg, session, session_id)
    elif event_type == "ping":
        await manager.send_to(websocket, {"type": "pong"})
    # --- Combat events ---
    elif event_type == "combat_start" and is_mm:
        await _handle_combat_start(msg, session, session_id)
    elif event_type == "declare_posture":
        await _handle_declare_posture(websocket, msg, session, session_id, identity)
    elif event_type == "reveal_postures" and is_mm:
        await _handle_reveal_postures(session, session_id)
    elif event_type == "strike":
        await _handle_strike(websocket, msg, session, session_id, identity)
    elif event_type == "react":
        await _handle_react(websocket, msg, session, session_id, identity)
    elif event_type == "apply_condition" and is_mm:
        await _handle_apply_condition(msg, session, session_id)
    elif event_type == "clear_condition" and is_mm:
        await _handle_clear_condition(msg, session, session_id)
    elif event_type == "end_exchange" and is_mm:
        await _handle_end_exchange(session, session_id)
    elif event_type == "combat_end" and is_mm:
        await _handle_combat_end(session, session_id)
    elif event_type == "support":
        await _handle_support(websocket, msg, session, session_id, identity)
    elif event_type == "maneuver":
        await _handle_maneuver(websocket, msg, session, session_id, identity)
    # --- Magic events ---
    elif event_type == "cast":
        await _handle_cast(websocket, msg, session, session_id, identity)
    # --- Contested roll ---
    elif event_type == "contested_roll" and is_mm:
        await _handle_contested_roll(websocket, msg, session, session_id)
    # --- Player skill spending ---
    elif event_type == "spend_skill_point":
        await _handle_spend_skill_point(websocket, msg, session, session_id, identity)
    # --- Technique events ---
    elif event_type == "technique_select" and is_mm:
        await _handle_technique_select(msg, session, session_id)
    elif event_type == "session_reset" and is_mm:
        await _handle_session_reset(session, session_id)
    # --- Enemy tracker events ---
    elif event_type == "spawn_enemy" and is_mm:
        await _handle_spawn_enemy(msg, session, session_id)
    elif event_type == "enemy_update" and is_mm:
        await _handle_enemy_update(msg, session, session_id)
    elif event_type == "remove_enemy" and is_mm:
        await _handle_remove_enemy(msg, session, session_id)
    # --- Threat Clock events (D4, PHB III.2) ---
    elif event_type == "clock_create" and is_mm:
        await _handle_clock_create(msg, session, session_id)
    elif event_type == "clock_advance" and is_mm:
        await _handle_clock_advance(msg, session, session_id)
    elif event_type == "clock_wind_back" and is_mm:
        await _handle_clock_wind_back(msg, session, session_id)
    # --- Spark: Act Break Nomination / Graceful Fail (D6) ---
    elif event_type == "act_break" and is_mm:
        await _handle_act_break(msg, session, session_id)
    elif event_type == "claim_graceful_fail":
        await _handle_claim_graceful_fail(msg, session, session_id, identity)
    else:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown event type: {event_type}"})


def _spend_sparks(character, count: int) -> int:
    """Spend up to `count` Sparks from character, returning the amount actually spent."""
    actual = min(count, character.sparks)
    for _ in range(actual):
        character.spend_spark()
    return actual


def _build_roll_request(character, msg: dict, ruleset, *, press: bool = False) -> RollRequest:
    """Build a RollRequest from a WebSocket message and character state."""
    attribute_id = msg.get("attribute_id", "strength")
    skill_id = msg.get("skill_id")
    return RollRequest(
        attribute_id=attribute_id,
        attribute_rating=character.attributes.get(attribute_id, 2),
        skill_id=skill_id,
        skill_rank_id=character.skills[skill_id].rank if skill_id and skill_id in character.skills else None,
        difficulty_label=str(msg.get("difficulty", "Standard")),
        sparks_spent=0,  # sparks are tracked separately via _spend_sparks
        press=press,
        description=str(msg.get("description", ""))[:200],
    )


async def _handle_roll(
    websocket: WebSocket,
    msg: dict,
    session,
    session_id: str,
    identity: str,
) -> None:
    """Resolve a dice roll request from a player."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found for this player."})
        return

    attribute_id = msg.get("attribute_id", "")
    sparks_requested = int(msg.get("sparks_spent", 0))

    # Validate attribute exists in character
    if attribute_id not in character.attributes:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown attribute '{attribute_id}'."})
        return

    sparks_to_spend = _spend_sparks(character, sparks_requested)
    request = RollRequest(
        attribute_id=attribute_id,
        attribute_rating=character.attributes[attribute_id],
        skill_id=msg.get("skill_id"),
        skill_rank_id=character.skills[msg["skill_id"]].rank if msg.get("skill_id") and msg["skill_id"] in character.skills else None,
        difficulty_label=msg.get("difficulty", "Standard"),
        sparks_spent=sparks_to_spend,
        description=str(msg.get("description", ""))[:200],
    )

    result = resolve_roll(request, session.ruleset)
    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name, result_dict)

    # Auto-mark skill as used this session (PHB II.4 advancement rule)
    used_skill = msg.get("skill_id")
    if used_skill and used_skill in character.skills:
        character.skills_used_this_session.add(used_skill)

    # Broadcast the roll result to everyone in the session
    await manager.broadcast(session_id, {
        "type": "roll_result",
        "player": player_name,
        "character_name": character.name,
        "roll": result_dict,
        "character_sparks_remaining": character.sparks,
    })


async def _handle_spark_earn(msg: dict, session, session_id: str) -> None:
    """MM awards a Spark to a player."""
    player_name = msg.get("player_name", "")
    reason = str(msg.get("reason", "MM award"))[:200]
    character = session.characters.get(player_name)
    if character:
        character.earn_spark()
        await manager.broadcast(session_id, {
            "type": "spark_earned",
            "player": player_name,
            "reason": reason,
            "sparks_now": character.sparks,
        })


async def _handle_spark_earn_peer(msg: dict, session, session_id: str, caller: str) -> None:
    """Any player calls 'Spark?' for another player. MM must confirm."""
    target_player = msg.get("player_name", "")
    await manager.broadcast(session_id, {
        "type": "spark_nomination",
        "nominated_by": caller,
        "player": target_player,
        "message": f"{caller} nominated {target_player} for a Spark — MM to confirm.",
    })


async def _handle_act_break(msg: dict, session, session_id: str) -> None:
    """MM opens an Act Break Nomination window after a major scene transition."""
    await manager.broadcast(session_id, {
        "type": "act_break_opened",
        "message": "Act break — nominate a player for something they did this scene.",
    })


async def _handle_claim_graceful_fail(msg: dict, session, session_id: str, caller: str) -> None:
    """Player-initiated Graceful Fail (D6): on any 6-, the player may claim it
    by narrating how they make the failure worse or richer. Mirrors the
    `spark_earn_peer` nomination shape — broadcasts a claim, MM confirms
    separately with `spark_earn`.
    """
    last_roll = None
    for entry in reversed(session.roll_log):
        if entry.get("player_name") == caller:
            last_roll = entry
            break

    if not last_roll or last_roll.get("outcome") != "failure":
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"{caller} has no unclaimed 6- roll to claim a Graceful Fail on.",
        })
        return

    if last_roll.get("graceful_fail_claimed"):
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"{caller} already claimed a Graceful Fail on that roll.",
        })
        return

    last_roll["graceful_fail_claimed"] = True
    await manager.broadcast(session_id, {
        "type": "graceful_fail_claimed",
        "player": caller,
        "message": f"{caller} claims a Graceful Fail — MM to confirm.",
    })


async def _handle_chat(msg: dict, session_id: str, identity: str) -> None:
    text = str(msg.get("text", ""))[:2000].strip()
    if text:
        await manager.broadcast(session_id, {
            "type": "chat",
            "from": identity,
            "text": text,
        })


async def _handle_skill_advance(msg: dict, session, session_id: str) -> None:
    """MM triggers end-of-session skill advancement for a player."""
    player_name = msg.get("player_name", "")
    skill_id = msg.get("skill_id", "")
    marks = int(msg.get("marks", 0))
    character = session.characters.get(player_name)
    if character and skill_id and marks > 0:
        # Determine SP cost and check remaining budget
        sk_def = session.ruleset.get_skill(skill_id)
        is_primary = sk_def is not None and sk_def.facet == character.primary_facet
        cost_context = "primary_facet" if is_primary else "cross_facet"
        sp_cost = session.ruleset.get_skill_point_cost(cost_context)
        if character.session_skill_points_remaining < sp_cost:
            await manager.broadcast(session_id, {
                "type": "error",
                "message": f"Insufficient skill points: need {sp_cost}, have {character.session_skill_points_remaining}.",
            })
            return
        character.session_skill_points_remaining -= sp_cost
        result = character.advance_skill(skill_id, marks, session.ruleset)
        await manager.broadcast(session_id, {
            "type": "skill_advanced",
            "player": player_name,
            "skill_id": skill_id,
            "marks_added": marks,
            "rank_advances": result["rank_advances"],
            "facet_level_advances": result["facet_level_advances"],
            "major_advancement": result.get("major_advancement", False),
            "new_rank": character.skills[skill_id].rank if skill_id in character.skills else "novice",
            "new_facet_level": character.facet_level,
            "total_facet_levels": character.total_facet_levels,
            "career_advances": character.career_advances,
        })


async def _handle_mark_skill_used(msg: dict, session, session_id: str) -> None:
    """MM marks a skill as used this session for a player, enabling advancement."""
    player_name = msg.get("player_name", "")
    skill_id = msg.get("skill_id", "")
    character = session.characters.get(player_name)
    if character and skill_id:
        character.skills_used_this_session.add(skill_id)
        await manager.broadcast(session_id, {
            "type": "skill_marked_used",
            "player": player_name,
            "skill_id": skill_id,
            "skills_used": sorted(character.skills_used_this_session),
        })


# ---------------------------------------------------------------------------
# Combat handlers
# ---------------------------------------------------------------------------

async def _handle_combat_start(msg: dict, session, session_id: str) -> None:
    """MM initialises combat. Sets all characters' endurance_current = endurance_max.

    Armor's per-scene downgrade budget (D2) is initialised here only if it
    isn't already set — a second `combat_start` within the same scene (a
    second fight) must not top the budget back up; it resets only at end of
    scene. See `combat.armor_budget`.
    """
    state: dict = {}
    for player_name, character in session.characters.items():
        character.endurance_current = character.endurance_max(session.ruleset)
        character.conditions = []
        character.posture = "measured"
        if character.armor and character.armor_downgrades_remaining is None:
            character.armor_downgrades_remaining = combat_module.armor_budget(
                character.armor, session.ruleset,
            )
        state[player_name] = {
            "endurance_current": character.endurance_current,
            "endurance_max": character.endurance_current,
            "conditions": [],
            "posture": "measured",
        }
    await manager.broadcast(session_id, {"type": "combat_started", "characters": state})


async def _handle_declare_posture(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Character declares their posture for this exchange. Stored but not broadcast."""
    player_name = identity
    character = session.characters.get(player_name)
    posture = msg.get("posture", "measured")
    valid_postures = {"aggressive", "measured", "defensive", "withdrawn"}
    if character and posture in valid_postures:
        character.posture = posture
        await manager.send_to(websocket, {"type": "posture_declared", "posture": posture})
    else:
        await manager.send_to(websocket, {"type": "error", "message": f"Invalid posture '{posture}'."})


async def _handle_reveal_postures(session, session_id: str) -> None:
    """MM reveals all postures simultaneously."""
    postures = {
        player_name: (character.posture or "measured")
        for player_name, character in session.characters.items()
    }
    await manager.broadcast(session_id, {"type": "postures_revealed", "postures": postures})


async def _handle_strike(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Character attempts a Strike. Resolves roll and broadcasts result."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    if character.endurance_current is None:
        await manager.send_to(websocket, {"type": "error", "message": "Not in combat."})
        return

    if character.posture == "withdrawn":
        await manager.send_to(websocket, {"type": "error", "message": "Cannot Strike from Withdrawn posture."})
        return

    press = bool(msg.get("press", False))
    sparks_requested = int(msg.get("sparks_spent", 0))
    difficulty = str(msg.get("difficulty", "Standard"))
    target_name = str(msg.get("target", ""))

    # Press costs 1 Endurance
    if press:
        if character.endurance_current is not None and character.endurance_current > 0:
            character.endurance_current -= 1
        else:
            await manager.send_to(websocket, {"type": "error", "message": "No Endurance to Press."})
            return

    sparks_to_spend = _spend_sparks(character, sparks_requested)

    # Accept attribute/skill from client; default to strength/combat for backward compat
    attribute_id = str(msg.get("attribute_id", "strength"))
    skill_id = msg.get("skill_id", "combat")

    # Validate attribute exists on character
    if attribute_id not in character.attributes:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown attribute '{attribute_id}'."})
        return

    # Posture offense modifier plus any Condition penalty (Staggered −1, PHB III.3).
    # Both come from combat.offense_modifier so this path and the simulator's
    # resolve_strike cannot drift apart again.
    offense_mod = combat_module.offense_modifier(
        character.posture or "measured", character.conditions, session.ruleset,
    ) or 0

    request = RollRequest(
        attribute_id=attribute_id,
        attribute_rating=character.attributes.get(attribute_id, 2),
        skill_id=skill_id,
        skill_rank_id=character.skills[skill_id].rank if skill_id and skill_id in character.skills else None,
        difficulty_label=difficulty,
        sparks_spent=sparks_to_spend,
        press=press,
        description=str(msg.get("description", ""))[:200],
    )
    result = resolve_roll(request, session.ruleset)
    result_dict = roll_result_to_dict(result)

    # Apply posture offense modifier to total
    if offense_mod != 0:
        result_dict["offense_modifier"] = offense_mod
        result_dict["total"] += offense_mod
        # Re-evaluate outcome with adjusted total
        from app.game.engine import _determine_outcome
        outcome, label, desc = _determine_outcome(result_dict["total"], session.ruleset)
        result_dict["outcome"] = outcome
        result_dict["outcome_label"] = label
        result_dict["outcome_description"] = desc

    session.record_roll(player_name, result_dict)

    # Auto-mark skill as used this session
    if skill_id and skill_id in character.skills:
        character.skills_used_this_session.add(skill_id)

    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "strike_result",
        "attacker": player_name,
        "target": target_name,
        "roll": result_dict,
        "press_used": press,
        "posture": character.posture,
        "endurance_remaining": character.endurance_current,
        "sparks_remaining": character.sparks,
    })


async def _handle_react(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Character declares a reaction (dodge/parry/absorb/intercept)."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    if character.endurance_current is None:
        await manager.send_to(websocket, {"type": "error", "message": "Not in combat."})
        return

    reaction = str(msg.get("reaction", "absorb"))

    # PHB: 0 Endurance = Absorb only
    if character.endurance_current <= 0 and reaction != "absorb":
        await manager.send_to(websocket, {
            "type": "error",
            "message": "No Endurance remaining — only Absorb is available.",
        })
        return
    valid_reactions = {"dodge", "parry", "absorb", "intercept"}
    if reaction not in valid_reactions:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown reaction '{reaction}'."})
        return

    # Compute Endurance cost (adjust for posture). K1 (BRIEF D8): the
    # Aggressive surcharge applies only to the first reaction of the
    # exchange — see `reactions_this_exchange`'s docstring on Character.
    is_first_reaction = character.reactions_this_exchange == 0
    character.reactions_this_exchange += 1
    cost = combat_module.reaction_cost(
        reaction, character.posture or "measured", session.ruleset, is_first_reaction,
    )

    if character.endurance_current < cost:
        # Cannot pay — forced to Absorb
        reaction = "absorb"
        cost = 0

    character.endurance_current = max(0, character.endurance_current - cost)

    # Active reactions (dodge/parry) require a roll
    roll_result = None
    if reaction in ("dodge", "parry"):
        attr_id = "dexterity" if reaction == "dodge" else "strength"
        skill_id = None if reaction == "dodge" else "combat"
        request = RollRequest(
            attribute_id=attr_id,
            attribute_rating=character.attributes.get(attr_id, 2),
            skill_id=skill_id,
            skill_rank_id=character.skills[skill_id].rank if skill_id and skill_id in character.skills else None,
            difficulty_label=str(msg.get("difficulty", "Standard")),
            description=f"{reaction} reaction",
        )
        roll = resolve_roll(request, session.ruleset)
        roll_result = roll_result_to_dict(roll)
        session.record_roll(player_name, roll_result)

    # Auto-mark skill as used this session (parry uses combat skill)
    if reaction == "parry" and "combat" in character.skills:
        character.skills_used_this_session.add("combat")

    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "react_result",
        "player": player_name,
        "reaction": reaction,
        "endurance_cost": cost,
        "endurance_remaining": character.endurance_current,
        "roll": roll_result,
    })


def _reduce_incoming_condition(
    condition: str, character, ruleset, reaction_downgraded: bool = False,
) -> tuple[str, bool]:
    """Reduce an incoming condition by armor and/or a partial reaction, under
    PHB III.3's non-stacking rule (`combat.resolve_incoming_condition`).

    Returns `(condition, armor_spent)` — the condition after the single greater
    reduction, or `""` if it was reduced away entirely. `armor_spent` says
    whether an armor charge actually paid for it, so the broadcast can tell a
    player their armor absorbed the hit versus their Parry did.

    Callers pass the **raw** incoming condition and set `reaction_downgraded`
    when a Dodge/Parry already partially succeeded — they must not hand in a
    pre-downgraded condition, or armor would reduce it a second time. Updates
    `character.armor_downgrades_remaining` in place.
    """
    if not ruleset.combat:
        return condition, False

    original_tier = combat_module.condition_tier(condition, ruleset)
    if original_tier <= 0:
        return condition, False

    result = combat_module.resolve_incoming_condition(
        original_tier,
        character.armor,
        character.armor_downgrades_remaining or 0,
        ruleset,
        reaction_downgraded=reaction_downgraded,
    )
    character.armor_downgrades_remaining = result.downgrades_remaining

    if result.tier == original_tier:
        return condition, False
    if result.tier == 0:
        return "", result.armor_spent

    # Map back to a condition of the lower tier (pick first available)
    conds = ruleset.combat.conditions
    tier_map = {1: conds.tier1, 2: conds.tier2, 3: conds.tier3}
    lower_tier_conds = tier_map.get(result.tier, [])
    if lower_tier_conds:
        return lower_tier_conds[0].id, result.armor_spent
    return condition, result.armor_spent


async def _handle_apply_condition(msg: dict, session, session_id: str) -> None:
    """MM applies a condition to a character."""
    player_name = msg.get("player_name", "")
    condition = str(msg.get("condition", ""))
    character = session.characters.get(player_name)
    if not character:
        return

    # `reaction_downgraded` is set when the target's Dodge/Parry partially
    # succeeded. The MM sends the RAW incoming condition either way; armor and
    # the reaction do not stack (PHB III.3), so the engine — not the MM —
    # applies the single greater reduction. Absent the flag, behaviour is
    # exactly as before: armor alone reduces, and pays a charge for it.
    reaction_downgraded = bool(msg.get("reaction_downgraded", False))
    condition, armor_spent = _reduce_incoming_condition(
        condition, character, session.ruleset, reaction_downgraded,
    )
    if not condition:
        await manager.broadcast(session_id, {
            "type": "condition_applied",
            "player": player_name,
            "condition": None,
            "armor_absorbed": armor_spent,
            "reaction_downgraded": reaction_downgraded,
            "all_conditions": list(character.conditions),
        })
        return

    # Stacking: a second Tier 2 condition of the SAME type escalates to Broken (D5 ledger row 2).
    # A duplicate of anything below Tier 2 is a silent no-op (pre-existing engine
    # behaviour, orthogonal to the simulator's list-based semantics — see LOG WS-A0).
    tier = combat_module.condition_tier(condition, session.ruleset)
    if condition in character.conditions and tier < 2:
        pass
    else:
        result = combat_module.apply_condition(character.conditions, condition, tier, session.ruleset)
        if result.broken:
            condition = "broken"
            if condition not in character.conditions:
                character.conditions.append(condition)

    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "condition_applied",
        "player": player_name,
        "condition": condition,
        "all_conditions": list(character.conditions),
    })


async def _handle_clear_condition(msg: dict, session, session_id: str) -> None:
    """MM clears a condition from a character."""
    player_name = msg.get("player_name", "")
    condition = str(msg.get("condition", ""))
    character = session.characters.get(player_name)
    if character and condition in character.conditions:
        character.conditions.remove(condition)
    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "condition_cleared",
        "player": player_name,
        "condition": condition,
        "all_conditions": list(character.conditions) if character else [],
    })


async def _handle_end_exchange(session, session_id: str) -> None:
    """MM signals end of exchange: clear Tier 1 conditions, apply Withdrawn recovery."""
    updates: dict = {}
    for player_name, character in session.characters.items():
        if character.endurance_current is None:
            continue

        # Clear Tier 1 conditions
        cleared = combat_module.end_exchange(character.conditions, session.ruleset)

        # K1 (BRIEF D8): reset the per-exchange reaction count.
        character.reactions_this_exchange = 0

        # Withdrawn endurance recovery (only if not striking, enforced by declare_posture)
        if character.posture == "withdrawn":
            max_end = character.endurance_max(session.ruleset)
            recovery_amount = combat_module.withdrawn_recovery_amount(session.ruleset)
            character.endurance_current = min(character.endurance_current + recovery_amount, max_end)

        updates[player_name] = {
            "conditions": list(character.conditions),
            "cleared_conditions": cleared,
            "endurance_current": character.endurance_current,
        }

    for pn in updates:
        session.save_character_to_disk(pn)
    await manager.broadcast(session_id, {"type": "exchange_ended", "characters": updates})


async def _handle_combat_end(session, session_id: str) -> None:
    """MM ends combat: clear all ephemeral combat state."""
    for character in session.characters.values():
        character.endurance_current = None
        character.conditions = []
        character.posture = None
    await manager.broadcast(session_id, {"type": "combat_ended"})


# ---------------------------------------------------------------------------
# Magic handler
# ---------------------------------------------------------------------------

async def _handle_cast(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Player declares a magical action. Server resolves difficulty and rolls."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    if not character.magic_domain:
        await manager.send_to(websocket, {"type": "error", "message": "Character has no magic domain."})
        return

    domain_id = str(msg.get("domain_id", character.magic_domain))
    scope = str(msg.get("scope", "minor"))
    intent = str(msg.get("intent", ""))[:500]
    spark_use = msg.get("spark_use")

    if scope not in ("minor", "significant", "major"):
        await manager.send_to(websocket, {"type": "error", "message": f"Invalid scope '{scope}'."})
        return

    # Spend Spark if needed
    if spark_use in ("improve_roll", "ease_focused_major", "push_scope"):
        if not character.spend_spark():
            await manager.send_to(websocket, {"type": "error", "message": "No Sparks remaining."})
            return

    try:
        result = resolve_magic_roll(
            character=character,
            domain_id=domain_id,
            scope=scope,
            intent=intent,
            ruleset=session.ruleset,
            spark_use=spark_use,
        )
    except ValueError as e:
        await manager.send_to(websocket, {"type": "error", "message": str(e)})
        return

    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name, result_dict)

    await manager.broadcast(session_id, {
        "type": "cast_result",
        "player": player_name,
        "domain_id": domain_id,
        "scope": scope,
        "intent": intent,
        "technique_active": character.magic_technique_active,
        "roll": result_dict,
        "sparks_remaining": character.sparks,
    })


# ---------------------------------------------------------------------------
# Support / Maneuver handlers (2.1)
# ---------------------------------------------------------------------------

async def _handle_support(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Character uses their action to support an ally."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    if character.endurance_current is None:
        await manager.send_to(websocket, {"type": "error", "message": "Not in combat."})
        return

    target_player = str(msg.get("target", ""))
    bonus_type = str(msg.get("bonus_type", "add_die"))  # "add_die" or "ease_difficulty"

    if bonus_type not in ("add_die", "ease_difficulty"):
        await manager.send_to(websocket, {"type": "error", "message": f"Invalid bonus_type '{bonus_type}'."})
        return

    request = _build_roll_request(character, msg, session.ruleset)
    result = resolve_roll(request, session.ruleset)
    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name, result_dict)

    # Auto-mark skill as used this session
    used_skill = msg.get("skill_id")
    if used_skill and used_skill in character.skills:
        character.skills_used_this_session.add(used_skill)

    await manager.broadcast(session_id, {
        "type": "support_result",
        "player": player_name,
        "target": target_player,
        "bonus_type": bonus_type,
        "roll": result_dict,
        "outcome": result_dict["outcome"],
    })


async def _handle_maneuver(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Character uses their action to reposition, create advantage, or disarm."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    if character.endurance_current is None:
        await manager.send_to(websocket, {"type": "error", "message": "Not in combat."})
        return

    if character.posture == "withdrawn":
        await manager.send_to(websocket, {"type": "error", "message": "Cannot Maneuver from Withdrawn posture."})
        return

    target_name = str(msg.get("target", ""))

    request = _build_roll_request(character, msg, session.ruleset)
    result = resolve_roll(request, session.ruleset)
    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name, result_dict)

    # Auto-mark skill as used this session
    used_skill = msg.get("skill_id")
    if used_skill and used_skill in character.skills:
        character.skills_used_this_session.add(used_skill)

    await manager.broadcast(session_id, {
        "type": "maneuver_result",
        "player": player_name,
        "target": target_name,
        "roll": result_dict,
        "outcome": result_dict["outcome"],
    })


# ---------------------------------------------------------------------------
# Contested roll handler (2.2)
# ---------------------------------------------------------------------------

async def _handle_contested_roll(
    websocket, msg: dict, session, session_id: str,
) -> None:
    """MM triggers a contested roll between two characters."""
    player_a = str(msg.get("player_a", ""))
    player_b = str(msg.get("player_b", ""))
    char_a = session.characters.get(player_a)
    char_b = session.characters.get(player_b)

    if not char_a or not char_b:
        await manager.send_to(websocket, {"type": "error", "message": "Both players must have characters."})
        return

    attr_a = str(msg.get("attribute_a", "strength"))
    attr_b = str(msg.get("attribute_b", attr_a))
    skill_a = msg.get("skill_a")
    skill_b = msg.get("skill_b")
    difficulty = str(msg.get("difficulty", "Standard"))

    req_a = RollRequest(
        attribute_id=attr_a,
        attribute_rating=char_a.attributes.get(attr_a, 2),
        skill_id=skill_a,
        skill_rank_id=char_a.skills[skill_a].rank if skill_a and skill_a in char_a.skills else None,
        difficulty_label=difficulty,
        description=str(msg.get("description", ""))[:200],
    )
    req_b = RollRequest(
        attribute_id=attr_b,
        attribute_rating=char_b.attributes.get(attr_b, 2),
        skill_id=skill_b,
        skill_rank_id=char_b.skills[skill_b].rank if skill_b and skill_b in char_b.skills else None,
        difficulty_label=difficulty,
        description=str(msg.get("description", ""))[:200],
    )

    result_a = resolve_roll(req_a, session.ruleset)
    result_b = resolve_roll(req_b, session.ruleset)
    dict_a = roll_result_to_dict(result_a)
    dict_b = roll_result_to_dict(result_b)

    if result_a.total > result_b.total:
        winner = player_a
    elif result_b.total > result_a.total:
        winner = player_b
    else:
        winner = "tie"

    session.record_roll(player_a, dict_a)
    session.record_roll(player_b, dict_b)

    await manager.broadcast(session_id, {
        "type": "contested_roll_result",
        "player_a": player_a,
        "player_b": player_b,
        "roll_a": dict_a,
        "roll_b": dict_b,
        "winner": winner,
    })


# ---------------------------------------------------------------------------
# Player skill point spending (2.3)
# ---------------------------------------------------------------------------

async def _handle_spend_skill_point(
    websocket, msg: dict, session, session_id: str, identity: str,
) -> None:
    """Player spends a skill point to mark a skill for advancement."""
    player_name = identity
    character = session.characters.get(player_name)
    if not character:
        await manager.send_to(websocket, {"type": "error", "message": "No character found."})
        return

    skill_id = str(msg.get("skill_id", ""))
    if not skill_id:
        await manager.send_to(websocket, {"type": "error", "message": "Missing skill_id."})
        return

    # Enforce "only skills used this session" rule (PHB II.4)
    if character.skills_used_this_session and skill_id not in character.skills_used_this_session:
        await manager.send_to(websocket, {
            "type": "error",
            "message": f"Skill '{skill_id}' was not used this session. Ask the MM to mark it as used.",
        })
        return

    # Determine cost
    sk_def = session.ruleset.get_skill(skill_id)
    is_primary = sk_def is not None and sk_def.facet == character.primary_facet
    cost_context = "primary_facet" if is_primary else "cross_facet"
    sp_cost = session.ruleset.get_skill_point_cost(cost_context)

    if character.session_skill_points_remaining < sp_cost:
        await manager.send_to(websocket, {
            "type": "error",
            "message": f"Insufficient skill points: need {sp_cost}, have {character.session_skill_points_remaining}.",
        })
        return

    character.session_skill_points_remaining -= sp_cost
    result = character.advance_skill(skill_id, 1, session.ruleset)

    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "skill_point_spent",
        "player": player_name,
        "skill_id": skill_id,
        "sp_cost": sp_cost,
        "marks_added": 1,
        "rank_advances": result["rank_advances"],
        "facet_level_advances": result["facet_level_advances"],
        "major_advancement": result.get("major_advancement", False),
        "new_rank": character.skills[skill_id].rank if skill_id in character.skills else "novice",
        "new_marks": character.skills[skill_id].marks if skill_id in character.skills else 0,
        "new_facet_level": character.facet_level,
        "session_skill_points_remaining": character.session_skill_points_remaining,
    })


# ---------------------------------------------------------------------------
# Technique handler
# ---------------------------------------------------------------------------

async def _handle_technique_select(msg: dict, session, session_id: str) -> None:
    """MM selects a Technique for a character at a Facet level advancement."""
    player_name = msg.get("player_name", "")
    technique_id = str(msg.get("technique_id", ""))
    choice = msg.get("choice")  # optional, for Techniques with choices
    character = session.characters.get(player_name)
    if not character or not technique_id:
        return

    # All selection rules (already-held, prerequisites, pick budget, magic
    # activation) live in Character.select_technique — the single source of truth.
    ok, message = character.select_technique(technique_id, session.ruleset, choice)
    if not ok:
        await manager.broadcast(session_id, {"type": "error", "message": message})
        return

    session.save_character_to_disk(player_name)
    await manager.broadcast(session_id, {
        "type": "technique_selected",
        "player": player_name,
        "technique_id": technique_id,
        "choice": choice,
        "all_techniques": list(character.techniques),
        "technique_picks_available": character.technique_picks_available,
    })


async def _handle_session_reset(session, session_id: str) -> None:
    """MM signals start of new session: reset once-per-session technique tracking."""
    for character in session.characters.values():
        character.techniques_used_this_session = []
        character.sparks = session.ruleset.spark.base_sparks_per_session if session.ruleset.spark else 3
    await manager.broadcast(session_id, {"type": "session_reset"})


# ---------------------------------------------------------------------------
# Enemy tracker handlers
# ---------------------------------------------------------------------------

async def _handle_spawn_enemy(msg: dict, session, session_id: str) -> None:
    """MM spawns an enemy into the active combat tracker."""
    from app.game.enemy import Enemy

    enemy_id = str(msg.get("enemy_id", ""))
    instance_name = str(msg.get("instance_name", ""))

    # Try loading from library first
    library_enemy = session.enemy_library.get(enemy_id)
    if library_enemy:
        enemy = library_enemy.model_copy(deep=True)
        if instance_name:
            enemy.name = instance_name
    else:
        # Inline enemy data
        enemy_data = msg.get("enemy_data")
        if not enemy_data or not isinstance(enemy_data, dict):
            await manager.broadcast(session_id, {
                "type": "error",
                "message": f"Enemy '{enemy_id}' not in library and no inline data provided.",
            })
            return
        enemy = Enemy(
            id=enemy_id,
            name=enemy_data.get("name", enemy_id),
            tier=enemy_data.get("tier", "mook"),
            resolve=enemy_data.get("resolve", 0),
            attack_modifier=enemy_data.get("attack_modifier", 0),
            defense_modifier=enemy_data.get("defense_modifier", 0),
            armor=enemy_data.get("armor", "none"),
        )

    enemy.init_combat()
    tracker_key = instance_name or f"{enemy_id}_{len(session.active_enemies)}"
    session.active_enemies[tracker_key] = enemy

    await manager.broadcast(session_id, {
        "type": "enemy_spawned",
        "tracker_key": tracker_key,
        "enemy": enemy.to_client_dict(),
        "tr": enemy.calculate_tr(),
    })


async def _handle_enemy_update(msg: dict, session, session_id: str) -> None:
    """MM updates an active enemy's resolve or conditions."""
    tracker_key = str(msg.get("tracker_key", ""))
    enemy = session.active_enemies.get(tracker_key)
    if not enemy:
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"No active enemy with key '{tracker_key}'.",
        })
        return

    phase_index = None
    if "resolve_current" in msg:
        resolve_before = enemy.resolve_current
        enemy.resolve_current = max(0, int(msg["resolve_current"]))
        if resolve_before is not None and enemy.phases:
            phase_index = combat_module.phase_crossed(
                resolve_before, enemy.resolve_current,
                [p.resolve_threshold for p in enemy.phases],
            )
    if "add_condition" in msg:
        cond = str(msg["add_condition"])
        if cond and cond not in enemy.conditions:
            enemy.conditions.append(cond)
    if "remove_condition" in msg:
        cond = str(msg["remove_condition"])
        if cond in enemy.conditions:
            enemy.conditions.remove(cond)

    await manager.broadcast(session_id, {
        "type": "enemy_updated",
        "tracker_key": tracker_key,
        "resolve_current": enemy.resolve_current,
        "conditions": list(enemy.conditions),
    })

    if phase_index is not None:
        await manager.broadcast(session_id, {
            "type": "enemy_phase_change",
            "enemy_id": tracker_key,
            "phase_index": phase_index,
            "description": enemy.phases[phase_index].description,
        })


async def _handle_remove_enemy(msg: dict, session, session_id: str) -> None:
    """MM removes an enemy from the active combat tracker."""
    tracker_key = str(msg.get("tracker_key", ""))
    if tracker_key in session.active_enemies:
        del session.active_enemies[tracker_key]
    await manager.broadcast(session_id, {
        "type": "enemy_removed",
        "tracker_key": tracker_key,
    })


# ---------------------------------------------------------------------------
# Threat Clock handlers (D4, PHB III.2)
# ---------------------------------------------------------------------------

async def _handle_clock_create(msg: dict, session, session_id: str) -> None:
    """MM creates a new Threat Clock, visible to the whole table.

    Segment count defaults to `hazards.threat_clock.segments` from the
    ruleset (facet.yaml) unless the MM overrides it.
    """
    name = str(msg.get("name", "Threat"))[:128]
    default_segments = 4
    if session.ruleset.hazards:
        default_segments = session.ruleset.hazards.threat_clock.segments
    segments = int(msg.get("segments", default_segments))
    clock_id = str(msg.get("clock_id") or uuid.uuid4())

    clock = ThreatClock(id=clock_id, name=name, segments=segments)
    session.threat_clocks[clock_id] = clock

    await manager.broadcast(session_id, {
        "type": "clock_created",
        "clock": clock.to_client_dict(),
    })


async def _handle_clock_advance(msg: dict, session, session_id: str) -> None:
    """MM advances a Threat Clock by one segment, if the outcome tier qualifies.

    `outcome_tier` is checked against `hazards.threat_clock.advances_on`
    (default: partial_success, failure) — a 10+ (full_success) never advances
    the clock. No new resolution mechanic: this reuses the existing roll
    outcome tiers (BRIEF non-goal).
    """
    clock_id = str(msg.get("clock_id", ""))
    clock = session.threat_clocks.get(clock_id)
    if not clock:
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"No Threat Clock with id '{clock_id}'.",
        })
        return

    outcome_tier = str(msg.get("outcome_tier", ""))
    advances_on = (
        session.ruleset.hazards.threat_clock.advances_on
        if session.ruleset.hazards else ["partial_success", "failure"]
    )

    just_filled = False
    if outcome_tier in advances_on:
        just_filled = clock.advance()

    await manager.broadcast(session_id, {
        "type": "clock_advanced",
        "clock": clock.to_client_dict(),
    })

    if just_filled:
        await manager.broadcast(session_id, {
            "type": "clock_fill",
            "clock": clock.to_client_dict(),
        })


async def _handle_clock_wind_back(msg: dict, session, session_id: str) -> None:
    """Spend an action to wind a Threat Clock back one segment.

    Unconditional — no roll (Brain, BRIEF §EF4). A rolled wind-back would let
    a 7-9 advance the very clock being wound.
    """
    clock_id = str(msg.get("clock_id", ""))
    clock = session.threat_clocks.get(clock_id)
    if not clock:
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"No Threat Clock with id '{clock_id}'.",
        })
        return

    clock.wind_back()

    await manager.broadcast(session_id, {
        "type": "clock_wound_back",
        "clock": clock.to_client_dict(),
    })
