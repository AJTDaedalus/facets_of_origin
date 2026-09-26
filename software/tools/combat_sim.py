"""Monte Carlo combat simulator for Lean Facets v1.0.

The simulator may only DRIVE the rules — every roll, hit, damage number, Hold
On, morale check and casting goes through `app.game.combat`, `app.game.magic`
and `app.game.character`. It carries no copy of any rule (CLAUDE.md: the v0.3
simulator's private rules copy diverged and invalidated a research corpus).
What lives here is only *policy*: who attacks whom, when a caster casts.

    python -m tools.combat_sim --level 1 --foes "mook:1x4"
    python -m tools.combat_sim --level 5 --foes "standard:5x3,mook:5x2" --trials 2000
    python -m tools.combat_sim --ladder          # the DESIGN §6 pacing ladder

A foe spec is `role:level[xcount]`, comma-separated; `card:<id>` uses a card
from `enemies/`. Mooks with a count fight as one mob.
"""
from __future__ import annotations

import argparse
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.game import combat
from app.game.character import Character, create_character
from app.game.enemy import Enemy
from app.game.magic import plan_cast, resolve_cast

REPO_ROOT = Path(__file__).resolve().parents[2]
FACETS_DIR = REPO_ROOT / "software" / "facets"
ENEMY_DIR = REPO_ROOT / "enemies"
MAX_EXCHANGES = 12

#: The default party: two fighters and two casters, one per class shape.
PARTY = [
    {"name": "Warrior", "facet": "body", "second_stat": "soul", "class_id": "warrior",
     "talent_choices": {"weapon_master": "blades"}, "background_id": "city_watch_veteran",
     "weapon_kind": "blades"},
    {"name": "Scout", "facet": "body", "second_stat": "mind", "class_id": "scout",
     "background_id": "wilderness_scout"},
    {"name": "Thaumaturge", "facet": "mind", "second_stat": "soul", "class_id": "thaumaturge",
     "background_id": "hedge_scholar",
     "magic": {"domain": "constructed_force",
               "signature_workings": ["A force bolt", "A shield of pressure"]}},
    {"name": "Invoker", "facet": "soul", "second_stat": "body", "class_id": "invoker",
     "background_id": "temple_acolyte",
     "magic": {"domain": "fire", "signature_workings": ["A lance of flame", "A wall of fire"]}},
]


def load_ruleset():
    from app.facets.loader import load_facet_file
    from app.facets.registry import MergedRuleset
    return MergedRuleset([load_facet_file(FACETS_DIR / "base" / "facet.yaml")])


# ---------------------------------------------------------------------------
# Building the sides
# ---------------------------------------------------------------------------

def _auto_pick(ruleset, ch: Character) -> dict:
    """A reasonable level-up pick (policy, not rules): the signature at its
    level; otherwise improve a held talent, else take a new one from the menu."""
    new_level = ch.level + 1
    adv = ruleset.advancement
    pick: dict = {}
    if new_level == adv.signature_level:
        klass = ruleset.get_class(ch.class_id or "")
        pick = {"kind": "signature", "talent_id": klass.signature if klass else None}
    else:
        improvable = [t for t in ch.talents if not t.improved]
        if improvable:
            pick = {"kind": "improve", "talent_id": improvable[0].id}
        else:
            for tdef in ruleset.talent_menu(ch.facet):
                if not ch.has_talent(tdef.id) and not tdef.choose and not (
                        tdef.requires and tdef.requires.any_talent):
                    pick = {"kind": "talent", "talent_id": tdef.id}
                    break
    if new_level in adv.stat_increase_levels:
        order = sorted(ch.stats, key=lambda s: -ch.stats[s])
        pick["stat"] = next(s for s in order
                            if ch.stats[s] < ruleset.stat_rules.maximum)
    if ch.magic is not None and new_level in adv.signature_working_levels:
        pick["signature_working"] = f"Working {len(ch.magic.signature_workings) + 1}"
    return pick


