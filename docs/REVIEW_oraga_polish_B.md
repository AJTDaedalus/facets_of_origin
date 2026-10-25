# REVIEW: Oraga Night 5e, polish pass B (the midnight attack)

*Fresh-eyes rules edit, 2026-10-25. Scope: 05 and 08 in full; 09 opening rules and cards S3, S8, S10, S14;
10 opening, "What spells buy", the Attendant, the Wept, the Radiant, the Hollow and Master Vell. Authority:
DECISIONS TP1–TP46 and TPN-1–TPN-20, and DESIGN_oraga_5e_3p_pass §2–§4 (§3.6 void per TP43). No module file
was edited. Line numbers are as of commit b89e14e.*

Where a finding sits on a task that TASKS_oraga_5e_3p_pass still lists as open, the task is named
("scheduled: T7.2"). These are still findings, because the text a DM would run tonight is wrong. They just
aren't news to the Planner.

**Counts:** 5 blocker · 21 should-fix · 15 polish.

---

## Blockers

### B1. The Root is printed as a refuge the Uninvited won't enter. It contradicts TP8/TP17/TP18 and the book's own trap rule *(scheduled: T7.2)* — **FIXED (05, 08, 10; 04 is review A's half; guard `root_trap`)**

- **05:54–57:** "A dozen guests can shelter behind the deepest crystal in Rekuzan, and the Uninvited will not go down there. Whatever the deep crystal is to them, they will not cross its threshold. Nothing in this adventure explains why."
- **08:120–121:** "From the Root (B11): … shelter for a dozen, and the Uninvited will not enter."
- **10:197–198:** "(and the Root of the House, the one threshold they will not cross)"

TP8 makes the Root a trap, not a refuge. TP18 says nobody knows the effect, and TP17 says no new safe room. The book also disagrees with itself here. 05:1308 has a table "lure one into the Root's threshold" to trap it, and the Attendant's *Where the Three Go* (10:297–299) "follows its three anywhere, the Root included", so the three go there after all.

**Fix:** delete the shelter and "will not cross" clauses in all three places. Keep the master-valve sentence. Replace the cut text with the TP18 line: nobody has seen what the deep crystal does to creatures like these, and the Uninvited don't know to avoid it. In 08 and 10, point to ⟨They trap one of the Uninvited⟩.

### B2. The Second Clause still ends "and send word to the river" *(scheduled: T7.11)* — **FIXED (05; T7.11 ☑; guard `second_clause`)**

- **05:1138–1139:** "*if a woman in Thenya wool comes out the front, hold her, and send word to the river.*"

TP21 cuts this: the clause ends at "hold her".

**Fix:** "*…comes out the front, hold her.*"

### B3. Three different dying rules for "everything else tonight" *(scheduled: T6.6)* — **FIXED (T6.6 ☑: 05 *Everyone else's steel*, crowd rule scoped, 09/10 pointers; TPN-35; guard `crowd_rule_scope`)**

- **05:283–286:** "Everything else tonight (the snakes, the Bought) uses the ordinary rules for dying, **except that the crowd rule holds anywhere in the palace after midnight.** Someone always comes."
- **05:457–458:** "**Someone always comes.** The crowd rule in 'Down, Not Out' holds anywhere in the palace after midnight."
- **05:806–807:** "*(This mercy covers only the Uninvited, and the Attendant while it is Idle. A snake's knife in the dark is an ordinary knife.)*"
- **09:580–583:** "no snake finishes a downed character … the crowd rule in 'Down, Not Out' holds in every snake fight after the bells"
- **10:41–42:** "after midnight the crowd rule in 'Down, Not Out' gets it up sooner"

The text contradicts itself: 05:806 says the mercy covers only the Uninvited, while 05:285 says it holds everywhere. It also contradicts the ruling. DESIGN §2.1 (Sharp) and §2.2 option 3, both under TP2, say "the crowd rule covers only creatures an Uninvited set aside", and at Sharp a heat-4 snake finishes a downed character who crossed it. The crowd rule's "Nobody is out for longer than two rounds" (05:269–270) also half-promises a rescue to the dying, which T6.6's acceptance line forbids.

**Fix:** per T6.6, rewrite 05:283–286 and 05:457–458 to the dial cells. At Sharp, the crowd rule covers only creatures an Uninvited or the Idle Attendant set aside. Make 09:580–583 and 10:41–42 pointers to that one paragraph, and keep 05:806–807 as written.

