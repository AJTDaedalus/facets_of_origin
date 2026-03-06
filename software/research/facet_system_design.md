# Facet Loading System Design

*Design document — Facets of Origin software implementation. 2026-03-03.*

---

## The Goal

The ruleset is not compiled into the app. It lives in declarative data files — **Facet files** — that the app loads and validates at session start. The base game is one Facet file. Optional modules are additional Facet files. The MM can swap them, stack them, or replace the base entirely.

This mirrors the design philosophy of the PHB itself: "Facets" as modular, optional, stackable layers of the game.

---

## Design Principles

1. **Data over code.** Mechanics are declared in YAML; the engine interprets them. Adding a new skill or technique should never require editing Python.
2. **Schema-validated.** Every Facet file is parsed against a strict Pydantic schema. Invalid files are rejected with a clear error message, not a runtime crash.
3. **Composable.** Multiple Facet files can be active at once. Later-loaded Facets can extend, override, or add to earlier ones.
4. **The base is just a Facet.** There is no "hardcoded" ruleset. The base game is `facets/base/facet.yaml`. If you want a different base game, replace that file.
5. **Fail loudly at load time.** A Facet file with a reference to an undefined attribute fails immediately, before any player connects. Never fail silently mid-session.

---

## Facet File Format

Facet files are YAML documents. The canonical schema is defined in `app/facets/schema.py`.

### Top-Level Structure

```yaml
# Required metadata
id: "base"                          # unique identifier, slug format
name: "Facets of Origin — Core"
version: "0.1.0"
authors: ["AJTDaedalus"]
description: "The core ruleset."
priority: 0                         # lower = loaded first; later Facets can override

# Rule sections (all optional — a Facet only needs to define what it changes)
attributes: { ... }
facets: [ ... ]
skills: [ ... ]
techniques: { ... }
roll_resolution: { ... }
spark: { ... }
advancement: { ... }
```

### Attributes Section

```yaml
attributes:
  major:
    - id: body
      name: Body
      description: "Physical presence: strength, speed, endurance."
      minor_attributes: [strength, dexterity, constitution]
    - id: mind
      name: Mind
      description: "Cognitive power: reasoning, instincts, knowledge."
      minor_attributes: [intelligence, wisdom, knowledge]
    - id: soul
      name: Soul
      description: "Inner self: will, presence, fate."
      minor_attributes: [spirit, luck, charisma]

  minor:
    - id: strength
      name: Strength
      description: "Raw physical force."
      major: body
    # ... etc.

  ratings:
    - rating: 1
      label: Weak
      modifier: -1
    - rating: 2
      label: Average
      modifier: 0
    - rating: 3
      label: Strong
      modifier: 1

  distribution:
    total_points: 18        # Total minor attribute points at character creation
    min_per_attribute: 1    # No attribute can be 0
    max_per_attribute: 3    # No attribute can exceed 3
```

### Facets Section (Character Archetypes)

Note: the word "facet" is overloaded. A *Facet file* is a ruleset module. A *character Facet* is an archetype (Body/Mind/Soul). Character Facets are defined inside a Facet file.

```yaml
facets:
  - id: body
    name: "Facet of the Body"
    description: "Warriors, scouts, athletes, brawlers. People who solve problems with their physical presence."
    major_attribute: body

  - id: mind
    name: "Facet of the Mind"
    description: "Scholars, detectives, arcane theorists. People who solve problems by understanding them."
    major_attribute: mind

  - id: soul
    name: "Facet of the Soul"
    description: "Diplomats, spiritual practitioners, luck-touched wanderers. People who solve problems by moving others."
    major_attribute: soul
```

### Skills Section

```yaml
skills:
  - id: athletics
    name: Athletics
    facet: body
    attribute: strength
    description: "Lifting, climbing, swimming, jumping, forcing things."
    status: active          # active | stub (stub = defined but rules not finalized)

  - id: combat
    name: Combat
    facet: body
    attribute: strength
    description: "Attacking, weapon use, fighting technique."
    status: active

  # Mind and Soul skills: status: stub until those chapters are written
  - id: investigation
    name: Investigation
    facet: mind
    attribute: intelligence
    description: "Searching for clues, examining evidence, finding what's hidden."
    status: stub
```

### Techniques Section

Techniques are organized by character Facet, then branch, then tier.

```yaml
techniques:
  body:
    branches:
      - id: might
        name: Might
        attribute: strength
        tiers:
          - tier: 1
            techniques:
              - id: forcing_hand
                name: "Forcing Hand"
                description: "When you succeed on an Athletics roll using raw force, you may leave a lasting environmental mark the MM cannot undo without explanation."
                prerequisites: []
              - id: weapon_mastery
                name: "Weapon Mastery"
                description: "Choose one weapon type. Rolls using that weapon type are treated as one difficulty step easier."
                prerequisites: []
                has_choice: true
                choice_prompt: "Choose a weapon type: blades, blunt, polearms, or unarmed."
          - tier: 2
            techniques:
              - id: overwhelming_force
                name: "Overwhelming Force"
                description: "When you succeed on a Strength roll against a physical obstacle or opponent, you may impose a lasting penalty on that obstacle or opponent."
                prerequisites: [forcing_hand]
```

