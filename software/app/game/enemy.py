"""Enemy model — stat blocks, TR calculation, and .fof serialization."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


EnemyTier = Literal["mook", "named", "boss"]


class Enemy(BaseModel):
    """An enemy stat block for use in encounters and the combat tracker.

    Mirrors the enemy .fof format defined in MM1: Encounters & Enemies.
    """

    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=128)
    tier: EnemyTier = "mook"
    endurance: int = Field(default=0, ge=0)
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

    # Combat tracker state (ephemeral, not saved to .fof)
    endurance_current: Optional[int] = None
    conditions: list[str] = Field(default_factory=list)

    def calculate_tr(self) -> int:
        """Calculate Threat Rating using the MM1 formula.

        TR = offense_value + durability_value + armor_bonus + technique_bonus

        Offense: attack_modifier mapped: -2->0, -1->1, 0->2, +1->3, +2->4, +3->5, +4->6
        Durability: Mook=0, Named by Endurance, Boss by Endurance
        Armor: none=0, light=1, heavy=2
        Techniques: 1 per technique (simplified)
        """
        # Offense value
        offense = max(0, self.attack_modifier + 2)

        # Durability value
        if self.tier == "mook":
            durability = 0
        elif self.endurance <= 2:
            durability = 1
        elif self.endurance <= 4:
            durability = 2
        elif self.endurance <= 6:
            durability = 3
        elif self.endurance <= 8:
            durability = 4
        elif self.endurance <= 10:
            durability = 5
        elif self.endurance <= 12:
            durability = 6
        else:
            durability = 7

        # Armor bonus
        armor_bonus = {"none": 0, "light": 1, "heavy": 2}.get(self.armor, 0)

        # Technique bonus (1 per technique)
        technique_bonus = len(self.techniques)

        raw_tr = offense + durability + armor_bonus + technique_bonus

        # Enforce tier minimums
        minimums = {"mook": 1, "named": 8, "boss": 12}
        return max(raw_tr, minimums.get(self.tier, 1))

    def init_combat(self) -> None:
        """Initialize combat tracker state."""
        self.endurance_current = self.endurance if self.tier != "mook" else 0
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
            enemy_block["endurance"] = self.endurance
        if self.tactics:
            enemy_block["tactics"] = self.tactics
        if self.personality:
            enemy_block["personality"] = self.personality
        if self.loot:
            enemy_block["loot"] = list(self.loot)

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

        return cls(
            id=fof_dict.get("id", "unknown"),
            name=fof_dict.get("name", "Unknown Enemy"),
            tier=enemy_block.get("tier", "mook"),
            endurance=enemy_block.get("endurance", 0),
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
        )
