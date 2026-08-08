# Fun & Ease-of-Play Review: Core Resolution Mechanics

**Scope:** `player_handbook/III.1_Core_Resolution.md`, `player_handbook/III.2_Adventuring.md`,
`player_handbook/II.2_Character_Creation_Attributes.md`, `player_handbook/II.6_Character_Creation_Skills.md`,
`player_handbook/Quick_Start.md` — evaluated against the project's own research yardstick,
`research/dice_system_analysis.md`.

**Lenses:** MDA (target aesthetics: Fellowship, Narrative, Fantasy, Discovery; Challenge light-touch),
fun (meaningful choice, pre-roll agency, three-tier drama), ease of play (cognitive load, handling
time, onboarding), and subtraction design.

**Date:** 2026-08-08

---

## 1. What Works — Mechanics That Deliver Fun and Ease

The core resolution layer is, on the whole, a faithful and often better-than-recommended
implementation of the research document. Credit where it is due, with citations:

**1.1 The 2d6 three-tier engine is exactly the research's Option A, and the book teaches it in one
sentence.** III.1's opener — "Ten or better and you get what you came for. Seven to nine and you get
it, and it costs you. Six or less and the world takes the next move instead of you" — is the
research's recommendation ("Bell curve... three tiers... two dice is the lowest cognitive load for
meaningful variance", `research/dice_system_analysis.md` §Recommendation) delivered in prose a new
player can repeat back after hearing it once. "This is the only resolution mechanic in the game...
Learn it once, use it everywhere" (III.1 §The 2d6 System) is the single biggest ease-of-play win in
the design.

