# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Facets of Origin** is a digital-first, open-source TTRPG built around a clear design philosophy:

**Prioritize:** fun, socializing, worldbuilding, and storytelling
**Minimize:** rules complexity, complicated mechanics, and gameplay friction

It is explicitly designed so that the rules never get in the way of the story or the people at the table. The digital toolset exists to handle complexity so players don't have to.

Three pillars:
1. A lightweight, accessible ruleset that works for any experience level
2. Software tools for online sessions, character creation, adventure creation, and ruleset expansion — the digital layer absorbs bookkeeping so humans can focus on narrative
3. An open-source (GPLv3) foundation for community participation and homebrew

The project is in early development — the toolset, ruleset, and example adventure are all on the roadmap but not yet implemented.

## Information Recording Principles

This document uses **progressive disclosure** architecture to optimize LLM working efficiency.

**Level 1 (this file)** contains: core rules, iron laws, key patterns, directory mapping, and trigger indexes to Level 2.

**Level 2 (`references/`)** contains: detailed character descriptions, full skill tables, extended examples, and SOPs.

When adding new information: high-frequency or high-consequence content goes in Level 1; detailed reference material goes in Level 2 with a trigger condition in Level 1 pointing to it.

## Reference Index

| Trigger | Reference File | Contents |
|---|---|---|
| Writing PHB examples or vignettes | `references/phb-examples.md` | Character personalities, formatting conventions, ground rules, established scenarios |
| Choosing a skill/tool for a task | `references/skills-reference.md` | Full skill tables by category with source and usage context |
| Using World Anvil MCP or WA API | `references/worldanvil-mcp.md` | Working config, common pitfalls, verification steps |

---

## Research Reference

The `research/` directory contains foundational documents that should inform all design decisions. **Always consult relevant research files before proposing mechanics, systems, or content.**

- `research/dice_system_analysis.md` — Synthesis of TTRPG market landscape and psychology of fun/dice/social bonding. Covers: why 2d6 three-tier outcomes are optimal, the Spark system recommendation, market gaps, what competing games do well and poorly, and five open design questions that need resolution before detailed system work begins.

When proposing anything related to dice mechanics, resolution systems, player experience, onboarding, or digital design, check this file first — the recommendations are grounded in academic psychology research and market analysis and should not be overridden without documented reasoning.

## Narrative & Lore Rules

**Iron law:** NEVER invent fictional details — objects, events, characters, relationships, affiliations, backstory — that the user has not explicitly established. When unsure whether something is canon, **ask before introducing it**.

- Treat all user-provided worldbuilding as **authoritative canon**. Do not assume character religions, affiliations, motivations, or backstory details.
- When the user provides lore corrections, propagate changes to **ALL relevant local files** in the same pass. Do not fix one file and leave others inconsistent.
- When writing narrative prose or vignettes, only reference objects, props, and setting details that have been **explicitly seeded** in the scene or source material. Do not add atmospheric details that introduce new canonical facts.
- If a worldbuilding session is starting, **read existing canon files first** before generating any content. Summarize what's established and confirm with the user before making changes.

## Copyright Policy

**High priority:** All content created for this project must be either original or sourced from openly licensed material. Open source / open license content is explicitly welcome — for example, the D&D 5e Systems Reference Document (SRD) released under the Creative Commons Attribution 4.0 license is fair game, as are other systems published under OGL, CC, or similarly permissive licenses. When using such material, note the source and confirm the license terms apply.

Do not reproduce, closely paraphrase, or derive mechanics, text, lore, or art from proprietary copyrighted works. When researching closed systems for inspiration, extract only general concepts and design principles — never copy specific wording, stat blocks, spell lists, monster names, or proprietary mechanics verbatim.

## PHB Scope Decisions

**Core PHB (v1):** Introduction, Character Creation (Overview, Attributes, Lineage, Classes, Backgrounds, Skills), Rules (Overview, Adventuring, Combat), Compendium (Skills, Equipment, Magical Items).

**Deferred to Facet modules:** Downtime, Crafting, Economy, Feats, Technology. These are listed in the ToC as optional modules but not written in the core PHB.

**Lineage (formerly Races):** The character ancestry chapter is called Lineage. Shattered Origin defaults to human — the core PHB describes humans and provides MM guidance for creating custom lineages. Non-human lineages belong in setting Facets or homebrew. This keeps onboarding simple and puts creative world-building in the MM's hands.

**Combat:** Has its own chapter (III.3) but uses the same 2d6 resolution system as everything else — no separate tactical subsystem.

## Software-PHB Synchronization

The software layer (`software/`) is the mechanical implementation of the PHB.
`software/facets/base/facet.yaml` is the machine-readable encoding of every
mechanic the engine needs: attributes, skills, Techniques, advancement rules,
combat parameters, and magic domains.

**When to update the software:** Any time a PHB decision settles a mechanic
(new system, changed rule, renamed concept), update the software in the same
development cycle. Do not let the software lag the PHB by more than one branch.
Purely narrative changes (vignettes, sidebars, tone) do not require software changes.

**Sync workflow:**
1. PHB change settled → update `facets/base/facet.yaml` first (single source of truth for rules)
2. If the mechanic needs engine logic → update `software/app/game/engine.py` and/or
   the character model (`software/app/game/character.py`)
