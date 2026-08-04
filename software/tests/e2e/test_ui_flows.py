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
    # Log to a file, never to an undrained pipe. uvicorn logs every request at
    # info level; with `stdout=PIPE` and nobody reading it, the 64KB OS pipe
    # buffer filled about fifty tests in and the server BLOCKED ON WRITE —
    # wedged, accepting no HTTP at all. It looked like flakiness in whichever
    # test happened to be running at the time.
    log_path = data_dir / "server.log"
    log_file = log_path.open("wb")
    proc = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=SOFTWARE_DIR, env=env,
        stdout=log_file, stderr=subprocess.STDOUT,
    )

    def _server_log() -> str:
        try:
            return log_path.read_text(errors="replace")
        except OSError:
            return "(no server log)"

    base = f"http://127.0.0.1:{port}"
    for _ in range(100):
        if proc.poll() is not None:
            pytest.fail(f"server exited early:\n{_server_log()}")
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
    log_file.close()


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


def _delete_session(base: str, token: str, session_id: str) -> None:
    """Best-effort teardown — a failure here must not mask a test result."""
    import urllib.error
    import urllib.request

    request = urllib.request.Request(
        f"{base.rstrip('/')}/api/sessions/{session_id}", method="DELETE",
        headers={"Authorization": f"Bearer {token}"})
    try:
        urllib.request.urlopen(request, timeout=10).close()
    except (urllib.error.URLError, OSError):
        pass


