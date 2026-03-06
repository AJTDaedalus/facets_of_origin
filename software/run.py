"""Entry point for the Facets of Origin tabletop server."""
import os
import sys
import uvicorn

from app.config import settings


def main() -> None:
    # Warn if not running with HTTPS in non-local mode
    if settings.external_url and not settings.external_url.startswith("https://"):
        print(
            "WARNING: external_url is set but does not use HTTPS. "
            "All traffic will be unencrypted. See research/self_hosting_best_practices.md.",
            file=sys.stderr,
        )

    print(f"Starting Facets of Origin server on {settings.host}:{settings.port}")
    if settings.external_url:
        print(f"External URL: {settings.external_url}")
    else:
        print(
            "Running in local-only mode. "
            "Set EXTERNAL_URL in .env to expose externally (requires HTTPS)."
        )

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
