"""Combat simulator for Facets of Origin encounter balancing.

Simulates combat encounters using the game's dice mechanics to generate
statistically significant win rate data for encounter budget calibration.

Usage:
    cd software
    python -m tools.combat_sim --series A     # Run Series A (Mook scaling)
    python -m tools.combat_sim --all          # Run all series
    python -m tools.combat_sim --custom ...   # Custom encounter
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import random
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.facets.registry import MergedRuleset, build_ruleset
from app.game import combat as combat_module

_RULESET_CACHE: Optional[MergedRuleset] = None


def _ruleset() -> MergedRuleset:
    """The merged base ruleset, built once and cached.

    `run_combat` reads every combat constant (armor, condition tiers,
    reaction costs, posture modifiers, Withdrawn recovery) through
    `app.game.combat`, which requires a ruleset — this is the single load
    point for the simulator. See DESIGN §2.1 / TASKS WS-A0.
    """
    global _RULESET_CACHE
    if _RULESET_CACHE is None:
        _RULESET_CACHE = build_ruleset([])
    return _RULESET_CACHE


def spark_refund_variant_enabled(ruleset: Optional[MergedRuleset] = None) -> bool:
    """Read the D6 `refund_on_failed_pretechnique_cast` variant flag (WD7).

    Test, do not adopt (BRIEF D6) — combat magic is not yet simulated
    (see PT03/PT04 findings), so this flag has no observable effect on
    `run_combat`. It exists so the sim and PT04 harness can read and
    report the flag's state; toggling it is a no-op until magic casting
    is modelled in the simulator.
    """
    rs = ruleset or _ruleset()
    return bool(rs.spark and rs.spark.variants.refund_on_failed_pretechnique_cast)


# ---------------------------------------------------------------------------
# Constants
#
# TIER1_CONDITIONS/TIER2_CONDITIONS/POSTURE_OFFENSE/POSTURE_REACTION_COST/
# DIFFICULTY_MOD/combat_roll below are no longer used by the resolution
# functions (`_pc_strike`, `_enemy_attack` call `app.game.combat` instead,
# which reads the equivalent values from `facet.yaml`). They are left in
# place because deleting them was not in WS-A0's scope and existing tests
# (`TestCombatRoll`, `test_staggered_attacker_penalty`) still exercise them
# directly as a plain dice utility. Flagged here as a residual duplication
# for a future pass, not silently carried forward.
# ---------------------------------------------------------------------------

TIER1_CONDITIONS = ("winded", "off_balance", "shaken")
TIER2_CONDITIONS = ("staggered", "cornered")
MAX_EXCHANGES = 20  # Safety cap

# Posture offense modifiers
POSTURE_OFFENSE = {
    "aggressive": 1,
    "measured": 0,
    "defensive": -1,
    "withdrawn": None,  # Cannot attack
}

# Posture reaction cost modifiers
POSTURE_REACTION_COST = {
    "aggressive": 1,
    "measured": 0,
    "defensive": -1,
    "withdrawn": -99,  # Free reactions (effectively -inf)
}

DIFFICULTY_MOD = {"Easy": 1, "Standard": 0, "Hard": -1, "Very Hard": -2}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SimResult:
    """Result of a single combat simulation run."""
    party_wins: bool
    exchanges: int
    sparks_spent: int
    pcs_broken: list[str]
    endurance_remaining: dict[str, int]
    enemies_remaining: int


@dataclass
class AggregateResult:
    """Aggregated statistics from multiple simulation runs."""
    label: str
    iterations: int
    wins: int
    losses: int
    draws: int
    win_rate: float
    win_rate_ci_low: float
    win_rate_ci_high: float
    mean_exchanges: float
    median_exchanges: float
    mean_sparks_spent: float
    mean_pcs_broken: float
    endurance_stats: dict[str, dict]


@dataclass
class PCState:
    """A PC's combat state for one simulation run."""
    name: str
    endurance_max: int
    endurance_current: int
    armor: str  # "none" | "light" | "heavy"
    sparks: int
    sparks_spent: int = 0
    # D2 per-scene armor downgrade budget. Set fresh at the top of
    # `run_combat` via `combat.armor_budget` — one `run_combat` call is one
    # scene's worth of combat for the simulator's purposes.
    armor_downgrades_remaining: int = 0
    # Offensive: Strike uses strength + combat
    strength_mod: int = 0
    combat_mod: int = 0
    # Defensive: Dodge uses dexterity, Parry uses strength + combat
    dexterity_mod: int = 0
    # State
    conditions: list[str] = field(default_factory=list)
    posture: str = "measured"
    is_broken: bool = False
    # K1 (BRIEF D8): count of reactions taken so far this exchange, reset
    # each exchange in `run_combat`. Feeds `combat.reaction_cost`'s
    # `is_first_reaction` in `_enemy_attack`.
    reactions_this_exchange: int = 0


@dataclass
class EnemyState:
    """An enemy's combat state for one simulation run.

    `resolve`/`resolve_current` (D1, DESIGN §4.1): a Mook has 0 and no
    pool; a Named/Boss's `resolve` is its base pool, and `resolve_current`
    starts at `resolve` plus its armor bonus (set by `make_enemy`, mirroring
    `Enemy.init_combat`). There is no enemy-side Broken — Resolve reaching 0
    is defeat, tracked via `is_removed` like a Mook.

    `phases` holds this enemy's authored `resolve_threshold`/`description`
    pairs straight from its `.fof` (purely narrative per the engine's
    `PhaseDef`). `special_attack_mod`/`special_ignores_tier1` are NOT a
    generic engine mechanic — they model an individual boss's authored
    "Special" stat-block text (e.g. Archive Guardian's Reduced Mode) so the
    simulator's numbers reflect that specific published enemy; a Named NPC
    or a boss without such text leaves them at their defaults and phase
    changes stay purely informational (`phase_index`).
    """
    name: str
    instance_id: str
    tier: str  # "mook" | "named" | "boss"
    resolve: int
    resolve_current: int
    attack_modifier: int
    defense_modifier: int
    armor: str
    posture: str = "measured"
    conditions: list[str] = field(default_factory=list)
    is_removed: bool = False
    phases: list[dict] = field(default_factory=list)
    phase_index: Optional[int] = None
    special_attack_mod: Optional[int] = None
    special_ignores_tier1: bool = False

    @property
    def is_out(self) -> bool:
        return self.is_removed


# ---------------------------------------------------------------------------
# Dice rolling
# ---------------------------------------------------------------------------

def combat_roll(
    modifier: int,
    difficulty: str = "Standard",
    extra_dice: int = 0,
) -> tuple[str, list[int], int]:
    """Roll 2d6 + modifier + difficulty_mod, with optional extra dice (drop lowest).

    Returns: (outcome, dice_kept, total)
    """
    diff_mod = DIFFICULTY_MOD.get(difficulty, 0)
    base_dice = 2
    total_dice = base_dice + extra_dice
    dice = sorted(random.randint(1, 6) for _ in range(total_dice))
    kept = dice[extra_dice:]  # Drop the lowest extra_dice

    total = sum(kept) + modifier + diff_mod
    if total >= 10:
        return "full_success", kept, total
    elif total >= 7:
        return "partial_success", kept, total
    else:
        return "failure", kept, total


# ---------------------------------------------------------------------------
# Condition management
#
# apply_condition/_apply_broken/cleanup_end_of_exchange/armor_downgrade were
# deleted here per TASKS WS-A0 (A0.3) — their rule logic now lives in
# `app.game.combat` (`apply_condition`, `armor_downgrade`, `end_exchange`),
# shared with `app/api/websocket.py`. `_mark_broken` below is NOT a moved
# rule: it is simulator-only bookkeeping (PCState.is_broken/EnemyState.
# is_removed plus the Boss phase-change reset) that reacts to the `broken`
# flag `combat.apply_condition` returns. Character/Enemy don't have this
# shape (Character represents Broken as a literal condition string), so it
# stays here rather than in combat.py — see combat.py's `Combatant` docstring.
# ---------------------------------------------------------------------------

