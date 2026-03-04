"""Character model — creation, validation, and skill advancement."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.facets.registry import MergedRuleset


SkillRankId = Literal["novice", "practiced", "expert"]


class SkillState(BaseModel):
    """Tracks a character's current rank and advancement marks for one skill.

    Attributes:
        skill_id: The skill's canonical ID (e.g. "athletics").
        rank: Current proficiency tier: novice (default), practiced, or expert.
        marks: Progress marks toward the next rank. Resets to 0 on rank advance.
    """

    skill_id: str
    rank: SkillRankId = "novice"
    marks: int = Field(default=0, ge=0)


class Character(BaseModel):
    """A player character. Validated against the active ruleset at creation.

    Attributes:
        name: The character's in-fiction name (1–64 characters).
        player_name: The player's display name; keys the character in the session store.
        primary_facet: The character's chosen Facet ID (e.g. "body", "mind", "soul").
        attributes: Minor attribute ratings keyed by attribute ID. Values are 1, 2, or 3.
        skills: SkillState instances keyed by skill ID.
        sparks: Current unspent Spark tokens. Starts at the ruleset's base_sparks_per_session.
        session_skill_points_remaining: Points left to spend on skill advancement this session.
        facet_level: How many Facet levels the character has earned.
        rank_advances_this_facet_level: Rank advances toward the next Facet level threshold.
        techniques: List of unlocked technique IDs.
    """

    name: str = Field(min_length=1, max_length=64)
    player_name: str = Field(min_length=1, max_length=32)
    primary_facet: str

    attributes: dict[str, int] = Field(default_factory=dict)
    skills: dict[str, SkillState] = Field(default_factory=dict)

    sparks: int = Field(default=3, ge=0)

    session_skill_points_remaining: int = Field(default=4, ge=0)
    facet_level: int = Field(default=0, ge=0)
    rank_advances_this_facet_level: int = Field(default=0, ge=0)

    techniques: list[str] = Field(default_factory=list)

    def validate_against_ruleset(self, ruleset: MergedRuleset) -> list[str]:
        """Return a list of validation errors against the ruleset. Empty list = valid.

        Checks:
        - Primary facet must exist in the ruleset.
        - All attribute IDs must be recognised.
        - All attribute ratings must be within valid_ratings.
        - If the ruleset specifies a distribution, all attributes must be present,
          total must match, and each must be within min/max bounds.
        - All skill IDs must be recognised.
        """
        errors: list[str] = []

        # Primary facet must exist
        facet_ids = {cf.id for cf in ruleset.character_facets}
        if self.primary_facet not in facet_ids:
            errors.append(f"Unknown primary facet '{self.primary_facet}'. Must be one of: {', '.join(facet_ids)}.")

        # All minor attributes must exist and be in range
        dist = ruleset.attribute_distribution
        known_minor = {ma.id for ma in ruleset.minor_attributes}
        valid_ratings = {r.rating for r in ruleset.attribute_ratings}

        for attr_id, rating in self.attributes.items():
            if attr_id not in known_minor:
                errors.append(f"Unknown attribute '{attr_id}'.")
                continue
            if rating not in valid_ratings:
                errors.append(f"Attribute '{attr_id}' has invalid rating {rating}. Valid: {sorted(valid_ratings)}.")

        if dist:
            missing = known_minor - set(self.attributes.keys())
            if missing:
                errors.append(f"Missing attributes: {', '.join(sorted(missing))}.")

            total = sum(self.attributes.values())
            if total != dist.total_points:
                errors.append(f"Total attribute points must equal {dist.total_points}, got {total}.")

            for attr_id, rating in self.attributes.items():
                if rating < dist.min_per_attribute:
                    errors.append(f"Attribute '{attr_id}' is {rating}, minimum is {dist.min_per_attribute}.")
                if rating > dist.max_per_attribute:
                    errors.append(f"Attribute '{attr_id}' is {rating}, maximum is {dist.max_per_attribute}.")

        # Skills must reference known skills
        known_skills = {sk.id for sk in ruleset.skills}
        for skill_id in self.skills:
            if skill_id not in known_skills:
                errors.append(f"Unknown skill '{skill_id}'.")

        return errors

    def get_attribute_modifier(self, attribute_id: str, ruleset: MergedRuleset) -> int:
        """Return the numeric modifier for one of this character's attributes."""
        rating = self.attributes.get(attribute_id, 2)
        return ruleset.get_minor_attribute_modifier(attribute_id, rating)

    def get_skill_modifier(self, skill_id: str, ruleset: MergedRuleset) -> int:
        """Return the numeric modifier for a skill. Returns 0 if skill is unknown."""
        state = self.skills.get(skill_id)
        if not state:
            return 0
        return ruleset.get_skill_rank_modifier(state.rank)

    def spend_spark(self) -> bool:
        """Spend one Spark. Returns True on success, False if no Sparks remain."""
        if self.sparks <= 0:
            return False
        self.sparks -= 1
        return True

    def earn_spark(self) -> None:
        """Award one Spark to this character."""
        self.sparks += 1

    def advance_skill(self, skill_id: str, marks_to_add: int, ruleset: MergedRuleset) -> dict:
        """Add marks to a skill, advancing rank if the threshold is met.

        Creates the skill at Novice rank if it does not yet exist on the character.
        Stops adding marks once Expert rank is reached.

        Args:
            skill_id: The skill to advance.
            marks_to_add: Number of marks to add (0 is a no-op).
            ruleset: Used to look up marks_per_rank, advancement config, and skill facet.

        Returns:
            A dict with keys: skill_id, rank_advances (int), facet_level_advances (int).
        """
        if skill_id not in self.skills:
            self.skills[skill_id] = SkillState(skill_id=skill_id)

        state = self.skills[skill_id]
        marks_per_rank = ruleset.advancement.marks_per_rank if ruleset.advancement else 3
        rank_order = ["novice", "practiced", "expert"]
        current_idx = rank_order.index(state.rank)

        result: dict = {"skill_id": skill_id, "rank_advances": 0, "facet_level_advances": 0}

        for _ in range(marks_to_add):
            if state.rank == "expert":
                break

            state.marks += 1
            if state.marks >= marks_per_rank:
                state.marks = 0
                state.rank = rank_order[current_idx + 1]
                current_idx += 1
                result["rank_advances"] += 1

                sk_def = ruleset.get_skill(skill_id)
                if sk_def and sk_def.facet == self.primary_facet:
                    self.rank_advances_this_facet_level += 1
                    threshold = ruleset.advancement.facet_level_threshold if ruleset.advancement else 6
                    if self.rank_advances_this_facet_level >= threshold:
                        self.facet_level += 1
                        self.rank_advances_this_facet_level = 0
                        result["facet_level_advances"] += 1

        return result

    def to_client_dict(self) -> dict:
        """Serialize the character to a JSON-safe dict for sending to clients."""
        return self.model_dump()


def create_default_character(
    name: str,
    player_name: str,
    primary_facet: str,
    attributes: dict[str, int],
    ruleset: MergedRuleset,
) -> tuple[Character | None, list[str]]:
    """Create a character and validate it against the ruleset.

    Initialises all active skills at Novice rank.

    Args:
        name: Character's in-fiction name.
        player_name: Player's display name (used as the session key).
        primary_facet: Chosen Facet ID.
        attributes: Minor attribute ratings (must satisfy the ruleset's distribution rules).
        ruleset: The session's merged ruleset.

    Returns:
        A tuple (Character, []) on success, or (None, [error strings]) on validation failure.
    """
    skills = {sk.id: SkillState(skill_id=sk.id) for sk in ruleset.skills if sk.status == "active"}
    sparks = ruleset.spark.base_sparks_per_session if ruleset.spark else 3
    session_points = ruleset.advancement.session_skill_points if ruleset.advancement else 4

    character = Character(
        name=name,
        player_name=player_name,
        primary_facet=primary_facet,
        attributes=attributes,
        skills=skills,
        sparks=sparks,
        session_skill_points_remaining=session_points,
    )

    errors = character.validate_against_ruleset(ruleset)
    if errors:
        return None, errors

    return character, []
