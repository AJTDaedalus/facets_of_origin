# Official-style audit: BALL slice (`04_The_Ball.md`)

*2026-09-30. Auditor slice BALL. File: `conversions/dnd5e/oraga_night/04_The_Ball.md`
(1,329 lines, about 15k words). Yardsticks: `docs/RESEARCH_5e_module_conventions_structure.md`
(C-S) and `docs/RESEARCH_5e_module_conventions_voice.md` (C-V, S). Audit only: no module
file was edited. Line numbers are those of the file on `feat/lean-facets` at the time of
the audit.*

## 1. Summary

| Dimension | Verdict |
|---|---|
| **PROSE** | **Off-standard (P2).** The voice is vivid and mostly human, but DM prose runs long: mean sentence about 24.6 words, median 20, 27% over 30 words (norm 16–19 / 15–17 / 10%), and 14 paragraphs over 120 words outside background blocks. About 230 em dashes (roughly 150 per 10k words), plus a cluster of "not X but Y" turns, tricolons and self-praising lines ("a superb scene", "the module's best red herring"). A few rhetorical and designer-voice lines. |
| **MECHANICS** | **Mostly sound, with 2 contradictions.** DCs sit on a sane ladder for 3rd level (10 / 13 / 15 / 18, with 25 reserved for Raunu). Checks almost always use "DC N Ability (Skill)". Defects: the Attendant's "gone until the Unmasking" undoes the one-habit-per-Movement rule that S14 depends on (P1); the orrery check cancels itself; the guard response still disagrees with S4; several checks have no stated result; lock checks drop the ability. |
| **STYLING** | **Off-standard (P2).** Read-aloud boxes are good: all have triggers, run 34–90 words (the toast is 125), use second person and present tense, and spell out numbers. But four boxes sit *above* their area headers, and the GM text below repeats them. Two boxes put GM text in read-aloud italics, which breaks the module's own legend (01). Capitalization of rules terms is mixed. The Snakes This Movement boxes run 355–559 words. |
| **CONTENT** | **Strong, with one hole (P1).** The chapter already follows the official social set-piece shapes: timed Movements with durations and "run if behind" lists, a general-features block (*The Palace on Alert*), a capture-not-death rule, a topics list for the host, a DM-fired interruption (the toast), and redundant clue trails. The hole is Agenda 4. The chapter marks the dinner for two as **not optional** and the rest of the night depends on it, but the page never says how the Agenda 4 character gets through the east wing doors, and it gives the dinner scene only two sentences. |

**Top 5 issues**

1. **BALL-1 (P1):** Agenda 4's way through the east wing doors is never written, and the dinner for two (marked *not optional*) has no scene: no box, no topics, no length, no exit.
2. **BALL-2 (P1):** Once the Attendant is followed or confronted, it is "gone until the Unmasking". That contradicts "one sighting per Movement… show every one of them", and S14's +2 bonuses depend on those sightings.
3. **BALL-3 / BALL-4 (P2):** Boxes are printed above the headers of B2, B4, B6 and B9, and the GM text under each header restates its box. The chapel box also gives away the fact that a DC 10 check is supposed to gate.
4. **BALL-5 (P2):** In the summons Q&A and the toast, GM guidance and stage directions are set in read-aloud italics, and the toast's speech is roman. By 01's legend, the MM would read the wrong half aloud.
5. **BALL-13 / BALL-14 (P2):** Sentence and paragraph length, and the AI-rhythm cluster (em-dash density, "not X but Y", inflated asides).

## 2. Findings

### BALL-1 [P1] Agenda 4 cannot get through the east wing doors from the page, and the dinner for two has no scene (CONTENT) [d20-portable]
- **Where:** 04:329–332 (B9: "the ways in are Agenda 4's errand, Anha's passages, and Undercurrent C"); 04:740–743 (Undercurrent C: "through them needs Agenda 4's errand… or real ingenuity"); 04:1065–1067 (Raunu: "If she chooses you, you will know"); 04:1126–1129 (time box: dinner for two under *If you have time* yet "**not optional if anyone carries Agenda 4**"); 04:1173–1175 (the whole dinner scene: two sentences). 07:64–69 repeats the same routes.
- **Yardstick:** C-S16 [U] (hosted dinner: arrival box, behaviour envelope, topics list, interruption); C-S29 [A] (what each talkable NPC knows is written down); C-S13 [A] (a timed beat needs a timing rule); brief §5 ("run any scene from the page"). Official evidence: the private-dinner and dining-hall patterns in CoS (p.57–58, p.125) and the feast in PotA (p.50) each script the host's envelope and give an exit trigger.
- **Problem:** Chapter V "leans on" someone reaching Veier (03 Agenda 4; 04:566). Agenda 4 is named as the first way in, but nothing says what the character *does* at the doors: show the ring? ask for her? wait to be sent for? Undercurrent C's trail ends at the same doors. The dinner scene has no arrival box, no list of what Veier or Raunu will say, no length and no exit. Without them the MM improvises the one scene the finale depends on. The time box also contradicts itself: the scene sits under *If you have time* and is flagged *not optional*.
- **Fix:**
  1. Move the dinner out of *If you have time* in the Mv IV time box: "*Run:* … and, if anyone carries Agenda 4, dinner for two in the east wing (B9)."
  2. Add a short subsection under Movement IV, **Dinner for Two (B9)**, built only from seeded material:
     - **Trigger:** "When a character is let into the east wing after the toast, read:". A box of 60–90 words from seeded details only: warm light, the two plates, the midwife, the packed-then-unpacked traveling pack by the door.
     - **Envelope:** Veier's *Play her* and the quote at 07:72–74. Raunu's summons manner. Say what neither will say: Raunu does not say what the Unmasking announcement is.
     - **Topics:** bullets drawn from 07 (Wants, Fears, Secret) and Agenda 4's three questions (is she well, is she free, is she herself), each with the answer 07 already gives.
     - **Length and exit:** a cap ("about ten minutes of table time"), and an exit that routes to Movement V ("Corval comes to the door as the lamps begin to lower; the guest is shown out").
  3. The access step itself needs a ruling (see N1). Recommended wording to offer the owner: "A character who shows the door guards the grandmother's ring and asks for Veier by name is asked to wait. The ring goes in. If Veier chooses them, and by default she does, a guard walks them up." This uses only the ring (03, Handout 2) and Raunu's own line.

