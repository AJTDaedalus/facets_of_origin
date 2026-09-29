"""Balance and encounter analysis built on the simulator (DESIGN v0.2 §7–§8).

No rule lives here: every fight is ``sim.Fight`` → ``combat.py``. This module builds
foes, encounters and parties, runs them, and turns outcomes into the numbers §7 and §8
ask for. Each public function is deterministic for its ``seed``.

Threat (Table 9–2). A foe's Threat is its Lanchester square-law strength,
``√(HP × damage per turn)``, for a standard foe of that CR (the SRD ladder's medians,
interpolated between CRs). Roles multiply it by factors **measured** in the simulator:
``minion`` (how many minions of a CR equal one standard of that CR), ``boss`` (how many
standards one boss equals) and ``never`` (a foe that never breaks). Square-law strengths
add, so an encounter's Threat is the plain sum of its foes' Threat.

Budgets (Table 9–1). For each party level and tier the simulator searches the Threat
total whose fights hit the tier's target (party HP lost at the middle of the tier's band;
Desperate: the middle of its win-rate band), averaged over three composition shapes. The
budget per character is that total ÷ 4.
"""
from __future__ import annotations

import bisect
import math
import random
import statistics
import zlib
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Optional

from . import monsters as M
from . import sim as S
from .combat import MonsterAttack, RuleOptions
from .monsters import MonsterBlock

TIERS = ("skirmish", "clash", "battle", "desperate")
MIN_CR, MAX_CR = 0.125, 30.0


def seed_for(*key) -> int:
    """A stable seed from a task key (independent of process scheduling)."""
    return zlib.crc32(repr(key).encode()) & 0x7FFFFFFF


# ================================================================ continuous-CR foes


def _lstsq3(xs, ys):
    """Least squares y = c0 + c1 x + c2 x² (pure Python normal equations)."""
    s = [sum(x ** k for x in xs) for k in range(5)]
    t = [sum(y * x ** k for x, y in zip(xs, ys)) for k in range(3)]
    a = [[s[0], s[1], s[2]], [s[1], s[2], s[3]], [s[2], s[3], s[4]]]
    # Gaussian elimination
    m = [row[:] + [t[i]] for i, row in enumerate(a)]
    for i in range(3):
        piv = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[piv] = m[piv], m[i]
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                m[r] = [a_ - f * b_ for a_, b_ in zip(m[r], m[i])]
    return [m[i][3] / m[i][i] for i in range(3)]


_FIT = None


def ladder_fit() -> dict:
    """Smooth stat lines by CR, fitted over every SRD ladder monster: log HP and log damage
    per turn, and AC, to-hit and saves, each quadratic in log CR. Monotone across 1/8–30
    (the piecewise medians are not: the CR 10 median hits softer than CR 9's)."""
    global _FIT
    if _FIT is None:
        ms = M.ladder()
        xs = [math.log(float(m.cr)) for m in ms]
        fits = {"hp": (_lstsq3(xs, [math.log(m.hp) for m in ms]), True),
                "dpt": (_lstsq3(xs, [math.log(m.routine_damage) for m in ms]), True),
                "ac": (_lstsq3(xs, [m.ac for m in ms]), False),
                "to_hit": (_lstsq3(xs, [m.to_hit for m in ms]), False),
                "attacks": (_lstsq3(xs, [sum(a.count for a in m.attacks) for m in ms]), False)}
        for a in ("str", "dex", "con", "int", "wis", "cha"):
            fits[a] = (_lstsq3(xs, [m.saves.get(a, 0) for m in ms]), False)
        _FIT = fits
    return _FIT


def _stat(cr: float, key: str) -> float:
    c, log = ladder_fit()[key]
    x = math.log(cr)
    v = c[0] + c[1] * x + c[2] * x * x
    return math.exp(v) if log else v


_WEAPON_SHARE = None


def ladder_weapon_share() -> float:
    """Share of the SRD ladder's attack damage that is bludgeoning, piercing or slashing."""
    global _WEAPON_SHARE
    if _WEAPON_SHARE is None:
        tot = bps = 0
        for m in M.ladder():
            for a in m.attacks:
                d = a.fixed * a.count
                tot += d
                bps += d if a.dtype in ("bludgeoning", "piercing", "slashing") else 0
        _WEAPON_SHARE = bps / tot
    return _WEAPON_SHARE


