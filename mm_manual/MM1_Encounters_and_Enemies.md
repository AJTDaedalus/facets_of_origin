# Mirror Master's Manual: Encounters and Enemies

Building a fight is three jobs, and only one of them is arithmetic.

The first is **stating an enemy** — the smallest set of numbers that lets you run something in a full exchange without writing it a character sheet. The second is **rating it**, so you can compare a harbour tough to an archive guardian without playing both fights first. The third is **choosing how many**, which is the one that actually decides whether your table has a good evening, and the one where the obvious tool is the wrong tool.

This chapter does them in that order, and it is honest about which of its numbers are simulation-validated and which are educated guesses.

And when you would rather not build anything: the **Bestiary** is eighteen creatures that arrive finished, sorted by Threat Rating, every one of them already carrying the conduct this chapter would otherwise have you invent.

This chapter gives you the tools to build enemies, assign them a Threat Rating, and calibrate how hard an encounter will feel for a given party — without requiring a full character sheet for every bandit in the room.

The system has three layers:

1. **Enemy stat blocks** — a minimal set of numbers sufficient to run any enemy in the full exchange structure
2. **Threat Rating (TR)** — a single number summarizing how dangerous one enemy is
3. **The Encounter Recipe Table** — simulation-validated rosters mapped to difficulty; this is the tool you actually build encounters from. Actor count, not summed TR, is what drives difficulty (see *Sizing an Encounter*, MM1).

---

## Enemy Stat Blocks

Enemy stat blocks are intentionally minimal. You do not need everything a player character has. You need enough to run the exchange structure faithfully.

### The Minimal Stat Block

```
Name/Type
Tier: Mook | Named | Boss
Resolve: [number]  — the durability pool Strikes deplete; Named 3–4, Boss ~8; Mooks have none
Attack: [modifier]  — e.g. +2 (Strength +1, Combat Practiced +1)
Armor: None | Light | Heavy  — adds a flat bonus to Resolve (light +1, heavy +2)
Techniques: [list, if any]
Special: [phase changes, triggers, or narrative rules — Boss only]
TR: [Threat Rating — calculated below]
```

An enemy has no Condition track of its own. A PC's Strike depletes Resolve — 2 on a full success (10+), 1 on a partial (7–9) — and the enemy is defeated when Resolve reaches 0. On a full success the attacker may *additionally* leave the enemy **Open**: Easy to Strike for everyone, with the player narrating what it looks like, until the enemy visibly spends its action to recover. Spending that action is your legitimate anti-snowball move — the party sees it and can answer it. Open never defeats an enemy on its own. A **Mook** has no Resolve at all: any success removes it (an armored Mook needs a full success).

**Named NPC example** — City Watch Sergeant:
```
City Watch Sergeant
Tier: Named
Resolve: 3
Attack: +2 (Strength +1, Combat Practiced +1)
Armor: Light
Techniques: —
TR: 8
```

**Mook example** — Harbor Thug:
```
Harbor Thug
Tier: Mook
Resolve: — (Mooks have no pool; one Strike removes them)
Attack: +0 (Strength +0, Combat Novice +0)
Armor: None
TR: 2
```

**Boss example** — The Archive Guardian (from Chapter III.3):
```
Archive Guardian
Tier: Boss
Resolve: 8 (effective 10 with heavy armor)
Attack: +3 (Strength +2, Combat Expert +2, −1 from fifteen years of wear) — iron weight, not technique
Armor: Heavy
Techniques: phase_change
Special: Phase change — when Resolve drops to 2 or below, enters Reduced Mode
         (Attack drops to +1 and its blows land as Tier 1, but it stops
         registering harm — left Open, it never spends an action recovering)
TR: 16
```

---

## Threat Rating

**Threat Rating (TR)** is a single number summarizing how dangerous an enemy is in combat. It is not a precise simulation — it is a calibration tool.

### Calculating TR

```
TR = offense + durability + armor_bonus + technique_bonus
```

**Offense** — the enemy's attack modifier (attribute + skill, an authoring input — NPCs don't roll):

**Table MM1–1: Offense Value by Attack Modifier**

