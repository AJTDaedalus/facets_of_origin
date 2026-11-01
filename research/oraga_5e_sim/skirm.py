"""skirm.py: generic snake-card skirmish engine, Oraga Night 5e (three-player pass).

Rebuilt for TASKS T3.1 from docs/audit_oraga_5e_3p/TUNING_3P.md §2 ("Method"); the
original scratchpad script was lost. A roster from chapter IX's cards
(conversions/dnd5e/oraga_night/09_The_Snakes.md) fights three (or four, or one)
of the chapter XI pregens until the card's morale trigger fires, everyone on one
side is down, or 30 rounds pass. Stat numbers are the module's chapter X blocks.
Rules base: D&D 5e SRD 5.2.1.

This file also holds what s14.py and chain.py share: dice, the five pregens, the
party codes, the PC offence and healing routines, damage, dropping, death saves
and the crowd rule.

Usage:
    python skirm.py --card S8 --party C1 --n 4000 --seed 1
    python skirm.py --card S2 --solo Dassa --n 4000 --seed 1
    python skirm.py --all --n 2000 --seed 1        # every card x C1..C5 (+4P)

Pure standard library; deterministic for a given --seed.
"""
import argparse
import random
from dataclasses import dataclass

# ----------------------------------------------------------------------------- dice


def roll(rng, n, s):
    return sum(rng.randint(1, s) for _ in range(n))


def d20(rng, adv=0):
    """adv > 0 Advantage, adv < 0 Disadvantage, 0 straight."""
    a = rng.randint(1, 20)
    if adv == 0:
        return a
    b = rng.randint(1, 20)
    return max(a, b) if adv > 0 else min(a, b)


# Policy switches (module-level so s14.py and chain.py share them).
# ilesse_attack_slots: Ilesse spends slots on Spiritual Weapon and Guiding Bolt.
#   Off by default: she keeps every slot for healing and attacks with Sacred
#   Flame. TUNING_3P §5 describes the healer as spending "almost everything on
#   healing (so no Spiritual Weapon)", and its C1 numbers read as a low-damage
#   party ("its weakness is damage output, so grindy fights run long").
OPTIONS = dict(ilesse_attack_slots=False, targeting="sticky")

# ------------------------------------------------------------------------- pregens
# Chapter XI, 11_Pregenerated_Characters.md. "tricks" are the distinct S14
# distraction tricks each pregen can plausibly play: (name, skill bonus, uses one
# of the Attendant's three habits, has Advantage). Advantage: the Orthaen gift on
# a crystal trick; Dassa's Remarkable Athlete on Athletics for a thrown light
# (TUNING §2 caveats: "a generous but rules-legal DM"). One trick per habit a
# pregen can credibly stage, plus arguing its orders; once a PC has used them,
# further tricks are repeats (no bonus, Disadvantage). The skill is the sheet's;
# where none fits, the ability modifier.

PREGENS = {
    "Dassa": dict(
        hd=(10, 3),
        hp=40, ac=16, init=3, init_adv=True, role="front", melee=True,
        saves=dict(str=6, dex=1, con=5, wis=1), medicine=3, athletics=6,
        second_wind=3, action_surge=1, slots={},
        tricks=[("thrown light", 6, True, True),
                ("cloak held out for its master", 0, True, False),
                ("argue its orders", 2, False, False)],
    ),
    "Pello": dict(
        hd=(8, 2),
        hp=31, ac=16, init=4, init_adv=False, role="striker", melee=True,
        saves=dict(str=-1, dex=6, con=2, wis=2), medicine=2, athletics=1, slots={},
        tricks=[("lift its cup", 8, True, False),
                ("something bright flicked past", 8, True, False),
                ("argue its orders", 3, False, False)],
    ),
    "Serane": dict(
        hd=(8, 2),
        hp=31, ac=14, init=4, init_adv=False, role="talker", melee=False,
        saves=dict(str=-1, dex=4, con=2, wis=1), medicine=2, athletics=0,
        slots={1: 4, 2: 3}, bi=4, healing_word=True,
        tricks=[("a tune that changes", 6, True, False),
                ("a false order from its master", 6, True, False),
                ("argue its orders", 8, False, False),
                ("crystal light from Prestidigitation", 1, True, True)],
    ),
    "Andra": dict(
        hd=(6, 2),
        hp=26, ac=15, init=2, init_adv=False, role="arcane", melee=False,
        saves=dict(str=-1, dex=2, con=2, wis=3), medicine=3, athletics=-1,
        slots={1: 3, 2: 3}, shield=True,
        tricks=[("a working crystal held up", 6, True, True),
                ("an illusion of light", 6, True, False),
                ("argue its orders", 6, False, False)],
    ),
    "Ilesse": dict(
        hd=(8, 2),
        hp=31, ac=14, init=3, init_adv=False, role="healer", melee=False,
        saves=dict(str=-1, dex=1, con=2, wis=6), medicine=6, athletics=-1,
        slots={1: 4, 2: 3}, healing_word=True, channel=2,
        tricks=[("her warding crystal made to glow", 4, True, True),
                ("a cup offered for its master", 4, True, False),
                ("argue its orders", 4, False, False)],
    ),
}

# 2014 conversion (DESIGN_oraga_5e_2014; chapter XI rebuilt by SRD 5.1): the same five
# guests as SRD 5.1 4th-level humans. set_edition("2014") swaps these in, and turns off
# the 2024-only features in pc_offence and healing (Savage Attacker, Sap, Steady Aim,
# Potent Cantrip; Vicious Mockery 1d4, Healing Word 1d4, Cure Wounds 1d8).
PREGENS_2014 = {
    "Dassa": dict(hp=36, ac=17, init=2, init_adv=False,
                  saves=dict(str=6, dex=2, con=4, wis=1), medicine=1, athletics=6,
                  second_wind=1, action_surge=1, hd=(10, 2)),
    "Pello": dict(hp=31, ac=16, init=4, saves=dict(str=-1, dex=6, con=2, wis=2), medicine=2,
                  athletics=-1),
    "Serane": dict(hp=31, ac=14, init=3, saves=dict(str=-1, dex=2, con=2, wis=1), medicine=2),
    "Andra": dict(hp=26, ac=15, init=2, saves=dict(str=-1, dex=2, con=2, wis=3), medicine=1),
    "Ilesse": dict(hp=31, ac=14, init=1, saves=dict(str=-1, dex=1, con=2, wis=6), medicine=6,
                   channel=1),
}
_PREGENS_2024 = {k: dict(v) for k, v in PREGENS.items()}
EDITION = {"name": "2024"}


def set_edition(name):
    """'2024' (the T3.1 model, default) or '2014' (the SRD 5.1 pregens)."""
    PREGENS.clear()
    for k, v in _PREGENS_2024.items():
        PREGENS[k] = dict(v)
        if name == "2014":
            PREGENS[k].update(PREGENS_2014[k])
    EDITION["name"] = name