def generic(cr: float) -> MonsterBlock:
    """A generic foe at a continuous CR, from the smooth fit over the SRD ladder."""
    cr = max(MIN_CR, min(MAX_CR, float(cr)))
    hp = max(1, round(_stat(cr, "hp")))
    dpt = max(1, round(_stat(cr, "dpt")))
    ac = round(_stat(cr, "ac"))
    to_hit = round(_stat(cr, "to_hit"))
    n = max(1, round(_stat(cr, "attacks")))
    saves = {a: round(_stat(cr, a)) for a in ("str", "dex", "con", "int", "wis", "cha")}
    # Damage types: the ladder's share of weapon (bludgeoning/piercing/slashing) damage;
    # the rest arrives as one extra non-weapon strike (resistances then count as they do
    # against real monsters).
    other = round(dpt * (1 - ladder_weapon_share()))
    per, extra = divmod(dpt - other, n)
    attacks = [MonsterAttack("Strike", to_hit, per + extra, None, 0, "bludgeoning", 1)]
    if n > 1:
        attacks.append(MonsterAttack("Strike", to_hit, per, None, 0, "bludgeoning", n - 1))
    if other > 0:
        attacks.append(MonsterAttack("Blast", to_hit, other, None, 0, "force", 1))
    return MonsterBlock(f"generic_{cr:.3f}", f"CR {cr:.2f} foe", Fraction(cr).limit_denominator(64),
                        ac, hp, tuple(attacks), saves, source="engine")


def strength(block: MonsterBlock) -> float:
    """Square-law strength √(HP × damage per turn)."""
    return math.sqrt(block.hp * block.damage_per_turn)


def standard_threat(cr: float) -> float:
    return strength(generic(cr))


def cr_for_threat(threat: float) -> float:
    lo, hi = MIN_CR, MAX_CR
    if threat <= standard_threat(lo):
        return lo
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        if standard_threat(mid) < threat:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


HARD_HITTER_FACTOR = 1.25   # damage per turn ≥ 1.25 × the SRD ladder's line for its CR


def hits_hard(block: MonsterBlock) -> bool:
    """A hard hitter: its damage per turn is at least 1.25 × the typical damage for its CR
    (Table 9–3's damage column). Generic foes sit on the line, so never qualify."""
    return block.routine_damage >= HARD_HITTER_FACTOR * generic(float(block.cr)).damage_per_turn


# ================================================================ the Threat model


@dataclass(frozen=True)
class ThreatModel:
    """Threat = square-law strength. Standard: √(HP × DPT). Minion: √(minion_hp × DPT)
    (a minion's durability is one hit, whatever its CR). Boss: × ``boss``. A foe that
    never breaks: × ``never``. The three numbers are measured by ``calibrate``."""
    minion_hp: float = 8.0
    boss: float = 2.0
    never: float = 1.15
    hard: float = 1.0      # a hard hitter's mark-up (playtest fix pass: Amendment 4 item 2)

    def of(self, block: MonsterBlock, role: str = "standard") -> float:
        return self.price(block.hp, block.damage_per_turn, role,
                          never=block.morale == "never", hard=hits_hard(block))

    def price(self, hp: float, dpt: float, role: str = "standard", *, never: bool = False,
              hard: bool = False) -> float:
        """09 step 2 for a monster's pricing numbers (``monsters.turn_damage``,
        ``monsters.effective_hp``). A hard hitter counts × ``hard`` in every role; a
        monster that never breaks × ``never`` as a standard or minion."""
        if role == "minion":
            t = math.sqrt(self.minion_hp * dpt)
        elif role in ("standard", "boss"):
            t = math.sqrt(hp * dpt) * (self.boss if role == "boss" else 1.0)
        else:
            raise ValueError(f"unknown role {role!r}")
        if never and role != "boss":
            t *= self.never
        if hard:
            t *= self.hard
        return t

    def of_cr(self, cr: float, role: str = "standard") -> float:
        return self.of(generic(cr), role)

    def cr_for(self, threat: float, role: str) -> float:
        lo, hi = MIN_CR, MAX_CR
        if self.of_cr(lo, role) >= threat:
            return lo
        for _ in range(40):
            mid = math.sqrt(lo * hi)
            if self.of_cr(mid, role) < threat:
                lo = mid
            else:
                hi = mid
        return math.sqrt(lo * hi)

    def encounter_threat(self, enc: S.Encounter) -> float:
        tot = 0.0
        for spec in enc.foes:
            blk = M.get(spec.monster) if isinstance(spec.monster, str) else spec.monster
            tot += spec.count * self.of(blk, spec.role)
        return tot

    def table(self) -> dict:
        """Table 9–3: Threat by CR and role (the smooth SRD-ladder stat line at each CR),
        with the line's damage per turn (the hard-hitter yardstick)."""
        out = {}
        for cr in M.TEMPLATE_CRS:
            blk = generic(float(cr))
            out[str(cr)] = {"standard": round(self.of(blk)), "minion": round(self.of(blk, "minion")),
                            "boss": round(self.of(blk, "boss")),
                            "damage": round(blk.damage_per_turn)}
        return out


