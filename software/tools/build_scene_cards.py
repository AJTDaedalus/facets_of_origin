"""Generate the stat lines on an adventure's scene cards and its pregen blocks.

    python -m tools.build_scene_cards           # fill the blocks
    python -m tools.build_scene_cards --check   # exit 1 if anything would change

The same discipline as `build_bestiary`, applied to modules: a scene card and
the card file it is about cannot disagree, because one is generated from the
other. Only the content between `<!-- statline: id -->` and `<!-- /statline -->`
(and between `<!-- pregen: slug -->` and `<!-- /pregen -->`) is generated; the
card's prose is hand-written and untouched.

Enemy resolution order, so a module can reskin without forking numbers: the
module's own `enemies/` first, then the setting-agnostic Bestiary. A reskin
must keep its original's numbers (INV-18).

Pregens come from `<module>/characters/<slug>.fof` (Lean Facets v1.0, DESIGN
§3.3), read through `Character.from_fof`, so HP and slots are computed.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from app.game.character import Character
from app.game.enemy import Enemy
from tools.build_bestiary import DAGGER, ROLE_LABEL, signed

REPO_ROOT = Path(__file__).resolve().parents[2]
ADVENTURES = REPO_ROOT / "adventures"
BESTIARY_ENEMIES = REPO_ROOT / "enemies"
FACETS_DIR = REPO_ROOT / "software" / "facets"

STATLINE = re.compile(
    r"(<!-- statline: ([a-z0-9_]+) -->\n).*?(<!-- /statline -->)", re.S)
PREGEN = re.compile(
    r"(<!-- pregen: ([a-z0-9_]+) -->\n).*?(<!-- /pregen -->)", re.S)

_COUNT_WORD = {2: "two", 3: "three", 4: "four"}


def load_ruleset():
    """Core plus every setting Facet on disk (modules may use setting content)."""
    from app.facets.loader import discover_facet_files, load_facet_file
    from app.facets.registry import MergedRuleset
    return MergedRuleset([load_facet_file(p) for p in discover_facet_files(FACETS_DIR)])


def load_enemies(module_dir: Path) -> dict[str, Enemy]:
    """Every enemy a module's cards may reference, module-local first."""
    out: dict[str, Enemy] = {}
    for source in (BESTIARY_ENEMIES, module_dir / "enemies"):
        if not source.is_dir():
            continue
        for path in sorted(source.glob("*.fof")):
            enemy = Enemy.from_fof(yaml.safe_load(path.read_text(encoding="utf-8")))
            out[enemy.id] = enemy
    return out


def _clean(text) -> str:
    return " ".join(str(text or "").split())


def render_statline(enemy: Enemy, ruleset=None) -> str:
    """One enemy's entry on a scene card: the numbers on one line, then the
    card lines the MM runs it from (WANTS, SPECIAL, WHEN BLOODIED, TELLS,
    BREAKS, NASTIER). Twists stay in the Bestiary."""
    ruleset = ruleset or load_ruleset()
    card = enemy.card(ruleset)
    over = set(card["overrides"])
    mark = lambda f: DAGGER if f in over else ""                     # noqa: E731
    parts = [f"**{enemy.name}** · *level {enemy.level} {ROLE_LABEL[enemy.role]}*"]
    if card["hp"] is None:
        parts.append("drops to any hit")
    else:
        parts.append(f"HP **{card['hp']}**{mark('hp')}")
    parts.append(f"attack {signed(card['attack'])}{mark('attack')}")
    damage = f"damage {card['damage']}{mark('damage')}"
    if card["mob"]:
        damage += (f" (+{card['mob_damage_per_extra']} per extra in the mob, "
                   f"max +{card['mob_damage_cap']})")
    parts.append(damage)
    if card["attacks"] > 1:
        parts.append(f"{_COUNT_WORD.get(card['attacks'], card['attacks'])} attacks{mark('attacks')}")
    parts.append(f"armor {enemy.armor}")
    parts.append(f"morale {enemy.morale}" + (" (fearless)" if card["fearless"] else ""))
    lines = [" · ".join(parts), ""]
    for label, value in (("Wants", enemy.wants), ("Special", enemy.special),
                         ("When bloodied", enemy.when_bloodied), ("Tells", enemy.tells),
                         ("Breaks", enemy.breaks), ("Nastier", enemy.nastier)):
        if _clean(value):
            lines += [f"**{label}:** {_clean(value)}", ""]
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Pregenerated characters
# ---------------------------------------------------------------------------

def _talent_label(ruleset, state) -> str:
    tdef = ruleset.get_talent(state.id)
    name = tdef.name if tdef else state.id.replace("_", " ").title()
    if state.id == "weapon_master" and state.choice:
        name += f" ({state.choice})"
    if state.improved:
        name += " (improved)"
    return name


def _item_label(ruleset, ch: Character, item) -> str:
    if item.weapon:
        die = ruleset.equipment.weapon_categories[item.weapon].die
        if ch.equipped.get("weapon") == item.id:
            die = ch.weapon_die(ruleset)
        return f"{item.name} (d{die})"
    if item.armor:
        cat = ruleset.equipment.armor.get(item.armor)
        return f"{item.name} (armor {cat.armor})" if cat else item.name
    if item.usage_die:
        return f"{item.name} (d{item.usage_die})"
    return item.name


