# Type: character

A `character` file is a portable, self-contained snapshot of a player character's complete game state. It can be moved between campaigns, shared between players, and loaded by any compliant tool.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `fof_version` | string | FOF spec version |
| `type` | `"character"` | Type discriminator |
| `id` | slug | Unique ID, `^[a-z][a-z0-9\-_]*$` |
| `name` | string | Display name for this file |
| `version` | semver | Content version; increment after each advancement |
| `authors` | list[string] | Player name(s) |
| `ruleset.modules` | list[ModuleRef] | Ruleset modules this character was created under |
| `character` | CharacterData | The actual character data (see below) |
| `created_at` | ISO 8601 datetime | Creation timestamp |
| `last_modified` | ISO 8601 datetime | Last save timestamp |

## Optional Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `description` | string | `""` | Notes about this character file |
| `campaign_id` | slug \| null | `null` | Campaign this character belongs to; null if standalone |
| `session_count` | int | `0` | Sessions played with this character |

## CharacterData Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Character's in-fiction name |
| `player_name` | string | Real name of the player |
| `primary_facet` | slug | Must reference a valid `id` in `character_facets` |
| `attributes` | map[slug → int] | All minor attribute ratings; must cover every minor attribute in the ruleset |
| `skills` | map[slug → SkillState] | Skills with non-default state; absent skills are implicitly `{ rank: novice, marks: 0 }` |
| `sparks` | int | Current Spark count |
| `session_skill_points_remaining` | int | Skill points remaining this session |
| `facet_level` | int | Current Facet Level (starts at 0) |
| `rank_advances_this_facet_level` | int | Rank advances taken at current Facet Level |
| `techniques` | list[slug] | IDs of all unlocked techniques |

## SkillState Fields

| Field | Type | Description |
|---|---|---|
| `rank` | `novice` \| `practiced` \| `expert` | Skill rank |
| `marks` | int | Progress marks toward next rank |

## Ruleset Binding

The `ruleset.modules` list records which modules were active when this character was created or last advanced. The tool uses this for:

1. **Validation on load** — verifying that all attribute IDs, skill IDs, facet IDs, and technique IDs in the character data exist in the referenced modules
2. **Compatibility checking on import** — when importing a character into a campaign, verifying the campaign's merged ruleset covers all referenced IDs

### ModuleRef Format

```yaml
ruleset:
  modules:
    - id: "base"
      version: "0.1.0"          # Exact version this character was built against
    - id: "sailing-expansion"
      version: "1.2.0"
```

## Portability Rules

A character `.fof` may be moved to a different campaign if:

1. The target campaign loads a **compatible** merged ruleset
2. Compatibility = every attribute ID, skill ID, facet ID, and technique ID referenced in `character.attributes`, `character.skills`, `character.primary_facet`, and `character.techniques` exists in the target campaign's merged ruleset

The tool validates on import and reports mismatches as errors. Mismatches are not auto-resolved — the player must reconcile them manually (e.g., by removing techniques that belong to a missing expansion module).

## Version Lifecycle

| Event | Action |
|---|---|
| Character created | `version: "1.0.0"`, `created_at` set |
| Session played, no advancement | `last_modified` updated, `session_count` incremented |
| Skill rank increased | `version` patch incremented (1.0.0 → 1.0.1), `last_modified` updated |
| Facet Level gained | `version` minor incremented (1.0.1 → 1.1.0) |
| Major campaign milestone | `version` minor incremented at author's discretion |

## Annotated Example

See [../examples/character-example.fof](../examples/character-example.fof) for a complete annotated character file.
