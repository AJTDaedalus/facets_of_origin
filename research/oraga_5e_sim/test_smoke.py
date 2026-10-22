"""Smoke and regression tests for the Oraga Night 5e three-player harness (TASKS T3.1).

Each script runs at N=200 with a fixed seed and must return a sane result
dictionary; each also carries one regression assertion: a coarse relation
from TUNING_3P that should survive small modelling changes. The tight,
4,000-run reproduction checks are recorded in README.md, not here (too slow
for a smoke suite).

Run: python -m pytest research/oraga_5e_sim -q
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import chain  # noqa: E402
import s14  # noqa: E402
import skirm  # noqa: E402

N = 200
SEED = 20261022


def _is_rate(x):
    return isinstance(x, float) and 0.0 <= x <= 1.0


# --------------------------------------------------------------------------- s14

def test_s14_structure():
    r = s14.simulate(party="C1", policy="engaged", n=N, seed=SEED)
    assert r["runs"] == N
    for k in ("win", "any_drop", "all_down", "win_by_focus", "win_by_hp"):
        assert _is_rate(r[k]), k
    assert r["mean_rounds"] > 0
    assert r["delay_bought"] >= 0
    assert abs(r["win_by_focus"] + r["win_by_hp"] - r["win"]) < 1e-9


def test_s14_deterministic():
    a = s14.simulate(party="C2", policy="naive", n=N, seed=SEED)
    b = s14.simulate(party="C2", policy="naive", n=N, seed=SEED)
    assert a == b


def test_s14_every_party_and_policy_runs():
    for party in s14.PARTIES:
        for policy in s14.POLICIES:
            r = s14.simulate(party=party, policy=policy, n=20, seed=SEED)
            assert r["runs"] == 20


def test_s14_regression_engaged_beats_slugging():
    # TUNING_3P Appendix: C1 engaged 90.7% vs slug 0.2%.
    eng = s14.simulate(party="C1", policy="engaged", n=N, seed=SEED)
    slug = s14.simulate(party="C1", policy="slug", n=N, seed=SEED)
    assert eng["win"] >= 0.75
    assert slug["win"] <= 0.15
    assert eng["win"] > slug["win"]


# ------------------------------------------------------------------------- skirm

def test_skirm_structure():
    r = skirm.simulate(card="S8", party="C1", n=N, seed=SEED)
    assert r["runs"] == N
    for k in ("any_drop", "pc_death", "party_wiped", "enemies_broke"):
        assert _is_rate(r[k]), k
    assert r["mean_drops"] >= 0
    assert r["mean_rounds"] > 0


def test_skirm_deterministic_and_all_cards_run():
    for card in skirm.CARDS:
        a = skirm.simulate(card=card, party="C3", n=20, seed=SEED)
        b = skirm.simulate(card=card, party="C3", n=20, seed=SEED)
        assert a == b, card


def test_skirm_solo_runs():
    r = skirm.simulate(card="S2", party="C1", n=N, seed=SEED, solo="Dassa")
    assert r["runs"] == N and _is_rate(r["any_drop"])


SOLO = ("S2", "S4", "S7", "S8", "S9", "S10", "S13")
FIGHTERS = ("Dassa", "Pello", "Andra")


def test_skirm_solo_lines_exist_and_run():
    """T3.10: every card a lone PC can walk into has a <card>_solo line."""
    for c in SOLO:
        assert c + "_solo" in skirm.CARDS, c
        for p in skirm.PREGENS:
            r = skirm.simulate(c + "_solo", n=50, seed=SEED, solo=p)
            assert _is_rate(r["any_drop"])


def test_skirm_regression_solo_line_softer_than_current():
    """T3.10: for a lone fighter, each solo line drops them no more often than the
    current rule (the three-character roster), and is never a sure thing."""
    for c in SOLO:
        for p in FIGHTERS:
            cur = skirm.simulate(c, n=N, seed=SEED, solo=p)["any_drop"]
            new = skirm.simulate(c + "_solo", n=N, seed=SEED, solo=p)["any_drop"]
            assert new <= cur + 0.08, (c, p, cur, new)
            assert 0.05 <= new <= 0.85, (c, p, new)


def test_skirm_regression_s8_fix_softer():
    # TUNING_3P F7: S8 as written C1 57%; breaking at one down 5-16%.
    base = skirm.simulate(card="S8", party="C1", n=N, seed=SEED)
    fix = skirm.simulate(card="S8_fix", party="C1", n=N, seed=SEED)
    assert base["any_drop"] > fix["any_drop"] + 0.2


# ------------------------------------------------------------------------- chain

def test_chain_structure():
    r = chain.simulate(party="C1", n=N, seed=SEED)
    assert r["runs"] == N
    for k in ("hp_at_gate", "pc_death", "any_drop_s14", "any_drop_s13", "any_drop_s3"):
        assert _is_rate(r[k]), k


def test_chain_deterministic():
    assert chain.simulate(party="C4", n=50, seed=SEED) == chain.simulate(party="C4", n=50, seed=SEED)


def test_chain_regression_party_reaches_gate_worn_down():
    # TUNING_3P F5's two qualitative claims: a Movement V fight first leaves the
    # party lower at the gate, and a party with no healer (C4) arrives lower than
    # one with Ilesse (C1). (TUNING's absolute 15-21% does not reproduce; see
    # README "Gaps". The first draft of this test asserted it and was revised.)
    r = chain.simulate(party="C1", n=N, seed=SEED)
    assert 0.0 < r["hp_at_gate"] < 1.0
    with_mv5 = chain.simulate(party="C1", n=N, seed=SEED, mv5_card="S2")
    assert with_mv5["hp_at_gate"] < r["hp_at_gate"]
    no_healer = chain.simulate(party="C4", n=N, seed=SEED)
    assert no_healer["hp_at_gate"] < r["hp_at_gate"]


# --------------------------------------------------------------------------- CLI

def test_cli_each_script():
    for script, extra in (("s14.py", ["--party", "C1"]),
                          ("skirm.py", ["--card", "S7"]),
                          ("chain.py", ["--party", "C1"])):
        out = subprocess.run([sys.executable, os.path.join(HERE, script),
                              "--n", "20", "--seed", "1", *extra],
                             capture_output=True, text=True, timeout=120)
        assert out.returncode == 0, out.stderr
        assert "seed=1" in out.stdout
