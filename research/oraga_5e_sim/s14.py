"""s14.py: card S14, the Attendant, Oraga Night 5e (three-player pass).

Rebuilt for TASKS T3.1 from docs/audit_oraga_5e_3p/TUNING_3P.md §2 ("Method");
the original scratchpad script was lost. Extended for T5.8 with the WP5 rules
(DESIGN §3.1, §4; TP5, TP6, TP30). Every new rule is a switch on `Rules`:
`OLD` (all off) reproduces the T3.1 baseline draw for draw, `NEW` (all on) is
the WP5 text. Sources: conversions/dnd5e/oraga_night/10_Bestiary.md "The
Attendant", 09_The_Snakes.md card S14, 05_The_Longest_Night.md "Midnight Rules".

Modelled under OLD (the rules as printed before WP5):
- Idle / Focused (focus checked at the start of each of its turns: Focused if the
  Wept has no Delay); Two Turns while Focused, the second at initiative - 10;
  the three-character line (178 HP; second Focused turn is a single Joined
  Hands); the four-player block (229 HP, full Multiattack on both turns).
- Rusty (Idle: one Joined Hands at Disadvantage; Put Aside only if Bloodied or its
  focus has been broken twice); Literal Orders (it attacks only a PC who attacked
  it or failed a trick on it since its last turn; in round 1 the whole party
  counts, because the card fires on their interference).
- Put Aside's recharge: the T3.1 script never rolled it (the roll sat after a
  `return`), so under OLD Put Aside is never used. `put_aside_recharge` fixes it.
- Clears the Way (once a round, free, at the first turn it keeps, after the focus
  check, if no non-furniture PC is within 5 ft).
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

WP5 switches (`Rules`, all on in NEW):
- lethal:        TP5. Idle, a PC it drops is set aside, Stable. Focused, ordinary
                 dying rules (death saves, massive damage). It finishes only a
                 PC that interfered since its last turn (TP57: one level; the
                 legacy `dial` switch, see LEGACY_DIALS, reproduces WP5's other
                 two settings). Allies stabilise
                 (Spare the Dying, Medicine DC 10) or rouse (an action, 1 HP).
                 Damage to a downed PC follows T5.3: a death-save failure (two
                 on a crit) that ends Stable.
- clears_action: Clears the Way costs the turn's action, at its start, no adjacency
                 test. Idle: it clears when nobody struck it since its last turn.
                 Focused: it attacks on its first turn and clears on its second; with
                 no Delay in the scene to clear, the second turn attacks as before
                 (TPN-8a). A lost turn clears nothing.
- solo_line:     one PC: the Focused second turn makes no attack.
- help:          Help applies to a distraction (the helper spends its action; the
                 trickster rolls with Advantage).
- dc18:          the Focused distraction DC is 18.
- idle_free:     a trick tried while it is Idle is not spent.
- nat20_idle:    a natural 20 while it is Idle costs it its next turn (TPN-8c).
- orders_window: Literal Orders counts interference since the start of its
                 previous round (not since the end of its last turn).
- tie:           the Wept acts first on an Initiative tie with the Attendant.
- cap3:          the Wept loses at most three turns in the scene to Delay; later
                 points are spent and she moves anyway.
- spells_roll:   smart policy's Delay: a trick is DC 13, DC 15 the second time,
                 never a third; a spell uses its roll (Fire Bolt +6 against AC 18,
                 Sacred Flame against Dex +3, Vicious Mockery against Wis +7), each
                 spell once.
- tp30_tricks:   TP30: the cup is cut; its trick is posing as, or announcing, the
                 master it awaits (Deception or Performance).
- put_aside_recharge: the model fix above.

Not modelled: the Wept's strikes (the engaged party keeps out of her reach), so
the Uninvited's own threat rule never bites inside S14; control spells (T5.7's
note: Sleep fails, Hold Person can't target it); tricks while Idle (no policy
tries one; `idle_free` and `nat20_idle` are covered by unit tests).

Policies (TUNING §2): slug, engaged, naive, smart. See README.md.

Usage:
    python s14.py --party C1 --policy engaged --n 4000 --seed 1
    python s14.py --all --n 4000 --seed 1                  # the T3.1 table (OLD)
    python s14.py --all --n 4000 --seed 1 --rules new
    python s14.py --wp5 --n 4000 --seed 1                  # the T5.9 tables
Pure standard library; deterministic for a given --seed.
"""
import argparse
import random
from dataclasses import dataclass, fields, replace

