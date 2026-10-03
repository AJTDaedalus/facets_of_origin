# Official-style audit: NIGHT slice (`05_The_Longest_Night.md`)

*2026-09-30. Auditor slice NIGHT. File: `conversions/dnd5e/oraga_night/05_The_Longest_Night.md`
(1,153 lines, 14,655 words). Weighted to the after-midnight half. Read-only audit: no
module file was edited. Yardsticks: `docs/RESEARCH_5e_module_conventions_structure.md`
(C-S#) and `docs/RESEARCH_5e_module_conventions_voice.md` (C-V#, S#). Frequency tags:
[A] always, [U] usually, [S] sometimes.*

*Level basis: **four 4th-level characters**, ending at 5th, per the owner ruling
(FIXPLAN_oraga_5e.md §6, "R2 is now: four 4th-level PCs"; 01 l.39, l.221; README l.7).
All XP budgets, DC checks and difficulty claims below use that party. The 2014 DMG
thresholds for four 4th-level characters are Easy 500, Medium 1,000, Hard 1,500 and
Deadly 2,000. The SRD 5.2.1 budgets are Low 1,000, Moderate 1,500 and High 2,000.
(Corrected from an earlier draft that also costed a 3rd-level party.)*

*DC check at 4th level:* the attack's DCs are 10 (a ward at Raunu's side), 13 (tricks,
ward-steering for those who studied, carrying, the crossfire, Persuasion at the gate), 15
(a repeat trick, the last-blow save, a Fracture with two tells, thieves' tools) and 18
(unstudied wards, a Fracture with one tell, the trap). All fit the DMG ladder for 4th
level (proficiency +2, typical key-skill bonus +5 to +6): 13 is a medium-easy check and 18
a hard one. The only DC outside the 10–20 band is 25 (Raunu and Vell), which is marked
Very Hard by design. No DC finding.

---

## 1. Summary

| Dimension | Verdict |
|---|---|
| **PROSE** | Strong voice and a real sense of occasion, but it runs long and hot for 5e DM prose. The mean sentence is 20.9 words (norm 16–19), 24% of sentences run over 30 words (norm ~10%), and 23 paragraphs run over 120 words. There are 229 em dashes (15.6 per 1,000 words), and the "does not X, does not Y, does not Z" and "not X — Y" figures recur. The party is "the players" or "player character" throughout; "the characters" never appears. |
| **MECHANICS** | The Uninvited's spine (Leashed, Down, Not Out, Delay, Fractures) is well designed and mostly in clean SRD grammar. There are three real rules defects. The Attendant's focus trigger contradicts card S14. The Leashed return point ("within 60 feet of its quarry", Chapter X) lets a party that drops the Radiant *move him closer* to Veier, and past Vell. Delay counts turns when the night runs in rounds and beats (about a minute each) when it runs in beats, so wards and the Wept's approach mean different things in each mode. Capitalization mixes 2014 and 5.2.1 forms. |
| **STYLING** | The module's own legend (italic = read-aloud) is broken both ways: the epilogue box is not italic, and five italic paragraphs are DM text. A sidebar holds scripted narration. Stat-block names at first mention are inconsistent. There are only five read-aloud moments in 14.7k words; the Crossing, the night's crescendo, has none. |
| **CONTENT** | The event structure fits the official patterns well: the Knives in the Dark lines are textbook CoS "special events", with heat-gated timing, a default, a card, and "If nobody stops them / If the party steps in" developments. The gaps are a clock that is never stated in one place, no scaling for the attack itself, no fight-space geometry, a name collision with card S2, and two continuity slips (the contract case; the "mask left behind in a trap"). |

**Top 5 issues**

1. **NIGHT-1 (P1).** The Attendant becomes Focused on one trigger in bullet 2 and on a different one in bullet 3. The first is left over from superseded FIXPLAN §5, and card S14 follows §5b.
2. **NIGHT-2 (P1).** A Leashed Uninvited dropped to 0 HP returns "within 60 feet of its quarry" (Chapter X). Dropping the Radiant can put him past Vell at the Crossing, which breaks the escape rule in 05.
3. **NIGHT-3 (P2).** Beats against rounds: Delay, ward durations (10 minutes), the Wept's "third turn" and "about thirty beats" don't share a unit, and the clock is stated nowhere in one place (C-S15).
4. **NIGHT-5 (P2).** The attack has no scaling. The 30-damage lump, the Wept's third turn, the trick DCs and the crossfire damage are fixed for three to five characters at 3rd to 5th level (C-S36).
5. **NIGHT-9 (P2).** The set pieces have no read-aloud. The Crossing and the opening of Movement VII carry their mood in DM prose (C-S22, C-V7).

---

## 2. Findings

### NIGHT-1 [P1] The Attendant's focus trigger contradicts itself and card S14 (MECHANICS)
- Where: 05:351–356 against 05:357–361; 09:1615–1622 (S14 *Enemy*); 08:65–67 (sheet line).
- Yardstick: C-S13 [A] (every beat has one timing rule); C-V16. FIXPLAN_oraga_5e §5 (old) against §5b (current).
- Problem: bullet 2 says that when the party earns Delay, strikes one of the three or stands in their way, "it is **Focused**". Bullet 3 and S14 say it is Focused at the start of its turn *only if one of the three in the scene has no Delay*, and S14 says it is **Idle when the card fires**. So a party that has just earned Delay on the only Uninvited in the room is Focused under bullet 2 and Idle under bullet 3. Bullet 2 is §5's wording, which §5b superseded. This is the hardest fight of the night, so the MM needs one rule.
- Fix: replace the second and third sentences of bullet 2 (from "When the party becomes…" to "…and it is **Focused**.") with: "Card S14 fires the first time the party becomes a real interruption: it earns Delay against one of the three, strikes one, or stands between one and their errand. The card fires with the Attendant Idle. From then on it is **Focused** at the start of any of its turns when one of the three in the scene has no Delay: that one glances at it, then at the party." Keep bullet 3 as it is.

### NIGHT-2 [P1] Dropping an Uninvited can move it closer to its quarry (MECHANICS)
- Where: 05:188–193 (*The last blow*), 05:551–556; 10:1301–1304 (Radiant *Leashed*), 10:1709–1712 (Wept); the Crossing rule at 05:484–495.
- Yardstick: C-V14 (a rule stated once, cleanly); rules contradiction (P1 by definition).
- Problem: 05 says an Uninvited at 0 HP "come[s] back on their next turn, whole", and doesn't say where. The blocks say "within 60 feet of his quarry". So a party that drops the Radiant 100 feet up the terrace sends him to within 60 feet of Veier, past Vell (whom "he does not break past" except once) and past any sealed door. The same holds for the Wept and Raunu's wards. The party's best damage round then buys the villain ground, which undoes the premise that damage "never takes Delay away". It is also an exploit a table could turn against itself without meaning to. (New; not in the prior audits.)
- Fix, in 05 and in all three blocks: "…returns at the start of its next turn, at full hit points, in the space where it dropped (or the nearest unoccupied space)." Keep the Hollow's "within 60 feet of the doors he holds", since holding the doors is his post and not ground gained. Not portable (5e block mechanics).

### NIGHT-3 [P2] Beats, rounds and the clock have no common unit, and the clock is never stated once (MECHANICS / CONTENT) [d20-portable]
- Where: 05:15–22 (beat ≈ a minute ≈ ten rounds; the attack ≈ thirty beats); 05:42–45 (a ward seal "holds for 10 minutes"); 05:52–54 ("perhaps half an hour"); 05:205–210 ("a point is a beat"); 05:234 (the Wept reaches Raunu "on her third turn"); 05:399–413 (the east-wing chase: a check per beat, length unstated); 05:938–943 and 986–989 (bells begin; last bell).
- Yardstick: C-S15 [U] (state the clock once: start, end, what a scene costs; HotDQ's hour track); C-S13 [A] (timing rule plus latitude); S25 ("perhaps" in DM prose).
- Problem:
  - In rounds, one Delay is one Uninvited turn (6 seconds). In beats it is "a beat", about 1 minute. Table V–1 pays the same "dozen guests" for both, which is fine as an abstraction, but the text also puts beats in minutes. A ward that "holds for 10 minutes" then lasts ten beats in beat mode, most of the attack, and 100 rounds in round mode.
  - The Wept kills Raunu on her third turn, and the attack is "about thirty beats". Nothing says what fills beats 4–30, or how many beats the east-wing chase lasts before the Crossing.
  - The sequence (Raunu falls → the Hollow leaves the doors → guests reach B12 → bells begin → the Crossing ends → the leash → the gate is decided → the last bell) has to be assembled from five places in 05 plus 08 Table VIII–2.
- Fix:
  - Drop the minute and round equivalence. In the box at 15–22, replace "As a rough scale, **one beat is about a minute** — ten rounds, if anyone asks — and the whole attack, from the first scream to the boat clearing the river gate, is about thirty beats. You will not need thirty." with "A beat and a round cost an Uninvited the same thing: one turn."
  - Change "holds for 10 minutes" and "for 10 minutes" (05:43–45) to "until the scene ends".
  - Add a short **The Midnight Clock** block under *How to Run the Attack*. Build it only from facts already in 05 and 08: (1) the lights die; nobody rolls. (2) Beats begin; Corro moves first. (3) The Wept reaches Raunu on her third turn toward him, plus one turn per Delay spent. (4) When Raunu falls, the Hollow turns east, the doors open and the crowd reaches B12, where the bells begin. (5) The Radiant reaches the garden stair: *default [N] beats after the lights; you can hold it back while the party is still in the east wing*. (6) The Crossing runs three beats. (7) When the boat is out of reach, the leash takes all three. (8) The gate is decided (card S3), and then the last bell rings.
  - Cut "perhaps" at 05:53: "the Uninvited have half an hour of story-time at most."
  - Item (5)'s default N is a pacing number, not canon. Planner to set it (see RULING list).

### NIGHT-4 [P2] A Fracture that misses by 4 or less: Delay unstated, and skills named without abilities (MECHANICS)
- Where: 05:615–632; 10:152–163 (same gap).
- Yardstick: C-V15 [A] ("DC N Ability (Skill) check"); C-V16.
- Problem: "Miss by 4 or less: it lands" doesn't say whether the 2 Delay comes with it or whether the Fracture is spent. The *Each Fracture works once* line implies it is spent, so the table needs the Delay stated. "Persuasion for a plea, Performance…, Religion…, Insight…" names skills bare. Religion is Intelligence and Insight is Wisdom, and a 5e table will ask.
- Fix: "**Miss by 4 or less:** it lands in full, and that Uninvited gains 2 Delay, but it answers first…" and "a Charisma (Persuasion) check for a plea, Charisma (Performance) for a spectacle, Intelligence (Religion) for a rite or a believer's rebuke, Wisdom (Insight) for naming what you have seen in it, or a plain Charisma check for a bared truth." Also say at 05:610 that an attempt needs at least one tell, as Chapter X does ("A character who has witnessed at least one tell can…").

### NIGHT-5 [P2] The attack has no Adjusting line (MECHANICS)
- Where: 05:222–224 (30 damage in a round); 05:234 and 05:386–388 (the Wept's third turn); 05:212–216 (tricks at DC 13 and 15); 05:513–525 (crossfire; "add half again").
- Yardstick: C-S36 [U] (session-length: an Adjusting sidebar per combat, marked "not cumulative"); C-V24; S36 (vague scaling). The module's own rule (01:328–330) is that every card scales for three or five characters and for 3rd or 5th level.
- Problem: the printed numbers are set for the baseline of four 4th-level characters, which is fine. The crossfire's 7 (2d6) / 14 (4d6) against a DC 13 save is about right for 4th-level hit points of 27–35. Every card in 09 also scales off that baseline, but the numbers that decide the attack itself don't. With resistance to bludgeoning, piercing and slashing on all three, 30 damage in a round is a very different bar for three 3rd-level characters than for five 5th-level ones, who have Extra Attack. "At 5th, add half again" isn't a number.
- Fix: add an **Adjusting the Attack** sidebar after *Buying Time*: "These recommendations are not cumulative. **Three characters:** the Wept reaches Raunu on her fourth turn; lump threshold 20. **Five characters, or 5th level:** lump threshold 40. **3rd level:** crossfire 3 (1d6) / 7 (2d6). **5th level:** crossfire 10 (3d6) / 21 (6d6)." In the crossfire sidebar, replace "(Scale it: at 3rd level, halve the damage; at 5th, add half again.)" with the same concrete dice. The lump and turn values are proposals; run them through the pass-2 sim before print.

### NIGHT-6 [P2] Difficulty claims read one or two bands harder under the 2014 DMG (MECHANICS)
- Where: 05:854–857 ("both are fights a 4th-level party can win outright", S12 and S13); the budgets 05 routes to: 09 Table IX–3 and the S3, S5, S8, S11, S12, S13 and S14 cards.
- Yardstick: C-V24 and §12 (one edition per line; "optionally give the 2014 equivalent"); 01:65–67 claims the module "runs unchanged at a 2014 table".
- Check: four 4th-level characters, 2014 DMG thresholds (Easy 500, Medium 1,000, Hard 1,500, Deadly 2,000) with encounter multipliers:

| Card (after midnight) | Foes | Raw XP | ×mult | Adjusted | 2014 band (4 × 4th) | Module label (5.2.1, 4 × 4th) |
|---|---|---|---|---|---|---|
| S3 (sergeant *Nastier* + 4 Blades) | 5 | 1,500 | ×2 | 3,000 | Deadly (1.5× the threshold) | Moderate ✓ |
| S3 + captain | 6 | 2,600 | ×2 | 5,200 | Deadly (2.6×) | over High ✓ |
| S5 (Tavva + 3 knives) | 4 | 600 | ×2 | 1,200 | Medium | under Low ✓ |
| S8 dark half (4 wardens) | 4 | 800 | ×2 | 1,600 | Hard | "Low" (actually under Low 1,000) |
| S11 (3 bodyguards + Corro) | 4 | 625 | ×2 | 1,250 | Medium | under Low ✓ |
| S12 (3 knives / 4 at heat 4) | 3/4 | 600/800 | ×2 | 1,200/1,600 | Medium/Hard | "Low" (both under Low) |
| S13 Draunel side | 3 | 1,350 | ×2 | 2,700 | Deadly (1.35×) | Moderate ✓ |
| S13, both sides (the card warns against it) | 7 | 2,100 | ×2.5 | 5,250 | Deadly (2.6×) | over High ✓ |
| S14 Attendant (Focused) | 1 | 3,900 | ×1 | 3,900 | Deadly (1.95×) | Deadly ✓ |
| S14 Attendant (Idle, card's CR 5 rating) | 1 | 1,800 | ×1 | 1,800 | Hard | High ✓ |

- Problem: against its declared SRD 5.2.1 budgets for four 4th-level characters the arithmetic is right, and the ✓ marks show where it holds. Under the 2014 DMG the multiplier pushes every multi-foe card one band up (S5, S11 and S12 to Medium; S8 and heat-4 S12 to Hard), and S3 and S13 to Deadly. A 2014 MM reading "Moderate" for S3 or "win outright" for S13 will see Deadly. The snakes fight to leave and quit early, so the labels are defensible in play, but the text never says so for 2014 readers. S8 and S12 are labeled "Low" while under the Low line (09's slice).
- Fix: in 05:856 replace "both are fights a 4th-level party can win outright" with "both are fights the party can end on its own terms". In 01's budget paragraph (or 09 *Running the Snakes*), add one line: "At a 2014 table the encounter multiplier rates most snake cards one or two steps harder than printed. The printed band is how they play, because every snake quits early." Pass S8 and S12 to the 09 auditor.

### NIGHT-7 [P2] "Never burst the lanterns" against "douse the lights" as a Fracture road (MECHANICS)
- Where: 05:294–295 against 05:659–664; 10:128 reconciles them, 05 does not.
- Yardstick: C-V14; C-S21-style clarity.
- Problem: the room-trick note tells the party never to darken the Radiant's corridor, because he hurries. The Fracture text lists "douse the lights" as the first road to his guilt. A table following 05 alone gets two opposite answers. The note is also an italic paragraph, which the module's legend reserves for read-aloud (NIGHT-11).
- Fix: turn 294–295 into plain text: "Darkness speeds him up: in an unlit corridor nobody is watching, so he isn't Witnessed. The exception is his Fracture. A character who puts out the lights *as* a Fracture attempt, denying him his congregation, makes the Fracture check instead (see *The Fractures*)."

### NIGHT-8 [P2] "Knives in the Dark" is the name of two different things (CONTENT / STYLING) [d20-portable in principle]
- Where: 05:694 (section) against 09:616 (card **S2. Knives in the Dark**, Tavva's crew, Movement V); 05:438–440 points to the section from the looters bullet, whose card S5 says "as in S2"; pointers at 04:88, 04:320, 04:459; 05:67, 05:880.
- Yardstick: C-S41 [A] (cross-references resolve unambiguously).
- Problem: "see *Knives in the Dark*" can mean the Movement V thieves or the midnight snakes, and at 05:438 it sits right next to Tavva's card.
- Fix: rename the 05 section **The Snakes in the Dark** (principle 4's own heading phrase, 05:63) and update every pointer (04 ×3, 05 ×3, 08, 09 Table IX–3 note, INVENTIONS #5/#7/#11/#15, flow.json).

### NIGHT-9 [P2] The set pieces after midnight have no read-aloud, and their mood sits in DM prose (STYLING / PROSE) [d20-portable]
- Where: the Crossing (05:442–499): none. Movement VII opening (05:866–876): none. The dais and east-wing default beats (05:378–413): none except a quoted order. After the Unmasking, there are three boxes in the whole half: the Attendant, B12 and the epilogue.
- Yardstick: C-S22 [U] and §3.2 (a set piece "runs a page or more and gets several boxes"); C-S7 [U] (a part opens with a situation paragraph, then its first box); C-V7 (mood in read-aloud; DM prose states function).
- Problem: the crescendo reads as DM prose full of imagery ("pressure and shear, crystal lanterns bursting in a line, the terrace balustrade exploding into gravel"). The MM has to improvise the moment the whole night builds to.
- Fix: lift what is already in the text into boxes, adding no new detail.
  - **Crossing**, trigger "When the Radiant comes out onto the terrace, read:"
    > *Behind you, the lanterns along the terrace go out one after another. A gray mask comes out of the smoke. The pale man beside Veier turns to face it, and then he is simply between you and the mask, without having crossed the space. Lanterns burst in a line. The balustrade goes to gravel. The masked one says a single word: "…You."*

    Then cut the matching imagery from 05:465–470 so the DM text keeps only function.
  - **Movement VII**, trigger "When the Uninvited have gone, read:"
    > *The three gray masks are gone. Fire runs along the banquet galleries and smoke rolls under the dark crystal. Here and there a ward still burns rose-bright over a knot of guests. Near the stairs, the minister who greeted you at the gate is bleeding, upright, and counting his staff out loud.*

    Every detail is from 05:868–873 and Movement I. Check "who greeted you at the gate" against 04's receiving line before use.

### NIGHT-10 [P2] Scripted narration inside a sidebar (STYLING)
- Where: 05:580–584 (MM Note, *the table that will not stop trying to kill them*: "She stops. She looks at you…").
- Yardstick: C-S26 [A] (no read-aloud in sidebars).
- Fix: rephrase it as instruction: "When the Wept reaches 0 hit points, say plainly what happened: she stopped, threw the character clear, and is walking back to the dais whole. Then say what the round bought: Raunu a round, the crowd a round. Then ask the next player what they do."

### NIGHT-11 [P2] The module's own read-aloud device is used inconsistently (STYLING) [d20-portable]
- Where: the epilogue box at 05:1009–1020 is plain, not italic. Italic DM paragraphs appear at 05:3–4, 166–167, 294–295, 696–702 and 878–881.
- Yardstick: C-S2 [A] and §12 ("whatever device the module declares must be used consistently"). The legend at 01:336–339 says italic blocks are read-aloud.
- Problem: the one-shot ending, which is read aloud, doesn't look like read-aloud. Five DM paragraphs do look like it, and 696–702 is a whole italic lead-in in second-person-free DM voice.
- Fix: italicize the epilogue box. Set the five DM paragraphs in roman. Keep 3–4 as a chapter dek if the house wants one, and have the legend say so.

### NIGHT-12 [P2] Mixed edition capitalization and unitalicized magic items (MECHANICS / STYLING)
- Where: in 05, lowercase 2014 forms: "unconscious" (173), "prone" (192), "difficult terrain" (325, 520), "dim light" (107–108), "bright light" (44), "hit points" (13×), "speed" (476). Capitalized forms: "Stable" (173, 177, 180, 195, 397, 558), "Speed" (477, 670), "Heroic Inspiration". Chapters IX and X use 5.2.1 caps throughout ("the Prone condition", "Difficult Terrain", "Heavily Obscured", "Hit Points"). *House Seal* and *House Flare* are not italic at 05:259 and 05:277 (they are italic in 10:1954).
- Yardstick: C-V26 [A] (one scheme module-wide); C-S39 [A] (magic items italic); S15.
- Fix: choose 5.2.1 caps to match 09 and 10 (the BRIEF's target) and convert 05. "falls unconscious and Stable" → "has the Unconscious condition and is Stable"; "knocked prone" → "has the Prone condition"; "difficult terrain" → "Difficult Terrain"; "dim light" / "bright light" → "Dim Light" / "Bright Light"; "hit points" → "Hit Points"; "her speed" → "her Speed". Italicize *House Seal* and *House Flare*. Spell names in 05 are italic lowercase (2014). If 10 keeps *Tiny Hut*-style title case, align one way.

### NIGHT-13 [P2] How the party and the players are named (PROSE) [d20-portable]
- Where: "the characters" appears 0 times. "player character(s)" appears 30 times. "the players" meaning the characters: 05:12, 36, 112, 382, 413, 422, 435, 452, 461, 475, 490, 541, 609, 771, 1045, 1080, 1089, 1095, 1097 (about 19). DM-facing "you" addresses the players in the room-trick tables: 05:258 "he tells you exactly what to touch… whatever you studied", 259 "Yours", 285 "if you studied", 303 "behind you".
- Yardstick: C-V2 [default] ("the characters"; "the players" only for real people); C-V1 ("you" is only the MM); S2.
- Problem: "player character" is a defensible house term, but "the players carry history in their arms" and "Any player at his side becomes his hands" put real people into the fiction. The tables switch "you" from MM to player mid-chapter.
- Fix: default to "the characters" or "a character", and keep "player character" where it disambiguates from NPCs. Examples: 475 "The players carry history…" → "The characters carry history…"; 382 "Any player at his side" → "Any character at his side"; 1095 "makes the players the most interesting people" → "makes the characters…". In the tables: "he tells the character exactly what to touch"; "the character's own, or a House Seal…"; "DC 13 for a character who studied the wards".

### NIGHT-14 [P2] Rhythm: long sentences, long paragraphs, AI-rhythm figures (PROSE) [d20-portable]
- Where: whole file. Sentence mean 20.9 words, median 18, 24% over 30 words. Paragraphs over 120 words at lines 33 (266 words), 212, 378 (308), 399, 423 (255), 459, 471, 484 (246), 644, 653 (313), 674, 734, 743, 768, 796, 808, 818 (201), 868, 971, 1038 (244), 1055, 1068 (286), 1089. Em dashes: 229 (15.6 per 1,000 words; 25 lines carry two or more). Negative triplets: 113–114, 448, 540–542, 657–658, 667. "Not X — Y": 94 and 106 (the same image twice), 466, 1095.
- Yardstick: C-V4 [A-norm], C-V5, S40; memory rule (no tricolons, "not X but Y", em-dash chains).
- Problem: a 5e MM scans this mid-session. Paragraphs of 250–310 words (principle 2, the dais bullet, the Radiant's Fracture, the trap sidebar) bury the rule inside the image. Light-touch fixes that keep the voice:
  - 106–107: "**The lights die.** Mid-word. Not blown out — *drunk.* Every crystal…" → "**The lights die** mid-word. Every crystal…" (the box already has the "not blown out" image).
  - 113–114: "he does not startle, does not finish the sentence, does not waste one second on disbelief." → "He doesn't startle, and he doesn't finish the sentence."
  - 540–542: "not by the players, not by fifty guards, not by the palace, and not by a spell." → "Nothing in the palace can do it tonight, spells included."
  - 657–658: "Not from the hunt, not from the errand, not by darkness or doubt — nothing short of the leash ends his night." → "Nothing short of the leash ends his hunt."
  - 1095: "The truth without a patron is not power — it is exposure, and it makes…" → "Without a patron, the truth only exposes them. It makes…"
  - 26–29: cut "— which is exactly as it should be, because they will choose it".
  - Split principle 2 (33–51) into a rule paragraph (steering: action, DCs, once per ward-point, the three options) and a Root paragraph. Split the dais bullet (378–398) at "*(At his side…*" so the rule parenthetical becomes its own paragraph.

### NIGHT-15 [P2] Where the contract case is: on the captain's belt, or in the sergeant's hands (CONTENT) [d20-portable] → NEEDS-RULING
- Where: 05:906–907 ("a case chained to the captain's belt") and 05:913 ("which the captain alone has read") against 05:939–949 (a *sergeant* at the gate holds the chained case up and reads from it) and S3's timing (the captain arrives in round 3). 10:1950 hedges ("a sergeant's hip or the captain's belt"). Inherited from the Facets source (`adventures/oraga_night/05_The_Longest_Night.md:327` and `bought_captain.fof:23`).
- Problem: the players see the case in a sergeant's hands before the captain exists in the scene, so "captain alone has read" and the chained belt don't fit. Loot and evidence rulings (who has to fall for the case) depend on it.
- Fix: owner ruling (see §4). If the owner says "the sergeant carries it; the captain alone has read the third clause", change 907 to "written in a chained case the company's sergeant carries" and 10:1950 to match.

### NIGHT-16 [P2] "The mask of an Uninvited left behind in a trap" contradicts the trap branch (CONTENT)
- Where: 05:1091 (⟨They expose the truth⟩ evidence list) against 05:1083–1087 (⟨They trap one⟩: "the leash tears them out… by morning there is nothing to show the inquest but damage").
- Yardstick: C-S14 (developments are consistent); canon (the Uninvited leave no trace, 08 pillars).
- Problem: this is a 5e addition, not in the Facets source. It hands the table a piece of evidence that the canon pillar "the Uninvited leave no trace" says can't exist.
- Fix: cut "the mask of an Uninvited left behind in a trap". The list still has the study reliefs, the invitations and a Fracture's confession.

### NIGHT-17 [P2] The trap branch doesn't say what happens to the trapped one's errand (CONTENT) → NEEDS-RULING
- Where: 05:1068–1087.
- Yardstick: C-S14 [A] (every divergence has a stated development).
- Problem: a trap holds an Uninvited "until the last bell". If it is the Wept before she reaches Raunu, does Raunu live, as in ⟨They save Raunu⟩, or does he still spend his crystal and die "by his own choice"? If it is the Radiant, the escape is trivial. If it is the Hollow, the doors open early. The pillar "Raunu falls, by his own choice" (08) makes this canon-sensitive, so the fixer can't settle it alone.
- Fix: owner ruling (see §4). Then add one sentence per Uninvited to the sidebar.

### NIGHT-18 [P2] No General Features or fight-space geometry for the palace after midnight (CONTENT / MECHANICS) [d20-portable]
- Where: the rules for the dark palace are scattered: dim light (05:107–109), the crowd (05:315–326), smoke and fire only in cards S12 and S13 (09:1452–1455, 09:1535–1545), the service run's width (05:289). The Crystal Court, the dais, the main doors, the east-wing corridors, the three garden levels and the river gate have no dimensions anywhere in the module (04's B2, B5 and B9 have none either).
- Yardstick: C-S11 [U] (General Features before a site's scenes); C-S51 [A] (with no map image, give connections, fight-space dimensions and starting positions).
- Problem: a *thunderwave* "at the dais is up to nine people" assumes a grid the book never draws. "Within 30 feet of an Uninvited" and "15 feet pushed" need distances between the dais, the doors and the stair.
- Fix: add **The Palace After Midnight: General Features** under *Midnight Rules*, made only from rules already in the book: **Light.** Dim Light in the Court, Darkness in corridors and service passages unless a ward flares. **The crowd.** One guest per 5-foot square, Difficult Terrain. **Smoke.** In B3, Heavily Obscured beyond 10 feet, with the DC 10 Constitution save. **Fire.** 2d6 Fire damage, DC 13 Dexterity for half, and "the fire never finishes anyone". Dimensions are new physical facts about the palace: owner ruling (see §4), or state "the palace has no fixed plan; place it on the palace diagram (Chapter VIII)".

### NIGHT-19 [P3] Cross-references that don't resolve by name, and an unprinted award (STYLING / MECHANICS)
- Where: 05:828 and 05:883 "(*Carrying somebody out*, Chapter I)": no such section; the rows are "Somebody carried out" (Table I–3) and "A person carried out in Movement VII" (Table I–4). 05:1150 "as Chapter I pays *ending a fight without finishing it*": the row is "A fight ended by an out". 05:271 "(principle 2)" and 05:1076 point to an unnamed list item. 05:883–886 "XP for every person standing outside at the end" prints no amount.
- Yardstick: C-S41 [A]; C-S44 [A] (awards printed where earned).
- Fix: "(Chapter I, Table I–4)"; "as Table I–4 pays a fight ended by an out"; "(*How to Run the Attack*, principle 2)"; "and 100 XP to the carrier for each person they bring out (Table I–4)".

### NIGHT-20 [P3] The crossfire sidebar's Evasion sentence (MECHANICS)
- Where: 05:521–523.
- Problem: a successful save already takes no damage, so "a character with Evasion takes no damage on a success and the full result on a failure" says nothing, and "neither does Evasion's half-damage" reads as if Evasion did something first.
- Fix: "Cover doesn't help against a garden coming apart, and Evasion changes nothing: a success already takes no damage."

### NIGHT-21 [P3] Small rules gaps in the attack (MECHANICS)
- Where: 05:190–192 (the push on the last blow has no direction); 05:490–495 and 455 (the Radiant has no initiative at the Crossing, but he gets "one turn at the gate"); 05:101–104 (midnight surprise isn't stated); 05:322–324 ("is trampled" has no effect).
- Yardstick: C-S33 [A] (surprise and detection terms); C-V16.
- Fix:
  - "…pushed 15 feet in a direction the MM chooses and has the Prone condition".
  - "When he breaks past, he takes one turn at the gate, at the end of the round, after every character has acted."
  - "When the first beat turns into a fight, nobody is surprised: everyone saw the lights die."
  - "…is trampled: a guest dies, and a character takes 5 (2d4) Bludgeoning damage." The damage value is a proposal.

### NIGHT-22 [P3] The room-trick tables don't show DCs (MECHANICS / STYLING)
- Where: Tables V–2 to V–5 (05:254–309). The "Roll" column gives the ability and skill; the DC is only in *Buying Time*.
- Yardstick: C-V15 [A]; S6 ("roll" for a check).
- Fix: rename the column **Check (DC 13; DC 15 the second time)** and keep the per-row exceptions (DC 10 at Raunu's side, DC 13/18 on a sealed door, DC 15 Survival, thieves' tools DC 15).

### NIGHT-23 [P3] First-mention styling and small consistency slips (STYLING) [d20-portable except the bold]
- Where:
  - Stat-block names at first mention after midnight are neither bold nor pointed: "the nine honor guards" (378; **Boranis Honor Guard**), "his Bodyguards" (144), "the Wardens" (763), "his Duelists" (792), "sixteen blades, four sergeants, a captain" (906; bold only at 954). The same words are capitalized in some places and not in others: Bodyguards/bodyguards (144, 812 / 334), Duelists/duelists (792, 1147 / 334).
  - gray (75, 127, 854, 1013) and grey (765, 946).
  - 05:843 "in its sight" for the Radiant, whom 05 calls "he".
  - 05:449–450 "the pale factor stops being unmemorable" reads as if it meant the Radiant, who stepped out in the same sentence. It means Vell.
  - 05:427–428 "Two of her knives hit the trophy gallery; the others…": S5 gives her three knives, so "the others" is one knife.
- Yardstick: C-S32 [A] (count + **bold** name + location); C-V21.
- Fix: bold at first mention with a pointer: "the nine **Boranis Honor Guards** (Chapter X)", "his three **Phern Bodyguards**", "sixteen **Bought Blades**, four sergeants and a captain (Chapter X)". Lowercase the common nouns after that. Pick "gray". "its sight" → "his sight". "…and for the first and only time all night, Master Vell stops being unmemorable." "Two of her knives hit the trophy gallery (B7); she and the third work…"

### NIGHT-24 [P3] No Expected Duration or Treasure lines at part and area level (STYLING / CONTENT)
- Where: Movement VI (05:70) and Movement VII (05:866) headers; B12 (05:903–995) and the looters bullet (05:423–437).
- Yardstick: C-S8 [U] (session-length parts carry an expected duration; 01 Table I–1 has 50 and 40 minutes); C-S45 [A] (treasure itemised where found).
- Fix: under each header, "*Expected duration: 50 minutes*" / "*…40 minutes*". In B12, add "**Treasure.** The contract case and the company's purse (3d6 × 10 GP in old coin); see *The Night's Loot*, Chapter X." In the looters bullet, add "(*Tavva's sack*, Chapter X)".

---

## 3. What already meets the official standard (keep it)

- **The special-events shape** (CoS pattern §2.4a, C-S13/C-S14). *Knives in the Dark* gives each line a timing rule (heat read at the first scream), a default ("If nobody stops them"), a prevention condition (heat 0–2), a card, and a paired-conditional development ("If the party steps in… What it changes"). Table V–7 is a model faction-reaction table (C-V12: one clause per faction). Don't flatten it.
- **The villain visit rule** (C-S18). *Down, Not Out* is a clean, official-shaped "the visits test, they don't kill" rule, with a named fallback so the table never TPKs (C-S35). *Someone always comes* and "Say who it was. That person is now owed something" are excellent.
- **Rules grammar in the core blocks**: "DC 15 Strength or Dexterity saving throw", "7 (2d6) bludgeoning damage", "DC 13 Intelligence (Arcana) check", "DC 13 Strength (Athletics) or Constitution check", average-then-dice everywhere, numerals for game quantities, no bare "Perception check" (S3 clean), no DC ranges (S5 clean), no "we", no "Note that", no exclamation marks in DM prose, no rhetorical questions (S26–S29 clean), no "PCs" (S1 clean).
- **Discretion always carries a default** (C-V9). The MM Notes' *Default / The dial / The cost* triad is the official "make the call, then offer the dial" pattern in house form.
- **Secrets stated flatly to the MM** (C-V10): the Fracture truths, "What the module never says", the red herring about old coin ("Write the herring so it *can* be untangled").
- **Closing the obvious 5e exploits** by pointing to Chapter X's table and not restating spells (C-V14). *Fractures and magic* gets this exactly right.
- **The Raunu speech and the lights box**: correct triggers, scripted dialogue under three sentences, second person, present tense, numbers spelled out, no mechanics in the box (C-S19 to C-S21, C-S24).
- **Advancement printed where earned** ("Call 5th level here", C-S44). Heroic Inspiration awards are tied to Table I–3.
- **B12** follows the official area order well: context, trigger, box, objective, card pointer, three endings, Development (C-S12).

---

## 4. NEEDS-RULING (for the owner)

1. **Who carries the Bought's contract case at the gate?** *Background:* the text says the case is chained to the captain's belt and only the captain has read the third clause. But the scene the players see has a sergeant holding the chained case up and reading from it, and the captain doesn't arrive until the third round. The Facets edition has the same mismatch, so both editions need the answer. *Question:* does the sergeant carry the case (so the captain alone knowing the Second Clause means the third clause is kept from the sergeant somehow), or does the captain carry it (so the sergeant at the gate is reading the terms from memory, or from something else)? The recommended answer keeps the box as written: "the sergeant carries it; the captain has read the whole of it."
2. **What does trapping an Uninvited in ward-crystal do to its errand?** *Background:* the rare ⟨They trap one⟩ branch holds one of the three until the last bell. The book never says what that means for Raunu, whose death "by his own choice" is a pillar, or for Veier's escape. *Question:* if the Wept is trapped before she reaches Raunu, does he live (as in ⟨They save Raunu⟩), or does he still spend his last crystal on Veier and fall some other way? If the Radiant or the Hollow is trapped, is the outcome simply "the escape is easy" or "the doors open"?
3. **Room sizes for the midnight palace.** *Background:* 5e fights and area spells need distances (the dais to the doors, the Court's size, the garden levels), and the module never gives any. Room sizes are new physical facts about Raunu's palace. *Question:* may the 5e edition set approximate dimensions for B2, B5 and B9 (a design fact, not lore)? Or should it say "the palace has no fixed plan; use the Chapter VIII diagram and place distances as the scene needs"?
4. **(Planner, not owner) The Midnight Clock default.** How many beats after the lights the Radiant reaches the garden stair (NIGHT-3, item 5). This is a pacing number, and the sim or the Planner should set it.
5. **"MM" in place of "DM".** Not filed per occurrence. The owner is already considering it. In this slice the role name appears only in "the MM chooses" and "MM Note", so the official grammar ("you" for the MM) is otherwise kept.

*Checkpoint: complete.*
