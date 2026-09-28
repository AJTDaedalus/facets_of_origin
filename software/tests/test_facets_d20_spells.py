"""Facets d20 spell data v0.2: the Common list, domains, slot tables and sim spells.

Contract: docs/DESIGN_facets_d20_v0_2.md §1.6 and §3. Data:
facets_d20/data/facets_d20_spells.yaml. These are data-integrity tests (names, levels,
canon, SRD whitelist, table shape); rule behaviour is tested through the engine in
test_facets_d20_engine.py. Chapter-agreement tests were retired with v0.1: chapter 07 is
rewritten from the DESIGN in the prose pass, and its tests come back with it.
"""
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
SPELLS_YAML = REPO / "facets_d20" / "data" / "facets_d20_spells.yaml"
APPENDIX = REPO / "player_handbook" / "Appendix_Magic_Domains.md"

# SRD 5.2.1 full caster (Wizard/Cleric/Druid) spell slots, levels 1-10.
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
ENGINE_MODELS = {"attack", "save", "auto", "heal", "aura", "weapon_rider", "weapon_cantrip",
                 "disable", "shield", "buff_attack", "ac_set", "ac_bonus"}
ROLES = {"offense", "control", "support", "utility"}



@pytest.fixture(scope="module")
def data():
    return yaml.safe_load(SPELLS_YAML.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def domains(data):
    return {d["name"]: d for d in data["domains"]}


@pytest.fixture(scope="module")
def canon():
    """Canon catalog: {name: (tradition, prismatic)} from the appendix's bold header lines.

    Prismatic headers carry *(Prismatic)*; their tradition is the section they sit in
    ("Domains of the Soul" = Invocation, "Domains of the Mind" = Thaumaturgy).
    """
    out, section = {}, None
    for line in APPENDIX.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Domains of the Soul"):
            section = "invocation"
        elif line.startswith("## Domains of the Mind"):
            section = "thaumaturgy"
        m = re.match(r"^\*\*([A-Z][A-Za-z' ]+)\*\* \*\((Invocation|Thaumaturgy|Prismatic)\)\*", line)
        if m:
            name, tag = m.groups()
            out[name] = (section, tag == "Prismatic")
    return out


def all_listed(data):
    """(list name, spell) for the Common list and every domain."""
    for s in data["common_list"]:
        yield "Common", s
    for d in data["domains"]:
        for s in d["spells"]:
            yield d["name"], s


class TestShape:
    def test_version(self, data):
        assert str(data["version"]) == "0.2"

    def test_traditions(self, data):
        assert set(data["traditions"]) == {"thaumaturgy", "invocation"}
        assert data["traditions"]["thaumaturgy"]["ability"] == ["int"]
        assert data["traditions"]["invocation"]["ability"] == ["soul"]

    def test_no_preparation(self, data):
        # Ruling 4, less structure: cast anything on your lists; know all their cantrips.
        assert data["casting"]["known"] == "all_on_lists"
        assert data["casting"]["cantrips"] == "all_on_lists"
        # Amendment 2: domains come from `domains` effects (Spellcasting rank, Wider Study,
        # Deep Magic) in facets_d20.yaml's tracks, not from a path.
        assert "domains_on_path" not in data["casting"]
        assert data["casting"]["domains_from"] == "tracks"

    def test_prismatic_only_through_deep_magic(self, data):
        # §5.1 option (a), provisional pending the owner's ruling.
        assert data["casting"]["prismatic_from"] == "deep_magic"

    @pytest.mark.parametrize("name", ["Divine Smite", "Searing Smite"])
    def test_no_smite_spells(self, data, name):
        # V24: slots never buy weapon damage; Sworn Strike is the one smite.
        assert name not in {s["name"] for _, s in all_listed(data)}
        assert name not in {s["name"] for s in data["sim_spells"]}

    def test_one_clock(self, data):
        # v0.1's caster-level/character-level split (audit GF-M7 #10) is gone.
        assert data["casting"]["table_index"] == "character_level"
        assert "cantrips_known" not in data


class TestCommonList:
    def test_levels_zero_to_five(self, data):
        assert sorted({s["level"] for s in data["common_list"]}) == [0, 1, 2, 3, 4, 5]

    @pytest.mark.parametrize("name", ["Fireball", "Burning Hands", "Shatter", "Lightning Bolt",
                                      "Cone of Cold", "Fire Bolt"])
    def test_classic_evocation_for_both_traditions(self, data, name):
        # Ruling 4: a wizard-shaped Mind caster can cast a fireball.
        assert name in {s["name"] for s in data["common_list"]}

    def test_area_damage_at_every_spell_level(self, data):
        area = {1: "Burning Hands", 2: "Shatter", 3: "Fireball", 4: "Ice Storm", 5: "Cone of Cold"}
        names = {s["name"]: s["level"] for s in data["common_list"]}
        for lvl, n in area.items():
            assert names.get(n) == lvl

    def test_common_spells_not_on_domains(self, data):
        common = {s["name"] for s in data["common_list"]}
        for d in data["domains"]:
            assert not common & {s["name"] for s in d["spells"]}, d["name"]


class TestDomains:
    def test_exactly_the_canon_domains(self, domains, canon):
        assert set(domains) == set(canon)

    def test_traditions_match_canon(self, domains, canon):
        for name, d in domains.items():
            assert d["tradition"] == canon[name][0], name

    def test_divination_is_thaumaturgy_only(self, domains):
        # Canon item CAN-1 resolved: restored to the catalogue.
        assert domains["Divination"]["tradition"] == "thaumaturgy"

    def test_prismatic_flags_match_canon(self, domains, canon):
        for name, d in domains.items():
            assert d["prismatic"] is canon[name][1], name

    def test_roles(self, domains):
        for d in domains.values():
            assert d["role"] in ROLES, d["name"]

    def test_ids_snake_case_and_unique(self, data):
        ids = [d["id"] for d in data["domains"]]
        assert len(ids) == len(set(ids))
        assert all(re.fullmatch(r"[a-z][a-z0-9_]*", i) for i in ids)

    def test_each_tradition_has_domains(self, domains):
        assert {d["tradition"] for d in domains.values()} == {"thaumaturgy", "invocation"}

    def test_every_domain_has_a_cantrip_and_leveled_spells(self, domains):
        for d in domains.values():
            levels = [s["level"] for s in d["spells"]]
            assert 0 in levels and any(l >= 1 for l in levels), d["name"]

    def test_no_duplicates_within_a_list(self, data):
        seen = {}
        for where, s in all_listed(data):
            seen.setdefault(where, []).append(s["name"])
        for where, names in seen.items():
            assert len(names) == len(set(names)), where

    def test_same_spell_same_level_everywhere(self, data):
        level = {}
        for where, s in all_listed(data):
            assert level.setdefault(s["name"], s["level"]) == s["level"], (where, s["name"])


class TestTables:
    def test_full_table_matches_srd(self, data):
        assert {int(k): v for k, v in data["full_table"].items()} == SRD_FULL

    def test_half_table_matches_srd(self, data):
        assert {int(k): v for k, v in data["half_table"].items()} == SRD_HALF


class TestSimSpells:
    def test_models_known_to_engine(self, data):
        for s in data["sim_spells"]:
            assert s["model"] in ENGINE_MODELS, s["name"]

    def test_every_sim_spell_is_on_some_list(self, data):
        listed = {s["name"] for _, s in all_listed(data)}
        for s in data["sim_spells"]:
            assert s["name"] in listed, s["name"]

    def test_sim_levels_match_lists(self, data):
        level = {s["name"]: s["level"] for _, s in all_listed(data)}
        for s in data["sim_spells"]:
            assert level[s["name"]] == s["level"], s["name"]

    def test_names_unique(self, data):
        names = [s["name"] for s in data["sim_spells"]]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------- SRD 5.2.1 whitelist
# Verified against the SRD 5.2.1 PDF and Open5e srd-2024 (docs/RESEARCH_facets_d20_srd_check.md).
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
    def test_every_listed_spell_is_verified_srd_521(self, data):
        for where, s in all_listed(data):
            assert s["name"] in SRD_521_VERIFIED, (where, s["name"])

    def test_every_listed_spell_has_its_srd_level(self, data):
        for where, s in all_listed(data):
            assert SRD_521_VERIFIED[s["name"]] == s["level"], (where, s["name"])

    def test_whitelist_levels_in_range(self):
        assert all(0 <= lvl <= 5 for lvl in SRD_521_VERIFIED.values())

    @pytest.mark.parametrize("name", ["Thunderous Smite", "Toll the Dead", "Thorn Whip", "Hail of Thorns"])
    def test_known_non_srd_spells_absent(self, data, name):
        assert name not in {s["name"] for _, s in all_listed(data)}
