# DESIGN — Oraga Night 5e: Official-Module Fix Pass

*Planner output, 2026-09-30. Scope: `conversions/dnd5e/oraga_night/` only. The Facets d20
edition is out of scope; findings tagged `[d20-portable]` are carried over at the end
(T9.4).*

**Inputs.**
- `docs/AUDIT_oraga_5e_official_style.md`: the consolidated audit. Its §5a holds the owner rulings.
- `docs/audit_oraga_5e_official/*.md`: the six slice audits. Every finding ID below (FRONT-n, BALL-n, …) is defined there, with line numbers and before→after wording.
- The yardsticks: `docs/RESEARCH_5e_module_conventions_{structure,voice}.md`.
- Tasks: `docs/TASKS_oraga_5e_official.md`. Log: `docs/LOG_oraga_5e_official_audit.md`.

## 1. Goal and non-goals

**Goal.** The 5e edition reads, looks and runs like an official 5e adventure: SRD 5.2.1 rules
grammar, official book architecture, DM-facing voice, no rules contradictions, and prose that
reads as human-written. No copyrighted text is used.

**Non-goals.**
- No new canon (CLAUDE.md iron law). Anything that needs a new fact waits on an owner ruling (§7).
- No change to the night's design: the Movements, the Uninvited, the snakes, the XP totals and the pillars stay as they are.
- No renumbering of chapters unless the owner rules for it (Q3).
- No edits to `adventures/oraga_night/` (the Facets edition).
- No wholesale rewrites. The prose pass is light-touch and keeps the voice (memory: *prose must read human*).

## 2. Line numbers will drift: the rule for workers

The audits cite line numbers from the text as it stood on 2026-09-30. Every task changes line
numbers for the ones after it. **Workers locate targets by quoted text, not by line.** The
slice audits quote the text at every site. If a quoted phrase is no longer found, the worker
logs it and skips the site. The worker must not guess.

## 3. The 5e style sheet (decided; applies to every task)

These decisions settle the audits' open "pick one scheme" items. Evidence: SRD 5.2.1
(`SRD_CC_v5.2.1.pdf`, downloaded 2026-09-30 from media.dndbeyond.com, CC BY 4.0) was counted
for each term.

