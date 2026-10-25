"""Tests for fact_check.py, the Oraga Night 5e continuity checker (review-fix task R0.1).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q

Every check type (forbid, sentence, count, size, movement, require) has at least three
tests: a hit, a clean miss, and an edge case (a wrapped line, an `unless`, a file filter,
a noun window). The fixtures cover the four kinds of contradiction the task names: a count,
a floor, a Movement and a size.
"""
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import fact_check as F  # noqa: E402


def facts(*checks, fid="t"):
    return F.validate({"version": 1, "facts": [{"id": fid, "truth": "x", "checks": list(checks)}]})


def hits(text, *checks, fname="04_The_Ball.md"):
    return [h.match for h in F.check_text(text, fname, facts(*checks))]


# --------------------------------------------------------------------------- unwrapping

class TestUnwrap:
    def test_wrapped_phrase_is_found(self):
        text = "Master Vell stands two terraces\nbelow, at the gate.\n"
        assert hits(text, {"type": "forbid", "pattern": r"\btwo terraces below\b"}) == ["two terraces below"]

    def test_hit_reports_the_line_where_the_match_starts(self):
        text = "Line one.\n\nA second paragraph that wraps and then says four-\nfold? No: four-fold here.\n"
        got = F.check_text(text, "02_The_World_and_the_Night.md",
                           facts({"type": "forbid", "pattern": r"\bfour-fold\b"}))
        assert [h.line for h in got] == [4]

    def test_blank_line_splits_paragraphs(self):
        text = "The nine stand at the gate.\n\nLater, the dais is empty.\n"
        chk = {"type": "sentence", "scope": "block", "all": [r"\bnine\b", r"\bdais\b"]}
        assert hits(text, chk) == []

    def test_blockquote_markers_are_stripped(self):
        text = "> *There are nine. At midnight they die\n> on the dais.*\n"
        chk = {"type": "sentence", "scope": "block", "all": [r"\bnine\b", r"\bdais\b"]}
        assert hits(text, chk) == ["nine"]

    def test_context_is_unwrapped(self):
        text = "The palace staff is cut\nfour-fold.\n"
        got = F.check_text(text, "02_x.md", facts({"type": "forbid", "pattern": "four-fold"}))
        assert "cut four-fold" in got[0].context


# --------------------------------------------------------------------------- forbid

class TestForbid:
    def test_hit(self):
        assert hits("The palace staff is cut four-fold.", {"type": "forbid", "pattern": r"\bfour-?fold\b"}) == ["four-fold"]

    def test_miss(self):
        assert hits("The staff was cut by nearly two-thirds.", {"type": "forbid", "pattern": r"\bfour-?fold\b"}) == []

    def test_unless_cancels_in_the_same_sentence(self):
        chk = {"type": "forbid", "pattern": r"\bforty blades\b", "unless": r"\bshould field\b"}
        text = "A house this rich should field forty blades. The hunt is watched by forty blades."
        assert hits(text, chk) == ["forty blades"]

    def test_files_filter(self):
        chk = {"type": "forbid", "pattern": "four-fold", "files": ["02"]}
        assert hits("cut four-fold", chk, fname="04_The_Ball.md") == []
        assert hits("cut four-fold", chk, fname="02_The_World_and_the_Night.md") == ["four-fold"]


# --------------------------------------------------------------------------- sentence

class TestSentence:
    CHK = {"type": "sentence", "all": [r"\bbrought\b", r"\bthree\s+(?:\*\*)?Church Wardens\b"]}

    def test_hit(self):
        assert hits("**Who they brought.** Kovaun and three **Church Wardens**, her escort.", self.CHK) == ["brought"]

    def test_miss_other_sentence(self):
        text = "Kovaun brought her escort. Three **Church Wardens** wait in the chapel."
        assert hits(text, self.CHK) == []

    def test_miss_right_number(self):
        assert hits("Kovaun brought four **Church Wardens**.", self.CHK) == []

    def test_unless(self):
        chk = {"type": "sentence", "all": [r"\bMaiven\b", r"\bwill not leave\b"],
               "unless": r"\b[Ii]f (?:Maiven|she) lived\b"}
        assert hits("Maiven will not leave the city without her cousin.", chk) == ["Maiven"]
        assert hits("If Maiven lived, she will not leave the city without her cousin.", chk) == []

    def test_block_scope_spans_sentences(self):
        chk = {"type": "sentence", "scope": "block", "all": [r"\bnine\b(?!\s+people)", r"\bdais\b"]}
        assert hits("There are nine. At midnight they fall on the dais.", chk) == ["nine"]
        assert hits("A spell at the dais is up to nine people.", chk) == []

    def test_table_row_is_a_block(self):
        chk = {"type": "sentence", "scope": "block", "all": [r"\bnine\b", r"\bdais\b"]}
        text = "| Who | Midnight |\n|---|---|\n| **The nine honor guards** | To the dais, and stay |\n"
        got = F.check_text(text, "08_Handouts.md", facts(chk))
        assert [h.line for h in got] == [3]


