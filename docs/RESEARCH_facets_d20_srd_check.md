# RESEARCH — Facets d20 against SRD 5.2.1

*Integration review, 2026-09-27. Checks every spell name and level in
`facets_d20/data/facets_d20_spells.yaml` / `facets_d20/07_Magic.md`, the candidate
spells drafter C left out as "uncertain", and the six worked monster conversions in
`facets_d20/09_Mirror_Masters_Guide.md`.*

## Sources actually retrieved

| Source | URL | What it gave |
|---|---|---|
| SRD 5.2.1 PDF (official, 364 pp., footer "System Reference Document 5.2.1") | https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf | Full text, extracted with PyMuPDF. 339 spells parsed from the spell headers; monster stat blocks read directly |
| Open5e v2 API, document `srd-2024` (the SRD 5.2 release) | https://api.open5e.com/v2/spells/?document__key=srd-2024&limit=500&fields=name,level | 339 spells, names and levels; a cross-check of the PDF parse |
| D&D Beyond SRD landing page (licence and attribution text) | https://www.dndbeyond.com/srd | Attribution wording used in every chapter |

The two spell sources agree exactly (same 339 names, no level differences). The
integration reviewer re-ran the comparison of the final yaml against the PDF parse:
all 202 spells on the domain lists match name and level. Nothing below is from memory.

## 1. Spells on the domain lists

- **Drafter C's 189 spells: all present in SRD 5.2.1 under exactly the listed name, at
  the listed level.** No renames, no level changes, nothing removed. (The 5.2.1 names
  C used — Tiny Hut, Black Tentacles, Resilient Sphere, Arcane Hand, Faithful Hound,
  Private Sanctum, Secret Chest — are correct.)
- 13 added back (below), for 202 unique spells. All 202 are now pinned in
  `software/tests/test_facets_d20_spells.py::SRD_521_VERIFIED`; a spell not on that
  list fails the suite.

## 2. Candidates C omitted as uncertain

**In SRD 5.2.1** (level): Elementalism (0), Sorcerous Burst (0), Starry Wisp (0),
Hunter's Mark (1), Divine Smite (1), Searing Smite (1), Divine Favor (1), Ensnaring
Strike (1), Shining Smite (2), Enthrall (2), Find Traps (2), Spiritual Weapon (2),
Moonbeam (2), Giant Insect (4), Aura of Life (4), Hallow (5), Holy Aura (8 — over the
cap).

**Not in SRD 5.2.1:** Thunderous, Wrathful, Branding, Blinding, Staggering and
Banishing Smite; Thorn Whip; Toll the Dead; Word of Radiance; Shape Water; Mold Earth;
Hail of Thorns; Zephyr Strike; Conjure Barrage; Summon Beast; Summon Fey; Aura of
Vitality; Circle of Power; Destructive Wave. (The only smites in 5.2.1 are Divine,
Searing and Shining. Elementalism stands in for Shape Water / Mold Earth.)

**Added to domains** (each list stays within 8–15):

| Spell | Lvl | Domain | Why there |
|---|---|---|---|
| Hunter's Mark | 1 | Beasts | The hunter's spell; feeds the ranger-shape build in 03 (Beasts + Verdance) |
| Giant Insect | 4 | Beasts | Animals made large |
| Divine Smite | 1 | Presence | Spiritual weight in a blow; feeds the holy-warrior build in 03 (Presence + Binding) |
| Spiritual Weapon | 2 | Presence | The priest staple the Priest pair lacked |
| Searing Smite | 1 | Fire | Fire |
| Ensnaring Strike | 1 | Verdance | Vines |
| Enthrall | 2 | Resonance | Holds attention with the voice; doesn't command |
| Find Traps | 2 | Divination | Finding out |
| Hallow | 5 | Warding | A protective limit on a place |
| Aura of Life | 4 | The Tide | Vitality; The Tide had no 4th-level spell |
| Elementalism | 0 | Storm | Wind and water shaping; Storm had two cantrips |
| Sorcerous Burst | 0 | The Arcane | Raw magic; The Arcane had no damaging cantrip |
| Starry Wisp | 0 | Fate | Closest fit; the Oracle pair had no damaging cantrip besides True Strike |

**Not placed** (in the SRD, but every fitting list was full or none fits): Divine
Favor, Shining Smite, Moonbeam. Owner can swap them in if wanted.

## 3. Monster conversions (09)

| Monster | SRD 5.2.1 block (PDF page) | 09 said | Result |
|---|---|---|---|
| Bandit | CR 1/8, AC 12, HP 11 (2d8+2); Scimitar +3, 4 (1d6+1); Light Crossbow +3, 5 (1d8+1) (p. 261) | AC 12, +3, 4 or 5 | Correct. Added "11 as a standard foe" |
| Goblin Warrior | CR 1/4, AC 15, HP 10 (3d6); Scimitar/Shortbow +4, 5 (1d6+2), +2 (1d4) with advantage; Nimble Escape (p. 290) | AC 15, 10 HP, +4, 5 | Correct. Added "7 with advantage" |
| Zombie | CR 1/4, AC 8, HP 15 (2d8+6); Slam +3, 5 (1d8+1); Undead Fortitude (pp. 343–344) | AC 8, +3, 5 | Correct. Added "15 as a standard foe" |
| Ogre | CR 2, AC 11, HP 68 (8d10+24); Greatclub +6, 13 (2d8+4); Javelin +6, 11 (2d6+4) (p. 312) | AC 11, 68, +6, 13 / 11 | Correct |
| Owlbear | CR 3, AC 13, HP 59 (7d10+21); Multiattack two Rends, +7, 14 (2d8+5) each (p. 313) | AC 13, 59, +7, 2 × 14 = 28 | Correct |
| Young Red Dragon | CR 10, AC 18, HP 178 (17d10+85); Multiattack three Rends, +10, 13 (2d6+6) slashing + 3 (1d6) fire each; Fire Breath Recharge 5–6, DC 17 Dex, 56 (16d6), half on success (p. 318) | "about 45" a turn | **Corrected to 48 a turn** (3 × 16); boss total 96, still within the 9th-level Standard budget (205 / 106) |

The budget arithmetic around each conversion (Ogre as a 1st–2nd level boss, Owlbear
at 3rd, the 3rd-level Standard example) was rechecked against Table 9–1 and holds.

## 4. Other SRD facts spot-checked

- Actions list in 08 (Attack, Dash, Disengage, Dodge, Help, Hide, Influence, Magic,
  Ready, Search, Study, Utilize) matches SRD 5.2.1.
- Longsword's mastery property is Sap (08's vignette uses it correctly).
- The Young Red Dragon's Rend is its only attack; 09's Bloodied line now says "instead
  of making its Rend attacks" (was "instead of biting").

- The fifteen conditions in 08 are exactly SRD 5.2.1's fifteen `[Condition]` entries.
- Death saves in 08 match the PDF (p. 18): DC 10, three of a kind, a 1 is two failures,
  a 20 regains 1 HP, damage at 0 is a failure (two on a crit).
