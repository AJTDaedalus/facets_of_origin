# REVIEW 3: Oraga Night 5e for three players

*2026-10-20, at `b254fb0` on `feat/lean-facets`. The owner asked for a full and very critical audit
for a table of **three 4th-level PCs**, judged on tuning, voice and sense against the reference
modules (Curse of Strahd, Lost Mine of Phandelver, Death House, Storm King's Thunder, AL DDEX1).*

Five independent auditors produced the evidence, each in `docs/audit_oraga_5e_3p/`:

| Report | Lens | Score |
|---|---|---|
| `TUNING_3P.md` | Every fight at 3 PCs, with Monte Carlo sims and expected-damage math | 7.0 |
| `RULES.md` | Stat blocks, pregens, module-invented rules, exploits (against SRD 5.2.1) | 6.5 |
| `LOGIC.md` | Motive, clue paths, causality, agency, endings | 6.5 |
| `VOICE.md` | Read-aloud, DM prose, NPC voice, tic rates against the references | 7.0 |
| `USABILITY.md` | Simulated 90-minute prep and a Friday session from the DM sheet | 5.5 |

The headline findings below were checked against the text by the integrator, and the check is
noted on each. Each report has full file:line evidence and exact fixes.

---

## 0. Verdict

**6.5 / 10 as a module you can run for three players next session.** It is not yet at the
reference bar, though it beats the references in several places.

This score and Review 2's 8.0 measure different things:
- Review 2 graded the *book* for four players.
- This review asks whether a DM can prep it, run it for three, and have it hold up when players
  are clever.
- The production polish Review 2 credited is real and still there.

**What already meets or beats the references:**
- **Arithmetic.** Every stat block's HP, AC, attacks, DCs and damage are correct, and all five
  pregens are legal 2024 builds. The repo's checkers and the hand derivations agree.
- **Encounter budgets.** The 4th-level SRD 5.2.1 row (250/375/500 per PC) is right in Table
  IX–1.
- **Three-character lines.** Every fight card has one, which is more scaling support than WotC
  usually prints.
- **The social night.** The six snake threat lines, the heat tracker, the cast's motives, and the
  "impossible guests" mystery with its Fracture tells hang together.
- **Read-aloud.** It is short (63–81 words), concrete and speakable.
- **Top-tier NPCs.** Raunu's summons Q&A and the Vorlain and Corval blocks are more runnable than
  the CoS Vallaki pages.
- **Tone.** The identity ("glamour over a blade", the snakes in the chicken pen) is strong.
- **The boss.** S14 holds its odds at three. A table that plays the distraction game wins 90–96%,
  and the chance a PC drops in round one falls to 18–25% (36–49% at four).

**What keeps it below the bar falls into five themes:**
1. **The climax's levers are off the run path, and its subsystem breaks under clever play.**
   - The Fracture tells are not where the DM runs from (§1, A1).
   - Spells buy Delay for free, and the Attendant can be locked Idle (A2, A3).
   - The Crossing cannot fail (A4).
2. **Three players is a sidebar, not a mode.** The numbers the DM reads at the table are the
   four-player ones, and there is no cast guidance below four (A5, A6).
3. **The night's hinges do not survive scrutiny.** Raunu's motive, the garden doors and the
   midnight east wing are the problems (A7–A9).
4. **Prep and runtime are oversold.**
   - The 90-minute prep is really about 138 minutes as written, and 3 hours in practice.
   - The 4 h 50 runtime is really about 5 h 40 at three.
   - The book is ~100,000 words, against 8,500–15,000 for the session-length references (A10,
     A11).
5. **The DM prose still has a machine rhythm,** and roughly 40 invented terms with no glossary
   (A12, A13).

**Counts, deduplicated across reports:** P0 **1** · P1 **13** · P2 ≈ **30** · P3 ≈ **45**.

---

## 1. P0: will derail the session if the book is followed literally

### A1. The Fracture tells are not on the path a DM runs from *(USABILITY P0-1; verified)*

The Fractures are the climax's main lever, and each needs a tell witnessed during the ball. The
tells are listed only in **Table V–6** (`05_The_Longest_Night.md:765`), plus two lines in chapter
VII. None appear:
- in chapter IV's Movement text (a search for each tell phrase in `04_The_Ball.md` returns 0);
- on the DM sheet, which prints the Fracture *rule* (`08_Handouts.md:83`) but not the tells;
- in the prep box.

A DM running from the sheet, as the README instructs, reaches midnight having shown almost none.
The DCs are then 18 instead of 15, and the Wept's and Radiant's arcs never land.

**Fix:** add a "Tells to show" column on the DM sheet by Movement, and one tell bullet in each of
Movements III, IV and V in chapter IV. About an hour of work, and the largest single gain.

---

## 2. P1: real defects at a three-player table

### The climax subsystem

**A2. Spells and cantrips buy Delay with no roll** *(RULES P1-2; verified)*. The source is
`05:254`, "A spell is a trick like any other: if it lands, that is the success".
- Any spell with no attack roll or save auto-succeeds, cantrips included, twice per Uninvited.
- Andra's cantrips alone are about 10 free Delay per Uninvited.
- Chapter X (`10:164-166`) says a trick earns Delay "when its check succeeds", so the two
  chapters disagree.

*Fix:* a spell trick is a check like any other, made with the caster's spellcasting ability.
Cantrips get Disadvantage, or count as the same trick each time. Make chapters V and X say the
same thing.

**A3. The Idle-lock** *(RULES P1-1, TUNING Delay stall; mechanism verified)*. The Attendant is
Focused only when an Uninvited in the scene has no Delay. *Clears the Way* (its only Delay
removal) switches off whenever any enemy is within 5 feet (`10:217-260`).
- With three PCs, one stands next to the Attendant and takes a weak Disadvantage swing each
  round.
- The other two make the 20-damage lump and turn a ward-point.
- Delay then grows faster than it drains. The sims show the Wept stalled for 5.3–5.9 of 6
  rounds, and the party grinds the Attendant down for full XP.

⟨If History Breaks⟩ (`05:1083`) does cover a runaway Delay outcome, so this is an exploit, not an
undefined hole.

*Fix (TUNING F10 / RULES):* an Uninvited loses at most three turns per scene to Delay, and spare
Delay saves guests instead. *Clears the Way* works from up to 30 feet, so adjacency only
disadvantages it. It also needs a timing ("at the start of its turn").

**A4. The Crossing has no fail state** *(LOGIC L4; verified)*. The prose says "the margin should
be the characters, not luck". The rules text two paragraphs later says the opposite: "Either way,
the escape holds" (`05:597-611`). Every Table V–5 trick at the river gate buys nothing a player
can feel.

*Owner ruling needed:* either the margin is real (with no Delay and no body at the gate, the
Radiant gets one attack at the boat, with consequences short of the child being taken), or the
book says plainly that the escape is fixed, and the stake moves to *who else* reaches the boat.

### Three players as a real mode

**A5. The numbers the DM reads are the four-player ones** *(USABILITY P1-3, TUNING; verified)*.
The three-player values sit in a sidebar:

| Value | 4 PCs (printed on the DM sheet / in chapter X) | 3 PCs (sidebar only) |
|---|---|---|
| Damage per point of Delay | 30 (printed in five places) | 20 |
| Wept reaches Raunu | 3rd turn (Table V–1) | 4th turn |
| Attendant HP | 229 (stat block) | 180 |

There are 12 hand-applied adjustments in total.

*Fix:* print both columns on the DM sheet, on the Midnight Tracker (A11) and in the S14 block.

**A6. No cast guidance below four, and Agenda 4 is mandatory in practice** *(LOGIC L7, TUNING;
verified)*.
- Chapter V leans on a PC beside Veier (Agenda 4).
- The fallback route into the wing (Anha's passages) runs into S7's guard.
- A fighter, rogue and wizard trio has no healer and drops Agenda 4.
- Several scenes trigger off agendas a trio won't hold.
- A lone PC who walks into a Dead Dance card faces the whole roster, because the rule is "one
  card per group" and no card has a one-PC line. That PC drops 71–100% of the time.

*Fix:* a "Three at the Table" box in chapter I.
- **Recommended trio:** Dassa, Ilesse and Serane, with Agendas 4, 8 and 2 dealt openly. For more
  fights, swap Serane for Pello. Never drop Ilesse.
- Agenda 4 is always dealt.
- Size each card to the PCs actually present, and add a solo line to S2, S7, S8, S9 and S10.

### The night's hinges *(LOGIC; each needs an owner ruling)*

**A7. Raunu's motive (L1).**
- He knows something is coming by Movement III.
- He owns the Root, a room the Uninvited will not enter, and Veier has sat in it.
- Yet he keeps her upstairs, and the text never says why the Root isn't used.
- *Corrected 2026-10-20 (owner): Raunu does not send her away by boat. He plans to keep her
  in the palace until the child is born. The boat is Master Vell's preparation, which the
  module already says (02:188–227; 07:529). The Root question is answered by TP8.*

This is the first thing a clever table asks.

**A8. The garden doors (L2).** Nothing closes them at midnight, and they lead through the gardens
to an unlocked river gate. That breaks two set pieces:
- the gate fight's premise (200 guests trapped at a barred gate);
- the Crossing's "dark, empty terraces".

**A9. The east wing at midnight (L3).** No route in is given once the wing seals. The Agenda 4 PC
has already been shown out at the Dead Dance. Review 2's open geometry item N4 (gallery stairs,
"second floor" against "gallery level") now feeds A8, A9 and S11's door.

### Divergences the book promises but does not run

**A10. ⟨They save Raunu⟩ is the likeliest divergence and has no procedure** *(LOGIC L5, RULES
P2-7)*.
- Two DC 10 ward-points get the Wept to 2 Delay, which drops her Fracture to DC 15.
- Success at a cost lands even a miss by 4, so Serane succeeds about 90% of the time.
- After the Wept's one-round stop, there are no rules for what happens next.
- The "real sacrifice" the sidebar asks for cannot happen under "Down, Not Out".

"Act before midnight" (L6) is promised as the solvers' reward, but warning Corval or Raunu changes
nothing. Getting Veier out early, or into the Root, is not covered at all.

### Product

**A11. No midnight tracker** *(USABILITY P1-2)*. About 20 values change at once, and nothing gives
the DM a place to record them:
- Delay on each of the three;
- the Wept's turn count;
- the Attendant's state and broken-focus count;
- tells seen;
- ward-points used;
- the two gate clocks.

*Fix:* a one-page Midnight Tracker with check boxes and both party-size columns.

**A12. Prep and runtime are oversold** *(USABILITY P1-1, P1-5)*.
- **Prep:** the box needs ~138 minutes as written, and 175–205 counting what it implies. It
  contradicts itself on chapter VII and leaves out S11, the one card live in the dark by default.
- **Runtime:** at three it is ~5 h 40 (range 5 h 05 to 6 h 25). S14 alone takes 40–60 minutes and
  is missing from the cut list.

*Fix:* cost the prep honestly, add a true 60-minute path with a five-block list, add a
three-player runtime column, and cap S14 at about six rounds.

**A13. Lethality after midnight is a hidden cliff** *(TUNING F3; verified as designed, flagged
for awareness)*. After midnight, snake damage is lethal and death saves apply (`09:546-550`). The
crowd rule rescues only Stable characters. A trio that fights S13 and then S3 to the end loses a
PC 15–21% of the time, and there is no rest after midnight. That may be intended, but the DM is
never told the price.

*Owner ruling:* keep it, with a warning on the DM sheet, or have snakes drag the downed clear,
Stable (TUNING F3).

---

## 3. Voice *(VOICE.md, 7.0)*

The book has a voice, and an identity a CoS reader would recognize as good. Keep the read-aloud,
the top NPC blocks and the tone.

The DM-facing prose carries a measurable machine fingerprint against the references:

| Per 1,000 words of running DM prose | Module | References |
|---|---|---|
| Mid-sentence colons | ~6.7 | 0–1.3 |
| Semicolons | ~5.9 | ~0.2 |
| "X, not Y" reframes | ~1 | 0 |
| Sentences of ≤6 words | 15–19% | 9–11% |

On top of the rates:
- **Moral kickers:** about 26 short closing lines.
- **Recycled flourishes:** about ten recur word for word across chapters ("struck glass",
  "acquires teeth", "rumor has no shelf for it").
- **Designer commentary on the DM page:** "a load-bearing sentence, not a gap"; "This is the
  crescendo".
- **Missing read-aloud:** B5 (the gardens, where the Crossing happens) and B8 (the study) have
  none.
- **Thin mid-tier NPCs:** Kovaun, Callun, Draunel, Essin, Maiven, Anha, Tavva and the Bought
  officers have traits but no lines to speak.
- **Jargon:** about 40 invented terms, where LMoP has almost none. Chapter I uses Delay, Fractures
  and the Wept before defining them, and "tell", "line", "clock" and "iron" are overloaded.

*Fix:* a de-patterning pass judged by ear (~150–250 sentence edits; 22 worked rewrites in
VOICE.md), a "Words of the Night" glossary box, one sample line per mid-tier NPC, and read-aloud
for B5 and B8. Estimated result: about 8.5.

---

## 4. Tuning at three: card by card *(TUNING_3P.md §3)*

| Card | At 3 PCs | Verdict | Fix |
|---|---|---|---|
| S1, S5, S6, S7, S11, S12 | Under Low, play as labeled | OK | — |
| S2 Service Corridor | OK as a group; a solo PC drops 71–100% | P1 when alone | Solo line; the box says "four people" |
| S3 Gate | 850 XP; with the captain, 1,950 = 1.3× High | Harsh for trios with no front line | Captain arrives at the start of round 4 at 3P |
| S4 East Wing Doors | The only card with no 3P reduction (900 XP) | P2 | One guard, the second in round 2 |
| S8 Study Door | 20–57% chance of a drop; "break at two down" means two of three | Plays Low–Moderate | Break when one is down |
| S9 Appointment | Easier than at 4P | OK | Clarify the one-side rosters |
| S10 Over the Wall | 44–82% chance of a drop; labeled Low | **Plays Moderate** | Maiven + 1 slinger, and Maiven makes two attacks |
| S13 Arrest in the Fire | XP fine; PC death 2.7–6.4% | Rules gap (A13) | Dying-rule fix |
| S14 Attendant | Distraction play wins 90–96%; naive play 57–75%; slugging 0–34% | **Well tuned** | Fix the label ("2.6× High" at 3P); 235 HP for a trio built to hit hard; fix A3 |

**Attrition.** A party that takes S14 plus one snake fight reaches the gate at about 15–20% of its
HP. *Fix:* at most one snake card after midnight besides S11; the chapel rest takes half a
Movement; each PC may spend one Hit Die at the toast.

**Read-aloud head counts.** S2, S11 and S13 describe more enemies than their three-character lines
field.

---

## 5. Rulings the owner needs to make before a fix pass

These block the fixes in §2. Each comes with options in LOGIC.md, RULES.md and TUNING_3P.md.

1. **Why doesn't Raunu hide Veier in the Root?** (A7) A one-line reason, or let the Root
   be a real option.
2. **The garden doors at midnight** (A8): sealed by the first crystal, jammed by the crowd, or
   held by someone?
3. **The route into the sealed east wing** (A9), and whether the Agenda 4 PC stays inside after
   the Dead Dance.
4. **Can the Crossing fail?** (A4)
5. **Saving Raunu** (A10): how hard should it be, and what happens in the rounds after?
6. **Lethality after midnight** (A13): keep it with a warning, or soften it?
7. **Delay caps** (A3) and **spell tricks need a roll** (A2). These are rules choices, not canon,
   and recommended as written above.
8. From LOGIC: what the Uninvited meant to do about the unborn child (P2-5); the nursery sale
   kidnapping a minister (P2-11); whether the Attendant enters the Root (P2-12).

---

## 6. Recommended order of work

1. **Friday-critical, no rulings needed (about one working session):**
   - A1, the tells on the run path;
   - A5 and A11, a Midnight Tracker with both party-size columns;
   - A6, a "Three at the Table" box with the recommended trio, solo lines and card sizing;
   - A2 and A3, the Delay rule fixes;
   - the §4 card fixes (S3, S4, S8, S10, S14 HP).
2. **Owner rulings** (§5), then the logic fixes (A4, A7–A10) and the N4 geometry. Add
   `facts.yaml` entries so the fact checker holds each decision.
3. **Prep and runtime honesty** (A12): a 60-minute path, a three-player runtime column, the S14
   cap, and a print build (DM packet, player packet, card deck).
4. **The voice pass** (§3), by ear, after the content settles, so it isn't done twice.

**Expected result:** the table is ready after step 1. A score of 8 or more needs step 2. Reaching
the reference bar needs steps 3–4.

**What no edit fixes:** 100,000 words cannot be prepped in 90 minutes. The prep path and the
tracker pages have to carry the product.

---

## 7. Re-read against the owner's direction (2026-10-20)

**The owner's direction, in their words:**
- "the lack of combat risks outside of the uninvited is a major risk"
- "the inflexibility of needing to find 'clues' of how to deal with the uninvited is going to be
  a problem"
- "We should have multiple ways to stop each, with them being somewhat thematic but rewarding
  creativity. Dealing with them permanently can take a specific hint/method, but delaying,
  distracting, or avoiding them should reward creativity over the 'right answer'."

**Where it sits against the old rulings:**
- It restates ruling R4 of 2026-09-28 (`FIXPLAN_oraga_5e.md`): "against the Uninvited, creativity
  beats direct force".
- It reverses part of the 5e brief's "visible, optional" framing for the snakes
  (`BRIEF_oraga_5e.md` §1.2). Chapter IX hardened that framing into three rules: no ambush, no
  death before midnight, and everyone breaks first.
- It does not touch R3, "knocked-out characters come back". A character can come back and still
  have been at real risk.

### 7.1 Combat risk outside the Uninvited: what the text does now

| Layer | What the text says | Effect |
|---|---|---|
| Before midnight | No ambush; every fight visible and optional; "no snake is the reason a character dies before midnight" (`09:53-55`). A dropped character is Stable at once and wakes at the end of the scene with 1 HP (`09:544-547`) | Dropping costs a few HP and nothing else |
| Budgets | "Several snake fights sit at or below Low on purpose" (`09:99-100`). At 3 PCs, 9 of 14 cards are under Low (TUNING §3) | Most fights cannot threaten a fresh party |
| Morale | "every snake's people break and run long before they die for their master" (`09:56-58`) | Fights end before they turn dangerous |
| Default night | With no table action, **one** card is live after midnight (S11), plus the gate (`09:475-481`) | A party can reach dawn with one or two fights |
| After midnight | Lethal, with death saves, but "no snake finishes a downed character", and the crowd rule holds in every snake fight (`09:549-552`, `05:233-235`) | Death is possible only in the gap before the crowd arrives |
| The Uninvited | "Down, Not Out": they never kill | By design, and canon-compatible |
| The Attendant | "Down, Not Out" too (`05:428`). This was the Planner's "deadly but not lethal" (FIXPLAN §5); the owner's recorded wording was "extremely challenging, but not a guaranteed death sentence" | The night's only beatable boss cannot kill anyone |

**Verdict: the owner is right.** No layer of the night carries the risk of losing a character, or
of losing anything else that lasts. The only real lethality is optional (S3 to the last, or S13),
and the rescue rules blunt even that.

Three of this review's own recommendations push the wrong way under this direction, and are
withdrawn or reversed:
- **A13 is reversed.** The review offered softening as an option. Keep lethality after midnight,
  and make it *known* rather than hidden: say it at the table when the lights die.
- **TUNING F3 is withdrawn.** It had snakes drag the downed clear, Stable.
- **TUNING F5's cap is withdrawn.** It allowed at most one snake card after midnight. Replace it
  with resources (see below), not fewer fights.

**The card fixes in §4 are re-aimed.** S8 breaking at one down, Maiven with one slinger, and the
captain arriving in round 4 all made fights *match their labels* by softening them. The better
fix is to keep those fights as they are and **correct the labels upward**. Then raise the
under-Low cards so that each Movement offers at least one fight that can genuinely drop a PC.

**Options for the owner** (several can combine):
1. **Snakes come for the characters.** At heat 4, or when a character has crossed that faction's
   line, the faction moves on *them*. That gives the night at least one fight that is not chosen.
   This retires chapter IX's rule 2, "no ambush", in favour of "every ambush is foreshadowed by
   its tell".
2. **Dropping costs something before midnight.** A character who drops is held, robbed of an
   agenda item, marked for the inquest, or wakes in the gatehouse cell. It still never kills, but
   it matters.
3. **Lethal after midnight, in full.** The crowd rule covers only the Uninvited and the Attendant.
   In snake and Bought fights, normal dying rules apply, and a snake at heat 4 *does* finish the
   downed.
4. **The Attendant can kill while Focused.** It is not Leashed, and removal is its whole order.
   Death saves apply to its drops; Idle, it still sets people aside. This would fit "not a
   guaranteed death sentence" literally.
5. **Live by default.** Change the default midnight heats so that two cards are live in the dark,
   not one.
6. **Budgets.** Before midnight, Low to Moderate at 3 PCs. After midnight, Moderate to High. Move
   morale triggers later on the after-midnight cards.
7. **Resources, to make the danger fair.** A short rest is available in the chapel (half a
   Movement), and one Hit Die can be spent at the toast. Without these, raising the risk just
   means attrition.

### 7.2 Stopping the Uninvited: where clues gate and where creativity is refused

The core of chapter V already matches the direction. "Earn it by being clever, not by hitting
harder" pays 1 Delay for any creative action at DC 13, and the room tables are "prompts, not a
menu" (`05:250-258`). The Attendant's distraction rule is the model the owner describes: any trick
works, and the habits seen before midnight give **+2** bonuses rather than unlocking anything
(`10:235-244`).

The gates and refusals sit around that core:

| # | Where | What it does | Why it cuts against the direction |
|---|---|---|---|
| G1 | The "nothing bought" rows of chapter X's spell table (`10:148-152`) | *Hold Person*, *Sleep*, *Hideous Laughter*, *Charm Person*, *Suggestion*, *Command*, *Calm Emotions*, fear, *Polymorph*, and a grapple or *Web* on the Wept or the Hollow all buy nothing | These are the most common creative spells at 4th level. In the recommended trio, Serane's whole enchantment list (*Charm Person*, *Hideous Laughter*, *Calm Emotions*, *Suggestion*) is dead at the climax, and so are Ilesse's *Command* and Andra's *Sleep*, *Hold Person* and *Web*. The text's own framing is that the blocks "close every door a clever table will try" (`10:128`) |
| G2 | Fracture invocation (`05:742-751`) | Needs at least one witnessed tell; DC 18 with one, DC 15 with two or more; "Intimidation never works, and neither does Deception" | The scene-level effects (the Wept stopping for a round, the Radiant's guilt) sit behind a clue gate. Under the direction, only *permanent* outcomes should. Banning two whole skills also refuses creative approaches outright |
| G3 | The tells are off the run path (A1) | The DM may never show them | This compounds G2: the gate may have no key at all |
| G4 | Divergences (`05:1090-1136`) | Saving Raunu needs the Wept's Fracture, landed early. A trap needs deep ward-crystal, a ward-literate character and DC 18; "no spell does this"; one a night | These are the "permanent" outcomes, so a specific method is allowed. But each has exactly one route |
| G5 | Repetition | The same trick is DC 15 the second time and never works a third | Consistent with the direction, since it pushes variety. Keep it |
| G6 | The Attendant | Focused DC 19; one trick a round; Help doesn't apply | It already rewards creativity, but at three PCs with one try a round, DC 19 (15 at best with both +2s) is steep. Allowing Help would reward teamwork |

**The Fracture effects also sit in different tiers.** Each one does something of a different
size:
- **The Wept's:** a one-round stop, which is temporary.
- **The Radiant's:** slower for the rest of the night, and he won't break past Vell. That lasts
  the night, but it doesn't end his hunt.
- **The Hollow's:** he leaves the field, which is permanent for the night.

So the clue gate guards a temporary effect on one Uninvited and a permanent one on another.

**The proposed structure, for owner approval.** Three tiers per Uninvited, the same shape for all
three:

| Tier | What it does | How it's reached | Clue needed? |
|---|---|---|---|
| **Slow** (Delay) | Costs them a turn; each point is spent on people | Any creative action, skill, spell or attack that lands, judged by "does it fit the room and the moment". **Every spell that lands buys 1 Delay, once per spell per Uninvited**, including the G1 list (the leash shrugs it off next turn, but the turn is bought). Spells still need their roll (fixes A2) | No |
| **Stop** (scene effect) | The Wept freezes for a round; the Radiant falters and slows; the Hollow steps off the doors for a beat. Each also earns 2 Delay | Three ways: (a) words that touch the person, with no tell needed at DC 15; (b) **a thematic success**, meaning a trick that plays to their nature (grief and children for the Wept; audience and worship for the Radiant; belonging and permission for the Hollow), which earns 2 Delay instead of 1, and three of these in a scene trigger Stop; (c) the existing room effects that already freeze them, such as a child crying | No. Tells give **+2 each** (max +4), like the Attendant's habits |
| **End** (permanent, tonight) | The Hollow goes home; the Radiant's hunt is broken at the Crossing (canon: he still cannot be turned); the Wept spares Raunu (⟨They save Raunu⟩) | A specific method: the Fracture with two or more witnessed tells, **or** the Root trap, **or** one more owner-chosen method per Uninvited | **Yes**, by design |

The themes are drawn from each Fracture's printed "Truth" (`05:773-818`), not invented. Which
method each End uses, and whether the Radiant gets an End tier at all, are owner calls.

**Side effects of this structure:**
- **It simplifies.** One ladder replaces the Fracture DC table, the "nothing bought" rows and the
  Intimidation/Deception ban. That is about four fewer rule families than the 52 counted in
  USABILITY §5.1.
- **A1 drops from P0 to P1.** With tells as bonuses, a missed tell costs +2 instead of the whole
  climax. Tells still belong on the DM sheet.
- **A2 is resolved inside Slow:** spells need their roll.
- **A3 changes.** The Delay cap ("an Uninvited loses at most three turns per scene; spare Delay
  saves guests") now matches the direction rather than fighting it. Slow is meant to save people,
  not to change history: changing history is End's job. The adjacency loophole on *Clears the Way*
  is a separate exploit and still needs fixing.
- **A10 is absorbed.** Saving Raunu becomes an End outcome with a defined method and a procedure
  for the rounds after.
- **RULES P2-1 is resolved.** *Hideous Laughter* buys 1 Delay, instead of contradicting its
  table row.
- **RULES P2-4 still stands.** Social spells on the noncombatant NPCs need a ruling of their own.

### 7.3 Other findings that change under the direction

| Finding | Change |
|---|---|
| A4 (the Crossing cannot fail) | **Strengthened.** Real risk means a real margin at the river gate. Recommended: with no Delay and nobody at the gate, the Radiant gets his attack at the boat |
| A6 (three players) | Still needed. Recommended party is unchanged, but the reason Serane fits now depends on G1 being fixed |
| A7, L6 (Raunu and the Root; acting before midnight) | **Strengthened.** "Act early" should have several creative routes (hide Veier, the Root, warning the right person), each with a visible payoff |
| TUNING F2 (solo PCs) | Re-aimed: a solo line that is *dangerous but fair* (High for one), not a token fight |
| S14 tuning | Re-run the sims if option 4 (lethal while Focused) is chosen. Current win odds for a party playing the distraction game (90–96%) leave room for that |


---

## 8. Owner rulings, 2026-10-20

The owner ruled TP1–TP6:
- all seven risk options, under a DM dial;
- Slow / Stop / End approved;
- the Radiant gets a weakness through his emotion;
- the Attendant can kill;
- the Uninvited can kill, but rarely see anyone as a threat.

The mechanics are in `docs/DESIGN_oraga_5e_3p_pass.md`, and the decisions are logged in
`docs/DECISIONS.md` (TP1–TP6). Where §0–§7 disagree with those, the design document wins.
