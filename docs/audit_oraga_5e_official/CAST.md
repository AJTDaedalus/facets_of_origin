# Official-Standard Audit — Slice CAST (07 Cast, 08 MM Sheet and Handouts, 11 Pregens)

*2026-09-30. Audit only; no module file was edited. Yardsticks:
`docs/RESEARCH_5e_module_conventions_structure.md` (C-S), `docs/RESEARCH_5e_module_conventions_voice.md`
(C-V, S). Evidence also from the CoS handouts appendix (text-extracted, format only) and
the source pregens in `adventures/oraga_night/characters/*.fof`.*

**Level note.** The shared brief said "3rd level, 2014 PHB". The owner's ruling (FIXPLAN §6)
sets the party at **4th level**, and chapter XI builds the pregens at 4th under **SRD 5.2.1**.
All pregen legality below was checked at 4th level against SRD 5.2.1. The 2014 case is
covered only as the chapter's own "At a 2014 table" note (CAST-12). The script is
`/tmp/claude-0/-root-facets-of-origin/a69f14e1-998c-493e-9f3a-649283070f5d/scratchpad/pregen_check.py`.
It re-derives base array, background bonus, ASI, HP, AC, Initiative, passive Perception, every
skill total, the number of skill sources, spell DC and attack, cantrip and prepared counts,
and Andra's spellbook. Result: **no arithmetic errors.**

---

## 1. Summary

| Dimension | Verdict |
|---|---|
| **PROSE** | Good voice, near official sentence norms (07 mean 18.7 words, median 15). It has no "PCs", no designer "we", no rhetorical questions and no exclamation marks. Off-standard habits: the module talks about itself as a character ("the module notes / suggests / would prefer"), "player" often stands in for "character", and the em-dash density is high (about 21 per 1,000 words in 07). |
| **MECHANICS** | Pregens are **legal and arithmetically correct at 4th level, SRD 5.2.1**, and every subclass is in the SRD. The problems are elsewhere. One pregen has no legal casting focus. The 2014 note keeps scores a 2014 build can't reach. Vell's DCs name no ability. Several rows of the Key DCs table name no ability or skill. The biggest gap is that the Attendant answers every question *truthfully* and nothing it says is written down. |
| **STYLING** | Handouts are named consistently, and 2 of 3 are dealt at a stated moment. Handout 3 is an MM table filed as a handout. Handouts sit mid-book, not last. Capitalization and item names are mixed between 11/08 and chapter X. Box labels in 07 don't match the legend's declared species. |
| **CONTENT** | Every stat block named in 07 exists in chapter X under exactly that name (22 checked), and non-combatants get a fallback line. The missing piece is the "what they know" list: only Vorlain, Corval and the Bought have one, which is short of an [always] convention in a social module. The pregens also lack ideal, bond and flaw. |

**Top five**
1. **CAST-1 (P1).** The Attendant must answer any direct question literally and truthfully, but none of its answers are written down, and the questions players will ask land on *What the Module Never Says*.
2. **CAST-2 (P2).** Eleven talkable NPCs have no "what they know" list. Agenda 4 and Agenda 8 both end in a conversation (Veier, Anha) the book doesn't script.
3. **CAST-8 / CAST-9 (P2).** Handout 3 is an MM table with MM notes inside it. Handout 1 has no trigger and no recipient.
4. **CAST-5 / CAST-6 (P2).** Meta-winks ("the module would prefer…"), and "player" used for the character, across 07.
5. **CAST-11 (P2).** Andra has no legal spellcasting focus, so her AC 15 from *mage armor* can't legally be cast. Ilesse's focus isn't a Holy Symbol.

---

## 2. Findings

### P1

### CAST-1 [P1] The Attendant answers every direct question truthfully, and the book never says what it answers (CONTENT) [d20-portable]
- **Where:** 07:458-466 (the habit) and 07:482-484 ("answers exactly the question asked"). Also 10:194 ("answers literally and truthfully"), 04:1086-1091 (the Movement III sighting that teaches it), and 09:1731 ("A direct question it must answer is a habit").
- **Yardstick:** C-S29 [always]; C-V11; structure §5.3 ("Every secret the players might extract is written down; none is left to improvisation").
- **Problem:** The module teaches this habit on purpose and pays +2 for using it at midnight. The first things a table asks a thing that *can't refuse and can't lie* are "Who is your master?", "What are the three?" and "Where did you come from?". Those questions run straight into *What the Module Never Says* (02:230-240: the name of the power in the east, and who the Uninvited were). The only scripted answer is "Asked whom it serves, it names no one". Everything else is improvised on the most canon-sensitive ground in the book, under the pressure of a boss fight.
- **Fix:** Add a sidebar after *Play it* titled **What the Attendant Answers**, with a trigger sentence and bullets. Use existing canon only:
  - *Whom do you serve?* It names no one, and looks around for the master (07:460; 04:935).
  - *What are you doing?* Before midnight: "Watching." After midnight: keeping the three from being interrupted (its orders, 07:453-454).
  - *Are you with them?* Yes. It came through with them (07:450). **NEEDS-RULING**: may it say so aloud?
  - *Anything on the Never-Says list:* **NEEDS-RULING** (N1). Give the owner a choice of dodge that keeps "truthfully" honest. (a) It answers the literal words, which are never the question the player meant. (b) It was made, not told, so it doesn't know. (c) It answers with the absence of its master.

  Make 10:194 match whichever the owner picks.

### P2

