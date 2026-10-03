# RESEARCH — 5e Reference Library Catalog

*2026-09-30. Written for the official-module audit of the 5e edition of Oraga Night
(`docs/AUDIT_oraga_5e_official_style.md`, log in `docs/LOG_oraga_5e_official_audit.md`).
Scope is 5e only for now. The same catalog will serve the later Facets d20 pass.*

## Where the books are

| Library | Path (WSL) | Role |
|---|---|---|
| D&D 5e (234 PDFs) | `/mnt/e/books/DandD 5E/` (folders have `-2017…Z-001` suffixes) | **Primary evidence** |
| D&D 3.5 | `(the owner's local D&D 3.5 folder; path kept out of the repo)` | Secondary evidence for phrasing only |

Text extracts (PyMuPDF, with `=== PAGE n ===` markers) sit in the session scratchpad,
which is temporary. Re-extract with PyMuPDF if they are needed again. Nothing from these
books is copied into the repo.

**Copyright posture.** These are proprietary books (the SRD 5.1 is CC BY 4.0, and it is the one exception).
Audit docs record **conventions and patterns only**: structure, voice, formatting, how
mechanics are phrased. Stock rules grammar that is also in the SRD (for example,
"DC 15 Wisdom (Perception) check") can be used freely. Named content, read-aloud text,
sentences, stat blocks and lore stay in the books.

## Classification by title

### A. Adventure modules: hardcover campaigns (primary structure/prose evidence)

| Title | File | Text? | Notes |
|---|---|---|---|
| Lost Mine of Phandelver (Starter Set) | `Epic/Epic/Lost Mine of Phandelver.pdf` | yes | The copy in `0 Core books/` is an image scan; use the Epic copy. The closest 5e analog for a starter module |
| Hoard of the Dragon Queen | `1 Tyranny of Dragons/Hoard of the Dragon Queen/Hoard of the Dragon Queen (1-8).pdf` | yes | Supplement files are its monster/magic-item supplement |
| Rise of Tiamat | `1 Tyranny of Dragons/Rise of Tiamat/Rise of Tiamat (8-15).pdf` | yes | Council of Waterdeep chapters are faction/social scene evidence |
| Princes of the Apocalypse | `2 Elemental evil/Princes of the Apocalypse/Princes of the Apocalypse (1-15).pdf` | yes | |
| Out of the Abyss | `3 Rage of Demons/Out.Of.The.Abyss/Out of the Abyss (OCR, Bookmarked, Cropped).pdf` | yes | |
| Curse of Strahd | `4 Curse of Strahd/Curse of Strahd Book.pdf` | yes | Gothic social set-pieces (a dinner, a feast, a ball-like scene): the closest tonal analog to Oraga Night |
| Storm King's Thunder | `Storm King's Thunder.pdf` | yes | |

### B. Adventure modules: short and session-length (primary evidence at our size)

| Title | File | Text? |
|---|---|---|
| Curse of Strahd Introductory Adventure (Death House) | `4 Curse of Strahd/Curse of Strahd Introductory Adventure.pdf` | yes. `Death house/Death house*.pdf` are image-only scans |
| Adventurers League DDEX1-1 to 1-14 (Tyranny of Dragons season) | `1 Tyranny of Dragons/DDEX1-*.pdf` | yes |
| Adventurers League DDEX2-01 to 2-16 (Elemental Evil season) | `2 Elemental evil/DDEX2-*.pdf` | yes |
| Adventurers League DDEX3-01 to 3-16 (Rage of Demons season) | `3 Rage of Demons/DDEX3-*.pdf` | yes |
| Adventurers League DDAL04-01 to 04-14 (Curse of Strahd season) | `4 Curse of Strahd/AL quests/DDAL04-*.pdf` | yes |
| D&D Epics DDEP1 to DDEP3 (multi-table events) | `Epic/Epic/DDEP*.pdf` | yes; "Admin" files are the organizer packets |
| Encounters-season sheets | `Hoard of the Dragon Queen/HoardDragonQueen_Encounters*.pdf`, `DDEN_PrincesoftheApocalypse*.pdf`, `DDE_OutoftheAbyss*.pdf`, `CurseofStrahdDM*.pdf` | yes (DM/print variants of the store-play season) |
| Playtest-era (D&D Next) adventures | `Prerelease Packet/Adventures and Pre-Gens/…` (Caves of Chaos, Isle of Dread, Mines of Madness, Mud Sorcerer's Tomb, Reclaiming Blingdenstone, Murder in Baldur's Gate supplements) | pre-release rules. **Low weight** |
| Legacy module | `4 Curse of Strahd/TSR-9075-I6-Ravenloft.pdf` | 1983 AD&D. Historical only |

### C. Core rulebooks and rules references (mechanics authority)

| Title | File | Notes |
|---|---|---|
| System Reference Document 5.1 | `System Reference Document.pdf` | **CC BY 4.0: the only freely usable source** |
| Player's Handbook | `0 Core books/D_D 5E - Player's Handbook.pdf`; `Player's Handbook with errata.pdf` | |
| Dungeon Master's Guide | `0 Core books/D_D 5E - Dungeon Master's Guide.pdf` | CR calculation (ch. 9), encounter building, adventure structure (ch. 3) |
| Monster Manual | `0 Core books/D_D 5E - Monster Manual.pdf`; `D_D 5e - Monster Manual (Full-size).pdf` | Stat-block format authority |
| Basic Rules (Player / DM) | `0 Core books/Basic Rules - *.pdf` | Free rules |
| Volo's Guide to Monsters | `0 Core books/Volo's Guide to Monsters.pdf` | Supplement |
| Sword Coast Adventurer's Guide | `0 Core books/D_D 5e - Sword Coast Adventurer's Guide.pdf` | Setting book |
| Elemental Evil Player's Companion | `EE_PlayersCompanion.pdf` | Supplement |