from skirm import (PARTIES, PC, Ctx, Enemy, crowd_start_of_round, d20, damage_pc,
                   death_save, heal_pc, make_party, pc_defend, pc_offence, roll,
                   second_wind, try_bonus_heal)

POLICIES = ("engaged", "naive", "smart", "slug")
# TP57 (2026-10-25): one difficulty level, the old "sharp" setting. The dial argument stays
# only so that the WP5 runs (T5.9) reproduce draw for draw: "sharp" is the default and the
# rules as printed; "gentle" and "merciless" are LEGACY switches for those old tables.
LEGACY_DIALS = ("gentle", "sharp", "merciless")
DIALS = LEGACY_DIALS
PARTIES = PARTIES  # re-export: C1..C5 and 4P
# T5.10's adjusting lines: five characters (all five pregens). "Four at 3rd level"
# is approximated by simulate(level3=True): 80% HP and one fewer 2nd-level slot.
EXTRA_PARTIES = {"5P": ["Dassa", "Ilesse", "Serane", "Andra", "Pello"],
                 "4S": ["Dassa", "Pello", "Andra", "Ilesse"]}   # the four best at blows


def make_s14_party(code, attrited, rng, solo=None, level3=False):
    if code in EXTRA_PARTIES and not solo:
        pcs = [PC(n, attrited, rng) for n in EXTRA_PARTIES[code]]
    else:
        pcs = make_party(code, attrited, rng, solo=solo)
    if level3:
        for p in pcs:
            p.max_hp = p.hp = int(round(p.max_hp * 0.8))
            if p.slots.get(2, 0) > 0:
                p.slots[2] -= 1
    return pcs


@dataclass(frozen=True)
class Rules:
    lethal: bool = False
    clears_action: bool = False
    solo_line: bool = False
    help: bool = False
    dc18: bool = False
    idle_free: bool = False
    nat20_idle: bool = False
    orders_window: bool = False
    tie: bool = False
    cap3: bool = False
    spells_roll: bool = False
    tp30_tricks: bool = False
    put_aside_recharge: bool = False


OLD = Rules()
NEW = Rules(**{f.name: True for f in fields(Rules)})
SWITCHES = tuple(f.name for f in fields(Rules))

# TP30: the cup trick becomes posing as, or announcing, the awaited master
# (Deception or Performance). Pello Deception +2; Ilesse Charisma +2 (no
# Deception or Performance); Dassa's cloak was already Charisma +0.
TP30_SWAP = {
    ("Pello", "lift its cup"): ("announce its master at a doorway", 2, True, False),
    ("Ilesse", "a cup offered for its master"): ("'your master is here'", 2, True, False),
}

