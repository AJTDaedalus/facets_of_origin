# DESIGN: Oraga Night 5e, three-player pass

*Planner/Brain, 2026-10-20. Input: `docs/REVIEW_oraga_5e_3p.md` (§0–§7) and the five reports in
`docs/audit_oraga_5e_3p/`. Scope: `conversions/dnd5e/oraga_night/` only.*

This document records the owner's rulings of 2026-10-20 and turns them into mechanics a Worker
can implement. Open rulings are listed in §5. `TASKS_oraga_5e_3p_pass.md` follows once §5 is
answered.

---

## 1. Owner rulings, 2026-10-20

| # | Ruling (the owner's words where quoted) |
|---|---|
| **TP1** | **The owner will run it for three players.** The pass tunes for three 4th-level PCs. *Whether the three-player numbers become the printed baseline, with four as the adjustment line, is a Planner proposal awaiting the owner (§5 Q5), not a ruling* |
| **TP2** | **Up the risk, all seven options** (REVIEW §7.1): "Up the risk with all of these options, leave it to the DM to determine how hard to go after players." |
| **TP3** | **Slow / Stop / End is approved** (REVIEW §7.2) |
| **TP4** | **The Radiant gets a real weakness:** "using his emotion against him" |
| **TP5** | **The Attendant can kill** |
| **TP6** | **The Uninvited can kill too,** "but they don't see most people as threats so are unlikely to" |

**What these supersede:**
- **Chapter IX's rule 2,** "no snake ambushes a character, and no snake is the reason a
  character dies before midnight": retired by TP2.
- **"Deadly but not lethal"** for the Attendant (FIXPLAN §5): retired by TP5.
- **"A character is only ever in mortal danger by choice"** (05:27) and "Down, Not Out" as a
  blanket mercy: replaced by TP6's threat rule (§3).

**What stays:**
- **R3, knocked-out characters come back.** The crowd and the party still haul people up; the
  difference is that death is now possible on the way.
- **R4, creativity beats force.** TP3 is its implementation.
- **R6, the heir stays secret.**
- **"The Uninvited cannot be killed tonight."** *Leashed* is unchanged.

---

## 2. Risk: all seven options, under one DM dial (TP2)

### 2.1 The dial

A box in chapter I, "How Hard to Go", gives the DM three settings. One word on the DM sheet
records the choice. The book's numbers are written at **Sharp**.

| Setting | Snakes | Dying | Uninvited | Attendant |
|---|---|---|---|---|
| **Gentle** | Ambush only with a tell shown first; finish nobody | Before midnight a drop costs something (2.3) but never kills; after midnight the crowd rule covers everyone | Mark threats slowly (3.1); never finish | Finishes nobody |
| **Sharp** *(default)* | Heat 4 ambushes; heat 4 finishes a downed character who crossed it | Normal dying rules everywhere after midnight; the crowd rule covers only creatures the Uninvited set aside | Mark on the printed triggers; finish a marked creature only if it is still in the way | Focused, it finishes a creature that interrupts again |
| **Merciless** | Any heat-3+ faction ambushes; finishes whoever crossed it | No crowd rule in fights; death saves rolled in the open | Mark on the first trigger; finish marked creatures | Finishes any interruption |

