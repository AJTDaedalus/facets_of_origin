"""Dice notation parser — converts 'NdS' strings to structured specs."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass

# The trailing modifier group exists for the MM's table roller, where an MM
# types whatever a random table asks for ("1d20+3"). It is optional, so plain
# 'NdS' — which is what the resolution engine and combat module pass — parses
# exactly as before, with a modifier of 0.
_DICE_RE = re.compile(r"^(\d+)\s*d\s*(\d+)(?:\s*([+-])\s*(\d+))?$")


@dataclass
class DiceSpec:
    """A parsed dice formula: count dice with sides faces each, plus a flat modifier."""

    count: int
    sides: int
    modifier: int = 0

    @classmethod
    def parse(cls, notation: str) -> DiceSpec:
        """Parse 'NdS' or 'NdS+M' / 'NdS-M' (e.g. '2d6', '1d20+3').

        Raises ValueError on anything else.
        """
        m = _DICE_RE.match(notation.strip())
        if not m:
            raise ValueError(
                f"Invalid dice notation: {notation!r}. "
                "Expected 'NdS' or 'NdS+M' (e.g. '2d6', '1d20+3')."
            )
        count, sides = int(m.group(1)), int(m.group(2))
        if count < 1 or sides < 1:
            raise ValueError(f"Dice count and sides must be >= 1, got {count}d{sides}.")

        modifier = 0
        if m.group(3):
            modifier = int(m.group(4)) * (-1 if m.group(3) == "-" else 1)
        return cls(count=count, sides=sides, modifier=modifier)

    def roll(self) -> list[int]:
        """Roll count dice, each with sides faces. Returns list of individual results."""
        return [random.randint(1, self.sides) for _ in range(self.count)]

    def total(self, dice: list[int]) -> int:
        """Sum of the rolled dice plus this spec's flat modifier."""
        return sum(dice) + self.modifier
