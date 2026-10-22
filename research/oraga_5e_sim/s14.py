"""s14.py: card S14, the Attendant, Oraga Night 5e (three-player pass).

Rebuilt for TASKS T3.1 from docs/audit_oraga_5e_3p/TUNING_3P.md §2 ("Method");
the original scratchpad script was lost. Models the rules AS PRINTED NOW (before
WP5): conversions/dnd5e/oraga_night/10_Bestiary.md "The Attendant",
09_The_Snakes.md card S14, and 05_The_Longest_Night.md "Midnight Rules".

Modelled:
- Idle / Focused (focus checked at the start of each of its turns: Focused if the
  Wept has no Delay); Two Turns while Focused, the second at initiative - 10;
  the three-character line (180 HP; second Focused turn is a single Joined
  Hands); the four-player block (229 HP, full Multiattack on both turns).
- Rusty (Idle: one Joined Hands at Disadvantage; Put Aside only if Bloodied or its
  focus has been broken twice); Put Aside recharge (5-6 Focused, 6 Idle), rolled at
  the start of its first turn each round; Literal Orders (it attacks only a PC who
  attacked it or failed a trick on it since its last turn; in round 1 the whole
  party counts, because the card fires on their interference).
- Clears the Way (once a round, at the first turn it keeps, after the focus check,
  if no non-furniture PC is within 5 ft).
- Can Be Distracted: DC 13 Idle / 19 Focused; +2 played out, +2 seen habit (max
  +4); repeats get no bonus and Disadvantage; one trick a round; success by 5 or a
  natural 20 also loses its next turn; four broken focuses = it wanders off;
  success while Idle makes the distractor furniture (does not count); failure while
  Focused puts its next attack on the distractor. Help does not apply.
- Down, Not Out (Stable; Healing Word or the crowd rule: up with 1 HP at the start
  of the round after next), "Hauling each other up", Heroic Inspiration (one each;
  the first PC to try a trick gains it, hint 4; a natural 20 pays its own).
- Party kit: Bardic Inspiration on a failed trick and Cutting Words, Tactical Mind,
  Shield, Sap, Vicious Mockery, Healing Word, Second Wind, Action Surge.
- The Wept's errand clock: the card fires with 1 Delay on her and her moves left at
  6 (three PCs) or 5 (four); at the start of her turn she spends a Delay or makes a
  move; when her moves run out the room is done and the Attendant leaves (a loss).

Policies (TUNING §2): slug, engaged, naive, smart. See README.md.

Usage:
    python s14.py --party C1 --policy engaged --n 4000 --seed 1
    python s14.py --all --n 4000 --seed 1        # the TUNING Appendix table
Pure standard library; deterministic for a given --seed.
"""
import argparse
import random

from skirm import (PARTIES, Ctx, Enemy, crowd_start_of_round, d20, damage_pc,
                   make_party, pc_defend, pc_offence, roll, second_wind,
                   try_bonus_heal)

POLICIES = ("engaged", "naive", "smart", "slug")
PARTIES = PARTIES  # re-export: C1..C5 and 4P


def p_success(bonus, adv, dc):
    """Chance that d20 + bonus >= dc (natural 1 fails, natural 20 succeeds)."""
    need = max(2, min(20, dc - bonus))
    p = (21 - need) / 20.0
    if adv > 0:
        return 1 - (1 - p) ** 2
    if adv < 0:
        return p * p
    return p


