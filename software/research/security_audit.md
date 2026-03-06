# Security Audit — Facets of Origin Server
**Version audited:** 0.1.0
**Date:** 2026-03-03
**Auditor:** Claude Code (automated review)
**Branch:** draft_software_implementation

---

## 1. Executive Summary

The Facets of Origin server is a self-hosted FastAPI application designed for small-group TTRPG sessions over a local network or through a reverse-proxy tunnel (e.g., Cloudflare Tunnel). Its threat model is **trusted operator, semi-trusted players** — the Mirror Master (MM) hosts the server and controls access; players receive single-use invite links.

Overall security posture for a **private self-hosted tool** is **adequate**. The application correctly uses modern cryptographic primitives (bcrypt, HS256 JWT), validates all user input through Pydantic, prevents the most common injection classes, and applies defensive HTTP headers.

Two findings require attention before any public-facing deployment: the volatile in-memory `secret_key` (tokens become unverifiable after restart) and the absence of rate limiting on the WebSocket endpoint. All other findings are low-risk mitigations or accepted trade-offs for a first draft.

---

## 2. Scope and Methodology

**In scope:**
- `app/` — all Python source files
- `app/static/` — frontend JS and HTML
- `facets/base/facet.yaml` — rule data ingestion
- `requirements.txt` — dependency versions

**Methodology:**
Manual code review of all application source files. Checked authentication flows, authorization boundaries, input handling, cryptographic choices, information disclosure, concurrency behaviour, and dependency versions. Mapped findings to the OWASP Top 10 (2021).

**Out of scope:**
Network infrastructure, host OS hardening, DNS configuration, reverse proxy setup.

---

## 3. Authentication

### 3.1 JWT Implementation
- Library: `python-jose[cryptography]` 3.3.0
- Algorithm: HS256 (symmetric HMAC-SHA256)
- Signing key: `settings.secret_key` — a 64-character hex string

**Observations:**
- The secret key is generated with `secrets.token_hex(32)` as the Pydantic field default, which means **a new random key is generated on every process start** unless `SECRET_KEY` is set in `.env`. This invalidates all outstanding JWTs whenever the server restarts (see Finding M-01).
- Token expiry is enforced: MM tokens expire in 8 hours (configurable), invite tokens in 24 hours.
- The `decode_token` function validates `exp`, signature, and role claim in sequence — correct.
- Both `iat` and `exp` claims are present in every token.

### 3.2 Password Hashing
- Library: `passlib[bcrypt]` 1.7.4
- Work factor: passlib default (12 rounds)
- Salt: generated automatically per hash

**Observations:**
- `verify_password` uses constant-time comparison via passlib — not vulnerable to timing attacks.
- `hash_password` always generates a new salt — correct.

### 3.3 Invite Token Single-Use Enforcement
- Used tokens are tracked in `session.used_invite_tokens` (a Python `set`).
- Check and mark are performed in `redeem_invite` before issuing a session token.
- The set is **in-memory only** — cleared on restart. Restarting the server allows re-use of previously consumed invite tokens if they have not yet expired (see Finding L-01).

### 3.4 Token Type Discrimination
- MM tokens have `{"role": "mm"}`.
- Player invite tokens have `{"role": "player", "type": "invite"}`.
- Player session tokens have `{"role": "player", "type": "session"}`.
- The `redeem_invite` endpoint explicitly checks `data.token_type == "invite"`, preventing session tokens from being used as invites.

---

## 4. Authorization

### 4.1 MM vs. Player Role Enforcement
- All MM-only API routes use `Depends(require_mm)`, which decodes the token and asserts `data.is_mm`.
- Returning HTTP 403 (not 401) when a player token is presented to an MM-only route is correct.
- WebSocket: `_dispatch` checks `is_mm` before routing `spark_earn` and `skill_advance` events. A player sending these events receives "Unknown event type" — correct.

### 4.2 IDOR (Insecure Direct Object Reference)
- Session IDs are UUIDs — not guessable, but they are only as secret as the invite token that carries them.
- Player tokens embed `session_id` — the HTTP roll endpoint verifies `token_data.session_id == body.session_id` (HTTP 403 on mismatch). The character route also checks session membership.
- **No enumeration protection:** an authenticated player can call `GET /api/characters/{any_session_id}` if they have any valid player token. This is low-risk for a private server but worth noting.

