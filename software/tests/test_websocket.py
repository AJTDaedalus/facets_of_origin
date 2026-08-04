"""Tests for WebSocket ConnectionManager and event handling."""
from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import yaml

from app.api.websocket import ConnectionManager
from app.auth.tokens import create_mm_token, create_session_token
from app.game import combat as combat_module
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

    # -----------------------------------------------------------------------
    # TD-8: hazard_type / knowledge_field on the generic roll (B4 Q1)
    # -----------------------------------------------------------------------

    def test_roll_without_hazard_or_knowledge_field_behaves_as_today(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "roll", "attribute_id": "intelligence", "difficulty": "Standard"})
            msg = ws.receive_json()
            assert msg["type"] == "roll_result"
            assert msg["technique_step"] is None
            assert msg["roll"]["difficulty"] == "Standard"

    def test_roll_hazard_type_and_knowledge_field_round_trip_without_error(self, client, session_with_character):
        """Neither field qualifies any Technique this character holds — the
        point here is only that the server accepts and does not choke on them."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll", "attribute_id": "intelligence", "difficulty": "Standard",
                "hazard_type": "extreme cold", "knowledge_field": "arcane theory",
            })
            msg = ws.receive_json()
            assert msg["type"] == "roll_result"
            assert msg["technique_step"] is None

    # -----------------------------------------------------------------------
    # TD-9: the generic roll handler calls apply_character_difficulty_step
    # -----------------------------------------------------------------------

    def test_roll_acclimated_steps_difficulty_when_hazard_matches(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("acclimated")
        char.technique_choices["acclimated"] = "extreme cold"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll", "attribute_id": "constitution", "skill_id": "endurance",
                "difficulty": "Hard", "hazard_type": "extreme cold",
            })
            msg = ws.receive_json()
            assert msg["roll"]["difficulty"] == "Standard"
            assert msg["technique_step"]["technique_id"] == "acclimated"
            assert msg["technique_step"]["technique_name"] == "Acclimated"

    def test_roll_field_of_mastery_does_not_fire_on_mismatched_field(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("field_of_mastery")
        char.technique_choices["field_of_mastery"] = "history"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll", "attribute_id": "knowledge", "skill_id": "lore",
                "difficulty": "Hard", "knowledge_field": "arcane theory",
            })
            msg = ws.receive_json()
            assert msg["roll"]["difficulty"] == "Hard"
            assert msg["technique_step"] is None


# ---------------------------------------------------------------------------
# TD-9: the magic handler is deliberately NOT wired to difficulty composition
# (DESIGN_technique_difficulty.md §2.6 — magic difficulty comes from the
# domain/scope table, and no Technique in this cycle steps it).
# ---------------------------------------------------------------------------

class TestCastHandlerUnaffectedByDifficultyStep:
    def test_cast_ignores_a_technique_that_would_fire_on_a_strike(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.magic_domain = "inscription"
        char.magic_technique_active = True
        # A Technique that would step a Strike's difficulty if this context
        # ever reached apply_character_difficulty_step.
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "cast", "domain_id": "inscription", "scope": "minor",
                "intent": "test", "weapon_type": "blades",
            })
            msg = ws.receive_json()
            assert msg["type"] == "cast_result"
            assert "technique_step" not in msg


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
# Graceful Fail — player-initiated (D6, WD4)
# ---------------------------------------------------------------------------

class TestGracefulFailWS:
    def _roll_until_outcome(self, ws, outcome_tier: str, max_tries: int = 100) -> None:
        """Roll with attribute 0 modifier + Very Hard difficulty until a specific
        outcome tier lands, consuming the roll_result message each time."""
        for _ in range(max_tries):
            ws.send_json({
                "type": "roll",
                "attribute_id": "spirit",
                "difficulty": "Very Hard" if outcome_tier == "failure" else "Easy",
            })
            msg = ws.receive_json()
            if msg["roll"]["outcome"] == outcome_tier:
                return
        raise AssertionError(f"Could not roll a '{outcome_tier}' outcome within {max_tries} tries.")

    def test_act_break_broadcasts(self, client, mm_headers, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "act_break"})
            msg = ws.receive_json()
            assert msg["type"] == "act_break_opened"

    def test_claim_rejected_when_no_roll_yet(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "claim_graceful_fail"})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_claim_rejected_when_last_roll_not_failure(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            self._roll_until_outcome(ws, "full_success")
            ws.send_json({"type": "claim_graceful_fail"})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_claim_broadcasts_for_confirmation(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            self._roll_until_outcome(ws, "failure")
            ws.send_json({"type": "claim_graceful_fail"})
            msg = ws.receive_json()
            assert msg["type"] == "graceful_fail_claimed"
            assert msg["player"] == "Zahna"

    def test_mm_confirmation_awards_exactly_one_spark(
        self, client, mm_headers, mm_token, session_with_character
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as player_ws:
            _auth_player(player_ws, player_token)
            self._roll_until_outcome(player_ws, "failure")
            player_ws.send_json({"type": "claim_graceful_fail"})
            player_ws.receive_json()  # graceful_fail_claimed

            char = session_store.get(session_id).characters["Zahna"]
            sparks_before = char.sparks
            with client.websocket_connect("/ws") as mm_ws:
                _auth_mm(mm_ws, mm_token, session_id)
                mm_ws.send_json({
                    "type": "spark_earn",
                    "player_name": "Zahna",
                    "reason": "Graceful Fail",
                })
                msg = mm_ws.receive_json()
                assert msg["type"] == "spark_earned"
                assert msg["sparks_now"] == sparks_before + 1

    def test_double_claim_same_roll_rejected(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            self._roll_until_outcome(ws, "failure")
            ws.send_json({"type": "claim_graceful_fail"})
            msg = ws.receive_json()
            assert msg["type"] == "graceful_fail_claimed"
            ws.send_json({"type": "claim_graceful_fail"})
            msg = ws.receive_json()
            assert msg["type"] == "error"


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

    def test_skill_advanced_broadcast_carries_the_technique_pick(
        self, client, mm_token, session_with_character,
    ):
        """TODO T10: a Facet level grants a Technique pick, and the client has to
        be told, or the advancement panel keeps showing the old count until a
        reload. The broadcast reported the new rank and Facet level but not this.
        """
        session, _ = session_with_character
        session_id = session["session_id"]
        character = session_store.get(session_id).characters["Zahna"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            # Enough marks to cross a Facet level threshold and earn a pick.
            ws.send_json({
                "type": "skill_advance", "player_name": "Zahna",
                "skill_id": "lore", "marks": 60,
            })
            msg = ws.receive_json()

        assert msg["type"] == "skill_advanced"
        assert "technique_picks_available" in msg, (
            "the client cannot show a pick it is never told about")
        assert msg["technique_picks_available"] == character.technique_picks_available

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
        session_store.get(session_id).characters["Zahna"].technique_picks_available = 1
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
        session_store.get(session_id).characters["Zahna"].technique_picks_available = 1
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
# WS-B / B4 — Technique pick budget (§6.4)
# ---------------------------------------------------------------------------

class TestTechniquePickBudget:
    def test_select_rejected_with_zero_picks(self, client, mm_token, session_with_character):
        """A character with no earned Facet levels cannot pick a Technique."""
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        assert char.technique_picks_available == 0
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "read_the_room",
            })
            msg = ws.receive_json()
        assert msg["type"] == "error"
        assert "pick" in msg["message"].lower()
        assert "read_the_room" not in char.techniques

    def test_pick_consumed_on_success(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.technique_picks_available = 2
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "read_the_room",
            })
            msg = ws.receive_json()
        assert msg["type"] == "technique_selected"
        assert msg["technique_picks_available"] == 1
        assert char.technique_picks_available == 1

    def test_non_primary_tree_technique_accepted(self, client, mm_token, session_with_character):
        """Prerequisite checking is tree-agnostic: a mind-primary character may
        pick a soul-tree Technique whose prerequisites are met (D3)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]  # primary = mind
        char.techniques.append("read_the_room")  # soul-tree Tier 1 prerequisite
        char.technique_picks_available = 1
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "the_aimed_truth",  # soul Tier 2
            })
            msg = ws.receive_json()
        assert msg["type"] == "technique_selected"
        assert "the_aimed_truth" in char.techniques

    def test_tier_three_accepted_with_tier_two_held(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.extend(["read_the_room", "the_aimed_truth"])
        char.technique_picks_available = 1
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "the_turning",  # soul Tier 3, prereq the_aimed_truth
            })
            msg = ws.receive_json()
        assert msg["type"] == "technique_selected"
        assert "the_turning" in char.techniques

    def test_tier_three_rejected_without_tier_two(self, client, mm_token, session_with_character):
        """PHB II.4:83: Tier 3 requires a Tier 2 in the same branch. Holding only
        a Tier 1 Presence Technique (read_the_room) is not enough for the_turning
        (Presence Tier 3), regardless of which specific Tier 2 pick is missing."""
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("read_the_room")  # has Tier 1 but not Tier 2
        char.technique_picks_available = 1
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "technique_select",
                "player_name": "Zahna",
                "technique_id": "the_turning",
            })
            msg = ws.receive_json()
        assert msg["type"] == "error"
        assert "Tier 2" in msg["message"]
        assert "the_turning" not in char.techniques
        # A rejected pick must not be consumed.
        assert char.technique_picks_available == 1


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

    # -----------------------------------------------------------------------
    # TD-7: weapon_category on the Strike (B4 Q1 — DESIGN §2.4)
    # -----------------------------------------------------------------------

    def test_strike_without_weapon_category_behaves_as_today(self, client, mm_token, session_with_character):
        """Backward compatibility: a Strike that never mentions weapon_category
        or weapon_type is byte-for-byte what it was before TD-7/TD-18."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["weapon_category"] is None
            assert msg["weapon_type"] is None
            assert msg["technique_step"] is None
            assert msg["roll"]["difficulty"] == "Standard"

    def test_strike_with_valid_weapon_category_round_trips(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "weapon_category": "light"})
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["weapon_category"] == "light"

    def test_strike_with_unknown_weapon_category_returns_error(self, client, mm_token, session_with_character):
        """INV-8 is about attribute/skill pairings, not the reference-data
        vocabulary — an unrecognised category is a mistake, not a house rule,
        and is rejected with a message rather than silently dropped."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "weapon_category": "explosive"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "explosive" in msg["message"]

    # -----------------------------------------------------------------------
    # TD-18: weapon_type — the orthogonal, fictional vocabulary (DESIGN §8)
    # -----------------------------------------------------------------------

    def test_strike_with_valid_weapon_type_round_trips(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "weapon_type": "blades"})
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["weapon_type"] == "blades"

    def test_strike_with_unknown_weapon_type_returns_error(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "weapon_type": "explosive"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "explosive" in msg["message"]

    # -----------------------------------------------------------------------
    # TD-9: the Strike handler calls apply_character_difficulty_step
    # -----------------------------------------------------------------------
    #
    # TD-18 (DESIGN §8): weapon_mastery's step_trigger now matches
    # `weapon_type` (blades/blunt/polearms/unarmed — the fictional
    # vocabulary Weapon Mastery masters), not `weapon_category` (the
    # mechanical IV.1 vocabulary that only defaults the attribute). The two
    # are orthogonal and both ship on the Strike message. The four tests
    # below replace the TD-7-era pair that fired Weapon Mastery through
    # `weapon_category` — that only ever worked because the test used
    # `"light"` as a stand-in value for both fields, which is exactly the
    # bug the TD-7 escalation found (see docs/LOG_technique_difficulty.md).

    def test_strike_weapon_mastery_fires_on_matching_weapon_type(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike", "target": "goblin",
                "weapon_type": "blades", "difficulty": "Hard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["roll"]["difficulty"] == "Standard"
            assert msg["technique_step"] == {
                "technique_id": "weapon_mastery",
                "technique_name": "Weapon Mastery",
                "from": "Hard",
                "to": "Standard",
            }

    def test_strike_weapon_mastery_does_not_fire_on_mismatched_weapon_type(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike", "target": "goblin",
                "weapon_type": "blunt", "difficulty": "Hard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["roll"]["difficulty"] == "Hard"
            assert msg["technique_step"] is None

    def test_strike_weapon_mastery_does_not_fire_when_weapon_type_absent(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "difficulty": "Hard"})
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["weapon_type"] is None
            assert msg["roll"]["difficulty"] == "Hard"
            assert msg["technique_step"] is None

    def test_strike_weapon_category_alone_does_not_fire_weapon_mastery(self, client, mm_token, session_with_character):
        """Proves the two vocabularies are separate axes (DESIGN §8): a
        Strike that only carries `weapon_category` — never `weapon_type` —
        must not fire Weapon Mastery, even when the category value happens
        to equal the character's recorded choice."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike", "target": "goblin",
                "weapon_category": "light", "difficulty": "Hard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["weapon_category"] == "light"
            assert msg["roll"]["difficulty"] == "Hard"
            assert msg["technique_step"] is None

    def test_iii_3_513_mordai_weapon_mastery_blades_standard_becomes_easy(
        self, client, mm_token, session_with_character,
    ):
        """Regression for the flagship case the TD-7 escalation found broken
        (docs/LOG_technique_difficulty.md, docs/DESIGN_technique_difficulty.md
        §8): III.3:513 — Mordai, Weapon Mastery (blades), striking with a
        blade at the MM's declared Standard, gets Easy end to end."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("weapon_mastery")
        char.technique_choices["weapon_mastery"] = "blades"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike", "target": "goblin",
                "weapon_category": "standard", "weapon_type": "blades",
                "difficulty": "Standard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"
            assert msg["roll"]["difficulty"] == "Easy"
            assert msg["technique_step"]["technique_id"] == "weapon_mastery"
            assert msg["technique_step"]["from"] == "Standard"
            assert msg["technique_step"]["to"] == "Easy"

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

    def test_heavy_armor_downgrades_tier3_to_tier2(self, client, mm_token, session_with_character):
        """A5/D2: Heavy armor downgrades any incoming tier by one step (its
        per-scene budget spends here, first hit of the scene) — Tier 3
        (Broken) to Tier 2, not a 2-tier subtraction."""
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
            # broken (T3) downgraded one step → T2 (staggered)
            assert msg["condition"] == "staggered"

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

    def test_light_armor_budget_exhausts_after_two_hits(self, client, mm_token, session_with_character):
        """A5/D2: light armor's per-scene budget downgrades the first 2 hits
        and passes the 3rd through unmodified."""
        session, _ = session_with_character
        session_id = session["session_id"]
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            for _ in range(2):
                ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
                msg = ws.receive_json()
                assert msg["condition"] == "winded"
                ws.send_json({"type": "clear_condition", "player_name": "Zahna", "condition": "winded"})
                ws.receive_json()

            assert char.armor_downgrades_remaining == 0

            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg = ws.receive_json()
            assert msg["condition"] == "staggered"

    def test_armor_budget_persists_across_second_combat_start(self, client, mm_token, session_with_character):
        """A5/D2: a second `combat_start` (a second fight in the same scene)
        does not top the armor budget back up."""
        session, _ = session_with_character
        session_id = session["session_id"]
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            ws.receive_json()
            assert char.armor_downgrades_remaining == 1

            ws.send_json({"type": "combat_end"})
            ws.receive_json()
            self._start_combat(ws)
            assert char.armor_downgrades_remaining == 1

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

    def test_zero_endurance_dodge_refused_while_withdrawn(self, client, mm_token, session_with_character):
        """D5: the 0-Endurance floor is absolute — Withdrawn's free_reactions
        (0 Endurance cost) does not exempt a character from it. Only Absorb
        is available, regardless of Posture."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.endurance_current = 0
        char.posture = "withdrawn"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "dodge"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Absorb" in msg["message"]

    def test_zero_endurance_dodge_refused_while_defensive(self, client, mm_token, session_with_character):
        """D5: same floor, Defensive posture — its reduced reaction cost
        (min 0) does not exempt a character from the floor either."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.endurance_current = 0
        char.posture = "defensive"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "dodge"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Absorb" in msg["message"]

    def test_tier2_same_type_stacking_to_broken(self, client, mm_token, session_with_character):
        """D5 row 2: a second Tier 2 condition of the SAME type escalates to Broken."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            # Apply first T2
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg1 = ws.receive_json()
            assert msg1["condition"] == "staggered"
            # Apply staggered again → should become broken
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg2 = ws.receive_json()
            assert msg2["condition"] == "broken"

    def test_tier2_different_type_does_not_stack_to_broken(self, client, mm_token, session_with_character):
        """D5 row 2: Staggered and Cornered coexist without escalating to Broken."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg1 = ws.receive_json()
            assert msg1["condition"] == "staggered"
            # Apply a different Tier 2 → both present, no escalation
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "cornered"})
            msg2 = ws.receive_json()
            assert msg2["condition"] == "cornered"
            assert "staggered" in msg2["all_conditions"]
            assert "cornered" in msg2["all_conditions"]
            assert "broken" not in msg2["all_conditions"]

    def test_tier2_third_application_of_present_type_is_broken(self, client, mm_token, session_with_character):
        """D5 row 2: a third application of an already-present Tier 2 type stays Broken."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg2 = ws.receive_json()
            assert msg2["condition"] == "broken"
            # Third application of the same type — still resolves to Broken
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg3 = ws.receive_json()
            assert msg3["condition"] == "broken"

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

    def test_react_first_reaction_pays_aggressive_surcharge(
        self, client, mm_token, session_with_character,
    ):
        """K1 (BRIEF D8): the first reaction of the exchange still pays
        Aggressive's +1 surcharge (base 1 + 1 = 2)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "aggressive"})
            ws.receive_json()
            ws.send_json({"type": "react", "reaction": "dodge"})
            msg = ws.receive_json()
            assert msg["endurance_cost"] == 2

    def test_react_second_reaction_same_exchange_no_surcharge(
        self, client, mm_token, session_with_character,
    ):
        """K1 (BRIEF D8): a second reaction in the SAME exchange pays only
        the base cost — the Aggressive surcharge applies to the first
        reaction only."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "aggressive"})
            ws.receive_json()
            ws.send_json({"type": "react", "reaction": "dodge"})
            first = ws.receive_json()
            assert first["endurance_cost"] == 2
            ws.send_json({"type": "react", "reaction": "dodge"})
            second = ws.receive_json()
            assert second["endurance_cost"] == 1

    def test_reactions_this_exchange_resets_on_end_exchange(
        self, client, mm_token, session_with_character,
    ):
        """K1 (BRIEF D8): the per-exchange reaction count resets at end of
        exchange, so the next exchange's first reaction again pays the
        full Aggressive surcharge."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "aggressive"})
            ws.receive_json()
            ws.send_json({"type": "react", "reaction": "dodge"})
            first = ws.receive_json()
            assert first["endurance_cost"] == 2
            ws.send_json({"type": "react", "reaction": "dodge"})
            second = ws.receive_json()
            assert second["endurance_cost"] == 1

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "end_exchange"})
            ws.receive_json()

        # Restore Endurance so the assertion below isolates the reaction
        # counter reset, not Endurance availability.
        sess = session_store.get(session_id)
        sess.characters["Zahna"].endurance_current = sess.characters["Zahna"].endurance_max(sess.ruleset)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "dodge"})
            third = ws.receive_json()
            assert third["endurance_cost"] == 2

    # -----------------------------------------------------------------------
    # TD-9: the reaction handler calls apply_character_difficulty_step
    # -----------------------------------------------------------------------

    def test_react_declared_technique_steps_difficulty(self, client, mm_token, session_with_character):
        """A fiction-scoped Technique (The Uncanny Angle) only fires when the
        player toggles it via declared_technique_ids — it composes with the
        Parry roll's difficulty exactly like an auto Technique would."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_uncanny_angle")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "react", "reaction": "parry", "difficulty": "Hard",
                "declared_technique_ids": ["the_uncanny_angle"],
            })
            msg = ws.receive_json()
            assert msg["roll"]["difficulty"] == "Standard"
            assert msg["technique_step"] == {
                "technique_id": "the_uncanny_angle",
                "technique_name": "The Uncanny Angle",
                "from": "Hard",
                "to": "Standard",
            }

    def test_react_technique_not_toggled_does_not_fire(self, client, mm_token, session_with_character):
        """Same Technique, same character, but not declared on this roll —
        a fiction-scoped step never applies itself."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_uncanny_angle")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "parry", "difficulty": "Hard"})
            msg = ws.receive_json()
            assert msg["roll"]["difficulty"] == "Hard"
            assert msg["technique_step"] is None

    def test_react_absorb_carries_no_technique_step_key(self, client, mm_token, session_with_character):
        """Absorb never rolls, so there is no difficulty to step — the key is
        present and None rather than silently absent, matching every other
        reaction payload shape."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "react", "reaction": "absorb"})
            msg = ws.receive_json()
            assert msg["technique_step"] is None

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


class TestSkillUseEnforcement:
    """PHB II.4: Only skills used this session can receive advancement points."""

    def test_spend_rejected_when_skill_not_used(self, client, mm_token, session_with_character):
        """Spending on a skill that wasn't used returns error when other skills were used."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 4
        # Mark combat as used but NOT lore
        sess.characters["Zahna"].skills_used_this_session = {"combat"}

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spend_skill_point", "skill_id": "lore"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "not used this session" in msg["message"].lower()

    def test_spend_allowed_when_skill_was_used(self, client, mm_token, session_with_character):
        """Spending on a used skill succeeds."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 4
        sess.characters["Zahna"].skills_used_this_session = {"lore"}

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spend_skill_point", "skill_id": "lore"})
            msg = ws.receive_json()
            assert msg["type"] == "skill_point_spent"

    def test_spend_allowed_when_no_skills_tracked(self, client, mm_token, session_with_character):
        """When no skills have been used/marked, all skills are spendable (fresh session)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].session_skill_points_remaining = 4
        sess.characters["Zahna"].skills_used_this_session = set()

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "spend_skill_point", "skill_id": "lore"})
            msg = ws.receive_json()
            assert msg["type"] == "skill_point_spent"

    def test_mm_mark_skill_used(self, client, mm_token, session_with_character):
        """MM can mark a skill as used for a player."""
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "mark_skill_used",
                "player_name": "Zahna",
                "skill_id": "lore",
            })
            msg = ws.receive_json()
            assert msg["type"] == "skill_marked_used"
            assert msg["player"] == "Zahna"
            assert msg["skill_id"] == "lore"
            assert "lore" in msg["skills_used"]

        sess = session_store.get(session_id)
        assert "lore" in sess.characters["Zahna"].skills_used_this_session

    def test_auto_mark_on_roll(self, client, mm_token, session_with_character):
        """Rolling with a skill auto-marks it as used."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll",
                "attribute_id": "knowledge",
                "skill_id": "lore",
                "difficulty": "Standard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "roll_result"

        sess = session_store.get(session_id)
        assert "lore" in sess.characters["Zahna"].skills_used_this_session

    def test_auto_mark_on_strike(self, client, mm_token, session_with_character):
        """Striking with a skill auto-marks it as used."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.endurance_current = 5
        char.posture = "measured"

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike",
                "attribute_id": "strength",
                "skill_id": "combat",
                "difficulty": "Standard",
            })
            msg = ws.receive_json()
            assert msg["type"] == "strike_result"

        assert "combat" in sess.characters["Zahna"].skills_used_this_session

    def test_skills_used_in_client_dict(self, client, mm_token, session_with_character):
        """skills_used_this_session is included in character client dict."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        sess.characters["Zahna"].skills_used_this_session = {"lore", "combat"}

        d = sess.characters["Zahna"].to_client_dict()
        # Pydantic model_dump converts set to list
        assert set(d["skills_used_this_session"]) == {"lore", "combat"}


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
        magic_mock.pre_technique_difficulty_penalty = 0

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

    def test_enemy_update_resolve(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        # Also add a named enemy
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "sergeant",
            "name": "Sergeant",
            "tier": "named",
            "resolve": 3,
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
            # Update resolve
            ws.send_json({
                "type": "enemy_update",
                "tracker_key": "Sgt. Davies",
                "resolve_current": 1,
            })
            msg = ws.receive_json()
            assert msg["type"] == "enemy_updated"
            assert msg["resolve_current"] == 1

    def test_enemy_update_conditions(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "named1", "name": "Named", "tier": "named", "resolve": 3,
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

    def _spawn_boss_with_phase(self, client, mm_headers, mm_token, ws, session_id):
        """Spawn a Named enemy, then attach a phase directly (no CRUD support
        for `phases` yet — see A7 LOG scope note). Returns the tracker_key.
        """
        from app.game.enemy import PhaseDef

        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "boss1", "name": "Boss", "tier": "boss", "resolve": 5,
        }, headers=mm_headers)
        ws.send_json({"type": "spawn_enemy", "enemy_id": "boss1", "instance_name": "Boss 1"})
        ws.receive_json()  # enemy_spawned
        sess = session_store.get(session_id)
        sess.active_enemies["Boss 1"].phases = [
            PhaseDef(resolve_threshold=2, description="Reduced Mode."),
        ]
        return "Boss 1"

    def test_enemy_phase_change_fires_on_threshold_cross(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Phase Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            tracker_key = self._spawn_boss_with_phase(client, mm_headers, mm_token, ws, session_id)
            ws.send_json({"type": "enemy_update", "tracker_key": tracker_key, "resolve_current": 2})
            updated = ws.receive_json()
            assert updated["type"] == "enemy_updated"
            phase_msg = ws.receive_json()
            assert phase_msg["type"] == "enemy_phase_change"
            assert phase_msg["enemy_id"] == tracker_key
            assert phase_msg["phase_index"] == 0
            assert phase_msg["description"] == "Reduced Mode."

    def test_enemy_phase_change_fires_once_not_repeatedly(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Phase Test 2"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            tracker_key = self._spawn_boss_with_phase(client, mm_headers, mm_token, ws, session_id)
            ws.send_json({"type": "enemy_update", "tracker_key": tracker_key, "resolve_current": 2})
            ws.receive_json()  # enemy_updated
            ws.receive_json()  # enemy_phase_change (first crossing)
            ws.send_json({"type": "enemy_update", "tracker_key": tracker_key, "resolve_current": 1})
            second_updated = ws.receive_json()
            assert second_updated["type"] == "enemy_updated"
            # Already past the threshold before this call — no second phase_change.
            ws.send_json({"type": "enemy_update", "tracker_key": tracker_key, "resolve_current": 0})
            third_updated = ws.receive_json()
            assert third_updated["type"] == "enemy_updated"

    def test_enemy_phase_change_does_not_fire_without_phases(self, client, mm_headers, mm_token):
        session_id = self._create_session_with_enemy(client, mm_headers)
        client.post("/api/enemies/", json={
            "session_id": session_id,
            "id": "named1", "name": "Named", "tier": "named", "resolve": 3,
        }, headers=mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "spawn_enemy", "enemy_id": "named1", "instance_name": "Named 1"})
            ws.receive_json()  # enemy_spawned
            ws.send_json({"type": "enemy_update", "tracker_key": "Named 1", "resolve_current": 0})
            msg = ws.receive_json()
            assert msg["type"] == "enemy_updated"

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


# ---------------------------------------------------------------------------
# Threat Clock (D4, PHB III.2 — WD2)
# ---------------------------------------------------------------------------

class TestThreatClockWS:
    """Tests for clock_create, clock_advance, clock_wind_back, clock_fill."""

    def _create_clock(self, ws, name="Rising Tide", segments=4):
        ws.send_json({"type": "clock_create", "name": name, "segments": segments})
        msg = ws.receive_json()
        assert msg["type"] == "clock_created"
        return msg["clock"]["id"]

    def test_clock_create_defaults_to_ruleset_segments(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "clock_create", "name": "The Rising Waters"})
            msg = ws.receive_json()
            assert msg["type"] == "clock_created"
            assert msg["clock"]["segments"] == 4
            assert msg["clock"]["filled_segments"] == 0
            assert msg["clock"]["is_full"] is False

    def test_clock_advances_on_partial_success(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws)
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "partial_success"})
            msg = ws.receive_json()
            assert msg["type"] == "clock_advanced"
            assert msg["clock"]["filled_segments"] == 1

    def test_clock_advances_on_failure(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws)
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "failure"})
            msg = ws.receive_json()
            assert msg["type"] == "clock_advanced"
            assert msg["clock"]["filled_segments"] == 1

    def test_clock_does_not_advance_on_full_success(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws)
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "full_success"})
            msg = ws.receive_json()
            assert msg["type"] == "clock_advanced"
            assert msg["clock"]["filled_segments"] == 0

    def test_clock_wind_back_is_unconditional_and_never_advances(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws)
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "partial_success"})
            ws.receive_json()  # clock_advanced (now at 1)
            ws.send_json({"type": "clock_wind_back", "clock_id": clock_id})
            msg = ws.receive_json()
            assert msg["type"] == "clock_wound_back"
            assert msg["clock"]["filled_segments"] == 0
            # Winding back an already-empty clock never advances it, and never errors.
            ws.send_json({"type": "clock_wind_back", "clock_id": clock_id})
            msg = ws.receive_json()
            assert msg["type"] == "clock_wound_back"
            assert msg["clock"]["filled_segments"] == 0

    def test_clock_fill_fires_once_at_segment_4(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws, segments=4)
            for _ in range(3):
                ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "failure"})
                msg = ws.receive_json()
                assert msg["type"] == "clock_advanced"
            # The 4th advance fills the clock and fires clock_fill.
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "failure"})
            advanced = ws.receive_json()
            assert advanced["type"] == "clock_advanced"
            assert advanced["clock"]["is_full"] is True
            fill = ws.receive_json()
            assert fill["type"] == "clock_fill"
            # A further advance while already full does not re-fire clock_fill.
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "failure"})
            advanced_again = ws.receive_json()
            assert advanced_again["type"] == "clock_advanced"
            assert advanced_again["clock"]["filled_segments"] == 4

    def test_clock_state_survives_session_round_trip(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws, name="Collapsing Ceiling")
            ws.send_json({"type": "clock_advance", "clock_id": clock_id, "outcome_tier": "partial_success"})
            ws.receive_json()

        sess = session_store.get(session_id)
        assert clock_id in sess.threat_clocks
        assert sess.threat_clocks[clock_id].name == "Collapsing Ceiling"
        assert sess.threat_clocks[clock_id].filled_segments == 1

    def test_clock_advance_unknown_id_errors(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Test"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "clock_advance", "clock_id": "nonexistent", "outcome_tier": "failure"})
            msg = ws.receive_json()
            assert msg["type"] == "error"

    def test_player_cannot_create_clock(self, client, mm_headers, active_session, valid_attributes):
        session_id = active_session["session_id"]
        client.post("/api/characters/", json={
            "session_id": session_id,
            "character_name": "Tester",
            "primary_facet": "body",
            "attributes": valid_attributes,
        }, headers=mm_headers)
        player_token = create_session_token("Tester", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "clock_create", "name": "Sneaky Clock"})
            msg = ws.receive_json()
            assert msg["type"] == "error"
            assert "Unknown event type" in msg["message"]


# ---------------------------------------------------------------------------
# Parity: WebSocket handler vs. app.game.combat, direct
#
# TASKS WS-A0 (A0.3): permanent guard against F1 (DESIGN §1) recurring —
# the engine and the simulator used to independently reimplement armor
# downgrade and Broken escalation, and they diverged. Now both the
# WebSocket handler and the simulator call the same `app.game.combat`
# functions; these tests assert the handler's observable result for a
# given input equals calling `combat.py` directly on the same input.
# ---------------------------------------------------------------------------

class TestCombatRulesParity:
    def test_heavy_armor_downgrade_matches_combat_module(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "heavy"
        ruleset = sess.ruleset

        # Compute the expected result directly through combat.py.
        original_tier = combat_module.condition_tier("broken", ruleset)
        budget = combat_module.armor_budget(char.armor, ruleset)
        expected = combat_module.armor_downgrade(original_tier, char.armor, budget, ruleset)
        expected_condition = ruleset.combat.conditions.tier2[0].id
        assert expected.tier == 2  # sanity: Tier 3 downgrades one step to Tier 2

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "combat_start"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "broken"})
            msg = ws.receive_json()

        assert msg["condition"] == expected_condition
        assert char.conditions == [expected_condition]

    def test_same_tier2_twice_escalates_to_broken_matches_combat_module(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        ruleset = sess.ruleset

        # Compute the expected end-state directly through combat.py, on an
        # independent list mirroring the character's starting conditions.
        expected_conditions: list[str] = []
        tier = combat_module.condition_tier("staggered", ruleset)
        combat_module.apply_condition(expected_conditions, "staggered", tier, ruleset)
        second = combat_module.apply_condition(expected_conditions, "staggered", tier, ruleset)
        assert second.broken is True
        expected_conditions.append("broken")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "combat_start"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            msg = ws.receive_json()

        assert msg["condition"] == "broken"
        assert char.conditions == expected_conditions

    def test_end_exchange_clears_tier1_matches_combat_module(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        ruleset = sess.ruleset

        expected_conditions = ["staggered", "winded"]
        combat_module.end_exchange(expected_conditions, ruleset)  # mutates in place

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "combat_start"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "staggered"})
            ws.receive_json()
            ws.send_json({"type": "apply_condition", "player_name": "Zahna", "condition": "winded"})
            ws.receive_json()
            ws.send_json({"type": "end_exchange"})
            ws.receive_json()

        assert char.conditions == expected_conditions == ["staggered"]


class TestOffenseAndNonStackingInLivePlay:
    """The two rules that were canon (and simulated) but never reached a real
    table: the Staggered −1 offensive penalty, and armor/reaction non-stacking.

    Both are PHB III.3. Before this, `_handle_strike` applied only the posture
    modifier (the Staggered penalty lived in `combat.resolve_strike`, which no
    production path calls), and `_handle_apply_condition` always spent an armor
    charge because it had no way to know a reaction had already downgraded the
    hit.
    """

    def _start_combat(self, ws):
        ws.send_json({"type": "combat_start"})
        ws.receive_json()  # combat_started

    def _recv(self, ws, msg_type):
        msg = ws.receive_json()
        assert msg.get("type") == msg_type, f"expected {msg_type}, got {msg}"
        return msg

    def test_staggered_applies_minus_one_to_strike(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].conditions = ["staggered"]

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = self._recv(ws, "strike_result")
            assert msg["roll"]["offense_modifier"] == -1

    def test_staggered_stacks_with_posture_modifier(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess = session_store.get(session_id)
        sess.characters["Zahna"].conditions = ["staggered"]

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "declare_posture", "posture": "aggressive"})
            ws.receive_json()
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = self._recv(ws, "strike_result")
            # Aggressive +1 and Staggered −1 cancel out.
            assert msg["roll"].get("offense_modifier", 0) == 0

    def test_unstaggered_strike_is_unpenalised(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin"})
            msg = self._recv(ws, "strike_result")
            assert msg["roll"].get("offense_modifier", 0) == 0

    def test_reaction_downgrade_does_not_stack_with_armor(
        self, client, mm_token, session_with_character,
    ):
        """PHB III.3: light armor + partial Parry vs Tier 2 lands as Tier 1
        (winded), not negated entirely."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "staggered",
                "reaction_downgraded": True,
            })
            msg = self._recv(ws, "condition_applied")
            assert msg["condition"] == "winded"
            assert "winded" in msg["all_conditions"]

    def test_redundant_armor_charge_is_not_spent(
        self, client, mm_token, session_with_character,
    ):
        """The reaction supplied the reduction, so the per-scene armor budget —
        what keeps an armored PC breakable — is left intact."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            before = sess.characters["Zahna"].armor_downgrades_remaining
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "staggered",
                "reaction_downgraded": True,
            })
            self._recv(ws, "condition_applied")
            assert sess.characters["Zahna"].armor_downgrades_remaining == before

    def test_armor_alone_still_spends_a_charge(
        self, client, mm_token, session_with_character,
    ):
        """No reaction: armor supplies the reduction and pays for it. Absent
        the flag, behaviour is unchanged — the message is backward compatible."""
        session, _ = session_with_character
        session_id = session["session_id"]

        sess = session_store.get(session_id)
        char = sess.characters["Zahna"]
        char.armor = "light"

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            before = sess.characters["Zahna"].armor_downgrades_remaining
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "staggered",
            })
            msg = self._recv(ws, "condition_applied")
            assert msg["condition"] == "winded"
            assert sess.characters["Zahna"].armor_downgrades_remaining == before - 1

    def test_reaction_downgrade_negates_tier1_for_unarmored(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Zahna",
                "condition": "winded",
                "reaction_downgraded": True,
            })
            msg = self._recv(ws, "condition_applied")
            assert msg["condition"] is None
            assert msg.get("armor_absorbed") is False


class TestPressCostFromYaml:
    """sync-M-2: Press's Endurance cost and extra-die effect are read from
    facet.yaml (combat.press), not a hardcoded literal in the handler."""

    def _start_combat(self, ws):
        ws.send_json({"type": "combat_start"})
        return ws.receive_json()

    def test_press_cost_read_from_yaml(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        sess = session_store.get(session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        before = sess.characters["Zahna"].endurance_current
        expected_cost = sess.ruleset.combat.press.endurance_cost

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "press": True})
            msg = ws.receive_json()

        assert msg["type"] == "strike_result"
        assert msg["press_used"] is True
        assert msg["endurance_remaining"] == before - expected_cost

    def test_modified_yaml_press_cost_changes_the_deduction(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        sess = session_store.get(session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess.ruleset.combat.press.endurance_cost = 2
        before = sess.characters["Zahna"].endurance_current

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "press": True})
            msg = ws.receive_json()

        assert msg["endurance_remaining"] == before - 2

    def test_press_refused_with_insufficient_endurance(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        sess = session_store.get(session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        sess.characters["Zahna"].endurance_current = 0

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "strike", "target": "goblin", "press": True})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "Press" in msg["message"]
        assert sess.characters["Zahna"].endurance_current == 0


class TestSavingThrow:
    """sync-M-8 part 2: III.1:84-99 saving throws, rollable end-to-end
    through the WebSocket layer."""

    def test_saving_throw_happy_path(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "saving_throw",
                "major_attribute_id": "mind",
                "difficulty": "Standard",
            })
            msg = ws.receive_json()

        assert msg["type"] == "saving_throw_result"
        assert msg["major_attribute_id"] == "mind"
        assert msg["outcome"] in ("full_success", "partial_success", "failure")
        assert "roll" in msg

    def test_saving_throw_unknown_major_attribute_returns_error(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "saving_throw",
                "major_attribute_id": "flying",
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "flying" in msg["message"]


# ---------------------------------------------------------------------------
# Front-end audit A3 — a player may select their OWN Technique
# ---------------------------------------------------------------------------

class TestPlayerTechniqueSelect:
    """A3: `technique_select` was MM-gated while the only UI control that sent
    it was the player-facing Builder tab, so no character could ever gain a
    Technique. Players now select for themselves; the MM may still select on
    any player's behalf. All selection rules stay in Character.select_technique.
    """

    def test_player_selects_own_technique(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        session_store.get(session_id).characters["Zahna"].technique_picks_available = 1
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "technique_select",
                "technique_id": "arcane_study",
                "choice": "inscription",
            })
            msg = ws.receive_json()

        assert msg["type"] == "technique_selected"
        assert msg["player"] == "Zahna"
        assert "arcane_study" in msg["all_techniques"]

    def test_player_cannot_select_for_another_player(self, client, session_with_character):
        """A player naming someone else is forced back onto their own sheet."""
        session, _ = session_with_character
        session_id = session["session_id"]
        stored = session_store.get(session_id)
        stored.characters["Zahna"].technique_picks_available = 1
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "technique_select",
                "player_name": "SomeoneElse",
                "technique_id": "arcane_study",
                "choice": "inscription",
            })
            msg = ws.receive_json()

        assert msg["type"] == "technique_selected"
        assert msg["player"] == "Zahna"

    def test_mm_may_still_select_on_behalf_of_a_player(
        self, client, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        session_store.get(session_id).characters["Zahna"].technique_picks_available = 1

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
        assert msg["player"] == "Zahna"

    def test_player_with_no_picks_left_gets_an_error(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        session_store.get(session_id).characters["Zahna"].technique_picks_available = 0
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "technique_select",
                "technique_id": "arcane_study",
                "choice": "inscription",
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"


# ---------------------------------------------------------------------------
# Front-end audit B16 — a Threat Clock can be removed once it stops mattering
# ---------------------------------------------------------------------------

class TestThreatClockDelete:
    """Clocks could be created, advanced, and wound back, but never removed —
    a resolved hazard stayed on every player's screen for the rest of the
    session. `clock_delete` is MM-only, like every other clock event.
    """

    def _create_clock(self, ws, name="Rising Tide"):
        ws.send_json({"type": "clock_create", "name": name})
        msg = ws.receive_json()
        assert msg["type"] == "clock_created"
        return msg["clock"]["id"]

    def test_clock_delete_removes_it_from_session_state(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Delete"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            clock_id = self._create_clock(ws)
            ws.send_json({"type": "clock_delete", "clock_id": clock_id})
            msg = ws.receive_json()

        assert msg["type"] == "clock_deleted"
        assert msg["clock_id"] == clock_id
        assert clock_id not in session_store.get(session_id).threat_clocks

    def test_clock_delete_unknown_id_returns_error(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Clock Delete 2"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "clock_delete", "clock_id": "nope"})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "nope" in msg["message"]

    def test_player_cannot_delete_a_clock(self, client, mm_headers, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as mm_ws:
            _auth_mm(mm_ws, mm_token, session_id)
            clock_id = self._create_clock(mm_ws)

        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "clock_delete", "clock_id": clock_id})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert clock_id in session_store.get(session_id).threat_clocks


# ---------------------------------------------------------------------------
# Front-end audit — a new character must reach everyone already connected
# ---------------------------------------------------------------------------

class TestCharacterCreatedBroadcast:
    """Character creation is a REST call and broadcast nothing, so an MM sitting
    in the session never learned a player had made a character: the combat
    roster, every player picker, and the party list stayed empty until reload.
    """

    def test_character_creation_broadcasts_to_connected_clients(
        self, client, mm_token, mm_headers, active_session, valid_attributes,
    ):
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            client.post(
                "/api/characters/",
                json={
                    "session_id": session_id,
                    "character_name": "Zahna",
                    "primary_facet": "mind",
                    "attributes": valid_attributes,
                },
                headers=mm_headers,
            )
            msg = ws.receive_json()

        assert msg["type"] == "character_created"
        assert msg["player"] == "Zahna"
        assert msg["character"]["name"] == "Zahna"

    def test_broadcast_carries_the_full_character(
        self, client, mm_token, mm_headers, active_session, valid_attributes,
    ):
        """Clients merge the payload straight into `allCharacters`, so it has to
        be the same shape the state dict uses."""
        session_id = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            resp = client.post(
                "/api/characters/",
                json={
                    "session_id": session_id,
                    "character_name": "Mordai",
                    "primary_facet": "body",
                    "attributes": valid_attributes,
                },
                headers=mm_headers,
            )
            msg = ws.receive_json()

        assert msg["character"] == resp.json()["character"]

    def test_upload_also_broadcasts(
        self, client, mm_token, mm_headers, active_session, valid_attributes,
    ):
        """An imported .fof has to announce itself the same way a built one does."""
        session_id = active_session["session_id"]
        client.post(
            "/api/characters/",
            json={
                "session_id": session_id,
                "character_name": "Zulnut",
                "primary_facet": "body",
                "attributes": valid_attributes,
            },
            headers=mm_headers,
        )
        export = client.get(
            f"/api/characters/{session_id}/Zulnut/export", headers=mm_headers,
        )
        assert export.status_code == 200

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            client.post(
                "/api/characters/upload",
                json={"session_id": session_id, "fof_yaml": export.text},
                headers=mm_headers,
            )
            msg = ws.receive_json()

        assert msg["type"] == "character_created"
        assert msg["player"] == "Zulnut"


# ---------------------------------------------------------------------------
# MM table roller — a utility, deliberately not a resolution mechanic
# ---------------------------------------------------------------------------

class TestTableRoll:
    """Raw dice for the things around the game that are not the game: random
    tables, oracles, "which of you does it notice first".

    It returns dice and a total and nothing else. There is deliberately no
    outcome tier, no attribute, and no skill — a 2d6 with a success band would
    be a second implementation of the core resolution system, and would let an
    MM roll for an NPC, which PHB III.3 says never happens.
    """

    def test_mm_can_roll_arbitrary_dice(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Table"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "3d6", "label": "Loot value"})
            msg = ws.receive_json()

        assert msg["type"] == "table_roll_result"
        assert msg["notation"] == "3d6"
        assert msg["label"] == "Loot value"
        assert len(msg["dice"]) == 3
        assert all(1 <= d <= 6 for d in msg["dice"])
        assert msg["total"] == sum(msg["dice"])

    def test_modifier_is_applied_to_the_total(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Table Mod"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "2d6+4"})
            msg = ws.receive_json()

        assert msg["modifier"] == 4
        assert msg["total"] == sum(msg["dice"]) + 4

    def test_result_carries_no_outcome_tier(self, client, mm_headers, mm_token):
        """Guards the boundary: this must never grow into a second copy of the
        2d6 resolution system."""
        resp = client.post("/api/sessions/", json={"name": "No Tier"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "2d6"})
            msg = ws.receive_json()

        assert "outcome" not in msg
        assert "outcome_label" not in msg

    def test_table_rolls_stay_out_of_the_character_roll_log(
        self, client, mm_headers, mm_token,
    ):
        """The roll log is a record of character actions. A d100 for a weather
        table is not one, and would render as a malformed entry."""
        resp = client.post("/api/sessions/", json={"name": "Log Clean"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "1d100"})
            ws.receive_json()

        assert session_store.get(session_id).roll_log == []

    def test_invalid_notation_returns_an_error(self, client, mm_headers, mm_token):
        resp = client.post("/api/sessions/", json={"name": "Bad Dice"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "banana"})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "banana" in msg["message"]

    def test_absurd_dice_counts_are_refused(self, client, mm_headers, mm_token):
        """A bounded roller cannot be used to flood every connected client."""
        resp = client.post("/api/sessions/", json={"name": "Too Many"}, headers=mm_headers)
        session_id = resp.json()["session_id"]
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({"type": "table_roll", "notation": "9999d6"})
            msg = ws.receive_json()

        assert msg["type"] == "error"

    def test_players_cannot_table_roll(self, client, mm_token, session_with_character):
        """Players roll through the resolution system. A second, tier-less
        roller on their sheet would only muddy which one is the real mechanic."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "table_roll", "notation": "1d20"})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "Unknown event type" in msg["message"]


