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
   cd facets_of_origin/software
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
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

The app has three tabs: **Build**, **Play**, and **Tools**. Everyone sees all three; what is on them depends on whether you are the Mirror Master or a player. The rules are Lean Facets v1.0 (the PHB's Quick Start is the ten-minute version).

### Build

**Players:**
- **Creation wizard** — Facet → stats (+2 / +1 / +0) → a preset class (the default) or *write your own* (name, concept, knack, two talents from your Facet's menu, kit) → a background (fifteen examples or your own: knack + Specialty) → kit by slots → magic (domain + two signature workings, for Thaumaturges and Invokers) → review. A gifted lineage also picks its gift domain.
- **Level-up** — when the MM grants a level, pick a new talent, improve one you hold, take your signature (level 3), and raise a stat (levels 4 and 8). Before level 3 you may rebuild freely.

**Mirror Master:**
- **Monster-card builder** — choose a level and a role; the numbers come from the level table, live. Fill in the card (Wants, Special, When Bloodied, Tells, Breaks, six Twists, Nastier) and save it to the session library. The Bestiary's cards load into the library the first time you connect.

### Play

**Players:** the character sheet (stats, HP, knacks, Specialty, talents with use trackers, magic, a slots grid holding gear, Wounds and Fatigue, Sparks) and five actions:
- **Roll** — 2d6 + a stat, +1 if a knack applies, at the MM's difficulty.
- **Attack** — on a 10+ pick one: +1d6 damage, a stunt, or cover for an ally. On a 7–9 you are exposed.
- **Cast** — domain, scope, working and intent; the app previews difficulty and Fatigue before you roll. On a 7–9 you choose between two costs.
- **Defend / Intercept** — attacks on you (or aimed at an ally) are Hard this exchange.
- **Avoid** — the old saving throw: 2d6 + the stat that fits.
Every action takes Spark, Help and Borrowed Trouble toggles (each adds a d6; keep the best two). At 0 HP the app rolls your Wound and prompts **Hold On**.

**Mirror Master:**
- **Combat tracker** — add foes from the library (Mooks fight as one mob), write each foe's telegraph, and press **Attack (rolls in the open)**; the app rolls, applies armor and exposure, and shows the table. HP bars, Bloodied and broken badges, **Morale** checks, and the danger read.
- **Toolbox** (private until you reveal it) — reaction roll, Pressure die (with terrain variants), fight / explore / social complications, MM move, NPC on the spot, trinkets, curios, relics, hoards, the oracle, any table by name, and **Stuck?**, which offers three ways forward.
- **Threat clocks**, **scenes and act breaks**, **breathers and nights' rest**, and **End of session**: the five level-up prompts and a Grant Level button.
- **Sparks** — award them, and confirm players' peer calls and nominations.

**Chat** is visible to everyone in the session.

### Tools

- **Rules reference** — rendered from the loaded ruleset (and any setting Facet).
- **Inventory editor** — slot-checked; equip weapon, armor and shield.
- **Notes** — player notes, and the MM's private notes (never sent to players).
- **Export** — download a character as a `.fof` file.

---

## Deployment Options

### Local LAN (simplest)

Add to `.env`:
```
HOST=0.0.0.0
```
Restart the server. Players on the same network connect to `http://<your-local-ip>:8000`.

Find your local IP with `ip route get 1` (Linux/WSL) or `ipconfig` (Windows).

---

### Cloudflare Tunnel (recommended for remote play)

Cloudflare Tunnel gives players a public HTTPS URL without opening firewall ports, changing router settings, or exposing your home IP. It's free and takes about two minutes to set up. The server speaks plain HTTP; Cloudflare handles encryption.

#### Install cloudflared

**Linux / WSL (Debian/Ubuntu):**
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
  -o cloudflared.deb
sudo dpkg -i cloudflared.deb
rm cloudflared.deb
```

**macOS (Homebrew):**
```bash
brew install cloudflared
```

**Windows:** Download the installer from the [cloudflared releases page](https://github.com/cloudflare/cloudflared/releases/latest) and run it.

#### Run a session

You need two terminals. Keep both open for the duration of the session.

**Terminal 1 — start the game server:**
```bash
cd facets_of_origin/software
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> The server must bind to `0.0.0.0` (not `127.0.0.1`) so cloudflared can reach it.
> Set `HOST=0.0.0.0` in `.env` to make this permanent.

**Terminal 2 — open the tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

Cloudflare prints a URL like:
```
https://random-words-here.trycloudflare.com
```

#### Configure the server to use the tunnel URL

Copy that URL into your `.env` file so invite links point to the public address:
```ini
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
EXTERNAL_URL=https://random-words-here.trycloudflare.com
```

Restart Terminal 1 after editing `.env`. Invite links generated after restart will use the tunnel URL automatically.

#### Notes

- **The tunnel URL changes every time** you run `cloudflared tunnel --url ...` (no-account mode). Generate fresh invites at the start of each session. If you create a [free Cloudflare account](https://dash.cloudflare.com/sign-up) and register a named tunnel, you get a stable URL.
- **WSL note:** if `localhost` doesn't work in the cloudflared command, use `127.0.0.1` explicitly: `cloudflared tunnel --url http://127.0.0.1:8000`.
- The tunnel is tied to the cloudflared process. If Terminal 2 closes, players lose connection.

---

### Caddy + Domain (permanent hosting)

If you own a domain and want a permanent URL, use [Caddy](https://caddyserver.com/) as a reverse proxy. Caddy handles HTTPS certificates automatically.

```
# Caddyfile
yourdomain.example.com {
    reverse_proxy localhost:8000
}
```

Set in `.env`:
```ini
HOST=0.0.0.0
EXTERNAL_URL=https://yourdomain.example.com
```

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
| `ROLL_RATE_LIMIT` | `10/minute` | Max roll requests per minute per client IP. |
| `AUTH_RATE_LIMIT` | `5/minute` | Max auth attempts per minute per client IP. |

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

A minimal `facet.yaml` adds content; it never changes a core rule:

```yaml
id: "my-expansion"          # slug: alphanumeric, hyphens, underscores only
name: "My Expansion"
version: "0.1.0"
authors: ["Your Name"]
description: "Adds a sea-going class and one talent."
priority: 10

talents:
  - id: sea_legs
    name: Sea Legs
    facet: body
    kind: talent
    use: passive
    text: "On a moving deck, climbing and fighting are never harder than Standard."
    improved: "Once per scene, keep your footing through anything the sea does."
    normal: "A pitching deck can make physical rolls Hard."

classes:
  - id: corsair
    name: Corsair
    facet: body
    concept: "I am a raider of the coast roads and the sea lanes."
    knack: "Ships and the sea"
    talents: [sea_legs, fast_hands]
    signature: whirlwind
    kit: [light_weapon, rope, rations]
```

A setting Facet may add `lineages`, `talents`, `classes`, `backgrounds`, `magic_domains`, curio `items` and `tables`. It may not write the core rule sections (`stats`, `facets`, `roll_resolution`, `spark`, `advancement`, `hp`, `combat`, `monsters`, `magic` and the rest), and it may not redefine a core id; the loader rejects a Facet that tries. See `facets/base/facet.yaml` for the full core, `facets/valloh/facet.yaml` for a real setting Facet, and `docs/DESIGN_lean_facets.md` §3 for the formats.

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

#### Front-end tests

`tests/e2e/test_ui_flows.py` drives the web app in a real browser and asserts
that an action a player or MM takes actually changes what they see. It covers
the failure mode the rest of the suite cannot see — a control that exists, looks
enabled, and is wired to nothing.

It skips unless Playwright is installed:

```bash
pip install playwright && playwright install chromium
pytest tests/e2e/test_ui_flows.py
```

Add a case here whenever you add a control to the UI. If a button has no
front-end test, nothing in CI notices when its handler stops working.

### Project Structure

```
software/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── character.py    # Character creation, listing, notes, inventory
│   │   │   ├── enemy.py        # Enemy CRUD endpoints
│   │   │   ├── encounter.py    # Encounter CRUD endpoints
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
│   │   ├── encounter.py        # Encounter model and TR budget calculation
│   │   ├── enemy.py            # Enemy model and Threat Rating calculation
│   │   ├── engine.py           # 2d6 roll resolution and Spark mechanic
│   │   └── session.py          # GameSession and SessionStore
│   ├── static/
│   │   ├── index.html          # SPA shell: auth, tabs, character creation
│   │   ├── css/style.css       # Styles (dark theme, responsive)
│   │   └── js/
│   │       ├── app.js          # Core: auth, WebSocket, state, routing
│   │       ├── play.js         # Play Field tab: rolling, combat, magic, chat
│   │       ├── tools.js        # Tools tab: sheets, inventory, rules, budget
│   │       ├── builder.js      # Builder tab: advancement, enemy/encounter builder
│   │       └── components.js   # Shared rendering functions
│   ├── config.py               # Settings via pydantic-settings / .env
│   └── main.py                 # FastAPI app: middleware, routers, static files
├── facets/
│   └── base/
│       └── facet.yaml          # Core ruleset (always loaded)
├── research/                   # Design documents and security audit
├── tests/                      # Pytest test suite (613 tests)
│   └── e2e/                    # End-to-end playtest simulations
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # + pytest, httpx
└── run.py                      # Server entry point (uvicorn)
```

### Architecture

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Real-time | WebSockets (FastAPI native) |
| Auth | JWT (python-jose) + bcrypt |
| Frontend | Vanilla JS — no build step required |
| Ruleset | YAML files validated by Pydantic v2 |
| State | In-memory with JSON file persistence for characters |

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
All session and character data is held in memory. If the server restarted, the session is gone — create a new one and generate fresh invite links. (Persistent storage is on the roadmap for v0.2.)

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