| Attack Modifier | Offense Value |
|---|---|
| −2 or lower | 0 |
| −1 | 1 |
| +0 | 2 |
| +1 | 3 |
| +2 | 4 |
| +3 | 5 |
| +4 | 6 |

**Durability** — an enemy's base Resolve (the armor bonus below is added separately):

**Table MM1–2: Durability Value by Enemy Type**

| Enemy Type | Durability Value |
|---|---|
| Mook (no Resolve, one Strike) | 0 |
| Named NPC | its base Resolve (typically 3–4) |
| Boss | its base Resolve (typically ~8) |

Durability is simply the enemy's base Resolve — the pool a party's Strikes deplete. A Mook has none, so its durability is 0.

**Armor bonus:**

**Table MM1–3: Armor Bonus**

| Armor | Bonus |
|---|---|
| None | 0 |
| Light | 1 |
| Heavy | 2 |

**Technique bonus** — **+1 for each Technique or special ability** listed on the enemy (a phase change, a Weapon Mastery, an area attack, and the like each count as one). The bonus is simply the number of entries in the enemy's Techniques list, so an enemy with two Techniques adds +2. Keep the list to abilities that materially affect the exchange — don't pad it with flavor.

### TR Reference Examples

**Table MM1–4: TR Reference Examples**

| Enemy | TR | Notes |
|---|---|---|
| Basic Mook (unskilled, no armor) | 2 | Offense 2, Durability 0 |
| Skilled Mook (Combat Practiced, light armor) | 4 | Offense 3, Durability 0, Armor 1 |
| City Watch Sergeant | 8 | Offense 4, Durability 3, Armor 1 |
| Veteran Soldier | 11 | Offense 5, Durability 4 (Resolve 4), Armor 1, Techniques 1 (Telegraphed Finisher) |
| The Archive Guardian | 16 | Offense 5, Durability 8 (Resolve 8), Armor 2, Techniques 1 |

> **Example — rating an enemy from scratch**
>
> The MM needs a harbour tough for a scene at the Thornwall docks. Not a name, not a threat — a body in a doorway.
>
> **Offense.** Strength 2, no Combat rank: attack modifier +0, which is offense value **2**.
> **Durability.** A Mook, so base Resolve 0 — durability value **0**.
> **Armor.** A leather jerkin, which is light: **+1**.
> **Techniques.** None: **+0**.
>
> `TR = 2 + 0 + 1 + 0 = 3`. Above the Mook minimum of 1, well under the Named minimum of 8, which is the arithmetic agreeing with the fiction: this is somebody's muscle, not somebody.
>
> Now the same body promoted. Give him Combat at Practiced (attack +1 → offense 3), a name, and Resolve 3, and TR goes to 7 — *below* the Named minimum. That is the formula telling the MM something true: a Named NPC at Resolve 3 with one skill rank is not yet worth the party's attention. Either give him a Technique, better armor, or leave him a Mook.

**TR minimums by tier.** A **Mook** is TR 1 at minimum — even the most incompetent attacker occupies space and splits attention. A **Named NPC** is TR 8: one that poses no real threat is not named, it is a Mook with a name. A **Boss** is TR 12: one that does not require sustained effort is not a Boss, it is a Named NPC with a phase.

---

## Sizing an Encounter

**Actor count drives difficulty, not total TR.** This is the single most important thing to know about building encounters in this system. Simulation (`research/simulation_log.md` Series 9) is unambiguous: **the number of Named/Boss enemies acting at once** is the primary difficulty variable. One Named or one Boss is trivial for a fresh party no matter how high its TR — the party simply concentrates fire and removes it. Two of them are still nearly a walkover, and even three on their own is a near-clean win (~96%). **A real fight begins once three simultaneously-acting Named/Boss enemies are backed by a Mook or two** — four Named is a coin-flip (Hard), five is a near-certain loss. Mook swarms, meanwhile, never produce genuine danger at any size a table would field.

