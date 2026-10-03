# RESEARCH — 5e Module Conventions: Prose Voice and Mechanics Phrasing (the yardstick)

*2026-09-30. Yardstick for the official-style audit of the 5e edition of Oraga Night
(`conversions/dnd5e/oraga_night/`). This file does **not** audit our module. It records how
official 5e adventures (2014–2016 era) sound and how they phrase mechanics, so an auditor
can measure against them. The companion file for layout and structure is
`docs/RESEARCH_5e_module_conventions_structure.md`. For the evidence set and the copyright
posture, see `docs/RESEARCH_5e_reference_catalog.md`.*

*Copyright: this file records conventions only. It reproduces no narrative sentences, read-aloud,
NPC names or lore. Stock rules grammar that also appears in the SRD is quoted verbatim
(CC BY 4.0). Every other example is invented and generic. Examples marked "e.g." are ours.*

**Status:** complete.

---

## 0. Method and evidence base

- **Sources.** Hardcovers: LMoP, HotDQ, RoT, PotA, OotA, CoS and SKT. Short adventures:
  CoS Intro (Death House), DDEX1-1, DDEX2-01, DDEX3-01, DDEX3-06, DDAL04-01/04/05/12/14 and
  DDEP1. Rules: DMG, Basic Rules DM and SRD. The SRD extract in the scratchpad is the
  OGL **SRD 5.0/5.1**, *not* 5.2.1. Every SRD 5.2.1 point in §12 comes from knowledge of
  that document, not from a local extract, and is flagged **[verify 5.2.1]**. Red Hand of Doom
  (3.5) was consulted only to contrast with the house style guide.
- **Pages** are extract page numbers (the PDF page index). They run close to the printed folios
  but do not always match them.
- **Counts** are `grep -o` over the 18 adventure extracts joined and de-wrapped. That corpus
  is `adv_all`: about 1.13 M words and about 55,900 sentences. OCR noise and line wraps lose
  some hits, so every count is a lower bound. The ratios are what matter.
- **Rhythm metrics** come from a small script. It joins lines, strips soft hyphens, drops
  headings and bullets, and drops sentences that open with "You" (a read-aloud proxy).
  LMoP and OotA extractions break mid-sentence, so their paragraph figures are discarded.
- **Typography** (italic and bold) was checked from PDF font spans with PyMuPDF on Death House
  pp. 2–12 and SKT pp. 20–40, because plain-text extracts lose it.
- **Weighting.** Our module is a single-night social intrigue with fights for 4–5
  3rd-level PCs. So the heaviest weight goes to the CoS social set-pieces (Vallaki pp. 96–97
  and 123–125, the dining hall pp. 57–58), the RoT council chapter (pp. 19–22), LMoP
  Phandalin (pp. 14–30), Death House, and the session-length AL adventures.

---

# A. PROSE VOICE

## 1. Address, reference to the party, tense

**Who "you" is.** Outside read-aloud, "you" is **always the DM**. The corpus has 551 "you can",
165 "you have", 55 "you might", 42 "you need", 39 "you may", 36 "you want", 35 "you choose",
32 "you must" and 26 "you should" (some "you can" hits are read-aloud). DM address takes
three forms:
- **Imperative instructions**, the most common. Sentence-initial imperatives in the corpus:
  *See* 160, *Roll* 117, *Give* 81, *Use* 76, *Read* 38, *Make* 26, *Adjust* 16,
  *Choose* 14, *Treat* 13, *Award* 10. An invented example: "Roll a d6 to determine which
  guest arrives next."
- **Permission and option grants**: "you can [delay/advance] X if …" (CoS p. 124). RoT p. 19
  offers an optional shortcut scenario the DM can use in place of a long journey.
- **Conditional DM context**: "If you played [the previous book] …" (RoT p. 19).

Read-aloud is the only place where "you" means the players' characters. No official text
addresses the players in DM-facing prose.

**How the PCs are named.** "The characters" is overwhelmingly the default in every book:

| Book | "the characters" | "the party" | "the adventurers" | "a character" | "the heroes" | "PCs" |
|---|---|---|---|---|---|---|
| LMoP | 235 | 101 | 23 | 39 | 0 | 0 |
| CoS | 603 | 44 | 15 | 89 | 2 | 0 |
| RoT | 392 | 96 | 139 | 51 | 28 | ~0 |
| SKT | 716 | 98 | 49 | 59 | 3 | 0 |
| OotA | 856 | 261 | 168 | 57 | 12 | ~0 |
| Death House | 31 | 2 | 2 | 14 | 0 | 0 |
| DDAL04-01 | 123 | 13 | 4 | 18 | 0 | 0 |
| DDEX2-01 | 142 | 17 | 50 | 16 | 0 | 0 |

- **"The characters"** is the default subject. **"The party"** is a stylistic variant, used
  mostly for group-level attitudes and possessives ("toward the party"). **"The adventurers"**
  is a variant in RoT, OotA and DDEX2-01, and it clusters in faction and social contexts
  (RoT council). Some books use "the heroes" (RoT, OotA).
- **"PCs" is effectively absent** from all official DM prose (the RoT hits are OCR splits of
  "NPCs"). "NPC" and "NPCs" are used freely.
- **"The players"** appears only when the text means the real people at the table (table
  management, handouts, reminding the players to record rewards). It never means the characters.
- **Singular individuals** are named by a relative clause: "a character who …" or
  "any character who …". To name a leader, the text uses "the character with the highest
  [ability/passive score]" (DDAL04-05 p. 10).
- **The DM role** is "you". Books name it "the DM" or "the Dungeon Master" only in
  organized-play admin text (DDEP1 has 40 "the DM"; hardcovers have 0–4). **Project
  deviation:** our module uses **MM (Mirror Master)** by house rule (BRIEF_oraga_5e §2). That
  is a deliberate difference, not a smell. The official *grammar* still applies: "you" in
  instructions, and the role name only where a third-person reference is unavoidable.

