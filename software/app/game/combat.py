"""Combat rules (PHB III.3, DESIGN §1 "Combat, per exchange").

This module is the ONLY implementation of combat rules. The WebSocket layer
and the simulator (`tools/combat_sim.py`) call these functions; neither may
carry its own copy of a rule (CLAUDE.md).

    Attack: 2d6 + Body (+knack). 10+ weapon die and pick one (+1d6 damage ·
    stunt · cover); 7-9 weapon die and you are exposed; 6- miss, MM move.
    Enemies roll in the open: 2d6 + attack. 10+ hard hit (+2 damage), 7-9
    hit, 6- miss; natural 12 something more, natural 2 an opening. Armor
    subtracts (min 1). Defend / cover / Warding Presence make attacks Hard;
    exposure adds a die (keep best two). Mooks drop to any hit and attack as
    a mob. Bloodied at half HP. Morale: 2d6 over the foe's morale breaks it.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field
from typing import Optional, Sequence

from app.game.engine import RollResult, resolve_roll, roll_expr, roll_result_to_dict

# ---------------------------------------------------------------------------
# Small pure rules
# ---------------------------------------------------------------------------


def level_gap_difficulty(ruleset, attacker_level: int, foe_level: int) -> str:
    """Your attacks on a foe 3+ levels above you are Hard, 6+ Very Hard."""
    gap = foe_level - attacker_level
    label = "Standard"
    for step in sorted(ruleset.combat.level_gap, key=lambda s: s.gap):
        if gap >= step.gap:
            label = step.difficulty
    return label


def mob_bonus(ruleset, count: int) -> int:
    """+1 damage per extra Mook in a mob, capped (+4)."""
    if count < 1:
        raise ValueError("A mob has at least one Mook.")
    role = ruleset.monsters.roles["mook"]
    return min((count - 1) * role.mob_damage_per_extra, role.mob_damage_cap)


def apply_armor(ruleset, damage: int, armor: int, pierce: int = 0, ignore: bool = False) -> int:
    """Armor subtracts from damage, never below the minimum (1)."""
    if damage <= 0:
        return 0
    effective = 0 if ignore else max(0, min(armor, ruleset.combat.armor.cap) - pierce)
    return max(ruleset.combat.armor.minimum_damage, damage - effective)


# ---------------------------------------------------------------------------
# Exchange state
# ---------------------------------------------------------------------------

@dataclass
class CombatState:
    """What lasts until the end of the exchange (DESIGN §1 step 5)."""

    exchange: int = 1
    exposed: dict[str, list[str]] = field(default_factory=dict)   # pc -> enemy keys (or ["*"])
    defending: dict[str, Optional[list[str]]] = field(default_factory=dict)  # pc -> intercepted allies
    covered: dict[str, str] = field(default_factory=dict)         # ally -> who covers them
    warded: set[str] = field(default_factory=set)                  # PCs a Warding Presence protects
    telegraphs: dict[str, str] = field(default_factory=dict)       # enemy key -> intent text

    def expose(self, pc: str, enemy_key: Optional[str] = None) -> None:
        self.exposed.setdefault(pc, []).append(enemy_key or "*")

    def is_exposed_to(self, pc: str, enemy_key: str) -> bool:
        keys = self.exposed.get(pc, [])
        return "*" in keys or enemy_key in keys

    def consume_exposure(self, pc: str, enemy_key: str) -> bool:
        """Exposure applies to that foe's NEXT attack on you this exchange."""
        keys = self.exposed.get(pc, [])
        for k in (enemy_key, "*"):
            if k in keys:
                keys.remove(k)
                return True
        return False

    def defend(self, pc: str, intercept_for: Optional[list[str]] = None) -> None:
        """Defend (attacks on you are Hard); Intercept also takes attacks aimed at allies."""
        self.defending[pc] = list(intercept_for) if intercept_for else None

    def interceptor_for(self, target: str) -> Optional[str]:
        """Who (if anyone) is intercepting attacks aimed at `target`. "*" means every ally."""
        for pc, allies in self.defending.items():
            if pc == target or not allies:
                continue
            if target in allies or "*" in allies:
                return pc
        return None

    def end_exchange(self) -> int:
        self.exposed.clear()
        self.defending.clear()
        self.covered.clear()
        self.warded.clear()
        self.telegraphs.clear()
        self.exchange += 1
        return self.exchange

    def to_dict(self) -> dict:
        return {"exchange": self.exchange, "exposed": {k: list(v) for k, v in self.exposed.items()},
                "defending": dict(self.defending), "covered": dict(self.covered),
                "warded": sorted(self.warded), "telegraphs": dict(self.telegraphs)}


