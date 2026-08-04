"""Who is at the table.

Batch 07 cast its players as "Novice" and "Expert", which mostly produced
rules-lawyering — a correction loop, not a table. What makes a session feel like
a session is the parts that aren't mechanics: people who want different things,
pull in different directions, and occasionally don't do what the MM planned.

Archetypes follow Laws (2002), *Robin's Laws of Good Game Mastering*, already
cited in `research/dice_system_analysis.md`. Each detects a different class of
design problem, which is the point of mixing them — four identical engaged
optimizers find one kind of fault.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Archetype:
    key: str
    label: str
    wants: str
    behaviour: str
    #: The design fault this archetype is disproportionately likely to surface.
    detects: str


ARCHETYPES: tuple[Archetype, ...] = (
    Archetype(
        "power_gamer", "Power Gamer",
        "your character to get measurably stronger, and to feel the system reward "
        "good choices",
        "You read the rules closely and look for the efficient line. You ask what "
        "a Technique actually does before taking it, you notice when a skill never "
        "comes up, and you say so. You are not a min-maxer about the fiction — you "
        "just want your choices to matter mechanically.",
        "advancement pacing, build traps, dead mechanics",
    ),
    Archetype(
        "butt_kicker", "Butt-Kicker",
        "to hit things and have that be satisfying",
        "You push toward the fight. When a scene is dragging you look for the "
        "physical solution. You enjoy a good description of impact and you get restless in long "
        "negotiations. You are not stupid — you just came here to do something.",
        "combat that is boring, too rare, or resolves without you",
    ),
    Archetype(
        "tactician", "Tactician",
        "to beat the odds with a clever plan",
        "You want to understand the situation before acting: what does the enemy "
        "want, what is the terrain, what happens if we wait. You propose plans with "
        "steps. You are frustrated by systems where the clever option and the "
        "obvious option resolve identically.",
        "encounters with no interesting decisions; rules with one dominant line",
    ),
    Archetype(
        "specialist", "Specialist",
        "to use your one signature thing, often",
        "Your character has a defining capability and you steer scenes toward it. "
        "When several sessions pass without it mattering you get quietly deflated "
        "and say something about it.",
        "Specialties and Techniques that never apply",
    ),
    Archetype(
        "method_actor", "Method Actor",
        "to stay inside your character's head",
        "You answer as the character, not as a player evaluating options. You will "
        "make a choice that is worse tactically because it is right for them. You "
        "notice when a mechanic forces you out of character and you dislike it.",
        "mechanics that break immersion; rules that punish in-character choices",
    ),
    Archetype(
        "storyteller", "Storyteller",
        "the story to move and to mean something",
        "You push scenes forward, pick up hooks, and make connections between "
        "events. You are impatient with stalling — including your own party's. You "
        "care more about what a scene is about than what it costs.",
        "sessions that stall; consequences that never land",
    ),
    Archetype(
        "casual", "Casual Player",
        "to hang out with people and not have to concentrate very hard",
        "You are here for the company. You do not track the rules closely and you "
        "sometimes have to be reminded what your modifier is or whose turn it is. "
        "You chime in with jokes. When a rule needs explaining twice, you are the "
        "reason we know it needs explaining.",
        "rules that punish inattention; anything you cannot learn by watching",
    ),
)


#: Private wants. The MM never sees these — they are what produce friction,
#: tangents, and side-quests rather than a decision tree.
AGENDAS: tuple[str, ...] = (
    "You want your character's worst fear to come up in play. Steer toward it, "
    "even though it's a bad idea.",
    "You think the MM's opening hook is boring. You would rather do something "
    "else, and you will try to take the party with you.",
    "You want to make the table laugh at least twice this session.",
    "You want another player's character to owe you a favour by the end.",
    "You are quietly competing with one other player for the spotlight. You will "
    "not say so.",
    "You want to solve at least one problem without rolling any dice at all.",
    "You want to end the session having learned one concrete fact about the world "
    "that nobody told you directly.",
    "You are testing whether the MM will let you do something the rules don't "
    "cover. You will try it at least once.",
    "You want to protect one specific NPC, even at cost to yourself.",
    "You are running low on patience for combat. If a fight starts, you will look "
    "for a way to end it early.",
    "You want your character to be wrong about something and have to admit it.",
    "You want to spend all your Sparks this session rather than hoarding them.",
)


@dataclass(frozen=True)
class Persona:
    player_name: str
    character_name: str
    archetype: Archetype
    agenda: str

    def describe_for_self(self) -> str:
        """The block that goes in this agent's own system prompt."""
        return (
            f"You are {self.player_name}, a player at this table, playing "
            f"{self.character_name}.\n\n"
            f"**How you play:** You are a {self.archetype.label}. You want "
            f"{self.archetype.wants}. {self.archetype.behaviour}\n\n"
            f"**Your private goal for tonight (nobody else knows this, including "
            f"the MM):** {self.agenda}\n"
        )


def assign(
    players: list[tuple[str, str]],
    seed: int,
    archetypes: tuple[Archetype, ...] = ARCHETYPES,
) -> list[Persona]:
    """Assign a distinct archetype and agenda to each (player_name, character).

    Deterministic in `seed` so an arm-paired rerun casts the same table — the A/B
    comparison in DESIGN §5 is only meaningful if the personalities match.
    """
    rng = random.Random(seed)
    picked_archetypes = rng.sample(archetypes, k=min(len(players), len(archetypes)))
    picked_agendas = rng.sample(AGENDAS, k=len(players))
    return [
        Persona(player_name=name, character_name=character,
                archetype=picked_archetypes[i % len(picked_archetypes)],
                agenda=picked_agendas[i])
        for i, (name, character) in enumerate(players)
    ]
