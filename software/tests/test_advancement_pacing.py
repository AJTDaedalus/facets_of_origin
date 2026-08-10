"""Advancement pacing and differentiation tests (D16).

This file is the guard against a future content or constant change silently
altering advancement. It encodes what the D16 ruleset must hold:

  1. Rank caps: at most 3 skills per Facet beyond Practiced, at most 1 at
     Master. Enforced on every Facet, primary and cross-trained alike.
  2. Escalating marks: 3 / 5 / 8 per rank advance. A fully-shaped Facet is
     1 Master / 2 Expert / 2 Practiced = 9 rank advances = 38 marks.
  3. Facet levels land at exactly 3, 6, and 9 rank advances
     (`facet_level_threshold: 3`), driven through the real Character engine,
     so all three Technique picks stay inside the primary Facet.
  4. The first Major Advancement fires with Facet level 3, including when the
     third level is reached across two Facets.
  5. **Differentiation** — the ruling itself (`DECISIONS.md` D16): two maximal
     same-Facet builds can end visibly different and never reconverge.

Supersedes the v0.3 pacing assertions (threshold 5, flat 3 marks, levels at
5/10/15, level 3 at session 12). See `docs/BRIEF_advancement_differentiation.md`.
"""
import math

import pytest

from app.game.character import Character, create_default_character


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RANKS_PER_SKILL = 3        # novice → practiced → expert → master
SHAPED_ADVANCES = 9        # 1 Master (3) + 2 Expert (2 each) + 2 Practiced (1 each)
SHAPED_MARKS = 38          # 5×3 + 3×5 + 1×8
RANK_ORDER = ["practiced", "expert", "master"]


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


def _marks_to_reach(ruleset, top_rank: str) -> int:
    """Total marks to take one skill from Novice to `top_rank`."""
    mpr = ruleset.advancement.marks_per_rank
    return sum(mpr.for_rank(r) for r in RANK_ORDER[:RANK_ORDER.index(top_rank) + 1])


def _build_shape(char, ruleset, plan: dict[str, str]) -> tuple[int, int]:
    """Advance each skill in `plan` to its target rank. Returns (marks, advances)."""
    marks = advances = 0
    for skill_id, top in plan.items():
        for rank in RANK_ORDER[:RANK_ORDER.index(top) + 1]:
            cost = ruleset.advancement.marks_per_rank.for_rank(rank)
            result = char.advance_skill(skill_id, cost, ruleset)
            marks += cost
            advances += result["rank_advances"]
    return marks, advances


def _full_shape(skills: list[str]) -> dict[str, str]:
    """The maximal legal shape for a 5-skill Facet: 1 Master, 2 Expert, 2 Practiced."""
    return {
        skills[0]: "master",
        skills[1]: "expert", skills[2]: "expert",
        skills[3]: "practiced", skills[4]: "practiced",
    }


def _spend_marks(char: Character, ruleset, skills: list[str], marks: int) -> int:
    """Add `marks` marks one at a time the way a player optimising for Facet
    levels would: always buy the **cheapest** next rank advance available,
    finishing a part-paid skill before starting an equally-priced one.

    Under the escalating curve this is breadth-first to Practiced, then Expert,
    then the single Master — which is exactly the shaped ceiling, so the model
    also gives the true session *floor*. Skills the caps have walled off are
    skipped; marks with no legal target are dropped, so a caller may request
    more than the shape can absorb without overflowing.
    """
    mpr = ruleset.advancement.marks_per_rank
    order = ["novice", "practiced", "expert", "master"]
    advances = 0
    added = 0
    while added < marks:
        candidates = []
        for sid in skills:
            state = char.skills.get(sid)
            rank = state.rank if state else "novice"
            if rank == char.rank_ceiling_for(sid, ruleset):
                continue
            next_rank = order[order.index(rank) + 1]
            banked = state.marks if state else 0
            # Cheapest remaining cost first; break ties toward the skill already
            # part-paid, so marks are never stranded across parallel skills.
            candidates.append((mpr.for_rank(next_rank) - banked, -banked, sid))
        if not candidates:  # Facet fully shaped — nothing legal left to raise
            break
        _, _, sid = min(candidates)
        advances += char.advance_skill(sid, 1, ruleset)["rank_advances"]
        added += 1
    return advances


