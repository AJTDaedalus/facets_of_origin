"""SRD 5.1 (2014 rules) legality check for the five 4th-level pregens in
11_Pregenerated_Characters.md (2014 conversion, DESIGN_oraga_5e_2014; was SRD 5.2.1).

Data hand-entered from the chapter. The printed AC, Hit Points, Initiative and Passive
Perception are also cross-checked against the text of chapter XI, so an edit there that
is not mirrored here fails loudly.

2014 build: SRD human (+1 to every score), the standard array, the 4th-level Ability
Score Improvement, a background of two skills; the gifted take their gift as a bonus
feat at 1st level (chapter III), which grants no skill. Jack of All Trades adds half the
proficiency bonus to every ability check without proficiency, Initiative included.

Usage: python pregen_check.py [--quiet] [--file PATH]
Exit 0 = every pregen is legal and matches the text; 1 = mismatch.
"""
import argparse, re, sys
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
PREGENS = MODULE / "11_Pregenerated_Characters.md"

PB=2; LV=4
ARRAY=sorted([15,14,13,12,10,8])
HUMAN=1   # SRD 5.1 human: every ability score +1
m=lambda s:(s-10)//2
HD={'bard':8,'rogue':8,'wizard':6,'fighter':10,'cleric':8}
# 2014 tables at 4th level (SRD 5.1): cantrips known; bard spells known; prepared =
# ability modifier + class level for clerics and wizards
CANTRIPS={'bard':3,'wizard':4,'cleric':4}
KNOWN={'bard':7}
PREP_ABIL={'wizard':'INT','cleric':'WIS'}
PCs={
 'Serane':dict(cls='bard',final=dict(STR=9,DEX=14,CON=15,INT=11,WIS=13,CHA=18),asi={'CHA':2},
   armor=('studded',12,None),printed=dict(AC=14,HP=31,init=3,pp=13,dc=14,atk=6),
   prof={'Persuasion','History','Deception','Performance','Insight','Investigation','Perception','Religion'},exp={'Persuasion','Insight'},
   skillsrc=dict(bg=2,cls=3,sub=3),cantrips=['message','minor illusion','vicious mockery'],
   known=['charm person','disguise self','healing word','hideous laughter','silent image','calm emotions','suggestion'],
   printed_sk=dict(Persuasion=8,Insight=5,Deception=6,Performance=6,Perception=3,History=2,Investigation=2,Religion=2,Intimidation=5,Acrobatics=3,SleightofHand=3,Stealth=3,AnimalHandling=2,Medicine=2,Survival=2,Arcana=1,Nature=1,Athletics=0),joat=True),
 'Pello':dict(cls='rogue',final=dict(STR=9,DEX=18,CON=14,INT=13,WIS=15,CHA=11),asi={'DEX':2},
   armor=('studded',12,None),printed=dict(AC=16,HP=31,init=4,pp=14),
   prof={'Stealth','Sleight of Hand','Acrobatics','Perception','Insight','Persuasion'},exp={'Stealth','Sleight of Hand'},
   skillsrc=dict(bg=2,cls=4,sub=0),
   printed_sk={'Stealth':8,'Sleight of Hand':8,'Acrobatics':6,'Perception':4,'Insight':4,'Persuasion':2}),
 'Andra':dict(cls='wizard',final=dict(STR=9,DEX=15,CON=14,INT=18,WIS=13,CHA=11),asi={'INT':2},
   armor=('mage armor',13,None),printed=dict(AC=15,HP=26,init=2,pp=11,dc=14,atk=6),
   prof={'History','Investigation','Arcana','Insight'},exp=set(),
   skillsrc=dict(bg=2,cls=2,sub=0),cantrips=['fire bolt','mage hand','minor illusion','ray of frost'],
   prep=['mage armor','magic missile','shield','silent image','sleep','darkness','hold person','misty step'],
   book1=['comprehend languages','detect magic','identify','mage armor','magic missile','shield','silent image','sleep'],book2=['darkness','hold person','misty step','web'],
   printed_sk={'History':6,'Arcana':6,'Investigation':6,'Insight':3,'Nature':4,'Religion':4,'Perception':1}),
 'Dassa':dict(cls='fighter',final=dict(STR=18,DEX=14,CON=15,INT=9,WIS=13,CHA=11),asi={'STR':2},
   armor=('scale mail',14,2),defense=True,printed=dict(AC=17,HP=36,init=2,pp=13),
   prof={'Athletics','Insight','Perception','Intimidation'},exp=set(),
   skillsrc=dict(bg=2,cls=2,sub=0),
   printed_sk={'Athletics':6,'Insight':3,'Perception':3,'Intimidation':2}),
 'Ilesse':dict(cls='cleric',final=dict(STR=9,DEX=13,CON=15,INT=11,WIS=18,CHA=14),asi={'WIS':2},
   armor=('chain shirt',13,2),printed=dict(AC=14,HP=31,init=1,pp=14,dc=14,atk=6),
   prof={'Insight','Persuasion','Medicine','History'},exp=set(),
   skillsrc=dict(bg=2,cls=2,sub=0),cantrips=['guidance','light','sacred flame','spare the dying'],
   prep=['command','guiding bolt','healing word','sanctuary','shield of faith','aid','calm emotions','prayer of healing'],
   printed_sk={'Insight':6,'Medicine':6,'Persuasion':4,'History':2}),
}
SK={'Athletics':'STR','Acrobatics':'DEX','Sleight of Hand':'DEX','Stealth':'DEX','Arcana':'INT','History':'INT','Investigation':'INT','Nature':'INT','Religion':'INT',
 'Animal Handling':'WIS','Insight':'WIS','Medicine':'WIS','Perception':'WIS','Survival':'WIS','Deception':'CHA','Intimidation':'CHA','Performance':'CHA','Persuasion':'CHA'}

