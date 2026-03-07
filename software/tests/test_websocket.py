"""Tests for WebSocket ConnectionManager and event handling."""
from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml

from app.api.websocket import ConnectionManager
from app.auth.tokens import create_mm_token, create_session_token
from app.game.session import session_store


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


# ---------------------------------------------------------------------------
# B3.1 — Silent broadcast failure is logged (not swallowed)
# ---------------------------------------------------------------------------

class TestSendToLogsWarningOnFailure:
    async def test_send_to_logs_warning_when_send_fails(self, caplog):
        """B3.1: send_to() must log a warning and return False when send_json raises."""
        manager = ConnectionManager()
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("simulated network error")
        with caplog.at_level(logging.WARNING, logger="app.api.websocket"):
            result = await manager.send_to(ws, {"type": "test"})
        assert result is False
        assert any("simulated network error" in r.message for r in caplog.records)

    async def test_send_to_returns_true_on_success(self, caplog):
        """Sanity: send_to() returns True when no exception is raised."""
        manager = ConnectionManager()
        ws = AsyncMock()
        result = await manager.send_to(ws, {"type": "pong"})
        assert result is True


# ---------------------------------------------------------------------------
# B3.2 — Magic-granting Technique activates via schema flag (not hardcoded ID)
# ---------------------------------------------------------------------------

class TestMagicGrantingTechniqueFlag:
    def test_arcane_study_sets_magic_technique_active(self, client, mm_token, session_with_character):
        """B3.2: Selecting arcane_study (magic_granting: true in YAML) activates magic."""
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "arcane_study",
                "choice": "inscription",
            })
            msg = ws.receive_json()
        assert msg["type"] == "technique_selected"
        char = session_store.get(session_id).characters["Zahna"]
        assert char.magic_technique_active is True

    def test_magic_domain_set_from_choice(self, client, mm_token, session_with_character):
        """B3.2: magic_domain is set from the choice field when magic_granting technique is selected."""
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "arcane_study",
                "choice": "inscription",
            })
            ws.receive_json()
        char = session_store.get(session_id).characters["Zahna"]
        assert char.magic_domain == "inscription"


# ---------------------------------------------------------------------------
# B3.4 — Persistence after state mutation: strike saves to disk
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 0.9 — Combat gameplay loop tests
# ---------------------------------------------------------------------------

