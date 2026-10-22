# Voice and Prose Audit: Oraga Night, Fifth Edition (third-party pass)

*2026-10-20. Status: COMPLETE. Auditor role: senior line editor for official 5e adventures.
Scope: chapters 01, 04, 05, 07 read in full; 02, 03, 06, 08, 09, 10, 11 sampled
(02 to the end of "What Is Coming"; 03 opening and gifts; 06 in full; 08 handouts; 09 intro,
S1, S3, S6, S7, S8, S13 and S14 boxes; 10 Uninvited preamble and The Wept; 11 intro and Serane).
Calibration: PyMuPDF extracts of Curse of Strahd (Castle Ravenloft K7–K10 dining hall;
Vallaki N1–N2 and the Special Events, including the Festival of the Blazing Sun and Lady
Wachter's Wish), Lost Mine of Phandelver (the opening of Part 1 and the Phandalin town
overview), and Storm King's Thunder (the Nightstone chapter). The extracts are kept in the
session scratchpad only. Nothing from the references is quoted here. Reference patterns are
described in my own words. The yardsticks are `docs/RESEARCH_5e_module_conventions_voice.md`,
`docs/RESEARCH_5e_module_conventions_structure.md`, the module's `STYLE_5e.md`, and the
owner's standing rule that book prose must read as human-written and get light-touch edits
that keep its voice.*

---

## Verdict

**Score: 7.0 / 10 against the references.** Yes, the book has a voice, and a better one than most
official adventures. It falls short of the references in one specific way, and that problem can be fixed.

| Dimension | Score | Versus the references |
|---|---|---|
| Identity and tone ("glamour over a blade") | 8.5 | Exceeds LMoP and SKT, and matches CoS in its set pieces. The book has a concept you can say in a sentence (snakes in the chicken pen; the host who never finishes his sentence) and images that stick: the inward-facing guard, the two plates, the Attendant's cup. |
| Read-aloud | 8.0 | Short (mean 63–81 words; LMoP and CoS run longer), concrete and speakable. Four boxes slip: one decides an action, one editorializes, one is vague, and one is the epilogue's dream line. Several keyed rooms have no box at all. |
| NPC voice | 7.5 | Raunu, Vorlain and Corval are better than anything in the CoS Vallaki pages: their Q&A blocks can be run from the page. Behind them sits a flat second tier (Kovaun, Callun, Draunel, Essin, Maiven, Tavva, the Bought officers) with traits and no voice, and three characters share the same "unmemorable on purpose" note. |
| DM prose mechanics | 6.0 | The rules sections (Midnight Clock, Down Not Out, Buying Time, room-trick tables, fight cards) are imperative, numbered, present-tense and clear, which is the most official-feeling writing in the book. The connective prose around them has a machine fingerprint. It has 10x the reference rate of colon splices, "X, not Y" reframes where the references have none, half again as many very short sentences, aphoristic paragraph closers, and recurring pet images ("hallways", "arithmetic", "weather", "ammunition"). Designer commentary also leaks onto the DM page. |
| Jargon load | 5.5 | About 40 invented terms a DM must hold. LMoP asks for essentially none and CoS asks for a handful. Four words are overloaded (tell, line, clock, iron), and chapter I uses Delay, Fractures and the Wept before anything defines them. |

**Meets or exceeds the references?** On identity, set-piece read-aloud and the top three
NPCs, the book already exceeds them. On transparency of DM prose it does not, and an experienced
5e reader will feel the difference in the first ten pages. The main giveaway is the colon. The
fix is a light de-patterning pass of roughly 150–250 sentence-level edits across 01, 04, 05
and 07, plus a glossary box and the NPC voice lines listed below. That pass would take the book
to about 8.5. No rewrite is needed and none is recommended: the voice is the asset.

---

## Strengths (keep these; do not let a polish pass flatten them)

1. **Raunu's summons.** The Q&A at 04:1096–1129 (mirrored in 07:48–63) is the best NPC
   writing in the book. The lines are short, they deflect in character, and the dialogue carries the
   characterization: *"I wanted to see what you would do with a long walk." (Beat.) "You did rather
   well. Most people talk."* No reference NPC is this runnable from the page.
