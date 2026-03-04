"""Character creation and management routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError
from pydantic import BaseModel, Field

from app.auth.tokens import decode_token
from app.game.character import create_default_character
from app.game.session import session_store

router = APIRouter(prefix="/api/characters", tags=["characters"])


def _require_player_or_mm(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token.")
    token = auth.removeprefix("Bearer ").strip()
    try:
        return decode_token(token)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


class CreateCharacterRequest(BaseModel):
    session_id: str
    character_name: str = Field(min_length=1, max_length=64)
    primary_facet: str
    attributes: dict[str, int] = Field(description="Minor attribute ID -> rating (1-3).")


@router.post("/")
async def create_character(body: CreateCharacterRequest, request: Request):
    """Create a character in a session. Players create their own; MM can create any."""
    token_data = _require_player_or_mm(request)

    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Players can only create a character with their own player name
    if not token_data.is_mm:
        if token_data.session_id != body.session_id:
            raise HTTPException(status_code=403, detail="Token is for a different session.")
        player_name = token_data.player_name
    else:
        # MM can specify a player_name or it defaults to character name
        player_name = body.character_name

    character, errors = create_default_character(
        name=body.character_name,
        player_name=player_name or body.character_name,
        primary_facet=body.primary_facet,
        attributes=body.attributes,
        ruleset=session.ruleset,
    )

    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})

    session.add_character(character)
    return {"character": character.to_client_dict()}


@router.get("/{session_id}")
async def list_characters(session_id: str, request: Request):
    _require_player_or_mm(request)
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"characters": {pn: c.to_client_dict() for pn, c in session.characters.items()}}
