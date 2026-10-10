# R6.1 Copyright phrasing scan: Oraga Night 5e

Review-fix pass task R6.1, 2026-10-10. Tool: `conversions/dnd5e/oraga_night/tools/copyright_scan.py`
(tests: `test_copyright_scan.py`; class (b) rulings: `copyright_allow.txt`).

**Result: 0 class (c) hits after the fixes.** The first scan found 52 hits: 27 (a), 18 (b) and
7 (c). All 7 (c) sentences were rewritten. The final scan shows 28 (a), 18 (b) and 0 (c). One of
the rewrites now uses SRD 5.2.1 wording, so it moved to (a).

## Corpus

The extracts were made with PyMuPDF into a session scratch directory. They are not in the repo
and were not committed.

**Official (the comparison corpus, 21 books):**
- *Lost Mine of Phandelver*
- *Hoard of the Dragon Queen*
- *The Rise of Tiamat*
- *Princes of the Apocalypse*
- *Out of the Abyss* (the OCR copy)
- *Curse of Strahd*
- *Curse of Strahd* Introductory Adventure
- *Storm King's Thunder*
- *Dungeon Master's Guide* (2014)
- *Player's Handbook* (2014)
- DDEX1-1 *Defiance in Phlan*
- DDEX2-01 *City of Danger*
- DDEX3-01 *Harried in Hillsfar*
- DDEX3-06 *No Foolish Matter*
- DDAL04-01 *The Suits of the Mists*
- DDAL04-04 *The Marionette*
- DDAL04-05 *The Seer*
- DDAL04-12 *The Raven*
- DDAL04-14 *The Darklord*
- DDEP1 *Corruption in Kryptgarden*
- *Red Hand of Doom* (D&D 3.5)

**Allowed (CC BY 4.0):** System Reference Document 5.1 and SRD 5.2.1 (downloaded from D&D Beyond).

## Method

Page numbers in this report are PDF page indices in the extract, not the printed folios.

1. **Text.** Each module chapter (`*.md` except `INVENTIONS_5e.md` and `STYLE_5e.md`; the read-aloud
   is included) is unwrapped into rendered paragraphs with `lint_5e.unwrap`. The paragraphs are
   split into sentences, and each table cell counts as one sentence.
2. **Normalizing.** The text is lowercased, apostrophes are dropped, other punctuation becomes a
   space, and whitespace is collapsed. In the PDF text, words broken across a line end are
   rejoined.
3. **Shingles.** Every 8-word window in a sentence is a shingle: 4,979 sentences give 43,641
   distinct shingles. Shingles are looked up in the official text, which is treated as one stream
   per book, so a match can cross a sentence or a page. Overlapping matches in one sentence merge
   into a single hit.
4. **Classes.** A hit is (a) when every one of its shingles is also in an SRD. Every other hit was
   judged by hand: (b) for short functional rules grammar, or (c), which must be rewritten.
   `--check` fails on any hit that is neither (a) nor listed in `copyright_allow.txt`. That file
   stores the SHA-1 of each (b) run, never its text.

Re-run with:
`python conversions/dnd5e/oraga_night/tools/copyright_scan.py --refs <official txt dir> --srd <srd txt dir> --check`

## Counts

| Class | First scan | Final |
|---|---|---|
| (a) in SRD 5.1 / 5.2.1 | 27 | 28 |
| (b) generic rules grammar, allowlisted | 18 | 18 |
| (c) distinctive, must fix | 7 | 0 |

The (a) hits are spread across the files as follows: 10 Bestiary 14, 09 Snakes 7, 04 Ball 2,
05 Night 2, 11 Pregens 2 and 08 Handouts 1. Typical (a) runs are "on a failed save or half as
much damage on a successful one", "sheds bright light in a 20-foot radius", "has advantage on
saving throws against spells and other magical effects".

The 18 (b) hits are 14 distinct runs. Each one is functional:
- DC calls: "a DC 15 Strength or Dexterity saving throw" (×4), "must succeed on a DC 13 …"
  (×2).
- Duration and Advantage grammar (×3).
- SRD stat-block sentences with a gendered pronoun in place of "it": Legendary Resistance (×3),
  the Regeneration timing (×3) and the teleport (×2).
- One push save.

None of them carries a description, a name or a turn of phrase.

## Class (c) hits and fixes

| # | Module (first scan) | Excerpt (module) | Official source | Fix |
|---|---|---|---|---|
| 1 | 04_The_Ball.md:344 | "when the characters first come within sight of" | *Curse of Strahd* p. 131 | The read-aloud cue now reads "Read this when the east wing doors come into view:" |
| 2 | 04_The_Ball.md:200 | "If the check fails by 5 or more, Corval…" | DMG p. 242; *Hoard of the Dragon Queen* pp. 75, 80; *Curse of Strahd* p. 72. Not in either SRD | Now "If the check misses by 5 or more", which matches the "A miss by 4 or less" line just above it |
| 3 | 10_Bestiary.md:598 | "can use its Reaction to move up to half its Speed" | PHB p. 75 (a Battle Master maneuver; not in either SRD) | Now "can, as a Reaction, move up to half its Speed and make one attack" |
| 4 | 10_Bestiary.md:654 | same run, followed by "…without provoking Opportunity Attacks" | PHB p. 75 | Now "can, as a Reaction, move up to half its Speed toward…" |
| 5 | 10_Bestiary.md:828 | same run (Direct the Wardens) | PHB p. 75 | Now "can, as a Reaction, move up to half its Speed and make one Mace attack" |
| 6 | 10_Bestiary.md:1771 | same run (the second copy of the Blades' line) | PHB p. 75 | Same wording as #4, so the two copies stay identical |
| 7 | 10_Bestiary.md:2000 | "Bludgeoning damage, and a Large or smaller target is" | DDAL04-01 p. 22 | Now in SRD 5.2.1 form: "Bludgeoning damage. If the target is a Large or smaller creature, it is pushed up to 10 feet away." This is class (a) now |

None of the fixes changes a rule, DC, damage figure, distance or name. The read-aloud text itself
was not changed: only the cue line above the box was.

## Checks after the fixes

- `copyright_scan --check`: 0 (c).
- `lint_5e --check`: 0.
- `fact_check --check`: 0.
- `bestiary_check`: 0 mismatches.
- `pregen_check`: 0 issues.
- `pytest tools`: 407 passed (394 before, plus 13 new).
