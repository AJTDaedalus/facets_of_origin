"""Pydantic schema for Lean Facets v1.0 ruleset files.

`software/facets/base/facet.yaml` is the single source of truth for every
number the engine uses (DESIGN_lean_facets §3.1). Every section of that file
has a model here; the engine reads these models and never hard-codes a rule.

A *setting Facet* (e.g. `facets/valloh/facet.yaml`) uses the same `FacetFile`
model but may only fill the additive collections (lineages, talents, classes,
backgrounds, items, magic_domains, tables). The registry enforces that.

`tables.yaml` (the MM toolbox, DESIGN §3.2) is modelled by `TablesFile`; each
table must cover every face of its die exactly once (`table_coverage_errors`).
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class _Model(BaseModel):
    """Base: unknown keys are rejected, so a typo in YAML fails loudly."""

    model_config = ConfigDict(extra="forbid")


class _Loose(BaseModel):
    """Base for prose-heavy entries that may carry canon-only extra fields."""

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------------------------
# Stats and Facets
# ---------------------------------------------------------------------------

class StatDef(_Model):
    id: str
    name: str
    description: str = ""


class StatCreationDef(_Model):
    facet_stat: int = 2
    second: int = 1
    third: int = 0


class StatRulesDef(_Model):
    creation: StatCreationDef = Field(default_factory=StatCreationDef)
    maximum: int = 3
    increase_levels: list[int] = Field(default_factory=list)
    increase_amount: int = 1


class FacetDef(_Model):
    id: str
    name: str
    stat: str
    grit_die: int = Field(ge=2)
    grit_average: int = Field(ge=1)
    tradition: Optional[str] = None
    description: str = ""


# ---------------------------------------------------------------------------
# Talents and classes
# ---------------------------------------------------------------------------

TalentUse = Literal["passive", "at_will", "once_per_scene", "once_per_session", "once_per_rest"]


class TalentRequiresDef(_Model):
    any_talent: list[str] = Field(default_factory=list)


class TalentDef(_Model):
    id: str
    name: str
    facet: str
    kind: Literal["talent", "signature"]
    use: TalentUse
    text: str
    normal: str
    improved: Optional[str] = None
    choose: Optional[str] = None
    requires: Optional[TalentRequiresDef] = None
    shared_with: list[str] = Field(default_factory=list)
    effects: dict[str, Any] = Field(default_factory=dict)
    improved_effects: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _menu_talents_have_improved_forms(self) -> "TalentDef":
        if self.kind == "talent" and not self.improved:
            raise ValueError(f"talent '{self.id}' is a menu talent with no improved form")
        return self

    def on_menu_of(self, facet_id: str) -> bool:
        """True if this talent appears on `facet_id`'s menu (own Facet or shared)."""
        return self.facet == facet_id or facet_id in self.shared_with

    def effect(self, key: str, improved: bool = False, default: Any = None) -> Any:
        """The value of an engine hook, preferring the improved form's when held improved."""
        if improved and key in self.improved_effects:
            return self.improved_effects[key]
        return self.effects.get(key, default)

    def uses_allowed(self, improved: bool = False) -> Optional[int]:
        """How many times the talent may be used per its `use` period.

        None for passive / at-will talents (no tracking). Limited talents allow
        one use; an improved form whose text begins "Twice" allows two, and
        Lucky's `rerolls_per_session` effect is honoured directly.
        """
        if self.use in ("passive", "at_will"):
            return None
        if "rerolls_per_session" in self.effects:
            return int(self.effect("rerolls_per_session", improved, 1))
        if improved and self.improved and self.improved.strip().lower().startswith("twice"):
            return 2
        return 1


class ClassDef(_Model):
    id: str
    name: str
    facet: str
    concept: str
    knack: str
    talents: list[str]
    signature: str
    kit: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Core resolution and Sparks
# ---------------------------------------------------------------------------

