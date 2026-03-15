"""Integration tests for the FastAPI HTTP endpoints."""
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.auth.tokens import create_invite_token, create_mm_token, create_session_token

SPEC_EXAMPLES = Path(__file__).parent.parent.parent / "spec" / "examples"


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

    def test_invalid_background_id_returns_422(self, client, mm_headers, active_session, valid_attributes):
        """B3.3: Creating a character with an unknown background_id must return 422."""
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Zahna",
                "primary_facet": "mind",
                "attributes": valid_attributes,
                "background_id": "nonexistent_bg_xyz",
            },
            headers=mm_headers,
        )
        assert resp.status_code == 422

    def test_background_guild_apprentice_replaces_secondary_with_domain(
        self, client, mm_headers, active_session, valid_attributes
    ):
        """Guild Apprentice: choosing a magic domain skips secondary skill (investigate)."""
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Lyra",
                "primary_facet": "mind",
                "attributes": valid_attributes,
                "background_id": "guild_apprentice",
                "magic_domain": "warding",
            },
            headers=mm_headers,
        )
        assert resp.status_code == 200
        char = resp.json()["character"]
        # Starting skill: lore at practiced
        assert char["skills"]["lore"]["rank"] == "practiced"
        # Secondary skill (investigate) is SKIPPED because domain replaces it
        assert char["skills"]["investigate"]["marks"] == 0
        # Magic domain is set
        assert char["magic_domain"] == "warding"
        assert char["career_advances"] == 1

    def test_background_guild_apprentice_no_domain_keeps_secondary(
        self, client, mm_headers, active_session, valid_attributes
    ):
        """Guild Apprentice: without a magic domain, secondary skill (investigate) is granted."""
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Scholar",
                "primary_facet": "mind",
                "attributes": valid_attributes,
                "background_id": "guild_apprentice",
            },
            headers=mm_headers,
        )
        assert resp.status_code == 200
        char = resp.json()["character"]
        assert char["skills"]["lore"]["rank"] == "practiced"
        assert char["skills"]["investigate"]["marks"] == 1  # secondary granted
        assert char["magic_domain"] is None

    def test_background_temple_acolyte_keeps_secondary_with_domain(
        self, client, mm_headers, active_session, valid_attributes
    ):
        """Temple Acolyte: choosing a magic domain does NOT skip secondary skill (perform)."""
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Sable",
                "primary_facet": "soul",
                "attributes": valid_attributes,
                "background_id": "temple_acolyte",
                "magic_domain": "resonance",
            },
            headers=mm_headers,
        )
        assert resp.status_code == 200
        char = resp.json()["character"]
        # Starting skill: attune at practiced
        assert char["skills"]["attune"]["rank"] == "practiced"
        # Secondary skill (perform) is KEPT even with magic domain
        assert char["skills"]["perform"]["marks"] == 1
        # Magic domain is set
        assert char["magic_domain"] == "resonance"
        assert char["career_advances"] == 1

    def test_background_city_watch_veteran_no_domain(
        self, client, mm_headers, active_session, valid_attributes
    ):
        """City Watch Veteran: non-magical background with secondary skill."""
        resp = client.post(
            "/api/characters/",
            json={
                "session_id": active_session["session_id"],
                "character_name": "Rowan",
                "primary_facet": "body",
                "attributes": valid_attributes,
                "background_id": "city_watch_veteran",
            },
            headers=mm_headers,
        )
        assert resp.status_code == 200
        char = resp.json()["character"]
        assert char["skills"]["combat"]["rank"] == "practiced"
        assert char["skills"]["endurance"]["marks"] == 1
        assert char["magic_domain"] is None


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


# ---------------------------------------------------------------------------
# Malformed JSON / missing fields (422 responses)
# ---------------------------------------------------------------------------

