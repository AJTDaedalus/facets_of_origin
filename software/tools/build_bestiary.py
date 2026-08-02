"""Fill the Bestiary's stat blocks and finding aids from the enemy .fof files.

The Bestiary's prose is hand-written; its numbers are not. Each chapter marks
where a stat block goes:

    <!-- statblock: chalk_hound -->
    <!-- /statblock -->

and this tool replaces everything between the markers with a block generated
from `enemies/chalk_hound.fof`. The book and the tool therefore cannot disagree
about a creature's Resolve, and `monster_books.md` §9's format-drift
anti-pattern is structurally impossible rather than merely discouraged.

Field order follows the 2007 stat-block principle (`monster_books.md` §3):
group by the moment the MM needs it, not by data category —

    identity + Threat Rating   (the moment the encounter starts)
    Resolve + armor            (when the players act on it)
    attack + special + phases  (when it acts)
    disposition + triggers     (how it acts)
    morale + negotiation       (when it stops)
    organization               (prep)

`Finding_Aids.md` is generated whole: every creature by Threat Rating, then by
tier. The TR-sorted list comes first because it is the one an MM actually uses
(`monster_books.md` §1 — the 2007 lesson was to move it to the front).

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

# Chapters in reading order. The finding aids link into these.
CHAPTERS = [
    "B1_Beasts_and_Vermin.md",
    "B2_Folk.md",
    "B3_The_Made.md",
    "B4_What_Remains.md",
]

TIER_LABEL = {"mook": "Mook", "named": "Named", "boss": "Boss"}
ARMOR_LABEL = {"none": "none", "light": "light (+1 Resolve)", "heavy": "heavy (+2 Resolve)"}
TIER_ORDER = ["mook", "named", "boss"]

BLOCK = re.compile(
    r"(<!-- statblock: ([a-z_]+) -->\n).*?(<!-- /statblock -->)", re.S)


def load_enemies() -> dict[str, Enemy]:
    """Every shipped enemy, keyed by id."""
    out = {}
    for path in sorted(ENEMY_DIR.glob("*.fof")):
        enemy = Enemy.from_fof(yaml.safe_load(path.read_text()))
        out[enemy.id] = enemy
    return out


def _signed(value: int) -> str:
    """A modifier with an explicit sign and a true minus (style guide Law 5)."""
    return f"+{value}" if value >= 0 else f"−{abs(value)}"


def render_block(enemy: Enemy) -> str:
    """One creature's stat block, in table-moment order."""
    lines = [
        f"**{enemy.name}** · *{TIER_LABEL[enemy.tier]}* · **TR {enemy.calculate_tr()}**",
        "",
    ]
    resolve = "—" if enemy.tier == "mook" else str(enemy.resolve)
    incoming = "Tier 1" if enemy.tier == "mook" else "Tier 2"
    lines += [
        f"**When they act on it:** Resolve {resolve} · armor "
        f"{ARMOR_LABEL.get(enemy.armor, enemy.armor)} · defense "
        f"{_signed(enemy.defense_modifier)}",
        "",
        f"**When it acts:** attack {_signed(enemy.attack_modifier)} · incoming {incoming}",
        "",
    ]
    # A creature may carry several named special moves; each gets its own
    # labelled paragraph so the block stays greppable by eye
    # (`monster_books.md` §7 — boldface run-in labels let the eye grep it).
    if enemy.special:
        for part in enemy.special.split("\n"):
            part = " ".join(part.split())
            if part:
                lines += [f"**Special:** {part}", ""]
    for phase in enemy.phases:
        lines += [f"**At Resolve {phase.resolve_threshold}:** "
                  f"{' '.join(phase.description.split())}", ""]
    if enemy.disposition:
        lines += [f"**Disposition:** {' '.join(enemy.disposition.split())}", ""]
    if enemy.first_target:
        lines += [f"**Goes for:** {' '.join(enemy.first_target.split())}", ""]
    if enemy.triggers:
        lines.append("**In play:**")
        lines.append("")
        for trigger in enemy.triggers:
            lines.append(f"- {' '.join(trigger.split())}")
        lines.append("")
    if enemy.morale:
        lines += [f"**Morale:** {' '.join(enemy.morale.split())}", ""]
    if enemy.negotiation:
        lines += [f"**Negotiation:** {' '.join(enemy.negotiation.split())}", ""]
    if enemy.organization:
        lines += [f"**Appears:** {' '.join(enemy.organization.split())}", ""]
    lines.append(f"*`enemies/{enemy.id}.fof`*")
    lines.append("")
    return "\n".join(lines)