def render_pregen(fof: dict, ruleset=None) -> str:
    """One pregenerated character's printed block, from their `.fof`."""
    ruleset = ruleset or load_ruleset()
    ch = Character.from_fof(fof, ruleset)
    raw = fof.get("character") or {}
    lin = ruleset.get_lineage(ch.lineage)
    lin_name = lin.name if lin else ch.lineage.title()
    if ch.gifted:
        knack = lin.gift_knack if lin else f"{lin_name} gift"
        gift = f"**Lineage:** {lin_name} — **gifted** (gift knack *{knack}*"
        if ch.gift_domain:
            dom = ruleset.get_domain(ch.gift_domain)
            gift += f"; Minor workings in {dom.name if dom else ch.gift_domain}"
        lineage_line = gift + ")"
    elif lin is not None and lin.gifted:
        lineage_line = f"**Lineage:** {lin_name} — ungifted"
    else:
        lineage_line = f"**Lineage:** {lin_name}"

    lines = [
        lineage_line,
        "",
        f"**Facet:** {ch.facet.title()} · **Level {ch.level}** · **HP {ch.hp_max(ruleset)}** · "
        f"**Slots {ch.slots_total(ruleset)}** · **Sparks {ch.sparks}**",
        "",
    ]
    concept = f" — *{_clean(ch.concept)}*" if ch.concept else ""
    lines += [f"**Class:** {ch.class_name}" + (" *(custom)*" if ch.custom_class else "")
              + concept, ""]
    lines += ["**Stats:** " + " · ".join(
        f"{s.name} {signed(ch.stats.get(s.id, 0))}" for s in ruleset.stats), ""]
    if ch.knacks:
        lines += ["**Knacks:** " + " · ".join(ch.knacks), ""]
    if ch.talents:
        lines += ["**Talents:** " + " · ".join(_talent_label(ruleset, t) for t in ch.talents), ""]
    if ch.signature:
        sdef = ruleset.get_talent(ch.signature)
        lines += [f"**Signature:** {sdef.name if sdef else ch.signature}", ""]
    if ch.magic:
        tdef = ruleset.magic.traditions.get(ch.magic.tradition)
        doms = ", ".join((ruleset.get_domain(d).name if ruleset.get_domain(d) else d)
                         for d in ch.magic.domains)
        stat = tdef.stat.title() if tdef else ""
        lines += [f"**Magic:** {ch.magic.tradition.title()} ({stat}) — {doms}", ""]
        if ch.magic.signature_workings:
            lines += ["**Signature workings:** " + "; ".join(
                f"*{_clean(w)}*" for w in ch.magic.signature_workings), ""]
    if ch.specialty:
        lines += [f"**Specialty:** {_clean(ch.specialty)}", ""]
    gear = [_item_label(ruleset, ch, i) for i in ch.inventory if not i.curio]
    curios = [i.name.split(": ", 1)[-1].lower() for i in ch.inventory if i.curio]
    carrying = " · ".join(gear)
    if curios:
        carrying += (" · " if carrying else "") + "*curios:* " + ", ".join(curios)
    if carrying:
        lines += [f"**Carrying:** {carrying}", ""]
    if raw.get("suggested_agenda"):
        lines += [f"**Suggested agenda:** {_clean(raw['suggested_agenda'])}", ""]
    return "\n".join(lines).rstrip() + "\n"


def _pregens(module_dir: Path) -> dict[str, dict]:
    out = {}
    directory = module_dir / "characters"
    if directory.is_dir():
        for path in sorted(directory.glob("*.fof")):
            out[path.stem] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return out


def fill_text(text: str, enemies: dict[str, Enemy], pregens: dict[str, dict],
              ruleset) -> tuple[str, list[str]]:
    """Fill every marker in one file. Returns (new text, unknown ids)."""
    missing: list[str] = []

    def _fill(match: re.Match) -> str:
        open_tag, enemy_id, close_tag = match.groups()
        enemy = enemies.get(enemy_id)
        if enemy is None:
            missing.append(enemy_id)
            return match.group(0)
        return open_tag + render_statline(enemy, ruleset) + close_tag

    def _fill_pregen(match: re.Match) -> str:
        open_tag, slug, close_tag = match.groups()
        fof = pregens.get(slug)
        if fof is None:
            missing.append(slug)
            return match.group(0)
        return open_tag + render_pregen(fof, ruleset) + close_tag

    return PREGEN.sub(_fill_pregen, STATLINE.sub(_fill, text)), missing


def build(write: bool, adventures: Path = ADVENTURES) -> list[str]:
    """Fill every marker in every adventure. Returns changed paths.

    Raises:
        SystemExit: a marker names an unknown enemy or pregen.
    """
    changed: list[str] = []
    if not adventures.is_dir():
        return changed
    ruleset = load_ruleset()
    for module_dir in sorted(p for p in adventures.iterdir() if p.is_dir()):
        enemies = load_enemies(module_dir)
        pregens = _pregens(module_dir)
        for path in sorted(module_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if "<!-- statline:" not in text and "<!-- pregen:" not in text:
                continue
            new_text, missing = fill_text(text, enemies, pregens, ruleset)
            if missing:
                raise SystemExit(f"{path.name} references unknown enemies or pregens: "
                                 f"{', '.join(sorted(set(missing)))}")
            if new_text != text:
                try:
                    changed.append(str(path.relative_to(REPO_ROOT)))
                except ValueError:
                    changed.append(str(path))
                if write:
                    path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if any card would change")
    args = ap.parse_args()
    changed = build(write=not args.check)
    if args.check and changed:
        print("Scene cards are stale:\n  " + "\n  ".join(changed))
        sys.exit(1)
    print(f"Scene cards: {len(changed)} file(s) {'would change' if args.check else 'rebuilt'}")


if __name__ == "__main__":
    main()
