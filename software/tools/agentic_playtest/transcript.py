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
    """One event as one transcript line, or None if it isn't shown.

    **Every `event.kind` below is a `type` the server actually broadcasts.** An
    earlier draft matched invented names (`roll`, `strike`, `enemy_attack`) that
    the observer socket never emits, so the mechanical half of the renderer was
    dead code and a transcript would have contained no dice at all. Adding a
    branch here means finding the `manager.broadcast` that produces it in
    `app/api/websocket.py` and reading the payload off that call — not guessing.
    """
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

    if event.kind == "roll_result":
        desc = f" ({d['description']})" if d.get("description") else ""
        spark = (f" · spent {d['roll']['sparks_spent']} Spark(s)"
                 if d["roll"].get("sparks_spent") else "")
        return f"`{a} rolls{desc}:` {_fmt_roll(d['roll'])}{spark}"
    if event.kind == "saving_throw_result":
        return f"`{a} saves ({_pretty(d['major_attribute_id'])}):` {_fmt_roll(d['roll'])}"
    if event.kind == "cast_result":
        pre = "" if d.get("technique_active") else " (pre-Technique)"
        return (f"`{a} casts {_pretty(d['domain_id'])} [{d['scope']}]{pre} — "
                f"\"{d['intent']}\":` {_fmt_roll(d['roll'])}")
    if event.kind == "support_result":
        return (f"`{a} supports {d['target']} ({_pretty(d['bonus_type'])}):` "
                f"{_fmt_roll(d['roll'])}")
    if event.kind == "maneuver_result":
        return f"`{a} manoeuvres against {d['target']}:` {_fmt_roll(d['roll'])}"
    if event.kind == "contested_roll_result":
        return (f"`{d['player_a']} vs {d['player_b']}:` {_fmt_roll(d['roll_a'])} / "
                f"{_fmt_roll(d['roll_b'])} — **{d['winner']}** takes it")

    if event.kind == "combat_started":
        return "\n### Combat begins\n"
    if event.kind == "combat_ended":
        return "\n### Combat ends\n"
    if event.kind == "posture_declared":
        return f"`{a} declares {d['posture']}.`"
    if event.kind == "postures_revealed":
        shown = ", ".join(f"{k}={v}" for k, v in d["postures"].items())
        return f"`Postures revealed: {shown}`"
    if event.kind == "strike_result":
        press = " [Press]" if d.get("press_used") else ""
        return f"`{a} strikes {d['target']}{press}:` {_fmt_roll(d['roll'])}"
    if event.kind == "react_result":
        cost = f" (−{d['endurance_cost']} End)" if d.get("endurance_cost") else " (free)"
        tail = f" {_fmt_roll(d['roll'])}" if d.get("roll") else ""
        return f"`{a} reacts: {_pretty(d['reaction'])}{cost}`{tail}"
    if event.kind == "condition_applied":
        # The server sends the *outcome* of an enemy attack: `condition` is None
        # when armour or a reaction ate it.
        applied = d.get("condition")
        soft = " [softened]" if d.get("arm_softened") else ""
        target = d.get("player", a)
        if not applied:
            by = "armour" if d.get("armor_absorbed") else "the reaction"
            return f"`Enemy attack on {target}{soft}: absorbed by {by}.`"
        broke = " — **Broken**" if applied == "broken" else ""
        return f"`Enemy attack on {target}{soft}: {_pretty(applied)}{broke}`"
    if event.kind == "condition_cleared":
        return f"`{d.get('player', a)}: {_pretty(d['condition'])} cleared.`"
    if event.kind == "exchange_ended":
        cleared = [f"{pn} clears {', '.join(_pretty(c) for c in u['cleared'])}"
                   for pn, u in d["characters"].items() if u.get("cleared")]
        tail = f" — {'; '.join(cleared)}" if cleared else ""
        return f"`Exchange ends.{tail}`"

    # The server nests the stat block under `enemy` and reports depletion on
    # `enemy_updated`. Read those shapes, not a shape of our own invention.
    if event.kind == "enemy_spawned":
        enemy = d.get("enemy") or {}
        name = enemy.get("name", d.get("tracker_key", "An enemy"))
        tier = enemy.get("tier", "?")
        return f"`{name} joins the fight ({tier}, TR {d.get('tr', '?')}).`"
    if event.kind == "enemy_updated":
        if d.get("mook_removed") or d.get("defeated"):
            return f"`{d['tracker_key']} is defeated.`"
        if not d.get("depletion"):
            return None  # a manual correction, not a Strike landing
        return (f"`{d['tracker_key']}: Resolve −{d['depletion']} "
                f"→ {d['resolve_current']}.`")
    if event.kind == "enemy_phase_change":
        return f"`{d['enemy_id']} changes: {d['description'].strip()}`"

    if event.kind == "spark_earned":
        return (f"`✦ {d['player']} earns a Spark — {d['reason']} "
                f"(now {d['sparks_now']}).`")
    if event.kind == "skill_point_spent":
        up = " — **rank up**" if d.get("rank_advances") else ""
        major = " — **Major Advancement**" if d.get("major_advancement") else ""
        return (f"`{d['player']} spends {d['sp_cost']} SP on "
                f"{_pretty(d['skill_id'])}{up}{major}.`")
    if event.kind == "act_break_opened":
        return "\n*— act break: nominate someone for a Spark —*\n"

    # Clock events nest the whole clock under `clock`.
    if event.kind == "clock_created":
        c = d["clock"]
        return f"`Threat Clock \"{c['name']}\" created ({c['segments']} segments).`"
    if event.kind in ("clock_advanced", "clock_fill"):
        c = d["clock"]
        full = " — **it strikes**" if c.get("is_full") else ""
        return f"`{c['name']}: {c['filled_segments']}/{c['segments']}{full}`"

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
