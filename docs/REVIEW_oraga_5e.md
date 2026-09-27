# Review — Oraga Night, 5e Edition (integration pass)

*2026-09-27, integration reviewer. Scope: `conversions/dnd5e/oraga_night/` (README,
01–11, INVENTIONS_5e.md, flow/). Branch `feat/oraga-5e`; nothing committed.*

Four drafters wrote the book in parallel. The rules chapters (09, 10) were already
in step with each other; the drift was in the chapters that point at them (04, 05, 07,
08, the flow data), which had been written against an older card numbering and an
older draft of the after-midnight snake beats.

## 1. Known issues — status

| # | Issue | Finding | Fix |
|---|---|---|---|
| 1 | Fight-card numbering drift | 09 is internally consistent (S6 Boranis, S7 Circle, S8 Church, S9 Draunel+Boranis, S10 Thenya, S11 Phern, S12 Circle, S13 Draunel+Boranis). 10's Table X–1 and every block's *Cards* line already matched 09. Stale: 04 Table IV–1 (all six rows), 07's six "If it comes to steel" lines, 08's Optional Steel row and Snake Tracker. README said "S1–S12". 01 had no drift | All corrected to 09. README now says S1–S13 |
| 1b | flow.json | Fight-node labels and refs already matched 09. But five after-midnight nodes (`kd-*`) described the old draft (Corval carried off, the coast relief taken, Essin arrested, Phern cutting to the gardens), two edge labels still said "the relief", `ihb-snakefed` and `gate-void` were stale, three clocks (bench, noise, fire) used the old "any hard miss" triggers, and two edges were duplicated | Nodes, edges, clocks rewritten to 05/09; duplicates removed; `oraga_night_flow.html` regenerated with `build_flow_page.py` |
| 2 | The Wept's bloodied phase | 05 and 10 already agreed (Fracture DC 15 whatever tells, once bloodied) | Tidied 05's sentence only |
| 3 | Gate void-contract DC | 05 said DC 13, DC 10 with the case proven. 09 S3: DC 13 to the sergeant, no check to the captain — internally consistent | 05 now matches 09 (and says "in front of the sergeants", as 09 does). Flow `gate-void` updated |
| 4 | Heat/clock rules | 04 (Thenya heat 3+) and 05 (0–2 out / 3–4 act) matched 09. 08's tracker was a different design (Scheme/Tell/Escalation/Midnight boxes, no heat, old cards) | 08 Table VIII–7 rebuilt as 09's heat tracker (start values, rises with automatic ones marked, falls, 0–2/3/4 rule). 09's own Circle row fixed: S7's clock sets heat **to 4** (the card says so; the tracker had it as +1) |

## 2. General pass — issues found and fixed

**Cross-chapter rules drift**
- 08 crisis panel: crystal charges near an Uninvited were "60 ft, DC 13 Wisdom"; 05 and 10 say 30 ft, DC 13 Charisma. Ward range likewise 60 → 30 ft. Fixed.
- 08 Optional Steel clocks used "hard miss" triggers; 09 uses natural 1s, rounds and noise. Rewritten from 09, and the table now lists every card S1–S13 with its faction.
- 05 Phern door: "DC 13, DC 10 for a Phern or anyone who walked with him"; 09 S11: no check for those, DC 15 shouted for anyone else. 05 now matches 09.
- House Boranis at heat 3–4 pointed at S13, but S13 only fires when *Draunel's* heat is 3–4. Clarified in 09's tracker, 08's tracker and 05 Table V–2 (otherwise the cousins simply go into the fire with Vorlain).
- Veier's speed: 10 said 20 ft tonight, 05's Crossing says 15 ft. 10 now says 15.
- Corval, deceiving him about household matters: 07 DC 20, 10 DC 18. 10 now DC 20.
- 04 Mv I box gave Callun "the two" Hired Knives; 09 says she brought three. Now "the Hired Knives".
- 07 Draunel still said his three irons are "left to your invention"; now points to Chapter IX, which names them.

**DC ladder** — every DC outside stat blocks is 10/13/15/18/20/25 except S13's fire save (DC 12), now DC 13. Stat-block save DCs (12, 13, 14, 17) are PB + ability and stay.

**Encounter math** — every card's sum checked against SRD 5.2.1 (verified from the SRD PDF: 3rd level Low 150 / Moderate 225 / High 400; 2nd 100/150/200; 4th 250/375/500; 5th 500/750/1,100). Table IX–1 is correct. Every card sum is right; S5's table row said "Low" for 550 XP (under Low) — now "just under Low", as the card says. S1 (150), S6 (200) and S9 one-sided are deliberately far under Low and say so.

