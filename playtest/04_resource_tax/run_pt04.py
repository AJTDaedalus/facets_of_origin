"""PT04 -- Resource Tax driver: The Ashwood Trail (WD8, D6 acceptance test).

Drives the real engine via `tools.combat_sim.run_combat` for every fight --
this script supplies only the Ashwood Trail's three-encounter roster and the
between-encounter recovery/Nomination steps scripted in scenario.md. No rule
computation is re-implemented here; see C1 in CLAUDE.md.

**What "the new Spark cadence" means for this harness.** Act Break
Nomination and the player-initiated Graceful Fail (D6, WD4/WD5) are social,
table-driven events -- there is no dice roll to simulate. This driver models
their effect the same way scenario.md scripts them: one Spark awarded to a
rotating PC after each of the two Nomination Rounds (after Encounter 1 and
after Encounter 2), exactly as "Nomination Round 1" / "Nomination Round 2"
in scenario.md call for. This is a scripted assumption standing in for a
table event, not a simulated roll.

**Spark refund variant (D6, WD7).** `spark.variants.refund_on_failed_pretechnique_cast`
is read and reported per run. It has **no observable effect** in this
harness: combat magic/pretechnique casting is not simulated in
`tools.combat_sim` (a pre-existing scope gap, noted in PT03's results as F7).
The flag is measured as "no change" for that reason, not because the variant
failed to do anything -- there is nothing in the sim for it to act on yet.

Usage (from software/):
    python ../playtest/04_resource_tax/run_pt04.py --table   # single verbose run
    python ../playtest/04_resource_tax/run_pt04.py --rate    # N seeded runs
"""
from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[2] / "software"
sys.path.insert(0, str(SOFTWARE))

from tools.combat_sim import (            # noqa: E402
    PCState, EnemyState, SimResult,
    make_enemy, make_pc,
    mordai_def, zahna_def, zulnut_def,
    run_combat,
    _ruleset,
    spark_refund_variant_enabled,
)
from app.game import combat as combat_module  # noqa: E402


def pt04_party() -> list[dict]:
    """The standard 3-PC party (Mordai / Zahna / Zulnut)."""
    return [mordai_def(), zahna_def(), zulnut_def()]


# ---------------------------------------------------------------------------
# Ashwood Trail roster (scenario.md)
# ---------------------------------------------------------------------------

def bandit_scout_def() -> dict:
    """Bandit Scout: Mook, TR 1, atk +0."""
    return dict(name="Bandit Scout", instance_id="scout", tier="mook",
                resolve=0, attack_modifier=0, defense_modifier=0, armor="none")


def bandit_lieutenant_def() -> dict:
    """Bandit Lieutenant: Named, TR 8 (Recipe Table core), Resolve 3, atk +2,
    def +2, light armor -- offense(+2->4) + durability(3) + armor(light->1) = 8."""
    return dict(name="Bandit Lieutenant", instance_id="lieutenant", tier="named",
                resolve=3, attack_modifier=2, defense_modifier=2, armor="light")


def bandit_archer_def() -> dict:
    """Bandit Archer: Mook, TR 1, atk +0 (ranged is narrative flavor only)."""
    return dict(name="Bandit Archer", instance_id="archer", tier="mook",
                resolve=0, attack_modifier=0, defense_modifier=0, armor="none")


def elite_bandit_def() -> dict:
    """Elite Bandit: Mook, TR 1, atk +0."""
    return dict(name="Elite Bandit", instance_id="elite", tier="mook",
                resolve=0, attack_modifier=0, defense_modifier=0, armor="none")


def bandit_captain_def() -> dict:
    """Bandit Captain: Named, TR 8 -- identical stat block to Bandit
    Lieutenant (Recipe Table's 3-Named-at-TR-8 core, WD9); her distinction is
    narrative (commands, offers terms), not a hidden TR bonus. scenario.md no
    longer gives her a Rally Technique -- it would have pushed her off the
    calibrated TR-8 row this roster is built from."""
    return dict(name="Bandit Captain", instance_id="captain", tier="named",
                resolve=3, attack_modifier=2, defense_modifier=2, armor="light")


ENCOUNTERS = [
    ("Encounter 1 -- Skirmish: The Scout Party",
     [(bandit_scout_def(), 3)]),
    ("Encounter 2 -- Standard: The Bridge Ambush",
     [(bandit_lieutenant_def(), 3), (bandit_archer_def(), 1)]),
    ("Encounter 3 -- Hard: The Bandit Captain",
     [(bandit_captain_def(), 1), (bandit_lieutenant_def(), 2), (elite_bandit_def(), 2)]),
]

NOMINATION_ROUNDS_AFTER = {0, 1}  # after Encounter 1 and after Encounter 2 (0-indexed)


