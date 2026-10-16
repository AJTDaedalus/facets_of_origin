"""Pydantic schema for Facet YAML files — the ruleset data format."""
from __future__ import annotations

import warnings
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


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


class MajorDerivationBandDef(BaseModel):
    """One band of the Major Attribute modifier table (II.2, Deriving Your
    Major Attribute Modifiers): a sum of the three Minor Attributes under a
    Major maps to a modifier.
    """

    min_sum: int
    max_sum: int
    modifier: int


class AttributesDef(BaseModel):
    major: list[MajorAttributeDef] = Field(default_factory=list)
    minor: list[MinorAttributeDef] = Field(default_factory=list)
    ratings: list[AttributeRating] = Field(default_factory=list)
    distribution: AttributeDistribution | None = None
    major_derivation: list[MajorDerivationBandDef] = Field(default_factory=list)


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

class StepTriggerDef(BaseModel):
    """The condition under which a Technique's `difficulty_step` fires (B4 Q1,
    DESIGN_technique_difficulty.md §2.3).

    Two kinds:
        "auto": the app evaluates the trigger itself from roll context data it
                already holds (e.g. `weapon_category`), and the step applies
                without asking the player — the roll banner shows it happened.
        "declared": the trigger is a fictional judgement call no data can
                settle (e.g. "an unexpected angle of attack"), so the player
                toggles it on the roll.

    Fields:
        kind: "auto" | "declared".
        match: For "auto" only — the roll-context field name to check
               (e.g. "weapon_category", "hazard_type", "knowledge_field",
               "skill_id"). Unused (None) for "declared".
        against: For "auto" only — what `match`'s context value must equal
                 to fire. Either the literal string "choice" (compare
                 against the character's `technique_choices[technique_id]`)
                 or a literal value to compare against directly (e.g.
                 Steady Hand's `skill_id == "finesse"`). Unused (None) for
                 "declared".
    """

    kind: Literal["auto", "declared"]
    match: str | None = None
    against: str | None = None
    #: When set, the trigger only fires on a roll using this skill. The
    #: book scopes some Techniques to one skill — Acclimated is "Endurance
    #: rolls against your chosen hardship", Field of Mastery is "Lore rolls
    #: that fall within your chosen field". Without this conjunct the engine
    #: implements a broader rule than the printed one.
    requires_skill: str | None = None


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
        penalty_expires: "next_facet_level" | None (T4.2/D9). On a
                        `grants_secondary_domain` Technique, declares that the
                        one-step penalty lifts at the character's next Facet
                        level after acquisition — `select_technique` records
                        the acquisition level so the engine can honor the
                        expiry. None (the default) leaves any penalty
                        permanent, the pre-D9 behavior.
        requires_domain: Facet id ("mind" or "soul") whose domain list the character
                        must already hold a domain from — Second Domain and Ascendant
                        Domain both require an existing domain in their own tree
                        (PHB II.4b/II.4c). Encoded explicitly rather than left as a
                        side effect of the prerequisite chain, since the chain is not
                        guaranteed to route through the Facet's domain-granting
                        Technique (sync report H-2).
        difficulty_step: "easier" | "harder" | None (B4 Q1). If set, this
                        Technique — once unlocked and its `step_trigger`
                        satisfied — shifts a roll's declared difficulty one
                        rung. Composed by `app.game.combat
                        .apply_character_difficulty_step`, never applied
                        inline by a caller. Optional and defaults to None so
                        every Technique that predates B4 Q1 parses unchanged.
        step_trigger: The `StepTriggerDef` gating `difficulty_step`. Required
                        in practice whenever `difficulty_step` is set, but not
                        enforced by the schema — a Technique with a step and
                        no trigger simply never fires (see combat.py).
        choices: The machine-readable option list for a `has_choice` Technique
                        that is not domain-granting (DESIGN §8 / TD-19)  —
                        e.g. Weapon Mastery's `blades`/`blunt`/`polearms`/
                        `unarmed`. `choice_prompt` stays the human-readable
                        label printed in the book; `choices` is what the
                        client renders a picker from and what
                        `technique_choices[tech_id]` is expected to hold.
                        Optional and defaults to `None` so every Technique
                        that predates TD-19 (including domain-granting ones,
                        which build their option list from the domain
                        catalog instead) parses unchanged. For Techniques
                        whose fiction is deliberately open-ended (Field of
                        Mastery), the list is suggestions, not a closed set —
                        nothing in the schema or the engine enforces
                        membership (INV-8).
        removes_target_from_conflict: True only for *The Final Blow* (B4 Q3
                        / TD-12). Marks a Technique as a **licensed
                        override** — III.3's rule that the Open tag never
                        defeats an enemy on its own (Resolve does) does
                        not apply to a Technique
                        carrying this flag. The engine resolves its use as
                        a defeat event through the canonical defeat path
                        (`combat.apply_final_blow_removal`), never a raw
                        `resolve_current` write (P11 invariant). A flag,
                        not a mechanism — kept explicit and greppable so
                        overrides stay countable (exactly one Technique
                        this cycle; see
                        `test_facets_schema.py::TestFinalBlowOverrideFlag`).
                        Optional and defaults to `False` so every other
                        Technique parses unchanged.
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
    penalty_expires: str | None = None
    requires_domain: str | None = None
    difficulty_step: Literal["easier", "harder"] | None = None
    step_trigger: StepTriggerDef | None = None
    choices: list[str] | None = None
    removes_target_from_conflict: bool = False


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