def _mark_broken(target: PCState) -> None:
    """Mark a PC Broken (Condition tier 3, D5 ledger row 2).

    PC-only since D1 (A4): enemies no longer have a Condition-based Broken
    track — an enemy's defeat comes from Resolve reaching 0, handled
    directly in `_pc_strike` via `combat_module.apply_resolve_damage`,
    which sets `is_removed` the same way a Mook removal does.
    """
    target.is_broken = True


# ---------------------------------------------------------------------------
# AI: Posture selection
# ---------------------------------------------------------------------------

def choose_pc_posture(pc: PCState, allies_active: int) -> str:
    """Choose posture for a PC based on Endurance level."""
    if pc.endurance_current == 0:
        # At 0 End: Withdraw to recover if allies can cover
        if allies_active > 1:
            return "withdrawn"
        return "measured"  # Last PC standing, must attack

    ratio = pc.endurance_current / pc.endurance_max if pc.endurance_max > 0 else 0

    if ratio > 0.66:
        return "aggressive"
    elif ratio > 0.33:
        return "measured"
    else:
        return "defensive"


def choose_enemy_posture(enemy: EnemyState) -> str:
    """Choose posture for an enemy. Named/Boss use Measured by default."""
    if enemy.tier == "mook":
        return "measured"
    # Named/Boss: Measured by default
    # Defensive if has T2 conditions and low Resolve
    if enemy.resolve_current == 0 and enemy.tier != "mook":
        return "defensive"
    return "measured"


# ---------------------------------------------------------------------------
# AI: Target selection
# ---------------------------------------------------------------------------

def choose_pc_target(pc: PCState, enemies: list[EnemyState]) -> Optional[EnemyState]:
    """PC target selection: focus fire on weakest enemy."""
    active = [e for e in enemies if not e.is_out]
    if not active:
        return None

    # Priority: Mooks first (remove action economy), then wounded Named/Boss
    mooks = [e for e in active if e.tier == "mook"]
    if mooks:
        return mooks[0]

    # Named/Boss: prioritize those with T2 conditions (close to Broken)
    with_t2 = [e for e in active if any(c in TIER2_CONDITIONS for c in e.conditions)]
    if with_t2:
        return with_t2[0]

    # Default: first active enemy
    return active[0]


def choose_enemy_target(enemy: EnemyState, pcs: list[PCState]) -> Optional[PCState]:
    """Enemy target selection: attack PC with lowest Endurance."""
    active = [p for p in pcs if not p.is_broken]
    if not active:
        return None

    # Target lowest endurance (most vulnerable)
    return min(active, key=lambda p: p.endurance_current)


# ---------------------------------------------------------------------------
# AI: Reaction and resource decisions
# ---------------------------------------------------------------------------

def should_spend_spark(pc: PCState, target: EnemyState, policy: str = "conservative") -> int:
    """Decide how many Sparks to spend on this Strike.

    `policy` (WD10, BRIEF D6): selectable, default-preserving. `should_spend_spark`
    is exercised by every recorded Gate/Series corpus, so its old behaviour
    cannot be edited in place without silently re-baselining every recorded
    number (the exact failure A14 already recorded once) — see
    `docs/TASKS_v0.3_ruleset_revision.md` WD10.

    - `"conservative"` (default): today's exact behaviour, unchanged bit for
      bit. Spend only against a Boss, in desperation (Endurance <= 2), or to
      finish a Tier-2-conditioned target.
    - `"player_like"`: a less hoarding-prone spender (BRIEF D6's premise).
      Superset of `"conservative"` — spends on any Named-or-Boss target (a
      "climax," not just a Boss), in the same desperation/finishing-blow
      cases, and additionally when holding 2+ Sparks (a "floor" of 1 kept in
      reserve rather than hoarding the whole allotment).
    """
    if pc.sparks <= 0:
        return 0

    if policy == "player_like":
        if target.tier in ("named", "boss"):
            return 1
        if pc.endurance_current <= 2:
            return 1
        if any(c in TIER2_CONDITIONS for c in target.conditions):
            return 1
        if pc.sparks >= 2:
            return 1
        return 0

    # "conservative" — today's exact behaviour, the default.
    # Spend against Bosses
    if target.tier == "boss":
        return 1
    # Desperation: low Endurance
    if pc.endurance_current <= 2:
        return 1
    # Finishing blow: target has T2 condition (close to Broken)
    if any(c in TIER2_CONDITIONS for c in target.conditions):
        return 1
    return 0


def should_press(pc: PCState, target: EnemyState) -> bool:
    """Decide whether to Press (spend 1 End for +1d6)."""
    if pc.endurance_current <= 1:
        return False
    if pc.posture == "aggressive" and pc.endurance_current <= 2:
        return False  # Need End for reactions
    # Press against Named/Boss when we have End to spare
    if target.tier in ("named", "boss") and pc.endurance_current >= 3:
        return True
    return False


def choose_pc_reaction(pc: PCState, incoming_tier: int, enemy_posture: str) -> str:
    """Choose reaction type for a PC. Returns 'dodge', 'parry', or 'absorb'."""
    # Calculate reaction cost
    base_cost = 1
    posture_adj = POSTURE_REACTION_COST.get(pc.posture, 0)
    cost = max(0, base_cost + posture_adj)

    if pc.endurance_current < cost:
        return "absorb"

    # Don't waste Endurance on Mook T1 if we have armor
    if incoming_tier == 1 and pc.armor in ("light", "heavy"):
        return "absorb"  # Armor will handle T1

    # Choose Dodge or Parry based on which gives better odds
    parry_mod = pc.strength_mod + pc.combat_mod
    dodge_mod = pc.dexterity_mod
    if parry_mod >= dodge_mod:
        return "parry"
    return "dodge"


# ---------------------------------------------------------------------------
# Resolution: PC Strike against Enemy
# ---------------------------------------------------------------------------
#
# Enemies do not react (A14/§5-quater F5/F8). Settled asymmetric-combat
# doctrine ("NPCs don't roll; PCs react") plus Q4's "Resolve is durability,
# not an action-economy pool": a Strike against a Named/Boss depletes Resolve
# by its effective outcome, full stop. There is no enemy Parry, and no Resolve
# is ever spent on defense. Enemy durability is Resolve + phases, never
# out-defending the party.

def _choose_condition(target_conditions: list[str], ruleset) -> str:
    """Which Condition to apply on a Tier 2 hit against a PC: prefer the
    ruleset's first Tier 2 id if the target already has it (to trigger
    Broken), else its second Tier 2 id if that's already present, else
    default to the first. This is AI policy (the PHB leaves the choice to
    the attacker), not a rule — it stays here, not in `app.game.combat`.
    PC-only since D1 (A4) — see `_choose_rider` for the enemy-side
    equivalent, which never escalates to Broken.
    """
    tier2_ids = [c.id for c in ruleset.combat.conditions.tier2]
    for candidate in tier2_ids:
        if candidate in target_conditions:
            return candidate
    return tier2_ids[0]


def _choose_rider(target: EnemyState, ruleset) -> Optional[str]:
    """AI policy for the Tier 1/2 Condition a full-success Strike may
    impose on an enemy as a rider (D1, DESIGN §4.1). Always prefers a
    Tier 2 id the target doesn't already carry — deliberately the most
    aggressive policy available, so G1 (DESIGN §5) measures the worst-case
    rider→Easy snowball rather than an averaged one. Falls back to a Tier 1
    rider only once both Tier 2 ids are already present, at which point a
    boss whose authored Special text grants Tier 1 immunity post-phase
    (Archive Guardian's Reduced Mode) gets no rider at all — riders must
    keep their normal table effect (Brain, EF1), and a Tier 1 rider with no
    effect is not that.
    """
    tier2_ids = [c.id for c in ruleset.combat.conditions.tier2]
    for candidate in tier2_ids:
        if candidate not in target.conditions:
            return candidate
    if target.special_ignores_tier1 and target.phase_index is not None:
        return None
    return "winded"


