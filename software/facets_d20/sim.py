"""Monte Carlo fight simulator for Facets d20.

Every roll and every rule goes through ``combat.py``; this module only decides *what*
each creature does (the tactical AI below) and keeps score. It carries no rule of its
own. Spell numbers come from ``sim_spells`` in the yaml (spells.py), character numbers
from ``build.py`` profiles, monster numbers from ``monsters.py``.

Tactical AI (documented; change it here and nowhere else)
---------------------------------------------------------
Fight start: Field Kit temp HP; Kindle Sparks handed to allies (1 each, cap 3) and
Turn the Odds' floor of 1; Mage Armor already cast (it lasts all day).

Party — each PC, on its turn, in party order:
  1. At 0 HP: death save (with advantage: Die Hard). Sap (edge) laid by this PC ends.
  2. Bonus action, first that applies:
     a. Below half HP with Second Wind → use it.
     b. An ally at 0 HP and a bonus-action heal (Healing Word, Mass Healing Word,
        Mending Hands pool) → heal them.
     c. Rage (turn one). Study the focus target (new target). Aim (ranged weapon).
     d. Sustain a bonus-action concentration spell already up (Spiritual Weapon,
        Flaming Sphere), or cast one if not concentrating and a slot is free.
     e. After the Attack action: Flurry (if focus is left) or the free Martial Arts strike.
  3. Action, first that applies:
     a. An ally at 0 HP → best heal (spell, Channel, Mending Hands).
     a2. Can't heal, and a friend at 0 HP has two failed death saves → stabilize it
        (an action, no check: V56; RuleOptions.stabilize "check" plays the SRD roll).
     b. Healer and an ally below half → heal.
     c. Not concentrating, ≥2 foes, an aura spell (Spirit Guardians...) → cast it, if two
        rounds of it are worth at least one Attack action (S-5: highest expected value).
     d. ≥3 foes and an area damage spell → the best one by expected total damage, if that
        beats the Attack action's expected damage.
     e. Not concentrating, a disable spell that works on the biggest foe (a boss, or a
        foe holding ≥40% of enemy HP) → cast it, if holding it for two of its turns
        (chance it fails the save × its expected turn damage × 2) beats the Attack action.
     f. Otherwise the best expected single-target damage: the Attack action (with riders),
        a cantrip, Channel damage, a sustained action spell (Call Lightning), or a
        leveled single-target spell (leveled spells only in the first two rounds).
     Action Surge: a second action (never a spell) on the first turn it is available.
  Edges on weapon attacks: Heavy Hands is the weapon's damage-die floor; Graze deals its
  damage on the first qualifying miss of the turn; Sap marks the first creature hit each
  turn (its next attack roll has disadvantage). Piercing Spell is spent on the first
  save of the first slot spell or disable spell it can reach (one target).
  Riders (E1): at most one per turn; the biggest eligible one is used, free before paid on
  a tie; paid ones (Sworn Strike) are spent on the first eligible hit.
  Targeting (focus fire): the standing foe with the highest threat per remaining HP
  (threat = its ordinary-turn damage), ties to the lowest HP. Area spells catch
  ``targets`` standing foes at random.
  Sparks (V15): +1d6 after a roll, spent only when it can turn the result (a miss or a
  failed save short by 1–6); the roller's own Spark first, else an ally's. A Turn the
  Odds holder subtracts a d6 from an enemy hit it could turn into a miss (once a round).
  Session Sparks and MM awards are roleplay rewards and are not modelled; Kindle and Turn
  the Odds Sparks are.
Enemies:
  - Every foe, boss included, attacks a random standing PC (DESIGN v0.2 §6.2: the MM
    spreads the enemy side's attacks). Nobody attacks a PC at 0 HP.
  - A recharge special (breath) is used when ready and ≥2 PCs stand; it rolls to
    recharge at the start of the foe's turn (a boss: its top-of-round turn only).
  - A boss takes its turns at the top of the round and right after the party's first
    turn (combat.round_order); leaderless minions check morale when half are down.
  - A Bloodied boss turns desperate (advantage on its attacks, attacks against it have
    advantage) — RuleOptions.boss_bloodied.
  - PC reactions to a hit, in order: Shield (if it turns the hit into a miss);
    Parry (edge; the first non-critical hit, spent without knowing whether +2 turns it —
    hidden AC, V46 — and never by a PC with Shield to cast or Uncanny Dodge); Turn the Odds; Guardian (an ally with more HP to spare takes the hit, reduced);
    Clockwork Guard (the first hit on its ward — the ally the construct stood beside when
    it acted right after its maker, the one with the lowest share of HP — until the
    maker's next turn; 5-ft reach, DESIGN §4 Clockwork Guardian); Uncanny Dodge (halve). Before the roll:
    Anticipate gives disadvantage if the attacker is that PC's studied target, as does
    Sap on a sapped attacker. On damage: Steady Focus spends the reaction on a failed
    concentration save; Second Breath's temporary HP arrive the first time a PC is
    Bloodied and standing.
Daily resources: a fight starts with ``resource_share`` of each long-rest pool (slots per
level, long-rest uses), rounded up, plus the short-rest regain; short-rest pools are
full; HP full. Default share 1/3: a fight is one of the day's three Clashes (V34).
"""
from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional

from . import combat, spells as _spells
from .combat import Combatant, RuleOptions
from .dice import Dice
from .profile import CombatProfile, Uses, Weapon

MAX_ROUNDS = 20
DEFAULT_SHARE = 1 / 3  # a fight is one of the day's three Clashes (yaml adventuring_day, V34)


# ================================================================ encounter description


@dataclass(frozen=True)
class FoeSpec:
    monster: object                 # library id or MonsterBlock
    role: str = "standard"
    count: int = 1
    leader: bool = False


@dataclass(frozen=True)
class Encounter:
    foes: tuple
    surprise: Optional[str] = None  # "party" | "enemy" is surprised
    name: str = ""

    @classmethod
    def of(cls, *specs, surprise=None, name=""):
        return cls(tuple(specs), surprise, name)


# ================================================================ results


@dataclass
class FightResult:
    won: bool
    rounds: int
    dropped: set
    dead: set
    damage_by_pc: dict
    resources_spent: dict
    party_hp_lost: int
    party_hp_max: int
    foes_broken: int
    foes_killed: int
    timed_out: bool = False
    healing_by_pc: dict = field(default_factory=dict)
    prevented_by_pc: dict = field(default_factory=dict)
    selfheal_by_pc: dict = field(default_factory=dict)
    temp_by_pc: dict = field(default_factory=dict)
    attacks_on: dict = field(default_factory=dict)
    hits_on: dict = field(default_factory=dict)
    raw_on: dict = field(default_factory=dict)
    taken_on: dict = field(default_factory=dict)
    end_hp: list = field(default_factory=list)
    end_state: list = field(default_factory=list)
    party_hp_start: int = 0
    used: list = field(default_factory=list)         # per PC: {pool: used}
    slots_used: list = field(default_factory=list)   # per PC: [per level]
    sparks_left: list = field(default_factory=list)


@dataclass
class SimSummary:
    n: int
    win_rate: float
    mean_rounds: float
    p_any_drop: float
    p_death: float
    mean_hp_lost_frac: float
    dpr_by_pc: dict
    resources_spent: dict
    rounds_hist: dict = field(default_factory=dict)

    def as_row(self) -> dict:
        return dict(n=self.n, win=round(self.win_rate, 3), rounds=round(self.mean_rounds, 2),
                    p_drop=round(self.p_any_drop, 3), p_death=round(self.p_death, 3),
                    hp_lost=round(self.mean_hp_lost_frac, 3))


# ================================================================ per-fight PC state


def per_fight(u: Optional[Uses], share: float) -> int:
    if u is None:
        return 0
    if u.recharge == "short":
        return u.uses
    return min(u.uses, math.ceil(u.uses * share) + u.short_regain)


def pools(prof: CombatProfile) -> dict:
    """Every limited pool a profile has, as {key: Uses}."""
    d = {}
    if prof.second_wind:
        d["second_wind"] = prof.second_wind["uses"]
    if prof.action_surge:
        d["action_surge"] = prof.action_surge
    if prof.reroll_save:
        d["reroll"] = prof.reroll_save["uses"]
    if prof.rage and prof.rage.get("uses"):
        d["rage"] = prof.rage["uses"]
    if prof.drop_to_one:
        d["floor"] = prof.drop_to_one["uses"]
    for key in ("focus", "study", "master_plan", "kindle"):
        u = getattr(prof, key)
        if u:
            d[key] = u
    if prof.heal_pool:
        d["heal_pool"] = Uses(prof.heal_pool, "long")
    if prof.heal_touch:
        d["channel"] = prof.heal_touch["uses"]
    if prof.caster and prof.caster.maximize:
        d["maximize"] = prof.caster.maximize
    if prof.piercing:
        d["piercing"] = prof.piercing
    for r in prof.riders:
        if r.uses:
            d[f"rider:{r.name}"] = r.uses
    return d