### Roll Resolution Section

```yaml
roll_resolution:
  dice: "2d6"
  modifier_source: "minor_attribute"   # what provides the +/- modifier
  thresholds:
    full_success: 10
    partial_success: 7
    # anything below partial_success threshold = failure
  outcomes:
    full_success:
      label: "Full Success"
      description: "You achieve your goal cleanly."
    partial_success:
      label: "Success with Cost"
      description: "You succeed, but with a complication or cost."
    failure:
      label: "Things Go Wrong"
      description: "The story always moves forward, but not in your favor."
  difficulty_modifiers:
    - label: Easy
      modifier: 1
      description: "Clear advantage, weak or inattentive opposition."
    - label: Standard
      modifier: 0
      description: "The default — uncertain outcome, no special advantage or impediment."
    - label: Hard
      modifier: -1
      description: "Skilled opposition, poor conditions, acting against the grain."
    - label: "Very Hard"
      modifier: -2
      description: "Extraordinary opposition, severe circumstances, nearly impossible odds."
```

### Spark Section

```yaml
spark:
  base_sparks_per_session: 3       # starting Sparks at session open
  mechanic:
    spend: "per_spark_add_d6_drop_lowest"
    description: "Each Spark adds a d6 to the roll; drop an equal number of lowest dice."
  earn_methods:
    - id: mm_award
      label: "MM Award"
      description: "MM awards for exceptional roleplay, creative problem-solving, or playing your character's traits and weaknesses in a way that costs you something."
    - id: peer_call
      label: "Spark? — Peer Call"
      description: "Any player calls Spark? for another player's moment. MM confirms."
    - id: graceful_fail
      label: "The Graceful Fail"
      description: "On a 6-, lean into the consequence or add to the fiction. MM may award a Spark."
```

### Advancement Section

```yaml
advancement:
  skill_ranks:
    - id: novice
      label: Novice
      modifier: 0
      default: true
    - id: practiced
      label: Practiced
      modifier: 1
    - id: expert
      label: Expert
      modifier: 2

  skill_point_costs:
    - context: "primary_facet_success"
      cost: 1
    - context: "primary_facet_failure"
      cost: 2
    - context: "secondary_facet_success"
      cost: 2
    - context: "secondary_facet_failure"
      cost: 4

  session_skill_points: 4
  marks_per_rank: 3
  facet_level_threshold: 6        # skill rank advances per facet level
```

---

## Composition and Override Rules

When multiple Facet files are active, they are merged in priority order (lowest `priority` value first, then ascending):

| Operation | Rule |
|---|---|
| New skill added by later Facet | Appended to skill list |
| Skill ID collision | Later Facet wins; earlier Facet's version is overridden |
| New technique added | Appended to tree |
| Roll resolution overridden | Later Facet's thresholds completely replace earlier |
| New attribute added | Appended; must reference a valid major attribute |

**Example:** A "Magic" Facet module adds 3 new skills (Arcana, Ritual, Attunement), a new character Facet (Facet of the Arcane), and a new technique tree. It does not touch the base game's resolution system. Both Facet files are active; the registry merges them.

---

## File Discovery and Loading

At session start, the registry scans `facets/` for `.yaml` files:

```
facets/
├── base/
│   └── facet.yaml          # Priority 0 — always loaded
├── magic/
│   └── facet.yaml          # Priority 10 — loaded if active for this session
└── technology/
    └── facet.yaml          # Priority 10 — loaded if active for this session
```

The MM selects which non-base Facets are active when creating a session. The registry:
1. Loads `base/facet.yaml` unconditionally
2. Loads each selected Facet file in priority order
3. Validates cross-references (a skill referencing an undefined attribute fails loudly)
4. Builds the merged ruleset in memory
5. Caches the result for the session lifetime

The merged ruleset is a single Python object (validated Pydantic model) that the game engine, character validator, and API all read from. It never changes mid-session.

---

## Future Considerations

- **Online Facet registry**: A central repo where MMs can download community Facet files (homebrew settings, rule variants). The app fetches, validates, and caches them locally. Trust model: Facet files are data, not code — they cannot execute arbitrary Python.
- **Facet versioning**: Pin a Facet version to a campaign so a module update doesn't break an in-progress game.
- **Per-session overrides**: Allow the MM to patch single values (e.g., change `session_skill_points` from 4 to 6 for a long session) without editing the Facet file.
