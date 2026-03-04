# Self-Hosting a Digital Tabletop: Best Practices & Architecture

*Research document — Facets of Origin software implementation. 2026-03-03.*

---

## The Problem

The Mirror Master wants to run a game session from their own PC. Players connect from wherever they are. The app needs to:

- Serve game state in real time to all connected players
- Authenticate players without requiring account creation
- Keep communication secure (nobody outside the session sees game state)
- Be simple enough that a non-technical MM can start it with one command

This is the exact deployment model of **Foundry Virtual Tabletop**, the current gold standard for self-hosted TTRPGs. Their architecture is the primary reference for this document.

---

## Relevant Prior Art

### Foundry VTT
The closest equivalent to what we're building. Key design decisions:
- Node.js server, runs on GM's machine
- Players connect via browser — no install required
- "World" = campaign data. "System" = game rules plugin. "Module" = optional extensions.
- Recommends a **reverse proxy (Caddy or nginx)** for HTTPS and port exposure
- Does NOT handle HTTPS itself — delegates to the proxy layer
- Authentication: GM sets an admin password; players enter a session access key per world
- Exposes via port forwarding, or GM pays for a cloud relay service

**Lesson:** Separate concerns — the game server handles game logic; the proxy layer handles TLS and exposure. This is the right pattern.

### Owlbear Rodeo
- Simpler, cloud-hosted, no self-hosting option
- Join via link with embedded room code
- No authentication beyond link knowledge (security-by-obscurity)
- **Lesson:** Link-only auth is fine for casual use, but invite tokens should be time-limited and signed, not just room IDs embedded in URLs.

### Roll20
- Fully cloud-hosted, not self-hosted
- **Lesson:** Not directly relevant, but their "invite link" UX is the expected pattern — a URL that brings the player directly into the session.

---

## Recommended Stack

### Backend: FastAPI (Python)
**Rationale:**
- Native async support (`asyncio`) — essential for WebSocket-heavy real-time apps
- Automatic OpenAPI docs (useful for API exploration and debugging)
- Pydantic v2 for data validation — input validation is free at the model layer
- WebSocket support built in via Starlette (FastAPI is built on Starlette)
- Excellent ecosystem: `python-jose` for JWT, `passlib` for password hashing, `aiosqlite` for async SQLite, `PyYAML` for facet files

**Alternative considered:** Node.js/Express (what Foundry uses). Rejected because the project uses Python-first design thinking and FastAPI offers superior input validation ergonomics.

