"""WebSocket layer (DESIGN §4.2): auth, permissions, and every event handler.

Each handler gets a happy path, an edge case, and a refusal. Dice are scripted
through `app.api.websocket.RNG` so outcomes are exact; the handlers call the
engine, so these tests check wiring and broadcasts, not rule arithmetic
(that lives in test_combat / test_magic / test_character / test_toolbox).
"""
from __future__ import annotations

import random
from contextlib import ExitStack
from unittest.mock import AsyncMock

import pytest

from app.api import websocket as wsmod
from app.api.websocket import ConnectionManager, HANDLERS
from app.auth.tokens import create_invite_token, create_mm_token, create_session_token
from app.game.session import session_store
from tests.conftest import make_caster, make_character, make_enemy


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------

class ScriptedRNG(random.Random):
    """randint() returns queued values first (clamped to the range asked), then random ones."""

    def __init__(self):
        super().__init__(7)
        self.queue: list[int] = []

    def push(self, *values: int) -> "ScriptedRNG":
        self.queue.extend(values)
        return self

    def randint(self, a, b):
        if self.queue:
            return max(a, min(b, self.queue.pop(0)))
        return super().randint(a, b)


@pytest.fixture
def dice(monkeypatch) -> ScriptedRNG:
    rng = ScriptedRNG()
    monkeypatch.setattr(wsmod, "RNG", rng)
    return rng


def call(ws, msg: dict | None = None) -> list[dict]:
    """Send `msg`, then a ping; return everything received before the pong."""
    if msg is not None:
        ws.send_json(msg)
    ws.send_json({"type": "ping"})
    out = []
    for _ in range(500):
        m = ws.receive_json()
        if m["type"] == "pong":
            return out
        out.append(m)
    raise AssertionError("no pong")


def first(msgs: list[dict], kind: str) -> dict:
    found = [m for m in msgs if m["type"] == kind]
    assert found, f"no {kind!r} in {[m['type'] for m in msgs]}"
    return found[0]


def kinds(msgs: list[dict]) -> list[str]:
    return [m["type"] for m in msgs]


def error_text(msgs: list[dict]) -> str:
    return first(msgs, "error")["message"]


class Table:
    """A session with Mordai (Player1, Warrior) and Zahna (Thaumaturge), an MM
    socket and a socket per player."""

    def __init__(self, client, ruleset):
        self.client = client
        self.rs = ruleset
        mm_token = create_mm_token()
        resp = client.post("/api/sessions/", json={"name": "WS Table"},
                           headers={"Authorization": f"Bearer {mm_token}"})
        self.sid = resp.json()["session_id"]
        self.session = session_store.get(self.sid)
        self.mordai = make_character(self.session.ruleset)
        self.zahna = make_caster(self.session.ruleset)
        self.session.add_character(self.mordai)
        self.session.add_character(self.zahna)
        self.mm_token = mm_token
        self._stack = ExitStack()
        self.mm = self._connect({"token": mm_token, "session_id": self.sid})
        self.p1 = self._connect({"token": create_session_token("Player1", self.sid)})
        self.z = self._connect({"token": create_session_token("Zahna", self.sid)})
        for w in (self.mm, self.p1, self.z):
            call(w)   # drain joins

    def _connect(self, auth: dict):
        w = self._stack.enter_context(self.client.websocket_connect("/ws"))
        w.send_json(auth)
        assert w.receive_json()["type"] == "state"
        return w

    def close(self):
        self._stack.close()

    def add_card(self, **kw):
        """A card with its numbers pinned (overrides), so ruleset tuning cannot move them."""
        role = kw.get("role", "standard")
        if role != "mook":
            kw.setdefault("hp_override", 8 * {"standard": 1, "elite": 2, "boss": 4}[role])
        kw.setdefault("damage_override", 3)
        kw.setdefault("attack_override", 1)
        e = make_enemy(**kw)
        self.session.enemy_library[e.id] = e
        return e

    def spawn(self, count=1, **kw) -> str:
        card = self.add_card(**kw)
        msgs = call(self.mm, {"type": "enemy_spawn", "enemy_id": card.id, "count": count})
        return first(msgs, "enemy_spawned")["enemy"]["key"]

    def foe(self, key):
        return self.session.active_enemies[key]


@pytest.fixture
def t(client, ruleset):
    table = Table(client, ruleset)
    yield table
    table.close()


MM_ONLY = sorted(e for e, (_, mm) in HANDLERS.items() if mm)


# ---------------------------------------------------------------------------
# ConnectionManager
# ---------------------------------------------------------------------------

class TestConnectionManager:
    async def test_connect_and_broadcast(self):
        m = ConnectionManager()
        a, b = AsyncMock(), AsyncMock()
        await m.connect(a, "s", "P1")
        await m.connect(b, "s", "mm")
        await m.broadcast("s", {"type": "x"})
        a.send_json.assert_called_once_with({"type": "x"})
        b.send_json.assert_called_once_with({"type": "x"})

    async def test_broadcast_split_gives_mm_its_own_view(self):
        m = ConnectionManager()
        p, mm = AsyncMock(), AsyncMock()
        await m.connect(p, "s", "P1")
        await m.connect(mm, "s", "mm")
        await m.broadcast_split("s", {"v": "mm"}, {"v": "player"})
        p.send_json.assert_called_once_with({"v": "player"})
        mm.send_json.assert_called_once_with({"v": "mm"})

    async def test_dead_connections_are_dropped(self):
        m = ConnectionManager()
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("gone")
        await m.connect(ws, "s", "P1")
        await m.broadcast("s", {"type": "x"})
        await m.broadcast_split("s", {}, {})
        assert m._connections["s"] == []

    async def test_send_to_identity_only_reaches_that_identity(self):
        m = ConnectionManager()
        p, mm = AsyncMock(), AsyncMock()
        await m.connect(p, "s", "P1")
        await m.connect(mm, "s", "mm")
        await m.send_to_identity("s", "mm", {"type": "secret"})
        p.send_json.assert_not_called()
        mm.send_json.assert_called_once()

    async def test_send_to_swallows_failure(self):
        m = ConnectionManager()
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("gone")
        assert await m.send_to(ws, {"type": "x"}) is False


# ---------------------------------------------------------------------------
# Auth and dispatch
# ---------------------------------------------------------------------------