def expire_exchange_effects(enemy) -> None:
    """End of exchange for a foe: stunt openings ("*") and Studied Foe expire;
    a natural-2 opening, named for its target, lasts until that target uses it."""
    enemy.openings = [o for o in enemy.openings if o != "*"]
    enemy.studied = False


def declare_defend(ruleset, state: CombatState, character,
                   intercept_for: Optional[list[str]] = None) -> dict:
    """A character Defends (no attack; attacks on them are Hard) or Intercepts
    (Defend, and attacks aimed at the named ally come to them). Intercepting
    more than one ally, or everyone ("*"), needs Sentinel.

    Raises:
        ValueError: a downed character, or too many allies without Sentinel.
    """
    if character.status != "ok":
        raise ValueError(f"{character.name} cannot defend now.")
    allies = [a for a in (intercept_for or []) if a != character.name]
    if (len(allies) > 1 or "*" in allies) and not character.has_talent("sentinel"):
        raise ValueError("Intercepting more than one ally needs Sentinel.")
    state.defend(character.name, allies or None)
    return {"defender": character.name, "intercept_for": allies,
            "can_attack": character.has_talent("sentinel", improved=True)}


# ---------------------------------------------------------------------------
# Damage to foes
# ---------------------------------------------------------------------------

@dataclass
class EnemyDamageResult:
    enemy: str
    damage: int
    hp_before: Optional[int]
    hp_after: Optional[int]
    count_before: int
    count_after: int
    mooks_dropped: int
    bloodied_now: bool         # crossed half HP on this hit
    phase_change: bool         # a Boss's Bloodied phase fired
    defeated: bool
    when_bloodied: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def apply_damage_to_enemy(ruleset, enemy, damage: int, *, hit: bool = True,
                          drops: int = 1) -> EnemyDamageResult:
    """Apply a hit to a live foe.

    Mooks drop to any hit (`drops` of them from one hit — Cleave); others lose
    HP. Crossing half HP marks the foe Bloodied (a Boss changes phase).

    Raises:
        ValueError: negative damage, or the foe is already defeated.
    """
    if damage < 0:
        raise ValueError("Damage cannot be negative.")
    if enemy.defeated:
        raise ValueError(f"{enemy.name} is already defeated.")
    count_before = enemy.count
    hp_before = enemy.hp_current
    dropped = 0
    bloodied_now = phase = False
    if enemy.is_mook:
        if hit:
            dropped = min(max(1, drops), enemy.count)
            enemy.count -= dropped
            if enemy.count <= 0:
                enemy.count = 0
                enemy.defeated = True
    else:
        mx = enemy.hp_max(ruleset)
        if enemy.hp_current is None:
            enemy.hp_current = mx
        hp_before = enemy.hp_current
        enemy.hp_current = max(0, enemy.hp_current - damage)
        if not enemy.bloodied and enemy.hp_current <= mx // 2 and enemy.hp_current > 0:
            enemy.bloodied = bloodied_now = True
            if ruleset.monsters.roles[enemy.role].bloodied_phase:
                enemy.phase += 1
                phase = True
        if enemy.hp_current == 0:
            enemy.defeated = True
            if not enemy.bloodied:
                enemy.bloodied = True
    return EnemyDamageResult(
        enemy=enemy.key or enemy.id, damage=damage, hp_before=hp_before,
        hp_after=enemy.hp_current, count_before=count_before, count_after=enemy.count,
        mooks_dropped=dropped, bloodied_now=bloodied_now, phase_change=phase,
        defeated=enemy.defeated, when_bloodied=enemy.when_bloodied if bloodied_now else None)


# ---------------------------------------------------------------------------
# Player attacks
# ---------------------------------------------------------------------------

@dataclass
class AttackResult:
    roll: RollResult
    attacker: str
    target: Optional[str]
    difficulty: str
    tier: str
    hit: bool
    weapon_die: int
    damage_dice: list[int]
    damage_bonus: int
    options: list[str]
    options_allowed: int
    extra_damage_dice: list[int]
    raw_damage: int
    damage: int                 # after armor
    exposed: bool
    mm_move: bool
    opening_used: bool = False
    enemy_result: Optional[EnemyDamageResult] = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["roll"] = roll_result_to_dict(self.roll)
        d["enemy_result"] = self.enemy_result.to_dict() if self.enemy_result else None
        return d


