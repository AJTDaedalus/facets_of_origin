# Type: campaign

A `campaign` file is the top-level container for a multi-session story arc. It declares the ruleset, enrolled characters, and session index. Campaign-level overrides apply at the highest priority (100), above all modules.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `fof_version` | string | FOF spec version |
| `type` | `"campaign"` | Type discriminator |
| `id` | slug | Unique ID, `^[a-z][a-z0-9\-_]*$` |
| `name` | string | Display name |
| `version` | semver | Content version |
| `authors` | list[string] | GM/creator names |
| `modules` | list[ModuleRef] | Active ruleset modules for this campaign |
| `started_at` | ISO 8601 date | Date the campaign started |
| `status` | StatusEnum | Campaign status |

## Optional Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `description` | string | `""` | Campaign summary |
| `overrides` | OverridesDef | `{}` | Campaign-level singleton overrides (priority 100) |
| `characters` | list[CharacterEntry] | `[]` | Enrolled character roster |
| `sessions` | list[SessionEntry] | `[]` | Session index |
| `session_count` | int | `0` | Total sessions played |
| `tags` | list[string] | `[]` | Descriptive tags for filtering/search |

## Status Values

| Value | Meaning |
|---|---|
| `active` | Campaign is ongoing |
| `hiatus` | Temporarily paused |
| `complete` | Story concluded intentionally |
| `archived` | Preserved but not playable |

## ModuleRef Format

```yaml
modules:
  - id: "base"
    version: ">=0.1.0"    # Semver constraint
  - id: "sailing-expansion"
    version: ">=1.0.0"
```

## Overrides

Campaign overrides apply to **singleton sections only** (fields that cannot be merged from multiple sources). They always win, regardless of module priority.

```yaml
overrides:
  spark:
    base_sparks_per_session: 4    # Override base ruleset's default of 3
  advancement:
    session_skill_points: 5       # Override base ruleset's default of 4
```

Permitted override targets (all singletons):

| Target | Overridable Fields |
|---|---|
| `spark` | `base_sparks_per_session`, `mechanic`, `earn_methods` |
| `advancement` | `skill_ranks`, `skill_point_costs`, `session_skill_points`, `marks_per_rank`, `facet_level_threshold` |
| `roll_resolution` | `dice`, `thresholds`, `outcomes`, `difficulty_modifiers` |
| `attribute_distribution` | `total_points`, `min_per_attribute`, `max_per_attribute` |

## CharacterEntry

```yaml
characters:
  - id: "zahna-003"              # Must match id in the referenced .fof file
    player_name: "Zahna"         # Real player name for display
    file: "characters/zahna.fof" # Path relative to campaign.fof
    joined_session: 1            # Session number when this character joined
    active: true                 # false = character retired/dead
```

## SessionEntry

```yaml
sessions:
  - id: "session-001"                          # Must match id in the session .fof file
    session_number: 1
    date: "2026-03-03"
    file: "sessions/session-001.fof"           # Path relative to campaign.fof
    summary: "The party met the informant."    # One-line summary for the index
```

## Conventional Directory Layout

```
the-shattered-crown/
├── campaign.fof          ← This file
├── characters/
│   ├── zahna.fof
│   └── miro.fof
└── sessions/
    ├── session-001.fof
    └── session-002.fof
```

The tool discovers characters and sessions from the paths declared in `characters[].file` and `sessions[].file`. There is no required filename convention — the paths are explicit.

## Character Lifecycle

1. **Enrollment** — add a `CharacterEntry` to `characters[]`; set `joined_session` and `active: true`
2. **Session play** — the session file records character snapshots; the character `.fof` is updated at session end
3. **Retirement/death** — set `active: false` in the `CharacterEntry`; the character file is preserved

## Annotated Example

See [../examples/campaign-example.fof](../examples/campaign-example.fof) for a complete annotated campaign file.
