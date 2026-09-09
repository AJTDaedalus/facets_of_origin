"""Pure, synchronous combat-resolution rules (PHB III.3).

Combat rules live here; `app/api/websocket.py` and `tools/combat_sim.py`
call into it rather than carrying their own copies. See
`docs/DESIGN_v0.3_ruleset_revision.md` §2.1 and TASKS `WS-A0`.

The two callers do not consume the same surface, and the difference is
load-bearing. The simulator drives the whole module, `resolve_strike` and
`resolve_reaction` included. The live engine calls the *lookups and
consequences* (`offense_modifier`, `reaction_cost`, `condition_tier`,
`apply_condition`, `resolve_incoming_condition`, `armor_budget`,
`end_exchange`, `phase_crossed`); its dice still go through
`engine.resolve_roll`/`RollRequest`, because a Strike there is spread
across two player/MM actions rather than one call (LOG WS-A0, judgment
call #3). So `resolve_strike`/`resolve_reaction` have no production caller.

**Put shared rules in the helpers, never inside `resolve_strike`.** That
asymmetry is a standing divergence risk: a rule written into
`resolve_strike` reaches the simulator and never a real table. It has
already happened once — the Staggered −1 offensive penalty lived there as
a literal, so a Staggered PC was penalised in every simulation and at no
actual table (DECISIONS R1). It now lives in `offense_modifier`, which
both callers use, and `resolve_strike` merely calls that.

No I/O, no async, no session objects. Every function takes plain state
(lists, ints, strings) plus a `MergedRuleset`, and returns a result
dataclass. Constants — reaction costs, condition tier IDs, posture and
Condition modifiers, Withdrawn recovery, strike-outcome tiers — are read
from the ruleset, not hardcoded. One literal remains: the `dodge`/`parry`
"this reaction rolls" test in `resolve_reaction`.

Scope note: `resolve_strike`/`resolve_reaction` resolve *rolls and their
immediate rule consequences* (mook removal, Endurance cost). *Choosing*
what to do with an outcome is left to the caller — against a character,
which Tier 1/2 Condition to apply (PHB III.3: "10+ = Tier 2 Condition,
attacker chooses which"); against an enemy, whether a full success leaves
it Open (K-6/D4, attacker's option). In the simulator both are AI policy
(`tools.combat_sim.choose_pc_reaction` and friends). combat.py never
makes those choices itself.
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
class FinalBlowResult:
    """Result of `apply_final_blow_removal` (B4 Q3 — *The Final Blow*).

    Deliberately its own type, not a reuse of `ResolveDamageResult`: the two
    must be distinguishable at the type level, not just by field values, so
    a transcript or a future sim series can tell a licensed-override removal
    apart from an ordinary Strike defeating an enemy at 0 Resolve on sight —
    without relying on a caller remembering to check a `cause` string.
    `cause` is carried anyway, for callers (the WS broadcast, the transcript
    log) that want a machine-readable label rather than a type check.
    """

    resolve_current: int  # always 0 — the target is removed
    depletion: int  # however much Resolve this removal actually took off, for the transcript
    defeated: bool  # always True
    phase_index: Optional[int]  # index into the caller's `phase_thresholds`, or None
    cause: str = "final_blow"  # distinguishes this event from an ordinary Resolve-0 defeat


@dataclass
class ArmorDowngradeResult:
    """Result of `armor_downgrade` (D2 — PC per-scene downgrade budget)."""

    tier: int  # tier after downgrade; 0 = fully negated
    downgrades_remaining: int  # budget left after this call
    downgraded: bool  # True iff a downgrade was actually spent this call


@dataclass
class IncomingConditionResult:
    """Result of `resolve_incoming_condition` — armor and reaction downgrades
    combined under PHB III.3's non-stacking rule."""

    tier: int  # final tier after the single greater reduction; 0 = negated
    downgrades_remaining: int  # armor budget left after this call
    armor_spent: bool  # True iff an armor charge was actually consumed
    reaction_applied: bool  # True iff the reaction supplied the reduction


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


def condition_offense_modifier(conditions: list[str], ruleset) -> int:
    """Total offensive-roll modifier from the conditions a combatant holds.

    Read from each condition's `offense_modifier` in `facet.yaml` (Staggered
    is −1; everything else 0). Unknown condition IDs contribute nothing.
    """
    by_id = {
        c.id: c
        for tier in (
            ruleset.combat.conditions.tier1,
            ruleset.combat.conditions.tier2,
            ruleset.combat.conditions.tier3,
        )
        for c in tier
    }
    return sum(by_id[c].offense_modifier for c in conditions if c in by_id)


