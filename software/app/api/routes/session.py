"""Session management API routes — MM only."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError
from pydantic import BaseModel, Field

from app.auth.tokens import (
    create_invite_token,
    create_mm_token,
    create_session_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.config import settings
from app.game.session import session_store

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

# ---------------------------------------------------------------------------
# Simple in-memory MM credential store (first-run setup handled separately)
# ---------------------------------------------------------------------------
_mm_password_hash: str | None = None


def _get_mm_hash() -> str | None:
    return _mm_password_hash


def set_mm_password(plain: str) -> None:
    global _mm_password_hash
    _mm_password_hash = hash_password(plain)


# ---------------------------------------------------------------------------
# Auth dependency
# ---------------------------------------------------------------------------

def require_mm(request: Request) -> None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token.")
    token = auth.removeprefix("Bearer ").strip()
    try:
        data = decode_token(token)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    if not data.is_mm:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="MM access required.")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

class MMLoginRequest(BaseModel):
    password: str = Field(min_length=1)


@router.post("/auth/mm-login")
async def mm_login(body: MMLoginRequest):
    """MM logs in with their password and receives a JWT."""
    pw_hash = _get_mm_hash()
    if pw_hash is None or not verify_password(body.password, pw_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")
    token = create_mm_token()
    return {"access_token": token, "token_type": "bearer"}


class SetupRequest(BaseModel):
    password: str = Field(min_length=8, description="MM password, minimum 8 characters.")


@router.post("/auth/setup")
async def setup_mm_password(body: SetupRequest):
    """First-run endpoint: set the MM password. Can only be called once."""
    if _get_mm_hash() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password already set.")
    set_mm_password(body.password)
    return {"message": "MM password set. You can now log in."}


class CreateSessionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128, description="Session/campaign name.")
    active_facet_ids: list[str] = Field(default_factory=list)


@router.post("/", dependencies=[Depends(require_mm)])
async def create_session(body: CreateSessionRequest):
    """Create a new game session."""
    try:
        session = session_store.create_session(body.name, body.active_facet_ids or [])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"session_id": session.id, "name": session.name}


@router.get("/", dependencies=[Depends(require_mm)])
async def list_sessions():
    return {"sessions": session_store.list_sessions()}


class InviteRequest(BaseModel):
    player_name: str = Field(min_length=1, max_length=32)
    session_id: str


@router.post("/invite", dependencies=[Depends(require_mm)])
async def create_invite(body: InviteRequest, request: Request):
    """Generate an invite link for a player."""
    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    try:
        token = create_invite_token(body.player_name, body.session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    base_url = settings.external_url or str(request.base_url).rstrip("/")
    invite_url = f"{base_url}/join?token={token}"
    return {"invite_url": invite_url, "player_name": body.player_name, "expires_in_hours": settings.invite_token_expire_hours}


class RedeemInviteRequest(BaseModel):
    invite_token: str


@router.post("/join")
async def redeem_invite(body: RedeemInviteRequest):
    """Player redeems an invite token and receives a session token."""
    try:
        data = decode_token(body.invite_token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid invite token: {e}")

    if data.token_type != "invite" or not data.player_name or not data.session_id:
        raise HTTPException(status_code=400, detail="Not a valid invite token.")

    session = session_store.get(data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session_store.is_invite_used(data.session_id, body.invite_token):
        raise HTTPException(status_code=400, detail="Invite link has already been used.")

    session_store.mark_invite_used(data.session_id, body.invite_token)
    session_token = create_session_token(data.player_name, data.session_id)

    return {
        "access_token": session_token,
        "token_type": "bearer",
        "player_name": data.player_name,
        "session_id": data.session_id,
        "session_name": session.name,
    }
