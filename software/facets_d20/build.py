"""Characters from picks: computed numbers and build legality (schema v0.2).

    picks = Picks(facet="soul", path="spell", level=4, abilities={...}, ...)
    ch = build(ruleset, picks)        # raises BuildError listing every broken rule
    ch.hp, ch.ac, ch.attack_bonus, ch.save_dc, ch.slots, ch.profile()

``Character.profile()`` is the ``CombatProfile`` the simulator runs. Every number in it
comes from the yaml (facet, path, talents and their ``effects``) through the handlers
in ``_apply_effect``; nothing is keyed on a talent's id.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from . import data as _data
from .dice import Dice
from .profile import CasterProfile, CombatProfile, Rider, Uses, Weapon

HP_FIRST = _data.HP_FIRST_RULES

ABILITIES = _data.ABILITIES


class BuildError(ValueError):
    """An illegal build. ``errors`` lists every rule broken, one line each."""

    def __init__(self, errors):
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("illegal build:\n  - " + "\n  - ".join(self.errors))

    def __reduce__(self):            # survive multiprocessing
        return (BuildError, (self.errors,))


# ================================================================ SRD 5.2.1 equipment

# id: (category, base AC, dex cap or None for no cap / 0 for no dex)
ARMOR = {
    "padded": ("light", 11, None), "leather": ("light", 11, None),
    "studded_leather": ("light", 12, None),
    "hide": ("medium", 12, 2), "chain_shirt": ("medium", 13, 2),
    "scale_mail": ("medium", 14, 2), "breastplate": ("medium", 14, 2),
    "half_plate": ("medium", 15, 2),
    "ring_mail": ("heavy", 14, 0), "chain_mail": ("heavy", 16, 0),
    "splint": ("heavy", 17, 0), "plate": ("heavy", 18, 0),
}


@dataclass(frozen=True)
class WeaponDef:
    id: str
    dice: str
    category: str               # simple | martial
    dtype: str
    props: frozenset = frozenset()
    versatile: Optional[str] = None


def _w(id_, dice, cat, dtype, props=(), versatile=None):
    return WeaponDef(id_, dice, cat, dtype, frozenset(props), versatile)


WEAPONS = {w.id: w for w in [
    _w("club", "1d4", "simple", "bludgeoning", ["light"]),
    _w("dagger", "1d4", "simple", "piercing", ["finesse", "light", "thrown"]),
    _w("dart", "1d4", "simple", "piercing", ["finesse", "thrown"]),
    _w("greatclub", "1d8", "simple", "bludgeoning", ["two_handed"]),
    _w("handaxe", "1d6", "simple", "slashing", ["light", "thrown"]),
    _w("javelin", "1d6", "simple", "piercing", ["thrown"]),
    _w("mace", "1d6", "simple", "bludgeoning"),
    _w("quarterstaff", "1d6", "simple", "bludgeoning", versatile="1d8"),
    _w("sickle", "1d4", "simple", "slashing", ["light"]),
    _w("spear", "1d6", "simple", "piercing", ["thrown"], versatile="1d8"),
    _w("light_crossbow", "1d8", "simple", "piercing", ["ranged", "two_handed"]),
    _w("shortbow", "1d6", "simple", "piercing", ["ranged", "two_handed"]),
    _w("sling", "1d4", "simple", "bludgeoning", ["ranged"]),
    _w("battleaxe", "1d8", "martial", "slashing", versatile="1d10"),
    _w("flail", "1d8", "martial", "bludgeoning"),
    _w("glaive", "1d10", "martial", "slashing", ["heavy", "two_handed", "reach"]),
    _w("greataxe", "1d12", "martial", "slashing", ["heavy", "two_handed"]),
    _w("greatsword", "2d6", "martial", "slashing", ["heavy", "two_handed"]),
    _w("halberd", "1d10", "martial", "slashing", ["heavy", "two_handed", "reach"]),
    _w("longsword", "1d8", "martial", "slashing", versatile="1d10"),
    _w("maul", "2d6", "martial", "bludgeoning", ["heavy", "two_handed"]),
    _w("morningstar", "1d8", "martial", "piercing"),
    _w("rapier", "1d8", "martial", "piercing", ["finesse"]),
    _w("scimitar", "1d6", "martial", "slashing", ["finesse", "light"]),
    _w("shortsword", "1d6", "martial", "piercing", ["finesse", "light"]),
    _w("warhammer", "1d8", "martial", "bludgeoning", versatile="1d10"),
    _w("war_pick", "1d8", "martial", "piercing", versatile="1d10"),
    _w("trident", "1d8", "martial", "piercing", ["thrown"], versatile="1d10"),
    _w("whip", "1d4", "martial", "slashing", ["finesse", "reach"]),
    _w("hand_crossbow", "1d6", "martial", "piercing", ["ranged", "light"]),
    _w("heavy_crossbow", "1d10", "martial", "piercing", ["ranged", "heavy", "two_handed"]),
    _w("longbow", "1d8", "martial", "piercing", ["ranged", "heavy", "two_handed"]),
]}

STANDARD_ARRAY = sorted([15, 14, 13, 12, 10, 8])
POINT_BUY_COST = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}


def mod(score: int) -> int:
    return (score - 10) // 2


# ================================================================ picks


@dataclass
class Picks:
    facet: str
    path: Optional[str]                  # legacy v0.2 Steel/Spell; None when the ruleset has no paths
    level: int
    abilities: dict                      # final 1st-level scores, background included
    background: Optional[str] = None
    base_abilities: Optional[dict] = None   # custom builds: validated + background added
    talents: dict = field(default_factory=dict)   # {level: talent id}
    knacks: Optional[dict] = field(default_factory=dict)  # {level: id}; None = unspecified
    casting_ability: Optional[str] = None   # resolved from the Facet/talent when None
    domains: list = field(default_factory=list)   # domain ids, path domain first
    kit: dict = field(default_factory=dict)       # {armor, shield, weapons: [...]}
    name: str = "custom"
    asi_priority: Optional[tuple] = None          # E-3 / SRD baselines: ASI order
    asi: dict = field(default_factory=dict)       # V21: {4: {"plus2": "str"} | {"plus1": [a, b]} | {"knack": id}}
    tradition: Optional[str] = None               # E3: a Body caster names its tradition

    @classmethod
    def from_entry(cls, rs, entry: dict, level: int, *, name: Optional[str] = None) -> "Picks":
        """A preset or sim_build entry (§1.5) at a character level."""
        if entry.get("preset"):
            return cls.from_entry(rs, rs.presets[entry["preset"]], level,
                                  name=name or entry.get("id"))
        domains = [entry["domain"]] if entry.get("domain") else []
        extra = entry.get("extra_domains") or {}
        if isinstance(extra, dict):
            domains += [d for l, d in sorted((int(k), v) for k, v in extra.items()) if l <= level]
        else:
            domains += list(extra)
        talents = {int(k): v for k, v in (entry.get("talents") or {}).items() if int(k) <= level}
        kit = dict(entry.get("kit") or {})
        for kl, change in sorted((int(k), v) for k, v in (entry.get("kit_by_level") or {}).items()):
            if kl <= level:
                kit.update(change)
        probe = cls(facet=entry["facet"], path=entry.get("path"), level=level,
                    abilities=dict(entry["abilities"]), talents=talents,
                    tradition=entry.get("tradition"))
        casts = bool(_casting_sources(rs, probe))
        if not casts:
            domains = []          # the domain arrives with the first Spell talent
        elif entry.get("deep_domain"):
            deep = any(rid for rid, e in track_ranks(rs, probe)
                       if e["type"] == "domains" and e.get("prismatic"))
            if deep:
                domains.append(entry["deep_domain"])
        knacks = entry.get("knacks")
        if knacks is not None:
            knacks = {int(k): v for k, v in knacks.items() if int(k) <= level}
            if not entry.get("background") and entry.get("id") in (rs.sim_builds or {}):
                knacks = None
        elif entry.get("id") in getattr(rs, "sim_builds", {}):
            knacks = None
        asi = {int(k): v for k, v in (entry.get("asi") or {}).items() if int(k) <= level}
        return cls(facet=entry["facet"], path=entry.get("path"), level=level, asi=asi,
                   abilities=dict(entry["abilities"]), background=entry.get("background"),
                   talents=talents, knacks=knacks, tradition=entry.get("tradition"),
                   casting_ability=entry.get("casting_ability"), domains=domains,
                   kit=kit, name=name or entry.get("name") or entry["id"],
                   asi_priority=tuple(entry["asi_priority"]) if entry.get("asi_priority") else None)

    @classmethod
    def from_preset(cls, rs, preset_id: str, level: int) -> "Picks":
        if preset_id not in rs.presets:
            raise KeyError(f"unknown preset {preset_id!r}")
        return cls.from_entry(rs, rs.presets[preset_id], level)

    @classmethod
    def from_sim_build(cls, rs, build_id: str, level: int) -> "Picks":
        if build_id not in rs.sim_builds:
            raise KeyError(f"unknown sim build {build_id!r}")
        return cls.from_entry(rs, rs.sim_builds[build_id], level, name=build_id)


# ================================================================ expressions


class Ctx:
    def __init__(self, level, pb, mods, casting_mod=None, soul_mod=None, slot_level=0,
                 spell_dc=None):
        self.level, self.pb, self.mods = level, pb, mods
        self.casting_mod = casting_mod
        self.soul_mod = soul_mod
        self.slot_level = slot_level
        self.spell_dc = spell_dc

    def term(self, t: str) -> int:
        if "*" in t:
            k, rest = t.split("*", 1)
            return int(k) * self.term(rest)
        if t.isdigit():
            return int(t)
        if t == "pb":
            return self.pb
        if t == "level":
            return self.level
        if t == "half_level":
            return self.level // 2
        if t == "half_level_round_up":
            return (self.level + 1) // 2
        if t == "slot_level":
            return self.slot_level
        if t == "spell":
            return self.spell_dc if self.spell_dc is not None else 0
        if t == "casting":
            return self.casting_mod if self.casting_mod is not None else 0
        if t == "soul":
            if self.soul_mod is not None:
                return self.soul_mod
            return max(self.mods["wis"], self.mods["cha"])
        if t in self.mods:
            return self.mods[t]
        raise _data.DataError(f"unknown expression term {t!r}")


def eval_amount(expr, ctx: Ctx):
    """Evaluate an expression → (Dice or None, flat int)."""
    if expr is None:
        return None, 0
    if isinstance(expr, int):
        return None, expr
    d, flat = None, 0
    for t in str(expr).replace(" ", "").split("+"):
        if "d" in t and t[0].isdigit() and t.split("d")[1].isdigit():
            nd = Dice.parse(t)
            d = nd if d is None else Dice(d.count + nd.count, d.sides)
        else:
            flat += ctx.term(t)
    return d, flat


def eval_int(expr, ctx: Ctx, minimum: Optional[int] = None) -> int:
    d, flat = eval_amount(expr, ctx)
    if d is not None:
        raise _data.DataError(f"expected a number, got dice in {expr!r}")
    return max(flat, minimum) if minimum is not None else flat


def active_effects(entry: dict, level: int, *, depth: Optional[dict] = None,
                   scaling_depth: Optional[dict] = None, facet: Optional[str] = None) -> list:
    """An entry's effects at a character level, with ``scaling`` applied (§1.3).

    Tracked talents (Amendment 2): a scaling line at level N also needs depth
    ``scaling_depth[N]`` in the talent's ``track``. An effect with ``facets:`` applies only
    to those Facets."""
    effects = [dict(e) for e in entry.get("effects") or []]
    track = entry.get("track")
    for lvl in sorted(int(k) for k in (entry.get("scaling") or {})):
        if lvl > level:
            continue
        if track and depth is not None and scaling_depth:
            need = int(scaling_depth.get(lvl, scaling_depth.get(str(lvl), 0)) or 0)
            if depth.get(track, 0) < need:
                continue
        sc = entry["scaling"]
        for new in sc.get(lvl, sc.get(str(lvl))) or []:
            key = (new["type"], new.get("id"))
            for i, old in enumerate(effects):
                if (old["type"], old.get("id")) == key:
                    effects[i] = dict(new)
                    break
            else:
                effects.append(dict(new))
    if facet is not None:
        effects = [e for e in effects if not e.get("facets") or facet in e["facets"]]
    return effects


def background_bonus(bg: Optional[dict]) -> dict:
    """A background's ability bonuses: a list means +1 to each; a map is explicit."""
    if not bg:
        return {}
    ab = bg.get("abilities") or {}
    if isinstance(ab, list):
        return {a: 1 for a in ab}
    return dict(ab)