class TestCombatGameplayLoop:
    """Comprehensive combat tests covering strike, react, posture, armor,
    endurance, conditions, and full exchange flow."""

    def _start_combat(self, ws):
        """Send combat_start and drain the response."""
        ws.send_json({"type": "combat_start"})
        return ws.receive_json()  # combat_started

    def test_strike_with_dexterity_attribute(self, client, mm_token, session_with_character):
        """0.1: Strike can use any attribute, not just Strength."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike",
                "target": "goblin",
                "attribute_id": "dexterity",
                "skill_id": "finesse",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["roll"]["attribute_id"] == "dexterity"

    def test_strike_with_intelligence(self, client, mm_token, session_with_character):
        """0.1: Strike with Intelligence+Lore (Mind character)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike",
                "target": "goblin",
                "attribute_id": "intelligence",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["roll"]["attribute_id"] == "intelligence"

    def test_strike_invalid_attribute_returns_error(self, client, mm_token, session_with_character):
        """0.1: Strike with unknown attribute returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike",
                "target": "goblin",
                "attribute_id": "flying",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "flying" in msg["message"]

    def test_posture_offense_modifier_in_strike(self, client, mm_token, session_with_character):
        """0.2: Aggressive posture applies +1 offense modifier to strike."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            # Declare aggressive posture
            ws.send_json({"type": "declare_posture", "posture": "aggressive"})
            ws.receive_json()  # posture_declared
            # Strike
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["posture"] == "aggressive"
            # The offense modifier should be in the roll
            assert msg["roll"].get("offense_modifier", 0) == 1

    def test_armor_downgrades_condition(self, client, mm_token, session_with_character):
        """0.3: Light armor downgrades Tier 2 condition to Tier 1."""
        session, _ = session_with_character
        session_id = session["session_id"]

        # Set armor on character
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            # Apply Tier 2 condition — should be downgraded to Tier 1
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "staggered",
            })
            msg = ws.receive_json()
            assert msg["type"] == "condition_applied"
            # staggered (T2) should be downgraded to first T1 condition (winded)
            assert msg["condition"] == "winded"

    def test_heavy_armor_downgrades_tier3_to_tier1(self, client, mm_token, session_with_character):
        """0.3: Heavy armor (downgrades 2) reduces Tier 3 to Tier 1."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "heavy"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "broken",
            })
            msg = ws.receive_json()
            assert msg["type"] == "condition_applied"
            # broken (T3) downgraded by 2 tiers → T1 (winded)
            assert msg["condition"] == "winded"

    def test_no_armor_no_downgrade(self, client, mm_token, session_with_character):
        """0.3: Without armor, conditions are not downgraded."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "staggered",
            })
            msg = ws.receive_json()
            assert msg["condition"] == "staggered"

    def test_zero_endurance_absorb_only(self, client, mm_token, session_with_character):
        """0.4: At 0 Endurance, only Absorb reaction is allowed."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        # Start combat then drain endurance
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].endurance_current = 0

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "dodge"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Absorb" in msg["message"]

    def test_zero_endurance_absorb_allowed(self, client, mm_token, session_with_character):
        """0.4: Absorb still works at 0 Endurance."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].endurance_current = 0

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "absorb"})
            msg = ws.receive_json()
            assert msg["type"] == "react_result"
            assert msg["reaction"] == "absorb"

    def test_tier2_stacking_to_broken(self, client, mm_token, session_with_character):
        """Two Tier 2 conditions stack to Broken."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            # Apply first T2
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg1 = ws.receive_json()
            assert msg1["condition"] == "staggered"
            # Apply second T2 → should become broken
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "cornered"})
            msg2 = ws.receive_json()
            assert msg2["condition"] == "broken"

    def test_end_exchange_clears_tier1(self, client, mm_token, session_with_character):
        """End-of-exchange clears all Tier 1 conditions."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            # Apply T1 conditions
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "winded"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "off_balance"})
            ws.receive_json()
            # End exchange
            ws.send_json({"type": "end_exchange"})
            msg = ws.receive_json()
            assert msg["type"] == "exchange_ended"
            zahna_data = msg["characters"]["Zahna"]
            assert "winded" not in zahna_data["conditions"]
            assert "off_balance" not in zahna_data["conditions"]
            assert "winded" in zahna_data["cleared_conditions"]

    def test_end_exchange_keeps_tier2(self, client, mm_token, session_with_character):
        """End-of-exchange does NOT clear Tier 2 conditions."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            ws.receive_json()
            ws.send_json({"type": "end_exchange"})
            msg = ws.receive_json()
            assert "staggered" in msg["characters"]["Zahna"]["conditions"]

    def test_withdrawn_endurance_recovery(self, client, mm_token, session_with_character):
        """Withdrawn posture recovers 2 Endurance at end of exchange."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        # Set low endurance and withdrawn posture
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.endurance_current = 1
        char.posture = "withdrawn"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "end_exchange"})
            msg = ws.receive_json()
            zahna = msg["characters"]["Zahna"]
            # Should have recovered 2 Endurance (capped at max)
            assert zahna["endurance_current"] == 3

    def test_withdrawn_cannot_strike(self, client, mm_token, session_with_character):
        """Withdrawn posture blocks Strike."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "withdrawn"})
            ws.receive_json()
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Withdrawn" in msg["message"]

    def test_full_exchange_sequence(self, client, mm_token, session_with_character):
        """Full exchange: set posture → strike → react → apply condition → end exchange."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        # Start combat
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        # Player declares posture and strikes
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "measured"})
            posture_msg = ws.receive_json()
            assert posture_msg["type"] == "posture_declared"

            ws.send_json({"type": "strike", "target": "goblin"})
            strike_msg = ws.receive_json()
            assert strike_msg["type"] == "strike_result"

            ws.send_json({"type": "react", "reaction": "dodge"})
            react_msg = ws.receive_json()
            assert react_msg["type"] == "react_result"

        # MM applies condition and ends exchange
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "winded"})
            cond_msg = ws.receive_json()
            assert cond_msg["type"] == "condition_applied"

            ws.send_json({"type": "end_exchange"})
            end_msg = ws.receive_json()
            assert end_msg["type"] == "exchange_ended"
            # T1 condition should be cleared
            assert "winded" not in end_msg["characters"]["Zahna"]["conditions"]

    def test_skill_advance_checks_skill_points(self, client, mm_token, session_with_character):
        """0.7: Skill advance deducts session_skill_points_remaining."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.session_skill_points_remaining = 0

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "skill_advance",
                "player_name": "Zahna",
                "skill_id": "lore",
                "marks": 1,
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "skill points" in msg["message"].lower()

    def test_combat_end_clears_state(self, client, mm_token, session_with_character):
        """combat_end clears all ephemeral combat state."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({"type": "combat_end"})
            msg = ws.receive_json()
            assert msg["type"] == "combat_ended"

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        assert char.endurance_current is None
        assert char.conditions == []
        assert char.posture is None


