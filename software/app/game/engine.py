"""Core roll resolution engine — 2d6 + modifier, Spark, 3-tier outcomes.

The client submits a RollRequest describing what is being attempted. The server
resolves everything: attribute modifier, skill modifier, difficulty modifier,
Spark dice addition, and outcome tier. The client never provides modifiers.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Literal

from app.facets.registry import MergedRuleset


OutcomeTier = Literal["full_success", "partial_success", "failure"]


@dataclass
class RollRequest:
    """All inputs required to resolve a 2d6 roll.

    Attributes:
        attribute_id: ID of the minor attribute being tested (e.g. "strength").
        attribute_rating: Player's rating in that attribute (1, 2, or 3).
        skill_id: Optional skill ID contributing a bonus.
        skill_rank_id: Skill rank if skill_id is set: "novice", "practiced", or "expert".
        difficulty_label: One of "Easy", "Standard", "Hard", "Very Hard".
        sparks_spent: Number of Sparks to spend (adds dice and drops lowest).
        description: Free-text description of the attempted action.
    """

    attribute_id: str
    attribute_rating: int
    skill_id: str | None
    skill_rank_id: str | None
    difficulty_label: str
    sparks_spent: int = 0
    description: str = ""

    def __post_init__(self) -> None:
        if self.sparks_spent < 0:
            raise ValueError("sparks_spent cannot be negative")


@dataclass
class RollResult:
    """Complete result of a resolved roll.

    Attributes:
        dice_rolled: All dice values before dropping (base 2 + sparks_spent extra).
        dice_kept: The top 2 dice after dropping the lowest sparks_spent.
        dice_sum: Sum of dice_kept.
        attribute_modifier: Modifier from the attribute rating.
        skill_modifier: Modifier from the skill rank (0 if no skill).
        difficulty_modifier: Modifier from the difficulty label.
        total: dice_sum + all modifiers — the value compared to thresholds.
        outcome: Machine-readable outcome tier.
        outcome_label: Human-readable label (e.g. "Full Success").
        outcome_description: Narrative prompt for the outcome.
        sparks_spent: How many Sparks were actually spent.
        request: The original RollRequest that produced this result.
    """

    dice_rolled: list[int]
    dice_kept: list[int]
    dice_sum: int
    attribute_modifier: int
    skill_modifier: int
    difficulty_modifier: int
    total: int
    outcome: OutcomeTier
    outcome_label: str
    outcome_description: str
    sparks_spent: int
    request: RollRequest


def resolve_roll(request: RollRequest, ruleset: MergedRuleset) -> RollResult:
    """Resolve a 2d6 + modifier roll with optional Spark spending.

    The client submits a roll request; the server resolves everything.
    The client never provides modifiers — they're derived from ruleset data.

    Args:
        request: Validated roll inputs.
        ruleset: The session's merged ruleset, used to look up modifiers and thresholds.

    Returns:
        A fully resolved RollResult.
    """
    # --- Attribute modifier ---
    attr_modifier = ruleset.get_minor_attribute_modifier(request.attribute_id, request.attribute_rating)

    # --- Skill modifier ---
    skill_modifier = 0
    if request.skill_id and request.skill_rank_id:
        skill_modifier = ruleset.get_skill_rank_modifier(request.skill_rank_id)

    # --- Difficulty modifier ---
    diff_modifier = _get_difficulty_modifier(request.difficulty_label, ruleset)

    # --- Spark mechanic: add d6s, drop lowest ---
    base_dice = 2
    extra_dice = max(0, request.sparks_spent)
    total_dice = base_dice + extra_dice

    dice_rolled = [random.randint(1, 6) for _ in range(total_dice)]
    dice_sorted = sorted(dice_rolled)

    # Drop the lowest `sparks_spent` dice to keep exactly 2
    dice_kept = dice_sorted[extra_dice:]  # keep the top 2

    dice_sum = sum(dice_kept)
    total = dice_sum + attr_modifier + skill_modifier + diff_modifier

    # --- Outcome ---
    outcome, outcome_label, outcome_desc = _determine_outcome(total, ruleset)

    return RollResult(
        dice_rolled=dice_rolled,
        dice_kept=dice_kept,
        dice_sum=dice_sum,
        attribute_modifier=attr_modifier,
        skill_modifier=skill_modifier,
        difficulty_modifier=diff_modifier,
        total=total,
        outcome=outcome,
        outcome_label=outcome_label,
        outcome_description=outcome_desc,
        sparks_spent=request.sparks_spent,
        request=request,
    )


def _get_difficulty_modifier(label: str, ruleset: MergedRuleset) -> int:
    """Look up the numeric modifier for a difficulty label.

    Falls back to hard-coded defaults if the ruleset has no roll_resolution.
    Returns 0 for unknown labels.
    """
    if not ruleset.roll_resolution:
        defaults = {"Easy": 1, "Standard": 0, "Hard": -1, "Very Hard": -2}
        return defaults.get(label, 0)
    for dm in ruleset.roll_resolution.difficulty_modifiers:
        if dm.label.lower() == label.lower():
            return dm.modifier
    return 0


def _determine_outcome(total: int, ruleset: MergedRuleset) -> tuple[OutcomeTier, str, str]:
    """Map a numeric total to an outcome tier, label, and description.

    Uses ruleset thresholds if available; falls back to 10/7 defaults.

    Returns:
        A tuple of (tier, label, description).
    """
    if ruleset.roll_resolution:
        thresholds = ruleset.roll_resolution.thresholds
        full = thresholds.get("full_success", 10)
        partial = thresholds.get("partial_success", 7)
        outcomes = ruleset.roll_resolution.outcomes
    else:
        full, partial = 10, 7
        outcomes = None

    if total >= full:
        tier: OutcomeTier = "full_success"
        label = outcomes.full_success.label if outcomes else "Full Success"
        desc = outcomes.full_success.description if outcomes else "You achieve your goal cleanly."
    elif total >= partial:
        tier = "partial_success"
        label = outcomes.partial_success.label if outcomes else "Success with Cost"
        desc = outcomes.partial_success.description if outcomes else "You succeed, but with a complication or cost."
    else:
        tier = "failure"
        label = outcomes.failure.label if outcomes else "Things Go Wrong"
        desc = outcomes.failure.description if outcomes else "The story always moves forward, but not in your favor."

    return tier, label, desc


def roll_result_to_dict(result: RollResult) -> dict:
    """Serialize a RollResult to a JSON-safe dict for API responses and broadcast."""
    return {
        "dice_rolled": result.dice_rolled,
        "dice_kept": result.dice_kept,
        "dice_sum": result.dice_sum,
        "attribute_modifier": result.attribute_modifier,
        "skill_modifier": result.skill_modifier,
        "difficulty_modifier": result.difficulty_modifier,
        "total": result.total,
        "outcome": result.outcome,
        "outcome_label": result.outcome_label,
        "outcome_description": result.outcome_description,
        "sparks_spent": result.sparks_spent,
        "attribute_id": result.request.attribute_id,
        "skill_id": result.request.skill_id,
        "difficulty": result.request.difficulty_label,
        "description": result.request.description,
    }
