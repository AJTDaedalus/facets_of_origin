"""The two peak-moment mechanics (docs/RESEARCH_fun_gap_analysis.md items 1-2).

Written before the implementation.

  1. **Natural 12** — both kept dice showing 6. Always at least a full success
     regardless of modifiers, and flagged so the table knows something happened.
     Deliberately keyed to the *dice*, not the total: a total-based tier would
     scale with competence and stop being rare.
  2. **Natural 2** — both kept dice showing 1. Does NOT override the tier
     downward; it only auto-confirms the Graceful Fail when the roll was a
     failure anyway. Overriding upward rewards, overriding downward would punish
     competence — the exact d20 flaw `research/dice_system_analysis.md` cites.
  3. **Borrowed Trouble** — accept a complication for one extra die, dropped
     lowest, exactly as a Spark. Costs no Spark, and the complication lands
     whatever the dice say.
"""
import pytest

from app.game.engine import RollRequest, resolve_roll, _roll_and_resolve


# ---------------------------------------------------------------------------
# Helpers — force the dice rather than fishing for them
# ---------------------------------------------------------------------------

def _forced(monkeypatch, values: list[int]) -> None:
    """Make random.randint return `values` in order."""
    seq = iter(values)
    monkeypatch.setattr("app.game.engine.random.randint", lambda a, b: next(seq))


def _roll(ruleset, monkeypatch, dice, *, difficulty="Standard", rating=2,
          skill=None, rank=None, sparks=0, borrowed_trouble=False):
    _forced(monkeypatch, dice)
    return resolve_roll(
        RollRequest(
            attribute_id="strength", attribute_rating=rating,
            skill_id=skill, skill_rank_id=rank,
            difficulty_label=difficulty, sparks_spent=sparks,
            borrowed_trouble=borrowed_trouble,
        ),
        ruleset,
    )


# ---------------------------------------------------------------------------
# 1. Natural 12
# ---------------------------------------------------------------------------

class TestNaturalTwelve:
    def test_boxcars_is_flagged_critical(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [6, 6])
        assert result.critical is True
        assert result.outcome == "full_success"

    def test_ordinary_ten_is_not_critical(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [6, 4])
        assert result.total == 10
        assert result.outcome == "full_success"
        assert result.critical is False

    def test_natural_twelve_beats_a_crushing_penalty(self, ruleset, monkeypatch):
        """12 - 2 (Very Hard) - 1 (Weak attribute) = 9, a partial by the table.
        The dice override it: two sixes is a full success whatever the modifiers
        say. This is the underdog moment the crit exists to create."""
        result = _roll(ruleset, monkeypatch, [6, 6], difficulty="Very Hard", rating=1)
        assert result.total == 9
        assert result.critical is True
        assert result.outcome == "full_success"

    def test_a_twelve_total_from_ordinary_dice_is_not_critical(self, ruleset, monkeypatch):
        """Keyed to the dice, not the total — otherwise competence inflates it."""
        result = _roll(ruleset, monkeypatch, [5, 4], rating=3, skill="combat", rank="master")
        assert result.total >= 12
        assert result.critical is False

    def test_spark_kept_dice_decide_it_not_the_dropped_one(self, ruleset, monkeypatch):
        """3d6 drop lowest: the two KEPT dice must both be 6."""
        crit = _roll(ruleset, monkeypatch, [6, 6, 1], sparks=1)
        assert crit.dice_kept == [6, 6]
        assert crit.critical is True

        # The dropped die is irrelevant: a 5 dropped still leaves two sixes.
        dropped_high = _roll(ruleset, monkeypatch, [6, 5, 6], sparks=1)
        assert dropped_high.dice_kept == [6, 6]
        assert dropped_high.critical is True

        not_crit = _roll(ruleset, monkeypatch, [6, 5, 5], sparks=1)
        assert not_crit.dice_kept == [5, 6]
        assert not_crit.critical is False

    def test_press_also_feeds_the_crit(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [6, 6, 2])
        # press adds a die through the same path as a Spark
        _forced(monkeypatch, [6, 6, 2])
        pressed = resolve_roll(
            RollRequest(attribute_id="strength", attribute_rating=2,
                        skill_id=None, skill_rank_id=None,
                        difficulty_label="Standard", press=True),
            ruleset,
        )
        assert pressed.dice_kept == [6, 6]
        assert pressed.critical is True


# ---------------------------------------------------------------------------
# 2. Natural 2 — no downward override
# ---------------------------------------------------------------------------

