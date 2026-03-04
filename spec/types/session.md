# Type: session

A `session` file is the atomic play-record unit. It captures character state at session start (as embedded snapshots), a roll log, a chat log, MM-only notes, and end-of-session character deltas. Sessions are immutable records — they are written during or after play and not modified afterward.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `fof_version` | string | FOF spec version |
| `type` | `"session"` | Type discriminator |
| `id` | slug | Unique ID, `^[a-z][a-z0-9\-_]*$` |
| `campaign_id` | slug | ID of the parent campaign |
| `session_number` | int | Sequential session number within the campaign |
| `date` | ISO 8601 date | Date the session was played |

## Optional Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | string | `""` | Display name for this file |
| `version` | semver | `"1.0.0"` | File version |
| `authors` | list[string] | `[]` | GM/recorder names |
| `duration_minutes` | int | `null` | Actual play time |
| `character_snapshots` | list[CharacterSnapshot] | `[]` | Character state at session START |
| `rolls` | list[RollEntry] | `[]` | Full roll log |
| `chat` | list[ChatEntry] | `[]` | Full chat log |
| `mm_notes` | string | `""` | MM-only notes (not exposed to players) |
| `character_end_states` | list[EndState] | `[]` | Per-character advancement deltas |

## Character Snapshots

Snapshots embed character state at session **start** — not referenced, embedded. This ensures the session is a complete, self-contained record even if the character file is later updated.

```yaml
character_snapshots:
  - player_name: "Zahna"
    character_id: "zahna-003"
    snapshot:
      name: "Zahna"
      primary_facet: "mind"
      attributes:
        strength: 1
        dexterity: 2
        constitution: 2
        intelligence: 3
        wisdom: 3
        knowledge: 2
        spirit: 1
        luck: 2
        charisma: 2
      skills:
        athletics:     { rank: novice,    marks: 0 }
        investigation: { rank: novice,    marks: 0 }
      sparks: 3
      facet_level: 0
      rank_advances_this_facet_level: 0
      techniques: []
```

**Rationale:** If character files are edited (e.g., retroactive corrections), session records remain accurate. Investigators can always reconstruct what state a character was in during any session.

## Roll Log Fields

Each entry in `rolls` captures the complete mechanical context of a single roll.

| Field | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 datetime | When the roll was made |
| `player_name` | string | Who rolled |
| `attribute_id` | slug | Minor attribute used |
| `attribute_rating` | int | Rating value at time of roll |
| `skill_id` | slug \| null | Skill used, or null for raw attribute rolls |
| `skill_rank_id` | slug \| null | Skill rank at time of roll |
| `difficulty` | string | Difficulty label (`Easy`, `Standard`, `Hard`, `Very Hard`) |
| `sparks_spent` | int | Sparks consumed on this roll |
| `dice_rolled` | list[int] | All dice values rolled (including extra Spark dice) |
| `dice_kept` | list[int] | Dice kept after dropping lowest Spark dice |
| `dice_sum` | int | Sum of kept dice |
| `attribute_modifier` | int | Modifier from attribute rating |
| `skill_modifier` | int | Modifier from skill rank |
| `difficulty_modifier` | int | Modifier from difficulty (negative = harder) |
| `total` | int | `dice_sum + attribute_modifier + skill_modifier + difficulty_modifier` |
| `outcome` | slug | `full_success`, `partial_success`, or `failure` |
| `outcome_label` | string | Human-readable outcome label |
| `description` | string | What the character was attempting |

## Chat Log Fields

| Field | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 datetime | When the message was sent |
| `player_name` | string | Who sent it |
| `text` | string | Message content |

## MM Notes

`mm_notes` is a free-text field for the game master's private notes. The tool must not expose this field to players in any player-facing view.

```yaml
mm_notes: |
  Players found the cipher. Prep vault encounter for next session.
  Zahna's player is clearly planning something with the informant — leave space for it.
```

## End-of-Session Character State

Records advancement that occurred during or after the session. The tool uses this to update the character `.fof` file.

```yaml
character_end_states:
  - player_name: "Zahna"
    character_id: "zahna-003"
    sparks_delta: -1                  # Sparks spent net (can be negative or positive)
    skill_advances:                   # Each rank advance
      - skill_id: "investigation"
        from_rank: "novice"
        to_rank: "practiced"
    facet_level_delta: 0              # Facet Level gains (usually 0 per session)
```
