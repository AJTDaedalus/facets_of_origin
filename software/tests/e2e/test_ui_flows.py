"""Browser-driven flows for the Lean Facets v1.0 table app.

Drives the real app in Chromium against a live uvicorn process: the MM signs
in, opens a session and invites two players; the players build characters
(a preset caster and a custom class); the MM builds a monster card, starts a
fight and attacks in the open; the players attack and cast; the MM ends the
session and grants a level; a player picks it. Every step asserts that what
the user did changed what they see.

Skipped unless Playwright and its Chromium build are installed:

    pip install playwright && playwright install chromium
"""
from __future__ import annotations

import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

try:
    from playwright.sync_api import expect, sync_playwright
except ImportError as exc:  # pragma: no cover
    pytest.skip(f"Playwright unavailable ({exc}); front-end tests skipped.", allow_module_level=True)

PASSWORD = "e2e-test-password"
SOFTWARE_DIR = Path(__file__).resolve().parents[2]
T = 15000   # ms


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    """A real uvicorn process on its own port and throwaway data directory."""
    port = _free_port()
    data_dir = tmp_path_factory.mktemp("e2e-data")
    env = {**os.environ, "DATA_DIR": str(data_dir), "PORT": str(port), "HOST": "127.0.0.1"}
    log_path = data_dir / "server.log"
    log_file = log_path.open("wb")   # never an undrained pipe: a full pipe wedges uvicorn
    proc = subprocess.Popen([sys.executable, "run.py"], cwd=SOFTWARE_DIR, env=env,
                            stdout=log_file, stderr=subprocess.STDOUT)
    for _ in range(150):
        if proc.poll() is not None:
            pytest.fail(f"server exited early:\n{log_path.read_text(errors='replace')}")
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
    log_file.close()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


class Errors(list):
    def attach(self, page, label):
        page.on("pageerror", lambda e: self.append(f"[{label}] pageerror: {e}"))
        page.on("console", lambda m: self.append(f"[{label}] console.{m.type}: {m.text}")
                if m.type == "error" and "401" not in m.text and "422" not in m.text else None)
        return page


@pytest.fixture(scope="module")
def errors():
    return Errors()


@pytest.fixture(scope="module")
def table(live_server, browser, errors):
    """The MM with an open session, and two joined players (no characters yet)."""
    mm = errors.attach(browser.new_context(viewport={"width": 1440, "height": 1000}).new_page(), "mm")
    mm.goto(live_server)
    mm.click("#btn-show-setup")
    mm.fill("#setup-password", PASSWORD)
    mm.fill("#setup-confirm", PASSWORD)
    mm.click("#btn-setup")
    expect(mm.locator("#auth-ok")).to_contain_text("Password set", timeout=T)
    mm.fill("#mm-password", PASSWORD)
    mm.click("#btn-login")
    expect(mm.locator("#mm-dashboard")).to_be_visible(timeout=T)
    mm.fill("#new-session-name", "Thornwall")
    mm.click("#btn-create-session")
    expect(mm.locator("#session-list")).to_contain_text("Thornwall", timeout=T)

    links = {}
    for player in ("Zahna", "Mordai"):
        mm.fill("#invite-player-name", player)
        mm.click("#btn-invite")
        mm.wait_for_function(f"() => document.querySelector('#invite-result code') && document.querySelector('#invite-result').textContent.includes('{player}')", timeout=T)
        links[player] = mm.locator("#invite-result code").inner_text()

    mm.click("[data-open]")
    expect(mm.locator("#game-screen")).to_be_visible(timeout=T)
    expect(mm.locator("#hdr-conn.online")).to_be_attached(timeout=T)

    players = {}
    for player, url in links.items():
        page = errors.attach(browser.new_context(viewport={"width": 1440, "height": 1000}).new_page(), player)
        page.goto(url)
        page.click("#btn-join")
        expect(page.locator("#game-screen")).to_be_visible(timeout=T)
        expect(page.locator(".wizard")).to_be_visible(timeout=T)
        players[player] = page
    return {"mm": mm, **players, "base": live_server}


def _next(page):
    page.click("[data-wnext]")


SHOTS = SOFTWARE_DIR / "tests" / "_output" / "e2e"


def _shot(page, name):
    """A picture for a human to judge (gitignored); never an assertion."""
    SHOTS.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=True)


