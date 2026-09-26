"""The MM toolbox (MM6, DESIGN §3.2 and §4.1): table rolls, the reaction roll,
the Pressure die, the oracle and the "Stuck?" helper.

All tables come from `tables.yaml` via the ruleset (`ruleset.tables`). Every
function accepts `roll=` (a fixed die result) or `rng=` so results replay.
"""
from __future__ import annotations

import random
from typing import Optional

from app.facets.schema import die_faces

#: Odds work as difficulty (MM6): likely +1, even 0, unlikely −1, very unlikely −2.
ORACLE_ODDS = {"likely": 1, "even": 0, "unlikely": -1, "very_unlikely": -2}
PRESSURE_VARIANTS = ("generic", "underground", "wild", "settlement", "occasion")


def roll_die(die: str, rng: Optional[random.Random] = None) -> int:
    """One result of a table die: 1d6, 1d8, 1d12, 1d20, 2d6 or d66 (tens then units)."""
    r = rng or random
    if die == "d66":
        return r.randint(1, 6) * 10 + r.randint(1, 6)
    if die == "2d6":
        return r.randint(1, 6) + r.randint(1, 6)
    faces = die_faces(die)          # raises on an unknown die
    return r.randint(1, len(faces))


def _table(ruleset, table_id: str):
    table = ruleset.get_table(table_id)
    if table is None:
        raise KeyError(f"No table {table_id!r} is loaded (tables.yaml).")
    return table


def roll_table(ruleset, table_id: str, *, roll: Optional[int] = None,
               rng: Optional[random.Random] = None) -> dict:
    """Roll (or read, with `roll=`) one table. Returns {table, name, die, roll, text}.

    Raises:
        KeyError: no such table loaded.
        ValueError: a fixed `roll` that is not a result of the table's die.
    """
    table = _table(ruleset, table_id)
    face = roll if roll is not None else roll_die(table.die, rng)
    if face not in die_faces(table.die):
        raise ValueError(f"{face} is not a result of {table.die}.")
    entry = table.lookup(face)
    return {"table": table.id, "name": table.name, "die": table.die, "roll": face,
            "entry_roll": entry.roll, "text": entry.text}


def roll_distinct(ruleset, table_id: str, n: int, rng: Optional[random.Random] = None) -> list[dict]:
    """`n` different entries from one table (e.g. two costs to choose between)."""
    table = _table(ruleset, table_id)
    if n > len(table.entries):
        raise ValueError(f"{table_id} has only {len(table.entries)} entries.")
    out: list[dict] = []
    seen: set[str] = set()
    tries = 0
    while len(out) < n:
        res = roll_table(ruleset, table_id, rng=rng)
        tries += 1
        if res["entry_roll"] in seen and tries < 200:
            continue
        seen.add(res["entry_roll"])
        out.append(res)
    return out


def reaction_roll(ruleset, *, modifier: int = 0, dice: Optional[list[int]] = None,
                  rng: Optional[random.Random] = None) -> dict:
    """2d6 (+modifier, clamped to the table) on the reaction table."""
    tid = ruleset.exploration.reaction_roll.table
    table = _table(ruleset, tid)
    if dice is not None:
        if len(dice) != 2 or any(not 1 <= d <= 6 for d in dice):
            raise ValueError("A reaction roll is two d6.")
        rolled = list(dice)
    else:
        r = rng or random
        rolled = [r.randint(1, 6), r.randint(1, 6)]
    faces = die_faces(table.die)
    total = max(faces[0], min(faces[-1], sum(rolled) + modifier))
    res = roll_table(ruleset, tid, roll=total)
    res.update({"dice": rolled, "modifier": modifier, "total": total})
    return res


def pressure_roll(ruleset, variant: str = "generic", *, roll: Optional[int] = None,
                  rng: Optional[random.Random] = None) -> dict:
    """The Pressure die, on the generic table or a terrain variant."""
    if variant not in PRESSURE_VARIANTS:
        raise ValueError(f"Unknown Pressure variant {variant!r}; one of {PRESSURE_VARIANTS}.")
    return roll_table(ruleset, f"pressure_{variant}", roll=roll, rng=rng)


