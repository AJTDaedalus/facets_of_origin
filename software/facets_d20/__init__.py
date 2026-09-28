"""Facets d20 rules engine — the single source of Facets d20 rule logic.

Modules:
    dice      — dice expressions and d20 rolls (advantage / disadvantage)
    data      — load and validate facets_d20/data/*.yaml
    build     — characters from picks: computed numbers and build legality
    combat    — the combat rules as functions (08_Combat.md, 09 MM guide)
    monsters  — SRD-style monster blocks converted per the MM guide
    spells    — combat-relevant spell effects (data) used by the simulator
    sim       — Monte Carlo fight simulator with a documented tactical AI

Tools (software/tools/d20_sim.py) and tests drive these modules; they never carry a
copy of a rule. See docs/DESIGN_facets_d20_engine.md.

Includes material adapted from the System Reference Document 5.2.1 by Wizards of the
Coast LLC, licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/legalcode).
"""
