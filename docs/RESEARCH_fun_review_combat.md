# Fun & Ease-of-Play Review: Combat and Encounter Mechanics

**Date:** 2026-08-08
**Scope:** `player_handbook/III.3_Combat.md`, `mm_manual/MM1_Encounters_and_Enemies.md`,
`mm_manual/MM5_Quick_Reference.md`, evaluated against `research/simulation_log.md`
(Series 6–9), `playtest/01_thornwall_undercroft/playtest_report.md`,
`research/armored_enemy_breaking_problem.md`, and
`research/dice_system_analysis.md`.
**Lenses:** MDA (mechanic → table dynamic → aesthetic), fun, ease of play,
subtraction design. Two qualities only: does it produce fun, and is it easy to run.

---

## 1. What Works

The core verdict first: **the exchange system delivers its promise.** The
playtest measured combats at 2–3 exchanges, 10–20 minutes, with the players
calling it "tactically light but decision-heavy" (playtest_report.md, Alex's
feedback). Nobody waits for an initiative slot; everyone declares posture every
beat; the defender rolls dice on the enemy's "turn" (reactions), which is the
single best anti-waiting mechanic in the design — the person being attacked is
the person holding the dice. The promise is "no queue," not literal simultaneity
(the vignette in III.3 still walks the spotlight Mordai → Zulnut → Zahna), and
that's the right promise to keep.

Specific things that verifiably work, with the fixes-landed audit the earlier
rounds earned:

- **Three-tier resolution carries combat unchanged.** No separate tactical
  subsystem exists; Strike/Dodge/Parry/Maneuver/Support all resolve on the same
  2d6 table (III.3 Tables III.3-3, III.3-4). Playtest: "Every roll produced a
  story beat."
- **Conditions-instead-of-HP produces story, not tracking pain — for PCs.**
  Playtest: "'Staggered' tells a story that '-8 HP' doesn't." The load stays
  small because Tier 1 self-clears at end of exchange (III.3 §Tier 1
  Conditions) — the "Through the Mirror" box there documents exactly the
  subtraction reasoning (Weary/Spent/Bleeding/Exposed cut) this review was
  asked to re-apply. That cut was correct and it held.
