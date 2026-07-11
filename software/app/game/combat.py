"""Pure, synchronous combat-resolution rules (PHB III.3).

This is the only place combat rules live — `app/api/websocket.py` and
`tools/combat_sim.py` both call into it; neither reimplements it. See
`docs/DESIGN_v0.3_ruleset_revision.md` §2.1 and TASKS `WS-A0`.

No I/O, no async, no session objects. Every function takes plain state
(lists, ints, strings) plus a `MergedRuleset`, and returns a result
dataclass. Constants — reaction costs, condition tier IDs, posture
modifiers, Withdrawn recovery, strike-outcome tiers — are always read from
the ruleset, never hardcoded.

Scope note: `resolve_strike`/`resolve_reaction` resolve *rolls and their
immediate rule consequences* (mook removal, Endurance cost). *Choosing*
which Tier 1/2 Condition to apply is left to the caller — in the live
engine that choice belongs to the attacking player or the MM (PHB III.3:
"10+ = Tier 2 Condition, attacker chooses which"); in the simulator it is
AI policy (`tools.combat_sim.choose_pc_reaction` and friends). combat.py
never makes that choice itself.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional, Protocol

from app.game import engine as _engine
from app.game.dice import DiceSpec


class Combatant(Protocol):
    """Structural protocol satisfied by `Character`, `Enemy`, and the
    simulator's `PCState`/`EnemyState`.

    Functions that need posture, armor, or Endurance/Resolve take them as
    explicit parameters instead of reading them off this object, because
    the field names and types diverge across the four implementations
    (`Character.endurance_max` is a method; `Enemy` has no `posture`).
    `conditions` is the one field every combatant shares, and the only one
    these functions mutate directly.
    """

    conditions: list[str]


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class RollOutcome:
    outcome: str  # "full_success" | "partial_success" | "failure"
    dice: list[int]
    total: int


@dataclass
class ConditionResult:
    """Result of `apply_condition`."""

    applied: bool  # False only when the application escalated to Broken instead of landing
    condition: Optional[str]
    tier: int
    broken: bool


@dataclass
class StrikeOptions:
    difficulty: str = "Standard"
    extra_dice: int = 0  # from Sparks + Press, already decided by the caller


@dataclass
class StrikeRoll:
    """Result of the attack-roll portion of a Strike (`resolve_strike`)."""

    outcome: str  # "full_success" | "partial_success" | "failure"
    dice: list[int]
    total: int
    condition_tier: int  # the tier a landed hit would inflict, BEFORE reaction/armor; 0 on failure
    mook_removed: bool  # True if outcome != "failure" (any success removes a Mook)


@dataclass
class ReactionRoll:
    outcome: Optional[str]  # roll outcome, or None if the reaction doesn't roll (Absorb/Intercept)
    dice: list[int]
    total: int
    cost: int  # Endurance actually spent


@dataclass
class ResolveDamageResult:
    """Result of `apply_resolve_damage`."""

    resolve_current: int
    depletion: int
    defeated: bool  # True when resolve_current has reached 0
    phase_index: Optional[int]  # index into the caller's `phase_thresholds`, or None


@dataclass
class ArmorDowngradeResult:
    """Result of `armor_downgrade` (D2 — PC per-scene downgrade budget)."""

    tier: int  # tier after downgrade; 0 = fully negated
    downgrades_remaining: int  # budget left after this call
    downgraded: bool  # True iff a downgrade was actually spent this call


# ---------------------------------------------------------------------------
# Ruleset lookups — no literals; everything below reads facet.yaml
# ---------------------------------------------------------------------------

def _tier1_ids(ruleset) -> set[str]:
    return {c.id for c in ruleset.combat.conditions.tier1}


def _tier2_ids(ruleset) -> set[str]:
    return {c.id for c in ruleset.combat.conditions.tier2}


def condition_tier(condition_id: str, ruleset) -> int:
    """Return the tier (1/2/3) a condition ID belongs to, or 0 if unknown."""
    if condition_id in _tier1_ids(ruleset):
        return 1
    if condition_id in _tier2_ids(ruleset):
        return 2
    for c in ruleset.combat.conditions.tier3:
        if c.id == condition_id:
            return 3
    return 0


def _strike_outcome_tier(outcome: str, ruleset) -> int:
    entry = ruleset.combat.strike_outcomes.get(outcome, {})
    return entry.get("condition_tier", 0)


def posture_offense_modifier(posture: str, ruleset) -> Optional[int]:
    """Offense modifier for a posture, or None if the posture cannot attack (Withdrawn)."""
    posture_def = ruleset.combat.postures.get(posture, {})
    return posture_def.get("offense_modifier", 0)


def reaction_cost(
    reaction: str, posture: str, ruleset, is_first_reaction: bool = True,
) -> int:
    """Endurance cost of a reaction, adjusted for posture.

    Withdrawn grants free reactions regardless of the base cost.

    K1 (BRIEF D8, adopted after Gate G3 — research/simulation_log.md
    Series 8): a posture whose `reaction_cost_modifier_applies` is
    `first_reaction_only` (Aggressive, by default) only pays its
    surcharge on the combatant's first reaction of the exchange; every
    reaction after that is costed with the modifier zeroed out. Other
    postures (Measured, Defensive) apply their modifier on every
    reaction, `first_reaction_only` or not, since they have no
    surcharge to soften.

    `is_first_reaction` defaults to True so a caller that doesn't track
    per-exchange reaction counts (an enemy's Parry, in the simulator)
    sees unchanged, always-pays-the-surcharge behaviour.
    """
    posture_def = ruleset.combat.postures.get(posture, {})
    if posture_def.get("free_reactions"):
        return 0
    base = ruleset.combat.reactions.get(reaction, 0)
    modifier = posture_def.get("reaction_cost_modifier", 0) or 0
    applies = posture_def.get("reaction_cost_modifier_applies", "always")
    if applies == "first_reaction_only" and not is_first_reaction:
        modifier = 0
    return max(0, base + modifier)


def withdrawn_recovery_amount(ruleset) -> int:
    return ruleset.combat.endurance.recovery_withdrawn


# ---------------------------------------------------------------------------
# Dice
# ---------------------------------------------------------------------------

def roll(modifier: int, difficulty: str, ruleset, extra_dice: int = 0) -> RollOutcome:
    """Roll the ruleset's dice formula (default 2d6) + modifier + difficulty,
    with `extra_dice` added and the lowest dropped (Sparks/Press).

    Uses the same ruleset-driven helpers as `engine.resolve_roll` for dice
    sizing, the difficulty modifier, and outcome thresholds — it does not
    reimplement them.
    """
    diff_mod = _engine._get_difficulty_modifier(difficulty, ruleset)
    dice_spec = DiceSpec.parse(ruleset.roll_resolution.dice if ruleset.roll_resolution else "2d6")
    total_dice = dice_spec.count + extra_dice
    dice_rolled = sorted(random.randint(1, dice_spec.sides) for _ in range(total_dice))
    kept = dice_rolled[extra_dice:]
    total = sum(kept) + modifier + diff_mod
    outcome, _, _ = _engine._determine_outcome(total, ruleset)
    return RollOutcome(outcome=outcome, dice=kept, total=total)


# ---------------------------------------------------------------------------
# Strike / reaction resolution
# ---------------------------------------------------------------------------

def resolve_strike(
    modifier: int,
    posture: str,
    conditions: list[str],
    ruleset,
    opts: StrikeOptions = StrikeOptions(),
) -> StrikeRoll:
    """Resolve a Strike's attack roll: posture offense modifier and the
    Staggered penalty ("−1 to offensive rolls") applied to `modifier`, then
    rolled.

    Does not apply a condition to the target or remove a Mook — see the
    module scope note. `mook_removed` tells the caller whether the target
    *would* be removed if it is a Mook; checking the target's tier is the
    caller's job.
    """
    offense_mod = posture_offense_modifier(posture, ruleset) or 0
    total_mod = modifier + offense_mod
    if "staggered" in conditions:
        total_mod -= 1

    result = roll(total_mod, opts.difficulty, ruleset, opts.extra_dice)

    return StrikeRoll(
        outcome=result.outcome,
        dice=result.dice,
        total=result.total,
        condition_tier=_strike_outcome_tier(result.outcome, ruleset),
        mook_removed=(result.outcome != "failure"),
    )


def resolve_reaction(
    reaction: str,
    modifier: int,
    posture: str,
    difficulty: str,
    ruleset,
    is_first_reaction: bool = True,
) -> ReactionRoll:
    """Resolve a reaction (dodge/parry/absorb/intercept): pay the Endurance
    cost, then roll if the reaction is active (dodge/parry). Absorb and
    Intercept do not roll.
    """
    cost = reaction_cost(reaction, posture, ruleset, is_first_reaction)
    if reaction not in ("dodge", "parry"):
        return ReactionRoll(outcome=None, dice=[], total=0, cost=cost)

    result = roll(modifier, difficulty, ruleset)
    return ReactionRoll(outcome=result.outcome, dice=result.dice, total=result.total, cost=cost)


# ---------------------------------------------------------------------------
# Armor — PC per-scene downgrade budget (D2, DESIGN §4.2)
# ---------------------------------------------------------------------------

def armor_budget(armor: Optional[str], ruleset) -> int:
    """Starting per-scene Condition-downgrade budget for an armor type.

    Read from `combat.armor.<type>.downgrades_per_scene` — never hardcoded.
    Unarmored (or an unrecognised armor string) gets 0. Used both to
    initialise a combatant's `armor_downgrades_remaining` when a scene's
    first combat starts, and to reset it when the scene ends — the same
    starting value either way. The budget itself is **not** owned by this
    module (see `armor_downgrade`'s docstring); the caller tracks the
    counter and passes it in.
    """
    if armor not in ("light", "heavy"):
        return 0
    return getattr(ruleset.combat.armor, armor).downgrades_per_scene


def armor_downgrade(
    tier: int, armor: Optional[str], downgrades_remaining: int, ruleset,
) -> ArmorDowngradeResult:
    """Downgrade an incoming Condition tier using a PC's per-scene armor
    budget (D2).

    Light armor downgrades the first `downgrades_per_scene` (2) Conditions
    a PC receives *per scene* by one tier each (Tier 2 -> Tier 1; Tier 1 ->
    none/absorbed). Heavy does the same for its first 4. This is a finite
    budget, not a standing gate: once `downgrades_remaining` reaches 0,
    further incoming Conditions pass through unmodified for the rest of the
    scene.

    Pure function — the budget is a counter the caller owns
    (`Character.armor_downgrades_remaining`); this returns the post-call
    count rather than mutating anything, exactly like `apply_resolve_damage`
    reports a new pool value instead of holding one. It does **not** reset
    on `end_exchange` — only at end of scene, via `armor_budget`. See
    DESIGN §4.2: against a single boss landing one Tier 2 per exchange, an
    unlimited per-exchange downgrade (the shape this replaces) never runs
    out, so an armored PC could never be Broken — the bug this budget
    fixes.

    Superseded shape (do not resurrect): the pre-D2 version gated *which*
    tier each armor type touched (light only Tier 2, heavy only Tier 3),
    with no limit on how many times it could apply. See
    `test_combat_characterization.py` for the retired semantics and why
    they were a bug, not a feature.
    """
    if armor not in ("light", "heavy") or downgrades_remaining <= 0 or tier <= 0:
        return ArmorDowngradeResult(
            tier=tier, downgrades_remaining=downgrades_remaining, downgraded=False,
        )

    tiers_reduced = getattr(ruleset.combat.armor, armor).tiers_reduced
    new_tier = max(0, tier - tiers_reduced)
    return ArmorDowngradeResult(
        tier=new_tier, downgrades_remaining=downgrades_remaining - 1, downgraded=True,
    )


# ---------------------------------------------------------------------------
# Enemy Resolve — D1 (DESIGN §4.1)
# ---------------------------------------------------------------------------

_OUTCOME_ORDER = ["failure", "partial_success", "full_success"]


def phase_crossed(
    resolve_before: int, resolve_after: int, phase_thresholds: Optional[list[int]],
) -> Optional[int]:
    """Return the index of the phase whose threshold this Resolve change
    crossed (`resolve_before` strictly above it, `resolve_after` at-or-below
    it), or `None` if none crossed.

    `phase_thresholds` are each `PhaseDef.resolve_threshold`, in the order
    the enemy's phases are defined. Callers that already track the enemy's
    prior Resolve value (a WebSocket handler, `apply_resolve_damage`) use
    this to detect a crossing without any extra state on the enemy —
    "fires exactly once" falls out of the caller only ever moving Resolve
    downward and comparing against the value it held last time.
    """
    for i, threshold in enumerate(phase_thresholds or []):
        if resolve_before > threshold >= resolve_after:
            return i
    return None


def apply_resolve_damage(
    resolve_current: int,
    outcome: str,
    ruleset,
    phase_thresholds: Optional[list[int]] = None,
) -> ResolveDamageResult:
    """Deplete an enemy's Resolve pool from a PC Strike outcome (D1).

    Depletion is read from `combat.enemy_durability.strike_depletion`
    (full_success=2, partial_success=1, failure=0 by default) — never
    hardcoded. Resolve floors at 0, which is `defeated`.

    See `phase_crossed` for how `phase_index` is derived.
    """
    depletion = getattr(ruleset.combat.enemy_durability.strike_depletion, outcome, 0)
    new_resolve = max(0, resolve_current - depletion)

    return ResolveDamageResult(
        resolve_current=new_resolve,
        depletion=depletion,
        defeated=new_resolve <= 0,
        phase_index=phase_crossed(resolve_current, new_resolve, phase_thresholds),
    )


def enemy_armor_resolve_bonus(armor: Optional[str], ruleset) -> int:
    """Flat Resolve bonus an enemy's armor grants at combat start (D1).

    Read from `combat.enemy_durability.armor_resolve_bonus` — light +1,
    heavy +2 by default, never hardcoded. Numerically equal to the
    Threat Rating formula's `armor_bonus` term (the TR identity, DESIGN
    §4.1): `TR = offense_value + resolve + armor_bonus + technique_bonus`.
    """
    return getattr(ruleset.combat.enemy_durability.armor_resolve_bonus, armor or "none", 0)


def mook_removed(outcome: str, armored: bool, ruleset) -> bool:
    """Whether a Mook Strike outcome removes it (D1).

    A Mook has no Resolve pool: any success (7+) removes it. An armored
    Mook requires a full success (10+) — the thresholds are read from
    `combat.enemy_durability.mook_removed_on` / `armored_mook_removed_on`.
    """
    threshold = (
        ruleset.combat.enemy_durability.armored_mook_removed_on
        if armored
        else ruleset.combat.enemy_durability.mook_removed_on
    )
    try:
        return _OUTCOME_ORDER.index(outcome) >= _OUTCOME_ORDER.index(threshold)
    except ValueError:
        return False


def target_strike_difficulty(base_difficulty: str, target_conditions: list[str], ruleset) -> str:
    """A target holding a Tier 2 rider Condition (Staggered/Cornered) is
    Easy to Strike (D1) — this is what makes the attacker's 10+ choice on
    the *previous* Strike real: deplete Resolve now, or set up an Easy
    follow-up for the rest of the party.
    """
    if any(c in _tier2_ids(ruleset) for c in target_conditions):
        return "Easy"
    return base_difficulty


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def apply_condition(
    conditions: list[str],
    condition: str,
    tier: int,
    ruleset,
    *,
    is_rider: bool = False,
) -> ConditionResult:
    """Apply a condition to a combatant's `conditions` list in place.

    A second Tier 2+ condition of the *same* type escalates to Broken
    instead of being added again (D5 ledger row 2: same type, not "any
    second Tier 2"). There is no special handling for 0 Endurance — an
    Absorb taken at 0 Endurance applies the incoming tier unmodified (F5
    retired, DESIGN §4.3): under D1 enemies have no Condition kill-track,
    and under D2 armored PCs are already breakable without it.

    `is_rider` marks an enemy Condition applied as a Strike rider (D1):
    riders never escalate to Broken, since Resolve — not Conditions — is
    what defeats an enemy. Enemy armor does not downgrade rider Conditions
    (`armor_downgrade` is PC-only, D2); this flag is the only special
    handling riders get.

    The caller is responsible for not calling this on an already-Broken or
    already-removed target.
    """
    if not is_rider and tier >= 2 and condition in conditions:
        return ConditionResult(applied=False, condition=condition, tier=tier, broken=True)

    conditions.append(condition)
    return ConditionResult(applied=True, condition=condition, tier=tier, broken=False)


def end_exchange(conditions: list[str], ruleset) -> list[str]:
    """Clear Tier 1 conditions at end of exchange. Tier 2+ conditions
    persist until treated. Returns the condition IDs that were cleared.
    Mutates `conditions` in place.

    Withdrawn Endurance recovery is not handled here — the Endurance field
    name and max-value lookup differ across combatant types (see
    `Combatant`); use `withdrawn_recovery_amount(ruleset)` and apply it to
    the caller's own Endurance field, exactly as `end_exchange` here only
    ever touched conditions.
    """
    tier1_ids = _tier1_ids(ruleset)
    cleared = [c for c in conditions if c in tier1_ids]
    conditions[:] = [c for c in conditions if c not in tier1_ids]
    return cleared
