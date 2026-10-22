# LEDGER: Oraga Night 5e, three-player pass: consolidated findings

*2026-10-21. Docs only: no module file was edited to make this ledger. Scope: `conversions/dnd5e/oraga_night/`.*

## Purpose

This is one deduplicated list of every finding from the five audit reports and the synthesis. Each
finding has a disposition set against the approved design and the owner's rulings, so the fix pass
can be cut into tasks (`TASKS_oraga_5e_3p_pass.md`) with nothing lost and nothing done twice.

**Sources.**
- `docs/audit_oraga_5e_3p/TUNING_3P.md` (F1–F16), `LOGIC.md` (L1–L7, P2-1–P2-14, P3-1–P3-12),
  `VOICE.md` (P1-1–P3-6, rewrites R1–R22), `USABILITY.md` (P0-1–P3-10, §5.3, §5.4),
  `RULES.md` (P1-1–P3-17).
- `docs/REVIEW_oraga_5e_3p.md` (A1–A13, G1–G6, §7.1–§7.3, withdrawn recommendations).
- `docs/DESIGN_oraga_5e_3p_pass.md` (§2 risk dial and seven options, §3 Slow / Stop / End and the
  threat rule, §4 the lethal Attendant, §5 rulings TP7–TP12 and the still-open list).
- `docs/DECISIONS.md`, "Oraga Night 5e — three-player pass (2026-10-20)": TP1–TP12, which are
  authoritative.

**Owner direction this ledger enforces.**
- Combat risk outside the Uninvited goes **up**. The DM picks Gentle, Sharp or Merciless, and the
  book is written at Sharp.
- Every Uninvited can be slowed and stopped by creative, thematic play. Only a permanent End needs
  a specific method.
- The Attendant can kill.
- Three players is the printed baseline (TP10).
- Any earlier recommendation that softens difficulty is **WITHDRAWN**.

**Line numbers** are from `b254fb0`, as the auditors cited them. Spot-checks were made against
today's working tree. The TP11/TP12 edits moved `02` lines after 207 down by about 1–2 and `06`
lines after 34 by about 1. Nothing under `references/oraga_night/` is cited.

## Legend

**Severity.**
- **P0:** derails the session if the book is followed literally.
- **P1:** real defect at a three-player table.
- **P2:** costs time or fairness.
- **P3:** polish.

The severity shown is the highest any source gave, unless the merge note says otherwise.

**Disposition.**

| Code | Meaning |
|---|---|
| **FIX** | Covered by the approved design. The DESIGN section is named |
| **FIX-NEW** | A straightforward fix that is not yet in the design |
| **SUPERSEDED** | The finding or its proposed fix is replaced by the new design |
| **WITHDRAWN** | The recommendation contradicts owner direction (it softens difficulty) |
| **DONE** | Already fixed by the TP11/TP12 edits |
| **DISPUTED** | Checked against the text: the finding is wrong or overstated (the reason is given) |
| **RULING** | Needs an owner decision. Each has a question in §6 |

**Flags.**

| Flag | Meaning |
|---|---|
| `FRI` | Friday-critical: do it in the first fix chunk |
| `SIM` | Numbers must come from a re-simulation (the TUNING_3P method) |
| `CANON` | Touches canon. Use only printed facts, or the owner confirms |
| `FACTS` | Add or extend a `facts.yaml` guard so the fact checker holds the decision |
| `DIAL` | The text must say what changes at Gentle, Sharp and Merciless |

**Areas, in order:** Climax/Uninvited · Combat & risk · Three-player baseline · Story logic ·
Usability/prep · Rules accuracy · Voice.

---

## 1. P0

### Climax / Uninvited

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-001** | The Fracture tells, which Stop gets bonuses from and End requires, appear only in Table V–6. They are not in the prep box, chapter IV's Movements or the DM sheet, so a DM running from the sheet shows almost none | 05:765–771; 08:83–86; 04 (0 hits for each tell); 01:18–22 | USABILITY P0-1; REVIEW A1, G3 | FIX (§3.7, last bullet) | Add a "Tells to show" column to Table VIII–1, by Movement, and one tell bullet each to Movements III–V in ch IV. Put "The Fractures" (soon Slow / Stop / End) in prep step 4, and a tells-seen grid on the Midnight Tracker (L-027). Under §3.3 a missed tell costs only +2 toward Stop, but End still needs two tells, so this stays P0 | `FRI` |

---

## 2. P1

### Climax / Uninvited

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-002** | "A spell is a trick … if it lands, that is the success": a spell with no attack or save, cantrips included, buys Delay with no roll, twice per Uninvited. Andra alone gets ~10 free Delay. Chapter X says a trick needs "its check", so the two chapters disagree | 05:254–255; 10:164–166 | RULES P1-2; REVIEW A2 | FIX (§3.2 "Spells roll") | A spell with an attack or save uses that roll, and *Centuries of Practice* can refuse it. A spell with neither is a trick check with the caster's spellcasting ability, DC 13. Each spell counts once per Uninvited. Chapters V and X print the same sentence | `FRI` `FACTS` |
| **L-003** | The Idle-lock. One PC adjacent to the Attendant switches off *Clears the Way*, and the Attendant stays Idle. Delay is uncapped and outruns the spend of 1 a round, so the Wept stalls for 5.3–5.9 of 6 rounds and the party grinds the Attendant down for full XP | 10:217–260; 05:242–262; 09:1782–1793 | RULES P1-1; TUNING F10 (exploit); REVIEW A3 | FIX (§3.2 cap; §4 *Clears the Way*) | An Uninvited loses at most three turns per scene to Delay, and spare Delay gets named people out. *Clears the Way* costs one turn's action and no longer depends on adjacency. RULES' "Delay ≤3 / 8th-turn ceiling" and TUNING's "4 (3) turns" cap are superseded by the §3.2 cap. Decide after the S14 re-sim whether Idle-grind XP needs halving (RULES fix 3) | `FRI` `SIM` `FACTS` |
| **L-004** | The Crossing cannot fail. "The margin should be the characters, not luck" sits beside "Either way, the escape holds". Every Table V–5 trick, any Delay carried down, and the Radiant's Fracture at the gate buy nothing | 05:597–611; 05:625–629; 05:806–807; 05:273; 08:41 | LOGIC L4 and agency table; REVIEW A4, §7.3; RULES P3-14 | FIX (§5 TP7; §3.6; §3.1) | Rewrite the rules paragraph. With no Delay and no Last Rite, the Radiant's turn at the gate runs under the threat rule and can kill a marked creature. The Last Rite holds him at the altar until the boat is out of reach. The escape itself still holds (canon). Delete "the margin should be the characters, not luck" unless the rewrite makes it true. LOGIC's options (a)–(c) are not adopted | `CANON` `DIAL` |
| **L-005** | ⟨They save Raunu⟩, the likeliest divergence, has no procedure after the Wept's one-round stop. It is also near-automatic (two DC 10 ward-points → DC 15, and a fail by 4 still lands), and Down, Not Out removes the "real sacrifice" it asks for | 05:1090–1103; 05:484–487; 05:780–782; 05:755 | LOGIC L5; RULES P2-7; REVIEW A10, §7.2 | FIX (§3.4–§3.5 Wept End "Mercy"; §3.1) | Saving Raunu becomes the Wept's End: two tells plus Mercy, and a failure counts as a Stop attempt. The threat rule supplies the sacrifice, because whoever lands a Stop or End is marked. Write the following rounds as numbered steps once R-05 is ruled. Raise dais ward-steering to DC 13 unless the character studied the wards (the FIX-NEW part). RULES' Delay-discount and "blow ignores DNO" fixes are superseded by §3.7 and §3.1 | `DIAL` |
| **L-006** | DESIGN §3.5 makes the Wept's End "subject to §5 Q2: Raunu's own choice", and no TP ruling answers Q2. The book cannot say whether landing Mercy saves Raunu outright | DESIGN §3.5 table; 05:1093; 02:136–139 | DESIGN §3.5; LOGIC L5 | RULING (R-05) | See §6 R-05 | `CANON` |
| **L-007** | The control spells buy nothing. *Hold Person*, *Sleep*, *Hideous Laughter*, *Command*, *Charm Person*, *Suggestion*, *Calm Emotions*, fear, and *Web* or a grapple on the Wept or the Hollow are all "nothing bought", so the recommended trio's enchantments are dead at the climax. RAW, *Hideous Laughter* also leaves an Uninvited Prone, which contradicts its own row | 10:143–162 (148–152); 10:128; 10:1145; 10:1127, 1399, 1924 | RULES P2-1; REVIEW G1, §7.2 | FIX (§3.2 "Spells that land always buy 1 Delay"; §3.7) | A spell that lands buys 1 Delay, once per spell per Uninvited, or 2 on theme. Condition immunities stay, and the effect ends at once. Add Prone and "laughter, or anything that would leave them helpless" to *Held by Something Else* so the effect really does end. Turn the spell table into a short "what spells buy" list, and rewrite 10:128 | |
| **L-008** | The Fracture is gated by a clue. It needs a witnessed tell at DC 18/15, Intimidation and Deception are banned outright, each Fracture works once a night, and the scene effect sits behind the gate | 05:742–761; Table V–6 DC rows | REVIEW G2, G4, §7.2 | FIX (§3.3; §3.7) | Stop has three routes. (a) Words that reach the person: any fitting skill, DC 15, +2 per tell up to +4. (b) Three thematic successes in a scene. (c) A printed room freeze. Each Stop earns 2 Delay, marks the speaker, and can be used once per scene per Uninvited. The skill bans move into the Hollow's End only | |
| **L-009** | The three Fracture effects are different sizes: one round for the Wept, the rest of the night for the Radiant, gone for the Hollow. The Radiant has no permanent End and no weakness at all | 05:773–818; 10:1421; 10:1444–1505 | REVIEW §7.2 (tier note); TP4 | FIX (§3.5; §3.6 / TP7 "The Last Rite") | Use the per-Uninvited table: Stop effects scoped to the scene, and the Ends Mercy, The Last Rite and Permission. "Cannot be turned" stays as printed (TP7) | `CANON` |
| **L-010** | "Down, Not Out" is a blanket mercy for the Uninvited. Standing in the way costs nothing, which is what makes the Idle-lock blocker and the saving-Raunu body free | 05:204–235; 05:27–28 ("only ever in mortal danger by choice") | REVIEW §7.1; RULES §5 ("free resource"); TUNING §5 ("toothless"); TP6 | FIX (§3.1 threat rule) | Replace it for the Uninvited with the threat rule. A creature is marked when it lands a Stop, earns Delay three times in one scene against that Uninvited, or deals the last blow. Unmarked creatures are set aside, Stable. Marked creatures use normal dying rules, and at Sharp the Uninvited finish one only if it is still in the way. Retire 05:27's sentence. The DM says the mark aloud | `DIAL` `FACTS` |

