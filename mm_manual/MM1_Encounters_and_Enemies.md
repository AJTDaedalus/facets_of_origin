# Mirror Master's Manual: Encounters and Enemies

## Overview

This chapter gives you the tools to build enemies, assign them a Threat Rating, and calibrate how hard an encounter will feel for a given party — without requiring a full character sheet for every bandit in the room.

The system has three layers:

1. **Enemy stat blocks** — a minimal set of numbers sufficient to run any enemy in the full exchange structure
2. **Threat Rating (TR)** — a single number summarizing how dangerous one enemy is
3. **The Encounter Recipe Table** — simulation-validated rosters mapped to difficulty; this is the tool you actually build encounters from. (A rough TR budget is also provided, but it is a loose ordering check, not a difficulty predictor — see below.)

---

## Enemy Stat Blocks

Enemy stat blocks are intentionally minimal. You do not need everything a player character has. You need enough to run the exchange structure faithfully.

### The Minimal Stat Block

```
Name/Type
Tier: Mook | Named | Boss
Resolve: [number]  — the durability pool Strikes deplete; Named 3–4, Boss ~8; Mooks have none
Attack: [roll modifier]  — e.g. +2 (Strength +1, Combat Practiced +1)
Defense: [roll modifier] — same modifier used for Parry; Dodge uses Dex modifier if different
Armor: None | Light | Heavy  — adds a flat bonus to Resolve (light +1, heavy +2)
Techniques: [list, if any]
Special: [phase changes, triggers, or narrative rules — Boss only]
TR: [Threat Rating — calculated below]
```

An enemy has no Condition track of its own. A PC's Strike depletes Resolve — 2 on a full success (10+), 1 on a partial (7–9) — and the enemy is defeated when Resolve reaches 0. On a full success the attacker may *additionally* hang one rider Condition on the enemy; a Tier 2 rider (Staggered/Cornered) leaves it Easy to Strike until cleared, but riders never defeat an enemy on their own. A **Mook** has no Resolve at all: any success removes it (an armored Mook needs a full success).

**Named NPC example** — City Watch Sergeant:
```
City Watch Sergeant
Tier: Named
Resolve: 3
Attack: +2 (Strength +1, Combat Practiced +1)
Defense: +2
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
Defense: +0
Armor: None
TR: 1
```

**Boss example** — The Archive Guardian (from Chapter III.3):
```
Archive Guardian
Tier: Boss
Resolve: 8 (effective 10 with heavy armor)
Attack: +3 (Strength +2, Combat Expert +2) — strikes with iron weight, not technique
Defense: +1 (Dexterity −1, Combat Practiced +1... partially damaged)
Armor: Heavy
Techniques: phase_change, tier1_immunity
Special: Phase change — when Resolve drops to 2 or below, enters Reduced Mode
         (Attack drops to +1, but ignores Tier 1 Conditions entirely — it does not feel them)
TR: 17
```

---

## Threat Rating

**Threat Rating (TR)** is a single number summarizing how dangerous an enemy is in combat. It is not a precise simulation — it is a calibration tool.

### Calculating TR

```
TR = offense + durability + armor_bonus + technique_bonus
```

**Offense** — the enemy's attack roll modifier (attribute + skill):

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

| Enemy Type | Durability Value |
|---|---|
| Mook (no Resolve, one Strike) | 0 |
| Named NPC | its base Resolve (typically 3–4) |
| Boss | its base Resolve (typically ~8) |

Durability is simply the enemy's base Resolve — the pool a party's Strikes deplete. A Mook has none, so its durability is 0.

**Armor bonus:**

| Armor | Bonus |
|---|---|
| None | 0 |
| Light | 1 |
| Heavy | 2 |

**Technique bonus** — **+1 for each Technique or special ability** listed on the enemy (a phase change, a Weapon Mastery, an area attack, and the like each count as one). The bonus is simply the number of entries in the enemy's Techniques list, so an enemy with two Techniques adds +2. Keep the list to abilities that materially affect the exchange — don't pad it with flavor.

### TR Reference Examples

| Enemy | TR | Notes |
|---|---|---|
| Basic Mook (unskilled, no armor) | 1 | Offense 2, Durability 0 — minimum 1 |
| Skilled Mook (Combat Practiced, light armor) | 4 | Offense 3, Durability 0, Armor 1 |
| City Watch Sergeant | 8 | Offense 4, Durability 3, Armor 1 |
| Veteran Soldier | 10 | Offense 5, Durability 4 (Resolve 4), Armor 1 |
| The Archive Guardian | 17 | Offense 5, Durability 8 (Resolve 8), Armor 2, Techniques 2 |

