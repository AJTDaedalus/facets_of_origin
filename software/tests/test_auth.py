"""Tests for JWT auth — token creation, verification, expiry, and edge cases."""
import time
from datetime import datetime, timedelta, timezone

import pytest
from jose import JWTError, jwt

from app.auth.tokens import (
    create_invite_token,
    create_mm_token,
    create_session_token,
    decode_token,
    hash_password,
    verify_password,
    PLAYER_NAME_RE,
)
from app.config import settings


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        h = hash_password("mypassword")
        assert h != "mypassword"

    def test_verify_correct_password(self):
        h = hash_password("correct")
        assert verify_password("correct", h) is True

    def test_reject_wrong_password(self):
        h = hash_password("correct")
        assert verify_password("wrong", h) is False

    def test_same_password_different_hashes(self):
        h1 = hash_password("password")
        h2 = hash_password("password")
        assert h1 != h2  # bcrypt salts are different each time


# ---------------------------------------------------------------------------
# MM token
# ---------------------------------------------------------------------------

class TestMMToken:
    def test_mm_token_decodes_successfully(self):
        token = create_mm_token()
        data = decode_token(token)
        assert data.is_mm

    def test_mm_token_has_correct_role(self):
        token = create_mm_token()
        data = decode_token(token)
        assert data.role == "mm"

    def test_mm_token_has_no_player_name(self):
        token = create_mm_token()
        data = decode_token(token)
        assert data.player_name is None

    def test_mm_token_has_no_session_id(self):
        token = create_mm_token()
        data = decode_token(token)
        assert data.session_id is None


# ---------------------------------------------------------------------------
# Invite tokens
# ---------------------------------------------------------------------------

class TestInviteTokens:
    def test_invite_token_created(self):
        token = create_invite_token("Zahna", "session-123")
        assert token

    def test_invite_token_decodes(self):
        token = create_invite_token("Zahna", "session-123")
        data = decode_token(token)
        assert data.player_name == "Zahna"
        assert data.session_id == "session-123"
        assert data.token_type == "invite"
        assert data.role == "player"
        assert not data.is_mm

    def test_invite_token_with_spaces_in_name(self):
        token = create_invite_token("The Bard", "session-abc")
        data = decode_token(token)
        assert data.player_name == "The Bard"

    def test_invite_token_rejects_empty_name(self):
        with pytest.raises(ValueError, match="Player name"):
            create_invite_token("", "session-123")

    def test_invite_token_rejects_too_long_name(self):
        with pytest.raises(ValueError, match="Player name"):
            create_invite_token("A" * 33, "session-123")

    def test_invite_token_rejects_special_chars(self):
        with pytest.raises(ValueError, match="Player name"):
            create_invite_token("hack<script>", "session-123")

    def test_invite_token_rejects_semicolon(self):
        with pytest.raises(ValueError):
            create_invite_token("name; DROP TABLE", "session-123")


# ---------------------------------------------------------------------------
# Session tokens
# ---------------------------------------------------------------------------

class TestSessionTokens:
    def test_session_token_type_is_session(self):
        token = create_session_token("Mordai", "sess-456")
        data = decode_token(token)
        assert data.token_type == "session"

    def test_session_token_preserves_player_and_session(self):
        token = create_session_token("Mordai", "sess-456")
        data = decode_token(token)
        assert data.player_name == "Mordai"
        assert data.session_id == "sess-456"


# ---------------------------------------------------------------------------
# Token expiry
# ---------------------------------------------------------------------------

class TestTokenExpiry:
    def test_expired_token_raises_jwterror(self):
        payload = {
            "role": "mm",
            "iat": datetime.now(tz=timezone.utc) - timedelta(hours=10),
            "exp": datetime.now(tz=timezone.utc) - timedelta(hours=1),  # expired
        }
        expired_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        with pytest.raises(JWTError):
            decode_token(expired_token)

    def test_token_with_wrong_secret_raises(self):
        payload = {
            "role": "mm",
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=8),
        }
        bad_token = jwt.encode(payload, "wrong-secret", algorithm=settings.algorithm)
        with pytest.raises(JWTError):
            decode_token(bad_token)

    def test_tampered_payload_raises(self):
        token = create_mm_token()
        # Tamper by splitting and replacing the payload
        header, payload, sig = token.split(".")
        import base64, json
        padded = payload + "=" * (4 - len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(padded))
        decoded["role"] = "superadmin"
        # Re-encode with wrong secret — should fail
        tampered_token = jwt.encode(decoded, "wrong-key", algorithm=settings.algorithm)
        with pytest.raises(JWTError):
            decode_token(tampered_token)


# ---------------------------------------------------------------------------
# Invalid tokens
# ---------------------------------------------------------------------------

class TestInvalidTokens:
    def test_garbage_string_raises(self):
        with pytest.raises(JWTError):
            decode_token("not.a.token")

    def test_empty_string_raises(self):
        with pytest.raises(JWTError):
            decode_token("")

    def test_valid_jwt_unknown_role_raises(self):
        payload = {
            "role": "moderator",
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        with pytest.raises(JWTError, match="invalid role"):
            decode_token(token)


# ---------------------------------------------------------------------------
# Player name boundary — 32-char max
# ---------------------------------------------------------------------------

class TestPlayerNameBoundary:
    def test_exactly_32_chars_accepted(self):
        name = "A" * 32
        token = create_invite_token(name, "sess-1")
        data = decode_token(token)
        assert data.player_name == name

    def test_exactly_33_chars_rejected(self):
        with pytest.raises(ValueError, match="Player name"):
            create_invite_token("A" * 33, "sess-1")

    def test_whitespace_only_name_rejected(self):
        with pytest.raises(ValueError, match="Player name"):
            create_invite_token("   ", "sess-1")

    def test_name_with_numbers_accepted(self):
        token = create_invite_token("Player123", "sess")
        data = decode_token(token)
        assert data.player_name == "Player123"

    def test_name_with_underscore_accepted(self):
        token = create_invite_token("The_Bard", "sess")
        data = decode_token(token)
        assert data.player_name == "The_Bard"


# ---------------------------------------------------------------------------
# Token payload structure
# ---------------------------------------------------------------------------

class TestTokenPayloadStructure:
    def test_mm_token_has_iat_claim(self):
        token = create_mm_token()
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "iat" in payload

    def test_mm_token_has_exp_claim(self):
        token = create_mm_token()
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "exp" in payload

    def test_player_token_has_iat_claim(self):
        token = create_session_token("Alice", "sess-1")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "iat" in payload

    def test_invite_token_has_type_claim(self):
        token = create_invite_token("Bob", "sess-2")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload.get("type") == "invite"

    def test_session_token_has_session_type(self):
        token = create_session_token("Carol", "sess-3")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload.get("type") == "session"

    def test_mm_token_does_not_have_player_name_in_payload(self):
        token = create_mm_token()
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "player_name" not in payload


# ---------------------------------------------------------------------------
# Algorithm field
# ---------------------------------------------------------------------------

class TestAlgorithmField:
    def test_settings_algorithm_is_hs256(self):
        assert settings.algorithm == "HS256"

    def test_token_uses_configured_algorithm(self):
        token = create_mm_token()
        # jwt.get_unverified_header extracts header without verifying sig
        from jose import jwt as jose_jwt
        header = jose_jwt.get_unverified_header(token)
        assert header["alg"] == settings.algorithm
