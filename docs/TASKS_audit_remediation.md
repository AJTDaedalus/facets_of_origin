# TASKS — Completeness Audit Remediation

**Tier:** Planner (Opus) output — Worker (Sonnet) executes
**Design:** `docs/DESIGN_audit_remediation.md` · **Brief:** `docs/BRIEF_audit_remediation.md`
**Log:** `docs/LOG_audit_remediation.md` (Worker creates on first task)
**Baseline:** 1026 tests green on `main` (DESIGN §1 S2).

## Worker protocol

1. Read only the DESIGN sections your task cites, plus the files the task names. Do **not** scan the repo.
2. Pick **one** task. TDD where code is involved: write the test, watch it fail, implement, watch it pass.
3. Do the task's **whole propagation set in one commit**. A partial propagation is a blocked task, not a done one.
4. Update this file (`[x]` done / `[!]` blocked) and append to `LOG_audit_remediation.md`: command run, result, pass/fail counts.
5. **Stop and report.** Do not start the next task without confirmation.
6. Escalate per DESIGN §7 after 2 failed attempts or on any Non-goal boundary.

**Wave rules**
- One branch and one PR per wave; branch from `main` only after the previous wave's PR merges.
- Any task touching `Glossary.md` or a heading regenerates `Index.md` (`cd software && python -m tools.build_index`) in the same commit — INV-4.
- Every PR description lists the finding IDs it closes and flags the DESIGN §6 sign-off items it contains.
- Never stage `adventures/`, `references/oraga_night/`, `playtest/07_*`, or `software/tools/run_oraga_night_playtests*.py`.
- Run the full suite before every commit; report the count.

---

## W0 — Land the plan

Branch: `docs/audit-remediation-plan` · PR title: `Commit audit corpus and remediation plan`

- [ ] **W0-1 — Commit the audit corpus and this plan.**
  Files: `docs/BRIEF_audit_remediation.md`, `docs/RESEARCH_completeness_audit.md`, `docs/RESEARCH_audit_phb_creation.md`, `_phb_rules.md`, `_phb_apparatus.md`, `_mm_manual.md`, `_software_sync.md`, `docs/DESIGN_audit_remediation.md`, `docs/TASKS_audit_remediation.md`.
  Use explicit `git add <file>` per file (CLAUDE.md git hygiene). Confirm `gh auth status` first.
  Accept: nine docs committed; `git status` shows the four out-of-scope untracked trees still untracked; suite unchanged at 1026.

---

## W1 — Mechanical corrections

Branch: `fix/audit-wave1-corrections` · Closes: cre-H1–H3, cre-M1, M2, M4, M5, cre-L1–L6, rul-M4, M5, rul-L1, L2, L3, L6, mm-M1, app-M5, M6, app-L1–L4, L6, README.
No canon judgment anywhere in this wave. If a fix seems to need one, escalate.

- [ ] **W1-1 — Create the LOG and record the baseline.**
  Files: `docs/LOG_audit_remediation.md`.
  Record: branch, date, `pytest --collect-only -q` count, and the wave's task list.
  Accept: file exists with the baseline count measured, not copied.

- [ ] **W1-2 — II.2 point-buy arithmetic and the Scholar's Luck.** *(cre-H1, cre-M1)*
  Files: `player_handbook/II.2_Character_Creation_Attributes.md:102, :118-121`.
  - `:102` — replace the illegal example with **four at 3, four at 1, one at 2** (4 spent, 4 saved, 1 at baseline = 18). Recompute the sentence; do not patch only the visible words.
  - `:118-121` — the stat line is correct (Luck 2, total 18). Fix the **prose**: the clause must stop claiming "Strong in Luck". Surgical edit, voice preserved (DESIGN §4.1).
  Accept: both examples arithmetically valid against the 18-point rule at `:98`; no other prose altered. Flag the `:121` wording in the PR for voice review.

- [ ] **W1-3 — "Each Facet's tree" → "the Mind and Soul trees"; drop the phantom Techniques.** *(cre-H2, cre-H3, cre-M4 — D1)*
  Files: `player_handbook/II.3_Magic.md:246`, `player_handbook/Glossary.md:90`, `player_handbook/II.3_Magic.md:93`.
  - `:246` and `Glossary:90` — the Techniques live in the Mind (Archive) and Soul (Communion) trees only. Do **not** add Body Techniques (D1, Non-goal).
  - `II.3:93` — the two illustrative Techniques ("ease Minor magic", "remove collateral") exist in no tree. Reword so the illustration cites Techniques that exist or drops the specifics; inventing an effect is out of bounds.
  Regenerate `Index.md`.
  Accept: no file claims a magic Technique in the Body tree; INV-3 and INV-4 green.

- [ ] **W1-4 — Soul Second Domain prerequisite line.** *(cre-M2)*
  Files: `player_handbook/II.4c_Character_Creation_Facet_Soul.md:134-135`.
  Add the prerequisite line its Mind twin carries (`II.4b:137-138`) and its own Ascendant Domain entry already carries (`II.4c:138`): requires an existing Soul domain (Spiritual Domain). Match the sibling's wording pattern.
  Accept: a Soul character cannot reach "second" domain without a first, per the text. Note in the LOG that W2-8 encodes the same guard in software.

