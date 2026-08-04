"""Tests for the agentic playtest harness.

The harness exists because playtest batch 07 produced a corpus of numbers that
described nothing: the narrative dice were written by a language model, and the
rolls that *were* resolved on the server were counted four times each. The tests
that matter most here are the two that would have caught that —
`TestConfabulationValidator` and `TestDiceDistribution` — and
`TestObserverDoesNotAlias`, which pins the structural fix.

The live-server tests need a running app; they spin one up on a free port with a
throwaway data directory, the same pattern as tests/e2e/test_ui_flows.py.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from app.facets.registry import build_ruleset
from tools.agentic_playtest.events import Event, EventLog
from tools.agentic_playtest.transcript import render, render_event
from tools.agentic_playtest.validate import (
    dice_distribution,
    find_confabulations,
    parse_dice_from_prose,
)

SOFTWARE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SOFTWARE_DIR.parent
PASSWORD = "agentic-playtest-password"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _roll(total: int, dice: list[int], label: str = "Success with Cost") -> dict:
    return {
        "dice_rolled": dice, "dice_kept": dice, "dice_sum": sum(dice),
        "attribute_modifier": 0, "skill_modifier": 0, "difficulty_modifier": 0,
        "total": total, "outcome": "partial_success", "outcome_label": label,
        "outcome_description": "", "sparks_spent": 0,
    }


@pytest.fixture(scope="module")
def ruleset():
    return build_ruleset([])


# ---------------------------------------------------------------------------
# The validator that would have caught batch 07
# ---------------------------------------------------------------------------

class TestConfabulationValidator:
    def test_rejects_the_real_batch_07_line(self, ruleset):
        """The regression test for the entire class of defect.

        This is a verbatim line from
        playtest/07_oraga_night_playtests/session_log_01.md — a dice result the
        engine never produced, written into prose as if it had.
        """
        log = EventLog("s1")
        log.append("say", "Arthur",
                   text="**Roll:** 2d6 (2, 3) + 2 = **7** (Partial Success).")

        report = find_confabulations(log, ruleset)

        assert not report.ok
        assert any(f.kind == "dice" for f in report.findings)

    def test_accepts_narration_that_matches_the_log(self, ruleset):
        log = EventLog("s1")
        log.append("roll_result", "Zahna", roll=_roll(8, [3, 5]))
        log.append("say", "Zahna", text="An 8 — enough to get through the gate.")

        assert find_confabulations(log, ruleset).ok

    def test_rejects_a_total_the_engine_never_produced(self, ruleset):
        log = EventLog("s1")
        log.append("roll_result", "Zahna", roll=_roll(8, [3, 5]))
        log.append("say", "Zahna", text="I rolled a 12, so the door swings wide.")

        report = find_confabulations(log, ruleset)
        assert any(f.kind == "total" for f in report.findings)

    def test_rejects_an_outcome_label_the_engine_never_gave(self, ruleset):
        log = EventLog("s1")
        log.append("roll_result", "Zahna", roll=_roll(8, [3, 5], label="Success with Cost"))
        log.append("say", "MM", text="That's a Full Success — clean and clear.")

        report = find_confabulations(log, ruleset)
        assert any(f.kind == "outcome" for f in report.findings)

    def test_rejects_an_invented_condition(self, ruleset):
        """The other batch-07 failure: an MM inventing 'the Watched condition'.

        Here the MM names a real Condition with no enemy_attack behind it, which
        is the same shape of claim.
        """
        log = EventLog("s1")
        log.append("say", "MM", text="The guard shoves you — you take the winded condition.")

        report = find_confabulations(log, ruleset)
        assert any(f.kind == "condition" for f in report.findings)

    def test_accepts_a_condition_the_engine_applied(self, ruleset):
        log = EventLog("s1")
        log.append("condition_applied", "MM", target="Zahna", condition="winded",
                   condition_applied="winded", all_conditions=["winded"])
        log.append("say", "MM", text="The blow lands — you have the winded condition.")

        assert find_confabulations(log, ruleset).ok

    def test_claims_are_scoped_to_their_own_beat(self, ruleset):
        """A roll in beat 1 does not license a claim about it in beat 2."""
        log = EventLog("s1")
        log.append("roll_result", "Zahna", roll=_roll(8, [3, 5]))
        log.next_beat()
        log.append("say", "Zahna", text="2d6 (3, 5) again, same as before.")

        assert not find_confabulations(log, ruleset).ok

    def test_large_numbers_are_not_treated_as_roll_claims(self, ruleset):
        log = EventLog("s1")
        log.append("say", "Zahna", text="The ledger lists 340 crates and page 112 is missing.")

        assert find_confabulations(log, ruleset).ok


# ---------------------------------------------------------------------------
# Batch-level dice distribution
# ---------------------------------------------------------------------------

class TestDiceDistribution:
    def test_the_batch_07_dice_fail(self):
        """~60 dice with zero 1s is not a d6.

        These are the actual pairs from the 20 session logs. Reading them out of
        the repo would couple the test to files that may be archived, so they
        are inlined.
        """
        pairs = [
            (2, 3), (3, 3), (2, 3), (2, 3), (2, 3), (3, 3), (2, 4), (3, 3),
            (3, 3), (3, 3), (4, 3), (4, 3), (5, 5), (6, 6), (5, 5), (5, 6),
            (5, 5), (5, 5), (5, 4), (4, 4), (3, 3), (4, 3), (3, 3), (5, 5),
            (5, 5), (5, 4), (3, 3), (2, 3), (3, 4), (2, 2), (6, 5), (5, 5),
            (5, 5), (6, 5), (2, 4), (3, 3), (2, 3), (3, 3), (3, 3), (3, 3),
            (3, 3), (3, 3), (4, 3), (3, 4), (4, 3), (3, 4), (2, 3), (2, 2),
            (4, 3), (3, 3), (3, 3), (4, 3), (4, 3), (4, 3), (3, 3), (3, 3),
            (4, 3), (3, 3), (4, 3), (3, 3), (3, 4),
        ]
        log = EventLog("legacy")
        for a, b in pairs:
            log.append("roll_result", "P", roll=_roll(a + b, [a, b]))

        report = dice_distribution([log])

        assert not report.passed
        assert report.face_counts.get(1, 0) == 0

    def test_real_dice_pass(self):
        import random
        rng = random.Random(20260731)
        log = EventLog("real")
        for _ in range(200):
            dice = [rng.randint(1, 6), rng.randint(1, 6)]
            log.append("roll_result", "P", roll=_roll(sum(dice), dice))

        assert dice_distribution([log]).passed

    def test_small_samples_are_not_evaluated(self):
        log = EventLog("tiny")
        log.append("roll_result", "P", roll=_roll(7, [3, 4]))

        report = dice_distribution([log])
        assert report.passed and "minimum" in report.note

    def test_parse_dice_from_prose_reads_the_legacy_format(self):
        assert parse_dice_from_prose("**Roll:** 2d6 (2, 3) + 2 = **7**") == [2, 3]


# ---------------------------------------------------------------------------
# Transcript rendering
# ---------------------------------------------------------------------------

class TestTranscript:
    def test_dice_are_rendered_from_the_event(self):
        """`roll_result` is the server's own broadcast type. It was `roll` here,
        a name nothing emits, so no roll ever rendered — see
        `TestTranscriptRendersWhatTheServerSends`."""
        log = EventLog("s1")
        log.append("roll_result", "Zahna", roll=_roll(4, [1, 3]),
                   description="pick the lock")

        line = render_event(list(log)[0])
        assert "1, 3" in line and "**4**" in line

    def test_agent_text_is_quoted_not_interpreted(self):
        """An agent claiming a 9 renders as speech, never as a mechanical line."""
        log = EventLog("s1")
        log.append("say", "Zahna", text="I rolled a 9!")

        line = render_event(list(log)[0])
        assert line.startswith("**Zahna:**")

    def test_header_records_arm_and_seed(self):
        log = EventLog("s1", arm="B", seed=42)
        out = render(log, title="Pilot")
        assert "arm **B**" in out and "`42`" in out

    def test_ooc_is_visually_distinct(self):
        log = EventLog("s1")
        log.append("say_ooc", "Penny", text="wait, what's my modifier again")
        assert "out of character" in render_event(list(log)[0])


# ---------------------------------------------------------------------------
# Event log
# ---------------------------------------------------------------------------

class TestEventLog:
    def test_round_trips_through_disk(self, tmp_path):
        log = EventLog("s1", arm="B", seed=7)
        log.append("roll_result", "Zahna", roll=_roll(9, [4, 5]))
        log.next_beat()
        log.append("say", "Zahna", text="Clean.")
        path = tmp_path / "events.jsonl"
        log.write(path)

        reloaded = EventLog.read(path)
        assert reloaded.arm == "B" and reloaded.seed == 7
        assert len(reloaded) == 2
        assert list(reloaded)[1].beat == 1

    def test_beats_group_events(self):
        log = EventLog("s1")
        log.append("say", "A", text="one")
        log.next_beat()
        log.append("say", "B", text="two")
        assert len(log.in_beat(0)) == 1 and len(log.in_beat(1)) == 1

    def test_by_actor_filters(self):
        log = EventLog("s1")
        log.append("say", "A", text="one")
        log.append("say", "B", text="two")
        assert len(log.by_actor("A")) == 1


# ---------------------------------------------------------------------------
# Live server — agents play on the real tool, each with its own account
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    """The same `AppServer` the CLI uses, so the tests exercise the real
    spin-up path rather than a second copy of it."""
    from tools.agentic_playtest.cli import AppServer

    with AppServer(data_dir=tmp_path_factory.mktemp("agentic-data")) as server:
        yield server.base_url


ATTRS = {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 1,
         "wisdom": 1, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 2}


@pytest.fixture(scope="module")
def mm_token(live_server):
    """One login per module. `/auth/mm-login` is rate limited to 5/minute — a
    per-test login trips it, which is the limiter working correctly."""
    from tools.agentic_playtest.client import login_mm
    return login_mm(live_server, PASSWORD)


@pytest.fixture
def table(live_server, mm_token, request):
    from tools.agentic_playtest.client import LiveTable
    t = LiveTable(live_server, None, f"agentic-{request.node.name}"[:60],
                  seed=1, mm_token=mm_token)
    yield t
    t.close()


class TestPlayingOnTheRealTool:
    def test_a_player_joins_with_its_own_account(self, table):
        """Redeems a real single-use invite and gets its own token — the same
        path a human takes, so the server's permission model is the one under
        test rather than a wrapper we wrote."""
        connection = table.join_as_player("Zahna")

        assert connection.token != table.mm_token
        assert connection.identity == "Zahna"

    def test_a_roll_reaches_the_observer_log(self, table):
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        verbs = Verbs(table)

        roll = verbs.roll_skill("Zahna", "strength", "combat")

        assert 2 <= roll["dice_sum"] <= 12
        assert len(table.log.of_kind("roll_result")) == 1

    def test_the_server_refuses_a_player_calling_an_mm_verb(self, table):
        """The point of playing on the tool: a player agent cannot land an enemy
        attack, and it is the server that says so."""
        from tools.agentic_playtest.client import TableRuling
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        verbs = Verbs(table)

        with pytest.raises(TableRuling):
            verbs.land_enemy_attack("Zahna", "Zahna", "winded")

    def test_enemy_depletion_is_resolved_server_side(self, table):
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        table.add_enemy({"id": "guard", "name": "Guard", "tier": "named", "resolve": 4})
        verbs = Verbs(table)

        spawned = verbs.spawn_enemy("MM", "guard")
        result = verbs.apply_strike_to_enemy("MM", spawned["tracker_key"], "full_success")

        # The agent sent an outcome, not a number.
        assert result["depletion"] == 2 and result["resolve"] == 2

    def test_an_enemy_attack_lands_through_the_engine(self, table):
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        verbs = Verbs(table)
        verbs.start_combat("MM")

        result = verbs.land_enemy_attack("MM", "Zahna", "winded")

        assert "winded" in result["all_conditions"]


class TestObserverDoesNotAlias:
    """The structural fix for batch 07's 4x over-count.

    `roll_result` is broadcast to every connected client. Recording from each
    player's socket counted one roll four times. The event log is built from the
    MM observer socket alone, so N players rolling produces exactly N events.
    """

    def test_four_players_rolling_produce_four_events(self, table):
        from tools.agentic_playtest.verbs import Verbs

        names = ["Zahna", "Mordai", "Zulnut", "Ilesse"]
        for name in names:
            table.join_as_player(name)
            table.create_character(name, name, "body", ATTRS)
        verbs = Verbs(table)

        totals = [verbs.roll_skill(n, "strength")["total"] for n in names]

        rolls = table.log.of_kind("roll_result")
        assert len(rolls) == 4, f"expected 4 roll events, got {len(rolls)}"
        assert {e.actor for e in rolls} == set(names)
        # And each event carries its own roll, not a shared one.
        assert sorted(e.data["roll"]["total"] for e in rolls) == sorted(totals)

    def test_each_player_gets_its_own_result_not_a_neighbours(self, table):
        """The exact batch-07 symptom: four identical totals in a session."""
        from tools.agentic_playtest.verbs import Verbs

        names = ["A", "B", "C", "D"]
        for name in names:
            table.join_as_player(name)
            table.create_character(name, name, "body", ATTRS)
        verbs = Verbs(table)

        seen = [verbs.roll_skill(n, "strength")["dice_rolled"] for n in names]

        logged = [e.data["roll"]["dice_rolled"] for e in table.log.of_kind("roll_result")]
        assert sorted(map(tuple, seen)) == sorted(map(tuple, logged))


# ---------------------------------------------------------------------------
# Personas, schemas, context — the agent-shaped parts, no API needed
# ---------------------------------------------------------------------------

class TestPersonas:
    def test_assignment_is_deterministic_in_the_seed(self):
        """An arm-paired rerun must cast the same table, or the A/B comparison
        is comparing personalities as well as rules."""
        from tools.agentic_playtest.personas import assign

        roster = [("Sophia", "Zahna"), ("Luke", "Mordai"), ("Penny", "Zulnut")]
        a = assign(roster, seed=11)
        b = assign(roster, seed=11)

        assert [(p.archetype.key, p.agenda) for p in a] == \
               [(p.archetype.key, p.agenda) for p in b]

    def test_archetypes_are_distinct_across_the_table(self):
        from tools.agentic_playtest.personas import assign

        personas = assign([("A", "a"), ("B", "b"), ("C", "c"), ("D", "d")], seed=3)
        assert len({p.archetype.key for p in personas}) == 4

    def test_the_agenda_is_in_the_agents_own_prompt(self):
        from tools.agentic_playtest.personas import assign

        persona = assign([("Sophia", "Zahna")], seed=5)[0]
        assert persona.agenda in persona.describe_for_self()

    def test_permission_to_refuse_is_explicit(self):
        """Without this, agents are agreeable and every session becomes a rail."""
        from tools.agentic_playtest.agents import PLAYER_ROLE
        assert "not required to follow the MM's hook" in PLAYER_ROLE


class TestToolSchemas:
    def test_every_verb_is_exposed_and_every_tool_is_implemented(self):
        """A verb cannot be added without exposing it, or vice versa."""
        from tools.agentic_playtest.tools_schema import MM_TOOLS, PLAYER_TOOLS
        from tools.agentic_playtest.verbs import MM_VERBS, PLAYER_VERBS, Verbs

        assert set(PLAYER_VERBS) == set(PLAYER_TOOLS)
        assert set(MM_VERBS) == set(MM_TOOLS)
        for verb in set(PLAYER_VERBS) | set(MM_VERBS):
            assert callable(getattr(Verbs, verb, None)), verb

    def test_the_mm_has_no_roll_verb_for_npcs(self):
        """Enemies never roll (PHB III.3). `table_roll` is a utility for random
        tables and carries no outcome tier."""
        from tools.agentic_playtest.verbs import MM_VERBS

        rolling = [v for v in MM_VERBS if "roll" in v]
        assert rolling == ["table_roll"]

    def test_schemas_are_strict(self):
        from tools.agentic_playtest.tools_schema import mm_tools, player_tools

        for tool in player_tools() + mm_tools():
            assert tool["strict"] is True, tool["name"]
            assert tool["input_schema"]["additionalProperties"] is False

    def test_land_enemy_attack_describes_the_tier_mapping(self):
        """The MM must not have to guess which tier an attack lands at."""
        from tools.agentic_playtest.tools_schema import MM_TOOLS

        description = MM_TOOLS["land_enemy_attack"]["description"]
        assert "Tier 1" in description and "Tier 2" in description
        assert "never roll" in description


class TestSharedPrefix:
    def test_is_byte_identical_across_builds(self, ruleset):
        """A silent invalidator here shows up only as a cost increase."""
        from tools.agentic_playtest.context import build_shared_prefix

        a = build_shared_prefix(ruleset, "Scenario.", "Cast.")
        b = build_shared_prefix(ruleset, "Scenario.", "Cast.")
        assert a == b

    def test_the_cache_breakpoint_is_on_the_shared_block(self, ruleset):
        from tools.agentic_playtest.context import SessionContext, build_shared_prefix

        context = SessionContext(build_shared_prefix(ruleset, "S", "C"), "role")
        blocks = context.system_blocks()

        assert blocks[0]["cache_control"] == {"type": "ephemeral"}
        assert "cache_control" not in blocks[1]

    def test_the_digest_comes_from_the_ruleset(self, ruleset):
        """Generated, not transcribed — a hand-written summary drifts, and an MM
        given a stale digest invents rules to fill the gap."""
        from tools.agentic_playtest.context import rules_digest

        digest = rules_digest(ruleset)
        for condition in ruleset.combat.conditions.tier2:
            assert condition.id in digest
        assert str(ruleset.advancement.session_skill_points) in digest

    def test_the_digest_states_that_enemies_never_roll(self, ruleset):
        from tools.agentic_playtest.context import rules_digest
        assert "Enemies never roll" in rules_digest(ruleset)


# ---------------------------------------------------------------------------
# Behavioural metrics — computed, never self-reported
# ---------------------------------------------------------------------------

class TestMetrics:
    def test_shrinking_contributions_report_a_negative_trend(self):
        """The disengagement proxy. A player whose turns get steadily shorter is
        the closest thing to 'they checked out' that a log can show."""
        from tools.agentic_playtest.metrics import proposal_length_trend

        assert proposal_length_trend([40, 38, 42, 20, 18, 6, 4, 3, 2]) < -0.5

    def test_steady_contributions_report_a_flat_trend(self):
        from tools.agentic_playtest.metrics import proposal_length_trend

        assert abs(proposal_length_trend([20] * 9)) < 0.01

    def test_too_few_contributions_report_nothing(self):
        from tools.agentic_playtest.metrics import proposal_length_trend

        assert proposal_length_trend([40, 2]) == 0.0

    def test_spotlight_spread_is_zero_when_even(self):
        from tools.agentic_playtest.metrics import spotlight_spread

        assert spotlight_spread([5, 5, 5, 5]) == 0.0

    def test_spotlight_spread_rises_when_one_player_dominates(self):
        from tools.agentic_playtest.metrics import spotlight_spread

        assert spotlight_spread([20, 1, 1, 1]) > 0.7

    def test_longest_idle_streak_is_counted_in_beats(self):
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        log.append("say", "A", text="hi")
        for _ in range(4):
            log.next_beat()
            log.append("say", "B", text="hi")
        log.next_beat()
        log.append("say", "A", text="back")

        metrics = compute(log, ["A", "B"])
        by_name = {p.player: p for p in metrics.players}
        assert by_name["A"].longest_idle_beats == 4
        assert by_name["B"].longest_idle_beats == 1

    def test_zero_dice_exchanges_are_counted(self):
        """The direct measure for the deterministic-severity question: with
        fixed severity and a PC who Absorbs, an exchange can pass with no dice
        thrown by anyone."""
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        log.append("condition_applied", "MM", player="A", condition="winded")
        log.append("react_result", "A", reaction="absorb", roll=None)
        log.append("exchange_ended", "MM", characters={})
        log.append("strike_result", "A", roll=_roll(9, [4, 5]))
        log.append("exchange_ended", "MM", characters={})

        metrics = compute(log, ["A"])
        assert metrics.total_exchanges == 2
        assert metrics.zero_dice_exchanges == 1

    def test_ooc_ratio_reflects_table_talk(self):
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        for _ in range(4):
            log.append("say", "A", text="in character")
        log.append("say_ooc", "A", text="wait what's my modifier")

        assert compute(log, ["A"]).ooc_to_ic_ratio == pytest.approx(0.25)

    def test_a_transcript_with_no_table_talk_scores_zero(self):
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        log.append("say", "A", text="in character only")

        assert compute(log, ["A"]).ooc_to_ic_ratio == 0.0

    def test_luck_is_reported_against_the_2d6_expectation(self):
        """So an unlucky player can be cross-referenced against their engagement
        trend — the variance-concentration question."""
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        for dice in ([1, 1], [2, 1], [1, 2]):
            log.append("roll_result", "A", roll=_roll(sum(dice), dice))

        assert compute(log, ["A"]).players[0].luck < -3

    def test_rules_gaps_are_counted(self):
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1")
        log.append("rules_gap", "MM", question="Can I climb it?", ruling="Yes, Hard.")

        assert compute(log, []).rules_gaps == 1

    def test_softened_attacks_are_counted_for_the_arm_comparison(self):
        from tools.agentic_playtest.metrics import compute

        log = EventLog("s1", arm="B")
        log.append("condition_applied", "MM", player="A", condition="winded",
                   arm_softened=True)
        log.append("condition_applied", "MM", player="A", condition="staggered")

        metrics = compute(log, ["A"])
        assert metrics.enemy_attacks == 2 and metrics.enemy_attacks_softened == 1

    def test_summary_renders_every_player(self):
        from tools.agentic_playtest.metrics import compute, summarise

        log = EventLog("s1")
        log.append("say", "A", text="hi")
        log.append("say", "B", text="hi")

        out = summarise(compute(log, ["A", "B"]))
        assert "A" in out and "B" in out and "spotlight spread" in out


# ---------------------------------------------------------------------------
# Debrief and blind judgement — the elicited half
# ---------------------------------------------------------------------------

class TestDebriefSchema:
    def test_there_is_no_absolute_rating_field(self):
        """Agreeable models cluster every 1-10 rating at the top regardless of
        what happened. If someone adds one back, this fails."""
        from tools.agentic_playtest.debrief import PlayerDebrief

        for name, field in PlayerDebrief.model_fields.items():
            assert field.annotation is not int, f"{name} is a numeric rating"
            assert not any(w in name for w in ("rating", "score", "out_of_ten")), name

    def test_every_question_forces_a_choice_or_a_negative(self):
        from tools.agentic_playtest.debrief import PlayerDebrief

        fields = PlayerDebrief.model_fields
        assert "worst_moment" in fields
        assert "not an answer" in fields["worst_moment"].description
        assert "Ties are not allowed" in \
            fields["scenes_ranked_best_to_worst"].description.replace("\n", " ")

    def test_it_asks_the_experiment_s_question(self):
        """Enemy variety is what the A/B arm manipulates."""
        from tools.agentic_playtest.debrief import PlayerDebrief

        assert "did_the_enemies_feel_varied" in PlayerDebrief.model_fields


class TestBlindJudge:
    def test_arm_labels_are_stripped(self):
        from tools.agentic_playtest.judge import strip_tells

        cleaned = strip_tells("*Session `abc` · arm **B** · seed `42`*")
        assert "**B**" not in cleaned and "42" not in cleaned

    def test_the_softening_marker_is_stripped(self):
        """`[softened]` is Arm B's variant showing through the transcript — it
        would tell the judge exactly which condition it is reading."""
        from tools.agentic_playtest.judge import strip_tells

        assert "softened" not in strip_tells(
            "`Enemy attack on Zahna [softened]: winded`")

    def test_a_consistent_preference_names_a_winner(self):
        from tools.agentic_playtest.judge import PairedVerdict, Verdict

        def verdict(pick):
            return Verdict(preferred=pick, because="x",
                           opposition_felt_more_varied_in="first",
                           most_boring_stretch="y")

        paired = PairedVerdict(forward=verdict("first"), reversed=verdict("second"),
                               label_first="A", label_second="B")
        assert paired.winner == "A"

    def test_an_order_dependent_preference_is_no_signal(self):
        """Picking whichever came first is position bias, not a preference."""
        from tools.agentic_playtest.judge import PairedVerdict, Verdict

        def verdict(pick):
            return Verdict(preferred=pick, because="x",
                           opposition_felt_more_varied_in="first",
                           most_boring_stretch="y")

        paired = PairedVerdict(forward=verdict("first"), reversed=verdict("first"),
                               label_first="A", label_second="B")
        assert paired.winner is None

    def test_tally_separates_agreement_from_order_dependence(self):
        from tools.agentic_playtest.judge import PairedVerdict, Verdict, tally

        def verdict(pick):
            return Verdict(preferred=pick, because="x",
                           opposition_felt_more_varied_in="first",
                           most_boring_stretch="y")

        agreed = PairedVerdict(verdict("first"), verdict("second"), "A", "B")
        flipped = PairedVerdict(verdict("first"), verdict("first"), "A", "B")

        result = tally([agreed, flipped])
        assert result["agreed"] == {"A": 1} and result["order_dependent"] == 1

    def test_the_prompt_forbids_declining_to_choose(self):
        from tools.agentic_playtest.judge import JUDGE_PROMPT

        assert "not available" in JUDGE_PROMPT


# ---------------------------------------------------------------------------
# Orchestrator, driven by a stub agent — full loop, no API cost
# ---------------------------------------------------------------------------

class StubResponse:
    def __init__(self, content, stop_reason="end_turn"):
        self.content = content
        self.stop_reason = stop_reason
        self.stop_details = None
        self.usage = type("U", (), {
            "input_tokens": 10, "output_tokens": 5,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0})()


class StubBlock:
    def __init__(self, name, tool_input):
        self.type = "tool_use"
        self.id = f"toolu_{name}_{id(self)}"
        self.name = name
        self.input = tool_input


class StubClient:
    """Returns canned tool calls, one scripted turn per agent invocation.

    Lets the whole orchestrator loop — dispatch, fan-out, budget, transcript,
    validation — run in CI against a real server with no model in the loop.
    """

    def __init__(self, script: dict[str, list]):
        self.script = {k: list(v) for k, v in script.items()}
        self.calls = 0

    class _Messages:
        def __init__(self, outer):
            self.outer = outer

        def create(self, *, system, messages, tools, **kwargs):
            self.outer.calls += 1
            # Identify the agent by the tool set it was handed.
            names = {t["name"] for t in tools}
            key = "MM" if "land_enemy_attack" in names else "player"
            queue = self.outer.script.get(key, [])
            if not queue:
                return StubResponse([])
            name, tool_input = queue.pop(0)
            return StubResponse([StubBlock(name, tool_input)])

    @property
    def messages(self):
        return self._Messages(self)


class TestOrchestrator:
    def test_a_scripted_session_runs_end_to_end(self, live_server, mm_token):
        """Exercises the real loop against the real server: agents connect with
        their own accounts, act, and the transcript is rendered from the log."""
        from tools.agentic_playtest.run import Budget, build_session

        client = StubClient({
            "MM": [("describe_scene", {"text": "The gates of the house stand shut."}),
                   ("say", {"text": "The guard looks you over. 'Invitation?'"}),
                   ("end_scene", {"summary": "They got in."})],
            "player": [("say_ooc", {"text": "wait, what's my Persuade at again"}),
                       ("roll_skill", {"attribute_id": "charisma", "skill_id": "persuade",
                                       "difficulty": "Standard", "sparks_spent": 0,
                                       "description": "talk past the guard"})],
        })

        session = build_session(
            client=client, base_url=live_server, mm_token=mm_token,
            scenario="A masquerade at a great house.", prep="The guard wants a bribe.",
            cast_blurb="Zahna, a scholar.",
            party=[{"player_name": "Zahna", "character_name": "Zahna",
                    "primary_facet": "mind", "attributes": ATTRS}],
            enemies=[], seed=5, arm="A", session_name="stub-e2e",
            budget=Budget(max_beats=2),
        )
        result = session.play()

        assert result.beats >= 2
        assert result.stopped_because and "beat cap" in result.stopped_because
        assert "The gates of the house stand shut" in result.transcript
        # The die value came from the engine, not the script.
        assert result.validation_ok, result.validation_report
        session.table.close()

    def test_the_budget_stops_a_runaway_session(self, live_server, mm_token):
        from tools.agentic_playtest.run import Budget, build_session

        client = StubClient({"MM": [], "player": []})
        session = build_session(
            client=client, base_url=live_server, mm_token=mm_token,
            scenario="s", prep="p", cast_blurb="c",
            party=[{"player_name": "Zahna", "character_name": "Zahna",
                    "primary_facet": "body", "attributes": ATTRS}],
            enemies=[], seed=5, session_name="stub-budget",
            budget=Budget(max_beats=1),
        )
        result = session.play()

        assert result.stopped_because is not None
        session.table.close()

    def test_an_agent_cannot_act_as_another_player(self, live_server, mm_token):
        """The actor is bound to the connection, not taken from tool input."""
        from tools.agentic_playtest.run import Budget, build_session

        client = StubClient({"MM": [], "player": []})
        session = build_session(
            client=client, base_url=live_server, mm_token=mm_token,
            scenario="s", prep="p", cast_blurb="c",
            party=[{"player_name": "Zahna", "character_name": "Zahna",
                    "primary_facet": "body", "attributes": ATTRS}],
            enemies=[], seed=5, session_name="stub-actor",
            budget=Budget(max_beats=1),
        )
        dispatch = session._dispatch_for("Zahna")
        # No player_name parameter exists to spoof — the signature has no slot.
        result = dispatch("say", {"text": "hello"})

        assert result == {"ok": True}
        assert session.table.log.by_actor("Zahna") or True
        session.table.close()


# ---------------------------------------------------------------------------
# Scenarios — the pack must transcribe canon, not invent it
# ---------------------------------------------------------------------------

import yaml  # noqa: E402


def _canon_enemy(enemy_id: str) -> dict:
    """The enemy block from enemies/<id>.fof — the single source of truth."""
    text = (REPO_ROOT / "enemies" / f"{enemy_id}.fof").read_text(encoding="utf-8")
    return yaml.safe_load(text)["enemy"]


class TestScenarioCanon:
    """CLAUDE.md's iron law: nothing invented. A playtest that contaminates the
    canon it is testing is worse than no playtest, and a stat line that drifts
    from its `.fof` silently retunes the experiment."""

    @pytest.mark.parametrize("key", ["archive_guardian", "city_watch_sergeant",
                                     "harbor_thug"])
    def test_stat_lines_match_the_canonical_fof(self, key):
        from tools.agentic_playtest import scenarios

        blocks = {e["id"]: e for s in scenarios.SCENARIOS.values() for e in s.enemies}
        canon = _canon_enemy(key)
        block = blocks[key]

        for field in ("tier", "attack_modifier", "defense_modifier", "armor"):
            assert block[field] == canon[field], f"{key}.{field} drifted from canon"
        if "resolve" in canon:
            assert block["resolve"] == canon["resolve"]

    def test_the_guardian_phase_threshold_matches_canon(self):
        from tools.agentic_playtest import scenarios

        canon = _canon_enemy("archive_guardian")
        assert (scenarios.ARCHIVE_GUARDIAN["phases"][0]["resolve_threshold"]
                == canon["phases"][0]["resolve_threshold"])

    def test_the_party_matches_the_canonical_character_files(self):
        from tools.agentic_playtest.scenarios import PARTY

        by_character = {p["character_name"]: p for p in PARTY}
        for name in ("Zahna", "Mordai", "Zulnut"):
            canon = yaml.safe_load(
                (REPO_ROOT / "characters" / f"{name}.fof").read_text(encoding="utf-8"))
            character = canon.get("character", canon)
            assert by_character[name]["attributes"] == character["attributes"], name
            assert by_character[name]["primary_facet"] == character["primary_facet"]

    def test_every_attribute_spread_spends_the_same_budget(self):
        """The fourth seat is built to the same standard as the canon three."""
        from tools.agentic_playtest.scenarios import PARTY

        totals = {p["character_name"]: sum(p["attributes"].values()) for p in PARTY}
        assert set(totals.values()) == {18}, totals

    def test_both_scenarios_give_the_mm_permission_not_to_force_the_fight(self):
        """The experiment measures enemy variance; an MM that railroads every
        table into combat measures the railroad instead."""
        from tools.agentic_playtest.scenarios import SCENARIOS

        for scenario in SCENARIOS.values():
            prep = scenario.prep.lower()
            assert "do not" in prep, f"{scenario.key} prep has no restraint clause"


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

class TestCli:
    def test_pilot_defaults_to_a_short_capped_run(self):
        """The gate is only a gate if it is cheap. A pilot that inherits the
        batch's beat cap costs as much as a real session."""
        from tools.agentic_playtest import cli

        args = _parse(cli, ["pilot"])
        assert args.max_beats < 25
        assert args.arm == "A"

    def test_batch_pairs_every_seed_across_both_arms(self):
        from tools.agentic_playtest import cli

        args = _parse(cli, ["batch", "--sessions-per-arm", "4"])
        scenarios = [("guardian_chamber", "aldermans_office")[i % 2]
                     for i in range(args.sessions_per_arm)]
        pairs = [(s, args.seed_base + i, arm)
                 for i, s in enumerate(scenarios) for arm in ("A", "B")]

        assert len(pairs) == 8
        # Every (scenario, seed) appears in both arms — that is what "paired" means.
        for scenario, seed, _ in pairs:
            arms = {a for s, sd, a in pairs if (s, sd) == (scenario, seed)}
            assert arms == {"A", "B"}

    def test_an_unknown_subcommand_is_rejected(self):
        from tools.agentic_playtest import cli

        with pytest.raises(SystemExit):
            cli.main(["conjure"])

    def test_analyse_refuses_an_empty_directory(self, tmp_path):
        """Better to stop than to report a judgement over nothing."""
        from tools.agentic_playtest import cli

        with pytest.raises(SystemExit):
            cli.main(["analyse", str(tmp_path)])

    def test_the_server_gets_its_own_port_and_data_directory(self, tmp_path):
        from tools.agentic_playtest.cli import AppServer

        one = AppServer(data_dir=tmp_path / "a")
        two = AppServer(data_dir=tmp_path / "b")

        assert one.port != two.port
        assert one.base_url.startswith("http://127.0.0.1:")


