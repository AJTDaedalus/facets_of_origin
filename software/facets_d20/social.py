"""Facets d20 social rules (facets_d20/06_Backgrounds_Sparks_and_Social.md, *Social Play*).

One function per rule; the chapter's Table 6–2 and Table 6–3 are tested against these.

    TRACK                 Hostile → Wary → Neutral → Friendly → Ally
    starting_attitude     a stranger starts Neutral; someone the party has crossed, Wary
                          (playtest fix pass, MM #6)
    case_dc               10 / 15 / 20 by how hard the person is to move
    result_steps          +2 (beat by 10), +1 (meet), 0 and the argument is spent (miss by
                          1–4), −1 (miss by 5 or more); Silver Tongue: +2 from beating by 5
    move                  one attitude moved along the track, clamped at the ends
    may_roll              one roll per character per person per scene (MM #6)
    after_threat          Intimidation moves someone toward Ally while the threat holds;
                          when it's gone they fall one step toward Hostile (MM #6)
    stops_fighting        a foe moved to Neutral or better in a fight stops, as if broken
"""
from __future__ import annotations

TRACK = ("hostile", "wary", "neutral", "friendly", "ally")
DCS = {"no_reason": 10, "reasons": 15, "good_reasons": 20}


def starting_attitude(*, crossed: bool = False) -> str:
    """Where a person starts before anyone rolls: Neutral, or Wary if the party has crossed
    them (or people like them). The MM can always start someone elsewhere for a reason."""
    return "wary" if crossed else "neutral"


def case_dc(how_hard: str) -> int:
    if how_hard not in DCS:
        raise KeyError(f"unknown difficulty {how_hard!r}; one of {sorted(DCS)}")
    return DCS[how_hard]


def result_steps(total: int, dc: int, *, silver_tongue: bool = False) -> int:
    """Table 6–3: attitude steps toward Ally (negative: toward Hostile)."""
    two = 5 if silver_tongue else 10
    if total >= dc + two:
        return 2
    if total >= dc:
        return 1
    if total >= dc - 4:
        return 0
    return -1


def argument_spent(total: int, dc: int) -> bool:
    """A miss by 1–4 changes nothing, and that argument won't work again this scene."""
    return dc - 4 <= total < dc


def move(attitude: str, steps: int) -> str:
    if attitude not in TRACK:
        raise KeyError(f"unknown attitude {attitude!r}")
    i = max(0, min(len(TRACK) - 1, TRACK.index(attitude) + steps))
    return TRACK[i]


def may_roll(character: str, person: str, rolled_this_scene: set) -> bool:
    """One roll per character per person per scene. ``rolled_this_scene`` holds the
    (character, person) pairs that have already rolled."""
    return (character, person) not in rolled_this_scene


def after_threat(attitude: str) -> str:
    """Intimidation works while the threat holds. Once it's gone, the person falls one
    step toward Hostile from wherever the threat left them."""
    return move(attitude, -1)


def stops_fighting(attitude: str) -> bool:
    """Influence in a fight: a foe moved to Neutral or better stops fighting, as if it had
    broken (Chapter 08)."""
    if attitude not in TRACK:
        raise KeyError(f"unknown attitude {attitude!r}")
    return TRACK.index(attitude) >= TRACK.index("neutral")