# ---------------------------------------------------------------------------
# 1. Rank caps — the ruling
# ---------------------------------------------------------------------------

class TestRankCaps:
    def test_caps_are_three_beyond_practiced_and_one_master(self, ruleset):
        caps = ruleset.advancement.rank_caps
        assert caps.beyond_practiced == 3
        assert caps.master == 1

    def test_fourth_skill_cannot_pass_practiced(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, _full_shape(body))
        with pytest.raises(ValueError, match="cannot rise past Practiced"):
            char.advance_skill(body[3], 1, ruleset)

    def test_second_skill_cannot_reach_master(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, _full_shape(body))
        assert char.skills[body[1]].rank == "expert"
        with pytest.raises(ValueError, match="cannot rise past Expert"):
            char.advance_skill(body[1], 1, ruleset)

    def test_refusal_adds_no_marks(self, ruleset, valid_attributes):
        """Refuse, never absorb — a mark must not bank toward a forbidden rank."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, _full_shape(body))
        before = (char.skills[body[3]].rank, char.skills[body[3]].marks, char.career_advances)
        with pytest.raises(ValueError):
            char.advance_skill(body[3], 1, ruleset)
        assert (char.skills[body[3]].rank, char.skills[body[3]].marks,
                char.career_advances) == before

    def test_slot_is_claimed_on_commitment_not_arrival(self, ruleset, valid_attributes):
        """One mark past Practiced claims the slot, so two skills cannot both
        bank toward the last one and strand."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        for sid in body[:3]:
            char.advance_skill(sid, ruleset.advancement.marks_per_rank.for_rank("practiced"), ruleset)
            char.advance_skill(sid, 1, ruleset)     # one mark toward Expert
            assert char.skills[sid].rank == "practiced" and char.skills[sid].marks == 1
        # Three slots now committed even though none has arrived at Expert.
        char.advance_skill(body[3], ruleset.advancement.marks_per_rank.for_rank("practiced"), ruleset)
        with pytest.raises(ValueError, match="cannot rise past Practiced"):
            char.advance_skill(body[3], 1, ruleset)

    def test_caps_bind_cross_facet_too(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        secondary = _secondary_facet(ruleset, "body")
        cross = _active_skills(ruleset, secondary)
        _build_shape(char, ruleset, _full_shape(cross))
        with pytest.raises(ValueError, match="cannot rise past Practiced"):
            char.advance_skill(cross[3], 1, ruleset)

    def test_spend_skill_point_does_not_burn_the_point_on_refusal(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, _full_shape(body))
        char.session_skill_points_remaining = 4
        char.skills_used_this_session = set()
        with pytest.raises(ValueError, match="cannot rise past Practiced"):
            char.spend_skill_point(body[3], ruleset)
        assert char.session_skill_points_remaining == 4


# ---------------------------------------------------------------------------
# 2. Escalating marks
# ---------------------------------------------------------------------------

class TestEscalatingMarks:
    def test_marks_per_rank_is_three_five_eight(self, ruleset):
        mpr = ruleset.advancement.marks_per_rank
        assert (mpr.practiced, mpr.expert, mpr.master) == (3, 5, 8)

    def test_onboarding_cost_is_unchanged(self, ruleset):
        """Novice → Practiced stays 3: the early game is the hook, untouched."""
        assert ruleset.advancement.marks_per_rank.for_rank("practiced") == 3

    def test_one_skill_to_master_costs_sixteen(self, ruleset):
        assert _marks_to_reach(ruleset, "master") == 16

    def test_full_shape_costs_thirty_eight_marks(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        marks, advances = _build_shape(char, ruleset, _full_shape(body))
        assert marks == SHAPED_MARKS
        assert advances == SHAPED_ADVANCES

    def test_legacy_flat_integer_still_loads(self):
        """Pre-D16 `marks_per_rank: 3` expands across all tiers, with a warning."""
        from app.facets.schema import AdvancementDef
        with pytest.warns(DeprecationWarning):
            adv = AdvancementDef(marks_per_rank=3)
        mpr = adv.marks_per_rank
        assert (mpr.practiced, mpr.expert, mpr.master) == (3, 3, 3)

    def test_omitted_caps_mean_uncapped(self, ruleset, valid_attributes):
        """A homebrew Facet that omits rank_caps is not silently constrained."""
        from app.facets.schema import AdvancementDef
        assert AdvancementDef().rank_caps.beyond_practiced is None
        assert AdvancementDef().rank_caps.master is None


# ---------------------------------------------------------------------------
# 3. Facet levels land at 3 / 6 / 9 advances
# ---------------------------------------------------------------------------

class TestFacetLevelThresholds:
    def test_threshold_is_three(self, ruleset):
        assert ruleset.advancement.facet_level_threshold == 3

    def test_first_level_at_three_advances(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, {body[0]: "practiced", body[1]: "practiced"})
        assert char.facet_level == 0
        _build_shape(char, ruleset, {body[2]: "practiced"})
        assert char.facet_level == 1

    def test_levels_land_at_3_6_9(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _, advances = _build_shape(char, ruleset, _full_shape(body))
        assert advances == SHAPED_ADVANCES
        assert char.facet_level == 3
        assert char.rank_advances_this_facet_level == 0

    def test_level_three_reachable_inside_the_primary_facet(self, ruleset):
        """All three Technique picks — including the magic formalization arc —
        must stay reachable without cross-training. Any threshold or cap change
        that pushes level 3 past the shaped ceiling must trip this."""
        adv = ruleset.advancement
        assert 3 * adv.facet_level_threshold <= SHAPED_ADVANCES

    def test_three_technique_picks_by_level_three(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _build_shape(char, ruleset, _full_shape(body))
        assert char.technique_picks_available == 3


# ---------------------------------------------------------------------------
# 4. First Major Advancement fires at Facet level 3
# ---------------------------------------------------------------------------

class TestFirstMajorAdvancement:
    def test_major_threshold_is_three(self, ruleset):
        assert ruleset.advancement.major_advancement_threshold == 3

    def test_major_fires_at_level_three_all_primary(self, ruleset, valid_attributes):
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        major_seen = False
        for skill_id, top in _full_shape(body).items():
            for rank in RANK_ORDER[:RANK_ORDER.index(top) + 1]:
                cost = ruleset.advancement.marks_per_rank.for_rank(rank)
                major_seen = char.advance_skill(skill_id, cost, ruleset)["major_advancement"] or major_seen
        assert char.total_facet_levels == 3
        assert major_seen

    def test_major_fires_across_two_facets(self, ruleset, valid_attributes):
        """Third level reached via 2 primary + 1 cross-Facet level — the case
        that only works once `_check_facet_level_threshold` credits non-primary
        advances."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        cross = _active_skills(ruleset, _secondary_facet(ruleset, "body"))

        # Two primary levels = 6 advances: 2 Expert (4) + 2 Practiced (2).
        _build_shape(char, ruleset, {
            body[0]: "expert", body[1]: "expert",
            body[2]: "practiced", body[3]: "practiced",
        })
        assert char.total_facet_levels == 2

        # One cross-Facet level = 3 advances in the secondary Facet.
        major_seen = False
        for sid in cross[:3]:
            cost = ruleset.advancement.marks_per_rank.for_rank("practiced")
            major_seen = char.advance_skill(sid, cost, ruleset)["major_advancement"] or major_seen

        assert char.total_facet_levels == 3
        assert char.facet_level == 2  # primary unchanged by the cross-Facet level
        assert major_seen


# ---------------------------------------------------------------------------
# 5. Differentiation — the ruling (D16)
# ---------------------------------------------------------------------------

class TestDifferentiation:
    def test_two_maximal_same_facet_builds_differ(self, ruleset, valid_attributes):
        """A ranger and a barbarian both play out their whole Body Facet and
        still do not have the same sheet. This is the ruling, as a test."""
        body = _active_skills(ruleset, "body")
        brawler = _new_character(ruleset, valid_attributes)
        scout = _new_character(ruleset, valid_attributes)

        _build_shape(brawler, ruleset, {
            body[1]: "master", body[0]: "expert", body[4]: "expert",
            body[2]: "practiced", body[3]: "practiced",
        })
        _build_shape(scout, ruleset, {
            body[2]: "master", body[3]: "expert", body[0]: "expert",
            body[1]: "practiced", body[4]: "practiced",
        })

        # Both are finished — neither can raise anything further in Body.
        for char in (brawler, scout):
            assert char.facet_level == 3
            for sid in body:
                assert char.skills[sid].rank == char.rank_ceiling_for(sid, ruleset)

        ranks = lambda c: {s: c.skills[s].rank for s in body}
        assert ranks(brawler) != ranks(scout)
        # The signature difference: each is Master where the other is Practiced.
        assert brawler.skills[body[1]].rank == "master"
        assert scout.skills[body[1]].rank == "practiced"

    def test_no_build_can_exceed_the_caps(self, ruleset, valid_attributes):
        """Spend far more marks than the shape can absorb; the caps still hold."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        _spend_marks(char, ruleset, body, 500)
        ranks = [char.skills[s].rank for s in body if s in char.skills]
        assert sum(1 for r in ranks if r in ("expert", "master")) <= 3
        assert sum(1 for r in ranks if r == "master") <= 1

    def test_career_ceiling_is_twenty_seven_advances(self, ruleset, valid_attributes):
        """9 advances × 3 Facets. The track ends; it does not run forever."""
        char = _new_character(ruleset, valid_attributes)
        facets = sorted({s.facet for s in ruleset.skills if s.status == "active"})
        for facet in facets:
            _spend_marks(char, ruleset, _active_skills(ruleset, facet), 500)
        assert char.career_advances == SHAPED_ADVANCES * len(facets) == 27
        assert char.total_facet_levels == 9


# ---------------------------------------------------------------------------
# 6. Session projections
# ---------------------------------------------------------------------------

def _sessions_to_shape(ruleset, efficiency: float) -> int:
    """Sessions for a dedicated character at `efficiency` primary-SP to finish
    their primary shape (Facet level 3 + first Major)."""
    marks_per_session = efficiency * ruleset.advancement.session_skill_points
    return math.ceil(SHAPED_MARKS / marks_per_session)


class TestSessionProjections:
    @pytest.mark.parametrize("efficiency,expected_session", [
        (1.0, 10),   # 38 marks / 4 SP = 9.5 → session 10
        (0.8, 12),
        (0.6, 16),
    ])
    def test_projection_matches_design_table(self, ruleset, efficiency, expected_session):
        assert _sessions_to_shape(ruleset, efficiency) == expected_session

    def test_engine_simulation_finishes_the_shape_on_session_ten(self, ruleset, valid_attributes):
        """Drive the real engine at 100% efficiency (4 primary marks/session)."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        sp = ruleset.advancement.session_skill_points
        milestone = None
        for session in range(1, 40):
            _spend_marks(char, ruleset, body, sp)
            if char.facet_level >= 3 and milestone is None:
                milestone = session
                break
        assert milestone == 10
        assert char.total_facet_levels == 3

    def test_first_technique_arrives_by_session_three(self, ruleset, valid_attributes):
        """Level 1 at 3 advances = 9 marks: the deliberate onboarding win."""
        char = _new_character(ruleset, valid_attributes)
        body = _active_skills(ruleset, "body")
        sp = ruleset.advancement.session_skill_points
        for session in range(1, 10):
            _spend_marks(char, ruleset, body, sp)
            if char.facet_level >= 1:
                assert session == 3   # 9 marks at 4/session
                return
        pytest.fail("Facet level 1 never reached")
