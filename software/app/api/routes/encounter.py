"""Encounter CRUD routes and the danger read — MM only (MM1)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.routes.session import require_mm
from app.game.encounter import Encounter, EncounterEnemy
from app.game.session import session_store

router = APIRouter(prefix="/api/encounters", tags=["encounters"])


class EncounterEnemyRequest(BaseModel):
    enemy_id: str
    count: int = Field(default=1, ge=1, le=50)


class CreateEncounterRequest(BaseModel):
    session_id: str
    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=256)
    environment: str = ""
    description: str = ""
    enemies: list[EncounterEnemyRequest] = Field(default_factory=list)
    lateral_solutions: list[str] = Field(default_factory=list)
    rewards_sparks: int = Field(default=0, ge=0)
    rewards_narrative: str = ""
    notes: str = ""


class PreviewRequest(BaseModel):
    """Roster for a live danger read. Party size/level default to the session's."""

    session_id: str
    enemies: list[EncounterEnemyRequest] = Field(default_factory=list)
    party_size: int | None = Field(default=None, ge=1, le=12)
    party_level: int | None = Field(default=None, ge=1, le=10)


def _session(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


def _encounter(body) -> Encounter:
    return Encounter(id=getattr(body, "id", "_preview"), name=getattr(body, "name", "_preview"),
                     enemies=[EncounterEnemy(e.enemy_id, e.count) for e in body.enemies])


@router.post("/", dependencies=[Depends(require_mm)])
async def create_encounter(body: CreateEncounterRequest):
    session = _session(body.session_id)
    encounter = Encounter(
        id=body.id, name=body.name, environment=body.environment,
        description=body.description,
        enemies=[EncounterEnemy(e.enemy_id, e.count) for e in body.enemies],
        lateral_solutions=body.lateral_solutions, rewards_sparks=body.rewards_sparks,
        rewards_narrative=body.rewards_narrative, notes=body.notes)
    session.encounter_library[encounter.id] = encounter
    return {"encounter": encounter.to_client_dict(),
            "danger": encounter.danger(session.enemy_library, session.party_size(),
                                       session.party_level()),
            "missing": encounter.missing(session.enemy_library)}


@router.post("/preview", dependencies=[Depends(require_mm)])
async def preview(body: PreviewRequest):
    """Danger read for an unsaved roster (foes from the session library)."""
    session = _session(body.session_id)
    encounter = _encounter(body)
    missing = encounter.missing(session.enemy_library)
    if missing:
        raise HTTPException(status_code=404,
                            detail=f"Enemy id(s) not in the session library: {', '.join(missing)}.")
    return {"danger": encounter.danger(session.enemy_library,
                                       body.party_size or session.party_size(),
                                       body.party_level or session.party_level())}


@router.get("/{session_id}", dependencies=[Depends(require_mm)])
async def list_encounters(session_id: str):
    session = _session(session_id)
    size, level = session.party_size(), session.party_level()
    return {"encounters": {
        eid: {**enc.to_client_dict(),
              "danger": enc.danger(session.enemy_library, size, level)}
        for eid, enc in session.encounter_library.items()}}


@router.delete("/{session_id}/{encounter_id}", dependencies=[Depends(require_mm)])
async def delete_encounter(session_id: str, encounter_id: str):
    session = _session(session_id)
    if encounter_id not in session.encounter_library:
        raise HTTPException(status_code=404, detail="Encounter not found.")
    del session.encounter_library[encounter_id]
    return {"deleted": encounter_id}
