"""Generate the stat lines on an adventure's scene cards from its enemy files.

    python -m tools.build_scene_cards           # fill the blocks
    python -m tools.build_scene_cards --check   # exit 1 if anything would change

The same discipline as `build_bestiary`, applied to modules: a scene card and
the `.fof` it is about cannot disagree, because one of them is generated from
the other. An MM reading a card mid-session is reading numbers that were
simulated, not numbers somebody retyped.

A card's *prose* — trigger read-aloud, objective, clock, tactics, terrain,
outs, Sparks, development — is hand-written and untouched. Only the content
between `<!-- statline: id -->` and `<!-- /statline -->` is generated.

Enemy resolution order, so a module can reskin without forking numbers:
the module's own `enemies/` first, then the setting-agnostic Bestiary. A
reskin is required by INV-18 to differ from its Bestiary original in flavour
fields only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from app.game.enemy import Enemy
from tools.build_bestiary import _signed, ARMOR_LABEL, TIER_LABEL

REPO_ROOT = Path(__file__).resolve().parents[2]
ADVENTURES = REPO_ROOT / "adventures"
BESTIARY_ENEMIES = REPO_ROOT / "enemies"

STATLINE = re.compile(
    r"(<!-- statline: ([a-z_]+) -->\n).*?(<!-- /statline -->)", re.S)


def load_enemies(module_dir: Path) -> dict[str, Enemy]:
    """Every enemy a module's cards may reference, module-local first."""
    out: dict[str, Enemy] = {}
    for source in (BESTIARY_ENEMIES, module_dir / "enemies"):
        if not source.is_dir():
            continue
        for path in sorted(source.glob("*.fof")):
            enemy = Enemy.from_fof(yaml.safe_load(path.read_text()))
            out[enemy.id] = enemy
    return out


def render_statline(enemy: Enemy) -> str:
    """One enemy's line on a scene card.

    Denser than the Bestiary's block on purpose. A card is read standing up,
    mid-scene, with players waiting: tier, Resolve, attack, armor, stance
    triggers, Techniques, TR — in that order, every time, so the MM's eye
    lands in the same place on every card.
    """
    resolve = "—" if enemy.tier == "mook" else str(enemy.resolve)
    parts = [
        f"**{enemy.name}** · *{TIER_LABEL[enemy.tier]}* · "
        f"Resolve **{resolve}** · attack {_signed(enemy.attack_modifier)} · "
        f"armor {ARMOR_LABEL.get(enemy.armor, enemy.armor)} · "
        f"incoming {'Tier 1' if enemy.tier == 'mook' else 'Tier 2'} · "
        f"**TR {enemy.calculate_tr()}**",
        "",
    ]
    if enemy.techniques:
        parts += ["**Techniques:** " + ", ".join(
            t.replace("_", " ") for t in enemy.techniques), ""]
    if enemy.special:
        for chunk in enemy.special.split("\n"):
            chunk = " ".join(chunk.split())
            if chunk:
                parts += [f"**Special:** {chunk}", ""]
    for phase in enemy.phases:
        parts += [f"**Phase:** {' '.join(phase.description.split())}", ""]
    if enemy.triggers:
        parts.append("**Stance triggers:**")
        parts.append("")
        for trigger in enemy.triggers:
            parts.append(f"- {' '.join(trigger.split())}")
        parts.append("")
    if enemy.first_target:
        parts += [f"**Opens on:** {' '.join(enemy.first_target.split())}", ""]
    if enemy.morale:
        parts += [f"**Morale:** {' '.join(enemy.morale.split())}", ""]
    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Pregenerated characters
# ---------------------------------------------------------------------------

PREGEN = re.compile(
    r"(<!-- pregen: ([a-z_]+) -->\n).*?(<!-- /pregen -->)", re.S)

_RANK_MOD = {"novice": 0, "practiced": 1, "expert": 2, "master": 3}


def _mod(rating: int) -> str:
    return {1: "−1", 2: "+0", 3: "+1"}[rating]


