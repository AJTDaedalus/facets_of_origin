# RESEARCH: What Call of Cthulhu Can Teach Facets

*Research memo, 2026-10-03. Status: complete. No project files changed apart from this one.*

**Question.** Is there anything in the owner's Call of Cthulhu (CoC) books worth bringing into Facets, and if so, what can we legally use?

**Sources read.** I extracted text with PyMuPDF to scratch and searched it. I did not read any book in full.
- *Masks of Nyarlathotep* (core campaign book, 669 pp.), plus the America and Peru books, the Peru handouts, the Keeper Reference Booklet (85 pp.) and the pregenerated-characters booklet.
- *The Things We Leave Behind* (a collection of contemporary scenarios, 138 pp.).
- The owner's individual character-sheet and background PDFs. These are image-only, with no text layer and no form fields, so I took the pregen layout from the characters booklet, which does have text.
- **There is no core rulebook in the folder.** Everything I say about CoC rules comes from how the adventures use them. The adventures cite page numbers in the rulebook for its optional Luck rule, the development phase, wound recovery and Sanity recovery.
- Chaosium's open content: I downloaded and searched the *Basic Roleplaying ORC Content Document* (303 pp.), the ORC License and its official Answers & Explanations (AxE) document, and the older *BRP System Reference Document 1.0* with its *BRP Open Game License*.

**Hard rule kept.** This memo quotes no CoC text and uses no CoC names, monsters or lore. Wherever a CoC mechanic is named, the name is there only to identify it for the owner. None of these names should appear in Facets text.

---

## 1. Executive summary: the top five

Facets already does most of what CoC does well, and often does it better. CoC's luck currency, rerolls with stakes and bonus dice are already covered by Sparks, Borrowed Trouble, extra dice, success at a cost, the Oracle and the *Stuck?* button. The real lessons from the books are about **running an adventure**, not about dice. In priority order:

1. **Adopt: clue maps plus a "vital clue" flag (all rulesets, and the app).** Every *Masks* chapter ships a clue flow diagram. *Things We Leave Behind* tells the Keeper to lean toward letting players find the clue that moves the story, and supplies an NPC who can bring up clues the players missed. Facets has the three-clue rule (MM2) but no map, no flag and no safety net. Proposal: in an adventure's data file, scenes list the clues they hold and the conclusions those clues point to. A clue marked **vital** is never put behind a roll; the roll decides only what it costs or what extra comes with it. The app then draws the map and warns the author about any conclusion with fewer than three routes. This costs players nothing in rules, and it is exactly the bookkeeping the digital layer exists to absorb.
2. **Adapt: a chase as a set piece (Lean Facets first, then d20).** Facets has no chase rules at all. CoC and BRP both treat a chase as its own scene type, and the *Masks* example is laid out well: a short **course** of three or four locations, each with a hazard and the one or two approaches that get past it, plus a small card for the pursuers. Proposal: a four-band **gap track** run by the ordinary 2d6 tiers, prepped as a course of hazards. It takes half a page in III.2 and reuses the Threat Clock's visual language. The text has to be original (see §2.4).
3. **Adopt: time as the price of a failed search, on a visible deadline.** In *Things We Leave Behind*, a failed records search can be tried again, but each try costs hours, and the scenario runs against a deadline. Failure is never a dead end, only a cost against the clock. Facets has every piece of this already (the Pressure die, Threat Clocks, *Trying Again*). What's missing is the MM2 guidance that connects them for investigation scenes: the clue is always reachable, and failing just costs time on a clock the table can see.
4. **Adopt: rewards keyed to story outcomes, listed in the module (adventure format).** Each *Masks* chapter ends with a list of rewards tied to specific results: solving the central crime pays a little, an ally dying costs a little, breaking the cult pays more. Facets modules should end each act with a short **"What it earned"** list (Sparks, a level, standing, treasure, Drive payoffs) keyed to what the party actually did. This puts the reward loop MM3 describes onto the page, so the MM isn't left to improvise it.
5. **Adapt: pregens and a cast sheet built for the table.** Each CoC pregen backstory **ends with the reason this character is at the opening scene**, and carries four one-line hooks (look, temperament, belief, a treasured object). The Keeper Reference Booklet collects every stat block by chapter, grouped by role (allies, adversaries, hirelings, plus generic "average crowd member" profiles), each with a one-line identity tag, and is printable on its own so the Keeper doesn't flip pages. Facets should adopt two pieces. First, a "why you're here tonight" line on every pregen, with a "something you'd hate to lose" line next to the Drives. Second, a per-module **cast sheet**, generated from the `.fof` files like the Bestiary, grouped by role, including crowd profiles.

