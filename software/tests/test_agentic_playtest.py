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

import socket
import subprocess
import sys
import time
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
        log.append("roll", "Zahna", roll=_roll(8, [3, 5]))
        log.append("say", "Zahna", text="An 8 — enough to get through the gate.")

        assert find_confabulations(log, ruleset).ok

    def test_rejects_a_total_the_engine_never_produced(self, ruleset):
        log = EventLog("s1")
        log.append("roll", "Zahna", roll=_roll(8, [3, 5]))
        log.append("say", "Zahna", text="I rolled a 12, so the door swings wide.")

        report = find_confabulations(log, ruleset)
        assert any(f.kind == "total" for f in report.findings)

    def test_rejects_an_outcome_label_the_engine_never_gave(self, ruleset):
        log = EventLog("s1")
        log.append("roll", "Zahna", roll=_roll(8, [3, 5], label="Success with Cost"))
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
        log.append("enemy_attack", "MM", target="Zahna", condition_applied="winded",
                   condition_declared="winded", all_conditions=["winded"])
        log.append("say", "MM", text="The blow lands — you have the winded condition.")

        assert find_confabulations(log, ruleset).ok

    def test_claims_are_scoped_to_their_own_beat(self, ruleset):
        """A roll in beat 1 does not license a claim about it in beat 2."""
        log = EventLog("s1")
        log.append("roll", "Zahna", roll=_roll(8, [3, 5]))
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
            log.append("roll", "P", roll=_roll(a + b, [a, b]))

        report = dice_distribution([log])

        assert not report.passed
        assert report.face_counts.get(1, 0) == 0

    def test_real_dice_pass(self):
        import random
        rng = random.Random(20260731)
        log = EventLog("real")
        for _ in range(200):
            dice = [rng.randint(1, 6), rng.randint(1, 6)]
            log.append("roll", "P", roll=_roll(sum(dice), dice))

        assert dice_distribution([log]).passed

    def test_small_samples_are_not_evaluated(self):
        log = EventLog("tiny")
        log.append("roll", "P", roll=_roll(7, [3, 4]))

        report = dice_distribution([log])
        assert report.passed and "minimum" in report.note

    def test_parse_dice_from_prose_reads_the_legacy_format(self):
        assert parse_dice_from_prose("**Roll:** 2d6 (2, 3) + 2 = **7**") == [2, 3]


# ---------------------------------------------------------------------------
# Transcript rendering
# ---------------------------------------------------------------------------

class TestTranscript:
    def test_dice_are_rendered_from_the_event(self):
        log = EventLog("s1")
        log.append("roll", "Zahna", roll=_roll(4, [1, 3]), description="pick the lock")

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
        log.append("roll", "Zahna", roll=_roll(9, [4, 5]))
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

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    port = _free_port()
    data_dir = tmp_path_factory.mktemp("agentic-data")
    env = {
        **dict(__import__("os").environ),
        "DATA_DIR": str(data_dir), "PORT": str(port), "HOST": "127.0.0.1",
    }
    proc = subprocess.Popen([sys.executable, "run.py"], cwd=SOFTWARE_DIR, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for _ in range(100):
        if proc.poll() is not None:
            pytest.fail(proc.stdout.read().decode(errors="replace"))
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("server did not start")

    yield f"http://127.0.0.1:{port}"
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


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