def resolve_casting_ability(spec, abilities: dict) -> str:
    """``int`` → int; ``soul`` → the higher of Wis and Cha (ties: Wis)."""
    if isinstance(spec, list):
        spec = spec[0] if len(spec) == 1 else spec
    if isinstance(spec, list):
        return max(spec, key=lambda a: (abilities[a], a == "wis"))
    if spec == "soul":
        return "wis" if abilities["wis"] >= abilities["cha"] else "cha"
    return spec


# ================================================================ the character


@dataclass
class Character:
    rs: object
    picks: Picks
    abilities: dict
    hit_die: int
    hp: int
    ac: int
    prof: int
    saves: dict
    effects: list                 # (source id, effect) active at this level
    tradition: Optional[str]
    progression: Optional[str]
    casting_ability: Optional[str]
    slots: list
    cantrips: list
    spells: list
    domains: list
    weapon: Optional[Weapon]
    resources: dict
    features: list
    armored: bool = False
    shield: bool = False

    @property
    def level(self) -> int:
        return self.picks.level

    @property
    def mods(self) -> dict:
        return {a: mod(s) for a, s in self.abilities.items()}

    @property
    def attack_bonus(self) -> Optional[int]:
        return self.weapon.to_hit if self.weapon else None

    @property
    def casting_mod(self) -> Optional[int]:
        return self.mods[self.casting_ability] if self.casting_ability else None

    @property
    def save_dc(self) -> Optional[int]:
        return 8 + self.prof + self.casting_mod if self.casting_ability else None

    @property
    def spell_attack(self) -> Optional[int]:
        return self.prof + self.casting_mod if self.casting_ability else None

    @property
    def max_spell_level(self) -> int:
        return len(self.slots)

    def attack_with(self, weapon_id: str) -> Weapon:
        """The attack line for one weapon of the kit (to-hit, damage die and modifier)."""
        return _make_weapon(self.rs, self.picks, weapon_id, self.abilities, self.prof,
                            self.effects, _ctx(self.level, self.prof, self.mods,
                                               self.casting_ability, self.tradition),
                            armored=self.armored)

    def has_effect(self, etype: str) -> bool:
        return any(e["type"] == etype for _, e in self.effects)

    def profile(self) -> CombatProfile:
        return _profile(self)