# smart policy, spells_roll: (name, kind, bonus) against the Wept (AC 18;
# Dex save +3, Wis save +7; spell save DC 14). "attack": +bonus vs AC 18.
ROOM_SPELLS = {
    "Andra": [("Fire Bolt", "attack", 6)],
    "Ilesse": [("Sacred Flame", "save", 3)],
    "Serane": [("Vicious Mockery", "save", 7)],
}


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
    def __init__(self, pcs, rng, policy, four=False, moves=None, wept_delay=1,
                 rules=OLD, dial="sharp", hp=None, dc=None):
        self.pcs = pcs
        self.dc_override = dc
        self.rng = rng
        self.policy = policy
        self.four = four
        self.R = rules
        self.dial = dial
        self.ctx = Ctx(rng, lethal=False)
        # slugging means everyone hits it, the cleric's slots included
        self.ctx.ilesse_attack = policy == "slug"
        if hp is None:
            hp = 229 if four else 178
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
        # WP5 bookkeeping (unused under OLD)
        self.interf_round = {p.name: 0 for p in pcs}   # round of last interference
        self.interf_clock = {p.name: 0 for p in pcs}   # clock of last interference
        self.att_clock = 0                              # clock at the end of its last turn
        self.helped = None                              # (pc name, round) with Help
        self.wept_lost = 0                              # turns lost to Delay (cap3)
        self.room_uses = {}
        self.clears = 0
        self.att_turns = 0
        self.idle_turns = 0
        self.set_aside = set()                          # dropped while Idle
        self.finish_attacks = 0
        if rules.tp30_tricks:
            for p in pcs:
                p.tricks = [TP30_SWAP.get((p.name, t[0]), t) for t in p.tricks]
        if policy == "smart":
            melee = [p for p in pcs if p.melee]
            self.guard = (max(melee, key=lambda p: p.max_hp) if melee
                          else max(pcs, key=lambda p: p.max_hp)).name

    # ------------------------------------------------------------------ tricks
    def focused_dc(self):
        if self.dc_override is not None:
            return self.dc_override
        return 18 if self.R.dc18 else 19

    def trick_options(self, pc):
        """[(p, trick, bonus, adv)] for this PC at the current DC, best first."""
        dc = self.focused_dc() if self.focused else 13
        helped = self.R.help and self.helped == (pc.name, self.ctx.round)
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
            if helped:
                a += 1
            out.append((p_success(bonus, max(-1, min(1, a)), dc), t, bonus, a))
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
        if not (self.R.idle_free and not self.focused):
            self.trick_uses[(pc.name, name)] = self.trick_uses.get((pc.name, name), 0) + 1
        self.tried_round = self.ctx.round
        first_try = not self.first_try_done
        self.first_try_done = True
        dc = self.focused_dc() if self.focused else 13
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
            if self.R.orders_window:
                self.interf_round[pc.name] = -9
            if self.R.nat20_idle and nat == 20:
                self.lost_turn = True
        else:
            if self.focused:
                self.attack_distractor = pc.name
                self.interferers.add(pc.name)
                self.last_hit_by[pc.name] = self.clock
                self._interfere(pc)
        return True

    def _interfere(self, pc):
        self.interf_round[pc.name] = self.ctx.round
        self.interf_clock[pc.name] = self.clock

    def room_trick(self, pc):
        """Smart policy: buy Delay on the Wept (DC 13; distinct tricks)."""
        if not self.R.spells_roll:
            name, skill, _, adv = max(pc.tricks, key=lambda t: t[1] + (3 if t[3] else 0))
            if d20(self.rng, 1 if adv else 0) + skill >= 13:
                self.wept_delay += 1
                self.delay_bought += 1
            return
        # DC 13, DC 15 the second time, never a third; each spell once.
        opts = []
        for name, skill, _, adv in pc.tricks:
            u = self.room_uses.get((pc.name, name), 0)
            if u < 2:
                dc = 13 if u == 0 else 15
                opts.append((p_success(skill, 1 if adv else 0, dc), "trick", name, skill, adv, dc))
        for name, kind, b in ROOM_SPELLS.get(pc.name, []):
            if self.room_uses.get((pc.name, name), 0) == 0:
                p = p_success(b, 0, 18) if kind == "attack" else 1 - p_success(b, 0, 14)
                opts.append((p, kind, name, b, False, 0))
        if not opts:
            return
        p, kind, name, b, adv, dc = max(opts, key=lambda o: o[0])
        self.room_uses[(pc.name, name)] = self.room_uses.get((pc.name, name), 0) + 1
        if kind == "trick":
            ok = d20(self.rng, 1 if adv else 0) + b >= dc
        elif kind == "attack":
            nat = d20(self.rng)
            ok = nat == 20 or (nat != 1 and nat + b >= 18)
        else:
            ok = d20(self.rng) + b < 14
        if ok:
            self.wept_delay += 1
            self.delay_bought += 1

    # ------------------------------------------------------------------ turns
    def pc_turn(self, pc, remaining):
        R = self.R
        if R.lethal and pc.down and not pc.dead and not pc.stable:
            death_save(pc, self.ctx)
            return
        if not pc.up:
            return
        self.clock += 1
        ctx = self.ctx
        pc._bonus_used = False
        if pc.name == "Dassa":
            second_wind(pc, ctx)
        try_bonus_heal(pc, self.pcs, ctx)
        if R.lethal and pc.up:
            # healed allies are no longer set aside
            for q in self.pcs:
                if q.up:
                    self.set_aside.discard(q.name)
        pol = self.policy
        if pol != "slug" and self.focused and self.tried_round != ctx.round:
            mine = self.best_p(pc)
            live_later = [q for q in remaining if q.up]
            later = [self.best_p(q) for q in live_later]
            if mine > 0 and mine >= max(later, default=0.0):
                self.do_trick(pc)
                return
            if R.help and pol != "naive" and live_later and \
                    (self.helped is None or self.helped[1] != ctx.round):
                best = max(live_later, key=lambda q: self.best_p(q))
                if self.best_p(best) > 0:
                    self.helped = (best.name, ctx.round)
                    return
        if R.lethal and self.support(pc):
            return
        if pol == "smart" and pc.name != self.guard and self.wept_delay == 0 \
                and self.delay_is_free(remaining):
            self.room_trick(pc)
            return
        dealt = pc_offence(pc, self.att, ctx, first_turn=(ctx.round == 1))
        self.interferers.add(pc.name)
        self.furniture.discard(pc.name)
        self.last_hit_by[pc.name] = self.clock
        self._interfere(pc)
        if self.att.hp <= 0 and self.result is None:
            self.result = "hp"
        return dealt

    def support(self, pc):
        """Lethal mode: stabilise a dying ally (Ilesse: Spare the Dying; anyone not
        on the front line: Medicine DC 10), or rouse a Stable one the crowd will
        not reach (an action, 1 HP). Returns True if the action was used."""
        dying = [q for q in self.pcs if q.down and not q.dead and not q.stable]
        if dying:
            if pc.name == "Ilesse":
                dying[0].stable = True
                dying[0].stable_round = self.ctx.round
                return True
            if pc.role not in ("front", "striker"):
                if d20(self.rng) + pc.medicine >= 10:
                    dying[0].stable = True
                    dying[0].stable_round = self.ctx.round
                return True
        stable = [q for q in self.pcs if q.down and not q.dead and q.stable
                  and not self.crowd_covers(q)]
        if stable and pc.role not in ("front", "striker"):
            heal_pc(stable[0], 1)
            self.set_aside.discard(stable[0].name)
            return True
        return False

    def crowd_covers(self, pc):
        if self.dial == "gentle":
            return True
        if self.dial == "sharp":
            return pc.name in self.set_aside
        return False

    def crowd(self):
        if not self.R.lethal:
            crowd_start_of_round(self.pcs, self.ctx)
            return
        for pc in self.pcs:
            if pc.down and not pc.dead and self.crowd_covers(pc):
                if pc.stable_round is None:          # legacy dial: a dying PC is dragged clear
                    pc.stable_round = pc.down_round
                if self.ctx.round >= pc.stable_round + 2:
                    pc.stable = True
                    heal_pc(pc, 1)
                    self.set_aside.discard(pc.name)

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
            if self.R.cap3:
                if self.wept_lost < 3:
                    self.wept_lost += 1
                    return
            else:
                return
        self.wept_moves -= 1
        if self.wept_moves <= 0 and self.result is None:
            self.result = "errand"

    def valid_targets(self, include_down=False, k=1):
        if self.R.orders_window:
            r = self.ctx.round
            vt = [p for p in self.pcs if p.up and self.interf_round[p.name] >= r - 1
                  and p.name not in self.furniture]
        else:
            vt = [p for p in self.pcs if p.up and p.name in self.interferers
                  and p.name not in self.furniture]
        if include_down:
            vt += self.finishable()
        return vt

    def finishable(self):
        """Downed PCs a Focused Attendant may attack (lethal mode, by dial)."""
        if not (self.R.lethal and self.focused) or self.dial == "gentle":
            return []
        out = []
        for p in self.pcs:
            if not p.down or p.dead or p.name in self.furniture:
                continue
            if self.dial == "sharp":
                # interrupted since its last turn
                if self.interf_clock[p.name] > self.att_clock:
                    out.append(p)
            else:
                # legacy dial: any interruption still inside its orders' window
                if self.R.orders_window:
                    if self.interf_round[p.name] >= self.ctx.round - 1:
                        out.append(p)
                elif p.name in self.interferers:
                    out.append(p)
        return out

    def choose_target(self):
        vt = self.valid_targets(include_down=self.R.lethal)
        if not vt:
            return None
        if self.attack_distractor:
            for p in vt:
                if p.name == self.attack_distractor:
                    return p
        return max(vt, key=lambda p: self.last_hit_by.get(p.name, -1))

    def hit_pc(self, pc, dmg):
        """Damage from the Attendant to a PC under the current rules."""
        if not self.R.lethal:
            damage_pc(pc, dmg, self.ctx, nonlethal=True)   # Down, Not Out
            return
        if pc.down:
            # T5.3: the legacy gentle dial never damages a set-aside creature; otherwise,
            # the rules as written (a failure, two on a crit; ends Stable)
            if self.dial == "gentle" or pc.dead:
                return
            self.finish_attacks += 1
            if dmg >= pc.max_hp:
                pc.dead = True
                self.ctx.deaths += 1
                return
            pc.stable = False
            pc.stable_round = None
            self.set_aside.discard(pc.name)
            pc.ds_fail += 2                     # within 5 ft of an Unconscious target: a crit
            if pc.ds_fail >= 3:
                pc.dead = True
                self.ctx.deaths += 1
            return
        self.ctx.lethal = True
        damage_pc(pc, dmg, self.ctx, nonlethal=not self.focused)
        self.ctx.lethal = False
        if pc.down and not pc.dead:
            if not self.focused:
                self.set_aside.add(pc.name)
            elif self.dial == "gentle":
                # legacy dial: the crowd rule covers everyone; dragged clear, Stable
                pc.stable = True
                pc.stable_round = self.ctx.round

    def joined_hands(self, pc, adv=0):
        att, ctx = self.att, self.ctx
        if pc.down:
            adv += 1                                       # Unconscious: Advantage
        if att.disadv_next:
            adv -= 1
            att.disadv_next = False
        nat = d20(self.rng, max(-1, min(1, adv)))
        if nat == 1:
            return
        if not pc_defend(pc, nat + 7, nat, self.pcs, ctx):
            return
        crit = nat == 20 or pc.down
        dmg = roll(self.rng, 2 if crit else 1, 10) + 4
        pc.adjacent = False                                # pushed 5 ft
        self.hit_pc(pc, dmg)

    def put_aside_on(self, primary):
        caught = [primary] + [p for p in self.valid_targets()
                              if p is not primary and p.adjacent]
        for p in caught:
            if p.down:
                continue
            dmg = roll(self.rng, 2, 8)
            if d20(self.rng) + p.saves["str"] >= 15:
                dmg //= 2
            else:
                p.adjacent = False
            self.hit_pc(p, dmg)

    def att_turn(self, k):
        ctx, R = self.ctx, self.R
        # A broken focus lasts until the start of its next turn, so the focus
        # check happens even on a turn it then loses (success by 5).
        self.focused = self.wept_delay == 0
        if k == 1:
            self.second_turn = self.focused
            if R.put_aside_recharge and not self.put_aside \
                    and self.rng.randint(1, 6) >= (5 if self.focused else 6):
                self.put_aside = True
        self.att_turns += 1
        self.idle_turns += not self.focused
        if self.lost_turn:
            self.lost_turn = False
            self.cleared_round = ctx.round      # a lost turn also loses Clears the Way
            self.interferers = set()
            self.attack_distractor = None
            self.att_clock = self.clock
            return
        if R.clears_action:
            struck = any(self.last_hit_by.get(p.name, -1) > self.att_clock for p in self.pcs)
            if self.wept_delay > 0 and (self.focused and k == 2
                                        or not self.focused and not struck):
                self.wept_delay -= 1
                self.clears += 1
                self._end_turn()
                return
        elif self.cleared_round != ctx.round and self.wept_delay > 0:
            blockers = [p for p in self.pcs if p.up and p.adjacent
                        and p.name not in self.furniture]
            if not blockers:
                self.wept_delay -= 1
                self.cleared_round = ctx.round
        # attacks
        if self.focused:
            if k == 2 and R.solo_line and len(self.pcs) == 1:
                n_attacks = 0
            else:
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
            if pa_ok and i == 0 and tgt.up:
                self.put_aside = False
                pa_ok = False
                self.put_aside_on(tgt)
            else:
                self.joined_hands(tgt, adv)
            if not tgt.up and self.attack_distractor == tgt.name:
                self.attack_distractor = None
        self._end_turn()

    def _end_turn(self):
        self.attack_distractor = None
        self.interferers = set()
        self.att_clock = self.clock

    # ------------------------------------------------------------------ loop
    def run(self, max_rounds=20):
        rng, ctx = self.rng, self.ctx
        inits = {}
        for p in self.pcs:
            inits[p.name] = d20(rng, 1 if p.init_adv else 0) + p.init + rng.random() / 10
        self.wept_init = d20(rng) + 7 + rng.random() / 10
        self.att_init = d20(rng) + 3 + rng.random() / 10
        if self.R.tie and int(self.wept_init) == int(self.att_init):
            self.wept_init = int(self.wept_init) + 0.0999      # the Wept acts first
            self.att_init = int(self.att_init) + 0.0
        any_drop = False
        all_down = False
        while ctx.round < max_rounds and self.result is None:
            ctx.round += 1
            for p in self.pcs:
                p._reaction = True
            self.crowd()
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
        if self.R.lethal:
            self.aftermath()
        idle_frac = self.idle_turns / self.att_turns if self.att_turns else 0.0
        return dict(result=self.result, any_drop=any_drop, all_down=all_down,
                    rounds=ctx.round, delay_bought=self.delay_bought,
                    drops=ctx.drops, deaths=ctx.deaths,
                    pc_death=any(p.dead for p in self.pcs),
                    clears=self.clears, idle_frac=idle_frac,
                    finish_attacks=self.finish_attacks)

    def aftermath(self):
        """After the card: dying PCs. Standing allies stabilise them (a Healing
        Word, Spare the Dying, or Medicine DC 10 once a round); the crowd reaches
        whom the dial says; with the whole party down, the dying roll it out."""
        ctx = self.ctx
        for _ in range(12):
            dying = [p for p in self.pcs if p.down and not p.dead and not p.stable]
            if not dying:
                break
            ctx.round += 1
            for p in dying:
                if self.crowd_covers(p):
                    p.stable = True
                    continue
                death_save(p, ctx)
            helpers = [p for p in self.pcs if p.up]
            for h in helpers:
                dying = [p for p in self.pcs if p.down and not p.dead and not p.stable]
                if not dying:
                    break
                if h.healing_word and h.slots.get(1, 0) > 0:
                    h.slots[1] -= 1
                    heal_pc(dying[0], roll(self.rng, 2, 4) + 4)
                elif h.name == "Ilesse" or d20(self.rng) + h.medicine >= 10:
                    dying[0].stable = True


