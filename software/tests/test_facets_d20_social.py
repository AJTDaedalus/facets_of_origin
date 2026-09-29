"""Facets d20 social rules (06 *Social Play*) — direct rule tests, and the chapter's tables
held to the engine (playtest fix pass, MM #6)."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from facets_d20 import social

CH06 = Path(__file__).resolve().parents[2] / "facets_d20" / "06_Backgrounds_Sparks_and_Social.md"


class TestStartingAttitude:
    def test_a_stranger_starts_neutral(self):
        assert social.starting_attitude() == "neutral"

    def test_someone_the_party_crossed_starts_wary(self):
        assert social.starting_attitude(crossed=True) == "wary"

    def test_both_are_on_the_track(self):
        assert {social.starting_attitude(), social.starting_attitude(crossed=True)} <= set(social.TRACK)


class TestResults:
    def test_meet_the_dc_is_one_step(self):
        assert social.result_steps(15, 15) == 1

    def test_beat_by_ten_is_two_steps(self):
        assert social.result_steps(25, 15) == 2
        assert social.result_steps(24, 15) == 1

    def test_miss_by_one_to_four_changes_nothing_and_spends_the_argument(self):
        assert social.result_steps(11, 15) == 0 and social.argument_spent(11, 15)
        assert not social.argument_spent(15, 15)

    def test_miss_by_five_is_a_step_back(self):
        assert social.result_steps(10, 15) == -1

    def test_silver_tongue_two_steps_from_five(self):
        assert social.result_steps(20, 15, silver_tongue=True) == 2

    def test_dc_ladder(self):
        assert [social.case_dc(k) for k in ("no_reason", "reasons", "good_reasons")] == [10, 15, 20]

    def test_unknown_difficulty_is_an_error(self):
        with pytest.raises(KeyError):
            social.case_dc("impossible")


class TestTrack:
    def test_move_clamps_at_the_ends(self):
        assert social.move("ally", 2) == "ally"
        assert social.move("hostile", -1) == "hostile"

    def test_move_steps(self):
        assert social.move("wary", 2) == "friendly"

    def test_unknown_attitude_is_an_error(self):
        with pytest.raises(KeyError):
            social.move("smitten", 1)


class TestLimits:
    def test_one_roll_per_character_per_person_per_scene(self):
        rolled = {("rogue", "clerk")}
        assert not social.may_roll("rogue", "clerk", rolled)
        assert social.may_roll("priest", "clerk", rolled)
        assert social.may_roll("rogue", "captain", rolled)

    def test_intimidation_fades_one_step_toward_hostile(self):
        assert social.after_threat("friendly") == "neutral"
        assert social.after_threat("hostile") == "hostile"

    def test_influence_in_a_fight_stops_a_foe_at_neutral(self):
        assert social.stops_fighting("neutral") and social.stops_fighting("ally")
        assert not social.stops_fighting("wary")

    def test_stops_fighting_rejects_unknown(self):
        with pytest.raises(KeyError):
            social.stops_fighting("confused")


class TestChapter06MatchesTheEngine:
    @pytest.fixture(scope="class")
    def text(self):
        return CH06.read_text(encoding="utf-8")

    def test_attitude_table_lists_the_track_in_order(self, text):
        block = text.split("**Table 6–2")[1].split("\n\n")[1]
        names = re.findall(r"^\| \*\*(\w+)\*\*", block, re.M)
        assert [n.lower() for n in names] == list(social.TRACK)

    def test_dcs_printed(self, text):
        for dc in social.DCS.values():
            assert f"**{dc}**" in text

    def test_results_table_thresholds(self, text):
        block = text.split("**Table 6–3")[1]
        assert "Beat the DC by 10 or more" in block and "Miss by 1 to 4" in block \
            and "Miss by 5 or more" in block

    def test_defaults_and_limits_are_stated(self, text):
        assert "starts **Neutral**" in text and "**Wary**" in text
        assert "one roll per character per person per scene" in text.lower()
        assert "Intimidation" in text and "toward Hostile" in text
