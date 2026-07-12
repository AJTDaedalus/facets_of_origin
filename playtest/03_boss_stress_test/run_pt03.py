"""PT03 — Boss Stress Test driver: The Iron Crucible.

A13 human-acceptance run. Every rule computation routes through
`app.game.combat` (the same module the WebSocket server uses) — this
driver only supplies the Iron Crucible's *authored* stat-block behaviour
(Forge Slam = two attacks/exchange; Heat Surge Con check; the Resolve-keyed
phase change), never a re-implementation of a rule. See C1 in CLAUDE.md.

The Iron Crucible's scenario (playtest/03_boss_stress_test/scenario.md) was
authored before the D1 Resolve rewrite. This driver runs the D1-translated
enemy; the translation gaps are logged as findings in results.md.

Usage (from software/):
    python -m playtest.03_boss_stress_test.run_pt03 --table   # single verbose run
    python -m playtest.03_boss_stress_test.run_pt03 --rate    # N seeded runs
"""
from __future__ import annotations

import argparse
import random
import statistics
import sys

# Reuse the calibrated sim building blocks — all of which drive app.game.combat.
from tools.combat_sim import (
    PCState, EnemyState, SimResult,
    make_enemy, make_pc,
    mordai_def, zahna_def, zulnut_def,
    _pc_strike, _enemy_attack,
    choose_pc_posture, choose_enemy_posture, choose_pc_target,
    _ruleset,
)
from app.game import combat as combat_module

MAX_EXCHANGES = 20


# ---------------------------------------------------------------------------
# Sheet-reconciled PCs (A13: "modifier columns reconciled against sheets")
# ---------------------------------------------------------------------------

def pt03_party() -> list[dict]:
    """Standard party, reconciled to characters/*.fof.

    Mordai and Zahna match tools.combat_sim exactly. Zulnut is corrected:
    the stock zulnut_def() strikes at +0 (strength+combat), but by the sheet
    Zulnut has no Combat skill and strikes with Finesse — Dexterity(+1) +
    Finesse Practiced(+1) = +2 — under the Phase-0 "Strike accepts any
    attribute/skill" audit rule. Modelled here as combat_mod=2 so
    strength+combat = the sheet's +2 finesse Strike; his Dodge stays Dex +1.
    This divergence from the stock def is logged as a sim finding in results.md.
    """
    m = mordai_def()
    za = zahna_def()
    zu = zulnut_def()
    zu["combat_mod"] = 2   # Finesse Practiced stands in for the Strike skill column
    zu["strength_mod"] = 0  # Dexterity +1 is carried in dexterity_mod for Dodge
    # NB: strength+combat = 0+2 = +2 = the sheet's 2d6+2 Finesse Strike.
    return [m, za, zu]


# ---------------------------------------------------------------------------
# The Iron Crucible — D1-translated boss
# ---------------------------------------------------------------------------

def iron_crucible_def() -> dict:
    """The Iron Crucible, translated from scenario.md into the D1 Resolve model.

    scenario.md (pre-D1):  Endurance 10, Heavy armor (T3->T2), Attack +2,
      Aggressive, Forge Slam (two targets), phase "on first Tier 2 condition".

    D1 translation (findings F1-F4 in results.md):
      - Resolve 10; Heavy armor => +2 flat Resolve at init => effective 12.
      - Attack +2, Aggressive posture (reactions Hard; offense effectively +3).
      - Phase re-keyed to a Resolve threshold (scenario's "first Tier 2
        condition" has no D1 analogue — enemies have no condition track).
        Set at 6 (half of effective 12) for the intended MID-fight pivot.
      - special_attack_mod +3 on phase (scenario: +2 -> +3).
    """
    return dict(
        name="The Iron Crucible",
        instance_id="crucible",
        tier="boss",
        resolve=10,
        attack_modifier=2,
        defense_modifier=1,
        armor="heavy",
        posture="aggressive",
        phases=[{"resolve_threshold": 6, "description": "Cracked Shell"}],
        special_attack_mod=3,     # phase: attack +2 -> +3
        special_ignores_tier1=False,
    )