def offense_modifier(posture: str, conditions: list[str], ruleset) -> Optional[int]:
    """Total modifier on an offensive roll: posture plus any Condition penalty.
    `None` means the posture cannot attack at all (Withdrawn).

    Both callers go through this. It exists because the posture modifier and
    the Staggered penalty were applied in different places — the live engine
    applied only the former, the simulator (via `resolve_strike`) applied
    both — so a Staggered PC was penalised in simulation and not at the table.
    """
    posture_mod = posture_offense_modifier(posture, ruleset)
    if posture_mod is None:
        return None
    return posture_mod + condition_offense_modifier(conditions, ruleset)


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
    min_cost = posture_def.get("min_reaction_cost", 0)
    return max(min_cost, base + modifier)


def withdrawn_recovery_amount(ruleset) -> int:
    return ruleset.combat.endurance.recovery_withdrawn


def apply_withdrawn_recovery(current: int, pool_max: int, ruleset) -> int:
    """Withdrawn's end-of-exchange recovery, **up to your pool** (III.3,
    D5): returns the new Endurance value, clamped at `pool_max`. The clamp
    is a rule — callers (the WS end-exchange handler, the simulator loop)
    apply this function to their own Endurance field instead of re-deriving
    `min(max, current + amount)` inline.
    """
    return min(pool_max, current + withdrawn_recovery_amount(ruleset))


def exchange_uncontested(offensive_actions) -> bool:
    """The uncontested exchange (III.3, K-2/D5): an exchange in which no
    player character took an offensive action lets the situation advance
    for free — the MM may reposition, reinforce, progress a clock, or take
    the objective, no roll.

    `offensive_actions` is one truthy/falsy entry per offensive action
    considered (or per PC: "did they act offensively?"). This is the
    rule's only home — the WS end-exchange handler and any sim series read
    it from here, never re-derive it.
    """
    return not any(offensive_actions)


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
    """Resolve a Strike's attack roll: `offense_modifier` (posture plus any
    Condition penalty, e.g. Staggered's −1) applied to `modifier`, then rolled.

    Simulator-facing. The live engine composes the same roll from
    `offense_modifier` + `engine.resolve_roll` — see the module docstring, and
    keep any new offensive rule in `offense_modifier` so both paths get it.

    Does not apply a condition to the target or remove a Mook — see the
    module scope note. `mook_removed` tells the caller whether the target
    *would* be removed if it is a Mook; checking the target's tier is the
    caller's job. Note it ignores armor: an armored Mook needs a full success,
    so callers with a target in hand should use `mook_removed(...)` instead.
    """
    offense_mod = offense_modifier(posture, conditions, ruleset) or 0
    result = roll(modifier + offense_mod, opts.difficulty, ruleset, opts.extra_dice)

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


