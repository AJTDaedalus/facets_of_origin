"""Render a readable transcript from the event log.

Mechanical lines are rendered *here*, from events. Agent free-text is quoted as
prose but never supplies a die value, an outcome tier, or a Condition. That is
the structural guarantee: there is no code path by which a transcript can report
a roll the engine did not make.

Compare `playtest/07_oraga_night_playtests/session_log_01.md`, which was written
alongside the engine rather than from it, and whose dice are confabulated.
"""
from __future__ import annotations

from tools.agentic_playtest.events import Event, EventLog


def _fmt_roll(roll: dict) -> str:
    dice = ", ".join(str(d) for d in roll["dice_rolled"])
    kept = roll.get("dice_kept", roll["dice_rolled"])
    dropped = len(roll["dice_rolled"]) - len(kept)
    parts = [f"2d6 ({dice})" if len(roll["dice_rolled"]) == 2 else f"{len(roll['dice_rolled'])}d6 ({dice})"]
    if dropped:
        parts.append(f"drop {dropped}")
    mods = []
    if roll.get("attribute_modifier"):
        mods.append(f"attr {roll['attribute_modifier']:+d}")
    if roll.get("skill_modifier"):
        mods.append(f"skill {roll['skill_modifier']:+d}")
    if roll.get("difficulty_modifier"):
        mods.append(f"diff {roll['difficulty_modifier']:+d}")
    if roll.get("offense_modifier"):
        mods.append(f"posture {roll['offense_modifier']:+d}")
    mod_str = f" [{', '.join(mods)}]" if mods else ""
    return f"{' '.join(parts)}{mod_str} = **{roll['total']}** — {roll['outcome_label']}"


def _pretty(value: str) -> str:
    return str(value).replace("_", " ")


def render_event(event: Event) -> str | None:
    """One event as one transcript line, or None if it isn't shown."""
    d = event.data
    a = event.actor

    if event.kind == "say":
        return f"**{a}:** {d['text']}"
    if event.kind == "say_ooc":
        return f"> *{a} (out of character):* {d['text']}"
    if event.kind == "scene":
        return f"**MM:** {d['text']}"
    if event.kind == "scene_ended":
        return f"\n*— scene ends: {d['summary']} —*\n"

    if event.kind == "roll":
        desc = f" ({d['description']})" if d.get("description") else ""
        spark = f" · spent {d['sparks_spent']} Spark(s)" if d.get("sparks_spent") else ""
        return f"`{a} rolls{desc}:` {_fmt_roll(d['roll'])}{spark}"
    if event.kind == "saving_throw":
        return f"`{a} saves ({_pretty(d['major_attribute_id'])}):` {_fmt_roll(d['roll'])}"
    if event.kind == "cast":
        return (f"`{a} casts {_pretty(d['domain_id'])} [{d['scope']}] — \"{d['intent']}\":` "
                f"{_fmt_roll(d['roll'])}")

    if event.kind == "combat_started":
        return "\n### Combat begins\n"
    if event.kind == "combat_ended":
        return "\n### Combat ends\n"
    if event.kind == "posture_declared":
        return f"`{a} declares {d['posture']}.`"
    if event.kind == "postures_revealed":
        shown = ", ".join(f"{k}={v}" for k, v in d["postures"].items())
        return f"`Postures revealed: {shown}`"
    if event.kind == "strike":
        press = " [Press]" if d.get("press") else ""
        return f"`{a} strikes {d['target']}{press}:` {_fmt_roll(d['roll'])}"
    if event.kind == "react":
        cost = f" (−{d['endurance_cost']} End)" if d.get("endurance_cost") else " (free)"
        tail = f" {_fmt_roll(d['roll'])}" if d.get("roll") else ""
        return f"`{a} reacts: {d['reaction']}{cost}`{tail}"
    if event.kind == "enemy_attack":
        applied = d.get("condition_applied")
        soft = " [softened]" if d.get("arm_softened") else ""
        if not applied:
            by = "armour" if d.get("armor_spent") else "the reaction"
            return f"`Enemy attack on {d['target']}{soft}: absorbed by {by}.`"
        broke = " — **Broken**" if d.get("broken") else ""
        return f"`Enemy attack on {d['target']}{soft}: {_pretty(applied)}{broke}`"
    if event.kind == "condition_cleared":
        return f"`{d['target']}: {_pretty(d['condition'])} cleared.`"
    if event.kind == "exchange_ended":
        cleared = [f"{pn} clears {', '.join(_pretty(c) for c in u['cleared'])}"
                   for pn, u in d["characters"].items() if u.get("cleared")]
        tail = f" — {'; '.join(cleared)}" if cleared else ""
        return f"`Exchange ends.{tail}`"

    if event.kind == "enemy_spawned":
        return f"`{d['name']} joins the fight ({d['tier']}, TR {d['tr']}).`"
    if event.kind == "enemy_resolve":
        if d.get("mook_removed") or d.get("defeated"):
            return f"`{d['tracker_key']} is defeated.`"
        return f"`{d['tracker_key']}: Resolve {d['resolve_before']} → {d['resolve']}.`"

    if event.kind == "spark_awarded":
        return f"`✦ {d['target']} earns a Spark — {d['reason']} (now {d['sparks_now']}).`"
    if event.kind == "skill_point_spent":
        up = " — **rank up**" if d.get("rank_advanced") else ""
        return f"`{a} spends {d['sp_cost']} SP on {d['skill_id']}{up}.`"

    if event.kind == "clock_created":
        return f"`Threat Clock \"{d['name']}\" created ({d['segments']} segments).`"
    if event.kind == "clock_advanced":
        full = " — **it strikes**" if d.get("is_full") else ""
        return f"`{d['name']}: {d['filled_segments']}/{d['segments']}{full}`"

    if event.kind == "rules_gap":
        return f"> ⚖️ *MM ruling — {d['question']}: {d['ruling']}*"
    if event.kind == "refused":
        return f"> ⚠️ *{a} attempted {d['verb']}: {d['reason']}*"

    if event.kind == "character_joined":
        return None
    return None


def render(log: EventLog, title: str = "Playtest Session") -> str:
    lines = [
        f"# {title}",
        "",
        f"*Session `{log.session_id}` · arm **{log.arm}** · seed `{log.seed}`*",
        "",
        "> Every mechanical line below is rendered from the engine's event log. No "
        "die value in this document was written by a language model.",
        "",
    ]

    cast = [e for e in log.of_kind("character_joined")]
    if cast:
        lines.append("**Cast:** " + ", ".join(
            f"{e.data['character']} ({e.data['facet']}, played by {e.actor})" for e in cast))
        lines.append("")

    beat = -1
    for event in log:
        if event.beat != beat:
            beat = event.beat
            lines.append(f"\n<a id=\"beat-{beat}\"></a>")
        rendered = render_event(event)
        if rendered is not None:
            lines.append(rendered)

    return "\n".join(lines) + "\n"
