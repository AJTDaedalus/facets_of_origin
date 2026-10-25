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


# ------------------------------------------------------------ s14, WP5 switches (T5.8)

import random  # noqa: E402
from dataclasses import replace  # noqa: E402


def _fight(rules, party="C1", policy="engaged", dial="sharp", seed=7, **kw):
    rng = random.Random(seed)
    pcs = s14.make_s14_party(party, False, rng)
    return s14.S14(pcs, rng, policy, False, rules=rules, dial=dial, **kw), pcs


def test_s14_old_switches_reproduce_t31_baseline():
    """OLD is the T3.1 harness draw for draw: the seed string and the numbers."""
    a = s14.simulate("C1", "engaged", n=N, seed=SEED)
    b = s14.simulate("C1", "engaged", n=N, seed=SEED, rules=s14.Rules())
    assert a == b
    assert "pc_death" not in a


def test_s14_every_switch_runs_and_new_differs():
    for sw in s14.SWITCHES:
        r = s14.simulate("C2", "engaged", n=40, seed=SEED, rules=replace(s14.OLD, **{sw: True}))
        assert _is_rate(r["win"]) and _is_rate(r["pc_death"]), sw
    new = s14.simulate("C1", "engaged", n=N, seed=SEED, rules=s14.NEW)
    old = s14.simulate("C1", "engaged", n=N, seed=SEED)
    assert new["win"] != old["win"]


def test_s14_lethal_kills_only_when_lethal():
    """TP57: one level (sharp). The legacy dial values still order as WP5 ran them."""
    old = s14.simulate("C3", "slug", n=N, seed=SEED, rules=replace(s14.NEW, lethal=False))
    assert old["pc_death"] == 0.0
    sharp = s14.simulate("C3", "slug", n=N, seed=SEED, rules=s14.NEW, dial="sharp")
    merc = s14.simulate("C3", "slug", n=N, seed=SEED, rules=s14.NEW, dial="merciless")
    gent = s14.simulate("C3", "slug", n=N, seed=SEED, rules=s14.NEW, dial="gentle")
    assert gent["pc_death"] <= 0.02
    assert sharp["pc_death"] > 0.0
    assert merc["pc_death"] >= sharp["pc_death"]


def test_s14_idle_drop_is_set_aside_focused_drop_is_dying():
    f, pcs = _fight(s14.NEW)
    pc = pcs[0]
    f.focused = False
    f.hit_pc(pc, pc.hp)
    assert pc.down and pc.stable and pc.name in f.set_aside
    f2, pcs2 = _fight(s14.NEW)
    q = pcs2[0]
    f2.focused = True
    f2.hit_pc(q, q.hp)
    assert q.down and not q.stable


def test_s14_damage_to_downed_by_legacy_dial():
    """TP57: one level; "sharp" is the rule. The legacy values reproduce WP5."""
    for dial, expect in (("gentle", 0), ("sharp", 2), ("merciless", 2)):
        f, pcs = _fight(s14.NEW, dial=dial)
        pc = pcs[1]
        f.focused = True
        f.hit_pc(pc, pc.hp)          # drops (Gentle: Stable at once)
        f.hit_pc(pc, 5)              # a hit on a downed creature
        assert pc.ds_fail == expect, dial


def test_s14_clears_the_way_costs_the_action():
    f, pcs = _fight(s14.NEW)
    f.ctx.round = 1
    f.wept_delay = 1
    f.last_hit_by = {}
    f.att_turn(1)                    # Idle, not struck: it clears and attacks nobody
    assert f.wept_delay == 0 and f.clears == 1
    assert all(p.hp == p.max_hp for p in pcs)
    g, _ = _fight(s14.NEW)
    g.ctx.round = 1
    g.wept_delay = 1
    g.clock = 5
    g.last_hit_by = {"Dassa": 5}     # struck since its last turn: no clearing
    g.att_turn(1)
    assert g.wept_delay == 1 and g.clears == 0
    h, _ = _fight(s14.NEW)
    h.ctx.round = 1
    h.wept_delay = 1
    h.lost_turn = True               # a lost turn clears nothing
    h.att_turn(1)
    assert h.wept_delay == 1


def test_s14_help_dc18_idle_free_nat20_and_orders_window():
    f, pcs = _fight(s14.NEW)
    f.focused = True
    assert f.focused_dc() == 18
    serane = pcs[2]                  # her best trick has no Advantage of its own
    base = f.best_p(serane)
    f.helped = (serane.name, f.ctx.round)
    assert f.best_p(serane) > base   # Help: Advantage
    g, pcs2 = _fight(s14.NEW)
    g.focused = False
    g.do_trick(pcs2[1])
    assert not g.trick_uses           # a trick tried while Idle is not spent
    o, pcs3 = _fight(s14.OLD)
    o.focused = False
    o.do_trick(pcs3[1])
    assert o.trick_uses
    w, pcs4 = _fight(s14.NEW)
    w.ctx.round = 3
    w.interf_round = {p.name: 2 for p in pcs4}
    assert len(w.valid_targets()) == len(pcs4)   # since the start of its previous round
    w.interf_round = {p.name: 1 for p in pcs4}
    assert w.valid_targets() == []


def test_s14_cap3_and_tie():
    f, _ = _fight(s14.NEW)
    f.wept_delay = 5
    moves = f.wept_moves
    for _ in range(4):
        f.wept_turn()
    assert f.wept_lost == 3 and f.wept_moves == moves - 1


