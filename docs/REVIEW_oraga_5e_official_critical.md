# REVIEW: Oraga Night 5e, a critical pass after the official-module fix pass

*2026-10-06. Adversarial review of `conversions/dnd5e/oraga_night/` at `e95d326` plus
the working tree. I read every chapter as three readers: a DM prepping it for Friday night,
a rules lawyer, and a publisher's editor. Nothing in the module was edited. Paths below
are relative to that folder unless they say otherwise. Line numbers are from today's files.*

**Limits of this review.**
- The official reference extracts the brief named (`…/scratchpad/refs/`) **do not exist**
  in this session's scratchpad (the directory is missing). So the comparisons with
  LMoP/CoS/DMG layout and voice come from general knowledge of those books, and **no
  copyright text-diff against the official books was possible.** The copyright section says what
  was checked instead.
- The source Facets edition (`adventures/oraga_night/`) was used to decide which defects are
  inherited canon and which the 5e passes introduced.

**Tool runs (necessary, not sufficient).**
- `python tools/lint_5e.py --check`: OK, 0 hard and 0 structure hits.
- `bestiary_check.py`: 25 blocks + 3 Nastier lines, 0 mismatches.
- `pregen_check.py`: 5 pregens, 0 issues.
- I hand-checked every stat block's HP and hit-dice arithmetic, attack and DC maths, AC, the
  Initiative scores, and every pregen's array, HP, skills, slot and prepared counts. All of it
  is correct. The defects below are the kind those tools cannot see.

---

## 0. Verdict

**6.5 / 10.** This is a rich, unusually well-engineered adventure. The social sandbox, the
agendas, the snakes, Delay and Fractures, and the "Down, Not Out" mercy are genuinely good
5e design. The stat-block and pregen arithmetic is now clean, and that is rare. But it does
not yet read, look or hold together like a WotC book:

- **Continuity is not under control.** Several numbers and positions contradict each other
  across chapters: the household count, where the nine guards are, which floor the east wing
  is on, and when the Attendant and the Uninvited arrive. Some of these were made *worse* by
  Phase 8.
- **The boss card has a one-roll exploit.** S14's "Argue its orders" out ends the night's
  hardest fight with a single DC 13 check, and the bestiary contradicts the card on it.
- **Development scaffolding is printed in the book**: simulation tables with Monte Carlo
  percentages, repo file names, an HTML review comment, and "plays Low in simulation" notes.
- **There are no maps.** A WotC adventure without cartography does not look official,
  however good the text is. An ASCII box diagram is not a map.
- **The prose is competent but templated and repetitive.** The same NPC dossier appears in
  three chapters. The same rule is restated in up to five places, and the restatements have
  started to drift. Verbal tics recur dozens of times ("exactly" ×51, "the whole" ×44,
  "quietly" ×30, "to everyone's permanent confusion including his own" ×5).

**Counts:** P0 **0** · P1 **7** · P2 **24** · P3 **24**.

**What gets it to 9:**
1. One continuity bible (numbers, geography, who is where at midnight), reconciled and
   enforced by a fact checker, plus owner rulings on the canon conflicts.
2. Real maps of B2/B3, B5, B9, the B12 gate, and a whole-palace overview.
3. Fix S14's outs and make the bestiary agree with the card.
4. Strip every simulation, tooling and review artefact from the book text.
5. Make every rule live in one place, with only page references elsewhere.
6. A human line-edit for tics, redundancy and the over-split sentences.
7. One house format for trigger lines and boxes.

---

## 1. P0: blockers

None. Every scene can be run from the page, nothing in it is a legal blocker, and the SRD
5.2.1 attribution is present and correctly worded (README:111–114, 09:8–11, 10:7–10,
11:9–12).

---

## 2. P1: real defects

### P1-1. The household arithmetic contradicts itself, and the book invites the reader to do the sum
- 02:70: "The palace staff is cut **four-fold**."
- 04:705: "*The household was **sixty**. Two years ago it was cut four-fold…*"
- 07:225–229 (Corval): "There used to be sixty of you." / "**Twenty-two.**"
- 04:408 (B13): "the room where **twenty-two** people's effects are stacked."
- 07:196: "runs the whole ball with **two dozen** staff."
- 04:38–39: "A palace this size should hold **a hundred** servants; tonight… **about two dozen**."
- Sixty cut four-fold is 15, not 22. Undercurrent B literally offers "simple arithmetic by any
  guest who has run a household" as its spark (04:709–710), so a player *will* do this sum at
  the table.