def options_allowed(ruleset, character, brawling: bool = False) -> int:
    """How many 10+ options this attacker picks: 1; 2 with improved Weapon Master
    using the chosen kind, or an improved Brawler's brawling attack."""
    wm = character.talent("weapon_master")
    w = character.equipped_weapon()
    if wm and wm.improved and w is not None and w.kind and w.kind == wm.choice:
        return 2
    if brawling and character.has_talent("brawler", improved=True):
        return 2
    return 1


def resolve_attack(
    ruleset,
    character,
    enemy=None,
    *,
    state: Optional[CombatState] = None,
    difficulty: str = "Standard",
    options: Sequence[str] = (),
    knack: bool = False,
    bonus: int = 0,
    stat: str = "body",
    sparks: int = 0,
    help: int = 0,
    borrowed_trouble: bool = False,
    extra_dice: int = 0,
    brawling: bool = False,
    in_cover: bool = False,
    within_reach: bool = True,
    dice: Optional[Sequence[int]] = None,
    damage_dice: Optional[Sequence[int]] = None,
    extra_damage_roll: Optional[Sequence[int]] = None,
    rng: Optional[random.Random] = None,
    apply: bool = True,
) -> AttackResult:
    """A player character attacks (optionally a live `enemy`).

    Difficulty is the harder of `difficulty`, the level gap, and cover (Hard
    for ranged attacks unless Marksman); an opening on the foe (a natural 2,
    a stunt) or Studied Foe then eases it one step. Sparks are debited.

    `options` are the 10+ picks (from `combat.attack.full_success.pick_one`);
    unknown or too many options raise. `damage_dice` fixes the weapon die
    roll(s) and `extra_damage_roll` the +1d6.

    Raises:
        ValueError: bad option, more Sparks than held, a downed attacker.
    """
    if character.status != "ok" or character.hp_current <= 0:
        raise ValueError(f"{character.name} is in no state to attack.")
    if sparks > character.sparks:
        raise ValueError(f"{character.name} has only {character.sparks} Spark(s).")
    allowed_opts = ruleset.combat.attack.full_success.pick_one
    for o in options:
        if o not in allowed_opts:
            raise ValueError(f"Unknown option {o!r}; choose from {allowed_opts}.")
    if len(set(options)) != len(options):
        raise ValueError("An option can be picked once.")
    n_allowed = options_allowed(ruleset, character, brawling)
    if len(options) > n_allowed:
        raise ValueError(f"Pick at most {n_allowed} option(s).")

    ranged = character.is_ranged(ruleset)
    notes: list[str] = []
    diff = difficulty
    if enemy is not None:
        diff = ruleset.harder_of(diff, level_gap_difficulty(ruleset, character.level, enemy.level))
    if in_cover and ranged:
        if character.has_talent("marksman"):
            notes.append("Marksman ignores cover.")
        else:
            diff = ruleset.harder_of(diff, "Hard")
    opening = False
    if enemy is not None and (character.name in enemy.openings or "*" in enemy.openings
                              or enemy.studied):
        diff = ruleset.shift_difficulty(diff, 1)
        opening = True

    roll = resolve_roll(ruleset, stat_value=character.stats.get(stat, 0), stat=stat,
                        knack=knack, bonus=bonus, difficulty=diff, sparks=sparks, help=help,
                        borrowed_trouble=borrowed_trouble, extra_dice=extra_dice, dice=dice,
                        rng=rng, kind="attack")
    if apply:
        character.sparks -= sparks
        if opening and enemy is not None:
            if character.name in enemy.openings:
                enemy.openings.remove(character.name)
            elif "*" in enemy.openings:
                enemy.openings.remove("*")

    tier = roll.outcome
    die = character.weapon_die(ruleset)
    dmg_bonus = character.damage_bonus(ruleset)
    hit = tier in ("full_success", "partial_success")
    dmg_dice: list[int] = []
    extra: list[int] = []
    exposed = mm_move = False
    chosen = list(options) if tier == "full_success" else []
    if brawling and character.has_talent("brawler") and hit and "stunt" not in chosen:
        chosen.append("stunt")     # Brawler: a brawling hit is also a stunt
        notes.append("Brawler: the hit pins, trips or hurls — a stunt.")
    if hit:
        n_weapon = 2 if (tier == "full_success" and ranged and character.signature == "deadeye") else 1
        dmg_dice, _ = roll_expr(f"{n_weapon}d{die}", rng, damage_dice)
        raw = sum(dmg_dice) + dmg_bonus
        if "extra_damage" in chosen:
            opt = ruleset.combat.options["extra_damage"]
            extra, _ = roll_expr(opt.dice or "1d6", rng, extra_damage_roll)
            raw += sum(extra)
        if tier == "partial_success" and within_reach:
            exposed = True
    else:
        raw = 0
        mm_move = True

    damage = raw
    enemy_result = None
    if enemy is not None and hit:
        pierce = int(character._effect_total(ruleset, "ranged_armor_pierce")) if ranged else 0
        ignore = enemy.studied and character.signature == "anatomist"
        damage = apply_armor(ruleset, raw, enemy.armor, pierce=pierce, ignore=ignore)
        if apply:
            drops = 1
            if enemy.is_mook and character.has_talent("cleave", improved=True):
                drops = 3 if tier == "full_success" else 2
            enemy_result = apply_damage_to_enemy(ruleset, enemy, damage, drops=drops)
            if "stunt" in chosen:
                enemy.openings.append("*")
    if apply and exposed and state is not None:
        state.expose(character.name, enemy.key if enemy is not None else None)

    return AttackResult(
        roll=roll, attacker=character.name, target=(enemy.key or enemy.id) if enemy else None,
        difficulty=diff, tier=tier, hit=hit, weapon_die=die, damage_dice=dmg_dice,
        damage_bonus=dmg_bonus if hit else 0, options=chosen, options_allowed=n_allowed,
        extra_damage_dice=extra, raw_damage=raw, damage=damage, exposed=exposed,
        mm_move=mm_move, opening_used=opening, enemy_result=enemy_result, notes=notes)


