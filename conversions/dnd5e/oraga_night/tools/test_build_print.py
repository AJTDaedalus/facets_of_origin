"""Tests for build_print.py (T9.6–T9.12): Markdown to print-ready HTML for the DM packet,
the player packet, the card deck and the pregenerated character sheets."""
import hashlib
import re
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
MODULE = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import build_print as P  # noqa: E402


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("print")
    paths = P.build_all(MODULE, out)
    return {k: Path(v).read_text(encoding="utf-8") for k, v in paths.items()}


def visible(html):
    """Text a reader sees: data URIs and tags removed."""
    html = re.sub(r"data:[^\"')\s]+", "", html)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)


# --------------------------------------------------------------------------- inline

class TestInline:
    def test_bold_and_italic(self):
        assert P.inline("**a** and *b*") == "<strong>a</strong> and <em>b</em>"

    def test_bold_italic_together(self):
        assert P.inline("***Leashed.*** x") == "<strong><em>Leashed.</em></strong> x"

    def test_escapes_html(self):
        assert P.inline("a < b & c") == "a &lt; b &amp; c"

    def test_code_is_not_formatted(self):
        assert P.inline("`**x**`") == "<code>**x**</code>"

    def test_link_and_image(self):
        assert P.inline("[t](u)") == '<a href="u">t</a>'
        assert P.inline("![alt](pic.png)") == '<img alt="alt" src="pic.png">'

    def test_asterisk_in_a_word_is_left_alone(self):
        assert P.inline("2 * 3 * 4") == "2 * 3 * 4"


# --------------------------------------------------------------------------- blocks

class TestMdToHtml:
    def test_heading_paragraph_and_rule(self):
        html = P.md_to_html("# Title\n\nOne line\nwrapped.\n\n---\n")
        assert '<h1 id="title">Title</h1>' in html
        assert "<p>One line wrapped.</p>" in html
        assert "<hr>" in html

    def test_table(self):
        html = P.md_to_html("| A | B |\n|---|---|\n| 1 | **2** |\n")
        assert "<th>A</th><th>B</th>" in html
        assert "<td>1</td><td><strong>2</strong></td>" in html

    def test_blockquote_holds_a_list(self):
        html = P.md_to_html("> **Box**\n>\n> - one\n> - two\n")
        assert html.startswith("<blockquote>")
        assert "<li>one</li><li>two</li>" in html

    def test_nested_list_and_continuation(self):
        html = P.md_to_html("- top line\n  continued\n  - inner\n- next\n")
        assert "<li>top line continued<ul><li>inner</li></ul></li><li>next</li>" in html

    def test_ordered_list(self):
        assert "<ol><li>a</li><li>b</li></ol>" in P.md_to_html("1. a\n2. b\n")

    def test_comments_are_dropped(self):
        assert "secret" not in P.md_to_html("<!-- secret -->\ntext\n")

    def test_image_becomes_a_figure(self):
        html = P.md_to_html("![Map one](m.svg)\n")
        assert "<figure>" in html and "<figcaption>Map one</figcaption>" in html

    def test_empty_text(self):
        assert P.md_to_html("") == ""


# --------------------------------------------------------------------------- sections

class TestSection:
    TEXT = "# A\n\n## One\nx\n### Sub\ny\n## Two\nz\n"

    def test_takes_subsections(self):
        s = P.section(self.TEXT, "One")
        assert s.startswith("## One") and "### Sub" in s and "## Two" not in s

    def test_matches_on_prefix(self):
        assert P.section(self.TEXT, "Tw").strip().endswith("z")

    def test_missing_heading_is_an_error(self):
        with pytest.raises(KeyError):
            P.section(self.TEXT, "Three")


# --------------------------------------------------------------------------- stripping

