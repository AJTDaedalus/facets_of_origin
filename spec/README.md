# FOF Format Specification

**FOF** (Facets of Origin Format) is the unified file format for all Facets of Origin documents. Every `.fof` file is valid YAML with a mandatory header block that declares its type, version, and identity.

## Document Types

| Type | Purpose | Status |
|---|---|---|
| `ruleset` | Game rules module — attributes, skills, techniques, resolution mechanics | v0.1 stable |
| `character` | Portable character sheet with full game state | v0.1 stable |
| `campaign` | Multi-session story arc container | v0.1 stable |
| `session` | Atomic play record: snapshots, roll log, chat log | v0.1 stable |
| `adventure` | Pre-written adventure module | v0.1 reserved |

## Quick Start: Write a Ruleset Module in 5 Minutes

Create a file called `my-expansion.fof`:

```yaml
fof_version: "0.1"
type: ruleset
id: "my-expansion"
name: "My Expansion"
version: "0.1.0"
authors: ["your-name"]
description: "Adds sailing skills."

requires:
  - id: "base"
    version: ">=0.1.0"

incompatible_with: []

scope:
  applies_to: all
  tags: [expansion, community]

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

Drop it in your campaign directory alongside `campaign.fof`. The tool picks it up automatically.

## Slug Rules

IDs follow `^[a-z][a-z0-9\-_]*$`:
- Lowercase letters, digits, hyphens, underscores
- Must start with a letter
- No spaces

Future: dot-scoped namespacing is reserved — `community.sailing-expansion`.

## Versioning

- `fof_version` — the FOF spec version this file conforms to (e.g. `"0.1"`)
- `version` — the content version of this specific file, in semver (`"1.2.3"`)

Dependency constraints use `>=`, `=`, or `~=` semver operators.

## Specification Index

| Document | Description |
|---|---|
| [FOF-SPEC-v0.1.md](FOF-SPEC-v0.1.md) | Full normative specification |
| [conflict-resolution.md](conflict-resolution.md) | Conflict/scope rules with worked examples |
| [types/ruleset.md](types/ruleset.md) | Ruleset field reference and examples |
| [types/character.md](types/character.md) | Character field reference and portability rules |
| [types/campaign.md](types/campaign.md) | Campaign field reference and directory layout |
| [types/session.md](types/session.md) | Session field reference and roll log definitions |
| [types/adventure.md](types/adventure.md) | Adventure type (v0.1 reserved) |

## Examples

| File | Description |
|---|---|
| [examples/base-ruleset.fof](examples/base-ruleset.fof) | The core ruleset in .fof form |
| [examples/character-example.fof](examples/character-example.fof) | Complete annotated character |
| [examples/campaign-example.fof](examples/campaign-example.fof) | Campaign with overrides, character ref, session index |
