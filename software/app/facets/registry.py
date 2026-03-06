"""Merged ruleset registry — loads, validates, and merges Facet files for a session."""
from __future__ import annotations

from pathlib import Path

from app.facets.loader import FacetLoadError, discover_facet_files, load_facet_file
from app.facets.schema import (
    AdvancementDef,
    BackgroundDefinition,
    CharacterFacetDef,
    CombatDef,
    FacetFile,
    FacetTreeDef,
    MagicDef,
    RollResolutionDef,
    SkillDef,
    SparkDef,
)
from app.config import settings


class MergedRuleset:
    """The fully merged, validated ruleset for an active session.

    Built once at session creation; immutable thereafter.
    """

    def __init__(self, facet_files: list[FacetFile]) -> None:
        self._files = sorted(facet_files, key=lambda f: f.priority)
        self._merge()

    def _merge(self) -> None:
        # Dicts keyed by ID for deduplication; later Facets override earlier ones.
        major_attrs: dict[str, object] = {}
        minor_attrs: dict[str, object] = {}
        ratings: dict[int, object] = {}
        character_facets: dict[str, CharacterFacetDef] = {}
        skills: dict[str, SkillDef] = {}
        techniques: dict[str, FacetTreeDef] = {}
        backgrounds: dict[str, BackgroundDefinition] = {}
        distribution = None
        roll_resolution: RollResolutionDef | None = None
        spark: SparkDef | None = None
        advancement: AdvancementDef | None = None
        combat: CombatDef | None = None
        magic: MagicDef | None = None

        for ff in self._files:
            for ma in ff.attributes.major:
                major_attrs[ma.id] = ma
            for mi in ff.attributes.minor:
                minor_attrs[mi.id] = mi
            for r in ff.attributes.ratings:
                ratings[r.rating] = r
            if ff.attributes.distribution:
                distribution = ff.attributes.distribution

            for cf in ff.facets:
                character_facets[cf.id] = cf

            for sk in ff.skills:
                skills[sk.id] = sk

            for facet_id, tree in ff.techniques.items():
                techniques[facet_id] = tree

            for bg in ff.backgrounds:
                backgrounds[bg.id] = bg

            if ff.roll_resolution:
                roll_resolution = ff.roll_resolution
            if ff.spark:
                spark = ff.spark
            if ff.advancement:
                advancement = ff.advancement
            if ff.combat:
                combat = ff.combat
            if ff.magic:
                magic = ff.magic

        self.major_attributes = list(major_attrs.values())
        self.minor_attributes = list(minor_attrs.values())
        self.attribute_ratings = sorted(ratings.values(), key=lambda r: r.rating)
        self.attribute_distribution = distribution
        self.character_facets = list(character_facets.values())
        self.skills = list(skills.values())
        self.techniques = techniques
        self.backgrounds = list(backgrounds.values())
        self.roll_resolution = roll_resolution
        self.spark = spark
        self.advancement = advancement
        self.combat = combat
        self.magic = magic

        self._validate_cross_references()

    def _validate_cross_references(self) -> None:
        """Fail loudly if skills/techniques reference undefined attributes or facets."""
        known_minor = {ma.id for ma in self.minor_attributes}
        known_facets = {cf.id for cf in self.character_facets}

        errors: list[str] = []
        for skill in self.skills:
            if skill.attribute not in known_minor:
                errors.append(f"Skill '{skill.id}' references unknown attribute '{skill.attribute}'.")
            if skill.facet not in known_facets:
                errors.append(f"Skill '{skill.id}' references unknown facet '{skill.facet}'.")

        if errors:
            raise FacetLoadError("Cross-reference validation failed:\n" + "\n".join(f"  {e}" for e in errors))

    def get_minor_attribute_modifier(self, attribute_id: str, rating: int) -> int:
        for r in self.attribute_ratings:
            if r.rating == rating:
                return r.modifier
        return 0

    def get_skill(self, skill_id: str) -> SkillDef | None:
        for sk in self.skills:
            if sk.id == skill_id:
                return sk
        return None

    def get_skill_rank_modifier(self, rank_id: str) -> int:
        if not self.advancement:
            return 0
        for sr in self.advancement.skill_ranks:
            if sr.id == rank_id:
                return sr.modifier
        return 0

    def get_skill_point_cost(self, context: str) -> int:
        if not self.advancement:
            return 1
        for cost_def in self.advancement.skill_point_costs:
            if cost_def.context == context:
                return cost_def.cost
        return 1

    def get_background(self, background_id: str) -> "BackgroundDefinition | None":
        for bg in self.backgrounds:
            if bg.id == background_id:
                return bg
        return None

    def to_client_dict(self) -> dict:
        """Serialise the ruleset to a JSON-safe dict for sending to clients."""
        from pydantic import BaseModel

        def _serialize(obj):
            if isinstance(obj, BaseModel):
                return obj.model_dump()
            if isinstance(obj, list):
                return [_serialize(i) for i in obj]
            if isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            return obj

        return {
            "major_attributes": _serialize(self.major_attributes),
            "minor_attributes": _serialize(self.minor_attributes),
            "attribute_ratings": _serialize(self.attribute_ratings),
            "attribute_distribution": _serialize(self.attribute_distribution),
            "character_facets": _serialize(self.character_facets),
            "skills": _serialize(self.skills),
            "techniques": _serialize(self.techniques),
            "backgrounds": _serialize(self.backgrounds),
            "roll_resolution": _serialize(self.roll_resolution),
            "spark": _serialize(self.spark),
            "advancement": _serialize(self.advancement),
            "combat": _serialize(self.combat),
            "magic": _serialize(self.magic),
        }


def build_ruleset(active_facet_ids: list[str] | None = None) -> MergedRuleset:
    """Discover, load, and merge Facet files.

    Always loads the base facet. Loads additional facets named in active_facet_ids.
    Raises FacetLoadError if any file is invalid.
    """
    facets_dir = settings.facets_dir
    all_paths = discover_facet_files(facets_dir)

    if not all_paths:
        raise FacetLoadError(f"No ruleset files found in {facets_dir.resolve()}.")

    loaded: list[FacetFile] = []
    for path in all_paths:
        ff = load_facet_file(path)
        # Always include base; include others only if requested
        if ff.id == "base" or (active_facet_ids and ff.id in active_facet_ids):
            loaded.append(ff)

    if not loaded:
        raise FacetLoadError("No Facet files matched. At minimum, the base facet must be present.")

    return MergedRuleset(loaded)
