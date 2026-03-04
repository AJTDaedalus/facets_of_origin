# Facets of Origin — Digital Tabletop Server

Facets of Origin is a digital-first, open-source tabletop RPG. This directory contains the self-hosted server that powers a live session: rolling dice, tracking characters, spending Sparks, and keeping everyone at the same table — whether they're in the same room or across the world.

The server is run by the **Mirror Master** (the person running the game). Players receive a single-use invite link, click it, and they're in. The software handles all the bookkeeping so the humans can focus on the story.

---

## Prerequisites

- Python 3.11 or later
- `pip` (comes with Python)
- A terminal

---

## Installation

```bash
git clone https://github.com/AJTDaedalus/facets_of_origin.git
cd facets_of_origin/software
pip install -r requirements.txt
```

---

## First-Run Setup

1. Start the server:
   ```bash
   python run.py
   ```

2. Open your browser to `http://localhost:8000`.

3. Click **First Run Setup** and set a password for the Mirror Master account. You'll use this password every time you log in.

4. Log in with your password.

---

## Creating a Session

1. Log in as Mirror Master.
2. Enter a name for your session or campaign (e.g. *The Shattered Crown*).
3. Click **Create Session**. The session ID appears in the session list.

---

## Generating Player Invites

1. From the MM dashboard, enter the session ID and the player's name.
2. Click **Generate Invite Link**.
3. Copy the URL and send it to the player (Discord, email, message — anything works).

Each link is **single-use**. Once the player clicks it and joins, it can't be reused. Generate a new one if needed.

---

## Playing

### Rolling Dice
- Click an attribute in your character sheet to select it.
- Optionally select a difficulty and fill in a description.
- Click the spark pips to spend Sparks before rolling.
- Click **Roll 2d6**.
- The result is broadcast to everyone at the table.

### Spending Sparks
Each Spark you spend adds a d6 to your roll and drops the lowest — shifting the odds in your favour without changing the core 2d6 mechanic. Click the circular pip icons to add Sparks before rolling.

### Earning Sparks
- The MM can award a Spark from the **Mirror Master Controls** panel.
- Any player can nominate another using the **Nominate for Spark** panel — the MM confirms it.
- Rolling a 6- and leaning into the consequence may earn a Spark at the MM's discretion.

### Table Chat
Use the chat box in the right panel. Messages are visible to everyone in the session.

---

## Deployment Options

### Local LAN (simplest)

Change the host in `.env`:
```
HOST=0.0.0.0
```
Then restart the server. Players on the same network can connect to `http://<your-ip>:8000`.

### Cloudflare Tunnel (recommended for remote play)

Cloudflare Tunnel gives players a public HTTPS URL without opening firewall ports or configuring a domain.

1. Install [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).
2. Run: `cloudflared tunnel --url http://localhost:8000`
3. Copy the `*.trycloudflare.com` URL into `.env`:
   ```
   EXTERNAL_URL=https://your-tunnel.trycloudflare.com
   ```
4. Restart the server.

Invite links will use the tunnel URL automatically.

### Caddy + Domain (permanent hosting)