class ThresholdsDef(_Model):
    full_success: int = 10
    partial_success: int = 7


class OutcomeTextDef(_Model):
    label: str
    description: str = ""


class NaturalDef(_Model):
    natural: Literal["high", "low"]
    label: str = ""
    description: str = ""
    min_outcome: Optional[str] = None


class ExtraDieDef(_Model):
    extra_dice: int = 1
    max_per_roll: int = 1
    spark_cost: int = 0
    helper_shares_cost: bool = False


class DifficultyDef(_Model):
    label: str
    modifier: int
    description: str = ""


class OutcomeTierDef(_Model):
    id: str
    threshold: Optional[int] = None
    label: str
    description: str = ""


class AvoidDef(_Model):
    modifier_source: str = "stat"
    default_difficulty: str = "Standard"
    outcomes: dict[str, str] = Field(default_factory=dict)


class RollResolutionDef(_Model):
    dice: str = "2d6"
    modifier_source: str = "stat"
    knack_bonus: int = 1
    bonus_cap: int = 4
    thresholds: ThresholdsDef = Field(default_factory=ThresholdsDef)
    outcomes: dict[str, OutcomeTextDef] = Field(default_factory=dict)
    critical: Optional[NaturalDef] = None
    fumble: Optional[NaturalDef] = None
    borrowed_trouble: ExtraDieDef = Field(default_factory=ExtraDieDef)
    help: ExtraDieDef = Field(default_factory=ExtraDieDef)
    difficulty_modifiers: list[DifficultyDef]
    outcome_tiers: list[OutcomeTierDef] = Field(default_factory=list)
    avoid: AvoidDef = Field(default_factory=AvoidDef)
    contested_roll: dict[str, Any] = Field(default_factory=dict)
    group_roll: dict[str, Any] = Field(default_factory=dict)

    def get_difficulty_modifier(self, label: str) -> int:
        for d in self.difficulty_modifiers:
            if d.label == label:
                return d.modifier
        raise ValueError(f"Unknown difficulty {label!r}; expected one of "
                         f"{[d.label for d in self.difficulty_modifiers]}")

    def difficulty_labels_hard_to_easy(self) -> list[str]:
        return [d.label for d in sorted(self.difficulty_modifiers, key=lambda d: d.modifier)]


class SparkEarnDef(_Model):
    id: str
    label: str
    description: str = ""


class SparkDef(_Model):
    base_sparks_per_session: int = 3
    mechanic: dict[str, Any] = Field(default_factory=dict)
    earn_methods: list[SparkEarnDef] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Advancement
# ---------------------------------------------------------------------------

class DamageBonusStep(_Model):
    level: int
    bonus: int


class PromptDef(_Model):
    id: str
    text: str


class PacingStep(_Model):
    level: int
    after_session: int


class AdvancementDef(_Model):
    max_level: int = 10
    starting_talents: int = 2
    signature_level: int = 3
    respec_until_level: int = 3
    stat_increase_levels: list[int] = Field(default_factory=list)
    signature_working_levels: list[int] = Field(default_factory=list)
    damage_bonus: list[DamageBonusStep] = Field(default_factory=list)
    improve_requires_levels_held: int = 1
    off_facet_requires: str = "teacher"
    prompts: list[PromptDef] = Field(default_factory=list)
    pacing: list[PacingStep] = Field(default_factory=list)

    def damage_bonus_at(self, level: int) -> int:
        """The level damage bonus: the highest step at or below `level`."""
        bonus = 0
        for step in sorted(self.damage_bonus, key=lambda s: s.level):
            if level >= step.level:
                bonus = step.bonus
        return bonus


# ---------------------------------------------------------------------------
# Durability, recovery, death, slots
# ---------------------------------------------------------------------------

class HPDef(_Model):
    level_one: str = "grit_die_max_plus_body"
    per_level: str = "grit_die_or_average"
    minimum_gain: int = 1


