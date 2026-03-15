"""Character creation and management routes."""
from __future__ import annotations

import yaml
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError
from pydantic import BaseModel, Field

from app.auth.tokens import decode_token
from app.game.character import Character, create_default_character
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
    background_id: str | None = None
    magic_domain: str | None = None


class UploadCharacterRequest(BaseModel):
    session_id: str
    fof_yaml: str = Field(description="Raw YAML content of a character .fof file.")


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

    if body.background_id and not session.ruleset.get_background(body.background_id):
        raise HTTPException(
            status_code=422,
            detail=f"Unknown background: {body.background_id}",
        )

    character, errors = create_default_character(
        name=body.character_name,
        player_name=player_name or body.character_name,
        primary_facet=body.primary_facet,
        attributes=body.attributes,
        ruleset=session.ruleset,
        background_id=body.background_id,
        magic_domain=body.magic_domain,
    )

    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})

    session.add_character(character)
    return {"character": character.to_client_dict()}


@router.post("/upload")
async def upload_character(body: UploadCharacterRequest, request: Request):
    """Upload a character .fof file to join or update a character in a session.

    Players may only upload a character whose player_name matches their token.
    MM may upload any character.
    """
    token_data = _require_player_or_mm(request)

    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        fof_dict = yaml.safe_load(body.fof_yaml)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"YAML parse error: {e}")

    if not isinstance(fof_dict, dict) or fof_dict.get("type") != "character":
        raise HTTPException(
            status_code=400,
            detail="File must be a character .fof (type: character).",
        )

    try:
        character = Character.from_fof(fof_dict)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Players can only upload their own character
    if not token_data.is_mm:
        if token_data.session_id != body.session_id:
            raise HTTPException(status_code=403, detail="Token is for a different session.")
        if character.player_name != token_data.player_name:
            raise HTTPException(
                status_code=403,
                detail="Character player_name does not match your token.",
            )

    errors = character.validate_against_ruleset(session.ruleset)
    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})

    session.add_character(character)
    return {"character": character.to_client_dict()}


@router.get("/{session_id}/{player_name}/export")
async def export_character(session_id: str, player_name: str, request: Request):
    """Download the current character state as a .fof file.

    Players may only export their own character. MM may export any.
    """
    token_data = _require_player_or_mm(request)

    if not token_data.is_mm and token_data.player_name != player_name:
        raise HTTPException(status_code=403, detail="You can only export your own character.")

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    character = session.characters.get(player_name)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found in session.")

    module_refs = [{"id": f.id, "version": f.version} for f in session.ruleset._files]
    fof_dict = character.to_fof(module_refs, session_id)
    yaml_str = yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)

    return Response(
        content=yaml_str,
        media_type="application/yaml",
        headers={"Content-Disposition": f'attachment; filename="{player_name}.fof"'},
    )


@router.get("/{session_id}")
async def list_characters(session_id: str, request: Request):
    _require_player_or_mm(request)
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"characters": {pn: c.to_client_dict() for pn, c in session.characters.items()}}


class UpdateNotesRequest(BaseModel):
    notes_player: str | None = None
    notes_mm: str | None = None


@router.put("/{session_id}/{player_name}/notes")
async def update_notes(session_id: str, player_name: str, body: UpdateNotesRequest, request: Request):
    """Update player and/or MM notes on a character.

    Players can only update notes_player on their own character.
    MM can update both notes_player and notes_mm on any character.
    """
    token_data = _require_player_or_mm(request)

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    character = session.characters.get(player_name)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    if not token_data.is_mm:
        if token_data.session_id != session_id:
            raise HTTPException(status_code=403, detail="Token is for a different session.")
        if token_data.player_name != player_name:
            raise HTTPException(status_code=403, detail="You can only update your own notes.")
        if body.notes_mm is not None:
            raise HTTPException(status_code=403, detail="Only the MM can set MM notes.")

    if body.notes_player is not None:
        character.notes_player = body.notes_player[:2000]
    if body.notes_mm is not None:
        character.notes_mm = body.notes_mm[:2000]

    session.save_character_to_disk(player_name)
    return {"notes_player": character.notes_player, "notes_mm": character.notes_mm}


class UpdateInventoryRequest(BaseModel):
    inventory: list[str]


@router.put("/{session_id}/{player_name}/inventory")
async def update_inventory(session_id: str, player_name: str, body: UpdateInventoryRequest, request: Request):
    """Update a character's inventory. Players update their own; MM can update any."""
    token_data = _require_player_or_mm(request)

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    character = session.characters.get(player_name)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    if not token_data.is_mm:
        if token_data.session_id != session_id:
            raise HTTPException(status_code=403, detail="Token is for a different session.")
        if token_data.player_name != player_name:
            raise HTTPException(status_code=403, detail="You can only update your own inventory.")

    character.inventory = [item[:200] for item in body.inventory[:100]]
    session.save_character_to_disk(player_name)
    return {"inventory": character.inventory}