class SavingThrowDef(BaseModel):
    """Saving throws (III.1:84-99): 2d6 + the Major Attribute modifier,
    resolved on the same three-tier table as any other roll. No skill
    applies — called for when something happens *to* the character, not
    something they chose to attempt.
    """

    modifier_source: str = "major_attribute"
    default_difficulty: str = "Standard"


class ContestedRollVsNpcDef(BaseModel):
    """Contested roll against an NPC (III.1): only the PC rolls; the NPC's
    relevant attribute informs the difficulty the MM sets. NPCs never roll
    dice."""

    only_pc_rolls: bool = True


class ContestedRollVsPcDef(BaseModel):
    """Contested roll between two player characters (III.1): both roll, the
    higher total wins; on a tie, both achieve partial success."""

    both_roll: bool = True
    higher_wins: bool = True
    tie_result: str = "both_partial_success"


class ContestedRollDef(BaseModel):
    vs_npc: ContestedRollVsNpcDef = Field(default_factory=ContestedRollVsNpcDef)
    vs_pc: ContestedRollVsPcDef = Field(default_factory=ContestedRollVsPcDef)


class GroupRollDef(BaseModel):
    """Group roll (III.1): the whole party attempts a task together. Majority
    success (partial success or better counts) succeeds the group. The lead
    roller + Support (III.3) is the stated alternative for tasks where one
    character is clearly more capable.
    """

    majority_rule: str = "partial_success_or_better_counts"
    lead_roller_alternative: bool = True


class NaturalResultDef(BaseModel):
    """A result keyed to the dice themselves rather than the modified total.

    Fields:
        natural: "high" — every kept die shows the maximum face; "low" — every
            kept die shows 1.
        min_outcome: Tier this result can never fall below, whatever the
            modifiers say. None leaves the tier alone.
        max_outcome: Tier this result can never rise above. **Left None for the
            fumble on purpose** — overriding a tier upward rewards, overriding
            it downward punishes competence, which is the d20 failure mode
            `research/dice_system_analysis.md` rejects.
        label: What the table calls it.
    """
    natural: Literal["high", "low"]
    min_outcome: Optional[str] = None
    max_outcome: Optional[str] = None
    label: str = ""
    description: str = ""


class BorrowedTroubleDef(BaseModel):
    """Accept a complication, take an extra die (PHB III.1, *Borrowed Trouble*).

    Mechanically identical to spending a Spark, drawn from a different place:
    nothing is spent, and the complication lands whatever the dice say.
    """
    extra_dice: int = 1
    spark_cost: int = 0
    max_per_roll: int = 1


class RollResolutionDef(BaseModel):
    dice: str = "2d6"
    modifier_source: str = "minor_attribute"
    thresholds: dict[str, int]           # {"full_success": 10, "partial_success": 7}
    outcomes: OutcomesDef
    difficulty_modifiers: list[DifficultyModifier] = Field(default_factory=list)
    outcome_tiers: list[OutcomeTierDef] = Field(default_factory=list)
    saving_throw: SavingThrowDef = Field(default_factory=SavingThrowDef)
    contested_roll: ContestedRollDef = Field(default_factory=ContestedRollDef)
    group_roll: GroupRollDef = Field(default_factory=GroupRollDef)
    critical: Optional[NaturalResultDef] = None
    fumble: Optional[NaturalResultDef] = None
    borrowed_trouble: Optional[BorrowedTroubleDef] = None


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