def _make_session_and_invite(page, name, player):
    page.fill("#new-session-name", name)
    page.click("button:has-text('Create Session')")
    # Wait for the option, not for a fixed 600ms. The list re-render is async and
    # the session list grows all run, so a sleep is a race by construction.
    page.wait_for_function(
        """expected => {
            const select = document.getElementById('invite-session-id');
            return !!select && [...select.options].some(o => o.textContent === expected);
        }""",
        arg=name, timeout=15000)
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
    session_id = mm.evaluate("() => state.sessionId")

    player = errors.attach(browser.new_page(viewport={"width": 1400, "height": 950}), "PLAYER")
    _join_and_build(player, invite, "Zahna")
    mm.wait_for_timeout(500)

    yield mm, player
    mm.close()
    player.close()
    # Delete the session. Every test in this module makes one against a shared
    # server and nothing used to clean them up, so the dashboard's session list
    # grew all run; past ~50 the MM's own list stopped rendering and later
    # fixtures found an empty session picker. Bounding the accumulation is the
    # actual fix — waiting longer for the list only moved the threshold.
    if session_id:
        _delete_session(live_server, mm_token, session_id)


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



    def test_a_strike_on_a_tracked_enemy_can_be_applied_from_the_prompt(self, table):
        """A Strike roll does not itself remove the enemy — the MM must apply
        the outcome. The prompt used to say "apply it on the enemy tracker" and
        leave them to find the row, so between the roll and the click the table
        and the engine disagreed about whether the enemy was still standing.

        Found by the subagent playtest, 2026-07-31 (F4): a player rolled a full
        success on a Mook, said "that one should be gone", and it was not.
        """
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

        # Drive the Strike through the socket so the test does not depend on
        # the dice: any non-failure outcome must offer the MM an Apply.
        tracker_key = mm.evaluate("() => Object.keys(state.activeEnemies)[0]")
        assert tracker_key, "nothing in the enemy tracker to strike"
        mm.evaluate(
            """key => onStrikeResult({
                attacker: 'Zahna', target: key,
                roll: {dice_rolled: [6, 5], dice_kept: [6, 5], dice_sum: 11,
                       attribute_modifier: 0, skill_modifier: 0,
                       difficulty_modifier: 0, total: 11, outcome: 'full_success',
                       outcome_label: 'Full Success', outcome_description: '',
                       sparks_spent: 0},
                endurance_remaining: 5, sparks_remaining: 3, press_used: false,
            })""",
            tracker_key)
        mm.wait_for_timeout(400)

        apply_button = mm.locator("#toast-host button:has-text('Apply')")
        assert apply_button.count() == 1, "no one-click Apply on the Strike prompt"

        apply_button.click()
        mm.wait_for_timeout(800)

        # A Mook taking a full success is removed outright — the engine's call.
        remaining = mm.evaluate("() => Object.keys(state.activeEnemies)")
        assert tracker_key not in remaining, "Apply did not reach the engine"

    def test_a_strike_on_an_untracked_target_offers_no_apply(self, table):
        """PvP and untracked targets have nothing to apply the outcome to, so
        the prompt must stay advisory rather than offering a dead button."""
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)

        mm.evaluate(
            """() => onStrikeResult({
                attacker: 'Zahna', target: 'Some Bystander',
                roll: {dice_rolled: [6, 5], dice_kept: [6, 5], dice_sum: 11,
                       attribute_modifier: 0, skill_modifier: 0,
                       difficulty_modifier: 0, total: 11, outcome: 'full_success',
                       outcome_label: 'Full Success', outcome_description: '',
                       sparks_spent: 0},
                endurance_remaining: 5, sparks_remaining: 3, press_used: false,
            })""")
        mm.wait_for_timeout(400)

        assert mm.locator("#toast-host button:has-text('Apply')").count() == 0
        assert "Some Bystander" in mm.inner_text("#toast-host")

    def test_technique_step_banner_shows_both_moves(self, table):
        """B4 Q1 UX (DESIGN_technique_difficulty.md §2.7, TD-10): auto-apply is
        only legible at the table because the roll banner shows both moves —
        the MM's declared label and the Technique that stepped it."""
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(400)

        player.evaluate(
            """() => onStrikeResult({
                attacker: 'Zahna', target: 'goblin',
                roll: {dice_rolled: [6, 5], dice_kept: [6, 5], dice_sum: 11,
                       attribute_modifier: 0, skill_modifier: 0,
                       difficulty_modifier: 0, total: 11, outcome: 'full_success',
                       outcome_label: 'Full Success', outcome_description: '',
                       sparks_spent: 0, difficulty: 'Standard'},
                endurance_remaining: 5, sparks_remaining: 3, press_used: false,
                technique_step: {technique_id: 'weapon_mastery', technique_name: 'Weapon Mastery',
                                  from: 'Hard', to: 'Standard'},
            })""")
        player.wait_for_timeout(400)

        banner = player.inner_text("#play-roll-result-box")
        assert "Hard" in banner and "Standard" in banner and "Weapon Mastery" in banner
        assert player.locator("#play-roll-result-box .technique-step-banner").count() == 1

    def test_ordinary_strike_banner_has_no_technique_step(self, table):
        """Same box, no Technique fired — TD-10 must not change the banner
        when `technique_step` is absent."""
        mm, player = table
        mm.click("button:has-text('Start Combat')")
        mm.wait_for_timeout(600)
        player.wait_for_timeout(400)

        player.evaluate(
            """() => onStrikeResult({
                attacker: 'Zahna', target: 'goblin',
                roll: {dice_rolled: [6, 5], dice_kept: [6, 5], dice_sum: 11,
                       attribute_modifier: 0, skill_modifier: 0,
                       difficulty_modifier: 0, total: 11, outcome: 'full_success',
                       outcome_label: 'Full Success', outcome_description: '',
                       sparks_spent: 0, difficulty: 'Standard'},
                endurance_remaining: 5, sparks_remaining: 3, press_used: false,
            })""")
        player.wait_for_timeout(400)

        assert player.locator("#play-roll-result-box .technique-step-banner").count() == 0

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

    def test_available_technique_list_is_populated(self, table):
        """TODO T9: `renderBuilderTechniques` read `character_facets[].techniques`,
        a field the wire format has never carried, so the "Available" list was
        always empty and the panel always claimed every Technique was learned —
        whatever the truth. The tree actually lives at
        `ruleset.techniques[facet].branches[].tiers[].techniques[]`.
        """
        _, player = table
        player.click("button[data-tab='builder']")
        player.wait_for_timeout(500)
        panel = player.inner_text("#builder-technique-list")
        # The section label is uppercased by CSS, so compare case-insensitively.
        assert "available" in panel.lower(), (
            f"no Available section rendered — the tree lookup came back empty. "
            f"panel={panel[:200]!r}")
        # A real Tier 1 Technique from the pregen's own Facet.
        facet = player.evaluate("state.character.primary_facet")
        expected = {"body": "Forcing Hand", "mind": "Sharp Analysis",
                    "soul": "Read the Room"}[facet]
        assert expected in panel, f"expected {expected!r} for facet {facet!r}"

    def test_technique_display_name_resolves_from_the_real_tree(self, table):
        """Same root cause as T9, in `app.js::techniqueDisplayName`: it searched
        `character_facets[].techniques` and so always fell through to its
        id-prettifying default.

        The ids here are chosen so the prettifier gives the *wrong* answer —
        "Read The Room" vs the printed "Read the Room", "Cross Reference" vs
        "Cross-Reference". An earlier version of this test used `the_wrong_note`,
        whose printed name is exactly what the prettifier produces, so it passed
        against the broken code and proved nothing.
        """
        _, player = table
        assert player.evaluate("techniqueDisplayName('read_the_room')") == "Read the Room"
        assert player.evaluate("techniqueDisplayName('cross_reference')") == "Cross-Reference"
        # An unknown id still degrades to the prettified fallback.
        assert player.evaluate("techniqueDisplayName('no_such_technique')") == "No Such Technique"


