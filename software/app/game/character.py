"""Character model — creation, validation, and skill advancement."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field, computed_field, model_validator

from app.facets.registry import MergedRuleset


SkillRankId = Literal["novice", "practiced", "expert", "master"]


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
        facet_levels: Facet levels earned per Facet, keyed by Facet ID. Cross-Facet
            levels are tracked separately so they can each count toward Major Advancement.
        rank_advances_by_facet: Rank advances toward the next level, per Facet.
        facet_level: (computed) primary-Facet levels earned; = facet_levels[primary_facet].
        total_facet_levels: (computed) sum of levels across ALL Facets (for Major Advancement).
        rank_advances_this_facet_level: (computed) advances toward the next primary-Facet level.
        career_advances: Total skill rank advances across all sessions (for encounter budget).
        techniques: List of unlocked technique IDs.
        techniques_used_this_session: Technique IDs marked used for "once per session" tracking.
        technique_choices: Dict of technique_id → chosen option (for Techniques with choices).
        background_id: The character's chosen Background ID (or None for custom backgrounds).
        specialty: The character's specialty text (from Background or custom).
        magic_domain: Primary magic domain ID if the character has magic.
        magic_tradition: "intuitive" (Spirit) or "scholarly" (Knowledge).
        magic_technique_active: True once the Tier 1 magic Technique is unlocked.
        endurance_current: Current Endurance in combat; None when not in combat.
        conditions: Active condition IDs in combat.
        posture: Current combat posture ("aggressive"|"measured"|"defensive"|"withdrawn").
        armor_downgrades_remaining: PC armor's per-scene Condition-downgrade
            budget (D2); None when unarmored or outside a scene. Persists
            across `combat_start`/`combat_end` within the same scene — two
            fights in one scene share the budget — and is only reinitialised
            via `combat.armor_budget` at the start of a new scene.
        reactions_this_exchange: Count of reactions taken so far this
            exchange (K1, BRIEF D8) — feeds `combat.reaction_cost`'s
            `is_first_reaction`. Reset to 0 by `_handle_end_exchange`.
    """

    name: str = Field(min_length=1, max_length=64)
    player_name: str = Field(min_length=1, max_length=32)
    primary_facet: str

    attributes: dict[str, int] = Field(default_factory=dict)
    skills: dict[str, SkillState] = Field(default_factory=dict)

    sparks: int = Field(default=3, ge=0)

    session_skill_points_remaining: int = Field(default=4, ge=0)
    skills_used_this_session: set[str] = Field(default_factory=set)
    facet_levels: dict[str, int] = Field(default_factory=dict)
    rank_advances_by_facet: dict[str, int] = Field(default_factory=dict)
    career_advances: int = Field(default=0, ge=0)
    # One Technique pick is granted per Facet level earned in ANY Facet and
    # spent by `technique_select` (D3, §6.4). Persisted across sessions.
    technique_picks_available: int = Field(default=0, ge=0)

    techniques: list[str] = Field(default_factory=list)
    techniques_used_this_session: list[str] = Field(default_factory=list)
    technique_choices: dict[str, str] = Field(default_factory=dict)

    # Background
    background_id: Optional[str] = None
    specialty: Optional[str] = None

    # Magic (persisted)
    magic_domain: Optional[str] = None
    secondary_magic_domain: Optional[str] = None  # Soul Communion T3 "Second Domain"
    # Tier 3 "Ascendant Domain" — a prismatic domain held *alongside* the
    # original. Kept apart from secondary_magic_domain because the routes cost
    # differently: Second Domain is one difficulty step harder, while Ascendant
    # pays with the Broad table instead and takes no step penalty (II.4b/II.4c).
    # One per character (II.3).
    ascendant_domain: Optional[str] = None
    # A domain taken from the *other* Facet's Tier 1, held alongside the first at
    # no difficulty penalty (II.3). One field per acquisition route, because the
    # route is what sets the price.
    cross_facet_domain: Optional[str] = None
    magic_tradition: Optional[str] = None  # "intuitive" | "scholarly"
    magic_technique_active: bool = False

    # Player-facing fields
    inventory: list[str] = Field(default_factory=list)
    notes_player: str = ""
    notes_mm: str = ""

    # Combat state — ephemeral, not persisted to .fof between sessions
    endurance_current: Optional[int] = None
    conditions: list[str] = Field(default_factory=list)
    posture: Optional[str] = None  # "aggressive"|"measured"|"defensive"|"withdrawn"
    armor: Optional[str] = None  # None | "light" | "heavy"
    armor_downgrades_remaining: Optional[int] = None
    reactions_this_exchange: int = 0

    # --- Derived Facet-level views (read-only; kept for .fof and UI compat) ---

    @computed_field
    @property
    def facet_level(self) -> int:
        """Primary-Facet levels earned. Backward-compatible with .fof and UI."""
        return self.facet_levels.get(self.primary_facet, 0)

    @computed_field
    @property
    def total_facet_levels(self) -> int:
        """Sum of Facet levels across all Facets — the Major Advancement counter."""
        return sum(self.facet_levels.values())

    @computed_field
    @property
    def rank_advances_this_facet_level(self) -> int:
        """Rank advances banked toward the next primary-Facet level."""
        return self.rank_advances_by_facet.get(self.primary_facet, 0)

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

    @property
    def endurance_max_base(self) -> int:
        """Base Endurance before ruleset modifiers. Use endurance_max(ruleset) for the real value."""
        return 4

    def endurance_max(self, ruleset: MergedRuleset) -> int:
        """Maximum Endurance pool: base 4 + Constitution modifier + Endurance skill rank modifier."""
        if not ruleset.combat:
            base = 4
        else:
            base = ruleset.combat.endurance.base
        con_mod = self.get_attribute_modifier("constitution", ruleset)
        end_skill_mod = self.get_skill_modifier("endurance", ruleset)
        return base + con_mod + end_skill_mod

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

    def _try_advance_rank(self, state: "SkillState", marks_to_add: int, marks_per_rank: int) -> int:
        """Add marks to a skill state, advancing rank as thresholds are crossed.

        Mutates state in place. Returns the number of rank advances that occurred.
        Stops at expert rank (the ceiling for advancement).
        """
        rank_order = ["novice", "practiced", "expert", "master"]
        current_idx = rank_order.index(state.rank)
        advances = 0
        for _ in range(marks_to_add):
            if state.rank == "master":
                break
            state.marks += 1
            if state.marks >= marks_per_rank:
                state.marks = 0
                state.rank = rank_order[current_idx + 1]
                current_idx += 1
                advances += 1
        return advances

    def _check_facet_level_threshold(self, facet_id: str, rank_advances: int, threshold: int) -> int:
        """Credit `rank_advances` in `facet_id` toward that Facet's level track.

        Every Facet — primary or cross — accrues its own levels, and each level
        counts toward `total_facet_levels` (and therefore Major Advancement).
        Returns the number of new Facet levels reached in this Facet.
        """
        levels_gained = 0
        for _ in range(rank_advances):
            self.rank_advances_by_facet[facet_id] = self.rank_advances_by_facet.get(facet_id, 0) + 1
            if self.rank_advances_by_facet[facet_id] >= threshold:
                self.facet_levels[facet_id] = self.facet_levels.get(facet_id, 0) + 1
                self.rank_advances_by_facet[facet_id] = 0
                levels_gained += 1
        return levels_gained

    def _check_major_advancement(self, major_threshold: int) -> bool:
        """Return True if total_facet_levels just crossed a Major Advancement threshold."""
        return self.total_facet_levels > 0 and self.total_facet_levels % major_threshold == 0

    def advance_skill(self, skill_id: str, marks_to_add: int, ruleset: MergedRuleset) -> dict:
        """Add marks to a skill, advancing rank if the threshold is met.

        Creates the skill at Novice rank if it does not yet exist on the character.
        Stops adding marks once Expert rank is reached.

        Args:
            skill_id: The skill to advance.
            marks_to_add: Number of marks to add (0 is a no-op).
            ruleset: Used to look up marks_per_rank, advancement config, and skill facet.

        Returns:
            A dict with keys: skill_id, rank_advances (int), facet_level_advances (int),
            major_advancement (bool).
        """
        if skill_id not in self.skills:
            self.skills[skill_id] = SkillState(skill_id=skill_id)

        state = self.skills[skill_id]
        marks_per_rank = ruleset.advancement.marks_per_rank if ruleset.advancement else 3
        threshold = ruleset.advancement.facet_level_threshold if ruleset.advancement else 5
        major_threshold = ruleset.advancement.major_advancement_threshold if ruleset.advancement else 3

        rank_advances = self._try_advance_rank(state, marks_to_add, marks_per_rank)
        self.career_advances += rank_advances

        sk_def = ruleset.get_skill(skill_id)
        facet_level_advances = 0
        if sk_def is not None and sk_def.facet:
            facet_level_advances = self._check_facet_level_threshold(sk_def.facet, rank_advances, threshold)

        # Each Facet level (any Facet) grants one Technique pick to spend later.
        self.technique_picks_available += facet_level_advances

        major = False
        if facet_level_advances > 0:
            major = self._check_major_advancement(major_threshold)

        return {
            "skill_id": skill_id,
            "rank_advances": rank_advances,
            "facet_level_advances": facet_level_advances,
            "major_advancement": major,
        }

    def select_technique(
        self, technique_id: str, ruleset: MergedRuleset, choice: Optional[str] = None
    ) -> tuple[bool, str]:
        """Spend one Technique pick on `technique_id` (§6.4). Single source of
        truth for the rule; the WebSocket handler and playtest harness both call it.

        Order of checks: not already held → prerequisites met (tree-agnostic) →
        a pick is available. On success, appends the Technique, decrements the
        pick budget, records any choice, and activates magic if the Technique is
        magic-granting. On failure, mutates nothing.

        Returns (ok, message); message is "ok" on success, else the reason.
        """
        if technique_id in self.techniques:
            return False, f"Technique '{technique_id}' already selected."

        tech_def = ruleset.get_technique(technique_id)
        if tech_def:
            missing = [p for p in tech_def.prerequisites if p not in self.techniques]
            if missing:
                return False, f"Technique '{technique_id}' requires: {', '.join(missing)}."

        if self.technique_picks_available <= 0:
            return False, "No Technique picks available — reach a Facet level to earn one."

        # Validated before anything is consumed: an illegal domain pick must not
        # burn the Technique slot on its way out.
        if tech_def and choice:
            valid, reason = self._validate_domain_choice(
                tech_def, str(choice), ruleset, technique_id
            )
            if not valid:
                return False, reason

        self.technique_picks_available -= 1
        self.techniques.append(technique_id)
        if choice:
            self.technique_choices[technique_id] = str(choice)
        if tech_def and tech_def.magic_granting:
            self.magic_technique_active = True
        if tech_def and choice:
            # Which slot the choice lands in is the whole difference between the
            # magic Techniques, and the slot is what sets the price:
            #   ascendant_domain      — prismatic, Broad table, no step penalty
            #   secondary_magic_domain — Second Domain, one step harder
            #   cross_facet_domain    — the other Facet's Tier 1, untaxed
            #   magic_domain          — the original
            if tech_def.grants_prismatic_domain:
                self.ascendant_domain = str(choice)
            elif tech_def.grants_secondary_domain:
                self.secondary_magic_domain = str(choice)
            elif tech_def.magic_granting:
                # Formalizing the Background's domain re-sets the same value;
                # anything else is a genuine second domain from the other Facet.
                if self.magic_domain in (None, str(choice)):
                    self.magic_domain = str(choice)
                else:
                    self.cross_facet_domain = str(choice)
        return True, "ok"

    def held_domains(self) -> list[str]:
        """Every domain the character currently practises, by any route."""
        return [
            d for d in (
                self.magic_domain,
                self.cross_facet_domain,
                self.secondary_magic_domain,
                self.ascendant_domain,
            ) if d
        ]

    @staticmethod
    def _facet_domains(facet_id: str | None, ruleset) -> list:
        """The domain catalog for a Facet's tree. Body has no domains of its own.

        Keyed on the *Technique's* Facet, not the character's primary one: a
        cross-training character choosing from Soul's tree picks Soul domains
        (PHB II.3 — "choosing from that Facet's domain list").
        """
        if not ruleset.magic or facet_id is None:
            return []
        pools = {
            "soul": ruleset.magic.soul_domains,
            "mind": ruleset.magic.mind_domains,
        }
        return pools.get(facet_id, [])

    def _validate_domain_choice(
        self, tech_def, choice: str, ruleset, technique_id: str
    ) -> tuple[bool, str]:
        """Ascendant Domain takes a prismatic domain; Second Domain takes a
        non-prismatic one that differs from the first. Both draw from the domain
        list of the Facet whose tree the Technique lives in. Techniques whose
        choice isn't a domain at all pass straight through.
        """
        grants_domain = (
            tech_def.grants_prismatic_domain
            or tech_def.grants_secondary_domain
            or tech_def.magic_granting
        )
        if not grants_domain:
            return True, "ok"

        facet_id = ruleset.get_technique_facet(technique_id)
        pool = self._facet_domains(facet_id, ruleset)
        domain = next((d for d in pool if d.id == choice), None)
        if domain is None:
            return False, (
                f"'{choice}' is not a domain of the Facet of the "
                f"{(facet_id or 'unknown').capitalize()}."
            )

        # Re-selecting the domain a Background already granted is not a duplicate:
        # the Tier 1 Technique *formalizes* that domain and unlocks full scope
        # (II.3, II.5). It adds nothing, so it is exempt from the checks below.
        formalizing = tech_def.magic_granting and choice == self.magic_domain

        # Otherwise no domain may be practised twice, by any route.
        if choice in self.held_domains() and not formalizing:
            return False, f"You already practise '{choice}'."

        if tech_def.grants_prismatic_domain:
            if domain.type != "broad":
                return False, (
                    f"Ascendant Domain requires a prismatic domain; "
                    f"'{choice}' is not one."
                )
            # One prismatic territory per character (II.3).
            if self.ascendant_domain:
                return False, (
                    f"You already hold the prismatic domain "
                    f"'{self.ascendant_domain}' — a character masters only one."
                )
            return True, "ok"

        # Every non-Ascendant route takes a non-prismatic domain.
        if domain.type == "broad":
            return False, (
                f"Prismatic territories like '{choice}' require the Ascendant "
                f"Domain Technique."
            )

        if (
            tech_def.magic_granting
            and not formalizing
            and self.magic_domain
            and self.cross_facet_domain
        ):
            return False, (
                "You already practise a domain in each Facet — a further domain "
                "requires the Second Domain Technique."
            )
        return True, "ok"

    def to_client_dict(self) -> dict:
        """Serialize the character to a JSON-safe dict for sending to clients."""
        d = self.model_dump()
        # Pydantic preserves set type; JSON requires list
        d["skills_used_this_session"] = sorted(self.skills_used_this_session)
        return d

    def to_fof(
        self,
        module_refs: list[dict],
        session_id: str,
        created_at: str | None = None,
    ) -> dict:
        """Serialize this character to a FOF-format dict suitable for yaml.dump.

        Only skills with non-default state (rank != novice OR marks != 0) are
        included in the output. Absent skills are implicitly novice/0 on reload.

        Args:
            module_refs: List of {"id": ..., "version": ...} dicts for loaded modules.
            session_id: Used as the campaign_id and to suffix the character's file id.
            created_at: ISO timestamp string; defaults to now if not supplied.
        """
        now = datetime.now(tz=timezone.utc).isoformat()
        slug = re.sub(r"[^a-z0-9]+", "-", self.player_name.lower()).strip("-")

        non_default_skills = {
            skill_id: {"rank": state.rank, "marks": state.marks}
            for skill_id, state in self.skills.items()
            if state.rank != "novice" or state.marks != 0
        }

        char_block: dict = {
            "name": self.name,
            "player_name": self.player_name,
            "primary_facet": self.primary_facet,
            "attributes": dict(self.attributes),
            "skills": non_default_skills,
            "sparks": self.sparks,
            "session_skill_points_remaining": self.session_skill_points_remaining,
            "facet_levels": dict(self.facet_levels),
            "rank_advances_by_facet": dict(self.rank_advances_by_facet),
            # Derived views, written for human readability and older readers.
            "facet_level": self.facet_level,
            "total_facet_levels": self.total_facet_levels,
            "career_advances": self.career_advances,
            "technique_picks_available": self.technique_picks_available,
            "techniques": list(self.techniques),
            "technique_choices": dict(self.technique_choices),
        }
        if self.background_id is not None:
            char_block["background_id"] = self.background_id
        if self.specialty is not None:
            char_block["specialty"] = self.specialty
        if self.magic_domain is not None:
            char_block["magic_domain"] = self.magic_domain
            char_block["magic_tradition"] = self.magic_tradition
            char_block["magic_technique_active"] = self.magic_technique_active
        if self.secondary_magic_domain is not None:
            char_block["secondary_magic_domain"] = self.secondary_magic_domain
        if self.ascendant_domain is not None:
            char_block["ascendant_domain"] = self.ascendant_domain
        if self.cross_facet_domain is not None:
            char_block["cross_facet_domain"] = self.cross_facet_domain
        # Persist combat state so server restarts mid-combat can resume
        if self.endurance_current is not None:
            char_block["endurance_current"] = self.endurance_current
        if self.conditions:
            char_block["conditions"] = list(self.conditions)
        if self.posture is not None:
            char_block["posture"] = self.posture
        if self.armor is not None:
            char_block["armor"] = self.armor
        if self.armor_downgrades_remaining is not None:
            char_block["armor_downgrades_remaining"] = self.armor_downgrades_remaining
        if self.inventory:
            char_block["inventory"] = list(self.inventory)
        if self.notes_player:
            char_block["notes_player"] = self.notes_player
        if self.notes_mm:
            char_block["notes_mm"] = self.notes_mm

        return {
            "fof_version": "0.1",
            "type": "character",
            "id": f"{slug}-{session_id[:8]}",
            "name": self.name,
            "version": "1.0.0",
            "authors": [self.player_name],
            "ruleset": {"modules": module_refs},
            "campaign_id": session_id,
            "character": char_block,
            "created_at": created_at or now,
            "last_modified": now,
        }

    @classmethod
    def from_fof(cls, fof_dict: dict, ruleset=None) -> "Character":
        """Deserialize a Character from a FOF-format dict.

        Args:
            fof_dict: A dict produced by yaml.safe_load on a character .fof file.
            ruleset: Optional MergedRuleset. When provided, validate_against_ruleset()
                     is called and any validation errors are raised as ValueError.
                     Without a ruleset, the caller must validate manually.

        Returns:
            A Character instance.

        Raises:
            ValueError: If the dict is not a character file, is missing required fields,
                        or fails ruleset validation when a ruleset is provided.
        """
        if fof_dict.get("type") != "character":
            raise ValueError(
                f"Expected type 'character', got {fof_dict.get('type')!r}. "
                "Only character .fof files can be loaded here."
            )

        char_block = fof_dict.get("character")
        if not isinstance(char_block, dict):
            raise ValueError("Missing or invalid 'character' block in FOF file.")

        for required_field in ("name", "player_name", "primary_facet", "attributes"):
            if required_field not in char_block:
                raise ValueError(f"Missing required field 'character.{required_field}'.")

        raw_skills = char_block.get("skills") or {}
        skills: dict[str, SkillState] = {}
        for skill_id, state in raw_skills.items():
            if isinstance(state, dict):
                skills[skill_id] = SkillState(
                    skill_id=skill_id,
                    rank=state.get("rank", "novice"),
                    marks=state.get("marks", 0),
                )

        # Per-Facet level tracking. Prefer the canonical dicts; fall back to the
        # older flat fields (facet_level / rank_advances_this_facet_level) by
        # crediting them to the primary Facet.
        primary_facet = char_block["primary_facet"]
        facet_levels = char_block.get("facet_levels")
        rank_advances_by_facet = char_block.get("rank_advances_by_facet")
        if facet_levels is None:
            facet_levels = {}
            legacy_level = char_block.get("facet_level", 0)
            if legacy_level:
                facet_levels[primary_facet] = legacy_level
        if rank_advances_by_facet is None:
            rank_advances_by_facet = {}
            legacy_advances = char_block.get("rank_advances_this_facet_level", 0)
            if legacy_advances:
                rank_advances_by_facet[primary_facet] = legacy_advances

        character = cls(
            name=char_block["name"],
            player_name=char_block["player_name"],
            primary_facet=primary_facet,
            attributes=char_block["attributes"],
            skills=skills,
            sparks=char_block.get("sparks", 3),
            session_skill_points_remaining=char_block.get("session_skill_points_remaining", 4),
            facet_levels=facet_levels,
            rank_advances_by_facet=rank_advances_by_facet,
            career_advances=char_block.get("career_advances", 0),
            technique_picks_available=char_block.get("technique_picks_available", 0),
            techniques=char_block.get("techniques") or [],
            technique_choices=char_block.get("technique_choices") or {},
            background_id=char_block.get("background_id"),
            specialty=char_block.get("specialty"),
            magic_domain=char_block.get("magic_domain"),
            secondary_magic_domain=char_block.get("secondary_magic_domain"),
            ascendant_domain=char_block.get("ascendant_domain"),
            cross_facet_domain=char_block.get("cross_facet_domain"),
            magic_tradition=char_block.get("magic_tradition"),
            magic_technique_active=char_block.get("magic_technique_active", False),
            endurance_current=char_block.get("endurance_current"),
            conditions=char_block.get("conditions") or [],
            posture=char_block.get("posture"),
            armor=char_block.get("armor"),
            armor_downgrades_remaining=char_block.get("armor_downgrades_remaining"),
            inventory=char_block.get("inventory") or [],
            notes_player=char_block.get("notes_player") or "",
            notes_mm=char_block.get("notes_mm") or "",
        )
        if ruleset is not None:
            errors = character.validate_against_ruleset(ruleset)
            if errors:
                raise ValueError(f"Character fails ruleset validation: {'; '.join(errors)}")
        return character


