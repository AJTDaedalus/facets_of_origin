# DESIGN — The Val'loh Setting Facet

**Date:** 2026-09-08 · **Tier:** Planner · **Brief:** `docs/BRIEF_valloh_facet.md`
**Tasks:** `docs/TASKS_valloh_facet.md` · **Log:** `docs/LOG_valloh_facet.md`
**Branch:** `feat/valloh-facet` off `feat/lineage` (merged) · **Decisions of record:** D17, D18, D19/S2
**Depends on:** `DESIGN_lineage.md` complete and merged. The ten lineages load through `LineageDefinition`
and INV-16; nothing here can be built before that model exists.

---

## 0. Where this sits in the program

Track 1, second. Produces the data and book that `oraga_rewrite`'s pregens load through. Independent of
`fun_second_act`.

## 1. Approach

This is the game's first setting Facet, so it is also the proof that a setting Facet is *only* data plus
book text. The discipline that makes it a proof is the counted-novelty line, and it is written **first**:

> *The core 2d6, Sparks, Conditions, exchanges, advancement, magic, and the three Facets are unchanged.
> Val'loh adds exactly: ten Lineages (two playable in Oraga Night), ten Gift domains, and crystal charges
> as one-use items. It removes nothing and it changes no rule.*

Everything else must agree with that sentence, and a test makes it structural: the counts in `V0` are
machine-checked against the merged data, so the pitch can never drift from the file. `facet.yaml` for
Val'loh carries nothing in `roll_resolution`, `spark`, `advancement`, `magic` rules, or `combat`. If a
task finds itself wanting to write in one of those, it is out of scope and comes back to Planner.

Owner ruling D17 removed the tempo rule that an earlier draft proposed for spellforms: magic works
exactly as the core writes it — no per-day limit, no slots, gifts and spellforms both cast freely. `V2`
is therefore short by design and must not restate II.3.

## 2. Planner rulings made here

1. **Book text lives at `settings/valloh/`**, data at `software/facets/valloh/`. The brief allowed either;
   book text and code have never shared a directory in this repo and should not start.
2. **Oraga Night's Chapter VIII is deleted in this workstream**, not in `oraga_rewrite`, together with
   the minimum corrections that stop the module contradicting itself in the interval: the "there are no
   magic domains in Val'loh", "nobody casts in a crisis", and "gifts are flair" lines in `02` and `03`.
   Everything else about the module waits for `oraga_rewrite`. Rationale: the repo is never left asserting
   retired canon, and the module's real surgery still happens in one place.
3. **Crystals ship as data.** The brief offered a fallback of free text in `inventory` if the item
   collection reads as complexity. It does not: `Character.inventory` is already `list[str]`, so an item
   id is a valid entry today and the whole system is one merged collection plus a `use_item` path with no
   roll and no arithmetic. If the *table* later finds it heavy, the fallback is still one commit away.
4. **The Bond's reaction clause is simmed before it prints** (brief §9). If a free Intercept at the
   Bond's difficulty reads as a new combat rule rather than a domain intent, the clause is cut and the
   Bond is an ordinary reaction-shaped intent. This is the one place a gift touches combat.

## 3. Module breakdown

### M1 — `software/facets/valloh/facet.yaml`

`id: valloh`, `priority: 1` (official expansion band), `requires: [base]`.

**Ten lineages**, brief §3's table, in `LineageDefinition` format. `playable` is per-Facet: false for
Krenn and Tyndi (MM-side; Krenn exists so Master Vell can be statted honestly and is never shown to
players), false for the six the Facet's own text opens by default but Oraga Night does not — the module
overrides `playable` for its own pregens, which is what a module-local override is for. The Facet's text
says a Val'loh campaign opens all but Krenn and Tyndi.

**Ten gift domains** in `magic.soul_domains`, all Focused, intuitive tradition, `requires_tier3: false`,
and two new flags:
- `lineage_gift: true` — so the II.3 Tier 1 Technique's domain choice list can exclude them. A Soul mage
  in Shattered Origin cannot pick "Crystal". This is the flag that keeps a setting's blood-magic out of
  the core's shopping list, and it is the only schema addition the domain model needs.
- `draft: true` on every example intent until the owner has read them. Every intent in brief §5 is new
  invention; the flag is what says so in the file rather than only in a doc.

**Items.** A new top-level `items` collection merged by id: `{id, name, kind: consumable, scope, effect}`.
Six entries, all Minor, from the module's existing suggested charges: steady light, seal a door, veil of
quiet, chime at a threshold, warmth, held image.

