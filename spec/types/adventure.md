# Type: adventure

**Status: Reserved — full schema deferred to FOF v0.2**

The `adventure` type is reserved in FOF v0.1. Files with `type: adventure` are accepted by the parser but no additional fields beyond the envelope are required or validated.

## v0.1 Stub Format

```yaml
fof_version: "0.1"
type: adventure
id: "the-midnight-vault"
name: "The Midnight Vault"
version: "0.1.0"
authors: ["AJTDaedalus"]
description: "A heist adventure for 3–4 players, one session."
# Full schema deferred to FOF v0.2
```

## What v0.2 Will Define

The v0.2 adventure schema is expected to include:

- **Scene graph** — a directed graph of scenes with connections, triggers, and branching conditions
- **NPC roster** — named characters with traits, motivations, and stat blocks for any required rolls
- **Handouts** — player-facing text documents (maps, letters, inscriptions) embedded or referenced
- **MM guidance** — tone notes, pacing suggestions, scene-specific advice
- **Encounter seeds** — optional structured conflicts with recommended difficulty ratings
- **Reward table** — techniques, sparks, or advancement milestones unlocked by scene completion
- **Tags** — system tags for length (`one-shot`, `multi-session`), tone, setting, and player count

## Stub Compatibility

v0.1 stubs are forward-compatible. When v0.2 is released, a migration tool will validate and fill required fields. The `id`, `name`, `version`, and `description` fields written in v0.1 stubs are preserved.

## Relationship to Campaign

Adventures are playable standalone or embedded within a campaign. When embedded:
- The campaign references the adventure file in a `modules` or `adventures` list (v0.2 field)
- The adventure's scene graph is available to the tool for navigation
- Session files reference the adventure's scene IDs in the roll log (v0.2 field)