# ---------------------------------------------------------------------------
# TD-20 (DESIGN §8): pickTechniqueChoice's non-domain choices fallback
# ---------------------------------------------------------------------------

class TestTechniqueChoicePicker:
    """`pickTechniqueChoice` used to build only domain-name option lists, so
    Weapon Mastery/Acclimated/Field of Mastery — none of which are domain-
    granting — offered whatever domain list the character's primary Facet
    happened to map to as candidate "weapon types". TD-19 gave the three a
    `choices` list of their own in facet.yaml; TD-20 makes the picker use it.

    These tests call `pickTechniqueChoice` directly, which isolates the picker
    from the surrounding advancement flow — the same direct-injection approach
    TD-10's Strike-banner tests use in this file. When they were written that was
    also a necessity: T9 left the Builder's "Available" list empty, so no real
    click-through existed. T9 is fixed (see
    `TestAdvancementAndSparks::test_available_technique_list_is_populated`), so
    this is now an isolation choice rather than a workaround.
    """

    def _find_technique(self, page, tech_id):
        return page.evaluate(
            """id => {
                for (const facetId in state.ruleset.techniques) {
                    for (const branch of state.ruleset.techniques[facetId].branches) {
                        for (const tier of branch.tiers) {
                            const found = tier.techniques.find(t => t.id === id);
                            if (found) return found;
                        }
                    }
                }
                return null;
            }""",
            tech_id)

    def test_weapon_mastery_choice_reaches_technique_choices_on_the_character(self, table, live_server):
        mm, player = table

        # Grant a Technique pick the only way currently reachable: two Body
        # skill advances cross the 5-rank-advance Facet-level threshold
        # (facet.yaml advancement.facet_level_threshold). Zahna is created
        # with no Background (custom/none is the create-character default in
        # `table`), so both skills start clean at Novice/0 marks — each maxes
        # to Master (3 rank advances) well within the 100 marks sent, and two
        # skills' worth (6 advances) crosses the threshold of 5 for 1 SP each,
        # inside the 4-SP session budget.
        for skill_id in ("athletics", "stealth"):
            mm.evaluate(
                "args => sendWS({type: 'skill_advance', player_name: args.p, "
                "skill_id: args.s, marks: 100})",
                {"p": "Zahna", "s": skill_id})
            mm.wait_for_timeout(400)

        # `technique_picks_available` really is incremented server-side at
        # this point — `character.advance_skill` computed it correctly — but
        # the `skill_advanced` broadcast never carries the field and
        # `app.js`'s handler never applies it to `state.character` (a third,
        # separate pre-existing wiring gap; see docs/TODO.md T10). A reload
        # re-authenticates from the stored token and re-fetches full session
        # state, which — unlike the incremental broadcast — does carry the
        # true value, so this routes around the gap rather than depending on
        # a fix that is out of TD-20's scope. A plain reload would re-run the
        # invite-join flow instead, since the page URL still carries the
        # invite token query param that takes precedence over sessionStorage
        # (app.js's DOMContentLoaded routing) — going to the bare origin
        # avoids that and falls into the stored-token branch.
        player.goto(live_server)
        player.wait_for_selector("#game-screen:not(.hidden)", timeout=10000)
        player.wait_for_timeout(500)

        picks = player.evaluate("() => state.character.technique_picks_available")
        assert picks >= 1, "skill advance did not grant a Technique pick"

        weapon_mastery = self._find_technique(player, "weapon_mastery")
        assert weapon_mastery is not None
        assert weapon_mastery["choices"] == ["blades", "blunt", "polearms", "unarmed"]

        # Kick off the real picker without awaiting it in-page — the Promise
        # only resolves once the dialog's Confirm button is clicked, below.
        player.evaluate(
            "def => { window.__pickResult = undefined; "
            "pickTechniqueChoice(def).then(r => { window.__pickResult = r; }); }",
            weapon_mastery)
        player.wait_for_selector(".modal-input", timeout=5000)

        option_values = player.eval_on_selector_all(".modal-input option", "els => els.map(e => e.value)")
        assert option_values == ["blades", "blunt", "polearms", "unarmed"], (
            "picker did not offer Weapon Mastery's own choices — "
            f"got {option_values}")

        player.select_option(".modal-input", "blades")
        player.click("button[data-act='ok']")
        player.wait_for_function("() => window.__pickResult !== undefined", timeout=5000)
        resolved = player.evaluate("() => window.__pickResult")
        assert resolved == "blades"

        # `selectTechnique` would send exactly this once its own `def` lookup
        # (docs/TODO.md T9) is fixed; sending it here proves the resolved
        # choice — not just the dialog's local state — is what reaches the
        # character over the real `technique_select` WS handler.
        player.evaluate(
            "choice => sendWS({type: 'technique_select', technique_id: 'weapon_mastery', choice})",
            resolved)
        player.wait_for_timeout(500)

        # `onTechniqueSelected` (app.js) never applies `msg.choice` to
        # `state.character.technique_choices` — a fourth pre-existing wiring
        # gap alongside T9/T10 (docs/TODO.md T11). The character's stored
        # `technique_choices` is correct server-side regardless (`Character
        # .select_technique`, `character.py:402`); fetch it the same way as
        # the picks-available check above rather than trust the incremental
        # broadcast handler this test is not about.
        player.goto(live_server)
        player.wait_for_selector("#game-screen:not(.hidden)", timeout=10000)
        player.wait_for_timeout(500)

        techniques = player.evaluate("() => state.character.techniques")
        choices = player.evaluate("() => state.character.technique_choices")
        assert "weapon_mastery" in techniques
        assert choices["weapon_mastery"] == "blades"

    def test_domain_granting_technique_keeps_the_domain_list_behaviour(self, table):
        """A Technique with no `choices` — every domain-granting one; TD-19
        gave `choices` to exactly the three non-domain Techniques — must
        still get the pre-existing domain-list picker, not an empty result."""
        _, player = table
        arcane_study = self._find_technique(player, "arcane_study")
        assert arcane_study is not None
        assert arcane_study.get("choices") is None

        player.evaluate(
            "def => { window.__pickResult2 = undefined; "
            "pickTechniqueChoice(def).then(r => { window.__pickResult2 = r; }); }",
            arcane_study)
        player.wait_for_selector(".modal-input", timeout=5000)

        option_labels = player.eval_on_selector_all(".modal-input option", "els => els.map(e => e.textContent)")
        # Domain options render as "Name (type)" (the pre-existing branch) —
        # never a bare weapon/hardship/field string, which is what a wrongly
        # taken `choices` fallback would produce instead.
        assert option_labels, "domain picker offered no options"
        assert all("(" in label and ")" in label for label in option_labels)

        player.click("button[data-act='cancel']")


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


