"""Application configuration via environment variables / .env file."""
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Server
    host: str = "127.0.0.1"        # localhost-only by default — must opt in to external
    port: int = 8000
    debug: bool = False
    external_url: str = ""          # Set to your Cloudflare Tunnel or domain URL

    # Security — generated on first run if not set
    secret_key: str = secrets.token_hex(32)
    algorithm: str = "HS256"
    mm_token_expire_hours: int = 8
    invite_token_expire_hours: int = 24

    # Paths
    facets_dir: Path = Path("facets")
    data_dir: Path = Path("data")
    db_path: Path = Path("data/facets.db")

    # Rate limiting
    roll_rate_limit: str = "10/minute"
    auth_rate_limit: str = "5/minute"


settings = Settings()

# Ensure data directory exists
settings.data_dir.mkdir(parents=True, exist_ok=True)