### CAST-2 [P2] Most talkable NPCs have no written "what they know" (CONTENT) [d20-portable]
- **Where:** 07. Raunu 22-43, Veier 60-76, Anha 210-222, Kovaun 231-241, Sella 249-260, Callun 265-274, Corro 281-292, Draunel 300-307, Essin 313-322, Maiven 329-343, Tavva 502-522. Only Vorlain (110-141), Corval (167-203) and the Bought (554-588) have one.
- **Yardstick:** C-S29 [always]; C-V11; structure §5.3 (bulleted fact list after a trigger sentence, untrue items flagged).
- **Problem:** This is a talking module. Agenda 8 ends in a conversation with Anha ("Getting her to talk… is the night's work", 03) and Agenda 4 ends in one with Veier. For both, the MM gets character prose, not the list of facts they hand over. Anha's facts are scattered across her *Secret* line (07:211-215), Undercurrent A's trail (04:593-596) and Undercurrent C's spark (04:734).
- **Fix:** For each NPC, add a trigger sentence plus bullets, **assembled only from facts already printed**. Worked example for Anha:
  > Characters who win Anha's trust (family or kindness; pressure gets nothing) learn the following:
  > - The east wing's lights burn all night.
  > - Meals for two go up. These last months, plates for three come back down.
  > - She has heard the master's voice in empty rooms.
  > - There are corridors she is forbidden to sweep.
  > - For two years, supplies have gone down the lower cellar stair and never come back up: candles, lamp-oil, and once a salt-packed crate from the eastern coast that hissed. (Once befriended, she offers this unprompted.)
  > - She knows the service passages. With her, no check (chapter IV, area B10).

  Do the same for Tavva (07:519-521: she can prove she planned the gallery job for a season), Sella (07:251-254: what Raunu asked her at the wedding; the fresh offerings are hers) and Essin (07:315-317). Raunu's list should say plainly what he will not answer (the Never-Says items). Veier's needs a ruling on the heir (N2, owner ruling R6). Put a trailing "(untrue)" on any belief the NPC holds that the MM knows is false.

### CAST-3 [P2] The chapter promises a DC in every entry, but half the entries have none (MECHANICS) [d20-portable]
- **Where:** The promise is at 07:5-6. Entries with no DC: Veier, Sella, Corro, Draunel, Maiven, Tavva, the Attendant before midnight, and the Bought Sergeant (his DC 13 appears only in 08:86).
- **Yardstick:** C-V15 [always], C-V12. Official social NPCs state what moves them and how hard it is.
- **Problem:** The MM who opens 07 to find how hard Draunel is to move gets nothing. 04:410-412 sends the MM to 07 for exactly this.
- **Fix:** Don't invent a DC for each NPC. Change the intro to state the default: "*Outside a fight NPCs never roll dice. Where an entry gives no DC, moving that guest is DC 13 behind a mask (the ladder in chapter I); the entries below note only the exceptions.*" Add to the Sergeant: "Voiding the contract is DC 13 Charisma (Persuasion); see card S3."

### CAST-4 [P2] Vell's DCs name no ability, and one check hides behind an undefined gate (MECHANICS) [d20-portable in shape]
- **Where:** 07:376-378 ("make all social pressure on Vell **DC 25**"), 07:384-386 ("A player with an exceptional will… DC 25 Wisdom (Insight)"), and 08:106 ("move Vell | 25").
- **Yardstick:** C-V15 [always] ("DC N Ability (Skill) check").
- **Problem:** "Social pressure" doesn't say which roll, and "an exceptional will" is not a rules term. The MM has to decide at the table who is allowed to roll.
- **Fix:** At 376-378, "make every Charisma check to move Vell (Deception, Intimidation or Persuasion) DC 25, and let even a success buy honesty rather than compliance". At 384-386, "A character who studies him directly can make a DC 25 Wisdom (Insight) check to notice the nudge; on a success, they learn the most dangerous piece of information at the ball: someone is editing you." In 08 Table VIII–3, "25 Charisma".

### CAST-5 [P2] The module appears as a character in DM prose (PROSE) [d20-portable]
- **Where:** 07:83 ("the module suggests spending it"), 270 ("the module notes the resemblance to her host without comment"), 342-343 ("The module would prefer somebody competent went with her."), 397-398 ("a killer the module has spent two chapters establishing as unbeatable") and 515 ("the module notes she would be genuinely offended").
- **Yardstick:** C-V13 [always]: no winks or meta-commentary in DM prose. Official humor is a deadpan informational one-liner.
- **Problem:** These read as the author nudging the MM, which official books never do. **Keep** 07:369 and 400-401 ("the module does not say" / "never explains him"). The legend (01:350) makes that phrase load-bearing.
- **Fix:**
  - 83: "the module suggests spending it on" → "spend it on".
  - 270: "She is merely *prepared* — the module notes the resemblance to her host without comment." → "She is merely prepared, like her host."
  - 342-343: cut "The module would prefer somebody competent went with her."
  - 397-398: "a killer the module has spent two chapters establishing as unbeatable" → "a killer nothing else tonight can stop".
  - 515: "and the module notes she would be genuinely offended to learn it" → "and she would be offended to learn it".

### CAST-6 [P2] "Player" used for the character in DM prose (PROSE) [d20-portable]
- **Where:** 07:65, 67, 221, 257, 289, 320, 340, 366, 378, 384, 391, 398, 403 (13 lines). Keep 37, 161, 371, 435 and 465, which mean the real people.
- **Yardstick:** C-V2 [always] ("the players" means only real people at the table).
- **Fix:** Swap in "character". Examples: 65 "reachable only by characters who earn the east wing"; 257 "where shaken characters wash up"; 320 and 340 "the Agenda 3 character's", "the Agenda 4 character's"; 391 "Characters standing between him and the river gate".

