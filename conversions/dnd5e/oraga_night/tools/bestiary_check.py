"""Verify 10_Bestiary.md stat-block math and run a DMG ch.9 CR sanity check.

Data hand-entered from the blocks (read 2026-09-30). The script also cross-checks the
hand-entered AC / HP / hit dice / CR against the text of 10_Bestiary.md, so a block edit
that is not mirrored here fails loudly.

Usage: python bestiary_check.py [--quiet]
Exit 0 = no math problems and the text agrees with the data; 1 = mismatch.
The CR estimate (DMG 2014 ch. 9) is informational and never fails the run.
"""
import argparse, math, re, sys
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
BESTIARY = MODULE / "10_Bestiary.md"

SIZE_DIE = {"M": 8}
XP = {"1/8": 25, "1/4": 50, "1/2": 100, "1": 200, "2": 450, "3": 700, "4": 1100,
      "8": 3900, "9": 5000, "10": 5900, "11": 7200}
CRS = ["0", "1/8", "1/4", "1/2"] + [str(i) for i in range(1, 31)]
def pb(cr):
    v = eval(cr)
    return 2 if v < 5 else 3 if v < 9 else 4 if v < 13 else 5 if v < 17 else 6
# DMG 2014 table: cr -> (AC, HPmax, atk, DPRmax, DC)
T = {"0": (13, 6, 3, 1, 13), "1/8": (13, 35, 3, 3, 13), "1/4": (13, 49, 3, 5, 13),
     "1/2": (13, 70, 3, 8, 13), "1": (13, 85, 3, 14, 13), "2": (13, 100, 3, 20, 13),
     "3": (13, 115, 4, 26, 13), "4": (14, 130, 5, 32, 14), "5": (15, 145, 6, 38, 15),
     "6": (15, 160, 6, 44, 15), "7": (15, 175, 6, 50, 15), "8": (16, 190, 7, 56, 16),
     "9": (16, 205, 7, 62, 16), "10": (17, 220, 7, 68, 16), "11": (17, 235, 8, 74, 17),
     "12": (17, 250, 8, 80, 17), "13": (18, 265, 8, 86, 18), "14": (18, 280, 8, 92, 18),
     "15": (18, 295, 8, 98, 18), "16": (18, 310, 9, 104, 18), "17": (19, 325, 10, 110, 19),
     "18": (19, 340, 10, 116, 19), "19": (19, 355, 10, 122, 19), "20": (19, 400, 10, 140, 19)}
def idx_by(val, col):
    for c in CRS:
        if c in T and val <= T[c][col]:
            return CRS.index(c)
    return CRS.index("20")
def mod(s): return (s - 10) // 2
def avg(n, d, b=0): return int(n * (d + 1) / 2) + b

def defensive(hp, ac, mult=1.0, bonus_hp=0, ac_bonus=0):
    i = idx_by(hp * mult + bonus_hp, 1)
    exp = T[CRS[i]][0]
    return i + ((ac + ac_bonus) - exp) / 2
def offensive(dpr, atk):
    i = idx_by(dpr, 3)
    exp = T[CRS[i]][2]
    return i + (atk - exp) / 2
def crname(x):
    x = max(0, min(round(x), len(CRS) - 1)); return CRS[x]

