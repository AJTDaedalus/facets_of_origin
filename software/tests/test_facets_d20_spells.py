"""Facets d20 spell data: domains -> SRD 5.2.1 spell lists, and the caster tables.

Contract: docs/DESIGN_facets_d20.md section 2. Data: facets_d20/data/facets_d20_spells.yaml.
These tests read files only; they do not touch the Lean engine.
"""
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
SPELLS_YAML = REPO / "facets_d20" / "data" / "facets_d20_spells.yaml"
APPENDIX = REPO / "player_handbook" / "Appendix_Magic_Domains.md"
MAGIC_CHAPTER = REPO / "facets_d20" / "07_Magic.md"

TRADITIONS = {"Thaumaturgy", "Invocation"}

# SRD 5.2.1 full caster (e.g. Wizard/Cleric/Druid) spell slots, levels 1-10.
SRD_FULL = {
    1: [2], 2: [3], 3: [4, 2], 4: [4, 3], 5: [4, 3, 2],
    6: [4, 3, 3], 7: [4, 3, 3, 1], 8: [4, 3, 3, 2],
    9: [4, 3, 3, 3, 1], 10: [4, 3, 3, 3, 2],
}
# SRD 5.2.1 half caster (Paladin/Ranger) spell slots, levels 1-10.
SRD_HALF = {
    1: [2], 2: [2], 3: [3], 4: [3], 5: [4, 2],
    6: [4, 2], 7: [4, 3], 8: [4, 3], 9: [4, 3, 2], 10: [4, 3, 2],
}


@pytest.fixture(scope="module")
def data():
    with SPELLS_YAML.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def domains(data):
    return {d["name"]: d for d in data["domains"]}


@pytest.fixture(scope="module")
def appendix_domains():
    """Domain names from the canon catalog: bold header lines like **Fire** *(Invocation)*."""
    text = APPENDIX.read_text(encoding="utf-8")
    names = re.findall(r"^\*\*([A-Z][A-Za-z' ]+)\*\* \*\((?:Invocation|Thaumaturgy|Prismatic)\)\*",
                       text, flags=re.M)
    return set(names)


# ---------------------------------------------------------------- loading

class TestLoads:
    def test_file_exists(self):
        assert SPELLS_YAML.is_file()

    def test_parses_to_mapping(self, data):
        assert isinstance(data, dict)

    def test_top_level_keys(self, data):
        for key in ("traditions", "domains", "full_table", "half_table", "cantrips_known"):
            assert key in data, key

    def test_traditions_exact(self, data):
        assert {t["name"] for t in data["traditions"]} == TRADITIONS

    def test_tradition_abilities(self, data):
        abil = {t["name"]: set(t["ability"]) for t in data["traditions"]}
        assert abil["Thaumaturgy"] == {"Intelligence"}
        assert abil["Invocation"] == {"Wisdom", "Charisma"}

    def test_tradition_facets(self, data):
        fac = {t["name"]: t["facet"] for t in data["traditions"]}
        assert fac == {"Thaumaturgy": "Mind", "Invocation": "Soul"}


# ---------------------------------------------------------------- coverage

class TestDomainCoverage:
    def test_appendix_parse_finds_21(self, appendix_domains):
        assert len(appendix_domains) == 21

    def test_every_canon_domain_listed_or_excluded(self, data, domains, appendix_domains):
        excluded = {e["name"] for e in data.get("excluded", [])}
        missing = appendix_domains - set(domains) - excluded
        assert not missing, missing

    def test_no_invented_domains(self, domains, appendix_domains):
        assert set(domains) <= appendix_domains

    def test_exclusions_have_reasons(self, data):
        for e in data.get("excluded", []):
            assert e.get("reason"), e

    def test_domain_traditions_valid(self, domains):
        for name, d in domains.items():
            assert d["traditions"], name
            assert set(d["traditions"]) <= TRADITIONS, name

    def test_each_tradition_has_domains(self, domains):
        for t in TRADITIONS:
            assert sum(t in d["traditions"] for d in domains.values()) >= 6

    def test_no_duplicate_domain_names(self, data):
        names = [d["name"] for d in data["domains"]]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------- spell lists