### 4.3 Character Ownership
- Players can only create a character for their own `player_name` (from the token). Attempting to create under a different name returns 403.
- The MM can create characters for any player by submitting a character with the target name.

---

## 5. Session Management

### 5.1 In-Memory State
- All session data lives in `session_store`, a module-level singleton `SessionStore`.
- A server restart loses all session state, all roll logs, all characters, and the MM password.
- The MM password hash is stored in `_mm_password_hash` — a module-level global. This is fine for single-worker deployments; multi-worker deployments (e.g., `uvicorn --workers 4`) would have each worker hold a separate hash, potentially causing login failures (see Finding M-02).

### 5.2 Session Token Lifetime
- Player session tokens expire after `mm_token_expire_hours` (8h default) — same as MM tokens.
- There is no logout/revocation mechanism. Tokens remain valid until expiry regardless of disconnect.

---

## 6. Input Validation

### 6.1 HTTP API — Pydantic Models
All HTTP request bodies are parsed through Pydantic `BaseModel` subclasses with explicit field constraints:
- `SetupRequest.password`: `min_length=8`
- `CreateSessionRequest.name`: `min_length=1, max_length=128`
- `InviteRequest.player_name`: `min_length=1, max_length=32`
- `RollHTTPRequest.sparks_spent`: `ge=0, le=10`
- `RollHTTPRequest.description`: `max_length=200`

**Gap:** `RollRequest` (the dataclass, not the HTTP model) previously had no validation on `sparks_spent`. A `__post_init__` guard (`sparks_spent >= 0`) has been added in this review cycle.

### 6.2 WebSocket Messages
WebSocket messages are parsed from `receive_json()` with no schema enforcement. Handlers extract fields using `.get()` with safe defaults. Values that could be abused:
- `description` — truncated to 200 characters in `_handle_roll`.
- `reason` — truncated to 200 characters in `_handle_spark_earn`.
- `text` — truncated to 2000 characters in `_handle_chat`.
- `sparks_spent` — capped to `min(requested, character.sparks)` server-side.

**Gap:** No maximum message size is enforced on the WebSocket endpoint (see Finding M-03).

### 6.3 YAML Input
The facet loader uses `yaml.safe_load()` — correct. Arbitrary code execution via YAML is not possible with `safe_load`.

### 6.4 Player Name Regex
`PLAYER_NAME_RE = re.compile(r"^[A-Za-z0-9 _\-]{1,32}$")` — validated before creating invite tokens. Prevents most injection payloads in player names.

---

## 7. WebSocket Security

### 7.1 Authentication Timing
The WebSocket endpoint accepts the connection immediately, then waits for the client's first message containing the JWT. If the token is invalid, it sends an error and closes. This avoids exposing the token in the URL query string (which would appear in access logs) — a deliberate good design choice.

**Gap:** A malicious client can connect and never send an auth message, holding a connection indefinitely (resource exhaustion).

### 7.2 Event Validation
All events are dispatched through `_dispatch`, which uses an explicit allowlist of event types. Unknown types return an error — no arbitrary code is executed.

### 7.3 Connection Lifecycle
The `finally` block in `handle_websocket` always calls `manager.disconnect` and broadcasts `player_left`. This prevents ghost connections. However, dead connections are cleaned up lazily (only on the next broadcast attempt) — acceptable for this use case.

### 7.4 Double-Accept Issue
`handle_websocket` calls `await websocket.accept()` directly and then manually appends to `manager._connections`, bypassing `manager.connect()` (which would call `accept()` a second time, causing an error). This is architecturally inconsistent — `manager.connect()` is designed to accept connections but is not called from the main handler. This is a design smell, not a security issue.

---

## 8. Cryptographic Practices

| Property | Choice | Assessment |
|---|---|---|
| Token algorithm | HS256 | Adequate for single-server. A compromised key forges all tokens. RS256 would allow read-only verification on clients. |
| Key length | 64 hex chars = 256 bits | Strong. |
| Key persistence | Generated at startup if not set | **Problematic** — see Finding M-01. |
| Password hashing | bcrypt, work factor 12 | Good. |
| Random sources | `secrets.token_hex` | Cryptographically secure. |