# ================================================================ encounters from a budget

SHAPES = ("standards", "boss_minions", "standards_minions")
MAX_MINIONS = 10


def compose(shape: str, total: float, model: ThreatModel) -> S.Encounter:
    """A generic encounter of ``shape`` worth ``total`` Threat (continuous CRs)."""
    specs = []
    # Minions are mooks: never more than half the CR of a standard foe of this budget
    # (the CR four standards would have). Minion Threat grows only with √DPT, so without
    # the cap a few minions of a very high CR (a CR 13 "minion" at 7th level) would carry
    # the share. The count rises instead, up to MAX_MINIONS.
    minion_cap = model.cr_for(total / 4, "standard") / 2

    def add(role, share, count):
        if share <= 0:
            return
        each = total * share / count
        cr = model.cr_for(each, role)
        if role == "minion" and cr > minion_cap:
            cr = minion_cap
            k = total * share / model.of_cr(cr, role)
            if k > MAX_MINIONS:
                cr = model.cr_for(total * share / MAX_MINIONS, role)
        blk = generic(cr)
        real_each = model.of(blk, role)
        n = max(1, round(total * share / real_each)) if real_each > 0 else count
        specs.append(S.FoeSpec(blk, role=role, count=n, leader=(role != "minion")))

    if shape == "standards":
        add("standard", 1.0, 4)
    elif shape == "boss_minions":
        add("boss", 0.6, 1)
        add("minion", 0.4, 5)
    elif shape == "standards_minions":
        add("standard", 0.5, 2)
        add("minion", 0.5, 4)
    elif shape == "solo_boss":
        add("boss", 1.0, 1)
    elif shape == "boss_standards":
        add("boss", 0.6, 1)
        add("standard", 0.4, 2)
    elif shape == "minion_swarm":
        add("minion", 1.0, 8)
    else:
        raise ValueError(shape)
    return S.Encounter(tuple(specs), name=shape)


# ================================================================ running


def party_profiles(rs, ids, level) -> list:
    from . import build as B
    out = []
    for pid in ids:
        entry = rs.presets.get(pid) or rs.sim_builds.get(pid)
        out.append(B.build(rs, B.Picks.from_entry(rs, entry, level, name=pid)).profile())
    return out


@dataclass
class Outcome:
    n: int
    win: float
    rounds: float
    hp_lost: float
    p_drop: float
    p_death: float
    rounds_sd: float = 0.0
    hp_lost_sd: float = 0.0

    def ci_hp(self) -> float:
        return 1.96 * self.hp_lost_sd / math.sqrt(max(1, self.n))

    def ci_rounds(self) -> float:
        return 1.96 * self.rounds_sd / math.sqrt(max(1, self.n))


def run_encounter(party, enc, *, n, seed, opts=RuleOptions(), share=S.DEFAULT_SHARE,
                  start_hp_frac=1.0) -> list:
    rng = random.Random(seed)
    start = [max(1, int(p.hp * start_hp_frac)) for p in party] if start_hp_frac < 1 else None
    return [S.run_fight(rng, party, enc, opts, share, start_hp=start) for _ in range(n)]


def outcome(results) -> Outcome:
    """HP lost is measured against the HP the party started the fight with (so a tired
    party that starts at half HP is compared like for like)."""
    n = len(results)
    hp = [r.party_hp_lost / max(1, r.party_hp_start or r.party_hp_max) for r in results]
    rd = [r.rounds for r in results]
    return Outcome(n=n, win=sum(r.won for r in results) / n, rounds=statistics.fmean(rd),
                   hp_lost=statistics.fmean(hp), p_drop=sum(bool(r.dropped) for r in results) / n,
                   p_death=sum(bool(r.dead) for r in results) / n,
                   rounds_sd=statistics.pstdev(rd), hp_lost_sd=statistics.pstdev(hp))


def mixed_outcome(party, total, model, *, n, seed, shapes=SHAPES, **kw) -> Outcome:
    res = []
    for i, shape in enumerate(shapes):
        enc = compose(shape, total, model)
        res += run_encounter(party, enc, n=n, seed=seed + i, **kw)
    return outcome(res)


