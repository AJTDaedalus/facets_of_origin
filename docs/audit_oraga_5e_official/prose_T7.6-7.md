# Phase 7: T7.6 (01, 02, 03, 06) and T7.7 (08, 11, README), prose voice pass

*Worker, 2026-10-03. FRONT-7, FRONT-21, CAST notes for 08/11. Model: the T7.1 pilot (LOG, "Phase 7 — T7.1 pilot (chapter 04)"). Every site was located by quoted text. These are wording changes only. A script compared every `DC n`, dice expression and numeral in the seven files before and after, and the multisets are identical. The only numeral tokens that moved were the "5" in "5e": nine uses of conversion talk were removed ("A 5e table", "the 5e shape", "In 5e", "any 5e world", five "in 5e terms") and one was added to README's contributor table ("the 5e text", replacing the hard hit "this edition"). Not committed. Not re-baselined.*

## Metrics

From `lint_5e.py --report --file <name>`, DM prose only. Each cell is before → after.

| file | hard | wps | >30 % | —/1k | paras>120 | "the players" | "player char." | perhaps | rq | not…but |
|---|---|---|---|---|---|---|---|---|---|---|
| 01_Overture | 9 → **0** | 14.57 → 14.24 | 6.1 → 4.61 | 5.95 → 1.93 | 1 → 0 | 11 → 0 | 4 → 1 | 0 | 0 | 10 → 9 |
| 02_The_World_and_the_Night | 0 | 14.90 → 14.22 | 8.56 → 6.62 | **16.78 → 1.69** | **8 → 0** | 2 → 0 | 7 → 0 | 1 → 1 | 2 → 2 | 7 → 5 |
| 03_Masks_and_Agendas | 0 | 14.80 → 14.25 | 7.09 → 5.52 | 8.79 → 0.55 | 0 | 0 | 1 → 1 | 0 | 0 | 3 → 1 |
| 06_Aftermath | 0 | 14.31 → 13.90 | 4.05 → 3.95 | 6.89 → 0.99 | 0 | 1 → 0 | 0 | 0 | 2 → 0 | 2 |
| 08_Handouts | 1 → **0** | 10.80 → 10.36 | 3.21 → 3.12 | 14.97 → 7.81 | 0 | 1 → 0 | 1 → 1 | 1 → 1 | 2 → 1 | 1 |
| 11_Pregenerated_Characters | 0 | 11.48 → 11.23 | 3.72 → 2.43 | 11.16 → 1.56 | 0 | 0 | 2 → 1 | 0 | 6 → 5 | 2 |
| README | 1 → **0** | 18.41 → 17.46 | 6.0 → 3.85 | 10.63 → 1.19 | 2 → 0 | 0 | 1 → 0 | 0 | 0 | 1 → 0 |

The targets are met in every file: mean ≤ 19 words per sentence, ≤ 12 % of sentences over 30 words, ≤ 8 em dashes per 1,000 words, ≤ 3 paragraphs over 120 words, and no hard hits. Sentences were not shortened further, as the calibration asked. The mean moved only where dash chains were split. The 08 word count fell by 16 because the canon Draunel card line is now whitelisted (see below), so the linter skips it.

**Variance from S2/S25/S27 = 0 (explained):**
- **02 "perhaps" (1).** This is in Agenda 2's catch, "seen perhaps four times tonight". Handout 2's canon card in 08 says the same words, so I left both alone to keep them mirrored.
- **02 rq (2).** These are the patrons' own questions inside the agenda text ("*is the man who came back the man who left?*", "is she well, is she free, is she *herself*?"). They are content, not narrator questions.
- **08 perhaps (1), rq (1).** Both are in Handout 2's agenda cards, which are canon card text and were not touched.
- **11 rq (5).** These are the five **Mask** questions. The chapter's design is "one question about it, for the player to answer". They are kept.
- **Remaining "player character" (01, 03, 08, 11, one each).** Each one separates player characters from NPCs: Heroic Inspiration "may give it to another player character" (SRD rule wording), "a player character will almost never be Thenya" (vs. the NPC Thenya), "unless a player character tells them" (the pillar), and "bodyguard to another player character".

