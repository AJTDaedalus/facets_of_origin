# BRIEF — Oraga Night, Rebuilt as the Starter Module

**Date:** 2026-09-08 · **Tier:** Brain · **Parent:** `docs/BRIEF_oraga_starter_module.md` §6
**Depends on:** `docs/BRIEF_lineage.md`, `docs/BRIEF_valloh_facet.md` (both must land first; the pregens load through them)
**Feeds:** `docs/DESIGN_oraga_rewrite.md`, `docs/TASKS_oraga_rewrite.md`
**Rulings in force:** the Bought hold the gate (yes); the prelude is cut; magic is as written; the Uninvited stay unbeatable; the canonical outcome and the spoiler boundary stand; PCs are Orthaen or rarely Phern; weapons culture as ruled; the written-word ban is canon with both carve-outs; **"old coin" stays as a deliberate red herring** (§6.1); **the audit's R2/R3 are settled before this module's fights are tuned** (`BRIEF_fun_second_act.md` precedes §11 here).
**Pattern source:** `style/analysis/adventures.md` (the 3.5-era module conventions, concepts only). Its §9 checklist is the acceptance list for this rewrite.

---

## 1. What is being made

The existing nine-file module is rebuilt in place under `adventures/oraga_night/`. Most prose survives. What changes is the *architecture* (front matter, hooks, clock, alert state, scene cards), the *opening* (the line outside the gate, no prelude), the *combat arc* (three escalating opt-in fights, each a scene card, one of them new), the *characters* (pregens rebuilt through Lineage and the Val'loh Facet; advancement happens), and the *magic chapter* (Chapter VIII deleted; the Facet replaces it).

## 2. File plan

| File | Action | Notes |
|---|---|---|
| `README.md` | rewrite contents table; add "what you need" line pointing at the Val'loh Facet | |
| `01_Overture.md` | **rebuild** to the front-matter battery (§3) | keeps tone, safety, canon-and-your-table, what-the-MM-knows, what-the-night-pays |
| `02_The_World_and_the_Night.md` | trim the public section to what a player needs on the night; the rest moves to the Facet's `V3` gazetteer; MM-only truth unchanged | remove the "there are no magic domains" paragraph and the "Magic is different here" bullet everywhere |
| `03_Masks_and_Agendas.md` | keep agendas verbatim; rewrite *Making Characters* to Lineage + Facet; rebuild the five pregens (§8) | "How You Got In" moves to the Overture as the hooks |
| `04_The_Ball.md` | keep rooms, undercurrents, Movements I–V; add the alert-state paragraph above the rooms (§5); Movement I becomes a full scene (§4); *Trouble You Can Walk Into* becomes pointer lines to the scene cards; add the Q&A blocks (§9) | |
| `05_The_Longest_Night.md` | keep the attack, the Crossing, the Fractures, the endings; add the gate (§6) as a Movement VII scene and its ⟨If History Breaks⟩ branch | |
| `06_Wings.md` | **delete the prelude wing**; keep the aftermath wing; add the advancement beat (§8.3) and the Bought thread (§6.5) | the mask-maker becomes one aftermath paragraph |
| `07_Cast_of_the_Ball.md` | unchanged except: a Bought sergeant and captain entry (§6), and Q&A blocks for Corval, Vorlain, Raunu's summons | |
| `08_Appendix_Tribes_of_Valloh.md` | **delete**; replace with a one-paragraph pointer file or fold the pointer into the README | |
| `08_Handouts.md` | keep; night-tracker gains the **clock column** (§5) and the three scene-card IDs in the Optional Steel table | |
| **new** `09_Scene_Cards.md` | three one-page cards (§7) plus the two sidebar fights as half-cards | generated stat lines (see §11) |
| `enemies/` | add `bought_blade`, `bought_sergeant`, `bought_captain` as module-local reskins with Val'loh `description`/`organization`; everything else unchanged | the Bestiary files stay setting-agnostic (B9) |

## 3. The Overture, rebuilt (front-matter battery, in this order)

1. **What this adventure is.** Party size 3–5; starting Facet level 0; ending: Facet level 0 as a one-shot, **Facet level 1 by the end of the aftermath wing**; play length 4–6 hours as written, 3 sessions with the aftermath.
2. **What you need.** The core rules and the Val'loh Facet (`settings/valloh/`); "every enemy's Resolve, stance, and Techniques are on its scene card; you need no other book."
3. **The story so far** (unchanged).
4. **Synopsis** — one paragraph per Movement, each ending with the world-state ("By the end of Movement IV, the room has been told something it does not know what to do with"). The current *Night in Seven Movements* list is already this; expand each line to a paragraph.
5. **Hooks** — six named, bold-titled, converging hooks, each 3–6 sentences, each ending *"Begin at the Gatehouse Court, B1, Movement I."* Drawn from *How You Got In*: **The Invited · The Entourage · The Discarded Invitation · Hired for the Night · The Patron's Errand · The Wrong Place, Deliberately.** Each names which agendas fit it.
6. **Running the night** — the tone section, *What the Night Pays* (unchanged, printed rewards), and a new paragraph: **the three fights are visible and optional; here is how to nudge a restless table toward one without forcing anyone** (three sentences, one per fight).
7. **Format legend** — `**B1.**` keys, italic read-aloud with trigger lines, the three sidebar species, scene-card IDs (`S1`–`S3`, half-cards `S4`–`S5`), the enemy notation (tier · Resolve · stance triggers · Techniques · TR), and the clock column.
8. **Safety** (unchanged).

Signed designer's note, one per Part (the style guide's highest-trust register): the Overture's note says why the Uninvited cannot be beaten and what the fights are *for*.

