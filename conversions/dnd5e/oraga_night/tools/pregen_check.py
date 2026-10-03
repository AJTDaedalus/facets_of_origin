"""SRD 5.2.1 (2024 rules) legality check for the five 4th-level pregens in
11_Pregenerated_Characters.md.

Data hand-entered from the chapter (read 2026-09-30). The printed AC, Hit Points,
Initiative and Passive Perception are also cross-checked against the text of chapter XI,
so an edit there that is not mirrored here fails loudly.

Usage: python pregen_check.py [--quiet]
Exit 0 = every pregen is legal and matches the text; 1 = mismatch.
"""
import argparse, re, sys
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
PREGENS = MODULE / "11_Pregenerated_Characters.md"
ap = argparse.ArgumentParser(description="Pregen legality check for chapter XI.")
ap.add_argument("--quiet", action="store_true", help="print only the summary line and any problems")
args = ap.parse_args()
out = (lambda *a, **k: None) if args.quiet else print

PB=2; LV=4
ARRAY=sorted([15,14,13,12,10,8])
m=lambda s:(s-10)//2
HD={'bard':8,'rogue':8,'wizard':6,'fighter':10,'cleric':8}
# per-level prepared/cantrip tables at 4th (2024 PHB/SRD 5.2.1)
CANTRIPS={'bard':3,'wizard':4,'cleric':4}
PREP={'bard':7,'wizard':7,'cleric':7}
PCs={
 'Serane':dict(cls='bard',final=dict(STR=8,DEX=14,CON=14,INT=10,WIS=13,CHA=18),bg={'CHA':2,'WIS':1},asi={'CHA':1,'CON':1},bg_opts={'INT','WIS','CHA'},
   armor=('studded',12,None),alert=True,printed=dict(AC=14,HP=31,init=4,pp=13,dc=14,atk=6),
   prof={'Persuasion','Deception','Intimidation','Performance','Insight','Perception','History','Investigation','Religion'},exp={'Persuasion','Insight'},
   skillsrc=dict(bg=2,cls=3,skillful=1,sub=3,feat=0),cantrips=['message','minor illusion','vicious mockery'],prep=['charm person','disguise self','healing word','hideous laughter','silent image','calm emotions','suggestion'],
   printed_sk=dict(Persuasion=8,Deception=6,Intimidation=6,Performance=6,Insight=5,Perception=3,History=2,Investigation=2,Religion=2,Acrobatics=3,SleightofHand=3,Stealth=3,AnimalHandling=2,Medicine=2,Survival=2,Arcana=1,Nature=1,Athletics=0),joat=True),
 'Pello':dict(cls='rogue',final=dict(STR=8,DEX=19,CON=14,INT=12,WIS=14,CHA=10),bg={'DEX':2,'WIS':1},asi={'DEX':2},bg_opts={'DEX','INT','WIS'},
   armor=('studded',12,None),alert=False,printed=dict(AC=16,HP=31,init=4,pp=14),
   prof={'Stealth','Sleight of Hand','Acrobatics','Insight','Perception','Investigation','Deception','Persuasion','Athletics'},exp={'Stealth','Sleight of Hand'},
   skillsrc=dict(bg=2,cls=4,skillful=1,sub=0,feat=2),
   printed_sk={'Stealth':8,'Sleight of Hand':8,'Acrobatics':6,'Insight':4,'Perception':4,'Investigation':3,'Deception':2,'Persuasion':2,'Athletics':1}),
 'Andra':dict(cls='wizard',final=dict(STR=8,DEX=14,CON=14,INT=19,WIS=12,CHA=10),bg={'INT':2,'CON':1},asi={'INT':2},bg_opts={'CON','INT','WIS'},
   armor=('mage armor',13,None),alert=False,printed=dict(AC=15,HP=26,init=2,pp=13,dc=14,atk=6),
   prof={'History','Arcana','Investigation','Nature','Religion','Insight','Medicine','Perception'},exp={'History'},
   skillsrc=dict(bg=2,cls=2,skillful=1,sub=0,feat=3),cantrips=['fire bolt','mage hand','minor illusion','ray of frost'],prep=['mage armor','magic missile','shield','silent image','sleep','darkness','misty step'],
   book1=['alarm','comprehend languages','detect magic','feather fall','identify','mage armor','magic missile','shield','silent image','sleep'],book2=['darkness','hold person','misty step','web'],
   printed_sk={'History':8,'Arcana':6,'Investigation':6,'Nature':6,'Religion':6,'Insight':3,'Medicine':3,'Perception':3}),
 'Dassa':dict(cls='fighter',final=dict(STR=18,DEX=13,CON=16,INT=8,WIS=12,CHA=10),bg={'STR':2,'CON':1},asi={'STR':1,'CON':1},bg_opts={'STR','CON','WIS'},
   armor=('breastplate',14,2),defense=True,alert=True,printed=dict(AC=16,HP=40,init=3,pp=13),
   prof={'Athletics','Insight','Medicine','Perception','Intimidation'},exp=set(),
   skillsrc=dict(bg=2,cls=2,skillful=1,sub=0,feat=0),
   printed_sk={'Athletics':6,'Insight':3,'Medicine':3,'Perception':3,'Intimidation':2}),
 'Ilesse':dict(cls='cleric',final=dict(STR=8,DEX=12,CON=14,INT=10,WIS=18,CHA=15),bg={'WIS':2,'CHA':1},asi={'WIS':1,'CON':1},bg_opts={'CON','WIS','CHA'},
   armor=('chain shirt',13,2),alert=True,printed=dict(AC=14,HP=31,init=3,pp=14,dc=14,atk=6),
   prof={'Insight','Medicine','Persuasion','History','Stealth'},exp=set(),
   skillsrc=dict(bg=2,cls=2,skillful=1,sub=0,feat=0),cantrips=['guidance','light','mending','sacred flame','spare the dying'],thaumaturge=True,
   prep=['command','guiding bolt','healing word','sanctuary','shield of faith','calm emotions','spiritual weapon'],
   printed_sk={'Insight':6,'Medicine':6,'Persuasion':4,'Arcana':4,'Religion':4,'Stealth':3,'History':2}),
}
SK={'Athletics':'STR','Acrobatics':'DEX','Sleight of Hand':'DEX','Stealth':'DEX','Arcana':'INT','History':'INT','Investigation':'INT','Nature':'INT','Religion':'INT',
 'Animal Handling':'WIS','Insight':'WIS','Medicine':'WIS','Perception':'WIS','Survival':'WIS','Deception':'CHA','Intimidation':'CHA','Performance':'CHA','Persuasion':'CHA'}