def share_allowance(prof: CombatProfile, share: float) -> tuple:
    """One fight's allowance when a fight gets ``share`` of each long-rest pool."""
    allow = {k: per_fight(u, share) for k, u in pools(prof).items()}
    if "heal_pool" in allow:
        allow["heal_pool"] = math.ceil(prof.heal_pool * share)
    slots = [math.ceil(n * share) for n in prof.caster.slots] if prof.caster else []
    return allow, slots


class _PCState:
    def __init__(self, prof: CombatProfile, allow: dict, slots: list):
        self.prof = prof
        self.allow = dict(allow)
        self.allow_slots = list(slots)
        self.slots = list(slots)
        self.second_wind = allow.get("second_wind", 0)
        self.action_surge = allow.get("action_surge", 0)
        self.reroll = allow.get("reroll", 0)
        self.rage = allow.get("rage", 0)
        self.floor = allow.get("floor", 0)
        self.focus = allow.get("focus", 0)
        self.study = allow.get("study", 0)
        self.master_plan = allow.get("master_plan", 0)
        self.kindle = allow.get("kindle", 0)
        self.heal_pool = allow.get("heal_pool", 0)
        self.channel = allow.get("channel", 0)
        self.maximize = allow.get("maximize", 0)
        self.piercing = allow.get("piercing", 0)          # Piercing Spell (edge)
        self.breathed = False                              # Second Breath used this fight
        self.rider_uses = {r.name: allow.get(f"rider:{r.name}", 0) for r in prof.riders if r.uses}
        self.raging = False
        self.sparks = 0
        self.studied = None
        self.aura = None               # (SpellEffect, slot) of a concentration spell
        self.sustain_used_round = 0
        self.spent = {}
        self.max_next = False
        self.turned_odds_round = 0

    def remaining(self) -> dict:
        d = {k: getattr(self, k) for k in self.allow if hasattr(self, k) and not k.startswith("rider:")}
        d.update({f"rider:{k}": v for k, v in self.rider_uses.items()})
        return d

    def used(self) -> dict:
        rem = self.remaining()
        return {k: self.allow[k] - rem.get(k, self.allow[k]) for k in self.allow}

    def slots_used(self) -> list:
        return [a - b for a, b in zip(self.allow_slots, self.slots)]

    def spend(self, key, n=1):
        self.spent[key] = self.spent.get(key, 0) + n

    def best_slot(self, min_level: int) -> Optional[int]:
        levels = [i + 1 for i, n in enumerate(self.slots) if n > 0 and i + 1 >= min_level]
        return max(levels) if levels else None

    def low_slot(self, min_level: int) -> Optional[int]:
        levels = [i + 1 for i, n in enumerate(self.slots) if n > 0 and i + 1 >= min_level]
        return min(levels) if levels else None

    def take(self, level: Optional[int]) -> Optional[int]:
        if level is None or self.slots[level - 1] <= 0:
            return None
        self.slots[level - 1] -= 1
        self.spend(f"slot_{level}")
        return level


def pc_combatant(prof: CombatProfile, idx: int) -> Combatant:
    return Combatant(id=f"pc{idx}:{prof.name}", name=prof.name, side="party", max_hp=prof.hp,
                     ac=prof.ac, role="pc", saves=dict(prof.saves), dex_mod=prof.dex_mod,
                     resist=set(prof.resist), evasion=prof.evasion, profile=prof,
                     temp_hp=prof.temp_hp)


def _threat(foe: Combatant) -> float:
    return sum(a.fixed * a.count for a in foe.attacks) * (2 if foe.role == "boss" else 1) or 1


def _roll(rng, groups, maximize=False) -> int:
    if maximize:
        return sum(g.count * g.sides for g in groups)
    return sum(combat.roll_damage(rng, g, 0) for g in groups)


