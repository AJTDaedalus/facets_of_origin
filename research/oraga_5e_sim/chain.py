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
from dataclasses import dataclass, fields

from s14 import NEW, OLD, run_s14
from skirm import (CARDS, PARTIES, WP6, heal_pc, make_party, roll, run_fight, short_rest,
                   spend_hit_die, stand_up_all)


@dataclass(frozen=True)
class ChainWP6:
    """WP6 switches for the chain (T6.9). All off = the T3.1 chain, draw for draw.
    s14_new:   S14 under the WP5 rules (`s14.NEW`, the one level TP57 kept).
    potions:   one Potion of Healing each (T6.8, the kitchens); drunk or fed in a fight
               (skirm.WP6.potions), and between scenes by anyone under half HP.
    hit_die:   one Hit Die each at the toast, spent after the optional early card if hurt.
    chapel:    the chapel's Short Rest after the Movement V card (before midnight).
    finish:    S13 is a heat-4 snake: Draunel's men finish a downed character.
    cards:     the WP6 rosters and morale (S13_wp6, S3_wp6) in place of S13 / S3."""
    s14_new: bool = False
    potions: bool = False
    hit_die: bool = False
    chapel: bool = False
    finish: bool = False
    cards: bool = False

    @classmethod
    def full(cls):
        return cls(**{f.name: True for f in fields(cls)})

    def any(self):
        return any(getattr(self, f.name) for f in fields(self))

    def tag(self):
        return "".join(str(int(getattr(self, f.name))) for f in fields(self))


def between_scenes(pcs, rng, heal=True, potions=False):
    stand_up_all(pcs)
    if potions:
        for p in pcs:
            if not p.dead and p.potions > 0 and p.hp < p.max_hp // 2:
                p.potions -= 1
                heal_pc(p, roll(rng, 2, 4) + 2)
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
              s13_card="S13", s3_card="S3", heal=True, wp6=None, early_card=None):
    w = wp6 or ChainWP6()
    pcs = make_party(party, False, rng)
    if w.potions:
        for p in pcs:
            p.potions = 1
    fight6 = WP6(potions=w.potions) if w.potions else None
    out = {}
    if early_card:                                   # a Movement II-IV card, before the toast
        run_fight(early_card, pcs, rng, crowd, wp6=fight6)
        between_scenes(pcs, rng, heal, w.potions)
    if w.hit_die:                                    # the toast: one Hit Die, if hurt
        for p in pcs:
            if p.hp < p.max_hp:
                spend_hit_die(p, rng)
    if mv5_card:
        r = run_fight(mv5_card, pcs, rng, crowd, wp6=fight6)
        out["any_drop_mv5"] = r["any_drop"]
        between_scenes(pcs, rng, heal, w.potions)
    if w.chapel:                                     # half a Movement in the chapel
        for p in pcs:
            short_rest(p, rng)
    if w.s14_new:
        r = run_s14(pcs, rng, s14_policy, rules=NEW)
    else:
        r = run_s14(pcs, rng, s14_policy)
    out["any_drop_s14"] = r["any_drop"]
    out["s14_win"] = r["result"] in ("focus", "hp")
    between_scenes(pcs, rng, heal, w.potions)
    if w.cards and s13_card == "S13":
        s13_card = "S13_wp6"
    if w.cards and s3_card == "S3":
        s3_card = "S3_wp6"
    s13_rules = WP6(potions=w.potions, heat4_finish=w.finish) if (w.potions or w.finish) else None
    r = run_fight(s13_card, pcs, rng, crowd, wp6=s13_rules)
    out["any_drop_s13"] = r["any_drop"]
    between_scenes(pcs, rng, heal, w.potions)
    out["hp_at_gate"] = hp_share(pcs)
    r = run_fight(s3_card, pcs, rng, crowd, wp6=fight6)
    out["any_drop_s3"] = r["any_drop"]
    out["pc_death"] = any(p.dead for p in pcs)
    return out


def simulate(party="C1", n=4000, seed=1, crowd="strict", mv5_card=None,
             s14_policy="engaged", s13_card="S13", s3_card="S3", heal=True, wp6=None,
             early_card=None):
    tag = ""
    if wp6 is not None and wp6.any():
        tag += "|wp6:" + wp6.tag()
    if early_card:
        tag += "|early:" + early_card
    rng = random.Random(f"chain|{party}|{crowd}|{mv5_card}|{s14_policy}|{s13_card}|"
                        f"{s3_card}|{heal}|{seed}" + tag)
    keys = ["any_drop_s14", "s14_win", "any_drop_s13", "any_drop_s3", "pc_death"]
    if mv5_card:
        keys.append("any_drop_mv5")
    tot = {k: 0 for k in keys}
    hp = 0.0
    for _ in range(n):
        r = run_chain(party, rng, crowd, mv5_card, s14_policy, s13_card, s3_card, heal, wp6,
                      early_card)
        for k in keys:
            tot[k] += r[k]
        hp += r["hp_at_gate"]
    res = dict(runs=n, party=party, crowd=crowd, mv5=mv5_card, hp_at_gate=hp / n)
    if wp6 is not None and wp6.any():
        res["wp6"] = wp6.tag()
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
    ap.add_argument("--wp6", default=None,
                    help="'full', or a comma list of ChainWP6 switches: "
                         "s14_new,potions,hit_die,chapel,finish,cards")
    ap.add_argument("--early", default=None, choices=sorted(CARDS),
                    help="a Movement II-IV card fought before the toast (e.g. S6)")
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args(argv)
    s13 = "S13_last" if a.to_the_last else "S13"
    s3 = "S3_last" if a.to_the_last else "S3"
    heal = not a.no_between_heal
    if a.wp6 == "full":
        wp6 = ChainWP6.full()
    elif a.wp6:
        wp6 = ChainWP6(**{k: True for k in a.wp6.split(",")})
    else:
        wp6 = None
    print(f"chain.py seed={a.seed} n={a.n} crowd={a.crowd} s13={s13} s3={s3} "
          f"between_heal={heal}")
    if a.all:
        for p in ("C1", "C2", "C3", "C4", "C5", "4P"):
            for mv5 in (None, "S2"):
                print(_fmt(simulate(p, a.n, a.seed, a.crowd, mv5, "engaged", s13, s3, heal,
                                    wp6, a.early)))
    else:
        print(_fmt(simulate(a.party, a.n, a.seed, a.crowd, a.mv5, "engaged", s13, s3, heal,
                            wp6, a.early)))


if __name__ == "__main__":
    main()
