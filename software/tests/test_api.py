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
    def test_create_character_with_mm_token(self, client, mm_headers, active_session, create_payload):
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **create_payload},
                           headers=mm_headers)
        assert resp.status_code == 200
        char = resp.json()["character"]
        assert char["name"] == "Zahna"
        assert char["stats"] == {"body": 0, "mind": 2, "soul": 1}
        assert char["derived"]["hp_max"] == 6
        assert char["magic"]["domains"] == ["inscription"]

    def test_create_character_bad_second_stat_returns_422(self, client, mm_headers, active_session,
                                                           create_payload):
        payload = {**create_payload, "second_stat": "mind"}   # the Facet's own stat
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **payload},
                           headers=mm_headers)
        assert resp.status_code == 422
        assert resp.json()["detail"]["errors"]

    def test_create_custom_class_character(self, client, mm_headers, active_session):
        resp = client.post("/api/characters/", json={
            "session_id": active_session["session_id"], "character_name": "Zulnut",
            "facet": "body", "second_stat": "soul",
            "custom_class": {"name": "Wandering Disciple", "concept": "I move and I am still.",
                             "knack": "Motion and stillness",
                             "talents": ["unarmored_discipline", "athlete"],
                             "kit": ["rope", "rations"], "signature": "ghost"},
            "custom_background": {"name": "Pilgrim", "knack": "Roads and shrines",
                                  "specialty": "Knows every shrine on the pilgrim road."},
            "coin": 10,
        }, headers=mm_headers)
        assert resp.status_code == 200, resp.text
        char = resp.json()["character"]
        assert char["class"]["custom"] is True
        assert char["class"]["signature"] == "ghost"
        assert char["knacks"] == ["Motion and stillness", "Roads and shrines"]
        assert char["derived"]["armor"] == 1          # Unarmored Discipline

    def test_list_characters_requires_auth(self, client, active_session):
        resp = client.get(f"/api/characters/{active_session['session_id']}")
        assert resp.status_code == 401

    def test_list_characters_returns_characters(self, client, mm_headers, session_with_character):
        session, _ = session_with_character
        resp = client.get(f"/api/characters/{session['session_id']}", headers=mm_headers)
        assert resp.status_code == 200
        assert "Zahna" in resp.json()["characters"]

    def test_player_creates_own_character(self, client, active_session, create_payload):
        session_id = active_session["session_id"]
        headers = {"Authorization": f"Bearer {create_session_token('Alice', session_id)}"}
        resp = client.post("/api/characters/",
                           json={"session_id": session_id, **create_payload}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["character"]["player_name"] == "Alice"

    def test_player_cannot_create_char_in_other_session(self, client, active_session, create_payload):
        headers = {"Authorization": f"Bearer {create_session_token('Alice', 'other-session')}"}
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **create_payload},
                           headers=headers)
        assert resp.status_code == 403

    def test_invalid_background_id_returns_422(self, client, mm_headers, active_session, create_payload):
        payload = {**create_payload, "background_id": "nonexistent_bg_xyz"}
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **payload},
                           headers=mm_headers)
        assert resp.status_code == 422

    def test_any_character_may_take_any_background(self, client, mm_headers, active_session,
                                                   create_payload):
        """PHB ruling: backgrounds are not tied to a Facet."""
        payload = {**create_payload, "background_id": "dockworker"}   # a 'body' example
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **payload},
                           headers=mm_headers)
        assert resp.status_code == 200

    def test_caster_without_domain_returns_422(self, client, mm_headers, active_session,
                                               create_payload):
        payload = {k: v for k, v in create_payload.items() if k != "magic"}
        resp = client.post("/api/characters/",
                           json={"session_id": active_session["session_id"], **payload},
                           headers=mm_headers)
        assert resp.status_code == 422

    def test_update_inventory_checks_slots(self, client, mm_headers, session_with_character):
        session, _ = session_with_character
        sid = session["session_id"]
        ok = client.put(f"/api/characters/{sid}/Zahna/inventory",
                        json={"inventory": [{"id": "staff"}, {"id": "rope"}],
                              "equipped": {"weapon": "staff", "armor": "none"}},
                        headers=mm_headers)
        assert ok.status_code == 200, ok.text
        assert ok.json()["slots_free"] == 8
        too_many = client.put(f"/api/characters/{sid}/Zahna/inventory",
                              json={"inventory": [{"id": "rope"}] * 11,
                                    "equipped": {"weapon": None, "armor": "none"}},
                              headers=mm_headers)
        assert too_many.status_code == 422

    def test_update_inventory_unknown_character_404(self, client, mm_headers, active_session):
        resp = client.put(f"/api/characters/{active_session['session_id']}/Nobody/inventory",
                          json={"inventory": []}, headers=mm_headers)
        assert resp.status_code == 404


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
            "stat": "body",
        })
        assert resp.status_code == 401

    def test_roll_returns_result(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "stat": "mind",
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
            "stat": "mind",
        }, headers=headers)
        total = resp.json()["roll"]["total"]
        assert isinstance(total, int)

    def test_roll_unknown_stat_returns_422(self, client, session_with_character):
        session, char = session_with_character
        session_id = session["session_id"]
        player_token = create_session_token("Zahna", session_id)
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/rolls/", json={
            "session_id": session_id,
            "stat": "nonexistent",
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
            "facet": "body",
            "second_stat": "soul",
        }, headers=mm_headers)
        assert resp.status_code == 422

    def test_roll_missing_session_id_returns_422(self, client, mm_headers):
        resp = client.post("/api/rolls/", json={
            "stat": "body",
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
            "stat": "mind",
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
            "stat": "mind",
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

def _make_character_fof_yaml(player_name: str, session_id: str | None = None) -> str:
    """A minimal valid v1.0 character .fof (a preset Thaumaturge)."""
    from app.facets.registry import build_ruleset
    from tests.conftest import make_caster
    ruleset = build_ruleset([])
    ch = make_caster(ruleset, name=player_name, player_name=player_name)
    fof = ch.to_fof(ruleset.module_refs(), session_id, ruleset=ruleset)
    return yaml.dump(fof, allow_unicode=True, sort_keys=False)


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
        assert char["facet"] == "mind"

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

    def test_upload_retired_v03_example_fof_is_refused_clearly(self, client, mm_headers,
                                                                active_session):
        """spec/'s character example is still v0.3; uploading it must say why it fails."""
        session_id = active_session["session_id"]
        fof_yaml = (SPEC_EXAMPLES / "character-example.fof").read_text(encoding="utf-8")
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=mm_headers,
        )
        assert resp.status_code == 422
        assert "v0.3" in resp.json()["detail"]

    def test_upload_cast_character_file(self, client, mm_headers, active_session):
        """The cast's Mordai.fof (v1.0) uploads and keeps its computed HP."""
        session_id = active_session["session_id"]
        path = Path(__file__).parent.parent.parent / "characters" / "Mordai.fof"
        resp = client.post("/api/characters/upload",
                           json={"session_id": session_id, "fof_yaml": path.read_text()},
                           headers=mm_headers)
        assert resp.status_code == 200, resp.text
        assert resp.json()["character"]["derived"]["hp_max"] == 16


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

    def test_export_reimport_roundtrip(self, client, mm_headers, active_session, create_payload):
        """Export → re-upload should produce an identical character."""
        session_id = active_session["session_id"]
        client.post("/api/characters/",
                    json={"session_id": session_id, **create_payload,
                          "character_name": "Roundtrip"},
                    headers=mm_headers)
        export_resp = client.get(f"/api/characters/{session_id}/Roundtrip/export",
                                 headers=mm_headers)
        assert export_resp.status_code == 200
        upload_resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": export_resp.text},
            headers=mm_headers,
        )
        assert upload_resp.status_code == 200, upload_resp.text
        reimported = upload_resp.json()["character"]
        assert reimported["name"] == "Roundtrip"
        assert reimported["facet"] == "mind"
        assert reimported["magic"]["signature_workings"] == create_payload["magic"]["signature_workings"]

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