**Tense.** DM prose is in the **present tense** for the situation, for what NPCs do and for
what happens on a trigger (for example, "If the characters challenge X, X orders…", CoS
p. 124). The **past tense** is kept for backstory blocks. The **future** ("will") is rare and
appears mostly as an NPC's intent or inside a read-aloud promise. Conditional consequences
use the simple present, not "will" (an invented example: "If the characters refuse, the steward
calls the guards", not "…will call the guards").

## 2. Sentence and paragraph rhythm; register

**Sentence length (DM-facing prose).** The table shows two methods. The per-paragraph method
is a lower bound because fragmentation shortens it. The joined-blob method is an upper bound
because table fragments inflate it.

| Sample | words/sentence (paragraph method) mean / median | words/sentence (joined) mean / median | p90 | share > 30 words |
|---|---|---|---|---|
| LMoP pp. 14–30 (Phandalin) | 16.4 / 15 | 18.8 / 17 | 31 | 10% |
| CoS pp. 96–110 (Vallaki) | 16.7 / 15 | 18.6 / 17 | 31 | 11% |
| CoS pp. 40–60 (village, castle) | 16.7 / 15 | — | 28 | — |
| RoT pp. 19–30 (council) | 20.3 / 19 | 22.7 / 21 | 36 | 19% |
| HotDQ pp. 10–25 | 17.1 / 16 | 19.1 / 17 | 32 | 12% |
| Death House (CoS Intro) | 16.0 / 14 | 17.8 / 16 | 30 | 9% |
| DDAL04-01 | 15.3 / 13 | 17.8 / 15 | 31 | 10% |
| DDAL04-14 | 15.7 / 13 | — | 29 | — |
| DDEX1-1 | 17.2 / 15 | 19.7 / 17 | 34 | 14% |
| DDEX2-01 | 15.7 / 14 | — | 28 | — |
| SKT pp. 20–40 | 16.3 / 15 | 18.6 / 17 | 30 | 9% |
| OotA pp. 20–40 | 20.1 / 17 | 23.8 / 21 | 43 | 24% |

**Norm:** DM-facing prose averages **about 16–19 words per sentence (median 15–17)**. About
**one sentence in ten runs past 30 words**. The 10th percentile is about 7–8 words, so short
sentences of 5–8 words are routine. The faction and politics chapters (RoT council, OotA)
run longer, at about 20–23 words. A passage whose mean sits well above 22, or which has
no sentences under 10 words, reads un-official.

**Paragraph length.** These figures come from books with reliable extraction.

| Sample | sentences/paragraph mean (median) | words/paragraph mean (median) |
|---|---|---|
| CoS Vallaki | 4.0 (3) | 68 (54) |
| CoS village/castle | 4.0 (3) | 68 (50) |
| Death House | 4.7 (4) | 75 (64) |
| SKT pp. 20–40 | 4.0 (3.5) | 66 (54) |
| DDAL04-01 | 4.3 (3) | 66 (43) |
| DDAL04-14 | 4.5 (4) | 71 (50) |
| DDEX2-01 | 4.2 (3) | 67 (45) |
| DDEX1-1 | 4.5 (3) | 77 (59) |
| RoT council / PotA / HotDQ | 5.6–7.3 (4.5–5) | 108–125 (78–88) — paragraph breaks partly lost in extraction; read at RoT p. 20, real paragraphs run ~4–6 sentences |

**Norm:** **3–5 sentences and about 45–75 words** per paragraph. One-sentence paragraphs are
common and do real work: a flat ruling (an invented example: "The mirrors are ordinary."), a treasure line, or a
pointer to another section. Paragraphs over about 120 words are rare outside
background and history blocks.

**Register.** The register is **plain, confident and lightly flavored**. The traits are:
- Declarative statements of fact, including invented facts about the fiction, asserted like an
  encyclopedia ("X is Y's spy"). There is no "it seems" or "perhaps" about canon.
- Flavor lives in *nouns and verbs*, not adverbs or rhetorical flourish. For example, a room
  is described by what hangs on its walls (an invented example: "hung with faded banners")
  rather than as "evocatively appointed". Metaphor in
  DM prose is rare. It belongs to the read-aloud.
- **Instruction versus flavor.** In area and scene entries, DM prose is roughly two-thirds
  *what is here and what happens* (instruction, trigger, consequence) and one-third
  *what it is like / why* (motive, history). Mood is delegated to the read-aloud box. DM
  prose then states function flatly. The CoS dining hall (pp. 57–58) is a model: an evocative
  box, then flat function (what the figure is, how many rounds it lasts, what ends it, which
  DC finds the hidden thing), then a one-line anticlimax that tells the DM the food is safe.
- **Contractions are normal.** The rate per 10k words is 99–124 in the hardcovers and 54–91
  in the AL adventures, which are more formal. "Doesn't", "can't" and "isn't" appear in
  rules-adjacent prose too (CoS p. 58 uses "can't" in a secret-door rule).

## 3. Uncertainty, DM choice and branching

**The conditional is the backbone.** About **1 sentence in 17 starts with "If"** (3,201 of about
55,900). Other sentence-initial connectives, in order: *When* 750, *As* 487, *Once* 305,
*However* 278, *While* 271, *After* 230, *Although* 146, ***Otherwise* 141**, *Unless* 91,
*Whenever* 30.

The grammar of branching:
1. **"If the characters + verb …, [NPC/world] + present-tense verb …."** The subject is the
   characters' observable action: *are* 96, *have* 41, *ask* 38, *approach* 34, *take* 25,
   *don't* 22, *enter* 19, *defeat* 19, *attack* 19, *leave* 17, *agree* 15, *refuse* 13. The
   trigger is **something a player can do**, not an internal state.
2. The paired fallback uses **"Otherwise, …"** (141) far more than "If not, …" (under 20 in
   the whole corpus). "Unless the characters intervene, …" states a default outcome that
   the party can interrupt (CoS p. 124).
3. **Chained Development consequences.** A short "Development" block gives 2–4 stacked
   "If …" sentences, each a one-step consequence (CoS pp. 124–125). They are not nested
   inside one sentence.
4. **Time and trigger clauses** set the moment: "The first time the characters enter…",
   "When the characters arrive…", "Once [event], …".

**DM discretion is delegated by name, with a default.** The typical forms are:
- **"You can [delay/advance/adjust] X if …"**: a permission plus a condition (CoS p. 124:
  delay the festival if the party is waylaid, advance it if they hurry).
- **"If events unfold differently in your campaign, adjust … accordingly"** (RoT p. 20).
- **"at your discretion"** is rare: 0–6 per book, and about 1 per AL module.
  **"up to you"** and **"you decide"** each appear under 1 per 10k words. Official modules
  make the call and then offer the dial. They do not hand the decision over blank.
- **"Feel free to …"** is an **AL-specific** tic: 4–8 per AL module, 0–5 per hardcover.
  It appears in AL boilerplate and adjustment notes.
- **Options are scoped.** Two or three concrete defaults come first, then "or any other … of
  your choice" (RoT p. 19). An invented example: "The meeting can take place in the chapel, the
  library, or any other room of your choice."

**Uncertainty inside the fiction** uses *might* (LMoP 16 per 10k words, RoT 15, CoS 3.7,
SKT 7.4, AL 8–12). The subject is nearly always the characters or an NPC: "the characters
might" (134), "they might" (102), "it/he/she might". It predicts what players may do or
what an NPC may say. It is **not** a hedge on the rules. *Perhaps*, *possibly* and
*probably* each run at 0–2 per 10k words.

## 4. NPC motivation, secrets and "what they know"

These are the patterns that recur across CoS, RoT, LMoP, Death House and AL:

- **Motive as a plain present-tense verb.** The verbs are *wants* (434), *believes* (228),
  *fears* (164), *hopes* (153), *knows that* (156), *hates* (59) and *suspects* (30). An invented
  example: "The steward wants the ball to end before the lamps run out. He fears the
  host more than any guest." There is **no labeled "Motivation:" field** in any hardcover
  (0 hits).
- **Secrets are stated flatly to the DM, in the same paragraph as the surface.** The shape is
  "Although they appear to be X, they are actually Y" (Death House p. 3). Other forms are
  "What X doesn't know is that …" (LMoP p. 16) and "X secretly …". Counts: *is actually* 61,
  *doesn't know* 113, *secretly* 23, *in truth* 19, *is unaware* 16. The secret is **never
  withheld from the DM** and never hinted at coyly.
- **"What they know" is a bulleted fact list** introduced by a trigger sentence. The shape is
  "Characters who question [X] learn the following information:" followed by bullets
  (Death House p. 3; *the following information* has 32 hits and *learn(s) the following*
  has 10). Each bullet is one fact in the NPC's framing. **Truth status is annotated in a
  trailing parenthetical** when the NPC is wrong, for example "(Untrue, but the speaker
  believes it.)". Such status parentheticals occur 8 times. Town-lore lists work the same way
  (CoS p. 96: a lead-in saying that, beyond the general lore, the locals know the following, then
  bullets).