- In the source, 80 left and 22 stayed, which is consistent with "should hold a hundred" and
  "four-fold". The owner's ruling Q20a (60) was applied to Undercurrent B only, and O31 hid
  the derived 45 without noticing that 22 and "four-fold" are both still printed.
- **Fix:** this is canon, so escalate to the owner with the three options. (a) Sixty, with 22
  staying: drop "four-fold" from 02:70, 04:705 and 02:422, and say "cut by two-thirds". (b) Sixty,
  cut four-fold: Corval says "Fifteen", and B13 and 07:196 follow. (c) A hundred, with eighty
  let go: revert Q20a. Then add the household figure to a fact sheet the linter checks.

### P1-2. The nine honor guards are in places that cannot all be true, at the climax most of all
- The text fixes the number at nine (04:877–878, 10:421 "There are nine") and sends all nine to
  the dais at midnight: 04:83 "**the nine go to the dais and stay there**"; 08:43; 05:461 "The
  nine Boranis Honor Guards… die or fall protecting their chief"; 05:817–818 "**the only guards
  left are dying on the dais**".
- Yet the same minutes need guards elsewhere:
  - 05:149–150: the Radiant's "first sign is **the guards' lanterns going dark along the
    gallery**".
  - Table V–1 (05:268): "**a guard at the doors**".
  - Table V–4 (05:336): "Bring **the guards off the east wing doors**".
  - Undercurrent C promises "its inner guards by name" (04:774).
- Before midnight it is just as incoherent:
  - All nine stand on the gate in Movement I (04:169–170), yet steel drawn there brings only
    "two guards" (04:98–99, S4).
  - B9's doors have "more guards on them than the rest of the palace is using put together"
    (04:344).
  - B7 is where "the few real guards concentrate" (04:305).
  - Corval *doubles* the east-wing guard in Movement V (04:1347).
- A DM running the Radiant's hunt cannot say who is at the east-wing doors, and a rules lawyer
  will ask why two guards answer a drawn blade with nine standing beside it.
- **Fix:** write one deployment table in chapter VIII (Movements I–V and midnight) that says
  where each of the nine stands and who guards the east wing at midnight. Either say "the east
  wing has its own household guard, not counted in the nine" (that is new canon, so ask the
  owner), or keep two of the nine at B9 and change "the nine go to the dais" to "seven". Make
  S4's "two guards" explicitly "the two nearest".

### P1-3. S14: one DC 13 check beats the night's boss and pays 3,900 XP, and the bestiary disagrees
- 09:1921–1925 lists "**Argue its orders**" as an out: an Intelligence (Investigation) or
  Charisma (Persuasion) check "against the distraction DC".
- 09:1931–1932 pays the full 3,900 XP "when… its orders are argued away".
- The card always fires with the Attendant **Idle** (09:1798), so the distraction DC is
  **13**. The first character to act makes one DC 13 Persuasion check (with the +2 for playing it
  out) and the "hardest fight of the night" is over.
- The bestiary says the opposite. 10:293–295 calls the same argument "**a distraction like any
  other**", which would count only while Focused and only as one of four.
- The card never says what a successful argument does: whether the Attendant ignores that one
  character, or leaves.
- **Fix:** make arguing a *distraction* (the bestiary's version). A success while Focused breaks
  its focus and counts toward the four; a success while Idle makes that one character
  "furniture" for the scene. Delete it from the Rewards trigger list, and make 05:412–417,
  07:645–647, 08:73–81 and 10:228–243 agree.

### P1-4. The Attendant and the Uninvited arrive at contradictory times
- 01:62–64: "at midnight something **comes through with the Uninvited**… built to be the
  hardest fight". Elsewhere the Attendant is at the ball from Movement I (04:856–861; 07:602
  "It came in with the early guests").
- The Uninvited arrive "with the **Movement III** crush" (07:574; 04:1075). But Table V–6 gives
  the Hollow tells in "**any Movement**" and "(B10 edges, **Mv II–V**)" (05:753). That
  contradicts both the arrival time and the line that tells are "salted through Movements
  III–V" (05:714, 10:154). A DM following Table V–6 shows a tell from a guest who has not
  arrived yet.
