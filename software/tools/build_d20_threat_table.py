"""Render Table 9–2 (Threat per SRD monster) into facets_d20/Appendix_Monster_Threat.md.

Drives ``facets_d20.analysis`` only: every number comes from ``threat_appendix()``,
which prices each monster in ``software/facets_d20/data/srd_monsters.yaml`` from its own
stat block with the Threat model the simulator wrote into ``facets_d20.yaml``. This file
formats; it carries no rule.

The appendix marks the generated region:

    <!-- threat-table -->
    ...
    <!-- /threat-table -->

Usage:
    cd software
    python -m tools.build_d20_threat_table           # write the appendix
    python -m tools.build_d20_threat_table --check   # exit 1 if anything would change
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))

from facets_d20 import analysis as A  # noqa: E402

REPO = SOFTWARE.parent
APPENDIX = REPO / "facets_d20" / "Appendix_Monster_Threat.md"
START, END = "<!-- threat-table -->", "<!-- /threat-table -->"
MARKER = re.compile(re.escape(START) + r"\n(.*?)" + re.escape(END), re.S)

ATTRIBUTION = (
    '*This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") '
    "by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 "
    "is licensed under the Creative Commons Attribution 4.0 International License, available "
    "at https://creativecommons.org/licenses/by/4.0/legalcode.*")

SKELETON = f"""# Appendix: Monster Threat

Table 9–2 prices every SRD 5.2.1 monster the simulator knows, from its own stat block, for
the encounter budgets in 09_Mirror_Masters_Guide.md. Look a monster up, write down the
number for the role you're using it in, and add.

{START}
{END}

{ATTRIBUTION}
"""


def _cr(cr) -> str:
    return str(cr)


def _notes(r: dict) -> str:
    bits = []
    if r["hits_hard"]:
        bits.append("hits hard")
    if r["never"]:
        bits.append("never breaks")
    return ", ".join(bits)


def render_region(raw=None) -> str:
    """The generated block between the markers (ends with a newline)."""
    rows = A.threat_appendix(raw)
    model = A.threat_model_from_data(raw)
    lone = A.lone_boss_factor(raw)
    lo, hi = A.STANDARD_COUNT
    blo, bhi = A.BOSS_SHARE
    out = [
        "*Generated — do not edit. Source: `software/facets_d20/data/srd_monsters.yaml`, "
        "priced by `software/facets_d20/analysis.py`; regenerate with "
        "`python -m tools.build_d20_threat_table` from `software/`.*",
        "",
        "**Table 9–2: Threat by Monster**",
        "",
        "| Monster | CR | Standard | Minion | Boss | Standard at levels | Boss at levels | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        out.append(f"| {r['name']} | {_cr(r['cr'])} | {r['standard']} | {r['minion']} | "
                   f"{r['boss']} | {A.level_range(r['standard_levels'])} | "
                   f"{A.level_range(r['boss_levels'])} | {_notes(r)} |")
    pct = lambda x: f"{round(100 * x)}%"  # noqa: E731
    out += [
        "",
        f"**How the numbers are made.** *Standard* is √(hit points × damage per turn), "
        f"damage per turn being everything the block does on an ordinary turn if it all "
        f"hits (a Recharge ability left out). *Minion* is √({model.minion_hp:g} × damage per "
        f"turn). *Boss* is the standard figure × {model.boss:.2f}, which already pays for the "
        f"boss's doubled hit points and its extra turn. A monster that never breaks is already "
        f"counted × {model.never:.2f} in its standard and minion figures, and one that hits "
        f"hard × {model.hard:.2f} in all three. A lone boss counts × {lone:g}; one whose company "
        f"is worth less than a fifth of it, × {A.SMALL_COMPANY[1]:g}.",
        "",
        f"**Standard at levels** is where {lo} to {hi} of the monster make a Clash for four "
        f"characters; **Boss at levels** is where the boss figure is {pct(blo)} to {pct(bhi)} "
        f"of that Clash for four characters, leaving the rest for its followers. Both columns "
        f"assume four characters: with three, look one level higher. A dash means it doesn't "
        f"fit levels 1–10 in that role.",
        "",
        f"**Hits hard** marks a monster whose damage per turn is at least "
        f"{pct(A.HARD_HITTER_FACTOR - 1)} above the usual for its CR (Table 9–3's *Damage* "
        f"column). The mark-up is already in its numbers; don't adjust the fight for it.",
        "",
    ]
    return "\n".join(out)


def fill(text: str, region: str) -> str:
    """Replace what sits between the markers with ``region``."""
    if not MARKER.search(text):
        raise ValueError(f"no {START} … {END} region")
    return MARKER.sub(lambda m: f"{START}\n{region}{END}", text, count=1)


def build(check: bool = False, path: Path = APPENDIX) -> list:
    """Write (or, with ``check``, only compare) the appendix. Returns the stale paths."""
    old = path.read_text(encoding="utf-8") if path.exists() else SKELETON
    new = fill(old, render_region())
    if new == (path.read_text(encoding="utf-8") if path.exists() else None):
        return []
    if not check:
        path.write_text(new, encoding="utf-8")
    return [str(path)]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    check = "--check" in argv
    stale = build(check=check)
    if check and stale:
        print("stale:", *stale)
        return 1
    print("wrote" if stale else "up to date:", APPENDIX.relative_to(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
