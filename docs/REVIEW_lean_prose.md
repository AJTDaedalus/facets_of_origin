# Review: Lean Facets v1.0: Prose, Canon and Licensing

Branch `feat/lean-facets`, reviewed 2026-09-26 against tag `pre-lean-facets`. Read-only review: no book or code was edited.

**Scope.** Prose quality, canon (the iron law), and copyright/licensing across the PHB, MM Manual, Bestiary, Oraga Night, Val'loh and `software/facets/base/tables.yaml`.

**How this file is laid out.**
- Part 1 is the consolidated, severity-ranked list.
- Part 2 holds my own detailed notes on the core PHB chapters and MM1.
- Appendices A–C are the full specialist reports, with every quote and rewrite: A covers tables, MM6, the Bestiary and MM2–4; B covers canon plus the Oraga and Val'loh voice; C covers copyright. Their finding IDs (O-1, V-1 and so on) are cited in Part 1.

Line numbers are for HEAD at review time.

---

## Part 0: Verdict in brief

- **The rebuilt rules prose (PHB, MM1–MM6) is mostly clean and human.** It averages 0.3–3 em-dashes per 1,000 words, down from roughly 10–20 before, with short declarative rules and few hedges. The cast vignettes are the best writing in the PHB. The problems are elsewhere:
  - **Wrong arithmetic in MM1.** Its worked examples use the wrong monster-damage row (Critical).
  - **Stock taglines, repeated.** "That is the whole of X" appears 8 times, and there are aphoristic closers and "not X; it is Y" constructions.
  - **Duplicated scenes and sidebars.** Quick Start retells the II.3 vignette. III.3 and MM1 carry the same Through-the-Mirror sidebar. MM6 repeats MM2.
- **The untouched or lightly touched material is AI-textured.** This is the Bestiary lore, Oraga Night 04–05 (unchanged since the tag) and Val'loh. It runs 10–25 em-dashes per 1,000 words, with frequent not-X-it's-Y constructions and templated paragraphs (all ten Bestiary *Adaptation* paragraphs share one shape). It also has two lines that must never reach print: `CLAUDE.md` cited in the Bestiary front matter, and a dev in-joke in the chicken entry.
- **Canon.** The lean pass invented almost no new lore. All of its new names are logged in the INVENTIONS files. But it made one owner ruling worse: the Uninvited are called "it", though the owner ruled they are human, he/she. It also leaves several older breaks unlisted, including a Val'loh "by letter" line in a world with no letters and a contradiction in the Oraga testament witnesses.
- **Licensing.** No Critical infringement: no copied paragraphs, stat blocks, table entries or D&D Product Identity. But the Credits page is inaccurate:
  - It claims "none of their text appears here", yet III.1:169 has two Dungeon World GM-move phrases word for word.
  - It credits the wrong source for Fatigue-in-slots and for knacks.
  - It names a 13th Age mechanic the game doesn't have.
  - It omits Blades in the Dark (clocks, Borrowed Trouble), OSE/B/X (morale, reaction, exploration turns), Ironsworn (the oracle pairing) and the safety-tool authors.
  - "NASTIER" is 13th Age's label.
- **`tables.yaml`** is the strongest writing in the set: about 14 of 22 tables and about 75% of entries are strong. The weak ones are Fight Complications, Exploration Complications and NPC Wants. One entry is circular and unplayable (fight 24).

**Counts (consolidated, de-duplicated):** Critical 7 · Major 29 · Minor ~55 · Nit ~20. The appendices carry the long tail of Minor and Nit items individually.

---

## Part 1: Consolidated findings, severity-ranked

### Critical

| # | Where | Quote / problem | Remedy |
|---|---|---|---|
| C1 | `mm_manual/MM1_Encounters_and_Enemies.md:93` | "a level 3 foe that hits deals 4". Table MM1–1 and `facet.yaml:1034` say level 3 deals **6**. | "a level 3 foe that hits deals 6" |
| C2 | `MM1:108` | "Five Mooks at level 2 roll once at +0 and deal 2 + 4 = 6 on a hit. When three of them are down, the survivors deal 2 + 1 = 3." The level 2 base is 5, and the Mook −1 makes it 4. | "…deal 4 + 4 = 8 on a hit. When three of them are down, the two survivors deal 4 + 1 = 5." |
| C3 | `MM1:288–290` (Toll Ogre example) | The ogre's damage is used as 4, but the card printed 40 lines earlier says **Damage 6**. It is also misread against its own level. The example teaches every new MM the wrong number. | "a hard hit, 6 + 2 = 8 damage. Mordai's heavy armor and shield stop 3, so he takes 5. … It deals 6, and Zahna's light armor stops 1. Zahna takes 5 and is on 1 of his 6 HP." Adjust the MM line: "…you're bruised badly, and you're very aware of the river." |
| C4 | `bestiary/Front_Matter.md:19` | "The project's copyright policy is in `CLAUDE.md`; this book is written to it." A printed book cites an AI-assistant config file. The same paragraph also claims nothing is "mechanically modelled on any proprietary bestiary", which "NASTIER" (13th Age) contradicts. | Replace the sentence with: "Facets of Origin is released under GPLv3, and nothing in this book is licensed from anyone else." Soften "mechanically modelled" per Appendix C. |
| C5 | `bestiary/B1_Beasts_and_Vermin.md:303` | "Three chickens are no danger to anyone… So are five. Seven chickens … will genuinely hurt somebody, which is a sentence this project has had to live with since March." This is a dev in-joke plus a grammar error. | "Three chickens are no danger to anyone. Nor are five. Seven, attacking as one mob, will genuinely hurt somebody, and you should let the table find that out." |
| C6 | `settings/valloh/V1_Lineages.md:103` (V-1) | "a Kshalo most people would rather consult by letter". This is player-facing, and Val'loh bans the written word (U8/U10). | "…a Kshalo most people would rather consult through a go-between." |
| C7 | All ten Bestiary *Adaptation* paragraphs (B1:97, 191, 250; B2:129, 255, 316; B3:165; B4:70, 140, 174) | One template ten times: "Keep A, keep B, and keep C. A [creature] that [breaks it] is [not this entry; it is a war / a riddle / …]." This is the most machine-made texture in the line, and it is exactly the "uniform texture" tell the style guide bans. | Vary the form. Some become a bare reskin list, some a single "keep" clause, and at most two or three keep the kicker. Rewrites are in Appendix A §4c. |

### Major: prose and structure