### CAST-7 [P2] AI rhythm in a few places: em-dash chains and "not X. It is Y" (PROSE) [d20-portable]
- **Where:** 07 has 129 em dashes in 6,166 words (about 21 per 1,000), and 10 lines carry two or more. Worst spots: 102-104, 161, 380-381, 427-428 and 488-495.
- **Yardstick:** Owner memory rule (no AI rhythm); C-V4/C-V5.
- **Fix (light touch; keep the voice and the jokes, including "load-bearing wall", which is character comedy):**
  - 102-104: "Drunk (it takes real work — an hour of pouring, and a DC 15 Charisma (Persuasion) check to keep him at it — and Essin will try to stop it), he says one true thing:" → "Getting him drunk takes an hour of pouring and a DC 15 Charisma (Persuasion) check to keep him at it, and Essin will try to stop it. Drunk, he says one true thing:". Also cut the quoted line that follows (104-105), because the box repeats it (CAST-18).
  - 161: "Bribing Corval is impossible — not DC 20, *impossible*, tell the players so." → "Bribing Corval is impossible. There is no check; tell the players so." (This matches 10's wording.)
  - 380-381: "never once interesting to look at — and that last is not luck." → "never once interesting to look at. That is not luck."
  - 427-428: "What makes them monstrous is not what was taken from them. It is how much is left." → "What makes them monstrous is how much of them is left."
  - 488-495: split the one long sentence into four, one per state change: Idle, Focused, the fourth broken focus, and 0 hit points.

### CAST-8 [P2] Handout 3 is an MM table filed as a player handout (STYLING/CONTENT) [d20-portable]
- **Where:** 08:296-316.
- **Yardstick:** C-S48 [always]; structure §10.1 (handouts are player-facing; the CoS handouts appendix carries in-world text only, with no DM notes on the page).
- **Problem:** The intro is MM instruction ("Roll 2d6 in any social scene, or choose"). Rumor 7 carries "(The common one.)" and rumor 12 carries "(Deliver this one straight. Let the table sit with it at dawn.)". Printed and handed over as a "Handout", these leak MM notes. Nothing says who receives it, and in practice nobody does, because the MM rolls it.
- **Fix:** Retitle it as an MM table, "**Rumors at the Ball** *(MM table)*", keep Table VIII–7, and drop "Handout 3". If the owner wants a player-facing recap (C-S49 [sometimes], a pacing option), make it a separate handout with the MM parentheticals removed.

### CAST-9 [P2] Handout 1 has no trigger and no recipient (STYLING) [d20-portable]
- **Where:** 08:225-239. Compare 01:122 ("put out… the invitation").
- **Yardstick:** C-S48 [always] (the trigger names who gets the handout).
- **Fix:** Add under the heading: "*Put it on the table in the first five minutes (chapter I). In the fiction it is the card a character with **The Invited** hook carries to the gate (chapter IV, area B1). A character with **The Discarded Invitation** hook carries one with someone else's name on it.*" Every fact here is already canon (01 Table I–2; 02:18-20). **Don't touch the invitation text.** It is marked canonical, so its "Guest"/"you all" mismatch and the repeated "revelry" stay.

### CAST-10 [P2] Pregens lack ideal, bond and flaw (CONTENT) [d20-portable]
- **Where:** 11, every sheet. Each has *Personality* prose, an *Agenda hook* and a *Mask* question.
- **Yardstick:** C-S50 [usually]; structure §10.2 (the LMoP pregen convention: two traits, ideal, bond, flaw, background, adventure tie).
- **Problem:** The adventure tie is there (the agenda hook, which does the job of a bond). The ideal, bond and flaw lines that 5e players expect to find on a sheet, and that pay Inspiration at a 5e table, are not.
- **Fix:** Draw the **Ideal** from existing canon: the first-person class concept in each source `.fof`.
  - Serane: "I am the voice that ends fights before they start."
  - Pello: "I carry other people's valuables through dangerous country, and lose none of them."
  - Andra: "I keep the record of a pattern nobody else believes is there."
  - Dassa: "I am a shield for the people behind me."
  - Ilesse: "I carry words between people who cannot be seen talking to each other."

  Relabel the agenda hook **Bond**. The **Flaw** is NEEDS-RULING (N3); canon gives none.

### CAST-11 [P2] Andra has no legal spellcasting focus; Ilesse's focus isn't a Holy Symbol (MECHANICS) [not portable]
- **Where:** 11:251 ("the lattice as focus"), 11:262-263 (Carrying), 11:416-417 (Ilesse's crystal focus), and 11:407-411 (Channel Divinity). Compare 03:150-152 (the lattice *is* the spellbook) and 03:99 (the gift sliver is a focus for the gift cantrip only).
- **Yardstick:** SRD 5.2.1. A wizard's focus is an Arcane Focus (a spellbook isn't one). A cleric's focus is a Holy Symbol, and Turn Undead and Preserve Life are used by presenting it [verify 5.2.1].
- **Problem:** Andra carries no component pouch or arcane focus. *Mage armor*, *sleep* and *silent image* all have material components, so the AC 15 the sheet opens with can't legally be cast. Ilesse has a focus for her gift cantrip, not for her cleric spells.
- **Fix:** For Andra, 251 "…attack +6; a crystal as arcane focus". Add "crystal (arcane focus)" to Carrying. Crystal is on the SRD's arcane-focus list, so this needs no new canon. For Ilesse, either add a component pouch to Carrying (it covers spells but not Channel Divinity) or rule that her warding crystal serves as her Holy Symbol (N4, since "what answers her, the module does not say").

### CAST-12 [P2] "At a 2014 table" keeps ability scores a 2014 build can't reach (MECHANICS) [not portable]
- **Where:** 11:45-46.
- **Yardstick:** 2014 PHB (standard array, human +1 to all or variant +1/+1, one ASI at 4th).
- **Problem:** Pello's DEX 19 and Andra's INT 19 come from the 5.2.1 background +2 plus a +2 ASI. A 2014 standard-array human tops out at 18 by 4th level.
- **Fix:** "*At a 2014 table:* keep the concept and the equipment, and rebuild ability scores and class features from your own rules (a 2014 standard-array human reaches 18, not 19). The gift is the variant human's feat (chapter III)."

### CAST-13 [P2] Capitalization and item names are mixed between 11/08 and chapter X (STYLING) [not portable]
- **Where:**
  - 11:108-109, 262-263, 426-427 use italic lowercase charge names (*steady light*, *a sealed door*, *a veil of quiet*, *a held image*, *a chime at a threshold*). 10's *Items of the Night* uses **Steady Light**, **A Sealed Door**, and so on.
  - 11 has 5.2.1 capitals (Initiative, Bloodied, Heroic Inspiration) beside 2014 lowercase: "short rest/long rest" (11:94, 243, 327, 331, 407), "advantage/disadvantage" (80, 89, 155, 175), "speed is 0" (176), "hit points" in prose.
  - 08 has "Unconscious and Stable", "Prone" and "Heroic Inspiration" beside "disadvantage" and "difficult terrain" (08:52-79).
- **Yardstick:** C-V26 [always]; voice §12 (pick one scheme).
- **Fix:** Match chapter X (5.2.1). In 11, write charges exactly as 10 does; write "Short Rest/Long Rest", "Advantage/Disadvantage", "Speed", "Difficult Terrain". Spell names follow whatever scheme the module-wide decision picks (other slices will hit the same issue).

### CAST-14 [P2] Key DCs table rows with no ability or skill (MECHANICS) [not portable]
- **Where:** 08:98 ("The line's first check (B0) | 13"), 99 ("An approach across station, behind a mask | 10"), 100 ("Identify a masked guest… | 15 / 20") and 103 ("15 / 18 thieves' tools").
- **Yardstick:** C-V15 [always].
- **Fix:** Take each from its source text:
  - 98: "13 Charisma (Persuasion) or Wisdom (Insight)" (04:178-179).
  - 99: "10, the check that fits the approach" (04:414-415).
  - 100: "15 / 20 Wisdom (Insight)" (03:181-182).
  - 103: "15 / 18 Dexterity (thieves' tools)".

  The midnight-rules bullets' shorthand ("DC 15 Str or Dex save", "DC 13 Persuasion") is acceptable quick-reference compression. Leave it.

### P3

### CAST-15 [P3] Cast headers are uneven (STYLING) [d20-portable]
- **Where:** Six faction entries have no italic apposition line: Kovaun 231, Callun 264, Corro 280, Draunel 299, Essin 312, Maiven 328. The Bought Sergeant (540) and Captain (563) have no stat-block pointer of their own.
- **Yardstick:** C-S27 [always] (one convention used throughout); C-S28.
- **Fix:** Add appositions built from existing labels (chapter X subtitles and chapter III patrons):
  - Kovaun: "*Prelate of the Church; Agenda 2's patron.*"
  - Callun: "*Mistress of the Merchant's Circle; Agenda 1's patron.*"
  - Corro: "*The Phern magnate.*"
  - Draunel: "*Lord of House Draunel; Agenda 3's patron.*"
  - Essin: "*Vorlain's cousin.*"
  - Maiven: "*Veier's cousin; Agenda 4's patron.*"

  Give the Sergeant and the Captain "**If it comes to steel:** stat block **Bought Sergeant** / **Bought Captain**; card S3."

### CAST-16 [P3] The personality block uses a house shape, not one of the four official ones (STYLING) [d20-portable]
- **Where:** Every 07 entry (Wants / Fears / Secret / Play him).
- **Yardstick:** C-S28 [usually]; C-V10 (motive as a plain verb; no labeled "Motivation:" field in any hardcover).
- **Assessment:** This is a house choice, and it works. It maps onto the DMG's NPC vocabulary (ideal, flaw, secret), and the secrets are stated flatly to the MM, which is exactly the official habit. Keep it. Optional polish: rename *Play him/her* to **Roleplaying [Name]** (format D). Where an entry already has a signature line (Veier 73-74, Sella 258-260, Vell 366 and 406, Vorlain's drunk line), set it as a **Quote:** line. Write no new dialogue.

