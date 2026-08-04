"""Post-session debrief — forced-choice and forced-negative only.

Never "rate this 1-10". Agreeable models cluster every absolute rating at the top
regardless of what happened, so an absolute scale measures nothing. Every
question here either forces a comparison, forces a criticism, or asks for a quote
the transcript can be checked against.

`tests/test_agentic_playtest.py` asserts the schema contains no absolute rating
field, so one cannot be added back without the test failing.
"""
from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field

MODEL = "claude-opus-5"


class PlayerDebrief(BaseModel):
    """What one player says afterwards, out of character."""

    best_moment: str = Field(
        description="The single moment you'd tell someone else about. Quote or "
                    "describe it specifically.")
    worst_moment: str = Field(
        description="The single moment you would cut from the session. You must "
                    "name one — 'nothing' is not an answer.")
    scenes_ranked_best_to_worst: list[str] = Field(
        description="Every scene of the session, ordered best to worst. Ties are "
                    "not allowed; pick an order.")
    moment_i_did_not_know_my_options: str = Field(
        description="A point where you were unsure what you were allowed to do, "
                    "or how a rule worked. Quote the moment. Write 'none' only if "
                    "there genuinely was not one.")
    one_rule_change: str = Field(
        description="You get exactly one change to the rules. What is it, and "
                    "what did it cost you tonight?")
    best_moment_by_another_player: str = Field(
        description="Which other player had the best moment, and what was it?")
    who_had_the_worst_session: str = Field(
        description="Which player (possibly you) got the least out of tonight, "
                    "and why?")
    did_the_enemies_feel_varied: str = Field(
        description="Did the opposition feel like it was doing different things "
                    "over the course of the fight, or the same thing repeatedly? "
                    "Answer only if there was a fight; otherwise write 'no fight'.")
    would_play_session_two: bool = Field(
        description="Would you come back next week for session two?")
    would_play_session_two_because: str = Field(
        description="The honest reason for that answer, in one sentence.")


DEBRIEF_PROMPT = """\
The session has ended. Step fully out of character and answer as the player, not
as the character you were playing.

Be candid and specific. This is a playtest — the point is to find what did not
work, and a debrief where everything was great is a debrief that tells the
designers nothing. Where a question asks for a negative, you must give one.

Quote actual moments from tonight rather than describing them in general terms.
"""


def collect(client: Any, agent: Any) -> PlayerDebrief:
    """Ask one player agent for its debrief, in its own session context."""
    agent.observe(DEBRIEF_PROMPT)
    response = client.messages.parse(
        model=MODEL,
        max_tokens=3000,
        system=agent.context.system_blocks(),
        messages=agent.messages,
        output_format=PlayerDebrief,
    )
    agent.usage.add(response.usage)
    return response.parsed_output


def to_dict(debrief: PlayerDebrief) -> dict:
    return json.loads(debrief.model_dump_json())
