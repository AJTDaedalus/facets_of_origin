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

## Terminology

- The facilitating player role is called the **Mirror Master (MM)** — never "GM" or "DM". The name is thematic: the MM's role is to reflect the spotlight back onto the players and keep them the stars of their own story.

## Example Characters & Writing Style

All PHB chapters include short, in-world example vignettes that demonstrate mechanics. These examples must be:
- **Sarcastic and lighthearted** in tone — comical, not mean-spirited
- Set in a **fantasy context** consistent with Shattered Origin
- Brief — a sidebar, not a scene

The four recurring characters are:

**The Mirror Master (MM)** — The narrator of all examples. Frequently exasperated by the party's approach to problems, but clearly relishing every moment. Reacts to chaos with the weary delight of someone who absolutely should have seen this coming.

**Zahna** — A studious young mage. Entirely absorbed in books, magical theory, and intellectual problems. Not rude, but thoroughly dismissive of anything he considers beneath analysis. Will solve the puzzle correctly while being completely oblivious to the social situation around him. Attributes: Knowledge 3, Intelligence 3, Wisdom 1 (very much does not read the room).

**Mordai** — A strong warrior with a genuine heart. Considers himself a defender of the weak and takes that seriously. Not the brightest, but far from foolish — he simply prefers the direct solution to every problem, usually the most physical one available. Will ask the archivist for information the same way he'd ask a locked door. Attributes: Strength 3, Constitution 3, Intelligence 1.

**Zulnut** — Lazy. Profoundly, almost philosophically lazy. Exceptionally nimble and prefers to accomplish things with the minimum possible effort and maximum possible flair. Will complete a task with a dazzling acrobatic flourish, then immediately try to smoke a cigarette and leave. Has a preternatural talent for noticing the one thing in the room that matters, then doing something absurd with that information. Attributes: Dexterity 3, Luck 3, Constitution 1.

### Example Scenario Per Chapter
Each chapter should have one brief vignette demonstrating the chapter's core mechanic or concept. Scenarios established so far:
- **II.2 Attributes** — Investigating a series of mysterious disappearances in a village called Millhaven, sourced from records in a city archive (Thornwall Municipal Archive). Zahna researches records, Mordai questions the archivist, Zulnut finds a forgotten box of field notes on a high shelf in about four seconds and then tries to leave.

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
