"""Combat effects of spells, read from ``facets_d20_spells.yaml`` → ``sim_spells``.

The yaml is the single source (DESIGN v0.2 §1.6/§1.4a, E-1). This module turns each
entry into a ``SpellEffect`` and answers "how many dice at this slot / character level".
A spell a character can cast that has no ``sim_spells`` entry is never cast by the
simulator (utility and out-of-combat spells).

Models: attack, save (single or area by ``targets``), auto (Magic Missile), heal, aura
(concentration; ticks once a round on up to ``targets`` foes), weapon_rider (smites,
Hunter's Mark with ``per_hit``), weapon_cantrip (True Strike, Shillelagh), disable,
shield, buff_attack (Bless), ac_set (Mage Armor), ac_bonus (Shield of Faith).
``sustain: bonus|action`` — a concentration spell whose effect repeats each turn for that
action while it lasts (Spiritual Weapon, Flaming Sphere, Call Lightning).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .dice import Dice

MODELS = {"attack", "save", "area_save_damage", "auto", "heal", "aura", "weapon_rider",
          "weapon_cantrip", "disable", "shield", "buff_attack", "ac_set", "ac_bonus"}


def parse_dice(text) -> tuple:
    """``"2d10+4d6"`` → (Dice(2,10), Dice(4,6)); ``None`` → ()."""
    if not text:
        return ()
    return tuple(Dice.parse(t) for t in str(text).replace(" ", "").split("+"))


def add_dice(groups: tuple, extra: tuple, times: int = 1) -> tuple:
    out = list(groups)
    for e in extra:
        for _ in range(times):
            for i, g in enumerate(out):
                if g.sides == e.sides:
                    out[i] = Dice(g.count + e.count, g.sides)
                    break
            else:
                out.append(e)
    return tuple(out)


def average(groups: tuple) -> float:
    return sum(g.average for g in groups)


@dataclass(frozen=True)
class SpellEffect:
    name: str
    level: int
    model: str
    dice: tuple = ()
    upcast: tuple = ()
    add_mod: bool = False
    plus: int = 0
    save: Optional[str] = None
    half_on_save: bool = True
    targets: int = 1
    concentration: bool = False
    action: str = "action"          # action | bonus | reaction
    sustain: Optional[str] = None   # bonus | action
    beams: int = 1
    beams_upcast: int = 0
    beams_by_level: tuple = ()      # ((char level, beams), ...)
    scale_cantrip: bool = False
    extra_by_level: tuple = ()      # True Strike: ((5, "1d6"),)
    weapon_die_by_level: tuple = () # Shillelagh
    per_hit: bool = False
    melee: bool = False
    repeat_save: bool = True
    ends_on_damage: bool = False
    creature_types: tuple = ()
    precast: bool = False
    value: int = 0                  # ac_bonus
    base: int = 0                   # ac_set
    dtype: str = "force"
    raw: dict = field(default_factory=dict, compare=False, hash=False)

    @property
    def kind(self) -> str:
        return "save" if self.model == "area_save_damage" else self.model

    @property
    def area(self) -> bool:
        return self.targets >= 2


def from_entry(e: dict) -> SpellEffect:
    model = e["model"]
    if model not in MODELS:
        raise ValueError(f"sim_spells {e.get('name')!r}: unknown model {model!r}")
    action = e.get("action") or ("bonus" if e.get("bonus_action") else
                                 "reaction" if model == "shield" else "action")
    return SpellEffect(
        name=e["name"], level=int(e.get("level", 0)), model=model,
        dice=parse_dice(e.get("dice")), upcast=parse_dice(e.get("upcast")),
        add_mod=bool(e.get("add_mod")), plus=int(e.get("plus", 0)), save=e.get("save"),
        half_on_save=bool(e.get("half_on_success", True)), targets=int(e.get("targets", 1)),
        concentration=bool(e.get("concentration")), action=action, sustain=e.get("sustain"),
        beams=int(e.get("beams", 1)), beams_upcast=int(e.get("beams_upcast", 0)),
        beams_by_level=tuple(sorted((int(k), int(v)) for k, v in
                                    (e.get("beams_by_level") or {}).items())),
        scale_cantrip=e.get("scale") == "cantrip",
        extra_by_level=tuple(sorted((int(k), str(v)) for k, v in
                                    (e.get("extra_by_level") or {}).items())),
        weapon_die_by_level=tuple(sorted((int(k), str(v)) for k, v in
                                         (e.get("weapon_die_by_level") or {}).items())),
        per_hit=bool(e.get("per_hit")), melee=bool(e.get("melee")),
        repeat_save=bool(e.get("repeat_save", True)),
        ends_on_damage=bool(e.get("ends_on_damage")),
        creature_types=tuple(e.get("creature_types") or ()), precast=bool(e.get("precast")),
        value=int(e.get("value", 0)), base=int(e.get("base", 0)),
        dtype=e.get("damage_type", "force"), raw=dict(e))


def book(rs) -> dict:
    """{spell name: SpellEffect} for a Ruleset (its ``sim_spells``)."""
    return {name: from_entry(e) for name, e in rs.sim_spells.items()}


def _by_level(pairs: tuple, level: int, default=None):
    out = default
    for lvl, v in pairs:
        if level >= lvl:
            out = v
    return out


def dice_at(eff: SpellEffect, slot_level: int = 0, character_level: int = 1) -> tuple:
    """Damage/heal dice groups when cast with ``slot_level`` (cantrips by character level)."""
    if not eff.dice:
        return ()
    if eff.level == 0:
        if eff.scale_cantrip:
            steps = 1 + (character_level >= 5) + (character_level >= 11)
            return tuple(Dice(g.count * steps, g.sides) for g in eff.dice)
        return eff.dice
    if slot_level < eff.level:
        raise ValueError(f"{eff.name} needs a level-{eff.level} slot, not {slot_level}")
    return add_dice(eff.dice, eff.upcast, slot_level - eff.level)


def beams_at(eff: SpellEffect, slot_level: int = 0, character_level: int = 1) -> int:
    if eff.beams_by_level:
        return _by_level(eff.beams_by_level, character_level, eff.beams)
    if eff.level == 0:
        return eff.beams
    return eff.beams + eff.beams_upcast * max(0, slot_level - eff.level)


def cantrip_extra(eff: SpellEffect, character_level: int) -> tuple:
    """True Strike's extra radiant dice at a character level."""
    v = _by_level(eff.extra_by_level, character_level)
    return parse_dice(v) if v else ()


def weapon_die(eff: SpellEffect, character_level: int) -> Optional[Dice]:
    """Shillelagh's weapon die at a character level."""
    v = _by_level(eff.weapon_die_by_level, character_level)
    return Dice.parse("1" + v if str(v).startswith("d") else v) if v else None