The dial is announced to the table at session zero in plain words ("tonight the knives are
real"). It is not a secret difficulty.

### 2.2 The seven options as text changes

1. **Snakes come for the characters.**
   - Chapter IX's rule 2 becomes: "Every ambush is foreshadowed. No snake moves on a character
     whose tell the table has not been shown."
   - Each faction line gains one *Heat 4: they come for you* row, naming who, where, and which
     card it uses.
   - These reuse existing cards. For example, the Circle's knives are S7's roster in a service
     passage, and Draunel's duelists are S9's roster on the terrace.
2. **Dropping costs something before midnight.** "Death before midnight" (09:544) gains a cost
   table, rolled or chosen per drop:
   - robbed of an agenda item or a crystal charge;
   - held, so the character misses the next beat;
   - marked for the inquest;
   - wakes in the gatehouse cell (S3's cell already exists).

   It still never kills, at every setting.
3. **Lethal after midnight.**
   - 09:549–552 is rewritten. Normal dying rules apply in every snake and Bought fight.
   - The crowd rule now covers only creatures an Uninvited set aside (§3.1).
   - At Sharp, a snake at heat 4 *does* finish a downed character who crossed its line.
4. **The Attendant can kill.** See §4.
5. **Live by default.**
   - The "If the table does nothing" heats (09:475) move up so that **two** cards are live in
     the dark by default, S11 and one other. The recommendation is S12 (the Circle), which
     needs only the Circle's start to move from 1 to 2.
   - Table VIII–2 and the flow graph follow.
6. **Budgets at three PCs (750 / 1,125 / 1,500).**
   - Before-midnight cards go to Low or Moderate; after-midnight cards to Moderate or High.
   - Morale triggers on after-midnight cards move from "first foe drops" to "half down".
   - The REVIEW §4 softening fixes are **withdrawn**. S8, S10 and S3 keep their rosters, and
     their labels are corrected upward instead.
   - New three-player rosters are built and re-simulated per card (the TUNING_3P method).
7. **Resources, so that risk is fair.**
   - **A chapel short rest:** it costs half a Movement and advances every visible snake clock
     by one.
   - **One Hit Die** each at the toast.
   - **One healing potion per character** among the ball's loot (Table X loot), placed where
     a party exploring finds it.

---

## 3. The Uninvited: Slow, Stop, End (TP3, TP4, TP6)

### 3.1 The threat rule (TP6), replacing "Down, Not Out" for the Uninvited

The Uninvited see most people as furniture. A creature becomes **a threat** to one of them when
it does one of these:
- lands a **Stop** on that Uninvited;
- earns Delay against it **three times in one scene**;
- deals its **last blow** (the *Leashed* throw).

The DM says it aloud: *"She looks at you — properly, for the first time."*

- **Not a threat:** at 0 HP the creature is set aside, Unconscious and Stable, and the crowd
  rule applies. This is the current text.
- **A threat:** normal dying rules apply. At Sharp, the Uninvited finishes a marked creature
  only if it is still between them and their errand on their next turn. Otherwise they walk
  on, because they have somewhere to be.
- **The quarry** (Raunu, Veier) is unchanged.
- **Mark status lasts the scene.** "Unlikely to" holds because marking takes real
  interference, and finishing takes staying in the way.

### 3.2 Slow (Delay): any creativity

These rules replace the current "Earn it by being clever" rules (05:250) and the "nothing
bought" rows (10:148–152).

- **Any creative action that lands earns 1 Delay:** a skill check (DC 13), an attack, or a
  spell. Repeats keep the current rule: DC 15 the second time, never a third.
- **Spells roll.**
  - A spell with an attack roll or a save uses that roll, and *Centuries of Practice* can
    refuse it 3/day.
  - A spell with neither is a trick check, made with the caster's spellcasting ability against
    DC 13. This fixes RULES P1-2.
- **Spells that land always buy 1 Delay,** once per spell per Uninvited. This includes the
  control list that buys nothing today: *Hold Person*, *Sleep*, *Hideous Laughter*, *Command*,
  *Charm Person*, *Suggestion*, *Calm Emotions*, fear, and *Web* or a grapple on the Wept or
  the Hollow.
  - The fiction: the leash snaps them out of it at once, but the moment is bought.
  - Condition immunities stay. The spell's effect ends at once, and the Delay is the whole
    payoff. This fixes RULES P2-1.
- **Theme pays double.** A trick or spell that plays to that Uninvited's nature (3.5) earns
  **2 Delay** instead of 1.
- **Damage lumps:** 20 damage in a round at three PCs (30 at four) is 1 Delay. Unchanged.
- **Cap:** an Uninvited loses at most **three turns per scene** to Delay. Delay beyond that
  gets **named people out** (Table V–1's "each point" column) and never stalls them further.
  Changing history is End's job (REVIEW §7.2, A3).

### 3.3 Stop: the scene effect, no clue required

A Stop is reached by any of three routes:
- **(a) Words that reach the person:** an action within 30 feet where they can hear, using any
  skill the words fit, DC 15.
  - Witnessed tells give **+2 each** (+4 at most), the Attendant's model.
  - The Intimidation and Deception bans are lifted for Stop, except where the creature's
    nature makes a skill pointless (the Hollow and Intimidation, 3.5).
- **(b) Three thematic successes** against the same Uninvited in one scene.
- **(c) A room effect the text already gives as a freeze,** such as the child crying for the
  Wept.

**Every Stop:**
- earns **2 Delay**;
- makes the speaker a threat (3.1);
- **can be used once per scene per Uninvited**, not once a night.

A failure by 4 or less still lands, at a cost: the parting blow, now under the threat rule. A
failure by 5 or more doesn't land, and the scene gets worse.

### 3.4 End: permanent tonight, needing a specific method

Each Uninvited's End needs **two or more witnessed tells** plus one specific method. The methods
are in 3.5. **The Root trap** (05:1124) stays a second End route for all three, unchanged.

**On a success:**
- **the End lands;**
- that Uninvited is out of the attack for the night, or its errand is forfeit, as 3.5 says;
- the speaker earns Heroic Inspiration;
- run the matching ⟨If History Breaks⟩ entry.

**On a failure:**
- the attempt counts as a Stop attempt instead;
- the End can be tried again after a new tell.

### 3.5 Per Uninvited

The themes come from each Fracture's printed "Truth" (05:773–818). Nothing in them is new canon.

| | The Wept *(sorrow)* | The Radiant *(devotion)* | The Hollow *(despair)* |
|---|---|---|---|
| **Theme (Slow pays 2, three = Stop)** | Children, mothers, mourning, mercy, a family kept together: the child crying, the cradle-song, an offering in the old rite, guests shielding their children | Being watched, worship, duty, light, ceremony: an audience, a rite, a better performance, darkness that steals his witnesses | Belonging, permission, honesty, people who have each other: answering him truly, two who belong together, a name called, an object handed to him |
| **Stop effect** | She freezes for one full round: no actions, no Bonus Actions, no Reactions, no movement (the current Fracture effect) | He **falters** for the rest of the scene: Speed 20, Shadow-Step once a minute (the current guilt effect, scoped to the scene) | He steps off the doors for one round: *The Post* doesn't apply, and the crowd pours through |
| **End (2+ tells + method)** | **Mercy:** with two tells, a plea that names what was done to her family and offers her the chance not to do it to another. She leaves the dais. → ⟨They save Raunu⟩ *(subject to §5 Q2: Raunu's own choice)* | **His devotion turned on him (TP4).** See 3.6 | **Permission:** what is printed now, "tell him… he can stop". He opens his hands and goes home. Intimidation never works on this |

### 3.6 The Radiant's weakness (TP4)

His printed nature (10:1444–1505, 05:784–807):
- worship must be witnessed to count;
- he poses when watched, and re-stages a kill nobody saw;
- he cannot resist dancing beautifully where the light falls;
- he "can only be made to feel".

TP4 asks for his emotion to be used against him. **Recommended End, "The Last Rite":**
- **Trigger:** with two tells, a character gives him a **congregation and a liturgy worthy of
  it**. That means a lit room, watchers, and a rite or performance to which his devotion must
  answer (Charisma (Performance), or Intelligence (Religion) for a rite).
- **Effect:** he stops hunting to officiate. His devotion will not let him leave a congregation
  that is waiting on him.
- **Duration:** he stays, performing, while anyone keeps the rite going. That takes one
  character's action each round, with no check.
- **The ending:** if the rite lasts until the boat is out of reach, the leash takes him at the
  altar he made.
- **Canon fit:** this keeps the printed line "cannot be turned" literally true. He never
  abandons the errand; his worship forfeits it. It also gives the Crossing a real stake
  (REVIEW A4).

**Alternative (owner choice, §5 Q1), "The Broken Faith":** "plant the doubt" with two tells
and a believer breaks his faith outright. He kneels and stops. This overrides "cannot be
turned" (10:1421).

### 3.7 What gets deleted or merged

- Table V–6's DC rows (18 with one tell, 15 with two) become +2 per tell.
- "Each Fracture works once" becomes "End once; Stop once per scene".
- Chapter X's spell table becomes a short "what spells buy" list, using one rule: *lands → 1
  Delay; on theme → 2*.
- The Intimidation/Deception ban moves into the Hollow's End only.
- The "nothing bought" framing goes. 10:128, "the blocks close every door a clever table will
  try", is rewritten as "every door a clever table tries opens a little".
- The tells go onto the run path (REVIEW A1): the DM sheet and chapter IV, by Movement.

---

## 4. The Attendant can kill (TP5)

- **Its "Down, Not Out" trait is replaced:**
  - *Idle:* a creature it drops is set aside, Stable (it isn't trying).
  - *Focused:* normal dying rules.
  - At Sharp, a Focused Attendant attacks a downed creature only if that creature interrupted
    the three since its last turn. Its orders are about interruptions.
- ***Clears the Way* (fixes the RULES P1-1 Idle-lock).**
  - An adjacent enemy no longer stops it.
  - Instead, clearing the way **costs the action** of one of its turns. Idle, it clears the way
    when nobody has struck it since its last turn. Focused, it attacks on its first turn and
    clears on its second.
  - Timing: at the start of the turn it uses.
- **Distraction at three PCs:**
  - **Help applies** to a distraction, which rewards teamwork.
  - Focused DC **18**, re-simulated.
  - The bonuses and the four-broken-focuses win are unchanged.
- **HP:** 180 at three PCs. Whether the block prints 180 or 229 depends on §5 Q5.
- **Re-simulate S14** under the threat rule and lethal Focused drops.
  - **Targets, at Sharp:** engaged-distraction win ≥ 85%; a PC death ≤ 10% for an engaged
    party; a slugging party mostly loses, with death a real possibility.
  - Report rates at each dial setting.

---

## 5. Rulings answered 2026-10-20 (TP7–TP10)

| # | Ruling | Consequence for the text |
|---|---|---|
| **TP7** | **The Radiant's End is "The Last Rite"** (3.6). "The Broken Faith" is not used | "Cannot be turned" stays as printed. The Crossing's stake becomes the Last Rite plus the threat rule (3.1): at 0 Delay and with no rite, the Radiant can now genuinely kill whoever is marked at the gate. Delete "the margin should be the characters, not luck" (05:602) unless the rewrite makes it true. LOGIC L4's options (a)–(c) are not adopted |
| **TP8** | **The Root** (owner's words): "The root was made for another purpose, a part of the research he did into the gifts. It's affect on the uninvited is tangential. They also don't know to avoid it." | Raunu built the Root as his gift-research workshop, not as a refuge, so hiding Veier there is not part of his plan (answers LOGIC L1). **Its effect on the Uninvited is a side effect.** **The Uninvited don't avoid it.** Rewrite "the Uninvited will not go down there… will not cross its threshold" (05:50–55; 04:706–711; 10:172) so that an Uninvited who enters or is lured in is caught by the deep crystal, which is the Root-trap End (3.4). This also resolves LOGIC P2-12, the trap rule contradicting "will not cross". *Integrator's reading, to confirm with the owner: whether Raunu knows of the side effect at all is left unstated; the text should not claim he does* |
| **TP9** | **The garden doors:** the Hollow's *Post* covers both the main doors and the Court's garden doors; he shadow-steps between them | Answers LOGIC L2. *The Post* and *Only the Doors* name both sets of doors. Table V–3 trick 5 ("another door") is retargeted. The crowd leaves only by the service doors and the gallery-side door until he turns east or his Stop or End lands. When the garden doors open (his End, or after the Wept's work), the crowd reaching the gardens makes the Radiant *Witnessed* at the Crossing. That is a reward the text should state |
| **TP10** | **Three is the printed baseline** | Stat blocks, cards, Table V–1, the DM sheet and the tracker print the three-player numbers. Four and five become the adjustment lines (reversing R2's four-player baseline). Table IX–1 is reordered |

| **TP11** | **Canon correction** (owner): "Raunu doesn't send Veier away by boat, he plans to keep her there until the child is born." | The module already gives the boat, gate and garden to Master Vell (02:188–227; 07:529). Raunu's last charge buys her escape from the attack, not a planned departure. The audit's "sends her off by boat" (LOGIC L1, REVIEW A7) was a misreading, now corrected in both. **Add the plan to chapter II, "How the Night Ends" or "Why the Ball":** Raunu meant to keep Veier in the sealed east wing until the birth. That gives the DM the answer to "why is she upstairs?" Then propagate to 07 (Raunu, Veier), `facts.yaml` and `flow.json` in the same pass |

| **TP12** | **Canon** (owner): Vell "organises flight by steed, not by boat… towards the mountains to the west"; then "It can stay a boat heading north up the tributary towards the foothills, where he's arranged horses." | The boat, the river gate and the Crossing are unchanged. **Applied now** to both editions (5e 02, 05, 06; Facets 02, 05, 06): the trail's carter step becomes the empty boat and a horse-line in the foothills, with tracks going west. TP11's line on Raunu's plan was added in the same edit. `facts.yaml` escape_route guards both. Checks green (fact_check 0, lint 0, tools 422 passed, Facets docs tests 37 passed) |

**Still open:** none. The east-wing route, the unborn child and the nursery sale are answered by TP13, TP15 and TP24 (§6).

## 6. Rulings on the findings ledger, 2026-10-21 (TP13–TP26)

Answers to `docs/LEDGER_oraga_5e_3p.md` §6. These close the "still open" list above.

| # | Ledger | Ruling | Consequence for the text |
|---|---|---|---|
| **TP13** | R-01 | **Veier is never met directly** (owner: "Veier is supposed to remain mysterious, she can be met through the door, but not directly"; confirmed: never directly, all night) | Agenda 4 is done through the east-wing door, and its "beside Veier at the Unmasking" note is reworded: at midnight she listens for that character's voice through the door. In the east-wing chase and at the Crossing, Vell and the household move her; the party holds the Radiant off from doors, corridors and garden, and no character escorts or touches her. Rewrite Table V–4 tricks 1 and 5, Table V–5 trick 3, the Crossing steps (05:585–597, the Speed 15 note) and any read-aloud that puts her in reach. *Integrator default, to confirm in TASKS: only the double doors at the head of the east stair seal; the service and garden stairs stay open as drawn, as the party's routes to intercept the Radiant* |
| **TP14** | R-02 | **Acting early: history holds, with payoffs** | Veier and Raunu refuse to move, in character (TP11). Each early act gets a visible midnight payoff: guests moved early are not among the dead, a warned character starts in position, a convinced Corval opens a door. 01:423–425 keeps its promise through those payoffs |
| **TP15** | R-03 | **What the Radiant does at the Crossing is left unstated** | "The module does not say." DM line: never narrate an attack on Veier herself; his violence goes to whoever is marked under the threat rule and stands in his way |
| **TP16** | R-05 | **The Wept's End buys Raunu's choice, at a price** | When Mercy lands, Raunu spends the twin crystal on himself and lives, so "by his own choice" stays true. The doors behind Veier do not seal: the Radiant gains beats on her, and the party is all that stands between them. Gives L-005 its numbered steps |
| **TP17** | R-06 | **The Attendant enters the Root, unaffected** | It goes wherever its three go; the Root traps only the Uninvited. No new safe room |
| **TP18** | R-07 | **Raunu does not know the Root catches the Uninvited** | One DM line: nobody has seen the effect until creatures like these stand in it. Supersedes TP8's integrator note |
| **TP19** | R-08 | **Vell's sword stays on his back** | He holds the Radiant off without drawing it. Chapters VII (07:520–522, 566) and X (10:2141–2142) change; chapter V and the INVENTIONS #66 read-aloud stand |
| **TP20** | R-09 | **"Both rivers, one spring" stays gated** | No echo elsewhere. A DM note says most tables won't see it |
| **TP21** | R-10 | **Cut "and send word to the river"** | The Second Clause ends at "hold her" (05:965; 07:749) |
| **TP22** | R-11 | **Mid-tier NPCs get speech habits only** | One habit each for Kovaun, Callun, Draunel, Essin, Maiven, Anha, Tavva and the two Bought officers, drafted strictly from printed traits, for owner approval. No sample quotes |
| **TP23** | R-12 | **Place the midwife and the two Tithe ministers, unnamed** | Positions on Tables VIII–2 / VIII–6; the ministers stay "the elder" and "the younger". Claude proposes positions from the existing map; the owner approves |
| **TP24** | R-04 | **The nursery sale: a midnight beat and an aftermath** | At heat 4 the Circle's knives go for the east wing's service door in the dark, into the Radiant's path (a "they come" row reusing S7's roster). Chapter VI gains a line that the Circle knows, as the exception to "the pregnancy never gets out"; the owner words that consequence |
| **TP25** | — | **History breaks at the boat only by stopping the boat** | Follows TP13. A character can stop the boat or bar the river gate, from a distance; "holds Veier back" is removed from ⟨If History Breaks⟩ (05:1110) |
| **TP26** | R-13 | **Handout 1 stays as written, with no note** | No change |
| **TP27** | E1 (TASKS) | **Cut Dinner for Two** | Follows TP13. The face-to-face dinner in B9 is cut. Agenda 4 is done entirely at the east-wing door, a guard carrying word up and Veier's answer back; at midnight she listens for that character's voice. The heir is found only through Undercurrent C's other clues. INVENTIONS #58 and #72 are superseded. How the ring travels (through the guard, or kept at the door) is a derived detail to log for owner review |
| **TP28** | C1 (TASKS) | **Only the double doors at the head of the east stair seal at the lights** | The service stair and the garden stair stay open as drawn, as the party's routes to intercept the Radiant. The inner doors still lock behind Veier on Raunu's last charge, as printed (TP16 depends on them) |
| **TP29** | C2 (TASKS) | **The S4 roster cut is withdrawn too** | S4 keeps its full roster; its label is corrected upward (L-016) |
