"""Tests for lint_5e.py, the Oraga Night 5e style linter (DESIGN_oraga_5e_official §4).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q

Every rule family has at least three tests: a hit, a clean miss, and an edge case
(a read-aloud skip, a whitelist, a capitalized or compressed form).
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import lint_5e as L  # noqa: E402

FIX = TOOLS / "fixtures"
FIX_MODULE = FIX / "module"


def fam(text, family, fname="04_The_Ball.md", allow=()):
    """Matched strings for one hard family."""
    return [h.match for h in L.lint_hard(text, fname, allow) if h.family == family]


def box(*lines):
    """An indented italic read-aloud block after a trigger line."""
    body = "\n".join("> " + x for x in lines)
    return "Read this when the doors open:\n\n" + body + "\n"


# --------------------------------------------------------------------------- line classes

class TestClassify:
    def test_readaloud_block_is_whole_block(self):
        kinds = L.classify("Read this:\n\n> *One line,\n> and its tail.*\n\nPlain.\n")
        assert kinds == ["prose", "blank", "readaloud", "readaloud", "blank", "prose"]

    def test_bold_sidebar_is_prose(self):
        kinds = L.classify("> **DM Note — a thing**\n>\n> Text here.\n")
        assert kinds[0] == "prose" and kinds[2] == "prose"

    def test_italic_paragraph_inside_sidebar_is_skipped(self):
        kinds = L.classify("> **Wants.** Nothing.\n> *Made, not born.*\n")
        assert kinds == ["prose", "readaloud"]

    def test_tables_headings_rules(self):
        kinds = L.classify("# Title\n\n| a | b |\n|---|---|\n\n---\n")
        assert kinds == ["heading", "blank", "table", "table", "blank", "rule"]

    def test_statblock_runs_to_rule(self):
        text = ("### Bought Blade\n*Medium Humanoid*\n\n**AC** 16\n**HP** 22 (4d8 + 4)\n\n"
                "Some trait text.\n\n---\n\nAfter the block.\n")
        kinds = L.classify(text, "10_Bestiary.md")
        assert kinds[0] == "heading"
        assert all(k in ("statblock", "blank") for k in kinds[1:7])
        assert kinds[-1] == "prose"

    def test_statblock_with_epithet_line_and_comment(self):
        # T4.4: the epithet sits on its own line above the type line, and a TODO comment
        # can follow the type line; the AC line is then seven lines below the heading.
        text = ("### The Hollow\n*The blank gray mask.*\n\n*Medium Humanoid (Human)*\n"
                "<!-- TODO-Q18: alignment pending. -->\n\n**AC** 16\n**HP** 157 (21d8 + 63)\n")
        kinds = L.classify(text, "10_Bestiary.md")
        assert kinds[1] == "statblock" and kinds[6] == "statblock"

    def test_h3_without_ac_is_not_statblock(self):
        kinds = L.classify("### The Palace on Alert\n\nPlain prose here.\n", "10_Bestiary.md")
        assert kinds[2] == "prose"


# --------------------------------------------------------------------------- hard rules

class TestRoleName:
    def test_hit_mm(self):
        assert fam("The MM decides.", "role_name") == ["MM"]

    def test_hit_mirror_master(self):
        assert fam("ask the Mirror Master", "role_name") == ["Mirror Master"]

    def test_miss_dm_and_mmm(self):
        assert fam("The DM decides. MMM is a noise. HMM.", "role_name") == []

    def test_edge_inside_readaloud_still_hits(self):
        assert fam(box("*the MM smiles*"), "role_name") == ["MM"]

    def test_edge_heading_hits(self):
        assert fam("# VIII. The MM Sheet", "role_name") == ["MM"]


class TestLowercaseTerms:
    def test_hit_advantage(self):
        assert fam("They have advantage on the check.", "lowercase_terms") == ["advantage"]

    def test_hit_rests_and_points(self):
        got = fam("After a short rest they regain hit points.", "lowercase_terms")
        assert got == ["short rest", "hit points"]

    def test_hit_condition_and_prone(self):
        got = fam("it has the prone condition; a target is knocked prone", "lowercase_terms")
        assert got == ["prone condition", "knocked prone"]

    def test_hit_action_and_speed(self):
        got = fam("It takes the dash action at half its speed.", "lowercase_terms")
        assert got == ["dash action", "its speed"]

    def test_miss_capitalized(self):
        text = ("They have Advantage. Hit Points 22. A Short Rest. Difficult Terrain. "
                "It has the Prone condition and takes the Dash action; Bloodied.")
        assert fam(text, "lowercase_terms") == []

    def test_miss_inside_word(self):
        assert fam("An advantageous seat; disadvantaged heirs.", "lowercase_terms") == []

    def test_miss_english_idiom(self):
        text = "She takes advantage of the noise, to their advantage, at a disadvantage."
        assert fam(text, "lowercase_terms") == []

    def test_edge_readaloud_skipped(self):
        assert fam(box("*You have the advantage of height.*"), "lowercase_terms") == []

    def test_edge_quoted_speech_skipped(self):
        assert fam('He says, "Press your advantage on him."', "lowercase_terms") == []


class TestBareDC:
    def test_hit_bare(self):
        assert fam("The lock is DC 18 with thieves' tools.", "bare_dc") == ["DC 18"]

    def test_hit_range(self):
        assert fam("Standard is DC 13–15 here.", "bare_dc") == ["DC 13–15"]

    def test_hit_skill_without_ability(self):
        assert fam("a DC 15 Insight check", "bare_dc") == ["DC 15 Insight check"]

    def test_hit_missing_check(self):
        got = fam("- Get between them: DC 13 Strength (Athletics).", "bare_dc")
        assert got == ["DC 13 Strength (Athletics)"]

    def test_miss_full_forms(self):
        text = ("a DC 15 Wisdom (Insight) check; a DC 15 Strength or Dexterity saving throw; "
                "a DC 15 Intelligence (Religion) or DC 15 Charisma (Persuasion) check; "
                "a DC 18 Charisma check; spell save DC 14.")
        assert fam(text, "bare_dc") == []

    def test_miss_statblock_saving_throw_form(self):
        assert fam("***Put Aside.*** *Strength Saving Throw:* DC 14, each creature", "bare_dc") == []

    def test_edge_table_compression_allowed(self):
        text = "| Who | Check |\n|---|---|\n| Corval | 13 Charisma (Persuasion) |\n| Gate | DC 13 |\n"
        assert fam(text, "bare_dc") == []

    def test_edge_table_range_still_hits(self):
        text = "| Who | Check |\n|---|---|\n| Gate | DC 13–15 |\n"
        assert fam(text, "bare_dc") == ["DC 13–15"]


class TestRollCheck:
    def test_hit_roll_ability(self):
        assert fam("Have them roll Wisdom.", "roll_check") == ["roll Wisdom"]

    def test_hit_skill_roll_and_beat(self):
        got = fam("An Insight roll that beats the DC wins.", "roll_check")
        assert got == ["Insight roll", "beats the DC"]

    def test_hit_roll_the_ability(self):
        assert fam("roll the ability and skill that fit", "roll_check") == ["roll the ability"]

    def test_miss(self):
        assert fam("Make a DC 13 Wisdom (Insight) check. Roll initiative.", "roll_check") == []

    def test_edge_readaloud_skipped(self):
        assert fam(box("*The dice roll Wisdom across the floor.*"), "roll_check") == []


class TestSaveDamage:
    def test_hit_save_and_failed_saving_throw(self):
        got = fam("make a DC 13 Dexterity save; on a failed saving throw", "save_damage")
        assert got == ["make a DC 13 Dexterity save", "on a failed saving throw"]

    def test_hit_bare_dice_and_missing_type(self):
        got = fam("It takes 2d6 damage. It deals 7 (2d6) damage.", "save_damage")
        assert got == ["takes 2d6", "7 (2d6) damage"]

    def test_hit_lowercase_type_and_half(self):
        got = fam("7 (2d6) fire damage, half on a success", "save_damage")
        assert got == ["7 (2d6) fire damage", "half on a success"]

    def test_miss(self):
        text = ("must succeed on a DC 13 Dexterity saving throw or take 7 (2d6) Fire damage, "
                "or half as much damage on a successful one.")
        assert fam(text, "save_damage") == []

    def test_edge_fall_keeps_bare_dice(self):
        assert fam("A creature pushed over the rail falls and takes 1d6 Bludgeoning damage.",
                   "save_damage") == []


class TestConversionTalk:
    def test_hit(self):
        got = fam("Heroic Inspiration replaces the original's Sparks in this edition.", "conversion_talk")
        assert got == ["the original", "this edition"]

    def test_hit_source_ch(self):
        assert fam("(source Ch. III) New in this edition:", "conversion_talk") == ["(source Ch", "New in this edition"]

    def test_miss(self):
        assert fam("The light has no visible origin.", "conversion_talk") == []

    def test_edge_whitelisted(self):
        allow = [L.AllowEntry("04_The_Ball.md", "the source of the light", "in-world")]
        assert fam("He finds the source of the light.", "conversion_talk", allow=allow) == []


class TestNarratorVoice:
    def test_hit_module(self):
        assert fam("The module would rather you improvise.", "narrator_voice") == ["The module would"]

    def test_hit_honest(self):
        assert fam("**Honest note.** It is hard.", "narrator_voice") == ["Honest note"]

    def test_miss(self):
        assert fam("This adventure is built for four characters.", "narrator_voice") == []

    def test_edge_other_verb(self):
        assert fam("the module contains seven Movements", "narrator_voice") == []


class TestDesignerWe:
    def test_hit(self):
        assert fam("We suggest you open on the street.", "designer_we") == ["We"]

    def test_hit_our(self):
        assert fam("In our playtests it ran long.", "designer_we") == ["our"]

    def test_miss(self):
        assert fam("You open on the street. Use US Letter paper.", "designer_we") == []

    def test_edge_quoted_and_readaloud(self):
        text = 'Raunu says, "We are honored."\n\n' + box("*We walk on.*")
        assert fam(text, "designer_we") == []


class TestDeadlyBudget:
    def test_hit(self):
        assert fam("*Budget:* 2,400 XP — Deadly.", "deadly_budget") == ["Deadly"]

    def test_miss_lowercase(self):
        assert fam("A deadly blade; 1,000 XP, Low.", "deadly_budget") == []

    def test_edge_not_a_budget_line(self):
        assert fam("The Deadly Nightshade is a tavern.", "deadly_budget") == []


class TestPCs:
    def test_hit(self):
        assert fam("The PCs arrive.", "pcs") == ["PCs"]

    def test_hit_singular(self):
        assert fam("one PC at a time", "pcs") == ["PC"]

    def test_miss(self):
        assert fam("The characters arrive at the PCB plant.", "pcs") == []


class TestSpelledDistance:
    def test_hit(self):
        assert fam("a twelve-foot drop and thirty feet away", "spelled_distance") == ["twelve-foot", "thirty feet"]

    def test_miss_numerals(self):
        assert fam("a 12-foot drop and 30 feet away", "spelled_distance") == []

    def test_edge_readaloud_keeps_words(self):
        assert fam(box("*The wall is twenty feet high.*"), "spelled_distance") == []


class TestGP:
    def test_hit(self):
        assert fam("The fee is 30 gp.", "gp") == ["gp"]

    def test_miss(self):
        assert fam("The fee is 30 GP; a gpu is not coin.", "gp") == []

    def test_edge_table(self):
        assert fam("| Item | Cost |\n|---|---|\n| Mask | 5 gp |\n", "gp") == ["gp"]


class TestBritish:
    def test_hit(self):
        assert fam("A rumour about the colour of the centre.", "british_spelling") == ["rumour", "colour", "centre"]

    def test_hit_verbs(self):
        assert fam("She recognises it; it is labelled.", "british_spelling") == ["recognises", "labelled"]

    def test_miss(self):
        assert fam("A rumor about the color of the center; honor; favor.", "british_spelling") == []

    def test_edge_readaloud_still_hits(self):
        assert fam(box("*Her honour is intact.*"), "british_spelling") == ["honour"]


class TestGrey:
    def test_hit(self):
        assert fam("three grey masks", "grey") == ["grey"]

    def test_miss(self):
        assert fam("three gray masks; greyhound", "grey") == []

    def test_edge_whitelist(self):
        allow = [L.AllowEntry("10_Bestiary.md", "grey robes", "INVENTIONS #43")]
        assert fam("in grey robes", "grey", fname="10_Bestiary.md", allow=allow) == []
        assert fam("in grey robes", "grey", fname="04_The_Ball.md", allow=allow) == ["grey"]


class TestDesignersNote:
    def test_hit(self):
        assert fam("**Designer's note.** Why.", "designers_note") == ["Designer's note"]

    def test_hit_curly(self):
        assert fam("Designer’s Note:", "designers_note") == ["Designer’s Note"]

    def test_miss(self):
        assert fam("**DM Note —** Why.", "designers_note") == []


class TestAttendantHabit:
    def test_hit(self):
        assert fam("it answers any direct question", "attendant_habit") == ["direct question"]

    def test_hit_truthful(self):
        assert fam("answers literally and truthfully", "attendant_habit") == ["literally and truthfully"]

    def test_miss(self):
        assert fam("it names no one, and looks for the master", "attendant_habit") == []


class TestWhitelistFile:
    def test_load_format(self, tmp_path):
        p = tmp_path / "allow.txt"
        p.write_text("# comment\n\n08_Handouts.md|honor to invite you|Handout 1 is canonical\n")
        entries = L.load_allow(p)
        assert entries == [L.AllowEntry("08_Handouts.md", "honor to invite you", "Handout 1 is canonical")]

    def test_bad_line_raises(self, tmp_path):
        p = tmp_path / "allow.txt"
        p.write_text("no pipes here\n")
        with pytest.raises(ValueError):
            L.load_allow(p)

    def test_star_matches_any_file(self):
        allow = [L.AllowEntry("*", "the players", "people at the table")]
        assert L.is_allowed("05_The_Longest_Night.md", "ask the players first", allow)
        assert not L.is_allowed("05_The_Longest_Night.md", "ask the characters", allow)

    def test_shipped_allow_file_has_handout_1(self):
        entries = L.load_allow(TOOLS / "lint_5e_allow.txt")
        assert any(e.file == "08_Handouts.md" and "invite you" in e.text for e in entries)


# --------------------------------------------------------------------------- soft metrics

class TestSentenceLength:
    def test_mean_words(self):
        m = L.soft_metrics("One two three four. Five six.\n", "04_The_Ball.md")
        assert m["sentences"] == 2 and m["mean_wps"] == 3.0

    def test_long_share_counts_semicolon_split(self):
        long_clause = " ".join(["word"] * 31)
        m = L.soft_metrics(f"{long_clause}. Short one.\n", "x.md")
        assert m["long_sentence_pct"] == 50.0
        m2 = L.soft_metrics(" ".join(["word"] * 20) + "; " + " ".join(["word"] * 20) + ".\n", "x.md")
        assert m2["long_sentence_pct"] == 0.0 and m2["sentences"] == 1

    def test_skips_tables_headings_readaloud(self):
        text = ("# A heading with many words in it\n\n| a b c d | e f g |\n|---|---|\n\n"
                + box("*" + " ".join(["word"] * 50) + ".*") + "\nTwo words.\n")
        m = L.soft_metrics(text, "x.md")
        # only "Read this when the doors open:" and "Two words." are prose
        assert m["sentences"] == 2

    def test_abbreviations_do_not_split(self):
        m = L.soft_metrics("It has 30 ft. of reach and e.g. a cloak. Next.\n", "x.md")
        assert m["sentences"] == 2


class TestEmDash:
    def test_rate(self):
        text = " ".join(["word"] * 99) + " — end.\n"
        m = L.soft_metrics(text, "x.md")
        assert m["words"] == 100 and m["emdash_per_k"] == 10.0

    def test_none(self):
        assert L.soft_metrics("No dashes here at all.\n", "x.md")["emdash_per_k"] == 0.0

    def test_readaloud_dash_ignored(self):
        m = L.soft_metrics(box("*a — b — c*") + "\nPlain prose.\n", "x.md")
        assert m["emdash_per_k"] == 0.0


class TestLongParagraphs:
    def test_counts_over_120(self):
        para = " ".join(["word"] * 121) + "."
        assert L.soft_metrics(para + "\n\nShort.\n", "x.md")["long_paras"] == 1

    def test_exactly_120_is_fine(self):
        para = " ".join(["word"] * 120) + "."
        assert L.soft_metrics(para + "\n", "x.md")["long_paras"] == 0

    def test_background_section_excluded(self):
        para = " ".join(["word"] * 150) + "."
        text = "## Adventure Background\n\n" + para + "\n\n## Next\n\n" + para + "\n"
        assert L.soft_metrics(text, "x.md")["long_paras"] == 1

    def test_list_items_are_separate(self):
        item = "- " + " ".join(["word"] * 70) + "."
        assert L.soft_metrics(item + "\n" + item + "\n", "x.md")["long_paras"] == 0


class TestSoftCounts:
    def test_counts(self):
        text = ("The players decide. A player character is hurt. Perhaps you help. "
                "Is it fair? It is not cruel, but kind.\n")
        m = L.soft_metrics(text, "x.md")
        assert (m["the_players"], m["player_character"], m["perhaps"], m["you"],
                m["rhetorical"], m["not_but"]) == (1, 1, 1, 1, 1, 1)

    def test_clean(self):
        m = L.soft_metrics("The characters decide. The DM helps.\n", "x.md")
        assert (m["the_players"], m["player_character"], m["perhaps"], m["you"],
                m["rhetorical"], m["not_but"]) == (0, 0, 0, 0, 0, 0)

    def test_quotes_and_readaloud_excluded(self):
        text = 'He asks, "Do you dance?"\n\n' + box("*Perhaps you see the players?*")
        m = L.soft_metrics(text, "x.md")
        assert (m["you"], m["rhetorical"], m["perhaps"], m["the_players"]) == (0, 0, 0, 0)

    def test_whitelisted_line_excluded(self):
        allow = [L.AllowEntry("x.md", "the players at the table", "people")]
        m = L.soft_metrics("Ask the players at the table.\n", "x.md", allow)
        assert m["the_players"] == 0


# --------------------------------------------------------------------------- structure

def struct(rule=None, module=FIX_MODULE):
    hits = L.lint_structure(module)
    return [h for h in hits if rule is None or h.rule == rule]


class TestXref:
    def test_good_refs_resolve(self):
        # the fixture's chapter V carries only references that resolve
        assert [h for h in struct("xref") if h.file == "05_The_Longest_Night.md"] == []

    def test_bad_chapter_title(self):
        m = [h.match for h in struct("xref")]
        assert any("No Such Section" in x for x in m)

    def test_bad_card_area_table(self):
        m = " | ".join(h.match for h in struct("xref"))
        assert "S99" in m and "B77" in m and "Table IV–9" in m

    def test_good_card_area_table_not_flagged(self):
        m = " | ".join(h.match for h in struct("xref"))
        assert "S1" not in m.replace("S99", "") and "B9" not in m and "Table IV–1" not in m

    def test_missing_chapter(self):
        assert any("chapter xiv" in h.match.lower() for h in struct("xref"))

    def test_multiline_chapter_title_resolves(self):
        assert not any("Seating" in h.match for h in struct("xref"))


class TestCreatureBold:
    def test_unknown_creature_flagged(self):
        assert [h.match for h in struct("creature_bold")] == ["Ghost Pirates"]

    def test_plural_and_article_match(self):
        # "Eight **Feuding Kinsmen**" and "**The Attendant**" resolve to their blocks
        assert not any("Kinsmen" in h.match or "Attendant" in h.match for h in struct("creature_bold"))

    def test_non_creature_bold_ignored(self):
        assert not any(h.match == "Nastier" for h in struct("creature_bold"))

    def test_only_chapters_04_05_09(self):
        assert all(h.file in ("04_The_Ball.md", "05_The_Longest_Night.md", "09_The_Snakes.md")
                   for h in struct("creature_bold"))


class TestReadAloudTrigger:
    def test_missing_trigger_flagged(self):
        hits = [h for h in struct("readaloud_trigger") if h.file == "09_The_Snakes.md"]
        assert len(hits) == 1 and "untriggered" in hits[0].match

    def test_trigger_present_not_flagged(self, tmp_path):
        (tmp_path / "04_The_Ball.md").write_text("# IV. The Ball\n\n" + box("*Fine.*"))
        assert struct("readaloud_trigger", tmp_path) == []

    def test_heading_is_not_a_trigger(self, tmp_path):
        (tmp_path / "04_The_Ball.md").write_text("# IV. The Ball\n\n## Area\n\n> *Box.*\n")
        assert len(struct("readaloud_trigger", tmp_path)) == 1

    def test_trigger_must_be_within_two_lines(self, tmp_path):
        (tmp_path / "04_The_Ball.md").write_text(
            "# IV. The Ball\n\nRead this:\n\n\n\n> *Box.*\n")
        assert len(struct("readaloud_trigger", tmp_path)) == 1

    def test_bold_sidebar_needs_no_trigger(self, tmp_path):
        (tmp_path / "04_The_Ball.md").write_text("# IV. The Ball\n\n## Area\n\n> **DM Note —** text.\n")
        assert struct("readaloud_trigger", tmp_path) == []


# --------------------------------------------------------------------------- CLI, baseline, check

@pytest.fixture
def mod(tmp_path):
    d = tmp_path / "module"
    shutil.copytree(FIX_MODULE, d)
    return d


def cli(mod, *args):
    allow = mod / "allow.txt"
    if not allow.exists():
        allow.write_text("")
    return L.main(["--module", str(mod), "--baseline-path", str(mod / "baseline.json"),
                   "--allow", str(allow), *args])


class TestCLI:
    def test_baseline_writes_json(self, mod, capsys):
        assert cli(mod, "--baseline") == 0
        data = json.loads((mod / "baseline.json").read_text())
        assert set(data) >= {"hard", "soft", "structure"}
        assert data["hard"]["04_The_Ball.md"]["role_name"]["MM"] >= 1

    def test_check_passes_unchanged(self, mod):
        cli(mod, "--baseline")
        assert cli(mod, "--check") == 0

    def test_check_passes_when_hits_go_down(self, mod):
        cli(mod, "--baseline")
        p = mod / "04_The_Ball.md"
        p.write_text(p.read_text().replace("The MM", "The DM", 1))
        assert cli(mod, "--check") == 0

    def test_check_fails_on_new_hard_hit(self, mod, capsys):
        cli(mod, "--baseline")
        p = mod / "04_The_Ball.md"
        p.write_text(p.read_text() + "\nThe PCs leave with 30 gp.\n")
        assert cli(mod, "--check") == 1
        assert "pcs" in capsys.readouterr().out

    def test_check_fails_on_new_structure_hit(self, mod):
        cli(mod, "--baseline")
        p = mod / "04_The_Ball.md"
        p.write_text(p.read_text() + "\nSee card S42.\n")
        assert cli(mod, "--check") == 1

    def test_check_fails_on_soft_regression(self, mod, capsys):
        cli(mod, "--baseline")
        p = mod / "04_The_Ball.md"
        p.write_text(p.read_text() + "\n" + " — ".join(["word"] * 60) + ".\n")
        assert cli(mod, "--check") == 1
        assert "emdash_per_k" in capsys.readouterr().out

    def test_check_fails_on_new_soft_count(self, mod):
        cli(mod, "--baseline")
        p = mod / "04_The_Ball.md"
        p.write_text(p.read_text() + "\nPerhaps the players will notice.\n")
        assert cli(mod, "--check") == 1

    def test_check_without_baseline_errors(self, mod):
        assert cli(mod, "--check") == 2

    def test_report_prints_table(self, mod, capsys):
        assert cli(mod, "--report") == 0
        out = capsys.readouterr().out
        assert "| file |" in out and "04_The_Ball.md" in out and "TOTAL" in out

    def test_file_limits_scope(self, mod, capsys):
        assert cli(mod, "--file", "09_The_Snakes.md") == 0
        out = capsys.readouterr().out
        assert "09_The_Snakes.md" in out and "04_The_Ball.md:" not in out

    def test_excludes_inventions_and_style(self, mod):
        (mod / "INVENTIONS_5e.md").write_text("The MM invented this.\n")
        (mod / "STYLE_5e.md").write_text("Never write MM.\n")
        rep = L.run(mod, allow=[])
        assert not any(h.file in ("INVENTIONS_5e.md", "STYLE_5e.md") for h in rep["hard"])

    def test_real_module_runs_fast(self):
        import time
        t = time.time()
        rep = L.run(L.MODULE, allow=L.load_allow(L.ALLOW))
        assert time.time() - t < 10
        assert "04_The_Ball.md" in rep["soft"]


# --------------------------------------------------------------------------- fixtures

class TestFixtureFiles:
    def test_hard_fixture_hits_every_family(self):
        text = (FIX / "hard_hits.md").read_text()
        got = {h.family for h in L.lint_hard(text, "04_The_Ball.md")}
        assert got == set(L.HARD_FAMILIES)

    def test_clean_fixture_has_no_hard_hits(self):
        text = (FIX / "clean.md").read_text()
        assert L.lint_hard(text, "04_The_Ball.md") == []

    def test_clean_fixture_meets_soft_targets(self):
        m = L.soft_metrics((FIX / "clean.md").read_text(), "04_The_Ball.md")
        assert m["mean_wps"] <= 19 and m["emdash_per_k"] <= 8 and m["long_paras"] == 0