- **Fix:**
  - 01:63: "and something that came with them, at the ball all evening".
  - Table V–6, Hollow: "(B10 edges, Mv III–V)" and "(any Movement from III)".

### P1-5. The east wing's floor and the gardens' layout don't hold together after O28
- O28 gives a level "cleared corridor, 10 feet wide and about 60 feet long, from the Court's
  east doors to the wing's double doors" (05:440–443).
- Other passages put the wing upstairs:
  - S10: "one lit window **on the second floor**", a 20-foot wall (09:1434, 09:1465).
  - Maiven "comes down **the service stair** from the east wing doors" (09:1454–1455).
  - The wing's corridor "booms shut somewhere **above**" (05:142–143).
  - The Radiant's route runs "along the gallery" (05:149–150).
  - B8 is "second floor, dark wing" (04:314).
- No stair connects the Court to the wing anywhere in "General Features", so a DM cannot place
  the wing, the "private stair" or the "garden stair". (Are those two the same stair? 05:443,
  05:540, 08:37.)
- The terraces have the same problem:
  - S9 puts the duel "on **the upper garden terrace**" (09:1323), but its box has the crowd "at
    the rail of the upper terrace, looking down… **On the grass below them**" (09:1331–1333),
    which is the next terrace down.
  - "**Two terraces below**… a tall pale factor at the river gate" (04:1391; 09:1355). O28 puts
    the gate 150 feet past the lowest terrace (05:436–439), not two terraces down.
- **Fix:**
  - Add an *Elevations* bullet to 05 "General Features": the Court is at ground level, the
    galleries 12 feet up, and the east doors open on a stair or a gallery-level corridor.
    Choose one, then fix 05:142, 05:149 and S10 to match.
  - Name the private stair as *the* garden stair, or say how they differ.
  - Fix S9's box to "On the upper terrace below the Court's garden doors…", or move the duel.
  - Replace "two terraces below" with "down at the river gate".

### P1-6. No cartography
- The only map is a not-to-scale ASCII diagram (08:141–172) that places five of the
  thirteen rooms in a list below it instead (08:174–185). Every fight card depends on spaces
  the DM cannot see: S3's gate, wicket and gate-walk; S1's gallery rail; S7's 5-foot run; S9's
  terraces; the B9 corridor.
- An official adventure always has keyed maps, and this one also promises "the palace diagram"
  as one of the three things you run from (01:5–7, 01:94–96).
