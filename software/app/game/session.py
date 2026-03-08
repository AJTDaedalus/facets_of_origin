"""Game session management — in-memory with JSON persistence planned."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from app.config import settings
from app.game.character import Character
from app.game.enemy import Enemy
from app.game.encounter import Encounter
from app.facets.registry import MergedRuleset, build_ruleset


@dataclass
class GameSession:
    """A single game session: one ruleset, one roll log, any number of characters.

    Attributes:
        id: UUID string — uniquely identifies the session.
        name: Human-readable session or campaign name.
        created_at: UTC timestamp of session creation.
        active_facet_ids: List of optional Facet module IDs loaded for this session.
        ruleset: The fully merged and validated ruleset for this session.
        characters: Active player characters keyed by player_name.
        used_invite_tokens: JWT strings that have already been redeemed (single-use enforcement).
        roll_log: Chronological list of resolved rolls (unbounded; capped at 50 on read).
        _character_dir: Directory where per-character .fof files are written on save.
    """

    id: str
    name: str
    created_at: datetime
    active_facet_ids: list[str]
    ruleset: MergedRuleset
    characters: dict[str, Character] = field(default_factory=dict)
    used_invite_tokens: set[str] = field(default_factory=set)
    roll_log: list[dict] = field(default_factory=list)
    enemy_library: dict[str, Enemy] = field(default_factory=dict)
    encounter_library: dict[str, Encounter] = field(default_factory=dict)
    active_enemies: dict[str, Enemy] = field(default_factory=dict)
    _character_dir: Path | None = field(default=None)

    def add_character(self, character: Character) -> None:
        """Add or replace a character in this session, keyed by player_name."""
        self.characters[character.player_name] = character
        self.save_character_to_disk(character.player_name)

    def save_character_to_disk(self, player_name: str) -> None:
        """Write the current character state to data/sessions/{id}/characters/{player_name}.fof.

        Silent no-op if player_name is not in the session or _character_dir is not set.

        Raises:
            IOError: If the write fails (permissions, disk full, etc.).
        """
        character = self.characters.get(player_name)
        if not character or not self._character_dir:
            return
        module_refs = [{"id": f.id, "version": f.version} for f in self.ruleset._files]
        fof_dict = character.to_fof(module_refs, self.id)
        path = self._character_dir / f"{player_name}.fof"
        try:
            path.write_text(yaml.dump(fof_dict, allow_unicode=True, sort_keys=False), encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to save character '{player_name}': {e}") from e

    def record_roll(self, player_name: str, roll_dict: dict) -> None:
        """Append a resolved roll to the session roll log with timestamp and player."""
        self.roll_log.append({
            "player_name": player_name,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            **roll_dict,
        })
        if len(self.roll_log) > 500:
            self.roll_log = self.roll_log[-500:]

    def to_state_dict(self) -> dict:
        """Full session state sent to the MM on WebSocket join.

        Returns the most recent 50 rolls to keep the payload manageable.
        Includes enemy/encounter libraries and active enemies for the MM's
        Builder and Play Field tabs.
        """
        return {
            "session_id": self.id,
            "session_name": self.name,
            "all_characters": {pn: c.to_client_dict() for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],
            "enemy_library": {eid: e.to_client_dict() for eid, e in self.enemy_library.items()},
            "encounter_library": {eid: e.to_client_dict() for eid, e in self.encounter_library.items()},
            "active_enemies": {key: e.to_client_dict() for key, e in self.active_enemies.items()},
        }

    def to_player_state_dict(self, player_name: str) -> dict:
        """Session state sent to a specific player on WebSocket join.

        Includes the player's own character separately as 'your_character' for
        easy access, plus all characters for the player list panel and active
        enemies for combat awareness.
        """
        character = self.characters.get(player_name)
        return {
            "session_id": self.id,
            "session_name": self.name,
            "your_character": character.to_client_dict() if character else None,
            "all_characters": {pn: c.to_client_dict() for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],
            "active_enemies": {key: e.to_client_dict() for key, e in self.active_enemies.items()},
        }


class SessionStore:
    """In-memory session store. All state is lost on server restart.

    Persistence (SQLite) is planned for v0.2. Until then, the MM should not
    restart the server during an active session.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, GameSession] = {}
        self._persistence_dir = settings.data_dir / "sessions"
        self._persistence_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, name: str, active_facet_ids: list[str] | None = None) -> GameSession:
        """Create a new session, load its ruleset, and register it.

        Args:
            name: Human-readable session name.
            active_facet_ids: Optional list of additional Facet module IDs to load.

        Returns:
            The newly created GameSession.

        Raises:
            FacetLoadError: If the ruleset cannot be loaded (e.g., missing base facet).
        """
        session_id = str(uuid.uuid4())
        ruleset = build_ruleset(active_facet_ids or [])

        char_dir = self._persistence_dir / session_id / "characters"
        char_dir.mkdir(parents=True, exist_ok=True)

        session = GameSession(
            id=session_id,
            name=name,
            created_at=datetime.now(tz=timezone.utc),
            active_facet_ids=active_facet_ids or [],
            ruleset=ruleset,
            _character_dir=char_dir,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> GameSession | None:
        """Retrieve a session by ID, or None if not found."""
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[dict]:
        """Return a summary list of all sessions (id, name, created_at, player_count)."""
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
        """Record that an invite token has been consumed.

        No-op if the session does not exist.
        """
        session = self._sessions.get(session_id)
        if session:
            session.used_invite_tokens.add(token)

    def is_invite_used(self, session_id: str, token: str) -> bool:
        """Return True if the invite token has already been redeemed."""
        session = self._sessions.get(session_id)
        return session is not None and token in session.used_invite_tokens


# Singleton store — shared across the entire application process.
session_store = SessionStore()
