# Mirror Master's Manual: Encounters and Enemies

## Overview

This chapter gives you the tools to build enemies, assign them a Threat Rating, and calibrate how hard an encounter will feel for a given party — without requiring a full character sheet for every bandit in the room.

The system has three layers:

1. **Enemy stat blocks** — a minimal set of numbers sufficient to run any enemy in the full exchange structure
2. **Threat Rating (TR)** — a single number summarizing how dangerous one enemy is
3. **Encounter Budget** — a comparison of total enemy Threat against party strength, giving you a difficulty read before you run the scene

---

## Enemy Stat Blocks

Enemy stat blocks are intentionally minimal. You do not need everything a player character has. You need enough to run the exchange structure faithfully.

### The Minimal Stat Block

```
Name/Type
Tier: Mook | Named | Boss
Endurance: [number]
Attack: [roll modifier]  — e.g. +2 (Strength +1, Combat Practiced +1)
Defense: [roll modifier] — same modifier used for Parry; Dodge uses Dex modifier if different
Armor: None | Light | Heavy
Conditions: [current condition track — blank at start]
Techniques: [list, if any]
Special: [phase changes, triggers, or narrative rules — Boss only]
TR: [Threat Rating — calculated below]
```

**Named NPC example** — City Watch Sergeant:
```
City Watch Sergeant
Tier: Named
Endurance: 6
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
Endurance: — (Mooks have no pool; one Strike removes them)
Attack: +0 (Strength +0, Combat Novice +0)
Defense: +0
Armor: None
TR: 1
```