# --------------------------------------------------------------------------- count (a count contradiction)

class TestCount:
    CHK = {"type": "count", "noun": r"\b(?:servants|household|staff)\b", "window": 3, "allowed": [60, 22, 24]}

    def test_hit_word_number(self):
        assert hits("A palace this size should hold a hundred servants.", self.CHK) == ["a hundred servants"]

    def test_hit_numeral(self):
        assert hits("The household of 45 servants is gone.", self.CHK) == ["45 servants"]

    def test_miss_allowed(self):
        text = "The household was sixty. Twenty-two staff stayed. He runs it with two dozen staff."
        assert hits(text, self.CHK) == []

    def test_noun_window_avoids_false_positive(self):
        # the number is more than three words before the noun
        assert hits("Nine guards stood at the gate while the household slept.", self.CHK) == []

    def test_one_is_not_a_count(self):
        assert hits("Every one of the household chose to stay.", self.CHK) == []

    def test_compound_number_words(self):
        assert hits("forty-five servants were let go", self.CHK) == ["forty-five servants"]
        assert F.number_value("twenty-two") == 22 and F.number_value("two dozen") == 24


# --------------------------------------------------------------------------- size (a size contradiction)

class TestSize:
    CHK = {"type": "size", "subject": r"\bCrystal Court\b", "window": 90,
           "allowed": {"long": [140], "wide": [80]}}

    def test_hit(self):
        assert hits("The Crystal Court is about 100 feet long and 80 feet wide.", self.CHK) == ["100 feet long"]

    def test_miss(self):
        assert hits("The Crystal Court is about 140 feet long and 80 feet wide.", self.CHK) == []

    def test_hyphenated_form_and_unlisted_dim(self):
        chk = {"type": "size", "subject": r"\bterraces?\b", "window": 70, "allowed": {"drop": [10]}}
        assert hits("Each terrace ends at a 12-foot drop to the next.", chk) == ["12-foot drop"]
        assert hits("Each terrace ends at a 10-foot drop, 3 feet high.", chk) == []

    def test_outside_window_ignored(self):
        text = "The Crystal Court is vast. " + "x " * 60 + "The yard is 100 feet long."
        assert hits(text, self.CHK) == []


# --------------------------------------------------------------------------- movement (a Movement contradiction)

class TestMovement:
    CHK = {"type": "movement", "subject": r"\b(?:the )?(?:Uninvited|Hollow)\b", "from": "III"}

    def test_hit_range(self):
        text = "| The Hollow | watches the servants (B10 edges, Mv II–V) | Holds |\n"
        assert hits(text, self.CHK) == ["Mv II–V"]

    def test_hit_any_movement(self):
        assert hits("The Hollow stands beside a different exit (any Movement).", self.CHK) == ["any Movement"]

    def test_miss_from_three(self):
        text = ("The Uninvited arrive with the Movement III crush. The Hollow's tells come "
                "in Movements III–V (any Movement from III).")
        assert hits(text, self.CHK) == []

    def test_miss_other_subject(self):
        assert hits("Vell is in the line in Movement I.", self.CHK) == []

    def test_roman_parsing(self):
        assert F.roman("III") == 3 and F.roman("VII") == 7
        with pytest.raises(ValueError):
            F.roman("Q")


# --------------------------------------------------------------------------- require (a floor contradiction)

