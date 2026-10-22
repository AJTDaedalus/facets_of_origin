# Oraga Night 5e: Usability Audit for a 3-Player, 4th-Level Friday Session

*2026-10-20. Audit of `conversions/dnd5e/oraga_night/` at `b254fb0` (clean tree), done as the DM who runs it on
Friday for **three** 4th-level players with **90 minutes** of prep. I read chapters 01–11, the five
maps (PNG by eye, SVG labels), the handouts, the pregens and the flow page. I simulated the prep
box by word count (200 wpm reading, ~400 wpm skimming), then walked the night Movement by Movement
from the DM sheet. I compared the result with three session-length official analogs, extracted to
the scratchpad only: Lost Mine of Phandelver (intro and Part 1), the Curse of Strahd Introductory
Adventure (Death House) and DDEX1-5 *The Courting of Fire* (also DDEX1-1). No reference text is quoted
here, and no module file was edited. Line numbers are from today's files. The prior findings are in
`docs/REVIEW_oraga_5e_official_critical_2.md` (R2, 8.0/10). This audit covers what still hurts at a
table, plus new problems.*

---

## 0. Verdict

**5.5 / 10 as a runnable product for this Friday.** (R2's 8.0 graded it as a *book*. This grade is
whether a DM can prep it in 90 minutes and run it for three players in one evening.)

**What works, and works better than the references:**
- The run boxes at the head of each Movement.
- The two checkpoints (toast by 2:15, midnight by 3:15) and the cut list.
- A fight-card format with clocks, outs and three-character lines on every card.
- The DM sheet's "Where Everyone Stands" and honor-guard tables.
- Read-aloud that is ready to read.
- A cost table for near misses.
- No official one-shot of this size gives the DM that much table scaffolding.

**Why it still loses Friday:**
1. **It is ten times the size of its analogs.** Chapters 01–11 run to **99,700 words**. Death House is
   about 8,500 words. LMoP's intro and Part 1 together are about 9,100. DDEX1-5, appendices included,
   is about 15,000.
2. **The 90-minute prep box assigns 138 minutes of reading** (185 counting the stat blocks it says to
   know, about 205 counting chapter VII, which chapter I says both to skip and to "skim again").
3. **The prep path and the run path both skip the climax's main lever.** The Fracture tells are not in
   the prep list, not in chapter IV's Movement text and not on the DM sheet (P0-1).
4. **The midnight hour has no tracking sheet.** It runs on **52 module-invented rule families** and
   about 20 pieces of live state.
5. **The three-player numbers are scattered.** Five places print the four-player number with no
   override: the DM sheet, chapter X, chapter V's prose, Table V–1 and Table VIII–1.
6. **The runtime is unrealistic for three players.** Book 4 h 50 min; likely 5 h 30 min to 6 h 15 min.
   The boss fight alone (S14) is 40–60 minutes at three.
7. **The gallery geometry R2 left open now blocks the one card live by default at midnight** (S11).

**Counts:** P0 **1** · P1 **6** · P2 **12** · P3 **10**. Module-invented rule families **52**.
Cross-references **~473** (96 named-section, 111 bare-chapter, 101 card, 80 table, 70 area, 15 map). The
named-section references resolve mechanically. **3** are broken or misleading, and **9** are vague
enough to cost a flip.

---

## 1. Scale against the references

| | Words | Maps | Rule systems a DM must learn beyond core 5e | Prep at 200 wpm |
|---|---|---|---|---|
| Death House (CoS intro adventure) | ~8,500 | 2 (house, dungeon) | A handful of room-level effects | ~45 min, whole adventure |
| LMoP intro + Part 1 | ~9,100 | 2 | None of note | ~45 min |
| DDEX1-5 (AL, 2–4 h) | ~15,000, incl. appendices | 2 | One party-strength table, used once; per-encounter adjust sidebars | ~60 min skim |
| **Oraga Night 5e, ch 01–11** | **~99,700** | **5 + flow page** | **52 families** (§5.1) | **138–205 min** (§2) |

Structural lessons from the references, which the module only partly takes:
- **AL computes party strength once, up front, and every encounter's sidebar reads off it.** Oraga
  prints a three-character line on each card (good). But its non-card rules (Delay lumps, the Wept's
  timing, the Attendant) carry their three-player numbers in one sidebar (05:285–297), and the tools
  the DM actually runs from repeat the four-player numbers.
- **AL and LMoP put every stat block an encounter needs in an appendix, in order of appearance.**
  Oraga files 29 blocks alphabetically, so S3 alone needs three distant blocks (10:491, 10:538,
  10:1731).
- **Death House can be read whole in one sitting.** Oraga cannot, so its prep box is the product. The
  box therefore has to be right (§2).

---

## 2. The prep simulation (followed literally)

The box is at 01:3–36. Word counts are of the exact ranges it names. "Skim" is costed at 400 wpm.

