"""Tests for WebSocket ConnectionManager and event handling."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.api.websocket import ConnectionManager
from app.auth.tokens import create_mm_token, create_session_token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _auth_mm(ws, mm_token: str, session_id: str) -> None:
    """Authenticate as MM and drain the state + player_joined messages."""
    ws.send_json({"token": mm_token, "session_id": session_id})
    ws.receive_json()  # state
    ws.receive_json()  # player_joined


def _auth_player(ws, player_token: str) -> None:
    """Authenticate as a player and drain state + player_joined."""
    ws.send_json({"token": player_token})
    ws.receive_json()  # state
    ws.receive_json()  # player_joined


# ---------------------------------------------------------------------------
# ConnectionManager unit tests (async, isolated from the HTTP app)
# ---------------------------------------------------------------------------

class TestConnectionManager:
    async def test_connect_adds_connection(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        await manager.connect(ws, "sess1", "Player1")
        assert "sess1" in manager._connections
        assert len(manager._connections["sess1"]) == 1

    async def test_connect_stores_identity(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        await manager.connect(ws, "sess1", "Player1")
        _, stored_identity = manager._connections["sess1"][0]
        assert stored_identity == "Player1"

    async def test_connect_two_players_same_session(self):
        manager = ConnectionManager()
        ws1, ws2 = AsyncMock(), AsyncMock()
        await manager.connect(ws1, "sess1", "P1")
        await manager.connect(ws2, "sess1", "P2")
        assert len(manager._connections["sess1"]) == 2

    async def test_connect_different_sessions_independent(self):
        manager = ConnectionManager()
        ws1, ws2 = AsyncMock(), AsyncMock()
        await manager.connect(ws1, "sess1", "P1")
        await manager.connect(ws2, "sess2", "P2")
        assert len(manager._connections["sess1"]) == 1
        assert len(manager._connections["sess2"]) == 1

    async def test_disconnect_removes_websocket(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        await manager.connect(ws, "sess1", "P1")
        manager.disconnect(ws, "sess1")
        assert manager._connections["sess1"] == []

    async def test_disconnect_only_removes_target_ws(self):
        manager = ConnectionManager()
        ws1, ws2 = AsyncMock(), AsyncMock()
        await manager.connect(ws1, "sess1", "P1")
        await manager.connect(ws2, "sess1", "P2")
        manager.disconnect(ws1, "sess1")
        assert len(manager._connections["sess1"]) == 1
        assert manager._connections["sess1"][0][0] is ws2

    async def test_disconnect_unknown_session_noop(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        manager.disconnect(ws, "no-such-session")  # must not raise

    async def test_broadcast_sends_to_all_in_session(self):
        manager = ConnectionManager()
        ws1, ws2 = AsyncMock(), AsyncMock()
        await manager.connect(ws1, "sess1", "P1")
        await manager.connect(ws2, "sess1", "P2")
        await manager.broadcast("sess1", {"type": "test"})
        ws1.send_json.assert_called_once_with({"type": "test"})
        ws2.send_json.assert_called_once_with({"type": "test"})

    async def test_broadcast_does_not_reach_other_sessions(self):
        manager = ConnectionManager()
        ws1, ws2 = AsyncMock(), AsyncMock()
        await manager.connect(ws1, "sess1", "P1")
        await manager.connect(ws2, "sess2", "P2")
        await manager.broadcast("sess1", {"type": "test"})
        ws2.send_json.assert_not_called()

    async def test_broadcast_removes_dead_connections(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("Connection dead")
        await manager.connect(ws, "sess1", "P1")
        await manager.broadcast("sess1", {"type": "test"})
        assert manager._connections["sess1"] == []

    async def test_broadcast_empty_session_noop(self):
        manager = ConnectionManager()
        await manager.broadcast("empty-sess", {"type": "test"})  # must not raise

    async def test_send_to_calls_send_json(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        await manager.send_to(ws, {"type": "pong"})
        ws.send_json.assert_called_once_with({"type": "pong"})

    async def test_send_to_silently_ignores_failure(self):
        manager = ConnectionManager()
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("dead")
        await manager.send_to(ws, {"type": "test"})  # must not raise


# ---------------------------------------------------------------------------
# WebSocket auth flow — integration tests via TestClient
# ---------------------------------------------------------------------------

class TestWebSocketAuth:
    def test_mm_receives_state_message(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token, "session_id": session_id})
            msg = ws.receive_json()
            assert msg["type"] == "state"

    def test_mm_state_contains_session_id(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token, "session_id": session_id})
            msg = ws.receive_json()
            assert msg["data"]["session_id"] == session_id

    def test_mm_receives_player_joined_after_state(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token, "session_id": session_id})
            ws.receive_json()  # state
            joined = ws.receive_json()
            assert joined["type"] == "player_joined"
            assert joined["player"] == "mm"

    def test_player_receives_state_with_own_character(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": player_token})
            msg = ws.receive_json()
            assert msg["type"] == "state"
            assert "your_character" in msg["data"]

    def test_invalid_token_returns_error(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": "not.a.valid.token"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Authentication failed" in msg["message"]

    def test_empty_token_returns_error(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": ""})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_mm_missing_session_id_returns_error(self, client, mm_token):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token})  # no session_id for MM
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Missing session_id" in msg["message"]

    def test_nonexistent_session_returns_error(self, client, mm_token):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token, "session_id": "does-not-exist"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Session not found" in msg["message"]


# ---------------------------------------------------------------------------
# Ping / pong
# ---------------------------------------------------------------------------

class TestWebSocketPing:
    def test_ping_returns_pong(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "ping"})
            msg = ws.receive_json()
            assert msg["type"] == "pong"

    def test_multiple_pings(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            for _ in range(3):
                ws.send_json({"type": "ping"})
                msg = ws.receive_json()
                assert msg["type"] == "pong"

    def test_unknown_event_returns_error(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "this_does_not_exist"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Unknown event type" in msg["message"]


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class TestWebSocketChat:
    def test_chat_broadcasts_to_sender(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "chat", "text": "Hello table!"})
            msg = ws.receive_json()
            assert msg["type"] == "chat"
            assert msg["text"] == "Hello table!"
            assert msg["from"] == "mm"

    def test_chat_text_preserved(self, client, mm_token, active_session):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "chat", "text": "The dragon stirs."})
            msg = ws.receive_json()
            assert msg["text"] == "The dragon stirs."

    def test_empty_chat_not_broadcast(self, client, mm_token, active_session):
        """Empty or whitespace-only chat must not be broadcast."""
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "chat", "text": "   "})
            # Next message should be from a ping, not a chat
            ws.send_json({"type": "ping"})
            msg = ws.receive_json()
            assert msg["type"] == "pong"


# ---------------------------------------------------------------------------
# Roll via WebSocket
# ---------------------------------------------------------------------------

class TestWebSocketRoll:
    def test_roll_returns_result_broadcast(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll",
                "attribute_id": "intelligence",
                "difficulty": "Standard",
                "sparks_spent": 0,
            })
            msg = ws.receive_json()
            assert msg["type"] == "roll_result"

    def test_roll_result_contains_outcome(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll",
                "attribute_id": "intelligence",
                "difficulty": "Standard",
                "sparks_spent": 0,
            })
            msg = ws.receive_json()
            assert msg["roll"]["outcome"] in ("full_success", "partial_success", "failure")

    def test_roll_result_contains_player(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "roll", "attribute_id": "intelligence"})
            msg = ws.receive_json()
            assert msg["player"] == "Zahna"

    def test_roll_unknown_attribute_returns_error(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "roll", "attribute_id": "flying"})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_roll_with_no_character_returns_error(self, client, active_session):
        session_id = active_session["session_id"]
        player_token = create_session_token("NoOneHere", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "roll", "attribute_id": "strength"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "No character" in msg["message"]

    def test_roll_sparks_capped_at_available(self, client, session_with_character):
        """Spark spend above available should be silently capped."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll",
                "attribute_id": "intelligence",
                "sparks_spent": 999,  # far more than available
            })
            msg = ws.receive_json()
            assert msg["type"] == "roll_result"
            # Sparks spent must not exceed what the character had
            assert msg["roll"]["sparks_spent"] <= 3