def _pc_strike(
    pc: PCState,
    target: EnemyState,
    ruleset,
    verbose: bool = False,
    spark_policy: str = "conservative",
) -> None:
    """Resolve a PC's Strike against an enemy target.

    Mook: any success removes it (an armored Mook needs a full success).
    Named/Boss: enemies have no reaction (A14 F5) — Resolve depletes by the
    Strike's outcome (D1) and a full success may additionally impose a
    Tier 1/2 Condition as a rider. Riders never escalate to Broken, since
    Resolve is what defeats an enemy now.

    `spark_policy` (WD10) is forwarded to `should_spend_spark` unchanged;
    default `"conservative"` reproduces every recorded corpus bit-identical.
    """
    if pc.posture == "withdrawn":
        return  # Cannot attack

    # Determine extra dice (Sparks + Press)
    sparks = should_spend_spark(pc, target, spark_policy)
    press = should_press(pc, target)

    if sparks > 0 and pc.sparks >= sparks:
        pc.sparks -= sparks
        pc.sparks_spent += sparks
    else:
        sparks = 0

    if press:
        pc.endurance_current -= 1

    extra_dice = sparks + (1 if press else 0)
    modifier = pc.strength_mod + pc.combat_mod

    # A Tier 2 rider from a prior Strike makes this one Easy (D1).
    difficulty = combat_module.target_strike_difficulty("Standard", target.conditions, ruleset)

    strike = combat_module.resolve_strike(
        modifier, pc.posture, pc.conditions, ruleset,
        combat_module.StrikeOptions(difficulty=difficulty, extra_dice=extra_dice),
    )

    if verbose:
        print(f"  {pc.name} strikes {target.instance_id}: "
              f"dice={strike.dice} mod={modifier} diff={difficulty} total={strike.total} → {strike.outcome}")

    if strike.outcome == "failure":
        # 6-: consequence for attacker (T1 condition)
        combat_module.apply_condition(pc.conditions, "winded", 1, ruleset)
        return

    # Mook: any success removes them (armored Mook needs a full success)
    if target.tier == "mook":
        armored = target.armor in ("light", "heavy")
        if combat_module.mook_removed(strike.outcome, armored, ruleset):
            target.is_removed = True
            if verbose:
                print(f"    → {target.instance_id} removed (Mook)")
        return

    # Named/Boss: no enemy reaction (A14 F5). Resolve depletes by the
    # Strike's own outcome.
    effective_outcome = strike.outcome
    phase_thresholds = [p["resolve_threshold"] for p in target.phases]
    damage = combat_module.apply_resolve_damage(
        target.resolve_current, effective_outcome, ruleset, phase_thresholds,
    )
    target.resolve_current = damage.resolve_current

    if verbose:
        print(f"    → {target.instance_id} Resolve {damage.resolve_current} (-{damage.depletion})")

    if damage.phase_index is not None:
        target.phase_index = damage.phase_index
        if target.special_attack_mod is not None:
            target.attack_modifier = target.special_attack_mod
        if verbose:
            print(f"    → {target.instance_id} enters phase {damage.phase_index}")

    if damage.defeated:
        target.is_removed = True
        if verbose:
            print(f"    → {target.instance_id} defeated")
        return

    # A full success may additionally impose a rider Condition
    # (D1: "on a full success only").
    if effective_outcome == "full_success":
        condition = _choose_rider(target, ruleset)
        if condition is not None:
            tier2_ids = {c.id for c in ruleset.combat.conditions.tier2}
            tier = 2 if condition in tier2_ids else 1
            combat_module.apply_condition(
                target.conditions, condition, tier, ruleset, is_rider=True,
            )
            if verbose:
                print(f"    → {target.instance_id} takes {condition} (rider, T{tier})")


# ---------------------------------------------------------------------------
# Resolution: Enemy Attack against PC
# ---------------------------------------------------------------------------

def _enemy_attack(enemy: EnemyState, target: PCState, ruleset, verbose: bool = False) -> None:
    """Resolve an enemy's attack against a PC.

    NPCs don't roll. The incoming condition tier is determined by enemy type.
    The PC reacts (Dodge, Parry, or Absorb) via `app.game.combat`'s rules;
    reaction choice is AI policy (`choose_pc_reaction`), made here.
    """
    if target.is_broken:
        return

    # K1 (BRIEF D8): this attack is the target's first reaction of the
    # exchange only if none has landed yet this exchange.
    is_first_reaction = target.reactions_this_exchange == 0
    target.reactions_this_exchange += 1

    # Incoming tier by enemy type
    incoming_tier = 1 if enemy.tier == "mook" else 2

    # Reaction difficulty adjusted by enemy posture
    difficulty = "Standard"
    if enemy.posture == "aggressive":
        difficulty = "Hard"
    elif enemy.posture == "defensive":
        difficulty = "Easy"

    # PC chooses reaction
    reaction = choose_pc_reaction(target, incoming_tier, enemy.posture)

    if verbose:
        print(f"  {enemy.instance_id} attacks {target.name} (T{incoming_tier}): "
              f"{target.name} {reaction}s")

    if reaction == "absorb":
        # Take full hit — Absorb never downgrades, so armor alone reduces here.
        incoming = combat_module.resolve_incoming_condition(
            incoming_tier, target.armor, target.armor_downgrades_remaining, ruleset,
        )
        target.armor_downgrades_remaining = incoming.downgrades_remaining
        final_tier = incoming.tier

        if final_tier <= 0:
            if verbose:
                print(f"    → negated by armor")
            return

        condition = _choose_condition(target.conditions, ruleset) if final_tier >= 2 else "winded"

        result = combat_module.apply_condition(
            target.conditions, condition, final_tier, ruleset,
        )
        if result.broken:
            _mark_broken(target)
        if verbose:
            broken_str = " → BROKEN!" if target.is_broken else ""
            print(f"    → {target.name} takes {condition} (T{final_tier}){broken_str}")
        return

    # Active reaction: Dodge or Parry — pay Endurance cost, then roll
    cost = combat_module.reaction_cost(reaction, target.posture, ruleset, is_first_reaction)
    target.endurance_current = max(0, target.endurance_current - cost)

    mod = target.dexterity_mod if reaction == "dodge" else (target.strength_mod + target.combat_mod)
    result = combat_module.roll(mod, difficulty, ruleset)

    if verbose:
        print(f"    {target.name} rolls {reaction}: dice={result.dice} total={result.total} → {result.outcome}")

    if result.outcome == "full_success":
        # Fully avoided
        if verbose:
            print(f"    → avoided entirely")
        return

    # Armor and a partial reaction do not stack (PHB III.3) — the shared rule
    # applies the single greater reduction, and does not spend an armor charge
    # the reaction has already made redundant.
    incoming = combat_module.resolve_incoming_condition(
        incoming_tier,
        target.armor,
        target.armor_downgrades_remaining,
        ruleset,
        reaction_downgraded=(result.outcome == "partial_success"),
    )
    target.armor_downgrades_remaining = incoming.downgrades_remaining
    final_tier = incoming.tier

    if final_tier <= 0:
        if verbose:
            print(f"    → condition negated")
        return

    condition = _choose_condition(target.conditions, ruleset) if final_tier >= 2 else "winded"

    applied = combat_module.apply_condition(target.conditions, condition, final_tier, ruleset)
    if applied.broken:
        _mark_broken(target)
    if verbose:
        broken_str = " → BROKEN!" if target.is_broken else ""
        print(f"    → {target.name} takes {condition} (T{final_tier}){broken_str}")


# ---------------------------------------------------------------------------
# Combat loop
# ---------------------------------------------------------------------------

