"""Application configuration via environment variables / .env file.

All settings are read from the environment (or a .env file) at startup.
Fields with defaults work out of the box for development; production deployments
should set SECRET_KEY, HOST, and EXTERNAL_URL at minimum.
"""
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pydantic-settings model for all application configuration.

    Values are resolved in priority order:
    1. Environment variables (highest priority)
    2. .env file in the working directory
    3. Field defaults (lowest priority)
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Server
    host: str = "127.0.0.1"
    """Bind address. Defaults to localhost-only; set to 0.0.0.0 to accept external connections."""

    port: int = 8000
    """HTTP port the server listens on."""

    debug: bool = False
    """Enable debug mode. Enables /api/docs and more verbose logging. Never use in production."""

    external_url: str = ""
    """Public-facing base URL (e.g. a Cloudflare Tunnel URL). Used to construct invite links."""

    # Security — generated on first run if not set
    secret_key: str = secrets.token_hex(32)  # nosec B105 — generated dynamically, not hardcoded
    """JWT signing key. Must be set in .env for tokens to survive server restarts.
    Defaults to a new random 256-bit key each process start — not suitable for production."""

    algorithm: str = "HS256"
    """JWT signing algorithm. HS256 is correct for single-server deployments."""

    mm_token_expire_hours: int = 8
    """How many hours a Mirror Master login token remains valid."""

    invite_token_expire_hours: int = 24
    """How many hours a player invite link remains valid."""

    # Paths
    facets_dir: Path = Path("facets")
    """Root directory searched for facet.yaml module files."""

    data_dir: Path = Path("data")
    """Directory for persistent data (session snapshots, future DB files)."""

    db_path: Path = Path("data/facets.db")
    """SQLite database path (planned for v0.2 persistence)."""

    # Rate limiting
    roll_rate_limit: str = "10/minute"
    """Maximum roll requests per minute per client IP (slowapi format)."""

    auth_rate_limit: str = "5/minute"
    """Maximum auth attempts per minute per client IP (slowapi format)."""


settings = Settings()

# Ensure data directory exists
settings.data_dir.mkdir(parents=True, exist_ok=True)