class Fight:
    def __init__(self, rng, party: list, encounter: Encounter, opts: RuleOptions,
                 resource_share: float = DEFAULT_SHARE, book: Optional[dict] = None, *,
                 allowances: Optional[list] = None, start_hp: Optional[list] = None,
                 start_sparks: Optional[list] = None, control: bool = True):
        from . import monsters
        self.rng = rng
        self.opts = opts
        self.control = control
        self.book = book if book is not None else _default_book()
        self.pcs = [pc_combatant(p, i) for i, p in enumerate(party)]
        self.state = {}
        for i, c in enumerate(self.pcs):
            allow, slots = allowances[i] if allowances else share_allowance(c.profile,
                                                                            resource_share)
            self.state[c.id] = _PCState(c.profile, allow, slots)
            if start_hp is not None:
                c.hp = max(0, min(c.max_hp, int(start_hp[i])))
                if c.hp == 0:
                    c.state = "dead" if start_hp[i] < 0 else "stable"
            if start_sparks is not None:
                self.state[c.id].sparks = start_sparks[i]
        self.healing_by_pc = {c.id: 0 for c in self.pcs}
        self.prevented_by_pc = {c.id: 0.0 for c in self.pcs}
        self.selfheal_by_pc = {c.id: 0 for c in self.pcs}
        self.temp_by_pc = {c.id: 0 for c in self.pcs}
        self.attacks_on = {c.id: 0 for c in self.pcs}
        self.hits_on = {c.id: 0 for c in self.pcs}
        self.raw_on = {c.id: 0 for c in self.pcs}
        self.taken_on = {c.id: 0 for c in self.pcs}
        self.foes = []
        n = 0
        for spec in encounter.foes:
            for k in range(spec.count):
                n += 1
                self.foes.append(monsters.convert(spec.monster, role=spec.role,
                                                  uid=f"f{n}", leader=spec.leader and k == 0,
                                                  hp_multiplier=opts.boss_hp_multiplier))
        self.encounter = encounter
        self.damage_by_pc = {c.id: 0 for c in self.pcs}
        self.dropped = set()
        self.round = 0
        self._turns = {}               # pc id -> the turn dict of its current turn
        self.guard_ward = {}           # Clockwork Guardian: maker id -> the ally it stands beside
        self.guard_ready = {}          # maker id -> its Guard is up (until the maker's next turn)
        self.blessed = {}
        self._turns_this_round = {}    # foe id -> its turns so far this round (boss rule)
        self._leaderless_checked = False

    # ------------------------------------------------------------ setup
    def setup(self) -> None:
        for pc in self.pcs:
            p, st = pc.profile, self.state[pc.id]
            if p.field_kit:
                pc.temp_hp = max(pc.temp_hp, p.field_kit["amount"])
                self.temp_by_pc[pc.id] += p.field_kit["amount"]
                others = [c for c in self.pcs if c is not pc][: p.field_kit["allies"]]
                for c in others:
                    gain = max(0, p.field_kit["amount"] - c.temp_hp)
                    c.temp_hp = max(c.temp_hp, p.field_kit["amount"])
                    self.healing_by_pc[pc.id] += gain
            st.sparks = max(st.sparks, p.spark_floor)
        for pc in self.pcs:
            st = self.state[pc.id]
            k = st.kindle
            for c in [x for x in self.pcs if x is not pc] + [pc]:
                if k <= 0:
                    break
                cs = self.state[c.id]
                if cs.sparks < 3:
                    cs.sparks += 1
                    k -= 1
                    st.spend("kindle")

    # ------------------------------------------------------------ queries
    def _spell(self, name):
        return self.book.get(name)

    def standing_foes(self):
        return [f for f in self.foes if f.state == "active"]

    def standing_pcs(self):
        return [c for c in self.pcs if c.state == "active"]

    def over(self) -> Optional[bool]:
        if not self.standing_foes():
            return True
        if not self.standing_pcs():
            return False
        return None

    def focus_target(self) -> Optional[Combatant]:
        foes = self.standing_foes()
        if not foes:
            return None
        return max(foes, key=lambda f: (_threat(f) / max(1, f.hp), -f.hp))

    def party_save_bonus(self, pc) -> int:
        bonus = 0
        for other in self.standing_pcs():
            if other is not pc and other.profile.save_aura:
                bonus = max(bonus, other.profile.save_aura)
        return bonus

    def melee_ally_beside(self, pc) -> bool:
        return any(c is not pc and c.profile.weapon is not None and not c.profile.weapon.ranged
                   for c in self.standing_pcs())

    # ------------------------------------------------------------ bookkeeping
    def _heal(self, healer: Combatant, target: Combatant, amount: int) -> int:
        """Heal through the rules; credit what was actually restored (no overheal)."""
        got = combat.heal(target, amount)
        if target is healer:
            self.selfheal_by_pc[healer.id] += got
        else:
            self.healing_by_pc[healer.id] += got
        return got

    def _credit(self, pc_id: Optional[str], amount: float) -> None:
        if pc_id in self.prevented_by_pc:
            self.prevented_by_pc[pc_id] += amount

    def foe_turn_value(self, foe: Combatant) -> float:
        """Expected damage of one of the foe's turns against the party (disabled-turn credit)."""
        up = self.standing_pcs() or self.pcs
        ac = sum(c.ac for c in up) / len(up)
        return sum(a.fixed * a.count * combat.hit_chance(a.to_hit, round(ac)) for a in foe.attacks)

    # ------------------------------------------------------------ damage bookkeeping
    def hurt_foe(self, pc: Optional[Combatant], foe: Combatant, amount: int, *,
                 crit=False, dtype=None):
        before = foe.hp
        out = combat.apply_damage(self.rng, foe, amount, crit=crit, dtype=dtype)
        if pc is not None:
            self.damage_by_pc[pc.id] += max(0, before - foe.hp)
        if "entranced" in foe.conditions and amount > 0:
            foe.conditions.discard("entranced")
        if out.concentration_dc is not None:
            combat.concentration_check(self.rng, foe, dc=out.concentration_dc)
        if combat.morale_triggers(foe, out, leader_fell=False, opts=self.opts):
            combat.morale_check(self.rng, foe, self.opts)
        if out.killed and foe.leader:
            for other in self.standing_foes():
                if combat.morale_triggers(other, None, leader_fell=True, opts=self.opts):
                    combat.morale_check(self.rng, other, self.opts)
        if foe.role == "minion" and foe.state != "active":
            mins = [f for f in self.foes if f.role == "minion"]
            if combat.leaderless_minions_check(
                    has_leader=any(f.leader for f in self.foes), minions=len(mins),
                    minions_down=sum(f.state != "active" for f in mins),
                    already=self._leaderless_checked):
                self._leaderless_checked = True
                for other in [f for f in mins if f.state == "active"]:
                    combat.morale_check(self.rng, other, self.opts)
        if foe.role == "boss" and foe.state == "active" and combat.is_bloodied(foe) \
                and self.opts.boss_bloodied == "desperate":
            foe.conditions.add("desperate")
        return out

    def hurt_pc(self, pc: Combatant, amount: int, *, crit=False, dtype=None):
        st = self.state[pc.id]
        prof = pc.profile
        if st.raging and dtype in prof.rage.get("resist", ()):
            amount //= 2
        floor = False
        if st.floor > 0 and prof.drop_to_one and \
                (prof.drop_to_one["needs"] != "raging" or st.raging):
            floor = True
        out = combat.apply_damage(self.rng, pc, amount, crit=crit, dtype=dtype, floor_one=floor)
        if out.floored:
            st.floor -= 1
            st.spend("drop_to_one")
            if prof.max_next_hit:
                st.max_next = True
        if out.dropped:
            self.dropped.add(pc.id)
            self.end_concentration(pc)
            st.raging = False
        if out.concentration_dc is not None:
            held = pc.concentrating
            if not combat.concentration_check(self.rng, pc, dc=out.concentration_dc):
                # Steady Focus (edge): spend the reaction to succeed instead.
                if prof.steady_focus and combat.take_reaction(pc):
                    pc.concentrating = held
                    st.spend("steady_focus")
                else:
                    self.end_concentration(pc)
        # Second Breath (edge): the first time this fight you are Bloodied and standing.
        if prof.second_breath and not st.breathed and pc.state == "active" and pc.hp > 0 \
                and combat.is_bloodied(pc):
            st.breathed = True
            pc.temp_hp = max(pc.temp_hp, prof.second_breath)
            self.temp_by_pc[pc.id] += prof.second_breath
        return out

    def end_concentration(self, pc):
        st = self.state[pc.id]
        pc.concentrating = None
        if st.aura and st.aura[0].name == "Bless":
            self.blessed = {}
        st.aura = None

    def pc_save(self, pc: Combatant, ability: str, dc: int, *, advantage=False,
                stake: float = 0.0) -> bool:
        st = self.state[pc.id]
        aura = self.party_save_bonus(pc)
        bonus = pc.saves.get(ability, 0) + aura
        if self.plan_active():
            advantage = True
        sres = combat.saving_throw(self.rng, bonus, dc, advantage=advantage)
        if aura and sres.success and sres.total - aura < dc and stake:
            warden = max((c for c in self.standing_pcs() if c is not pc and c.profile.save_aura),
                         key=lambda c: c.profile.save_aura, default=None)
            if warden is not None:
                self._credit(warden.id, stake)
        # The MM calls the failure (the rule, spark_may_spend); the table spends when it
        # judges 1d6 can turn it (AI: the party knows the DC once it has seen a save or two).
        if combat.spark_may_spend(succeeded=sres.success, natural=sres.natural) \
                and combat.spark_can_turn(total=sres.total, target=dc) \
                and self.spark_holder(pc) is not None:
            sres = combat.spark_save(self.rng, sres, dc=dc)
        ok = sres.success
        if not ok and st.reroll > 0:
            st.reroll -= 1
            st.spend("reroll")
            ok = combat.saving_throw(self.rng, bonus + pc.profile.reroll_save["add"], dc).success
        return ok

    def spark_holder(self, pc) -> Optional[Combatant]:
        """Who spends a Spark on ``pc``'s roll: the roller first, else any standing ally
        (one Spark per roll). Returns the spender, having spent it, or None."""
        for c in [pc] + [x for x in self.standing_pcs() if x is not pc]:
            st = self.state[c.id]
            if st.sparks > 0:
                st.sparks -= 1
                st.spend("spark")
                return c
        return None

    def party_has_plan(self) -> bool:
        return getattr(self, "_plan", False)

    def plan_active(self) -> bool:
        """Master Plan: advantage on attacks and saves in the plan's first rounds."""
        return self.party_has_plan() and self.round <= getattr(self, "_plan_rounds", 1)

    # ------------------------------------------------------------ PC weapon attacks
    def weapon_attack(self, pc: Combatant, target: Combatant, weapon: Weapon, *,
                      attack_action: bool, turn: dict, extra: tuple = (),
                      to_hit: Optional[int] = None, mod: Optional[int] = None,
                      dtype: Optional[str] = None) -> bool:
        prof = pc.profile
        st = self.state[pc.id]
        adv = "desperate" in target.conditions or "held" in target.conditions \
            or "entranced" in target.conditions
        if prof.reckless and st.raging and weapon.str_based and not weapon.ranged:
            adv = True
            turn["reckless"] = True
        if turn.pop("study_adv", False) and st.studied is target:
            adv = True
        if weapon.ranged and turn.pop("aim_adv", False):
            adv = True
        if self.plan_active():
            adv = True
        bonus = weapon.to_hit if to_hit is None else to_hit
        if pc.id in self.blessed:
            bonus += combat.roll_damage(self.rng, Dice(1, 4), 0)
        crit_min = weapon.crit_min
        if st.studied is target:
            crit_min = min(crit_min, prof.crit_min_studied)
            m_studied = prof.studied_damage_bonus
        else:
            m_studied = 0
        res = combat.attack_roll(self.rng, bonus, target.ac, advantage=adv, crit_min=crit_min)
        turn["attacks"] = turn.get("attacks", 0) + 1
        # The MM calls the miss (the rule); the party spends when it judges 1d6 can turn it
        # (AI: it knows the foe's AC once it has seen a few attacks).
        if combat.spark_may_spend(succeeded=res.hit, natural=res.natural) \
                and combat.spark_can_turn(total=res.total, target=target.ac):
            sparker = self.spark_holder(pc)
            if sparker is not None:
                res = combat.spark_attack(self.rng, res, ac=target.ac)
        if not res.hit:
            # Graze (edge): once per turn, a two-handed heavy/versatile melee miss still hurts.
            if prof.graze and not weapon.ranged and weapon.heavy_or_versatile \
                    and weapon.two_handed and not turn.get("graze_used"):
                turn["graze_used"] = True
                st.spend("graze")
                self.hurt_foe(pc, target, prof.graze, dtype=dtype or weapon.dtype)
            return False
        crit = res.crit or ("held" in target.conditions and not weapon.ranged)
        m = (weapon.mod if mod is None else mod) + m_studied
        maxed = st.max_next
        if maxed:
            st.max_next = False
            dmg = weapon.dice.count * weapon.dice.sides * (2 if crit else 1) + m
        else:
            dmg = combat.roll_damage(self.rng, weapon.dice, m, crit=crit, min_face=weapon.min_face)
        if st.raging and weapon.str_based and not weapon.ranged:
            dmg += prof.rage.get("damage", 0)
        for g in extra:
            dmg += combat.roll_damage(self.rng, g, 0, crit=crit)
        dmg += self._riders(pc, target, weapon, adv, crit, turn)
        dmg += self._spell_riders(pc, weapon, crit, turn)
        if prof.stun and st.focus >= prof.stun["cost"] and not weapon.ranged \
                and target.role != "minion" and "stunned" not in target.conditions \
                and not turn.get("stun_used"):
            st.focus -= prof.stun["cost"]
            st.spend("focus")
            turn["stun_used"] = True
            if not combat.saving_throw(self.rng, target.saves.get("con", 0), prof.stun["dc"]).success:
                if combat.inflict(target, "stunned", round_no=self.round) != "resisted":
                    target.disabled_by = pc.id  # type: ignore[attr-defined]
        if prof.cleave and not weapon.ranged and weapon.heavy_or_versatile \
                and not turn.get("cleave_used"):
            others = [f for f in self.standing_foes() if f is not target]
            if others:
                turn["cleave_used"] = True
                self.hurt_foe(pc, self.rng.choice(others), prof.cleave, dtype=weapon.dtype)
        if crit and prof.crit_heal:
            self._heal(pc, pc, prof.crit_heal)
        self.hurt_foe(pc, target, dmg, crit=crit, dtype=dtype or weapon.dtype)
        # Sap (edge): once per turn, the creature hit has disadvantage on its next attack roll
        # before the start of your next turn.
        if prof.sap and not turn.get("sap_used") and target.state == "active":
            turn["sap_used"] = True
            target.conditions.add("sapped")
            target.sapped_by = pc.id  # type: ignore[attr-defined]
        return True

    def clear_sap(self, pc: Combatant) -> None:
        """Sap lasts until the start of the sapper's next turn."""
        for f in self.foes:
            if "sapped" in f.conditions and getattr(f, "sapped_by", None) == pc.id:
                f.conditions.discard("sapped")

    def save_disadvantage(self, pc: Combatant) -> bool:
        """Piercing Spell (edge): spend a use so one target saves with disadvantage."""
        st = self.state[pc.id]
        if st.piercing > 0:
            st.piercing -= 1
            st.spend("piercing")
            return True
        return False

    def _riders(self, pc, target, weapon, adv, crit, turn) -> int:
        prof = pc.profile
        st = self.state[pc.id]
        if turn.get("riders", 0) >= prof.rider_limit:
            return 0
        flags = {"has_advantage": adv, "studied_target": st.studied is target,
                 "ally_adjacent_to_target": self.melee_ally_beside(pc), "raging": st.raging}
        wflags = {"finesse": weapon.finesse, "ranged": weapon.ranged, "melee": not weapon.ranged}
        eligible = []
        used = turn.setdefault("riders_used", set())
        for r in prof.riders:
            if r.fallback or (r.once_per_turn and r.name in used):
                continue
            if r.any_of and not any(flags.get(c, False) for c in r.any_of):
                continue
            if r.all_of and not all(flags.get(c, False) for c in r.all_of):
                continue
            if r.weapon and not any(wflags.get(w, False) for w in r.weapon):
                continue
            if r.uses is not None and st.rider_uses.get(r.name, 0) <= 0:
                continue
            eligible.append(r)
        if not eligible:
            fb = [r for r in prof.riders if r.fallback and r.name not in used
                  and (not r.weapon or any(wflags.get(w, False) for w in r.weapon))]
            if not fb:
                return 0
            eligible = fb
        r = max(eligible, key=lambda r: (r.dice.average, r.uses is None))
        if r.uses is not None:
            st.rider_uses[r.name] -= 1
        st.spend(r.name)
        used.add(r.name)
        turn["riders"] = turn.get("riders", 0) + 1
        return combat.roll_damage(self.rng, r.dice, 0, crit=crit)

    def _spell_riders(self, pc, weapon, crit, turn) -> int:
        """Smite spells (bonus action + slot; count as the turn's rider) and Hunter's Mark."""
        prof = pc.profile
        st = self.state[pc.id]
        cst = prof.caster
        if not cst or (st.raging and cst.forbidden_while_raging):
            return 0
        dmg = 0
        if st.aura and st.aura[0].model == "weapon_rider" and st.aura[0].per_hit:
            dmg += _roll(self.rng, [g.times(2) if crit else g for g in st.aura[0].dice])
        if turn.get("riders", 0) >= prof.rider_limit or turn.get("bonus_used") or weapon.ranged:
            return dmg
        smites = [self._spell(n) for n in cst.spells]
        smites = [e for e in smites if e and e.model == "weapon_rider" and not e.per_hit]
        if not smites:
            return dmg
        eff = max(smites, key=lambda e: _spells.average(e.dice))
        slot = st.take(st.low_slot(eff.level))
        if slot is None:
            return dmg
        turn["bonus_used"] = True
        turn["riders"] = turn.get("riders", 0) + 1
        groups = _spells.dice_at(eff, slot, prof.level)
        return dmg + _roll(self.rng, [g.times(2) if crit else g for g in groups])

    def attack_action(self, pc: Combatant, turn: dict) -> None:
        prof = pc.profile
        turn["attack_action"] = True
        for _ in range(prof.attacks_per_action):
            t = self.focus_target()
            if t is None:
                return
            self.weapon_attack(pc, t, prof.weapon, attack_action=True, turn=turn)

    # ------------------------------------------------------------ spells
    def castable(self, pc: Combatant, models: tuple, *, action: Optional[str] = None) -> list:
        cst = pc.profile.caster
        st = self.state[pc.id]
        if not cst or (st.raging and cst.forbidden_while_raging):
            return []
        out = []
        for name in list(cst.cantrips) + list(cst.spells):
            eff = self._spell(name)
            if eff is None or eff.kind not in models:
                continue
            if action and eff.action != action:
                continue
            if eff.level > 0 and st.best_slot(eff.level) is None:
                continue
            out.append(eff)
        return out

    def _spell_bonus(self, pc, eff) -> int:
        cst = pc.profile.caster
        b = cst.mod if eff.add_mod else 0
        if eff.level == 0 and eff.model in ("attack", "save"):
            b += cst.cantrip_damage_bonus
        return b + cst.spell_damage_bonus

    def spell_damage_roll(self, pc, eff, slot, *, crit=False) -> int:
        st = self.state[pc.id]
        groups = _spells.dice_at(eff, slot, pc.profile.level)
        if crit:
            groups = tuple(g.times(2) for g in groups)
        maxed = False
        if st.maximize > 0 and eff.level >= 3:
            st.maximize -= 1
            st.spend("maximize")
            maxed = True
        return _roll(self.rng, groups, maxed) + self._spell_bonus(pc, eff)

    def cast_attack(self, pc, eff, slot, target) -> None:
        cst = pc.profile.caster
        beams = _spells.beams_at(eff, slot, pc.profile.level)
        for i in range(beams):
            t = target if target.state == "active" else self.focus_target()
            if t is None:
                return
            adv = "desperate" in t.conditions or "held" in t.conditions
            turn = self._turns.get(pc.id) or {}
            if self.state[pc.id].studied is t and turn.pop("study_adv", False):
                adv = True                      # Study: the next attack roll, spell or weapon
            res = combat.attack_roll(self.rng, cst.attack, t.ac, advantage=adv)
            if res.hit:
                dmg = self.spell_damage_roll(pc, eff, slot, crit=res.crit)
                if i > 0:
                    dmg -= self._spell_bonus(pc, eff) - (cst.mod if eff.add_mod else 0)
                self.hurt_foe(pc, t, dmg, crit=res.crit, dtype=eff.dtype)

    def cast_save(self, pc, eff, slot, targets, *, pierce: bool = True) -> None:
        dmg = self.spell_damage_roll(pc, eff, slot)
        dc = pc.profile.caster.dc
        first = pierce and eff.level > 0
        for t in targets:
            if t.state != "active":
                continue
            dis = first and self.save_disadvantage(pc)
            first = False
            saved = combat.saving_throw(self.rng, t.saves.get(eff.save, 0), dc,
                                        disadvantage=dis).success
            self.hurt_foe(pc, t, combat.damage_after_save(t, dmg, saved=saved,
                                                          half_on_save=eff.half_on_save),
                          dtype=eff.dtype)

    def cast_auto(self, pc, eff, slot) -> None:
        beams = _spells.beams_at(eff, slot, pc.profile.level)
        for i in range(beams):
            t = self.focus_target()
            if t is None:
                return
            dmg = _roll(self.rng, _spells.dice_at(eff, slot)) + eff.plus
            if i == 0:
                dmg += pc.profile.caster.spell_damage_bonus
            self.hurt_foe(pc, t, dmg, dtype=eff.dtype)

    def cast_effect(self, pc, eff, slot, target=None) -> None:
        if eff.kind == "attack":
            self.cast_attack(pc, eff, slot, target or self.focus_target())
        elif eff.kind == "save":
            if eff.targets >= 2:
                self.cast_save(pc, eff, slot, self.area_targets(eff.targets))
            else:
                self.cast_save(pc, eff, slot, [target or self.focus_target()])
        elif eff.kind == "auto":
            self.cast_auto(pc, eff, slot)

    def area_targets(self, n) -> list:
        foes = self.standing_foes()
        self.rng.shuffle(foes)
        return foes[:n]

    def spell_ev(self, pc, eff, slot, t, nfoes=1) -> float:
        cst = pc.profile.caster
        lvl = pc.profile.level
        groups = _spells.dice_at(eff, slot, lvl)
        avg = _spells.average(groups) + self._spell_bonus(pc, eff)
        if eff.kind == "attack":
            p = combat.hit_chance(cst.attack, t.ac)
            return _spells.beams_at(eff, slot, lvl) * p * _spells.average(groups) \
                + p * self._spell_bonus(pc, eff)
        if eff.kind == "auto":
            return _spells.beams_at(eff, slot, lvl) * (_spells.average(groups) + eff.plus)
        if eff.kind in ("save", "aura"):
            n = min(eff.targets, nfoes) if eff.targets >= 2 else 1
            p_fail = min(0.95, max(0.05, (cst.dc - 1 - t.saves.get(eff.save, 0)) / 20))
            return n * avg * (p_fail + (1 - p_fail) * (0.5 if eff.half_on_save else 0))
        return 0.0

    # ------------------------------------------------------------ healing
    def heal_ally(self, pc: Combatant, ally: Combatant, *, bonus_only=False) -> bool:
        st = self.state[pc.id]
        prof = pc.profile
        heals = self.castable(pc, ("heal",), action="bonus" if bonus_only else None)
        if heals:
            eff = max(heals, key=lambda e: (e.targets, e.level))
            slot = st.take(st.low_slot(eff.level))
            if slot is not None:
                amt_bonus = prof.caster.mod if eff.add_mod else 0
                if eff.targets > 1:
                    hurt = sorted([c for c in self.pcs if c.state != "dead"],
                                  key=lambda c: c.hp / c.max_hp)[:eff.targets]
                else:
                    hurt = [ally]
                for i, c in enumerate(hurt):
                    amt = _roll(self.rng, _spells.dice_at(eff, slot)) + amt_bonus
                    if i == 0 and prof.caster.heal_boost:
                        amt += 2 + slot
                    self._heal(pc, c, amt)
                return True
        if st.heal_pool > 0:
            amt = min(st.heal_pool, ally.max_hp - ally.hp)
            if amt > 0:
                st.heal_pool -= amt
                st.spend("heal_pool", amt)
                self._heal(pc, ally, amt)
                return True
        if bonus_only:
            return False
        if st.channel > 0 and prof.heal_touch:
            st.channel -= 1
            st.spend("channel")
            ht = prof.heal_touch
            self._heal(pc, ally, combat.roll_damage(self.rng, ht["dice"], ht["bonus"]))
            return True
        return False

    # ------------------------------------------------------------ the PC's action
    def take_action(self, pc: Combatant, turn: dict) -> None:
        prof = pc.profile
        st = self.state[pc.id]
        foes = self.standing_foes()
        if not foes:
            return
        down = [c for c in self.pcs if c.state in ("down", "stable")]
        if down and self.heal_ally(pc, down[0]):
            return
        # Stabilize (V56): a character who can't heal a dying friend stabilizes it once it
        # has two failed death saves (AI: earlier costs the party too many actions).
        dying = [c for c in self.pcs if c.state == "down" and c.death_failures >= 2]
        if dying and self.opts.stabilize != "none":
            combat.stabilize(self.rng, dying[0], bonus=(prof.abilities.get("wis", 10) - 10) // 2,
                             check=self.opts.stabilize == "check")
            st.spend("stabilize")
            return
        if prof.healer:
            low = [c for c in self.standing_pcs() if c.hp < c.max_hp / 2]
            if low and self.heal_ally(pc, min(low, key=lambda c: c.hp / c.max_hp)):
                return
        focus = self.focus_target()
        atk_ev = self.attack_ev(pc, focus, turn) if focus is not None else 0.0
        if pc.concentrating is None and len(foes) >= 2:
            auras = self.castable(pc, ("aura",), action="action")
            if auras:
                eff = max(auras, key=lambda e: (e.level, e.targets))
                # an aura keeps ticking: worth it if two rounds of it beat one Attack action
                if 2 * self.spell_ev(pc, eff, st.best_slot(eff.level), focus, len(foes)) >= atk_ev:
                    slot = st.take(st.best_slot(eff.level))
                    pc.concentrating, st.aura = eff.name, (eff, slot)
                    return
        if len(foes) >= 3:
            areas = [e for e in self.castable(pc, ("save",), action="action")
                     if e.targets >= 2 and e.level > 0]
            if areas:
                t = foes[0]
                eff = max(areas, key=lambda e: self.spell_ev(pc, e, st.best_slot(e.level), t,
                                                             len(foes)))
                if self.spell_ev(pc, eff, st.best_slot(eff.level), t, len(foes)) >= atk_ev:
                    slot = st.take(st.best_slot(eff.level))
                    self.cast_save(pc, eff, slot, self.area_targets(eff.targets))
                    return
        if pc.concentrating is None and self.control:
            dis = self.castable(pc, ("disable",), action="action")
            total = sum(f.hp for f in foes)
            big = [f for f in foes if f.role == "boss" or f.hp >= 0.4 * total]
            if dis and big:
                t = max(big, key=lambda f: f.hp)
                ok = [e for e in dis if not e.creature_types
                      or any(f"type:{ct}" in t.tags for ct in e.creature_types)]
                if ok:
                    eff = max(ok, key=lambda e: (e.level, e.targets))
                    # S-5: holding the foe for about two of its turns must beat the Attack action
                    p_fail = min(0.95, max(0.05, (pc.profile.caster.dc - 1 - t.saves.get(eff.save, 0)) / 20))
                    if 2 * p_fail * self.foe_turn_value(t) < atk_ev:
                        ok = []
                if ok:
                    slot = st.take(st.best_slot(eff.level))
                    pc.concentrating, st.aura = eff.name, (eff, slot)
                    self.try_disable(pc, eff, t)
                    return
        if pc.concentrating is None and self.round == 1 and len(self.standing_pcs()) >= 3:
            bless = self.castable(pc, ("buff_attack",), action="action")
            if bless:
                eff = bless[0]
                slot = st.take(st.low_slot(eff.level))
                pc.concentrating, st.aura = eff.name, (eff, slot)
                attackers = sorted(self.standing_pcs(),
                                   key=lambda c: -(c.profile.attacks_per_action
                                                   if c.profile.weapon else 0))[:eff.targets]
                self.blessed = {c.id: True for c in attackers}
                return
        self.single_target(pc, turn)

    def attack_ev(self, pc: Combatant, t: Combatant, turn: Optional[dict] = None) -> float:
        """Expected damage of the Attack action against ``t`` (0 without a weapon): hit and
        crit chances (advantage from Study this turn, a plan, a held or desperate target,
        reckless rage), the weapon's damage with its flat bonuses (rage, studied target),
        crit dice, and the biggest rider once if any attack hits."""
        prof = pc.profile
        st = self.state[pc.id]
        w = prof.weapon
        if w is None:
            return 0.0
        studied = st.studied is t
        adv = ("desperate" in t.conditions or "held" in t.conditions
               or "entranced" in t.conditions or self.plan_active()
               or (prof.reckless and st.raging and w.str_based and not w.ranged)
               or bool(turn and turn.get("study_adv") and studied))
        p = combat.hit_chance(w.to_hit, t.ac)
        crit_min = min(w.crit_min, prof.crit_min_studied) if studied else w.crit_min
        pcrit = (21 - crit_min) / 20
        if adv:
            p, pcrit = 1 - (1 - p) ** 2, 1 - (1 - pcrit) ** 2
        per_hit = w.dice.average + w.mod + (prof.studied_damage_bonus if studied else 0)
        if st.raging and w.str_based:
            per_hit += prof.rage.get("damage", 0)
        n = prof.attacks_per_action
        ev = n * (p * per_hit + pcrit * w.dice.average)
        if prof.riders:
            ev += (1 - (1 - p) ** n) * max(r.dice.average for r in prof.riders)
        return ev

    def try_disable(self, pc, eff, t):
        cst = pc.profile.caster
        targets = [t] if eff.targets < 2 else self.area_targets(eff.targets)
        held_any = False
        for i, tt in enumerate(targets):
            dis = i == 0 and self.save_disadvantage(pc)
            if not combat.saving_throw(self.rng, tt.saves.get(eff.save, 0), cst.dc,
                                       disadvantage=dis).success:
                cond = "entranced" if eff.ends_on_damage else "held"
                outcome = combat.inflict(tt, cond, round_no=self.round)
                if outcome != "resisted":
                    tt.disabled_by = pc.id  # type: ignore[attr-defined]
                if outcome == "applied":
                    held_any = True
                    tt.held_by = pc.id  # type: ignore[attr-defined]
                    tt.held_save = (eff.save, cst.dc, eff.repeat_save)  # type: ignore[attr-defined]
                self.state[pc.id].spend("disable_landed")
        if not held_any:
            self.end_concentration(pc)

    def single_target(self, pc: Combatant, turn: dict, *, no_spells=False) -> None:
        prof = pc.profile
        st = self.state[pc.id]
        t = self.focus_target()
        if t is None:
            return
        options = []
        if prof.weapon is not None:
            options.append((self.attack_ev(pc, t, turn), "attack", None, None))
        cst = prof.caster
        if cst and not no_spells and not (st.raging and cst.forbidden_while_raging):
            if st.aura and st.aura[0].sustain == "action" and st.sustain_used_round != self.round:
                eff, slot = st.aura
                options.append((self.spell_ev(pc, eff, slot, t) * 1.2, "sustain", eff, slot))
            for eff in self.castable(pc, ("attack", "save", "auto", "weapon_cantrip"),
                                     action="action"):
                if eff.targets >= 2 and eff.level > 0:
                    continue
                if eff.concentration and pc.concentrating is not None:
                    continue
                if eff.kind == "weapon_cantrip":
                    if prof.weapon is None and eff.name == "True Strike":
                        continue
                    w = prof.weapon
                    extra = _spells.average(_spells.cantrip_extra(eff, prof.level))
                    ev = combat.hit_chance(cst.attack, t.ac) * (w.dice.average + cst.mod + extra)
                    options.append((ev, "true_strike", eff, 0))
                    continue
                slot = 0 if eff.level == 0 else st.best_slot(eff.level)
                if eff.level > 0 and self.round > 2:
                    continue
                ev = self.spell_ev(pc, eff, slot, t)
                if eff.level > 0:
                    ev *= 0.75
                options.append((ev, "spell", eff, slot))
        if prof.channel_damage and st.channel > 0 and cst:
            cd = prof.channel_damage
            p_fail = min(0.95, max(0.05, (cst.dc - 1 - t.saves.get(cd["save"], 0)) / 20))
            ev = (cd["dice"].average + cd["bonus"]) * (p_fail + (1 - p_fail) * 0.5) * 0.7
            options.append((ev, "channel", None, None))
        if not options:
            return
        ev, kind, eff, slot = max(options, key=lambda o: o[0])
        if kind == "attack":
            self.attack_action(pc, turn)
        elif kind == "sustain":
            st.sustain_used_round = self.round
            self.cast_effect(pc, eff, slot, t)
        elif kind == "true_strike":
            w = prof.weapon
            self.weapon_attack(pc, t, w, attack_action=False, turn=turn,
                               extra=_spells.cantrip_extra(eff, prof.level),
                               to_hit=cst.attack, mod=cst.mod, dtype=eff.dtype)
        elif kind == "channel":
            cd = prof.channel_damage
            st.channel -= 1
            st.spend("channel")
            dmg = combat.roll_damage(self.rng, cd["dice"], cd["bonus"])
            saved = combat.saving_throw(self.rng, t.saves.get(cd["save"], 0), cst.dc).success
            self.hurt_foe(pc, t, combat.damage_after_save(t, dmg, saved=saved,
                                                          half_on_save=cd["half"]),
                          dtype=cd["dtype"])
        else:
            if eff.level > 0:
                slot = st.take(slot)
            if eff.concentration:
                pc.concentrating, st.aura = eff.name, (eff, slot)
                st.sustain_used_round = self.round
            self.cast_effect(pc, eff, slot or 0, t)

    # ------------------------------------------------------------ bonus actions
    def bonus_before(self, pc: Combatant, turn: dict) -> None:
        prof = pc.profile
        st = self.state[pc.id]
        if prof.second_wind and st.second_wind > 0 and pc.hp < pc.max_hp / 2:
            st.second_wind -= 1
            st.spend("second_wind")
            sw = prof.second_wind
            self._heal(pc, pc, combat.roll_damage(self.rng, sw["dice"], sw["bonus"]))
            turn["bonus_used"] = True
            return
        down = [c for c in self.pcs if c.state in ("down", "stable")]
        if down and self.heal_ally(pc, down[0], bonus_only=True):
            turn["bonus_used"] = True
            return
        if prof.rage and not st.raging and st.rage > 0:
            st.rage -= 1
            st.spend("rage")
            st.raging = True
            turn["bonus_used"] = True
            return
        t = self.focus_target()
        if prof.study and st.study > 0 and t is not None and st.studied is not t:
            st.study -= 1
            st.spend("study")
            st.studied = t
            turn["study_adv"] = True
            turn["bonus_used"] = True
            return
        if prof.aim and prof.weapon is not None and prof.weapon.ranged:
            turn["aim_adv"] = True
            turn["bonus_used"] = True
            return
        if st.aura and st.aura[0].sustain == "bonus" and st.sustain_used_round != self.round \
                and pc.concentrating == st.aura[0].name:
            eff, slot = st.aura
            st.sustain_used_round = self.round
            self.cast_effect(pc, eff, slot, t)
            turn["bonus_used"] = True
            return
        if pc.concentrating is None and prof.caster:
            bon = [e for e in self.castable(pc, ("attack", "save", "weapon_rider"), action="bonus")
                   if e.concentration and e.level > 0]
            if prof.weapon is None or prof.weapon.ranged:
                bon = [e for e in bon if not (e.model == "weapon_rider" and prof.weapon is None)]
            if bon:
                eff = max(bon, key=lambda e: (e.level, _spells.average(e.dice)))
                slot = st.take(st.best_slot(eff.level))
                pc.concentrating, st.aura = eff.name, (eff, slot)
                if eff.model != "weapon_rider":
                    st.sustain_used_round = self.round
                    self.cast_effect(pc, eff, slot, t)
                turn["bonus_used"] = True

    def bonus_after(self, pc: Combatant, turn: dict) -> None:
        prof = pc.profile
        st = self.state[pc.id]
        if turn.get("bonus_used") or not turn.get("attack_action"):
            return
        if prof.bonus_attack is None and not prof.flurry:
            return
        n = 1
        if prof.flurry and st.focus >= prof.flurry["cost"]:
            st.focus -= prof.flurry["cost"]
            st.spend("focus")
            n = prof.flurry["count"]
        w = prof.bonus_attack or Weapon("unarmed strike", Dice(1, 4), prof.weapon.to_hit,
                                        prof.weapon.mod)
        for _ in range(n):
            t = self.focus_target()
            if t is None:
                return
            self.weapon_attack(pc, t, w, attack_action=False, turn=turn)
        turn["bonus_used"] = True

    # ------------------------------------------------------------ turns
    def guard_step(self, maker: Combatant) -> None:
        """Clockwork Guardian acts right after its maker (E2): it steps beside one ally —
        the standing PC with the lowest share of its HP — and Guards it until the maker's
        next turn. The Guard covers only that ally (within 5 feet of the construct)."""
        up = self.standing_pcs()
        self.guard_ready[maker.id] = False
        if not up:
            return
        ward = min(up, key=lambda c: (c.hp / max(1, c.max_hp), c.max_hp))
        self.guard_ward[maker.id] = ward.id
        self.guard_ready[maker.id] = True

    def pc_turn(self, pc: Combatant) -> None:
        if pc.profile.guard:
            self.guard_ready[pc.id] = False      # last round's Guard ends as the maker's turn begins
        self._pc_turn(pc)
        if pc.profile.guard and self.over() is None:
            self.guard_step(pc)

    def _pc_turn(self, pc: Combatant) -> None:
        st = self.state[pc.id]
        self.clear_sap(pc)
        if pc.state == "down":
            combat.death_save(self.rng, pc, advantage=pc.profile.death_save_advantage)
            return
        if pc.state != "active":
            return
        if not combat.begin_turn(pc):
            return
        pc.conditions.discard("shielded")
        turn = {}
        self._turns[pc.id] = turn
        self.bonus_before(pc, turn)
        self.take_action(pc, turn)
        if st.action_surge > 0 and self.standing_foes():
            st.action_surge -= 1
            st.spend("action_surge")
            self.single_target(pc, turn, no_spells=True)
        self.bonus_after(pc, turn)

    def pick_pc(self, foe: Combatant) -> Optional[Combatant]:
        up = self.standing_pcs()
        if not up:
            return None
        return self.rng.choice(up)

    def foe_turn(self, foe: Combatant) -> None:
        if foe.state != "active":
            return
        n = self._turns_this_round[foe.id] = self._turns_this_round.get(foe.id, 0) + 1
        refresh = combat.boss_turn_refreshes(foe, n, self.opts)
        for cond in ("held", "entranced"):
            if cond in foe.conditions:
                holder = next((c for c in self.pcs if c.id == getattr(foe, "held_by", None)), None)
                if holder is None or holder.concentrating is None or holder.state != "active":
                    foe.conditions.discard(cond)
        if "held" in foe.conditions or "entranced" in foe.conditions:
            self._credit(getattr(foe, "disabled_by", None), self.foe_turn_value(foe))
            save, dc, repeat = foe.held_save  # type: ignore[attr-defined]
            if repeat and combat.saving_throw(self.rng, foe.saves.get(save, 0), dc).success:
                foe.conditions.discard("held")
            return
        if not combat.begin_turn(foe, refresh_reaction=refresh):
            self._credit(getattr(foe, "disabled_by", None), self.foe_turn_value(foe))
            foe.conditions.discard("stunned")   # until the start of the stunner's next turn
            return
        special = getattr(foe, "special", None)
        if special is not None and refresh:
            combat.roll_recharge(self.rng, foe, recharge_min=special.recharge_min)
        if special is not None and getattr(foe, "special_ready", False) and len(self.standing_pcs()) >= 2:
            foe.special_ready = False  # type: ignore[attr-defined]
            ups = self.standing_pcs()
            self.rng.shuffle(ups)
            for pc in ups[:special.targets]:
                full = special.fixed
                saved = self.pc_save(pc, special.save_ability, special.save_dc,
                                     stake=full - combat.damage_after_save(
                                         pc, full, saved=True, half_on_save=special.half_on_save))
                dmg = combat.damage_after_save(pc, full, saved=saved,
                                               half_on_save=special.half_on_save)
                self.attacks_on[pc.id] += 1
                self.hits_on[pc.id] += 1
                self.raw_on[pc.id] += full
                out = self.hurt_pc(pc, dmg, dtype=special.dtype)
                self.taken_on[pc.id] += out.dealt
            return
        for atk in foe.attacks:
            for _ in range(atk.count):
                pc = self.pick_pc(foe)
                if pc is None:
                    return
                self.foe_attack(foe, pc, atk)

    def foe_attack(self, foe, pc, atk) -> None:
        st = self.state[pc.id]
        self.attacks_on[pc.id] += 1
        adv = "desperate" in foe.conditions or (pc.profile.reckless and st.raging)
        dis = False
        anticipator = None
        for other in self.standing_pcs():
            ost = self.state[other.id]
            if other.profile.anticipate and ost.studied is foe and other.reaction_available:
                combat.take_reaction(other)
                ost.spend("anticipate")
                dis, anticipator = True, other
                break
        if "sapped" in foe.conditions:            # Sap (edge): its next attack roll
            foe.conditions.discard("sapped")
            if not dis:
                sapper = getattr(foe, "sapped_by", None)
                p_norm = combat.hit_chance(atk.to_hit, pc.ac)
                self._credit(sapper, atk.fixed * (p_norm - p_norm ** 2))
            dis = True
        ac = pc.ac + (5 if "shielded" in pc.conditions else 0)
        if anticipator is not None and anticipator is not pc:
            p_norm = combat.hit_chance(atk.to_hit, ac)
            p_dis = p_norm ** 2 if not adv else p_norm
            self._credit(anticipator.id, atk.fixed * (p_norm - p_dis))
        res = combat.attack_roll(self.rng, atk.to_hit, ac, advantage=adv, disadvantage=dis)
        if not res.hit:
            return
        # Shield: only if it turns the hit into a miss.
        cst = pc.profile.caster
        if not res.crit and res.total < ac + 5 and "shielded" not in pc.conditions and cst \
                and self._spell("Shield") and "Shield" in cst.spells and pc.reaction_available \
                and st.low_slot(1):
            combat.take_reaction(pc)
            st.take(st.low_slot(1))
            pc.conditions.add("shielded")
            return
        # Parry (edge): reaction, +N AC against this hit. The MM calls "hit" without the
        # total (V46), so a player parries the first hit it can and learns afterwards
        # whether it turned: the sim spends it on the first non-critical hit — after
        # *Shield* (a caster's better reaction) and never with Uncanny Dodge to hand.
        has_shield = bool(cst and "Shield" in cst.spells and st.low_slot(1))
        if pc.profile.parry and not res.crit and pc.reaction_available \
                and not pc.profile.halve_damage and not has_shield:
            combat.take_reaction(pc)
            st.spend("parry")
            if res.total < ac + pc.profile.parry:
                return
        # Turn the Odds: subtract a Spark die when it could turn the hit into a miss.
        if combat.spark_may_spend(succeeded=res.hit, natural=res.natural, subtract=True,
                                  crit=res.crit) and res.total - ac < 6:
            for other in self.standing_pcs():
                ost = self.state[other.id]
                if other.profile.spark_subtract and ost.sparks > 0 \
                        and ost.turned_odds_round != self.round:
                    ost.sparks -= 1
                    ost.spend("spark")
                    ost.turned_odds_round = self.round
                    res = combat.spark_attack(self.rng, res, ac=ac, subtract=True)
                    if not res.hit:
                        if other is not pc:
                            self._credit(other.id, atk.fixed)
                        return
                    break
        dmg = combat.monster_damage(self.rng, atk, crit=res.crit)
        target = pc
        # Guardian: an ally beside the target takes the hit instead, reduced.
        if pc.profile.redirect == 0:
            guards = [g for g in self.standing_pcs() if g is not pc and g.profile.redirect
                      and g.reaction_available and g.hp - max(0, dmg - g.profile.redirect)
                      > g.max_hp * 0.25 and g.hp / g.max_hp > pc.hp / pc.max_hp]
            if guards:
                g = guards[0]
                combat.take_reaction(g)
                self.state[g.id].spend("guardian")
                self._credit(g.id, min(dmg, g.profile.redirect))
                target, dmg = g, max(0, dmg - g.profile.redirect)
        for maker_id, ward_id in self.guard_ward.items():
            if ward_id == pc.id and self.guard_ready.get(maker_id):
                maker = next(c for c in self.pcs if c.id == maker_id)
                self.guard_ready[maker_id] = False
                gd = maker.profile.guard
                cut = min(dmg, combat.roll_damage(self.rng, gd["dice"], gd["bonus"]))
                dmg -= cut
                self.state[maker_id].spend("guard")
                if maker is not target:
                    self._credit(maker_id, cut)
                break
        own = target is pc          # redirected hits count only as the guardian's credit
        if own:
            self.hits_on[pc.id] += 1
            self.raw_on[pc.id] += atk.fixed
        if target.profile.halve_damage and target.reaction_available and dmg > 0:
            combat.take_reaction(target)
            self.state[target.id].spend("halve_damage")
            dmg //= 2
        out = self.hurt_pc(target, dmg, crit=res.crit, dtype=atk.dtype)
        if own:
            self.taken_on[pc.id] += out.dealt

    def aura_tick(self) -> None:
        """Aura spells hurt up to ``targets`` foes once a round (at the enemy phase)."""
        for pc in self.pcs:
            st = self.state[pc.id]
            if not st.aura or pc.concentrating is None or pc.state != "active":
                continue
            eff, slot = st.aura
            if eff.kind == "aura":
                self.cast_save(pc, eff, slot, self.area_targets(eff.targets), pierce=False)

    def enemy_phase(self, *, boss_only=False) -> None:
        if not boss_only:
            self.aura_tick()
        for foe in list(self.foes):
            if self.over() is not None:
                return
            if boss_only:
                if foe.role == "boss":
                    self.foe_turn(foe)
                continue
            for _ in range(combat.turns_in_side_half(foe, self.opts)):
                self.foe_turn(foe)

    def party_phase(self, part: str = "all") -> None:
        """The party's half. ``part``: "all"; "first" — only the first character's turn
        (a boss acts right after it, Table 8–1); "rest" — everyone else."""
        order = [pc for pc in self.pcs if pc.state != "dead"]
        if part == "first":
            order = order[:1]
        elif part == "rest":
            order = order[1:]
        for pc in order:
            if self.over() is not None:
                return
            self.pc_turn(pc)

    # ------------------------------------------------------------ the fight
    def run(self) -> FightResult:
        self.start_hp = [c.hp for c in self.pcs]
        self.setup()
        self._plan = False
        for pc in self.pcs:
            st = self.state[pc.id]
            if st.master_plan > 0:
                st.master_plan -= 1
                st.spend("master_plan")
                self._plan = True
                self._plan_rounds = pc.profile.master_plan_rounds
                break
        party_mods = [c.dex_mod + c.profile.initiative_bonus for c in self.pcs]
        first = combat.side_initiative(
            self.rng, party_mods, [f.dex_mod for f in self.foes],
            surprised=self.encounter.surprise,
            party_advantage=any(c.profile.initiative_advantage for c in self.pcs))
        has_boss = any(f.role == "boss" for f in self.foes)
        result = None
        while result is None and self.round < MAX_ROUNDS:
            self.round += 1
            self._turns_this_round = {}
            order = combat.round_order(first, self.opts, enemy_has_boss=has_boss,
                                       round_no=self.round, surprised=self.encounter.surprise)
            for phase in order:
                if phase == "boss":
                    self.enemy_phase(boss_only=True)
                elif phase == "party":
                    self.party_phase()
                elif phase == "party_first":
                    self.party_phase("first")
                elif phase == "party_rest":
                    self.party_phase("rest")
                else:
                    self.enemy_phase()
                result = self.over()
                if result is not None:
                    break
        dead = {c.id for c in self.pcs if c.state == "dead"}
        spent = {}
        for st in self.state.values():
            for k, v in st.spent.items():
                spent[k] = spent.get(k, 0) + v
        return FightResult(won=bool(result), rounds=self.round, dropped=set(self.dropped),
                           dead=dead, damage_by_pc=dict(self.damage_by_pc),
                           resources_spent=spent,
                           party_hp_lost=sum(max(0, self.start_hp[i] - c.hp)
                                             for i, c in enumerate(self.pcs)),
                           party_hp_max=sum(c.max_hp for c in self.pcs),
                           party_hp_start=sum(self.start_hp),
                           foes_broken=sum(f.state == "broken" for f in self.foes),
                           foes_killed=sum(f.state == "dead" for f in self.foes),
                           timed_out=result is None,
                           healing_by_pc=dict(self.healing_by_pc),
                           prevented_by_pc=dict(self.prevented_by_pc),
                           selfheal_by_pc=dict(self.selfheal_by_pc),
                           temp_by_pc=dict(self.temp_by_pc),
                           attacks_on=dict(self.attacks_on), hits_on=dict(self.hits_on),
                           raw_on=dict(self.raw_on), taken_on=dict(self.taken_on),
                           end_hp=[c.hp for c in self.pcs],
                           end_state=[c.state for c in self.pcs],
                           used=[self.state[c.id].used() for c in self.pcs],
                           slots_used=[self.state[c.id].slots_used() for c in self.pcs],
                           sparks_left=[self.state[c.id].sparks for c in self.pcs])