# ---------------------------------------------------------------------------
# Front-end audit B19/B21 — sessions and characters can be removed
# ---------------------------------------------------------------------------

class TestSessionDeletion:
    """An MM could create sessions but never remove one, so the dashboard grew
    a permanent list of dead campaigns and test runs."""

    def test_mm_can_delete_a_session(self, client, mm_headers):
        session_id = client.post(
            "/api/sessions/", json={"name": "Scratch"}, headers=mm_headers,
        ).json()["session_id"]

        resp = client.delete(f"/api/sessions/{session_id}", headers=mm_headers)
        assert resp.status_code == 200

        listed = client.get("/api/sessions/", headers=mm_headers).json()["sessions"]
        assert all(s["id"] != session_id for s in listed)

    def test_deleting_an_unknown_session_is_404(self, client, mm_headers):
        resp = client.delete("/api/sessions/not-a-session", headers=mm_headers)
        assert resp.status_code == 404

    def test_players_cannot_delete_a_session(self, client, mm_headers):
        from app.auth.tokens import create_session_token

        session_id = client.post(
            "/api/sessions/", json={"name": "Protected"}, headers=mm_headers,
        ).json()["session_id"]
        player_headers = {"Authorization": f"Bearer {create_session_token('Zahna', session_id)}"}

        resp = client.delete(f"/api/sessions/{session_id}", headers=player_headers)
        assert resp.status_code in (401, 403)
        assert client.get("/api/sessions/", headers=mm_headers).status_code == 200