def is_2014():
    return EDITION["name"] == "2014"


PARTIES = {
    "C1": ["Dassa", "Ilesse", "Serane"],
    "C2": ["Dassa", "Ilesse", "Andra"],
    "C3": ["Dassa", "Pello", "Ilesse"],
    "C4": ["Dassa", "Pello", "Andra"],
    "C5": ["Serane", "Andra", "Pello"],
    "4P": ["Dassa", "Ilesse", "Serane", "Andra"],
}


class PC:
    def __init__(self, name, attrited=False, rng=None):
        d = PREGENS[name]
        self.name = name
        self.max_hp = d["hp"]
        self.hp = d["hp"]
        self.ac = d["ac"]
        self.init = d["init"]
        self.init_adv = d["init_adv"]
        self.role = d["role"]
        self.melee = d["melee"]
        self.saves = d["saves"]
        self.medicine = d["medicine"]
        self.slots = dict(d["slots"])
        self.bi = d.get("bi", 0)
        self.healing_word = d.get("healing_word", False)
        self.shield = d.get("shield", False)
        self.channel = d.get("channel", 0)
        self.second_wind = d.get("second_wind", 0)
        self.action_surge = d.get("action_surge", 0)
        self.tricks = d["tricks"]
        self.hi = True                      # Heroic Inspiration (Resourceful)
        self.hd = d["hd"]                   # (die size, Con modifier); T6.9
        self.hit_dice = 4                   # 4th level
        self.potions = 0                    # WP6: given by the caller when modelled
        if attrited:                        # TUNING Appendix: 70% HP, half slots, HI 50%
            self.hp = int(round(self.max_hp * 0.7))
            self.slots = {k: v // 2 for k, v in self.slots.items()}
            self.bi = self.bi // 2
            self.hi = rng.random() < 0.5
        self.reset_fight()
        self.dead = False
        self.drops = 0

    def reset_fight(self):
        self.down = False
        self.stable = False
        self.ds_succ = 0
        self.ds_fail = 0
        self.down_round = None
        self.stable_round = None
        self.conc_sw = False                # Spiritual Weapon up
        self.adjacent = False
        self.in_fight = True
        self.provoked_by = None
        self.read_marked = False

    @property
    def up(self):
        return not self.down and not self.dead


def make_party(code, attrited=False, rng=None, solo=None):
    names = [solo] if solo else PARTIES[code]
    return [PC(n, attrited, rng) for n in names]


# --------------------------------------------------------------------------- enemies

class Enemy:
    def __init__(self, name, hp, ac, init, attacks, dex_save=1, wis_save=0, con_save=1,
                 parry=False, uncanny=False, sneak=None, paid_extra=False, riposte=False,
                 interpose=False, provocation=False, detain=False, terms=False,
                 arrive=1, leader=False, read=False, command=False, kind=""):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.ac = ac
        self.init = init
        self.attacks = attacks      # list of (to_hit, n, s, bonus)
        self.dex_save = dex_save
        self.wis_save = wis_save
        self.con_save = con_save
        self.parry = parry
        self.uncanny = uncanny
        self.sneak = sneak
        self.paid_extra = paid_extra
        self.riposte = riposte
        self.interpose = interpose
        self.provocation = provocation
        self.detain = detain        # its drops are Stable (detain, nonlethal)
        self.terms = terms          # To the Terms: leaves a PC at 1 HP
        self.arrive = arrive        # first round on the field
        self.leader = leader
        self.read = read
        self.command = command
        self.kind = kind
        self.gone = False           # broke, fled, left
        self.reaction = True
        self.disadv_next = False    # Sap, Vicious Mockery
        self.adv_vs_next = False    # Guiding Bolt
        self.target = None
        self.first_turn_done = False
        self.damaged = False

    @property
    def active(self):
        return self.hp > 0 and not self.gone

    @property
    def bloodied(self):
        return self.hp <= self.max_hp // 2


def E(name, **kw):
    b = dict(BLOCKS[name])
    b.update(kw)
    return Enemy(name, **b)


# Chapter X blocks (10_Bestiary.md). attacks = list of (to-hit, dice n, dice s, bonus).
BLOCKS = {
    "Tavva": dict(hp=44, ac=15, init=5, attacks=[(5, 1, 4, 3)] * 2, dex_save=5, wis_save=2,
                  uncanny=True, sneak=(2, 6), leader=True, kind="tavva"),
    "Gallery Knife": dict(hp=13, ac=13, init=2, attacks=[(4, 1, 4, 2)], dex_save=2),
    "Circle Hired Knife": dict(hp=32, ac=15, init=3, attacks=[(5, 1, 4, 3)] * 2, dex_save=5,
                               wis_save=1, paid_extra=True),
    "Church Warden": dict(hp=33, ac=16, init=1, attacks=[(4, 1, 6, 2)] * 2, wis_save=3,
                          interpose=True, detain=True),
    "Draunel Duelist": dict(hp=27, ac=15, init=3, attacks=[(5, 1, 8, 3)], dex_save=5,
                            riposte=True, provocation=True, kind="duelist"),
    "Boranis Cousin's Blade": dict(hp=22, ac=14, init=1, attacks=[(4, 1, 8, 2)]),
    "Maiven Nolonaire": dict(hp=58, ac=15, init=3, attacks=[(5, 1, 6, 3)] * 3, dex_save=5,
                             wis_save=4, leader=True),
    "Thenya Border Slinger": dict(hp=19, ac=14, init=3, attacks=[(5, 1, 4, 3)], dex_save=3,
                                  wis_save=1),
    "Essar Draunel": dict(hp=58, ac=16, init=3, attacks=[(5, 1, 8, 3)] * 3, dex_save=5,
                          wis_save=3, parry=True, leader=True),
    "Bought Sergeant": dict(hp=52, ac=17, init=2, attacks=[(4, 1, 8, 2)] * 2, dex_save=2,
                            wis_save=1, parry=True, leader=True),
    "Veteran Bought Sergeant": dict(hp=78, ac=17, init=2, attacks=[(5, 1, 8, 3)] * 3,
                                    dex_save=2, wis_save=1, parry=True, leader=True),
    "Bought Blade": dict(hp=22, ac=16, init=1, attacks=[(4, 1, 6, 2)], terms=True),
    "Bought Captain": dict(hp=97, ac=17, init=2, attacks=[(5, 1, 10, 3)] * 2, dex_save=2,
                           wis_save=4, parry=True, read=True, command=True, arrive=3,
                           kind="captain"),
    "Boranis Honor Guard": dict(hp=52, ac=18, init=1, attacks=[(5, 1, 8, 3)] * 2, wis_save=1,
                                detain=True, kind="guard"),
}

# --------------------------------------------------------------------------- cards
# Each card: roster(party_size) -> list of Enemy, plus flags. "lethal": after
# midnight (death saves, crowd rule). "end": morale trigger, see check_end().
# Roster lines are the cards' printed lines (four-player line for 4P, the
# "Three characters" line for three or fewer, as T3.1 asks: the CURRENT rules).


def _r_s2(k):
    return [E("Tavva")] + [E("Gallery Knife") for _ in range(3 if k >= 4 else 2)]


def _r_s3(k, captain=True):
    sgt = E("Veteran Bought Sergeant") if k >= 4 else E("Bought Sergeant")
    r = [sgt] + [E("Bought Blade") for _ in range(4)]
    if captain:
        r.append(E("Bought Captain"))
    return r


def _r_s4(k):
    return [E("Boranis Honor Guard") for _ in range(2)]


def _r_s7(k):
    return [E("Circle Hired Knife") for _ in range(4 if k >= 4 else 3)]


def _r_s8(k, staggered=False):
    """Default: every warden on the line fights from round 1 (TUNING lists S8 as
    "3 wardens"; the lock clock that brings the later ones advances only while
    the wardens work the lock undisturbed, so in a fight its timing is a DM call).
    staggered=True: the third arrives in round 3 and the fourth in round 4."""
    r = [E("Church Warden"), E("Church Warden"),
         E("Church Warden", arrive=3 if staggered else 1)]
    if k >= 4:
        r.append(E("Church Warden", arrive=4 if staggered else 1))
    return r


def _r_s9(k):
    if k >= 4:
        duel = [E("Draunel Duelist", hp=58, ac=16, attacks=[(6, 1, 8, 4)] * 2, leader=True)]
        duel += [E("Draunel Duelist") for _ in range(2)]
        cous = [E("Boranis Cousin's Blade") for _ in range(3)]
    else:
        duel = [E("Draunel Duelist") for _ in range(2)]
        cous = [E("Boranis Cousin's Blade") for _ in range(2)]
    return duel + cous


def _r_s10(k, fix=False):
    m = E("Maiven Nolonaire", arrive=3)
    if fix:
        m.attacks = m.attacks[:2]
        return [m, E("Thenya Border Slinger")]
    return [m] + [E("Thenya Border Slinger") for _ in range(3 if k >= 4 else 2)]


def _r_s13(k):
    r = [E("Essar Draunel"), E("Draunel Duelist")]
    if k >= 4:
        r.insert(1, E("Draunel Duelist", hp=58, ac=16, attacks=[(6, 1, 8, 4)] * 2))
    return r


# --- T3.10 solo lines: one PC walks into the card alone (two PCs use the
# three-character line). Tuned so that Dassa, Pello and Andra drop 15-70% of the
# time; Ilesse and Serane are logged, and the cards send them to the outs first.

def _solo_s2(k):
    return [E("Tavva"), E("Gallery Knife", arrive=2)]


def _solo_s4(k):
    return [E("Boranis Honor Guard")]


def _solo_s8(k):
    return [E("Church Warden"), E("Church Warden", arrive=3)]


def _solo_s10(k):
    m = E("Maiven Nolonaire", arrive=3)
    m.attacks = m.attacks[:2]                 # she pulls her blows
    return [m]


def _solo_s13(k):
    return [E("Essar Draunel")]


# --- WP6 (T6.10, T6.13) three-player rosters, from existing blocks and the printed
# headcounts only (the Circle brought four knives, Draunel three duelists, Boranis three
# Cousin's Blades; S13's line says "Draunel and two of his duelists").

def _r_s7_wp6(k):
    return [E("Circle Hired Knife") for _ in range(4)]          # all four (cap: four)


def _r_s9_wp6(k):
    if k >= 4:
        return _r_s9(k)
    return [E("Draunel Duelist") for _ in range(3)] + \
        [E("Boranis Cousin's Blade") for _ in range(3)]


def _r_s13_wp6(k):
    if k >= 4:
        return _r_s13(k)
    return [E("Essar Draunel"), E("Draunel Duelist"), E("Draunel Duelist")]


def _r_s12(k, heat4=False):
    return [E("Circle Hired Knife") for _ in range(3 if heat4 else 2)]


def _r_s5(k):
    return [E("Tavva")] + [E("Gallery Knife") for _ in range(2)]


# The Veteran Draunel Duelist block is approximated (58 HP, AC 16, two +6 1d8+4);
# it appears only in the four-player S9/S13 lines.

# 2014 conversion: the four-player printed rosters (DESIGN_oraga_5e_2014 §7).
def _r14_s2(k):
    return [E("Tavva")] + [E("Gallery Knife") for _ in range(3)]


def _r14_s3(k, captain=False):
    r = [E("Bought Sergeant")] + [E("Bought Blade") for _ in range(4)]
    if captain:
        r.append(E("Bought Captain"))
    return r


def _r14_s7(k):
    return [E("Circle Hired Knife") for _ in range(3)]


def _r14_s8(k):
    return [E("Church Warden") for _ in range(3)]


def _r14_s9(k):
    return [E("Draunel Duelist") for _ in range(3)] + [E("Boranis Cousin's Blade") for _ in range(3)]


def _r14_s10(k):
    return [E("Maiven Nolonaire", arrive=3)] + [E("Thenya Border Slinger") for _ in range(2)]


def _r14_s13(k):
    # the Veteran Draunel Duelist as chapter X prints it: 44 HP, AC 15, two +5 1d8+3
    return [E("Essar Draunel"), E("Draunel Duelist", hp=44, attacks=[(5, 1, 8, 3)] * 2)]


CARDS = {
    # name: (roster fn, lethal, end rule, focus rule, extras)
    "S2": dict(roster=_r_s2, lethal=False, end="tavva", focus="leader"),
    "S3": dict(roster=_r_s3, lethal=True, end="s3", focus="low", single_file=True),
    "S3_last": dict(roster=_r_s3, lethal=True, end="last", focus="low", single_file=True),
    "S3_fix": dict(roster=lambda k: _r_s3(k), lethal=True, end="s3", focus="low",
                   single_file=True, captain_round=4),
    # S4 "fought before the reinforcements" (TUNING §3): the two guards fought out,
    # Call the House not modelled. S4_clock ends the fight when the four arrive.
    "S4": dict(roster=_r_s4, lethal=False, end="last", focus="low"),
    "S4_clock": dict(roster=_r_s4, lethal=False, end="s4", focus="low"),
    "S7": dict(roster=_r_s7, lethal=False, end="first_bloodied", focus="low"),
    "S7_nasty": dict(roster=_r_s7, lethal=False, end="half_down", focus="low"),
    "S8": dict(roster=_r_s8, lethal=False, end="two_down", focus="low"),
    "S8_fix": dict(roster=_r_s8, lethal=False, end="one_down", focus="low"),
    "S8_staggered": dict(roster=lambda k: _r_s8(k, staggered=True), lethal=False,
                         end="two_down", focus="low"),
    "S9": dict(roster=_r_s9, lethal=False, end="s9", focus="duelist"),
    "S9_last": dict(roster=_r_s9, lethal=False, end="last", focus="low"),
    "S10": dict(roster=_r_s10, lethal=False, end="maiven", focus="leader"),
    "S10_fix": dict(roster=lambda k: _r_s10(k, fix=True), lethal=False, end="maiven",
                    focus="leader"),
    "S13": dict(roster=_r_s13, lethal=True, end="draunel_bloodied", focus="leader",
                smoke=True),
    "S13_last": dict(roster=_r_s13, lethal=True, end="last", focus="low", smoke=True),
    # WP6 (T6.10, T6.13): canon-capped rosters; after midnight, morale at "half down".
    "S7_wp6": dict(roster=_r_s7_wp6, lethal=False, end="first_bloodied", focus="low"),
    "S7_wp6_last": dict(roster=_r_s7_wp6, lethal=False, end="last", focus="low"),
    "S9_wp6": dict(roster=_r_s9_wp6, lethal=False, end="s9", focus="duelist"),
    "S9_wp6_last": dict(roster=_r_s9_wp6, lethal=False, end="last", focus="low"),
    "S3_wp6": dict(roster=_r_s3, lethal=True, end="s3", focus="low", single_file=True),
    "S5": dict(roster=_r_s5, lethal=True, end="tavva", focus="leader"),
    "S5_wp6": dict(roster=_r_s5, lethal=True, end="half_down", focus="low"),
    "S7_dark": dict(roster=_r_s7, lethal=True, end="half_down", focus="low"),
    "S8_dark": dict(roster=_r_s8, lethal=True, end="half_down", focus="low"),
    "S12": dict(roster=_r_s12, lethal=True, end="first_bloodied", focus="low"),
    "S12_wp6": dict(roster=_r_s12, lethal=True, end="half_down", focus="low"),
    "S12_h4_wp6": dict(roster=lambda k: _r_s12(k, heat4=True), lethal=True, end="half_down",
                       focus="low"),
    "S13_wp6": dict(roster=_r_s13_wp6, lethal=True, end="half_down", focus="low", smoke=True),
    # T3.10 solo lines (see above). S7 and S9 keep their three-character rosters.
    "S2_solo": dict(roster=_solo_s2, lethal=False, end="first_bloodied", focus="leader"),
    "S4_solo": dict(roster=_solo_s4, lethal=False, end="last", focus="low"),
    "S7_solo": dict(roster=lambda k: _r_s7(3), lethal=False, end="first_bloodied", focus="low"),
    "S8_solo": dict(roster=_solo_s8, lethal=False, end="one_down", focus="low"),
    "S9_solo": dict(roster=lambda k: _r_s9(3), lethal=False, end="s9", focus="duelist"),
    "S10_solo": dict(roster=_solo_s10, lethal=False, end="maiven", focus="leader"),
    "S13_solo": dict(roster=_solo_s13, lethal=True, end="draunel_bloodied", focus="leader",
                     smoke=True),
}

# 2014 conversion: each card's 2014 four-player roster, same rules as the card it copies.
for _name, _fn in {"S2": _r14_s2, "S3": _r14_s3, "S7": _r14_s7, "S8": _r14_s8, "S9": _r14_s9,
                   "S10": _r14_s10, "S13": _r14_s13}.items():
    CARDS[_name + "_14"] = dict(CARDS[_name], roster=_fn)


# ------------------------------------------------------------------------ WP6 (T6.9)

@dataclass(frozen=True)
class WP6:
    """WP6 switches for a skirmish (all off = the T3.1 model, draw for draw).
    potions:      each PC may drink its Potion of Healing (2d4 + 2) as a Bonus Action when
                  at 35% HP or less, or feed it to a dying ally (SRD 5.2.1: drinking or
                  administering a potion is a Bonus Action). The caller hands out the potions.
    heat4_finish: a heat-4 snake finishes a downed character who crossed it (05 "Everyone
                  else's steel"): after midnight, a foe whose target dropped keeps attacking
                  it (Advantage; a hit within 5 ft is a critical: two failed death saves)
                  until it is dead, then moves on. Foes that detain never do.
                  Cut from the book by TP61 (2026-10-25): leave it off for the current
                  rules; it stays only so the WP6 runs reproduce."""
    potions: bool = False
    heat4_finish: bool = False


def spend_hit_die(pc, rng):
    """Spend one Hit Die: roll it and add the Constitution modifier (minimum 0)."""
    if pc.dead or pc.hit_dice <= 0:
        return False
    pc.hit_dice -= 1
    size, con = pc.hd
    heal_pc(pc, max(0, roll(rng, 1, size) + con))
    return True


def short_rest(pc, rng):
    """The chapel's Short Rest (T6.8): spend Hit Dice while a die's average still fits under
    the maximum; Second Wind regains one use, Action Surge its use, Channel Divinity one
    use, and Andra's Arcane Recovery one 2nd-level slot."""
    if pc.dead:
        return
    if pc.down:
        heal_pc(pc, 1)
    size, con = pc.hd
    avg = (size + 1) / 2 + con
    while pc.hit_dice > 0 and pc.max_hp - pc.hp >= avg:
        spend_hit_die(pc, rng)
    base = PREGENS[pc.name]
    if base.get("second_wind"):
        pc.second_wind = min(base["second_wind"], pc.second_wind + 1)
    if base.get("action_surge"):
        pc.action_surge = base["action_surge"]
    if base.get("channel"):
        pc.channel = min(base["channel"], pc.channel + 1)
    if pc.name == "Andra":
        pc.slots[2] = min(base["slots"][2], pc.slots.get(2, 0) + 1)


def try_potion(pc, pcs, ctx):
    """WP6 potions: feed a dying ally, else drink when low. Bonus Action. True if used."""
    w = getattr(ctx, "wp6", None)
    if not (w and w.potions) or pc.potions <= 0 or getattr(pc, "_bonus_used", False):
        return False
    if not pc.up:
        return False
    dying = [p for p in pcs if p.down and not p.dead and not p.stable and p.in_fight]
    if ctx.lethal and dying:
        tgt = dying[0]
    elif pc.hp <= int(pc.max_hp * 0.35):
        tgt = pc
    else:
        return False
    pc.potions -= 1
    heal_pc(tgt, roll(ctx.rng, 2, 4) + 2)
    pc._bonus_used = True
    return True


def finish_attack(en, pc, atk, ctx):
    """WP6 heat4_finish: one attack on a downed PC. True on a hit."""
    if pc.dead or not pc.down:
        return False
    to_hit = atk[0]
    nat = d20(ctx.rng, 1)                    # Unconscious: attacks have Advantage
    if nat == 1 or (nat != 20 and nat + to_hit < pc.ac):
        return False
    pc.stable = False                        # a Stable creature that takes damage is dying again
    pc.stable_round = None
    pc.ds_fail += 2                          # within 5 ft: a critical hit, two failures
    if pc.ds_fail >= 3:
        pc.dead = True
        ctx.deaths += 1
    return True


# ------------------------------------------------------------------------ the fight

class Ctx:
    def __init__(self, rng, lethal, crowd="strict"):
        self.rng = rng
        self.lethal = lethal
        self.crowd = crowd
        self.round = 0
        self.drops = 0
        self.dropped = set()
        self.deaths = 0
        self.haul_hi_given = False
        self.wp6 = WP6()


# --- damage, dropping, death saves, the crowd rule (chapter V "Down, Not Out") ---

def damage_pc(pc, dmg, ctx, source=None, nonlethal=False, terms=False):
    """Apply damage. nonlethal: the drop is Stable at once (detain, Down Not Out,
    before midnight). terms: Bought Blade To the Terms (1 HP instead)."""
    if dmg <= 0 or pc.dead:
        return
    if pc.down:
        return                      # nobody here attacks a downed character
    if pc.conc_sw:                  # Ilesse's Spiritual Weapon concentration
        dc = max(10, dmg // 2)
        if d20(ctx.rng) + pc.saves["con"] < dc:
            pc.conc_sw = False
    if terms and dmg >= pc.hp:
        pc.hp = 1
        return
    pc.hp -= dmg
    if pc.hp <= 0:
        overflow = -pc.hp
        pc.hp = 0
        pc.down = True
        pc.down_round = ctx.round
        pc.drops += 1
        pc.adjacent = False
        pc.conc_sw = False
        ctx.drops += 1
        ctx.dropped.add(pc.name)
        if ctx.lethal and not nonlethal:
            if overflow >= pc.max_hp:           # massive damage
                pc.dead = True
                ctx.deaths += 1
                return
            pc.stable = False
            pc.ds_succ = pc.ds_fail = 0
            if ctx.crowd == "generous":
                pc.stable_round = ctx.round     # dragged clear at end of this round
        else:
            pc.stable = True
            pc.stable_round = ctx.round


def heal_pc(pc, amount):
    if pc.dead or amount <= 0:
        return
    if pc.down:
        pc.down = False
        pc.stable = False
        pc.hp = 0
        pc.stable_round = None
    pc.hp = min(pc.max_hp, pc.hp + amount)


def death_save(pc, ctx):
    """Start of a dying PC's turn (SRD 5.2.1)."""
    r = d20(ctx.rng)
    if r < 10 and r != 1 and pc.hi:
        pc.hi = False
        r = d20(ctx.rng)
    if r == 20:
        heal_pc(pc, 1)
        return
    if r == 1:
        pc.ds_fail += 2
    elif r >= 10:
        pc.ds_succ += 1
    else:
        pc.ds_fail += 1
    if pc.ds_fail >= 3:
        pc.dead = True
        pc.down = True
        ctx.deaths += 1
    elif pc.ds_succ >= 3:
        pc.stable = True
        pc.stable_round = ctx.round


def crowd_start_of_round(pcs, ctx):
    """'If a Stable character is still down at the end of the next round and nobody
    has helped, a guest or a servant drags them clear, and they come round with 1 HP
    at the start of the round after.' Strict reading: only Stable PCs. Generous
    reading (F3): a dying PC is dragged clear and Stable at the end of the round it
    dropped (set in damage_pc)."""
    for pc in pcs:
        if pc.down and not pc.dead and pc.stable_round is not None:
            if ctx.round >= pc.stable_round + 2:
                pc.stable = True
                heal_pc(pc, 1)


def stand_up_all(pcs):
    """Between scenes: everyone down and alive is up with at least 1 HP."""
    for pc in pcs:
        if pc.down and not pc.dead:
            heal_pc(pc, 1)
        pc.reset_fight()


# --- PC offence --------------------------------------------------------------------

def pc_attack_roll(pc, target, ctx, to_hit, adv=0, melee=True, crit_range=20):
    """Return (hit, crit, nat). Handles the target's Interpose (Disadvantage),
    Guiding Bolt Advantage, Parry, and Riposte."""
    rng = ctx.rng
    if target.adv_vs_next:
        adv += 1
        target.adv_vs_next = False
    if getattr(ctx, "interpose_ok", None) and ctx.interpose_ok(target):
        adv -= 1
    if pc.provoked_by is not None and pc.provoked_by is not target:
        adv -= 1
    adv = max(-1, min(1, adv))
    nat = d20(rng, adv)
    total = nat + to_hit
    if nat == 1:
        hit = False
    elif nat >= crit_range:
        hit = True
    else:
        hit = total >= target.ac
        if hit and target.parry and melee and target.reaction and total < target.ac + 2:
            target.reaction = False
            hit = False
    crit = hit and nat >= crit_range
    if not hit and melee and target.riposte and target.reaction and target.active:
        target.reaction = False
        enemy_single_attack(target, pc, target.attacks[0], ctx)
    return hit, crit, nat


def deal(target, dmg, ctx, melee_hit=False):
    if dmg <= 0 or not target.active:
        return 0
    if target.uncanny and target.reaction and melee_hit:
        target.reaction = False
        dmg = dmg // 2
    target.hp -= dmg
    target.damaged = True
    return dmg


def pc_offence(pc, target, ctx, first_turn=False, allow_slots=True):
    """One PC turn's damage against one target (Action + Bonus Action where the
    pregen has one). Returns damage dealt."""
    rng = ctx.rng
    total = 0
    n = pc.name
    if n == "Dassa":
        attacks = 1
        if pc.action_surge and (first_turn or target.max_hp > 60):
            pc.action_surge -= 1
            attacks = 2
        savage = not is_2014()                    # Savage Attacker is a 2024 origin feat
        for _ in range(attacks):
            if not target.active:
                break
            hit, crit, _ = pc_attack_roll(pc, target, ctx, 6, crit_range=19)
            if hit:
                dice = 2 if crit else 1
                dmg = roll(rng, dice, 10)
                if savage:
                    dmg = max(dmg, roll(rng, dice, 10))
                    savage = False
                total += deal(target, dmg + 4, ctx, True)
                if not is_2014():
                    target.disadv_next = True     # Sap (2024 Weapon Mastery)
        pc.adjacent = True
    elif n == "Pello":
        sneak_used = False
        ally_close = getattr(ctx, "front_up", lambda p: False)(pc)
        for i, (dn, mod) in enumerate(((1, 4), (1, 0))):     # dagger, Nick dagger
            if not target.active:
                break
            adv = 1 if i == 0 and not is_2014() else 0         # Steady Aim (2024 only)
            hit, crit, _ = pc_attack_roll(pc, target, ctx, 6, adv=adv)
            if hit:
                dice = 2 if crit else 1
                dmg = roll(rng, dice, 4) + mod
                if not sneak_used and (adv > 0 or ally_close):
                    dmg += roll(rng, 4 if crit else 2, 6)
                    sneak_used = True
                total += deal(target, dmg, ctx, True)
        pc.adjacent = True
    elif n == "Andra":
        if allow_slots and pc.slots.get(2, 0) > 0 and target.hp > 10:
            pc.slots[2] -= 1
            total += deal(target, sum(roll(rng, 1, 4) + 1 for _ in range(4)), ctx)
        else:
            hit, crit, _ = pc_attack_roll(pc, target, ctx, 6, melee=False)
            dmg = roll(rng, 2 if crit else 1, 10)
            total += deal(target, dmg if hit else (0 if is_2014() else dmg // 2), ctx)  # Potent Cantrip: 2024
    elif n == "Ilesse":
        bonus_free = not getattr(pc, "_bonus_used", False)
        if bonus_free and not pc.conc_sw and allow_slots and getattr(ctx, "ilesse_attack", OPTIONS["ilesse_attack_slots"]) \
                and pc.slots.get(2, 0) > 0:
            pc.slots[2] -= 1
            pc.conc_sw = True
        if bonus_free and pc.conc_sw and target.active:
            hit, crit, _ = pc_attack_roll(pc, target, ctx, 6, melee=False)
            if hit:
                total += deal(target, roll(rng, 2 if crit else 1, 8) + 4, ctx)
        if target.active:
            if allow_slots and getattr(ctx, "ilesse_attack", OPTIONS["ilesse_attack_slots"]) and pc.slots.get(1, 0) > 2:
                pc.slots[1] -= 1
                hit, crit, _ = pc_attack_roll(pc, target, ctx, 6, melee=False)
                if hit:
                    total += deal(target, roll(rng, 8 if crit else 4, 6), ctx)
                    target.adv_vs_next = True
            else:
                if d20(rng) + target.dex_save < 14:
                    total += deal(target, roll(rng, 1, 8), ctx)
    elif n == "Serane":
        if d20(rng) + target.wis_save < 14:                   # Vicious Mockery
            total += deal(target, roll(rng, 1, 4 if is_2014() else 6), ctx)
            target.disadv_next = True
    pc._bonus_used = False
    return total


# --- PC support ------------------------------------------------------------------

def try_bonus_heal(pc, pcs, ctx):
    """Healing Word a downed ally (Bonus Action). Returns True if used."""
    if not pc.healing_word or pc.slots.get(1, 0) <= 0:
        return False
    downs = [p for p in pcs if p.down and not p.dead and p.in_fight]
    if not downs:
        return False
    tgt = downs[0]
    pc.slots[1] -= 1
    amt = roll(ctx.rng, 1 if is_2014() else 2, 4) + 4 + (3 if pc.name == "Ilesse" else 0)   # Disciple of Life
    heal_pc(tgt, amt)
    if not ctx.haul_hi_given:                 # "Hauling each other up"
        ctx.haul_hi_given = True
        if not pc.hi:
            pc.hi = True
    pc._bonus_used = True
    return True


def try_action_heal(pc, pcs, ctx):
    """Ilesse: Preserve Life or Cure Wounds on a badly hurt ally; Spare the Dying on a
    dying ally when she has no slot. Returns True if the Action was used."""
    if pc.name != "Ilesse":
        return False
    rng = ctx.rng
    dying = [p for p in pcs if p.down and not p.dead and not p.stable and p.in_fight]
    if dying and pc.slots.get(1, 0) <= 0:
        dying[0].stable = True                       # Spare the Dying
        dying[0].stable_round = ctx.round
        return True
    bloodied = [p for p in pcs if p.up and p.hp <= p.max_hp // 2 and p.in_fight]
    missing = sum(p.max_hp // 2 - p.hp for p in bloodied)
    if pc.channel > 0 and len(bloodied) >= 2 and missing >= 12:
        pc.channel -= 1
        pool = 20
        for p in sorted(bloodied, key=lambda q: q.hp):
            give = min(pool, p.max_hp // 2 - p.hp)
            p.hp += give
            pool -= give
        return True
    low = [p for p in pcs if p.up and p.hp <= p.max_hp // 4 and p.in_fight]
    if low and pc.slots.get(1, 0) > 1:
        pc.slots[1] -= 1
        heal_pc(low[0], roll(rng, 1 if is_2014() else 2, 8) + 4 + 3)
        return True
    return False


def try_stabilize(pc, pcs, ctx):
    """Medicine check (DC 10) on a dying ally, as an Action."""
    dying = [p for p in pcs if p.down and not p.dead and not p.stable and p.in_fight]
    if not dying or pc.name == "Ilesse":
        return False
    if d20(ctx.rng) + pc.medicine >= 10:
        dying[0].stable = True
        dying[0].stable_round = ctx.round
    return True


def second_wind(pc, ctx):
    if pc.second_wind > 0 and pc.up and pc.hp <= pc.max_hp // 2:
        pc.second_wind -= 1
        heal_pc(pc, roll(ctx.rng, 1, 10) + 4)
        return True
    return False


# --- enemy offence -------------------------------------------------------------------

def pc_defend(pc, total, nat, pcs, ctx):
    """Reactions that turn a hit into a miss: Shield (Andra), Cutting Words (Serane)."""
    if nat == 20:
        return True
    if total < pc.ac:
        return False
    if pc.shield and pc.slots.get(1, 0) > 0 and total < pc.ac + 5 and not pc.down:
        pc.slots[1] -= 1
        return False
    for bard in pcs:
        if bard.bi > 1 and bard.up and getattr(bard, "_reaction", True) and total - pc.ac <= 2:
            bard.bi -= 1
            bard._reaction = False
            if total - roll(ctx.rng, 1, 6) < pc.ac:
                return False
    return True


def enemy_single_attack(en, pc, atk, ctx, adv=0, pcs=None, sneak_ok=False):
    rng = ctx.rng
    to_hit, dn, ds, bonus = atk
    if en.disadv_next:
        adv -= 1
        en.disadv_next = False
    if en.read and pc.read_marked:
        adv += 1
    adv = max(-1, min(1, adv))
    nat = d20(rng, adv)
    total = nat + to_hit
    if nat == 1:
        return False
    hit = pc_defend(pc, total, nat, pcs or [], ctx)
    if not hit:
        return False
    crit = nat == 20
    dmg = roll(rng, dn * (2 if crit else 1), ds) + bonus
    if en.sneak and sneak_ok:
        dmg += roll(rng, en.sneak[0] * (2 if crit else 1), en.sneak[1])
    if en.paid_extra and adv > 0:
        dmg += roll(rng, 1, 6)
    damage_pc(pc, dmg, ctx, en, nonlethal=en.detain or not ctx.lethal, terms=en.terms)
    return True


def pick_target(en, pcs, ctx):
    """Enemy targeting, per OPTIONS["targeting"]:
    "sticky"  - pick a standing PC at random, keep hitting it until it drops;
    "random"  - a fresh random standing PC for every attack;
    "front"   - sticky, but the front line draws twice the attention;
    "soft"    - focus-fire the PC with the lowest AC, then lowest HP (TUNING's
                "if the crew focus-fires the softest PC" variant)."""
    live = [p for p in pcs if p.up and p.in_fight]
    if not live:
        return None
    mode = OPTIONS["targeting"]
    if mode == "soft":
        return min(live, key=lambda p: (p.ac, p.hp))
    if mode == "random":
        return ctx.rng.choice(live)
    if en.target in live:
        return en.target
    w = []
    for p in live:
        x = 1.0
        if mode == "front":
            if p.role == "front":
                x = 2.0
            elif p.melee:
                x = 1.5
        w.append(x)
    en.target = ctx.rng.choices(live, weights=w)[0]
    return en.target


# --- end conditions -------------------------------------------------------------------

def check_end(rule, enemies, ctx):
    act = [e for e in enemies if e.active and e.arrive <= ctx.round + 1]
    down = [e for e in enemies if e.hp <= 0]
    if not any(e.active for e in enemies):
        return True
    if rule == "last":
        return False
    if rule == "tavva":
        t = enemies[0]
        return not t.active
    if rule == "first_bloodied":
        return any(e.bloodied for e in enemies)
    if rule == "half_down":
        return len(down) * 2 >= len(enemies)
    if rule == "two_down":
        return len(down) >= 2
    if rule == "one_down":
        return len(down) >= 1
    if rule == "maiven":
        return enemies[0].hp <= 0
    if rule == "draunel_bloodied":
        return enemies[0].bloodied
    if rule == "s3":
        sgt = enemies[0]
        blades = [e for e in enemies if e.name == "Bought Blade"]
        return sgt.hp <= 0 or sum(1 for b in blades if b.hp <= 0) * 2 >= len(blades)
    if rule == "s9":
        duel = [e for e in enemies if e.kind == "duelist"]
        cous = [e for e in enemies if e.name == "Boranis Cousin's Blade"]
        if any(e.damaged for e in duel):
            for e in duel:
                e.gone = True
        if sum(1 for c in cous if c.hp <= 0) * 2 >= len(cous):
            for c in cous:
                c.gone = True
        return not any(e.active for e in enemies)
    if rule == "s4":
        return getattr(ctx, "s4_reinforce_round", None) is not None and \
            ctx.round + 1 >= ctx.s4_reinforce_round
    return False


def choose_pc_target(card, enemies, ctx):
    act = [e for e in enemies if e.active and e.arrive <= ctx.round]
    if not act:
        return None
    focus = card["focus"]
    if focus == "leader":
        lead = [e for e in act if e.leader]
        if lead:
            return lead[0]
    if focus == "duelist":
        du = [e for e in act if e.kind == "duelist"]
        if du:
            return min(du, key=lambda e: e.hp)
    return min(act, key=lambda e: e.hp)


def run_fight(card_name, pcs, rng, crowd="strict", max_rounds=30, wp6=None):
    """Fight one card with the given (persistent) PCs. Mutates the PCs. Returns a
    per-fight result dict."""
    card = CARDS[card_name]
    k = len(pcs)
    enemies = card["roster"](k)
    if "captain_round" in card:
        for e in enemies:
            if e.kind == "captain":
                e.arrive = card["captain_round"]
    ctx = Ctx(rng, card["lethal"], crowd)
    if wp6 is not None:
        ctx.wp6 = wp6
    for p in pcs:
        p.reset_fight()
        p.in_fight = not card.get("single_file")
    order_front = sorted(pcs, key=lambda p: {"front": 0, "striker": 1}.get(p.role, 2))

    def front_up(pc):
        return any(q.up and q.in_fight and q.melee and q is not pc for q in pcs)
    ctx.front_up = front_up

    def interpose_ok(target):
        if not target.interpose:
            return False
        for o in enemies:
            if o is not target and o.interpose and o.active and o.reaction and \
                    o.arrive <= ctx.round:
                o.reaction = False
                return True
        return False
    ctx.interpose_ok = interpose_ok
    ctx.s4_reinforce_round = None

    inits = {}
    for p in pcs:
        inits[id(p)] = d20(rng, 1 if p.init_adv else 0) + p.init + rng.random() / 10
    for e in enemies:
        inits[id(e)] = d20(rng) + e.init + rng.random() / 10
    actors = sorted(list(pcs) + enemies, key=lambda a: -inits[id(a)])

    ended = False
    while ctx.round < max_rounds and not ended:
        ctx.round += 1
        if card.get("single_file"):
            entered = min(len(order_front), ctx.round)
            for p in order_front[:entered]:
                if not p.in_fight:
                    p.in_fight = True
        for e in enemies:
            e.reaction = True
        for p in pcs:
            p._reaction = True
        crowd_start_of_round(pcs, ctx)
        for a in actors:
            if ended:
                break
            if isinstance(a, PC):
                pc_turn(a, pcs, enemies, card, ctx)
            else:
                enemy_turn(a, pcs, enemies, card, ctx)
            if check_end(card["end"], enemies, ctx):
                ended = True
                break
            if not any(p.up for p in pcs):
                break
        if not any(p.up for p in pcs):
            # everyone down: the foes walk away (nobody finishes anyone); dying
            # PCs keep rolling until stable or dead, unaided. WP6 heat4_finish: the
            # foes that kill finish the fallen first, for up to three rounds.
            if ctx.wp6.heat4_finish and ctx.lethal:
                for _ in range(3):
                    for e in enemies:
                        if not e.active or e.detain or e.terms:
                            continue
                        for atk in e.attacks:
                            down = [p for p in pcs if p.down and not p.dead]
                            if not down:
                                break
                            finish_attack(e, rng.choice(down), atk, ctx)
            for _ in range(10):
                ctx.round += 1
                crowd_start_of_round(pcs, ctx)
                for p in pcs:
                    if p.down and not p.dead and not p.stable and ctx.lethal:
                        death_save(p, ctx)
                if all(p.dead or p.stable or p.up for p in pcs):
                    break
            break
    wiped = all(p.down or p.dead for p in pcs)
    # Unresolved dying PCs at the end of a lethal fight: roll it out, unaided.
    if ctx.lethal:
        for p in pcs:
            while p.down and not p.dead and not p.stable:
                death_save(p, ctx)
    return dict(any_drop=bool(ctx.dropped), drops=ctx.drops, deaths=ctx.deaths,
                wiped=wiped, broke=check_end(card["end"], enemies, ctx) and not wiped,
                rounds=ctx.round)



def pc_turn(pc, pcs, enemies, card, ctx):
    rng = ctx.rng
    if pc.dead or not pc.in_fight:
        return
    if pc.down:
        if ctx.lethal and not pc.stable:
            death_save(pc, ctx)
        return
    if card.get("smoke") and rng.random() < 0.5 and d20(rng) + pc.saves["con"] < 10:
        smoke_lost = True
    else:
        smoke_lost = False
    if card.get("smoke") and rng.random() < 0.10:              # the fire
        dmg = roll(rng, 2, 6)
        if d20(rng) + pc.saves["dex"] >= 13:
            dmg //= 2
        damage_pc(pc, dmg, ctx, nonlethal=True)                 # the fire never finishes anyone
        if pc.down:
            return
    pc._bonus_used = False
    second_wind(pc, ctx) if pc.name == "Dassa" else None
    if try_bonus_heal(pc, pcs, ctx):
        pass
    else:
        try_potion(pc, pcs, ctx)
    if smoke_lost:
        return
    if try_action_heal(pc, pcs, ctx):
        return
    if ctx.lethal and try_stabilize(pc, pcs, ctx) and pc.role not in ("front", "striker"):
        return
    tgt = choose_pc_target(card, enemies, ctx)
    if tgt is None:
        return
    pc_offence(pc, tgt, ctx, first_turn=(ctx.round == 1))


def enemy_turn(en, pcs, enemies, card, ctx):
    rng = ctx.rng
    if not en.active or en.arrive > ctx.round:
        return
    if card.get("smoke") and rng.random() < 0.5 and d20(rng) + en.con_save < 10:
        return
    if en.read and not en.first_turn_done:
        en.first_turn_done = True
        for p in pcs:                       # The Read: who shields, heals, stands in front
            if p.up and p.in_fight and p.role in ("front", "healer"):
                p.read_marked = True
        return
    en.first_turn_done = True
    if en.kind == "guard" and en.bloodied and ctx.s4_reinforce_round is None:
        ctx.s4_reinforce_round = ctx.round + 2          # Call the House
    if en.kind == "tavva" and en.bloodied:
        # Release a Charge on her next turn: she attacks, then is gone, and the
        # knives break with her (S2 morale).
        if getattr(en, "_charge_pending", False):
            _enemy_attacks(en, pcs, enemies, ctx)
            for e in enemies:
                e.gone = True
            return
        en._charge_pending = True
    if en.provocation:
        tgt = pick_target(en, pcs, ctx)
        if tgt is not None and d20(rng) + tgt.saves["wis"] < 12:
            tgt.provoked_by = en
    _enemy_attacks(en, pcs, enemies, ctx)
    if en.command:
        blades = [b for b in enemies if b.name == "Bought Blade" and b.active and b.reaction]
        if blades:
            blades[0].reaction = False
            t = pick_target(blades[0], pcs, ctx)
            if t is not None:
                enemy_single_attack(blades[0], t, blades[0].attacks[0], ctx, pcs=pcs)


def _enemy_attacks(en, pcs, enemies, ctx):
    sneak_ok = True
    for atk in en.attacks:
        t = en.target
        if (ctx.wp6.heat4_finish and ctx.lethal and not en.detain and not en.terms
                and t is not None and t.down and not t.dead):
            finish_attack(en, t, atk, ctx)
            continue
        tgt = pick_target(en, pcs, ctx)
        if tgt is None:
            return
        allies_close = any(o is not en and o.active for o in enemies)
        hit = enemy_single_attack(en, tgt, atk, ctx, pcs=pcs,
                                  sneak_ok=sneak_ok and allies_close)
        if hit and en.sneak:
            sneak_ok = False


# ----------------------------------------------------------------------- simulate

def _wp6_tag(wp6):
    if wp6 is None or not (wp6.potions or wp6.heat4_finish):
        return ""
    return f"|wp6:{int(wp6.potions)}{int(wp6.heat4_finish)}"


def simulate(card, party="C1", n=2000, seed=1, solo=None, crowd="strict", attrited=False,
             wp6=None):
    """Run n fights of one card. Returns rates over runs. wp6: a WP6 (None or all off =
    the T3.1 model, same seed stream)."""
    rng = random.Random(f"skirm|{card}|{party}|{solo}|{crowd}|{attrited}|{seed}" + _wp6_tag(wp6))
    tot = dict(any_drop=0, drops=0, deaths=0, wiped=0, broke=0, rounds=0)
    for _ in range(n):
        pcs = make_party(party, attrited, rng, solo)
        if wp6 is not None and wp6.potions:
            for p in pcs:
                p.potions = 1
        r = run_fight(card, pcs, rng, crowd, wp6=wp6)
        tot["any_drop"] += r["any_drop"]
        tot["drops"] += r["drops"]
        tot["deaths"] += 1 if r["deaths"] else 0
        tot["wiped"] += r["wiped"]
        tot["broke"] += r["broke"]
        tot["rounds"] += r["rounds"]
    return dict(runs=n, card=card, party=solo or party,
                any_drop=tot["any_drop"] / n, mean_drops=tot["drops"] / n,
                pc_death=tot["deaths"] / n, party_wiped=tot["wiped"] / n,
                enemies_broke=tot["broke"] / n, mean_rounds=tot["rounds"] / n)


def _fmt(r):
    return (f"{r['card']:<9} {r['party']:<7} drop {100*r['any_drop']:5.1f}%  "
            f"drops {r['mean_drops']:.2f}  death {100*r['pc_death']:4.1f}%  "
            f"wiped {100*r['party_wiped']:4.1f}%  rounds {r['mean_rounds']:.1f}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--card", default="S8", choices=sorted(CARDS))
    ap.add_argument("--party", default="C1", choices=sorted(PARTIES))
    ap.add_argument("--solo", default=None, choices=sorted(PREGENS))
    ap.add_argument("--crowd", default="strict", choices=["strict", "generous"])
    ap.add_argument("--all", action="store_true", help="every card x every party")
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--wp6", default=None, help="comma list of WP6 switches: potions,heat4_finish")
    a = ap.parse_args(argv)
    wp6 = WP6(**{k: True for k in a.wp6.split(",")}) if a.wp6 else None
    print(f"skirm.py seed={a.seed} n={a.n} crowd={a.crowd} wp6={a.wp6}")
    if a.all:
        for c in sorted(CARDS):
            for p in sorted(PARTIES):
                print(_fmt(simulate(c, p, a.n, a.seed, crowd=a.crowd, wp6=wp6)))
    else:
        print(_fmt(simulate(a.card, a.party, a.n, a.seed, a.solo, a.crowd, wp6=wp6)))


if __name__ == "__main__":
    main()
