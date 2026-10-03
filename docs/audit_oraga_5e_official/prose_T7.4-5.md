# Phase 7 — T7.4 (chapter 07) and T7.5 (chapter 10): prose voice pass

*Worker, 2026-10-03. CAST-5, -6, -7; BESTIARY-10, -15; FRONT-7 (07 Draunel "The source left them…", 10 "carried over from the original cards"). Every site was found by quoted text. Wording only. A script compared every `DC n`, dice expression, numeral and straight-quoted string before and after, and found them identical in both files. Stat-block numeric lines and trait mechanics in 10 were not touched. Edits went only into the Wants / Tells / Breaks / Nastier lines, the lore tails, the How to Read prose, "If It Comes to It"'s intro, the charge rules prose and the loot list. Not committed. Baseline not re-run.*

Calibration (from the owner's G1 adjustment): keep the occasional em dash, stay in the 14–19 mean-sentence band, and don't atomize. Dashes were turned into colons, commas or parentheses, and sentences were split only where a chain ran on.

## Metrics (`lint_5e.py --report --file`, DM prose)

| metric | target | 07 before | 07 after | 10 before | 10 after |
|---|---|---|---|---|---|
| words | — | 7,390 | 7,360 | 2,524 | 2,512 |
| mean words per sentence | ≤ 19 | 14.78 | 14.21 | 16.18 | 15.80 |
| sentences over 30 words | ≤ 12% | 6.01% | 4.46% | 8.33% | 7.07% |
| em dashes per 1,000 words | ≤ 8 (aim 3–8) | 13.40 | 3.67 | 11.09 | 3.18 |
| paragraphs over 120 words | ≤ 3 | 7 | 0 | 1 | 1 |
| "the players" (S2) | 0 | 1 | 1 | 1 | 1 |
| "player character" | — | 2 | 0 | 1 | 0 |
| "you" (info only) | — | 5 | 3 | 2 | 2 |
| "not X but Y" / ", not" | — | 8 | 8 | 4 | 3 |
| hard hits | — | 6 (narrator 4, conversion 2) | 0 | 1 (conversion) | 0 |

The "the players" left in each file is "tell the players so" (Corval's bribe). It means the people at the table, as CAST-7's own fix wrote it. The "you" left in 07 is the DM ("at your table", "so you know what she does") and the realization "someone is editing you" in Vell's DM truth. In 10 it is "Treat a good idea that fails the way you treat a hard blow" and "The block exists to tell you". Both are the DM. The 10 dash count only covers what the linter classes as DM prose. Box lines also lost dashes (Wants, Tells and Breaks lines).

## Chapter 07 — what was done

- **CAST-5 (narrator):** "the module suggests spending it on a player character" became "Spend it on a character who bled for her". "the module notes the resemblance to her host without comment" became "prepared, like her host". The cut is "The module would prefer somebody competent went with her." "a killer the module has spent two chapters establishing as unbeatable" became "a killer nothing else tonight can stop". "the module notes she would be genuinely offended" became "she would be offended to learn it". **Kept as CAST-5 says:** "What it cost him… the module does not say", "The module never explains him.", the Namak-Zai "The module never uses the word at the table", and "neither does the module" in the factor DM Note. The legend backs all of these.
- **FRONT-7:** "The source left them to the DM; this edition names them in chapter IX." became "A Draunel never brings one plan to a Boranis party, and chapter IX names all three."
- **CAST-6 ("player" for the character):** these became "character": the east wing reach, "Characters who reach her", Vorlain's box ("For the character with Agenda 3"), Anha's "any character thought to befriend her", Sella's "shaken characters", Corro's "A character who takes him seriously", "The Agenda 3 character's true opponent", "the Agenda 4 character's natural ally", the Vell sword ("If a character asks", "If the characters notice"), "Characters who shadow him", "Characters standing between him", "Any character who has watched", "if a character earns it", "Every tell a character witnesses", and the Attendant's "a character with a blade out". **Kept (real people):** "pick from the player's own backstory", "tell the players so", "Players need never hear the name", and the omen line "a player who says one out loud". The factor DM Note's "help you find out" became "help them find out", because there "you" meant the table.
- **CAST-7:** Corval: "Bribing Corval is impossible. There is no check for it at all; tell the players so." Vell: "never once interesting to look at. That is not luck." Uninvited: "What makes them monstrous is how much of them is left." The Attendant's single state-change sentence was split into Idle, Focused, the fourth broken focus, and 0 Hit Points. The Vorlain drunk fix (102–104) and the cut of the repeated quote were already in the file.
- **Long paragraphs (7 → 0):** each was split at a natural turn. Raunu's summons is manner, then knowledge. The Vell sword is the public face, then the *(DM truth)* aside. Vell's roleplaying is the levers, then the DM truth. The Uninvited are company, then wrongness. The Attendant has habits, and its steel is states, then breaking. Tavva is the job, then the midnight chaos.
- **Dash chains** became colons, commas or parentheses. Kept on purpose: Vorlain's "and — this is the part House Draunel cannot imagine — *not like this*", Raunu's "the dais — the one predictable moment", Corro's "expansive — and increasingly, visibly *wrong*", the box labels (**What Corval Says —**, **DM Note —**), the "— **if friendly:**" run-ins, and canon speech.

**Kept (voice):** "the load-bearing wall of his personality", every Corval line in his box ("like a stone in my shoe", "Ask me again tomorrow"), "Corval's inability to hold the gray-mask question has a cousin", "the second-best unmemorable performance in the palace", "a businessperson who has been shot at, and it shows in both directions", every Quote line and every "What X Knows" list (untouched). Functional contrasts kept: "a prize, not a schedule item", "an exit, not a weapon", "a made thing, not a born one", "arriving, not running", "not a hit-point total".

## Chapter 10 — what was done

- **FRONT-7:** "carried over from the original cards" was cut.
- **BESTIARY-10 ("you" / "player"):** "what a watchful character sees". Essin's Tells became "Admires a character's mask from the side nearest Vorlain, then invites them, very warmly…". Essin's Nastier became "what the character said to Vorlain; a cousin was standing at their elbow". The Gallery Knife became "not on the characters". The Hollow became "nobody can frighten a man". Callun's Nastier became "whatever the party is trying to sell her". Also "A guest a character kills" (the crowd line).
- **BESTIARY-15:** "in the fiction, not by veto" lost its ", not by veto". "their lives, their minds and their shapes" became "lives, minds and shapes", and that sentence was split. The Sect Guard's flavor sentence became "They shout and whistle long before they draw." (This is the trait's closing flavor line. The whistle mechanic above it is unchanged.) The Sect Guard's Wants became "The trouble ended." The Wept's "She has a task, not a body count." was cut. The Radiant became "He keeps going, never answers, and never turns." That keeps all three facts without the anaphora. "very probably" was cut from "If It Comes to It". The Wept's "she does not wind up — she arrives" became "she arrives without winding up".
- **Dashes** were converted in How to Read, the two mercies, the Fractures bullets, the Wants, Breaks and Tells lines (Attendant, Honor Guard, Captain, Sergeant, Circle Knife, Draunel Duelist, Draunel, Hollow, Maiven, Radiant, Tavva, Thenya Slinger, Wept), Vell's tail, the charge rules and Tavva's sack. Corval's line now matches 07: "is **impossible**. There is no check; tell the players so."
- **Not touched:** every numeric line, every trait and action mechanic (including "held, not hurt worse", *Move Aside*, *Elsewhere* "arriving, not running", the Hollow's Shadow-Step, In His Cups, Thirty Degrees Hotter, and the Second Clause), Table X–1 and X–3, and the SRD notice. **Kept for voice:** the "A person — …" tails on all three Uninvited (one deliberate pattern across the three), Essin's "a favor, a name, where a body is", Callun's "*what did he say?*", the bodyguards' "remember them like this", Vorlain's "forever, aching — and *not like this*", and "It is an heirloom, not treasure" (it carries a rule).

## Before → after samples

*1. 07, the Attendant's states (CAST-7).*

> **Before:** It has two states. **Idle** — its default — it is rusty, easily distracted, and cannot be bothered with its own magic. **Focused** — at the start of any of its turns, once the party has become a real interruption, if one of the three in the scene has no Delay and glances at it and at the party — it is devastating. A clever distraction breaks its focus, but only until one of the three glances at it again; the fourth broken focus of the night sends it off to stand at a window and watch the fires; driven to 0 Hit Points, it loses interest in being here and steps back into the shadow. It leaves no body. …
>
> **After:** It has two states. **Idle** is its default: it is rusty, easily distracted, and cannot be bothered with its own magic. It turns **Focused** at the start of any of its turns, once the party has become a real interruption, if one of the three in the scene has no Delay and glances at it and at the party. Focused, it is devastating.
>
> A clever distraction breaks its focus, but only until one of the three glances at it again. The fourth broken focus of the night sends it off to stand at a window and watch the fires. Driven to 0 Hit Points, it loses interest in being here and steps back into the shadow. It leaves no body. …

*2. 07, Vell (CAST-5, -6, -7).*

> **Before:** … Players who shadow him find only preparations: a walked garden, a tested gate, a purchased boat. All night he does not fight, does not hurry, and is never once interesting to look at — and that last is not luck. *(DM truth: …)* … he moves *the way the Uninvited move* — arriving, not running — and he holds the Radiant, a killer the module has spent two chapters establishing as unbeatable, alone, barely, long enough. Any player who has watched the three all night understands without being told …
>
> **After:** … Characters who shadow him find only preparations: a walked garden, a tested gate, a purchased boat. All night he does not fight, does not hurry, and is never once interesting to look at. That is not luck.
>
> *(DM truth: …)* … he moves *the way the Uninvited move*, arriving, not running, and he holds the Radiant, a killer nothing else tonight can stop, alone, barely, long enough. Any character who has watched the three all night understands without being told …

*3. 10, "The Uninvited, Before You Read Their Blocks" (BESTIARY-15).*

> **Before:** They close them in the fiction, not by veto. Something holds each of the three on a leash that runs east, and that leash holds their lives, their minds and their shapes, and pulls them home when their work is done — or at the last bell, whichever comes first. Say that at the table when a player reaches for the spell, and then say what the spell bought.
>
> **After:** They close them in the fiction. Something holds each of the three on a leash that runs east. That leash holds their lives, minds and shapes, and it pulls them home when their work is done or at the last bell, whichever comes first. Say that at the table when a player reaches for the spell, and then say what the spell bought.

## Commands

- `lint_5e.py --report --file 07_Cast_of_the_Ball.md` / `--file 10_Bestiary.md`: see the table above. Both files now have 0 hard hits.
- `lint_5e.py --check`: OK (0 problems; 5 hard and 0 structure hits remain, module-wide, with other workers' files in flight).
- `bestiary_check.py --quiet`: 25 blocks + 3 Nastier, 0 mismatches.
- `pregen_check.py --quiet`: 5 pregens, 0 issues.
- `python -m pytest conversions/dnd5e/oraga_night/tools -q`: 159 passed.
- Number/quote diff script (backups in the scratchpad): DC, dice, numerals and straight-quoted strings identical in both files.
