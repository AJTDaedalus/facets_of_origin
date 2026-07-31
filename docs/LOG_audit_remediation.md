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

- [x] W1-1 — Create the LOG and record the baseline. *(this entry)*
- [x] W1-2 — II.2 point-buy arithmetic and the Scholar's Luck. *(cre-H1, cre-M1)*
- [x] W1-3 — "Each Facet's tree" → "the Mind and Soul trees"; drop the phantom Techniques. *(cre-H2, cre-H3, cre-M4 — D1)*
- [x] W1-4 — Soul Second Domain prerequisite line. *(cre-M2)*
- [x] W1-5 — Zulnut's Finesse and the Knowledge/Lore slip. *(cre-M5)*
- [x] W1-6 — Threat Clock vignette and pacing math. *(rul-M4, rul-M5)*
- [x] W1-7 — Four small text corrections across III.3, IV.1, Quick Start, MM5. *(rul-L1, rul-L2, rul-L3, rul-L6, mm-M1)*
- [x] W1-8 — Glossary: add Saving Throw, fix citations, close the term gaps. *(app-M5, app-L1, app-L2/cre-L4, app-L3, app-L4)*
- [x] W1-9 — Index slugger: one hyphen per whitespace character. *(app-M6)* **TDD**
- [ ] W1-10 — Apparatus low-severity sweep. *(cre-L1, cre-L2, cre-L3, cre-L5, cre-L6, app-L6)*
- [ ] W1-11 — README: regenerate every factual claim from canon. *(README audit — D2 for the TR value)*
- [ ] W1-12 — Wave 1 close-out.

### W1-1

Command: `cd software && python -m pytest --collect-only -q`
Result: **1026 tests collected**, 0 errors.
Accept criteria met: file exists with the baseline count measured (not copied from W0).

### W1-2 *(cre-H1, cre-M1)*

- `II.2:102` — replaced the illegal "four at 3, two at 1, three at 2" example (nets to 20, not 18) with the legal **four at 3, four at 1, one at 2** (4 spent, 4 saved, 1 at baseline = 18). Recomputed the whole sentence, not just the numbers.
- `II.2:121` — the Scholar's stat line was already correct (Luck 2, total 18 ✓); the prose falsely claimed "Strong in Luck" (Strong = 3, Luck is baseline 2). Replaced with "Nothing lucky about them, either — cleverness is the only edge they've got," preserving the sentence's voice without the false claim.
- No other prose in the section touched.
- **Flag for voice review (DESIGN §6):** the `:121` replacement clause is a new sentence, not a pure arithmetic fix — worth a second look for tone.

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-3 *(cre-H2, cre-H3, cre-M4 — D1)*