ASI_FORMS = ("plus2", "plus1", "knack")


def primary_ability(rs, picks: Picks) -> str:
    """The build's main attack or casting ability (V21's default ASI target): the casting
    ability when magic is the build's main line (Spell is the main track, or a legacy
    caster), otherwise the main weapon's ability."""
    casters = _casting_sources(rs, picks)
    spell_main = bool(casters)
    if rs.raw.get("tracks"):
        spell_main = picks_main_track(rs, picks) == "spell"
    if casters and spell_main:
        _, trad, spec, _ = casters[0]
        tdef = (rs.spells_raw.get("traditions") or {}).get(trad) or {}
        return resolve_casting_ability(spec or tdef.get("ability"), picks.abilities)
    ws = [WEAPONS[w] for w in picks.kit.get("weapons") or [] if w in WEAPONS]
    if ws:
        w = ws[0]
        if "ranged" in w.props:
            return "dex"
        if "finesse" in w.props and picks.abilities["dex"] > picks.abilities["str"]:
            return "dex"
        for _, e in _static_feature_effects(rs, picks):
            if e["type"] == "martial_die" and picks.abilities["dex"] > picks.abilities["str"]:
                return "dex"
        return "str"
    return max(ABILITIES, key=lambda a: (picks.abilities[a], -ABILITIES.index(a)))


def _static_feature_effects(rs, picks):
    for tid in picks.talents.values():
        for e in (rs.talents.get(tid) or {}).get("effects") or []:
            yield tid, e


def default_asi(rs, picks: Picks, scores: dict) -> dict:
    """V21 default for presets and sim builds: +2 to the primary ability (the overflow past
    20 goes to the next-highest score as +1/+1)."""
    prim = primary_ability(rs, picks)
    if scores[prim] <= 18:
        return {"plus2": prim}
    nxt = max((a for a in ABILITIES if a != prim and scores[a] < 20),
              key=lambda a: (scores[a], -ABILITIES.index(a)))
    if scores[prim] == 19:
        return {"plus1": [prim, nxt]}
    return {"plus2": nxt} if scores[nxt] <= 18 else {"plus1": [nxt, max(
        (a for a in ABILITIES if a not in (prim, nxt) and scores[a] < 20),
        key=lambda a: scores[a])]}


def asi_choices(rs, picks: Picks) -> dict:
    """{level: choice} for every ASI level reached, defaults filled in (V21)."""
    rule = rs.advancement.get("asi_rule")
    out = {}
    if rule not in ("choice", "two_highest_plus_one"):
        return out
    scores = dict(picks.abilities)
    facet = rs.facets.get(picks.facet) or {}
    for lvl in facet.get("asi_levels") or rs.advancement.get("asi_levels", []):
        if lvl > picks.level:
            continue
        if rule == "choice":
            ch = picks.asi.get(lvl) or default_asi(rs, picks, scores)
        else:
            cands = sorted([a for a in ABILITIES if scores[a] < 20],
                           key=lambda a: (-scores[a], ABILITIES.index(a)))
            ch = {"plus1": cands[:2]}
        out[lvl] = ch
        _apply_asi(scores, ch)
    return out


def _apply_asi(scores: dict, ch: dict) -> None:
    if "plus2" in ch:
        scores[ch["plus2"]] += 2
    elif "plus1" in ch:
        for a in ch["plus1"]:
            scores[a] += 1


def _abilities_at(picks: Picks, rs, level: int) -> dict:
    scores = dict(picks.abilities)
    facet = rs.facets.get(picks.facet) or {}
    levels = facet.get("asi_levels") or rs.advancement.get("asi_levels", [])
    rule = rs.advancement.get("asi_rule")
    if rule in ("choice", "two_highest_plus_one"):
        for lvl, ch in asi_choices(rs, picks).items():
            if lvl <= level:
                _apply_asi(scores, ch)
        return {a: min(20, v) for a, v in scores.items()}
    for lvl in levels:
        if lvl > level:
            continue
        if rule == "plus_two_primary" and picks.asi_priority:
            order = list(picks.asi_priority) + sorted(ABILITIES, key=lambda a: -scores[a])
            gain = 2
            for a in order:
                while gain and scores[a] < 20:
                    scores[a] += 1
                    gain -= 1
    return scores


def _ctx(level, pb, mods, casting_ability, tradition):
    cm = mods[casting_ability] if casting_ability else None
    soul = cm if tradition == "invocation" and cm is not None else None
    dc = 8 + pb + cm if cm is not None else None
    return Ctx(level, pb, mods, cm, soul, spell_dc=dc)


def _path(rs, picks) -> dict:
    """The legacy v0.2 path entry, or {} (Amendment 2: no paths; nothing binds to them)."""
    return (rs.paths.get(picks.path) or {}) if picks.path else {}


# ================================================================ tracks (Amendment 2)

PROGRESSION_ORDER = {"half": 1, "full": 2}


def track_depth(rs, picks) -> dict:
    """{track: number of talents taken that carry that track tag}."""
    d = {}
    for tid in picks.talents.values():
        tr = (rs.talents.get(tid) or {}).get("track")
        if tr:
            d[tr] = d.get(tr, 0) + 1
    return d


def main_track(depth: dict, weight: Optional[dict] = None, tie: str = "steel") -> Optional[str]:
    """DESIGN v0.2 §1.2 step 2: Steel if depth.steel + weight.steel ≥ depth.spell +
    weight.spell, else Spell (ties to ``tie``). None when nothing is tracked or weighted."""
    weight = weight or {}
    tot = {t: depth.get(t, 0) + weight.get(t, 0) for t in ("steel", "spell")}
    if tot["steel"] == 0 and tot["spell"] == 0:
        return None
    if tot["steel"] == tot["spell"]:
        return tie
    return "steel" if tot["steel"] > tot["spell"] else "spell"


def picks_main_track(rs, picks) -> Optional[str]:
    tracks = rs.raw.get("tracks") or {}
    weight = (tracks.get("facet_weight") or {}).get(picks.facet) or {}
    tie = (tracks.get("main_track") or {}).get("tie", "steel")
    return main_track(track_depth(rs, picks), weight, tie)


