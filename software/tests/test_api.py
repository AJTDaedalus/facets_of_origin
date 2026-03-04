"""Integration tests for the FastAPI HTTP endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.auth.tokens import create_invite_token, create_session_token


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

class TestHealthCheck:
    def test_health_returns_ok(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# MM Auth
# ---------------------------------------------------------------------------

class TestMMAuth:
    def test_setup_mm_password(self, client):
        """First-run setup sets the password. Note: once set it persists for the test session."""
        # Reset by overriding
        from app.api.routes.session import set_mm_password, _get_mm_hash
        import app.api.routes.session as session_mod
        session_mod._mm_password_hash = None

        resp = client.post("/api/sessions/auth/setup", json={"password": "securepass1"})
        assert resp.status_code == 200

    def test_setup_cannot_be_called_twice(self, client):
        from app.api.routes.session import set_mm_password
        set_mm_password("alreadyset")
        resp = client.post("/api/sessions/auth/setup", json={"password": "newpassword"})
        assert resp.status_code == 400

    def test_mm_login_with_correct_password(self, client, mm_password):
        resp = client.post("/api/sessions/auth/mm-login", json={"password": mm_password})
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_mm_login_wrong_password(self, client, mm_password):
        resp = client.post("/api/sessions/auth/mm-login", json={"password": "wrongpassword"})
        assert resp.status_code == 401

    def test_mm_login_returns_bearer_token(self, client, mm_password):
        resp = client.post("/api/sessions/auth/mm-login", json={"password": mm_password})
        assert resp.json()["token_type"] == "bearer"


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

class TestSessionManagement:
    def test_create_session_requires_auth(self, client):
        resp = client.post("/api/sessions/", json={"name": "Test"})
        assert resp.status_code == 401

    def test_create_session_with_mm_token(self, client, mm_headers):
        resp = client.post("/api/sessions/", json={"name": "Adventure"}, headers=mm_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "session_id" in data
        assert data["name"] == "Adventure"

    def test_list_sessions_requires_auth(self, client):
        resp = client.get("/api/sessions/")
        assert resp.status_code == 401

    def test_list_sessions_returns_sessions(self, client, mm_headers):
        client.post("/api/sessions/", json={"name": "Session 1"}, headers=mm_headers)
        resp = client.get("/api/sessions/", headers=mm_headers)
        assert resp.status_code == 200
        assert "sessions" in resp.json()

    def test_create_session_with_player_token_fails(self, client):
        player_token = create_session_token("Alice", "some-session")
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/sessions/", json={"name": "Sneaky"}, headers=headers)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Invite links
# ---------------------------------------------------------------------------

class TestInviteLinks:
    def test_create_invite_for_valid_session(self, client, mm_headers, active_session):
        resp = client.post(
            "/api/sessions/invite",
            json={"player_name": "Zahna", "session_id": active_session["session_id"]},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "invite_url" in data
        assert "Zahna" in data["player_name"]

    def test_invite_for_nonexistent_session_returns_404(self, client, mm_headers):
        resp = client.post(
            "/api/sessions/invite",
            json={"player_name": "Zahna", "session_id": "no-such-session"},
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_invite_url_contains_token(self, client, mm_headers, active_session):
        resp = client.post(
            "/api/sessions/invite",
            json={"player_name": "Mordai", "session_id": active_session["session_id"]},
            headers=mm_headers,
        )
        url = resp.json()["invite_url"]
        assert "token=" in url

    def test_redeem_invite_returns_session_token(self, client, active_session):
        token = create_invite_token("Zulnut", active_session["session_id"])
        resp = client.post("/api/sessions/join", json={"invite_token": token})
        assert resp.status_code == 200
        data = resp.json()
        assert data["player_name"] == "Zulnut"
        assert data["session_id"] == active_session["session_id"]
        assert "access_token" in data

    def test_redeem_invite_single_use(self, client, active_session):
        token = create_invite_token("SingleUse", active_session["session_id"])
        resp1 = client.post("/api/sessions/join", json={"invite_token": token})
        assert resp1.status_code == 200
        resp2 = client.post("/api/sessions/join", json={"invite_token": token})
        assert resp2.status_code == 400

    def test_redeem_invalid_token_rejected(self, client):
        resp = client.post("/api/sessions/join", json={"invite_token": "garbage.token.here"})
        assert resp.status_code == 401

    def test_redeem_mm_token_as_invite_rejected(self, client):
        mm_token = create_mm_token()
        resp = client.post("/api/sessions/join", json={"invite_token": mm_token})
        assert resp.status_code == 400  # Not an invite token


# ---------------------------------------------------------------------------
# Character API
# ---------------------------------------------------------------------------

class TestCharacterAPI:
    def test_create_character_with_mm_token(self, client, mm_headers, active_session, valid_attributes):
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Zahna",
                "primary_facet": "mind",
                "attributes": valid_attributes,
            },
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["character"]["name"] == "Zahna"

    def test_create_character_invalid_attributes_returns_422(self, client, mm_headers, active_session):
        bad_attrs = {"strength": 5, "dexterity": 5, "constitution": 5,
                     "intelligence": 5, "wisdom": 5, "knowledge": 5,
                     "spirit": 5, "luck": 5, "charisma": 5}
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Invalid",
                "primary_facet": "body",
                "attributes": bad_attrs,
            },
            headers=mm_headers,
        )
        assert resp.status_code == 422

    def test_list_characters_requires_auth(self, client, active_session):
        resp = client.get(f"/api/characters/{active_session['session_id']}")
        assert resp.status_code == 401

    def test_list_characters_returns_characters(self, client, mm_headers, session_with_character):
        session, _ = session_with_character
        resp = client.get(f"/api/characters/{session['session_id']}", headers=mm_headers)
        assert resp.status_code == 200
        assert "characters" in resp.json()

    def test_player_creates_own_character(self, client, active_session, valid_attributes):
        """A player with a valid session token can create a character."""
        session_id = active_session["session_id"]
        player_token = create_session_token("Alice", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": session_id,
                "character_name": "Alice the Brave",
                "primary_facet": "body",
                "attributes": valid_attributes,
            },
            headers=headers,
        )
        assert resp.status_code == 200

    def test_player_cannot_create_char_in_other_session(self, client, active_session, valid_attributes):
        player_token = create_session_token("Alice", "different-session-id")
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Alice",
                "primary_facet": "body",
                "attributes": valid_attributes,
            },
            headers=headers,
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Facets API
# ---------------------------------------------------------------------------

class TestFacetsAPI:
    def test_list_facets_requires_auth(self, client):
        resp = client.get("/api/facets/available")
        assert resp.status_code == 401

    def test_list_facets_returns_base(self, client, mm_headers):
        resp = client.get("/api/facets/available", headers=mm_headers)
        assert resp.status_code == 200
        facet_ids = [f["id"] for f in resp.json()["facets"] if "id" in f]
        assert "base" in facet_ids


# ---------------------------------------------------------------------------
# Roll endpoint
# ---------------------------------------------------------------------------

class TestRollEndpoint:
    def test_roll_requires_auth(self, client, active_session):
        resp = client.post("/api/rolls/", json={
            "session_id": active_session["session_id"],
            "attribute_id": "strength",
        })
        assert resp.status_code == 401

    def test_roll_returns_result(self, client, session_with_character, valid_attributes):
        session, char = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "attribute_id": "intelligence",
            "difficulty": "Standard",
            "sparks_spent": 0,
        }, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "roll" in data
        assert data["roll"]["outcome"] in ("full_success", "partial_success", "failure")

    def test_roll_total_is_correct_type(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "attribute_id": "intelligence",
        }, headers=headers)
        total = resp.json()["roll"]["total"]
        assert isinstance(total, int)

    def test_roll_unknown_attribute_returns_422(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "attribute_id": "nonexistent",
        }, headers=headers)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

class TestSecurityHeaders:
    def test_x_content_type_options_set(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options_set(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("x-frame-options") == "DENY"

    def test_referrer_policy_set(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("referrer-policy") == "no-referrer"

    def test_csp_header_present(self, client):
        resp = client.get("/api/health")
        assert "content-security-policy" in resp.headers
