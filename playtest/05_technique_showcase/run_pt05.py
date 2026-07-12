"""PT05 — Technique Showcase: advancement-reachability harness (WS-B / B6).

Drives the *real* engine (`Character.advance_skill` for pacing and
`Character.select_technique` for the pick/prerequisite rules) to answer B6's
question: under the v0.3 pacing (facet_level_threshold 5, major 3), can a
single character actually reach a Tier 3 Technique, a Prismatic domain, and
Second Domain — and at which session does each land, versus DESIGN §6.3?

Progression under test — a Soul Facet character taking the Communion chain:
  Facet level 1 -> spiritual_domain (T1, magic-granting; standard first domain)
  Facet level 2 -> the_language_beneath_language (T2)
  Facet level 3 -> second_domain (T3), choosing a Prismatic Soul domain

Second Domain is itself a Tier 3 Technique, and the Prismatic domain is the
second domain it grants — which is exactly the Tier-3 gate the appendix
requires ("Prismatic domains require a Tier 3 Technique; never a starting
domain"). One character therefore demonstrates all three B6 targets.

Run from the `software/` directory:  python ../playtest/05_technique_showcase/run_pt05.py
"""
import math
import os
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[2] / "software"
sys.path.insert(0, str(SOFTWARE))
os.environ.setdefault("DATA_DIR", str(SOFTWARE / "tests" / "_test_data"))
os.environ.setdefault("SECRET_KEY", "pt05-harness-key")

from app.facets.registry import build_ruleset          # noqa: E402
from app.game.character import create_default_character  # noqa: E402

RULESET = build_ruleset([])
ADV = RULESET.advancement
SOUL_SKILLS = [s.id for s in RULESET.skills if s.facet == "soul" and s.status == "active"]

# The Communion chain and the domains chosen along it.
CHAIN = [
    ("spiritual_domain", "resonance"),          # T1 — first (standard) domain
    ("the_language_beneath_language", None),    # T2
    ("second_domain", "fate"),                  # T3 — second (Prismatic) domain
]
ATTRS = {"strength": 1, "dexterity": 2, "constitution": 1, "intelligence": 2,
         "wisdom": 2, "knowledge": 2, "spirit": 3, "luck": 2, "charisma": 3}


def project_session_for_level(level: int, efficiency: float) -> int:
    """DESIGN §6.3 projection: session at which `level` primary Facet levels land."""
    marks = level * ADV.facet_level_threshold * ADV.marks_per_rank
    return math.ceil(marks / (efficiency * ADV.session_skill_points))


def run(efficiency: float) -> dict:
    """Simulate one character at `efficiency` primary-SP, taking the next
    Communion Technique the moment a Facet level grants a pick."""
    char, errors = create_default_character(
        name="Communicant", player_name="PT05", primary_facet="soul",
        attributes=ATTRS, ruleset=RULESET,
    )
    assert not errors, errors

    marks_budget = 0.0
    picks_taken = 0
    log = []          # (event, session)
    level_seen = 0

    for session in range(1, 61):
        # Bank this session's primary-Facet marks (fractional efficiency accrues).
        marks_budget += efficiency * ADV.session_skill_points
        while marks_budget >= 1:
            sid = next((s for s in SOUL_SKILLS
                        if char.skills.get(s) is None or char.skills[s].rank != "master"), None)
            if sid is None:
                marks_budget = 0
                break
            char.advance_skill(sid, 1, RULESET)
            marks_budget -= 1

        # Take the next Technique in the chain whenever a pick is available.
        while char.technique_picks_available > 0 and picks_taken < len(CHAIN):
            tid, choice = CHAIN[picks_taken]
            ok, msg = char.select_technique(tid, RULESET, choice)
            assert ok, f"select {tid} failed at session {session}: {msg}"
            log.append((f"Facet level {char.total_facet_levels}: {tid}"
                        + (f" ({choice})" if choice else ""), session))
            picks_taken += 1

        if char.facet_level > level_seen:
            level_seen = char.facet_level

        if picks_taken == len(CHAIN) and char.facet_level >= 3:
            return {"char": char, "log": log, "final_session": session}

    raise RuntimeError("did not reach Facet level 3 within 60 sessions")


def main():
    print(f"Constants: facet_level_threshold={ADV.facet_level_threshold}, "
          f"major_advancement_threshold={ADV.major_advancement_threshold}, "
          f"session_skill_points={ADV.session_skill_points}, marks_per_rank={ADV.marks_per_rank}\n")

    for efficiency, label in [(1.0, "100% (dedicated)"), (0.8, "80% (realistic)")]:
        result = run(efficiency)
        char = result["char"]
        print(f"=== {label} — primary-SP efficiency {efficiency:g} ===")
        for level in (1, 2, 3):
            proj = project_session_for_level(level, efficiency)
            landed = next((s for e, s in result["log"] if e.startswith(f"Facet level {level}:")), None)
            print(f"  Facet level {level}: unlock at session {landed}   (DESIGN §6.3 projection s{proj})")
        for event, session in result["log"]:
            print(f"    - session {session}: {event}")
        print(f"  Final: techniques={char.techniques}")
        print(f"         magic_domain={char.magic_domain!r}, "
              f"second-domain choice={char.technique_choices.get('second_domain')!r}, "
              f"total_facet_levels={char.total_facet_levels}, "
              f"first Major fired at level {ADV.major_advancement_threshold}\n")


if __name__ == "__main__":
    main()
