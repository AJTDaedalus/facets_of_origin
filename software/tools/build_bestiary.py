"""Fill the Bestiary's stat blocks and finding aids from the enemy cards.

The Bestiary's prose is hand-written; its numbers are not. Each chapter marks
where a stat block goes:

    <!-- statblock: chalk_hound -->
    <!-- /statblock -->

and this tool replaces everything between the markers with a block generated
from `enemies/chalk_hound.fof` (a v1.0 monster card, DESIGN §3.4). HP, damage,
attack and attacks are derived from the card's level and role through
`facet.yaml`'s monster level table, so the book and the data cannot disagree.
A number the card overrides is marked with a dagger (†).

Block order follows the moment the MM needs each line: identity; the numbers;
WANTS; SPECIAL; WHEN BLOODIED; TELLS; BREAKS; TWISTS (d6); NASTIER.

`Finding_Aids.md` is generated whole: every creature sorted by level, then role.

Usage:
    cd software
    python -m tools.build_bestiary           # fill blocks + write finding aids
    python -m tools.build_bestiary --check   # exit 1 if anything would change
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from app.game.enemy import Enemy

REPO_ROOT = Path(__file__).resolve().parents[2]
ENEMY_DIR = REPO_ROOT / "enemies"
BESTIARY_DIR = REPO_ROOT / "bestiary"
FINDING_AIDS = BESTIARY_DIR / "Finding_Aids.md"
FACETS_DIR = REPO_ROOT / "software" / "facets"

# Chapters in reading order. The finding aids link into these.
CHAPTERS = [
    "B1_Beasts_and_Vermin.md",
    "B2_Folk.md",
    "B3_The_Made.md",
    "B4_What_Remains.md",
]

ROLE_ORDER = ["mook", "standard", "elite", "boss"]
ROLE_LABEL = {"mook": "Mook", "standard": "Standard", "elite": "Elite", "boss": "Boss"}
DAGGER = "†"

BLOCK = re.compile(
    r"(<!-- statblock: ([a-z0-9_]+) -->\n).*?(<!-- /statblock -->)", re.S)


def load_ruleset():
    """The core ruleset, loaded straight from disk (no settings/env needed)."""
    from app.facets.loader import load_facet_file
    from app.facets.registry import MergedRuleset
    return MergedRuleset([load_facet_file(FACETS_DIR / "base" / "facet.yaml")])


def load_enemies(enemy_dir: Path = ENEMY_DIR) -> dict[str, Enemy]:
    """Every enemy card in a directory, keyed by id."""
    out = {}
    for path in sorted(enemy_dir.glob("*.fof")):
        enemy = Enemy.from_fof(yaml.safe_load(path.read_text(encoding="utf-8")))
        out[enemy.id] = enemy
    return out


def signed(value: int) -> str:
    """A modifier with an explicit sign and a true minus (style guide Law 5)."""
    return f"+{value}" if value >= 0 else f"−{abs(value)}"


# Kept for callers written against the old name.
_signed = signed


def _clean(text) -> str:
    return " ".join(str(text or "").split())


def numbers_line(enemy: Enemy, ruleset) -> str:
    """HP · armor · attack · damage · attacks · morale, with † on overrides."""
    card = enemy.card(ruleset)
    over = set(card["overrides"])
    mark = lambda f: DAGGER if f in over else ""                     # noqa: E731
    if card["hp"] is None:
        hp = "— (drops to any hit)"
    else:
        hp = f"{card['hp']}{mark('hp')}"
    parts = [
        f"**HP** {hp}",
        f"**Armor** {enemy.armor}",
        f"**Attack** {signed(card['attack'])}{mark('attack')}",
        f"**Damage** {card['damage']}{mark('damage')}",
        f"**Attacks** {card['attacks']}{mark('attacks')}",
        f"**Morale** {enemy.morale}" + (" (fearless)" if card["fearless"] else ""),
    ]
    return " · ".join(parts)


def role_notes(enemy: Enemy, ruleset) -> list[str]:
    card = enemy.card(ruleset)
    notes = []
    if card["mob"]:
        notes.append(f"Attacks as a mob: +{card['mob_damage_per_extra']} damage per extra "
                     f"Mook (max +{card['mob_damage_cap']}).")
    if card["bloodied_phase"]:
        notes.append("Changes phase when Bloodied (half HP).")
    if card["overrides"]:
        notes.append(f"{DAGGER} The card overrides the level table.")
    return notes


def render_block(enemy: Enemy, ruleset=None) -> str:
    """One creature's stat block, in table-moment order."""
    ruleset = ruleset or load_ruleset()
    lines = [
        f"**{enemy.name}** · *Level {enemy.level} {ROLE_LABEL[enemy.role]}*"
        + (f" · {_clean(enemy.weapon)}" if enemy.weapon else ""),
        "",
        numbers_line(enemy, ruleset),
        "",
    ]
    for note in role_notes(enemy, ruleset):
        lines += [f"*{note}*", ""]
    for label, value in (("Wants", enemy.wants), ("Special", enemy.special),
                         ("When bloodied", enemy.when_bloodied), ("Tells", enemy.tells),
                         ("Breaks", enemy.breaks)):
        if _clean(value):
            lines += [f"**{label}:** {_clean(value)}", ""]
    if enemy.twists:
        lines += ["**Twists (d6):**", ""]
        lines += [f"{i}. {_clean(t)}" for i, t in enumerate(enemy.twists, start=1)]
        lines.append("")
    if _clean(enemy.nastier):
        lines += [f"**Nastier:** {_clean(enemy.nastier)}", ""]
    lines.append(f"*`enemies/{enemy.id}.fof`*")
    lines.append("")
    return "\n".join(lines)


