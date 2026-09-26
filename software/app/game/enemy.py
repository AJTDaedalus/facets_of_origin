"""Monster cards (MM1, DESIGN §1 "Monsters" and §3.4).

One dial (level 1-10) and a role set a foe's HP, damage, attack and number of
attacks from `monsters.level_table` and `monsters.roles`. Overrides on the card
are final values (not modifiers) and are flagged so the Bestiary can print a †.
The card carries the texture: WANTS · SPECIAL · WHEN BLOODIED · TELLS · BREAKS ·
TWISTS (d6) · NASTIER.

An `Enemy` is also the live tracker entry: `spawn()` returns a copy with HP set,
and for a Mook mob `count` is the number of Mooks still standing.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Optional

FOF_VERSION = "1.0"
ROLES = ("mook", "standard", "elite", "boss")
OVERRIDE_FIELDS = ("hp", "damage", "attack", "attacks")
CARD_TEXT_FIELDS = ("weapon", "wants", "special", "when_bloodied", "tells", "breaks",
                    "nastier", "description", "notes")


class EnemyFormatError(ValueError):
    """An enemy file that cannot be read as a v1.0 card."""


@dataclass
class Enemy:
    id: str
    name: str
    level: int
    role: str = "standard"
    armor: int = 0
    morale: int = 7
    weapon: str = ""
    hp_override: Optional[int] = None
    damage_override: Optional[int] = None
    attack_override: Optional[int] = None
    attacks_override: Optional[int] = None
    wants: str = ""
    special: str = ""
    when_bloodied: Optional[str] = None
    tells: str = ""
    breaks: str = ""
    twists: list[str] = field(default_factory=list)
    nastier: Optional[str] = None
    description: str = ""
    notes: str = ""
    reskin_of: Optional[str] = None
    # --- live state (tracker)
    hp_current: Optional[int] = None
    count: int = 1
    bloodied: bool = False
    defeated: bool = False
    broken: bool = False
    phase: int = 1
    key: Optional[str] = None
    openings: list[str] = field(default_factory=list)   # names whose next attack is Easy
    studied: bool = False

    # ------------------------------------------------------------ derived
    def _row(self, ruleset):
        return ruleset.monsters.row(self.level)

    def _role(self, ruleset):
        role = ruleset.monsters.roles.get(self.role)
        if role is None:
            raise ValueError(f"Unknown role {self.role!r}.")
        return role

    @property
    def is_mook(self) -> bool:
        return self.role == "mook"

    def hp_max(self, ruleset) -> Optional[int]:
        """Level HP × role multiplier; None for a Mook (drops to any hit)."""
        role = self._role(ruleset)
        if role.hp_mult is None:
            return None
        if self.hp_override is not None:
            return self.hp_override
        return self._row(ruleset).hp * role.hp_mult

    def damage(self, ruleset) -> int:
        if self.damage_override is not None:
            return self.damage_override
        return max(1, self._row(ruleset).damage + self._role(ruleset).damage_mod)

    def attack(self, ruleset) -> int:
        if self.attack_override is not None:
            return self.attack_override
        return self._row(ruleset).attack + self._role(ruleset).attack_mod

    def attacks(self, ruleset) -> int:
        if self.attacks_override is not None:
            return self.attacks_override
        return self._role(ruleset).attacks

    def overridden(self) -> list[str]:
        """Which derived numbers the card overrides (the Bestiary prints a †)."""
        return [f for f in OVERRIDE_FIELDS if getattr(self, f"{f}_override") is not None]

    def validate(self, ruleset) -> list[str]:
        errors = []
        if self.role not in ruleset.monsters.roles:
            errors.append(f"{self.id}: unknown role {self.role!r}.")
        if not 1 <= self.level <= len(ruleset.monsters.level_table):
            errors.append(f"{self.id}: level {self.level} is off the level table.")
        lo, hi = ruleset.monsters.armor_range
        if not lo <= self.armor <= hi:
            errors.append(f"{self.id}: armor {self.armor} is outside {lo}-{hi}.")
        if not 2 <= self.morale <= 12:
            errors.append(f"{self.id}: morale {self.morale} is outside 2-12.")
        if len(self.twists) != 6:
            errors.append(f"{self.id}: a card has exactly six twists, not {len(self.twists)}.")
        for f_ in ("wants", "special", "tells", "breaks"):
            if not (getattr(self, f_) or "").strip():
                errors.append(f"{self.id}: the card has no {f_.upper()}.")
        if self.role != "mook" and not (self.when_bloodied or "").strip():
            errors.append(f"{self.id}: a {self.role} needs a WHEN BLOODIED line.")
        if self.count < 1:
            errors.append(f"{self.id}: count must be at least 1.")
        return errors

    def card(self, ruleset) -> dict:
        """The derived numbers the MM builds from (the card preview)."""
        role = self._role(ruleset)
        return {
            "level": self.level, "role": self.role, "hp": self.hp_max(ruleset),
            "damage": self.damage(ruleset), "attack": self.attack(ruleset),
            "attacks": self.attacks(ruleset), "armor": self.armor, "morale": self.morale,
            "mob": role.mob, "mob_damage_per_extra": role.mob_damage_per_extra,
            "mob_damage_cap": role.mob_damage_cap, "bloodied_phase": role.bloodied_phase,
            "overrides": self.overridden(),
            "fearless": self.morale >= ruleset.monsters.morale.fearless,
        }

    # ------------------------------------------------------------ live
    def spawn(self, ruleset, count: int = 1, key: Optional[str] = None) -> "Enemy":
        """A fresh tracker copy at full HP (for a Mook mob, `count` Mooks)."""
        if count < 1:
            raise ValueError("Spawn at least one.")
        if count > 1 and not self.is_mook:
            raise ValueError("Only Mooks spawn as a mob; spawn others one at a time.")
        live = copy.deepcopy(self)
        live.hp_current = self.hp_max(ruleset)
        live.count = count
        live.bloodied = live.defeated = live.broken = False
        live.phase = 1
        live.openings = []
        live.studied = False
        live.key = key or self.id
        return live

    # ------------------------------------------------------------ serialise
    def to_fof(self, module_refs: Optional[list[dict]] = None) -> dict:
        body: dict[str, Any] = {"level": self.level, "role": self.role, "armor": self.armor,
                                "morale": self.morale}
        for f_ in OVERRIDE_FIELDS:
            v = getattr(self, f"{f_}_override")
            if v is not None:
                body[f_] = v
        body["weapon"] = self.weapon
        for f_ in ("wants", "special", "when_bloodied", "tells", "breaks"):
            body[f_] = getattr(self, f_)
        body["twists"] = list(self.twists)
        if self.nastier:
            body["nastier"] = self.nastier
        body["description"] = self.description
        body["notes"] = self.notes
        body["reskin_of"] = self.reskin_of
        return {
            "fof_version": FOF_VERSION, "type": "enemy", "id": self.id, "name": self.name,
            "ruleset": {"modules": module_refs or [{"id": "base", "version": "1.0.0"}]},
            "enemy": body,
        }

    @classmethod
    def from_fof(cls, fof: dict) -> "Enemy":
        """Read an enemy card. A v0.3 file (tier/Resolve/TR) fails with a clear message."""
        if not isinstance(fof, dict) or fof.get("type") != "enemy":
            raise EnemyFormatError("Not an enemy file (type: enemy).")
        e = fof.get("enemy")
        if not isinstance(e, dict):
            raise EnemyFormatError(f"{fof.get('id')}: no `enemy:` block.")
        if "tier" in e or "resolve" in e or str(fof.get("fof_version")) != FOF_VERSION:
            raise EnemyFormatError(
                f"{fof.get('id')}: this enemy uses the retired v0.3 format (tier, Resolve, "
                "Threat Rating). v1.0 cards have a level and a role (MM1).")
        if "level" not in e:
            raise EnemyFormatError(f"{fof.get('id')}: a card needs a level.")
        return cls(
            id=fof["id"], name=fof.get("name") or fof["id"], level=int(e["level"]),
            role=e.get("role", "standard"), armor=int(e.get("armor", 0) or 0),
            morale=int(e.get("morale", 7) or 7), weapon=e.get("weapon") or "",
            hp_override=e.get("hp"), damage_override=e.get("damage"),
            attack_override=e.get("attack"), attacks_override=e.get("attacks"),
            wants=_text(e.get("wants")), special=_text(e.get("special")),
            when_bloodied=e.get("when_bloodied"), tells=_text(e.get("tells")),
            breaks=_text(e.get("breaks")), twists=[str(t) for t in e.get("twists") or []],
            nastier=e.get("nastier"), description=_text(e.get("description")),
            notes=_text(e.get("notes")), reskin_of=e.get("reskin_of"),
        )

    def to_client_dict(self, ruleset=None) -> dict:
        d = {
            "id": self.id, "key": self.key or self.id, "name": self.name, "level": self.level,
            "role": self.role, "armor": self.armor, "morale": self.morale, "weapon": self.weapon,
            "wants": self.wants, "special": self.special, "when_bloodied": self.when_bloodied,
            "tells": self.tells, "breaks": self.breaks, "twists": list(self.twists),
            "nastier": self.nastier, "description": self.description, "notes": self.notes,
            "reskin_of": self.reskin_of,
            "overrides": {f_: getattr(self, f"{f_}_override") for f_ in OVERRIDE_FIELDS
                          if getattr(self, f"{f_}_override") is not None},
            "hp_current": self.hp_current, "count": self.count, "bloodied": self.bloodied,
            "defeated": self.defeated, "broken": self.broken, "phase": self.phase,
            "openings": list(self.openings), "studied": self.studied,
        }
        if ruleset is not None:
            d["card"] = self.card(ruleset)
        return d


def _text(v) -> str:
    return "" if v is None else str(v)