2. **Vorlain and Corval.** 07:156–187 and 07:213–249. The NPC is funny when he deflects, and the
   comedy carries the menace: *"Do you know how much work it is, doing nothing where everybody can
   see you?"* Corval's *"like a stone in my shoe"* and *"Please ask me again tomorrow"* give the
   DM a character arc in two lines.
3. **Set-piece read-aloud.** The street (04:141–146), the cup (04:871–874), the gatehouse
   (04:878–881), the toast (04:1181–1197), the lights dying (05:125–130) and the fight-card boxes
   (09:563–566 "Two more are standing because he is."; 09:1210–1214 "the way you wait for a
   kettle"). They are sensory, they put the actionable fact first, they tell the players nothing
   about what they feel, and each fits in one breath.
4. **The rules voice.** 05:71–95, 05:204–283 and the room-trick tables (05:306–363) are written the
   way official text gives rulings: a flat statement, a number, and what ends it. "Someone always
   comes." (05:235) is the right kind of short sentence: a ruling, not an aphorism.
5. **Dry humor in the DM's ear.** 01:380–383 (Corval's sticking door, "because he certainly
   is"); 06 "three inquests wearing one coat"; 04:101–102 "which is a fine way to spend a
   masquerade". This deadpan informational joke is exactly what the voice research allows (C-V13),
   and it fits the project's warm, wry register.
6. **Structure that serves the voice.** Wants / Fears / Secret / Roleplaying / What X Knows is
   more usable than the CoS habit of burying motive mid-paragraph, and the truth-status tags
   ("(untrue)", 07:373, 07:492) follow the official convention exactly.

---

## Tic-rate table

Method: scratchpad script (`tics.py`) over the module markdown, with table and heading lines
stripped, and over the reference extracts, with lines joined and soft hyphens removed. Rates are
per 1,000 words. **Caveats:** the CoS PDF is an OCR scan, and its colon and semicolon counts are
inflated by OCR noise (most CoS semicolons are garbled characters). All three PDFs lose the em
dash in extraction, so the reference em-dash rate cannot be measured from these files. The
module's colon count includes run-in label colons ("**Wants:**", "*Knocked out:*"). The
references write run-in labels with a period, so the row below reports the label colons and the
prose colons separately.

| Measure (per 1,000 words unless %) | CoS (9.2k w) | LMoP (6.0k w) | SKT (4.2k w) | **Module, 6 chapters (≈61k w)** | Module range by chapter | Multiple vs refs |
|---|---|---|---|---|---|---|
| Mid-sentence colon followed by lowercase, prose only | ≤1.3 (OCR-inflated) | 0.0 | 0.5 | **6.7** | 01: 8.5 → 07: 21.8 (all colons) | **~10x** |
| Same, run-in label colons | (labels use periods) | — | — | **5.9** | — | n/a (house style) |
| Semicolons | ≤3.7 (mostly OCR noise) | 0.2 | 0.2 | **5.9** | 4.1 (02) → 10.3 (07) | **~25x vs clean refs** |
| ", not X" reframe | 0.0 | 0.0 | 0.0 | **1.05** | 0.8–1.9 | ∞ (refs have none) |
| "is not X … it is Y" reframe | 0.0 | 0.0 | 0.0 | 0.05 (but see the hand count below) | — | — |
| "the way …" simile | 0.11 | 0.17 | 0.0 | **0.52** | 0 (01) → 1.8 (06) | ~4x |
| "like a/the …" simile | 0.32 | 0.17 | 0.48 | 0.36 | 0.16–0.72 | ≈ refs |
| Triad "a, b, and c" (lowercase) | 0.97 | 1.51 | 0.72 | 0.93 | 0.5–2.2 | ≈ refs (not a problem) |
| Em dash | not measurable | not measurable | not measurable | **3.3** | 0.9 (06) → 5.2 (09) | — |
| Mean sentence length (words) | 19.3 | 19.7 | 17.0 | 17–20 | 16.8–21.4 | ≈ refs |
| % sentences ≤ 6 words | 8.8% | 10.6% | 11.0% | **15–19%** in 01/02/04/05 (24% in 09, 9% in 07) | 5.9–24.4% | **~1.6x** |
| % sentences > 30 words | 13.2% | 10.9% | 7.7% | 9.5–17.5% | — | ≈ refs (07 high) |

**Hand counts the script can't make:**

- **Aphoristic paragraph closers.** These are short abstract sentences that end a DM paragraph on
  a moral or a turn rather than on a ruling or pointer. An automatic short-final-sentence pass
  flagged 57 paragraphs in 01, 04, 05 and 07. By hand, about 26 of them are aphoristic kickers
  (≈0.65 per 1,000 words); the rest are functional ("Nobody but the master goes down there."). In
  the reference pages the short paragraph closers are deadpan facts about the fiction, the
  kind where a villain's cruelty is stated as a plain logistics detail, not morals. The module
  needs about half as many kickers, and the ones that stay should be facts.
- **Recurring pet images** across 01–07 and 09: "hallway(s)" as a unit of rescued time (9),
  "arithmetic" (6), "weather" as a metaphor (5), "ammunition" (4), "load-bearing" (2), "plainly"
  (15), "honest/honestly" (20), "the only" (57), "nobody" (147). The reference pages lean on no
  equivalent recurring figure of speech.
- **Verbatim flourishes reused across chapters**, so the second reading feels generated rather
  than cross-referenced: "rumor has no shelf for it" (04:1307, 07:89); "What makes them
  monstrous is how much of them is left" (02, 07:583); "ringing like a struck glass … pointing
  nowhere" (04:964, 07:384, 07:400); "census of souls" (04:949, 07:301); "the true thing said
  where the polite thing was expected" (04:1046, 04:1290, 07:35); "acquires teeth" (04:1207,
  04:1241); "lands on her like a slap" (04:1258, 07:474); "The Wept is not going anywhere. The
  guest is." (01:492, 05:715); "forgettable on purpose" (07:443 Essin, 07:671 Tavva); "cold
  after the Court" (09:1016, 09:1210).

