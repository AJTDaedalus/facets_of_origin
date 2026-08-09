"""Encounter model — enemy groups, TR budget, and action economy."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

#: The published difficulty ladder, in order (MM1 Encounter Recipe Table).
DIFFICULTY_BANDS = ["skirmish", "standard", "hard", "deadly"]

_VALID_TIERS = {"mook", "named", "boss"}


def compute_band(enemy_tiers: list[str], party_strength: int = 3) -> dict:
    """Compute a roster's difficulty band from the MM1 Encounter Recipe Table.

    Actor count of Named/Boss enemies is the dial, plus one band per Mook once
    the Named core is in place — the actor-count doctrine simulation validated
    in ``research/simulation_log.md`` Series 9 (T6.1, K-3). Every branch below
    is keyed to a published row or its accompanying prose:

    Party Strength 3 (Table MM1–5, measured — seeds 1/2/3 win rates):
      * Mook-only, any size: **Skirmish** (100%; Mook swarms never dangerous)
      * 1–2 Named/Boss (any Mooks): **Skirmish** ("trivial at any TR")
      * 3 Named alone: **Skirmish** (~96% — inside the 85–100% target)
      * 3 Named + 1/2/3+ Mooks: **Standard / Hard / Deadly** (76% / 47% / 20%)
      * 4 Named alone: **Hard** ("a coin-flip"); + any Mook: **Deadly**
      * 5+ Named/Boss: **Deadly**, flagged "near-certain party loss" —
        below the published Deadly target (15–35%), so the note says so.

    Party Strength ≠ 3 (Table MM1–6 and the "+1 Named per additional PC"
    rule of thumb): the same ladder shifted by ``party_strength − 3`` actors,
    with the MM1–6 shape (threshold Named alone = Standard). **The book
    itself flags these rows as un-simulated extrapolation** ("Do not present
    them to players as calibrated"), so the result carries
    ``calibrated: False`` — honesty over silent extrapolation.

    Args:
        enemy_tiers: One tier string per individual actor
            (``"mook"``/``"named"``/``"boss"``, case-insensitive).
        party_strength: Sum of participating characters' career advances
            (MM1 §Party Strength). Only PS 3 is simulation-calibrated.

    Returns:
        Dict with ``band`` (str or None for an empty roster), ``band_index``
        (position in :data:`DIFFICULTY_BANDS`, or None), ``calibrated``
        (bool — True only at PS 3), ``named_boss_count``, ``mook_count``,
        ``party_strength``, and ``note`` (honest caveat text, may be empty).

    Raises:
        ValueError: On an unknown tier string or non-positive party strength.
    """
    if party_strength < 1:
        raise ValueError(f"party_strength must be >= 1, got {party_strength}.")

    tiers = [str(t).lower() for t in enemy_tiers]
    unknown = sorted(set(tiers) - _VALID_TIERS)
    if unknown:
        raise ValueError(
            f"Unknown enemy tier(s): {', '.join(unknown)}. "
            f"Valid tiers: mook, named, boss."
        )

    named_boss = sum(1 for t in tiers if t in ("named", "boss"))
    mooks = len(tiers) - named_boss
    calibrated = party_strength == 3

    band: str | None
    note = ""

    if not tiers:
        band = None
        note = "No enemies in the roster yet."
    elif calibrated:
        # Table MM1-5 + MM1 "Sizing an Encounter" prose (measured, Series 9).
        if named_boss == 0:
            band = "skirmish"
            note = (
                "Mook-only — Mook swarms never produce genuine danger "
                "at any size a table would field (MM1 Scaling Notes)."
            )
        elif named_boss <= 2:
            band = "skirmish"
            note = (
                "1-2 Named/Boss actors are trivial for a fresh party "
                "at any TR (MM1 Scaling Notes)."
            )
        elif named_boss == 3:
            band = DIFFICULTY_BANDS[min(mooks, 3)]
            if mooks == 0:
                note = (
                    "Three Named alone is a near-clean win (~96%) — "
                    "add a Mook for a Standard fight (MM1)."
                )
        elif named_boss == 4:
            band = "hard" if mooks == 0 else "deadly"
        else:
            band = "deadly"
            note = (
                "Beyond the published Deadly window: five or more "
                "Named/Boss actors is a near-certain party loss "
                "(MM1 Scaling Notes)."
            )
    else:
        # Table MM1-6 shape, shifted by the "+1 Named per additional PC" rule
        # of thumb. Un-simulated — MM1's own caveat is the precedent.
        threshold = max(1, 3 + (party_strength - 3))
        if named_boss < threshold:
            band = "skirmish"
        elif named_boss == threshold:
            band = DIFFICULTY_BANDS[min(1 + mooks, 3)]
        else:
            band = "deadly"
        note = (
            f"Party Strength {party_strength} is un-simulated — extrapolated "
            "from the PS-3 findings (MM1, Table MM1-6 caveat). Treat as a "
            "starting guess, not a validated recipe."
        )

    return {
        "band": band,
        "band_index": DIFFICULTY_BANDS.index(band) if band else None,
        "calibrated": calibrated if band else False,
        "named_boss_count": named_boss,
        "mook_count": mooks,
        "party_strength": party_strength,
        "note": note,
    }


class EncounterEnemy(BaseModel):
    """An enemy entry in an encounter definition."""

    enemy_id: str
    count: int = Field(default=1, ge=1)


class Encounter(BaseModel):
    """An encounter definition with enemies, difficulty, and TR budget.

    Mirrors the encounter .fof format.

    **On the TR budget's status (task A10 / DESIGN §5-ter).** The
    ``TR × multiplier`` budget below is a *rough ordering sanity check*, not a
    difficulty predictor. Simulation (``research/simulation_log.md`` Series 9)
    proved the real difficulty curve is a steep, actor-count-gated threshold —
    1–2 simultaneously-acting Named/Boss actors are trivial at *any* TR, 3–5 is
    a cliff, per-enemy TR is only a second-order modulator past that gate, and
    Mook swarms never produce real danger (mean PCs Broken stays 0.00 through
    30 Mooks). That is neither the linear nor the separable relationship this
    weighted-TR-sum formula assumes, so **it is explicitly non-predictive for
    rosters of 3+ Named/Boss enemies and for Mook swarms.** The calibrated,
    simulation-validated tool an MM should actually use is the **Encounter
    Recipe Table in ``mm_manual/MM1_Encounters_and_Enemies.md``**. Do not retune
    the constants here to hit specific win-rate bands — that resurrects the
    false-precision trap A10 escalated.
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
        """Return the encounter budget multiplier for a difficulty level.

        Rough ordering only. These multipliers do **not** map to validated
        win-rate bands (that mapping was voided — BRIEF §Q3); they exist to
        give a loose "bigger number = probably harder" read for simple/solo/
        Mook rosters. Use the MM1 Recipe Table for anything with 3+ Named/Boss
        enemies.
        """
        return {
            "skirmish": 1.0,
            "standard": 2.0,
            "hard": 3.0,
            "deadly": 4.0,
        }.get(difficulty.lower(), 2.0)

    # Enemy tier weights — a rough ordering hint, not a calibrated coefficient.
    # Mooks self-cancel as they die; Named maintain pressure; Bosses have phase
    # changes and psychological impact. These weights capture the *direction* of
    # that intuition (mook < named < boss) but NOT its magnitude: Series 9
    # showed the true driver is simultaneous Named/Boss actor *count*, which no
    # per-enemy weight in a weighted-sum formula reproduces. Non-predictive for
    # 3+ Named/Boss rosters — see the class docstring and the MM1 Recipe Table.
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

        Legacy interface kept for backward compatibility. Rough ordering only —
        count-scaled multipliers do not reproduce the actor-count threshold the
        simulator measured (DESIGN §5-ter); see the class docstring.

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
        """Calculate the encounter TR budget from party strength and difficulty.

        Rough heuristic. This is a loose ordering aid for simple rosters, not a
        difficulty prediction — it is non-predictive for 3+ Named/Boss rosters
        and for Mook swarms (DESIGN §5-ter). The authoritative, simulation-
        validated tool is the MM1 Encounter Recipe Table.
        """
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

        When *enemy_tiers* is provided the tier-weighted formula is used::

            effective_tr = sum(TR_i × tier_weight_i × count_i) × group_modifier

        Without tier info, falls back to the legacy action-economy multiplier.

        **This number is a rough ordering aid, not a difficulty predictor.**
        It is a linear, separable weighted sum; the real difficulty curve is a
        steep, actor-count-gated threshold (DESIGN §5-ter, Series 9). The
        formula is known to *mis-rank* multi-Named/Boss rosters — e.g. it scores
        two Bosses above four Named enemies, while simulation has the four Named
        far deadlier. Non-predictive for 3+ Named/Boss rosters and Mook swarms;
        for those, use the MM1 Recipe Table. Do not "fix" the constants to make
        this number predictive.

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

    def band(self, enemy_tiers: dict[str, str], party_strength: int) -> dict:
        """Difficulty band for this encounter's roster (T6.2, K-3).

        Expands each entry by its count and defers to :func:`compute_band`.
        Entries whose enemy_id is not in *enemy_tiers* (a deleted library
        enemy — "will no longer resolve") are skipped: the band describes the
        actors that will actually hit the table.

        Args:
            enemy_tiers: Dict mapping enemy_id → tier string.
            party_strength: Sum of participating characters' career advances.
        """
        tiers: list[str] = []
        for entry in self.enemies:
            tier = enemy_tiers.get(entry.enemy_id)
            if tier is None:
                continue
            tiers.extend([tier] * entry.count)
        return compute_band(tiers, party_strength)

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
