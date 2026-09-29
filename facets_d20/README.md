# Facets d20

**Facets d20** is a rules option for Facets of Origin that runs on the d20 rules of the System Reference Document 5.2.1. If you have played a game built on the SRD 5.2.1, read Chapter 01 (one page) and Chapter 02, and you can make a character tonight.

It changes three things.

**Facets instead of classes.** You pick a Facet (Body, Mind or Soul), which sets your hit die, saves and training, and then five talents over ten levels. Talents are tagged **Steel** (weapons and armor) or **Spell** (magic), or neither. Put your picks into one and you become a fighter or a full caster; split them and you become something in between, with less of each. A Soul character can be a priest, a druid, an oracle or a paladin, depending on the picks. At every even level you also take an **edge**, a small trick from one list everyone shares.

**Role-play that pays.** Every character has two Drives and a Specialty. Your Drives earn Sparks when they make your life harder, your Specialty gives you advantage, and talking your way through a scene has its own short rules.

**Short fights.** One initiative roll per side, fixed monster damage, minions, morale, and bosses that act twice a round, at the top of it and again after the party's first turn. A standard fight lasts three or four rounds.

Levels run from 1st to 10th, and spells stop at 5th level.

This is one of three rulesets in this repository. The other two (Lean Facets and the older 2d6 rules) use their own dice; Facets d20 is for tables that would rather keep the d20.

---

## The Files

**Table 0–1: Facets d20 Chapters**

| File | Contents | Written for |
|---|---|---|
| `01_What_Is_Different.md` | Every change from the SRD 5.2.1, on one page | Everyone, first |
| `02_Characters.md` | Making a character, the Facets, Steel and Spell, levels, the twelve presets, the shared talents, the edges | Players |
| `03_Facet_of_the_Body.md` | Body features and talents | Players |
| `04_Facet_of_the_Mind.md` | Mind features and talents | Players |
| `05_Facet_of_the_Soul.md` | Soul features and talents | Players |
| `06_Backgrounds_Sparks_and_Social.md` | Backgrounds, Specialties, knacks, Drives, Sparks, social play, travel | Players |
| `07_Magic.md` | Thaumaturgy and Invocation, the Common list, the domains, slot tables | Casters |
| `08_Combat.md` | Side initiative, riders, Bloodied, morale, minions, bosses | Players |
| `09_Mirror_Masters_Guide.md` | Encounter tables, bosses, running the table, monster threat | The MM |
| `10_Quick_Reference.md` | One page for the table, and a half page for the MM | Everyone |
| `data/` | The machine-readable rules: talents, presets, spell lists, encounter tables | Tools |

The person running the game is the **Mirror Master (MM)**.

You will also want the SRD 5.2.1 itself, for spell descriptions, equipment, conditions and monsters. This book points to it instead of reprinting it.

The numbers in these chapters come from `data/facets_d20.yaml` and `data/facets_d20_spells.yaml`. The rules engine in `software/facets_d20/` reads the same files, and a test (`software/tests/test_facets_d20_chapters.py`) fails if a chapter and the data disagree.

---

## Legal

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

The SRD material has been modified: rules were adapted, reorganized and combined with original material. Talents and edges whose data entry reads `basis: original` are this project's own mechanics.

Everything else in Facets d20 is part of Facets of Origin and is released under the GNU General Public License, version 3 (see `LICENSE.txt` at the root of the repository). Material adapted from the SRD 5.2.1 remains available under CC BY 4.0 as well.