- [ ] **W1-5 — Zulnut's Finesse and the Knowledge/Lore slip.** *(cre-M5)*
  Files: `player_handbook/II.4_Character_Creation_Facets.md:59, :73, :116, :120`.
  - `:59, :73` — the examples advance Finesse Novice→Practiced, but Zulnut has Finesse **Practiced at creation** (`characters/Zulnut.fof`, II.2:200). Swap the example skill to **Stealth** (Novice, 1 Background Mark). Recompute the whole example: Background Mark rule (II.5:43), 3-marks-per-rank (II.4:57), unspent-points-are-lost (II.4:53). Write the number you computed, not the number that was there.
  - `:116, :120` — "Knowledge rank ticks to Practiced" / "A Knowledge advancement": Knowledge is an attribute; the skill is **Lore**.
  Accept: every number in both examples recomputes correctly; no contradiction with `characters/Zulnut.fof`. Flag for voice review.

- [ ] **W1-6 — Threat Clock vignette and pacing math.** *(rul-M4, rul-M5)*
  Files: `player_handbook/III.2_Adventuring.md:19, :96`.
  - `:96` — a restarted 4-segment clock fills after 3 narrated advances. Add the missing fourth advance beat (do not redefine "restarting"; the first vignette at `:43-57` is correct and is the model).
  - `:19` — at a 72% advance rate a 4-segment clock takes 4 ÷ 0.72 ≈ 5.6 rolls. Keep 72%; replace "roughly 3–4 party rolls" with the correct figure.
  Accept: vignette shows four advances; the stated rate and the stated roll count agree. Flag the added beat for voice review.

- [ ] **W1-7 — Four small text corrections across III.3, IV.1, Quick Start, MM5.** *(rul-L1, rul-L2, rul-L3, rul-L6, mm-M1)*
  Files: `player_handbook/III.3_Combat.md:317`, `player_handbook/IV.1_Equipment.md:31-50` (or `III.3:287`), `player_handbook/Quick_Start.md:121-123`, `player_handbook/III.3_Combat.md:458-460`, `mm_manual/MM5_Quick_Reference.md:107`.
  - `III.3:317` — Named NPCs: acknowledge Tier 1 riders (canon at `:124` and quick ref `:677` allow Tier 1 **or** Tier 2).
  - `III.3:287` promises armor "Technique interactions" that IV.1 does not contain. **Trim the promise** — do not author content (Non-goal).
  - `Quick_Start.md:121-123` — the MM calls a peer "Spark?" call a Graceful Fail. Graceful Fail is player-claimed (III.1:72). Relabel to the peer call.
  - `III.3:458-460` — add a half-sentence grounding Mordai's Weapon Mastery (a later-campaign scene), so readers do not infer starting characters have Techniques.
  - `MM5:107` — Maneuver reverses canon: rolls **against** the target are Easy, **until the situation changes** (III.3:146). Restate as a compression of that line.
  Accept: MM5 line matches III.3 in direction and duration; INV-6 green; no new rule text anywhere.