class TestMalformedRequests:
    def test_setup_missing_password_returns_422(self, client):
        resp = client.post("/api/sessions/auth/setup", json={})
        assert resp.status_code == 422

    def test_create_session_missing_name_returns_422(self, client, mm_headers):
        resp = client.post("/api/sessions/", json={}, headers=mm_headers)
        assert resp.status_code == 422

    def test_create_character_missing_session_id_returns_422(self, client, mm_headers):
        resp = client.post("/api/characters/", json={
            "character_name": "Test",
            "primary_facet": "body",
            "attributes": {},
        }, headers=mm_headers)
        assert resp.status_code == 422

    def test_roll_missing_session_id_returns_422(self, client, mm_headers):
        resp = client.post("/api/rolls/", json={
            "attribute_id": "strength",
        }, headers=mm_headers)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Password length edge cases
# ---------------------------------------------------------------------------

class TestPasswordLengthBoundary:
    def _reset_password(self):
        import app.api.routes.session as s
        s._mm_password_hash = None

    def test_7_char_password_rejected_by_setup(self, client):
        self._reset_password()
        resp = client.post("/api/sessions/auth/setup", json={"password": "seven77"})
        assert resp.status_code == 422

    def test_8_char_password_accepted_by_setup(self, client):
        self._reset_password()
        resp = client.post("/api/sessions/auth/setup", json={"password": "eight888"})
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Roll with all four difficulties via HTTP
# ---------------------------------------------------------------------------

class TestRollDifficulties:
    @pytest.mark.parametrize("difficulty", ["Easy", "Standard", "Hard", "Very Hard"])
    def test_roll_all_difficulties(self, client, session_with_character, difficulty):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "attribute_id": "intelligence",
            "difficulty": difficulty,
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["roll"]["outcome"] in ("full_success", "partial_success", "failure")


# ---------------------------------------------------------------------------
# Facets API — extra coverage
# ---------------------------------------------------------------------------

class TestFacetsAPIExtra:
    def test_facets_response_does_not_include_path(self, client, mm_headers):
        """File paths must not be exposed to clients."""
        resp = client.get("/api/facets/available", headers=mm_headers)
        assert resp.status_code == 200
        for facet in resp.json()["facets"]:
            assert "path" not in facet

    def test_facets_includes_version(self, client, mm_headers):
        resp = client.get("/api/facets/available", headers=mm_headers)
        base = next(f for f in resp.json()["facets"] if f.get("id") == "base")
        assert "version" in base


# ---------------------------------------------------------------------------
# Player token session mismatch
# ---------------------------------------------------------------------------

class TestPlayerSessionMismatch:
    def test_roll_with_mismatched_session_token_rejected(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        # Token for a DIFFERENT session
        player_token = create_session_token("Zahna", "completely-different-session-id")
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "attribute_id": "intelligence",
        }, headers=headers)
        assert resp.status_code == 403

    def test_list_characters_with_player_token_allowed(self, client, session_with_character):
        session, _ = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.get(f"/api/characters/{session_id}", headers=headers)
        assert resp.status_code == 200

    def test_invite_for_session_not_found_returns_404(self, client, mm_headers):
        resp = client.post("/api/sessions/invite", json={
            "player_name": "Alice",
            "session_id": "nonexistent-session",
        }, headers=mm_headers)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Rate limiting (H-01)
# ---------------------------------------------------------------------------

