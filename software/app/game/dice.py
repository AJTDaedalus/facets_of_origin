"""Dice notation parser — converts 'NdS' strings to structured specs."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass

_DICE_RE = re.compile(r"^(\d+)d(\d+)$")


@dataclass
class DiceSpec:
    """A parsed dice formula: count dice with sides faces each."""

    count: int
    sides: int

    @classmethod
    def parse(cls, notation: str) -> DiceSpec:
        """Parse 'NdS' notation (e.g. '2d6', '1d20'). Raises ValueError on invalid."""
        m = _DICE_RE.match(notation.strip())
        if not m:
            raise ValueError(f"Invalid dice notation: {notation!r}. Expected format 'NdS' (e.g. '2d6').")
        count, sides = int(m.group(1)), int(m.group(2))
        if count < 1 or sides < 1:
            raise ValueError(f"Dice count and sides must be >= 1, got {count}d{sides}.")
        return cls(count=count, sides=sides)

    def roll(self) -> list[int]:
        """Roll count dice, each with sides faces. Returns list of individual results."""
        return [random.randint(1, self.sides) for _ in range(self.count)]