def tier_target(tier: str, tiers: dict) -> tuple:
    t = tiers[tier]["targets"]
    if tier == "desperate":
        return "win", (t["win_pct_min"] + t["win_pct_max"]) / 200
    lo, hi = t["party_hp_lost_pct"]
    return "hp", (lo + hi) / 200


def fit_total(party, tier, tiers, model, *, n=300, seed=1, iters=12, **kw) -> tuple:
    """Search the encounter Threat total that hits a tier's target for this party.
    Returns (total, Outcome at that total)."""
    metric, target = tier_target(tier, tiers)
    lo, hi = 1.0, 20.0
    # grow the bracket
    def value(total):
        o = mixed_outcome(party, total, model, n=n, seed=seed, **kw)
        return (o.hp_lost if metric == "hp" else -o.win), o
    goal = target if metric == "hp" else -target
    v_hi, _ = value(hi)
    while v_hi < goal and hi < 5000:
        lo, hi = hi, hi * 2
        v_hi, _ = value(hi)
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        v, _ = value(mid)
        if v < goal:
            lo = mid
        else:
            hi = mid
    total = math.sqrt(lo * hi)
    return total, value(total)[1]


# ================================================================ calibrating the role multipliers


def equivalent_count(party, make_enc, target_hp, *, n, seed, lo=1, hi=40, **kw) -> float:
    """Continuous count k with make_enc(k) giving party HP lost = target_hp."""
    def hp(k):
        return outcome(run_encounter(party, make_enc(k), n=n, seed=seed, **kw)).hp_lost
    prev_k, prev_v = None, None
    for k in range(lo, hi + 1):
        v = hp(k)
        if v >= target_hp:
            if prev_k is None:
                return float(k)
            return prev_k + (target_hp - prev_v) / max(1e-9, v - prev_v)
        prev_k, prev_v = k, v
    return float(hi)


def calibrate_role(party, cr, role, *, n=400, seed=1, standards=4) -> float:
    """Measure one role against standards of the same CR (same party, same HP lost).

    minion → the HP a minion is "worth" in √(H × DPT) (so its Threat matches);
    boss → how many standards one boss equals; never → the strength ratio of a
    never-breaking standard to a normal one."""
    blk = generic(cr)
    base = S.Encounter.of(S.FoeSpec(blk, count=standards))
    target = outcome(run_encounter(party, base, n=n, seed=seed)).hp_lost
    if role == "minion":
        k = equivalent_count(party, lambda k: S.Encounter.of(S.FoeSpec(blk, role="minion", count=k)),
                             target, n=n, seed=seed + 1, lo=standards, hi=80)
        per_minion = standards * strength(blk) / k        # Threat one minion carries
        return per_minion ** 2 / blk.damage_per_turn
    if role == "boss":
        boss = S.Encounter.of(S.FoeSpec(blk, role="boss"))
        tb = outcome(run_encounter(party, boss, n=n, seed=seed + 2)).hp_lost
        return equivalent_count(party, lambda k: S.Encounter.of(S.FoeSpec(blk, count=k)), tb,
                                n=n, seed=seed + 3, lo=1, hi=24)
    if role == "never":
        nb = replace(blk, morale="never")
        k = equivalent_count(party, lambda k: S.Encounter.of(S.FoeSpec(nb, count=k)), target,
                             n=n, seed=seed + 4, lo=1, hi=standards * 2)
        return standards / k
    raise ValueError(role)


CALIBRATION_ANCHORS = ((1, 0.25), (1, 0.5), (4, 1.0), (4, 2.0), (7, 3.0), (7, 5.0),
                       (10, 6.0), (10, 9.0))


# ================================================================ real-monster encounters (validation)


def real_encounter(shape: str, total: float, model: ThreatModel, rng) -> S.Encounter:
    """An encounter of real SRD ladder monsters of ``shape`` worth about ``total`` Threat.

    For each part of the shape, every ladder monster is tried with the count that best
    matches the part's share of the budget (each monster priced by its own Threat), and one
    of the three closest fits is drawn at random."""
    ladder = M.ladder()
    plan = {"solo_boss": [("boss", 1.0, (1, 1))],
            "boss_minions": [("boss", 0.6, (1, 1)), ("minion", 0.4, (3, 8))],
            "boss_standards": [("boss", 0.6, (1, 1)), ("standard", 0.4, (1, 3))],
            "standards": [("standard", 1.0, (2, 6))],
            "standards_minions": [("standard", 0.5, (1, 3)), ("minion", 0.5, (3, 8))],
            "minion_swarm": [("minion", 1.0, (6, 14))]}[shape]
    specs = []
    for role, share, (lo, hi) in plan:
        want = total * share
        cands = []
        for blk in ladder:
            each = model.of(blk, role)
            k = min(hi, max(lo, round(want / each)))
            cands.append((abs(k * each - want) / want, k, blk))
        cands.sort(key=lambda c: c[0])
        err, k, blk = rng.choice(cands[:3])
        specs.append(S.FoeSpec(blk, role=role, count=k, leader=(role != "minion")))
    return S.Encounter(tuple(specs), name=shape)