issues=[]
for n,p in PCs.items():
    f=p['final']; base=dict(f)
    for d in (p['bg'],p['asi']):
        for k,v in d.items(): base[k]-=v
    ok_arr=sorted(base.values())==ARRAY
    ok_bg=set(p['bg'])<=p['bg_opts'] and sorted(p['bg'].values())==[1,2]
    ok_cap=max(f.values())<=20
    hd=HD[p['cls']]; con=m(f['CON'])
    hp=hd+con+(LV-1)*(hd//2+1+con)
    name,base_ac,cap=p['armor']
    dex=m(f['DEX']); ac=base_ac+(dex if cap is None else min(dex,cap))+(1 if p.get('defense') else 0)
    init=dex+(PB if p['alert'] else 0)
    pp=10+m(f['WIS'])+(PB if 'Perception' in p['prof'] else 0)
    src=p['skillsrc']; nprof=sum(src.values())
    out(f"{n}: base {base} array={ok_arr} bg={ok_bg} cap={ok_cap} | HP {hp}/{p['printed']['HP']} AC {ac}/{p['printed']['AC']} init {init}/{p['printed']['init']} PP {pp}/{p['printed']['pp']} | skills {len(p['prof'])} vs sources {nprof}")
    for chk,a,b in [('HP',hp,p['printed']['HP']),('AC',ac,p['printed']['AC']),('init',init,p['printed']['init']),('PP',pp,p['printed']['pp']),('skillcount',len(p['prof']),nprof)]:
        if a!=b: issues.append((n,chk,a,b))
    if not(ok_arr and ok_bg and ok_cap): issues.append((n,'abilities',base,None))
    # skills
    for sk,val in p['printed_sk'].items():
        key={'SleightofHand':'Sleight of Hand','AnimalHandling':'Animal Handling'}.get(sk,sk)
        mod=m(f[SK[key]])
        if key in p['prof']: mod+=PB*(2 if key in p['exp'] else 1)
        elif p.get('joat'): mod+=PB//2
        if p.get('thaumaturge') and key in ('Arcana','Religion') and key not in p['prof']: mod+=max(1,m(f['WIS']))
        if mod!=val: issues.append((n,'skill '+key,mod,val))
    if 'dc' in p['printed']:
        abil={'bard':'CHA','wizard':'INT','cleric':'WIS'}[p['cls']]
        dc=8+PB+m(f[abil]); atk=PB+m(f[abil])
        if (dc,atk)!=(p['printed']['dc'],p['printed']['atk']): issues.append((n,'spell dc/atk',(dc,atk),(p['printed']['dc'],p['printed']['atk'])))
        nc=len(p['cantrips']); expc=CANTRIPS[p['cls']]+(1 if p.get('thaumaturge') else 0)
        np_=len(p['prep'])
        out(f"   cantrips {nc}/{expc} prepared {np_}/{PREP[p['cls']]} (+ gift cantrip; Life domain spells always prepared)")
        if nc!=expc: issues.append((n,'cantrips',nc,expc))
        if np_!=PREP[p['cls']]: issues.append((n,'prepared',np_,PREP[p['cls']]))
    if n=='Andra':
        book=len(p['book1'])+len(p['book2']); exp=6+2*(LV-1)+2
        out(f"   spellbook {book}/{exp} (6 + 2/level + Evocation Savant 2); prepared all in book: {set(p['prep'])<=set(p['book1']+p['book2'])}")
        if book!=exp: issues.append((n,'spellbook',book,exp))

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

issues += text_issues(PREGENS.read_text(encoding="utf-8"))
if issues:
    print('ISSUES:', issues)
print(f"pregen_check: {len(PCs)} pregens checked; {len(issues)} issue(s)")
sys.exit(1 if issues else 0)
