"""WebSocket connection manager and event dispatcher (Lean Facets v1.0, DESIGN §4.2).

This module is plumbing: authentication, permissions, message limits, and
broadcasting. Every rule lives in the engine (`app.game.engine`, `combat`,
`magic`, `character`, `toolbox`); a handler reads the message, calls the
engine, and tells the table what happened. No handler carries a rule of its
own (CLAUDE.md: the simulator and the app may only drive the rules module).

Security patterns kept from v0.3: the token arrives in the first message (not
the URL), unauthenticated sockets time out, every message is size-capped, and
MM-only events are refused for players. Players act only as themselves; the
MM may act for any character by naming `player`.

Dice: handlers pass the module-level `RNG` to the engine so tests can script
the dice. Clients can never supply dice.
"""
from __future__ import annotations

import asyncio
import json
import logging
import random
import time
import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Optional

import yaml
from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError

from app.auth.tokens import decode_token
from app.game import combat, magic, toolbox
from app.game.engine import resolve_avoid, roll_character, roll_result_to_dict
from app.game.enemy import Enemy, EnemyFormatError
from app.game.session import ThreatClock, _player_enemy_view, session_store

logger = logging.getLogger(__name__)

#: The dice source for every handler. Tests replace it with a scripted one.
RNG: random.Random = random.Random()

#: Where the Bestiary's cards live (repo/enemies/*.fof); seeded into a
#: session's enemy library the first time its MM connects.
BESTIARY_DIR = Path(__file__).resolve().parents[3] / "enemies"


class ConnectionManager:
    """Tracks active WebSocket connections per session."""

    def __init__(self) -> None:
        # session_id -> list of (websocket, player_name | "mm")
        self._connections: dict[str, list[tuple[WebSocket, str]]] = {}

    async def connect(self, websocket: WebSocket, session_id: str, identity: str) -> None:
        await websocket.accept()
        self._connections.setdefault(session_id, []).append((websocket, identity))
        logger.info("WS connected: %s in session %s", identity, session_id)

    def register(self, websocket: WebSocket, session_id: str, identity: str) -> None:
        self._connections.setdefault(session_id, []).append((websocket, identity))

    def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        connections = self._connections.get(session_id, [])
        self._connections[session_id] = [(ws, ident) for ws, ident in connections if ws is not websocket]

    async def broadcast(self, session_id: str, message: dict) -> None:
        """Send a message to all connections in a session."""
        dead: list[WebSocket] = []
        for ws, _ in list(self._connections.get(session_id, [])):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, session_id)

    async def broadcast_split(self, session_id: str, mm_message: dict, player_message: dict) -> None:
        """The MM gets one view, everyone else another (e.g. a foe's HP)."""
        dead: list[WebSocket] = []
        for ws, ident in list(self._connections.get(session_id, [])):
            try:
                await ws.send_json(mm_message if ident == "mm" else player_message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, session_id)

    async def send_to(self, websocket: WebSocket, message: dict) -> bool:
        """Send a message to a single WebSocket. Returns True on success, False on failure."""
        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            logger.warning("Failed to send to websocket: %s", e)
            return False

    async def send_to_identity(self, session_id: str, identity: str, message: dict) -> None:
        """Send to every connection in *session_id* held by *identity* (e.g. ``"mm"``)."""
        for ws, ident in list(self._connections.get(session_id, [])):
            if ident == identity:
                await self.send_to(ws, message)

    def identities(self, session_id: str) -> list[tuple[WebSocket, str]]:
        return list(self._connections.get(session_id, []))


manager = ConnectionManager()

# Maximum allowed WebSocket message size in bytes (M-03).
WS_MAX_MESSAGE_BYTES = 8_192
# Seconds to wait for the auth message before closing unauthenticated connections (L-03).
WS_AUTH_TIMEOUT_SECONDS = 30
# How many private toolbox results the MM can still reveal.
PRIVATE_RESULTS_KEPT = 50


# ---------------------------------------------------------------------------
# Table state the app keeps beside the engine's (pending choices, reveals)
# ---------------------------------------------------------------------------

@dataclass
class TableState:
    """App-layer bookkeeping for a session: nothing here is a rule."""

    #: player -> a 10+ attack awaiting its option pick (replayed with the same dice).
    pending_attacks: dict[str, dict] = field(default_factory=dict)
    #: player -> the two 7-9 casting costs offered.
    pending_complications: dict[str, list[dict]] = field(default_factory=dict)
    #: players at 0 HP who have taken their Wound and must roll Hold On.
    pending_hold_on: set[str] = field(default_factory=set)
    #: MM-private toolbox results that can still be revealed.
    private_results: "OrderedDict[str, dict]" = field(default_factory=OrderedDict)
    bestiary_seeded: bool = False


_tables: dict[str, TableState] = {}


def table_state(session_id: str) -> TableState:
    return _tables.setdefault(session_id, TableState())


class WSError(Exception):
    """A refusal sent back to the sender only."""


@dataclass
class Ctx:
    websocket: WebSocket
    msg: dict
    session: Any
    session_id: str
    identity: str
    is_mm: bool

    @property
    def rs(self):
        return self.session.ruleset

    @property
    def table(self) -> TableState:
        return table_state(self.session_id)


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

