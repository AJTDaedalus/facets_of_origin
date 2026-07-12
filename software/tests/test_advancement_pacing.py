"""Advancement pacing regression tests (WS-B / DESIGN §6.3).

This file is the guard against a future content or constant change silently
altering advancement pacing. It encodes three things the v0.3 ruleset must hold:

  1. Facet levels land at exactly 5, 10, and 15 rank advances
     (`facet_level_threshold: 5`, driven through the real Character engine).
  2. The first Major Advancement fires with Facet level 3
     (`major_advancement_threshold: 3`), including when the third level is
     reached across two Facets (2 primary + 1 cross) — the case that only
     works once `_check_facet_level_threshold` credits non-primary advances.
  3. The DESIGN §6.3 session projections: a dedicated character reaches
     Facet level 3 (Tier 3 + first Major) at roughly session 12 / 15 / 19 for
     100% / 80% / 60% primary-SP efficiency.

Written BEFORE the constant change (B2) and the per-Facet tracking rewrite
(B3). It fails against the current `facet_level_threshold: 6` /
`major_advancement_threshold: 4` constants and the primary-only level counter.
"""
import math

import pytest

from app.game.character import Character, create_default_character


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RANKS_PER_SKILL = 3  # novice → practiced → expert → master


def _active_skills(ruleset, facet: str) -> list[str]:
    return [s.id for s in ruleset.skills if s.facet == facet and s.status == "active"]


def _secondary_facet(ruleset, primary: str) -> str:
    facets = sorted({s.facet for s in ruleset.skills if s.status == "active"})
    return next(f for f in facets if f != primary)


def _new_character(ruleset, valid_attributes, primary: str = "body") -> Character:
    char, errors = create_default_character(
        name="Pacing", player_name="P",
        primary_facet=primary, attributes=valid_attributes,
        ruleset=ruleset,
    )
    assert not errors, errors
    return char


def _advance_marks(char: Character, ruleset, skills: list[str], marks: int) -> int:
    """Add `marks` marks one skill at a time, filling a skill toward its next
    rank before moving on (the efficient-play model DESIGN §6.3 projects), and
    skipping any skill already at master. Returns total rank advances.

    Marks that fall on an all-maxed skill list are dropped, so a caller may
    request the full 15-advance ceiling without overflowing.
    """
    advances = 0
    added = 0
    while added < marks:
        sid = next(
            (s for s in skills
             if char.skills.get(s) is None or char.skills[s].rank != "master"),
            None,
        )
        if sid is None:  # every skill maxed
            break
        result = char.advance_skill(sid, 1, ruleset)
        advances += result["rank_advances"]
        added += 1
    return advances


# ---------------------------------------------------------------------------
# 1. Facet levels land at 5 / 10 / 15 advances
# ---------------------------------------------------------------------------

