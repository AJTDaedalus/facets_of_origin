"""Anthropic tool definitions — one per agent-callable verb.

Descriptions are prescriptive about *when* to call each tool, not just what it
does: recent Opus models reach for tools conservatively, and a trigger condition
in the description measurably raises the should-call rate.

`strict: true` everywhere, so an agent cannot smuggle a free-text mechanical
claim through a parameter. `tests/test_agentic_playtest.py` asserts that the
schema set and the `Verbs` surface match, so a verb cannot be added without
being exposed or vice versa.
"""
from __future__ import annotations

from typing import Any

from tools.agentic_playtest.verbs import MM_VERBS, PLAYER_VERBS


def _tool(name: str, description: str, properties: dict[str, Any],
          required: list[str]) -> dict:
    return {
        "name": name,
        "description": description,
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
    }


_TEXT = {"type": "string"}
_DIFFICULTY = {"type": "string", "enum": ["Easy", "Standard", "Hard", "Very Hard"]}
_OUTCOME = {"type": "string",
            "enum": ["full_success", "partial_success", "failure"]}

# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

SAY = _tool(
    "say",
    "Speak or act in character. Use this for anything your character says or "
    "does that does not need a die roll. Most of your turns should be this.",
    {"text": _TEXT}, ["text"],
)

SAY_OOC = _tool(
    "say_ooc",
    "Speak as yourself, not your character — a joke, a question about the rules, "
    "an aside to another player, thinking out loud about what to do. Real tables "
    "are full of this; use it whenever it's what you'd actually say.",
    {"text": _TEXT}, ["text"],
)

# ---------------------------------------------------------------------------
# Player verbs
# ---------------------------------------------------------------------------

