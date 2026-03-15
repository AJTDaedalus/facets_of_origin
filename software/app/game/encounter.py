"""Encounter model — enemy groups, TR budget, and action economy."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class EncounterEnemy(BaseModel):
    """An enemy entry in an encounter definition."""

    enemy_id: str
    count: int = Field(default=1, ge=1)


class Encounter(BaseModel):
    """An encounter definition with enemies, difficulty, and TR budget.

    Mirrors the encounter .fof format.
    """

    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=256)
    difficulty: str = "standard"  # skirmish | standard | hard | deadly
    environment: str = ""
    description: str = ""
    enemies: list[EncounterEnemy] = Field(default_factory=list)
    lateral_solutions: list[str] = Field(default_factory=list)
    rewards_sparks: int = Field(default=0, ge=0)
    rewards_narrative: str = ""
    notes: str = ""

    @staticmethod
    def difficulty_multiplier(difficulty: str) -> float:
        """Return the encounter budget multiplier for a difficulty level."""
        return {
            "skirmish": 1.0,
            "standard": 2.0,
            "hard": 3.0,
            "deadly": 4.0,
        }.get(difficulty.lower(), 2.0)

    # Enemy tier weights derived from combat simulation data (Series A-C).
    # Mooks self-cancel as they die; Named maintain pressure; Bosses have
    # phase changes and psychological impact.
    TIER_WEIGHTS: dict[str, float] = {
        "mook": 0.5,
        "named": 1.0,
        "boss": 1.25,
    }

    # Group-size modifier applied after tier weighting.
    @staticmethod
    def group_size_modifier(enemy_count: int) -> float:
        """Modifier for total enemy count — captures action economy pressure."""
        if enemy_count <= 3:
            return 1.0
        elif enemy_count <= 6:
            return 1.1
        else:
            return 1.2

    @staticmethod
    def action_economy_multiplier(enemy_count: int, all_mooks: bool = False) -> float:
        """Return the action economy multiplier based on total enemy count.

        Legacy interface kept for backward compatibility.

        MM1 rules:
        - Solo (1): x0.75
        - Small group (2-3): x1.0
        - Medium group (4-6): x1.25 (Mook-only groups: x1.1 provisional)
        - Large group (7+): x1.5
        """
        if enemy_count <= 1:
            return 0.75
        elif enemy_count <= 3:
            return 1.0
        elif enemy_count <= 6:
            return 1.1 if all_mooks else 1.25
        else:
            return 1.5

    @staticmethod
    def calculate_budget(party_career_advances: int, difficulty: str) -> float:
        """Calculate the encounter TR budget from party strength and difficulty."""
        return party_career_advances * Encounter.difficulty_multiplier(difficulty)

    def total_enemy_count(self) -> int:
        """Total number of individual enemies in this encounter."""
        return sum(entry.count for entry in self.enemies)

    def calculate_effective_tr(
        self,
        enemy_trs: dict[str, int],
        enemy_tiers: dict[str, str] | None = None,
    ) -> float:
        """Calculate effective TR using tier-weighted enemy contributions.

        When *enemy_tiers* is provided the new simulation-calibrated formula
        is used::

            effective_tr = sum(TR_i × tier_weight_i × count_i) × group_modifier

        Without tier info, falls back to the legacy action-economy multiplier.

        Args:
            enemy_trs: Dict mapping enemy_id → individual TR.
            enemy_tiers: Optional dict mapping enemy_id → tier string
                         (``"mook"``, ``"named"``, ``"boss"``).
        """
        if enemy_tiers is not None:
            weighted_tr = sum(
                enemy_trs.get(entry.enemy_id, 0)
                * self.TIER_WEIGHTS.get(
                    enemy_tiers.get(entry.enemy_id, "named"), 1.0
                )
                * entry.count
                for entry in self.enemies
            )
            return weighted_tr * self.group_size_modifier(self.total_enemy_count())

        # Legacy path (no tier info)
        raw_tr = sum(
            enemy_trs.get(entry.enemy_id, 0) * entry.count
            for entry in self.enemies
        )
        total_count = self.total_enemy_count()
        all_mooks = all(
            enemy_trs.get(entry.enemy_id, 0) <= 2
            for entry in self.enemies
        )
        return raw_tr * self.action_economy_multiplier(total_count, all_mooks)

    def to_client_dict(self) -> dict:
        """Serialize for sending to clients."""
        return self.model_dump()

    def to_fof(self) -> dict:
        """Serialize to .fof format."""
        now = datetime.now(tz=timezone.utc).isoformat()
        encounter_block: dict = {
            "difficulty": self.difficulty,
            "environment": self.environment,
            "description": self.description,
            "enemies": [
                {"enemy_id": e.enemy_id, "count": e.count}
                for e in self.enemies
            ],
        }
        if self.lateral_solutions:
            encounter_block["lateral_solutions"] = list(self.lateral_solutions)
        encounter_block["rewards"] = {
            "sparks": self.rewards_sparks,
            "narrative": self.rewards_narrative,
        }
        if self.notes:
            encounter_block["notes"] = self.notes

        return {
            "fof_version": "0.1",
            "type": "encounter",
            "id": self.id,
            "name": self.name,
            "encounter": encounter_block,
            "created_at": now,
            "last_modified": now,
        }

    @classmethod
    def from_fof(cls, fof_dict: dict) -> "Encounter":
        """Deserialize from a .fof format dict."""
        if fof_dict.get("type") != "encounter":
            raise ValueError(
                f"Expected type 'encounter', got {fof_dict.get('type')!r}."
            )
        enc = fof_dict.get("encounter")
        if not isinstance(enc, dict):
            raise ValueError("Missing or invalid 'encounter' block.")

        enemies = [
            EncounterEnemy(enemy_id=e["enemy_id"], count=e.get("count", 1))
            for e in enc.get("enemies", [])
        ]

        rewards = enc.get("rewards", {})

        return cls(
            id=fof_dict.get("id", "unknown"),
            name=fof_dict.get("name", "Unknown Encounter"),
            difficulty=enc.get("difficulty", "standard"),
            environment=enc.get("environment", ""),
            description=enc.get("description", ""),
            enemies=enemies,
            lateral_solutions=enc.get("lateral_solutions") or [],
            rewards_sparks=rewards.get("sparks", 0) if rewards else 0,
            rewards_narrative=rewards.get("narrative", "") if rewards else "",
            notes=enc.get("notes", ""),
        )