### Combat & risk

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-011** | No layer of the night outside the Uninvited can cost a character anything that lasts. Chapter IX's rule 2 forbids ambushes and deaths before midnight, a drop is Stable at once with 1 HP, and every snake's people break early | 09:53–58; 09:544–547; 09:99–100; 05:27 | REVIEW §7.1; TP2 | FIX (§2.1 dial; §2.2 options 1–2) | Add a "How Hard to Go" box to ch I, with one dial word on the DM sheet. Rule 2 becomes "every ambush is foreshadowed". Each faction gains a *Heat 4: they come for you* row that reuses an existing card. Before midnight, a drop costs something from a table (robbed, held, marked for the inquest, or the gatehouse cell) but never kills | `DIAL` |
| **L-012** | After midnight the dying rule is ambiguous. The crowd rule only reaches *Stable* characters, but a snake's blade leaves a character dying, so the text half-promises a rescue it doesn't give. S13's fire clause makes any drop in the gallery Stable | 05:215–219; 05:232–235; 09:549–552; 09:1698–1704 | TUNING F3 (the defect); RULES P2-5 (S13 part); REVIEW A13 | FIX (§2.2 option 3) | Rewrite 09:549–552 and 05:232–235. Normal dying rules apply in every snake and Bought fight. The crowd rule covers only creatures an Uninvited set aside, and a heat-4 snake at Sharp finishes a downed character who crossed its line. S13 becomes "a creature the *fire* drops". Say it at the table when the lights die | `DIAL` |
| **L-013** | The Attendant cannot kill. Its Down, Not Out ("deadly but not lethal") makes the night's only beatable boss harmless | 05:428; the Attendant block (10) | REVIEW §7.1 option 4; TP5 | FIX (§4) | Idle, it sets a creature aside, Stable. Focused, normal dying rules apply, and at Sharp it attacks a downed creature only if that creature interrupted since its last turn. Re-sim S14 against the targets: engaged win ≥85%, a PC death ≤10%, and slugging mostly loses. Report every dial setting | `SIM` `DIAL` |
| **L-014** | The night has no rest after midnight, no healing items, and a Short Rest that costs a whole Movement. A party that likes a fight reaches the gate at 5–21% of its HP | 01:285–286; 04:286–287; 10:2155–2232 | TUNING F5 (b), (c); REVIEW §4, §7.1 option 7 | FIX (§2.2 option 7) | The chapel short rest costs half a Movement and advances every visible snake clock by one. Each character may spend one Hit Die at the toast. Place one healing potion per character in the Table X loot, where an exploring party finds it | |
| **L-015** | Card budgets are soft at three. 9 of 14 cards are under Low, and morale ends fights before they turn dangerous | 09:99–109; 09:56–58; per-card three-character lines | REVIEW §4, §7.1 option 6; TUNING §3 | FIX (§2.2 option 6) | Before midnight, cards go to Low or Moderate (750 / 1,125). After midnight they go to Moderate or High (1,125 / 1,500), and morale moves to "half down". Build new three-player rosters and re-sim each card | `SIM` |
| **L-016** | Labels are false at three. S8 ("well under Low") and S10 ("plays Low") play Moderate. S4 at 900 XP is above Low. S14's "nearly twice High" is 2.6× High. Five blocks list a CR one step above the derived one | 09:1242, 1262, 1298; 09:1449–1455, 1494; 09:906, 943; 09:531, 1798; 10:312–313; RULES §1 | TUNING F6, F7, F12, F14 (labels); RULES P3-17 (CR, S4); REVIEW §4, §7.1 | FIX (§2.2 option 6, "labels corrected upward") | Keep the rosters and correct each label to what the fight plays at three, from the re-sim. Settle the CR question (re-derive, or accept that labels read high) in the same pass | `SIM` |
| **L-017** | By default only S11 is live in the dark, plus the gate, so a party can reach dawn with one or two fights | 09:475–481; Table VIII–2; flow graph | REVIEW §7.1 option 5 | FIX (§2.2 option 5) | Move the default heats so two cards are live, S11 and S12: the Circle starts at 2, not 1. Update Table VIII–2 and `flow.json` | `FACTS` |
| **L-018** | Withdrawn fix for L-012: "after midnight a snake-downed character is dragged clear and Stable; dropped twice, stays down" (TUNING F3), and REVIEW A13's "soften" option | — | TUNING F3 (fix); REVIEW A13 (option) | WITHDRAWN | It softens lethality after midnight. L-012 applies instead | |
| **L-019** | Withdrawn fix for L-014: "at most one snake card live after midnight besides S11" | — | TUNING F5 (a) | WITHDRAWN | It cuts fights instead of adding resources. L-014 and L-017 apply instead | |

### Three-player baseline

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-020** | There is no three-player cast guidance. The table can pick a trio with no healer and no Agenda 4, and Agenda 4 is the only reliable route to the pregnancy and the east wing. Face-down dealing can lose it too | README:8–10; 01:219–221; 03:196–199; 11:29–31; 02:351–353; 11:22–24 | TUNING F1, F16; LOGIC L7, clue row 2; USABILITY §5.4 (1–2), §7; REVIEW A6, §7.3 | FIX-NEW (TP10 baseline; no DESIGN section) | Add a "Three at the Table" box to ch I, III and XI. Deal Dassa, Ilesse and Serane, with Agendas 4 / 8 / 2 dealt openly. For more steel, swap Serane for Pello. Never drop Ilesse unless someone else heals. Agenda 4 is always dealt | `FRI` |
| **L-021** | "One card per group" sends a lone PC against the whole three-character roster (71–100% drop at S2, S8, S10), and no card has a one- or two-PC line | 09:505–512; 04:1324–1327; 08:22; 04:446 | TUNING F2, §5 (S14 solo); REVIEW A6, §7.3 (re-aimed) | FIX-NEW | Size each card to who walks in: two PCs use the three-character line, and one PC gets a solo line built to be *dangerous but fair* (about High for one), not a token fight. With one PC in S14, the Focused second turn makes no attack | `SIM` |
| **L-022** | The tools the DM runs from print the four-player numbers: the 30-damage lump, the Wept on her third turn, the Attendant's 229 HP. The three-player values live in one sidebar, and 12 adjustments are left to apply by hand | 08:64–70; 08:36–37; 10:200; 10:145; 05:260, 272, 681, 706; 05:285–297; 09:1920 | TUNING F4; USABILITY P1-3, P2-5, §5.4 (5–8); REVIEW A5 | FIX (§5 TP10; §4 HP) | Print the three-player numbers everywhere: stat blocks, cards, Table V–1, the DM sheet, the tracker. Four and five become the adjustment lines. Add the Wept's turn ("4th") and the Radiant's "stair at fall + 3 beats" to Table VIII–2. The Attendant prints 180 HP. Reorder Table IX–1 | `FRI` `FACTS` |

### Story logic

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-023** | Raunu's motive: why is Veier upstairs at midnight when he knew something was coming? The audit's "sends her off by boat" was a misreading (TP11) | 02:207–208 (new); 04:827–831 | LOGIC L1; REVIEW A7 | DONE (TP11 line in ch II) | Chapter II now says he meant to keep her in the sealed east wing until the birth. The propagation that is still owed is L-024 | `CANON` |
| **L-024** | TP11 has not been propagated. 07 (Raunu, Veier), `facts.yaml` and `flow.json` don't carry the plan, and 04:831 ("What he is already doing about it is chapter V") points at two wrist crystals only | 04:831; 07 Raunu and Veier entries; `facts.yaml`; `flow.json` | DESIGN §5 TP11; LOGIC L1 | FIX (§5 TP11) | Add the one-line plan to 07 and a `facts.yaml` guard. Repoint 04:831 at what chapter V shows (the sealed wing and the crystals) | `CANON` `FACTS` |
| **L-025** | The Root is written as a refuge that "the Uninvited will not enter". That contradicts the trap divergence (you can't lure them across a threshold they won't cross), and it is never seeded to players | 04:706–711; 05:50–55; 08:90; 10:172; 05:1124–1136 | LOGIC L1, P2-12, clue row 7; REVIEW A7 | FIX (§5 TP8) | The Root is Raunu's gift-research workshop. Its effect on the Uninvited is a side effect, and they don't know to avoid it. Rewrite the four sites so that an Uninvited who enters or is lured in is caught by the deep crystal (the Root-trap End, §3.4). Don't claim Raunu knows of the effect (R-07) | `CANON` `FACTS` |
| **L-026** | The Court's garden doors are open at midnight and lead to an unlocked river gate. That breaks S3's "trapped at a barred gate" and the Crossing's "dark, empty terraces" | 05:150; 08:38; 05:382–384; 08:189–190; 05:861; 09:866; 09:1596–1597; Table V–3 trick 5 | LOGIC L2; REVIEW A8 | FIX (§5 TP9) | *The Post* and *Only the Doors* name both sets of doors, and he shadow-steps between them. Retarget trick 5. The crowd leaves only by the service doors and the gallery-side door until he turns, is Stopped or is Ended. State the reward: once the garden doors open, the crowd in the gardens makes the Radiant *Witnessed* at the Crossing. Reconcile "the one open door" with "service doors" | `FACTS` |
| **L-027** | Nobody can get into the east wing at midnight. The Agenda 4 PC has been shown out at the Dead Dance, it is unclear what the first crystal seals, and Anha's passages run into S4's doubled guard | 02:351–353; 04:1318–1320; 05:145–146; 05:501–506; 09:1122–1124; 09:1149–1151 | LOGIC L3, L7 (Anha); REVIEW A9, §5 item 3; DESIGN still-open | RULING (R-01) | See §6 R-01 | `CANON` `FACTS` |
| **L-028** | The book promises "act before midnight" as the solvers' reward, then prints "no" for everything a table would try: warn Corval, warn Raunu, get Veier out early, move guests, skip the Unmasking | 01:423–425; Table I–1 Movement V; 04:825–838; 02:383–384 | LOGIC L6, agency table; REVIEW A10, §7.3 | RULING (R-02) | See §6 R-02 | `CANON` |

