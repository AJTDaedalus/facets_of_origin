# Official-Style Audit — SNAKES slice (`09_The_Snakes.md`)

*2026-09-30. Auditor: SNAKES. Scope: `conversions/dnd5e/oraga_night/09_The_Snakes.md`
(1,756 lines, about 19.6k words): the faction threat lines, the Snake Tracker, and fight
cards S1–S14. Yardsticks: `docs/RESEARCH_5e_module_conventions_structure.md` (C-S) and
`docs/RESEARCH_5e_module_conventions_voice.md` (C-V, S). Context read: BRIEF, both
FIXPLANs, the tail of LOG pass 2, the prior audits, and INVENTIONS_5e.md. Read-only: no
module file was edited.*

**Party baseline: four 4th-level characters** (owner ruling, FIXPLAN §6; the night ends at
5th), per the coordinator's correction. Every budget, difficulty claim and DC judgment
below is made against four 4th-level characters, using 2014 DMG thresholds (Easy 500 /
Medium 1,000 / Hard 1,500 / Deadly 2,000 for the party, with the group multiplier). The
one 3rd-level column in SNAKES-7 is not a baseline. It only checks each card's own
printed "Four at 3rd level" scaling line.

---

## 1. Summary

### Verdict per dimension

| Dimension | Verdict |
|---|---|
| **CONTENT** | **Strong.** The faction presentation is closer to official practice than most of the module. Each line has a Movement-by-Movement escalation table with a visible tell, a "walk into it / turn it / snake on snake" block, and an "at dawn" consequence. Together these match the RoT council's per-faction follow-up and scorecard (C-S17) and the AL social-tier-to-combat pattern (C-S38). Canon holds: R6 (the heir) is respected everywhere in 09, and the canon beats are intact (Vorlain's hero turn, Maiven going east, the Bought as the only purchasable foe). Three gaps: the tracker is not the complete index it claims to be, heat 4 is undefined for three cards, and two boxes put in figures that the GM text never names. |
| **MECHANICS** | **Sound but not run-at-a-glance in places.** Every referenced stat block and trait exists in 10. Every card's XP sum and every scaling sum re-derives correctly against SRD 5.2.1. DCs sit on a sane 10/13/15/18 ladder. The problems are rule seams: heat 4 does nothing on S8, S11 and S13; the morale trigger "first real wound" is undefined and contradicts S7's own Bloodied line; walk-away outs pay full card XP (S4 pays 1,350 for leaving, S14 up to 3,900); no card states surprise or detection terms, and three boxes hard-code the party being seen; the card Inspiration awards break Chapter I's "reminder, not extra" rule. At a 2014 table, the multiplier math puts every "Low" card at Medium to Deadly. |
| **PROSE** | **Good rhythm, un-official address.** Sentence mean 15.2 words (median 13), 8.8% over 30 words, so C-V4 passes. The deviations are "player character" used 74 times against 0 uses of "the characters" (C-V2), about 20 places where DM prose addresses the players as "you" (C-V1), and a leftover narrator voice ("the module would prefer…", "Honest note", "with a straight face", "without comment"). Several A-16 AI-rhythm tics are still in the text. |
| **STYLING** | **Consistent house format, a few official conventions missed.** Every box has a trigger (C-S19) and every box runs 50–75 words (C-S22). The card field order holds. The misses: 25 of 33 DCs drop the word "check" (C-V15), 28 pointers read "(Chapter X)" instead of "(see chapter X)" (C-S41), and 11 distances are spelled out in GM prose. Treasure is only a pointer to Chapter X (C-S45). "Walk into it / Turn it / Snake on snake" run together as one paragraph of 130–210 words six times. |

### Top 5 issues

1. **SNAKES-1** — Heat 4 ("clock one segment filled, or Nastier") is a no-op or undefined on S8-in-the-dark, S11 and S13, and ambiguous on S13 (whose Nastier?).
2. **SNAKES-2** — The Snake Tracker is not the complete rise/fall index: four card Developments change heat on triggers the table never lists, and two rises are ambiguous by default.
3. **SNAKES-4** — No card states surprise or detection terms (C-S33 [A]). The S2, S8 and S10 boxes end with the party already spotted, which removes the stealthy approach.
4. **SNAKES-5** — Walk-away outs pay the whole card's XP (S4 "go back the way you came" = 1,350; S14 "stop interfering" = up to 3,900).
5. **SNAKES-7** — At 2014 tables, the SRD 5.2.1 no-multiplier budgets read two bands soft. Nothing in the book warns a 2014 MM, so they will "correct" the cards or distrust the labels.

**No P1 findings.** Nothing in this slice breaks play outright. The P2s are seams an MM hits mid-scene.

---

## 2. Findings

### SNAKES-1 [P2] Heat 4 is a no-op on three cards, and ambiguous on a fourth (MECHANICS)
- **Where:** 09:469–471 (the heat-4 rule); S8 *In the dark* 09:1162–1167; S11 09:1381; S13 09:1514–1515; S12 09:1458–1459; 10:630, 10:849, 10:1272.
- **Yardstick:** C-S13 [A] (every event beat has a clear timing rule); C-V24 (adjustments are concrete deltas).
- **Problem:** Heat 4 says the card starts "with its clock one segment filled, or with the foes' **Nastier** line in play (MM's choice)." Pass 2 (INVENTIONS #54) moved several Nastier lines into the base rosters, so:
  - **S8 in the dark:** "The clock is gone", so there is no clock to fill. The Warden Nastier (a fourth warden inside) is already in the base roster. Both options do nothing.
  - **S11:** the base roster is already three bodyguards, and 10's Phern Bodyguard Nastier still reads "A third bodyguard…" (10:1272; Steel's request S-3 was not applied in 10). The Nastier option does nothing.
  - **S13:** one duelist already has the Duelist Nastier. It is unclear which Nastier heat 4 means. Draunel's own Nastier (10:849) adds "two duelists who have watched Vorlain all night", which would take the card to 1,750 XP, and the card never budgets that.
  - **S12** handles heat 4 correctly (a fourth knife, 800 XP). It is the model the others should follow.