**1.2 Sparks are Option D implemented verbatim, and the earning channels are a Fellowship machine.**
The spend ("Each Spark adds a d6... drop an equal number of lowest dice... always spent before you
roll", III.1 §Spending Sparks) matches the research's pre-roll-agency prescription exactly
(Ladouceur & Sévigny via §Psychology of Dice). Better: the earning design answers the research's
open question 2 ("the earning mechanism defines what behavior the game rewards") in the most
socially-loaded way possible. The **peer call** ("Any player may call out 'Spark?' for *another*
player's moment... The recognition comes from the table rather than from the chair") and the **act
break nomination** are direct mechanizations of Lazzaro's People Fun multiplier — the mechanic's
dynamic is players watching each other for award-worthy moments, and the aesthetic is Fellowship.
This is MDA working as intended.

**1.3 The Graceful Fail converts the worst roll into authorship.** "On any 6−, narrate how you make
the failure worse or richer for the story, and the MM confirms" (III.1 §Earning Sparks). The
research identifies the near-miss/failure moment as the dopamine-rich, socially-amplified beat
(§near-miss effect); this mechanic hands the player narrative control at exactly that moment and
pays them for it. Dynamic: failure becomes a performance opportunity rather than a sulk. Aesthetic:
Narrative + Fellowship. Few published games do this this cleanly.

**1.4 Modifier weight is deliberately small — the design dodges PbtA's known failure.** The research
table lists PbtA's key problem as "Stat modifier weight too large." Facets caps attributes at
−1/0/+1 (Table II.2–1) and combined attribute+skill at +4 (II.6 §Skill Ranks at a Glance). The dice
stay the star; competence shows without deleting variance. In practice a roll is **two chunks**: "my
number" (attribute+skill, pre-computed and memorizable per skill, as Quick Start demonstrates with
"2d6+2" lines on every pregen) plus the MM's difficulty. That is comfortably inside the ~4-chunk
working-memory budget the research cites (Sweller, §cognitive load).

**1.5 Difficulty declared before the roll, out loud, with a calibration table.** "The MM declares
difficulty before you roll" (III.1 §Difficulty), and Table III.1–5's benchmarks column "Who succeeds
most of the time" gives the MM real anchors ("A Practiced character, about two times in three").
This is the transparency lesson of Blades' Position/Effect without its overhead, and it directly
serves the research's market gap 5 ("GM-easy that actually is"). The Front Desk vignette models it:
"I'm calling that Hard, minus one. Saying it now so nobody's surprised later."

**1.6 "When Not to Roll" makes every roll a social event.** The three-condition gate and the
explicit statement "Facets has fewer rolls per session than most TTRPGs, on purpose" (III.1 MM Note)
implement the research's social-memory logic: high-stakes public resolution is what generates
flashbulb memories. Fewer, heavier rolls is the right call and the book says why.

**1.7 Threat Clocks are one hazard subsystem instead of many, and the no-roll wind-back is a
quietly excellent piece of subtraction design.** "Winding it back costs a character an action,
nothing more. There is no roll" — and the book prints its own reasoning ("a 7–9 on that very roll
would advance the clock you are trying to wind back — a rules-lawyer loop", III.2 §Hazards). No new
dice mechanic, visible to the whole table (shared tension = Fellowship), and a nice emergent
dynamic: skilled characters (10+ never advances the clock) genuinely slow hazards down, so
competence is visible in pacing itself.

**1.8 The death rules are the adventure register, mechanized.** "Broken never kills you...
the choice is the player's and no one else's" (III.2 §When a Character Would Die). Permanent scar
vs. heroic death with an auto-succeeding final action makes death "a story beat instead of an
accident." This is wonder-and-heroism design with zero grimdark accident risk, and The Beam vignette
shows the table-quiet moment it produces. Aesthetic: Narrative and Fantasy, fully delivered.

**1.9 Player-facing rolls, with the costs documented.** "NPCs do not roll dice" (III.1 §Contested
Rolls) halves combat handling time and keeps the MM's eyes on the players. The research addendum
(§Player-Facing Rolls) did the homework — precedent, honest costs, playtest flags — and the
recommendation to keep it is sound.

**1.10 The standing rulings pre-empt the two classic table arguments.** "Trying Again" ("What's
different this time?" — the whole ruling in one question) and "Acting on Unnarrated Details" (ask
freely, MM leans yes, new facts enter through the MM) are friction-killers written specifically so
the MM "does not have to invent a ruling mid-scene" (III.1 §Standing Rulings). Both protect the
Narrative aesthetic (failure stays meaningful; the shared scene stays shared).

**1.11 Group rolls default to speed.** "When in doubt, group roll — it is faster and produces a
cleaner narrative beat" (III.1 MM Note) — the tie-break criterion is table pace. Correct priorities.

---

## 2. Findings

Severity: **High** = actively hurts fun or adds friction at the table; **Medium** = real but
containable; **Low** = polish.

---

### F1 — HIGH: Quick Start breaks its own ten-minute promise at combat and saving throws

**Mechanic:** `Quick_Start.md` promises "Sit down and play in ten minutes" and delivers on it for
skill checks — then Table QS–4 and the closing reference blocks cite rules the document never
defines, and omit numbers it tells you to roll.

Specifics:
- QS–4: "Resist an effect | 2d6 + Major Attribute (Body/Mind/Soul)" — but **no pregen sheet lists
  Major Attribute values**. Tables QS–1/2/3 list only the nine Minors. A new player told to roll
  Body has no number to roll and no derivation table in the document (it lives in II.2, Table
  II.2–2). For the record: Zahna's Mind is +0, not the +1 a new player would guess for "The Scholar."
- "**Combat Postures:** Aggressive (+1 offense, first reaction of the exchange costs extra)..." —
  *exchange*, *reaction*, *offense* are all undefined in the Quick Start, with no pointer to III.3.
- "**Conditions:** Tier 1 (Winded/Off-Balance/Shaken) clear end of exchange..." — same problem.
- "Cast a spell | 2d6 + Spirit or Knowledge (by tradition)" — a fork the new player cannot resolve;
  the document never says which tradition uses which.
- Pregen sheets carry advancement metadata a first-session player cannot use and may puzzle over:
  "Endurance (Novice, 1 mark)", "Minor scope only until Facet Technique unlocked", "the domain
  origin takes the place of a secondary skill."

**Table dynamic:** the first ten minutes are genuinely great (see §4), and then the first fight or
the first save stops play for a book lookup the Quick Start doesn't even cite. That is the exact
moment a brand-new table is most fragile.

**Recommendation:** (a) Add a Body/Mind/Soul modifier line to each pregen block — three numbers,
one line. (b) Either add a five-line combat primer (what an exchange is, what a reaction is, one
sentence each) or cut the Postures/Conditions lines from QS–4 and replace with "Combat: see Chapter
III.3 — the same 2d6 roll." (c) Resolve the spell line per pregen ("Zahna casts with Knowledge").
(d) Strip "(1 mark)" and secondary-skill annotations from Quick Start sheets; they belong on the
full sheet.

---

### F2 — MEDIUM: The Spark economy is ambiguous at session start and all earning is discretionary — the known hoarding problem has no structural counterweight

**Mechanic:** "Each character begins each session with **3 Sparks**" (III.1 §Sparks). It is not
stated whether unspent Sparks carry over (reset to 3? floor of 3? +3?). All four earning channels
(MM award, peer call, nomination, Graceful Fail) require someone to actively confirm; none is
guaranteed during play.

**Table dynamic:** the research warned "too scarce and players hoard rather than engage"
(§Option D, Risk), and the 2026-03-13 playtest observed exactly that (Spark hoarding,
`playtest/01_thornwall_undercroft/`). If Sparks bank across sessions, hoarding is strictly
rewarded; if they reset, the rule as written doesn't say so, so tables will argue it. A player
sitting on 3 Sparks all night is a player the pre-roll-agency layer isn't reaching.

**Recommendation:** One sentence resolves the ambiguity — recommend explicit **reset to 3** ("Sparks
do not carry over; you start every session at 3"), which is also the anti-hoarding lever: unspent
Sparks are wasted Sparks. Additionally, the research's own digital-integration list already
prescribes "Spark tracking and award prompting" — make the app nudge the MM when a player hasn't
earned or spent in a while. No new mechanic needed.

---

### F3 — MEDIUM: The Technique difficulty-step paragraph is the densest text in the core chapter, placed before a new reader knows what a Technique is

**Mechanic:** III.1 §Difficulty, the paragraph beginning "A Technique can then move that declared
difficulty one step further in your favor..." — ~110 words covering the one-step cap, a two-way
trigger taxonomy ("a step whose trigger is something the roll already carries... applies on its own
and the roll result names it; a step whose trigger is a judgment call... you declare yourself"), and
a fixed ordering rule, in a single paragraph of the chapter every new player reads first.

**Table dynamic:** the cap itself is good anti-stacking design (credit). But the auto-apply vs.
self-declare taxonomy invites mid-scene classification debates ("is my hunch 'something the roll
already carries'?") and front-loads Facet-chapter complexity into the one chapter that should stay
at "roll 2d6, add your number."

**Recommendation:** Keep one sentence in III.1: "A Technique may shift the declared difficulty one
step in your favor — at most one step per roll, and the ladder's ends hold." Move the trigger
taxonomy and ordering detail to the Facet chapters (II.4x) where Techniques are defined, and let the
digital tool auto-apply carried triggers (it knows the character's Techniques and the roll's tags).

---

### F4 — MEDIUM: Specialty and the Technique step both relabel difficulty, and nothing says whether they stack

**Mechanic:** III.1 caps Technique steps at one ("At most one such step ever applies to a single
roll, no matter how many Techniques you hold") — but a **Specialty** ("Standard becomes Easy when
directly applicable", every Quick Start pregen; defined in II.5) is not a Technique. As written, a
Hard roll could arguably go Hard → Standard (Technique step) → Easy (Specialty), a two-step swing
the one-step cap was built to prevent.

**Table dynamic:** exactly the modifier-negotiation the small difficulty ladder exists to avoid; the
player who reads carefully gets a better ladder than the player who doesn't.

**Recommendation:** One unified rule in III.1 §Difficulty: the declared difficulty can shift **at
most one step total** from all character abilities (Techniques, Specialties, anything future),
whichever single source the player picks. This future-proofs the cap as Facet content grows.

---

### F5 — MEDIUM: A group roll near a Threat Clock can advance the clock multiple segments in one narrated beat

**Mechanic:** The clock "advances one segment whenever **a character** rolls a partial success (7–9)
or a failure (6−) on a roll made near the hazard" (III.2 §Hazards). A group roll (III.1 §Group
Rolls) has every participant roll. At the stated ~72% partial-or-fail rate, a four-player group roll
near a hazard expects ~3 advances — most of a 4-segment clock filled by a single "we all sneak past
the fire" beat, even if the group *succeeds* by majority.

**Table dynamic:** the party wins the group check and loses the scene, which reads as unfair and
undermines the majority-success rule's promise. The Mill vignette only ever shows individual rolls,
so the book never models the interaction.

**Recommendation:** One sentence in III.2: "A group roll advances a Threat Clock at most once,
keyed to the group's overall result." Preserves both mechanics unchanged.

---

### F6 — MEDIUM: "Endurance" names two different numbers on the same character sheet

**Mechanic:** Endurance the **skill** (II.6: "Pushing through physical hardship... 2d6 +
Constitution + your Endurance rank") and Endurance the **combat pool** (Quick Start pregens:
"Endurance: 5 (base 4, Constitution +1)"). Mordai's Quick Start block carries both: "Skills: ...
Endurance (Novice, 1 mark)" and "Endurance: 5" four lines apart.

**Table dynamic:** a new player asked to "spend 1 Endurance to Press" or "roll Endurance to push
through" must disambiguate a term the sheet uses twice with different types (a spendable pool vs. a
rolled rank). This is a permanent low-grade tax on exactly the players the game is written for.

**Recommendation:** Rename the pool (it is a spendable combat resource — a name like the existing
condition vocabulary's register, distinct from any skill) or, at minimum, always print it as
"Endurance Pool" everywhere the pool is meant. A rename touches III.3, facet.yaml, the engine, and
the quick refs per the sync rule — flagging cost honestly — but the collision compounds with every
new player onboarded.

---

### F7 — LOW: The 7–9 guidance implies a post-roll decision point the rules never define

**Mechanic:** "The MM must name the cost *before* the player decides how to proceed" (III.1
§Partial Success). Proceed with what? The roll has already happened. This wording gestures at a
PbtA-style "take it at this cost, or back off" choice, but no rule grants the player the option to
decline a partial success.

**Table dynamic:** some tables will play 7–9 as an offer (adds a nice choice), others as a
narration order (cost simply happens). Both are fine games; the book should pick one, because the
"offer" reading is a meaningfully different — and arguably more fun — mechanic.

**Recommendation:** Either state it as narration sequencing ("name the cost before narrating the
success") or embrace the offer explicitly ("on a 7–9 the MM names the cost; the player may take the
success at that cost, or withdraw the attempt with nothing gained"). The second option adds genuine
meaningful choice for free; the first is simpler. Choose deliberately.

---

### F8 — LOW: Attribute purchase power is uneven — Charisma buys three skills, Luck buys one

**Mechanic:** II.6 Table II.6–1 fixed pairings mean Charisma governs Persuade, Deceive, and Perform;
Dexterity two skills plus combat reactions; Luck governs only Gamble; Spirit only Attune (plus
magic, for casters). Attribute points cost the same everywhere (II.2, 18-point buy).

**Table dynamic:** a soft dominant pattern — non-casters dump Spirit, non-gamblers dump Luck, and
the "every strength is bought with a weakness" promise (II.2) bites unevenly: dumping Charisma
costs three skills, dumping Luck costs almost nothing rollable. Saving throws via the derived Major
(Soul) are the only systemic brake, and at −1 it is a light one.

**Recommendation:** No redesign needed — but the MM-facing text should note that Luck and Spirit
earn their points through MM-invoked rolls ("surviving against the odds," sensing the supernatural)
and encourage the MM to actually call for them. Alternatively, watch in playtest whether
Luck-1/Spirit-1 becomes the universal build; if it does, that is the signal to widen those
attributes' roll surface, not to add rules now.

---

### F9 — LOW: Fixed skill–attribute pairs vs. the Strike's flexible pairing is a consistency seam

**Mechanic:** II.6 hardcodes every skill to one attribute ("**Roll:** 2d6 + Strength + your
Athletics rank"), while QS–4 says "Hit something | 2d6 + weapon attribute + Combat or Finesse —
whichever fits how you're striking" (and the engine accepts any attribute/skill for Strikes).

**Table dynamic:** fixed pairs are an *ease win* — no per-roll negotiation about "can I Persuade
with Wisdom?" — so this is the right default. But combat visibly breaking the pattern teaches
players the pairing is negotiable, which reopens the negotiation everywhere else.

**Recommendation:** State the principle once in II.6 §Using Skills: pairs are fixed except where a
rule explicitly says otherwise (the Strike being the named exception). One sentence closes the seam.

---

### F10 — LOW: The Graceful Fail can ritualize into a per-6− negotiation

**Mechanic:** "This one is yours to claim. On any 6−, narrate how you make the failure worse or
richer... Not every failure earns a Spark" (III.1 §Earning Sparks).

**Table dynamic:** the mechanic is excellent (see §1.3), but "yours to claim... on any 6−" plus a
soft MM gate means an incentive to attempt the claim on *every* 6−, turning failures into small
adjudication moments — friction at the exact beat the mechanic is meant to speed up. The MM confirm
is the control, but the book gives the MM no calibration for saying no.

**Recommendation:** One line of MM guidance: what a confirm-worthy Graceful Fail looks like versus a
restatement of the failure (the II.2 vignette's "you cannot tell which" award is a good model —
consider cross-referencing it). Do not add a hard cap; the social gate just needs one sentence of
backbone.

---

### F11 — LOW: Rating labels (1/2/3) and modifiers (−1/0/+1) are a dual encoding

**Mechanic:** II.2 Table II.2–1 maps rating 1/2/3 to modifier −1/0/+1; sheets and vignettes carry
both ("Charisma 2, no rank, so a flat +0").

**Table dynamic:** every roll passes through a translation step for new players. The mitigations are
already good — Quick Start prints both columns and pre-computes "2d6+2" lines, and the digital sheet
absorbs it entirely — so this is polish only. The 1–3 scale earns its keep in the point-buy and the
Major derivation sums, so cutting it is not free.

**Recommendation:** Keep, but ensure every printed sheet and app view leads with the modifier
(the number you actually roll) and treats the rating as chargen bookkeeping.

---

### F12 — LOW: The clock wind-back creates a "designated janitor" who never rolls

**Mechanic:** Wind-back "costs a character an action, nothing more. There is no roll" (III.2).

**Table dynamic:** mathematically sound (one winder cannot hold a clock alone against two rollers:
expected +1.44 vs −1 per cycle, so the hazard still closes — good). But the winding player opts out
of dice drama entirely, and the optimal party assigns the job to whoever has the worst modifiers —
the exact player the spotlight rules should be protecting. Zulnut's vignette line ("The best kind of
action. The kind that can't fail") plays it as characterful, which it is — once.

**Recommendation:** No rules change. Add an MM sidebar note: rotate who winds, and narrate the
wind-back as vividly as any roll. Watch in playtest whether the janitor role concentrates.

---

## 3. Modifier-Stacking Audit — One Roll

Everything that can legally touch a single 2d6 roll, worst case (a combat Strike by a maxed
character; bracketed items are combat-only):

| # | Source | Range | Type |
|---|---|---|---|
| 1 | Minor Attribute (II.2) | −1 to +1 | flat |
| 2 | Skill rank (II.6) | +0 to +3 | flat |
| 3 | MM difficulty (III.1) | +1 to −2 | flat |
| 4 | Technique step (III.1) | relabels #3 one step, max one | relabel |
| 5 | Specialty (II.5/QS) | Standard→Easy; stacking with #4 unstated (F4) | relabel |
| 6 | Sparks (III.1) | +Nd6 drop N lowest; N uncapped by rule, capped by stock | dice |
| 7 | [Posture, III.3] | +1 / −1 offense | flat |
| 8 | [Press, III.3] | +1d6 drop lowest, 1 Endurance | dice |

**Counts:** a non-combat roll has **3 flat sources** (max +5) plus up to 2 difficulty relabels and
Spark dice. A combat Strike has **4 flat sources** (max +6) plus relabels, Sparks, and Press — the
extreme legal case is **7d6 drop 5, +6** (3 Sparks + Press + all flats). 

**Verdict:** the flat layer is healthy — it collapses to "my number + difficulty," two chunks,
because attribute+skill is stable per skill and pre-computable (Quick Start already does this).
This meets the research's cognitive-load bar cleanly and deserves credit. The two watch areas are
the **relabel layer** (F3, F4 — that's where the ambiguity and the negotiation live, not in the
numbers) and the **dice-adder layer**, which is uncapped in text but self-limiting through the
Spark/Endurance economies and fully absorbed by the digital roller. No change to the caps is needed
if F4's unified one-step rule lands.

---

## 4. Onboarding Walkthrough Verdict — Quick Start, Simulated

Simulating a brand-new player handed `Quick_Start.md` cold:

- **Minute 0–1:** "The One Rule" — one roll, three bands, memorable phrasing. Passes instantly.
- **Minute 1–5:** Pick a pregen. Personalities are one line each and evocative. The worked roll
  line on every sheet ("*When Zulnut picks a lock: 2d6 +1 (Dexterity) +1 (Finesse skill) =
  2d6+2*") is the single best onboarding device in the document — it converts the whole modifier
  system into one memorized number. **Friction:** "Guild Apprentice (magical — the domain origin
  takes the place of a secondary skill)", "(Novice, 1 mark)", "Minor scope only until Facet
  Technique unlocked" — three phrases that answer questions no first-session player has asked (F1d).
- **Minute 5–9:** The Sealed Door example scene. Excellent — it demonstrates all three outcome
  tiers, difficulty declared aloud, a Spark award via peer call, and pre-technique magic in play,
  in under a page. A player who reads it knows how the game *sounds*, which is the hard part.
- **Minute 9–10:** QS–4 Quick Reference. Skill lines fine. Then: "Cast a spell: Spirit or Knowledge
  (by tradition)" — unresolvable here; "Resist an effect: 2d6 + Major Attribute" — **the number is
  not on the sheet**; Postures and Conditions — five undefined terms (exchange, reaction, offense,
  Staggered's "treated", Broken) with no pointer to where they are defined (F1).

**Verdict: a genuine pass for exploration/social play — a table really can be rolling meaningful
dice inside ten minutes, which very few systems achieve — with three specific holes (saves, combat
vocabulary, the spell fork) that all open at predictable moments and are all fixable inside
Quick_Start.md without touching any rule.** The fixes in F1 would take this from "great until the
first fight" to honestly complete.

---

## 5. Cut Candidates

Ranked by confidence that cutting (or relocating) loses no fun:

1. **The Technique trigger taxonomy in III.1** (F3) — relocate to the Facet chapters. III.1 keeps
   one sentence. No fun lost; the core chapter gets lighter for every reader.
2. **Advancement metadata on Quick Start pregens** (F1d) — "(1 mark)", scope caveats,
   secondary-skill notes. Pure noise at minute 3 of a player's first session.
3. **Postures/Conditions lines in QS–4** — cut from Quick Start (not from the game) unless a
   combat primer is added; a reference to undefined terms is worse than a pointer to III.3.
4. **The "lead roller alternative" paragraph in III.1 §Group Rolls** — it forward-references
   Support (III.3) inside the core chapter. Could compress to one sentence + pointer. Marginal.
5. **Duplicated outcome/difficulty tables in II.2** (Tables II.2–3, II.2–4 restate III.1's tables) —
   defensible as teaching-order duplication, but it is two more tables to keep in sync forever;
   the "quick references are compressions" rule makes them a standing maintenance liability.
   Consider whether II.2 needs the tables or just the one-sentence version plus a pointer.
6. **Perform as a separate skill** (II.6) — three Charisma skills where Persuade and Perform share
   "moving people"; Perform is the narrowest roll surface in the list and a mild trap pick for a
   new player (it does less than its neighbors for the same cost). *Weak* candidate: merging is a
   real rules change touching Backgrounds and facet.yaml, and bard-fantasy players will look for
   it. Flag for playtest data (does Perform ever get rolled?) rather than cutting now.

**Explicitly not cut candidates, despite complexity:** Major Attributes (the derivation table is
bookkeeping, but the proactive/reactive save distinction is clean, the MM Note rule is one
sentence, and the digital sheet computes the sums); the four Spark earning channels (each produces
a different Fellowship dynamic — chair, peer, ritual, self — and that variety is the point); Threat
Clocks (already minimal); the 1–3 rating scale (load-bearing for point-buy).

**Dominant strategies and traps found:** no hard dominant option exists in the core layer — the
one-step difficulty cap, the small flats, and the Spark economy each close a stacking door
(credit). The soft patterns to watch are Luck/Spirit as dump stats (F8), the clock janitor (F12),
and reflexive Graceful Fail claims (F10). No true trap options at chargen; the transparency of the
three-point scale protects new players.

---

## Summary

The core resolution layer implements its own research document with unusual fidelity — 2d6
three-tier (Option A), Sparks exactly as Option D specified, never-a-dead-end failure, player-facing
rolls with the costs documented, small modifier weight that dodges PbtA's known stat-weight problem,
and a roll-rarely philosophy that treats each roll as a social event. The Graceful Fail, peer Spark
call, and player-authored death rules are better than anything the research asked for. The problems
are concentrated at the edges, not the center: the Quick Start reneges on its ten-minute promise
precisely at combat and saving throws (F1, the one High), the Spark economy has a session-boundary
ambiguity feeding a playtest-confirmed hoarding problem (F2), and the difficulty-relabel layer
(Technique step, Specialty) is where all the remaining ambiguity and table-negotiation risk lives
(F3, F4). Every Medium finding is fixable in one or two sentences of rules text; none requires
redesign.
