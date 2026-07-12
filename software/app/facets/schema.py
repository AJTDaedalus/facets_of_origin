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
        grants_prismatic_domain: True for Ascendant Domain (Tier 3). The choice is an
                        *additional* prismatic domain — it lands in `ascendant_domain`
                        and leaves the character's original `magic_domain` untouched
                        (PHB II.4b/II.4c: "Your original domain is unchanged").
                        Without this, `magic_granting` would overwrite the original.
        grants_secondary_domain: True for Second Domain (Tier 3). The choice lands in
                        `secondary_magic_domain`, which the engine taxes one difficulty
                        step harder. Standard domains only — prismatic territories
                        require Ascendant Domain instead (II.4c).
    """

    id: str
    name: str
    description: str
    prerequisites: list[str] = Field(default_factory=list)
    has_choice: bool = False
    choice_prompt: str = ""
    magic_granting: bool = False
    grants_prismatic_domain: bool = False
    grants_secondary_domain: bool = False


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
    structured: bool = False
    target_per_session: str = ""


class SparkVariantsDef(BaseModel):
    """Untested/optional rule variants, kept off by default (D6).

    Fields:
        refund_on_failed_pretechnique_cast: If true, a failed pre-Technique
            magic cast refunds its Spark cost. Measured by PT04 (WD8) but
            not adopted — the flag exists so the sim/harness can toggle it.
    """

    refund_on_failed_pretechnique_cast: bool = False


class SparkDef(BaseModel):
    base_sparks_per_session: int = Field(ge=0)
    mechanic: SparkMechanicDef
    earn_methods: list[SparkEarnMethod] = Field(default_factory=list)
    variants: SparkVariantsDef = Field(default_factory=SparkVariantsDef)


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
        secondary_skill: Skill ID that begins at Novice with 1 mark.
        specialty: Narrow fictional expertise that eases directly applicable rolls.
        domain_origin: "mind" | "soul" | null. Set on magic-granting backgrounds to
                       indicate which domain list the player chooses from.
        domain_replaces_secondary: If true, choosing a magic domain skips the
                                   secondary skill (Guild Apprentice, Hedge Scholar).
                                   If false, both are granted (Temple Acolyte).
    """

    id: str
    name: str
    facet: str
    starting_skill: str
    secondary_skill: Optional[str] = None
    specialty: str
    domain_origin: Optional[str] = None
    domain_replaces_secondary: bool = False


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
        offense_modifier: Modifier this condition applies to the holder's
                offensive rolls. Staggered is −1 ("−1 to offensive rolls",
                PHB III.3); every other condition is 0. Machine-readable so
                `combat.offense_modifier` reads the penalty instead of
                hardcoding it — the penalty used to exist only in the
                `description` prose and a literal in `combat.py`.
    """

    id: str
    clears: str
    description: str
    offense_modifier: int = 0


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
    """One armor tier's per-scene Condition-downgrade budget for player
    characters (D2).

    Fields:
        downgrades_per_scene: Number of incoming Conditions this armor
                              downgrades before the budget is spent. The
                              budget resets at end of **scene**, never end
                              of exchange or end of fight — two fights
                              inside one scene share the budget.
        tiers_reduced: Number of Condition tiers each downgrade removes
                       (e.g. 1 = Tier 2 -> Tier 1; Tier 1 -> none).
    """

    downgrades_per_scene: int = 2
    tiers_reduced: int = 1


class ArmorDef(BaseModel):
    """PC armor downgrade rules keyed by armor type ("light", "heavy")."""

    light: ArmorEntryDef = Field(default_factory=ArmorEntryDef)
    heavy: ArmorEntryDef = Field(
        default_factory=lambda: ArmorEntryDef(downgrades_per_scene=4)
    )


class StrikeDepletionDef(BaseModel):
    """Resolve depletion an enemy takes from a PC Strike, keyed by outcome tier."""

    full_success: int = 2
    partial_success: int = 1
    failure: int = 0


class ArmorResolveBonusDef(BaseModel):
    """Flat Resolve bonus an enemy's armor grants (D1). Numerically equal to
    the Threat Rating formula's `armor_bonus` term — the TR identity."""

    none: int = 0
    light: int = 1
    heavy: int = 2


