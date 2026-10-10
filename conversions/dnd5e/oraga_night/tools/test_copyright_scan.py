"""Tests for copyright_scan.py, the 8-word shingle scan (review-fix task R6.1).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q

Every fixture is synthetic text written for the test; no official wording is used.
"""
import hashlib
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import copyright_scan as C  # noqa: E402

PHRASE = "the copper kettle sang a tune nobody in the village knew"


def setup(tmp_path, module_text, ref_text, srd_text="", allow=""):
    mod, refs, srd = tmp_path / "mod", tmp_path / "refs", tmp_path / "srd"
    for d in (mod, refs, srd):
        d.mkdir()
    (mod / "01_Test.md").write_text(module_text, encoding="utf-8")
    (refs / "BookA.txt").write_text(ref_text, encoding="utf-8")
    (srd / "SRD.txt").write_text(srd_text, encoding="utf-8")
    allow_path = tmp_path / "allow.txt"
    allow_path.write_text(allow, encoding="utf-8")
    (a, b, c), _, _ = C.run(mod, refs, [srd], allow_path)
    return a, b, c


class TestNormalize:
    def test_case_punctuation_and_apostrophes(self):
        assert C.normalize("The Guard’s DC-15 check!") == ["the", "guards", "dc", "15", "check"]

    def test_pdf_hyphenation_rejoined(self):
        assert C.normalize("charac-\nters walk") == ["characters", "walk"]

    def test_markdown_emphasis_stripped_from_segments(self):
        segs = C.segments("The **copper** kettle sang a *tune* nobody in the village knew.\n",
                          "01_Test.md")
        assert segs[0].words == C.normalize(PHRASE)


class TestScan:
    def test_shared_sentence_is_a_class_c_hit_with_page(self, tmp_path):
        ref = "=== PAGE 1 ===\nfiller\n=== PAGE 7 ===\nOnce, " + PHRASE + ", they said.\n"
        a, b, c = setup(tmp_path, "Intro line.\n\n" + PHRASE.capitalize() + ".\n", ref)
        assert not a and not b and len(c) == 1
        assert c[0].line == 3 and ("BookA", 7) in c[0].sources
        assert c[0].run == PHRASE  # overlapping shingles merge into one run

    def test_clean_module_has_no_hits(self, tmp_path):
        a, b, c = setup(tmp_path, "A wholly different sentence about lanterns and a bridge.\n",
                        "=== PAGE 1 ===\n" + PHRASE + "\n")
        assert (a, b, c) == ([], [], [])

    def test_seven_shared_words_are_below_threshold(self, tmp_path):
        seven = "one two three four five six seven"
        a, b, c = setup(tmp_path, f"Then {seven} and more words follow here.\n", seven)
        assert c == []

    def test_wrapped_line_still_matches(self, tmp_path):
        text = "The copper kettle sang a tune\nnobody in the village knew.\n"
        _, _, c = setup(tmp_path, text, PHRASE)
        assert len(c) == 1 and c[0].line == 1

    def test_srd_text_is_class_a(self, tmp_path):
        a, b, c = setup(tmp_path, PHRASE + ".\n", PHRASE, srd_text=PHRASE)
        assert len(a) == 1 and not c

    def test_allowlisted_hash_is_class_b_only_for_its_file(self, tmp_path):
        h = hashlib.sha1(PHRASE.encode()).hexdigest()
        a, b, c = setup(tmp_path, PHRASE + ".\n", PHRASE, allow=f"{h} | 01_Test.md | (b) test\n")
        assert len(b) == 1 and not c
        other = tmp_path / "other"
        other.mkdir()
        a, b, c = setup(other, PHRASE + ".\n", PHRASE, allow=f"{h} | 99_Other.md | (b) test\n")
        assert not b and len(c) == 1

    def test_excluded_files_are_not_scanned(self, tmp_path):
        mod = tmp_path / "m"
        mod.mkdir()
        (mod / "STYLE_5e.md").write_text(PHRASE + ".\n", encoding="utf-8")
        assert C.load_module(mod) == []


class TestAllowAndCli:
    def test_malformed_allow_line_raises(self, tmp_path):
        p = tmp_path / "allow.txt"
        p.write_text("not-a-hash | 01_Test.md | why\n", encoding="utf-8")
        with pytest.raises(ValueError):
            C.load_allow(p)

    def test_check_exits_1_on_class_c(self, tmp_path, capsys):
        setup(tmp_path, PHRASE + ".\n", PHRASE)
        rc = C.main(["--refs", str(tmp_path / "refs"), "--srd", str(tmp_path / "srd"),
                     "--module", str(tmp_path / "mod"), "--allow", str(tmp_path / "allow.txt"),
                     "--check"])
        assert rc == 1 and "(c) to review 1" in capsys.readouterr().out

    def test_missing_refs_dir_is_an_error(self, tmp_path):
        with pytest.raises(SystemExit):
            C.main(["--refs", str(tmp_path / "nope")])