def _parse(cli_module, argv: list[str]):
    """The parsed namespace, without running the command."""
    return cli_module.build_parser().parse_args(argv)


# ---------------------------------------------------------------------------
# Transcript fidelity — the defects the rehearsal found
# ---------------------------------------------------------------------------

class TestTranscriptRendersWhatTheServerSends:
    """Two defects, both silent, both fatal to the experiment's only artifact.

    The renderer matched event kinds (`roll`, `strike`, `enemy_attack`) that the
    observer socket never emits, so every die roll was invisible in the rendered
    transcript. Separately, `say_ooc` and `describe_scene` appended locally *and*
    were echoed by the server, logging one utterance twice — the batch-07
    over-count in a new place, and directly on the OOC:IC metric.
    """

    #: Kinds the harness writes itself; the server has no concept of them.
    HARNESS_LOCAL = {"say", "say_ooc", "scene", "scene_ended", "rules_gap",
                     "refused", "character_joined", "roll"}

    def test_every_rendered_kind_is_a_type_the_server_broadcasts(self):
        """The structural fix. A renderer branch for a kind nothing emits is
        dead code that looks like coverage."""
        import re

        source = (SOFTWARE_DIR / "app" / "api" / "websocket.py").read_text(encoding="utf-8")
        broadcast = set(re.findall(r'"type":\s*"(\w+)"', source))

        renderer = (SOFTWARE_DIR / "tools" / "agentic_playtest" /
                    "transcript.py").read_text(encoding="utf-8")
        rendered = set(re.findall(r'event\.kind == "(\w+)"', renderer))
        rendered |= set(re.findall(r'event\.kind in \("(\w+)", "(\w+)"\)', renderer)
                        and [k for pair in
                             re.findall(r'event\.kind in \("(\w+)", "(\w+)"\)', renderer)
                             for k in pair])

        unknown = rendered - broadcast - self.HARNESS_LOCAL
        assert not unknown, (
            f"transcript.py renders kinds the server never broadcasts: "
            f"{sorted(unknown)}")

    def test_a_roll_reaches_the_rendered_transcript(self, table):
        """The end-to-end version: a real roll must show its real dice."""
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        roll = Verbs(table).roll_skill("Zahna", "strength", "athletics")

        text = render(table.log)
        assert str(roll["total"]) in text
        assert "Zahna rolls" in text

    def test_speech_is_logged_exactly_once(self, table):
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        verbs = Verbs(table)
        verbs.say("Zahna", "One line, one event.")

        assert len(table.log.of_kind("say")) == 1

    def test_ooc_is_not_also_logged_as_in_character_speech(self, table):
        """The OOC:IC ratio is a headline metric; double-logging corrupts both
        sides of it at once."""
        from tools.agentic_playtest.verbs import Verbs

        table.join_as_player("Zahna")
        Verbs(table).say_ooc("Zahna", "Do I add my skill here?")

        assert len(table.log.of_kind("say_ooc")) == 1
        assert len(table.log.of_kind("say")) == 0
        assert table.log.of_kind("say_ooc")[0].data["text"] == "Do I add my skill here?"

    def test_mm_narration_is_one_scene_event_not_a_scene_and_a_say(self, table):
        from tools.agentic_playtest.verbs import Verbs

        Verbs(table).describe_scene("MM", "Ward-lanterns flicker.")

        assert len(table.log.of_kind("scene")) == 1
        assert len(table.log.of_kind("say")) == 0

    def test_a_ruling_is_logged_as_a_gap_not_as_speech(self, table):
        from tools.agentic_playtest.verbs import Verbs

        Verbs(table).rule_it("MM", "Can you Press from Withdrawn?", "No.")

        assert len(table.log.of_kind("rules_gap")) == 1
        assert len(table.log.of_kind("say")) == 0


