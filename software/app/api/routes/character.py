"""Character creation and management routes."""
from __future__ import annotations

import yaml
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError
from pydantic import BaseModel, Field

from app.auth.tokens import decode_token
from app.game.character import Character
from app.game.character import create_character as build_character
from app.game.session import session_store

router = APIRouter(prefix="/api/characters", tags=["characters"])


async def _announce_character(session_id: str, character: Character) -> None:
    """Tell everyone already connected that a character now exists.

    Character creation is a REST call, so it used to change session state
    silently: an MM sitting in the session saw an empty combat roster, empty
    player pickers, and an empty party list until they reloaded the page.
    Imported here rather than at module scope to avoid a circular import
    (websocket.py -> session -> routes).
    """
    from app.api.websocket import manager

    view = character.to_client_dict(session_store.get(session_id).ruleset)
    player_view = {k: v for k, v in view.items() if k != "notes_mm"}
    await manager.broadcast_split(
        session_id,
        {"type": "character_created", "player": character.player_name, "character": view},
        {"type": "character_created", "player": character.player_name, "character": player_view},
    )


def _require_player_or_mm(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token.")
    token = auth.removeprefix("Bearer ").strip()
    try:
        return decode_token(token)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


class CustomClassRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    concept: str = Field(min_length=1, max_length=300)
    knack: str = Field(min_length=1, max_length=64)
    talents: list[str]
    kit: list[str] = Field(default_factory=list)
    signature: str | None = None


class CustomBackgroundRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    knack: str = Field(min_length=1, max_length=64)
    specialty: str = Field(min_length=1, max_length=300)
    description: str = Field(default="", max_length=2000)


class MagicRequest(BaseModel):
    domain: str
    signature_workings: list[str]


class CreateCharacterRequest(BaseModel):
    """Lean Facets v1.0 creation (PHB II.1): Facet, second stat, a preset
    class or a custom one, a background (listed or custom), lineage."""

    session_id: str
    character_name: str = Field(min_length=1, max_length=64)
    facet: str
    second_stat: str
    class_id: str | None = None
    custom_class: CustomClassRequest | None = None
    background_id: str | None = None
    custom_background: CustomBackgroundRequest | None = None
    lineage: str = "human"
    gifted: bool | None = None
    gift_domain: str | None = None
    talent_choices: dict[str, str] = Field(default_factory=dict)
    magic: MagicRequest | None = None
    kit: list[str] | None = None
    coin: int | None = Field(default=None, ge=0)


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

    character, errors = build_character(
        session.ruleset,
        name=body.character_name,
        player_name=player_name or body.character_name,
        facet=body.facet,
        second_stat=body.second_stat,
        class_id=body.class_id,
        custom_class=body.custom_class.model_dump() if body.custom_class else None,
        background_id=body.background_id,
        custom_background=body.custom_background.model_dump() if body.custom_background else None,
        lineage=body.lineage,
        gifted=body.gifted,
        gift_domain=body.gift_domain,
        talent_choices=body.talent_choices,
        magic=body.magic.model_dump() if body.magic else None,
        kit=body.kit,
        coin=body.coin,
    )

    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})

    session.add_character(character)
    await _announce_character(body.session_id, character)
    return {"character": character.to_client_dict(session.ruleset)}


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
        character = Character.from_fof(fof_dict, session.ruleset)
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
    await _announce_character(body.session_id, character)
    return {"character": character.to_client_dict(session.ruleset)}


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

    fof_dict = character.to_fof(session.ruleset.module_refs(), session_id, ruleset=session.ruleset)
    yaml_str = yaml.dump(fof_dict, allow_unicode=True, sort_keys=False)

    return Response(
        content=yaml_str,
        media_type="application/yaml",
        headers={"Content-Disposition": f'attachment; filename="{player_name}.fof"'},
    )


@router.delete("/{session_id}/{player_name}")
async def delete_character(session_id: str, player_name: str, request: Request):
    """Remove a character so it can be rebuilt.

    A misbuilt character used to be permanent: nothing could delete one, and a
    player's invite is single-use, so they could not rejoin to start over
    either. Players may delete their own; the MM may delete any.
    """
    token_data = _require_player_or_mm(request)

    if not token_data.is_mm:
        if token_data.session_id != session_id:
            raise HTTPException(status_code=403, detail="Token is for a different session.")
        if token_data.player_name != player_name:
            raise HTTPException(status_code=403, detail="You can only delete your own character.")

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if player_name not in session.characters:
        raise HTTPException(status_code=404, detail="Character not found in session.")

    del session.characters[player_name]

    from app.api.websocket import manager
    await manager.broadcast(session_id, {
        "type": "character_removed",
        "player": player_name,
    })
    return {"deleted": player_name}


@router.get("/{session_id}")
async def list_characters(session_id: str, request: Request):
    _require_player_or_mm(request)
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"characters": {pn: c.to_client_dict(session.ruleset)
                           for pn, c in session.characters.items()}}


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


class InventoryItemRequest(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    name: str = Field(default="", max_length=200)
    slots: int | None = Field(default=None, ge=0, le=4)
    kind: str | None = None
    usage_die: int | None = None


class UpdateInventoryRequest(BaseModel):
    inventory: list[InventoryItemRequest] = Field(max_length=100)
    equipped: dict | None = None


@router.put("/{session_id}/{player_name}/inventory")
async def update_inventory(session_id: str, player_name: str, body: UpdateInventoryRequest, request: Request):
    """Replace a character's inventory (items fill slots; Wounds and Fatigue
    keep theirs). Players update their own; the MM can update any. Refused if
    the items would not fit, or the equipped gear is not carried."""
    from app.game.character import InventoryItem

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

    ruleset = session.ruleset
    items = []
    for req in body.inventory:
        raw = {k: v for k, v in req.model_dump().items() if v not in (None, "")}
        items.append(InventoryItem.from_dict(raw, ruleset))
    old_items, old_equipped = character.inventory, dict(character.equipped)
    character.inventory = items
    if body.equipped is not None:
        character.equipped.update(body.equipped)
    errors = character.validate_against_ruleset(ruleset)
    if character.slots_free(ruleset) < 0:
        errors.append(f"That is {-character.slots_free(ruleset)} slot(s) too many.")
    if character.curios_carried() > character.curio_limit(ruleset):
        errors.append("That is more curios than the limit.")
    if errors:
        character.inventory, character.equipped = old_items, old_equipped
        raise HTTPException(status_code=422, detail={"errors": errors})
    session.save_character_to_disk(player_name)
    return {"inventory": [i.to_dict() for i in character.inventory],
            "equipped": character.equipped,
            "slots_free": character.slots_free(ruleset)}