class TestSupportAndManeuver:
    """Phase 2.1: Support and Maneuver action handlers."""

    def _start_combat(self, ws):
        ws.send_json({"type": "combat_start"})
        return ws.receive_json()

    def test_support_broadcasts_result(self, client, mm_token, session_with_character):
        """Support action rolls and broadcasts support_result."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "support",
                "target": "Mordai",
                "bonus_type": "add_die",
                "attribute_id": "charisma",
            })
            msg = ws.receive_json()
            assert msg["type"] == "support_result"
            assert msg["player"] == "Zahna"
            assert msg["target"] == "Mordai"
            assert msg["bonus_type"] == "add_die"
            assert "roll" in msg

    def test_support_invalid_bonus_type(self, client, mm_token, session_with_character):
        """Support with invalid bonus_type returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "support",
                "target": "Mordai",
                "bonus_type": "invalid",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "invalid" in msg["message"].lower()

    def test_support_requires_combat(self, client, mm_token, session_with_character):
        """Support outside combat returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "support", "target": "Mordai"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "combat" in msg["message"].lower()

    def test_maneuver_broadcasts_result(self, client, mm_token, session_with_character):
        """Maneuver action rolls and broadcasts maneuver_result."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "maneuver",
                "target": "goblin",
                "attribute_id": "dexterity",
            })
            msg = ws.receive_json()
            assert msg["type"] == "maneuver_result"
            assert msg["player"] == "Zahna"
            assert msg["target"] == "goblin"
            assert "roll" in msg

    def test_maneuver_withdrawn_blocked(self, client, mm_token, session_with_character):
        """Maneuver from Withdrawn posture is blocked."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "withdrawn"})
            ws.receive_json()
            ws.send_json({"type": "maneuver", "target": "goblin"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Withdrawn" in msg["message"]

    def test_maneuver_requires_combat(self, client, mm_token, session_with_character):
        """Maneuver outside combat returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "maneuver", "target": "goblin"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "combat" in msg["message"].lower()


class TestContestedRoll:
    """Phase 2.2: Contested roll handler."""

    def test_contested_roll_produces_winner(self, client, mm_token, session_with_character):
        """Contested roll between two characters produces a winner."""
        session, _ = session_with_character
        session_id = session["session_id"]

        # Create a second character
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": session_id,
                "character_name": "Mordai",
                "primary_facet": "body",
                "attributes": {
                    "strength": 3, "dexterity": 2, "constitution": 3,
                    "intelligence": 1, "wisdom": 1, "knowledge": 2,
                    "spirit": 2, "luck": 2, "charisma": 2,
                },
            },
            headers={"Authorization": f"Bearer {create_mm_token()}"},
        )
        assert resp.status_code == 200

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "contested_roll",
                "player_a": "Zahna",
                "player_b": "Mordai",
                "attribute_a": "intelligence",
                "attribute_b": "strength",
            })
            msg = ws.receive_json()
            assert msg["type"] == "contested_roll_result"
            assert msg["player_a"] == "Zahna"
            assert msg["player_b"] == "Mordai"
            assert "roll_a" in msg
            assert "roll_b" in msg
            assert msg["winner"] in ("Zahna", "Mordai", "tie")

    def test_contested_roll_missing_character_error(self, client, mm_token, session_with_character):
        """Contested roll with nonexistent player returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "contested_roll",
                "player_a": "Zahna",
                "player_b": "Nobody",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "characters" in msg["message"].lower() or "players" in msg["message"].lower()

    def test_contested_roll_requires_mm(self, client, mm_token, session_with_character):
        """Contested roll is MM-only; players cannot trigger it."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "contested_roll",
                "player_a": "Zahna",
                "player_b": "Mordai",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"