### CAST-17 [P3] Box labels don't match the legend's box species (STYLING) [d20-portable]
- **Where:** 07:110 ("**Vorlain by the wine — …**"), 167 ("**Corval at the gate — …**") and 590 ("**MM — the factor.**"). The legend is at 01:343-346 ("Sidebar —", "⟨If History Breaks⟩", "MM Note").
- **Yardstick:** C-S25 [usually]; structure §12 (whatever device the legend declares, use it consistently).
- **Fix:** 590 → "**MM Note — the factor**". For the two Q&A boxes, either add a species to the legend ("**What [Name] Says**", which is the official "What [someone] Knows" species) or title them "**Sidebar — What Vorlain Says**" and "**Sidebar — What Corval Says**". The Q&A format itself is fine: §12 accepts it.

### CAST-18 [P3] A duplicated read-aloud and a duplicated quote (STYLING) [d20-portable]
- **Where:** The box at 07:477-480 is identical to 05:126-129. Vorlain's drunk line appears at 07:104-105 and again at 133-135.
- **Problem:** Two copies of a box drift apart. Official NPC appendices carry no read-aloud.
- **Fix:** 07:474-480 → "At the Unmasking it sets the cloak and cup down on the nearest table and takes its place by the Uninvited (chapter V has the read-aloud)." Cut the prose copy of Vorlain's line (see CAST-7).

### CAST-19 [P3] DCs sit off the module's own ladder (MECHANICS) [d20-portable]
- **Where:**
  - 07:273 (Callun, money: DC 25). The ladder at 01:163 says "Very Hard 25: Deceiving Raunu. Moving Vell. Very little else."
  - 07:164, 240 and 321 use DC 20 for "Hard", while 04:412 says "*Hard* DC 18".
