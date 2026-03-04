"""Tests for session store and session state management."""
import pytest

from app.game.session import GameSession, SessionStore
from app.facets.registry import build_ruleset


@pytest.fixture
def store():
    return SessionStore()


@pytest.fixture
def session(store):
    return store.create_session("Test Campaign")


class TestSessionCreation:
    def test_session_has_id(self, session):
        assert session.id

    def test_session_has_name(self, session):
        assert session.name == "Test Campaign"

    def test_session_starts_with_no_characters(self, session):
        assert len(session.characters) == 0

    def test_session_ruleset_loaded(self, session):
        assert session.ruleset is not None

    def test_session_stored_in_store(self, store, session):
        retrieved = store.get(session.id)
        assert retrieved is session

    def test_nonexistent_session_returns_none(self, store):
        assert store.get("no-such-id") is None

    def test_list_sessions_includes_created(self, store, session):
        sessions = store.list_sessions()
        ids = [s["id"] for s in sessions]
        assert session.id in ids


class TestSessionCharacters:
    def test_add_character(self, session, body_character):
        session.add_character(body_character)
        assert "Player1" in session.characters

    def test_add_character_retrievable(self, session, body_character):
        session.add_character(body_character)
        assert session.characters["Player1"].name == "Mordai"


class TestRollLog:
    def test_record_roll_appends(self, session):
        session.record_roll("Player1", {"outcome": "full_success", "total": 10})
        assert len(session.roll_log) == 1

    def test_record_roll_includes_player_name(self, session):
        session.record_roll("Zahna", {"outcome": "failure", "total": 5})
        assert session.roll_log[0]["player_name"] == "Zahna"

    def test_record_roll_includes_timestamp(self, session):
        session.record_roll("Zahna", {"total": 8})
        assert "timestamp" in session.roll_log[0]


class TestInviteTokenTracking:
    def test_unused_token_returns_false(self, store, session):
        assert not store.is_invite_used(session.id, "some-token")

    def test_used_token_returns_true(self, store, session):
        store.mark_invite_used(session.id, "some-token")
        assert store.is_invite_used(session.id, "some-token")

    def test_different_token_still_unused(self, store, session):
        store.mark_invite_used(session.id, "used-token")
        assert not store.is_invite_used(session.id, "other-token")


class TestStateDict:
    def test_to_state_dict_includes_session_id(self, session):
        d = session.to_state_dict()
        assert d["session_id"] == session.id

    def test_to_state_dict_includes_characters(self, session, body_character):
        session.add_character(body_character)
        d = session.to_state_dict()
        assert "Player1" in d["characters"]

    def test_to_state_dict_roll_log_capped(self, session):
        for i in range(100):
            session.record_roll("p", {"total": i})
        d = session.to_state_dict()
        assert len(d["roll_log"]) <= 50

    def test_to_player_state_dict_has_own_character(self, session, body_character):
        session.add_character(body_character)
        d = session.to_player_state_dict("Player1")
        assert d["your_character"]["name"] == "Mordai"

    def test_to_player_state_dict_no_char_returns_none(self, session):
        d = session.to_player_state_dict("UnknownPlayer")
        assert d["your_character"] is None