**Stat blocks** — every block checked for CR↔XP, PB, attack bonus = PB + ability, save DC = 8 + PB + ability, and HP = average hit dice + Con. All correct. One *Nastier* dial (Bought Sergeant) claimed +6 to hit at CR 4 with Str 15; now Strength 17, +5, 7 (1d8 + 3).

**Names and references** — every bolded stat-block name in 01–09 exists in 10 by exact name (plurals only). Every chapter/section cross-reference checked (Table I–1, *Knives in the Dark*, *The Gatehouse Court, Held*, *The Other Thieves*, *Items of the Night*, *The Night's Loot*, *The Palace on Alert*, the ⟨If History Breaks⟩ sidebars, B0–B13) and resolves.

**Pregens (11)** — HP, AC, initiative, saves, every skill total, attack bonuses, spell DC/attack, slots (4/2), cantrip and prepared counts (6 each for bard, cleric, wizard at 3rd), Andra's lattice (6 + 2 + 2 + 2 Evocation Savant = 12 spells), and every class feature checked against SRD 5.2.1. All correct as written; no changes.

**INVENTIONS_5e.md** — rebuilt as one numbered table (41 rows). Merged duplicates the drafters had logged separately (the Church's filing, the Phern door, S12, Draunel's irons, the Thenya rope and S10 location, Veier's flare, retinue sizes). A "Review these first" list heads the file. No new inventions were added by this pass.

**README** — contents table lists every file including 09, 10, 11 and `flow/` (now naming the build script and saying never to hand-edit the HTML). SRD 5.2.1 CC BY 4.0 attribution is present, verbatim.

**Owner rulings** — all intact: no mandatory fight (S3's gate is unavoidable, its fight is not, and the text says so); every fight visible; the Radiant can't be turned and guilt never ends the hunt (05, 10); Tavva's crew is the one flatly winnable fight; the Bought hold the gate; the midnight attack is the Uninvited's alone (09, 05, 04 all say so); Raunu dies by his own choice; everyone is human; no books (wizard lattice, no scrolls); *What the Module Never Says* is held, including against spells. "Mirror Master (MM)" throughout; no "DM" or "GM" anywhere.

## 3. SRD 5.2.1 verification

Verified directly against the SRD 5.2.1 PDF (`media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf`, text-searched):

- Classes/subclasses: Bard (College of Lore), Cleric (Life Domain), Fighter (Champion), Rogue (Thief), Wizard (Evoker) — all present.
- Feats: Alert, Magic Initiate, Savage Attacker, Skilled — present. Level 4 ASI allows "another feat of your choice for which you qualify", so *Magic Initiate at 4th level* (03, 06) is legal.
- Human traits Resourceful / Skillful / Versatile, and class features used on the sheets (Cutting Words, Jack of All Trades, Thaumaturge, Divine Spark, Preserve Life, Disciple of Life, Tactical Mind, Remarkable Athlete, Steady Aim, Fast Hands, Second-Story Work, Ritual Adept, Scholar, Evocation Savant, Potent Cantrip) — present.
- Every spell named in the module is in the SRD: the pregens' lists; the gift cantrip list; and the ones the text answers (*banishment, calm emotions, charm person, command, commune, counterspell, darkness, detect evil and good, detect thoughts, disintegrate, dispel magic, disguise self, dominate person/monster, flesh to stone, hideous laughter, hold person, hold monster, identify, knock, legend lore, message, plane shift, polymorph, power word kill, sleep, speak with dead, suggestion, thaumaturgy, wall of force, zone of truth, arcane lock*).
- Jeweler's tools, gaming set, disguise kit, thieves' tools, vehicles (land) — present.
- XP budget and CR/XP/PB tables — match the book.

**Unverified:** nothing the module depends on. No card tells the MM to "use the SRD X block"; every creature is a custom block in Chapter X.

## 4. Remaining owner questions

1. **The testament's witnesses.** 01's opening vignette has two paid witnesses "not seen since Tuesday"; 04 Undercurrent B and 06 have Corval and Mother Sella as the witnesses. Both come from the source text. Which is canon, or are both true (two sets)?
2. **Sixty or eighty servants.** Corval's gate question in 07 says "there used to be sixty of you"; 04 Undercurrent B says eighty left. Also from the source. A guest's wrong guess, or a number to fix?
3. **The Palace on Alert vs S4.** 04 says four guards converge within 2 rounds; S4 runs two guards plus four more after *Call the House*. Both work at the table; say if you want one number.
4. The **Review these first** list at the top of `INVENTIONS_5e.md` — especially #2 (cousins from 3160), #9 (Callun learns of a possible heir), #13 (Essin's bodies as a bargaining chip) and #17 (the Uninvited's CR and type).
5. 02 states as MM truth that Veier will not survive the night. That is carried from the source and untouched; flagged only because the 5e edition gives her a stat line and a Speed.