# name: cr, hd(n), hp, ac, abilities, save_prof list, skills {name:(abil,val)}, pp, perc_prof,
# attacks [(bonus, abil, dmg_str, stated_avg)], dcs [(dc, abil)], dpr, eff mods
B = {
 "Attendant": dict(cr="8", hd=27, hp=229, ac=17, ab=[18,16,18,22,12,6], sv=[2,3],
   sk={"Arcana":(3,9),"Perception":(4,4)}, pp=14,
   atk=[(7,0,(1,10,4),9)], dc=[(14,None)], dpr=40, atkb=7),
 "Cousin's Blade": dict(cr="1/2", hd=4, hp=22, ac=14, ab=[14,13,12,10,10,12], sv=[],
   sk={"Athletics":(0,4),"Intimidation":(5,3)}, pp=10,
   atk=[(4,0,(1,8,2),6)], dc=[], dpr=6, atkb=4),
 "Honor Guard": dict(cr="2", hd=8, hp=52, ac=18, ab=[16,12,14,10,13,11], sv=[0,2],
   sk={"Athletics":(0,5),"Perception":(4,3)}, pp=13,
   atk=[(5,0,(1,8,3),7)], dc=[(13,0)], dpr=14, atkb=5),
 "Bought Blade": dict(cr="1/2", hd=4, hp=22, ac=16, ab=[14,13,12,10,11,10], sv=[],
   sk={"Athletics":(0,4)}, pp=10, atk=[(4,0,(1,8,2),6),(4,0,(1,6,2),5)], dc=[], dpr=6, atkb=4),
 "Bought Captain": dict(cr="4", hd=13, hp=97, ac=17, acb=1, ab=[17,14,16,14,15,14], sv=[0,2,4],
   sk={"Insight":(4,6),"Perception":(4,4),"Persuasion":(5,4)}, pp=14,
   atk=[(5,0,(1,10,3),8)], dc=[], dpr=22, atkb=5),
 "Bought Sergeant": dict(cr="2", hd=8, hp=52, ac=17, acb=1, ab=[15,14,14,12,13,13], sv=[0,2],
   sk={"Insight":(4,3),"Perception":(4,3),"Persuasion":(5,3)}, pp=13,
   atk=[(4,0,(1,8,2),6)], dc=[], dpr=12, atkb=4),
 "Sergeant (Nastier)": dict(cr="4", hd=12, hp=78, ac=17, acb=1, ab=[17,14,14,12,13,13], sv=[],
   sk={"Perception":(4,3)}, pp=13, atk=[(5,0,(1,8,3),7)], dc=[], dpr=21, atkb=5),
 "Church Warden": dict(cr="1", hd=6, hp=33, ac=16, ab=[14,12,13,10,13,11], sv=[4],
   sk={"Insight":(4,3),"Perception":(4,3),"Religion":(3,2)}, pp=13,
   atk=[(4,0,(1,6,2),5)], dc=[(12,0)], dpr=10, atkb=4),
 "Circle Hired Knife": dict(cr="1", hd=5, hp=32, ac=15, ab=[12,16,14,11,12,10], sv=[1],
   sk={"Intimidation":(5,2),"Perception":(4,3),"Stealth":(1,5)}, pp=13,
   atk=[(5,1,(1,4,3),5)], dc=[], dpr=12, atkb=5),
 "Damaris Kovaun": dict(cr="1", hd=6, hp=33, ac=11, ab=[10,12,12,16,18,16], sv=[4,5],
   sk={"History":(3,5),"Insight":(4,8),"Persuasion":(5,5),"Religion":(3,5)}, pp=14,
   atk=[(2,0,(1,6,0),3)], dc=[(14,4)], dpr=3, atkb=2),
 "Draunel Duelist": dict(cr="1", hd=5, hp=27, ac=15, ab=[11,16,12,10,11,14], sv=[1],
   sk={"Acrobatics":(1,5),"Intimidation":(5,4),"Performance":(5,4)}, pp=10,
   atk=[(5,1,(1,8,3),7)], dc=[(12,5)], dpr=10, atkb=5),
 "Duelist (Nastier)": dict(cr="2", hd=8, hp=44, ac=15, ab=[11,16,12,10,11,14], sv=[], sk={}, pp=10,
   atk=[], dc=[], dpr=17, atkb=5),
 "Essar Draunel": dict(cr="3", hd=9, hp=58, ac=16, acb=1, ab=[12,16,14,14,12,17], sv=[1,4,5],
   sk={"Deception":(5,5),"Insight":(4,3),"Intimidation":(5,5),"Persuasion":(5,7)}, pp=11,
   atk=[(5,1,(1,8,3),7)], dc=[], dpr=21, atkb=5),
 "Essin Boranis": dict(cr="2", hd=10, hp=45, ac=14, ab=[10,16,11,15,14,14], sv=[1,3],
   sk={"Deception":(5,6),"Insight":(4,6),"Perception":(4,4),"Sleight of Hand":(1,5),"Stealth":(1,5)}, pp=14,
   atk=[(5,1,(1,4,3),5)], dc=[], dpr=17, atkb=5),
 "Feuding Kinsman": dict(cr="1/8", hd=2, hp=9, ac=11, ab=[13,12,11,9,8,12], sv=[],
   sk={"Athletics":(0,3),"Intimidation":(5,3)}, pp=9,
   atk=[(3,0,(1,4,1),3)], dc=[], dpr=3, atkb=3),
 "Kinsman principal (Nastier)": dict(cr="1/8", hd=4, hp=22, ac=11, ab=[13,12,12,9,8,12], sv=[], sk={}, pp=9,
   atk=[], dc=[], dpr=3, atkb=3),
 "Gallery Knife": dict(cr="1/4", hd=3, hp=13, ac=13, ab=[10,15,10,11,10,10], sv=[],
   sk={"Sleight of Hand":(1,4),"Stealth":(1,4)}, pp=10,
   atk=[(4,1,(1,4,2),4)], dc=[], dpr=4, atkb=4),
 "The Hollow": dict(cr="9", hd=21, hp=157, ac=16, ab=[20,16,17,12,14,10], sv=[0,2,4],
   sk={"Athletics":(0,9),"Perception":(4,6)}, pp=16,
   atk=[(9,0,(2,10,5),16)], dc=[(17,0),(15,None)], dpr=32, atkb=9, mult=1.5, lr=3),
 "Maiven Nolonaire": dict(cr="3", hd=9, hp=58, ac=15, ab=[14,17,14,11,14,13], sv=[1,4],
   sk={"Athletics":(0,4),"Insight":(4,6),"Perception":(4,4),"Survival":(4,4)}, pp=14,
   atk=[(5,1,(1,6,3),6),(5,1,(1,4,3),5)], dc=[(13,1)], dpr=18, atkb=5),
 "Pellin Corro": dict(cr="1/8", hd=3, hp=13, ac=11, ab=[8,12,10,14,16,15], sv=[],
   sk={"Insight":(4,5),"Perception":(4,5),"Persuasion":(5,4)}, pp=15,
   atk=[(3,1,(1,4,1),3)], dc=[], dpr=3, atkb=3),
 "Phern Bodyguard": dict(cr="1", hd=6, hp=33, ac=15, ab=[15,14,13,10,14,10], sv=[0,4],
   sk={"Athletics":(0,4),"Insight":(4,4),"Perception":(4,4)}, pp=14,
   atk=[(4,0,(1,6,2),5)], dc=[(12,0)], dpr=10, atkb=4),
 "The Radiant": dict(cr="10", hd=25, hp=162, ac=17, ab=[16,20,14,14,16,20], sv=[1,4,5],
   sk={"Acrobatics":(1,9),"Performance":(5,13),"Perception":(4,7),"Religion":(3,6)}, pp=17,
   atk=[(9,1,(2,10,5),16)], dc=[(17,None),(15,None)], dpr=50, atkb=9, mult=1.5, lr=3),
 "Rhaza Callun": dict(cr="1/4", hd=5, hp=22, ac=11, ab=[9,12,11,18,15,14], sv=[3,4],
   sk={"Deception":(5,4),"Insight":(4,4),"Investigation":(3,6),"Persuasion":(5,4)}, pp=12,
   atk=[(3,1,(1,4,1),3)], dc=[], dpr=3, atkb=3),
 "Sect Guard": dict(cr="1/8", hd=2, hp=11, ac=16, ab=[13,12,12,10,11,10], sv=[],
   sk={"Perception":(4,2)}, pp=12, atk=[(3,0,(1,6,1),4)], dc=[], dpr=4, atkb=3),
 "Tavva": dict(cr="2", hd=8, hp=44, ac=15, ab=[10,17,12,14,14,15], sv=[1,3],
   sk={"Deception":(5,6),"Insight":(4,4),"Perception":(4,6),"Sleight of Hand":(1,7),"Stealth":(1,7)}, pp=16,
   atk=[(5,1,(1,4,3),5)], dc=[(13,1)], dpr=17, atkb=5),
 "Thenya Border Slinger": dict(cr="1/2", hd=3, hp=19, ac=14, ab=[11,16,14,10,13,10], sv=[],
   sk={"Perception":(4,3),"Stealth":(1,5),"Survival":(4,3)}, pp=13,
   atk=[(5,1,(1,4,3),5),(5,1,(1,6,3),6)], dc=[], dpr=6, atkb=5),
 "Vorlain Boranis": dict(cr="3", hd=11, hp=60, ac=15, acb=1, ab=[14,16,12,15,13,17], sv=[1,4,5],
   sk={"Deception":(5,7),"Insight":(4,5),"Perception":(4,3),"Persuasion":(5,5)}, pp=13,
   atk=[(5,1,(1,8,3),7)], dc=[], dpr=17, atkb=5),
 "The Wept": dict(cr="11", hd=22, hp=187, ac=18, ab=[22,16,18,13,16,18], sv=[0,2,4],
   sk={"Athletics":(0,10),"Insight":(4,7),"Perception":(4,7)}, pp=17,
   atk=[(10,0,(4,10,6),28)], dc=[(15,None)], dpr=84, atkb=10, mult=1.5, lr=3),
}