- `II.3_Magic.md:93` — the two illustrative Techniques ("ease Minor magic one step," "remove unintended collateral") exist in neither the Archive nor Communion trees. Checked `II.4b`/`II.4c` for every Technique that touches magic difficulty — none match. Reworded to cite Techniques that actually exist: Second Domain and Ascendant Domain (both Tier 3), describing what they do (extend reach) instead of inventing an easing effect.
- `II.3_Magic.md:246` — "Ascendant Domain Technique (Tier 3, in each Facet's tree)" → "in the Mind and Soul trees" (D1: no Body-tree magic Techniques exist or are being added).
- `Glossary.md:90` — same "each Facet's tree" → "the Mind and Soul trees" fix. (Citation-format and dual-citation fix deferred to W1-8, out of this task's scope.)
- Regenerated `Index.md` (`python -m tools.build_index`) since Glossary.md was touched (INV-4) — no diff, since no heading text changed.
- Grepped `each Facet's tree` and "Body...Technique...magic" repo-wide: the one remaining hit (`II.3:242`, Body Facet characters cross-training into Mind/Soul magic Techniques) is a correct, unrelated statement — not a Body-tree magic Technique claim.

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-4 *(cre-M2)*

- `II.4c:134` — Soul's **Second Domain** was missing the prerequisite line its Mind twin carries (`II.4b:137`: *"Requires an existing Mind domain (Arcane Study)."*) and that Soul's own Ascendant Domain entry already carries (`II.4c:138`). Added the matching line: *"Requires an existing Soul domain (Spiritual Domain)."*, copying the sibling's exact wording pattern.
- Regenerating `Index.md` was required even though this task touches neither a heading nor Glossary.md — `test_index_is_up_to_date` failed after the content edit alone (two `II.4c — Tier 1` search-index entries dropped from keyword-ranked sections once the surrounding text changed). Noting this for future tasks: **any body-text edit can stale the Index, not just heading/Glossary changes** — regenerate and check the test, don't rely on the wave-rule trigger list alone.

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-5 *(cre-M5)*

- `II.4:59` (Advancing Skills example) — the original showed Finesse advancing Novice→Practiced via marks, but Zulnut's Finesse is Practiced at creation (`characters/Zulnut.fof`). Rebuilt as a **Stealth-only** example per the task instruction: 2 marks earned this session + the 1 Background Mark already on Stealth (II.5:43: "reach Practiced in two marks rather than three") = 3 marks = advance to Practiced (II.4:57's 3-marks-per-rank rule). Added the unspent-points-are-lost beat (II.4:53) using the 2 leftover points.
- `II.4:73` (Facet Levels example) — **judgment call, deviated from the literal "swap to Stealth" instruction.** Stealth already occupies two other slots in this same example (advances 2 and 4: Novice→Practiced→Expert), so reusing it a third time for slot 5 would either duplicate a transition already shown or require Stealth to jump straight to Master mid-example, distorting the rest of the sequence. Since Finesse legitimately starts Practiced, its two real remaining transitions are Practiced→Expert and Expert→Master — so slot (5) became **"Finesse to Expert"** (with an inline note that this is Finesse's first advance, since it started Practiced) and slot (9) became **"Finesse to Master"** (previously "Finesse to Expert," now redundant with the corrected slot 5). This keeps all 5 named skills distinct, keeps the 10-advances-by-Facet-level-2 count intact, and removes the Novice→Practiced claim without touching Stealth's already-correct chain.
- `II.4:116` — "His Knowledge rank ticks to Practiced" → "His Lore rank ticks to Practiced" (Knowledge is a Minor Attribute, not a skill; the skill is Lore, governed by Knowledge — II.6:22). Confirmed against `characters/Zahna.fof`: Lore Practiced.
- `II.4:120` — "A Knowledge advancement is richer..." → "A Lore advancement is richer..." (same fix, MM-guidance paragraph).
- Regenerated `Index.md` — no diff.
- **Flag for voice review (DESIGN §6):** the `:73` fix departs from the task's literal wording ("swap to Stealth") for the reasons above; worth a second look to confirm the Finesse-Expert-then-Master framing reads naturally.

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-6 *(rul-M4, rul-M5)*

- `III.2:96` (The Beam vignette) — the restarted 4-segment clock (reset to 0) was only narrating 3 advances before "fills." Added the missing fourth beat and explicit numbering matching the model vignette's style (`:43-57`, which numbers "the second segment fills," "a partial, three," "a partial, four"): Zahna's scramble (one), Zulnut's (two), a new beat — the stairs buckling underfoot (three) — then the beam settling deeper fills it (four). Did not touch the definition of "restarting" itself, per the task's explicit instruction.
- `III.2:19` — at the stated 72% partial/failure rate, a 4-segment clock takes 4 ÷ 0.72 ≈ 5.6 rolls, not "roughly 3–4." Kept 72% (it's the derived, correct figure) and replaced the roll-count claim with "roughly five or six party rolls."
- Regenerated `Index.md` — no diff (no heading touched).

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-7 *(rul-L1, rul-L2, rul-L3, rul-L6, mm-M1)*

- `III.3:317` — the Named NPC section only mentioned Staggered/Cornered (Tier 2) riders, but the Strike rules (`III.3:124`) and quick ref (`:677`) both allow a Tier 1 **or** Tier 2 rider. Reworded to name both tiers.
- `III.3:287` — trimmed the promise that the Equipment chapter covers armor "Technique interactions"; `IV.1_Equipment.md` has no such section (it covers weapon Techniques at `:27`, not armor ones). Did not author the missing content (Non-goal) — just removed the false promise.
- `Quick_Start.md:123` — the MM's line called another player's "Spark?" peer call (III.1:70) a "graceful failure." Graceful Fail is player-claimed by the roller on their own 6- (III.1:72) — this was a different player recognizing Zulnut's moment, i.e., the peer call, not a Graceful Fail. Reworded to drop the misapplied term.
- `III.3:458` (The Archive's Guardian vignette) — Mordai uses Weapon Mastery, a Technique that requires Facet level 1+, which starting characters don't have. Added a grounding clause to the vignette's opening line: "Several sessions on from where this book's other vignettes leave off — long enough that Mordai has since taken Weapon Mastery," so readers don't infer starting characters have Techniques.
- `MM5:107` — the Maneuver row had the direction and duration backwards: it said the *target's* next roll becomes Easy (one roll only). Canon (`III.3:146`) is that rolls made **against** the target are Easy, **until the situation changes** (not a single-roll effect). Rewrote the row as a compression of the canonical line, fixing both direction and duration; also compressed the 7–9 case ("rolls against the target stay Standard") to match.
- Regenerated `Index.md` — no diff (no heading touched).

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-8 *(app-M5, app-L1, app-L2/cre-L4, app-L3, app-L4)*

- Added **Saving Throw** (compression of III.1:84-99: 2d6 + the relevant Major Attribute modifier, reactive vs. proactive framing), inserted alphabetically between Rider and Scope.
- `:12` Ascendant Domain and `:90` Second Domain — added the missing "Chapter" prefix (matching the other 52 entries' format) and cited **both** homes: `*(Chapters II.4b, II.4c)*`. Note: `_GLOSSARY_ENTRY`'s regex (`software/tests/test_docs_consistency.py:227`) only captures a single trailing token (no comma/space), so a two-chapter citation isn't parsed by `test_glossary_pointers_resolve` — it's silently skipped rather than validated, same as the existing bare-MM-citation entries are skipped by the `Chapter X.Y`-only cross-reference check. Confirmed by hand that both II.4b and II.4c contain each term.
- Added five standalone entries, each a compression of canonical text, alphabetically placed:
  - **Off-Balance** and **Shaken** (Tier 1 Conditions, III.3:235-237) — Winded already existed; these two didn't.
  - **Party Strength** (MM1:140-144) — bare `(MM1)` citation, matching the book's convention for MM-manual-only terms.
  - **Pinnacle Technique** (II.4:98) — Major Advancement's non-Attribute option.
  - **Weapon** (IV.1:13-19) — the category-to-attribute table, compressed; cited `(Chapter IV.1)`.
  - **Winded** — added alongside Off-Balance/Shaken for a complete, consistent Tier 1 trio (Staggered/Cornered, Tier 2, already had entries).
- Glossary term count: 61 (was 54; +7: Saving Throw, Off-Balance, Party Strength, Pinnacle Technique, Shaken, Weapon, Winded). Regenerated `Index.md` — 61 `## ` sections, matching the term count exactly.

Command: `cd software && python -m pytest -q`
Result: **1026 passed**.

### W1-9 *(app-M6)* — TDD

- `software/tools/build_index.py:_slugify` used `re.sub(r"\s+", "-", slug)`, collapsing any run of whitespace into a single hyphen. GitHub's actual anchor algorithm emits one hyphen **per** whitespace character — an em-dash heading like `### Zahna — The Scholar` strips the em-dash as punctuation but leaves the space on each side, so the real GitHub anchor is `#zahna--the-scholar` (double hyphen), not the collapsed `#zahna-the-scholar` every link in the old Index pointed at. Fixed by dropping the `+` quantifier: `re.sub(r"\s", "-", slug)`.
- Tests added to `software/tests/test_build_index.py` (3, using the exact real headings the bug affects, not synthetic ones):
  - `test_slugify_em_dash_heading_anchors_with_double_hyphen` — `"Zahna — The Scholar"` (`Quick_Start.md:17`) → `"zahna--the-scholar"`.
  - `test_slugify_plus_containing_heading` — `"Magic: Domain + Intent + Scope"` (`MM5_Quick_Reference.md:206`) → `"magic-domain--intent--scope"`.
  - `test_slugify_plain_heading_unchanged` — `"Facet Levels"` → `"facet-levels"` (single spaces are unaffected by the per-character fix).
- Regenerated `Index.md`: **33 lines changed** (matches the audit's "33 previously-broken anchors" exactly). Spot-checked 3 by hand against the actual source headings:
  1. `Quick_Start.md#zahna--the-scholar` ← `### Zahna — The Scholar` (`Quick_Start.md:17`) ✓
  2. `MM5_Quick_Reference.md#magic-domain--intent--scope` ← `## Magic: Domain + Intent + Scope` (`MM5_Quick_Reference.md:206`) ✓
  3. `II.4c_Character_Creation_Facet_Soul.md#facet-of-the-soul--technique-tree` ← `## Facet of the Soul — Technique Tree` (`II.4c_Character_Creation_Facet_Soul.md:23`) ✓
  All three now match GitHub's actual anchor generation; all three were broken (single-hyphen) before this fix.

Command: `cd software && python -m pytest -q`
Result: **1029 passed** (1026 + 3 new).