**What to leave alone.** Facets should not take a Sanity meter, a second luck currency, penalty dice, percentile skills or experience checks. §5 lists what CoC does badly.

---

## 2. Licence: what is actually open

### 2.1 What Chaosium has released

| Release | Licence | What it covers | CoC material? |
|---|---|---|---|
| *Basic Roleplaying: Universal Game Engine* ORC Content Document (2023; credit line dated 2024 on Chaosium's ORC page) | **ORC License** (Library of Congress TX 9-307-067) | The BRP text: d100 skills, characteristics, combat, magic and powers, plus optional systems including Sanity, Passions, Allegiance, Reputation, Fatigue, a Luck *roll*, and chases with a range track | **No.** Chaosium's ORC page lists Call of Cthulhu as a trademark, which makes it Reserved/Product Identity. |
| *BRP System Reference Document 1.0* (2020) | **BRP Open Game License 1.0** (Chaosium's own) | An earlier BRP SRD | Explicitly **prohibited**: all CoC product-line material and all Cthulhu Mythos works, "including those that are otherwise public domain". |
| CoC 7th edition rules, *Masks*, *Things We Leave Behind* | All rights reserved | Everything | Proprietary. The *Masks* booklet allows copying only character sheets and handouts, for in-game use. |

The ORC Content Document is a **free PDF**: <https://www.chaosium.com/content/orclicense/BasicRoleplaying-ORC-Content-Document.pdf>. It is the SRD for the *BRP: Universal Game Engine* book. The printed book is a separate commercial product. I downloaded the PDF and checked the claims below against it.

### 2.2 Which CoC mechanics are in the open SRD?

I checked by searching the 303-page ORC document for each mechanic.

| CoC mechanic | In BRP ORC document? | Status for Facets |
|---|---|---|
| **Sanity** (a d100 pool that drains, with temporary insanity) | **Yes, as a BRP option**: SAN = POW×5, roll against current SAN, a temporary-insanity threshold, d6 and d8 effect and duration tables. It is not CoC's version: CoC's bouts of madness, indefinite insanity and the Mythos cap on maximum Sanity are not there. | BRP's version is ORC-licensed text. CoC's version is proprietary. In both cases the idea of a mental-strain pool is a general mechanic. |
| **Luck as a roll** (POW×5, for "is fortune with me?") | **Yes** | ORC text. The idea itself is general. |
| **Spending Luck points** to change a roll | **No.** Zero hits; the document has only the Luck *roll*. | It's CoC's optional rule and proprietary as written. The general idea of a spendable resource that improves a roll is not protectable, and Facets already has one (Sparks). |
| **Pushed rolls** | **No** | Proprietary as written. Chaosium's 2020 BRP OGL listed "Pushing: if substantially similar to the Call of Cthulhu rules" as prohibited content. That's a clear statement that Chaosium sees it as a CoC signature. |
| **Bonus/penalty dice** (an extra tens die, keep the better or worse) | **No.** Zero hits. | The d100 tens-die version is CoC's. The general "roll an extra die and keep the best" is everywhere: Facets' extra dice, and advantage in SRD 5.2.1 under CC BY 4.0. |
| **Chases** | **Yes, BRP's own.** The GM sets up six aspects (start, course, skills, combat, duration, conclusion); a five-band range track; each round's roll moves participants along it; a d10 trouble table for vehicles. | ORC text. CoC 7e's chase system, which is built on locations and movement actions, is different and proprietary. Chase-as-abstract-track is a general idea. |
| **Passions** | **Yes** (a percentile rating that inspires bonuses and despair on a fumble) | ORC text. The 2020 OGL had prohibited it if similar to Pendragon or RuneQuest, and ORC has since opened BRP's version. Facets' Drives already do this job. |
| **Experience checks** | **Yes** | ORC text. Not wanted (§4). |
| **Mythos, Keeper, investigator conventions** | **No.** "Cthulhu Mythos" appears only twice, both times as a suggested genre. | Reserved. Avoid. |

### 2.3 What the ORC License requires, and its friction with GPLv3

The full text is at <https://azoralaw.com/wp-content/uploads/2023/09/ORC-License.FINAL_.pdf> and the AxE at <https://azoralaw.com/wp-content/uploads/2023/09/ORC-AxE.FINAL_.pdf>. The key terms, paraphrased:

- **Licensed Material** is the expression needed to convey a game's functional ideas: rules, procedures, statistics, outcome methods and so on (§I.e). **Reserved Material** is trademarks, trade dress and creative expression that isn't essential to the mechanics: art, characters, settings, plots, proper nouns (§I.h). Reserved Material is not licensed unless the licensor expressly designates it.
- The grant is worldwide, royalty-free and **irrevocable**, and it terminates only on breach, with a 60-day cure (§II.a, §V.a).
- **The licence is share-alike for mechanics (§II.b).** It applies to a "Derivative Work", which for a single-system product is the **whole product** (§I.c). Every recipient must get an irrevocable ORC licence to the *Adapted Licensed Material*, meaning the mechanical expression in that product. And you **"may not offer or impose any additional or different terms or conditions on the Licensed Material."**
- **Required notices (§III)**: the ORC notice with the TX number, attribution for every upstream licensor, a statement of your own Reserved Material, and a statement of anything you have expressly designated as Licensed Material. Chaosium also asks for the "Powered by BRP" logo and a set credit line (<https://www.chaosium.com/orclicense/>).
- The AxE answers a closely related question directly. Asked "Can I use ORC Licensed Material in my CC-BY product?", it says **no**, unless every upstream licensor agrees. Dual-licensing the *same work you wrote yourself* under ORC and another licence is "not prohibited", but the AxE advises keeping the editions separate.

**What this means for GPLv3 Facets. Please read this carefully; I am not a lawyer.**
- If Facets copied or adapted **any BRP ORC text**, the mechanical expression across the whole Facets product would become Adapted Licensed Material, and would have to be offered under ORC. GPLv3 §10 forbids "further restrictions", and ORC §II.b forbids "different terms". Each licence demands that it alone govern the same material. By the AxE's own reasoning for CC BY, you cannot relicense ORC material under a different licence. The ORC notice, Reserved-Material statement and logo would not all obviously fit within GPLv3 §7's list of allowed additional terms. **No FSF or OSI ruling on ORC–GPL compatibility exists that I could find.** Treat the two as **not known to be compatible.**
- Facets d20 sits on SRD 5.2.1 under CC BY 4.0, which is permissive and only asks for attribution. ORC is a different kind of licence: it is copyleft, and its copyleft competes with GPL's.
- **The safe route, which I recommend, is to use no BRP ORC text at all.** Every recommendation in this memo is a general mechanic or a general GM practice, to be written fresh in Facets' own words. US copyright does not cover "any idea, procedure, process, system, method of operation" (17 U.S.C. §102(b); U.S. Copyright Office, *Circular 33: Works Not Protected by Copyright*, <https://www.copyright.gov/circs/circ33.pdf>). On that basis Facets needs neither ORC nor any Chaosium permission.
- **One caution on look-alikes.** Facets' own policy says resemblance is fine and only licences matter (memory: *feedback_similarity_ok*). Even so, don't name anything "push", "Sanity", "Luck points", "bonus/penalty die" or "Keeper", and don't copy the *structure* of CoC's rule write-ups (step order, table layout). That keeps Facets well clear of the "substantially similar" line Chaosium drew in 2020, even though that line has no force against a game that never accepted the BRP OGL.

### 2.4 Licence status codes used below

- **GEN**: a general mechanic or practice. Not copyrightable; write it in our own words. Usable.
- **ORC**: the text exists in the BRP ORC document. Using the *text* triggers ORC and the GPL friction above, so restate the idea as GEN or don't use it.
- **PROP**: CoC-specific expression or identity. Avoid. Take only the underlying idea, and only if it is GEN.

---

## 3. Candidate table

| # | Candidate | Licence | Facets already has | Fit / value | Complexity cost | Verdict |
|---|---|---|---|---|---|---|
| C1 | Clue flow diagram + vital clues never gated + safety-net NPC | GEN | Three-clue rule (MM2); *Stuck?*: "a secret surfaces" (MM6) | **High.** Prevents the commonest investigation failure, and the app can carry it. | None for players; small authoring cost | **Adopt** |
| C2 | Chase as a set piece (gap track + hazard course) | GEN (BRP's range track is ORC *text*; don't copy it) | Nothing | **High.** A missing scene type; cinematic and social. | Half a page; one new tracker | **Adapt** |
| C3 | Failed research costs time against a deadline | GEN | Pressure die, Threat Clocks, *Trying Again* | **Medium-high.** Turns "roll until it works" into tension. | None; it's guidance | **Adopt** (MM2) |
| C4 | Story-outcome rewards listed per chapter | GEN | MM3 reward loop; d20 levels at the MM's call | **Medium-high.** Writes the reward loop into modules. | One short list per act | **Adopt** (module format) |
| C5 | Pregen "why you're here" ending + four one-line hooks | GEN | Drives (want/line) in d20; Oraga pregens | **Medium.** Faster openings; MM gets material to work with. | One or two lines per pregen | **Adapt** |
| C6 | Per-adventure cast sheet by role, with crowd profiles | GEN | Generated Bestiary; scene-card statlines; Oraga cast chapter | **Medium.** Table usability. | Generator work, none in play | **Adapt** |
| C7 | Handouts as numbered, separate, dealt objects | GEN | Oraga Ch. VIII handouts | **Medium.** The digital-first payoff is the app dealing them privately. | App feature | **Adopt** (app/format) |
| C8 | Reroll with stakes ("pushed roll") | PROP as written; GEN as an idea | Borrowed Trouble (pre-roll), *Trying Again* (fiction must change), success at a cost, d20 Sparks after the roll | **Low-medium.** Mostly redundant. The one useful piece is "name the price before the retry". | Must stay at one sentence | **Adapt narrowly** (one line in *Trying Again*) |
| C9 | Roll-to-connect when stuck (a hint roll that fails forward) | GEN (CoC's Idea roll is PROP as written) | MM6 *Stuck?*, Oracle, *Loremaster*-style "ask one more" | **Medium.** Lets the *player* pull the hint rather than wait for the MM to push it. | One paragraph | **Adapt** (optional, MM2) |
| C10 | Bonus/penalty dice | GEN idea; PROP d100 form | Lean extra dice (keep best 2); d20 advantage; difficulty steps | **Low.** Already covered. A penalty die would duplicate difficulty steps. | Would add a rule | **Reject** |
| C11 | Luck as a spendable pool | PROP (spend rule); ORC (roll) | Sparks (both rulesets) | **Low.** A second currency means bookkeeping and hoarding. | A new pool to track | **Reject** |
| C12 | Group luck roll: the unluckiest character suffers | PROP/GEN | Oracle, Pressure die | **Low.** Needs a Luck stat. | — | **Reject** (MM can pick by fiction) |
| C13 | Sanity / mental-strain pool | ORC (BRP's) / PROP (CoC's) | Avoid (Soul) for things acting on the will; Wounds; Threat Clocks | **Low.** Wrong register; real-illness depiction risk; more bookkeeping. | A new pool, tables, recovery rules | **Reject for core**; at most a setting-Facet idea |
| C14 | "Closure heals": recovery from resolving the threat | GEN | Rest rules; Drives | **Low-medium.** A nice beat, folded into C4. | — | **Fold into C4** |
| C15 | Two-mode adventure (classic/pulp alternates in one book) | GEN | MM-note "dials" | **Low-medium.** Could become a module-level heroic/gritty dial. | Doubles stat blocks if done CoC's way | **Defer** (open question Q5) |
| C16 | Non-linear hub campaign with a deadline and a per-location outcome ledger | GEN | MM3 campaign structures (Mystery) | **Medium** for MM3 guidance. | Guidance only | **Adapt** (MM3, low priority) |
| C17 | Replacement characters drawn from NPCs already met | GEN | — | **Low-medium.** Good practice for any death. | One paragraph | **Adopt** (MM3/MM4, low priority) |
| C18 | Experience checks (tick a skill on success, roll to improve later) | ORC | Levels | **Negative.** Bookkeeping, and it rewards rolling over playing. | High | **Reject** |
| C19 | Passions (a percentile emotional rating) | ORC | Drives + compels | **Low.** Drives already do it with less overhead. | — | **Reject** |
| C20 | Three success grades printed per skill (regular/half/fifth) | PROP | Three-tier outcomes on one roll | **Negative.** Three numbers per skill on the sheet. | High | **Reject** |

---

## 4. Details

### C1: Clue maps and vital clues (Adopt)

**What it is.** The adventure gives the GM a diagram per chapter linking scenes, the clues each one holds, and where each clue points. The text tells the GM to understand what each clue *means* before play. Modern scenarios add two habits: say outright that the vital clue should be easy to find, and supply an NPC whose job is to turn up what the party missed. One scenario says plainly that the party does not need to follow every line of inquiry, only enough of them.

**Fit.** This matches the Facets philosophy exactly: the story never stalls on a die. MM2 already has the principle and the three-clue rule. What's missing is the tooling, and that's the digital layer's job.

**Recommendation.**
- *Adventure format (`.fof` / scene cards):* each scene lists `clues: [{id, points_to, vital: bool, how_found}]`. Each conclusion lists the clues that lead to it.
- *Generator:* `build_scene_cards` (or a sibling tool) draws a clue map into the module, the same way the Bestiary generates stat blocks. Add a test: any conclusion with fewer than three routes, or any vital clue reachable only through a roll, is a failing check for the author.
- *MM2, one paragraph:* "A vital clue is never behind a roll. Roll for what it costs, how long it takes, or what else comes with it." Add a line about a **safety-net NPC**: one cast member per module whose role is to bring up a missed clue, used with *Stuck?: a secret surfaces*.
- Cost to players: zero. Cost to authors: a few fields per scene, which pays for itself the first time the map catches a hole.

### C2: Chases (Adapt)

**What it is.** CoC and BRP each give chases their own procedure, because a fight rule run with everyone moving is dull. The ORC BRP chase has the GM fix six things in advance, then moves participants along a five-band range track based on each round's rolls. The *Masks* write-up adds the most useful piece. Its chase is a **course**: about four locations in order, each with a hazard and one or two ways past it (a strength or a jumping approach, frightening or barging bystanders aside, a short-cut found by navigation). There is also a small card listing only the pursuers' movement-relevant numbers.

**Fit.** Chases are People Fun. Everyone acts, everyone describes, near-misses are public, and nobody counts squares. Facets has nothing for them, so an escape currently has to run as a fight or as a single roll.

**Proposal (Lean Facets; original design, not BRP text).**
- **The gap track.** Four bands, *Grabbing distance / Close / In sight / Lost*, shown like a Threat Clock. The quarry starts one band from where it would escape or be caught; the MM sets the start from the fiction.
- **Each exchange**, every runner names how they're handling the current hazard on the course and rolls the stat that fits, which moves the gap: **10+** one band your way; **7–9** hold, or move a band your way at a cost the MM names (drop something, take a scrape, split from the group); **6−** one band against you. The party's best roll moves the gap and the worst one sets the cost, which keeps the whole table rolling without adding up totals.
- **The course.** The MM preps three to five hazards, each with a *likely* stat and a *clever* alternative. Each exchange moves to the next hazard. If the course runs out before the gap closes, the quarry escapes or the chase becomes a fight, whichever the fiction calls for.
- **Sparks, Help and Borrowed Trouble** work as on any roll. A chase is a natural place for Borrowed Trouble ("you make the jump, but the satchel goes into the canal").
- *Facets d20:* the same track, with a DC per hazard: success moves a band; fail by 1–4 and you hold at a cost; fail by 5+ and you lose a band.
- *Software:* `combat.py` already owns shared rules. A chase is a small state machine (band index plus hazard index). The simulator rule in CLAUDE.md applies: the simulator should call shared code, not re-implement the rule.
- *Oraga Night* has foes who flee and a night that runs on a clock, which makes it a ready test bed.

**Licence.** "Track the distance in abstract bands and move along it on each roll's result" is a general mechanic. **Don't** copy BRP's six-aspect list, its band names, its range-effect columns or its trouble table. Under ORC, doing so would put the whole Facets product under ORC share-alike (§2.3).

### C3: Time as the price of failure (Adopt)

**What it is.** A failed research roll can be retried, but each try costs a few hours, and the scenario runs against a hard deadline. A failure becomes a cost against the clock, never a dead end.

**Facets equivalent.** All the parts exist. *Trying Again* allows "time that cost something"; the Pressure die makes "time is never free somewhere dangerous" a rule; Threat Clocks give a deadline the table can see. What's missing is the statement that puts them together for **investigation**. In MM2's *Investigation* section: "A failed search or study can always be tried again. The price is time. Tick the clock, roll the Pressure die, or let the rival get there first." No new rule is needed.

### C4: Story-outcome rewards (Adopt)

**What it is.** Each chapter closes with a list of rewards tied to specific results. Some are positive (the mystery solved, the villain stopped, a monster destroyed) and some are negative (an ally the party could have saved died). Recovery comes from *closure*, not just rest.

**Fit.** MM3 says the reward loop should count "exploring, treasure, goals, consequences", not kills. A module that writes the loop down per act saves the MM from inventing it at the table, and tells players what the story valued. In the d20 tree, levels come at the MM's call, so a "this act earns a level if…" line fits naturally.

**Recommendation.** Add an optional **"What it earned"** block to the module template (Oraga Night's acts are the first user): three to six bullets, each a deed paired with a reward (Spark, level, standing with a faction, treasure, a Drive payoff). Allow negative entries sparingly, and only for consequences the players could see coming. Keep the reward in Facets currencies; there's no Sanity analogue to restore.

### C5: Pregens that walk into the first scene (Adapt)

**What it is.** Each CoC pregen gets one page: an identity line (age, occupation, origin), numbers, a backstory paragraph that **ends with why they are at the campaign's opening**, and four one-line hooks: appearance, temperament, belief, and a treasured object. In CoC the backstory also matters mechanically (it can be put at risk, and time spent with it aids recovery). Facets should not copy that linkage.

**Facets equivalent.** d20 has Drives (a want and a line); the Oraga pregens exist as `.fof` files.

**Recommendation.** Two small additions to the pregen template, in all rulesets:
- **"Why you're here tonight"**: the last sentence of the background, tied to the module's opening scene.
- **"Something you'd hate to lose"**: a person, an object or a place, sitting next to the Drives as a thing the MM may put in danger, which pays a Spark under the existing compel rule. It needs no new mechanics: it's a third Drive-shaped prompt that rides on the compel. If the owner wants zero new fields, put it in the background text instead (Q3).

### C6: The cast sheet (Adapt)

**What it is.** A separate booklet gathers every stat profile in the campaign by chapter, grouped by role (allies and independents, adversaries, hirelings) plus generic "average crowd member" profiles. Each opens with a one-line tag (age, a two- or three-word character note), so the Keeper can play the NPC from the tag. It's built to be printed and kept beside the GM screen.

**Facets equivalent.** The generated Bestiary, statline blocks on scene cards, and Oraga's cast chapter (grouped by house, faction and guests, with an epithet per character, which is already close).

**Recommendation.** Generate a **cast sheet** per module from its `characters/` and `enemies/` `.fof` files, grouped by role and including crowd profiles (one "guard on duty", one "guest at the ball"). Each entry gets a one-line tag and its statline. It's tooling only and can't drift from the source, which matches the "generated, never hand-edited" rule in CLAUDE.md.

### C7: Handouts (Adopt, app and format)

**What it is.** The campaigns treat handouts as first-class: numbered, printed in their own booklet, referenced by number in the scene text. The modern scenarios use contemporary media (a forum thread, a sample audio file, a list found in a room).

**Facets equivalent.** Oraga Night has a handouts chapter, and its invitation has an interactive rendering.

**Recommendation.** Make the handout a `.fof` object type (`id`, `title`, `body`, `audience: table|player|mm`, `revealed_by: scene/clue id`), and let the app **deal** a handout to one player or to the whole table, logging who holds what. This connects to C1: a handout is often a clue. Private deals are the digital-first payoff, because secret information shared between players is a socialising engine, and paper does it badly online.

### C8: Reroll with stakes (Adapt narrowly)

**What it is.** In CoC, a player who fails can justify a second attempt. The GM signals what failing again will cost, and the second failure brings that cost. *Masks* uses this throughout: a failed second attempt at a social scene gets the party thrown out; a failed second climb or search drops someone down a shaft or brings something up from below.

**Facets equivalent.** Covered from several directions. Lean Facets has Borrowed Trouble (take a complication for a die *before* rolling), the 7–9 band (success at a cost), the Graceful Fail and *Trying Again* (allowed when the fiction has changed). Facets d20 has Sparks spent *after* a miss.

**What's worth taking.** One idea only: **name the stake before the retry.** Lean already says "say it out loud" for difficulty.

**Recommendation.** Add one sentence to *Trying Again*: "Raising the stakes counts as a change: the MM names what a second failure will cost, and if you still try, a 6− brings it." Don't add a separate named rule, and never call it a "push" (§2.3).

### C9: Roll to connect the dots (Adapt, optional)

**What it is.** CoC uses an intellect roll to get stuck players moving. Even when it fails, they still learn the connection, but they learn it the hard way. *Things We Leave Behind* uses the same roll to let a character connect a detail to something they know.

**Facets equivalent.** MM6 *Stuck?* (the MM pushes); the Oracle (the MM asks the dice what's true).

**Recommendation.** A player-pull counterpart, as an MM2 option: "*Stuck? Ask your head.* A player may roll Mind (d20: Intelligence) to work out what links two things the party knows. **10+** the MM says it plainly; **7–9** the MM says it, and it took time or tipped someone off; **6−** they get it the hard way: the answer finds them, with danger attached." It fails forward on every result. It's GEN, but write it fresh and don't call it an "Idea roll".

### C10–C12: Dice and luck currencies (Reject)

- **Bonus/penalty dice.** Lean's "add a d6, keep the best two" *is* a bonus die with a bell curve, and d20 has advantage. A penalty die would duplicate difficulty steps and add a cancellation rule. No gain.
- **Spendable Luck.** *Masks* tells classic-mode Keepers to use the spend-Luck rule to keep investigators alive and the campaign on track. In other words, CoC needed a currency after the roll to make a lethal campaign survivable. Facets already has that in Sparks, and the Facets research (*Through the Mirror: why Sparks reset*) found that piling currencies up produces hoarding. A second pool adds bookkeeping for nothing.
- **Group luck roll, unluckiest suffers.** It's a neat way to answer "who falls through the floor", but it needs a Luck stat. The MM can choose by fiction (who searched there), or roll the Oracle.

### C13–C14: Sanity and closure (Reject for core; fold the good beat into C4)

**What it is.** A pool of mental stability that horrors drain, with short-term breakdowns at a threshold. Recovery comes through therapy, time, or **defeating the source** of the fear. The BRP ORC version even carries its own disclaimer about trivialising mental illness.

**Why not.** Facets is written in an adventure register of wonder and heroism (research doc; MEMORY). A drain-to-breakdown meter pulls toward horror, adds a pool and two tables, and puts a depiction of mental illness at the table, which MM4's safety tools would then have to manage. Lean already covers "a voice in your head telling you to kneel" with **Avoid (Soul)**. A setting Facet that really wants dread can build it from a Threat Clock aimed at one character's composure, with no new subsystem.

**What to keep.** *Closure heals.* Resolving the threat should feel restorative. Put it in C4 as a reward line ("the house is quiet again: everyone recovers a Wound"), not a meter.

### C15–C17: Campaign craft (Defer / Adapt / Adopt, low priority)

- **Two modes in one book.** One campaign, run either "classic" or "pulp": alternate tougher combat profiles for NPCs, sidebars that raise the danger in key scenes, and guidance on clue difficulty (in pulp mode, important clues are put in plain view). This is a tonal dial for a whole module. Facets could offer a module-level *heroic/gritty* switch: one line per encounter, not doubled stat blocks. Deferred to the owner (Q5).
- **Hub campaign with a deadline and an outcome ledger.** The chapters can be played in any order, a fixed date caps the campaign, and the finale describes what each location looks like on that date, depending on what the party did there. It's good MM3 guidance for a *Mystery* or *Race* campaign. The "ledger" is just Threat Clocks per location that the app can show.
- **Replacement characters from NPCs met.** For lethal moments, *Masks* suggests drawing a replacement from NPCs the party already knows. One paragraph in MM4 (or the Death Choice text) costs nothing and keeps a new player connected to the story.

### C18–C20: Character bookkeeping (Reject)

Experience checks, percentile Passions and three printed success grades per skill all add numbers to the sheet and steps to every roll. Facets' core research says the opposite: keep it under four working-memory chunks, automate it within three sessions, and avoid modifier arithmetic. Drives and levels already do these jobs.

---

## 5. What CoC does badly (avoid)

1. **Gating clues behind skill rolls.** The *Masks* introduction has to advise pulp-mode Keepers to put the important clues in plain view, which implies the classic default doesn't. Many scenes hang information on a perception or library roll. Facets' fix is C1.
2. **A sprawling skill list on a flat d100.** A typical pregen has about sixteen skills plus several languages, with a 50% social skill that fails half the time. A flat d100 makes a specialist feel unreliable. That is exactly what the bell-curve research in `research/dice_system_analysis.md` warns about.
3. **Bookkeeping density.** HP, magic points, Sanity, Luck, plus half and fifth values for every skill, plus (in pulp) talents that spend 10 Luck. The dual classic/pulp profiles double each stat block. Facets' digital layer exists so players never see this.
4. **Lethality patched after the fact.** The revised *Masks* had to tone down encounters to prevent party wipes, recommends the Luck rule to keep investigators alive, and tells Keepers to plan for replacement characters. Facets should design survivability in from the start (HP/Wounds, the Death Choice, Sparks), not bolt it on.
5. **Prep burden.** A 669-page campaign that the Keeper is told to study before play, with cheat sheets recommended and constant references to rulebook pages. Facets modules should keep prep in generated cards, maps and cast sheets (C1, C6), and never reference a book the MM doesn't have open.
6. **Register and content.** *Things We Leave Behind* deals with child abduction, suicide and body horror in a contemporary setting. Fine for its audience, wrong for Facets' default. *Masks* treats real cultures as exotic backdrops, and its own disclaimer admits the portrayals may not be accurate. Facets should keep the adventure register, keep its peoples invented, and keep safety tools (MM4) prominent.
7. **A fixed doomsday plot under a claim of freedom.** "Go anywhere" sits on top of a world-ending date and a single villain plan. It's thrilling when the table is up for it, and a railroad when it isn't. If Facets borrows the hub-and-deadline shape (C16), the ending should vary with the per-location ledger, as *Masks*' finale does, and not hinge on one pass/fail.
8. **Mental illness as a game resource.** See C13.

---

## 6. Open questions for the owner

Each question has the background needed to answer it without the rest of the memo.

**Q1. Should Facets ever use Chaosium's open BRP text, or stay "general ideas only"?**
*Background:* Chaosium's open rules (Basic Roleplaying) are under the ORC License. ORC requires that every *game mechanic* in a product that uses its text be offered under ORC too, and it forbids "different terms". GPLv3, Facets' licence, has the mirror-image demand. Nobody has ruled on whether the two can coexist, and ORC's own FAQ says ORC material can't be relabelled as CC BY. If we only borrow general ideas in our own words, which copyright doesn't protect, the question never comes up. *My recommendation:* ideas only, never ORC text. *Your call:* agree, or do you want ORC kept open for some separate future product?

**Q2. Do you want a chase rule, and in which ruleset first?**
*Background:* Facets has no rule for a pursuit, so an escape currently plays as a fight or as one roll. The proposal is a four-band "gap" tracker, moved by the normal roll results, with the MM prepping three to five hazards for the route. It's about half a page. *Options:* (a) Lean Facets first, (b) Facets d20 first, (c) both together, (d) not now.

**Q3. Should pregens and characters get a "something you'd hate to lose" line?**
*Background:* CoC characters list a treasured possession and important people, which gives the GM things to threaten. Facets d20 has two Drives (a want and a line). The proposal adds a third prompt (a person, object or place), and when the MM puts it in danger it pays a Spark through the existing compel rule. No new mechanics, but one more line on the sheet. *Options:* (a) add it to the sheet, (b) only in pregen background text, (c) no.

**Q4. Should modules list rewards per act, tied to what the party did?**
*Background:* CoC chapters end with a list such as "solved the murder: a reward; the ally died: a penalty". Facets' MM3 says rewards should count goals and consequences rather than kills, but modules don't currently spell them out. The proposal is a short "What it earned" list per act in Facets currencies (Sparks, a level, standing, treasure). *Question:* yes or no? And should negative entries (a cost when an ally dies) be allowed at all?

**Q5. Do you want a module-level heroic/gritty dial?**
*Background:* The CoC campaign can be run "classic" (scarce clues, deadly) or "pulp" (obvious clues, tougher heroes, more action), with alternate numbers printed throughout. Facets could offer one switch per module, with one line per encounter saying what changes. That doubles nothing, but it is one more thing for authors to write. *Options:* (a) yes for future modules, (b) only as general MM advice, (c) no; one tone per module.

**Q6. Should the app own clue maps and handouts?**
*Background:* The two biggest lessons from these books are clue maps (so investigations can't stall) and handouts (dealt privately to one player or shown to the table). Both need small additions to the adventure file format and the app. It's software work, but players never see a new rule. *Question:* add them to the software roadmap, and should the clue check (every conclusion has three routes, no vital clue behind a roll) be an enforced test like the other generated-content invariants?

---

## Sources

- Chaosium, *Basic Roleplaying ORC Content Document*, <https://www.chaosium.com/content/orclicense/BasicRoleplaying-ORC-Content-Document.pdf> (downloaded and searched: Sanity option at its *Sanity (Option)* section; Luck roll; Chases and range track; Passions; no hits for "bonus die", "penalty die", Luck spending or pushing).
- Chaosium, ORC licence page, <https://www.chaosium.com/orclicense/> (Call of Cthulhu listed among excluded trademarks; credit line; "Powered by BRP" logo).
- Chaosium, *BRP System Reference Document 1.0* and *BRP Open Game License 1.0* (2020), via <https://chaosium.com/brp-current-srd-download-it>; announcement: <https://www.chaosium.com/blogannouncing-the-basic-roleplaying-system-reference-document-and-open-game-license/> (Prohibited Content lists CoC product lines, all Mythos works, and mechanics "substantially similar" to CoC Pushing and Sanity).
- Azora Law, *ORC License* (TX 9-307-067), <https://azoralaw.com/wp-content/uploads/2023/09/ORC-License.FINAL_.pdf>, and *ORC AxE*, <https://azoralaw.com/wp-content/uploads/2023/09/ORC-AxE.FINAL_.pdf> (§I.c, §I.e, §I.h, §II.b, §III; AxE on CC BY and dual licensing).
- U.S. Copyright Office, *Circular 33: Works Not Protected by Copyright*, <https://www.copyright.gov/circs/circ33.pdf>; 17 U.S.C. §102(b).
- Owner's PDFs (local, not redistributed): *Masks of Nyarlathotep* core, America, Peru, Peru handouts, Keeper Reference Booklet, characters booklet; *The Things We Leave Behind*.
- Facets context: `CLAUDE.md`, `research/dice_system_analysis.md`, `COMPARISON.md`, `player_handbook/III.1`, `III.2`, `mm_manual/MM2`, `MM3`, `MM6`, `facets_d20/06`, `facets_d20/README.md`, `adventures/oraga_night/`.

---

## Owner decision (2026-10-05)

The owner reviewed the recommendations and decided **not to bring any of them into Facets**. This memo stays as a reference only. Its six questions are closed.
