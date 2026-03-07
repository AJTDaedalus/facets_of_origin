"""Core roll resolution engine — data-driven dice, modifiers, and N-tier outcomes.

The client submits a RollRequest describing what is being attempted. The server
resolves everything: attribute modifier, skill modifier, difficulty modifier,
Spark dice addition, and outcome tier. The client never provides modifiers.

The dice formula and outcome tiers are read from the ruleset, allowing custom
FoF modules to use different dice (1d20, 1d100, 3d8) and outcome structures.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from app.facets.registry import MergedRuleset
from app.facets.schema import OutcomeTierDef
from app.game.dice import DiceSpec


_DEFAULT_OUTCOME_TIERS = [
    OutcomeTierDef(id="full_success", threshold=10, label="Full Success",
                   description="You achieve your goal cleanly."),
    OutcomeTierDef(id="partial_success", threshold=7, label="Success with Cost",
                   description="You succeed, but with a complication or cost."),
    OutcomeTierDef(id="failure", threshold=None, label="Things Go Wrong",
                   description="The story always moves forward, but not in your favor."),
]

_DEFAULT_DIFFICULTY_ORDER = ["Easy", "Standard", "Hard", "Very Hard"]


@dataclass
class RollRequest:
    """All inputs required to resolve a roll.

    Attributes:
        attribute_id: ID of the minor attribute being tested (e.g. "strength").
        attribute_rating: Player's rating in that attribute (1, 2, or 3).
        skill_id: Optional skill ID contributing a bonus.
        skill_rank_id: Skill rank if skill_id is set: "novice", "practiced", "expert", or "master".
        difficulty_label: One of "Easy", "Standard", "Hard", "Very Hard".
        sparks_spent: Number of Sparks to spend (adds dice and drops lowest).
        press: Whether the Press combat mechanic is active (costs 1 Endurance, adds 1 die).
        description: Free-text description of the attempted action.
    """

    attribute_id: str
    attribute_rating: int
    skill_id: str | None
    skill_rank_id: str | None
    difficulty_label: str
    sparks_spent: int = 0
    press: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        if self.sparks_spent < 0:
            raise ValueError("sparks_spent cannot be negative")


@dataclass
class RollResult:
    """Complete result of a resolved roll.

    Attributes:
        dice_rolled: All dice values before dropping (base dice + extra from sparks/press).
        dice_kept: The top N dice after dropping extras (N = base dice count from formula).
        dice_sum: Sum of dice_kept.
        attribute_modifier: Modifier from the attribute rating.
        skill_modifier: Modifier from the skill rank (0 if no skill).
        difficulty_modifier: Modifier from the difficulty label.
        total: dice_sum + all modifiers — the value compared to thresholds.
        outcome: Machine-readable outcome tier ID.
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
    outcome: str
    outcome_label: str
    outcome_description: str
    sparks_spent: int
    request: RollRequest


