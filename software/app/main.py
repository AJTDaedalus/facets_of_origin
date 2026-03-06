"""FastAPI application — wires together routes, WebSocket, middleware, and static files."""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.routes.character import router as character_router
from app.api.routes.facets_route import router as facets_router
from app.api.routes.rolls import router as rolls_router
from app.api.routes.session import router as session_router
from app.api.websocket import handle_websocket
from app.config import settings
from app.limiter import limiter

logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Facets of Origin",
    description="Self-hosted digital tabletop for the Facets of Origin TTRPG.",
    version="0.1.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url=None,
)

# ---------------------------------------------------------------------------
# Rate limiter — attach to app state so SlowAPIMiddleware can find it.
# Routes opt in with @limiter.limit("N/interval").
# ---------------------------------------------------------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ---------------------------------------------------------------------------
# Security headers middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "   # inline scripts needed for first-draft vanilla JS
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws: wss:;"
    )
    return response


# ---------------------------------------------------------------------------
# CORS — restricted to the server's own origin
# ---------------------------------------------------------------------------
allowed_origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
if settings.external_url:
    allowed_origins.append(settings.external_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------
app.include_router(session_router)
app.include_router(character_router)
app.include_router(rolls_router)
app.include_router(facets_router)

# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)

# ---------------------------------------------------------------------------
# Static file serving — the frontend
# ---------------------------------------------------------------------------
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(static_dir / "index.html")

@app.get("/join")
async def serve_join():
    """Invite link landing page — the token is in the query string on the client side."""
    return FileResponse(static_dir / "index.html")

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