| Topic | Rule | Evidence / source |
|---|---|---|
| **Role name** | "the DM" in third person, and "you" when the text instructs the DM. "DM Note", "DM sheet". Never "MM" or "Mirror Master" in the 5e edition. | Owner Q1 |
| **Party** | "the characters" / "a character" by default. "The players" means only the people at the table. "Player character" only where it disambiguates from NPCs. "You" outside read-aloud means only the DM. | C-V1, C-V2 |
| **Rules-term capitals** | SRD 5.2.1 Title Case: Advantage, Disadvantage, Hit Points, Short Rest, Long Rest, Speed, Difficult Terrain, Dim Light, Bright Light, Darkness, Heavily/Lightly Obscured, Half/Three-Quarters Cover, Bloodied, Stable, Heroic Inspiration, and action names (Attack, Dash, Disengage, Dodge, Help, Hide, Influence, Magic, Ready, Search, Study, Utilize). Conditions are written "has the Prone condition" / "is Unconscious". | SRD 5.2.1 counts: Advantage 209 vs 9; Hit Points 345 vs 0; Short Rest 27 vs 0; Prone condition 82 vs 0; Utilize 73. This **overrules** FRONT-10's lowercase recommendation and SNAKES-17's "drop Utilize". |
| **Spells** | Italic Title Case: *Detect Thoughts*, *Tiny Hut*, *Mage Armor*. | SRD 5.2.1 ("cast *Guiding Bolt*") |
| **Magic items and crystal charges** | Italic Title Case: *Steady Light*, *Dark-Burst*, *A Sealed Door*, *House Flare*. Never bold, never roman. | C-S39; BESTIARY-7 |
| **Coin** | "GP", "SP", "CP" in capitals, after a normal space: "10 GP", "1,200 GP". | SRD 5.2.1: GP 396 vs gp 1 |
| **Checks** | "a DC 15 Wisdom (Insight) check"; "succeeds on a DC 13 Charisma (Persuasion) check". Never a bare DC, a DC range, a skill without its ability, or "roll". Alternatives spell out both: "a DC 15 Intelligence (Religion) or DC 15 Charisma (Persuasion) check". Tables may compress to "13 Charisma (Persuasion)". | C-V15; smells S3–S7 |
| **Saves and damage** | "must succeed on a DC 13 Dexterity saving throw or take 7 (2d6) Fire damage" or "…taking 7 (2d6) Fire damage on a failed save, or half as much damage on a successful one". Average first, dice in parentheses, then the damage type in Title Case (5.2.1). Falls may keep bare dice. | C-V18/19; S8–S12 |
| **Numbers** | Numerals for game quantities in DM text ("a 15-foot drop", "for 10 minutes"). Words inside read-aloud boxes. | C-V; S13, S37 |
| **Stat blocks** | SRD 5.2.1 layout throughout Chapter X: bare AC plus a **Gear** line; a single **Immunities** line ("Poison, Psychic; Charmed, Frightened"); "Darkvision 120 ft.; Passive Perception 14"; Advantage folded into the Initiative score; no commentary in numeric fields; limited uses as "(1/Day)", "(3/Day)", "(1/Day Each)"; "When Bloodied" becomes a ***Bloodied.*** trait; epithets go on their own line above the type line. | C-S42; BESTIARY-5/12/13 |
| **Difficulty vocabulary** | SRD 5.2.1 only: Low / Moderate / High, plus "beyond High". "Deadly" never appears in a budget line. One DM Note explains the 2014 multiplier. | C-V24; S34; SNAKES-7/8 |
| **Read-aloud** | An indented italic block, always after a plain trigger line ("Read this when…:"). Italic paragraphs that are **not** indented are notes to the DM. Sidebars never contain read-aloud. Area header → trigger → box → DM text, in that order. | C-S2, C-S12, C-S19–C-S26; FRONT-5 |
| **Box species** | Declared in the legend and used exactly as declared: **Sidebar —**, **DM Note —**, **Troubleshooting —**, ⟨If History Breaks⟩, **What [Name] Says** (Q&A), the fight-card **Wants / Tells / Breaks / Nastier** lines, and the Movement run box. No **Designer's note** (pending Q4). | FRONT-5, CAST-17 |
| **Cross-references** | "(see chapter V)", '(see chapter V, "Down, Not Out")', "(card S2)", "(area B9)", "(Table I–3)". Lowercase "chapter" with a Roman numeral in running text and parentheses, capitalized only at a sentence start. Section names in quotation marks, not italics. No "(source Ch. …)". | C-S41; SNAKES-15/24, CAST-24. The house Roman numerals stay |
| **Spelling** | American (rumor, color, center). "Gray" everywhere, except "grey robes" only if INVENTIONS #43 fixes it as canon (check first). | BALL-22, NIGHT-23 |
| **Emphasis** | No italics for emphasis in DM prose. Italics mark spells, items, section-title book names and non-indented DM notes only. | CAST-24 |
| **Tables** | House numbering ("Table IV–1") stays, as a house choice. Every table gets a title. | FRONT §3 |

This table is also written out as `conversions/dnd5e/oraga_night/STYLE_5e.md` (T0.3), so
workers and later editors have it beside the module.

## 4. Verification tooling (built first, TDD)

Nothing in this module was machine-checked except the two math scripts. Phase 0 builds a
checker, so each task's acceptance criterion is a command rather than an opinion.

