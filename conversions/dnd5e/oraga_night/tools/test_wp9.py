"""WP9 guards (three-player pass): the runtime agrees everywhere it is printed, the prep box
adds up, and the cast cues and handouts stay inside the printed text."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def _mins(hm):
    h, m = hm.split(":")
    return int(h) * 60 + int(m)


def _table_i1():
    """[(start, minutes)] from Table I–1, in order."""
    rows = re.findall(r"^\| (\d:\d\d) \| [^|]+ \| (\d+) \|", _read("01_Overture.md"), re.M)
    return [(_mins(a), int(b)) for a, b in rows]


class TestRuntime:
    def test_table_i1_is_contiguous(self):
        rows = _table_i1()
        assert len(rows) == 10
        for (s1, m1), (s2, _) in zip(rows, rows[1:]):
            assert s1 + m1 == s2

    def test_table_i1_total_matches(self):
        rows = _table_i1()
        total = rows[-1][0] + rows[-1][1]
        m = re.search(r"\*\*(\d) h (\d+) min\*\*", _read("01_Overture.md"))
        assert m and int(m.group(1)) * 60 + int(m.group(2)) == total

    def test_dm_sheet_agrees_with_table_i1(self):
        rows = re.findall(r"^\| (\d:\d\d) \| [^|]*?\((\d+)\) \|", _read("08_Handouts.md"), re.M)
        assert [(_mins(a), int(b)) for a, b in rows] == _table_i1()

    def test_run_boxes_agree(self):
        starts = {s: m for s, m in _table_i1()}
        boxes = re.findall(r"\*\*About (\d+) minutes\*\* \(starts (\d:\d\d)\)",
                           _read("04_The_Ball.md") + _read("05_The_Longest_Night.md"))
        assert len(boxes) == 7
        for mins, start in boxes:
            assert starts[_mins(start)] == int(mins), start

    def test_flow_phases_agree(self):
        flow = json.loads(_read("flow/flow.json"))
        starts = {s: m for s, m in _table_i1()}
        for ph in flow["phases"]:
            m = re.search(r"(\d:\d\d) · (\d+) min", ph["time"])
            assert m, ph["id"]
            assert starts[_mins(m.group(1))] == int(m.group(2)), ph["id"]

    def test_checkpoints_agree(self):
        a = re.search(r"toast has not happened by \*\*(\d:\d\d)\*\*", _read("01_Overture.md"))
        b = re.search(r"the toast by \*\*(\d:\d\d)\*\*", _read("08_Handouts.md"))
        assert a and b and a.group(1) == b.group(1)


class TestPrepBox:
    def _box(self):
        text = _read("01_Overture.md")
        return text[: text.index("## What This Adventure Is")]

    def test_one_hour_path_adds_up(self):
        box = self._box()
        part = box[box.index("**If you have one hour.**"): box.index("**Know these five")]
        mins = [int(m) for m in re.findall(r"\((\d+) minutes\)", part)]
        assert sum(mins) == 60
        assert "That is 60 minutes." in part

    def test_full_read_adds_up(self):
        box = self._box()
        part = box[box.index("**If you have an evening**"):]
        mins = [int(m) for m in re.findall(r"\((\d+) minutes", part)]
        stated = int(re.search(r"That is (\d+) minutes\.", part).group(1))
        assert sum(mins) == stated == 210

    def test_know_these_five_has_five(self):
        box = self._box()
        part = box[box.index("**Know these five"): box.index("**If you have an evening**")]
        assert len(re.findall(r"^> - \*\*", part, re.M)) == 5
        for card in ("S3", "S11", "S12", "S14"):
            assert card in box

    def test_no_dial_in_prep_box(self):
        box = self._box().lower()
        for w in ("gentle", "merciless", "the dial", "every setting"):
            assert w not in box


class TestCastCues:
    def _entries(self):
        text = _read("07_Cast_of_the_Ball.md")
        parts = re.split(r"^### ", text, flags=re.M)[1:]
        return {p.split("\n", 1)[0]: p for p in parts}

    def test_every_entry_has_a_cue(self):
        entries = self._entries()
        assert len(entries) == 18
        for name, body in entries.items():
            assert "**At a glance:**" in body, name
            cue = " ".join(body.split("**At a glance:**", 1)[1].split("\n\n", 1)[0].split())
            assert "At midnight" in cue, name

    def test_cue_comes_first(self):
        for name, body in self._entries().items():
            paras = [p for p in body.split("\n\n")[1:] if p.strip()]
            first = paras[0] if not paras[0].startswith("*") or paras[0].startswith("**") else paras[1]
            assert first.startswith("**At a glance:**"), name

    def test_cue_cards_and_areas_are_printed(self):
        sheet = _read("08_Handouts.md")
        t2 = sheet[sheet.index("**Table VIII–2"): sheet.index("### Page Two")]
        for name, body in self._entries().items():
            cue = body.split("**At a glance:**", 1)[1].split("\n\n", 1)[0]
            rest = body.replace(cue, "")
            for ref in re.findall(r"\b(?:S\d+|B\d+)\b", cue):
                assert ref in rest or ref in t2, (name, ref)


class TestPublicRoomSketch:
    """T9.12: Player Handout 4 draws the public rooms only."""

    @staticmethod
    def _build(tmp_path):
        import sys
        sys.path.insert(0, str(ROOT / "maps"))
        import build_maps as B
        return B, B.build_handouts(tmp_path, png=False)[0]

    def test_builds_a_titled_svg(self, tmp_path):
        import xml.etree.ElementTree as ET
        _, p = self._build(tmp_path)
        r = ET.parse(p).getroot()
        assert r.tag.endswith("svg")
        assert "Player Handout 4: The Public Rooms" in p.read_text(encoding="utf-8")

    def test_no_private_room_or_dm_mark(self, tmp_path):
        _, p = self._build(tmp_path)
        text = " ".join(re.findall(r">([^<]+)</text>", p.read_text(encoding="utf-8")))
        for bad in (r"\bB\d+\b", r"\bS\d+\b", "East Wing", "east wing", "study", "Study",
                    "Kitchen", "kitchen", "Root", "Trophy", "trophy", "mews", "servants",
                    "service", "ward", "seal", "Seal", "held", "dark wing"):
            assert not re.search(bad, text), bad

    def test_committed_copy_matches_the_script(self, tmp_path):
        _, p = self._build(tmp_path)
        committed = ROOT / "maps" / "handout_4_public_rooms.svg"
        assert committed.read_text(encoding="utf-8") == p.read_text(encoding="utf-8")
        assert (ROOT / "maps" / "handout_4_public_rooms.png").stat().st_size > 10_000


class TestCustomsHandout:
    """T9.12: every custom on Player Handout 5 is a printed line."""

    def _handout(self):
        text = _read("08_Handouts.md")
        return text[text.index("### Player Handout 5"): text.index("## The Midnight Tracker")]

    def test_four_customs(self):
        h = self._handout()
        for c in ("**Masks.**", "**Steel.**", "**The Dead Dance.**", "**The Unmasking.**"):
            assert c in h, c

    def test_each_custom_traces_to_printed_text(self):
        src = " ".join((_read("02_The_World_and_the_Night.md") + _read("04_The_Ball.md")).split())
        for phrase in ("the dead of the year, the spirits of the harvest, the luck and grief of the",
                       "nothing said or done behind a spirit's face is entirely yours",
                       "Nobody is disarmed at the door, because nobody is ever disarmed anywhere",
                       "bare steel pointed at a person",
                       "the lamps are lowered, the music turns slow and strange",
                       "with whoever the dark provides, living and dead alike, until the midnight bells",
                       "the masks come off, the spirits are thanked and sent home",
                       "business that cannot stand daylight"):
            assert phrase.lower() in src.lower(), phrase
            assert phrase.split()[1].lower() in " ".join(self._handout().split()).lower()

    def test_no_secret_in_the_customs(self):
        h = self._handout()
        for bad in ("Uninvited", "Veier", "Raunu", r"\bheir\b", r"\bVell\b", "east wing"):
            assert not re.search(bad, h), bad
