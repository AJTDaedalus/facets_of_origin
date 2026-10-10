# REVIEW 2: Oraga Night 5e, a critical re-review after the review-fix pass (R6.2)

*2026-10-10. Adversarial review of `conversions/dnd5e/oraga_night/` at `ee82586` (clean tree).
I read every chapter, the README, `facts.yaml`, `STYLE_5e.md` and the five maps (PNG, by eye)
as three readers: a DM prepping for Friday, a rules lawyer at a 5e table, and a publisher's
editor. No module file was edited and nothing was committed. Paths are relative to the module
folder. Line numbers are from today's files.*

**Tool runs (necessary, not sufficient).** All green:
- `lint_5e.py --check`: OK, 0 hard and 0 structure hits. Every new rule family is at 0, and every
  tic sits exactly on its target. That precision is a sign the edit was steered to the metric
  (see N17).
- `fact_check.py --check`: OK, 0 hits.
- `bestiary_check.py`: 28 blocks + 1 Nastier line, 0 mismatches.
- `pregen_check.py`: 5 pregens, 0 issues.
- `copyright_scan.py --refs …/r61/refs --srd …/r61/srd`: 4,979 sentences; (a) SRD 28, (b)
  allowlisted 18, (c) to review **0**. I also ran an independent 6-word-shingle pass against the
  21 reference extracts, minus the SRD. Its 142 hits are all stock check and save grammar ("a DC
  13 Wisdom (Perception) check to notice") or generic English ("at the end of this chapter").
  **No read-aloud or descriptive prose overlaps an official book.** The copyright position is
  clean.
- `pytest tools`: 407 passed.

I hand-checked the three new blocks, every block's HP and hit dice, its attack and DC
arithmetic, and every card's budget sum at every scaling line. All of it is correct. The defects
below are the kinds the tools cannot see.

---

## 0. Verdict

**8.0 / 10.** This is a large, real improvement on 6.5:
- The continuity bible did its job. The household, the nine guards, the arrivals, "forty blades"
  and Maiven now agree everywhere.
- The prose no longer prints simulation data, file names or HTML comments.
- One trigger format and one box-label format hold throughout.
- The dossiers are deduplicated, and "Down, Not Out" lives in one place.
- There are five original, scaled maps that agree with the text's numbers.
- The copyright position is clean, and the stat blocks and pregens are still clean.

It still is not an official-quality book, for three reasons:
1. **The O32 fix gave the boss a new exploit.** An Idle distraction makes a character
   "furniture for the rest of the scene", with no exit clause.
2. **The QR3 retinue change broke S8's clock.** A fourth warden is "already inside" the room
   the other three are picking the lock of.
3. **The maps carry the scaffolding the prose lost:** decision IDs ("(O54)"), a "?" in a
   profile, "not given" ten times, and "drawn plausibly". Chapter VIII's frame says the same
   things ("Rooms the text does not place").

A layer of geometry residue sits under the maps ("second floor" against "gallery level"; S10's
window; the unknown drop from the walk; no access to the galleries). There are also a few
pointers left dangling by the new named blocks.

**Counts:** P0 **0** · P1 **3** · P2 **9** · P3 **17**.

**Old findings:**

| Severity | Resolved | Partly resolved | Regressed |
|---|---|---|---|
| P1 (7) | 3 | 4 | 0 |
| P2 (24) | 19 | 5 | 0 |
| P3 (24) | 20 | 3 | 0 |

One P3 (P3-24) cannot be judged: it is ledger-only. Section 1 gives the table.

---

## 1. The previous review's findings

### P1s

| ID | Status | Notes |
|---|---|---|
| P1-1 Household | **Resolved** | Sixty; "cut by nearly two-thirds" (02:69, 02:420, 04:716); 22 who stayed (07:196, 07:228); "four-fold" is gone. |
| P1-2 Nine guards | **Partly** | Table VIII–7 is good: seven to the dais, two at the doors (04:83, 05:475, 08:43, 10:497). Residue: 04:79–81 says that if the wing is forced, "The east wing stays doubled for the rest of the night", but the table has two at midnight (N22). And S4 fields two guards in Movement V, when four stand on the doors (N24). |
| P1-3 S14 one-roll win | **Resolved as specified**, but **O32's replacement is exploitable** | Arguing is a trick everywhere, and the Rewards line no longer pays for it. But the new Idle "furniture" rule is a fresh exploit (N1). |
| P1-4 Arrivals | **Resolved** | 01:62–64; Table V–6 "(any Movement from III)", "Mv III–V". |
| P1-5 East-wing floor, terraces | **Partly** | Elevations are now in 05 General Features, and the private stair is the garden stair. "Two terraces below" is gone, and S9's box is fixed. Residue: "second floor" is used both as a separate level (B8) and for the east wing (S10); S10's 20-foot wall doesn't fit a floor 12 feet up; the drop from the walk to the terrace is never given (N4). |
| P1-6 No cartography | **Partly** | Five maps, to scale where scaled, consistent with O28/O33. But they print development scaffolding (N3); the overview is still a schematic that leaves six areas unplaced (N11); and no map shows how anyone reaches the galleries (N4). |
| P1-7 Nastier as baseline | **Partly** | Three new named blocks, and S3, S6, S7, S8 and S9 have real Nastier dials again. Residue: S1 still uses its Nastier line as its base roster (N7); 05 and 07 point to the wrong sergeant block (N5); the cousin blocks are muddled (N6). |

### P2s

| ID | Status | ID | Status |
|---|---|---|---|
| P2-1 sim data | Resolved (CR "yardstick" commentary remains, N20) | P2-13 README licensing | Resolved |
| P2-2 file names | **Partly**: 08 now prints `[PNG](maps/…png)` links and "Each map links a PNG copy for printing" (08:144–185) | P2-14 grapple | Resolved (05:361) |
| P2-3 HTML comment | Resolved | P2-15 hint 5 | Resolved (09:1876–1880) |
| P2-4 conversion talk | Resolved in body (02:10–13's pointer to the "Facets of Origin books" is acceptable cross-product framing) | P2-16 out-slug claim | Resolved |
| P2-5 Maiven | Resolved (06:43–44) | P2-17 S3 ending 1 | Resolved |
| P2-6 forty blades | Resolved | P2-18 rule copies | **Partly**: "Down, Not Out" is fixed, but the Fracture rule is now printed in full twice (N8) |
| P2-7 Vell "before midnight" | Resolved | P2-19 2014 claim | Resolved (10:56–82) |
| P2-8 Scora/Kshalo | **Partly**: glossed, but the glosses are garbled (N19), and "Svara" is unglossed (N14) | P2-20 triggers | Resolved |
| P2-9 read-aloud contradictions | Resolved | P2-21 box labels | Resolved (one unlabelled box, N23) |
| P2-10 S4 out vs B9 | Resolved | P2-22 dossiers | Resolved (small residue: the "three heads" sentence ×3, N19) |
| P2-11 Bought change sides | Resolved | P2-23 tics | **Partly**: the targets are met, but the cure is colon and semicolon splices (N17) |
| P2-12 tracker trigger | Resolved | P2-24 emphasis italics | Resolved |

### P3s

Resolved: P3-1, -2, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19,
-21, -23. Partly:
- **P3-3:** "(Deception, Intimidation, or Persuasion)" survives in body text at 07:527 (N15).
- **P3-20:** the glosses are still bolted on (N19).
- **P3-22:** fixed in the loot entry; the phrase now recurs as "a case of writing chained to the
  sergeant's hip" (10:2232), which is fine.

P3-24 (the INVENTIONS annotations) is done in the ledger.

---

## 2. P0: blockers

None. Every scene can be run from the page. The attribution is present and correct in README,
09, 10 and 11.

---

## 3. P1: real defects

### N1. The Attendant's "furniture" rule is a scene-long immunity with no exit clause, so the boss can be switched off
- **10:263–265:** "A success while it is Idle makes the distractor **furniture** to it for the
  rest of the scene: it ignores that creature, **as if it had never interfered**, and goes on
  acting as before."
- The same rule appears at 09:1850–1852, 05:403–405 ("so is a character who distracts it while
  it is Idle") and 08:77–79.
- Nothing says the status ends when that creature interferes again. *Literal Orders*
  (10:244–247, "since the end of its last turn") points the other way, so a rules lawyer will
  argue that "for the rest of the scene… as if it had never interfered" is the specific rule and
  wins.
- **The exploit.** The card fires with the Attendant Idle (09:1786). It stays Idle on any turn
  where every Uninvited in the scene has Delay. Each Idle round, one character makes a DC 13
  check, with up to +4 for playing it out and using a habit, so effectively DC 9. That character
  can then never be attacked by the Attendant this scene.
  - A furniture fighter standing adjacent also switches off *Clears the Way*, which needs "no
    enemy within 5 feet". That is the card's only clock.
  - Two or three furniture characters can grind its 229 Hit Points at no risk. Four of them make
    the "hardest fight of the night" harmless.
- This is the P1-3 class again: one cheap check rewrites the boss fight.
- **Fix:** add one clause in all four places: "…furniture to it until that creature next
  attacks it or interferes with one of the three." Or drop the Idle success outright and say "on
  a success while Idle the trick is wasted on it, and it counts as tried". Either keeps the O32
  intent, since a successful Idle distraction doesn't count toward the four.

### N2. S8's fourth warden is already inside the room whose lock the other wardens are racing to pick
- **09:1234–1236:** "Two **Church Wardens** at the door; the third arrives up the stair on the
  clock's second segment; **and the fourth is already inside the room, and has already found
  something.** Kovaun brought four."
- **09:1228–1232:** "The lock clock… **Full:** the wardens are inside. One round later the slate
  is wiped."
- The box (09:1206–1210) shows two figures kneeling at a crystal lock (DC 18 Thieves' Tools,
  04:316) that is still shut.
- If a warden is inside, the lock clock is meaningless. He can open the door from inside, and
  he can wipe the slate now, which is the card's objective. The text never says how he got
  past a crystal lock. A DM will be asked both questions in the first round.
- The QR3 change ("each faction brought four") was applied by bolting a fourth body on where it
  breaks the card. The scaling lines prove it: "nobody inside (600 XP)" at three characters and
  at 3rd level.
- **Fix:** put the fourth warden at the foot of the dark-wing stair as a lookout, arriving on the
  clock's third segment, or have him working the study's second door from the other side. The
  objective stays "decide what leaves the study". Update *Three characters* and *Four at 3rd
  level* to match.

### N3. The maps, and chapter VIII's frame around them, print development scaffolding
- On the maps themselves (PNG and SVG):
  - **Decision IDs:** "(O53)" on map VIII–2; "(O54)" on VIII–3; "(O33)" and "(O54, O55)" on
    VIII–4; "(O55)" on VIII–5.
  - **A question mark:** VIII–4's profile prints "walk ? upper terrace" and "the walk-to-terrace
    drop is not given (?)".
  - **"Not given" ×10:** "rooms… (their order is not given)", "one lit window (whose is not
    given)", "route not given", "Level not given", "Not given: B4, B6, B7, B13".
  - **Map captions as audit notes:** "Approximate: the court, the gatehouse and the gate's width
    are not given and are drawn plausibly" (VIII–2); "Placed by connection only" (VIII–1).
- In chapter VIII:
  - 08:141–142: "Whatever the text does not fix… is drawn plausibly, and each map's caption says
    so."
  - 08:190: "**Rooms the text does not place:**"
  - 08:150–185: the `[PNG](maps/…png)` links, and "Each map links a PNG copy for printing"
    (08:144).
- This is exactly the class P2-1 to P2-4 removed from the prose: the book talking about its own
  editing. An official map is drawn with confidence. It never hedges, never cites a design log,
  and never asks the reader a question. Here it is on every map, and the maps were the fix for a
  P1.
- **Fix:**
  - Strip every O-number, "?", "not given", "approximate" and "drawn plausibly" from
    `build_maps.py`'s labels and captions. Keep the provenance in `facts.yaml` and DECISIONS,
    where it belongs.
  - Decide the open values (the drop from the walk, room order, the run's route) as design facts,
    as O33 did, and draw them.
  - Rename "Rooms the text does not place" to "Other Areas".
  - Move the PNG links to the README.

---

## 4. P2: off-standard

**N4. The geometry under the maps still has gaps** (residue of P1-5 and P1-6).
- **"Second floor" means two things.**
  - 05:455–456 separates them: "The banquet galleries and the east wing are at gallery level, 12
    feet up. Raunu's study (B8) is on the second floor."
  - Map VIII–1's legend gives "Second floor" and "Gallery level, 12 ft up" different colors.
  - But S10's box puts the east wing's "one lit window **on the second floor**" (09:1428).
  - **Fix:** S10 should say "one lit window at gallery level, high in the wall". Say once in 05
    how high B8's floor is, or call it "the upper floor of the dark wing".
- **S10's wall doesn't fit.** "The wall is 20 feet of grown crystal to the window" (09:1459),
  but the wing's floor is 12 feet up. The sill would be 8 feet above the floor, and "anyone who
  reaches it sees warm light, a quiet household" (09:1463) doesn't work.
  - **Fix:** say the garden below the wing lies one terrace lower (so 22 feet), or make the wall
  "12 feet to the sill".
- **The drop from the walk to the upper terrace is never given.**
  - 05:453–454 says only "the upper terrace lies below that rail". The map prints "?".
  - S9's crowd watches from that rail, and a character who vaults it to stop the duel needs a
    number.
  - **Fix:** choose one (10 feet, to match the other drops) and print it in 05, S9 and the map.
- **Nobody can reach the galleries.**
  - B3 is 12 feet up (05:455), and Movement IV fills it (04:1170), yet no text or map gives a
    stair or a door to it. Map VIII–3's caption admits "B3's doors are not placed".
  - S13's trigger is "Read this when a character reaches **the gallery doors**" (09:1653), and
    S12 and S13's fire and smoke rules need the exits.
  - The Thenya "walk the gallery toward the east wing as far as the cleared corridor" (04:1003–
    1004; 10:1728–1729). No map connects B3 to that corridor.
  - **Fix:** draw two gallery stairs off the Court floor and the gallery doors, and either add a
    gallery door onto the corridor or reword the Thenya tell.

**N5. Three pointers name the wrong sergeant.** S3's roster is "One **Veteran Bought
Sergeant**" (09:789), but these still point to the CR 2 block:
- 05:1002: "the **Bought Sergeant**, the **Bought Blades**…"
- 07:710: "stat blocks **Bought Sergeant**, **Bought Captain**…"
- 07:736, the "Sergeant of the Bought" entry: "stat block **Bought Sergeant** (see chapter X);
  card S3."

A DM who builds from VII or V runs a CR 2 sergeant in a CR 4 slot. **Fix:** name the Veteran
in all three places, and say "(the Bought Sergeant at 3rd level or for three characters)".

**N6. The Boranis cousins are the same three people with two blocks, swapped from card to
card.**
- 09:313–315 says House Boranis brought three Cousin's Blades, "the cousins who stood with
  Vorlain in the missing year". The *Boranis Cousin of 3160* block is "The cousins who were there
  in 3160, the missing year" (10:427). Both blocks therefore describe the same three people.
- Yet S6 fields three Cousins of 3160 (09:1023), while S9 and S13 field three Cousin's Blades
  (09:1352, 09:1683). S9's Nastier swaps back to 3160 (09:1401).
- Worse, the Draunel *Provocation* and S9's circle clock key on the block name: "A Boranis
  **Cousin's Blade** that fails this save draws steel" (10:878–879, 10:1832–1833); "whenever a
  Cousin's Blade fails its save" (09:1329). Under S9's Nastier line the clock no longer ticks.
- **Fix:** either rename 3160 as a *veteran* variant ("Essin's eldest cousin") and field one of
  them, or word *Provocation* and the clock as "a Boranis cousin". Then give the cousins one
  identity across S6, S9 and S13.

**N7. S1 still uses its Nastier line as its base roster** (residue of P1-7).
- 09:576–578: "Eight **Feuding Kinsmen**… — and one principal still swinging (**the kinsmen's
  Nastier line**)."
- The card has no Nastier dial, and the budget (8 × 25 = 200) leaves the principal out.
- **Fix:** write the principal into the roster as a named variant ("a principal: a kinsman with
  22 HP"), and give the card a real Nastier line (for example, "both principals swinging; the
  bench clock advances twice on a 1").

**N8. The Fracture rule is printed in full twice, and each copy calls the other the home.**
- 05:731–763 holds the full rule, and 05:750–751 says "(The same rule is printed **once** in
  chapter X, above the Uninvited's blocks.)"
- 10:178–201 holds the full rule too: DCs, success, both failure bands, "works once". It ends
  "The full rule is in chapter V".
- The two copies agree today, but this is the drift pattern P2-18 (and O36) exist to stop, and
  the sentence "printed once" is false.
- **Fix:** keep 05 as the home. Cut chapter X to its first sentence plus the DC line and "(see
  chapter V, 'The Fractures')". Add a `rule_copy` entry for it to `facts.yaml`.

**N9. Half the Radiant's Fracture sits under Bonus Actions.**
- 10:1496–1501, after *Shadow-Step*: "On a success, guilt gets into the errand like grit into a
  joint. For the rest of the night he… moves at 20 feet…"
- This belongs to *Fracture — Devotion* (10:1464–1474). Where it is printed, it reads as the
  result of a Shadow-Step. The Hollow and the Wept keep their success text inside the trait.
- **Fix:** move the paragraph up into the Fracture trait.

**N10. S3: the gate-walk's outer stair is a way over the gate for the crowd.**
- 09:757–763: "a stair up to the gate-walk… a second stair runs down from the gate-walk to the
  street. One Blade holds the top." Map VIII–2 draws that outer stair.
- The scene's premise is that "Two hundred people are trying to leave through a gate barred from
  the far side" (01:396). Once one Blade (22 HP) is down, guests can file over the gate, and the
  text never says why they don't.
- **Fix:** add one terrain line ("the outer stair is a ladder-steep flight one body wide, and
  the Blade at the top has drawn it up; it is a way for a fighter, not a crowd"). Or cut the outer
  stair and let the walk be a drop-only route (the 15-foot drop is already printed).

**N11. The overview map is still a flowchart.**
- Map VIII–1 is "Not to scale: a schematic", and it lists six areas "Placed by connection only":
  B4 (dashed, "level not given"), B6, B7, B8, B10 and B13.
- The previous review faulted the ASCII figure for placing "five of the thirteen rooms in a list
  below it". This one places six of fourteen in a list.
- **Fix:** draw a true ground-floor and gallery-level plan, at the same scale as VIII–3, and place
  B4, B6, B7, B10 and B13 by design decision. Leave only B8 and B11 as insets.

**N12. Chapter VIII's map frame is a contributor's note, not a reader's caption** (part of P2-2;
folds into N3).
- 08:134–144 explains how the maps were derived ("drawn from chapter V", "at the sizes chapter
  V prints", "where the text gives no route… the map marks them schematic").
- **Fix:** two sentences: what the maps show, and "one square = 5 feet".

---

## 5. P3: polish

13. **Map VIII–3's legend has one rail symbol, "Rail, 12 ft above the Court floor", but it is
    also drawn for the ground-level garden-walk rail.** It needs a second symbol.
14. **"Svara" is never glossed** (01:438, 05:1103, README:136). The book's world is otherwise
    "Val'loh". `terms.txt` doesn't list Svara or "Namak-Zai" (07:604). Gloss Svara once ("the
    world of Svara").
15. **A compressed skill list in body text:** "a DC 25 Charisma (Deception, Intimidation, or
    Persuasion) check" (07:527). The linter's "(X or Y)" rule misses the three-way form.
16. **Undefined place names:** "high gallery" (01:169, 04:1016, 07:29, 08:20, 08:236); "lower
    gallery" (04:406, 08:200); "gallery corridor" (04:537, 08:193); "garden wing" (04:1218);
    "gallery stair" (09:1757); "terrace doors" (09:1051) where everywhere else says "garden
    doors". Define each once in 05 General Features, or use the defined names.
17. **The tic cure has its own rhythm.** The joins swapped full stops for splices. Semicolons
    rose from 635 to 683 and prose colon-joins from 517 to 574, now 5.7 per 1,000 words. For
    example: "Nothing from here on can be scripted: this chapter can only…" (05:167); "spend one
    point: that turn they make no progress" (05:244); "They are frightened and armed: they are…".
    A colon every other paragraph reads as machine cadence. In a human pass, turn about a third of
    them back into two sentences, or into "because" or "so".
18. **Designer commentary is left in the blocks and cards.**
    - S14's CR derivation: "by the usual yardstick its offense rates about CR 5… and its defense
      about CR 11" (09:1792–1800; 10:327–329).
    - Vell: "The block exists to tell you one thing… four 5th-level characters land roughly 15
      damage a round" (10:2153–2159).
    - Make each a two-line DM Note in table voice ("Idle, it hits far softer than its CR; award the
      full XP anyway"; "Vell can be hit, but no party here can drop him before the boat clears").
19. **Garbled or bolted-on sentences.**
    - "A Scora (one of the rememberers attached to great houses everywhere, **who are the
      record**)" (04:685).
    - The Kshalo gloss is spoken inside a guest's rumor (08:287). Move it to an italic DM aside.
    - "Let your table manner carry that, not those words: the hints below are how" (09:1806–1807).
    - "Minister Corval's and two ministers'", three times (02:291, 07:371, 09:157). It should read
      "Corval's and two other ministers'", and it only needs printing once.
20. *(Merged into 18.)*
21. **"Wept: east doors"** in Table VIII–6 (08:250). Table V–6 says "the east wing doors". These
    are different doors, 60 feet and a stair apart.
22. **The forced-wing rule contradicts the midnight post.** "The east wing stays doubled for the
    rest of the night" (04:79–81), against Table VIII–7's "Two, who stay" at midnight. Add "until
    midnight".
23. **An unlabelled box:** 04:574 ("> Undercurrents A, B and D are marked…") has no species.
    Make it a DM Note, or put it in the italic reading note.
24. **S4 in Movement V:** four guards stand on the doors (Table VIII–7), but S4 fields "Two
    Boranis Honor Guards" and calls four more. Say "two of the four engage; the other two hold
    the doors".
25. **S10's box shows two slingers, but the Enemies line counts three.** The box has the one
    "watching the corner" standing under the window (09:1427–1431); the Enemies line adds "the one
    at the corner" (09:1448–1450). Put the third in the box.
26. **S11 at five characters:** "the door they picked is narrower than it looks" (09:1570), but
    the card fixes it at 5 feet wide (09:1538). Say "jammed half-open".
27. **The natural 20 on a distraction while Idle is undefined** (09:1855: "as succeeding by 5 or
    more", which does nothing while Idle). Say what it does.
28. **The Prickle still doesn't say whether it cancels an unseen attacker's Advantage**
    (03:110–111). This was flagged last time. Add "It doesn't stop the attacker having
    Advantage."
29. **Block-level Nastier lines now point at the card baselines.** The Bought Sergeant points to
    the Veteran (10:673), the Draunel Duelist to the Veteran (10:894–895), and the Cousin's Blade
    to 3160 (10:374–375). This is harmless, but it is the P1-7 confusion in miniature: a DM
    reading chapter X sees the baseline roster offered as "harder". Give each base block its own
    dial.
30. **A clumsy citation:** "(…; see chapter V, 'The Palace After Midnight: General Features';
    see map VIII–3.)" (04:237–239). The same double "see" recurs at 04:269–271 and 04:357–358.
    Use one "see".

---

## 6. The three readers

**The DM on Friday.** The prep box, the DM sheet, Table VIII–7 and the Midnight Clock now let me
run the night from four pages, and I never had to reconcile two numbers to do it. That is the
main achievement of this pass. Where I still got stuck:
- S8's warden inside the locked room (N2).
- Which sergeant block to run (N5).
- How guests get up to the galleries where the toast happens (N4).
- What "the gallery doors" in S13's trigger are (N4).
- Whether the S10 window is reachable (N4).
- The maps answered most spatial questions, then undercut themselves with "?" and "drawn
  plausibly" (N3).

**The rules lawyer.**
- The block and pregen arithmetic is correct throughout, the three new blocks included:
  - *Veteran Bought Sergeant:* 78 (12d8+24), three attacks at +5 for 7, CR 4. That is a slight
    over-rating, which is safe.
  - *Veteran Draunel Duelist:* 44, two Rapier attacks and Provocation at DC 12, CR 2.
  - *Boranis Cousin of 3160:* 33, two Longsword attacks, CR 1.
- Every card budget re-derives, every scaling line included, against SRD 5.2.1 (Table IX–1 is
  right).
- The S14 rewrite is sound in its Focused half. Its Idle "furniture" half is exploitable (N1).
- The grapple fix (Table V–5 row 6) is correct 5.2.1. *Hold the Terms* and *To the Terms* read
  cleanly.
- Vell is unchanged and fine. He is over-built but not exploitable.
- The open questions: N1, N2, N6 (*Provocation* and S9's clock against the 3160 cousins), N10
  (the outer stair), N27 (the natural 20) and N28 (the Prickle).

**The editor.**
- The read-aloud is still the best thing in the book.
- The DM prose is now consistent in format and mostly human in voice, though the joins lean on
  colons (N17).
- The layout is close to house standard.
- Three things still say "work in progress":
  - the maps' hedges and decision IDs (N3, N12);
  - the designer's derivations in S14 and Vell (N18);
  - two bolted-on glosses (N19).

---

## 7. Challenges to the Planner's decisions

- **O32 (S14: an Idle success makes the distractor "furniture").** The intent is right: an Idle
  success shouldn't count toward the four. But "for the rest of the scene… as if it had never
  interfered" creates an immunity (N1). Recommend: the Idle success is simply wasted, or the
  furniture status ends when that creature next interferes.
- **The QR3 application (the four-warden roster in S8).** The ruling is owner-decided and stands.
  The application broke the card (N2): a fourth body was added where the card's logic had no
  room for one.
- **O53–O56 (the map choices).** The choices are sound. Printing their IDs and their doubts on
  the maps is not (N3). The doubts should have been decided, as O33 decided the wing's floor.
- **O36 (one home per rule).** Right, but applied to "Down, Not Out" only. Extend it to the
  Fracture rule (N8), with a fact-checker entry.
- **O39 and the tic targets.** Hitting every target exactly suggests the edit chased the metric.
  The next voice pass should be judged by ear, not by count (N17).

---

## 8. Where the tooling still gives false confidence

1. `fact_check` has no entry for "second floor" against "gallery level", for S10's 20-foot wall,
   for the walk drop or for gallery access, so N4 passes.
2. `test_maps.py` checks that the drawn shapes match `facts.yaml`. Nothing checks map labels for
   scaffolding: O-numbers, "?", "not given", "approximate", "plausibly" (N3).
3. The `rule_copy` check exists only for "Down, Not Out" (N8).
4. `defined_terms` checks only the listed terms, and Svara and Namak-Zai are not listed (N14).
5. The "(X or Y)" rule misses three-way lists (N15).
6. `bestiary_check` verifies blocks, not the blocks that cards and dossiers point to (N5), and
   not trait or action text whose conditions key on another block's name (N6).
7. Nothing checks a card's roster against its own clock and terrain logic (N2).

---

## 9. What 9 or above would need

1. Fix the three P1s: the furniture exit clause (N1), the S8 fourth warden (N2), and the map
   scaffolding stripped and the open values decided (N3, N12).
2. Close the geometry residue: one name for each level, S10's wall, the walk drop, gallery stairs
   and doors on map VIII–3 (N4), and the S3 outer stair (N10).
3. Fix the pointers and identities left by the new blocks: the sergeant (N5), the cousins (N6),
   S1's Nastier (N7), and the Radiant's orphaned paragraph (N9).
4. Give the Fracture rule one home (N8).
5. Draw a real overview map that places every public room (N11).
6. A short human line-edit for the colon splices, the designer commentary and the garbled glosses
   (N17–N19). Then run the remaining P3s.

With items 1–4 done, this is an 8.5–9 book. Item 5 and a human ear on item 6 are what separate
it from an official one.

---

## Resolution

*2026-10-10, R6.2 fix pass (Worker). Decisions O60–O66 in `docs/DECISIONS.md`; INVENTIONS #87;
log in `docs/LOG_oraga_5e_official_audit.md`, "Review-fix pass — R6.2 fixes".*

| Finding | Status | How |
|---|---|---|
| **N1** (P1) furniture exploit | **Fixed** | O60: furniture lasts until that creature next attacks the Attendant or interferes with one of the three; furniture doesn't stop *Clears the Way*. 10, 09 S14, 05, 08, flow.json agree |
| **N2** (P1) S8 warden inside | **Fixed** | O61: the fourth warden comes up the stair on the clock's third segment; scaling lines updated |
| **N3** (P1) map scaffolding | **Fixed** (labels, captions, chapter VIII frame) · **open** (deciding the walk drop, room order and run route as design facts; folded into N4) | O62: no decision IDs, "?", "not given", "plausibly" on any map; one caption line each; "Rooms shown by connection"; PNG links moved to README; `test_maps.py` guards it |
| **N4** geometry gaps | **Open** (owner) | Second floor vs gallery level, S10's wall, the walk drop, gallery access |
| **N5** wrong sergeant | **Fixed** | O66: 05 and 07 ×2 name the Veteran Bought Sergeant |
| **N6** cousins muddle | **Fixed** | O63: one set of cousins, one block per card; *Provocation* and the circle clock key on "a Boranis cousin (either block)" |
| **N7** S1 Nastier as base | **Fixed** | O65: "Variant: the principal" line (CR 1/8); S1 225 XP; a real Nastier line; bestiary_check checks the variant |
| **N8** Fracture rule twice | **Fixed** | O64: chapter X is a pointer plus its DCs; `fracture_rule` rule_copy in facts.yaml |
| **N9** Radiant's orphaned paragraph | **Fixed** | O66: moved into *Fracture — Devotion* |
| **N10** S3 outer stair | **Fixed** | O66: both gatehouse stairs ladder-steep and one body wide |
| **N11** overview flowchart | **Open** (owner) | Redraw VIII–1 as a true plan |
| **N12** map frame | **Fixed** | Folded into N3: chapter VIII's frame is two sentences |
| P3 13–16, 18, 19, 21–28, 30 | **Open** | Owner and the human line-edit (N17–N19) |
| P3 17 colon splices | **Open** | Human line-edit, judged by ear |
| P3 29 block Nastier lines | **Partly** | The kinsmen's Nastier is its own dial now (O65); the sergeant, duelist and cousin base blocks still point to their veterans |

**Checks after the fixes:** lint --check OK; fact_check --check OK (0); bestiary_check 28 blocks +
1 variant line, 0 mismatches; pregen_check 0; copyright_scan (c) 0; pytest tools 422 passed;
flow page rebuilt.
