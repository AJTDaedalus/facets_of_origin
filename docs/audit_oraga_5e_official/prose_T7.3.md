# T7.3 prose voice pass: chapter 09 (The Snakes)

*Worker, 2026-10-03. Covers SNAKES-10 (option b), SNAKES-11 and FRONT-7's 09 sites. Only `09_The_Snakes.md` was edited. Every site was found by quoted text. The edits change wording only: no fact, number, DC, budget, rule, read-aloud box or line of canon speech was changed. Nothing is committed and the lint baseline was not re-run.*

## Metrics

`python conversions/dnd5e/oraga_night/tools/lint_5e.py --report --file 09_The_Snakes.md` (DM prose):

| metric | target | before | after |
|---|---|---|---|
| hard hits | — | 8 (conversion_talk 3, narrator_voice 4, pcs 1) | 0 |
| words | — | 16,910 | 16,805 |
| mean words per sentence | ≤ 19 (don't shorten further) | 13.82 | 13.71 |
| sentences over 30 words | ≤ 12% | 5.81% | 5.76% |
| em dashes per 1,000 words | ≤ 8 (keep about 3–8) | 9.34 | 7.20 |
| paragraphs over 120 words | ≤ 3 | 11 | 0 |
| "the players" (S2) | 0 | 4 | 2 |
| "player character" | — | 66 | 3 |
| "you" (info only) | — | 43 | 16 |
| "perhaps" (S25) | 0 | 1 | 0 |
| rhetorical questions (S27) | 0 | 1 | 1 |
| "not X but Y" / ", not" | — | 16 | 15 |

Whole file, raw grep: "player character" 72 → 2 lines (one more is split across a line break), em dashes 223 → 184.

**What the remaining counts are.**
- **"the players" (2):** both mean the people at the table: "Read this before the first round; the players need it too" (S3) and "Let the players see that it *needed* calling back" (S14). STYLE allows both.
- **"player character" (3):** each one separates PCs from NPCs. "only a player character can make it" (the nursery sale), "unless a player character tells them" (S7), and "The duelists hold Provocation until a player character has taken a turn" (S9, where the duelists are taking turns too).
- **"you" (16):** all are the DM ("you pick which", "your call", "you roll who", "you narrate who"), a generic "the way you would call a dog", or quoted in-world speech ("just the two of you", "bring your cousin's excuses").
- **rq (1):** a false positive. It is the knife's quoted question, *who eats off the second plate?*.

**Commands.** `lint_5e.py --check` → OK (0 problems). `bestiary_check.py --quiet` → 25 blocks + 3 Nastier, 0 mismatches. `pregen_check.py --quiet` → 5 pregens, 0 issues. `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 159 passed.

**Numbers check.** A script compared every `DC n`, `n XP`, dice expression, `n GP` and numeral in the file before and after the pass. DC (50), XP (83), dice (17) and GP (6) are identical, in order. The one added numeral is the "11" in the new comment `<!-- INVENTIONS #11 … -->`. No read-aloud line changed. The only `> *` lines that changed are inside DM Notes.

## Changes

- **SNAKES-10 (b), the *Walk into it* blocks:** all six now use the official voice, for example "**Walk into it.** The characters can follow the coat, or be in the service doorway…". The *Turn it* imperatives were converted the same way: "Giving Callun what she wants quiets the line", "An honest judgment Kovaun can file turns it", "If Agenda 3's 'understanding' is delivered…", "A party that helps Essin keep Vorlain sober and unbaited has Essin in its debt…". Draunel's inline **Snake on snake.** now starts its own paragraph, like the other five lines.
- **Party "you" → the characters:** "at midnight you are standing" → "they are"; "walk back inside with your dignity… still yours" → "the characters… their… theirs"; "more than you do" → "than the characters do"; "Going back the way you came" → "…they came" (the TODO-Q14 comment quoting it was updated to match); "your invitation's good standing" → "Losing costs the party the east wing… and its invitations' good standing"; "land on you — both principals' next attacks target you" → "land on whoever is in between: … target that character" (S1, and the same in S9); "nobody else in the palace will tell you" → "the characters"; "Two hundred people are behind you" → "behind the characters"; "get yourselves and whoever you are carrying" → "the characters and whoever they are carrying"; "you kept your head" → "the party kept its head"; "ask you, embarrassed" / "that you will say nothing" → "the character"; "proof you speak for her" → "proof of speaking for her"; "*…you pay now.*" → "*…the party pays now.*"; "hold Vorlain… yourselves" → "in the party's own hands"; "no longer includes you" → "the party"; "knowing what you are handing" → "knowing what it is"; Heroic Inspiration "you have it or you don't" → "works as the SRD says: a character has it or doesn't".
- **"player character" → "character"** at every subject site where nothing separates PCs from NPCs, including all trigger lines and the DM Note "how it plays" lines. The 30 *Adjusting the Encounter* labels became "*Three characters:*" and "*Five characters:*", matching "three characters, five" in *Running the Snakes*. Table IX–3's header "(four 4th-level PCs)" became "characters" (the `pcs` hard hit). "the players are standing" / "a player's agenda" / "the Agenda 1 player" / "Every time the player turns" / "Agenda 8's player" / "Agenda 1's player" / "the players' proof" → character forms. "a player pulls a thread" → "a character pulls a thread".
- **SNAKES-11, every listed site:** "which is worse" cut. "Let the table sit with it." cut. "a debt of a very particular kind" → "his debts are worth having". "the source notes with a straight face" → "He is also the only patron…". "the most frightened armed people… the only ones facing the right way" → "They are frightened and armed, and they are the only guests facing the right way" (keeps the fact that row V states). "The module would prefer…" cut. "It is the whole scene." cut. "*Honest note:*" and "*Honest warning:*" dropped, and "That is the cost of the ending the module least expects… so you can see it coming" → "…and the least likely of the three endings. When it starts to go that way, reach for an out." "A second leader is a cliff, not a step" → "makes the fight far harder at once". "That is the point." cut (S4). "— which, at this hour of this night, is not nothing" cut. "— and the module notes, without comment…" cut after "clean". Also cut: "That is deliberate:" (S3 budget) and "and the card is written that way rather than pretending otherwise" (S2).
- **FRONT-7 and other conversion or narrator talk:** "which the source leaves to the DM's invention… This edition names the three below, as inventions for the owner's review" now reads "…three other irons in tonight's fire. A Draunel never brings one plan to a Boranis party." The owner flag survives as `<!-- INVENTIONS #11: the three other irons below are inventions, for the owner's review. -->`. "the source's plain fact" → "a plain fact". "The module does not say why…" → "Why… is never said." "(the module never says who did)" → "(who did is left open)". "something the module does not explain" → "something nobody can name" (echoes "Instruments nobody can name" in the same card). "what the scorch marks mean, the module does not say" → "is left open". "the table this module expects" → "the table the cards expect". The three "(canon)" provenance tags (Agenda 3 iron; Vorlain hauling guests, twice) were removed. They appear in no other chapter, and the iron list is now covered by the INVENTIONS comment.
- **Long paragraphs (11 → 0):** each split at a natural turn. The splits: "None of them planned…", S3 budget ("With the captain drawn in…"), S3 tactics ("The captain spends…"), S3 endings 1 ("Fought to the last Blade…") and 2 ("Or a better offer…"), S6 where-and-when ("Accepting is walking in…"), S6 enemies ("A quiet word is not supposed to be a fight."), the S7 clock ("*(The knife never learns…)*"), the S9 clock ("**Full:**"), and the S14 enemy block ("*Budget:*", "Idle, its offense drops…").
- **Em dashes (9.34 → 7.20/1k):** about 15 mid-sentence pairs became commas, colons or parentheses, for example "no papers (there are none anywhere), but", "If the night breaks (and after midnight it does)", "Ask them (no check), and", "The slingers aim at hands (Maiven's sling makes a creature drop its weapon)". Dashes stay in headings, box labels, numbered-ending labels, budget lists and a few places where they read naturally.

## Keeps

- Every read-aloud box, unchanged, including its "you".
- Canon and in-world speech: "just the two of you, and a friend of mine…", "bring your cousin's excuses", "*who eats off the second plate?*", the DM-to-player lines "It's locked on you" / "It's drifting".
- Lines that earn their place: "Remember them like this", "Essin, alone, which he never is", "the polite is the threat", "Possible, and printed above so nobody chooses it by accident", "He will be back; he always has a second way".
- Functional contrasts: "facing the palace doors, not the gates", "to check the arithmetic, not to act on it", "the clock, not the roster", "fights to leave, not to win", "detain, not to kill", "The reinforcements never change; they are the point", the run-in **Not a scheme — a panic with knives.**
- The DM-facing "you" in the S14 paragraph "Say so with your whole table manner".
- Imperative *Outs* labels ("Let her go.", "Name Essin.", "Walk away.", "Stop interfering."). They are option names, and the TODO-Q14 comments quote them.
- The phrase "Essin keep Vorlain sober and unbaited" is still in *Turn it*, so INVENTIONS #68's source quote still matches as a substring. The Circle's "That sale is the only way the Circle ever learns what is in the east wing" is unchanged.

## Skips

- I did not shorten sentences. The mean was already 13.8, and the brief said not to go lower.
- I did not rewrite "not X but Y" further (16 → 15). What remains carries rules or facts.
- I left italic emphasis in DM prose ("which a character can *be*", "*for everyone*"). It is a STYLE "Emphasis" issue, not part of this voice brief.
- S14's Inspiration "to the first player who tries to distract it" stays as written, because hint 4 rewards the person's attempt.

## Sample pair (S2, *The Service Corridor Job*)

> **Before:** …and on anything loud — a shout, a thrown body, a spell anyone past the wall could hear (your call). **Full:** the honor guard arrives, and *both sides lose*. … **Say this to the table out loud at the top of the scene.** It is the whole scene.
>
> *Honest note:* the party will very likely win the fight. The difficulty of this scene is the clock, not the roster, and the card is written that way rather than pretending otherwise. Do not add a second leader to "fix" it; that makes the fight much harder, not a little.
>
> **After:** …and on anything loud: a shout, a thrown body, a spell anyone past the wall could hear (your call). **Full:** the honor guard arrives, and *both sides lose*. … **Say this to the table out loud at the top of the scene.**
>
> The party will very likely win the fight. The difficulty of this scene is the clock, not the roster. Do not add a second leader to "fix" it; that makes the fight much harder, not a little.
