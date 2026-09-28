"""Load and validate the Facets d20 data (facets_d20/data/*.yaml, schema v0.2).

The schema is docs/DESIGN_facets_d20_v0_2.md §1. ``load()`` returns a ``Ruleset``;
anything the engine would have to guess at is a ``DataError`` at load time, not a
silent pass (unknown effect types, unknown condition keywords, dangling ids).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml

REPO = Path(__file__).resolve().parents[2]
DATA_DIR = REPO / "facets_d20" / "data"
RULES_FILE = DATA_DIR / "facets_d20.yaml"
SPELLS_FILE = DATA_DIR / "facets_d20_spells.yaml"

ABILITIES = ("str", "dex", "con", "int", "wis", "cha")

# §1.4 — the effect vocabulary. (N) = non-combat, the only types a knack may use.
EFFECT_TYPES = {
    "hp_per_level", "hit_die_step", "ac_formula", "ac_bonus", "attack_bonus",
    "damage_bonus", "extra_damage_dice", "crit_range", "extra_attack", "bonus_attack",
    "extra_action", "advantage", "impose_disadvantage", "resistance", "damage_reduction",
    "redirect_hit", "heal", "heal_pool", "heal_boost", "temp_hp", "drop_to_one", "reroll",
    "save_proficiency", "save_bonus", "condition_on_hit", "aoe_rider", "speed_bonus",
    "spark", "resource", "casting", "domains", "spells_known", "wild_shape", "companion",
    "surprise_immunity",
    # §1.4a additions (binding, 2026-09-28)
    "stance", "reckless", "forbid", "martial_die", "cunning_action", "halve_damage",
    "evasion", "sculpt", "maximize_spell", "studied_target", "slot_recovery",
    "initiative_bonus", "save_damage", "condition_immunity", "resource_refill",
    "max_damage_next_hit", "hit_dice_bonus",
    # engine note E-7 (Amendment 2: no paths — proficiencies come from talents)
    "armor_proficiency", "weapon_proficiency",
    # (N)
    "skill_proficiency", "expertise", "tool_proficiency", "languages", "narrative",
}
NONCOMBAT_TYPES = {"skill_proficiency", "expertise", "tool_proficiency", "languages",
                   "narrative"}
KNACK_EXTRA_TYPES = {"hit_dice_bonus"}   # §1.4a (N*): the one knack effect the sim models

CONDITIONS = {"advantage_or_ally_adjacent", "studied_target", "raging", "unarmored",
              "armored", "shield", "no_shield", "one_handed_melee", "heavy_or_versatile",
              "ranged_weapon", "bloodied", "first_round", "attack_action",
              # §1.4a
              "has_advantage", "ally_adjacent_to_target", "not_moved", "planned",
              "oath_kept", "adjacent_ally_aura",
              "conscious"}   # used by Alert; to be listed in §1.4a (engine note E-6)

SIM_SPELL_MODELS = {"attack", "save", "area_save_damage", "auto", "heal", "aura",
                    "weapon_rider", "weapon_cantrip", "disable", "shield", "buff_attack",
                    "ac_set", "ac_bonus"}

_ATOM = r"(pb|level|half_level|half_level_round_up|slot_level|casting|soul|spell|str|dex|con|int|wis|cha)"
_TERM = re.compile(r"^(\d+|\d+d\d+|" + _ATOM + r"|\d+\*" + _ATOM + r")$")


class DataError(ValueError):
    """The yaml breaks the schema; the message names the entry and the field."""


def check_expr(expr, where: str) -> None:
    """Validate a §1.4 expression (int or ``a+b+...`` of known terms)."""
    if isinstance(expr, bool):
        raise DataError(f"{where}: boolean is not an expression")
    if isinstance(expr, int):
        return
    if not isinstance(expr, str) or not expr.strip():
        raise DataError(f"{where}: bad expression {expr!r}")
    for term in expr.replace(" ", "").split("+"):
        if not _TERM.match(term):
            raise DataError(f"{where}: unknown term {term!r} in {expr!r}")


def _conditions(effect) -> list:
    c = effect.get("condition")
    if c is None:
        return []
    return list(c) if isinstance(c, (list, tuple)) else [c]


def check_effect(effect, where: str, *, knack: bool = False) -> None:
    if not isinstance(effect, dict) or "type" not in effect:
        raise DataError(f"{where}: effect without a type: {effect!r}")
    t = effect["type"]
    if t not in EFFECT_TYPES:
        raise DataError(f"{where}: unknown effect type {t!r}")
    if knack and t not in NONCOMBAT_TYPES | KNACK_EXTRA_TYPES:
        on = effect.get("roll") or effect.get("on") or []
        if not (t == "advantage" and set(on if isinstance(on, list) else [on]) <= {"check"}):
            raise DataError(f"{where}: a knack may only use non-combat effects, not {t!r}")
    # condition_on_hit names what it inflicts (`inflicts:`, formerly `condition:`).
    gates = [] if (t == "condition_on_hit" and "inflicts" not in effect) else _conditions(effect)
    for kw in gates + list(effect.get("condition_any") or []) + \
            list(effect.get("condition_target") or []):
        if kw not in CONDITIONS:
            raise DataError(f"{where}: unknown condition keyword {kw!r}")
    for key in ("value", "uses", "dc", "amount", "size"):
        if key in effect and effect[key] is not None and not isinstance(effect[key], dict):
            check_expr(effect[key], f"{where}.{key}")


@dataclass
class Ruleset:
    raw: dict
    spells_raw: dict
    facets: dict = field(default_factory=dict)
    paths: dict = field(default_factory=dict)
    talents: dict = field(default_factory=dict)
    knacks: dict = field(default_factory=dict)
    backgrounds: dict = field(default_factory=dict)
    presets: dict = field(default_factory=dict)
    domains: dict = field(default_factory=dict)
    sim_spells: dict = field(default_factory=dict)
    sim_builds: dict = field(default_factory=dict)

    @property
    def version(self):
        return self.raw.get("version")

    @property
    def advancement(self) -> dict:
        return self.raw["advancement"]

    @property
    def build_rules(self) -> dict:
        return self.raw.get("build_rules", {})

    def prof(self, level: int) -> int:
        return int(self.raw["proficiency_bonus"][level])

    def entry(self, tid: str) -> Optional[dict]:
        return self.talents.get(tid) or self.knacks.get(tid)

    def common_list(self) -> list:
        return list(self.spells_raw.get("common_list") or [])

    def slot_row(self, progression: str, level: int) -> list:
        table = self.spells_raw[f"{progression}_table"]
        return list(table.get(level) or table.get(str(level)) or [])


def _index(entries, kind: str) -> dict:
    out = {}
    for e in entries or []:
        if "id" not in e:
            raise DataError(f"{kind} entry without an id: {e!r}")
        if e["id"] in out:
            raise DataError(f"duplicate {kind} id {e['id']!r}")
        out[e["id"]] = e
    return out


# advancement.hp_first: 1st-level hit points = dice x hit die maximum + flat + Con modifier.
# The SRD's hit die + Con, and Facets d20's (balance pass V35): hit die + 8 + Con.
HP_FIRST_RULES = {"hit_die_plus_con": (1, 0), "hit_die_plus_eight_plus_con": (1, 8)}


def from_dicts(raw: dict, spells_raw: dict) -> Ruleset:
    """Build and validate a Ruleset from already-parsed yaml (tests use this)."""
    if str(raw.get("version")) != "0.2":
        raise DataError(f"engine needs facets_d20.yaml version 0.2, found {raw.get('version')!r}")
    for key in ("proficiency_bonus", "advancement", "facets", "talents"):
        if key not in raw:
            raise DataError(f"facets_d20.yaml: missing top-level {key!r}")
    hp_first = raw["advancement"].get("hp_first", "hit_die_plus_con")
    if hp_first not in HP_FIRST_RULES:
        raise DataError(f"advancement.hp_first: unknown rule {hp_first!r}")
    rs = Ruleset(raw=raw, spells_raw=spells_raw)
    rs.facets = dict(raw["facets"])
    rs.paths = dict(raw.get("paths") or {})
    rs.talents = _index(raw.get("talents"), "talent")
    rs.knacks = _index(raw.get("knacks"), "knack")
    clash = set(rs.talents) & set(rs.knacks)
    if clash:
        raise DataError(f"ids used by both a talent and a knack: {sorted(clash)}")
    rs.backgrounds = _index(raw.get("backgrounds"), "background")
    rs.presets = _index(raw.get("presets"), "preset")
    rs.sim_builds = _index(raw.get("sim_builds"), "sim_build")
    spells_raw = _normalise_spells(spells_raw)
    rs.spells_raw = spells_raw
    rs.domains = {d["id"]: d for d in spells_raw.get("domains") or []}
    for s in spells_raw.get("sim_spells") or []:
        model = s.get("model")
        if model not in SIM_SPELL_MODELS:
            raise DataError(f"sim_spells {s.get('name')!r}: unknown model {model!r}")
        rs.sim_spells[s["name"]] = s

    for fid, f in rs.facets.items():
        for feat in f.get("features") or []:
            for i, e in enumerate(feat.get("effects") or []):
                check_effect(e, f"facets.{fid}.features.{feat.get('id')}[{i}]")
    for pid, p in rs.paths.items():
        for feat in p.get("features") or []:
            for i, e in enumerate(feat.get("effects") or []):
                check_effect(e, f"paths.{pid}.features.{feat.get('id')}[{i}]")
    for kind, table in (("talent", rs.talents), ("knack", rs.knacks)):
        for tid, t in table.items():
            for i, e in enumerate(t.get("effects") or []):
                check_effect(e, f"{kind}.{tid}.effects[{i}]", knack=kind == "knack")
            for lvl, effs in (t.get("scaling") or {}).items():
                for i, e in enumerate(effs or []):
                    check_effect(e, f"{kind}.{tid}.scaling.{lvl}[{i}]", knack=kind == "knack")
            for m in t.get("menus") or []:
                if m not in rs.facets:
                    raise DataError(f"{kind}.{tid}: unknown menu {m!r}")
            req = t.get("requires")
            if isinstance(req, str) and rs.entry(req) is None:
                raise DataError(f"{kind}.{tid}: requires unknown {req!r}")
    for bid, b in rs.backgrounds.items():
        k = b.get("knack")
        if k is not None and k not in rs.knacks:
            raise DataError(f"background.{bid}: unknown knack {k!r}")
    return rs


def _normalise_spells(sp: dict) -> dict:
    """Accept the v0.1 spells file shape until it is migrated (list traditions,
    ``traditions: [Name]`` on domains, no ids). Returns a v0.2-shaped copy."""
    sp = dict(sp)
    trad = sp.get("traditions")
    if isinstance(trad, list):
        sp["traditions"] = {
            t["name"].lower(): {"facet": t["facet"].lower(),
                                "ability": [a[:3].lower() for a in t["ability"]]}
            for t in trad}
    doms = []
    for d in sp.get("domains") or []:
        d = dict(d)
        d.setdefault("id", _slug(d["name"]))
        if "tradition" not in d and d.get("traditions"):
            d["tradition"] = str(d["traditions"][0]).lower()
        doms.append(d)
    sp["domains"] = doms
    sp["casting"] = dict(sp.get("casting") or {})
    for key in ("full_table", "half_table"):
        if key in sp:
            sp[key] = {int(k): v for k, v in sp[key].items()}
    return sp


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def slug(name: str) -> str:
    return _slug(name)


BASELINES_FILE = Path(__file__).resolve().parent / "data" / "srd_baselines.yaml"


@lru_cache(maxsize=2)
def load_baselines(path: Path = BASELINES_FILE) -> Ruleset:
    """The SRD 5.2.1 baseline classes as a Ruleset (DESIGN v0.2 §8 item 4, S-9).

    Their sim spells are the Facets ``sim_spells`` (same SRD spells, same numbers) plus
    ``sim_spells_extra`` for the few only a baseline uses."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    main = yaml.safe_load(SPELLS_FILE.read_text(encoding="utf-8"))
    sp = dict(raw["spells"])
    extra = list(sp.pop("sim_spells_extra", []))
    names = {e["name"] for e in extra}
    sp["sim_spells"] = [e for e in main.get("sim_spells") or [] if e["name"] not in names] + extra
    return from_dicts(raw["rules"], sp)


@lru_cache(maxsize=4)
def load(rules_path: Path = RULES_FILE, spells_path: Path = SPELLS_FILE) -> Ruleset:
    raw = yaml.safe_load(Path(rules_path).read_text(encoding="utf-8"))
    spells_raw = yaml.safe_load(Path(spells_path).read_text(encoding="utf-8"))
    return from_dicts(raw, spells_raw)