- **Fix:** commission or draft four maps (B1/B12 gate, B2/B3 Court and galleries, B5
  terraces to the river gate, and B9 with B10's service run) at the O28 sizes, plus a whole-palace
  key. Until then, call 08's figure a "flowchart", not "the palace, keyed".

### P1-7. "Nastier" is the baseline on most cards, so roster lines contradict the cards
- The legend defines **Nastier** as "how to make it harder" (01:140–141; 10:28–30). Yet the
  default rosters *are* the Nastier lines:
  - S3's sergeant is "the veteran of the block's **Nastier** line" (09:810).
  - S6's cousins are the Nastier ones (09:1044).
  - S7's fourth knife (09:1143–1145).
  - S8's fourth warden (09:1248–1250).
  - S9's lead duelist (09:1360).
- The flavor lines then contradict the cards. 10:656 says "*Kovaun **brought three**. Card:
  S8*", and S8 fields four. 09:170 says the Circle brought three, and S7 fields four. Table X–1
  lists the "Bought Sergeant (**CR 2**)" (10:75), but S3's budget uses CR 4 (09:814).
- A DM building from chapter X gets the wrong fight, and "make it harder" has nowhere left to
  go on those cards.
- **Fix:** promote the used variants to their own blocks (*Veteran Bought Sergeant*, CR 4;
  *Cousin of 3160*, CR 1) or make them the base blocks. Change the faction sizes to match ("the
  Circle brought four"; Kovaun four, which needs the owner to confirm INVENTIONS #1). Give each
  card a real Nastier dial again.

---

## 3. P2: off-standard

**Development artefacts in print**
- **P2-1. Simulation data printed as DM Notes.**
  - S14's table of Monte Carlo outcomes ("Simulated, 5,000 fights a row…", 09:1823–1845).
  - "A character drops in about one fight in twenty" (09:694–695); likewise 09:824–825,
    09:1151–1152, 09:1365–1366 and 09:1700–1701.
  - "one run in twenty to one in four" (09:106–108).
  - "how the fight played in simulation" (09:140–141).
  - No WotC book prints design-validation data. **Fix:** keep one sentence per card ("Expect
    one character to drop") and move the numbers to `research/`.
- **P2-2. Repo file names in the book.** "chapter IX, *The Snakes* (`09_The_Snakes.md`)… the
  Bestiary (`10_Bestiary.md`)" (04:22–23). **Fix:** delete the parentheticals; the README is the
  only place for file names.
- **P2-3. A leftover review comment.** `<!-- INVENTIONS #11: the three other irons below are
  inventions, for the owner's review. -->` (09:268). It shows in any non-HTML export and in
  source. **Fix:** delete it; the ledger already records it.
- **P2-4. Conversion talk the style sheet bans.**
  - README:42–46: "This is the fifth-edition conversion of the Facets of Origin module…"
  - 03:82–87: "Sidebar — for players who know the Facets edition… the old domains".
  - 01:35 points the DM's prep box at "*Inventions*", a contributor file.
  - The linter's conversion-talk regex only matches "the source / the original / this edition",
    so it misses all three. **Fix:** cut the sidebar, cut the README paragraph's first sentence,
    and drop *Inventions* from the prep box.

**Continuity and canon**
- **P2-5. Maiven is alive in the aftermath, though she dies by default.** 06:43: "Maiven
  Nolonaire will not leave the city without her cousin or a body", printed as "the record".
  By default she dies (05:860; 08:46; 07:480). **Fix:** "If Maiven lived, she will not leave…;
  if not, the delegation takes her home."
- **P2-6. "Forty blades" against a company of twenty-one.** 05:1173 and 05:1178 ("forty blades",
  "forty sworn witnesses") contradict 05:936 (sixteen Blades, four sergeants, a captain). This is
  inherited from the source, but still wrong. **Fix:** "twenty blades"; it is canon-adjacent, so
  tell the owner.
- **P2-7. Vell "before midnight".** "No party… drops him **before midnight**" (10:25–26;
  10:1918–1919; 07:563–564). The only time a party fights him is the Crossing, after midnight.
  05:636 already says "before the boat clears". **Fix:** use that wording everywhere.
- **P2-8. Undefined peoples.** "A **Scora** reads the figure without a check" (04:677) is a
  rule that keys on a people the 5e book never defines (INVENTIONS #25 admits the definition was
  cut). "A **Kshalo** dreamed him away" (08:256) has the same problem. **Fix:** gloss both in one
  clause, as Q17 did for Mazaa and the Blackwatch, or replace "A Scora" with "a character
  trained in…".
- **P2-9. Two inherited contradictions in read-aloud.**
  - B2's box says "**It has been dark for hours**" (04:233), but Movement I is "*(dusk)*" and the
    B0 box has the walls "holding the last of the day" (04:144–145, 04:843).
  - B4 is "**A smaller crystal chamber**" (04:252), but the Movement III box says "The hall is
    **bigger than it needs to be**… vast, bare hall" (04:1012, 04:1023).
  - These are descriptions, not canon facts. **Fix:** "It is not long dark"; pick one size.
- **P2-10. The S4 outs override B9.** B9: "Nobody gets through them on a single check. The ways
  in are…" (04:350–352). S4's first out: "An invitation and a good story: a DC 15 Charisma
  (Deception or Persuasion) check" (09:936), with the objective "get through" (09:927). **Fix:**
  say the out ends the fight, not the door ("an escort back, no expulsion").
- **P2-11. "The Bought change sides" can't be reached.** The branch asks for the company "in the
  trade district **at dusk**" (05:1163–1167), but play starts in the street at dusk and nothing
  is played before it (01:51–54, 01:211). **Fix:** give the route an in-palace door (a
  sergeant's runner at the gate in Movement V), or mark it as a campaign-prep branch.
- **P2-12. The Snake Tracker's "second card" list names a trigger that doesn't exist.**
  "A second goes live only if the table saw a line and let it go (S8's tell, **the Circle's
  coat**, the appointment…)" (09:498–499). Seeing the coat is not a Rises item for the Circle
  (09:487; 08:202). **Fix:** "Callun's coin refused", or add the coat to Rises.
- **P2-13. The README's licensing claims are inaccurate.**
  - README:125–126: "Every stat block is an original creature… **none is copied from the
    SRD**." The Sect Guard is "**Built on the SRD guard**" (10:1543), with the SRD Guard's AC,
    HP and scores, and "A guest" is the SRD commoner (10:1886–1887). CC BY permits this, but
    the sentence is false.
  - README:135–136: the canon "appear[s] here **by that author's hand**", yet the 5e text carries
    82 ledgered inventions.
  - **Fix:** "Most stat blocks are original; the Sect Guard adapts the SRD Guard"; and "the
    setting's canon belongs to its author; inventions are listed in INVENTIONS_5e.md."

**Rules**
- **P2-14. A grapple priced as a DC 13 check.** Table V–5 row 6, "Hold him in the shallows…
  An Unarmed Strike (Grapple)" (05:354), sits under the header "Check (DC 13; DC 15 the second
  time)". In 5.2.1 the *target* makes the save against the grappler's DC, and the Radiant has
  Dex +9 and *Centuries of Practice*. **Fix:** "succeeds if he fails the save; the grapple's 1
  Delay is the trick".
- **P2-15. S14's hint 5 overrides the Focus rule.** "If nobody has tried by the third round,
  one of the Uninvited… [calls it] back to Focused" (09:1898–1901). Focus is mechanical (a
  member of the three with no Delay, 10:213–216). **Fix:** "…when one of the three next has no
  Delay, show that glance big."
- **P2-16. The Attendant's out-slug claim is false by the book's own numbers.** 10:22–24 says
  it is "built to be more than a party can out-slug". S14's table says an optimized party that
  "only trades blows" wins 80% (09:1832). **Fix:** "more than *these* pregens can out-slug", or
  drop the claim.
- **P2-17. S3's ending 1 contradicts itself.** The Second Clause makes "the company stop holding
  the gate and start looking for a woman in Thenya wool" (09:858–860; 10:503–507). The next
  sentence has the captain still fighting and "negotiating, out loud, while his attacks
  continue" (09:860–862). Who holds the wicket after the clause? **Fix:** the clause pulls the
  Blades back to watch the crowd for Thenya wool and the gate is open; the captain fights on
  only if the party blocks the search.
- **P2-18. "Down, Not Out" is restated five times, and the copies drift.** Copies in 05:199–230,
  08:62–67, 09:564–574, 09:1704–1710 and 10:43–48. S13 says the crowd rule rouses a creature
  "at the start of **the round after next**" (09:1709–1710). 05:210–213 says "the round after".
  This is how the combat-sim divergence happened in the main project. **Fix:** keep the full
  rule once (05) and reduce every other copy to "Down, Not Out (chapter V)" plus anything
  local.
- **P2-19. The 2014 claim overreaches.** 10:52–54 says "everything else reads the same" at a
  2014 table. But the blocks use Emanation, Utilize, the Magic action, Bloodied, Study and
  Influence, and the condition line format, none of which a 2014 DMG has. The cards also rate
  nearly every fight *Deadly* by the 2014 multiplier (S3: 1,500 × 2 = 3,000; S14 is nearly twice
  Deadly). The DM Note at 09:136–141 says so, but the README's "playable at a 2014 table"
  (README:16–17) undersells the work. **Fix:** a ten-line "At a 2014 table" glossary box in
  chapter X.

**Layout, voice and style**
- **P2-20. Three trigger-line styles.** STYLE says "a plain trigger line". The book uses italic
  (04:139 "*Read to open the session:*", 04:856), bold (04:228, 04:250, 04:863, 05:120,
  05:545), and bold-italic in every card (09:583 "***Trigger — read when…***"). The linter's
  `readaloud_trigger` rule only checks that a trigger exists. **Fix:** one format, enforced.
- **P2-21. Three box-label styles.**
  - Heading style: "**Sidebar — title**" on its own line (03:82).
  - Run-in with a colon: "**Sidebar — Steel at the ball:** the Orthaen…" (04:206, 04:554,
    05:178, 05:616).
  - Run-in with a period: "**Sidebar — Snakes at the feud.**" (04:518); "**DM Note — what
    you must not say.** The factor…" (05:952); also 07:765.
  - **Fix:** the heading style everywhere.
- **P2-22. NPC dossiers repeated three times.** Callun's want, fear and secret appear nearly
  word for word in 07:356–361, 09:162–168 and 10:1492–1498. The same goes for Kovaun (07, 09:212–216,
  10), Draunel, Essin, Corro and Maiven. "The fight aimed at the noble-minded… nothing at stake
  but property and decency" appears four times (04:528–529, 05:521–522, 07:698–699, 09:463–464,
  09:978). **Fix:** chapter IX should point to VII ("see chapter VII") and add only the threat
  line. That cuts several pages.
- **P2-23. Verbal tics and a templated cadence.** Counts across the chapters:
  - "exactly" ×51, "the whole" ×44, "quietly" ×30, "out loud" ×24, "genuinely" ×15, "Say so"
    ×14.
  - "to everyone's permanent confusion including his own" ×5.
  - "not X… but Y" constructions ×20.
  - Every DM Note runs **Default / The dial / The cost** (04:178–191, 05:687–704, 05:871–883,
    09:71–79, 09:514–523).
  - Over-split sentences left by the prose pass: "It leads nowhere. / It is the moment…"
    (06:96–97); "The doors close. One heartbeat." (04:1186).
  - These violate the house rule that prose must read human. **Fix:** a human line-edit with
    a tic list; vary the DM Note form.
- **P2-24. Italics used for emphasis.** STYLE bans emphasis italics, but they remain: "*at a
  cost*" (04:180, 04:189), "*steer*" (04:398, 05:35), "Andra *is* her research" (11:205), "how it
  *shows itself*" (03:62). Italicized "*Heroic Inspiration*" appears on every card's Rewards
  line (09:640 and others), and that is a rules term, not a spell or item. The linter has no
  emphasis rule.

---

## 4. P3: polish

1. The README and 01 line endings are inconsistent: README:14 and :20 lack a final period; 01:130–132's
   blank line splits the box list into two lists.
2. DC-ladder vocabulary: "Standard 13–15" (01:257) where SRD 5.2.1 says Medium 15. It is a house
   choice, but say so once.
3. "Wisdom (Insight or Perception)", "Charisma (Persuasion or Intimidation)" and similar
   compressions appear 9 times in body text (03:181–183, 09:627–628, 09:1397, 09:936). STYLE
   spells alternatives out; the linter misses the form.
4. 01:116 says "Nothing else in the module carries an enemy's numbers", but cards print Passive
   Perceptions (09:676, 09:1124, 09:1228, 09:1441), the Attendant's "229 Hit Points and AC 17"
   (09:1926), and "A guest: AC 10, 4 HP" (05:365). Soften the claim.
5. Raunu's Unmasking rite (05:110–118) is a plain blockquote, not italic like every other
   read-aloud (compare the toast, 04:1168–1184).
6. "*If you have time*" is bold in the legend (01:145) and italic in the text (01:205, 04:20,
   04:391).
7. "Intimidation never **works**" (05:730; 10:160) vs "Intimidation never **adds**" (05:796).
8. The Wept's Fracture "needs ammunition… **or** 2 Delay banked" (10:1819–1820), against
   "Invoking a Fracture takes at least one witnessed tell" (05:723).
9. Three near-identical seal items, *A Sealed Door*, *House Seal* and *Door-Seal*, plus the
   guard's "*Seal*" (10:398, 10:2013–2021). Readers will confuse them.
10. Stat-block nits:
    - "*Hit:* 3 (1 + 2)" (10:335); 5.2.1 writes a flat value.
    - "**Speed** 30 ft., and some other way" (10:1900) and "**Languages** Common, two
      centuries out of fashion" (10:1067) are commentary in data fields, which STYLE forbids.
    - "Bright light" is lowercase (10:401).
    - A narrative paragraph sits inside Vell's block, before Traits (10:1916–1922).
    - "**Fracture — …**" headers sit outside any 5.2.1 section.
    - "*Dominate*" is not a spell name (10:124).
11. Vell's blade is a "broadsword" (07:505; 10:1938) and a "greatsword" (07:513).
12. 07:697 gives Tavva a "**Gallery Knife** for her crew of four"; there are three knives, and
    Tavva makes four (10:1043).
13. Pregen tools: "gaming set" is lowercase (11:73, 11:302) against O16's Title Case ("Gaming
    Set" is in SRD 5.2.1). "vehicles (land)" (11:147, 11:151) is not a 5.2.1 tool, so a 5.2.1
    background cannot grant it.
14. Andra's *Mage Armor* "lasts the night" (11:213). It lasts 8 hours, and the night runs dusk to
    dawn. Say "cast at dusk; it lasts past midnight".
15. S3 says "nobody on the party's side can Hide" in Bright Light (09:830), but 5.2.1 Hide
    works behind Three-Quarters Cover in any light. The gate-walk is "15 feet above the arch"
    (09:781), but a shove from the stair's top "falls 10 feet" (09:832).
16. Agenda card 2 promises "a favor… **of frightening size**" (08:306), while the default is
    "one favor… without scandal" (02:321–322). This is intended (O31), but add "(the patron's
    pitch)" in 02 so the DM knows the card oversells.