def resolve_incoming_condition(
    tier: int,
    armor: Optional[str],
    downgrades_remaining: int,
    ruleset,
    *,
    reaction_downgraded: bool = False,
) -> IncomingConditionResult:
    """Reduce an incoming Condition tier by armor and/or a partial reaction,
    applying PHB III.3's non-stacking rule.

    "Armor downgrades and successful reaction downgrades (Dodge 7-9, Parry
    7-9) do not stack. Apply the greater reduction only." Both reduce by one
    tier, so a partial Parry in light armor against a Tier 2 lands as **Tier
    1** — not negated. Callers pass the *raw* incoming tier plus whether a
    reaction already downgraded it; they must not pre-reduce the tier
    themselves, or the two reductions silently compound.

    When the reaction has already applied the greater (here, equal) reduction,
    the armor charge is **not** spent: armor softened nothing the reaction had
    not already softened, and the per-scene budget is what keeps an armored PC
    breakable (D2, DESIGN §4.2). Spending a charge for no benefit would drain
    that budget faster than the design intends. The PHB fixes the resulting
    *tier* but is silent on whether the charge is consumed; this is the
    reading consistent with armor being "a finite number of incoming
    Conditions it can soften" (PHB III.3) — a charge that softens nothing is
    not spent.

    Pure: the budget counter stays with the caller, as in `armor_downgrade`.
    """
    if reaction_downgraded:
        reduction = ruleset.combat.armor.reaction_downgrade_tiers
        return IncomingConditionResult(
            tier=max(0, tier - reduction),
            downgrades_remaining=downgrades_remaining,
            armor_spent=False,
            reaction_applied=True,
        )

    downgrade = armor_downgrade(tier, armor, downgrades_remaining, ruleset)
    return IncomingConditionResult(
        tier=downgrade.tier,
        downgrades_remaining=downgrade.downgrades_remaining,
        armor_spent=downgrade.downgraded,
        reaction_applied=False,
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


def apply_final_blow_removal(
    resolve_current: int,
    phase_thresholds: Optional[list[int]] = None,
) -> FinalBlowResult:
    """Resolve *The Final Blow*'s target removal (B4 Q3) as a defeat event
    through the canonical defeat path — never a raw `resolve_current = 0`
    write.

    P11 invariant: every `resolve_current` mutation routes through
    `phase_crossed`, the same primitive `apply_resolve_damage` uses to
    detect a Boss phase crossing from an ordinary Strike. A raw write would
    skip that call and could silently miss a phase change the removal
    triggers in passing (e.g. a Boss whose Reduced Mode threshold sits above
    0) — bypassing phase logic and corrupting anything reading the
    transcript afterward. This function is *not* `apply_resolve_damage`
    with a bigger number: it works on any target regardless of remaining
    Resolve (Bosses included, per B4/the BRIEF's Q3 ruling — the removal is
    a licensed override, not depletion), and it returns the distinct
    `FinalBlowResult` type so a capstone removal can never be mistaken for,
    or silently merged with, an ordinary Resolve-0 defeat.

    The once-per-session gate, the Spark spend, and the "succeed" (7+)
    requirement are the caller's job (`websocket._handle_*`) — this
    function only resolves the mechanical consequence once a caller has
    already established the Technique fires. It also does not decide
    whether the removal *commits*: MM confirmation gates that at the
    caller, because auto-apply (B4's UX ruling) governs difficulty steps,
    not actor removal.

    Args:
        resolve_current: The target's Resolve immediately before removal.
        phase_thresholds: The target's `PhaseDef.resolve_threshold` values,
            in definition order, or `None`/empty for a target with no
            phases (Mooks, Named NPCs, most Bosses outside a phase block).

    Returns:
        A `FinalBlowResult` with `resolve_current=0`, `defeated=True`, and
        `phase_index` set if the drop to 0 crosses a phase boundary.
    """
    new_resolve = 0
    return FinalBlowResult(
        resolve_current=new_resolve,
        depletion=max(0, resolve_current),
        defeated=True,
        phase_index=phase_crossed(resolve_current, new_resolve, phase_thresholds),
    )


def maneuver_target_difficulty(outcome: str, base_difficulty: str, ruleset) -> str:
    """Effect of a Maneuver's outcome on rolls against the target (III.3):
    a 10+ makes rolls against the target Easy (until the situation
    changes — tracked by the caller, not here); a 7-9 leaves the target at
    the base difficulty; a 6- backfires and has no effect on the target.
    Read from `combat.actions.maneuver`, not hardcoded.
    """
    effect = getattr(ruleset.combat.actions.maneuver, outcome, "standard")
    if effect == "easy":
        return "Easy"
    return base_difficulty


def support_bonus_modes(ruleset) -> list[str]:
    """The non-stacking bonus types a Support action may grant an ally's
    very next roll (III.3) — the supporting character's choice. Read from
    `combat.actions.support.modes`, not a hardcoded tuple.
    """
    return list(ruleset.combat.actions.support.modes)


def enemy_incoming_condition_tier(enemy_type: str, ruleset) -> int:
    """Condition tier a PC takes from an enemy attack, by enemy type (III.3,
    Incoming Condition Tier). Read from `combat.enemy_attacks.incoming_tier`,
    not hardcoded — Mook 1, Named/Boss 2 by default.
    """
    return getattr(ruleset.combat.enemy_attacks.incoming_tier, enemy_type, 1)


def enemy_posture_reaction_difficulty(
    base_difficulty: str, enemy_type: str, enemy_posture: Optional[str], ruleset,
) -> str:
    """Shift a PC's reaction difficulty by the attacking enemy's Posture
    (III.3, Enemy Posture and Reaction Difficulty): Aggressive one step
    harder, Defensive one step easier, Measured unchanged. Mooks never
    declare Posture — no shift applies regardless of what is passed.
    """
    if enemy_type == "mook" and not ruleset.combat.enemy_attacks.mook_declares_posture:
        return base_difficulty

    shift = getattr(
        ruleset.combat.enemy_attacks.posture_reaction_shift, enemy_posture or "measured", "none",
    )
    if shift == "harder":
        return _engine._step_difficulty_harder(base_difficulty, ruleset)
    if shift == "easier":
        return _engine._step_difficulty_easier(base_difficulty, ruleset)
    return base_difficulty


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


def can_apply_open(outcome: str, ruleset) -> bool:
    """Whether a Strike outcome is eligible to additionally leave the enemy
    Open, on top of Resolve depletion (III.3 / K-6/D4 — attacker's option,
    "on a full success only"). Read from `combat.enemy_durability.open_on`,
    not hardcoded, so a homebrew ruleset could widen or narrow it.

    Whether the attacker *takes* the option is the caller's choice (player
    at a table, AI policy in the simulator) — this function only rules on
    eligibility. The player narrates what Open looks like (staggered,
    cornered, blinded, disarmed); the mechanics carry one tag.
    """
    return outcome == ruleset.combat.enemy_durability.open_on


def open_clear_mode(ruleset) -> str:
    """How the Open tag clears — read from
    `combat.enemy_durability.open_clears`. The base ruleset's
    `"enemy_action"` means: ONLY by the enemy visibly spending its action.
    Open never clears at end of exchange (`end_exchange` touches
    Conditions, and Open is not a Condition), and nothing the PCs do
    removes it. Callers (WS handler, simulator enemy AI) gate their
    clearing paths on this value rather than hardcoding the lifecycle.
    """
    return ruleset.combat.enemy_durability.open_clears


def open_clears_at_end_of_exchange(ruleset) -> bool:
    """Whether the Open tag expires with the Tier 1 Conditions (R2), rather
    than only when the enemy visibly spends its action.

    The one-line predicate every caller actually wants, so no caller has to
    compare `open_clear_mode`'s string itself and none of them can drift.
    """
    return open_clear_mode(ruleset) == "end_of_exchange"


def strike_riders(ruleset) -> list:
    """The rider menu a full-success Strike chooses from (R3), read from
    `combat.enemy_durability.strike_riders`. A setting may trim or extend
    it, so nothing downstream may hardcode the three the base book prints.
    """
    return list(ruleset.combat.enemy_durability.strike_riders)


def rider_menu(outcome: str, target_removed: bool, ruleset) -> list:
    """The riders actually on offer for this Strike result.

    Empty unless the Strike was a full success (`can_apply_open`'s
    eligibility — the rider replaced the bare Open option and inherits its
    tier), and empty when the target was removed: against a Mook a 10+ takes
    it off the board, and a tempo tag on a departed enemy is nothing.
    """
    if target_removed or not can_apply_open(outcome, ruleset):
        return []
    return strike_riders(ruleset)


def _rider_def(rider_id: str, ruleset):
    for rider in strike_riders(ruleset):
        if rider.id == rider_id:
            return rider
    raise ValueError(
        f"No rider '{rider_id}' in this ruleset's menu "
        f"({', '.join(r.id for r in strike_riders(ruleset))}). "
        "The menu is data (combat.enemy_durability.strike_riders); a rider "
        "the book does not print must not be applied."
    )


def apply_rider(rider_id: str, target, ruleset, *, ally=None,
                exchange_no: int = 1) -> list[str]:
    """Apply one full-success Strike rider and report the tags it wrote.

    The first post-roll decision in combat that is not "pay or don't": the
    attacker chooses after seeing the 10+, and all three options are things
    the fight already let them do, folded into the roll everyone makes.

    `target` is the enemy that was Struck; `ally` is the ally named by
    Cover. Duck-typed on both, for the same reason `expire_end_of_exchange`
    is: the app's models and the simulator's dataclasses carry the same tags
    and the rule lives here once.

    Cover buys a reaction's Endurance cost, never its outcome — the reaction
    is still rolled. That is what keeps it from being a free success, and it
    is the line the acceptance's PCs-Broken gate is watching.
    """
    rider = _rider_def(rider_id, ruleset)

    if rider.effect == "easy_tag":
        target.open = True
        return ["open"]

    if rider.effect == "easy_tag_next_roll":
        # "this exchange or next" — so it survives the end of the exchange
        # it was applied in and expires at the end of the following one.
        target.position = {"uses": 1, "expires_after_exchange": exchange_no + 1}
        return ["position"]

    if rider.effect == "free_reaction_ally":
        if ally is None:
            raise ValueError(
                "Cover names an ally; apply_rider needs `ally=` to know whose "
                "reaction is free."
            )
        ally.free_reaction = True
        return ["cover"]

    raise ValueError(f"Rider effect '{rider.effect}' has no engine behaviour.")


def has_easy_tag(target) -> bool:
    """Whether this target is currently Easy to Strike from a rider — Open,
    or a Position that has not been spent.

    Open and Position never stack: both feed the single `easy_tag` input to
    `compose_difficulty`, and III.1's precedence makes Easy an absolute
    override. This function is the reason that stays true in one place.
    """
    if getattr(target, "open", False):
        return True
    position = getattr(target, "position", None)
    return bool(position) and position.get("uses", 0) > 0


def consume_position(target) -> bool:
    """Spend a Position tag on the roll that just used it. Returns whether
    there was one to spend."""
    position = getattr(target, "position", None)
    if not position or position.get("uses", 0) <= 0:
        return False
    position["uses"] -= 1
    return True


def consume_free_reaction(character) -> bool:
    """Spend Cover on a reaction. Returns whether the reaction was free.

    One reaction, and only for the ally Cover named. The roll still happens
    — this waives the Endurance cost, not the result.
    """
    if not getattr(character, "free_reaction", False):
        return False
    character.free_reaction = False
    return True


def expire_end_of_exchange(target, ruleset, *, exchange_no: int = None) -> list[str]:
    """Expire end-of-exchange combat *tags* on a combatant, and report which
    ones went. Returns the tag names cleared, so the caller can narrate them.

    The sibling of `end_exchange`, which clears Conditions. Open is not a
    Condition — it is a tag on an enemy — so it needs its own expiry, and
    `end_exchange`'s signature (a bare condition list) has several callers
    and is deliberately left alone.

    Duck-typed on the target: the app's `Enemy` and the simulator's
    `EnemyState` are different types carrying the same tags, and the rule
    must live here once rather than once in each.

    Under `open_clears: enemy_action` this function must leave Open standing —
    the mode is the authority on the lifecycle, and end of exchange does not
    get to clear the tag behind its back.

    `exchange_no` is what lets Position expire on the right beat; without it
    Position is left alone rather than guessed at, so a pre-R3 caller that
    only cares about Open keeps working unchanged.
    """
    expired: list[str] = []

    if getattr(target, "open", False) and open_clears_at_end_of_exchange(ruleset):
        target.open = False
        expired.append("open")

    # Position outlives the exchange it was taken in ("this exchange or
    # next"), so it expires only once `exchange_no` has reached the
    # deadline written on it. Called without an exchange number — the
    # pre-R3 call shape — it is left alone rather than guessed at.
    position = getattr(target, "position", None)
    if position and exchange_no is not None:
        if exchange_no >= position.get("expires_after_exchange", 0):
            target.position = None
            expired.append("position")

    if getattr(target, "free_reaction", False):
        target.free_reaction = False
        expired.append("cover")

    return expired


def target_strike_difficulty(base_difficulty: str, target_open: bool, ruleset) -> str:
    """An Open enemy is Easy to Strike for everyone (K-6/D4) — this is what
    makes the attacker's 10+ option on the *previous* Strike real: leave
    the enemy Open now and every ally's follow-up is Easy, until the enemy
    visibly spends its action recovering.

    Composed through `compose_difficulty` as an Easy-tag source (III.1
    precedence step 2) — the override is absolute and does not stack with
    itself, and this function must never carry its own copy of that rule.
    """
    label, _ = compose_difficulty(base_difficulty, ruleset=ruleset, easy_tag=target_open)
    return label


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def apply_condition(
    conditions: list[str],
    condition: str,
    tier: int,
    ruleset,
) -> ConditionResult:
    """Apply a condition to a character's `conditions` list in place.

    A second Tier 2+ condition of the *same* type escalates to Broken
    instead of being added again (D5 ledger row 2: same type, not "any
    second Tier 2"). There is no special handling for 0 Endurance — an
    Absorb taken at 0 Endurance applies the incoming tier unmodified (F5
    retired, DESIGN §4.3): under D1 enemies have no Condition kill-track,
    and under D2 armored PCs are already breakable without it.

    Character-target only since K-6/D4: a Strike against an enemy never
    hangs a Condition — a full success may leave it Open instead
    (`can_apply_open`), and Resolve is what defeats it. The retired
    `is_rider` flag marked the enemy-rider path and died with the menu.

    The caller is responsible for not calling this on an already-Broken or
    already-removed target.
    """
    if tier >= 2 and condition in conditions:
        return ConditionResult(applied=False, condition=condition, tier=tier, broken=True)

    conditions.append(condition)
    return ConditionResult(applied=True, condition=condition, tier=tier, broken=False)


# ---------------------------------------------------------------------------
# Difficulty composition — B4 Q1 (DESIGN_technique_difficulty.md §2.2)
# ---------------------------------------------------------------------------

def apply_character_difficulty_step(
    declared_label: str,
    character,
    context: dict,
    ruleset,
) -> tuple[str, Optional[str]]:
    """Compose the MM's declared difficulty label with at most one
    character-side Technique step (DECISIONS.md B4, Q1).

    This lives here, not in `websocket.py` or `tools/combat_sim.py`, because
    it is a rule: `CLAUDE.md`'s iron law is that the simulator may only
    *drive* `combat.py`, never carry its own copy of a rule, and this project
    has already been burned once by exactly that divergence (DECISIONS R1).
    Every caller — the three WS handlers this cycle wires (strike, generic
    roll, reaction) and any future sim series — must call this function
    rather than re-deriving a step inline.

    **Order** (non-negotiable, B4): `declared_label` is the MM's situational
    call, already resolved, and is never second-guessed here. A character-side
    step applies to it second. The ladder then clamps via
    `engine._step_difficulty_easier`/`_harder`, which already saturate at
    the four-rung ladder's ends (Easy stays Easy; Very Hard stays Very Hard)
    — those are ladder primitives; this function only composes them.

    **Guardrail**: character-side steps never stack, whatever their source —
    at most one per roll. Specialty and Technique share this one pool
    (III.1 §Difficulty, T2.4/D2): a declared Specialty
    (`context["specialty_declared"]` truthy, on a character whose
    `.specialty` is set) is a candidate exactly like a Technique, and a
    Hard roll reaches Standard via either source, never Easy via both.
    `context` may make several sources qualify at once; only one step is
    ever applied. Precedence is deterministic so the roll banner names a
    stable source: a player-declared Technique beats a declared Specialty,
    which beats an auto Technique, then lowest Technique id. The applied id
    for a Specialty step is the literal string `"specialty"`.

    Only Techniques in `character.techniques` (i.e. actually unlocked) are
    eligible — an un-unlocked Technique's `difficulty_step` never fires,
    even if its trigger would otherwise match.

    Args:
        declared_label: The MM's already-resolved situational difficulty.
        character: Anything exposing `.techniques` (list[str], unlocked
            Technique ids) and `.technique_choices` (dict[str, str]).
        context: Roll facts the trigger evaluates against — `skill_id`,
            `weapon_category`, `weapon_type`, `hazard_type`,
            `knowledge_field`, and `declared_technique_ids` (the player's
            toggles for declared-kind Techniques). A field this dict omits
            simply means no auto trigger keyed on it can fire — it is not
            an error. `weapon_category` and `weapon_type` are orthogonal
            (DESIGN §8): the former is the mechanical IV.1 taxonomy that
            sets a Strike's attribute, the latter the fictional taxonomy
            *Weapon Mastery* masters (blades/blunt/polearms/unarmed) — this
            function does not know or care which trigger reads which key,
            it only compares `context[trigger.match]`.
        ruleset: A `MergedRuleset` (or anything exposing `get_technique()`
            and the attributes `_step_difficulty_easier`/`_harder` read).

    Returns:
        `(final_label, applied_technique_id)` — `applied_technique_id` is
        `None` when no Technique fired, so the roll banner and transcript
        can distinguish an unmodified roll from a stepped one (DESIGN §2.7).
    """
    # Client-supplied; a non-iterable here used to raise straight through the
    # dispatch loop and disconnect the sender.
    raw_declared = context.get("declared_technique_ids") or []
    if isinstance(raw_declared, (str, bytes)) or not isinstance(raw_declared, (list, tuple, set)):
        raw_declared = []
    declared_ids = {str(x) for x in raw_declared}
    # (precedence_rank, source_id): rank 0 = player-declared Technique,
    # rank 1 = declared Specialty, rank 2 = auto Technique. Sorting by this
    # tuple gives "declared beats Specialty beats auto, then lowest id".
    candidates: list[tuple[int, str]] = []

    # Specialty shares the one character-side step pool (T2.4/D2). It is
    # always player-declared — the MM confirms it applies in the fiction —
    # and always eases (II.6: a directly applicable Specialty turns a
    # Standard roll Easy; composed here as one step easier).
    if context.get("specialty_declared") and getattr(character, "specialty", None):
        candidates.append((1, "specialty"))

    for tech_id in character.techniques:
        tech_def = ruleset.get_technique(tech_id)
        if tech_def is None or tech_def.difficulty_step is None or tech_def.step_trigger is None:
            continue

        trigger = tech_def.step_trigger
        if trigger.kind == "declared":
            if tech_id not in declared_ids:
                continue
            candidates.append((0, tech_id))
        elif trigger.kind == "auto":
            # A Technique the book scopes to one skill only fires on that skill.
            # Without this, Acclimated ("Endurance rolls against your chosen
            # hardship") and Field of Mastery ("Lore rolls within your chosen
            # field") stepped any roll that carried the matching context string —
            # the engine implementing a wider rule than the printed one.
            if trigger.requires_skill and context.get("skill_id") != trigger.requires_skill:
                continue
            match_field = trigger.match
            if not match_field or match_field not in context:
                continue
            context_value = context[match_field]
            if context_value is None:
                continue
            if trigger.against == "choice":
                expected = character.technique_choices.get(tech_id)
            else:
                expected = trigger.against
            if expected is None or context_value != expected:
                continue
            candidates.append((2, tech_id))

    if not candidates:
        return declared_label, None

    candidates.sort()
    _, applied_id = candidates[0]

    if applied_id == "specialty":
        step = "easier"
    else:
        step = ruleset.get_technique(applied_id).difficulty_step

    if step == "easier":
        final_label = _engine._step_difficulty_easier(declared_label, ruleset)
    else:
        final_label = _engine._step_difficulty_harder(declared_label, ruleset)

    return final_label, applied_id


def compose_difficulty(
    base_label: str,
    character=None,
    context: Optional[dict] = None,
    ruleset=None,
    *,
    easy_tag: bool = False,
    support_ease: bool = False,
) -> tuple[str, Optional[str]]:
    """The full printed precedence for a roll's difficulty (III.1
    §Difficulty; T2.4/D2), composed in its fixed order:

    1. **Base** from the situation — `base_label`, the MM's call.
    2. **Easy-tag override** — an Open enemy (K-6/D4) or a Maneuver
       (`easy_tag=True`) overrides the base downward to Easy. Tags are
       absolute, so they cannot stack with themselves: two tags are still
       one Easy.
    3. **One character-side step** — at most one, from all character
       abilities combined (Technique, Specialty, anything future), via
       `apply_character_difficulty_step`'s shared pool.
    4. **Support's step** — `support_ease=True` when the ally's pending
       Support bonus is the ease-difficulty mode (party-side, so it lands
       on top of the single character step).
    5. **Clamp** — Easy is the floor, Very Hard the ceiling; the ladder
       primitives (`engine._step_difficulty_easier`/`_harder`) saturate
       at both ends.

    This is the rule's only home. `target_strike_difficulty` composes through
    here for the Easy tag; the WS handlers and the simulator reach the same
    ladder through `apply_character_difficulty_step`, which step 3 calls.
    Nobody steps a difficulty inline.

    Returns `(final_label, applied_source_id)` — the source id is a
    Technique id, the literal `"specialty"`, or None (see
    `apply_character_difficulty_step`).
    """
    label = base_label
    if easy_tag:
        label = "Easy"

    applied_id: Optional[str] = None
    if character is not None:
        label, applied_id = apply_character_difficulty_step(
            label, character, context or {}, ruleset,
        )

    if support_ease:
        label = _engine._step_difficulty_easier(label, ruleset)

    return label, applied_id


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