class EnemyDurabilityDef(BaseModel):
    """Enemy Resolve pool rules (D1): depletion, armor bonus, and Mook removal.

    Fields:
        strike_depletion: Resolve lost per PC Strike outcome tier.
        armor_resolve_bonus: Flat Resolve granted by enemy armor.
        mook_removed_on: Outcome tier that removes an unarmored Mook.
        armored_mook_removed_on: Outcome tier that removes an armored Mook.
    """

    strike_depletion: StrikeDepletionDef = Field(default_factory=StrikeDepletionDef)
    armor_resolve_bonus: ArmorResolveBonusDef = Field(default_factory=ArmorResolveBonusDef)
    mook_removed_on: str = "partial_success"
    armored_mook_removed_on: str = "full_success"


class CombatDef(BaseModel):
    """Full combat rule set loaded from facet.yaml (PHB III.3).

    The structured sub-models (endurance, conditions, armor, enemy_durability)
    are read by the engine for data-driven behaviour. Remaining sections
    (postures, reactions, press, strike_outcomes) are informational and
    stored as open dicts until more structured models are needed.
    """

    endurance: EnduranceDef = Field(default_factory=EnduranceDef)
    postures: dict[str, Any] = Field(default_factory=dict)
    reactions: dict[str, Any] = Field(default_factory=dict)
    press: dict[str, Any] = Field(default_factory=dict)
    conditions: CombatConditionsTierDef = Field(default_factory=CombatConditionsTierDef)
    armor: ArmorDef = Field(default_factory=ArmorDef)
    enemy_durability: EnemyDurabilityDef = Field(default_factory=EnemyDurabilityDef)
    strike_outcomes: dict[str, Any] = Field(default_factory=dict)
    endurance_floor_rule: str = ""
    mook_rule: str = ""
    named_npc_rule: str = ""
    boss_rule: str = ""


# ---------------------------------------------------------------------------
# Hazards & Death (PHB III.2 — D4)
# ---------------------------------------------------------------------------

class ThreatClockDef(BaseModel):
    """A visible-to-the-table pressure clock (PHB III.2).

    Fields:
        segments: Total segments before the clock fills and the hazard strikes.
        advances_on: Outcome tiers (roll_resolution ids) that advance the clock
                     by one segment when rolled near the hazard.
        wind_back_cost: Narrative cost description for winding the clock back
                        one segment (e.g. "1_action").
        wind_back_requires_roll: Always False by design (Brain, BRIEF §EF4) — a
                                  rolled wind-back would let a 7-9 advance the
                                  very clock being wound.
    """

    segments: int = Field(default=4, ge=1)
    advances_on: list[str] = Field(
        default_factory=lambda: ["partial_success", "failure"]
    )
    wind_back_cost: str = "1_action"
    wind_back_requires_roll: bool = False


class HazardsDef(BaseModel):
    threat_clock: ThreatClockDef = Field(default_factory=ThreatClockDef)


class DeathDef(BaseModel):
    """Death rule (PHB III.2): Broken is never lethal by itself.

    Fields:
        broken_is_lethal: Always False — a Broken Condition alone never ends
                           a character's life.
        doom_gate: The two player-chosen outcomes when a Broken result would
                   end a character's life in the fiction.
    """

    broken_is_lethal: bool = False
    doom_gate: list[str] = Field(
        default_factory=lambda: ["permanent_scar", "heroic_death"]
    )


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
        pre_technique_difficulty_penalty: No additional difficulty penalty pre-Technique.
                                          Default 0 (scope restriction alone is the penalty).
        soul_domains: Domains available to Soul Facet characters.
        mind_domains: Domains available to Mind Facet characters.
    """

    traditions: dict[str, Any] = Field(default_factory=dict)
    domain_types: dict[str, Any] = Field(default_factory=dict)
    pre_technique_penalty: str = "scope_only"
    pre_technique_scope_limit: str = "minor"       # scope ceiling before Technique is unlocked
    pre_technique_difficulty_penalty: int = 0       # no additional difficulty penalty pre-Technique
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
    hazards: HazardsDef | None = None
    death: DeathDef | None = None

    @field_validator("id")
    @classmethod
    def id_is_slug(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Facet ID must be a slug (alphanumeric, hyphens, underscores only).")
        return v
