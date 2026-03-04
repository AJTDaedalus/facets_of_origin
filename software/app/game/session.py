"""Game session management — in-memory with JSON persistence."""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings
from app.game.character import Character
from app.facets.registry import MergedRuleset, build_ruleset


@dataclass
class GameSession:
    id: str
    name: str
    created_at: datetime
    active_facet_ids: list[str]
    ruleset: MergedRuleset
    characters: dict[str, Character] = field(default_factory=dict)  # keyed by player_name
    used_invite_tokens: set[str] = field(default_factory=set)
    roll_log: list[dict] = field(default_factory=list)

    def add_character(self, character: Character) -> None:
        self.characters[character.player_name] = character

    def record_roll(self, player_name: str, roll_dict: dict) -> None:
        self.roll_log.append({
            "player_name": player_name,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            **roll_dict,
        })

    def to_state_dict(self) -> dict:
        """Full session state — sent to MM on join."""
        return {
            "session_id": self.id,
            "session_name": self.name,
            "characters": {pn: c.to_client_dict() for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],  # last 50 rolls only
        }

    def to_player_state_dict(self, player_name: str) -> dict:
        """Session state sent to a specific player."""
        character = self.characters.get(player_name)
        return {
            "session_id": self.id,
            "session_name": self.name,
            "your_character": character.to_client_dict() if character else None,
            "all_characters": {pn: c.to_client_dict() for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],
        }


class SessionStore:
    """In-memory session store with JSON persistence."""

    def __init__(self) -> None:
        self._sessions: dict[str, GameSession] = {}
        self._persistence_dir = settings.data_dir / "sessions"
        self._persistence_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, name: str, active_facet_ids: list[str] | None = None) -> GameSession:
        session_id = str(uuid.uuid4())
        ruleset = build_ruleset(active_facet_ids or [])

        session = GameSession(
            id=session_id,
            name=name,
            created_at=datetime.now(tz=timezone.utc),
            active_facet_ids=active_facet_ids or [],
            ruleset=ruleset,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> GameSession | None:
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[dict]:
        return [
            {
                "id": s.id,
                "name": s.name,
                "created_at": s.created_at.isoformat(),
                "player_count": len(s.characters),
            }
            for s in self._sessions.values()
        ]

    def mark_invite_used(self, session_id: str, token: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.used_invite_tokens.add(token)

    def is_invite_used(self, session_id: str, token: str) -> bool:
        session = self._sessions.get(session_id)
        return session is not None and token in session.used_invite_tokens


# Singleton store
session_store = SessionStore()