## Lint whitelist (tools/lint_5e_allow.txt)

- `01_Overture.md|Designer's note|gated on owner Q4`, as instructed. The note itself, its heading and its "— *the designers*" signature are unchanged, and so is its inner wording.
- `08_Handouts.md|out if he misses the taste. Get him to say anything we could later call an|Handout 2 canon agenda card, in-character "we"`. The `designer_we` hit was Lord Draunel's voice on canon card text ("we" means House Draunel). It is a false positive, and the card must not be edited. **The caller should confirm this entry.**

## What was done

**01 Overture**
- **Conversion talk (FRONT-7, all 8 hits).** "this edition has real fights" → "the night has real fights". Ladder header "The source says" → "Tier". The knack sentence was replaced with FRONT-7's wording ("Where a check depends on a character's training, proficiency in the fitting skill or tool applies…"). "replaces the Sparks of the original edition" was cut, leaving "**Heroic Inspiration** works as the SRD says". "This is the thing the fifth edition adds… the original already states" → "It starts from one fact:". "A fifth-edition party arrives with tools the original never had to answer" → "A party arrives with spells that pry:". "more steel… than the original had" → "The snakes put more steel in the night, and more of it in the dark."
- **FRONT-21 "load-bearing" twice.** The Reading-This-Book entry "Where the module says *the module does not say*, that is load-bearing" became "**Gaps on purpose.** Some answers are left out deliberately (see "What the DM Knows", below)." The "load-bearing sentence" in "What the DM Knows" stays.
- **Party.** "the players" → "the characters" where it meant the characters (read-aloud never names, ⟨If History Breaks⟩, Movements, checkpoint, guest lookup, derailing). It became "the table" where it means the people at the table: invitation for, tell two things, enjoy the party, dice in their hands, the Delay die. "the player characters scheme" and two others became "the characters", as did "two player characters walked in together" (Table I–1). The prep box's "your players' agendas" became "the characters' agendas".
- **Narrator voice.** "The module's rule is that clever and peaceful play is paid on the page…" became "Clever and peaceful play is paid on the page here…". "The module's own camera" became "This adventure's camera". "mysteries the module keeps" became "…the adventure keeps".
- **Dashes and long paragraphs.** Chains were split into colons, parentheses or sentences (omen, threat line, 6,500 XP, Long Rest, the Phern money, ⟨If History Breaks⟩ list, mysteries list, prep box). The Attendant bullet (190 words) is now three paragraphs inside the bullet. The keyed-room legend reads "**Keyed rooms** are headed **B1. The Room Name.** That is a code and a name, then what is there."
- "so here is how to put each in front of them" → "Still, a table that came for damage dice and Initiative should not have to go home without touching them. Here is how to put each fight in front of the characters without pushing." "not just its numbers" → "as well as its numbers".