def track_ranks(rs, picks) -> list:
    """[(rank id, effect)] granted by the tracks at this level (§1.2 step 3): a rank applies
    iff depth ≥ rank.depth, level ≥ rank.level, and (not rank.main, or its track is main).
    An effect with ``facets:`` applies only to those Facets."""
    tracks = rs.raw.get("tracks") or {}
    if not tracks:
        return []
    depth = track_depth(rs, picks)
    main = picks_main_track(rs, picks)
    out = []
    for tname, tdef in tracks.items():
        if not isinstance(tdef, dict) or "ranks" not in tdef:
            continue
        dep = depth.get(tname, 0)
        for rank in tdef["ranks"]:
            if int(rank.get("depth", 1)) > dep or int(rank.get("level", 1)) > picks.level:
                continue
            if rank.get("main") and main != tname:
                continue
            for e in rank.get("effects") or []:
                if e.get("facets") and picks.facet not in e["facets"]:
                    continue
                out.append((rank["id"], dict(e)))
    return out


def _casting_sources(rs, picks) -> list:
    """[(source, tradition, ability spec, progression)] for the picks."""
    facet = rs.facets[picks.facet]
    out = []
    ranks = [(rid, e) for rid, e in track_ranks(rs, picks) if e["type"] == "casting"]
    if ranks:
        best = max(ranks, key=lambda re: PROGRESSION_ORDER.get(re[1].get("progression"), 0))
        trad = best[1].get("tradition") or facet.get("tradition") or picks.tradition
        spec = best[1].get("ability") or facet.get("casting_ability")
        if spec is None and trad:
            spec = ((rs.spells_raw.get("traditions") or {}).get(trad) or {}).get("ability")
        out.append((best[0], trad, spec, best[1].get("progression", "half")))
    path = _path(rs, picks)
    if path.get("casting") and facet.get("tradition"):
        out.append(("path", facet["tradition"], facet.get("casting_ability"),
                    path["casting"].get("progression", "full")))
    for l in sorted(picks.talents):
        t = rs.talents.get(picks.talents[l]) or {}
        for e in t.get("effects") or []:
            if e["type"] == "casting":
                out.append((t["id"], e.get("tradition"), e.get("ability"),
                            e.get("progression", "half")))
    return out


def check(rs, picks: Picks) -> list:
    """Every rule the picks break (empty list = legal)."""
    errs = []
    lv = picks.level
    lo, hi = rs.raw["levels"]["min"], rs.raw["levels"]["max"]
    if not lo <= lv <= hi:
        return [f"level {lv} outside {lo}–{hi}"]
    facet = rs.facets.get(picks.facet)
    if facet is None:
        return [f"unknown Facet {picks.facet!r}"]
    if rs.paths and facet.get("paths") and picks.path not in facet["paths"]:
        errs.append(f"the {picks.facet} Facet has no {picks.path!r} path "
                    f"(paths: {facet.get('paths')})")
    if not rs.paths and picks.path:
        errs.append(f"this ruleset has no paths; drop path {picks.path!r}")

    # ---- abilities
    missing = [a for a in ABILITIES if a not in picks.abilities]
    if missing:
        return errs + [f"missing ability score {a}" for a in missing]
    if any(not 3 <= picks.abilities[a] <= 20 for a in ABILITIES):
        errs.append("ability scores must be 3–20")
    bg = rs.backgrounds.get(picks.background) if picks.background else None
    if picks.background and bg is None:
        errs.append(f"unknown background {picks.background!r}")
    if picks.base_abilities is not None:
        base = [picks.base_abilities[a] for a in ABILITIES]
        if sorted(base) != STANDARD_ARRAY:
            if any(s not in POINT_BUY_COST for s in base) or \
                    sum(POINT_BUY_COST[s] for s in base) > 27:
                errs.append("base abilities are neither the standard array nor a 27-point buy")
        bonus = background_bonus(bg)
        want = {a: picks.base_abilities[a] + bonus.get(a, 0) for a in ABILITIES}
        if want != {a: picks.abilities[a] for a in ABILITIES}:
            errs.append("final abilities do not equal base + background bonuses")

    # ---- talent and knack slots
    adv = rs.advancement
    for l in picks.talents:
        if l not in adv["talent_levels"]:
            errs.append(f"L{l}: no talent pick at this level (talent levels {adv['talent_levels']})")
        elif l > lv:
            errs.append(f"L{l}: talent chosen above character level {lv}")
    for l in adv["talent_levels"]:
        if l <= lv and l not in picks.talents:
            errs.append(f"L{l}: no talent chosen")
    if picks.knacks is not None:
        for l in picks.knacks:
            if l not in adv.get("knack_levels", []):
                errs.append(f"L{l}: no knack pick at this level "
                            f"(knack levels {adv.get('knack_levels')})")
            elif l > lv:
                errs.append(f"L{l}: knack chosen above character level {lv}")
        for l in adv.get("knack_levels", []):
            if l <= lv and l not in picks.knacks:
                errs.append(f"L{l}: no knack chosen")

    # ---- talents
    taken, cross = [], []
    is_caster = bool(_path(rs, picks).get("casting"))
    for l in sorted(picks.talents):
        tid = picks.talents[l]
        t = rs.talents.get(tid)
        if t is None:
            errs.append(f"L{l}: {tid!r} is not a talent"
                        + (" (it is a knack)" if tid in rs.knacks else ""))
            continue
        if picks.facet not in (t.get("menus") or []):
            cross.append(tid)
        rp = t.get("requires_path") if rs.paths else None
        if rp and rp != picks.path:
            errs.append(f"L{l}: {tid} requires the {rp} path")
        if l < int(t.get("min_level", 1)):
            errs.append(f"L{l}: {tid} needs level {t['min_level']}")
        req = t.get("requires")
        if isinstance(req, str) and req not in taken:
            errs.append(f"L{l}: {tid} requires {req} first")
        if isinstance(req, dict) and req.get("casting") and not is_caster:
            errs.append(f"L{l}: {tid} requires spellcasting")
        if tid in taken and not t.get("repeatable"):
            errs.append(f"L{l}: {tid} taken twice")
        if any(e["type"] == "casting" for e in t.get("effects") or []):
            is_caster = True
        taken.append(tid)
    limit = rs.build_rules.get("controlled_creature_limit")
    if limit is not None:
        companions = [tid for tid in taken for e in (rs.talents.get(tid) or {}).get("effects") or []
                      if e["type"] in ("companion",)]
        if len(companions) > limit:
            errs.append(f"E2: {len(companions)} controlled creatures ({', '.join(companions)}); "
                        f"the limit is {limit}")
    cap = rs.build_rules.get("cross_facet_talent_cap")
    if cap is not None and len(cross) > cap:
        errs.append(f"{len(cross)} cross-Facet talents ({', '.join(cross)}); the cap is {cap}")
    casters = _casting_sources(rs, picks)
    if rs.build_rules.get("one_tradition") and len(casters) > 1:
        errs.append("a character casts from one tradition only; casting comes from "
                    + ", ".join(src for src, *_ in casters))

    # ---- V21 ability-score choices at 4th and 8th
    asi_levels = (rs.facets[picks.facet].get("asi_levels")
                  or rs.advancement.get("asi_levels", []))
    for l, ch in picks.asi.items():
        if l not in asi_levels or l > lv:
            errs.append(f"L{l}: no ability-score pick at this level (levels {asi_levels})")
            continue
        if rs.advancement.get("asi_rule") != "choice":
            errs.append(f"L{l}: this ruleset's ability increases are automatic")
            continue
        if not isinstance(ch, dict) or len(ch) != 1 or next(iter(ch)) not in ASI_FORMS:
            errs.append(f"L{l}: pick exactly one of +2 to one ability, +1 to two, or a knack "
                        f"({{plus2: a}} | {{plus1: [a, b]}} | {{knack: id}}), not {ch!r}")
            continue
        if "plus2" in ch and ch["plus2"] not in ABILITIES:
            errs.append(f"L{l}: unknown ability {ch['plus2']!r}")
        if "plus1" in ch and (len(set(ch["plus1"])) != 2
                              or not set(ch["plus1"]) <= set(ABILITIES)):
            errs.append(f"L{l}: +1 goes to two different abilities, not {ch['plus1']!r}")
        if "knack" in ch and ch["knack"] not in rs.knacks:
            errs.append(f"L{l}: {ch['knack']!r} is not a knack")
    if rs.advancement.get("asi_rule") == "choice" and not any(
            e.startswith(f"L{l}:") for e in errs for l in picks.asi):
        running = dict(picks.abilities)
        for l, ch in sorted(asi_choices(rs, picks).items()):
            _apply_asi(running, ch)
            over = [a for a in ABILITIES if running[a] > 20]
            if over:
                errs.append(f"L{l}: {', '.join(over)} would go above 20")

    # ---- knacks
    if picks.knacks is not None:
        seen = [bg["knack"]] if bg and bg.get("knack") else []
        seen += [ch["knack"] for ch in picks.asi.values() if isinstance(ch, dict) and "knack" in ch]
        for l in sorted(picks.knacks):
            kid = picks.knacks[l]
            k = rs.knacks.get(kid)
            if k is None:
                errs.append(f"L{l}: {kid!r} is not a knack"
                            + (" (it is a talent)" if kid in rs.talents else ""))
                continue
            if kid in seen and not k.get("repeatable"):
                errs.append(f"L{l}: knack {kid} taken twice")
            seen.append(kid)

    # ---- casting ability and domains
    if casters:
        _, trad, spec, _ = casters[0]
        tdef = (rs.spells_raw.get("traditions") or {}).get(trad) or {}
        allowed = []
        for a in (tdef.get("ability") or ([spec] if isinstance(spec, str) else spec or [])):
            allowed += ["wis", "cha"] if a == "soul" else [a]
        resolved = resolve_casting_ability(spec or tdef.get("ability"), picks.abilities)
        if picks.casting_ability is not None and picks.casting_ability != resolved:
            errs.append(f"{trad} casts with {resolved} for these scores, "
                        f"not {picks.casting_ability}")
        want = _domain_count(rs, picks)
        if len(picks.domains) != want:
            errs.append(f"{len(picks.domains)} domains chosen; this build has {want}")
        if trad is None:
            errs.append("a Body caster names its tradition (invocation or thaumaturgy) with "
                        "its first Spell talent")
        prismatic_ok = sum(int(e.get("count", 1)) for _, e in track_ranks(rs, picks)
                           if e["type"] == "domains" and e.get("prismatic"))
        prismatic = [d for d in picks.domains if (rs.domains.get(d) or {}).get("prismatic")]
        if rs.raw.get("tracks") and len(prismatic) > prismatic_ok:
            errs.append(f"prismatic domain(s) {prismatic} need Deep Magic")
        for d in picks.domains:
            dd = rs.domains.get(d)
            if dd is None:
                errs.append(f"unknown domain {d!r}")
            elif dd.get("tradition") and trad and dd["tradition"] != trad:
                errs.append(f"domain {d} is {dd['tradition']}, not {trad}")
        if len(set(picks.domains)) != len(picks.domains):
            errs.append("the same domain twice")
    elif picks.domains:
        errs.append("domains chosen but the build doesn't cast")

    # ---- kit
    armor = picks.kit.get("armor")
    prof_armor = _armor_profs(rs, picks)
    if armor:
        if armor not in ARMOR:
            errs.append(f"unknown armor {armor!r}")
        elif ARMOR[armor][0] not in prof_armor:
            errs.append(f"not proficient with {ARMOR[armor][0]} armor ({armor})")
    if picks.kit.get("shield") and "shields" not in prof_armor:
        errs.append("not proficient with shields")
    for w in picks.kit.get("weapons") or []:
        if w not in WEAPONS:
            errs.append(f"unknown weapon {w!r}")
    return errs


