"""Dice: expressions like ``2d6`` and the d20 roll with advantage/disadvantage.

Every roll goes through an RNG object exposing ``randint(a, b)`` (``random.Random`` or a
scripted stand-in in tests), so a seeded run is fully deterministic.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_DICE_RE = re.compile(r"^\s*(\d+)\s*d\s*(\d+)\s*$")


@dataclass(frozen=True)
class Dice:
    count: int
    sides: int

    def __post_init__(self):
        if self.count < 1 or self.sides < 2:
            raise ValueError(f"bad dice {self.count}d{self.sides}")

    @classmethod
    def parse(cls, text: str) -> "Dice":
        m = _DICE_RE.match(str(text))
        if not m:
            raise ValueError(f"not a dice expression: {text!r}")
        return cls(int(m.group(1)), int(m.group(2)))

    @property
    def average(self) -> float:
        return self.count * (self.sides + 1) / 2

    def times(self, k: int) -> "Dice":
        return Dice(self.count * k, self.sides)

    def __str__(self) -> str:
        return f"{self.count}d{self.sides}"


def roll(rng, d: Dice, *, min_face: int = 1) -> int:
    """Sum of the faces; faces below ``min_face`` count as ``min_face`` (Great Weapon)."""
    return sum(max(rng.randint(1, d.sides), min_face) for _ in range(d.count))


def mean_with_min_face(d: Dice, min_face: int = 1) -> float:
    per = sum(max(f, min_face) for f in range(1, d.sides + 1)) / d.sides
    return d.count * per


@dataclass(frozen=True)
class D20Roll:
    natural: int
    rolls: tuple


def d20(rng, *, advantage: bool = False, disadvantage: bool = False) -> D20Roll:
    """One d20 test. Advantage and disadvantage together cancel (one die)."""
    if advantage and not disadvantage:
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        return D20Roll(max(a, b), (a, b))
    if disadvantage and not advantage:
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        return D20Roll(min(a, b), (a, b))
    a = rng.randint(1, 20)
    return D20Roll(a, (a,))