class TestNaturalTwo:
    def test_snake_eyes_is_flagged(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [1, 1])
        assert result.fumble is True
        assert result.outcome == "failure"

    def test_snake_eyes_does_not_override_a_partial_success(self, ruleset, monkeypatch):
        """2 + 1 (Strong) + 3 (Master) + 1 (Easy) = 7 — a partial success.
        The natural 2 is flagged, but it does NOT drag the tier down: that would
        punish competence, which is the d20 failure mode we rejected."""
        result = _roll(ruleset, monkeypatch, [1, 1], difficulty="Easy",
                       rating=3, skill="combat", rank="master")
        assert result.total == 7
        assert result.fumble is True
        assert result.outcome == "partial_success"

    def test_ordinary_failure_is_not_a_fumble(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [2, 3])
        assert result.outcome == "failure"
        assert result.fumble is False

    def test_a_spark_all_but_eliminates_the_fumble(self, ruleset, monkeypatch):
        """With 3d6 drop lowest, both kept dice show 1 only if all three do."""
        saved = _roll(ruleset, monkeypatch, [1, 1, 3], sparks=1)
        assert saved.dice_kept == [1, 3]
        assert saved.fumble is False

        still = _roll(ruleset, monkeypatch, [1, 1, 1], sparks=1)
        assert still.dice_kept == [1, 1]
        assert still.fumble is True

    def test_critical_and_fumble_are_mutually_exclusive(self, ruleset, monkeypatch):
        for dice in ([6, 6], [1, 1], [3, 4]):
            result = _roll(ruleset, monkeypatch, list(dice))
            assert not (result.critical and result.fumble)


# ---------------------------------------------------------------------------
# 3. Borrowed Trouble
# ---------------------------------------------------------------------------

class TestBorrowedTrouble:
    def test_it_adds_one_die_and_drops_the_lowest(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [2, 5, 4], borrowed_trouble=True)
        assert len(result.dice_rolled) == 3
        assert result.dice_kept == [4, 5]

    def test_it_costs_no_spark(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [2, 5, 4], borrowed_trouble=True)
        assert result.sparks_spent == 0
        assert result.borrowed_trouble is True

    def test_it_stacks_with_a_spark(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [1, 2, 5, 6], sparks=1, borrowed_trouble=True)
        assert len(result.dice_rolled) == 4
        assert result.dice_kept == [5, 6]

    def test_it_stacks_with_press(self, ruleset, monkeypatch):
        _forced(monkeypatch, [1, 2, 5, 6])
        result = resolve_roll(
            RollRequest(attribute_id="strength", attribute_rating=2,
                        skill_id=None, skill_rank_id=None,
                        difficulty_label="Standard", press=True,
                        borrowed_trouble=True),
            ruleset,
        )
        assert len(result.dice_rolled) == 4
        assert result.dice_kept == [5, 6]

    def test_declining_it_changes_nothing(self, ruleset, monkeypatch):
        result = _roll(ruleset, monkeypatch, [3, 4], borrowed_trouble=False)
        assert len(result.dice_rolled) == 2
        assert result.borrowed_trouble is False

    def test_it_can_reach_a_critical(self, ruleset, monkeypatch):
        """The bargain buys a real shot at the peak, not just at success."""
        result = _roll(ruleset, monkeypatch, [1, 6, 6], borrowed_trouble=True)
        assert result.dice_kept == [6, 6]
        assert result.critical is True


# ---------------------------------------------------------------------------
# 4. The ruleset states all of it — no engine literals
# ---------------------------------------------------------------------------

class TestRulesetDrivesTheMechanics:
    def test_critical_rule_is_in_the_ruleset(self, ruleset):
        rr = ruleset.roll_resolution
        assert rr.critical is not None
        assert rr.critical.natural == "high"      # all kept dice at max face
        assert rr.critical.min_outcome == "full_success"

    def test_fumble_rule_is_in_the_ruleset_and_does_not_override(self, ruleset):
        rr = ruleset.roll_resolution
        assert rr.fumble is not None
        assert rr.fumble.natural == "low"
        assert rr.fumble.max_outcome is None      # never drags a tier down

    def test_borrowed_trouble_is_in_the_ruleset(self, ruleset):
        bt = ruleset.roll_resolution.borrowed_trouble
        assert bt is not None
        assert bt.extra_dice == 1
        assert bt.spark_cost == 0