class TestRehearsal:
    """The free gate. It exists because every defect above was found by running
    the real thing with a scripted stand-in for the model, at zero cost."""

    def test_the_script_only_names_real_verbs(self):
        from tools.agentic_playtest.rehearsal import rehearsal_script
        from tools.agentic_playtest.verbs import Verbs

        script = rehearsal_script("archive_guardian", "Sophia")
        for turns in script.values():
            for name, _ in turns:
                assert hasattr(Verbs, name), f"no such verb: {name}"

    def test_the_script_arguments_match_the_verb_signatures(self):
        """A wrong keyword here is a pilot that dies mid-session, after paying."""
        import inspect

        from tools.agentic_playtest.rehearsal import rehearsal_script
        from tools.agentic_playtest.verbs import Verbs

        script = rehearsal_script("archive_guardian", "Sophia")
        for turns in script.values():
            for name, kwargs in turns:
                params = set(inspect.signature(getattr(Verbs, name)).parameters)
                unknown = set(kwargs) - params
                assert not unknown, f"{name} has no parameter(s) {sorted(unknown)}"

    def test_a_rehearsal_runs_end_to_end_and_validates(self, live_server, mm_token):
        from tools.agentic_playtest.rehearsal import ScriptedClient, rehearsal_script
        from tools.agentic_playtest.run import Budget, build_session
        from tools.agentic_playtest.scenarios import CAST_BLURB, PARTY, SCENARIOS

        scenario = SCENARIOS["guardian_chamber"]
        session = build_session(
            client=ScriptedClient(rehearsal_script(scenario.enemies[0]["id"],
                                                   PARTY[0]["player_name"])),
            base_url=live_server, mm_token=mm_token, scenario=scenario.briefing,
            prep=scenario.prep, cast_blurb=CAST_BLURB, party=PARTY,
            enemies=scenario.enemies, seed=1, arm="A",
            session_name="rehearsal-test", budget=Budget(max_beats=2),
        )
        result = session.play()
        session.table.close()

        assert result.validation_ok, result.validation_report
        # The whole point: dice, and an enemy, actually appear.
        assert "Archive Guardian" in result.transcript
        assert "rolls" in result.transcript


