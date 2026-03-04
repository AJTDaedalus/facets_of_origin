"""JWT token creation and verification for MM and player auth."""
import re
from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

PLAYER_NAME_RE = re.compile(r"^[A-Za-z0-9 _\-]{1,32}$")


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# Token creation
# ---------------------------------------------------------------------------

def _make_token(payload: dict, expire_hours: int) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {
        **payload,
        "iat": now,
        "exp": now + timedelta(hours=expire_hours),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_mm_token() -> str:
    return _make_token({"role": "mm"}, settings.mm_token_expire_hours)


def create_invite_token(player_name: str, session_id: str) -> str:
    """Creates a single-use invite token for a player."""
    if not PLAYER_NAME_RE.match(player_name):
        raise ValueError("Player name must be 1–32 alphanumeric characters (spaces, hyphens, underscores allowed).")
    return _make_token(
        {"role": "player", "player_name": player_name, "session_id": session_id, "type": "invite"},
        settings.invite_token_expire_hours,
    )


def create_session_token(player_name: str, session_id: str) -> str:
    """Issues a session token after consuming a valid invite token."""
    return _make_token(
        {"role": "player", "player_name": player_name, "session_id": session_id, "type": "session"},
        settings.mm_token_expire_hours,
    )


# ---------------------------------------------------------------------------
# Token verification
# ---------------------------------------------------------------------------

class TokenData:
    def __init__(self, role: Literal["mm", "player"], player_name: str | None, session_id: str | None, token_type: str | None):
        self.role = role
        self.player_name = player_name
        self.session_id = session_id
        self.token_type = token_type

    @property
    def is_mm(self) -> bool:
        return self.role == "mm"


def decode_token(token: str) -> TokenData:
    """Decode and validate a JWT. Raises JWTError on failure."""
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