class TestStripRepoPaths:
    def test_strips_a_backticked_path(self):
        assert "tools/" not in P.strip_repo_paths("run `tools/build_print.py` now")

    def test_strips_bare_file_names_and_folders(self):
        out = P.strip_repo_paths("see 04_The_Ball.md and conversions/dnd5e/x and INVENTIONS_5e.md")
        assert ".md" not in out and "conversions/" not in out and "INVENTIONS" not in out

    def test_leaves_prose_and_data_uris(self):
        text = "a DC 15 check (see chapter V). ![m](data:image/svg+xml;base64,QUJD/ZGVm)"
        assert P.strip_repo_paths(text) == text


class TestStripDmLines:
    def test_drops_an_italic_paragraph(self):
        out = P.strip_dm_lines("*Hand this over at the gate.*\n\n**1. CARD** — *card text.*\n")
        assert "Hand this over" not in out and "card text" in out

    def test_keeps_italics_inside_a_quote(self):
        out = P.strip_dm_lines("> *To My Esteemed Guest,*\n")
        assert "Esteemed" in out

    def test_drops_a_multiline_italic_paragraph(self):
        out = P.strip_dm_lines("*One line\nand a second line.*\n\nKeep.\n")
        assert out.strip() == "Keep."


class TestSafetyProblems:
    def test_clean_text_has_none(self):
        assert P.safety_problems("A fine invitation.", player=True) == []

    def test_flags_repo_paths_and_inventions(self):
        probs = P.safety_problems("see tools/lint_5e.py and INVENTIONS_5e.md")
        assert len(probs) >= 2

    def test_flags_dm_words_only_for_players(self):
        text = "The Uninvited wait. DM Note — secret."
        assert P.safety_problems(text, player=True)
        assert P.safety_problems(text, player=False) == []

    def test_flags_a_private_word(self):
        planted = {hashlib.sha256(b"zzsecret").hexdigest()}
        assert P.safety_problems("the Zzsecret line", hashes=planted)

    def test_ignores_words_inside_data_uris(self):
        assert P.safety_problems("x data:image/png;base64,VellUninvited y", player=True) == []

    def test_their_is_not_heir(self):
        assert P.safety_problems("their masks", player=True) == []


# --------------------------------------------------------------------------- page and cut

class TestPage:
    def test_is_a_standalone_document(self):
        doc = P.page("T", "<p>x</p>")
        assert doc.startswith("<!DOCTYPE html>") and "<title>T</title>" in doc
        assert "<style>" in doc and "@page" in doc

    def test_escapes_the_title(self):
        assert "<title>A &amp; B</title>" in P.page("A & B", "")

    def test_landscape_option(self):
        assert "landscape" in P.page("T", "", landscape=True)
        assert "landscape" not in P.page("T", "")


class TestCut:
    def test_wraps_in_a_cut_box(self):
        out = P.cut("<p>x</p>")
        assert 'class="cut"' in out and "<p>x</p>" in out

    def test_marks_the_cut_line(self):
        assert "✂" in P.cut("x")

    def test_label_is_escaped(self):
        assert "a &amp; b" in P.cut("x", label="a & b")


# --------------------------------------------------------------------------- data

class TestStatBlocks:
    def test_finds_every_block(self):
        blocks = P.stat_blocks((MODULE / "10_Bestiary.md").read_text(encoding="utf-8"))
        assert "The Attendant" in blocks and "Bought Captain" in blocks and "Master Vell" in blocks
        assert len(blocks) >= 29

    def test_block_ends_before_the_next(self):
        blocks = P.stat_blocks("## The Blocks, A to Z\n### A\na\n### B\nb\n## Items\nz\n")
        assert blocks == {"A": "### A\na\n", "B": "### B\nb\n"}

    def test_no_blocks_is_empty(self):
        assert P.stat_blocks("# nothing\n") == {}


class TestFightCards:
    def test_finds_s1_to_s14(self):
        cards = P.fight_cards((MODULE / "09_The_Snakes.md").read_text(encoding="utf-8"))
        assert list(cards) == [f"S{n}" for n in range(1, 15)]

    def test_card_body_stops_at_next_card(self):
        cards = P.fight_cards("## S1. One\na\n## S2. Two\nb\n")
        assert cards["S1"].strip() == "## S1. One\na"

    def test_no_cards_is_empty(self):
        assert P.fight_cards("## The Snakes\n") == {}