class TestRequire:
    CHK = {"type": "require", "file": "05_The_Longest_Night.md",
           "pattern": r"(?:east doors|east wing)[^\n]{0,300}?(?:rises 12 feet|gallery level)",
           "anchor": r"\*The east wing \(B9\)\*"}

    def _mod(self, tmp_path, text):
        (tmp_path / "05_The_Longest_Night.md").write_text(text)
        return F.check_module(tmp_path, facts(self.CHK))

    def test_hit_missing_reported_at_anchor(self, tmp_path):
        got = self._mod(tmp_path, "# V.\n\n- *The east wing (B9)* is reached by a cleared\n  corridor.\n")
        assert len(got) == 1 and got[0].line == 3 and got[0].kind == "require"

    def test_miss_present_across_a_wrap(self, tmp_path):
        got = self._mod(tmp_path, "- *The east wing (B9)* is up a stair from the Court's east doors that\n"
                                  "  rises 12 feet to gallery level.\n")
        assert got == []

    def test_missing_file_is_not_a_hit(self, tmp_path):
        (tmp_path / "04_The_Ball.md").write_text("Nothing here.\n")
        assert F.check_module(tmp_path, facts(self.CHK)) == []

    def test_no_anchor_reports_line_one(self, tmp_path):
        got = self._mod(tmp_path, "# V.\n\nNo wing here.\n")
        assert got[0].line == 1


# --------------------------------------------------------------------------- rule_copy (R1.2, O36)

class TestRuleCopy:
    CHK = {"type": "rule_copy", "home": "05", "max": 2,
           "elements": [r"\bStable\b", r"\bno Death Saving Throws\b",
                        r"\bwithin 5 (?:feet|ft\.)[^.]{0,80}\baction\b", r"\b1 (?:Hit Point|HP)\b",
                        r"\blast blow\b"]}
    FULL = ("- **Down, Not Out.** Dropped by an Uninvited: Unconscious and Stable, no Death\n"
            "  Saving Throws. Anyone within 5 ft. spends an action and they are up with 1 HP.\n")

    def test_hit_full_restatement_outside_home(self):
        got = F.check_text(self.FULL, "08_Handouts.md", facts(self.CHK))
        assert len(got) == 1 and got[0].kind == "rule_copy" and got[0].line == 1

    def test_miss_in_the_home_file(self):
        assert F.check_text(self.FULL, "05_The_Longest_Night.md", facts(self.CHK)) == []

    def test_miss_pointer_with_local_rule(self):
        text = ("- **Down, Not Out** (see chapter V). Whoever they drop is Stable, and whoever\n"
                "  deals the last blow makes a saving throw.\n")
        assert F.check_text(text, "08_Handouts.md", facts(self.CHK)) == []

    def test_elements_counted_once_each(self):
        text = "Stable, Stable, Stable and Stable again; 1 HP.\n"
        assert F.check_text(text, "09_The_Snakes.md", facts(self.CHK)) == []

    def test_elements_split_across_paragraphs_are_not_a_copy(self):
        text = "Unconscious and Stable, no Death Saving Throws.\n\nWithin 5 feet, an action: 1 HP.\n"
        assert F.check_text(text, "10_Bestiary.md", facts(self.CHK)) == []

    def test_match_names_the_elements_found(self):
        got = F.check_text(self.FULL, "10_Bestiary.md", facts(self.CHK))
        assert got[0].match.startswith("4 of 5 elements")

    def test_needs_elements_and_home(self):
        with pytest.raises(ValueError):
            facts({"type": "rule_copy", "home": "05"})
        with pytest.raises(ValueError):
            facts({"type": "rule_copy", "elements": ["x"]})


# --------------------------------------------------------------------------- loading and validation