class TestAuth:
    def test_mm_state_has_library_and_role(self, client, active_session):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": create_mm_token(), "session_id": active_session["session_id"]})
            state = ws.receive_json()
            assert state["type"] == "state"
            assert state["data"]["role"] == "mm"
            assert "enemy_library" in state["data"]
            # The Bestiary is seeded into a fresh session's library.
            assert "harbor_thug" in state["data"]["enemy_library"]

    def test_player_state_hides_the_mm_view(self, t):
        with t.client.websocket_connect("/ws") as ws:
            ws.send_json({"token": create_session_token("Player1", t.sid)})
            data = ws.receive_json()["data"]
            assert data["role"] == "player"
            assert data["your_character"]["name"] == "Mordai"
            assert "enemy_library" not in data and "danger" not in data

    def test_character_view_carries_use_trackers(self, t):
        view = wsmod.character_view(t.session, t.mordai)
        assert view["talent_uses_left"] == {}      # Warrior talents are passive
        assert view["level_up_ready"] is False and view["must_hold_on"] is False

    def test_bad_token_is_refused(self, client, active_session):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": "nope"})
            assert "Authentication failed" in ws.receive_json()["message"]

    def test_invite_token_cannot_open_a_socket(self, client, active_session):
        sid = active_session["session_id"]
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": create_invite_token("P9", sid)})
            assert "invite" in ws.receive_json()["message"].lower()

    def test_unknown_session_is_refused(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": create_mm_token(), "session_id": "no-such"})
            assert ws.receive_json()["message"] == "Session not found."

    def test_mm_needs_session_id(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"token": create_mm_token()})
            assert ws.receive_json()["message"] == "Missing session_id."

    def test_oversized_auth_is_refused(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_text("x" * (wsmod.WS_MAX_MESSAGE_BYTES + 1))
            assert ws.receive_json()["message"] == "Message too large."

    def test_invalid_json_auth_is_refused(self, client):
        with client.websocket_connect("/ws") as ws:
            ws.send_text("{nope")
            assert ws.receive_json()["message"] == "Invalid JSON."

    def test_oversized_message_in_loop_is_refused(self, t):
        t.p1.send_text("x" * (wsmod.WS_MAX_MESSAGE_BYTES + 1))
        assert error_text(call(t.p1)) == "Message too large."

    def test_non_object_message_is_refused(self, t):
        t.p1.send_text("[1, 2]")
        assert error_text(call(t.p1)) == "Invalid message."

    def test_unknown_event(self, t):
        assert "Unknown event" in error_text(call(t.p1, {"type": "strike"}))

    @pytest.mark.parametrize("event", MM_ONLY)
    def test_mm_only_events_refuse_players(self, t, event):
        msgs = call(t.p1, {"type": event})
        err = first(msgs, "error")
        assert err["message"] == "Only the Mirror Master can do that."
        assert err["event"] == event

    def test_every_design_event_has_a_handler(self):
        design = {"roll", "chat", "attack", "choose_option", "enemy_attack", "defend", "cast",
                  "avoid", "hold_on", "rest", "usage_roll", "wound_add", "wound_remove",
                  "level_up", "level_pick", "enemy_spawn", "enemy_update", "enemy_remove",
                  "morale_check", "toolbox_roll", "reaction_roll", "pressure_roll", "oracle",
                  "stuck", "end_exchange", "start_combat", "end_combat", "spend_spark",
                  "award_spark", "peer_call", "act_break", "graceful_fail", "session_end",
                  "threat_clock_create", "threat_clock_advance", "threat_clock_wind_back",
                  "threat_clock_delete", "ping"}
        assert design <= set(HANDLERS)


# ---------------------------------------------------------------------------
# Basics
# ---------------------------------------------------------------------------

class TestChat:
    def test_chat_reaches_everyone(self, t):
        call(t.p1, {"type": "chat", "text": "Hello"})
        assert first(call(t.z), "chat") == {"type": "chat", "from": "Player1", "text": "Hello"}

    def test_chat_is_capped(self, t):
        msgs = call(t.p1, {"type": "chat", "text": "a" * 5000})
        assert len(first(msgs, "chat")["text"]) == 2000

    def test_empty_chat_refused(self, t):
        assert "Say something" in error_text(call(t.p1, {"type": "chat", "text": "  "}))


# ---------------------------------------------------------------------------
# Rolls
# ---------------------------------------------------------------------------

class TestRoll:
    def test_roll_broadcasts_and_logs(self, t, dice):
        dice.push(5, 4)
        call(t.p1, {"type": "roll", "stat": "body", "difficulty": "Standard"})
        r = first(call(t.z), "roll_result")
        assert r["player"] == "Player1" and r["roll"]["total"] == 11
        assert r["roll"]["outcome"] == "full_success"
        assert t.session.roll_log[-1]["player_name"] == "Player1"

    def test_sparks_add_dice_and_are_debited(self, t, dice):
        dice.push(1, 2, 6)
        msgs = call(t.p1, {"type": "roll", "stat": "body", "sparks": 1, "knack": True})
        r = first(msgs, "roll_result")["roll"]
        assert r["kept"] == [6, 2] and r["total"] == 11
        assert t.mordai.sparks == 2
        assert first(msgs, "character_updated")["character"]["sparks"] == 2

    def test_natural_two_confirms_graceful_fail(self, t, dice):
        dice.push(1, 1)
        r = first(call(t.p1, {"type": "roll", "stat": "mind"}), "roll_result")["roll"]
        assert r["graceful_fail_claimed"] and t.mordai.sparks == 4

    def test_help_and_borrowed_trouble(self, t, dice):
        dice.push(1, 1, 6, 6)
        r = first(call(t.p1, {"type": "roll", "stat": "body", "help": 1, "helper": "Zahna",
                              "borrowed_trouble": True}), "roll_result")["roll"]
        assert r["natural_high"] and r["helper"] == "Zahna"

    def test_bad_stat_refused(self, t):
        assert "stat" in error_text(call(t.p1, {"type": "roll", "stat": "luck"}))

    def test_bad_difficulty_refused(self, t):
        assert "Difficulty" in error_text(call(t.p1, {"type": "roll", "stat": "body",
                                                      "difficulty": "Impossible"}))

    def test_too_many_sparks_refused(self, t):
        assert "Spark" in error_text(call(t.p1, {"type": "roll", "stat": "body", "sparks": 5}))

    def test_mm_rolls_for_a_named_player(self, t, dice):
        dice.push(3, 3)
        r = first(call(t.mm, {"type": "roll", "stat": "soul", "player": "Zahna"}), "roll_result")
        assert r["player"] == "Zahna"

    def test_mm_must_name_the_player(self, t):
        assert "Name the player" in error_text(call(t.mm, {"type": "roll", "stat": "body"}))

    def test_player_without_character(self, t, client):
        with client.websocket_connect("/ws") as w:
            w.send_json({"token": create_session_token("Nobody", t.sid)})
            w.receive_json()
            assert "no character" in error_text(call(w, {"type": "roll", "stat": "body"}))


class TestAvoid:
    def test_avoid_carries_the_tier_text(self, t, dice):
        dice.push(4, 4)
        r = first(call(t.z, {"type": "avoid", "stat": "mind"}), "avoid_result")["roll"]
        assert r["kind"] == "avoid" and r["total"] == 10
        assert r["extra"]["text"] == t.rs.roll_resolution.avoid.outcomes["full_success"]

    def test_avoid_spends_sparks(self, t, dice):
        dice.push(1, 1, 5)
        call(t.z, {"type": "avoid", "stat": "soul", "sparks": 1})
        assert t.zahna.sparks == 2

    def test_avoid_refuses_unheld_sparks(self, t):
        assert "Spark" in error_text(call(t.z, {"type": "avoid", "stat": "soul", "sparks": 9}))


# ---------------------------------------------------------------------------
# Combat
# ---------------------------------------------------------------------------

class TestCombatFlow:
    def test_start_combat(self, t):
        msgs = call(t.mm, {"type": "start_combat"})
        assert first(msgs, "combat_started")["combat"]["exchange"] == 1
        assert first(call(t.p1), "combat_started")
        assert t.session.combat is not None

    def test_start_twice_refused(self, t):
        call(t.mm, {"type": "start_combat"})
        assert "already" in error_text(call(t.mm, {"type": "start_combat"}))

    def test_end_exchange_expires_effects(self, t, dice):
        call(t.mm, {"type": "start_combat"})
        call(t.p1, {"type": "defend"})
        msgs = call(t.mm, {"type": "end_exchange"})
        ended = first(msgs, "exchange_ended")
        assert ended["exchange"] == 2 and ended["combat"]["defending"] == {}

    def test_end_exchange_without_fight(self, t):
        assert "No fight" in error_text(call(t.mm, {"type": "end_exchange"}))

    def test_end_combat(self, t):
        call(t.mm, {"type": "start_combat"})
        assert first(call(t.mm, {"type": "end_combat"}), "combat_ended")
        assert t.session.combat is None

    def test_end_combat_without_fight(self, t):
        assert "No fight" in error_text(call(t.mm, {"type": "end_combat"}))

    def test_telegraph_is_public(self, t):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        call(t.mm, {"type": "telegraph", "enemy": key, "text": "lunges at Zahna"})
        msg = first(call(t.z), "telegraph")
        assert msg["text"] == "lunges at Zahna" and msg["combat"]["telegraphs"][key]

    def test_telegraph_needs_a_fight(self, t):
        key = t.spawn()
        assert "Start the fight" in error_text(call(t.mm, {"type": "telegraph", "enemy": key,
                                                           "text": "x"}))

    def test_telegraph_needs_text(self, t):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        assert "Say what" in error_text(call(t.mm, {"type": "telegraph", "enemy": key}))


class TestAttack:
    def test_partial_hit_damages_and_exposes(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        dice.push(3, 3, 4)                      # 6 + Body 2 = 8; d8 shows 4
        msgs = call(t.p1, {"type": "attack", "target": key})
        res = first(msgs, "attack_result")["result"]
        assert res["tier"] == "partial_success" and res["damage"] == 4 and res["exposed"]
        assert "hp_after" not in res["enemy_result"]          # players do not see foe HP
        assert t.foe(key).hp_current == 4 and t.foe(key).bloodied
        assert t.session.combat.exposed["Mordai"] == [key]
        mm_view = first(call(t.mm), "attack_result")["result"]
        assert mm_view["enemy_result"]["hp_after"] == 4

    def test_ten_plus_waits_for_the_option_then_replays(self, t, dice):
        key = t.spawn()
        dice.push(5, 5, 3)                      # 12: full success; d8 shows 3
        msgs = call(t.p1, {"type": "attack", "target": key})
        choose = first(msgs, "attack_choose")
        assert {c["id"] for c in choose["choices"]} == {"extra_damage", "stunt", "cover"}
        assert "attack_result" not in kinds(msgs)
        assert t.foe(key).hp_current == 8          # nothing applied yet
        dice.push(2)                                # the +1d6
        res = first(call(t.p1, {"type": "choose_option", "options": ["extra_damage"]}),
                    "attack_result")["result"]
        assert res["damage_dice"] == [3] and res["extra_damage_dice"] == [2]
        assert res["damage"] == 5 and t.foe(key).hp_current == 3

    def test_named_option_in_advance_resolves_at_once(self, t, dice):
        key = t.spawn()
        dice.push(6, 5, 2)
        res = first(call(t.p1, {"type": "attack", "target": key, "options": ["stunt"]}),
                    "attack_result")["result"]
        assert res["options"] == ["stunt"] and "*" in t.foe(key).openings

    def test_cover_names_an_ally(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        dice.push(6, 5, 2)
        call(t.p1, {"type": "attack", "target": key})
        res = first(call(t.p1, {"type": "choose_option", "options": ["cover"], "cover_ally": "Zahna"}),
                    "attack_result")["result"]
        assert res["cover_for"] == "Zahna" and t.session.combat.covered["Zahna"] == "Mordai"

    def test_cover_without_ally_refused(self, t, dice):
        key = t.spawn()
        assert "Cover names an ally" in error_text(
            call(t.p1, {"type": "attack", "target": key, "options": ["cover"]}))

    def test_second_attack_while_choosing_refused(self, t, dice):
        key = t.spawn()
        dice.push(6, 6, 1)
        call(t.p1, {"type": "attack", "target": key})
        assert "option first" in error_text(call(t.p1, {"type": "attack", "target": key}))

    def test_miss_is_an_mm_move(self, t, dice):
        key = t.spawn()
        dice.push(1, 2)
        res = first(call(t.p1, {"type": "attack", "target": key}), "attack_result")["result"]
        assert res["mm_move"] and not res["hit"]

    def test_mook_drops_to_any_hit(self, t, dice):
        key = t.spawn(count=3, role="mook")
        dice.push(3, 3, 1)
        call(t.p1, {"type": "attack", "target": key})
        assert t.foe(key).count == 2

    def test_attack_without_target(self, t, dice):
        dice.push(3, 3, 5)
        res = first(call(t.p1, {"type": "attack"}), "attack_result")["result"]
        assert res["target"] is None and res["damage"] == 5

    def test_attack_unknown_target(self, t):
        assert "No foe" in error_text(call(t.p1, {"type": "attack", "target": "ghost"}))

    def test_attack_defeated_target(self, t):
        key = t.spawn()
        t.foe(key).defeated = True
        assert "out of the fight" in error_text(call(t.p1, {"type": "attack", "target": key}))

    def test_bad_option_refused(self, t):
        key = t.spawn()
        assert "Unknown option" in error_text(call(t.p1, {"type": "attack", "target": key,
                                                          "options": ["decapitate"]}))


class TestChooseOption:
    def test_nothing_pending(self, t):
        assert "no 10+" in error_text(call(t.p1, {"type": "choose_option", "options": ["stunt"]}))

    def test_empty_pick_refused(self, t, dice):
        key = t.spawn()
        dice.push(6, 6, 1)
        call(t.p1, {"type": "attack", "target": key})
        assert "Pick an option" in error_text(call(t.p1, {"type": "choose_option"}))

    def test_single_option_string(self, t, dice):
        key = t.spawn()
        dice.push(6, 6, 1)
        call(t.p1, {"type": "attack", "target": key})
        res = first(call(t.p1, {"type": "choose_option", "option": "stunt"}), "attack_result")
        assert res["result"]["options"] == ["stunt"]

    def test_foe_gone_before_pick(self, t, dice):
        key = t.spawn()
        dice.push(6, 6, 1)
        call(t.p1, {"type": "attack", "target": key})
        call(t.mm, {"type": "enemy_remove", "key": key})
        assert "gone" in error_text(call(t.p1, {"type": "choose_option", "option": "stunt"}))


class TestEnemyAttack:
    def test_hard_hit_through_armor(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        dice.push(5, 5)                           # 10 + 1 = 11: hard hit, 3 + 2 = 5, armor 3
        msgs = call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Player1"})
        res = first(msgs, "enemy_attack_result")["result"]
        assert res["label"] == "Hard hit" and res["raw_damage"] == 5 and res["armor"] == 3
        assert res["damage"] == 2 and t.mordai.hp_current == t.mordai.hp_max(t.rs) - 2
        assert first(call(t.p1), "enemy_attack_result")

    def test_exposure_adds_a_die(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        dice.push(3, 3, 4)
        call(t.p1, {"type": "attack", "target": key})
        dice.push(1, 1, 6)
        res = first(call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Mordai"}),
                    "enemy_attack_result")["result"]
        assert res["exposure_die"] and len(res["dice"]) == 3 and res["kept"] == [6, 1]

    def test_defend_makes_it_hard(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        call(t.z, {"type": "defend"})
        dice.push(4, 4)
        res = first(call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Zahna"}),
                    "enemy_attack_result")["result"]
        assert res["difficulty"] == "Hard" and res["total"] == 8

    def test_intercept_redirects(self, t, dice):
        key = t.spawn()
        call(t.mm, {"type": "start_combat"})
        call(t.p1, {"type": "defend", "intercept_for": ["Zahna"]})
        dice.push(4, 4)
        msgs = call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Zahna"})
        res = first(msgs, "enemy_attack_result")
        assert res["result"]["target"] == "Mordai" and res["player"] == "Player1"
        assert t.zahna.hp_current == t.zahna.hp_max(t.rs)

    def test_drop_to_zero_takes_a_wound_and_asks_for_hold_on(self, t, dice):
        key = t.spawn(level=5, role="boss", damage_override=40)
        dice.push(6, 6, 3)                        # a natural 12; the wound table roll
        msgs = call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Zahna"})
        res = first(msgs, "enemy_attack_result")
        assert res["fall"]["wound"]["name"]
        assert t.zahna.hp_current == 0
        assert t.zahna.wounds and "Zahna" in wsmod.table_state(t.sid).pending_hold_on
        assert first(msgs, "character_updated")["character"]["must_hold_on"] is True

    def test_broken_foe_cannot_attack(self, t):
        key = t.spawn()
        t.foe(key).broken = True
        assert "out of the fight" in error_text(call(t.mm, {"type": "enemy_attack", "enemy": key,
                                                            "target": "Zahna"}))

    def test_unknown_target(self, t):
        key = t.spawn()
        assert "No character" in error_text(call(t.mm, {"type": "enemy_attack", "enemy": key,
                                                        "target": "Nobody"}))


class TestDefend:
    def test_defend(self, t):
        call(t.mm, {"type": "start_combat"})
        msg = first(call(t.z, {"type": "defend"}), "defend_declared")
        assert msg["defender"] == "Zahna" and "Zahna" in msg["combat"]["defending"]

    def test_intercept_two_needs_sentinel(self, t):
        call(t.mm, {"type": "start_combat"})
        t.session.add_character(make_character(t.session.ruleset, name="Third", player_name="P3"))
        assert "Sentinel" in error_text(call(t.p1, {"type": "defend",
                                                    "intercept_for": ["Zahna", "P3"]}))

    def test_defend_outside_combat(self, t):
        assert "no fight" in error_text(call(t.p1, {"type": "defend"}))

    def test_intercept_unknown_ally(self, t):
        call(t.mm, {"type": "start_combat"})
        assert "No ally" in error_text(call(t.p1, {"type": "defend", "intercept_for": ["Ghost"]}))


# ---------------------------------------------------------------------------
# Magic
# ---------------------------------------------------------------------------

class TestCast:
    def test_harm_working_hits_and_pays_fatigue(self, t, dice):
        key = t.spawn()
        dice.push(5, 4, 6)                       # 9 + Mind 2 = 11; 1d8 shows 6
        msgs = call(t.z, {"type": "cast", "domain": "inscription", "scope": "significant",
                          "intent": "harm: a burning glyph", "target": key})
        res = first(msgs, "cast_result")["result"]
        assert res["outcome"] == "full_success" and res["damage"] == 6 and res["fatigue_paid"] == 1
        assert t.zahna.fatigue == 1 and t.foe(key).hp_current == 2

    def test_signature_working_is_easier(self, t, dice):
        dice.push(3, 3)
        res = first(call(t.z, {"type": "cast", "domain": "inscription", "scope": "minor",
                               "working": "A sealing glyph", "intent": "seal"}), "cast_result")["result"]
        assert res["plan"]["signature"] and res["plan"]["difficulty"] == "Easy"
        assert res["roll"]["total"] == 9 and res["fatigue_paid"] == 0

    def test_partial_offers_two_costs_then_choice(self, t, dice):
        dice.push(3, 3)                          # 6 + 2 = 8
        res = first(call(t.z, {"type": "cast", "domain": "inscription", "scope": "significant",
                               "intent": "bind the door"}), "cast_result")["result"]
        assert len(res["complication_options"]) == 2
        chosen = first(call(t.z, {"type": "choose_complication", "index": 1}), "complication_chosen")
        assert chosen["complication"] == res["complication_options"][1]
        assert "No casting cost" in error_text(call(t.z, {"type": "choose_complication", "index": 0}))

    def test_failure_rolls_a_mishap(self, t, dice):
        dice.push(1, 2)
        res = first(call(t.z, {"type": "cast", "domain": "inscription", "scope": "significant",
                               "intent": "x"}), "cast_result")["result"]
        assert res["mishap"] and res["graceful_fail_applies"]

    def test_major_needs_level_three(self, t):
        assert "level 3" in error_text(call(t.z, {"type": "cast", "domain": "inscription",
                                                  "scope": "major", "intent": "x"}))

    def test_non_caster_refused(self, t):
        assert "holds no" in error_text(call(t.p1, {"type": "cast", "domain": "inscription",
                                                    "scope": "minor"}))

    def test_group_targets_on_single_scope_refused(self, t, dice):
        a, b = t.spawn(id="a"), t.spawn(id="b")
        dice.push(6, 6, 3)
        assert "group" in error_text(call(t.z, {"type": "cast", "domain": "inscription",
                                                "scope": "significant", "intent": "harm",
                                                "targets": [a, b]}))

    def test_preview_is_private_and_rolls_nothing(self, t):
        msgs = call(t.z, {"type": "cast_preview", "domain": "inscription", "scope": "significant"})
        plan = first(msgs, "cast_plan")["plan"]
        assert plan["fatigue"] == 1 and plan["ok"] and t.zahna.fatigue == 0
        assert "cast_plan" not in kinds(call(t.p1))

    def test_preview_reports_errors(self, t):
        plan = first(call(t.p1, {"type": "cast_preview", "domain": "fire", "scope": "minor"}),
                     "cast_plan")["plan"]
        assert not plan["ok"] and plan["errors"]


# ---------------------------------------------------------------------------
# 0 HP and recovery
# ---------------------------------------------------------------------------

def _drop(t, player="Zahna"):
    ch = t.session.characters[player]
    ch.hp_current = 0
    wsmod.table_state(t.sid).pending_hold_on.add(player)
    return ch


class TestHoldOn:
    def test_ten_plus_stands_at_one(self, t, dice):
        _drop(t, "Player1")
        dice.push(5, 4)                           # 9 + Body 2
        msg = first(call(t.p1, {"type": "hold_on"}), "hold_on_result")
        assert msg["status"] == "ok" and t.mordai.hp_current == 1
        assert "Player1" not in wsmod.table_state(t.sid).pending_hold_on

    def test_six_minus_is_dying(self, t, dice):
        _drop(t)
        dice.push(2, 3)
        assert first(call(t.z, {"type": "hold_on"}), "hold_on_result")["status"] == "dying"

    def test_not_at_zero_refused(self, t):
        assert "not at 0 HP" in error_text(call(t.z, {"type": "hold_on"}))


class TestTendAndDeath:
    def test_tend_saves_the_dying(self, t):
        ch = _drop(t)
        ch.status = "dying"
        msg = first(call(t.p1, {"type": "tend", "target": "Zahna"}), "tended")
        assert msg["status"] == "out" and ch.status == "out"

    def test_tend_someone_not_dying(self, t):
        assert "not dying" in error_text(call(t.p1, {"type": "tend", "target": "Zahna"}))

    def test_tend_yourself_refused(self, t):
        t.zahna.status = "dying"
        assert "yourself" in error_text(call(t.z, {"type": "tend", "target": "Zahna"}))

    def test_death_choice_scar(self, t, dice):
        t.zahna.status = "dying"
        msg = first(call(t.z, {"type": "death_choice", "choice": "scar"}), "death_choice_made")
        assert msg["scar"]["name"] and t.zahna.status == "out"

    def test_death_choice_heroic(self, t):
        t.zahna.status = "dying"
        assert first(call(t.z, {"type": "death_choice", "choice": "heroic"}),
                     "death_choice_made")["status"] == "dead"

    def test_death_choice_when_not_dying(self, t):
        assert "not dying" in error_text(call(t.z, {"type": "death_choice", "choice": "scar"}))


class TestRest:
    def test_player_breather_restores_half(self, t):
        t.mordai.hp_current = 2
        msg = first(call(t.p1, {"type": "rest", "kind": "breather"}), "rest_result")
        assert msg["results"][0]["hp"] == 2 + t.mordai.hp_max(t.rs) // 2

    def test_mm_night_rest_clears_fatigue_and_a_wound(self, t):
        t.zahna.fatigue = 2
        t.zahna.add_wound("Cracked ribs")
        t.zahna.hp_current = 1
        msg = first(call(t.mm, {"type": "rest", "kind": "night", "players": ["Zahna"]}), "rest_result")
        assert msg["results"][0]["fatigue_cleared"] == 2
        assert t.zahna.fatigue == 0 and not t.zahna.wounds
        assert t.zahna.hp_current == t.zahna.hp_max(t.rs)

    def test_player_cannot_call_a_night(self, t):
        assert "MM calls" in error_text(call(t.p1, {"type": "rest", "kind": "night"}))

    def test_bad_kind(self, t):
        assert "breather or a night" in error_text(call(t.p1, {"type": "rest", "kind": "nap"}))

    def test_breather_in_danger_rolls_pressure_for_the_mm(self, t):
        msgs = call(t.mm, {"type": "rest", "kind": "breather", "in_danger": True})
        assert first(msgs, "toolbox_result")["kind"] == "pressure"
        assert "toolbox_result" not in kinds(call(t.p1))

    def test_dying_character_reports_error_in_results(self, t):
        t.zahna.status = "dying"
        msg = first(call(t.mm, {"type": "rest", "kind": "breather"}), "rest_result")
        assert any("error" in r for r in msg["results"])


class TestHpAdjust:
    def test_damage_and_heal(self, t):
        mx = t.mordai.hp_max(t.rs)
        call(t.mm, {"type": "hp_adjust", "player": "Player1", "delta": -5})
        assert t.mordai.hp_current == mx - 5
        call(t.mm, {"type": "hp_adjust", "player": "Player1", "delta": 3})
        assert t.mordai.hp_current == mx - 2

    def test_damage_to_zero_asks_for_hold_on(self, t):
        msg = first(call(t.mm, {"type": "hp_adjust", "player": "Zahna", "delta": -50}), "hp_adjusted")
        assert msg["fall"]["wound"] and "Zahna" in wsmod.table_state(t.sid).pending_hold_on

    def test_zero_refused(self, t):
        assert "non-zero" in error_text(call(t.mm, {"type": "hp_adjust", "player": "Zahna"}))


class TestWounds:
    def test_player_adds_a_named_wound(self, t):
        msg = first(call(t.p1, {"type": "wound_add", "name": "Sprained wrist"}), "wound_added")
        assert msg["wound"] == {"name": "Sprained wrist"} and t.mordai.wounds

    def test_unnamed_wound_is_rolled(self, t):
        msg = first(call(t.mm, {"type": "wound_add", "player": "Zahna"}), "wound_added")
        assert msg["wound"]["name"]

    def test_wound_past_capacity_flags_items_to_drop(self, t):
        for i in range(6):
            t.zahna.add_wound(f"w{i}")
        msg = first(call(t.z, {"type": "wound_add", "name": "one more"}), "wound_added")
        assert msg["items_to_drop"] >= 1

    def test_mm_removes_a_wound(self, t):
        t.zahna.add_wound("Cut")
        assert first(call(t.mm, {"type": "wound_remove", "player": "Zahna", "index": 0}),
                     "wound_removed")["wound"]["name"] == "Cut"

    def test_remove_with_no_wounds(self, t):
        assert "no Wounds" in error_text(call(t.mm, {"type": "wound_remove", "player": "Zahna"}))


class TestUsageRoll:
    def test_low_roll_steps_down(self, t, dice):
        dice.push(1)
        res = first(call(t.p1, {"type": "usage_roll", "item": "rations"}), "usage_result")["result"]
        assert res["stepped_down"] and res["usage_die"] == 4

    def test_high_roll_holds(self, t, dice):
        dice.push(6)
        res = first(call(t.p1, {"type": "usage_roll", "item": "rations"}), "usage_result")["result"]
        assert not res["stepped_down"] and res["usage_die"] == 6

    def test_item_without_usage_die(self, t):
        assert "no usage die" in error_text(call(t.p1, {"type": "usage_roll", "item": "rope"}))


class TestTalentUse:
    def test_limited_talent_ticks_down(self, t):
        ch = make_character(t.session.ruleset, name="Vex", player_name="P3", facet="soul",
                            second_stat="body", class_id=None, background_id="street_performer",
                            custom_class={"name": "Herald", "concept": "I lift the room.",
                                          "knack": "Crowds", "talents": ["inspiring", "hunch"],
                                          "kit": ["rations"]})
        t.session.add_character(ch)
        tid = "inspiring"
        msg = first(call(t.mm, {"type": "talent_use", "player": "P3", "talent_id": tid}), "talent_used")
        assert msg["uses_left"] == 0
        assert "no uses left" in error_text(call(t.mm, {"type": "talent_use", "player": "P3",
                                                        "talent_id": tid}))

    def test_passive_talent_is_untracked(self, t):
        msg = first(call(t.p1, {"type": "talent_use", "talent_id": "tough"}), "talent_used")
        assert msg["uses_left"] is None

    def test_unheld_talent_refused(self, t):
        assert "does not have" in error_text(call(t.p1, {"type": "talent_use", "talent_id": "lucky"}))

    def test_scene_end_refreshes(self, t):
        t.mordai.talent_uses["tough@scene"] = 1
        assert first(call(t.mm, {"type": "scene_end"}), "scene_ended")
        assert "tough@scene" not in t.mordai.talent_uses


# ---------------------------------------------------------------------------
# Sparks
# ---------------------------------------------------------------------------

class TestSparks:
    def test_award(self, t):
        msg = first(call(t.mm, {"type": "award_spark", "player": "Zahna", "reason": "Great bit"}),
                    "spark_earned")
        assert msg["sparks_now"] == 4 and msg["reason"] == "Great bit"

    def test_award_unknown_player(self, t):
        assert "No character" in error_text(call(t.mm, {"type": "award_spark", "player": "X"}))

    def test_spend(self, t):
        assert first(call(t.p1, {"type": "spend_spark"}), "spark_spent")["sparks_now"] == 2

    def test_spend_with_none_left(self, t):
        t.mordai.sparks = 0
        assert "Spark" in error_text(call(t.p1, {"type": "spend_spark"}))

    def test_peer_call(self, t):
        call(t.p1, {"type": "peer_call", "player": "Zahna"})
        msg = first(call(t.mm), "spark_nomination")
        assert msg["kind"] == "peer_call" and msg["player"] == "Zahna" and t.zahna.sparks == 3

    def test_peer_call_on_yourself_refused(self, t):
        assert "someone else" in error_text(call(t.p1, {"type": "peer_call", "player": "Player1"}))

    def test_act_break_and_nomination(self, t):
        call(t.mm, {"type": "act_break"})
        assert first(call(t.p1), "act_break_opened")
        msg = first(call(t.p1, {"type": "act_break_nominate", "player": "Zahna"}), "spark_nomination")
        assert msg["kind"] == "act_break"

    def test_act_break_self_nomination_refused(self, t):
        assert "someone else" in error_text(call(t.z, {"type": "act_break_nominate", "player": "Zahna"}))

    def test_graceful_fail_claim_and_confirm(self, t, dice):
        dice.push(2, 1)
        call(t.z, {"type": "roll", "stat": "body"})
        assert first(call(t.z, {"type": "graceful_fail", "narration": "I fall in the fountain"}),
                     "graceful_fail_claimed")
        msg = first(call(t.mm, {"type": "graceful_fail_confirm", "player": "Zahna"}), "spark_earned")
        assert msg["reason"] == "Graceful Fail" and t.zahna.sparks == 4

    def test_graceful_fail_needs_a_failed_roll(self, t, dice):
        dice.push(6, 5)
        call(t.z, {"type": "roll", "stat": "mind"})
        assert "not a 6-" in error_text(call(t.z, {"type": "graceful_fail"}))

    def test_graceful_fail_claimed_once(self, t, dice):
        dice.push(2, 1)
        call(t.z, {"type": "roll", "stat": "body"})
        call(t.z, {"type": "graceful_fail"})
        assert "already claimed" in error_text(call(t.z, {"type": "graceful_fail"}))

    def test_confirm_without_claim(self, t):
        assert "no Graceful Fail" in error_text(call(t.mm, {"type": "graceful_fail_confirm",
                                                            "player": "Zahna"}))


# ---------------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------------

class TestLevels:
    def test_session_end_prompts_are_mm_only(self, t):
        msg = first(call(t.mm, {"type": "session_end"}), "session_end_prompts")
        assert len(msg["prompts"]) == 5 and msg["pacing_suggests_level"] == 2
        assert {c["player"] for c in msg["characters"]} == {"Player1", "Zahna"}
        assert "session_end_prompts" not in kinds(call(t.p1))

    def test_grant_then_pick_a_talent(self, t):
        before = t.mordai.hp_max(t.rs)
        msgs = call(t.mm, {"type": "level_up", "players": ["Player1"]})
        assert first(msgs, "level_up_ready")["players"] == ["Player1"]
        done = first(call(t.p1, {"type": "level_pick", "kind": "talent", "talent_id": "sentinel"}),
                     "level_up_done")
        assert done["level"] == 2 and t.mordai.level == 2
        assert t.mordai.hp_max(t.rs) == before + t.mordai.facet_def(t.rs).grit_average
        assert "Player1" not in t.session.level_up_ready

    def test_grant_everyone(self, t):
        assert set(first(call(t.mm, {"type": "level_up"}), "level_up_ready")["players"]) == \
            {"Player1", "Zahna"}

    def test_grant_unknown_player(self, t):
        assert "No such" in error_text(call(t.mm, {"type": "level_up", "players": ["Ghost"]}))

    def test_pick_without_grant(self, t):
        assert "not called" in error_text(call(t.p1, {"type": "level_pick", "kind": "talent",
                                                      "talent_id": "sentinel"}))

    def test_invalid_pick_returns_errors_and_keeps_level(self, t):
        call(t.mm, {"type": "level_up"})
        msg = first(call(t.p1, {"type": "level_pick", "kind": "talent", "talent_id": "tough"}),
                    "level_pick_error")
        assert msg["errors"] and t.mordai.level == 1 and "Player1" in t.session.level_up_ready

    def test_rolled_hp(self, t, dice):
        call(t.mm, {"type": "level_up"})
        dice.push(9)
        done = first(call(t.p1, {"type": "level_pick", "kind": "talent", "talent_id": "sentinel",
                                 "hp": "roll"}), "level_up_done")
        assert done["hp_roll"] == 9

    def test_bad_hp_mode(self, t):
        call(t.mm, {"type": "level_up"})
        assert "HP is" in error_text(call(t.p1, {"type": "level_pick", "kind": "talent",
                                                 "talent_id": "sentinel", "hp": "max"}))

    def test_signature_at_three(self, t):
        t.mordai.level = 2
        call(t.mm, {"type": "level_up"})
        call(t.p1, {"type": "level_pick", "kind": "signature", "talent_id": "unstoppable"})
        assert t.mordai.signature == "unstoppable" and t.mordai.level == 3

    def test_next_session_resets_sparks(self, t):
        t.mordai.sparks = 0
        msgs = call(t.mm, {"type": "next_session"})
        assert first(msgs, "session_started")["session_number"] == 2
        assert t.mordai.sparks == 3 and first(msgs, "state")

    def test_respec_before_signature(self, t):
        call(t.p1, {"type": "respec", "talents": [{"id": "weapon_master", "choice": "blunt"},
                                                  {"id": "sentinel"}]})
        assert {x.id for x in t.mordai.talents} == {"weapon_master", "sentinel"}

    def test_respec_bad_talents(self, t):
        assert error_text(call(t.p1, {"type": "respec", "talents": [{"id": "nope"}]}))

    def test_respec_needs_a_list(self, t):
        assert "list" in error_text(call(t.p1, {"type": "respec", "talents": "tough"}))


# ---------------------------------------------------------------------------
# The tracker
# ---------------------------------------------------------------------------

class TestEnemySpawn:
    def test_spawn_split_views(self, t):
        key = t.add_card(level=3, hp_override=None).id
        call(t.mm, {"type": "enemy_spawn", "enemy_id": key})
        msg = first(call(t.p1), "enemy_spawned")["enemy"]
        assert msg["key"] == key and "hp_current" not in msg and "wants" not in msg
        assert t.foe(key).hp_current == t.rs.monsters.row(3).hp

    def test_spawn_mob_and_unique_keys(self, t):
        t.add_card(role="mook")
        k1 = first(call(t.mm, {"type": "enemy_spawn", "enemy_id": "mook_1", "count": 4}),
                   "enemy_spawned")["enemy"]["key"]
        k2 = first(call(t.mm, {"type": "enemy_spawn", "enemy_id": "mook_1"}),
                   "enemy_spawned")["enemy"]["key"]
        assert k1 == "mook_1" and k2 == "mook_1-2" and t.foe(k1).count == 4

    def test_spawn_mob_of_standards_refused(self, t):
        t.add_card()
        assert "Only Mooks" in error_text(call(t.mm, {"type": "enemy_spawn",
                                                      "enemy_id": "standard_1", "count": 3}))

    def test_spawn_unknown_card(self, t):
        assert "No card" in error_text(call(t.mm, {"type": "enemy_spawn", "enemy_id": "zzz"}))

    def test_spawn_updates_mm_danger(self, t):
        t.add_card(role="boss", level=3)
        msgs = call(t.mm, {"type": "enemy_spawn", "enemy_id": "boss_3"})
        assert first(msgs, "danger")["danger"]["read"] in ("hard", "deadly", "fight", "skirmish")


class TestEnemyUpdate:
    def test_damage_goes_through_the_engine(self, t):
        key = t.spawn()
        msgs = call(t.mm, {"type": "enemy_update", "key": key, "damage": 5})
        assert first(msgs, "enemy_damage")["result"]["bloodied_now"]
        assert t.foe(key).bloodied and t.foe(key).hp_current == 3

    def test_manual_corrections(self, t):
        key = t.spawn()
        call(t.mm, {"type": "enemy_update", "key": key, "hp_current": 2, "broken": True, "name": "Bob"})
        f = t.foe(key)
        assert f.hp_current == 2 and f.broken and f.name == "Bob"
        call(t.mm, {"type": "enemy_update", "key": key, "heal": 100})
        assert f.hp_current == 8

    def test_mook_count(self, t):
        key = t.spawn(count=3, role="mook")
        call(t.mm, {"type": "enemy_update", "key": key, "count": 0})
        assert t.foe(key).defeated

    def test_hp_out_of_range(self, t):
        key = t.spawn()
        assert "between" in error_text(call(t.mm, {"type": "enemy_update", "key": key,
                                                   "hp_current": 99}))

    def test_unknown_key(self, t):
        assert "No foe" in error_text(call(t.mm, {"type": "enemy_update", "key": "x"}))


class TestEnemyRemove:
    def test_remove(self, t):
        key = t.spawn()
        call(t.mm, {"type": "enemy_remove", "key": key})
        assert key not in t.session.active_enemies
        assert first(call(t.p1), "enemy_removed")["key"] == key

    def test_remove_unknown(self, t):
        assert "No foe" in error_text(call(t.mm, {"type": "enemy_remove", "key": "x"}))

    def test_remove_then_spawn_reuses_key(self, t):
        key = t.spawn()
        call(t.mm, {"type": "enemy_remove", "key": key})
        assert first(call(t.mm, {"type": "enemy_spawn", "enemy_id": "standard_1"}),
                     "enemy_spawned")["enemy"]["key"] == key


class TestMorale:
    def test_breaks_over_morale(self, t, dice):
        key = t.spawn(morale=6)
        dice.push(4, 3)
        res = first(call(t.mm, {"type": "morale_check", "enemy": key}), "morale_result")["result"]
        assert res["breaks"] and t.foe(key).broken

    def test_fearless_never_breaks(self, t, dice):
        key = t.spawn(morale=12)
        dice.push(6, 6)
        res = first(call(t.mm, {"type": "morale_check", "enemy": key, "bonus": 2}),
                    "morale_result")["result"]
        assert res["fearless"] and not res["breaks"]

    def test_defeated_foe(self, t):
        key = t.spawn()
        t.foe(key).defeated = True
        assert "defeated" in error_text(call(t.mm, {"type": "morale_check", "enemy": key}))


class TestBestiaryLoad:
    def test_library_holds_the_bestiary(self, t):
        msg = first(call(t.mm, {"type": "bestiary_load"}), "enemy_library")
        assert "chicken" in msg["library"] and "archive_guardian" in msg["library"]

    def test_reload_adds_nothing_new(self, t):
        assert first(call(t.mm, {"type": "bestiary_load"}), "enemy_library")["loaded"] == []

    def test_missing_dir_is_harmless(self, t, monkeypatch, tmp_path):
        monkeypatch.setattr(wsmod, "BESTIARY_DIR", tmp_path / "none")
        assert first(call(t.mm, {"type": "bestiary_load"}), "enemy_library")["loaded"] == []


# ---------------------------------------------------------------------------
# Toolbox
# ---------------------------------------------------------------------------

class TestToolbox:
    def test_table_roll_is_private(self, t):
        msg = first(call(t.mm, {"type": "toolbox_roll", "table": "trinkets"}), "toolbox_result")
        assert msg["result"]["text"] and not msg["revealed"] and msg["result_id"]
        assert "toolbox_result" not in kinds(call(t.p1))

    def test_revealed_roll_is_public(self, t):
        call(t.mm, {"type": "toolbox_roll", "table": "trinkets", "reveal": True})
        assert first(call(t.p1), "toolbox_result")["revealed"]

    def test_reveal_a_private_result(self, t):
        rid = first(call(t.mm, {"type": "toolbox_roll", "table": "npc_names"}), "toolbox_result")["result_id"]
        call(t.mm, {"type": "toolbox_reveal", "result_id": rid})
        assert first(call(t.p1), "toolbox_result")["revealed"]
        assert "no longer" in error_text(call(t.mm, {"type": "toolbox_reveal", "result_id": rid}))

    def test_unknown_table(self, t):
        assert "No table" in error_text(call(t.mm, {"type": "toolbox_roll", "table": "dragons"}))

    def test_reaction(self, t, dice):
        dice.push(6, 6)
        res = first(call(t.mm, {"type": "reaction_roll", "modifier": -1}), "toolbox_result")["result"]
        assert res["total"] == 11 and res["table"] == "reaction"

    def test_reaction_modifier_bounds(self, t):
        assert "between" in error_text(call(t.mm, {"type": "reaction_roll", "modifier": 9}))

    def test_reaction_clamps_to_table(self, t, dice):
        dice.push(1, 1)
        assert first(call(t.mm, {"type": "reaction_roll", "modifier": -3}),
                     "toolbox_result")["result"]["total"] == 2

    @pytest.mark.parametrize("variant", ["generic", "underground", "wild", "settlement", "occasion"])
    def test_pressure_variants(self, t, variant):
        res = first(call(t.mm, {"type": "pressure_roll", "variant": variant}), "toolbox_result")["result"]
        assert res["table"] == f"pressure_{variant}"

    def test_pressure_default_is_generic(self, t):
        assert first(call(t.mm, {"type": "pressure_roll"}),
                     "toolbox_result")["result"]["table"] == "pressure_generic"

    def test_pressure_bad_variant(self, t):
        assert "Unknown Pressure" in error_text(call(t.mm, {"type": "pressure_roll", "variant": "sea"}))

    def test_oracle(self, t, dice):
        dice.push(6, 6)
        res = first(call(t.mm, {"type": "oracle", "odds": "unlikely", "question": "Is it locked?"}),
                    "toolbox_result")["result"]
        assert res["answer"] == "Yes, and…" and res["question"] == "Is it locked?"

    def test_oracle_default_odds(self, t):
        assert first(call(t.mm, {"type": "oracle"}), "toolbox_result")["result"]["odds"] == "even"

    def test_oracle_bad_odds(self, t):
        assert "Unknown odds" in error_text(call(t.mm, {"type": "oracle", "odds": "certain"}))

    def test_stuck_gives_three_options(self, t):
        res = first(call(t.mm, {"type": "stuck"}), "toolbox_result")["result"]
        assert [o["kind"] for o in res] == ["threat", "arrival", "secret"]

    def test_stuck_names_a_clock(self, t):
        call(t.mm, {"type": "threat_clock_create", "name": "The flood"})
        res = first(call(t.mm, {"type": "stuck"}), "toolbox_result")["result"]
        assert "The flood" in res[0]["text"]

    def test_stuck_is_never_revealed_directly(self, t):
        call(t.mm, {"type": "stuck", "reveal": True})
        assert "toolbox_result" not in kinds(call(t.p1))

    def test_hoard(self, t):
        res = first(call(t.mm, {"type": "hoard", "site_level": 3}), "toolbox_result")["result"]
        assert res["site_level"] == 3 and res["curio"]

    def test_hoard_level_bounds(self, t):
        assert "between" in error_text(call(t.mm, {"type": "hoard", "site_level": 11}))

    def test_hoard_revealed(self, t):
        call(t.mm, {"type": "hoard", "site_level": 1, "reveal": True})
        assert first(call(t.p1), "toolbox_result")["kind"] == "hoard"

    def test_npc_card(self, t):
        res = first(call(t.mm, {"type": "npc"}), "toolbox_result")["result"]
        assert all(res[k] for k in ("name", "trait", "want", "secret"))

    def test_npc_private(self, t):
        call(t.mm, {"type": "npc"})
        assert "toolbox_result" not in kinds(call(t.p1))

    def test_npc_revealed(self, t):
        call(t.mm, {"type": "npc", "reveal": True})
        assert first(call(t.z), "toolbox_result")["kind"] == "npc"


# ---------------------------------------------------------------------------
# Threat clocks
# ---------------------------------------------------------------------------

class TestClocks:
    def _make(self, t, **kw):
        return first(call(t.mm, {"type": "threat_clock_create", **kw}), "clock_updated")["clock"]

    def test_create_uses_ruleset_default(self, t):
        clock = self._make(t, name="Guards")
        assert clock["segments"] == 4 and first(call(t.p1), "clock_updated")

    def test_create_bounds(self, t):
        assert "between" in error_text(call(t.mm, {"type": "threat_clock_create", "segments": 40}))

    def test_create_default_name(self, t):
        assert self._make(t)["name"] == "Threat"

    def test_advance_and_fill(self, t):
        c = self._make(t, segments=2)
        call(t.mm, {"type": "threat_clock_advance", "clock_id": c["id"]})
        msg = first(call(t.mm, {"type": "threat_clock_advance", "clock_id": c["id"]}), "clock_updated")
        assert msg["filled"] and msg["clock"]["is_full"]

    def test_full_success_does_not_advance(self, t):
        c = self._make(t)
        msg = first(call(t.mm, {"type": "threat_clock_advance", "clock_id": c["id"],
                                "outcome_tier": "full_success"}), "clock_updated")
        assert msg["clock"]["filled_segments"] == 0

    def test_advance_unknown(self, t):
        assert "No Threat Clock" in error_text(call(t.mm, {"type": "threat_clock_advance",
                                                           "clock_id": "x"}))

    def test_wind_back(self, t):
        c = self._make(t)
        call(t.mm, {"type": "threat_clock_advance", "clock_id": c["id"]})
        msg = first(call(t.mm, {"type": "threat_clock_wind_back", "clock_id": c["id"]}), "clock_updated")
        assert msg["clock"]["filled_segments"] == 0

    def test_wind_back_floor(self, t):
        c = self._make(t)
        msg = first(call(t.mm, {"type": "threat_clock_wind_back", "clock_id": c["id"]}), "clock_updated")
        assert msg["clock"]["filled_segments"] == 0

    def test_wind_back_unknown(self, t):
        assert "No Threat Clock" in error_text(call(t.mm, {"type": "threat_clock_wind_back",
                                                           "clock_id": "x"}))

    def test_delete(self, t):
        c = self._make(t)
        call(t.mm, {"type": "threat_clock_delete", "clock_id": c["id"]})
        assert first(call(t.p1), "clock_deleted")["clock_id"] == c["id"]
        assert not t.session.threat_clocks

    def test_delete_unknown(self, t):
        assert "No Threat Clock" in error_text(call(t.mm, {"type": "threat_clock_delete",
                                                           "clock_id": "x"}))

    def test_delete_one_of_two(self, t):
        a, b = self._make(t, name="A"), self._make(t, name="B")
        call(t.mm, {"type": "threat_clock_delete", "clock_id": a["id"]})
        assert list(t.session.threat_clocks) == [b["id"]]


# ---------------------------------------------------------------------------
# A full round, end to end
# ---------------------------------------------------------------------------

def test_full_combat_round(t, dice):
    """Telegraph, attack with a 10+ pick, a cast, an enemy attack in the open,
    end of exchange: the whole of DESIGN §1's exchange through the socket."""
    key = t.spawn(level=1, role="elite")                 # HP 16, two attacks
    call(t.mm, {"type": "start_combat"})
    call(t.mm, {"type": "telegraph", "enemy": key, "text": "swings at Zahna"})
    dice.push(5, 5, 6)
    call(t.p1, {"type": "attack", "target": key})
    dice.push(4)
    call(t.p1, {"type": "choose_option", "options": ["extra_damage"]})
    assert t.foe(key).hp_current == 6 and t.foe(key).bloodied
    dice.push(4, 4, 5)
    call(t.z, {"type": "cast", "domain": "inscription", "scope": "significant",
               "intent": "harm", "target": key})
    assert t.foe(key).hp_current == 1
    dice.push(3, 3)
    call(t.mm, {"type": "enemy_attack", "enemy": key, "target": "Zahna"})
    assert t.zahna.hp_current == t.zahna.hp_max(t.rs) - 2   # 3 damage - light armor 1
    msgs = call(t.mm, {"type": "end_exchange"})
    assert first(msgs, "exchange_ended")["exchange"] == 2
    log = [e["kind"] for e in t.session.roll_log]
    assert log == ["attack", "cast"]


class TestPrivacyAndSync:
    def test_players_never_see_mm_notes(self, t):
        t.zahna.notes_mm = "secretly the heir"
        mm_msgs = call(t.mm, {"type": "character_sync", "player": "Zahna"})
        assert "notes_mm" not in first(call(t.p1), "character_updated")["character"]
        assert first(mm_msgs, "character_updated")["character"]["notes_mm"] == "secretly the heir"

    def test_player_state_strips_mm_notes(self, t):
        t.zahna.notes_mm = "x"
        data = wsmod.state_for(t.session, "Zahna", False)
        assert "notes_mm" not in data["your_character"]
        assert all("notes_mm" not in c for c in data["all_characters"].values())

    def test_sync_refuses_unknown_character(self, t):
        assert "No character" in error_text(call(t.mm, {"type": "character_sync", "player": "Ghost"}))

    def test_player_syncs_only_themselves(self, t):
        msg = first(call(t.p1, {"type": "character_sync", "player": "Zahna"}), "character_updated")
        assert msg["player"] == "Player1"


class TestStaticAssets:
    """The SPA the socket serves: every asset loads, and none speaks v0.3."""

    ASSETS = ["/static/js/app.js", "/static/js/components.js", "/static/js/play.js",
              "/static/js/builder.js", "/static/js/tools.js", "/static/css/style.css"]

    def test_index_links_every_asset(self, client):
        html = client.get("/").text
        assert "<title>Facets of Origin</title>" in html
        for asset in self.ASSETS:
            assert asset in html

    @pytest.mark.parametrize("asset", ASSETS)
    def test_asset_is_served(self, client, asset):
        resp = client.get(asset)
        assert resp.status_code == 200 and len(resp.text) > 1000

    def test_join_route_serves_the_app(self, client):
        assert "id=\"join-screen\"" in client.get("/join?token=x").text

    def test_every_client_event_has_a_handler(self):
        """Each `type: '...'` the SPA sends is an event the server handles."""
        import re
        from pathlib import Path
        root = Path(wsmod.__file__).resolve().parents[1] / "static" / "js"
        sent = set()
        for js in root.glob("*.js"):
            sent |= set(re.findall(r"send\(\{\s*type:\s*'([a-z_]+)'", js.read_text(encoding="utf-8")))
        # Events sent with a computed type (data-mm buttons) are listed in play.js's session panel.
        sent |= {"start_combat", "end_exchange", "end_combat", "scene_end", "act_break", "session_end"}
        assert sent and sent <= set(HANDLERS), sorted(sent - set(HANDLERS))