def build_character(ruleset, spec: dict, level: int) -> Character:
    ch, errors = create_character(
        ruleset, name=spec["name"], player_name=spec["name"], facet=spec["facet"],
        second_stat=spec["second_stat"], class_id=spec["class_id"],
        background_id=spec.get("background_id"), talent_choices=spec.get("talent_choices"),
        magic=spec.get("magic"), coin=0)
    if errors:
        raise ValueError(f"{spec['name']}: {errors}")
    if spec.get("weapon_kind"):
        w = ch.equipped_weapon()
        if w is not None:
            w.kind = spec["weapon_kind"]
    while ch.level < level:
        errors = ch.level_up(ruleset, **_auto_pick(ruleset, ch))
        if errors:
            raise ValueError(f"{spec['name']} level {ch.level + 1}: {errors}")
    return ch


def build_party(ruleset, level: int, specs: Optional[list[dict]] = None) -> list[Character]:
    return [build_character(ruleset, s, level) for s in (specs or PARTY)]


def generic_foe(role: str, level: int, n: int = 0) -> Enemy:
    return Enemy(id=f"{role}_{level}_{n}", name=f"{role.title()} L{level}", level=level,
                 role=role, armor=0 if role == "mook" else 1, morale=7 if role != "boss" else 10,
                 wants="-", special="-", tells="-", breaks="-", twists=["-"] * 6,
                 when_bloodied=None if role == "mook" else "-")


def parse_foes(ruleset, text: str) -> list[Enemy]:
    """'mook:1x4,standard:1x2,card:chalk_hound' → live Enemy objects."""
    foes: list[Enemy] = []
    for i, part in enumerate(p.strip() for p in text.split(",") if p.strip()):
        head, _, count_s = part.partition("x")
        count = int(count_s) if count_s else 1
        kind, _, arg = head.partition(":")
        if kind == "card":
            import yaml
            base = Enemy.from_fof(yaml.safe_load((ENEMY_DIR / f"{arg}.fof").read_text()))
        else:
            base = generic_foe(kind, int(arg), i)
        if base.is_mook:
            foes.append(base.spawn(ruleset, count=count, key=f"{base.id}#{i}"))
        else:
            foes += [base.spawn(ruleset, key=f"{base.id}#{i}.{k}") for k in range(count)]
    return foes


# ---------------------------------------------------------------------------
# One fight
# ---------------------------------------------------------------------------

@dataclass
class FightResult:
    won: bool
    exchanges: int
    pcs_down: int
    pcs_dying: int
    hp_lost_fraction: float
    foes_broken: int
    log: list[str] = field(default_factory=list)


def _standing(chars):
    return [c for c in chars if c.status == "ok" and c.hp_current > 0]


def _active(foes):
    return [f for f in foes if not f.defeated and not f.broken]


def _pc_turn(ruleset, ch: Character, foes, state, rng, log) -> None:
    targets = _active(foes)
    if not targets:
        return
    target = min(targets, key=lambda f: (f.hp_current or 0) if not f.is_mook else -f.count)
    if ch.magic is not None:
        plan = plan_cast(ruleset, ch, domain=ch.magic.domains[0], scope="significant",
                         working=ch.magic.signature_workings[0])
        if plan.ok:
            res = resolve_cast(ruleset, ch, domain=ch.magic.domains[0], scope="significant",
                               intent="harm", working=ch.magic.signature_workings[0],
                               enemy=target, rng=rng)
            log.append(f"{ch.name} casts at {target.key}: {res.outcome}, {res.damage} dmg")
            if res.outcome == "partial_success":
                state.expose(ch.name, target.key)
            return
    res = combat.resolve_attack(ruleset, ch, target, state=state,
                                options=["extra_damage"], rng=rng)
    log.append(f"{ch.name} attacks {target.key}: {res.tier}, {res.damage} dmg")


def _morale(ruleset, foes, trigger_state: dict, rng, log) -> None:
    down = sum(1 for f in foes if f.defeated)
    total = len(foes)
    trigger = None
    if down >= 1 and not trigger_state.get("first"):
        trigger_state["first"] = True
        trigger = "first_to_fall"
    elif down * 2 >= total and not trigger_state.get("half"):
        trigger_state["half"] = True
        trigger = "half_down"
    if trigger:
        for f in _active(foes):
            res = combat.morale_check(ruleset, f, rng=rng)
            if res.breaks:
                log.append(f"{f.key} breaks ({trigger})")


