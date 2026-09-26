"""Casting (PHB II.3, DESIGN §1 "Magic").

    Domain + Intent + Scope, cast with the tradition's stat (+1 knack).
    Scope sets difficulty, Fatigue, minimum level and harm (facet.yaml
    `magic.scopes`). Signature workings are one step Easier; a Wider Domain
    is one step Harder until improved; a prismatic domain is always Harder.
    Heavy armor adds Fatigue to a full working; Arcane Mastery and an
    improved casting talent (once per scene) take it away. Fatigue fills
    slots: no free slot, no full working. 7-9 offers two costs from
    `magic_complications`; 6- rolls `magic_mishaps` and the Graceful Fail
    applies. A lineage gift casts Minor workings only, for free.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field
from typing import Optional, Sequence

from app.game.engine import RollResult, resolve_roll, roll_expr, roll_result_to_dict

HARM_INTENT = "harm"
#: PHB II.5 ruling: a lineage gift's Minor workings are cast with Soul.
GIFT_STAT = "soul"


@dataclass
class CastPlan:
    domain: str
    scope: str
    stat: str
    difficulty: str
    fatigue: int
    signature: bool
    gift: bool
    steps: list[str] = field(default_factory=list)      # why the difficulty/Fatigue moved
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class CastResult:
    plan: CastPlan
    roll: Optional[RollResult]
    intent: str
    outcome: str
    fatigue_paid: int
    damage_dice: list[int]
    damage_bonus: int
    raw_damage: int
    damage: int
    complication_table: Optional[str] = None
    complication_options: list[dict] = field(default_factory=list)
    mishap_table: Optional[str] = None
    mishap: Optional[dict] = None
    graceful_fail_applies: bool = False
    enemy_result: Optional[dict] = None
    enemy_results: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["roll"] = roll_result_to_dict(self.roll) if self.roll else None
        return d


def _domain_step(ruleset, character, domain_id: str) -> tuple[int, Optional[str]]:
    """Difficulty step for which of the caster's domains this is."""
    dom = ruleset.get_domain(domain_id)
    m = character.magic
    if dom is None or m is None or domain_id not in m.domains:
        return 0, None
    if dom.prismatic:
        return ruleset.magic.prismatic_step, "prismatic domain: one step Harder"
    if m.domains.index(domain_id) > 0:
        wd = character.talent("wider_domain")
        if not (wd and wd.improved):
            return ruleset.magic.wider_domain_step, "Wider Domain: one step Harder"
    return 0, None


def plan_cast(ruleset, character, *, domain: str, scope: str, working: Optional[str] = None,
              signature: Optional[bool] = None, reduce_fatigue: bool = False,
              miracle: bool = False) -> CastPlan:
    """Work out a casting's stat, difficulty and Fatigue without rolling.

    Args:
        working: the working's name; if it is one of the caster's signature
            workings it is one step Easier (and Arcane Mastery may apply).
        signature: force the signature step on/off (default: from `working`).
        reduce_fatigue: spend the improved casting talent's once-per-scene -1.
        miracle: spend Miracle (once per session) on a Major working: no Fatigue.
    """
    errors: list[str] = []
    steps: list[str] = []
    mg = ruleset.magic
    try:
        sc = mg.get_scope(scope)
    except ValueError as e:
        return CastPlan(domain, scope, "", "Standard", 0, False, False, errors=[str(e)])
    dom = ruleset.get_domain(domain)
    if dom is None:
        return CastPlan(domain, scope, "", "Standard", 0, False, False,
                        errors=[f"Unknown domain {domain!r}."])
    stat = mg.traditions[dom.tradition].stat
    gift = False
    m = character.magic
    if m is not None and domain in m.domains:
        pass
    elif character.gift_domain == domain and character.gifted:
        gift = True
        stat = GIFT_STAT
        if scope != mg.lineage_gift_scope:
            errors.append(f"A lineage gift casts {mg.lineage_gift_scope.title()} workings only.")
    else:
        errors.append(f"{character.name} holds no {dom.name} domain.")
    if character.level < sc.min_level:
        errors.append(f"{sc.label} workings need level {sc.min_level}.")

    if signature is None:
        signature = bool(m and working and working in m.signature_workings)
    if gift:
        signature = False
    diff = sc.difficulty
    if signature:
        diff = ruleset.shift_difficulty(diff, mg.signature_step)
        steps.append("signature working: one step Easier")
    dstep, why = _domain_step(ruleset, character, domain)
    if dstep:
        diff = ruleset.shift_difficulty(diff, dstep)
        steps.append(why)

    fatigue = 0 if gift else sc.fatigue
    if fatigue > 0 and (character.equipped.get("armor") == "heavy"):
        fatigue += mg.heavy_armor_extra_fatigue
        steps.append(f"heavy armor: +{mg.heavy_armor_extra_fatigue} Fatigue")
    if (fatigue > 0 and character.signature == "arcane_mastery" and working
            and working == (character.arcane_mastery_working or (m.signature_workings[0] if m and m.signature_workings else None))):
        fatigue -= 1
        steps.append("Arcane Mastery: -1 Fatigue")
    if reduce_fatigue:
        casting = next((t for t in character.talents
                        if (tdef := ruleset.get_talent(t.id)) and tdef.effects.get("grants_tradition")),
                       None)
        if casting is None or not casting.improved:
            errors.append("Reducing Fatigue needs an improved casting talent.")
        elif not character.uses_remaining(ruleset, casting.id, period="scene"):
            errors.append("The improved casting talent's reduction is spent this scene.")
        elif fatigue > 0:
            fatigue -= 1
            steps.append("improved casting talent: -1 Fatigue")
    if miracle:
        if character.signature != "miracle":
            errors.append("Only a Miracle signature casts a Major working for free.")
        elif scope != "major":
            errors.append("Miracle is for a Major working.")
        elif not character.uses_remaining(ruleset, "miracle"):
            errors.append("Miracle is spent this session.")
        else:
            fatigue = 0
            steps.append("Miracle: no Fatigue")
    fatigue = max(0, fatigue)
    if fatigue and mg.fatigue_takes_slot and fatigue > character.slots_free(ruleset):
        errors.append(f"No free slot for {fatigue} Fatigue: no full working.")
    return CastPlan(domain=domain, scope=scope, stat=stat, difficulty=diff, fatigue=fatigue,
                    signature=signature, gift=gift, steps=steps, errors=errors)