### B4. Nobody can tell whether Delay on the Radiant pushes back his three beats — **FIXED (Delay pushes back his beats; *Witnessed* not double-counted; TPN-30)**

- **05:86–91** (Clock step 5): he reaches the garden stair "three beats after Raunu falls … *Witnessed* is the third … You can hold him back while the characters are still in the east wing."
- **08:455:** "The garden stair at Raunu's fall + 3 beats: ☐ ☐ ☐"
- **Table V–1** Radiant row (05:343): "one more person in his way gets clear"
- **05:296–299:** a point spent means "that turn they make no progress toward their errand … a point is a beat"
- **05:325–328:** Witnessed is "half a turn's progress; two such turns are 1 Delay"

The Wept's clock says "plus one turn for each point of Delay spent on her". The Radiant's says nothing, while the general rule says a spent point is a beat of no progress. Witnessed is counted twice: once as the fixed third beat, and again as the half-progress rule. "You can hold him back" is fiat, not a rule. A DM running the east-wing chase, the scene the chapter calls "where the night has been pointing", can't tell whether Delay buys the party time or only buys bystanders.

**Fix (Planner call, not OWNER):** say it one way in step 5, Table V–1, the Radiant's *Delay* trait (10:1474–1478) and the tracker. For example: "fall + 3 beats, plus a beat for each point of Delay spent on him (within the cap); being watched is already counted in the third beat, so *Witnessed* adds no further slowing in the east wing." Then delete "You can hold him back…".

### B5. A faked child's cry is both a DC 13 trick and a free Stop — **FIXED (a real child is the freeze; a faked cry is trick 7, a nature trick; TPN-31; guard `wept_freeze`)**

- **05:387** (Table V–2 trick 7): "**A child crying,** somewhere she can hear it. She goes still at the sound … | Charisma (Performance) or Charisma (Deception)"
- **05:878–880:** "a child crying where the Wept can hear it is the one Table V–6 gives. If a character brought it about, that character landed it."
- **10:2035:** "A child crying where she can hear it does this with no check."
- **08:111:** "or a child crying, for the Wept"

Read together, a character who fakes a cry lands a Stop with no check, once per scene, which makes trick 7 a worse version of itself. TPN-6c reads route (c) as "the only printed freeze". It never says whether a faked cry counts.