def run_combat(
    pcs: list[PCState],
    enemies: list[EnemyState],
    verbose: bool = False,
    spark_policy: str = "conservative",
) -> SimResult:
    """Run a single combat encounter to completion.

    Returns a SimResult with win/loss, exchanges, Sparks spent, etc.

    `spark_policy` (WD10) is forwarded to every PC Strike's
    `should_spend_spark` call; default `"conservative"` reproduces every
    recorded corpus bit-identical.
    """
    ruleset = _ruleset()
    for pc in pcs:
        pc.armor_downgrades_remaining = combat_module.armor_budget(pc.armor, ruleset)

    for exchange in range(1, MAX_EXCHANGES + 1):
        active_pcs = [p for p in pcs if not p.is_broken]
        active_enemies = [e for e in enemies if not e.is_out]

        if not active_enemies:
            return _build_result(True, exchange - 1, pcs, enemies)
        if not active_pcs:
            return _build_result(False, exchange - 1, pcs, enemies)

        # K1 (BRIEF D8): reset the per-exchange reaction count.
        for pc in active_pcs:
            pc.reactions_this_exchange = 0

        if verbose:
            print(f"\n--- Exchange {exchange} ---")
            for p in active_pcs:
                print(f"  {p.name}: End={p.endurance_current}/{p.endurance_max} "
                      f"Sparks={p.sparks} Cond={p.conditions}")
            for e in active_enemies:
                end_str = f"Resolve={e.resolve_current}/{e.resolve}" if e.tier != "mook" else "Mook"
                print(f"  {e.instance_id}: {end_str} Cond={e.conditions}")

        # 1. Declare postures
        for pc in active_pcs:
            pc.posture = choose_pc_posture(pc, len(active_pcs))
        for enemy in active_enemies:
            enemy.posture = choose_enemy_posture(enemy)

        if verbose:
            postures = {p.name: p.posture for p in active_pcs}
            e_postures = {e.instance_id: e.posture for e in active_enemies}
            print(f"  Postures — PCs: {postures}, Enemies: {e_postures}")

        # 2. PC actions
        for pc in active_pcs:
            if pc.posture == "withdrawn":
                if verbose:
                    print(f"  {pc.name} withdraws (recovering)")
                continue
            target = choose_pc_target(pc, enemies)
            if target is None:
                continue
            _pc_strike(pc, target, ruleset, verbose, spark_policy)
            # Refresh active enemies (a Mook may have been removed)
            active_enemies = [e for e in enemies if not e.is_out]

        # Check if all enemies defeated after PC actions
        active_enemies = [e for e in enemies if not e.is_out]
        if not active_enemies:
            return _build_result(True, exchange, pcs, enemies)

        # 3. Enemy actions
        for enemy in active_enemies:
            active_pcs_now = [p for p in pcs if not p.is_broken]
            if not active_pcs_now:
                break
            target = choose_enemy_target(enemy, active_pcs_now)
            if target is None:
                continue
            _enemy_attack(enemy, target, ruleset, verbose)

        # Check if all PCs broken after enemy actions
        active_pcs = [p for p in pcs if not p.is_broken]
        if not active_pcs:
            return _build_result(False, exchange, pcs, enemies)

        # 4. End-of-exchange cleanup
        for pc in pcs:
            if pc.is_broken:
                continue
            combat_module.end_exchange(pc.conditions, ruleset)
            if pc.posture == "withdrawn":
                pc.endurance_current = min(
                    pc.endurance_max,
                    pc.endurance_current + combat_module.withdrawn_recovery_amount(ruleset),
                )
        for enemy in enemies:
            if not enemy.is_out:
                combat_module.end_exchange(enemy.conditions, ruleset)
                if enemy.posture == "withdrawn":
                    resolve_max = enemy.resolve + combat_module.enemy_armor_resolve_bonus(
                        enemy.armor, ruleset,
                    )
                    enemy.resolve_current = min(
                        resolve_max,
                        enemy.resolve_current + combat_module.withdrawn_recovery_amount(ruleset),
                    )

    # Timeout: draw (counted as loss)
    return _build_result(False, MAX_EXCHANGES, pcs, enemies)


def _build_result(
    party_wins: bool,
    exchanges: int,
    pcs: list[PCState],
    enemies: list[EnemyState],
) -> SimResult:
    return SimResult(
        party_wins=party_wins,
        exchanges=exchanges,
        sparks_spent=sum(p.sparks_spent for p in pcs),
        pcs_broken=[p.name for p in pcs if p.is_broken],
        endurance_remaining={p.name: p.endurance_current for p in pcs},
        enemies_remaining=sum(1 for e in enemies if not e.is_out),
    )


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

def run_simulation(
    pc_defs: list[dict],
    enemy_defs: list[tuple[dict, int]],
    iterations: int = 200,
    label: str = "",
    verbose: bool = False,
    seed: Optional[int] = None,
    spark_policy: str = "conservative",
) -> AggregateResult:
    """Run N iterations of a combat encounter and aggregate results.

    Args:
        pc_defs: List of PC definition dicts (see make_pc()).
        enemy_defs: List of (enemy_def_dict, count) tuples.
        iterations: Number of simulation runs.
        label: Label for this simulation series.
        verbose: Print per-exchange details.
        seed: Random seed for reproducibility.
        spark_policy: (WD10) `"conservative"` (default, today's exact
            behaviour) or `"player_like"` — see `should_spend_spark`.

    Returns:
        AggregateResult with statistics.
    """
    if seed is not None:
        random.seed(seed)

    results: list[SimResult] = []

    for i in range(iterations):
        # Deep-copy combatants for each run
        pcs = [make_pc(d) for d in pc_defs]
        enemies = []
        for edef, count in enemy_defs:
            for j in range(count):
                e = make_enemy(edef, j + 1 if count > 1 else 0)
                enemies.append(e)

        result = run_combat(pcs, enemies, verbose=(verbose and i == 0), spark_policy=spark_policy)
        results.append(result)

    return _aggregate(results, label, iterations)


def _aggregate(results: list[SimResult], label: str, iterations: int) -> AggregateResult:
    """Compute aggregate statistics from simulation results."""
    wins = sum(1 for r in results if r.party_wins)
    losses = sum(1 for r in results if not r.party_wins)
    draws = 0  # Not tracked separately

    win_rate = wins / iterations if iterations > 0 else 0

    # Wilson score confidence interval (95%)
    z = 1.96
    ci_low, ci_high = _wilson_ci(wins, iterations, z)

    exchanges = [r.exchanges for r in results]
    sparks = [r.sparks_spent for r in results]
    broken_counts = [len(r.pcs_broken) for r in results]

    # Per-PC endurance stats
    pc_names = set()
    for r in results:
        pc_names.update(r.endurance_remaining.keys())

    endurance_stats = {}
    for name in sorted(pc_names):
        values = [r.endurance_remaining.get(name, 0) for r in results]
        endurance_stats[name] = {
            "mean": round(statistics.mean(values), 1),
            "min": min(values),
            "max": max(values),
        }

    return AggregateResult(
        label=label,
        iterations=iterations,
        wins=wins,
        losses=losses,
        draws=draws,
        win_rate=round(win_rate, 4),
        win_rate_ci_low=round(ci_low, 4),
        win_rate_ci_high=round(ci_high, 4),
        mean_exchanges=round(statistics.mean(exchanges), 1),
        median_exchanges=round(statistics.median(exchanges), 1),
        mean_sparks_spent=round(statistics.mean(sparks), 1),
        mean_pcs_broken=round(statistics.mean(broken_counts), 2),
        endurance_stats=endurance_stats,
    )


def _wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return 0.0, 0.0
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, centre - margin), min(1.0, centre + margin)


# ---------------------------------------------------------------------------
# Canonical definitions — Characters
# ---------------------------------------------------------------------------

def make_pc(d: dict) -> PCState:
    """Create a PCState from a definition dict."""
    return PCState(**d)


