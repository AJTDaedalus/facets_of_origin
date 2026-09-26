"""Merged ruleset registry — loads, validates and merges Facet files for a session.

One core file (the one that defines `stats`; normally `facets/base`) supplies
every rule. Setting Facets are additive only (DESIGN §3.1, INV-17): they may
add lineages, talents, classes, backgrounds, items, magic domains and tables,
but may not write a core rule section nor redefine an id the core already has.
"""
from __future__ import annotations

import logging
from typing import Optional

from pydantic import BaseModel

from app.config import settings
from app.facets.loader import FacetLoadError, discover_facet_files, load_facet_file
from app.facets.schema import (
    BackgroundDef, ClassDef, FacetDef, FacetFile, ItemDef, LineageDef,
    MagicDomainDef, StatDef, TableDef, TalentDef,
)

logger = logging.getLogger(__name__)

#: Tables the MM toolbox and the engine expect (DESIGN §3.2).
REQUIRED_TABLE_IDS = (
    "reaction", "reaction_wants", "pressure_generic", "pressure_underground",
    "pressure_wild", "pressure_settlement", "pressure_occasion", "trouble",
    "complications_fight", "complications_explore", "complications_social",
    "magic_complications", "magic_mishaps", "wounds", "scars", "trinkets",
    "curios", "relics", "npc_names", "npc_traits", "npc_wants", "npc_secrets",
    "oracle_actions", "oracle_themes",
)

_SINGLETONS = (
    "stat_rules", "roll_resolution", "spark", "advancement", "hp", "recovery",
    "wounds", "hold_on", "death", "slots", "magic", "combat", "monsters",
    "hazards", "exploration", "treasure",
)


