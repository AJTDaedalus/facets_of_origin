"""WebSocket connection manager and event dispatcher."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError

from app.auth.tokens import decode_token
from app.game.engine import RollRequest, resolve_roll, roll_result_to_dict
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
            "new_rank": character.skills[skill_id].rank if skill_id in character.skills else "novice",
            "new_facet_level": character.facet_level,
        })