class BreatherDef(_Model):
    restores: str = "half_max_hp"
    pressure_roll_if_dangerous: bool = True


class NightRestDef(_Model):
    restores: str = "full_hp"
    clears_fatigue: str = "all"
    clears_wounds: int = 1


class RecoveryDef(_Model):
    breather: BreatherDef = Field(default_factory=BreatherDef)
    night_rest: NightRestDef = Field(default_factory=NightRestDef)


class WoundsDef(_Model):
    takes_slot: bool = True
    effect: str = ""
    table: str = "wounds"


class HoldOnDef(_Model):
    stat: str = "body"
    outcomes: dict[str, str] = Field(default_factory=dict)


class DeathDef(_Model):
    broken_is_lethal: bool = False
    death_choice: list[str] = Field(default_factory=list)
    scar_table: str = "scars"


class SlotsDef(_Model):
    base: int = 10
    plus_stat: str = "body"
    coin_per_slot: int = 100
    curio_limit: int = 3


# ---------------------------------------------------------------------------
# Magic
# ---------------------------------------------------------------------------

class TraditionDef(_Model):
    stat: str
    facet: str
    style: str = ""


class ScopeDef(_Model):
    id: str
    label: str
    difficulty: str
    fatigue: int = Field(ge=0)
    min_level: int = 1
    damage: Optional[str] = None
    targets: Optional[str] = None
    description: str = ""


class MagicDef(_Model):
    traditions: dict[str, TraditionDef]
    scopes: list[ScopeDef]
    signature_step: int = 1
    starting_signature_workings: int = 2
    wider_domain_step: int = -1
    prismatic_step: int = -1
    heavy_armor_extra_fatigue: int = 1
    fatigue_takes_slot: bool = True
    fatigue_clears_on: str = "night_rest"
    complication_table: str = "magic_complications"
    mishap_table: str = "magic_mishaps"
    lineage_gift_scope: str = "minor"

    def get_scope(self, scope_id: str) -> ScopeDef:
        for s in self.scopes:
            if s.id == scope_id:
                return s
        raise ValueError(f"Unknown scope {scope_id!r}; expected one of {[s.id for s in self.scopes]}")


class MagicDomainDef(_Loose):
    id: str
    name: str
    facet: str
    tradition: str
    prismatic: bool = False
    description: str = ""


# ---------------------------------------------------------------------------
# Combat and monsters
# ---------------------------------------------------------------------------

class AttackTierDef(_Model):
    damage: str = "none"
    pick_one: list[str] = Field(default_factory=list)
    exposed: bool = False
    mm_move: bool = False


class AttackDef(_Model):
    full_success: AttackTierDef
    partial_success: AttackTierDef
    failure: AttackTierDef


class AttackOptionDef(_Model):
    label: str
    dice: Optional[str] = None
    description: str = ""


class ExposureDef(_Model):
    applies_when: str = "partial_success_within_reach"
    extra_enemy_dice: int = 1


class EnemyAttackTierDef(_Model):
    hit: bool
    damage_bonus: int = 0
    label: str = ""


class EnemyAttackDef(_Model):
    dice: str = "2d6"
    full_success: EnemyAttackTierDef
    partial_success: EnemyAttackTierDef
    failure: EnemyAttackTierDef
    natural_high: str = ""
    natural_low: str = ""


class DefendDef(_Model):
    enemy_difficulty: str = "Hard"


class InterceptDef(_Model):
    as_defend: bool = True


class ArmorRuleDef(_Model):
    minimum_damage: int = 1
    cap: int = 3


class LevelGapDef(_Model):
    gap: int
    difficulty: str


class CombatDef(_Model):
    exchange_steps: list[str] = Field(default_factory=list)
    attack: AttackDef
    options: dict[str, AttackOptionDef]
    exposure: ExposureDef = Field(default_factory=ExposureDef)
    enemy_attack: EnemyAttackDef
    defend: DefendDef = Field(default_factory=DefendDef)
    intercept: InterceptDef = Field(default_factory=InterceptDef)
    armor: ArmorRuleDef = Field(default_factory=ArmorRuleDef)
    level_gap: list[LevelGapDef] = Field(default_factory=list)
    unarmed_die: int = 4