def fill_chapter(text: str, enemies: dict[str, Enemy], source: str) -> str:
    """Replace every marked region in one chapter with its generated block."""
    def replace(match: re.Match) -> str:
        opener, enemy_id, closer = match.group(1), match.group(2), match.group(3)
        enemy = enemies.get(enemy_id)
        if enemy is None:
            raise KeyError(
                f"{source} references `{enemy_id}`, which has no "
                f"enemies/{enemy_id}.fof")
        return f"{opener}\n{render_block(enemy)}\n{closer}"

    return BLOCK.sub(replace, text)


def referenced_ids() -> dict[str, str]:
    """{enemy id: chapter filename} for every block marker in the book."""
    out = {}
    for name in CHAPTERS:
        path = BESTIARY_DIR / name
        if not path.exists():
            continue
        for match in BLOCK.finditer(path.read_text()):
            out[match.group(2)] = name
    return out


def generate_finding_aids_text() -> str:
    enemies = load_enemies()
    where = referenced_ids()
    listed = [e for e in enemies.values() if e.id in where]
    by_tr = sorted(listed, key=lambda e: (e.calculate_tr(), e.name))
    by_tier = sorted(listed, key=lambda e: (TIER_ORDER.index(e.tier), e.calculate_tr(),
                                            e.name))

    lines = [
        "# Finding Aids",
        "",
        "*Generated by `software/tools/build_bestiary.py` from `enemies/*.fof` — do not"
        " edit by hand. Regenerating this file should produce no diff (INV-15).*",
        "",
        "Threat Rating first, because that is the list you actually use. Tier second,"
        " for the nights you know what shape of problem you want and not how hard.",
        "",
        "Party Strength 3 bands, from Table MM1–7: **3–7 Mooks** is a Skirmish;"
        " **3 Named + 1 Mook** is Standard; each further Mook moves it one band.",
        "",
        "---",
        "",
        "## By Threat Rating",
        "",
        "**Table B0–1: Creatures by Threat Rating**",
        "",
        "| TR | Creature | Tier | Chapter |",
        "|---|---|---|---|",
    ]
    for enemy in by_tr:
        lines.append(f"| **{enemy.calculate_tr()}** | [{enemy.name}]({where[enemy.id]}) "
                     f"| {TIER_LABEL[enemy.tier]} | {where[enemy.id]} |")
    lines += ["", "---", "", "## By Tier", "",
              "**Table B0–2: Creatures by Tier**", "",
              "| Tier | Creature | TR | Chapter |", "|---|---|---|---|"]
    for enemy in by_tier:
        lines.append(f"| {TIER_LABEL[enemy.tier]} | [{enemy.name}]({where[enemy.id]}) "
                     f"| {enemy.calculate_tr()} | {where[enemy.id]} |")

    no_fight = [e for e in listed if e.negotiation]
    lines += ["", "---", "", "## Creatures With a Way Out", "",
              "Every creature below states a negotiation surface — what it wants, what"
              " shifts it, and what deal it will honour. Reach for these when the table"
              " wants a scene rather than a fight.", "",
              "**Table B0–3: Negotiable Creatures**", "",
              "| Creature | TR | What it wants |", "|---|---|---|"]
    for enemy in sorted(no_fight, key=lambda e: e.calculate_tr()):
        want = " ".join(enemy.negotiation.split())
        want = want.split(".")[0] + "."
        lines.append(f"| [{enemy.name}]({where[enemy.id]}) | {enemy.calculate_tr()} "
                     f"| {want} |")
    lines.append("")
    return "\n".join(lines)


def build(write: bool) -> list[str]:
    """Fill blocks and finding aids. Returns the names of files that changed."""
    enemies = load_enemies()
    changed = []
    for name in CHAPTERS:
        path = BESTIARY_DIR / name
        if not path.exists():
            continue
        current = path.read_text()
        filled = fill_chapter(current, enemies, name)
        if filled != current:
            changed.append(name)
            if write:
                path.write_text(filled)
    aids = generate_finding_aids_text()
    if (FINDING_AIDS.read_text() if FINDING_AIDS.exists() else "") != aids:
        changed.append(FINDING_AIDS.name)
        if write:
            FINDING_AIDS.write_text(aids)
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
    total = len(referenced_ids())
    print(f"Bestiary rebuilt: {total} stat blocks, "
          f"{len(changed)} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