- **Fix:** Replace the generic heat-4 sentence with a per-card line, and put that line on each card under *Enemies*:
  - 09:469–471 → "**4: it happens with steel already out.** Each card says what heat 4 changes (the line *At heat 4* under its Enemies)."
  - S8 dark: "*At heat 4:* the wardens are already on the stair when the party arrives, and the drawer is halfway down it; the out *Fetch Kovaun* is gone (she is in the dark Court)."
  - S11: "*At heat 4:* the crush clock starts with one segment filled."
  - S13: "*At heat 4:* the gallery clock starts with one segment filled." Do not add Draunel's Nastier, because two more duelists push it over High.
  - In 10 (BESTIARY owner), change the Phern Bodyguard Nastier to S-3's wording. [not portable]

### SNAKES-2 [P2] The Snake Tracker misses heat changes that the cards make (MECHANICS / STYLING) [d20-portable]
- **Where:** Table IX–2, 09:443–452, against the card Developments at 09:983 (S6), 09:1184 (S8), 09:1275–1278 (S9); the rises at 09:449–450.
- **Yardstick:** C-S17 [S] (the RoT scorecard lists every event that moves a faction); the slice brief asks whether the tracks run at a glance.
- **Problem:** The tracker is billed as the thing to "read the whole row at midnight". But four heat changes live only in card text:
  - S6: "A cousin beaten in public is a House Boranis heat box ticked" (not a Boranis rise).
  - S8: "If the wardens were turned back, the Church's heat falls by one" (not a Church fall).
  - S9: "If the clock filled, both houses' heat rises by one" (not a rise for either house).
  - S9: Draunel's heat falls if he is shamed. The tracker has "embarrassed in front of guests", so this one is covered.

  Two listed rises also misfire by default:
  - Draunel, "Agenda 3 refused or failed": does that count when no player character carries Agenda 3?
  - Boranis, "Vorlain baited or got drunk in public": canon has Vorlain drinking in Movement IV (09:314), so this could tick with nobody acting. The "If the table does nothing" paragraph (09:454–460) assumes it does not.