class TestFacetLevelThresholds:
    def test_threshold_is_five(self, ruleset):
        assert ruleset.advancement.facet_level_threshold == 5

    def test_first_level_at_five_advances(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        primary = _active_skills(ruleset, "body")
        # Four advances: no level yet.
        _advance_marks(char, ruleset, primary, 4 * ruleset.advancement.marks_per_rank)
        assert char.facet_level == 0
        # Fifth advance: level 1.
        _advance_marks(char, ruleset, primary, 1 * ruleset.advancement.marks_per_rank)
        assert char.facet_level == 1

    def test_levels_land_at_5_10_15(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        primary = _active_skills(ruleset, "body")
        mpr = ruleset.advancement.marks_per_rank
        # Max out all five primary skills = 15 advances.
        total_advances = _advance_marks(char, ruleset, primary, 5 * RANKS_PER_SKILL * mpr)
        assert total_advances == 15
        # 15 advances at threshold 5 = exactly 3 levels, no remainder.
        assert char.facet_level == 3
        assert char.rank_advances_this_facet_level == 0

    def test_level_three_reachable_in_facet(self, ruleset):
        """A 6th active skill would not break reachability, but any change to
        threshold or skill count that pushes level 3 past the in-Facet ceiling
        must trip this test."""
        adv = ruleset.advancement
        advances_to_level_3 = 3 * adv.facet_level_threshold
        in_facet_ceiling = 5 * RANKS_PER_SKILL  # 5 skills × 3 rank advances
        assert advances_to_level_3 <= in_facet_ceiling
        assert advances_to_level_3 == 15


# ---------------------------------------------------------------------------
# 2. First Major Advancement fires at Facet level 3
# ---------------------------------------------------------------------------

class TestFirstMajorAdvancement:
    def test_major_threshold_is_three(self, ruleset):
        assert ruleset.advancement.major_advancement_threshold == 3

    def test_major_fires_at_level_three_all_primary(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        primary = _active_skills(ruleset, "body")
        mpr = ruleset.advancement.marks_per_rank
        major_seen = False
        for sid in primary:
            for _ in range(RANKS_PER_SKILL):
                result = char.advance_skill(sid, mpr, ruleset)
                major_seen = major_seen or result["major_advancement"]
        assert char.total_facet_levels == 3
        assert major_seen

    def test_major_fires_across_two_facets(self, ruleset, valid_attributes):
        """Third level reached via 2 primary + 1 cross-Facet level.

        This is the assertion that requires `_check_facet_level_threshold` to
        credit non-primary advances (B3). Until then, cross-Facet advances
        return 0 and `total_facet_levels` never reaches 3 this way.
        """
        char = _new_character(ruleset, valid_attributes)
        primary = _active_skills(ruleset, "body")
        secondary = _secondary_facet(ruleset, "body")
        cross = _active_skills(ruleset, secondary)
        mpr = ruleset.advancement.marks_per_rank
        threshold = ruleset.advancement.facet_level_threshold

        # Two primary levels = 2 × threshold advances.
        _advance_marks(char, ruleset, primary, 2 * threshold * mpr)
        assert char.total_facet_levels == 2

        # One cross-Facet level = threshold advances in the secondary Facet.
        major_seen = False
        added = 0
        i = 0
        while added < threshold:
            sid = cross[i % len(cross)]
            i += 1
            if char.skills.get(sid) is not None and char.skills[sid].rank == "master":
                continue
            result = char.advance_skill(sid, mpr, ruleset)
            added += result["rank_advances"]
            major_seen = major_seen or result["major_advancement"]

        assert char.total_facet_levels == 3
        assert char.facet_level == 2  # primary unchanged by the cross-Facet level
        assert major_seen


# ---------------------------------------------------------------------------
# 3. Session projections (DESIGN §6.3): s12 / s15 / s19
# ---------------------------------------------------------------------------

def _project_sessions_to_level_three(ruleset, efficiency: float) -> int:
    """Sessions for a dedicated character at `efficiency` primary-SP to reach
    Facet level 3, derived from ruleset constants (DESIGN §6.3)."""
    adv = ruleset.advancement
    marks_to_level_3 = 3 * adv.facet_level_threshold * adv.marks_per_rank
    marks_per_session = efficiency * adv.session_skill_points
    return math.ceil(marks_to_level_3 / marks_per_session)


class TestSessionProjections:
    @pytest.mark.parametrize("efficiency,expected_session", [
        (1.0, 12),
        (0.8, 15),
        (0.6, 19),
    ])
    def test_projection_matches_design_table(self, ruleset, efficiency, expected_session):
        assert _project_sessions_to_level_three(ruleset, efficiency) == expected_session

    def test_engine_simulation_reaches_level_three_at_session_twelve(self, ruleset, valid_attributes):
        """Drive the real engine at 100% efficiency (4 primary marks/session)
        and confirm Facet level 3 + first Major land on session 12."""
        char = _new_character(ruleset, valid_attributes)
        primary = _active_skills(ruleset, "body")
        sp = ruleset.advancement.session_skill_points
        milestone_session = None
        for session in range(1, 40):
            _advance_marks(char, ruleset, primary, sp)
            if char.facet_level >= 3 and milestone_session is None:
                milestone_session = session
                break
        assert milestone_session == 12
        assert char.total_facet_levels == 3