class TestFacts:
    def test_unknown_type_raises(self):
        with pytest.raises(ValueError):
            facts({"type": "bogus", "pattern": "x"})

    def test_missing_field_raises(self):
        with pytest.raises(ValueError):
            facts({"type": "count", "noun": "x"})

    def test_bad_regex_raises(self):
        with pytest.raises(ValueError):
            facts({"type": "forbid", "pattern": "(unclosed"})

    def test_duplicate_ids_raise(self):
        with pytest.raises(ValueError):
            F.validate({"version": 1, "facts": [{"id": "a", "truth": "x", "checks": []},
                                                {"id": "a", "truth": "y", "checks": []}]})

    def test_shipped_facts_load_and_cover_the_bible(self):
        ids = {f["id"] for f in F.load_facts(F.FACTS)}
        assert {"household", "honor_guards", "retinues", "bought_company", "arrivals",
                "east_wing_floor", "stairs", "terraces", "room_sizes", "maiven_fate",
                "threat_rule", "fracture_rule"} <= ids
        assert "down_not_out" not in ids  # T5.1: replaced by threat_rule

    def test_shipped_truths_follow_the_rulings(self):
        by = {f["id"]: f for f in F.load_facts(F.FACTS)}
        assert "sixty" in by["household"]["truth"] and "four-fold" in by["household"]["truth"]
        assert "seven go to the dais" in by["honor_guards"]["truth"]
        assert by["bought_company"]["size"]["total"] == 21
        assert by["retinues"]["sizes"]["circle"] == 4 and by["retinues"]["sizes"]["church"] == 4
        assert "dies" in by["maiven_fate"]["truth"]


class TestThreePlayerGuards:
    """T4.1 and T5.1 (three-player pass): the guards fire on the retired wording."""

    @pytest.fixture(scope="class")
    @staticmethod
    def facts():
        return F.load_facts(F.FACTS)

    @staticmethod
    def _hits(facts, text, fname, fid):
        return [h for h in F.check_text(text, fname, facts) if h.fact == fid]

    def test_nothing_bought_is_forbidden(self, facts):
        row = "| *Sleep* | Condition immunities; nothing bought | *Held by Something Else* |\n"
        assert self._hits(facts, row, "10_Bestiary.md", "fracture_rule")

    def test_free_spell_success_is_forbidden(self, facts):
        text = "A spell is a trick like any other: if it lands, that is the success.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "fracture_rule")

    def test_spells_roll_sentence_is_not_a_hit(self, facts):
        text = ("A spell with an attack roll or a saving throw uses that roll, and *Centuries of "
                "Practice* can refuse the save; a spell with neither is a trick check with the "
                "caster's spellcasting ability, DC 13.\n")
        assert not self._hits(facts, text, "10_Bestiary.md", "fracture_rule")

    def test_buying_time_restated_outside_05_is_a_copy(self, facts):
        text = ("A trick earns 1 Delay, DC 15 the second time, never a third time, and an "
                "Uninvited loses at most three turns per scene.\n")
        assert self._hits(facts, text, "09_The_Snakes.md", "fracture_rule")
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "fracture_rule")

    def test_mortal_danger_by_choice_is_forbidden(self, facts):
        text = "A character is only ever in mortal danger by choice.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "threat_rule")

    def test_deadly_but_not_lethal_is_forbidden(self, facts):
        text = "The Attendant is deadly, but not lethal.\n"
        assert self._hits(facts, text, "10_Bestiary.md", "threat_rule")

    def test_threat_rule_restated_outside_05_is_a_copy(self, facts):
        text = ("Marked when it earns Delay three times in one scene; the DM says she looks at "
                "you, properly, for the first time, and the mark lasts the scene.\n")
        assert self._hits(facts, text, "10_Bestiary.md", "threat_rule")

    # T4.5: Stop and End replace "Fracture" as rule terms in 05, 08 and 10
    def test_fracture_as_rule_term_is_forbidden(self, facts):
        text = "A character who lands his Fracture makes the Fracture check.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "fracture_rule")
        assert self._hits(facts, text, "08_Handouts.md", "fracture_rule")

    def test_fractures_heading_pointer_is_not_a_hit(self, facts):
        text = 'Two tells land an End (see chapter V, "The Fractures").\n'
        assert not self._hits(facts, text, "10_Bestiary.md", "fracture_rule")

    def test_fracture_term_outside_owned_files_is_not_scanned(self, facts):
        # 01-04, 06, 07, 09 keep the word until the later sweep (LOG T4.5)
        text = "Her Fracture check is easier once she has seen a tell.\n"
        assert not self._hits(facts, text, "07_Cast_of_the_Ball.md", "fracture_rule")

    def test_stop_rule_restated_outside_05_is_a_copy(self, facts):
        text = ("A Stop is DC 15, +2 per tell, once per scene; an End needs two or more tells, "
                "and a failure by 4 or less still lands.\n")
        assert self._hits(facts, text, "09_The_Snakes.md", "fracture_rule")
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "fracture_rule")

    # T7.4: what seals at midnight (TP28)
    def test_corridor_booms_shut_is_forbidden(self, facts):
        text = "The east wing corridor booms shut somewhere above, sealed from afar.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "midnight_wing_routes")

    def test_sealed_stair_is_forbidden(self, facts):
        text = "At the lights the garden stair is sealed behind her.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "midnight_wing_routes")

    def test_open_stair_beside_sealed_doors_is_not_a_hit(self, facts):
        text = "He takes them by the service stair beside the sealed double doors.\n"
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "midnight_wing_routes")

    def test_anha_passages_as_a_way_in_is_forbidden(self, facts):
        text = "She is reachable only through Agenda 4's errand, Anha's passages, Undercurrent C.\n"
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md", "midnight_wing_routes")

    # T4.10: Veier unmet before the Crossing (TP13, TP41)
    def test_take_veier_in_the_wing_is_forbidden(self, facts):
        row = ("| 5 | **The service door.** Take Veier out through the east wing's service door "
               "into the run | Wisdom (Survival); no check with Anha or any of the household |\n")
        assert self._hits(facts, row, "05_The_Longest_Night.md", "veier_unmet")

    def test_beside_veier_is_forbidden(self, facts):
        text = "It is the one agenda that puts a character beside Veier.\n"
        assert self._hits(facts, text, "11_Pregenerated_Characters.md", "veier_unmet")

    def test_crossing_carry_note_is_exempt(self, facts):
        text = ("A character can carry her (Strength 13 or better) or support her (the Help "
                "action).\n")
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "veier_unmet")

    def test_household_moving_her_is_exempt(self, facts):
        text = "The household moves her through the wing, and nobody stands with Veier but them.\n"
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "veier_unmet")

    # T7.14: the Circle exception beside "never gets out" (TP46)
    def test_pregnancy_secret_requires_both_editions(self, facts):
        by = {f["id"]: f for f in facts}
        files = {c["file"] for c in by["pregnancy_secret"]["checks"] if c["type"] == "require"}
        assert files == {"06_Aftermath.md", "../../../adventures/oraga_night/06_Aftermath.md"}


