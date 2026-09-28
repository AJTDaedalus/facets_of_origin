"""Build facets_d20's SRD monster ladder from the SRD 5.2 creature data.

    python -m tools.build_srd_monsters [--cache PATH]

Source: the Open5e v2 API, document ``srd-2024`` (the SRD 5.2 release; the same source
docs/RESEARCH_facets_d20_srd_check.md used as its cross-check), fetched once and cached.
Output: ``software/facets_d20/data/srd_monsters.yaml`` — the curated CR 1/8–12 ladder
the simulator uses. Every number (AC, HP, saves, to-hit, damage) is copied from the
retrieved data; damage is the average the SRD prints in each action's text ("13 (2d6 +
6) Slashing damage plus 3 (1d6) Fire damage" → 16). The curation below only picks
which monsters and how their Multiattack is composed, quoting the SRD Multiattack text
into the yaml so a reviewer can check it.

Includes material from the System Reference Document 5.2.1 by Wizards of the Coast LLC,
licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/legalcode).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

URL = "https://api.open5e.com/v2/creatures/?document__key=srd-2024&limit=400"
OUT = Path(__file__).resolve().parents[1] / "facets_d20" / "data" / "srd_monsters.yaml"

# name: multiattack as [(action, count), ...]. Two or more per CR; melee, ranged, casters.
LADDER = {
    "Bandit": [("Scimitar", 1)],
    "Guard": [("Spear", 1)],
    "Cultist": [("Ritual Sickle", 1)],
    "Kobold Warrior": [("Dagger", 1)],
    "Goblin Warrior": [("Scimitar", 1)],
    "Skeleton": [("Shortbow", 1)],
    "Wolf": [("Bite", 1)],
    "Zombie": [("Slam", 1)],
    "Priest Acolyte": [("Radiant Flame", 1)],
    "Scout": [("Longbow", 2)],
    "Tough": [("Mace", 1)],
    "Black Bear": [("Rend", 2)],
    "Hobgoblin Warrior": [("Longsword", 1)],
    "Worg": [("Bite", 1)],
    "Bugbear Warrior": [("Grab", 1)],
    "Dire Wolf": [("Bite", 1)],
    "Goblin Boss": [("Scimitar", 2)],
    "Animated Armor": [("Slam", 2)],
    "Spy": [("Shortsword", 1)],
    "Ogre": [("Greatclub", 1)],
    "Bandit Captain": [("Scimitar", 2)],
    "Priest": [("Radiant Flame", 2)],
    "Berserker": [("Greataxe", 1)],
    "Gargoyle": [("Claw", 2)],
    "Owlbear": [("Rend", 2)],
    "Knight": [("Greatsword", 2)],
    "Hobgoblin Captain": [("Greatsword", 2)],
    "Hell Hound": [("Bite", 2)],
    "Wight": [("Necrotic Sword", 2)],
    "Ettin": [("Battleaxe", 1), ("Morningstar", 1)],
    "Guard Captain": [("Longsword", 2)],
    "Ghost": [("Withering Touch", 2)],
    "Tough Boss": [("Warhammer", 2)],
    "Troll": [("Rend", 3)],
    "Hill Giant": [("Tree Club", 2)],
    "Gladiator": [("Spear", 3)],
    "Air Elemental": [("Thunderous Slam", 2)],
    "Wraith": [("Life Drain", 1)],
    "Mage": [("Arcane Burst", 3)],
    "Wyvern": [("Bite", 1), ("Sting", 1)],
    "Chimera": [("Ram", 1), ("Bite", 1), ("Claw", 1)],
    "Young White Dragon": [("Rend", 3)],
    "Stone Giant": [("Stone Club", 2)],
    "Giant Ape": [("Fist", 2)],
    "Young Black Dragon": [("Rend", 3)],
    "Oni": [("Claw", 2)],
    "Assassin": [("Shortsword", 3)],
    "Frost Giant": [("Frost Axe", 2)],
    "Young Green Dragon": [("Rend", 3)],
    "Tyrannosaurus Rex": [("Bite", 1), ("Tail", 1)],
    "Fire Giant": [("Flame Sword", 2)],
    "Bone Devil": [("Claw", 2), ("Infernal Sting", 1)],
    "Young Blue Dragon": [("Rend", 3)],
    "Young Red Dragon": [("Rend", 3)],
    "Stone Golem": [("Slam", 2)],
    "Aboleth": [("Tentacle", 2)],
    "Remorhaz": [("Bite", 1)],
    "Roc": [("Beak", 2)],
    "Horned Devil": [("Searing Fork", 3)],
    "Archmage": [("Arcane Burst", 4)],
    "Erinyes": [("Withering Sword", 3)],
}

ABBR = {"strength": "str", "dexterity": "dex", "constitution": "con",
        "intelligence": "int", "wisdom": "wis", "charisma": "cha"}
_DMG = re.compile(r"(\d+) \((\d+)d(\d+)(?: ?([+-]) ?(\d+))?\) (\w+) damage", re.I)
_SAVE = re.compile(r"(\w+) Saving Throw: DC (\d+)", re.I)


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def load(cache: Path) -> list:
    if not cache.exists():
        with urllib.request.urlopen(URL, timeout=120) as r:  # noqa: S310 (fixed https URL)
            cache.write_bytes(r.read())
    return json.loads(cache.read_text())["results"]


def parse_damage(desc: str):
    """[(avg, count, sides, bonus, type), ...] from the SRD's printed damage text.

    Only unconditional damage counts: a clause like "plus 2 (1d4) Slashing damage if the
    attack roll had Advantage" is left out of the fixed number."""
    out = []
    for m in _DMG.finditer(desc):
        avg, n, d, sign, b, typ = m.groups()
        tail = desc[m.end():].split(".")[0]
        if out and re.match(r"\s*(if|when|while|against)\b", tail, re.I):
            continue
        bonus = int(b or 0) * (-1 if sign == "-" else 1)
        out.append((int(avg), int(n), int(d), bonus, typ.lower()))
    return out


