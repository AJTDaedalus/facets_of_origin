"""Enemy model — stat blocks, TR calculation, and .fof serialization."""
from __future__ import annotations

import warnings
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


EnemyTier = Literal["mook", "named", "boss"]

# v0.1 -> v0.2 migration map (DESIGN §4.1): resolve := old durability_value.
_LEGACY_ENDURANCE_TO_RESOLVE = [
    (2, 1), (4, 2), (6, 3), (8, 4), (10, 5), (12, 6),
]


def _map_legacy_endurance_to_resolve(endurance: int) -> int:
    for ceiling, resolve in _LEGACY_ENDURANCE_TO_RESOLVE:
        if endurance <= ceiling:
            return resolve
    return 7


class PhaseDef(BaseModel):
    """A durability-threshold phase change (DESIGN §4.1)."""

    resolve_threshold: int = Field(ge=0)
    description: str = ""


class Enemy(BaseModel):
    """An enemy stat block for use in encounters and the combat tracker.

    Mirrors the enemy .fof format defined in MM1: Encounters & Enemies.
    """

    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=128)
    tier: EnemyTier = "mook"
    resolve: int = Field(default=0, ge=0)
    attack_modifier: int = 0
    defense_modifier: int = 0
    armor: str = "none"  # "none" | "light" | "heavy"
    techniques: list[str] = Field(default_factory=list)
    special: Optional[str] = None
    description: str = ""
    tactics: str = ""
    personality: str = ""
    loot: list[str] = Field(default_factory=list)
    notes: str = ""
    phases: list[PhaseDef] = Field(default_factory=list)

    # Combat tracker state (ephemeral, not saved to .fof)
    resolve_current: Optional[int] = None
    conditions: list[str] = Field(default_factory=list)

    def calculate_tr(self) -> int:
        """Calculate Threat Rating using the MM1 formula.

        TR = offense_value + durability_value + armor_bonus + technique_bonus

        Offense: attack_modifier mapped: -2->0, -1->1, 0->2, +1->3, +2->4, +3->5, +4->6
        Durability: Mook=0, else = Resolve
        Armor: none=0, light=1, heavy=2
        Techniques: 1 per technique (simplified)
        """
        # Offense value
        offense = max(0, self.attack_modifier + 2)

        # Durability value
        durability = 0 if self.tier == "mook" else self.resolve

        # Armor bonus
        armor_bonus = {"none": 0, "light": 1, "heavy": 2}.get(self.armor, 0)

        # Technique bonus (1 per technique)
        technique_bonus = len(self.techniques)

        raw_tr = offense + durability + armor_bonus + technique_bonus

        # Enforce tier minimums
        minimums = {"mook": 1, "named": 8, "boss": 12}
        return max(raw_tr, minimums.get(self.tier, 1))

    def init_combat(self) -> None:
        """Initialize combat tracker state.

        Armor grants a flat Resolve bonus at combat start (D1) — the same
        `armor_bonus` value `calculate_tr()` adds as a separate TR term,
        applied here to the actual fight pool. Mooks have no Resolve pool.
        """
        if self.tier == "mook":
            self.resolve_current = 0
        else:
            armor_bonus = {"none": 0, "light": 1, "heavy": 2}.get(self.armor, 0)
            self.resolve_current = self.resolve + armor_bonus
        self.conditions = []

    def to_client_dict(self) -> dict:
        """Serialize for sending to clients."""
        return self.model_dump()

    def to_fof(self) -> dict:
        """Serialize to .fof format."""
        now = datetime.now(tz=timezone.utc).isoformat()
        enemy_block: dict = {
            "tier": self.tier,
            "attack_modifier": self.attack_modifier,
            "defense_modifier": self.defense_modifier,
            "armor": self.armor,
            "techniques": list(self.techniques),
            "special": self.special,
            "tr": self.calculate_tr(),
            "description": self.description,
            "notes": self.notes,
        }
        if self.tier != "mook":
            enemy_block["resolve"] = self.resolve
        if self.tactics:
            enemy_block["tactics"] = self.tactics
        if self.personality:
            enemy_block["personality"] = self.personality
        if self.loot:
            enemy_block["loot"] = list(self.loot)
        if self.phases:
            enemy_block["phases"] = [p.model_dump() for p in self.phases]

        return {
            "fof_version": "0.1",
            "type": "enemy",
            "id": self.id,
            "name": self.name,
            "ruleset": {"modules": [{"id": "base", "version": "0.1.0"}]},
            "enemy": enemy_block,
            "created_at": now,
            "last_modified": now,
        }

    @classmethod
    def from_fof(cls, fof_dict: dict) -> "Enemy":
        """Deserialize from a .fof format dict."""
        if fof_dict.get("type") != "enemy":
            raise ValueError(
                f"Expected type 'enemy', got {fof_dict.get('type')!r}."
            )
        enemy_block = fof_dict.get("enemy")
        if not isinstance(enemy_block, dict):
            raise ValueError("Missing or invalid 'enemy' block in FOF file.")

        if "resolve" in enemy_block:
            resolve = enemy_block["resolve"]
        elif "endurance" in enemy_block:
            warnings.warn(
                "Enemy .fof uses the legacy 'endurance' key; migrate to "
                "'resolve' (DESIGN §4.1). Support for 'endurance' will be "
                "removed in v0.4.",
                DeprecationWarning,
                stacklevel=2,
            )
            resolve = _map_legacy_endurance_to_resolve(enemy_block["endurance"])
        else:
            resolve = 0

        return cls(
            id=fof_dict.get("id", "unknown"),
            name=fof_dict.get("name", "Unknown Enemy"),
            tier=enemy_block.get("tier", "mook"),
            resolve=resolve,
            attack_modifier=enemy_block.get("attack_modifier", 0),
            defense_modifier=enemy_block.get("defense_modifier", 0),
            armor=enemy_block.get("armor", "none"),
            techniques=enemy_block.get("techniques") or [],
            special=enemy_block.get("special"),
            description=enemy_block.get("description", ""),
            tactics=enemy_block.get("tactics", ""),
            personality=enemy_block.get("personality", ""),
            loot=enemy_block.get("loot") or [],
            notes=enemy_block.get("notes", ""),
            phases=enemy_block.get("phases") or [],
        )