def test_s14_solo_line_softer_and_tp30_tricks():
    a = s14.simulate("C1", "engaged", n=N, seed=SEED, rules=replace(s14.NEW, solo_line=False),
                     solo="Dassa")
    b = s14.simulate("C1", "engaged", n=N, seed=SEED, rules=s14.NEW, solo="Dassa")
    assert b["any_drop"] < a["any_drop"]
    f, pcs = _fight(s14.NEW, party="C3")
    names = [t[0] for p in pcs for t in p.tricks]
    assert not any("cup" in n for n in names)


def test_s14_regression_wp5_targets_at_sharp():
    """DESIGN §4 targets at Sharp: engaged wins >= 85%, a death <= 10%; slugging
    mostly loses (N=200 slack)."""
    eng = s14.simulate("C2", "engaged", n=N, seed=SEED, rules=s14.NEW)
    slug = s14.simulate("C2", "slug", n=N, seed=SEED, rules=s14.NEW)
    assert eng["win"] >= 0.85 and eng["pc_death"] <= 0.12
    assert slug["win"] <= 0.3


# --------------------------------------------------------------------------- WP6 (T6.9)

def test_wp6_all_off_reproduces_baseline():
    base = skirm.simulate("S13", "C1", n=N, seed=SEED)
    off = skirm.simulate("S13", "C1", n=N, seed=SEED, wp6=skirm.WP6())
    assert base == off
    c0 = chain.simulate("C1", n=50, seed=SEED)
    c1 = chain.simulate("C1", n=50, seed=SEED, wp6=chain.ChainWP6())
    assert c0 == c1


def test_wp6_potion_drunk_when_low():
    import random
    rng = random.Random(1)
    pcs = skirm.make_party("C1")
    pcs[0].hp = 5
    pcs[0].potions = 1
    ctx = skirm.Ctx(rng, lethal=True)
    ctx.wp6 = skirm.WP6(potions=True)
    pcs[0]._bonus_used = False
    assert skirm.try_potion(pcs[0], pcs, ctx)
    assert pcs[0].potions == 0 and pcs[0].hp >= 9


def test_wp6_potion_fed_to_dying_ally():
    import random
    rng = random.Random(2)
    pcs = skirm.make_party("C1")
    ally = pcs[1]
    ally.hp, ally.down, ally.stable = 0, True, False
    pcs[0].potions = 1
    pcs[0]._bonus_used = False
    ctx = skirm.Ctx(rng, lethal=True)
    ctx.wp6 = skirm.WP6(potions=True)
    assert skirm.try_potion(pcs[0], pcs, ctx)
    assert ally.up and ally.hp >= 4


def test_wp6_heat4_finish_hits_a_downed_pc():
    import random
    rng = random.Random(3)
    pcs = skirm.make_party("C1")
    pc = pcs[2]
    pc.hp, pc.down, pc.stable = 0, True, True
    en = skirm.E("Draunel Duelist")
    en.target = pc
    ctx = skirm.Ctx(rng, lethal=True)
    ctx.wp6 = skirm.WP6(heat4_finish=True)
    for _ in range(20):
        if skirm.finish_attack(en, pc, en.attacks[0], ctx):
            break
    assert pc.ds_fail >= 2 and not pc.stable


def test_wp6_finish_raises_deaths():
    a = skirm.simulate("S13_last", "C5", n=N, seed=SEED, wp6=skirm.WP6())
    b = skirm.simulate("S13_last", "C5", n=N, seed=SEED, wp6=skirm.WP6(heat4_finish=True))
    assert b["pc_death"] >= a["pc_death"]


def test_wp6_hit_die_and_short_rest():
    import random
    rng = random.Random(4)
    pcs = skirm.make_party("C1")
    d = pcs[0]
    d.hp = 10
    skirm.spend_hit_die(d, rng)
    assert d.hit_dice == 3 and 14 <= d.hp <= 23           # 1d10 + 3
    d.hp, d.second_wind = 5, 0
    skirm.short_rest(d, rng)
    assert d.second_wind == 1 and d.hit_dice < 3 and d.hp > 5


def test_wp6_half_down_morale_cards_exist():
    for c in ("S3_wp6", "S13_wp6", "S7_wp6", "S9_wp6"):
        assert c in skirm.CARDS
        r = skirm.simulate(c, "C1", n=50, seed=SEED)
        assert r["runs"] == 50


def test_wp6_chain_runs_and_reports():
    r = chain.simulate("C1", n=100, seed=SEED, wp6=chain.ChainWP6.full())
    assert _is_rate(r["hp_at_gate"]) and _is_rate(r["pc_death"])
    r2 = chain.simulate("C1", n=100, seed=SEED, wp6=chain.ChainWP6.full())
    assert r == r2


def test_tp61_chain_rules_leave_the_finish_off():
    w = chain.ChainWP6.tp61()
    assert not w.finish
    assert w.s14_new and w.potions and w.hit_die and w.chapel and w.cards
    assert chain.ChainWP6.full().finish            # legacy runs still reproduce


def test_tp61_chain_runs_and_is_deterministic():
    r = chain.simulate("C1", n=100, seed=SEED, wp6=chain.ChainWP6.tp61())
    r2 = chain.simulate("C1", n=100, seed=SEED, wp6=chain.ChainWP6.tp61())
    assert r == r2 and r["wp6"] == "111101"
