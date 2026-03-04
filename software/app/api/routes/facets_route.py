"""Facet management routes — list available Facet modules."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status
from jose import JWTError

from app.auth.tokens import decode_token
from app.config import settings
from app.facets.loader import FacetLoadError, discover_facet_files, load_facet_file

router = APIRouter(prefix="/api/facets", tags=["facets"])


def _require_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token.")
    try:
        return decode_token(auth.removeprefix("Bearer ").strip())
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/available")
async def list_available_facets(request: Request):
    """List all Facet files found in the facets directory."""
    _require_auth(request)
    paths = discover_facet_files(settings.facets_dir)
    result = []
    for path in paths:
        try:
            ff = load_facet_file(path)
            result.append({
                "id": ff.id,
                "name": ff.name,
                "version": ff.version,
                "description": ff.description,
                "authors": ff.authors,
                "priority": ff.priority,
                "path": str(path),
            })
        except FacetLoadError as e:
            result.append({"path": str(path), "error": str(e)})
    return {"facets": result}
