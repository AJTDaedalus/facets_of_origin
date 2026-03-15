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

# ---------------------------------------------------------------------------
# Constants
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
    # Offensive: Strike uses strength + combat
    strength_mod: int = 0
    combat_mod: int = 0
    # Defensive: Dodge uses dexterity, Parry uses strength + combat
    dexterity_mod: int = 0
    # State
    conditions: list[str] = field(default_factory=list)
    persistent_conditions: set[str] = field(default_factory=set)
    posture: str = "measured"
    is_broken: bool = False


@dataclass
class EnemyState:
    """An enemy's combat state for one simulation run."""
    name: str
    instance_id: str
    tier: str  # "mook" | "named" | "boss"
    endurance_max: int
    endurance_current: int
    attack_modifier: int
    defense_modifier: int
    armor: str
    posture: str = "measured"
    conditions: list[str] = field(default_factory=list)
    persistent_conditions: set[str] = field(default_factory=set)
    is_broken: bool = False
    is_removed: bool = False
    # Boss phase change
    has_phase_change: bool = False
    phase_changed: bool = False
    phase2_attack_mod: int = 0
    phase2_endurance: int = 4
    phase2_ignores_t1: bool = False

    @property
    def is_out(self) -> bool:
        return self.is_broken or self.is_removed


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
# ---------------------------------------------------------------------------

def apply_condition(target, condition: str, tier: int, is_zero_end_absorb: bool = False):
    """Apply a condition to a combatant, handling escalation and persistence.

    Args:
        target: PCState or EnemyState
        condition: condition ID (e.g. "staggered", "winded")
        tier: 1 or 2
        is_zero_end_absorb: True if this is an Absorb at 0 Endurance
    """
    if target.is_broken or (hasattr(target, "is_removed") and target.is_removed):
        return

    # 0-Endurance Absorb: treat as T2 and persistent
    if is_zero_end_absorb and tier < 2:
        tier = 2
        # Upgrade T1 condition to a T2 condition
        condition = "staggered"  # Default T2 when upgrading from T1

    # Check for Broken escalation: same T2 condition twice
    if tier >= 2 and condition in target.conditions:
        # Same T2 already present → Broken
        _apply_broken(target)
        return

    target.conditions.append(condition)
    if is_zero_end_absorb or tier >= 2:
        target.persistent_conditions.add(condition)


def _apply_broken(target):
    """Mark a combatant as Broken. Handle Boss phase changes."""
    if isinstance(target, EnemyState) and target.has_phase_change and not target.phase_changed:
        # Boss phase change: reset instead of breaking
        target.phase_changed = True
        target.conditions.clear()
        target.persistent_conditions.clear()
        target.attack_modifier = target.phase2_attack_mod
        target.endurance_current = target.phase2_endurance
        target.endurance_max = target.phase2_endurance
        return

    target.is_broken = True
    if isinstance(target, EnemyState):
        target.is_removed = True


def cleanup_end_of_exchange(combatant):
    """End-of-exchange cleanup: clear non-persistent T1 conditions."""
    if combatant.is_broken:
        return
    if hasattr(combatant, "is_removed") and combatant.is_removed:
        return

    # Keep persistent conditions and T2 conditions
    remaining = []
    for c in combatant.conditions:
        if c in combatant.persistent_conditions:
            remaining.append(c)
        elif c in TIER2_CONDITIONS:
            remaining.append(c)
        # T1 conditions not in persistent_conditions are cleared
    combatant.conditions = remaining

    # Withdrawn recovery
    if combatant.posture == "withdrawn":
        combatant.endurance_current = min(
            combatant.endurance_max,
            combatant.endurance_current + 2,
        )


def armor_downgrade(tier: int, armor: str) -> int:
    """Downgrade condition tier by armor. Returns new tier (0 = negated).

    Per PHB:
    - Light armor: Tier 2 becomes Tier 1 (only affects T2)
    - Heavy armor: Tier 3 (Broken) becomes Tier 2 (only affects T3)
    """
    if armor == "light" and tier == 2:
        return 1
    elif armor == "heavy" and tier == 3:
        return 2
    return tier


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
    # Defensive if has T2 conditions and low endurance
    if enemy.endurance_current == 0 and enemy.tier != "mook":
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

def should_spend_spark(pc: PCState, target: EnemyState) -> int:
    """Decide how many Sparks to spend on this Strike."""
    if pc.sparks <= 0:
        return 0
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