# --------------------------------------------------------------------------- the real module (the R2 worklist)

class TestRealModule:
    @pytest.fixture(scope="class")
    @staticmethod
    def real():
        return F.check_module(F.MODULE, F.load_facts(F.FACTS))

    def test_module_agrees_after_r2(self, real):
        # R2 (QR1, QR2, QR4, O33–O35, P2-5) worked the first-run list to zero
        assert [(h.file, h.line, h.fact) for h in real] == []

    def test_guard_posts_recorded(self):
        by = {f["id"]: f for f in F.load_facts(F.FACTS)}
        pos = by["honor_guards"]["positions"]
        for key in ("movements_II_to_IV", "movement_V", "midnight"):
            assert sum(pos[key].values()) == 9, key
        assert pos["midnight"] == {"dais": 7, "east_wing_doors": 2}
        assert pos["movement_V"]["east_wing_doors"] == 2 * pos["movements_II_to_IV"]["east_wing_doors"]

    def test_retinues_agree_after_r1_4(self, real):
        # R1.4 (owner QR3): the Circle and the Church brought four; no hit remains
        assert [h for h in real if h.fact == "retinues"] == []

    def test_no_false_positive_on_ceremony_forty(self, real):
        assert not any(h.fact == "bought_company" and h.file.startswith("04") for h in real)

    def test_threat_rule_has_one_home(self, real):
        assert [h for h in real if h.fact == "threat_rule"] == []

    def test_slow_rule_agrees(self, real):
        # T4.1-T4.5: spells roll, the cap, no "nothing bought", Stop and End (no "works once",
        # no DC 18 row)
        assert [h for h in real if h.fact == "fracture_rule"] == []

    def test_excluded_files_not_scanned(self, real):
        assert not any(h.file in ("INVENTIONS_5e.md", "STYLE_5e.md") for h in real)


# --------------------------------------------------------------------------- CLI and baseline

@pytest.fixture
def mod(tmp_path):
    d = tmp_path / "m"
    d.mkdir()
    (d / "02_The_World_and_the_Night.md").write_text("The palace staff is cut four-fold.\n")
    (d / "facts.yaml").write_text(
        "version: 1\nfacts:\n  - id: household\n    truth: sixty\n    checks:\n"
        "      - type: forbid\n        pattern: 'four-?fold'\n")
    return d