async def handle_websocket(websocket: WebSocket) -> None:
    """Main WebSocket handler — authentication then event loop."""
    session_id: str | None = None
    identity: str = "unknown"

    try:
        # Step 1: authenticate via the first message (not the URL — avoids logging the token)
        await websocket.accept()
        try:
            auth_text = await asyncio.wait_for(websocket.receive_text(), timeout=WS_AUTH_TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            await websocket.send_json({"type": "error", "message": "Authentication timeout."})
            await websocket.close(code=1008)
            return
        if len(auth_text) > WS_MAX_MESSAGE_BYTES:
            await websocket.send_json({"type": "error", "message": "Message too large."})
            await websocket.close(code=1009)
            return
        try:
            auth_msg = json.loads(auth_text)
            if not isinstance(auth_msg, dict):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            await websocket.send_json({"type": "error", "message": "Invalid JSON."})
            await websocket.close(code=1008)
            return

        token = auth_msg.get("token", "")
        try:
            token_data = decode_token(token)
        except JWTError as e:
            await websocket.send_json({"type": "error", "message": f"Authentication failed: {e}"})
            await websocket.close(code=1008)
            return
        if token_data.token_type == "invite":
            await websocket.send_json({"type": "error", "message": "Redeem the invite first."})
            await websocket.close(code=1008)
            return

        session_id = token_data.session_id if token_data.role == "player" else auth_msg.get("session_id")
        if not session_id:
            await websocket.send_json({"type": "error", "message": "Missing session_id."})
            await websocket.close(code=1008)
            return
        session = session_store.get(session_id)
        if not session:
            await websocket.send_json({"type": "error", "message": "Session not found."})
            await websocket.close(code=1008)
            session_id = None
            return

        identity = "mm" if token_data.is_mm else (token_data.player_name or "player")
        manager.register(websocket, session_id, identity)
        if token_data.is_mm:
            _seed_bestiary(session, table_state(session_id))
        await manager.send_to(websocket, {"type": "state",
                                          "data": state_for(session, identity, token_data.is_mm)})
        await manager.broadcast(session_id, {"type": "player_joined", "player": identity})

        # Step 2: event loop — enforce message size on every incoming message (M-03).
        while True:
            text = await websocket.receive_text()
            if len(text) > WS_MAX_MESSAGE_BYTES:
                await manager.send_to(websocket, {"type": "error", "message": "Message too large."})
                continue
            try:
                raw = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                await manager.send_to(websocket, {"type": "error", "message": "Invalid JSON."})
                continue
            if not isinstance(raw, dict):
                await manager.send_to(websocket, {"type": "error", "message": "Invalid message."})
                continue
            await _dispatch(websocket, raw, session_id, identity, token_data.is_mm)

    except WebSocketDisconnect:
        pass
    except Exception as e:  # pragma: no cover - defensive
        logger.exception("Unexpected WS error for %s: %s", identity, e)
    finally:
        if session_id:
            manager.disconnect(websocket, session_id)
            await manager.broadcast(session_id, {"type": "player_left", "player": identity})


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def character_view(session, ch) -> dict:
    """A character for clients: the engine's view plus use trackers and table flags."""
    rs = session.ruleset
    d = ch.to_client_dict(rs)
    uses = {}
    for t in ch.talents:
        tdef = rs.get_talent(t.id)
        if tdef is not None and tdef.use not in ("passive", "at_will"):
            uses[t.id] = ch.uses_remaining(rs, t.id)
    if ch.signature:
        sdef = rs.get_talent(ch.signature)
        if sdef is not None and sdef.use not in ("passive", "at_will"):
            uses[ch.signature] = ch.uses_remaining(rs, ch.signature)
    d["talent_uses_left"] = uses
    d["player_name"] = ch.player_name
    d["level_up_ready"] = ch.player_name in session.level_up_ready
    d["must_hold_on"] = ch.player_name in table_state(session.id).pending_hold_on
    d["can_respec"] = ch.can_respec(rs)
    return d


def state_for(session, identity: str, is_mm: bool) -> dict:
    """The join-time state, with character views that carry use trackers."""
    if is_mm:
        data = session.to_state_dict()
    else:
        data = session.to_player_state_dict(identity)
        ch = session.characters.get(identity)
        data["your_character"] = _player_safe(character_view(session, ch)) if ch else None
    views = {pn: character_view(session, c) for pn, c in session.characters.items()}
    data["all_characters"] = views if is_mm else {pn: _player_safe(v) for pn, v in views.items()}
    data["role"] = "mm" if is_mm else "player"
    data["you"] = identity
    return data


def _enemy_msgs(session, enemy, kind: str = "enemy_updated") -> tuple[dict, dict]:
    rs = session.ruleset
    return ({"type": kind, "enemy": enemy.to_client_dict(rs)},
            {"type": kind, "enemy": _player_enemy_view(enemy, rs)})


async def _push_enemy(ctx: Ctx, enemy, kind: str = "enemy_updated") -> None:
    mm, pl = _enemy_msgs(ctx.session, enemy, kind)
    await manager.broadcast_split(ctx.session_id, mm, pl)
    await _push_danger(ctx)


async def _push_danger(ctx: Ctx) -> None:
    await manager.send_to_identity(ctx.session_id, "mm",
                                   {"type": "danger", "danger": ctx.session.active_danger()})


def _player_safe(view: dict) -> dict:
    """What players see of a character: everything but the MM's private notes."""
    return {k: v for k, v in view.items() if k != "notes_mm"}


async def _push_character(ctx: Ctx, ch) -> None:
    view = character_view(ctx.session, ch)
    base = {"type": "character_updated", "player": ch.player_name}
    await manager.broadcast_split(ctx.session_id, {**base, "character": view},
                                  {**base, "character": _player_safe(view)})
    _save(ctx.session, ch.player_name)


async def _push_state(session_id: str) -> None:
    session = session_store.get(session_id)
    if session is None:
        return
    for ws, ident in manager.identities(session_id):
        await manager.send_to(ws, {"type": "state", "data": state_for(session, ident, ident == "mm")})


def _save(session, player_name: str) -> None:
    try:
        session.save_character_to_disk(player_name)
    except IOError as e:  # pragma: no cover - disk trouble is logged, not fatal
        logger.warning("%s", e)


def _strip_enemy_hp(result: Optional[dict]) -> Optional[dict]:
    """Players see what a hit did, not how much HP the foe has left."""
    if not result:
        return result
    r = dict(result)
    for k in ("hp_before", "hp_after"):
        r.pop(k, None)
    return r


# ---------------------------------------------------------------------------
# Message parsing
# ---------------------------------------------------------------------------

def _int(msg: dict, key: str, default: int = 0, lo: int = 0, hi: int = 99) -> int:
    v = msg.get(key, default)
    if v is None or v == "":
        v = default
    try:
        n = int(v)
    except (TypeError, ValueError):
        raise WSError(f"{key} must be a number.")
    if not lo <= n <= hi:
        raise WSError(f"{key} must be between {lo} and {hi}.")
    return n


def _bool(msg: dict, key: str) -> bool:
    return bool(msg.get(key, False))


def _str(msg: dict, key: str, limit: int = 200, default: str = "") -> str:
    v = msg.get(key, default)
    return default if v is None else str(v)[:limit].strip()


def _difficulty(ctx: Ctx, key: str = "difficulty", default: str = "Standard") -> str:
    label = _str(ctx.msg, key, 20) or default
    labels = [d.label for d in ctx.rs.roll_resolution.difficulty_modifiers]
    if label not in labels:
        raise WSError(f"Difficulty must be one of {labels}.")
    return label


def _stat(ctx: Ctx, default: Optional[str] = None) -> str:
    stat = _str(ctx.msg, "stat", 20) or (default or "")
    if stat not in {s.id for s in ctx.rs.stats}:
        raise WSError("Name a stat: body, mind or soul.")
    return stat


def _extra_dice(ctx: Ctx) -> dict:
    """Sparks, Help and Borrowed Trouble, as the engine takes them."""
    return {"sparks": _int(ctx.msg, "sparks", 0, 0, 10),
            "help": _int(ctx.msg, "help", 0, 0, 1),
            "borrowed_trouble": _bool(ctx.msg, "borrowed_trouble")}


def _actor(ctx: Ctx):
    """The character acting: a player acts as themselves; the MM names `player`."""
    if ctx.is_mm:
        player = _str(ctx.msg, "player", 64)
        if not player:
            raise WSError("Name the player this is for.")
    else:
        player = ctx.identity
    ch = ctx.session.characters.get(player)
    if ch is None:
        raise WSError(f"No character for {player}." if ctx.is_mm else "You have no character yet.")
    return ch


def _target_character(ctx: Ctx, key: str = "player"):
    name = _str(ctx.msg, key, 64)
    ch = ctx.session.characters.get(name)
    if ch is None:   # accept a character name as well as a player name
        ch = next((c for c in ctx.session.characters.values() if c.name == name), None)
    if ch is None:
        raise WSError(f"No character {name!r}.")
    return ch


def _enemy(ctx: Ctx, key: str = "enemy", required: bool = True):
    k = _str(ctx.msg, key, 64)
    if not k:
        if required:
            raise WSError("Name the foe.")
        return None
    e = ctx.session.active_enemies.get(k)
    if e is None:
        raise WSError(f"No foe {k!r} on the tracker.")
    return e


def _party(session) -> dict:
    return {c.name: c for c in session.characters.values()}


def _by_character_name(session, name: str):
    return next((c for c in session.characters.values() if c.name == name), None)


def _record_roll(session, player_name: str, roll_dict: dict) -> None:
    """The natural 2's automatic Graceful Fail, then the roll log. Every
    rolling handler goes through here so the rule reads the same everywhere."""
    session.confirm_natural_two_graceful_fail(player_name, roll_dict)
    session.record_roll(player_name, roll_dict)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

Handler = Callable[[Ctx], Awaitable[None]]
#: event -> (handler, MM only)
HANDLERS: dict[str, tuple[Handler, bool]] = {}


def on(event: str, mm_only: bool = False):
    def deco(fn: Handler) -> Handler:
        HANDLERS[event] = (fn, mm_only)
        return fn
    return deco


async def _dispatch(websocket: WebSocket, msg: dict, session_id: str, identity: str,
                    is_mm: bool) -> None:
    """Route an incoming message: permission first, then the handler."""
    event_type = msg.get("type")
    session = session_store.get(session_id)
    if session is None:
        return
    entry = HANDLERS.get(event_type) if isinstance(event_type, str) else None
    if entry is None:
        await manager.send_to(websocket, {"type": "error", "message": f"Unknown event: {event_type!r}"})
        return
    handler, mm_only = entry
    if mm_only and not is_mm:
        await manager.send_to(websocket, {"type": "error", "event": event_type,
                                          "message": "Only the Mirror Master can do that."})
        return
    ctx = Ctx(websocket, msg, session, session_id, identity, is_mm)
    try:
        await handler(ctx)
    except (WSError, ValueError, KeyError) as e:
        text = e.args[0] if isinstance(e, KeyError) and e.args else str(e)
        await manager.send_to(websocket, {"type": "error", "event": event_type, "message": str(text)})
        return
    await _maybe_nudge_spark_flow(session, session_id)


# T6.3: how long a player can go without earning or spending a Spark before
# the MM gets a quiet prompt. A tool prompt, not a rule (MM5, Spark flow).
SPARK_FLOW_NUDGE_SECONDS = 25 * 60


async def _maybe_nudge_spark_flow(session, session_id: str) -> None:
    now = time.monotonic()
    for player_name in session.characters:
        flow = session.spark_flow.setdefault(player_name, {"last_flow": now, "last_nudge": None})
        if now - flow["last_flow"] < SPARK_FLOW_NUDGE_SECONDS:
            continue
        if flow["last_nudge"] is not None and now - flow["last_nudge"] < SPARK_FLOW_NUDGE_SECONDS:
            continue
        flow["last_nudge"] = now
        await manager.send_to_identity(session_id, "mm", {
            "type": "spark_flow_nudge", "player": player_name,
            "minutes_quiet": int((now - flow["last_flow"]) // 60),
            "message": (f"{player_name} hasn't earned or spent a Spark in a while. Every 6- is "
                        "a Graceful Fail waiting to happen, and unspent Sparks vanish at session end."),
        })


# ---------------------------------------------------------------------------
# Basics
# ---------------------------------------------------------------------------

@on("ping")
async def _ping(ctx: Ctx) -> None:
    await manager.send_to(ctx.websocket, {"type": "pong"})


@on("chat")
async def _chat(ctx: Ctx) -> None:
    text = _str(ctx.msg, "text", 2000)
    if not text:
        raise WSError("Say something first.")
    await manager.broadcast(ctx.session_id, {"type": "chat", "from": ctx.identity, "text": text})


# ---------------------------------------------------------------------------
# Rolls
# ---------------------------------------------------------------------------

@on("roll")
async def _roll(ctx: Ctx) -> None:
    """A general roll: 2d6 + stat (+knack) at a difficulty, with extra dice."""
    ch = _actor(ctx)
    extra = _extra_dice(ctx)
    result = roll_character(ctx.rs, ch, _stat(ctx), knack=_bool(ctx.msg, "knack"),
                            bonus=_int(ctx.msg, "bonus", 0, 0, 2), difficulty=_difficulty(ctx),
                            rng=RNG, description=_str(ctx.msg, "description"), **extra)
    rd = roll_result_to_dict(result)
    rd["helper"] = _str(ctx.msg, "helper", 64) or None
    if extra["sparks"]:
        ctx.session.record_spark_flow(ch.player_name)
    _record_roll(ctx.session, ch.player_name, rd)
    await manager.broadcast(ctx.session_id, {"type": "roll_result", "player": ch.player_name,
                                             "character": ch.name, "roll": rd})
    await _push_character(ctx, ch)


@on("avoid")
async def _avoid(ctx: Ctx) -> None:
    """The avoid roll: 2d6 + the stat that fits what is acting on you."""
    ch = _actor(ctx)
    extra = _extra_dice(ctx)
    if extra["sparks"] > ch.sparks:
        raise WSError(f"{ch.name} has only {ch.sparks} Spark(s).")
    stat = _stat(ctx)
    result = resolve_avoid(ctx.rs, stat_value=ch.stats.get(stat, 0), stat=stat,
                           difficulty=_difficulty(ctx), knack=_bool(ctx.msg, "knack"),
                           rng=RNG, description=_str(ctx.msg, "description"), **extra)
    if extra["sparks"]:
        ch.spend_spark(extra["sparks"])
        ctx.session.record_spark_flow(ch.player_name)
    rd = roll_result_to_dict(result)
    _record_roll(ctx.session, ch.player_name, rd)
    await manager.broadcast(ctx.session_id, {"type": "avoid_result", "player": ch.player_name,
                                             "character": ch.name, "roll": rd})
    await _push_character(ctx, ch)


# ---------------------------------------------------------------------------
# Combat — the exchange
# ---------------------------------------------------------------------------

def _combat_msg(session) -> dict:
    return {"type": "combat_state", "combat": session.combat.to_dict() if session.combat else None}


@on("start_combat", mm_only=True)
async def _start_combat(ctx: Ctx) -> None:
    if ctx.session.combat is not None:
        raise WSError("A fight is already running.")
    state = ctx.session.start_combat()
    await manager.broadcast(ctx.session_id, {"type": "combat_started", "combat": state.to_dict()})
    for ch in ctx.session.characters.values():
        await _push_character(ctx, ch)


@on("end_exchange", mm_only=True)
async def _end_exchange(ctx: Ctx) -> None:
    n = ctx.session.end_exchange()     # raises when no fight is running
    ctx.table.pending_attacks.clear()
    await manager.broadcast(ctx.session_id, {"type": "exchange_ended", "exchange": n,
                                             "combat": ctx.session.combat.to_dict()})
    for e in ctx.session.active_enemies.values():
        mm, pl = _enemy_msgs(ctx.session, e)
        await manager.broadcast_split(ctx.session_id, mm, pl)


@on("end_combat", mm_only=True)
async def _end_combat(ctx: Ctx) -> None:
    if ctx.session.combat is None:
        raise WSError("No fight is running.")
    ctx.session.end_combat()
    ctx.table.pending_attacks.clear()
    await manager.broadcast(ctx.session_id, {"type": "combat_ended"})


@on("telegraph", mm_only=True)
async def _telegraph(ctx: Ctx) -> None:
    """Step 1 of the exchange: the MM says what a foe is about to do, and to whom."""
    if ctx.session.combat is None:
        raise WSError("Start the fight first.")
    enemy = _enemy(ctx)
    text = _str(ctx.msg, "text", 300)
    if not text:
        raise WSError("Say what the foe is about to do.")
    ctx.session.combat.telegraphs[enemy.key or enemy.id] = text
    await manager.broadcast(ctx.session_id, {"type": "telegraph", "enemy": enemy.key or enemy.id,
                                             "name": enemy.name, "text": text,
                                             "combat": ctx.session.combat.to_dict()})


def _attack_kwargs(ctx: Ctx, ch) -> dict:
    opts = ctx.msg.get("options") or []
    if isinstance(opts, str):
        opts = [opts]
    if not isinstance(opts, list) or len(opts) > 2:
        raise WSError("options is a list of up to two picks.")
    kw = {"difficulty": _difficulty(ctx), "options": [str(o)[:20] for o in opts],
          "knack": _bool(ctx.msg, "knack"), "brawling": _bool(ctx.msg, "brawling"),
          "in_cover": _bool(ctx.msg, "in_cover"),
          "within_reach": ctx.msg.get("within_reach", True) is not False,
          **_extra_dice(ctx)}
    if kw["sparks"] > ch.sparks:
        raise WSError(f"{ch.name} has only {ch.sparks} Spark(s).")
    return kw


def _cover_ally(ctx: Ctx, attacker, options: list[str], ally_name: str) -> Optional[str]:
    if "cover" not in options:
        return None
    ally = ctx.session.characters.get(ally_name) or _by_character_name(ctx.session, ally_name)
    if ally is None or ally is attacker:
        raise WSError("Cover names an ally (not yourself).")
    return ally.name


async def _finish_attack(ctx: Ctx, ch, enemy, kw: dict, dice, damage_dice, cover_ally: str) -> None:
    """Resolve (apply) an attack with known dice and broadcast it."""
    res = combat.resolve_attack(ctx.rs, ch, enemy, state=ctx.session.combat, rng=RNG,
                                dice=dice, damage_dice=damage_dice or None, apply=True, **kw)
    cover_for = None
    if "cover" in res.options and ctx.session.combat is not None and cover_ally:
        ctx.session.combat.covered[cover_ally] = ch.name
        cover_for = cover_ally
    d = res.to_dict()
    d["cover_for"] = cover_for
    d["target_name"] = enemy.name if enemy is not None else None
    if kw["sparks"]:
        ctx.session.record_spark_flow(ch.player_name)
    _record_roll(ctx.session, ch.player_name, d["roll"])
    player_d = dict(d, enemy_result=_strip_enemy_hp(d["enemy_result"]))
    base = {"type": "attack_result", "player": ch.player_name, "character": ch.name,
            "combat": ctx.session.combat.to_dict() if ctx.session.combat else None}
    await manager.broadcast_split(ctx.session_id, {**base, "result": d}, {**base, "result": player_d})
    await _push_character(ctx, ch)
    if enemy is not None:
        await _push_enemy(ctx, enemy)


@on("attack")
async def _attack(ctx: Ctx) -> None:
    """A character attacks. On a 10+ with no option named in advance, the
    player picks it afterwards (`choose_option`); the engine then replays the
    same dice with the pick, so the choice never re-rolls the attack."""
    ch = _actor(ctx)
    if ch.player_name in ctx.table.pending_attacks:
        raise WSError("Pick your 10+ option first.")
    enemy = _enemy(ctx, "target", required=False)
    if enemy is not None and (enemy.defeated or enemy.broken):
        raise WSError(f"{enemy.name} is out of the fight.")
    kw = _attack_kwargs(ctx, ch)
    cover_ally = _cover_ally(ctx, ch, kw["options"], _str(ctx.msg, "cover_ally", 64))
    preview = combat.resolve_attack(ctx.rs, ch, enemy, state=ctx.session.combat, rng=RNG,
                                    apply=False, **kw)
    dice, dmg = preview.roll.dice, preview.damage_dice
    if preview.tier == "full_success" and not kw["options"]:
        ctx.table.pending_attacks[ch.player_name] = {
            "enemy": (enemy.key or enemy.id) if enemy is not None else None,
            "dice": dice, "damage_dice": dmg, "kwargs": kw}
        choices = [{"id": o, **ctx.rs.combat.options[o].model_dump()}
                   for o in ctx.rs.combat.attack.full_success.pick_one]
        await manager.broadcast(ctx.session_id, {
            "type": "attack_choose", "player": ch.player_name, "character": ch.name,
            "target_name": enemy.name if enemy is not None else None,
            "roll": roll_result_to_dict(preview.roll), "options_allowed": preview.options_allowed,
            "choices": choices})
        return
    await _finish_attack(ctx, ch, enemy, kw, dice, dmg, cover_ally)


@on("choose_option")
async def _choose_option(ctx: Ctx) -> None:
    """The 10+ pick for a pending attack: +1d6 damage, a stunt, or cover."""
    ch = _actor(ctx)
    pending = ctx.table.pending_attacks.get(ch.player_name)
    if pending is None:
        raise WSError("You have no 10+ attack waiting for an option.")
    opts = ctx.msg.get("options") or ctx.msg.get("option") or []
    if isinstance(opts, str):
        opts = [opts]
    if not isinstance(opts, list) or not opts:
        raise WSError("Pick an option.")
    kw = dict(pending["kwargs"], options=[str(o)[:20] for o in opts])
    enemy = ctx.session.active_enemies.get(pending["enemy"]) if pending["enemy"] else None
    if pending["enemy"] and (enemy is None or enemy.defeated):
        ctx.table.pending_attacks.pop(ch.player_name, None)
        raise WSError("That foe is gone.")
    cover_ally = _cover_ally(ctx, ch, kw["options"], _str(ctx.msg, "cover_ally", 64))
    await _finish_attack(ctx, ch, enemy, kw, pending["dice"], pending["damage_dice"], cover_ally)
    ctx.table.pending_attacks.pop(ch.player_name, None)


async def _drop_to_zero(ctx: Ctx, ch) -> dict:
    """At 0 HP: take a Wound (rolled on the wounds table); Hold On is the player's roll."""
    tid = ctx.rs.wounds.table
    name = toolbox.roll_table(ctx.rs, tid, rng=RNG)["text"] if ctx.rs.get_table(tid) else "Wound"
    wound = ch.add_wound(name)
    ctx.table.pending_hold_on.add(ch.player_name)
    return {"wound": wound, "items_to_drop": ch.items_to_drop(ctx.rs)}


@on("enemy_attack", mm_only=True)
async def _enemy_attack(ctx: Ctx) -> None:
    """A foe attacks in the open: the app rolls 2d6 + attack, reads exposure,
    Defend, cover, Warding and armor from the exchange, and applies damage."""
    enemy = _enemy(ctx)
    if enemy.defeated or enemy.broken:
        raise WSError(f"{enemy.name} is out of the fight.")
    target = _target_character(ctx, "target")
    if target.status == "dead":
        raise WSError(f"{target.name} is dead.")
    res = combat.resolve_enemy_attack(ctx.rs, enemy, target, state=ctx.session.combat,
                                      party=_party(ctx.session), rng=RNG, apply=True)
    d = res.to_dict()
    d["enemy_name"] = enemy.name
    hit_ch = _by_character_name(ctx.session, res.target) if res.target else None
    fall = None
    if hit_ch is not None and res.target_result and res.target_result.get("dropped"):
        fall = await _drop_to_zero(ctx, hit_ch)
    await manager.broadcast(ctx.session_id, {
        "type": "enemy_attack_result", "result": d, "fall": fall,
        "player": hit_ch.player_name if hit_ch else None,
        "combat": ctx.session.combat.to_dict() if ctx.session.combat else None})
    if hit_ch is not None:
        await _push_character(ctx, hit_ch)
    await _push_enemy(ctx, enemy)


@on("defend")
async def _defend(ctx: Ctx) -> None:
    """Defend (attacks on you are Hard), or Intercept for allies."""
    ch = _actor(ctx)
    if ctx.session.combat is None:
        raise WSError("Defend is a combat action; no fight is running.")
    raw = ctx.msg.get("intercept_for") or []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list) or len(raw) > 12:
        raise WSError("intercept_for is a list of allies.")
    allies = []
    for name in raw:
        name = str(name)[:64]
        if name == "*":
            allies.append("*")
            continue
        ally = ctx.session.characters.get(name) or _by_character_name(ctx.session, name)
        if ally is None:
            raise WSError(f"No ally {name!r}.")
        allies.append(ally.name)
    info = combat.declare_defend(ctx.rs, ctx.session.combat, ch, allies or None)
    await manager.broadcast(ctx.session_id, {"type": "defend_declared", "player": ch.player_name,
                                             **info, "combat": ctx.session.combat.to_dict()})


# ---------------------------------------------------------------------------
# Magic
# ---------------------------------------------------------------------------

def _cast_args(ctx: Ctx) -> dict:
    sig = ctx.msg.get("signature")
    return {"domain": _str(ctx.msg, "domain", 64), "scope": _str(ctx.msg, "scope", 20),
            "working": _str(ctx.msg, "working", 200) or None,
            "signature": None if sig is None else bool(sig),
            "reduce_fatigue": _bool(ctx.msg, "reduce_fatigue"), "miracle": _bool(ctx.msg, "miracle")}


@on("cast_preview")
async def _cast_preview(ctx: Ctx) -> None:
    """What a working will cost before it is cast (difficulty, Fatigue, why)."""
    ch = _actor(ctx)
    plan = magic.plan_cast(ctx.rs, ch, **_cast_args(ctx))
    await manager.send_to(ctx.websocket, {"type": "cast_plan", "plan": {**plan.__dict__, "ok": plan.ok}})


@on("cast")
async def _cast(ctx: Ctx) -> None:
    """Cast a working: the engine plans it, rolls it, pays Fatigue and resolves harm."""
    ch = _actor(ctx)
    args = _cast_args(ctx)
    enemy = _enemy(ctx, "target", required=False)
    group = []
    raw_targets = ctx.msg.get("targets") or []
    if not isinstance(raw_targets, list) or len(raw_targets) > 20:
        raise WSError("targets is a list of foes.")
    for k in raw_targets:
        e = ctx.session.active_enemies.get(str(k))
        if e is None:
            raise WSError(f"No foe {k!r} on the tracker.")
        group.append(e)
    extra = _extra_dice(ctx)
    res = magic.resolve_cast(ctx.rs, ch, intent=_str(ctx.msg, "intent", 300), knack=_bool(ctx.msg, "knack"),
                             enemy=enemy, enemies=group or None, rng=RNG, **args, **extra)
    d = res.to_dict()
    if extra["sparks"]:
        ctx.session.record_spark_flow(ch.player_name)
    _record_roll(ctx.session, ch.player_name, d["roll"])
    if res.complication_options:
        ctx.table.pending_complications[ch.player_name] = res.complication_options
    player_d = dict(d, enemy_result=_strip_enemy_hp(d["enemy_result"]),
                    enemy_results=[_strip_enemy_hp(r) for r in d["enemy_results"]])
    base = {"type": "cast_result", "player": ch.player_name, "character": ch.name}
    await manager.broadcast_split(ctx.session_id, {**base, "result": d}, {**base, "result": player_d})
    await _push_character(ctx, ch)
    for e in {id(x): x for x in ([enemy] if enemy else []) + group}.values():
        await _push_enemy(ctx, e)


@on("choose_complication")
async def _choose_complication(ctx: Ctx) -> None:
    """On a 7-9 working the player picks one of the two costs offered."""
    ch = _actor(ctx)
    options = ctx.table.pending_complications.get(ch.player_name)
    if not options:
        raise WSError("No casting cost is waiting for a choice.")
    idx = _int(ctx.msg, "index", 0, 0, len(options) - 1)
    chosen = ctx.table.pending_complications.pop(ch.player_name)[idx]
    await manager.broadcast(ctx.session_id, {"type": "complication_chosen", "player": ch.player_name,
                                             "character": ch.name, "complication": chosen})


# ---------------------------------------------------------------------------
# 0 HP, Hold On, recovery
# ---------------------------------------------------------------------------

@on("hold_on")
async def _hold_on(ctx: Ctx) -> None:
    """Roll Hold On (2d6 + Body) at 0 HP."""
    ch = _actor(ctx)
    if ch.player_name not in ctx.table.pending_hold_on and not (ch.hp_current == 0 and ch.status == "ok"):
        raise WSError(f"{ch.name} is not at 0 HP waiting to Hold On.")
    sparks = _int(ctx.msg, "sparks", 0, 0, 10)
    result = ch.hold_on(ctx.rs, rng=RNG, sparks=sparks)
    ctx.table.pending_hold_on.discard(ch.player_name)
    rd = roll_result_to_dict(result)
    _record_roll(ctx.session, ch.player_name, rd)
    await manager.broadcast(ctx.session_id, {"type": "hold_on_result", "player": ch.player_name,
                                             "character": ch.name, "roll": rd,
                                             "status": ch.status, "text": result.extra.get("text", "")})
    await _push_character(ctx, ch)


@on("tend")
async def _tend(ctx: Ctx) -> None:
    """An ally tends a dying character before the scene ends."""
    target = _target_character(ctx, "target")
    tender = ctx.session.characters.get(ctx.identity) if not ctx.is_mm else None
    if tender is target:
        raise WSError("You cannot tend yourself.")
    surgeon = bool(tender and tender.signature == "field_surgeon")
    status = target.tend(field_surgeon=surgeon)
    await manager.broadcast(ctx.session_id, {"type": "tended", "player": target.player_name,
                                             "by": ctx.identity, "status": status,
                                             "field_surgeon": surgeon})
    await _push_character(ctx, target)


@on("death_choice")
async def _death_choice(ctx: Ctx) -> None:
    """Untended at scene's end: live with a Scar, or a heroic final action."""
    ch = _actor(ctx)
    choice = _str(ctx.msg, "choice", 10)
    out = ch.death_choice(ctx.rs, choice, rng=RNG)
    await manager.broadcast(ctx.session_id, {"type": "death_choice_made", "player": ch.player_name,
                                             "character": ch.name, **out})
    await _push_character(ctx, ch)


@on("rest")
async def _rest(ctx: Ctx) -> None:
    """A breather (half HP) or a night's rest (full HP, Fatigue, a Wound).
    Players take a breather themselves; the MM calls either for anyone."""
    kind = _str(ctx.msg, "kind", 10)
    if kind not in ("breather", "night"):
        raise WSError("A rest is a breather or a night.")
    if ctx.is_mm:
        names = ctx.msg.get("players") or list(ctx.session.characters)
        if not isinstance(names, list):
            raise WSError("players is a list.")
        chars = []
        for n in names:
            c = ctx.session.characters.get(str(n))
            if c is None:
                raise WSError(f"No character for {n}.")
            chars.append(c)
    else:
        if kind == "night":
            raise WSError("The MM calls a night's rest.")
        chars = [_actor(ctx)]
    results = []
    for c in chars:
        if c.status in ("dead",):
            continue
        try:
            if kind == "breather":
                results.append({"player": c.player_name, "hp": c.breather(ctx.rs)})
            else:
                r = c.night_rest(ctx.rs, _int(ctx.msg, "wound_index", 0, 0, 20))
                results.append({"player": c.player_name, **r})
        except ValueError as e:
            results.append({"player": c.player_name, "error": str(e)})
    await manager.broadcast(ctx.session_id, {"type": "rest_result", "kind": kind, "results": results})
    for c in chars:
        await _push_character(ctx, c)
    if kind == "breather" and ctx.is_mm and _bool(ctx.msg, "in_danger"):
        res = toolbox.pressure_roll(ctx.rs, _str(ctx.msg, "variant", 20) or "generic", rng=RNG)
        await _private_result(ctx, "pressure", res, reveal=False)


@on("hp_adjust", mm_only=True)
async def _hp_adjust(ctx: Ctx) -> None:
    """The MM applies damage (a hazard, a filled clock) or healing to a character."""
    ch = _target_character(ctx)
    delta = _int(ctx.msg, "delta", 0, -200, 200)
    if delta == 0:
        raise WSError("Give a non-zero amount.")
    fall = None
    if delta < 0:
        r = ch.take_damage(ctx.rs, -delta)
        if r["dropped"]:
            fall = await _drop_to_zero(ctx, ch)
    else:
        ch.heal(ctx.rs, delta)
    await manager.broadcast(ctx.session_id, {"type": "hp_adjusted", "player": ch.player_name,
                                             "delta": delta, "hp": ch.hp_current, "fall": fall})
    await _push_character(ctx, ch)


@on("wound_add")
async def _wound_add(ctx: Ctx) -> None:
    ch = _actor(ctx)
    name = _str(ctx.msg, "name", 120)
    if not name:
        tid = ctx.rs.wounds.table
        name = toolbox.roll_table(ctx.rs, tid, rng=RNG)["text"] if ctx.rs.get_table(tid) else "Wound"
    wound = ch.add_wound(name)
    await manager.broadcast(ctx.session_id, {"type": "wound_added", "player": ch.player_name,
                                             "wound": wound, "items_to_drop": ch.items_to_drop(ctx.rs)})
    await _push_character(ctx, ch)


@on("wound_remove", mm_only=True)
async def _wound_remove(ctx: Ctx) -> None:
    ch = _actor(ctx)
    wound = ch.remove_wound(_int(ctx.msg, "index", 0, 0, 50))
    await manager.broadcast(ctx.session_id, {"type": "wound_removed", "player": ch.player_name,
                                             "wound": wound})
    await _push_character(ctx, ch)


@on("usage_roll")
async def _usage_roll(ctx: Ctx) -> None:
    """Roll an item's usage die after a scene of use."""
    ch = _actor(ctx)
    item = _str(ctx.msg, "item", 64)
    res = ch.usage_roll(ctx.rs, item, rng=RNG)
    await manager.broadcast(ctx.session_id, {"type": "usage_result", "player": ch.player_name,
                                             "character": ch.name, "result": res})
    await _push_character(ctx, ch)


@on("talent_use")
async def _talent_use(ctx: Ctx) -> None:
    """Tick a limited talent's use (once per scene / session / rest)."""
    ch = _actor(ctx)
    tid = _str(ctx.msg, "talent_id", 64)
    if not ch.has_talent(tid):
        raise WSError(f"{ch.name} does not have that talent.")
    left = ch.use_talent(ctx.rs, tid, period=_str(ctx.msg, "period", 10) or None)
    tdef = ctx.rs.get_talent(tid)
    await manager.broadcast(ctx.session_id, {"type": "talent_used", "player": ch.player_name,
                                             "character": ch.name, "talent_id": tid,
                                             "talent": tdef.name if tdef else tid, "uses_left": left})
    await _push_character(ctx, ch)



@on("character_sync")
async def _character_sync(ctx: Ctx) -> None:
    """Re-broadcast a character after a REST change (inventory, notes)."""
    await _push_character(ctx, _actor(ctx))


@on("scene_end", mm_only=True)
async def _scene_end(ctx: Ctx) -> None:
    """A new scene: once-per-scene uses refresh."""
    for c in ctx.session.characters.values():
        c.reset_uses(ctx.rs, "scene")
    await manager.broadcast(ctx.session_id, {"type": "scene_ended"})
    for c in ctx.session.characters.values():
        await _push_character(ctx, c)


# ---------------------------------------------------------------------------
# Sparks
# ---------------------------------------------------------------------------

@on("award_spark", mm_only=True)
async def _award_spark(ctx: Ctx) -> None:
    ch = _target_character(ctx)
    ch.earn_spark()
    ctx.session.record_spark_flow(ch.player_name)
    await manager.broadcast(ctx.session_id, {"type": "spark_earned", "player": ch.player_name,
                                             "reason": _str(ctx.msg, "reason", 200) or "MM award",
                                             "sparks_now": ch.sparks})
    await _push_character(ctx, ch)


@on("spend_spark")
async def _spend_spark(ctx: Ctx) -> None:
    """Spend a Spark outside a roll (a talent that costs one, a named moment)."""
    ch = _actor(ctx)
    ch.spend_spark(1)
    ctx.session.record_spark_flow(ch.player_name)
    await manager.broadcast(ctx.session_id, {"type": "spark_spent", "player": ch.player_name,
                                             "reason": _str(ctx.msg, "reason", 200),
                                             "sparks_now": ch.sparks})
    await _push_character(ctx, ch)


@on("peer_call")
async def _peer_call(ctx: Ctx) -> None:
    """"Spark?" — any player calls it for another player's moment; the MM confirms."""
    target = _target_character(ctx)
    if not ctx.is_mm and target.player_name == ctx.identity:
        raise WSError("Call it for someone else.")
    await manager.broadcast(ctx.session_id, {"type": "spark_nomination", "kind": "peer_call",
                                             "nominated_by": ctx.identity, "player": target.player_name,
                                             "message": f"{ctx.identity} calls \"Spark?\" for "
                                                        f"{target.player_name}. MM to confirm."})


@on("act_break", mm_only=True)
async def _act_break(ctx: Ctx) -> None:
    await manager.broadcast(ctx.session_id, {
        "type": "act_break_opened",
        "message": "Act break: nominate someone for something they did in the scene just past."})


@on("act_break_nominate")
async def _act_break_nominate(ctx: Ctx) -> None:
    target = _target_character(ctx)
    if not ctx.is_mm and target.player_name == ctx.identity:
        raise WSError("Nominate someone else.")
    await manager.broadcast(ctx.session_id, {"type": "spark_nomination", "kind": "act_break",
                                             "nominated_by": ctx.identity, "player": target.player_name,
                                             "reason": _str(ctx.msg, "reason", 200),
                                             "message": f"{ctx.identity} nominates {target.player_name} "
                                                        "at the act break. MM to confirm."})


@on("graceful_fail")
async def _graceful_fail(ctx: Ctx) -> None:
    """Claim the Graceful Fail on your last 6-: narrate it richer; the MM confirms."""
    ch = _actor(ctx)
    last = next((e for e in reversed(ctx.session.roll_log) if e.get("player_name") == ch.player_name), None)
    if not last or last.get("outcome") != "failure":
        raise WSError("Your last roll was not a 6-.")
    if last.get("graceful_fail_claimed"):
        raise WSError("That roll's Graceful Fail is already claimed.")
    last["graceful_fail_claimed"] = True
    last["graceful_fail_pending"] = True
    await manager.broadcast(ctx.session_id, {"type": "graceful_fail_claimed", "player": ch.player_name,
                                             "narration": _str(ctx.msg, "narration", 500),
                                             "message": f"{ch.name} claims a Graceful Fail. MM to confirm."})


@on("graceful_fail_confirm", mm_only=True)
async def _graceful_fail_confirm(ctx: Ctx) -> None:
    ch = _target_character(ctx)
    last = next((e for e in reversed(ctx.session.roll_log)
                 if e.get("player_name") == ch.player_name and e.get("graceful_fail_pending")), None)
    if last is None:
        raise WSError(f"{ch.name} has no Graceful Fail waiting.")
    last["graceful_fail_pending"] = False
    ch.earn_spark()
    ctx.session.record_spark_flow(ch.player_name)
    await manager.broadcast(ctx.session_id, {"type": "spark_earned", "player": ch.player_name,
                                             "reason": "Graceful Fail", "sparks_now": ch.sparks})
    await _push_character(ctx, ch)


# ---------------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------------

@on("session_end", mm_only=True)
async def _session_end(ctx: Ctx) -> None:
    """The five prompts and the pacing hint, for the MM's level-up call."""
    prompts = ctx.session.end_session_prompts()
    prompts["characters"] = [{"player": c.player_name, "name": c.name, "level": c.level,
                              "ready": c.player_name in ctx.session.level_up_ready}
                             for c in ctx.session.characters.values()]
    await manager.send_to_identity(ctx.session_id, "mm", {"type": "session_end_prompts", **prompts})


@on("level_up", mm_only=True)
async def _level_up(ctx: Ctx) -> None:
    """The MM grants a level (to everyone, or to the players named)."""
    names = ctx.msg.get("players")
    if names is not None and (not isinstance(names, list) or len(names) > 20):
        raise WSError("players is a list.")
    ready = ctx.session.call_level_up([str(n) for n in names] if names is not None else None)
    await manager.broadcast(ctx.session_id, {"type": "level_up_ready", "players": ready})
    for n in ready:
        await _push_character(ctx, ctx.session.characters[n])


@on("level_pick")
async def _level_pick(ctx: Ctx) -> None:
    """The player's pick for a granted level: a talent, an improved form, or
    the signature (plus the stat at levels 4/8 and a working at 5/9)."""
    ch = _actor(ctx)
    if ch.player_name not in ctx.session.level_up_ready:
        raise WSError("The MM has not called a level-up for you.")
    hp = _str(ctx.msg, "hp", 10) or "average"
    hp_roll = None
    if hp == "roll":
        hp_roll = RNG.randint(1, ch.facet_def(ctx.rs).grit_die)
    elif hp != "average":
        raise WSError("HP is 'roll' or 'average'.")
    extras = ctx.msg.get("extra_talents")
    if extras is not None and (not isinstance(extras, list) or len(extras) > 2):
        raise WSError("extra_talents is a list of two.")
    old_level = ch.level
    errors = ch.level_up(ctx.rs, kind=_str(ctx.msg, "kind", 12), talent_id=_str(ctx.msg, "talent_id", 64),
                         choice=_str(ctx.msg, "choice", 64) or None, teacher=_bool(ctx.msg, "teacher"),
                         stat=_str(ctx.msg, "stat", 10) or None,
                         signature_working=_str(ctx.msg, "signature_working", 200) or None,
                         hp_roll=hp_roll, extra_talents=[str(e) for e in extras] if extras else None)
    if errors:
        await manager.send_to(ctx.websocket, {"type": "level_pick_error", "errors": errors})
        return
    ctx.session.level_up_ready.discard(ch.player_name)
    await manager.broadcast(ctx.session_id, {"type": "level_up_done", "player": ch.player_name,
                                             "character": ch.name, "from": old_level, "level": ch.level,
                                             "hp_roll": hp_roll})
    await _push_character(ctx, ch)


@on("respec")
async def _respec(ctx: Ctx) -> None:
    """Rebuild talents for free before the signature level."""
    ch = _actor(ctx)
    talents = ctx.msg.get("talents")
    if not isinstance(talents, list) or len(talents) > 12:
        raise WSError("talents is a list.")
    errors = ch.respec(ctx.rs, talents=[t for t in talents if isinstance(t, dict)],
                       magic=ctx.msg.get("magic") if isinstance(ctx.msg.get("magic"), dict) else None)
    if errors:
        raise WSError("; ".join(errors))
    await _push_character(ctx, ch)


@on("next_session", mm_only=True)
async def _next_session(ctx: Ctx) -> None:
    """Start the next session: Sparks back to 3, session uses refresh."""
    n = ctx.session.next_session()
    await manager.broadcast(ctx.session_id, {"type": "session_started", "session_number": n})
    await _push_state(ctx.session_id)


# ---------------------------------------------------------------------------
# The tracker: foes
# ---------------------------------------------------------------------------

def _seed_bestiary(session, table: TableState) -> list[str]:
    """Load the Bestiary's cards into the library (once per session)."""
    if table.bestiary_seeded:
        return []
    table.bestiary_seeded = True
    return _load_bestiary(session)


def _load_bestiary(session) -> list[str]:
    loaded = []
    if not BESTIARY_DIR.is_dir():
        return loaded
    for path in sorted(BESTIARY_DIR.glob("*.fof")):
        try:
            enemy = Enemy.from_fof(yaml.safe_load(path.read_text(encoding="utf-8")))
        except (EnemyFormatError, yaml.YAMLError, KeyError, TypeError, ValueError) as e:
            logger.warning("Bestiary card %s skipped: %s", path.name, e)
            continue
        if enemy.id not in session.enemy_library and not enemy.validate(session.ruleset):
            session.enemy_library[enemy.id] = enemy
            loaded.append(enemy.id)
    return loaded


@on("bestiary_load", mm_only=True)
async def _bestiary_load(ctx: Ctx) -> None:
    loaded = _load_bestiary(ctx.session)
    ctx.table.bestiary_seeded = True
    rs = ctx.rs
    await manager.send_to_identity(ctx.session_id, "mm", {
        "type": "enemy_library", "loaded": loaded,
        "library": {eid: e.to_client_dict(rs) for eid, e in ctx.session.enemy_library.items()}})


@on("enemy_spawn", mm_only=True)
async def _enemy_spawn(ctx: Ctx) -> None:
    """Put a card from the library on the tracker (a Mook mob with `count`)."""
    eid = _str(ctx.msg, "enemy_id", 64)
    card = ctx.session.enemy_library.get(eid)
    if card is None:
        raise WSError(f"No card {eid!r} in the library.")
    count = _int(ctx.msg, "count", 1, 1, 30)
    if len(ctx.session.active_enemies) >= 40:
        raise WSError("The tracker is full.")
    base = _str(ctx.msg, "key", 64) or eid
    key, n = base, 1
    while key in ctx.session.active_enemies:
        n += 1
        key = f"{base}-{n}"
    live = card.spawn(ctx.rs, count=count, key=key)
    name = _str(ctx.msg, "name", 128)
    if name:
        live.name = name
    elif n > 1:
        live.name = f"{card.name} {n}"
    ctx.session.active_enemies[key] = live
    await _push_enemy(ctx, live, "enemy_spawned")


@on("enemy_update", mm_only=True)
async def _enemy_update(ctx: Ctx) -> None:
    """Damage (through the engine), healing, or a manual correction."""
    enemy = _enemy(ctx, "key")
    rs = ctx.rs
    report = None
    if "damage" in ctx.msg:
        report = combat.apply_damage_to_enemy(rs, enemy, _int(ctx.msg, "damage", 0, 0, 500)).to_dict()
    if "heal" in ctx.msg and not enemy.is_mook:
        mx = enemy.hp_max(rs)
        enemy.hp_current = min(mx, (enemy.hp_current or 0) + _int(ctx.msg, "heal", 0, 0, 500))
        if enemy.hp_current > 0:
            enemy.defeated = False
    if "hp_current" in ctx.msg and not enemy.is_mook:
        enemy.hp_current = _int(ctx.msg, "hp_current", 0, 0, enemy.hp_max(rs))
        enemy.defeated = enemy.hp_current == 0
    if "count" in ctx.msg and enemy.is_mook:
        enemy.count = _int(ctx.msg, "count", 1, 0, 30)
        enemy.defeated = enemy.count == 0
    for flag in ("bloodied", "broken", "defeated"):
        if flag in ctx.msg:
            setattr(enemy, flag, _bool(ctx.msg, flag))
    if "name" in ctx.msg and _str(ctx.msg, "name", 128):
        enemy.name = _str(ctx.msg, "name", 128)
    if report is not None:
        await manager.send_to_identity(ctx.session_id, "mm", {"type": "enemy_damage", "result": report,
                                                             "name": enemy.name})
    await _push_enemy(ctx, enemy)


@on("enemy_remove", mm_only=True)
async def _enemy_remove(ctx: Ctx) -> None:
    enemy = _enemy(ctx, "key")
    del ctx.session.active_enemies[enemy.key or enemy.id]
    await manager.broadcast(ctx.session_id, {"type": "enemy_removed", "key": enemy.key or enemy.id})
    await _push_danger(ctx)


@on("morale_check", mm_only=True)
async def _morale_check(ctx: Ctx) -> None:
    """2d6 over the foe's morale and it breaks (flees, surrenders, parleys)."""
    enemy = _enemy(ctx)
    res = combat.morale_check(ctx.rs, enemy, bonus=_int(ctx.msg, "bonus", 0, 0, 4), rng=RNG)
    await manager.broadcast(ctx.session_id, {"type": "morale_result", "name": enemy.name,
                                             "result": res.to_dict()})
    await _push_enemy(ctx, enemy)


# ---------------------------------------------------------------------------
# Toolbox (MM6) — private to the MM unless revealed
# ---------------------------------------------------------------------------

async def _private_result(ctx: Ctx, kind: str, result: Any, reveal: bool) -> None:
    msg = {"type": "toolbox_result", "kind": kind, "result": result, "revealed": reveal}
    if reveal:
        await manager.broadcast(ctx.session_id, msg)
        return
    rid = uuid.uuid4().hex[:12]
    store = ctx.table.private_results
    store[rid] = {"kind": kind, "result": result}
    while len(store) > PRIVATE_RESULTS_KEPT:
        store.popitem(last=False)
    await manager.send_to_identity(ctx.session_id, "mm", {**msg, "result_id": rid})


@on("toolbox_roll", mm_only=True)
async def _toolbox_roll(ctx: Ctx) -> None:
    res = toolbox.roll_table(ctx.rs, _str(ctx.msg, "table", 64), rng=RNG)
    await _private_result(ctx, "table", res, _bool(ctx.msg, "reveal"))


@on("toolbox_reveal", mm_only=True)
async def _toolbox_reveal(ctx: Ctx) -> None:
    entry = ctx.table.private_results.pop(_str(ctx.msg, "result_id", 32), None)
    if entry is None:
        raise WSError("That result is no longer available to reveal.")
    await manager.broadcast(ctx.session_id, {"type": "toolbox_result", "kind": entry["kind"],
                                             "result": entry["result"], "revealed": True})


@on("reaction_roll", mm_only=True)
async def _reaction_roll(ctx: Ctx) -> None:
    res = toolbox.reaction_roll(ctx.rs, modifier=_int(ctx.msg, "modifier", 0, -3, 3), rng=RNG)
    await _private_result(ctx, "reaction", res, _bool(ctx.msg, "reveal"))


@on("pressure_roll", mm_only=True)
async def _pressure_roll(ctx: Ctx) -> None:
    res = toolbox.pressure_roll(ctx.rs, _str(ctx.msg, "variant", 20) or "generic", rng=RNG)
    await _private_result(ctx, "pressure", res, _bool(ctx.msg, "reveal"))


@on("oracle", mm_only=True)
async def _oracle(ctx: Ctx) -> None:
    res = toolbox.oracle(ctx.rs, _str(ctx.msg, "odds", 20) or "even", rng=RNG)
    res["question"] = _str(ctx.msg, "question", 300)
    await _private_result(ctx, "oracle", res, _bool(ctx.msg, "reveal"))


@on("stuck", mm_only=True)
async def _stuck(ctx: Ctx) -> None:
    """"Stuck?" — three ways forward: a threat moves, someone arrives, a secret surfaces."""
    clock = None
    cid = _str(ctx.msg, "clock_id", 64)
    if cid and cid in ctx.session.threat_clocks:
        clock = ctx.session.threat_clocks[cid].name
    elif ctx.session.threat_clocks:
        clock = next(iter(ctx.session.threat_clocks.values())).name
    res = toolbox.stuck_helper(ctx.rs, rng=RNG, clock=clock)
    await _private_result(ctx, "stuck", res, False)


@on("hoard", mm_only=True)
async def _hoard(ctx: Ctx) -> None:
    res = toolbox.roll_hoard(ctx.rs, _int(ctx.msg, "site_level", 1, 1, 10), rng=RNG)
    await _private_result(ctx, "hoard", res, _bool(ctx.msg, "reveal"))


@on("npc", mm_only=True)
async def _npc(ctx: Ctx) -> None:
    """An NPC on the spot: a name, a trait, a want and a secret."""
    card = {}
    for key, tid in (("name", "npc_names"), ("trait", "npc_traits"), ("want", "npc_wants"),
                     ("secret", "npc_secrets")):
        card[key] = toolbox.roll_table(ctx.rs, tid, rng=RNG)["text"] if ctx.rs.get_table(tid) else None
    await _private_result(ctx, "npc", card, _bool(ctx.msg, "reveal"))


# ---------------------------------------------------------------------------
# Threat clocks (PHB III.2)
# ---------------------------------------------------------------------------

def _clock(ctx: Ctx) -> ThreatClock:
    cid = _str(ctx.msg, "clock_id", 64)
    clock = ctx.session.threat_clocks.get(cid)
    if clock is None:
        raise WSError(f"No Threat Clock {cid!r}.")
    return clock


@on("threat_clock_create", mm_only=True)
async def _clock_create(ctx: Ctx) -> None:
    name = _str(ctx.msg, "name", 128) or "Threat"
    segments = _int(ctx.msg, "segments", ctx.rs.hazards.threat_clock.segments, 2, 12)
    if len(ctx.session.threat_clocks) >= 20:
        raise WSError("Twenty clocks is plenty.")
    clock = ThreatClock(id=uuid.uuid4().hex[:10], name=name, segments=segments)
    ctx.session.threat_clocks[clock.id] = clock
    await manager.broadcast(ctx.session_id, {"type": "clock_updated", "clock": clock.to_client_dict()})


@on("threat_clock_advance", mm_only=True)
async def _clock_advance(ctx: Ctx) -> None:
    """Tick a clock. With `outcome_tier`, only a tier that advances clocks ticks it."""
    clock = _clock(ctx)
    tier = _str(ctx.msg, "outcome_tier", 20)
    filled = False
    if not tier or tier in ctx.rs.hazards.threat_clock.advances_on:
        filled = clock.advance()
    await manager.broadcast(ctx.session_id, {"type": "clock_updated", "clock": clock.to_client_dict(),
                                             "filled": filled})


@on("threat_clock_wind_back", mm_only=True)
async def _clock_wind_back(ctx: Ctx) -> None:
    clock = _clock(ctx)
    clock.wind_back()
    await manager.broadcast(ctx.session_id, {"type": "clock_updated", "clock": clock.to_client_dict()})


@on("threat_clock_delete", mm_only=True)
async def _clock_delete(ctx: Ctx) -> None:
    clock = _clock(ctx)
    del ctx.session.threat_clocks[clock.id]
    await manager.broadcast(ctx.session_id, {"type": "clock_deleted", "clock_id": clock.id})
