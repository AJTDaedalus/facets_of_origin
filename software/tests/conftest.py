"""Shared fixtures for the Facets of Origin test suite (Lean Facets v1.0)."""
import os
import random
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

from app.main import app  # noqa: E402
from app.facets.registry import build_ruleset, MergedRuleset  # noqa: E402
from app.game.character import Character, create_character  # noqa: E402
from app.game.enemy import Enemy  # noqa: E402
from app.auth.tokens import create_mm_token  # noqa: E402
from app.api.routes.session import set_mm_password  # noqa: E402


@pytest.fixture(scope="session")
def ruleset() -> MergedRuleset:
    """The fully loaded base ruleset — expensive to build, shared across tests."""
    return build_ruleset([])


@pytest.fixture(scope="session")
def valloh_ruleset() -> MergedRuleset:
    """Base plus the Val'loh setting Facet."""
    return build_ruleset(["valloh"])


@pytest.fixture
def rng() -> random.Random:
    return random.Random(12345)


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


def make_character(ruleset, **overrides) -> Character:
    """A valid character; defaults to Mordai the Warrior."""
    kwargs = dict(name="Mordai", player_name="Player1", facet="body", second_stat="soul",
                  class_id="warrior", background_id="city_watch_veteran",
                  talent_choices={"weapon_master": "blades"}, coin=40)
    kwargs.update(overrides)
    ch, errors = create_character(ruleset, **kwargs)
    assert not errors, errors
    return ch


def make_caster(ruleset, **overrides) -> Character:
    """A Mind Thaumaturge with Inscription."""
    kwargs = dict(name="Zahna", player_name="Zahna", facet="mind", second_stat="soul",
                  class_id="thaumaturge", background_id="guild_apprentice",
                  magic={"domain": "inscription",
                         "signature_workings": ["A sealing glyph", "A warning rune"]},
                  coin=30)
    kwargs.update(overrides)
    return make_character(ruleset, **kwargs)


def make_enemy(level=1, role="standard", armor=0, morale=7, **kw) -> Enemy:
    return Enemy(id=kw.pop("id", f"{role}_{level}"), name=kw.pop("name", f"{role} {level}"),
                 level=level, role=role, armor=armor, morale=morale, wants="w", special="s",
                 tells="t", breaks="b", twists=["x"] * 6,
                 when_bloodied=None if role == "mook" else "wb", **kw)


@pytest.fixture
def body_character(ruleset) -> Character:
    return make_character(ruleset)


@pytest.fixture
def caster(ruleset) -> Character:
    return make_caster(ruleset)


CREATE_PAYLOAD = {
    "character_name": "Zahna",
    "facet": "mind",
    "second_stat": "soul",
    "class_id": "thaumaturge",
    "background_id": "guild_apprentice",
    "magic": {"domain": "inscription",
              "signature_workings": ["A sealing glyph", "A warning rune"]},
    "coin": 30,
}


@pytest.fixture
def create_payload() -> dict:
    return dict(CREATE_PAYLOAD)


@pytest.fixture
def active_session(mm_headers, client) -> dict:
    """A live session, returns session dict with id and name."""
    resp = client.post("/api/sessions/", json={"name": "Test Session"}, headers=mm_headers)
    assert resp.status_code == 200
    return resp.json()


@pytest.fixture
def session_with_character(active_session, client, mm_headers, create_payload) -> tuple[dict, dict]:
    """A session with a character already created. Returns (session, character)."""
    session_id = active_session["session_id"]
    resp = client.post("/api/characters/",
                       json={"session_id": session_id, **create_payload}, headers=mm_headers)
    assert resp.status_code == 200, resp.text
    return active_session, resp.json()["character"]