def mordai_def() -> dict:
    """Mordai: Body, Str 3, Combat Practiced, End 5."""
    return dict(
        name="Mordai",
        endurance_max=5,  # 4 + Con(3→+1) + Endurance(novice→+0)
        endurance_current=5,
        armor="none",
        sparks=3,
        strength_mod=1,   # Str 3 → +1
        combat_mod=1,     # Combat Practiced → +1
        dexterity_mod=0,  # Dex 2 → 0
    )


def zahna_def() -> dict:
    """Zahna: Mind, Str 1, no Combat, End 3."""
    return dict(
        name="Zahna",
        endurance_max=3,  # 4 + Con(1→-1) + Endurance(novice→+0) = 3
        endurance_current=3,
        armor="none",
        sparks=3,
        strength_mod=-1,  # Str 1 → -1
        combat_mod=0,     # No Combat skill
        dexterity_mod=1,  # Dex 3 → +1
    )


def zulnut_def() -> dict:
    """Zulnut: Body, Str 2, no Combat, End 3."""
    return dict(
        name="Zulnut",
        endurance_max=3,  # 4 + Con(1→-1) + Endurance(novice→+0)
        endurance_current=3,
        armor="none",
        sparks=3,
        strength_mod=0,   # Str 2 → 0
        combat_mod=0,     # No Combat skill
        dexterity_mod=1,  # Dex 3 → +1
    )


def standard_party() -> list[dict]:
    """The standard 3-PC party: Mordai, Zahna, Zulnut."""
    return [mordai_def(), zahna_def(), zulnut_def()]


def drew_def() -> dict:
    """Drew: Body, Str 3, Combat Practiced, End 5 (4th player from PT02)."""
    return dict(
        name="Drew",
        endurance_max=5,
        endurance_current=5,
        armor="none",
        sparks=3,
        strength_mod=1,
        combat_mod=1,
        dexterity_mod=0,
    )


def four_player_party() -> list[dict]:
    """4-PC party: standard + Drew."""
    return standard_party() + [drew_def()]


# Advanced party (PS 6-8): characters with Practiced skills + Techniques
def advanced_mordai_def() -> dict:
    """Mordai at career_advances 2: Combat Expert."""
    return dict(
        name="Mordai",
        endurance_max=6,  # 4 + Con(+1) + Endurance Practiced(+1)
        endurance_current=6,
        armor="none",
        sparks=3,
        strength_mod=1,
        combat_mod=2,     # Combat Expert → +2
        dexterity_mod=0,
    )


def advanced_zahna_def() -> dict:
    """Zahna at career_advances 2: Lore Expert, magic active."""
    return dict(
        name="Zahna",
        endurance_max=3,
        endurance_current=3,
        armor="none",
        sparks=3,
        strength_mod=-1,
        combat_mod=0,
        dexterity_mod=1,
    )


def advanced_zulnut_def() -> dict:
    """Zulnut at career_advances 2: Finesse Expert."""
    return dict(
        name="Zulnut",
        endurance_max=3,
        endurance_current=3,
        armor="none",
        sparks=3,
        strength_mod=0,
        combat_mod=0,
        dexterity_mod=1,
    )


def advanced_party() -> list[dict]:
    """Advanced 3-PC party at PS 6."""
    return [advanced_mordai_def(), advanced_zahna_def(), advanced_zulnut_def()]


# ---------------------------------------------------------------------------
# Canonical definitions — Enemies
# ---------------------------------------------------------------------------

def make_enemy(d: dict, instance_num: int = 0) -> EnemyState:
    """Create an EnemyState from a definition dict.

    Def dicts carry only base `resolve` (0 for Mook); `resolve_current`
    starts at `resolve` plus the enemy's armor bonus (D1) — mirroring
    `Enemy.init_combat`, applied here since this is the simulator's
    equivalent one-time combat-start hook.
    """
    d = dict(d)  # shallow copy
    if instance_num > 0:
        d["instance_id"] = f"{d.get('instance_id', d['name'])}_{instance_num}"
    base_resolve = d.pop("resolve", 0)
    enemy = EnemyState(resolve=base_resolve, resolve_current=base_resolve, **d)
    if enemy.tier != "mook":
        enemy.resolve_current += combat_module.enemy_armor_resolve_bonus(enemy.armor, _ruleset())
    return enemy


def chicken_def() -> dict:
    """Chicken: Mook, TR 1."""
    return dict(
        name="Chicken",
        instance_id="chicken",
        tier="mook",
        resolve=0,
        attack_modifier=-1,
        defense_modifier=-1,
        armor="none",
    )


def harbor_thug_def() -> dict:
    """Harbor Thug: Mook, TR 1."""
    return dict(
        name="Harbor Thug",
        instance_id="harbor_thug",
        tier="mook",
        resolve=0,
        attack_modifier=0,
        defense_modifier=0,
        armor="none",
    )


def city_watch_sergeant_def() -> dict:
    """City Watch Sergeant: Named, TR 8, light armor. Matches
    `enemies/city_watch_sergeant.fof` exactly (D1 migration)."""
    return dict(
        name="City Watch Sergeant",
        instance_id="sergeant",
        tier="named",
        resolve=3,
        attack_modifier=2,
        defense_modifier=2,
        armor="light",
    )


def veteran_soldier_def() -> dict:
    """Veteran Soldier: Named, TR 10, light armor. Matches
    `enemies/veteran_soldier.fof` exactly (D1 migration)."""
    return dict(
        name="Veteran Soldier",
        instance_id="veteran",
        tier="named",
        resolve=4,
        attack_modifier=3,
        defense_modifier=3,
        armor="light",
    )


def generic_named_def(tr: int = 8) -> dict:
    """Generic Named NPC at a target TR. Minimal configuration (no
    techniques). TR = offense_value + resolve + armor_bonus (D1, DESIGN
    §4.1); durability is `resolve` directly, not derived from Endurance.
    Approximate — full recalibration against these post-D1 numbers is
    Gate G4 (task A10), not this function's job.
    """
    if tr <= 8:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            resolve=3,           # offense(+2→4) + resolve(3) + armor(light→1) = 8
            attack_modifier=2,
            defense_modifier=2,
            armor="light",
        )
    elif tr <= 10:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            resolve=4,           # offense(+3→5) + resolve(4) + armor(light→1) = 10
            attack_modifier=3,
            defense_modifier=3,
            armor="light",
        )
    else:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            resolve=5,           # offense(+3→5) + resolve(5) + armor(heavy→2) = 12
            attack_modifier=3,
            defense_modifier=2,
            armor="heavy",
        )


def generic_boss_def(tr: int = 12) -> dict:
    """Generic Boss at a target TR. No authored phase change — that is
    per-enemy stat-block content (see `archive_guardian_def`), not a
    generic engine mechanic. Approximate; see `generic_named_def`'s
    docstring on recalibration scope.
    """
    if tr <= 12:
        return dict(
            name=f"Boss (TR {tr})",
            instance_id=f"boss_tr{tr}",
            tier="boss",
            resolve=5,            # offense(+3→5) + resolve(5) + armor(heavy→2) = 12
            attack_modifier=3,
            defense_modifier=2,
            armor="heavy",
        )
    else:
        return dict(
            name=f"Boss (TR {tr})",
            instance_id=f"boss_tr{tr}",
            tier="boss",
            resolve=7,
            attack_modifier=4,
            defense_modifier=3,
            armor="heavy",
        )