class S14:
    def __init__(self, pcs, rng, policy, four=False, moves=None, wept_delay=1):
        self.pcs = pcs
        self.rng = rng
        self.policy = policy
        self.four = four
        self.ctx = Ctx(rng, lethal=False)
        # slugging means everyone hits it, the cleric's slots included
        self.ctx.ilesse_attack = policy == "slug"
        hp = 229 if four else 180
        self.att = Enemy("Attendant", hp, 17, 3, attacks=[(7, 1, 10, 4)],
                         dex_save=3, wis_save=1, con_save=7)
        self.focused = False
        self.breaks = 0
        self.lost_turn = False
        self.put_aside = False
        self.tried_round = 0
        self.attack_distractor = None
        self.furniture = set()
        self.interferers = set(p.name for p in pcs)     # round 1: the party fired the card
        self.last_hit_by = {}
        self.clock = 0
        self.cleared_round = 0
        self.trick_uses = {}                            # (pc, trick) -> times tried
        self.first_try_done = False
        self.wept_delay = wept_delay
        self.wept_moves = moves if moves is not None else (5 if four else 6)
        self.delay_bought = 0
        self.result = None
        self.guard = None
        if policy == "smart":
            melee = [p for p in pcs if p.melee]
            self.guard = (max(melee, key=lambda p: p.max_hp) if melee
                          else max(pcs, key=lambda p: p.max_hp)).name

    # ------------------------------------------------------------------ tricks
    def trick_options(self, pc):
        """[(p, trick, bonus, adv)] for this PC at the current DC, best first."""
        dc = 19 if self.focused else 13
        out = []
        for t in pc.tricks:
            name, skill, habit, adv = t
            uses = self.trick_uses.get((pc.name, name), 0)
            if uses >= 2:
                continue
            if uses == 1:
                bonus, a = skill, (adv and 1 or 0) - 1
            else:
                if self.policy == "naive":
                    lean = 2 if self.rng.random() < 0.25 else 0
                else:
                    lean = 2 + (2 if habit else 0)
                bonus, a = skill + min(4, lean), (1 if adv else 0)
            out.append((p_success(bonus, a, dc), t, bonus, a))
        if self.policy == "naive":
            # bare rolls: the player reaches for the character's best skill,
            # whether or not that trick has been tried already
            out.sort(key=lambda x: -x[1][1])
        else:
            out.sort(key=lambda x: -x[0])
        return out

    def best_p(self, pc):
        o = self.trick_options(pc)
        return o[0][0] if o else 0.0

    def do_trick(self, pc):
        rng = self.rng
        opts = self.trick_options(pc)
        if not opts:
            return False
        _, t, bonus, adv = opts[0]
        name = t[0]
        self.trick_uses[(pc.name, name)] = self.trick_uses.get((pc.name, name), 0) + 1
        self.tried_round = self.ctx.round
        first_try = not self.first_try_done
        self.first_try_done = True
        dc = 19 if self.focused else 13
        nat = d20(rng, max(-1, min(1, adv)))
        total = nat + bonus
        if nat != 20 and (total < dc or nat == 1) and pc.hi:
            pc.hi = False
            nat = d20(rng, max(-1, min(1, adv)))
            total = nat + bonus
        ok = nat == 20 or (nat != 1 and total >= dc)
        lean_in = self.policy != "naive"
        if lean_in and not ok and nat != 1 and pc.name == "Dassa" and pc.second_wind > 0:
            extra = roll(rng, 1, 10)                       # Tactical Mind
            if total + extra >= dc:
                pc.second_wind -= 1
                total += extra
                ok = True
        if lean_in and not ok and nat != 1:
            bards = [b for b in self.pcs if b.bi > 0 and b.up and b is not pc]
            if bards:                                       # Bardic Inspiration (given earlier)
                bards[0].bi -= 1
                total += roll(rng, 1, 6)
                ok = total >= dc
        if nat == 20 or first_try:      # a natural 20 pays its own; hint 4 rewards the attempt
            pc.hi = True
        if ok and self.focused:
            self.breaks += 1
            self.focused = False
            if nat == 20 or total >= dc + 5:
                self.lost_turn = True
            if self.breaks >= 4:
                self.result = "focus"
        elif ok:
            self.furniture.add(pc.name)
            self.interferers.discard(pc.name)
        else:
            if self.focused:
                self.attack_distractor = pc.name
                self.interferers.add(pc.name)
                self.last_hit_by[pc.name] = self.clock
        return True

    def room_trick(self, pc):
        """Smart policy: buy Delay on the Wept (DC 13; distinct tricks)."""
        name, skill, _, adv = max(pc.tricks, key=lambda t: t[1] + (3 if t[3] else 0))
        if d20(self.rng, 1 if adv else 0) + skill >= 13:
            self.wept_delay += 1
            self.delay_bought += 1

    # ------------------------------------------------------------------ turns
    def pc_turn(self, pc, remaining):
        if not pc.up:
            return
        self.clock += 1
        ctx = self.ctx
        pc._bonus_used = False
        if pc.name == "Dassa":
            second_wind(pc, ctx)
        try_bonus_heal(pc, self.pcs, ctx)
        pol = self.policy
        if pol != "slug" and self.focused and self.tried_round != ctx.round:
            mine = self.best_p(pc)
            later = [self.best_p(q) for q in remaining if q.up]
            if mine > 0 and mine >= max(later, default=0.0):
                self.do_trick(pc)
                return
        if pol == "smart" and pc.name != self.guard and self.wept_delay == 0 \
                and self.delay_is_free(remaining):
            self.room_trick(pc)
            return
        dealt = pc_offence(pc, self.att, ctx, first_turn=(ctx.round == 1))
        self.interferers.add(pc.name)
        self.furniture.discard(pc.name)
        self.last_hit_by[pc.name] = self.clock
        if self.att.hp <= 0 and self.result is None:
            self.result = "hp"
        return dealt

    def delay_is_free(self, remaining_actors):
        """True when the Wept, not the Attendant, is the next of the two to act:
        a Delay bought now is spent before the Attendant can see it."""
        for kind in self._rest_kinds:
            if kind == "wept":
                return True
            if kind == "att":
                return False
        return self.wept_init > self.att_init

    def wept_turn(self):
        if self.wept_delay > 0:
            self.wept_delay -= 1
        else:
            self.wept_moves -= 1
            if self.wept_moves <= 0 and self.result is None:
                self.result = "errand"

    def valid_targets(self):
        return [p for p in self.pcs if p.up and p.name in self.interferers
                and p.name not in self.furniture]

    def choose_target(self):
        vt = self.valid_targets()
        if not vt:
            return None
        if self.attack_distractor:
            for p in vt:
                if p.name == self.attack_distractor:
                    return p
        return max(vt, key=lambda p: self.last_hit_by.get(p.name, -1))

    def joined_hands(self, pc, adv=0):
        att, ctx = self.att, self.ctx
        if att.disadv_next:
            adv -= 1
            att.disadv_next = False
        nat = d20(self.rng, max(-1, min(1, adv)))
        if nat == 1:
            return
        if not pc_defend(pc, nat + 7, nat, self.pcs, ctx):
            return
        dmg = roll(self.rng, 2 if nat == 20 else 1, 10) + 4
        pc.adjacent = False                                # pushed 5 ft
        damage_pc(pc, dmg, ctx, nonlethal=True)           # Down, Not Out

    def put_aside_on(self, primary):
        caught = [primary] + [p for p in self.valid_targets()
                              if p is not primary and p.adjacent]
        for p in caught:
            dmg = roll(self.rng, 2, 8)
            if d20(self.rng) + p.saves["str"] >= 15:
                dmg //= 2
            else:
                p.adjacent = False
            damage_pc(p, dmg, self.ctx, nonlethal=True)

    def att_turn(self, k):
        ctx = self.ctx
        # A broken focus lasts until the start of its next turn, so the focus
        # check happens even on a turn it then loses (success by 5).
        self.focused = self.wept_delay == 0
        if k == 1:
            self.second_turn = self.focused
        if self.lost_turn:
            self.lost_turn = False
            self.cleared_round = ctx.round      # a lost turn also loses Clears the Way
            self.interferers = set()
            self.attack_distractor = None
            return
            if not self.put_aside and self.rng.randint(1, 6) >= (5 if self.focused else 6):
                self.put_aside = True
        if self.cleared_round != ctx.round and self.wept_delay > 0:
            blockers = [p for p in self.pcs if p.up and p.adjacent
                        and p.name not in self.furniture]
            if not blockers:
                self.wept_delay -= 1
                self.cleared_round = ctx.round
        # attacks
        if self.focused:
            n_attacks = 2 if (k == 1 or self.four) else 1
            pa_ok = self.put_aside and (k == 1 or self.four)
            adv = 0
        else:
            n_attacks = 1
            pa_ok = self.put_aside and (self.att.bloodied or self.breaks >= 2)
            adv = -1
        for i in range(n_attacks):
            tgt = self.choose_target()
            if tgt is None:
                break
            if pa_ok and i == 0:
                self.put_aside = False
                pa_ok = False
                self.put_aside_on(tgt)
            else:
                self.joined_hands(tgt, adv)
            if not tgt.up and self.attack_distractor == tgt.name:
                self.attack_distractor = None
        self.attack_distractor = None
        self.interferers = set()

    # ------------------------------------------------------------------ loop
    def run(self, max_rounds=20):
        rng, ctx = self.rng, self.ctx
        inits = {}
        for p in self.pcs:
            inits[p.name] = d20(rng, 1 if p.init_adv else 0) + p.init + rng.random() / 10
        self.wept_init = d20(rng) + 7 + rng.random() / 10
        self.att_init = d20(rng) + 3 + rng.random() / 10
        any_drop = False
        all_down = False
        while ctx.round < max_rounds and self.result is None:
            ctx.round += 1
            for p in self.pcs:
                p._reaction = True
            crowd_start_of_round(self.pcs, ctx)
            self.second_turn = False
            seq = [(inits[p.name], "pc", p) for p in self.pcs]
            seq.append((self.wept_init, "wept", None))
            seq.append((self.att_init, "att", 1))
            seq.append((self.att_init - 10, "att", 2))
            seq.sort(key=lambda x: -x[0])
            for i, (_, kind, who) in enumerate(seq):
                if self.result is not None:
                    break
                rest = seq[i + 1:]
                self._rest_kinds = [kd for _, kd, w in rest
                                    if kd != "att" or w == 1 or self.second_turn]
                if kind == "pc":
                    remaining = [w for _, kd, w in rest if kd == "pc"]
                    self.pc_turn(who, remaining)
                elif kind == "wept":
                    self.wept_turn()
                elif who == 1:
                    self.att_turn(1)
                elif self.second_turn:
                    self.att_turn(2)
                if any(p.down for p in self.pcs):
                    any_drop = True
                if all(p.down for p in self.pcs):
                    all_down = True
                    self.result = "all_down"
        if self.result is None:
            self.result = "timeout"
        return dict(result=self.result, any_drop=any_drop, all_down=all_down,
                    rounds=ctx.round, delay_bought=self.delay_bought,
                    drops=ctx.drops)