17. "The memo from the east" (07:296, 09:214–215): "memo" is anachronistic in a world where only
    the Church writes. "Businessperson who has been shot at" (07:750) is likewise modern.
18. "The Second Clause" is the name of the **third** task (05:943; 10:533). This is inherited;
    give the DM a one-line gloss ("the second, sealed clause of the contract's terms").
19. 05:534 has broken italics: `*(… See* "The Snakes in the Dark".*)*`.
20. 02:26 says "eastern mists" twice in one sentence (the Q17 insertion). 06:25–26's gloss is
    bolted on.
21. "*Darkness* and a patient eye make her the guest likeliest to catch a tell" (11:272–273) is
    a non sequitur.
22. 10:2044–2045: "Contract case… Chained to the sergeant's hip: a chained case".
23. Pello's line "it is all signs, knots and chalk that gets wiped" (11:173) is ungrammatical.
24. INVENTIONS is stale: #18 still says "Vell's non-block: no AC, HP or CR" and sits in
    "Review These First"; #38 still says "a 3rd-level caster". Annotate both as superseded by
    #75.

---

## 5. The three readers, briefly

**The DM on Friday night.** The prep box, the DM sheet and the Midnight Clock are excellent;
this is better DM support than most official books give. Where I got lost:
- Who guards the east wing at midnight (P1-2).
- Which floor the wing is on (P1-5).
- Whether one Persuasion check ends S14 (P1-3).
- Why chapter X says Kovaun brought three when S8 fields four (P1-7).
- What a Scora is (P2-8).
- Whether Maiven is alive in the aftermath (P2-5).
The rules are spread over 05, 08, 09 and 10 with small differences, so I had to check
four places to be sure of "Down, Not Out".

