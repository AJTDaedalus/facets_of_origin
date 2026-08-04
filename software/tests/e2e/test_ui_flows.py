"""Browser-driven front-end regression tests.

The Python suite exercises the engine and the API. It cannot see the failure
mode the 2026-07-31 front-end audit was full of: a control that exists, looks
enabled, and is wired to nothing — a mismatched broadcast key, an MM-gated event
behind a player-facing button, a form that posts into a library nothing renders.
Every check here drives the real app in a real browser and asserts that an
action a player or MM would take actually changes what they see.

Skipped unless Playwright and its Chromium build are installed:

    pip install playwright && playwright install chromium

See docs/RESEARCH_frontend_audit.md for the findings these cover.
"""
from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # not installed, or installed without its browsers
    pytest.skip(
        f"Playwright unavailable ({exc}); front-end tests skipped. "
        "Install with: pip install playwright && playwright install chromium",
        allow_module_level=True,
    )

PASSWORD = "e2e-test-password"
SOFTWARE_DIR = Path(__file__).resolve().parents[2]


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    """A real uvicorn process against a throwaway data directory.

    Its own port and data dir keep it from colliding with a dev server or
    inheriting an MM password from a previous run.
    """
    port = _free_port()
    data_dir = tmp_path_factory.mktemp("e2e-data")

    # Settings has no env_prefix, so the env var names are the field names.
    env = {
        **dict(__import__("os").environ),
        "DATA_DIR": str(data_dir),
        "PORT": str(port),
        "HOST": "127.0.0.1",
    }
    proc = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=SOFTWARE_DIR, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )

    base = f"http://127.0.0.1:{port}"
    for _ in range(100):
        if proc.poll() is not None:
            pytest.fail(f"server exited early:\n{proc.stdout.read().decode(errors='replace')}")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("server did not start")

    yield base
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


class Errors(list):
    """Collects console errors and page exceptions raised by any page."""

    def attach(self, page, label):
        page.on("pageerror", lambda e: self.append(f"[{label}] pageerror: {e}"))
        page.on("console", lambda m: (
            self.append(f"[{label}] console.{m.type}: {m.text}")
            if m.type == "error" and "401" not in m.text else None))
        return page


@pytest.fixture
def errors():
    e = Errors()
    yield e
    assert not e, "front-end errors:\n" + "\n".join(e)


@pytest.fixture(scope="module")
def mm_token(live_server, browser):
    """Set the MM password once and keep the token.

    `/auth/mm-login` is rate limited (`auth_rate_limit`), which is correct
    behaviour and exactly what a per-test login through the form trips: later
    tests started failing setup with 429. One real login per module, reused.
    """
    page = browser.new_page()
    page.goto(live_server)
    page.wait_for_timeout(250)
    page.click("text=First Run Setup")
    page.fill("#setup-password", PASSWORD)
    page.fill("#setup-confirm", PASSWORD)
    page.click("text=Set Password")
    page.wait_for_timeout(400)
    page.fill("#mm-password", PASSWORD)
    page.click("button:has-text('Log In')")
    page.wait_for_selector("#mm-dashboard:not(.hidden)", timeout=10000)
    token = page.evaluate("() => sessionStorage.getItem('facets_token')")
    page.close()
    assert token, "MM login did not store a token"
    return token


def _login_mm(page, base, token):
    """Seed the stored session the login form would have written, then load.

    Deliberately skips the form: the login path itself is covered once by the
    `mm_token` fixture, and repeating it here would only exercise the limiter.
    """
    page.goto(base)
    page.evaluate("""t => {
        sessionStorage.setItem('facets_token', t);
        sessionStorage.setItem('facets_role', 'mm');
        sessionStorage.setItem('facets_player_name', 'MM');
    }""", token)
    page.goto(base)
    page.wait_for_timeout(250)
    page.evaluate("() => showMMDashboard()")
    page.wait_for_selector("#mm-dashboard:not(.hidden)", timeout=10000)
    page.wait_for_timeout(300)


