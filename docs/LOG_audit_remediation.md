# LOG — Completeness Audit Remediation

**Tier:** Worker (Sonnet) execution log
**Design:** `docs/DESIGN_audit_remediation.md` · **Tasks:** `docs/TASKS_audit_remediation.md`

---

## W0 — Land the plan

- **Branch:** `docs/audit-remediation-plan`
- **Date:** 2026-07-31
- **W0-1** — Committed the nine audit/plan docs (BRIEF, DESIGN, TASKS, RESEARCH_completeness_audit, RESEARCH_audit_phb_creation/_phb_rules/_phb_apparatus/_mm_manual/_software_sync).
  `pytest --collect-only -q` → 1026 tests collected (unchanged from baseline).
  PR #13 opened and merged into `main`.

---

## W1 — Mechanical corrections

- **Branch:** `fix/audit-wave1-corrections`
- **Date:** 2026-07-31
- **Baseline:** `pytest --collect-only -q` → **1026 tests collected**, measured on this branch after merging W0.

### W1 task list (from `docs/TASKS_audit_remediation.md`)

- [ ] W1-1 — Create the LOG and record the baseline. *(this entry)*
- [ ] W1-2 — II.2 point-buy arithmetic and the Scholar's Luck. *(cre-H1, cre-M1)*
- [ ] W1-3 — "Each Facet's tree" → "the Mind and Soul trees"; drop the phantom Techniques. *(cre-H2, cre-H3, cre-M4 — D1)*
- [ ] W1-4 — Soul Second Domain prerequisite line. *(cre-M2)*
- [ ] W1-5 — Zulnut's Finesse and the Knowledge/Lore slip. *(cre-M5)*
- [ ] W1-6 — Threat Clock vignette and pacing math. *(rul-M4, rul-M5)*
- [ ] W1-7 — Four small text corrections across III.3, IV.1, Quick Start, MM5. *(rul-L1, rul-L2, rul-L3, rul-L6, mm-M1)*
- [ ] W1-8 — Glossary: add Saving Throw, fix citations, close the term gaps. *(app-M5, app-L1, app-L2/cre-L4, app-L3, app-L4)*
- [ ] W1-9 — Index slugger: one hyphen per whitespace character. *(app-M6)* **TDD**
- [ ] W1-10 — Apparatus low-severity sweep. *(cre-L1, cre-L2, cre-L3, cre-L5, cre-L6, app-L6)*
- [ ] W1-11 — README: regenerate every factual claim from canon. *(README audit — D2 for the TR value)*
- [ ] W1-12 — Wave 1 close-out.

### W1-1

Command: `cd software && python -m pytest --collect-only -q`
Result: **1026 tests collected**, 0 errors.
Accept criteria met: file exists with the baseline count measured (not copied from W0).