PLAYER_TOOLS: dict[str, dict] = {
    "say": SAY,
    "say_ooc": SAY_OOC,
    "roll_skill": _tool(
        "roll_skill",
        "Attempt something risky where the outcome is uncertain and the stakes "
        "matter. Call this instead of describing a success — you do not know "
        "whether you succeed until this returns.",
        {"attribute_id": _TEXT,
         "skill_id": {"type": ["string", "null"]},
         "difficulty": _DIFFICULTY,
         "sparks_spent": {"type": "integer", "minimum": 0, "maximum": 3},
         "description": _TEXT},
        ["attribute_id", "skill_id", "difficulty", "sparks_spent", "description"],
    ),
    "saving_throw": _tool(
        "saving_throw",
        "Roll when something happens TO your character rather than something you "
        "chose to attempt — a trap springs, a spell lands, the floor gives way.",
        {"major_attribute_id": {"type": "string", "enum": ["body", "mind", "soul"]},
         "difficulty": _DIFFICULTY,
         "sparks_spent": {"type": "integer", "minimum": 0, "maximum": 3}},
        ["major_attribute_id", "difficulty", "sparks_spent"],
    ),
    "cast": _tool(
        "cast",
        "Use magic. Describe what you want to happen (intent) and how big it is "
        "(scope). Only call this if your character has a magic domain.",
        {"domain_id": _TEXT,
         "scope": {"type": "string", "enum": ["minor", "significant", "major"]},
         "intent": _TEXT,
         "spark_use": {"type": ["string", "null"],
                       "enum": ["improve_roll", "push_scope", "ease_focused_major", None]}},
        ["domain_id", "scope", "intent", "spark_use"],
    ),
    "declare_posture": _tool(
        "declare_posture",
        "Declare your stance for this exchange. Everyone declares in secret and "
        "the MM reveals them together, so choose before you know what others did.",
        {"posture": {"type": "string",
                     "enum": ["aggressive", "measured", "defensive", "withdrawn"]}},
        ["posture"],
    ),
    "strike": _tool(
        "strike",
        "Attack a target in combat. Press spends 1 Endurance to add a die and "
        "drop the lowest.",
        {"target": _TEXT, "attribute_id": _TEXT,
         "skill_id": {"type": ["string", "null"]},
         "difficulty": _DIFFICULTY,
         "press": {"type": "boolean"},
         "sparks_spent": {"type": "integer", "minimum": 0, "maximum": 3}},
        ["target", "attribute_id", "skill_id", "difficulty", "press", "sparks_spent"],
    ),
    "react": _tool(
        "react",
        "Respond to an incoming attack. Call this when the MM tells you something "
        "is coming at you. Absorb is always free; at 0 Endurance it is your only "
        "option.",
        {"reaction": {"type": "string",
                      "enum": ["dodge", "parry", "absorb", "intercept"]}},
        ["reaction"],
    ),
    "support": _tool(
        "support",
        "Help an ally instead of acting yourself. Use it when someone else's roll "
        "matters more than yours.",
        {"target": _TEXT,
         "bonus_type": {"type": "string", "enum": ["add_die", "ease_difficulty"]},
         "attribute_id": _TEXT,
         "skill_id": {"type": ["string", "null"]}},
        ["target", "bonus_type", "attribute_id", "skill_id"],
    ),
    "maneuver": _tool(
        "maneuver",
        "Change the situation rather than dealing damage — disarm, shove, blind, "
        "cut the rope, tip the brazier. Use it when the clever option beats the "
        "direct one.",
        {"target": _TEXT, "attribute_id": _TEXT,
         "skill_id": {"type": ["string", "null"]},
         "description": _TEXT},
        ["target", "attribute_id", "skill_id", "description"],
    ),
    "nominate_for_spark": _tool(
        "nominate_for_spark",
        "Nominate another player for a Spark because they did something great. "
        "Call this at an act break, or any time it's deserved. The MM confirms.",
        {"player_name": _TEXT}, ["player_name"],
    ),
    "claim_graceful_fail": _tool(
        "claim_graceful_fail",
        "Claim a Spark for your own failure. Call this after you roll a 6- and "
        "narrate how the failure makes the story richer rather than just worse.",
        {}, [],
    ),
    "spend_skill_point": _tool(
        "spend_skill_point",
        "Advance a skill you actually used this session. Call this at the end of "
        "the session, or when the MM says advancement is open.",
        {"skill_id": _TEXT}, ["skill_id"],
    ),
    "select_technique": _tool(
        "select_technique",
        "Take a Technique. Only available when you have a pick from a Facet level.",
        {"technique_id": _TEXT, "choice": {"type": ["string", "null"]}},
        ["technique_id", "choice"],
    ),
}

# ---------------------------------------------------------------------------
# MM verbs. Note the absence of any roll verb for NPCs.
# ---------------------------------------------------------------------------

