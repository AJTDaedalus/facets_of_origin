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
- [x] W1-10 — Apparatus low-severity sweep. *(cre-L1, cre-L2, cre-L3, cre-L5, cre-L6, app-L6)*
- [x] W1-11 — README: regenerate every factual claim from canon. *(README audit — D2 for the TR value)*
- [x] W1-12 — Wave 1 close-out.

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

### W1-10 *(cre-L1, cre-L2, cre-L3, cre-L5, cre-L6, app-L6)*

- `Appendix_Magic_Domains.md:189` — "following the same structure as Soul" implied matching counts; Soul is 9 core + 3 prismatic, Mind is 6 core + 3 prismatic. Reworded to claim only the structural pattern (core/prismatic split, same Tier gating), not the counts.
- `II.3:188` — added a one-line forward pointer in the Domain Quick Reference intro noting Body domains are deferred, pointing at *A Brief Note on Body Magic* below (which keeps the actual explanation, unmoved).
- `II.3:223` — removed the duplicate "Full descriptions ... Appendix: Magic Domain Catalog" sentence; the near-identical sentence at `:188` (which also carries the † prismatic-marker note) stays as the one pointer.
- `II.4b:139` / `II.4c:136` — Ascendant Domain's "taken once, however many Facet trees" rule lived only at `II.3:246`. Added the same sentence, cited back to Chapter II.3, at the end of each tree's own Ascendant Domain entry.
- `Table_of_Contents.md:13-16` — II.4/II.4a/b/c titles ("Facets & Advancement (Body)" etc.) didn't match the files' own titles ("Facet of the Body" etc.) at all. Brought the ToC in line with the actual file titles, following the same short-form convention every other II./III./IV. entry already uses.
- `Table_of_Contents.md:32-33` — "Appendix A: Magic Domain Catalog" / "Appendix B: Character Sheet" — the letters exist nowhere in the appendix files themselves (`# Appendix: Magic Domain Catalog`, `# Appendix: Character Sheet`), and nothing else in the repo references "Appendix A/B" (grepped). Dropped the letters in the ToC rather than adding them to two more files, per the task's "pick one" instruction — lower blast radius.
- Regenerated `Index.md` — no diff (no heading text changed by any of the above).

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W1-11 (README audit — D2 for the TR value)

Every number checked against the source file at edit time:

- "24 skills" → **15** — counted `player_handbook/II.6_Character_Creation_Skills.md`'s skill table (5 per Facet × 3 = 15).
- "27 domains across three traditions (Resonance, Channeling, and one TBD)" → **21 domains across two traditions (Resonance/Mind, Channeling/Soul); Body magic deferred to the Shattered Origin setting Facet** — counted `II.3_Magic.md`'s Domain Quick Reference tables (12 Soul + 9 Mind = 21); there is no third tradition in canon, and Body magic isn't a tradition awaiting a name, it's explicitly deferred.
- "613 tests" (both occurrences) → **1029** — `pytest --collect-only -q`, run in this commit (post-W1-9, which added 3 tests).
- "Harbor Thug (Mook TR 1)" → **TR 2**. **Correction to the task's premise**: `enemies/harbor_thug.fof` already has `tr: 2` (with the arithmetic in a comment) — D2's value is *already true* in the .fof, just not yet in `mm_manual/MM1_Encounters_and_Enemies.md`'s stat-block example (`:47-56`) or its `.fof`-format example block (`:293`), which is what W2-4 (mm-H1) actually fixes. The README was simply stale against an already-correct source file.
- "Archive Guardian (Boss TR 16)" → **TR 17** — `enemies/archive_guardian.fof:24` already states `tr: 17`.
- "Two simulated playtests" (both occurrences: features list and roadmap checkbox) → **Six** — `git ls-tree -d --name-only HEAD playtest/` lists 6 committed directories (`01_thornwall_undercroft` through `06_expert_novice_campaign`); `playtest/07_oraga_night_playtests` is untracked and correctly excluded per the task instruction.
- Added an HTML comment above the claims block (Character Creation bullet onward) naming each figure's source, so future edits know to re-verify rather than hand-edit a number.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W1-12 — Wave 1 close-out

All 12 W1 tasks done (W1-1 through W1-11 above, this entry for W1-12). Final suite run before opening the PR:

Command: `cd software && python -m pytest -q`
Result: **1029 passed** (baseline was 1026; +3 from W1-9's slugger tests).

Findings closed this wave: cre-H1, cre-H2, cre-H3, cre-M1, cre-M2, cre-M4, cre-M5, cre-L1, cre-L2, cre-L3, cre-L4, cre-L5, cre-L6, rul-M4, rul-M5, rul-L1, rul-L2, rul-L3, rul-L6, mm-M1, app-M5, app-M6, app-L1, app-L2, app-L3, app-L4, app-L6, README audit (D2's TR value stated; made fully true pending W2-4 in MM1).

DESIGN §6 voice-review flags carried into the PR: W1-2 (Scholar's Luck replacement clause), W1-5 (the :73 Facet Levels example — departed from the task's literal "swap to Stealth" wording), W1-6 (the added fourth Threat Clock beat).

PR: opened via `gh pr create` against `main`, branch `fix/audit-wave1-corrections`.

---

## W2 — v0.3 migration completion

- **Branch:** `fix/audit-wave2-v03-migration`
- **Date:** 2026-07-31
- **Baseline:** `pytest --collect-only -q` → **1029 tests collected**, measured on this branch after merging W1 (PR #14).

### W2 task list (from `docs/TASKS_audit_remediation.md`)

- [x] W2-1 — Migrate Magic in Combat and Attune to the Resolve model. *(mm-M2)*
- [x] W2-2 — Combat quick reference: declarable actions. *(rul-M2)*
- [x] W2-3 — MM1 enemy Attack/Defense modifiers: what they mean at the table. *(mm-M4)*
- [x] W2-4 — Mook TR: the formula wins. *(mm-H1 — D2)*
- [x] W2-5 — Retire superseded simulation citations. *(mm-M5, mm-L4, mm-L5)*
- [x] W2-6 — MM low-severity sweep. *(mm-L1, mm-L6, mm-L7)*
- [x] W2-7 — facet.yaml: Overwhelming Force. *(sync-H-1)* **TDD**
- [x] W2-8 — Encode the magic-Technique domain prerequisite (the guard). *(sync-H-2, part 1)* **TDD**
- [x] W2-9 — Switch to the PHB's branch/tier prerequisite rule. *(sync-H-2, part 2)* **TDD**
- [x] W2-10 — Wave 2 close-out.

### W2-1 *(mm-M2)*

- `III.3:379` — "Conditions from magical Strikes" applied the PvP Condition-tier table unconditionally, even against enemies, which contradicts the Resolve model (III.3:124) that governs the "usual case." Rewrote as "Resolving magical Strikes": against an enemy, deplete Resolve on the same table as a physical Strike (10+ = -2 and may hang a rider, 7-9 = -1); against another character, apply a Condition directly on the PvP tier table. No magic-specific number invented — it's the existing Strike table, cited, not extended.
- `III.3:391` (Attune) — "the Condition tier follows the Strike outcome table" was ambiguous/wrong for the enemy case (no Condition tier applies there, Resolve does). Reworded to state both branches explicitly.
- **Verify-only, unchanged:** `MM5:109` ("vs enemy depletes Resolve like a Strike") was already a legal compression of the corrected body text — confirmed, not rewritten. `Quick_Start.md:143` ("Cast a spell | 2d6 + Spirit or Knowledge (by tradition)") states only the roll formula, never the old Condition-tier-only model — confirmed unchanged is correct.
- Regenerated `Index.md` — 1 new line (`III.3 — Mind and Soul in a Fight` now indexes under Resolve, since Attune's paragraph now names Resolve explicitly).
- Did not touch `III.3:395` (Gamble / "Reckless Press") — out of this task's scope; that's W3-5 (rul-M3, D6).

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-2 *(rul-M2)*

- `III.3:646` — the Exchange Flow quick ref listed "Withdraw" as a step-2 action alongside Strike/Support/Maneuver/Magic. Withdraw is a Posture, declared in step 1, not an action — body text defines exactly three actions (`:104-161`) plus Magic (which uses the Strike action economy, `:375`). Removed "Withdraw" from the step-2 list.
- Regenerated `Index.md` — no diff.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-3 *(mm-M4)* — flagged for PR review per DESIGN §6

- `MM1:26` (stat-block field) — "same modifier used for Parry; Dodge uses Dex modifier if different" implies the enemy rolls, which contradicts `III.3:331` ("NPCs do not roll dice"). Reworded: an authoring input, not a rolled modifier — feeds the TR formula and informs the difficulty the MM sets for PC Strikes and PC reactions against this enemy's attacks (both Chapter III.3, no new rule asserted).
- `MM1:197` (Named NPC "short list") — "what they use to Parry" had the same problem. Same fix applied.
- Grepped `used for Parry|use to Parry|Dodge uses Dex` repo-wide — no other instances.
- Did not touch the `Attack:` field (`MM1:25`) — it doesn't make an explicit rolled-modifier claim and wasn't named in the task.
- Regenerated `Index.md` — no diff.
- **Flag for review:** this is the one Wave 2 line a reader could mistake for a new rule, per DESIGN §4.2 — it states only what III.3 already rules, but worth a second look.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-4 *(mm-H1 — D2)*

**Grep hit list** (`TR 1|tr: 1|harbor_thug` across `mm_manual/`, `enemies/`, `spec/`, committed `playtest/` dirs, `software/tests/`), before editing:

```
mm_manual/MM1_Encounters_and_Enemies.md:52  (stat-block example: Attack +0, TR: 1)
mm_manual/MM1_Encounters_and_Enemies.md:121 (TR Reference Examples: "Basic Mook ... | 1 | Offense 2, Durability 0 — minimum 1")
mm_manual/MM1_Encounters_and_Enemies.md:128 (TR minimums note: "Mook: TR 1 (even the most incompetent...)")
mm_manual/MM1_Encounters_and_Enemies.md:286-293 (.fof teaching example block: id harbor_thug, attack_modifier 0, tr: 1)
enemies/harbor_thug.fof:18 (tr: 2, already correct) and :29 ("TR 1 minimum by rule." — self-contradicting note)
enemies/chicken.fof:18 (tr: 1, attack_modifier -1)
software/tests/test_encounter.py:131 (synthetic trs = {"thug": 1} in a weighting-formula unit test)
software/tests/test_enemy.py:244-250 (loads harbor_thug.fof, asserts calculate_tr() >= 1)
software/tests/test_api_enemy.py:24 (creates an enemy id "harbor_thug", asserts tr >= 1)
software/tests/test_combat_characterization.py:37,174 (uses harbor_thug_def fixture, no TR assertion)
playtest/01_thornwall_undercroft/scenario.md:39,44,67 (Dust Construct, "minimum TR 1", offense 2 computed)
playtest/02_silence_of_ashenmoor/scenario.md:43,49,92,100 and session_log.md:419 (Husk, same pattern)
playtest/04_resource_tax/scenario.md:86,105,129 and run_pt04.py:59,72,78 (Bandit Scout/Archer, Elite Bandit)
playtest/05_technique_showcase/scenario.md:105,107,129 (Sparring Partner, Arena Assistant)
playtest/06_expert_novice_campaign/scenario.md:47,52,73, session_log.md:71,79, live_unscripted_playtest_log.md:45,66, agent_playtest_log.md:51, agentic_playtest_compendium.md:35, batch_results.json:45 (Water-Logged Sentinel, Sonic Bat)
```

**Fixed** (the four sites the task names):
- `MM1:52` — Harbor Thug stat-block example: `TR: 1` → `TR: 2` (Attack +0 → Offense 2 per the table at `:87-92`; Durability 0; sum 2).
- `MM1:121` — TR Reference Examples table: "Basic Mook (unskilled, no armor) | 1 | Offense 2, Durability 0 — minimum 1" was self-contradicting — its own stated inputs sum to 2, so the "minimum 1" floor never actually applied here. Fixed to `| 2 | Offense 2, Durability 0 |`.
- `MM1:293` — the `.fof`-format teaching example (`id: harbor_thug, attack_modifier: 0, tr: 1`) → `tr: 2`, matching the real file.
- `enemies/harbor_thug.fof:29` — removed the self-contradicting "TR 1 minimum by rule." note (the file's own `tr: 2` doesn't need or match the floor).

**Left unchanged, with reason:**
- `MM1:128` ("Mook: TR 1 ... even the most incompetent attacker") — this is the TR-minimum-by-rule text itself, explicitly told to stay (task instruction: "MM1:127's minimum-1 floor text stays — it is still correct for attack −2"). It describes the genuine floor case (attack −2 → offense 0, which needs clamping to 1), not Harbor Thug's case.
- `enemies/chicken.fof:18` — `tr: 1` is **correct**: attack −1 → offense 1 (not 2), + durability 0 = 1. No floor clamping even applies; the arithmetic is simply 1. The chicken remains the TR-1 baseline, not renamed, per the task instruction.
- `software/tests/test_encounter.py:131`, `test_enemy.py:244-250`, `test_api_enemy.py:24`, `test_combat_characterization.py:37,174` — none hardcode an exact TR of 1 for Harbor Thug; they use `>= 1` floor checks or a synthetic, unrelated `"thug": 1` fixture for testing the weighting formula in isolation. Confirmed the full suite (1029) still passes after the `.fof` and MM1 edits — nothing broke.
- **All committed `playtest/` scenario and session-log hits** (01, 02, 04, 05, 06) — these are historical playtest records for *other* Mooks (Dust Construct, Husk, Bandit Scout/Archer, Elite Bandit, Sparring Partner, Arena Assistant, Water-Logged Sentinel, Sonic Bat), not Harbor Thug, and several show the *same* systemic pattern (offense 2, misapplied "minimum TR 1" floor). They are out of this task's explicit scope (the task names four fix sites: `MM1:55, :121, :293` and `harbor_thug.fof:29`) and are transcripts of what happened in a specific simulated session — rewriting their numbers after the fact would falsify the historical record, the same principle W2-5 applies to superseded simulation citations (don't re-run simulations, don't rewrite history). Left untouched.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-5 *(mm-M5, mm-L4, mm-L5)*

- `MM1:411` (last line) — "Simulation data confirms this arc: Skirmish → Standard survives at 98%. Skirmish → Standard → Hard survives at 55%…" was sourced from Series 6/F (`research/simulation_log.md:352-353`), a section explicitly marked **SUPERSEDED (v0.2 semantics)** (`:365`) — those runs used the deprecated TR-budget multiplier definitions of Skirmish/Standard/Hard, not the current Recipe-Table ones (under which Hard alone is ~47%). Did not re-run simulations (per the task instruction); re-sourced to the current, already-validated Recipe Table numbers instead of inventing a new cumulative statistic: "the Encounter Recipe Table above confirms the shape of this arc at each individual band — Skirmish (100%), Standard (~76-80%), Hard (~47-48%)."
- `MM2:165` — "A Skirmish-budget fight (Party Strength × 1) against Mooks" defined Skirmish by the deprecated TR-budget formula. The current definition (MM1's Encounter Recipe Table, `:343`) is a Mook-only roster, not a TR multiplier. Reworded to "A Skirmish fight (a Mook-only roster, per the Encounter Recipe Table)."
- `enemies/veteran_soldier.fof:41-42` — the notes field computed "effective TR 10 × 0.75 = 7.5 ... between Standard and Hard" for a solo encounter, using the pre-Series-9 TR-budget-with-solo-multiplier model. This directly contradicts MM1's current actor-count doctrine (`:136`: "One Named or one Boss is trivial for a fresh party no matter how high its TR"). Replaced with a note stating the current doctrine and steering the MM toward a multi-actor roster instead.
- **Adjacent issue found, left out of scope:** `veteran_soldier.fof:16` — `defense_modifier: 3 # Parry: same roll` has the same "NPCs don't roll" problem W2-3 fixed in MM1, but this file wasn't named in either task's file list. Not fixed here to avoid unauthorized scope expansion; worth a follow-up sweep.
- Regenerated `Index.md` — no diff. `research/simulation_log.md`'s Series 6 section remains labeled SUPERSEDED and untouched, per the task's explicit instruction.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-6 *(mm-L1, mm-L6, mm-L7)*

- `MM3:218` — the Facet Level 2 row claimed "a second and third Technique deepen their specialty," but II.4 grants exactly one Technique per Facet level, and MM3's own Level 3 row already claims "a third Technique unlock." Fixed to "a second Technique."
- `MM1:220` — "(see *Armor*, above)" pointed at a heading named "Armor" that doesn't exist anywhere in MM1. The real referent is the "**Armor bonus:**" subsection. Fixed the pointer text to match.
- `MM1:176` — "Mooks need only three things: an attack modifier, a fictional description, and a number" undercounted against its own four-step "Building a Mook" list (attack modifier, description, armor decision, calculate TR) two lines below. Fixed to "four things," naming the armor decision explicitly.
- No rules text changed — counts and pointers only, per the task's accept criteria.
- Regenerated `Index.md` — no diff.

Command: `cd software && python -m pytest -q`
Result: **1029 passed**.

### W2-7 *(sync-H-1)* — TDD

- `software/facets/base/facet.yaml:294-299` — Overwhelming Force still carried the pre-v0.3 rule ("succeed by 3 or more above the threshold... staggered... act last... cannot take reactions"), which has no relationship to the current Condition/Resolve model. Replaced with PHB II.4a:39-40's actual rule: once per scene, on a full success (10+) Strike against a single target, the target takes no offensive action in the next exchange.
- Tests added to `software/tests/test_docs_consistency.py` (2, written first — confirmed red before the fix):
  - `test_overwhelming_force_matches_phb_ii4a` — the yaml description carries "once per scene" and the 10+/full-success trigger.
  - `test_no_pre_v03_overwhelming_force_text_survives` — `"3 or more above the threshold"` doesn't appear anywhere in `facet.yaml`.
  - Added a `_find_technique` helper that walks the full `techniques` tree (`facets.yaml`'s `techniques: {body/mind/soul: {branches: [...]}}` structure) by id, for reuse in later Wave 2/4 technique tests.

Command: `cd software && python -m pytest -q`
Result: **1031 passed** (1029 + 2 new).

### W2-8 *(sync-H-2, part 1)* — TDD

- `software/app/facets/schema.py` (`TechniqueDef`) — added `requires_domain: str | None = None`, a Facet id ("mind"/"soul") whose domain list the character must already hold a domain from. Documented why: the sync report's H-2 note is that this prerequisite is *currently* satisfied only as a side effect of the strict Tier1→Tier2→Tier3 chain, which W2-9 is about to loosen (branch/tier rule instead of the specific chain). Without an explicit guard, loosening the chain would let a character reach Second/Ascendant Domain via a non-domain-granting Tier 1/2 pick in the same branch.
- `software/facets/base/facet.yaml` — set `requires_domain: mind` on `second_domain_mind` and `ascendant_domain_mind`; `requires_domain: soul` on `second_domain` and `ascendant_domain_soul`. Did not touch any `prerequisites` list, per the task's explicit instruction.
- `software/app/game/character.py` (`select_technique`) — enforces the guard right after the existing prerequisite check: if `tech_def.requires_domain` is set, the character must hold a domain (via `held_domains()`) drawn from that Facet's domain catalog (`_facet_domains()`, both pre-existing helpers). Refusal message names the missing domain's Facet.
- Tests added to `software/tests/test_character.py` (3, written first):
  - `test_select_technique_second_domain_refused_without_domain` — `the_language_beneath_language` injected directly into `techniques` (bypassing `select_technique`) so the prerequisite-chain check passes while `magic_domain` stays unset; the domain guard refuses independently of the chain.
  - `test_select_technique_second_domain_permitted_with_domain` — the full legitimate chain (`spiritual_domain` → `the_language_beneath_language` → `second_domain`) succeeds once a domain exists.
  - `test_select_technique_ascendant_domain_refused_without_domain` — same bypass pattern, for Ascendant Domain.
  - Note: under the *old* chain (still in place this task), the guard can't organically trigger in real play — the chain itself already forces a domain-granting Tier 1 pick first. The refusal tests use direct `techniques.append()` injection specifically to prove the guard's logic is independent of the chain, since that's exactly the property W2-9 will rely on.

Command: `cd software && python -m pytest -q`
Result: **1034 passed** (1031 + 3 new).

### W2-9 *(sync-H-2, part 2)* — TDD

- `software/app/facets/registry.py` (`MergedRuleset`) — added `_technique_branch_map` and `_technique_tier_map` (built once at merge time, alongside the existing `_technique_facet_map`) and their accessors `get_technique_branch()` / `get_technique_tier()`.
- `software/app/game/character.py` (`select_technique`) — added the PHB II.4:83 branch/tier check right after the existing (now-mostly-empty) `prerequisites` list check: for any Technique at tier > 1, the character must hold at least one Technique at `tier - 1` in the *same branch*. The old `prerequisites` field/check stays in the schema and code path — it's just a no-op for the base ruleset now, and still available for homebrew Facets that want a specific chain.
- `software/facets/base/facet.yaml` — emptied all 39 Tier 2/Tier 3 `prerequisites: [x]` lists to `[]` (script-verified: exactly the 39 chain-only entries, confirmed by diffing before/after — nothing else in the file touched). Did not touch `requires_domain` (W2-8) or any other field.
- Tests (7 total, per DESIGN §4.2's exact list — 5 new + 2 pre-existing updated, all written/updated before running to confirm red→green):
  1. **Newly legal** — `test_branch_tier_rule_weapon_mastery_unlocks_overwhelming_force`: Weapon Mastery (Might T1) → Overwhelming Force (Might T2), previously rejected (old chain-only prereq was `forcing_hand`), now legal.
  2. **Mirror in a different branch and tree** — `test_branch_tier_rule_mirrors_in_a_different_branch_and_tree`: the_wrong_note (Mind/Instinct T1) → immediate_threat (Mind/Instinct T2, old chain-only prereq was `never_surprised`), now legal. One example satisfying both "different branch" and "different tree" from the Might case.
  3. **No Tier 1 in branch** — `test_branch_tier_rule_rejects_tier_two_without_any_tier_one_in_branch`: fresh character, no Techniques, `overwhelming_force` refused.
  4. **Cross-branch Tier 1 doesn't count** — `test_branch_tier_rule_rejects_cross_branch_tier_two`: holding `forcing_hand` (Might T1) does not satisfy `shadow_walk` (Grace T2) — the rule is branch-scoped, not tree-wide.
  5. **Tier 3 with only Tier 1 in branch** — pre-existing `test_tier_three_rejected_without_tier_two` (`test_websocket.py`) updated: its exact-message assertion (`"the_aimed_truth" in msg`) no longer holds since the rejection reason is now generic ("Tier 2"), but the underlying behavior — still refused — is unchanged. Updated the assertion, not the test's intent.
  6. **Second Domain, no domain, post-loosening** — `test_branch_tier_rule_second_domain_still_refused_without_domain_post_loosening`: proves the W2-8 guard survives the chain loosening using a *genuinely reachable* sequence (sense_the_unseen → formed_bond satisfies the branch/tier rule with no domain ever granted), not W2-8's direct-injection bypass (which was necessary only while the old chain still blocked this path in play).
  7. **Second Domain, with domain, still legal** — pre-existing `test_select_technique_second_domain_permitted_with_domain` (W2-8) continues to pass unmodified; the full legitimate chain still works exactly as before.
- Also updated `test_select_technique_rejects_unmet_prerequisite` (`test_character.py`) — same exact-message-vs-generic-message issue as item 5's websocket test, fixed the same way.
- **Both message-assertion updates are within the advancement/technique test area** (the exact area this task changes) and both still assert the same underlying behavior (rejection) — not new failures outside scope requiring escalation. Confirmed no other file in the repo references specific chain-prerequisite ids in an assertion (grepped `software/tests/`, `software/app/`, `software/tools/`).

Command: `cd software && python -m pytest -q`
Result: **1039 passed** (1034 + 5 new).

### W2-10 — Wave 2 close-out

All 10 W2 tasks done. Final suite run before opening the PR:

Command: `cd software && python -m pytest -q`
Result: **1039 passed** (baseline was 1029; +10 across W2-7/8/9's TDD tasks).

Findings closed this wave: mm-H1, mm-M2, mm-M4, mm-M5, mm-L1, mm-L4, mm-L5, mm-L6, mm-L7, rul-M2, sync-H-1, sync-H-2.

DESIGN §6 flag carried into the PR: W2-3 (MM1 enemy Attack/Defense modifiers) — states only what III.3 already rules, but is the one Wave 2 line a reader could mistake for a new rule.

PR: opened via `gh pr create` against `main`, branch `fix/audit-wave2-v03-migration`.

---

## W3 — Canon-decision items

- **Branch:** `feature/audit-wave3-canon`
- **Date:** 2026-07-31
- **Baseline:** `pytest --collect-only -q` → **1039 tests collected**, measured on this branch after merging W2 (PR #15).
- **Model routing this wave:** mechanical/TDD tasks execute directly on Sonnet (this session); new-canon-prose tasks (W3-6, W3-8, W3-9, W3-10, W3-11, W3-13 — all DESIGN §6 sign-off items) are drafted by an Opus subagent via the Agent tool's `model` override, briefed with the relevant DESIGN section, the PHB/MM text being extended, and `references/phb-examples.md`'s voice guide, then reviewed/integrated/tested/committed here. Every draft still goes to the user for D12 sign-off before merge, per the plan.

### W3 task list (from `docs/TASKS_audit_remediation.md`)

- [x] W3-1 — Guild Apprentice gets its Specialty (three-way propagation). *(rul-H1 — D4)* **TDD**
- [x] W3-2 — Amend II.1's character sheet specification. *(app-H1, H2, M1–M4 — D7, part 1)*
- [x] W3-3 — Rebuild the character sheet appendix to the amended spec. *(D7, part 2)* **TDD**
- [x] W3-4 — 0 Endurance means Absorb only, absolutely. *(rul-M1, rul-L4 — D5)* **TDD**
- [x] W3-5 — Cut Reckless Press. *(rul-M3 — D6)*
- [x] W3-6 — Redefine pushing scope against the pre-Technique cap. *(cre-M3, mm-L8 — D8)* — sign-off
- [x] W3-7 — The Shattered Origin promise, both fixes. *(app-M7 — D9)*
- [x] W3-8 — Give the Trouble Table a canonical home. *(mm-M3, part 1 — D3)* — sign-off
- [x] W3-9 — Two Common Rulings into III.1. *(mm-M3, part 2 — D3)* — sign-off
- [x] W3-10 — MM2: "Adjudicating Magic". *(mm-M6 — D10, part 1)* — sign-off
- [x] W3-11 — MM coverage pointers + MM5 compression of the new section. *(mm-M6, mm-L9 — D10, part 2)* — sign-off
- [x] W3-12 — MM5 Spark-economy drift. *(mm-L2, mm-L3)*
- [x] W3-13 — II.4a gains its Facet introduction. *(cre-M6)* — sign-off
- [x] W3-14 — Rule two findings as-designed. *(cre-M7, rul-L5)* — sign-off
- [x] W3-15 — Wave 3 close-out.

### W3-1 *(rul-H1 — D4)* — TDD

- `II.5:197` — Guild Apprentice had **no** Specialty line at all (every other Background does), breaking II.5's own "five elements" claim. Added the Quick Start text verbatim: *"Artificers' Guild technical records — Standard becomes Easy when directly applicable."*
- `facet.yaml` (`guild_apprentice`) — replaced its third, different specialty string ("Formal training in a structured discipline...") with the same Quick Start text, per the task's explicit "replaced, not merged" instruction.
- Tests added to `test_docs_consistency.py` (2, written first, confirmed red on the yaml side before the fix — the PHB side was already correct from the same edit):
  - `test_guild_apprentice_specialty_matches_quick_start` — both II.5 and `facet.yaml` equal the Quick Start wording exactly.
  - `test_all_fifteen_backgrounds_have_a_specialty_in_phb_and_yaml` — every one of the 15 pre-built Backgrounds has a non-empty Specialty in both II.5 and `facet.yaml` (regression guard against this ever recurring for another Background).
- Regenerated `Index.md` — no diff.

Command: `cd software && python -m pytest -q`
Result: **1041 passed** (1039 + 2 new).

### W3-2 *(app-H1, H2, M1–M4 — D7, part 1)*

- `II.1:11` — "six sections" → "nine sections."
- Amended the section table to the shape DESIGN §4.3 specifies:
  - **Facet** — relabeled "advancement track" to "rank advances toward the next level" and added **Career Advances** (app-M2, app-M4).
  - **Background** — Secondary Skill row now reads "Secondary Skill (Novice, 1 mark) or Domain Origin if your Background grants magic" (app-M1).
  - **Magic** *(new)* — domain name, type, pre-Technique Minor-only flag (app-H2).
  - **Combat** *(new)* — Endurance (with the printed formula), Armor type + downgrade budget, Conditions, and Sparks (moved here from Session Resources; app-H1).
  - **Inventory** *(new)* — equipment, including the armor that drives the Combat section's budget (app-M3).
  - **Session Resources** — now Skill Points only.
- Nothing in the amended table states a rule the PHB doesn't already state elsewhere (Endurance formula from `Glossary.md:42`/III.3, Armor budget from III.3, domain scope-gating from II.3).
- `Appendix_Character_Sheet.md:3` still says "six sections" — that's W3-3 (D7, part 2), not touched here.
- Regenerated `Index.md` — 5 new lines (the new section's Armor/Magic/Combat/Spark mentions now index it, as expected).

Command: `cd software && python -m pytest -q`
Result: **1041 passed**.

### W3-3 *(D7, part 2)* — TDD

- `Appendix_Character_Sheet.md` — rebuilt to mirror W3-2's nine-section spec exactly: relabeled the Facet section's advancement row, added Career Advances; changed Background's Secondary Skill row to "...or Domain Origin"; added Magic (Magic Domain), Combat (Endurance with the printed formula, Armor Type, Armor Downgrade Budget Remaining This Scene, Active Conditions, Sparks — moved here), and Inventory sections; Session Resources now Skill Points only. `:3`'s "six sections" → "nine sections."
- **No new `Character` field added** — every new row maps to a field that already existed: `career_advances`, `magic_domain`, `endurance_current`, `armor`, `armor_downgrades_remaining`, `conditions`, `inventory` (all confirmed present on the model before writing a single sheet row).
- `test_docs_consistency.py` — updated `CHARACTER_SHEET_FIELDS` (renamed the advancement-track label, added the eight new-section labels) and added `test_new_character_sheet_sections_need_no_new_model_field`, a dedicated regression guard beyond the general INV-2 check, asserting each of the seven new labels is both registered and maps to a real attribute.
- **Zahna transcription check** (`characters/Zahna.fof`), by hand — nothing lost:
  - Attributes: Str 1, Dex 3, Con 1, Int 3, Wis 1, Kno 3, Spi 2, Luck 3, Cha 1 — all nine fit.
  - Facet: Mind, Level 0, 0 rank advances, Career Advances 1.
  - Background: "Former Apprentice" (Guild Apprentice), Starting Skill Lore (Practiced), Domain Origin (Inscription — magic-granting Background replaces the secondary skill slot, per `facet.yaml`'s `domain_replaces_secondary`), Specialty (Guild records).
  - Skills: Lore Practiced, 0 marks; the other 14 sit at their sheet rows Novice/0 by omission.
  - Techniques: none (empty list — the Techniques table is simply blank).
  - Magic Domain: Inscription.
  - Combat: Endurance current/max not set in the `.fof` (Zahna isn't mid-combat) — the max the formula computes is 4 + Constitution modifier (1 → −1) + Endurance rank (Novice, +0) = 3, matching the character's own `notes:` field ("Endurance pool of 3"). Armor/Conditions unset (none yet). Sparks 3.
  - Inventory: empty (not yet tracked in the `.fof`).
  - Session Resources: skill points remaining is session-transient state, not part of the persistent `.fof` — correctly has no source to transcribe.

Command: `cd software && python -m pytest -q`
Result: **1042 passed** (1041 + 1 new).

### W3-4 *(rul-M1, rul-L4 — D5)* — TDD

- **Engine check first:** `_handle_react` (`websocket.py:614`) already gates on `character.endurance_current <= 0 and reaction != "absorb"` **before** computing any posture-based reaction cost — so Withdrawn's `free_reactions` and Defensive's reduced cost never get a chance to override the floor. The engine was already correct; per the task's own instruction ("if the engine already refuses, keep the tests as regressions"), this task became text + yaml + a regression-test job, not a behavior fix.
- `III.3:167` (Reactions intro) — added the clarifying sentence: the 0-Endurance floor "is absolute, regardless of Posture: Withdrawn's free reactions and Defensive's reduced reaction cost only apply while you have at least 1 Endurance to spend."
- `III.3:718` (quick ref) — "Conditions land at full tier — no extra penalty" was wrong for an armored character (`:47`: armor still helps downgrade Conditions even at 0 Endurance). Corrected to "land at their normal tier — your armor still helps," and added "regardless of Posture" for the same reason as the body-text fix.
- `MM5:200` — already said "normal tier — no extra penalty" (not the "full tier" bug), so no correction needed there; added "regardless of Posture" anyway for consistency with the other two now-updated sites.
- `facet.yaml` (`combat.endurance_floor_rule`) — set to a full statement of the rule (previously empty, the field existed but was unused, like its siblings `mook_rule`/`named_npc_rule`/`boss_rule`). `websocket.py`'s refusal message now reads this field (falling back to the old literal if empty) — the engine genuinely reads it now, not just declares it in the schema.
- Tests (3 required; 2 new + 1 pre-existing satisfying the third), all in `test_websocket.py`:
  - `test_zero_endurance_dodge_refused_while_withdrawn` *(new)* — Dodge refused at 0 Endurance while Withdrawn.
  - `test_zero_endurance_dodge_refused_while_defensive` *(new)* — same, Defensive.
  - `test_zero_endurance_absorb_allowed` *(pre-existing, already covers "Absorb permitted")* — left as-is; still passes, now also exercises the yaml-sourced message path.
- Regenerated `Index.md` — 1 new line.

Command: `cd software && python -m pytest -q`
Result: **1044 passed** (1042 + 2 new).

### W3-5 *(rul-M3 — D6)*

- `III.3:395` (Gamble) — "Reckless Press" named a mechanic that was just the plain Spark rule (III.1:73-76: spend a Spark, add a d6, drop the lowest) under a different name, with no distinct effect of its own. A named mechanic must earn its name. Rewrote to point at the actual Spark rule directly.
- Grepped `Reckless` repo-wide: zero hits in `player_handbook/`, `mm_manual/`, `software/`, `characters/`, `enemies/`, `spec/`. The only remaining hits are in `docs/` — the audit corpus and this plan itself, which legitimately discuss the finding being fixed, not shipped content.
- Regenerated `Index.md` — no diff.

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-7 *(app-M7 — D9)*

- `I_Introduction.md:27` — "This handbook includes the Shattered Origin setting" overclaimed completeness (II.3 already defers Body magic domains to a forthcoming "Shattered Origin setting Facet," so the full setting isn't actually included). Softened to "is set in Shattered Origin," and named the forthcoming setting Facet explicitly.
- `Table_of_Contents.md` — added **"Shattered Origin (setting Facet)"** to the Facets (Optional Modules) planned list, giving II.3:252's Body-magic deferral an actual destination in the ToC, matching the other five planned-module entries' format.
- Regenerated `Index.md` — no diff (`Table_of_Contents.md` is in `NOT_INDEXED`; `I_Introduction.md`'s change touched no heading).

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-12 *(mm-L2, mm-L3)*

- `MM5:59` — "1-2 Graceful Fail claims mid-session, not just at session end" invented a timing emphasis MM2 doesn't state; MM2's actual target is "1-2 per session across the whole table" (`MM2:499`). Fixed to match.
- `MM5:61` — the "midpoint diagnostic" was inverted: MM5 diagnosed on **earning** ("if no Spark has been earned by the midpoint"), but MM2's actual checklist item diagnoses on **spending** ("if a player hasn't spent a Spark by the session's midpoint, design a moment that rewards it," `MM2:536`). Fixed to match MM2 exactly — did not invent a new diagnostic.
- `MM5:62-63` — "Peer nominations are contagious... model it yourself" had no MM2 source at all; cut rather than authoring new MM2 text to retroactively justify it (out of this task's scope — no sign-off flag on W3-12). "Hoarding is a signal" does trace to MM2 (`:480`'s hoarding-is-behavioral-not-mechanical framing) — kept, reworded to match that framing precisely instead of the invented "award more visibly" fix.
- `MM5:74` — "Spend 2-4, earn 2-4, end with 2-4" flattened MM2's actual three-band Target Economy table (`MM2:519-524`: Low-activity 1-2/1-2/2-3, Standard 2-3/3-4/2-3, High-combat 3-4/4-6/1-3) into a single wrong number. Replaced with a compressed version of all three bands.
- INV-6 (typographic dashes) verified green.
- Regenerated `Index.md` — no diff.

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-14 *(cre-M7, rul-L5)* — sign-off item, user may veto

Added a new "Completeness Audit Remediation — Wave 3" section to `docs/DECISIONS.md` with two entries:

- **cre-M7** — Communion Tier 3 has one fewer non-magic pick than Archive (3 vs 4 total, counting the shared Second/Ascendant Domain pair both trees carry). Recorded as accepted: authoring a fourth Communion Technique is outside this cycle's Non-goals, and both trees offer the *same total* Tier 3 pick count once the shared magic-extension Techniques are counted — no character is actually short a door.
- **rul-L5** — no pre-built Background grants Survival. Recorded as accepted: changing an existing Background's skill grant has real knock-on cost (PHB entry, `facet.yaml`, tests, pre-gen characters) and is a content change outside this cycle's Non-goals; the custom Background path (II.5:83, five steps) already lets a Mind-primary character choose Survival as their Starting or Secondary skill.
- Both entries name the finding ID, state the rejected alternative, and give the rationale, per the task's accept criteria. **Flagged for user sign-off — either ruling may be vetoed, which escalates to Brain per D12.**

Command: `cd software && python -m pytest -q`
Result: **1044 passed** (unaffected — `DECISIONS.md` isn't part of the tested corpus).

### W3-6 *(cre-M3, mm-L8 — D8)* — sign-off item, drafted via Opus subagent

- **Drafted by an Opus subagent** (briefed with II.3's "Sparks and Magic" section, the "Before the Technique" blockquote, MM5's magic quick ref, and II.4c:135), reviewed and integrated by Sonnet.
- `II.3_Magic.md` — added a new bullet, **"Reaching Significant early (before the Technique)"**, between the existing "Pushing scope" and "Easing Major effects" bullets: a pre-Technique caster may spend a Spark to attempt one Significant-scope effect at the domain's normal Significant difficulty (the Spark buys scope, not a discount) — one effect per Spark, not a permanent unlock; Major stays closed until the Tier 1 Technique. Has a real referent back to the Minor-scope cap (points at *Before the Technique*, below it in the same chapter).
- `MM5_Quick_Reference.md` — rewrote the four post-difficulty-table bullets to group **all three** Spark-magic rules together (Focused eases Major / Broad ceiling immovable / the new pre-Technique push) and added the "standard domains only" qualifier to the Second Domain bullet (from II.4c:135), which the old MM5 line lacked.
- INV-6 (typographic dashes) verified green.
- Regenerated `Index.md` — 3 new lines (new heading term indexed).
- **Flagged for user sign-off (D12) — new canonical rule text.**

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-13 *(cre-M6)* — sign-off item, drafted via Opus subagent

- **Drafted by an Opus subagent** (briefed with II.4b's and II.4c's opening templates and II.4:13's one-sentence Body summary), reviewed and integrated by Sonnet.
- `II.4a_Character_Creation_Facet_Body.md` — added a `## The Body Facet` section between the chapter title and `### Skills of the Body`, matching II.4b/II.4c's template exactly: paragraph 1 (who they are, how they solve problems, a three-way comparative sentence) + paragraph 2 (their tools + capstone). Deliberately used a fresh "wall" image for the comparative sentence rather than reusing the door metaphor a third time (it already appears verbatim in both `II.4_Character_Creation_Facets.md` and `II.4c`) — a voice call, noted for review.
- No new mechanics — pure framing prose parallel to its siblings.
- **Adjacent issue found, left out of scope:** II.4a uses `### Skills of the Body` (h3) while II.4b/II.4c use `## Skills of the Mind`/`## Skills of the Soul` (h2), so the new `## The Body Facet` (h2) now nests the existing h3 beneath it — a pre-existing heading-level inconsistency between II.4a and its siblings, not introduced by this task. Worth a follow-up sweep; not fixed here.
- Regenerated `Index.md` — 1 new line.
- **Flagged for user sign-off (D12) — new framing prose.**

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-9 *(mm-M3, part 2 — D3)* — sign-off item, drafted via Opus subagent

- **Drafted by an Opus subagent** (briefed with III.1's structure/voice and MM5's existing "Unnarrated details" / "Can I try again?" bullets, which had no canonical source at all before this task), reviewed and integrated by Sonnet.
- `III.1_Core_Resolution.md` — added a new `## Standing Rulings` section at the end of the chapter (after "Failure (6-)"), with two subsections:
  - **Acting on Unnarrated Details** — players can always *ask* about the scene; they cannot *declare* an action assuming an unstated fact. Ties to the existing "lean toward yes" default.
  - **Trying Again** — a failed/partial roll may be retried only if the fiction has genuinely changed (new approach, new information, or time passing that cost something); otherwise the first result stands. Explicitly grounded in the already-canonical "a 6- is a development, never a dead end" principle.
- `MM5_Quick_Reference.md` — both Common Rulings bullets now cite their III.1 source (matching the file's existing trailing-parenthetical convention, e.g. `III.3:192`'s `(III.3, *Armor and Reaction Downgrades*)`), and compress the new body text rather than standing as unsourced assertions.
- Regenerated `Index.md` — no diff (neither new heading names a Glossary term).
- **Flagged for user sign-off (D12) — new canonical rule text.** Per the task's stated exception: if either ruling is rejected as non-canon, delete it from MM5 rather than keep an orphaned quick-ref line.

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-8 *(mm-M3, part 1 — D3)* — sign-off item, drafted via Opus subagent

- **Drafted by an Opus subagent** (briefed with MM2's "Improvisation Techniques" section for structure/voice and MM5's existing Trouble Table, which had no canonical source), reviewed and integrated by Sonnet.
- `MM2_Session_Design.md` — added a new `### The Trouble Table` subsection at the end of "Improvisation Techniques" (after "The NPC Name List"), expanding the six-row d6 table into full canonical guidance: per-category explanation with a worked example each, plus a "Working with the table" list (pick-over-roll, size to risk, never halt the story, vary it, hand it to a Graceful Fail claimant, pair with the Magic 6- Templates). Same six categories, same die mapping — no mechanic changed, only explained.
- `MM5_Quick_Reference.md` — the Trouble Table section now cites its MM2 source in the heading (matching the file's existing "(compressed from II.3 — see II.3 for full text)" convention) and compresses down to the table plus four short bullets instead of standing alone.
- INV-6 (typographic dashes) verified green.
- Regenerated `Index.md` — 15 insertions / 6 deletions (new heading and reworded MM5 table content reindex).
- **Flagged for user sign-off (D12) — new canonical body text.**

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

### W3-10 *(mm-M6 — D10, part 1)* — sign-off item, drafted via Opus subagent, largest new-prose task of the cycle

- **Drafted by an Opus subagent** (briefed with II.3's Scope table, the domain-boundary "lean toward yes" paragraph, the Outcome Tiers for Magic 7-9 guidance, and III.3's "Scope in combat" paragraph — the four PHB sources this section compresses), reviewed, fact-checked, and integrated by Sonnet.
- `MM2_Session_Design.md` — added `## Adjudicating Magic` as a new top-level section (after the newly-added Trouble Table, before "Managing Player Spotlight"), covering exactly four topics, each traced to a real PHB source:
  - **Judging Scope** — the scale-and-duration test, worked through two paired examples (a hold-glyph door: Significant vs. the same glyph asked to endure: Major) that isolate duration as an independent axis; the pre-Technique Minor-scope ceiling as a hard availability limit, not a difficulty question.
  - **Domain Boundary Calls** — the "lean toward yes" default, plus a "substance vs. rhyme" discriminator built directly from II.3's own two rejected examples (fire/weather, shadow/invisibility) contrasted with its own accepted ones (fire/air, shadow/sound).
  - **Designing the 7-9 Complication** — the three complication categories from II.3, with a technique for deriving a complication from the player's own stated intent (worked three ways against the canonical "freeze-the-lock" intent from II.3:33).
  - **Magic Against Active Opposition** — the Standard-difficulty floor, with the derived observation that it only ever moves the Focused/Minor cell (arithmetic on the existing difficulty table, not a new rule) — flagged as the section's strongest single line and worth extra scrutiny at sign-off.
- **Fact-check pass (before integrating):** verified every concrete claim against its cited source — the difficulty-table arithmetic, the "lean toward yes" quote, the three complication categories, the Standard-floor combat rule, and the "same action economy as a Strike" line all check out verbatim or near-verbatim against II.3/III.3. **Caught and corrected one inaccuracy:** the agent's active-opposition example paraphrased the established "In Play: The Beam" vignette (III.2) as *"He is holding a beam off Zulnut with one arm"* — the actual scene has Mordai holding the beam with **both hands**, buying the doorway for **both** Zahna and Zulnut, not one arm for one character. Corrected to *"He is holding up a collapsing beam with both hands so the others can get through,"* accurate to the source without over-specifying.
- No new mechanics anywhere in the section — every paragraph is a compression or application of already-existing PHB rules, per the task's hard constraint.
- Regenerated `Index.md` — 14 new lines.

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

**Flagged for user sign-off (D12) — the largest new-prose task in the cycle. Please review closely**, especially the "substance vs. rhyme" domain-boundary framing and the active-opposition floor's derived claim.

### W3-11 *(mm-M6, mm-L9 — D10, part 2)* — sign-off item, drafted via Opus subagent

- **Drafted by an Opus subagent** (briefed with the just-landed W3-10 "Adjudicating Magic" section, MM2's Pacing Toolkit, III.2's Hazards/Threat Clock and death-choice rules, II.5's Specialty rule, and MM5's existing citation conventions), reviewed, fact-checked, and integrated by Sonnet. Four pieces:
  - `MM2_Session_Design.md` — new "### Hazards as a Pacing Tool" subsection at the end of Pacing Toolkit, closing MM2's total absence of any hazard/Threat Clock mention. States the mechanic (4-segment clock, advances on partial/failure, wind-back costs an action with no roll) and the pacing shape (fills in roughly five or six party rolls — matching the exact figure W1-6 already corrected in III.2), then points at III.2 for the full rule.
  - `MM4_Running_the_Table.md` — new "### Character Death Is the Player's Call" subsection closing out Safety and Consent, framing the game's death-choice rule (scar vs. heroic death, player's call, never the MM's) explicitly as a consent mechanic — a real gap, since the section previously said nothing about death at all despite it being the most safety-relevant rule in the book.
  - `MM5_Quick_Reference.md` Common Rulings — one new bullet compressing II.5's Specialty rule (directly applicable → Standard becomes Easy; tangential → free information, no roll), inserted between "When not to roll" and "Saving throws."
  - `MM5_Quick_Reference.md` Magic quick ref — a new "### Adjudicating Magic (compressed from MM2 — see MM2 for full text)" subsection, six bullets compressing all four W3-10 topics (rule-out-loud habit, scope = scale + duration, pre-Technique ceiling, domain boundary substance-vs-rhyme, 7-9 complication categories, active-opposition floor) at quick-ref density, inserted right after the Second Domain bullet and before the pre-existing Magic 6- Templates subsection.
- **Fact-check pass:** verified the Threat Clock mechanic and "five or six party rolls" figure against III.2 (matches the figure I corrected myself in W1-6); verified the death-choice language against III.2's "When a Character Would Die" (scar named together by player and MM, heroic death's final action auto-succeeds, player's choice never the MM's); verified the Specialty bullet against II.5:51; verified the MM5 Adjudicating Magic compression against the actual W3-10 text now in the file (including the Easy-cell floor claim already fact-checked once in W3-10).
- No new mechanics — every line is a pointer to or compression of already-existing PHB/MM body text.
- INV-6 (typographic dashes) verified green.
- Regenerated `Index.md` — 4 new lines.

Command: `cd software && python -m pytest -q`
Result: **1044 passed**.

**Flagged for user sign-off (D12).**

### W3-15 — Wave 3 close-out

All 14 W3 tasks done. Final suite run before opening the PR:

Command: `cd software && python -m pytest -q`
Result: **1044 passed** (baseline was 1039; +5 across W3-1's and W3-3's TDD tasks).

Findings closed this wave: rul-H1, app-H1, app-H2, app-M1, app-M2, app-M3, app-M4, rul-M1, rul-L4, rul-M3, cre-M3, mm-L8, app-M7, mm-M3 (both parts), mm-M6 (both parts), mm-L9, mm-L2, mm-L3, cre-M6, cre-M7, rul-L5.

**Every DESIGN §6 sign-off item in this wave — none merged without being flagged here for review:**
- **W3-6** — new rule: pre-Technique casters can push to Significant scope with a Spark.
- **W3-8** — new canonical body text: the Trouble Table's MM2 home.
- **W3-9** — new canonical body text: "Unnarrated details" and "Can I try again?" in III.1.
- **W3-10** — the largest new-prose task of the cycle: MM2's "Adjudicating Magic" section. One factual inaccuracy in the initial draft (a misquoted established vignette) was caught during integration and corrected before commit — noted in the PR for extra scrutiny.
- **W3-11** — MM2/MM4 coverage pointers (hazards, death-as-consent) and MM5's Adjudicating Magic compression.
- **W3-13** — new framing prose: II.4a's missing Facet introduction.
- **W3-14** — two findings ruled as-designed in `DECISIONS.md` (cre-M7, rul-L5) — the user may veto either, which escalates to Brain.

**Model routing note:** all six prose sign-off tasks (W3-6, W3-8, W3-9, W3-10, W3-11, W3-13) were drafted by Opus subagents briefed with exact source citations, then fact-checked, reviewed, and integrated by this Sonnet session before commit — per the user's explicit direction earlier in this conversation. Every subagent draft was checked against its cited PHB/MM sources before landing; one inaccuracy was found and fixed (W3-10, see above).

PR: opened via `gh pr create` against `main`, branch `feature/audit-wave3-canon`.