def run_s14(pcs, rng, policy="engaged", four=None, moves=None, wept_delay=1):
    """Fight S14 with existing PCs (used by chain.py). Returns the result dict."""
    if four is None:
        four = len(pcs) >= 4
    for p in pcs:
        p.reset_fight()
    return S14(pcs, rng, policy, four, moves, wept_delay).run()


def simulate(party="C1", policy="engaged", n=4000, seed=1, clock="book", attrited=False):
    """Run n S14 fights. clock: "book" (6 moves at 3P, 5 at 4P) or "tight" (3 / 2)."""
    rng = random.Random(f"s14|{party}|{policy}|{clock}|{attrited}|{seed}")
    four = party == "4P"
    moves = None if clock == "book" else (2 if four else 3)
    tot = dict(win=0, focus=0, hp=0, drop=0, alldown=0, rounds=0, delay=0)
    for _ in range(n):
        pcs = make_party(party, attrited, rng)
        r = run_s14(pcs, rng, policy, four, moves)
        tot["focus"] += r["result"] == "focus"
        tot["hp"] += r["result"] == "hp"
        tot["drop"] += r["any_drop"]
        tot["alldown"] += r["all_down"]
        tot["rounds"] += r["rounds"]
        tot["delay"] += r["delay_bought"]
    win = (tot["focus"] + tot["hp"]) / n
    return dict(runs=n, party=party, policy=policy, clock=clock, attrited=attrited,
                win=win, win_by_focus=tot["focus"] / n, win_by_hp=tot["hp"] / n,
                any_drop=tot["drop"] / n, all_down=tot["alldown"] / n,
                mean_rounds=tot["rounds"] / n, delay_bought=tot["delay"] / n)