_BOOK = None


def _default_book() -> dict:
    global _BOOK
    if _BOOK is None:
        from . import data
        _BOOK = _spells.book(data.load())
    return _BOOK


def run_fight(rng, party: list, encounter: Encounter, opts: RuleOptions = RuleOptions(),
              resource_share: float = DEFAULT_SHARE, **kw) -> FightResult:
    return Fight(rng, party, encounter, opts, resource_share, **kw).run()


def simulate(party: list, encounter: Encounter, *, n: int = 1000, seed: int = 1,
             opts: RuleOptions = RuleOptions(), resource_share: float = DEFAULT_SHARE,
             start_hp_frac: float = 1.0) -> SimSummary:
    """Run one fight ``n`` times from one seed. Deterministic for a given seed.

    ``resource_share``: the fraction of each long-rest pool this fight may use (default
    one of four Clashes). ``start_hp_frac``: the party enters at this fraction of max HP
    (the "tired party" adjustment uses 0.5)."""
    rng = random.Random(seed)
    start = [max(1, int(p.hp * start_hp_frac)) for p in party] if start_hp_frac < 1 else None
    results = [run_fight(rng, party, encounter, opts, resource_share, start_hp=start)
               for _ in range(n)]
    return summarise(results)


def summarise(results: list) -> SimSummary:
    n = len(results)
    rounds = [r.rounds for r in results]
    hist = {}
    for r in rounds:
        hist[r] = hist.get(r, 0) + 1
    dpr = {}
    for r in results:
        for pid, dmg in r.damage_by_pc.items():
            dpr.setdefault(pid, []).append(dmg / max(1, r.rounds))
    spent = {}
    for r in results:
        for k, v in r.resources_spent.items():
            spent[k] = spent.get(k, 0) + v / n
    return SimSummary(
        n=n,
        win_rate=sum(r.won for r in results) / n,
        mean_rounds=statistics.fmean(rounds),
        p_any_drop=sum(bool(r.dropped) for r in results) / n,
        p_death=sum(bool(r.dead) for r in results) / n,
        mean_hp_lost_frac=statistics.fmean(r.party_hp_lost / r.party_hp_max for r in results),
        dpr_by_pc={k: statistics.fmean(v) for k, v in dpr.items()},
        resources_spent=spent,
        rounds_hist=dict(sorted(hist.items())),
    )