def _con_mod(pc_name: str) -> int:
    """Constitution modifier from the sheets, for Heat Surge Con checks."""
    return {"Mordai": 1, "Zahna": -1, "Zulnut": -1}[pc_name]


# ---------------------------------------------------------------------------
# Combat loop with the Crucible's authored actions
# ---------------------------------------------------------------------------

def run_crucible_fight(pcs: list[PCState], crucible: EnemyState, verbose: bool = False) -> SimResult:
    ruleset = _ruleset()
    for pc in pcs:
        pc.armor_downgrades_remaining = combat_module.armor_budget(pc.armor, ruleset)

    heat_surge_active = False

    for exchange in range(1, MAX_EXCHANGES + 1):
        active_pcs = [p for p in pcs if not p.is_broken]
        if crucible.is_out:
            return _result(True, exchange - 1, pcs, crucible)
        if not active_pcs:
            return _result(False, exchange - 1, pcs, crucible)

        for pc in active_pcs:
            pc.reactions_this_exchange = 0

        if verbose:
            print(f"\n--- Exchange {exchange} ---")
            for p in active_pcs:
                print(f"  {p.name}: End={p.endurance_current}/{p.endurance_max} "
                      f"Sparks={p.sparks} Cond={p.conditions}")
            phase = "Cracked Shell" if crucible.phase_index is not None else "Intact"
            print(f"  Crucible: Resolve={crucible.resolve_current}/{crucible.resolve+2} "
                  f"[{phase}] posture={crucible.posture} atk=+{crucible.attack_modifier} "
                  f"Cond={crucible.conditions}")

        # 1. Postures
        for pc in active_pcs:
            pc.posture = choose_pc_posture(pc, len(active_pcs))
        # Crucible posture is authored: Aggressive until phase, then Measured.
        crucible.posture = "measured" if crucible.phase_index is not None else "aggressive"

        if verbose:
            print(f"  Postures — PCs: {{{', '.join(f'{p.name}:{p.posture}' for p in active_pcs)}}}, "
                  f"Crucible:{crucible.posture}")

        # 2. PC actions (focus fire the Crucible)
        for pc in active_pcs:
            if pc.posture == "withdrawn":
                if verbose:
                    print(f"  {pc.name} withdraws (recovering)")
                continue
            if crucible.is_out:
                break
            _pc_strike(pc, crucible, ruleset, verbose)

        was_phased = crucible.phase_index is not None
        if crucible.is_out:
            return _result(True, exchange, pcs, crucible)
        # Detect the phase transition this exchange (for Heat Surge onset).
        if crucible.phase_index is not None and not heat_surge_active:
            heat_surge_active = True
            if verbose:
                print("  *** PHASE CHANGE: the Crucible's shell cracks — Heat Surge online ***")

        # 3. Crucible action — Forge Slam hits the TWO lowest-Endurance PCs.
        targets = sorted(
            [p for p in pcs if not p.is_broken],
            key=lambda p: p.endurance_current,
        )[:2]
        for tgt in targets:
            if crucible.is_out:
                break
            _enemy_attack(crucible, tgt, ruleset, verbose)

        # 3b. Heat Surge (post-phase): one random living PC, Con check or Winded.
        if heat_surge_active:
            living = [p for p in pcs if not p.is_broken]
            if living:
                victim = random.choice(living)
                chk = combat_module.roll(_con_mod(victim.name), "Standard", ruleset)
                if verbose:
                    print(f"  Heat Surge -> {victim.name} Con check: {chk.total} -> {chk.outcome}")
                if chk.outcome == "failure":
                    res = combat_module.apply_condition(victim.conditions, "winded", 1, ruleset)
                    if res.broken:
                        victim.is_broken = True
                    if verbose:
                        print(f"    -> {victim.name} takes Winded (Heat Surge)")

        active_pcs = [p for p in pcs if not p.is_broken]
        if not active_pcs:
            return _result(False, exchange, pcs, crucible)

        # 4. End of exchange
        for pc in pcs:
            if pc.is_broken:
                continue
            combat_module.end_exchange(pc.conditions, ruleset)
            if pc.posture == "withdrawn":
                pc.endurance_current = min(
                    pc.endurance_max,
                    pc.endurance_current + combat_module.withdrawn_recovery_amount(ruleset),
                )
        if not crucible.is_out:
            combat_module.end_exchange(crucible.conditions, ruleset)

    return _result(False, MAX_EXCHANGES, pcs, crucible)


