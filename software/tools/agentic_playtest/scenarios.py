"""Scenario definitions for batch 08.

Everything here is drawn from canon already in the repository —
`playtest/01_thornwall_undercroft/scenario.md`, `characters/*.fof`, and
`enemies/*.fof`. Nothing is invented. `CLAUDE.md`'s iron law forbids inventing
setting material, and a playtest that contaminates the canon it is testing is
worse than no playtest.

See `playtest/08_npc_variance/scenario.md` for the human-readable pack.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Scenario:
    key: str
    title: str
    #: Given to every agent in the shared, cached prefix.
    briefing: str
    #: Given to the MM only, in its role block.
    prep: str
    enemies: list[dict] = field(default_factory=list)


#: Canon stat lines, transcribed from enemies/*.fof.
ARCHIVE_GUARDIAN = {
    "id": "archive_guardian", "name": "Archive Guardian", "tier": "boss",
    "resolve": 8, "attack_modifier": 3, "defense_modifier": 1, "armor": "heavy",
    "techniques": ["phase_change", "tier1_immunity"],
    "phases": [{"resolve_threshold": 2,
                "description": "Reduced Mode — its attacks weaken and land as "
                               "Tier 1, but it now ignores Tier 1 Conditions "
                               "entirely. It is running on something else."}],
    "description": "An ancient construct protecting the sealed vault.",
    "tactics": "Holds the vault door. Does not pursue. Strikes whoever is nearest.",
}

DUST_CONSTRUCT = {
    "id": "dust_construct", "name": "Dust Construct", "tier": "mook",
    "attack_modifier": 0, "defense_modifier": 0, "armor": "none",
    "description": "Humanoid shapes of compressed dust and old paper, animated "
                   "by residual ward magic.",
    "tactics": "Move silently. Strike with hardened limbs.",
}

HARBOR_THUG = {
    "id": "harbor_thug", "name": "Harbor Thug", "tier": "mook",
    "attack_modifier": 0, "defense_modifier": 0, "armor": "none",
    "description": "Hired muscle from the harbour district.",
}

WATCH_SERGEANT = {
    "id": "city_watch_sergeant", "name": "City Watch Sergeant", "tier": "named",
    "resolve": 3, "attack_modifier": 2, "defense_modifier": 2, "armor": "light",
    "description": "A mid-rank officer of the city watch. Fights methodically — "
                   "not inspired, but very hard to rattle. Will call for backup "
                   "if the fight runs more than two exchanges.",
    "tactics": "Measured first exchange, Defensive if Staggered. Will not go "
               "Aggressive unless the party is clearly losing.",
}


GUARDIAN_CHAMBER = Scenario(
    key="guardian_chamber",
    title="The Guardian Chamber",
    briefing="""\
You are in the sealed lower stacks beneath the Thornwall Municipal Archive. You
came down on behalf of Alderman Brost to find out what has been making noise
below, and you have reached the guardian chamber. Ward-lanterns flicker. Dust
hangs in the air where something has been moving. Ahead is a sealed vault door,
and standing before it, an ancient construct.
""",
    prep="""\
The party is at the threshold of the guardian chamber. The Archive Guardian is
not yet active — it wakes when they approach the vault door, or when they are
noticed.

Two Dust Constructs are in the room, half-collapsed among the shelves. They
animate first.

The Archive Guardian: a Boss with Resolve 8 and heavy armour. At Resolve 2 it
enters Reduced Mode — its attacks weaken and land at Tier 1, but it stops
registering Tier 1 Conditions at all. Narrate that shift when it happens; it is
running on something other than its senses.

The Guardian can be deactivated with the right knowledge or the right magic.
Do not volunteer this. If a player looks for it, let them find it — that is a
legitimate way for this to end and is worth more than a fight you steered them
into.

Behind the vault door: sealed documents, a century old — contracts, debts,
material somebody would pay to keep quiet. You do not have to open it tonight.
""",
    enemies=[ARCHIVE_GUARDIAN, DUST_CONSTRUCT],
)


ALDERMANS_OFFICE = Scenario(
    key="aldermans_office",
    title="The Alderman's Office",
    briefing="""\
You are in Alderman Brost's office above the Thornwall Municipal Archive. He
asked for you by name, through a mutual contact. The lower stacks — sealed for
decades — have been making noises, and he wants investigators who are not the
Watch. In the outer room a young clerk named Lira is waiting; she went down two
days ago and came back shaking.
""",
    prep="""\
Alderman Brost wants the sealed documents in the vault. They contain proof of his
family's historical land claims. That is his real reason and he will not say it.

His secret: he knows exactly what is down there. The noises are real, but he has
been waiting for an excuse to send someone in. He offers 50 silver and a favour
from the Archive.

He speaks with his hands folded precisely on the desk and never gestures.

Lira, in the outer room, keeps touching the back of her neck where something cold
brushed her. If asked: "It wasn't an animal. It moved like purpose. Like it was
looking for something that wasn't me."

This is a conversation, not a fight. The party may take the job, negotiate, refuse
it, investigate Brost instead, or walk out — all of those are fine and none of
them are wrong. Do not steer them back to the job.

If it does turn — if they threaten him, or rob the office — Brost can call the
Watch: a Sergeant and two hired hands from the harbour. The Sergeant is very hard
to rattle and fights methodically; he calls for backup if it runs past two
exchanges. The thugs do not want to die for this job and will run if he goes down.
""",
    enemies=[HARBOR_THUG, WATCH_SERGEANT],
)


SCENARIOS = {s.key: s for s in (GUARDIAN_CHAMBER, ALDERMANS_OFFICE)}


#: The canon party, transcribed from characters/*.fof, plus a fourth seat built
#: to the same 18-point standard so the table is four-handed.
PARTY = [
    {"player_name": "Sophia", "character_name": "Zahna", "primary_facet": "mind",
     "attributes": {"strength": 1, "dexterity": 3, "constitution": 1,
                    "intelligence": 3, "wisdom": 1, "knowledge": 3,
                    "spirit": 2, "luck": 3, "charisma": 1},
     "background_id": "guild_apprentice", "magic_domain": "inscription"},
    {"player_name": "Luke", "character_name": "Mordai", "primary_facet": "body",
     "attributes": {"strength": 3, "dexterity": 2, "constitution": 3,
                    "intelligence": 1, "wisdom": 1, "knowledge": 2,
                    "spirit": 2, "luck": 2, "charisma": 2},
     "background_id": "city_watch_veteran"},
    {"player_name": "Penny", "character_name": "Zulnut", "primary_facet": "body",
     "attributes": {"strength": 2, "dexterity": 3, "constitution": 1,
                    "intelligence": 2, "wisdom": 2, "knowledge": 2,
                    "spirit": 1, "luck": 3, "charisma": 2}},
    {"player_name": "Toby", "character_name": "Ilesse", "primary_facet": "soul",
     "attributes": {"strength": 1, "dexterity": 2, "constitution": 2,
                    "intelligence": 2, "wisdom": 3, "knowledge": 2,
                    "spirit": 3, "luck": 2, "charisma": 1},
     "background_id": "temple_acolyte"},
]

CAST_BLURB = """\
Sophia plays Zahna — a Mind-Facet Guild Apprentice, sharp and quick, with the
Inscription domain and no combat training to speak of.
Luke plays Mordai — a Body-Facet City Watch Veteran, strong and durable, the one
who stands in front.
Penny plays Zulnut — a Body-Facet Wandering Disciple, fast and light-footed,
monk-adjacent, more finesse than force.
Toby plays Ilesse — a Soul-Facet Temple Acolyte, watchful and steady, the one who
notices things.
"""