def cli(mod, *args):
    return F.main(["--module", str(mod), "--facts", str(mod / "facts.yaml"),
                   "--baseline-path", str(mod / "base.json"), *args])


class TestCLI:
    def test_default_exits_nonzero_on_hits(self, mod, capsys):
        assert cli(mod) == 1
        out = capsys.readouterr().out
        assert "02_The_World_and_the_Night.md:1" in out and "four-fold" in out

    def test_default_exits_zero_when_clean(self, mod):
        (mod / "02_The_World_and_the_Night.md").write_text("Cut by nearly two-thirds.\n")
        assert cli(mod) == 0

    def test_report_lists_counts_per_fact(self, mod, capsys):
        assert cli(mod, "--report") == 1
        out = capsys.readouterr().out
        assert "| household | 1 |" in out

    def test_baseline_then_check_passes(self, mod):
        assert cli(mod, "--baseline") == 0
        data = json.loads((mod / "base.json").read_text())
        assert data["facts"]["household"]["02_The_World_and_the_Night.md"]["four-fold"] == 1
        assert cli(mod, "--check") == 0

    def test_check_fails_on_new_hit(self, mod, capsys):
        cli(mod, "--baseline")
        p = mod / "02_The_World_and_the_Night.md"
        p.write_text(p.read_text() + "\nAnd fourfold again.\n")
        assert cli(mod, "--check") == 1
        assert "NEW" in capsys.readouterr().out

    def test_check_passes_when_hits_go_down(self, mod):
        cli(mod, "--baseline")
        (mod / "02_The_World_and_the_Night.md").write_text("Cut by nearly two-thirds.\n")
        assert cli(mod, "--check") == 0

    def test_check_without_baseline_errors(self, mod):
        assert cli(mod, "--check") == 2


class TestVeierDoorErrand:
    """T7.5 / T7.6 (three-player pass): the door errand guard (TP13, TP27, TP33)."""

    @pytest.fixture(scope="class")
    @staticmethod
    def facts():
        return F.load_facts(F.FACTS)

    @staticmethod
    def _hits(facts, text, fname):
        return [h for h in F.check_text(text, fname, facts) if h.fact == "veier_door_errand"]

    def test_beside_veier_is_forbidden_in_02(self, facts):
        text = "This agenda puts a character beside Veier at the Unmasking.\n"
        assert self._hits(facts, text, "02_The_World_and_the_Night.md")

    def test_dinner_for_two_is_forbidden_in_04(self, facts):
        text = "See \"Dinner for Two (B9)\", below.\n"
        assert self._hits(facts, text, "04_The_Ball.md")

    def test_at_dinner_is_forbidden_in_07(self, facts):
        text = "At dinner, when she asks him for a minute alone, he steps out.\n"
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md")

    def test_the_door_errand_is_not_a_hit(self, facts):
        text = ("The door opens a hand's width and her hand comes through it and takes the "
                "ring. Her face stays unseen.\n")
        assert not self._hits(facts, text, "04_The_Ball.md")

    def test_08_dinner_row_is_forbidden(self, facts):
        """Table VIII–6 now follows TP27/TP33 (WP5 follow-up): 08 is in scope."""
        text = "| Veier | B9 — dinner for two |\n"
        assert self._hits(facts, text, "08_Handouts.md")


class TestRootAttendant:
    """T5.7 (three-player pass): TP17, the Attendant enters the Root unaffected."""

    @pytest.fixture(scope="class")
    @staticmethod
    def facts():
        return F.load_facts(F.FACTS)

    @staticmethod
    def _hits(facts, text, tmp_path):
        (tmp_path / "10_Bestiary.md").write_text(text, encoding="utf-8")
        fact = next(f for f in facts if f["id"] == "root")
        return [h for c in fact["checks"] if c["type"] == "require"
                for h in F._require(fact, c, tmp_path)]

    def test_require_fires_when_the_line_is_missing(self, facts, tmp_path):
        assert self._hits(facts, "### The Attendant\n\nIt follows its three.\n", tmp_path)

    def test_line_present_is_not_a_hit(self, facts, tmp_path):
        text = ("### The Attendant\n\n***Where the Three Go.*** It follows its three "
                "anywhere, the Root included: nothing there touches it.\n")
        assert not self._hits(facts, text, tmp_path)