- **Fix:** Callun → DC 20, which is "against somebody's expertise" (the ladder's Hard). Otherwise, add her to the ladder row. Change 04:412 to "*Hard* DC 18–20" to match 01. DC sanity at 4th level is otherwise fine: 10/13/15/18/20/25 against pregen bonuses of +2 to +8.

### CAST-20 [P3] The 07 intro miscounts the snakes (CONTENT) [d20-portable]
- **Where:** 07:9-11 ("The six factions who came as Raunu's enemies — the snakes"). 07:346, 01:263 and 09:377 all say the Thenya are **not** a snake.
- **Fix:** "Five factions came as Raunu's enemies (the snakes), and a sixth, the Thenya, came as his wife's kin; each has a threat line and fight cards in chapter IX…"

### CAST-21 [P3] The pregen intro's "can stand in a fight" claim doesn't match the sheets (CONTENT) [not portable]
- **Where:** 11:24 ("Dassa at 40 hit points and Pello at 31"). Serane and Ilesse also have 31. What separates Pello is AC.
- **Fix:** "**Dassa (AC 16, 40 hit points) and Pello (AC 16, 31)**".

### CAST-22 [P3] Feature wording nits against SRD 5.2.1 (MECHANICS) [not portable]
- 11:243, Arcane Recovery: "Once a day, on a short rest" → "Once per Long Rest, when you finish a Short Rest".
- 11:177-179, Fast Hands: this is its own set of Bonus Action options, not an extension of Cunning Action [verify 5.2.1]. Suggest "Bonus Action: a Dexterity (Sleight of Hand) check (a lock, a trap with thieves' tools, a pocket), the Utilize action, or the Magic action to use a magic item, a crystal charge included."
- 07:84-86: Veier's *For Them* leaves out the 60-foot limit that 03:129-131 prints. Add "while within 60 feet of her".

### CAST-23 [P3] The rumor table has no truth notes where the module itself knows the answer (CONTENT) [d20-portable]
- **Where:** 08:311-315. Rumor 6 (the bride is dead; 07 has her alive), rumor 8 (Vorlain never stopped ruling; 07:97-98 says he has no plot and gave the seat back), rumor 11 (the staff are still inside; 04:695-712 has Corval's ledger of eighty placements).
- **Yardstick:** C-V11 [always] (false beliefs carry a trailing truth parenthetical, for the MM).
- **Fix:** Only once the table is MM-facing (CAST-8), add "(Untrue. See chapter VII.)" and similar to 6, 8 and 11 **only**. Leave every rumor that touches *What the Module Never Says* (1-5, 9, 10, 12) unmarked, because that silence is canon.

### CAST-24 [P3] Cross-reference and emphasis typography (STYLING) [d20-portable]
- **Where:** Throughout 07 and 08: "(Chapter V)", "Chapter X under *If It Comes to It*", "(*Buying Time*, Chapter V)". About 18 italics used for emphasis in 07's DM prose (*completely*, *nothing*, *aimed*, *toward*…).
- **Yardstick:** C-S41 [always] ('(see chapter 5, "Down, Not Out")'); C-S39 [always] (italic is for spells and items).
- **Fix:** This is a house-wide decision, logged once. If adopted: '(see chapter X, "If It Comes to It")' and plain roman in place of emphasis italics. Roman chapter numerals can stay as house style.

### CAST-25 [P3] Handout placement and naming (STYLING) [d20-portable]
- **Where:** 08 puts the handouts in chapter VIII, ahead of the Snakes, the Bestiary and the Pregens. Headings read "Handout 1 — The Invitation".
- **Yardstick:** C-S9 [always] (handouts come last); C-S48; the CoS handouts appendix.
- **Fix:** Move Handouts 1-2 into a closing appendix after chapter XI, titled "Player Handout 1: The Invitation" and "Player Handout 2: Agenda Cards". The MM sheet stays in chapter VIII.

### CAST-26 [P3] The "one page" MM sheet is still longer than a page. Still open from AUDIT_oraga_5e_playability / M1 (much reduced) (STYLING) [d20-portable]
- **Where:** 08:9-118, about 1,600 words: two wide tables, seven rule bullets, the pillars, and two more tables.
- **Fix:** Retitle it "the Night on Two Pages" and break it after *The pillars* (08:92). Page 1 is Tables VIII–1 and VIII–2. Page 2 is the midnight rules, Key DCs and Costs.

### CAST-27 [P3] The palace diagram gives one key to three places (STYLING) [d20-portable]
- **Where:** 08:132-138. "B5 the river gate", "B5 the lower garden" and "B5 the garden terraces" each carry B5.
- **Yardstick:** C-S10 [always] (one code per area; sub-areas NA/Na).
- **Fix:** One box, "B5 The Gardens", with the gate, the lower garden and the terraces as plain labels inside it. Using B5a-c instead would mean editing 04 too.

### Still open from earlier documents (present in current text)
- 07:179, "There used to be sixty of you" against eighty in 04:696. Still open from LOG_oraga_5e_pass2 Open Q1 and AUDIT_oraga_5e_playability / m7.
- 07:155, the testament's witnesses. Still open from LOG_oraga_5e_pass2 Open Q2.
- 07:315-317, Essin's "two bodies". Still open from LOG_oraga_5e_pass2 Open Q3 and INVENTIONS #13.

---

## 3. What already meets the official standard (don't break these)

- **Stat pointers resolve.** All 22 block names in 07 exist in chapter X exactly as named. The noncombatants point to *If It Comes to It* (10:1795), which has a one-line fallback for "a guest". That is exactly C-S30.
- **Secrets are stated flatly to the MM, next to the surface.** Vorlain's "he has no plot tonight" and Corro's "Secret: none" are examples (C-V10).
- **Corval's Q&A box** gates deeper answers behind "if friendly / if pressed a second time" and flags his false belief ("He believes this while he says it"). That is C-V11 done right. The check inside it is in correct form ("DC 18 Wisdom (Insight)").
- **The Bought's negotiation surfaces** (wants, what shifts him, what deal he honours) are the official delegate shape, format C: what wins them over and what alienates them. The captain's "doesn't know who hired him" is a written knowledge limit, as the official standard requires.
- **The Attendant's read-aloud** has a trigger, is perception-only, and identifies nothing the players haven't seen (C-S19 to C-S21). It just shouldn't be printed twice (CAST-18).
- **Handout 2 (agenda cards):** it has a trigger ("deal one per player in the first five minutes") and carries only what the character knows. The spoiler in the chapter III catch ("She never comes down") is correctly left off card 4. The *Pays* lines are back (playability m9 fixed).
- **The rumor table's** 2d6 first column and deliberate bell curve are sound. Titled die-range tables meet C-S40.
- **Pregens:** legal at 4th level under SRD 5.2.1, and the arithmetic is verified by script:
  - Standard array plus background +2/+1 plus the ASI; HP at max for 1st level, then average + CON.
  - AC, Initiative (Alert), passive Perception, and every skill total (Expertise, Jack of All Trades, Thaumaturge).
  - Skill counts reconcile with class + background + Skillful + Skilled/Lore.
  - Slots 4/3; cantrips 3 bard / 4 wizard / 4+1 cleric, plus the gift; prepared 7 each; Andra's spellbook of 14.
  - Every subclass (Lore, Thief, Evoker, Champion, Life) is in both SRD 5.1 and 5.2.1. Every feat (Alert, Skilled, Savage Attacker, ASI) is an SRD 5.2.1 feat. The SRD attribution block is present.
  - Each pregen carries an adventure-specific tie (the agenda hook), which is the core of C-S50.
- **Mechanics consistency with the rest of the book:** the Snake Tracker values, Table VIII–6's Essin row (m5 fixed), the Crossing in Movement VI (M2 fixed), and the midnight one-liners all match 05 and 09 (pass-2 sweep).
- **Voice hygiene:** no "PCs", no designer "we", no rhetorical questions or exclamation marks in DM prose, and no future-tense trigger consequences. Sentence lengths are within the official band (07 mean 18.7, 08 16.4, 11 20.7).

---

## 4. NEEDS-RULING

- **N1. What does the Attendant say when asked something the module never answers?** *Background:* The Attendant must answer any direct question, literally and (per chapter X) truthfully. Players are taught this and rewarded for using it. But the book promises never to name the power in the east or say who the Uninvited were. *Question:* When a player asks "Who is your master?" or "What are the three?", which should happen? (a) It answers the literal words, which are never what was meant. (b) It was made, not told, so it doesn't know. (c) It answers with its missing master. (d) Something else you'd prefer. Also, may it admit it came through *with* the three? (CAST-1)
- **N2. What does Veier tell a character who reaches her?** *Background:* Your ruling R6 keeps the heir secret unless a player character discovers it. Agenda 4's carrier is the one character built to reach her, and the book gives her one spoken reply but no list of what she'll share. *Question:* May she confirm the pregnancy to someone she comes to trust, or must they see the nursery for themselves? (CAST-2)
- **N3. Flaws for the five pregens.** *Background:* 5e sheets usually list an ideal, a bond and a flaw. The source files give each pregen a first-person concept line, which can serve as the ideal, and the agenda serves as the bond. None of them has a flaw in canon. *Question:* Do you want to write a one-line flaw for each, or leave the sheets without one? (CAST-10)
- **N4. Is Ilesse's warding crystal her holy symbol?** *Background:* In 5e a cleric's spells and Channel Divinity use a Holy Symbol. The module deliberately never says what answers her. *Question:* Should the crystal simply *count* as her holy symbol (a rules label only), or should she carry a plain component pouch instead? (CAST-11)
- **N5. Pronunciations.** *Background:* Official modules usually give a pronunciation for invented names (C-S31 [usually]). There are none anywhere in the project, and inventing them would be canon. *Question:* Do you want a pronunciation line for the main names (Raunu, Veier Nolonaire, Vorlain, Corval, Anha, Kovaun, Rhaza Callun, Pellin Corro, Essar Draunel, Essin, Maiven, Vell, Tavva, Orthaen, Thenya, Phern, Rekuzan, Oraga, Elanna, Val'loh), and if so, how are they said?
- **N6. Alignment tags on the cast.** *Background:* Newer official books tag each NPC like "(LN female human **noble**)". Chapter X already gives alignments to the combatant blocks but none to Raunu, Veier, Corval, Anha, Sella, Vell or the Uninvited. *Question:* Leave the cast untagged (recommended; the book's apposition-plus-stat-block style is also official), or tag it, in which case you would need to give the missing alignments?
- **N7. Initials on the agenda cards.** *Background:* Cards 1-4 sign off "— R.C.", "— D.K.", "— E.D." and "— M.N.", as if they were written notes. The world's law is that only the Church writes (02:18-20). *Question:* Are the initials a table convenience (fine as is), or should the cards say how the ask was delivered ("in person", "by a go-between")? This is carried over unchanged from the Facets handouts.
- **N8. "MM" on the player-facing pregen sheets.** This is already being raised with you. Chapter XI's sheets say "the MM gives the answer without a check" five times, and a 5e player holding only the sheet won't know the term. Whatever you rule, one clause in 11's intro defining it would help.
- **N9. Still open from pass 2:** sixty or eighty servants (07:179), the testament's witnesses (07:155), and Essin's "two bodies" (07:315-317).

---

## 5. Status after fix pass (2026-10-03)

*Final review T9.3, against HEAD (`git diff pre-official-5e..HEAD`). Line numbers are current.
`tools/pregen_check.py`: 5 pregens checked, 0 issues.*

| ID | Status | Evidence |
|---|---|---|
| CAST-1 | void | Owner Q5 removed the habit. 07:607-610 keeps only "Asked whom it serves, it names no one"; 07:612-616 lists three habits (crystal and light, cup and cloak, music), matching 09 S14 and 08 Table VIII-1 (no Movement III sighting, per O3/Q22). |
| CAST-2 | fixed (Q7 and Q11 residue gated) | "What [Name] Knows" lists for Raunu 48-68, Veier 105-116, Anha 265-278, Kovaun 301-309, Sella 332-344, Callun 362-370, Corro 392-399, Draunel 418-425, Essin 444-452, Maiven 476-486, Tavva 674-688. Spot-checked nine bullets against their sources, all printed elsewhere: Anha's cellar stair (04:581-583), Callun's "three heads" (02:290), Essin's appointment (04:1236), Maiven's palace window (02:69), Raunu's *Speak with Dead* (02:246-249), Corro "worst near the three" (04:787), Kovaun's blessing (05:736), Tavva's pick-two (09:723), Sella's testament (04:718-720). "(untrue)" flags at 368 and 486. Veier's pregnancy is a TODO-Q7 at 116; Essin's bodies are a TODO-Q11 at 452. |
| CAST-3 | fixed | Default-DC sentence at 07:5-7. Sergeant: 07:727. |
| CAST-4 | fixed | 07:520-522 "DC 25 Charisma (Deception, Intimidation, or Persuasion) check"; 07:530-533 Insight with no gate; 08:116. |
| CAST-5 | fixed | All five winks are gone (83, 270, 342, 397, 515 rewritten). The kept "the module does not say / never explains him" lines are at 513 and 547. |
| CAST-6 | fixed | The "player" lines left (40, 203, 615) mean the real people. |
| CAST-7 | fixed | Em dashes are down from 129 to 45 (about 6 per 1,000 words). 144-146, 201-203, 524-525, 576-577 and 638-643 are rewritten as proposed. |
| CAST-8 | fixed | 08:236 "Rumors at the Ball *(DM table)*" now sits outside "Player Handouts". |
| CAST-9 | fixed | 08:267-270 has the trigger and recipient. Invitation text untouched. |
| CAST-10 | gated (Q16) | T8.12. Sheets still have Personality / Agenda hook, with no Ideal/Bond/Flaw labels. |
| CAST-11 | partly; rest gated (Q16) | Andra: 11:252 "a crystal as Arcane Focus", 11:263 Carrying. Ilesse: TODO-Q16 at 11:421. |
| CAST-12 | fixed | 11:45-47. |
| CAST-13 | fixed | 11 and 08 use 5.2.1 capitals. Charges are italic Title Case (11:110, 264, 429-430), matching 10 and Handout 3. |
| CAST-14 | fixed | 08:108-113: every row names its ability and skill. |
| CAST-15 | fixed | Appositions at 07:288, 349, 377, 407, 431, 459. Sergeant 729 and Captain 764 have pointers. (377 is redundant: see NEW-CAST-4.) |
| CAST-16 | fixed (optional polish done) | "Roleplaying [Name]" throughout. **Quote:** lines at 102, 329, 535, each an existing line. |
| CAST-17 | fixed | "What Vorlain Says" 151, "What Corval Says" 208, "DM Note — the factor" 758. |
| CAST-18 | fixed | The Attendant box is now a pointer (07:625-626). Vorlain's line is printed once (box, 173-176). |
| CAST-19 | fixed | Callun is DC 20 (07:359). 04 no longer says "Hard DC 18"; 01:251's ladder reads Hard 18-20. |
| CAST-20 | fixed | 07:9-11. |
| CAST-21 | fixed | 11:24. |
| CAST-22 | fixed | Arcane Recovery 11:244-245; Fast Hands 11:178-180 matches the 5.2.1 text; *For Them* range at 07:127-128. |
| CAST-23 | fixed | Truth notes on rumors 6, 8 and 11 only (08:250, 252, 255). Never-Says rumors are left bare. The rumor 11 pointer resolves (04:698). |
| CAST-24 | partly | Prose cross-references follow the style sheet. Left: "(Ch. IX)", "(Ch. I)" and "Ch. V read-aloud" in Table VIII-1 (08:15, 17, 26), and emphasis italics at 07:545 ("*the way the Uninvited move*"). |
| CAST-25 | partly (by design) | T2.5 grouped the handouts as a closing "Player Handouts" section of 08 (08:260), renamed "Player Handout N: ...", instead of moving them after XI (O8: no renumbering). |
| CAST-26 | fixed | 08:9-58: "the Night on Two Pages", split at *The pillars*. |
| CAST-27 | fixed | 08:141-149: one B5 box. |
| Still-open: sixty/eighty | gated (Q20) | 07:220 still says "sixty"; 04:699 and 04:716 say eighty. |
| Still-open: testament witnesses | gated (Q20) | 04:718-720 and 07:196 as before, now also in Sella's new list (07:339-341). See NEW-CAST-2. |
| Still-open: Essin's two bodies | gated (Q11) | 07:435 unchanged; TODO-Q11 at 452. |
| N1 | void | Q5. |
| N2 | gated (Q7) | TODO-Q7 at 07:116. |
| N3, N4 | gated (Q16) | T8.12. |
| N5 / N6 / N7 | gated (Q17 / Q18 / Q19) | No pronunciations and no cast alignment tags. Cards still sign "— R.C." etc. (08:296-313). |
| N8 | fixed (Q1) | The sheets say "the DM". |
| N9 | gated (Q11, Q20) | As above. |

**Counts:** fixed 22 (CAST-2 to -9, -12 to -23, -26, -27), partly 3 (CAST-11, -24, -25), gated 1 (CAST-10), void 1 (CAST-1), skipped 0, regressed 0.

---

## 6. New issues found in final review

*Pregen rules were rechecked against SRD 5.2.1 by hand: ability scores, HP, AC, saves, skill counts, cantrip and prepared counts, Bardic Inspiration, Cutting Words, Nick, Steady Aim, Fast Hands, Second-Story Work, Arcane Recovery, Scholar, Evocation Savant, Potent Cantrip, Second Wind, Tactical Mind, Remarkable Athlete, Thaumaturge, Divine Spark, Preserve Life and Spiritual Weapon (Concentration). No P1 rules errors. Handout 3 (Crystal Charges) matches 10:1960-1990 and keeps the Uninvited's smothering hidden ("the DM will tell you"). Handouts 1-2 carry no DM notes. The 08 contract line now matches 09:864-866 and 05:989-998.*

### NEW-CAST-1 [P2] The player-facing pregen sheets send players to the DM-only chapter IX and use the DM's word "snake" (pre-existing, missed by the audit)
- **Where:** 11:119 "she is working a snake's errand (see chapter IX), from inside"; 11:190-191 "the Circle is a snake (see chapter IX)"; 11:350 "when a snake comes through it"; 11:271-272 "a tell: the Uninvited's, or a snake's". Also on the sheet: 11:414 "*Turn Undead:* nothing at this ball is undead" (a fact about the gray masks that 10:134 keeps in a DM table), and 11:437-439 "the one that puts a character beside Veier when the lights die".
- **Problem:** Chapter XI is handed out ("Hand them out as they are", 11:6). Chapter IX is the DM's faction chapter, and "snake" and "the Uninvited" are DM vocabulary. "When the lights die" tells a player in advance that midnight goes dark.
- **Fix:** 119 → "Either way she is working a faction's errand, from inside."; 190-191 → "…a Phern's standing to use it."; 350 → "when trouble comes through it"; 271-272 → "the guest likeliest to catch a tell."; 414 → "*Turn Undead:* as the SRD." (or cut the sentence); 438-439 → "…and the one that puts a character beside Veier." Leave the chapter-IX pointers in the DM-facing table and intro.

### NEW-CAST-2 [P3] Sella's new knowledge list repeats the gated testament-witness fact
- **Where:** 07:339-341 "Three days before the ball she stood witness in this chapel, with Corval, as the law requires…"
- **Problem:** The fact is not invented: 04:718-720 prints it. But it is the still-open Q20 item (the cut Facets vignette had a notary and two paid witnesses). It now stands in three places, and T8.16's site list (07, 04) won't catch the new bullet.
- **Fix:** Add `<!-- TODO-Q20 -->` after the bullet, as with Q7 and Q11, and add 07:339-341 to T8.16.

### NEW-CAST-3 [P3] Veier's "uncle" sits next to a list that makes her a cousin
- **Where:** 07:102-103 and 109 ("Her answer for Maiven is her quote": "Tell my uncle his message…"); 07:481 "Veier is the Thenyan chief's cousin"; 02:64 likewise. 04:1275-1277 repeats the quote.
- **Problem:** The quote is Facets canon (adventures/oraga_night/07:63). The new lists now set it beside "the chief's cousin" and Maiven, another cousin. A DM reads it as a slip: whose message is it?
- **Fix:** Don't edit the quote. Raise it with the owner as a one-line question: is "uncle" a third relative, or should it be "cousin"? Until then, change 07:109 to "Her answer for the delegation is her quote, above."

### NEW-CAST-4 [P3] Redundancy left by the CAST-15 fixes
- **Where:** 07:376-377 header "Master Pellin Corro — the Phern Magnate", then apposition "*The Phern magnate.*". 07:764-767: the Captain's "If it comes to steel" repeats 755-756 ("A bought-out captain does not resume the fight tonight for any inducement") and points to S3 twice.
- **Fix:** 377 → "*A Phern magnate, and exactly what he appears.*" (from 381), or drop it. 764-767 → "**If it comes to steel:** stat block **Bought Captain** (see chapter X); card S3. The captain's and sergeant's negotiation surfaces above are the two outs the card leans on."

### NEW-CAST-5 [P3] Pello's Weapon Mastery line misreads after the dash was removed (regression)
- **Where:** 11:173-174 "Dagger (Nick), Shortsword (Vex), for the first blade he picks up after midnight; he carries none."
- **Problem:** With the em dash now a comma, it reads as if both masteries wait on a found blade, though he carries two daggers.
- **Fix:** "Dagger (Nick); Shortsword (Vex), for the first shortsword he picks up after midnight (he carries none)."

### NEW-CAST-6 [P3] 07's default social DC is muddled with 04's "behind a mask" rule
- **Where:** 07:5-6 "the DC to move that guest is 13 behind a mask"; 04:430-431 "Behind a mask, a character approaching someone far above their station… DC 10, where it would otherwise be 13"; 08:109.
- **Problem:** In 04, the mask is what lowers 13 to 10 across station. In 07, 13 is the masked default. Both can be read as true, but a DM comparing them will stall.
- **Fix:** 07:5-7 → "Where an entry gives no DC, moving that guest is DC 13 (DC 10 for a character approaching far above their station behind a mask; see chapter IV, "Social checks at the ball"); the entries below note only the exceptions."

### NEW-CAST-7 [P3] Small wording and consistency nits
- 07:153-155 (box intro): '"If friendly" here means "drunk"', but no line in the box is labeled "if friendly"; they say "drunk". Fix: 'The "drunk" lines take real work, and Essin will try to stop it.'
- 07:359-360: Callun's money DC is plain and her "human" DC is bold. Bolding varies across 07 (bold at 45, 205, 298, 441, 521; plain at 144, 242, 442, 531, 727). Pick one; official books don't bold DCs.
- 08:3-5: "the Snake Tracker, where everyone stands and the rumor table" reads as a relative clause. Fix: "the Snake Tracker, Where Everyone Stands, and the rumor table".
- 11:168 Sneak Attack leaves out 5.2.1's "and you don't have Disadvantage" (pre-existing), and Pello's Thieves' Cant extra language isn't on the sheet. Fix: "…with Advantage, or with an ally within 5 ft. of the target and no Disadvantage."

### 6a. Resolved (Phase 9 final-review fixes, 2026-10-03)

| ID | Resolved | Note |
|---|---|---|
| NEW-CAST-1 | fixed | 11: "a faction's errand"; the Circle-is-a-snake clause cut; "the guest likeliest to catch a tell."; "when trouble comes through it"; *Turn Undead* now gives the SRD effect instead of the gray-mask spoiler; "puts a character beside Veier." (no "when the lights die"). The DM-facing intro's chapter V pointer stays. Handouts 1–3 checked: their only DM text is the italic trigger lines, and Handout 3 points only at chapter III. |
| NEW-CAST-2 | gated (Q20) | `<!-- TODO-Q20 -->` under Sella's witness bullet; the bullet added to T8.16's row in TASKS. |
| NEW-CAST-3 | gated (Q24, new) | Quote untouched. 07 "Her answer for the delegation is her quote, above." `<!-- TODO-Q24 -->` beside it. Q24 added to AUDIT §5a with background. |
| NEW-CAST-4 | fixed | Corro's apposition dropped (it echoed the header and line 383). The Captain's steel line cut to the stat block, card S3 and the two outs. |
| NEW-CAST-5 | fixed | "Dagger (Nick); Shortsword (Vex), for the first shortsword he picks up after midnight (he carries none)." |
| NEW-CAST-6 | fixed | 07 dek: "the DC to move that guest is 13, or 10 for a character approaching far above their station behind a mask (see chapter IV, "Social checks at the ball")". |
| NEW-CAST-7 | fixed | Vorlain box intro "The "drunk" lines take real work…"; all six bold DCs in 07 unbolded; 08 dek "the Snake Tracker, Where Everyone Stands, and the rumor table"; Sneak Attack adds "and no Disadvantage"; Thieves' Cant adds "one more language of his choice" (SRD 5.2.1). pregen_check 0. |
| CAST-24 leftovers | fixed | Table VIII–1 "(chapter IX)", "(chapter I)", "Chapter V read-aloud"; 07 "the way the Uninvited move" roman. |
