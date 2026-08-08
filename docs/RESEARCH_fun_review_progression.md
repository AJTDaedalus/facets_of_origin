# RESEARCH — Fun & Ease-of-Play Review: Magic, Character Creation, Advancement, Equipment

*Review date: 2026-08-08. Scope: II.1, II.3, II.4/a/b/c, II.5, IV.1, Appendix_Magic_Domains,
research/magic_system_analysis.md, research/advancement_priority_questions.md,
docs/BRIEF_technique_difficulty.md, docs/DESIGN_technique_difficulty.md, with III.1 and II.2
consulted for the resolution and point-buy baselines. Evaluated against exactly two qualities:
fun and ease of play, per the project philosophy. Lenses: MDA (target aesthetics Fantasy,
Expression, Narrative, Fellowship), fun of creation/advancement, cognitive load, subtraction design.*

---

## 1. What Works

These are load-bearing successes, not politeness. Most of the review's findings are joints
between systems; the systems themselves are largely doing what the research told them to do.

**The no-spell-list bet lands.** Domain + Intent + Scope delivers the Expression and Fantasy
aesthetics it was designed for. "The question is never 'do I have this spell?' It is 'what do I
want my fire to do, and how ambitious am I feeling?'" (II.3, *What Is Magic?*) is the correct
mechanic→dynamic→aesthetic chain: the mechanic (domain licenses, dice price ambition) produces
the dynamic (players author intents, the table leans in) that produces wonder. The Appendix's
framing of example intents as "design patterns, not a menu" (Appendix_Magic_Domains, *Reading
the Entries*) actively defends the bet against the failure mode where examples calcify into a
spell list.

**MM burden — the research's number-one freeform failure — is genuinely mitigated.** The
magic_system_analysis identified live adjudication as the thing that kills freeform magic. The
shipped design answers it three ways: domain scope is "a one-time conversation at character
creation, not a recurring negotiation mid-session" (II.3, *Domain*); scope declaration happens
*before* the roll; and the "6− templates" MM Note (II.3, *Outcome Tiers for Magic*) hands the MM
six ready failure patterns. That box is quiet excellence — it converts the scariest MM moment
(improvising a magical failure) into a menu, exactly where a menu belongs.

**Pre-Technique magic capped by scope, not difficulty, is playtest-earned wisdom.** The
"Through the Mirror" box (II.3, *Acquiring a Domain*) records the lesson: punishing the roll
"taught them that their character's defining trait was a liability." Capping scope instead keeps
starting casters *succeeding* at small magic from session one. This is the single best
fun-preserving decision in the magic chapter — and it becomes the yardstick two findings below
measure other rules against.

**The Normal: field on every Technique is a teaching mechanism disguised as formatting.**
Restating "the baseline rule this Technique departs from" (II.4, *Reading the Entries*) means a
Technique is never a mystery modifier — the player sees exactly what they now get to break.
Combined with the Q1 composition doctrine (BRIEF_technique_difficulty: MM's label first, at most
one character-side step, ladder clamps), the game has permanently capped its own modifier math
at "one step from the MM, one step from you." On a 2d6 engine that discipline is worth more than
any individual Technique.

