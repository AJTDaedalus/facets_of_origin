# Oraga Night 5e: Logic and Sense Audit (three players, 4th level)

*2026-10-20. Veteran-editor audit of `conversions/dnd5e/oraga_night/` (clean tree at `b254fb0`)
for one question: **does it make sense**, run for three 4th-level players? I read the README,
chapters 01–09 in full, the relevant parts of 10 (the Uninvited's front matter, "If It Comes to
It", Master Vell) and 11 (the cast table and the agenda hooks), `facts.yaml`, and every label on
the five SVG maps. I read `docs/REVIEW_oraga_5e_official_critical_2.md` so I would not repeat
it. No module file was edited. Paths are relative to the module folder, and line numbers are
from today's files.*

**Tooling.** `python3 tools/fact_check.py --check` returns OK (0 problems, 0 hits). That is
expected and tells us nothing here. The checker matches phrases against `facts.yaml`, and none
of the defects below is a phrase mismatch. They are causal, spatial and motivational gaps, and
the tooling has no model of those.

---

## 0. Verdict

**"Makes sense" score: 6.5 / 10 at a three-player table** (about 7 at four).

This score is not comparable with the 8.0 in review 2. That review scored overall production
quality: rules arithmetic, layout, copyright. This one scores only coherence: motives,
information flow, causality, geometry and agency.

**What holds up, and holds up well:**
- The *social* night is coherent. Every faction has a want, a fear, a visible tell, an
  escalation and an out, and the heat tracker ties them together. Chapter IX is the best-built
  part of the book.
- The cast is logically consistent. Vorlain's "no plot" secret holds everywhere, and Corval's
  memory-slide is a clean, motivated tell. Undercurrent B (the evacuated household) is a
  mystery whose answer is fair, findable from several directions, and satisfying.
- The "you cannot beat them" spine is honest with the table. The Delay die is on the table,
  the DM is told to say the rule aloud, and the Fractures give a real non-violent lever.
  Players will not feel cheated by the Uninvited themselves.
- "Down, Not Out", the crowd rule and the morale lines mean nobody dies to the spine. That
  removes the worst railroad failure: dying to an unwinnable fight.

**What does not hold up.** Five things would break a sharp table's suspension of disbelief or
leave the DM without an answer, and each happens at the hinge of the night:
1. **The host's motive collapses under the players' best play** (L1). Raunu knows by
   Movement III that something is coming. If warned he says "I know" and "does not act". He
   owns a room the Uninvited will not enter, and Veier has sat in it. Yet he keeps her
   upstairs and sends her out by boat *[corrected 2026-10-20 by the owner: Raunu plans to keep her in the palace until the child is born. The boat is Vell's preparation, not Raunu's; see DESIGN_oraga_5e_3p_pass.md TP11]*. The book never says why. The table that solves the
   most is the one most likely to ask.
2. **The palace leaks** (L2). The Court's garden doors open onto the terraces, the gardens run
   to an unlocked river gate, and nothing closes them at midnight. The premise of S3 ("two
   hundred people… a gate barred from the far side") and the Crossing's "dark, empty
   terraces" both depend on nobody walking out the back.
3. **Nobody can get into the east wing at midnight** (L3), and the agenda that is supposed to
   put a character beside Veier has already shown that character out.
4. **The climax has no fail state** (L4). "Either way, the escape holds" (05:610–611). Every
   trick at the river gate buys nothing, and the escape succeeds offstage with no character
   present. The night's set piece is a cutscene with dice.
5. **Three players are not planned for** (L7). The cast-pick guidance, the runtime and the
   east-wing access all assume four. With three players, only three of the eight agendas
   are dealt, and the only reliable route to the night's central secret depends on one of
   them.

**Counts:** P0 **0** · P1 **7** · P2 **14** · P3 **12**.

**Old open items from review 2 that still matter for sense:** N4 (all four geometry gaps are
still present, and two of them now feed P1s below), P3-22 (forced wing "doubled for the rest of
the night", 04:79–81), P3-21 ("Wept: east doors", 08:243), and P3-24/25 (S4's guard count in
Movement V; S10's box shows two slingers but the card fields three). N11 (the overview
schematic) matters less for sense than L2 and L3, which a schematic would at least have
exposed.

---

## 1. Clue-path table: the secrets the night hangs on

The book's own rule is redundant clues, so that "never let a single failed check close a
thread" (04:580–582). This table tests that rule.

| # | Secret | Clue paths (file:line) | Paths | Gate / single point of failure | Verdict |
|---|---|---|---|---|---|
| 1 | **The three gray masks are impossible guests** | Mv III omen (04:1080–1087); Corval's slide (04:800–802, 07:242–249); Corro worst near them (04:803–804); craft-eye DC 13 (04:805–807); antique speech, History DC 13 (04:808–810); Orthaen crystals go faint (04:811–812); Undercurrent D's gossip hole, Insight DC 13 (04:795–796) | 7 | None | **Robust.** A model three-clue mystery. But see L6: knowing it buys almost nothing to *do*. |
| 2 | **Veier is pregnant: the heir, and what the ball was for** | Anha's third plate (07:274; 04:753); new-hemmed linens, Perception DC 13 (04:754–756); rumor 11 tests the guards (04:756–758); the midwife glimpsed end of Mv II (04:760–762); the nursery in B9 (04:382–385); Veier confirms at dinner (04:1312–1315); the Root's observation lattices (04:670–673); rumor 7 says "heir" (08:278) | 8 sparks | **Every spark ends at the east-wing doors.** The conclusion needs B9 or Veier. The ways in are the ring (Agenda 4), Anha's passages (contradicted, see L7) or "real ingenuity" (04:762–763). Forcing the doors is S4, and "nobody gets through the doors this way" (09:911–912). The Root route is the deepest optional thread. | **Single point of failure at three players.** Without Agenda 4, a table can suspect the pregnancy but cannot confirm it. |
| 3 | **What the child *is*** ("both rivers, one spring") | The Root's orrery only (04:676–696) | 1 | Behind Undercurrent A ("if you have time", cut first when behind, 01:204; 04:574). Its key is the study slate (B8: DC 18 lock, wiped by the wardens in S8), or a DC 18 Arcana improvisation | **Single path, maximally gated.** The night's most satisfying answer is the one most tables never see (P2-7). |
| 4 | **Fracture truths** (daughter / devotion / promised family) | Table V–6 (05:769–771): 4/3/3 tells before midnight and 2 each during the attack; the dance line is "given to any character" (04:1376); hearsay through Sella or Kovaun counts (05:736–737) | 10+ | None | **Robust**, and the best-seeded system in the book. |
| 5 | **The Attendant's three habits** | Sightings in Mv I, II, IV and V (04:869–874, 967–971, 1223–1227, 1379–1384); hint list (09:1863–1884) | 4 + hints | None | **Robust.** |
| 6 | **The Root exists, and how to open it** | Rumor 5 (08:276); Anha's forbidden stair (07:276–277); the slate's door-shape, Investigation DC 13 (04:597–600); tally cords (04:603–609); the seam (04:610–616) | 3 sparks, 2 keys | The key is the slate (in B8, which needs Thieves' Tools or S8's wardens to open it) or a DC 18 Arcana check after ward study. At three players, Pello (the only Thieves' Tools pregen) is often the one left out | **Fragile** at three players, and fine at four. |
| 7 | **The Uninvited will not cross the Root's threshold** | None. It is stated to the DM (04:709–711; 05:53–55) and never seeded to players | 0 | Players can learn it only by trying it at midnight | **Dead end.** It also contradicts the trap rule (P2-12). |
| 8 | **The household was evacuated, not disposed of** | The returned footman (04:718–729); Corval (04:731–737); Sella's testament (07:344–346); Corval "if friendly" (07:228–229) | 4 | None | **Robust**, and fair. |
| 9 | **Raunu chose Veier over his own life** | The wrist crystal on the dais (05:490–495); Agenda 2's watcher (05:143–145); Sella's "dying well" (07:341–342); rumor 12 (08:283); the testament (04:735–737) | 5 supporting | Seeing the crush needs a character at the dais | **Good.** |
| 10 | **Vell paid for the gate, and planned the escape** | Agenda 6's card (08:348–351); "old coin" (02:397; 06:34); Vell at the river gate in Mv V (04:1361–1365); Tavva's trade (09:700–704); the Crossing | 4 | The DM is told to "reveal this with care and full weight" (02:389–392), but no scene carries the reveal unless that character is at the river gate. The claim is also false (P2-6) | **The DM is told it but has no way to convey it.** |
| 11 | **Somebody wanted Veier held (the Second Clause)** | Only the captain invoking it in S3's ending 1 (05:1015–1019; 09:839–842) | 1 | Ending 1 only | Acceptable as a bonus, but "send word to the river" dangles (P2-10). |
| 12 | **The Tithe of Hands** | Raunu, to anyone who asks at a summons (04:1065–1068); Corval's kindness (02:290–292) | 2 | A summons, which Corval controls | **Good.** |

**Net:** the *ball's* mysteries (1, 4, 5, 8, 12) are well built. The *night's* mysteries (2,
3, 6, 7, 10) are gated, single-path or seeded to the DM alone.

---

## 2. Where agency is real, and where it is illusory

| Player choice | Changes the outcome? | Evidence |
|---|---|---|
| Who lives: Maiven, Corval, the Tithe ministers, guests at the Phern door and in the fire | **Real** | 05:880–887; 09:1525–1527; 09:1676–1679 |
| Raunu saved | **Real**, and easier than the text implies (L5) | 05:1090–1103 |
| A snake's line answered or turned (heat, S7–S13) | **Real**, with visible downstream cards | 09:464–481 |
| The slate or the drawer kept from the Church | **Real** (for the aftermath and the Root) | 09:1305–1308 |
| The Bought fought, bought, voided or outlasted | **Real** in *how*, not *whether* ("all of them are wins") | 05:1013–1035 |
| Trapping an Uninvited | **Real**, and contradictory (P2-12) | 05:1124–1156 |
| **Warning Raunu or Corval before midnight** | **Illusory.** Corval: "it already will be" doubled. Raunu "does not act" | 04:825–831 |
| **Acting on the pattern before midnight** (the reward 01:424–425 promises) | **Uncovered** (L6) | — |
| **Agenda 6: unlocking the gate** | **Illusory.** Vell unlocks it himself if not | 04:1363–1365 |
| **The Crossing: every trick, Delay, a body at the gate** | **Illusory.** The escape holds either way, and holds with no character present | 05:605–611; 05:625–629 |
| **Delay "buys Veier hallways"** | **Illusory** for Veier (she escapes regardless). Real only where it buys a named person (Table V–1's Radiant row) | 05:270–274 |
| The ending text | **Barely.** One read-aloud, written for the default history | 05:1059–1072 |

Players will feel this most at the river gate. A DM who has read 05:610–611 will feel it the
whole time they run the climax.

---

## 3. P1 findings

### L1. The host's motive falls apart exactly where the players are cleverest
- **Raunu knows before midnight.**
  - "Are you in danger?… I am not certain the arranging was sufficient" (04:1118–1121).
  - Warned about the three: *"I know… stay near the walls after the bells"*, and he "does not
    act" (04:827–831; 07:62–63). The note promises "What he is already doing about it is
    chapter V" (04:831).
  - Chapter V shows only two wrist crystals (05:143–147, 05:490–495).
- **He has a safe room the Uninvited will not enter.**
  - The Root is "a safe room that can shelter a dozen guests… the Uninvited will not enter it"
    (04:706–711; 05:50–55; 10:172).
  - Veier has been in it: "a chair with a wide armrest, a stool beside it, a lap-blanket of
    Thenya wool" (04:647–649). It is his "true workshop" (04:398–399).
- **And yet** Veier stays in the east wing at midnight, and her escape is a wounded flight
  down a garden to a boat.
- **The book admits a gap one level up:** "Why the most prepared man in Val'loh let every one
  of his enemies walk into his house armed is never said" (09:31–33). That is an acceptable
  mystery. The Root question is not a mystery. It is a hole, because the module hands the
  players the answer to their own question.
- **Table failure.** The party bottoms Undercurrents A and D by Movement IV, which the book
  explicitly rewards. Their player asks at dinner: "Why don't you take her down to the Root?
  We've seen it." The DM has nothing in the text to say. Any improvised answer ("he doesn't
  know they won't cross it") contradicts nothing, but now the DM is inventing the spine's
  logic live. If the DM says "fine", history breaks with no ⟨If History Breaks⟩ sidebar for it
  (see L6).
- **Fix (needs owner ruling). Give the DM one paragraph in chapter II, "Why the Ball", that
  answers "why doesn't he hide her?"** Options, each consistent with current text:
  - (a) **Raunu does not know the threshold holds.** "Nothing in this adventure explains why"
    (05:55) already makes it unknown in-world. Say outright that he has never tested it, so
    only a party that discovers it at midnight can use it. Then add an ⟨If History Breaks⟩
    entry for "Veier taken to the Root".
  - (b) **The Root cannot hold a birth, or the child.** For example, what the instruments
    measure makes the deep crystal unsafe for the gift itself. This is new canon.
  - (c) **He believes no place holds them for a whole night**, which "deep ward-crystal holds
    them" and the trap rule (05:1132–1136, "until the last bell and not one moment past it")
    nearly support. His plan is therefore movement plus seals plus Vell's boat. This needs
    one sentence saying Raunu knows of Vell's arrangement, or Raunu's "I know" stays
    unexplained.
  - Whichever option is chosen, rewrite 04:831 so it points to something chapter V actually
    shows.

### L2. The Court's garden doors make the night's two set pieces impossible
- The Court's garden doors open at ground level onto the railed garden walk. The terraces step
  down from them to the lower garden and the river gate (05:445–448, 05:454–455; maps VIII–1,
  VIII–3, VIII–4).
- Nothing closes them at midnight:
  - The Hollow holds "the main doors" (05:150, 08:38).
  - The crowd "leaves by the service doors and the gallery-side door" (05:382–384).
  - The Phern door is "the one open door off B2 at midnight" (08:189–190) and "the only one
    open" (05:861).
  - `grep` finds no midnight rule for the garden doors anywhere.
- S12's read-aloud even calls the gardens the *right* way out: knives "coming the wrong way…
  toward the service passages, not the gardens" (09:1596–1597).
- **The consequences:**
  1. **S3's premise fails.** "Two hundred people are trying to leave through a gate barred
     from the far side" (01:395–396). They can walk out the back to an unlocked river gate
     onto the river walk. The card even lists "the river gate, if anyone thinks of it" as an
     out (09:866).
  2. **The Crossing fails.** It happens on "dark, empty terraces, nobody watching" (05:592–
     594). If the crowd flees through the gardens, the Radiant is *Witnessed* by hundreds, and
     his Fracture's best road is gone.
  3. **The "decoy" logic of the front gate** ("Vell… planned around it", 05:975–978) means
     nothing if the back is open to everyone.
- **Table failure.** At 3:40 a player says: "We take the crowd out through the garden doors,
  like we did for the duel." The DM must either invent a block on the spot (railroad, felt) or
  let 200 people stream across the Crossing and through the river gate, which dissolves both
  S3 and the Crossing.
- **Fix (needs owner ruling).** Decide what the garden doors do at midnight and print it in 05
  "General Features" and in Table VIII–2:
  - (a) **They are warded routes** that seal at the lights, as Raunu's corridor wards do
    ("every warded route is lit, loud, and watched", 04:84). Only a ward-steerer or the Root
    opens them. This also makes the Crossing private by construction.
  - (b) **The Hollow's Post covers both sets of doors**, with *Shadow-Step* between them. Table
    V–3's trick 5 already has him stepping to "another door".
  - (c) **Let the crowd use them**, and rewrite the Crossing as a witnessed scene and S3 as
    "the front gate is where the gentry go". This is the largest rewrite.
  - Option (a) is the smallest change and the most consistent. Whichever is chosen, reconcile
    "the one open door" and "the service doors" (plural) in the same pass.

### L3. Nobody can get into the east wing at midnight, and Agenda 4 has already left
- **The promise.** Agenda 4: "This agenda puts a character beside Veier at the Unmasking.
  Chapter V leans on it" (02:351–353). Chapter V: "Any character with her (Agenda 4 above
  all)" (05:555–556).
- **The reality.**
  - Dinner ends "when the lamps begin to lower for the Dead Dance, Corval comes to the door and
    the guest is shown out" (04:1318–1320). So the Agenda 4 character is *not* in the wing at
    midnight.
  - At the lights, "The east wing corridor booms shut somewhere above, sealed from afar"
    (05:145–146).
  - Maiven "goes toward the east wing" and dies "in the east wing corridor" (05:876–881).
  - The Radiant hunts "through corridors that lock themselves behind her" (05:501–506). Raunu's
    *second* crystal is spent only when the Wept reaches him (05:490–495). So who seals what,
    and when, is unclear (the first crystal sealed "the corridor": which one?).
- No text says how a character in the Court reaches the Radiant's chase. Nothing says whether
  the two guards on the east-wing doors (Table VIII–7) are inside or outside the seal, or
  whether the service stair or service door is open.
- **Table failure.** The Agenda 4 player, who has spent the night earning Veier's trust,
  stands at the foot of the east stair at 3:15 and asks how to get to her. The DM has three
  contradictory pages and no answer, in the scene the book calls "where the night has been
  pointing" (05:517–518).
- **Fix (needs owner ruling on what is sealed).** Add a three-line "Into the wing at midnight"
  entry to 05 "General Features":
  - what the first crystal seals (for example, the double doors, so that the cleared corridor
    stays open);
  - the routes still open: the service stair and the wing's service door (map VIII–5 draws
    both), the garden stair from the upper terrace, and Table V–4's plank wall;
  - one sentence on the Agenda 4 character, for example "If Veier chose them at dinner, she
    asks them to stay. Corval shows out everyone else." Or cut "beside Veier at the Unmasking"
    from 02:352–353.

### L4. The climax has no fail state, and the book says so in two places
- 05:605–611: "If he has any Delay left… the boat is out of reach before he acts. If he has
  none, he spends the turn on whoever stands between him and the boat… and the boat is out of
  reach all the same. **Either way, the escape holds.**"
- 05:625–629: with no character present, "run it offstage… Vell holds, the boat clears".
- Table VIII–2: "out the river gate (**by default, even if no player character is there**)"
  (08:41).
- **So:**
  - Every Table V–5 trick, the Delay "carried down to the gate" (05:595–596), and the Radiant's
    Fracture at its "most invocable" buy nothing.
  - "The margin should be the characters, not luck" (05:602–603) contradicts both passages.
  - Table V–1 says Delay on the Radiant buys "one more person in his way gets clear", but at
    the gate nobody is in his way except a character, who is protected by "Down, Not Out".
- **Table failure.** A player spends Heroic Inspiration on the Radiant's Fracture at the
  water's edge and lands it. Nothing changes, and the DM knows nothing could have. Tables
  that read the module afterward, or a DM with a conscience, will feel the railroad here,
  in the scene that is supposed to pay off all the night's seeding.
- **Fix (needs owner ruling: the stake must not break canon).** Give the Crossing one real
  stake that the record doesn't fix. Options:
  - (a) **Vell's cost.** At 0 Delay with nobody between, Vell must break his rule and *touch*
    the wrapped sword (07:517–522). Canon holds, but the garden drops where it stands:
    Maiven, guests, the characters. This is new canon.
  - (b) **Veier's condition at the boat.** The cart in 06:35–36 ("a factor and his sick
    daughter") and "she will not survive the night" (02:215) leave room for how long she has.
    At 0 Delay she takes a second wound, and the characters see it. This is cosmetic but
    felt.
  - (c) **Who the Radiant goes through.** At 0 Delay he kills a named NPC beside the party
    (Maiven, a slinger, a guard). Delay is then the margin for *that* life, which matches
    Table V–1.
  - Whichever is chosen, delete "the margin should be the characters, not luck" unless it
    becomes true.

### L5. ⟨They save Raunu⟩ is the likeliest divergence, and it has no rules after its first round
- **The math at a three-player table.**
  - A character at Raunu's side steers dais ward-points with a DC 10 Arcana check ("whatever
    they studied", 05:484–486). Four ward-points give 1 Delay each.
  - Two successes put the Wept at 2 Delay, and her Fracture drops to DC 15 "whatever tells
    have been seen" (05:780–782). The guaranteed dance-line tell (04:1371–1377) makes it
    legal to invoke at all.
  - She reaches Raunu on her **fourth** turn at three players (05:78–80, 05:291–292), plus 1
    per Delay. That gives a two-character team about five rounds to make two DC 10 checks and
    one DC 15 check.
  - That is roughly a coin flip or better. It is not "possible, but it takes… real
    sacrifice" (05:1090).
- **What the sidebar doesn't say:**
  - *What happens after her one round.* The Wept "takes no actions… for one full round"
    (05:776–777), then she is the Wept again, with Raunu 5 feet away. "That round is the one
    Raunu needs to choose differently" (05:1093) implies the twin crystal protects him. But it
    doesn't say how long it lasts, whether she tries again, or what happens to "every door
    between Veier's rooms and the river seals itself behind her" if he spends it on himself.
  - *Whether the Crossing changes*, beyond "count from the beat he would have fallen"
    (05:85–86).
- **Table failure.** The flagship divergence lands at 3:30. The DM has a paragraph of tone
  ("Vorlain's face…") and no procedure for the next six rounds.
- **Fix (needs owner ruling).** Print the branch as steps:
  1. Raunu crushes the twin crystal on himself, and it holds him as deep ward-crystal holds
     them (consistent with 02:136–139 and 10:139–141) until the leash or the last bell.
  2. The doors behind Veier therefore *do not* seal. The Radiant gains N beats on her, so the
     party is now the only thing between him and her.
  3. The Wept, her work lost, turns east at the boat as written.
  - Also reconsider the DC 10 dais steering, or make the Fracture's DC 15 need two Delay
    *from tricks other than his wards*, if saving Raunu should really cost something.

### L6. "Act before midnight" is promised, and the book covers almost nothing a table would do
- **The promise.** 01:423–425: "players who assemble the pattern earn the best reward this
  night has: the chance to act before midnight." Also Table I–1's Movement V row: "Anyone who
  assembled the pattern has one chance to act on it."
- **What the book prints.**
  - Warn Corval: nothing changes (04:825–826).
  - Warn Raunu: "does not act" (04:827–831).
  - Confront the three: they leave (04:832–838).
- **What a table will actually try, with nothing printed for any of it:**
  - get Veier out by the river gate *before* midnight (Vell's gate opens "at midnight, not
    before", 02:383–384);
  - tell Maiven and get the Thenya to carry her out;
  - persuade Raunu to skip or cut short the Unmasking;
  - start moving guests out early;
  - take Veier to the Root (L1).
- **Table failure.** The party that played best, the one the book is designed to reward, gets
  either "no" or an improvised branch that breaks canon with no sidebar, at the moment the DM
  has the least slack (Movement V, five live cards).
- **Fix (needs owner ruling for each branch's outcome).** Add an ⟨If History Breaks⟩ entry,
  "They try to get ahead of midnight", with three rows:
  - *Veier refuses or agrees.* Her stated want is "her child born safe" (07:87). Her fear is
    "something is coming… neither knows what" (07:115–116).
  - *Raunu's answer.* For example, he explains why the dais and the seals are the plan, which
    ties to L1.
  - *What the Uninvited do if she is gone early.* For example, the leash and "arriving" mean
    the Radiant finds her on the river walk instead. That needs a ruling.

### L7. Three players: no cast guidance, Agenda 4 de facto mandatory, and the backup route into the wing is closed
- **Cast guidance stops at four.** "With four players and the pregens, leave out Andra or
  Pello. Leave out Ilesse only if another player takes Agenda 4" (01:219–221; 03:197–199;
  11:29–31). Nothing covers three players.
- **Agenda 4 is the only reliable route to the night's central secret** (row 2 of the
  clue-path table):
  - The book calls it "the one agenda that reaches the east wing" (11:30–31).
  - Anha's passages are listed as an alternative route in (04:352–353; 04:762; 07:92–93;
    09:426–427).
  - But chapter IX says the wing's service door has the honor guard behind it: a knife who
    reaches it "finds the honor guard doubled on the far side of it, and is turned back at the
    threshold" (09:1122–1124). "Any fight that reaches the door… becomes S4" (09:1149–1151).
    Nothing says Anha can get anyone past that guard. So the backup route is closed, and
    "real ingenuity" (04:763) is all that remains.
- **Agenda-specific beats with no fallback at three players:**
  - Anha "and her sibling empty the smoke-filled galleries" if Agenda 8 is in play (05:922–
    924).
  - S11's "open another door: Anha, and the character with Agenda 8" (09:1562–1563).
  - Agenda 5's ward knowledge is the main source of DC 13 ward-steering. Without it, every
    off-dais steer is DC 18 (05:37–41).
  - The S8 Agenda 2 out (09:1269–1271).
  - The Agenda 6 reveal (02:389–392).
  - With three of eight agendas dealt, most of these are simply absent. That is fine if the
    DM knows it, and the book never tells them.
- **Runtime.** Table I–1 is "for four players" (01:180). Three players cut fewer ways, so the
  night runs faster, but Movement V's "one card per group" means a three-way split still
  runs three cards in 40 minutes.
- **The midnight split at three.** The night has four places that "need" a character: the
  dais (Raunu, and the L5 save), the east wing (the Radiant, and Maiven, who "dies unless
  somebody competent goes", 05:876–878), the Crossing, and S11's crush. Maiven and the east
  wing converge, which helps. The dais and the east wing don't.
- **Fix (no new canon needed):**
  - Add a "With three players" line to 01, 03 and 11: **keep Ilesse (Agenda 4) and Dassa;
    take Serane or Pello third** (Pello brings Thieves' Tools for B8 and the Root slate;
    Serane brings the second healer and the summons talker).
  - Say plainly that Agenda 4 must be dealt.
  - Either let Anha's passages pass the service door ("the household on the far side knows her
    face"; a small ruling) or strike Anha from the list of ways into the wing.
  - Add a one-line "which agenda beats vanish at three" note to the DM sheet.

---

## 4. P2 findings

**P2-1. Agenda 3 has no completion condition.**
- The ask is to get Vorlain "to say something, anything, that House Draunel could later call
  an understanding" (02:325–327). The heat tracker sets Draunel to 0 on "Agenda 3's
  'understanding' delivered" (09:291, 09:470).
- But Vorlain "says nothing incriminating sober" (02:330; 07:149–151), and every printed
  drunk line is a non-answer (07:179–187). No line, check or scene is marked as *the*
  understanding.
- *Table failure:* Serane's player works Vorlain for an hour, wins the DC 15 drinking check,
  and asks "did I get it?" The DM doesn't know, and the Heroic Inspiration and the 200 XP
  hang on the answer.
- *Fix:* name what counts. For example, "any drunk line, carried to Draunel and *framed* as
  an understanding", which is a Deception check against Draunel (DC 13). Also say what it
  does to Vorlain at dawn, because the card hands a weapon to a man with no plot.

**P2-2. The Patron's Errand hook tells Ilesse's player her patron is a snake.**
- Table I–2: "your patron is also a snake (see chapter IX)", and it lists *The Cousin's
  Errand* among its fits (01:237).
- Ilesse's suggested hook is exactly that (11:22), and the Thenya are "not a snake" everywhere
  else (02:356–358; 09:397–412).
- *Fix:* "…and your patron may be a snake" (the Thenya are the exception). Or drop *The
  Cousin's Errand* from the Fits column and give Ilesse *The Entourage*.

**P2-3. Vell's sword: on his back, or wielded bound?**
- "The wrapped sword stays on his back… through everything that follows" (05:564–565,
  05:577–578).
- But he "fights the Radiant with it still bound" (07:520–522), "holds the Radiant with the
  sword still wrapped" (07:565–566; 10:2141–2142).
- The DM will describe one and the cast chapter says the other. *Fix:* pick one. "Still
  bound" is the stronger image and needs only 05 changed.

**P2-4. How does Vell end up in the boat?**
- Vell holds the Radiant on the terrace and in the garden, and the characters carry Veier to
  the gate. The Radiant "breaks past Vell" and reaches the water "as the boat pulls out"
  (05:597–600). Yet "a pale man rowing hard into the dark" (05:616), and "the water takes him"
  (07:559–560).
- Vell is behind the Radiant when the boat leaves. *Fix:* one sentence, using his *Elsewhere*
  action (10:2118–2121): "When the Radiant breaks past, Vell is already at the oars, arrived
  rather than run."

**P2-5. The child is unborn, and the book never says what the Uninvited meant to do about it.**
- The task is "kill Veier… and carry away the child she is about to deliver" (02:154–155;
  01:77). The Second Clause holds "a woman in Thenya wool" (05:964–965), so the payer wants
  *her*, not a child.
- A table that learns the pregnancy will ask how you take an unborn child from a woman you
  were sent to kill. The answer the text implies is one the safety section (01:540–545)
  promises never to put near the table. The DM needs to know what to steer away from, and
  what the Radiant is *doing* when he catches her.
- *Fix (needs owner ruling):* one line in "What Is Coming". For example, "they were sent to
  take her, and the child with her. The parents' deaths were the errand's cover", or "labor
  begins at the lights". Each option changes the Radiant's behaviour at the Crossing (does he
  strike to kill, or to seize?).

**P2-6. Agenda 6's emotional reveal is false, and has no channel to the player.**
- The DM is told to reveal that "the character who felt like a hired traitor all night was,
  in fact, the reason mother and child got out" (02:389–392).
- But if the character refuses or reports the job, "he unlocks it himself. He always has a
  second way" (04:1363–1365), and the escape holds regardless (L4).
- Nothing puts that character at the river gate to see Vell. *Fix:* reword the note to "one
  of the reasons, and the one that let Vell spend his second way on something else". Add a
  beat in which Vell looks at *that* character at the gate, folding in 07:556–560's "one crack
  in the ice".

**P2-7. The night's best answer is gated behind its most cuttable thread.**
- "Both rivers, one spring" (04:692–696) is the only place the night tells the table why the
  child matters. It sits in Undercurrent A, which is marked "if you have time" and is on the
  first-to-cut list (01:204; 04:574).
- Reaching it takes a spark, the cellar seam, and the B8 slate (DC 18 lock, contested by S8's
  wardens) or a DC 18 Arcana check.
- At three players, most tables never see it. They walk out with "the child was the prize,
  and we never learned why", which is the "secrets withheld" problem in its worst form.
- *Fix (needs owner ruling for any new line):* route one echo of the figure into a
  non-optional scene. For example:
  - Raunu's "Something true" at the summons gains a beat;
  - Veier at dinner says her husband "says the baby remembers";
  - the Root voice-lattice line (04:643–644) is quoted by Anha as "the master's voice in empty
    rooms" (07:275).
  - The Anha option is the lightest, because the line and the voice already exist.

**P2-8. The endings are indistinguishable.**
- One epilogue read-aloud is written for the default: "the chief… dead in his shining hall…
  his bride gone into the river dark" (05:1061–1067). It also gives *every* character the
  Wept's dance memory, though only one heard it (05:1069–1072 against 04:1376).
- ⟨They save Raunu⟩, ⟨The child is taken⟩, a living Maiven and a captured sergeant get "adjust
  it". The book's own principle is "a reward you have to remember to invent is a reward that
  does not happen" (01:290–292).
- *Fix:* add an endings box that sets the state variables already in the book against one
  replacement sentence each:
  - Raunu alive or dead;
  - Maiven alive or dead;
  - Corval and the Tithe minister alive or taken;
  - Vorlain taken or free;
  - the slate and the drawer;
  - the Bought fought, bought or outlasted;
  - the Wept looked back;
  - the Hollow sent home early.
  - Change "each of you dreams" to "the one she danced with dreams".
  - No new canon is needed.

**P2-9. The bell sequence confuses the DM, and the last bell waits for the party.**
- The text uses midnight bells, quarter-bells, a half-bell, "the bells of Oraga begin to toll"
  after Raunu falls (05:83), and "the last bell of Oraga".
- The last bell is the leash's hard limit (02:131–133; 10:131–132). But it rings "once the
  front gate is decided" (05:62–63), on a clock that "counts only the rounds the characters
  spend at the gate" (05:90–95; 09:783–791). So a civic bell over a whole city waits for a
  party at one gate.
- The text manages the timing so the leash comes first, and players won't see the seam. A
  DM reconciling "the leash takes them at the last bell at the latest" with "the last bell
  never rings during the Crossing" will stall.
- *Fix:* add a one-line bell glossary to the DM sheet. Reword the S3 clock as "the sect
  guard's arrival" (the real in-world event), with the last bell as its signal.

**P2-10. Voiding the contract because "the target is gone" doesn't void it, and "send word to the river" dangles.**
- Clause 2 is "nobody in, nobody out" until the last bell (05:961–962). Veier's escape voids
  only clause 3, yet "the named target already gone" is a listed void (05:1020–1022; 07:730–
  731; 09:852–854).
- The Second Clause's "send word to the river" (05:965; 07:749) implies the payer expects
  someone at the river. It is the one line that points at the escape route, and nothing
  explains it.
- *Fix:* make the "target gone" route work through the captain ("the clause he was really
  paid for is dead; he won't hold a gate for a fee's leftovers"). Rule on "the river" (needs
  owner ruling): cut it, or say whom it means.

**P2-11. Selling the nursery has a consequence that doesn't follow from it, and breaks a pillar.**
- Callun "fears exactly one thing… an heir" (04:779–783). Selling her the nursery sets heat
  to 4 (09:184–185), and heat 4 fires S12: her knives kidnap a Tithe minister (09:175). That
  answers the heir with a tax policy.
- The pillar says "no faction learns of the child unless a player character tells them"
  (08:55–56), and 06:28–32 still says "the pregnancy never gets out". Nothing says what the
  Circle does with the knowledge, or how the aftermath changes.
- This is the night's most morally loaded choice, and it gets a non-sequitur.
- *Fix (needs owner ruling):* give the sale its own midnight beat (for example, the knives go
  for the east wing's service door in the dark, into the Radiant's path), and its own
  aftermath line in 06.

**P2-12. The trap rule contradicts the threshold rule.**
- The Uninvited "will not cross" the Root's threshold (04:710–711; 05:53–55). ⟨They trap one⟩
  says "a table that lures one into the Root's threshold… has caught something" (05:1127–
  1130). You cannot lure someone across a threshold they won't cross.
- Players can't learn the threshold rule before midnight either (clue table, row 7).
- *Fix:* cut "the Root's threshold" from the trap list (keep "a resealed ward-corridor, or a
  gallery ring"). Say whether the **Attendant**, which is not Leashed, will enter the Root. As
  written, a party hiding in the Root is safe from the boss too, and nobody has said so.

**P2-13. The slingers climb a 20-foot wall beside two stairs.**
- S10 has the slingers roping up to a lit window (09:1430–1435, 09:1462–1463). Map VIII–5
  draws a **service stair** "up to the doors, down and out to the garden (S10)", and the
  **garden stair** runs "down the wing's outer wall to the upper terrace" (05:457–459). Maiven
  herself "comes down the service stair" (09:1451–1452).
- Nothing says the garden stair's top door is locked or guarded.
- *Fix:* one terrain line, for example "the garden stair's door at the top is crystal-sealed
  from inside, and the service stair ends at the guarded doors". This also partly closes
  review N4's S10 window problem.

**P2-14. The Attendant has no rule for a split party.**
- It is "beside the three" (08:39), and the three are in three places (the dais, the wing,
  the doors). S14 "fires wherever the party gets in an Uninvited's way" (09:1759–1761).
- At three players, one character on the dais and two in the wing is the expected split, and
  the DM must decide which scene the boss is in. *Fix:* "It goes to the first Uninvited the
  party interrupts and stays in that scene. It cannot be in two."

---

## 5. P3 findings

1. **Corval's doubling is inconsistent.** The forced-wing rule says the wing "stays doubled
   for the rest of the night" (04:79–81), but Table VIII–7 has two guards at midnight. This is
   review P3-22, still open.
2. **Table VIII–6 has "Wept: east doors"** (08:243), but the tell is at the **east-wing**
   doors (05:769). These are 60 feet and a stair apart. This is review P3-21, still open.
3. **The toast happens "in the galleries, for everyone"** (04:460; 04:1170), but Raunu stands
   at the high table on the Court dais (04:1171–1172). The galleries are 12 feet up along the
   long sides (05:442–444) and have no stairs or doors on any map (review N4). The sightline
   works only if the galleries overlook the dais, so say so. Then draw the gallery stairs.
4. **The slingers watch "the guard change on [the east-wing corridor] from the gallery rail"**
   (04:1160–1161), but the corridor is beyond the east doors and up a stair. They cannot see
   it from a Court gallery.
5. **The midwife has no midnight position.** She is the "third plate", "gone by dawn"
   (06:28–29), and absent from Table VIII–2. A party guarding the family will ask where she
   is.
6. **The two Tithe ministers are never placed.** They are central to Agenda 1, S12 and
   "keep Corval alive and the Tithe survives" (02:294–296). Neither is in Table VIII–6, and
   neither is named.
7. **"Raunu summons four guests all night"** (04:1037), and he is "seen exactly four times"
   (07:21) by the public. Dinner is a fifth, private appearance. That is fine, but say
   "publicly".
8. **The S10/S4 default leaves the slingers in limbo.** The Thenya default to heat 3, so the
   half-bell S4 runs offstage at every table that does nothing (08:218–221). Are the slingers
   in the cell at midnight, when "her slingers behind her" (05:877)? Answer: the cell opens at
   the lights (04:72–74). Say so in S10's Development.
9. **Vell's route is odd.** He is at the river gate at the end of Movement V, then at
   midnight takes "service passages → garden stair → the river gate" (08:42; 05:171–173). That
   means walking up through the palace to come back down. A line saying "he climbs back to the
   foot of the garden stair to meet her" fixes it.
10. **"The Radiant reaches the garden stair three beats after Raunu falls"** (05:84–86), but
    he is in the wing from the first beat, and Raunu's door-sealing crystal fires only at the
    fall. The wing chase therefore lasts five or more beats against a woman with 15 feet of
    Speed. Give the DM one sentence on why: the seals from the first crystal, plus Witnessed.
11. **Agenda 2's "honest judgment"** concerns a question the module refuses to answer
    (02:235). It is workable as "any sincere judgment completes it", but the card's "the
    Prelate will know if you shade it" (08:329–330) needs a DM line on how she knows.
12. **"The Undercurrent C find is the secret the ballroom is guessing at"** (04:770), but
    02:176–180 says the ballroom guesses a trade decree. Pick one.

---

## 6. Does the spine work for the DM, and does it feel like a railroad?

- **For the DM: yes, mostly.**
  - "The Uninvited cannot be beaten, only delayed; history bends toward the record" is stated
    once (02:198–228) and backed by mechanics: *Leashed*, Delay, the Fractures, "Down, Not
    Out". The DM Note on never fudging (05:718–723) is exactly right.
  - What fails the DM is not the spine. It is the **load-bearing walls around it**: why Raunu
    stays (L1), how the palace channels people (L2, L3), and what happens when the table
    bends history in the most likely way (L5, L6).
- **For the players: it depends on where they push.**
  - At the dais and the doors, Delay buys named lives, and the table sees the die move. That
    feels earned.
  - At the Crossing, the payoff of everything (L4), nothing they do changes anything, and the
    book knows it.
  - Before midnight, the reward for solving the night is the chance to act. The actions the
    book prints all end in "no".
  - Fix L4 and L6, and the railroad becomes a river with banks.
- **The "secrets withheld" approach** is defensible for the setting's meta-mysteries (the
  missing year, the master, Vell's order). It is not defensible when the one answer the night
  *does* give ("both rivers, one spring") is the one hardest to reach (P2-7), or when the DM
  is told a truth (Agenda 6) with no scene to tell it in (P2-6). Officially published
  adventures that withhold their deep lore still make sure every table leaves knowing what
  *tonight* was about. This one ensures that only for tables with Agenda 4.

---

## 7. Recommended order of work

1. **Owner rulings first**, because every fix after them depends on these: L1 (why not hide
   her), L2 (the garden doors), L3 (what the first crystal seals), L4 (the Crossing's stake),
   P2-5 (the unborn child's fate), P2-10 ("the river"), P2-11 (the nursery sale), and whether
   the Attendant enters the Root (P2-12).
2. **Three-player pass (L7):** cast line, Agenda 4 mandatory, Anha's route, the agenda-beat
   fallback note.
3. **Procedures for the divergences:** ⟨They save Raunu⟩ as steps (L5), "Ahead of midnight"
   (L6), the endings box (P2-8).
4. **Contradiction sweep:** P2-2, P2-3, P2-4, P2-12, P2-13, P2-14 and the P3s, plus review
   N4's geometry, which L2 and L3 now make urgent.
5. **Tooling:** add `facts.yaml` entries for the garden-door state, the midnight wing routes
   and the boat. The fact checker could then hold these decisions once they are made.