# ---------------------------------------------------------------------------
# Enemy attacks
# ---------------------------------------------------------------------------

@dataclass
class EnemyAttackResult:
    enemy: str
    target: Optional[str]
    original_target: Optional[str]
    dice: list[int]
    kept: list[int]
    attack_bonus: int
    difficulty: str
    difficulty_modifier: int
    total: int
    tier: str
    label: str
    hit: bool
    natural_high: bool
    natural_low: bool
    exposure_die: bool
    base_damage: int
    mob_bonus: int
    raw_damage: int
    damage: int
    armor: int
    target_result: Optional[dict] = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_enemy_attack(
    ruleset,
    enemy,
    character=None,
    *,
    state: Optional[CombatState] = None,
    exposed: Optional[bool] = None,
    defending: Optional[bool] = None,
    cover: Optional[bool] = None,
    warded: Optional[bool] = None,
    party: Optional[dict] = None,
    dice: Optional[Sequence[int]] = None,
    rng: Optional[random.Random] = None,
    apply: bool = True,
) -> EnemyAttackResult:
    """An enemy rolls one attack in the open against a character.

    With a `state`, the target is redirected to an interceptor (looked up in
    `party`, {name: Character}; if absent the redirect is only reported), and exposure,
    Defend, cover and Warding are read from it (explicit flags override).
    Defend, cover and Warding each make the roll Hard (they do not stack).
    Exposure adds one die; keep the best two. A natural 2 opens the foe to
    the target's next attack (Easy).

    Raises:
        ValueError: the foe is defeated, or fixed `dice` have the wrong count.
    """
    if enemy.defeated:
        raise ValueError(f"{enemy.name} is defeated.")
    ek = enemy.key or enemy.id
    notes: list[str] = []
    original = character.name if character is not None else None
    target_name = original
    if state is not None and character is not None:
        interceptor = state.interceptor_for(character.name)
        if interceptor:
            notes.append(f"{interceptor} intercepts the attack aimed at {character.name}.")
            target_name = interceptor
    ea = ruleset.combat.enemy_attack
    if exposed is None:
        exposed = bool(state and target_name and state.consume_exposure(target_name, ek)) \
            if apply else bool(state and target_name and state.is_exposed_to(target_name, ek))
    if defending is None:
        defending = bool(state and target_name in state.defending)
    if cover is None:
        cover = bool(state and target_name in state.covered)
    if warded is None:
        warded = bool(state and target_name in state.warded)
    hard = defending or cover or warded
    diff = ruleset.combat.defend.enemy_difficulty if hard else "Standard"
    diff_mod = ruleset.difficulty_modifier(diff)

    n = 2 + (ruleset.combat.exposure.extra_enemy_dice if exposed else 0)
    if dice is not None:
        rolled = list(dice)
        if len(rolled) != n or any(not 1 <= d <= 6 for d in rolled):
            raise ValueError(f"Expected {n} d6 values, got {rolled}.")
    else:
        r = rng or random
        rolled = [r.randint(1, 6) for _ in range(n)]
    kept = sorted(rolled, reverse=True)[:2]
    atk = enemy.attack(ruleset)
    total = sum(kept) + atk + diff_mod
    th = ruleset.roll_resolution.thresholds
    tier = ("full_success" if total >= th.full_success else
            "partial_success" if total >= th.partial_success else "failure")
    nat_high, nat_low = kept == [6, 6], kept == [1, 1]
    if nat_high:
        tier = "full_success"
        notes.append(ea.natural_high)
    if nat_low:
        tier = "failure"
        notes.append(ea.natural_low)
    tier_def = getattr(ea, tier)
    hit = tier_def.hit
    base = enemy.damage(ruleset)
    mb = mob_bonus(ruleset, enemy.count) if enemy.is_mook else 0
    raw = base + mb + tier_def.damage_bonus if hit else 0

    target_char = character
    armor = 0
    if character is not None and target_name != character.name:
        target_char = (party or {}).get(target_name)
    if target_char is not None:
        armor = target_char.armor_value(ruleset)
    damage = apply_armor(ruleset, raw, armor) if hit else 0
    target_result = None
    if apply and target_char is not None and hit:
        target_result = target_char.take_damage(ruleset, damage)
    if apply and nat_low and target_name:
        enemy.openings.append(target_name)
    return EnemyAttackResult(
        enemy=ek, target=target_name, original_target=original, dice=rolled, kept=kept,
        attack_bonus=atk, difficulty=diff, difficulty_modifier=diff_mod, total=total,
        tier=tier, label=tier_def.label, hit=hit, natural_high=nat_high, natural_low=nat_low,
        exposure_die=exposed, base_damage=base if hit else 0, mob_bonus=mb if hit else 0,
        raw_damage=raw, damage=damage, armor=armor, target_result=target_result, notes=notes)