def resolve_cast(
    ruleset,
    character,
    *,
    domain: str,
    scope: str,
    intent: str = "",
    working: Optional[str] = None,
    signature: Optional[bool] = None,
    reduce_fatigue: bool = False,
    miracle: bool = False,
    knack: bool = False,
    sparks: int = 0,
    help: int = 0,
    borrowed_trouble: bool = False,
    enemy=None,
    enemies: Optional[list] = None,
    dice: Optional[Sequence[int]] = None,
    damage_dice: Optional[Sequence[int]] = None,
    rng: Optional[random.Random] = None,
    apply: bool = True,
) -> CastResult:
    """Cast a working: plan it, roll it, pay Fatigue, and resolve harm.

    Fatigue is paid whatever the roll (the working was attempted). A harm
    intent at Significant/Major scope rolls the scope's damage (+ the level
    damage bonus) on a 7+; against `enemy` armor applies and the hit lands.
    A Major harm working rolls once and every foe in `enemies` takes that
    amount minus its own armor (`enemy_results` holds one entry per foe).
    Minor never deals damage (in a fight it is a stunt).

    Raises:
        ValueError: the plan has errors, or more Sparks than the caster holds.
    """
    from app.game.combat import apply_armor, apply_damage_to_enemy
    from app.game.toolbox import roll_distinct, roll_table

    plan = plan_cast(ruleset, character, domain=domain, scope=scope, working=working,
                     signature=signature, reduce_fatigue=reduce_fatigue, miracle=miracle)
    if not plan.ok:
        raise ValueError("; ".join(plan.errors))
    if character.status != "ok":
        raise ValueError(f"{character.name} is in no state to cast.")
    if sparks > character.sparks:
        raise ValueError(f"{character.name} has only {character.sparks} Spark(s).")
    roll = resolve_roll(ruleset, stat_value=character.stats.get(plan.stat, 0), stat=plan.stat,
                        knack=knack, difficulty=plan.difficulty, sparks=sparks, help=help,
                        borrowed_trouble=borrowed_trouble, dice=dice, rng=rng, kind="cast",
                        description=intent)
    sc = ruleset.magic.get_scope(scope)
    dmg_dice: list[int] = []
    raw = dmg = 0
    bonus = 0
    enemy_result = None
    is_harm = intent.strip().lower().startswith(HARM_INTENT)
    group_results: list[dict] = []
    if enemies and (sc.targets != "group"):
        raise ValueError(f"A {sc.label} working strikes one target; only a group scope takes `enemies`.")
    if roll.succeeded and is_harm and sc.damage:
        dmg_dice, total = roll_expr(sc.damage, rng, damage_dice)
        bonus = character.damage_bonus(ruleset)
        raw = total + bonus
        dmg = raw
        if enemy is not None:
            dmg = apply_armor(ruleset, raw, enemy.armor)
            if apply:
                enemy_result = apply_damage_to_enemy(ruleset, enemy, dmg).to_dict()
        for foe in enemies or []:
            if foe is enemy or foe.defeated:
                continue
            each = apply_armor(ruleset, raw, foe.armor)
            if apply:
                group_results.append(apply_damage_to_enemy(ruleset, foe, each).to_dict())
            else:
                group_results.append({"enemy": foe.key or foe.id, "damage": each})

    result = CastResult(plan=plan, roll=roll, intent=intent, outcome=roll.outcome,
                        fatigue_paid=plan.fatigue, damage_dice=dmg_dice, damage_bonus=bonus,
                        raw_damage=raw, damage=dmg, enemy_result=enemy_result,
                        enemy_results=group_results)
    mg = ruleset.magic
    if roll.outcome == "partial_success":
        result.complication_table = mg.complication_table
        if ruleset.get_table(mg.complication_table):
            result.complication_options = roll_distinct(ruleset, mg.complication_table, 2, rng=rng)
    elif roll.outcome == "failure":
        result.mishap_table = mg.mishap_table
        result.graceful_fail_applies = True
        if ruleset.get_table(mg.mishap_table):
            result.mishap = roll_table(ruleset, mg.mishap_table, rng=rng)

    if apply:
        character.sparks -= sparks
        if plan.fatigue:
            character.fatigue += plan.fatigue
        if reduce_fatigue:
            casting = next(t for t in character.talents
                           if (tdef := ruleset.get_talent(t.id)) and tdef.effects.get("grants_tradition"))
            character.use_talent(ruleset, casting.id, period="scene")
        if miracle:
            character.use_talent(ruleset, "miracle")
    return result