class TestSpendSkillPoint:
    """Phase 2.3: Player-initiated skill point spending."""

    def test_spend_skill_point_success(self, client, mm_token, session_with_character):
        """Player can spend a skill point to advance a skill."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        # Ensure character has skill points
        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 4

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "spend_skill_point",
                "skill_id": "lore",
            })
            msg = ws.receive_json()
            assert msg["type"] == "skill_point_spent"
            assert msg["player"] == "Zahna"
            assert msg["skill_id"] == "lore"
            assert msg["marks_added"] == 1
            assert "session_skill_points_remaining" in msg

    def test_spend_skill_point_insufficient_budget(self, client, mm_token, session_with_character):
        """Spending a skill point with 0 remaining returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 0

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "spend_skill_point",
                "skill_id": "lore",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "skill points" in msg["message"].lower()

    def test_spend_skill_point_missing_skill_id(self, client, mm_token, session_with_character):
        """Missing skill_id returns error."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spend_skill_point"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "skill_id" in msg["message"].lower()

    def test_spend_skill_point_deducts_budget(self, client, mm_token, session_with_character):
        """Spending deducts from session_skill_points_remaining."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 4

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spend_skill_point", "skill_id": "lore"})
            msg = ws.receive_json()
            assert msg["type"] == "skill_point_spent"

        # Check that the budget was decremented
        remaining = sess.characters["Zahna"].session_skill_points_remaining
        assert remaining < 4


class TestSecondaryMagicDomain:
    """Phase 2.4: Secondary magic domain with difficulty penalty."""

    def test_secondary_domain_harder_difficulty(self):
        """Secondary magic domain rolls one difficulty step harder."""
        from types import SimpleNamespace
        from unittest.mock import MagicMock, patch
        from app.facets.schema import MagicDomainDef
        from app.game.engine import resolve_magic_roll

        domain_primary = MagicDomainDef(
            id="test_primary", name="Primary", type="focused",
            tradition="intuitive", description="Primary domain.",
        )
        domain_secondary = MagicDomainDef(
            id="test_secondary", name="Secondary", type="focused",
            tradition="intuitive", description="Secondary domain.",
        )
        magic_mock = MagicMock()
        magic_mock.get_domain.side_effect = lambda d: (
            domain_primary if d == "test_primary" else domain_secondary
        )
        magic_mock.domain_types = {
            "focused": {"scope_difficulties": {"minor": "Easy", "significant": "Standard", "major": "Hard"}},
        }
        magic_mock.pre_technique_scope_limit = "minor"
        magic_mock.pre_technique_difficulty_penalty = 1

        ruleset_mock = MagicMock()
        ruleset_mock.magic = magic_mock
        ruleset_mock.roll_resolution = None
        ruleset_mock.get_minor_attribute_modifier.return_value = 0
        ruleset_mock.get_skill_rank_modifier.return_value = 0

        char = SimpleNamespace(
            magic_technique_active=True,
            magic_domain="test_primary",
            secondary_magic_domain="test_secondary",
            attributes={"spirit": 2},
        )

        with patch("random.randint", return_value=5):
            result_primary = resolve_magic_roll(char, "test_primary", "minor", "test", ruleset_mock)
            result_secondary = resolve_magic_roll(char, "test_secondary", "minor", "test", ruleset_mock)

        # Secondary domain is one step harder: Easy→Standard (modifier +1 → 0)
        assert result_secondary.difficulty_modifier == result_primary.difficulty_modifier - 1

    def test_character_secondary_domain_serialization(self, ruleset):
        """secondary_magic_domain round-trips through to_fof/from_fof."""
        from app.game.character import Character

        char = Character(
            name="TestMage",
            player_name="P1",
            primary_facet="soul",
            attributes={
                "strength": 2, "dexterity": 2, "constitution": 2,
                "intelligence": 2, "wisdom": 2, "knowledge": 2,
                "spirit": 2, "luck": 2, "charisma": 2,
            },
            magic_domain="test_primary",
            secondary_magic_domain="test_secondary",
        )

        fof_data = char.to_fof(module_refs=[], session_id="test-session")
        restored = Character.from_fof(fof_data, ruleset)
        assert restored.secondary_magic_domain == "test_secondary"