class TestSpellLists:
    def test_levels_zero_to_five(self, domains):
        for name, d in domains.items():
            for s in d["spells"]:
                assert isinstance(s["level"], int), (name, s)
                assert 0 <= s["level"] <= 5, (name, s)

    def test_size_eight_to_fifteen(self, domains):
        for name, d in domains.items():
            assert 8 <= len(d["spells"]) <= 15, (name, len(d["spells"]))

    def test_at_least_two_cantrips(self, domains):
        for name, d in domains.items():
            assert sum(s["level"] == 0 for s in d["spells"]) >= 2, name

    def test_has_leveled_spells(self, domains):
        for name, d in domains.items():
            assert any(s["level"] >= 1 for s in d["spells"]), name

    def test_has_first_level_spell(self, domains):
        # A 1st-level caster only has 1st-level slots; every domain must feed them.
        for name, d in domains.items():
            assert any(s["level"] == 1 for s in d["spells"]), name

    def test_prismatic_flags_match_canon(self, domains):
        canon = {"The Undying", "Fate", "The Living World",
                 "The Arcane", "The Constructed Mind", "Chronomancy"}
        assert {n for n, d in domains.items() if d.get("prismatic")} == canon

    def test_no_duplicates_within_domain(self, domains):
        for name, d in domains.items():
            spells = [s["name"] for s in d["spells"]]
            assert len(spells) == len(set(spells)), name

    def test_spell_names_nonempty_strings(self, domains):
        for name, d in domains.items():
            for s in d["spells"]:
                assert isinstance(s["name"], str) and s["name"].strip(), name

    def test_same_spell_same_level_everywhere(self, domains):
        seen = {}
        for d in domains.values():
            for s in d["spells"]:
                assert seen.setdefault(s["name"], s["level"]) == s["level"], s["name"]

    def test_body_has_no_domains(self, data):
        # Canon: the Body has no magic tradition.
        assert all(t["facet"] != "Body" for t in data["traditions"])


# ---------------------------------------------------------------- presets

class TestPresetPairs:
    @pytest.mark.parametrize("preset", ["Priest", "Druid", "Oracle"])
    def test_soul_preset_pair_exists(self, data, domains, preset):
        pair = data["recommended_pairs"][preset]
        assert len(pair) == 2
        for dom in pair:
            assert "Invocation" in domains[dom]["traditions"], (preset, dom)

    def test_priest_has_healing(self, data, domains):
        spells = {s["name"] for dom in data["recommended_pairs"]["Priest"]
                  for s in domains[dom]["spells"]}
        assert "Cure Wounds" in spells

    def test_druid_has_nature(self, data, domains):
        spells = {s["name"] for dom in data["recommended_pairs"]["Druid"]
                  for s in domains[dom]["spells"]}
        assert {"Druidcraft", "Speak with Animals"} <= spells

    def test_oracle_has_divination(self, data, domains):
        spells = {s["name"] for dom in data["recommended_pairs"]["Oracle"]
                  for s in domains[dom]["spells"]}
        assert {"Augury", "Divination"} <= spells


# ---------------------------------------------------------------- tables