def archive_guardian_def() -> dict:
    """Archive Guardian: Boss, TR 17, heavy armor. Matches
    `enemies/archive_guardian.fof` exactly (D1 migration corrected the
    published TR from 16 to 14 — the old `special` bonus was double-
    counted at authoring time, DESIGN §4.1; A8/G1 retuned base Resolve
    5 -> 8 to clear the median-3-exchange floor under the worst-case
    rider->Easy snowball, per DESIGN §5-bis — TR 14 -> 17).

    `phases` is the enemy's authored, purely-narrative `resolve_threshold`
    trigger (matches the .fof's `phases:` block). `special_attack_mod`/
    `special_ignores_tier1` model its authored "Special" text (Reduced
    Mode: attack_modifier drops to +1, ignores Tier 1 Conditions entirely)
    — boss-specific flavor, not a generic engine mechanic.
    """
    return dict(
        name="Archive Guardian",
        instance_id="guardian",
        tier="boss",
        resolve=8,
        attack_modifier=3,
        defense_modifier=1,
        armor="heavy",
        phases=[{"resolve_threshold": 2, "description": "Reduced Mode"}],
        special_attack_mod=1,
        special_ignores_tier1=True,
    )


# ---------------------------------------------------------------------------
# Series definitions (from the balancing plan)
# ---------------------------------------------------------------------------

def get_series() -> dict[str, list[tuple[str, list[dict], list[tuple[dict, int]]]]]:
    """Return all simulation series as {series_id: [(label, pcs, enemies)]}."""
    party3 = standard_party()
    party4 = four_player_party()
    advanced = advanced_party()

    return {
        "A": [
            ("A1: 3 Mooks (TR 3)", party3, [(chicken_def(), 3)]),
            ("A2: 5 Mooks (TR 5)", party3, [(chicken_def(), 5)]),
            ("A3: 7 Mooks (TR 7)", party3, [(chicken_def(), 7)]),
            ("A4: 10 Mooks (TR 10)", party3, [(chicken_def(), 10)]),
            ("A5: 15 Mooks (TR 15)", party3, [(chicken_def(), 15)]),
        ],
        "B": [
            ("B1: 1 Named (TR 8) solo", party3, [(generic_named_def(8), 1)]),
            ("B2: 1 Named (TR 10) solo", party3, [(generic_named_def(10), 1)]),
            ("B3: 1 Named (TR 12) solo", party3, [(generic_named_def(12), 1)]),
            ("B4: 1 Named (TR 8) + 3 Mooks", party3,
             [(generic_named_def(8), 1), (chicken_def(), 3)]),
            ("B5: 2 Named (TR 8) each", party3, [(generic_named_def(8), 2)]),
        ],
        "C": [
            ("C1: 1 Boss (TR 12) solo", party3, [(generic_boss_def(12), 1)]),
            ("C2: 1 Boss (TR 16) solo", party3, [(generic_boss_def(16), 1)]),
            ("C3: 1 Boss (TR 12) + 2 Mooks", party3,
             [(generic_boss_def(12), 1), (chicken_def(), 2)]),
            ("C4: 1 Boss (TR 16) + 4 Mooks", party3,
             [(generic_boss_def(16), 1), (chicken_def(), 4)]),
        ],
        "D": [
            ("D1: 2 PCs vs Named(8) + 5 Mooks", party3[:2],
             [(generic_named_def(8), 1), (chicken_def(), 5)]),
            ("D2: 3 PCs vs Named(8) + 5 Mooks", party3,
             [(generic_named_def(8), 1), (chicken_def(), 5)]),
            ("D3: 4 PCs vs Named(8) + 5 Mooks", party4,
             [(generic_named_def(8), 1), (chicken_def(), 5)]),
            ("D4: 5 PCs vs Named(8) + 5 Mooks",
             party4 + [drew_def()],
             [(generic_named_def(8), 1), (chicken_def(), 5)]),
        ],
        "E": [
            ("E1: Advanced vs Named (TR 8)", advanced, [(generic_named_def(8), 1)]),
            ("E2: Advanced vs Boss (TR 12)", advanced, [(generic_boss_def(12), 1)]),
            ("E3: Advanced vs Boss (TR 16)", advanced, [(generic_boss_def(16), 1)]),
        ],
    }


# ---------------------------------------------------------------------------
# Series F: Sequential encounters (special handling)
# ---------------------------------------------------------------------------

def run_sequential_series(iterations: int = 200, seed: Optional[int] = None) -> list[AggregateResult]:
    """Run Series F: sequential encounters without full recovery."""
    if seed is not None:
        random.seed(seed)

    sequences = [
        ("F1: Skirmish → Standard", [
            ([(chicken_def(), 3)], "Skirmish"),
            ([(generic_named_def(8), 1)], "Standard"),
        ]),
        ("F2: Skirmish → Standard → Hard", [
            ([(chicken_def(), 3)], "Skirmish"),
            ([(generic_named_def(8), 1)], "Standard"),
            ([(generic_named_def(8), 1), (chicken_def(), 3)], "Hard"),
        ]),
        ("F3: Standard → Hard (3 PCs)", [
            ([(generic_named_def(8), 1)], "Standard"),
            ([(generic_named_def(8), 1), (chicken_def(), 3)], "Hard"),
        ]),
    ]

    results = []
    for label, encounter_sequence in sequences:
        sim_results = []
        for _ in range(iterations):
            pcs = [make_pc(d) for d in standard_party()]
            survived_all = True

            for enemy_defs, _ in encounter_sequence:
                # Build fresh enemies
                enemies = []
                for edef, count in enemy_defs:
                    for j in range(count):
                        enemies.append(make_enemy(edef, j + 1 if count > 1 else 0))

                result = run_combat(pcs, enemies)

                if not result.party_wins:
                    survived_all = False
                    sim_results.append(result)
                    break

                # Carry over PC state (don't reset Endurance or conditions)
                # But do clear T1 conditions (already done by cleanup)
                # Withdraw recovery between fights: each PC gets 2 End back
                for pc in pcs:
                    if not pc.is_broken:
                        pc.endurance_current = min(
                            pc.endurance_max,
                            pc.endurance_current + 2,
                        )

            if survived_all:
                sim_results.append(SimResult(
                    party_wins=True,
                    exchanges=sum(1 for _ in encounter_sequence),  # Approximate
                    sparks_spent=sum(p.sparks_spent for p in pcs),
                    pcs_broken=[p.name for p in pcs if p.is_broken],
                    endurance_remaining={p.name: p.endurance_current for p in pcs},
                    enemies_remaining=0,
                ))

        results.append(_aggregate(sim_results, label, iterations))

    return results


# ---------------------------------------------------------------------------
# Gate G3: Aggressive posture knob K1 (BRIEF D8, DESIGN §5)
#
# "Test, don't adopt blind" — K1 (the +1 Aggressive reaction surcharge
# applies to the first reaction per exchange only) is a one-off
# experimental knob, not a settled rule. It is deliberately implemented
# as its own self-contained fight loop below rather than threaded through
# `run_combat`/`_enemy_attack`/`choose_pc_reaction` — those are exercised
# by every other Series and already under test; a knob that may be
# rejected has no business touching shared, tested code paths. It still
# routes every rule computation (cost table, dice, condition tiers)
# through `app.game.combat` — only the *choice of which posture's cost to
# look up* is new, per the C1 "simulator may never reimplement a rule"
# boundary.
# ---------------------------------------------------------------------------

def _g3_pc_def() -> dict:
    """G3's solo PC (BRIEF D8 / DESIGN §5 G3: "Unarmored Endurance-3
    PC"). Reuses Zahna's canonical stat block exactly — she already is
    Endurance 3 and unarmored — rather than inventing a new character for
    a one-off experiment."""
    return zahna_def()


def _g3_named_def() -> dict:
    """A deliberately weak, unarmored Named enemy for G3's isolated
    experiment — attack_modifier 0, resolve 2. Not tied to any TR
    formula (this experiment measures posture, not encounter balance);
    weak enough that a solo Endurance-3 PC has a genuine chance, strong
    enough (Tier 2 capable) that Broken is reachable at all.
    """
    return dict(
        name="G3 Foe", instance_id="g3_foe", tier="named",
        resolve=2, attack_modifier=0, defense_modifier=0, armor="none",
    )


