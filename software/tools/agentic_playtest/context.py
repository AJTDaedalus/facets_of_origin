"""The stable prompt prefix, built once and cached.

Every agent in a session shares a large prefix: the rules digest, the scenario,
the cast. It is identical across every agent and every turn, which makes it the
single highest-leverage place to put a `cache_control` breakpoint — without one,
a session costs roughly five times more than it needs to.

The prefix must therefore be **byte-identical between builds**. No timestamps, no
unsorted dicts, no run IDs. Volatile content (the beat number, recent events)
goes strictly after the breakpoint. `tests/test_agentic_playtest.py` asserts the
determinism, because a silent invalidator here shows up only as a cost increase.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _posture_line(name: str, spec: dict) -> str:
    """One posture, described by what it costs and buys.

    `offense_modifier` is None for Withdrawn — it allows no offense at all,
    which is a different thing from a modifier of zero.
    """
    offense = spec.get("offense_modifier")
    parts = ["no offense" if offense is None else f"offense {offense:+d}"]
    cost = spec.get("reaction_cost_modifier")
    if cost:
        parts.append(f"reactions cost {cost:+d}")
    if spec.get("endurance_recovery"):
        parts.append(f"recover {spec['endurance_recovery']} Endurance")
    return f"{name} ({', '.join(parts)})"


def rules_digest(ruleset) -> str:
    """A compact, complete statement of the mechanics an agent needs.

    Generated from the loaded ruleset rather than transcribed, so it cannot drift
    from `facet.yaml` the way a hand-written summary would. An MM agent given a
    stale digest invents rules to fill the gap — which is how batch 07 produced
    'the Watched condition'.
    """
    r = ruleset
    lines: list[str] = ["## The rules you are playing", ""]

    # Tiers carry a lower `threshold`; the catch-all lowest tier has None.
    ordered = sorted(r.roll_resolution.outcome_tiers,
                     key=lambda t: (t.threshold is None, -(t.threshold or 0)))
    tiers = ", ".join(
        f"{t.threshold}+ = {t.label}" if t.threshold is not None
        else f"below that = {t.label}"
        for t in ordered
    )
    lines += [
        f"**Core roll:** {r.roll_resolution.dice} + Attribute modifier + Skill "
        f"modifier + Difficulty modifier. Outcomes: {tiers}.",
        "",
        "**Difficulty:** " + ", ".join(
            f"{d.label} {d.modifier:+d}" for d in r.roll_resolution.difficulty_modifiers),
        "",
    ]

    lines += ["**Attributes** (rating 1-3):"]
    for major in r.major_attributes:
        minors = ", ".join(
            m.name for m in r.minor_attributes if m.id in major.minor_attributes)
        lines.append(f"- {major.name}: {minors}")
    lines.append("")

    lines += ["**Skill ranks:** " + ", ".join(
        f"{s.label} {s.modifier:+d}" for s in r.advancement.skill_ranks), ""]

    combat = r.combat
    lines += [
        "**Combat** — everyone acts in simultaneous Exchanges.",
        f"- Endurance pool: {combat.endurance.base} + Constitution modifier + "
        f"Endurance skill rank.",
        "- Postures, declared secretly each exchange, then revealed: " + ", ".join(
            _posture_line(name, d) for name, d in sorted(combat.postures.items())),
        "- Reactions, one per incoming action: Dodge (Dexterity), Parry "
        "(Strength+Combat), Absorb (free, take it), Intercept (protect an ally, "
        "once per exchange).",
        "- At 0 Endurance only Absorb is available.",
        "",
        "**Enemies never roll.** An enemy attack is declared by the MM and lands as "
        "a Condition; the PC reacts to reduce it. A Mook's attack lands at Tier 1, "
        "a Named NPC's or Boss's at Tier 2.",
        "",
        "**Conditions:**",
    ]
    for tier, group in ((1, combat.conditions.tier1), (2, combat.conditions.tier2),
                        (3, combat.conditions.tier3)):
        for c in group:
            lines.append(f"- Tier {tier} `{c.id}` — {c.description}")
    lines += [
        "Tier 1 clears at end of exchange. Tier 2 persists until treated. A second "
        "Tier 2 of the same kind escalates to Broken (out of the fight).",
        "",
        "**Striking an enemy:** 10+ depletes 2 Resolve, 7-9 depletes 1. At 0 "
        "Resolve the enemy is defeated. Mooks have no Resolve — one Strike removes "
        "them (10+ if armoured).",
        "",
        "**Armour (PC):** a per-scene downgrade budget — Light softens the first 2 "
        "incoming Conditions one tier each, Heavy the first 4. Armour and a partial "
        "reaction never stack; only the greater reduction applies.",
        "",
        f"**Sparks:** spend before rolling; each adds a die and drops the lowest. "
        f"You start a session with {r.spark.base_sparks_per_session if r.spark else 3}. "
        "Earn them by MM award, peer nomination at an act break, or by claiming a "
        "Graceful Failure — narrating how your own 6- makes the story richer.",
        "",
        "**Magic:** Domain + Intent + Scope, no spell lists. Scopes are Minor, "
        "Significant, Major; the difficulty depends on your domain's breadth. "
        "Before you unlock a Technique your magic works at Minor scope only — the "
        "scope restriction is the whole limitation, there is no extra difficulty.",
        "",
        f"**Advancement:** {r.advancement.session_skill_points} Skill Points per "
        f"session, spendable only on skills you actually used. "
        f"{r.advancement.marks_per_rank} marks advance a rank. Primary-Facet skills "
        f"cost 1 SP, everything else 2.",
        "",
    ]
    return "\n".join(lines)


def skill_reference(ruleset) -> str:
    lines = ["## Skills", ""]
    by_facet: dict[str, list[str]] = {}
    for skill in ruleset.skills:
        if skill.status == "stub":
            continue
        by_facet.setdefault(skill.facet, []).append(
            f"`{skill.id}` ({skill.attribute}) — {skill.description}")
    for facet in sorted(by_facet):
        lines.append(f"**{facet.title()}**")
        lines += [f"- {entry}" for entry in sorted(by_facet[facet])]
        lines.append("")
    return "\n".join(lines)


@dataclass
class SessionContext:
    """The pieces of the prompt, split by how often they change."""

    #: Identical for every agent, every turn — the cache breakpoint goes here.
    shared_prefix: str
    #: Per-agent, stable for the session.
    role_block: str

    def system_blocks(self) -> list[dict]:
        """System prompt as Anthropic content blocks with the breakpoint set.

        `cache_control` sits on the last shared block, so the role block and
        everything after it stays outside the cached prefix.
        """
        return [
            {"type": "text", "text": self.shared_prefix,
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": self.role_block},
        ]


def build_shared_prefix(ruleset, scenario: str, cast: str) -> str:
    """Deterministic. Byte-identical for the same inputs, or caching breaks."""
    return "\n".join([
        "You are taking part in a playtest of *Facets of Origin*, a tabletop "
        "roleplaying game. Play it as a real session at a real table.",
        "",
        rules_digest(ruleset),
        skill_reference(ruleset),
        "## Tonight's scenario",
        "",
        scenario.strip(),
        "",
        "## Who is at the table",
        "",
        cast.strip(),
        "",
        "## How this works",
        "",
        "You act by calling tools. Two rules govern everything:",
        "",
        "1. **Never state a mechanical result yourself.** You do not know what you "
        "rolled until the tool tells you. Do not write dice values, totals, "
        "outcome labels, or Conditions in your speech unless a tool has just "
        "returned them to you. Narrate around the result you were given.",
        "2. **Speak like a person at a table.** You can talk in character, talk "
        "out of character, joke, ask questions, disagree, and change your mind. "
        "Short turns are fine. You do not have to narrate everything.",
        "",
        "If a tool refuses your action, read the reason and choose something else "
        "— that is the rules talking.",
    ])