def _domain_count(rs, picks) -> int:
    if rs.raw.get("tracks"):
        n = sum(int(e.get("count", 1)) for _, e in track_ranks(rs, picks) if e["type"] == "domains")
    else:
        n = int(rs.spells_raw.get("casting", {}).get("domains_on_path", 1))
    for tid in picks.talents.values():
        t = rs.talents.get(tid) or {}
        for e in active_effects(t, picks.level):
            if e["type"] == "domains":
                n += int(e.get("count", 1))
    return n


def _rank_and_talent_effects(rs, picks):
    for rid, e in track_ranks(rs, picks):
        yield rid, e
    for tid in picks.talents.values():
        for e in (rs.talents.get(tid) or {}).get("effects") or []:
            yield tid, e


def _armor_profs(rs, picks) -> set:
    facet = rs.facets[picks.facet]
    profs = set(facet.get("armor") or [])
    for _, e in track_ranks(rs, picks):
        if e["type"] == "armor_proficiency":
            cats = e.get("categories") or []
            profs |= set(cats.get(picks.facet) or []) if isinstance(cats, dict) else set(cats)
    add = _path(rs, picks).get("armor_add") or {}
    profs |= set(add.get(picks.facet) or [])
    for tid in picks.talents.values():
        for e in (rs.talents.get(tid) or {}).get("effects") or []:
            if e["type"] == "armor_proficiency":
                cats = e.get("categories") or []
                if isinstance(cats, dict):
                    cats = cats.get(picks.facet) or []
                profs |= set(cats)
    return profs


def _weapon_profs(rs, picks) -> set:
    facet = rs.facets[picks.facet]
    profs = set(facet.get("weapons") or [])
    profs |= set(_path(rs, picks).get("weapons_add") or [])
    for _, e in track_ranks(rs, picks):
        if e["type"] == "weapon_proficiency":
            profs |= set(e.get("categories") or [])
    for tid in picks.talents.values():
        for e in (rs.talents.get(tid) or {}).get("effects") or []:
            if e["type"] == "weapon_proficiency":
                profs |= set(e.get("categories") or [])
    return profs


