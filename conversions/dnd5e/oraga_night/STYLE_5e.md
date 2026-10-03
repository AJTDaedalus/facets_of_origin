# Style Sheet — Oraga Night, 5e Edition

This is the house style for every file in this folder. It copies the decisions in
`docs/DESIGN_oraga_5e_official.md` §3. The rules-term casing follows the SRD 5.2.1
(CC BY 4.0), which this module declares. When this sheet and an older file disagree,
this sheet wins. The linter (`tools/lint_5e.py`) checks most of these rules
mechanically. Run it before and after any edit.

The example in each row shows the form to use, with a wrong form beside it where that
helps. The examples use names and numbers already printed in the module, so they add no
canon.

## The rules

| Topic | Rule | Write | Not |
|---|---|---|---|
| **Role name** | "the DM" in third person. "You" when the text tells the DM what to do. "DM Note", "DM sheet". Never "MM" or "Mirror Master" in this edition. | "If the clock fills, you choose which agenda door closes, and say so out loud." / "The DM sheet tracks the night." | "the MM picks which" |
| **Party** | "the characters" or "a character" by default. "The players" means only the people at the table. Use "player character" only where it tells PCs apart from NPCs. Outside read-aloud, "you" means only the DM. | "A character who reaches the grille can see the street." / "Ask the players whether they want a break." | "The players notice the grille." |
| **Rules-term capitals** | SRD 5.2.1 Title Case: Advantage, Disadvantage, Hit Points, Short Rest, Long Rest, Speed, Difficult Terrain, Dim Light, Bright Light, Darkness, Heavily/Lightly Obscured, Half/Three-Quarters Cover, Bloodied, Stable, Heroic Inspiration. Action names too: Attack, Dash, Disengage, Dodge, Help, Hide, Influence, Magic, Ready, Search, Study, Utilize. Write conditions as "has the Prone condition" or "is Unconscious". | "Moving through the benches is Difficult Terrain." / "A creature dropped to 0 Hit Points is Unconscious and Stable." / "Releasing a charge takes the Magic action." | "has advantage", "knocked prone", "half its speed" |
| **Spells** | Italic Title Case. | "*Detect Thoughts*", "*Tiny Hut*", "cast as she dresses for the ball: *Mage Armor*" | "detect thoughts", "*mage armor*" |
| **Magic items and crystal charges** | Italic Title Case. Never bold, never roman. | "a *Steady Light* carried in", "a second *Dark-Burst*", "*A Sealed Door*", "*House Flare*" | "**Steady Light**", "a dark-burst" |
| **Coin** | "GP", "SP", "CP" in capitals, after a normal space. | "50 GP", "25 GP of raw crystal", "1,200 GP" | "30 gp", "50gp" |
| **Checks** | "a DC 15 Wisdom (Insight) check"; "succeeds on a DC 13 Charisma (Persuasion) check". Never a bare DC, a DC range, a skill without its ability, or "roll". Spell out both alternatives: "a DC 15 Intelligence (Religion) or DC 15 Charisma (Persuasion) check". Tables may compress to "13 Charisma (Persuasion)". | "Forcing it takes a successful DC 15 Strength (Athletics) check." / Table cell: "13 Charisma (Persuasion)" | "DC 13–15", "a DC 15 Insight check", "roll Wisdom", "beat the DC" |
| **Saves and damage** | "must succeed on a DC 13 Dexterity saving throw or take 7 (2d6) Fire damage", or "…taking 7 (2d6) Fire damage on a failed save, or half as much damage on a successful one". Average first, dice in parentheses, then the damage type in Title Case. Falls may keep bare dice. | "*Failure:* 9 (2d8) Force damage" / "A creature pushed over the rail takes 1d6 Bludgeoning damage." (a fall) | "takes 2d6 damage", "14 (4d6) bludgeoning damage", "on a failed saving throw" |
| **Numbers** | Numerals for game quantities in DM text. Words inside read-aloud boxes. | DM text: "a 12-foot drop", "for 10 minutes", "within 30 feet". Box: "*the wall is twenty feet high*" | DM text: "a twelve-foot drop", "fifteen feet" |
| **Stat blocks** | SRD 5.2.1 layout throughout chapter X: bare AC plus a **Gear** line; one **Immunities** line ("Poison, Psychic; Charmed, Frightened"); "Darkvision 120 ft.; Passive Perception 14"; Advantage folded into the Initiative score; no commentary in numeric fields; limited uses as "(1/Day)", "(3/Day)", "(1/Day Each)"; "When Bloodied" becomes a ***Bloodied.*** trait; epithets go on their own line above the type line. | `**AC** 17 · **Initiative** +2 (12)` then `**Gear** Chain Shirt, Shield` / `**Immunities** Poison, Psychic; Charmed, Exhaustion, Frightened, Poisoned` / `**Senses** Darkvision 120 ft.; Passive Perception 14` | `**AC** 14 (chain shirt under a festival coat)`, separate Damage and Condition Immunities lines |
| **Difficulty vocabulary** | SRD 5.2.1 only: Low, Moderate, High, plus "beyond High". "Deadly" never appears in a budget line. One DM Note explains the 2014 multiplier. | "*Budget:* 800 XP — Low." / "nearly twice High" | "800 XP — Deadly", "a Hard fight" |
| **Read-aloud** | An indented italic block, always after a plain trigger line ("Read this when…:"). Italic paragraphs that are not indented are notes to the DM. Sidebars never contain read-aloud. Order: area header, then trigger, then box, then DM text. | `Read this when the first guests reach the court:` then a blank line, then `> *The outer gate is shut, and it was shut from the far side.*` | A box straight after a heading; read-aloud inside a **DM Note** |
| **Box species** | Declared in the legend and used exactly as declared: **Sidebar —**, **DM Note —**, **Troubleshooting —**, ⟨If History Breaks⟩, **What [Name] Says** (Q&A), the fight card's **Wants / Tells / Breaks / Nastier** lines, and the Movement run box. No **Designer's note** (pending owner ruling Q4). | `> **DM Note — the first check of the night**` / `> **Wants.** The contract satisfied or voided.` | "**Designer's note.**", "**MM Note**", a new unlabelled box |
| **Cross-references** | "(see chapter V)", '(see chapter V, "Down, Not Out")', "(card S2)", "(area B9)", "(Table I–3)". Lowercase "chapter" with a Roman numeral, in running text and in parentheses. Capitalize it only at the start of a sentence. Put section names in quotation marks, not italics. No "(source Ch. …)". The house Roman numerals stay. | "The fight is card S1 (see chapter IX, "The Seating Feud")." / "Chapter X holds every stat block." | "(Chapter V, *Midnight Rules*)", "(source Ch. III)" |
| **Spelling** | American: rumor, color, center, honor, recognize, labeled. "Gray" everywhere, except "grey robes" only if INVENTIONS #43 fixes it as canon. Check that entry before changing it. | "a rumor", "three gray masks", "the center of the court" | "rumour", "colours", "centre", "recognises", "defence" |
| **Emphasis** | No italics for emphasis in DM prose. Italics mark spells, items, section-title book names and non-indented DM notes only. | "Bare steel voids the whole scene." | "Bare steel *voids* the whole scene." |
| **Tables** | House numbering ("Table IV–1") stays, as a house choice. Every table gets a title. | `**Table IV–1: Who Came Armed**` above the table | An untitled table, or "Table 4.1" |