def _make_session_and_invite(page, name, player):
    page.fill("#new-session-name", name)
    page.click("button:has-text('Create Session')")
    page.wait_for_timeout(600)
    page.select_option("#invite-session-id", label=name)
    page.fill("#invite-player-name", player)
    page.click("button:has-text('Generate Invite Link')")
    page.wait_for_selector(".invite-url", timeout=10000)
    invite = page.inner_text(".invite-url")
    page.click(f"#session-list li:has-text('{name}') button:has-text('Open')")
    page.wait_for_selector("#game-screen:not(.hidden)", timeout=10000)
    page.wait_for_timeout(500)
    return invite


def _join_and_build(page, invite, char_name):
    page.goto(invite)
    page.wait_for_timeout(300)
    page.click("button:has-text('Join Session')")
    page.wait_for_selector("#char-create-panel:not(.hidden)", timeout=10000)
    page.wait_for_timeout(300)
    page.fill("#cc-name", char_name)
    page.click("button:has-text('Create Character')")
    page.wait_for_selector("#character-panel:not(.hidden)", timeout=10000)
    page.wait_for_timeout(500)


@pytest.fixture
def table(live_server, browser, errors, request, mm_token):
    """An MM in a session plus one player with a character.

    Each test gets its own session — they share one server process, and a
    shared session would let one test's enemies and clocks leak into the next.
    """
    mm = errors.attach(browser.new_page(viewport={"width": 1400, "height": 950}), "MM")
    _login_mm(mm, live_server, mm_token)
    session_name = f"E2E {request.node.name}"[:60]
    invite = _make_session_and_invite(mm, session_name, "Zahna")

    player = errors.attach(browser.new_page(viewport={"width": 1400, "height": 950}), "PLAYER")
    _join_and_build(player, invite, "Zahna")
    mm.wait_for_timeout(500)

    yield mm, player
    mm.close()
    player.close()


# ---------------------------------------------------------------------------
# Session state reaches everyone who is already connected
# ---------------------------------------------------------------------------

class TestSessionAwareness:
    def test_mm_sees_a_new_character_without_reloading(self, table):
        """Character creation is a REST call that used to broadcast nothing."""
        mm, _ = table
        assert "Zahna" in mm.inner_text("#mm-combat-roster")

    def test_mm_player_pickers_populate_from_live_state(self, table):
        """Every MM control that addresses a player was a free-text field; a
        typo was a silent no-op."""
        mm, _ = table
        options = mm.eval_on_selector_all(
            "#play-mm-spark-player option", "els => els.map(e => e.value).filter(Boolean)")
        assert "Zahna" in options

    def test_mm_is_not_shown_an_empty_player_sheet(self, table):
        mm, _ = table
        assert not mm.is_visible("#character-panel")
        assert mm.is_visible("#mm-left-panel")


# ---------------------------------------------------------------------------
# Combat — the enemy half of a fight has to be drivable
# ---------------------------------------------------------------------------