def _result(win: bool, exchanges: int, pcs: list[PCState], crucible: EnemyState) -> SimResult:
    return SimResult(
        party_wins=win,
        exchanges=exchanges,
        sparks_spent=sum(p.sparks_spent for p in pcs),
        pcs_broken=[p.name for p in pcs if p.is_broken],
        endurance_remaining={p.name: p.endurance_current for p in pcs},
        enemies_remaining=0 if crucible.is_out else 1,
    )


def _build() -> tuple[list[PCState], EnemyState]:
    pcs = [make_pc(d) for d in pt03_party()]
    crucible = make_enemy(iron_crucible_def())
    return pcs, crucible


def run_table(seed: int) -> None:
    random.seed(seed)
    pcs, crucible = _build()
    print(f"=== PT03 TABLE RUN (seed={seed}) ===")
    print(f"Crucible: Resolve {crucible.resolve_current}/{crucible.resolve}+2 armor, "
          f"attack +{crucible.attack_modifier} Aggressive, Forge Slam (2 targets), "
          f"phase at Resolve <= 6")
    result = run_crucible_fight(pcs, crucible, verbose=True)
    print(f"\n=== RESULT: {'PARTY WINS' if result.party_wins else 'PARTY LOSES'} in "
          f"{result.exchanges} exchanges ===")
    print(f"Sparks spent: {result.sparks_spent} | Broken: {result.pcs_broken}")
    print(f"Endurance remaining: {result.endurance_remaining}")


def run_rate(n: int, seed: int) -> None:
    random.seed(seed)
    results = []
    phased_count = 0            # fights in which the Resolve phase change fired
    end_endurance = []          # per-PC Endurance at fight end, across all fights
    for _ in range(n):
        pcs, crucible = _build()
        results.append(run_crucible_fight(pcs, crucible, verbose=False))
        # phase_index is set once the Resolve threshold is crossed and never unset,
        # so inspecting the mutated crucible after the fight reports whether it fired.
        if crucible.phase_index is not None:
            phased_count += 1
        end_endurance.extend(p.endurance_current for p in pcs)
    wins = sum(1 for r in results if r.party_wins)
    exch = [r.exchanges for r in results]
    broken = [len(r.pcs_broken) for r in results]
    sparks = [r.sparks_spent for r in results]
    print(f"=== PT03 RATE (n={n}, seed={seed}) ===")
    print(f"Win rate: {wins/n:.1%} ({wins}/{n})")
    print(f"Exchanges: mean {statistics.mean(exch):.1f}, median {statistics.median(exch):.0f}, "
          f"min {min(exch)}, max {max(exch)}")
    print(f"Phase fired: {phased_count/n:.1%} ({phased_count}/{n})")
    print(f"PCs Broken/fight: mean {statistics.mean(broken):.2f}")
    print(f"Sparks spent/fight: mean {statistics.mean(sparks):.1f} (of 9 party total)")
    print(f"PC Endurance remaining at fight end: mean {statistics.mean(end_endurance):.1f}")
    # Broken frequency per PC
    from collections import Counter
    c = Counter(name for r in results for name in r.pcs_broken)
    print(f"Broken incidence by PC: {dict(c)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--rate", action="store_true")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=13)
    args = ap.parse_args()
    if args.table:
        run_table(args.seed)
    elif args.rate:
        run_rate(args.n, args.seed)
    else:
        ap.print_help()