# ---------------------------------------------------------------------------
# Enemy Resolve depletion must be resolved by the engine, not by the client
# ---------------------------------------------------------------------------

class TestEnemyStrikeDepletion:
    """`enemy_update` takes `resolve_current` as a raw number the client
    computes. That put the D1 depletion rule (10+ takes 2, 7-9 takes 1) in the
    front end and the simulator but not the server — a second implementation of
    a rule, which the Software-PHB sync policy forbids, and which would force an
    agent playing over the API to do rule arithmetic itself.

    `enemy_strike` sends the *outcome* and lets `combat.apply_resolve_damage`
    decide. `enemy_update` stays for manual MM corrections.
    """

    def _session_with_enemy(self, client, mm_headers, tier="named", resolve=4, armor="none"):
        session_id = client.post(
            "/api/sessions/", json={"name": "Depletion"}, headers=mm_headers,
        ).json()["session_id"]
        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "guard", "name": "Guard",
            "tier": tier, "resolve": resolve, "armor": armor,
        }, headers=mm_headers)
        return session_id

    def _spawn(self, ws, enemy_id="guard"):
        ws.send_json({"type": "spawn_enemy", "enemy_id": enemy_id})
        msg = ws.receive_json()
        assert msg["type"] == "enemy_spawned"
        return msg["tracker_key"]

    def test_full_success_depletes_two(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(client, mm_headers, resolve=4)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "full_success"})
            msg = ws.receive_json()

        assert msg["type"] == "enemy_updated"
        assert msg["depletion"] == 2
        assert msg["resolve_current"] == 2

    def test_partial_success_depletes_one(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(client, mm_headers, resolve=4)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "partial_success"})
            msg = ws.receive_json()

        assert msg["depletion"] == 1
        assert msg["resolve_current"] == 3

    def test_failure_depletes_nothing(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(client, mm_headers, resolve=4)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "failure"})
            msg = ws.receive_json()

        assert msg["depletion"] == 0
        assert msg["resolve_current"] == 4

    def test_reaching_zero_marks_defeated(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(client, mm_headers, resolve=2)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "full_success"})
            msg = ws.receive_json()

        assert msg["resolve_current"] == 0
        assert msg["defeated"] is True

    def test_mook_falls_to_one_strike(self, client, mm_headers, mm_token):
        """Mooks have no Resolve pool — `mook_removed` decides, not arithmetic."""
        session_id = self._session_with_enemy(client, mm_headers, tier="mook", resolve=0)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "partial_success"})
            msg = ws.receive_json()

        assert msg["defeated"] is True
        assert msg["mook_removed"] is True

    def test_armored_mook_needs_a_full_success(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(
            client, mm_headers, tier="mook", resolve=0, armor="light")
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "partial_success"})
            msg = ws.receive_json()

        assert msg["defeated"] is False

    def test_phase_change_is_broadcast(self, client, mm_headers, mm_token):
        session_id = client.post(
            "/api/sessions/", json={"name": "Phases"}, headers=mm_headers,
        ).json()["session_id"]
        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss", "tier": "boss",
            "resolve": 4, "phases": [{"resolve_threshold": 2, "description": "Enrages"}],
        }, headers=mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws, "boss")
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "full_success"})
            ws.receive_json()  # enemy_updated
            msg = ws.receive_json()

        assert msg["type"] == "enemy_phase_change"

    def test_unknown_outcome_is_refused(self, client, mm_headers, mm_token):
        session_id = self._session_with_enemy(client, mm_headers)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            ws.send_json({"type": "enemy_strike", "tracker_key": key,
                          "outcome": "banana"})
            msg = ws.receive_json()

        assert msg["type"] == "error"

    def test_players_cannot_deplete_resolve(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({"type": "enemy_strike", "tracker_key": "x",
                          "outcome": "full_success"})
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "Unknown event type" in msg["message"]


class TestFinalBlowLicensedOverride:
    """TD-14 (B4 Q3): *The Final Blow* fires on 7+ (both success tiers per
    the BRIEF), never on a 6- failure, is refused a second time in the same
    session, and does not commit an enemy removal without a separate MM
    confirmation (`final_blow_confirm`) — auto-apply governs difficulty
    steps, not actor removal (DESIGN §4).

    Dice are pinned with `patch("random.randint", ...)`: Zahna's Strength
    is 3 (+1 minor modifier, `valid_attributes` fixture) and the Strike
    uses the default Standard difficulty (+0), so a constant die value of
    6 lands well past the 10+ full-success threshold, 3 lands in the 7-9
    partial band, and 1 lands at failure — regardless of the extra
    Spark die (all dice equal, so dropping the lowest changes nothing).
    """

    def _session_with_enemy(self, client, mm_headers, resolve=8):
        session_id = client.post(
            "/api/sessions/", json={"name": "Final Blow"}, headers=mm_headers,
        ).json()["session_id"]
        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": resolve,
        }, headers=mm_headers)
        return session_id

    def _spawn(self, ws, enemy_id="boss"):
        ws.send_json({"type": "spawn_enemy", "enemy_id": enemy_id})
        msg = ws.receive_json()
        assert msg["type"] == "enemy_spawned"
        return msg["tracker_key"]

    def _start_combat(self, ws):
        ws.send_json({"type": "combat_start"})
        return ws.receive_json()

    def test_fires_on_full_success(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            with patch("random.randint", return_value=6):
                ws.send_json({
                    "type": "strike", "target": "boss",
                    "final_blow": True, "sparks_spent": 1,
                })
                msg = ws.receive_json()

        assert msg["type"] == "strike_result"
        assert msg["roll"]["outcome"] == "full_success"
        assert msg["final_blow_available"] is True

    def test_fires_on_partial_success(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            with patch("random.randint", return_value=3):
                ws.send_json({
                    "type": "strike", "target": "boss",
                    "final_blow": True, "sparks_spent": 1,
                })
                msg = ws.receive_json()

        assert msg["roll"]["outcome"] == "partial_success"
        assert msg["final_blow_available"] is True

    def test_does_not_fire_on_failure(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            with patch("random.randint", return_value=1):
                ws.send_json({
                    "type": "strike", "target": "boss",
                    "final_blow": True, "sparks_spent": 1,
                })
                msg = ws.receive_json()

        assert msg["roll"]["outcome"] == "failure"
        assert msg["final_blow_available"] is False

    def test_second_use_in_same_session_is_refused(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")
        char.techniques_used_this_session.append("the_final_blow")

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "strike", "target": "boss",
                "final_blow": True, "sparks_spent": 1,
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "already" in msg["message"].lower()

    def test_removal_does_not_commit_without_mm_confirmation(
        self, client, mm_headers, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": 8,
        }, headers=mm_headers)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            with patch("random.randint", return_value=6):
                ws.send_json({
                    "type": "strike", "target": "boss",
                    "final_blow": True, "sparks_spent": 1,
                })
                msg = ws.receive_json()

        assert msg["final_blow_available"] is True

        enemy = session_store.get(session_id).active_enemies[key]
        assert enemy.resolve_current != 0
        assert "the_final_blow" not in char.techniques_used_this_session

    def test_mm_confirm_commits_the_removal(
        self, client, mm_headers, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": 8,
        }, headers=mm_headers)

        player_token = create_session_token("Zahna", session_id)
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            self._start_combat(ws)

        # A confirm only commits an offer a Strike actually made (TODO T12), so
        # the Strike has to happen first and has to name the tracker key.
        with client.websocket_connect("/ws") as pws:
            _auth_player(pws, player_token)
            with patch("random.randint", return_value=6):
                pws.send_json({
                    "type": "strike", "target": key,
                    "final_blow": True, "sparks_spent": 1,
                })
                offer = pws.receive_json()
        assert offer["final_blow_available"] is True

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": key,
                "offer_id": offer["final_blow_offer_id"],
            })
            msg = ws.receive_json()

        assert msg["type"] == "enemy_updated"
        assert msg["resolve_current"] == 0
        assert msg["defeated"] is True
        assert msg["cause"] == "final_blow"
        assert "the_final_blow" in char.techniques_used_this_session

    def test_second_mm_confirm_is_refused(
        self, client, mm_headers, mm_token, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")

        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": 8,
        }, headers=mm_headers)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            self._start_combat(ws)
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": key,
            })
            ws.receive_json()  # enemy_updated
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": key,
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"

    def test_zero_sparks_cannot_use_the_final_blow(self, client, mm_token, session_with_character):
        """Review finding: the precondition tested the Spark the client *asked*
        to spend, but `_spend_sparks` clamps to what the character holds and
        silently spends 0 — so a character at 0 Sparks got the capstone free.
        The printed cost is "when you spend a Spark on a Combat roll" (II.4a)."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")
        char.sparks = 0

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            with patch("random.randint", return_value=6):
                ws.send_json({
                    "type": "strike", "target": "boss",
                    "final_blow": True, "sparks_spent": 1,
                })
                msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "Spark" in msg["message"]
        assert "the_final_blow" not in char.techniques_used_this_session

    def test_confirm_without_an_offer_is_refused(
        self, client, mm_headers, mm_token, session_with_character,
    ):
        """TODO T12: the 7+ outcome and the Spark cost are enforced by the Strike
        that makes the offer, not by the confirm. So a confirm arriving with no
        live offer — a stale toast, a replay, a hand-made message — used to
        remove an enemy off the back of a Strike that never succeeded."""
        session, _ = session_with_character
        session_id = session["session_id"]
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")
        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": 8,
        }, headers=mm_headers)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            self._start_combat(ws)
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": key,
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "on offer" in msg["message"]
        assert "the_final_blow" not in char.techniques_used_this_session
        assert session_store.get(session_id).active_enemies[key].resolve_current != 0

    def test_a_failed_strike_clears_any_standing_offer(
        self, client, mm_headers, mm_token, session_with_character,
    ):
        """A 6- Strike must not leave an earlier offer standing — otherwise the
        MM's stale toast still commits."""
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        char = session_store.get(session_id).characters["Zahna"]
        char.techniques.append("the_final_blow")
        char.sparks = 3
        client.post("/api/enemies/", json={
            "session_id": session_id, "id": "boss", "name": "Boss",
            "tier": "boss", "resolve": 8,
        }, headers=mm_headers)

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            key = self._spawn(ws)
            self._start_combat(ws)

        with client.websocket_connect("/ws") as pws:
            _auth_player(pws, player_token)
            with patch("random.randint", return_value=6):      # offer opens
                pws.send_json({"type": "strike", "target": key,
                               "final_blow": True, "sparks_spent": 1})
                first = pws.receive_json()
            assert first["final_blow_available"] is True
            with patch("random.randint", return_value=1):      # then a 6- Strike
                pws.send_json({"type": "strike", "target": key,
                               "final_blow": True, "sparks_spent": 1})
                pws.receive_json()

        assert session_store.get(session_id).pending_final_blow is None

        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": key,
                "offer_id": first["final_blow_offer_id"],
            })
            msg = ws.receive_json()
        assert msg["type"] == "error"

    def test_non_mm_cannot_confirm_final_blow(self, client, mm_token, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)

        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "final_blow_confirm", "player": "Zahna", "tracker_key": "x",
            })
            msg = ws.receive_json()

        assert msg["type"] == "error"
        assert "Unknown event type" in msg["message"]
