"""Monsters: the SRD 5.2.1 ladder as data, converted per the MM guide (09, Table 9–2).

``LIBRARY`` is loaded from ``facets_d20/data/srd_monsters.yaml``, generated from the SRD
5.2 creature data by ``software/tools/build_srd_monsters.py`` (61 monsters, CR 1/8–12,
two to five per CR; AC, HP, saves, to-hit and the SRD's printed average damage).
A few engine-only blocks (``source="engine"``) are added for examples in the book
(the alley leader of 08) and tests.

Conversion (``convert``) applies the MM guide: a **minion** has 1 HP, a **boss** takes
two turns, "never" foes don't break. ``template(cr)`` is a generic foe for a CR: the
median AC/HP/to-hit/damage of the ladder's monsters at that CR (engine-derived from
SRD data, not SRD text).
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Optional

import yaml

from .combat import Combatant, MonsterAttack
from .dice import Dice

ROLES = ("minion", "standard", "boss")
LADDER_FILE = Path(__file__).resolve().parent / "data" / "srd_monsters.yaml"


@dataclass(frozen=True)
class MonsterBlock:
    id: str
    name: str
    cr: Fraction
    ac: int
    hp: int
    attacks: tuple
    saves: dict
    morale: str = "normal"
    special: Optional[MonsterAttack] = None   # a recharge ability (breath)
    resist: frozenset = frozenset()
    source: str = "srd-5.2.1"
    note: str = ""
    traits: frozenset = frozenset()
    ctype: str = "monstrosity"

    @property
    def damage_per_turn(self) -> int:
        """Everything it does on an ordinary turn if it all hits (09 "What counts")."""
        return sum(a.fixed * a.count for a in self.attacks)

    @property
    def to_hit(self) -> int:
        return max(a.to_hit for a in self.attacks) if self.attacks else 0

    @property
    def dex_mod(self) -> int:
        return self.saves.get("dex", 0)


def _cr(x) -> Fraction:
    return Fraction(x).limit_denominator(8)


def _load_ladder(path: Path = LADDER_FILE) -> dict:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = {}
    for m in raw["monsters"]:
        attacks = tuple(
            MonsterAttack(name=a["name"], to_hit=int(a["to_hit"]), fixed=int(a["fixed"]),
                          dice=Dice.parse(a["dice"]), mod=int(a["mod"]),
                          dtype=a.get("dtype") or "bludgeoning", count=int(a["count"]),
                          extra=tuple(Dice.parse(x) for x in a.get("extra_dice") or ()))
            for a in m["attacks"])
        sp = m.get("special")
        special = None
        if sp:
            special = MonsterAttack(name=sp["name"], to_hit=0, fixed=int(sp["fixed"]),
                                    dice=Dice.parse(sp["dice"]), dtype=sp["dtype"],
                                    save_dc=int(sp["dc"]), save_ability=sp["save"],
                                    half_on_save=bool(sp["half_on_success"]),
                                    targets=int(sp["targets"]),
                                    recharge_min=int(sp["recharge_min"]))
        traits = frozenset("undead_fortitude" for t in m.get("traits") or []
                           if t == "Undead Fortitude")
        out[m["id"]] = MonsterBlock(m["id"], m["name"], _cr(m["cr"]), int(m["ac"]), int(m["hp"]),
                                    attacks, dict(m["saves"]), m["morale"], special,
                                    frozenset(m.get("resist") or ()), "srd-5.2.1", "",
                                    traits, m["type"])
    return out


def _atk(name, to_hit, fixed, dice=None, mod=0, dtype="slashing", count=1):
    return MonsterAttack(name=name, to_hit=to_hit, fixed=fixed,
                         dice=Dice.parse(dice) if dice else None, mod=mod,
                         dtype=dtype, count=count)


def _saves(dex, con, wis, str_=0, int_=0, cha=0):
    return {"str": str_, "dex": dex, "con": con, "int": int_, "wis": wis, "cha": cha}


LIBRARY: dict = _load_ladder()
LIBRARY.update({m.id: m for m in [
    MonsterBlock("bandit_leader", "Bandit Leader", Fraction(1, 2), 13, 22,
                 (_atk("Longsword", 4, 6, "1d8", 2),), _saves(1, 1, 0),
                 source="engine", note="08's alley leader: AC 13, 22 HP, +4, 6.",
                 ctype="humanoid"),
    MonsterBlock("brute", "Brute", Fraction(1, 2), 13, 30,
                 (_atk("Greataxe", 5, 9, "1d12", 3),), _saves(1, 3, 0),
                 source="engine", note="Generic orc-like brute; not an SRD block.",
                 ctype="humanoid"),
]})


def get(mid: str) -> MonsterBlock:
    if mid not in LIBRARY:
        raise KeyError(f"unknown monster {mid!r}")
    return LIBRARY[mid]


def ladder(cr=None) -> list:
    """The SRD ladder (optionally one CR), sorted by CR then name."""
    ms = [m for m in LIBRARY.values() if m.source == "srd-5.2.1"]
    if cr is not None:
        ms = [m for m in ms if m.cr == _cr(cr)]
    return sorted(ms, key=lambda m: (m.cr, m.name))


# ---------------------------------------------------------------- generic templates

TEMPLATE_CRS = tuple(sorted({m.cr for m in ladder()}))


def template(cr) -> MonsterBlock:
    """A generic foe for a CR: the ladder's medians at that CR (engine-derived)."""
    key = _cr(cr)
    ms = ladder(key)
    if not ms:
        raise KeyError(f"no template for CR {cr}")
    ac = round(statistics.median(m.ac for m in ms))
    hp = round(statistics.median(m.hp for m in ms))
    to_hit = round(statistics.median(m.to_hit for m in ms))
    dpt = round(statistics.median(m.damage_per_turn for m in ms))
    n = round(statistics.median(sum(a.count for a in m.attacks) for m in ms))
    per, extra = divmod(dpt, n)
    attacks = [MonsterAttack("Strike", to_hit, per + extra, None, 0, "bludgeoning", 1)]
    if n > 1:
        attacks.append(MonsterAttack("Strike", to_hit, per, None, 0, "bludgeoning", n - 1))
    saves = {a: round(statistics.median(m.saves.get(a, 0) for m in ms))
             for a in ("str", "dex", "con", "int", "wis", "cha")}
    return MonsterBlock(f"cr_{str(key).replace('/', '_')}", f"CR {key} foe", key, ac, hp,
                        tuple(attacks), saves, source="engine")