def build(rs, picks: Picks) -> Character:
    errs = check(rs, picks)
    if errs:
        raise BuildError(errs)
    lv = picks.level
    facet = rs.facets[picks.facet]
    path = _path(rs, picks)
    pb = rs.prof(lv)
    abil = _abilities_at(picks, rs, lv)
    mods = {a: mod(s) for a, s in abil.items()}

    # ---- effects active at this level: facet ladder, path ladder, talents, knacks
    effects, features = [], []
    depth = track_depth(rs, picks)
    sdepth = (rs.raw.get("tracks") or {}).get("scaling_depth")
    for feat in list(facet.get("features") or []) + list(path.get("features") or []):
        if int(feat.get("level", 1)) > lv:
            continue
        if feat.get("path") and feat["path"] != picks.path:
            continue
        if feat.get("requires_talent") and feat["requires_talent"] not in picks.talents.values():
            continue
        features.append(feat.get("id"))
        effects += [(feat.get("id"), e) for e in active_effects(feat, lv, facet=picks.facet)]
    ranks = track_ranks(rs, picks)
    for rid in dict.fromkeys(r for r, _ in ranks):
        features.append(rid)
    effects += ranks
    for l in sorted(picks.talents):
        t = rs.talents[picks.talents[l]]
        features.append(t["id"])
        effects += [(t["id"], e) for e in active_effects(t, lv, depth=depth,
                                                         scaling_depth=sdepth, facet=picks.facet)]
    bg = rs.backgrounds.get(picks.background) if picks.background else None
    kn = ([bg["knack"]] if bg and bg.get("knack") else []) + list((picks.knacks or {}).values())
    kn += [ch["knack"] for ch in asi_choices(rs, picks).values() if "knack" in ch]
    for kid in kn:
        features.append(kid)
        effects += [(kid, e) for e in active_effects(rs.knacks[kid], lv)]

    # ---- casting
    tradition = progression = casting_ability = None
    casters = _casting_sources(rs, picks)
    if casters:
        _, tradition, spec, progression = casters[0]
        tdef = (rs.spells_raw.get("traditions") or {}).get(tradition) or {}
        casting_ability = resolve_casting_ability(spec or tdef.get("ability"), picks.abilities)
    ctx = _ctx(lv, pb, mods, casting_ability, tradition)

    # ---- hit points: hit die + Con at 1st (Facets d20: hit die + 8 + Con, V35), then
    #      half die + 1 + Con per level (fixed)
    hd = int(facet["hit_die"])
    if picks.facet in (path.get("applies_hit_die_step_to") or []):
        hd += 2 * int(path.get("hit_die_step", 0))
    for _, e in effects:
        if e["type"] == "hit_die_step":
            hd += 2 * eval_int(e.get("value", 1), ctx)
    hd = min(hd, int(rs.build_rules.get("max_hit_die", 12)))
    dice, flat = HP_FIRST[rs.advancement.get("hp_first", "hit_die_plus_con")]
    first = dice * hd + flat
    hp = first + mods["con"] + (lv - 1) * (hd // 2 + 1 + mods["con"])
    for _, e in effects:
        if e["type"] == "hp_per_level":
            hp += eval_int(e.get("value", 1), ctx) * lv

    # ---- saves (the sheet includes your own Warden bonus)
    save_profs = set(facet.get("saves") or [])
    save_bonus = 0
    for _, e in effects:
        if e["type"] == "save_proficiency":
            if e.get("abilities"):
                save_profs |= set(e["abilities"])
            elif e.get("choose"):
                opts = [a for a in e.get("from") or [] if a not in save_profs]
                save_profs |= set(opts[: int(e["choose"])])   # engine choice: listed order
        if e["type"] == "save_bonus" and "self" in (e.get("targets") or ["self"]):
            save_bonus += eval_int(e.get("value", 0), ctx, e.get("min"))
    saves = {a: mods[a] + (pb if a in save_profs else 0) + save_bonus for a in ABILITIES}

    # ---- armor class
    armor = picks.kit.get("armor")
    shield = bool(picks.kit.get("shield"))
    if armor:
        cat, base, cap = ARMOR[armor]
        dex = mods["dex"] if cap is None else (min(mods["dex"], cap) if cap else 0)
        ac = base + dex
    else:
        ac = 10 + mods["dex"]
    for _, e in effects:
        if e["type"] == "ac_formula" and not armor:
            if shield and not e.get("shield_allowed", True):
                continue
            ac = max(ac, int(e.get("base", 10)) + sum(mods[a] for a in e.get("add") or []))
    if shield:
        ac += 2
    for _, e in effects:
        if e["type"] == "ac_bonus":
            conds = set(_data._conditions(e))
            if ("armored" in conds and not armor) or ("shield" in conds and not shield) \
                    or ("unarmored" in conds and armor) or "adjacent_ally_aura" in conds:
                continue
            ac += eval_int(e.get("value", 0), ctx)

    # ---- spells: everything on your lists of a level you have a slot for
    slots, cantrips, spells_ = [], [], []
    if tradition:
        slots = rs.slot_row(progression, lv)
        pool = list(rs.common_list())
        for d in picks.domains:
            pool += list((rs.domains.get(d) or {}).get("spells") or [])
        for _, e in effects:
            if e["type"] == "spells_known":
                pool += [{"name": x, "level": e.get("max_level", 0)} if isinstance(x, str)
                         else x for x in e.get("spells") or []]
        seen = set()
        for sp in pool:
            name, slvl = sp["name"], int(sp.get("level", 0))
            if name in seen:
                continue
            if slvl == 0:
                cantrips.append(name)
                seen.add(name)
            elif slvl <= len(slots):
                spells_.append(name)
                seen.add(name)

    # ---- resources declared by effects
    resources = {}
    for src, e in effects:
        if e["type"] == "resource":
            uses = e.get("uses", 1)
            by = e.get("by_level") or {}
            for k in sorted(int(x) for x in by):
                if k <= lv:
                    uses = by.get(k, by.get(str(k)))
            resources[e.get("id", src)] = Uses(eval_int(uses, ctx, e.get("min")),
                                               e.get("recharge", "long"),
                                               int(e.get("short_rest_regain", 0)))

    weapon = _main_weapon(rs, picks, abil, pb, effects, ctx, armored=bool(armor))
    return Character(rs=rs, picks=picks, abilities=abil, hit_die=hd, hp=hp, ac=ac, prof=pb,
                     saves=saves, effects=effects, tradition=tradition,
                     progression=progression, casting_ability=casting_ability,
                     slots=slots, cantrips=cantrips, spells=spells_,
                     domains=list(picks.domains), weapon=weapon, resources=resources,
                     features=features, armored=bool(armor), shield=shield)


# ================================================================ weapons


def _weapon_filter(e) -> list:
    ws = e.get("weapon")
    return [ws] if isinstance(ws, str) else list(ws or ["any"])


def _weapon_ok(e, wdef: WeaponDef, *, shield: bool, two_handed: bool, armored: bool,
               str_based: bool) -> bool:
    ranged = "ranged" in wdef.props
    hv = "heavy" in wdef.props or wdef.versatile is not None
    ok = False
    for w in _weapon_filter(e):
        if (w == "any" or (w == "ranged" and ranged) or (w == "melee" and not ranged)
                or (w == "finesse" and "finesse" in wdef.props)
                or (w == "str_melee" and not ranged and str_based)
                or (w == "heavy_or_versatile_melee" and hv and not ranged)
                or w in wdef.props):
            ok = True
    if not ok:
        return False
    for c in _data._conditions(e):
        if (c == "one_handed_melee" and (ranged or two_handed)) \
                or (c == "heavy_or_versatile" and not hv) \
                or (c == "ranged_weapon" and not ranged) \
                or (c == "no_shield" and shield) or (c == "shield" and not shield) \
                or (c == "unarmored" and armored) or (c == "armored" and not armored):
            return False
    return True


_RUNTIME_CONDS = {"raging", "studied_target", "has_advantage", "ally_adjacent_to_target",
                  "advantage_or_ally_adjacent", "bloodied", "first_round", "attack_action",
                  "not_moved", "planned", "oath_kept"}


def _static(e) -> bool:
    """True if the effect applies all the time (no fight-state condition, no resource)."""
    return not (set(_data._conditions(e)) & _RUNTIME_CONDS) and not e.get("resource") \
        and not e.get("condition_any") and not e.get("trigger")


def _make_weapon(rs, picks, wid, abil, pb, effects, ctx, *, armored: bool) -> Weapon:
    wdef = WEAPONS[wid]
    shield = bool(picks.kit.get("shield"))
    mods = {a: mod(s) for a, s in abil.items()}
    ranged = "ranged" in wdef.props
    ability = "dex" if ranged else "str"
    if "finesse" in wdef.props and mods["dex"] > mods["str"]:
        ability = "dex"
    dice = wdef.dice
    two = "two_handed" in wdef.props
    if wdef.versatile and not shield:
        dice, two = wdef.versatile, True
    # Martial Arts: Dex and a die floor for unarmed / simple melee / light melee weapons.
    for _, e in effects:
        if e["type"] != "martial_die" or ranged:
            continue
        conds = set(_data._conditions(e))
        if ("unarmored" in conds and armored) or ("no_shield" in conds and shield):
            continue
        applies = set(e.get("applies") or [])
        if (wdef.category == "simple" and "simple_melee" in applies) or \
                ("light" in wdef.props and "light_melee" in applies):
            md = Dice.parse("1" + e["die"] if str(e["die"]).startswith("d") else e["die"])
            if md.average > Dice.parse(dice).average:
                dice = str(md)
            if mods[e.get("ability", "dex")] > mods[ability]:
                ability = e.get("ability", "dex")
    str_based = ability == "str"
    profs = _weapon_profs(rs, picks)
    to_hit = mods[ability] + (pb if wdef.category in profs else 0)
    dmg = mods[ability]
    crit_min = 20
    for _, e in effects:
        if not _static(e) or e["type"] not in ("attack_bonus", "damage_bonus", "crit_range"):
            continue
        if e.get("applies") == "spell":
            continue
        if not _weapon_ok(e, wdef, shield=shield, two_handed=two, armored=armored,
                          str_based=str_based):
            continue
        if e["type"] == "attack_bonus":
            to_hit += eval_int(e.get("value", 0), ctx)
        elif e["type"] == "damage_bonus":
            dmg += eval_int(e.get("value", 0), ctx)
        else:
            crit_min = min(crit_min, int(e.get("min", 20)))
    hv = "heavy" in wdef.props or wdef.versatile is not None
    return Weapon(wid, Dice.parse(dice), to_hit, dmg, wdef.dtype, ranged,
                  "finesse" in wdef.props, two, 1, crit_min, hv, str_based)


def _main_weapon(rs, picks, abil, pb, effects, ctx, *, armored: bool) -> Optional[Weapon]:
    ws = [w for w in picks.kit.get("weapons") or [] if w in WEAPONS]
    if not ws:
        return None
    built = [_make_weapon(rs, picks, w, abil, pb, effects, ctx, armored=armored) for w in ws]
    return max(built, key=lambda w: (min(0.95, max(0.05, (w.to_hit + 7) / 20))
                                     * (w.dice.average + w.mod), not w.ranged))


# ================================================================ combat profile


def _profile(ch: Character) -> CombatProfile:
    lv, mods, pb = ch.level, ch.mods, ch.prof
    ctx = _ctx(lv, pb, mods, ch.casting_ability, ch.tradition)
    p = CombatProfile(name=ch.picks.name, level=lv, prof=pb, hp=ch.hp, ac=ch.ac,
                      saves=dict(ch.saves), dex_mod=mods["dex"], abilities=dict(ch.abilities),
                      weapon=ch.weapon, features=list(ch.features), hit_die=ch.hit_die)
    for _, e in ch.effects:
        if e["type"] == "hit_dice_bonus":
            p.hd_bonus = eval_int(e.get("amount", 0), ctx)
    p.rider_limit = int(ch.rs.build_rules.get("rider_limit_per_turn", 1))
    if ch.tradition:
        p.caster = CasterProfile(
            tradition=ch.tradition, kind=ch.progression, ability=ch.casting_ability,
            mod=ch.casting_mod, attack=ch.spell_attack, dc=ch.save_dc, slots=list(ch.slots),
            cantrips=list(ch.cantrips), spells=list(ch.spells), domains=list(ch.domains))
    for src, e in ch.effects:
        _apply_effect(p, ch, src, e, ctx)
    # A precast AC spell (Mage Armor) on the character's lists: cast once a day, unarmored.
    if p.caster and not ch.armored:
        for name in p.caster.spells:
            sp = ch.rs.sim_spells.get(name) or {}
            if sp.get("model") == "ac_set" and sp.get("precast") and p.caster.slots:
                alt = int(sp.get("base", 13)) + mods[sp.get("add", "dex")] + (2 if ch.shield else 0)
                if alt > p.ac:
                    p.ac = alt
                    p.caster.slots[0] = max(0, p.caster.slots[0] - 1)
                    p.notes.append(f"{name} precast: AC {alt}, one 1st-level slot a day")
    if p.second_wind is None and p.heal_touch is None and p.heal_pool == 0 and p.caster \
            and any(s in ch.spells for s in ("Cure Wounds", "Healing Word")) and p.caster.heal_boost:
        p.healer = True
    return p


def _uses(ch, e, ctx, default: int = 1) -> Uses:
    rid = e.get("resource")
    if rid and rid in ch.resources:
        return ch.resources[rid]
    if "uses" in e:
        return Uses(eval_int(e["uses"], ctx, e.get("min")), e.get("recharge", "long"),
                    int(e.get("short_rest_regain", 0)))
    return Uses(default, "long")


_NOT_SIMULATED = {"speed_bonus", "cunning_action", "sculpt", "slot_recovery",
                  "surprise_immunity", "condition_immunity", "resource_refill",
                  "hit_dice_bonus", "forbid", "wild_shape", "spells_known", "domains",
                  "casting", "hp_per_level", "hit_die_step", "ac_formula", "ac_bonus",
                  "save_proficiency", "resource"}


def _apply_effect(p: CombatProfile, ch: Character, src: str, e: dict, ctx: Ctx) -> None:
    t = e["type"]
    conds = set(_data._conditions(e))
    if t in _data.NONCOMBAT_TYPES:
        return
    if t == "extra_attack":
        p.attacks_per_action = max(p.attacks_per_action, int(e.get("attacks", 2)))
    elif t == "extra_damage_dice":
        d, _ = eval_amount(e.get("dice"), ctx)
        if d is None:
            return
        any_of = set(e.get("condition_any") or [])
        all_of = conds & {"studied_target", "has_advantage", "ally_adjacent_to_target", "raging"}
        if "advantage_or_ally_adjacent" in conds:
            any_of |= {"has_advantage", "ally_adjacent_to_target"}
        p.riders.append(Rider(src if not e.get("id") else e["id"], d, frozenset(any_of),
                              frozenset(_weapon_filter(e)) - {"any"},
                              _uses(ch, e, ctx) if e.get("resource") else None,
                              bool(e.get("fallback")), e.get("damage_type", "radiant"),
                              bool(e.get("rider", True)), frozenset(all_of),
                              e.get("frequency", "once_per_turn") == "once_per_turn"))
    elif t == "damage_bonus":
        if "raging" in conds:
            p.rage = p.rage or {"damage": 0, "resist": set()}
            p.rage["damage"] = eval_int(e.get("value", 0), ctx)
        elif e.get("applies") == "spell" and p.caster:
            p.caster.spell_damage_bonus = eval_int(e.get("value", 0), ctx)
        elif e.get("applies") == "cantrip" and p.caster:
            p.caster.cantrip_damage_bonus = eval_int(e.get("value", 0), ctx)
        elif "studied_target" in conds:
            p.studied_damage_bonus = eval_int(e.get("value", 0), ctx)
    elif t == "attack_bonus" or t == "crit_range":
        if t == "crit_range" and "studied_target" in conds:
            p.crit_min_studied = min(p.crit_min_studied, int(e.get("min", 20)))
    elif t == "heal":
        d, flat = eval_amount(e.get("amount"), ctx)
        if e.get("trigger") == "on_crit":
            p.crit_heal = flat
            return
        u = _uses(ch, e, ctx)
        if e.get("targets") in ("self", ["self"]):
            p.second_wind = {"uses": u, "dice": d, "bonus": flat}
        else:
            p.heal_touch = {"uses": u, "dice": d, "bonus": flat}
            p.healer = True
    elif t == "save_damage":
        d, _ = eval_amount(e.get("dice"), ctx)
        _, add = eval_amount(e.get("add"), ctx)
        p.channel_damage = {"dice": d, "bonus": add, "save": e.get("save", "con"),
                            "half": bool(e.get("half_on_success", True)),
                            "dtype": e.get("damage_type", "radiant")}
    elif t == "extra_action":
        p.action_surge = _uses(ch, e, ctx)
    elif t == "reroll":
        _, add = eval_amount(e.get("add", 0), ctx)
        p.reroll_save = {"uses": _uses(ch, e, ctx), "add": add}
    elif t == "stance":
        p.rage = p.rage or {"damage": 0, "resist": set()}
        p.rage["uses"] = _uses(ch, e, ctx)
    elif t == "resistance":
        types = set(e.get("damage_types") or [])
        if "raging" in conds:
            p.rage = p.rage or {"damage": 0, "resist": set()}
            p.rage["resist"] = set(p.rage.get("resist", set())) | types
        elif not conds:
            p.resist |= types
    elif t == "reckless":
        p.reckless = True
    elif t == "drop_to_one":
        p.drop_to_one = {"uses": _uses(ch, e, ctx),
                         "needs": "raging" if "raging" in conds else None}
    elif t == "max_damage_next_hit":
        p.max_next_hit = True
    elif t == "martial_die":
        pass   # folded into the weapon
    elif t == "bonus_attack":
        if armored_or_shield_blocks(ch, conds):
            return
        md = _martial_die(ch)
        m = max(ch.mods["dex"], ch.mods["str"])
        w = Weapon("unarmed strike", md, m + ch.prof, m, "bludgeoning")
        if e.get("resource"):
            p.flurry = {"count": int(e.get("count", 2)), "cost": int(e.get("cost", 1))}
            p.focus = _uses(ch, e, ctx)
        else:
            p.bonus_attack = w
    elif t == "condition_on_hit":
        if (e.get("inflicts") or e.get("condition")) == "stunned":
            p.stun = {"dc": eval_int(e.get("dc", "8+pb+wis"), ctx), "cost": int(e.get("cost", 1))}
            if e.get("resource") and p.focus is None:
                p.focus = _uses(ch, e, ctx)
    elif t == "halve_damage":
        p.halve_damage = True
    elif t == "evasion":
        p.evasion = True
    elif t == "redirect_hit":
        p.redirect = eval_int(e.get("reduce_by", 0), ctx)
    elif t == "aoe_rider":
        w = ch.weapon
        if w is not None and not w.ranged and w.heavy_or_versatile:
            p.cleave = eval_int(e.get("damage", 0), ctx)
    elif t == "studied_target":
        p.study = _uses(ch, e, ctx)
    elif t == "advantage":
        on = e.get("roll") or e.get("on") or []
        on = [on] if isinstance(on, str) else on
        if "initiative" in on:
            p.initiative_advantage = True
            return
        if "attack" not in on:
            return
        scope = e.get("scope")
        if scope == "next_ranged_attack_this_turn":
            p.aim = True
        elif "first_round" in conds:
            p.master_plan = _uses(ch, e, ctx)
            p.master_plan_rounds = int(e.get("rounds", 1))
    elif t == "impose_disadvantage":
        p.anticipate = True
    elif t == "companion":
        g = e.get("guard") or {}
        d, flat = eval_amount(g.get("reduce"), ctx)
        p.guard = {"dice": d, "bonus": flat}
    elif t == "temp_hp":
        _, amt = eval_amount(e.get("amount"), ctx)
        tg = e.get("targets") or {}
        if e.get("trigger") == "fight_start":
            allies = eval_int(tg.get("allies", 0), ctx) if isinstance(tg, dict) else 0
            p.field_kit = {"amount": amt, "allies": allies}
        else:
            p.temp_hp += amt
    elif t == "spark":
        if e.get("grant") and e.get("resource"):
            p.kindle = _uses(ch, e, ctx)
        if e.get("floor"):
            p.spark_floor = max(p.spark_floor, int(e["floor"]))
        if e.get("subtract"):
            p.spark_subtract = True
    elif t == "heal_pool":
        p.heal_pool += eval_int(e.get("size", 0), ctx)
        p.healer = True
    elif t == "heal_boost":
        if p.caster:
            p.caster.heal_boost = True
        p.healer = True
    elif t == "save_bonus":
        if "allies" in (e.get("targets") or []):
            p.save_aura = eval_int(e.get("value", 0), ctx, e.get("min"))
    elif t == "initiative_bonus":
        p.initiative_bonus = eval_int(e.get("value", 0), ctx)
    elif t == "maximize_spell":
        if p.caster:
            p.caster.maximize = _uses(ch, e, ctx)
    elif t == "forbid":
        if p.caster and "raging" in conds:
            p.caster.forbidden_while_raging = True
    elif t in _NOT_SIMULATED:
        if t in ("wild_shape", "cunning_action", "slot_recovery"):
            p.notes.append(f"{src}: {t} not simulated")
    else:
        p.notes.append(f"{src}: {t} not simulated")


def armored_or_shield_blocks(ch, conds) -> bool:
    return ("unarmored" in conds and ch.armored) or ("no_shield" in conds and ch.shield)


def _martial_die(ch) -> Dice:
    best = Dice(1, 4)
    for _, e in ch.effects:
        if e["type"] == "martial_die":
            d = Dice.parse("1" + e["die"] if str(e["die"]).startswith("d") else e["die"])
            if d.average > best.average:
                best = d
    return best