> **TR minimums by tier:**
> - Mook: TR 1 (even the most incompetent attacker occupies space and splits attention)
> - Named NPC: TR 8 (a Named NPC that poses no real threat isn't named — they're a Mook with a name)
> - Boss: TR 12 (a Boss that doesn't require sustained effort isn't a Boss — it's a Named NPC with a phase)

---

## Encounter Budget

**Actor count drives difficulty, not total TR.** This is the single most important thing to know about building encounters in this system, and it is the opposite of what a TR-summing budget would tell you. Simulation (`research/simulation_log.md` Series 9) is unambiguous: **the number of Named/Boss enemies acting at once** is the primary difficulty variable. One Named or one Boss is trivial for a fresh party no matter how high its TR — the party simply concentrates fire and removes it. Two of them are still nearly a walkover, and even three on their own is a near-clean win (~96%). **A real fight begins once three simultaneously-acting Named/Boss enemies are backed by a Mook or two** — four Named is a coin-flip (Hard), five is a near-certain loss. Mook swarms, meanwhile, never produce genuine danger at any size a table would field.

Because of this, **the calibrated tool you should actually build from is the [Encounter Recipe Table](#encounter-recipe-table) below** — concrete, simulation-validated rosters mapped to difficulty. The TR budget that follows is kept only as a rough ordering sanity check for simple rosters. It is **explicitly non-predictive for encounters with 3+ Named/Boss enemies and for Mook swarms** — use the Recipe Table for those.

### Party Strength

Party Strength is the sum of all participating characters' `career_advances`.

> *Zahna, Mordai, and Zulnut each have `career_advances: 1`. Party Strength = 3.*

### The TR budget (a rough ordering check only)

| Difficulty | Intended feel | Total Enemy TR | Description |
|---|---|---|---|
| **Skirmish** | Clean win | Party Strength × 1 | Party should win cleanly; resources mostly intact |
| **Standard** | Genuine danger | Party Strength × 2 | A real fight; someone likely takes a Tier 2 Condition |
| **Hard** | Coin flip | Party Strength × 3 | Someone likely goes Broken; requires good decisions |
| **Deadly** | Expected loss | Party Strength × 4 | Party is expected to lose the straight fight; winning requires cleverness or exceptional luck |

The "intended feel" column is the *design intent* for each difficulty. The multipliers (×1/×2/×3/×4) are **not** validated to produce those feels — they are a loose "bigger number is probably harder" ordering aid for simple/solo/Mook rosters. Any earlier presentation of these as validated "~95/75/50/25%" win rates was withdrawn: simulation showed no set of multipliers can reproduce the real (actor-count-gated) difficulty curve. **Do not derive a multi-Named/Boss encounter from this table — it will over-count badly (see the example below). Use the Recipe Table.**

### Action Economy Adjustment

Raw TR comparison doesn't account for **action economy** — more enemies mean more actions per exchange. The modifiers below are the same kind of rough ordering aid as the budget itself, and carry the same caveat: they capture the *direction* (more actors, more pressure) but not the sharp actor-count threshold the simulator measured.

| Enemy Configuration | TR Multiplier | Notes |
|---|---|---|
| Single enemy | × 0.75 | Solo enemies badly underperform their TR — the party concentrates fire and removes them |
| 2–3 enemies | × 1.0 | Baseline |
| 4–6 enemies | × 1.25 | Action pressure compounds (Mook-only swarms: ×1.1) |
| 7+ enemies | × 1.5 | Swarming creates tactical overload |

> **Example — why the budget is only a rough check.** Three City Watch Sergeants (TR 8 each = 24 total, ×1.0 for three enemies = **24 effective TR**) sit at eight times a Party Strength of 3 — the raw budget screams "well above Deadly." Simulation says otherwise: three TR-8 Named enemies against a fresh PS-3 party is a near-clean win (~96% party win) — a Standard fight only *once you add a Mook*. The budget over-counted by more than a full difficulty band, because what it can't see is that three Named is barely the threshold at which difficulty becomes *tunable* at all — you climb from there by adding actors. This is exactly why the Recipe Table, not the budget, is the tool you build from.

---

## Building Enemies

### Mooks

Mooks need only three things: an attack modifier, a fictional description, and a number. They do not have Resolve. They do not have individual Condition tracks. Any successful Strike (7+) removes one — an armored Mook takes a full success (10+).

**What makes a Mook dangerous is volume.** Three Mooks attacking simultaneously each demand a reaction decision. A party with limited Endurance that chooses to Absorb all Mook attacks will arrive at the Named NPC already worn down.

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
- Attack modifier (best offensive roll modifier)
- Defense modifier (what they use to Parry; or note if they Dodge instead)
- Armor
- One or two Techniques if they should feel distinct

**Resist over-building.** A Named NPC who lasts two exchanges and dies memorably is better than one who lasts six exchanges and becomes a slog. Use Hard difficulty against them to make fights meaningful; don't pad their Resolve to make them last.

---

### Bosses

Bosses should be built to last *and* to change. A Boss that simply has more Resolve is a longer fight, not a better one. A Boss with a phase change is a fight with a second act.

**Phase changes** are narrative triggers — keyed to a `resolve_threshold` on the Boss's stat block, crossed when a Strike depletes their Resolve past that point — that shift something about how the fight works. Not necessarily harder; sometimes stranger.

> *The Archive Guardian's phase change: when its Resolve drops to 2 or below, it enters Reduced Mode. Its attack drops. But it begins ignoring Tier 1 Conditions entirely — not because it's powerful, but because the thing that was interpreting sensory feedback has shut down. It's running on something else now. What that is, the party doesn't know.*

**What a phase change may actually do.** A phase must change something that is live *right now*, in the exchange the party is fighting through — a piece of the enemy's runtime state, not a number that was already spent. Four levers do this, and they are the whole toolbox:

- **Raise its danger.** The Boss's attack grows — a higher incoming Condition tier, or a more aggressive posture. It hits harder, or its Strikes are harder to react to. ("It stops holding back.")
- **Grant or revoke a Special.** The Boss gains or loses a standing rule. The Archive Guardian's Reduced Mode is exactly this: it *starts ignoring Tier 1 Conditions.* A held-in-reserve domain that switches on, a vulnerability that opens, an immunity that drops — all the same lever.
- **Second wind.** The Boss adds Resolve — a genuine durability spike the party can *see*, because it moves the same bar they've been grinding down. Use it sparingly; it is the honest version of "the fight isn't over."
- **Change the space or the target.** The Boss floods the room, collapses the floor, pulls Mooks in, or fixes on a new PC. This is MM-narrated — the engine doesn't track it — but it changes the tactical picture as much as any stat.

**What a phase change may *not* do: crack its own armor.** Do not write a phase as "its armor falls away" or "it trades defense for offense." Under our rules armor is a flat, one-time bonus baked into the Boss's starting Resolve pool the moment the fight begins (see *Armor*, above) — there is no armor value sitting on the stat block mid-fight for a phase to reduce. A "the plating cracks, now it's vulnerable" phase looks evocative and does *nothing*: the pool it would have drained was already spent into the starting number. If you want a Boss to get more fragile, that is not a phase — it is simply a lower Resolve. If you want a phase to raise the stakes, use one of the four levers above.

Phase changes should feel like story beats, not just mechanical resets. The fiction should change *and* something the party can act on should change with it — never the fiction alone dressed over a stat that can't move.

---

## Running Asymmetric Encounters

Sometimes an encounter is designed to be asymmetric — the party cannot win by hitting things until they stop moving. The Archive Guardian encounter from Chapter III.3 is an example: at TR 17 against a Party Strength of 3, it is a Deadly encounter on paper, but it was never intended as a straight fight. Zahna's glyph, Zulnut's structural read, and the specific weak joint Mordai exploited were all intended paths around the raw numbers.

**Design asymmetric encounters deliberately:**
- Give the party something to notice (an environmental element, a phase change trigger, a behavioral rule)
- Give the party something to exploit (a structural weakness, a limitation in the enemy's programming, a negotiation opening)
- Make the straight fight winnable but costly — it should be a real option, just an expensive one

> If a player finds a clever lateral solution that bypasses most of the TR, that is not them breaking the encounter. That is the encounter working correctly. The TR budget is a calibration tool, not a ceiling.

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
  defense_modifier: 2     # same roll for Parry
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
        Reduced Mode. Its attack drops, but it stops registering Tier 1
        Conditions entirely.
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
  tr: 1

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

Rough TR budget (ordering check only — NOT a difficulty predictor;
use the Recipe Table, especially for 3+ Named/Boss or Mook swarms):
  Skirmish = Party Strength × 1     Solo enemy   × 0.75
  Standard = Party Strength × 2     2–3 enemies  × 1.0
  Hard     = Party Strength × 3     4–6 enemies  × 1.25
  Deadly   = Party Strength × 4     7+ enemies   × 1.5
```

---

## Encounter Recipe Table

This is the tool you build encounters from. It maps difficulty to concrete enemy compositions that automated simulation has *measured* landing in the intended band — not derived from TR arithmetic, which (as shown above) mis-predicts multi-enemy fights.

**How to use:** Find your party's column. Pick the difficulty row. Use the suggested enemy composition. Adjust flavor (Mooks become cultists, Named becomes a captain, Boss becomes a dragon) without changing the mechanical profile.

### Party Strength 3 (3 fresh characters, 1 career advance each)

Validated in `research/simulation_log.md` Series 9 Part D (200 iterations per seed, seeds 1/2/3; the Sim Win Rate column lists all three seeds).

| Difficulty | Win Rate Target | Suggested Composition | Sim Win Rate (seeds 1/2/3) |
|------------|----------------|-----------------------|-------------|
| **Skirmish** | 85–100% | 3–7 Mooks | 100% / 100% / 100% |
| **Standard** | 65–85% | 3 Named (TR 8) + 1 Mook | 76% / 74.5% / 80% |
| **Hard** | 40–60% | 3 Named (TR 8) + 2 Mooks | 47.5% / 48% / 47% |
| **Deadly** | 15–35% | 3 Named (TR 8) + 3 Mooks, or 4 Named (TR 8) + 1 Mook | 20% / 20% / 22.5% · 20% / 16.5% / 21% |

Note what these rosters have in common and what a TR budget would never tell you: **the Standard-through-Deadly ladder is built by adding actors, not by raising TR.** The core is three TR-8 Named in every band; you climb the ladder by adding a single throwaway Mook at a time — one Mook is Standard, two is Hard, three is Deadly. (Swapping that third Mook for a fourth Named, then trimming a Mook, lands the same Deadly window — the "upgrade a throwaway to a real threat" reading.) Per-enemy TR is a fine-tuning knob *after* you've set the actor count — 3× TR-10 Named is far harder than 3× TR-8 — but actor count is the dial you reach for first.

### Party Strength 4 (4 PCs or 3 advanced PCs)

> **Not yet simulation-validated.** Series 9 measured the PS-3 party only. The compositions below are *un-simulated extrapolations* from the PS-3 findings and the "each additional PC shifts the actor-count thresholds up by roughly one Named" rule of thumb — treat them as a starting guess to be confirmed at your table, not as validated recipes. Do not present them to players as calibrated.

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

---

## The Five-Minute Encounter Design Method

A quick framework for designing balanced encounters without a calculator.

### Step 1: What's the story?

Every encounter exists to serve the narrative. Ask: what does this fight (or potential fight) accomplish? If the answer is "I need a fight here," redesign the scene. Good fights create decisions. Great fights create stories.

### Step 2: Pick a difficulty feel.

- **Skirmish** — The party should win. This encounter taxes a few Endurance points and establishes the threat. Use when: introducing a new enemy type, pacing between major beats, rewarding players for good preparation.
- **Standard** — A real fight. Someone will take conditions. Sparks will be spent. This is the default difficulty for most encounters. Use when: the stakes matter and the outcome is uncertain.
- **Hard** — Someone might go down. Requires smart posture choices and possibly a lateral solution. Use when: the climax of an arc, protecting something important, facing a worthy adversary.
- **Deadly** — The party should NOT fight this straight. This encounter exists to be solved, circumvented, or fled from. If they fight it and win, that's a story they'll tell forever. Use when: the Big Bad, a force of nature, a fight that should feel impossible.

### Step 3: Build the enemy roster.

Use the Encounter Recipe Table above. Find your party's column, pick the difficulty row, and use the suggested enemy composition. Adjust flavor without changing the mechanical profile.

### Step 4: Add one lateral solution.

For Standard and above, design at least one way the party can shortcut the encounter through clever play: an environmental hazard they can exploit, a weakness they can discover, a social angle that ends the fight. This isn't a consolation prize — it's the intended design. The lateral solution IS the encounter.

### Step 5: Sanity check.

Run through one exchange mentally. Does the first exchange feel dangerous but survivable? Can the party's tank absorb two hits? Can the fragile character contribute without dying immediately? If yes, you're good. If the math says "party wipe in exchange 1," dial it back. If the math says "party wins without spending Endurance," dial it up.

> **The golden rule:** If you're unsure between two difficulties, pick the easier one. Players who feel competent take bigger risks. Players who feel punished play conservatively. The easier fight leads to more interesting decisions.

### The "Three Encounter Session" Template

Most sessions have 2–3 encounters. The ideal difficulty arc:

1. **Opening:** Skirmish or light Standard — warm-up, establish the threat, let players feel competent
2. **Rising action:** Standard or Hard — the real challenge, resource drain, stakes escalate
3. **Climax:** Hard or Deadly — the payoff, lateral solutions welcome, maximum tension

**Never:** Hard → Hard → Hard. This exhausts resources without narrative payoff. The second fight feels like grinding, and the third feels unfair.

**Never:** Deadly as the opener. Players need to feel competent before you challenge them.

Simulation data confirms this arc: Skirmish → Standard survives at 98%. Skirmish → Standard → Hard survives at 55% — genuine late-session tension where smart play and lateral solutions determine the outcome.