class MergedRuleset:
    """The fully merged, validated ruleset for an active session. Immutable after build."""

    def __init__(self, facet_files: list[FacetFile]) -> None:
        self._files = sorted(facet_files, key=lambda f: f.priority)
        self.warnings: list[str] = []
        self._merge()

    # ------------------------------------------------------------------ merge
    def _merge(self) -> None:
        cores = [f for f in self._files if f.is_core]
        if len(cores) != 1:
            raise FacetLoadError(
                f"Exactly one core ruleset (a file defining `stats`) is required; "
                f"found {len(cores)}: {[f.id for f in cores]}.")
        core = cores[0]
        for name in _SINGLETONS:
            setattr(self, name, getattr(core, name))
            if getattr(core, name) is None:
                raise FacetLoadError(f"{core.id}: core ruleset is missing section '{name}'.")
        self.stats: list[StatDef] = list(core.stats)
        self.facets: list[FacetDef] = list(core.facets)
        self.equipment = core.equipment

        collections: dict[str, dict[str, BaseModel]] = {
            "talents": {}, "classes": {}, "backgrounds": {}, "lineages": {},
            "items": {}, "magic_domains": {}, "tables": {},
        }
        errors: list[str] = []
        for ff in [core] + [f for f in self._files if f is not core]:
            self.warnings.extend(ff.load_warnings)
            if ff is not core:
                written = ff.written_core_sections()
                if written:
                    errors.append(
                        f"Setting Facet '{ff.id}' may only add content; it writes core "
                        f"rule section(s): {', '.join(written)}.")
            sources = {
                "talents": ff.talents, "classes": ff.classes,
                "backgrounds": ff.backgrounds, "lineages": ff.lineages,
                "items": ff.all_items(), "magic_domains": ff.magic_domains,
                "tables": ff.all_tables(),
            }
            for kind, entries in sources.items():
                for entry in entries:
                    if entry.id in collections[kind]:
                        errors.append(f"'{ff.id}' redefines {kind[:-1]} '{entry.id}'; "
                                      "setting Facets are additive only.")
                        continue
                    collections[kind][entry.id] = entry
        if errors:
            raise FacetLoadError("Ruleset merge failed:\n" + "\n".join(f"  {e}" for e in errors))

        self.talents: list[TalentDef] = list(collections["talents"].values())
        self.classes: list[ClassDef] = list(collections["classes"].values())
        self.backgrounds: list[BackgroundDef] = list(collections["backgrounds"].values())
        self.lineages: list[LineageDef] = list(collections["lineages"].values())
        self.items: list[ItemDef] = list(collections["items"].values())
        self.magic_domains: list[MagicDomainDef] = list(collections["magic_domains"].values())
        self.tables: dict[str, TableDef] = dict(collections["tables"])

        self._stat_map = {s.id: s for s in self.stats}
        self._facet_map = {f.id: f for f in self.facets}
        self._talent_map = {t.id: t for t in self.talents}
        self._class_map = {c.id: c for c in self.classes}
        self._background_map = {b.id: b for b in self.backgrounds}
        self._lineage_map = {x.id: x for x in self.lineages}
        self._item_map = {i.id: i for i in self.items}
        self._domain_map = {d.id: d for d in self.magic_domains}

        self._validate_cross_references()
        for w in self.warnings:
            logger.warning(w)

    def _validate_cross_references(self) -> None:
        """Fail loudly on any dangling reference inside the merged ruleset."""
        errors: list[str] = []
        stat_ids = set(self._stat_map)
        facet_ids = set(self._facet_map)
        traditions = self.magic.traditions
        scope_ids = {s.id for s in self.magic.scopes}
        difficulties = {d.label for d in self.roll_resolution.difficulty_modifiers}

        for f in self.facets:
            if f.stat not in stat_ids:
                errors.append(f"Facet '{f.id}' uses unknown stat '{f.stat}'.")
            if f.tradition and f.tradition not in traditions:
                errors.append(f"Facet '{f.id}' names unknown tradition '{f.tradition}'.")
        for tid, tdef in traditions.items():
            if tdef.stat not in stat_ids:
                errors.append(f"Tradition '{tid}' casts with unknown stat '{tdef.stat}'.")
            if tdef.facet not in facet_ids:
                errors.append(f"Tradition '{tid}' belongs to unknown Facet '{tdef.facet}'.")
        for s in self.magic.scopes:
            if s.difficulty not in difficulties:
                errors.append(f"Scope '{s.id}' has unknown difficulty '{s.difficulty}'.")
        for gap in self.combat.level_gap:
            if gap.difficulty not in difficulties:
                errors.append(f"Level gap {gap.gap} has unknown difficulty '{gap.difficulty}'.")
        if self.combat.defend.enemy_difficulty not in difficulties:
            errors.append("combat.defend.enemy_difficulty is not a difficulty label.")
        for opts in (self.combat.attack.full_success.pick_one,):
            for o in opts:
                if o not in self.combat.options:
                    errors.append(f"Attack option '{o}' is not defined in combat.options.")
        if self.hold_on.stat not in stat_ids:
            errors.append(f"hold_on.stat '{self.hold_on.stat}' is not a stat.")
        if self.slots.plus_stat not in stat_ids:
            errors.append(f"slots.plus_stat '{self.slots.plus_stat}' is not a stat.")
        levels = sorted(r.level for r in self.monsters.level_table)
        if levels != list(range(1, self.advancement.max_level + 1)):
            errors.append(f"monsters.level_table must cover levels 1-{self.advancement.max_level}.")

        for t in self.talents:
            if t.facet not in facet_ids:
                errors.append(f"Talent '{t.id}' belongs to unknown Facet '{t.facet}'.")
            for other in t.shared_with:
                if other not in facet_ids:
                    errors.append(f"Talent '{t.id}' is shared with unknown Facet '{other}'.")
            if t.requires:
                for req in t.requires.any_talent:
                    if req not in self._talent_map:
                        errors.append(f"Talent '{t.id}' requires unknown talent '{req}'.")
            granted = t.effects.get("grants_tradition")
            if granted and granted not in traditions:
                errors.append(f"Talent '{t.id}' grants unknown tradition '{granted}'.")

        for c in self.classes:
            if c.facet not in facet_ids:
                errors.append(f"Class '{c.id}' belongs to unknown Facet '{c.facet}'.")
            if len(c.talents) != self.advancement.starting_talents:
                errors.append(f"Class '{c.id}' has {len(c.talents)} talents; "
                              f"expected {self.advancement.starting_talents}.")
            for tid in c.talents:
                t = self._talent_map.get(tid)
                if t is None:
                    errors.append(f"Class '{c.id}' names unknown talent '{tid}'.")
                elif t.kind != "talent" or not t.on_menu_of(c.facet):
                    errors.append(f"Class '{c.id}': '{tid}' is not a talent on the {c.facet} menu.")
            sig = self._talent_map.get(c.signature)
            if sig is None:
                errors.append(f"Class '{c.id}' names unknown signature '{c.signature}'.")
            elif sig.kind != "signature" or not sig.on_menu_of(c.facet):
                errors.append(f"Class '{c.id}': '{c.signature}' is not a {c.facet} signature.")
            for item_id in c.kit:
                if item_id not in self._item_map:
                    errors.append(f"Class '{c.id}' kit names unknown item '{item_id}'.")

        for b in self.backgrounds:
            if b.facet and b.facet not in facet_ids:
                errors.append(f"Background '{b.id}' names unknown Facet '{b.facet}'.")
        for d in self.magic_domains:
            if d.tradition not in traditions:
                errors.append(f"Domain '{d.id}' names unknown tradition '{d.tradition}'.")
            if d.facet not in facet_ids:
                errors.append(f"Domain '{d.id}' names unknown Facet '{d.facet}'.")
        for lin in self.lineages:
            if lin.gift_domain_scope and lin.gift_domain_scope not in scope_ids:
                errors.append(f"Lineage '{lin.id}' gift scope '{lin.gift_domain_scope}' is not a scope.")
            if lin.gift_domain_scope and not lin.gift:
                errors.append(f"Lineage '{lin.id}' has a gift domain scope but no gift.")
            for dom in lin.gift_domains:
                if dom not in self._domain_map:
                    errors.append(f"Lineage '{lin.id}' gift domain '{dom}' is not a domain.")
        eq = self.equipment
        if eq is not None:
            for i in self.items:
                if i.weapon and i.weapon not in eq.weapon_categories:
                    errors.append(f"Item '{i.id}' has unknown weapon category '{i.weapon}'.")
                if i.armor and i.armor not in eq.armor:
                    errors.append(f"Item '{i.id}' has unknown armor category '{i.armor}'.")
                if i.kind and eq.weapon_kinds and i.kind not in eq.weapon_kinds:
                    errors.append(f"Item '{i.id}' has unknown weapon kind '{i.kind}'.")

        if errors:
            raise FacetLoadError("Cross-reference validation failed:\n"
                                 + "\n".join(f"  {e}" for e in errors))

    # ---------------------------------------------------------------- lookups
    def get_stat(self, stat_id: str) -> Optional[StatDef]:
        return self._stat_map.get(stat_id)

    def get_facet(self, facet_id: str) -> Optional[FacetDef]:
        return self._facet_map.get(facet_id)

    def get_talent(self, talent_id: str) -> Optional[TalentDef]:
        return self._talent_map.get(talent_id)

    def get_class(self, class_id: str) -> Optional[ClassDef]:
        return self._class_map.get(class_id)

    def get_background(self, background_id: str) -> Optional[BackgroundDef]:
        return self._background_map.get(background_id)

    def get_lineage(self, lineage_id: str) -> Optional[LineageDef]:
        return self._lineage_map.get(lineage_id)

    def get_item(self, item_id: str) -> Optional[ItemDef]:
        return self._item_map.get(item_id)

    def get_domain(self, domain_id: str) -> Optional[MagicDomainDef]:
        return self._domain_map.get(domain_id)

    def get_table(self, table_id: str) -> Optional[TableDef]:
        return self.tables.get(table_id)

    def talent_menu(self, facet_id: str, kind: str = "talent") -> list[TalentDef]:
        """Every talent (or signature) on a Facet's menu, shared talents included."""
        return [t for t in self.talents if t.kind == kind and t.on_menu_of(facet_id)]

    def classes_for_facet(self, facet_id: str) -> list[ClassDef]:
        return [c for c in self.classes if c.facet == facet_id]

    def domains_for_tradition(self, tradition: str, prismatic: Optional[bool] = None) -> list[MagicDomainDef]:
        return [d for d in self.magic_domains if d.tradition == tradition
                and (prismatic is None or d.prismatic == prismatic)]

    def difficulty_modifier(self, label: str) -> int:
        return self.roll_resolution.get_difficulty_modifier(label)

    def shift_difficulty(self, label: str, steps: int) -> str:
        """Move a difficulty `steps` easier (positive) or harder (negative), clamped."""
        order = self.roll_resolution.difficulty_labels_hard_to_easy()
        idx = order.index(label) if label in order else None
        if idx is None:
            raise ValueError(f"Unknown difficulty {label!r}")
        return order[max(0, min(len(order) - 1, idx + steps))]

    def harder_of(self, a: str, b: str) -> str:
        return a if self.difficulty_modifier(a) <= self.difficulty_modifier(b) else b

    def missing_required_tables(self) -> list[str]:
        """Required MM table ids (DESIGN §3.2) not present in the loaded tables."""
        return [t for t in REQUIRED_TABLE_IDS if t not in self.tables]

    # ------------------------------------------------------------- serialise
    def to_client_dict(self) -> dict:
        """The ruleset as a JSON-safe dict for clients."""
        def dump(obj):
            if isinstance(obj, BaseModel):
                return obj.model_dump()
            if isinstance(obj, list):
                return [dump(i) for i in obj]
            if isinstance(obj, dict):
                return {k: dump(v) for k, v in obj.items()}
            return obj

        out = {name: dump(getattr(self, name)) for name in _SINGLETONS}
        out.update({
            "stats": dump(self.stats),
            "facets": dump(self.facets),
            "talents": dump(self.talents),
            "classes": dump(self.classes),
            "backgrounds": dump(self.backgrounds),
            "lineages": dump(self.lineages),
            "items": dump(self.items),
            "magic_domains": dump(self.magic_domains),
            "equipment": dump(self.equipment),
            "tables": {tid: dump(t) for tid, t in self.tables.items()},
            "modules": [{"id": f.id, "name": f.name, "version": f.version} for f in self._files],
        })
        return out

    def module_refs(self) -> list[dict]:
        return [{"id": f.id, "version": f.version} for f in self._files]


def build_ruleset(active_facet_ids: list[str] | None = None) -> MergedRuleset:
    """Discover, load and merge Facet files: the core always, others by id.

    Raises:
        FacetLoadError: no files, no core, an invalid file, or a merge error.
    """
    facets_dir = settings.facets_dir
    all_paths = discover_facet_files(facets_dir)
    if not all_paths:
        raise FacetLoadError(f"No ruleset files found in {facets_dir.resolve()}.")

    wanted = set(active_facet_ids or [])
    loaded: list[FacetFile] = []
    found_ids: set[str] = set()
    for path in all_paths:
        ff = load_facet_file(path)
        found_ids.add(ff.id)
        if ff.id == "base" or ff.id in wanted:
            loaded.append(ff)
    unknown = wanted - found_ids
    if unknown:
        raise FacetLoadError(f"Unknown Facet module(s): {', '.join(sorted(unknown))}.")
    if not any(f.id == "base" for f in loaded):
        raise FacetLoadError("The base Facet must be present.")
    return MergedRuleset(loaded)
