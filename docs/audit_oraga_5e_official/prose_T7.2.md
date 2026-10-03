# T7.2: Prose voice pass, chapter 05 (The Longest Night)

*Worker, 2026-10-03. Findings: NIGHT-13, NIGHT-14, and FRONT-7's 05 sites, including both "*(New in this edition.)*" tags. Only `05_The_Longest_Night.md` was edited. Every site was located by quoted text. The pass changed wording only: no fact, number, DC, rule meaning, read-aloud box or canon speech was changed. Calibration follows the G1 adjustment: em dashes are kept at about 3–8 per 1,000 rather than the pilot's 1.5, so a few atmospheric dashes stay in, and sentences are split without atomizing the prose.*

## Metrics

From `python conversions/dnd5e/oraga_night/tools/lint_5e.py --report --file 05_The_Longest_Night.md` (DM prose):

| metric | target | before | after |
|---|---|---|---|
| words | — | 11,515 | 11,364 |
| mean words per sentence | ≤ 19 (aim 14–19) | 16.86 | 14.78 |
| sentences over 30 words | ≤ 12% | 11.17% | 6.50% |
| em dashes per 1,000 words | ≤ 8 (aim 3–8) | 15.02 | 3.43 |
| paragraphs over 120 words | ≤ 3 | 16 | 0 |
| "the players" (S2) | 0 | 16 | 0 |
| "player character" | — | 33 | 7 |
| "you" (info) | — | 29 | 24 |
| "perhaps" (S25) | 0 | 0 | 0 |
| rhetorical questions (S27) | 0 | 2 | 0 |
| "not X but Y" / ", not" | — | 17 | 15 |
| hard hits (conversion talk 3, narrator 2) | — | 5 | 0 |

## Verification

- **Numbers script** (before = `git show HEAD:…/05_The_Longest_Night.md`): every `DC n` is unchanged, and so is every dice expression. One numeral is gone: the "5" in "A 5e table will reach for the spell list", now "A table will reach…" (conversion talk). No numeral was added.
- **Read-aloud:** all 9 indented italic read-aloud lines are byte-identical. Canon speech is untouched ("Corval. The stairs.", "the third sconce — turn it — NOW", "Take her. The gate. Don't stop.", the rite, the Epilogue).
- `lint_5e.py --check`: OK (0 problems).
- `bestiary_check.py --quiet`: 25 blocks + 3 Nastier, 0 mismatches.
- `pregen_check.py --quiet`: 5 pregens, 0 issues.
- `python -m pytest conversions/dnd5e/oraga_night/tools -q`: 159 passed.
- No re-baseline. No commit.

## What changed

- **NIGHT-13, how the party is named.** Every "the players" that meant the characters now reads "the characters" or "a character". That covers "The characters carry history in their arms", "Any character at his side", "makes the characters the most interesting people", "the characters his only trusted witnesses" and "Let it be the characters". Where "the players" meant the people, it became "the table" ("where the table can see it", "when the table asks", "the hints that tell the table"). "The party" became "the characters" in most running text. "Player character" was cut from 33 to 7. The ones kept tell PCs apart from NPCs: "Roll Initiative only for the player characters" (vs Vell and the Radiant), "If no player character is at the Crossing", "one player character between them" (Raunu), "a player character's choice opens it", the ⟨A player character dies⟩ label, and "never kills a player character". **Tables V–2, V–4 and V–5** no longer say "you" to the player: "he tells the character exactly what to touch… whatever the character studied", "The character's own, or a *House Seal*…", "DC 13 for a character who studied the wards, DC 18 otherwise", "behind the party", "Slower for the characters". "No roll for Agenda 6's player" became "no check for the character with Agenda 6". The sidebar label "Players who attack Vell" became "Characters who attack Vell". Nothing outside the chapter cites that label.
- **NIGHT-14, rhythm.** These fixes follow the audit's text:
  - "**The lights die** mid-word." (the "Not blown out — *drunk*" doublet is cut; the box keeps its image).
  - "he does not startle, and he does not finish the sentence".
  - "**…cannot be defeated by force tonight. Nothing in the palace can do it, spells included.**"
  - "Nothing short of the leash ends his hunt."
  - "Without a patron, the truth only exposes them."
  - "— which is exactly as it should be, because they will choose it" is cut.
  - Principle 2 is split into a rule paragraph, a sub-list of the three ward options and a Root paragraph.
  - The dais bullet is split at "*(At his side…*". The east wing, the looters, the lower garden, the river gate, the Radiant's and the Hollow's Fractures, the trap sidebar, ⟨They save Raunu⟩, ⟨The child is taken⟩, ⟨They expose the truth⟩, Void the contract and the two Crossing sidebars were each split at a natural turn.

  Elsewhere, em-dash and semicolon chains became sentences, colons or parentheses.
