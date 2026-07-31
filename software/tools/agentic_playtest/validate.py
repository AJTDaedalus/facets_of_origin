"""Validators. These are the point of the harness.

`find_confabulations` fails a run when an agent's free-text asserts a mechanic
the event log does not contain. Its regression test is a real line lifted from
`playtest/07_oraga_night_playtests/session_log_01.md` — the batch whose numbers
turned out to describe nothing.

`dice_distribution` is the batch-level check that would have caught the same
defect statistically: across ~60 confabulated dice there was not a single 1.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field

from tools.agentic_playtest.events import Event, EventLog

#: "2d6 (2, 3)", "3d6 (4,1,6)" — an explicit claim about what the dice showed.
_DICE_TUPLE = re.compile(r"\b(\d+)\s*d\s*6\s*\(\s*(\d(?:\s*,\s*\d)*)\s*\)", re.I)
#: "= 7", "total 11", "rolled a 9" — an explicit claim about a roll total.
_TOTAL = re.compile(r"(?:=\s*|\btotal(?:s|ed)?\s*(?:of\s*)?|\brolled\s+(?:an?\s+)?)(\d{1,2})\b", re.I)
#: The outcome tier labels from facet.yaml. An agent may never assert one.
_OUTCOME_LABELS = ("full success", "success with cost", "things go wrong",
                   "partial success")

#: Verbs whose result the agent may legitimately narrate in the same beat.
_MECHANICAL_KINDS = ("roll", "saving_throw", "cast", "strike", "react",
                     "enemy_attack", "enemy_resolve")


@dataclass
class Finding:
    seq: int
    beat: int
    actor: str
    claim: str
    kind: str
    excerpt: str

    def __str__(self) -> str:
        return (f"[beat {self.beat} seq {self.seq}] {self.actor} asserted "
                f"{self.kind} '{self.claim}' with no matching event: "
                f"\"{self.excerpt.strip()[:120]}\"")


@dataclass
class ValidationReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings

    def __str__(self) -> str:
        if self.ok:
            return "No confabulated mechanics found."
        head = f"{len(self.findings)} confabulated mechanic(s):"
        return "\n".join([head] + [f"  - {f}" for f in self.findings])


def _condition_ids(ruleset) -> set[str]:
    conds = ruleset.combat.conditions
    return {c.id for group in (conds.tier1, conds.tier2, conds.tier3) for c in group}


def _beat_facts(log: EventLog, beat: int) -> tuple[set[tuple[int, ...]], set[int], set[str], set[str]]:
    """Everything the engine actually produced in one beat.

    Returns (dice tuples, totals, outcome labels, condition ids).
    """
    dice: set[tuple[int, ...]] = set()
    totals: set[int] = set()
    labels: set[str] = set()
    conditions: set[str] = set()

    for event in log.in_beat(beat):
        if event.kind not in _MECHANICAL_KINDS:
            continue
        roll = event.data.get("roll")
        if roll:
            dice.add(tuple(roll["dice_rolled"]))
            totals.add(roll["total"])
            totals.add(roll["dice_sum"])
            labels.add(roll["outcome_label"].lower())
        if event.kind == "enemy_attack":
            for key in ("condition_applied", "condition_declared"):
                if event.data.get(key):
                    conditions.add(event.data[key])
        if event.kind == "enemy_resolve":
            for key in ("resolve", "resolve_before", "depletion"):
                if event.data.get(key) is not None:
                    totals.add(event.data[key])
    return dice, totals, labels, conditions


def find_confabulations(log: EventLog, ruleset) -> ValidationReport:
    """Fail the run if agent free-text claims a mechanic the log doesn't have.

    Scoped per beat: an agent narrating "an 8 — enough" right after the engine
    logged an 8 is fine. An agent writing "**Roll:** 2d6 (2, 3) + 2 = **7**"
    with no roll event in that beat is not.
    """
    report = ValidationReport()
    known_conditions = _condition_ids(ruleset)

    for event in log:
        if event.kind not in ("say", "say_ooc", "scene", "scene_ended", "rules_gap"):
            continue
        text = " ".join(str(v) for v in event.data.values())
        dice, totals, labels, conditions = _beat_facts(log, event.beat)

        for match in _DICE_TUPLE.finditer(text):
            claimed = tuple(int(x) for x in re.split(r"\s*,\s*", match.group(2)))
            if claimed not in dice:
                report.findings.append(Finding(
                    event.seq, event.beat, event.actor, match.group(0), "dice", text))

        for match in _TOTAL.finditer(text):
            value = int(match.group(1))
            # Only 2-12 style values are plausibly roll claims; larger numbers
            # are dates, counts, page references.
            if 2 <= value <= 24 and value not in totals:
                report.findings.append(Finding(
                    event.seq, event.beat, event.actor, match.group(0), "total", text))

        lowered = text.lower()
        for label in _OUTCOME_LABELS:
            if label in lowered and label not in labels:
                report.findings.append(Finding(
                    event.seq, event.beat, event.actor, label, "outcome", text))

        for condition in known_conditions:
            pretty = condition.replace("_", " ")
            if re.search(rf"\b{re.escape(pretty)}\b", lowered) and condition not in conditions:
                # A Condition named in prose with no enemy_attack event behind it
                # is the "You have the 'Watched' condition (Tier 1)" failure.
                if re.search(rf"\b{re.escape(pretty)}\b.{{0,40}}\bcondition\b", lowered) or \
                   re.search(rf"\bcondition\b.{{0,40}}\b{re.escape(pretty)}\b", lowered):
                    report.findings.append(Finding(
                        event.seq, event.beat, event.actor, condition, "condition", text))

    return report


# ---------------------------------------------------------------------------
# Batch-level dice distribution
# ---------------------------------------------------------------------------

@dataclass
class DiceReport:
    n: int
    face_counts: Counter
    chi_square: float
    degrees_of_freedom: int
    critical_value: float
    passed: bool
    note: str = ""

    def __str__(self) -> str:
        faces = " ".join(f"{f}:{self.face_counts.get(f, 0)}" for f in range(1, 7))
        verdict = "PASS" if self.passed else "FAIL"
        return (f"{verdict} — {self.n} d6 faces [{faces}] "
                f"χ²={self.chi_square:.2f} (df={self.degrees_of_freedom}, "
                f"crit={self.critical_value:.2f}){' — ' + self.note if self.note else ''}")


#: χ² critical values at p=0.01, df=5. A batch this far from uniform is not dice.
_CHI2_CRIT_DF5_P01 = 15.086


def dice_distribution(logs: list[EventLog], min_dice: int = 30) -> DiceReport:
    """Chi-square goodness-of-fit of every logged d6 face against uniform.

    Run across a batch, not a session — a single session has too few dice to
    separate bad luck from fabrication. The batch-07 corpus fails this badly:
    ~60 dice with zero 1s has a vanishing probability under a real d6.
    """
    faces: Counter = Counter()
    for log in logs:
        for event in log:
            roll = event.data.get("roll")
            if roll:
                faces.update(roll["dice_rolled"])

    n = sum(faces.values())
    if n < min_dice:
        return DiceReport(n, faces, 0.0, 5, _CHI2_CRIT_DF5_P01, True,
                          note=f"below {min_dice}-die minimum; not evaluated")

    expected = n / 6
    chi = sum((faces.get(f, 0) - expected) ** 2 / expected for f in range(1, 7))
    return DiceReport(n, faces, chi, 5, _CHI2_CRIT_DF5_P01,
                      passed=chi <= _CHI2_CRIT_DF5_P01)


def parse_dice_from_prose(text: str) -> list[int]:
    """Extract d6 faces from prose. Used to evaluate the legacy corpus."""
    faces: list[int] = []
    for match in _DICE_TUPLE.finditer(text):
        faces.extend(int(x) for x in re.split(r"\s*,\s*", match.group(2)))
    return faces