class TestCardBlocks:
    BLOCKS = {"Bought Blade": "", "Bought Captain": "", "Circle Hired Knife": "", "The Attendant": ""}

    def test_plural_names_match(self):
        names = P.card_blocks("Six **Bought Blades** and the **Bought Captain**.", self.BLOCKS)
        assert names == ["Bought Blade", "Bought Captain"]

    def test_knives(self):
        assert P.card_blocks("two **Circle Hired Knives**", self.BLOCKS) == ["Circle Hired Knife"]

    def test_unbolded_names_do_not_count(self):
        assert P.card_blocks("the Attendant watches", self.BLOCKS) == []


class TestPregens:
    def test_five_sheets(self):
        sheets = P.pregen_sheets_md((MODULE / "11_Pregenerated_Characters.md").read_text(encoding="utf-8"))
        assert len(sheets) == 5

    def test_preamble_is_merged_into_each(self):
        sheets = P.pregen_sheets_md((MODULE / "11_Pregenerated_Characters.md").read_text(encoding="utf-8"))
        for name, md in sheets.items():
            assert "Resourceful" in md and "Heroic Inspiration" in md, name
            assert "Masks." in md or "mask" in md.lower(), name

    def test_no_sheets_is_empty(self):
        assert P.pregen_sheets_md("# XI\n\nno sheets\n") == {}


class TestTrackers:
    SHEET = ("**Hit Points** 31 · **Hit Dice** 4d8\n- *Slots:* 1st ×4, 2nd ×3\n"
             "- **Bardic Inspiration** (4 uses, d6; regain on a Long Rest).\n")

    def test_hit_points_and_dice(self):
        t = P.trackers(self.SHEET)
        assert "of 31" in t and "☐☐☐☐" in t

    def test_slots_and_uses(self):
        t = P.trackers(self.SHEET)
        assert "1st-level slots" in t and "2nd-level slots" in t and "Bardic Inspiration" in t

    def test_always_has_heroic_inspiration_and_death_saves(self):
        t = P.trackers("**Hit Points** 10")
        assert "Heroic Inspiration" in t and "Death Saving Throws" in t


class TestSpellLines:
    def test_lists_each_prepared_spell(self):
        lines = P.spell_lines("- *Cantrips:* *Light*, *Mending*\n- *Prepared:* *Bless*\n")
        assert [l.split(".")[0] for l in lines] == ["*Light*", "*Mending*", "*Bless*"]

    def test_unknown_spell_is_an_error(self):
        with pytest.raises(KeyError):
            P.spell_lines("- *Cantrips:* *Wish*\n")

    def test_no_spellcasting_is_empty(self):
        assert P.spell_lines("**Attacks**\n- *Dagger.* +6\n") == []

    def test_every_pregen_spell_has_a_line(self):
        sheets = P.pregen_sheets_md((MODULE / "11_Pregenerated_Characters.md").read_text(encoding="utf-8"))
        for md in sheets.values():
            P.spell_lines(md)          # raises on a gap


# --------------------------------------------------------------------------- packets

class TestBuildAll:
    def test_writes_four_packets(self, built):
        assert sorted(built) == ["card_deck", "dm_packet", "player_packet", "pregen_sheets"]

    def test_every_packet_is_free_of_repo_paths_and_private_words(self, built):
        for name, html in built.items():
            assert P.safety_problems(visible(html)) == [], name

    def test_refuses_to_write_unsafe_player_text(self, tmp_path, monkeypatch):
        real = P.build_player_packet
        monkeypatch.setattr(P, "build_player_packet", lambda m: real(m).replace(
            "</body>", "<p>The Uninvited</p></body>"))
        with pytest.raises(ValueError):
            P.build_all(MODULE, tmp_path)


