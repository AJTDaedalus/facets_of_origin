"""Enemy card CRUD routes — MM only (MM1, DESIGN §3.4)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.routes.session import require_mm
from app.game.enemy import Enemy
from app.game.session import session_store

router = APIRouter(prefix="/api/enemies", tags=["enemies"])


class EnemyCardFields(BaseModel):
    """The numbers a card is built from; overrides are final values."""

    level: int = Field(ge=1, le=10)
    role: str = "standard"
    armor: int = Field(default=0, ge=0, le=2)
    morale: int = Field(default=7, ge=2, le=12)
    hp: int | None = Field(default=None, ge=1)
    damage: int | None = Field(default=None, ge=0)
    attack: int | None = None
    attacks: int | None = Field(default=None, ge=1, le=4)


class CreateEnemyRequest(EnemyCardFields):
    session_id: str
    id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    weapon: str = ""
    wants: str = ""
    special: str = ""
    when_bloodied: str | None = None
    tells: str = ""
    breaks: str = ""
    twists: list[str] = Field(default_factory=list, max_length=6)
    nastier: str | None = None
    description: str = ""
    notes: str = ""
    reskin_of: str | None = None


def _card_enemy(body: EnemyCardFields, **text) -> Enemy:
    return Enemy(
        id=text.pop("id", "preview"), name=text.pop("name", "preview"), level=body.level,
        role=body.role, armor=body.armor, morale=body.morale, hp_override=body.hp,
        damage_override=body.damage, attack_override=body.attack,
        attacks_override=body.attacks, **text)


def _ruleset_or_default(session_id: str | None):
    if session_id:
        session = session_store.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")
        return session.ruleset
    from app.facets.registry import build_ruleset
    return build_ruleset([])


class PreviewCardRequest(EnemyCardFields):
    session_id: str | None = None


@router.post("/preview-card", dependencies=[Depends(require_mm)])
async def preview_card(body: PreviewCardRequest):
    """Derived numbers for an unsaved card (level + role → HP, damage, attack,
    attacks). The Builder asks the engine rather than re-implementing the
    level table in JavaScript."""
    ruleset = _ruleset_or_default(body.session_id)
    if body.role not in ruleset.monsters.roles:
        raise HTTPException(status_code=422, detail=f"Unknown role {body.role!r}.")
    return {"card": _card_enemy(body).card(ruleset)}


@router.post("/", dependencies=[Depends(require_mm)])
async def create_enemy(body: CreateEnemyRequest):
    """Save an enemy card to a session's library. Incomplete cards are refused."""
    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    text = body.model_dump(exclude={"session_id", "level", "role", "armor", "morale",
                                    "hp", "damage", "attack", "attacks"})
    enemy = _card_enemy(body, **text)
    errors = enemy.validate(session.ruleset)
    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})
    session.enemy_library[enemy.id] = enemy
    return {"enemy": enemy.to_client_dict(session.ruleset)}


@router.get("/{session_id}", dependencies=[Depends(require_mm)])
async def list_enemies(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"enemies": {eid: e.to_client_dict(session.ruleset)
                        for eid, e in session.enemy_library.items()}}


@router.delete("/{session_id}/{enemy_id}", dependencies=[Depends(require_mm)])
async def delete_enemy(session_id: str, enemy_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if enemy_id not in session.enemy_library:
        raise HTTPException(status_code=404, detail="Enemy not found.")
    del session.enemy_library[enemy_id]
    return {"deleted": enemy_id}
