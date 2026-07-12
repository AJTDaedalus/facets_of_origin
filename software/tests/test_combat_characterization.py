"""Characterization tests for combat resolution.

Per DESIGN §3 (WS-A0): these pin the *simulator's* current semantics, not the
pre-extraction engine's — every figure in `research/simulation_log.md` was
produced under simulator semantics. This file is the G0 gate baseline.

The targeted semantics tests below (armor_downgrade, apply_condition,
end_exchange, reaction cost by posture) now import from `app.game.combat`
per A0.2's accept criterion — that module is the moved, ruleset-driven home
for these rules (see combat.py's module docstring for confirmation that its
dice RNG draws are bit-identical to the simulator's, seed for seed).

The 5 fixed-seed full end-to-end scenarios still import `run_combat` and
friends from `tools.combat_sim` — that orchestration loop (AI policy +
statistics) is *not* part of combat.py's API (DESIGN §2.1) and stays in the
simulator through A0.3. Reproducing these exact end-states after A0.3
rewires `run_combat` to call `combat.py` internally is the G0 gate itself.

Do not "fix" a divergence found here — if a change alters one of these
values, that change introduced a behaviour change and must be corrected,
not the test.
"""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.facets.registry import build_ruleset
from app.game import combat as combat_module

from tools.combat_sim import (
    archive_guardian_def,
    city_watch_sergeant_def,
    harbor_thug_def,
    make_enemy,
    make_pc,
    mordai_def,
    run_combat,
    standard_party,
)


@pytest.fixture(scope="module")
def ruleset():
    return build_ruleset([])


# ---------------------------------------------------------------------------
# Targeted semantics — armor_downgrade
#
# SUPERSEDED (D2, task A5): the gated shape pinned below — light only ever
# touches Tier 2, heavy only ever touches Tier 3, with no limit on how many
# times it fires — was itself the bug DESIGN §4.2 identifies: against a
# single boss landing one Tier 2 per exchange, an unlimited downgrade never
# runs out, so an armored PC could never be Broken (the same infinite-loop
# problem `research/armored_enemy_breaking_problem.md` found on the enemy
# side, relocated to the player side). `armor_downgrade` now takes a
# per-scene budget counter instead of gating by tier; see
# `test_combat.py::TestArmorDowngrade`/`TestArmorBreakability` for its
# current behaviour. Not part of the G0 baseline — G0 pins the extraction
# (A0.3), not this redesign (A5) — so this section documents what changed
# rather than asserting the old signature still works.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Targeted semantics — apply_condition stacking / zero-End absorb
#
# SUPERSEDED (F5, task A6): the zero-End escalation pinned below — an
# Absorb taken at 0 Endurance upgraded to a persistent Tier 2 — was a
# simulator-only house rule (`is_zero_end_absorb`), never part of the PHB,
# `facet.yaml`, or the engine. DESIGN §4.3 retires it: D1 removes enemies'
# Condition kill-track and D2 makes armored PCs breakable without it. The
# rule is now no rule — Absorb applies the incoming tier unmodified.
# ---------------------------------------------------------------------------

class TestApplyConditionSemantics:
    def test_same_tier2_condition_twice_escalates_to_broken(self, ruleset):
        conditions: list[str] = []
        combat_module.apply_condition(conditions, "staggered", 2, ruleset)
        result = combat_module.apply_condition(conditions, "staggered", 2, ruleset)
        assert result.broken is True

    def test_different_tier2_conditions_coexist_without_breaking(self, ruleset):
        conditions: list[str] = []
        combat_module.apply_condition(conditions, "staggered", 2, ruleset)
        result = combat_module.apply_condition(conditions, "cornered", 2, ruleset)
        assert result.broken is False
        assert set(conditions) == {"staggered", "cornered"}

    def test_zero_end_absorb_is_gone(self, ruleset):
        """F5 retired (DESIGN §4.3): an Absorb at 0 Endurance applies the
        incoming tier unmodified — no escalation to a persistent Tier 2."""
        conditions: list[str] = []
        result = combat_module.apply_condition(conditions, "winded", 1, ruleset)
        assert conditions == ["winded"]
        assert result.tier == 1


# ---------------------------------------------------------------------------
# Targeted semantics — end_exchange (formerly cleanup_end_of_exchange)
# ---------------------------------------------------------------------------