# ================================================================ the adventuring day


@dataclass
class DayResult:
    fights: list                  # FightResult per fight fought
    survived: bool                # the party won every fight
    deaths: int
    rounds: int


class _DayPC:
    """A PC's pools, HP, Hit Dice and Sparks across a day."""

    def __init__(self, prof: CombatProfile):
        self.prof = prof
        self.pools = pools(prof)
        self.left = {k: u.uses for k, u in self.pools.items()}
        self.slots = list(prof.caster.slots) if prof.caster else []
        self.hp = prof.hp
        self.hd = prof.level
        self.sparks = 0
        self.dead = False

    def allowance(self, fights_left: int, short_rest_next: bool) -> tuple:
        """Pace daily pools evenly over the fights left (S-5); short-rest pools are spent
        freely when a short rest comes before the next fight."""
        allow = {}
        for k, u in self.pools.items():
            if u.recharge == "short":
                allow[k] = self.left[k]
            else:
                allow[k] = min(self.left[k], math.ceil(self.left[k] / fights_left))
        slots = [min(n, math.ceil(n / fights_left)) for n in self.slots]
        return allow, slots

    def after_fight(self, res: FightResult, i: int) -> None:
        for k, v in res.used[i].items():
            self.left[k] = max(0, self.left[k] - v)
        self.slots = [max(0, a - b) for a, b in zip(self.slots, res.slots_used[i])]
        self.hp = res.end_hp[i]
        self.sparks = res.sparks_left[i]
        if res.end_state[i] == "dead":
            self.dead = True
        elif self.hp <= 0:
            self.hp = 1   # stabilised and patched up after the fight

    def short_rest(self, rng, hd_bonus: int) -> None:
        for k, u in self.pools.items():
            if u.recharge == "short":
                self.left[k] = u.uses
            elif u.short_regain:
                self.left[k] = min(u.uses, self.left[k] + u.short_regain)
        con = (self.prof.abilities.get("con", 10) - 10) // 2
        die = self.prof.hit_die
        while self.hd > 0 and self.prof.hp - self.hp >= (die + 1) / 2 + con + hd_bonus:
            self.hd -= 1
            face = die if self.prof.hd_max else rng.randint(1, die)   # Hale (edge): the maximum
            self.hp = min(self.prof.hp, self.hp + max(1, face + con) + hd_bonus)


