"""Encounter CRUD routes — MM only."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.routes.session import require_mm
from app.game.encounter import Encounter, EncounterEnemy
from app.game.session import session_store

router = APIRouter(prefix="/api/encounters", tags=["encounters"])


class EncounterEnemyRequest(BaseModel):
    enemy_id: str
    count: int = Field(default=1, ge=1)


class CreateEncounterRequest(BaseModel):
    session_id: str
    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=256)
    difficulty: str = "standard"
    environment: str = ""
    description: str = ""
    enemies: list[EncounterEnemyRequest] = Field(default_factory=list)
    lateral_solutions: list[str] = Field(default_factory=list)
    rewards_sparks: int = Field(default=0, ge=0)
    rewards_narrative: str = ""
    notes: str = ""


@router.post("/", dependencies=[Depends(require_mm)])
async def create_encounter(body: CreateEncounterRequest):
    """Save an encounter definition to a session."""
    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    encounter = Encounter(
        id=body.id,
        name=body.name,
        difficulty=body.difficulty,
        environment=body.environment,
        description=body.description,
        enemies=[
            EncounterEnemy(enemy_id=e.enemy_id, count=e.count)
            for e in body.enemies
        ],
        lateral_solutions=body.lateral_solutions,
        rewards_sparks=body.rewards_sparks,
        rewards_narrative=body.rewards_narrative,
        notes=body.notes,
    )

    # Calculate effective TR if enemies are in the library
    enemy_trs = {
        eid: e.calculate_tr()
        for eid, e in session.enemy_library.items()
    }
    effective_tr = encounter.calculate_effective_tr(enemy_trs)

    session.encounter_library[encounter.id] = encounter
    return {
        "encounter": encounter.to_client_dict(),
        "effective_tr": effective_tr,
    }


@router.get("/{session_id}", dependencies=[Depends(require_mm)])
async def list_encounters(session_id: str):
    """List all encounters in a session."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    enemy_trs = {
        eid: e.calculate_tr()
        for eid, e in session.enemy_library.items()
    }

    return {
        "encounters": {
            eid: {
                **enc.to_client_dict(),
                "effective_tr": enc.calculate_effective_tr(enemy_trs),
            }
            for eid, enc in session.encounter_library.items()
        }
    }


@router.delete("/{session_id}/{encounter_id}", dependencies=[Depends(require_mm)])
async def delete_encounter(session_id: str, encounter_id: str):
    """Remove an encounter from the session."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if encounter_id not in session.encounter_library:
        raise HTTPException(status_code=404, detail="Encounter not found.")
    del session.encounter_library[encounter_id]
    return {"deleted": encounter_id}
