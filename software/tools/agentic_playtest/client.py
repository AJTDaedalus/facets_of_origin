"""Real clients against a running server.

Each agent gets its own account: a player redeems a single-use invite link and
receives its own JWT, exactly as a human would. The server then enforces
permissions for us — a player agent that tries to award itself a Spark or land
an enemy attack gets `Unknown event type` back from the API, not a polite refusal
from a Python wrapper we wrote.

**The event log is built from the MM's socket alone.** Every mechanical fact is
broadcast to the whole session, so one privileged observer sees each fact exactly
once. Summing what the player sockets saw is what produced batch 07's 4x
over-count: `roll_result` is a broadcast, so four sockets each reported the same
roll. Player sockets here are used for *sending* and are drained but never
recorded.
"""
from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from queue import Empty, Queue
from typing import Any

from websockets.sync.client import connect as ws_connect

from tools.agentic_playtest.events import EventLog

#: The server has one chat channel and no concept of narration, table talk, or a
#: rules gap. These tags carry that distinction over it, so the observer socket
#: stays the single writer of the speech log — a verb that also appended locally
#: would log one utterance twice, which is the batch-07 over-count in miniature.
OOC_TAG = "(ooc) "
SCENE_TAG = "[scene] "
RULING_TAG = "[MM ruling] "


class ServerError(RuntimeError):
    """The API refused a request."""


class TableRuling(RuntimeError):
    """The rules refused an action.

    The agent asked for something the rules do not allow — Strike from Withdrawn,
    Intercept twice in an exchange, spend a Skill Point on a skill it never used.
    Returned to the agent as a tool result so it can choose again, and logged: a
    high rate of these says the rules are not legible from the text the agent was
    given, which is a finding in itself.
    """


