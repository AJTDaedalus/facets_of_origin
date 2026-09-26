"""Core roll resolution (PHB III.1, DESIGN §1).

    2d6 + stat (+ knack, + talent bonus; together capped at +4) + difficulty.
    Extra dice (Sparks, Help, Borrowed Trouble) each add a d6; keep the best two.
    10+ full success · 7-9 success with a cost · 6- things go wrong.
    Naturals are read on the kept dice: 6+6 is a full success whatever the
    modifiers; 1+1 on a failed roll confirms the Graceful Fail.

Every number comes from `ruleset.roll_resolution`. Pass `dice=[...]` to fix the
dice for tests or replays (it must hold exactly 2 + extra dice values).
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field
from typing import Optional, Sequence

from app.game.dice import DiceSpec


@dataclass
class RollResult:
    """Everything a client needs to show a roll."""

    dice: list[int]                 # every die rolled
    kept: list[int]                 # the best two
    stat: Optional[str]
    stat_value: int
    knack: bool
    bonus: int                      # talent / situational bonus requested
    modifier: int                   # stat + knack + bonus after the cap
    capped: bool                    # True if the cap cut the modifier
    difficulty: str
    difficulty_modifier: int
    total: int
    outcome: str                    # full_success | partial_success | failure
    outcome_label: str
    natural_high: bool              # kept 6+6
    natural_low: bool               # kept 1+1
    graceful_fail_auto: bool        # natural_low on a failure
    sparks: int = 0
    help: int = 0
    borrowed_trouble: bool = False
    kind: str = "roll"              # roll | avoid | attack | cast | hold_on | ...
    description: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return self.outcome != "failure"


def roll_d6s(n: int, rng: Optional[random.Random] = None) -> list[int]:
    r = rng or random
    return [r.randint(1, 6) for _ in range(n)]


def roll_expr(expr: str, rng: Optional[random.Random] = None,
              fixed: Optional[Sequence[int]] = None) -> tuple[list[int], int]:
    """Roll a dice expression like '1d8' or '2d8+1'. Returns (dice, total).

    `fixed` supplies the dice values instead of rolling (must match the count).
    """
    spec = DiceSpec.parse(expr)
    if fixed is not None:
        dice = list(fixed)
        if len(dice) != spec.count or any(not 1 <= d <= spec.sides for d in dice):
            raise ValueError(f"fixed dice {dice} do not fit {expr}")
    else:
        r = rng or random
        dice = [r.randint(1, spec.sides) for _ in range(spec.count)]
    return dice, spec.total(dice)


def outcome_for_total(ruleset, total: int) -> str:
    th = ruleset.roll_resolution.thresholds
    if total >= th.full_success:
        return "full_success"
    if total >= th.partial_success:
        return "partial_success"
    return "failure"


def outcome_label(ruleset, outcome: str) -> str:
    rr = ruleset.roll_resolution
    if outcome in rr.outcomes:
        return rr.outcomes[outcome].label
    for tier in rr.outcome_tiers:
        if tier.id == outcome:
            return tier.label
    return outcome


def capped_modifier(ruleset, stat_value: int, knack: bool, bonus: int) -> tuple[int, bool]:
    """stat + knack + bonus, never above the cap (+4). Returns (modifier, was_capped)."""
    rr = ruleset.roll_resolution
    raw = stat_value + (rr.knack_bonus if knack else 0) + bonus
    if raw > rr.bonus_cap:
        return rr.bonus_cap, True
    return raw, False


def resolve_roll(
    ruleset,
    *,
    stat_value: int,
    stat: Optional[str] = None,
    knack: bool = False,
    bonus: int = 0,
    difficulty: str = "Standard",
    sparks: int = 0,
    help: int = 0,
    borrowed_trouble: bool = False,
    extra_dice: int = 0,
    dice: Optional[Sequence[int]] = None,
    rng: Optional[random.Random] = None,
    kind: str = "roll",
    description: str = "",
) -> RollResult:
    """Resolve one 2d6 roll.

    Args:
        stat_value: the stat's value (-1..+3 in practice).
        knack: True if one of the roller's knacks applies (+1; never stacks).
        bonus: any talent/situational bonus (counts toward the +4 cap).
        difficulty: a label from `roll_resolution.difficulty_modifiers`.
        sparks: Sparks spent (each adds a d6). The caller debits the character.
        help: 0 or 1 (an ally's Help; max per roll from the ruleset).
        borrowed_trouble: accept a complication for an extra die (max one).
        extra_dice: other sources of extra dice (Inspiring, exposure ...).
        dice: fixed dice values (len == 2 + all extra dice).

    Raises:
        ValueError: negative counts, too much Help / Borrowed Trouble, an
            unknown difficulty, or `dice` of the wrong length/range.
    """
    rr = ruleset.roll_resolution
    if sparks < 0 or help < 0 or extra_dice < 0:
        raise ValueError("Sparks, Help and extra dice cannot be negative.")
    if help > rr.help.max_per_roll:
        raise ValueError(f"At most {rr.help.max_per_roll} Help per roll.")
    if borrowed_trouble and rr.borrowed_trouble.max_per_roll < 1:
        raise ValueError("Borrowed Trouble is not allowed.")
    diff_mod = rr.get_difficulty_modifier(difficulty)

    n_extra = (sparks + help * rr.help.extra_dice
               + (rr.borrowed_trouble.extra_dice if borrowed_trouble else 0) + extra_dice)
    n = 2 + n_extra
    if dice is not None:
        rolled = list(dice)
        if len(rolled) != n or any(not 1 <= d <= 6 for d in rolled):
            raise ValueError(f"Expected {n} d6 values, got {rolled}.")
    else:
        rolled = roll_d6s(n, rng)
    kept = sorted(rolled, reverse=True)[:2]

    modifier, capped = capped_modifier(ruleset, stat_value, knack, bonus)
    total = sum(kept) + modifier + diff_mod
    outcome = outcome_for_total(ruleset, total)
    natural_high = kept == [6, 6]
    natural_low = kept == [1, 1]
    if natural_high:
        outcome = "full_success"
    graceful = natural_low and outcome == "failure"

    return RollResult(
        dice=rolled, kept=kept, stat=stat, stat_value=stat_value, knack=knack,
        bonus=bonus, modifier=modifier, capped=capped, difficulty=difficulty,
        difficulty_modifier=diff_mod, total=total, outcome=outcome,
        outcome_label=outcome_label(ruleset, outcome), natural_high=natural_high,
        natural_low=natural_low, graceful_fail_auto=graceful, sparks=sparks,
        help=help, borrowed_trouble=borrowed_trouble, kind=kind,
        description=description,
    )


def resolve_avoid(ruleset, *, stat_value: int, stat: Optional[str] = None,
                  difficulty: Optional[str] = None, knack: bool = False, sparks: int = 0,
                  help: int = 0, borrowed_trouble: bool = False,
                  dice: Optional[Sequence[int]] = None,
                  rng: Optional[random.Random] = None, description: str = "") -> RollResult:
    """The avoid roll (the old saving throw): 2d6 + the stat that fits.

    The result's `extra["text"]` carries the ruleset's line for the tier
    (avoid it entirely / the worst of it / it takes hold).
    """
    av = ruleset.roll_resolution.avoid
    result = resolve_roll(
        ruleset, stat_value=stat_value, stat=stat, knack=knack,
        difficulty=difficulty or av.default_difficulty, sparks=sparks, help=help,
        borrowed_trouble=borrowed_trouble, dice=dice, rng=rng, kind="avoid",
        description=description)
    result.extra["text"] = av.outcomes.get(result.outcome, "")
    return result


def roll_character(ruleset, character, stat: str, **kwargs) -> RollResult:
    """Resolve a roll for a character: reads the stat, debits Sparks.

    Raises:
        ValueError: unknown stat, or more Sparks than the character holds.
    """
    if stat not in character.stats:
        raise ValueError(f"Unknown stat {stat!r}.")
    sparks = kwargs.get("sparks", 0)
    if sparks > character.sparks:
        raise ValueError(f"{character.name} has only {character.sparks} Sparks.")
    result = resolve_roll(ruleset, stat_value=character.stats[stat], stat=stat, **kwargs)
    if sparks:
        character.sparks -= sparks
    return result


def roll_result_to_dict(result: RollResult) -> dict:
    """JSON-safe dict of a roll (for WebSocket/REST payloads and the roll log)."""
    d = asdict(result)
    d["succeeded"] = result.succeeded
    return d