def run_s14(pcs, rng, policy="engaged", four=None, moves=None, wept_delay=1,
            rules=OLD, dial="sharp", hp=None, dc=None):
    """Fight S14 with existing PCs (used by chain.py). Returns the result dict."""
    if four is None:
        four = len(pcs) >= 4
    for p in pcs:
        p.reset_fight()
    return S14(pcs, rng, policy, four, moves, wept_delay, rules, dial, hp, dc).run()


def _rules_tag(rules):
    if rules == OLD:
        return ""
    if rules == NEW:
        return "|new"
    return "|" + ",".join(n for n in SWITCHES if getattr(rules, n))


def simulate(party="C1", policy="engaged", n=4000, seed=1, clock="book", attrited=False,
             rules=OLD, dial="sharp", hp=None, moves=None, solo=None, dc=None,
             level3=False):
    """Run n S14 fights. clock: "book" (6 moves at 3P, 5 at 4P) or "tight" (3 / 2).
    rules: OLD (as printed before WP5), NEW (WP5), or any Rules(...). dial matters
    only with rules.lethal. hp: override the block's HP. moves: override the clock.
    solo: a pregen name for a one-PC run (the party code is ignored)."""
    # The seed string is unchanged under OLD with no overrides, so T3.1's runs
    # reproduce draw for draw.
    tag = _rules_tag(rules)
    if rules.lethal:
        tag += "|" + dial
    if hp is not None:
        tag += f"|hp{hp}"
    if moves is not None:
        tag += f"|m{moves}"
    if solo:
        tag += f"|solo{solo}"
    if dc is not None:
        tag += f"|dc{dc}"
    if level3:
        tag += "|l3"
    rng = random.Random(f"s14|{party}|{policy}|{clock}|{attrited}|{seed}{tag}")
    four = party in ("4P", "5P", "4S") and not solo
    if moves is None:
        moves = None if clock == "book" else (2 if four else 3)
    tot = dict(win=0, focus=0, hp=0, drop=0, alldown=0, rounds=0, delay=0, death=0,
               errand=0, timeout=0, clears=0, idle_grind=0, idle=0.0)
    for _ in range(n):
        pcs = make_s14_party(party, attrited, rng, solo, level3)
        r = run_s14(pcs, rng, policy, four, moves, rules=rules, dial=dial, hp=hp, dc=dc)
        tot["focus"] += r["result"] == "focus"
        tot["hp"] += r["result"] == "hp"
        tot["errand"] += r["result"] == "errand"
        tot["timeout"] += r["result"] == "timeout"
        tot["drop"] += r["any_drop"]
        tot["alldown"] += r["all_down"]
        tot["rounds"] += r["rounds"]
        tot["delay"] += r["delay_bought"]
        tot["death"] += r.get("pc_death", False)
        tot["clears"] += r.get("clears", 0)
        tot["idle"] += r.get("idle_frac", 0.0)
        tot["idle_grind"] += r["result"] == "hp" and r.get("idle_frac", 0.0) >= 0.5
    win = (tot["focus"] + tot["hp"]) / n
    out = dict(runs=n, party=party, policy=policy, clock=clock, attrited=attrited,
               win=win, win_by_focus=tot["focus"] / n, win_by_hp=tot["hp"] / n,
               any_drop=tot["drop"] / n, all_down=tot["alldown"] / n,
               mean_rounds=tot["rounds"] / n, delay_bought=tot["delay"] / n)
    if rules != OLD or hp is not None or moves is not None or solo or dc or level3:
        out.update(pc_death=tot["death"] / n, errand=tot["errand"] / n,
                   timeout=tot["timeout"] / n, clears=tot["clears"] / n,
                   idle_frac=tot["idle"] / n, idle_grind=tot["idle_grind"] / n,
                   dial=dial if rules.lethal else "-", hp=hp)
    return out