**The rules lawyer.**
- Block and pregen maths: correct throughout.
- 5.2.1 wording: Weapon Mastery, Nick, Fast Hands with charges, Divine Spark, Preserve Life and
  Cutting Words are all accurate.
- Exploitable: S14's argument out; an Idle success costs the Attendant its whole turn at DC 13,
  so one action a round locks it while Delay holds.
- Broken: grappling the Radiant under a DC 13 header.
- Questions the book leaves open: does the Prickle cancel an unseen attacker's Advantage? The
  text gives only "knows the direction", so say it doesn't. And does the Hollow resist
  ordinary shoves? *Leashed* covers only magic.
- **Vell (O29):** AC 20, 285 HP, resistance to all thirteen types, Magic Resistance and a
  per-round hit negation meet the owner's ruling. It is over-built (any two of the four layers
  would do), and the explanatory paragraph inside the block is non-standard. It is not
  exploitable.
- **The O28 sizes** are internally consistent with the 12-foot rail, the 10-foot drops, the
  10-foot doors for *A Sealed Door*, and 200 guests filling half the Court. The trouble is the
  elevations they leave out (P1-5).
- **O25–O27** hold, with one gap: the bell clock that counts only rounds at the gate means the
  last bell waits indefinitely if no character reaches the gate, and the guests stand trapped
  for an unbounded stretch of fiction. Add a default: "if no character reaches the gate by the
  end of Movement VII, the sect guard arrives and ending 3 runs offstage."