# Base block name in the text, when it differs from the key above.
TEXT_NAME = {"Attendant": "The Attendant", "Cousin's Blade": "Boranis Cousin's Blade", "Honor Guard": "Boranis Honor Guard"}
# Nastier variants whose numbers are printed in the base block's Nastier line.
NASTIER_OF = {"Sergeant (Nastier)": "Bought Sergeant", "Duelist (Nastier)": "Draunel Duelist",
              "Kinsman principal (Nastier)": "Feuding Kinsman"}


def split_blocks(text):
    """Map H3 heading -> block text (up to the next H2/H3)."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^(#{2,3}) (.+)$", line)
        if m:
            if cur: out[cur] = "\n".join(buf)
            cur = m.group(2).strip() if m.group(1) == "###" else None
            buf = []
        elif cur:
            buf.append(line)
    if cur: out[cur] = "\n".join(buf)
    return out


def text_problems(text):
    blocks = split_blocks(text)
    probs = []
    for n, b in B.items():
        if n in NASTIER_OF:
            blk = blocks.get(NASTIER_OF[n])
            m = blk and re.search(r"\*\*Nastier\.\*\*(.*?)(?:\n> \*|\n\n)", blk, re.S)
            if not m:
                probs.append(f"{n}: Nastier line not found in text"); continue
            line = m.group(1).replace("\n> ", " ")
            hp = re.search(r"(\d+) HP \((\d+)d8", line)
            if not hp or (int(hp.group(1)), int(hp.group(2))) != (b["hp"], b["hd"]):
                probs.append(f"{n}: text HP/HD {hp.groups() if hp else None} vs data {b['hp']}/{b['hd']}d8")
            cr = re.search(r"CR ([\d/]+)", line)
            if cr and cr.group(1) != b["cr"]:
                probs.append(f"{n}: text CR {cr.group(1)} vs data {b['cr']}")
            continue
        name = TEXT_NAME.get(n, n)
        blk = blocks.get(name)
        if blk is None:
            probs.append(f"{n}: no '### {name}' block in 10_Bestiary.md"); continue
        ac = re.search(r"\*\*AC\*\* (\d+)", blk)
        hp = re.search(r"\*\*HP\*\* (\d+) \((\d+)d8", blk)
        cr = re.search(r"\*\*CR\*\* ([\d/]+)", blk)
        if not ac or int(ac.group(1)) != b["ac"]:
            probs.append(f"{n}: text AC {ac.group(1) if ac else None} vs data {b['ac']}")
        if not hp or (int(hp.group(1)), int(hp.group(2))) != (b["hp"], b["hd"]):
            probs.append(f"{n}: text HP {hp.groups() if hp else None} vs data {b['hp']}/{b['hd']}d8")
        if not cr or cr.group(1) != b["cr"]:
            probs.append(f"{n}: text CR {cr.group(1) if cr else None} vs data {b['cr']}")
    return probs


ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("--quiet", action="store_true", help="print only the summary line and any problems")
args = ap.parse_args()
out = (lambda *a, **k: None) if args.quiet else print

# Stated saves in the Save row (for the proficient abilities): check = mod + PB
problems = []
for n, b in B.items():
    p = pb(b["cr"]); m = [mod(s) for s in b["ab"]]; con = m[2]
    exp_hp = avg(b["hd"], 8, b["hd"] * con)
    if exp_hp != b["hp"]:
        problems.append(f"{n}: HP stated {b['hp']} vs {b['hd']}d8+{b['hd']*con} = {exp_hp}")
    for sk, (a, v) in b["sk"].items():
        if v == m[a] + p: continue
        if v == m[a] + 2 * p: problems.append(f"{n}: {sk} +{v} = expertise (OK, note)")
        else: problems.append(f"{n}: {sk} +{v} vs mod {m[a]} + PB {p}")
    per = b["sk"].get("Perception")
    exp_pp = 10 + (per[1] if per else m[4])
    if exp_pp != b["pp"]:
        problems.append(f"{n}: passive Perception {b['pp']} vs {exp_pp}")
    for bonus, a, (dn, dd, db), st in b["atk"]:
        if bonus != m[a] + p: problems.append(f"{n}: attack +{bonus} vs {m[a]}+{p}")
        if avg(dn, dd, db) != st: problems.append(f"{n}: dmg {st} vs {dn}d{dd}+{db}={avg(dn,dd,db)}")
        if db != m[a]: problems.append(f"{n}: dmg mod {db} vs ability {m[a]}")
    for dc, a in b["dc"]:
        if a is None: continue
        if dc != 8 + p + m[a]: problems.append(f"{n}: DC {dc} vs 8+{p}+{m[a]}")
    if b["cr"] in XP: pass
    mult = b.get("mult", 1.0)
    lr_hp = b.get("lr", 0) * (20 if 5 <= eval(b["cr"]) <= 10 else 30 if eval(b["cr"]) > 10 else 10)
    d = defensive(b["hp"], b["ac"], mult, lr_hp, b.get("acb", 0))
    o = offensive(b["dpr"], b["atkb"])
    fin = (d + o) / 2
    stated = CRS.index(b["cr"])
    flag = "  <-- >1 step off" if abs(fin - stated) > 1.01 else ""
    out(f"{n:28s} stated CR {b['cr']:>4s}  def {crname(d):>4s}  off {crname(o):>4s}  "
          f"=> ~CR {crname(fin):>4s} (steps {fin - stated:+.1f}){flag}")
notes = [x for x in problems if "(OK, note)" in x]
errors = [x for x in problems if "(OK, note)" not in x]
errors += text_problems(BESTIARY.read_text(encoding="utf-8"))
out("\nNotes:")
for x in notes: out(" -", x)
if errors:
    print("MISMATCHES:")
    for x in errors: print(" -", x)
n_nastier = sum(1 for k in B if "(Nastier)" in k)
print(f"bestiary_check: {len(B) - n_nastier} blocks + {n_nastier} Nastier checked; "
      f"{len(errors)} mismatch(es)")
sys.exit(1 if errors else 0)