class TestEndExchangeSemantics:
    def test_tier1_clears_tier2_persists(self, ruleset):
        conditions = ["winded", "staggered"]
        combat_module.end_exchange(conditions, ruleset)
        assert conditions == ["staggered"]

    def test_withdrawn_recovery_amount_matches_ruleset(self, ruleset):
        # end_exchange only touches conditions (Endurance field names diverge
        # across combatant types — see combat.py's docstring); the recovery
        # amount itself is still ruleset-driven and pinned here.
        assert combat_module.withdrawn_recovery_amount(ruleset) == 2


# ---------------------------------------------------------------------------
# Targeted semantics — reaction Endurance cost by posture
# ---------------------------------------------------------------------------

class TestReactionCostByPosture:
    """Cost is deterministic regardless of dice — no seeding required.
    Confirmed against a live scenario (posture, expected_cost) =
    (aggressive, 2), (measured, 1), (defensive, 0), (withdrawn, 0)."""

    def test_aggressive_adds_1_to_base_cost(self, ruleset):
        assert combat_module.reaction_cost("dodge", "aggressive", ruleset) == 2

    def test_measured_is_base_cost(self, ruleset):
        assert combat_module.reaction_cost("dodge", "measured", ruleset) == 1

    def test_defensive_subtracts_1_floored_at_0(self, ruleset):
        assert combat_module.reaction_cost("dodge", "defensive", ruleset) == 0

    def test_withdrawn_is_free(self, ruleset):
        assert combat_module.reaction_cost("dodge", "withdrawn", ruleset) == 0


# ---------------------------------------------------------------------------
# G0 baseline — 5 fixed seeds, full run_combat, exact end-state
# ---------------------------------------------------------------------------

def _pc_state(p):
    # persistent_conditions is not compared: A0.3 dropped the field from
    # PCState/EnemyState (WS-A0 established it was redundant with a Tier
    # 2+ membership check — see combat.py's `end_exchange` docstring).
    # Conditions, Endurance, Sparks, and Broken status are DESIGN's
    # explicit G0 checklist and are still pinned exactly.
    return (p.name, p.endurance_current, p.endurance_max, tuple(p.conditions),
            p.sparks_spent, p.is_broken)


def _enemy_state(e):
    # is_broken dropped (A8, D1): enemies have no Condition-based Broken
    # track anymore — defeat is is_removed via Resolve reaching 0.
    # phase_changed -> phase_index: informational Resolve-threshold crossing
    # (None or a crossed index), not a Condition escalation.
    return (e.instance_id, e.resolve_current, e.resolve, tuple(e.conditions),
            e.is_removed, e.phase_index)