def test_wizard_builds_a_preset_caster(table):
    z = table["Zahna"]
    z.click("[data-facet=mind]")
    _shot(z, "wizard_facet")
    _next(z)
    z.click("[data-second=soul]")
    _next(z)
    z.click("[data-class=thaumaturge]")
    _next(z)
    z.click("[data-bg=guild_apprentice]")
    _next(z)
    expect(z.locator(".slot-meter")).to_contain_text("/ 10 slots")
    _next(z)
    z.click("[data-domain=inscription]")
    z.fill("[data-wwork='0']", "A sealing glyph")
    z.fill("[data-wwork='1']", "A warning rune")
    _next(z)
    z.fill("[data-wname]", "Zahna")
    z.click("[data-wcreate]")
    expect(z.locator(".sheet-head h2")).to_have_text("Zahna", timeout=T)
    expect(z.locator(".sheet-sub")).to_contain_text("Level 1 Thaumaturge")
    expect(z.locator(".panel h3", has_text="Magic")).to_be_visible()
    # The MM's party panel shows her too.
    expect(table["mm"].locator(".pc-name", has_text="Zahna")).to_be_visible(timeout=T)


def test_wizard_refuses_to_skip_a_step(table):
    m = table["Mordai"]
    _next(m)
    expect(m.locator("#wiz-err")).to_have_text("Pick a Facet.")


def test_wizard_builds_a_custom_class(table):
    m = table["Mordai"]
    m.click("[data-facet=body]")
    _next(m)
    m.click("[data-second=soul]")
    _next(m)
    m.click("[data-wmode=custom]")
    m.fill("[data-wc=name]", "Wandering Disciple")
    m.fill("[data-wc=concept]", "I am a monk of the open road.")
    m.fill("[data-wc=knack]", "Motion and stillness")
    m.click("[data-wtalent=brawler]")
    m.click("[data-wtalent=weapon_master]")
    m.select_option("[data-wchoice=weapon_master]", "blades")
    _shot(m, "wizard_custom_class")
    _next(m)
    m.click("[data-bg=city_watch_veteran]")
    _next(m)
    for item in ("standard_weapon", "light_armor", "rope", "rations"):
        m.click(f"[data-kitadd={item}]")
    expect(m.locator(".slot-meter")).to_contain_text("4 / 12 slots")
    _next(m)
    m.fill("[data-wname]", "Mordai")
    m.click("[data-wcreate]")
    expect(m.locator(".sheet-sub")).to_contain_text("Wandering Disciple", timeout=T)
    expect(m.locator(".chip", has_text="custom")).to_be_visible()


def test_mm_builds_a_monster_card(table):
    mm = table["mm"]
    mm.click(".tab[data-tab=build]")
    mm.fill("[data-mb=name]", "Chalk Wraith")
    mm.locator("[data-mb=level]").fill("2")
    mm.click("[data-seg=mbRole] button[data-v=elite]")
    expect(mm.locator(".preview-card")).to_contain_text("level 2 elite", timeout=T)
    expect(mm.locator(".preview-card")).to_contain_text("Attacks 2")
    for key, text in (("wants", "Your chalk"), ("special", "Walks through walls"),
                      ("when_bloodied", "It screams"), ("tells", "Dust falls"),
                      ("breaks", "It sinks into the floor")):
        mm.fill(f"[data-mb={key}]", text)
    for i in range(6):
        mm.fill(f"[data-twist='{i}']", f"Twist {i + 1}")
    mm.click("[data-mbsave]")
    expect(mm.locator(".lib-row", has_text="Chalk Wraith")).to_be_visible(timeout=T)


def test_monster_card_refuses_an_incomplete_card(table):
    mm = table["mm"]
    mm.click("[data-mbnew]")
    mm.fill("[data-mb=name]", "Half a card")
    mm.click("[data-mbsave]")
    expect(mm.locator("#mb-err")).to_contain_text("six twists", timeout=T)
    expect(mm.locator("#mb-err")).to_contain_text("WANTS")


def test_combat_round_with_an_enemy_attack(table):
    mm, m, z = table["mm"], table["Mordai"], table["Zahna"]
    mm.click(".lib-row:has-text('Chalk Wraith') [data-libspawn]")
    mm.click(".tab[data-tab=play]")
    expect(mm.locator(".foe-name", has_text="Chalk Wraith")).to_be_visible(timeout=T)
    mm.click("[data-mm=start_combat]")
    expect(mm.locator(".exchange-n")).to_have_text("Exchange 1", timeout=T)
    mm.fill("[data-ui='tg_chalk_wraith']", "claws at Mordai")
    mm.click("[data-tg=chalk_wraith]")
    expect(m.locator("#feed")).to_contain_text("claws at Mordai", timeout=T)

    # Mordai attacks; on a 10+ the option picker opens.
    m.click("[data-actab=attack]")
    m.click("[data-act=attack]")
    m.wait_for_function("() => document.querySelector('.modal') || [...document.querySelectorAll('#feed .entry')].some(e => e.textContent.includes('attacks'))", timeout=T)
    if m.locator(".modal").count():
        m.check("input[name=opt][value=extra_damage]")
        m.click(".modal .btn.primary")
    expect(m.locator("#feed .entry", has_text="attacks Chalk Wraith").last).to_be_visible(timeout=T)
    expect(mm.locator("#feed .entry", has_text="attacks Chalk Wraith").last).to_be_visible(timeout=T)

    # The Wraith attacks Mordai in the open.
    hp_before = m.locator(".hp-top b").first.inner_text()
    mm.select_option("[data-ui='tgt_chalk_wraith']", "Mordai")
    mm.click("[data-eatk=chalk_wraith]")
    expect(m.locator("#feed .entry.foe", has_text="attacks Mordai")).to_be_visible(timeout=T)
    entry = m.locator("#feed .entry.foe", has_text="attacks Mordai").last.inner_text()
    if "Miss" not in entry:
        expect(m.locator(".hp-top b").first).not_to_have_text(hp_before, timeout=T)

    mm.click("[data-mm=end_exchange]")
    expect(mm.locator(".exchange-n")).to_have_text("Exchange 2", timeout=T)
    expect(z.locator("#feed")).to_contain_text("Exchange 2", timeout=T)


