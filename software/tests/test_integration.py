"""B3.6 — Full session lifecycle integration test.

Covers: session creation → MM auth → invite → player join → character upload
        → roll → condition applied → character export.
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
    def test_full_session_lifecycle(self, client, mm_headers, valid_attributes):
        """B3.6: Create session → invite → join → upload character → roll → condition → export."""

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

        # 4. Upload a character via the character API
        # Build a minimal .fof YAML directly from a Character object
        from app.facets.registry import build_ruleset
        ruleset = build_ruleset([])
        from app.game.character import create_default_character
        char, errors = create_default_character(
            name="Mordai",
            player_name="Mordai",
            primary_facet="body",
            attributes=valid_attributes,
            ruleset=ruleset,
        )
        assert not errors
        fof_dict = char.to_fof(
            module_refs=[{"id": f.id, "version": f.version} for f in ruleset._files],
            session_id=session_id,
        )
        fof_yaml = yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)

        player_headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post(
            "/api/characters/upload",
            json={"session_id": session_id, "fof_yaml": fof_yaml},
            headers=player_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["character"]["name"] == "Mordai"

        # 5. Player rolls via WebSocket
        with client.websocket_connect("/ws") as ws:
            _auth_player(ws, player_token)
            ws.send_json({
                "type": "roll",
                "attribute_id": "strength",
                "difficulty": "Standard",
                "sparks_spent": 0,
            })
            msg = ws.receive_json()
        assert msg["type"] == "roll_result"
        assert msg["roll"]["outcome"] in ("full_success", "partial_success", "failure")

        # 6. MM applies a condition
        mm_token = create_mm_token()
        with client.websocket_connect("/ws") as ws:
            _auth_mm(ws, mm_token, session_id)
            ws.send_json({
                "type": "apply_condition",
                "player_name": "Mordai",
                "condition": "winded",
            })
            msg = ws.receive_json()
        assert msg["type"] == "condition_applied"
        assert "winded" in msg["all_conditions"]

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