`conversions/dnd5e/oraga_night/tools/`
- `bestiary_check.py`, `pregen_check.py`: moved from `docs/audit_oraga_5e_official/`. Each must exit 0 on the current text (the baseline) and after every stat-block or pregen edit.
- `lint_5e.py`: a style linter over the module's `.md` files (excluding `INVENTIONS_5e.md` and `STYLE_5e.md`). Its rules:
  - **Hard (count must reach 0):**
    - the role name: `\bMM\b`, `Mirror Master`;
    - lowercase 5.2.1 terms from §3;
    - bare or ranged DCs (S3–S5, plus `DC \d+(?! (Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma))` outside tables);
    - "roll" for a check (S6), "beat/pass the DC" (S7), save or damage templates (S8–S12);
    - conversion talk: `\bthe source\b`, `\bthe original\b`, `this edition`, `\(source Ch`, `New in this edition`;
    - narrator voice: `the module (would|notes|suggests|prefers|intends|has spent)`, `Honest (note|warning)`;
    - designer "we" (S28), "Deadly" in a budget line (S34), `\bPCs?\b` (S1), spelled-out distances in DM text (S37), `\bgp\b`, British spellings from the BALL-22 list, `grey` (outside the whitelist), `Designer's note`;
    - the removed Attendant habit: `direct question`, `literally and truthfully`.
  - **Soft (reported as metrics, with per-file targets):**
    - mean words per sentence in DM prose (target ≤ 19) and the share of sentences over 30 words (target ≤ 12%);
    - em dashes per 1,000 words (target ≤ 8);
    - paragraphs over 120 words outside background blocks (target ≤ 3 per file);
    - counts of "the players" (S2), "player character", "you" in non-box DM prose, "perhaps" (S25), rhetorical questions (S27), and "not X but Y" / ", not" constructions.
  - **Structure:**
    - every "(see chapter N, "Title")" and "(card SN)" / "(area BN)" / "Table N–N" reference resolves to a heading or table in the module;
    - every **bold** creature name at first mention in chapters IV, V and IX exists as a stat block in chapter X;
    - read-aloud blocks are preceded by a trigger line.
  - A whitelist file, `tools/lint_5e_allow.txt`, holds file:quoted-text exceptions with a reason (for example, "the players" where it means the people).
- `test_lint_5e.py`: pytest with fixtures. At least 3 tests per rule family (hit, miss, edge), per the CLAUDE.md coverage rule.

Run from the repo root: `python conversions/dnd5e/oraga_night/tools/lint_5e.py [--baseline|--check]`.
`--baseline` writes `tools/lint_baseline.json`. `--check` exits non-zero if any hard rule has hits
or any soft metric regresses against the baseline. Every task's acceptance names the rule
families that must be at 0 for the files it touched.

## 5. Order of work, and why

Several streams rewrite the same sentences. The order is chosen so that no pass undoes an earlier one.

| Phase | Stream | Why here |
|---|---|---|
| 0 | Tooling, style sheet, baseline | Every later acceptance check depends on it |
| 1 | P1 contradictions and the owner rulings already given (Q2, Q5, Q6) | Changes rules; must precede wording sweeps |
| 2 | Architecture: agendas move, front matter, dedupes, handouts | Moves text between files; sweeps must see the final layout |
| 3 | Mechanics fixes, one task per chapter | Changes numbers and rules text before its grammar is normalized |
| 4 | Module-wide mechanical sweeps (DM, capitals, check grammar, stat-block layout, cross-refs, names, spelling) | Largely scriptable, and safe once content is stable |
| 5 | Read-aloud and styling | Needs the final box and legend rules from Phase 2 |
| 6 | NPC knowledge lists | Content from printed facts; the prose pass will polish it |
| 7 | Prose voice, per chapter, **04 first as a pilot with an owner review gate** | Last, so it polishes final text once |
| 8 | Canon-gated tasks, as rulings arrive | Can slot in any time after Phase 2 |
| 9 | Ledger, flow page, full verification, d20 carryover | Closeout |

Phases 3's chapter tasks are independent of each other and can run in parallel (separate files).
The Phase 7 chapter tasks are also parallel, after the pilot is approved.

## 6. Decisions this plan makes (Planner level; logged in DECISIONS.md as O1–O8)