def test_casting_pays_fatigue(table):
    z = table["Zahna"]
    z.click("[data-actab=cast]")
    z.click("[data-seg=scope] button[data-v=significant]")
    expect(z.locator("#cast-plan")).to_contain_text("costs 1 Fatigue", timeout=T)
    z.select_option("[data-ui=working]", "A sealing glyph")
    expect(z.locator("#cast-plan")).to_contain_text("signature working", timeout=T)
    z.fill("[data-ui=intent]", "seal the crypt door")
    z.click("[data-act=cast]")
    expect(z.locator("#feed .entry.magic", has_text="seal the crypt door")).to_be_visible(timeout=T)
    expect(z.locator(".slot.fatigue")).to_have_count(1, timeout=T)
    if z.locator(".modal").count():          # a 7-9: choose the cost
        z.click(".modal .btn.magic")


def test_toolbox_stuck_and_reveal(table):
    mm, z = table["mm"], table["Zahna"]
    mm.click("[data-tb=stuck]")
    result = mm.locator(".result", has_text="Threat").first
    expect(result).to_be_visible(timeout=T)
    expect(result).to_contain_text("Arrival")
    expect(result).to_contain_text("Secret")
    mm.click("[data-table=trinkets]")
    expect(mm.locator(".result .kind", has_text="table")).to_be_visible(timeout=T)
    mm.locator("[data-reveal]").first.click()
    expect(z.locator("#feed .entry", has_text="MM reveals")).to_be_visible(timeout=T)


def test_level_up_granted_and_picked(table):
    mm, m = table["mm"], table["Mordai"]
    mm.click("[data-mm=end_combat]")
    mm.click("[data-mm=session_end]")
    expect(mm.locator(".modal")).to_contain_text("Did we discover", timeout=T)
    mm.click(".modal [data-grant=Mordai]")
    mm.click(".modal .actions .btn:not(.primary)")
    expect(m.locator(".banner", has_text="Level up")).to_be_visible(timeout=T)
    m.click(".tab[data-tab=build]")
    expect(m.locator(".banner", has_text="Level 1 → 2")).to_be_visible(timeout=T)
    m.click("[data-lvt=sentinel]")
    _shot(m, "level_up")
    m.click("[data-lvgo]")
    m.click(".tab[data-tab=play]")
    expect(m.locator(".sheet-sub")).to_contain_text("Level 2", timeout=T)
    expect(m.locator(".talent-name", has_text="Sentinel")).to_be_visible()


def test_tools_reference_and_inventory(table):
    z = table["Zahna"]
    z.click(".tab[data-tab=tools]")
    expect(z.locator(".ref .panel h2")).to_have_text("Rolling the dice", timeout=T)
    z.click("[data-ref=talents]")
    z.fill("[data-refsearch]", "sentinel")
    expect(z.locator(".ref-entry:not(.hidden)")).to_have_count(1)
    z.click("[data-tsub=inventory]")
    z.click("[data-invadd=rope]")
    z.click("[data-invsave]")
    z.click(".tab[data-tab=play]")
    expect(z.locator(".slot.item", has_text="Rope")).to_be_visible(timeout=T)


def test_no_front_end_errors(table, errors):
    assert not errors, "front-end errors:\n" + "\n".join(errors)


def test_screenshots(table, tmp_path_factory):
    """Leave a picture of each view for a human to judge (not an assertion)."""
    out = SOFTWARE_DIR / "tests" / "_output" / "e2e"
    out.mkdir(parents=True, exist_ok=True)
    table["mm"].click(".tab[data-tab=play]")
    table["mm"].screenshot(path=str(out / "mm_play.png"), full_page=True)
    table["Zahna"].click(".tab[data-tab=play]")
    table["Zahna"].screenshot(path=str(out / "player_play.png"), full_page=True)
    table["mm"].click(".tab[data-tab=build]")
    table["mm"].screenshot(path=str(out / "mm_build.png"), full_page=True)