class TestCharacterDeletion:
    """A misbuilt character was permanent — nothing could remove one, and the
    player's invite is single-use, so they could not start over either."""

    def test_mm_can_delete_a_character(
        self, client, mm_headers, session_with_character,
    ):
        session, _ = session_with_character
        session_id = session["session_id"]

        resp = client.delete(f"/api/characters/{session_id}/Zahna", headers=mm_headers)
        assert resp.status_code == 200

        listed = client.get(f"/api/characters/{session_id}", headers=mm_headers).json()
        assert "Zahna" not in listed["characters"]

    def test_player_can_delete_their_own_character(
        self, client, mm_headers, session_with_character,
    ):
        """Rebuilding your own character must not need the MM — the invite that
        let you in was single-use."""
        from app.auth.tokens import create_session_token

        session, _ = session_with_character
        session_id = session["session_id"]
        headers = {"Authorization": f"Bearer {create_session_token('Zahna', session_id)}"}

        resp = client.delete(f"/api/characters/{session_id}/Zahna", headers=headers)
        assert resp.status_code == 200

    def test_player_cannot_delete_someone_elses_character(
        self, client, mm_headers, session_with_character,
    ):
        from app.auth.tokens import create_session_token

        session, _ = session_with_character
        session_id = session["session_id"]
        headers = {"Authorization": f"Bearer {create_session_token('Mordai', session_id)}"}

        resp = client.delete(f"/api/characters/{session_id}/Zahna", headers=headers)
        assert resp.status_code == 403

    def test_deleting_an_unknown_character_is_404(
        self, client, mm_headers, active_session,
    ):
        session_id = active_session["session_id"]
        resp = client.delete(f"/api/characters/{session_id}/Nobody", headers=mm_headers)
        assert resp.status_code == 404

    def test_deletion_is_broadcast(self, client, mm_headers, mm_token, session_with_character):
        """Everyone's roster has to drop the character too."""
        from app.api.websocket import manager  # noqa: F401  (import parity with the route)

        session, _ = session_with_character
        session_id = session["session_id"]
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": mm_token, "session_id": session_id})
            ws.receive_json()  # state
            ws.receive_json()  # player_joined
            client.delete(f"/api/characters/{session_id}/Zahna", headers=mm_headers)
            msg = ws.receive_json()

        assert msg["type"] == "character_removed"
        assert msg["player"] == "Zahna"


class TestCharacterCreationCarriesLineage:
    """PHB II.5 / L14. Every rule about lineage lives in the character model;
    the handler only relays it."""

    def _payload(self, session_id, **kw):
        payload = {"session_id": session_id, "character_name": "Serane", "facet": "soul",
                   "second_stat": "mind", "class_id": "speaker",
                   "background_id": "street_performer", "coin": 0}
        payload.update(kw)
        return payload

    def _session(self, client, mm_headers, facets=None):
        return client.post("/api/sessions/",
                           json={"name": "Lin", **({"active_facet_ids": facets} if facets else {})},
                           headers=mm_headers).json()["session_id"]

    def test_lineage_defaults_to_human_when_unsent(self, client, mm_headers):
        sid = self._session(client, mm_headers)
        resp = client.post("/api/characters/", json=self._payload(sid), headers=mm_headers)
        assert resp.status_code == 200, resp.text
        assert resp.json()["character"]["lineage"] == {"id": "human"}

    def test_an_unknown_lineage_is_rejected(self, client, mm_headers):
        sid = self._session(client, mm_headers)
        resp = client.post("/api/characters/", json=self._payload(sid, lineage="dragonborn"),
                           headers=mm_headers)
        assert resp.status_code == 422
        assert "dragonborn" in str(resp.json())

    def test_gifted_on_an_ungifted_lineage_is_rejected_by_the_model(self, client, mm_headers):
        sid = self._session(client, mm_headers)
        resp = client.post("/api/characters/",
                           json=self._payload(sid, lineage="human", gifted=True),
                           headers=mm_headers)
        assert resp.status_code == 422
        assert "no gift" in str(resp.json()).lower()


