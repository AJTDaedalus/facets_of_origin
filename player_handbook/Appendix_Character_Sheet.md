# Appendix: Character Sheet

Print this, copy it into a notebook, or use it as a checklist beside the app. Every field on it is described in Chapter II.1, and nothing here is new.

---

| Character Name | Player Name |
|---|---|
| | |

---

### Who You Are

| Field | Value |
|---|---|
| Facet (Body / Mind / Soul) | |
| Level | |
| Class | |
| Concept (*I am a ___ who ___*) | |
| Preset or custom | |
| Lineage | |
| Background | |

---

### Stats

| Stat | Modifier |
|---|---|
| Body | |
| Mind | |
| Soul | |

---

### Hit Points and Armor

| Field | Value |
|---|---|
| Maximum HP | |
| Current HP | |
| Armor (worn + shield, 3 at most) | |
| Weapon and damage die | |
| Damage bonus (level 3+) | |

---

### Knacks and Specialty

| Field | Value |
|---|---|
| Class knack | |
| Background knack | |
| Gift knack (if any) | |
| Specialty | |

---

### Talents and Signature

| Talent | Choice (if any) | Improved? | Uses spent |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| Signature (level 3) | | — | |

---

### Magic (casters only)

| Field | Value |
|---|---|
| Tradition (Thaumaturgy / Invocation) | |
| Domain(s) | |
| Signature workings | |

---

### Slots (10 + Body)

| Slot | Item, Wound or Fatigue | Usage die |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |
| 11 | | |
| 12 | | |
| 13 | | |

---

### Resources and Marks of the Road

| Field | Value |
|---|---|
| Coin | |
| Sparks (3 each session) | |
| Fatigue | |
| Wounds | |
| Scars | |

---

### Notes

| Player notes |
|---|
| |

---

### For the App

The app saves this sheet as a character file. Each section above is one or more fields in that file.

| Sheet section | Character file field |
|---|---|
| Character Name / Player Name | `name`, `player_name` |
| Facet, Level | `facet`, `level` |
| Class, Concept, Preset or custom | `class.name`, `class.concept`, `class.custom` |
| Lineage | `lineage` |
| Background | `background` |
| Stats | `stats.body`, `stats.mind`, `stats.soul` |
| Maximum and current HP | `hp.max`, `hp.current` |
| Armor, weapon | `equipped.armor`, `equipped.shield`, `equipped.weapon` |
| Knacks | `knacks` |
| Specialty | `specialty` |
| Talents, choice, improved | `talents` |
| Uses spent | `talent_uses` |
| Signature | `signature` |
| Magic | `magic.tradition`, `magic.domains`, `magic.signature_workings` |
| Slots | `inventory` |
| Coin, Sparks, Fatigue | `coin`, `sparks`, `fatigue` |
| Wounds, Scars | `wounds`, `scars` |
| Player notes | `notes_player` |