### Usability / prep

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-029** | The midnight hour has no tracker, though it runs on ~20 pieces of live state (more once threat marks, Stops used and the dial are added) | 08:58–129 | USABILITY P1-2, §5.2; REVIEW A11 | FIX-NEW | Add a one-page Midnight Tracker. It holds three Delay tracks with their arrival lines (three-player numbers first), the Attendant's state, breaks and HP, a tells grid, threat marks, Stop used per scene per Uninvited, End attempts, ward-point boxes, the dial word, and the S3 clocks | `FRI` |
| **L-030** | The "90-minute" prep box takes 138 minutes as written and 175–205 as implied. It leaves out the Fractures and S11, the one card live by default, and says both to skip chapter VII and to skim it again | 01:3–36; 01:28 vs 01:551–553; 01:30; 09:478–479 | USABILITY P1-1, §2; REVIEW A12 | FIX-NEW | Re-cost each step honestly, add a true 60-minute path and a five-block "know these" list, put Slow / Stop / End and S11 in, and fix the chapter VII contradiction. No edit makes 100k words preppable in 90 minutes; the prep path has to carry the product | |
| **L-031** | The 4 h 50 runtime is ~5 h 40 at three (S14 alone takes 40–60 minutes). The cut list never names S14, and Table I–1 is "for four players" | 01:180–207; 08:13–30; 09:1787; 04:446 | USABILITY P1-5, §3; TUNING F15; LOGIC L7 (runtime); USABILITY §5.4 (3–4); REVIEW A12 | FIX-NEW | Make the three-player runtime the printed column (TP10). Add S14 and the dark-hour cards to the cut list. Any S14 cap must end with the errand *completing* (the Uninvited finish the room), never with the party let off | `DIAL` |
| **L-032** | The gallery geometry (R2's N4) is still open. No stair reaches B3, and the S11 and B4 doors are drawn in a gallery wall 12 ft up, so the crowd can't reach the default midnight card. The toast sightline to the dais and the slingers' view of the wing corridor don't work either | Map VIII–3; 05:177, 384; 09:1510; 04:1170–1172; 05:925–926; 04:1160–1161 | USABILITY P1-4, §4; LOGIC P3-3, P3-4; REVIEW A9 (N4) | FIX-NEW | Settle the values once in `facts.yaml`: two gallery stairs, the S11 and B4 doors at floor level under a mezzanine, and the galleries overlooking the dais. Redraw VIII–3 and fix its caption. Move or cut the slingers' line of sight | `FACTS` |
| **L-033** | It can't be printed as shipped. The sheet is "two pages" of six-column tables (really 3–4), there are five loose map files, the handouts carry DM italics and have no cut lines, and there is no HTML/PDF build | 08:3–5; 08:289–290, 317; `tools/` | USABILITY P1-6, P2-9, P3-3, §6 | FIX-NEW | Make a print build (Markdown → HTML/PDF) with a DM packet (sheet, tracker, maps), a player packet (handouts with cut lines) and a card deck with each card's stat blocks appended (the AL appendix convention) | |

### Voice

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-034** | Colon chains and splices run at ~10× the reference rate, and semicolons at ~25× | e.g. 04:62–64, 04:112–114, 05:1109–1111, 04:83–85, 04:739–741, 05:56, 07:203–204, 07:437 | VOICE P1-1, R3, R4, R12; REVIEW §3 | FIX-NEW | A light de-patterning pass, judged by ear, after the content settles. Turn every second colon in a sentence into a period, and half the rest into a period or "so". Keep the voice (the owner's light-touch rule) | |
| **L-035** | Designer commentary and aphoristic kickers sit on the DM page ("a load-bearing sentence", "This is the crescendo", about 26 moral closers) | 01:459–464; 05:568–570; 05:719–720; 05:727–730; 05:806–807; 05:980–989; 07:554, and the kickers listed in VOICE | VOICE P1-2, R1, R2, R9–R18; REVIEW §3 | FIX-NEW | Cut the meta and keep the instruction. Keep the kickers that earn their place (01:428–429, 01:449–450). R17 must now say "horses", not "carter" (TP12), and R13 and R16 have to fit the L-004 rewrite | `CANON` |
| **L-036** | Chapter I uses Delay, Fractures, the Wept and the Bought before anything defines them, and there is no glossary for ~40 invented terms | 01:399–402; 01:479–493; 01:177, 405 | VOICE P1-3, R22, jargon note; REVIEW §3 | FIX-NEW | Add a "Words of the Night" box to ch I with about 15 lines, now including Slow / Stop / End, threat (marked), and the dial. Gloss Delay and the Wept inline at first use | |

---

## 3. P2

### Climax / Uninvited

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-037** | *Clears the Way* has no timing and keeps working while the Attendant is Incapacitated or Commanded. Which of the Wept and the Attendant acts first changes the result (35% vs 24% win). Control spells on the Attendant are unaddressed: *Sleep* auto-fails, *Hold Person* can't target a Construct | 10:217–260 (256); 10:210; 09:1782 | RULES P2-2; TUNING F11 | FIX (§4 timing, "costs the action") + FIX-NEW (control note, tie rule) | Under §4 it uses a turn's action, at the start of that turn, so a lost turn means no clearing. Add a two-line S14 control note: *Sleep* fails; *Hold Person* can't target it; a turn lost to *Command* or *Laughter* counts as a lost turn but not toward the four breaks. Add a tie rule: the Wept acts first | `SIM` |
| **L-038** | The Attendant has no rule for a split party, and with no Uninvited in the scene its Focus test is vacuously false, so it stays Idle for ever | 08:39; 09:1759–1761; 09:1786; 10:217–224 | LOGIC P2-14; RULES P1-1 (vacuous case) | FIX-NEW | "It goes to the first Uninvited the party interrupts and stays in that scene; it cannot be in two. With no Uninvited left in the scene it follows the nearest one, or leaves (*Not Here*): the card ends, no XP." | |
| **L-039** | Progress is counted two ways that never meet: turns (Delay, the Midnight Clock) and Speed (*Witnessed*, *Slow*, *Ray of Frost*, and now the Radiant's Stop at Speed 20). DMs will run it both ways | 05:78–86; 05:244–246; 10:1444–1449; 10:158 | RULES P2-3 | FIX-NEW | Add to Buying Time: "an Uninvited whose Speed is halved, or cut to 20 ft or less, for a whole turn makes half a turn's progress; two such turns are 1 Delay (subject to the §3.2 cap)." Make "nothing slows him below 20 ft" a global clause on the Radiant | |
| **L-040** | Down, Not Out doesn't say what later damage (crossfire, *Put Aside*'s Emanation, trample, area spells) does to a set-aside, Stable creature | 05:206–209; 05:631–647; 10:283; 05:377–379 | RULES P2-5 (first half) | FIX-NEW (adjusted) | State it per dial. At Gentle, a set-aside creature takes no damage until it is up. At Sharp and Merciless the rules as written apply: damage is a death-save failure and ends Stable, and the Uninvited still never *target* a set-aside creature. RULES' blanket "takes no damage" softens risk and is used at Gentle only | `DIAL` |
| **L-041** | The claim that S14 at three "usually times out" because neither winning route fits six rounds, and that protecting Raunu (keeping Delay up) prevents breaks | 09:1782–1793; 09:1787; 09:1823 | USABILITY P2-1, P1-5 (S14 part) | DISPUTED | TUNING's sims (2–6k runs on the book clock) show engaged distraction wins 90–96% at three within the six-round errand. A timeout happens only on the late-firing (tight) clock. The tension between Delay and Focus is real, but it is the design. Its fix (three breaks, DC 17) is superseded by §4 (DC 18, Help applies). Re-check in the S14 re-sim | `SIM` |
| **L-042** | Delay is weaker at three (~1.5–2 banked against ~3 at four), and the three-player line double-dips: an extra Wept turn *and* a 20 lump, which is 6.7 per PC against 7.5 per PC at four | 05:285–297; 05:291–292 | TUNING F10 (weaker at three); RULES P3-13 | SUPERSEDED (§3.2) | §3.2 keeps "20 at three (30 at four), unchanged" and adds theme doubling and the three-turn cap, so the per-head rate is moot. Confirm the extra Wept turn in the S14 re-sim | `SIM` |

### Combat & risk

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-043** | S14's "a table built to hit hard: 300 HP" isn't scaled by party size, and "use one line" leaves a trio choosing between 180 and 300 | 09:1808–1812; 09:1927; 09:96 | TUNING F8 | FIX-NEW | Print a three-player value for the hit-hard line, set by the §4 re-sim (TUNING suggests 235; the lethal Focused drops may move it), and say that it combines with the party-size line | `SIM` |
| **L-044** | Withdrawn roster softenings: S10 to Maiven + 1 slinger with two attacks (F6); S8 breaking at one down (F7); S3's captain arriving in round 4 at three (F9, USABILITY P2-2) | 09:1494; 09:1298; 09:883–884 | TUNING F6, F7, F9; USABILITY P2-2; REVIEW §4 | WITHDRAWN | Withdrawn by TP2 and DECISIONS. The rosters stand, and the labels are corrected upward under L-016 | |
| **L-045** | S11 turns every guest through the held door into 100 carry-out XP: four rounds earns ~4,800. Table I–4 is also a Movement VII row | 09:1583–1584; 09:1558–1560; 01:318 | USABILITY P2-3 | FIX-NEW | "Holding the door counts once, as one person carried out, for each character who held it." | |

### Three-player baseline

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-046** | Agenda-dependent beats vanish at three and nothing tells the DM. Anha empties the galleries only with Agenda 8, and the S11 out, DC 13 ward-steering (Agenda 5), the S8 out (Agenda 2) and the Agenda 6 reveal all hang on agendas too. Three snake cooling exits are agendas. The Root's key (the B8 lock) is fragile without Pello | 05:922–924; 09:1562–1563; 05:37–41; 09:1269–1271; 02:389–392; clue row 6 | LOGIC L7, clue row 6; TUNING §6, F16 | FIX-NEW | Add a one-line "beats that vanish at three" note to the DM sheet, and a fallback for each cooling exit (its −1 boxes). Point at the non-Pello routes to the Root (S8's wardens, the keys, the DC 18 Arcana check) | |
| **L-047** | Movement V's "one card per group" has no time budget, so a split trio can run three fights in 40 minutes | 09:505–512; 04:1324–1328 | USABILITY P2-10, §5.4 (12) | FIX-NEW | "Past 2:40, at most one card on screen; the others resolve offstage *with their consequence* (clock filled, heat moved)." That keeps the risk and only cuts table time | `DIAL` |

### Story logic

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-048** | The book never says what the Uninvited meant to do about the unborn child ("kill Veier… carry away the child she is about to deliver"), which matters for how the Radiant acts at the Crossing and under the Last Rite | 02:154–155; 01:77; 05:964–965; 01:540–545 | LOGIC P2-5; REVIEW §5 item 8; DESIGN still-open | RULING (R-03) | See §6 R-03 | `CANON` |
| **L-049** | Selling Callun the nursery sets the Circle to heat 4, and the consequence is S12, a minister kidnapped over the Tithe: a non-sequitur. 06 still says "the pregnancy never gets out" | 09:184–185; 09:175; 08:55–56; 06:28–32 | LOGIC P2-11; REVIEW §5 item 8; DESIGN still-open | RULING (R-04) | See §6 R-04 | `CANON` |
| **L-050** | Raunu's knowledge: does Raunu know the Root catches the Uninvited? TP8 leaves it unstated, and the integrator asked for confirmation | DESIGN §5 TP8 (note); 05:55 | DESIGN TP8; LOGIC L1 (option a) | RULING (R-07) | See §6 R-07 | `CANON` |
| **L-051** | Nobody has said whether the Attendant, which is not Leashed, enters the Root, or what the Root does to it | 05:1124–1136; 10 Attendant | LOGIC P2-12; REVIEW §5 item 8 | RULING (R-06) | See §6 R-06 | `CANON` |
| **L-052** | Vell's sword: chapter V says the wrapped sword "stays on his back"; chapters VII and X say he fights the Radiant with it still bound | 05:564–565, 577; 07:520–522, 566; 10:2141–2142; INVENTIONS #66 | LOGIC P2-3 | RULING (R-08) | See §6 R-08 | `CANON` |
| **L-053** | How does Vell get into the boat? He is behind the Radiant when the boat pulls out, yet "a pale man rowing hard into the dark" | 05:597–600; 05:616; 07:559–560; 10:2118–2121 | LOGIC P2-4 | FIX-NEW | Add one sentence using his printed *Elsewhere* action: when the Radiant breaks past, Vell is already at the oars. Check it against the Last Rite rewrite (L-004) and TP12's route north | `CANON` |
| **L-054** | Agenda 6's reveal ("the reason mother and child got out") is false, since Vell "always has a second way", and no scene carries it to the player | 02:389–392 (now ~391–394); 04:1363–1365 | LOGIC P2-6, clue row 10, agency table | FIX-NEW | Reword it to "one of the reasons, and the one that let Vell spend his second way on something else". Add a gate beat in which Vell looks at that character, drawn only from 07:556–560's printed "crack in the ice" | `CANON` |
| **L-055** | "Both rivers, one spring", the only place the night says why the child matters, sits behind the most cuttable thread (Undercurrent A, the B8 lock or DC 18 Arcana) | 04:692–696; 01:204; 04:574; 04:643–644; 07:275 | LOGIC P2-7, clue row 3 | RULING (R-09) | See §6 R-09 | `CANON` |
| **L-056** | The endings are indistinguishable: one epilogue box is written for the default history, and "each of you dreams of dancing" gives everyone a memory only one character has | 05:1059–1072; 04:1376 | LOGIC P2-8, agency table; VOICE P2-4 (epilogue) | FIX-NEW | Add an endings box that sets the printed state variables against one replacement sentence each: Raunu, Maiven, Corval and the minister, Vorlain, slate and drawer, the Bought, the Wept looked back, the Hollow sent home, and now the Last Rite. Change the dream line to "the one she danced with" | |
| **L-057** | The bell sequence confuses the DM. The "last bell" (the leash's hard limit) waits on a gate clock that counts only the party's rounds, and 04:90–91 points to a Bought bell schedule the DM sheet doesn't have | 05:62–63, 83, 90–95; 02:131–133; 10:131–132; 09:783–791; 04:90–91 | LOGIC P2-9; USABILITY P2-4, §5.3 (1) | FIX-NEW | Put a one-line bell glossary on the DM sheet and tracker. Reword the S3 clock as "the sect guard's arrival", with the last bell as its signal. Print the Bought's schedule at 04:90 (from 05:1180) or cut the pointer | |
| **L-058** | Voiding the contract because "the target is gone" doesn't follow from the clauses, and the Second Clause's "send word to the river" dangles, now beside TP12's river route | 05:961–965; 05:1020–1022; 07:730–731; 07:749; 09:852–854 | LOGIC P2-10 | RULING (R-10) | See §6 R-10. The captain-route reword is FIX-NEW whichever way R-10 goes: "the clause he was really paid for is dead; he won't hold a gate for a fee's leftovers" | `CANON` |
| **L-059** | Agenda 3 has no completion condition. Vorlain never says anything incriminating sober, so a player who wins the drinking check can't tell whether they got "the understanding" (200 XP and Heroic Inspiration ride on it) | 02:325–330; 07:149–151, 179–187; 09:291, 470 | LOGIC P2-1 | FIX-NEW | Name what counts: any drunk line, carried to Draunel and *framed* as an understanding (Deception DC 13 against Draunel). Leave what it does to Vorlain at dawn to the existing aftermath text | |
| **L-060** | Table I–2's Patron's Errand says "your patron is also a snake" and lists *The Cousin's Errand*, but the Thenya are "not a snake" everywhere else, and it is Ilesse's suggested hook | 01:237 (verified); 11:22; 02:356–358; 09:397–412 | LOGIC P2-2 | FIX-NEW | Change it to "…your patron may be a snake", or drop *The Cousin's Errand* from the fits and give Ilesse *The Entourage* | |
| **L-061** | S10's slingers rope up a 20-ft wall to a lit window beside two stairs, and nothing says the garden stair's top door is shut | 09:1430–1435, 1451–1452, 1462–1463; 05:457–459 | LOGIC P2-13 | FIX-NEW | Settle the door's state in the N4 `facts.yaml` pass, with the owner confirming the physical fact, then add one terrain line to S10 | `CANON` `FACTS` |

### Usability / prep

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-062** | Map residue: "other positions approximate" on four maps; VIII–1 still a schematic (N11); the rail drop is 12 ft on one map and 10 ft on another; "second floor" vs gallery level for S10's window; undrawn places (high gallery, musicians' gallery, B4 antechamber, dais and door ward-points) | VIII–1–VIII–5; 09:1431; 04:1016, 231, 1141; 05:306 | USABILITY P2-6, §4; LOGIC §0 (N4, N11) | FIX-NEW | Decide each value once in `facts.yaml` and redraw. Give the walk rail its own symbol. Draw the four dais and two door ward-points that Tables V–2 and V–3 count | `FACTS` |
| **L-063** | Chapter VII is the at-table reference but runs to 7,800 words of prose, so "what does Essin want?" takes a minute | 07 throughout | USABILITY P2-7 | FIX-NEW | Open each entry with a two-line cue (wants / where at midnight), drawn from the printed entry, or add a one-page cast roster to the DM packet. The voice line is R-11 | |
| **L-064** | The pregens aren't sheets a new player can use: no trackers, no spell text, a shared preamble that is lost when one sheet is printed, and no "on your turn" line | 11 throughout; 11:33–43 | USABILITY P2-8, §7 | FIX-NEW | In the print build, merge the preamble into each sheet and add trackers, one line per spell, and an "on your turn" line | |
| **L-065** | The flow page is outside the DM's path. It is a design map (111 nodes, no print stylesheet) with repository-path references and a provenance footer | `flow/oraga_night_flow.html`; README:89 | USABILITY P2-11, §8, P3-9 | FIX-NEW | Keep it out of the DM's path, labelled a contributor tool, or build a one-page printable "night at a glance". Strip the repo paths from anything a DM sees | |
| **L-066** | The number of snakes to show per Movement is stated three ways: "one or two", "default one", "one snake line" | 04:908, 975, 1133; 09:71; 04:940 | USABILITY P2-12 | FIX-NEW | Say "one" everywhere and put the dial in one place. Align it with the heat-4 "they come for you" rows (L-011) | |

### Rules accuracy

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-067** | Social spells hit NPCs who have no saves: "NPCs make no checks", but spells force saves, and the noncombatants have AC and HP only. Casting *Suggestion* unseen isn't clearly steel | 01:275–276; 10:2026–2057; 10:2042–2043; 09:119–124 | RULES P2-4; REVIEW §7.2 (still stands) | FIX-NEW | Add one save line per noncombatant (Wis and Cha), and "saving throws are not checks; NPCs roll them". Casting with Verbal or Somatic components in a guest's view is noticed on DC 13 Perception, and noticed means steel. Any Charmed immunity for Raunu needs the owner's nod | `CANON` |
| **L-068** | Success at a cost has no scope, and chapter I gives it two strengths ("may offer" vs "always arrives") | 01:269–273; 01:513–516 (verified) | RULES P2-6 | FIX-NEW | It applies to talk and exploration before midnight. It doesn't apply to Delay tricks, Stop, End (which has its own band), ward-steering, Attendant distractions or Very Hard DCs. Change 01:515 to "arrives, if you offer it". This raises difficulty, consistent with TP2 | |

### Voice

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-069** | Overloaded terms. "Tell" covers three systems, and "line", "clock" and "iron" are each used several ways. "The fourth iron" appears before chapter IX defines the irons | 01:300; 05:732ff.; 05:869, 896; 09:262 | VOICE P2-1 | FIX-NEW (one sub-point DISPUTED) | Write "Fracture tell" (or whatever the Slow / Stop / End rewrite names it) every time. Spell out "threat line" at first use. Consider "Midnight Order". Move the gloss of "the fourth iron" before the term. **Disputed sub-point:** 07:415's "three other irons … chapter IX names all three" is consistent, because three plus Agenda 3 makes IX's four (09:262–268 lists Agenda 3 as iron 1) | |
| **L-070** | B5 (the Crossing's ground) and B8 (the study) have no read-aloud, nor do B3, B7 and B10 | 04 B3, B5, B7, B8, B10 | VOICE P2-3; REVIEW §3 | FIX-NEW | Write 35–50-word boxes for B5 and B8 at least, using only printed details | `CANON` |
| **L-071** | Read-aloud slips: one box decides an action (04:231–232), one is vague (04:255–256), one editorializes (04:1343–1344), and "a something-to-say" reads as a typo | 04:231–232; 04:255–256; 04:1343–1344; 05:1065–1066 | VOICE P2-4, R5–R7, R20 | FIX-NEW | Apply R5–R7 and R20. The dream line is handled in L-056 | |
| **L-072** | Blank-cheque phrasing: 06's "larger at your discretion" gives no default | 06 Rewards (the Church's favor) | VOICE P2-5 | FIX-NEW | Pair it with a default ("one favor; double it if…") | |
| **L-073** | Second-tier NPCs (Kovaun, Callun, Draunel, Essin, Maiven, Anha, Tavva, the Sergeant, the Captain) have traits but no line to speak, and three share the "forgettable on purpose" note | 07:263, 301, 363, 418–420, 443, 473, 671, 722, 752 | VOICE P2-2, R19; REVIEW §3 | RULING (R-11) | See §6 R-11. VOICE says the owner should write or approve the quotes, because they are voice, not structure | `CANON` |

---

## 4. P3

### Climax / Uninvited

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-074** | Attendant edge rules. A distraction tried while it is Idle burns the trick for at most one turn of being ignored. A natural 20 while Idle does nothing (N27). *Literal Orders* resets twice a round under *Two Turns*, which opens targeting windows | 10:226–241; 09:1859; 09:1878 | RULES P3-10 (N27), P3-11, P3-12 | FIX-NEW (fold into the §4 rewrite) | "A trick tried while it is Idle isn't spent." Give the natural 20 an Idle effect, or cut it. Change "since the end of its last turn" to "since the start of its previous round". Check all three in the S14 re-sim | `SIM` |
| **L-075** | A spell can carry the Fracture's words (*Message*, 120 ft), but invoking needs the speaker within 30 ft | 05:826; 05:742–743 | RULES P3-6 | FIX-NEW | §3.3 keeps "within 30 feet where they can hear". Say that a carried voice doesn't count | |
| **L-076** | Vell's immunities don't match "Nothing holds Vell". *Hold Person* can land at the Crossing (~4%) and open ⟨The child is taken⟩ by accident | 10:2084, 2110 | RULES P3-5 | FIX-NEW | Add the Paralyzed, Stunned, Incapacitated and Unconscious immunities, or give *Beyond Reach* "no spell or effect stops him taking his action" | |

### Combat & risk

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-077** | The read-aloud head counts contradict the three-character lines: S2 says "four people", S11 "three big men", S13 "three men". S9's three-player line drops the veteran but its Nastier line still uses him, and its one-side fights are unstated | 09:649; 09:1519; 09:1661; 09:1403–1406 | TUNING F13; REVIEW §4 | FIX (§5 TP10) | At the three-player baseline the boxes print three-player counts, and the four-player count goes on the adjustment line. Settle S9's one-side rosters and its Nastier line | |
| **L-078** | S14's "how it plays" note says slugging "fairly often" ends with the whole party down. That never happened above 4% in the sims under the old rules | 09:1816–1818 | TUNING F14 (note) | FIX (§4 re-sim) | Rewrite the note from the lethal re-sim's numbers, giving a rate for each dial setting. TUNING's "soften to 'usually goes its way'" may no longer apply once Focused drops can kill | `SIM` `DIAL` |
| **L-079** | Withdrawn: S4's three-player line as one guard, with the second arriving in round 2 | 09:943 | TUNING F12 | WITHDRAWN | It softens a fight. DECISIONS lists S3, S8 and S10 by name; S4 is the same kind of change (confirm in TASKS). Correct S4's label upward instead (L-016) | |
| **L-080** | The balustrade is a one-Shove removal: 1d6, Prone and out of the scene, with full XP | 09:1365–1366 | RULES P3-16 | FIX-NEW | Add "unless it makes a DC 13 Strength (Athletics) check to catch the rail", or "climbs back next round" | |
| **L-081** | The non-lethal house rule has no result. Is it the SRD's 1 HP and Unconscious, or the palace's "0 HP, Stable"? Does it reach area spells? | 09:125–128; 10:36–42 | RULES P3-15 | FIX-NEW | "As the SRD's Knocking Out a Creature, for any attack roll; never for an area effect." | |
| **L-082** | In 2024, *Sleep* only Incapacitates on the first failure, so "dropped into a crush… on the floor at the end of the round" fires a round early | 05:376–379 | RULES P3-7 | FIX-NEW | "Anyone left Unconscious on the floor at the end of a round" | |

### Three-player baseline

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-083** | Four-player assumptions in passing: "two [summoned] should be PCs" is two-thirds of a trio, and "lands close to 6,500 XP" is the four-player total | 04:1038; 01:322 | USABILITY §5.4 (10–11) | FIX (§5 TP10) | Restate both for three, with four on the adjustment line | |
| **L-084** | The five-at-5th scaling rule reads differently in two places | 05:289; 09:96–97 | USABILITY P3-7 | FIX (§5 TP10) | Rewrite the party-size rule once, three-player first, and reference it from both places | |

### Story logic

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-085** | Corval's guard doubling is inconsistent. A forced wing "stays doubled for the rest of the night", but Table VIII–7 has two guards at midnight (R2 P3-22) | 04:79–81; Table VIII–7 | LOGIC P3-1, §0 | FIX-NEW | Add the forced-wing case to Table VIII–7 ("four if the wing was forced"), or drop "for the rest of the night" | |
| **L-086** | Table VIII–6 says "Wept: east doors", but the tell is at the *east-wing* doors, 60 ft and a stair away (R2 P3-21) | 08:243 (verified); 05:769 | LOGIC P3-2; USABILITY P3-2, §5.3 (2) | FIX-NEW | Change it to "Wept: the east-wing doors" | `FRI` |
| **L-087** | The midwife has no midnight position, and the two Tithe ministers are never placed or named, though Agenda 1, S12 and Corval's line turn on them | 06:28–29; Table VIII–2, VIII–6; 02:294–296 | LOGIC P3-5, P3-6 | RULING (R-12) | See §6 R-12 | `CANON` |
| **L-088** | "Raunu summons four guests all night" and "he is seen exactly four times", but dinner is a fifth, private appearance | 04:1037; 07:21 | LOGIC P3-7 | FIX-NEW | Add "publicly" | |
| **L-089** | Where are the slingers at midnight under the default S4/S10 run offstage? The S4 guard count in Movement V and the S10 box's two slingers against three fielded are still open from R2 (P3-24, P3-25) | 08:218–221; 05:877; 04:72–74 | LOGIC P3-8, §0 | FIX-NEW | Add to S10's Development: "the cell opens at the lights; her slingers are with her". Align S10's box count with its three-player line. Settle the S4 count | |
| **L-090** | Vell's midnight route is odd: he is at the river gate at the end of Movement V, then goes "service passages → garden stair → the river gate" | 08:42 (verified); 05:171–173 | LOGIC P3-9 | FIX-NEW | Add one line: he climbs back to the foot of the garden stair to meet her. Check it against TP12's boat (unchanged) | `CANON` |
| **L-091** | The Radiant reaches the garden stair "three beats after Raunu falls", though he has been in the wing since the first beat, so the chase runs 5+ beats against Speed 15 with no reason given | 05:84–86; 05:501–506 | LOGIC P3-10 | FIX-NEW | One sentence: the first crystal's seals plus *Witnessed* account for it. Write it after R-01 decides what is sealed | |
| **L-092** | Agenda 2's "the Prelate will know if you shade it" has no mechanism, and the agenda asks a question the module refuses to answer | 08:329–330; 02:235 | LOGIC P3-11 | FIX-NEW | Add a DM line: any sincere judgment completes it, and a shaded one is caught on the Prelate's Insight (printed) or a fixed DC. Don't add lore | |
| **L-093** | The claim that "the Undercurrent C find is the secret the ballroom is guessing at" (04:770) contradicts 02's "the ballroom guesses a trade decree" | 04:770; 02:176–180 | LOGIC P3-12 | DISPUTED | No contradiction. 02:176–180 says the ballroom guesses at the midnight pronouncement and guesses *wrong* (a trade decree), "the truth is upstairs". 04:770 names that truth. At most, a voice-pass clarity tweak | |

### Usability / prep

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-094** | "The palace diagram" survives as a single object, though it is now five maps. 08:3–5's "print the first three pages" no longer matches | 01:16, 109; 04:50, 407 (all verified); 08:3–5 | USABILITY P3-1, P3-3, §5.3 (3) | FIX-NEW | Use "the maps (VIII–1 to VIII–5)". Rewrite the print line to match the print build (L-033) | |
| **L-095** | Nine cross-references are vague enough to cost a flip: 04:1424, 04:1043, the six "→ chapter IX" snake pointers, and 05:226 "'Leashed'" (a trait printed three times) | as listed | USABILITY §5.3 | FIX-NEW | Name the section, table or row in each | |
| **L-096** | Four Attendant sightings show "one of its three habits" each, so one habit repeats unstated | 04:896–897 | USABILITY P3-4 | FIX-NEW | Say that the Movement V glint repeats the crystal-and-light habit. Fold this into the L-001 tells column | |
| **L-097** | Table V–5 row 2 assumes S9 already happened ("the duel has already smashed the balustrade") | 05:357 | USABILITY P3-5 | FIX-NEW | Add "(or the Crossing's first beat did)" | |
| **L-098** | The automatic heat ticks are marked ✱ in Table VIII–5 and in italics in Table IX–2 | Tables VIII–5, IX–2 | USABILITY P3-6 | FIX-NEW | Use one notation | |
| **L-099** | A gate draw goes to S4 on the DM sheet, but S4's terrain is the east-wing corridor | 08:18; 09:899–902 | USABILITY P3-10 | FIX-NEW | Add to S4's *Where and when*: "run in B1 on a gate draw; the corridor terrain doesn't apply" | |
| **L-100** | Open R2 polish: "Svara" unglossed (01:438), the skill list given three ways (07:527, 08:117), designer "yardstick" commentary (09:1796–1802, 10:313), and the Prickle against an unseen attacker's Advantage (N28) | 01:438; 07:527; 08:117; 09:1796–1802; 10:313; 03:110–111 | USABILITY P3-8; RULES P3-10 (N28) | FIX-NEW | Clear them in the sweep. Gloss Svara only with printed facts. Rule N28 in one sentence | `CANON` |
| **L-101** | Missing player handouts: a sketch of the public rooms, and a one-page "tonight's customs" (no disarming, masks, the Unmasking, the Dead Dance) | 08 | USABILITY §6 | FIX-NEW | Build both from printed text and the public-room maps only. Add them to the player packet | `CANON` |

### Rules accuracy

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-102** | Dassa's breastplate (400 GP) is out of reach of 2024 starting equipment. Three pregens carry three common charges and two carry none, against the guide's one each | 11:293, 342 | RULES P3-1 | FIX-NEW | Give Dassa chain mail (AC 17) or scale mail (AC 16, Stealth Disadvantage), or state the breastplate as a gift. Even out the charges. Re-run `pregen_check.py` | |
| **L-103** | Three grapples are made with no free hand (the Honor Guard's *Seize*, the Warden's *Seize for Questioning*, the Blade's *To the Terms*) | 10:456; 10:701; 10:514–517 | RULES P3-2 | FIX-NEW | "It lets go of its weapon to do this", or "it grapples with its shield arm" | |
| **L-104** | Serane's Bardic Inspiration leaves out "another creature" and "see or hear", and her *Vicious Mockery* leaves out "before the end of its next turn" | 11:94–96; 11:90–91 | RULES P3-3, P3-4 | FIX-NEW | Copy the SRD 5.2.1 wording | |
| **L-105** | Midnight charge text: "feels it go cold and quiet" reads as if charges die, while the sidebar says only releases within 30 ft are at risk | 05:139–142; 05:183–189 | RULES P3-8 | FIX-NEW | Add "(it still works; see the sidebar)" | |
| **L-106** | *A Veil of Quiet* and *Dark-Burst* don't say whether the effect moves with a carried crystal. That matters more now that darkness feeds the Radiant and the Last Rite | 10:2189; 10:2195 | RULES P3-9 | FIX-NEW | "The effect stays where it was released." | |
| **L-107** | Format and labels: the "—" alignment on the Uninvited and Vell isn't an SRD form, and it is unstated whether the Orthaen *Gift Knack* gives Advantage on a crystal distraction | 10 (alignment lines); 03:90–91; 09:1830 | RULES P3-17 (the rest is in L-016) | FIX-NEW | Use "Neutral" or "Unaligned". Rule the Gift Knack question in one sentence | |

### Voice

| ID | Defect | Where | Sources | Disp. | Proposed fix | Flag |
|---|---|---|---|---|---|---|
| **L-108** | Rhythm tics: "the way X" similes (~4× the reference rate), "not running, arriving" three times, ~10 verbatim flourishes reused across chapters, and 15–19% of sentences at six words or fewer | 04:1017, 1220, 827; 07:662, 148; 05:149, 565; 07:550–551; tic table | VOICE P3-1–P3-3, tic table; REVIEW §3 | FIX-NEW | Part of the voice pass. Keep the two best similes, keep "arriving" only in the read-aloud (INVENTIONS #66), and in a chapter that repeats a fact, repeat the fact and drop the flourish | |
| **L-109** | Player Handout 1 repeats "revelry" and "look forward" within one sentence. The text is marked canonical | 08:303–307 | VOICE P3-4 | RULING (R-13) | See §6 R-13 | `CANON` |
| **L-110** | The Captain's roleplaying line ("it shows in both directions") is unclear | 07:752 | VOICE P3-5, R21 | FIX-NEW | Apply R21 or similar, with no new facts | |
| **L-111** | The DC ladder's tier names (Standard 13–15, Hard 18–20) differ from the SRD's labels, and it is the only place a DC range appears | 01:252–262 | VOICE P3-6 | FIX-NEW | Cosmetic: align the names, or leave them with the existing explanation | |

---

## 5. Summary counts

| Severity | FIX | FIX-NEW | SUPERSEDED | WITHDRAWN | DONE | DISPUTED | RULING | **Total** |
|---|---|---|---|---|---|---|---|---|
| **P0** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| **P1** | 19 | 10 | 0 | 2 | 1 | 0 | 3 | **35** |
| **P2** | 1 | 25 | 1 | 1 | 0 | 1 | 8 | **37** |
| **P3** | 4 | 30 | 0 | 1 | 0 | 1 | 2 | **38** |
| **Total** | **25** | **65** | **1** | **4** | **1** | **2** | **13** | **111** |

**Notes on the counts.**
- Each row is counted under its primary disposition.
- L-037 is FIX, though it carries FIX-NEW extras. L-069 is FIX-NEW with one disputed sub-point.
- L-005 and L-058 have FIX-NEW parts that wait on R-05 and R-10.
- The superseded and withdrawn *proposed fixes* inside rows count under their row:
  - RULES' Delay cap and Raunu "blow" fix, and TUNING's F10 cap, are in L-003 and L-005;
  - USABILITY P2-1's DC 17 fix is in L-041;
  - LOGIC L4 (a)–(c) is in L-004.
- Compared with REVIEW §0's estimate (P0 1 · P1 13 · P2 ≈30 · P3 ≈45): P1 grew because the
  owner's direction added the risk and Slow / Stop / End findings (§7.1, §7.2). P3 shrank
  because rows were merged.

---

## 6. Owner rulings needed

> **Answered 2026-10-21.** All thirteen are ruled; see DESIGN §6 and DECISIONS TP13–TP26.
> R-01 → TP13 · R-02 → TP14 · R-03 → TP15 · R-05 → TP16 · R-06 → TP17 · R-07 → TP18 · R-08 → TP19 · R-09 → TP20 · R-10 → TP21 · R-11 → TP22 · R-12 → TP23 · R-04 → TP24 · R-13 → TP26. Veier is never met directly (TP13), which adds rewrite work to WP4 and WP7; history breaks at the boat only by stopping it (TP25).

Thirteen questions. The first four are the DESIGN's "still open" list plus the integrator's note
on TP8, and R-05 is the unanswered DESIGN §5 Q2. Each option is a choice for the owner, not a
claim about canon. Where an option names a position or a line, it is an example to approve or
replace.

### R-01. How does anyone get into the east wing at midnight? *(L-027; DESIGN still-open; LOGIC L3)*

**Background.**
- Agenda 4 promises a character "beside Veier at the Unmasking" (02:351–353), but dinner ends
  with Corval showing that guest out (04:1318–1320).
- At the lights, "the east wing corridor booms shut… sealed from afar" (05:145–146), and the text
  never says which doors.
- Two honor guards hold the east-wing doors (Table VIII–7). Anha's passages are listed as a way
  in, but chapter IX puts the doubled guard behind the wing's service door (09:1122–1124).
- Map VIII–5 draws a service stair and a garden stair.
- The Agenda 4 player stands at the foot of the east stair asking how to reach her, in the scene
  the book calls "where the night has been pointing".

**Question:** At midnight, what is sealed, and how does a character reach Veier and the
Radiant's chase?

- **A. Seal the double doors only.** The first crystal seals the double doors at the head of the
  east stair. The service stair, the wing's service door and the garden stair from the upper
  terrace stay open. This uses only drawn routes (LOGIC's default).
- **B. The Agenda 4 character stays.** If Veier chose them at dinner, she asks them to stay, and
  Corval shows out everyone else. That character is inside when the lights die.
- **C. The wing is fully sealed.** The only ways in are through Anha (the household on the far
  side lets her through with one companion) or a ward-steer at the doors (Table V–2's DCs).
- **D. Cut the promise.** Delete "beside Veier at the Unmasking" from 02. The party meets her
  only once the chase reaches the garden stair.

**Recommended: A and B together.** They don't conflict. B keeps Agenda 4's printed promise, A
adds no undrawn geometry, and neither needs a new character behaviour beyond Veier's request.
Strike Anha from the list of ways in unless C is chosen. Record the answer in `facts.yaml`
(midnight wing routes).

### R-02. What does "acting before midnight" buy, and can Veier leave early? *(L-028; LOGIC L6)*

**Background.**
- 01:423–425 promises the solvers "the chance to act before midnight".
- What the text prints for each attempt:
  - warn Corval: nothing changes;
  - warn Raunu: "I know… stay near the walls", and he does not act;
  - confront the three: they leave.
- Nothing covers the other moves a table will try: getting Veier out early (Vell's gate opens "at
  midnight, not before", 02:383–384), moving guests early, or cutting the Unmasking short.
- TP11: Raunu means to keep Veier in the sealed east wing until the birth.
- TP8: the Root is a trap for the Uninvited, not a refuge.

**Question:** When a table acts on the pattern before midnight, what changes?

- **A. History holds, and early action pays at midnight.** Veier and Raunu decline to move (her
  printed want, his TP11 plan), in character. Each early act gets a visible midnight payoff:
  - guests moved early come off the casualty count;
  - a warned character starts midnight already in position;
  - a convinced Corval opens a door.
- **B. Veier can leave early.** This needs a new ⟨If History Breaks⟩ entry: the Uninvited arrive
  wherever she is, and the Crossing moves (to the river walk, say).
- **C. She can be moved within the palace, not out of it.** For example, she can go down to the
  Root, where an Uninvited who follows is caught (TP8). Vell's gate stays shut until midnight.
- **D. Withdraw the promise.** Reword 01:423–425 to "the chance to be ready when midnight comes".

**Recommended: A.** It keeps the record (TP11, and the escape at midnight) and turns the promise
into payoffs a DM can read off the page. It needs no new branch of history. C is a good addition
if the owner wants the Root trap to be reachable on purpose.

### R-03. What did the Uninvited mean to do about the unborn child? *(L-048; DESIGN still-open; LOGIC P2-5)*

**Background.**
- The errand is "kill Veier… and carry away the child she is about to deliver" (02:154–155;
  01:77).
- The safety section promises to keep certain content away from the table (01:540–545).
- The Second Clause's payer wants "a woman in Thenya wool" (05:964–965).
- Under the threat rule and the Last Rite, the DM now needs to know what the Radiant *does* when
  he reaches her.

**Question:** What is the Radiant doing at the Crossing?

- **A. Leave the "how" unstated.** Treat it as a "the module does not say" mystery, and add a DM
  behaviour line: never narrate an attack on Veier herself; his on-screen violence goes to
  whoever is marked and in his way.
- **B. Take her alive.** They were sent to take her, and the child with her, and the parents'
  deaths were the errand's cover. He moves to seize her, not to kill.
- **C. Labor begins at the lights.** The birth becomes part of the night's clock (this changes
  Veier's Speed and carrying).
- **D. State the printed errand plainly.** He means to kill her and take the child, and the DM
  keeps it off-screen under the safety section.

**Recommended: A.** It adds no canon, honours the safety section, and gives the Crossing and the
Last Rite all the behaviour they need through the threat rule.

### R-04. What follows from selling Callun the nursery? *(L-049; DESIGN still-open; LOGIC P2-11)*

**Background.**
- Callun "fears exactly one thing… an heir" (04:779–783).
- Selling her the nursery sets the Circle's heat to 4 (09:184–185). Heat 4 fires S12, in which
  her knives take a Tithe minister (09:175). That answers the heir with a tax policy.
- 08:55–56 says no faction learns of the child unless a PC tells them, and 06:28–32 still says
  "the pregnancy never gets out".
- It is the night's most morally loaded choice.

**Question:** What does the Circle do with the knowledge?

- **A. Keep S12 as printed.** Add one DM line explaining why the knowledge leads there, with the
  owner supplying the reason.
- **B. A midnight beat of its own.** The knives go for the east wing's service door in the dark,
  into the Radiant's path. This is a heat-4 "they come" row reusing S7's roster (TP2 option 1).
- **C. Aftermath only.** 06 gains a line that the Circle knows, and "the pregnancy never gets
  out" gets its exception.
- **D. B and C together.**

**Recommended: D.** It makes the choice matter on the night and after it, fits the TP2 heat-4
pattern with an existing roster, and removes 06's contradiction. The owner words the aftermath
consequence.

### R-05. When the Wept's End (Mercy) lands, is Raunu saved outright? *(L-006; DESIGN §3.5 "§5 Q2", unanswered)*

**Background.**
- DESIGN §3.5 maps the Wept's End to ⟨They save Raunu⟩, "subject to §5 Q2: Raunu's own choice".
  TP7–TP12 don't answer Q2.
- The printed canon: Raunu dies "by his own choice", spending his last charge sealing doors
  behind Veier (08:40; 02:207–212).
- The current sidebar says the Wept's stopped round "is the one Raunu needs to choose
  differently" (05:1093).

**Question:** After Mercy lands, what decides whether Raunu lives?

- **A. Saved outright.** The Wept leaves the dais and Raunu lives. His charge still seals the
  doors behind Veier.
- **B. The End buys the choice, and the choice has a price.** Raunu spends the twin crystal on
  himself, and it holds him as deep crystal holds them (LOGIC L5). The doors behind Veier do *not*
  seal, so the Radiant gains beats on her, and the party is the only thing between them.
- **C. The End buys the choice, and he must be persuaded.** In that round a character must
  persuade him. Otherwise he spends the charge on Veier anyway.
- **D. The party's call.** After the End, Raunu is wounded and lives only if the party carries
  him clear. No crystal mechanics.

**Recommended: B.** It keeps "by his own choice" literally true, and the price lands somewhere
the table can see: more pressure at the Crossing. It also gives L-005 its numbered steps.

### R-06. Does the Attendant enter the Root? *(L-051; LOGIC P2-12)*

**Background.**
- TP8 makes the Root a trap: an Uninvited who enters is caught by the deep crystal, and they
  don't know to avoid it.
- The Attendant is not Leashed, and nothing says what the Root does to it.

**Question:** What happens when the Attendant reaches the Root?

- **A. It goes where its three go.** It follows an Uninvited in, and the Root does not affect it.
- **B. It won't enter.** Its orders keep it beside the three, so it waits at the threshold. A
  party in the Root is safe from it, but not from an Uninvited who walks in and is caught.
- **C. The Root catches it too.** That is a second trap route, for the boss.

**Recommended: A.** It creates no new safe room, keeps risk up under TP2, and keeps the Root a
trap for the Uninvited only, with the least new fact.

### R-07. Does Raunu know the Root catches the Uninvited? *(L-050; DESIGN TP8 integrator note)*

**Background.**
- TP8: the Root was built for gift research. Its effect on the Uninvited is tangential, and they
  don't know to avoid it.
- The integrator left Raunu's knowledge unstated.
- A table that finds the Root will ask why he didn't use it (LOGIC L1).

**Question:** What does Raunu know?

- **A. Leave it unstated** (the DESIGN default). The text never claims either way.
- **B. He doesn't know.** One DM line says nobody has seen the effect until creatures like these
  stand in it. That answers the table's question.
- **C. He suspects but never tested it.** He won't stake Veier on a guess, which fits his TP11
  plan.
- **D. He knows.** Then the text needs his reason for not using it, supplied by the owner.

**Recommended: B.** One line answers the likeliest question at the table and mirrors "they don't
know to avoid it". If the owner prefers the mystery, A works with a "the module does not say" DM
line.

### R-08. Vell's sword: on his back, or wielded still bound? *(L-052; LOGIC P2-3)*

**Background.**
- Chapter V (and its read-aloud, logged at INVENTIONS #66) says the wrapped sword "stays on his
  back" through the Crossing.
- Chapters VII and X say he fights the Radiant with it still bound (07:520–522, 566;
  10:2141–2142).

**Question:** Which is it?

- **A. Still bound.** He fights with it wrapped. Change 05:564–565 and 577, and the read-aloud
  box.
- **B. On his back.** He holds the Radiant without drawing it at all. Change 07 and 10.
- **C. Both, in sequence.** It is on his back when they meet and wrapped in his hand by the end,
  with one transition line.

**Recommended: A.** It is the stronger image, and only one chapter changes (LOGIC).

### R-09. Should "both rivers, one spring" be reachable outside Undercurrent A? *(L-055; LOGIC P2-7)*

**Background.**
- The only place the night says why the child matters is the Root's orrery (04:692–696).
- It is gated behind the first thread the cut list drops, and behind a DC 18 lock or Arcana
  check.
- Most three-player tables leave knowing that the child mattered, but not why.

**Question:** Should one echo of the figure reach a scene every table plays?

- **A. Anha's echo.** Anha quotes the Root's voice-lattice line as "the master's voice in empty
  rooms". Both lines already exist (04:643–644; 07:275), so there is no new canon.
- **B. Veier at dinner.** She says her husband "says the baby remembers". This is a new line.
- **C. Raunu at the summons.** A beat in his "Something true" answer. This is a new line.
- **D. Leave it gated.** A DM note says most tables won't see it.

**Recommended: A.** It is the lightest option and uses only printed words.

### R-10. Who, if anyone, is "the river" in the Second Clause? *(L-058; LOGIC P2-10)*

**Background.**
- The Bought's Second Clause reads: "If a woman in Thenya wool comes out the front, hold her, and
  send word to the river" (05:965; 07:749).
- The payer is never identified.
- Since TP12, Vell's boat goes north up the tributary, and nothing explains who waits on the
  river.

**Question:** What should the text do with "send word to the river"?

- **A. Cut the phrase.**
- **B. Keep it as a deliberate unknown.** A DM line says the module does not say who waits on the
  river, and the DM never answers it. This joins the "who paid" mystery.
- **C. Keep it and tie it to the escape.** Someone was watching the river, which is part of why
  Vell went north. The owner supplies who.

**Recommended: B.** It keeps the hook and adds no canon. The captain-route reword in L-058
proceeds whichever option is chosen.

### R-11. Who writes the mid-tier NPCs' voice lines? *(L-073; VOICE P2-2)*

**Background.**
- Kovaun, Callun, Draunel, Essin, Maiven, Anha, Tavva and the two Bought officers have traits and
  no line a DM can say.
- VOICE's method (R19) builds one habit and one quote from each NPC's printed Wants and Secret,
  but says the owner should write or approve them, because voice is canon-adjacent.

**Question:** How should the lines be produced?

- **A. Drafted, then approved.** Claude drafts one habit and one quote each, strictly from the
  printed text, and the owner approves or rewrites each line.
- **B. The owner writes them.**
- **C. Habits only, no quotes.** Drafted from the printed traits and approved by the owner.

**Recommended: A.** It is the fastest route, and the owner keeps the final word on each line.

### R-12. Where are the midwife and the two Tithe ministers at midnight? *(L-087; LOGIC P3-5, P3-6)*

**Background.**
- The midwife is the "third plate" and is "gone by dawn" (06:28–29), but she is absent from
  Table VIII–2.
- The two Tithe ministers drive Agenda 1, S12 and "keep Corval alive and the Tithe survives"
  (02:294–296), but they are never placed or named.
- A party guarding the family will ask where everyone is.

**Question:** Should the book place them, and name the ministers?

- **A. Place and name.** The owner places all three on Tables VIII–2 / VIII–6 and names the
  ministers.
- **B. Place only.** Positions without names ("the elder minister", "the younger").
- **C. Leave them unplaced.** A DM line says "not given; place them where your table needs
  them".

**Recommended: B.** Position is what tables ask for, and names can wait. The positions are the
owner's to choose. "The midwife with Veier in B9" and "the ministers on the Court floor near
Corval" are examples only.

### R-13. Is Player Handout 1's repetition intended? *(L-109; VOICE P3-4)*

**Background.** The invitation repeats "revelry" and "look forward" within one sentence. The
text is marked canonical, so no editor may change it.

**Question:** Is the repetition deliberate?

- **A. Yes,** as Raunu's out-of-practice formality. Add a DM note so later editors leave it
  alone.
- **B. No.** The owner edits the canonical text.
- **C. Leave it as it is,** with no note.

**Recommended: A if it is intended, otherwise B.** C invites another "fix" in a later pass.

---

## 7. Proposed work packages

These are FIX and FIX-NEW items grouped into chunks for the fix pass. Rows waiting on a ruling
are marked *(after R-nn)*. The voice pass comes last so it isn't done twice.

| # | Package | Rows | Depends on |
|---|---|---|---|
| **WP1** | **Tells on the run path.** Add a tells column to Table VIII–1 and a tell bullet to each of Movements III–V in ch IV. Put Slow / Stop / End in the prep box | L-001, L-096 | — (`FRI`) |
| **WP2** | **Midnight Tracker and DM-sheet numbers.** Build the tracker page. Add the Wept's turn and the Radiant's stair beat, the bell glossary, the "east-wing doors" fix, and the vanished-beats note | L-029, L-057, L-086, L-046 | WP3 numbers, WP4 state (`FRI`) |
| **WP3** | **Three-player baseline (TP10).** Add the "Three at the Table" box. Print three-player numbers in blocks, cards, Table V–1 and the sheet. Add solo lines. Fix the Movement V budget, the box head counts, the summons and XP lines, and the scaling rule | L-020, L-021, L-022, L-047, L-077, L-083, L-084 | `SIM` for the solo lines (`FRI`) |
| **WP4** | **Slow / Stop / End (§3.2–§3.7).** Spells roll. The control list buys Delay. Add the cap, the Stop routes, the Ends, and the Last Rite. Rewrite the Crossing, the saving-Raunu procedure, the speed-to-turn rule and the *Message* range | L-002, L-007, L-008, L-009, L-004, L-005 *(after R-05)*, L-039, L-075, L-042 (confirm) | R-03 for the Radiant's behaviour |
| **WP5** | **Threat rule and lethal Attendant (§3.1, §4).** Write the threat rule, then the Attendant: lethal when Focused, *Clears the Way* costs an action, a control-spell note, scene binding, damage to the set-aside per dial, edge rules, Vell's immunities. Run the S14 re-sim, with rates per dial, the hit-hard HP and the "how it plays" note | L-010, L-013, L-003, L-037, L-038, L-040, L-074, L-076, L-043, L-078, L-041 (re-check) | R-06 (the Root) |
| **WP6** | **Risk options, re-budget and re-sims (§2).** The dial box. Rule 2 rewritten with heat-4 rows. A drop costs something before midnight. Lethal after midnight. Two cards live by default. Resources. New three-player rosters, labels corrected upward, and a re-sim per card. Also the S11 XP rule, the snake-show count, the balustrade, the non-lethal rule and *Sleep* timing | L-011, L-012, L-014, L-015, L-016, L-017, L-045, L-066, L-080, L-081, L-082 | R-04 (the Circle's heat-4 row) |
| **WP7** | **Logic fixes.** Propagate TP11. Rewrite the Root (TP8) and the garden doors (TP9). Then Vell's boat and route, the Agenda 6 reveal, the endings box, the contract void, Agenda 3, the Patron's Errand, Corval's doubling, "publicly", the slingers, the Radiant's chase line, and Agenda 2. Rows waiting on rulings: east-wing routes *(after R-01)*, acting early *(after R-02)*, the river *(after R-10)*, echoes and NPC positions *(after R-09, R-12)* | L-024, L-025, L-026, L-053, L-054, L-056, L-058, L-059, L-060, L-085, L-088, L-089, L-090, L-091, L-092; L-027, L-028 | R-01, R-02, R-07, R-08, R-09, R-10, R-12 |
| **WP8** | **N4 geometry and maps.** In `facts.yaml`, settle the gallery stairs, the floor-level S11 and B4 doors, the rail drop, the S10 window and garden level, and the garden-stair door. Draw the ward-points. Remove the "approximate" hedges and VIII–1's schematic boxes | L-032, L-061, L-062, L-099 | R-01 (what is sealed) |
| **WP9** | **Prep and runtime honesty, and the print build.** Re-cost the prep box with a 60-minute path. Add the three-player runtime column and the S14 cap (the errand completes). Build the DM packet, player packet and card deck. Add the cast cues, the pregen sheets and the flow page decision. Fix "palace diagram" and the vague cross-references. Clear the open R2 polish. Add the player handouts | L-030, L-031, L-033, L-063, L-064, L-065, L-094, L-095, L-097, L-098, L-100, L-101 | WP2–WP6 content settled |
| **WP10** | **Rules accuracy sweep.** NPC saves and casting as steel, the scope of success at a cost, Dassa's armour and the charges, free-hand grapples, Serane's wording, the charge text, moving charges, alignment and the Gift Knack | L-067, L-068, L-102, L-103, L-104, L-105, L-106, L-107 | — |
| **WP11** | **Voice pass, by ear, last.** De-colon. Cut the meta and kickers (R17 says "horses"). Add the glossary (with Slow / Stop / End, threat and dial), overloaded terms, the B5 and B8 read-aloud, the read-aloud slips, blank cheques, rhythm tics, the Captain's line and the DC ladder names. Add the mid-tier lines *(after R-11)* and Handout 1 *(after R-13)* | L-034, L-035, L-036, L-069, L-070, L-071, L-072, L-108, L-110, L-111; L-073, L-109 | All content packages; R-11, R-13 |

**Suggested order:**
1. WP1, WP3 and WP2 (Friday-critical, no rulings needed).
2. The owner answers R-01 to R-13.
3. WP4, WP5 and WP6 (with their re-sims).
4. WP7 and WP8.
5. WP10.
6. WP9.
7. WP11.

Every package adds `facts.yaml` guards for the rows flagged `FACTS`, and must keep these green:
`tools/fact_check.py`, the lint, `bestiary_check.py`, `pregen_check.py`, and the docs tests.