- **FRONT-7 and narrator talk.**
  - "And a fourth, for this edition:" is gone. The list now opens "Four principles:" and runs 1–4 unbroken, so "principle 2" cross-references still resolve.
  - Both "*(New in this edition.)*" tags are deleted.
  - "This edition gives them full stat blocks" → "The three have full stat blocks".
  - "The module states this and does not explain it" → "Nothing in this adventure explains why".
  - "in the history this module keeps" → "in the default history".
  - "From here the module cannot script" → "Nothing from here on can be scripted".
  - "the module trusts the table to notice" → "leave it for the table to notice".
  - "the module deliberately does not name the forces" → "nothing here names the forces".
  - "where the module keeps its tone promise" → "This Movement keeps the adventure's tone promise".
  - "the module expects the margin…" → "The margin… is meant to be made of exactly this".
  - "the module refuses to leave it there, and so should you" → "do not leave it there".
  - "the module holds that line" → "that line holds".
  - "this module's spine" → "the adventure's spine".
  - "all the module knows" → "all this adventure says".
  - The remaining "the module" sites now read "this adventure".
- **Winks and self-praise cut.**
  - "The module would prefer somebody competent went with her."
  - "and the module notes, without comment, which kind of night the table chose to have"
  - "and a very good one"
  - "and the module blesses it without reservation"
- **"Not X but Y" undone where it was rhythm only.** "his kills are not showmanship but **liturgy**" → "His kills are **liturgy**". "that is not a divergence from history — it is history" → "that is history, not a divergence from it". "That is not a dead end. It is a campaign frame" → "That is a campaign frame, not a dead end". "Invoked: not ferocity — … — but **sincerity**" → "Invoked, what reaches him is **sincerity**, not ferocity."
- **Prompts and cross-references.** "*what do you do?*" and the Epilogue's closing question are now quoted DM-to-player speech, which clears S27. Italic section pointers inside asides (*Down, Not Out*, *Knives in the Dark*) became quoted names, per the style sheet.

## Kept on purpose

- Every read-aloud box, and all canon speech.
- **Atmospheric dashes**, about 39 in the chapter:
  - "three gray masks stay on"
  - Raunu's voice "— flat, carrying, instantly obeyed —"
  - "not running, *arriving*"
  - the Wept's held round
  - "Each of the three is still a person — that is the terrible engine of them —"
  - the Hollow's "belonging, after a life of nothing"
  - the river gate "Unlocked — someone saw to it" and "is gone east with the mist"
  - the mask "A person's face — ordinary, and tired…"
  - "*watched* — by forty blades"
  - the pursuit "— with Vell… as patron"
  - the crystal "— a second small thing"
  - the looters "— just a blade and the willingness"
  - Maiven "— a border fighter"
  - "One of them — the Wept, if any character earned it — looks back."
