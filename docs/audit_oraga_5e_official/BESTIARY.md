# Official-Standard Audit — Slice BESTIARY (`10_Bestiary.md`)

*Auditor: BESTIARY slice, 2026-09-30. Audit only; no module file edited.
Yardstick: `docs/RESEARCH_5e_module_conventions_structure.md` (C-S) and
`docs/RESEARCH_5e_module_conventions_voice.md` (C-V, S). Maths verified with
`<scratchpad>/bestiary_check.py` (HP from hit dice, ability mods, saves, skills,
passive Perception, attack bonus and damage averages, save DCs, XP/PB, and a DMG
ch. 9 CR estimate for all 25 blocks and 5 Nastier variants).*

File: `conversions/dnd5e/oraga_night/10_Bestiary.md` (1,965 lines, 16,579 words).
The module declares SRD 5.2.1 (2024) stat blocks as its target (`10:3`; voice doc §12),
so format is judged against the 2024 layout. Where the file is in 2014 layout instead,
that counts as a mixed layout.

**Party level:** four 4th-level characters, ending at 5th (owner ruling, FIXPLAN §6;
matches `10:16-19`). The difficulty claims here use the 2024 budget for four 4th-level
characters: Low 1,000, Moderate 1,500, High 2,000 XP. The DMG ch. 9 CR estimates are
properties of each creature and don't depend on party level.

---

## 1. Summary