# CAST-11 (T3.5): a pregen whose spells need a focus must carry one. The printed
# Spellcasting line names it, and the same item is on the Carrying line.
# O16: SRD 5.2.1 Title-Cases equipment and focus names, so the match is "Arcane Focus".
# Owner ruling Q16b (2026-10-05): Ilesse's warding crystal counts as her Holy Symbol.
FOCUS={'Andra':dict(spell='a crystal as Arcane Focus', carry='crystal (Arcane Focus)'),
       'Ilesse':dict(spell='warding crystal as Holy Symbol', carry='warding crystal (Holy Symbol)')}


def legality_issues(out=print):
    issues=[]
    for n,p in PCs.items():
        f=p['final']; base={k:v-HUMAN for k,v in f.items()}
        for k,v in p['asi'].items(): base[k]-=v
        ok_arr=sorted(base.values())==ARRAY
        ok_asi=sum(p['asi'].values())==2 and len(p['asi']) in (1,2)
        ok_cap=max(f.values())<=20
        hd=HD[p['cls']]; con=m(f['CON'])
        hp=hd+con+(LV-1)*(hd//2+1+con)
        name,base_ac,cap=p['armor']
        dex=m(f['DEX']); ac=base_ac+(dex if cap is None else min(dex,cap))+(1 if p.get('defense') else 0)
        init=dex+(PB//2 if p.get('joat') else 0)
        pp=10+m(f['WIS'])+(PB if 'Perception' in p['prof'] else 0)
        nprof=sum(p['skillsrc'].values())
        out(f"{n}: base {base} array={ok_arr} asi={ok_asi} cap={ok_cap} | HP {hp}/{p['printed']['HP']} AC {ac}/{p['printed']['AC']} init {init}/{p['printed']['init']} PP {pp}/{p['printed']['pp']} | skills {len(p['prof'])} vs sources {nprof}")
        for chk,a,b in [('HP',hp,p['printed']['HP']),('AC',ac,p['printed']['AC']),('init',init,p['printed']['init']),('PP',pp,p['printed']['pp']),('skillcount',len(p['prof']),nprof)]:
            if a!=b: issues.append((n,chk,a,b))
        if not(ok_arr and ok_asi and ok_cap): issues.append((n,'abilities',base,None))
        for sk,val in p['printed_sk'].items():
            key={'SleightofHand':'Sleight of Hand','AnimalHandling':'Animal Handling'}.get(sk,sk)
            mod=m(f[SK[key]])
            if key in p['prof']: mod+=PB*(2 if key in p['exp'] else 1)
            elif p.get('joat'): mod+=PB//2
            if mod!=val: issues.append((n,'skill '+key,mod,val))
        if 'dc' in p['printed']:
            abil={'bard':'CHA','wizard':'INT','cleric':'WIS'}[p['cls']]
            dc=8+PB+m(f[abil]); atk=PB+m(f[abil])
            if (dc,atk)!=(p['printed']['dc'],p['printed']['atk']): issues.append((n,'spell dc/atk',(dc,atk),(p['printed']['dc'],p['printed']['atk'])))
            nc=len(p['cantrips']); expc=CANTRIPS[p['cls']]
            if nc!=expc: issues.append((n,'cantrips',nc,expc))
            if p['cls'] in KNOWN:
                if len(p['known'])!=KNOWN[p['cls']]: issues.append((n,'spells known',len(p['known']),KNOWN[p['cls']]))
                out(f"   cantrips {nc}/{expc} known {len(p['known'])}/{KNOWN[p['cls']]} (+ gift cantrip)")
            else:
                want=m(f[PREP_ABIL[p['cls']]])+LV
                if len(p['prep'])!=want: issues.append((n,'prepared',len(p['prep']),want))
                out(f"   cantrips {nc}/{expc} prepared {len(p['prep'])}/{want} (+ gift cantrip; Life domain spells always prepared)")
        if n=='Andra':
            book=len(p['book1'])+len(p['book2']); exp=6+2*(LV-1)
            out(f"   spellbook {book}/{exp} (6 + 2 per level after 1st); prepared all in book: {set(p['prep'])<=set(p['book1']+p['book2'])}")
            if book!=exp: issues.append((n,'spellbook',book,exp))
            if not set(p['prep'])<=set(p['book1']+p['book2']): issues.append((n,'prepared not in book',None,None))
    return issues


def text_issues(text):
    found = []
    secs = re.split(r"^## ", text, flags=re.M)[1:]
    for n, p in PCs.items():
        sec = next((x for x in secs if x.startswith(n)), None)
        if sec is None:
            found.append((n, 'section missing in text', None, None)); continue
        sec = re.sub(r"\s+", " ", sec)
        pats = {'AC': r"\*\*Armor Class\*\* (\d+)", 'HP': r"\*\*Hit Points\*\* (\d+)",
                'init': r"\*\*Initiative\*\* \+(\d+)", 'pp': r"\*\*Passive Perception\*\* (\d+)"}
        for k, pat in pats.items():
            m_ = re.search(pat, sec)
            if not m_ or int(m_.group(1)) != p['printed'][k]:
                found.append((n, 'text ' + k, m_.group(1) if m_ else None, p['printed'][k]))
    return found


def _section(text, name):
    secs = re.split(r"^## ", text, flags=re.M)[1:]
    sec = next((x for x in secs if x.startswith(name)), None)
    return None if sec is None else re.sub(r"\s+", " ", sec)


def focus_issues(text):
    found = []
    for n, f in FOCUS.items():
        sec = _section(text, n)
        if sec is None:
            found.append((n, 'section missing in text', None, None)); continue
        sp = re.search(r"\*\*Spellcasting\*\* \(([^)]*)\)", sec)
        sp_text = sp.group(1) if sp else None
        if not sp_text or f['spell'] not in sp_text:
            found.append((n, 'spellcasting focus', sp_text, f['spell']))
        carry = re.search(r"\*\*Carrying\.\*\* (.*?)(?= \*\*| ---|$)", sec)
        if not carry or f['carry'] not in carry.group(1):
            found.append((n, 'focus not carried', None, f['carry']))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pregen legality check for chapter XI.")
    ap.add_argument("--quiet", action="store_true", help="print only the summary line and any problems")
    ap.add_argument("--file", type=Path, default=PREGENS, help="pregen text to check (default: 11_Pregenerated_Characters.md)")
    args = ap.parse_args(argv)
    out = (lambda *a, **k: None) if args.quiet else print
    text = args.file.read_text(encoding="utf-8")
    issues = legality_issues(out) + text_issues(text) + focus_issues(text)
    if issues:
        print('ISSUES:', issues)
    print(f"pregen_check: {len(PCs)} pregens checked; {len(issues)} issue(s)")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