def should_enemy_react(enemy: EnemyState, incoming_tier: int) -> bool:
    """Decide if a Named/Boss enemy should spend Endurance to Parry."""
    if enemy.tier == "mook":
        return False
    if enemy.endurance_current <= 0:
        return False
    # Don't bother reacting to T1 (clears at end of exchange)
    if incoming_tier <= 1:
        return False
    # React to T2 conditions
    return True


# ---------------------------------------------------------------------------
# Resolution: PC Strike against Enemy
# ---------------------------------------------------------------------------

def resolve_pc_strike(pc: PCState, target: EnemyState, verbose: bool = False):
    """Resolve a PC's Strike against an enemy target.

    Handles: posture offense, difficulty from conditions, Sparks, Press,
    enemy reaction (Parry for Named/Boss), armor, condition application,
    Mook removal, and Boss phase changes.
    """
    if pc.posture == "withdrawn":
        return  # Cannot attack

    # Determine extra dice (Sparks + Press)
    sparks = should_spend_spark(pc, target)
    press = should_press(pc, target)

    if sparks > 0 and pc.sparks >= sparks:
        pc.sparks -= sparks
        pc.sparks_spent += sparks
    else:
        sparks = 0

    if press:
        pc.endurance_current -= 1

    extra_dice = sparks + (1 if press else 0)

    # Calculate modifier: strength + combat + posture offense
    total_mod = pc.strength_mod + pc.combat_mod
    posture_off = POSTURE_OFFENSE.get(pc.posture, 0)
    if posture_off is not None:
        total_mod += posture_off

    # Staggered condition reduces offense by 1
    if "staggered" in pc.conditions:
        total_mod -= 1

    # Difficulty: Standard, Easy if target has T2 conditions
    difficulty = "Standard"
    if any(c in TIER2_CONDITIONS for c in target.conditions):
        difficulty = "Easy"

    outcome, dice, total = combat_roll(total_mod, difficulty, extra_dice)

    if verbose:
        print(f"  {pc.name} strikes {target.instance_id}: "
              f"dice={dice} mod={total_mod} diff={difficulty} total={total} → {outcome}")

    if outcome == "failure":
        # 6-: consequence for attacker (T1 condition)
        apply_condition(pc, "winded", 1)
        return

    # Determine base condition tier
    if outcome == "full_success":
        base_tier = 2
    else:  # partial_success
        base_tier = 1

    # Mook: any success removes them
    if target.tier == "mook":
        target.is_removed = True
        if verbose:
            print(f"    → {target.instance_id} removed (Mook)")
        return

    # Named/Boss: enemy may react
    final_tier = base_tier
    reaction_downgraded = False

    if should_enemy_react(target, base_tier):
        # Enemy Parries: spend 1 Endurance
        reaction_cost = max(0, 1 + POSTURE_REACTION_COST.get(target.posture, 0))
        if target.endurance_current >= reaction_cost:
            target.endurance_current -= reaction_cost
            parry_outcome, _, _ = combat_roll(target.defense_modifier, "Standard")
            if verbose:
                print(f"    {target.instance_id} parries: → {parry_outcome}")
            if parry_outcome == "full_success":
                return  # Attack fully deflected
            elif parry_outcome == "partial_success":
                final_tier = max(0, base_tier - 1)
                reaction_downgraded = True

    # Apply armor (doesn't stack with reaction downgrade)
    armor_tier = armor_downgrade(base_tier, target.armor)
    if reaction_downgraded:
        # Take the greater reduction (don't stack)
        final_tier = min(final_tier, armor_tier)
    else:
        final_tier = armor_tier

    # 0-Endurance Absorb override: conditions become T2 persistent
    is_zero_end = (target.endurance_current <= 0 and target.tier != "mook")

    if final_tier <= 0:
        if verbose:
            print(f"    → condition negated (armor/reaction)")
        return

    # Choose which condition to apply
    if final_tier >= 2:
        # Choose T2 that target already has (to trigger Broken), else staggered
        if "staggered" in target.conditions:
            condition = "staggered"
        elif "cornered" in target.conditions:
            condition = "cornered"
        else:
            condition = "staggered"
    else:
        condition = "winded"

    apply_condition(target, condition, final_tier, is_zero_end_absorb=is_zero_end)

    if verbose:
        broken_str = " → BROKEN!" if target.is_broken else ""
        print(f"    → {target.instance_id} takes {condition} (T{final_tier})"
              f"{' [persistent]' if is_zero_end else ''}{broken_str}")


# ---------------------------------------------------------------------------
# Resolution: Enemy Attack against PC
# ---------------------------------------------------------------------------