| # | Where | Quote / problem | Remedy |
|---|---|---|---|
| M1 | `player_handbook/Quick_Start.md:89–121` vs `II.3_Magic.md:136–184` | "The Three Tiers in Play" re-tells the II.3 vignette almost beat for beat: the sealed glyph door, Zahna reads it on a 10, Mordai forces it at Hard for an 8, "someone wrote a locking instruction". A reader meets the same scene twice in the first forty pages. | Give Quick Start a fresh scene that shows the three tiers on one problem nobody reuses. One option: crossing a flooded ford (Mordai hauls the cart for a 10; Zahna calculates the current for an 8 and his notes get soaked; Zulnut fails a 6 and turns it into a Graceful Fail). Alternatively, cut II.3's first two rolls and let II.3 open where Quick Start stops. |
| M2 | "That is the whole of…" tagline, eight times: `Quick_Start.md:11`, `II.3_Magic.md:5`, `IV.1_Equipment.md:13`, `I_Introduction.md:9` ("the whole shape of it … That is the entire activity"), `oraga_night/01:283`, `03:15`, `07:449`, `bestiary/B1:92` | A stock closer that reads as a generated tic once you have seen it twice. | Keep at most one, in Quick Start. Rewrites: II.3:5 "A domain says where you can reach…" (drop the lead sentence). IV.1:13 "There are no weights and no speed penalties: if it fits in your slots, you can carry it." Intro:9 end at "…when the outcome is genuinely uncertain." |
| M3 | `I_Introduction.md:5` (the book's first sentence after the title) | "Not rules-first stories, not combat-first stories — stories about characters you care about, worlds worth exploring, and moments you'll still be talking about years later." This is a "not X, not Y — Z" frame followed by a triplet. | "Facets of Origin is a tabletop roleplaying game about friends telling a story together, and about the characters, places and nights you'll still be arguing about years later." |
| M4 | `I_Introduction.md:15` vs `:47` | L15 says the story is "the only thing that actually matters". L47 says "The most important thing … is the people at your table." These are two "most important" claims in one chapter, the first inflated. L7 and L9 also both lean on "genuinely". | L15: "…so you can keep your attention on the story." Keep L47. |
| M5 | `I_Introduction.md:19, :35`; `II.5_Lineage.md:3`; `settings/valloh/V0_Ten_Things.md:13` | "The rules are a framework, not a ceiling." "It is an invitation, not an obligation." "…that is not a limitation; it is the setting saying something." "That register is not decoration; it is where the Sparks are." The negative-parallel construction recurs in every opener. | L19: cut the sentence. L35: "You don't have to play in Shattered Origin." II.5:3: "In Shattered Origin that is a choice the setting made on purpose." V0:13: "That register is also where the Sparks come from." |
| M6 | `III.3_Combat.md:75–79` vs `MM1:254–256` | The same "why the enemies/foes roll" Through the Mirror box appears twice, with the same argument, the same "earlier version" origin and the same gasp-at-the-dice image. The style guide says to teach twice and legislate once. | Keep the III.3 box. Cut MM1's, or make it MM-specific: "the dice take the blame off you". Most of that point is already at MM1:252. |
| M7 | `III.3_Combat.md:174` (Archive Guardian read-out) | "It has the proportions of a person and the material certainty of a vault. It takes one step toward you. The floor doesn't shake. It doesn't need to." The closer is an overwritten AI beat in the PHB's flagship vignette. | "…It has the proportions of a person and the build of a vault door. It takes one step toward you, and the floor takes the weight without a sound." |
| M8 | `III.3:176` | A 90-word italic parenthesis carries the MM's whole scaling calculation. Per phb-examples.md, italics are the fiction's outcomes and parentheses are the MM's human asides, so this mixes both registers and buries a rule-of-thumb inside a joke ("never fought anything bigger than a chicken"). | Move it to a boxed **MM Note — scaling a Boss down** before the vignette. Leave a one-line aside in the scene: "(The MM has quietly shrunk this thing to fit a level 1 party. It is still going to hurt.)" |
| M9 | `II.4_Character_Creation_Facets.md:55` vs `:89` and `II.6:225` | The rule says "'Fighting' and 'sneaking' are not knacks … A good knack fits about one roll in four". Two paragraphs later the book's model custom build takes the knack *Sleight of hand and quiet feet*, which is sneaking plus stealing. The model example breaks the rule on the same page. | Give Zulnut a narrow knack: *Rooftops and back doors*, or *Temple-yard acrobatics*. Propagate to II.6:225, `characters/Zulnut.fof` and phb-examples.md in one pass. This needs the owner's OK, since it changes a cast fact. |
| M10 | MM6 vs MM2 (Appendix A §3) | "Stuck? Three Options", the Pressure die, the Trouble table and the 7–9 test repeat MM2 near-verbatim, down to the same closing line. The relics text repeats MM3. The morale triggers are restated in five places. | MM6 keeps the tables and procedures. MM2 and MM3 keep the advice and point into MM6 by table designation. |
| M11 | MM4 Philosophy opener (L5–9) and *Growing as an MM* (L267–279); MM2:74 | This is the densest cluster of "isn't X. It's Y." and aphorisms in the MM. "Situations, not scripts/plots" appears three times across MM2 and MM4. | Rewrites are in Appendix A §5. |
| M12 | Bestiary lore voice (Appendix A §4) | Em-dashes run 10–16 per 1,000 words. A "They are not X. This is the thing people get wrong" opener recurs. There is self-praise ("one of the best things this system does"). Spelling is mixed British/US within one book (harbour/behaviour/armour/colour/grey/centre against Armor/Harbor). | Run a dash pass to a target of 3 per 1,000 or fewer. Cut the self-praise. Pick US spelling to match the PHB. Mixed spelling also appears in Oraga 04, 05, 07, 08, 09 and in Val'loh V3. |
| M13 | Oraga Night 04 and 05 (Appendix B §prose) | These are unchanged since the tag, at 19.7 and 21.7 em-dashes per 1,000 words, with 7 and 9 "not X — it's Y" constructions. 04 has four duplicated passages, including two near-identical read-aloud boxes for the first sight of the hill. The 05 epilogue box tells the PCs what they know and dream, which breaks the module's own read-aloud rule. | Appendix B gives about 35 quoted rewrites. Minimum: merge the duplicate hill boxes, rewrite the epilogue box in perception verbs only, and make a dash pass. |
| M14 | Val'loh (Appendix B) | The "What It Adds, Counted" box is printed verbatim in both V0 and V4. V1 uses the same either/or quip four times and prints one gift-domain sentence nine times. | Keep the box in V0 and point to it from V4. Hoist the gift-domain sentence into the Reading the Entries legend. |
| M15 | `software/facets/base/tables.yaml`, complications_fight:24 | "You overreach: you're exposed, exactly as if you'd rolled 7-9." This table is rolled *on* a 7–9, so the entry is circular and unplayable. | "You overreach and stumble past it; now it's between you and your friends." Appendix A §2c has 15 more replacements (fight 13/64, explore 12/44/61, social 51, npc_wants 45/51/64, secrets 17, relic quirks 11/17, and others). |

### Major: canon

| # | Where | Problem | Remedy |
|---|---|---|---|
| K1 | `enemies/the_wept.fof:16–55` and the other Uninvited cards; `oraga_night/05` mixed (O-2) | The lean card lines call the Uninvited "it" throughout (18 → 27 uses in the Wept card). The owner ruled they are human, she/he ([private canon notes], "Later rulings"). The lean pass made this worse. | Replace "it" with she or he per card. Rewrites are in Appendix B. If the Bestiary house style needs "it", add an Oraga exception to the card `notes`. |
| K2 | `enemies/bought_captain.fof` generated TWISTS (O-1) | "The Second Clause is to take the party alive…", "…voids the contract if the employer lied" and "The employer has come onto the field" contradict inventions 4.2 and 4.3. | Add an Oraga reroll note to the card. The TWISTS must match the Bestiary under INV-18, so don't hand-edit the generated block. |
| K3 | `oraga_night/01_Overture.md:5–8` vs `04_The_Ball.md:506–508`, `06:71`, `07:132` | The opening vignette has "two witnesses who were paid not to remember it … neither of the witnesses has been seen since Tuesday", and a notary who "wrote what he was told to write". Chapters 04, 06 and 07 say the testament was sworn aloud with **Corval and Mother Sella** standing witness, and both are at the ball. "Tuesday" also imports a real-world weekday. The line predates the lean pass, but the module contradicts itself on page one. | "…swore a testament aloud before his majordomo and a lay-sister of Elanna. It took eleven minutes. Neither of them has repeated a word of it." This drops the notary, which also removes writing from the scene. |
| K4 | `V0_Ten_Things.md:35` (V-2) | "the four people in five who were born without a gift" comes three lines after "four in five Orthaen are born able to grow crystal". It reads as a contradiction even if it means the whole population. | "…including everyone born without a gift, and the visitors born without a tribe." |
| K5 | `V3_Rekuzan_and_the_Tribes.md:90` (V-3) | "the **Chiefs' Concourse**" is a named place that is in neither canon nor either INVENTIONS file. | List it for the owner, or write "the chiefs' hall". |
| K6 | `oraga_night/04:274` (O-6) | Effects "labelled in a hand". That is writing, against U8/U10. | "…each marked with a cord-knot in the house pattern". |
| K7 | `bestiary/B3_The_Made.md:141` (B-1); `bestiary/Front_Matter.md:33` | The Guardian's guild "has since dissolved … along with every record" settles the open Artificers' Guild ruling (T6) in print. The front matter also calls the Guardian "canon" in a book that is setting-agnostic by rule. | Cut the dissolution clause: "the body that commissioned it is not what it was". Change FM:33 to "the one creature the PHB's example party has already met". Both need an owner ruling. |

### Major: licensing (details and replacement Credits text in Appendix C)

| # | Where | Problem | Remedy |
|---|---|---|---|
| L1 | `III.1_Core_Resolution.md:169` | "reveals an unwelcome truth, or puts someone in a spot" is Dungeon World GM-move wording, verbatim. That makes Front_Matter:57 ("none of their text appears here") untrue. Related: "the MM makes a move" (III.1:169, III.3:37, :47, QS:128) is DW's signature phrase. | "The MM answers: a new danger arrives, something is lost, the truth turns out worse, or someone is left somewhere bad." Consider "the MM answers" in place of "makes a move" book-wide. |
| L2 | `player_handbook/Front_Matter.md` Credits | The Whitehack line credits HP-cost casting, but FoO charges Fatigue in slots, which is Cairn's mechanic, and Cairn isn't credited for it. "Knacks" are unverified as Whitehack's (its term is "groups"). The 13th Age line credits "one unique thing", which the game doesn't have. Blades (clocks, Borrowed Trouble ≈ Devil's Bargain), B/X/OSE (morale, reaction, exploration turns), Ironsworn (the action/theme oracle), Justin Alexander (the Three Clue Rule, by name) and the safety-tool creators (Stavropoulos: X-Card; Edwards: lines and veils; Quade: stars and wishes) are all missing. | Replace the section with the corrected Credits in Appendix C §5. It adds a trademark notice (Morrowind etc.) and a rule on which licenses may be *incorporated* versus only drawn on for ideas. OGL and CC BY 3.0 material is ideas-only for a GPLv3 book. |
| L3 | `NASTIER` field, 17 Bestiary cards and a `.fof` key | This is 13th Age's "Nastier Specials" label. | Rename it (for example **REMATCH** or **HARDER**) in the cards, the MM1 legend (MM1:35), the generator and the tests. It needs a software change, not just a books change. |
| L4 | Bestiary and MM Manual | Neither has a credits page, though the BRIEF promised one for the MM. | Add a short acknowledgements block to each that points to the PHB credits and names the MM-specific debts (Alexandrian, Sly Flourish, Necropraxis, the safety tools). |
| L5 | `II.4_Character_Creation_Facets.md:113–117` | The end-of-session questions ("Did we discover something new about the world? … Did we bring treasure home?") closely paraphrase Dungeon World's End of Session questions. Rated Minor in Appendix C, but it is load-bearing for the Credits claim. | Credit DW for the idea, and reword so the questions are ours: "What did we find out that we didn't know? What came home in our packs? Who went after what they wanted? What's different out there now? What will we still be talking about next week?" |

### Minor (selected; the rest are in the appendices)

- `Quick_Start.md:71–85` vs `:93–119`: two vignettes in one file use two formats. The first uses "**Mordai's player:**" in a box with no quotes; the second uses "**Zahna:**" with quotes, unboxed. phb-examples.md specifies `CharacterName:`. Use `Mordai:` throughout, and keep the out-of-character sheet talk as the player's line only where it really is out of character.
- `Quick_Start.md:109`: "(A 7–9 is a success with a price. The MM names the price.)" A rules gloss sits inside an MM-aside parenthesis. Move it outside, as plain text, like the Graceful Fail line at :121.
- `Quick_Start.md:17`: "They are ready-made, they are balanced against each other, and every one of them is a fine first character." This is rule-of-three. Change it to: "They're ready-made and balanced against each other; any one is a fine first character."
- `Quick_Start.md:25–29` / `II.4:23`: the "Solves problems by" column is ungrammatical ("moving the people around them, or by luck"). "people who solve problems by…" is also repeated as a triplet in II.4:23 and II.4a:3. Change the Soul row to "moving people, or trusting luck".
- `II.4:25`: "The Body pays for its big grit die by having no magic. The Mind pays for…" sets up a three-way pattern and drops Soul. Add "The Soul pays for its luck with a middling die and a smaller menu of sure things," or cut both sentences.
- `II.4:41`, `II.4:119`: "That's it." and "Notice what is missing. … The game rewards the things it is about." These are stock closers. Cut both second sentences.
- `II.2_Character_Creation_Stats.md:83`: Zulnut asks for "The brass key. Lower archives." The MM's narration seeded a *keyring*, not a brass key or the lower archives. That breaks the ground rule, and it clashes with :95 ("several keys, none labeled"). Change to: "**Zulnut:** 'The keyring.'"
- `II.2:87`: "**Another player:** 'Spark?'" Name the player, for example "**Zahna:** 'Spark?'", which also shows Zahna noticing something social for once.
- `III.3:280` "Not out. Dimmed." is a fragment tic. Use: "…and the light in its eyes goes down to an ember." `III.3:292` "It is extremely on brand." is off-register slang. Use: "(The MM has been waiting all fight for Zahna to say something like this.)"
- `III.3:284`, `II.3:184`: stage directions in italic parentheses ("*(still on its back)*"). Parentheses are reserved for the MM's asides. Write "**Zulnut**, still on its back:" instead.
- `III.2_Adventuring.md:148`: "I want to be precise here, because this is the one moment where precision matters most." This is inflated. Use: "Listen carefully, because this is the part that's yours to decide." `:158` "It's permanent, and it's true." Cut "and it's true".
- `III.2:77`: three rolls are compressed into one italic sentence with no roller named ("The valve wheel is seized, a failure…"). Name who rolled each.
- `MM1:278`: Mordai's longsword "deals 1d8". *Weapon Master* makes it a d10 (QS:81, III.3:200). Change to 1d10 and recompute.
- `MM1:276–292`: the Toll Ogre example drops bold on `MM:` and switches to narrated rolls. Match the III.3 format.
- `MM1:126`, `:252`: "isn't in a fight. It's in trouble" and "does something your players will feel before they can name it". These are mild tells. Keep the first and cut the second.
- `II.6:9`: "the life that shaped you: the work you did, the world you moved through, the people who shaped you." It uses "shaped you" twice and is a triplet. Change to: "the life you had before: the work, the places, the people."
- `I_Introduction.md:25`: "These fundamentals work for any genre and any tone" contradicts L11's "familiar if you have played older fantasy games". Change to: "…are built to carry other genres through Facets."
- `I_Introduction.md:33`: "This handbook gives you enough of the world to start playing today." The v1 PHB carries almost no Shattered Origin content, since II.5 says only that humans are the default. Change to: "…The setting Facet is forthcoming; until then, Oraga Night and your own table will fill it in." Or name what the PHB actually gives you.
- The Oraga and Val'loh minors from Appendix B: "history books" (05:126); "mask of a dead Uninvited" (05:454), though they cannot be killed; "forty blades" against a company of 21 (05:474); unlisted falconry mews (04:809) and "the Just One" (05:284); the unconfirmed Ulan→apostate line stated as fact (05:175–177); "three cities" (V1:31); V2 contradicting itself on whether releasing a charge takes a roll; tavva.fof:38 "festival hiring list" (a written list); and 01:260 pointing to an MM6 social table that includes "It's written down somewhere…", which is wrong for Val'loh.
- Credits and licensing minors (Appendix C): six talent names coincide with D&D 5e feat names (Sentinel, Tough, Weapon Master, Athlete, Lucky, Linguist). The mechanics are original, and short names aren't copyrightable, but *Sentinel* and *Weapon Master* are worth renaming for distance. The README doesn't point to the acknowledgements.

### Nits

- `III.1:13`: the "6−" row reads "Things go wrong | Things go wrong, but…". Drop the repetition.
- `II.4a`: the Brawler class takes a talent also called *Brawler*. Rename the talent (for example *Street Fists*).
- `MM2:454`: "*City Watch*" should be *City Watch Veteran*.
- `I_Introduction.md:45`: the dice list omits the extra d6 needed for Mind grit. Harmless, since you have 2d6.
- `MM2:9`, `MM3:9`: repo paths (`adventures/oraga_night/`) are printed in the book text. Use the title.

---

## Part 2: Detailed notes on the deep-read chapters (mine)

**Quick_Start: B+.**
- It is tight, playable and warm. The character-in-ten-minutes box is the right idea, and the MM aside "(It means I will be enjoying the library scene.)" is exactly the house voice.
- Problems: the glyph-door duplication (M1), the two vignette formats, the rules-in-an-aside at :109, and "the MM makes a move" (L1). The arithmetic checks out: HP 16, 12 slots with 6 filled, armor 3.

**I_Introduction: C+.**
- This is the chapter that carried the most pre-lean AI texture forward: M3, M4, M5, the "entire activity / refinement" tagline, and "genuinely" twice.
- The lean pass added two good paragraphs (L11 on what's familiar and what's ours; L29 on the second meaning of Facet), and the new *Playing Without Software* is concrete and useful.
- It is the first prose a reader meets, so it deserves one human rewrite pass. About 150 words would change.

**II.4: B+.**
- The clearest chapter in the book. "The Facet Owns the Numbers" is a strong organizing idea, well stated.
- The Zulnut custom-class box is funny and in voice ("the Brawler is far too keen"; "the only thing he enjoys more than not fighting is climbing away from a fight"; "(That is going to be a problem for me for years.)"). Its knack breaks the rule on the same page (M9).
- The session-end questions track Dungeon World too closely (L5). The two stock closers are listed in Minor.

**III.3: A− for the rules, B+ for the vignette.**
- The rules text is the best in the line: short, declarative, and each table carries one lookup.
- The Archive Guardian vignette does work: a failed roll with consequences (the lost knife), MM rulings said aloud, and a lateral ending ("not every fight ends at zero").
- The arithmetic is correct end to end. I checked every hit: 32→23→20→11, Mordai 16→15→12→8, Zulnut 12→7.
- The cast is in voice. Zulnut's "I'd like it noted that I was going to stop stabbing it anyway" and "I have no knife, seven hit points, and no interest" are good. So is Zahna's "A hinge is just a door that doesn't know it."
- Flaws: the overwritten opening read-out (M7), the rules digression in an italic parenthesis (M8), "Not out. Dimmed.", "extremely on brand", and the stage-direction parentheses.
- Canon: "fifteen years" and "commissioned by the city" were both already there at the tag, and the Artificers' Guild is correctly unnamed.

**MM1: B− (would be B+ without C1–C3).**
- The monster card is excellent design writing. The Toll Ogre card is a model entry: WANTS, TELLS and six TWISTS that each make a different fight.
- The morale and reaction-roll sections are clear, and the "When in doubt, the easier fight" note is sound advice.
- The three arithmetic errors (C1–C3) all come from one slip: level 1 damage (4) was used for a level 3 foe. They are the most consequential finding in this review, because MM1 is where MMs learn the numbers.
- The duplicate "why the foes roll" box (M6) is the only structural issue.

**II.2 / II.3 / III.2 vignettes (sampled): B+ to A−.**
- The Millhaven archive, the sealed door and the Beam are the strongest cast writing in the line, and all of it is pre-lean text carried over well.
- The Beam respects and establishes the shoulder scar exactly as phb-examples.md records it.
- The two ground-rule slips are the unseeded "brass key" (II.2:83) and the II.2 vs III.1 double-telling of the archive-desk scene (Appendix B P-2). The owner should pick one version.

---

## Part 3: Grades

| Book | Grade | One-line reason |
|---|---|---|
| **Player's Handbook** | **B+** | The rules prose is clean and human and the vignettes are funny and correct. Held back by the Introduction's inherited tells, one duplicated vignette, a stock tagline, and a self-contradicting model knack. |
| **MM Manual** | **B−** | Strong design writing (the monster card, morale, the Toolbox tables). Wrong damage arithmetic in MM1's teaching examples, heavy MM2↔MM6 duplication, and MM4's aphorism clusters. |
| **Bestiary** | **B−** | The most voice and the best ideas per page. Also the heaviest AI texture, one ten-times template, mixed spelling, and two lines that must not print. |
| **Oraga Night** | **C+** | Rich and playable. Chapters 04–05 were never line-edited (≈20 dashes per 1,000 words, duplicated boxes), the "it"-for-Uninvited regression, and the testament contradiction on page one. |
| **Val'loh** | **B−** | A good pitch structure. A repeated box, repeated quips, a "by letter" line in a world with no letters, and one self-contradiction in the Ten Things. |
| **tables.yaml** | **B+** | About 75% of entries are strong. Three weak tables and one circular entry. |
| **Licensing hygiene** | **B** | No infringement found. The credits are inaccurate and incomplete, and one short DW phrase is verbatim. |

## Part 4: The five most important edits

1. **Fix MM1's monster-damage arithmetic** (C1–C3, plus the 1d8 longsword at MM1:278). It teaches wrong numbers. It is a 10-minute fix.
2. **Rewrite the Credits and remove the verbatim Dungeon World phrase** (L1–L5): fix III.1:169, replace the Front_Matter Credits with Appendix C §5, rename NASTIER, and add credits blocks to the MM Manual and Bestiary. At the same time, cut `CLAUDE.md` and the "since March" joke from the Bestiary (C4–C5).
3. **Put the Uninvited pronouns back to the owner's ruling and clear the writing-ban and witness breaks** (K1, K3, C6, K6, O-3), then add every remaining unlisted item (K5, the Oraga minors) to the INVENTIONS files for owner review. Get the owner's ruling on the B3 guild-dissolution line (K7).
4. **De-duplicate** by giving each scene or passage one home: the Quick Start and II.3 glyph door (M1); the III.3 and MM1 sidebar (M6); MM2 and MM6 (M10); V0 and V4's counted box (M14); Oraga 04's twin hill boxes (M13).
5. **One human line-edit pass on the untouched texture.** In priority order:
   - I_Introduction (M3–M5)
   - Bestiary Adaptations and dashes (C7, M12)
   - Oraga 04–05 (M13)
   - The "That is the whole of…" tagline (M2)

   Target: no more than 3 em-dashes per 1,000 words, at most one negative-parallel per chapter, and US spelling throughout.

---

# Appendix A — Tables, MM6, Bestiary, MM2–MM4 (specialist report)


Branch `feat/lean-facets`. Read-only review. Severity scale: **Critical** (would embarrass in print or is unusable), **Major**, **Minor**, **Nit**.
Stat blocks inside `<!-- statblock -->` markers and rendered tables inside `<!-- table -->` markers are generated. They are only treated as data here. Fixes to tables go in `software/facets/base/tables.yaml`, and fixes to cards go in `enemies/*.fof`.

---

### A·0. Headline

1. **The tables are the best writing in the set.** About 75% of entries are strong: specific, active, usable at the table in under five seconds. The weak ones cluster in three places: Fight Complications, Exploration Complications and NPC Wants. They fail by duplicating each other or by stating a bare mechanic, not by AI rhythm.
2. **MM6's prose is short and mostly clean.** Its ~10k words are about 85% rendered tables. The prose tells are aphoristic paragraph closers, and several passages repeat MM2 and MM3 almost word for word.
3. **The Bestiary is voicey and often very good.** It still has the heaviest AI texture in the set:
   - em-dashes at ~10–16 per 1,000 words of prose
   - the same Adaptation-paragraph template in all ten entries
   - a recurring "They are not X. This is the thing people get wrong" opener
   - self-praise ("one of the best things this system does")
   - a developer in-joke and a reference to `CLAUDE.md` that must not reach print.
4. **MM4 has the densest "isn't X. It's Y." / aphorism clusters** (Philosophy opener; *Growing as an MM*).
5. **Possible invented canon:** B3 says the Archive Guardian's commissioning guild "has since dissolved… along with every record." The canon source (`enemies/archive_guardian.fof`) says only "the Thornwall city government through the Artificers' Guild." It says nothing about dissolution, and the Guild's canon status is itself still an open ruling.

---

### A·1. Quantification

### 1a. Em-dash density (`grep -o '—'` vs `wc -w`)

| File | Words | Em-dashes | per 1k |
|---|---|---|---|
| MM1 | 4,862 | 10 | 2.1 |
| MM2 | 7,070 | 15 | 2.1 |
| MM3 | 4,704 | 3 | 0.6 |
| MM4 | 4,074 | 1 | 0.2 |
| MM5 | 1,530 | 1 | 0.7 |
| MM6 | 10,113 | 4 | 0.4 |
| B1 (whole file) | 3,883 | 45 | 11.6 |
| B2 (whole file) | 4,014 | 45 | 11.2 |
| B3 (whole file) | 2,463 | 25 | 10.2 |
| B4 (whole file) | 3,076 | 41 | 13.3 |
| Bestiary Front Matter | 1,634 | 2 | 1.2 |
| Finding_Aids (generated) | 1,045 | 7 | 6.7 |

**Bestiary hand-written prose only** (stat blocks stripped):

| File | Prose words | Em-dashes | per 1k | per 1k after removing the structural `**6−** —` lore-box dashes |
|---|---|---|---|---|
| B1 | 2,231 | 36 | 16.1 | ~10.8 |
| B2 | 2,099 | 35 | 16.7 | ~12.4 |
| B3 | 1,549 | 21 | 13.6 | ~9.7 |
| B4 | 2,448 | 39 | 15.9 | ~12.3 |

The MM chapters are already clean on dashes, so the MM line edits worked. The Bestiary never got that pass. Target for the Bestiary: ≤4 per 1k in running prose, leaving the lore-box and encounter-parenthetical dashes, which are structural.

### 1b. Pattern counts (grep -c / grep -o, whole file)

Columns: 1 = `isn't … — it's` · 2 = `not …, but` · 3 = `Here's` · 4 = `the point is/of` · 5 = `That's the` · 6 = `That's it./all./the whole` · 7 = sentence-initial `Not x` · 8 = `it's not / it isn't` · 9 = `never` · 10 = sentence-initial `Every` · 11 = `rather than` · 12 = `n't/not … . It's/They're/You're/That's` (two-sentence negative parallel) · 13 = `, not a/the X` inversions · 14 = `the whole/entire point/job/creature`

| File | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MM1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 6 | 4 | 3 | 2 | 7 | 1 |
| MM2 | 0 | 0 | 0 | 1 | 2 | 1 | 6 | 3 | 12 | 4 | 3 | 0 | 15 | 1 |
| MM3 | 0 | 1 | 0 | 0 | 1 | 1 | 2 | 0 | 6 | 7 | 4 | 1 | 11 | 1 |
| MM4 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 7 | 4 | 1 | **6** | **19** | 0 |
| MM5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| MM6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 14 | 5 | 1 | 0 | 6 | 1 |
| B1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 7 | 1 | 1 | 3 | 1 | 2 |
| B2 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 6 | 4 | 3 | 2 | 3 | 1 |
| B3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 3 | 1 | 0 |
| B4 | 0 | 2 | 0 | 0 | 1 | 1 | 2 | 0 | 11 | 0 | 1 | 2 | 3 | 2 |
| Front Matter | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 6 | 0 | 1 | 1 | 0 |

The literal "Here's the thing" / "isn't X — it's Y" forms are gone. What remains is the **two-sentence** version ("It isn't a flaw. It's the job."), plus `, not X` inversions. MM4 has the most of both.

**Tic words** across Bestiary and MM (B1 B2 B3 B4 FM MM2 MM3 MM4 MM6):
- "the entry": 3 3 1 **8** 3 0 0 0 1
- "whole": **8** 1 2 2 3 **6 7** 2 1
- "exactly": 6 1 2 2 0 4 0 2 **6**
- "genuinely": 1 **5** 0 3 1 2 0 0 0
- "worth": 3 **8** 2 0 3 4 **6** 1 2

**Recurring images:**
- "drawer": MM6 lines 3 and 878. This one is deliberate and fine.
- "furniture": MM2:114, Front Matter:27.
- "scenery": MM2:19 ("it isn't a hook, it's scenery") and MM3:71 ("they're scenery with a name").
- "is a story / is a number": MM3:183, MM6:741.
- "situations, not scripts/plots/problems": MM2:241 (heading), MM4:21, MM4:247 (as "problems, not scripts"), MM4:267 ("Steal situations, not stories").

---

### A·2. `software/facets/base/tables.yaml`: the Toolbox tables

### 2a. Verdict per table

| Table | Die | Verdict | Notes |
|---|---|---|---|
| reaction | 2d6 | Strong | 7–9 = Uncertain, which holds the 7 (16/36 = 44%). **2d6 weighting is correct.** |
| reaction_wants | d66 | Strong | Best social table. "To cross a name off a list, and one of the party's names is on it"; "To win an argument that has been going on for an hour". Overlap: 46 "To join the party" duplicates Social Complications 41 and 51. |
| pressure_generic | 1d6 | Adequate (by design) | Category glosses; it has to be generic. |
| pressure_underground | 1d6 | Strong | "Fresh scratches at knee height, and a draft that wasn't there a minute ago." |
| pressure_wild | 1d6 | Strong | 6 "the land shows the party something worth stopping for" is vague. |
| pressure_settlement | 1d6 | Strong | "the inn is full and its price is not." Face 3 is a four-item list. |
| pressure_occasion | 1d6 | Strong | Every face is a picture. |
| trouble | 1d6 | Adequate (by design) | An index of categories. Fine. |
| complications_fight | d66 | Mixed (~65% strong) | Duplicates and one circular entry (below). |
| complications_explore | d66 | Mixed (~65% strong) | Four usage-die entries (12, 26, 43, and 35 slots); several bland two-to-five-word entries. |
| complications_social | d66 | Strong (~85%) | "Their superior has to approve it, and their superior is in the room." Weak: 51 (dup), 65 (clever but hard to play). |
| magic_complications | 1d12 | Strong | Varied, all playable. |
| magic_mishaps | 1d12 | Good | 5 "Beacon" is vague ("everything within a long way"). 10 and 12 overlap with complications 9 and 10 (being noticed; the domain marks you). |
| wounds | 1d6 | Functional, samey by design | Every entry has the same shape: "X. [image]. Strained by A, B and C." The fixed shape is justified because it's a lookup, but it produces 6 of the file's 58 triplet lists. |
| scars | 1d12 | Strong | 2 is vague ("one thing you will never be able to lift again"). |
| trinkets | d66 | Strong (~85%) | "An IOU for twelve chickens"; "A folded note that says only: 'Not this one either.'" Bland: 43, 44, 61. |
| curios | 1d20 | Strong | Every entry is object + verb + effect. Very playable. |
| relics | 1d20 | Strong but samey quirks | **Three quirks are lie detectors:** 1 Patient Lantern, 11 Hospitable Kettle ("won't boil while anyone at the fire is lying"), 17 Weighing Stone ("grows heavy near lies about money"). Relic 11's quirk is also more useful than a quirk should be. |
| npc_names | d66 | Adequate | Runs alphabetically A–Y then A–L, a visible machine pattern. Heavy on nature names (Kestrel, Linnet, Lark, Juniper, Quill). Consider shuffling the order. |
| npc_traits | d66 | Strong | "Tall, stooped, and apologetic about the ceiling"; "Always slightly damp." |
| npc_wants | d66 | **Blandest table (~60% strong)** | Several are generic life goals with no hook (see 2c). |
| npc_secrets | 1d20 | Good | 17 is vague. 12 "They set the fire." is excellent. |
| oracle_actions / oracle_themes | d66 | Adequate | Component word lists. Fine as is. |

**Fractions (estimates):**
- **Tables:** 14 of 22 strong, 6 adequate or functional-by-design, 2 mixed. NPC Wants is weak-leaning.
- **Entries:** ~503 in all. Of the ~395 that are more than a single name or word, ~75% are strong, ~20% serviceable, ~5% weak (bland, duplicate, circular or vague).

**2d6 check:** only `reaction` uses 2d6, and its commonest band (7–9) contains 7, as the style guide requires. Everything else is flat (d6, d12, d20, d66). That's legal, but STYLE_GUIDE's "random tables weighted on the 2d6 curve" commitment is met by one table in 22 (Minor). A 2d6 Reaction Wants or Pressure variant is not needed. If you want a second weighted table, Wounds is the natural candidate: make the common wounds common.

### 2b. Samey structure and words

- **Triplet lists:** 58 of the ~395 prose entries (~15%) contain an "A, B(,) and/or C" list. Examples: "a supply, a favor, an opportunity" (trouble 1); "a lever, a hostage, a door" (fight 25); "a street, a kitchen, a stair" (fight 65); "a seal, a ward, a door" (mishap 11); "(a scorch, a frost, a sigil)" (complication 3); "(stone, ice, shelving)" (explore 56); "a goat, a dog, a hawk" (reaction_wants 34); and every Wounds entry. At one line per entry, this is the table-level rule-of-three tic. Cut about a third of them down to one concrete item. The single item is almost always stronger: "The foe backs toward the lever" beats "a lever, a hostage, a door".
- **Frequent content words** across entries: power 21 and quirk 20 (these are field labels), back 18, foe 16, **light 15**, **door 12**, **usage (die) 8+12**, hand 11, long 11, water 8, fire 7. "Door" appears in reaction_wants 44, pressure_settlement 5, fight 25, 44 and 64, explore 13 and 41, mishap 11, relic 3, and the oracle. It's worth varying two or three.
- **Near-duplicate entries across tables:**
  - "joins/follows the party": reaction_wants 46; social 41 and 51; npc_wants 41 ("To go adventuring, like the party")
  - "more foes arrive": fight 21 and 64; fight 13 and 41
  - "the way back closes": explore 13; pressure_underground 3
  - "take 1 damage": fight 46; explore 24; mishap 11 is also 1 damage ("It bites back")
  - "domain marks you": magic_complications 10; mishap 12
  - "wants the party gone": npc_wants 44 and 52

### 2c. Worst entries, with replacements

| # | Table:roll | Current | Problem | Replacement |
|---|---|---|---|---|
| 1 | complications_fight:24 | "You overreach: you're exposed, exactly as if you'd rolled 7-9." | **Unplayable/circular.** The table's use is "a cost for a 7-9", so on a 7–9 this entry says "as if you'd rolled 7–9". It's also a rule reference, not an event. | "You overreach and stumble past it; now it's between you and your friends." |
| 2 | complications_fight:64 | "One more Mook arrives at the door, on their side." | Duplicates 21; bland; "on their side" is redundant. | "Someone who was hiding under a table decides now is the moment, and picks their side." |
| 3 | complications_fight:13 | "A second foe turns toward you." | Duplicates 41; no picture. | "A second foe sees you're busy and circles to your blind side." |
| 4 | complications_explore:12 | "Roll a usage die now: light, rations or rope." | Bare mechanic; third usage-die entry. | "The rope frays on a sharp edge; roll its usage die, and someone is still on it." |
| 5 | complications_explore:44 | "You've been seen from a distance." | Bland, passive. | "A glint on the far ridge, then nothing: someone with a glass knows where you are." |
| 6 | complications_explore:61 | "Night falls sooner than planned." | Bland. | "The light goes early; the last stretch is done by feel, and someone has to go first." |
| 7 | complications_social:51 | "They want to come along." | Duplicates social 41 and reaction_wants 46. | "They'll do it, but only if their cousin comes too, and their cousin talks." |
| 8 | npc_wants:45 | "To build something that will outlast them." | Abstract life goal; no hook. | "To finish the bridge their mother started, one stone a week." |
| 9 | npc_wants:64 | "To become someone else entirely." | Abstract. | "To be taken for a noble, just once, at one particular dinner." |
| 10 | npc_wants:51 | "To win back someone they lost." | Generic. | "To win back the partner who left for the city with the good horse." |
| 11 | npc_secrets:17 | "Their family is not what it claims to be." | Vague; the MM has to invent the secret anyway. | "The family 'inheritance' was a payroll that never reached the soldiers it was owed to." |
| 12 | relics:11 (quirk) | "it won't boil while anyone at the fire is lying." | Third lie-detector quirk, and it's a power, not a drawback. | "Quirk: it always pours one cup short, and somebody has to go without." |
| 13 | relics:17 (quirk) | "it also grows heavy near lies about money." | Lie detector again. | "Quirk: it also grows heavy near anything its last owner hated, and it has no way to say what that was." |
| 14 | magic_mishaps:5 | "everything within a long way that is attuned to the domain knows where you are." | Vague range and actor. | "Beacon: for the rest of the scene, anything that feeds on or serves the domain can find you, and something already is." |
| 15 | scars:2 | "There is one thing you will never be able to lift again." | Vague; the MM can't act on it. | "A shoulder that set wrong. That arm won't go above your head: high shelves, climbing and surrendering are all awkward." |
| 16 | trinkets:43 | "A fish carved from bone." | Bland beside its neighbors. | "A bone fish, carved by somebody who had plainly never seen one." |

Also note:
- explore 52 ("use face 3 of its Pressure die") and explore 11 ("roll the Pressure die again") are fine but meta. Keep at most one.
- pressure_wild 6 "the land shows the party something worth stopping for" is vague. Try "a view of tomorrow's route, and a place worth camping."
- complications_social 65 "They're relieved you asked, which ought to worry you" is clever but leaves the MM to invent everything. Consider replacing it.

---

### A·3. `mm_manual/MM6_The_Toolbox.md` (prose only; tables are generated)

MM6 has ~1,500 words of prose. The rest is rendered tables. Em-dashes (0.4/1k) are fine. The tells are aphoristic closers and repetition of MM2 and MM3.

| Sev | Line | Quote | Issue | Rewrite |
|---|---|---|---|---|
| Major | 443–453 | Whole *Stuck? Three Options* section | **Near-verbatim duplicate of MM2:261–269.** Same three options, the same example list ("a letter, a slip of the tongue, … a dream") and the same closing line: MM2 "Don't pick the one that's most dramatic; pick the one that fits the room" vs MM6 "Don't pick the most dramatic. Pick the one that fits the room." | Give the section one home. Either MM2 carries it in one sentence plus a pointer, or MM6 does, since the button's procedure lives here. Keep the MM6 version and cut MM2 to: "The app's **Stuck?** button, and the procedure behind it in MM6, gives you three ways to get the table moving." |
| Major | 104, 187–195 | Pressure-die gloss; Trouble; "the one test for every entry: does the table now have something to do?" | Repeats MM2:82–88 and 126–153 almost clause for clause: "say the consequence, never the category"; "one package"; "does the table now have something to do?"; "If … only slightly worse off … pick again/take the next one"; "Roll it at three moments". | MM6 should state the procedure; MM2 should teach the craft and point here. Delete the 195 paragraph (MM2:88 owns it) or MM2's copy. Don't keep both. |
| Minor | 96–98 | Morale restated | Style guide: "Re-explaining a mechanic outside its home section". The four morale triggers appear in PHB III.3:126, MM1:142 (home), MM5:108 (quick ref, legitimate), MM6:96 and Bestiary Front Matter:53. | Cut to: "Morale is MM1's procedure (Table MM1–3). There's no table here, because a broken foe's card already says what happens next in its BREAKS line. Retainers check at the same triggers and when asked to do something dangerous that wasn't part of the deal (*Retainers*, MM3)." |
| Minor | 13 | "…rewrite entries for your own table. They're yours." | One-line aphoristic closer. It also pre-empts the 878 closer ("a drawer that's entirely yours"). | Cut "They're yours." |
| Minor | 17 | "The table's job is to break the silence, not to run your game." | "Not X but Y" closer, and a repeat of MM2:151 "A result is a prompt, not an order." | "The table only breaks the silence; what the silence becomes is up to you." Or cut the sentence. |
| Minor | 21 | "You keep the choice, which is where the craft is." | Aphorism. It also conflicts with 351 (magic offers **two**, not three). | "You keep the choice. (Magic Complications is the exception: roll two and let the caster pick.)" |
| Minor | 98 | "That's what the BREAKS line is for." | Recap closer. | Cut. |
| Minor | 104 | "Every face means something: … None of them is blank." | Echoes MM2:120 ("a die that's never blank") and MM2:139 ("none of its faces is empty"). | Cut "None of them is blank." |
| Minor | 191 | "The character gets what they wanted. The cost comes with it. It's never instead of it." | Three short sentences in rule-of-three cadence. | "The character gets what they wanted, and the cost comes with it, never instead of it." |
| Minor | 403 | "A Scar is a part of the character's story from now on. Treat it with the weight the player gave it." | Inflated closer. | "From now on it's part of the character, so bring it up when the fiction touches it." |
| Minor | 447 | "The world didn't stop while the party was busy." | Aphoristic closer. | Cut it. The instruction already says so. |
| Minor | 453 | "Don't pick the most dramatic. Pick the one that fits the room." | Two-beat maxim, duplicated in MM2. | "Pick whichever fits the room, which usually isn't the most dramatic one." |
| Minor | 741 | "It does nothing. It's a story, and it's the reason players search pockets." | Negative-parallel cadence; "is a story" also at MM3:183. | "It does nothing, and players will search every pocket for one anyway." |
| Minor | 751 | Relics paragraph | Duplicates MM3:177 and the relics table's `use` line nearly word for word ("the power belongs to the object and not the bearer, and carrying one never makes anyone a caster … write the quirk so it's also a hook"). | Keep it once, in MM3 or MM6, and cross-reference from the other. |
| Minor | 862 | "It's here because it's a procedure you run, not the players." | Garbled (it reads as "you run, not the players [run]"), and it's a negative parallel. | "It's here because you're the one who calls for it." |
| Minor | 868 | "The best tables at your table will be the ones you write." | "Tables at your table" jars. | "The best tables you'll use are the ones you write." |
| Minor | 874 | "A noun is a prop. A want or a situation is a scene." | Maxim pair. The example before it already makes the point. | Cut. |
| Nit | 471 | "The oracle is also the whole engine for playing without an MM…" | An unmapped claim: no solo procedure is given or referenced. | Either point to one or say "…and it's enough to run a scene without an MM, if you ever want to." |
| Nit | 743 | "under the ogre's bridge" | Ogres aren't in the Bestiary or the PHB, and setting-neutrality is claimed at line 13. | "under the troll's bridge" has the same problem. Use "under the toll-keeper's floor". |

The opening (lines 3–5) is good, human, and not throat-clearing. Leave it alone.

---

### A·4. Bestiary

### 4a. Book-level findings

| Sev | Where | Finding | Fix |
|---|---|---|---|
| **Critical** | Front_Matter:19 | "The project's copyright policy is in `CLAUDE.md`; this book is written to it." | A printed book that cites an AI-assistant config file. Replace with: "Facets of Origin is released under GPLv3; nothing in it is licensed from anyone else." Or cut the sentence. |
| **Critical** | B1:303 | "Seven chickens attacking as one mob will genuinely hurt somebody, which is a sentence this project has had to live with since March." | A developer in-joke about simulation calibration. It means nothing to a reader and breaks the style guide's "no jokes at the game's expense". The same line has a grammar error: "Three chickens are no danger … **So are five**" should be "Nor are five." Rewrite: "Three chickens are no danger to anyone. Nor are five. Seven, attacking as one mob, will genuinely hurt somebody, and you should let the table find that out." |
| **Critical (texture)** | Every Adaptation paragraph: B1:97, 191, 250; B2:129, 255, 316; B3:165; B4:70, 140, 174; also FM:29 | **One template, ten times:** "Change/swap the material… Keep A, keep B, and keep C. A [creature] that [breaks the rule] is [just a dog / not this entry; it is a war / a different creature and a much less interesting one / a long afternoon, not an entry / stops being the entry…]." The style guide names this exact failure ("uniform texture"). Read in sequence, it's the most machine-made thing in the book. | Vary the form entry by entry. Some Adaptations should just be a list of reskins. Some should name the one thing to keep in a single clause. Only two or three should keep the "A ___ that ___ is ___" kicker. Suggested rewrites below (4c). |
| Major | Front_Matter:11 vs 39, 53, 55 | Line 11 promises "these entries use those words without re-teaching them". Then *How to Read a Card* re-teaches role math (39), morale triggers (53) and the open attack roll (55). | Either drop the promise, or cut 39/53/55 to one sentence each plus a pointer to MM1. Keep only what the card needs: † overrides, the Breaks line when morale is 12. |
| Major | Front_Matter:33; B3:141, 145, 157 | FM:33: "the Archive Guardian, which was already canon before this book existed". This contradicts FM:27 ("None of this is Shattered Origin canon") and TODO T6's closing decision (B4/B9: "permanently setting-agnostic"). B3:141/145 also **invents canon**: "a guild that has since dissolved", "the guild that could have countermanded it dissolved along with every record of who held authority over it". The canon source (`enemies/archive_guardian.fof`) says only "commissioned by the Thornwall city government through the Artificers' Guild". Nothing there says the Guild dissolved, and the Guild's canon status is an open NEEDS-RULING item. | **Ask the owner.** Until then, B3 should not state that the Guild dissolved. Neutral rewrite for B3:145: "…and no successor office anyone can find; whoever held authority over it, the records of it are gone or out of reach." FM:33 should be reconciled with T6: either "The Archive Guardian also appears in the Player Handbook's examples, and its entry here matches them", or cut the sentence. |
| Major | Bestiary prose throughout | Em-dash density ~10–16 per 1k (see 1a), against ≤2 in the MM chapters. | Convert most mid-sentence dashes to commas, colons or full stops. Examples below. |
| Major | B1:92, B3:99, B4:64, B4:168, B4:170, B1:91 | **Self-praise tic:** "the table will remember it"; "an extremely good forty minutes"; "quietly one of the better scenes of the session"; "one of the best things this system does"; "the party will talk about it afterwards"; "will feel clever for the rest of the campaign". | Keep one in the book at most. Say what happens, not how good it will be. B4:168: "…and the whole encounter is coordination without speech." (stop there). |
| Major | "the entry" self-reference: B4 ×8, B2 ×3, B1 ×3, FM ×3 | "the entry does not resolve it for you", "the entry means this literally", "the entry is explicit about that", "the wrong reading of the entry", "the entry ends the way it was built to", "that is the entire point of the entry". | Replace most with direct instruction to the MM: "Don't resolve it for them." / "Take this literally." |
| Major | B3:21 / B4:19 | Same opener template: "They are not stupid. This is the point most people miss and it gets them hurt." / "They are not hostile. This is the thing every entry about the restless dead gets wrong and this one will not." | B3: "They are not stupid, and people who assume they are get hurt." B4: "They are not hostile. A Waiting One is *occupied*." (cut the self-congratulation). |
| Major | B1:5 / B3:7 | Same chapter-intro template: "That is the theme of this chapter, and it is worth stating plainly because…" / "That is the pleasure of the chapter, and it is worth protecting." | B1: "It sounds simple and it is the hardest thing to run well: everything here…" B3: "Protect that. A latchman that refuses a correct reading…" |
| Minor | Spelling | British and American mixed. The Bestiary uses colour, behaviour, armour (B1, B3), travelled/travellers, harbour, favour, modelled, reorganising, labour, centre, catalogued, plough, judgement. The MM, PHB and tables use US spelling (color, behavior, armor, favor), and stat blocks print "Armor". The tables also mix: "travelling" (tables.yaml:209) next to "color". | Pick one (the rest of the line is US) and run a pass. |
| Minor | Front_Matter:77, 93–97 | File names in print: `Finding_Aids.md`, and a contents table listing `B1_Beasts_and_Vermin.md` etc. | Use chapter titles: "B1 Beasts and Vermin". Same issue at MM2:9 and MM3:9 (`adventures/oraga_night/`). |
| Minor | Front_Matter:81–83 | "Levels 3–4 … the middle of the book"; "Levels 3–5 hold the Bosses". | Overlapping bands. Say "Bosses run from level 3 to 5". |

### 4b. Front Matter line notes

| Sev | Line | Quote | Rewrite |
|---|---|---|---|
| Major | 15 | "**Every entry ends in a way out.** Not an escape hatch for the party. An alternative for the table. … That is not softness. A monster with only one solution is a door with only one key, and doors like that are why players stop asking questions." | Three negations and a maxim in five sentences. Rewrite: "**Every entry ends in a way out.** Each creature has at least one resolution that isn't a fight, and where one genuinely has none, the entry says why. Players who learn that asking questions can end a fight keep asking them." |
| Minor | 13 | "This is the book for the nights you would rather not." | Keep, but 79 reuses "for the nights you need a number now". Change one. |
| Minor | 21 | "That has a design consequence worth naming." | Throat-clearing. Cut, and start with "You will not find the familiar roster here." |
| Minor | 23 | "But these were grown in this soil." | Aphoristic closer. Cut. "Reskin these freely." is a fine last line. |
| Minor | 29 | "A glassback with its antlers swapped for antlers of something else" | Clumsy. Use "A glassback with amber antlers is still a glassback; one that starts fights is a different animal wearing its name." |
| Minor | 48 | "Information before impact is the whole courtesy of a fair monster." | Maxim. Use "Give these freely; a fair monster shows its hand before it bites." Or cut. |
| Minor | 53 | "Low numbers are not a weakness. They are the reason most fights in this book end with someone walking away." | "Low numbers are why most fights in this book end with someone walking away." |
| Nit | 63 | "it is a sketch, not a script." | Fine; it's a stock phrase. But it's the fourth "X, not Y" on the page. |

### 4c. B3 The Made (deep read)

Strong: the vignette (13–15), the "Ask … accurately" pair in line 21, "there is no dignity in them and they know it", the 10+ lore box ("beaten by a clever apprentice with a borrowed coat more often than by anyone with a hammer"), and the Ecology trades (161).

| Sev | Line | Quote | Issue | Rewrite |
|---|---|---|---|---|
| Major | 141–143 | "It is not malevolent. It is doing exactly what it was told. / That is, in certain lights, worse." | Negative parallel plus a one-line aphorism paragraph. **This text is copied from the canon `archive_guardian.fof` description**, so the owner must approve any change. | "It bears no one any malice. It is doing exactly what it was told, which in certain lights is worse." |
| Major | 141, 145 | "through a guild that has since dissolved"; "the guild that could have countermanded it dissolved along with every record…" | Invented canon (see 4a). | See 4a. |
| Major | 106 + 145 + 157 | "The Latchmen's Boss is not a bigger latchman. It is…" / "What makes it a Boss and not a large latchman…" / "intended to be solved sideways … It is not meant to be met head-on." | The same point is made twice, and "sideways/not head-on" three times, in 50 lines. | Cut 106 to "The Latchmen's Boss is what the same commissioning produces when the thing behind the door is worth more than the building." Cut the 157 sentence "It is not meant to be met head-on." |
| Minor | 5 | "cannot be frightened, and will not be reasoned with — but it *can* be read." | Triplet plus dash reveal. | "A made thing wants nothing, can't be frightened and won't be argued with. It can be read." |
| Minor | 7 | "A latchman that arbitrarily refuses a correct reading is a locked door with extra steps." | "with extra steps" is an internet meme. It will date the book and reads as snark. | "…is just a locked door that talks." |
| Minor | 17 | "Not to guard them — *keep* them, in the sense a clerk keeps a register" | Not-X-dash-Y. | "Latchmen were made to keep doors, the way a clerk keeps a register: to know the rule about this door and apply it." |
| Minor | 17, 161 | "commissioned … across several centuries"; "A city that used latchmen extensively three centuries ago" | World-history claims in a setting-agnostic book. FM:65 allows lore stated as fact, so this is borderline. | Frame as portable: "Wherever latchmen were made, they were commissioned for centuries…" |
| Minor | 99 | "heavy armour" | Spelling; the card says Armor. | "heavy armor". |
| Minor | 145 | "no clever reading…, no borrowed coat, and no successor office — the guild…" | Triplet plus dash. | See 4a rewrite. |
| Minor | 161 | "There are people… There are forgers… There are three or four families…" (then 163 "And there are rooms…") | Four-fold "There are" anaphora. | Merge the middle two: "There are people whose whole trade is knowing which dissolved authority commissioned which building's fittings, and what form of words it accepted; some of them are forgers." Keep the families line and the 163 closer. The closer is earned. |
| Minor | 165 | "Keep the instruction, keep the fact…, and keep the seam. A made thing that cannot be satisfied…" | The template (4a). | "The commissioning body and the material are free to change: a temple order, a dead monarch's household; brass, stone, a bound spirit. What makes it a latchman is that it will state its instruction when asked and that the instruction has a seam. The Guardian's end of the ladder is the only place for one without a seam, and one per campaign is plenty." |

### 4d. B1, B2 and B4 samples

**Samey entry texture across the four chapters.** Every family follows Vignette → one-line thesis → lore with one bolded sentence → cards → lore box → Encounters (the last always "*(no fight)*") → Ecology → Adaptation, and every Ecology ends on a wry kicker line:
- B1: "very slightly smug"
- B2: "Word travels at the speed of a shift change."; "widely disliked and universally hired"
- B3: "with something in them"
- B4: "furious with them about it"

A shared structure is the point of a catalog. The shared *closing cadence* is the tell. Vary the endings: let some Ecology paragraphs just stop on a fact.

**Vignettes.** All are read-aloud boxes with no cast members, so cast voice doesn't apply. They're good and don't act for the PCs. Two use negative parallels inside the read-aloud:
- B4:76: "not the figures moving on it, not the sound, but the sheer scale"
- B4:146: "Not because anyone has stopped talking —"

Suggest for B4:146: "*The conversation stops. The man across the yard is still talking, mouth moving, hands going, and there is nothing.*"

**Setting canon.** Mostly clean and portable. Borderline:
- B2:141: "They have existed in some form in every settled region for as long as anyone has been able to write down what they wanted done." (a named company, present everywhere)
- B2:306: "There are people alive today…"
- B1:201: "Every competent archivist in the world knows this."

These are fine under FM:65 but lean on "the world". A light fix: "in every settled region *where they operate*".

| Sev | File:line | Quote | Rewrite |
|---|---|---|---|
| Major | B2:137–141 | "It is not a joke. … **This is not decoration. It is the entire creature.** … The name changes. The case does not." | Two negations back to back, plus an aphoristic closer. "The Bought are a mercenary company that jokes its most dangerous asset is the paperwork, and it's right. A Bought contract… **The contract is the creature.** A company that fights strictly to written terms…" Cut "The name changes. The case does not." |
| Major | B4:152 | "Nothing about that requires a new subsystem, and that is the entire point of the entry." | Designer-voice paragraph with "entire point". It belongs in a Through the Mirror box if it belongs anywhere. Cut, or fold into 148. |
| Major | B4:5 | "…is not *you are being punished* but *somebody needed help and nobody came*. The Waiting are sad. The Unfinished is enormous and sad. The hushfall is not sad at all, but … its own kind of unsettling." | Keep the first sentence, which is good. Then: "The Waiting and the Unfinished are sad; the hushfall can't be hit, which unsettles people in a different way." |
| Major | B2:123 | "The fight is winnable. The arrest is survivable. The report is the actual problem." | Triad of short sentences. "The fight is winnable and the arrest survivable; the report is the real problem." |
| Minor | B1:15 | "They cannot leave their road. Not will not — cannot." | "They cannot leave their road, and it isn't a choice." Or keep one "cannot" in italics. |
| Minor | B1:91 | "It is not dangerous. It is terrifying, which is a different thing, and a party that works out the standing-still rule here will feel clever for the rest of the campaign." | "It's terrifying rather than dangerous, and it's the place for a party to work out the standing-still rule." |
| Minor | B1:97 | "those two facts are the whole creature. A chalk hound that can chase you into a field is just a dog." | "Whole creature" also appears at B2:139. Keep this kicker (it's the best of the ten) and vary the rest. |
| Minor | B1:185 | "The entry's whole job is that both options are real." | "Make both options real." |
| Minor | B1:305 | "**Ecology.** It was never really part of this." | Unclear referent. "**Ecology.** The chicken has none. Let it survive through sheer irrelevance and wander off at the end." (This also removes the passive "Mirror Masters are encouraged to".) |
| Minor | B2:5 | "are not the same creature at two sizes, they are two different jobs." | Comma splice plus negative parallel. "…are two different jobs rather than one creature at two sizes." |
| Minor | B2:7 | "Not as a mercy the Mirror Master extends, but as the ordinary behaviour…" | "It isn't mercy; it's what ordinary people do when a fight is going worse than they expected." |
| Minor | B2:251 | "the entry is explicit about that because players will not guess it." | "Tell the players this if they don't guess it; they won't." |
| Minor | B2:265 | "They always speak first, always politely, always in whatever language…" | Triple anaphora. "They speak first and politely, in whatever language…" |
| Minor | B4:17 | "Not all of them, and not most of them — the great majority…" | "Most people who die at work simply die at work." |
| Minor | B4:60 | "That's the whole of it." | Cut. The next sentence is the good one. |
| Minor | B4:64 | "it is quietly one of the better scenes of the session." | Self-praise. "…the party finishes somebody's work, and that's the scene." |
| Minor | B4:88 | "Which means the only real ending is to make it finishable." | Fragment paragraph. Fold it into 86: "…there is no roll under which it stops, so the only real ending is to make the work finishable." |
| Minor | B4:136 | "Sometimes it is not. That is the good version of this scene." | "Sometimes it isn't, and that's the good version." |
| Minor | B4:170 | "This is not a monster encounter. It is a rescue with a very strange constraint, and the party will talk about it afterwards." | "It's a rescue with a very strange constraint." |
| Nit | B1:107 | "completely safe, completely legal…, and completely uninteresting" | Comic triple. Keep; it earns it. |

---

### A·5. MM2, MM3 and MM4 samples

### MM2 (read lines 1–32, 72–176, 261–272)

Voice is generally good. The opener (line 3, "Nobody remembers a well-structured session…") is a strong human hook.

| Sev | Line | Quote | Issue / rewrite |
|---|---|---|---|
| Major | 261–269 | *When You're Stuck* | Duplicates MM6:443–453 (see §3). |
| Major | 82, 86–90, 126–153 | Trouble, 7–9 cost test, Pressure faces, usage dice | Duplicates MM6 (see §3). Decide which chapter owns each procedure. |
| Major | 74 | "On a 6−, something always happens. That's the whole point of it. A 6− isn't 'you fail and nothing changes.' It's 'the situation moves…'" | The heading says the same thing, so the first sentence repeats it, and "whole point" plus "isn't… It's" follow. Rewrite: "A 6− never means 'you fail and nothing changes'. It means the situation moves in a direction nobody planned." |
| Major | 9 (and MM3:9) | "`adventures/oraga_night/` … this project's worked example" | Repo path and "this project" in a printed book. Use "**Oraga Night**, the starter module, is a worked example…" |
| Minor | 19 | "If your opening lets the party shrug and go shopping, it isn't a hook, it's scenery." | Comma-splice negative parallel. "If the party can shrug and go shopping, you've opened on scenery." |
| Minor | 29 | "The three acts are a default, not a cage." | "Treat the three acts as a default." |
| Minor | 80 | "A 6− that stops the story is the MM's mistake, not the dice's." | Fine as a maxim, but it's the fourth "X, not Y" on the page. "If a 6− stops the story, the roll shouldn't have been called." (merges with the next sentence) |
| Minor | 98 | "Not louder: different." | Keep one of these per chapter at most. |
| Minor | 114 | "That turns a counter into a picture. … A clock that lingers stops being pressure and becomes furniture." | Two aphoristic closers in one paragraph. Cut the first and keep the second. |
| Minor | 120 | "The fix is a clock that isn't a timer, and a die that's never blank." | Riddling. "The fix is the exploration turn and the Pressure die." |
| Minor | 139–141 | "And none of its faces is empty. … That's the pressure. You didn't have to raise your voice." | Two closers. Cut "That's the pressure." |
| Minor | 153 | "It's the only supply tracking this game does, and it's plenty." | OK. It duplicates MM6:860. |
| Nit | 173 | "Zulnut, very sensibly, climbs onto a ledge to look around." | Slightly off-voice for the profoundly lazy acrobat. "Zulnut, who has found the one dry ledge in the room, stays on it and looks around." Also, the example has no failed roll and no MM ruling spoken aloud (style guide). The treat-4-as-quiet ruling could be spoken: "(MM: 'First room. I'm letting that one go.')" |

### MM3 (read lines 1–14, 47–74, 165–219)

| Sev | Line | Quote | Issue / rewrite |
|---|---|---|---|
| Minor | 51 | "They'll be the ones who felt like people: who wanted something, who surprised the table, who came back when nobody expected them to." | Triple anaphora. "…the ones who felt like people, usually because they wanted something and came back when nobody expected them." |
| Minor | 69 | "The shopkeeper you improvised… will come back; the one you spent an hour designing won't. Accept it." | "Accept it." is a closer. Cut it. |
| Minor | 71 | "If you can't answer, they're scenery with a name." | "Scenery" also at MM2:19. Keep one. |
| Minor | 167 | "…will treat fights as obstacles rather than the point." | Fine. |
| Minor | 175–177 | Curios and relics paragraphs | Duplicate MM6:751 and the relics table `use` text (see §3). |
| Minor | 183 | "A chest of coin stamped with a guild's seal is a story; forty coins is a number." | Same "is a story" beat as MM6:741. Keep this one and change MM6's. |
| Minor | 187 | "Hand out the strange, not the bigger. … and that's on purpose. An item that does something odd produces play. An item that only makes a number bigger produces nothing but a slightly different number." | Heading plus two parallel sentences. "…and that's on purpose: an odd item produces play, and a bigger number produces a bigger number." |
| Minor | 206 | "That's a guideline." | A hedge after a table. Cut; the next sentence makes the point. |
| Minor | 210 | "A skirmish before a hard fight isn't about the skirmish. It's about the HP and Fatigue the party carries into the next room." | Negative parallel. "A skirmish before a hard fight is there for the HP and Fatigue the party carries out of it." |
| Minor | 216 | "Combat is a tool, not an obligation." | Cut; the next sentence makes the point. |

### MM4 (read lines 1–26, 99–156, 231–282): the densest tells in the MM

| Sev | Line | Quote | Issue / rewrite |
|---|---|---|---|
| **Major** | 5–9 | "You aren't the author…, and you aren't the antagonist. You aren't even the narrator… / You are the world, responding to protagonists. / That distinction matters more than any other advice in this chapter." | Triple negation, a one-line thesis paragraph, then an importance claim. The idea is good; the rhythm is AI. "You're not the author of this story or its antagonist, and you're only the narrator in a narrow sense: you don't know what happens next either. You're the world, answering the protagonists. Most of this chapter follows from that." |
| Major | 267 | "That isn't a flaw; it's the job. Steal situations, not stories: not a novel's plot, but the premise of its best chapter… Most of it will never become anything. A few will become the best sessions you ever run." | Three negative parallels and a closer in one paragraph. "Every experienced MM runs on things lifted from other games, books and films. Steal situations: the premise of a novel's best chapter, not its plot…" Cut the last two sentences, or keep only the second. |
| Major | 271–279 | "A bad session isn't evidence that… It's evidence that…" / "That tells you what you need to know." / "That isn't because… It's because…" / "Every session is information." / "There's no point where you've figured it out… That's the point." / "which is exactly why it's worth doing for years." | Six tells in three paragraphs, the densest cluster in the MM books. Cut "That tells you what you need to know.", "Every session is information." and "That's the point." Merge the two "isn't/It's" pairs into direct statements. For example, 277: "The MM running their tenth session is better than the one who ran their first, because they've grown instincts: when to push, when to hold back, when a scene needs to end." |
| Minor | 17 | "'No' stops the story. 'Yes, but' keeps it moving." | Maxim pair; it duplicates MM2's *Yes, And; Yes, But; No, But* (231) and MM4:251–253. Cut here, since MM2 owns it. |
| Minor | 19 | "isn't filler. It's an invitation to build the story with you." | "…invites them to build the story with you." |
| Minor | 21 | "**Prepare situations, not scripts.**" | Third copy of MM2:241 *Prep Situations, Not Plots* (also MM4:247). Cut here or at 247. |
| Minor | 101 | "…is a communication problem, not a behavior problem. … isn't a solution. It's an escalation." | Two negative parallels in the section opener. "Every one of these is a communication problem, and the answer is to talk. Punishing a player in the fiction (the rocks fall, everyone dies) only escalates it." |
| Minor | 109 | "It's a redirect, not a correction" | Cut; the next clause says it. |
| Minor | 117 | "If they're enjoying it, that's enough." | Closer; fine, but one of many. |
| Minor | 135 | "You're not firing anyone. You're ending a social arrangement…" | "It isn't firing anyone; it's ending an arrangement that's stopped working for the people in it." Or cut. |
| Minor | 141 | "…and none of them is wrong. This isn't a rigid taxonomy…, but a loose vocabulary helps." | "…and none of them is wrong. These five labels are loose, and most players are several at once." |
| Minor | 245 | "They're the learning curve, not failures." | Cut. |
| Minor | 251 | "Your plan is a suggestion. Their enthusiasm is the game." | Maxim pair. Keep only if it's the one maxim you allow in the section. |

The rest of *Difficult Situations* (What it looks like / What's usually happening / What to do) is well built and practical, and the cast examples (109, 117) are in voice.

---

### A·6. Suggested order of work

1. Remove the Criticals: FM:19 `CLAUDE.md`; B1:303 "since March" and "So are five".
2. Get an owner ruling on the Archive Guardian: the invented "dissolved guild", and FM:33 vs T6.
3. Pick one home for each duplicated procedure: MM2↔MM6 (Stuck, Pressure die, Trouble, 7–9 test, usage dice) and MM3↔MM6 (relics/curios).
4. Bestiary dash-and-cadence pass: em-dashes, the ten Adaptation kickers, the "the entry" and self-praise tics, spelling normalisation.
5. MM4 *Philosophy* and *Growing as an MM* rhythm pass.
6. Table swaps in tables.yaml (§2c), then run `python -m tools.build_toolbox` to re-render MM6.

---

# Appendix B — Canon audit and Oraga/Val'loh voice (specialist report)


Read-only audit. I edited nothing in the repo and ran no git command that changes state.

**Method.** I took a word-diff of every file under `adventures/oraga_night/`, `settings/valloh/`, `player_handbook/`, `mm_manual/`, `bestiary/`, `characters/` and `enemies/` against the tag. I then diffed the proper nouns: every capitalised token and run in the lean books, set against every capitalised token anywhere in the tag (books, references, research, docs, facet data). Every hit was checked against `references/phb-examples.md`, `references/oraga_night/{[private canon notes],WORKING_NOTES,INVENTIONS_FOR_REVIEW}.md`, `references/valloh/INVENTIONS_FOR_REVIEW.md` and the owner's corpus [author's private setting notes] (the source for the eight gods and for Elanna and Rycha). I read `04_The_Ball.md`, `05_The_Longest_Night.md` and all of `settings/valloh/` in full.

### B·Headline

**The Lean conversion invented almost no new lore.** Every Oraga and Val'loh change is mechanical: stats, HP, curios and knacks. The new pregen/class/background names, the TWISTS tables and the Hold On floor are all recorded in Oraga INVENTIONS **Revision 5** and in the Val'loh file's Lean addenda. No new towns, factions, gods or named NPCs appear in the PHB, the MM Manual or the Bestiary, apart from MM6's setting-neutral generator tables and the credits page. The Artificers' Guild is **no longer named anywhere in the PHB or MM** (III.3 now says only "commissioned by the city").

The real problems are these:
1. **The lean enemy cards make three contradictions worse:**
   - The Bought captain's generated TWISTS contradict the module's own Second Clause and faceless-factor rulings (4.2, 4.3).
   - A new Tavva twist repeats a written "hiring list".
   - The new card lines call the Uninvited "it" throughout, against the owner's ruling that the [private] are human, she/he.
2. **Several older contradictions of the written-word ban (U8/U10) survived the pass.** Examples: "history books", "labelled in a hand", "consult by letter". MM6's social table, which Oraga now tells the MM to keep open, has writing-based entries.
3. **Several older inventions were never listed** for the owner: the Chiefs' Concourse, the falconry mews, "the Just One", "three cities". Some of these lines also contradict canon, such as V0's "the four people in five who were born without a gift".
4. **The PHB has one archive-scene continuity clash** between III.1 and II.2, and the MM1 ogre example gives Mordai the wrong weapon die. Both are Minor.

Severity key: **Critical** means it contradicts owner canon, or invents major lore in player-facing text without being listed. **Major** means an unlisted named entity, or a contradiction of an owner ruling in MM-facing text. **Minor** means a small unlisted detail or an internal inconsistency. **Nit** is cosmetic. Findings are labelled **NEW** (introduced or touched by the lean commits) or **PRE** (already there at the tag, and the lean pass left it alone).

---

### B·1. Oraga Night (`adventures/oraga_night/`)

### 1a. What the lean diff added, checked against INVENTIONS_FOR_REVIEW

| Item | Where | Listed? |
|---|---|---|
| Pregen classes: Speaker (preset), Courier, Pattern-Keeper, Go-Between; Guardian (preset) | 03, `characters/*.fof` | Yes: Rev 5 table |
| Backgrounds: Minor Scion, Factor's Nephew, Lattice-Scholar, Border Courtier; all knack names | 03, `.fof` | Yes: Rev 5 |
| Background descriptions (House Vaskarin branch, Tessarin branch, Kethaun border branch, "five tribes' roads") | `.fof` | These descriptions predate the lean pass; the house names are invention #2 |
| Gift domains for the pregens | 03 | Yes: Val'loh §3 plus Rev 5 |
| Dassa's *City Watch Veteran* knack | `dassa.fof` | Already Dassa's background before the lean pass. Fine |
| Enemy card WANTS / SPECIAL / BLOODIED / TELLS / BREAKS / TWISTS | `enemies/*.fof`, 09 | Yes: Rev 5 ("All six-line TWISTS tables are new") |
| Honor guard "House blade", sect guard "whistle", "Cudgel" | `.fof` | Covered by the TWISTS/flavour note; trivial |
| Seating feud now uses the Bestiary Harbor Thug card for kinsmen | 09 S1 | **Not listed** (mechanical; see M-5) |
| Session-end prompts; level 2 at the epilogue, level 3 at the inquest | 01, 06 | Yes: Rev 5 "Advancement" |
| Crossfire hazard, seating-feud mercy, Hold On floor | 04, 05, 08 | Yes: Rev 5 |

No new proper noun, NPC, place or faction appears in any lean-changed Oraga line. A scan for spoiler-boundary leaks came up empty: no Krenn, [private], [private], [private], [private], [private], [private], Adella'suk, Nao Mar, [private], Raquora, Ulan or Xilen anywhere in `adventures/`. Master Vell is never named Krenn.

### 1b. Findings

**O-1 · Major · NEW (generated from the Bestiary)**: the Bought captain's TWISTS contradict inventions 4.2 and 4.3.
- `adventures/oraga_night/enemies/bought_captain.fof` twists, printed into `09_Scene_Cards.md` S3 (lines 29–35 of the card block):
  - "The Second Clause is to take the party alive and deliver them to the employer."
  - "The Second Clause voids the contract if the employer lied, and the employer lied."
  - "The employer has come onto the field, and the captain would very much prefer otherwise."
- Oraga's Second Clause is fixed canon for the module: *"if a woman in Thenya wool comes out the front, hold her, and send word to the river"* (05:333–334, invention 4.2). The factor "has no face and no name… the module never gives it" (05:340–341, invention 4.3). Twists 1, 2 and 6 would overwrite the first and produce the second.
- Card lines must stay identical to the Bestiary's (INV-18), so the fix belongs in the notes, not the twists.
- **Remedy:** add a line to the reskin notes of `bought_captain.fof` (and to S3's card preamble): *"At Oraga, the Second Clause is always the one in Chapter V, and the employer never appears. Reroll twists 1, 2 and 6."* Also list this in INVENTIONS Rev 5, "The enemy cards".

**O-2 · Major · NEW lines, older habit**: the Uninvited are called "it" throughout the lean card text.
- `enemies/the_wept.fof:16` "It has a task, not a body count."; `:19–27`; `:29–32` "It is losing the argument with what it used to be."; twists `:50–55` "It steps through the world's shadow…". The Radiant and the Hollow cards do the same ("A lantern bursts as it passes"; "It asks, flatly…").
- Counts of "it" rose in the lean pass: Wept 18→27, Radiant 19→28. These print into the Chapter IX scene cards and the Chapter VIII handout.
- This contradicts `[private canon notes]`, "Later rulings": *"The [private] are very much still human… pronouns she/he; 'creatures/monsters/not people' phrasing removed."* Chapter 05 is also mixed. The Fractures section uses she/he, but 05:79–84, 121–124, 131–135, 166–177 and 184–196 use "it".
- **Remedy:** Wept is she/her, Radiant and Hollow are he/him, everywhere in the three `.fof` files and in 05's beats. Examples:
  - "She has a task, not a body count."
  - "She steps through the world's shadow and is suddenly on the other side of the party."
  - "A lantern bursts as he passes; the corridor goes dark, and he hurries — nobody is watching."
  - 05:83 "he has gone for the east wing"; 05:175 "The Radiant recognizes him. He says one word".
  - If the Bestiary house style needs "it", note the Oraga exception in the card's `notes`.

**O-3 · Minor · NEW line**: a written list, against U8/U10.
- `enemies/tavva.fof:38` twist: "She names the player character she is fighting, correctly, from the festival hiring list."
- The same phrase already sits in the description (`tavva.fof:42–43`, "a different name on every festival hiring list") and at `07_Cast_of_the_Ball.md:377–378` (PRE). In a world where "guest list → Corval's memory", a hiring *list* is writing.
- **Remedy:**
  - twist: "She names the player character she is fighting, correctly — she stood behind them in the hiring line."
  - description: "a different name at every festival hiring"
  - 07:377: "somewhere in every festival's hiring line under a different name."

**O-4 · Minor · NEW pointer**: Oraga now tells the MM to keep MM6's social complications table open, and that table contains writing.
- `01_Overture.md:260–262`: "keep the social complications table open. It is in MM6, *The Toolbox*, beside the night-tracker". Two problems:
  - The table is not beside the night-tracker. The night-tracker is Oraga's Chapter VIII.
  - Entries in the table break the Church ban: `mm_manual/MM6_The_Toolbox.md:314` "It's written down somewhere that other people read."; the pressure table at `:176` "a servant hurries off with a note".
- **Remedy:** "…open. It is in MM6, *The Toolbox*; print it beside the night-tracker. In Val'loh, anything the table says is written down is *remembered* instead — by a Scora, a steward, or Corval."

**O-5 · Minor · PRE**: "history books" in a world with no books.
- `05_The_Longest_Night.md:125–126`: "the escape in the history books happens because people got in the way."
- **Remedy:** "the escape the city will spend twenty years retelling happens because people got in the way."

**O-6 · Major · PRE (Revision 4 invention 4.20)**: a hand-labelled room.
- `04_The_Ball.md:274–275` (B13): "make it the room where twenty-two people's effects are stacked and labelled in a hand nobody recognises."
- Handwriting on labels breaks U8/U10. Invention 4.20 also claims B13 "invents only a door and its position; the contents are the MM's", but the example contents are the module's.
- **Remedy:** "…effects are stacked and knotted with tally-cords in a pattern nobody recognises." Update 4.20 to say the three examples are suggestions.

**O-7 · Nit · PRE**: `04:361` "the crew's list and their grandmother's crystal". This reads as a written list.
- **Remedy:** "the crew's targets and their grandmother's crystal".

**O-8 · Minor · PRE, unlisted**: `04:809` "the falconry mews behind the garden wing erupt — every bird screaming at once". The mews are not in WORKING_NOTES and not in INVENTIONS.
- **Remedy:** list it as omen texture under Revision 2/4, or cut it to "every bird in the garden wing erupts screaming at once, then, worse, all at once silent."

**O-9 · Minor · PRE, unlisted epithet**: `05:284` "Whatever spoke to you, it was not the Just One." The epithet for Rycha (God of Justice, `[author's private setting notes]`) is new and appears nowhere in canon.
- **Remedy:** list it in H1/H2, or write "it was not Rycha."

**O-10 · Minor · PRE**: the text asserts a mapping the owner has not confirmed.
- `05:175–177`: the Radiant's "…You." carries "the special hatred the devout reserve for an apostate".
- `[private canon notes]` records Ulan → hatred of the apostate as a *proposed* mapping that "needs user confirmation".
- **Remedy:** add it to R6's "confirm" note, or soften it to "wary for the first time tonight, and underneath the wariness, something older."

**O-11 · Minor · PRE**: an internal contradiction about killing the Uninvited.
- `05:453–454` (⟨They expose the truth⟩): "the mask of a dead Uninvited".
- "Killing one is off the table" (05:437; R7). No Uninvited can die, so this evidence cannot exist.
- **Remedy:** "the mask an Uninvited left behind".

**O-12 · Minor · PRE**: a head-count mismatch.
- `05:474` "watched — by forty blades", and `05:479–480` "forty sworn witnesses". The Bought are sixteen blades, four sergeants and one captain: 21 (05:326; invention 4.5).
- **Remedy:** "by twenty-one blades" and "twenty-one sworn witnesses". Alternatively, say explicitly that the forty include the sect guard.

**O-13 · Nit · PRE**: an interiority and spoiler question.
- `05:422` "once he understands what came for his son". This asserts the unborn child's sex, and that Raunu knows it. It is MM-facing, but the module otherwise never sexes the child.
- **Remedy:** "what came for his child".

**O-14 · Nit · PRE**: `05:482` "used his company's name to burn a city". There were fires in two districts (invention 4.1).
- **Remedy:** "to set fires across the city".

**O-15 · Nit · NEW**: Andra's kit.
- `characters/andra.fof` carries `{id: ink_and_chalk, name: "Chalk and a wiping slate"}`. The id says ink, and the slate as standing kit leans on U10's *unconfirmed* slate carve-out.
- **Remedy:** rename the id to `chalk_and_slate`, and add "Andra's kit slate" to U10's confirm list.

**M-5 · Nit · NEW, unlisted mechanical choice**: the Harbor Thug card doesn't fit drunk kinsmen.
- `09_Scene_Cards.md` S1 prints the Bestiary Harbor Thug card for Boranis/Tessarin kinsmen. Its generated lines, "Wants: Paid, and home…", "looking back at whoever hired them" and "takes the nearest portable cargo along", don't fit drunk cousins.
- **Remedy:** list the S1 reskin in Rev 5. Add to the italic note after the card: "Ignore the card's Wants/Tells/Breaks: kinsmen want to win the argument, watch their principal, and stop when an elder is obeyed."

---

### B·2. Val'loh (`settings/valloh/`)

The lean diff is purely mechanical: gift knack plus Minor-for-life, curios, Fatigue, Thaumaturgy/Invocation. It is fully recorded in the Val'loh INVENTIONS addenda (§3, §6). **No new proper nouns** were added. Everything below was already in the books before the lean pass, left in place and never listed.

**V-1 · Critical · PRE, player-facing contradiction of U8/U10**: "consult by letter".
- `V1_Lineages.md:103`: "a Kshalo who can enter your dream is a Kshalo most people would rather consult by letter."
- V3:105 says outright "no letters". This is the players' chapter.
- **Remedy:** "…is a Kshalo most people would rather consult across a crowded room."

**V-2 · Major · PRE, contradicts its own item 1**: "four people in five who were born without a gift".
- `V0_Ten_Things.md:35`: "including the four people in five who were born without a gift."
- Item 1, three lines earlier, says four in five Orthaen *have* it. Across the published rates (Scora all; Phern, Dekhi, Fthala and Tyndi most or nearly all), most of Val'loh is gifted.
- **Remedy:** "including the Orthaen fifth who were born without the gift, and the visitors who were born without a tribe."

**V-3 · Major · PRE, unlisted named place**: `V3_Rekuzan_and_the_Tribes.md:90` "in the order their banners hang in the **Chiefs' Concourse**". The name is not in [author's private setting notes] and not in either INVENTIONS file.
- **Remedy:** list it in Val'loh §7 (and against invention #2, since the sect order rides on it), or strike it: "The eight sects of the Orthaen: …"

**V-4 · Minor · PRE, unlisted**: `V1:31` "A Phern factor's word is currency in three cities". Is this an invented count of Val'loh cities?
- **Remedy:** "…is currency on every road they walk", or list it.

**V-5 · Minor · PRE**: the sea and the mists.
- `V0:7` "And a sea in the east that has stopped breathing in." Canon says the *mists* recede (the mists "roll in from the sea like tides"). The line reads as the sea itself.
- **Remedy:** "And mists in the east that have stopped coming in."

**V-6 · Minor · PRE, internal contradiction**: V2 says three times that a charge takes no roll, then says it does.
- `V2:39` "There is no roll."; `:45` "no Fatigue, no roll"; `:47` "Spending one takes no roll at all… When the fiction makes a *release* chancy … that is a Soul roll".
- **Remedy:** delete the `:47` "Spending one…" paragraph's first two sentences, and fold the chancy-release case into `:45`: "Releasing one is not a working: no Fatigue, and no roll — unless the fiction makes the release chancy (fumbled in the dark, held near something that eats magic), which is a Soul roll at Standard."

**V-7 · Nit · PRE**: `V1:133` "*Most, in specialties carry it.*" is broken.
- **Remedy:** "*Most carry it, each in one specialty.*"

**V-8 · Nit · NEW**: `V2:25` "from the Mind list of domains — on the Mind menu, or from another Facet's with a teacher found in play." This garbles talent-menu and domain-list language.
- **Remedy:** "the Thaumaturgy talent, cast with Mind — on the Mind talent menu, or taken from another Facet's menu with a teacher found in play."

---

### B·3. PHB / MM Manual / Bestiary / `characters/`

### 3a. Cast facts, checked against `phb-examples.md`

- **Pronouns:** no she/her for Zahna, Mordai or Zulnut anywhere. The only nearby "she" is the archivist (II.2:93).
- **Stats:** all three match (Zahna Mind+2/Soul+1/Body+0; Mordai and Zulnut Body+2/Soul+1/Mind+0).
- **Classes and knacks:** Zahna is a Thaumaturge (Inscription; *Arcane theory*, *Guild Apprentice*). Mordai is a Warrior (*Soldiering*, *City Watch Veteran*; HP 16). Zulnut is a Wandering Disciple (custom; Unarmored Discipline + Athlete; signature Ghost). These match in II.1:59–60, II.4:73–89, Quick_Start:71–83, III.3, IV.1:103 and all three `characters/*.fof`.
- **All human:** II.5:3 and 27. Each `.fof` has `lineage: {id: human}`.
- **Millhaven scar:** III.2:136–166 matches canon: he takes the Scar and not the heroic death, the shoulder is set wrong, and "one thing it will never carry again". The lean pass added a temporary *Cracked ribs* Wound (III.2:144), which is harmless. `Mordai.fof` records that the file predates Millhaven. Arc order holds: II.2 → II.3 → III.3 in Thornwall, then III.2.
- **Artificers' Guild:** not named anywhere in `player_handbook/` or `mm_manual/`. Good, per the phb-examples III.3 note.

**P-1 · Minor · NEW**: the MM1 ogre example ignores Weapon Master.
- `mm_manual/MM1_Encounters_and_Enemies.md:278`: "His longsword deals 1d8".
- Mordai has *Weapon Master (blades)*, which makes it a d10 (Quick_Start:75–77, III.3:198, `Mordai.fof` notes).
- **Remedy:** "His longsword deals 1d10 (Weapon Master), showing 5, and he picks +1d6 damage…". The arithmetic that follows is unchanged.

**P-2 · Minor · PRE**: two versions of the same archive-desk scene.
- `III.1_Core_Resolution.md:177–205`: it is ten past closing; Mordai's Soul roll **fails** (6); Zahna is Easy with *Guild Apprentice* and gets 11. It ends "That's Chapter II.2's problem. Roll it there."
- `II.2_Character_Creation_Stats.md:53–93`: the archive "closes in one hour"; Mordai's Soul roll is a **partial** (8) with the archivist pointing at the door; Zahna is Standard "Neither of your knacks is the city's paperwork" and gets 10.
- phb-examples canonises the II.2 version (Mordai partial success).
- **Remedy (lightest):** make III.1 a *different* visit.
  - Open it with "The morning after, the party is back at the Thornwall Municipal Archive, and it closes to the public at four…"
  - Replace the hand-off line with: **Zulnut:** *(delighted)* "I would like to be near the desk." **MM:** "(You were near the desk yesterday. That is why she has written *your* description down too.)"
  - Alternatively, make Mordai's III.1 roll the canonical 8.

**P-3 · Nit · PRE**: `mm_manual/MM2_Session_Design.md:454` "Does *City Watch* apply?" The knack is *City Watch Veteran*.
- **Remedy:** "Does *City Watch Veteran* apply?"

**P-4 · Nit · PRE**: some MM vignettes are undated relative to Millhaven.
- MM1 ogre bridge, MM2 warehouse, MM4 alley, and the MM3 "End of the Road" campaign finale all have Mordai in heavy armor with a shield and no mention of the shoulder. MM3's finale, after a 16-session campaign, is almost certainly post-Millhaven.
- None of them contradicts the scar outright: he is not shown carrying something heavy.
- **Remedy (optional, MM3 only):** add to MM3:319 "(There aren't. He looks anyway, rolling the bad shoulder the way he does on cold evenings. …)". Or note in phb-examples that MM vignettes are timeline-free.

### 3b. New proper nouns

Every capitalised run in the lean PHB and MM that is absent from the whole tag falls into these groups:
- Talent, class, table and section names (rules vocabulary).
- `MM6_The_Toolbox.md`'s **name table** (lines ~580–615: Ansel, Bettany, Osric, Tamsin…), its relic/curio names (Ironbark Shield, Crown of Small Kingdoms, Boots of the Long Road…) and its one-line news examples (MM3:261 "Low Ford", "the river guild").
- The MM1 worked example monster "the Toll Ogre".
- Credits (Front_Matter:57–70: Whitehack, Necropraxis/Brendan S., Sly Flourish/Mike Shea, and so on).

MM6:13 declares the tables "setting-neutral: no place, people or name in them belongs to any particular world". That is acceptable, and **not flagged**.

There are no new towns, guilds, gods, historical events or recurring NPCs. The Thornwall and Millhaven material, "The Shattered Road", "Thornwall City Watch", "governor", "coastal archive" and "merchant lord" all predate the lean pass (MM3).

### 3c. Bestiary

**B-1 · Minor · PRE**: the Bestiary settles the guild's fate.
- `bestiary/B3_The_Made.md:141`: "The Guardian was commissioned by a city government through a guild that has since dissolved".
- Front_Matter:33 declares the Archive Guardian Shattered Origin canon, so this line asserts a canon fact: a guild that commissioned it and has *dissolved*. Whether the Artificers' Guild is canon is an open owner ruling (the #29 review's NEEDS-RULING list). The PHB carefully avoids it.
- **Remedy:** "The Guardian was commissioned by a city government to hold one room." Keep the 7–9 line (B3:153, "Guild work…") only if the ruling lands; otherwise use "Commissioned work — proper construction, and old."

**B-2 · Nit · PRE**: dev-log voice and unchecked numbers in the chicken entry.
- `B1_Beasts_and_Vermin.md:303`: "…which is a sentence this project has had to live with since March."
- It also states v0.3 simulation outcomes ("wins every time") that the v1 numbers have not re-validated. Oraga's cards removed exactly this kind of claim.
- **Remedy:** "Three chickens are no danger to anyone. Five are a nuisance. Seven attacking as one mob will genuinely hurt somebody, and the MM should say so with a straight face."

Otherwise the Bestiary makes no Shattered Origin, Val'loh, Thornwall or Church claims. It stays placeless.

### 3d. `characters/*.fof`

All three agree with phb-examples. `Zahna.fof` still names the **Thornwall Artificers' Guild** and its dissolution (specialty, background, magic origin). That text predates the lean pass and is not PHB text, but it is the one live instance of the open ruling.
- **Remedy:** leave it until the owner rules. Add a comment such as `# Owner ruling pending: Artificers' Guild canon status (see docs/RESEARCH_pr29_review.md).`
- The signature workings are new and are flagged in the file and in Rev 5. OK.

---

### B·4. Prose voice: 04, 05 and Val'loh

### Counts

| File | Words | Em-dashes | per 1k | "not X — it is Y"-type | "either…or" |
|---|---|---|---|---|---|
| 04_The_Ball | 9072 | 179 | **19.7** | 7 | 4 |
| 05_The_Longest_Night | 5695 | 124 | **21.7** | 9 | 2 |
| V0 | 793 | 7 | 8.8 | 1 | 0 |
| V1 | 1583 | 14 | 8.8 | 2 | 2 (+2 more hedged either/or quips) |
| V2 | 1081 | 17 | 15.7 | 0 | 0 |
| V3 | 1230 | 11 | 8.9 | 2 | 1 |
| V4 | 626 | 4 | 6.4 | 1 | 0 |
| *Baseline: PHB II.2* | 1034 | 3 | 2.9 | | |
| *Baseline: MM2* | 7070 | 15 | 2.1 | | |
| *04 at pre-lean tag* | 9031 | 178 | 19.7 | | |
| *05 at pre-lean tag* | 5625 | 123 | 21.8 | | |

The lean pass left 04 and 05 prose exactly where it was. Their em-dash density is about **7–10×** the rebuilt PHB/MM house voice. The table counts dashes in table and structure lines too, but those are a small share. Other tics in 04 alone: "quietly" ×8, "deliberately" ×6, "the whole" ×11, "holding its breath" ×2 plus "a household holding its breath" (04:533).

### Oraga 04: flagged passages

1. **Verbatim duplication (structure).**
   - Two read-aloud boxes for the same first sight of the hill: 04:70–74 "*The whole hill is lit. Not with lamps — the walls themselves are doing it…*" and 04:611–617 "*The whole hill is lit. Not lamps — the walls themselves…*".
   - "without a written list — because there is no written list, and with Corval there has never needed to be" appears twice (04:79–80, 04:115–117).
   - "the best gossip hour of the year" appears twice (04:76, 04:607).
   - "Every summons ends the same way: abruptly, with something that is nearly a kindness, and the long walk back" appears twice (04:695–696, 04:736–737).
   - **Fix:** keep B0's box and delete the Movement I "first comes into view" box, keeping only its last line ("*The line ahead of you is long and in no hurry. Every face in it is already a mask.*") appended to B0. Delete the B1 repeat of the Corval sentence ("Where invitations are presented, by name, against Corval's memory."). Keep one copy of the summons line (the box).
2. **04:65–66** "This is not a transition into the ball; it is the first scene of the adventure, and it is where a table learns what rolling feels like in this game." → "The adventure starts here, in the queue, and so does the table's first roll."
3. **04:132–133** "the house that prepared for everything apparently does not care about your knife. Sit with what that implies." This tells the reader how to feel. → "the house that prepared for everything apparently does not care about your knife."
4. **04:156–157**, boxed: "The room is quiet in the particular way of a room that a great many people are deliberately not entering." → "People are standing near the door. Nobody has gone in."
5. **04:184–185** "Someone in this house has been sitting with mortality." → "Someone in this house has been praying to the goddess of death."
6. **04:251–252** "In hindsight, this room is the night's most devastating." This inflated summary adds nothing. → cut.
7. **04:256–257** "(The other way through everything. At midnight, the difference between a tragedy and a massacre.)" → "(At midnight these passages are the only unwarded way out; see Chapter V.)"
8. **04:417–418** "it is *beautiful* — no torture-vault, no horror, which is somehow more unsettling." → "It is beautiful. Players braced for a torture-vault will not know what to do with that."
9. **04:479–481** "The find is a door left ajar on something vast — and it is also, quietly, why rumors 2 through 12 all exist: everyone senses he was *doing something*. Nobody guessed this." → "This is also why rumors 2 through 12 exist: everyone could tell he was doing something. Nobody guessed what."
10. **04:510–513** "nothing sinister — and let the table feel the floor tilt as that lands. … love expressed as logistics. The silent palace was never hiding a crime. It was clearing the decks." This combines a stage direction for the table's feelings, a slogan, and a not-X/Y. → "Nothing sinister. The staff were evacuated, one by one, with a placement found for each. The palace was being emptied on purpose. For what, neither Corval nor the testament says."
11. **04:833** "This hour is the night holding its breath. Run it slow." → "Run this hour slowly."
12. **04:686–687** "Being summoned is an honor, a threat, and a mystery" is a rule-of-three. → "Nobody at the ball can tell whether a summons is an honor or a threat, and everyone watches who goes in."

### Oraga 05: flagged passages

1. **05:392–403, epilogue box: it acts and feels for the PCs.** This breaks the module's own read-aloud rule at 01:98 ("they never say what anyone feels or does"): "You know what you saw… each of you dreams of dancing — a warm hand in yours…".
   - **Fix:** "The fires are out by dawn. By noon there are three stories, one for each faction that needs one, and none of them is yours. No one is ever charged. The fishermen say the mists off the eastern coast are rising again." Then ask the table instead: *"Does anyone still hear that voice from the dance?"*
2. **05:9–11** "this is not a set-piece battle. It is a burning building with three killers out of another age in it, two hundred civilians, and a handful of people — the players — capable of choosing anything at all." → "Treat it as a burning building rather than a battle: three killers, two hundred civilians, and the players."
3. **05:58 and 05:69** repeat the same construction within eleven lines: "Not blown out — drawn out" and "Not blown out — *drunk.*" → keep the boxed one and change 05:69 to "**The lights die**, mid-word, as if the walls forgot sunlight."
4. **05:73–76** "he does not startle, does not finish the sentence, does not waste one second on disbelief" is a triple anaphora. The same pattern recurs at 05:285 ("does not stop, does not answer, does not turn"). → "He doesn't startle. His hand is already at his wrist."
5. **05:141–149**:
   - "aimed straight at the players' better natures … a sight no decent character walks past" presumes the PCs' morals.
   - "and the module notes, without comment, which kind of night the table chose to have" is moralising.
   - **Fix:** "…guests are being robbed as they crawl out of the fire. No Fracture, leash or ward-lore is needed, only a blade. If nobody interferes, the crew gets away clean."
6. **05:161–163** "This is the crescendo, and its rule is simple: … What they can do is everything else, and everything else is what decides it." → "The players can't beat either of them. Everything else they do decides how it ends."
7. **05:166–169** "any player who has watched the three all night understands, wordlessly, that whatever they are, he is the same order of thing" decides a player's understanding. → "Anyone who watched the three all night will recognise how he moves."
8. **05:173–174** "The collision is not fencing — it is pressure and shear" → "They don't fence. Lanterns burst in a line and the balustrade goes to gravel."
9. **05:182–183** "The players carry history in their arms down a garden being demolished behind them." This is inflated and acts for the PCs. → "Whoever takes Veier is carrying her down the stairs while the garden comes apart behind them."
10. **05:226–227** "and a hopeless fight becomes the best scene at the table." → cut.
11. **05:336–338** "They are not cruel, and they are not monsters. They are exactly as dangerous as their terms" → "They aren't cruel. They will do exactly what the contract says, and nothing past the gate."
12. **05:457–460** "The truth without a patron is not power — it is exposure… That is not a dead end. It is a campaign frame" uses two not-X/Ys in three lines. → "With no patron behind it, the truth just makes the players interesting to several organizations at once. The aftermath wing runs on that."
13. **05:426–427** "the module blesses it without reservation" → "and that's fine."

### Val'loh: flagged passages

1. **Duplication.** V0:53–55 and V4:76–80 print the same "What It Adds, Counted" box and paragraph verbatim. V0:59–65 and V4:104–110 are the same "Where to Start" list. **Fix:** keep them in V0. V4 says "See V0 for the full footprint" and keeps only its "Bringing a Core Character In" and "Taking … Out" sections.
2. **V0:13** "That register is not decoration; it is where the Sparks are." → "Sparks come from that register: a table that talks its way through a room earns them the same way a table that fights does."
3. **V0:21** is a five-fragment catalogue ("Ten peoples… A capital city… A god-ordained law… A harvest festival… And a Blackwatch…"), a classic AI list-rhythm. → "Ten human peoples, some born with magic. A capital grown out of crystal. A Church that owns the written word. A harvest festival where the city wears its dead. And a Blackwatch on the coast that isn't sleeping."
4. **V1:3** "the tribes of Val'loh are not different kinds of people. They are the same kind of people, and some of them are born carrying something." → "The tribes of Val'loh are all human; some are born carrying something."
5. **V1, the either/or quip repeated 4× in one chapter:**
   - :31 "which is either why they took to the roads or why the roads have not killed them"
   - :61 "nobody is quite sure which way the causation runs"
   - :117 "whether this is caution or preference"
   - :131 "either excellent craft or a design flaw depending on the device"
   - **Fix:** keep the Tyndi one and flatten the other three. :31 → "Nearly all of them feel trouble coming, which helps on the roads." :117 → "…and leave before the gates shut."
6. **V1:21 and following**: the same sentence is printed nine times ("Minor workings in one Soul or Mind domain of your choice, not a prismatic one"). **Fix:** state it once in the intro (V1:5) and print only "**Gift knack:** *Orthaen gift*." per entry.
7. **V2:29** "The patience is where the fiction lives … and the difficulty ladder is where the game lives." → "Play the patience in the fiction; the dice don't care."
8. **V2:37** "This is the fact the whole economy of Val'loh rests on" → "Most of Val'loh's wealth rests on this."
9. **V3:78–80** "an unexplained low tide is not a gift, it is a held breath. … Keep it in the players' peripheral vision. It matters." → "The Blackwatch are unnerved; they like the sea predictable. Inland it is dinner gossip. Mention it once or twice, in passing."
10. **V3:123** "A blade at a ball is not a threat; it is dress." It repeats V0:41 "Wearing one is dress." → "Wearing a blade to a ball is simply part of being dressed."
11. **V4:68** "This is not a conversion between two games or two settings; it is a different part of one place" → "Val'loh is another part of the same world."
12. **V4:78** "and it is checked against the ruleset data by a test — the pitch cannot drift from the file." This is developer meta in player-facing text. → cut.

---

### B·5. Recommended INVENTIONS entries to add, if the owner keeps the lines

- **Oraga Rev 5:**
  - S1 kinsmen use the Harbor Thug card (M-5).
  - At Oraga, the Bought captain's generic TWISTS 1, 2 and 6 are overridden (O-1).
  - Andra's slate is standing kit (O-15).
- **Oraga Rev 2/4:** falconry mews omen (O-8); "the Just One" epithet (O-9); the Ulan → apostate-hatred line (O-10).
- **Val'loh §7:** the Chiefs' Concourse (V-3); the Phern "three cities" (V-4).

---

# Appendix C — Copyright and licensing (specialist report)


Read-only review, 2026-09-26. Scope: `player_handbook/`, `mm_manual/`, `bestiary/`, `adventures/oraga_night/`, `settings/valloh/`, `Quick_Start.md`, `software/facets/base/facet.yaml`, `software/facets/base/tables.yaml`, `README.md`, `LICENSE.txt`.

### C·Verdict

**No Critical findings.** I found no copied paragraphs, stat blocks, or table entries from a closed work, and no D&D Product Identity monster names. What I did find:

- A handful of **distinctive borrowed labels or phrases**: two Dungeon World GM-move names used verbatim, and 13th Age's "Nastier" stat-block heading.
- **Credits that are inaccurate or incomplete.** Blades in the Dark is not credited, though Borrowed Trouble and Threat Clocks come from it. The 13th Age line credits a mechanic the game does not have. The Whitehack line credits a casting cost that actually comes from Cairn. Cairn's Fatigue-in-slots is not credited.
- A **false blanket claim** at `Front_Matter.md:57` ("None of the works below is quoted").

Web verification was limited because the session's WebSearch budget was already used up (0 searches available). I confirmed these with WebFetch:
- The Dungeon World SRD GM move list (dungeonworldsrd.com/gamemastering).
- Cairn is CC BY-SA 4.0 (github.com/yochaigal/cairn: "The full text is licensed under CC-BY-SA 4.0").
- The FSF license list says CC BY 4.0 is "compatible with all versions of the GNU GPL" and CC BY-SA 4.0 is "one-way compatible with the GNU GPL version 3". It does not mention the OGL.

Everything else relies on my own knowledge plus the project's research files (`docs/RESEARCH_lean_nsr.md`, `docs/RESEARCH_lean_oldschool.md`, `docs/BRIEF_lean_facets.md` §7), and I've marked it as such.

---

### C·1. Findings table

Severity key: **Critical** = likely infringement or license violation. **Major** = a distinctive borrowed term or wording, or a credit that is inaccurate or missing. **Minor** = a credit gap or name overlap with low legal risk. **Nit** = cosmetic.

### Major

**M1. Dungeon World GM-move names used verbatim.** `player_handbook/III.1_Core_Resolution.md:169`
> "The MM makes a move: introduces a new danger, takes something away, reveals an unwelcome truth, or puts someone in a spot."

"Reveal an unwelcome truth" and "Put someone in a spot" are word-for-word GM moves from the Dungeon World SRD (CC BY 3.0; confirmed at dungeonworldsrd.com/gamemastering). "Makes a move" is also PbtA jargon.

Why this matters:
- It makes `Front_Matter.md:57` untrue ("None of the works below is quoted, and none of their text appears here").
- CC BY 3.0 is not on the FSF's list of GPL-compatible licenses (only 4.0 is), and `BRIEF_lean_facets.md` §7 already classes DW as "ideas only".

Short phrases are probably not copyrightable, so the legal risk is low. But the project's own claim and policy are broken.

**Remedy:** reword.
> "On a 6−, things go wrong, and the story moves. The MM answers with trouble: a new danger arrives, something is lost or taken, the characters learn something they'd rather not know, or someone ends up badly placed."

Check that `mm_manual/MM6` "Trouble" table and `MM5` do not repeat the DW phrasing. From my grep they don't.

**M2. Borrowed Trouble is Blades in the Dark's Devil's Bargain, and Blades is not credited.**
- `player_handbook/III.1_Core_Resolution.md:99-105`: "Before a roll, the MM or any player may offer you a complication. Accept it, and add a d6 … **it happens whether you succeed or fail.**"
- Also appears in `Glossary.md:19`, `MM5_Quick_Reference.md:34`, `Quick_Start.md:144`, and `facet.yaml:795`.

The Blades SRD (CC BY 3.0) defines the Devil's Bargain like this: the GM or any player may offer it, you take +1d, and it happens regardless of the roll's outcome. That is the same structure with the same three defining features. The wording here is FoO's own, and the name "Borrowed Trouble" is original, so there is no need to rename. The credit is missing.

**Remedy:** add a Blades line to Credits (see §4).

**M3. Threat Clocks come from Blades and Apocalypse World clocks, not credited.**
- `player_handbook/III.2_Adventuring.md:27-45`: "each gets a **Threat Clock**, a four-segment tracker the whole table can see"
- Also `Glossary.md:141`, `MM2_Session_Design.md:112`, and `facet.yaml:1060` (`threat_clock: segments: 4`).

The segmented progress clock is Blades' signature tool, and its predecessor is Apocalypse World's countdown clocks. The name "Threat Clock" is generic enough to keep.

**Remedy:** credit it in the same Blades line.

**M4. "Nastier" is 13th Age's "Nastier Specials" heading.**
- `bestiary/Front_Matter.md:51`: "**Nastier.** An optional harder version…"
- 17 stat blocks, e.g. `bestiary/B1_Beasts_and_Vermin.md:44`, `bestiary/B3_The_Made.md:135`
- The `nastier:` key in `enemies/*.fof`, e.g. `enemies/city_watch_sergeant.fof:31`

In 13th Age, "Nastier Specials" is the stat-block section for an optional harder version of a monster. That is the same slot with the same purpose. 13th Age is credited, but not for this, and `bestiary/Front_Matter.md:19` says no creature is "mechanically modelled on any proprietary bestiary". The 13th Age core book is proprietary; only the Archmage Engine SRD is OGL.

**Remedy (preferred):** rename the label to **"Rematch:"**. That matches the stated purpose: "for when the party has met this thing before". This is a software change as well:
- The `build_bestiary.py` label.
- The `.fof` key `nastier` → `rematch`, with a deprecation alias like the old `endurance` key.
- The INV no-diff tests.

**Remedy (alternative):** keep the label and add "13th Age's stat blocks gave us the optional 'nastier' version of a monster" to Credits. Also amend `bestiary/Front_Matter.md:19` (see M8).

**M5. The Whitehack credit misattributes the magic cost.** `player_handbook/Front_Matter.md:63`
> "**Whitehack** is where the idea of knacks that never stack, and of casting paid for out of your own hide, comes from."

- **Casting cost.** FoO casting is paid in **Fatigue that fills inventory slots** (`II.3_Magic.md:92-100`, `IV.1_Equipment.md:13`). That is Cairn's mechanic: casting from a spellbook adds Fatigue, which occupies a slot and clears with safe rest. The project's own research traces it there (`docs/RESEARCH_lean_nsr.md:17, 87, 174`). Whitehack's Wise pays for miracles in **HP**, and HP is not what this game uses.
- **Knacks.** "Knack" is FoO's own word. Whitehack's mechanic is called **groups** (vocations, affiliations, species), and the edge from a group doesn't stack (`RESEARCH_lean_nsr.md:259, 278, 290`). The current sentence reads as if Whitehack has "knacks". I could not verify this against the Whitehack text because the search budget was exhausted, so owner should confirm.

**Remedy:**
> "**Whitehack** (Christian Mehrstam): its free-form groups (a vocation, an affiliation, a people) are where our knacks come from, including the rule that they never stack."

Then move the casting cost to Cairn (M6).

**M6. Cairn's Fatigue-in-slots is not credited, and the scar credit is loose.** `player_handbook/Front_Matter.md:61`
> "**Cairn** gave us hit points as grit rather than meat, and the scar a close call leaves behind."

- **Fatigue.** The game uses Cairn's distinctive term **Fatigue** for a condition that fills an inventory slot and clears with safe rest (`II.3:92-96`, `III.2:89`, `IV.1:13`). This is Cairn's most recognizable mechanic after HP-as-grit, and it is not mentioned.
- **Scars.** In Cairn, a scar comes from damage that lands exactly on 0 HP and is often beneficial. In FoO, a Scar is the price of surviving the death choice (`III.2:118-124`). The concept and name are borrowed and the rule is changed. The credit is acceptable but should say "the idea of a permanent scar".
- **Table.** FoO's Scars table (`tables.yaml:348-365`) shares no entries with Cairn's, so it is fine.

**Remedy:** see the corrected Cairn line in §4. Cairn is CC BY-SA 4.0, which is one-way compatible with GPLv3, so even Cairn text could legally be adapted with attribution, and the adapted file would become GPLv3. None is used.

**M7. The 13th Age credit names a mechanic the game doesn't have.** `player_handbook/Front_Matter.md:65`
> "**13th Age** gave us the idea that a character's one unique thing belongs on the sheet…"

I found no "one unique thing" mechanic anywhere in the books or `facet.yaml`. A grep for "unique thing" returns only this line. The Specialty (`II.6:25-33`) is a narrow expertise, not a unique fact about the world. Naming "One Unique Thing" (a distinctive 13th Age term) to credit something that isn't there is inaccurate. It also advertises a 13th Age trademark-adjacent term for no benefit.

What FoO really takes from 13th Age:
- The monster-level table (`MM1_Encounters_and_Enemies.md:74-91`). The numbers are original; I compared them against 13th Age's table, whose level-1 HP is 27, not 8.
- The Mook role (`MM1:103-108`).
- The "Nastier" version (M4).
- Arguably free-text backgrounds as bonuses, which knacks and backgrounds resemble.

**Remedy:** see §4.

**M8. The Bestiary's originality claim is overstated, and the Bestiary has no credits.** `bestiary/Front_Matter.md:19`
> "None of them is derived from, named after, adapted from, or mechanically modelled on any proprietary bestiary…"

The creature names and lore do look original (see §3). But the stat-block *shape* is modelled on published games:
- Level-by-table numbers and the Nastier version come from 13th Age.
- Bloodied comes from D&D 4e, and is now in SRD 5.2.
- Morale comes from B/X.
- Mooks come from 13th Age.

Also, `BRIEF_lean_facets.md` §7 promises acknowledgements in "the PHB and MM Manual", but the MM Manual has none.

**Remedy:** replace the sentence with:
> "Every creature in this book was invented for Facets of Origin. No name, stat block or piece of lore is carried over from a published game. The stat-block format borrows ideas, not words, from other games: monster numbers read off a level table and an optional nastier version (13th Age), a Bloodied threshold (D&D; the term is in the System Reference Document 5.2), and 2d6 morale (the 1981 Basic/Expert rules). The full acknowledgements are in the Player's Handbook front matter."

Add a one-line pointer to the PHB Credits in the MM Manual as well, because MM2, MM4 and MM6 are where the Alexandrian, Sly Flourish, Necropraxis and safety-tool ideas actually live.

**M9. "Nothing is quoted" is untrue until M1 is fixed.** `player_handbook/Front_Matter.md:57`
> "Every sentence and every table in these books is original… None of the works below is quoted, and none of their text appears here."

**Remedy:** fix M1, then keep the sentence. If any open text is ever adapted, change it to "…except where credited below with its license".

### Minor

**m1. End-of-session questions follow Dungeon World's End of Session move.**
- `II.4_Character_Creation_Facets.md:113-117`, `MM3_Campaign_Design.md:127`, `MM5:165`, `facet.yaml:893`
- Quote: "Did we discover something new about the world? … Did we bring treasure home?"

DW asks whether the party learned something new and important about the world, overcame a notable monster, and looted a memorable treasure. FoO paraphrases two of the three, with different wording, and adds three of its own. That is fine as an idea, but it should be credited. The DW credit line currently mentions only the 2d6 bands.

**Remedy:** reword the first question to put more distance from DW, e.g. "Did the world show us something we didn't know?" Add to the DW credit line: "…and that ending a session by asking the table what happened is a better measure of growth than counting kills."

**m2. Oracle Verbs and Themes follow Ironsworn's Action and Theme oracles.** `tables.yaml:629-713`, rendered in MM6.

The pairing structure is Ironsworn's (CC BY 4.0), and Mythic GME had a similar Action/Subject pair before it. The d66 word selections are FoO's own. Any overlap is single common words (e.g. Abandon, Betray, Hunt, Mourn, Reveal, Change) in a different arrangement, so no table is lifted.

**Remedy:** add a credit: "**Ironsworn** (Shawn Tomkin) paired an action with a theme to spark an idea; our oracle tables do the same."

**m3. B/X and OSE procedures are not credited.** Three procedures follow B/X:
- The 2d6 reaction roll (`tables.yaml:23-33`). The bands are different: FoO uses 2-4, 5-6, 7-9, 10-11, 12, where B/X uses 2, 3-5, 6-8, 9-11, 12.
- 2d6 morale against a score with "first to fall" and "half down" triggers (`MM1:134-158`, `III.3:124-130`).
- Exploration turns (`III.2:9`, `MM2:118-124`).

These are generic old-school procedures. The mechanics are not copyrightable, and FoO uses no OGL text.

**Remedy:** add an optional credit line: "**The 1981 Basic/Expert rules** and their open restatements (Old-School Essentials) gave us exploration turns, the reaction roll and the morale check."

**m4. The Three Clue Rule is named without attribution.** `mm_manual/MM2_Session_Design.md:205`: "**The three-clue rule.**"

This is Justin Alexander's named principle. The Alexandrian credit exists but is generic.

**Remedy:** extend the Alexandrian credit with "(the Three Clue Rule, and prep situations not plots)".

**m5. Safety tools lack individual creators.** `MM4_Running_the_Table.md:69-83`
- The X-Card was created by John Stavropoulos. Its official text is CC BY-SA 3.0; FoO uses its own words.
- Lines and Veils come from Ron Edwards (*Sex & Sorcery*).
- Stars and wishes come from Lu Quade.
- The Toolkit credit to Shaw and Bryant-Monk is correct.

**Remedy:** see §4.

**m6. Talent names overlap D&D 5e feat names.** `II.4a:91, 103, 113, 193`; `II.4b:155`; `II.4c:115`
- **Weapon Master, Sentinel, Tough, Athlete, Linguist, Lucky** are six names shared with the 2014 5e PHB feat list, which is proprietary and not in SRD 5.1.
- **Second Wind, Counterspell, Cleave, Whirlwind** are also D&D names, but these are in the SRDs (CC BY 4.0 / OGL) or generic.

Every mechanic is FoO's own. I read Sentinel, Tough, Athlete, Lucky, Linguist and Second Wind, and none paraphrases 5e. Single-word titles aren't copyrightable, so this is low risk. But the cluster of six reads as a feat list lifted from D&D.

**Remedy (optional):** rename two or three so the cluster breaks up:
- Sentinel → *Shield-Wall*
- Tough → *Hard to Drop*
- Athlete → *Sure-Footed*
- Lucky → *Charmed*

Keep the rest.

**m7. Morrowind needs a trademark disclaimer.**
- `Front_Matter.md:69` and the veiled reference at `II.4:45`.
- Only the idea is used (a class written inside a broad specialization). Naming it in credits is nominative fair use.

**Remedy:** add a trademark notice (§4).

**m8. README does not point to the acknowledgements.** `README.md:152-154` says only "GPLv3 — see `LICENSE.txt`". `LICENSE.txt` is the unmodified GPLv3 text, which is correct.

**Remedy:** add to README:
> "Game ideas borrowed from other games are acknowledged in `player_handbook/Front_Matter.md` (Credits). No third-party text is incorporated. Product names mentioned there are trademarks of their owners and imply no affiliation."

### Nit

**n1.** Talent entries print a **"Normal:"** line (`II.4a:89`). This is the D&D 3.x feat format from the d20 SRD (OGL). Format conventions are not protectable. It is already covered by the style guide's 3.5 lineage, so no action is needed.

**n2.** **Bloodied** (`III.3:120`, `Glossary.md:15`) originated in D&D 4e and is now a defined term in SRD 5.2 (CC BY 4.0). It is also used generically across the hobby. No action is needed beyond M8's mention.

**n3.** **Mook** (`MM1:103`, `III.3:112`) is pulp and film vocabulary, also used in Feng Shui and 13th Age. It is generic.

**n4.** "If failure would just mean nothing happens, don't roll: say yes" (`III.1:156`) is the well-known "say yes or roll the dice" principle from Vincent Baker's *Dogs in the Vineyard*. It is expressed in FoO's own words, so no action is needed. Credit is optional.

**n5.** Usage die mechanics (`IV.1:77-83`): a roll of 1-2 steps the die down, d8 → d6 → d4 → gone. This is The Black Hack's mechanic, and it is correctly credited. The Black Hack is OGL, and no text is used.

**n6.** The Pressure die (`tables.yaml:81-92`) faces are Encounter, Sign, Local hazard, Cost, Opportunity, Quiet. That follows the order of Necropraxis's overloaded encounter die (encounter, spoor/sign, locality, exhaustion/expiration, …). The entries are FoO's own words, and the credit is accurate. I could not fetch the Necropraxis page (the old URL returns 404).

---

### C·2. Term-by-term sweep

These were grepped across all scoped books and YAML, excluding the generated `Index.md`. Classification codes:
- **(a)** generic genre vocabulary
- **(b)** borrowed concept in original words, which should be acknowledged
- **(c)** distinctive borrowed name or wording, which should be renamed or explicitly credited

| Term | Hits | Class | Notes |
|---|---|---|---|
| Hack and Slash, Defy Danger, Spout Lore, Discern Realities, Last Breath | 0 | — | Clean |
| Volley | 2 (`Appendix_Magic_Domains.md:301,308`) | a | "a volley of arrows" |
| Parley | 1 (`MM1:164`) | a | ordinary English |
| Bonds | 1 (`settings/valloh/V1_Lineages.md:75`, "bond to a single blade") | a | not DW Bonds |
| hold | 153 | a | ordinary usage; no PbtA "hold 3" |
| Fatigue | 101 | **b** | Cairn mechanic; credit is missing (M6) |
| Deprived, Critical Damage | 0 | — | |
| Scar(s) | 36 | b | Cairn idea, rule changed; credited (M6) |
| Usage die | 34 | b | The Black Hack; credited |
| cypher | 0 | — | |
| One Unique Thing | 1 (credits only) | **c** in credits | mechanic absent (M7) |
| Icons | 0 | — | |
| Escalation (die) | 0 as a mechanic | a | |
| Position and Effect, Devil's bargain, Flashback, Stress | 0 | — | Borrowed Trouble is a Devil's Bargain concept (M2) |
| Trauma | 1 (`MM4:65`, tone) | a | |
| Clock(s) | 71 | **b** | Blades / Apocalypse World; not credited (M3) |
| Momentum, Iron vow, Face Danger, Secure an Advantage, Pay the Price | 0 | — | the Ironsworn oracle structure is used (m2) |
| Burn | 37 | a | fire |
| knack | 179 | b | own word; Whitehack groups concept (M5) |
| Pressure die | 70 | b | Necropraxis; credited |
| overloaded encounter die | 1 (credits) | — | correct |
| Bloodied | 70 | a/b | 4e origin, now SRD 5.2 (n2) |
| Mook | 77 | a | (n3) |
| torch | 20 | a | no Shadowdark real-time torch |
| Crawl | 2 | a | |
| slots | 141 | b | Knave; credited |
| Deed | 3 | a | |
| Mishap | 14 | a | "Magic Mishaps" is generic; the table is original |
| talent | 305 | a | chosen from a menu, not Shadowdark's rolled talent tables |
| Luck token, torch timer | 0 | — | |
| grit | 52 | b | Cairn / Into the Odd; credited |
| **Nastier** | 18 + `.fof` | **c** | 13th Age (M4) |
| reveal an unwelcome truth / put someone in a spot | 1 | **c** | DW verbatim (M1) |
| three-clue rule | 1 | b | Alexandrian (m4) |
| X-card, lines and veils | several | b | m5 |

---

### C·3. Table, creature and name spot-checks

- **Bestiary creatures.** Latchmen / Archive Guardian, The Waiting, The Unfinished, Hushfall, The Ordinary Dangerous, The Bought (Blades, Sergeant, Captain), The Kindly, Chalk Hounds, Glassbacks, Ledgerlice, The Chicken. All look original.
  - "The Kindly" echoes the classical euphemism "the Kindly Ones" for the Furies. That is public domain and fine.
  - I found no D&D Product Identity names (beholder, mind flayer/illithid, displacer beast, githyanki/githzerai, owlbear, umber hulk, carrion crawler, yuan-ti, kuo-toa, slaad, tarrasque, drow, gelatinous cube, rust monster, bulette, myconid, aboleth, kenku, tabaxi, dragonborn, tiefling, warforged, modron, beholder-kin).
  - "ogre" appears once as a generic folklore example (`III.3:21`, `MM1:130`).
  - I found no Forgotten Realms, Greyhawk, Eberron or Morrowind setting names (no Dunmer, Daedra, Tribunal, Vvardenfell, etc.).
- **Trinkets** (`tables.yaml:370-411`). Original. I compared them against the 5e PHB trinket list from memory. Overlap is only generic objects (a tooth, a lock of hair), with different wording.
- **Curios and Relics** (`tables.yaml:413-468`). Original names (Patient Lantern, Sexton's Spade, Courteous Knocker…) and original mechanics. Not Shadowdark or OSE items.
- **Wounds and Scars** (`tables.yaml:335-365`). No entry matches Cairn's scar table (Lasting Scar, Rattling Blow, Walloped, Broken Limb, Diseased, Reorienting Head Wound, Hamstrung, Deafened, Re-Brained, Sundered, Gutted, Doomed).
- **Magic Complications and Mishaps** (`tables.yaml:293-331`). Original. They don't match Shadowdark's wizard mishap tables or DCC's corruption tables.
- **NPC names, traits, wants and secrets.** Original. The names are common real-world given names, so there's no issue.
- **Reaction table.** B/X concept with different bands and original text (m3).
- **Monster level table** (`MM1:78-91`). The numbers are original (level 1: HP 8, damage 4, attack +1). 13th Age's are much larger, so the only thing shared is the idea of a single table (credited).
- **Class and talent names.** Preset classes (Warrior, Scout, Guardian, Brawler, Thaumaturge, Investigator, Physician, Tactician, Invoker, Speaker, Wanderer, Captain) are generic. Talent names are covered in m6.
- **Valloh lineages and Oraga Night.** These are covered by the existing canon process. The grep found no borrowed game terms.

---

### C·4. License-compatibility assessment

- **Is any openly licensed TEXT incorporated?** Only the two DW move names at `III.1:169` (M1). Everything else I checked is original wording, so no CC attribution or share-alike obligation is currently triggered. Fix M1 and the books contain no third-party text.
- **CC BY 4.0** (Knave 1e, Ironsworn, SRD 5.1/5.2). FSF says this is compatible with all GPL versions, so adapting text would be allowed with attribution.
- **CC BY-SA 4.0** (Cairn). One-way compatible into GPLv3 (FSF and CC both say so). Adapted text is allowed with attribution, and the adapted work goes out under GPLv3. No text is currently used.
- **CC BY 3.0** (Dungeon World, Blades SRD). FSF lists only CC BY 4.0 as GPL-compatible, and `BRIEF §7` already classes these as ideas-only. Keep it that way, which is why M1 should be reworded rather than attributed.
- **OGL 1.0a** (The Black Hack, 13th Age Archmage Engine SRD, OSE SRD).
  - Using Open Game Content would require:
    - Including the OGL text.
    - Honouring the Product Identity exclusions.
    - Accepting §7's ban on indicating compatibility with trademarks.
  - Those are further restrictions that GPLv3 §7/§10 forbid, so the two are generally regarded as incompatible.
  - **Therefore no OGL text may enter the books.** None has.
  - Crediting these games by name for ideas, as the Credits do, is plain nominative reference and triggers nothing.
  - Unverified: the BRIEF lists Whitehack under OGL. I could not confirm this, and Whitehack may simply be all-rights-reserved. Either way it's ideas-only.
- **Proprietary** (Shadowdark, 13th Age core, Into the Odd — the original 2014 edition is not openly licensed and I could not verify the Remastered edition's terms — Knave 2e, which I could not verify, and Morrowind). Ideas only. FoO complies.
- **Shadowdark.** None of its distinctive terms appear (rolled talent tables, Luck tokens, real-time torch). No credit is needed, but it would be harmless.

---

### C·5. Proposed corrected Credits section — `player_handbook/Front_Matter.md` (replaces lines 53-73)

```markdown
### C·Credits and Acknowledgments

Facets of Origin is created and maintained by its contributors; the full list lives in the project repository.

Every sentence and every table in these books is original. The game does borrow *ideas*, and we would rather say so plainly. None of the works below is quoted, and none of their text appears here. Game mechanics are free to share; the words and tables that express them are each author's own, and we have written ours from scratch.

- **Dungeon World** (Sage LaTorra and Adam Koebel) showed that a three-band 2d6 roll could carry a whole fantasy game, that a hit on a partial success is worth more than a miss, and that ending a session by asking the table what happened is a better measure of growth than counting kills.
- **Blades in the Dark** (John Harper) gave us the segmented clock that puts a timer on a hazard, and the bargain behind Borrowed Trouble: take the extra die, and the trouble comes whatever the dice say.
- **Knave** (Ben Milton) gave us inventory slots that do double duty, holding wounds as well as gear, and kit that tells you who a character is.
- **Cairn** (Yochai Gal) gave us hit points as grit rather than meat, Fatigue that takes up room in your pack, and the idea of a permanent scar.
- **Into the Odd** (Chris McDowall) showed how little a fight needs: damage that bites, and a roll to avoid harm only when the danger is real.
- **Whitehack** (Christian Mehrstam): its free-form groups are where our knacks come from, including the rule that they never stack.
- **The Black Hack** (David Black) gave us the usage die and the habit of letting players roll what matters.
- **13th Age** (Rob Heinsoo and Jonathan Tweet) showed that a monster's numbers can come off a single table by level, that a crowd of mooks can be one threat, and that a monster can print a nastier version of itself.
- **Ironsworn** (Shawn Tomkin) paired an action with a theme to spark an idea; our oracle tables do the same.
- **The 1981 Basic/Expert rules**, and their open restatements such as Old-School Essentials (Gavin Norman), gave us exploration turns, the reaction roll and the morale check.
- **Necropraxis** (Brendan S.) and the overloaded encounter die are the root of our Pressure die.
- **The Alexandrian** (Justin Alexander) shaped the MM's side: the Three Clue Rule, prep that survives contact with players, and situations instead of plots.
- **Sly Flourish** (Mike Shea) taught a generation that lazy prep is good prep, and the MM Manual listened.
- **Morrowind** gave us the shape of the class system: a broad specialization that owns the numbers, with the freedom to write your own class inside it.

The safety tools discussed in MM4 draw on the **TTRPG Safety Toolkit**, curated by **Kienna Shaw and Lauren Bryant-Monk** and freely available online. The **X-Card** was created by **John Stavropoulos**; **lines and veils** come from **Ron Edwards**; **stars and wishes** from **Lu Quade**.

Product names in this section are trademarks of their respective owners. They are named only to give credit; Facets of Origin is not affiliated with or endorsed by any of them.

Openly licensed material incorporated in future revisions will be credited here with its source and license, as the project's contribution policy requires. Only text under licenses compatible with the GNU GPL version 3 (for example CC BY 4.0 or CC BY-SA 4.0) may be incorporated; material under the Open Game License, CC BY 3.0 or a proprietary license is used for ideas only.
```

Note on the M4 alternative: if "Nastier" is renamed to "Rematch", change the 13th Age line's last clause to "…and that a monster can print a harder version of itself".

---

### C·6. Action list (priority order)

1. **M1:** reword `III.1_Core_Resolution.md:169`. This is needed to make `Front_Matter.md:57` true.
2. **M2, M3, M5, M6, M7, m1-m5, m7:** replace the Credits section with §5.
3. **M4:** rename "Nastier" to "Rematch". This touches `bestiary/*`, `enemies/*.fof`, and the `oraga_night` enemy `.fof` files if any use the key, plus the generator, schema and tests. Alternatively, keep it and rely on the credit.
4. **M8:** amend `bestiary/Front_Matter.md:19` and add a credits pointer to the Bestiary and the MM Manual.
5. **m8:** add the README acknowledgement and trademark line.
6. **m6** (optional): rename two or three talents.