| Step | Box budget | What it covers | Words | Real minutes |
|---|---|---|---|---|
| 1 | 15 | Ch I to the end of "The Snakes in the Chicken Pen" (01:1–411, incl. "The Fights, and How to Offer Them") | 4,640 | **23.2** |
| 2 | 15 | Ch II "What Is Coming" → "What the Module Never Says" + "The Eight Agendas" (02:116–435) | 3,190 | 16.0 |
| 3 | 10 | Ch VIII DM sheet + "palace diagram" (08:1–197) | 2,340 | 11.7 |
| 4 | 25 | Ch V: How to Run (1,075), Mv VI opening (1,026), Down Not Out + Buying Time (1,155), the Attendant (474), the Crossing (1,286), Mv VII opening (465), Epilogue (239); skim Room Tricks + 200 People (1,767) | 5,720 + 1,767 skim | **33.0** |
| 5 | 15 | Ch IX "Snakes at the Ball" + "Running the Snakes" (1,494), S3 (1,864), S14 (2,015); skim the agenda cards. For a likely trio (Dassa / Agenda 8, Serane / Agenda 3, Ilesse / Agenda 4): S2, S4, S6, S7, S9, S10, S13 (6,450) | 5,373 + 6,450 skim | **43.0** |
| 6 | 10 | Ch IV Palace on Alert, Draws Early, Running the Room, the 5 run boxes; Undercurrent C (Agenda 4 is in play) | 1,832 + 434 | 11.4 |
| **Listed total** | **90** | | | **138 min** |
| Implied, unbudgeted | 0 | "Skim or skip ch X **beyond** the Uninvited, the Attendant and the Bought" (01:30), so those are read: Uninvited preamble, Attendant, Hollow, Radiant, Wept, 4 Bought blocks | 7,298 | +36.5 → **~175** |
| Implied, unbudgeted | 0 | "Know the cast… chapter VII… the chapter to skim again before you sit down" (01:551–553) | 7,783 skim | +19.5 → **~195** |
| Not in the box at all | — | 3-player annotation of the DM sheet (§5.5), printing and cutting handouts, laying out 5 maps | — | +10–15 → **~205** |

**Result: 138 minutes for the listed reading, about 1.5× the budget. A realistic 175–205, about 2–2.3×.**

Worse than the overrun is what the box leaves out. These are the parts the night depends on:
- **"The Fractures" (05:725–828) and "You Cannot Beat Them" (05:664–723) are not in step 4.** The DM
  sheet gives the Fracture rule one line (08:83–86) and no tells. Chapter V calls Delay, the Fractures
  and the leash "the complete list" of what changes outcomes (05:700–702). See P0-1.
- **S11 is not in step 5.** Chapter IX says S11 is the *one* card live in the dark when the table does
  nothing (09:478–479; 08:218–221).
- **Step 3 says "print both"** (the DM sheet and "the palace diagram", 01:16). The palace is now five
  maps, and chapter VIII says "print the first three pages" (08:5).

What I would actually do with 90 minutes: steps 1–3 trimmed (35 min), chapter V's Midnight Clock,
Down Not Out, Buying Time, the Attendant, the Fractures and the Crossing (30 min), and S14, S3 and S11
(20 min). Anything left goes on Table V–6. That reading order is not the one the book gives.

---

## 3. The session walk (from the DM sheet, three players)

Book minutes are Table I–1 / VIII–1 (written for four). My three-player estimates assume the likely
trio above and a table of mixed experience. A "flip" means leaving the DM sheet for another chapter.