# ---------------------------------------------------------------------------
# Morale
# ---------------------------------------------------------------------------

@dataclass
class MoraleResult:
    enemy: str
    dice: list[int]
    bonus: int
    total: int
    morale: int
    breaks: bool
    fearless: bool
    breaks_text: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def morale_check(ruleset, enemy, *, bonus: int = 0, dice: Optional[Sequence[int]] = None,
                 rng: Optional[random.Random] = None, apply: bool = True) -> MoraleResult:
    """The MM rolls 2d6 (+bonus, e.g. Dread Presence improved +2); over the
    foe's morale it breaks. A fearless foe (morale 12+) never breaks."""
    if enemy.defeated:
        raise ValueError(f"{enemy.name} is defeated.")
    if dice is not None:
        rolled = list(dice)
        if len(rolled) != 2 or any(not 1 <= d <= 6 for d in rolled):
            raise ValueError(f"Morale rolls two d6, got {rolled}.")
    else:
        r = rng or random
        rolled = [r.randint(1, 6), r.randint(1, 6)]
    total = sum(rolled) + bonus
    fearless = enemy.morale >= ruleset.monsters.morale.fearless
    breaks = (not fearless) and total > enemy.morale
    if apply and breaks:
        enemy.broken = True
    return MoraleResult(enemy=enemy.key or enemy.id, dice=rolled, bonus=bonus, total=total,
                        morale=enemy.morale, breaks=breaks, fearless=fearless,
                        breaks_text=enemy.breaks if breaks else "")


def retainer_morale(ruleset, captain) -> int:
    """A Captain's retainers have morale 7 + the Captain's Soul (PHB II.4c).
    Retainers fight as Help on a character's roll; they make no attack rolls."""
    return ruleset.monsters.morale.default + captain.stats.get("soul", 0)


def morale_triggers(ruleset) -> list[str]:
    return list(ruleset.monsters.morale.triggers)