**Mind and Soul Techniques are permissions, not arithmetic.** Sharp Analysis buys an honest
answer; Convenient Coincidence lets a player author a fact; The Turning ends a standoff by
speaking (II.4b, II.4c). These are Narrative and Fellowship mechanics — they generate table
moments ("The MM may comment on this. The other players may comment on this. This is
appropriate," II.4c, *The Odds Were Never Real*) rather than sheet updates. This is what
"exciting unlocks, not fiddly modifiers" looks like when it's achieved.

**Equipment is the best subtraction-design chapter in the book.** Weapons collapse to an
attribute picker (Table IV.1–1), armor is a handful of per-scene decisions instead of per-blow
arithmetic (the "Through the Mirror" box in IV.1 defends this correctly), gear is narrative with
a charming Luck-roll fallback ("Do You Have It?"), and currency is explicitly deferred. Almost
nothing here is dead weight. The chapter even says why it's short.

**Character creation is fast and largely MM-free.** No Technique choice at creation, no
equipment shopping, no spell selection — a new player picks 9 numbers under one constraint,
a Facet, and a Background, and the Background auto-fills the skill section (II.1, II.5).
Realistic time-to-first-play is 20–30 minutes. The five-element Background format is tight, and
the Secondary Skill's 1-mark head start is a small mechanical hook that makes history pay out in
the advancement system from day one (II.5, *Secondary Skill*).

**The difficulty benchmarks table** (III.1, Table III.1–5) pairing each tier with "who succeeds
most of the time" is exemplary calibration prose — it lets a new MM price a magical scope call
by feel instead of by table.

**Reflection scenes are encouragement, not a gate.** "Advancement happens whether or not the
scene takes place" (II.4, *Advancement and Reflection*) avoids the trap of taxing advancement
with mandatory ceremony while still offering the Fellowship payoff.

---

## 2. Findings

Severity: **High** = actively hurts fun or adds friction at the table; **Medium** = real cost,
survivable; **Low** = polish.

---

### F1. HIGH — The "Pushing scope" Spark rule cannot be executed as written

**Mechanic.** II.3, *Sparks and Magic*: "By spending a Spark, a character may attempt an effect
one scope tier beyond their domain's natural ceiling. A Standard domain character whose Major
effects are normally Very Hard may spend a Spark to push to a scope that would otherwise be
unavailable... at Very Hard difficulty."

**The problem.** Post-Technique, no domain type has a scope ceiling — Table II.3–2 prices Minor,
Significant, *and* Major for all three types. There is no scope tier beyond Major, so "one scope
tier beyond their domain's natural ceiling" has no referent. The section then compounds the
confusion by mixing ladders: "Broad (Prismatic) domains cannot be pushed beyond Very Hard" is a
*difficulty* statement guarding what was framed as a *scope* mechanic, while "Easing Major
effects" is a difficulty mechanic sitting in the same list. A table reading this section cannot
determine what the first Spark use actually buys.

**Dynamic.** The player's most exciting moment — "I want to attempt the impossible thing" —
lands on the least coherent paragraph in the magic chapter. The MM improvises, tables diverge,
and the digital layer cannot implement it.

**Recommendation.** Rewrite the section around the two ladders explicitly. The settled decisions
(memory/DECISIONS: Sparks as optional scope fuel; Focused can ease Major one step) survive, but
the four current bullets should become at most two: one scope rule (pre-Technique: a Spark buys
one Significant-scope attempt) and one difficulty rule (Focused only: a Spark eases a Major
working one step; Broad's ceiling never moves). If "beyond Major" epic workings are intended,
they need a named tier or explicit MM-ritual framing; if not, delete the sentence.

---

### F2. HIGH — Whether a casting roll takes a skill modifier is unstated, and the answer decides whether mages ever grow

**Mechanic.** II.3, *Rolling Magic* specifies only the attribute: "The attribute you roll
depends on your magical tradition." Both worked examples roll bare attribute: "Zahna rolls
2d6 + Knowledge (3 → +1) at Standard difficulty" (II.3, *A Mage, a Beam, a Problem*). Meanwhile
III.1 says "You always roll with an attribute; you add a skill when your training directly
applies" — and Attune is defined as the Spirit-casting-adjacent skill (II.4c).

**The problem.** If casting is attribute-only (as every printed example shows), a caster's roll
modifier is capped at +1 *forever*. A session-1 acolyte and a 20-session archmage roll the same
dice at the same difficulty for the same working. The project's own research names this exact
failure: "magic-users don't feel like they've *grown* as magical practitioners"
(magic_system_analysis, Approach 5, "What fails"). The Technique tree grants breadth (full
scope, Second Domain, Ascendant) but never reliability — while a fighter's Combat climbs from
+0 to +4 (attribute + Master rank, II.4 Table II.4–1). It also makes the Hard/Very Hard rungs of
the domain tables brutally flat: Very Hard at net −1 is a 41.7% chance of even a partial, and no
amount of advancement improves it (only Sparks do).

**Dynamic.** Either mages plateau mechanically at creation (a growth-curve hole for the game's
flagship fantasy), or every table quietly house-rules Attune/Lore onto casting rolls and the
tables diverge from the book and the engine.

**Recommendation.** Decide and print it in II.3 *Rolling Magic*, one sentence, and sync
facet.yaml/engine in the same cycle per the sync iron law. Either answer is defensible; the
skill-applies answer gives casters the same +0→+4 arc as everyone else and softens F3 without
touching the domain tables.

---

### F3. HIGH — The Broad table re-imports the exact feel-bad the pre-Technique playtest removed

**Mechanic.** Table II.3–2: Broad (Prismatic) = Hard / Very Hard / Very Hard, "Broad domains
cannot be pushed beyond Very Hard under any circumstances, including Sparks" (II.3). Prismatic
territory is gated behind Ascendant Domain, a Tier 3 Technique — the most expensive unlock in
the game (II.4b/II.4c).

**The problem.** The game's own doctrine (II.3, *Through the Mirror*) says punishing the roll
"meant new casters failed publicly and often, which taught them that their character's defining
trait was a liability." Ascendant Domain does this to *veterans*: with attribute-only casting
(F2), a prismatic cantrip at Hard fails or complicates ~58% of the time unsparked; Significant
and Major workings full-succeed on ~8% of rolls. The player who paid Tier 3 for magical
transcendence experiences it mostly as 6−s and partials. The ceiling-that-Sparks-cannot-move is
a rule whose main output is disappointment at the table's most dramatic beat, protecting against
an abuse (routine world-scale magic) that the Very Hard label, the MM's scope call, and once-a-
scene fiction already police.

**Dynamic.** Wonder is the target aesthetic; the mechanic delivers frustration precisely at the
top of the fantasy ladder. It also makes the Ascendant choice worse than its sibling (see §5).

**Recommendation.** Keep the identity ("the grandest effects are desperate rolls") but move one
number: Broad at Hard/Hard/Very Hard, or let dice-Sparks remain fully effective and drop only
the "ceiling" sentence (dice-Sparks *are* currently legal on Broad rolls — if so, say it in the
same breath as the ceiling rule, because the current wording reads as "Sparks don't work here"
to a fast reader). Resolving F2 in favor of skills-apply also substantially rehabilitates this
table without touching it.

---

### F4. MEDIUM — A mage's first Technique choice is a forced pick

**Mechanic.** A magical Background grants Minor-scope magic; full scope requires the Facet's
magic-granting Tier 1 Technique — Arcane Study or Spiritual Domain (II.3, *Acquiring a Domain*;
II.5, *Magic and Backgrounds*). Facet level 1 grants exactly one Technique (II.4, *Techniques*).

**The problem.** For a caster, the first advancement milestone (~4–6 sessions in, see §4) offers
no real choice: taking anything other than the magic activator postpones the character's defining
capability to Facet level 2, roughly nine sessions in. Non-casters get a genuine 6-way pick at
level 1; casters get a checkbox. Expression — "character build as self-expression" — is exactly
the aesthetic this spends.

**Dynamic.** Every caster's build is identical through level 1, and the "meaningful mechanical
milestone... the moment of formalization" (II.5) is meaningful but not a decision.

**Recommendation.** Either own it in the prose ("your first Technique is your formalization —
your first *choice* comes at level 2"), so expectations are set honestly, or decouple the scope
unlock from the Technique slot (e.g., the magic-granting Technique also carries a Choose: field
with a real option inside it). The first is a one-sentence fix; the second is a design change to
weigh against schedule.

---

### F5. MEDIUM — "Only skills you used" collides with "master all five skills," and unspent points evaporate

**Mechanic.** "You may only advance skills you used this session. You may not save points
between sessions — unspent points are lost" (II.4, *Advancing Skills*). Facet level 3 — the
gateway to the first Major Advancement — requires all 15 rank advances, i.e. Master rank in
*every* skill of the Facet (II.4, *Facet Levels*).

**The problem.** Late-Facet progression legally requires marks in your least-used skills, but
marks can only go to skills you used. The optimum play is to shoehorn a Gamble or Deceive roll
into every session for bookkeeping reasons — activity generated by the advancement economy, not
the fiction. Meanwhile the book's own example shows the feel-bad of the forfeit rule: "He has 2
points left; he didn't use another skill this session, so they go unspent, and unspent points
are lost" (II.4, example). Punishing a focused session with lost progression is friction with no
compensating fun; the abuse it prevents (banking a large point pool) barely exists at 4 points a
session.

**Dynamic.** Players either grind unfitting rolls or watch points burn; the MM fields "can I
quickly gamble with the innkeeper before we end?" requests they can see straight through.

**Recommendation.** Let a character bank up to 2 unspent points across sessions, or allow 1 of
the 4 points to go to an unused Primary-Facet skill ("training between sessions"). Either
preserves the used-skills principle where it matters and deletes both the forfeiture sting and
the shoehorn incentive.

---

### F6. MEDIUM — Whether the Background's starting Practiced counts toward Facet level 1 is settled only by example

**Mechanic.** "Your Facet level... advances every time you accumulate 5 skill rank advances
within it" (II.4, *Facet Levels*). "The Background starting skill counts as 1 advance at
character creation" (II.4, *Career Advances*). The Zulnut example counts five in-play advances
for level 1, with a parenthetical implying the creation rank is excluded ("Finesse started
Practiced at creation, so this is its first advance").

**The problem.** One counter (career advances) includes the creation rank; the other (Facet
level) excludes it — but the exclusion is never stated as a rule, only implied by an example.
A player who reads the career benchmark "3–5: first Facet level (5 advances) within reach"
(Table II.4–3) beside career_advances starting at 1 can honestly conclude they need only 4 more.
That is a session's worth of difference on the game's first milestone.

**Recommendation.** One sentence in *Facet Levels*: "Ranks granted at character creation count
toward career advances but not toward Facet levels" (or the reverse, if that's the intent —
the example says this one). Sync facet.yaml/engine counting in the same commit.

---

### F7. MEDIUM — Second Domain's permanent penalty makes the standard-domain pick price identically to a prismatic territory

**Mechanic.** Second Domain (Tier 3): a second standard domain "one difficulty step harder than
normal for that domain" (II.4b/II.4c, as re-anchored by BRIEF/DESIGN_technique_difficulty Q2).

**The problem.** A Standard second domain at +1 step prices Hard/Very Hard/Very Hard — label-
for-label the Broad table (Table II.3–2), for a far narrower territory (its ceiling is at least
Spark-movable, which is the one distinction). A Focused second domain prices Standard/Hard/Very
Hard — a full tier better. So inside one Technique, one Choose: option is plainly stronger, and
the penalty never lifts: the second domain never matures, a permanent difficulty tax on a
defining trait — the shape of rule the pre-Technique playtest already identified as fun-hostile
(II.3, *Through the Mirror*). The Q2 ruling made the pricing *coherent* (correctly); it did not
ask whether the price is fun.

**Recommendation.** Consider letting the penalty expire — e.g., the step lifts at the next
Facet level or Major Advancement, making Second Domain an arc instead of a tax. If it stays
permanent, add one sentence of guidance at the Choose: field noting Focused picks suffer it
least, so the trap is at least labeled.

---

### F8. MEDIUM — Never Surprised passively deletes a scene genre from Tier 1

**Mechanic.** "If the MM would call for a roll to notice an ambush, trap, or sudden threat
before it lands, you automatically succeed" (II.4b, Instinct Tier 1). Passive, always on.

**The problem.** One character's Tier 1 pick permanently removes ambush reveals and trap
springs from the campaign — not eases them, removes the roll. Unlike its Tier 3 sibling First
Move (once per session), it has no frequency governor. The other Tier 1 Instinct option (The
Wrong Note) is calibrated far more carefully ("something feels off — even if they do not tell
you what"). This is less a balance problem than an MM-fun problem: a whole species of scene
opener is off the table for the price of the game's cheapest unlock.

**Recommendation.** Downshift the guarantee to The Wrong Note's shape ("you always get a
warning beat; what you do with it is yours") or move the absolute version up a tier. The
fantasy ("never the most surprised person in the room") survives fully at warning-beat strength.

---

### F9. MEDIUM — The magical-Spark rules are the one overloaded joint in an otherwise light casting chain

**Mechanic.** II.3, *Sparks and Magic* defines four distinct magical Spark interactions with
different eligibility: (a) add-a-die (universal), (b) push scope (see F1), (c) buy one
Significant attempt pre-Technique, (d) ease Major one step, Focused only — plus the Broad
no-ceiling-movement exception.

**The problem.** The core casting loop is three decisions (see §3) — then the Spark question
arrives carrying four sub-rules keyed to domain type and Technique status. This is where the
chapter's cognitive load concentrates, and it is exactly the kind of conditional stack the rest
of the system refuses to build (compare the Q1 guardrail: "at most one character-side step,
whatever its source").

**Recommendation.** Fold to two printed rules after fixing F1: "A Spark improves the dice
(anywhere)" and "A Spark buys reach (one Significant attempt pre-Technique; one step off a
Major for Focused)." Two sentences, one home, and the digital layer can enforce eligibility
silently — which is what the toolset is for.

---

### F10. LOW — Background pairs that are mechanical duplicates

Road Guard and Dockworker are both Athletics (Practiced) + Endurance (Novice, 1 mark); Guild
Apprentice and Hedge Scholar are both Lore + Investigate with a Mind domain-origin option
(II.5). They are distinct in fiction and Specialty only. This is defensible — Specialty is a
real mechanic (Standard→Easy) and the chapter is explicitly fiction-forward — but with 15 slots,
two intra-Facet duplicates spend variety the list doesn't have much of. Worth diverging one
skill in one member of each pair when the chapter is next touched; not worth a dedicated pass.

### F11. LOW — "Broad (Prismatic)" runs under three names

The type is "Broad," the acquisition tier is "prismatic," and the compound "Broad (Prismatic)"
appears in tables (II.3 Table II.3–2, II.3–3), while the Appendix says "All Prismatic domains
are Broad type." Techniques say "prismatic territories" but price "on the Broad difficulty
table" (II.4b, Ascendant Domain). Each usage is individually correct; together they force the
reader to learn that two words are one concept. Pick one player-facing word (Prismatic is the
evocative one) and demote the other to a single definitional sentence.

### F12. LOW — Chapter order makes new casters read magic before they know they have it

II.3 (Magic) precedes both the Facet chapters that grant the activating Technique and the
Background chapter that grants the domain origin — yet the domain "comes from your Background"
(II.3, *Acquiring a Domain*). A first-time reader meets 21 domains and a difficulty matrix
before learning whether their character is magical at all. II.1's walkthrough partly mitigates
this. A half-page "skip ahead unless your concept is magical" signpost at the top of II.3 —
or moving the domain quick-reference tables into the Appendix wholesale — would spare
non-casters the chapter and let casters arrive at it with a Background in hand.

### F13. LOW — Career Advances is bookkeeping the philosophy says software should absorb

Career Advances is "a single integer that counts every skill rank advance" (II.4), lives on the
paper sheet (II.1, sheet table), and no rule consumes it — it exists as a comparability
benchmark. It is fully derivable from the rest of the sheet. Keep the field in the character
file and the app; consider cutting it from the paper sheet and demoting Table II.4–3 to MM
Manual guidance, where cross-party comparability actually gets used.

### F14. LOW — The two weapon vocabularies will eventually reach the player

DESIGN_technique_difficulty §8 correctly rules that weapon *category* (heavy/standard/light/
ranged/unarmed — sets the attribute, IV.1) and Weapon Mastery's weapon *type* (blades/blunt/
polearms/unarmed — II.4a) are orthogonal axes. The book, however, never shows them together: a
player with Weapon Mastery carries a longsword that is "standard" in IV.1 and "blades" on their
Technique, and no table joins the two. One added column of examples in Table IV.1–1 (or a
type column) closes it. The recorded ranged gap in Weapon Mastery (no option for archers) is
already in docs/TODO.md and is correctly signposted in II.4a's italic note pointing archers to
Steady Hand — credit for that note.

### F15. LOW — Stale research docs contradict shipped math

research/advancement_priority_questions.md item #5 is marked RESOLVED with "Facet level 1 at
advance 6, level 2 at advance 12" and a "4 points per out-of-Facet failure" economy — both
superseded by the shipped 5/10/15 thresholds and flat 2-point cross-Facet cost (II.4). The doc
is a design record, not canon, but it is listed as a live reference and will mislead a future
contributor doing exactly what this review did. Add a superseded-by header note.

---

## 3. Casting-Decision-Chain Audit

Counting decisions and lookups for one spell, at two positions on the mastery curve.

**Best case — post-Technique Focused Fire mage, "freeze the lock shut" (Minor):**

| # | Step | Kind | Load |
|---|---|---|---|
| 1 | Is it in my domain? | Fiction check | Instant — "what does fire do?" is self-answered (the design's stated goal, magic_system_analysis) |
| 2 | State intent | Creative act | This is the fun, not friction |
| 3 | Declare scope | 3-way decision | Table II.3–1's examples calibrate it well |
| 4 | Find difficulty | Lookup, Table II.3–2 | One row of three cells — memorized by session 2, amortizes to zero |
| 5 | Attribute | None | Fixed by tradition (Spirit/Knowledge); only dual-tradition characters decide |
| 6 | Spark? | Optional decision | Usually "no" |
| 7 | Roll, read tier | Universal | Same three tiers as everything else |

**Net: 3 real decisions, 1 memorizable lookup, 0 page-flips.** This clears the design goal —
"describe what they want, know roughly how hard it is, roll... without looking anything up"
(magic_system_analysis, *Core Design Tension*) — comfortably. For comparison, the D&D-style
chain this replaces is: scan prepared list, pick spell, pick slot level, check components/range/
area, resolve rider rules. The subtraction is real and large.

**Worst case — pre-Technique Standard-domain caster with dual traditions attempting a
Significant effect:**

1. Domain fit (instant) → 2. intent → 3. scope — *blocked*: recall the Minor-only cap →
4. recall the Spark exception that buys one Significant attempt (II.3, *Sparks and Magic*) and
decide to spend → 5. difficulty lookup (Hard) → 6. attribute choice (dual tradition, II.3
*Rolling Magic*) → 7. separate decision: also spend a dice-Spark? (different rule, same
resource) → 8. MM situational adjustment → roll.

**Net: 6 decisions plus 2 recalled exceptions.** The doubling comes entirely from the Spark
sub-rules (F1, F9) and the pre-Technique overlay. The core chain is one of the lightest casting
loops in the hobby; the Spark joint is where a table will actually stumble, and it is the one
place in the chapter that reads like it was written in four passes.

Not counted above but real on the MM side: pricing scope is a recurring judgment call — the
inherent cost of the no-spell-list bet. The chapter supports it about as well as prose can
(the "same intent at three scopes" box, the benchmarks table, "scale of change and duration,
not how impressive the result looks").

---

## 4. Advancement Pacing Trace

**Subject: a starting Soul caster (Temple Acolyte, magical variant — Attune Practiced, domain
origin in place of the secondary skill), the flagship "new mage" experience.**

Economy: 4 skill points/session; Primary marks cost 1; 3 marks = rank advance; 5 rank advances =
Facet level; Facet level = 1 Technique (II.4). Realistic throughput is ~3–4 marks/session spread
over 2–3 used skills ≈ **~1 rank advance per session**, slightly more if focused.

| When | What happens | Payoff quality |
|---|---|---|
| Session 0 | Creation, ~20–30 min. Casting works from minute one at Minor scope | Strong — the playtest-derived scope cap means the mage *succeeds* at small magic immediately |
| Sessions 1–4 | Marks and ranks: a +1 (Practiced) lands roughly every session — on 2d6, each +1 is genuinely felt (dice_system_analysis) | Small but honest hits every session; no decisions, just marking |
| ~Session 4–6 | **Facet level 1 → Spiritual Domain → full scope.** The class fantasy completes | Big — but it is a forced pick (F4); the milestone is a door opening, not a choice made |
| ~Session 9–10 | Facet level 2 → **first freely chosen Technique** | The first real Expression moment in advancement arrives ~2.5 months into weekly play |
| ~Session 13–15 | Facet level 3 + first Major Advancement (they coincide by design, II.4 *Through the Mirror*) | Large — but requires Master rank in all five Soul skills, including ones the concept never touches, under the used-this-session rule (F5) |

**Verdict.** The cadence is honestly structured — a small payoff every session, a medium one
every ~4–5, a large one at ~14 — and the first big payoff arrives at a defensible interval.
Two blemishes: the mage's first unlock is predetermined (F4), so casters go ~9 sessions before
advancement asks them a question; and the road to the first Major runs through skills the
economy forces you to perform rather than play (F5). Note also that across this entire trace the
caster's *casting roll* never improves under the examples-as-written reading (F2) — the fighter
in the same party went from +1 to +3 on their signature roll in the same span.

---

## 5. Trap-Option and Dominant-Build Check

**Prismatic domains are not a new-player trap** — correctly. They are unavailable at creation
and gated behind Tier 3 (II.3, *Acquiring a Domain*), so the unmovable ceiling can never ambush
a first character. Credit: this is the right fence in the right place.

**Prismatic domains are arguably a veteran trap.** At Tier 3 the caster chooses between Second
Domain and Ascendant Domain. A Focused Second Domain prices Standard/Hard/Very Hard with a
movable ceiling; Ascendant prices Hard/Very Hard/Very Hard with an unmovable one (F3, F7). The
breadth-vs-reliability trade is a legitimate choice in principle, but the current numbers mean
the game's most expensive unlock is also its least reliable practice, and the feel-bad
concentrates at the most dramatic rolls. Within Second Domain itself, the Focused pick
dominates the Standard pick by a full tier at two of three scopes (F7).

**Step-easier passives quietly dominate their Tier 1 narrative twins.** Weapon Mastery (every
qualifying Strike one step easier) vs Forcing Hand (narrative marking); Steady Hand (all
Finesse, including ranged Strikes — the DESIGN doc itself calls the reading "slightly generous")
vs Fleet Step. On 2d6 a persistent step is among the strongest effects in the game, and the Q1
guardrail caps stacking but not pick-rate. The narrative twins are lovely, but a
mechanically-minded player will take the step every time; expect Tier 1 pick diversity to be
lower than the trees' width suggests. Mitigation is cheap: this matters much less at Tier 2–3,
where the permission-style Techniques carry real power.

**Never Surprised is the dominant Instinct Tier 1 and an MM-fun tax** (F8).

**The mage's forced Tier 1** (F4) is the inverse of a trap — a non-choice — but costs the same
aesthetic.

**Backgrounds contain no traps.** The magical trade (domain origin replaces the secondary
skill's 1-mark head start, II.5 *Magic and Backgrounds*) is a fair, legible price. The
duplicate pairs (F10) are a variety issue, not a trap.

**One structural double-dip worth watching** (adjacent scope, one line): the Endurance skill
both rolls and enlarges the Endurance pool (II.1 sheet table), making it the default second
mark-sink for every Body character; three of five Body Backgrounds already hand it out (II.5).
Expect Body characters to look samey at the secondary-skill slot.

**No degenerate loops found.** The Q1/Q2/Q3 composition doctrine (BRIEF_technique_difficulty)
has already fenced the classic ones: no character-side step stacking, no ambient Nth-domain
taxes, overrides explicit and frequency-capped. That governance work is why this section is
short.

---

## 6. Cut / Fold Candidates

Ordered by expected friction removed per word deleted.

1. **Rewrite/cut "Pushing scope"** (II.3, *Sparks and Magic*) — currently un-executable (F1).
   If nothing beyond Major is intended, the paragraph deletes cleanly.
2. **Fold the four magical Spark uses into two sentences** (F9): dice anywhere; reach in two
   defined cases. The Broad-ceiling exception folds into the same sentence.
3. **Fold the dual-domain-via-cross-Facet paragraph** (II.3, *Acquiring a Domain*: "A mage who
   already practises one domain can cross-train into the other Facet's Tier 1 Technique...")
   into one sentence. It is rules text for a build that costs an entire second tree's
   advancement — a case so rare the BRIEF itself notes such questions "only ever arise in one
   shape." One sentence plus MM discretion covers it; the current paragraph plus its
   one-domain-per-Facet guardrail is legalese pricing an abuse no real table will attempt.
4. **Fold "Broad (Prismatic)" to one term** (F11) — pure terminology, touches tables in II.3,
   the Appendix, and both Tier 3 Technique entries.
5. **Cut Career Advances from the paper sheet; keep it in the app** (F13). Demote the benchmark
   table to the MM Manual. This is the philosophy — "the digital layer absorbs bookkeeping" —
   applied to the book's own sheet.
6. **Fold the two weapon vocabularies into one table** (F14) — a column, not a rule change.
7. **Drop the unspent-points forfeit** (part of F5) — the banked-pool abuse it prevents cannot
   occur at 4 points/session with 3-mark ranks; the rule's only reliable output is the feel-bad
   its own example demonstrates.
8. **Do not cut:** the Secondary Skill mark (cheap, charming, hooks advancement), the Normal:
   fields (teaching apparatus), the 6− template box (MM burden relief), the "Do You Have It?"
   rule (three lines that replace an equipment list), or the scope-cap pre-Technique rule (the
   chapter's best decision). These are the small rules earning their keep.

---

*End of review. Companion audits: docs/RESEARCH_editorial_review.md (prose/apparatus),
docs/RESEARCH_completeness_audit.md (coverage). This document evaluates fun and ease of play
only; findings F1, F2, and F6 additionally imply engine/facet.yaml sync work if adopted, per
the Software-PHB sync iron law.*