def render_pregen(block: dict, ruleset) -> str:
    """One pregenerated character's block, from their `.fof`.

    A pregen used to exist twice — as a paragraph in the module and as numbers
    somebody typed under it — and the two could disagree without anything
    noticing. Now there is one source, the `.fof`, and this is its printed form.
    """
    attrs = block["attributes"]
    skills = block.get("skills") or {}
    con = _RANK_MOD.get("", 0)
    endurance = (4 + {1: -1, 2: 0, 3: 1}[attrs["constitution"]]
                 + _RANK_MOD[(skills.get("endurance") or {}).get("rank", "novice")])

    order = ["strength", "dexterity", "constitution", "intelligence", "wisdom",
             "knowledge", "spirit", "luck", "charisma"]
    short = {"strength": "Str", "dexterity": "Dex", "constitution": "Con",
             "intelligence": "Int", "wisdom": "Wis", "knowledge": "Kno",
             "spirit": "Spi", "luck": "Luc", "charisma": "Cha"}
    attr_line = ", ".join(
        f"{short[a]} {attrs[a]} ({_mod(attrs[a])})" for a in order)

    skill_bits = []
    for sid, state in sorted(skills.items()):
        rank = state.get("rank", "novice")
        marks = state.get("marks", 0)
        label = sid.replace("_", " ").title()
        if rank != "novice":
            skill_bits.append(f"{label} ({rank.title()}, +{_RANK_MOD[rank]})")
        elif marks:
            skill_bits.append(f"{label} (Novice, {marks} mark)")

    lines = [
        f"**Lineage:** {block.get('lineage', 'human').title()}"
        + (" — **gifted**" if block.get("gifted") else " — ungifted"),
        "",
        f"**Primary Facet:** {block['primary_facet'].title()} · "
        f"**Endurance Pool {endurance}** · **Sparks {block.get('sparks', 3)}**",
        "",
        f"**Attributes:** {attr_line}",
        "",
    ]
    if skill_bits:
        lines += [f"**Skills:** {', '.join(skill_bits)}", ""]
    if block.get("magic_domain"):
        domain = None
        if ruleset is not None and ruleset.magic:
            domain = ruleset.magic.get_domain(block["magic_domain"])
        name = domain.name if domain else block["magic_domain"]
        lines += [
            f"**Gift:** {name} — a domain, at **Minor scope** until it formalizes "
            "at your first Facet level, which costs no Technique pick "
            "(Chapter II.5).",
            "",
        ]
    if block.get("specialty"):
        lines += [f"**Specialty:** {' '.join(block['specialty'].split())}", ""]
    if block.get("inventory"):
        lines += ["**Carrying:** " + ", ".join(
            i.replace("_", " ") for i in block["inventory"]), ""]
    if block.get("technique_at_facet_level_1"):
        lines += [
            "**At Facet level 1 you would likely take:** "
            f"*{block['technique_at_facet_level_1'].replace('_', ' ').title()}*",
            "",
        ]
    if block.get("suggested_agenda"):
        lines += [f"**Suggested agenda:** {block['suggested_agenda']}", ""]
    return "\n".join(lines).rstrip() + "\n"


def _pregen_blocks(module_dir: Path) -> dict[str, dict]:
    out = {}
    directory = module_dir / "characters"
    if directory.is_dir():
        for path in sorted(directory.glob("*.fof")):
            out[path.stem] = yaml.safe_load(path.read_text())["character"]
    return out


def build(write: bool) -> list[str]:
    """Fill every statline marker in every adventure. Returns changed paths."""
    changed: list[str] = []
    try:
        from app.facets.loader import load_facet_file
        from app.facets.registry import MergedRuleset
        facets = REPO_ROOT / "software" / "facets"
        ruleset = MergedRuleset([load_facet_file(facets / "base" / "facet.yaml"),
                                 load_facet_file(facets / "valloh" / "facet.yaml")])
    except Exception:                                    # pragma: no cover
        ruleset = None

    for module_dir in sorted(p for p in ADVENTURES.iterdir() if p.is_dir()):
        enemies = load_enemies(module_dir)
        pregens = _pregen_blocks(module_dir)
        for path in sorted(module_dir.glob("*.md")):
            text = path.read_text()
            if "<!-- statline:" not in text and "<!-- pregen:" not in text:
                continue

            missing: list[str] = []

            def _fill(match: re.Match) -> str:
                open_tag, enemy_id, close_tag = match.groups()
                enemy = enemies.get(enemy_id)
                if enemy is None:
                    missing.append(enemy_id)
                    return match.group(0)
                return open_tag + render_statline(enemy) + close_tag

            def _fill_pregen(match: re.Match) -> str:
                open_tag, slug, close_tag = match.groups()
                block = pregens.get(slug)
                if block is None:
                    missing.append(slug)
                    return match.group(0)
                return open_tag + render_pregen(block, ruleset) + close_tag

            new_text = PREGEN.sub(_fill_pregen, STATLINE.sub(_fill, text))
            if missing:
                raise SystemExit(
                    f"{path.relative_to(REPO_ROOT)} references unknown "
                    f"enemies or pregens: {', '.join(sorted(set(missing)))}"
                )
            if new_text != text:
                changed.append(str(path.relative_to(REPO_ROOT)))
                if write:
                    path.write_text(new_text)
    return changed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any card would change")
    args = ap.parse_args()
    changed = build(write=not args.check)
    if args.check and changed:
        print("Scene cards are stale:\n  " + "\n  ".join(changed))
        sys.exit(1)
    print(f"Scene cards: {len(changed)} file(s) "
          f"{'would change' if args.check else 'rebuilt'}")


if __name__ == "__main__":
    main()