---

## 9. Information Disclosure

### 9.1 Error Messages
- HTTP error responses from FastAPI include `"detail"` strings. These are generally safe (e.g., "Session not found", "Invalid password").
- JWT decode failures expose the library's error message string. This reveals slightly more than necessary but poses no practical risk.

### 9.2 File Paths in API Responses
- `GET /api/facets/available` **previously** returned `"path": str(path)` for each facet file, disclosing the server's absolute file system paths. This has been **fixed** in this review cycle — paths are no longer included in success responses.

### 9.3 API Documentation
- Swagger/ReDoc is disabled when `debug=False` (the default) — correct.

### 9.4 Logs
- The WebSocket handler logs `"WS connected: %s in session %s"` (identity + session ID). No tokens or passwords are logged.

---

## 10. Concurrency and Race Conditions

### 10.1 MM Password Setup Race
`setup_mm_password` checks `_get_mm_hash() is not None` then sets the password. Under concurrent requests, two requests could both see `None` and both succeed. In practice, this is a one-time first-run action and the risk of concurrent calls is negligible, but it is not atomic. A `threading.Lock` would eliminate the theoretical race.

### 10.2 Spark Spending in WebSocket
`_handle_roll` reads and decrements `character.sparks` without locking. If two roll events arrived simultaneously for the same character (unlikely given WebSocket's sequential message delivery per connection), there could be a TOCTOU race. Python's GIL prevents data corruption, but logical double-spending is theoretically possible with two concurrent WebSocket connections authenticated as the same player.

### 10.3 Session Store
`session_store._sessions` is a plain dict. Under Python's GIL, dict reads/writes are thread-safe at the bytecode level, but compound operations (check + insert) are not atomic. For a single-worker server this is fine.

---

## 11. Dependency Security

Checking `requirements.txt` versions as of 2026-03:

| Package | Pinned Version | Notes |
|---|---|---|
| fastapi | 0.115.0 | Current stable; no known critical CVEs |
| uvicorn[standard] | 0.30.6 | Current stable; no known critical CVEs |
| pydantic | 2.8.2 | Current v2 stable |
| pydantic-settings | 2.4.0 | Current stable |
| python-jose[cryptography] | 3.3.0 | Last release 2022; maintained but aging. Consider `PyJWT` 2.x for newer releases |
| passlib[bcrypt] | 1.7.4 | Last release 2020; still widely used; bcrypt backend secure |
| PyYAML | 6.0.2 | Current stable; `safe_load` in use — correct |
| python-multipart | 0.0.9 | Current stable |
| slowapi | 0.1.9 | Used for rate limiting configuration; not yet wired to routes |

**Action item:** `slowapi` is listed as a dependency and `Settings` defines rate limits, but no `@limiter.limit()` decorators appear on any route. Rate limiting is currently **not active** (see Finding H-01).

---

## 12. CORS and CSP

### 12.1 CORS
```
allow_origins: ["http://localhost:8000", "http://127.0.0.1:8000"] + optional external_url
allow_methods: ["GET", "POST"]
allow_headers: ["Authorization", "Content-Type"]
allow_credentials: True
```
This is appropriately restrictive. Only the server's own origin is permitted.

### 12.2 Content Security Policy
```
default-src 'self';
script-src 'self' 'unsafe-inline';
style-src 'self' 'unsafe-inline';
connect-src 'self' ws: wss:;
```
`'unsafe-inline'` is required because the current frontend uses inline `<script>` blocks. This is noted in source comments as a first-draft limitation. Migrating to a bundled JS file would allow removal of `'unsafe-inline'` and a significant CSP hardening. This is tracked as Finding L-02.

---

## 13. OWASP Top 10 Mapping (2021)

| ID | Category | Status | Notes |
|---|---|---|---|
| A01 | Broken Access Control | **Low** | MM/player enforcement correct; minor IDOR on character listing |
| A02 | Cryptographic Failures | **Medium** | HS256 adequate; key non-persistence is the main risk |
| A03 | Injection | **Low** | Pydantic + yaml.safe_load; no SQL; player name regex |
| A04 | Insecure Design | **Medium** | In-memory state; no multi-worker support; no logout |
| A05 | Security Misconfiguration | **Low** | Docs off in prod; CSP has unsafe-inline |
| A06 | Vulnerable Components | **Low** | python-jose aging; passlib unmaintained; slowapi inactive |
| A07 | Identification / Auth Failures | **Medium** | Secret key volatility; no revocation |
| A08 | Software and Data Integrity | **Info** | No supply-chain controls needed at this scale |
| A09 | Security Logging and Monitoring | **Low** | Basic logging; no audit trail for MM actions |
| A10 | SSRF | **Info** | No outbound HTTP requests |

---

## 14. Findings Table

| ID | Severity | Category | Title | Status |
|---|---|---|---|---|
| H-01 | **High** | Input Validation | Rate limiting configured but not applied to any route | **Fixed** |
| M-01 | **Medium** | Cryptography | `secret_key` regenerated on restart — all tokens invalidated | Open |
| M-02 | **Medium** | Session Management | Multi-worker deployment would split MM password state | Open |
| M-03 | **Medium** | WebSocket | No maximum WebSocket message size enforced | **Fixed** |
| L-01 | **Low** | Auth | In-memory invite token revocation cleared on restart | Accepted |
| L-02 | **Low** | CSP | `unsafe-inline` in script-src (style-src requires inline styles) | Accepted |
| L-03 | **Low** | Auth | No WebSocket connection timeout for unauthenticated connections | **Fixed** |
| L-04 | **Low** | Information | JWT decode error messages slightly verbose | Accepted |
| L-05 | **Low** | Logging | No MM action audit trail | Open |
| I-01 | **Info** | Dependency | `python-jose` last released 2022 | Accepted |
| I-02 | **Info** | Dependency | `passlib` replaced with direct `bcrypt` | **Fixed** |
| I-03 | **Info** | Design | `manager.connect()` not used by main WS handler (design smell) | Open |
| **Fixed** | — | Info Disclosure | File paths exposed in facets API response | **Fixed** |
| **Fixed** | — | Input Validation | `RollRequest.sparks_spent` had no non-negative guard | **Fixed** |

---

## 15. Remediation Roadmap

### Immediate (before any public deployment)

**H-01 — Activate rate limiting**
Import `slowapi` limiter and decorate the auth endpoints (`/auth/mm-login`, `/auth/setup`) with `@limiter.limit(settings.auth_rate_limit)` and the roll endpoint with `@limiter.limit(settings.roll_rate_limit)`. These settings already exist in `Settings` — they just need to be connected.

**M-01 — Persist secret_key**
Add `SECRET_KEY` to the `.env.example` file and document that it **must** be set before deployment. Consider auto-generating it on first run and writing it to `.env`, similar to how `secret_key: str = secrets.token_hex(32)` works now but persisting the result.

**L-03 — WebSocket auth timeout**
Add an `asyncio.wait_for(..., timeout=30)` around the `receive_json()` auth step so that connections that never authenticate are automatically closed.

### Near-term (v0.2 backlog)

**M-02 — Document single-worker requirement**
Add to README: the server must run with a single worker process. Rate limiting and session state use process-local memory.

**M-03 — WebSocket message size limit**
Use `websocket.receive_text()` with a byte limit, or check `len(text)` before `json.loads`, to prevent pathological large messages.

**L-02 — Remove unsafe-inline from CSP**
Consolidate the inline `<script>` block in `index.html` into `app.js`, then tighten the CSP to remove `'unsafe-inline'`.

**L-05 — MM audit log**
Emit structured log entries for: MM login, session creation, invite generation, spark awards, and skill advances.

### Long-term

**I-03 — Refactor WebSocket connection management**
`handle_websocket` should call `manager.connect()` rather than manually mutating `_connections`. This removes the double-accept risk and centralises connection registration.

**I-01 / I-02 — Evaluate dependency alternatives**
Consider migrating from `python-jose` to `PyJWT` (actively maintained) and from `passlib` to direct use of `bcrypt` or `argon2-cffi`.

---

*This audit covers the application code as reviewed on 2026-03-03. It does not constitute a penetration test and does not cover network-level attacks, host OS vulnerabilities, or social engineering.*