class TestRateLimiting:
    """Verify that rate-limited endpoints return 429 after the limit is exhausted."""

    @pytest.fixture(autouse=True)
    def reset_limiter(self, reset_limiter):
        """Use the shared reset_limiter fixture to clear state around every test."""

    def test_setup_rate_limit(self, client):
        """setup endpoint returns 429 after 5 requests from the same IP."""
        # The first 5 requests succeed or fail normally (password may already be set)
        for _ in range(5):
            client.post("/api/sessions/auth/setup", json={"password": "testpassword"})
        resp = client.post("/api/sessions/auth/setup", json={"password": "testpassword"})
        assert resp.status_code == 429

    def test_login_rate_limit(self, client, mm_password):
        """mm-login endpoint returns 429 after 5 requests from the same IP."""
        for _ in range(5):
            client.post("/api/sessions/auth/mm-login", json={"password": "wrongpassword"})
        resp = client.post("/api/sessions/auth/mm-login", json={"password": "wrongpassword"})
        assert resp.status_code == 429

    def test_rate_limit_response_is_json(self, client):
        """429 response body is valid JSON."""
        for _ in range(5):
            client.post("/api/sessions/auth/setup", json={"password": "testpassword"})
        resp = client.post("/api/sessions/auth/setup", json={"password": "testpassword"})
        assert resp.status_code == 429
        data = resp.json()
        assert "error" in data


# ---------------------------------------------------------------------------
# Character upload endpoint
# ---------------------------------------------------------------------------

# Zahna's attributes from character-example.fof (sum = 18)
_ZAHNA_ATTRIBUTES = {
    "strength": 1, "dexterity": 2, "constitution": 2,
    "intelligence": 3, "wisdom": 3, "knowledge": 2,
    "spirit": 1, "luck": 2, "charisma": 2,
}


def _make_character_fof_yaml(player_name: str, session_id: str | None = None) -> str:
    """Build a minimal valid character .fof YAML string."""
    fof_dict = {
        "fof_version": "0.1",
        "type": "character",
        "id": f"{player_name.lower()}-test",
        "name": player_name,
        "version": "1.0.0",
        "authors": [player_name],
        "ruleset": {"modules": [{"id": "base", "version": "0.1.0"}]},
        "campaign_id": session_id or "test-session",
        "character": {
            "name": player_name,
            "player_name": player_name,
            "primary_facet": "mind",
            "attributes": _ZAHNA_ATTRIBUTES,
            "skills": {"investigate": {"rank": "practiced", "marks": 2}},
            "sparks": 2,
            "session_skill_points_remaining": 4,
            "facet_level": 1,
            "rank_advances_this_facet_level": 3,
            "techniques": [],
        },
    }
    return yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)


class TestCharacterUpload:
    def test_upload_character_fof_with_mm_token(self, client, mm_headers, active_session):
        session_id = active_session["session_id"]
        fof_yaml = _make_character_fof_yaml("Zahna", session_id)
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        char = resp.json()["character"]
        assert char["name"] == "Zahna"
        assert char["primary_facet"] == "mind"

    def test_upload_character_appears_in_session(self, client, mm_headers, active_session):
        session_id = active_session["session_id"]
        fof_yaml = _make_character_fof_yaml("Mordai", session_id)
        client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        resp = client.get(f"/api/characters/{session_id}", headers=mm_headers)
        assert "Mordai" in resp.json()["characters"]

    def test_upload_writes_fof_file_to_disk(self, client, mm_headers, active_session, tmp_path):
        """After upload, a .fof file should exist in the session's character dir."""
        from app.game.session import session_store
        session_id = active_session["session_id"]
        fof_yaml = _make_character_fof_yaml("DiskTest", session_id)
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        session = session_store.get(session_id)
        assert session is not None
        assert session._character_dir is not None
        fof_path = session._character_dir / "DiskTest.fof"
        assert fof_path.exists(), f"Expected {fof_path} to exist after upload"

    def test_upload_invalid_yaml_returns_400(self, client, mm_headers, active_session):
        session_id = active_session["session_id"]
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": ":: invalid: yaml: ["},
            headers=mm_headers,
        )
        assert resp.status_code == 400

    def test_upload_wrong_type_returns_400(self, client, mm_headers, active_session):
        session_id = active_session["session_id"]
        ruleset_fof = (SPEC_EXAMPLES / "base-ruleset.fof").read_text(encoding="utf-8")
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": ruleset_fof},
            headers=mm_headers,
        )
        assert resp.status_code == 400

    def test_upload_with_player_token_own_character(self, client, active_session):
        session_id = active_session["session_id"]
        player_token = create_session_token("Alice", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        fof_yaml = _make_character_fof_yaml("Alice", session_id)
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=headers,
        )
        assert resp.status_code == 200

    def test_upload_with_wrong_player_name_returns_403(self, client, active_session):
        """Player uploading a character with a different player_name must be rejected."""
        session_id = active_session["session_id"]
        player_token = create_session_token("Alice", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        # .fof says player_name is Bob, but token says Alice
        fof_yaml = _make_character_fof_yaml("Bob", session_id)
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=headers,
        )
        assert resp.status_code == 403

    def test_upload_session_not_found_returns_404(self, client, mm_headers):
        fof_yaml = _make_character_fof_yaml("Ghost")
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": "no-such-session", "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_upload_character_example_fof(self, client, mm_headers, active_session):
        """The canonical character-example.fof from spec/ should upload successfully."""
        session_id = active_session["session_id"]
        fof_yaml = (SPEC_EXAMPLES / "character-example.fof").read_text(encoding="utf-8")
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["character"]["name"] == "Zahna"