def run_fight(ruleset, party: list[Character], foes: list[Enemy],
              rng: Optional[random.Random] = None, morale: bool = True) -> FightResult:
    """One fight to the finish (or MAX_EXCHANGES). Mutates party and foes."""
    rng = rng or random.Random()
    state = combat.CombatState()
    log: list[str] = []
    start_hp = sum(c.hp_current for c in party)
    triggers: dict = {}
    party_map = {c.name: c for c in party}
    for _ in range(MAX_EXCHANGES):
        for ch in _standing(party):
            _pc_turn(ruleset, ch, foes, state, rng, log)
        if morale:
            _morale(ruleset, foes, triggers, rng, log)
        if not _active(foes):
            break
        for foe in _active(foes):
            n_attacks = 1 if foe.is_mook else foe.attacks(ruleset)
            for _a in range(n_attacks):
                targets = _standing(party)
                if not targets:
                    break
                target = rng.choice(targets)
                res = combat.resolve_enemy_attack(ruleset, foe, target, state=state,
                                                  party=party_map, rng=rng)
                victim = party_map.get(res.target)
                log.append(f"{foe.key} → {res.target}: {res.label}, {res.damage} dmg")
                if victim is not None and res.target_result and res.target_result["dropped"]:
                    fell = victim.fall(ruleset, wound="Hurt", rng=rng)
                    log.append(f"{victim.name} falls: Hold On {fell['hold_on'].outcome}")
        if not _standing(party):
            break
        state.end_exchange()
        for f in foes:
            combat.expire_exchange_effects(f)
    exchanges = state.exchange
    won = not _active(foes)
    return FightResult(
        won=won, exchanges=exchanges,
        pcs_down=sum(1 for c in party if c.status != "ok" or c.hp_current <= 0),
        pcs_dying=sum(1 for c in party if c.status == "dying"),
        hp_lost_fraction=1 - sum(c.hp_current for c in party) / max(1, start_hp),
        foes_broken=sum(1 for f in foes if f.broken), log=log)


# ---------------------------------------------------------------------------
# Many fights
# ---------------------------------------------------------------------------

@dataclass
class Summary:
    level: int
    foes: str
    trials: int
    win_rate: float
    mean_exchanges: float
    median_exchanges: float
    mean_pcs_down: float
    any_down_rate: float
    mean_hp_lost: float

    def line(self) -> str:
        return (f"L{self.level:<2} {self.foes:<32} win {self.win_rate:6.1%}  "
                f"exch {self.mean_exchanges:4.2f} (med {self.median_exchanges:g})  "
                f"down {self.mean_pcs_down:4.2f} (any {self.any_down_rate:5.1%})  "
                f"hp lost {self.mean_hp_lost:5.1%}")


def simulate(level: int, foes: str, trials: int = 500, seed: int = 1,
             ruleset=None, specs: Optional[list[dict]] = None) -> Summary:
    ruleset = ruleset or load_ruleset()
    rng = random.Random(seed)
    template = build_party(ruleset, level, specs)
    import copy
    results = []
    for _ in range(trials):
        party = copy.deepcopy(template)
        results.append(run_fight(ruleset, party, parse_foes(ruleset, foes), rng))
    ex = [r.exchanges for r in results]
    return Summary(
        level=level, foes=foes, trials=trials,
        win_rate=sum(r.won for r in results) / trials,
        mean_exchanges=statistics.mean(ex), median_exchanges=statistics.median(ex),
        mean_pcs_down=statistics.mean(r.pcs_down for r in results),
        any_down_rate=sum(r.pcs_down > 0 for r in results) / trials,
        mean_hp_lost=statistics.mean(r.hp_lost_fraction for r in results))


def ladder(level: int) -> dict[str, str]:
    """The DESIGN §6 encounter ladder at a party level."""
    return {
        "trivial": f"mook:{level}x4",
        "standard": f"standard:{level}x3,mook:{level}x2",
        "boss": f"boss:{level}",
    }


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--level", type=int, default=1)
    ap.add_argument("--foes", default="mook:1x4")
    ap.add_argument("--trials", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ladder", action="store_true", help="run the pacing ladder at 1, 5, 10")
    args = ap.parse_args(argv)
    ruleset = load_ruleset()
    if args.ladder:
        for level in (1, 5, 10):
            for name, foes in ladder(level).items():
                s = simulate(level, foes, args.trials, args.seed, ruleset)
                print(f"{name:<9} {s.line()}")
        return 0
    print(simulate(args.level, args.foes, args.trials, args.seed, ruleset).line())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