def _fmt(r):
    s = (f"{r['party']:<3} {r['policy']:<8} win {100*r['win']:5.1f}% "
         f"(focus {100*r['win_by_focus']:4.1f} / hp {100*r['win_by_hp']:4.1f})  "
         f"drop {100*r['any_drop']:5.1f}%  all-down {100*r['all_down']:4.1f}%  "
         f"rounds {r['mean_rounds']:.1f}  delay {r['delay_bought']:.2f}")
    if "pc_death" in r:
        s += (f"  death {100*r['pc_death']:4.1f}%  errand {100*r['errand']:4.1f}%  "
              f"idle-grind {100*r['idle_grind']:4.1f}%")
    return s


def _parse_rules(name):
    if name == "old":
        return OLD
    if name == "new":
        return NEW
    on = [s for s in name.split(",") if s]
    bad = [s for s in on if s not in SWITCHES]
    if bad:
        raise SystemExit(f"unknown switch(es): {bad}; known: {SWITCHES}")
    return replace(OLD, **{s: True for s in on})


def wp5_tables(n, seed):
    """T5.9 (legacy, pre-TP57): current against WP5, every party, all three old dial settings."""
    for pol in ("engaged", "slug", "naive", "smart"):
        print(f"\n## {pol}: current (old rules) -> WP5 at gentle / sharp / merciless")
        for p in ("C1", "C2", "C3", "C4", "C5", "4P"):
            print(_fmt(simulate(p, pol, n, seed)))
            for d in DIALS:
                print("   " + d[:5], _fmt(simulate(p, pol, n, seed, rules=NEW, dial=d)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="S14 the Attendant")
    ap.add_argument("--party", default="C1", choices=sorted(PARTIES) + sorted(EXTRA_PARTIES))
    ap.add_argument("--policy", default="engaged", choices=POLICIES)
    ap.add_argument("--clock", default="book", choices=["book", "tight"])
    ap.add_argument("--attrited", action="store_true")
    ap.add_argument("--rules", default="old",
                    help="old, new, or a comma list of switches: " + ",".join(SWITCHES))
    ap.add_argument("--legacy-dial", dest="dial", default="sharp", choices=LEGACY_DIALS,
                    help="TP57: one level (sharp). The others only reproduce the WP5 runs")
    ap.add_argument("--hp", type=int, default=None)
    ap.add_argument("--moves", type=int, default=None)
    ap.add_argument("--solo", default=None)
    ap.add_argument("--dc", type=int, default=None, help="Focused distraction DC override")
    ap.add_argument("--level3", action="store_true", help="approximate 3rd-level pregens")
    ap.add_argument("--all", action="store_true", help="every party x every policy")
    ap.add_argument("--wp5", action="store_true", help="the T5.9 current-vs-WP5 tables")
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args(argv)
    rules = _parse_rules(a.rules)
    print(f"s14.py seed={a.seed} n={a.n} clock={a.clock} attrited={a.attrited} "
          f"rules={a.rules} dial={a.dial}")
    if a.wp5:
        wp5_tables(a.n, a.seed)
    elif a.all:
        for p in ("4P", "C1", "C2", "C3", "C4", "C5"):
            for pol in POLICIES:
                print(_fmt(simulate(p, pol, a.n, a.seed, a.clock, a.attrited,
                                    rules, a.dial, a.hp, a.moves)))
    else:
        print(_fmt(simulate(a.party, a.policy, a.n, a.seed, a.clock, a.attrited,
                            rules, a.dial, a.hp, a.moves, a.solo, a.dc, a.level3)))


if __name__ == "__main__":
    main()
