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
        assert "Player1" in d["all_characters"]

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


# ---------------------------------------------------------------------------
# Duplicate character overwrites
# ---------------------------------------------------------------------------

class TestDuplicateCharacter:
    def test_adding_same_player_name_overwrites(self, session, body_character, ruleset):
        from tests.conftest import make_caster
        session.add_character(body_character)
        assert session.characters["Player1"].name == "Mordai"
        session.add_character(make_caster(ruleset, name="Zaryn", player_name="Player1"))
        assert session.characters["Player1"].name == "Zaryn"


# ---------------------------------------------------------------------------
# Roll log cap
# ---------------------------------------------------------------------------

class TestRollLogCap:
    def test_roll_log_exactly_50_returns_50(self, session):
        for i in range(50):
            session.record_roll("p", {"total": i})
        d = session.to_state_dict()
        assert len(d["roll_log"]) == 50

    def test_roll_log_51_returns_last_50(self, session):
        for i in range(51):
            session.record_roll("p", {"total": i})
        d = session.to_state_dict()
        assert len(d["roll_log"]) == 50
        # Most recent 50 — the first entry's total should be 1
        assert d["roll_log"][0]["total"] == 1

    def test_roll_log_100_still_capped_at_50(self, session):
        for i in range(100):
            session.record_roll("p", {"total": i})
        d = session.to_state_dict()
        assert len(d["roll_log"]) == 50


# ---------------------------------------------------------------------------
# Session name edge cases
# ---------------------------------------------------------------------------

class TestSessionNameEdgeCases:
    def test_session_name_with_special_chars(self, store):
        s = store.create_session("Campaign: The Shattered Crown!")
        assert s.name == "Campaign: The Shattered Crown!"

    def test_session_name_with_unicode(self, store):
        s = store.create_session("Le Voyage — \u00e0 travers le miroir")
        assert "miroir" in s.name

    def test_list_sessions_with_zero(self, store):
        listing = store.list_sessions()
        assert isinstance(listing, list)

    def test_list_sessions_with_one(self, store, session):
        listing = store.list_sessions()
        assert len(listing) >= 1

    def test_list_sessions_with_many(self, store):
        for i in range(5):
            store.create_session(f"Session {i}")
        listing = store.list_sessions()
        assert len(listing) >= 5


# ---------------------------------------------------------------------------
# State dict completeness
# ---------------------------------------------------------------------------

class TestStateDictCompleteness:
    def test_to_state_dict_has_all_keys(self, session):
        d = session.to_state_dict()
        for key in ("session_id", "session_name", "all_characters", "ruleset", "roll_log",
                    "enemy_library", "encounter_library", "active_enemies"):
            assert key in d, f"Missing key: {key}"

    def test_to_player_state_dict_has_all_keys(self, session):
        d = session.to_player_state_dict("nobody")
        for key in ("session_id", "session_name", "your_character", "all_characters",
                    "ruleset", "roll_log", "active_enemies"):
            assert key in d, f"Missing key: {key}"

    def test_ruleset_in_state_dict_is_dict(self, session):
        d = session.to_state_dict()
        assert isinstance(d["ruleset"], dict)

    def test_session_name_preserved_in_state(self, store):
        s = store.create_session("My Campaign")
        d = s.to_state_dict()
        assert d["session_name"] == "My Campaign"


class TestCombatAndDanger:
    def test_start_combat_opens_exchange_one(self, session):
        state = session.start_combat()
        assert state.exchange == 1
        assert session.to_state_dict()["combat"]["exchange"] == 1

    def test_end_exchange_without_combat_raises(self, session):
        with pytest.raises(ValueError):
            session.end_exchange()

    def test_end_exchange_keeps_named_openings_and_drops_stunts(self, session, ruleset):
        from tests.conftest import make_enemy
        session.start_combat()
        foe = make_enemy().spawn(ruleset)
        foe.openings = ["Mordai", "*"]
        foe.studied = True
        session.active_enemies[foe.key] = foe
        assert session.end_exchange() == 2
        assert foe.openings == ["Mordai"]
        assert foe.studied is False

    def test_end_combat_clears_state(self, session):
        session.start_combat()
        session.end_combat()
        assert session.combat is None

    def test_party_level_defaults_to_one(self, session):
        assert session.party_level() == 1
        assert session.party_size() == 1

    def test_active_danger_reads_the_tracker(self, session, ruleset, body_character):
        from tests.conftest import make_enemy
        session.characters[body_character.player_name] = body_character
        for i in range(2):
            e = make_enemy(id=f"s{i}").spawn(ruleset, key=f"s{i}")
            session.active_enemies[e.key] = e
        assert session.active_danger()["read"] == "deadly"      # 2 points vs 1 PC

    def test_defeated_foes_leave_the_danger_read(self, session, ruleset, body_character):
        from tests.conftest import make_enemy
        session.characters[body_character.player_name] = body_character
        e = make_enemy().spawn(ruleset)
        e.defeated = True
        session.active_enemies[e.key] = e
        assert session.active_danger()["points"] == 0


class TestSessionEnd:
    def test_prompts_are_the_five_from_the_ruleset(self, session):
        data = session.end_session_prompts()
        assert [p["id"] for p in data["prompts"]] == [
            "discovery", "treasure", "goal", "change", "moment"]
        assert data["pacing_suggests_level"] == 2          # after session 1

    def test_call_level_up_marks_characters_ready(self, session, body_character):
        session.characters[body_character.player_name] = body_character
        assert session.call_level_up() == ["Player1"]
        assert session.to_player_state_dict("Player1")["level_up_ready"] is True

    def test_call_level_up_unknown_player_raises(self, session):
        with pytest.raises(ValueError):
            session.call_level_up(["Nobody"])

    def test_next_session_resets_sparks_without_carry_over(self, session, body_character):
        body_character.sparks = 7
        session.characters[body_character.player_name] = body_character
        assert session.next_session() == 2
        assert body_character.sparks == 3

    def test_natural_two_failure_confirms_graceful_fail(self, session, body_character):
        session.characters[body_character.player_name] = body_character
        roll = {"outcome": "failure", "natural_low": True}
        assert session.confirm_natural_two_graceful_fail("Player1", roll) is True
        assert body_character.sparks == 4
        assert roll["graceful_fail_claimed"] is True

    def test_natural_two_on_success_does_not_fire(self, session, body_character):
        session.characters[body_character.player_name] = body_character
        assert not session.confirm_natural_two_graceful_fail(
            "Player1", {"outcome": "partial_success", "natural_low": True})


class TestPlayerView:
    def test_player_view_hides_the_card(self, session, ruleset):
        from tests.conftest import make_enemy
        e = make_enemy().spawn(ruleset)
        session.active_enemies[e.key] = e
        view = session.to_player_state_dict("nobody")["active_enemies"][e.key]
        assert "special" not in view and "twists" not in view
        assert view["name"] == e.name