- [ ] **W1-8 — Glossary: add Saving Throw, fix citations, close the term gaps.** *(app-M5, app-L1, app-L2/cre-L4, app-L3, app-L4)*
  Files: `player_handbook/Glossary.md`, then regenerate `player_handbook/Index.md`.
  - Add **Saving Throw** — compression of III.1:84-99 (2d6 + Major Attribute modifier), cited `*(Chapter III.1)*`.
  - `:12` and `:90` — use the `*(Chapter X.Y)*` format the other 52 entries use, and cite **both** homes for Ascendant Domain (II.4b, II.4c) and Second Domain (II.4b, II.4c).
  - Add standalone entries for **Winded**, **Off-Balance**, **Shaken** (Tier 2's Staggered/Cornered already have them), **Pinnacle Technique** (II.4), **Party Strength** (MM1), and one **Weapon** / equipment term (IV.1).
  - Every new entry is a compression of canonical text — no new rules.
  Accept: INV-3 (pointers resolve and contain the term) green; INV-4 green after regeneration; Index section count equals Glossary term count.

- [ ] **W1-9 — Index slugger: one hyphen per whitespace character.** *(app-M6)* **TDD**
  Files: `software/tools/build_index.py:110-113` (`_slugify`), `software/tests/test_build_index.py`, then regenerate `player_handbook/Index.md`.
  GitHub emits one hyphen per space; `re.sub(r"\s+", "-", slug)` collapses runs, so "Zahna — The Scholar" must anchor `#zahna--the-scholar`, not `#zahna-the-scholar`.
  Tests (3, written first): em-dash heading → double hyphen; a `+`-containing heading ("Magic: Domain + Intent + Scope"); a plain heading unchanged.
  Accept: 3 new tests pass; `python -m tools.build_index` regenerates; INV-4 green; the 33 previously-broken anchors now match their targets (spot-check 3 by hand and record them in the LOG).

- [ ] **W1-10 — Apparatus low-severity sweep.** *(cre-L1, cre-L2, cre-L3, cre-L5, cre-L6, app-L6)*
  Files: `player_handbook/Appendix_Magic_Domains.md:189`, `player_handbook/II.3_Magic.md:188, :223, :246`, `player_handbook/II.4b_…Mind.md:140-141`, `player_handbook/II.4c_…Soul.md:137-138`, `player_handbook/Table_of_Contents.md:13-15, :32-33`.
  - Appendix `:189` — "following the same structure as Soul" is false on counts (Soul 9+3, Mind 6+3). Fix the phrasing to claim only the core/prismatic split.
  - `II.3:188` — one-line forward pointer at the Domain Quick Reference that Body domains are deferred (the explanation at `:250-252` stays where it is).
  - `II.4b:140-141` / `II.4c:137-138` — state or point to the "Ascendant Domain is taken once" rule that currently lives only at II.3:246.
  - `II.3:188`/`:223` — the identical appendix-pointer sentence appears twice in a 35-line section; keep one.
  - ToC `:13-15` — chapter titles match the files' own titles; `:32-33` — either drop the A/B letters or add them to the appendix files (pick one and apply both ways).
  Regenerate `Index.md`.
  Accept: INV-5 and INV-7 green; INV-4 green.

- [ ] **W1-11 — README: regenerate every factual claim from canon.** *(README audit — D2 for the TR value)*
  Files: `README.md`.
  Correct, each verified against the source at the moment of the edit (DESIGN §1 S7):
  - "24 skills" → **15** (II.6).
  - "27 domains across three traditions (Resonance, Channeling, and one TBD)" → **21 domains** across **two** traditions (Resonance/Mind, Channeling/Soul); Body magic deferred to the Shattered Origin setting Facet.
  - "613 tests" (both occurrences, features list and project tree) → the count from `pytest --collect-only -q` **run in this commit**.
  - "Harbor Thug (Mook TR 1)" → **TR 2** (D2). "Archive Guardian (Boss TR 16)" → **TR 17**.
  - "Two simulated playtests" (features list **and** the roadmap checkbox) → the number of **committed** `playtest/` directories; `playtest/07_*` is untracked and does not count.
  - Add a one-line HTML comment above the claims block marking these figures as derived-from-canon and naming their sources, so future edits know to verify (BRIEF robustness item).
  Accept: every number traceable to a file you opened; note in the PR that the TR 2 claim states D2's decided value, which W2-4 makes true in MM1.

- [ ] **W1-12 — Wave 1 close-out.**
  Run the full suite; record the count in the LOG. Open the PR with `gh`; body lists every finding ID above and flags the DESIGN §6 voice-review items (W1-2, W1-5, W1-6).
  Accept: suite green; PR open; this file's W1 boxes all `[x]`.

---

## W2 — v0.3 migration completion

Branch: `fix/audit-wave2-v03-migration` · Closes: mm-H1, mm-M2, M4, M5, mm-L1, L4, L5, L6, L7, rul-M2, sync-H-1, sync-H-2.

- [ ] **W2-1 — Migrate Magic in Combat and Attune to the Resolve model.** *(mm-M2)*
  Files: `player_handbook/III.3_Combat.md:379, :391`; verify-only: `mm_manual/MM5_Quick_Reference.md:109`, `player_handbook/Quick_Start.md:143`.
  Against an enemy, a magical Strike uses the **same** table as a physical Strike (III.3:124): 10+ depletes 2 Resolve and may hang a rider; 7–9 depletes 1. Against another character, the PvP tier table applies. Do not invent a magic-specific number (DESIGN §4.2).
  Accept: no Condition-tier-only resolution survives in the Magic-in-Combat or Attune paragraphs; MM5:109 is now a legal compression (verify, do not rewrite); Quick Start unchanged or corrected if it states the old model.

- [ ] **W2-2 — Combat quick reference: declarable actions.** *(rul-M2)*
  Files: `player_handbook/III.3_Combat.md:646`.
  Body text defines three actions — Strike, Maneuver, Support (`:102-161`) — and magic uses the Strike action economy (`:375`). "Withdraw" is a **Posture** (step 1), not an action.
  Accept: step 2 lists only canonical actions; the quick ref introduces no wording the body text lacks.

- [ ] **W2-3 — MM1 enemy Attack/Defense modifiers: what they mean at the table.** *(mm-M4)*
  Files: `mm_manual/MM1_Encounters_and_Enemies.md:25-26, :197`.
  Remove "same modifier used for Parry" / "what they use to Parry" — NPCs do not roll (III.3:331). State only what canon already rules: the modifiers are authoring inputs feeding the TR formula and the simulator, and they inform the difficulty the MM sets for PC Strikes (III.3:114) and for reactions against enemy attacks (III.3:335-355).
  Accept: no MM1 text implies an enemy rolls dice; the replacement cites III.3 sections rather than asserting anything new. **Flag in the PR** (DESIGN §6).

- [ ] **W2-4 — Mook TR: the formula wins.** *(mm-H1 — D2)*
  Files: `mm_manual/MM1_Encounters_and_Enemies.md:55, :121, :293`, `enemies/harbor_thug.fof:29`.
  **First**, grep `TR 1`, `tr: 1`, `harbor_thug` across `mm_manual/`, `enemies/`, `spec/`, committed `playtest/` dirs, and `software/tests/`; paste the hit list into the LOG before editing.
  A +0-attack Mook is **TR 2** (offense 2 + durability 0). Fix the stat block, the table row, the `.fof` example block, and the `.fof`'s self-contradicting "TR 1 minimum by rule" note. `MM1:127`'s minimum-1 floor text **stays** — it is still correct for attack −2. The chicken remains the TR-1 baseline and is not renamed.
  Accept: no file claims a +0-attack Mook is TR 1; `harbor_thug.fof` is internally consistent; every hit from the grep list is either fixed or explained in the LOG; suite green.

- [ ] **W2-5 — Retire superseded simulation citations.** *(mm-M5, mm-L4, mm-L5)*
  Files: `mm_manual/MM1_Encounters_and_Enemies.md:411`, `mm_manual/MM2_Session_Design.md:165`, `enemies/veteran_soldier.fof:41-42`.
  - `MM1:411` cites Series 6/F, marked SUPERSEDED (v0.2 semantics) in `research/simulation_log.md:365`. Remove the citation or re-source it to the current Recipe-Table numbers (`MM1:341-348`) — do not re-run simulations (DESIGN §5).
  - `MM2:165` defines a Skirmish by the deprecated ×1 TR budget; the current definition is a Mook-only roster.
  - `veteran_soldier.fof:41-42` — stale pre-Series-9 solo-difficulty note contradicting MM1's actor-count doctrine (`MM1:136, :363`). Delete or correct.
  Accept: no superseded series is cited as evidence anywhere; superseded sections in the simulation log stay labeled and untouched.

- [ ] **W2-6 — MM low-severity sweep.** *(mm-L1, mm-L6, mm-L7)*
  Files: `mm_manual/MM3_Campaign_Design.md:218`, `mm_manual/MM1_Encounters_and_Enemies.md:220, :176-185`.
  - MM3 Level-2 row claims "a second and third Technique"; Level 2 grants only the second (II.4: one per Facet level).
  - MM1:220 "(see *Armor*, above)" has no target section — point at the real referent (`MM1:107` TR armor bonus, or the stat-block note at `:27`).
  - MM1:176 "three things" vs the four-step build list at `:180-185` — make the count match the list.
  Accept: INV-6 green; no rules text changed, only counts and pointers.

- [ ] **W2-7 — facet.yaml: Overwhelming Force.** *(sync-H-1)* **TDD**
  Files: `software/facets/base/facet.yaml:294-299`, `software/tests/` (facets/schema or a docs-consistency case).
  Replace the pre-v0.3 rule ("succeed by 3 or more … staggered … act last … no reactions") with II.4a:39-40: **once per scene**, on a **10+** Strike against a single target, the target takes **no offensive action** in the next exchange.
  Tests (2, written first): the yaml description carries the once-per-scene limit and the 10+ trigger; no `"3 or more above the threshold"` string survives anywhere in `facet.yaml`.
  Accept: 2 tests pass; full suite green; commit message cites PHB II.4a.

- [ ] **W2-8 — Encode the magic-Technique domain prerequisite (the guard).** *(sync-H-2, part 1)* **TDD**
  Files: `software/app/facets/schema.py` (`TechniqueDef`), `software/facets/base/facet.yaml` (`second_domain`, `second_domain_mind`, `ascendant_domain_soul`, and the Mind Ascendant entry), `software/app/game/character.py`, `software/tests/test_character.py`.
  Today "requires an existing domain" is satisfied only as a side effect of the strict prerequisite chain (sync report H-2 note). Encode it explicitly — a `requires_domain` (Facet id) field on `TechniqueDef`, enforced in the selection path — **before** W2-9 loosens the chain.
  Tests (3, written first): Second Domain refused with no domain; permitted with one; Ascendant Domain likewise.
  Accept: 3 tests pass with the old chain still in place; suite green. Do **not** touch the prerequisite lists in this task.

- [ ] **W2-9 — Switch to the PHB's branch/tier prerequisite rule.** *(sync-H-2, part 2)* **TDD**
  Files: `software/app/game/character.py:338`, `software/facets/base/facet.yaml` (Tier 2/3 `prerequisites` lists), `software/tests/test_character.py`.
  PHB II.4:83 — Tier 2 requires **any** Tier 1 in the same branch; Tier 3 requires **any** Tier 2 in the same branch. Enforce that rule in code; empty the per-Technique chain lists in the base yaml where they encoded nothing but the chain (keep the `prerequisites` field in the schema for homebrew Facets).
  Tests (7, written first) — DESIGN §4.2 lists them exactly: 2 newly-legal picks, 1 second-tree mirror, and 4 that must still be refused (no Tier 1 in branch; cross-branch Tier 1; Tier 3 with only Tier 1; Second Domain with no domain).
  Accept: all 7 pass; full suite green; no test outside the advancement area changes behaviour. If an unlisted test breaks, **escalate** (DESIGN §7).

- [ ] **W2-10 — Wave 2 close-out.**
  Full suite; count in the LOG; PR via `gh` listing finding IDs and flagging W2-3.
  Accept: suite green; PR open.

---

## W3 — Canon-decision items

Branch: `feature/audit-wave3-canon` · Closes: rul-H1, rul-M1, M3, rul-L4, app-H1, H2, app-M1–M4, M7, cre-M3, M6, M7, mm-M3, M6, mm-L2, L3, L8, L9, rul-L5.
**Highest canon risk of the cycle.** Every new-prose task ends with a draft to the user before merge (D12).

- [ ] **W3-1 — Guild Apprentice gets its Specialty (three-way propagation).** *(rul-H1 — D4; DESIGN §1 S1)* **TDD**
  Files: `player_handbook/II.5_Character_Creation_Backgrounds.md:187-197`, `software/facets/base/facet.yaml:1424`, `software/tests/`.
  Adopt the user-established Quick Start text verbatim: *"Artificers' Guild technical records — Standard becomes Easy when directly applicable"* (`Quick_Start.md:36`). **The yaml currently carries a third, different specialty string** ("Formal training in a structured discipline…") — it is replaced, not merged.
  Tests (2, written first): the yaml specialty for `guild_apprentice` equals the II.5 text; all 15 Backgrounds have a non-empty specialty in both II.5 and yaml.
  Accept: II.5's five-elements claim (`:15`) holds for all 15; Quick Start, II.5, and yaml agree word-for-word.

- [ ] **W3-2 — Amend II.1's character sheet specification.** *(app-H1, H2, M1–M4 — D7, part 1)*
  Files: `player_handbook/II.1_Character_Creation_Overview.md:11-24`.
  Nine sections (DESIGN §4.3 table): Attributes, Facet (relabelled to **rank advances**, plus **Career Advances**), Background (Secondary Skill **or Domain Origin**), Skills, Techniques, **Magic** (new), **Combat** (new — Endurance, Armor + downgrade budget, Conditions; **Sparks moves here**), **Inventory** (new), Session Resources (keeps Skill Points).
  Update the "six sections" count at `:11`.
  Accept: the section table and the count agree; nothing describes a rule the PHB doesn't already state.

- [ ] **W3-3 — Rebuild the character sheet appendix to the amended spec.** *(D7, part 2)* **TDD**
  Files: `player_handbook/Appendix_Character_Sheet.md`, `software/tests/test_docs_consistency.py` (`CHARACTER_SHEET_FIELDS`).
  Mirror W3-2 exactly. Print the Endurance formula (4 + Constitution modifier + Endurance rank) beside the Endurance row. Update `:3`'s "six sections" claim.
  Field mapping (DESIGN §1 S3 — every one already exists on `Character`): Endurance → `endurance_current`; Armor type → `armor`; downgrade budget → `armor_downgrades_remaining`; Conditions → `conditions`; Magic Domain → `magic_domain`; Inventory → `inventory`; Career Advances → `career_advances`; the relabelled advancement row stays → `rank_advances_this_facet_level`.
  **Add no new `Character` field.** If a label seems to need one, escalate (DESIGN §7).
  Tests: INV-2 updated and green; 1 new assertion that every new section label maps to a real model attribute.
  Accept: Zahna (`characters/Zahna.fof`) transcribes onto the sheet with nothing lost — verify by hand and record the transcription in the LOG. Suite green.

- [ ] **W3-4 — 0 Endurance means Absorb only, absolutely.** *(rul-M1, rul-L4 — D5)* **TDD**
  Files: `player_handbook/III.3_Combat.md:45, :87-88, :167, :718`, `mm_manual/MM5_Quick_Reference.md:199-202`, `software/facets/base/facet.yaml` (`combat.endurance_floor_rule`), `software/app/game/combat.py`, `software/tests/test_combat.py`.
  - Body text gains one clarifying sentence at `:167`: at 0 Endurance only Absorb is available **regardless of posture**; Withdrawn's free reactions and Defensive's cost reduction apply only while Endurance ≥ 1.
  - `:718` quick ref currently says Conditions "land at full tier" — wrong for an armored character (`:47`: armor still helps). Correct the compression.
  - Encode the rule in `combat.endurance_floor_rule` (the schema field already exists) and have the engine read it.
  Tests (3, written first): Dodge refused at 0 Endurance while Withdrawn; refused while Defensive; Absorb permitted.
  Accept: text, quick refs, yaml, and engine all state the same rule in one commit. If the engine already refuses, keep the tests as regressions and say so in the LOG.

- [ ] **W3-5 — Cut Reckless Press.** *(rul-M3 — D6)*
  Files: `player_handbook/III.3_Combat.md:395`; verify-only: repo-wide grep for "Reckless".
  Rewrite the Gamble entry to reference the plain Spark rule (III.1:76 — spend a Spark, add 1d6, drop the lowest). A named mechanic must earn its name.
  Accept: "Reckless Press" appears nowhere in the repo; the Gamble entry states no mechanic the Spark rule doesn't already give.

- [ ] **W3-6 — Redefine pushing scope against the pre-Technique cap.** *(cre-M3, mm-L8 — D8)*
  Files: `player_handbook/II.3_Magic.md:170`, `mm_manual/MM5_Quick_Reference.md:208-217`.
  New rule: a **pre-Technique** caster may spend a Spark to attempt a single **Significant**-scope effect at their domain's normal Significant difficulty. The Tier 1 Technique remains the only route to routine full scope and to Major. Focused-domains-Spark-to-ease-Major is unchanged; the Broad/prismatic ceiling stays immovable.
  MM5 then lists all three Spark-magic rules (closing mm-L8) and adds II.4c:135's "standard domains only" note on Second Domain.
  Accept: the rule has a real referent (the II.3:229 Minor cap); MM5 is a compression of the new body text, written after it. **Sign-off item** — flag in the PR. W4-9 encodes it.

- [ ] **W3-7 — The Shattered Origin promise, both fixes.** *(app-M7 — D9)*
  Files: `player_handbook/I_Introduction.md:29`, `player_handbook/Table_of_Contents.md:51-58`.
  - Soften `:29`: the handbook is *set in* Shattered Origin; the full setting Facet is forthcoming.
  - Add **"Shattered Origin (setting Facet)"** to the ToC's planned-modules list, giving II.3:252's Body-magic deferral a destination.
  Regenerate `Index.md`.
  Accept: INV-5 green; no chapter is promised that does not exist or is not marked planned.

- [ ] **W3-8 — Give the Trouble Table a canonical home.** *(mm-M3, part 1 — D3)*
  Files: `mm_manual/MM2_Session_Design.md` (Improvisation section — DESIGN §2.3), `mm_manual/MM5_Quick_Reference.md:284-293`, then regenerate `Index.md`.
  Write the d6 table into MM2 as canonical body text; MM5's version becomes a compression pointing at it.
  Accept: the table's canonical home is a body chapter, not a quick ref; Index links resolve to the new home after regeneration. **Sign-off item** — draft to the user before merge.

- [ ] **W3-9 — Two Common Rulings into III.1.** *(mm-M3, part 2 — D3)*
  Files: `player_handbook/III.1_Core_Resolution.md` (near `:129`), `mm_manual/MM5_Quick_Reference.md:299, :302`, then regenerate `Index.md`.
  Write **"Unnarrated details"** (players cannot act on details the MM has not described) and **"Can I try again?"** (only if the fiction changes — new approach, new information, or time passes) as canonical III.1 text; MM5 compresses.
  If the user rejects either as non-canon, delete it from MM5 instead (D3's stated exception).
  Accept: neither rule exists only in a quick ref; INV-4/INV-5 green. **Sign-off item.**

- [ ] **W3-10 — MM2: "Adjudicating Magic".** *(mm-M6 — D10, part 1)*
  Files: `mm_manual/MM2_Session_Design.md` (new top-level section), then regenerate `Index.md`.
  Four topics, each a compression of existing PHB rules into MM-facing guidance — no new mechanics: scope classification (II.3:43-49), domain boundary calls with the "lean toward yes" posture (II.3:25), designing 7–9 complications (II.3:124-140 templates), active-opposition difficulty (III.3:381).
  Accept: every paragraph traceable to a PHB rule you cite in the LOG; the manual keeps its five-chapter shape. **Sign-off item — draft to the user before merge.**

- [ ] **W3-11 — MM coverage pointers + MM5 compression of the new section.** *(mm-M6, mm-L9 — D10, part 2)*
  Files: `mm_manual/MM5_Quick_Reference.md` (Common Rulings + a magic-adjudication compression), `mm_manual/MM2_Session_Design.md` (hazard/Threat Clock pointers to III.2), `mm_manual/MM4_Running_the_Table.md` (safety section → III.2's death choice), then regenerate `Index.md`.
  Specialty ruling into MM5 Common Rulings, compressing II.5:49-51 (directly applicable → Standard becomes Easy; tangential → free information). Pinnacle-approval guidance stays **deferred** (open blocker, Non-goal).
  Accept: MM5 compresses only text that now exists; INV-6 green. **Sign-off item.**

- [ ] **W3-12 — MM5 Spark-economy drift.** *(mm-L2, mm-L3)*
  Files: `mm_manual/MM5_Quick_Reference.md:57-63, :74`; source: `mm_manual/MM2_Session_Design.md:493-536`.
  - `:59` mid-session Graceful Fail timing and `:61`'s **earned**-by-midpoint diagnostic both diverge from MM2 (which targets 1–2 GF per session and diagnoses on **spending**). `:62-63` is guidance with no MM2 source.
  - `:74` "earn 2–4" vs MM2's 1–2 / 2–3 / 3–4 table.
  Compress MM2; do not invent a diagnostic.
  Accept: every MM5 Spark line traces to an MM2 line; INV-6 green.

- [ ] **W3-13 — II.4a gains its Facet introduction.** *(cre-M6)*
  Files: `player_handbook/II.4a_Character_Creation_Facet_Body.md:1-3`; models: `II.4b:3-7`, `II.4c:3-5`.
  Add a "## The Body Facet" section parallel to its siblings — framing prose only, drawn from II.4:13 and the existing Body material. No new mechanics.
  Regenerate `Index.md` (new heading).
  Accept: the three Facet chapters open the same way; INV-4 green. **Sign-off item** — new prose in the book's voice.

- [ ] **W3-14 — Rule two findings as-designed.** *(cre-M7, rul-L5)*
  Files: `docs/DECISIONS.md`.
  - **cre-M7** — Communion Tier 3 offers one fewer non-magic pick than Archive. Fixing means authoring a Technique (Non-goal). Record as accepted, noting both trees offer the same Tier 3 *count* once magic Techniques are included.
  - **rul-L5** — no pre-built Background grants Survival. Fixing means changing a Background's skill grant (content change with yaml/test/pre-gen knock-on). Record as accepted; the custom path (II.5:83) covers it.
  Accept: both entries name the finding ID, the rationale, and the alternative rejected. **Sign-off item** — the user may veto either, which escalates to Brain.

- [ ] **W3-15 — Wave 3 close-out.**
  Full suite; count in the LOG; PR via `gh` listing finding IDs and **every** DESIGN §6 sign-off item in this wave (W3-6, W3-8, W3-9, W3-10, W3-11, W3-13, W3-14).
  Accept: suite green; PR open; no new-prose task merged without recorded user sign-off.

---

## W4 — Sync backlog

Branch: `feature/audit-wave4-sync` · Closes: sync-M-1 … M-12, sync-L-1 … L-8.
Every task follows the sync workflow: yaml → schema model → engine → WebSocket → tests → commit citing the PHB section. Depth per D11 / DESIGN §2.4. M-3 through M-7 **must not change behaviour** — they move literals into data.

- [ ] **W4-1 — Press cost into yaml.** *(sync-M-2)* **TDD**
  Files: `software/facets/base/facet.yaml` (`combat.press`), `software/app/facets/schema.py` (`CombatDef.press` already exists — give it a typed model), `software/app/api/websocket.py:528-534`, `software/tests/test_websocket.py`.
  Encode cost 1 Endurance + the add-a-die/drop-lowest effect (III.3:132); the handler reads the ruleset instead of the hardcoded literal.
  Tests (3): cost read from yaml; a modified yaml cost changes the deduction; insufficient Endurance still refuses.
  Accept: no Press cost literal remains in `websocket.py`; suite green.

- [ ] **W4-2 — Strike riders and Easy-to-Strike into yaml.** *(sync-M-3)* **TDD**
  Files: `facet.yaml` (`combat.strike_outcomes` / `enemy_durability`), `schema.py`, `software/app/game/combat.py:512, :543-547`, `software/tests/test_combat.py`.
  Encode: 10+ may hang a Tier 1 or Tier 2 rider; a Tier 2 rider makes the enemy Easy to Strike until cleared; riders never defeat (III.3:124, quick ref :675-681).
  Tests (3): rider tiers sourced from yaml; Tier 2 rider yields the Easy-to-Strike state; a rider never reduces Resolve to defeat.
  Accept: behaviour identical to today; suite green.

- [ ] **W4-3 — Same-Tier-2 escalation into yaml.** *(sync-M-4)* **TDD**
  Files: `facet.yaml` (`combat.conditions`), `schema.py`, `software/app/game/combat.py:536, :552-553`, `software/app/api/websocket.py:747`, tests.
  Encode III.3:254 — a second Tier 2 Condition **of the same type** escalates to Broken.
  Tests (3): same-type → Broken; different-type → coexist; rule read from yaml, not a literal set.
  Accept: no hardcoded Tier 2 id set survives in either consumer.

- [ ] **W4-4 — Armor/reaction non-stacking into yaml.** *(sync-M-5)* **TDD**
  Files: `facet.yaml` (`combat.armor`), `schema.py`, `software/app/game/combat.py:131-137`, tests.
  Encode III.3:357-363 — downgrades do not stack (apply the greater); when the reaction supplies the reduction the armor charge is **not spent**.
  Tests (3): non-stacking; charge preserved; charge spent when armor alone supplies it.

- [ ] **W4-5 — Enemy attack rules into yaml.** *(sync-M-6)* **TDD**
  Files: `facet.yaml` (`combat.enemy_attacks`), `schema.py`, engine/WS read path, tests.
  Encode III.3:333-355 — incoming tier by enemy type (Mook 1, Named 2, Boss 2); Named/Boss posture shifts PC reaction difficulty (Aggressive one step harder, Defensive one step easier); Mooks declare no posture.
  Tests (3): tier by type from yaml; posture shift applied; Mook posture ignored.

- [ ] **W4-6 — Maneuver and Support into yaml.** *(sync-M-7)* **TDD**
  Files: `facet.yaml` (`combat.actions`), `schema.py`, `software/app/api/websocket.py:886-961`, tests.
  Encode III.3:141-161 — Maneuver 10+/7–9/6−; Support grants +1d6-drop-lowest **or** one difficulty step, next roll only, non-stacking (most recent applies).
  Tests (3): Maneuver outcomes from yaml; Support's two modes; non-stacking replacement.

- [ ] **W4-7 — Major Attribute modifier derivation.** *(sync-M-8, part 1)* **TDD**
  Files: `facet.yaml` (`attributes.major_derivation`), `software/app/facets/schema.py` (`AttributesDef`), `software/app/game/character.py`, `software/tests/test_character.py`.
  Encode II.2:106-113 — minor sum 3–4 → −1, 5–7 → +0, 8–9 → +1 — and add the derivation to `Character`.
  Tests (4): each of the three bands, plus an out-of-range guard.

- [ ] **W4-8 — Saving throws: engine + WebSocket.** *(sync-M-8, part 2 — D11 full depth)* **TDD**
  Files: `facet.yaml` (`roll_resolution.saving_throw`), `schema.py`, `software/app/game/engine.py`, `software/app/api/websocket.py`, `software/tests/test_roll_engine.py`, `software/tests/test_websocket.py`.
  III.1:84-99 — 2d6 + the Major Attribute modifier from W4-7, resolved on the standard three-tier table.
  Tests (3): engine path; WS event happy path; WS error on an unknown Major Attribute.
  Accept: a saving throw is rollable end-to-end; the modifier comes from W4-7's derivation, not a second implementation.

- [ ] **W4-9 — Spark scope fuel into yaml, including D8.** *(sync-M-9)* **TDD**
  Files: `facet.yaml` (`magic.spark_rules`), `schema.py` (`MagicDef`), `software/app/game/engine.py:230-256`, tests.
  Encode all three: Focused may Spark a Major from Hard → Standard; the Broad/prismatic ceiling is immovable; **D8** — a pre-Technique caster may Spark to attempt one Significant-scope effect at the domain's normal Significant difficulty (W3-6's body text is the source).
  Tests (4): Focused ease-Major; Broad refusal; D8 push permitted pre-Technique; Major still refused pre-Technique.
  Accept: `push_scope` is rewritten against the yaml, not extended in place; commit cites PHB II.3.

- [ ] **W4-10 — Group rolls and contested rolls: encoding only.** *(sync-M-10, M-11 — D11)* **TDD**
  Files: `facet.yaml` (`roll_resolution.group_roll`, `roll_resolution.contested_roll`), `schema.py`, `software/tests/test_facets_schema.py`.
  Encode III.1:104-123 — contested: vs NPC only the PC rolls (the NPC informs difficulty), PC-vs-PC both roll, higher wins, tie = both partial. Group: majority success, partial counts; lead roller + Support alternative.
  No engine work: the contested handler already exists (`websocket.py:970-1025`) and group rolls wait for a playtest to demand them (D11).
  Tests (≥2): both blocks load and validate; the contested handler's tie rule matches the yaml text.

- [ ] **W4-11 — Weapon category → attribute table.** *(sync-M-12)* **TDD**
  Files: `facet.yaml` (`equipment.weapon_categories`), `schema.py`, `software/tests/test_facets_schema.py`.
  Encode IV.1:13-19 — Heavy = Strength; Standard = Str or Dex; Light = Dex; Ranged = Dex; Unarmed = Str or Dex. The engine stays permissive on Strike attributes (deliberate); this is reference data.
  Tests (≥2): the block loads; all five categories present with their attributes.

- [ ] **W4-12 — First Move timing.** *(sync-M-1)*
  Files: `software/facets/base/facet.yaml:569-574`.
  PHB II.4b:96 — the effect governs **this** exchange, not the next, and includes the ambush/trap-negation clause. Restore both.
  Accept: the yaml description matches the PHB sentence in timing and scope; add a text assertion if one is cheap.

- [x] **W4-13 — Sync low-severity sweep.** *(sync-L-1 … L-8)*
  Files: `software/facets/base/facet.yaml`, `software/app/facets/schema.py`.
  - L-1 Spark earn methods: add the "Spark?" peer call (III.1:70); reconcile `spark_for_weakness` with III.1's folding of weakness-play into the MM award.
  - L-2 Tier 1 Conditions clear at end of scene **out of combat** (III.2:69).
  - L-3 Intercept once-per-exchange limit (III.3:219).
  - L-4 Defensive "min 0" clamp as an explicit field.
  - L-5 `second_domain` / `second_domain_mind` id asymmetry — rename only if nothing outside yaml/tests references the id; otherwise record as accepted in `DECISIONS.md`.
  - L-6, L-8 description drift: restore the PHB clauses the yaml trims (Luck and five other minor attributes; Grinding Advance, Sharp Analysis, Commanding Presence, Unforgettable).
  - L-7 domain acquisition limits (II.3:244-246: one domain per Facet via cross-training, Ascendant once ever, prismatics never a starting domain).
  Accept: each item either fixed or recorded as accepted with a reason; suite green.

- [ ] **W4-14 — Cycle close-out.**
  Full suite; final count in the LOG. PR via `gh` listing finding IDs. Then append a cycle summary to `docs/LOG_audit_remediation.md`: findings closed, findings ruled as-designed, findings deliberately left (app-L5), and the final test count against the 1026 baseline.
  Accept: every High and Medium finding in the audit is either fixed or has a `DECISIONS.md` entry (BRIEF Goal 1); PR open.

---

## Coverage check

| Severity | Total | Fixed by a task | Ruled as-designed | Logged only |
|---|---|---|---|---|
| High | 9 | 9 | 0 | 0 |
| Medium | 37 | 36 | 1 (cre-M7) | 0 |
| Low | 35 | 33 | 1 (rul-L5) | 1 (app-L5, correct as-is) |
| README | 1 | 1 | — | — |