### Database: SQLite (via aiosqlite)
**Rationale:**
- Zero server setup — it's a file. Perfect for self-hosting.
- Async-compatible via aiosqlite
- Sufficient for single-session concurrency (an MM's game has 2–8 players, not 10,000 concurrent users)
- Data lives next to the app — easy backup, easy migration

**Alternative considered:** PostgreSQL (more scalable). Rejected because a game session is not a scale problem — SQLite is the correct tool for this use case.

### Real-time: WebSockets
**Rationale:**
- Game state (dice rolls, character updates, chat) must reach all players instantly
- HTTP polling creates perceptible lag that breaks immersion
- WebSockets are natively supported in FastAPI/Starlette
- Single persistent connection per player, managed by a connection manager

### Frontend: Vanilla JavaScript (no build step)
**Rationale:**
- No build toolchain required — players open a URL, everything just works
- Self-hosting should not require npm or webpack
- The app is not a SPA that needs client-side routing — it's a real-time game UI
- A build step can be added later; removing one is painful

---

## Security Architecture

### 1. Transport Security (TLS)

**The rule:** Never send game data over plaintext HTTP. Always HTTPS/WSS.

**For self-hosting, three practical options:**

#### Option A: Cloudflare Tunnel (Recommended for most MMs)
Cloudflare Tunnel (`cloudflared`) creates an encrypted tunnel from the MM's machine to Cloudflare's edge without opening any inbound ports on the home router. Cloudflare terminates TLS and proxies traffic to localhost.

```bash
# MM installs cloudflared, then:
cloudflared tunnel --url http://localhost:8000
# Returns: https://random-subdomain.trycloudflare.com
# Share this URL with players
```

**Advantages:** No port forwarding required. No static IP required. Free for this use case. Automatic HTTPS. Hides home IP.

#### Option B: Reverse Proxy + Port Forwarding (For MMs who control their router)
Use **Caddy** (recommended over nginx for simplicity — automatic HTTPS if you have a domain):

```caddyfile
facets.yourdomain.com {
    reverse_proxy localhost:8000
}
```

Requires: owning a domain, port 80/443 forwarded on the router.

#### Option C: Local Network Only (For in-person or VPN sessions)
Run with `--host 0.0.0.0` and share the local IP. All players must be on the same network, or connect via **Tailscale** (a simple WireGuard-based VPN mesh):

```
tailscale up
# All devices on the tailnet can reach each other at stable IPs
```

**The app should default to localhost-only** and require explicit configuration to expose externally. This prevents accidental exposure.

### 2. Authentication

**MM Authentication (admin access):**
- MM sets a password on first run, stored as a **bcrypt hash** (never plaintext)
- Login returns a signed JWT with role `"mm"` and a reasonable expiry (8 hours — a session length)
- JWT is stored in `sessionStorage` (not `localStorage`) so it clears when the browser closes

**Player Authentication (invite links):**
- MM generates an invite link for each player via the dashboard
- The link contains a **signed JWT** with: role `"player"`, player name, session ID, expiry (24 hours)
- Tokens are single-use enforced at the server — once a player has connected, the invite token is consumed and a session token is issued
- Invite tokens must not be reusable — if a token is intercepted, it shouldn't let a third party join

**Security properties:**
- Tokens are signed with a server-side secret key (generated at startup, stored in `.env`)
- Token payloads include `iat` (issued-at) and `exp` (expiry) claims
- The server verifies signature and expiry on every request
- WebSocket connections authenticate via token in the `Authorization` header at upgrade time (not in the URL, to avoid logging)

### 3. Input Validation

FastAPI + Pydantic v2 provides model-level validation at every API boundary. Additional rules:

- **Roll requests**: Validate that attribute modifiers claimed by the client match server-side character data — the client does not get to pick its own modifier
- **Character updates**: Attribute distribution is validated server-side (total point budget enforced)
- **Facet file uploads**: YAML is parsed and validated against the Pydantic schema before it touches any game state
- **Chat/narration input**: Strip HTML. Truncate to reasonable length (2000 chars). No eval, no execution.
- **Player names in tokens**: Validate on issue, not just at use. Alphanumeric + spaces, max 32 chars.

### 4. Rate Limiting

Use `slowapi` (the FastAPI equivalent of Flask-Limiter):
- Roll endpoint: 10 requests/minute per player (prevents spam rolling)
- Auth endpoint: 5 attempts/minute per IP (prevents brute-force)
- WebSocket: reconnection rate limited (prevents flood)

### 5. Security Headers

Applied via middleware:
```
Content-Security-Policy: default-src 'self'; script-src 'self'; connect-src 'self' wss:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
```

CSP `connect-src wss:` permits WebSocket connections to the same origin only.

### 6. CORS

CORS is restricted to the server's own origin. Cross-origin requests to the API are rejected. This prevents third-party sites from using a player's session token to make API calls on their behalf.

```python
allow_origins=["http://localhost:8000"]  # adjusted at startup based on configured URL
```

---

## Deployment Topology

```
Players (browsers)
     │
     │  HTTPS / WSS
     ▼
[Cloudflare Tunnel or Caddy] ──── terminates TLS
     │
     │  HTTP / WS (localhost)
     ▼
[FastAPI server :8000] ──── game logic, auth, WebSocket hub
     │
[SQLite database]    [facets/ directory]
     │
[Static files (served by FastAPI)]
```

---

## What NOT to Do

- **Do not store tokens in localStorage** — vulnerable to XSS. Use `sessionStorage` or `HttpOnly` cookies.
- **Do not put tokens in URL query strings** — they appear in server logs and browser history.
- **Do not disable HTTPS "for testing" on a deployed instance** — test locally, deploy securely.
- **Do not trust client-submitted roll results** — always resolve rolls server-side.
- **Do not expose the admin password endpoint without rate limiting** — brute force is trivial without it.
- **Do not auto-expose to the internet** — the default should be localhost. External exposure is opt-in.

---

## Summary of Recommendations

| Concern | Recommendation |
|---|---|
| Backend | FastAPI + Uvicorn |
| Database | SQLite via aiosqlite |
| Real-time | WebSockets (native FastAPI) |
| Frontend | Vanilla JS, no build step |
| TLS for external | Cloudflare Tunnel (simplest) or Caddy (domain required) |
| TLS for local | Local network only, or Tailscale for VPN |
| Auth | JWT: bcrypt-hashed MM password + signed invite tokens |
| Token storage | sessionStorage (not localStorage) |
| Input validation | Pydantic v2 models at every API boundary |
| Rate limiting | slowapi on auth and roll endpoints |
| Security headers | CSP, X-Content-Type-Options, X-Frame-Options |