**02 The World and the Night**
- **FRONT-7 02 L10.** "belong to the setting, not to this module; the Facets of Origin edition keeps them… A 5e table needs only what follows" → "belong to the setting, and the Val'loh gazetteer of the Facets of Origin books covers them in full… This adventure needs only what follows." The pointer is kept and the edition talk is gone.
- **FRONT-21.** Both fixes were applied as written: "What makes them monstrous is how much of them is left: grief, faith, exhaustion, courtesy. Play every scene with one of them as a scene with a person, and the horror takes care of itself." and "Hold these lines even against clever players. The honest night is the one nobody walks out of understanding."
- **Narrator voice.** "The module calls them **the Uninvited**;" → "Three killers are coming to the ball: **the Uninvited**." "(…The module does not answer this question…)" → "Nothing in this adventure answers this question…". "the **Leashed** trait — the 5e shape of everything in this section" → "…which puts everything in this section into rules". In Agenda 1's DM aside, "The module invents it here;" was cut. "the module rewards that" → "the adventure rewards that". The load-bearing phrase "the module does not say" (the child) is kept, because 01 and 03 point at it.
- **Party.** "player characters get in", "players who earned the east wing", "if the players later piece that together", "No player character learns", the "Player characters who cross him / help him" pair, "Each player character carries", "puts a player character beside Veier" and "The player character who felt like a hired traitor" all now say "characters" or "character". "the players' peripheral vision" became "the table's peripheral vision".
- **Dashes (70 down to 7) and paragraphs (8 long down to 0).** The ladder parentheticals, the hater list, Vell, Raunu's last charge (now two sentences: "Raunu has already understood… and he spends that charge…"), the snakes and the pillars were all reworked. The agenda definition list now uses "**The ask:**" and similar labels, matching how each agenda prints them. In the eight agendas, the ask/catch/at-midnight lines got punctuation-only edits: every word was kept and dashes became commas, colons or parentheses. A paragraph break now goes before each **The catch:** and **At midnight:**. Those lines used to run together into one rendered paragraph, and that was 7 of the 8 long paragraphs. The "What Is Coming" paragraph (188 words) was split at "Their master cannot act."
- **Kept:** "the best-loved Orthaen chief in generations — by commoners" (the one punchline dash), "Not revenants, not shades.", "It is a choice, not a failure", "a movement, not a magic *Counterspell* can reach", and "heirloom, not treasure".

**03 Masks and Agendas**
- FRONT-21: "which puts a spotlight on them" and "It is knowledge, with no bonus attached." Both were applied, in sentence form.
- FRONT-7 03 L83: the old-domains guide is now a `> **Sidebar — for players who know the Facets edition**` box, as the audit recommended. "In 5e it is an **origin feat**" → "Mechanically, it is an **origin feat**". "any 5e world" → "anywhere else".
- The Thenya DM aside's not-X-but-Y with doubled dashes became "The feat is Minor like the rest, but the whole of it points at another character…". The other dash pairs became commas, colons or parentheses.
- **Kept:** "It matters to nobody and everybody, which is the correct proportion for a masquerade", "how it *shows itself*, not what it is", and "wealth and not decoration". The whitelisted DC 10 line still matches its whitelist entry.

**06 After Dawn**
- The two DM-to-player prompts became quoted speech, as in the pilot: "What does your character carry out of Oraga Night?" and "You know more than the record. What do you do with it?". "in front of the players" → "in front of the table". "a player who asks to have their statement read back" and the two "Players who reached/learned the east wing" now say characters.
- The inquest triplet and Vorlain's dash pair were split. "That is not a clue that leads anywhere. It is the moment…" → "It leads nowhere. It is the moment…". In the sidebar, "The module ends at the mist-line" → "The adventure ends…". The joke "with the module's blessing" is kept.

**08 DM sheet and handouts (T7.7)**
- "Behind? Cut B13…" → "If you are behind, cut B13…". "handouts for the players" → "for the table". The pillar, Table VIII–4 caption, rumor-table intro and Handout 3's two charge sentences lost their dashes.
- The "Rooms the text does not place" list now uses the keyed-room form "**B6. The Chapel.** A public room…". This matches 04's headers.
- **Not touched:** Handout 1, Handout 2's card text (its titles, signatures and "perhaps" are the 13 dashes and the S25/S27 hits left), the rumor table, and every table cell.

**11 Pregenerated Characters (T7.7)**
- "**Specialty, in 5e terms:**" → "**Specialty:**" on all five sheets (conversion talk). "**Four players?**" → "**With four players.**". "puts a player character beside Veier" → "a character".
- Dashes became colons or parentheses in the Common-to-all-five traits, Heritage lines, Specialty lines, the Prickle, Thieves' Cant, Savage Attacker/Alert, the Weapon Mastery notes, two mask questions and the Thaumaturge note. Punctuation only: no rules text was reworded, and every number and condition is the same.
- Personality prose is untouched. The only change in that area is in Ilesse's intro ("…learned to gossip about it. That is exactly why…").