# ---------------------------------------------------------------- conversion (Table 9–2)


def convert(block, *, role: str = "standard", uid: Optional[str] = None,
            leader: bool = False, hp_multiplier: int = 1) -> Combatant:
    """A MonsterBlock (or library id) as a Combatant in the given role. ``hp_multiplier``
    applies to a boss only (MM rule, balance pass V37: a boss has twice its stat block's
    hit points — ``RuleOptions.boss_hp_multiplier``)."""
    if isinstance(block, str):
        block = get(block)
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}, not {role!r}")
    hp = 1 if role == "minion" else block.hp * (hp_multiplier if role == "boss" else 1)
    traits = set(block.traits)
    if role == "minion":
        traits.discard("undead_fortitude")  # 09: a minion doesn't get to cling on
    c = Combatant(id=uid or block.id, name=block.name, side="enemy", max_hp=hp, ac=block.ac,
                  role=role, saves=dict(block.saves), dex_mod=block.dex_mod,
                  morale=block.morale, leader=leader, resist=set(block.resist),
                  attacks=list(block.attacks), tags=traits | {f"type:{block.ctype}"})
    c.block = block  # type: ignore[attr-defined]
    c.special = block.special  # type: ignore[attr-defined]
    c.special_ready = block.special is not None  # type: ignore[attr-defined]
    return c


def budget_hp(c: Combatant, *, party_level: int) -> int:
    """v0.1 09 "What counts": minion 7 (L1–4) / 10 (L5–10); never-breaks HP × 1.25."""
    base = (7 if party_level <= 4 else 10) if c.role == "minion" else c.max_hp
    return int(base * 1.25) if c.morale == "never" else base


def budget_damage(c: Combatant) -> int:
    """v0.1 09 "What counts": ordinary-turn damage if all hits; a boss counts twice."""
    dpt = sum(a.fixed * a.count for a in c.attacks)
    return dpt * (2 if c.role == "boss" else 1)