COMPOSITION_CLASSES = ("solo_boss", "boss_minions", "boss_standards", "standards",
                       "standards_minions", "minion_swarm")


def classify(o: Outcome, tiers: dict) -> str:
    """The tier whose party-HP-lost band an outcome's mean falls in (Desperate by wins)."""
    t = {k: tiers[k]["targets"] for k in TIERS}
    if o.win < t["battle"]["win_pct_min"] / 100 - 0.05:
        return "desperate"
    hp = o.hp_lost * 100
    bands = [("skirmish", (0, 17.5)), ("clash", (17.5, 35)), ("battle", (35, 55))]
    for name, (lo, hi) in bands:
        if lo <= hp < hi:
            return name
    return "desperate"


# ================================================================ parties used by the analysis

PARTIES = {
    "ref4": ("fighter", "rogue", "wizard", "priest"),
    "ref3": ("fighter", "wizard", "priest"),
    "ref5": ("fighter", "rogue", "wizard", "priest", "oathsworn"),
    "ref6": ("fighter", "rogue", "wizard", "priest", "oathsworn", "druid"),
}
TIRED = {"start_hp_frac": 0.5, "share": S.DEFAULT_SHARE / 2}   # ~50% HP and ~50% of the fight's resources


def build_profile(build_id: str, level: int, source: str = "facets"):
    from . import build as B
    from . import data as D
    rs = D.load() if source == "facets" else D.load_baselines()
    entry = rs.presets.get(build_id) or rs.sim_builds.get(build_id)
    if entry is None:
        raise KeyError(build_id)
    return B.build(rs, B.Picks.from_entry(rs, entry, level, name=build_id)).profile()


def party_for(key: str, level: int) -> list:
    return [build_profile(pid, level) for pid in PARTIES[key]]


def tiers_spec() -> dict:
    from . import data as D
    return {t["id"]: t for t in D.load().raw["encounter_tiers"]}


# ================================================================ tasks (pure; the CLI parallelises them)


def task_calibrate(level, cr, role, n, seed) -> float:
    return calibrate_role(party_for("ref4", level), cr, role, n=n, seed=seed)


def task_fit(party_key, level, tier, model: ThreatModel, n, iters, seed, tired=False) -> dict:
    kw = dict(start_hp_frac=TIRED["start_hp_frac"], share=TIRED["share"]) if tired else {}
    total, o = fit_total(party_for(party_key, level), tier, tiers_spec(), model, n=n,
                         iters=iters, seed=seed, **kw)
    return {"total": total, "outcome": o.__dict__}


def task_eval(party_key, level, total, model: ThreatModel, n, seed, shapes=SHAPES,
              tired=False, party_ids=None) -> dict:
    kw = dict(start_hp_frac=TIRED["start_hp_frac"], share=TIRED["share"]) if tired else {}
    party = [build_profile(p, level) for p in party_ids] if party_ids else party_for(party_key, level)
    o = mixed_outcome(party, total, model, n=n, seed=seed, shapes=shapes, **kw)
    d = dict(o.__dict__)
    d["ci_hp"], d["ci_rounds"] = o.ci_hp(), o.ci_rounds()
    return d


def task_validate(level, tier, total, cls, sample, model: ThreatModel, n, seed) -> dict:
    rng = random.Random(seed)
    enc = real_encounter(cls, total, model, rng)
    o = outcome(run_encounter(party_for("ref4", level), enc, n=n, seed=seed + 7))
    return {"class": cls, "tier": tier, "level": level, "threat": model.encounter_threat(enc),
            "foes": [f"{s.count}× {s.monster.name} ({s.role}, CR {s.monster.cr})" for s in enc.foes],
            "outcome": o.__dict__, "landed": classify(o, tiers_spec())}