class MonsterLevelRow(_Model):
    level: int
    hp: int
    damage: int
    attack: int


class RoleDef(_Model):
    hp: Optional[str] = None               # "drops_to_any_hit" for Mooks
    hp_mult: Optional[int] = None
    damage_mod: int = 0
    attack_mod: int = 0
    attacks: int = 1
    mob: bool = False
    mob_damage_per_extra: int = 0
    mob_damage_cap: int = 0
    bloodied_phase: bool = False

    @model_validator(mode="after")
    def _hp_rule(self) -> "RoleDef":
        if self.hp is None and self.hp_mult is None:
            raise ValueError("a role needs hp_mult or an hp rule")
        return self


class MoraleDef(_Model):
    dice: str = "2d6"
    breaks_when: str = "roll_exceeds_morale"
    default: int = 7
    fearless: int = 12
    triggers: list[str] = Field(default_factory=list)


class MonstersDef(_Model):
    level_table: list[MonsterLevelRow]
    roles: dict[str, RoleDef]
    morale: MoraleDef = Field(default_factory=MoraleDef)
    bloodied_at: str = "half_hp"
    armor_range: list[int] = Field(default_factory=lambda: [0, 2])

    def row(self, level: int) -> MonsterLevelRow:
        for r in self.level_table:
            if r.level == level:
                return r
        raise ValueError(f"No monster level-table row for level {level}")


# ---------------------------------------------------------------------------
# Hazards, exploration
# ---------------------------------------------------------------------------

class ThreatClockDef(_Model):
    segments: int = 4
    advances_on: list[str] = Field(default_factory=list)
    wind_back_cost: str = "1_action"
    wind_back_requires_roll: bool = False


class HazardsDef(_Model):
    threat_clock: ThreatClockDef = Field(default_factory=ThreatClockDef)


class PressureDieDef(_Model):
    dice: str = "1d6"
    table: str = "pressure_generic"
    rolled: list[str] = Field(default_factory=list)


class ReactionRollDef(_Model):
    dice: str = "2d6"
    table: str = "reaction"


class UsageDieDef(_Model):
    steps: list[int] = Field(default_factory=lambda: [8, 6, 4])
    steps_down_on: list[int] = Field(default_factory=lambda: [1, 2])


class ExplorationDef(_Model):
    pressure_die: PressureDieDef = Field(default_factory=PressureDieDef)
    reaction_roll: ReactionRollDef = Field(default_factory=ReactionRollDef)
    usage_die: UsageDieDef = Field(default_factory=UsageDieDef)


# ---------------------------------------------------------------------------
# Equipment and treasure
# ---------------------------------------------------------------------------

class WeaponCategoryDef(_Model):
    die: int
    slots: int = 1
    examples: str = ""
    notes: str = ""


class ArmorCategoryDef(_Model):
    armor: int
    slots: int = 0
    notes: str = ""


class ItemDef(_Loose):
    """An item. `weapon` names a weapon category, `armor` an armor category,
    `kind` a weapon kind (blades, bows ...). A `curio` is a one-use item that
    counts against the curio limit; `effect` states what it does."""

    id: str
    name: str
    slots: int = Field(default=1, ge=0)
    weapon: Optional[str] = None
    kind: Optional[str] = None
    armor: Optional[str] = None
    usage_die: Optional[int] = None
    curio: bool = False
    effect: Optional[str] = None
    description: str = ""


class PriceDef(_Model):
    label: str
    coin: int
    examples: str = ""