def fill_chapter(text: str, enemies: dict[str, Enemy], source: str, ruleset=None) -> str:
    """Replace every marked region in one chapter with its generated block.

    Raises:
        KeyError: a marker names an enemy with no card.
    """
    ruleset = ruleset or load_ruleset()

    def replace(match: re.Match) -> str:
        opener, enemy_id, closer = match.group(1), match.group(2), match.group(3)
        enemy = enemies.get(enemy_id)
        if enemy is None:
            raise KeyError(f"{source} references `{enemy_id}`, which has no "
                           f"enemies/{enemy_id}.fof")
        return f"{opener}\n{render_block(enemy, ruleset)}\n{closer}"

    return BLOCK.sub(replace, text)


def referenced_ids(bestiary_dir: Path = BESTIARY_DIR) -> dict[str, str]:
    """{enemy id: chapter filename} for every block marker in the book."""
    out = {}
    for name in CHAPTERS:
        path = bestiary_dir / name
        if not path.exists():
            continue
        for match in BLOCK.finditer(path.read_text(encoding="utf-8")):
            out[match.group(2)] = name
    return out


def sort_key(enemy: Enemy):
    return (enemy.level, ROLE_ORDER.index(enemy.role), enemy.name)


def generate_finding_aids_text(enemies: dict[str, Enemy] | None = None,
                               where: dict[str, str] | None = None, ruleset=None) -> str:
    """Finding_Aids.md: every creature in the book, by level then role."""
    enemies = enemies if enemies is not None else load_enemies()
    where = where if where is not None else referenced_ids()
    ruleset = ruleset or load_ruleset()
    listed = sorted((e for e in enemies.values() if e.id in where), key=sort_key)

    lines = [
        "# Finding Aids",
        "",
        "*Generated by `software/tools/build_bestiary.py` from `enemies/*.fof` — do not"
        " edit by hand. Regenerating this file should produce no diff (INV-15).*",
        "",
        "Every creature in the Bestiary, by level and then by role: the list you reach"
        " for when you know how tough the fight should be. HP is blank for a Mook,"
        " which drops to any hit.",
        "",
        "---",
        "",
        "## By Level",
        "",
        "**Table B0–1: Creatures by Level**",
        "",
        "| Level | Creature | Role | HP | Attack | Damage | Morale | Chapter |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for e in listed:
        card = e.card(ruleset)
        hp = "—" if card["hp"] is None else str(card["hp"])
        lines.append(
            f"| {e.level} | [{e.name}]({where[e.id]}) | {ROLE_LABEL[e.role]} | {hp} "
            f"| {signed(card['attack'])} | {card['damage']} | {e.morale} | {where[e.id]} |")
    lines += ["", "---", "", "## By Role", "",
              "**Table B0–2: Creatures by Role**", "",
              "| Role | Creature | Level | Chapter |", "|---|---|---|---|"]
    for e in sorted(listed, key=lambda x: (ROLE_ORDER.index(x.role), x.level, x.name)):
        lines.append(f"| {ROLE_LABEL[e.role]} | [{e.name}]({where[e.id]}) | {e.level} "
                     f"| {where[e.id]} |")
    lines += ["", "---", "", "## By Morale", "",
              "Morale is what the MM rolls over to break a foe (2d6, over the number"
              " breaks it). Low morale ends fights early; morale 12 never breaks.", "",
              "**Table B0–3: Creatures by Morale**", "",
              "| Morale | Creature | Level | Role | Breaks |", "|---|---|---|---|---|"]
    for e in sorted(listed, key=lambda x: (x.morale, x.level, x.name)):
        label = f"{e.morale} (fearless)" if e.card(ruleset)["fearless"] else str(e.morale)
        lines.append(f"| {label} | [{e.name}]({where[e.id]}) | {e.level} "
                     f"| {ROLE_LABEL[e.role]} | {_clean(e.breaks).split('. ')[0].rstrip('.')}. |")
    lines.append("")
    return "\n".join(lines)


def build(write: bool, bestiary_dir: Path = BESTIARY_DIR, enemy_dir: Path = ENEMY_DIR) -> list[str]:
    """Fill blocks and finding aids. Returns the names of files that changed."""
    ruleset = load_ruleset()
    enemies = load_enemies(enemy_dir)
    changed = []
    for name in CHAPTERS:
        path = bestiary_dir / name
        if not path.exists():
            continue
        current = path.read_text(encoding="utf-8")
        filled = fill_chapter(current, enemies, name, ruleset)
        if filled != current:
            changed.append(name)
            if write:
                path.write_text(filled, encoding="utf-8")
    aids_path = bestiary_dir / FINDING_AIDS.name
    aids = generate_finding_aids_text(enemies, referenced_ids(bestiary_dir), ruleset)
    if (aids_path.read_text(encoding="utf-8") if aids_path.exists() else "") != aids:
        changed.append(aids_path.name)
        if write:
            aids_path.write_text(aids, encoding="utf-8")
    return changed


def main(argv: list[str]) -> int:
    check = "--check" in argv
    changed = build(write=not check)
    if check:
        if changed:
            print(f"Bestiary is stale ({', '.join(changed)}) — run "
                  f"`python -m tools.build_bestiary`.")
            return 1
        print("Bestiary is up to date.")
        return 0
    print(f"Bestiary rebuilt: {len(referenced_ids())} stat blocks, "
          f"{len(changed)} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