class TestASettingFacetCanActuallyBeTurnedOn:
    """The opt-in path, end to end: a Facet is discovered, offered, selected at
    session creation, and its content reaches the table.

    Every link in that chain existed and was tested in isolation — discovery,
    the merge, the schema, the picker's rendering — and nothing tested the
    chain. A setting Facet that loads perfectly in a unit test and cannot be
    switched on from the app is the "control wired to nothing" failure in its
    most expensive form: the whole workstream, unreachable.
    """

    def test_valloh_is_offered_as_an_optional_facet(self, client, mm_headers):
        resp = client.get("/api/facets/available", headers=mm_headers)
        assert resp.status_code == 200, resp.text
        facets = {f["id"]: f for f in resp.json()["facets"] if not f.get("error")}
        assert "base" in facets
        assert "valloh" in facets, "the Val'loh Facet is not offered to the MM"

    def test_a_session_without_it_sees_only_the_core(self, client, mm_headers):
        """The default has to stay the default. A setting Facet sitting in the
        directory must not leak into every table's game."""
        sid = client.post("/api/sessions/", json={"name": "Core only"},
                          headers=mm_headers).json()["session_id"]
        from app.game.session import session_store
        rs = session_store.get(sid).ruleset
        assert [lin.id for lin in rs.lineages] == ["human"]
        assert not any(i.curio for i in rs.items)

    def test_a_session_that_opts_in_gets_the_whole_facet(self, client, mm_headers):
        sid = client.post(
            "/api/sessions/",
            json={"name": "Val'loh", "active_facet_ids": ["valloh"]},
            headers=mm_headers,
        ).json()["session_id"]
        from app.game.session import session_store
        rs = session_store.get(sid).ruleset
        assert len([l for l in rs.lineages if l.id != "human"]) == 10
        curios = [i for i in rs.items if i.curio]
        assert len(curios) == 6
        # D24: Val'loh adds no domains — gifts are chosen from the core catalog.
        from app.facets.registry import build_ruleset
        core = build_ruleset([])
        assert {d.id for d in rs.magic_domains} == {d.id for d in core.magic_domains}
        assert rs.get_lineage("human") is not None

    def test_the_opted_in_session_serves_lineages_to_its_clients(
            self, client, mm_headers):
        """The builder's picker renders from the session payload, so a lineage
        the server knows and never sends is a lineage no player can choose."""
        sid = client.post(
            "/api/sessions/",
            json={"name": "Val'loh", "active_facet_ids": ["valloh"]},
            headers=mm_headers,
        ).json()["session_id"]
        from app.game.session import session_store
        payload = session_store.get(sid).ruleset.to_client_dict()
        ids = {l["id"] for l in payload["lineages"]}
        assert {"orthaen", "phern"} <= ids
        assert payload["items"], "crystal charges never reach the client"

    def test_a_gifted_character_can_be_created_in_an_opted_in_session(
            self, client, mm_headers):
        """The whole point of the Facet, exercised through the real API."""
        sid = client.post(
            "/api/sessions/",
            json={"name": "Val'loh", "active_facet_ids": ["valloh"]},
            headers=mm_headers,
        ).json()["session_id"]
        resp = client.post("/api/characters/", json={
            "session_id": sid, "character_name": "Serane", "facet": "soul",
            "second_stat": "mind", "class_id": "speaker", "background_id": "street_performer",
            "lineage": "orthaen", "gift_domain": "transmutation", "coin": 0,
        }, headers=mm_headers)
        assert resp.status_code == 200, resp.text
        char = resp.json()["character"]
        assert char["lineage"] == {"id": "orthaen", "gifted": True, "gift_domain": "transmutation"}
        assert "Orthaen gift" in char["knacks"]
        assert char["magic"] is None

    def test_a_valloh_gift_is_refused_in_a_core_session(self, client, mm_headers):
        """A table that did not load the Facet cannot reach its content by guessing an id."""
        sid = client.post("/api/sessions/", json={"name": "Core only"},
                          headers=mm_headers).json()["session_id"]
        resp = client.post("/api/characters/", json={
            "session_id": sid, "character_name": "Serane", "facet": "soul",
            "second_stat": "mind", "class_id": "speaker", "background_id": "street_performer",
            "lineage": "orthaen", "gift_domain": "transmutation",
        }, headers=mm_headers)
        assert resp.status_code == 422
        assert "orthaen" in str(resp.json())