3. If players interact with the mechanic → add or update WebSocket events in
   `software/app/api/websocket.py`
4. Write or update tests before committing
5. Commit message references the PHB section: e.g., `Implement PHB III.3: Combat exchanges`

**Deferred modules** (Crafting, Economy, Feats, Technology): Do not implement
until the corresponding PHB chapter is written.

**Quick references are compressions, not paraphrases.** A quick-reference card
(`mm_manual/MM5_Quick_Reference.md`, `Quick_Start.md`, in-chapter quick-ref
blocks) may only restate canonical body text in shorter form. It may never
introduce a rule, exception, or wording the canonical section doesn't already
state. Any rules change must update body text, every quick ref that touches
it, `facet.yaml`, and the engine — all in the same commit.

**The simulator may only drive `app/game/combat.py`. It must never
re-implement a rule.** Combat resolution existed as two independent
implementations (`websocket.py` and `tools/combat_sim.py`) that silently
diverged, which invalidated a research corpus of recorded simulation numbers.
Simulation tooling calls the shared rules module; it does not carry its own
copy of rule logic.

## Software Development Ethos

This project uses **test-driven development (TDD)** as its core software practice:

1. Write the test first — before implementing any new feature, handler, or mechanic.
2. Run the test to confirm it fails (red).
3. Implement the minimum code to make it pass (green).
4. Refactor if needed, keeping all tests green.

Every software change that adds or modifies behaviour must have a corresponding test. New WebSocket handlers, roll modifiers, character fields, and API endpoints all require tests before or alongside the implementation. PRs without tests for new behaviour will not be merged.

**Coverage expectations:**
- Minimum **3 tests per public function** (happy path, edge case, error handling).
- When delivering a new module or major feature, test count should be proportional to code size — a 500-line module needs more than 5 tests.
- After completing implementation, run the full test suite and report the pass/fail count. Do not consider a feature done until all tests pass.

## Terminology

- The facilitating player role is called the **Mirror Master (MM)** — never "GM" or "DM". The name is thematic: the MM's role is to reflect the spotlight back onto the players and keep them the stars of their own story.

## Example Characters & Writing Style

Four recurring characters (MM, Zahna, Mordai, Zulnut) appear in PHB example vignettes. Tone is sarcastic and lighthearted — comical, not mean-spirited — set in fantasy consistent with Shattered Origin.

**Read `references/phb-examples.md` when:**
- Writing or editing a PHB chapter vignette
- Creating a new example scenario
- Checking formatting conventions for examples

> Contains: full character personalities with attributes, formatting conventions (MM:/CharacterName:/italics/parentheses), ground rules, and established scenarios per chapter.

## Available Skills

Key skills for quick reference. **Full tables with all skills, sources, and detailed usage context are in `references/skills-reference.md`.**

| Task | Key Skills |
|---|---|
| Game mechanics design | `/game-design`, `/systems-thinking-leverage`, `/constraint-based-creativity` |
| Mechanic testing | `/prototyping-pretotyping`, `/evaluation-rubrics`, `/encounter-balance` |
| PHB content organization | `/information-architecture`, `/cognitive-design`, `/writing-structure-planner` |
| PHB prose editing | `/writing-revision`, `/writing-pre-publish-checklist` |
| Software development | `/code-data-analysis-scaffolds`, `/adr-architecture`, `/rpg-api-development` |
| UI/frontend | `/frontend-design:frontend-design`, `/cognitive-design` |
| Prioritization | `/prioritization-effort-impact`, `/focus-timeboxing-8020`, `/roadmap-backcast` |
| Creative blocks | `/brainstorm-diverge-converge`, `/constraint-based-creativity` |
| MM/adventure content | `/mimir-dm`, `/npc-generator`, `/panel-patterns` |
| Consistency checking | `/continuity-check` |

## Git & GitHub

- Always use **`gh` CLI** for pushes and PRs — never raw HTTPS push.
- Before committing, **review staged files** — never sweep in `.env`, credentials, or secret files. If unsure, show `git status` and the full diff for user approval before committing.
- Confirm which GitHub account is authenticated (`gh auth status`) before attempting PR operations.
- Prefer specific `git add <file>` over `git add -A` or `git add .`.

## Contributing Workflow

```bash
git checkout -b feature/FeatureName   # create feature branch
git commit -m 'Add some feature'       # commit changes
git push origin feature/FeatureName   # push branch (use gh CLI)
# then open a Pull Request on GitHub
```

GitHub: https://github.com/AJTDaedalus/facets_of_origin

## License

GPLv3 — see `LICENSE.txt`.

---

## Reference Trigger Index

| You're about to... | Read this first |
|---|---|
| Write a PHB example vignette | `references/phb-examples.md` — character voices, formatting, established scenarios |
| Choose a skill for a task | `references/skills-reference.md` — full tables by category |
| Propose new mechanics | `research/dice_system_analysis.md` — 2d6 system rationale, open design questions |
| Implement a settled mechanic | Software-PHB Sync workflow above + `facets/base/facet.yaml` |
| Use World Anvil MCP or API | `references/worldanvil-mcp.md` — working config, pitfalls, verification |