**README (T7.7)**
- FRONT-21: "The module leaves some of it out on purpose: those answers belong to the setting's future, and no table needs them to run the night." The self-praise "unforgettable" was dropped with it.
- "this edition had to invent" → "the 5e text had to invent" (the hard hit). "The player characters come too" → "The characters come too". The dash asides were reworked. The front-matter conversion statement ("This is the fifth-edition conversion…") is kept, because FRONT-7 says that is where it belongs.
- **Layout only:** the Setting/Players/Length/Rules/Tone lines are now separate paragraphs (they rendered as one run-on paragraph). The license block has one paragraph break before "Every stat block is an original creature". No license wording changed.

## Left alone, for the caller

- **01's DC-ladder table still has no title.** FRONT §3 asks for one, but numbering it would push Tables I–3 and I–4, which are cross-referenced module-wide. That is outside a wording pass.
- **Italic emphasis in DM prose** (*feels*, *for*, *always arrives*, *looked at*, *works*, *watching the proof grow*-type) breaks the STYLE "Emphasis" rule. It was not swept, because it is a style sweep and not voice.
- **01's Designer's note** keeps its "That is not a difficulty setting; it is the module's spine" (gated on Q4).

## Before → after samples

*1. 02, What Is Coming (FRONT-21).*

> **Before:** Treat them as what they are operationally: **bound servants of a power sealed away in the far east, beyond the mists** — and understand the thing that makes them work at the table: **they are people.** Not revenants, not shades. Men and women, ancient and bound, who eat the food and praise the wine and dance beautifully in a style nobody living learned. What makes them monstrous is not what was taken from them but how much is left — grief, faith, exhaustion, courtesy — and every scene with one of them should be played as a scene with a person. Do that, and the horror takes care of itself. Their master cannot act. They can, barely, briefly: …
>
> **After:** Treat them as what they are operationally: **bound servants of a power sealed away in the far east, beyond the mists**. Then understand the thing that makes them work at the table: **they are people.** Not revenants, not shades. Men and women, ancient and bound, who eat the food and praise the wine and dance beautifully in a style nobody living learned. What makes them monstrous is how much of them is left: grief, faith, exhaustion, courtesy. Play every scene with one of them as a scene with a person, and the horror takes care of itself.
>
> Their master cannot act. They can, barely, briefly: …

*2. 01, Checks (FRONT-7).*

> **Before:** Checks are written the SRD way: `a DC 15 Wisdom (Insight) check`. Where the source said a "knack applies", this edition means the character's proficiency in the fitting skill or tool, and a gifted character's gift (see chapter III) gives Advantage when the check is about the thing the gift does. … **Heroic Inspiration** replaces the Sparks of the original edition, and it works as the SRD says: …
>
> **After:** Checks are written the SRD way: `a DC 15 Wisdom (Insight) check`. Where a check depends on a character's training, proficiency in the fitting skill or tool applies, and a gifted character's gift (see chapter III) gives Advantage when the check is about the thing the gift does. … **Heroic Inspiration** works as the SRD says: …

*3. 02, How the Night Ends.*

> **Before:** When the moment comes, the last and best of his preparations has one charge in it, and Raunu — who has already understood, faster than anyone in the room, what the masked things have come for — spends it on his wife's escape instead of his own life. He dies on his own ballroom floor. It is a choice, not a failure, and if the players later piece that together, let them.
>
> **After:** When the moment comes, the last and best of his preparations has one charge in it. Raunu has already understood, faster than anyone in the room, what the masked things have come for, and he spends that charge on his wife's escape instead of his own life. He dies on his own ballroom floor. It is a choice, not a failure, and if the characters later piece that together, let them.

## Commands

- `lint_5e.py --report --file <f>` was run for each of the seven files, before and after (table above).
- `lint_5e.py --check` → OK (0 problems; 0 hard and 0 structure hits remain, module-wide at time of run).
- `bestiary_check.py --quiet` → 25 blocks + 3 Nastier, 0 mismatches.
- `pregen_check.py --quiet` → 5 pregens, 0 issues.
- `python -m pytest conversions/dnd5e/oraga_night/tools -q` → 159 passed.
- Numeral, DC and dice diff (scratchpad script, pre-edit snapshots): identical in all seven files, except the "5e" tokens listed at the top.