def resolve_roll(request: RollRequest, ruleset: MergedRuleset) -> RollResult:
    """Resolve a dice roll with optional Spark spending.

    The dice formula is read from the ruleset (defaults to 2d6). Sparks and Press
    add extra dice; the lowest extras are dropped to keep the base count.

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

    # --- Dice from ruleset ---
    dice_spec = DiceSpec.parse(
        ruleset.roll_resolution.dice if ruleset.roll_resolution else "2d6"
    )

    # --- Spark + Press mechanic: add dice, drop lowest ---
    base_dice = dice_spec.count
    extra_dice = max(0, request.sparks_spent) + (1 if request.press else 0)
    total_dice = base_dice + extra_dice

    dice_rolled = [random.randint(1, dice_spec.sides) for _ in range(total_dice)]
    dice_sorted = sorted(dice_rolled)

    # Drop the lowest `extra_dice` dice to keep exactly `base_dice`
    dice_kept = dice_sorted[extra_dice:]

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


# ---------------------------------------------------------------------------
# Magic roll resolution
# ---------------------------------------------------------------------------

def resolve_magic_roll(
    character: "Character",  # type: ignore[name-defined]
    domain_id: str,
    scope: str,
    intent: str,
    ruleset: MergedRuleset,
    spark_use: str | None = None,
) -> RollResult:
    """Resolve a magical effect using the Domain + Intent + Scope framework.

    Args:
        character: The casting character.
        domain_id: The domain being used (e.g. "inscription", "fire").
        scope: "minor" | "significant" | "major".
        intent: Free-text description of what the magic does (logged only).
        ruleset: The session's merged ruleset.
        spark_use: Optional Spark use: "improve_roll" | "push_scope" |
                   "ease_focused_major" (focused domains only).

    Returns:
        A RollResult with difficulty and modifiers resolved from domain + scope.
    """
    if not ruleset.magic:
        # No magic rules loaded — fall back to Standard difficulty
        return resolve_roll(
            RollRequest(
                attribute_id="spirit",
                attribute_rating=character.attributes.get("spirit", 2),
                skill_id=None,
                skill_rank_id=None,
                difficulty_label="Standard",
                description=f"[magic] {intent}",
            ),
            ruleset,
        )

    domain_def = ruleset.magic.get_domain(domain_id)
    if not domain_def:
        raise ValueError(f"Unknown magic domain '{domain_id}'.")

    domain_type_cfg = ruleset.magic.domain_types.get(domain_def.type, {})
    scope_difficulties: dict = domain_type_cfg.get("scope_difficulties", {})

    # Scope → base difficulty
    scope_to_key = {"minor": "minor", "significant": "significant", "major": "major"}
    difficulty_label: str = scope_difficulties.get(scope_to_key.get(scope, scope), "Standard")

    # Pre-Technique restriction: scope ceiling and difficulty penalty
    if not character.magic_technique_active:
        scope_limit = ruleset.magic.pre_technique_scope_limit if ruleset.magic else "minor"
        penalty_steps = ruleset.magic.pre_technique_difficulty_penalty if ruleset.magic else 1
        if scope_limit == "minor" and scope != "minor":
            raise ValueError(
                f"Before unlocking the Technique, magic is limited to {scope_limit} scope only. "
                "Unlock the corresponding Facet Technique to access broader scopes."
            )
        for _ in range(penalty_steps):
            difficulty_label = _step_difficulty_harder(difficulty_label, ruleset)

    # Spark use
    sparks_spent = 0
    if spark_use == "ease_focused_major" and domain_def.type == "focused" and scope == "major":
        difficulty_label = _step_difficulty_easier(difficulty_label, ruleset)
    elif spark_use == "push_scope":
        if domain_def.type == "broad":
            raise ValueError(
                "Broad (Prismatic) domains cannot be pushed beyond their scope ceiling — "
                "Very Hard is the maximum regardless of Sparks."
            )
        # Push scope one step higher: difficulty steps harder to reflect the ambition
        difficulty_label = _step_difficulty_harder(difficulty_label, ruleset)
    elif spark_use == "improve_roll":
        sparks_spent = 1  # consumed by caller; here we model the dice bonus

    # Secondary domain penalty: one difficulty step harder (Soul Communion T3 rule)
    is_secondary = (
        hasattr(character, "secondary_magic_domain")
        and character.secondary_magic_domain
        and domain_id == character.secondary_magic_domain
    )
    if is_secondary:
        difficulty_label = _step_difficulty_harder(difficulty_label, ruleset)

    # Broad domain hard ceiling: Very Hard max, Sparks cannot push further
    if domain_def.type == "broad":
        difficulty_label = "Very Hard"  # enforce ceiling

    # Attribute for roll: tradition determines attribute
    tradition = domain_def.tradition
    if tradition == "intuitive":
        attr_id = "spirit"
    else:
        attr_id = "knowledge"

    attr_rating = character.attributes.get(attr_id, 2)

    request = RollRequest(
        attribute_id=attr_id,
        attribute_rating=attr_rating,
        skill_id=None,
        skill_rank_id=None,
        difficulty_label=difficulty_label,
        sparks_spent=sparks_spent,
        description=f"[magic:{domain_id}:{scope}] {intent}",
    )
    return resolve_roll(request, ruleset)


# ---------------------------------------------------------------------------
# Difficulty stepping (data-driven)
# ---------------------------------------------------------------------------

def _get_difficulty_order(ruleset) -> list[str]:
    """Derive ordered difficulty labels from ruleset modifiers (easiest → hardest)."""
    if (ruleset.roll_resolution
            and ruleset.roll_resolution.difficulty_modifiers):
        return [dm.label for dm in sorted(
            ruleset.roll_resolution.difficulty_modifiers,
            key=lambda dm: dm.modifier, reverse=True,
        )]
    return _DEFAULT_DIFFICULTY_ORDER


def _step_difficulty_harder(label: str, ruleset=None) -> str:
    order = _get_difficulty_order(ruleset) if ruleset else _DEFAULT_DIFFICULTY_ORDER
    idx = order.index(label) if label in order else 1
    return order[min(idx + 1, len(order) - 1)]


def _step_difficulty_easier(label: str, ruleset=None) -> str:
    order = _get_difficulty_order(ruleset) if ruleset else _DEFAULT_DIFFICULTY_ORDER
    idx = order.index(label) if label in order else 1
    return order[max(idx - 1, 0)]


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


# ---------------------------------------------------------------------------
# Outcome resolution (data-driven N-tier)
# ---------------------------------------------------------------------------

def _get_outcome_tiers(ruleset) -> list[OutcomeTierDef]:
    """Return outcome tiers sorted for evaluation: non-null thresholds descending, null last."""
    # Prefer new outcome_tiers list
    if (ruleset.roll_resolution
            and ruleset.roll_resolution.outcome_tiers):
        tiers = list(ruleset.roll_resolution.outcome_tiers)
        return sorted(tiers, key=lambda t: (t.threshold is None, -(t.threshold or 0)))

    # Backward compat: build from old thresholds/outcomes
    if (ruleset.roll_resolution
            and ruleset.roll_resolution.thresholds):
        rr = ruleset.roll_resolution
        thresholds = rr.thresholds
        outcomes = rr.outcomes
        built: list[OutcomeTierDef] = []
        full_th = thresholds.get("full_success", 10)
        partial_th = thresholds.get("partial_success", 7)
        built.append(OutcomeTierDef(
            id="full_success", threshold=full_th,
            label=outcomes.full_success.label if outcomes else "Full Success",
            description=outcomes.full_success.description if outcomes else "You achieve your goal cleanly.",
        ))
        built.append(OutcomeTierDef(
            id="partial_success", threshold=partial_th,
            label=outcomes.partial_success.label if outcomes else "Success with Cost",
            description=outcomes.partial_success.description if outcomes else "You succeed, but with a complication or cost.",
        ))
        built.append(OutcomeTierDef(
            id="failure", threshold=None,
            label=outcomes.failure.label if outcomes else "Things Go Wrong",
            description=outcomes.failure.description if outcomes else "The story always moves forward, but not in your favor.",
        ))
        return sorted(built, key=lambda t: (t.threshold is None, -(t.threshold or 0)))

    # Hardcoded fallback
    return sorted(_DEFAULT_OUTCOME_TIERS, key=lambda t: (t.threshold is None, -(t.threshold or 0)))


def _determine_outcome(total: int, ruleset) -> tuple[str, str, str]:
    """Map a numeric total to an outcome tier, label, and description.

    Supports any number of outcome tiers. Tiers are evaluated from highest
    threshold to lowest; the first tier whose threshold is met (total >= threshold)
    wins. A tier with threshold=None is the catch-all fallback.

    Returns:
        A tuple of (tier_id, label, description).
    """
    tiers = _get_outcome_tiers(ruleset)
    for tier in tiers:
        if tier.threshold is not None and total >= tier.threshold:
            return tier.id, tier.label, tier.description
    # Catch-all: last tier (threshold=None)
    fallback = tiers[-1]
    return fallback.id, fallback.label, fallback.description


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