def run_day(rng, party: list, encounters: list, *, opts: RuleOptions = RuleOptions(),
            short_rests_after: tuple = (1, 2)) -> DayResult:
    """Fight ``encounters`` in order with short rests after the listed fights (1-based).

    Default: short rests after the first and second fight (the yaml's adventuring_day:
    three Clashes, V34). HP, daily pools, Hit Dice and Sparks carry over; pools are paced
    evenly."""
    day = [_DayPC(p) for p in party]
    fights = []
    for k, enc in enumerate(encounters, start=1):
        alive = [i for i, d in enumerate(day) if not d.dead]
        if not alive:
            break
        members = [party[i] for i in alive]
        allows = [day[i].allowance(len(encounters) - k + 1, k in short_rests_after)
                  for i in alive]
        res = Fight(rng, members, enc, opts, allowances=allows,
                    start_hp=[day[i].hp for i in alive],
                    start_sparks=[day[i].sparks for i in alive]).run()
        # map results back to the full party order
        for j, i in enumerate(alive):
            day[i].after_fight(res, j)
        res.members = alive  # type: ignore[attr-defined]
        fights.append(res)
        if not res.won:
            break
        if k in short_rests_after:
            bonus = max((p.hd_bonus for p in party), default=0)
            for d in day:
                if not d.dead:
                    d.short_rest(rng, bonus)
    return DayResult(fights=fights, survived=len(fights) == len(encounters) and all(
        f.won for f in fights), deaths=sum(d.dead for d in day),
        rounds=sum(f.rounds for f in fights))


