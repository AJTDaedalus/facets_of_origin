"""Character model — creation, validation, and skill advancement."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.facets.registry import MergedRuleset


SkillRankId = Literal["novice", "practiced", "expert"]


class SkillState(BaseModel):
    skill_id: str
    rank: SkillRankId = "novice"
    marks: int = Field(default=0, ge=0)   # marks toward next rank


class Character(BaseModel):
    """A player character. Validated against the active ruleset at creation."""

    name: str = Field(min_length=1, max_length=64)
    player_name: str = Field(min_length=1, max_length=32)
    primary_facet: str                      # character facet ID (body / mind / soul)

    # Minor attribute ratings (1/2/3). Keys are attribute IDs.
    attributes: dict[str, int] = Field(default_factory=dict)

    # Skill state keyed by skill ID
    skills: dict[str, SkillState] = Field(default_factory=dict)

    # Spark economy
    sparks: int = Field(default=3, ge=0)

    # Advancement tracking
    session_skill_points_remaining: int = Field(default=4, ge=0)
    facet_level: int = Field(default=0, ge=0)
    rank_advances_this_facet_level: int = Field(default=0, ge=0)

    # Unlocked technique IDs
    techniques: list[str] = Field(default_factory=list)

    def validate_against_ruleset(self, ruleset: MergedRuleset) -> list[str]:
        """Return a list of validation errors against the ruleset. Empty = valid."""
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
            # All minor attributes must be present
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
        rating = self.attributes.get(attribute_id, 2)
        return ruleset.get_minor_attribute_modifier(attribute_id, rating)

    def get_skill_modifier(self, skill_id: str, ruleset: MergedRuleset) -> int:
        state = self.skills.get(skill_id)
        if not state:
            return 0
        return ruleset.get_skill_rank_modifier(state.rank)

    def spend_spark(self) -> bool:
        if self.sparks <= 0:
            return False
        self.sparks -= 1
        return True

    def earn_spark(self) -> None:
        self.sparks += 1

    def advance_skill(self, skill_id: str, marks_to_add: int, ruleset: MergedRuleset) -> dict:
        """Add marks to a skill, advancing rank if threshold is met. Returns advancement info."""
        if skill_id not in self.skills:
            self.skills[skill_id] = SkillState(skill_id=skill_id)

        state = self.skills[skill_id]
        marks_per_rank = ruleset.advancement.marks_per_rank if ruleset.advancement else 3
        rank_order = ["novice", "practiced", "expert"]
        current_idx = rank_order.index(state.rank)

        result: dict = {"skill_id": skill_id, "rank_advances": 0, "facet_level_advances": 0}

        for _ in range(marks_to_add):
            if state.rank == "expert":
                break  # already maxed

            state.marks += 1
            if state.marks >= marks_per_rank:
                state.marks = 0
                state.rank = rank_order[current_idx + 1]
                current_idx += 1
                result["rank_advances"] += 1

                # Check if this skill is in the character's primary facet for level tracking
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
        return self.model_dump()


def create_default_character(
    name: str,
    player_name: str,
    primary_facet: str,
    attributes: dict[str, int],
    ruleset: MergedRuleset,
) -> tuple[Character | None, list[str]]:
    """Create a character and validate it. Returns (character, errors)."""
    # Initialise all skills at Novice
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
