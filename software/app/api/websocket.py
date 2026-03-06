"""WebSocket connection manager and event dispatcher."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError

from app.auth.tokens import decode_token
from app.game.engine import RollRequest, resolve_roll, resolve_magic_roll, roll_result_to_dict
from app.game.session import session_store

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

    async def send_to(self, websocket: WebSocket, message: dict) -> None:
        try:
            await websocket.send_json(message)
        except Exception:
            pass


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
    # --- Magic events ---
    elif event_type == "cast":
        await _handle_cast(websocket, msg, session, session_id, identity)
    # --- Technique events ---
    elif event_type == "technique_select" and is_mm:
        await _handle_technique_select(msg, session, session_id)
    elif event_type == "session_reset" and is_mm:
        await _handle_session_reset(session, session_id)
    else:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown event type: {event_type}"})


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

    # Validate Spark spend — server authoritative
    sparks_to_spend = min(sparks_requested, character.sparks)
    if sparks_to_spend > 0:
        for _ in range(sparks_to_spend):
            character.spend_spark()

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


# ---------------------------------------------------------------------------
# Combat handlers
# ---------------------------------------------------------------------------

async def _handle_combat_start(msg: dict, session, session_id: str) -> None:
    """MM initialises combat. Sets all characters' endurance_current = endurance_max."""
    state: dict = {}
    for player_name, character in session.characters.items():
        character.endurance_current = character.endurance_max(session.ruleset)
        character.conditions = []
        character.posture = "measured"
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

    sparks_to_spend = min(sparks_requested, character.sparks)
    for _ in range(sparks_to_spend):
        character.spend_spark()

    request = RollRequest(
        attribute_id="strength",
        attribute_rating=character.attributes.get("strength", 2),
        skill_id="combat",
        skill_rank_id=character.skills["combat"].rank if "combat" in character.skills else None,
        difficulty_label=difficulty,
        sparks_spent=sparks_to_spend,
        press=press,
        description=str(msg.get("description", ""))[:200],
    )
    result = resolve_roll(request, session.ruleset)
    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name, result_dict)

    await manager.broadcast(session_id, {
        "type": "strike_result",
        "attacker": player_name,
        "target": target_name,
        "roll": result_dict,
        "press_used": press,
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
    valid_reactions = {"dodge", "parry", "absorb", "intercept"}
    if reaction not in valid_reactions:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown reaction '{reaction}'."})
        return

    # Compute Endurance cost (adjust for posture)
    base_costs = {"dodge": 1, "parry": 1, "absorb": 0, "intercept": 2}
    base_cost = base_costs[reaction]
    posture_mod = 0
    if character.posture == "aggressive":
        posture_mod = 1
    elif character.posture == "defensive" or character.posture == "withdrawn":
        posture_mod = -1
    cost = max(0, base_cost + posture_mod)
    if character.posture == "withdrawn":
        cost = 0  # withdrawn: free reactions

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

    await manager.broadcast(session_id, {
        "type": "react_result",
        "player": player_name,
        "reaction": reaction,
        "endurance_cost": cost,
        "endurance_remaining": character.endurance_current,
        "roll": roll_result,
    })


async def _handle_apply_condition(msg: dict, session, session_id: str) -> None:
    """MM applies a condition to a character."""
    player_name = msg.get("player_name", "")
    condition = str(msg.get("condition", ""))
    character = session.characters.get(player_name)
    if not character:
        return

    # Stacking: second Tier 2 condition → Broken
    tier2_conditions = {"staggered", "cornered"}
    tier2_on_char = [c for c in character.conditions if c in tier2_conditions]
    if condition in tier2_conditions and len(tier2_on_char) >= 1:
        condition = "broken"

    if condition and condition not in character.conditions:
        character.conditions.append(condition)

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
    await manager.broadcast(session_id, {
        "type": "condition_cleared",
        "player": player_name,
        "condition": condition,
        "all_conditions": list(character.conditions) if character else [],
    })


async def _handle_end_exchange(session, session_id: str) -> None:
    """MM signals end of exchange: clear Tier 1 conditions, apply Withdrawn recovery."""
    tier1_conditions = {"winded", "off_balance", "shaken"}
    recovery_amount = 2  # from combat YAML: recovery_withdrawn: 2

    updates: dict = {}
    for player_name, character in session.characters.items():
        if character.endurance_current is None:
            continue

        # Clear Tier 1 conditions
        cleared = [c for c in character.conditions if c in tier1_conditions]
        character.conditions = [c for c in character.conditions if c not in tier1_conditions]

        # Withdrawn endurance recovery (only if not striking, enforced by declare_posture)
        if character.posture == "withdrawn":
            max_end = character.endurance_max(session.ruleset)
            character.endurance_current = min(character.endurance_current + recovery_amount, max_end)

        updates[player_name] = {
            "conditions": list(character.conditions),
            "cleared_conditions": cleared,
            "endurance_current": character.endurance_current,
        }

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

    # Validate: technique must not already be selected
    if technique_id in character.techniques:
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"Technique '{technique_id}' already selected.",
        })
        return

    # Validate prerequisites in the ruleset technique trees
    prereq_errors: list[str] = []
    for facet_id, tree in session.ruleset.techniques.items():
        for branch in tree.branches:
            for tier_def in branch.tiers:
                for tech in tier_def.techniques:
                    if tech.id == technique_id:
                        for prereq in tech.prerequisites:
                            if prereq not in character.techniques:
                                prereq_errors.append(prereq)

    if prereq_errors:
        await manager.broadcast(session_id, {
            "type": "error",
            "message": f"Technique '{technique_id}' requires: {', '.join(prereq_errors)}.",
        })
        return

    character.techniques.append(technique_id)
    if choice:
        character.technique_choices[technique_id] = str(choice)

    # Special: magic-granting Techniques activate magic_technique_active
    magic_granting = {"arcane_study", "spiritual_domain"}
    if technique_id in magic_granting:
        character.magic_technique_active = True
        if choice:
            character.magic_domain = choice

    await manager.broadcast(session_id, {
        "type": "technique_selected",
        "player": player_name,
        "technique_id": technique_id,
        "choice": choice,
        "all_techniques": list(character.techniques),
    })


async def _handle_session_reset(session, session_id: str) -> None:
    """MM signals start of new session: reset once-per-session technique tracking."""
    for character in session.characters.values():
        character.techniques_used_this_session = []
        character.sparks = session.ruleset.spark.base_sparks_per_session if session.ruleset.spark else 3
    await manager.broadcast(session_id, {"type": "session_reset"})
