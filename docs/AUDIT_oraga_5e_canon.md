# Audit — Oraga Night 5e: Canon, Continuity, Licence, Prose

*2026-09-27. Read-only audit of `conversions/dnd5e/oraga_night/` (README, 01–11,
INVENTIONS_5e.md, flow/) on `feat/oraga-5e` (PR #33), against `adventures/oraga_night/`,
`settings/valloh/`, `docs/BRIEF_oraga_5e.md`, `docs/REVIEW_oraga_5e.md`, and the owner's
private canon notes (consulted, not quoted; nothing from them is reproduced here).
Lens: canon fidelity, inventions, internal continuity, leakage, licence/trademark,
prose. Mechanics balance is out of scope.*

## Executive verdict

**Canon fidelity is high.** Chapters 01–08 reuse the source almost line for line (diffs of
02, 06, 07 and 08 are small and additive). Every owner ruling I was asked to check holds
at the level of story: no fight is mandatory and every one is shown before it starts; the
Radiant is never turned and its guilt never ends the hunt (05 and 10 now say so
explicitly); the midnight attack is the Uninvited's alone and Tavva is blindsided; the
Bought hold the gate; Raunu dies by his own choice by default; everyone is Human; no
books, with the invitation and slate carve-outs; *What the Module Never Says* is held,
and 01, 02, 04 and 10 add spell-by-spell refusals. **No true names, no master's name, no
word on the child's nature or the missing year appear anywhere** — grep for every
private-canon name returned zero hits in the conversion, the flow data and the HTML.

**Nothing is Critical, but five Major findings should be fixed before merge.** One is a
leak (a private metaphysical fact paraphrased into the public inventions log), one
depersonalises the Uninvited against an explicit owner ruling, one is a self-contradiction
about which fights are winnable, one opens a faction route to the heir secret, and one is
"D&D" used as a title in the PR, the commit and the flow page. The rest are Minor:
continuity slips, a handful of unlogged inventions, source errors carried over unfixed,
four read-aloud breaches, and some AI rhythm in the new chapters.

**Counts:** Critical 0 · Major 5 · Minor 14.

---

## Findings, ranked

### MAJOR

**A-1 · Major · Leakage · `INVENTIONS_5e.md` rows #17, #18, #38**
*Evidence.* Row #17's *Derived from* cell cites "private author canon notes" and
paraphrases three facts from them. Two of the three are already public in the source
module (the shadow-step, the "they are people" ruling). The third is a metaphysical fact
about what the Uninvited can and cannot access, and it uses a term that appears in no
public file: grep across `adventures/oraga_night/`, `settings/valloh/` and the rest of
the conversion finds it only in that cell. Rows #18 and #38 cite the same private notes.
#38 adds "references/, not in repo" and "The Vell line leans on author canon without
naming it".
*Why it matters.* The repo is public and the branch is already pushed. The owner's rule
is that module text uses only the veiled forms. A reviewer's provenance cell is still
committed text. Pointing readers at an unpublished notes file, and saying a line "leans
on author canon", tells them there is something there to dig for.
*Fix.* Delete the private-notes paraphrase from #17. Cite public sources only: Ch. II
"whatever greater powers they once wielded are sealed away with their master" covers the
same ground. In #18 and #38, replace "private author canon notes" with the public Ch. VII
MM-truth paragraph, which already states Vell's mind-reading. Drop "leans on author
canon". A follow-up commit is enough, because no name leaked. Keep the sourcing to the
private notes in the gitignored `references/` file.

**A-2 · Major · Canon (owner ruling: the Uninvited are people, pronouns she/he, no
"creatures") · 10 *The Radiant*, *The Hollow*, *The Wept* traits; 05 rules parentheticals;
05 L644, L185**
*Evidence.* The Radiant's block uses *it/its* 44 times and *he* not once. Examples:
"It is not undead and it is not afraid", "its Speed is halved", "It re-stages the kill".
The source `.fof` and 05's Fracture truth call him *he*. The Hollow's shared traits
(*Leashed*, *Not Its Quarry*, *The Post*) use *it*, and his Fracture paragraph and Wants
line use *he*. The Wept is *she* in her own traits and *it* in "As the Hollow, except
that it returns…". In 05, the rules parentheticals ("its *Witnessed* trait") sit inside
paragraphs that call the Radiant *he*. Two phrasings carried over from the source also
survive the ruling: "Three creatures on a leash did not set fires" (05 L644) and "moving
like things called home" (05 L185).
*Why it matters.* The owner ruled that the Uninvited are human (Ch. II: "they are
people. Not revenants, not shades."; INVENTIONS_5e #17 tags them *Humanoid (Human)* for
the same reason), and the module was swept of wording that makes them things. The whole Fracture
mechanic depends on the table treating them as persons. A 5e stat block is where an MM
reads them most closely, and it is where the edition turns them back into *it*.
*Fix.* Give the Radiant *he* throughout his block and in 05, and the Hollow *he*. Write
each shared trait out per creature, or phrase them neutrally ("the Uninvited returns…").
Replace "Three creatures on a leash" with "Three people on a leash", and "things called
home" with "people called home". Fix both editions.

**A-3 · Major · Canon (owner ruling: Tavva's crew is the winnable fight) and continuity
· 05 L194, L701; 09 L397–398, L402, L777; 07 L471–472; 08 crisis panel; vs 05 L603–605**
*Evidence.* The book says, in five places, that S5 is "the night's one fully winnable
fight". 05 L701 says the Bought are "the only antagonist tonight that can be beaten".
09 L402 goes further: "the only antagonists tonight who can be beaten, bargained with or
outlasted". Against that, 05 L603–605 says the Circle's delivery and the fourth iron are
"both … fights a 3rd-level party can win outright", and every snake card S6–S13 is a
beatable fight. 07 had already fixed the Bought line ("They can be beaten, and — more
usefully — they can be talked to"), and 09 L402 undoes the fix.
*Why it matters.* The source made these claims when they were true. In this edition
they are false, and they are false about a line the owner ruled on. An MM reading 05
next to 09 cannot tell which fight the ruling is protecting.
*Fix.* Keep Tavva's special status, and say what it is: the one fight with nothing at
stake but decency. For example: "the night's one fight with no faction, no clock and
nothing at stake but property and decency — aimed straight at the players' better
natures". Change the two "only antagonist(s) who can be beaten" lines to "the only mortal
antagonist between the crowd and the way out".

**A-4 · Major · Canon (the pregnancy never becomes known beyond the east wing) · 09 S7
clock "Full"; 04 Undercurrent C parenthetical; 09 Circle *Turn it*; Snake Tracker
(INVENTIONS #9)**
*Evidence.* Chapter II (source and 5e): "The only people who may ever know are players
who earned the east wing." When S7's clock fills, a Circle knife "sees … small linens …
a midwife … and walks back out to tell Callun there may be an heir". The clock advances
on any round the knife moves "unhindered", so no player character is needed. 04 also
turns the source's passing "sell it (the Circle would reprice the room)" into a costed
transaction that sets Circle heat to 4. #9 is logged, and "tells no one" keeps the
*public* record intact. It still breaks the narrower canon line that only players may
ever know.
*Why it matters.* The heir is the most closely held secret in the module. The owner
ruled that it never becomes public, and the source limits who can know it to players who
earned the east wing. This is also the only snake beat that touches that secret.
*Fix.* Either (a) let the knife see the linens and misread them, bringing Callun the
rumour the whole ballroom already believes (the mad wife) rather than "an heir", or
(b) keep Callun's knowledge only on the route a player causes (the sale), and make the
S7 clock fill with the knife caught at the door by the doubled guard. Either way, get
the owner's ruling on #9 before merge. It heads the file's "Review these first" list
and should stay there.

**A-5 · Major · Trademark · PR #33 title; commit `bcd7658` subject;
`flow/flow_page.template.html` L111 and the generated `oraga_night_flow.html`; BRIEF
title**
*Evidence.* The PR is titled "Oraga Night: D&D 5e edition …". The commit subject is "Add
Oraga Night D&D 5e edition …". The flow page's eyebrow reads "Oraga Night · D&D 5e
edition · module flow". The book itself is clean: it uses "fifth edition", "5e" and "SRD
5.2.1" throughout, and never "Dungeons & Dragons".
*Why it matters.* CC BY 4.0 licenses the SRD's copyrighted text, not the *Dungeons &
Dragons* / *D&D* trademarks. Using the mark as a product title implies an affiliation
the licence does not grant. The flow page is the piece most likely to be published as
a standalone HTML artifact. It also carries no SRD attribution.
*Fix.* Retitle the PR and the flow eyebrow along the lines of "Oraga Night — Fifth
Edition" or "compatible with fifth edition (SRD 5.2.1)". Regenerate the HTML. Add the
SRD 5.2.1 attribution statement to the flow page footer. Optionally add a line to the
README: "Not affiliated with or endorsed by Wizards of the Coast." The directory name
`dnd5e/` is low risk but could become `5e/`. The commit subject stays in history, so no
action is needed there beyond the PR title.

### MINOR

**A-6 · Minor · Never Says against spells · 02 L243–248; 04 L613–614, L954–956; 01
L421–427**
*Evidence.* "The pale factor's mind is not a room a 3rd-level caster gets into." That
line invites the question of which level *does* get in, and the aftermath wing reaches
5th. *Speak with dead* on Raunu "returns something true and small", but the book gives
no example, so the MM has to invent one under pressure. *Detect thoughts* on Raunu finds
"a man thinking about a staircase", which is new and unlogged, though harmless: it
foreshadows "Corval. The stairs."
*Fix.* Make it "is not a room any caster at this table gets into". Print two or three
canned small true answers for *speak with dead* ("It was dark." · "She was upstairs." ·
"I chose."), each checked against the Never Says list. Log the staircase line.

**A-7 · Minor · Written-word continuity · 05 L314 vs 03 L170; 05 L178; 06 L102**
*Evidence.* 03 says there are no spell scrolls in Val'loh. 05 says "a *wall of force* if
somebody has a scroll". Two lines carried over from the source also contradict the ban:
"the escape in the history books" (05 L178) and the inquest that "everyone signs" (06
L102).
*Fix.* Change the scroll line to "a *wall of force* if somebody has one". Change
"history books" to "the record". Change "everyone signs" to "everyone swears to", or rule
that signing before a Church notary is sanctioned. Fix the last two in the source too.

**A-8 · Minor · DC ladder for masks · 01 L65 and 04 L10 ("13 behind a mask") vs 01
L461–464 ("a masked approach is Easy … DC 10") vs 03 L204–206 and 04 L376–378 (DC 10 only
for someone far above your station)**
*Fix.* Change 01's troubleshooting to "an approach *across station* behind a mask is
Easy (DC 10)".

**A-9 · Minor · "No mandatory fights" in the data · `flow.json` nodes `S3`, `gate-fight`
(`optional: false`); 01 L502 "it is the only fight the ending needs" (inherited)**
*Evidence.* The prose is careful ("The fight is optional; the gate is not"), but the
flow marks the S3 *fight* as non-optional, and the abridged run calls it the fight the
ending needs.
*Fix.* Leave `b12` non-optional, and set `S3` and `gate-fight` to `optional: true`. Change
01 to "it is the only scene the ending needs; the fight in it is still optional".

**A-10 · Minor · Draunel's irons · 10 *Essar Draunel* Nastier ("a fourth iron you didn't
find"); 09 S13 Scaling ("Draunel's fourth iron — whatever the table did not find")**
*Evidence.* The source gives "three other irons" alongside Agenda 3. 09 names all four,
and Iron 4 is the arrest. Both dials describe a further, unnamed scheme, which means a
fifth iron.
*Fix.* Change the Nastier line to "Iron 3 is in the room: two duelists who have watched
Vorlain all night and will swear to anything". Make S13's scaling concrete in the same
way.

**A-11 · Minor · Roster/timing continuity**
- S13: "What is happening" says "three duelists and their lord", while Enemies lists
  Draunel plus **two** duelists and the read-aloud shows "three men in good coats".
  Pick one.
- The appointment is made "after the bells, on the terraces" (04 Mv IV, 09 Iron 2), but
  S9 runs in Movement V, *before* midnight. Change it to "at the first quarter-bell".
- Bought Captain Breaks: "it contracted for two diversions". Task 1 in the contract is
  three targets (two districts and the courier post). Change it to "for diversions, not
  for this".
- Gallery Knives: "Four of them tonight" (10), S2 has three with Tavva, and 07 says
  "crew of four". State once whether Tavva is one of the four.

**A-12 · Minor · Invention that may contradict rather than extend · 09 S13 broker out;
10 *Essin* Wants/Breaks (INVENTIONS #13)**
*Evidence.* The source line "knows exactly where its two bodies are buried" reads as an
idiom for secrets. The 5e edition makes it literal: hidden corpses whose location Essin
can trade. The 3160 killings are public knowledge, which makes secretly buried bodies an
odd fit.
*Fix.* Owner call. If the idiom was meant, recast the out as trading the *secrets* of
Vorlain's year.

**A-13 · Minor · Unlogged inventions (INVENTIONS_5e.md is otherwise thorough)**
Not in the log:
- The Circle "keeps its accounts in trained heads, the only way the law allows" (04 Mv I).
- The Church Wardens' grey robes, and their *Keepers of the Word* authority to seize any
  writing, grown or held, "and it takes what it finds" (10). This is an institutional
  power. #6 logs the Wardens' actions, not this power.
- Alignments assigned to canon NPCs, including *Neutral* for all three Uninvited and
  for Vell (10).
- Raunu "thinking about a staircase" (04).
- The Wept humming the cradle-song *mid-attack* when bloodied, which is a new tell (10).
- The chapel as "the only short rest the ball offers" (04 B6), a mechanic with a
  fictional hook.
- Pello's thieves' cant as "signs, knots and chalk that gets wiped", a new grey zone at
  the edge of the written-word ban (11).

*Fix.* Add them to the table. Consider dropping alignments for the Uninvited and for
Vell ("Alignment —") rather than rule on their morality.

**A-14 · Minor · Source errors carried over unfixed (fix in both editions after owner
rulings)**
- Kovaun "works the room like a man taking a census of souls" (04 L866). Kovaun is
  *she*.
- "a century" (01, 04) vs "two centuries" (07, 10) vs "centuries" (05, 10) out of
  fashion.
- 04 says fourteen named guests, 07 says fifteen.
- The Going-east sidebar (06) says the mists are rising "*because the child got away*".
  That answers part of Never Says item 4 ("why they recede"). Ask the owner whether the
  causal clause stays.
- The two open questions the integration review already raised: sixty or eighty
  servants, and which witnesses the testament had.

**A-15 · Minor · Read-aloud rule (only what the characters perceive, never what anyone
feels or does inside) · new boxes in 09**
- S2: "She has not raised the alarm. **She is deciding.**"
- S7 (Mv V): "doing nothing, **the way men do nothing when they have been told to**."
- S11: "**You saw it** in the last of the rose", which tells the players what their
  characters perceived.
- Inherited in 04: "nobody has been told not to".

*Fix.* "She has not raised the alarm." (stop there) · "doing nothing, and not talking" ·
"In the last of the rose, a small man…" · "and nobody is walking toward them."

**A-16 · Minor · Prose: AI rhythm in the new sections**
Chapters 01–08 keep the source's voice because they *are* the source's voice. The new
material in 09, in the 04/05 snake boxes and in 10's lines falls back on a few habits:
- Negative-parallel pairs: "They are not villains. They are the most frightened armed
  people in the palace" (09 L324); "The Uninvited are the scene. The snakes are what the
  scene walks past" (05 L599).
- Epigram closers: "Breaks. Never. Not the leash's fault, and not yours." (10 Radiant);
  "None of them wants to hurt an Orthaen at this ball; all of them will." (09 S10);
  "Every snake in the pen is in the room to watch him do it. Not one of them is ready for
  what comes next." (04 L1236–1237, a cliché end-of-chapter stinger).
- Stock phrases repeated across cards: "a plain good coat" about twenty times; "a debt
  of a very particular kind" twice; "a cliff, not a step" twice; "exactly" 8× in 09 (2×
  in the source's scene cards).
- Self-praise: "This is the best thing in this module." (09 S3, carried over from the
  source card, where it was already odd).

None of this is severe, and some of it is good (the Hollow's "Nastier. None. He does not
want anything enough to be nastier." earns its place). *Fix.* Do a light humanizer pass
on 09 and on 10's Wants/Tells/Breaks/Nastier lines only. Cut the chapter-end stinger in
04. Vary "plain good coat" after its first use in each chapter ("the Circle's man", "the
coat"). Per the house rule, change as little as possible.

**A-17 · Minor · Licence hygiene**
- The SRD 5.2.1 attribution is correct and verbatim in README, 09 and 10. Chapter 11
  closely paraphrases SRD class-feature text but has no attribution line, and neither
  does the flow page (see A-5). Add the statement to 11.
- CC BY 4.0 §3(a)(1)(B) asks adapters to indicate changes. Add one clause to the README
  attribution: "Stat blocks and rules text are adapted; all creatures are original."
- Terminology: "a caster reaches for the third circle" (06) is non-SRD jargon; use
  "level 3 spells". "Calligrapher's kit" (03) is *Calligrapher's Supplies* in the SRD.
- README: "The world of Svara and all its canon belong to the setting's author" sits
  awkwardly beside the GPLv3 grant on the same text. Ask the owner whether setting
  canon is meant to be carved out of the GPL grant. If it is, say so explicitly in the
  root LICENSE/README rather than in a module README.
- "City Watch Veteran" (Dassa's background) is the project's own FoO background name,
  and no WotC text is used. There is no licence issue, but WotC has a similarly named
  non-SRD background, and the owner may want that noted.

**A-18 · Minor · Canon extension to confirm · 04 Undercurrent C parenthetical; 09 Circle
*Turn it***
*Evidence.* Selling the nursery to Callun now has a price and a mechanical consequence
(heat to 4, S12). The source only mentioned it in passing. This is covered by A-4's
ruling. It is listed separately so the owner sees that the *player-driven* route also
changed.

**A-19 · Minor · Kovaun's recognition range · 10 *A Census of Souls* (INVENTIONS #20)**
*Evidence.* "and one or two that nobody living has". This gives Kovaun knowledge of rites
*older than living memory*, which is exactly the Radiant's tell. It may let the Church
read more into the Uninvited than the source allows (the source has her recognize the
blessing as "not used in living memory", and nothing about knowing *what* it is).
*Fix.* Keep recognition at "a form not used in living memory" and let her know no more
than that. Owner call.

---

## What I checked and found clean

- **Leakage:** zero hits across `conversions/dnd5e/oraga_night/` (all .md, flow.json,
  the HTML and the template) for every proper name and author-only term in the owner's
  private notes, including the names on the Never Says list and the child's name and
  nature. The only exception is A-1. "Krenn", "Mazaa(ian)" and "Svara" appear only
  where the public source already uses them.
- **Owner rulings:** as listed in the verdict. Maiven's default death, Vorlain's hero
  turn, "no one is ever charged", the Second Clause failing, and the Bought captain's
  honour clause all match the source.
- **Room keys B0–B13** match the source (Root = B11, B12 = the gate after midnight, no
  B12 in Ch. IV). **Card IDs S1–S13** are consistent across 01, 04, 05, 07, 08, 09, 10
  and `flow.json`. **Snake Tracker** start/rise/fall values match between 08 Table VIII–7
  and 09 Table IX–2.
- **Pregens:** every biographical line matches `characters/*.fof`. Ilesse's
  *Thaumaturge* note correctly separates the SRD term from Val'loh's Thaumaturgy, and no
  deity or patron is assigned.
- **SRD scope:** every class, subclass, feat, spell and tool named is in SRD 5.2.1 (the
  integration review verified the same). No WotC setting names, monsters or non-SRD
  subclasses. Every creature is an original block.
- **Flow:** `build_flow_page.py` regenerates `oraga_night_flow.html` byte-identically
  (I ran it read-only; `git status` stayed clean).
