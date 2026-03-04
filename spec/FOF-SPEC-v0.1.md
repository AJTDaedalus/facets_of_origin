# FOF Format Specification v0.1

**Status:** Active — normative
**Date:** 2026-03-03
**Maintained by:** AJTDaedalus

This document is the single authoritative reference for the Facets of Origin Format (FOF) v0.1. All other documents in `spec/` are derived from or supplementary to this document. In case of contradiction, this document takes precedence.

---

## 1. Overview

FOF is a YAML-based file format for Facets of Origin documents. Every `.fof` file:

- Is valid YAML
- Begins with a standard envelope block
- Declares its `type`, which determines required and optional additional fields
- Uses slug IDs that match `^[a-z][a-z0-9\-_]*$`
- Uses semver for content versioning

The format is designed to be human-writable, diffable, and portable. Files may be kept alongside campaign materials or shared between players and groups.

---

## 2. The FOF Envelope

Every `.fof` file begins with this header block. These fields are required for all types.

```yaml
fof_version: "0.1"
type: ruleset
id: "base"
name: "Facets of Origin — Core Ruleset"
version: "0.1.0"
authors: ["AJTDaedalus"]
description: ""
```

### 2.1 Envelope Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `fof_version` | string | Yes | FOF spec version this file conforms to |
| `type` | TypeEnum | Yes | Document type (see §3) |
| `id` | slug | Yes | Unique identifier for this document |
| `name` | string | Yes | Human-readable display name |
| `version` | semver | Yes | Content version of this file |
| `authors` | list[string] | Yes | Author or creator names |
| `description` | string | No | Free-text description; defaults to `""` |

### 2.2 Slug Format

IDs must match: `^[a-z][a-z0-9\-_]*$`

- Lowercase ASCII letters, digits, hyphens, underscores
- Must start with a letter
- No spaces, no uppercase

**Reserved:** dot-notation (`community.module-name`) is reserved for future namespacing. Do not use dots in v0.1 IDs.

### 2.3 Semver

`version` fields follow Semantic Versioning (`MAJOR.MINOR.PATCH`):
- MAJOR: breaking changes
- MINOR: new features, backwards-compatible
- PATCH: bug fixes, corrections

Dependency constraints use:
- `>=1.0.0` — at least this version
- `=1.0.0` — exactly this version
- `~=1.0.0` — compatible release (same major and minor, any patch)

---

## 3. Document Types

| Type | Description | Status |
|---|---|---|
| `ruleset` | Game rules module | v0.1 stable |
| `character` | Portable character sheet | v0.1 stable |
| `campaign` | Multi-session story arc | v0.1 stable |
| `session` | Atomic play record | v0.1 stable |
| `adventure` | Pre-written adventure module | v0.1 reserved |

---

## 4. Type: ruleset

See [types/ruleset.md](types/ruleset.md) for the full field reference.

### 4.1 Priority System

Modules are loaded in priority order. Lower number = lower authority.

| Priority | Owner |
|---|---|
| 0 | `base` — always loads first |
| 1–9 | Official expansions |
| 10–99 | Community modules |
| 100 | Campaign overrides (always win) |

### 4.2 Additional Required Fields for ruleset

Beyond the envelope: `priority` (int).

### 4.3 Merge Semantics

**Singleton sections** — only one active definition allowed. Highest-priority non-null wins. Warning if two modules both define one.

- `roll_resolution`
- `spark`
- `advancement`
- `attribute_distribution`

**Collection sections** — merged by key. Later-loaded module's entry replaces earlier on key collision.

- `attributes.major[]` → keyed by `id`
- `attributes.minor[]` → keyed by `id`
- `attributes.ratings[]` → keyed by `rating` (int)
- `character_facets[]` → keyed by `id`
- `skills[]` → keyed by `id`
- `techniques[facet_id][branch_id][tier][technique_id]`

**Denial** — a skill entry with `status: removed` suppresses definitions from lower-priority modules. Warning emitted.

---

## 5. Type: character

