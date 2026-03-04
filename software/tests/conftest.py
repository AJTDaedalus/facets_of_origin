"""Shared fixtures for the Facets of Origin test suite."""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the software/ directory is on the path so imports resolve correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

# Point config at the real facets directory
os.environ.setdefault("FACETS_DIR", str(Path(__file__).parent.parent / "facets"))
os.environ.setdefault("DATA_DIR", str(Path(__file__).parent / "_test_data"))
os.environ.setdefault("DB_PATH", str(Path(__file__).parent / "_test_data" / "test.db"))
os.environ.setdefault("SECRET_KEY", "test-secret-key-do-not-use-in-production")

from app.main import app
from app.facets.registry import build_ruleset, MergedRuleset
from app.game.character import Character, SkillState, create_default_character
from app.game.engine import RollRequest, resolve_roll, roll_result_to_dict
from app.auth.tokens import (
    create_mm_token,
    create_invite_token,
    create_session_token,
    decode_token,
    hash_password,
)
from app.api.routes.session import set_mm_password
from app.game.session import session_store


@pytest.fixture(scope="session")
def ruleset() -> MergedRuleset:
    """The fully loaded base ruleset — expensive to build, shared across tests."""
    return build_ruleset([])


@pytest.fixture
def client():
    """FastAPI test client — fresh per test."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def reset_limiter():
    """Reset the in-memory rate limiter storage before and after the test."""
    app.state.limiter._storage.reset()
    yield
    app.state.limiter._storage.reset()


@pytest.fixture
def mm_token() -> str:
    return create_mm_token()


@pytest.fixture
def mm_headers(mm_token) -> dict:
    return {"Authorization": f"Bearer {mm_token}"}


@pytest.fixture
def mm_password():
    pw = "testpassword123"
    set_mm_password(pw)
    return pw


@pytest.fixture
def valid_attributes() -> dict:
    """An 18-point attribute distribution matching the base ruleset rules."""
    return {
        "strength": 3,
        "dexterity": 3,
        "constitution": 2,
        "intelligence": 2,
        "wisdom": 2,
        "knowledge": 2,
        "spirit": 1,
        "luck": 2,
        "charisma": 1,
    }


@pytest.fixture
def body_character(ruleset, valid_attributes) -> Character:
    """A valid Facet of the Body character."""
    char, errors = create_default_character(
        name="Mordai",
        player_name="Player1",
        primary_facet="body",
        attributes=valid_attributes,
        ruleset=ruleset,
    )
    assert not errors, f"Character creation failed: {errors}"
    return char


@pytest.fixture
def active_session(mm_headers, client) -> dict:
    """A live session, returns session dict with id and name."""
    resp = client.post("/api/sessions/", json={"name": "Test Session"}, headers=mm_headers)
    assert resp.status_code == 200
    return resp.json()


@pytest.fixture
def session_with_character(active_session, client, mm_headers, valid_attributes) -> tuple[dict, dict]:
    """A session with a character already created. Returns (session, character)."""
    session_id = active_session["session_id"]
    resp = client.post(
        "/api/characters/",
        json={
            "session_id": session_id,
            "character_name": "Zahna",
            "primary_facet": "mind",
            "attributes": valid_attributes,
        },
        headers=mm_headers,
    )
    assert resp.status_code == 200
    return active_session, resp.json()["character"]