def run_session(verbose: bool = False) -> dict:
    """Run all three Ashwood Trail encounters back-to-back, carrying PC
    Endurance, Conditions, and Sparks across the session (scenario.md's
    Recovery Between Encounters rules)."""
    ruleset = _ruleset()
    pcs = [make_pc(d) for d in pt04_party()]
    per_encounter: list[SimResult] = []

    for i, (label, enemy_defs) in enumerate(ENCOUNTERS):
        enemies = []
        for edef, count in enemy_defs:
            for j in range(count):
                enemies.append(make_enemy(edef, j + 1 if count > 1 else 0))

        if verbose:
            print(f"\n=== {label} ===")
            for pc in pcs:
                print(f"  {pc.name}: End={pc.endurance_current}/{pc.endurance_max} "
                      f"Sparks={pc.sparks} (spent so far: {pc.sparks_spent})")

        result = run_combat(pcs, enemies, verbose=verbose)
        per_encounter.append(result)

        if not result.party_wins:
            break

        # Recovery Between Encounters (scenario.md): Withdrawn-equivalent
        # recovery of 2 Endurance for surviving PCs; Tier 1 already clears
        # end-of-exchange; Tier 2 persists unless treated (not modelled here
        # -- no PC enters this harness already Staggered/Cornered).
        for pc in pcs:
            if not pc.is_broken:
                pc.endurance_current = min(
                    pc.endurance_max,
                    pc.endurance_current + combat_module.withdrawn_recovery_amount(ruleset),
                )

        # Nomination Round (D6, new Spark cadence): one Spark to a rotating
        # PC, modelling the table's Act Break Nomination between encounters.
        if i in NOMINATION_ROUNDS_AFTER:
            nominee = pcs[i % len(pcs)]
            nominee.sparks += 1
            if verbose:
                print(f"  [Nomination Round {i + 1}] {nominee.name} earns a Spark "
                      f"(now {nominee.sparks}).")

    session_won = all(r.party_wins for r in per_encounter) and len(per_encounter) == len(ENCOUNTERS)
    return {
        "pcs": pcs,
        "per_encounter": per_encounter,
        "session_won": session_won,
    }


def run_rate(iterations: int = 200, seeds: list[int] | None = None,
             force_variant: bool = False) -> dict:
    """Run the full session under N seeds; report Sparks spent per player.

    `force_variant` flips `spark.variants.refund_on_failed_pretechnique_cast`
    to True on the cached ruleset for this run only (WD8: "run with ... the
    refund variant enabled for measurement"), without touching facet.yaml's
    committed default (still off -- D6, "test, do not adopt").
    """
    import random

    ruleset = _ruleset()
    original_flag = ruleset.spark.variants.refund_on_failed_pretechnique_cast
    if force_variant:
        ruleset.spark.variants.refund_on_failed_pretechnique_cast = True

    seeds = seeds or [1, 2, 3, 7, 13, 42, 99]
    sparks_per_player: list[float] = []
    pcs_broken_counts: list[int] = []
    session_wins = 0
    total_runs = 0
    variant_enabled = spark_refund_variant_enabled(ruleset)

    for seed in seeds:
        random.seed(seed)
        for _ in range(iterations):
            result = run_session()
            total_runs += 1
            if result["session_won"]:
                session_wins += 1
            pcs = result["pcs"]
            sparks_per_player.append(sum(p.sparks_spent for p in pcs) / len(pcs))
            pcs_broken_counts.append(sum(1 for p in pcs if p.is_broken))

    ruleset.spark.variants.refund_on_failed_pretechnique_cast = original_flag

    return {
        "iterations": total_runs,
        "session_win_rate": session_wins / total_runs,
        "mean_sparks_spent_per_player": statistics.mean(sparks_per_player),
        "median_sparks_spent_per_player": statistics.median(sparks_per_player),
        "min_sparks_spent_per_player": min(sparks_per_player),
        "mean_pcs_broken": statistics.mean(pcs_broken_counts),
        "spark_refund_variant_enabled": variant_enabled,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", action="store_true", help="single verbose run")
    parser.add_argument("--rate", action="store_true", help="N seeded runs, aggregate stats")
    parser.add_argument("--iterations", type=int, default=200)
    args = parser.parse_args()

    if args.table:
        result = run_session(verbose=True)
        print("\n=== Session Summary ===")
        for pc in result["pcs"]:
            print(f"  {pc.name}: End={pc.endurance_current}/{pc.endurance_max} "
                  f"Sparks remaining={pc.sparks} Sparks spent={pc.sparks_spent}")
        print(f"  Session won: {result['session_won']}")

    if args.rate or not args.table:
        for label, force_variant in [("Variant OFF (facet.yaml default)", False),
                                      ("Variant ON (measurement only)", True)]:
            agg = run_rate(iterations=args.iterations, force_variant=force_variant)
            print(f"\n=== PT04 Aggregate -- {label} ===")
            print(f"  Iterations: {agg['iterations']}")
            print(f"  Session win rate: {agg['session_win_rate']:.1%}")
            print(f"  Mean Sparks spent/player: {agg['mean_sparks_spent_per_player']:.2f}")
            print(f"  Median Sparks spent/player: {agg['median_sparks_spent_per_player']:.2f}")
            print(f"  Min Sparks spent/player (worst run): {agg['min_sparks_spent_per_player']:.2f}")
            print(f"  Mean PCs Broken: {agg['mean_pcs_broken']:.2f}")
            print(f"  Spark refund variant enabled: {agg['spark_refund_variant_enabled']}")
            print(f"  D6 Accept (Sparks spent/player >= 2): "
                  f"{'PASS' if agg['mean_sparks_spent_per_player'] >= 2 else 'FAIL'}")


if __name__ == "__main__":
    main()
