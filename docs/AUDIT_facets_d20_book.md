# AUDIT — Facets d20 as a product: prose, organisation, licence, canon

*Branch `feat/facets-d20` (PR #32), commit 60848cd. Scope: `facets_d20/README.md` and
chapters 01–10. Read-only audit: nothing else was edited. Read against `CLAUDE.md`,
`references/phb-examples.md`, `style/STYLE_GUIDE.md`, `docs/BRIEF_facets_d20.md`
§4.1/§4.6 and `player_handbook/Appendix_Magic_Domains.md`. Drafter ownership, from
DESIGN §5: **A** = README, 01, 02, 06, 08, 10 · **B** = 03, 04, 05 · **C** = 07, 09.*

## Executive verdict

The book works as a product. It is short, it is honest about what it leaves to the SRD,
and a d20 player could build a character from it in an evening. The voice is dry,
confident and mostly human. The three drafters sound like one author, which is rare.
The SRD 5.2.1 attribution is word-perfect and appears in every file. The MM term is
used throughout, with no GM or DM anywhere, and no Shattered Origin or Val'loh lore
has leaked in.

It is not ready to ship as is, for four reasons:

1. **Licence policy.** About nine talents and signatures are close mechanical
   derivations of *non-SRD* WotC material: the 2024 PHB feats Tough, Sharpshooter,
   Sentinel, Great Weapon Master and Healer, plus the Assassin, Circle of the Moon and
   Artificer subclasses. BRIEF §4.1 forbids this. None of the text is copied, so the
   legal risk is low, but the policy breach is real and the DESIGN doc wrongly says
   Tough is in the SRD.
2. **Rules duplicated across chapters have already drifted apart.** *Martial Training*
   is printed differently on the Mind and Soul menus, and both chapters say the two
   entries are the same. Cantrip progression is stated three ways that don't agree.
3. **Canon.** Divination has been quietly made an Invocation domain, while the text
   calls the list "the game's twenty-one canon domains". Small new facts have been
   invented for the recurring cast.
4. **Missing apparatus.** There is no character sheet (Drives, Sparks, Specialty,
   talents and signature don't fit an SRD sheet), no glossary, no index and no
   all-talents finder.

The prose has no em-dash problem: there are zero in body text. Its tell is the
**aphoristic kicker and the not-X-but-Y reframe**, about 70 of them, most dense in
07 and 09. A light de-patterning pass of about 40 sentences fixes it without
flattening the voice.

**Counts:** Critical 0 · Major 8 · Minor 20.

---

## Prose tally (hand count after a full read; pattern instances, not lines)

| Chapter (drafter) | Words | Kicker / summary line | Not-X-but-Y reframe | Triad reflex | Em-dash in prose | Flavor inside a rules entry |
|---|---|---|---|---|---|---|
| README (A) | ~410 | 1 | 1 | 2 | 0 | 0 |
| 01 (A) | ~830 | 3 | 2 | 0 | 0 | 0 |
| 02 (A) | ~1,630 | 3 | 1 | 1 | 0 | 0 |
| 03 (B) | ~3,030 | 5 | 2 | 1 | 0 | 4 |
| 04 (B) | ~2,700 | 4 | 2 | 1 | 0 | 3 |
| 05 (B) | ~2,830 | 3 | 3 | 2 | 0 | 2 |
| 06 (A) | ~2,030 | 4 | 5 | 1 | 0 | 0 |
| 07 (C) | ~2,870 | 5 | 9 | 3 | 0 | 0 |
| 08 (A) | ~1,740 | 3 | 2 | 1 | 0 | 0 |
| 09 (C) | ~3,120 | 7 | 8 | 2 | 0 | 0 |
| 10 (A) | ~420 | 0 | 0 | 0 | 0 | 0 |

Em-dashes appear only in box titles ("Through the Mirror — why…") and as empty
table cells. Hedging is not a problem: the "about"/"roughly" in 09 sit on real
estimates.

**Voice consistency.** All three drafters use the same register: short declaratives,
second person, contractions, dry asides. The differences are small:

- **B** opens all three Facet chapters with the same construction, and starts rules
  entries with a flavor line.
- **C** carries the densest aphorisms, and the 07 tradition paragraphs are lifted
  almost verbatim from the Lean appendix's more ornate register.
- **A** is the most restrained.
- British and American spellings are mixed (B and C).

---

## Findings, ranked

### Major

**LIC-1 · Major · Talents derived from non-SRD WotC material**
*Location:* 03 L224–226 *Tough*, L266–268 *Cleaving Blow*, L292–294 *Ambush*,
L308–314 *Bulwark*/*Deadeye*; 04 L182–184 *Field Medic*, L186–198 *Gadgeteer*,
L246–250 *Infuse Item*, L306–308 *Clockwork Companion*; 05 L231–235 *Beast Heart*;
03 L193/L195 *Dueling*/*Protection*; `docs/DESIGN_facets_d20.md` L118.

*Evidence and likely source:*

| Book text | Likely source | In SRD 5.2.1? |
|---|---|---|
| *Tough*: "hit point maximum increases by 2 for every level" | 2024 PHB Tough feat | No. SRD 5.2.1 origin feats are Alert, Magic Initiate, Savage Attacker and Skilled |
| *Deadeye*: "ignore half cover and three-quarters cover, and attacking at long range doesn't give you disadvantage" | Sharpshooter | No |
| *Bulwark*: "has its speed drop to 0" on an opportunity-attack hit | Sentinel | No |
| *Cleaving Blow*: crit or drop to 0 → another attack | Great Weapon Master | No |
| *Ambush*: advantage against creatures that haven't had a turn, plus extra damage | Assassin's Assassinate | No; the SRD rogue subclass is Thief |
| *Field Medic*: healer's kit heal of 1d6 + … once per rest | Healer feat | No |
| *Beast Heart*: CR 1 forms, "temporary hit points equal to 3 × your level" | Circle of the Moon | No; the SRD has Circle of the Land |
| *Infuse Item*: +1 weapon, +1 armor, stored-spell trinket | Artificer infusions | No |
| *Clockwork Companion*: bonus-action-commanded construct, 5 × level HP, 1d8 + PB | Artificer Steel Defender | No |
| *Dueling*, *Protection* | SRD **5.1** fighting styles | Not in 5.2.1's fighting-style feats (Archery, Defense, Great Weapon Fighting, Two-Weapon Fighting) |

DESIGN L118 says "Tough is one in both", which is very likely wrong.

*Why it matters:* BRIEF §4.1 says "we never pull from non-SRD WotC material
(non-SRD subclasses…)". CLAUDE.md's copyright policy also forbids deriving
mechanics from proprietary works. The owner's later note (similarity is fine, only
licences matter) lowers the legal stakes: the wording is original and mechanics
aren't copyrightable. But the book's own contract is broken, and the DESIGN record
says otherwise.

*Fix:* get an owner ruling on whether mechanical resemblance is acceptable. If it
is, amend BRIEF §4.1 and correct DESIGN L118. If it isn't, retune the numbers and
triggers of these nine. Either way, add the SRD 5.1 attribution line next to 5.2.1
if *Dueling* and *Protection* are kept as SRD material. Verify the 5.2.1 feat list
against the PDF before acting; this audit worked from memory of it.

**ORG-1 · Major · *Martial Training* says two different things, and both chapters say they're the same**
*Location:* 04 L204–206; 05 L205–207; 04 L166; 05 L173.
*Evidence:* Mind: "proficiency with martial weapons, and training with medium armor
and shields." Soul: "proficiency with martial weapons, and training with heavy
armor." Yet 04 L166 lists it as "on the Soul menu too", and 05 L173 adds "and read
the same there". The yaml (L118) makes the split deliberate ("one more step of
armor").
*Why it matters:* a reader is told outright that the two entries are identical. It
also leaves open which version a cross-Facet Body character takes, though that is
moot for Body.
*Fix:* keep the Facet-dependent rule, but write it once: "one more step of armor
than your Facet gives: Mind gains medium armor and shields, Soul gains heavy armor".
Put it in both entries and drop "read the same".

**ORG-2 · Major · Shared talents are re-printed on every menu ("legislate once" broken)**
*Location:* ASI 03 L171 / 04 L170 / 05 L177; *Expertise* 03 L183 / 04 L174;
*Magic Initiate* 04 L200 / 05 L201; *Extra Attack*, *Potent Cantrips*, *Wider Study*
in 04 and 05; *Thaumaturgy* and *Invocation* each also summarised in 02 and 07.
*Evidence:* the texts are nearly identical but not quite. 03's ASI adds "It is on all
three menus…", and 03's *Expertise* says "also on the Mind menu" where 04's doesn't
mention Body. ORG-1 is what this pattern produces.
*Why it matters:* STYLE_GUIDE law 2 says to define a rule in one home and point
everywhere else. Every future rules edit has to be made in two or three places, and
the tests check the yaml, not the prose.
*Fix:* add a "Shared Talents" section, in 02 or at the head of 03. The menus then
list the names with "(shared, Chapter 02)". Or add a prose-equality test for shared
entries.

**ORG-3 · Major · Cantrip progression stated three ways**
*Location:* 07 Table 7–2 (Cantrips column, keyed to **caster level**); 07 Table 7–4
("2; 3 from 4th level; 4 at 10th (by character level)"); 04 L220 and 05 L197 ("three
from 4th level, four at 10th", with no key).
*Evidence:* a Body character who takes *Invocation* at 2nd is character level 4 but
caster level 3. That gives 3 cantrips by Table 7–4 and 2 by Table 7–2.
*Why it matters:* the reader gets two answers from the same chapter.
*Fix:* choose one key, state it once (Table 7–4), and delete the Cantrips column
from 7–2 or re-key it.

**CAN-1 · Major · Divination has been made an Invocation domain and presented as canon**
*Location:* 07 L125–127, L151, L360; Table 7–6 (Oracle = Fate + Divination);
05 L100.
*Evidence:* "The names and territories below are the game's twenty-one canon domains
… Divination is the one domain on both lists." The canon catalog
(`Appendix_Magic_Domains.md` L286) has "**Divination** *(Thaumaturgy)*" only. The
book also opens the six prismatic domains from 1st level (L129), against canon's "No
character starts with one". That change is openly flagged, which is fine, but it
still needs a ruling. DESIGN §7 records Divination as a drafter decision, not an
owner ruling.
*Why it matters:* this is the magic-lore iron law ("never invent… when unsure, ask").
A shared domain changes the fiction of both traditions, and Lean's appendix now
disagrees with d20.
*Fix:* owner ruling. Either accept it (and say in 07 "In Facets d20, Divination is
also open to Invokers") or rebuild the Oracle on a Fate plus Soul-domain pair. Also
reword L125 so it doesn't claim the table *is* canon.

**CAN-2 · Major · Invented facts about the recurring cast**
*Location:* 02 L166 and L178; 06 L115 and L131; 03 L326; 08 L144–148.
*Evidence:*
- Mordai: "the district he patrolled for **eleven years**"; "He is not [one of
  yours]" after a Watch-trained mugger.
- Mordai's two Drives, which are new canon statements about the character.
- Zulnut: "a disciple of **a wandering teacher who moved on**"; his Specialty,
  "noticing the exact moment a room's attention shifts off him".
- The alley leader has "Watch training, years ago", which ties an NPC to Mordai's
  institution.

*Why it matters:* CLAUDE.md's iron law says never invent backstory for established
characters, and to ask first. These details are in character and harmless, but they
are new facts.
*Fix:* ask the owner to confirm them. Otherwise cut "eleven years" to "for years",
drop "who moved on", and keep the Drives, flagged for confirmation.

**ORG-4 · Major · No character sheet, glossary, index or talent finder**
*Location:* the whole tree; compare `player_handbook/Appendix_Character_Sheet.md`,
`Glossary.md` and `Index.md`.
*Evidence:* a Facets d20 character needs fields no SRD sheet has: Facet, talents by
level, signature, origin talent, Drives ×2, Sparks, Specialty, domains, caster level.
Talents are spread over three chapters with no A–Z list. Signatures appear in three
places. SRD look-ups ("Look up what they do in the SRD 5.2.1", 07 L183; equipment,
02 L86) give the landing URL but never the SRD section.
*Why it matters:* STYLE_GUIDE law 9 treats finding aids as first-class content. A
player with only this folder can't write the character down.
*Fix:*
- Add `11_Character_Sheet.md`, even a plain Markdown form.
- Add an all-talents index table (name · Facet(s) · tier · origin · chapter) and a
  short glossary: Bloodied, caster level, d20 test, Drive, Heart die, minion,
  origin, preset, signature, Spark, Specialty, studied target, tier.
- Name SRD sections in pointers, e.g. "SRD 5.2.1, *Spells*".

**PRO-1 · Major · Aphoristic kickers and not-X-but-Y reframes (about 70)**
*Location:* the whole book, densest in 07 and 09 (see tally).
*Worst examples:*
- 08 L106–108: "Long fights are rarely long because they are interesting. They are long because…" and "None of it touches the part you came for: your turn, your roll, your idea." (a reframe and a triad kicker in one box)
- 07 L3: "You don't get magic from a class, you get it from a talent. And you don't get a class spell list, you get two **domains**…" (two reframes back to back), then L5 "That is the whole spin."
- 04 L5: "But you aren't a caster because you're Mind. You're a caster because you took the *Thaumaturgy* talent."
- 09 L69: "A fight is over when its question has been answered, not when the last hit point is gone."
- 09 L120: "Two sums you can do in your head are more honest than one number that's quietly off."
- 09 L192: "A character whose want has changed is a character who has grown, and that's the best thing that can happen at a table." (inflated)
- 09 L212 "It's a guide, not a rule." / L218 "a feel, not a formula" / L41 "That's a scene, not a stall." (three "X, not Y" in one chapter)
- 06 L3 "None of it is decoration."; 06 L222 "A person is moved by what you offer them, and the check is how well you offered it."
- 05 L5 "None of it is a fence."; 05 L333 "Half druid, half oracle, and nobody needs to decide which."
- 04 L332 "It doesn't look like any SRD class, and it doesn't have to."
- 07 domain blurbs: "It nudges; it never compels." / "It alters; it doesn't create from nothing." / "Not fire, not lightning." / "Not healing." / "Never people, never undead or constructs." (a negative-definition formula, five times)

*Why it matters:* the owner's bar is that no one could tell it's AI, and these are
exactly the tells the 2026-07-11 pass thinned. Each one is fine alone. Together they
set a rhythm.
*Fix:* light de-patterning only. Keep roughly one per section where it carries a
rule (06 L125 "Good with people is not a Specialty" earns its place). Cut or flatten
the rest, especially section-ending kickers. Keep the vignette flourishes, such as
08 L162, "less time than choosing dinner".

### Minor

**PRO-2 · Minor · Identical openers and flavor inside rules (drafter B)**
The chapter openers repeat one construction. 03 L3: "Fighters, rogues, barbarians,
monks. People who solve problems by…". 04 L3: "Wizards, investigators, loremasters,
tinkers. People who solve problems by…". 05 L3: "Priests, druids, oracles, the
oathsworn. People who solve problems through what they believe, what they feel, and
who will stand with them."

Rules entries open with a flavor line:
- 03 L30 "You have a reserve most people never find."
- 03 L177 "you shout in time"
- 03 L230 "Nothing is slowing you down."
- 04 L30 "You look at a creature the way other people read a page."
- 04 L226 "say exactly the wrong thing at exactly the right time"
- 05 L30 "You know what to say, and when."

Rules text also carries humor: 04 L300 "If they are arguing about it, they aren't."
STYLE_GUIDE law 3 keeps flavor and humor out of rules text. *Fix:* vary two of the
openers, and move flavor lines to the preset "Play it like" slots or cut them.

**PRO-3 · Minor · The "your own build is just as legal" motif, six times**
README L7, 01 L11, 02 L5 and L23, 03 L7 and L340. *Fix:* say it firmly once, in 02,
and cut the others to a clause.

**PRO-4 · Minor · Mixed spelling**
British: "recognise" (05 L68), "duellist" (04 L5), "centrepiece" (09 L116), "favour"
(09 L230). American elsewhere: "armor", "recognize" (06 L64, L74), "color". *Fix:*
use American, as the rest of the project does.

**PRO-5 · Minor · A copy-paste stumble in a designer note**
04 L326: "At 1st level, … deal about what an SRD rogue deals. At 5th, they deal about
what an SRD rogue deals." *Fix:* give the 5th-level number, or merge the two
sentences.

**ORG-5 · Minor · Example formatting drifts from `phb-examples.md`**
- 08 puts dialogue in quotation marks (L116 onward); 02, 03 and 06 don't.
- The MM appears in italics (08 L124 "*(Behind the screen: … The MM has already decided…)*", L152 "*The MM rolls two attacks…*"). The convention says the MM "never appears in italics".
- Parentheses carry mechanics (08 L136 "(The MM rolls his morale save…)", L158), when they are reserved for the MM's human asides.
- Dice notation mixes "d20 + Dex (+3)" with "d20 + 5".

*Fix:* one convention book-wide. Put mechanics after `→`.

**ORG-6 · Minor · "Talents never change these" is false**
02 L43: "Your Facet owns every number that matters for balance. Your talents never
change these." 01 L11: "…Nothing else does." But *Martial Training* changes armor
and weapons, *Tough* changes HP, and *Iron Mind* adds a save. *Fix:* "Talents can
add to these, but never replace them."

**ORG-7 · Minor · 01 claims to list every change but misses some**
01 L3 says "If something isn't on it, it works the way you're used to." Missing:
- milestone levelling with no XP (09 L198)
- no component pouch (02 L96, 07 L115)
- starting kit or 100 gp (02 L86)
- Specialty makes routine checks automatic (06 L123)
- Recharge rolled once per enemy half (09 L65)

*Fix:* add a line for each, or soften the claim.

**ORG-8 · Minor · Combat rules homed outside the combat chapter**
The stunned-boss rule is at 03 L258 and 09 L63 but not in 08's Bosses section
(L90). Recharge timing appears only in 09 L65. *Fix:* put both in 08 and point to
them from 03 and 09.

**ORG-9 · Minor · A dangling "it"**
07 L38–40: after the *Magic Initiate* paragraph, "When you take it, you gain:" now
grammatically refers to Magic Initiate. *Fix:* "When you take a caster talent, you
gain:", or move the Magic Initiate paragraph after the list.

**ORG-10 · Minor · Chapter 06 mixes creation and play**
Backgrounds are step 4 of creation. Sparks, social play and travel are play rules
used in every session. The creation steps also jump 02 → 06 → 03–05 → 02.
*Fix:* consider splitting 06 into "Backgrounds and Drives" (placed before the Facet
chapters or folded into 02) and "Sparks and Social Play" (placed next to 08).

**ORG-11 · Minor · Incomplete worked characters**
- Zulnut's custom background (06 L115) omits the origin talent and the ability
  increases, the two steps the procedure just told the reader to do.
- Zulnut never gets scores, HP or AC.
- Zahna is never built, yet 08 L142 gives him "Int (+3)" and a Specialty.
- The only full caster example (07 L119) is an anonymous "she".

STYLE_GUIDE's FoO commitments say the cast does the worked arithmetic. *Fix:* finish
Zulnut, and turn 07's Priest example into Zahna's Thaumaturge build (Inscription is
his canon domain).

**ORG-12 · Minor · Label and numbering nits**
- Box titles vary: "Reading the cards" (03 L42), "Reading the entries" (03 L138),
  "Reading the Entries — backgrounds" (06 L22).
- README uses "Table 0–1".
- Table 10–4 has a blank header cell.
- 03 Table 3–2 puts "(5th level)" inside the talent name column.

Table numbering is otherwise sequential and consistent, and all "Table N–k" and
"Chapter NN" cross-references resolve.

**ACC-1 · Minor · Jargon used without a definition or pointer**
- "d20 test" (05 L30, L193, L283) is never defined; it is the SRD 5.2.1 umbrella
  term for attack rolls, ability checks and saves.
- "Bloodied" is used in 03 L280 (*Survivor*) with no pointer to 08.
- "Hit Point Dice" (06 L232) sits beside "hit dice" (02 L131).
- "Magic action" (05 L185) comes before 08 lists it.
- "Heart die" is fine.

*Fix:* define these on first use or in the glossary (ORG-4).

**ACC-2 · Minor · "Thaumaturgy" is two different things**
It is the Mind tradition and also an SRD cantrip, and the cantrip sits on two
*Invocation* lists (Resonance and Presence, 07 L232 and L263). The clash is
explained only at 07 L183. A new player will read "an Invoker casting Thaumaturgy"
as a rules error. *Fix:* add a note at the first mention in 02, or italicise the
spell everywhere (*thaumaturgy*).

**ACC-3 · Minor · The Quick Reference has no magic**
10 correctly restates only what the chapters say; the house rule is met, and nothing
in it is new. But casters' most-used look-ups are missing: spell save DC and attack
bonus (07 L45), prepared count (Table 7–4), a pointer to Tables 7–2 and 7–3, and the
ritual rule. *Fix:* add a short "Magic (Chapter 07)" block.

**LIC-2 · Minor · CC BY 4.0 "indicate changes"**
The footer is WotC's requested statement word for word (BRIEF §4.6), in the README,
all ten chapters and the yaml header. CC BY 4.0 §3(a)(1)(B) also asks you to
indicate whether the material was modified. The README L55 phrase "Material adapted
from…" comes close. *Fix:* add to the README Legal section: "The SRD material has
been modified: rules were adapted, reorganised and combined with original
material." The per-chapter footers can stay as they are.

**LIC-3 · Minor · Trademark-adjacent phrasing**
README L3: "if you have played the fifth edition of the world's most popular fantasy
roleplaying game". No mark is used, but the wink invites an implied association, and
"most popular" is a claim about a third party's product. The title "Facets d20" is
fine ("d20" alone is generic; WotC's mark is "d20 System" and its logo), but never
add "System" or the logo. No "D&D" or "Dungeons & Dragons" appears anywhere, and no
Pathfinder or Paizo text was found. "Oracle", "Investigator" and "Loremaster" are
generic words that happen to be Pathfinder class names; no text is shared. *Fix:*
"if you have played a game built on the SRD 5.2.1".

**CAN-3 · Minor · "An earlier playtest" overstates the evidence**
06 L179: "An earlier playtest of this game let Sparks pile up…". That playtest
(`playtest/01_thornwall_undercroft/`) was *simulated*, and the project has had no
human table (fun audit, 2026-09). *Fix:* "Earlier drafts of this game let Sparks pile
up; in simulated play, players saved them…", or just give the reasoning.

**CAN-4 · Minor · A vague canon pointer**
07 L125: "the Magic Domain Catalog appendix of the core book". There are three
rulesets, and that appendix
(`player_handbook/Appendix_Magic_Domains.md`) is written for Lean's 2d6 (Harder
steps, *Wider Domain*). *Fix:* name the file, and say that its scope and difficulty
rules don't apply here.

**CAN-5 · Minor · "Wandering Disciple" moved from class to background**
In `phb-examples.md`, Zulnut's *Wandering Disciple* is a custom **class** (Unarmored
Discipline + Athlete, signature Ghost). Here it is his **background** name (06
L115), and his build is Martial Arts / Unarmored Defense / Cunning Action / Still
Water. Adapting him for d20 is reasonable, but the reused name now means two
different things. *Fix:* note the d20 build in `references/phb-examples.md`, or
rename the background.

---

## Passes (checked, no finding)

- **MM terminology:** "Mirror Master (MM)" is defined in the README, 01 and 09. There
  is no GM, DM, game master or dungeon master anywhere.
- **Setting lore:** no Shattered Origin, Val'loh, Thornwall or Millhaven names. The
  alley vignette says only "the archive", consistent with the established Thornwall
  arc, and it comes before Millhaven, so Mordai's shoulder scar isn't due yet.
- **Cast personalities** match `phb-examples.md`. Zahna is oblivious and pedantic
  (08 L146, L152; 04 L7). Mordai is direct ("I don't dodge. I stand there."). Zulnut
  is lazy and has a cigarette, lit from a lamp the MM had already described (the
  ground rule holds). Everyone is human, and Lineage gets one line (02 L193).
- **Worked numbers:** Mordai's HP 14 and AC 19, the Priest's DC 13, and the Table 9–1
  example sums all check out.
- **Quick Reference (10):** every line traces to a chapter statement, and it
  introduces no new rule.
- **Tables:** numbered and sequential (2–1 to 10–4); every "Table N–k" citation
  resolves.