---

## Findings

### P1: fix before calling the prose official-grade

**P1-1. Colon chains and colon splices (≈10x the reference rate).** This is the single most
visible machine tell in the book. Official 5e DM prose links a ruling to its consequence with a
period, "and", or a parenthesis. It almost never uses a colon mid-sentence, and it never chains
two colons in one sentence. The module does both, often. Worst cases: 04:62–64 (two colons),
04:112–114 (two colons around a parenthesis), 05:1109–1111 (two colons), 04:83–85, 04:739–741,
05:56, 05:1213–1218, 07:203–204, 07:437. **Fix:** in DM prose, turn every second colon in a
sentence into a period, and turn half the remaining single colons into a period or "so". Keep
colons only where they introduce a list or a ruling label. Rewrites R3, R4 and R12 show the move.

**P1-2. Designer commentary and aphoristic kickers on the DM page.** Official text tells the DM
what to do and what is true. It does not explain the author's intent, praise its own
structure, or close on a moral. The module does all three, mostly in 01 and 05:
- Self-commentary: 01:459–460 ("a load-bearing sentence, not a gap"), 05:568 ("This is the
  crescendo, and its rule is simple"), 05:719–720 ("the adventure's spine was negotiable"),
  05:980–985 ("that collision is **deliberate** … Write the herring so it can be untangled"),
  05:729 ("that is the terrible engine of them"), 07:554 ("is the entire exposition"),
  04:184–189 (a seven-sentence pedagogy note on why the first DC is 13; one clause would do).
- Kickers: 01:463–464, 01:470–471, 04:739–741, 04:842, 04:850, 05:569–570, 05:806–807,
  05:989, 05:1041–1042, 05:1099–1100, 07:42–43, 07:531, 07:583–584.
**Fix:** cut the meta, keep the instruction. Of the kickers, keep the ones that are load-bearing
(the owner's rule) and that a DM might say aloud: 01:428–429 "The party is over." and 01:449–450
"It has written its own Val'loh." both earn their place. Rewrite or cut the rest (R1, R2, R9–R11,
R13–R18).

**P1-3. Jargon front-loaded before its definitions.** Chapter I, which the prep box tells the DM
to read first, uses *Delay* (01:401, 01:485), *Fractures* (01:402), *the Wept* (01:479–493) and
*the Bought* (01:177, 01:405) before any definition, which first arrives in chapter II or chapter V.
A first-time reader meets the troubleshooting box "the table will not stop hitting the Wept"
without knowing who the Wept is. **Fix:** add a "Words of the Night" box to chapter I, about 12
lines with one plain sentence each: Movement, omen, agenda, Undercurrent, snake/threat line,
tell, heat, the Uninvited (the Wept, the Radiant, the Hollow), Delay, Fracture, the
Attendant, the Bought, crystal charge, ward-point. Then gloss *Delay* and *the Wept* inline the
first time each appears in chapter I ("Delay, the turns the three lose (see chapter V)").

### P2: fix in the same pass if possible

**P2-1. Overloaded terms.** "Tell" covers three systems: snake tells (chapter IX), Fracture tells
(05:732ff.) and the Attendant's habits, which 01:300 also counts as omens. "Line" covers the
receiving line, a threat line, scaling lines, lines and veils, and "show one or two lines". "Clock"
covers the Midnight Clock (which is an ordered list, not a segmented clock), the fire clock, the
bell clock, the bench clock and the noise clock. "Iron" appears at 05:869 and 05:896 ("the fourth
iron") before chapter IX defines Draunel's four irons (09:262), and 07:415 says "three other
irons … chapter IX names all three" while chapter IX lists four. **Fix:** write "Fracture tell"
every time in chapter V; call threat lines "the Circle's line" only after first use spells out
"threat line"; consider renaming the Midnight Clock "the Midnight Order"; gloss "the fourth
iron" at 05:869 ("Draunel's last plan: …", which the text already gives in parentheses, so move
the gloss before the term); align 07:415 with 09:262.

**P2-2. Second-tier NPCs have traits but no voice.** CoS hands the DM motive verbs plus a line
when a scene turns on that NPC. AL modules give a one-line "Quote:". This module does that for
Raunu, Veier, Vorlain, Corval, Sella and Vell, but not for Kovaun (07:301), Callun (07:363),
Draunel (07:418), Essin (07:443), Maiven (07:473), Corro (beyond one line), Anha (07:263),
Tavva (07:671), the Sergeant (07:722) or the Captain (07:752). Each of these is a scene partner in
a social adventure, so each needs one mannerism and one quotable line. Draunel's "ambitious in the
standard noble key" (07:418–419) is the weakest entry in the cast: the text describes how other
characters relate to him and gives the DM nothing to perform. Three NPCs (Essin, Tavva, Vell)
share the trait of being unmemorable on purpose, and the text points this out for Tavva (07:671).
That works as a joke once, but it leaves three performances sounding alike. **Fix:** add a
**Quote:** line to each, built only from established wants and secrets so that no new canon
enters (see R19 for the method). Give Essin a physical tic instead of a second "forgettable on
purpose". The owner should write or approve these, because they are voice and not structure.

**P2-3. Keyed rooms without read-aloud.** B3 (Banquet Galleries), B5 (Garden Terraces and the
River Gate), B7 (Trophy Gallery), B8 (Study) and B10 (Kitchens) have DM prose but no box. In CoS
every keyed area the party enters gets a box. B5 matters most: it is the Crossing's ground, and
the players get no sensory picture of the terraces before the box at 05:562 shows them being
destroyed. **Fix:** write 35–50-word boxes for B5 and B8 at least, using only details already
printed (three terraces, lanterns, the iron river gate, couples and conspirators; the study's
great table and work-slate).

**P2-4. Read-aloud slips.**
- 04:231–232 decides an action: "where you brush them" (R5).
- 04:255–256 is vague and abstract: "quiet in the particular way of a room that…" (R6).
- 04:1343–1344 editorializes inside the box: "and that is the point of the hour" (R7).
- 05:1069–1072, the epilogue, assigns the characters' dreams ("each of you dreams of dancing").
  CoS-style epilogues do narrate outcomes, but this line decides an inner experience. It is
  acceptable as the book's closing image. Consider softening it to "and some of you, on quiet
  nights, will dream of dancing" so that the players keep the choice. Also 05:1065–1066 "a
  something-to-say" reads as a typo (R20).

**P2-5. Hedged or blank-cheque phrasing in DM prose.** This is rare in the book, but present:
06 "larger at your discretion" (Rewards, the Church's favor) gives no default. Per C-V9,
pair it with a default ("one favor; double it if the character also brought back X").

### P3: polish

- **P3-1. "The way X" similes** (0.5 per 1,000 words, about 4x the references), clustered in 04
  and 07: "the way a man watches weather" (04:1017), "the way a forest does" (04:1220), "the way
  he listens to everything" (04:827), "the way sailors respect weather" (07:662), "the way other
  men pocket coins" (07:148). Keep the two best and convert the rest to plain statements.
- **P3-2. "Not running, arriving"** (05:149, 05:565, 07:550–551). The image is good. Three uses
  make it a formula, so keep it in the read-aloud at 05:564–565 only.
- **P3-3. Cross-chapter verbatim flourishes** (see the tic table). When a reference chapter
  repeats a fact, repeat the fact and drop the flourish. 07 is a lookup chapter, so its entries
  should be plainer than 04's scene prose, not identical to it.
- **P3-4. Player Handout 1** (08:303–307) repeats "revelry" and "look forward" within one
  sentence. The text is marked *canonical*, so do not change it. Ask the owner whether the
  repetition is intended as Raunu's out-of-practice formality. If it is, a DM note saying so
  would stop editors from "fixing" it.
- **P3-5. Captain's roleplaying line** (07:752) "it shows in both directions" is unclear about
  what the two directions are (R21).
- **P3-6. DC ladder tier names.** 01:252–262 names tiers "Standard" (13–15) and "Hard" (18–20),
  while the SRD's labels are Medium 15 and Hard 20. The book explains the split, which is
  honest, but the ladder table is also the one place a DC range appears, and the voice research
  notes that official text never prints one. Every check in the body prints a single DC, so this
  is cosmetic.

---

## Before → after: the worst passages

Light touch throughout: same facts, same voice, fewer tics. No new canon. Line numbers are
from the files as they stand on `feat/lean-facets` at `b254fb0`.

**R1. 01:459–464 (designer meta plus kicker)**
> *Before:* It is not the whole truth. Where the module says "the module does not say", that is a
> load-bearing sentence, not a gap. Raunu's missing year, the full nature of the Uninvited's
> distant master and of what serves him, what the child will one day become: these are mysteries
> the adventure keeps on purpose. Resist the urge to invent answers at the table. The honest
> version of this night is the one where even the survivors die not knowing.
>
> *After:* It is not the whole truth. Where the text says "the module does not say", the answer
> is withheld on purpose: Raunu's missing year, the full nature of the Uninvited's distant master
> and of what serves him, and what the child will one day become. Don't invent answers for them at
> the table. Nobody in the world ever learns them, the survivors included.

**R2. 01:469–471 (purple closer)**
> *Before:* A spell that would reach one of those answers gets rumor, contradiction, and the cold
> satisfaction of standing at the edge of something vast, which is what the world gives everybody
> else.
>
> *After:* A spell that would reach one of those answers gets rumor and contradiction, which is
> what the world gives everybody else.

**R3. 04:62–65 (double colon)**
> *Before:* They do not fight to hurt: they detain and expel, and every blow they land is a
> knockout blow: a creature they reduce to 0 Hit Points is Unconscious and Stable, never dying.
>
> *After:* They fight to detain and expel, never to hurt. A creature they reduce to 0 Hit Points
> is Unconscious and Stable, never dying.

**R4. 04:112–116 (double colon around a parenthesis)**
> *Before:* Raunu will not fight a guest: on his turn he releases a ward (see chapter X, "If It
> Comes to It"): a wall of crystal between him and the blade, the honor guard in the room the round
> after (S4), and Raunu gone by a door the attacker cannot follow.
>
> *After:* Raunu will not fight a guest. On his turn he releases a ward (see chapter X, "If It
> Comes to It") that raises a wall of crystal between him and the blade. The honor guard is in the
> room the round after (S4), and Raunu is gone by a door the attacker cannot follow.

**R5. 04:231–233 (read-aloud decides an action)**
> *Before:* The walls give off a faint warmth where you brush them, like stone that has been in sun
> all day.
>
> *After:* The walls give off a faint warmth, like stone that has been in sun all day.

**R6. 04:255–256 (vague read-aloud)**
> *Before:* The room is quiet in the particular way of a room that a great many people are
> deliberately not entering.
>
> *After:* Guests slow as they pass the doorway, look in, and keep walking.

**R7. 04:1343–1345 (editorial in the box)**
> *Before:* All around you the spirit-faces turn — you cannot tell who anyone is, and neither can
> they, and that is the point of the hour.
>
> *After:* All around you the spirit-faces turn. You cannot tell who anyone is, and nobody can tell
> who you are.

**R8. 04:363–364 (throat-clearing before the payoff; keep the payoff)**
> *Before:* And, telling its whole story without a word: her traveling pack.
>
> *After:* And her traveling pack.
>
> *(Leave the rest of the bullet, including "She stopped being ready to go home.", as it is. That
> closer is load-bearing.)*

**R9. 04:739–741 (two stacked reframes plus an abstract-noun kicker)**
> *Before:* The staff weren't victims; they were evacuated, with a thoroughness that reads as love
> expressed as logistics. The silent palace hid no crime: it was clearing the decks.
>
> *After:* The staff weren't victims. They were evacuated, every one of them placed with the care
> Corval just recited. The silent palace hid no crime; Raunu was clearing the decks.

**R10. 04:840–842 (jargon chain plus kicker)**
> *Before:* At midnight: everything. Fracture ammunition (see chapter V) is this thread's
> currency; characters who walked it enter the Longest Night armed, positioned, and, rarest of all
> at Oraga, unsurprised.
>
> *After:* At midnight: everything this trail turned up counts as Fracture tells (see chapter V,
> "The Fractures"). Characters who walked it start the Longest Night already armed and in
> position, and they are the only guests in the palace who are not surprised.

**R11. 04:1376–1377 (jargon plus kicker)**
> *Before:* It is sorrow ammunition, and it will follow them home either way.
>
> *After:* It counts as a tell for the Wept's Fracture (chapter V), and the epilogue gives it back
> to them.

**R12. 05:1109–1111 (double colon)**
> *Before:* The darkest branch, and it never happens by default: only a player character's choice
> opens it: someone stops the boat, holds Veier back from it, …
>
> *After:* The darkest branch. It never happens by default; only a player character's choice opens
> it. Someone stops the boat, holds Veier back from it, …

**R13. 05:568–570 (self-commentary plus chiasmus)**
> *Before:* This is the crescendo, and its rule is simple: the characters are caught between two
> people the mortal world has no answer for, and they cannot beat either one. What they can do is
> everything else, and everything else is what decides it.
>
> *After:* The characters are caught between two people the mortal world has no answer for, and
> they cannot beat either one. Everything else they do here, from carrying Veier to holding the
> gate, decides how it ends.

**R14. 05:727–730 (meta plus em-dash aside)**
> *Before:* The point is the seams. Each of the three is still a person — that is the terrible
> engine of them — and a character who has paid attention can reach the person.
>
> *After:* Each of the three is still a person, though, and a character who has paid attention can
> reach that person.

**R15. 05:718–721 (designer voice)**
> *Before:* Never, ever lower the numbers behind the table's back so that one of them dies. A table
> that kills an Uninvited through a fudge has won nothing. It has learned that the adventure's spine
> was negotiable, and every other promise the night made goes soft with it.
>
> *After:* Never lower the numbers behind the table's back so that one of them dies. A table that
> kills an Uninvited through a fudge learns that every limit tonight can be fudged, and nothing
> else the night promises will hold.

**R16. 05:806–807 (kicker pair)**
> *Before:* Guilt is slow, and slow is hallways. The margin at the river gate is meant to be made of
> this.
>
> *After:* Every turn his guilt costs him is a hallway for Veier, and those turns add up at the
> river gate.

**R17. 05:980–989 (designer leak in a DM Note)**
> *Before:* …and that collision is **deliberate**. A table that notices will suspect the pale
> factor of hiring the company. Let them. The aftermath is where it comes apart: … Write the herring
> so it can be untangled. Never confirm it. … Every one of them will suggest a rival by morning.
> That is the aftermath's weather, not an answer.
>
> *After:* …A table that notices will suspect the pale factor of hiring the company. Let them. The
> suspicion comes apart in the aftermath: … Never confirm who paid. … Every one of them will
> suggest a rival by morning, and none of those accusations is the answer.

**R18. 05:1041–1042 and 05:944–946 (two kickers)**
> *Before:* The Bought's hours are over. The night is.
>
> *After:* The Bought's contract ends, and so does the night.
>
> *Before:* (That is all this adventure says about the other attacks. Diversions, of course. By
> whom is the same answer as everything else tonight.)
>
> *After:* (That is all this adventure says about the other attacks. They were diversions, and who
> ordered them is one of the questions the module does not answer.)

**R19. 07:418–420 (an NPC with no voice; method, not canon)**
> *Before:* **Roleplaying Draunel:** the anti-Raunu: polished, obvious, ambitious in the standard
> noble key. Useful to the table as a patron, a foil, and by dawn the loudest voice insisting
> Vorlain hang for this.
>
> *After (suggested; owner to approve the quote):* **Roleplaying Draunel:** polished and obvious,
> everything Raunu is not. He never says the word "seat" aloud, because he fears being seen wanting
> it, and he talks instead about Vorlain's year as if it were a kindness someone should repay. By
> dawn he is the loudest voice insisting Vorlain hang for this.
> **Quote:** "Vorlain ran the house for a year, and ran it well. I only wonder whether he misses
> it. You might ask him. Kindly."
>
> *(Every fact here is already in 07:413–429 and Agenda 3. Use the same method for Kovaun, Callun,
> Essin, Maiven, Anha, Tavva and the Bought officers: one habit and one line, built from their
> printed Wants and Secret.)*

**R20. 05:1065–1066 (reads as a typo)**
> *Before:* …and a something-to-say, two years in the keeping, that no one will ever hear.
>
> *After:* …and a sentence two years in the keeping that no one will ever hear.

**R21. 07:752 (unclear image)**
> *Before:* **Roleplaying the Captain:** a man of business who has been shot at, and it shows in both
> directions.
>
> *After:* **Roleplaying the Captain:** a man of business who has been shot at often enough that
> nothing tonight hurries him.

**R22. 01:399–402 (jargon before definition; pairs with P1-3)**
> *Before:* The Uninvited cannot be beaten, by design. Cleverness buys Delay, Delay buys hallways
> and lives, and Fractures change outcomes.
>
> *After:* The Uninvited cannot be beaten. Cleverness slows them down (Delay, chapter V), every turn
> they lose is a hallway or a life, and reaching the person inside the mask (a Fracture, chapter V)
> can change outcomes.

---

## Tone and identity: a short note

"Glamour over a blade" shows in the read-aloud and the NPC dialogue: warm, wry, faintly
uneasy until midnight, then clipped. 01:428–429 tells the DM to change register at the
Unmasking ("Shorter sentences. Fewer adjectives."), and the read-aloud obeys. The DM prose does
not need that rule, but it has caught it: across the whole book, not just after midnight, it
keeps closing on solemn short sentences. Before midnight that pulls it toward an elegiac,
aphoristic register that fights the party tone the chapter asks for. Rule of thumb for the
polish pass: **the DM prose should be the calmest voice in the book.** Mood belongs to the boxes
and the NPCs (C-V7). The humor is the right kind and should stay: deadpan, informational, never
at the players' expense.

## Jargon: what a DM must hold

About 40 invented terms or term-uses: Movement, omen, agenda, hook, Undercurrent (spark /
trail / find / at midnight), approach loop, snake, threat line, tell, heat 0–4, Snake Tracker,
night-tracker, DM sheet, fight card (Wants / Tells / Breaks / Nastier, outs, clock), the
Uninvited (Wept, Radiant, Hollow), Delay, lump, Fracture, Fracture tell, Leashed, Witnessed,
Held by Something Else, Shadow-Step, the leash, Down Not Out, the crowd rule, Room Tricks,
ward-point, ward-literate, steering, the Attendant (Idle / Focused / broken focus), beats
versus rounds, the Crossing, crossfire, the Midnight Clock, crystal charges (five named), gift,
Heritage, knack, the Bought, the Second Clause, fire clock, bell clock, iron, success at a cost,
and the DC ladder tiers. LMoP introduces essentially no bespoke mechanics. CoS adds the card
reading and a few location terms. Much of the module's load is earned, because it is what makes
a 5e table able to run an unbeatable antagonist. The DM sheet carries most of it. The failure is
order and overload, not count: see P1-3 and P2-1.
