"""The event log — the single source of truth for a playtest session.

Every mechanical fact the engine produces is appended here as one event. The
transcript is rendered from this log and the metrics are computed from it, so
there is no path by which the narrative and the mechanics can disagree.

Agent free-text is also logged (as `say` / `say_ooc` events) but is never the
source of a mechanical claim — see validate.py, which fails a run when agent
text asserts a mechanic this log does not contain.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterator


@dataclass
class Event:
    """One thing that happened, in order.

    `beat` groups events into the unit a player experiences as "a turn at the
    table" — the metrics in metrics.py are mostly per-beat, and validate.py
    scopes an agent's mechanical claims to the beat it made them in.
    """

    seq: int
    beat: int
    kind: str
    actor: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


class EventLog:
    """Append-only log of everything that happened in a session."""

    def __init__(self, session_id: str, arm: str = "A", seed: int | None = None) -> None:
        self.session_id = session_id
        self.arm = arm
        self.seed = seed
        self._events: list[Event] = []
        self._beat = 0

    # -- writing ---------------------------------------------------------

    def append(self, kind: str, actor: str, **data: Any) -> Event:
        event = Event(seq=len(self._events), beat=self._beat, kind=kind, actor=actor, data=data)
        self._events.append(event)
        return event

    def next_beat(self) -> int:
        """Advance to the next beat. Returns the new beat number."""
        self._beat += 1
        return self._beat

    # -- reading ---------------------------------------------------------

    @property
    def beat(self) -> int:
        return self._beat

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self) -> Iterator[Event]:
        return iter(self._events)

    def of_kind(self, *kinds: str) -> list[Event]:
        return [e for e in self._events if e.kind in kinds]

    def in_beat(self, beat: int) -> list[Event]:
        return [e for e in self._events if e.beat == beat]

    def by_actor(self, actor: str) -> list[Event]:
        return [e for e in self._events if e.actor == actor]

    # -- persistence -----------------------------------------------------

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "type": "session_header",
                "session_id": self.session_id,
                "arm": self.arm,
                "seed": self.seed,
            }) + "\n")
            for event in self._events:
                fh.write(json.dumps(event.to_dict()) + "\n")

    @classmethod
    def read(cls, path: Path) -> EventLog:
        lines = path.read_text(encoding="utf-8").splitlines()
        header = json.loads(lines[0])
        log = cls(header["session_id"], header.get("arm", "A"), header.get("seed"))
        for line in lines[1:]:
            if not line.strip():
                continue
            d = json.loads(line)
            log._events.append(Event(seq=d["seq"], beat=d["beat"], kind=d["kind"],
                                     actor=d["actor"], data=d["data"]))
        log._beat = max((e.beat for e in log._events), default=0)
        return log