def _api(base_url: str, method: str, path: str, token: str = "", body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(base_url + path, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=15) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace") if e.fp else str(e)
        raise ServerError(f"{method} {path} -> {e.code}: {detail}") from e


@dataclass
class Connection:
    """One authenticated WebSocket, with a background reader."""

    identity: str
    token: str
    socket: Any
    inbox: "Queue[dict]" = field(default_factory=Queue)
    _reader: threading.Thread | None = None
    _closed: threading.Event = field(default_factory=threading.Event)

    def start(self) -> None:
        def pump() -> None:
            while not self._closed.is_set():
                try:
                    raw = self.socket.recv(timeout=0.5)
                except TimeoutError:
                    continue
                except Exception:
                    return
                try:
                    self.inbox.put(json.loads(raw))
                except json.JSONDecodeError:
                    continue

        self._reader = threading.Thread(target=pump, daemon=True)
        self._reader.start()

    def send(self, payload: dict) -> None:
        self.socket.send(json.dumps(payload))

    def drain(self) -> list[dict]:
        out = []
        while True:
            try:
                out.append(self.inbox.get_nowait())
            except Empty:
                return out

    def close(self) -> None:
        self._closed.set()
        try:
            self.socket.close()
        except Exception:
            pass


def login_mm(base_url: str, password: str) -> str:
    """Configure the MM password if this is a fresh server, then log in.

    Call once per process and reuse the token — `/auth/mm-login` is rate limited
    to a handful of attempts per minute.
    """
    base_url = base_url.rstrip("/")
    try:
        _api(base_url, "POST", "/api/sessions/auth/setup", body={"password": password})
    except ServerError:
        pass  # already configured — the usual case on a warm server
    return _api(base_url, "POST", "/api/sessions/auth/mm-login",
                body={"password": password})["access_token"]


class LiveTable:
    """A session on a running server, with one connection per participant.

    The MM connection is the observer of record. `await_broadcast` waits for a
    specific broadcast type on it, which is how every verb below turns an
    asynchronous event stream into a synchronous tool result the agent can act on.
    """

    #: Broadcast types that carry a mechanical fact and belong in the event log.
    MECHANICAL = {
        "roll_result", "saving_throw_result", "cast_result", "strike_result",
        "react_result", "support_result", "maneuver_result", "contested_roll_result",
        "condition_applied", "condition_cleared", "combat_started", "combat_ended",
        "exchange_ended", "posture_declared", "postures_revealed",
        "enemy_spawned", "enemy_updated", "enemy_removed", "enemy_phase_change",
        "spark_earned", "skill_advanced", "skill_point_spent", "skill_marked_used",
        "technique_selected", "clock_created", "clock_advanced", "clock_fill",
        "clock_wound_back", "clock_deleted", "character_created", "character_removed",
        "table_roll_result", "act_break_opened", "graceful_fail_claimed",
        "session_reset", "spark_nomination",
    }

    def __init__(self, base_url: str, mm_password: str | None, session_name: str,
                 arm: str = "A", seed: int | None = None,
                 active_facet_ids: list[str] | None = None,
                 mm_token: str | None = None) -> None:
        """Open a session on a running server.

        Pass `mm_token` to reuse a token from an earlier login. `/auth/mm-login`
        is rate limited (correctly — it is a password endpoint), so a harness
        that logs in per session trips the limiter after five. Log in once, keep
        the token, pass it here.
        """
        self.base_url = base_url.rstrip("/")
        self.ws_url = self.base_url.replace("http://", "ws://").replace("https://", "wss://") + "/ws"

        if mm_token is None:
            self.mm_token = login_mm(self.base_url, mm_password or "")
        else:
            self.mm_token = mm_token
        self.session_id = _api(self.base_url, "POST", "/api/sessions/", self.mm_token,
                               {"name": session_name,
                                "active_facet_ids": active_facet_ids or []})["session_id"]

        self.log = EventLog(self.session_id, arm=arm, seed=seed)
        self.connections: dict[str, Connection] = {}
        self.mm = self._connect("MM", self.mm_token)
        self._rulings: list[str] = []

    # ------------------------------------------------------------------
    # Joining
    # ------------------------------------------------------------------

    def _connect(self, identity: str, token: str) -> Connection:
        socket = ws_connect(self.ws_url, open_timeout=10)
        socket.send(json.dumps({"token": token, "session_id": self.session_id}))
        connection = Connection(identity=identity, token=token, socket=socket)
        connection.start()
        self.connections[identity] = connection
        time.sleep(0.15)  # let the state + player_joined frames land
        connection.drain()
        return connection

    def invite_player(self, player_name: str) -> str:
        """Generate a real single-use invite link, as the MM would."""
        return _api(self.base_url, "POST", "/api/sessions/invite", self.mm_token,
                    {"session_id": self.session_id, "player_name": player_name})["invite_url"]

    def join_as_player(self, player_name: str) -> Connection:
        """Redeem an invite and connect on the resulting player token.

        The player never sees the MM token — its permissions are whatever the
        server grants a player, which is the point of doing it this way.
        """
        invite_url = self.invite_player(player_name)
        invite_token = invite_url.split("token=")[-1]
        token = _api(self.base_url, "POST", "/api/sessions/join",
                     body={"invite_token": invite_token})["access_token"]
        return self._connect(player_name, token)

    def create_character(self, player_name: str, character_name: str, primary_facet: str,
                         attributes: dict[str, int], background_id: str | None = None,
                         magic_domain: str | None = None) -> dict:
        connection = self.connections[player_name]
        character = _api(self.base_url, "POST", "/api/characters/", connection.token, {
            "session_id": self.session_id,
            "character_name": character_name,
            "primary_facet": primary_facet,
            "attributes": attributes,
            "background_id": background_id,
            "magic_domain": magic_domain,
        })["character"]
        self.await_broadcast("character_created", timeout=5)
        return character

    def add_enemy(self, enemy: dict) -> dict:
        return _api(self.base_url, "POST", "/api/enemies/", self.mm_token,
                    {"session_id": self.session_id, **enemy})["enemy"]

    def state(self) -> dict:
        """Current session state as the MM sees it."""
        return _api(self.base_url, "GET", f"/api/characters/{self.session_id}", self.mm_token)

    # ------------------------------------------------------------------
    # The observer loop
    # ------------------------------------------------------------------

    def _record(self, message: dict) -> None:
        kind = message.get("type")
        if kind in ("state", "pong", "player_joined", "player_left", "chat"):
            if kind == "chat":
                self._record_chat(message)
            return
        if kind == "error":
            self._rulings.append(message.get("message", ""))
            return
        if kind in self.MECHANICAL:
            actor = (message.get("player") or message.get("attacker")
                     or message.get("player_a") or message.get("rolled_by") or "MM")
            data = {k: v for k, v in message.items() if k != "type"}
            self.log.append(kind, actor, **data)

    def _record_chat(self, message: dict) -> None:
        """One chat message becomes exactly one speech event, of one kind."""
        # The server identifies the MM socket as "mm"; the rest of the harness
        # calls it "MM". Normalise here so metrics keyed on actor don't split
        # the MM's speech from the MM's mechanical events.
        speaker = message.get("from", "?")
        speaker = "MM" if speaker == "mm" else speaker
        text = str(message.get("text", ""))
        if text.startswith(RULING_TAG):
            return  # already logged as a structured `rules_gap`
        if text.startswith(OOC_TAG):
            self.log.append("say_ooc", speaker, text=text[len(OOC_TAG):])
        elif text.startswith(SCENE_TAG):
            self.log.append("scene", speaker, text=text[len(SCENE_TAG):])
        else:
            self.log.append("say", speaker, text=text)

    def pump(self) -> list[dict]:
        """Record everything the MM socket has seen since the last pump."""
        messages = self.mm.drain()
        for message in messages:
            self._record(message)
        # Player sockets are drained so their queues don't grow without bound.
        # They are deliberately NOT recorded — see the module docstring.
        for identity, connection in self.connections.items():
            if identity != "MM":
                connection.drain()
        return messages

    def await_broadcast(self, *kinds: str, timeout: float = 10.0,
                        actor: str | None = None,
                        also_watch: "Connection | None" = None) -> dict:
        """Block until one of `kinds` arrives on the MM socket, or an error does.

        `actor` filters to a specific player's result, which matters when two
        players act in the same beat — the aliasing trap from batch 07 in a
        different guise. Pass `actor=None` to accept any.

        `also_watch` is the acting player's own connection. Refusals are sent
        with `send_to`, not broadcast, so a player agent calling an MM verb
        produces an error only on its own socket — without watching it, that
        call would block until timeout instead of raising.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if also_watch is not None and also_watch is not self.mm:
                for message in also_watch.drain():
                    if message.get("type") == "error":
                        self._rulings.append(message.get("message", ""))
                        raise TableRuling(message.get("message", "refused"))
            try:
                message = self.mm.inbox.get(timeout=0.2)
            except Empty:
                continue
            self._record(message)
            if message.get("type") == "error":
                raise TableRuling(message.get("message", "refused"))
            if message.get("type") in kinds:
                if actor is None:
                    return message
                who = (message.get("player") or message.get("attacker")
                       or message.get("target") or message.get("rolled_by")
                       or message.get("from"))
                if who == "mm":
                    who = "MM"
                if who == actor:
                    return message
        raise TimeoutError(f"No {kinds} broadcast within {timeout}s")

    def close(self) -> None:
        for connection in self.connections.values():
            connection.close()