**The editor.**
- Strong: the read-aloud is genuinely good (the B0 box, the Dead Dance and the toast); it reads
  better than much official boxed text.
- Weak: the DM prose leans on tics, templates and three-fold repetition; the box and trigger
  styling is inconsistent; and the book shows its scaffolding (simulations, file names, an HTML
  comment, a contributor file in the prep box).
- In a printed book the ASCII diagram would be the first thing a reader notices.

---

## 6. Challenges to the Planner's O-decisions

- **O22, and the simulation clauses ("plays Moderate"):** keep the label-then-play idea, but the
  *play* clause should be table advice ("expect one character to drop"), not data. See P2-1.
- **O25:** sound for pacing, but it has the gap above. Add the offstage default.
- **O29:** acceptable. I recommend simplifying to AC 20, 300 HP, resistance to all damage and
  *Not Where It Landed*, and moving the "the block exists to…" paragraph to a DM Note.
- **O30:** consistent, but "Shout" (S6) and "Make enough noise to lose" (S2) also end the scene
  badly without resolving it. The test "nothing is resolved" arguably catches them too. That is
  an owner-level call; flag it, don't decide it.
- **O31:** the right instinct (print no new number), but it missed the two counts that already
  conflict with the ruling (P1-1). Escalate.
- **INVENTIONS #54 (Nastier lines as base rosters):** the decision behind P1-7. Promote the
  variants to named blocks instead.

