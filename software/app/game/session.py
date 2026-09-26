"""Game session management — in-memory with JSON persistence planned."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from app.config import settings
from app.game.character import Character
from app.game.combat import CombatState
from app.game.enemy import Enemy
from app.game.encounter import Encounter, danger_read
from app.facets.registry import MergedRuleset, build_ruleset


@dataclass
class ThreatClock:
    """A visible-to-the-table pressure clock (PHB III.2, D4).

    Advances on qualifying outcome tiers (default: partial_success, failure —
    see `facet.yaml` `hazards.threat_clock.advances_on`). Winding back is
    always unconditional and never itself advances the clock (Brain, BRIEF
    §EF4) — there is no roll involved in `wind_back`.
    """

    id: str
    name: str
    segments: int
    filled_segments: int = 0

    @property
    def is_full(self) -> bool:
        return self.filled_segments >= self.segments

    def advance(self) -> bool:
        """Fill one segment. Returns True only on the advance that fills the clock."""
        was_full = self.is_full
        if not was_full:
            self.filled_segments = min(self.segments, self.filled_segments + 1)
        return self.is_full and not was_full

    def wind_back(self) -> None:
        """Empty one segment. Unconditional — no roll."""
        self.filled_segments = max(0, self.filled_segments - 1)

    def to_client_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "segments": self.segments,
            "filled_segments": self.filled_segments,
            "is_full": self.is_full,
        }


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
    threat_clocks: dict[str, ThreatClock] = field(default_factory=dict)
    #: Live combat (exchange number, exposures, defenders, cover); None out of combat.
    combat: CombatState | None = None
    #: Sessions played so far (drives the default level pacing).
    session_number: int = 1
    #: Player names the MM has called a level-up for, awaiting their pick.
    level_up_ready: set[str] = field(default_factory=set)
    #: Per-player Spark-flow tracker (T6.3, C-2 app-side): player_name →
    #: {"last_flow": monotonic ts of the last earn OR spend, "last_nudge":
    #: monotonic ts of the last MM prompt about it, or None}. Feeds the quiet
    #: MM-only `spark_flow_nudge` prompt in the WS layer — a tool prompt,
    #: not a rule (see `SPARK_FLOW_NUDGE_SECONDS` in `app/api/websocket.py`).
    spark_flow: dict[str, dict] = field(default_factory=dict)
    _character_dir: Path | None = field(default=None)

    def add_character(self, character: Character) -> None:
        """Add or replace a character in this session, keyed by player_name."""
        self.characters[character.player_name] = character
        # Joining opens a fresh Spark-flow stretch — the nudge clock starts now.
        self.record_spark_flow(character.player_name)
        self.save_character_to_disk(character.player_name)

    def record_spark_flow(self, player_name: str) -> None:
        """Record a Spark earn or spend (or other stretch reset) for the
        Spark-flow nudge tracker (T6.3). Also clears any pending nudge
        cooldown — a fresh flow starts a fresh stretch.
        """
        self.spark_flow[player_name] = {
            "last_flow": time.monotonic(),
            "last_nudge": None,
        }

    def save_character_to_disk(self, player_name: str) -> None:
        """Write the current character state to data/sessions/{id}/characters/{player_name}.fof.

        Silent no-op if player_name is not in the session or _character_dir is not set.

        Raises:
            IOError: If the write fails (permissions, disk full, etc.).
        """
        character = self.characters.get(player_name)
        if not character or not self._character_dir:
            return
        fof_dict = character.to_fof(self.ruleset.module_refs(), self.id, ruleset=self.ruleset)
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

    def confirm_natural_two_graceful_fail(self, player_name: str, roll_dict: dict) -> bool:
        """III.1, the natural 2: when both kept dice show 1 and the roll
        failed, the Graceful Fail is "confirmed without asking — no judgment
        call, no MM discretion". Awards the Spark and marks the roll.

        The marks go on the roll payload rather than into a separate event so
        the table reads them with the roll that earned them, and so one
        chokepoint carries the rule for every handler. Returns True when it
        fired; the player still narrates.
        """
        if roll_dict.get("outcome") != "failure" or not roll_dict.get("natural_low"):
            return False
        if roll_dict.get("graceful_fail_claimed"):
            return False
        character = self.characters.get(player_name)
        if character is None:
            return False
        character.earn_spark()
        self.record_spark_flow(player_name)
        roll_dict["graceful_fail_claimed"] = True
        roll_dict["graceful_fail_reason"] = "natural_2"
        roll_dict["graceful_fail_sparks_now"] = character.sparks
        return True

    # ------------------------------------------------------------ combat
    def start_combat(self) -> CombatState:
        """Begin a fight: exchange 1, a fresh scene for talent uses."""
        self.combat = CombatState()
        for c in self.characters.values():
            c.reset_uses(self.ruleset, "scene")
        return self.combat

    def end_combat(self) -> None:
        self.combat = None

    def end_exchange(self) -> int:
        """Exchange effects expire (exposure, Defend, cover, stunt openings,
        Studied Foe). A natural-2 opening (named for its target) lasts until used."""
        if self.combat is None:
            raise ValueError("No fight is running.")
        from app.game.combat import expire_exchange_effects
        for e in self.active_enemies.values():
            expire_exchange_effects(e)
        return self.combat.end_exchange()

    def party_size(self) -> int:
        return max(1, sum(1 for c in self.characters.values() if c.status != "dead"))

    def party_level(self) -> int:
        """The party's typical (median, rounded down) level; 1 with nobody present."""
        levels = sorted(c.level for c in self.characters.values())
        return levels[(len(levels) - 1) // 2] if levels else 1

    def active_danger(self) -> dict:
        """Danger read of the live tracker (foes still standing)."""
        roster = [(e.role, e.level, e.count if e.is_mook else 1)
                  for e in self.active_enemies.values() if not e.defeated and not e.broken]
        return danger_read(roster, self.party_size(), self.party_level())

    # ------------------------------------------------------------ session end
    def end_session_prompts(self) -> dict:
        """The five level-up prompts and the default pacing hint for the MM."""
        adv = self.ruleset.advancement
        suggested = [p.level for p in adv.pacing if p.after_session == self.session_number]
        return {
            "session_number": self.session_number,
            "prompts": [p.model_dump() for p in adv.prompts],
            "pacing_suggests_level": suggested[0] if suggested else None,
        }

    def call_level_up(self, player_names: list[str] | None = None) -> list[str]:
        """The MM calls a level-up (for everyone, or the named players)."""
        names = list(self.characters) if player_names is None else player_names
        unknown = [n for n in names if n not in self.characters]
        if unknown:
            raise ValueError(f"No such character(s): {', '.join(unknown)}.")
        ready = [n for n in names
                 if self.characters[n].level < self.ruleset.advancement.max_level]
        self.level_up_ready.update(ready)
        return ready

    def next_session(self) -> int:
        """Start the next session: Sparks reset (no carry-over), session uses refresh."""
        self.session_number += 1
        for c in self.characters.values():
            c.start_session(self.ruleset)
        return self.session_number

    def to_state_dict(self) -> dict:
        """Full session state sent to the MM on WebSocket join.

        Returns the most recent 50 rolls to keep the payload manageable.
        Includes enemy/encounter libraries and active enemies for the MM's
        Builder and Play Field tabs.
        """
        return {
            "session_id": self.id,
            "session_name": self.name,
            "all_characters": {pn: c.to_client_dict(self.ruleset) for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],
            "enemy_library": {eid: e.to_client_dict(self.ruleset) for eid, e in self.enemy_library.items()},
            "encounter_library": {eid: e.to_client_dict() for eid, e in self.encounter_library.items()},
            "active_enemies": {key: e.to_client_dict(self.ruleset) for key, e in self.active_enemies.items()},
            "threat_clocks": {cid: c.to_client_dict() for cid, c in self.threat_clocks.items()},
            "combat": self.combat.to_dict() if self.combat else None,
            "session_number": self.session_number,
            "level_up_ready": sorted(self.level_up_ready),
            # MM dial only: deliberately absent from the player state.
            "danger": self.active_danger(),
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
            "your_character": character.to_client_dict(self.ruleset) if character else None,
            "all_characters": {pn: c.to_client_dict(self.ruleset) for pn, c in self.characters.items()},
            "ruleset": self.ruleset.to_client_dict(),
            "roll_log": self.roll_log[-50:],
            "active_enemies": {key: _player_enemy_view(e, self.ruleset)
                               for key, e in self.active_enemies.items()},
            "threat_clocks": {cid: c.to_client_dict() for cid, c in self.threat_clocks.items()},
            "combat": self.combat.to_dict() if self.combat else None,
            "level_up_ready": player_name in self.level_up_ready,
        }


def _player_enemy_view(enemy: Enemy, ruleset) -> dict:
    """What players see of a foe: name, level, role, state — not the card's secrets."""
    return {"key": enemy.key or enemy.id, "id": enemy.id, "name": enemy.name,
            "level": enemy.level, "role": enemy.role, "count": enemy.count,
            "bloodied": enemy.bloodied, "defeated": enemy.defeated, "broken": enemy.broken}


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

    def delete_session(self, session_id: str) -> bool:
        """Drop a session from the store. Returns False if it was not there.

        Only the in-memory session goes; anything already written under
        `data/` is left alone, so a deletion cannot destroy exported character
        files the MM may still want.
        """
        return self._sessions.pop(session_id, None) is not None

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