class EquipmentDef(_Model):
    weapon_categories: dict[str, WeaponCategoryDef] = Field(default_factory=dict)
    weapon_kinds: list[str] = Field(default_factory=list)
    armor: dict[str, ArmorCategoryDef] = Field(default_factory=dict)
    items: list[ItemDef] = Field(default_factory=list)
    starting_coin: str = ""
    price_guide: list[PriceDef] = Field(default_factory=list)


class TreasureDef(_Model):
    curio_limit: int = 3
    tables: list[str] = Field(default_factory=list)
    relics_usable_by_anyone: bool = True


# ---------------------------------------------------------------------------
# Lineages and backgrounds
# ---------------------------------------------------------------------------

class LineageDef(_Loose):
    """A lineage. A *gifted* lineage has a `gift` (its gift knack text) and may
    set `gift_domain_scope: minor` — the player then chooses one domain in
    which the character may cast Minor workings (L14, D24)."""

    id: str
    name: str
    variants: list[str] = Field(default_factory=list)
    description: str = ""
    gift: Optional[str] = None
    gift_domain_scope: Optional[str] = None
    gift_domains: list[str] = Field(default_factory=list)
    playable: bool = True

    @property
    def gifted(self) -> bool:
        return bool(self.gift)

    @property
    def gift_knack(self) -> Optional[str]:
        """The knack a gifted lineage adds: its own `knack` if it names one,
        else "<Name> gift"."""
        if not self.gift:
            return None
        return getattr(self, "knack", None) or f"{self.name} gift"


class BackgroundDef(_Loose):
    id: str
    name: str
    facet: Optional[str] = None
    knack: str
    specialty: str
    description: str = ""


# ---------------------------------------------------------------------------
# MM tables (tables.yaml)
# ---------------------------------------------------------------------------

TABLE_DICE = ("1d6", "1d8", "1d12", "1d20", "2d6", "d66")


def die_faces(die: str) -> list[int]:
    """Every possible result of a table die, in order. d66 reads tens-then-units."""
    if die == "d66":
        return [a * 10 + b for a in range(1, 7) for b in range(1, 7)]
    if die == "2d6":
        return list(range(2, 13))
    if die in TABLE_DICE:
        return list(range(1, int(die.split("d")[1]) + 1))
    raise ValueError(f"Unknown table die {die!r}; expected one of {TABLE_DICE}")


def expand_roll(roll: str | int, die: str) -> list[int]:
    """The faces an entry's `roll` covers: "7", 7, "2-4" or "2–4" (en dash).

    A range covers every legal face of the die between its ends, so a d66
    range "15-22" is 15, 16, 21, 22.
    """
    text = str(roll).strip().replace("–", "-")
    faces = die_faces(die)
    if "-" in text:
        lo_s, hi_s = text.split("-", 1)
        lo, hi = int(lo_s), int(hi_s)
        if lo > hi:
            raise ValueError(f"range {roll!r} runs backwards")
        return [f for f in faces if lo <= f <= hi]
    value = int(text)
    return [value] if value in faces else []


class TableEntry(_Model):
    roll: str
    text: str

    @field_validator("roll", mode="before")
    @classmethod
    def _roll_to_str(cls, v: Any) -> str:
        return str(v)


class TableDef(_Model):
    id: str
    name: str
    die: str
    pillar: str = ""
    use: str = ""
    entries: list[TableEntry]

    @field_validator("die")
    @classmethod
    def _known_die(cls, v: str) -> str:
        if v not in TABLE_DICE:
            raise ValueError(f"die must be one of {TABLE_DICE}, got {v!r}")
        return v

    def lookup(self, face: int) -> TableEntry:
        for entry in self.entries:
            if face in expand_roll(entry.roll, self.die):
                return entry
        raise ValueError(f"table {self.id!r} has no entry for {face}")