def morale_of(c) -> str:
    t = c["type"]["key"]
    intel = c["ability_scores"]["intelligence"]
    if t in ("construct", "ooze") or (t == "undead" and intel <= 6) or (t == "plant" and intel <= 3):
        return "never"
    return "normal"


def entry(c, multi) -> dict:
    acts = {a["name"]: a for a in c["actions"]}
    attacks = []
    for name, count in multi:
        a = acts[name]
        dm = parse_damage(a["desc"])
        if not dm:
            raise ValueError(f"{c['name']}: no damage in {name!r}: {a['desc']}")
        to_hit = a["attacks"][0]["to_hit_mod"] if a.get("attacks") else None
        main = dm[0]
        attacks.append({
            "name": name, "count": count, "to_hit": to_hit,
            "fixed": sum(x[0] for x in dm),
            "dice": f"{main[1]}d{main[2]}", "mod": main[3], "dtype": main[4],
            "extra_dice": [f"{x[1]}d{x[2]}" for x in dm[1:]],
            "ranged": "Ranged Attack" in a["desc"] and "Melee" not in a["desc"],
        })
    special = None
    for a in c["actions"]:
        lim = a.get("usage_limits") or {}
        if lim.get("type") == "RECHARGE_ON_ROLL":
            sv, dm = _SAVE.search(a["desc"]), parse_damage(a["desc"])
            if sv and dm:
                big = any(s in a["desc"] for s in ("60-foot", "90-foot", "40-foot", "20-foot-radius"))
                tiny = "5-foot-radius" in a["desc"]
                special = {"name": a["name"], "save": ABBR[sv.group(1).lower()],
                           "dc": int(sv.group(2)), "fixed": sum(x[0] for x in dm),
                           "dice": f"{dm[0][1]}d{dm[0][2]}", "dtype": dm[0][4],
                           "half_on_success": "Half damage" in a["desc"],
                           "targets": 1 if tiny else (3 if big else 2),
                           "recharge_min": int(lim["param"])}
    multi_text = next((a["desc"] for a in c["actions"] if a["name"] == "Multiattack"), None)
    ri = c.get("resistances_and_immunities") or {}
    resist = sorted({d["key"] for d in (ri.get("damage_resistances") or [])}
                    | {d["key"] for d in (ri.get("damage_immunities") or [])})
    return {
        "id": slug(c["name"]), "name": c["name"],
        "cr": float(c.get("challenge_rating_decimal") or c.get("challenge_rating") or 0),
        "type": c["type"]["key"], "ac": int(c["armor_class"]), "hp": int(c["hit_points"]),
        "saves": {ABBR[k]: int(v) for k, v in (c.get("saving_throws_all")
                                                or c.get("saving_throws") or {}).items()
                  if k in ABBR},
        "attacks": attacks, "special": special, "resist": resist,
        "morale": morale_of(c),
        "traits": [t["name"] for t in c.get("traits") or [] if t["name"] == "Undead Fortitude"],
        "multiattack_text": multi_text,
        "source": "SRD 5.2 (Open5e srd-2024)",
    }


def build(cache: Path) -> dict:
    by_name = {c["name"]: c for c in load(cache)}
    missing = [n for n in LADDER if n not in by_name]
    if missing:
        raise SystemExit(f"not in the SRD data: {missing}")
    mons = [entry(by_name[n], m) for n, m in LADDER.items()]
    mons.sort(key=lambda m: (m["cr"], m["name"]))
    return {"source": "SRD 5.2.1 (CC BY 4.0) via Open5e v2 srd-2024; generated by "
                      "software/tools/build_srd_monsters.py — do not edit by hand",
            "monsters": mons}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cache", type=Path, default=Path("/tmp/facets_d20_srd2024_creatures.json"))
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    data = build(a.cache)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("# Generated — do not edit. See software/tools/build_srd_monsters.py\n"
                     "# Includes material from the System Reference Document 5.2.1 by Wizards of\n"
                     "# the Coast LLC, licensed CC BY 4.0.\n"
                     + yaml.safe_dump(data, sort_keys=False, width=100), encoding="utf-8")
    print(f"wrote {len(data['monsters'])} monsters to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
