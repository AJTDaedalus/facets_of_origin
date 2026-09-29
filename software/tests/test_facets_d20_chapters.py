"""Facets d20 player chapters agree with the data.

The chapters in facets_d20/ are prose; the rules live in facets_d20/data/*.yaml and the
engine in software/facets_d20/. These tests hold the prose to the data (DESIGN v0.2 §4.1:
every talent printed once; §10: presets as cards) without testing wording:

- every talent, Facet feature, knack, background and preset in the yaml is printed exactly
  once as an entry, and nothing is printed as one of those entries that isn't in the yaml;
- each entry carries its key numbers (every die and number in the yaml summary, its 5th and
  9th-level lines, and for Steel/Spell talents the depth those lines need);
- each preset card matches the yaml and the engine's computed HP, AC and attack at 1st;
- the slot tables, the Common list and every domain list in Chapter 07 match the spells yaml;
- the README carries the SRD 5.2.1 attribution (BRIEF §4.6); no "GM"/"DM"; no "D&D";
- every "Chapter NN", file name and "Table N–k" reference resolves.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest
import yaml

from facets_d20 import build as B
from facets_d20 import data as D

REPO = Path(__file__).resolve().parents[2]
BOOK = REPO / "facets_d20"
DATA = BOOK / "data" / "facets_d20.yaml"
SPELLS = BOOK / "data" / "facets_d20_spells.yaml"

# The player book this suite owns. Chapter 09 (the MM's guide) is checked only for
# terminology and references.
PLAYER_FILES = ["README.md", "01_What_Is_Different.md", "02_Characters.md",
                "03_Facet_of_the_Body.md", "04_Facet_of_the_Mind.md",
                "05_Facet_of_the_Soul.md", "06_Backgrounds_Sparks_and_Social.md",
                "07_Magic.md", "08_Combat.md", "10_Quick_Reference.md"]

ATTRIBUTION = (
    'This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") '
    "by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 "
    "is licensed under the Creative Commons Attribution 4.0 International License, "
    "available at https://creativecommons.org/licenses/by/4.0/legalcode."
)

# v0.1 names that must not come back as game objects (ruling 5, V21–V23, signatures cut).
RETIRED = ["Tough", "Deadeye", "Bulwark", "Cleaving Blow", "Ambush", "Beast Heart",
           "Infuse Item", "Clockwork Companion", "Fighting Style", "Survivor",
           "Glimpses", "Twist of Fate", "Well-Timed Word", "Inspiring Word",
           "Studied Eye", "Magic Initiate", "Ability Score Improvement", "Unarmored Discipline"]

ORD = {1: "1st", 2: "2nd", 3: "3rd"}
ENTRY = re.compile(r"^### (?P<name>[^\n]+)\n\*(?P<kind>[^*\n]+)\*[ \t]*\n(?P<body>.*?)(?=^#{1,3} |^---|\Z)",
                   re.M | re.S)
DIE = re.compile(r"(?<![\w])\d*d\d+(?![\w])")
NUM = re.compile(r"(?<![\w/.])\d+(?![\w])|(?<=/)\d+(?![\w])")


def ordinal(n: int) -> str:
    return ORD.get(n, f"{n}th")


def key_numbers(text: str) -> set:
    """Dice and bare numbers in a rules summary; design references like (V24) are not rules."""
    text = re.sub(r"\(V\d+\)|DESIGN §[\d.]+|§[\d.]+", "", text)
    return set(DIE.findall(text)) | set(NUM.findall(DIE.sub(" ", text)))


def tokens(text: str) -> set:
    return set(DIE.findall(text)) | set(NUM.findall(DIE.sub(" ", text)))


# ---------------------------------------------------------------- fixtures

@pytest.fixture(scope="module")
def data():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def spells():
    return yaml.safe_load(SPELLS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def texts():
    return {f: (BOOK / f).read_text(encoding="utf-8") for f in PLAYER_FILES}


@pytest.fixture(scope="module")
def entries(texts):
    """[(file, name, kind line, body)] for every '### Name' + '*kind*' entry."""
    out = []
    for f, t in texts.items():
        for m in ENTRY.finditer(t):
            out.append((f, m["name"].strip(), m["kind"].strip(), m["body"]))
    return out


def of_kind(entries, pred):
    return [e for e in entries if pred(e[2])]


def is_talent(kind):
    return " talent · " in kind


def is_feature(kind):
    return re.fullmatch(r"(Body|Mind|Soul) feature · \d+(st|nd|rd|th) level", kind) is not None


# ---------------------------------------------------------------- talents

class TestTalentEntries:
    def test_every_talent_printed_exactly_once(self, data, entries):
        printed = Counter(n for _, n, k, _ in of_kind(entries, is_talent))
        expected = {t["name"] for t in data["talents"]}
        assert set(printed) == expected, (
            f"missing: {sorted(expected - set(printed))}; not in the yaml: {sorted(set(printed) - expected)}")
        assert all(c == 1 for c in printed.values()), {n: c for n, c in printed.items() if c > 1}

    def test_shared_talents_live_in_chapter_02(self, data, entries):
        where = {n: f for f, n, k, _ in of_kind(entries, is_talent)}
        for t in data["talents"]:
            if len(t["menus"]) > 1:
                assert where[t["name"]] == "02_Characters.md", t["name"]
            else:
                chapter = {"body": "03", "mind": "04", "soul": "05"}[t["menus"][0]]
                assert where[t["name"]].startswith(chapter), t["name"]

    def test_track_and_menus_on_the_type_line(self, data, entries):
        kinds = {n: k for _, n, k, _ in of_kind(entries, is_talent)}
        for t in data["talents"]:
            track = {"steel": "Steel", "spell": "Spell", None: "General"}[t["track"]]
            menus = ", ".join(m.capitalize() for m in t["menus"])
            assert kinds[t["name"]] == f"{track} talent · {menus}", t["name"]

    def test_key_numbers_match_the_yaml(self, data, entries):
        bodies = {n: b for _, n, k, b in of_kind(entries, is_talent)}
        for t in data["talents"]:
            missing = key_numbers(t["summary"]) - tokens(bodies[t["name"]])
            assert not missing, f"{t['name']}: {sorted(missing)} not in the book entry"

    def test_scaling_lines_carry_their_depth(self, data, entries):
        bodies = {n: b for _, n, k, b in of_kind(entries, is_talent)}
        depth = data["tracks"]["scaling_depth"]
        for t in data["talents"]:
            body = bodies[t["name"]]
            for lvl in (t.get("scaling") or {}):
                label = f"**{ordinal(lvl)}"
                if t["track"]:
                    label += f" ({t['track'].capitalize()} {depth[lvl]})"
                assert label + ":**" in body, f"{t['name']}: no '{label}:**' line"
            for lvl in (5, 9):
                if lvl not in (t.get("scaling") or {}):
                    assert f"**{ordinal(lvl)}" not in body, f"{t['name']} prints a {lvl}th line the yaml lacks"

    def test_menu_tables_list_every_talent_on_the_menu(self, data, texts):
        files = {"body": "03_Facet_of_the_Body.md", "mind": "04_Facet_of_the_Mind.md",
                 "soul": "05_Facet_of_the_Soul.md"}
        for facet, f in files.items():
            table = re.search(r"\*\*Table \d–2: \w+ Talents\*\*\n\n(.*?)\n\n", texts[f], re.S).group(1)
            listed = set(re.findall(r"^\| \*([^*]+)\* \|", table, re.M))
            expected = {t["name"] for t in data["talents"] if facet in t["menus"]}
            assert listed == expected, f"{facet}: {sorted(listed ^ expected)}"

    def test_menu_tables_track_column(self, data, texts):
        tracks = {t["name"]: t["track"] or "general" for t in data["talents"]}
        for f in ("03_Facet_of_the_Body.md", "04_Facet_of_the_Mind.md", "05_Facet_of_the_Soul.md"):
            for name, track in re.findall(r"^\| \*([^*]+)\* \| (\w+) \|", texts[f], re.M):
                assert track.lower() == tracks[name], f"{f}: {name}"

    def test_no_retired_talent_is_named(self, texts):
        for f, t in texts.items():
            for name in RETIRED:
                assert f"*{name}*" not in t, f"{f} names the retired {name}"


# ---------------------------------------------------------------- features and ranks

class TestFeaturesAndRanks:
    def test_every_facet_feature_printed_once_with_its_level(self, data, entries):
        printed = Counter((n, k) for _, n, k, _ in of_kind(entries, is_feature))
        expected = {(f["name"], f"{fid.capitalize()} feature · {ordinal(f['level'])} level")
                    for fid, facet in data["facets"].items() for f in facet["features"]}
        assert set(printed) == expected
        assert all(c == 1 for c in printed.values())

    def test_feature_numbers(self, data, entries):
        bodies = {n: b for _, n, k, b in of_kind(entries, is_feature)}
        for facet in data["facets"].values():
            for f in facet["features"]:
                missing = key_numbers(f["summary"]) - tokens(bodies[f["name"]])
                assert not missing, f"{f['name']}: {sorted(missing)}"

    def test_every_rank_named_in_the_depth_table(self, data, texts):
        table = re.search(r"\*\*Table 2–3: What Depth Gives You\*\*\n\n(.*?)\n\n", texts["02_Characters.md"],
                          re.S).group(1)
        for track in ("steel", "spell"):
            for rank in data["tracks"][track]["ranks"]:
                assert table.count(f"**{rank['name']}**") == 1, rank["name"]

    def test_depth_table_numbers(self, data, texts):
        table = re.search(r"\*\*Table 2–3: What Depth Gives You\*\*\n\n(.*?)\n\n", texts["02_Characters.md"],
                          re.S).group(1)
        rows = {int(r[0]): r for r in re.findall(r"^\| (\d)[^|]*\|", table, re.M)}
        assert set(rows) == {1, 2, 3}
        vet = next(r for r in data["tracks"]["steel"]["ranks"] if r["id"] == "veteran")
        assert f"+{vet['effects'][0]['value']} hit point per level" in table
        assert f"+{vet['effects'][1]['value']} damage" in table
        ea = next(r for r in data["tracks"]["steel"]["ranks"] if r["id"] == "extra_attack")
        assert f"from {ordinal(ea['level'])} level" in table

    def test_hit_point_table_follows_the_rule(self, texts):
        rows = re.findall(r"^\| d(\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|",
                          texts["02_Characters.md"], re.M)
        assert len(rows) == 4
        for die, first, per, fifth, tenth in (map(int, r) for r in rows):
            assert first == die + 8                      # V35
            assert per == die // 2 + 1
            assert fifth == first + 4 * per and tenth == first + 9 * per


# ---------------------------------------------------------------- knacks and backgrounds

class TestKnacksAndBackgrounds:
    def test_every_knack_printed_once(self, data, entries):
        printed = Counter(n for _, n, k, _ in of_kind(entries, lambda k: k == "Knack"))
        assert set(printed) == {k["name"] for k in data["knacks"]}
        assert all(c == 1 for c in printed.values())

    def test_knack_numbers(self, data, entries):
        bodies = {n: b for _, n, k, b in of_kind(entries, lambda k: k == "Knack")}
        for k in data["knacks"]:
            missing = key_numbers(k["summary"]) - tokens(bodies[k["name"]])
            assert not missing, f"{k['name']}: {sorted(missing)}"

    def test_every_background_printed_once_as_in_the_yaml(self, data, entries):
        bgs = of_kind(entries, lambda k: k == "Background")
        assert Counter(n for _, n, _, _ in bgs) == Counter(b["name"] for b in data["backgrounds"])
        bodies = {n: b for _, n, _, b in bgs}
        knacks = {k["id"]: k["name"] for k in data["knacks"]}
        full = {"str": "Strength", "dex": "Dexterity", "con": "Constitution",
                "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma"}
        for b in data["backgrounds"]:
            body = bodies[b["name"]]
            assert "**Abilities:** " + ", ".join(full[a] for a in b["abilities"]) in body, b["name"]
            skills = ", ".join(s.replace("_", " ").title() for s in b["skills"])
            assert f"**Skills:** {skills}" in body, b["name"]
            assert f"**Knack:** *{knacks[b['knack']]}*" in body, b["name"]


# ---------------------------------------------------------------- presets

@pytest.fixture(scope="module")
def rs():
    return D.load()


@pytest.fixture(scope="module")
def cards(entries):
    return {n: (k, b) for _, n, k, b in of_kind(entries, lambda k: k.startswith("Preset · "))}


class TestPresetCards:
    def test_every_preset_printed_once_in_chapter_02(self, data, entries):
        printed = [(f, n) for f, n, k, _ in of_kind(entries, lambda k: k.startswith("Preset · "))]
        assert Counter(n for _, n in printed) == Counter(p["name"] for p in data["presets"])
        assert {f for f, _ in printed} == {"02_Characters.md"}
        assert len(data["presets"]) == 12

    def test_shape_line(self, data, cards):
        talents = {t["id"]: t for t in data["talents"]}
        for p in data["presets"]:
            depth = Counter(talents[t]["track"] for t in p["talents"].values())
            weight = data["tracks"]["facet_weight"].get(p["facet"], {})
            steel, spell = depth["steel"] + weight.get("steel", 0), depth["spell"] + weight.get("spell", 0)
            main = "Steel" if steel >= spell else "Spell"
            assert cards[p["name"]][0] == (f"Preset · {p['facet'].capitalize()} · Steel {depth['steel']}, "
                                           f"Spell {depth['spell']} at 10th · {main} main"), p["name"]

    def test_abilities_background_skills(self, data, cards):
        bgs = {b["id"]: b["name"] for b in data["backgrounds"]}
        for p in data["presets"]:
            body = cards[p["name"]][1]
            ab = ", ".join(f"{a.capitalize()} {p['abilities'][a]}"
                           for a in ("str", "dex", "con", "int", "wis", "cha"))
            assert f"**Abilities:** {ab} " in body, p["name"]
            assert f"**Background:** {bgs[p['background']]} " in body, p["name"]
            skills = ", ".join(s.replace("_", " ").title().replace(" Of ", " of ") for s in p["skills"])
            assert f"**Skills:** {skills}," in body, p["name"]

    def test_talents_by_level_with_tags(self, data, cards):
        talents = {t["id"]: t for t in data["talents"]}
        for p in data["presets"]:
            line = re.search(r"\*\*Talents:\*\* (.*)", cards[p["name"]][1]).group(1)
            printed = re.findall(r"(\d+)(?:st|nd|rd|th) \*([^*]+)\*( \[S[tp]\])?", line)
            expect = [(str(lvl), talents[t]["name"], {"steel": " [St]", "spell": " [Sp]", None: ""}[talents[t]["track"]])
                      for lvl, t in sorted(p["talents"].items())]
            assert printed == expect, p["name"]

    def test_knacks_domains_and_the_4th_8th_pick(self, data, spells, cards):
        knacks = {k["id"]: k["name"] for k in data["knacks"]}
        bgs = {b["id"]: b for b in data["backgrounds"]}
        doms = {d["id"]: d["name"] for d in spells["domains"]}
        full = {"str": "Strength", "dex": "Dexterity", "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma"}
        for p in data["presets"]:
            body = cards[p["name"]][1]
            line = re.search(r"\*\*Knacks:\*\* (.*)", body).group(1)
            assert line.startswith(f"{knacks[bgs[p['background']]['knack']]} (background)"), p["name"]
            for lvl, k in p["knacks"].items():
                assert f"{ordinal(lvl)} {knacks[k]}" in line, (p["name"], k)
            for lvl in (4, 8):
                assert f"+2 {full[p['asi'][lvl]['plus2']]}" in body, p["name"]
            ids = [p.get("domain")] + list((p.get("extra_domains") or {}).values()) + [p.get("deep_domain")]
            ids = [d for d in ids if d]
            dline = re.search(r"\*\*Domains:\*\* (.*)", body)
            if ids:
                assert re.findall(r"(?:^|, )([A-Z][\w ]+?) \(", dline.group(1)) == [doms[d] for d in ids], p["name"]
            else:
                assert dline is None, p["name"]

    def test_first_level_numbers_come_from_the_engine(self, rs, data, cards):
        for p in data["presets"]:
            ch = B.build(rs, B.Picks.from_preset(rs, p["id"], 1))
            weapon = p["kit"]["weapons"][0]
            w = ch.attack_with(weapon)
            m = re.search(r"\*\*At 1st:\*\* HP (\d+) · AC (\d+)[^·]* · ([a-z ]+) \+(\d+) \((\S+) ([+−]) (\d+)\)",
                          cards[p["name"]][1])
            assert m, p["name"]
            mod = int(m[7]) * (1 if m[6] == "+" else -1)
            assert (int(m[1]), int(m[2]), m[3], int(m[4]), m[5], mod) == \
                   (ch.hp, ch.ac, weapon.replace("_", " "), w.to_hit, str(w.dice), w.mod), p["name"]
            dc = re.search(r"spell save DC (\d+), spell attack \+(\d+)", cards[p["name"]][1])
            if ch.save_dc is None:
                assert dc is None, p["name"]
            else:
                assert (int(dc[1]), int(dc[2])) == (ch.save_dc, ch.spell_attack), p["name"]


# ---------------------------------------------------------------- magic

class TestMagicChapter:
    def slot_table(self, text, title):
        block = re.search(rf"\*\*{title}\*\*\n\n(.*?)\n\n", text, re.S).group(1)
        rows = {}
        for r in re.findall(r"^\| (\d+) \|(.*)\|$", block, re.M):
            rows[int(r[0])] = [int(c) for c in (x.strip() for x in r[1].split("|")) if c.isdigit()]
        return rows

    def test_slot_tables(self, spells, texts):
        t = texts["07_Magic.md"]
        assert self.slot_table(t, "Table 7–2: Full Casting Spell Slots") == {int(k): v for k, v in spells["full_table"].items()}
        assert self.slot_table(t, "Table 7–3: Half Casting Spell Slots") == {int(k): v for k, v in spells["half_table"].items()}

    def test_common_list(self, spells, texts):
        block = re.search(r"\*\*Table 7–4: The Common List\*\*\n\n(.*?)\n\n", texts["07_Magic.md"], re.S).group(1)
        printed = {(lvl, n) for row_lvl, names in re.findall(r"^\| (Cantrips|\d)\w* \| (.*) \|$", block, re.M)
                   for lvl in [0 if row_lvl == "Cantrips" else int(row_lvl)]
                   for n in re.findall(r"\*([^*]+)\*", names)}
        assert printed == {(s["level"], s["name"]) for s in spells["common_list"]}

    def test_every_domain_list(self, spells, texts):
        t = texts["07_Magic.md"]
        level = {"Cantrips": 0, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5}
        for d in spells["domains"]:
            m = re.search(rf"^\*\*{re.escape(d['name'])}\*\* \(([^)]*)\)\. (.*)$", t, re.M)
            assert m, d["name"]
            tag = d["role"] + (" · prismatic" if d["prismatic"] else "")
            assert m[1] == tag, d["name"]
            printed = {(level[lv], n) for lv, names in re.findall(r"\*\*(Cantrips|\d\w\w):\*\* ([^·]*)", m[2])
                       for n in re.findall(r"\*([^*]+)\*", names)}
            assert printed == {(s["level"], s["name"]) for s in d["spells"]}, d["name"]

    def test_domain_glance_table(self, spells, texts):
        rows = dict(re.findall(r"^\| ([A-Z][\w ]+?)(?: \*\(prismatic\)\*)? \| (Invocation|Thaumaturgy) \|",
                               texts["07_Magic.md"], re.M))
        assert rows == {d["name"]: d["tradition"].capitalize() for d in spells["domains"]}

    def test_no_smite_spell_named(self, texts):
        for f, t in texts.items():
            assert "Divine Smite" not in t and "Searing Smite" not in t, f


# ---------------------------------------------------------------- book-wide

def all_book_files():
    return sorted(BOOK.glob("*.md"))


class TestBookWide:
    def test_readme_carries_the_srd_attribution(self, texts):
        assert ATTRIBUTION in " ".join(texts["README.md"].split())

    def test_no_gm_or_dm(self):
        bad = re.compile(r"\b(GM|DM|GMs|DMs)\b|game master|dungeon master", re.I)
        for f in all_book_files():
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                assert not bad.search(line), f"{f.name}:{i}: {line.strip()}"

    def test_no_trademark_names(self):
        for f in all_book_files():
            t = f.read_text(encoding="utf-8")
            assert "D&D" not in t and "Dungeons" not in t, f.name

    def test_chapter_references_resolve(self, texts):
        numbers = {p.name[:2] for p in BOOK.glob("[0-9][0-9]_*.md")}
        for f, t in texts.items():
            for n in re.findall(r"Chapters? (\d\d)", t) + re.findall(r"Chapters \d\d(?:, \d\d)*,? and (\d\d)", t) \
                    + re.findall(r"Chapters \d\d–(\d\d)", t):
                assert n in numbers, f"{f}: Chapter {n}"

    def test_file_references_resolve(self, texts):
        for f, t in texts.items():
            for name in re.findall(r"`(\d\d_[\w]+\.md)`", t):
                assert (BOOK / name).exists(), f"{f}: {name}"

    def test_table_references_resolve(self, texts):
        defined = set()
        for p in all_book_files():
            defined |= set(re.findall(r"\*\*Table (\d+–\d+):", p.read_text(encoding="utf-8")))
        for f, t in texts.items():
            own = re.findall(r"\*\*Table (\d+–\d+):", t)
            assert len(own) == len(set(own)), f"{f}: a table number is used twice"
            for ref in re.findall(r"Tables? (\d+–\d+)", t):
                assert ref in defined, f"{f}: Table {ref} is never defined"

    def test_tables_are_numbered_by_chapter(self, texts):
        for f, t in texts.items():
            chapter = "0" if f == "README.md" else str(int(f[:2]))
            for num in re.findall(r"\*\*Table (\d+)–\d+:", t):
                assert num == chapter, f"{f}: Table {num}–"