class TestPolishReviewB:
    """Polish pass B (2026-10-25): TP47 Root trap, TP21 clause, T6.6 crowd scope, TPN-31 freeze."""

    @pytest.fixture(scope="class")
    @staticmethod
    def facts():
        return F.load_facts(F.FACTS)

    @staticmethod
    def _hits(facts, text, fname, fid):
        return [h for h in F.check_text(text, fname, facts) if h.fact == fid]

    @staticmethod
    def _req(facts, fid, fname, text, tmp_path):
        (tmp_path / fname).write_text(text, encoding="utf-8")
        fact = next(f for f in facts if f["id"] == fid)
        return [h for c in fact["checks"] if c["type"] == "require" and c["file"] == fname
                for h in F._require(fact, c, tmp_path)]

    def test_root_refuge_is_forbidden_in_08(self, facts):
        text = "From the Root (B11): shelter for a dozen, and the Uninvited will not enter.\n"
        assert self._hits(facts, text, "08_Handouts.md", "root_trap")

    def test_threshold_they_will_not_cross_is_forbidden_in_10(self, facts):
        text = "and the Root of the House, the one threshold they will not cross.\n"
        assert self._hits(facts, text, "10_Bestiary.md", "root_trap")

    def test_root_trap_wording_is_not_a_hit(self, facts):
        text = ("Guests can shelter in the Root: the Uninvited go only where their errands are, "
                "and they don't know to avoid it.\n")
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "root_trap")

    def test_root_trap_require_fires_without_the_tp18_line(self, facts, tmp_path):
        assert self._req(facts, "root_trap", "05_The_Longest_Night.md",
                         "If the characters found the Root, they hold the master valve.\n", tmp_path)

    def test_send_word_to_the_river_is_forbidden_in_05(self, facts):
        text = "*if a woman in Thenya wool comes out the front, hold her, and send word to the river.*\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "second_clause")

    def test_clause_ending_at_hold_her_is_not_a_hit(self, facts):
        text = "*if a woman in Thenya wool comes out the front, hold her.*\n"
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "second_clause")

    def test_crowd_rule_everywhere_is_forbidden(self, facts):
        text = "The crowd rule in \"Down, Not Out\" holds in every snake fight after the bells.\n"
        assert self._hits(facts, text, "09_The_Snakes.md", "crowd_rule_scope")

    def test_rescue_promise_is_forbidden(self, facts):
        text = "Nobody is out for longer than two rounds.\n"
        assert self._hits(facts, text, "05_The_Longest_Night.md", "crowd_rule_scope")

    def test_no_snake_finishes_is_forbidden(self, facts):
        text = "After midnight no snake finishes a downed character.\n"
        assert self._hits(facts, text, "09_The_Snakes.md", "crowd_rule_scope")

    def test_scoped_crowd_rule_is_not_a_hit(self, facts):
        text = "This is the crowd rule, and it covers only the set-aside.\n"
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "crowd_rule_scope")

    def test_wept_freeze_require_fires_on_a_bare_child_crying(self, facts, tmp_path):
        text = "- **A moment the room gives.** a child crying where the Wept can hear it.\n"
        assert self._req(facts, "wept_freeze", "05_The_Longest_Night.md", text, tmp_path)

    def test_wept_freeze_require_is_met_by_a_real_child(self, facts, tmp_path):
        text = "- **A moment the room gives.** a real child crying where the Wept can hear it.\n"
        assert not self._req(facts, "wept_freeze", "05_The_Longest_Night.md", text, tmp_path)


