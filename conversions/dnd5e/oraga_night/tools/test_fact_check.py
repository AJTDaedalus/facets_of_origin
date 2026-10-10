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
                "down_not_out"} <= ids

    def test_shipped_truths_follow_the_rulings(self):
        by = {f["id"]: f for f in F.load_facts(F.FACTS)}
        assert "sixty" in by["household"]["truth"] and "four-fold" in by["household"]["truth"]
        assert "seven go to the dais" in by["honor_guards"]["truth"]
        assert by["bought_company"]["size"]["total"] == 21
        assert by["retinues"]["sizes"]["circle"] == 4 and by["retinues"]["sizes"]["church"] == 4
        assert "dies" in by["maiven_fate"]["truth"]


# --------------------------------------------------------------------------- the real module (the R2 worklist)

class TestRealModule:
    @pytest.fixture(scope="class")
    @staticmethod
    def real():
        return F.check_module(F.MODULE, F.load_facts(F.FACTS))

    def test_expected_first_run_hits(self, real):
        got = {(h.fact, h.file[:2]) for h in real}
        for want in [("household", "02"), ("household", "04"), ("honor_guards", "04"),
                     ("honor_guards", "05"), ("bought_company", "05"), ("arrivals", "01"),
                     ("east_wing_floor", "05"),
                     ("maiven_fate", "06"), ("terraces", "04"), ("terraces", "09")]:
            assert want in got, want

    def test_retinues_agree_after_r1_4(self, real):
        # R1.4 (owner QR3): the Circle and the Church brought four; no hit remains
        assert [h for h in real if h.fact == "retinues"] == []

    def test_no_false_positive_on_ceremony_forty(self, real):
        assert not any(h.fact == "bought_company" and h.file.startswith("04") for h in real)

    def test_down_not_out_has_one_home(self, real):
        assert [h for h in real if h.fact == "down_not_out"] == []

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
