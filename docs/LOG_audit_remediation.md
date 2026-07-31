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
- [ ] W2-9 — Switch to the PHB's branch/tier prerequisite rule. *(sync-H-2, part 2)* **TDD**
- [ ] W2-10 — Wave 2 close-out.

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