- **Information gated by action.** "If the characters ask [X] about Y, [X] tells them …"
  (41 hits for *If the characters/they ask*, 24 for *If asked*). "When pressed, …" and
  "If pressed" reveal the next layer (CoS p. 125).
- **Faction positions as reactions.** RoT (pp. 21–22) states each faction's attitude to
  each possible outcome in turn: "Most delegates respect X. However, faction A would have
  preferred Y; B would have Z; C is firmly against." The text is compact and declarative,
  with one sentence or clause per faction, and it names what shifts each one.
- **Roleplaying blocks.** AL adventures use a boxed **"Roleplaying [Name]"** sidebar
  (DDAL04-05 p. 10, DDEX2-01 p. 8, 45 hits corpus-wide). It holds 2–5 sentences of
  appearance, manner and inner tension, then a one-line **"Quote:"** in the NPC's voice (18
  hits). SKT's appendix NPCs (p. 248) use **"Roleplaying Information"** under the stat block:
  one or two sentences, then **Ideal / Bond / Flaw** as first-person quoted lines (22 each).
  Hardcover body text integrates the same content into prose instead.
- **Social resolution is tiered and fails forward.** DDEX2-01 (p. 8) gives each approach its
  own DC. Intimidation is DC 5 and yields the full story. Deception or Persuasion is DC 15 and
  yields a partial story. **Failure still yields the minimum lead** needed to continue. Each
  tier is labeled with its success grade, and the scene tracks *how much* and *how fast* the
  party learns.
- **Knowledge limits are explicit.** "X is unaware of what the others have done"
  (DDAL04-01 p. 12). The DM is told where each NPC's knowledge ends, so the DM never has
  to improvise past it.

## 5. Signature habits and what official text avoids

**Habits (do):**
- A flat, declarative ruling immediately after the evocative box: what something is,
  whether it's dangerous, how long it lasts.
- **Deadpan one-line anticlimaxes** that settle a player worry the DM will face. The dining
  hall's food is safe (CoS p. 58), and the watching statues are harmless (CoS p. 58). This is
  the main outlet for humor in DM prose. It is dry, informational, and roughly one beat per
  several pages.
- **Pointer sentences**, "(see area N4)" or "(see chapter 11, "Title")", appear mid-sentence
  in parentheses rather than as standalone "See also" lines.
- **Parenthetical asides for DM-only clarifications.** Examples are a truth status, a stat
  reference, "(but do not lock)" and "(in that order)".