- **O1. Style sheet (§3) follows SRD 5.2.1 casing module-wide.** Rationale: the module declares 5.2.1, its stat blocks are 5.2.1, and 5.2.1 capitalizes. 2014 tables read the capitals without trouble.
- **O2. The Attendant becomes Focused on the §5b trigger** (NIGHT-1). It vanishes for the rest of that Movement only (BALL-2, N4). S14's +2 counts only habits the table actually saw.
- **O3. After Q5, the Attendant has three habits** (crystal and light; the cup and cloak; music), shown in Movements I, II, IV and V. The Movement III sighting (04 "The quiet guest — the literal answer") is **cut, not replaced**, because a replacement would be new canon. S14's "argue its orders" out keeps its check but loses the "direct question" line. *Owner confirmed 2026-10-03 (Q22): no replacement habit.*
- **O4. The Leashed return point** is the space where the creature dropped (the Hollow keeps "within 60 feet of the doors he holds") (NIGHT-2).
- **O5. The *detain* mercy** defers to the Bought Blade's *To the Terms* (1 HP and Grappled) (BESTIARY-1).
- **O6. The agendas move to Chapter II's DM-only half** as "The Eight Agendas" (Q2 said move; Planner picks the destination). Chapter II is already flagged DM-only and holds the night's secrets. Chapter III keeps a player-safe paragraph pointing at Handout 2.
- **O7. The Seating Feud** defaults to Movement II, with Movement III as a fallback, and is over before the toast (BALL-8, N5).
- **O8. Book organization defaults to the regroup option** (FRONT-11): README grouped as Before the Night / The Night / Appendices, and no renumbering. If the owner rules otherwise on Q3, T8.1 does the renumber.

Numbers the Planner sets, from arithmetic (with no simulator available the numbers are marked *unsimulated*, and the table should confirm them):
- NIGHT-5 "Adjusting the Attack" values, as proposed in NIGHT.md.
- The Midnight Clock default (NIGHT-3 item 5): the Radiant reaches the garden stair **three beats after Raunu falls**. That puts the Crossing at the same point the text's order implies, after the crowd reaches B12. T3.2 checks it against the sequence in 05 and 08 and records it as O9 in DECISIONS.
- BESTIARY-4: Kovaun goes to CR 1/2. S8 is rebudgeted.

## 7. Open owner rulings (gates)

From AUDIT §5, still open: **Q3, Q4, Q7–Q20**. Added by this plan:
- ✅ **Q21: approve the redundancy cuts.** Approved 2026-10-03. These are pass 2's pending "cuts I'd recommend": trim 04's *The Snakes in the Pen* to a table plus a pointer, and trim 05's section (renamed "The Snakes in the Dark") to Table V–7 plus card pointers (FRONT-9, SNAKES-28). They were left for the owner in pass 2.
- ✅ **Q22: veto O3?** No; no replacement habit (2026-10-03). Do you want a replacement Attendant habit for Movement III? (That would be new canon, from you.)

Tasks gated on a ruling are marked **GATED(Qn)** in TASKS. Every other task can run now.

## 8. Risks

| Risk | Mitigation |
|---|---|
| The sweeps mangle read-aloud text, quotations, or the canonical invitation text (Handout 1 is marked canonical) | Sweeps skip indented italic blocks and quoted speech unless the rule says otherwise. The linter reports and the worker edits; there is no blind `sed`. Handout 1 goes on the whitelist |
| The prose pass flattens the voice | The Chapter 04 pilot goes to the owner before the other chapters. Slice before→after examples are the model. Keep the jokes the audits flagged as earning their place |
| Line-number drift | §2 rule: locate by quoted text |
| Hidden new canon in the "from printed facts" content (the dinner scene, knowledge lists, Background, Overview, new boxes) | Each such task lists its permitted sources, and T9.1 adds each new block to INVENTIONS_5e.md with its sources for owner review |
| Cross-file drift (08 mirrors 05/09; 10 mirrors 05) | Every mechanics task lists its mirror sites. The linter's structure checks and the two math scripts run in every acceptance |
| Scope creep into the Facets edition | Out of scope. Items that affect both editions (Q10, FRONT-21 aphorisms) are logged in the d20 carryover doc (T9.4) |