def day_spec() -> dict:
    """The adventuring day (yaml ``adventuring_day``): Clashes per long rest and the
    fights (1-based) followed by a short rest."""
    from . import data as D
    d = D.load().raw["adventuring_day"]
    return {"clashes": int(d["clashes"]), "short_rests_after": list(d["short_rests_after"])}


DAY_SHAPES = ("standards", "boss_minions", "standards_minions")


def day_encounters(total: float, model: ThreatModel) -> list:
    n = day_spec()["clashes"]
    return [compose(DAY_SHAPES[i % len(DAY_SHAPES)], total, model) for i in range(n)]


def task_pi(build_id, source, level, clash_total, model: ThreatModel, n_days, seed) -> dict:
    """§8 metrics for one build at one level over n standard days (the yaml adventuring
    day: three Clashes, two short rests) beside three reference-party companions."""
    me = build_profile(build_id, level, source)
    comp = [p for p in PARTIES["ref4"] if p != build_id][:3]
    party = [me] + [build_profile(p, level) for p in comp]
    encs = day_encounters(clash_total, model)
    rng = random.Random(seed)
    dmg = heal = prev = selfheal = temp = 0.0
    rounds = fights = 0
    att = hits = raw = taken = 0
    days_survived = deaths_me = 0
    for _ in range(n_days):
        day = S.run_day(rng, party, encs, opts=RuleOptions(),
                        short_rests_after=tuple(day_spec()["short_rests_after"]))
        days_survived += day.survived
        for f in day.fights:
            if 0 not in f.members:
                continue
            pid = next(k for k in f.damage_by_pc if k.startswith(f"pc{f.members.index(0)}:"))
            dmg += f.damage_by_pc[pid]
            heal += f.healing_by_pc[pid]
            prev += f.prevented_by_pc[pid]
            selfheal += f.selfheal_by_pc[pid]
            temp += f.temp_by_pc[pid]
            att += f.attacks_on[pid]
            hits += f.hits_on[pid]
            raw += f.raw_on[pid]
            taken += f.taken_on[pid]
            rounds += f.rounds
            fights += 1
            if pid in f.dead:
                deaths_me += 1
    rounds = max(1, rounds)
    fights = max(1, fights)
    hit_rate = hits / att if att >= 50 else None
    if hit_rate is None:
        ref = generic(max(0.125, level * 0.6))
        from .combat import hit_chance
        hit_rate = hit_chance(ref.to_hit, me.ac)
    ratio = (raw / taken) if taken > 0 else 1.0
    edpr = (dmg + heal + prev) / rounds
    ehp = (me.hp + temp / fights + selfheal / fights) * (0.55 / max(0.05, hit_rate)) * ratio
    return {"build": build_id, "source": source, "level": level, "dpr": dmg / rounds,
            "heal_pr": heal / rounds, "prevent_pr": prev / rounds, "edpr": edpr,
            "hp": me.hp, "ac": me.ac, "hit_rate": hit_rate, "dmg_ratio": ratio,
            "selfheal_pf": selfheal / fights, "temp_pf": temp / fights, "ehp": ehp,
            "pi": edpr * ehp, "days_survived": days_survived / n_days, "deaths": deaths_me,
            "fights": fights}


def task_solo_factor(level, clash_total, model: ThreatModel, n, seed, iters=7) -> dict:
    """How much a lone boss must be marked up for the Clash budget to buy a Clash: the
    factor f such that a solo boss worth clash_total ÷ f Threat costs the Clash target."""
    tiers = tiers_spec()
    _, target = tier_target("clash", tiers)
    party = party_for("ref4", level)

    def hp(f):
        enc = compose("solo_boss", clash_total / f, model)
        return outcome(run_encounter(party, enc, n=n, seed=seed)).hp_lost

    lo, hi = 0.7, 3.0
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        if hp(mid) > target:
            lo = mid
        else:
            hi = mid
    f = math.sqrt(lo * hi)
    at1 = outcome(run_encounter(party, compose("solo_boss", clash_total, model), n=n, seed=seed))
    return {"level": level, "factor": f, "hp_lost_x1": at1.hp_lost, "win_x1": at1.win}


def task_day(level, clash_total, model: ThreatModel, n, seed, clashes=None, rests=None) -> dict:
    """The reference party's adventuring day at the Clash budget: ``clashes`` fights (the
    yaml day by default) with short rests after the listed fights. Survived = every fight
    won; also reports days with a PC death."""
    spec = day_spec()
    k = clashes or spec["clashes"]
    rests = tuple(rests if rests is not None else spec["short_rests_after"])
    encs = [compose(DAY_SHAPES[i % len(DAY_SHAPES)], clash_total, model) for i in range(k)]
    party = party_for("ref4", level)
    rng = random.Random(seed)
    ok = dead = 0
    for _ in range(n):
        d = S.run_day(rng, party, encs, opts=RuleOptions(), short_rests_after=rests)
        ok += d.survived
        dead += d.deaths > 0
    return {"level": level, "clashes": k, "rests": list(rests), "survived": ok / n,
            "any_death": dead / n}