## 4. Movement I as the first scene

The module opens **on the approach**, at the earliest mingling. Not a transition; a keyed scene with everything the old Night One did that mattered folded into the line.

**B0. The Approach and the Line** *(new key, before B1)*. Read-aloud on first sight of the lit palace (exists: "The whole hill is lit…"). Then the line: the best gossip hour of the year, and the module's *approach loop* begins here — a player character seeks someone or is sought. Scheduled in the line: Corval receiving by name; the Thenya delegation waiting with thinning patience; a burned-invitation footman quietly selling a card to someone two places ahead (the Discarded Invitation hook made visible); every great house's hired swords idling at the edge of the court (fact from the old Night Two, now an omen-shaped detail: *House Boranis hired none*); and, for the sharp-eyed, a tall pale factor already inside, having arrived early and unremarkably.

**The omen** (unchanged): nine honor guards, facing inward.

**Agenda beats** (unchanged) plus: Rumor Table rolls are legal from the first minute; the line is where a table learns the roll.

**The first roll of the night** should be a social one at Standard, with the 7–9 named from the MM2 table. The Overture's designer note says so: "the first roll teaches the tier the game lives in."

## 5. The clock and the alert state

### 5.1 The night clock (one page, in `09`, replacing nothing; the program table gains a column)

The Uninvited's own timeline, with **indented conditional lines that are the mission menu** (the 3.5 pattern):

| Bell | The Uninvited | The Bought | What the players can move |
|---|---|---|---|
| Dusk (Mv I) | not yet arrived | sixteen blades in matched coats drift into the trade district; the sergeants carry contract cases | — |
| Mv III crush | three gray masks arrive with the thickest crowd | — | *Undercurrent D bottomed before midnight: the party enters the Longest Night armed and positioned* |
| Quarter-bells (Mv V) | the Wept at the east doors, the Radiant in the Dance, the Hollow by an exit | fires set in two sect districts; a courier post goes dark; the company walks to the gatehouse | *Any Fracture tell witnessed: that Fracture invokes at Hard; two, at Standard* |
| Midnight | the lights die mid-sentence | the gate closes from outside: nobody in, nobody out | *The Wept's Fracture found before the dais: ⟨They save Raunu⟩ is possible* · *Every witness on the Radiant: one hallway for Veier* · *The Hollow's Fracture: the doors open, two hundred hostages stop being hostages* |
| The Crossing | the Radiant breaks past Vell once | the captain reads the Second Clause when the first guests reach the gate | *Guilt on the Radiant: it does not break past* · *The gate open, or the contract void: the crowd gets out, the sect guard gets in* |
| Last bell | the leash takes all three | the contract expires; the company withdraws in order | *Ring it when the table needs the end* |