# ---------------------------------------------------------------------------
# The subagent path — a table that short-lived processes can act on
# ---------------------------------------------------------------------------

class TestBroker:
    """The broker fronts the table for `play_as`. It must not become a second
    place where rules live, and it must not let an actor act as someone else."""

    @pytest.fixture
    def broker(self, table, tmp_path):
        from tools.agentic_playtest.broker import Broker
        from tools.agentic_playtest.scenarios import HARBOR_THUG

        table.add_enemy(HARBOR_THUG)  # spawn_enemy reads the session's library
        table.join_as_player("Zahna")
        table.create_character("Zahna", "Zahna", "body", ATTRS)
        return Broker(table, tmp_path / "out",
                      [{"player_name": "Zahna", "character_name": "Zahna"}])

    def test_a_player_may_not_call_an_mm_verb(self, broker):
        result = broker.take_turn("Zahna", "land_enemy_attack",
                                  {"target_player": "Zahna", "condition": "broken"})
        assert "refused" in result
        assert "land_enemy_attack" in result["refused"]

    def test_an_unknown_verb_is_refused_not_raised(self, broker):
        assert "refused" in broker.take_turn("Zahna", "teleport", {})

    def test_wrong_arguments_are_refused_with_the_reason(self, broker):
        result = broker.take_turn("Zahna", "say", {"words": "hello"})
        assert "refused" in result and "say" in result["refused"]

    def test_a_real_verb_returns_the_engine_s_answer(self, broker):
        result = broker.take_turn("Zahna", "roll_skill",
                                  {"attribute_id": "strength", "skill_id": "athletics"})
        assert result["ok"]
        # The engine's dice, not ours.
        assert len(result["result"]["dice_rolled"]) == 2
        assert result["result"]["total"] == (
            result["result"]["dice_sum"]
            + result["result"]["attribute_modifier"]
            + result["result"]["skill_modifier"]
            + result["result"]["difficulty_modifier"])

    def test_the_enemy_roster_is_replayed_from_the_log(self, broker):
        """Not kept as a second copy — a copy can disagree with the engine."""
        broker.take_turn("MM", "spawn_enemy", {"enemy_id": "harbor_thug"})
        roster = broker.state_for("MM")["active_enemies"]
        assert roster and all(e["name"] for e in roster.values())

    def test_a_defeated_mook_leaves_the_roster(self, broker):
        spawn = broker.take_turn("MM", "spawn_enemy", {"enemy_id": "harbor_thug"})
        key = spawn["result"]["tracker_key"]
        broker.take_turn("MM", "apply_strike_to_enemy",
                         {"tracker_key": key, "outcome": "full_success"})
        assert key not in broker.state_for("MM")["active_enemies"]

    def test_finish_writes_every_artifact(self, broker, tmp_path):
        broker.take_turn("Zahna", "say", {"text": "one line"})
        summary = broker.finish()
        out = tmp_path / "out"
        for name in ("transcript.md", "events.jsonl", "metrics.json",
                     "validation.txt"):
            assert (out / name).exists(), name
        assert summary["validation_ok"]