---

## 7. Copyright

- Checked: every spell, feat, subclass and condition named is in SRD 5.2.1 (one non-name,
  "*Dominate*", P3-10). No non-SRD monster is used: every block is original apart from the Sect
  Guard and the commoner reference (P2-13).
- No WotC proper nouns, place names or product identity were found. The DMG-style
  structures (the XP budget table, the CR table) are SRD 5.2.1 content.
- **Not checked:** whether any sentence closely echoes LMoP, CoS, HotDQ and the rest, because
  the reference extracts were unavailable. Re-run this check when they are restored. The house
  voice is distinctive enough that I saw no obvious borrowing.

---

## 8. Where the tooling gives false confidence

`lint_5e.py` is a line-by-line regex linter, and the two checkers are arithmetic checkers. They
cannot see the following:
1. **Facts that must agree across chapters:** counts (60 / four-fold / 22, nine guards, forty
   blades, crew sizes, faction retinues), timelines (which Movement the Uninvited arrive in, and
   tells keyed to Movements), or geometry. Every P1 except S14 and the maps is in this class.
2. **Rules that contradict each other:** S14 against the bestiary, hint 5 against Focus, the
   drifting "Down, Not Out" copies, and the grapple-as-DC.
3. **Anything split across a line break.** A DC at a line's end with its ability on the next
   line is not paired: there are 8+ such wraps (04:243, 04:282, 04:314, 04:533, 04:599, 04:610,
   04:649, 01:496), so the bare-DC check is partly blind. Sentence metrics are also skewed by
   hard wraps.
4. **The allowlist is too broad.** It exempts a *whole line* from *every* rule on a substring
   match (`is_allowed`), so one allowed phrase hides any other defect on that line.
5. **Style it has no rule for:** italics for emphasis, compressed alternative skills ("(X or Y)"),
   the trigger-line format (it checks presence only), box-label format, HTML comments, repo file
   names in body text, simulation jargon, and conversion talk beyond three phrasings ("Facets
   edition", "old domains" and "fifth-edition conversion" all pass).
6. **Design-level problems:** exploits, what "Nastier" means, encounter play beyond XP sums, and
   whether a referenced term (Scora, Kshalo) is defined.
7. **`bestiary_check.py` deliberately skips Vell** (no CR), and **pregen_check** accepts
   expertise silently ("= expertise (OK, note)"). Both are reasonable, but they mean the blocks
   most likely to be hand-edited later are the least checked.

**Suggested tooling:**
- A `facts.yaml` (household, guards, retinues, company size, the Movement each NPC arrives in,
  elevations) with a checker that greps for numerals and words near key nouns.
- Unwrap paragraphs before applying the regex rules.
- Make allowlist entries rule-scoped.
- Add rules for emphasis italics, "(X or Y)" skills, `<!--`, `` `\d\d_.*\.md` ``, "simulat",
  "Facets edition" and the trigger format.
- A "defined terms" check: every capitalized people or term must appear in a glossary.

---

## 9. Top five, in order of what to fix first

1. **P1-3:** S14's argue-out exploit, and the bestiary contradicting the card.
2. **P1-1:** the household arithmetic (60 / four-fold / 22); needs an owner ruling.
3. **P1-2:** the honor guards' positions, especially who is at the east wing at midnight.
4. **P1-5 and P1-4:** the east wing's floor, the terrace geometry, and when the Attendant and
   the Uninvited arrive.
5. **P1-6 with P2-1/2/3:** no maps, and development artefacts printed in the book.