**Fix (Planner call):** decide whether a *real* child (a guest's) is route (c) and a faked cry is trick 7, a nature trick worth 2 Delay. If so, say "a real child crying" in 05:879, 10:2035 and 08:111, and give trick 7 its double. If a faked cry is meant to count, cut trick 7.

---

## Should-fix

### S1. The three-turn cap is missing everywhere the Wept's clock is printed — **FIXED (cap on every copy; the Stop round sits outside the cap, TPN-32)**

- **05:80–82** (step 3): "plus one turn for each point of Delay spent on her"
- **05:342** (Table V–1 Wept): "every point spent pushes that back a turn"
- **10:2004–2009** (Wept *Delay*)
- **08:58, 08:455**

Each of these reads as unbounded, but 05:330–332 caps lost turns at three a scene. Nothing says whether the Wept's Stop round (no actions, no movement) counts against the cap.

**Fix:** add "(three at most in a scene; 'Three turns a scene, at most')" to step 3 and Table V–1, and a matching note on the tracker row. Planner: rule whether a Stop's frozen round counts toward the three.

### S2. "Every trick earns 1 Delay", but nature pays double — **FIXED (intro says 2 on nature; rows not marked)**

- **05:373–374:** "Every trick earns 1 Delay on a success, under the rules above."

05:313–316 says a trick on that Uninvited's nature earns 2. Several printed tricks are on nature: V–2 #7; V–3 #2, #3, #4, #6; V–4 #2, #3, #7. The table headers don't flag them, so a DM working off the tables will pay 1.

**Fix:** "Every trick earns 1 Delay on a success, or 2 when it plays to that one's nature." Optionally mark the on-nature rows with a symbol.

### S3. The DM sheet's Buying Time line drops four of the rules a DM needs mid-fight — **FIXED**

- **08:92–96**

The line has the DC and the lump, but not:

- nature pays double;
- spells roll (attack or save; otherwise a spellcasting-ability check at DC 13), once per spell per Uninvited;
- the three-turn cap;
- slowing (two half-speed turns make 1 Delay).

The chapter says to run the night "from the first three pages and the tracker" (08:6), and these come up every round.

**Fix:** add one clause each. For example: "On its nature: 2 Delay. Spells: the spell's own roll, else spellcasting ability vs DC 13; once per spell each. At most 3 turns lost per scene; past that, points still free people."

### S4. The Radiant's "deny the congregation" Stop can't be adjudicated, and two chapters disagree on it — **FIXED ("as well", stated once in 05's Stop rules; TPN-33)**

- **05:419–420:** "A character who puts out the lights to deny him his congregation, as a Stop, makes the Stop check **instead**."
- **10:180–181:** "It still plays to his nature (2 Delay), and a table that means to deny him his congregation has earned a try at his Stop **as well**."
- **10:1509–1511:** "the check itself is Charisma (Performance) or whatever the doing of it fits."

05:866–874 defines a Stop with words, in a voice the Uninvited can hear, within 30 feet. Dousing lamps is not words, so neither range nor skill is defined. "Instead" and "as well" also disagree on whether the dousing still earns its 2 Delay. Elsewhere, darkness makes him *faster* (05:417–418), so a DM has to hold three effects of one act in mind at once.

**Fix (Planner call):** pick one ("as well" matches the "Their nature, three times" route better). In 05's Stop rules, add a line that the Radiant's congregation can be denied by deed as well as words: the doer within 30 feet, check as 10:1510. Make 05:419–420 and 10:180–181 say the same.

### S5. "Comes easiest" is a promise with no rule behind it — **FIXED ("makes most sense")**

- **05:688–689:** "This is where a Stop on him (below) comes easiest: dark, empty terraces, nobody watching"

No rule makes the Stop easier at the Crossing.

**Fix:** "This is where a Stop on him (below) makes most sense in the fiction…", or give a mechanical edge (Planner).

### S6. Spells end "at once" in one place and "hold for a round at most" in another — **FIXED**

- **05:310:** "the leash snaps them out of it at once"
- **10:147–149:** "Whatever the spell would do to them ends at once"
- **05:811–812:** "A spell that would remove, hold, or end one of them holds for a round at most"
- **10:141–143:** "Anything that would hold, block, hide from or wall off one of the Uninvited works for one round at most"

A DM reading 05:812 gives *Hold Person* a round of paralysis. The *Held by Something Else* trait says it ends at once.

**Fix:** keep "one round at most" for barriers and wards only. 05:811–812: "A spell that would remove, hold, or end one of them ends at once; a barrier holds a round at most." 10:141: "Anything that would block, hide from or wall off…" (drop "hold").

### S7. "What changes outcomes" contradicts itself — **FIXED ("What actually moves the night", four items in both)**

- **05:820–822:** "**What actually changes outcomes**: Delay, … Stops and Ends, … and the leash … That is the complete list."
- **05:346–349:** "Delay alone never changes an outcome; ⟨If History Breaks⟩ … says what does."
- **10:194–199:** this "complete list" adds deep ward-crystal; 05's version leaves it out.

**Fix:** retitle 05:820 "**What actually moves the night**", and give both lists the same four items: Delay; Stops and Ends; the trap in the deep crystal; the leash.

### S8. The trap is "brief" in two places and "until the last bell" in two — **FIXED**

- **05:842:** "(a trap, briefly, is the outer edge of the possible)"
- **05:1305–1306:** "trapping one, briefly, is the outer edge of the possible"
- **05:911, 05:1316:** "holds until the last bell"

Holding one of them until the last bell is not brief.

**Fix:** cut "briefly" in both places.

### S9. Who is rowing at the river gate? — **FIXED**

- **05:696–698:** "Vell is already at the oars. The moment the Radiant is past him he takes his *Elsewhere* action (chapter X), and the boat pulls out with him in it."

Vell is holding the Radiant when the Radiant breaks past him, so he can't already be at the oars. The second sentence says he gets there by *Elsewhere*.

**Fix:** "A heartbeat later Vell is at the oars: the moment the Radiant is past him he takes his *Elsewhere* action…"

### S10. Corval's night has no end point, and his route crosses Vell's — **FIXED (garden stair while the terrace is empty; then the head of the service stair; TPN-36a)**

- **05:180–187:** Corval takes the party "by the routes he knows: the service stair … and the garden stair from the upper terrace", while "Vell meets her at the foot of the garden stair. Corval never meets Vell."
- **08:65:** "→ service stair or garden stair, in front of the Radiant."

If Corval brings the party up the garden stair from the upper terrace, he passes the foot of that stair, which is where Vell is waiting. Neither text says what Corval does once the party is in position. Does he stay, go back to the hall, or count staff (as he is at 05:1090)? The brief asked "where Corval goes", and the answer isn't printed.

**Fix:** one sentence. For example: "Once they are in front of the Radiant he leaves them and goes back down to his people. Movement VII finds him counting them (the read-aloud)." Also time his garden-stair use before Vell arrives at its foot, or route him by the service stair only. Whether he survives depends on the party; check against TP40.

### S11. The tracker can't track the threat rule or the cap *(scheduled: T2.6)* — **FIXED (T2.6 ☑: turns lost, Delay by whom, threats, End tries)**

- **08:450–460** (Table VIII–10)

The table has no row for who is marked as a threat to each Uninvited, no count of Delay earned per creature per scene (the "three times in one scene" trigger), and no count of turns lost this scene (the cap). These are exactly what "drifts if you carry it in your head".

**Fix:** add three rows: "Threats this scene (initials)"; "Delay earned this scene, per character (three = threat)"; "Turns lost this scene ☐☐☐".

### S12. The snakes' risk options from TP2 are not in the text yet *(scheduled: T6.2, T6.5, T6.7)* — **SKIPPED (WP6: T6.2, T6.5, T6.7 rebuild the heats and rule 2; not a polish fix)**

- **09:53–55** (rule 2): "No snake ambushes a character, and no snake is the reason a character dies before midnight." DESIGN §2.2 option 1 replaces this with "Every ambush is foreshadowed…".
- **05:1014:** "None of it is ambush."
- **09:575–578:** "Death before midnight" has no cost table (option 2).
- **08:260–263 and 09:490–495:** "the only card live in the dark by default is **S11**". Option 5 calls for two cards live by default (S11 and S12, the Circle starting at 2).

**Fix:** per WP6. Don't touch the heat numbers until T6.7.

### S13. The 2014 box still uses four-player figures — **FIXED (850 × 2 = 1,700; 3,900 is 2.6 × Deadly; TPN-36c)**

- **10:82:** "S3's 1,500 XP becomes 3,000, past Deadly, and S14 is nearly twice Deadly."

S3 prints 850 XP for three (1,500 is the four-player and Nastier line). S14's 3,900 is about 2.6 times the 2014 Deadly threshold for three 4th-level characters (1,500), not "nearly twice".

**Fix (TP10):** "S3's 850 XP becomes 1,700, past Deadly, and S14 is more than twice Deadly." The doubling of 850 assumes 2014's ×2 multiplier for five foes, so re-derive it before printing; flag to the Planner rather than guess.

### S14. Broken cross-reference for Veier's gift — **FIXED**

- **10:2092–2093:** "Her gift flares once, on behalf of someone she loves who is in mortal danger (see chapter V)."

Chapter V never mentions it. The text is at 07:122–124.

**Fix:** "(see chapter VII, Veier)".

### S15. ⟨The child is taken⟩ list doesn't match TP45 — **FIXED (list and trick 4)**

- **05:1289–1292:** "someone stops the boat, holds Veier back from it, drags her to the front gate instead, or otherwise stands between her and the water"

TP45's list is: stopping the boat, *barring the river gate*, holding Veier back, or taking her to the front gate. Barring the gate is missing. Table V–5 trick 4 (05:430), "**Shut the river gate** behind the boat and hold it", sits right beside it and protects the escape. A DM may read the two as the same act.

**Fix:** add "bars the river gate before she is through". In trick 4, "behind the boat" is already clear; consider "once the boat is through".

### S16. The opening principle gives the Attendant the wrong job — **FIXED (parenthetical trimmed to a pointer)**

- **05:31–32:** "What they do to people who get in the way is the Attendant's business, and that is below too."

The sentence just above it says what the Uninvited do to people in the way: the threat rule. The Attendant's business is its *own* violence.

**Fix:** "The Attendant, which can kill, is below too." Also consider cutting the whole parenthetical (05:28–32) to a pointer. It is five lines restating "Down, Not Out".

### S17. "The one who marked it" has no clear subject — **FIXED**

- **05:243–244:** "The one who marked it finishes it only if it is still between them and their errand on their next turn."

The creature did the marking. The Uninvited is the one marked against.

**Fix:** "The Uninvited it threatens finishes it only if…"

### S18. A broken focus may cost the Attendant nothing — **FIXED as a clarification (rule kept as the sim runs it; TPN-34)**

- **10:246–247, 10:269–270; 09:1939–1940**: "breaks its focus until the start of its next turn"
- **10:304–306:** while Focused it takes two turns a round, and it re-checks Focused "at the start of each of its turns"

If the break lands between its first and second turns, the Attendant re-Focuses at the start of the second and loses nothing except the count toward four. Neither text says whether an Idle Attendant still takes the second turn at count −10.

**Fix (Planner, check against the sim's s14.py):** add one clause to *Two Turns*: "If it is Idle when its second turn comes, it doesn't take it."

### S19. Table VIII–6 has the Radiant in the hall when TP34 sends him out — **FIXED**

- **08:285** (Uninvited, IV): "B2 edge, still"

TP34 has the Radiant slip out to walk the garden route after his blessing, which is the mews omen. 08:47 and Table V–6 also put the blessing in B3, not B2.

**Fix:** "B3 for the blessing; then the Radiant is gone a while (the mews)."

### S20. S10's window height disagrees with the east wing *(OWNER/WP8, T8.4)* — **OWNER (T8.4; no ruling)**

- **09:1491–1492:** "one lit window on the second floor"
- **09:1523:** "The wall is 20 feet of grown crystal to the window"

05:525–532 puts the east wing at gallery level, 12 feet up, and puts "the second floor" in the dark wing (B8). Nothing settles which is right.

**Fix:** OWNER/T8.4.

### S21. Clock step 8 is too knotted to read at the table — **FIXED**

- **05:95–100:** "Then the last bell rings, no later than the sect guard's arrival, the clock on card S3. That clock counts only the rounds the characters spend at the gate; the bells that begin in step 4 are only the warning, so the last bell never rings during the Crossing. If no character reaches the gate by the end of Movement VII, the sect guard arrives, ending 3 plays out offstage, and the last bell rings."

**Fix:** "**The front gate is decided** (card S3), by any of its three endings, and the last bell rings. S3's sect-guard clock sets the latest it can be: that clock counts only rounds spent at the gate, so the last bell never rings during the Crossing. If no character reaches the gate by the end of Movement VII, ending 3 happens offstage and the bell rings." Saying "front gate" also separates it from the river gate (see P15).

---

## Polish

- **P1 — FIXED. 05:39–44:** the ward-steering sentence puts two DCs and three conditions in one clause. Suggest: "Steering a Boranis ward takes an action at a ward-point and an Intelligence (Arcana) check: DC 13 if the character studied the wards (or is an Orthaen who has read them by hand tonight), DC 18 otherwise. The Orthaen Gift's knack applies."
- **P2 — FIXED. 05:1137–1138:** "(the second, sealed clause of the contract's terms, though it is the third task)" is a parenthetical that makes the reader count. Suggest: "**The Second Clause**, sealed, which the captain alone has read:".
- **P3 — FIXED. 09:1882 vs 09:1888–1890:** "nobody gets through 178 Hit Points in the rounds an errand takes", then "A table … built to hit hard can out-slug it". Change to "few tables get through". Also cut "Let your table manner carry that, not those words: the hints below are how" (09:1887–1888), which is opaque. Suggest: "Play it that way at the table; the hints below show how."
- **P4 — FIXED. 05:626–630:** "no faction, no clock, nothing at stake but property and decency … no tells, leash, or ward-lore — just a blade and the willingness" stacks two triads and an em-dash. Suggest: "This is the fight for the noble-minded: nothing at stake but property and decency, and it needs only a blade and the willingness."
- **P5 — FIXED. 10:1504–1505:** "not from the hunt, not from the errand, not by darkness or doubt" is a triad tic. Suggest: "The Radiant can't be turned from the hunt, by darkness or by doubt."
- **P6 — FIXED. 10:1553:** "Breaks. Never. Only guilt slows him, and only the leash stops him." *Witnessed*, Delay and the trap all slow or hold him too. Suggest: "Never. Guilt slows him; the deep crystal can hold him; only the leash stops him."
- **P7 — FIXED. 08:471:** "(Table V–4 for the doors)" sits beside "doors ○ ○" (the Hollow's doors, Table V–3). Suggest: "(Table V–4 for the sealed doors)".
- **P8 — FIXED. 05:412** (V–4 trick 5): "Wisdom (Survival) to lead him, DC 15 the first time" under a header that says "DC 13; DC 15 the second time". If intended, say "DC 15, even the first time".
- **P9 — FIXED in 09 ("empty", and TP53's sources; 04's word is review A's). 09:1543** "the unpacked traveling pack" (matching 04:779) vs **09:446, 09:488** "the empty traveling pack". Use one word; "unpacked" is 04's.
- **P10 — FIXED (row added). 01 Table I–3** has no row for a landed End, though 05:901 awards Heroic Inspiration for one, and 01's note says printed awards are reminders of I–3 rows. Add a row, or note the End as an exception.
- **P11 — FIXED (and guests moved early). 05:1218:** "And then the counting: Raunu Boranis is dead." This is wrong on the save-Raunu branch. Suggest: "Raunu Boranis is dead (or, at a table that saved him, alive and dangerous)", or just "And then the counting." with a pointer.
- **P12 — FIXED. 05:15–21:** "When the table needs the attack to end, bring the Crossing to the table" overrides the clock without saying so. Add "(sooner than step 5, if you must)".
- **P13 — FIXED. 10:1457–1458:** "or at the last bell, if it comes first". Per the Clock, the last bell can't come before the boat clears. Cut the clause.
- **P14 — FIXED. 08:60** (Table VIII–2 Hollow): "Herds the crowd back in. His End opens the doors". It omits that he turns east and the doors open when Raunu falls (Clock step 4). Suggest: "…His End opens the doors; so does Raunu's fall (he turns east)."
- **P15 — FIXED (05 clock and Crossing, 08 bells and gate lines). "The gate":** chapter V uses it for both the river gate (the Crossing, 05:691–716) and the front gate (B12, step 8). Write "river gate" and "front gate" every time in 05:691–716, the Midnight Clock and 08:128–134.

---

## Leftovers of cut content: what the sweep found

- **Cup on the Attendant:** none in 05/08/09/10. TP30 is applied in 05:161, 05:494–496, 08:19, 08:468, 09:1918, 09:1960–1962 and 10:268, 10:336–339. The cups at 05:399 (the Hollow trick), 09:296 and 10:915/1886 belong to others.
- **Scorched drawer:** none (TP38 applied in S8 and 05:1032, 05:1339–1340).
- **Last Rite:** none. 05:970–972 and 10:1521 state "no End that words can reach".
- **"Fracture" as a rule word:** none. "The Fractures" survives only as a section name (05:845; pointers at 05:231, 05:315, 05:420, 05:1260, 08:109, 08:445, 10:207), per TPN-6a.
- **"Down, Not Out" promising nobody dies:** the heading is now the threat rule. The surviving rescue promise is the crowd rule's scope (B3).
- **Veier met before the Crossing** — the optional 08:63 wording FIXED ("the household brings her down the private stair to Vell"): none. 08:63 "down the private stair on Vell's arm" (echoing 07:120–121) fits TP40 loosely; 05:186 has Vell meet her at the *foot*. Optional: "the household brings her down the private stair to Vell".
- **Old coin for the Bought:** none (05:1130, 09:906 say ordinary coin). 08:390–393 is Agenda 6's (Vell's) old coin, which is correct per TP44.

---

## Checked and consistent (no finding)

- The Attendant's block arithmetic: 178 = 21d8 + 84 at Con 18 (TPN-1); +7 / 9 (1d10 + 4); Put Aside DC 15; Perception +4 and passive 14.
- The Wept (187, +10, 28, CR 11), the Radiant (162, +9, DC 17, Performance +13) and the Hollow (157, +9, DC 17) are internally consistent.
- Distraction DCs 13/18, Help, +2/+2 (max +4), repeats and the natural 20 agree across 05:494–500, 08:99–108, S14 and 10:260–280.
- *Clears the Way* agrees in 05:351–353, 05:488–490, 08:95–96, S14:1858–1861 and 10:282–288 (TPN-8a).
- The threat rule's triggers and dial cells agree between 05:228–253 and 08:85–91 (TPN-4).
- The Stop DC (15, +2 per tell, max +4), its bands, once per scene, and the End's two tells agree in 05, 08 and 10.
- S3's numbers (850/1,950, captain at the start of round 3, the six-segment clock) agree with 05:1180–1206 and 08:128–134, 08:476–478. S3 at three uses TPN-2's Nastier.
- S8 has no drawer, and its targets are the mist relief and the slate (TP38). S10's "Go with them" matches TP35.
- The Crossing's carry note and healing line match TP41/TP42. The gate's one turn and its dial cells match TP43/TPN-7d. Saving Raunu's steps match TP16/TPN-7a/e.
