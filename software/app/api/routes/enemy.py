"""Enemy CRUD routes — MM only."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.routes.session import require_mm
from app.game.enemy import Enemy
from app.game.session import session_store

router = APIRouter(prefix="/api/enemies", tags=["enemies"])


class CreateEnemyRequest(BaseModel):
    session_id: str
    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=128)
    tier: str = "mook"
    endurance: int = Field(default=0, ge=0)
    attack_modifier: int = 0
    defense_modifier: int = 0
    armor: str = "none"
    techniques: list[str] = Field(default_factory=list)
    special: str | None = None
    description: str = ""
    tactics: str = ""
    personality: str = ""
    loot: list[str] = Field(default_factory=list)
    notes: str = ""


@router.post("/", dependencies=[Depends(require_mm)])
async def create_enemy(body: CreateEnemyRequest):
    """Save an enemy definition to a session's library."""
    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    enemy = Enemy(
        id=body.id,
        name=body.name,
        tier=body.tier,
        endurance=body.endurance,
        attack_modifier=body.attack_modifier,
        defense_modifier=body.defense_modifier,
        armor=body.armor,
        techniques=body.techniques,
        special=body.special,
        description=body.description,
        tactics=body.tactics,
        personality=body.personality,
        loot=body.loot,
        notes=body.notes,
    )
    session.enemy_library[enemy.id] = enemy
    return {"enemy": enemy.to_client_dict(), "tr": enemy.calculate_tr()}


@router.get("/{session_id}", dependencies=[Depends(require_mm)])
async def list_enemies(session_id: str):
    """List all enemies in a session's library."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    return {
        "enemies": {
            eid: {**e.to_client_dict(), "tr": e.calculate_tr()}
            for eid, e in session.enemy_library.items()
        }
    }


@router.delete("/{session_id}/{enemy_id}", dependencies=[Depends(require_mm)])
async def delete_enemy(session_id: str, enemy_id: str):
    """Remove an enemy from the session library."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if enemy_id not in session.enemy_library:
        raise HTTPException(status_code=404, detail="Enemy not found.")
    del session.enemy_library[enemy_id]
    return {"deleted": enemy_id}
