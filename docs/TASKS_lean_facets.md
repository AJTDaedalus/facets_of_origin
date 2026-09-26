# TASKS — Lean Facets v1.0 first pass

Spec: `docs/DESIGN_lean_facets.md` · Data: `software/facets/base/facet.yaml` · Revert pin: tag `pre-lean-facets`

| # | Task | Owner | Status |
|---|---|---|---|
| T0 | Pin, branch, BRIEF/DESIGN, facet.yaml v1 | Integration | done |
| T1 | Schema, registry, loader, tables loading (v1) + tests | SW-core | done |
| T2 | Character model (create preset/custom, HP, slots, level-up, wounds, fatigue, fof) + tests | SW-core | done |
| T3 | Roll engine, avoid, combat.py (attack, enemy attack, defend, damage, morale, mobs), magic.py, toolbox.py + tests | SW-core | done |
| T4 | Enemy model (card, derived stats), encounter danger read, REST routes + tests | SW-core | done |
| T5 | Generators: build_bestiary, build_scene_cards, build_toolbox (new); combat_sim rewrite + pacing test | SW-core | done |
| T6 | Val'loh facet.yaml converted to v1 (additive) | SW-core | done |
| T7 | PHB rewrite (all chapters in DESIGN §5; II.7 deleted) | PHB | done |
| T8 | MM Manual rewrite + MM6 Toolbox + tables.yaml content | MM | done |
| T9 | Bestiary: 18 enemy cards + prose | Bestiary | done |
| T10 | Oraga Night + Val'loh books + pregens + cast .fof | Module | done |
| T11 | WebSocket handlers + SPA rebuild + e2e | APP | done |
| T12 | Docs invariants rewritten (INV-3..27), generators run, full suite green | Integration | done |
| T13 | DECISIONS L1–L14, CLAUDE.md/README/memory updates, commit | Integration | done |