def create_default_character(
    name: str,
    player_name: str,
    primary_facet: str,
    attributes: dict[str, int],
    ruleset: MergedRuleset,
    background_id: str | None = None,
    magic_domain: str | None = None,
) -> tuple[Character | None, list[str]]:
    """Create a character and validate it against the ruleset.

    Initialises all active skills at Novice rank. If a background_id is
    supplied, applies its Starting Skill (Practiced), Secondary Skill (Novice
    with 1 mark), specialty, and domain_origin if applicable.

    Args:
        name: Character's in-fiction name.
        player_name: Player's display name (used as the session key).
        primary_facet: Chosen Facet ID.
        attributes: Minor attribute ratings (must satisfy the ruleset's distribution rules).
        ruleset: The session's merged ruleset.
        background_id: Optional background ID to apply at creation.
        magic_domain: Domain ID if the character has magic via a magic-granting background.

    Returns:
        A tuple (Character, []) on success, or (None, [error strings]) on validation failure.
    """
    skills = {sk.id: SkillState(skill_id=sk.id) for sk in ruleset.skills if sk.status == "active"}
    sparks = ruleset.spark.base_sparks_per_session if ruleset.spark else 3
    session_points = ruleset.advancement.session_skill_points if ruleset.advancement else 4

    specialty: str | None = None
    resolved_magic_domain: str | None = magic_domain
    resolved_magic_tradition: str | None = None
    career_advances = 0

    # Apply Background
    bg = ruleset.get_background(background_id) if background_id else None
    if bg:
        specialty = bg.specialty

        # Starting Skill → Practiced
        if bg.starting_skill in skills:
            skills[bg.starting_skill].rank = "practiced"
            skills[bg.starting_skill].marks = 0
            career_advances += 1  # one rank advance (novice → practiced)
        elif bg.starting_skill:
            # Skill not initialised yet (shouldn't happen with active skills) — create it
            skills[bg.starting_skill] = SkillState(
                skill_id=bg.starting_skill, rank="practiced", marks=0
            )
            career_advances += 1

        # Secondary Skill → Novice with 1 mark.
        # Magic-granting Backgrounds replace the secondary skill with the
        # domain origin when a domain is actually chosen (PHB II.5); without
        # a domain they grant the secondary skill like any other Background.
        skip_secondary = bg.domain_replaces_secondary and magic_domain
        if bg.secondary_skill and not skip_secondary:
            if bg.secondary_skill in skills:
                skills[bg.secondary_skill].marks = 1
            else:
                skills[bg.secondary_skill] = SkillState(
                    skill_id=bg.secondary_skill, rank="novice", marks=1
                )

        # Resolve magic domain and tradition if magic_domain is provided
        if magic_domain:
            resolved_magic_domain = magic_domain
            if ruleset.magic:
                domain_def = ruleset.magic.get_domain(magic_domain)
                if domain_def:
                    resolved_magic_tradition = domain_def.tradition

    character = Character(
        name=name,
        player_name=player_name,
        primary_facet=primary_facet,
        attributes=attributes,
        skills=skills,
        sparks=sparks,
        session_skill_points_remaining=session_points,
        background_id=background_id,
        specialty=specialty,
        magic_domain=resolved_magic_domain,
        magic_tradition=resolved_magic_tradition,
        career_advances=career_advances,
    )

    errors = character.validate_against_ruleset(ruleset)
    if errors:
        return None, errors

    return character, []