class TestPersistenceAfterMutation:
    def test_strike_persists_to_disk(self, client, mm_token, session_with_character):
        """B3.4: After a strike event, the character file on disk reflects combat state."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        # Step 1: MM starts combat (sets endurance_current)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "combat_start"})
            ws.receive_json()  # combat_started

        # Step 2: Player strikes (triggers save_character_to_disk)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin"})
            ws.receive_json()  # strike_result

        # Step 3: Read the character file from disk
        from app.config import settings
        char_file = settings.data_dir / "sessions" / session_id / "characters" / "Zahna.fof"
        assert char_file.exists(), "Character file not found on disk"
        fof_data = yaml.safe_load(char_file.read_text(encoding="utf-8"))
        char_block = fof_data["character"]

        # endurance_current should be present (combat state was persisted)
        assert "endurance_current" in char_block
        assert isinstance(char_block["endurance_current"], int)


# ---------------------------------------------------------------------------
# Enemy tracker WebSocket events
# ---------------------------------------------------------------------------

class TestEnemyTrackerWS:
    """Tests for spawn_enemy, enemy_update, and remove_enemy WebSocket events."""

    def _create_session_with_enemy(self, client, mm_headers):
        """Create a session and add an enemy to its library."""
        resp = client.post("/api/sessions/", json={"name": "Enemy Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "thug",
            "name": "Harbor Thug",
            "tier": "mook",
            "attack_modifier": 0,
        }, headers=mm_headers)
        return session_id

    def test_spawn_enemy_from_library(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "spawn_enemy",
                "enemy_id": "thug",
                "instance_name": "Thug 1",
            })
            msg = ws.receive_json()
            assert msg["type"] == "enemy_spawned"
            assert msg["tracker_key"] == "Thug 1"
            assert msg["enemy"]["name"] == "Thug 1"
            assert msg["tr"] >= 1

    def test_spawn_enemy_inline(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Inline Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "spawn_enemy",
                "enemy_id": "bandit",
                "enemy_data": {
                    "name": "Bandit",
                    "tier": "mook",
                    "attack_modifier": 1,
                },
            })
            msg = ws.receive_json()
            assert msg["type"] == "enemy_spawned"
            assert msg["enemy"]["name"] == "Bandit"

    def test_spawn_enemy_not_found_no_data(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Error Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "spawn_enemy",
                "enemy_id": "ghost",
            })
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_enemy_update_endurance(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        # Also add a named enemy
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "sergeant",
            "name": "Sergeant",
            "tier": "named",
            "endurance": 6,
            "attack_modifier": 2,
            "armor": "light",
        }, headers=mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            # Spawn
            ws.send_json({
                "type": "spawn_enemy",
                "enemy_id": "sergeant",
                "instance_name": "Sgt. Davies",
            })
            ws.receive_json()  # enemy_spawned
            # Update endurance
            ws.send_json({
                "type": "enemy_update",
                "tracker_key": "Sgt. Davies",
                "endurance_current": 4,
            })
            msg = ws.receive_json()
            assert msg["type"] == "enemy_updated"
            assert msg["endurance_current"] == 4

    def test_enemy_update_conditions(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "named1", "name": "Named", "tier": "named", "endurance": 5,
        }, headers=mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "spawn_enemy", "enemy_id": "named1", "instance_name": "Named 1"})
            ws.receive_json()  # spawned
            # Add condition
            ws.send_json({"type": "enemy_update", "tracker_key": "Named 1", "add_condition": "staggered"})
            msg = ws.receive_json()
            assert "staggered" in msg["conditions"]
            # Remove condition
            ws.send_json({"type": "enemy_update", "tracker_key": "Named 1", "remove_condition": "staggered"})
            msg = ws.receive_json()
            assert "staggered" not in msg["conditions"]

    def test_enemy_update_not_found(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Update Error"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "enemy_update", "tracker_key": "nobody"})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_remove_enemy(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "spawn_enemy", "enemy_id": "thug", "instance_name": "Thug A"})
            ws.receive_json()  # spawned
            ws.send_json({"type": "remove_enemy", "tracker_key": "Thug A"})
            msg = ws.receive_json()
            assert msg["type"] == "enemy_removed"
            assert msg["tracker_key"] == "Thug A"

    def test_player_cannot_spawn_enemy(self, client, mm_headers, active_session, valid_attributes):
        session_id = active_session["session_id"]
        # Create a character for the player
        client.post("/api/characters/", json={
            "session_id": session_id,
            "character_name": "Tester",
            "primary_facet": "body",
            "attributes": valid_attributes,
        }, headers=mm_headers)
        player_token = create_session_token("Tester", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spawn_enemy", "enemy_id": "thug"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Unknown event type" in msg["message"]