def resolve_enemy_attack(enemy: EnemyState, target: PCState, verbose: bool = False):
    """Resolve an enemy's attack against a PC.

    NPCs don't roll. The incoming condition tier is determined by enemy type.
    The PC reacts (Dodge, Parry, or Absorb).
    """
    if target.is_broken:
        return

    # Incoming tier by enemy type
    if enemy.tier == "mook":
        incoming_tier = 1
    else:
        incoming_tier = 2

    # Boss phase 2 may ignore T1 conditions (irrelevant for attacks)

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
        # Take full hit
        is_zero_end = target.endurance_current <= 0
        final_tier = incoming_tier

        # Armor downgrade
        armor_tier = armor_downgrade(incoming_tier, target.armor)
        final_tier = armor_tier

        # 0-End override
        if is_zero_end and final_tier > 0:
            final_tier = max(final_tier, 2)

        if final_tier <= 0:
            if verbose:
                print(f"    → negated by armor")
            return

        # Choose condition
        if final_tier >= 2:
            if "staggered" in target.conditions:
                condition = "staggered"
            elif "cornered" in target.conditions:
                condition = "cornered"
            else:
                condition = "staggered"
        else:
            condition = "winded"

        apply_condition(target, condition, final_tier, is_zero_end_absorb=is_zero_end)
        if verbose:
            broken_str = " → BROKEN!" if target.is_broken else ""
            print(f"    → {target.name} takes {condition} (T{final_tier})"
                  f"{' [persistent]' if is_zero_end else ''}{broken_str}")
        return

    # Active reaction: Dodge or Parry
    # Pay Endurance cost
    base_cost = 1
    posture_adj = POSTURE_REACTION_COST.get(target.posture, 0)
    cost = max(0, base_cost + posture_adj)
    target.endurance_current = max(0, target.endurance_current - cost)

    # Roll reaction
    if reaction == "dodge":
        mod = target.dexterity_mod
    else:  # parry
        mod = target.strength_mod + target.combat_mod

    outcome, dice, total = combat_roll(mod, difficulty)

    if verbose:
        print(f"    {target.name} rolls {reaction}: dice={dice} total={total} → {outcome}")

    if outcome == "full_success":
        # Fully avoided
        if verbose:
            print(f"    → avoided entirely")
        return

    # Determine final tier
    reaction_downgraded = False
    final_tier = incoming_tier
    if outcome == "partial_success":
        final_tier = max(0, incoming_tier - 1)
        reaction_downgraded = True

    # Armor downgrade (doesn't stack with reaction)
    armor_tier = armor_downgrade(incoming_tier, target.armor)
    if reaction_downgraded:
        final_tier = min(final_tier, armor_tier)
    else:
        final_tier = armor_tier

    if final_tier <= 0:
        if verbose:
            print(f"    → condition negated")
        return

    # Choose condition
    if final_tier >= 2:
        if "staggered" in target.conditions:
            condition = "staggered"
        elif "cornered" in target.conditions:
            condition = "cornered"
        else:
            condition = "staggered"
    else:
        condition = "winded"

    apply_condition(target, condition, final_tier)
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
) -> SimResult:
    """Run a single combat encounter to completion.

    Returns a SimResult with win/loss, exchanges, Sparks spent, etc.
    """
    for exchange in range(1, MAX_EXCHANGES + 1):
        active_pcs = [p for p in pcs if not p.is_broken]
        active_enemies = [e for e in enemies if not e.is_out]

        if not active_enemies:
            return _build_result(True, exchange - 1, pcs, enemies)
        if not active_pcs:
            return _build_result(False, exchange - 1, pcs, enemies)

        if verbose:
            print(f"\n--- Exchange {exchange} ---")
            for p in active_pcs:
                print(f"  {p.name}: End={p.endurance_current}/{p.endurance_max} "
                      f"Sparks={p.sparks} Cond={p.conditions}")
            for e in active_enemies:
                end_str = f"End={e.endurance_current}/{e.endurance_max}" if e.tier != "mook" else "Mook"
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
            resolve_pc_strike(pc, target, verbose)
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
            resolve_enemy_attack(enemy, target, verbose)

        # Check if all PCs broken after enemy actions
        active_pcs = [p for p in pcs if not p.is_broken]
        if not active_pcs:
            return _build_result(False, exchange, pcs, enemies)

        # 4. End-of-exchange cleanup
        for pc in pcs:
            cleanup_end_of_exchange(pc)
        for enemy in enemies:
            if not enemy.is_out:
                cleanup_end_of_exchange(enemy)
                # Boss phase 2: ignore T1 conditions
                if (isinstance(enemy, EnemyState) and enemy.phase_changed
                        and enemy.phase2_ignores_t1):
                    enemy.conditions = [
                        c for c in enemy.conditions if c in TIER2_CONDITIONS
                    ]

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
) -> AggregateResult:
    """Run N iterations of a combat encounter and aggregate results.

    Args:
        pc_defs: List of PC definition dicts (see make_pc()).
        enemy_defs: List of (enemy_def_dict, count) tuples.
        iterations: Number of simulation runs.
        label: Label for this simulation series.
        verbose: Print per-exchange details.
        seed: Random seed for reproducibility.

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

        result = run_combat(pcs, enemies, verbose=(verbose and i == 0))
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
    """Create an EnemyState from a definition dict."""
    d = dict(d)  # shallow copy
    if instance_num > 0:
        d["instance_id"] = f"{d.get('instance_id', d['name'])}_{instance_num}"
    return EnemyState(**d)


def chicken_def() -> dict:
    """Chicken: Mook, TR 1."""
    return dict(
        name="Chicken",
        instance_id="chicken",
        tier="mook",
        endurance_max=0,
        endurance_current=0,
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
        endurance_max=0,
        endurance_current=0,
        attack_modifier=0,
        defense_modifier=0,
        armor="none",
    )


def city_watch_sergeant_def() -> dict:
    """City Watch Sergeant: Named, TR 8, light armor."""
    return dict(
        name="City Watch Sergeant",
        instance_id="sergeant",
        tier="named",
        endurance_max=6,
        endurance_current=6,
        attack_modifier=2,
        defense_modifier=2,
        armor="light",
    )


def veteran_soldier_def() -> dict:
    """Veteran Soldier: Named, TR 10, light armor (from sim log)."""
    return dict(
        name="Veteran Soldier",
        instance_id="veteran",
        tier="named",
        endurance_max=6,
        endurance_current=6,
        attack_modifier=2,
        defense_modifier=2,
        armor="light",
    )


def generic_named_def(tr: int = 8) -> dict:
    """Generic Named NPC at a target TR. Minimal configuration."""
    # TR = offense + durability + armor + techniques
    # For simplicity: no armor, no techniques
    # offense = attack_mod + 2, durability by endurance
    # TR 8 = offense 4 (atk_mod +2) + durability 3 (end 6) + armor 1 (light)
    # TR 10 = offense 4 (atk_mod +2) + durability 4 (end 8) + armor 1 + tech 1
    # TR 12 = offense 5 (atk_mod +3) + durability 5 (end 10) + armor 2 (heavy)
    if tr <= 8:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            endurance_max=6,
            endurance_current=6,
            attack_modifier=2,
            defense_modifier=2,
            armor="light",
        )
    elif tr <= 10:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            endurance_max=8,
            endurance_current=8,
            attack_modifier=2,
            defense_modifier=2,
            armor="light",
        )
    else:
        return dict(
            name=f"Named NPC (TR {tr})",
            instance_id=f"named_tr{tr}",
            tier="named",
            endurance_max=10,
            endurance_current=10,
            attack_modifier=3,
            defense_modifier=2,
            armor="light",
        )


def generic_boss_def(tr: int = 12) -> dict:
    """Generic Boss at a target TR."""
    if tr <= 12:
        return dict(
            name=f"Boss (TR {tr})",
            instance_id=f"boss_tr{tr}",
            tier="boss",
            endurance_max=8,
            endurance_current=8,
            attack_modifier=2,
            defense_modifier=2,
            armor="light",
            has_phase_change=True,
            phase2_attack_mod=1,
            phase2_endurance=4,
            phase2_ignores_t1=True,
        )
    else:
        return dict(
            name=f"Boss (TR {tr})",
            instance_id=f"boss_tr{tr}",
            tier="boss",
            endurance_max=10,
            endurance_current=10,
            attack_modifier=3,
            defense_modifier=2,
            armor="heavy",
            has_phase_change=True,
            phase2_attack_mod=1,
            phase2_endurance=4,
            phase2_ignores_t1=True,
        )


def archive_guardian_def() -> dict:
    """Archive Guardian: Boss, TR 16, heavy armor, phase change."""
    return dict(
        name="Archive Guardian",
        instance_id="guardian",
        tier="boss",
        endurance_max=10,
        endurance_current=10,
        attack_modifier=3,
        defense_modifier=1,
        armor="heavy",
        has_phase_change=True,
        phase2_attack_mod=1,
        phase2_endurance=4,
        phase2_ignores_t1=True,
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
                        help="Run a specific series (A, B, C, D, E, F, or 'all')")
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
