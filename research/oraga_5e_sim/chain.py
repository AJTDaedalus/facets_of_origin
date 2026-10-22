"""chain.py: the post-midnight attrition chain, Oraga Night 5e (three-player pass).

Rebuilt for TASKS T3.1 from docs/audit_oraga_5e_3p/TUNING_3P.md §2, §5 and F3/F5;
the original scratchpad script was lost. One party fights, with Hit Points, spell
slots, Heroic and Bardic Inspiration, Second Wind and Channel Divinity carried
forward and no rest (the night allows none after midnight):

    [optional Movement V card, before midnight]  ->  S14 (s14.py)
        ->  S13, the arrest in the fire (skirm.py)  ->  the gate: S3's fight

Between scenes everyone down gets up with 1 HP (the crowd rule; "between fights,
when the night runs in beats, they are up by the next beat"), and, unless
--no-between-heal, each healer spends one 1st-level slot on the most-hurt ally
and Dassa takes a Second Wind if she is below half. "HP at the gate" is the
party's Hit Points on reaching S3 as a share of its maximum (a dead PC counts 0).

Usage:
    python chain.py --party C1 --n 4000 --seed 1
    python chain.py --party C1 --mv5 S2 --n 4000 --seed 1
    python chain.py --all --n 2000 --seed 1
Pure standard library; deterministic for a given --seed.
"""
import argparse
import random

from s14 import run_s14
from skirm import CARDS, PARTIES, heal_pc, make_party, roll, run_fight, stand_up_all


def between_scenes(pcs, rng, heal=True):
    stand_up_all(pcs)
    if not heal:
        return
    for p in pcs:
        if p.name == "Dassa" and not p.dead and p.second_wind > 0 and p.hp <= p.max_hp // 2:
            p.second_wind -= 1
            heal_pc(p, roll(rng, 1, 10) + 4)
    for healer in pcs:
        if healer.dead or not healer.healing_word or healer.slots.get(1, 0) <= 0:
            continue
        live = [p for p in pcs if not p.dead]
        worst = min(live, key=lambda p: p.hp / p.max_hp)
        if worst.hp >= worst.max_hp * 0.75:
            continue
        healer.slots[1] -= 1
        if healer.name == "Ilesse":                       # Cure Wounds + Disciple of Life
            heal_pc(worst, roll(rng, 2, 8) + 4 + 3)
        else:                                             # Serane: Healing Word
            heal_pc(worst, roll(rng, 2, 4) + 4)


def hp_share(pcs):
    return sum(0 if p.dead else p.hp for p in pcs) / sum(p.max_hp for p in pcs)


def run_chain(party, rng, crowd="strict", mv5_card=None, s14_policy="engaged",
              s13_card="S13", s3_card="S3", heal=True):
    pcs = make_party(party, False, rng)
    out = {}
    if mv5_card:
        r = run_fight(mv5_card, pcs, rng, crowd)
        out["any_drop_mv5"] = r["any_drop"]
        between_scenes(pcs, rng, heal)
    r = run_s14(pcs, rng, s14_policy)
    out["any_drop_s14"] = r["any_drop"]
    out["s14_win"] = r["result"] in ("focus", "hp")
    between_scenes(pcs, rng, heal)
    r = run_fight(s13_card, pcs, rng, crowd)
    out["any_drop_s13"] = r["any_drop"]
    between_scenes(pcs, rng, heal)
    out["hp_at_gate"] = hp_share(pcs)
    r = run_fight(s3_card, pcs, rng, crowd)
    out["any_drop_s3"] = r["any_drop"]
    out["pc_death"] = any(p.dead for p in pcs)
    return out


def simulate(party="C1", n=4000, seed=1, crowd="strict", mv5_card=None,
             s14_policy="engaged", s13_card="S13", s3_card="S3", heal=True):
    rng = random.Random(f"chain|{party}|{crowd}|{mv5_card}|{s14_policy}|{s13_card}|"
                        f"{s3_card}|{heal}|{seed}")
    keys = ["any_drop_s14", "s14_win", "any_drop_s13", "any_drop_s3", "pc_death"]
    if mv5_card:
        keys.append("any_drop_mv5")
    tot = {k: 0 for k in keys}
    hp = 0.0
    for _ in range(n):
        r = run_chain(party, rng, crowd, mv5_card, s14_policy, s13_card, s3_card, heal)
        for k in keys:
            tot[k] += r[k]
        hp += r["hp_at_gate"]
    res = dict(runs=n, party=party, crowd=crowd, mv5=mv5_card, hp_at_gate=hp / n)
    res.update({k: tot[k] / n for k in keys})
    return res


def _fmt(r):
    s = (f"{r['party']:<3} mv5={str(r['mv5']):<5} crowd={r['crowd']:<8} "
         f"HP at gate {100*r['hp_at_gate']:5.1f}%  death {100*r['pc_death']:5.1f}%  "
         f"drop S14 {100*r['any_drop_s14']:4.1f} S13 {100*r['any_drop_s13']:4.1f} "
         f"S3 {100*r['any_drop_s3']:4.1f}  S14 win {100*r['s14_win']:4.1f}")
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description="Post-midnight attrition chain")
    ap.add_argument("--party", default="C1", choices=sorted(PARTIES))
    ap.add_argument("--mv5", default=None, choices=sorted(CARDS),
                    help="a Movement V card fought first (e.g. S2)")
    ap.add_argument("--crowd", default="strict", choices=["strict", "generous"])
    ap.add_argument("--to-the-last", action="store_true",
                    help="S13 and S3 fought with no morale (S13_last, S3_last)")
    ap.add_argument("--no-between-heal", action="store_true")
    ap.add_argument("--all", action="store_true", help="every party, with and without S2")
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args(argv)
    s13 = "S13_last" if a.to_the_last else "S13"
    s3 = "S3_last" if a.to_the_last else "S3"
    heal = not a.no_between_heal
    print(f"chain.py seed={a.seed} n={a.n} crowd={a.crowd} s13={s13} s3={s3} "
          f"between_heal={heal}")
    if a.all:
        for p in ("C1", "C2", "C3", "C4", "C5", "4P"):
            for mv5 in (None, "S2"):
                print(_fmt(simulate(p, a.n, a.seed, a.crowd, mv5, "engaged", s13, s3, heal)))
    else:
        print(_fmt(simulate(a.party, a.n, a.seed, a.crowd, a.mv5, "engaged", s13, s3, heal)))


if __name__ == "__main__":
    main()
