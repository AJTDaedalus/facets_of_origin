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
    """A single unlockable Technique in a Facet's Technique tree.

    Fields:
        id: Slug identifier (e.g. "sharp_analysis").
        prerequisites: IDs of Techniques that must be unlocked before this one.
        has_choice: True if the player picks from a list when selecting this Technique
                    (e.g., choosing a magic domain).
        choice_prompt: Human-readable prompt shown when has_choice is True.
        magic_granting: True if selecting this Technique sets magic_technique_active = True
                        on the character. Replaces hardcoded ID checks in the engine.
    """

    id: str
    name: str
    description: str
    prerequisites: list[str] = Field(default_factory=list)
    has_choice: bool = False
    choice_prompt: str = ""
    magic_granting: bool = False


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


class OutcomeTierDef(BaseModel):
    """One outcome tier in the roll resolution system.

    Fields:
        id: Machine-readable identifier (e.g. "full_success", "critical", "fumble").
        threshold: Minimum total to reach this tier. None = catch-all lowest tier.
        label: Human-readable name shown to players.
        description: Narrative prompt for the outcome.
    """

    id: str
    threshold: int | None = None
    label: str
    description: str


class RollResolutionDef(BaseModel):
    dice: str = "2d6"
    modifier_source: str = "minor_attribute"
    thresholds: dict[str, int]           # {"full_success": 10, "partial_success": 7}
    outcomes: OutcomesDef
    difficulty_modifiers: list[DifficultyModifier] = Field(default_factory=list)
    outcome_tiers: list[OutcomeTierDef] = Field(default_factory=list)


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
    """A pre-built character background (PHB II.5).

    Fields:
        facet: The primary Facet this background belongs to ("body" | "mind" | "soul").
        starting_skill: Skill ID that begins at Practiced rank.
        secondary_skill: Skill ID that begins at Novice with 1 mark. Null for magic
                         backgrounds (domain_origin replaces the secondary skill slot).
        specialty: Narrow fictional expertise that eases directly applicable rolls.
        domain_origin: "mind" | "soul" | null. Set on magic-granting backgrounds to
                       indicate which domain list the player chooses from.
    """

    id: str
    name: str
    facet: str
    starting_skill: str
    secondary_skill: Optional[str] = None
    specialty: str
    domain_origin: Optional[str] = None


# ---------------------------------------------------------------------------
# Combat (PHB III.3)
# ---------------------------------------------------------------------------

class CombatConditionDef(BaseModel):
    """A single named combat condition.

    Fields:
        id: Slug identifier (e.g. "winded", "staggered", "broken").
        clears: When this condition is removed:
                "end_of_exchange" | "treated" | "end_of_scene".
        description: Human-readable effect summary.
    """

    id: str
    clears: str
    description: str


class CombatConditionsTierDef(BaseModel):
    tier1: list[CombatConditionDef] = Field(default_factory=list)
    tier2: list[CombatConditionDef] = Field(default_factory=list)
    tier3: list[CombatConditionDef] = Field(default_factory=list)


class EnduranceDef(BaseModel):
    """Endurance pool configuration.

    Fields:
        base: Starting Endurance before Constitution and skill modifiers.
        recovery_withdrawn: Endurance restored per exchange when posture is Withdrawn.
    """

    base: int = 4
    recovery_withdrawn: int = 2


class ArmorEntryDef(BaseModel):
    """One armor tier's downgrade rule.

    Fields:
        downgrades: Number of Condition tiers this armor downgrades (e.g. 1 = Tier 2→1).
    """

    downgrades: int = 1


class ArmorDef(BaseModel):
    """Armor downgrade rules keyed by armor type ("light", "heavy")."""

    light: ArmorEntryDef = Field(default_factory=ArmorEntryDef)
    heavy: ArmorEntryDef = Field(default_factory=lambda: ArmorEntryDef(downgrades=2))


class CombatDef(BaseModel):
    """Full combat rule set loaded from facet.yaml (PHB III.3).

    The structured sub-models (endurance, conditions, armor) are read by the
    engine for data-driven behaviour. Remaining sections (postures, reactions,
    press, strike_outcomes) are informational and stored as open dicts until
    more structured models are needed.
    """

    endurance: EnduranceDef = Field(default_factory=EnduranceDef)
    postures: dict[str, Any] = Field(default_factory=dict)
    reactions: dict[str, Any] = Field(default_factory=dict)
    press: dict[str, Any] = Field(default_factory=dict)
    conditions: CombatConditionsTierDef = Field(default_factory=CombatConditionsTierDef)
    armor: ArmorDef = Field(default_factory=ArmorDef)
    strike_outcomes: dict[str, Any] = Field(default_factory=dict)
    endurance_floor_rule: str = ""
    mook_rule: str = ""
    named_npc_rule: str = ""
    boss_rule: str = ""


# ---------------------------------------------------------------------------
# Magic (PHB II.3)
# ---------------------------------------------------------------------------

class MagicDomainDef(BaseModel):
    """A single magic domain (e.g. Fire, Inscription, Fate).

    Fields:
        type: Difficulty tier — "focused" (Easy/Standard/Hard),
              "standard" (Standard/Hard/Very Hard),
              "broad" (Hard/VH/VH, Sparks cannot push scope ceiling).
        tradition: Which attribute governs rolls — "intuitive" (Spirit) or
                   "scholarly" (Knowledge).
        requires_tier3: True for Prismatic domains that need a Tier 3 Technique.
    """

    id: str
    name: str
    type: Literal["focused", "standard", "broad"]
    tradition: str
    description: str
    requires_tier3: bool = False


class MagicDef(BaseModel):
    """Full magic configuration for a Facet module (PHB II.3).

    Fields:
        domain_types: Maps type keys ("focused" | "standard" | "broad") to
                      {"scope_difficulties": {"minor": "Easy", ...}}.
        pre_technique_scope_limit: Maximum scope before the Facet Technique is unlocked.
                                   Default "minor".
        pre_technique_difficulty_penalty: Steps harder applied before Technique.
                                          Default 1.
        soul_domains: Domains available to Soul Facet characters.
        mind_domains: Domains available to Mind Facet characters.
    """

    traditions: dict[str, Any] = Field(default_factory=dict)
    domain_types: dict[str, Any] = Field(default_factory=dict)
    pre_technique_penalty: str = "1_step_harder"
    pre_technique_scope_limit: str = "minor"       # scope ceiling before Technique is unlocked
    pre_technique_difficulty_penalty: int = 1       # number of difficulty steps harder pre-Technique
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