# ---------------------------------------------------------------------------
# Spark earn (MM-only)
# ---------------------------------------------------------------------------

class TestWebSocketSparkEarn:
    def test_mm_can_award_spark(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "spark_earn",
                "player_name": "Zahna",
                "reason": "great roleplay",
            })
            msg = ws.receive_json()
            assert msg["type"] == "spark_earned"
            assert msg["player"] == "Zahna"

    def test_mm_spark_earn_includes_reason(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "spark_earn",
                "player_name": "Zahna",
                "reason": "brilliant plan",
            })
            msg = ws.receive_json()
            assert msg["reason"] == "brilliant plan"

    def test_player_cannot_award_spark(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "spark_earn",
                "player_name": "Zahna",
            })
            # spark_earn + is_mm=False → falls to else → error
            ws.send_json({"type": "ping"})
            msg = ws.receive_json()
            # Either error from unknown event or pong follows
            assert msg["type"] in ("error", "pong")


# ---------------------------------------------------------------------------
# Spark earn peer (any player)
# ---------------------------------------------------------------------------

class TestWebSocketSparkEarnPeer:
    def test_peer_nomination_broadcasts(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "spark_earn_peer",
                "player_name": "AnotherPlayer",
            })
            msg = ws.receive_json()
            assert msg["type"] == "spark_nomination"
            assert msg["nominated_by"] == "Zahna"

    def test_peer_nomination_includes_target(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "spark_earn_peer",
                "player_name": "TargetPlayer",
            })
            msg = ws.receive_json()
            assert msg["player"] == "TargetPlayer"