### M2 — Schema and engine

- `ItemDefinition` in `app/facets/schema.py`; `items` merged by id in `MergedRuleset._merge` with an
  `_item_map`, the same loop `backgrounds` and now `lineages` use.
- `lineage_gift` and `draft` on the domain definition; the Tier 1 Technique's domain choice list filters
  `lineage_gift` out, and the lineage formalization path (Lineage M4) filters it *in*.
- `use_item(character, item_id)` in the game layer: removes the entry from `inventory`, emits a narration
  event, rejects a second use of a spent charge. WebSocket event `item_used`. No roll, no arithmetic —
  when the fiction makes a release chancy, the MM calls for Luck at Standard, which is an ordinary roll
  the app already has.

### M3 — The book: `settings/valloh/`

Built to `style/analysis/setting_books.md` §8: pitch in three pages, tone tied to a mechanic, one recent
wound, counted novelty, player-usable material before geography, timeline as a table at the end.

| File | Contents |
|---|---|
| `V0_Ten_Things.md` | Fragment-triplet opener (pink crystal walls; masks for the dead; a sea holding its breath). Tone formula *glamour over a blade*, tied to Sparks. One-page summary. **Ten Things You Need to Know** (brief §6, drafted). First page states: Val'loh is a continent of Shattered Origin's world (S2). Reading order. |
| `V1_Lineages.md` | The ten entries in II.5's four-field format. Krenn is not listed among the tribes a player meets. Ungifted members keep the Heritage and the Background's secondary skill. |
| `V2_Magic_of_Valloh.md` | Gifts as domains (one page); spellcraft as the scholarly tradition (one paragraph — Knowledge + Lore, Mind domains, cast as II.3 writes it, no tempo rule, D17); the crystal charge. Must not restate II.3. |
| `V3_Rekuzan_and_the_Tribes.md` | Gazetteer, short, compressed from Oraga `02`'s public section. Timeline table at the end, including the mist-tides of 3164. |
| `V4_Adaptation.md` | Running Val'loh with core characters — adaptation *within one world*, not conversion between two. What the Facet changes, counted. |

One-line pointer to the crystal charge in `player_handbook/IV.1_Equipment.md`.

### M4 — Invariants

- **INV-7 extended** to the Facet: `V2`'s catalog text and the merged data must match with `valloh`
  loaded, as the appendix and base data already must.
- **INV-16** (from Lineage) passes for all ten gifts.
- **INV-17 (new): the counted-novelty line is machine-checked.** Parse `V0`'s counts and compare against
  the merged ruleset — lineages, `lineage_gift` domains, items. The pitch cannot drift from the file.
- **Merge regression:** without `valloh` loaded, the merged base ruleset is byte-identical to today's.
  This is the guard that proves a setting Facet is additive.

## 4. Testing strategy

TDD; three tests per public function.

- **Merge with `valloh`:** ten lineages, ten more domains, six items, base unchanged.
- **Merge without it:** byte-identical to today (regression guard).
- **`lineage_gift` filtering:** these domains do not appear in Tier 1 Technique choice lists for Soul or
  Mind characters; they do appear for a lineage-gifted character's formalization.
- **Items:** `use_item` removes one charge and emits `item_used`; a second use is rejected; an unknown id
  is rejected.
- **Invariants:** INV-7 extended, INV-16 for all ten, INV-17 new.
- **The Bond:** one simulation run of the reaction clause before `V2` prints it (Planner ruling 4).

## 5. Risks and mitigations

- **A gift becomes a rule.** Only the Bond comes close, and it is gated by a sim.
- **The 5e-era tribe stats** (`/root/wanvil/intermediate/starting_info.md`) are a different era and a
  different system. Use them only to check a gift's flavour against what the owner once wanted at a
  table. Scora's "second try on a failed knowledge check" is now *Dissecting Failure*'s territory and
  stays a Technique, not a gift.
- **Krenn.** Data for Vell and nothing else. `V1` does not list them among the tribes a player meets.
- **Spelling** follows the player-doc rulings: Orthaen, Fthala (Vethala noted), Oraga, the Blackwatch.
- **Every example intent is invention.** `draft: true` in the data and a review table for the owner are
  what make that honest rather than silent.

## 6. Open questions for the owner (non-blocking; the work proceeds with `draft: true`)

1. The ten domains' territories, *beyond-the-focus* lines, and thirty example intents (brief §5).
2. The ten Heritages (brief §3), all new.
3. Fthala's gift rate — canon does not state one; "most" is a draft.
4. Whether the Bond's reaction clause survives its sim.