### D. Errata, lists and FAQ

`Errata and Extras/…`: PHB, DMG and MM errata; Sage Advice Compendium; Magic Items by
Rarity; Monsters by CR/Type; Spell Lists; Conversions to 5th Edition. Also `Monsters by CR.pdf`.

### E. Playtest and optional rules (not authority)

`Unearthed Arcana/…` (19 UA articles), `Codex - Unearthed Arcana.pdf`, and the
`Prerelease Packet/` rules PDFs (091913/101413 D&D Next packet).

### F. Organized-play and player material (not audit evidence)

Character sheets, pre-generated characters (`pre-gen/`, `Death house/*.pdf`,
`Elemental-Evil-Pregens.pdf`), AL player guides and logsheets, certs, table tents,
CoS character options, backgrounds and handouts, and the AL "DM Quests" cards. `Curse of Strahd Handouts.pdf`
and the pregen PDFs are **format** evidence for our `08_Handouts.md` and `11_Pregenerated_Characters.md`.

### G. Homebrew and third party (excluded)

`Homebrew - Invocation Drawbacks.pdf`, `DM ONLY/A_Guide_to_Curse_of_Strahd_*`, `Tome of Strahd.pdf`,
`Darker_Gifts_*`, `DM ONLY/Castle Ravenloft.pdf` (unverified provenance).

### H. 3.5 adventures (secondary phrasing evidence)

Red Hand of Doom (text OK), Expedition to Castle Ravenloft (image-heavy; little text),
Expedition to the Demonweb Pits, The Shattered Gates of Slaughtergarde, Eyes of the Lich
Queen (Eberron), Shadowdale (FR). The house style guide `style/analysis/adventures.md`
was already distilled from this era.

## Audit evidence set (what was actually read)

Hardcovers: LMoP, HotDQ, RoT, PotA, OotA, CoS, SKT. Short: CoS Intro (Death House),
DDEX1-1, DDEX2-01, DDEX3-01, DDEX3-06, DDAL04-01/04/05/12/14, DDEP1. Rules: SRD, DMG,
Basic Rules DM. Secondary: Red Hand of Doom.
