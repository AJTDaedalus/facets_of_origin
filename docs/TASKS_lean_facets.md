# TASKS — Lean Facets v1.0 first pass

Spec: `docs/DESIGN_lean_facets.md` · Data: `software/facets/base/facet.yaml` · Revert pin: tag `pre-lean-facets`

| # | Task | Owner | Status |
|---|---|---|---|
| T0 | Pin, branch, BRIEF/DESIGN, facet.yaml v1 | Integration | done |
| T1 | Schema, registry, loader, tables loading (v1) + tests | SW-core | open |
| T2 | Character model (create preset/custom, HP, slots, level-up, wounds, fatigue, fof) + tests | SW-core | open |
| T3 | Roll engine, avoid, combat.py (attack, enemy attack, defend, damage, morale, mobs), magic.py, toolbox.py + tests | SW-core | open |
| T4 | Enemy model (card, derived stats), encounter danger read, REST routes + tests | SW-core | open |
| T5 | Generators: build_bestiary, build_scene_cards, build_toolbox (new); combat_sim rewrite + pacing test | SW-core | open |
| T6 | Val'loh facet.yaml converted to v1 (additive) | SW-core | open |
| T7 | PHB rewrite (all chapters in DESIGN §5; II.7 deleted) | PHB | open |
| T8 | MM Manual rewrite + MM6 Toolbox + tables.yaml content | MM | open |
| T9 | Bestiary: 18 enemy cards + prose | Bestiary | open |
| T10 | Oraga Night + Val'loh books + pregens + cast .fof | Module | open |
| T11 | WebSocket handlers + SPA rebuild + e2e | APP | open (after T1–T4) |
| T12 | Docs invariants rewritten (INV-3..27), generators run, full suite green | Integration | open |
| T13 | DECISIONS L1–L14, CLAUDE.md/README/memory updates, commit | Integration | open |