See [types/character.md](types/character.md) for the full field reference.

### 5.1 Additional Required Fields for character

Beyond the envelope: `ruleset.modules` (list[ModuleRef]), `character` (CharacterData), `created_at` (datetime), `last_modified` (datetime).

### 5.2 Portability

A character may be moved between campaigns if all IDs it references exist in the target campaign's merged ruleset. The tool validates on import.

---

## 6. Type: campaign

See [types/campaign.md](types/campaign.md) for the full field reference.

### 6.1 Additional Required Fields for campaign

Beyond the envelope: `modules` (list[ModuleRef]), `started_at` (date), `status` (StatusEnum).

### 6.2 Campaign Overrides

The `overrides` block applies singleton values at priority 100. Only singleton fields may appear in `overrides`. The tool emits an info message for each override applied.

---

## 7. Type: session

See [types/session.md](types/session.md) for the full field reference.

### 7.1 Additional Required Fields for session

Beyond the envelope: `campaign_id` (slug), `session_number` (int), `date` (date).

### 7.2 Immutability

Session files are play records. Once written, they should not be edited. The tool may add a `sealed: true` marker in a future version to enforce this.

---

## 8. Type: adventure

See [types/adventure.md](types/adventure.md). Full schema deferred to FOF v0.2. v0.1 accepts files with `type: adventure` but validates only the envelope.

---

## 9. Validation Layers

Validation proceeds in three layers. Earlier layer failures abort later layers.

### Layer 1 — Envelope

1. `fof_version` is a known spec version
2. `type` is a valid TypeEnum value
3. `id` matches `^[a-z][a-z0-9\-_]*$`
4. `version` is valid semver (`MAJOR.MINOR.PATCH`)
5. `name` is a non-empty string
6. `authors` is a non-empty list

### Layer 2 — Type Schema

1. All required fields for the declared type are present
2. Field types match their declared types
3. Unknown top-level fields: warn in lenient mode, error in strict mode
4. Internal cross-references valid (e.g., `skill.facet` must exist in `character_facets[]`)

Cross-references validated for `ruleset` type:
- `skills[].facet` → exists in `character_facets[].id`
- `skills[].attribute` → exists in `attributes.minor[].id`
- `techniques[facet_id]` → `facet_id` exists in `character_facets[].id`
- `techniques[facet_id][branch_id].attribute` → exists in `attributes.minor[].id`
- `techniques[facet_id][branch_id][tier][technique].prerequisites[]` → each ID exists in same branch (same or earlier tier)

Cross-references validated for `character` type:
- `character.primary_facet` → exists in merged `character_facets[].id`
- `character.attributes` keys → each exists in merged `attributes.minor[].id`
- `character.skills` keys → each exists in merged `skills[].id` (and not `status: removed`)
- `character.techniques[]` → each exists in merged techniques

### Layer 3 — Merge (ruleset type only)

1. All `requires` constraints satisfied
2. No `incompatible_with` modules present
3. No circular dependencies in `requires` graph
4. Singleton conflicts detected; warnings emitted with module names

---

## 10. Reserved Fields

The following top-level keys are reserved for future FOF versions and must not be used in v0.1 module content:

- `schema` — future: JSON Schema reference
- `sealed` — future: session immutability marker
- `signature` — future: cryptographic author signature
- `assets` — future: embedded binary asset references
- `locale` — future: localisation metadata

---

## 11. Extension Policy

Third-party tools may add custom fields using the `x_` prefix:

```yaml
x_my_tool_export_format: "json"
x_my_tool_last_synced: "2026-03-03T20:00:00Z"
```

Tools implementing FOF must ignore unknown `x_` fields. Tools must not add `x_` fields to files they did not create unless the user has explicitly configured the tool to do so.

Extension namespacing: `x_{vendor}_{field}` is recommended to avoid collisions.

---

## 12. Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1 | 2026-03-03 | Initial release. Defines envelope, ruleset, character, campaign, session, and adventure (stub) types. |