def task_monster_factor(block_id: str, level: int, clash_total: float, model: ThreatModel,
                        n: int, seed: int, role: str = "standard", iters: int = 9) -> dict:
    """How a real SRD monster plays against its price (playtest fix pass: the hard-hitter
    mark-up, Amendment 4 item 2). A group of it (3–10 standards, or 3–14 minions) worth
    about the Clash budget fights the reference party; the ratio is the Threat of generic
    standards (the foes Table 9–1 was fitted on) that cost the party the same HP, over the
    group's price. Priced with ``model`` taken as ``hard = 1``, so the ratio measures the
    mark-up rather than including it."""
    base = replace(model, hard=1.0)
    blk = M.get(block_id)
    each = base.of(blk, role)
    lo_k, hi_k = (3, 10) if role == "standard" else (3, 14)
    k = min(hi_k, max(lo_k, round(clash_total / each)))
    party = party_for("ref4", level)
    enc = S.Encounter.of(S.FoeSpec(blk, role=role, count=k, leader=(role != "minion")))
    target = outcome(run_encounter(party, enc, n=n, seed=seed)).hp_lost
    priced = k * each

    def hp(total):
        return outcome(run_encounter(party, compose("standards", total, base), n=n,
                                     seed=seed + 1)).hp_lost

    lo, hi = 0.25 * priced, 4.0 * priced
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        if hp(mid) < target:
            lo = mid
        else:
            hi = mid
    eq = math.sqrt(lo * hi)
    return {"id": block_id, "role": role, "level": level, "count": k, "priced": priced,
            "equivalent": eq, "ratio": eq / priced, "hits_hard": hits_hard(blk),
            "hp_lost": target}


def task_swap(build_id, source, level, clash_total, model: ThreatModel, n, seed) -> dict:
    """The swap test — the balance band's primary measure (balance pass, V32).

    The reference party with this build swapped in for each member in turn plays ``n``
    standard days (the yaml adventuring day: three Clashes, short rests between), so
    daily resources are paced as at the table. The score is the mean share of the
    party's hit points lost per fight (lower is stronger); rounds, fight wins and whole
    days survived are reported beside it. Use one ``seed`` for every build at a level
    (common random numbers) so builds are compared on the same dice."""
    me = build_profile(build_id, level, source)
    ref = party_for("ref4", level)
    encs = day_encounters(clash_total, model)
    rests = tuple(day_spec()["short_rests_after"])
    hp, rounds, wins, days = [], [], [], []
    for i in range(len(ref)):
        party = ref[:i] + [me] + ref[i + 1:]
        rng = random.Random(seed + 10 * i)
        for _ in range(n):
            d = S.run_day(rng, party, encs, opts=RuleOptions(), short_rests_after=rests)
            days.append(d.survived)
            for f in d.fights:
                hp.append(f.party_hp_lost / max(1, f.party_hp_max))
                rounds.append(f.rounds)
                wins.append(f.won)
    return {"build": build_id, "source": source, "level": level,
            "hp_lost": statistics.fmean(hp), "rounds": statistics.fmean(rounds),
            "win": statistics.fmean(wins), "days_survived": statistics.fmean(days),
            "hp_lost_sd": statistics.pstdev(hp), "fights": len(hp)}


def task_dummy_dpr(build_id, source, level, n, seed) -> dict:
    me = build_profile(build_id, level, source)
    ac = round(generic(max(0.125, level * 0.75)).ac)
    return {"build": build_id, "source": source, "level": level, "ac": ac,
            "dpr_1": S.damage_per_round(me, ac=ac, n=n, seed=seed, foes=1, rounds=4),
            "dpr_3": S.damage_per_round(me, ac=ac, n=n, seed=seed, foes=3, rounds=4)}


# ================================================================ Table 9–2: Threat per monster
#
# BRIEF Amendment 4, ruling 2: every SRD 5.2.1 monster priced from its own stat block.
# The model's constants are the ones the simulator wrote into the yaml (`monster_threat`)
# and the book prints, so an MM with a calculator gets the same number as the table.
# The three presentation cut-offs below are not rules; they only say which party levels
# a monster suits and which ones the interim hard-hitters rule (09) applies to.