class TestG0FixedSeedEndStates:
    """5 fixed seeds against `run_combat`, pinning the *exact* end-state —
    not an aggregate win rate. Values below were captured from an
    unmodified run of `tools.combat_sim` on 2026-07-10 and are the
    G0 baseline for A0.3."""

    def test_seed_1_mook_wipe(self):
        random.seed(1)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(harbor_thug_def(), i) for i in (0, 2, 3)]
        result = run_combat(pcs, enemies)

        assert (result.party_wins, result.exchanges, result.sparks_spent,
                result.enemies_remaining) == (True, 3, 1, 0)
        assert [_pc_state(p) for p in pcs] == [
            ("Mordai", 5, 5, (), 0, False),
            ("Zahna", 0, 3, (), 1, False),
            ("Zulnut", 3, 3, (), 0, False),
        ]
        assert all(e.is_removed and not e.conditions for e in enemies)

    def test_seed_1_named_sergeant_zahna_broken(self):
        """Pinned value updated by A8/D1: `_pc_strike`'s enemy-durability
        model migrated from Condition-stacking to Resolve depletion
        (`combat.apply_resolve_damage`) — the Sergeant's Resolve (3, +1
        light armor = 4) drains in a single exchange instead of taking
        several Condition hits to escalate to Broken. Not a G0 regression —
        G0 pins the WS-A0 extraction only; see this file's module
        docstring on why re-pinning after an intentional rule change
        (D1, the same class as A5/A6's D2/F5 updates above) is expected.

        Re-pinned again by A14 (§5-quater F5): enemies no longer spend
        Resolve to Parry, so the fight resolves purely on the PCs' Strike
        outcomes — Zulnut now Presses (End 3→2, +1 Spark) and total Sparks
        spent moves 1 → 2.
        """
        random.seed(1)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(city_watch_sergeant_def())]
        result = run_combat(pcs, enemies)

        assert (result.party_wins, result.exchanges, result.sparks_spent,
                result.pcs_broken) == (True, 1, 2, [])
        assert [_pc_state(p) for p in pcs] == [
            ("Mordai", 4, 5, (), 0, False),
            ("Zahna", 2, 3, (), 1, False),
            ("Zulnut", 2, 3, (), 1, False),
        ]
        assert _enemy_state(enemies[0]) == (
            "sergeant", 0, 3, ("staggered",), True, None,
        )

    def test_seed_2_boss_defeated_with_phase_change(self):
        """Pinned value updated by A8/G1 (DESIGN §5-bis): the Archive
        Guardian's base Resolve moved 5 -> 8 (a content retune, not an
        engine regression — the Guardian's `.fof` and `archive_guardian_def`
        fixture both changed).

        Re-pinned again by A14 (§5-quater F5): with enemy Parry removed the
        Guardian no longer bleeds Resolve defending itself, so this seed's
        fight shortens 4 -> 3 exchanges *and* now crosses the Resolve-2 phase
        threshold before defeat (`phase_index` 0, not `None`). This seed
        formerly did NOT fire the phase; that it does now is exactly the
        Accept (c) signal A13 re-checks — removing the self-defeating enemy
        Parry raises the fraction of by-the-book fights in which the second
        act actually triggers.

        Formerly (pre-D1) (True, 20, 9, 0), Mordai Broken; (D1, Resolve 5)
        (True, 2, 5, 0) no phase; (A8/G1, Resolve 8) (True, 4, 8, 0) no
        phase; now (A14, no enemy Parry) (True, 3, 6, 0) with phase.
        """
        random.seed(2)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(archive_guardian_def())]
        result = run_combat(pcs, enemies)

        assert (result.party_wins, result.exchanges, result.sparks_spent,
                result.enemies_remaining) == (True, 3, 6, 0)
        assert result.pcs_broken == []
        assert [_pc_state(p) for p in pcs] == [
            ("Mordai", 2, 5, (), 3, False),
            ("Zahna", 2, 3, (), 1, False),
            ("Zulnut", 2, 3, (), 2, False),
        ]
        assert _enemy_state(enemies[0]) == (
            "guardian", 0, 8, ("staggered", "cornered"), True, 0,
        )

    def test_seed_3_boss_defeated_after_phase_change(self):
        """Pinned value updated by A8/G1 — same Resolve 5 -> 8 retune as
        test_seed_2's note above. This seed's Guardian crosses its
        Resolve-2 phase threshold before defeat (`phase_index == 0`).

        Re-pinned again by A14 (§5-quater F5): enemy Parry removed, so the
        Guardian takes full outcome depletion every landed Strike — the
        fight shortens 3 -> 2 exchanges and the rider snowball lands both
        Tier 2 Conditions ('staggered', 'cornered') before defeat.

        Formerly (D1, Resolve 5) (True, 2, 4) no phase; (A8/G1, Resolve 8)
        (True, 3, 6) with phase; now (A14, no enemy Parry) (True, 2, 5).
        """
        random.seed(3)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(archive_guardian_def())]
        result = run_combat(pcs, enemies)

        assert (result.party_wins, result.exchanges, result.sparks_spent) == (
            True, 2, 5,
        )
        assert [_pc_state(p) for p in pcs] == [
            ("Mordai", 3, 5, (), 2, False),
            ("Zahna", 0, 3, (), 1, False),
            ("Zulnut", 2, 3, (), 2, False),
        ]
        assert _enemy_state(enemies[0]) == (
            "guardian", 0, 8, ("staggered", "cornered"), True, 0,
        )

    def test_seed_5_named_mordai_double_condition(self):
        """Pinned value updated by A8/D1 — same migration as test_seed_1's
        note above. Formerly renamed once already (A5/D2, then A6/F5);
        this is the third and largest jump, since D1 replaces the
        enemy-side resolution model wholesale rather than tuning one input
        to it.

        Re-pinned again by A14 (§5-quater F5): with enemy Parry gone the
        Sergeant can no longer deflect a Strike, so the killing exchange now
        lands a 'staggered' rider (Zahna Presses, +1 Spark) instead of a
        clean no-condition drop.
        """
        random.seed(5)
        pcs = [make_pc(d) for d in standard_party()]
        enemies = [make_enemy(city_watch_sergeant_def())]
        result = run_combat(pcs, enemies)

        assert (result.party_wins, result.exchanges, result.sparks_spent) == (
            True, 1, 1,
        )
        assert [_pc_state(p) for p in pcs] == [
            ("Mordai", 4, 5, (), 0, False),
            ("Zahna", 2, 3, (), 1, False),
            ("Zulnut", 3, 3, (), 0, False),
        ]
        assert _enemy_state(enemies[0]) == (
            "sergeant", 0, 3, ("staggered",), True, None,
        )
