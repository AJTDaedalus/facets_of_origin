"""A long-lived table that short-lived processes can act on.

The harness holds one WebSocket per participant and an observer socket that is
the sole writer of the event log. A subagent driving the table through `Bash`
gets a fresh process per turn and cannot hold any of that.

So the table lives here, in one background process, behind a loopback HTTP API.
`play_as.py` is a thin client for it. Crucially, **the rule stays intact**: a
turn request names a verb and its arguments, `Verbs` sends it on that actor's own
authenticated socket, and the engine's broadcast comes back as the result. A
caller still cannot state an outcome — it can only ask for one.

Bound to 127.0.0.1 and unauthenticated: this is a local test fixture that fronts
a throwaway server holding invented characters. Do not expose it.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from tools.agentic_playtest.client import TableRuling
from tools.agentic_playtest.verbs import MM_VERBS, PLAYER_VERBS, Verbs


class Broker:
    """Owns the table. One instance per session."""

    def __init__(self, table, out_dir: Path, party: list[dict]) -> None:
        self.table = table
        self.verbs = Verbs(table)
        self.out_dir = out_dir
        self.party = {p["player_name"]: p for p in party}
        self.lock = threading.Lock()
        self.server: ThreadingHTTPServer | None = None

    # ------------------------------------------------------------------

    def take_turn(self, actor: str, verb: str, args: dict) -> dict:
        """Run one verb as one actor. Serialised — the table is not reentrant."""
        allowed = MM_VERBS if actor == "MM" else PLAYER_VERBS
        if verb not in allowed:
            return {"refused": f"'{verb}' is not something {actor} can do. "
                               f"Available: {', '.join(sorted(allowed))}"}
        method = getattr(self.verbs, verb, None)
        if method is None:
            return {"refused": f"No such verb '{verb}'."}

        with self.lock:
            try:
                result = method(actor, **args)
            except TableRuling as ruling:
                self.table.log.append("refused", actor, verb=verb, reason=str(ruling))
                return {"refused": str(ruling)}
            except TypeError as bad_args:
                return {"refused": f"Wrong arguments for {verb}: {bad_args}"}
            except TimeoutError:
                return {"refused": f"{verb} was sent but the engine did not answer. "
                                   f"It may not have applied."}
            self.table.pump()
        return {"ok": True, "result": result}

    def state_for(self, actor: str) -> dict:
        """What this actor can see.

        Sheets come from the server; the enemy roster is derived from the event
        log rather than kept as a second copy, so it cannot disagree with what
        the engine actually did.
        """
        with self.lock:
            self.table.pump()
            characters = self.table.state().get("characters", {})
            enemies = self._enemy_roster()
            beat = self.table.log.beat
            recent = [e.to_dict() for e in list(self.table.log)[-12:]]
        return {
            "you": characters.get(actor),
            "everyone": {k: {"conditions": v.get("conditions"),
                             "endurance_current": v.get("endurance_current"),
                             "endurance_max": v.get("endurance_max"),
                             "sparks": v.get("sparks")}
                         for k, v in characters.items()},
            "active_enemies": enemies,
            "beat": beat,
            "recent": recent,
        }

    def _enemy_roster(self) -> dict:
        """Live enemies, replayed from the log the engine wrote."""
        roster: dict[str, dict] = {}
        for event in self.table.log:
            d = event.data
            if event.kind == "enemy_spawned":
                enemy = d.get("enemy") or {}
                roster[d["tracker_key"]] = {
                    "name": enemy.get("name"), "tier": enemy.get("tier"),
                    "resolve": enemy.get("resolve"), "armor": enemy.get("armor"),
                    "tr": d.get("tr"),
                }
            elif event.kind == "enemy_updated" and d["tracker_key"] in roster:
                if d.get("defeated") or d.get("mook_removed"):
                    roster.pop(d["tracker_key"], None)
                else:
                    roster[d["tracker_key"]]["resolve"] = d.get("resolve_current")
            elif event.kind == "enemy_removed":
                roster.pop(d.get("tracker_key"), None)
            elif event.kind == "enemy_phase_change" and d.get("enemy_id") in roster:
                roster[d["enemy_id"]]["phase"] = d.get("description", "").strip()
        return roster

    def finish(self) -> dict:
        """Write the transcript, the log, and the metrics."""
        from tools.agentic_playtest.metrics import compute, summarise
        from tools.agentic_playtest.transcript import render
        from tools.agentic_playtest.validate import find_confabulations

        from app.facets.registry import build_ruleset

        with self.lock:
            self.table.pump()
            log = self.table.log
            report = find_confabulations(log, build_ruleset([]))
            metrics = compute(log, list(self.party))
            transcript = render(log, title="Subagent playtest")

        self.out_dir.mkdir(parents=True, exist_ok=True)
        (self.out_dir / "transcript.md").write_text(transcript, encoding="utf-8")
        log.write(self.out_dir / "events.jsonl")
        (self.out_dir / "metrics.json").write_text(
            json.dumps(metrics.to_dict(), indent=2), encoding="utf-8")
        (self.out_dir / "validation.txt").write_text(str(report), encoding="utf-8")
        return {"validation_ok": report.ok, "validation": str(report),
                "metrics": summarise(metrics), "out_dir": str(self.out_dir)}


class _Handler(BaseHTTPRequestHandler):
    broker: Broker = None  # set on the server instance

    def log_message(self, *args) -> None:  # silence the default access log
        pass

    def _reply(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        broker = self.server.broker
        if self.path.startswith("/state"):
            actor = self.path.partition("actor=")[2] or "MM"
            self._reply(broker.state_for(actor))
        elif self.path == "/transcript":
            from tools.agentic_playtest.transcript import render
            self._reply({"transcript": render(broker.table.log)})
        else:
            self._reply({"error": "unknown path"}, 404)

    def do_POST(self) -> None:
        broker = self.server.broker
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as e:
            self._reply({"refused": f"Malformed JSON: {e}"}, 400)
            return

        if self.path == "/turn":
            self._reply(broker.take_turn(str(payload.get("actor", "")),
                                         str(payload.get("verb", "")),
                                         payload.get("args") or {}))
        elif self.path == "/beat":
            broker.table.log.next_beat()
            self._reply({"ok": True, "beat": broker.table.log.beat})
        elif self.path == "/finish":
            self._reply(broker.finish())
            threading.Thread(target=broker.server.shutdown, daemon=True).start()
        else:
            self._reply({"error": "unknown path"}, 404)


def serve(broker: Broker, port: int = 0) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    server.broker = broker
    broker.server = server
    return server
