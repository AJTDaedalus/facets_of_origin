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
        borrowed_trouble: Whether an offered complication was accepted (PHB III.1).
            Adds a die exactly as a Spark does, but costs no Spark — the price
            is the complication, which lands whatever the dice say.
        description: Free-text description of the attempted action.
    """

    attribute_id: str
    attribute_rating: int
    skill_id: str | None
    skill_rank_id: str | None
    difficulty_label: str
    sparks_spent: int = 0
    press: bool = False
    borrowed_trouble: bool = False
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
        borrowed_trouble: Whether a complication was accepted for the extra die.
        critical: Every kept die showed its maximum face (PHB III.1).
        fumble: Every kept die showed 1 (PHB III.1).
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
    borrowed_trouble: bool = False
    critical: bool = False
    fumble: bool = False


def _natural_flags(dice_kept: list[int], sides: int, ruleset) -> tuple[bool, bool]:
    """(critical, fumble) for the kept dice, per the ruleset's natural results.

    Keyed to the dice rather than the total on purpose (III.1): a total-based
    tier scales with modifiers and stops being rare. Mutually exclusive by
    construction — the same dice cannot all be maximum and all be 1.
    """
    rr = getattr(ruleset, "roll_resolution", None)
    if not rr or not dice_kept:
        return False, False

    def _matches(rule) -> bool:
        if rule is None:
            return False
        face = sides if rule.natural == "high" else 1
        return all(d == face for d in dice_kept)

    return _matches(getattr(rr, "critical", None)), _matches(getattr(rr, "fumble", None))


def _apply_outcome_floor(outcome: str, rule, ruleset) -> str:
    """Raise `outcome` to the rule's `min_outcome` if it sits below it.

    Only ever raises. A natural result may promote a tier; nothing in the
    ruleset demotes one, because demoting punishes competence.
    """
    if rule is None or not getattr(rule, "min_outcome", None):
        return outcome
    tiers = [t.id for t in _get_outcome_tiers(ruleset)]  # best first
    if outcome not in tiers or rule.min_outcome not in tiers:
        return outcome
    return rule.min_outcome if tiers.index(outcome) > tiers.index(rule.min_outcome) else outcome


def _roll_and_resolve(
    attr_modifier: int,
    skill_modifier: int,
    difficulty_label: str,
    sparks_spent: int,
    press: bool,
    ruleset: MergedRuleset,
    borrowed_trouble: bool = False,
) -> tuple[list[int], list[int], int, int, int, str, str, str, bool, bool]:
    """Shared dice-rolling and outcome core: roll the ruleset's dice formula
    (Sparks/Press add dice, lowest extras dropped), sum against the given
    modifiers, and determine the outcome tier. `resolve_roll` and
    `resolve_saving_throw` both call this — only where the attribute
    modifier comes from differs (Minor Attribute + skill vs. Major
    Attribute alone).

    Returns (dice_rolled, dice_kept, dice_sum, diff_modifier, total,
    outcome, outcome_label, outcome_desc).
    """
    diff_modifier = _get_difficulty_modifier(difficulty_label, ruleset)

    dice_spec = DiceSpec.parse(
        ruleset.roll_resolution.dice if ruleset.roll_resolution else "2d6"
    )

    base_dice = dice_spec.count
    press_dice = ruleset.combat.press.extra_dice if press else 0
    bt_def = getattr(ruleset.roll_resolution, "borrowed_trouble", None) if ruleset.roll_resolution else None
    bt_dice = (bt_def.extra_dice if bt_def else 1) if borrowed_trouble else 0
    extra_dice = max(0, sparks_spent) + press_dice + bt_dice
    total_dice = base_dice + extra_dice

    dice_rolled = [random.randint(1, dice_spec.sides) for _ in range(total_dice)]
    dice_sorted = sorted(dice_rolled)

    # Drop the lowest `extra_dice` dice to keep exactly `base_dice`
    dice_kept = dice_sorted[extra_dice:]

    dice_sum = sum(dice_kept)
    total = dice_sum + attr_modifier + skill_modifier + diff_modifier

    outcome, outcome_label, outcome_desc = _determine_outcome(total, ruleset)

    critical, fumble = _natural_flags(dice_kept, dice_spec.sides, ruleset)
    if critical:
        promoted = _apply_outcome_floor(
            outcome, ruleset.roll_resolution.critical if ruleset.roll_resolution else None, ruleset
        )
        if promoted != outcome:
            outcome, outcome_label, outcome_desc = _outcome_by_id(promoted, ruleset)

    return (dice_rolled, dice_kept, dice_sum, diff_modifier, total,
            outcome, outcome_label, outcome_desc, critical, fumble)


def _outcome_by_id(outcome_id: str, ruleset) -> tuple[str, str, str]:
    """(id, label, description) for a tier named directly rather than by total."""
    for tier in _get_outcome_tiers(ruleset):
        if tier.id == outcome_id:
            return tier.id, tier.label, tier.description
    return outcome_id, outcome_id.replace("_", " ").title(), ""


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
    attr_modifier = ruleset.get_minor_attribute_modifier(request.attribute_id, request.attribute_rating)

    skill_modifier = 0
    if request.skill_id and request.skill_rank_id:
        skill_modifier = ruleset.get_skill_rank_modifier(request.skill_rank_id)

    (dice_rolled, dice_kept, dice_sum, diff_modifier, total,
     outcome, outcome_label, outcome_desc, critical, fumble) = (
        _roll_and_resolve(
            attr_modifier, skill_modifier, request.difficulty_label,
            request.sparks_spent, request.press, ruleset,
            request.borrowed_trouble,
        )
    )

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
        borrowed_trouble=request.borrowed_trouble,
        critical=critical,
        fumble=fumble,
    )


def resolve_saving_throw(
    major_attribute_id: str,
    character: "Character",  # type: ignore[name-defined]
    ruleset: MergedRuleset,
    difficulty_label: str = "Standard",
    sparks_spent: int = 0,
) -> RollResult:
    """Resolve a saving throw (III.1:84-99): 2d6 + the Major Attribute
    modifier, on the standard three-tier outcome table. No skill applies.

    The modifier comes from `Character.get_major_attribute_modifier`
    (sync-M-8 part 1) — not a second implementation of the II.2 derivation.
    """
    attr_modifier = character.get_major_attribute_modifier(major_attribute_id, ruleset)

    (dice_rolled, dice_kept, dice_sum, diff_modifier, total,
     outcome, outcome_label, outcome_desc, critical, fumble) = (
        _roll_and_resolve(attr_modifier, 0, difficulty_label, sparks_spent, False, ruleset)
    )

    request = RollRequest(
        attribute_id=major_attribute_id,
        attribute_rating=0,
        skill_id=None,
        skill_rank_id=None,
        difficulty_label=difficulty_label,
        sparks_spent=sparks_spent,
        press=False,
        description="Saving throw",
    )

    return RollResult(
        dice_rolled=dice_rolled,
        dice_kept=dice_kept,
        dice_sum=dice_sum,
        attribute_modifier=attr_modifier,
        skill_modifier=0,
        difficulty_modifier=diff_modifier,
        total=total,
        outcome=outcome,
        outcome_label=outcome_label,
        outcome_description=outcome_desc,
        sparks_spent=sparks_spent,
        request=request,
        critical=critical,
        fumble=fumble,
    )


# ---------------------------------------------------------------------------
# Magic roll resolution
# ---------------------------------------------------------------------------

# The only Spark uses a magic roll recognises (II.3, Sparks and Magic; T2.2/D8):
# the dice rule, plus the exactly-two reach cases. "push_scope" was retired with
# the un-executable "one scope tier beyond Major" rule (P-1).
VALID_SPARK_USES = frozenset({"improve_roll", "ease_focused_major", "pre_technique_push"})


def can_spark_ease_major(domain_type: str, scope: str, ruleset: MergedRuleset) -> bool:
    """Reach case 2 (II.3): a Focused domain may spend a Spark to shift a Major
    working one difficulty step easier. Reach-Sparks cannot move any other
    working — Broad (Prismatic) included; dice-Sparks work normally there."""
    if not ruleset.magic:
        return False
    rule = ruleset.magic.spark_rules.ease_focused_major
    return domain_type == rule.domain_type and scope == rule.scope


def can_spark_pre_technique_reach(
    character: "Character",  # type: ignore[name-defined]
    scope: str,
    ruleset: MergedRuleset,
) -> bool:
    """Reach case 1 (II.3, D8): a pre-Technique caster may spend a Spark to
    attempt ONE Significant-scope effect at the domain's normal difficulty —
    the Spark buys the scope, not a discount on the roll."""
    if not ruleset.magic:
        return False
    return (
        not character.magic_technique_active
        and scope == ruleset.magic.spark_rules.pre_technique_push.permitted_scope
    )


def resolve_magic_roll(
    character: "Character",  # type: ignore[name-defined]
    domain_id: str,
    scope: str,
    intent: str,
    ruleset: MergedRuleset,
    spark_use: str | None = None,
    press: bool = False,
    borrowed_trouble: bool = False,
) -> RollResult:
    """Resolve a magical effect using the Domain + Intent + Scope framework.

    Args:
        character: The casting character.
        domain_id: The domain being used (e.g. "inscription", "fire").
        scope: "minor" | "significant" | "major".
        intent: Free-text description of what the magic does (logged only).
        ruleset: The session's merged ruleset.
        spark_use: Optional Spark use: "improve_roll" (the dice rule) |
                   "ease_focused_major" (reach: Focused Major only) |
                   "pre_technique_push" (reach: pre-Technique Significant only).
                   Any other value — including the retired "push_scope" —
                   raises ValueError so the handler never wastes a Spark on it.
        press: The caster Pressed (D25: a magical Strike is a Strike, and can
            spend Endurance for the extra die like any other).
        borrowed_trouble: A complication was accepted for an extra die (III.1).

    Returns:
        A RollResult with difficulty and modifiers resolved from domain + scope.

    Raises:
        ValueError: On an unknown spark_use, an ineligible reach attempt
            (reach-Sparks cannot move a Broad working's difficulty), or a
            pre-Technique cast beyond the permitted scope.
    """
    if spark_use is not None and spark_use not in VALID_SPARK_USES:
        raise ValueError(
            f"Unknown Spark use '{spark_use}'. A Spark improves the dice on any "
            "roll, or buys reach in exactly two cases: a pre-Technique "
            "Significant-scope attempt, or easing a Focused domain's Major "
            "working one step (II.3, Sparks and Magic)."
        )

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
        # Domain not registered in the catalog — create a synthetic definition
        # using "standard" type so the cast still resolves with sensible defaults.
        from app.facets.schema import MagicDomainDef
        domain_def = MagicDomainDef(
            id=domain_id,
            name=domain_id.replace("_", " ").title(),
            type="standard",
            tradition="scholarly",
            description=f"Unregistered domain '{domain_id}'",
        )

    domain_type_cfg = ruleset.magic.domain_types.get(domain_def.type, {})
    scope_difficulties: dict = domain_type_cfg.get("scope_difficulties", {})

    # Scope → base difficulty
    scope_to_key = {"minor": "minor", "significant": "significant", "major": "major"}
    difficulty_label: str = scope_difficulties.get(scope_to_key.get(scope, scope), "Standard")

    # D8 (II.3, Reaching Significant Early): a pre-Technique caster may spend
    # a Spark to attempt one effect at spark_rules.pre_technique_push's
    # permitted scope, at the domain's *normal* difficulty for that scope —
    # the Spark buys the scope, not a discount on the roll (no difficulty
    # penalty is applied below, and no extra dice are added).
    pre_technique_push = (
        spark_use == "pre_technique_push"
        and can_spark_pre_technique_reach(character, scope, ruleset)
    )
    if spark_use == "pre_technique_push" and not pre_technique_push:
        raise ValueError(
            "A reach-Spark cannot buy that: pre-Technique, a Spark buys one "
            "Significant-scope attempt only (II.3, Reaching Significant Early)."
        )

    # Pre-Technique restriction: scope ceiling and difficulty penalty
    if not character.magic_technique_active and not pre_technique_push:
        scope_limit = ruleset.magic.pre_technique_scope_limit if ruleset.magic else "minor"
        penalty_steps = ruleset.magic.pre_technique_difficulty_penalty if ruleset.magic else 1
        if scope_limit == "minor" and scope != "minor":
            raise ValueError(
                f"Before unlocking the Technique, magic is limited to {scope_limit} scope only. "
                "Unlock the corresponding Facet Technique to access broader scopes."
            )
        for _ in range(penalty_steps):
            difficulty_label = _step_difficulty_harder(difficulty_label, ruleset)

    # Spark use — the dice rule plus reach case 2, both read from
    # ruleset.magic.spark_rules, not hardcoded domain-type/scope literals.
    sparks_spent = 0
    if spark_use == "ease_focused_major":
        if not can_spark_ease_major(domain_def.type, scope, ruleset):
            raise ValueError(
                "A reach-Spark cannot move this working's difficulty: only a "
                "Focused domain's Major working can be eased one step (II.3). "
                "Dice-Sparks work normally on any roll."
            )
        difficulty_label = _step_difficulty_easier(difficulty_label, ruleset)
    elif spark_use == "improve_roll":
        sparks_spent = 1  # consumed by caller; here we model the dice bonus
    # pre_technique_push needs no further action here: the scope ceiling was
    # already bypassed above, and the difficulty stays at its normal value —
    # no dice bonus, no difficulty shift.

    # Secondary domain penalty: one difficulty step harder (Second Domain,
    # Tier 3). T4.2/D9: the penalty is an arc, not a permanent tax — it lifts
    # at the character's next Facet level after acquiring the Technique
    # (Character.second_domain_penalty_expired; legacy characters without an
    # acquisition record keep the penalty).
    is_secondary = (
        hasattr(character, "secondary_magic_domain")
        and character.secondary_magic_domain
        and domain_id == character.secondary_magic_domain
    )
    if is_secondary and not getattr(character, "second_domain_penalty_expired", False):
        difficulty_label = _step_difficulty_harder(difficulty_label, ruleset)

    # No Broad ceiling clamp is needed here: Very Hard is the top of the
    # difficulty ladder and `_step_difficulty_harder` already saturates there,
    # while every reach-Spark on a Broad working is refused outright above.
    # Assigning "Very Hard" would not enforce a ceiling — it would *raise* a
    # Minor-scope Broad cast from its canonical Hard (II.4b/II.4c: "Hard at
    # Minor scope").

    # Attribute and skill for the roll (II.3, Rolling Magic; T4.1/D7):
    # the tradition determines both — casting with Spirit adds the Attune
    # rank; casting with Knowledge adds the Lore rank. The mapping is read
    # from ruleset.magic.traditions (facet.yaml), with the II.3 defaults as
    # fallback.
    tradition = domain_def.tradition
    # D24: a lineage Gift is cast intuitively whatever the domain's own
    # tradition — blood is not study. The character records it at creation.
    if (getattr(character, "domain_source", None) == "lineage"
            and domain_id == getattr(character, "magic_domain", None)
            and getattr(character, "magic_tradition", None)):
        tradition = character.magic_tradition
    _tradition_defaults = {
        "intuitive": ("spirit", "attune"),
        "scholarly": ("knowledge", "lore"),
    }
    traditions_cfg = getattr(ruleset.magic, "traditions", None) or {}
    trad_cfg = traditions_cfg.get(tradition)
    if trad_cfg is not None:
        attr_id, skill_id = trad_cfg.attribute, trad_cfg.skill
    elif tradition in _tradition_defaults:
        attr_id, skill_id = _tradition_defaults[tradition]
    else:
        # A domain declaring a tradition no Facet defines is a data error, and
        # guessing produces a wrong roll nobody can see. Name it instead.
        raise ValueError(
            f"Domain '{domain_id}' declares tradition '{tradition}', which no "
            f"loaded Facet defines under magic.traditions "
            f"(known: {', '.join(sorted(traditions_cfg)) or 'none'})."
        )

    attr_rating = character.attributes.get(attr_id, 2)

    # A caster without the tradition's skill casts at Novice (+0) — every
    # skill starts at Novice, so the skill still shows on the roll.
    skill_state = getattr(character, "skills", {}).get(skill_id)
    skill_rank_id = getattr(skill_state, "rank", None) or "novice"

    request = RollRequest(
        attribute_id=attr_id,
        attribute_rating=attr_rating,
        skill_id=skill_id,
        skill_rank_id=skill_rank_id,
        difficulty_label=difficulty_label,
        sparks_spent=sparks_spent,
        press=press,
        borrowed_trouble=borrowed_trouble,
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
        "borrowed_trouble": result.borrowed_trouble,
        "critical": result.critical,
        "fumble": result.fumble,
        "attribute_id": result.request.attribute_id,
        "skill_id": result.request.skill_id,
        "difficulty": result.request.difficulty_label,
        "description": result.request.description,
    }
