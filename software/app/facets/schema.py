"""Pydantic schema for Facet YAML files — the ruleset data format."""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# Attributes
# ---------------------------------------------------------------------------

class AttributeRating(BaseModel):
    rating: int = Field(ge=1, le=10)
    label: str
    modifier: int


class MajorAttributeDef(BaseModel):
    id: str
    name: str
    description: str
    minor_attributes: list[str]   # IDs of minor attributes that roll up to this


class MinorAttributeDef(BaseModel):
    id: str
    name: str
    description: str
    major: str                    # ID of the parent major attribute


class AttributeDistribution(BaseModel):
    total_points: int
    min_per_attribute: int
    max_per_attribute: int


class AttributesDef(BaseModel):
    major: list[MajorAttributeDef] = Field(default_factory=list)
    minor: list[MinorAttributeDef] = Field(default_factory=list)
    ratings: list[AttributeRating] = Field(default_factory=list)
    distribution: AttributeDistribution | None = None


# ---------------------------------------------------------------------------
# Character Facets (archetypes)
# ---------------------------------------------------------------------------

class CharacterFacetDef(BaseModel):
    id: str
    name: str
    description: str
    major_attribute: str          # ID of the major attribute this Facet draws from


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

class SkillDef(BaseModel):
    id: str
    name: str
    facet: str                    # character facet ID
    attribute: str                # minor attribute ID
    description: str
    status: Literal["active", "stub", "removed"] = "active"


# ---------------------------------------------------------------------------
# Techniques
# ---------------------------------------------------------------------------

class TechniqueDef(BaseModel):
    id: str
    name: str
    description: str
    prerequisites: list[str] = Field(default_factory=list)   # IDs of required techniques
    has_choice: bool = False
    choice_prompt: str = ""


class TierDef(BaseModel):
    tier: int = Field(ge=1, le=3)
    techniques: list[TechniqueDef]


class BranchDef(BaseModel):
    id: str
    name: str
    attribute: str                # minor attribute this branch focuses on
    tiers: list[TierDef]


class FacetTreeDef(BaseModel):
    branches: list[BranchDef]


# ---------------------------------------------------------------------------
# Roll Resolution
# ---------------------------------------------------------------------------

class OutcomeLabel(BaseModel):
    label: str
    description: str


class OutcomesDef(BaseModel):
    full_success: OutcomeLabel
    partial_success: OutcomeLabel
    failure: OutcomeLabel


class DifficultyModifier(BaseModel):
    label: str
    modifier: int
    description: str


class RollResolutionDef(BaseModel):
    dice: str = "2d6"
    modifier_source: str = "minor_attribute"
    thresholds: dict[str, int]           # {"full_success": 10, "partial_success": 7}
    outcomes: OutcomesDef
    difficulty_modifiers: list[DifficultyModifier] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Spark Economy
# ---------------------------------------------------------------------------

class SparkMechanicDef(BaseModel):
    spend: str
    description: str


class SparkEarnMethod(BaseModel):
    id: str
    label: str
    description: str


class SparkDef(BaseModel):
    base_sparks_per_session: int = Field(ge=0)
    mechanic: SparkMechanicDef
    earn_methods: list[SparkEarnMethod] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Advancement
# ---------------------------------------------------------------------------

class SkillRankDef(BaseModel):
    id: str
    label: str
    modifier: int
    default: bool = False


class SkillPointCostDef(BaseModel):
    context: str
    cost: int


class AdvancementDef(BaseModel):
    skill_ranks: list[SkillRankDef] = Field(default_factory=list)
    skill_point_costs: list[SkillPointCostDef] = Field(default_factory=list)
    session_skill_points: int = 4
    marks_per_rank: int = 3
    facet_level_threshold: int = 6
    major_advancement_threshold: int = 4   # total Facet levels before a Major Advancement


# ---------------------------------------------------------------------------
# Backgrounds (PHB II.5)
# ---------------------------------------------------------------------------

class BackgroundDefinition(BaseModel):
    id: str
    name: str
    facet: str                          # primary facet this background belongs to
    starting_skill: str                 # begins at Practiced
    secondary_skill: Optional[str] = None  # begins at Novice with 1 mark; null for magic backgrounds
    specialty: str
    domain_origin: Optional[str] = None  # "mind" | "soul" | null


# ---------------------------------------------------------------------------
# Combat (PHB III.3)
# ---------------------------------------------------------------------------

class CombatConditionDef(BaseModel):
    id: str
    clears: str                     # "end_of_exchange" | "treated" | "end_of_scene"
    description: str


class CombatConditionsTierDef(BaseModel):
    tier1: list[CombatConditionDef] = Field(default_factory=list)
    tier2: list[CombatConditionDef] = Field(default_factory=list)
    tier3: list[CombatConditionDef] = Field(default_factory=list)


class CombatDef(BaseModel):
    endurance: dict[str, Any] = Field(default_factory=dict)
    postures: dict[str, Any] = Field(default_factory=dict)
    reactions: dict[str, Any] = Field(default_factory=dict)
    press: dict[str, Any] = Field(default_factory=dict)
    conditions: CombatConditionsTierDef = Field(default_factory=CombatConditionsTierDef)
    armor: dict[str, Any] = Field(default_factory=dict)
    strike_outcomes: dict[str, Any] = Field(default_factory=dict)
    endurance_floor_rule: str = ""
    mook_rule: str = ""
    named_npc_rule: str = ""
    boss_rule: str = ""


# ---------------------------------------------------------------------------
# Magic (PHB II.3)
# ---------------------------------------------------------------------------

class MagicDomainDef(BaseModel):
    id: str
    name: str
    type: Literal["focused", "standard", "broad"]
    tradition: str                  # "intuitive" | "scholarly"
    description: str
    requires_tier3: bool = False    # Prismatic domains require Tier 3 Technique


class MagicDef(BaseModel):
    traditions: dict[str, Any] = Field(default_factory=dict)
    domain_types: dict[str, Any] = Field(default_factory=dict)
    pre_technique_penalty: str = "1_step_harder"
    soul_domains: list[MagicDomainDef] = Field(default_factory=list)
    mind_domains: list[MagicDomainDef] = Field(default_factory=list)

    @property
    def all_domains(self) -> list[MagicDomainDef]:
        return self.soul_domains + self.mind_domains

    def get_domain(self, domain_id: str) -> Optional[MagicDomainDef]:
        for d in self.all_domains:
            if d.id == domain_id:
                return d
        return None


# ---------------------------------------------------------------------------
# Root Facet File
# ---------------------------------------------------------------------------

class FacetFile(BaseModel):
    id: str
    name: str
    version: str
    authors: list[str] = Field(default_factory=list)
    description: str = ""
    priority: int = 10            # base ruleset uses 0; optional modules use higher values

    attributes: AttributesDef = Field(default_factory=AttributesDef)
    facets: list[CharacterFacetDef] = Field(default_factory=list)
    skills: list[SkillDef] = Field(default_factory=list)
    techniques: dict[str, FacetTreeDef] = Field(default_factory=dict)  # keyed by character facet ID
    backgrounds: list[BackgroundDefinition] = Field(default_factory=list)
    roll_resolution: RollResolutionDef | None = None
    spark: SparkDef | None = None
    advancement: AdvancementDef | None = None
    combat: CombatDef | None = None
    magic: MagicDef | None = None

    @field_validator("id")
    @classmethod
    def id_is_slug(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Facet ID must be a slug (alphanumeric, hyphens, underscores only).")
        return v