class TestDmPacket:
    def test_has_sheet_tracker_and_five_maps(self, built):
        html = built["dm_packet"]
        for s in ("Page One", "Page Two", "The Midnight Tracker", "The Palace, Keyed"):
            assert s in html, s
        assert html.count("data:image/svg+xml;base64,") == 5

    def test_is_landscape(self, built):
        assert "landscape" in built["dm_packet"]

    def test_each_sheet_page_starts_a_new_page(self, built):
        assert built["dm_packet"].count('class="sheet-page"') >= 2


class TestPlayerPacket:
    def test_has_every_handout(self, built):
        html = built["player_packet"]
        for n in range(1, 6):
            assert f"Player Handout {n}" in html, n

    def test_no_dm_text(self, built):
        text = visible(built["player_packet"])
        assert P.safety_problems(text, player=True) == []
        for dm_line in ("Put it on the table", "Deal these in the first five minutes",
                        "Give this page to every player", "Reproduce on good paper",
                        "Everything from here to the end"):
            assert dm_line not in text, dm_line

    def test_agenda_cards_have_cut_lines(self, built):
        html = built["player_packet"]
        assert html.count('class="cut"') >= 9          # eight agenda cards and the invitation

    def test_public_room_sketch_is_embedded(self, built):
        assert "data:image/svg+xml;base64," in built["player_packet"]


class TestCardDeck:
    def test_one_page_per_card(self, built):
        assert built["card_deck"].count('class="card"') == 14

    def test_every_card_carries_its_blocks(self, built):
        cards = P.fight_cards((MODULE / "09_The_Snakes.md").read_text(encoding="utf-8"))
        blocks = P.stat_blocks((MODULE / "10_Bestiary.md").read_text(encoding="utf-8"))
        html = built["card_deck"]
        pages = html.split('class="card"')[1:]
        assert len(pages) == 14
        for (cid, md), page_html in zip(cards.items(), pages):
            names = P.card_blocks(md, blocks)
            assert names, cid
            for name in names:
                assert f'data-block="{name}"' in page_html, (cid, name)

    def test_known_cards(self, built):
        pages = dict(zip([f"S{n}" for n in range(1, 15)], built["card_deck"].split('class="card"')[1:]))
        assert 'data-block="The Attendant"' in pages["S14"]
        for n in ("Bought Sergeant", "Bought Captain", "Bought Blade", "Veteran Bought Sergeant"):
            assert f'data-block="{n}"' in pages["S3"], n


class TestPregenSheets:
    def test_five_standalone_sheets(self, built):
        assert built["pregen_sheets"].count('class="pregen"') == 5

    def test_each_sheet_has_trackers_spells_and_a_turn_line(self, built):
        pages = built["pregen_sheets"].split('class="pregen"')[1:]
        for page_html in pages:
            assert "On your turn" in page_html
            assert "Hit Points" in page_html and "☐" in page_html
            assert "Resourceful" in page_html
        casters = [p for p in pages if "Spellcasting" in p]
        assert len(casters) == 3
        for p in casters:
            assert "Spells, one line each" in p

    def test_player_safe(self, built):
        assert P.safety_problems(visible(built["pregen_sheets"]), player=True) == []


class TestMain:
    def test_main_writes_files(self, tmp_path, capsys):
        assert P.main(["--out", str(tmp_path)]) == 0
        assert len(list(tmp_path.glob("*.html"))) == 4

    def test_page_count_of_a_pdf(self, tmp_path):
        pdf = tmp_path / "x.pdf"
        pdf.write_bytes(b"%PDF-1.4\n1 0 obj<</Type /Page>>\n2 0 obj<</Type /Page>>\n"
                        b"3 0 obj<</Type /Pages /Count 2>>\n")
        assert P.pdf_pages(pdf) == 2

    def test_pdf_pages_of_a_missing_file_is_an_error(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            P.pdf_pages(tmp_path / "nope.pdf")