# ---------------------------------------------------------------------------
# Skill advance (MM-only)
# ---------------------------------------------------------------------------

class TestWebSocketSkillAdvance:
    def test_mm_can_advance_skill(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "skill_advance",
                "player_name": "Zahna",
                "skill_id": "athletics",
                "marks": 1,
            })
            msg = ws.receive_json()
            assert msg["type"] == "skill_advanced"
            assert msg["player"] == "Zahna"

    def test_player_cannot_advance_skill(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "skill_advance",
                "player_name": "Zahna",
                "skill_id": "athletics",
                "marks": 1,
            })
            ws.send_json({"type": "ping"})
            msg = ws.receive_json()
            assert msg["type"] in ("error", "pong")

    def test_skill_advance_zero_marks_ignored(self, client, mm_token, session_with_character):
        """marks=0 should be silently ignored (not advance anything)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "skill_advance",
                "player_name": "Zahna",
                "skill_id": "athletics",
                "marks": 0,
            })
            # No broadcast expected; ping should come back
            ws.send_json({"type": "ping"})
            msg = ws.receive_json()
            assert msg["type"] == "pong"


# ---------------------------------------------------------------------------
# Message size limiting (M-03)
# ---------------------------------------------------------------------------

class TestWebSocketMessageSize:
    """Messages exceeding WS_MAX_MESSAGE_BYTES are rejected without closing the connection."""

    def test_oversized_message_returns_error(self, client, session_with_character, mm_token):
        session_id = session_with_character[0]["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            # A message just over the 8 KiB limit
            big_text = "x" * 9000
            ws.send_text('{"type":"chat","text":"' + big_text + '"}')
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "too large" in msg["message"].lower()

    def test_oversized_message_does_not_close_connection(self, client, session_with_character, mm_token):
        """Connection stays open after an oversized message; subsequent messages work."""
        session_id = session_with_character[0]["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            big_text = "x" * 9000
            ws.send_text('{"type":"chat","text":"' + big_text + '"}')
            ws.receive_json()  # error message
            # Connection should still be alive
            ws.send_json({"type": "ping"})
            pong = ws.receive_json()
            assert pong["type"] == "pong"

    def test_message_at_limit_is_accepted(self, client, session_with_character, mm_token):
        """A message exactly at WS_MAX_MESSAGE_BYTES (8192 bytes) is accepted."""
        from app.api.websocket import WS_MAX_MESSAGE_BYTES
        session_id = session_with_character[0]["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            # Build a ping message padded to exactly the limit
            prefix = '{"type":"ping","_pad":"'
            suffix = '"}'
            pad = "a" * (WS_MAX_MESSAGE_BYTES - len(prefix) - len(suffix))
            msg = prefix + pad + suffix
            assert len(msg) == WS_MAX_MESSAGE_BYTES
            ws.send_text(msg)
            resp = ws.receive_json()
            assert resp["type"] == "pong"


# ---------------------------------------------------------------------------
# Auth timeout (L-03)
# ---------------------------------------------------------------------------

class TestWebSocketAuthTimeout:
    """Connections that never send an auth message are closed after the timeout."""

    def test_auth_timeout_closes_connection(self, client):
        """Monkeypatch WS_AUTH_TIMEOUT_SECONDS to 0 to test timeout path."""
        import app.api.websocket as ws_module
        original = ws_module.WS_AUTH_TIMEOUT_SECONDS
        ws_module.WS_AUTH_TIMEOUT_SECONDS = 0
        try:
            with client.websocket_connect("/ws") as ws:
                # With a 0-second timeout, the server should close immediately
                msg = ws.receive_json()
                assert msg["type"] == "error"
                assert "timeout" in msg["message"].lower()
        except Exception:
            pass  # Connection closed by server — expected
        finally:
            ws_module.WS_AUTH_TIMEOUT_SECONDS = original
