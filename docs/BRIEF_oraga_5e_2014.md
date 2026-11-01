# BRIEF: Oraga Night 5e edition: full 2014 conversion, four-player baseline

Status: decisions taken 2026-10-31; no module text changed yet.

## Owner decisions (2026-10-31)
1. **Scope: full 2014 conversion** of `conversions/dnd5e/oraga_night/` covering stat blocks, pregens, rules terms and the licence (SRD 5.2.1 → SRD 5.1). The Facets edition is untouched because it has no party-size baseline.
2. **Baseline: four 4th-level characters.** Today's printed rosters become the "Three characters" line. The five-character and 3rd/5th-level lines are recomputed.
3. **Yardstick:** size groups with Xanathar's multiple-monster ratios (internal use only, never printed) and cross-check with the 2014 DMG adjusted XP. The book prints DMG-style numbers only.

## Constraints
- Copyright: the book may use **SRD 5.1 (CC BY 4.0)** content only. SRD 5.1 has the standard human only, one subclass per class, one background (Acolyte) and one feat (Grappler). Variant human, other feats, Xanathar's and Tasha's are not open, so the book may name them but not reproduce their text. The SRD 5.1 attribution text is in its legal page.
- Pregen rule conflict to resolve: chapter XI's 2014 note uses the variant human's feat for the gift, which is not in SRD 5.1. Chapter III instead grants the gift as a bonus feat at 1st level. This needs an owner ruling.
- Tooling: lint_5e, fact_check, pregen_check, bestiary_check, copyright_scan and 668 module tests encode 2024 terms. Expect broad test churn.
- Work on a new local branch. Commit per package on the owner's word. No push.

## In progress when the session stopped
- Inventory research → `docs/RESEARCH_oraga_5e_2014_inventory.md` (agent stopped; the file may be partial or absent).
- Encounter extraction with 2014 math → `docs/RESEARCH_oraga_5e_2014_encounters.md` (agent stopped; the file may be partial or absent).
- SRD 5.1 text extracted to the session scratchpad (re-download from https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf).

## Next
1. Finish both research files.
2. Write `DESIGN_oraga_5e_2014.md` and `TASKS_oraga_5e_2014.md`: package order (stat blocks → cards and budgets → pregens → terms and notes → licence → tooling and tests).
3. Get owner rulings on the open questions above, then execute package by package.