- Box labels, "***Card Sn*** —" pointers and table headers also keep their dashes.
- **Jokes that earn their place:**
  - Vorlain hauling guests out "to everyone's permanent confusion including his own"
  - "Nobody will ever thank them for it."
  - "Vorlain's face when his brother walks out of the smoke is worth the whole divergence"
  - "**A party that only held has won.**"
  - the forty blades who "will spend the rest of their lives not talking about it"
  - "it is the answer to the player who came to this ball wanting a real fight"
- **Functional contrasts:**
  - "a task, not a body count"
  - "a scene-cut, not a unit of time"
  - "Earn it by being clever, not by hitting harder"
  - "prompts, not a menu"
  - "Delay changes how many, not whether"
  - "to escape, not to kill"
  - "Not per attempt; per person"
  - "the aftermath's weather, not an answer"
  - "the default, not a cage"
  - "as a person and not a prize"
  - "**Intimidation never works**"
- **Other keeps:**
  - The **deliberate** old-coin note. It tells the DM the red herring is intended, so it is DM information.
  - The parallel faction list in ⟨They expose the truth⟩.
  - The box labels ⟨They save Raunu⟩ and ⟨The party turns one snake on another⟩. 10 cites the first, and flow.json may cite the second.
  - "*(Not a snake.)*" / "Not a snake."

## Sites skipped or left for others

- No quoted site was missing.
- NIGHT-15 (the contract case), NIGHT-17 (the trap's effect on an errand) and NIGHT-18 (dimensions) are still gated. Their TODO comments are untouched.
- The judgment calls are small additions that clarify without changing meaning:
  - "A trampled guest dies, and a trampled character takes…"
  - "by any of the three endings"
  - "that Blade spends the fight on the retinue. Think of Essin's cousins…" The original dash list is kept, as examples.

## Sample before → after (the Radiant's Fracture)

> **Before:** **The Radiant** *(devotion)*. Truth: he believes, and has believed for a very long time, that revelations were spoken to him and that this errand is holy — his kills are not showmanship but **liturgy**, service that must be witnessed to count as worship. Understand exactly what his Fracture can and cannot do: **the Radiant cannot be turned.** Not from the hunt, not from the errand, not by darkness or doubt — nothing short of the leash ends his night. **His Fracture never ends the hunt.** What he can be made to do is *feel*. Two roads to the guilt: **deny the congregation** — douse the lights, empty the room, turn every back, or a performance that makes a player character the better spectacle; unwitnessed, his service stops counting as worship, and the liturgy collapses into plain ugly work that even he can feel the shame of — he hurries, stops savoring, does it *badly*. Or **plant the doubt** — a priest, a believer, or anyone armed with his tells, declaring the truth to his face: *no god worth the name asks for a stolen child. Whatever spoke to you, it was not the Just One.* On a hit the words lodge. He does not stop, does not answer, does not turn — but guilt gets into the errand like grit into a joint: … Guilt is slow, and slow is hallways — the module expects the margin at the river gate to be made of exactly this.
>
> **After:** **The Radiant** *(devotion)*. Truth: he believes, and has believed for a very long time, that revelations were spoken to him and that this errand is holy. His kills are **liturgy**, service that must be witnessed to count as worship. Understand exactly what his Fracture can and cannot do: **the Radiant cannot be turned.** Nothing short of the leash ends his hunt. **His Fracture never ends the hunt.** What he can be made to do is *feel*. There are two roads to the guilt.
>
> **Deny the congregation:** douse the lights, empty the room, turn every back, or give a performance that makes a character the better spectacle. Unwitnessed, his service stops counting as worship, and the liturgy collapses into plain ugly work that even he can feel the shame of. He hurries, stops savoring, does it *badly*.
>
> **Plant the doubt:** a priest, a believer, or anyone armed with his tells declares the truth to his face: *no god worth the name asks for a stolen child. Whatever spoke to you, it was not the Just One.* On a hit the words lodge. He does not stop, does not answer, does not turn, but guilt gets into the errand like grit into a joint: …
>
> **In the rules:** … Guilt is slow, and slow is hallways. The margin at the river gate is meant to be made of exactly this.
