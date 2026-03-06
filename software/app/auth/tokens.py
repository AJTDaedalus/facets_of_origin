"""JWT token creation and verification for MM and player auth.

Two token types are issued:
- MM tokens: role="mm", no player or session binding, expire in mm_token_expire_hours.
- Invite tokens: role="player", type="invite", single-use, expire in invite_token_expire_hours.
- Session tokens: role="player", type="session", issued after consuming an invite token.

All tokens are HS256 JWTs signed with settings.secret_key.
"""
import re
from datetime import datetime, timedelta, timezone
from typing import Literal

import bcrypt
from jose import JWTError, jwt

from app.config import settings

PLAYER_NAME_RE = re.compile(r"^[A-Za-z0-9 _\-]{1,32}$")
"""Regex enforced on all player names before they are embedded in tokens."""


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    """Hash a plaintext password using bcrypt. Returns a salted hash string."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash. Constant-time comparison."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ---------------------------------------------------------------------------
# Token creation
# ---------------------------------------------------------------------------

def _make_token(payload: dict, expire_hours: int) -> str:
    """Encode a JWT with iat and exp claims added.

    Args:
        payload: Claims to include. Not mutated — a new dict is created.
        expire_hours: Token lifetime from now, in hours.

    Returns:
        A signed JWT string.
    """
    now = datetime.now(tz=timezone.utc)
    to_encode = {
        **payload,
        "iat": now,
        "exp": now + timedelta(hours=expire_hours),
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_mm_token() -> str:
    """Create a Mirror Master authentication token.

    Returns a JWT with role="mm" that grants full MM access.
    """
    return _make_token({"role": "mm"}, settings.mm_token_expire_hours)


def create_invite_token(player_name: str, session_id: str) -> str:
    """Create a single-use invite token for a player.

    Args:
        player_name: Display name for the player. Must match PLAYER_NAME_RE.
        session_id: UUID of the session being joined.

    Returns:
        A signed JWT with role="player", type="invite".

    Raises:
        ValueError: If player_name fails the regex check.
    """
    if not player_name.strip() or not PLAYER_NAME_RE.match(player_name):
        raise ValueError("Player name must be 1–32 alphanumeric characters (spaces, hyphens, underscores allowed).")
    return _make_token(
        {"role": "player", "player_name": player_name, "session_id": session_id, "type": "invite"},
        settings.invite_token_expire_hours,
    )


def create_session_token(player_name: str, session_id: str) -> str:
    """Issue a session token after consuming a valid invite token.

    Args:
        player_name: Player's display name (already validated at invite creation).
        session_id: UUID of the session.

    Returns:
        A signed JWT with role="player", type="session".
    """
    return _make_token(
        {"role": "player", "player_name": player_name, "session_id": session_id, "type": "session"},
        settings.mm_token_expire_hours,
    )


# ---------------------------------------------------------------------------
# Token verification
# ---------------------------------------------------------------------------

class TokenData:
    """Decoded and validated JWT payload.

    Attributes:
        role: Either "mm" or "player".
        player_name: Player's display name; None for MM tokens.
        session_id: Session UUID; None for MM tokens.
        token_type: "invite" or "session" for player tokens; None for MM tokens.
    """

    def __init__(
        self,
        role: Literal["mm", "player"],
        player_name: str | None,
        session_id: str | None,
        token_type: str | None,
    ):
        self.role = role
        self.player_name = player_name
        self.session_id = session_id
        self.token_type = token_type

    @property
    def is_mm(self) -> bool:
        """True if this token grants Mirror Master access."""
        return self.role == "mm"


def decode_token(token: str) -> TokenData:
    """Decode and validate a JWT. Raises JWTError on any failure.

    Validates: signature, expiry, and role claim.

    Args:
        token: A JWT string.

    Returns:
        TokenData with extracted claims.

    Raises:
        JWTError: If the token is invalid, expired, or has an unknown role.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as e:
        raise JWTError(f"Invalid token: {e}") from e

    role = payload.get("role")
    if role not in ("mm", "player"):
        raise JWTError("Token has invalid role claim.")

    return TokenData(
        role=role,
        player_name=payload.get("player_name"),
        session_id=payload.get("session_id"),
        token_type=payload.get("type"),
    )
