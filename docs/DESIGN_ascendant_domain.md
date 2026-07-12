# DESIGN — Ascendant Domain engine support (issue #8)

Planner output. Closes the gap where PR #7 added the **Ascendant Domain** Tier 3
Technique to the PHB, Glossary, and `facet.yaml`, but the engine honored none of
its three mechanical clauses.

## The three clauses (PHB II.4b / II.4c)

> Choose one prismatic domain [...] The Broad difficulty table applies — Hard at
> Minor scope, Very Hard at Significant and Major — and its Major-scope ceiling
> cannot be moved by Sparks. **Your original domain is unchanged.**

1. Original domain unchanged.
2. Broad difficulty table applies (Hard / Very Hard / Very Hard).
3. Sparks cannot move the ceiling.

## Root causes

| # | Cause | Site |
|---|---|---|
| 1 | `magic_granting: true` means *"this Technique **sets** `magic_domain`"* — right for Arcane Study, backwards for Ascendant Domain, which must **add**. Selecting it destroys the original domain. | `character.py:339` |
| 2,3 | `facet.yaml`'s `magic:` section has **no domain catalog**, so `get_domain()` returns `None` for every domain and the engine substitutes a synthetic `type="standard"`. A prismatic domain therefore rolls the Standard table, and `push_scope` (rejected only for `type == "broad"`) is wrongly permitted. | `engine.py:196-207`, `engine.py:232-237` |
| — | Latent: the Broad "ceiling" is written as an *assignment*, not a cap. It raises Minor-scope Broad from Hard to Very Hard. Harmless only because no domain has ever resolved to `broad`. Goes live the moment the catalog lands. | `engine.py:252-254` |

## Decisions

**D-A1 — Register the domain catalog in `facet.yaml`, transcribed from canon.**
`MagicDomainDef` and `MagicDef.soul_domains` / `.mind_domains` already exist in
`schema.py`, purpose-built for this and never populated (`requires_tier3` is even
documented as "True for Prismatic domains that need a Tier 3 Technique"). The 21
domains, their types, and their prismatic status are all fully specified in
`player_handbook/Appendix_Magic_Domains.md`; tradition follows from the Facet
(Mind rolls Knowledge → `scholarly`, Soul rolls Spirit → `intuitive`, per
II.4b/II.4c). This is **transcription of existing canon, not invention** — no
new mechanic is introduced, so it needs no Brain ruling.

Guarded by **INV-7**: the appendix and `facet.yaml` must agree on the domain set
and every domain's type. Same spirit as INV-1…INV-6 — the catalog now lives in
two coupled homes, and this is what stops them drifting.

**D-A2 — New field `Character.ascendant_domain`, distinct from `secondary_magic_domain`.**
The one-step-harder penalty is a property of the *acquisition route*, not of the
domain: Second Domain is +1 step, Ascendant Domain is no penalty (the Broad table
is its cost). Reusing `secondary_magic_domain` would leak Second Domain's penalty
onto Ascendant. A field per route is the honest model.

Rejected: a general `domains: list[str]` refactor — it touches persistence, the
API, the web app, and the `.fof` spec, for no gain this PR can use.

**D-A3 — New `TechniqueDef.grants_prismatic_domain`.** The two Ascendant
Techniques set it. `select_technique` routes the choice to `ascendant_domain`
instead of `magic_domain`, so the original survives. `magic_granting` keeps its
existing meaning everywhere else.

**D-A4 — Delete the Broad ceiling assignment.** `_step_difficulty_harder`
already saturates at the top of the ladder (`min(idx + 1, len - 1)`, and Very
Hard *is* the top), and `push_scope` is rejected outright for Broad domains. The
ceiling is therefore already enforced by construction; the assignment enforces
nothing and only corrupts Minor scope. Clause 2 requires Hard at Minor.

**D-A5 — Validate domain choices against the catalog.** Ascendant Domain requires
a prismatic (`broad`) domain of the character's Facet; Second Domain requires a
non-prismatic one ("prismatic territories require Ascendant Domain", II.4c). Now
cheap, because the catalog exists.

**D-A6 — Wire Second Domain's choice into `secondary_magic_domain`.** Companion
fix, same code path: nothing has ever written that field outside `.fof` loading,
so Second Domain's penalty could only fire for a hand-authored character. Same
class of bug as #1, and fixing it is what makes the two routes symmetric.

## Test strategy

Red first, per CLAUDE.md TDD.

- Catalog: every appendix domain resolves via `get_domain` with the right `type`;
  prismatics carry `requires_tier3`.
- Clause 1: Ascendant preserves `magic_domain`, populates `ascendant_domain`.
- Clause 2: Broad rolls Hard / Very Hard / Very Hard by scope.
- Clause 3: `push_scope` raises on a Broad domain.
- Penalty isolation: Second Domain's +1 step applies to `secondary_magic_domain`
  and **not** to `ascendant_domain`.
- Validation: Ascendant rejects a non-prismatic choice; Second Domain rejects a
  prismatic one.
- Persistence: `ascendant_domain` survives a `.fof` round trip.
- INV-7: appendix ↔ `facet.yaml` catalog agreement.