- **Numbers are written as numerals when they are game quantities** ("3 rounds", "2 feet",
  "24 hours"). Small counts of things are spelled out in prose ("two more stirges", "six
  town guards").

**Avoided (don't), with measured rates:**
- **Rhetorical questions in DM prose.** "?" runs at 1–5.5 per 10k words, and nearly all
  of those are in NPC dialogue or read-aloud. DM prose makes statements.
- **Addressing the players as "you"** in DM text (0 cases found outside read-aloud and AL
  story-award text).
- **Designer "we".** 0.3–2.4 per 10k, almost entirely in credits, forewords and AL
  boilerplate. There is no "we recommend" in body text (3 hits corpus-wide, all AL front
  matter). No book has a "Designer's Note" box (0 hits).
- **Meta-commentary and throat-clearing.** "It's important to note" has 0–1 hits.
  "Note that" has 0–1 per 10k. "Keep in mind" (25) and "Remember that" (15) occur, but only as
  single reminders of a specific rule or state, never as openers.
- **Hedging the rules.** *Perhaps* ≤ 1.9 per 10k (the DMG) and ≤ 1 in adventures. A DC is
  never given as a range ("DC 12–15"); every check has one DC.
- **Jokes at the players' or game's expense**, fourth-wall winks and exclamation marks in DM
  prose. "!" appears only in dialogue and AL story text.
- **"PCs".**
- **Explaining a core rule**. The text points instead ("see 'Social Interaction' in chapter 8 of
  the Dungeon Master's Guide", OotA p. 97).
- **Blank-cheque discretion** ("do whatever feels right"). Discretion always comes with a
  default.

**The AL register differs from hardcovers** in four ways. AL prose uses fewer contractions.
It has more "feel free", more "might" in advice, and a fixed boilerplate front section
("Adjusting the Adventure", "Running the Adventure"). It also carries more
table-management talk ("the players"). For a session-length module, the AL register is an
acceptable model **only for adjustment sidebars and reward sections**. For scene prose, the
hardcover register (CoS, LMoP) is the better target.

---

# B. MECHANICS PHRASING (the SRD grammar)

## 6. Ability checks

**The canonical template** (683 hits, the dominant form):

> **DC** *N* **Ability (Skill) check** — e.g. "a DC 15 Wisdom (Perception) check"

- **The ability is always named with the skill in parentheses.** A bare "DC 15 Perception
  check" occurs **twice in the whole corpus**. A skill-less check names the ability alone:
  "a DC 15 Strength check" (238 hits), used mostly for forcing doors and breaking objects.
- **Two skills that share an ability** go in one parenthesis: "a DC 15 Charisma (Deception or
  Persuasion) check" (DDEX2-01 p. 8). **Alternatives across abilities** are written out:
  "a successful DC 10 Charisma (Intimidation) or DC 15 Charisma (Persuasion) check".
- **DC frequency** in the corpus: DC 15 (505), DC 10 (403), DC 20 (168), DC 13 (141),
  DC 12 (140), DC 11 and DC 14 (63 each), DC 17 (59), DC 16 (32), DC 18 (31), DC 25 (26),
  DC 5 (17). The DMG ladder values 5/10/15/20/25 dominate, with in-between values used for
  tuning.
- **Skill frequency**: Wisdom (Perception) 387, Strength (Athletics) 163, Dexterity (Stealth)
  89, Intelligence (Investigation) 83, Wisdom (Insight) 56, Charisma (Persuasion) 52,
  Intelligence (Arcana) 48, Dexterity (Acrobatics) 38, Wisdom (Survival) 34,
  Intelligence (History) 20, Charisma (Deception) 19, Charisma (Intimidation) 15, and
  Charisma (Performance) 2.
  → Even in the social books, Insight and Persuasion together are under 11% of checks.
  An intrigue module will run well above that mix, which is expected. Keep the template
  identical anyway.

**Sentence frames, by frequency:**

| Frame | Hits | Use |
|---|---|---|
| "[Subject] **must succeed on** a DC N … check/saving throw [to …/or …]" | 248 | mandatory gate or hazard |
| "**With a successful** DC N … check, [a character] notices/can …" | 289 | discovery, sentence-initial |
| "[Subject] **must make** a DC N … check/saving throw" | 118 | followed by separate success/failure sentences |
| "… **requires a successful** DC N … check" | 100 | door, climb, lock |
| "**A successful** DC N … check **reveals/indicates** that …" | 76 | information, Insight especially |
| "[Subject] **can make / can attempt** a DC N … check" | 45 | optional attempt |
| "**A character who succeeds on** a DC N … check [verb] …" | ~30 (incl. "any character who", "characters who") | individual discovery |
| "… **succeeding on** a DC N … check" | 33 | participial variant |
| "… make(s) a DC N check. **On a success**, … / **On a failed check**, …" | ~35 / 18 | two-outcome procedures |

"Succeed **on**" is standard. "Succeed **at**" also appears, mostly in AL, and is
tolerated but secondary.

**How results are stated:**
- **Success-only is the norm for checks.** Only about **11%** of check sentences state a
  failure outcome in the same or next sentence. The failure result is silence: nothing is
  learned and nothing is noticed. By contrast, **80% of save sentences** state the failure
  consequence (in the same frame: "or be…", "taking … on a failed save").
- When failure matters, the text uses the forms "**If the check fails, …**" (18),
  "**On a failed check, …**" (18) or "**Otherwise, …**". For scaled failure it uses
  "**If the check fails by 5 or more, …**" (14 hits for *fails by 5 or more*).
- **The result verb is observational**: *notices*, *spots*, *discerns*, *realizes*, *recalls*,
  *can tell that*, *reveals that* or *indicates that*. The rest of the sentence then gives the
  fact itself, not "gains information".
- **Retry rules are explicit when they matter.** An invented example: "A failed check can't
  be retried against the same guest until an hour has passed" (the pattern is at SKT p. 208).
- **An action cost is stated when relevant**: "… check made as an action", or "A character
  can use an action to attempt …" (SKT p. 208).
- **Advantage is granted by listing conditions** after the check. A lead-in sentence says the
  character gains advantage under the following conditions, and a bold run-in list follows
  (SKT p. 208).

**Group checks** use "a DC 10 **group** Dexterity (Stealth) check" (the word *group* goes
before the ability, DDAL04-01 p. 12, OotA p. 44). There are about 33 hits, 9 of them Stealth.
The rule is never restated. The SRD definition (at least half the group succeeds) is assumed.

**Contests** use the form "a Dexterity (Stealth) check **contested by** the [creature]'s Wisdom
(Perception) check". For the listener it uses "contested by the [creatures'] **passive** Wisdom
(Perception) score" (LMoP; about 6 hits). No DC is given in a contest.

**Passive scores:**
- In prose conditions: "Characters **who have a passive Wisdom (Perception) score of 14 or
  higher** notice …" (CoS p. 125). The full form "passive Wisdom (Perception) score of N or
  higher" has about 45 hits. The short form "passive Perception" (264 hits) appears mostly in
  stat blocks ("Senses … passive Perception 12") and in rough references.
- **Norm for prose:** a threshold phrased as "score of N or higher", with the ability named.

## 7. Saving throws, damage, conditions, advantage and durations

**The save template** is SRD verbatim and appears 128 times in the SRD and 59 in adventures:

> "must make a DC 13 Dexterity saving throw, taking 10 (3d6) fire damage on a failed save,
> or half as much damage on a successful one."

**The save-or-condition template** (SRD, 89 hits):

> "must succeed on a DC 12 Constitution saving throw or be poisoned for 1 hour."

In adventures the forms are "or be paralyzed/frightened for 1 minute" (10) and "or become
[condition] for 1 minute" (5).

**The repeat-save clause** (SRD verbatim, 60 in the SRD and 18 in adventures):
> "The creature can repeat the saving throw at the end of each of its turns, ending the effect
> on itself on a success."

Outcome words: "on a failed save" (111, more common than "on a failed saving throw", 8), and
"on a successful save" (28, more common than "on a successful saving throw", 5). **Use
"save" in the outcome clause and "saving throw" in the demand clause.**

**Damage expressions:**
- **Average first, dice in parentheses, then type:** "takes 7 (2d6) fire damage". This form has
  **567** hits, against **69** for bare dice ("takes 2d6 fire damage"). Bare dice survive
  mostly in older LMoP and HotDQ traps and in spell-like text.
- Verbs: *takes* (64), *taking* (55), *plus* (33, for rider damage), *take* (29), *deals* (17)
  and *extra* (14).
- Damage types are lowercase in 2014 text ("piercing", "fire"; see §12 for 5.2.1).
- Other forms: "regains 7 (2d6) hit points", "drops to 0 hit points" (18), "is reduced to 0 hit
  points" (12) and "hit point maximum" (28).

**Conditions:**
- 2014 style is lowercase and adjectival. The verb forms are "**is** poisoned / restrained /
  grappled / incapacitated", "**be** paralyzed for 1 minute" and "**is knocked prone**"
  (57 hits; "falls prone" has 17).
- The noun form "**the [x] condition**" is rare (about 14 hits in total: frightened, poisoned
  and restrained). It is used when a rule ends or references the condition ("the poisoned
  condition ends").
- **Conditions are never italicized or bolded**. The PDF font check shows them in body text.
- "Frightened **of** [source]" gives the source when it matters.

**Advantage and disadvantage:**
- "has advantage on [checks/saving throws/attack rolls] …" is the stock form (SRD 158; adventure
  corpus: *advantage on* 371, *has advantage* 168, *with advantage* 51, *have advantage* 37).
- "makes the check with advantage" is used for a single roll. "gains advantage" (7) is rare.
  "grants advantage" (11) is used for items and allies.
- Advantage is always attached to a named roll type ("on Wisdom (Perception) checks that
  rely on sight"), never floating ("has advantage in this scene").
- **Inspiration** (50 hits) is awarded by name ("the character gains inspiration"). In 2014
  it is always lowercase.

**Durations**, by frequency: "for 1 minute" (62), "for 1 hour" (36), "for 24 hours" (31),
"for 10 minutes" (15), "until the start of its next turn" (10), "for 1 round" (9) and
"until the end of its next turn" (7). **Numerals and singular units** are used ("1 minute",
not "one minute"). Rest-keyed durations take the form "until it finishes a long rest".

**Areas** use the forms "within 30 feet of" (303 hits), "each creature in a 20-foot-radius
sphere" and "a 15-foot cone". Distances in feet are numerals. "Each creature in …" and
"any creature that …" are the subject forms. "Each creature that …" does not occur in this
corpus.

## 8. Attacks, spells, magic items and cross-references

**Attack lines** (stat blocks, and traps given as creatures) use the 2014 template verbatim:
> "*Melee Weapon Attack:* +4 to hit, reach 5 ft., one target. *Hit:* 5 (1d6 + 2) slashing
> damage."

Counts: melee 274, ranged 100, "Melee or Ranged Weapon Attack" 48, spell attacks 13.
"+N to hit" appears 557 times. In prose a trap or NPC attack uses the form "makes a ranged
weapon attack against one character: +5 to hit". Prose rarely says "attacks with a bonus
of…".

**Spells and magic items are italic and lowercase** in 2014 books. This was confirmed from
PDF fonts: Death House italicizes *bless*, *spiritual weapon*, *mage armor*, *cloak of
protection*, *potions of healing* and *wand of polymorph*, and SKT italicizes *levitate*,
*revivify*, *potion of invulnerability* and *staff of the magi*. Book titles are italic
too (*Monster Manual*, *Player's Handbook*). The plural goes on the item noun: "two
*potions of healing*" (the corpus has "a potion of healing" 19, "two/three potions of
healing" 7). Scrolls are written as "*spell scroll* of *X*" in later books and
"*scroll of X*" in LMoP.

**Creature names in bold.** When a creature that has a stat block first appears in an
encounter, its stat-block name is **bold** and lowercase: "four **ghouls**", "a **mimic**",
"two **goblins**" (PDF check, Death House and SKT). Named NPCs get a parenthetical tag
**(alignment sex race stat-block)**, for example "(CG male halfling **commoner**)", with the
stat-block name bolded inside it. There are 129 such tags. The common shapes are 4 words
(63) and 5 words (43). Groups take the form "(N male and female human **guards**)".

**Cross-references:**
- To appendices: "**(see appendix B)**" (about 250 hits across appendices A–E). It is
  parenthetical, lowercase "appendix", and uppercase letter.
- To the MM: "uses the **[creature]** statistics / stat block **in the Monster Manual**" (40)
  and "(see the Monster Manual)". To reuse a stat block: "use the **scout** statistics"
  or "uses the **troll** stat block" (the two forms are about equal).
- Modifications use the form "…statistics, with the following changes:" followed by a bulleted
  list (a handful in HotDQ, RoT and CoS).
- To the rulebooks: "chapter 7 of the Dungeon Master's Guide" (53) and '"Sample Traps" in
  chapter 5, "Adventure Environments," of the Dungeon Master's Guide' (CoS p. 124). The
  shape is section in quotes, then chapter number and title, then the book in italics.
  LMoP says "the rulebook" (36).
- Internal references: "(see area N4)", '(see chapter 2, "Title")' and '(see the "Endings"
  section)'. Sections are named in quotes.

## 9. Rest, time, light, travel and exhaustion; social rules

- **Rests**: the verb is "finishes a long rest" (14) or "finish a long rest" (10), and
  "take(s) a short rest" (9). The nouns are lowercase: "long rest" (92) and "short rest" (27).
  Stock phrasing includes "after finishing a short or long rest". DDEX2-01 states up front
  that the characters are assumed to take a long rest between sessions.
- **Time**: numerals plus a unit ("3 rounds", "10 minutes", "8 hours", "24 hours"). In-world
  time words ("dusk", "midnight", "three days after the characters first arrive") set
  scheduled events (CoS p. 124). Round counts are used for social set-pieces too, for
  example a conversation that lasts "no more than 3 rounds" (CoS p. 58).
- **Light** comes first in an area entry, as rules terms: "bright light" (34), "dim light"
  (41), "darkness" (170), "darkvision" (192), "lightly obscured" (17) and "heavily obscured"
  (21). AL adventures use a bold run-in **"Light."** feature line under an area heading
  (DDAL04-01 p. 12). Hardcovers use a "General Features" block per site.
- **Travel**: "at a normal pace", "fast pace" and "slow pace" (about 10 hits each). Distances
  are in miles, and the rules are pointed to rather than restated.
- **Exhaustion**: "gains **one level of exhaustion**" (also "suffers", "gain a level of
  exhaustion"), 8 hits. The effects are **never restated**. The SRD 5.1 form is "one level of
  exhaustion".
- **Social rules (DMG pp. 244–245).** The DMG defines three starting attitudes,
  **friendly, indifferent and hostile**. An attitude shifts at most one step per interaction.
  Charisma checks follow the DMG Conversation Reaction table. In adventures the attitude words
  are used as **lowercase adjectives with a preposition**: "is initially **indifferent
  toward** the characters" (OotA p. 9). Other counts: *friendly to/toward* 22, *hostile
  toward/to* 15, *indifferent to/toward* 6. Shifts use the form "shift X's attitude toward
  the party **from hostile to indifferent** by succeeding on a DC 20 Charisma (Persuasion)
  check" (the rules grammar at SKT p. 208). OotA p. 97 describes a two-step shift, hostile to
  indifferent to friendly, earned by helping openly, and cites "(see 'Social Interaction' in
  chapter 8 of the Dungeon Master's Guide)".
  - **Deviation:** RoT and SKT also use off-scale attitude words ("unfriendly", "neutral",
    "cautious"). That is a known inconsistency. Stay on the three-word DMG scale.
  - Several books (OotA p. 9) offer the DMG social rules as optional, with roleplaying,
    Charisma checks or a mix, as suits the group. Roleplay comes first, and the check
    confirms it. The LMoP-era books make the same point: if the players' roleplaying of a
    deception falls flat, the DM can call for a DC 15 Charisma (Deception) check from the
    character doing the talking.

## 10. Encounter difficulty, XP, CR and adjustments

- **Hardcovers rarely state difficulty labels.** "Hard encounter" or "deadly encounter"
  appear about 13 times in all seven books, mostly in RoT, and then as an instruction
  to build one: the DM is told to assemble a hard (or deadly) encounter from a creature
  table using the DMG guidelines (RoT). Encounter tables give **"XP Value"** per creature.
- **CR notation.** In stat blocks: "**Challenge 2 (450 XP)**" (SRD 317 hits). In prose, CR is
  almost never named ("challenge rating N" has 4 hits). XP is written as "**N XP**"
  (458 hits), never "XP N" and never "experience points" outside AL rewards sections.
- **Milestones** are stated as a short bulleted list of story goals in the form
  "Characters … advance to 2nd level" (Death House p. 3; CoS p. 3 likewise; SKT "can
  advance to 3rd level" or "should advance to 4th level"). Alternatively the text says "award
  each character N XP" at a story milestone (LMoP p. 7), or "XP Award" run-ins (OotA 23, LMoP
  3, DDAL04-01 7): "If the characters …, award each character 25 XP" (DDAL04-01 p. 12).
- **AL adjustment sidebar.** This fixed template is the best model for our per-fight scaling
  line (DDAL04-01 pp. 4 and 12; DDEX1-1 p. 8):
  - Heading: **"Adjusting the Encounter"** (73 hits).
  - Stock lead: one sentence saying these are recommendations for adjusting this combat
    encounter, then a second saying the adjustments are **not cumulative**.
  - Bullets keyed to the party-strength label: "**Weak party:** remove one X", "**Strong
    party:** add one Y", "**Very strong party:** …", and "**Very weak party:** …". The labels
    come from a front-matter table of party composition against APL.
  - Each bullet is an **imperative with concrete deltas**: add or remove N creatures, swap a
    stat block, change a DC or a round count. Nothing is vague ("make it harder").
- **Scaling DCs and timing are fair game** in adjustments ("reduce the DC to spot the cats
  to 12", "remove a round between the waves", DDAL04-01 p. 12).

## 11. Rewards and treasure

- **Coin notation**: "N gp" with a space (1,123 hits, against 2 for "Ngp"). The same applies
  to cp, sp, ep and pp. Thousands take a comma ("1,200 ep", 144 hits for "N,NNN gp"). Spelled
  "gold pieces" appears 22 times, mostly in AL reward boilerplate and dialogue. Mixed coin
  runs from smallest to largest with a serial comma: "600 cp, 180 sp, 90 ep, and 60 gp".
- **Valuables** take the form "[object] **worth N gp**" (466) and "**worth N gp each**" (147)
  for sets. In lists the value goes in a parenthetical: "(worth 250 gp)" (CoS p. 124).
- **Treasure blocks.** A **"Treasure."** bold run-in (150 hits) or a TREASURE heading comes
  at the end of the area or encounter. Then either one sentence (DDAL04-01 p. 12 has this
  shape; an invented example: "Under the bench, the characters find a velvet purse holding
  three pearls worth 100 gp each and a *potion of healing*") or a
  lead-in, "The [container] contains the following items:", with bullets. Each bullet reads
  **container → contents → value**, and the item's provenance or quirk goes in a trailing
  parenthetical (CoS p. 124).
- **Magic items in treasure** are italic, with a cross-reference "(see appendix C)" for unique
  items. Stock items get no citation, or "(see chapter 7 of the Dungeon Master's Guide)".
  AL rewards sections repeat each item with its type-and-rarity line and a pointer to where
  its description can be found (DDAL04-01 p. 13).
- **Rewards sections (AL):** Experience goes first (Combat Awards table *Name of Foe | XP per
  Foe*, Non-Combat Awards table *Task or Accomplishment | XP per Character*, minimum and maximum
  per character). Treasure follows (*Item Name | GP Value*), then Story Awards and
  Downtime (DDAL04-01 p. 13). **Non-combat and peaceful solutions carry printed XP.**
- **Hardcover rewards** are embedded where they are earned, not collected at the end.

## 12. Official deviations from pure SRD phrasing, and 2014 vs SRD 5.2.1 terms

**Deviations seen in official 2014 modules** (not errors to copy, but the tolerance band):
- "succeed**s at** a DC …" (AL) alongside "succeeds **on**" (standard).
- "passive Perception" short form in prose.
- Off-scale attitude words ("unfriendly", "neutral") in RoT and SKT.
- Bare dice damage in early books (LMoP and HotDQ traps).
- "the rulebook" (LMoP) instead of a named book.
- AL: "Feel free to…", "the DM" in third person, and spelled "gold pieces" in rewards.
- A creature's sex/race tag in parentheses is a module convention. It is not in the SRD.

**2014 PHB/DMG terms against SRD 5.2.1 (2024 rules).** Our module targets SRD 5.2.1 wording
and must also read correctly at 2014 tables. The 5.2.1 column comes from knowledge of the
document, not from a local extract, so treat every row as **[verify 5.2.1]** before an
auditor cites it.

| Topic | 2014 / SRD 5.1 form | SRD 5.2.1 form | Dual-compatible recommendation |
|---|---|---|---|
| Ability check | "a DC 15 Wisdom (Perception) check" | same | identical; use freely |
| Conditions | "is poisoned", "the poisoned condition" | "has the Poisoned condition" (conditions are capitalized glossary terms) | pick one capitalization house-wide. "has the Poisoned condition" reads fine at 2014 tables |
| Advantage | "has advantage on" | "has Advantage on" (capitalized) | as above: consistent capitalization |
| Damage type | "7 (2d6) fire damage" | "7 (2d6) Fire damage" | average-plus-dice form is identical; only the capital differs |
| Attack line | "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: …" | "Melee Attack Roll: +4, reach 5 ft. Hit: …" | stat blocks follow 5.2.1; prose avoids either label ("makes a melee attack: +4 to hit") |
| Save effect in stat block | prose sentence ("must make a DC 13 … saving throw, taking … on a failed save, or half as much damage on a successful one") | "Dexterity Saving Throw: DC 13, each creature in a … Failure: … Success: Half damage." | stat blocks follow 5.2.1; scene prose keeps the SRD sentence form, which both editions parse |
| Stat block header / CR | "Medium humanoid (human), neutral evil" … "Challenge 2 (450 XP)" | "Medium Humanoid, Neutral Evil" … "CR 2 (XP 450; PB +2)", plus an Initiative line | follow 5.2.1 in `10_Bestiary.md`; CR and XP numbers are the same in both |
| Spell and item names | italic lowercase: *cure wounds*, *potion of healing* | italic Title Case: *Cure Wounds*, *Potion of Healing* | pick one and apply it everywhere |
| Areas | "20-foot-radius sphere", "15-foot cone" | "20-foot-radius Sphere", "15-foot Cone", "Emanation" | geometry is identical |
| Light and terrain | "dim light", "heavily obscured", "difficult terrain" | Dim Light, Heavily Obscured, Difficult Terrain (capitalized) | consistent capitalization |
| Rests | "finishes a long rest" | "finishes a Long Rest" | same verb |
| Exhaustion | 6-level effects table | cumulative: −2 per level to D20 Tests, −5 ft Speed per level | say "gains 1 level of exhaustion" (or "Exhaustion level") and **never restate effects** |
| Inspiration | "inspiration" | "Heroic Inspiration" | name 5.2.1's term, or avoid awarding it |
| Surprise | surprised creatures can't act on the first turn | Disadvantage on Initiative | never restate; say "is surprised" and let the table's rules apply |
| Actions | Search, Use an Object, Help, Dash … ("cast a spell" as the Cast a Spell action) | adds Influence, Study, Utilize, Magic | prefer names in both (Search, Help, Dash, Hide). Where 5.2.1 names differ, describe the act ("uses an action to …") |
| Social | DMG (not SRD 5.1) attitudes friendly/indifferent/hostile, Conversation Reaction table | Influence action with a creature's attitude (Friendly, Indifferent, Hostile) affecting the check; 2024 DMG adds more **[verify exact 5.2.1 text]** | the three attitude words exist in both editions; use them, plus "DC N Charisma (Persuasion) check" |
| Encounter difficulty | Easy / Medium / Hard / Deadly XP thresholds per character, with **multipliers** ("adjusted XP") | 2024: Low / Moderate / High XP budget per character, no multipliers **[verify whether SRD 5.2.1 carries encounter building at all]** | don't mix vocabularies in one line. "Medium … adjusted XP" is pure 2014. If 5.2.1 is the target, state the budget in its terms and optionally give the 2014 equivalent in parentheses |
| DM role name | SRD 5.1 says "GM"; books say "DM" | "GM" in the SRD | project uses **MM** by house rule |

---

# C. CHECKLIST (for auditors)

**Voice**
- **C-V1.** In DM-facing prose, "you" means only the DM (MM for us). The players are never
  addressed except in read-aloud and handouts.
- **C-V2.** The party is "the characters" by default. "The party" and "the adventurers" are
  variants. "A character who …" names individuals. "PCs" does not appear. "The players" means
  only real people at the table.
- **C-V3.** Situations and trigger consequences are in the present tense ("If …, X orders"),
  not "will". The past tense is only for backstory.
- **C-V4.** Mean sentence length is about 16–19 words (median 15–17). About 10% of sentences
  run over 30 words, and short 5–8-word sentences occur regularly. A section whose mean is
  above 22, or which has no sentence under 10 words, fails this check.
- **C-V5.** Paragraphs run 3–5 sentences and about 45–75 words. One-sentence ruling
  paragraphs are fine. Paragraphs over about 120 words appear only in background blocks.
- **C-V6.** The register is plain and confident. Canon facts are asserted without "perhaps",
  "it seems" or "possibly". "Might" appears only for what players or NPCs may do.
- **C-V7.** Mood lives in read-aloud. DM prose after a box states function: what it is,
  whether it's dangerous, how long it lasts, and what ends it.
- **C-V8.** Branching uses "If the characters [observable act], [present-tense consequence]".
  Fallbacks use "Otherwise, …" or "Unless the characters …, …". Stacked consequences go in
  a Development block, one "If" per sentence.
- **C-V9.** Discretion is delegated with a default and a dial ("You can delay X if …").
  There is no blank "at your discretion" or "up to you" without a stated default.
  "Feel free" is at most AL-rate (a few per module).
- **C-V10.** NPC interiority is written with plain verbs (wants, fears, believes, knows,
  doesn't know). Secrets are stated flatly to the DM next to the surface ("Although …, X
  is actually …"). A secret is never coy or withheld from the DM.
- **C-V11.** "What they know" is a trigger sentence plus a bullet list, one fact per bullet.
  False beliefs carry a trailing truth parenthetical, and deeper layers are gated by "If
  pressed" or "If the characters ask about …".
- **C-V12.** Social scenes give tiered outcomes, and failure still yields the lead the plot
  needs. Faction reactions are one clause per faction.
- **C-V13.** There are no rhetorical questions, designer "we", "Note that" or "It's important"
  openers, exclamation marks, winks or jokes at the players' expense in DM prose. Humor comes
  only as a deadpan informational one-liner.
- **C-V14.** Core rules are pointed to, never re-explained.

**Mechanics**
- **C-V15.** Every check uses the form "DC N Ability (Skill) check", or "DC N Ability check"
  when no skill applies. There is never a bare "Perception check" and never a DC range.
- **C-V16.** Checks use the standard frames: "succeeds on", "must succeed on", "With a
  successful DC …", "A successful DC … check reveals that …" or "can make". The result is
  stated as an observable fact. A failure line is added only when failure changes something,
  in the form "If the check fails, …", "On a failed check, …" or "fails by 5 or more".
- **C-V17.** Group checks read "a DC N group Ability (Skill) check". Contests read "… check
  contested by X's Ability (Skill) check" and have no DC. Passive thresholds read "a passive
  Wisdom (Perception) score of N or higher".
- **C-V18.** Saves use the SRD sentence templates: demand → "taking N (XdY) type damage on a
  failed save, or half as much damage on a successful one", "or be [condition] for 1
  minute", and the repeat-save clause verbatim.
- **C-V19.** Damage is written "N (XdY) type damage", average first. Numerals and singular units
  are used ("1 minute"). Conditions are plain adjectives or the "[X] condition" form, never
  italic.
- **C-V20.** Advantage is always attached to a named roll ("has advantage on Charisma
  (Persuasion) checks made to …").
- **C-V21.** Spell and magic-item names are italic, and their case is consistent with the
  chosen edition (§12). Stat-block creature names are bold at first appearance in an
  encounter. Named NPCs get a parenthetical tag with the stat-block name bold.
- **C-V22.** Cross-references use the forms "(see appendix B)", "(see area X)" and
  '(see chapter N, "Title")'. Stat reuse uses "uses the **X** statistics" or "…, with the
  following changes:".
- **C-V23.** Light, rests, exhaustion, travel pace and attitudes use the rules terms
  (dim light; finishes a long rest; gains one level of exhaustion; friendly/indifferent/hostile
  toward). Effects are never restated.
- **C-V24.** Difficulty and XP read "N XP", and CR appears only in stat blocks. The scaling
  note follows the AL template: labeled strength, then an imperative with concrete deltas,
  "not cumulative". The difficulty vocabulary stays within one edition per line.
- **C-V25.** Coins are written "N gp" with a space and commas for thousands. Mixed coin is
  listed smallest to largest with a serial comma. Valuables read "worth N gp (each)".
  Treasure entries read container → contents → value, with the quirk in a parenthetical, and
  peaceful or clever outcomes carry printed rewards.
- **C-V26.** Edition terms are consistent. Every condition, advantage, damage type, spell and
  item name uses one capitalization scheme (2014 lowercase or 5.2.1 capitalized)
  throughout the module and bestiary.

---

# D. "Our phrasing smell → official form" (grep list)

Run these from `conversions/dnd5e/oraga_night/`. Patterns use `grep -nE` (ERE) unless marked
`-P`. Expect false positives in read-aloud (italic `*…*` blocks) and dialogue, so triage by
hand.

Each entry gives the smell, the pattern or patterns (separated by " ; "), and the official form.

- **S1. "PCs" in prose.** Pattern: `\bPCs?\b`. → Official form: "the characters" / "a character".
- **S2. "the players" meaning the characters.** Pattern: `\b[Tt]he players (notice|find|see|learn|enter|arrive|attack|are)`. → Official form: "the characters …".
- **S3. Bare skill check, no ability.** Pattern: `DC ?[0-9]+ (Perception|Insight|Investigation|Persuasion|Deception|Intimidation|Stealth|Athletics|Acrobatics|Arcana|History|Religion|Nature|Survival|Medicine|Performance|Sleight of Hand|Animal Handling) check`. → Official form: "DC 15 Wisdom (Insight) check".
- **S4. Skill-first or ability-less forms.** Pattern: `(Insight|Perception|Persuasion|Deception|Stealth|Investigation) \(?(Wisdom|Intelligence|Charisma|Dexterity)\)?` ; `\b(an?|the) (Insight|Perception|Persuasion|Deception|Stealth) (check|roll)`. → Official form: "a Wisdom (Insight) check".
- **S5. DC as a range or approximate.** Pattern: `DC ?[0-9]+ ?[–-] ?[0-9]+` ; `DC (of )?(about|around|~)`. → Official form: a single DC.
- **S6. "roll" for a check.** Pattern: `\b(roll|rolls) (a |an )?(Wisdom|Charisma|Intelligence|Dexterity|Strength|Constitution)\b` ; `(Insight|Persuasion|Perception) roll`. → Official form: "make a DC N … check" / "succeeds on".
- **S7. "beat/pass/make the DC".** Pattern: `\b(beat|beats|pass|passes|hit|hits|meet|meets) (the |a )?DC\b`. → Official form: "succeeds on a DC N … check".
- **S8. "save" in the demand clause.** Pattern: `(make|makes|attempt|attempts) a DC ?[0-9]+ [A-Z][a-z]+ save\b`. → Official form: "… saving throw" (use "save" only in "on a failed save").
- **S9. Failed/successful outcome with "saving throw".** Pattern: `on a (failed|successful) saving throw`. → Official form: "on a failed save" / "on a successful one".
- **S10. Half damage paraphrased.** Pattern: `half (damage )?on a (success|successful save)` ; `half as much on`. → Official form: "or half as much damage on a successful one".
- **S11. Bare dice damage.** Pattern: `(takes|taking|deals|dealing|take) [0-9]+d[0-9]+`. → Official form: "takes 7 (2d6) fire damage".
- **S12. Damage type before dice or missing.** Pattern: `[0-9]+ \([0-9]+d[0-9]+( ?\+ ?[0-9]+)?\) damage`. → Official form: "7 (2d6) slashing damage".
- **S13. Spelled-out game durations.** Pattern: `for (one|two|three|ten) (minute|minutes|hour|hours|round|rounds)\b`. → Official form: "for 1 minute", "for 10 minutes".
- **S14. Condition italicized/bolded.** Pattern: `\*{1,2}(blinded|charmed|deafened|frightened|grappled|incapacitated|invisible|paralyzed|petrified|poisoned|prone|restrained|stunned|unconscious)\*{1,2}` (case-insensitive). → Official form: plain word, or "the Poisoned condition".
- **S15. Mixed condition capitalization.** Pattern: `grep -noiE '\b(poisoned|frightened|charmed|restrained|prone|incapacitated)\b'` then check case consistency. → Official form: one scheme (§12).
- **S16. Mixed advantage capitalization.** Pattern: `\b[Aa]dvantage\b` , `\b[Dd]isadvantage\b` (count both cases). → Official form: one scheme.
- **S17. Floating advantage.** Pattern: `(gets?|has|have|gain|gains) (an? )?advantage(\.|,| in | for the (scene|rest))`. → Official form: "has advantage on [named roll] …".
- **S18. Passive threshold phrasing.** Pattern: `passive (Perception|Insight) (of )?[0-9]+\+?` ; `passive [A-Z][a-z]+ ?≥`. → Official form: "a passive Wisdom (Perception) score of 14 or higher".
- **S19. Spell or item not italic.** Pattern: `\b(potion of [a-z]+|cure wounds|healing word|detect magic|charm person|sleep|invisibility|spell scroll)\b` outside `*…*`. → Official form: *potion of healing* (italic).
- **S20. Stat-block name not bold at first appearance.** Pattern: `\b(two|three|four|five|six|[0-9]+) (guards?|thugs?|bandits?|spies|spy|nobles?|veterans?|assassins?|cultists?|mages?)\b` not wrapped in `**`. → Official form: "four **guards**".
- **S21. Coin without space, or spelled gold.** Pattern: `[0-9]gp\b` ; `[0-9,]+ gold( pieces)?\b` ; `[0-9]{4,} gp` (missing comma). → Official form: "1,200 gp".
- **S22. Value phrasing.** Pattern: `(valued at|value of|costs?) [0-9,]+ ?gp`. → Official form: "worth 50 gp", "(worth 50 gp each)".
- **S23. Future tense for trigger consequences.** Pattern: `\bIf [^.]{3,80}, (he|she|they|it|the [a-z]+) will\b`. → Official form: present tense: "…, the steward calls the guards".
- **S24. Blank discretion.** Pattern: `at your discretion|up to you|as you see fit|whatever (feels|seems) right|use your (best )?judgment`. → Official form: "You can [X] if [condition]; by default, [Y]".
- **S25. Hedged canon or rules.** Pattern: `\b(perhaps|possibly|probably|it seems|seemingly|arguably)\b` (DM prose only). → Official form: assert, or move to an in-world rumor.
- **S26. Meta openers.** Pattern: `\b(Note that|It is important|It's important|Keep in mind that|Remember,|This section (will|describes))`. → Official form: cut, or a single specific reminder.
- **S27. Rhetorical questions in DM prose.** Pattern: `^[^*>"“].*\?\s*$` (lines not read-aloud, dialogue or quote). → Official form: a statement.
- **S28. Designer "we".** Pattern: `\b(we|We|our|Our|us)\b` outside credits and designer boxes. → Official form: "you" (to the MM) or impersonal.
- **S29. Exclamation in DM prose.** Pattern: `^[^*>"“]*![^"”]*$`. → Official form: a period.
- **S30. "If not," fallback.** Pattern: `\bIf not,`. → Official form: "Otherwise, …".
- **S31. Off-scale attitudes.** Pattern: `\b(unfriendly|neutral|cautious|wary|warm) (to|toward)\b`. → Official form: friendly / indifferent / hostile toward.
- **S32. Restated core rule.** Pattern: `(which means|this means) (they|the character|a creature) (can't|cannot|has|have)` near a condition/exhaustion/surprise word. → Official form: point to the rule; don't restate.
- **S33. Exhaustion effects restated.** Pattern: `exhaustion[^.]{0,80}(disadvantage|speed|halved|−2|-2)`. → Official form: "gains one level of exhaustion".
- **S34. Mixed difficulty vocabulary.** Pattern: `\b(Easy|Medium|Hard|Deadly)\b[^.\n]{0,60}\b(Low|Moderate|High)\b` ; `adjusted XP` alongside `Moderate|High`. → Official form: one edition per line (§12).
- **S35. XP or CR notation.** Pattern: `XP ?[0-9]|[0-9]+XP|experience points` (outside a rewards table) ; `CR ?[0-9/]+` in prose. → Official form: "450 XP"; CR only in stat blocks and budget lines.
- **S36. Vague scaling.** Pattern: `(make it|slightly) (harder|easier)|scale (up|down) as needed|adjust as (needed|appropriate)`. → Official form: "Strong party: add one **guard**; raise the DC to 15.".
- **S37. Area/distance words.** Pattern: `\b(five|ten|fifteen|twenty|thirty|sixty) (feet|foot)\b`. → Official form: "30 feet", "a 20-foot-radius sphere".
- **S38. Group check phrasing.** Pattern: `(everyone|each character|the whole party) (rolls|makes) (a )?(Stealth|Dexterity)`. → Official form: "a DC 12 group Dexterity (Stealth) check".
- **S39. Contest phrasing.** Pattern: `(opposed|versus|vs\.?) (by )?(their|its|the [a-z]+'s) (Insight|Perception|Deception)`. → Official form: "contested by the X's Wisdom (Insight) check".
- **S40. Sentence-length drift.** Pattern: a script, not grep: mean words per sentence over 22, or a section with no sentences under 10 words. → Official form: §2 norms.

*End of file.*