def _fmt(r):
    return (f"{r['party']:<3} {r['policy']:<8} win {100*r['win']:5.1f}% "
            f"(focus {100*r['win_by_focus']:4.1f} / hp {100*r['win_by_hp']:4.1f})  "
            f"drop {100*r['any_drop']:5.1f}%  all-down {100*r['all_down']:4.1f}%  "
            f"rounds {r['mean_rounds']:.1f}  delay {r['delay_bought']:.2f}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="S14 the Attendant, current rules")
    ap.add_argument("--party", default="C1", choices=sorted(PARTIES))
    ap.add_argument("--policy", default="engaged", choices=POLICIES)
    ap.add_argument("--clock", default="book", choices=["book", "tight"])
    ap.add_argument("--attrited", action="store_true")
    ap.add_argument("--all", action="store_true", help="every party x every policy")
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args(argv)
    print(f"s14.py seed={a.seed} n={a.n} clock={a.clock} attrited={a.attrited}")
    if a.all:
        for p in ("4P", "C1", "C2", "C3", "C4", "C5"):
            for pol in POLICIES:
                print(_fmt(simulate(p, pol, a.n, a.seed, a.clock, a.attrited)))
    else:
        print(_fmt(simulate(a.party, a.policy, a.n, a.seed, a.clock, a.attrited)))


if __name__ == "__main__":
    main()
