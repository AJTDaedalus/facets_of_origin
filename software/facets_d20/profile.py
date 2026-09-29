"""The combat profile: what a built character brings to a fight.

``build.py`` turns picks (Facet, path, abilities, talents, domains, kit) into a
``CombatProfile``; ``sim.py`` turns a profile into a ``Combatant`` and runs it with the
rules in ``combat.py``. The profile holds numbers and switches only — no rule logic.
Every field is set by an effect in the yaml (see build._apply_effect) or by the chassis
numbers. Uses are per long rest unless ``recharge`` says "short"; ``short_regain`` is how
many come back on a short rest.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .dice import Dice


@dataclass(frozen=True)
class Weapon:
    name: str
    dice: Dice
    to_hit: int
    mod: int                       # damage modifier (ability + flat bonuses)
    dtype: str = "slashing"
    ranged: bool = False
    finesse: bool = False
    two_handed: bool = False
    min_face: int = 1
    crit_min: int = 20
    heavy_or_versatile: bool = False
    str_based: bool = False


@dataclass(frozen=True)
class Uses:
    uses: int
    recharge: str = "long"         # "long" | "short"
    short_regain: int = 0


@dataclass
class CasterProfile:
    tradition: str
    kind: str                      # "full" | "half"
    ability: str
    mod: int
    attack: int
    dc: int
    slots: list                    # slots per spell level, [1st, 2nd, ...]
    cantrips: list = field(default_factory=list)
    spells: list = field(default_factory=list)     # leveled spells castable (all on lists)
    domains: list = field(default_factory=list)
    heal_boost: bool = False       # Channel: a slot heal adds 2 + slot level to one target
    spell_damage_bonus: int = 0    # Evoker 5th: + casting mod to one damage roll per spell
    cantrip_damage_bonus: int = 0  # SRD Potent Spellcasting: + casting mod to cantrip damage
    maximize: Optional[Uses] = None
    forbidden_while_raging: bool = False


@dataclass
class Rider:
    """Extra dice on a weapon hit. ``rider`` ones share the one-per-turn limit (E1)."""
    name: str
    dice: Dice
    any_of: frozenset = frozenset()   # has_advantage | ally_adjacent_to_target | studied_target
    weapon: frozenset = frozenset()   # finesse | ranged | melee (empty = any)
    uses: Optional[Uses] = None       # resource-paid (Sworn Strike)
    fallback: bool = False            # only on a turn no other rider was used
    dtype: str = "radiant"
    is_rider: bool = True
    all_of: frozenset = frozenset()   # every one must hold (e.g. raging + has_advantage)
    once_per_turn: bool = True


@dataclass
class CombatProfile:
    name: str
    level: int
    prof: int
    hp: int
    ac: int
    saves: dict
    dex_mod: int
    abilities: dict = field(default_factory=dict)
    weapon: Optional[Weapon] = None
    attacks_per_action: int = 1
    riders: list = field(default_factory=list)
    rider_limit: int = 1
    # Body
    second_wind: Optional[dict] = None      # {"uses": Uses, "dice", "bonus"}
    action_surge: Optional[Uses] = None
    reroll_save: Optional[dict] = None      # {"uses": Uses, "add": int}
    rage: Optional[dict] = None             # {"uses": Uses, "damage", "resist": set, "ac"}
    reckless: bool = False                  # (while raging, if rage)
    drop_to_one: Optional[dict] = None      # {"uses": Uses, "needs": "raging"|None}
    bonus_attack: Optional[Weapon] = None   # Martial Arts (after the Attack action)
    flurry: Optional[dict] = None           # {"count": 2, "cost": 1}
    focus: Optional[Uses] = None
    stun: Optional[dict] = None             # {"dc", "cost"}
    halve_damage: bool = False              # Uncanny Dodge (reaction)
    evasion: bool = False
    redirect: int = 0                       # Guardian: take an adjacent ally's hit, reduce by this
    aim: bool = False                       # Marksman: bonus action, advantage on next ranged attack
    cleave: int = 0                         # second-creature damage on a heavy/versatile melee hit
    crit_heal: int = 0
    # Mind
    study: Optional[Uses] = None            # Study: bonus action, advantage on next attack
    crit_min_studied: int = 20
    studied_damage_bonus: int = 0           # Anatomist: + to weapon damage vs your studied target
    anticipate: bool = False
    master_plan: Optional[Uses] = None
    master_plan_rounds: int = 1             # the plan holds for the first N rounds
    guard: Optional[dict] = None            # Clockwork Guardian {"dice", "bonus"}
    field_kit: Optional[dict] = None        # {"amount", "allies"}
    # Soul
    kindle: Optional[Uses] = None           # grants Sparks
    spark_floor: int = 0                    # Turn the Odds
    spark_subtract: bool = False
    heal_pool: int = 0
    heal_touch: Optional[dict] = None       # Channel heal {"uses": Uses, "dice", "bonus"}
    channel_damage: Optional[dict] = None   # {"dice", "bonus", "save", "half"} (shares uses)
    save_aura: int = 0                      # Warden
    max_next_hit: bool = False
    initiative_bonus: int = 0
    hit_die: int = 8
    hd_bonus: int = 0                       # Field Medic: + per Hit Die spent (short rest)
    initiative_advantage: bool = False      # Alert: the party's side roll has advantage
    # Edges (Amendment 5, DESIGN §1.4b)
    damage_floor: int = 1                   # Heavy Hands (folded into the weapon's min_face)
    graze: int = 0                          # Graze: damage on a two-handed heavy/versatile melee miss
    sap: bool = False                       # Sap: a hit gives the target disadvantage on its next attack
    parry: int = 0                          # Parry: reaction, +N AC against one hit (melee weapon held)
    death_save_advantage: bool = False      # Die Hard
    second_breath: int = 0                  # Second Breath: temp HP the first time Bloodied in a fight
    hd_max: bool = False                    # Hale: Hit Dice restore their maximum on a short rest
    piercing: Optional[Uses] = None         # Piercing Spell: one target saves with disadvantage
    steady_focus: bool = False              # Steady Focus: reaction keeps concentration
    resist: set = field(default_factory=set)
    temp_hp: int = 0
    caster: Optional[CasterProfile] = None
    healer: bool = False
    features: list = field(default_factory=list)
    notes: list = field(default_factory=list)