### 5.2 The palace on alert (one paragraph above the keyed rooms in `04`)

Written once: what the honor guard does when steel is bared (four inside two exchanges; detain-and-expel; the gatehouse cell); when the east wing is forced (doubled at the doors, Corval informed, the offender's invitation void); when the lights die (the nine to the dais, the corridor wards fire, the service passages become the only unwarded route); what the Bought do at each bell (§5.1). Room entries then say *if alerted* and stop.

## 6. The gate at midnight *(the new scene; ruled in)*

### 6.1 The contract

Two nights ago a factor no one can describe hired a company of the Bought — sixteen blades, four sergeants, a captain — paid half in old coin, for three tasks written in a case chained to the captain's belt: **at the quarter-bells, fire in two named sect districts and the Blackwatch courier post; from the first bell of midnight to the last bell of Oraga, hold the Boranis gatehouse, nobody in and nobody out; and the Second Clause.** The captain alone has read it: *if a woman in Thenya wool comes out the front, hold her and send word to the river.* They do not know who paid them or why. They are not cruel. They are exactly as dangerous as their terms.

*(Owner canon note: this makes the "other attacks" mortal work done for the Uninvited's master through an intermediary. The factor's identity stays with "the same answer as everything else tonight" and is never given; Vell knows the company is there and has planned around it, which is why the river gate is the escape and the front never was.)*

*(Owner ruling on the coin: "old coin" is also Vell's signature — Agenda 6, the boat, the carter — and that is **deliberate**. A table that notices will suspect the pale factor of hiring the company. Let them. The aftermath wing is where it comes apart: a bought-out captain, asked, describes a payer who was not tall, not pale, and not soft-spoken, and the coin in the Bought's case is older than Vell's by a dynasty. Write the red herring so that it *can* be untangled, never so that it is confirmed.)*

### 6.2 The scene (Movement VII, keyed B12. The Gatehouse Court, Held)

**Trigger:** the first fleeing guests reach the Gatehouse Court and find the outer gate barred from outside, and a sergeant of the Bought standing on the wrong side of it reading the terms aloud. Read-aloud block written to the perception rule (matched coats, a case held up like a lantern, a voice naming a boundary).

**Recipe:** *Hard for a party strength of 3* — one Named (a sergeant, Resolve 3, light armor, *Hold the Terms*) and four Mooks (blades, light armor) at the gate; the captain (Boss, Resolve 6, heavy, *The Second Clause*, *Reform the Line*, phase at Resolve 3) arrives on the clock's third segment or when the sergeant falls, whichever is first. The other three sergeants and twelve blades hold the outer perimeter and are *off the card*; they matter only to the alert state ("if the party goes over the wall, they meet four more").

**The clock:** a four-segment **fire clock**, advancing on every partial and failure near the gate and once per exchange the gate stays shut (the uncontested-exchange rule in the enemy's favour). Full: the gallery fire reaches the Crystal Court's doors, and every exchange after costs the crowd (the MM narrates who did not get out; a Spark per person carried out still applies).

**Objective (stated on the card):** *open the way out.* Three ways it ends, all written as paired conditionals:

1. **Fight through.** Break the sergeant and two blades and the rest disengage in order (morale as written); the captain, arriving, spends an exchange placing blades and *watching who the party protects* (his first-target line), then invokes the Second Clause the exchange after the party looks like winning — and the objective changes: the company stops holding the gate and starts looking for a woman in Thenya wool. The party has just been told something. At Resolve 3 the captain starts negotiating mid-exchange (the phase; attacks continue).
2. **Void the contract.** Proof the employer has broken terms (the fires were not to spread; the palace is burning), or the named target already gone (Veier is out the river gate — a party that knows it can *say* it), or a better-paying offer made in front of the sergeants (a Circle magnate, a Draunel, a Boranis cousin all have coin and reasons). The sergeant surrenders the field the moment the contract is void and says so out loud. This is the Persuade-ends-the-fight route III.3 promises and the module's best social-into-combat beat.
3. **The sect guard.** On the clock's last segment word arrives that the districts' guards are at the outer wall; the captain calls the withdrawal at the first sight of a sect banner if the party has held even one exchange. A party that only *holds* has still won.

**Tactics on the card:** sergeant opens by naming the terms; blades fight to detain; nobody in the Bought goes Aggressive; captain never does. Morale lines verbatim from the Bestiary files.

**Sparks printed:** ending it without a death (one each); a voided contract (one to whoever voided it); every person carried out (as the Overture already says).

**Development:** a captured sergeant, contract case and all, is the inquest's best evidence and the only mortal thread that leads east (§6.5). A bought-out captain honours the deal absolutely and *will not resume the fight tonight for any inducement*, which a clever table can turn into sixteen blades holding the gate *open*.

### 6.3 Why this is the Hard fight

It has every lever the system owns and the audit found missing from the module: a Named enemy who states a stance and uses a Technique in the first exchange; a Boss whose phase the party will see because it lands at Resolve 3 of 6, not 2 of 10; an objective that is not a body count; a clock both sides feed; a negotiation surface; morale that ends the fight before the last Mook; and three endings the table chooses between. Simulate it (§11) before the Resolve numbers print.

### 6.4 ⟨If History Breaks⟩ — the Bought change sides

A table that buys the captain out *before* midnight (possible: the company is visible in the trade district at dusk for a Phern with the Warning gift, and a Draunel or Circle patron could be talked into fronting the fee) holds the gate open from the first scream. Two hundred guests get out in minutes; the sect guard is inside before the Crossing; the Radiant's hunt is *watched* by forty blades who do not understand what they are seeing. Canon still holds (the Radiant is faster than doors; Raunu still dies on his own choice), but the aftermath is a very different morning, and the module says so.

### 6.5 The aftermath thread

The aftermath wing gains: the inquest's interest in the company (a captured sergeant is dawn's favourite scapegoat, alongside Tavva); the old coin the Bought were paid in, which matches nothing minted in Val'loh; and the captain, if bought out, as a patron who genuinely wants to know who hired him, because the Bought's only asset is their reputation and someone has just used it to burn a city.

## 7. Scene cards (`09_Scene_Cards.md`; one page each, fixed field order)

**Card anatomy** (the Stage-3 encounter format): ID and title → *Use with* pointer (room key, Movement) → recipe line with the difficulty band and the audit's honest note if the band is a guess → trigger read-aloud (2–6 sentences, perception only) → objective and clock → enemies (stat lines: tier · Resolve · attack · armor · stance triggers · Techniques · TR) → tactics with an opening move, priority target, and a morale line each → terrain-as-rules lines (two or three: "the lowered lamps: Stealth Easy, Insight Hard"; "the gallery rail: Cornered is the Condition to reach for") → outs (surrender, the passages, a name dropped) → Sparks printed → Development (what changes in the rooms the party can reach next, and only those).

| ID | Fight | Movement | Recipe | Teaches |
|---|---|---|---|---|
| **S1** | The Seating Feud | II–IV, B3 | Skirmish: 4–6 Mooks (kinsmen, no armor, Tier 1 bruising); bare steel voids it and summons guards | postures, Tier 1 clearing per exchange, Absorb as a choice; the four-segment *bench* clock (full = guards fill the galleries for a Movement, one agenda door closes) |
| **S2** | Knives in the Dark | V, service corridors | Standard: Tavva (Named, Vanisher, stance triggers) + 2–3 gallery knives | a stated stance and a Technique; Press; Sparks; morale; the shared *noise* clock (any 6−, any bare steel; full = guards, both sides lose) |
| **S3** | The Gate at Midnight | VII, B12 | Hard: 1 Named + 4 Mooks; Boss on the third segment | Intercept, a Boss phase, negotiation ending a fight |
| S4 (half) | The East Wing Doors | V, B9 | honor guard detain-and-expel, 2–3 exchanges | outs visible; losing costs the evening, not the character |
| S5 (half) | The Looters | VII, B7/B3 | Tavva + knives, fights to leave | a branch of S3's night, not a set piece |

Pointer lines both ways: the room text says *"Scene card S2, page —"*; the card's Development says *"return to Movement V, B10."*

## 8. Characters

### 8.1 Making characters (`03`, rewritten)

Build by the core's seven steps with the Val'loh Facet loaded. Lineage: **Orthaen** (gifted or ungifted, the player's choice; four in five are gifted) or, rarely and with MM agreement, **Phern**. Backgrounds as core; a gifted character takes a non-magical Background (one domain at creation). Every character carries an invitation story (a hook) and an agenda. The section is one page; it must not restate the Facet.

### 8.2 The five pregens, rebuilt (through Lineage; `.fof` files shipped)

| Pregen | Lineage / gift | Facet | Background (core or custom) | Endurance | Notes |
|---|---|---|---|---|---|
| Serane Vaskarin | Orthaen, **Crystal** | Soul | custom: Minor Scion (Persuade Practiced; Deceive replaced by the gift) | 3 | the module's example caster: her Minor-scope intents appear in `04`'s summons scene |
| Pello | Phern, **Warning** | Body | custom: Factor's Nephew (Finesse Practiced) | **4** | Constitution 2; the gift's Minor intents appear in Movement II's omen |
| Andra Tessarin | Orthaen, Crystal | Mind | Guild Apprentice, non-magical variant (Lore Practiced, Craft secondary replaced by the gift) | 3 | |
| Dassa | Orthaen, **ungifted** | Body | City Watch Veteran reskinned (Combat Practiced, Endurance Novice + mark) | **5** | Heritage in play: reads crystalwork despite no gift |
| Ilesse Kethaun | Orthaen, Crystal | Soul | custom: Border Cousin (Persuade Practiced) | 3 | carries Agenda 4 |

Each sheet also prints **"At Facet level 1 you would likely take:"** with one Technique named (Serane: *Read the Room*; Pello: *Fleet Step*; Andra: *Sharp Analysis*; Dassa: *Weapon Mastery — blades*; Ilesse: *Lasting Impression*), so a first-night table sees the road ahead. A gifted pregen's gift formalizes at that same level, free.

### 8.3 Advancement happens

The one-shot ends with the standard 4 skill points and a reflection scene at the epilogue question. The aftermath wing, run as written for two sessions, lands Facet level 1 under D16a's floor; `06` says so and places the reflection scene at the inquest ("your threshold is met — take it on the dais, where the pen is not yours"). This is the single largest change to what the module *proves* about the system: a character who plays it through has grown.

## 9. NPC apparatus (`07`)

Three Q&A dialogue blocks (italic anticipated question, quoted in-voice answer, "if friendly" tier), six to ten exchanges each: **Corval at the gate** (what the line asks him; what he says about the staff, the master, the masks — the three grey masks make his answer slide), **Vorlain by the wine** (Agenda 3's overtures; his sober non-answers; the one drunk line already written), **Raunu's summons** (the questions the module already scripts, in this format). Answers are the writer's, under canon, using lines already in the module wherever they exist; new lines are flagged for the owner like every other invention.

The Bought's sergeant and captain get cast entries in the same format as Tavva's, with the negotiation surface printed (what they want, what shifts them, what deal they honour) — lifted from the Bestiary files and reskinned.

## 10. Troubleshooting sidebars and the abridged run

Four sidebars, each naming the derailment and giving two in-fiction answers:

- **The table will not stop hitting the Wept.** (Exists in spirit in "You Cannot Beat Them"; make it a sidebar: force buys hallways, and here is how to make the purchase visible.)
- **The MM keeps defaulting to Hard.** The line's first roll is Standard; the module's difficulty calls are printed on every scene card and cast entry; a masked approach is *Easy*.
- **A 7–9 is not a penalty.** The MM2 social table is reprinted on the night-tracker; the module's own examples name the cost before the success.
- **Someone asked whose turn it is.** No turn order; the card's exchange flow; the app's declare-then-reveal.

**Abridged run** (four hours): cut Undercurrent A (the Root) and the east-wing scene; run S1 or S2, not both; the gate as written.

## 11. Simulation and tests

- **Sequence:** the audit's R2 and R3 are **settled** (D20, `research/simulation_log.md` Series 12). Tune S2 and S3 against these rules, and only these:
  - Open expires at the end of the exchange, and an Open enemy still acts.
  - A 10+ Strike depletes 2 Resolve and chooses **Open** or **Position**. There is no Cover; it was cut at the gate.
  - Expect fights to run slightly longer and slightly harder than the pre-R2 corpus: the Hard recipe row now sits at 38.0–45.0% rather than 47.5%.
  - The gate Boss `bought_captain` was swept and needed no change; its Resolve-3 negotiation phase is unaffected by R2.
- **Simulate S3** with `tools/combat_sim.py` driving `app/game/combat.py`: PS-3 party, 1 Named (Resolve 3) + 4 Mooks, Boss (Resolve 6, phase at 3) entering on exchange 3. Acceptance: party win rate in the Hard band (40–60%) counting *any* of the three endings as a win; the phase fires in exchange 2 of the captain's presence in ≥70% of runs; median fight length 3–4 exchanges. Tune the captain's Resolve and entry exchange, not the recipe.
- **Simulate S2** as Standard (65–85%).
- **S1** needs no sim; it is Tier 1 only.
- **Docs:** extend `build_bestiary.py` (or a sibling `build_scene_cards.py`) to generate the stat lines on the scene cards from the module's `enemies/*.fof` into `<!-- statblock: id -->` markers, so the cards and the files cannot disagree; add a no-diff invariant. Extend INV-5's `Chapter X.Y` resolution to `adventures/` so the module's PHB pointers resolve. Keep read-aloud blocks under 120 words by test (a simple word count on italic blocks with a trigger line).
- **Style:** run the humanizer pass and the style guide's amateur-tells list over every new block; the recurring cast does not appear (this is a module, not the PHB), but the read-aloud rules do.

## 12. Order of work

1. Data first: module-local Bought reskins; pregens as `.fof` through Lineage.
2. S3 and S2 simulated; Resolve numbers fixed.
3. `01` rebuilt (battery, hooks, legend); `06` prelude deleted; `08` deleted; `02`/`03` trimmed and repointed.
4. `04`: B0, alert state, pointer lines, Q&A; `05`: the gate scene and its branch; `09`: the clock column.
5. `09_Scene_Cards.md` with generated stat lines; invariants.
6. Troubleshooting sidebars, designer's notes, abridged box.
7. `INVENTIONS_FOR_REVIEW.md` in `references/oraga_night/` gains a Revision 4 table listing every new invention here (the Bought's contract, the factor, the old coin, the six hooks' details, B0's line scenes, every Q&A line) for the owner's read.

## 13. Watch-outs

- **Nothing new in the read-aloud names a creature or resolves an action.** The existing blocks are good; keep the discipline on B0 and B12.
- **The Bought never learn who hired them, and the module never says.** The factor is "the same answer as everything else tonight." Any draft that gives him a face or a name breaks the spoiler boundary.
- **The Second Clause must never succeed.** Veier leaves by the river; the front is a decoy the party can discover. If a table somehow brings her to the front, the captain's honour clause and the sect guard's arrival are the outs; write that branch.
- **Do not lengthen the one-shot.** Every addition is a card the MM can skip; the abridged box protects the promise.
- **Agendas, omens, undercurrents, Fractures, the Crossing, the epilogue are untouched.** Any task that edits their prose beyond a pointer line is out of scope and should be sent back.