def table_coverage_errors(table: TableDef) -> list[str]:
    """Gaps, overlaps and out-of-range rolls in one table (empty = covers exactly)."""
    errors: list[str] = []
    faces = die_faces(table.die)
    seen: list[int] = []
    for entry in table.entries:
        try:
            covered = expand_roll(entry.roll, table.die)
        except ValueError as e:
            errors.append(f"{table.id}: bad roll {entry.roll!r} ({e})")
            continue
        if not covered:
            errors.append(f"{table.id}: roll {entry.roll!r} is not a result of {table.die}")
        if not entry.text.strip():
            errors.append(f"{table.id}: entry {entry.roll!r} has no text")
        seen.extend(covered)
    gaps = sorted(set(faces) - set(seen))
    dupes = sorted({f for f in seen if seen.count(f) > 1})
    if gaps:
        errors.append(f"{table.id} ({table.die}): no entry for {gaps}")
    if dupes:
        errors.append(f"{table.id} ({table.die}): more than one entry for {dupes}")
    return errors


class TablesFile(_Model):
    tables: list[TableDef] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------

#: Sections a setting Facet may never write (INV-17). `equipment` is allowed
#: only to add `items`.
CORE_RULE_SECTIONS = (
    "stats", "stat_rules", "facets", "roll_resolution", "spark", "advancement",
    "hp", "recovery", "wounds", "hold_on", "death", "slots", "magic", "combat",
    "monsters", "hazards", "exploration", "treasure",
)


class FacetFile(_Model):
    id: str
    name: str
    version: str
    authors: list[str] = Field(default_factory=list)
    description: str = ""
    priority: int = 0

    stats: list[StatDef] = Field(default_factory=list)
    stat_rules: Optional[StatRulesDef] = None
    facets: list[FacetDef] = Field(default_factory=list)
    talents: list[TalentDef] = Field(default_factory=list)
    classes: list[ClassDef] = Field(default_factory=list)
    roll_resolution: Optional[RollResolutionDef] = None
    spark: Optional[SparkDef] = None
    advancement: Optional[AdvancementDef] = None
    hp: Optional[HPDef] = None
    recovery: Optional[RecoveryDef] = None
    wounds: Optional[WoundsDef] = None
    hold_on: Optional[HoldOnDef] = None
    death: Optional[DeathDef] = None
    slots: Optional[SlotsDef] = None
    magic: Optional[MagicDef] = None
    combat: Optional[CombatDef] = None
    monsters: Optional[MonstersDef] = None
    hazards: Optional[HazardsDef] = None
    exploration: Optional[ExplorationDef] = None
    equipment: Optional[EquipmentDef] = None
    treasure: Optional[TreasureDef] = None
    tables_file: Optional[str] = None
    tables: list[TableDef] = Field(default_factory=list)
    items: list[ItemDef] = Field(default_factory=list)
    lineages: list[LineageDef] = Field(default_factory=list)
    backgrounds: list[BackgroundDef] = Field(default_factory=list)
    magic_domains: list[MagicDomainDef] = Field(default_factory=list)

    #: Tables loaded from `tables_file` by the loader (not a YAML key).
    loaded_tables: list[TableDef] = Field(default_factory=list, exclude=True)
    #: Non-fatal notes from loading (e.g. tables file absent).
    load_warnings: list[str] = Field(default_factory=list, exclude=True)

    @property
    def is_core(self) -> bool:
        """A file that defines stats is a core ruleset; anything else is a setting Facet."""
        return bool(self.stats)

    def written_core_sections(self) -> list[str]:
        """Core rule sections this file writes (non-empty). A setting Facet must write none."""
        written = [s for s in CORE_RULE_SECTIONS if getattr(self, s)]
        if self.equipment is not None:
            extra = [f for f in self.equipment.model_fields_set if f != "items"]
            if extra:
                written.append("equipment." + ",".join(sorted(extra)))
        return written

    def all_items(self) -> list[ItemDef]:
        return list(self.equipment.items if self.equipment else []) + list(self.items)

    def all_tables(self) -> list[TableDef]:
        return list(self.loaded_tables) + list(self.tables)