class TestCombatLoop:
    def test_mm_can_land_an_enemy_attack_on_a_character(self, table):
        """NPCs never roll, so applying the incoming Condition is the only way
        an enemy attack lands. It had no control anywhere in the UI."""
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(400)

        options = mm.eval_on_selector_all(".mm-attack-tier option", "els => els.map(e => e.value)")
        assert options, "no Condition options in the MM combat console"

        mm.select_option(".mm-attack-tier >> nth=0", options[0])
        mm.click("button:has-text('Land Hit')")
        mm.wait_for_timeout(700)

        assert player.inner_text("#combat-conditions").strip(), \
            "Condition did not render on the target"

    def test_mm_can_clear_a_condition(self, table):
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        options = mm.eval_on_selector_all(".mm-attack-tier option", "els => els.map(e => e.value)")
        mm.select_option(".mm-attack-tier >> nth=0", options[0])
        mm.click("button:has-text('Land Hit')")
        mm.wait_for_timeout(700)

        mm.click(".condition-clearable >> nth=0")
        mm.wait_for_timeout(700)
        assert not player.inner_text("#combat-conditions").strip()

    def test_postures_can_be_revealed(self, table):
        """Postures are declared in secret; without a reveal control the
        simultaneous-declaration mechanic never resolved."""
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(400)
        player.check("input[name='combat-posture'][value='defensive']")
        player.click("button:has-text('Declare Posture')")
        player.wait_for_timeout(500)

        mm.click("button:has-text('Reveal Postures')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(300)
        assert player.is_visible("#combat-postures-revealed")

    def test_combat_panel_stays_readable_out_of_combat(self, table):
        """Hiding it outright meant a player could not check their Endurance
        pool, armour budget, or reaction costs while deciding to fight."""
        _, player = table
        assert player.is_visible("#combat-panel")
        assert player.is_visible("#combat-idle-note")

    def test_strike_targets_come_from_a_picker(self, table):
        """Target was a free-text field while every legal target was already in
        client state."""
        mm, player = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.fill("#builder-enemy-name", "Harbor Thug")
        mm.select_option("#builder-enemy-tier", "mook")
        mm.click("button:has-text('Save to Library')")
        mm.wait_for_timeout(600)
        mm.click("button[data-tab='play']")
        mm.wait_for_timeout(300)
        mm.select_option("#play-spawn-enemy-select", "harbor_thug")
        mm.click("button:has-text('Spawn')")
        mm.wait_for_timeout(700)

        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(500)
        player.click("#combat-panel button:has-text('Strike')")
        player.wait_for_timeout(300)

        assert player.eval_on_selector("#strike-target", "e => e.tagName") == "SELECT"
        targets = player.eval_on_selector_all(
            "#strike-target option", "els => els.map(e => e.textContent)")
        assert any("Harbor Thug" in t for t in targets)


# ---------------------------------------------------------------------------
# Builder — saved content has to be reachable again
# ---------------------------------------------------------------------------

class TestBuilderLibraries:
    def test_an_encounter_can_be_saved_listed_and_run(self, table):
        """Encounters were write-only: nothing rendered, loaded, or ran one."""
        mm, _ = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.fill("#builder-enemy-name", "Harbor Thug")
        mm.select_option("#builder-enemy-tier", "mook")
        mm.click("button:has-text('Save to Library')")
        mm.wait_for_timeout(600)

        mm.fill("#builder-encounter-name", "Dock Ambush")
        mm.select_option("#builder-encounter-add-enemy", "harbor_thug")
        mm.click("#builder-mm-section button:has-text('Add')")
        mm.wait_for_timeout(300)
        mm.click("button:has-text('Save Encounter')")
        mm.wait_for_timeout(700)
        assert "Dock Ambush" in mm.inner_text("#builder-encounter-library-list")

        mm.click("#builder-encounter-library-list button:has-text('Run')")
        mm.wait_for_timeout(300)
        mm.click(".modal button:has-text('Run Encounter')")
        mm.wait_for_timeout(800)
        mm.click("button[data-tab='play']")
        mm.wait_for_timeout(400)
        assert "Harbor Thug" in mm.inner_text("#play-enemy-tracker")

    def test_a_saved_enemy_can_be_edited(self, table):
        """Save-new and delete only: changing one stat meant retyping the block."""
        mm, _ = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.fill("#builder-enemy-name", "Watch Sergeant")
        mm.select_option("#builder-enemy-tier", "named")
        mm.click("button:has-text('Save to Library')")
        mm.wait_for_timeout(600)

        mm.click("#builder-enemy-library-list button:has-text('Edit')")
        mm.wait_for_timeout(300)
        assert mm.input_value("#builder-enemy-name") == "Watch Sergeant"

    def test_threat_rating_comes_from_the_engine(self, table):
        """The Builder used to carry its own copy of the MM1 formula, and it had
        drifted: its Resolve bucketing disagreed with the engine."""
        mm, _ = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.fill("#builder-enemy-name", "Archive Guardian")
        mm.select_option("#builder-enemy-tier", "boss")
        mm.fill("#builder-enemy-resolve", "8")
        mm.fill("#builder-enemy-attack", "2")
        mm.select_option("#builder-enemy-armor", "heavy")
        mm.wait_for_timeout(600)
        # offense max(0, 2+2)=4 + resolve 8 + heavy 2 = 14
        assert "14" in mm.inner_text("#builder-enemy-tr")


# ---------------------------------------------------------------------------
# Advancement and the Spark cadence
# ---------------------------------------------------------------------------

class TestAdvancementAndSparks:
    def test_marking_a_skill_used_reaches_the_player(self, table):
        mm, player = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.select_option("#builder-mark-player", "Zahna")
        mm.select_option("#builder-mark-skill", "lore")
        mm.click("button:has-text('Mark as Used')")
        mm.wait_for_timeout(700)

        player.click("button[data-tab='builder']")
        player.wait_for_timeout(500)
        assert "USED" in player.inner_text("#builder-skills-list")

    def test_act_break_prompts_the_players(self, table):
        """The button used to post a chat line; the real act_break event was
        never sent, so players got no prompt at all."""
        mm, player = table
        mm.click("button:has-text('Open Act Break')")
        mm.wait_for_timeout(700)
        assert player.is_visible(".toast-gold")

    def test_mm_table_roller_shows_dice_and_a_total_only(self, table):
        """A utility for random tables and oracles. It must stay visibly apart
        from the resolution system — no outcome tier, and nothing that reads as
        an NPC rolling."""
        mm, player = table
        mm.click(".collapsible-toggle:has-text('Table Roller')")
        mm.wait_for_timeout(300)
        mm.fill("#table-roll-label", "Wandering encounter")
        mm.click(".dice-quick-row button:has-text('d20')")
        mm.wait_for_timeout(700)

        result = mm.inner_text("#table-roll-result")
        assert "Wandering encounter" in result
        for tier in ("Full Success", "Success with Cost", "Things Go Wrong"):
            assert tier not in result, "table roll must not carry a resolution outcome"

        # The table sees the result, so a roll behind the screen stays a choice.
        assert "Table roll" in player.inner_text("#play-chat-log")

    def test_players_have_no_table_roller(self, table):
        _, player = table
        assert not player.is_visible("#table-roll-notation")

    def test_enemy_strike_depletion_comes_from_the_engine(self, table):
        """The tracker sends the Strike outcome; the server applies the D1 rule.
        The buttons used to send a pre-computed Resolve value, which put the
        depletion rule in the browser as well as the simulator."""
        mm, _ = table
        mm.click("button[data-tab='builder']")
        mm.wait_for_timeout(300)
        mm.fill("#builder-enemy-name", "Watch Sergeant")
        mm.select_option("#builder-enemy-tier", "named")
        mm.fill("#builder-enemy-resolve", "4")
        mm.click("button:has-text('Save to Library')")
        mm.wait_for_timeout(600)

        mm.click("button[data-tab='play']")
        mm.wait_for_timeout(300)
        mm.select_option("#play-spawn-enemy-select", "watch_sergeant")
        mm.click("button:has-text('Spawn')")
        mm.wait_for_timeout(700)
        assert "4/4" in mm.inner_text("#play-enemy-tracker")

        mm.click("#play-enemy-tracker button:has-text('Hit 10+')")
        mm.wait_for_timeout(700)
        # 4 - 2 = 2, decided server-side by combat.apply_resolve_damage
        assert "2/4" in mm.inner_text("#play-enemy-tracker")

    def test_technique_panel_renders_for_a_player(self, table):
        """technique_select was MM-gated while the only control that sent it was
        the player's Builder tab, so no character could ever gain a Technique."""
        _, player = table
        player.click("button[data-tab='builder']")
        player.wait_for_timeout(500)
        assert "Technique pick" in player.inner_text("#builder-technique-list")


# ---------------------------------------------------------------------------
# Quick references may not state a rule facet.yaml does not
# ---------------------------------------------------------------------------

class TestQuickReferencesMatchCanon:
    def test_no_pre_technique_difficulty_penalty(self, table):
        """facet.yaml sets pre_technique_difficulty_penalty: 0 — the scope
        restriction is the whole limitation."""
        _, player = table
        player.click("button[data-tab='tools']")
        player.wait_for_timeout(500)
        assert "+1 difficulty step" not in player.inner_text("#tools-rule-summaries")

    def test_advancement_numbers_come_from_the_ruleset(self, table):
        """The card hard-coded a pre-v0.3 threshold of 6 and a Major every 4."""
        _, player = table
        player.click("button[data-tab='tools']")
        player.wait_for_timeout(400)
        player.click(".rule-summary-toggle:has-text('Skill Advancement')")
        player.wait_for_timeout(200)
        text = player.inner_text(".rule-summary-card:has-text('Skill Advancement')")
        assert "Every 5 primary" in text
        assert "Every 3 total" in text


# ---------------------------------------------------------------------------
# Starting over
# ---------------------------------------------------------------------------

class TestDestructiveFlows:
    def test_a_player_can_delete_and_rebuild(self, table):
        """An invite is single-use, so a misbuilt character was permanent."""
        mm, player = table
        player.click("button[data-tab='tools']")
        player.wait_for_timeout(500)
        player.click("button:has-text('Delete & Rebuild')")
        player.wait_for_timeout(300)
        player.click(".modal button:has-text('Delete Character')")
        player.wait_for_timeout(800)

        player.click("button[data-tab='play']")
        player.wait_for_timeout(400)
        assert player.is_visible("#char-create-panel")
        assert not player.is_visible("#character-panel")

        mm.wait_for_timeout(400)
        assert "Zahna" not in mm.inner_text("#mm-combat-roster")

        player.fill("#cc-name", "Zahna Reborn")
        player.click("button:has-text('Create Character')")
        player.wait_for_selector("#character-panel:not(.hidden)", timeout=10000)
        player.wait_for_timeout(500)
        assert "Zahna Reborn" in mm.inner_text("#mm-combat-roster")


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

class TestPresentation:
    def test_no_horizontal_overflow_on_a_phone(self, table):
        _, player = table
        player.set_viewport_size({"width": 390, "height": 844})
        player.wait_for_timeout(400)
        overflow = player.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        player.set_viewport_size({"width": 1400, "height": 950})
        assert overflow <= 2, f"page scrolls sideways by {overflow}px at 390px wide"

    @pytest.mark.parametrize("prop", ["--surface", "--accent"])
    def test_css_custom_properties_are_defined(self, table, prop):
        """Both were referenced by bar tracks and hover states but never
        declared, so those declarations were invalid and simply did nothing."""
        _, player = table
        value = player.evaluate(
            "p => getComputedStyle(document.documentElement).getPropertyValue(p).trim()", prop)
        assert value, f"{prop} is not defined"

    def test_radio_controls_are_not_stretched_to_full_width(self, table):
        """The blanket `input { width: 100% }` rule caught radios too, scattering
        the Posture, Scope, and Spark-use controls across their rows."""
        _, player = table
        width = player.evaluate(
            "() => document.querySelector(\"input[name='combat-posture']\").getBoundingClientRect().width")
        assert width < 40, f"radio is {width}px wide"

    def test_help_names_where_each_task_lives(self, table):
        mm, _ = table
        mm.click("button:has-text('Help')")
        mm.wait_for_timeout(300)
        assert "Land Hit" in mm.inner_text("#help-content")
        mm.click("#help-drawer button:has-text('Close')")
