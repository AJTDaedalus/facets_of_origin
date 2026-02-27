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

## Research Reference

The `research/` directory contains foundational documents that should inform all design decisions. **Always consult relevant research files before proposing mechanics, systems, or content.**

- `research/dice_system_analysis.md` — Synthesis of TTRPG market landscape and psychology of fun/dice/social bonding. Covers: why 2d6 three-tier outcomes are optimal, the Spark system recommendation, market gaps, what competing games do well and poorly, and five open design questions that need resolution before detailed system work begins.

When proposing anything related to dice mechanics, resolution systems, player experience, onboarding, or digital design, check this file first — the recommendations are grounded in academic psychology research and market analysis and should not be overridden without documented reasoning.

## Copyright Policy

**High priority:** All content created for this project must be either original or sourced from openly licensed material. Open source / open license content is explicitly welcome — for example, the D&D 5e Systems Reference Document (SRD) released under the Creative Commons Attribution 4.0 license is fair game, as are other systems published under OGL, CC, or similarly permissive licenses. When using such material, note the source and confirm the license terms apply.

Do not reproduce, closely paraphrase, or derive mechanics, text, lore, or art from proprietary copyrighted works. When researching closed systems for inspiration, extract only general concepts and design principles — never copy specific wording, stat blocks, spell lists, monster names, or proprietary mechanics verbatim.

## Contributing Workflow

```bash
git checkout -b feature/FeatureName   # create feature branch
git commit -m 'Add some feature'       # commit changes
git push origin feature/FeatureName   # push branch
# then open a Pull Request on GitHub
```

GitHub: https://github.com/AJTDaedalus/facets_of_origin

## License

GPLv3 — see `LICENSE.txt`.