STANDARD_COUNT = (3, 10)    # a standard "fits" a level when 3–10 of them make a Clash for four
BOSS_SHARE = (0.5, 1.0)     # a boss fits when it is half to all of a Clash for four (§7)

_NUM = r"(\d+(?:\.\d+)?)"


def _rules_raw(raw=None) -> dict:
    if raw is None:
        from . import data as D
        raw = D.load().raw
    return raw


def _model_number(model: dict, key: str, pattern: str) -> float:
    import re
    m = re.search(pattern, str(model.get(key, "")))
    if not m:
        raise ValueError(f"monster_threat.model.{key}: no constant in {model.get(key)!r}")
    return float(m.group(1))


def threat_model_from_data(raw=None) -> ThreatModel:
    """The ThreatModel the yaml prints (``monster_threat.model``), at the printed precision."""
    model = (_rules_raw(raw).get("monster_threat") or {}).get("model") or {}
    return ThreatModel(minion_hp=_model_number(model, "minion", r"sqrt\(\s*" + _NUM),
                       boss=_model_number(model, "boss", r"x\s*" + _NUM),
                       never=_model_number(model, "never_breaks", r"x\s*" + _NUM),
                       hard=_model_number(model, "hard_hitter", r"x\s*" + _NUM))


def lone_boss_factor(raw=None) -> float:
    """V42: a lone boss counts × this (``monster_threat.model.lone_boss``)."""
    model = (_rules_raw(raw).get("monster_threat") or {}).get("model") or {}
    return _model_number(model, "lone_boss", r"x\s*" + _NUM)


SMALL_COMPANY = (0.2, 1.1)   # company under a fifth of the boss's Threat: × 1.1 (measured ×1.06)


def boss_markup(boss_threat: float, company_threat: float, raw=None) -> float:
    """09 *Adjusting the budget* (playtest fix pass, MM #11): a boss alone counts × the
    lone-boss factor (1.2); a boss whose company is worth less than a fifth of its own
    Threat counts × 1.1 (the simulator: ×1.06 at a fifth; the company is usually gone in
    the first round); otherwise × 1."""
    if boss_threat <= 0 or company_threat < 0:
        raise ValueError("Threat can't be negative, and a boss has some")
    if company_threat == 0:
        return lone_boss_factor(raw)
    share, factor = SMALL_COMPANY
    return factor if company_threat < share * boss_threat else 1.0


def clash_totals(raw=None, *, party_size: int = 4, tier: str = "clash") -> dict:
    """{level: the tier's Threat budget for the whole party} from ``encounter_table``."""
    if tier not in TIERS:
        raise KeyError(tier)
    table = _rules_raw(raw)["encounter_table"]
    return {int(L): party_size * row[tier] for L, row in sorted(table.items(), key=lambda kv: int(kv[0]))}


def level_range(levels) -> str:
    """[3, 4, 5] → "3–5"; [1] → "1"; [] → "—". Levels must be contiguous."""
    levels = sorted(levels)
    if not levels:
        return "—"
    if levels != list(range(levels[0], levels[-1] + 1)):
        raise ValueError(f"levels not contiguous: {levels}")
    return str(levels[0]) if len(levels) == 1 else f"{levels[0]}–{levels[-1]}"


def monster_threat_row(block: MonsterBlock, model: ThreatModel, totals: dict) -> dict:
    """One Table 9–2 row: the block's Threat in each role, the party levels it fits as a
    standard and as a boss (against ``totals``, the Clash budget for four), and its flags."""
    if not totals:
        raise ValueError("need the Clash budget totals by level")
    std, mn, bs = (round(model.of(block, r)) for r in ("standard", "minion", "boss"))
    lo, hi = STANDARD_COUNT
    blo, bhi = BOSS_SHARE
    return {"id": block.id, "name": block.name, "cr": block.cr,
            "standard": std, "minion": mn, "boss": bs,
            "standard_levels": [L for L, t in totals.items() if lo <= t / std <= hi],
            "boss_levels": [L for L, t in totals.items() if blo <= bs / t <= bhi],
            "never": block.morale == "never",
            "hits_hard": hits_hard(block)}


def threat_appendix(raw=None) -> list:
    """Table 9–2: every SRD monster in ``srd_monsters.yaml``, by CR then name."""
    raw = _rules_raw(raw)
    model = threat_model_from_data(raw)
    totals = clash_totals(raw)
    return [monster_threat_row(b, model, totals) for b in M.ladder()]