def _g3_enemies() -> list[EnemyState]:
    """G3's enemy composition: two identical weak Named enemies, no
    Mooks.

    Two are required, not one — with a single attacker there is only
    ever one reaction per exchange, and "first reaction" is the *only*
    reaction, making K1 indistinguishable from baseline by construction.
    Both must be Tier 2 capable (Named, not Mook) for a Broken rate to be
    measurable at all: `incoming_tier` is fixed at 1 for Mooks
    (mirrored below from `_enemy_attack`), and Tier 1 alone never
    escalates to Broken.
    """
    return [make_enemy(_g3_named_def(), i) for i in range(2)]


def _g3_reaction_cost(
    reaction: str, posture: str, is_first_reaction: bool, k1_enabled: bool, ruleset,
) -> int:
    """K1's cost lookup for the G3 gate's before/after comparison.

    Historical note (2026-07-10): K1 was **adopted** as the canonical
    rule after this gate passed robustly across 7 seeds (Series 8) —
    `combat_module.reaction_cost` now applies the first-reaction-only
    surcharge natively via its own `is_first_reaction` parameter and
    `facet.yaml`'s `reaction_cost_modifier_applies`. This wrapper exists
    only so `run_g3_gate` can still reproduce the **pre-adoption
    baseline** (every reaction pays the full surcharge, `k1_enabled=
    False`) for the historical before/after record — passing
    `is_first_reaction=True` unconditionally reproduces that old
    behaviour through the same, now-canonical function, rather than a
    second copy of the rule.
    """
    return combat_module.reaction_cost(
        reaction, posture, ruleset,
        is_first_reaction=(True if not k1_enabled else is_first_reaction),
    )


def _g3_pc_reacts(
    pc: PCState,
    incoming_tier: int,
    enemy_difficulty: str,
    posture: str,
    is_first_reaction: bool,
    k1_enabled: bool,
    ruleset,
) -> None:
    """Resolve one incoming attack against G3's solo PC.

    Mirrors `_enemy_attack`'s reaction handling (same Dodge/Parry choice
    heuristic, same `app.game.combat` calls for roll/condition) — the
    sole divergence is the K1-adjusted cost lookup above.
    """
    parry_mod = pc.strength_mod + pc.combat_mod
    dodge_mod = pc.dexterity_mod
    reaction = "parry" if parry_mod >= dodge_mod else "dodge"

    cost = _g3_reaction_cost(reaction, posture, is_first_reaction, k1_enabled, ruleset)
    if pc.endurance_current < cost:
        reaction = "absorb"

    if reaction == "absorb":
        if incoming_tier <= 0:
            return
        condition = _choose_condition(pc.conditions, ruleset) if incoming_tier >= 2 else "winded"
        result = combat_module.apply_condition(pc.conditions, condition, incoming_tier, ruleset)
        if result.broken:
            _mark_broken(pc)
        return

    pc.endurance_current = max(0, pc.endurance_current - cost)
    mod = dodge_mod if reaction == "dodge" else parry_mod
    roll_result = combat_module.roll(mod, enemy_difficulty, ruleset)
    if roll_result.outcome == "full_success":
        return

    # Same non-stacking rule as `_enemy_attack`. G3's PC is unarmored by
    # construction, so armor never reduces here — routing through the shared
    # rule keeps the reduction in one place without changing G3's numbers.
    incoming = combat_module.resolve_incoming_condition(
        incoming_tier,
        pc.armor,
        pc.armor_downgrades_remaining,
        ruleset,
        reaction_downgraded=(roll_result.outcome == "partial_success"),
    )
    pc.armor_downgrades_remaining = incoming.downgrades_remaining
    final_tier = incoming.tier
    if final_tier <= 0:
        return

    condition = _choose_condition(pc.conditions, ruleset) if final_tier >= 2 else "winded"
    result = combat_module.apply_condition(pc.conditions, condition, final_tier, ruleset)
    if result.broken:
        _mark_broken(pc)


def _g3_pc_strike(pc: PCState, target: EnemyState, ruleset) -> None:
    """G3's PC Strike: no Press, no Sparks.

    Deliberately simpler than the shared `_pc_strike` — `should_press`'s
    policy spends 1 Endurance *before* reactions are even resolved for
    this exchange, which confounds the posture experiment: Zahna's
    Endurance-3 pool is exactly large enough that one pre-spent point
    changes whether K1's discount ever crosses an affordability
    threshold. G3 isolates the posture variable; Press/Spark spending is
    a different, orthogonal resource decision the gate isn't testing.
    Still routes the roll and Resolve depletion through `app.game.combat`
    exactly like `_pc_strike` does.
    """
    if pc.posture == "withdrawn":
        return

    modifier = pc.strength_mod + pc.combat_mod
    difficulty = combat_module.target_strike_difficulty("Standard", target.conditions, ruleset)
    strike = combat_module.resolve_strike(
        modifier, pc.posture, pc.conditions, ruleset,
        combat_module.StrikeOptions(difficulty=difficulty),
    )

    if strike.outcome == "failure":
        combat_module.apply_condition(pc.conditions, "winded", 1, ruleset)
        return

    # No enemy reaction (A14 F5): Resolve depletes by the Strike's outcome.
    effective_outcome = strike.outcome
    phase_thresholds = [p["resolve_threshold"] for p in target.phases]
    damage = combat_module.apply_resolve_damage(
        target.resolve_current, effective_outcome, ruleset, phase_thresholds,
    )
    target.resolve_current = damage.resolve_current
    if damage.defeated:
        target.is_removed = True
        return

    if effective_outcome == "full_success":
        condition = _choose_rider(target, ruleset)
        if condition is not None:
            tier2_ids = {c.id for c in ruleset.combat.conditions.tier2}
            tier = 2 if condition in tier2_ids else 1
            combat_module.apply_condition(target.conditions, condition, tier, ruleset, is_rider=True)


G3_EXCHANGES = 2  # BRIEF D8 / DESIGN §5 G3: bounded acute-burst window — see run_g3_fight's docstring


def run_g3_fight(posture: str, k1_enabled: bool, verbose: bool = False) -> SimResult:
    """One G3-gate combat: a solo Endurance-3 unarmored PC, posture fixed
    for the whole fight (bypassing `choose_pc_posture`'s Endurance-ratio
    logic entirely — G3 isolates the posture variable itself), against
    `_g3_enemies()`, bounded to `G3_EXCHANGES` (2).

    Bounded, not fight-to-conclusion — deliberately. A fight-to-conclusion
    version of this same matchup was tried first and rejected: over a
    multi-exchange war of attrition, cumulative Tier 2 exposure converges
    every posture toward the same Broken ceiling (measured empirically:
    baseline Aggressive and Measured both landed at ~84% Broken, no
    daylight between them at all — the reaction-cost differential a
    reaction ROLL's success chance never depends on posture, only the
    Endurance to attempt one does). The "Aggressive death-spiral" PT01
    and BRIEF D8 describe is specifically an *opening-exchange* alpha-
    strike phenomenon: burn Endurance reacting to the first attack of a
    multi-attacker exchange, then have nothing left for the second. That
    signal is only visible in a short, bounded window, not a long-run
    average. `party_wins` here means "cleared both enemies within the
    window" (the offense-edge proxy for the gate's win-rate-delta check);
    `pcs_broken`/`is_broken` is the safety signal K1 is meant to improve.
    """
    ruleset = _ruleset()
    pc = make_pc(_g3_pc_def())
    pc.posture = posture
    enemies = _g3_enemies()

    for _exchange in range(1, G3_EXCHANGES + 1):
        active_enemies = [e for e in enemies if not e.is_out]
        if not active_enemies or pc.is_broken:
            break

        # PC strikes (Press/Spark-free — see `_g3_pc_strike`'s docstring).
        target = choose_pc_target(pc, enemies)
        if target is not None:
            _g3_pc_strike(pc, target, ruleset)
        active_enemies = [e for e in enemies if not e.is_out]
        if not active_enemies:
            break

        # Every active enemy attacks the solo PC this exchange — this
        # simultaneity is what makes K1 measurable at all (BRIEF D8).
        for i, enemy in enumerate(active_enemies):
            if pc.is_broken:
                break
            incoming_tier = 1 if enemy.tier == "mook" else 2
            difficulty = "Standard"
            if enemy.posture == "aggressive":
                difficulty = "Hard"
            elif enemy.posture == "defensive":
                difficulty = "Easy"
            _g3_pc_reacts(
                pc, incoming_tier, difficulty, posture,
                is_first_reaction=(i == 0), k1_enabled=k1_enabled, ruleset=ruleset,
            )

        if pc.is_broken:
            break

        combat_module.end_exchange(pc.conditions, ruleset)
        for enemy in enemies:
            if not enemy.is_out:
                combat_module.end_exchange(enemy.conditions, ruleset)

    cleared = all(e.is_out for e in enemies)
    return _build_result(cleared, G3_EXCHANGES, [pc], enemies)


