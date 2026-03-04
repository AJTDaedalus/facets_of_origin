"""HTTP roll endpoint — alternative to WebSocket rolls for simple clients."""
from fastapi import APIRouter, HTTPException, Request, status
from jose import JWTError
from pydantic import BaseModel, Field

from app.auth.tokens import decode_token
from app.config import settings
from app.game.engine import RollRequest, resolve_roll, roll_result_to_dict
from app.game.session import session_store
from app.limiter import limiter

router = APIRouter(prefix="/api/rolls", tags=["rolls"])


class RollHTTPRequest(BaseModel):
    session_id: str
    attribute_id: str
    skill_id: str | None = None
    difficulty: str = "Standard"
    sparks_spent: int = Field(default=0, ge=0, le=10)
    description: str = Field(default="", max_length=200)


@router.post("/")
@limiter.limit(settings.roll_rate_limit)
async def http_roll(body: RollHTTPRequest, request: Request):
    """Resolve a roll via HTTP (useful for testing or non-WebSocket clients).

    This endpoint performs server-side resolution — the client cannot supply modifiers.
    Results are NOT broadcast to other players; use the WebSocket handler for live play.
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token.")
    try:
        token_data = decode_token(auth.removeprefix("Bearer ").strip())
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if token_data.role == "player" and token_data.session_id != body.session_id:
        raise HTTPException(status_code=403, detail="Token is for a different session.")

    session = session_store.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    player_name = token_data.player_name if not token_data.is_mm else None
    character = session.characters.get(player_name) if player_name else None

    if not character:
        raise HTTPException(status_code=404, detail="No character found for this player.")

    if body.attribute_id not in character.attributes:
        raise HTTPException(status_code=422, detail=f"Unknown attribute '{body.attribute_id}'.")

    sparks_to_spend = min(body.sparks_spent, character.sparks)
    for _ in range(sparks_to_spend):
        character.spend_spark()

    roll_req = RollRequest(
        attribute_id=body.attribute_id,
        attribute_rating=character.attributes[body.attribute_id],
        skill_id=body.skill_id,
        skill_rank_id=(
            character.skills[body.skill_id].rank
            if body.skill_id and body.skill_id in character.skills
            else None
        ),
        difficulty_label=body.difficulty,
        sparks_spent=sparks_to_spend,
        description=body.description,
    )

    result = resolve_roll(roll_req, session.ruleset)
    result_dict = roll_result_to_dict(result)
    session.record_roll(player_name or "mm", result_dict)

    return {"roll": result_dict, "sparks_remaining": character.sparks}
