# Type: ruleset

A `ruleset` file defines game mechanics: attributes, skills, techniques, and resolution rules. Multiple ruleset modules are merged at load time according to the conflict resolution rules. The base module (`id: "base"`, `priority: 0`) always loads first.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `fof_version` | string | FOF spec version |
| `type` | `"ruleset"` | Type discriminator |
| `id` | slug | Unique module ID, `^[a-z][a-z0-9\-_]*$` |
| `name` | string | Display name |
| `version` | semver | Content version of this module |
| `authors` | list[string] | Author names |
| `priority` | int | Load order (0 = base, 1–9 = official expansions, 10–99 = community, 100 = campaign) |

## Optional Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `description` | string | `""` | What this module does |
| `requires` | list[ModuleRef] | `[]` | Declared dependencies |
| `incompatible_with` | list[slug] | `[]` | Module IDs that cannot coexist |
| `scope` | ScopeDef | (see below) | Where this module applies |
| `merge_hints` | MergeHintsDef | (see below) | Author's intent for merge behaviour |
| `changelog` | list[ChangelogEntry] | `[]` | Structured change history |
| `attributes` | AttributesDef | `{}` | Attribute definitions |
| `attribute_distribution` | DistributionDef | `null` | Point allocation rules |
| `character_facets` | list[FacetDef] | `[]` | Character archetype definitions |
| `skills` | list[SkillDef] | `[]` | Skill definitions |
| `techniques` | TechniquesDef | `{}` | Technique trees by facet |
| `roll_resolution` | RollResolutionDef | `null` | Dice resolution rules |
| `spark` | SparkDef | `null` | Spark economy rules |
| `advancement` | AdvancementDef | `null` | Character progression rules |

## ModuleRef

```yaml
requires:
  - id: "base"
    version: ">=0.1.0"    # Supported operators: >=, =, ~=
```

`~=` means "compatible release" — same major and minor, any patch.

## ScopeDef

Declares where this module's contributions apply. Used by the tool to filter module lists and validate character imports.

```yaml
scope:
  applies_to: all              # all | campaign | session | character
  facet_filter: []             # Only applies to characters with one of these primary_facets
  session_types: [campaign, one-shot]
  min_players: 1
  max_players: 8
  tags: [expansion, magic, official]
```

All fields are optional. Defaults: `applies_to: all`, empty filters (no restriction).

## MergeHintsDef

Documents the author's intent for each section. Does not override the spec's merge rules but surfaces warnings when intent conflicts with what another module does.

```yaml
merge_hints:
  attributes: extend           # "extend" = merge by id; later wins on collision
  character_facets: extend
  skills: extend
  techniques: extend
  roll_resolution: override    # "override" = this module owns this singleton
  spark: override
  advancement: override
  attribute_distribution: override
```

Valid values: `extend` | `override`. A module that sets a singleton to `override` but another loaded module also sets it triggers a warning naming both modules.

## ChangelogEntry

```yaml
changelog:
  - version: "0.1.0"
    date: "2026-03-03"         # ISO 8601 date
    notes: "Initial release."
```

## Content Sections

### attributes

```yaml
attributes:
  major:
    - id: body
      name: Body
      description: "..."
      minor_attributes: [strength, dexterity, constitution]
  minor:
    - id: strength
      name: Strength
      description: "..."
      major: body
  ratings:
    - rating: 1
      label: Weak
      modifier: -1
```

**Merge type:** collection. Major, minor, and ratings are each merged by their key (`id` or `rating`). Later module's definition replaces earlier on collision.

### attribute_distribution

```yaml
attribute_distribution:
  total_points: 18
  min_per_attribute: 1
  max_per_attribute: 3
```

**Merge type:** singleton. Only one active definition. Highest-priority non-null wins. Warning emitted if two non-null definitions are loaded.

### character_facets

```yaml
character_facets:
  - id: body
    name: "Facet of the Body"
    description: "..."
    major_attribute: body
```

**Merge type:** collection, keyed by `id`.

### skills

```yaml
skills:
  - id: athletics
    name: Athletics
    facet: body
    attribute: strength
    description: "..."
    status: active    # active | stub | removed
```

`status: removed` is the **denial mechanism** — it suppresses a definition from a lower-priority module. The tool hides removed skills from UI and excludes them from character validation.

**Merge type:** collection, keyed by `id`. Full replacement on collision.

### techniques

```yaml
techniques:
  body:                          # Facet ID
    branches:
      - id: might                # Branch ID
        name: Might
        attribute: strength
        tiers:
          - tier: 1
            techniques:
              - id: forcing_hand
                name: "Forcing Hand"
                description: "..."
                prerequisites: []
```

**Merge type:** collection, keyed by `facet_id → branch_id → tier → technique_id`.

### roll_resolution

```yaml
roll_resolution:
  dice: "2d6"
  modifier_source: minor_attribute
  thresholds:
    full_success: 10
    partial_success: 7
  outcomes:
    full_success:
      label: "Full Success"
      description: "..."
    partial_success:
      label: "Success with Cost"
      description: "..."
    failure:
      label: "Things Go Wrong"
      description: "..."
  difficulty_modifiers:
    - label: Easy
      modifier: 1
      description: "..."
```

**Merge type:** singleton.

### spark

```yaml
spark:
  base_sparks_per_session: 3
  mechanic:
    spend: per_spark_add_d6_drop_lowest
    description: "..."
  earn_methods:
    - id: mm_award
      label: "MM Award"
      description: "..."
```

**Merge type:** singleton.

### advancement

```yaml
advancement:
  skill_ranks:
    - id: novice
      label: Novice
      modifier: 0
      default: true
  skill_point_costs:
    - context: primary_facet_success
      cost: 1
  session_skill_points: 4
  marks_per_rank: 3
  facet_level_threshold: 6
```

**Merge type:** singleton.

---

## Minimal Module Example

A module that only adds skills (no singletons, no attributes):

```yaml
fof_version: "0.1"
type: ruleset
id: "sailing-skills"
name: "Sailing Skills"
version: "0.1.0"
authors: ["seafarer"]
priority: 10

requires:
  - id: "base"
    version: ">=0.1.0"

merge_hints:
  skills: extend

changelog:
  - version: "0.1.0"
    date: "2026-03-03"
    notes: "Initial release."

skills:
  - id: sailing
    name: Sailing
    facet: body
    attribute: dexterity
    description: "Handling a vessel in any weather."
    status: active
```

## Complete Annotated Example

See [../examples/base-ruleset.fof](../examples/base-ruleset.fof) — the full core ruleset in `.fof` form.