**Boss example** — The Archive Guardian (from Chapter III.3):
```
Archive Guardian
Tier: Boss
Endurance: 10
Attack: +3 (Strength +2, Combat Expert +2) — strikes with iron weight, not technique
Defense: +1 (Dexterity −1, Combat Practiced +1... partially damaged)
Armor: Heavy
Techniques: —
Special: Phase change — when first Broken, enters Reduced Mode (Attack drops to +1,
         but ignores Tier 1 Conditions entirely — it does not feel them)
TR: 16
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

**Durability** — based on enemy tier and Endurance pool:

| Enemy Type | Durability Value |
|---|---|
| Mook (no Endurance, one Strike) | 0 |
| Named NPC, Endurance 3–4 | 2 |
| Named NPC, Endurance 5–6 | 3 |
| Named NPC, Endurance 7–8 | 4 |
| Boss, Endurance 9–10 | 5 |
| Boss, Endurance 11–12 | 6 |
| Boss, Endurance 13+ | 7 |

**Armor bonus:**

| Armor | Bonus |
|---|---|
| None | 0 |
| Light | 1 |
| Heavy | 2 |

**Technique bonus** — for each Technique or special ability the enemy has that materially affects the exchange structure:

| Technique type | Bonus |
|---|---|
| One relevant Technique (e.g. Weapon Mastery) | 1 |
| Two or more Techniques | 2 |
| Boss phase change | 2 |
| Exceptional special (area attacks, regeneration, immune to Tier 1) | 3 |

### TR Reference Examples

| Enemy | TR | Notes |
|---|---|---|
| Basic Mook (unskilled, no armor) | 1 | Offense 2, Durability 0 — minimum 1 |
| Skilled Mook (Combat Practiced, light armor) | 4 | Offense 3, Durability 0, Armor 1 |
| City Watch Sergeant | 8 | Offense 4, Durability 3, Armor 1 |
| Veteran Soldier | 10 | Offense 5, Durability 3, Armor 2 |
| The Archive Guardian | 16 | Offense 5, Durability 5, Armor 2, Special 4 |

> **TR minimums by tier:**
> - Mook: TR 1 (even the most incompetent attacker occupies space and splits attention)
> - Named NPC: TR 8 (a Named NPC that poses no real threat isn't named — they're a Mook with a name)
> - Boss: TR 12 (a Boss that doesn't require sustained effort isn't a Boss — it's a Named NPC with a phase)

---

## Encounter Budget

The **Encounter Budget** is how you calibrate an encounter's difficulty before running it.

### Party Strength

Party Strength is the sum of all participating characters' `career_advances`.

> *Zahna, Mordai, and Zulnut each have `career_advances: 1`. Party Strength = 3.*

### Encounter Budget by Difficulty

| Difficulty | Win Rate Target | Total Enemy TR | Description |
|---|---|---|---|
| **Skirmish** | ~95% | Party Strength × 1 | Party should win cleanly; resources mostly intact |
| **Standard** | ~75% | Party Strength × 2 | Genuine danger; someone likely takes a Tier 2 Condition |
| **Hard** | ~50% | Party Strength × 3 | A coin flip; someone likely goes Broken; requires good decisions |
| **Deadly** | ~25% | Party Strength × 4 | Party is expected to lose the straight fight; winning requires cleverness or exceptional luck |

The win rate targets are the design intent. The multipliers (×1/×2/×3/×4) are a working estimate. See `research/simulation_log.md` for simulation results and calibration notes. If playtesting reveals the actual win rates are systematically off, adjust the multipliers accordingly and record what changed.

> **Calibration note (2026-03-05, PS 3 party, Mook-only swarms):**
> Simulation against pure Mook swarms suggests the ×1.25 action economy multiplier (4–6 enemies) may slightly overstate difficulty — five chickens produced 100% win rate despite sitting at the effective TR budget for Standard. The ×1.5 multiplier (7+ enemies) appears better-calibrated: seven chickens produced approximately 75% win rate, matching the Standard difficulty target. Provisional recommendation: for **Mook-only swarms** of 4–6, consider ×1.1 as a working estimate instead of ×1.25. Named NPC and mixed encounters are unaffected.

> **Example — fresh party (Party Strength 3):**
>
> - Skirmish (≤ TR 3): Two basic Mooks — party wins with Endurance to spare.
> - Standard (≤ TR 6): Four Mooks, or one Named NPC — a real fight, outcome not guaranteed.
> - Hard (≤ TR 9): One Named NPC with Mook support (e.g. Sergeant + two Harbor Thugs, TR 8+2=10, borderline) — expect someone Broken.
> - Deadly (≤ TR 12): The Archive Guardian at TR 16 is above even the Deadly budget for this party — and that is intentional; see *Running Asymmetric Encounters* below.

### Action Economy Adjustment

Raw TR comparison doesn't account for one important factor: **action economy**. More enemies mean more actions per exchange, which scales faster than raw TR suggests.

Apply these modifiers to the enemy side's effective TR when assessing difficulty:

| Enemy Configuration | TR Multiplier | Notes |
|---|---|---|
| Single enemy | × 0.75 | Solo enemies underperform their TR — the party concentrates fire |
| 2–3 enemies | × 1.0 | Baseline |
| 4–6 enemies | × 1.25 | Action pressure compounds; some party members face forced Absorbs. For Mook-only swarms, provisional ×1.1 may be more accurate — see calibration note above |
| 7+ enemies | × 1.5 | Swarming creates genuine tactical overload; validated at ~75% win rate for PS 3 party vs 7 Mooks |

> **Example:** Three City Watch Sergeants (TR 8 each = 24 total), adjusted for 3 enemies: 24 × 1.0 = **24 effective TR**. Against a Party Strength of 3, that is eight times party strength — well above Deadly (budget 12). This party would need to be very creative, or very lucky, or both.

---

## Building Enemies

### Mooks

Mooks need only three things: an attack modifier, a fictional description, and a number. They do not have Endurance. They do not have individual Condition tracks. One Strike at any tier removes them.

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
- Endurance pool
- Attack modifier (best offensive roll modifier)
- Defense modifier (what they use to Parry; or note if they Dodge instead)
- Armor
- One or two Techniques if they should feel distinct

**Resist over-building.** A Named NPC who lasts two exchanges and dies memorably is better than one who lasts six exchanges and becomes a slog. Use Hard difficulty against them to make fights meaningful; don't pad their Endurance to make them last.

---

### Bosses

Bosses should be built to last *and* to change. A Boss that simply has more Endurance is a longer fight, not a better one. A Boss with a phase change is a fight with a second act.

**Phase changes** are narrative triggers — usually when the Boss hits a specific Condition or has their Endurance reduced past a threshold — that shift something about how the fight works. Not necessarily harder; sometimes stranger.

> *The Archive Guardian's phase change: when first Broken, it enters Reduced Mode. Its attack drops. But it begins ignoring Tier 1 Conditions entirely — not because it's powerful, but because the thing that was interpreting sensory feedback has shut down. It's running on something else now. What that is, the party doesn't know.*

**Useful phase change patterns:**
- **Reveal:** The Boss's true capability or nature becomes visible (a hidden second attack, a domain that was being held in reserve)
- **Restriction:** The Boss loses an option that made them dangerous, but gains a different kind of pressure
- **Environment shift:** The Boss does something to the space — floods the room, collapses the floor, draws Mooks in — that changes the tactical situation entirely
- **Negotiation window:** The phase change is the Boss's breaking point; if the party reads this and acts, the fight can end without anyone going Broken

Phase changes should feel like story beats, not just mechanical resets. The fiction should change, not just the stat block.

---

## Running Asymmetric Encounters

Sometimes an encounter is designed to be asymmetric — the party cannot win by hitting things until they stop moving. The Archive Guardian encounter from Chapter III.3 is an example: at TR 16 against a Party Strength of 3, it is a Deadly encounter on paper, but it was never intended as a straight fight. Zahna's glyph, Zulnut's structural read, and the specific weak joint Mordai exploited were all intended paths around the raw numbers.

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
  endurance: 6
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

For Mooks, the format simplifies further:

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
3. Calculate enemy TR budget: Party Strength × difficulty multiplier
4. Build enemy roster: mix of Mooks, Named NPCs, and (rarely) a Boss
5. Apply action economy multiplier if 4+ or 7+ enemies
6. Adjust for asymmetric design if the encounter has a clever solution path

TR Formula:
  TR = offense_value + durability_value + armor_bonus + technique_bonus

Encounter Budget:
  Skirmish = Party Strength × 1
  Standard = Party Strength × 2
  Hard     = Party Strength × 3
  Deadly   = Party Strength × 4

Action Economy:
  Solo enemy      × 0.75
  2–3 enemies     × 1.0
  4–6 enemies     × 1.25
  7+ enemies      × 1.5
```