Because of this, **the calibrated tool you build from is the [Encounter Recipe Table](#encounter-recipe-table) below** — concrete, simulation-validated rosters mapped to difficulty. There is deliberately no TR-summing budget in this book: earlier editions carried one, and simulation proved it structurally non-predictive — summed TR cannot see the actor-count threshold that actually gates difficulty. (The retired budget and its multipliers are preserved for the record in `docs/DECISIONS.md`.) TR remains what it always was: a per-enemy build and ordering number, not an encounter-sizing one.

### Party Strength

Party Strength is the sum of all participating characters' `career_advances`. The Recipe Table is keyed to it.

> **Example — Party Strength**
>
> *Zahna, Mordai, and Zulnut each have `career_advances: 1`. Party Strength = 3.*

> **Example — why summed TR cannot size a fight**
>
> Three City Watch Sergeants total 24 TR — eight times a Party Strength of 3, a number that looks catastrophic. Simulation says otherwise: three TR-8 Named enemies against a fresh PS-3 party is a near-clean win (~96% party win) — a Standard fight only *once you add a Mook*. What the sum cannot see is that three Named is barely the threshold at which difficulty becomes *tunable* at all — you climb from there by adding actors, one at a time.

---

## Building Enemies

### Mooks

Mooks need only four things: an attack modifier, a fictional description, an armor decision, and a TR number. They do not have Resolve. They do not have individual Condition tracks. Any successful Strike (7+) removes one — an armored Mook takes a full success (10+).

**What makes a Mook dangerous is volume.** Three Mooks attacking simultaneously each demand a reaction decision. Absorbing a Mook attack costs no Endurance Pool points — but it lands a Tier 1 Condition, and Winded (−1 to your next roll) or Off-Balance (your next reaction costs 1 additional Endurance Pool point) is exactly the handicap a character cannot afford in the same exchange a Named NPC's Tier 2 attack comes in. Mook chip damage defeats no one; it degrades the reactions that matter.

**A Mook-only encounter must carry a clock or an objective.** Pure Mook attrition cannot lose — the simulation record is unambiguous — because the party can always recover faster than chip damage accumulates. What makes a Mook fight matter is what the Mooks are *for*: the ritual finishing behind them, the gate closing, the reinforcements a Threat Clock is counting down, the prisoner being dragged away. Give every Mook-only fight a stake the uncontested-exchange rule can advance (see *The Exchange*, Chapter III.3), and the fight is about time, not survival.

**Building a Mook:**
1. Assign an attack modifier (usually −1 to +1 for cannon fodder; up to +2 for elite troops)
2. Give them one sentence of fictional description — what do they look like, how do they move?
3. Decide if they have armor (most don't; light armor on guard captains is fine)
4. Calculate TR

You rarely need more than two or three Mook types per setting. Players will not notice if every city guard uses the same stat block.

---

### Named NPCs

Named NPCs use the full exchange structure. Build them the same way you'd build a player character — Primary Facet, relevant attributes, a skill or two — but you only need the numbers you'll actually use at the table.

**The short list you actually need:**
- Resolve (3–4 for a Named NPC; armor adds to it)
- Attack modifier (the best offensive attribute-plus-skill pairing, as an authoring input)
- Armor
- One or two Techniques if they should feel distinct

**Resist over-building.** A Named NPC who lasts two exchanges and dies memorably is better than one who lasts six exchanges and becomes a slog. Use Hard difficulty against them to make fights meaningful; don't pad their Resolve to make them last.

### Three Worked Enemy Techniques

Enemy Techniques are the "feel distinct" line above made concrete. These three are mechanical templates — setting-agnostic shapes you reskin to fit the enemy in front of you. Each adds +1 TR, and each is a stat-block-ready `techniques:` entry.

**Flurry** — pressure everyone at once.

```yaml
  techniques: [flurry]
  # Flurry: once per scene, its attack targets every PC engaged with it
  # in one action. Each incoming hit lands at Tier 1 (whatever the
  # enemy's usual tier); each target reacts separately.
```

A reaction-economy attack: it trades one heavy blow for a demand on everybody's Endurance Pool in the same exchange. Strongest alongside a second enemy whose Tier 2 is arriving simultaneously — the chip degrades the reactions that matter. Reskin freely: a sweeping tail, a volley, a shove through the whole line.

**Telegraphed Finisher** — the visible killing blow.

```yaml
  techniques: [telegraphed_finisher]
  # Telegraphed Finisher: once per scene, against a character already
  # carrying a Tier 2 Condition, its attack repeats that Condition's
  # type — a landed repeat is Broken (III.3). The MM names the move
  # one full exchange before it can land. Always.
```

This is the incoming-Condition selection rule (III.3) sharpened into a signature move. The telegraph is not a courtesy, it is the mechanic: the whole table gets one exchange to answer — Intercept, Withdraw, treat the Condition, end the fight first. Reskin: the raised axe, the drawn-back sting, the word of unbinding half-spoken.

**Sapping Strike** — exhaust instead of injure.

```yaml
  techniques: [sapping_strike]
  # Sapping Strike: its attacks drain the tank instead of landing a
  # Condition — a hit that lands (Absorb, or a failed reaction) costs
  # the target 2 Endurance Pool points instead of the Condition tier. A partial
  # reaction halves it to 1.
```

A tempo weapon: it never moves anyone toward Broken, but it empties the pool that pays for Dodges and Parries — the enemy that follows it hits a party that can no longer afford to react. Reskin: draining cold, a wrestler's clinch, anything that wins by exhaustion.

---

### Bosses

Bosses should be built to last *and* to change. A Boss that simply has more Resolve is a longer fight, not a better one. A Boss with a phase change is a fight with a second act.

**Phase changes** are narrative triggers — keyed to a `resolve_threshold` on the Boss's stat block, crossed when a Strike depletes their Resolve past that point — that shift something about how the fight works. Not necessarily harder; sometimes stranger.

> **Example — the Archive Guardian changes phase**
>
> *The Archive Guardian's phase change: when its Resolve drops to 2 or below, it enters Reduced Mode. Its attack drops. But it stops registering harm — left Open, it will never spend an action recovering, because the thing that was interpreting sensory feedback has shut down. It's running on something else now. What that is, the party doesn't know.*

**What a phase change may actually do.** A phase must change something that is live *right now*, in the exchange the party is fighting through — a piece of the enemy's runtime state, not a number that was already spent. Four levers do this, and they are the whole toolbox:

- **Raise its danger.** The Boss's attack grows — a higher incoming Condition tier, or a more aggressive posture. It hits harder, or its Strikes are harder to react to. ("It stops holding back.")
- **Grant or revoke a Special.** The Boss gains or loses a standing rule. The Archive Guardian's Reduced Mode is exactly this: it *stops spending actions to recover — once Open, it stays Open.* A held-in-reserve domain that switches on, a vulnerability that opens, an immunity that drops — all the same lever.
- **Second wind.** The Boss adds Resolve — a genuine durability spike the party can *see*, because it moves the same bar they've been grinding down. Use it sparingly; it is the honest version of "the fight isn't over."
- **Change the space or the target.** The Boss floods the room, collapses the floor, pulls Mooks in, or fixes on a new PC. This is MM-narrated — the engine doesn't track it — but it changes the tactical picture as much as any stat.

**What a phase change may *not* do: crack its own armor.** Do not write a phase as "its armor falls away" or "it trades defense for offense." Under our rules armor is a flat, one-time bonus baked into the Boss's starting Resolve pool the moment the fight begins (see *Armor bonus*, above) — there is no armor value sitting on the stat block mid-fight for a phase to reduce. A "the plating cracks, now it's vulnerable" phase looks evocative and does *nothing*: the pool it would have drained was already spent into the starting number. If you want a Boss to get more fragile, that is not a phase — it is simply a lower Resolve. If you want a phase to raise the stakes, use one of the four levers above.

Phase changes should feel like story beats, not just mechanical resets. The fiction should change *and* something the party can act on should change with it — never the fiction alone dressed over a stat that can't move.

> **MM Note — build for the early exit, not against it**
>
> A Tier 3 capstone like *The Final Blow* (Body/Might, II.4a) can end a Boss outright, on any target, once per session — that is what the Technique is for, and it is not subject to Open's never-defeats limit (see *Strike*, III.3). If a Boss's second act only exists in your notes and never in the fiction the party can act on, a capstone landing early does not just skip a phase — it skips the *encounter*. Build Bosses so the party deleting them is a win, not a broken script: front-load anything the phase change was protecting (a hostage taken, information dropped mid-fight, an environmental threat the Boss was suppressing) so it is already live by the time a capstone could land, rather than something the party only sees by grinding Resolve down in order.

---

## Running Asymmetric Encounters

Sometimes an encounter is designed to be asymmetric — the party cannot win by hitting things until they stop moving. The Archive Guardian encounter from Chapter III.3 is an example: at TR 16 against a Party Strength of 3, it is a Deadly encounter on paper, but it was never intended as a straight fight. Zahna's glyph, Zulnut's structural read, and the specific weak joint Mordai exploited were all intended paths around the raw numbers.

**Design asymmetric encounters deliberately:**
- Give the party something to notice (an environmental element, a phase change trigger, a behavioral rule)
- Give the party something to exploit (a structural weakness, a limitation in the enemy's programming, a negotiation opening)
- Make the straight fight winnable but costly — it should be a real option, just an expensive one

> **MM Note — a lateral solution is the encounter working**
>
> If a player finds a clever lateral solution that bypasses most of the TR, they have not broken the encounter — that is the encounter working correctly. TR is a calibration tool, not a ceiling.

---

## Enemy Conduct Fields

A stat block says how hard something is. These say how it behaves, and the Bestiary
renders them straight out of the file — an enemy written without them is a
spreadsheet row.

**`disposition:`** its whole combat philosophy in one sentence.
**`first_target:`** who it goes for, and why.
**`triggers:`** a list of if-then rules — not a round-by-round script. **Posture
lives here.** Enemy stances are not declared blind — you state them openly as
each exchange opens (see *Postures*, Chapter III.3) — so write the stance as a
rule the table can learn: "Aggressive while its allies stand; Defensive once
Open; Withdrawn when its morale line is crossed." A stated stance driven by a
visible trigger is threat texture the party can read and play against; a
stance you invent fresh each exchange is noise.
**`morale:`** when it stops. Every enemy needs one; nothing fights to the death by
default.
**`organization:`** how many turn up together.
**`negotiation:`** for Named and Bosses that can be dealt with — what it wants,
what shifts it, what deal it honours. Leave it out when there is no deal to be had,
and the absence means exactly that.

The older free-text `tactics:` field still loads and is still read, but new enemies
should use the fields above: they are what the Bestiary and the app can actually
find.

---

## Enemy TR in `.fof` Files

Enemy stat blocks can be stored as `.fof` files using `type: enemy`. The format mirrors the character format for the fields that matter:

```yaml
fof_version: '0.1'
type: enemy
id: city_watch_sergeant
name: City Watch Sergeant

enemy:
  tier: named
  resolve: 3              # base durability pool; armor adds to it in play
  attack_modifier: 2      # Strength +1, Combat Practiced +1
  armor: light
  techniques: []
  special: null
  tr: 8

  description: >
    A mid-rank officer of the city watch. Experienced in crowd control,
    street violence, and the particular skill of making someone feel
    arrested before they've decided whether to resist. Fights
    methodically — not inspired, but very hard to rattle.
```

The durability field is `resolve`. (Older files that still use `endurance` load
with a deprecation warning — they are mapped to a `resolve` value automatically
— but write `resolve` in anything new.) A **Boss** adds a `phases` block: each
phase has a `resolve_threshold` and a `description`, and crossing that threshold
as Resolve is depleted triggers the phase in play. For example, the Archive
Guardian's:

```yaml
  phases:
    - resolve_threshold: 2
      description: >
        Reduced Mode. Its attack drops — blows land as Tier 1 — but it
        stops registering harm: once Open, it stays Open.
```

For Mooks, the format simplifies further — a Mook has no `resolve` field at all:

```yaml
fof_version: '0.1'
type: enemy
id: harbor_thug
name: Harbor Thug

enemy:
  tier: mook
  attack_modifier: 0
  armor: none
  tr: 2

  description: >
    Hired muscle. Doesn't want to die for this job.
    Will absolutely run if the Named NPC they're working for goes down first.
```

---

## Quick Reference: Encounter Building

```
1. Establish party career_advances total → Party Strength
2. Choose difficulty: Skirmish / Standard / Hard / Deadly
3. Look up the roster in the Encounter Recipe Table (below) — this is the build step
4. Reflavor the roster to fit the story (numbers stay, fiction changes)
5. Add one lateral solution / asymmetric hook if the fight has a clever path

Actor-count rule of thumb (PS 3 fresh party):
  0–3 Named/Boss ........ clean win at any TR (3 Named ~96%)
  3 Named + 1 Mook ...... Standard (first real fight)
  +1 Mook each step ..... Standard → Hard → Deadly (1/2/3 Mooks)
  4 Named + 1 Mook ...... also Deadly
  Mook swarms alone ..... only ever a Skirmish

TR Formula (for building one enemy):
  TR = offense_value + durability_value + armor_bonus + technique_bonus
```

---

## Encounter Recipe Table

This is the tool you build encounters from. It maps difficulty to concrete enemy compositions that automated simulation has *measured* landing in the intended band — not derived from TR arithmetic, which (as shown above) mis-predicts multi-enemy fights.

**How to use:** Find your party's column. Pick the difficulty row. Use the suggested enemy composition. Adjust flavor (Mooks become cultists, Named becomes a captain, Boss becomes a dragon) without changing the mechanical profile.

### Party Strength 3 (3 fresh characters, 1 career advance each)

Validated in `research/simulation_log.md` Series 9 Part D (200 iterations per seed, seeds 1/2/3; the Sim Win Rate column lists all three seeds).

**Table MM1–5: Encounter Recipes at Party Strength 3**

| Difficulty | Win Rate Target | Suggested Composition | Sim Win Rate (seeds 1/2/3) |
|------------|----------------|-----------------------|-------------|
| **Skirmish** | 85–100% | 3–7 Mooks | 100% / 100% / 100% |
| **Standard** | 65–85% | 3 Named (TR 8) + 1 Mook | 76% / 74.5% / 80% |
| **Hard** | 40–60% | 3 Named (TR 8) + 2 Mooks | 47.5% / 48% / 47% |
| **Deadly** | 15–35% | 3 Named (TR 8) + 3 Mooks, or 4 Named (TR 8) + 1 Mook | 20% / 20% / 22.5% · 20% / 16.5% / 21% |

Note what these rosters have in common and what a TR budget would never tell you: **the Standard-through-Deadly ladder is built by adding actors, not by raising TR.** The core is three TR-8 Named in every band; you climb the ladder by adding a single throwaway Mook at a time — one Mook is Standard, two is Hard, three is Deadly. (Swapping that third Mook for a fourth Named, then trimming a Mook, lands the same Deadly window — the "upgrade a throwaway to a real threat" reading.) Per-enemy TR is a fine-tuning knob *after* you've set the actor count — 3× TR-10 Named is far harder than 3× TR-8 — but actor count is the dial you reach for first.

### Party Strength 4 (4 PCs or 3 advanced PCs)

> **Through the Mirror — these numbers are not yet simulated**
>
> Series 9 measured the PS-3 party only. The compositions below are *un-simulated extrapolations* from the PS-3 findings and the "each additional PC shifts the actor-count thresholds up by roughly one Named" rule of thumb — treat them as a starting guess to be confirmed at your table, not as validated recipes. Do not present them to players as calibrated.

**Table MM1–6: Encounter Recipes at Other Party Strengths**

| Difficulty | Win Rate Target | Suggested Composition (extrapolated, unvalidated) |
|------------|----------------|-----------------------|
| **Skirmish** | 85–100% | 4–8 Mooks |
| **Standard** | 65–85% | 4 Named (TR 8) |
| **Hard** | 40–60% | 4 Named (TR 8) + 1 Mook |
| **Deadly** | 15–35% | 5 Named (TR 8) |

### Scaling Notes

- **Actor count is the primary dial; per-enemy TR is secondary.** For a fresh PS-3 party, one or two Named/Boss enemies is trivial at *any* TR (a solo TR-17 Boss wins for the party as reliably as a solo TR-8 Named). Three simultaneously-acting Named/Boss enemies is the first genuine fight; four is Deadly; five is a near-certain party loss. Set the count first, then adjust per-enemy TR to fine-tune.
- **Mook swarms only ever produce Skirmishes.** For a PS-3 party, mean PCs Broken stays at zero through 30 Mooks — the party is never in real danger, the fight just gets longer. (Win rate does eventually dip past ~40 Mooks, but that is the simulator's exchange cap timing out an unfinished-but-unlost fight, not a defeat.) Use Mooks for texture, action-economy pressure, and to nudge a Named fight up a band — not as a difficulty lever in their own right.
- **Each additional PC** shifts the actor-count thresholds up by roughly one Named enemy (unvalidated beyond PS 3 — see the PS-4 caveat above).
- **Advanced parties** (Techniques active) trivialize encounters designed for fresh PS-3 parties. Expect to add actors, not just TR — and re-check at the table, since the actor-count thresholds themselves move.
- **The recipes above are calibrated for a baseline party** — `standard_party()` in the simulation corpus carries no Techniques. A party fielding *Weapon Mastery* — the one step-easier Technique that eases a Strike — or a Tier 3 capstone like *The Final Blow* runs a Recipe Table encounter about a band hot. The other step-easier Techniques ease rolls a fight rarely calls for — hardship, scholarship, precision work, and acting on a hunch — so they do not shift a combat recipe at all — treat the difficulty row you picked as one notch easier than printed.

---

## The Five-Minute Encounter Design Method

A quick framework for designing balanced encounters without a calculator.

### Step 1: What's the story?

Every encounter exists to serve the narrative. Ask: what does this fight (or potential fight) accomplish? If the answer is "I need a fight here," redesign the scene. A good fight creates decisions — and the best ones send the table home with a story.

### Step 2: Pick a difficulty feel.

- **Skirmish** — The party should win. This encounter taxes a few Endurance Pool points and establishes the threat. Use when: introducing a new enemy type, pacing between major beats, rewarding players for good preparation.
- **Standard** — A real fight. Someone will take conditions. Sparks will be spent. This is the default difficulty for most encounters. Use when: the stakes matter and the outcome is uncertain.
- **Hard** — Someone might go down. Requires smart posture choices and possibly a lateral solution. Use when: the climax of an arc, protecting something important, facing a worthy adversary.
- **Deadly** — The party should NOT fight this straight. This encounter exists to be solved, circumvented, or fled from. If they fight it and win, that's a story they'll tell forever. Use when: the Big Bad, a force of nature, a fight that should feel impossible.

### Step 3: Build the enemy roster.

Use the Encounter Recipe Table above. Find your party's column, pick the difficulty row, and use the suggested enemy composition. Adjust flavor without changing the mechanical profile. And remember while the fight runs: **adding enemies mid-fight is the sharpest dial you own — one Mook is one difficulty band (76% → 47% → 20%).**

### Step 4: Add one lateral solution.

For Standard and above, design at least one way the party can shortcut the encounter through clever play: an environmental hazard they can exploit, a weakness they can discover, a social angle that ends the fight. This isn't a consolation prize — it's the intended design. The lateral solution IS the encounter.

### Step 5: Sanity check.

Run through one exchange mentally. Does the first exchange feel dangerous but survivable? Can the party's tank absorb two hits? Can the fragile character contribute without dying immediately? If yes, you're good. If the math says "party wipe in exchange 1," dial it back. If the math says "party wins without spending Endurance Pool points," dial it up.

> **MM Note — The golden rule**
>
> If you're unsure between two difficulties, pick the easier one. Players who feel competent take bigger risks. Players who feel punished play conservatively. The easier fight leads to more interesting decisions.

### The "Three Encounter Session" Template

Most sessions have 2–3 encounters. The ideal difficulty arc:

1. **Opening:** Skirmish or light Standard — warm-up, establish the threat, let players feel competent
2. **Rising action:** Standard or Hard — the real challenge, resource drain, stakes escalate
3. **Climax:** Hard or Deadly — the payoff, lateral solutions welcome, maximum tension

**Never:** Hard → Hard → Hard. This exhausts resources without narrative payoff. The second fight feels like grinding, and the third feels unfair.

**Never:** Deadly as the opener. Players need to feel competent before you challenge them.

The Encounter Recipe Table above confirms the shape of this arc at each individual band — Skirmish (100% win rate), Standard (~76–80%), Hard (~47–48%) — so a Skirmish → Standard → Hard session climbs through progressively tighter margins by design, ending in genuine late-session tension where smart play and lateral solutions determine the outcome.
