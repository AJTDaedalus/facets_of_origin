"""B3.6 — Full session lifecycle integration test.

Covers: session creation → MM auth → invite → player join → character upload
        → roll → character export.
"""
from __future__ import annotations

import yaml
import pytest

from app.auth.tokens import create_invite_token, create_mm_token, create_session_token
from app.game.character import Character


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _auth_mm(ws, mm_token: str, session_id: str) -> None:
    ws.send_json({"token": mm_token, "session_id": session_id})
    ws.receive_json()  # state
    ws.receive_json()  # player_joined


def _auth_player(ws, player_token: str) -> None:
    ws.send_json({"token": player_token})
    ws.receive_json()  # state
    ws.receive_json()  # player_joined


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------

class TestFullSessionLifecycle:
    def test_full_session_lifecycle(self, client, mm_headers):
        """Create session → invite → join → upload character → roll → export."""

        # 1. Create session
        resp = client.post("/api/sessions/", json={"name": "Integration Test Session"}, headers=mm_headers)
        assert resp.status_code == 200
        session_id = resp.json()["session_id"]

        # 2. Generate invite for player "Mordai"
        resp = client.post(
            "/api/sessions/invite",
            json={"player_name": "Mordai", "session_id": session_id},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        invite_url = resp.json()["invite_url"]
        invite_token = invite_url.split("token=")[-1]

        # 3. Player redeems invite
        resp = client.post("/api/sessions/join", json={"invite_token": invite_token})
        assert resp.status_code == 200
        player_token = resp.json()["access_token"]

        # 4. Upload a character .fof built through the v1 model
        from app.facets.registry import build_ruleset
        from tests.conftest import make_character
        ruleset = build_ruleset([])
        char = make_character(ruleset, name="Mordai", player_name="Mordai")
        fof_dict = char.to_fof(ruleset.module_refs(), session_id=session_id, ruleset=ruleset)
        fof_yaml = yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)

        player_headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=player_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["character"]["name"] == "Mordai"

        # 5. Player rolls over HTTP (the WebSocket events are the APP layer's)
        resp = client.post("/api/rolls/", json={
            "session_id": session_id, "stat": "body", "knack": True,
            "difficulty": "Standard", "sparks_spent": 1,
        }, headers=player_headers)
        assert resp.status_code == 200, resp.text
        assert resp.json()["roll"]["outcome"] in ("full_success", "partial_success", "failure")
        assert len(resp.json()["roll"]["dice"]) == 3
        assert resp.json()["sparks_remaining"] == 2

        # 7. Export character
        resp = client.get(
            f"/api/characters/{session_id}/Mordai/export",
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert "application/yaml" in resp.headers["content-type"]
        exported = yaml.safe_load(resp.content)
        assert exported["type"] == "character"
        assert exported["character"]["name"] == "Mordai"
