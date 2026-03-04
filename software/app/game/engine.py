"""Core roll resolution engine — 2d6 + modifier, Spark, 3-tier outcomes."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Literal

from app.facets.registry import MergedRuleset


OutcomeTier = Literal["full_success", "partial_success", "failure"]


@dataclass
class RollRequest:
    attribute_id: str           # minor attribute being rolled
    attribute_rating: int       # 1, 2, or 3
    skill_id: str | None        # optional skill contributing a bonus
    skill_rank_id: str | None   # novice / practiced / expert
    difficulty_label: str       # Easy / Standard / Hard / Very Hard
    sparks_spent: int = 0
    description: str = ""       # what the character is attempting


@dataclass
class RollResult:
    dice_rolled: list[int]      # all dice before dropping
    dice_kept: list[int]        # dice after dropping lowest (Spark effect)
    dice_sum: int               # sum of kept dice
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
    if not ruleset.roll_resolution:
        # Fallback defaults matching the PHB
        defaults = {"Easy": 1, "Standard": 0, "Hard": -1, "Very Hard": -2}
        return defaults.get(label, 0)
    for dm in ruleset.roll_resolution.difficulty_modifiers:
        if dm.label.lower() == label.lower():
            return dm.modifier
    return 0


def _determine_outcome(total: int, ruleset: MergedRuleset) -> tuple[OutcomeTier, str, str]:
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
