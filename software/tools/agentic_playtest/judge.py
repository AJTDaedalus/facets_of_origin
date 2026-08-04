"""Blind comparative judgement — the load-bearing instrument.

A fresh agent that took no part in either session is shown two transcripts with
every arm label stripped, and made to choose. It is the only measure here an
agreeable model cannot inflate: the output schema has no "both were good" option.

Order matters, so each pair is judged twice with the transcripts swapped. A
result that flips when the order flips is position bias, not a preference, and
the analysis must treat it as no signal.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field

JUDGE_MODEL = "claude-opus-5"

#: Anything that could reveal which arm a transcript came from.
_TELLS = (
    (re.compile(r"arm \*\*[AB]\*\*", re.I), "arm **?**"),
    (re.compile(r"\barm[ _-]?[AB]\b", re.I), "arm ?"),
    (re.compile(r"\[softened\]", re.I), ""),
    (re.compile(r"seed `?-?\d+`?", re.I), "seed `?`"),
    (re.compile(r"`[0-9a-f]{8}-[0-9a-f-]{27,}`"), "`?`"),  # session UUIDs
    (re.compile(r"^> Every mechanical line below.*$", re.M), ""),
)


def strip_tells(transcript: str) -> str:
    """Remove arm labels, seeds, session ids, and the softening marker.

    The softening marker is the important one: Arm B's variant shows up in the
    rendered transcript as `[softened]`, which would tell the judge exactly which
    condition it is looking at.
    """
    out = transcript
    for pattern, replacement in _TELLS:
        out = pattern.sub(replacement, out)
    return out


class Verdict(BaseModel):
    """A forced choice. There is deliberately no 'equal' option."""

    preferred: str = Field(
        description="Which table you would rather have played at. Must be "
                    "exactly 'first' or 'second'.")
    because: str = Field(
        description="The specific reason, referring to moments in the "
                    "transcripts rather than generalities.")
    opposition_felt_more_varied_in: str = Field(
        description="In which transcript did the opposition feel like it was "
                    "doing different things rather than repeating itself? "
                    "'first', 'second', or 'neither' if there was no fight.")
    most_boring_stretch: str = Field(
        description="Quote the dullest stretch across both transcripts and say "
                    "which one it came from.")


JUDGE_PROMPT = """\
You are reading two transcripts of the same tabletop roleplaying scenario, played
by different tables. You did not take part in either.

Read both, then answer. You must pick one — "both were good" and "they were
about the same" are not available, and an answer that avoids choosing is a
failed answer. If the two are close, pick the one you'd choose with a gun to your
head and say what tipped it.

Judge them as sessions you'd want to sit at: was anything happening, did the
people at the table seem engaged, did choices matter, was the opposition
interesting. Do not judge prose quality — these are play transcripts, not fiction.

--- TRANSCRIPT ONE ---
{first}

--- TRANSCRIPT TWO ---
{second}
"""


@dataclass
class PairedVerdict:
    """Both orderings of one pair."""

    forward: Verdict
    reversed: Verdict
    label_first: str
    label_second: str

    @property
    def winner(self) -> str | None:
        """The arm both orderings agreed on, or None if the order flipped it.

        A preference that reverses when the transcripts swap places is position
        bias. Returning None makes the analysis treat that pair as no signal
        rather than as evidence.
        """
        forward_pick = self.label_first if self.forward.preferred == "first" else self.label_second
        reverse_pick = self.label_second if self.reversed.preferred == "first" else self.label_first
        return forward_pick if forward_pick == reverse_pick else None

    def to_dict(self) -> dict:
        return {
            "label_first": self.label_first, "label_second": self.label_second,
            "forward": json.loads(self.forward.model_dump_json()),
            "reversed": json.loads(self.reversed.model_dump_json()),
            "winner": self.winner,
        }


def _ask(client: Any, first: str, second: str) -> Verdict:
    response = client.messages.parse(
        model=JUDGE_MODEL,
        max_tokens=2000,
        output_config={"effort": "high"},
        messages=[{"role": "user",
                   "content": JUDGE_PROMPT.format(first=first, second=second)}],
        output_format=Verdict,
    )
    return response.parsed_output


def compare(client: Any, transcript_a: str, transcript_b: str,
            label_a: str = "A", label_b: str = "B") -> PairedVerdict:
    """Judge a pair in both orders."""
    a = strip_tells(transcript_a)
    b = strip_tells(transcript_b)
    return PairedVerdict(
        forward=_ask(client, a, b),
        reversed=_ask(client, b, a),
        label_first=label_a,
        label_second=label_b,
    )


def tally(verdicts: list[PairedVerdict]) -> dict:
    """Count only the pairs where both orderings agreed."""
    counts: dict[str, int] = {}
    inconsistent = 0
    for verdict in verdicts:
        winner = verdict.winner
        if winner is None:
            inconsistent += 1
        else:
            counts[winner] = counts.get(winner, 0) + 1
    return {"agreed": counts, "order_dependent": inconsistent,
            "pairs": len(verdicts)}