| Movement | Book | Flips (where to) | Friction at the table | 3p estimate |
|---|---|---|---|---|
| **First five minutes + street** | 10 | 4: ch I Table I–2 (hooks are not on the DM sheet) → ch III / XI pregen table → ch VIII Handout 2 → ch IV B0 read-aloud | No guidance for **three** (01:228–230, 03:197–199 and 11:29–31 cover four only). The table must choose 3 of 5 pregens and 3 of 8 agendas, keep Ilesse for Agenda 4, and know the sheets are 600–800 words each with no spell text. New players need 5+ minutes per sheet | **15–20** |
| **I. Receiving Line** | 25 | 4–5: ch IV Mv I (two read-alouds) → B0 DM Note (first check) → B1 (gate DCs; also Table VIII–3) → Table VIII–8 / VIII–4 → ch VII Corval. If steel: ch IV Palace on Alert → S4 → Honor Guard block | Smooth. The DM sheet's "S4 if anyone draws" works, but S4's terrain is the east-wing corridor (09:899–902) | **20–25** |
| **II. Empty Rooms** | 45 | 6–9: ch IV Mv II → ch II agendas (each card's private "At midnight") → B7 / B9 / B10 by agenda → ch VII × 4–6 guests → S1 or S6 (+ blocks, ch X; map VIII–4) → Snake Tracker ticks | The run box says "one snake line" and chapter IV says "show one or two" (04:975). The agenda beats have no page pointers ("the gallery wards studied (Agenda 5)": go find B7). S1 or S6 adds 20–25 minutes of combat | **35–55** |
| **III. Summons** | 35 | 6–8: ch IV Mv III + "Raunu's Summons" → ch VII Raunu → ch VII Uninvited → **ch V Table V–6 for tells** (not on the sheet) → ch IV "The Other Thieves" for "Tavva's scout" (the DM sheet names it; Mv III's text does not) → S6 | **The Fracture tells for Mv III are nowhere on the run path** (P0-1). "High gallery" and "B4 antechamber" appear on no map | **35–50** |
| **IV. Toast** | 25 | 4–6: ch IV toast + Dinner for Two → ch VII Veier → S7 / S9 → Snake Tracker | **Six heat boxes tick at once** at the toast (Circle, Draunel and Thenya automatic; Church on the blessing; Boranis on the appointment; Phern omen). The DM must remember which are automatic, because Table VIII–5 marks them with ✱ while Table IX–2 uses italics | **25–35** |
| **V. Hour of Spirits** | 40 | 5–8: ch IV Mv V → Table V–6 (cradle-song, the Radiant's dance) → one card per group from S2 / S7 / S8 / S9 / S10, each with its blocks (ch X) and maps (VIII–4 / VIII–5) → tracker | With three players split, "one card per group" can mean three fights in 40 minutes (09:505–512). The Thenya default heat is 3, so S10's clock runs offstage even if no one goes. Stealth has Advantage (04:1335–1336): one more rule | **45–70** |
| *Break* | 10 | | | 10 |
| **VI. Unmasking** | 50 | **10–15:** ch V opening read-alouds → Midnight Clock → DM sheet VIII–2 + page 2 → Table V–1 → Tables V–2 to V–5 → the Fractures + tells-seen per Uninvited → S11 + map VIII–3 → S14 + the Attendant block + the 3p override (09:1920) → Uninvited blocks (ch X) when struck → the spell table (10:143–162) → the Crossing + crossfire + Vell sidebars → S8 dark half / S5 → ⟨If History Breaks⟩ | About 20 pieces of live state and no grid to hold them (P1-2). The Wept's turn count (3rd, or 4th at three) is not on the DM sheet (08:36). The 3p lump threshold (20) contradicts the DM sheet (30, 08:69). S11's door may be unreachable from the floor (P1-4). **S14 with three PCs: the slugging route needs ~12–14 rounds (180 HP, AC 17, ~13–15 party DPR at +6), and the distraction route ~7 rounds (four Focused breaks at DC 19, one try a round, ~55% each). Each round is 3 PC turns plus up to 2 Attendant turns** | **70–100** |
| **VII. Longest Night** | 40 | 6–8: ch V Mv VII + B12 → S3 + **three blocks at 10:491, 10:538, 10:1731** + map VIII–2 → carry-out rule + Tables I–3/I–4 → General Features (fire, smoke) → S12 / S13 / S5 | The S3 three-character line swaps the sergeant but leaves the captain arriving in round 3 (P2-2). Two clocks (fire, 4; bell, 6) plus the captain's trigger | **40–60** |
| **Epilogue** | 10 | 2: ch V epilogue → Table I–4 / ch VI | Fine | 10 |
| **Total** | **4 h 50** | **~50–65 flips** | | **5 h 05 low · ~5 h 40 likely · 6 h 25 high** |

**Is 4½–5 hours realistic at three?** Only with the cut list used hard: no S1 or S6, one card in Mv V,
and S14 resolved fast. The social Movements run about 15–20% faster with three, because there are fewer
spotlight rotations. The fights do not get faster. The S14 three-character line cuts the Attendant's
HP by 21% (229 → 180), but a three-PC party loses about 25–33% of its damage output. The card's own
"about six rounds" for the errand (09:1787) is shorter than either winning route takes at three, so the
boss usually just times out (P2-1). The cut list (01:204–207, 08:28–30) never mentions S14, the
longest scene in the night.

---

## 4. Maps

Checked: all five PNGs by eye, plus the SVG labels.

**Readable and good.**
- Clean legends, 5-ft grids, scale bars, fight-card badges on the map.
- The Gatehouse section and the terrace profile answer most "how far is the drop" questions.
- Map VIII–5's corridor lengths match chapter V (100 ft, 60 ft, a 12-ft stair).
- The decision IDs, "?" and "not given" are gone (R2 N3 fixed).

**What they still fail to answer** (the spatial questions the scenes raise):

| Question the scene raises | Where | Map answer |
|---|---|---|
| How does anyone get from the Court floor to the galleries (B3)? The toast fills them (04:1170); S13 burns them; Vorlain hauls guests out of them | 05:455–456, 04:1170, S12/S13 | **None.** VIII–3 draws no gallery stair. B3 is "gallery level, 12 ft up" wall to wall |
| Is the S11 "gallery-side service door" at floor level, where the crowd is, or at gallery level? | 05:177, 05:384, 09:379, 09:1510 | VIII–3 draws it in the **west gallery's outer wall**, inside the area labeled "gallery level, 12 ft up". If so, the floor crowd cannot reach the night's only default card. If it is under the gallery, the map does not show that |
| What floor is the Audience Hall (B4) on? | 04:1023–1036 | VIII–1 boxes it "by connection" with no floor color; VIII–3 puts its door in the gallery's outer wall |
| What is the drop from the garden walk to the upper terrace? (S9's rail crowd; vaulting the rail) | 05:453–455 | VIII–3's rail symbol is labeled "Rail, 12 ft above the Court floor"; VIII–4's legend says the rail has "a 10-ft drop beyond". **They disagree** |
| Is S10's lit window "on the second floor" or at gallery level? What level is the garden below the wing? | 09:1431, 09:1462 | VIII–5 says "20 ft of crystal wall up to one lit window" and gives no ground level for the garden. The text still says "second floor" (R2 N4 open) |
| Where are the "high gallery" (Mv III glimpse), the "musicians' gallery" (B2 read-aloud), the "B4 antechamber", and the four ward-points on the dais? | 04:1016, 04:231, 04:1141, 05:306 | Not drawn |

**Hedges still printed.** "Other positions approximate" appears on VIII–2, –3, –4 and –5. VIII–1 is still
a schematic that boxes six rooms "by connection" (B6, B7, B8, B10, B11, B13), and B4 is dashed (R2 N11
open). This is the hedging R2 said official maps never do.

---

## 5. Counts

### 5.1 Module-invented rules the DM must hold (52 families)

*Ladder and social (10):*
1. The DC ladder.
2. Success at a cost, and its d6 table.
3. NPCs make no checks.
4. The gift gives Advantage.
5. Inspiration transfer.
6. Printed Inspiration awards (6 rows).
7. The XP table.
8. Chapel-only Short Rest.
9. Masks: identify 15/20; DC 10 across station.
10. Raunu's friendly trigger.

*The ball (12):*
11. Palace on Alert: 2 guards, 4 more when one is Bloodied, knockout blows.
12. The gatehouse cell scene.
13. The forced wing doubles the guard.
14. Spells count as steel (Sleight of Hand DC 13 to cast unseen).
15. Nonlethal from any attack.
16. Stable-at-once before midnight.
17. Getaway chase: 3 successes before 3 failures.
18. Feud brawl nonlethal.
19. Ward study.
20. Dead Dance: Advantage on Stealth.
21. Omen naming.
22. Angling for a summons.

*Snakes and cards (7):*
23. Snake heat: 6 factions, automatic ticks, 0–2 / 3 / 4 bands.
24. Snakes shown per Movement.
25. One card per group in Mv V.
26. Card clocks, and "a 1 on a d20".
27. Morale triggers.
28. Outs pay full XP; "(no XP)" outs.
29. Heat-4 "steel out" lines.

*Charges (2):*
30. Charge release; chancy release DC 13.
31. Crystals gutter within 30 ft of an Uninvited.

*Midnight (21):*
32. Beats against rounds.
33. The 8-step Midnight Clock.
34. The Wept's arrival turn.
35. The Radiant's 3-beat delay.
36. Down, Not Out: rouse, crowd, first-haul Inspiration.
37. The last-blow throw.
38. Leashed return.
39. Delay: spend at turn start.
40. Trick DC 13 / 15 / never a third time, per Uninvited.
41. Damage lump: 30, or 20 at three.
42. What Delay buys (Table V–1).
43. Leftover Radiant Delay is spent at the gate.
44. Ward steering: 13 / 18 / 10, once per point, 3 options, 1 round within 30 ft.
45. Root master valve.
46. Two Hundred People: guests per square, area spells, trample.
47. Retinues take a Blade at the gate.
48. The Attendant: Idle/Focused, Literal Orders, Rusty, Two Turns, distraction DC 13/19 +2/+2 (max +4),
    one try a round, no Help, repeats, furniture, success by 5, natural 20, four breaks, Clears the Way.
    About 12 sub-rules on its own.
49. Fractures: DC by tells; Wept 15 at 2+ Delay; skills allowed and barred; three result bands; once each.
50. Witnessed, and chasing the Radiant.
51. The Crossing: 3 beats, crossfire save, Veier's speed and carrying.
52. Smoke, fire, carrying out, and the S3 field rules (bar, wicket, fire clock, bell clock, void
    contract), plus the ward-trap.

**Live at the same moment at midnight: about 21.** Death House and LMoP Part 1 ask the DM to hold two
or three bespoke mechanics. DDEX1-5 asks for one table, used once.

### 5.2 Numbers computed at the table (not printed where you need them)
- **Fracture DC per Uninvited.** It depends on how many tells *this* character witnessed (18/15), and
  the Wept's switches at 2+ Delay. No sheet records who saw what.
- **The damage lump.** The DM sums all party damage to *one* Uninvited across a round, against 30 (or
  20 at three).
- **When the Wept reaches Raunu.** Her turn count plus banked Delay, minus the Attendant's removals.
- **When the Radiant reaches the garden stair.** Beats counted from Raunu's fall.
- **The Attendant's second turn,** at Initiative −10.
- **Distraction DC.** The modifiers stack to +4, a repeat has Disadvantage, and "success by 5" must be
  checked.
- **Trick DC 13 or 15,** depending on whether *that* trick already worked on *that* Uninvited.
- **S3's captain arrival,** at the bell clock's 2nd segment or round 3. **XP splits** by three.
  **Carry-out XP** at 100 per person, per carrier.
- **Area spell casualties:** squares covered = guests.

### 5.3 Cross-references
- **About 473 in all:**
  - 96 to a named section;
  - 111 bare chapter references ("(see chapter X)" with no section);
  - 101 to a card;
  - 80 to a table;
  - 70 to an area;
  - 15 to a map.
- Every named-section target exists. The tools check that, and I re-checked it.

**Broken or misleading (3):**
1. **04:90–91.** "What the Bought do, at each bell: see the DM sheet". The DM sheet gives the Bought one
   row (08:44) and no bell schedule.
2. **08:243.** Table VIII–6 says "Wept: east doors". Table V–6 (05:769) says "the east wing doors", a
   different door 60 ft and a stair away (R2 P3-21, still open).
3. **01:16, 01:109, 04:50, 04:407.** "The palace diagram" is a single object that no longer exists. It
   is now five maps, and VIII–1 is a schematic.

**Vague enough to cost a flip (9):**
- 04:1424: "see chapter V: Maiven is where the night will need competent company". No section is named.
- 04:1043: "Play the summons per chapter VII".
- The six "→ the X's line, chapter IX" pointers in chapter IV's snake bullets. They give no table or row,
  and the line tables are 50 lines apart.
- 05:226: "chapter X, 'Leashed'". That is a trait printed three times (10:1135, 10:1407, 10:1932), not a section.

### 5.4 Three-player adjustments the DM must apply by hand (12)
1. **Pregen choice.** No 3-player trio is given (01:228–230; 03:197–199; 11:29–31).
2. **Agenda deal.** Three of eight cards, and nothing says which.
3. **Runtime table.** Table I–1 / VIII–1 are "(four players)" (01:183; 08:13).
4. **The scattered-party advice** assumes four (04:446).
5. **The Wept's turn: fourth at three** (05:79, 05:291). But Table V–1 says third (05:272), and the DM
   sheet gives no number (08:36).
6. **The lump: 20 at three** (05:291–292). But **30** is printed at 08:69 (the DM sheet), 10:145, 05:260,
   05:681 and 05:706.
7. **The Attendant: 180 HP** and a single Joined Hands on its second turn (09:1920). The block says 229
   (10:200), and the DM sheet gives no HP.
8. **S3: the three-character sergeant.** The captain is unaddressed (09:883–884 against 09:793–795).
9. Every fight card's *Three characters* line: S1–S14.
10. **Summons.** "Two should be PCs" (04:1038). At three, that is two-thirds of the table.
11. **The "lands close to 6,500 XP" claim** (01:322) is for four. At three, every card XP splits 3 ways.
    Moot under milestone, but the table says otherwise.
12. **Mv V's "one card per group"** for a split trio (09:507–509).

---

## 6. Handouts (chapter VIII)

**Player-safe: yes.**
- **Handout 1** (the invitation) is clean.
- **Handout 2** (the agenda cards) tells each character only what it knows. No card leaks a DM secret.
  The "who paid you" line on card 6 is a deliberate player-facing unknown.
- **Handout 3** (crystal charges) hints that "some things at this ball smother a charge". That is fair
  foreshadowing, not a secret.

**Printable: only after work.**
- The handouts are Markdown, with no page breaks and no cut lines.
- The agenda cards are eight run-on paragraphs to "cut apart" (08:317).
- The italic DM line at the head of each handout must be trimmed by hand before printing (08:289–290).
- Official AL handouts are laid out one per page, ready to copy.

**Missing.**
- A player-facing palace sketch (the public rooms only). Every masquerade table asks "where is the
  terrace?"
- A one-page "what your character knows about tonight's customs" (no disarming, masks, Unmasking,
  Dead Dance). The players need these customs, and today they live in DM prose.

---

## 7. Pregens (chapter XI)

**For an experienced 5e player:** usable and correct, and R2 verified the arithmetic.

**For a new player, not usable:**
- **They are stat blocks in prose, not sheets.** There are no HP, slot, Inspiration or charge trackers.
- **No spell text.** Serane has 9 spells and Ilesse 11 by name only, so the table needs the SRD open.
  Official starter pregens explain each spell on the sheet.
- **Each sheet depends on the shared preamble** (11:33–43: Resourceful, Skillful, the knife,
  Handout 3). Print one character per player and the human traits and the Heroic Inspiration rule are
  gone.
- **No "on your turn" line.** Such a line is what lets a new player act without reading a page.
- **No three-player trio.** The only advice is "Two of the five can stand in a fight: Dassa and Pello"
  (11:24). For three, the obvious trio is Dassa, Ilesse (needed for Agenda 4) and Serane or Pello.
  Say so.

---

## 8. The flow page (`flow/oraga_night_flow.html`)

- **The book never points to it.** It is listed only under README "For Contributors" (README:89). A DM
  following chapter I never meets it.
- **Its node references are file paths** ("→ 04_The_Ball.md#the-public-rooms (B0)"), not page or
  section names. Its footer is build-provenance text ("Generated from …/flow.json by
  flow/build_flow_page.py").
- **111 nodes and 201 edges, with no print stylesheet.** That is a design map, not a table tool. It needs
  network access for its fonts (it degrades acceptably).
- **It carries no three-player timings** and no midnight state.
- **Verdict:** useful to the author for checking that every branch closes. Of no use to the Friday DM.
  Either make it a one-page printable "night at a glance", or keep it out of the DM's path, as now.

---

## 9. Findings

### P0: will derail Friday if the book is followed literally

**P0-1. The Fracture tells, the climax's main lever, are on neither the prep path nor the run path.**
- **Where:**
  - The prep box step 4 (01:18–22) omits "You Cannot Beat Them" and "The Fractures" (05:664–828).
  - The DM sheet gives the Fractures one line (08:83–86) and lists no tells.
  - Table VIII–1's "omen" column holds only the Mv III gray masks and the Mv V Wept line.
  - Chapter IV's Movement text never places the tells: grep finds no cradle-song, no *"Whom do you
    serve?"*, no pages, no flat answer and no exit-standing. Only the Radiant's blessing (04:1240)
    and the Dead Dance line appear.
  - The tells live only in Table V–6 (05:765–771), in chapter V, which the DM does not open until
    midnight.
- **Failure:** the DM runs Movements III–V from the DM sheet and chapter IV, as the book says to
  (README:98–100). The party reaches midnight having seen one or two tells, by accident. The DM has not
  read the Fracture result bands (05:753–761), the Wept's 2+ Delay rule or the Radiant's two roads.
  Chapter V calls Delay, Fractures and the leash "the complete list" of what changes outcomes (05:700).
  One of the three is now gone, and ⟨They save Raunu⟩ (05:1090) becomes unreachable.
- **Fix:**
  - Add a **"Tells" column to Table VIII–1**, with one line per Movement taken from Table V–6.
  - Add a bullet to each Mv III–V block in chapter IV: "**The Uninvited's tell this Movement:** …".
  - Add "The Fractures" to prep step 4, costed at 5 minutes.
  - Add a tick-box row to the DM sheet: tells seen, per Uninvited, per character.

### P1: real table damage

**P1-1. The 90-minute prep box needs 138 minutes as written, 175–205 as implied, and contradicts itself.**
- **Where:**
  - 01:3–36. Steps 1, 4 and 5 overrun by 8, 8 and 28 minutes (§2).
  - 01:30 implies reading 7,300 words of chapter X at no cost.
  - 01:28 says to skim or skip chapter VII; 01:551–553 says to skim it *again*.
  - S11, the one default card, is omitted (09:478–479).
- **Failure:** the DM stops at about minute 90, partway through step 5, without S3 or S14 read and
  without the stat blocks.
- **Fix:**
  - Re-cost each step from its word count, or cut it to fit. Step 1 ends at "What the Night Pays"
    (−5 minutes). Step 2 drops "What the Module Never Says" to a skim. Step 5 becomes "S14, S3, S11;
    the agenda cards go into the box only as their one-line *where/when*".
  - Add a **"Before midnight, know these blocks" list of five**: the Attendant, Veteran Bought
    Sergeant, Bought Blade, Bought Captain, and the Wept, for her Fracture.
  - State the honest total, and give a **60-minute emergency path**.

**P1-2. The midnight hour has no tracker, though it runs on about 20 pieces of live state.**
- **Where:**
  - DM sheet page 2 (08:58–129) restates the rules but gives nothing to write on.
  - The state:
    - Delay on 3 Uninvited;
    - the Wept's turns toward Raunu (3, or 4 at three);
    - the Radiant's beats since Raunu fell;
    - the Crossing beat (1–3);
    - the Attendant: Idle/Focused, breaks (0–4), tricks used (repeat/never), the furniture list and its HP;
    - tells seen per character per Uninvited, and Fractures spent;
    - ward-points used (4 dais, 2 doors, the sealed doors);
    - heat at midnight;
    - the S3 fire and bell clocks.
- **Failure:** state drifts by about the third beat. Either the Wept reaches Raunu early or late, or
  the Attendant's break count is forgotten, and the climax's fairness depends on both.
- **Fix:** a third DM page, **"Midnight Tracker"**:
  - three Delay tracks, each with its arrival line printed (Wept: turn 3/4; Radiant: stair at
    fall+3);
  - an Attendant box: state, ○○○○ breaks, a "tricks used" list, HP 229/180;
  - a tells grid (3 × characters);
  - ward-point checkboxes;
  - the S3 clocks.

  This is the module's own invention. Official adventures that invent a subsystem ship its tracker.

**P1-3. The three-player numbers are in sidebars. The tools the DM runs from print the four-player numbers.**
- **Where:** §5.4 items 5–8. The lump of 30 at 08:69, 10:145, 05:260, 05:681 and 05:706, against 20 at
  05:291. The Wept "third turn" at 05:272 and nothing at 08:36. The Attendant at 229 (10:200) against
  180 (09:1920).
- **Failure:** mid-fight, the DM reads the DM sheet and applies 30 and turn 3. A three-player party
  then loses Raunu a turn early and needs 50% more damage per Delay than intended.
- **Fix:**
  - Print every DM-sheet number as "30 (3 PCs: 20)" and "3rd turn (3 PCs: 4th)".
  - Give the Attendant's block a scaling line beside its HP.
  - Better, follow AL: one "Your table" box at the top of the DM sheet, with the five non-card numbers
    for 3 / 4 / 5 players, filled in once before play.

**P1-4. The gallery geometry R2 left open (N4) now blocks the default midnight card and the fire scenes.**
- **Where:**
  - Map VIII–3 draws no stair between the Court floor and B3.
  - It puts S11's service door and B4's door in the outer wall of a gallery labeled "12 ft up".
  - 05:177, 05:384 and 09:1510 assume the crowd on the floor reaches that door.
  - S12 and S13 burn B3, and Vorlain hauls guests out of it (05:925–926) by no drawn route.
- **Failure:** "the door is up there?" stops the first beat of Movement VI at the table's most important
  moment. The DM improvises stairs and doors that then contradict Table V–3's door tricks.
- **Fix:**
  - Draw two gallery stairs off the Court floor, say at the dais end and the doors end.
  - Move the S11 service door and the B4 door to **floor level beneath the gallery**, and say so in
    05 General Features: "the galleries are a mezzanine over a floor-level aisle".
  - Fix the VIII–3 caption.

**P1-5. The 4 h 50 min runtime is not realistic at three, and the cut list ignores the longest scene.**
- **Where:**
  - 01:183–202 and 08:13–30.
  - S14's "about six rounds" (09:1787) against roughly 7 rounds to win by distraction and 12–14 by
    damage at three (§3).
  - The cut list (01:204–207) never names S14 or the dark-hour cards.
- **Failure:** midnight lands at 3:15 as the checkpoint forces. Movement VI then runs 70–100 minutes,
  and the gate starts at about 4:40. The session ends near 5:40 with an exhausted table, or the gate
  is played as a summary.
- **Fix:**
  - Add a **three-player runtime column**: social Movements −15%, Mv VI 70.
  - Add "S14: cap at 5 rounds; if it is still standing, the Uninvited finish the room and it leaves"
    to the cut list.
  - Add a hard rule: "Movement VI ends at 4:20 whatever is running; go to the gate."

**P1-6. The product cannot be printed as shipped.**
- **Where:**
  - 08:3–5 says "print the first three pages", but the files are Markdown.
  - The "two-page" DM sheet is 1,767 words of six-column tables: realistically 3–4 printed pages at
    legible size.
  - The maps are five separate SVG/PNG files.
  - The pregen sheets lean on a shared preamble.
  - The handouts carry DM italics.
  - There is no PDF, HTML build or print stylesheet. The `tools/` folder checks the text but does not
    build anything printable.
- **Failure:** 20–30 minutes of the 90 go on formatting, or the DM runs from a laptop and scrolls
  between files (§3: 50–65 flips).
- **Fix:**
  - Ship a print build (Markdown → HTML/PDF): the DM packet (sheet, tracker, the five maps), the player
    packet (handouts with cut lines, one pregen per page with the preamble merged in) and the card deck
    (each card with its stat blocks appended).

### P2: off-standard, costs time or fairness

**P2-1. S14 at three: neither route to victory fits the card's own six-round errand. The win also
requires letting Delay lapse.**
- **Where:** 09:1782–1793 and 09:1920. Breaks count only while it is Focused, and it is Focused only
  when an Uninvited in the scene has no Delay (09:1789–1793).
- **Failure:** the table that protects Raunu by keeping Delay up can never score a break. The table that
  chases breaks gives up Delay. Most three-player tables end S14 by timeout, earning no XP and no
  catharsis. The DM Note's claim that the 3p line "keeps those odds about where they are" (09:1823) is
  unsupported.
- **Fix:** the three-character line becomes "three breaks; Focused DC 17". Add one sentence of player-
  facing advice for the DM to say aloud: "It only comes for you when one of them is free."

**P2-2. The S3 three-character line ignores the captain.**
- **Where:** 09:883–884 against 09:793–795.
- **Failure:** sergeant + 4 Blades + captain = 1,950 XP against a three-player High of 1,500. The
  captain arrives in round 3 in every version.
- **Fix:** "*Three characters:* …; the captain arrives at the start of the fourth round and opens
  talking."

**P2-3. S11 turns every guest through the door into 100 carry-out XP.**
- **Where:** 09:1583–1584 ("counts as carried out (Table I–4)"), 09:1558–1560 (a dozen a round),
  01:318.
- **Failure:** one character holding the door for 4 rounds claims 48 people, which is 4,800 XP. Table
  I–4 is also a Movement VII row, and S11 happens in Movement VI.
- **Fix:** "counts once, as one person carried out, for each character who held the door".

**P2-4. A broken reference to the Bought's bell schedule.**
- **Where:** 04:90–91.
- **Fix:** either print the schedule (the quarter-bells: fires set; first midnight bell: the gate shut;
  the runner in Mv V, per 05:1180) or cut the sentence.

**P2-5. The DM sheet omits the two numbers that time the climax.**
- **Where:** 08:36 and 08:37. There is no "3rd turn (4th at three)" for the Wept and no "stair at
  fall + 3 beats" for the Radiant. Both are in 05:78–86.
- **Fix:** add both to Table VIII–2's "Then" column.

**P2-6. Map residue.**
- "Other positions approximate" on four maps.
- VIII–1 is still a schematic with six rooms boxed.
- The VIII–3 rail symbol (12 ft) conflicts with VIII–4's (10 ft drop).
- S10's "second floor" window (09:1431), and no level for the garden below the wing.
- Undrawn places named in the text: the high gallery, the musicians' gallery, the B4 antechamber, the
  dais ward-points.
- **Fix:** decide each value once in `facts.yaml` and redraw. Give the walk rail its own symbol. Draw
  the four dais ward-points and the two door ward-points, because Tables V–2 and V–3 count them.

**P2-7. Chapter VII is the at-table reference, and it is 7,800 words of prose.**
- **Where:** 07 throughout. Each entry runs 300–600 words.
- **Failure:** "what does Essin want?" takes a minute of reading while three players wait.
- **Fix:** open each entry with a **two-line cue**: wants / voice / one line they'd say / where they are
  at midnight. Or add a one-page cast roster to the DM packet.

**P2-8. The pregens are not sheets for new players.** See §7.
- **Fix:** merge the preamble into each sheet, add trackers, one line of text per spell and an "on your
  turn" line, and name a three-player trio.

**P2-9. Stat blocks are not grouped by card.**
- **Where:** S3 needs 10:491, 10:538 and 10:1731. S9 needs four blocks across 10:318–1846.
- **Fix:** append the needed blocks (or a mini-block of AC / HP / attacks) to each card in the print
  build. This is the AL appendix convention.

**P2-10. Movement V's "one card per group" has no time budget for a split trio.**
- **Where:** 09:505–512 and 04:1324–1328.
- **Failure:** three groups means three fights inside 40 minutes.
- **Fix:** "At most one card on screen in Movement V; others resolve offstage by default, whatever the
  grouping, if you are past 2:40."

**P2-11. The flow page is outside the DM's path and not a table tool.** See §8.

**P2-12. The snake-show count is stated three ways.**
- **Where:** "show one or two" (04:908, 04:975, 04:1133); "Default: one line per Movement" (09:71); run
  box "one snake line" (04:940).
- **Fix:** say "one" everywhere, with the dial in one place.

### P3: polish

1. **"Palace diagram"** survives at 01:16, 01:109, 04:50 and 04:407. Use "Map VIII–1" (or "the maps").
2. **Table VIII–6, "Wept: east doors"** (08:243). It should read "the east wing doors" (R2 P3-21, open).
3. **08:3–5, "Print the first three pages".** The third "page" is five maps, and the handouts aren't
   mentioned.
4. **"One sighting in Movements I, II, IV and V, each … shows one of its three habits"** (04:896–897):
   that is four sightings for three habits. Say the Mv V glint is the crystal-and-light habit again.
5. **Table V–5 row 2 assumes S9 happened** ("The duel has already smashed the terrace balustrade",
   05:357). Add "(or the Crossing's first beat did)".
6. **Heat-tick notation differs between the two trackers:** ✱ in VIII–5, italics in IX–2. Use one.
7. **The five-at-5th rule differs:** 05:289 against 09:96–97.
8. **R2's open P3s are still open:**
   - "Svara" unglossed (01:438);
   - the three-way skill list (07:527, 08:117);
   - designer "yardstick" commentary (09:1796–1802, 10:313);
   - the Prickle's Advantage question (03:110–111).
9. **The flow page footer** prints repository paths.
10. **S4's terrain is the east-wing corridor,** but the DM sheet's Mv I line sends a gate draw to S4
    (08:18). Add "(run in B1; the corridor terrain doesn't apply)" to S4's *Where and when*.

---

## 10. What "Friday-ready" would take, in order

1. **P0-1.** Put the tells on the run path: a DM-sheet column plus one bullet per Movement. About 1 hour
   of editing, and the largest single gain.
2. **A Midnight Tracker page with three-player numbers printed beside the four-player ones** (P1-2,
   P1-3, P2-5).
3. **Re-cost the prep box honestly, and add a 60-minute path and a five-block list** (P1-1).
4. **Gallery stairs and floor-level doors** on VIII–3, plus one sentence in 05 (P1-4).
5. **A three-player runtime column and an S14 round cap** (P1-5, P2-1).
6. **A print build:** DM packet, player packet, card deck with blocks (P1-6, P2-8, P2-9).

With 1–5 done this is a 7.5 runnable product. With 6 it competes with the official session-length
modules on usability while keeping its much richer table scaffolding. The remaining gap is size: no
change to the text makes 100,000 words preppable in 90 minutes. The prep path has to carry the product.