MM_TOOLS: dict[str, dict] = {
    "say": _tool(
        "say",
        "Speak as an NPC, or answer a player directly. Use this constantly — "
        "NPCs talking is most of what a session is.",
        {"text": _TEXT}, ["text"],
    ),
    "say_ooc": SAY_OOC,
    "describe_scene": _tool(
        "describe_scene",
        "Set or change the scene. Call this when the players arrive somewhere, "
        "when something visible changes, or when they need to know what their "
        "options are.",
        {"text": _TEXT}, ["text"],
    ),
    "rule_it": _tool(
        "rule_it",
        "Make a ruling the rules don't cover. Call this whenever you have to "
        "decide something the rules are silent or unclear about — say what you "
        "decided and move on. Do NOT stall; a ruling now beats a search. Every "
        "call is recorded as a gap in the rules, which is one of the most useful "
        "things this session can produce.",
        {"question": _TEXT, "ruling": _TEXT}, ["question", "ruling"],
    ),
    "end_scene": _tool(
        "end_scene",
        "Close the current scene and summarise what changed. Call this when the "
        "scene's question has been answered.",
        {"summary": _TEXT}, ["summary"],
    ),
    "start_combat": _tool(
        "start_combat",
        "Begin combat. Everyone's Endurance pool opens and postures start.",
        {}, [],
    ),
    "reveal_postures": _tool(
        "reveal_postures",
        "Flip everyone's declared posture face up. Call this once every player "
        "in the fight has declared, before actions resolve.",
        {}, [],
    ),
    "land_enemy_attack": _tool(
        "land_enemy_attack",
        "An enemy attacks a character. Enemies never roll — you declare the "
        "incoming Condition and the engine applies armour and any partial "
        "reaction. A Mook's attack lands at Tier 1, a Named NPC's or Boss's at "
        "Tier 2. Set reaction_downgraded when the target's Dodge or Parry got a "
        "7-9.",
        {"target_player": _TEXT, "condition": _TEXT,
         "reaction_downgraded": {"type": "boolean"}},
        ["target_player", "condition", "reaction_downgraded"],
    ),
    "clear_condition": _tool(
        "clear_condition",
        "Remove a Condition from a character — because it was treated, or because "
        "the fiction resolved it.",
        {"target_player": _TEXT, "condition": _TEXT},
        ["target_player", "condition"],
    ),
    "end_exchange": _tool(
        "end_exchange",
        "Close the exchange. Tier 1 Conditions clear, Withdrawn characters "
        "recover, and everyone declares posture again.",
        {}, [],
    ),
    "end_combat": _tool("end_combat", "End the fight.", {}, []),
    "spawn_enemy": _tool(
        "spawn_enemy",
        "Put an enemy from the library onto the board. Call this before combat "
        "starts, or mid-fight for reinforcements.",
        {"enemy_id": _TEXT, "instance_name": {"type": ["string", "null"]}},
        ["enemy_id", "instance_name"],
    ),
    "apply_strike_to_enemy": _tool(
        "apply_strike_to_enemy",
        "Apply a player's Strike result to an enemy. Send the OUTCOME the player "
        "rolled — the engine decides what it costs. Call this immediately after "
        "any Strike that hit.",
        {"tracker_key": _TEXT, "outcome": _OUTCOME},
        ["tracker_key", "outcome"],
    ),
    "award_spark": _tool(
        "award_spark",
        "Give a player a Spark. Call this for a great moment, for a confirmed "
        "peer nomination, or for a Graceful Failure claim.",
        {"player_name": _TEXT, "reason": _TEXT}, ["player_name", "reason"],
    ),
    "open_act_break": _tool(
        "open_act_break",
        "Open a nomination window. Call this at a scene or act break — it prompts "
        "every player to nominate someone for a Spark.",
        {}, [],
    ),
    "mark_skill_used": _tool(
        "mark_skill_used",
        "Mark a skill as used this session so its owner can advance it. Rolled "
        "skills are marked automatically; use this for skills used without a roll.",
        {"player_name": _TEXT, "skill_id": _TEXT}, ["player_name", "skill_id"],
    ),
    "create_clock": _tool(
        "create_clock",
        "Start a visible Threat Clock on a looming hazard. Call this when "
        "something is building that the players can see coming.",
        {"name": _TEXT, "segments": {"type": ["integer", "null"], "minimum": 2, "maximum": 12}},
        ["name", "segments"],
    ),
    "advance_clock": _tool(
        "advance_clock",
        "Advance a Threat Clock. A 7-9 or a 6- near the hazard advances it; a "
        "10+ never does.",
        {"clock_id": _TEXT, "outcome_tier": _OUTCOME},
        ["clock_id", "outcome_tier"],
    ),
    "table_roll": _tool(
        "table_roll",
        "Roll raw dice for something that is not a character action — a random "
        "table, which of two doors, an oracle. This has no outcome tier and is "
        "NOT how an enemy attacks.",
        {"notation": _TEXT, "label": _TEXT}, ["notation", "label"],
    ),
    "select_technique": _tool(
        "select_technique",
        "Grant a Technique to a player at a Facet level advancement.",
        {"technique_id": _TEXT, "choice": {"type": ["string", "null"]}},
        ["technique_id", "choice"],
    ),
}


def player_tools() -> list[dict]:
    return [PLAYER_TOOLS[name] for name in PLAYER_VERBS]


def mm_tools() -> list[dict]:
    return [MM_TOOLS[name] for name in MM_VERBS]