class TestTables:
    def test_full_table_matches_srd(self, data):
        assert {int(k): v for k, v in data["full_table"].items()} == SRD_FULL

    def test_half_table_matches_srd(self, data):
        assert {int(k): v for k, v in data["half_table"].items()} == SRD_HALF

    def test_full_table_tops_at_fifth(self, data):
        assert max(len(v) for v in data["full_table"].values()) == 5

    def test_half_table_tops_at_third(self, data):
        assert max(len(v) for v in data["half_table"].values()) == 3

    def test_half_is_full_at_half_level(self, data):
        full = {int(k): v for k, v in data["full_table"].items()}
        for lvl, row in data["half_table"].items():
            assert row == full[-(-int(lvl) // 2)], lvl

    def test_cantrips_known(self, data):
        ck = {int(k): v for k, v in data["cantrips_known"].items()}
        assert ck == {1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 4}

    def test_tables_cover_levels_1_to_10(self, data):
        for key in ("full_table", "half_table", "cantrips_known"):
            assert sorted(int(k) for k in data[key]) == list(range(1, 11)), key


# ---------------------------------------------------------------- book agrees with data

class TestChapterAgrees:
    def test_chapter_exists(self):
        assert MAGIC_CHAPTER.is_file()

    def test_every_domain_has_a_heading(self, domains):
        text = MAGIC_CHAPTER.read_text(encoding="utf-8")
        for name in domains:
            assert re.search(rf"^### {re.escape(name)}\b", text, flags=re.M), name

    def test_every_spell_named_in_chapter(self, domains):
        text = MAGIC_CHAPTER.read_text(encoding="utf-8")
        for d in domains.values():
            for s in d["spells"]:
                assert s["name"] in text, (d["name"], s["name"])

    def test_no_gm_or_dm(self):
        text = MAGIC_CHAPTER.read_text(encoding="utf-8")
        assert not re.search(r"\b(GM|DM)\b", text)


# ---------------------------------------------------------------- caster level (Planner ruling a)

def caster_level(level_taken: int, character_level: int) -> int:
    """Levels held since taking the caster talent, counting the level taken as 1."""
    if character_level < level_taken:
        raise ValueError("character has not taken the caster talent yet")
    return character_level - level_taken + 1


def slots(data, table: str, level_taken: int, character_level: int) -> list:
    """Slot row a caster uses, per the yaml's declared table index."""
    index = data["casting"][f"{table}_table_index"]
    assert index in ("caster_level", "character_level"), index
    row = caster_level(level_taken, character_level) if index == "caster_level" else character_level
    return data[f"{table}_table"][row]


class TestCasterLevel:
    def test_both_tables_read_by_caster_level(self, data):
        assert data["casting"]["full_table_index"] == "caster_level"
        assert data["casting"]["half_table_index"] == "caster_level"

    def test_cantrips_still_by_character_level(self, data):
        assert data["casting"]["cantrips_index"] == "character_level"

    def test_prepared_full_uses_caster_level(self, data):
        assert "caster_level" in data["casting"]["prepared_full"]
        assert "character_level" not in data["casting"]["prepared_full"]

    @pytest.mark.parametrize("level", range(1, 11))
    def test_taken_at_first_is_unaffected(self, data, level):
        # A full caster from 1st level reads the Full table at their character level.
        assert slots(data, "full", 1, level) == SRD_FULL[level]

    def test_late_full_caster_starts_at_row_one(self, data):
        # The loophole: Invocation taken at 6th no longer hands out 6th-level slots.
        assert slots(data, "full", 6, 6) == SRD_FULL[1]
        assert slots(data, "full", 6, 10) == SRD_FULL[5]

    def test_late_full_caster_never_reaches_fifth_level_spells_by_tenth(self, data):
        assert len(slots(data, "full", 3, 10)) == 4  # caster level 8: 4th-level slots

    def test_half_caster_counts_from_talent(self, data):
        assert slots(data, "half", 2, 2) == SRD_HALF[1]
        assert slots(data, "half", 2, 10) == SRD_HALF[9]

    def test_caster_level_rejects_level_before_talent(self):
        with pytest.raises(ValueError):
            caster_level(4, 3)

    def test_chapter_states_caster_level_for_full_table(self):
        text = MAGIC_CHAPTER.read_text(encoding="utf-8")
        assert "| Caster level | Cantrips |" in text
        assert "casting modifier + caster level" in text
        assert "reads it by character level" not in text

    @pytest.mark.parametrize("chapter", ["04_Facet_of_the_Mind.md", "05_Facet_of_the_Soul.md"])
    def test_tradition_talent_text_says_caster_level(self, chapter):
        text = (REPO / "facets_d20" / chapter).read_text(encoding="utf-8")
        assert "read by your character level" not in text
        assert "read by your **caster level**" in text


# ---------------------------------------------------------------- SRD 5.2.1 whitelist

# Every spell name and level below was checked on 2026-09-27 against the SRD 5.2.1 PDF
# (https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf) and the Open5e
# srd-2024 spell list. See docs/RESEARCH_facets_d20_srd_check.md. A new spell goes on a
# domain only after it has been checked and added here.
SRD_521_VERIFIED = {
    # level 0
    'Acid Splash': 0,
    'Chill Touch': 0,
    'Dancing Lights': 0,
    'Druidcraft': 0,
    'Eldritch Blast': 0,
    'Elementalism': 0,
    'Fire Bolt': 0,
    'Guidance': 0,
    'Light': 0,
    'Mage Hand': 0,
    'Mending': 0,
    'Message': 0,
    'Minor Illusion': 0,
    'Poison Spray': 0,
    'Prestidigitation': 0,
    'Produce Flame': 0,
    'Ray of Frost': 0,
    'Resistance': 0,
    'Sacred Flame': 0,
    'Shillelagh': 0,
    'Shocking Grasp': 0,
    'Sorcerous Burst': 0,
    'Spare the Dying': 0,
    'Starry Wisp': 0,
    'Thaumaturgy': 0,
    'True Strike': 0,
    'Vicious Mockery': 0,
    # level 1
    'Alarm': 1,
    'Animal Friendship': 1,
    'Bane': 1,
    'Bless': 1,
    'Burning Hands': 1,
    'Color Spray': 1,
    'Command': 1,
    'Comprehend Languages': 1,
    'Cure Wounds': 1,
    'Detect Evil and Good': 1,
    'Detect Magic': 1,
    'Detect Poison and Disease': 1,
    'Disguise Self': 1,
    'Divine Smite': 1,
    'Ensnaring Strike': 1,
    'Entangle': 1,
    'Expeditious Retreat': 1,
    'False Life': 1,
    'Feather Fall': 1,
    'Find Familiar': 1,
    'Fog Cloud': 1,
    'Goodberry': 1,
    'Grease': 1,
    'Healing Word': 1,
    'Hellish Rebuke': 1,
    'Heroism': 1,
    "Hunter's Mark": 1,
    'Identify': 1,
    'Illusory Script': 1,
    'Inflict Wounds': 1,
    'Longstrider': 1,
    'Mage Armor': 1,
    'Magic Missile': 1,
    'Protection from Evil and Good': 1,
    'Purify Food and Drink': 1,
    'Sanctuary': 1,
    'Searing Smite': 1,
    'Shield': 1,
    'Shield of Faith': 1,
    'Silent Image': 1,
    'Sleep': 1,
    'Speak with Animals': 1,
    'Thunderwave': 1,
    'Unseen Servant': 1,
    # level 2
    'Aid': 2,
    'Animal Messenger': 2,
    'Arcane Lock': 2,
    'Augury': 2,
    'Barkskin': 2,
    'Blindness/Deafness': 2,
    'Blur': 2,
    'Calm Emotions': 2,
    'Continual Flame': 2,
    'Darkness': 2,
    'Darkvision': 2,
    'Enhance Ability': 2,
    'Enlarge/Reduce': 2,
    'Enthrall': 2,
    'Find Traps': 2,
    'Flame Blade': 2,
    'Flaming Sphere': 2,
    'Gentle Repose': 2,
    'Gust of Wind': 2,
    'Heat Metal': 2,
    'Hold Person': 2,
    'Invisibility': 2,
    'Knock': 2,
    'Lesser Restoration': 2,
    'Levitate': 2,
    'Locate Animals or Plants': 2,
    'Locate Object': 2,
    'Magic Mouth': 2,
    'Magic Weapon': 2,
    'Mirror Image': 2,
    'Pass without Trace': 2,
    'Prayer of Healing': 2,
    'Ray of Enfeeblement': 2,
    'Scorching Ray': 2,
    'See Invisibility': 2,
    'Shatter': 2,
    'Silence': 2,
    'Spike Growth': 2,
    'Spiritual Weapon': 2,
    'Warding Bond': 2,
    'Zone of Truth': 2,
    # level 3
    'Animate Dead': 3,
    'Beacon of Hope': 3,
    'Bestow Curse': 3,
    'Blink': 3,
    'Call Lightning': 3,
    'Clairvoyance': 3,
    'Conjure Animals': 3,
    'Counterspell': 3,
    'Dispel Magic': 3,
    'Fear': 3,
    'Fireball': 3,
    'Fly': 3,
    'Glyph of Warding': 3,
    'Haste': 3,
    'Hypnotic Pattern': 3,
    'Lightning Bolt': 3,
    'Magic Circle': 3,
    'Major Image': 3,
    'Mass Healing Word': 3,
    'Meld into Stone': 3,
    'Nondetection': 3,
    'Phantom Steed': 3,
    'Plant Growth': 3,
    'Protection from Energy': 3,
    'Remove Curse': 3,
    'Revivify': 3,
    'Sending': 3,
    'Sleet Storm': 3,
    'Slow': 3,
    'Speak with Dead': 3,
    'Speak with Plants': 3,
    'Spirit Guardians': 3,
    'Tiny Hut': 3,
    'Tongues': 3,
    'Vampiric Touch': 3,
    'Wind Wall': 3,
    # level 4
    'Arcane Eye': 4,
    'Aura of Life': 4,
    'Banishment': 4,
    'Black Tentacles': 4,
    'Blight': 4,
    'Death Ward': 4,
    'Divination': 4,
    'Dominate Beast': 4,
    'Fabricate': 4,
    'Faithful Hound': 4,
    'Fire Shield': 4,
    'Freedom of Movement': 4,
    'Giant Insect': 4,
    'Greater Invisibility': 4,
    'Guardian of Faith': 4,
    'Hallucinatory Terrain': 4,
    'Ice Storm': 4,
    'Locate Creature': 4,
    'Phantasmal Killer': 4,
    'Polymorph': 4,
    'Private Sanctum': 4,
    'Resilient Sphere': 4,
    'Secret Chest': 4,
    'Stone Shape': 4,
    'Stoneskin': 4,
    'Wall of Fire': 4,
    # level 5
    'Animate Objects': 5,
    'Antilife Shell': 5,
    'Arcane Hand': 5,
    'Awaken': 5,
    'Commune': 5,
    'Commune with Nature': 5,
    'Cone of Cold': 5,
    'Conjure Elemental': 5,
    'Contagion': 5,
    'Dispel Evil and Good': 5,
    'Flame Strike': 5,
    'Geas': 5,
    'Greater Restoration': 5,
    'Hallow': 5,
    'Hold Monster': 5,
    'Insect Plague': 5,
    'Legend Lore': 5,
    'Mass Cure Wounds': 5,
    'Passwall': 5,
    'Planar Binding': 5,
    'Raise Dead': 5,
    'Scrying': 5,
    'Seeming': 5,
    'Telekinesis': 5,
    'Teleportation Circle': 5,
    'Tree Stride': 5,
    'Wall of Force': 5,
    'Wall of Stone': 5,
}


class TestSrdWhitelist:
    def test_every_domain_spell_is_verified_srd_521(self, domains):
        for d in domains.values():
            for s in d["spells"]:
                assert s["name"] in SRD_521_VERIFIED, (d["name"], s["name"])

    def test_every_domain_spell_has_its_srd_level(self, domains):
        for d in domains.values():
            for s in d["spells"]:
                assert SRD_521_VERIFIED[s["name"]] == s["level"], (d["name"], s["name"])

    def test_whitelist_levels_in_range(self):
        assert all(0 <= lvl <= 5 for lvl in SRD_521_VERIFIED.values())

    @pytest.mark.parametrize("name", ["Thunderous Smite", "Toll the Dead", "Thorn Whip", "Hail of Thorns"])
    def test_known_non_srd_spells_absent(self, domains, name):
        # Checked: these are not in SRD 5.2.1.
        assert all(name not in {s["name"] for s in d["spells"]} for d in domains.values())