class TestPolishRulings:
    """Polish review A (three-player pass): guards for TP19, TP21, TP47, TP48, TP52, TP53."""

    @pytest.fixture(scope="class")
    @staticmethod
    def facts():
        return F.load_facts(F.FACTS)

    @staticmethod
    def _hits(facts, text, fname, fid):
        return [h for h in F.check_text(text, fname, facts) if h.fact == fid]

    # TP47 — the Root is a trap, not a refuge
    def test_root_refuge_is_forbidden(self, facts):
        text = "And the Uninvited will not enter it: they will not cross the Root's threshold.\n"
        assert self._hits(facts, text, "04_The_Ball.md", "tp47_root_trap")

    def test_root_safe_room_is_forbidden(self, facts):
        text = "The Root is a safe room that can shelter a dozen guests.\n"
        assert self._hits(facts, text, "04_The_Ball.md", "tp47_root_trap")

    def test_root_trap_wording_is_clean(self, facts):
        text = ("A dozen guests can shelter there: the Uninvited go only where their errands "
                "are. One who crosses its threshold can be caught there.\n")
        assert not self._hits(facts, text, "04_The_Ball.md", "tp47_root_trap")

    def test_root_guard_skips_other_workers_files(self, facts):
        text = "The Uninvited will not cross the Root's threshold.\n"
        assert not self._hits(facts, text, "05_The_Longest_Night.md", "tp47_root_trap")

    # TP21 — the Second Clause ends at "hold her"
    def test_send_word_to_the_river_is_forbidden(self, facts):
        text = '"If a woman in Thenya wool comes out the front, hold her, and send word to the river."\n'
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp21_second_clause")

    def test_clause_ending_at_hold_her_is_clean(self, facts):
        text = '"If a woman in Thenya wool comes out the front, hold her."\n'
        assert not self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp21_second_clause")

    def test_wrapped_send_word_is_caught(self, facts):
        text = "hold her, and send word\nto the river.\n"
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp21_second_clause")

    # TP19 — Vell's sword stays on his back
    def test_fights_with_it_still_bound_is_forbidden(self, facts):
        text = "at the Crossing, where he fights the Radiant with it still bound.\n"
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp19_vell_sword")

    def test_holds_with_sword_still_wrapped_is_forbidden(self, facts):
        text = "where he holds the Radiant with the sword still wrapped.\n"
        assert self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp19_vell_sword")

    def test_sword_on_his_back_is_clean(self, facts):
        text = "where he holds the Radiant off with the sword still on his back.\n"
        assert not self._hits(facts, text, "07_Cast_of_the_Ball.md", "tp19_vell_sword")

    # TP52 — Raunu's line is cut everywhere
    def test_raunu_line_is_forbidden_in_04(self, facts):
        text = 'then: *"She chooses her guests herself these days."*\n'
        assert self._hits(facts, text, "04_The_Ball.md", "tp52_raunu_line")

    def test_raunu_line_is_forbidden_in_09(self, facts):
        text = '*"If she chooses you, you will know."*\n'
        assert self._hits(facts, text, "09_The_Snakes.md", "tp52_raunu_line")

    def test_veier_choosing_the_messenger_is_clean(self, facts):
        text = "If Veier chooses them, and by default she does, the door opens a hand's width.\n"
        assert not self._hits(facts, text, "04_The_Ball.md", "tp52_raunu_line")

    # TP48 — Undercurrent C is not gated on Agenda 4
    def test_agenda_4_gate_is_forbidden(self, facts):
        text = "### Undercurrent C — The Third Plate *(run it if anyone carries Agenda 4)*\n"
        assert self._hits(facts, text, "04_The_Ball.md", "tp48_undercurrent_c")

    def test_prep_box_gate_is_forbidden(self, facts):
        text = "Read Undercurrent C only if someone carries Agenda 4.\n"
        assert self._hits(facts, text, "01_Overture.md", "tp48_undercurrent_c")

    def test_if_you_have_time_is_clean(self, facts):
        text = "### Undercurrent C — The Third Plate *(if you have time)*\n"
        assert not self._hits(facts, text, "04_The_Ball.md", "tp48_undercurrent_c")

    # TP53 — Veier's room is not a find
    def test_three_finds_is_forbidden(self, facts):
        text = "Warm light, a midwife's quiet traffic, and three finds:\n"
        assert self._hits(facts, text, "04_The_Ball.md", "tp53_veier_room")

    def test_veier_rooms_bullet_is_forbidden(self, facts):
        text = "- **Veier's rooms.** Thenya through and through.\n"
        assert self._hits(facts, text, "04_The_Ball.md", "tp53_veier_room")

    def test_two_finds_is_clean(self, facts):
        text = "Nobody gets into her room. Two finds: Raunu's rooms and the nursery.\n"
        assert not self._hits(facts, text, "04_The_Ball.md", "tp53_veier_room")