class TestCharacterExport:
    def test_export_character_as_yaml(self, client, mm_headers, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_name = char["player_name"]
        resp = client.get(
            f"/api/characters/{session_id}/{player_name}/export",
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("application/yaml")

    def test_export_content_disposition(self, client, mm_headers, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_name = char["player_name"]
        resp = client.get(
            f"/api/characters/{session_id}/{player_name}/export",
            headers=mm_headers,
        )
        assert f'filename="{player_name}.fof"' in resp.headers["content-disposition"]

    def test_export_is_valid_yaml(self, client, mm_headers, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_name = char["player_name"]
        resp = client.get(
            f"/api/characters/{session_id}/{player_name}/export",
            headers=mm_headers,
        )
        parsed = yaml.safe_load(resp.text)
        assert parsed["type"] == "character"
        assert parsed["character"]["name"] == char["name"]

    def test_export_reimport_roundtrip(self, client, mm_headers, active_session, valid_attributes):
        """Export → re-upload should produce an identical character."""
        session_id = active_session["session_id"]
        # Create the character
        client.post(
            "/api/characters/",
            json={
                "session_id": session_id,
                "character_name": "Roundtrip",
                "primary_facet": "body",
                "attributes": valid_attributes,
            },
            headers=mm_headers,
        )
        # Export
        export_resp = client.get(
            f"/api/characters/{session_id}/Roundtrip/export",
            headers=mm_headers,
        )
        assert export_resp.status_code == 200

        # Re-upload (overwrites same character)
        upload_resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": export_resp.text},
            headers=mm_headers,
        )
        assert upload_resp.status_code == 200
        reimported = upload_resp.json()["character"]
        assert reimported["name"] == "Roundtrip"
        assert reimported["primary_facet"] == "body"

    def test_export_session_not_found_returns_404(self, client, mm_headers):
        resp = client.get(
            "/api/characters/no-such-session/SomePlayer/export",
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_export_character_not_found_returns_404(self, client, mm_headers, active_session):
        session_id = active_session["session_id"]
        resp = client.get(
            f"/api/characters/{session_id}/NoSuchPlayer/export",
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_player_can_export_own_character(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_name = char["player_name"]
        player_token = create_session_token(player_name, session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.get(
            f"/api/characters/{session_id}/{player_name}/export",
            headers=headers,
        )
        assert resp.status_code == 200

    def test_player_cannot_export_other_character(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_name = char["player_name"]
        other_token = create_session_token("SomeOtherPlayer", session_id)
        headers = {"Authorization": f"Bearer {other_token}"}
        resp = client.get(
            f"/api/characters/{session_id}/{player_name}/export",
            headers=headers,
        )
        assert resp.status_code == 403
