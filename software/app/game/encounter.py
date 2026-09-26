"""Encounters and the danger read (MM1).

Threat Rating and the encounter budget are gone (L3). An encounter is a list of
foes; the MM gets a *simple danger read* from role counts against the party's
size and level. The read is a rough guide calibrated by `tools/combat_sim.py`
(which drives `combat.py`), not a rule.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

#: Threat points per foe (MM1, Table MM1–4). Mooks are counted in fours
#: (every four, rounded up, is one point) — see `danger_read`.
ROLE_POINTS = {"mook": 0.25, "standard": 1.0, "elite": 2.0, "boss": 4.0}
#: A foe this many levels above the party counts double; this many below, half.
LEVEL_SWING = 3
READ_TEXT = {
    "skirmish": "A skirmish: over quickly, costs little.",
    "fight": "A real fight: a few exchanges, and someone gets hurt.",
    "hard": "Hard: someone may go down; expect Wounds and spent resources.",
    "deadly": "Deadly: someone probably goes down. Give them a way out.",
}


@dataclass
class EncounterEnemy:
    enemy_id: str
    count: int = 1

    def to_dict(self) -> dict:
        return {"enemy_id": self.enemy_id, "count": self.count}


@dataclass
class Encounter:
    id: str
    name: str
    environment: str = ""
    description: str = ""
    enemies: list[EncounterEnemy] = field(default_factory=list)
    lateral_solutions: list[str] = field(default_factory=list)
    rewards_sparks: int = 0
    rewards_narrative: str = ""
    notes: str = ""

    def roster(self, library: dict) -> list[tuple[str, int, int]]:
        """[(role, level, count)] for the foes found in `library` ({id: Enemy})."""
        out = []
        for ee in self.enemies:
            e = library.get(ee.enemy_id)
            if e is not None:
                out.append((e.role, e.level, ee.count))
        return out

    def missing(self, library: dict) -> list[str]:
        return sorted({ee.enemy_id for ee in self.enemies if ee.enemy_id not in library})

    def danger(self, library: dict, party_size: int, party_level: int) -> dict:
        return danger_read(self.roster(library), party_size, party_level)

    def to_client_dict(self) -> dict:
        return {
            "id": self.id, "name": self.name, "environment": self.environment,
            "description": self.description, "enemies": [e.to_dict() for e in self.enemies],
            "lateral_solutions": list(self.lateral_solutions),
            "rewards_sparks": self.rewards_sparks, "rewards_narrative": self.rewards_narrative,
            "notes": self.notes,
        }


def level_multiplier(level: int, party_level: int) -> float:
    """×2 for a foe 3+ levels above the party, ×½ for 3+ below, else ×1."""
    if level - party_level >= LEVEL_SWING:
        return 2.0
    if party_level - level >= LEVEL_SWING:
        return 0.5
    return 1.0


def foe_points(role: str, level: int, party_level: int) -> float:
    """One foe's threat points: Standard 1, Elite 2, Boss 4 (a lone Mook a
    quarter — mobs are rounded up per four in `danger_read`), with the level
    multiplier."""
    if role not in ROLE_POINTS:
        raise ValueError(f"Unknown role {role!r}.")
    return ROLE_POINTS[role] * level_multiplier(level, party_level)


def danger_read(roster: Iterable[tuple[str, int, int]], party_size: int,
                party_level: int) -> dict:
    """The danger read (MM1, Table MM1–4): total threat points against party size.

    Mooks count one point per four (rounded up). Under two-thirds of the
    party size is a skirmish; up to one per character a
    real fight; up to one and a half per character hard; above that deadly.

    Args:
        roster: (role, level, count) per entry.
        party_size: characters in the fight (>= 1).
        party_level: their typical level (1-10).

    Returns:
        {"read": skirmish|fight|hard|deadly, "points", "per_pc", "text", "counts"}
    Raises:
        ValueError: party_size < 1, a negative count or an unknown role.
    """
    if party_size < 1:
        raise ValueError("A party has at least one character.")
    import math
    points = 0.0
    counts: dict[str, int] = {}
    mooks_by_mult: dict[float, int] = {}
    for role, level, count in roster:
        if count < 0:
            raise ValueError("Counts cannot be negative.")
        if role not in ROLE_POINTS:
            raise ValueError(f"Unknown role {role!r}.")
        counts[role] = counts.get(role, 0) + count
        mult = level_multiplier(level, party_level)
        if role == "mook":
            mooks_by_mult[mult] = mooks_by_mult.get(mult, 0) + count
        else:
            points += ROLE_POINTS[role] * mult * count
    for mult, n in mooks_by_mult.items():
        points += math.ceil(n / 4) * mult          # every four Mooks, rounded up
    per_pc = points / party_size
    if points < party_size * 2 / 3:
        read = "skirmish"
    elif points <= party_size:
        read = "fight"
    elif points <= party_size * 1.5:
        read = "hard"
    else:
        read = "deadly"
    return {"read": read, "points": round(points, 2), "per_pc": round(per_pc, 2),
            "text": READ_TEXT[read], "counts": counts}