If you own a domain and want a permanent setup, use [Caddy](https://caddyserver.com/) as a reverse proxy:

```
# Caddyfile
yourdomain.example.com {
    reverse_proxy localhost:8000
}
```

Set `EXTERNAL_URL=https://yourdomain.example.com` in `.env`.

See `research/self_hosting_best_practices.md` for full details on each deployment option.

---

## Configuration Reference

All configuration is via a `.env` file in the `software/` directory. Every variable has a default — only set what you need to change.

| Variable | Default | Description |
|---|---|---|
| `HOST` | `127.0.0.1` | Server bind address. Set to `0.0.0.0` to accept external connections. |
| `PORT` | `8000` | HTTP port to listen on. |
| `DEBUG` | `false` | Enable debug mode (exposes API docs at `/api/docs`). Never enable in production. |
| `EXTERNAL_URL` | *(empty)* | Your public URL (tunnel or domain). Used to build invite links. If unset, invite links use the server's own address. |
| `SECRET_KEY` | *(random)* | JWT signing key. **Must be set** for tokens to survive server restarts. Generate one: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | `HS256` | JWT algorithm. HS256 is correct for single-server deployments. |
| `MM_TOKEN_EXPIRE_HOURS` | `8` | How long an MM login token stays valid (hours). |
| `INVITE_TOKEN_EXPIRE_HOURS` | `24` | How long a player invite link is valid (hours). |
| `FACETS_DIR` | `facets/` | Directory where Facet module YAML files are loaded from. |
| `DATA_DIR` | `data/` | Directory for persistent data files. |
| `ROLL_RATE_LIMIT` | `10/minute` | Max rolls per minute per player (rate limiting coming in v0.2). |
| `AUTH_RATE_LIMIT` | `5/minute` | Max auth attempts per minute (rate limiting coming in v0.2). |

---

## Facet Modules

The ruleset is defined by YAML files in the `facets/` directory. Each subdirectory contains a `facet.yaml` file. The `base/` facet is always loaded. Additional modules can be activated when creating a session.

### Installing a Community Facet

1. Download the facet directory (e.g., `my-expansion/facet.yaml`).
2. Place it inside `software/facets/`:
   ```
   software/facets/my-expansion/facet.yaml
   ```
3. It will appear in the MM dashboard the next time the session creation form loads.

### Writing Your Own Facet

A minimal `facet.yaml`:

```yaml
id: "my-expansion"          # slug: alphanumeric, hyphens, underscores only
name: "My Expansion"
version: "0.1.0"
authors: ["Your Name"]
description: "Adds new skills and techniques."
priority: 10                # higher priority wins on conflicting keys; base uses 0

skills:
  - id: sailing
    name: Sailing
    facet: body
    attribute: dexterity
    description: "Navigating watercraft in any conditions."
    status: active
```

See `facets/base/facet.yaml` for a complete example including attributes, character facets, techniques, roll resolution, Spark economy, and advancement rules. See `research/facet_system_design.md` for the full format specification.

**Override behaviour:** If two loaded facets define the same key (e.g., the same skill ID), the one with the higher `priority` value wins. This lets expansion modules replace or extend base content without forking it.

---

## Development Guide

### Running Tests

```bash
cd software/
pip install -r requirements-dev.txt
pytest
```

Run with `-v` for verbose output or `-x` to stop on the first failure:

```bash
pytest -v tests/test_roll_engine.py    # single file
pytest -k "TestSparkMechanics"         # by class name
pytest --tb=short                      # short tracebacks
```

### Project Structure

```
software/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── character.py    # Character creation and listing
│   │   │   ├── facets_route.py # Available Facet module listing
│   │   │   ├── rolls.py        # HTTP roll endpoint
│   │   │   └── session.py      # Session management and MM auth
│   │   └── websocket.py        # WebSocket handler and event dispatcher
│   ├── auth/
│   │   └── tokens.py           # JWT creation/verification, bcrypt hashing
│   ├── facets/
│   │   ├── loader.py           # YAML loading and validation
│   │   ├── registry.py         # Facet merging → MergedRuleset
│   │   └── schema.py           # Pydantic schema for facet.yaml files
│   ├── game/
│   │   ├── character.py        # Character model and advancement logic
│   │   ├── engine.py           # 2d6 roll resolution and Spark mechanic
│   │   └── session.py          # GameSession and SessionStore
│   ├── static/                 # Frontend (HTML, CSS, JavaScript)
│   ├── config.py               # Settings via pydantic-settings / .env
│   └── main.py                 # FastAPI app: middleware, routers, static files
├── facets/
│   └── base/
│       └── facet.yaml          # Core ruleset (always loaded)
├── research/                   # Design documents and security audit
├── tests/                      # Pytest test suite (300+ tests)
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # + pytest, httpx
└── run.py                      # Server entry point (uvicorn)
```

### Architecture

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Real-time | WebSockets (FastAPI native) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | Vanilla JS — no build step required |
| Ruleset | YAML files validated by Pydantic v2 |
| State | In-memory (SQLite persistence planned) |

### Contributing

See the root `CLAUDE.md` for the branching workflow and copyright policy. In brief:

1. Create a feature branch: `git checkout -b feature/MyFeature`
2. Write tests alongside your changes. Run `pytest` — all tests must pass.
3. Open a pull request on GitHub.

---

## Troubleshooting

**"No facet.yaml files found"**
The server can't find `facets/base/facet.yaml`. Run from the `software/` directory, or set `FACETS_DIR` to the correct absolute path in `.env`.

**"Session not found" on WebSocket connect**
Session state is in-memory. If the server restarted, the session is gone — create a new one.

**Invite link says "already been used"**
Each invite is single-use. Generate a new one from the MM dashboard.

**Players can't reach the server from outside the network**
- Ensure `HOST=0.0.0.0` in `.env`.
- For remote play, set up a Cloudflare Tunnel and set `EXTERNAL_URL`.
- Check that your firewall allows traffic on `PORT` (default 8000).

**All JWTs invalid after restart**
Set a permanent `SECRET_KEY` in `.env`. Without it, a new random key is generated on each start, which invalidates all outstanding tokens.

**Port 8000 already in use**
Set `PORT=8001` (or any available port) in `.env`.