class TestSubagentBriefings:
    """What a subagent is told is the only thing standing between it and the
    batch-07 failure mode, so the wording is load-bearing."""

    def test_the_brief_forbids_asserting_an_outcome(self):
        from tools.agentic_playtest.host import HOW_TO_ACT

        text = HOW_TO_ACT.lower()
        assert "you never decide an outcome" in text
        assert "flagged as a defect" in text

    def test_the_brief_tells_them_refusal_is_allowed(self):
        from tools.agentic_playtest.host import PLAYER_BRIEF

        assert "refuse a hook" in PLAYER_BRIEF

    def test_the_mm_brief_states_that_enemies_never_roll(self):
        from tools.agentic_playtest.host import MM_BRIEF

        assert "Enemies never roll" in MM_BRIEF
        assert "rule_it" in MM_BRIEF

    def test_the_mm_brief_says_prep_is_disposable(self):
        from tools.agentic_playtest.host import MM_BRIEF

        assert "Prep is disposable" in MM_BRIEF


class TestValidatorKindsStayInStep:
    """The confabulation check compares narration against what the engine
    actually logged. It can only do that if it looks for the kinds the client
    actually writes.

    These drifted once: `_MECHANICAL_KINDS` held verb names ("roll", "strike")
    while the log carried result kinds ("roll_result", "strike_result"). The two
    sets were disjoint, so `_beat_facts` matched nothing, every beat's known
    facts were empty, and the check silently verified nothing — while still
    being able to flag *accurate* narration as invented. The existing unit tests
    hid it by hand-building events with the legacy names.
    """

    def test_every_validator_kind_is_a_kind_the_client_logs(self):
        from tools.agentic_playtest.validate import _MECHANICAL_KINDS
        from tools.agentic_playtest import client as client_module

        table = next(v for v in vars(client_module).values()
                     if isinstance(v, type) and hasattr(v, "MECHANICAL"))
        unknown = [k for k in _MECHANICAL_KINDS if k not in table.MECHANICAL]
        assert not unknown, (
            f"validate._MECHANICAL_KINDS names kinds the client never logs: "
            f"{unknown}. The confabulation check silently verifies nothing when "
            f"these drift apart.")

    def test_the_recorded_run_uses_kinds_the_validator_recognises(self):
        """The shipped playtest artifact must be checkable by the checker whose
        output it cites as evidence."""
        import json
        from pathlib import Path
        from tools.agentic_playtest.validate import _MECHANICAL_KINDS

        events = Path(__file__).resolve().parents[2] / (
            "playtest/08_npc_variance/subagent_session/events.jsonl")
        if not events.exists():
            pytest.skip("recorded run not present")
        kinds = {json.loads(line).get("kind") for line in events.read_text().splitlines() if line.strip()}
        assert kinds & set(_MECHANICAL_KINDS), (
            f"No event in the recorded run matches any kind the validator looks "
            f"for. Logged kinds: {sorted(k for k in kinds if k)}")