## Voice, in one paragraph

Write to the DM, about the characters, in the present tense. Assert the rule, then the
exception. Keep sentences around 16–19 words, and paragraphs around 45–75. No narrator
("the module would rather…"), no designer "we", and no conversion talk ("the original",
"this edition", "the source"). The reader has never seen another edition. These are
soft targets: the linter reports them per file (`--report`), and a fix pass must not make
them worse.

## Do not touch

These stay exactly as they are, whatever a sweep or a lint rule says. The linter
whitelist (`tools/lint_5e_allow.txt`) exempts the first item.

1. **Handout 1's invitation text** (chapter VIII, "Handout 1 — The Invitation"). The page
   marks it canonical. Its wording, spelling and punctuation are fixed, from "To My
   Esteemed Guest" to "Raunu Boranis". The italic instruction line above it is DM text,
   and the normal rules apply to it.
2. **Canon NPC speech.** Quoted lines that are canon keep their wording. Only the DM
   text around them changes. If a quotation breaks a rule on this sheet (a lowercase
   term, a number in words), leave the quotation alone.
3. **`INVENTIONS_5e.md`.** It is the ledger of what this edition added, with history.
   Add rows to it when a task says so. Never sweep or restyle it.

## Running the checks

```
python conversions/dnd5e/oraga_night/tools/lint_5e.py --report        # summary per file
python conversions/dnd5e/oraga_night/tools/lint_5e.py --file 04_The_Ball.md
python conversions/dnd5e/oraga_night/tools/lint_5e.py --check         # vs lint_baseline.json
python conversions/dnd5e/oraga_night/tools/bestiary_check.py --quiet
python conversions/dnd5e/oraga_night/tools/pregen_check.py --quiet
python -m pytest conversions/dnd5e/oraga_night/tools -q
```

To add an exception, put a line in `tools/lint_5e_allow.txt` in the form
`file|quoted text|reason`, for example
`05_The_Longest_Night.md|ask the players|"the players" means the people at the table here`.
