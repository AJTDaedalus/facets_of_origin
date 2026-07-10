# LOG — v0.3 Ruleset Revision

**Tier:** Worker (Sonnet 5) execution log
**Tasks:** `docs/TASKS_v0.3_ruleset_revision.md`

---

## WS-C — Consolidation pass (D5)

**Scope:** C1–C11, run as a single session, landed as one commit per the task's own instruction ("Target: one commit"). User approved this scope explicitly before starting (WS-C only, then stop and report) rather than a strict one-task-per-checkpoint cadence.

- **C1** — Added the two repo rules to `CLAUDE.md` under Software-PHB Synchronization: quick refs compress/never paraphrase; simulator may only drive `app/game/combat.py`.
- **C2** — Fixed II.5's stale pre-technique magic text (removed the invented difficulty penalty). Verified II.3, MM5, Quick_Start.md, and `facet.yaml` already state the canonical rule (Minor scope only, no penalty) — no fix needed there.
- **C3** — Fixed the "same or different" → "same type" Broken-stacking language in III.3's quick-ref card and MM5.
- **C4** — Fixed `_handle_apply_condition` in `websocket.py` to escalate to Broken only when the incoming Tier 2 condition id already exists on the character (was: escalating on *any* second Tier 2, regardless of type). Reads the Tier 2 id set from `ruleset.combat.conditions.tier2` instead of a hardcoded literal. Rewrote the existing `test_tier2_stacking_to_broken` (which encoded the buggy behavior) into three tests: same-type escalation, different-type coexistence, third-application idempotence. All pass; full suite green.
- **C5** — Deleted the invented "deflect and counter (attacker takes T1)" Parry effect from III.3's quick-ref and MM5 — Parry outcomes are now identical to Dodge everywhere, matching the already-correct body text.
- **C6** — Generalized the Strike/Parry roll formulas in III.3 (body text + quick ref), MM5, and Quick_Start.md from hardcoded "Strength + Combat" to "weapon attribute + relevant skill" (Combat for melee/unarmed, Finesse for ranged), matching IV.1's weapon-category table. Confirmed the engine (`websocket.py:472-479`) already accepts any attribute/skill — no code change needed.
- **C7** — Fixed MM5: attribute rating 1 label "Poor" → "Weak" (matches `facet.yaml`); PvP tie rule "ties go to defender" → "both achieve partial success" (matches III.1).
- **C8** — Deleted the "Spent ally" ghost-text reference from Intercept in III.3 (Spent was cut in the 2026-03-04 simplification). Rewrote the ambiguous Maneuver wording ("target's next roll is Easy") to the canonical "rolls **against** the target are Easy."
- **C9** — Example-character continuity, the largest task in this batch:
  - **Escalated a real discrepancy to the user first**: BRIEF/DESIGN (both dated today) said Zulnut's background is "Wandering Disciple" / pronoun "he", but the actual `characters/Zulnut.fof`, II.5's Background section, and II.4's worked example currently said "Street Performer" / "she". Asked the user directly rather than guessing; confirmed "Wandering Disciple / he" is canonical (also matches the untouched `README.md` and `Quick_Start.md`, which were never drifted). Rewrote `characters/Zulnut.fof` (background block + top-level skill from `perform`→`stealth`), fixed II.5's closing "In Play" analysis paragraph, and fixed II.4's pronoun in the Stealth/Finesse point-spend example.
  - Rewrote II.3's "Example: A Mage, a Beam, a Problem" — previously described Zahna as a "Focused Fire mage" rolling Spirit; rewrote to Inscription domain (fracture-glyph on structural joints) rolling Knowledge, with correct "he" pronoun throughout.
  - Found and fixed two *additional* errors in III.3's "Example pools" block while verifying against source-of-truth `.fof` files (not explicitly named in the ledger row but caught by the "all four files agree with `characters/*.fof`" accept criterion): Zahna's Constitution was listed as 2 (actual: 1, pool should be 3 not 4); Mordai's Endurance skill was listed as Practiced (actual: Novice, pool should be 5 not 6). Traced the pool-6 error through the downstream boss-fight vignette and corrected three dependent Endurance-tracking numbers (lines ~456, 522, 536) that had been built on the wrong starting value.
  - Verified via `combat_sim.py`'s `mordai_def()`/`zulnut_def()` fixtures that the engine already used the correct pool values — only the PHB prose was stale.
- **C10** — Rewrote II.4 line 89, which said cross-Facet Facet-level advances "do not count toward your Major Advancement threshold" — directly contradicted the Major Advancement section's own worked example two paragraphs later (lines 207–209), which sums levels across Facets. Canonical (per BRIEF D3): cross-Facet levels **do** count. Left the Zulnut worked example at line 87 and the 6/12 threshold numbers untouched — those are B5's job (WS-B) once B2/B3 land the new 5/10/15 thresholds.
- **C11** — Manual continuity pass across `player_handbook/`, `mm_manual/`, and `Quick_Start.md` (the `continuity-check` skill's tooling targets World Anvil campaigns via MCP calls, not applicable here — did the equivalent by hand: grepped for remaining pronoun/background/formula drift for all three example characters, found none outstanding). Full test suite: **722 passed, 1 pre-existing unrelated failure** (`test_default_port_is_8000` — fails identically on a clean stash of the branch before any of this session's changes; caused by a local `.env` setting `PORT=8010`, not touched by WS-C).

**Files changed (10):** `CLAUDE.md`, `characters/Zulnut.fof`, `mm_manual/MM5_Quick_Reference.md`, `player_handbook/II.3_Magic.md`, `player_handbook/II.4_Character_Creation_Facets.md`, `player_handbook/II.5_Character_Creation_Backgrounds.md`, `player_handbook/III.3_Combat.md`, `player_handbook/Quick_Start.md`, `software/app/api/websocket.py`, `software/tests/test_websocket.py`.

**Note for whoever runs `git status` next:** an e2e Playwright test (`test_playtest_02.py`) regenerates `playtest/02_silence_of_ashenmoor/digital_tool_log.md` with new random dice rolls every time the full suite runs. This is pre-existing test behavior, not a WS-C change — it was reverted twice during this session and is not part of the commit.

**Status:** WS-C complete, ready to commit as `Consolidate contradictory rules (PHB D5 ledger)`. Per the user's chosen scope for this session, stopping here — WS-A0/WS-A/WS-B/WS-D/WS-E are not started.