def oracle(ruleset, odds: str = "even", *, dice: Optional[list[int]] = None,
           rng: Optional[random.Random] = None, prompts: bool = True) -> dict:
    """Ask the oracle a yes/no question: 2d6 ± odds. 10+ yes · 7-9 yes, but ·
    6- no; a natural 12 is "yes, and", a natural 2 "no, and".

    With `prompts`, adds a verb (`oracle_actions`) and a theme (`oracle_themes`)
    to colour the answer.
    """
    if odds not in ORACLE_ODDS:
        raise ValueError(f"Unknown odds {odds!r}; one of {list(ORACLE_ODDS)}.")
    if dice is not None:
        if len(dice) != 2 or any(not 1 <= d <= 6 for d in dice):
            raise ValueError("The oracle rolls two d6.")
        rolled = list(dice)
    else:
        r = rng or random
        rolled = [r.randint(1, 6), r.randint(1, 6)]
    total = sum(rolled) + ORACLE_ODDS[odds]
    th = ruleset.roll_resolution.thresholds
    if rolled == [6, 6]:
        answer, tier = "Yes, and…", "full_success"
    elif rolled == [1, 1]:
        answer, tier = "No, and…", "failure"
    elif total >= th.full_success:
        answer, tier = "Yes", "full_success"
    elif total >= th.partial_success:
        answer, tier = "Yes, but…", "partial_success"
    else:
        answer, tier = "No", "failure"
    out = {"odds": odds, "dice": rolled, "total": total, "tier": tier, "answer": answer,
           "natural": "high" if rolled == [6, 6] else "low" if rolled == [1, 1] else None,
           "action": None, "theme": None}
    if prompts:
        for key, tid in (("action", "oracle_actions"), ("theme", "oracle_themes")):
            if ruleset.get_table(tid):
                out[key] = roll_table(ruleset, tid, rng=rng)["text"]
    return out


def roll_hoard(ruleset, site_level: int, *, rng: Optional[random.Random] = None,
               coin_dice: Optional[list[int]] = None, relic_die: Optional[int] = None) -> dict:
    """A hoard (MM3/MM6): 2d6 × 10 × site level coin, one curio, a relic if a
    d6 shows 6, and a trinket for colour."""
    if not 1 <= site_level <= ruleset.advancement.max_level:
        raise ValueError(f"Site level must be 1-{ruleset.advancement.max_level}.")
    r = rng or random
    dice = list(coin_dice) if coin_dice is not None else [r.randint(1, 6), r.randint(1, 6)]
    if len(dice) != 2 or any(not 1 <= d <= 6 for d in dice):
        raise ValueError("Hoard coin is two d6.")
    d6 = relic_die if relic_die is not None else r.randint(1, 6)
    if not 1 <= d6 <= 6:
        raise ValueError("The relic die is a d6.")
    out = {"site_level": site_level, "coin_dice": dice, "coin": sum(dice) * 10 * site_level,
           "curio": None, "relic_die": d6, "relic": None, "trinket": None}
    if ruleset.get_table("trinkets"):
        out["trinket"] = roll_table(ruleset, "trinkets", rng=rng)
    if ruleset.get_table("curios"):
        out["curio"] = roll_table(ruleset, "curios", rng=rng)
    if d6 == 6 and ruleset.get_table("relics"):
        out["relic"] = roll_table(ruleset, "relics", rng=rng)
    return out


def stuck_helper(ruleset, rng: Optional[random.Random] = None,
                 clock: Optional[str] = None) -> list[dict]:
    """"Stuck?" (MM2, MM6) — three ways forward for the MM:

    1. a threat moves: tick a Threat Clock (`clock`, if one is named);
    2. someone arrives with a want: a name, a want and a reaction roll;
    3. a secret surfaces: from the prep list, or an NPC secret.

    Tables that are not loaded fall back to a setting-neutral prompt.
    """
    threat = {"kind": "threat", "table": None,
              "text": (f"A threat moves: tick the {clock} clock." if clock
                       else "A threat moves: tick a Threat Clock.")}
    if ruleset.get_table("trouble"):
        threat["detail"] = roll_table(ruleset, "trouble", rng=rng)["text"]
        threat["table"] = "trouble"

    arrival = {"kind": "arrival", "table": None,
               "text": "Someone arrives who wants something from the party."}
    if ruleset.get_table("npc_names") and ruleset.get_table("npc_wants"):
        name = roll_table(ruleset, "npc_names", rng=rng)["text"]
        want = roll_table(ruleset, "npc_wants", rng=rng)["text"]
        arrival.update({"table": "npc_names+npc_wants",
                        "text": f"{name} arrives, wanting: {want}"})
        if ruleset.get_table(ruleset.exploration.reaction_roll.table):
            arrival["reaction"] = reaction_roll(ruleset, rng=rng)["text"]

    secret = {"kind": "secret", "table": None,
              "text": "A secret surfaces: reveal one from your prep list."}
    if ruleset.get_table("npc_secrets"):
        secret.update({"table": "npc_secrets",
                       "detail": roll_table(ruleset, "npc_secrets", rng=rng)["text"]})
    return [threat, arrival, secret]