class TestSceneAndCombatControls:
    """Review finding: `endScene()` was inserted inside `endCombat()`'s body and
    took two statements with it, so End Combat silently stopped clearing the
    enemy tracker — while its own confirm dialog still promised to. The server
    never touches `active_enemies` on `combat_end`, so the client-side clear was
    the only thing emptying that panel."""

    def test_end_combat_clears_the_enemy_tracker(self, table):
        mm, _ = table
        mm.evaluate("state.activeEnemies = {'boss_0': {name: 'Boss', tier: 'boss'}}")
        # Drive the real function, auto-accepting its confirm.
        mm.evaluate("window.confirmDialog = async () => true")
        mm.evaluate("endCombat()")
        mm.wait_for_timeout(400)
        assert mm.evaluate("Object.keys(state.activeEnemies).length") == 0

    def test_end_scene_leaves_the_enemy_tracker_alone(self, table):
        """Ending a scene is not ending a fight — B6 keeps them separate on
        purpose, so End Scene must not quietly do End Combat's job."""
        mm, _ = table
        mm.evaluate("state.activeEnemies = {'boss_0': {name: 'Boss', tier: 'boss'}}")
        mm.evaluate("window.confirmDialog = async () => true")
        mm.evaluate("endScene()")
        mm.wait_for_timeout(400)
        assert mm.evaluate("Object.keys(state.activeEnemies).length") == 1