class MarksPerRankDef(BaseModel):
    """Marks required for each rank advance (PHB II.4, *Advancing Skills*).

    D16 replaced the flat cost with an escalating curve: the first advance stays
    cheap so onboarding is untouched, and Master is expensive enough that pushing
    one skill to the top is visibly a decision not to raise two others.
    """
    practiced: int = 3   # Novice → Practiced
    expert: int = 5      # Practiced → Expert
    master: int = 8      # Expert → Master

    def for_rank(self, target_rank: str) -> int:
        """Marks needed to reach `target_rank` from the rank below it."""
        return getattr(self, target_rank, self.practiced)


class RankCapsDef(BaseModel):
    """How many skills in one Facet may exceed Practiced (PHB II.4; D16).

    The ceiling that makes a Body character a *particular* Body character. Caps
    bind every Facet uniformly — primary and cross-trained alike — so there is
    one rule rather than two. `None` means uncapped, which is what a homebrew
    Facet that omits the block inherits: base's counts are tuned for five skills
    and must not silently constrain a Facet with a different count.
    """
    beyond_practiced: Optional[int] = None
    master: Optional[int] = None


class AdvancementDef(BaseModel):
    skill_ranks: list[SkillRankDef] = Field(default_factory=list)
    skill_point_costs: list[SkillPointCostDef] = Field(default_factory=list)
    session_skill_points: int = 4
    # D16: per-tier marks. A bare integer is the pre-D16 shape and still loads —
    # same deprecation contract as `enemy.endurance` → `resolve`.
    marks_per_rank: MarksPerRankDef = Field(default_factory=MarksPerRankDef)
    rank_caps: RankCapsDef = Field(default_factory=RankCapsDef)

    @field_validator("marks_per_rank", mode="before")
    @classmethod
    def _accept_legacy_flat_marks(cls, value):
        """Expand the pre-D16 `marks_per_rank: 3` integer across all three tiers."""
        if isinstance(value, int) and not isinstance(value, bool):
            warnings.warn(
                "advancement.marks_per_rank as a single integer is deprecated "
                "(PHB II.4 / D16 gives each rank its own cost). Use a mapping: "
                "{practiced: 3, expert: 5, master: 8}.",
                DeprecationWarning,
                stacklevel=2,
            )
            return {"practiced": value, "expert": value, "master": value}
        return value
    # T4.3/D10: the forfeit is dead. Up to `bank_cap` unspent points carry
    # into the next session, and `training_marks_per_session` of the session
    # points may go to an UNUSED Primary-Facet skill ("training between
    # sessions"). Both enforced by Character.spend_skill_point /
    # Character.start_new_session.
    bank_cap: int = 2
    training_marks_per_session: int = 1
    # Defaults mirror facets/base/facet.yaml. A Facet that omits these must land
    # on canon, not on a stale earlier revision (v0.3 moved 6 -> 5 and 4 -> 3;
    # D16 moved the threshold 5 -> 3 to fit the 9-advance shaped ceiling).
    facet_level_threshold: int = 3
    major_advancement_threshold: int = 3   # total Facet levels before a Major Advancement


# ---------------------------------------------------------------------------
# Backgrounds (PHB II.6)
# ---------------------------------------------------------------------------

