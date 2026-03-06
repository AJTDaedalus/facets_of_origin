# Conflict Resolution

This document explains how the tool merges multiple loaded ruleset modules and resolves conflicts. It covers the rationale, the full decision table, and worked examples.

## Rationale

Facets of Origin supports layered ruleset modules: a base module provides the complete core rules, and expansions or campaign overrides extend or adjust specific parts. The merge system must:

1. **Be deterministic** — identical inputs always produce identical output
2. **Be transparent** — when two modules conflict, the tool tells you which ones and why
3. **Default to "extend"** — most content (skills, techniques, attributes) accumulates across modules
4. **Protect singletons** — mechanic-level rules (dice, thresholds, advancement) have one owner
5. **Allow denial** — a module can explicitly suppress content from lower-priority modules

## Priority Ordering

Modules are sorted by `priority` before merging. Lower priority = loads first = lower authority.

| Priority Range | Owner |
|---|---|
| 0 | `base` module — always loads first |
| 1–9 | Official expansions |
| 10–99 | Community modules |
| 100 | Campaign overrides (always win) |

Within a priority tier, modules are sorted alphabetically by `id` for determinism.

## Merge Types

### Extend (Collections)

Collections are merged by key. The later-loaded module's entry replaces the earlier one on key collision. No warning is emitted — replacement is expected.

Keys used:
- `attributes.major[]` → `id`
- `attributes.minor[]` → `id`
- `attributes.ratings[]` → `rating` (int)
- `character_facets[]` → `id`
- `skills[]` → `id`
- `techniques[facet_id][branch_id][tier][technique_id]` → nested keys

### Override (Singletons)

Only one active definition is allowed. The highest-priority non-null value wins. If two modules both define the same singleton, the tool emits a warning naming both.

Singletons:
- `roll_resolution`
- `spark`
- `advancement`
- `attribute_distribution`

### Denial

A collection entry with `status: removed` suppresses the definition from any lower-priority module with the same key. The tool hides denied items from UI and excludes them from character validation. A warning is emitted to make the suppression visible.

Currently applicable to:
- `skills[].status: removed`

## Full Decision Table

| Field | Merge Type | Collision Behaviour | Warning? |
|---|---|---|---|
| `attributes.major[]` | Extend | Later ID replaces earlier | No |
| `attributes.minor[]` | Extend | Later ID replaces earlier | No |
| `attributes.ratings[]` | Extend | Later rating# replaces earlier | No |
| `attribute_distribution` | Singleton | Higher priority wins | Yes if both non-null |
| `character_facets[]` | Extend | Later ID replaces earlier | No |
| `skills[]` | Extend | Later ID fully replaces earlier | No |
| `skills[].status = removed` | Denial | Hides from UI, excluded from validation | Yes |
| `techniques[facet][branch][tier]` | Extend | Later technique ID replaces earlier | No |
| `roll_resolution` | Singleton | Higher priority wins | Yes if both non-null |
| `spark` | Singleton | Higher priority wins | Yes if both non-null |
| `advancement` | Singleton | Higher priority wins | Yes if both non-null |
| Campaign `overrides.*` | Singleton | Always wins (priority 100) | Yes if overriding |
| Character `attributes` | N/A (snapshot) | Validated against ruleset | Error if invalid |
| Character `skills` | N/A (snapshot) | Validated against ruleset | Error if invalid |

---

## Worked Examples

### Example 1: Two Modules Both Define `roll_resolution`

**Scenario:** `base` (priority 0) defines `roll_resolution`. A community module `gritty-combat` (priority 10) also defines `roll_resolution` with lower success thresholds.

**Merge result:** `gritty-combat` wins — it has higher priority. The tool emits:

```
WARNING: roll_resolution defined by both "base" (priority 0) and "gritty-combat" (priority 10).
         "gritty-combat" wins. If this is unintentional, check your module list.
```

**Design note:** If the author of `gritty-combat` intends this, they should set `merge_hints.roll_resolution: override` to document the intent. The tool will still warn, but the warning message will include `(author declared override intent)`.

---

### Example 2: A Module Removes a Skill

**Scenario:** `base` defines `fortune` (a Soul skill). A community module `low-magic` (priority 10) wants to remove luck-based mechanics. It includes:

```yaml
skills:
  - id: fortune
    name: Fortune
    facet: soul
    attribute: luck
    description: "Acting on hunches, pressing luck, recognising the thing that matters."
    status: removed
```

**Merge result:** `fortune` is suppressed. The tool emits:

```
WARNING: skill "fortune" removed by module "low-magic" (priority 10).
         It was previously defined by "base" (priority 0).
         Characters with fortune skill points will fail validation.
```

The tool hides `fortune` from the skill list in the UI. Characters built under `base` who have `fortune` in their skill list will fail import validation if `low-magic` is active.

---

### Example 3: Campaign Overrides Sparks

**Scenario:** `base` sets `spark.base_sparks_per_session: 3`. The campaign GM wants 4 sparks per session for a high-action campaign.

**Campaign file:**

```yaml
overrides:
  spark:
    base_sparks_per_session: 4
```

**Merge result:** Campaign overrides apply at priority 100. `base_sparks_per_session` becomes 4 for all sessions in this campaign. The tool emits:

```
INFO: Campaign "the-shattered-crown" overrides spark.base_sparks_per_session: 3 → 4.
```

This is an info-level message (not a warning) because campaign overrides are an expected, sanctioned operation.

---

### Example 4: Extension Module Adds Skills

**Scenario:** `base` defines 15 skills. A community module `maritime-skills` (priority 10) adds `sailing` and `navigation`.

**Merge result:** The merged ruleset contains 17 skills. No warnings — this is the expected use of the extend mechanism. Characters may freely take `sailing` or `navigation` as skills if `maritime-skills` is in the active module list.

---

### Example 5: Two Community Modules Define the Same Technique

**Scenario:** `martial-arts` (priority 10) and `street-fighter` (priority 12) both define a technique with `id: swift_strike` under `body.might.tier_1`.

**Merge result:** `street-fighter` wins (higher priority). No warning is emitted because technique collision is treated as extend behaviour (later replaces earlier). Module authors who anticipate collision should document it in their module's `description` or `changelog`.

---

## Module Compatibility Checking

Before merging, the tool runs compatibility pre-checks:

1. **Dependency resolution** — all `requires` constraints must be satisfied. If `maritime-skills` requires `base >= 0.1.0` and only `base 0.0.9` is loaded, load fails.

2. **Incompatibility check** — `incompatible_with` lists module IDs that cannot coexist. If `gritty-combat` declares `incompatible_with: [heroic-combat]` and both are in the campaign module list, load fails with an error naming both modules and which declared the incompatibility.

3. **Circular dependency detection** — if module A requires B and B requires A, load fails with a cycle error.

All three checks run before any merging begins.
