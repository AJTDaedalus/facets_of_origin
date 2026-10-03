# Official-Style Audit — FRONT slice and whole-module architecture

*2026-09-30. Auditor: FRONT. Scope: `conversions/dnd5e/oraga_night/` `README.md`,
`01_Overture.md`, `02_The_World_and_the_Night.md`, `03_Masks_and_Agendas.md`,
`06_Aftermath.md`, plus the heading outline of every chapter (architecture). This is a
read-only audit: no module file was edited. Yardsticks:
`docs/RESEARCH_5e_module_conventions_structure.md` (C-S#) and
`docs/RESEARCH_5e_module_conventions_voice.md` (C-V#, S#). Frequency tags: [A] always,
[U] usually, [S] sometimes. Party level is **4th, ending at 5th** (FIXPLAN §6, owner
ruling). DC sanity was judged against that level, not the 3rd level in the shared brief.*

---

## 1. Summary

| Dimension | Verdict |
|---|---|
| **PROSE** | Good. Sentence and paragraph rhythm sit inside official norms (01: mean 15.4 words per sentence, 10% over 30; 02: 17.7; 03: 16.0; 06: 16.3). There are no "PCs", no designer "we", no rhetorical questions and no exclamation marks. Three voice habits are un-official: conversion-artefact talk ("the source", "the original", "this edition"), a signed designer's note, and a handful of inherited not-X-but-Y aphorisms. |
| **MECHANICS** | Sound for 4th level. The DC ladder (10 / 13–15 / 18–20 / 25) is sane. XP to 5th level (2,700 → 6,500) adds up. The runtime table sums to 4 h 50 min as claimed. Heroic Inspiration is stated correctly for both 5.2.1 and 2014, and the gift feats are legal SRD 5.2.1 builds. Defects: a count error in 03, mask checks missing their ability, a mixed capitalization scheme across the module, and a 2014-compatibility overclaim. |
| **STYLING** | Mixed. The format legend exists but is incomplete. It sits too late (01 L320), and it declares "italic blocks are read-aloud" while the book uses italic for many MM-voice paragraphs. Several box species are undeclared, raw Markdown and code spans show in the legend, and cross-references use a consistent house form (italic section name + Roman chapter), not 5e's lowercase "(see chapter 5)". |
| **CONTENT / ARCHITECTURE** | The front matter covers every [A] block (party and level, required rules, overview, hooks, advancement, rewards, tone, troubleshooting, safety), but in the wrong order. The Adventure Background sits after the running material, in Chapter II. The Overview hides what happens. Player-facing chapters send players into MM-only material (Chapter III's agendas; Chapter X for crystal charges). Handouts sit mid-book. The snakes' ground rules are printed three times with different counts. |

**Top 5**
1. **FRONT-1 (P1).** Chapter III is the player-facing character chapter, yet it carries the agendas' MM-only *At midnight* lines, including the Agenda 6 reveal of Master Vell.
2. **FRONT-2 (P1).** Crystal-charge rules, which players need, exist only in Chapter X (the MM-only bestiary). Chapters III and XI send players there.
3. **FRONT-3 (P2).** There is no Adventure Background in the introduction. The villain's plan and the default outcome are at the end of Chapter II.
4. **FRONT-5 (P2).** The format legend is incomplete and late, and its read-aloud device ("italic blocks") collides with italic MM prose across the book.
5. **FRONT-7 (P2).** About 25 conversion-artefact references ("the source says", "the original", "new in this edition") are left in MM prose. The DC ladder's first column is headed "The source says".

---

## 2. Findings

### FRONT-1 [P1] Player-facing Chapter III carries MM-only secrets (CONTENT) [d20-portable]
- **Where:** 03 L193–360 (*The Agenda System*, *The Eight Agendas*). The worst lines are 03 L319–324 (Agenda 6: "the stranger was Master Vell, securing Veier's escape route"), L236–238 (Agenda 1: the Tithe explained, plus "The module invents it here"), L286–287 (Agenda 4: "Chapter V leans on it"), and every **At midnight** line. The chapter addresses players ("Build 4th-level characters", "You choose what it does", L5, L63). 01 L29–30 routes players to it ("Chapter III (only if players build their own characters …)"), and 11 L4–5 says "as Chapter III requires".
- **Yardstick:** C-S9 [A] and structure §1.4. Official character options are player-safe appendices (CoS app. A, HotDQ app. A), and secrets never sit beside them. C-V1 [A]: "you" in MM text means the MM. Here the addressee switches from player to MM inside one chapter.
- **Problem:** A player who builds a character from Chapter III reads the module's central escape route and the midnight turns. 02 marks its secret half "MM ONLY" (L111). Chapter III has no such line.
- **Fix:** Do the minimum first. Put a banner heading before L193: `## The Agenda System — MM Only`, with the italic note *Players see only the cards in Chapter VIII (Handout 2). Everything below, and every* At midnight *line especially, is yours.* In 01 L29–30, change "Chapter III (only if players build their own characters; …)" to "Chapter III's player options, up to *The Agenda System* (hand these to players who build their own characters; the agendas stay with you)". Better, if the owner accepts a small move: split III into *Player Options* (L1–191 plus *The Ready-Made Guests*) and move *The Agenda System* and *The Eight Agendas* into 01 or into the MM half of 08.

### FRONT-2 [P1] Crystal-charge rules live only in the MM-only bestiary (CONTENT/STYLING)
- **Where:** 03 L102–104 and L170–172 ("Their rules, their prices … are in **Items of the Night**, Chapter X"). 11 L38–39 tells pregen players to read *Items of the Night* in Chapter X. 01 L72.
- **Yardstick:** C-S9 [A]. Items are an appendix, or item cards are handouts (AL: DDAL04-12 p.24). Structure §10.1 lists magic-item cards as a handout type.
- **Problem:** Players holding charges must open Chapter X. That chapter opens with the Uninvited's *Leashed* design, the Attendant's habits and the whole "table tries" list, so it spoils the night.
- **Fix:** Add a player-safe card for the six common charges, either as **Handout 4 — Crystal Charges** in 08 or as a short section at the end of 03's *Crystal Charges*. Copy the rules text from X *Crystal Charges* as written. This is relocation, not new canon. Leave out the line on what a charge does near "something that eats magic" (L171–172), or reduce it to "some things at this ball smother a charge; the MM will tell you". Point 03 and 11 at the handout instead of at Chapter X.

### FRONT-3 [P2] No Adventure Background in the introduction; the background comes after the running rules (CONTENT) [d20-portable]
- **Where:** 01 (whole chapter). The background is spread over 02 L49–74 (public) and L111–228 (the MM truth), after 01's hooks, checks, rewards and legend.
- **Yardstick:** C-S3 [A]: Adventure Background → Overview → Hooks → Running (LMoP p.3–4; CoS p.6–7; the AL battery). A reader of LMoP, CoS or DDAL04-04 learns the villain's plan on page one.
- **Problem:** An MM who reads 01 first, as the prep box orders, learns how to run the night before knowing what happens in it. The 90-minute box patches this by sending the MM to Chapter II as step 2.
- **Fix:** Add `## Adventure Background` in 01 directly after *What This Adventure Is*. It should be MM-only, about 150 words, and built only from Chapter II facts. Original draft:
  > Raunu Boranis, chief of the Orthaen, vanished in 3160 and walked back into his hall a year later without a word about where he had been. He married Veier Nolonaire, cousin of the Thenyan chief, to seal a pact, then shut his palace for two years. Veier is now close to giving birth. Raunu has thrown an Oraga masquerade to announce the child at the midnight Unmasking, and he has invited every enemy he has.
  >
  > He never gets to say it. Three servants of a power sealed beyond the eastern mists, the Uninvited, come masked as spirits to kill Raunu and Veier and carry off the child. A second hidden power has sent Master Vell to make sure the child is not taken. By default Raunu dies on his ballroom floor after spending his last ward on his wife's escape, Veier leaves through the river gate on Vell's arm, and no one is ever charged (Chapter II, *The Truth of the Night*).

  Then shorten prep-box step 2 to "Chapter II, *What the Module Never Says*" (the rest is now in 01).

### FRONT-4 [P2] The Overview hides what happens (CONTENT/PROSE) [d20-portable]
- **Where:** 01 L77–104, *The Night in Seven Movements* and Table I–1's "By the end…" column: "The host's absence has stopped being funny", "The room has been told something it does not know what to do with", "Anyone who assembled the pattern has one chance to act on it".
- **Yardstick:** C-S3 [A] (Overview: one entry per part saying what the characters do and where it leads) and C-V10 [A] (secrets stated flatly to the DM, never coy).
- **Problem:** The only overview in the book is a pacing table written as teasers. The flat facts exist, but only on the 08 sheet (Table VIII–1, *Scheduled*).
- **Fix:** Keep Table I–1 as the pacing table. Before it, add an **Overview** list of seven one-liners taken from 08 Table VIII–1 and 02:
  **I.** Corval receives every guest by name. Nobody is disarmed, the hosts don't appear, and the honor guard faces inward.
  **II.** Vorlain holds court. The factions circulate, and the host still has not come down.
  **III.** Raunu is glimpsed on the high gallery, and Corval brings guests to him in the Audience Hall (B4), at least one player character among them.
  **IV.** Raunu toasts at the high table, promises something to say at the Unmasking, is served on two plates, and leaves.
  **V.** The Dead Dance and the quarter-bells. Vell goes down to the river gate, and the guard on the east wing is doubled.
  **VI.** The lights die mid-sentence. The Uninvited kill Raunu, and Veier escapes through the gardens on Vell's arm (the Crossing).
  **VII.** Fire and rescue. The Bought hold the front gate (S3) until the last bell.

### FRONT-5 [P2] The format legend is incomplete, late, and contradicted by the book's own italics (STYLING)
- **Where:** 01 L320–352 (*How This Module Is Written*). It comes after the hooks, the checks, the rewards and the snakes.
- **Yardstick:** C-S2 [A] (bold = stat block and where it lives; italic = spells and items; boxed text = read-aloud, with its trigger), C-S19 [A], C-S25 [U].
- **Problems:**
  1. *Placement.* The legend should sit in the running block near the top, not at L320.
  2. *Missing entries.* It doesn't cover bold stat-block names (every block is in Chapter X), italic spells and magic items, bold run-in room codes, the house cross-reference form (italic section name + Roman chapter), or the capitalization scheme (see FRONT-10).
  3. *Read-aloud device.* The legend says "***Italic blocks*** are read-aloud" (L338). In practice read-aloud is an indented italic block after a plain trigger line (04 L138–145). Meanwhile, many italic paragraphs are MM prose: 01 L417–419, 02 L3–5, L9–12, L113, 06 L3–5, 04 L126–130, and every chapter lead in 04–11. A reader who takes the legend literally will read those aloud.
  4. *Box species.* The legend declares three box kinds (Sidebar, ⟨If History Breaks⟩, MM Note). The book also uses **Troubleshooting —** (5), **Designer's note —** (1), the prep box, the Movement run boxes ("About 25 minutes…"), *Reading this chapter at a 5e table*, *The Snakes This Movement* (5), and the fight-card **Wants / Tells / Breaks / Nastier** lines.
  5. *Clocks.* "Clocks are four-segment" (L335) is wrong for S3's six-segment last-bell clock and for S2's three-segment scaling line (09 L690, L747). The same sentence is at 09 L93.
  6. *Raw syntax.* L322 prints "`**B1. The Room Name.**`" and L326 "`S1`–`S5`" as code, and L166 prints `DC 15 Wisdom (Insight)` as code. In a rendered book these show as asterisks and typewriter font.
- **Fix:** Move the section to just after *What You Need* and retitle it `## Reading This Book`. Replace the italic entry with: "**Read-aloud text** is an indented block in italics, always introduced by a plain line such as *Read to open the session:*. Read it or paraphrase it. Italic paragraphs that aren't indented are notes to you." Add: "A creature name in **bold** has a stat block in Chapter X. *Italic* lowercase marks spells and magic items. Keyed rooms are **B0–B13**. A section named in *italics* with a chapter number is a cross-reference." Rewrite the clock entry as "Clocks usually have four segments; each card says how many and what advances them." Add one line naming the box kinds above. Drop the code spans and write **B1. The Room Name.**, S1–S5, and "a DC 15 Wisdom (Insight) check".

### FRONT-6 [P2] Signed designer's note (PROSE/STYLING) [d20-portable] — see NEEDS-RULING R2
- **Where:** 01 L300–318, "> **Designer's note — what the fights are for** … — *the designers*".
- **Yardstick:** Structure §4 and §12. No 5e module has a signed designer-note box, and "we" appears only in forewords. The house 3.5 guide recommends such boxes, so this is a house-versus-5e conflict.
- **Problem:** It reads as a 3.5 book, and it closes on a wink ("and that is the trick") and an aphorism ("That is not a difficulty setting; it is the module's spine").
- **Fix:** Retitle it as an MM Note and drop the signature. A light-touch rewrite:
  > **MM Note — what the fights are for**
  >
  > The Uninvited cannot be beaten, by design. Cleverness buys Delay, Delay buys hallways and lives, and Fractures change outcomes. The fights give a table's fighting energy somewhere it works. The feud is about dignity, the corridor is a job, and the snakes are the host's enemies acting when the lights go out. The Attendant is the thing in the way. The Bought are the one foe at the gate who can be beaten or bought, and they come in Movement VII because that is when a table most needs a problem a sword can answer.
  >
  > If your table only wants the ball, cut every fight but the gate and let the gate be talked open. If it only wants the fights, run them; the ball still happens around them.

### FRONT-7 [P2] Conversion-artefact references in MM prose (PROSE) [d20-portable]
- **Where (slice):** 01 L57 ("this edition has real fights"), L159 (the DC ladder's first column is headed **"The source says"**), L166–167 ("Where the source said a 'knack applies', this edition means…"), L180 ("replaces the Sparks of the original edition"), L228 ("the thing the fifth edition adds … a fact the original already states"), L326 ("the original five (S1–S5)"), L408 ("tools the original never had to answer"), L489 ("more steel … than the original had"), 02 L10, 03 L83. **Elsewhere (for the other slices):** 04 L17, L393; 05 L61, L1139, L1146 ("*(New in this edition.)*"); 07 L303; 09 L129–132, L238–239, L330; 10 L26.
- **Yardstick:** C-V13 [A] (no meta-commentary) and C-V14. Official modules never refer to an earlier edition in body text. Conversion notes belong in the front matter's credits or a single sidebar.
- **Problem:** A 5e MM who has never seen the Facets book is told what "the source said". The DC ladder's header in particular is meaningless to that reader.
- **Fix:** Keep README L37 (a proper front-matter statement). Rewrite the rest to state the rule and drop the history. Examples:
  - L159 header "The source says" → "Tier".
  - L166–167: "Where a check depends on a character's training, proficiency in the fitting skill or tool applies; a gifted character's gift (Chapter III) gives advantage when the check is about what the gift does."
  - L180: "**Heroic Inspiration** works as the SRD says: …"
  - L228: "It starts from one fact: **Raunu Boranis has invited every enemy he has into his own house.**"
  - L326: "**Fight cards** live in Chapter IX, S1–S14, one card each."
  - L408: "A party arrives with spells that pry — *detect thoughts*, …"
  - L489: "The snakes put steel in the dark. The same camera rule applies to them."
  - Move 03 L83 (the old-domains guide) into a `> **Sidebar — for players who know the Facets edition**` box. That is a legitimate setting aside.
  - 05's "*(New in this edition.)*" tags: delete them.

### FRONT-8 [P2] Agenda count wrong: "Four of the eight agendas" have snake patrons (CONTENT)
- **Where:** 03 L217.
- **Yardstick:** C-S29 [A] consistency, and the cross-chapter facts.
- **Problem:** Only three patrons are snakes: Agenda 1 (Circle), Agenda 2 (Church) and Agenda 3 (Draunel). Agenda 4's patron is explicitly "not a snake" (L290), and Agendas 5–8 are personal or unknown. An MM who counts four will look for a line that doesn't exist.
- **Fix:** "Three of the eight agendas have a patron who is also one of the night's snakes, and a fourth, the Thenya's, has a patron who can become a fight. That is not a trap …". While here, the second half of L218 ("That is not a trap for the player; it is a vantage point") is a not-X-but-Y. Make it "It gives the player a vantage point."

### FRONT-9 [P2] The snakes' ground rules are printed three times with different counts (CONTENT/ARCHITECTURE)
- **Where:** 01 L241–261 ("Four rules hold for everything with a weapon tonight": visible and optional; the storm vs the snakes; the Attendant can be beaten; nobody is the Uninvited's ally). 09 L41–56 ("Three rules keep them honest (the same three Chapter IV runs them by)": nobody draws first; visible and optional; nobody here is the Uninvited). 04 L452–465 (the Chapter IV version, woven into *How to run the snakes*). 08's Snake Tracker and 05 *Knives in the Dark* restate parts again.
- **Yardstick:** C-V14 [A] (point to a rule, don't restate it). Still open from LOG_oraga_5e_pass2 §5 (*Cuts I'd recommend, not made*: "09 *The Six Lines* … 04 *The Snakes in the Pen* … describe each line three times").
- **Problem:** Two lists with the same framing but different contents and counts ("four rules" in 01, "the same three" in 09). The MM can't tell which list is binding.
- **Fix:** Make 09's three rules the only rule list. In 01, keep the framing paragraph (L228–239), then write "Chapter IX runs them by three rules, and one more thing holds tonight:", and keep only the Attendant bullet (L248–259), which is unique to 01. Drop 01's other three bullets. Then carry out pass 2's 04 cut, or reduce 04 L452–465 to its pointer plus "Nobody draws first" and "The Thenya are not snakes".

### FRONT-10 [P2] Edition capitalization is mixed across the module (MECHANICS/STYLING)
- **Where (counts):** Lowercase "hit points" in 01 (1), 03 (1), 04 (2), 05 (11) and 11 (4), against capitalized "Hit Points" in 09 (13), 10 (24) and 11 (5). "long rest" is lowercase everywhere (01 L185, 03 L131, 11). "Prone" and "Unconscious" are capitalized in 09 and 10 but lowercase in 04 and 05. "initiative" and "Initiative" are both used in 01 (L460, L462) and 11. Advantage is mostly lowercase, capitalized twice (04, 11). Spells are italic lowercase throughout (*detect thoughts*), while 5.2.1 uses Title Case.
- **Yardstick:** C-V26 [A] and C-V19. Pick one scheme (2014 lowercase or 5.2.1 capitalized) and use it everywhere.
- **Problem:** The front matter says the book is written against 5.2.1 but prints 2014 casing. The bestiary does the reverse.
- **Fix:** Owner or integrator picks the scheme. The recommendation is 2014 lowercase for conditions, rests, hit points and advantage, italic lowercase for spells and items, and capitalized only for the 5.2.1 terms 2014 lacks (Bloodied, Heroic Inspiration). This keeps the prose readable at both tables. State it in the legend (FRONT-5), then sweep 09, 10 and 11. In this slice, change only 01 L460 and L462 to one form.

### FRONT-11 [P2] Chapter order and grouping don't read like an official book (ARCHITECTURE) [d20-portable]
- **Where:** README L43–60 and the chapter sequence: I Overture, II World, III Options + Agendas, IV Ball, V Night, VI After Dawn, VII Cast, VIII MM Sheet + Handouts, IX Snakes (factions + all encounters), X Bestiary + Items, XI Pregens.
- **Yardstick:** C-S9 [A] (appendices hold stat blocks and items; handouts come last) and C-S3 [A]. Comparisons:
  - LMoP: Intro → Parts 1–4 → App. A items → App. B monsters.
  - CoS: Intro → chapters → App. A options … App. F handouts.
  - DDAL04-04: intro battery → parts → monster appendix → map → handouts.
  - Death House: background, hooks and advancement on one page, then keyed areas.
- **Problems:**
  - Handouts (VIII) are mid-book, and the MM's own sheet is filed as a "handout".
  - The encounter chapter (IX) comes after the handouts.
  - Items live inside the bestiary (see FRONT-2).
  - Player options (III) sit between the background and the adventure proper.

  Renumbering would touch about 420 "Chapter N" references across the module and `flow.json`: V has 96, IX 81 and VII 56.
- **Fix:** Don't renumber (see NEEDS-RULING R5 if the owner wants a full reorder). Group the README contents table under three subheads: **Before the Night** (I–III), **The Night** (IV–VI), and **Reference: the book's appendices** (VII–XI, each with "open this when…"). Say in the README that VII–XI are the appendices. Retitle 08's H1 "VIII. The MM Sheet, the Palace and the Handouts" so the MM sheet isn't filed as a handout.

### FRONT-12 [P3] Invented proper nouns with no gloss or pronunciation (CONTENT) [d20-portable]
- **Where:**
  - README L6 "3164 **PG**" (the era is never expanded).
  - 06 L26 "likely **Mazaaian**" (never introduced in the module).
  - 02 L25 and 06 L88 "the **Blackwatch**" (named, never explained).
  - No pronunciation anywhere for Oraga, Raunu, Boranis, Veier Nolonaire, Rekuzan, Val'loh, Orthaen, Thenya and Phern.
- **Yardstick:** C-S31 [U] (pronunciation at first mention or in an NPC summary); structure §5.5.
- **Fix:**
  - README: "the year 3164" (drop PG), unless the owner wants the era named (R3).
  - Glosses from existing canon (settings/valloh/V3 L11, L13; V0 L45), not new facts: 02 L25 "The Blackwatch, who keep the vigil over the eastern mists, are frightened …". 06 L26 "likely Mazaaian (from Mazaa, the tribes' enemy in the western mountains)". The owner should confirm these paraphrases.
  - Pronunciations: NEEDS-RULING R3.

### FRONT-13 [P3] Blank discretion on the Church's favor (MECHANICS) — NEEDS-RULING R4
- **Where:** 03 L256–258: "as large as the MM decides 'frightening' means at your table".
- **Yardstick:** C-V9 [A] and S24 (discretion needs a default).
- **Fix:** Give a default and a dial, for example: "By default, one favor the Prelate can grant without scandal; at your table it can be larger." Any concrete favor (a pardon, an audience) would be new canon, so the owner should choose.

### FRONT-14 [P3] Mask checks are missing their ability or skill, and the "usual" DC is stale (MECHANICS)
- **Where:** 03 L181–185.
- **Yardstick:** C-V15 [A] ("DC N Ability (Skill) check"; never a bare DC or a DC range) and S5.
- **Problem:**
  - "DC 20" and "DC 10 instead of the usual 13–15" name no ability.
  - "the usual 13–15" contradicts 01's ladder, which makes a masked Standard check DC 13.
  - Recognizing a known person by voice and build is a perception task, so Insight alone is a narrow fit.
- **Fix:**
  - "**Identifying a masked guest you know:** a DC 15 Wisdom (Insight or Perception) check."
  - "**Identifying one you have only heard described:** a DC 20 Wisdom (Insight or Perception) check."
  - "**Approaching someone far above your station, behind a mask:** a DC 10 Charisma check with the fitting skill, not the usual DC 13, because the custom protects the conversation."

### FRONT-15 [P3] 06 repeats 05's epilogue, and one trail check uses the wrong skill (CONTENT/MECHANICS)
- **Where:**
  - 06 L47–55 (*Ending the Session*: the "carry out" question and "Call 5th level") repeats 05 L1022–1028 word for word in substance.
  - 06 L74: "DC 15 Wisdom (Insight) to find the one who will talk".
- **Yardstick:** C-V14 (don't restate) and C-V16 (the result verb fits the skill).
- **Fix:**
  - Cut 06 steps 2–3 to "2. If you ran the epilogue in Chapter V, you have already asked the question and called 5th level. If you skipped it, do both now." Keep the paragraph on what 5th level means (L51–55) as the reason not to skip it.
  - L74: "the carter (DC 15 Charisma (Persuasion) or Intelligence (Investigation) to find the one who will talk)". The failure line at L75–76 is exemplary; keep it.

### FRONT-16 [P3] Party range and the scaling rules aren't stated once, up front (MECHANICS)
- **Where:** README L7–10, 01 L39–42.
- **Yardstick:** C-S1 [A] (range and optimum), C-S6 [U], and C-V24 (AL "not cumulative").
- **Problem:**
  - The range is only implied by the scaling lines.
  - Nothing says whether "five characters" and "5th level" lines combine (five characters at 5th), or what to do with two or six players.
  - README L10 lacks "level." and a period ("The night ends at 5th").
- **Fix:**
  - 01 L39: "Oraga Night is designed for three to five characters of 3rd to 5th level, and built for four characters of 4th level."
  - Add one sentence stating whether the lines stack. SNAKES owns the answer; if they stack, say so; if not, "use the line nearest your table; the lines are not cumulative".
  - README L10: "The night ends at 5th level."

### FRONT-17 [P3] MM used before it is defined (STYLING) — NEEDS-RULING R1
- **Where:** README L48, L55 and L64–69 ("MM sheet", "MM Note") come before the only definition at 01 L51 ("the Mirror Master (MM)").
- **Fix:** README L64: "**Ninety minutes of prep.** You, the Mirror Master (MM), run the night from …".

### FRONT-18 [P3] "Runs unchanged at a 2014 table" overclaims (MECHANICS)
- **Where:** 01 L65–67, against 11 L44–45 (pregens must have their class features rebuilt) and 03 L52–53 (the 2014 gift rule, "in place of whatever else the MM allows a human", is vague).
- **Fix:**
  - 01 L66: "and runs at a 2014 table with the notes marked *At a 2014 table*; only the pregenerated characters need rebuilding."
  - 03 L52–53: "*(At a 2014 table, a gifted human takes the gift as a bonus feat at 1st level.)*" This is a house rule, so list it in README *Changes from the SRD*.

### FRONT-19 [P3] The rest economy isn't stated in the front matter (MECHANICS)
- **Where:** 01 L184–186 says no long rest. The only short rest (the chapel, B6) appears only at 04 L275.
- **Yardstick:** C-S15 [U] (a clocked night states what a rest costs).
- **Fix:** Append to 01 L186: "The chapel (B6) is the one place to take a short rest, and the only one the ball offers."

### FRONT-20 [P3] README mixes product front matter with repository and process text (STYLING)
- **Where:** README L59 (`INVENTIONS_5e.md`, "for the setting author's review") and L60 (`flow/` build instructions). *Changes from the SRD* (L88–95) omits several house rules: success at a cost (01 L171–175), NPCs don't roll outside a fight (L177), nonlethal ranged and spell attacks (09 L108–113), and the DC ladder.
- **Yardstick:** C-S2/C-S3. Official front matter carries credits, the legend and the running notes, not build steps. CC BY 4.0 change notice: see AUDIT_oraga_5e_canon A-17, which is now applied, but the house-rule list is incomplete.
- **Fix:** Move the INVENTIONS and flow rows under a final `### For Contributors` subhead. Add the four house rules to *Changes from the SRD*.

### FRONT-21 [P3] Inherited aphorisms and not-X-but-Y turns (PROSE) [d20-portable]
- **Where** (most come from the source, so fix them in both editions; memory rule, light touch only):
  - README L76 "not to tease you, but because …" → "The module leaves some of it out on purpose: those answers belong to the setting's future, and no table needs them to run the night."
  - 01 L351–352 and L401–402 say "load-bearing" twice. Keep L401 and cut L351–352 to "See *What the MM Knows*, below."
  - 02 L125–128: "What makes them monstrous is not what was taken from them but how much is left — grief, faith, exhaustion, courtesy — and …" → "What makes them monstrous is how much of them is left: grief, faith, exhaustion, courtesy. Play every scene with one of them as a scene with a person, and the horror takes care of itself."
  - 02 L232–233: "Not because the answers are dull — but because …" → "The honest night is the one nobody walks out of understanding."
  - 03 L30–31: "which is not a problem but a spotlight" → "which puts a spotlight on them".
  - 03 L40: "It is knowledge, not a bonus." → "It is knowledge, with no bonus attached."
  - 03 L190: "It matters to nobody and everybody, which is the correct proportion for a masquerade" (source; keep, it earns its place).
  - 01 L263: "Maiven Nolonaire is not a snake; she is a wary ally" (fine, it is a ruling).
  - Em-dash asides: 03 has 49 in 3,800 words, with doubled pairs at L30, L264, L278 and L339. Replace one dash of each pair with commas or parentheses.

### FRONT-22 [P3] Cross-reference and handoff mismatches (ARCHITECTURE)
- **Where:**
  - 05 L1150–1151 tells the MM to pay "as Chapter I pays *ending a fight without finishing it*". No such phrase exists in 01. Table I–3/I–4's row is "A fight ended by an out". Fix: "as Table I–3 and Table I–4 pay *a fight ended by an out*".
  - INVENTIONS_5e.md #25 cites "03 *The Other Peoples*", a section 03 no longer has, while 04 L668 still names "a Scora". Re-point #25 to 04 L668, or mark it retired.
  - Chapter cross-references use a house form ("*Buying Time*, Chapter V"), not 5e's '(see chapter 5, "Title")' (C-S41 [A]). The house form is consistent throughout, so keep it and declare it in the legend (FRONT-5) rather than converting about 420 references.
- **Verified, and resolves:** every cross-reference in README, 01, 02, 03 and 06. That covers the prep box's 14 section targets, Tables I–1 to I–4, B0/B10/B13, Table VIII–4 *Costs to Hand*, card S14 and S3, *When Somebody Draws Early*, *Running a Scattered Party*, Chapter X's spell table (*banishment*, *hold person*), and 04 B0's opening DC 13.

### FRONT-23 [P3] No closing rewards recap (CONTENT) [d20-portable]
- **Where:** 06. XP and Inspiration are in 01 Tables I–3/I–4, agenda pay in 03, and loot in 10 *The Night's Loot*.
- **Yardstick:** C-S46 [U] (session-length: a closing Rewards section).
- **Fix:** Add a short `## Rewards` block to 06 with four pointer lines: Table I–4 XP (5th level by milestone), agenda pay (Callun's 100 gp; the 30 gp gate fee; the Church's favor; the heirloom crystal), *The Night's Loot* (Chapter X), and the carried-out question as the story award.

---

## 3. What already meets the official standard (don't break it)

- **The party and level sentence** (README L7–10, 01 L39–42), with the ending level and milestone advancement stated up front, and "Standing outside at dawn" as the story milestone (C-S1, C-S44).
- **Expected duration.** Table I–1 is an AL-grade *Expected Duration* per part and sums to exactly 4 h 50 min. It has two checkpoints and an ordered cut list (C-S8, C-S15).
- **Hooks.** Six named hooks, each routed to the same opening scene (B0) (C-S4). *The First Five Minutes* matches LMoP's opening table-setup checklist (structure §1.2).
- **Rewards.** *What the Night Pays* prints non-combat awards for clever and peaceful play (C-S47). The XP math is right (2,700 → about 6,500).
- **Tone and troubleshooting.** *Tone* is a genre toolkit (C-S5). *When It Goes Sideways* uses the official troubleshooting species, with in-fiction answers (C-S25). *Safety and the Table* has no official precedent, but it is modern good practice; keep it.
- **Required rules and licence.** "What You Need" is clear. The SRD 5.2.1 attribution is verbatim, the change notice is present, and there is no WotC trademark in a title.
- **02's split.** The public half is shareable and the MM-only half is flagged (L111). Motives are stated flatly with plain verbs ("wants", "fears"; C-V10). *What the Module Never Says* is decided owner canon; don't treat it as a C-V10 defect.
- **Gift feats and 06.** 03's gift feats are well-formed SRD 5.2.1 origin feats (every cantrip on the gift list is in the SRD; the *Versatile* route is legal). 06's trail checks give a failure line that keeps the story moving (C-V16, C-S14).
- **Numbered tables** ("Table I–1") are a house choice, not a 5e defect (structure §12). Keep them. Title the untitled DC-ladder table in 01 L159 to match.
- **Maps.** The flow page (a figure-like macro map) and 08's keyed palace diagram cover C-S51 for a module without map art.

---

## 4. NEEDS-RULING (for the owner)

- **R1. "MM" or "DM"?** This is logged once, as asked. Official 5e says "you" in instructions and "the DM" only in third person. This module uses "Mirror Master (MM)" by house rule (BRIEF §5), and 01's troubleshooting box is even titled "the MM keeps defaulting to DC 20". *Background:* a 5e reader will understand "MM" once it is defined, but it marks the book as a conversion. *Question:* keep MM throughout (then define it at first use in the README, FRONT-17), or use DM in the 5e edition only?
- **R2. The designer's note (FRONT-6).** The house style guide (3.5-derived) favors signed designer-note boxes. Official 5e has none. *Question:* keep the signed note as a house signature, or convert it to an unsigned MM Note as proposed?
- **R3. Invented names (FRONT-12).**
  - (a) How should Oraga, Raunu, Boranis, Veier, Nolonaire, Rekuzan, Val'loh, Orthaen, Thenya and Phern be pronounced? Only you can say, and 5e books print this at first mention.
  - (b) Should "PG" (the era in "3164 PG") be spelled out, or dropped?
  - (c) Confirm the glosses taken from the Val'loh setting file: the Blackwatch "keep the vigil over the eastern mists"; Mazaa is "the tribes' enemy in the western mountains".
- **R4. The Church's favor (Agenda 2, FRONT-13).** Official books never leave a reward's size blank. *Question:* what is the default favor Prelate Kovaun grants: a generic "one favor she can grant without scandal", or something specific?
- **R5. A full reorder into Parts + Appendices (FRONT-11).** The recommended fix only regroups the README, because renumbering touches about 420 references. *Question:* is the regrouping enough, or do you want the book renumbered (for example: Introduction, Parts 1–3, Appendices A–E)?
- **R6. Where the agendas live (FRONT-1).** The minimal fix is an "MM Only" banner in Chapter III. The cleaner fix moves the eight agendas out of the player chapter. *Question:* banner, or move?
