# Session Handoff: PHB/MM Editorial Pass — Commit + Follow-Up Work

**Date:** 2026-07-11
**Project:** /root/facets_of_origin (branch: `main`, HEAD 902a33c)
**Session:** Publisher-grade editorial review of PHB + MM manual, then full application of fixes.

## Current State

**Task:** Editorial review → fixes applied → follow-up work remains.
**Phase:** Review/fixes COMPLETE and committed as `249701f` on branch **`fix/editorial-pass`** (27 files). Not yet pushed; no PR yet.
**Tests:** `cd software && python -m pytest -q` → **965 passed, 1 failed**. The failure (`tests/test_config.py::test_default_port_is_8000`) is pre-existing and environment-caused (local `.env` sets `PORT=8010`) — tracked as `docs/TODO.md` T4. Do not "fix" it as part of this work.

## What We Did

1. Full editorial review of all 16 PHB files + MM1–MM5 against published-book standards → `docs/RESEARCH_editorial_review.md` (findings F1–F21 + section D production gaps).
2. Applied every technical fix (rules contradictions, stat-block math, vignette math, cross-book consistency) across PHB, MM manual, `facet.yaml`, `characters/Zahna.fof`, `enemies/archive_guardian.fof`, and one API test.
3. Light prose de-patterning pass on both books (owner chose "light" over "deep"): thinned "It is not X. It is Y." reframes, cut stacked kicker lines, broke anaphora triples, varied "This is deliberate" self-commentary, normalized MM punctuation to real em/en dashes.
4. Closed TODO T1 (armor-charge consumption now in III.3 + MM5). Updated project memory and the review doc's fixes-applied addendum.

## Decisions Made (owner rulings — do not relitigate)