| Dimension | Verdict |
|---|---|
| **MECHANICS** | **Strong on arithmetic, with some rules gaps.** All 25 blocks re-derive exactly: HP = average hit dice + Con × HD, every save = mod + PB, every skill = mod + PB (or + 2×PB for deliberate expertise, 14 cases), every passive Perception, attack bonus, damage average and save DC, and the XP/PB table are correct. The DMG CR check puts 21 of 25 blocks within one step of the stated CR. The four outliers are Kovaun (overstated) and the three Uninvited (understated, which is moot under *Leashed* apart from the Wept's action economy). The rules problems: one contradiction (the *detain* mercy against the Bought Blade), two uncapped or ambiguous triggers, and one block (Vell) that gives the MM nothing when a player attacks him. |
| **STYLING** | **Mostly official. The layout is mixed.** Field order, attack grammar, save-effect grammar, Trigger/Response reactions and alphabetical order all follow SRD 5.2.1. The 2014 carry-overs are armor sources in AC, the "Damage/Condition Immunities" labels, comma-separated Senses and commentary in CR lines. The file also adds non-SRD headers ("When Bloodied"), non-SRD usage tags ("1/Scene", "3/Night") and five different typographic forms for the crystal-charge item names. |
| **PROSE** | **Good, human, a little mannered.** Sentence length is on target (mean 14.3 words, median 12, 7.8% over 30 words). Seven lines address the characters as "you" (C-V1). There are about 21 "X, not Y" constructions (roughly 8 of them rhetorical) and 104 em dashes, which is the AI rhythm the house memory rule flags. Social thresholds are written as bare DCs, not "DC N Ability (Skill) check". |
| **CONTENT** | **Complete and on-brief.** Every creature named in Chapters IV, V and IX has a block, and every card in Table X–1 exists (S1–S14). No SRD monster is reused by name. No non-SRD (MM/Volo's) block is copied: the nearest SRD shapes (knight, veteran, spy, priest, noble) were checked and differ. The one exception is the Sect Guard, which carries the SRD **guard**'s numbers without saying so. The Uninvited spell-answer table is better than anything in an official module. |

**Top 5 issues**

1. **BESTIARY-1 (P1).** The *detain* mercy says the Bought knock a creature out, Unconscious and Stable. The Bought Blade's own block says it drops the creature to 1 HP and Grappled. Two rulings for one blow.
2. **BESTIARY-2 (P2).** The Wept's *She Arrives* gives her a third 28-damage attack on every turn she Shadow-Steps. That makes her *Nastier* dial ("three attacks a turn") meaningless, and her DMG CR about 14–17, not 11.
3. **BESTIARY-3 (P2).** *Call the House* fires for **each** guard's first Bloodied, which can summon twelve of the nine guards. The card S4 and Chapter IV mean "the first guard".
4. **BESTIARY-5 (P2).** The stat blocks are in a mixed 2014/2024 layout (C-S42 [A]): AC sources, 2014 immunity labels, Senses punctuation, initiative-with-advantage, and CR-line commentary.
5. **BESTIARY-8 (P2).** Social thresholds are bare DCs ("Deceiving him is DC 20", "(DC 13)", "is DC 25"), 9 places. C-V15 requires "DC N Ability (Skill) check".

---

## 2. Findings

### BESTIARY-1 [P1] *Detain* mercy contradicts the Bought Blade's *To the Terms* (MECHANICS)
- Where: `10:35-37` (How to Read, *Knocked out, not killed*: "…the Bought on a contract to detain … is **Unconscious and Stable**") vs `10:434-437` (Bought Blade, *To the Terms*: "drops to 1 Hit Point instead and has the Grappled condition").
- Yardstick: C-S42 [A] (the block is authoritative); brief's rules-contradiction P1 criterion; CLAUDE.md "quick references are compressions".
- Problem: an MM running S3 reads two different outcomes for the same blow. One leaves the character awake and grappled at 1 HP. The other leaves them unconscious and sends them to the gatehouse cell. That changes whether the character can act in the last bell.
- Fix: take the Bought out of the How to Read list and point to their trait. Before: "(the honor guard, the sect guard, the Bought on a contract to detain, the Church Wardens)". After: "(the honor guard, the sect guard, the Church Wardens; the Bought hold a creature at 1 Hit Point instead, see *To the Terms*)".

### BESTIARY-2 [P2] The Wept: *She Arrives* adds a third attack every turn, which breaks the *Nastier* dial and her CR (MECHANICS)
- Where: `10:1745-1747` (*She Arrives*), `10:1751` (Multiattack: two attacks), `10:1758` (Shadow-Step is a Bonus Action, usable every turn), `10:1788-1790` (*Nastier*: "she makes three Strength Like a Fact attacks a turn").
- Yardstick: C-S42 [A] (the block must be self-consistent); DMG ch. 9 CR check.
- Problem: a Bonus Action step followed by *She Arrives* gives her 3 × 28 = 84 damage a round at +10. DMG offensive CR is about 13–14. The defensive CR, counting the BPS resistance ×1.5 and three auto-saves, is 19 even before *Leashed*. The estimate lands near CR 17 against a stated CR 11. More to the point, *Nastier* promises three attacks a turn as the harder setting, but she already makes three on any turn she steps, so the dial does nothing or adds a fourth. *Down, Not Out* keeps this from killing anyone, but each hit very nearly drops a 4th-level character.
- Fix (keeps the "she does not wind up" fiction without adding an attack): "***She Arrives.*** The Wept does not wind up. When she uses Shadow-Step, she can make one of her Multiattack's attacks at once on arrival, against whoever stands between her and the dais." *Nastier* is then a real dial. With this change her offensive CR drops to about 10. The combined DMG figure stays near 14, but only because of the defensive side (resistances and auto-saves), which *Leashed* makes moot anyway.

### BESTIARY-3 [P2] *Call the House* has no cap (MECHANICS)
- Where: `10:395-398` ("*Trigger:* The guard is first Bloodied … Four more Boranis Honor Guards arrive"); the palace has nine guards (`10:408`). S4 (`09:852-853`) and `04:62` mean the first guard only.
- Yardstick: C-S42 [A]; C-S13 [A] (a beat needs a clear trigger).
- Problem: with S4's three guards, each first-Bloodied reaction calls four more, so up to 12 are summoned from a house of 9. The S4 budget (3,150 XP with "the four who are coming") assumes one call.
- Fix: "*Trigger:* The guard is Bloodied, and no guard has called the house this scene."

### BESTIARY-4 [P2] Damaris Kovaun is overstated at CR 1 (MECHANICS)
- Where: `10:692-704`, Table X–1 `10:61`.
- Yardstick: DMG ch. 9 (checked by script). Defensive: 33 HP at AC 11 gives about CR 0–1/8. Offensive: 3 DPR at +2 gives about CR 1/8. Stated CR 1 is roughly 3–4 steps high.
- Problem: *In the Church's Name* (a DC 14 area no-hostile-actions effect, Recharge 5–6) earns her some bump, but not three steps. Her 200 XP inflates S8's budget ("4 × 200 = 800 XP", `09:1125`) and its award. S8 labels 800 XP "Low", but for four 4th-level characters Low is 1,000 XP, so the card is already under Low. That is for the SNAKES slice to reconcile.
- Fix: CR 1/2 (XP 100; PB +2), which leaves room for the control effect. Update Table X–1 and hand S8's budget line to the SNAKES slice (3 × 200 + 100 = 700 XP). Or keep CR 1 and add one sentence to the block's lore saying the control effect carries the rating.

### BESTIARY-5 [P2] Mixed 2014/2024 stat-block layout (STYLING)
- Where / what:
  - **AC with armor source** (2014) on 21 blocks, for example `10:298`, `348`, `417`, `461`. SRD 5.2.1 prints bare AC and lists armor on a **Gear** line. The four Uninvited-side blocks (`10:180`, `1015`, `1281`, `1688`) are already 2024-style.
  - **2014 labels**: "Damage Immunities" and "Condition Immunities" (`10:191-192`), and "Condition Immunities" on all three Uninvited (`10:1027`, `1293`, `1701`) next to the 2024 "Resistances" label. 2024 uses a single line: **Immunities** Poison, Psychic; Charmed, Exhaustion, Frightened, Poisoned.
  - **Senses** use a comma before Passive Perception (`10:193`, `1029`, `1295`, `1703`). 2024 uses a semicolon: "Darkvision 120 ft.; Passive Perception 14".
  - **Initiative with advantage** is written as a suffix: "+1 (11), with advantage" (`10:1177`) and "+4 (14), with advantage" (`10:1223`). In 2024 the advantage is folded into the score: "+1 (16)" and "+4 (19)".
  - **Commentary in fields**: the CR lines (`10:195-197` Attendant, with "High by the clock", which is unclear; `10:1031`, `1297`, `1705` "— *but see Leashed*"; `10:1843`), and the Resistances line (`10:1699-1700` "*not armor: wrongness…*").
- Yardstick: C-S42 [A] (SRD field order and content); voice §12 ("follow 5.2.1 in `10_Bestiary.md`"); brief ("flag a mixed layout").
- Problem: the blocks mostly read as 2024 (Initiative, Attack Roll grammar, CR (XP; PB), the save table), and the 2014 remnants make them look hand-assembled. Commentary in a numeric field is something no official block does.
- Fix: normalise to 2024. (a) Either move armor into a **Gear** line ("**Gear** Chain Shirt, Shield, Longsword"), or keep the parentheses and say in How to Read that armor is noted in parentheses as a house choice. Either is acceptable; say which. (b) Use one **Immunities** line with a semicolon between damage types and conditions. (c) Use a semicolon before Passive Perception. (d) Fold advantage into the initiative score. (e) Move all field commentary into the trait or lore text. For example: "**CR** 8 (XP 3,900; PB +3)" and put "Idle, it fights like a CR 5; award the full XP however the party gets it out of the way" into the S14 pointer line. "*but see Leashed*" is already covered by the trait.

### BESTIARY-6 [P2] The Hollow: *The Post* doesn't say what a successful save does (MECHANICS)
- Where: `10:1065-1069`.
- Yardstick: C-V18 (the save template states both outcomes); C-S42 [A].
- Problem: "no creature passes … without his leave. A creature that tries must succeed on a DC 17 Strength saving throw or be pushed." The text never says what a success does. The main doors are where players will try this every round. *Delay* (`10:1052-1054`) implies nobody passes while he holds the post.
- Fix (follows the *Delay* text): "…or be pushed 10 feet away and have the Prone condition. On a success, the creature holds its ground but still doesn't get past him."

### BESTIARY-7 [P2] Crystal-charge names appear in five typographic forms (STYLING) [d20-portable]
- Where: *dark-burst* in italic lowercase (`10:1375`, `1527`, `1571`, `1949`); **Dark-Burst** in bold (`10:1933`); Dark-Burst in roman (`10:128`, `1936`); *House Flare* in italic Title Case (`10:1954`); Steady Light in roman (`10:1342`, `1917`); *door-seal* against **Door-Seal**.
- Yardstick: C-S39 [A] (magic items italic); C-V21 and C-V26 (one case scheme).
- Problem: a 5e reader takes italics to mean "magic item" and bold to mean "stat block". Here the same item appears in three styles.
- Fix: italic Title Case everywhere, matching the 2024 item style the file already uses for *House Flare*: *Dark-Burst*, *Door-Seal*, *Steady Light*, *A Sealed Door*, and so on. Keep the table's first column as italic, not bold.

### BESTIARY-8 [P2] Social thresholds are bare DCs, not the SRD check form (MECHANICS)
- Where (9): `10:708` "Lying to the Prelate about matters of faith is DC 20"; `10:876` "Deceiving him is DC 20"; `10:1143-1144` "(DC 13)"; `10:1425-1426` "DC 25 … DC 10"; `10:1805` Raunu "DC 25"; `10:1818` Corval "DC 20"; `10:1857-1858` Vell "Every check to move him … is DC 25"; `10:220-221` "roll the ability and skill that fit it against DC 13" (S6 smell); `10:150-151` Fractures, skills named without an ability ("Persuasion, Performance, Religion, Insight").
- Yardstick: C-V15, C-V16; S3, S4, S6; C-S39 [A] ("DC N Ability (Skill) check").
- Problem: a 5e MM has to guess which ability applies. Some of these would otherwise be contested (Deception against Insight), so the fixed DC should say so explicitly.
- Fix, examples:
  - `708`: "A creature that tries to deceive the Prelate about matters of faith must succeed on a DC 20 Charisma (Deception) check."
  - `1143`: "…but only by someone she already trusts, with a DC 13 Charisma (Persuasion) check, or by proof of her kinswoman (no check)."
  - `1425`: "Charisma (Deception) checks to deceive Callun about money are DC 25; about anything human, DC 10."
  - `221`: "…then make an ability check with whatever skill fits it: DC 13 while it is Idle, DC 19 while it is Focused."
  - `150`: "…an ability check using whatever skill the words fit: Charisma (Persuasion), Charisma (Performance), Intelligence (Religion), Wisdom (Insight), or a plain Charisma check for a bared truth."
  - Apply the same pattern to the rest.

### BESTIARY-9 [P2] The Delay-trick DC is given only for the second attempt (MECHANICS)
- Where: `10:133-134` "The same trick earns Delay twice at most on the same Uninvited (the second time at DC 15)". Chapter V gives the base: `05:216-218`, "at **DC 13** — **DC 15** if the same trick has already worked".
- Yardstick: C-V14 (point to the rule, don't half-restate it); CLAUDE.md quick-reference rule.
- Problem: a reader of the bestiary alone learns the DC for a repeat trick but not for the first one.
- Fix: "A trick earns Delay on a DC 13 check, DC 15 if it has already worked on that Uninvited tonight, and never a third time (Chapter V, *Buying Time*); a spell is a trick like any other."

### BESTIARY-10 [P2] MM-facing lines address the characters as "you" (PROSE) [d20-portable]
- Where (7): `10:28` "what a watchful **player** sees" (should be the character); `10:334-335` "Admires your mask from the side of you nearest Vorlain. Invites you, very warmly…"; `10:907-908` "what you said to Vorlain … at your elbow when you said it"; `10:1002` "not on you"; `10:1096` "you cannot frighten a man"; `10:1453` "what you are trying to sell her".
- Yardstick: C-V1 (in MM prose "you" means only the MM); C-V2; S2.
- Problem: in an official module "you" is the MM. These lines read as if the MM is the one being invited out onto the terrace.
- Fix, light-touch:
  - `28`: "what a watchful character sees".
  - `334`: "Admires a character's mask from the side nearest Vorlain, then invites them, very warmly, to take the air on the terraces."
  - `907`: "Essin already knows what the character said to Vorlain; a cousin was standing at their elbow."
  - `1002`: "Eyes on the service doors, not on the characters."
  - `1096`: "nobody can frighten a man who would not much mind ending."
  - `1453`: "She has already bought whatever the party is trying to sell her."

### BESTIARY-11 [P2] Master Vell: nothing says what happens when a character attacks him (MECHANICS/CONTENT)
- Where: `10:1839-1891` ("**AC** — · **HP** —"; "cannot be fought"; *Elsewhere* is an Action).
- Yardstick: C-S30 [U] (non-combatants still need a fallback); C-S35 [A] (every fight's Development covers what happens).
- Problem: players will attack him. With no AC and no rule, the MM has to improvise, and *Elsewhere* is an Action, so it can't answer a blow on someone else's turn. The text also says the Crossing is "the only time all night anyone sees" him move the way the Uninvited move. So any fix that makes him vanish under a blow conflicts with canon.
- Fix: **NEEDS-RULING** (see §4, item 1). Once the owner rules, add one trait. Two wordings, depending on the ruling:
  - (a) "***Not There.*** Attacks against Vell miss and spells that target him fail; he has already stepped where the blow wasn't, and nobody sees how."
  - (b) "***Not Worth It.*** A creature that means to attack Vell finds, when it comes to it, that it doesn't (no save); it can take a different action instead."

### BESTIARY-12 [P3] Non-SRD usage tags and "free action" (STYLING)
- Where: `10:384` "(Each 1/Scene)"; `10:553` "(1/Scene)"; `10:519` "(1/Scene)"; `10:1049`, `1320`, `1724` "(3/Night)"; `10:1429` "as a free action".
- Yardstick: C-S42 [A] (limited use written "(1/Day)", "(3/Day)", "(1/Day Each)", "(Recharge N–N)"); C-V26.
- Problem: 5e has no "scene" time unit and no free actions. A 2014 reader in particular will stall on them.
- Fix: the module is one night, so "(1/Day Each)", "(1/Day)" and "(3/Day)" say the same thing in SRD terms. For Callun: "She can call them off at any time, no action required." If "until the scene ends" (the Honor Guard's *Seal* and *House Seal*) stays, define it once in How to Read: "the scene ends when the fight ends or the Movement changes."

### BESTIARY-13 [P3] "When Bloodied" headers, Fracture run-ins and epithets in the type line (STYLING)
- Where: "**When Bloodied**" used as a section header (`10:1092`, `1365`, `1557`, `1762`). Epithets fused into the italic type line on 14 blocks, for example `10:178` "*A quiet guest with no master. Medium Construct, Unaligned*", `415`, `459`, `527`, `689`, `801`, `856`, `914`, `1013`, `1119`, `1175`, `1279`, `1406`, `1501`, `1627`, `1686`, `1840`.
- Yardstick: C-S42 [A] (sections are Traits, Actions, Bonus Actions, Reactions and Legendary Actions only; the type line is only size, type and alignment).
- Problem: an MM scanning for the type line has to read past a tagline first. "When Bloodied" looks like an action-economy category, and Tavva's version (`10:1559`) doesn't say what action releasing the charge costs.
- Fix: turn each "When Bloodied" block into a trait under Traits. For example "***Bloodied.*** When Tavva is first Bloodied, she uses Release a Charge on her next turn (a Bonus Action); if she has none left, she starts bargaining…". The Fracture run-ins can stay after the block as a house sidebar. Put the epithet on its own italic line above the type line, or open the lore tail with it: "*The Other Thief.*" on its own line, then "*Medium Humanoid (Human), Neutral*".

### BESTIARY-14 [P3] Traits with no rules effect (STYLING/CONTENT)
- Where: *Blood, Not Hire* (`10:315-317`), *Pays Her Debts* (`10:713`), *Stones Before Steel* (`10:1601-1603`, "aims at hands" does nothing in the block), *The Wrapped Sword* (`10:1861-1864`, deliberately empty).
- Yardstick: C-S42 [A] (every official trait carries a rule; flavour goes in the lore paragraph).
- Fix: move the first three into the italic lore tail or the Tells. For example, *Stones Before Steel* becomes a Tell: "Uses the sling first, and aims at hands." *The Wrapped Sword* can stay; it tells the MM something they need, namely that the block gives the sword no numbers.

### BESTIARY-15 [P3] AI rhythm: negative parallelism, tricolons, em-dash density (PROSE) [d20-portable]
- Where: 21 ", not …" constructions, about 8 of them rhetorical: `10:99` "in the fiction, not by veto"; `10:437` "held, not hurt worse"; `10:1482` "volume and numbers, not blades"; `10:1489` "Trouble ended, not a fight won"; `10:1521` "to leave, not to win"; `10:1778` "a task, not a body count"; `10:1953` "an heirloom, not treasure"; `10:1874` "arriving, not running". Tricolons: `10:100` "their lives, their minds and their shapes"; `10:1386` "He does not stop, does not answer, does not turn." `10:1099` is a four-beat list. 104 em dashes in 16.6k words, many in chains (`10:1799`, `1805`, `1370`). Hedge: `10:1799` "very probably" (S25).
- Yardstick: memory rule (no AI rhythm); C-V6; S25.
- Fix (light-touch; keep the functional contrasts in Tells such as `10:1615` "not the gate"):
  - `99`: "The blocks close those doors in the fiction."
  - `1482`: "They shout and whistle long before they draw."
  - `1489`: "**Wants.** The trouble ended."
  - `1521`: "She fights to get out."
  - `1778`: cut the sentence; *Wants* already says it.
  - `1386`: "He keeps going, and he never answers."
  - `100`: "…that leash holds their lives, minds and shapes…".
  - `1799`: "…and each one says why it should not happen."
  - Convert about a third of the em dashes to commas or full stops, starting with the stat lines under *If It Comes to It*.

### BESTIARY-16 [P3] Mixed capitalization of spells, conditions and advantage (STYLING)
- Where: spells in the table are lowercase italic, except *Tiny Hut* (`10:123`, 2024 Title Case). Condition words are lowercase in prose: "can't be charmed, frightened…" (`10:1046`, `1312`, `1721`, `1866`), against "the Prone condition" everywhere else. "Disadvantage" is capitalized at `10:216` and `225` against "advantage" and "disadvantage" lowercase 20 times elsewhere (module-wide: 31/2 and 14/3).
- Yardstick: C-V21, C-V26; S15, S16.
- Fix: *tiny hut*, to match the file's lowercase spells. "can't have the Charmed or Frightened condition, can't be put to sleep…". "with disadvantage" and "has disadvantage" at `216` and `225`. The module-wide scheme is the FRONT slice's call. Within this file, the majority is lowercase advantage and capitalized conditions and Hit Points.

### BESTIARY-17 [P3] Save-effect clauses carry flavor or no effect (STYLING)
- Where: `10:264` "*Success:* Half damage only. The magic is real. It rarely cares to use it."; `10:723-724` Kovaun "*Success:* The target knows exactly what it is doing, and so does the room."
- Yardstick: C-V18; C-S42 [A] (2024 "Success: Half damage.").
- Fix: `264`: "*Success:* Half damage." Move "The magic is real; it rarely cares to use it" to the *Before Midnight* lore paragraph. `723`: drop the Success clause; 2024 omits a Success line when success means nothing happens. Or keep a rule: "*Success:* The target is immune to this effect until the Prelate finishes a Short or Long Rest." That is a new mechanic, so it is optional.

### BESTIARY-18 [P3] The Attendant's *Two Turns* has edge cases (MECHANICS)
- Where: `10:249-251` (second turn "at Initiative count 10 lower"); `10:261` (Recharge 5–6 while Focused).
- Problem: at Initiative 9 or lower, the second turn falls below count 0. And with two turns, it is unclear whether *Put Aside* rolls its recharge at the start of each turn, which would make it about twice as frequent as the CR math assumes.
- Fix: "…and one at Initiative count 10 lower (last in the round, if that is below 1). Roll Put Aside's recharge only at the start of its first turn each round."

### BESTIARY-19 [P3] The Fracture rule is printed twice and the copies have drifted (PROSE/MECHANICS) [d20-portable]
- Where: `10:146-166` against `05:598-630`. The drift: "spend its action" against "an action in a fight, or one beat out of one"; "one word the speaker will carry home" against "carry for the rest of their life"; "The MM chooses which" is missing in 10's "4 or less" bullet.
- Yardstick: C-V14 (point, don't re-explain); CLAUDE.md "quick references are compressions, not paraphrases".
- Fix: make 10's copy a strict compression of Chapter V's, adding "or one beat out of one" and "the MM chooses", or cut it to the DCs plus a pointer: "(Chapter V, *The Fractures*)".

### BESTIARY-20 [P3] SRD reuse isn't noted, and the fallback block isn't named (CONTENT)
- Where: Sect Guard (`10:1458-1487`) has the SRD **guard**'s exact numbers (Str 13 Dex 12 Con 12 Int 10 Wis 11 Cha 10, AC 16, HP 11 (2d8 + 2), Perception +2, CR 1/8), with a new weapon and traits. The *A guest*, Anha and Otta lines (AC 10, HP 4) are the SRD **commoner**.
- Yardstick: C-S43 [U] (base creature named); C-S30 [U] (one fallback block named); brief (SRD source noted).
- Fix: add to the Sect Guard lore tail: "*Built on the SRD guard.*" For *A guest*: "use the **commoner** stat block (SRD 5.2.1), with no attacks."

### BESTIARY-21 [P3] Alignment is blank on the three Uninvited and Vell (STYLING)
- Where: `10:1013`, `1279`, `1686`, `1840`.
- Yardstick: C-S42 [A] (the type line always carries alignment). INVENTIONS #44 records the decision as "Alignment —".
- Problem: the blocks print nothing, while the ledger says "—". A blank reads as a typo.
- Fix: print it as the ledger says, "*Medium Humanoid (Human), —*", or add one line to How to Read: "The three Uninvited and Master Vell have no alignment listed, on purpose." Don't choose an alignment (that would be a canon call).

### BESTIARY-22 [P3] Veier's stat line is off-format (STYLING)
- Where: `10:1809-1811` "Speed 30 ft (15 ft tonight)", "+4, range 30/120 ft, 4 (1d4 + 2) Bludgeoning".
- Fix: "Speed 30 ft. (15 ft. tonight)". "*Border Sling.* *Ranged Attack Roll:* +4, range 30/120 ft. *Hit:* 4 (1d4 + 2) Bludgeoning damage."

### BESTIARY-23 [P3] Item presentation: no item-type line, one unvalued item, coin case (STYLING/CONTENT)
- Where: Table X–3 (`10:1921-1934`) has no type line. The loot entry "a coat worth more than the advance" (`10:1963`) has no value. "GP" (`10:1906-1961`, 6×) against "gp" in 03, 08 and 11.
- Yardstick: C-S45 [A] (treasure itemised with gp values); C-V25; official item entries carry "*Wondrous item, rarity*".
- Fix: caption the table with "All are consumable Wondrous Items; none requires attunement." Value the coat: "(worth 10 GP)" is a number, not canon, but it is the owner's call if the coat matters. Coin case goes to FRONT for one module-wide scheme.

### BESTIARY-24 [P3] CR labels on the Uninvited sit below the DMG math (MECHANICS)
- Where: the Hollow (`10:1031`), the Radiant (`10:1297`).
- Evidence (script): Hollow defensive about CR 15 (157 HP × 1.5 for BPS resistance, +60 for three auto-saves), offensive about CR 6, combined about CR 11 against a stated 9. Radiant: defensive 15, offensive 9, combined about 12 against a stated 10. (The Wept is in BESTIARY-2.) Rhaza Callun is about CR 0–1/8 against a stated 1/4, which is defensible given *Someone Else's Problem*. The Sect Guard is 1/4 by the DMG but 1/8 as the SRD's own guard, so it is fine.
- Problem: small. Under *Leashed* the defensive CR is infinite and no XP is budgeted for them, so the label only signals menace. The brief asked for "~CR 9–11", and the labels meet that.
- Fix: none required. Optionally add one line to *The Uninvited, Before You Read Their Blocks*: "Their CRs describe how hard they hit, not how hard they are to stop; nothing tonight stops them."

---

## 3. What already meets the official standard (don't break it)

- **Arithmetic is clean.** In all 25 blocks and all 5 *Nastier* variants: HP = average hit dice + Con × HD; saves = mod + PB; skills = mod + PB, with 14 deliberate expertise cases at + 2×PB; passive Perception = 10 + Perception; attack bonus = Str/Dex + PB; damage averages; save DCs = 8 + PB + ability (for example Kovaun 14 on Wis, Tavva 13 on Dex, Hollow and Radiant 17); Table X–2 XP/PB. Recheck with the script after any edit.
- **2024 field order and grammar** are correct throughout: type line; AC and Initiative (score in parentheses); HP (dice + mod); Speed; the ability/save table; Skills; Resistances; Senses; Languages; CR (XP; PB); then Traits, Actions (Multiattack first), Bonus Actions and Reactions (*Trigger/Response*). Attack lines use "*Melee Attack Roll:* +N, reach 5 ft. *Hit:* N (XdY + Z) Type damage." Save effects use "*Strength Saving Throw:* DC N, … *Failure:* … *Success:* …". Recharge tags are correct.
- **Alphabetical order**, filing "The X" under X (C-S9 and the LMoP habit). A **how-to-read primer** in LMoP style, with 2014-table notes (Initiative, Heroic Inspiration, the Magic action).
- **Licence hygiene:** SRD 5.2.1 attribution at the top. No SRD monster reused by name. No non-SRD book block copied.
- **The spell-answers table** for the Uninvited closes the obvious SRD exploits (banishment, power words, hold, charm, polymorph, counterspell, grapple, *tiny hut*, and so on), each with a stated result and a Delay price.
- **Every block carries morale (*Breaks*)** and a non-lethal default. Non-combatants get a stat line, not a block, and no XP (C-S30).
- **Item pricing** matches 2024 consumable pricing (common 50 GP, uncommon 200 GP). *House Flare* and *House Seal* match the Honor Guard's *Warder* (DC 20, 30-foot Emanation).
- **Cross-references resolve:** every card S1–S14 in Table X–1 exists in Chapter IX; Chapter V's *Midnight Rules*, *Down, Not Out*, *Buying Time*, *Two Hundred People*, *The Fractures*, ⟨They trap one…⟩ and ⟨They save Raunu⟩ exist; Chapter IV's *The Palace on Alert* exists. Every creature bolded in Chapters IV, V and IX has a block.
- **Numbers agree with Chapter V:** the last-blow DC 15 Str/Dex save, 15 ft. push and Prone; 30+ damage in a round = 1 Delay; the Wept's DC 15 at 2+ Delay; the Attendant's DC 13/19, four broken focuses, HP 229, CR 8. *Call the House* now matches Chapter IV and S4 on numbers (only the trigger cap is missing; see BESTIARY-3).
- **House choices, not defects:** the *Wants/Tells/Breaks/Nastier* sidebars are blockquoted, which the module's legend defines as boxed sidebars (`01:343`), so they are not read-aloud. Numbered tables ("Table X–1") follow the project style guide's invariants. The DC ladder in How to Read is Chapter I's decided ladder.

---

## 4. NEEDS-RULING

1. **Master Vell under attack (BESTIARY-11).** *Background:* the block says Vell "cannot be fought" but gives him no AC, no HP and no rule for what happens when a player swings at him anyway. At a 5e table someone will. Chapter V says the Crossing is the only time all night anyone sees him move the way the Uninvited move, so "he vanishes when attacked" would break that. *Question for the owner:* when a character attacks Vell before the Crossing, what does the table see? (a) The blow simply misses, every time, and nobody sees how. (b) The attacker finds they don't go through with it. (c) Something else you prefer. Or (d) he can be struck but shrugs it off, which would need numbers.
2. **The blank alignment on the Uninvited and Vell (BESTIARY-21).** INVENTIONS #44 says pass 2 chose "Alignment —" over ruling on their morality. The blocks print nothing at all. *Question:* print the dash, or keep it blank with a one-line note in How to Read? This is not asking for an alignment.
3. **The Circle knife's coat (BESTIARY-23):** give it a GP value, or leave it unvalued as flavour?
4. **"MM" for "DM"** is not filed here. It appears only a few times in this chapter, and the owner is already being asked about it.
