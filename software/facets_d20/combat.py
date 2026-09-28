"""Facets d20 combat rules (facets_d20/08_Combat.md, 09_Mirror_Masters_Guide.md).

Each rule is one function. The simulator (sim.py) calls these and nothing else to
resolve a fight; it never carries its own copy of a rule.

Rules encoded here:
    attack_roll          d20 + bonus vs AC; nat 20 hits and crits, nat 1 misses;
                         advantage/disadvantage; widened crit range
    roll_damage          PC damage: dice + mod; a crit doubles the dice, not the mod
    monster_damage       fixed (average) damage; on a crit roll double dice + mod
    saving_throw         d20 + bonus vs DC
    damage_after_save    half/none on a save; minions take none on a success and all
                         on a failure; Evasion
    apply_damage         temp HP, resistance, Bloodied, minion death, monster death,
                         PC unconscious / massive damage / damage-at-0 death failures,
                         concentration DC
    concentration_check  Con save vs max(10, half damage)
    spark_attack/save    the Spark die: +1d6 after a roll (−1d6 with Turn the Odds)
    morale_check         DC 10 Wis save; fail = broken; bosses and "never" exempt
    morale_triggers      first Bloodied; leader falls (all foes in v0.1, minions only
                         under the v0.2 option)
    side_initiative      surprise decides, else one d20 per side + the side's best Dex
                         modifier (Alert: advantage on the party's roll); ties to players
    round_order          the order of phases in a round (boss top-of-round option)
    turns_per_phase      boss 2, others 1
    inflict              a condition from a failed save; boss resolve (a boss loses its
                         next turn instead of a disabling effect, at most one a round)
    begin_turn           reaction back; resolve-owed or stunned turns are lost
    roll_recharge        a spent Recharge ability returns on a d6 at the turn's start
    take_reaction        one reaction per round
    provokes_opportunity_attack
    death_save / heal    SRD death saves, unchanged
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import dice as _dice
from .dice import Dice

ABILITIES = ("str", "dex", "con", "int", "wis", "cha")


@dataclass(frozen=True)
class RuleOptions:
    """Switches for the rules that differ between chassis versions.

    leader_morale: "all" (v0.1: every foe checks when its leader falls) or "minions"
        (audit K1 fix: only minions do).
    boss_top_of_round: audit K1 fix — a boss takes one of its turns at the top of every
        round, whoever won the side contest.
    morale_dc: the DC of the morale save.
    boss_bloodied: the boss's Bloodied change the simulator plays ("desperate": advantage
        on its attacks and on attacks against it — 09's second option; "none").
    """

    leader_morale: str = "minions"
    boss_top_of_round: bool = True
    morale_dc: int = 10
    boss_bloodied: str = "desperate"


# ---------------------------------------------------------------- data shapes


@dataclass(frozen=True)
class MonsterAttack:
    name: str
    to_hit: int
    fixed: int
    dice: Optional[Dice] = None
    mod: int = 0
    dtype: str = "bludgeoning"
    count: int = 1                 # attacks of this kind per turn (Multiattack)
    save_dc: Optional[int] = None  # area / save attacks
    save_ability: str = "dex"
    half_on_save: bool = True
    targets: int = 1               # creatures an area attack catches
    recharge_min: Optional[int] = None  # recharge on d6 >= this
    extra: tuple = ()              # unconditional extra dice ("plus 3 (1d6) Fire")


@dataclass
class Combatant:
    id: str
    name: str
    side: str                      # "party" | "enemy"
    max_hp: int
    ac: int
    role: str = "standard"         # "pc" | "minion" | "standard" | "boss"
    saves: dict = field(default_factory=dict)
    hp: Optional[int] = None
    temp_hp: int = 0
    dex_mod: int = 0
    morale: str = "normal"         # "normal" | "never"
    leader: bool = False
    resist: set = field(default_factory=set)
    conditions: set = field(default_factory=set)
    state: str = "active"          # active | down | stable | dead | broken
    bloodied_seen: bool = False
    death_successes: int = 0
    death_failures: int = 0
    reaction_available: bool = True
    concentrating: Optional[str] = None
    evasion: bool = False
    attacks: list = field(default_factory=list)   # MonsterAttack for foes
    turns_taken_this_phase: int = 0
    tags: set = field(default_factory=set)
    profile: object = None         # PC combat profile (build.CombatProfile)
    resources: dict = field(default_factory=dict)
    stun_turns_lost: int = 0
    lose_next_turn: bool = False
    last_resolve_round: int = -1

    def __post_init__(self):
        if self.hp is None:
            self.hp = self.max_hp
        for a in ABILITIES:
            self.saves.setdefault(a, 0)

    @property
    def is_pc(self) -> bool:
        return self.role == "pc"

    @property
    def in_fight(self) -> bool:
        """Still able to act or be targeted as a live threat."""
        return self.state == "active"


# ---------------------------------------------------------------- rolls


@dataclass(frozen=True)
class AttackResult:
    natural: int
    total: int
    hit: bool
    crit: bool


def attack_roll(rng, bonus: int, ac: int, *, advantage: bool = False,
                disadvantage: bool = False, crit_min: int = 20) -> AttackResult:
    r = _dice.d20(rng, advantage=advantage, disadvantage=disadvantage)
    total = r.natural + bonus
    if r.natural == 1:
        return AttackResult(r.natural, total, False, False)
    crit = r.natural >= crit_min
    hit = crit or r.natural == 20 or total >= ac
    return AttackResult(r.natural, total, hit, crit)


def hit_chance(bonus: int, ac: int) -> float:
    """Probability a single d20 attack hits (nat 1 misses, nat 20 hits)."""
    need = ac - bonus
    p = (21 - need) / 20
    return min(0.95, max(0.05, p))


def spark_can_turn(*, total: int, target: int) -> bool:
    """A Spark (+1d6) is worth spending only if the roll is short by 1–6."""
    return 0 < target - total <= 6


def spark_attack(rng, res: "AttackResult", *, ac: int, subtract: bool = False) -> "AttackResult":
    """Spend a Spark on an attack roll after it is made (+1d6, or −1d6 with Turn the Odds).

    Natural 1s still miss and natural 20s still hit (a crit can't be undone)."""
    if res.natural == 1 or res.natural == 20 or res.crit:
        return res
    d = rng.randint(1, 6)
    total = res.total - d if subtract else res.total + d
    return AttackResult(res.natural, total, total >= ac, False)


def spark_save(rng, res: "SaveResult", *, dc: int) -> "SaveResult":
    total = res.total + rng.randint(1, 6)
    return SaveResult(res.natural, total, total >= dc)


def roll_damage(rng, d: Optional[Dice], mod: int, *, crit: bool = False,
                min_face: int = 1) -> int:
    total = mod
    if d is not None:
        total += _dice.roll(rng, d.times(2) if crit else d, min_face=min_face)
    return max(0, total)


def monster_damage(rng, atk: MonsterAttack, *, crit: bool) -> int:
    """Fixed damage; a critical hit is rolled (double dice + modifier)."""
    if not crit:
        return atk.fixed
    if atk.dice is None:
        return atk.fixed * 2
    extra = sum(_dice.roll(rng, d.times(2)) for d in atk.extra)
    return max(0, _dice.roll(rng, atk.dice.times(2)) + atk.mod + extra)


@dataclass(frozen=True)
class SaveResult:
    natural: int
    total: int
    success: bool


def saving_throw(rng, bonus: int, dc: int, *, advantage: bool = False,
                 disadvantage: bool = False) -> SaveResult:
    r = _dice.d20(rng, advantage=advantage, disadvantage=disadvantage)
    total = r.natural + bonus
    return SaveResult(r.natural, total, total >= dc)


def damage_after_save(target: Combatant, damage: int, *, saved: bool,
                      half_on_save: bool) -> int:
    if target.role == "minion":
        return 0 if saved else damage
    if target.evasion and half_on_save:
        return 0 if saved else damage // 2
    if saved:
        return damage // 2 if half_on_save else 0
    return damage


# ---------------------------------------------------------------- taking damage


@dataclass
class DamageOutcome:
    dealt: int = 0
    became_bloodied: bool = False
    dropped: bool = False
    killed: bool = False
    floored: bool = False
    concentration_dc: Optional[int] = None


def is_bloodied(c: Combatant) -> bool:
    return c.hp <= c.max_hp // 2 if c.max_hp > 1 else False


def apply_damage(rng, target: Combatant, amount: int, *, crit: bool = False,
                 dtype: Optional[str] = None, floor_one: bool = False) -> DamageOutcome:
    """Deal damage. ``floor_one``: a drop-to-1 feature is available and used if needed
    (it can't stop massive damage). Undead Fortitude (tag ``undead_fortitude``): a
    non-crit, non-radiant blow that would kill allows a Con save (DC 5 + damage) to stay
    at 1 HP."""
    out = DamageOutcome()
    if target.state == "dead":
        return out
    if dtype is not None and dtype in target.resist:
        amount //= 2
    amount = max(0, amount)
    if amount == 0:
        return out

    # Already at 0 (a PC dying): a death-save failure, two on a crit.
    if target.is_pc and target.state in ("down", "stable"):
        target.state = "down"
        target.death_failures += 2 if crit else 1
        if amount >= target.max_hp:
            target.death_failures = 3
        if target.death_failures >= 3:
            target.state = "dead"
        return out

    absorbed = min(target.temp_hp, amount)
    target.temp_hp -= absorbed
    rest = amount - absorbed
    was_bloodied = is_bloodied(target)
    overflow = rest - target.hp
    target.hp = max(0, target.hp - rest)
    out.dealt = amount
    if target.hp == 0 and target.role != "minion":
        massive = target.is_pc and overflow >= target.max_hp
        if floor_one and not massive:
            target.hp = 1
            out.floored = True
        elif "undead_fortitude" in target.tags and not crit and dtype != "radiant" \
                and saving_throw(rng, target.saves.get("con", 0), 5 + amount).success:
            target.hp = 1

    if target.role == "minion" and amount > 0:
        target.hp = 0
    if target.concentrating is not None and target.hp > 0 and rest > 0:
        out.concentration_dc = max(10, rest // 2)

    if target.hp == 0:
        target.concentrating = None
        if target.is_pc:
            if overflow >= target.max_hp:
                target.state = "dead"
                out.killed = True
            else:
                target.state = "down"
                target.death_successes = target.death_failures = 0
            out.dropped = True
        else:
            target.state = "dead"
            out.killed = True
            out.dropped = True
        return out

    if not was_bloodied and is_bloodied(target) and not target.bloodied_seen:
        target.bloodied_seen = True
        out.became_bloodied = True
    return out


def concentration_check(rng, c: Combatant, *, dc: int) -> bool:
    ok = saving_throw(rng, c.saves.get("con", 0), dc).success
    if not ok:
        c.concentrating = None
    return ok


def heal(c: Combatant, amount: int) -> int:
    if c.state == "dead" or amount <= 0:
        return 0
    before = c.hp
    c.hp = min(c.max_hp, c.hp + amount)
    if c.hp > 0 and c.state in ("down", "stable"):
        c.state = "active"
        c.death_successes = c.death_failures = 0
    if not is_bloodied(c):
        pass
    return c.hp - before


# ---------------------------------------------------------------- morale


def morale_check(rng, c: Combatant, opts: RuleOptions = RuleOptions()) -> Optional[bool]:
    """True = broke, False = held, None = exempt (bosses, "never", PCs)."""
    if c.role in ("boss", "pc") or c.morale == "never" or c.state != "active":
        return None
    broke = not saving_throw(rng, c.saves.get("wis", 0), opts.morale_dc).success
    if broke:
        c.state = "broken"
    return broke


def morale_triggers(c: Combatant, outcome: Optional[DamageOutcome], *, leader_fell: bool,
                    opts: RuleOptions) -> bool:
    if c.role in ("boss", "pc") or c.morale == "never" or c.state != "active":
        return False
    if outcome is not None and outcome.became_bloodied:
        return True
    if leader_fell:
        return opts.leader_morale == "all" or c.role == "minion"
    return False


# ---------------------------------------------------------------- initiative and turns


def side_initiative(rng, party_dex_mods, enemy_dex_mods, *, surprised: Optional[str] = None,
                    party_advantage: bool = False, enemy_advantage: bool = False) -> str:
    """The side that goes first: "party" or "enemy" (DESIGN v0.2 §6.1).

    A surprised side goes second. Otherwise each side rolls ONE d20 + its best modifier;
    Alert gives the party's roll advantage; ties go to the players.
    """
    if surprised == "enemy":
        return "party"
    if surprised == "party":
        return "enemy"
    party = _dice.d20(rng, advantage=party_advantage).natural + max(party_dex_mods)
    enemy = _dice.d20(rng, advantage=enemy_advantage).natural + max(enemy_dex_mods)
    return "party" if party >= enemy else "enemy"


def round_order(first: str, opts: RuleOptions, *, enemy_has_boss: bool) -> list:
    """Phases of one round. "boss" is a phase in which each boss takes one turn."""
    second = "enemy" if first == "party" else "party"
    order = [first, second]
    if enemy_has_boss and opts.boss_top_of_round:
        order = ["boss"] + order
    return order


def turns_per_phase(c: Combatant) -> int:
    return 2 if c.role == "boss" else 1


DISABLING = frozenset({"stunned", "paralyzed", "incapacitated", "banished", "polymorphed",
                       "asleep", "held", "entranced"})


def inflict(c: Combatant, condition: str, *, round_no: int) -> str:
    """Apply a condition after a failed save. Returns "applied", "resolve" or "resisted".

    Boss resolve (DESIGN v0.2 §6.2): an effect that would stun, paralyse, incapacitate,
    banish, polymorph or put a boss to sleep makes it lose its next turn instead, and the
    effect ends. A boss loses at most one turn a round this way ("resisted" after that).
    """
    if c.role == "boss" and condition in DISABLING:
        if c.last_resolve_round == round_no:
            return "resisted"
        c.last_resolve_round = round_no
        c.lose_next_turn = True
        return "resolve"
    c.conditions.add(condition)
    return "applied"


def begin_turn(c: Combatant) -> bool:
    """Start a creature's turn. Returns False if it loses the turn.

    Its reaction comes back. A boss that owes a turn to boss resolve loses this one. A
    stunned creature loses the turn (the stun's duration is the caller's business).
    """
    c.reaction_available = True
    if c.lose_next_turn:
        c.lose_next_turn = False
        c.stun_turns_lost += 1
        return False
    if "stunned" in c.conditions:
        c.stun_turns_lost += 1
        return False
    return True


def roll_recharge(rng, c: Combatant, *, recharge_min: int) -> bool:
    """At the start of a creature's turn, a spent Recharge ability comes back on a d6 ≥ min."""
    if getattr(c, "special_ready", False):
        return True
    ready = rng.randint(1, 6) >= recharge_min
    c.special_ready = ready  # type: ignore[attr-defined]
    return ready


def take_reaction(c: Combatant) -> bool:
    if not c.reaction_available:
        return False
    c.reaction_available = False
    return True


def provokes_opportunity_attack(*, leaves_reach: bool, disengaged: bool = False,
                                forced: bool = False) -> bool:
    return leaves_reach and not disengaged and not forced


# ---------------------------------------------------------------- dying


def death_save(rng, c: Combatant) -> Optional[str]:
    """Roll a death save for a PC at 0 HP. Returns the new state if it changed."""
    if c.state != "down":
        return None
    n = rng.randint(1, 20)
    if n == 20:
        c.hp = 1
        c.state = "active"
        c.death_successes = c.death_failures = 0
        return "active"
    if n == 1:
        c.death_failures += 2
    elif n >= 10:
        c.death_successes += 1
    else:
        c.death_failures += 1
    if c.death_failures >= 3:
        c.state = "dead"
        return "dead"
    if c.death_successes >= 3:
        c.state = "stable"
        return "stable"
    return None