- **Prismatic access = Ascendant Domain** — new Tier 3 Technique in Archive (Mind) and Communion (Soul) branches grants one prismatic domain; Second Domain is now standard-domains-only. Chosen over Second-Domain-extension (difficulty stacking made everything Very Hard) and over MM-approval-only (breaks the "Technique = mechanical activation" pattern).
- **Magic Backgrounds: domain REPLACES secondary skill** — the II.5 rule stands; Zahna/Quick Start/Temple Acolyte/facet.yaml/tests corrected to match. The engine already had `domain_replaces_secondary: true` for Guild Apprentice + Hedge Scholar; Temple Acolyte was missing it (added), and a test asserting "keeps both" was inverted to codify the ruling.
- **Prose: light de-patterning only** — voice must survive. See memory `feedback_prose_human_voice.md`. Load-bearing antitheses and vignette flourishes stay ("That is not a failure. That is Tuesday.").
- **Reduced Mode blows land Tier 1** — added to the Guardian phase (MM1, `.fof`, III.3 example) so the flagship combat example follows its own rules (Mordai's Absorb now takes Winded).

## Code/Content Changes (all uncommitted)

- `player_handbook/IV.1_Equipment.md` — armor rewritten from stale tier-shift model to III.3's per-scene downgrade budget; Strike text now Resolve-aware. **The most important fix.**
- `player_handbook/III.3_Combat.md` — armor-charge rule added; veteran soldier rank label; vignette math (Lore +1, Aggressive +1 ×3); Absorb example lands Winded; glyph Hard call re-justified via Inscription slow-craft; Withdrawn quick-ref cell "Free (0)"; prose pass.
- `player_handbook/II.4_Character_Creation_Facets.md` — **Overwhelming Force rewritten** (was margin-of-success + turn order, now: once/scene, 10+ Strike → target takes no offensive action next exchange).
- `player_handbook/II.4b_..._Mind.md` — **First Move rewritten** (exchange-native pre-emption); **Ascendant Domain added** (Archive Tier 3).
- `player_handbook/II.4c_..._Soul.md` — Second Domain standard-only; **Ascendant Domain added** (Communion Tier 3).
- `software/facets/base/facet.yaml` — `ascendant_domain_mind` (prereq `cross_reference`), `ascendant_domain_soul` (prereq `the_language_beneath_language`), second_domain prompt updated, temple_acolyte `domain_replaces_secondary: true`.
- `software/tests/test_api.py` — Temple Acolyte test inverted + no-domain companion test added.
- `characters/Zahna.fof` — Investigate secondary removed; stale "one step harder" pre-technique note fixed.
- `enemies/archive_guardian.fof` — attack/defense breakdown comments now sum; Reduced Mode Tier 1 line.
- `mm_manual/MM1` — Guardian stat-block math; phase text; prose. `MM2` — enemy-Endurance stale line → Resolve; Spark units; prose. `MM3` — "Analytical Eye"→Sharp Analysis; career bands aligned to II.4 (0–2/3–5/6–10/11–15/16+); prose. `MM5` — magic row attribute-only; armor-charge line; MM-award row in Spark table; `--`/`->` → proper dashes/arrows.
- Small fixes: II.1, II.2, II.3, II.5 ("five elements", Temple Acolyte format, Lore commentary), II.6, III.1, III.2 (Tier 1 duration), I_Introduction, Quick_Start (Zahna skills, Zulnut "(custom)"), Appendix (Core vs Standard headings, Ascendant naming), `docs/TODO.md` (T1 struck).
- New file: `docs/RESEARCH_editorial_review.md` (full findings + fixes-applied addendum — **the authoritative record; read it first**).

## Needs Owner Review (only new mechanical wording in the pass)

- [ ] **Overwhelming Force** (`player_handbook/II.4_Character_Creation_Facets.md`, Might Tier 2) — power level: once/scene, denies the target's next offensive action.
- [ ] **First Move** (`II.4b`, Instinct Tier 3) — party's actions resolve before any opposition act this exchange.
- [ ] **Ascendant Domain** text (II.4b/II.4c/facet.yaml) — implements the owner's chosen option; wording is mine.

## Next Steps

1. [x] **Commit + push + PR.** Done: commit `8b8dc58` on `fix/editorial-pass` (the earlier `249701f` was rewritten into this hash), pushed 2026-07-11, PR #7 open against `main` (https://github.com/AJTDaedalus/facets_of_origin/pull/7). Test suite re-verified before push: 965 passed, 1 pre-existing env failure (TODO T4). Playtest RNG-churn log reverted after the run.
2. [ ] **Production apparatus** (section D of the review doc — the actual follow-up work, roughly in order):
   - Glossary of game terms (~30 terms: Spark, Exchange, Posture, Resolve, rider, Threat Clock, mark, career advance, Specialty, scope tiers…)
   - Index / bidirectional cross-reference layer
   - Character sheet appendix (II.1 describes six sections; no sheet exists)
   - Chapter renumbering: II.4/II.4b/II.4c → II.4 (shared advancement) + II.4a/b/c (trees); update ToC
   - Skill-text dedup: make II.6 canonical, Facet chapters point to it
   - Branch intro paragraphs for Body + Soul trees (Mind has them, others don't)
   - Standardize vignette roll markers (`→` in PHB vs `>` in MM2/MM4)
   - Front matter: credits/license page, "how to read this book", pointer to Quick Start for true novices
   - Decide III.2's fate for print (46 lines: grow with a vignette, or fold into III.1/III.3)
3. [ ] Optional deferred: **deep prose rewrite** of the most rhetorical sections (MM4 philosophy opening, chapter intros) — owner explicitly deferred this; ask before doing it.

**Tier guidance (per ~/.claude/CLAUDE.md):** step 2 is Planner (Opus) to spec the apparatus (a DESIGN/TASKS pair would fit), then Worker (Sonnet) execution. Prose-sensitive items (front matter, branch intros, III.2 growth) lean Brain/Fable — they create new canonical text and voice matters.

## Context to Remember

- **Never invent lore/mechanics** the owner hasn't established — ask. Both open design calls this session went through explicit owner rulings.
- **Quick refs are compressions, not paraphrases** — any rules change updates body text + every quick ref + `facet.yaml` + engine in the same commit.
- **Prose bar: "no one could tell it's AI"** — patterns to avoid are listed in memory `feedback_prose_human_voice.md`. Light touch; the dry/warm no-contraction voice is deliberate.
- The simulator may only drive `app/game/combat.py`; TDD applies to all software changes.
- Running the full test suite regenerates `playtest/02_silence_of_ashenmoor/digital_tool_log.md` (RNG churn) — revert before committing.

## Files to Review on Resume

- `docs/RESEARCH_editorial_review.md` — full findings, rulings, fixes-applied addendum (read first)
- `docs/TODO.md` — T2/T3/T4 remain open (UI Condition control, strike-path divergence, env-sensitive test)
- `git status` / `git diff` — the uncommitted pass itself
- `player_handbook/II.4*.md` — the three owner-review Technique texts