# ================================================================ single-character damage


def damage_per_round(profile: CombatProfile, *, ac: int, rounds: int = 3, n: int = 2000,
                     seed: int = 1, foes: int = 1, resource_share: float = DEFAULT_SHARE,
                     ally: bool = True) -> float:
    """Mean damage per round a character deals to dummies that never fight back.

    Dummies: ``ac``, huge HP, +2 on every save, never break. ``foes`` dummies stand, so
    area spells count. ``ally`` puts a passive melee ally beside the target. Control
    spells are off (a dummy can't be controlled into doing less)."""
    from .monsters import MonsterBlock
    dummy = MonsterBlock("dummy", "Dummy", Fraction(0), ac, 10_000, (),
                         {"str": 2, "dex": 2, "con": 2, "int": 2, "wis": 2, "cha": 2},
                         morale="never", source="engine")
    rng = random.Random(seed)
    total = 0.0
    buddy_prof = CombatProfile(name="ally", level=profile.level, prof=2, hp=10_000, ac=30,
                               saves={}, dex_mod=-10,
                               weapon=Weapon("club", Dice(1, 4), 0, 0))
    for _ in range(n):
        party = [profile] + ([buddy_prof] if ally else [])
        fight = Fight(rng, party, Encounter.of(FoeSpec(dummy, count=foes)), RuleOptions(),
                      resource_share, control=False)
        fight.setup()
        me = fight.pcs[0]
        for r in range(rounds):
            fight.round = r + 1
            fight.pc_turn(me)
            fight.aura_tick()
        total += fight.damage_by_pc[me.id] / rounds
    return total / n