- **Fix:** Add to Table IX–2 (and mirror in 08 Table VIII–7, which is NIGHT's file):
  - Boranis *Rises*: "a cousin beaten in public (S6) · S9's clock filled".
  - Church *Falls*: "−1 if the wardens are turned back at the study door (S8)".
  - Draunel *Rises*: "S9's clock filled".
  - Reword "Agenda 3 refused or failed" → "Agenda 3, if a player character carries it, refused or failed".
  - Reword "Vorlain baited or got drunk in public" → "Vorlain baited, or got drunk, by a player character".

### SNAKES-3 [P2] Morale trigger "the first real wound" is undefined, and S7 contradicts itself (MECHANICS)
- **Where:** 09:1035 ("the knives break at the first real wound") against 09:1057 ("break the moment the first of them is Bloodied"); 09:1248 (S9 duelists); 09:1548 (S13 duelists); 10 Draunel Duelist *Breaks* (the same phrase).
- **Yardstick:** C-S34 [U] (a morale or stop condition an MM can apply); structure §6.2 (flee thresholds are stated as rules).
- **Problem:** "Real wound" could mean any damage, Bloodied, or a critical hit. In S9 and S13 the answer decides whether a duel ends on the first hit or runs three rounds. S7 gives two different triggers for the same knives, one in the budget line and one in Morale.
- **Fix:** Pick one trigger. The shortest faithful choice: "The duelists break the first time one of them takes damage" (S9/S13; this fits "honour bleeds first"). S7 then reads 09:1035 → "…because the knives break when the first of them is Bloodied; …". Mirror the change in 10's Duelist *Breaks* (BESTIARY).

### SNAKES-4 [P2] No card states surprise or detection, and three boxes hard-code being spotted (MECHANICS / STYLING)
- **Where:** All fight cards (a grep of 09 for surprise and Stealth finds only the two terrain notes at 09:577 and 09:1236). The boxes: S2 09:625–627 ("looking back down the corridor at you"), S8 09:1102–1103 ("has turned his head toward you"), S10 09:1294–1295 ("now she is watching you").
- **Yardstick:** C-S33 [A] (every fight states surprise and detection terms); C-S21 [A] (a box contains no outcome the players haven't earned); C-S23 [U] (a box that assumes something says so).
- **Problem:** S2, S7 (Movement V) and S8 are exactly the scenes a rogue or wizard wants to creep up on. As written, the box decides the approach failed. The MM has no DC and no rule for what a quiet approach buys, whether surprise, a free clock segment or a better out.
- **Fix:** Add one detection line after each of those three boxes, and one to S7's Movement V box:
  - S2: "The box assumes the characters come down the corridor openly. If they came quietly, they make a DC 13 group Dexterity (Stealth) check contested by Tavva's passive Wisdom (Perception). On a success, drop the box's last two sentences: the crew is surprised, and the noise clock starts empty whatever happens in the first round."
  - S8: "…contested by the wardens' passive Wisdom (Perception); the corridor's Darkness gives the characters advantage."
  - S10: "…the slinger at the corner has a passive Wisdom (Perception) score of N (see chapter X)." Put the real number from the block in place of N.
  - For the open cards (S1, S3, S6, S9, S11, S13, S14), one line in *Running the Snakes*: "Unless a card says otherwise, nobody is surprised: every fight in this chapter starts in plain view." [the prose part is d20-portable]

### SNAKES-5 [P2] Walk-away outs pay the whole card's XP (MECHANICS)
- **Where:** 09:100–101 ("Ending a fight by an out pays the card's XP"); S4 09:865 with 09:872 ("Going back the way you came" / "1,350 XP for any out"); S14 09:1725–1727 with 09:1736 ("Stop interfering" / "3,900 XP, however it is got out of the way"); S2 "Let her go" 09:670; S5 "Let them go" 09:905; S6 "Walk away" 09:969. Table I–4 in 01 (FRONT's file) sets the same rule.
- **Yardstick:** C-S47 [U] (clever and social wins are paid); voice §10–11 (AL pays non-combat XP for *accomplishing* a task, never for leaving one).
- **Problem:** Paying outs is right; it is the module's philosophy and it is decided. But an out that resolves nothing now pays the same as one that resolves the scene. A party that bumps the honor guard and backs off earns 1,350 XP, about a third of what the module gives for the whole night. S14 is worse: provoke the Attendant, step back, and collect 3,900. At 4th level that is half a level for doing nothing. The rule only matters for tables that track XP (milestone is the default), so it is P2, not P1.
- **Fix:** In *Running the Snakes*, after "Outs are the section to read twice": "An out that ends the scene with the characters simply leaving (*let her go*, *walk away*, *go back the way you came*, *stop interfering*) pays nothing." Mark those bullets on each card with "*(no XP)*". S14's Rewards line becomes: "3,900 XP when its focus is broken four times, it is driven to 0 Hit Points, or its orders are argued away." Cross-file: FRONT should add the same clause to 01 Table I–4.

### SNAKES-6 [P2] The card Inspiration awards break Chapter I's "reminder, not extra" rule (MECHANICS)
- **Where:** 09:110–113; S3 09:825–826 ("to whoever held the wicket when it counted"); S9 09:1264–1266 ("to whoever answered Essin"); S8 09:1169 ("to whoever keeps the slate readable"); S13 09:1564–1565. Against 01:209–210 ("A fight card … that prints Inspiration is a reminder of one of these rows, not an extra award") and 01 Table I–3.
- **Yardstick:** C-S44 [A] (awards are printed where earned, and they agree with the model stated in the intro).
- **Problem:** Table I–3's rows are: an agenda completed, a pattern said out loud, a fight ended by an out, a companion hauled up, the Attendant distracted, and somebody carried out. Holding the wicket in a fight, answering Essin, and keeping the slate readable by fighting match none of them. Either 01's rule is wrong or these awards are. The MM finds out mid-session.
- **Fix:** Tie each card's award to a row, for example "*Heroic Inspiration* (Table I–3, *a fight ended by an out*): to whoever voided the contract." Then:
  - S3: cut the wicket fallback.
  - S9: keep "to whoever ended it with no blade drawn" and cut "answered Essin". Or ask FRONT to add a Table I–3 row, "a snake's leader helped when they asked".
  - S8: make it "to whoever keeps the slate readable by an out".
  - S13: make it "to whoever got Vorlain back into the gallery without a fight".

### SNAKES-7 [P2] At a 2014 table the budgets read two bands soft, and the book doesn't warn the MM (MECHANICS)
- **Where:** 09:82–92, Table IX–1 09:115–123, Table IX–3 09:498–515, and each card's *Budget* line.
- **Yardstick:** voice §12 (encounter difficulty row: "don't mix vocabularies… optionally give the 2014 equivalent"); C-V24 [A]; BRIEF §1 ("compatible with 2014 5e tables").
- **Problem:** The book uses SRD 5.2.1 sums with no multiplier, and says so (09:82–83). That is a decided choice, and its labels are simulation-checked (INVENTIONS #54). But a 2014 MM who re-checks a card with the DMG multiplier sees a Deadly fight labelled "Low". That MM will then cut foes (weakening the card) or stop trusting every label. The gap is large. Computed with 2014 DMG thresholds (four at 4th: Easy 500 / Medium 1,000 / Hard 1,500 / Deadly 2,000; four at 3rd: 300 / 600 / 900 / 1,600) and multipliers (×1.5 for 2 foes, ×2 for 3–6, ×2.5 for 7–10):

  | Card | Book label (4th) | Raw XP | Foes | 2014 adjusted, four at 4th | 2014 band (baseline) | Check of the card's own "four at 3rd" scaling line only (2014: 300/600/900/1,600) |
  |---|---|---|---|---|---|---|
  | S1 | trivial (200) | 200 | 8 | 500 | Easy | 150 ×2 = 300 → Easy |
  | S6 | under Low | 600 | 3 | 1,200 | Medium | 300 ×2 = 600 → Medium |
  | S2 | under Low | 600 | 4 | 1,200 | Medium | 600 ×2 = 1,200 → Hard |
  | S5 | under Low | 600 | 4 | 1,200 | Medium | 550 ×2 = 1,100 → Hard |
  | S11 | under Low | 625 | 4 | 1,250 | Medium | 625 ×2 = 1,250 → Hard |
  | S12 | Low (heat 3 / 4) | 600 / 800 | 3 / 4 | 1,200 / 1,600 | Medium / Hard | 400 ×1.5 = 600 → Medium |
  | S7 | Low | 800 | 4 | 1,600 | Hard | 600 ×2 = 1,200 → Hard |
  | S8 | Low | 800 | 4 | 1,600 | Hard | 600 ×2 = 1,200 → Hard |
  | S9 (Draunel side / both) | Low | 850 / 1,150 | 3 / 6 | 1,700 / 2,300 | Hard / Deadly | 600 ×2 = 1,200 → Hard |
  | S10 | Low | 1,000 | 4 | 2,000 | Deadly (at threshold) | 900 ×2 = 1,800 → Deadly |
  | S4 | Moderate | 1,350 | 3 | 2,700 | Deadly+ | 900 ×1.5 = 1,350 → Hard |
  | S13 (Draunel side) | Moderate | 1,350 | 3 | 2,700 | Deadly+ | 900 ×1.5 = 1,350 → Hard |
  | S3 (without / with captain) | Moderate / over High | 1,500 / 2,600 | 5 / 6 | 3,000 / 5,200 | Deadly ×1.5 / ×2.6 | 850 ×2 = 1,700 → Deadly |
  | S14 | Deadly / High | 3,900 | 1 | 3,900 | Deadly ×2 | CR 8 at 210 HP → Deadly ×2.4 |

  Table IX–1's 5.2.1 figures are all correct (checked: 3rd 150/225/400, 4th 250/375/500, 5th 500/750/1,100 per character). Every card sum and scaling sum re-derives correctly.
- **Fix:** One MM Note in *Running the Snakes* after 09:92: "**At a 2014 table.** The 2014 guide's group multiplier rates most of these cards one or two bands harder than printed. It counts heads, and these heads break early, fight to detain and quit on a clock. Trust the printed label. It comes from play, not from the sum." Optionally add a column "2014 adjusted XP" to Table IX–3 using the figures above. Do not change any roster. [not portable]

### SNAKES-8 [P2] "Deadly" mixes the 2014 vocabulary into a 5.2.1 budget line (MECHANICS / STYLING)
- **Where:** Table IX–3 S14 09:511; S14 *Budget* 09:1623–1629.
- **Yardstick:** C-V24 [A] (one edition's vocabulary per line); S34.
- **Problem:** SRD 5.2.1 has only Low, Moderate and High. "Deadly" is the 2014 DMG term. The card explains it ("nearly twice High… is what 'Deadly' means here"), but the explanation is itself the tell that the word comes from outside the system. A 2014 reader will read it as 2014 Deadly, which S14 also is (see SNAKES-7), so the label is accidentally right there and confusing everywhere else.
- **Fix:** 09:511 → "3,900 XP — nearly twice High while Focused; High while Idle". 09:1623 → "*Budget:* **beyond High while Focused; High while Idle.**" Then 09:1627: "…3,900 XP is nearly twice High for four 4th-level characters (2,000)." Delete "which is what 'Deadly' means here". Mirror in 10's S14 block header line (BESTIARY). [not portable]

### SNAKES-9 [P2] 04's Movement V box gates S10 on Thenya heat 3; the card fires whatever the heat (MECHANICS / CONTENT)
- **Where:** 04:1318–1321 ("If nobody stops them — and the Thenya's heat is 3 or more…"); 09 S10 09:1284–1303 (the clock "Advances at the end of each round, whatever anyone does"); 09 Mv V row 09:405; Table IX–2 09:452.
- **Yardstick:** C-S13 [A] (each event beat has a timing rule and a prevention condition).
- **Problem:** At heat 1–2 (for example, a player character promised to go with Maiven, −1) 04 says the rope stays coiled, but S10 still runs its half-bell clock. At heat 0, 09's Development says Maiven "does not climb", while the card's trigger and clock never check heat.
- **Fix:** Add to S10's *Where and when* (09:1284–1286): "Only if the Thenya's heat is 3 or more at the half-bell; at 0–2 the slingers coil the rope and go back to Maiven, and this card does not fire." Also change Table IX–2's last-column header to "What heat 3–4 sets off" so S10's Movement V timing isn't filed under "At midnight". [d20-portable]

### SNAKES-10 [P2] DM prose addresses the players as "you", and "player character" crowds out "the characters" (PROSE) [d20-portable]
- **Where:** "you/your/yourselves" in non-box prose meaning the characters, about 20 times: 09:366, 592, 672, 711, 865, 869, 942–946, 963, 966, 973, 1062, 1065, 1114, 1261, 1374–1375, 1554, 1609. "Player character(s)" appears 74 times and "the characters" 0 times. "The player(s)" meaning the characters: 09:312, 09:909. The imperative *Walk into it* blocks ("Follow the coat. Be in the service doorway…", 09:161 and the same pattern at 215, 271, 318, 365, 408).
- **Yardstick:** C-V1 [A] ("you" means only the DM); C-V2 [A] ("the characters" is the default, "PCs" and "player characters" are not used in prose, and "the players" means real people only); S2.
- **Problem:** Official prose never talks to the party outside read-aloud. The mixed "you" also makes some lines ambiguous for the MM. In "Losing costs the east wing… and your invitation's good standing" (09:869), it is unclear whether "your" means the MM or the party. The 74 uses of "player character" read as rules-text, not module prose. The pattern is probably module-wide, so FRONT should rule once.
- **Fix:** Two options. (a) Declare the device once in *Running the Snakes*: "*Objective* and *Outs* are written so you can read them straight to the table." Then leave them, and fix only the stray "you"s elsewhere (09:366, 09:672, 09:869). (b) Convert them to the official voice, for example:
  - 09:942 "walk back inside with your dignity" → "the characters walk back inside with their dignity";
  - 09:865 "Going back the way you came" → "Going back the way they came";
  - 09:161 "Walk into it. Follow the coat." → "**Walk into it.** The characters can follow the coat, …".

  Either way, change "a player character" to "a character" where it is a subject (most of the 74), and "the players' proof" (09:909) to "the characters' proof".

### SNAKES-11 [P2] Narrator voice and AI rhythm still present (PROSE) [d20-portable]
- **Where:** Still open from AUDIT_oraga_5e_canon A-16:
  - 09:321 "a debt of a very particular kind";
  - 09:765 "A second leader is a cliff, not a step";
  - 09:350–351 "they are the most frightened armed people in the palace, and the only ones facing the right way".

  New or also present:
  - 09:21 "which is worse";
  - 09:33–34 "Let the table sit with it.";
  - 09:330 "the source notes with a straight face";
  - 09:386 "The module would prefer somebody competent went with her.";
  - 09:637 "It is the whole scene.";
  - 09:645 "*Honest note:*";
  - 09:800 "*Honest warning:*";
  - 09:855 "That is the point.";
  - 09:902–903 "which, at this hour of this night, is not nothing";
  - 09:918–919 "the module notes, without comment, which kind of night the table chose to have".
- **Yardstick:** C-V13 [A] (no winks, no meta-commentary, humor only as a deadpan informational line); structure §4 (no designer-note voice in the body); memory rule (no epigram closers or "not X, Y" pairs).
- **Problem:** Each line is small. Together they give 09 a narrator who comments on the book ("the module would prefer", "honest note"). No official module has that voice. Several are also the epigram closers the house rule bans.
- **Fix (light touch, same meaning):**
  - 09:21 "…and need him, which is worse." → "…and need him."
  - 09:33–34 → cut "Let the table sit with it."
  - 09:321 "which is a debt of a very particular kind: he knows…" → "and Essin pays his debts. He knows…"
  - 09:330 "He is, the source notes with a straight face, the only patron…" → "He is also the only patron…"
  - 09:350–351 "…they are the most frightened armed people in the palace, and the only ones facing the right way." → "…they are frightened, armed, and facing the right way."
  - 09:386 → "Unless a capable character goes with her, she dies there."
  - 09:637 → cut "It is the whole scene." (the preceding bold already says it)
  - 09:645 "*Honest note:* the party will very likely win…" → "The party will very likely win…"
  - 09:765 "A second leader is a cliff, not a step, and it is the most reliable way…" → "A second leader doubles the danger at once, and it is the most reliable way…"
  - 09:800 "*Honest warning:* fought to the last…" → "Fought to the last…"
  - 09:855 cut "That is the point."
  - 09:902–903 "…the party's opinion of themselves — which, at this hour of this night, is not nothing." → "…the party's opinion of themselves."
  - 09:918–919 "— and the module notes, without comment, which kind of night the table chose to have." → cut after "clean".

### SNAKES-12 [P2] Treasure is a pointer, not itemised where it is found (STYLING / MECHANICS)
- **Where:** S2 09:680–682; S3 09:826–827; S7 09:1074; S8 09:1170–1171; S5 (no loot line, though 10 lists Tavva's sack for S5). The values live in 10 *The Night's Loot* (10:1939–1965).
- **Yardstick:** C-S45 [A] (treasure itemised in place with gp values and provenance); C-V25.
- **Problem:** At the moment of looting the MM has to flip to Chapter X for a number. Official modules print the value on the spot.
- **Fix:** Inline the value and keep the pointer:
  - S2: "*Treasure:* the crew's rope, sacking and shuttered lantern; if Tavva is caught, her sack (worth 2d6 × 25 gp to a fence) and any unspent charges (see chapter X, "The Night's Loot")."
  - S3: "…the company's purse (3d6 × 10 gp in old coin)."
  - S7 and S12: "each knife's advance (2d6 gp)."
  - S5: add the same line as S2.

  Rename the run-in *Loot* to **Treasure** to match the official label. Match the case (GP or gp) to the module-wide choice; 09:1065 uses "20 GP". [label d20-portable; values not]

### SNAKES-13 [P2] "Walk into it / Turn it / Snake on snake" run together as one long paragraph (STYLING) [d20-portable]
- **Where:** 09:161–174 (209 words), 09:215–225 (160), 09:271–282 (168), 09:318–327 (143), 09:365–373 (129), 09:408–414.
- **Yardstick:** C-V5 [U] (paragraphs of 45–75 words, over 120 only in background); structure §7 (run-in labels each begin their own paragraph); the brief's run-at-a-glance test.
- **Problem:** These three blocks are the ones the MM reaches for mid-scene: how the party gets in, how to defuse, how to set one snake on another. Merged into one paragraph, the second and third labels sit mid-line and are hard to find.
- **Fix:** Start each bold label on its own paragraph. No wording change.

### SNAKES-14 [P3] 25 of 33 DCs drop the word "check" (MECHANICS / STYLING)
- **Where:** For example 09:590, 591, 862, 867, 964, 1065, 1068, 1069, 1152, 1154, 1254, 1256, 1258, 1260, 1318, 1337, 1339, 1407, 1465, 1510, 1555, 1558, 1561; also S3 09:820, 09:361 (table cell).
- **Yardstick:** C-V15 [A] ("DC N Ability (Skill) check"); voice §6. Also: alternatives across abilities are written with both DCs.
- **Problem:** Readable, but the forms are inconsistent within the chapter ("DC 13 Charisma (Persuasion)." next to "DC 13 Strength (Athletics) check"). At 09:1152, "DC 15 Intelligence (Religion) or Charisma (Persuasion)" drops the second ability's DC.
- **Fix:** Add "check" throughout ("DC 13 Charisma (Persuasion) check"). 09:1151–1152 → "a DC 15 Intelligence (Religion) or DC 15 Charisma (Persuasion) check". [not portable]

### SNAKES-15 [P3] Cross-references read "(Chapter X)"; the official form is "(see chapter X)" (STYLING) [d20-portable]
- **Where:** 28 parenthetical "(Chapter …)" pointers, for example 09:557 "(Chapter X)", 09:639, 09:827, 09:1618. Only one "(see …)" in the chapter.
- **Yardstick:** C-S41 [A]; C-V22.
- **Fix:** "(Chapter X)" → "(see chapter X)". A named section → '(see chapter V, "Down, Not Out")'. Keep the Roman numerals.

### SNAKES-16 [P3] CR in running prose; leaders not bold at first mention in the Six Lines (STYLING)
- **Where:** 09:145, 192, 242, 297–298, 344, 388 (e.g. "Callun (CR 1/4) and three **Circle Hired Knives** (CR 1)").
- **Yardstick:** C-V24 (CR appears only in stat blocks and budget lines); C-S27 [A] and C-S32 [A] (the stat-block name is bold at first mention, with a location pointer).
- **Fix:** "Callun (CR 1/4) and three **Circle Hired Knives** (CR 1)" → "**Rhaza Callun** and three **Circle Hired Knives** (see chapter X)". Apply the same change to the other five *Who they brought* lines. If the CRs are kept for prep, move them into Table IX–3's *Who* column. [bolding portable, CR not]

### SNAKES-17 [P3] Edition-term consistency: advantage in lowercase next to capitalized 5.2.1 terms; "Utilize" (MECHANICS)
- **Where:** Lowercase "advantage/disadvantage" at 09:578, 652, 774, 1133, 1236, 1673; "Disadvantage" at 09:1628. Every other rules term in 09 is capitalized (Prone ×6, Dim Light ×4, Difficult Terrain ×4, Heavily Obscured ×3, Half Cover ×3). "Utilize action" at 09:716 and 09:725.
- **Yardstick:** C-V26 [A] (one capitalization scheme); voice §12 (actions row: where the 5.2.1 name differs, describe the act).
- **Fix:** Capitalize Advantage and Disadvantage (5.2.1 scheme), or lowercase the lot; one scheme, agreed with BESTIARY. 09:716 "lifting it is a Utilize action" → "lifting it takes an action"; 09:724–725 "can be searched through the grille with a Utilize action" → "…with an action". [not portable]

### SNAKES-18 [P3] Save and damage phrasing off the SRD template (MECHANICS)
- **Where:** S13 fire 09:1529–1530 ("takes 2d6 Fire damage (DC 13 Dexterity saving throw for half)"); S11 crowd 09:1389 ("take 1d6 Bludgeoning damage").
- **Yardstick:** C-V18 [A]; C-V19; S10; S11.
- **Fix:**
  - 09:1529–1530 → "A creature that enters the fire or starts its turn there must make a DC 13 Dexterity saving throw, taking 7 (2d6) Fire damage on a failed save, or half as much damage on a successful one."
  - 09:1388–1390 → "…or have the Prone condition and take 3 (1d6) Bludgeoning damage…"

  Falling damage (09:575, 731, 773, 959) may keep bare dice, as the SRD does for falls. [not portable]

### SNAKES-19 [P3] Distances spelled out in GM prose (STYLING)
- **Where:** 09:574 "twelve-foot drop", 721 "five feet wide", 727 "fifteen feet above", 731 "fifteen-foot drop", 734 "ten feet out", 958 and 1233 "ten-foot drop", 1040 and 1391 "five feet wide", 1317 "twenty feet". Eleven in all.
- **Yardstick:** C-V (numerals for game quantities in GM text; words only inside boxes); S37.
- **Fix:** "12-foot drop", "5 feet wide", "15 feet above", and so on. [d20-portable]

### SNAKES-20 [P3] Scaling lines are not marked "not cumulative", and combinations aren't covered (MECHANICS)
- **Where:** Every *Scaling* block; the lead-in at 09:79–81.
- **Yardstick:** C-S36 [U] (an Adjusting the Encounter sidebar whose bullets are marked not cumulative); voice §10.
- **Problem:** Five characters at 5th level, or three at 3rd, are both real tables. The lines don't say whether to stack "five player characters" with "four at 5th level". Some lines stack by design (S2's 5th-level line says "as for five").
- **Fix:** Add to 09:79–81: "Use one line only; the lines are not cumulative. For five characters at 5th level, use the 5th-level line and add one of the weakest foes." Optionally rename *Scaling* to **Adjusting the Encounter** to match the official label. [not portable]

### SNAKES-21 [P3] Half-cards and two full cards miss fields the chapter promises (STYLING / MECHANICS)
- **Where:**
  - S4 (09:846–882): no Tactics, Morale or Terrain.
  - S5 (09:886–920): no Tactics or Morale, and "as in S2" is its only pointer.
  - S12 (09:1433–1481): no Tactics or Morale. S7 gives the same knives a Bloodied break, so the rule exists and is just not printed here.
  - S6 Development (09:983–985) covers only the party winning.
  - S14 Development (09:1754–1756) covers only the Attendant leaving.
- **Yardstick:** C-S34 [U] (tactics and morale on every fight); C-S35 [A] (Development covers the party losing, without a game over).
- **Fix:**
  - S12: "**Morale.** As S7: the knives break when the first is Bloodied, or on Callun's word."
  - S4: "**Tactics.** The guards grapple and escort; they draw only on bare steel. **Morale.** None needed; they are winning."
  - S6 Development, add: "If the cousins win, the character is walked back to the garden doors with a torn sleeve, and Essin hears of it; Boranis heat does not change."
  - S14 Development, add: "If the whole party is down, the Attendant finishes clearing the way and goes back to the edge of the light; Chapter V's history runs as written."

### SNAKES-22 [P3] Boxes introduce figures the GM text never names (CONTENT / STYLING)
- **Where:** S9 box 09:1202–1203 ("a man in a good coat is walking slowly between the two sides, speaking to each in turn"); S13 box 09:1496 ("another man is reaching for his knife").
- **Yardstick:** C-S21 [A] (the GM text after a box identifies what the box shows).
- **Problem:** In S13 the GM text implies Essin ("Essin and his cousins are about to stop them") but never says it. In S9 nobody is named, and the text says Draunel "will not set foot on the grass", so the figure isn't obviously him.
- **Fix:** S13, after the box: "The man reaching for his knife is Essin Boranis." S9: see NEEDS-RULING 3. Do not invent the figure.

### SNAKES-23 [P3] Card-level inconsistencies (MECHANICS)
- S7 Tactics (09:1052–1053) says "the other two slip past", but the card fields four knives. The fourth's starting position is never given (C-S51 [A], starting positions). Fix: "Two step in to hold the run while the others slip past; the fourth starts at the far door, waiting." (This locates him; it adds no new fact beyond "has been in the service run all night".)
- S2 and S5 at 3rd level disagree: S2 keeps all three knives at 3rd ("as printed", 09:689), while S5 drops to two (09:915). Either is defensible, but say why: "S5 comes after the characters have fought the Uninvited; one knife fewer."
- S13 at 5th level (09:1573–1574: "a third duelist… 1,800 XP") against 10's Draunel Nastier (10:849: "two duelists who have watched Vorlain"). One of the two needs to change (BESTIARY and SNAKES to agree).
- S2 09:642: "Tavva's two knives and her Sneak Attack" reads as her crew, the Gallery **Knives**. Change to "Tavva's two dagger attacks".
- S14 09:1731: "a distraction check of Intelligence or Charisma (Persuasion)" is malformed. Change to "an Intelligence (Investigation) or Charisma (Persuasion) check against the distraction DC".
- S14 09:1653: "rolls **d20 + the ability and skill**" → "makes an ability check with the skill that fits the trick" (S6 smell).

### SNAKES-24 [P3] Provenance citations point outside the 5e book (CONTENT / STYLING) [d20-portable]
- **Where:** 14 "(source Ch. …)" citations (e.g. 09:136–137, 184–185, 235–236, 257); the gloss at 09:131–132; "(Val'loh, V3)" at 09:190, a setting document that is not part of this book.
- **Yardstick:** C-S41 [A] (cross-references resolve inside the product); BRIEF §5 ("a 5e MM can run any scene from the page without the Facets books").
- **Problem:** The same-number chapters do exist in this edition, so most citations resolve. But "source" tells the reader there is another book they lack, and "V3" doesn't resolve at all.
- **Fix:** "(source Ch. VII, *Mistress Rhaza Callun*)" → "(see chapter VII)". Cut the "The words 'the source' mean…" sentence (09:131–132). "(Val'loh, V3)" → "(see chapter II)", or just cut the parenthetical, since the fact is stated inline.

### SNAKES-25 [P3] The chapter's physical card order doesn't follow the night; two section names collide (STYLING) [d20-portable]
- **Where:** Cards are printed S1, S2, S3 (Movement VII), S4, … S14, while Table IX–3 lists them in night order. S2 "Knives in the Dark" has the same title as 05's section "## Knives in the Dark" (05:694), and 09 points at both (09:618 for S2; 04 and 05 cite the 05 section). "The Snakes in the Pen" is both 09:15 and 04:439.
- **Yardstick:** C-S41 [A] (unambiguous cross-references); structure §2 (encounters sit where play reaches them).
- **Fix:** Rename S2 to something distinct, e.g. "S2. The Service Corridor Job". Keep 05's title, which more files cite. Optionally put the Movement in each card header ("S3. The Gate at Midnight (Movement VII)"). Leave the numbering alone, since every file uses it.

### SNAKES-26 [P3] Rewards line: say how the XP divides (MECHANICS)
- **Where:** Every *Rewards* line, e.g. 09:596 "200 XP", 09:824.
- **Yardstick:** structure §9.1 (LMoP form: "divide N XP equally among the characters"); earlier confusion over per-character vs per-party XP (AUDIT_oraga_5e_playability, the item at its line 570).
- **Fix:** "**Rewards.** 200 XP, divided equally among the characters." Say it once per card; the explanation at 09:100–101 can stay. [not portable]

### SNAKES-27 [P3] Simulation statistics printed in the body (STYLING) — a house choice, noted only
- **Where:** 09:87–92; the per-card lines "drops a player character in about one fight in twenty" (09:642–644, 760–761, 1036, 1226–1227, 1517); S14's simulation table and the parentheticals in its scaling lines (09:1634–1650, 1740–1752).
- **Yardstick:** structure §12 (no designer-note material in 5e bodies); C-S37 [A] (no difficulty apparatus in headers; these lines are in the body, not headers).
- **Status:** FIXPLAN §6 told the fixer to "report the numbers on the card", so this was decided. It is still un-official in feel. **Optional fix:** move S14's table and the percentage asides into one MM Note per card, headed "How it plays", so the card body reads like a module and the evidence stays one glance away.

### SNAKES-28 [P3] Redundancy with 01, 04, 05 and 08 — flagged only, for the owners of those files [d20-portable]
- **Where:**
  - The faction framing is written four times: 01 *The Snakes in the Chicken Pen* (01:226–318, with **four** rules), 04 *The Snakes in the Pen* (04:439–481, about 550 words), 09 *The Snakes in the Pen* (09:15–58, with **three** rules, "the same three Chapter IV runs them by").
  - The after-midnight beats appear twice: 05 *Knives in the Dark* (05:694 onward, about 2,160 words) restates 09's Movement VI–VII rows and the "What is happening" paragraphs of S8, S12 and S13.
  - The heat tracker appears twice: 08 Table VIII–7 and 09 Table IX–2.
  - 04 Table IV–1's "Movement V post" column (Draunel "B3", Boranis "B3, drinking harder") sits oddly with 09's Movement V, where both houses' people are on the B5 terrace. The principals may stay in B3, but 04 should say so.
- **Yardstick:** C-V14 (point, don't restate); pass-2 LOG's recommended cuts (the Six Lines, 04's section, 08 tracker "describe each line three times").
- **Fix (not mine to make):** Keep 09 as the single home. Cut 04's section to Table IV–1 plus one pointer sentence. Cut 05's section to Table V–7 plus pointers to the cards. Bring 01's four rules and 09's three into one list, or have 09 say "the rules in chapter I". 04's owner should reconcile the Movement V posts.

---

## 3. What already meets the official standard (keep it)

- **Faction presentation.** *What they came for / Who they brought / The line / Walk into it / Turn it / Snake on snake / At dawn* covers everything an official faction block does (RoT delegate format C: motive, what wins them, what alienates them, resources) and adds the RoT follow-up role through *At dawn*. Motives use plain verbs, and secrets are stated flatly to the MM (C-V10). Each faction's Movement table (scheme / what the party can see / card) works as a council "session" breakdown and is the best at-a-glance device in the chapter. Keep it.
- **The Snake Tracker as a scorecard (C-S17).** It has start values, marked automatic rises, and a documented default ("If the table does nothing…"). The default arithmetic re-derives correctly: Circle 2, Church 2, Draunel 2, Boranis 1, Phern 3, Thenya 3, which leaves only S11 live at midnight. The "heat is not a debt" and "five cards, one hour" MM Notes are sound table craft in the official Default / Dial / Cost shape.
- **Visible and optional (owner rule).** Every card fires on something the table sees happen to someone else, and every card has at least two non-kill outs. Social success changes later fights (Corro trust → S11 free out; Agenda 2 → S8 free out; Essin helped → S9 ally), which is the AL social-tier pattern, C-S38.
- **Canon.** R6 holds (S7's clock-full, 09:1022–1029; the Circle's *Turn it* and the tracker say only a player character can sell the nursery). *House Boranis hired none* is protected (the cousins are blood). The Bought are not a faction's hires. The Uninvited stay out of every snake card (09:517–522). No new names.
- **Boxes.** Every box has a GM trigger (C-S19), is second person and present tense, runs 50–75 words (C-S22), spells numbers out, and scripts a short line of NPC speech where it helps. The A-15 fixes (S2, S7, S11) are in.
- **Stat-block references.** Every bold creature in 09 exists in 10 by exact name. Every trait named in the cards (*A Quiet Word*, *Provocation*, *Seconds and Circles*, *Always Between*, *To the Terms*, *Second Clause*, *Clears the Way*, *Put Aside*, *Not Here*, *Call the House*, *Veil of Quiet*, …) resolves in 10.
- **Numbers.** Every card budget, every scaling-line sum and Table IX–1 re-derive correctly against SRD 5.2.1. The CRs match 10's blocks. DCs sit on 10/13/15/18 (all sane at 4th level). The S3 clocks (fire only on idle rounds, six-segment bell, captain at the third round) and the S3 battlefield (wicket, gate-walk, parley) implement R5 cleanly, and the morale line uses "or".
- **Mercy rules.** *Death before midnight* and the after-midnight crowd rule give every card a non-game-over route (C-S35), stated once and applied consistently (S1, S4, S13's fire).
- **Rhythm.** Sentence mean 15.2 words, median 13, 8.8% over 30 words, 38% under 10. That is in the official band (C-V4). There is no "we", no exclamation mark, no "Note that", and no hedging on canon.

---

## 4. NEEDS-RULING (for the owner)

1. **"MM" for "DM"** (14 uses in 09). Already raised module-wide by the coordinator; logged here once. No per-occurrence finding.
2. **Essin and "the missing year's two bodies"** — still open from LOG_oraga_5e_pass2 open item 3, AUDIT_oraga_5e_canon A-12 and INVENTIONS #13. 09 uses it as S13's *Broker a trade* out (09:1559–1562) and in the Boranis line (09:292–293, 09:321–322). *Background:* the source says Essin "knows exactly where its two bodies are buried". That may be the idiom (he knows the secrets) or literal (two corpses). The 5e edition reads it literally and makes it a bargaining chip. *Question:* are the "two bodies" real corpses, or a figure of speech for secrets? If secrets, S13's out becomes "Essin knows what really happened in the missing year, and Draunel would give a great deal to know it" and nothing else changes.
3. **Who is the man walking between the duellists in S9?** *Background:* the S9 read-aloud (09:1202–1203) shows "a man in a good coat… walking slowly between the two sides, speaking to each in turn", but no text says who he is. Draunel "will not set foot on the grass" (09:1238–1239), and Essin only arrives later. *Question:* is he Lord Draunel working the terrace from its edge, one of the seconds, or should the line be cut? Cutting it is the canon-safe default.
4. **XP for walk-away outs (SNAKES-5).** This touches 01 Table I–4, a rule the pass-2 fixers set rather than the owner. *Question:* should an out in which the party simply leaves (let the thieves go, walk away from the cousins, back off from the Attendant) pay the card's full XP? *Recommend:* no. Pay outs that resolve the scene, not ones that leave it.

*Resolved. Audit of 09 complete; findings go to consolidation in `docs/AUDIT_oraga_5e_official_style.md`.*