def run_g3_gate(iterations: int = 200, seed: Optional[int] = None) -> dict[str, AggregateResult]:
    """Gate G3 (DESIGN §5, BRIEF D8): does K1 soften the Aggressive
    death-spiral without erasing the tradeoff?

    Runs all four configurations (Aggressive/Measured x baseline/K1),
    each re-seeded identically so the four runs are directly comparable.
    """
    configs = [
        ("baseline_aggressive", "aggressive", False),
        ("baseline_measured", "measured", False),
        ("k1_aggressive", "aggressive", True),
        ("k1_measured", "measured", True),
    ]
    results = {}
    for key, posture, k1_enabled in configs:
        if seed is not None:
            random.seed(seed)
        runs = [run_g3_fight(posture, k1_enabled) for _ in range(iterations)]
        label = f"G3: {posture} ({'K1' if k1_enabled else 'baseline'})"
        results[key] = _aggregate(runs, label, iterations)
    return results


def g3_verdict(results: dict[str, AggregateResult]) -> dict:
    """Compute the G3 pass/fail verdict per DESIGN §5's two-part
    condition. Both parts must hold to adopt K1.
    """
    base_agg = results["baseline_aggressive"]
    k1_agg = results["k1_aggressive"]
    base_meas = results["baseline_measured"]
    k1_meas = results["k1_measured"]

    if base_agg.mean_pcs_broken > 0:
        broken_cut = (base_agg.mean_pcs_broken - k1_agg.mean_pcs_broken) / base_agg.mean_pcs_broken
        broken_cut_defined = True
    else:
        broken_cut = 0.0
        broken_cut_defined = False

    base_delta = base_agg.win_rate - base_meas.win_rate
    k1_delta = k1_agg.win_rate - k1_meas.win_rate
    delta_preserved = abs(k1_delta - base_delta) <= 0.05

    broken_cut_passes = broken_cut_defined and broken_cut >= 0.15
    adopt = broken_cut_passes and delta_preserved

    return {
        "broken_cut": broken_cut,
        "broken_cut_defined": broken_cut_defined,
        "broken_cut_passes": broken_cut_passes,
        "base_delta": base_delta,
        "k1_delta": k1_delta,
        "delta_preserved": delta_preserved,
        "adopt": adopt,
    }


def print_g3_result(results: dict[str, AggregateResult]) -> None:
    """Print the G3 gate's four configurations and the pass/fail verdict."""
    for r in results.values():
        print_result(r)

    v = g3_verdict(results)
    print(f"\n{'=' * 60}")
    print("  Gate G3 verdict — Aggressive posture knob K1")
    print(f"{'=' * 60}")
    if v["broken_cut_defined"]:
        print(f"  Broken-rate cut (Aggressive, baseline->K1): {v['broken_cut']:.1%} (pass: >= 15%)")
    else:
        print("  Broken-rate cut: undefined (baseline Aggressive never Broken)")
    print(f"  Win-rate delta, baseline (Agg - Measured): {v['base_delta']:+.1%}")
    print(f"  Win-rate delta, K1 (Agg - Measured):       {v['k1_delta']:+.1%}")
    print(f"  Delta preserved within +/-5pp: {v['delta_preserved']}")
    print(f"  Verdict: {'ADOPT K1' if v['adopt'] else 'DO NOT ADOPT K1'}")


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_result(result: AggregateResult):
    """Print a formatted summary of an aggregate result."""
    print(f"\n{'=' * 60}")
    print(f"  {result.label}")
    print(f"{'=' * 60}")
    print(f"  Iterations: {result.iterations}")
    print(f"  Win rate:   {result.win_rate:.1%} "
          f"(95% CI: {result.win_rate_ci_low:.1%}–{result.win_rate_ci_high:.1%})")
    print(f"  Wins/Losses: {result.wins}/{result.losses}")
    print(f"  Exchanges:  mean={result.mean_exchanges}, median={result.median_exchanges}")
    print(f"  Sparks:     mean={result.mean_sparks_spent}")
    print(f"  PCs Broken: mean={result.mean_pcs_broken}")
    for name, stats in result.endurance_stats.items():
        print(f"  {name} End: mean={stats['mean']}, "
              f"range=[{stats['min']}, {stats['max']}]")


def print_summary_table(results: list[AggregateResult]):
    """Print a compact summary table."""
    print(f"\n{'Label':<45} {'Win%':>6} {'CI':>15} {'Exch':>6} {'Sparks':>7} {'Broken':>7}")
    print("-" * 95)
    for r in results:
        ci = f"{r.win_rate_ci_low:.0%}–{r.win_rate_ci_high:.0%}"
        print(f"{r.label:<45} {r.win_rate:>5.0%} {ci:>15} "
              f"{r.mean_exchanges:>6.1f} {r.mean_sparks_spent:>7.1f} {r.mean_pcs_broken:>7.2f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Combat simulator for Facets of Origin encounter balancing"
    )
    parser.add_argument("--series", type=str, default=None,
                        help="Run a specific series (A, B, C, D, E, F, G3, or 'all')")
    parser.add_argument("--iterations", "-n", type=int, default=200,
                        help="Iterations per configuration (default: 200)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print first iteration details")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    all_results: list[AggregateResult] = []
    all_series = get_series()

    series_to_run = []
    if args.series:
        if args.series.lower() == "all":
            series_to_run = list(all_series.keys()) + ["F"]
        else:
            series_to_run = [s.strip().upper() for s in args.series.split(",")]

    if not series_to_run:
        parser.print_help()
        return

    for series_id in series_to_run:
        if series_id == "F":
            results = run_sequential_series(args.iterations, args.seed)
            all_results.extend(results)
            for r in results:
                print_result(r)
        elif series_id == "G3":
            g3_results = run_g3_gate(args.iterations, args.seed)
            print_g3_result(g3_results)
            all_results.extend(g3_results.values())
        elif series_id in all_series:
            for label, pcs, enemies in all_series[series_id]:
                result = run_simulation(
                    pcs, enemies,
                    iterations=args.iterations,
                    label=label,
                    verbose=args.verbose,
                    seed=args.seed,
                )
                all_results.append(result)
                print_result(result)
        else:
            print(f"Unknown series: {series_id}")

    if len(all_results) > 1:
        print_summary_table(all_results)

    if args.json:
        json_results = []
        for r in all_results:
            json_results.append({
                "label": r.label,
                "iterations": r.iterations,
                "win_rate": r.win_rate,
                "ci_low": r.win_rate_ci_low,
                "ci_high": r.win_rate_ci_high,
                "mean_exchanges": r.mean_exchanges,
                "median_exchanges": r.median_exchanges,
                "mean_sparks_spent": r.mean_sparks_spent,
                "mean_pcs_broken": r.mean_pcs_broken,
                "endurance_stats": r.endurance_stats,
            })
        print(json.dumps(json_results, indent=2))


if __name__ == "__main__":
    main()