- **The Resolve/Condition asymmetry is excellent MM ergonomics.** One number
  per enemy, no enemy condition track (III.3 §Through the Mirror — "why
  enemies lose Resolve"). It also *dissolved* the armored-enemy-unbreakable
  bug entirely (`research/armored_enemy_breaking_problem.md`, RESOLVED
  2026-07-10) — the fix landed by deleting the loop's subject, which is the
  best kind of fix.
- **All three playtest "Must Fix" ambiguities landed.** Enemy posture →
  reaction difficulty (III.3 Table III.3-9), incoming tier by enemy type
  (Table III.3-8), armor/reaction non-stacking with the charge-not-spent
  refinement (III.3 §Armor and Reaction Downgrades). Group Rolls landed in
  MM5. Pre-technique magic penalty was removed (MM5: "Minor scope only, at
  the domain's normal difficulty — no extra penalty"), directly answering
  Riley's 0-for-3 frustration. Spark-flow MM guidance (midpoint diagnostic,
  Graceful Fail targets) landed in MM5 §Spark Flow. Verified present.
- **K1 (Aggressive surcharge on first reaction only) is a sim-proven fun
  repair.** Series 8: Broken rate for a fragile Aggressive PC cut 15.7–18.7%
  across 7 seeds while Aggressive's offense edge stayed within 0.6pp. The
  Series 3 Run 4 disaster ("Aggressive at 1 Endurance made all reactions cost
  2") can no longer eat a whole exchange of reactions.
- **The Recipe Table is honest and validated.** MM1's Encounter Recipe Table
  is built from Series 9 Part D (200 iterations × 3 seeds per row), the PS-4
  table is explicitly flagged un-simulated, and the withdrawn "~95/75/50/25%"
  multiplier claims are named as withdrawn. A rulebook that says which of its
  numbers are measured and which are guesses is rare and worth protecting.
- **Boss fights are tense, not grindy.** Post-A14/A15 numbers: Archive
  Guardian fight, median 3.0 exchanges across 7 seeds, mean 6.2 of 9 Sparks
  spent, Zahna finishing as low as 0 Endurance (Series 7 G1 re-run). That is
  "survivable but expensive" delivered in three dramatic beats — the opposite
  of a grind. The old 12–16-exchange boss slogs died with the enemy-Parry
  model, and good riddance.
- **NPCs-never-roll is the right call and is now documented.**
  `dice_system_analysis.md` §"NPCs Never Roll" supplies precedent (PbtA, FitD,
  Cypher) and the two-pillar justification; it halves dice handling per
  exchange and keeps the MM watching faces instead of adding numbers.
- **The digital layer absorbs the right things.** III.3 Table III.3-16 ("Your
  Five Numbers On Screen") covers Endurance, posture, Conditions, Sparks, and
  armor budget (auto-applied with log annotation). The bookkeeping-heavy parts
  of the design are exactly the parts the app owns.

---

## 2. Findings

Severity: **High** = actively hurts fun or adds table friction; **Medium** =
real but survivable; **Low** = polish.

### F1 — HIGH: Stale "enemies react/Parry" text contradicts the settled no-roll model

**Mechanic:** III.3 §Named NPCs: "Named NPCs and significant antagonists use
the full combat structure: Resolve, Posture, reactions, the works" and "**A
primary attribute and skill** — the modifier they use for Strikes and
Parries." Also MM1 §Enemy TR in `.fof` Files: `defense_modifier: 2 # same
roll for Parry`.
**Dynamic:** A new MM reading the PHB will conclude enemies roll Parries
against PC Strikes. The sim history proves the stakes: A14's removal of the
enemy Parry moved *every recipe a full difficulty band* (Series 9 Part C → D,
e.g. Hard 48.5% → 76%). An MM who house-rules enemy reactions back in from
this stale text is silently running every published recipe one band harder —
the exact dual-implementation drift the project has already been burned by
(MM5's own "Through the Mirror" box tells that war story).
**Evidence:** simulation_log.md Series 9 Part C header ("Model correction
(task A14) ... enemies never react — depletion is outcome-only ... moved
every recipe below ~one difficulty band"). MM1's stat-block Defense line was
corrected ("an authoring input, not a rolled modifier"); these two spots were
missed.
**Recommendation:** Fix III.3's Named NPC bullet to "Strikes" semantics that
match the no-roll model (attack modifier is an authoring input; PCs react),
change "reactions, the works" to "Resolve, Posture, Techniques," and delete
"same roll for Parry" from the MM1 `.fof` example. Same-commit sync with
`facet.yaml` per house rules.

### F2 — HIGH: Withdrawn cycling is a sim-proven degenerate loop with only a narrative patch

**Mechanic:** Withdrawn = no offense, **all reactions free**, +2 Endurance at
end of exchange (III.3 Table III.3-2).
**Dynamic:** Against enemies that can't force the issue, a PC in Withdrawn is
strictly safe and net-positive on resources indefinitely. Series 6 A5 caught
it red-handed: 15 Mooks produced a **98% win rate over 14.5 mean exchanges**
via "Withdrawn posture cycling ... PCs recover 2 End per exchange while
dodging for free," and Series 9's 40-Mook runs only "lose" by hitting the
simulator's 20-exchange cap. The current countermeasure is one MM Note ("a
fighter who Withdraws three exchanges in a row is buying time, not winning the
fight, and the fiction should say so" — III.3 §Recovering Endurance), i.e.,
the MM must improvise pressure the rules don't supply.
**Evidence:** simulation_log.md A5, Series 9 Part B Mook-swarm sweep.
**Recommendation:** Smallest mechanical fix consistent with subtraction
design: Withdrawn recovers 2 Endurance **only if the fight is still pressing
you** is too fiddly; better is "recover 2 Endurance, max pool" plus a rule
that the *enemy side advances* — e.g., an uncontested exchange (no PC took an
offensive action) lets the MM escalate the situation for free (reposition,
reinforce, take the objective). That converts the loop into the tempo trade
the MM Note already claims it is, and it's a scene rule the MM applies once,
not per-character bookkeeping. Alternatively: accept it, but say in MM1 that
Mook-heavy fights must carry a clock, because pure attrition cannot lose.

### F3 — HIGH: The difficulty dial is a hair-trigger the fiction doesn't telegraph

**Mechanic:** MM1 Encounter Recipe Table — a fixed 3-Named core where **one
throwaway Mook per step** walks the ladder: 3 Named ~96% → +1 Mook 76% →
+2 Mooks 47.5% → +3 Mooks 20% (Series 9 Part D, three seeds each).
**Dynamic:** The gap between "someone probably takes a Tier 2" and "the party
probably loses" is *two guys who each die to any 7+*. Nothing in the fiction
signals this — a player looking at 3 sergeants + 3 thugs sees roughly the
same scene as 3 sergeants + 1 thug. An MM who improvises "two more guards
round the corner" mid-fight has just moved a Standard encounter to Deadly
without noticing, and the golden rule ("pick the easier one," MM1 §Five-Minute
Method) can't help if the MM doesn't know they're choosing. This is the
biggest live threat to the intended wave-shaped session curve (Skirmish →
Standard → Hard), which is otherwise achievable and sim-confirmed (MM1 §Three
Encounter Session template).
**Evidence:** simulation_log.md Series 9 Parts B/D; the 29-point swing from
one Mook is the single steepest number in the corpus.
**Recommendation:** (a) Say it in MM1 in exactly these terms: "adding enemies
mid-fight is the sharpest dial you own — one Mook is one difficulty band."
(b) Have the app's encounter builder display the computed band live as
enemies are added, and warn when a mid-combat spawn crosses a band. The
recipe knowledge exists; it needs to be in the MM's face at the moment of
temptation, not in a chapter read last week.

### F4 — MEDIUM: Posture choice degrades into an Endurance-keyed script

**Mechanic:** Blind simultaneous posture declaration (III.3 §Postures), sold
as "half the tactical game."
**Dynamic:** In practice the correct posture is a function of your own
Endurance bar, not a read of the opponent: high End → Aggressive, low End →
Defensive/Withdrawn. The simulator's AI literally plays that script
(Series 6 methodology: "high End→Aggressive, mid→Measured, low→Defensive,
0 End→Withdrawn") and posts the win rates the recipes are balanced against.
Three things starve the mind-game the blind reveal promises: Mooks don't
declare postures at all (III.3 §Enemy Posture); the one Boss the book stages
"is Measured — it always is" (III.3 vignette); and K1, which correctly fixed
the death spiral, also cut Aggressive's downside to at most 1 Endurance per
exchange, making Aggressive the default whenever the bar is healthy — the
playtest had already flagged "the optimal strategy is always Aggressive"
against Mooks (playtest_report.md §4). Posture is still a *real* choice at
low Endurance against multiple Named (Series 8's own data: Aggressive 89%
Broken vs Measured 52% in the 2-attacker scenario) — but that's a resource
readout, not a bluffing game.
**Evidence:** playtest_report.md §"Mook Combat Is Fun but Mechanically Thin";
simulation_log.md Series 6 methodology and Series 8.
**Recommendation:** Don't add mechanics — feed the existing ones. Enemy
posture is already a live dial that changes PC reaction difficulty (Table
III.3-9) and PC Strike difficulty (III.3 §Strike); the missing piece is
enemies that actually *use* it. Put posture behavior into the conduct fields
(`triggers:` — "Aggressive while a hostage is in reach; Defensive once
Staggered") so Named/Boss postures vary by design, and make the Insight
pre-read (III.3 MM Note "Reading the opponent") the advertised counter. If
enemy posture stays effectively constant, consider cutting the blind-reveal
ceremony for enemies entirely and just stating their stance — a ritual that
never surprises anyone is pure overhead.

### F5 — MEDIUM: The TR budget and action-economy multipliers survive their own obituary

**Mechanic:** MM1 Table MM1-5 (budget ×1/×2/×3/×4) and Table MM1-6 (solo
×0.75 / ×1.0 / ×1.25 / ×1.5), plus their MM5 compression.
**Dynamic:** Series 9 Part B proved the model is structurally wrong, not
mistuned: "This is not resolvable by retuning ... as scalar constants. The
measured relationship is neither linear nor separable." MM1 now spends ~40
lines of caveats apologizing for two tables it tells you not to use ("Do not
derive a multi-Named/Boss encounter from this table"). Tables outlive prose:
an MM skimming mid-prep will find the multiplication easy and the caveat
skippable, and build the exact 3-Sergeants-is-8×-Deadly encounter the worked
example debunks. Keeping a tool whose primary documented property is that it
misleads is friction, and the caveat text is itself reading load.
**Evidence:** simulation_log.md Series 9 Parts B/C; MM1 §Encounter Budget's
own withdrawal notice.
**Recommendation:** Cut both tables from MM1 and MM5. Keep TR (it works as a
per-enemy build/ordering number and the Recipe Table is keyed to it), keep
the Recipe Table and actor-count rule of thumb, and demote the budget math to
`docs/DECISIONS.md` as a historical record. This is the same knife that cut
Weary/Spent/Bleeding/Exposed, applied to MM-facing content.

### F6 — MEDIUM: The rider menu is a pseudo-decision; PC Condition text doesn't map onto enemies

**Mechanic:** On a 10+ Strike, hang "a Tier 1 or Tier 2 Condition of your
choice" on the enemy, "with their usual effects" (III.3 §Strike, §Named
NPCs).
**Dynamic:** Walk the menu against a non-rolling, non-reacting enemy:
Winded ("−1 to your next roll") — enemies don't roll; Off-Balance ("+1
Endurance on next reaction") — enemies don't react; Shaken ("MM may direct
your next action") — the MM already directs it; Staggered ("−1 to offensive
rolls") — no rolls, so only the Easy-to-Strike tag does anything; Cornered —
Easy tag plus a posture ban that matters only if the enemy's posture ever
varies (see F4). So the five-option "attacker's choice" is really a
one-option choice (take a Tier 2 for the Easy tag) wearing a menu costume —
a small analysis-paralysis tax with a hidden right answer, paid on every 10+.
It also makes the Archive Guardian's `tier1_immunity` an immunity to nothing
mechanical.
**Evidence:** Cross-reading III.3 Tables III.3-5/6 against §Enemy Attacks
("NPCs do not roll dice") and Series 9's no-enemy-reaction model. The
vignette itself never uses a Tier 1 rider — nobody would.
**Recommendation:** Merge. On a 10+ vs an enemy: "you may leave it **Open** —
Easy to Strike for everyone until it recovers" (one tag; the player narrates
what Open looks like — staggered, cornered, blinded, disarmed). Fiction keeps
the variety, mechanics drop four dead options and the enemies-borrow-PC-
condition-text indirection. If the full menu stays for Technique/immunity
hooks, add one honest sentence: "against enemies, Tier 1 riders are color;
the Easy tag is the mechanical payload."

### F7 — MEDIUM: Which Condition an enemy attack inflicts is unspecified — and it's the lethality dial

**Mechanic:** Enemy attacks state a tier (Table III.3-8) but no rule says who
picks the specific Condition, while Broken requires "a Tier 2 Condition they
already have" — same type twice (III.3 §Tier 2).
**Dynamic:** Under same-type escalation, the MM's unstated choice of *which*
Staggered/Cornered to apply decides whether a 0-Endurance PC breaks in two
hits or shrugs off an alternating pair forever. G2's own analysis measured
the gap: an alternating attacker breaks a target a full exchange later than a
repeating one, uniformly across armor tiers. The rules hide the game's
kill-switch inside an undocumented MM habit — that's invisible friction and
inconsistent lethality between tables.
**Evidence:** simulation_log.md Series 7 G2 (F6 variation test); III.3
§Incoming Condition Tier's silence on selection.
**Recommendation:** One sentence in III.3 and MM5: "The MM chooses the
incoming Condition; repeating the type a PC already carries is how an enemy
deliberately finishes someone — telegraph it." Making it explicit turns a
hidden knob into a dramatic beat the table can see coming.

### F8 — MEDIUM: Difficulty-source stacking on a Strike has no precedence rule

**Mechanic:** A single Strike's difficulty can be touched by: the MM's base
call (enemy posture/Constitution/situation, III.3 §Strike), a Tier 2 rider's
absolute "Easy to Strike," Maneuver's absolute "rolls against the target are
Easy," Support's relative "one step easier," a Technique's "one step further"
(capped at one per roll, III.1), and Specialty's Standard→Easy.
**Dynamic:** Absolutes and relatives don't compose by any stated rule. Is a
Defensive Boss (Hard) carrying a Staggered rider (Easy) at Easy, Standard, or
Hard? Does Support's step move Easy to something beyond Easy (no "Very Easy"
exists, so presumably it saturates — unstated)? The vignette quietly models
best practice ("It's already Easy to Strike ... pick the other Support
benefit"), which proves the authors know the collision exists; the rules just
never say it. Every table resolves this live, some of them differently.
**Evidence:** III.3 §Strike, §Maneuver, §Support; the Zulnut Support beat in
the vignette.
**Recommendation:** Three lines in III.3 (and the MM5 card): "Set the base
difficulty from the situation; an Easy tag (rider or Maneuver) overrides it
downward; steps (Support, Technique) then shift it, and Easy is the floor."
Whatever the precedence, printing one kills the ambiguity.

### F9 — MEDIUM: Enemy threat texture is monotone — every Named/Boss hit is Tier 2, forever

**Mechanic:** Fixed incoming tier by enemy type (Table III.3-8); no roll ever
gates whether an enemy attack "arrives"; an all-Absorb exchange resolves with
zero dice thrown.
**Dynamic:** `dice_system_analysis.md` already named this: "a Boss lands
Tier 2 every single time it acts. An enemy's competence never varies, only
the PC's response to it," with the flagged risks of same-y long fights and
variance concentrating on one player (the lowest-Endurance PC eats every
attack, by both sim targeting policy and sensible MM play). The near-miss
research the whole dice system is built on (visible tension, shared witness)
gets no purchase on the enemy's side of the exchange. This is a deliberate,
well-precedented trade — the recommendation there was "keep the rule" and
this review agrees — but the mitigation it prescribed (variable incoming
tier for some enemy actions; enemy Techniques that escalate) exists only as
a stub ("Boss Techniques may escalate further," Table III.3-8) with no
worked examples anywhere in III.3 or MM1.
**Evidence:** dice_system_analysis.md §"The open question this surfaces";
Table III.3-8's Boss row.
**Recommendation:** Ship two or three concrete enemy Techniques in MM1 that
vary the incoming picture (a Tier 1 flurry against multiple PCs; a
telegraphed Tier 2-that-repeats-type per F7; an attack that drains Endurance
instead of landing a Condition). The conduct fields and Technique bonus slots
already exist to hold them — the toolbox is built, it's just empty.

### F10 — LOW: MM posture load scales with exactly the fights the recipes prescribe

**Mechanic:** "Every participant (player characters and significant
antagonists alike) simultaneously declares a Posture" (III.3 §Postures) —
so a by-the-book Standard fight has the MM blind-declaring for 3 Named every
exchange, each posture then modifying that enemy's Strike difficulty *and*
reactions against it in opposite directions (III.3 §Strike, Table III.3-9).
**Dynamic:** 3–4 hidden decisions per exchange plus per-enemy difficulty
adjustments is the largest MM-side per-exchange load in the system, and the
playtest already listed enemy-posture tracking with auto-difficulty as an
unbuilt app feature (playtest_report.md, Tool Recommendations #5).
**Recommendation:** Build that feature (posture field on the enemy tracker
that auto-labels reaction difficulty), and let conduct-field triggers (F4)
make most enemy postures rule-driven rather than per-exchange decisions.

### F11 — LOW: The Defense stat claims to feed a formula it isn't in

**Mechanic:** MM1's minimal stat block: Defense "feeds the TR formula and
informs the difficulty you set" — but `TR = offense + durability +
armor_bonus + technique_bonus` (MM1 §Calculating TR) has no defense term, and
no table maps defense modifier → suggested Strike difficulty.
**Dynamic:** An authoring field with a false description and no usage rule is
a stat MMs will fill in and never use, or worse, use inconsistently.
**Recommendation:** Either delete `defense_modifier` from the block (the MM
already sets Strike difficulty by situation) or give it its one honest job in
a sentence: "+2 or better suggests Hard Strikes against this enemy while it
fights well." Fix the "feeds the TR formula" claim either way.

### F12 — LOW: MM5 omits three mid-combat rulings it will be asked for

**Mechanic:** MM5's combat cards are otherwise excellent compressions, but:
Intercept's once-per-exchange limit and "the protected ally decides who steps
in" (III.3 §Intercept) are absent from Table MM5-9; and nothing in MM5 or
III.3 says when a rider Condition on an *enemy* clears — Tier 2 clearing is
defined as "a narrative action addresses them" for PCs, and in every sim and
the vignette an enemy rider simply persists to the end of the fight, which
quietly guarantees the Easy-tag snowball once one lands.
**Recommendation:** Add the Intercept limit to the MM5 row; add one line to
III.3: "an enemy clears a rider only if the MM spends its action doing so —
visibly." (That also gives the MM a legitimate anti-snowball move that the
players can see and answer.)

### F13 — LOW: The physical-table fallback is thinner than the text admits

**Mechanic:** III.3 offers paper slips for blind posture, but the armor
budget ("applied automatically — the action log shows '(downgraded by
armor)'", Table III.3-16) and K1's first-reaction-this-exchange flag have no
suggested paper representation at all.
**Dynamic:** Digital-first is the stated design and the app genuinely absorbs
these; but a rules chapter that ships a paper fallback for one hidden-state
mechanic and not the other two invites the exact bookkeeping fumbles the
system exists to prevent at any table playing offline.
**Recommendation:** One sidebar: armor = N check-boxes on the sheet per
scene; first reaction = flip a token when you react, clear at exchange end.
Two sentences buy the whole offline story.

---

## 3. Per-Exchange Tracking-Load Audit

**A single player, one exchange, worst case (paper table):**

| # | Item | Kind |
|---|---|---|
| 1 | Posture (choose from 4, blind) | decision |
| 2 | Current Endurance | number |
| 3 | Own Conditions (up to ~3 live: Tier 1s + Tier 2s) | tags |
| 4 | Armor downgrade budget remaining (per scene) | number |
| 5 | Sparks | number |
| 6 | Press? (per Strike) | decision |
| 7 | Spark spend? (per roll, pre-roll) | decision |
| 8 | Reaction choice per incoming attack (4 options × N attackers) | decision |
| 9 | "Have I reacted yet this exchange?" (K1 surcharge flag, if Aggressive) | flag |
| 10 | Pending Support die / Easy tag owed to or by an ally | tag |

Ten items; roughly 4–6 of them are *decisions* and the rest are state. **With
the app, items 2, 3, 4, 5, and 9 vanish into the screen** (Table III.3-16 +
engine `reactions_this_exchange`), leaving the player holding only decisions —
which is precisely the design intent, and it is met. On paper, item 4 and 9
are the fumble risks (F13).

**The MM, per enemy:** Resolve (1 number), rider tags (0–2), posture
(Named/Boss only), phase threshold (Boss only) — 2 to 4 items, exactly as the
"Through the Mirror" box promises ("one number the MM can track for six
enemies at once without a spreadsheet"). The real MM load is not tracking but
**adjudication**: a base difficulty call per Strike (posture/situation), a
reaction difficulty per enemy attack (enemy posture), an invented complication
per 7–9, and a Condition pick per landed enemy hit (F7). Jamie's playtest
verdict — "easier than D&D but harder than Fate" — locates the cost
correctly: it's improv, not arithmetic. The remaining reducible arithmetic is
the enemy-posture bookkeeping (F10).

**Legal stack count on one Strike roll** (the prompt's stacking question):
dice adders — Press (1d6) + Sparks (1d6 each, ≥2 legal) + Support (1d6) →
up to **6d6 drop 4**; flat modifiers — attribute (+1) + skill (up to +3) +
Aggressive (+1) + difficulty (Easy +1) → **up to +6**; difficulty movers —
MM base call, rider Easy, Maneuver Easy, Support step, Technique step,
Specialty (composition unspecified, F8). A fully stacked roll is a
near-guaranteed 10+ — which is fine as a priced climax button (Sparks and
Endurance are real costs), but it is the fuel line of the snowball in §4.

---

## 4. Dominant-Strategy / Degenerate-Loop Check

1. **Withdrawn cycling** — confirmed degenerate by simulation (A5: 98% win
   over 15 Mooks by cycling; 40-Mook fights unlosable, only un-finishable).
   The only current counter is MM narration. See F2. **This is the one loop
   that needs a rules answer.**
2. **Aggressive-by-default** — against Mooks, strictly dominant (Tier 1
   incoming, Absorb free, Tier 1 self-clears; playtest §4 said it outright);
   post-K1, dominant whenever Endurance is healthy. Posture reduces to an
   Endurance-bar script the sim AI plays verbatim and wins with. Not
   game-breaking — the script is *thematically* sensible — but the blind
   mind-game the chapter advertises is underfed. See F4.
3. **Absorb-everything vs Mooks** — Absorb costs 0, Mook hits are Tier 1,
   Tier 1 expires at exchange end: reacting to a Mook is almost never worth
   1 Endurance. Sim agrees: mean PCs Broken **0.00 through 30 Mooks**
   (Series 9 Part B). Corollary: MM1 §Mooks' claim that a party Absorbing
   all Mook attacks "will arrive at the Named NPC already worn down" is
   false as written — Absorb spends nothing. Mooks' measured danger in mixed
   fights (the one-Mook-per-band cliff) comes from Tier 1 chip *degrading
   reactions against simultaneous Named Tier 2s* (Winded −1 on your next
   reaction roll; Off-Balance +1 on its cost), not from Endurance attrition.
   MM1 should teach the true mechanism — it's the actual reason the recipes
   work.
4. **Rider → Easy snowball** — first 10+ hangs a Tier 2 rider, everyone's
   subsequent Strikes go Easy, 10+s chain. The G1 escalation record shows it
   deleting the pre-retune Guardian in exchange 1; the shipped fix was more
   Resolve, so the snowball now *is* the boss-fight pacing (median 3
   exchanges — good) but also makes every Named/Boss fight the same shape:
   land the tag, then chain. Combined with the effectively-permanent enemy
   rider (F12), there is no counterplay from the enemy side. Giving the MM a
   visible clear-the-rider action (F12) and enemies that change posture (F4)
   are the cheap variety injections.
5. **Press + Spark + Support mega-stack** — legal, potent, and fine: it
   spends three separately-earned resources for one guaranteed moment, which
   is what climax resources are for. No change recommended; just document the
   difficulty-source precedence (F8) so the stack resolves the same way at
   every table.

---

## 5. Cut / Merge Candidates

Applying the Weary/Spent/Bleeding/Exposed knife to what remains:

| Candidate | Verdict | Rationale |
|---|---|---|
| **TR budget table + action-economy multipliers** (MM1-5, MM1-6, MM5 copy) | **Cut** | Proven structurally non-predictive (Series 9 Part B); survives only wrapped in warnings. The Recipe Table + actor-count rule already do this job. Biggest single friction win available. |
| **Rider Condition menu vs enemies** | **Merge** to one "Open (Easy to Strike)" tag | Four of five options are mechanically null against non-rolling, non-reacting enemies (F6). Fiction keeps the variety. |
| **Tier 1 riders on enemies specifically** | **Cut** (subsumed by the merge) | Zero mechanical effect; exists only so `tier1_immunity` has a referent. |
| **`defense_modifier` on enemy stat blocks** | **Cut or define** | Not in the TR formula despite the text's claim; no mapping to difficulty; a field with no job (F11). |
| **Blind posture declaration *for enemies*** | **Merge** into conduct-field triggers | If enemy posture is effectively constant (vignette Guardian: "Measured — it always is"), the reveal ceremony is overhead; rule-driven postures are cheaper and *more* readable as fiction (F4/F10). PC-side blind declaration stays — it's load-bearing for the simultaneity feel. |
| **Defensive posture** | **Keep, watch** | Narrow niche (mid Endurance, multiple Named attackers) and overlaps Withdrawn, but it's the only "turtle without leaving" option and costs nothing to know. Re-examine if playtests show it unpicked. |
| **Winded / Off-Balance / Shaken as three distinct Tier 1s** | **Keep** | Each touches a different resource (roll, Endurance, agency); they're the true mechanism of mixed-fight difficulty (§4.3). The earlier cut already took this tier to its floor. |
| **Dodge vs Parry** | **Keep** | Mechanically twins, but the stat split (Dex vs weapon+Combat) is character expression, and the fiction-gating MM Note is genuinely used. Cheap identity, no tracking cost. |

---

## Verdict

The chassis is sound and the project's feedback loops demonstrably work: the
playtest's three Must-Fix ambiguities are all in the text, the armored-enemy
loop was dissolved rather than patched, K1 is a sim-validated fun repair, and
the Recipe Table is the rare TTRPG balance tool that is actually measured.
Combat is fast, decision-dense, and light to track — with the app, a player
holds almost nothing but choices, and the MM holds one number per enemy.
The remaining work is subtraction and honesty, not addition: delete the
disproven budget math (F5), align the two stale enemy-reaction passages with
the no-roll model before someone rebuilds the drift (F1), give Withdrawn
cycling and the one-Mook-per-band cliff real answers (F2, F3), and collapse
the rider menu to the one choice it actually contains (F6). None of these are
redesigns; all of them are the same knife the project has already shown it
knows how to use.
