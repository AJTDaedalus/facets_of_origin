# Facets of Origin — Digital Tabletop

Self-hosted tabletop software for the Facets of Origin TTRPG.

The Mirror Master runs the server on their PC. Players connect via browser — no install required.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Create .env for persistent settings
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env

# 3. Start the server
python run.py

# 4. Open http://localhost:8000 in your browser
# 5. Complete first-run setup to set the MM password
# 6. Create a session, generate invite links for players
```

---

## Exposing to External Players

For local network play (in-person or VPN): set `HOST=0.0.0.0` in `.env`.

For remote players (recommended): use **Cloudflare Tunnel** for free, no-port-forwarding access with automatic HTTPS:
```bash
# Install cloudflared, then:
cloudflared tunnel --url http://localhost:8000
# Copy the https://....trycloudflare.com URL and set it:
echo "EXTERNAL_URL=https://your-tunnel.trycloudflare.com" >> .env
```

See `research/self_hosting_best_practices.md` for full deployment options.

---

## Ruleset (Facet Files)

Game rules live in `facets/` as YAML files. The base ruleset is always loaded. Optional modules can be enabled per session.

```
facets/
└── base/
    └── facet.yaml    # Core ruleset (always loaded)
```

See `research/facet_system_design.md` for the full Facet file format and extension guide.

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

---

## Architecture

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Real-time | WebSockets (FastAPI native) |
| Database | SQLite (aiosqlite) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | Vanilla JS — no build step |
| Ruleset | YAML files, Pydantic v2 validated |

See `research/self_hosting_best_practices.md` for security architecture details.