### BALL-2 [P1] The Attendant's vanish rule contradicts its one-habit-per-Movement rule (MECHANICS) [d20-portable]
- **Where:** 04:860–866.
- **Yardstick:** C-S13 [A] (a timed beat's rule must be runnable); rules contradiction (P1 by the brief). The downstream effect is 09 S14, where the +2 for a habit depends on the table having seen it (LOG_oraga_5e_pass2, tail).
- **Problem:** The paragraph says "One sighting per Movement… show every one of them once". It then says that if anyone follows or confronts the Attendant "now or in any Movement… it is gone until the Unmasking". A curious table in Movement I (the likeliest time) loses the crystal, the literal answer, the music and the glint. Those are the habits S14 rewards, so the finale gets harder because the players paid attention.
- **Fix:** Before: "It never fights before midnight, and it is gone until the Unmasking." After: "It never fights before midnight. It is gone for the rest of that Movement and turns up in the next one as printed." If the owner intended the harsher rule, S14 needs a line saying that unseen habits still grant the +2 once named at midnight (see N4).

### BALL-3 [P2] Four read-aloud boxes sit above their area headers, and the GM text restates them (STYLING) [d20-portable]
- **Where:** B2 (box 219–224, header 226; "vault of rose-lit crystal" and "faint warmth… like a wall remembering sunlight" repeat the box); B4 (box 237–242, header 244; "A smaller crystal chamber off the Court" repeats verbatim); B6 (box 259–266, header 268; "Fraden's niche grandest as everywhere" repeats); B9 (box 323–327, header 329).
- **Yardstick:** C-S12 [A] (header → trigger → box → GM description); C-V7 [A] (after a box, DM prose states function and does not re-describe).
- **Problem:** An MM scanning for "B4" lands below the box and skips it, or reads the same description twice. The duplicated sentences cost about 120 words.
- **Fix:** Move each header above its trigger line. Then cut the GM text's re-description to function. For B2: "**B2. The Crystal Court.** The grand hall, and the room where nearly every scheduled event happens: dance floor, musicians' gallery, the high table on its dais." For B4: drop the first sentence and start at "Its dais is worn by generations of petitioners…".

### BALL-4 [P2] The chapel box gives away what the Perception check gates (STYLING) [d20-portable]
- **Where:** Box 04:261–266 ("The eighth has fresh offerings in it, and they have been tended recently, and carefully"); GM text 04:269–271 ("guests with sharp eyes notice… (DC 10 Wisdom (Perception) to notice …)").
- **Yardstick:** C-S21 [A] (no unearned information in boxes); 01's own legend ("never name a thing the players have not identified").
- **Problem:** The box tells every player what the DC 10 check is for, so the check does nothing. The Religion check still has a job.
- **Fix:** End the box on the seven ordinary niches. Before: the second paragraph of the box. After, as GM text: "A successful DC 10 Wisdom (Perception) check notices that the eighth niche, Elanna's, holds fresh offerings, tended recently and with care. A successful DC 13 Intelligence (Religion) check knows what it means for a chief's chapel to tend Elanna's niche." If the owner wants the offerings seen by everyone, keep the box and cut the Perception check.

### BALL-5 [P2] GM text is set in read-aloud italics, against 01's legend (STYLING) [d20-portable]
- **Where:** 04:1020–1060 (*Raunu's summons*: the italic lead "He is not the warm charmer… 'If friendly' here means…" and the italic stage notes); 04:1139–1155 (the toast: speech in roman, stage directions in italics, and a final narrative paragraph).
- **Yardstick:** C-S19/C-S21 [A]; 01:338 ("***Italic blocks*** are read-aloud"); C-S24 [U] (long conversation moves to bullets in GM text).
- **Problem:** By the module's own legend, the MM reads the italic parts aloud. In the summons that means reading the GM guidance about "if friendly". In the toast it means reading the stage directions and not the speech. The same mixed styling appears in 07's Vorlain block, so this is a module pattern.
- **Fix:** Summons: turn the box into a GM subsection. Put the intro paragraph in roman, the player questions as bold run-ins, and Raunu's replies in quotation marks. Toast: keep one italic read-aloud block. Put the speech inside it in quotation marks, and move the pauses and the drink into short bracketed GM cues in roman ("(Pause. He drinks; the room drinks a beat later.)"), or to a one-line GM note after the box.

### BALL-6 [P2] A failed invitation check at the gate has no result (MECHANICS) [d20-portable]
- **Where:** 04:194–198 (B1: DC 13 / DC 18 Charisma (Deception); "A miss by 4 or less gets them in").
- **Yardstick:** C-V12 [A] (failure still yields the lead); C-S14 [A] (failure continues the story); C-V16 ("If the check fails, …" when failure matters).
- **Problem:** A miss by 5 or more is the first real failure of the night, and the page is silent. The MM has to decide on the spot whether a player spends the ball in the street.
- **Fix:** Add, using routes the chapter already names (the kitchens at 04:852, the cell rule at 04:68): "If the check fails by 5 or more, Corval hands the card back with perfect courtesy and does not let its bearer through. The character can still get in with the festival hires through the kitchens (B10) or on another guest's arm, but Corval has their face and their false name, and the first time he sees them inside he sends for a guard."

### BALL-7 [P2] Several checks have no stated result (MECHANICS) [d20-portable]
- **Where:** 04:176–181 (the first check: "Charisma (Persuasion) to talk a place up the line, Wisdom (Insight) to read who is selling what"); 04:233–235 (B3: overhearing an alcove, DC 13); 04:922 (helping Corval "well", DC 13); 04:1067–1069 (angling to be summoned, DC 13, and no result).
- **Yardstick:** C-V16 [A] (the result is an observable fact); C-S29 [A].
- **Problem:** Each check names a DC but not what success buys, so the MM invents it at the table. The B0 note says this check "teaches the tier", which makes the gap worse there.
- **Fix:** One clause each:
  - **B0:** "On a success, the character gets one rumor (Table VIII–7) or a place in the line next to anyone named in the bullets above. At a cost, they get the same, and Table VIII–4 supplies the cost."
  - **B3:** "A success hears one rumor (Table VIII–7) or one fact from the speaker's entry in Chapter VII."
  - **Mv II:** "Helping well makes Corval grateful: see Agenda 1."
  - **Mv III:** "On a success, Corval fetches that character at the next summons."

### BALL-8 [P2] The Seating Feud's timing contradicts itself and collides with the toast (MECHANICS) [d20-portable]
- **Where:** 04:489 (header "Movements II–IV"); 04:493–494 ("loses its manners at dinner… between the first course and the second"); 04:907 (Mv II time box: "S1 if someone wants it"); 04:1131–1133 (the toast lands "between the first course and the second"); 09 S1 ("Any time in Movements II–IV", trigger "within earshot of the third bench").
- **Yardstick:** C-S13 [A] (a timing rule with DM latitude); CoS Special Events pattern (p.124).
- **Problem:** The prose sets the brawl at the same moment as the toast. The time box runs it in Movement II. An MM who follows the prose has the host arrive in the middle of a brawl.
- **Fix:** Before: "loses its manners at dinner… somewhere between the first course and the second". After: "loses its manners in the banquet galleries. By default it boils over in Movement II, the first time a character is within earshot of the third bench (card S1). You can hold it until Movement III if the galleries are empty of the party. It is over, one way or the other, before the toast." Also replace "(see the sidebar below)" at 04:505 with "(see *Guards Are a Scene*, below)".

### BALL-9 [P2] The summons set piece lacks an end trigger and a default for "if friendly" (CONTENT) [d20-portable]
- **Where:** 04:995–1069.
- **Yardstick:** C-S16 [U] (the host's behaviour envelope: how long, what ends it); C-V9 [A] (discretion with a default); C-V6 (the "perhaps" hedge).
- **Problem:** The topics list is good and meets the official pattern. But nothing says how long an audience lasts or what ends it besides "abruptly". "If friendly" is defined only as Raunu's private decision, so it never fires on anything a player does. "Raunu summons perhaps four guests" hedges a number the MM needs.
- **Fix:**
  - "Raunu summons four guests all night, two of them player characters."
  - "An audience lasts about five questions or five minutes of table time. Then he ends it with the closing line."
  - "He turns *friendly* when the guest tells him a true thing he did not know, or sits through the silence without filling it. By default, he is friendly with the second summoned character."
  - All three use only mechanics already in the chapter (04:1015–1016, 04:1027–1028).

### BALL-10 [P2] The orrery check cancels itself (MECHANICS)
- **Where:** 04:668–670 ("A Scora, or anyone who takes an hour with it (and succeeds on a DC 15 Intelligence check, or needs none after the hour if they are content to take the whole hour)").
- **Yardstick:** C-V15/C-V16 [A] (one check, clear frame); a retry or time-cost rule stated plainly.
- **Problem:** Both branches cost "the hour", so the check never matters. The likely intent is a quick read on a check and a slow read without one, but the page does not say so.
- **Fix:** "A Scora reads the figure at a glance. Anyone else can make a DC 15 Intelligence check after 10 minutes with it, or reads it with no check after a full hour:"

### BALL-11 [P2] The "tall, pale factor" is withheld from the MM (PROSE) [d20-portable]
- **Where:** 04:165–167 (B0 bullet); 04:1302–1303 (Mv V Draunel bullet).
- **Yardstick:** C-V10 [A] (secrets are stated flatly to the DM next to the surface; never coy).
- **Problem:** Both lines describe Master Vell without naming him. 07's header ("Master Vell — the Pale Factor") and 04:1259 confirm who he is. An MM running B0 cold does not know who this is, or that he must stay unremarkable.
- **Fix:** At 04:165, after "unremarkably": add "*(This is Master Vell, Chapter VII.)*". At 04:1302: "a tall pale factor" → "Master Vell".

### BALL-12 [P2] Callun's payments have no amounts (MECHANICS)
- **Where:** 04:1097–1099 (Mv III: "a quiet question… with coin behind it"); 04:759–763 (Undercurrent C: selling the nursery, "She pays on delivery").
- **Yardstick:** C-S45 [A] (NPC payments state amounts and conditions); C-V25.
- **Problem:** Players will ask "how much?" in both scenes, and in the nursery sale the price is the choice. 09's Snake Tracker counts "Callun's coin refused in Mv III" as a heat event, so the coin is part of the mechanics.
- **Fix:** Set numbers; these are mechanics, not lore. Suggested: Mv III: "10 gp for his words, now". Nursery: a figure the owner chooses (see N2). Print each in the bullet.

### BALL-13 [P2] DM prose runs long in both sentences and paragraphs (PROSE) [d20-portable]
- **Where:** Whole chapter. Measured over non-box, non-table prose: mean 24.6 words per sentence, median 20, 27% of sentences over 30 words, 47 over 45 words (a rough splitter, so read as an upper bound). 14 paragraphs over 120 words. Worst: 302–316 (B8, one sentence of about 109 words); 668–670; 707–709; 778–788 (Undercurrent D trail, about 138 words across two sentences); 112–120; 499–511; 1162–1175; 1251–1263.
- **Yardstick:** C-V4 [A] (mean 16–19, about 10% over 30 words); C-V5 (paragraphs of 45–75 words; over 120 only in background); S40.
- **Problem:** The chapter reads like a long essay, not a reference an MM scans between scenes. Most of the length comes from long em-dash and semicolon chains that pack two or three instructions into one sentence.
- **Fix:** Split at the dashes and semicolons. Model for B8 (04:302–311), with the voice kept. Before: "Two years of a genius's solitude, and — players will look for papers and find none, because there are none anywhere — the room thinks in crystal: instruments…". After: "Two years of a genius's solitude. The characters will look for papers and find none; there are none anywhere. The room thinks in crystal. On the great table… In a drawer…" Then give each find its own bold run-in, as in B9.

### BALL-14 [P2] AI-rhythm cluster: em-dash density, "not X but Y", inflated asides (PROSE) [d20-portable]
- **Where:**
  - **Em dashes:** about 230 in the chapter. Chains of two or three per sentence appear at 330–345, 614–617, 1255–1257.
  - **"Not X but Y" / "X, not Y" as a flourish:** 68 and 552 (the same slogan twice: "a scene, not a sentence"); 134; 821; 1157.
  - **Inflated or self-praising lines:** 358–359 "In hindsight, this room is the night's most devastating"; 615 "which is somehow more unsettling"; 682 "a door left ajar on something vast"; 780 "a superb scene"; 1164–1165 "the module's best red herring, because it is so *plausible*"; 1083–1084 "the part nobody can stop thinking about"; 718 "let the table feel the floor tilt".
  - **Tricolons and anaphora:** 37–38; 497 "masked, drunk, and delighted"; 819–821 ("the omens still fire, the agendas still collide, the snakes still circle, and the night still works").
  - **Repeated image:** "holding its breath" at 744 and 1248.
- **Yardstick:** Memory rule (prose must read human); C-V13 [A] (no winks or self-regard in DM prose); C-V7 [A] (mood belongs in read-aloud).
- **Problem:** These are the tells a reader spots first. They also add length (BALL-13).
- **Fix:** Light touch, keeping the voice.
  - 68: "**The gatehouse cell is a scene.**" Keep the slogan at 552 only.
  - 134: "This is the first scene of the adventure, not a transition into it." Or cut the sentence.
  - 358–359: cut "In hindsight… devastating."
  - 615: "…no torture-vault, no horror."
  - 780: cut "(a superb scene: …)" and keep the image as plain instruction ("he asks the guest to *hold the thought for him*").
  - 1164–1165: "(They are wrong.)"
  - 1157: "Then the room boils with the promise of news."
  - 819–821: "If a table chases none of them, the night still works. The Undercurrents are depth, not the floor." That keeps one contrast.
  - Aim for no more than one em dash per paragraph in DM prose.

### BALL-15 [P2] Rules-term capitalization is mixed (STYLING)
- **Where:** 04:64 "unconscious and is Stable"; 04:503 "unconscious and stable"; 04:64 and 503 "hit points"; 04:1236 "with Advantage". Module-wide counts: Hit Points 42 against hit points 21; Unconscious 14 against unconscious 3; Prone 18 against prone 1; advantage 31 against Advantage 2.
- **Yardstick:** C-V26 [A] (one scheme throughout), C-V19.
- **Problem:** The chapter mixes 2014 lowercase and 5.2.1 capitals inside one rule. The module as a whole leans 5.2.1 for conditions and Hit Points but 2014 for advantage.
- **Fix:** Apply whichever scheme the lead picks (N3). If it is 5.2.1: "Unconscious and Stable", "0 Hit Points", "Advantage" at 04:64, 503 and 1236.

### BALL-16 [P2] The guard response still disagrees with S4 (MECHANICS)
- **Where:** 04:60–62 ("two… arrive at once, and four more come if the fight goes on"); 04:98–99 (the gate fight "as card S4… two guards"); 09 S4 (titled *The East Wing Doors*; base "Three **Boranis Honor Guards**", reinforcements "at the start of the second round after the first guard is Bloodied"; scaling line "Four at 3rd level: two guards"; Development "Return to Movement V").
- **Yardstick:** C-S13 [A]; C-V16. Still open from `AUDIT_oraga_5e_playability.md` M10 / REVIEW open Q3, now narrowed.
- **Problem:** 04 now says two guards plus four, but it triggers on "if the fight goes on" where S4 triggers on Bloodied. S4's own base (three) disagrees with its scaling line (two). S4 is also named and staged for the east wing corridor and hard-routes to Movement V, while 04 sends Movement I gate fights and any drawn steel to it.
- **Fix:** In 04:61: "…and four more come at the start of the second round after the first guard is Bloodied (*Call the House*; card S4)". For the 09 owner, not this slice: make S4's base match its scaling line, add "the Gatehouse Court, Movement I" to its *Where and when*, and change the Development to "Return to the current Movement".

### BALL-17 [P3] Scheduled beats lack latitude for absent characters, and the Dead Dance box assumes a presence (MECHANICS) [d20-portable]
- **Where:** 04:1131–1137 (the toast); 04:1238–1246 (the Dead Dance box: "A hand is offered to you"); 04:840–845 (gate box). Compare 04:420 ("Four players will be in four rooms by Movement II").
- **Yardstick:** C-S13 [A] (DM latitude to delay or advance); C-S23 [U] (boxes state their assumptions).
- **Problem:** The chapter is built for a scattered party, yet its two big public beats assume everyone is in the room.
- **Fix:**
  - **Toast:** "Characters elsewhere hear of the two plates within minutes. You can hold the toast until at least one character is in the galleries."
  - **Dead Dance:** "Read this to the characters in the Crystal Court. For the rest, read only the first two sentences."

### BALL-18 [P3] Some checks drop the ability or the skill (MECHANICS)
- **Where:** 04:256, 289 ("DC 15 with thieves' tools"); 04:302 ("DC 18 with thieves' tools"); 04:922 ("a DC 13 check in whatever skill the help needs"); 04:1068 ("a DC 13 check of whatever kind the angle is").
- **Yardstick:** C-V15 [A]; S3.
- **Fix:** "a DC 15 Dexterity check using thieves' tools" (×2); "a DC 18 Dexterity check using thieves' tools". For the open-skill cases, give a default and a dial: "a DC 13 check, usually Charisma (Persuasion) or Intelligence (Investigation), or whatever the help needs".

### BALL-19 [P3] The chapter states the DC ladder two ways (MECHANICS)
- **Where:** 04:9 ("Standard DC 13–15 · Hard DC 18–20", matching 01:161–163) against 04:413 ("*Standard* DC 13, *Hard* DC 18").
- **Yardstick:** C-V15 (one DC per check); internal consistency.
- **Fix:** At 04:413: "*Standard* DC 13 (15 when merely competent), *Hard* DC 18 (20 when unearned)". Or point to Chapter I's table and drop the list.

### BALL-20 [P3] "Players" is used for the characters (PROSE) [d20-portable]
- **Where:** 04:303, 723, 752, 756, 813, 1169, 1173 (and "a player who brings her the nursery", 760).
- **Yardstick:** C-V2 [A]; S2.
- **Fix:** "the characters" or "a character who …" in each. Keep "players" at 432 and 1253, where it means the people at the table.

### BALL-21 [P3] Hedges, a rhetorical question and designer-voice asides (PROSE) [d20-portable]
- **Where:** "perhaps" (40, 999); "What then?" (796); "Sit with what that implies" (210); "Let the table sit with it…" (651–654); "Nobody at this ball knows the truth. Not even you." (408–409). That last line says the MM does not know, which is false for the MM (Chapter II) and reads as a wink. Also 674 "the module intends tables to discover it".
- **Yardstick:** C-V6, C-V13 [A]; S25, S27.
- **Fix:**
  - 40: "about two dozen".
  - 999: see BALL-9.
  - 796: "If they act on it:".
  - 210: cut.
  - 408–409: "Nobody at the ball knows the truth, and every rumor is told with total confidence (Table VIII–7)."
  - 674: "The shape of it is discoverable:".

### BALL-22 [P3] British and American spellings are mixed, and so are grey and gray (STYLING)
- **Where:** colours 163, rumour 189, centre 241, labelled 385, recognises 385, colour 1241 (the rest of the chapter is American: rumor, colored, honor). Also grey 877, 886, 950 (Church robes, Callun) against gray 774, 784, 974, 1073, 1090, 1270 (the masks).
- **Yardstick:** C-S39/C-S40 house consistency.
- **Fix:** Use American spelling throughout. Use "gray" everywhere, unless "grey robes" is fixed canon (INVENTIONS #43 uses "grey robes"; if so, keep "grey" for the robes only and log that as the deliberate exception).

### BALL-23 [P3] Continuity and conversion leftovers in B0 and Movement I (CONTENT) [d20-portable]
- **Where:**
  - 04:140–141 (B0 box: "all masked already") against 04:835 ("Masks go on at the door").
  - 04:169 ("*(unchanged, and…)*"): "unchanged" refers to the source edition, which the 5e reader has not seen.
  - 04:153–154 and 04:192–193: the same "no written list… never needed to be" sentence twice.
  - 04:868 (the cup box triggers "halfway up the line") is printed after the head-of-the-line box (840).
- **Yardstick:** C-S12 [A] (stable order); editorial consistency.
- **Fix:**
  - 835: "Masks are on before the gate."
  - 169: cut "unchanged, and".
  - Keep the Corval sentence at B1 only, and make the B0 bullet read "**Corval receives by name**, from memory (see B1)."
  - Put the cup box before the head-of-the-line box.

### BALL-24 [P3] The Snakes This Movement boxes are too long to be sidebars (STYLING)
- **Where:** 04:875–902 (355 words), 938–969 (433), 1093–1122 (425), 1188–1220 (409), 1284–1322 (559). The Summons box (1020–1060) runs 360.
- **Yardstick:** C-S25 [U] (sidebars run 30–200 words).
- **Problem:** These are the chapter's main GM content, not asides. Boxing 400–560 words hides them from scanning and puts them in the same blockquote shape as read-aloud.
- **Fix:** Make each an H4 subsection ("#### The Snakes This Movement — III") with the faction bullets unboxed. Keep the italic "optional; show one or two" note as its lead line. (Separately, LOG_oraga_5e_pass2 recommends cutting *The Snakes in the Pen*, about 560 words, as a triple description. That cut is still pending and is the owner's call; it is not a defect.)

### BALL-25 [P3] Cross-reference collisions (STYLING)
- **Where:** "Knives in the Dark" names both card S2 (09:616) and the Chapter V section (05:694); 04:88 and 04:320 mean Chapter V, and 04:541 uses the phrase for S2. 04:505 "see the sidebar below" (ambiguous; see BALL-8).
- **Yardstick:** C-S41 [A] (cross-references resolve unambiguously; section names in quotation marks).
- **Fix:** Write "(see chapter V, "Knives in the Dark")" and "(card S2)" explicitly wherever either is meant. Renaming S2 is the 09 owner's call.

### BALL-26 [P3] Undercurrent A's door has no retry rule (MECHANICS)
- **Where:** 04:606–612 (DC 18 Intelligence (Arcana) to improvise the key).
- **Yardstick:** C-V16 (retry rules stated when they matter); 04:571–572's own "never let a single failed check close a thread".
- **Fix:** Add "A failed attempt can be tried again after 10 more minutes at the seam. The slate in B8 always works."

## 3. What already meets the official standard (don't break it)

- **Read-aloud boxes (C-S19–C-S22):** every box has a GM trigger line. Lengths run 34–90 words, with the toast at 125 as a set piece. None is over 170. They are in second person, present tense, with numbers spelled out. They contain no DCs, and no PC actions beyond the minor "where you brush them" (221). Box content leads with sight and adds one other sense. The Audience Hall summons box (989–993) is a model: it stops at "Somebody is sitting in the chair" and names no one.
- **Clocked night (C-S8, C-S15):** every Movement opens with a duration, a start time and a *Run / If you have time* list. The one short rest is placed and costed (B6).
- **General Features (C-S11):** *The Palace on Alert* and the trespass numbers (286–290) are stated once, and rooms say "if alerted" and stop.
- **Losing is not a game over (C-S35):** the gatehouse cell as a one-Movement scene with a rescuer and a favor; *When Somebody Draws Early*; the knockout rule for guards.
- **Pacing and troubleshooting (C-S25 troubleshooting; the DDAL04-04 pacing caution):** *Running a Scattered Party* and *Threading the clock*.
- **Timed events with prevention conditions (C-S13):** the Thenya wall ("at the half-bell", heat 3+, "if nobody stops them"), Vell at the river gate (paired conditionals, 1261–1263), the midwife's glimpse ("end of Movement II"), the Draunel appointment ("first quarter-bell"), and S7 respecting R6.
- **Host set piece (C-S16):** the summons topics list, and the toast as a DM-fired interruption that routes onward ("Go to Chapter V").
- **Fail-forward social design (C-V12):** Undercurrents with redundant trails and an explicit rule that no single failed check closes a thread; tiered approaches (the footman at DC 10 gentle or DC 18 hard; Corval's help needs no check, doing it *well* is DC 13); success at a cost.
- **Mechanics grammar (C-V15, C-V21):** almost every check is "DC N Ability (Skill)". Spells are italic lowercase (*knock*, *speak with dead*, *legend lore*, *detect thoughts*, *zone of truth*). The obvious magical shortcuts are closed on the page.
- **Stat blocks (C-S32):** every bolded block name in the chapter exists in `10_Bestiary.md`: Boranis Honor Guard, Feuding Kinsman, Tavva, Gallery Knife, Circle Hired Knife, Church Warden, Draunel Duelist, Boranis Cousin's Blade, Phern Bodyguard, Thenya Border Slinger. Raunu's ward is under *If It Comes to It*.
- **Cross-references resolve:** Table I–1 and I–3 (01), Table VIII–4 and VIII–7 (rumors 5 and 11 match), the palace diagram (08 *The Palace, Keyed*, including B13), cards S1–S14, Chapter V's ⟨If History Breaks⟩ and *Knives in the Dark*.
- **Canon:** I found no new, unlogged fictional fact in the chapter. The snake tells are logged (INVENTIONS #1–16, #42–47, #55–56).

## 4. NEEDS-RULING

- **N1 — How does the Agenda 4 character get past the east wing doors? (BALL-1)** *Background:* the module says Agenda 4's errand is one of three ways in, but never says what the character does at the doors. The canon we have is the grandmother's ring (03, Handout 2) and Raunu's line "If she chooses you, you will know." *Question:* may the page say that the character shows the ring to the door guards, the ring is carried in, and Veier sends for them (by default, she does)? And at the dinner for two, may Raunu and Veier speak to the topics in 07 only, with Raunu refusing to say what the midnight announcement is?
- **N2 — What does Callun pay? (BALL-12)** *Background:* Callun offers coin for what a summoned guest heard (Mv III), and pays "on delivery" if a player sells her the nursery (Undercurrent C). No sum is printed. Prices are mechanics, but the nursery sale is a moral choice, and its price shapes it. *Question:* is 10 gp for the Mv III question acceptable, and what should the nursery fetch?
- **N3 — One capitalization scheme for rules terms (BALL-15)**, for the lead to settle module-wide: 5.2.1 capitals (Unconscious, Stable, Hit Points, Advantage) or 2014 lowercase. The module leans 5.2.1 for conditions and HP, but not for advantage.
- **N4 — The Attendant after it is confronted (BALL-2).** *Background:* the page says both "one habit per Movement" and "gone until the Unmasking" once followed. *Question:* should it vanish for the rest of that Movement only (recommended), or until midnight? If until midnight, should S14 still pay its +2 for habits the table never saw?
- **N5 — Which Movement does the Seating Feud belong to by default (BALL-8)?** Recommended: Movement II, with Movement III as the fallback, over before the toast.
- **MM terminology:** "MM" works cleanly throughout this chapter. I have nothing to add to the ruling already being raised.

## 5. Status after fix pass (2026-10-03)

*Final review T9.3, fresh eyes. Checked against `04_The_Ball.md` at HEAD (`cd174bf`, 1,406 lines) and
`git diff pre-official-5e..HEAD`. Line numbers below are HEAD lines. `lint_5e.py --file 04_The_Ball.md`:
0 hard hits, 0 structure hits; mean 13.46 words per sentence, 5.28% over 30 words, 1.54 em dashes per 1k words,
0 paragraphs over 120 words.*

**Counts:** 25 fixed · 1 gated (Q15) · 0 partly fixed · 0 skipped · 0 regressed. BALL-1 is fixed, but its two leftovers are gated on Q7 and Q23.

| ID | Status | Evidence |
|---|---|---|
| BALL-1 | fixed (leftovers gated Q7, Q23) | Mv IV time box now lists "if anyone carries Agenda 4, dinner for two in the east wing (B9)" under *Run* (1149–1151). `#### Dinner for Two (B9)` (1246–1294) has the Q6 access step with the ring (1252–1255), a trigger, a 78-word box, Veier and Raunu envelopes, "Raunu does not say what he will announce", Topics taken from 07, a 10-minute cap, and an exit to Mv V. B9 (346–348) and Undercurrent C (745–746) name the ring. `TODO-Q7` at 1289. Q23 ("no husband", but Raunu is at the table) is logged and open. |
| BALL-2 | fixed | 883–886: "It is gone for the rest of that Movement and turns up in the next one as printed." 07:620–621 matches. |
| BALL-3 | fixed | B2 (226–236), B4 (246–259), B6 (268–282) and B9 (336–349) now run header → trigger → box → DM text. B2/B4/B6 re-descriptions cut. |
| BALL-4 | fixed | The chapel box ends on the seven niches (272–274). The offerings are now behind the DC 10 Perception check in DM text (276–280). |
| BALL-5 | fixed | Summons converted to the DM subsection "Raunu's Summons: the Questions, and What He Says" (1078–1111): roman text, bold quoted questions, quoted replies. Toast (1164–1180): speech in quotes, stage cues roman in parentheses. |
| BALL-6 | fixed | 202–204: failing by 5+ means the bearer is refused, with the kitchens (B10) as the route in. The audit's "another guest's arm" and "sends for a guard" were left out on purpose as new detail (LOG T3.1). |
| BALL-7 | fixed | B0 result (181–183), B3 (243–244), Mv II "open gratitude" (939), Mv III "Corval fetches that character at the next summons" (1057–1058). |
| BALL-8 | fixed | Heading "(Movement II, or III; the Banquet Galleries)" (480). Timing per O7 (489–491). Sidebar pointer names "Guards are a scene, not a sentence" (499–500). 09 S1 *Where and when* matches. See NEW-BALL-6 for the Mv III time box. |
| BALL-9 | fixed | "Raunu summons four guests all night. At least one, and by default two…" (1019–1020); "about five questions or five minutes" (1036); the friendly trigger and its default (1041–1043). See NEW-BALL-3 and -4. |
| BALL-10 | fixed | 671–673: a Scora needs no check; anyone else makes a DC 15 Intelligence check after 10 minutes, or needs no check after an hour. |
| BALL-11 | fixed | "(This is Master Vell; see chapter VII.)" (166); "Master Vell is standing at the river gate" (1378–1379). |
| BALL-12 | gated (Q15) | `TODO-Q15` at 767 (nursery) and 1123 (Mv III coin). No amounts printed. Correct. |
| BALL-13 | fixed | No paragraph over 120 words. Mean 13.46 words per sentence. B8 has a bold run-in per find (310–324). Undercurrent D's trail is bulleted (782–796). See NEW-BALL-8 on choppiness. |
| BALL-14 | fixed | "The gatehouse cell is a scene." (68). The slogan survives only at 548. "In hindsight…", "superb scene", "best red herring", "door left ajar", "floor tilt" and "nobody can stop thinking about" are all gone. "(They are wrong.)" (1189). Undercurrents sidebar (831–832) as proposed. Em dashes 1.54/1k. |
| BALL-15 | fixed | "Unconscious and Stable", "0 Hit Points" (64, 497); "with Advantage" (1310). No lowercase rules terms left (lint 0). |
| BALL-16 | fixed | 60–62: "four more come at the start of the second round after the first guard is Bloodied (*Call the House*; card S4)". 09 S4 now has two guards, the Mv I gate and "Return to the current Movement". See NEW-BALL-1 for a new S4 line that conflicts with 04. |
| BALL-17 | fixed | Toast can be held, and the news travels (1159–1160). The Dead Dance trigger says who hears the whole box (1312–1313). |
| BALL-18 | fixed | "a DC 15/18 Dexterity check using Thieves' Tools" (265, 297, 310–311). Open-skill checks give a default (937–938, 1055–1056). |
| BALL-19 | fixed | The header ladder matches chapter I (9–10). *Social checks* points to chapter I's section and no longer restates it (428–430). |
| BALL-20 | fixed | No "the players" meaning characters (lint 0). "Player character" survives at 1020 and 1118–1119, where it separates PCs from NPC guests. |
| BALL-21 | fixed | "about two dozen" (39); "If the characters act on it:" (806–807); "Sit with what that implies" cut; "every rumor is told with total confidence (Table VIII–7)" (425–426); "The shape of it is discoverable." (677). |
| BALL-22 | fixed | British spellings 0, "grey" 0. Church robes are "gray" (901, 969), per LOG T4.6's reading of INVENTIONS #43. |
| BALL-23 | fixed | "Masks are on before the gate" (846); "unchanged" cut (169); the B0 bullet is "Corval receives by name, from memory (see B1)" (154); the cup box now comes before the head-of-the-line box (851–863). |
| BALL-24 | fixed | Five `#### The Snakes This Movement — I…V` sections, unboxed. *The Snakes in the Pen* was cut to a pointer and Table IV–1 (455–470), per Q21. |
| BALL-25 | fixed (moot) | S2 is now "The Service Corridor Job". 04 points to chapter V's "The Snakes in the Dark" (87–88, 333). No "Knives in the Dark" collisions. |
| BALL-26 | fixed | 606–607: "A failed attempt can be tried again after 10 more minutes at the seam. The slate from the study (B8) always works." |
| N1 | resolved (Q6) | See BALL-1. |
| N2 | gated (Q15) | See BALL-12. |
| N3 | resolved (O1) | SRD 5.2.1 capitals module-wide. |
| N4 | resolved (O2) | Vanishes for one Movement. S14 counts only habits the table saw. |
| N5 | resolved (O7) | Movement II by default, Movement III as the fallback, over before the toast. |

## 6. New issues found in final review

*Most of these are new problems or regressions from the fix pass. NEW-BALL-7 is a leftover from an earlier sweep, and NEW-BALL-9 lists defects that predate the pass but that BALL.md missed, kept at P3. No module file was edited.*

### NEW-BALL-1 [P2] Card S4's new Development line contradicts chapter IV's invitation rule (cross-file; fix-pass regression)
- **Where:** 09:960 (new in this pass): "If an out ended it, no invitation is void." Against 04:65 ("When steel is bared… The offender's invitation is void for the rest of the night"), 04:79–81 ("When the east wing is forced… the offender's invitation is void whether or not they were caught in the act"), and 04:101 ("The offender comes back in Movement II with no invitation"). 09 S4's own "Losing costs… its invitations' good standing" (941–942) is fine.
- **Problem:** A DM who resolves a Movement I gate fight or a forced east wing door by an out (a good story, a name, walking away) gets opposite answers from the two chapters on whether the invitation survives.
- **Fix (09 owner; 04 needs no edit):** "**Development.** If expelled, the offender is put out and Corval is informed. Bared steel or a forced door voids the invitation either way (chapter IV, "The Palace on Alert"). An out spares the character the cell, not the invitation." Or, if the intent is that an out saves the invitation, change 04:65 and 04:80 to "…void unless an out ends the scene (card S4)". That changes a rule, so it is the owner's pick. The first option keeps 04 as printed.

### NEW-BALL-2 [P2] "Getting in" has no timing, but the dinner is fixed after the toast
- **Where:** 04:1248 ("Run this after the toast") and 1252–1254 ("A character who shows the door guards the grandmother's ring… is asked to wait. The ring goes in. If Veier chooses them… a guard walks them up"). Against 04:941 (Mv II: "The east wing's guarded doors scouted (Agenda 4)") and 1050–1052 (Mv III: "If she chooses you, you will know").
- **Problem:** The Agenda 4 character will most likely show the ring in Movement II or III, when they first reach the doors. The page doesn't say whether the guard walks them up then (before the toast, with Raunu still in hiding and the dinner box not yet true) or whether they wait. A DM following "Getting in" literally runs the dinner box in Movement II.
- **Fix (a timing default, not canon; offer it to the owner with Q23):** add after 1254: "Whenever the ring is shown, the answer comes after the toast. A guard finds the character wherever they are as the galleries empty." The present-tense box then holds.

### NEW-BALL-3 [P3] The summons' "true thing" trigger is stated twice in a row
- **Where:** 04:1040–1042: "Impressing him takes no check at all: tell him a true thing he did not already know. He turns friendly when the guest tells him a true thing he did not know, or sits through the silence without filling it." (The second sentence is the BALL-9/O12 addition.)
- **Problem:** The reader can't tell whether "impressing" and "friendly" are two states or one. The prose stutters.
- **Fix:** "Impressing him takes no check at all. He turns friendly when the guest tells him a true thing he did not already know, or sits through the silence without filling it."

### NEW-BALL-4 [P3] The "friendly by default" rule breaks on the paired summons
- **Where:** 04:1042–1043 ("By default, he is friendly with the second summoned character"), against 04:446–447 ("At least once in Movement III, Corval fetches two characters at once") and the Mv III time box (992–993: "one summons (two characters walked in together)").
- **Problem:** On the default run, both characters walk in together in the one summons, so neither is clearly "second".
- **Fix:** "By default, he is friendly with the second character summoned. If two come in together, that is whichever of them speaks second."

### NEW-BALL-5 [P3] The dinner box names Veier before the characters have identified her
- **Where:** 04:1260–1261 (box): "Raunu Boranis and Veier Nolonaire are eating off them side by side".
- **Problem:** By the legend in 01 and C-S21, a box never names someone the players haven't identified. Raunu has been seen unmasked at the toast, but Veier has been seen by nobody.
- **Fix:** "…and Raunu Boranis and the woman you came to find are eating off them side by side…"

### NEW-BALL-6 [P3] The Movement III time box omits the feud fallback the BALL-8 fix created
- **Where:** 04:992–994 (Mv III *Run* / *If you have time*), against 04:489–491 ("You can hold it until Movement III") and 08 Table VIII–1 Mv III ("S1 if held from II").
- **Fix:** Append "and S1, if it was held from Movement II" to the Mv III *If you have time* list.

### NEW-BALL-7 [P3] One emphasis italic missed by the Phase 9 sweep
- **Where:** 04:1155: "Raunu Boranis is simply *standing at the high table*". This is DM prose, not read-aloud, and it isn't on the LOG's kept-by-rule list.
- **Fix:** Set it roman.

### NEW-BALL-8 [P3] A few split passages now read as staccato (pilot ran below the later 14–19 calibration)
- **Where:** 04 averages 13.46 words per sentence, below the 14–19 band the coordinator set after the pilot (LOG Phase 7, T7.2 note). The worst spots: 1070–1073 (four sentences in a row opening "They"); 1189–1190 ("(They are wrong.) Draunel fears a succession decree. Kovaun's question acquires teeth. Vorlain goes quiet and drinks."); 1270–1272 ("He listens completely. Raunu does not say what he will announce at the Unmasking.").
- **Fix (light touch):** 1071–1072: "They will do nothing at all until midnight; they are waiting for the one moment custom guarantees the recluse must appear." 1189–1190: "Draunel fears a succession decree; Kovaun's question acquires teeth; Vorlain goes quiet and drinks." 1271–1272: "He listens completely, and he does not say what he will announce at the Unmasking."

### NEW-BALL-9 [P3] Defects that predate the pass and that BALL.md missed (fresh-eyes catch)
- **Undercurrent C still reads as the only road to Veier.** 04:560–562 ("if anyone carries Agenda 4, it is the way to Veier"), 733 ("*(needed if anyone carries Agenda 4)*") and 1197 ("Undercurrent C is the map"). Since BALL-1, the ring gets the Agenda 4 character in without C. **Fix:** 562 "it is a way to Veier"; 733 "*(run it if anyone carries Agenda 4)*". 01:26 can stay as written.
- **A broken sentence** at 04:633–635: "Reading the gift in what, the room answers quietly: a chair with a wide armrest…". **Fix:** "Reading the gift in whom? The room answers quietly: a chair…" Or, keeping S27 at zero: "What they were reading, the room answers quietly: a chair…"
- **An echo** at 04:256: "ministers screening supplicants through a screen so thin it is almost an invitation". **Fix:** "ministers vetting supplicants through a screen so thin…"
- **A heading range that is off.** 04:517 "*(Movements III–VI — one trouble in three sightings)*", but the raid is "Movements VI–VII" (541). **Fix:** "*(Movements III–VII…)*".
- **Cross-reference form** (style sheet): 04:385–386 "Found only through Undercurrent A — The Root of the House, this chapter" → 'Found only through "Undercurrent A — The Root of the House", below'; 04:1393 "(chapter IX, the Snake Tracker)" → '(see chapter IX, "The Snake Tracker")'; Table IV–1 headers "*(Ch. VII)*", "*(Ch. IX)*" → "(chapter VII)", "(chapter IX)".

**No other new problems.** Every pointer checked resolves: chapter I "Checks, Inspiration, and the Ladder"; chapter II "Why the Ball"; chapter V "The Snakes in the Dark" and ⟨If History Breaks⟩; 07 "Veier Nolonaire — the Bride"; 09 "Running the Snakes" and cards S1–S14; chapter X "If It Comes to It"; Tables I–3, VIII–4 and VIII–7 (rumors 5 and 11). The Dinner Topics match 07's *What Veier Knows* line for line. No invented fact was found in the new Dinner, gate-failure, B0/B3 or summons text. The facts that left with *The Snakes in the Pen* are kept elsewhere: "the attack blindsides every faction" is at 05:798, and the heat rule is in 09.

### 6a. Resolved (Phase 9 final-review fixes, 2026-10-03)

| ID | Resolved | Note |
|---|---|---|
| NEW-BALL-1 | fixed | 09 S4 Development: "An out spares the character expulsion, but bared steel or a forced door voids the invitation either way (see chapter IV, "The Palace on Alert")." 04 unchanged. |
| NEW-BALL-2 | Planner O27 | 04 Getting in: "Whenever the ring is shown, the answer comes after the toast: a guard finds the character wherever they are." Q23 stays open. |
| NEW-BALL-3 | fixed | One statement of the "true thing" trigger. |
| NEW-BALL-4 | fixed | "…the second character summoned; if two come in together, that is whichever of them speaks second." |
| NEW-BALL-5 | fixed | Box: "Raunu Boranis and the woman you came to find…". |
| NEW-BALL-6 | fixed | Mv III *If you have time* adds "S1, if it was held from Movement II". |
| NEW-BALL-7 | fixed | "standing at the high table" roman. |
| NEW-BALL-8 | fixed | The three joins as proposed. |
| NEW-BALL-9 | fixed | "a way to Veier"; Undercurrent C tag "(run it if anyone carries Agenda 4)" (flow.json anchor updated); 1197 "the ring at its doors, or Undercurrent C"; the broken sentence → "What they were reading, the room answers quietly:"; "vetting supplicants"; "Movements III–VII"; B11 and Snake Tracker pointers in STYLE form; Table IV–1 headers "(chapter VII)", "(chapter IX)". |
| SNAKES-25 (04 side) | fixed | 04's heading is now "The Snakes at a Glance" so that no heading reads "The Snakes in the Pen" (09's is "The Snakes at the Ball"). No pointer targeted 04's heading; INVENTIONS #1 re-pointed. |