class BackgroundDefinition(BaseModel):
    """A pre-built character background (PHB II.6).

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


class ItemDefinition(BaseModel):
    """A catalog item — currently only one-use charges (Val'loh crystals).

    The smallest loot system the game can have, and deliberately so: a charge
    holds one finished working at one scope, is released at a touch by anyone,
    and needs no roll and no arithmetic. Making one is an ordinary domain
    working done in downtime under II.3's normal rules; nothing extra is
    tracked. When the fiction makes a *release* chancy — fumbled in the dark,
    near something that eats magic — that is an ordinary Luck roll, not a rule
    that lives here.

    `Character.inventory` is already `list[str]`, so an item id is a valid
    entry alongside free text: a table that wants none of this can ignore the
    collection entirely and lose nothing.

    Fields:
        kind: What sort of thing it is. Only "consumable" exists; the field is
              here so adding a second sort is a data change.
        scope: The scope of the working the charge holds — II.3's ladder, not
              a second vocabulary.
        effect: One sentence, in the fiction's voice.
    """

    id: str
    name: str
    kind: Literal["consumable"] = "consumable"
    scope: Literal["minor", "significant", "major"] = "minor"
    effect: str


class LineageDefinition(BaseModel):
    """A lineage — who a character was born as (PHB II.5, D18).

    Orthogonal to the Background, which is what they *did*. The core rules
    ship exactly one lineage, Human, with no gift and no heritage; every
    other lineage belongs to a setting Facet, and a lineage that wants to
    add to an attribute, a skill rank, or the Endurance Pool is asking for a
    number the core deliberately does not hand out at creation.

    Fields:
        variants: The common in-world names for these people, printed in
                  italics after the name.
        gift: How the gift shows itself in these people — one line of
                  fiction ("through grown crystal", "as a prickle before
                  danger"). Present means the lineage is gifted; absent means
                  it is not, which is the core's Human. **The player chooses
                  which domain the gift is** (D24): any Soul or Mind domain
                  that is not Prismatic. The lineage colours it; it does not
                  pick it. A Gift is a domain in every respect (II.3), cast in
                  the intuitive tradition whatever the domain's own, and it
                  *replaces* the Background's secondary skill — a character
                  holds one domain at creation, from Lineage or Background,
                  never both.
        gift_domains: An optional restriction. Empty — the default and the
                  norm — means any eligible domain. A setting that wants its
                  people narrower may name a short list here; it is data, not
                  a special case.
        gift_rate: Fiction only ("four in five", "vanishingly rare"). Never a
                  roll; it is texture, and a prompt for how the ungifted are
                  treated.
        heritage: One narrow fact every member grows up with, gifted or not.
                  Works as a Specialty does — Standard becomes Easy when it
                  bears directly, information without a roll when tangential
                  — and draws from the *same* one-step allowance (III.1,
                  Difficulty). It is not a second Specialty in the arithmetic.
        playable: Whether a player may choose this lineage. False for
                  lineages that exist in data only so their NPCs can be
                  statted honestly.
        formalizes_on: How a Gift reaches full scope. "first_facet_level"
                  (D18, the ruling): at the character's first Facet level in
                  whichever Facet it lands, spending no Technique pick —
                  blood is not study, and charging a Body-Facet gifted
                  character a cross-Facet Technique would make "born gifted"
                  cost more than "studied magic". "technique" is the
                  Background route, kept as legal data so a setting could
                  choose it. Ignored when `gift_domains` is empty.
    """

    id: str
    name: str
    variants: list[str] = Field(default_factory=list)
    description: str
    gift: Optional[str] = None
    gift_domains: list[str] = Field(default_factory=list)
    gift_rate: Optional[str] = None
    heritage: Optional[str] = None
    playable: bool = True
    formalizes_on: Literal["first_facet_level", "technique"] = "first_facet_level"

    @property
    def is_gifted(self) -> bool:
        return self.gift is not None

    @model_validator(mode="after")
    def _restriction_needs_a_gift(self) -> "LineageDefinition":
        if self.gift_domains and self.gift is None:
            raise ValueError(
                f"Lineage '{self.id}' lists gift_domains but carries no gift. "
                "A restriction on a gift that does not exist silently does "
                "nothing; give the lineage a `gift` line or drop the list."
            )
        return self


# ---------------------------------------------------------------------------
# Combat (PHB III.3)
# ---------------------------------------------------------------------------

class CombatConditionDef(BaseModel):
    """A single named combat condition.

    Fields:
        id: Slug identifier (e.g. "winded", "staggered", "broken").
        clears: When this condition is removed *in combat*:
                "end_of_exchange" | "treated" | "end_of_scene".
        out_of_combat_clears: When this condition is removed *outside*
                combat, where no exchange structure exists (III.2:69) —
                Tier 1 Conditions clear at end of scene rather than end of
                exchange. `None` for conditions whose `clears` value is
                already scene/treated-based and doesn't change outside
                combat.
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
    out_of_combat_clears: str | None = None
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
        recovery_withdrawn: Endurance restored per exchange when posture is
                            Withdrawn — up to the pool maximum (D5); the
                            clamp lives in `combat.apply_withdrawn_recovery`.
    """

    base: int = 4
    recovery_withdrawn: int = 2


class PressDef(BaseModel):
    """Press: spend Endurance before a Strike to add dice and drop the lowest (PHB III.3).

    Fields:
        endurance_cost: Endurance spent to Press.
        extra_dice: Dice added to the roll (before dropping the lowest), same
                    effect as a Spark, stacks with Sparks.
    """

    endurance_cost: int = 1
    extra_dice: int = 1


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
    """PC armor downgrade rules keyed by armor type ("light", "heavy").

    Fields:
        reaction_downgrade_tiers: Tiers a successful partial reaction
                (Dodge/Parry 7-9) downgrades an incoming Condition by.
                Armor and reaction downgrades do not stack — apply the
                greater reduction only (III.3).
    """

    light: ArmorEntryDef = Field(default_factory=ArmorEntryDef)
    heavy: ArmorEntryDef = Field(
        default_factory=lambda: ArmorEntryDef(downgrades_per_scene=4)
    )
    reaction_downgrade_tiers: int = 1


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


class EnemyIncomingTierDef(BaseModel):
    """Condition tier a PC takes from an enemy attack, keyed by enemy type
    (III.3, Incoming Condition Tier): Mooks are individually weak (Tier 1);
    Named/Boss attacks carry a full Strike's weight (Tier 2).
    """

    mook: int = 1
    named: int = 2
    boss: int = 2


class EnemyPostureReactionShiftDef(BaseModel):
    """How an enemy's declared Posture shifts the difficulty of a PC's
    reaction against its attack (III.3, Enemy Posture and Reaction
    Difficulty). Values are "harder" | "easier" | "none".
    """

    aggressive: str = "harder"
    measured: str = "none"
    defensive: str = "easier"


class ManeuverOutcomesDef(BaseModel):
    """Maneuver's effect on rolls against the target, by outcome tier
    (III.3): a 10+ makes rolls against the target Easy until the situation
    changes; a 7-9 works but leaves the target at the base difficulty; a 6-
    backfires (no effect on the target).
    """

    full_success: str = "easy"
    partial_success: str = "standard"
    failure: str = "backfire"


class SupportDef(BaseModel):
    """Support grants an ally a bonus to their very next roll only, the
    supporting character's choice of mode; bonuses from multiple Support
    actions do not stack — only the most recent applies (III.3).
    """

    modes: list[str] = Field(default_factory=lambda: ["add_die", "ease_difficulty"])
    duration: str = "next_roll_only"
    stacking: str = "most_recent_only"


class CombatActionsDef(BaseModel):
    """Maneuver and Support (III.3), the two non-Strike offensive/aid
    actions."""

    maneuver: ManeuverOutcomesDef = Field(default_factory=ManeuverOutcomesDef)
    support: SupportDef = Field(default_factory=SupportDef)


class EnemyAttacksDef(BaseModel):
    """Rules for how an enemy's type and Posture shape a PC's reaction
    against its attack (III.3, Enemy Attacks). NPCs never roll dice — the PC
    rolls the reaction; these fields set what that reaction is up against.

    Fields:
        incoming_tier: Condition tier by enemy type.
        posture_reaction_shift: Reaction-difficulty shift by enemy Posture.
        mook_declares_posture: Mooks do not declare Postures (the MM sets
                their attack difficulty by situation instead) — always False
                for the base ruleset.
    """

    incoming_tier: EnemyIncomingTierDef = Field(default_factory=EnemyIncomingTierDef)
    posture_reaction_shift: EnemyPostureReactionShiftDef = Field(
        default_factory=EnemyPostureReactionShiftDef
    )
    mook_declares_posture: bool = False


class StrikeRiderDef(BaseModel):
    """One option on the full-success Strike's rider menu (R3, III.3 Table
    III.3-3): *10+ — deplete 2 Resolve and choose one.*

    The menu is data so the app renders the confirm from it and a setting
    may add or trim one; the *effects* are engine, so `effect` is a closed
    set and a rider naming behaviour the engine does not implement fails at
    load rather than silently doing nothing at the table.

    Fields:
        id: Stable identifier the client sends back on the confirm.
        label: What the table sees on the button.
        effect: What the engine does.
                "easy_tag" — Open: Easy to Strike for everyone.
                "easy_tag_next_roll" — Position: Easy for the next roll
                against this target, whoever makes it.
                "free_reaction_ally" — Cover: a named ally's next reaction
                costs no Endurance. The reaction is still rolled; Cover
                buys the cost, never the outcome.
        duration: When it expires. Open and Cover expire with the Tier 1
                  Conditions; Position is consumed by the next roll against
                  the target, or expires at the end of the following
                  exchange if nobody takes it.

    Three is the working cap, not a schema limit. A fourth option on the
    most common outcome in the game is where a pick-list stops being fast
    (BRIEF_fun_second_act §8), so the base ruleset ships two and the schema
    lets a setting decide otherwise.
    """

    id: str
    label: str
    effect: Literal["easy_tag", "easy_tag_next_roll", "free_reaction_ally"]
    duration: Literal[
        "end_of_exchange",
        "next_roll_or_end_of_next_exchange",
    ]


def _default_strike_riders() -> list[StrikeRiderDef]:
    """The two riders III.3 prints. Open is the pre-R3 behaviour kept as an
    option; Position is the Maneuver result arriving on a hit.

    Cover — Intercept's effect without Intercept's Endurance cost — was
    drafted as a third and **cut at the gate** (Series 12 Part C, D20). It
    was not too weak; it was too good in the wrong direction. Waiving
    reaction costs keeps the party's Endurance up, which drives postures
    aggressive, which shortened the solo-Boss fight from a median 3
    exchanges back to 2 and dropped the fraction of runs where the Boss's
    phase landed before the final exchange from 51-58.5% to 19-23% —
    erasing exactly what R2 had just bought. The `free_reaction_ally`
    effect stays implemented so a setting or a future Technique can offer
    it deliberately; the core menu does not.
    """
    return [
        StrikeRiderDef(id="open", label="Open", effect="easy_tag",
                       duration="end_of_exchange"),
        StrikeRiderDef(id="position", label="Position",
                       effect="easy_tag_next_roll",
                       duration="next_roll_or_end_of_next_exchange"),
    ]


class EnemyDurabilityDef(BaseModel):
    """Enemy Resolve pool rules (D1): depletion, armor bonus, and Mook removal.

    Fields:
        strike_depletion: Resolve lost per PC Strike outcome tier.
        armor_resolve_bonus: Flat Resolve granted by enemy armor.
        mook_removed_on: Outcome tier that removes an unarmored Mook.
        armored_mook_removed_on: Outcome tier that removes an armored Mook.
        open_on: Outcome tier that may additionally leave the enemy Open
                 (K-6/D4 — attacker's option, III.3 "on a full success
                 only"), on top of Resolve depletion. An Open enemy is
                 Easy to Strike for everyone; the player narrates what
                 Open looks like. Open never defeats an enemy — Resolve
                 does.
        open_clears: How Open clears — a closed set, because a lifecycle
                     the engine does not implement must fail at load
                     rather than at the table.
                     "end_of_exchange" (R2, the base ruleset's choice):
                     Open expires with the Tier 1 Conditions, so it is a
                     tempo tag — exploit it now — and the enemy keeps its
                     action while Open.
                     "enemy_action" (the pre-R2 rule, kept legal so a
                     setting may choose it and so Series 12 Part A's
                     regression floor still runs): cleared only by the
                     enemy visibly spending its action, never at end of
                     exchange.
        strike_riders: The menu a full-success Strike chooses one option
                     from (R3). See StrikeRiderDef.
    """

    strike_depletion: StrikeDepletionDef = Field(default_factory=StrikeDepletionDef)
    armor_resolve_bonus: ArmorResolveBonusDef = Field(default_factory=ArmorResolveBonusDef)
    mook_removed_on: str = "partial_success"
    armored_mook_removed_on: str = "full_success"
    open_on: str = "full_success"
    open_clears: Literal["enemy_action", "end_of_exchange"] = "enemy_action"
    strike_riders: list["StrikeRiderDef"] = Field(
        default_factory=lambda: _default_strike_riders(),
    )


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
    press: PressDef = Field(default_factory=PressDef)
    conditions: CombatConditionsTierDef = Field(default_factory=CombatConditionsTierDef)
    armor: ArmorDef = Field(default_factory=ArmorDef)
    enemy_durability: EnemyDurabilityDef = Field(default_factory=EnemyDurabilityDef)
    enemy_attacks: EnemyAttacksDef = Field(default_factory=EnemyAttacksDef)
    actions: CombatActionsDef = Field(default_factory=CombatActionsDef)
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


class WeaponCategoryDef(BaseModel):
    """One weapon category's attribute options for a Strike (IV.1:13-19).

    Fields:
        attributes: One or two Minor Attribute IDs; two means the player's
                    choice ("Standard or Dexterity"). Reference data only —
                    the engine stays deliberately permissive on which
                    attribute a Strike uses (IV.1: "The engine stays
                    permissive on Strike attributes").
    """

    attributes: list[str]


class EquipmentDef(BaseModel):
    """Equipment reference data (PHB IV.1)."""

    weapon_categories: dict[str, WeaponCategoryDef] = Field(default_factory=dict)
    # DESIGN §8 (TD-18): the *fictional* weapon vocabulary — blades/blunt/
    # polearms/unarmed — that Weapon Mastery (II.4a) masters. Orthogonal to
    # `weapon_categories` above, which is the *mechanical* vocabulary that
    # sets a Strike's attribute. A longsword is `standard` category and
    # `blades` type at once; the two lists are not meant to line up. No
    # ranged entry exists here because Weapon Mastery has no option covering
    # ranged weapons (content gap, docs/TODO.md T8 — not fixed in code).
    weapon_types: list[str] = Field(default_factory=list)


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
        tradition: Which attribute and skill govern casting rolls —
                   "intuitive" (Spirit + Attune) or "scholarly"
                   (Knowledge + Lore); see MagicDef.traditions.
        requires_tier3: True for Prismatic domains that need a Tier 3 Technique.
    """

    id: str
    name: str
    type: Literal["focused", "standard", "broad"]
    tradition: str
    description: str
    requires_tier3: bool = False


class SparkEaseFocusedMajorDef(BaseModel):
    """Focused domains may spend a Spark to shift a Major effect one
    difficulty step easier (II.3, Sparks and Magic)."""

    domain_type: str = "focused"
    scope: str = "major"


class SparkPreTechniquePushDef(BaseModel):
    """D8: a pre-Technique caster (capped at Minor scope) may spend a Spark
    to attempt one effect at `permitted_scope`, at the domain's *normal*
    difficulty for that scope — the Spark buys the scope, not a discount
    on the roll. Each Spark buys one such effect; it is not a permanent
    unlock (II.3, Reaching Significant Early)."""

    permitted_scope: str = "significant"


class TraditionDef(BaseModel):
    """Which attribute and skill a tradition's casting roll uses (II.3,
    Rolling Magic; T4.1/D7): casting with Spirit adds the Attune rank,
    casting with Knowledge adds the Lore rank.

    Both fields are required. Typed rather than a bare dict because a
    misspelled key here does not fail — it silently casts with the other
    tradition's attribute and skill, which is a wrong roll at the table with
    nothing on screen to explain it.
    """

    model_config = ConfigDict(extra="forbid")

    attribute: str
    skill: str


class MagicSparkRulesDef(BaseModel):
    """The two Spark-reach rules (II.3, Sparks and Magic; T2.2/D8). A Spark
    buys reach in exactly two cases — pre-Technique, one Significant-scope
    attempt; Focused domains, one difficulty step off a Major working.
    Reach-Sparks cannot move a Broad working's difficulty; dice-Sparks work
    normally (that is the engine's improve_roll path, not a rule here).
    The retired push_scope rule (P-1) referenced a scope tier beyond Major
    that does not exist."""

    ease_focused_major: SparkEaseFocusedMajorDef = Field(default_factory=SparkEaseFocusedMajorDef)
    pre_technique_push: SparkPreTechniquePushDef = Field(default_factory=SparkPreTechniquePushDef)


class IntentPurposeDef(BaseModel):
    """One broad purpose a caster can ready an intent for (D23).

    Deliberately broad. A purpose is not a spell and not a list of effects —
    it is the *shape* of what the caster expects to need, decided ahead of
    time, with the domain and the finishing form still chosen in the moment.
    """

    id: str
    label: str
    description: str


class PreparedIntentsDef(BaseModel):
    """Readied intents: the limit on Significant and Major magic (D23).

    At the start of each session — and again after a full rest, which the MM
    calls — a formalized caster readies up to `capacity` intents spread across
    the purposes as they choose. A Significant or Major working spends one of
    the matching purpose; the domain and what the magic actually does are
    still decided when it is cast. Scopes in `free_scopes` spend nothing, so
    small magic stays unlimited. Casting for a purpose with nothing readied
    costs `off_purpose_spark_cost` Sparks instead.

    The limit comes from having to guess. A party that readied Harm and Ward
    and walks into a negotiation has no Reveal — a story about preparation,
    not a spreadsheet.

    Absent from a ruleset means no limit, which is the pre-D23 game; a setting
    may choose that.
    """

    capacity: int = Field(3, ge=1)
    free_scopes: list[Literal["minor", "significant", "major"]] = Field(
        default_factory=lambda: ["minor"])
    off_purpose_spark_cost: int = Field(1, ge=0)
    #: D25: the scopes a magical *Strike* may be declared at. A blow aimed at
    #: putting someone down is meaningful power, so it is never Minor — free
    #: magic acts in a fight as a Maneuver or a Support instead. A setting that
    #: wants the free magical attack back widens this list.
    strike_scopes: list[Literal["minor", "significant", "major"]] = Field(
        default_factory=lambda: ["significant", "major"])
    purposes: list[IntentPurposeDef] = Field(min_length=1)

    @field_validator("purposes")
    @classmethod
    def _unique_purposes(cls, v: list[IntentPurposeDef]) -> list[IntentPurposeDef]:
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate intent purpose ids: {ids}")
        return v

    def purpose(self, purpose_id: str) -> Optional[IntentPurposeDef]:
        return next((p for p in self.purposes if p.id == purpose_id), None)


class MagicDef(BaseModel):
    """Full magic configuration for a Facet module (PHB II.3).

    Fields:
        traditions: Maps tradition keys ("intuitive" | "scholarly") to
                    {"attribute": ..., "skill": ...} — a casting roll adds
                    the skill the tradition trains (II.3, Rolling Magic):
                    casting with Spirit adds the Attune rank; casting with
                    Knowledge adds the Lore rank.
        domain_types: Maps type keys ("focused" | "standard" | "broad") to
                      {"scope_difficulties": {"minor": "Easy", ...}}.
        pre_technique_scope_limit: Maximum scope before the Facet Technique is unlocked.
                                   Default "minor".
        pre_technique_difficulty_penalty: No additional difficulty penalty pre-Technique.
                                          Default 0 (scope restriction alone is the penalty).
        soul_domains: Domains available to Soul Facet characters.
        mind_domains: Domains available to Mind Facet characters.
        spark_rules: The two Spark-reach rules (Focused Major ease,
                     D8's pre-Technique push).
        prepared_intents: The limit on Significant and Major magic (D23).
                     None means unlimited.
    """

    traditions: dict[str, TraditionDef] = Field(default_factory=dict)
    domain_types: dict[str, Any] = Field(default_factory=dict)
    pre_technique_penalty: str = "scope_only"
    pre_technique_scope_limit: str = "minor"       # scope ceiling before Technique is unlocked
    pre_technique_difficulty_penalty: int = 0       # no additional difficulty penalty pre-Technique
    soul_domains: list[MagicDomainDef] = Field(default_factory=list)
    mind_domains: list[MagicDomainDef] = Field(default_factory=list)
    spark_rules: MagicSparkRulesDef = Field(default_factory=MagicSparkRulesDef)
    prepared_intents: Optional[PreparedIntentsDef] = None

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
    lineages: list[LineageDefinition] = Field(default_factory=list)
    items: list[ItemDefinition] = Field(default_factory=list)
    roll_resolution: RollResolutionDef | None = None
    spark: SparkDef | None = None
    advancement: AdvancementDef | None = None
    combat: CombatDef | None = None
    magic: MagicDef | None = None
    hazards: HazardsDef | None = None
    death: DeathDef | None = None
    equipment: EquipmentDef | None = None

    @field_validator("id")
    @classmethod
    def id_is_slug(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Facet ID must be a slug (alphanumeric, hyphens, underscores only).")
        return v
