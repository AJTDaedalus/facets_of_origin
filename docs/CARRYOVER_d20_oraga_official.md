# CARRYOVER — Oraga Night 5e official pass → a future Facets d20 edition

*Record only (T9.4, 2026-10-03). Nothing here has been applied. The d20 edition is out of
scope until the owner opens it.*

## 1. What this is, and how to use it

The 5e official-module audit (`docs/audit_oraga_5e_official/*.md`) tagged 67 findings
`[d20-portable]`, plus four inline fixes in SNAKES. Those lessons would apply to a Facets d20
version of Oraga Night too. This file records each lesson, how 5e solved it, and where it
would land.

**There is no Facets d20 Oraga Night yet.** `COMPARISON.md` lists two editions:
the **Facets edition** at `adventures/oraga_night/` (Lean Facets rules) and the **5e edition**
at `conversions/dnd5e/oraga_night/`. `facets_d20/` is a ruleset with no adventure in it.
`docs/BRIEF_facets_d20.md` §2.6 says SRD adventures run under d20 with "light-touch
conversion", and calls the 5e Oraga "a stepping stone". Its open question 3 ("Does the Oraga
Night 5e edition become the first Facets d20 adventure later?") is answered "Not now". So a d20
edition will start from one of two places:

- **Fork from the 5e edition (likely).** Most lessons are already applied. The work is
  re-skinning the 5e rules wording into d20 terms. See the *Adapt* column and §1a.
- **Fork from the Facets edition.** The inherited problems are still in the source: the
  agendas sit in the player chapter, the contract case, the aphorisms, sixty or eighty
  servants, the Handout 3 rumor table, the "one page" tracker. Apply the *Lesson* column
  directly.

The **Target** column names the Facets-edition site (`F:` = `adventures/oraga_night/`), where
the problem was inherited from, when a quick grep found it. "5e-only" means the content is a
5e invention (the snake cards S1–S14, the Attendant, the heat tracker, chapter X, the
pregenerated characters in chapter XI). That content matters only for a fork from 5e. "check"
means the grep found nothing definite.

**How to use:** pick the fork source, then go down the table. For each row, open the 5e
evidence (the slice file's §5 table gives HEAD line numbers at `cd174bf`) and copy the shape of
the fix, not its 5e wording.

### 1a. d20 vocabulary that differs from the 5e fix (check before porting any row)

| 5e edition (as fixed) | Facets d20 (`facets_d20/`) |
|---|---|
| "the DM" (owner Q1, 5e only) | **MM / Mirror Master** (`09_Mirror_Masters_Guide.md` L3). The Facets editions keep MM. |
| SRD 5.2.1 Title Case: Advantage, Hit Points, Short Rest (O1, O16) | lowercase "advantage", "short and long rests" (`01_What_Is_Different.md` L9). **Do not port O1 blindly.** |
| Heroic Inspiration | **Sparks** (`09` "Sparks") |
| XP awards; Low/Moderate/High budget labels (O22) | no XP (`09` "Levels"); **Threat** budget with the four tiers Skirmish/Clash/Battle/Desperate (`09` Table 9–1) |
| CR and the 2014 multiplier note | Threat pricing (`09` "Pricing Any SRD Monster") |
| 2014-table notes | probably unneeded |
| `lint_5e.py` role_name, lowercase_terms, deadly_budget, gp | 5e-specific: invert or retarget (see §5) |

---

## 2. The d20-portable findings (71: 67 tagged headers + 4 inline)

*Adapt:* **No** = a pure prose or structure lesson. **Light** = a vocabulary swap per §1a.
**Yes** = 5e rules wording that must be redone in d20 terms. **5e-only** = the content does not
exist in the Facets edition. *Phase* = the 5e fix-pass phase/task (commit `Oraga 5e official
pass: Phase N …`).

### FRONT (front matter, architecture; 5e ch. I–III, VI, README)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| FRONT-1 | Never put MM-only secrets ("At midnight" lines, the Vell reveal) in a player-facing chapter | Q2/O6: agendas moved to ch. II's DM-only half "The Eight Agendas". Ch. III keeps a pointer to Handout 2 (T2.1) | `F:03_Masks_and_Agendas.md` ("At midnight" ×13); `F:08_Handouts.md` L25 points players at ch. III | No |
| FRONT-3 | Open with an Adventure Background before the running rules | 01 "## Adventure Background", built only from ch. II facts; INVENTIONS #60 (T2.2) | `F:01_Overture.md` (none present) | No |
| FRONT-4 | The Overview must say flatly what happens in each part | 01 "**Overview.**", one line per Movement, checked against the chapter text; #61 (T2.2) | `F:01_Overture.md` (none present) | No |
| FRONT-6 | A signed designer's note doesn't read as an official book | **Gated Q4.** Still printed; whitelisted in `lint_5e_allow.txt` | `F:01_Overture.md` L134–142 | No (owner call) |
| FRONT-7 | Conversion talk ("the original", "this edition", "the module notes…") in MM prose | Lint family `conversion_talk` to 0; light rewrites (T7.1–T7.7) | `F:` has "the module" ×57; check for edition talk | No |
| FRONT-11 | The chapter order and grouping should read like an official book | O8: README regrouped as Before the Night / The Night / Appendices, with no renumbering (Q3 gated) (T2.3) | `F:README.md` | No |
| FRONT-12 | Invented proper nouns have no gloss or pronunciation | **Gated Q17** (3164 PG, "Mazaaian", the Blackwatch) | `F:README.md` L6, `F:06_Aftermath.md` L80, `F:02` L25 | No (owner call) |
| FRONT-21 | Inherited aphorisms and not-X-but-Y turns | Light-touch rewrites (T7.6): README, 02, 03; "load-bearing" kept once; 03 em dashes 49 → 5 | See §3.3 (every site is in `F:`) | No |
| FRONT-23 | No closing rewards recap | 06 "## Rewards": Table I–4, the agenda Pays lines, the loot, the story award (T2.6) | `F:06_Aftermath.md` | Yes (Sparks and levels, not XP) |

### BALL (5e ch. IV, The Ball → `F:04_The_Ball.md`)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| BALL-1 | A promised scene (Agenda 4's dinner for two) needs a way in and a written scene | Q6: the ring at the east-wing doors; `#### Dinner for Two (B9)` built only from ch. VII facts; #58 (T1.6). Leftovers gated on Q7 and Q23 | `F:04` (dinner ×3), `F:03` L128, `F:08` L40 | No |
| BALL-2 | A creature's vanish rule contradicted its one-sighting-per-Movement rule | O2: gone for the rest of that Movement only (T1.2) | 5e-only (the Attendant) | 5e-only |
| BALL-3 | Read-aloud boxes sat above their area headers, and the MM text restated them | Order: header, trigger, box, MM text; restatements cut (T5.1) | `F:04` keyed areas | No |
| BALL-4 | A box gave away what a check gates | The chapel box ends on the niches; the offerings moved behind the check (T5.1) | `F:04` chapel (B6) | Light |
| BALL-5 | MM text was set in read-aloud italics, against the legend | Summons and toast turned into roman MM subsections with quoted speech (T5.1) | `F:04` summons, toast | No |
| BALL-6 | A failed invitation check at the gate had no result | Fail by 5+: refused; the kitchens (B10) are the way in (T3.1) | `F:04` B0 | Light |
| BALL-7 | Several checks had no stated result | Results added: B0, B3, Mv II gratitude, Mv III summons (T3.1) | `F:04` | Light |
| BALL-8 | The Seating Feud's timing contradicted itself and collided with the toast | O7: Movement II by default, III as the fallback, over before the toast (T3.1) | `F:04` (×2), `F:09` (×2) | No |
| BALL-9 | A set piece (the summons) had no end trigger and no default | O12: four guests, at least one and by default two of them PCs; about five questions or five minutes; a friendly trigger with a default (T3.1) | `F:04`, `F:07` summons | No |
| BALL-11 | Withholding an NPC's identity from the MM ("tall, pale factor") | "(This is Master Vell; see chapter VII.)" at first mention (T6.1) | `F:04`, `F:07` ("factor") | No |
| BALL-13 | MM prose runs long in sentences and paragraphs | Pilot T7.1: 0 paragraphs over 120 words; bold run-ins and bullets (B8 is the model) | `F:04` | No |
| BALL-14 | AI-rhythm cluster: em-dash density, "not X but Y", inflated asides | T7.1 cuts (see LOG "Phase 7 — T7.1 pilot") | `F:04` | No |
| BALL-17 | Scheduled beats give no latitude for absent PCs; a box assumes they are present | The toast can be held and the news travels; the Dead Dance trigger says who hears the box (T3.1) | `F:04` Mv IV–V beats | No |
| BALL-20 | "Players" used for the characters | "the characters" by default; "player character" only to set PCs apart from NPC guests (T7.1) | `F:04` ("players" ×15) | No |
| BALL-21 | Hedges, rhetorical questions, designer-voice asides | "perhaps" → "about"; questions turned into statements (T7.1) | `F:04` | No |
| BALL-23 | Continuity and conversion leftovers in B0 and Movement I | Small fixes (T5.1) | check | No |

### NIGHT (5e ch. V, The Longest Night → `F:05_The_Longest_Night.md`)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| NIGHT-3 | Beats, rounds and the clock share no unit, and the clock is never stated in one place | "A beat and a round cost the same: one turn". **The Midnight Clock** is the one statement; O9 default: three beats after Raunu falls (T3.2) | `F:05` L7, L29, L86–99 | Yes (d20 rounds) |
| NIGHT-8 | One name ("Knives in the Dark") for two different things | 05 section renamed "The Snakes in the Dark"; S2 renamed "The Service Corridor Job" (T2.4). **Partly:** one pointer broke across a line and was missed (see §4.6) | `F:09` S2 title; `F:01`, `F:04` | No |
| NIGHT-9 | The set pieces after midnight have no read-aloud, and their mood sits in MM prose | New boxes (the Crossing, Movement VII) built only from printed text; #66, #67 (T5.3) | `F:05` (8 boxes) | No |
| NIGHT-11 | The module's own read-aloud device is used inconsistently | Box italic; MM paragraphs roman (T5.2) | `F:05` | No |
| NIGHT-13 | How the party and the players are named | "the characters" by default. **Partly:** player-"you" left in three room-trick rows | `F:05` ("players" ×15) | No |
| NIGHT-14 | Rhythm: long sentences, long paragraphs, AI-rhythm figures | T7.2 at the calibrated targets. **Partly:** two negative triplets kept as voice | `F:05` | No |
| NIGHT-15 | Where the contract case is | **Gated Q10** (`TODO-Q10`). Inherited; see §3.2 | `F:05` L327/L333/L359, `F:09` L127/L174/L199, `F:enemies/bought_captain.fof` L23, `bought_sergeant.fof` L35 | No (owner call) |
| NIGHT-18 | No General Features or fight-space geometry for the palace after midnight | *The Palace After Midnight: General Features* (light, crowd, smoke, fire). Dimensions **gated Q13** (T3.2) | `F:05` (none present) | Yes (hazard numbers) |
| NIGHT-23 | First-mention styling and small consistency slips | Bold first mention with a pointer, then lowercase common nouns (T5.4). The bold-for-stat-block part is 5e convention | check | Light ("except the bold") |

### SNAKES (5e ch. IX, the fight cards; partly → `F:09_Scene_Cards.md`)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| SNAKES-2 | The tracker misses heat changes the cards make | Table IX–2 and Table VIII–5 gained the missing rows (T3.3). Two still missing (NEW-SNAKES-4) | 5e-only (heat) | 5e-only |
| SNAKES-4 *(prose part)* | No card states surprise or detection; boxes hard-code being spotted | A default line ("nobody is surprised…") plus detection lines on four cards (T3.3) | `F:09` S1–S3 boxes, e.g. L127 | Yes (d20 has side initiative) |
| SNAKES-9 *(inline)* | A card fires whatever the heat, but the chapter IV box gates it on heat 3 | S10 gated on heat 3+; table header "What heat 3–4 sets off" (T3.3) | 5e-only | 5e-only |
| SNAKES-10 | MM prose addresses the players as "you"; "player character" crowds out "the characters" | Option (b): "player character" cut from 74 to 2 uses (T7.3) | `F:09` | No |
| SNAKES-11 | Narrator voice and AI rhythm | 13 lines cut or reworded; `narrator_voice` at 0 (T7.3) | `F:09` | No |
| SNAKES-12 *(label only)* | Treasure is a pointer, not itemized where it is found | A run-in **Treasure** field, value inline, pointer kept (T3.3). The values are 5e | `F:09` | Light (label; d20 Table 9–5 values) |
| SNAKES-13 | "Walk into it / Turn it / Snake on snake" run together in one paragraph | One paragraph each (T5.4) | 5e-only | 5e-only |
| SNAKES-15 | Cross-references read "(Chapter X)"; the official form is "(see chapter X)" | Scripted pass, 334 changes (T4.5). **Partly:** five pointers lack "see" | `F:` "(Chapter" ×16 | No |
| SNAKES-19 *(inline)* | Distances spelled out in MM prose | Numerals ("12-foot drop"); lint `spelled_distance` (T4.3) | `F:` 2 hits | No |
| SNAKES-24 | Provenance citations point outside the book | "source"/"V3" glosses cut; "(see chapter VII)" (T4.5) | check | No |
| SNAKES-25 | Card order doesn't follow the night; two section names collide | S2 renamed (T2.4). **Partly:** "The Snakes in the Pen" is still the heading in both 09 and 04 | `F:09` order table L12 | No |
| SNAKES-28 | Rules printed in 01, 04, 05 and 08 as well | Q21 cuts: 04 and 05 trimmed to a table plus pointers; 08 keeps a named compression (T2.4) | `F:01`, `F:04`, `F:05`, `F:08` "Optional Steel" | No |

### BESTIARY (5e ch. X → `F:enemies/*.fof` + `F:09` blocks)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| BESTIARY-7 | Item names (crystal charges) appear in five typographic forms | Italic Title Case everywhere (T4.2) | `F:` "charge" in 01, 05, 08, 09 | Light (pick the d20 house form) |
| BESTIARY-10 | MM-facing lines address the characters as "you" | Recast to "the characters" / "the party" (T7.5) | `F:enemies/*.fof` | No |
| BESTIARY-15 | AI rhythm: negative parallelism, tricolons, em dashes | Em dashes 104 → 54 (T7.5). **Partly:** two "not X" lines kept | `F:enemies/*.fof` (e.g. `bought_sergeant.fof` L36) | No |
| BESTIARY-19 | A rule printed twice drifted apart (the Fracture) | 10's copy is now a compression of 05's, with a pointer (T2.4) | `F:05` Fractures vs `F:08` L189 | No |

### CAST (5e ch. VII, VIII, XI → `F:07`, `F:08`, `F:characters/`)

| ID | Lesson | How 5e solved it | Target | Adapt |
|---|---|---|---|---|
| CAST-1 | A mechanic (the Attendant answers truthfully) with the content left unwritten | **Void**: owner Q5 removed the habit (T1.3). See §3.1 | 5e-only; the Facets edition has no Attendant | 5e-only |
| CAST-2 | Most talkable NPCs have no written "what they know" | "What [Name] Knows" lists, each bullet sourced from printed text; #68 (T6.1) | `F:07` | No |
| CAST-3 | The chapter promised a DC in every entry; half had none | O14: one default-DC sentence in the intro (T3.5) | `F:07` | Light |
| CAST-4 | Vell's DCs name no ability, and one check hides behind an undefined gate | DC 25 Charisma (…); Insight with no gate (T3.5) | `F:07` Vell | Light ("in shape") |
| CAST-5 | The module appears as a character in MM prose | Winks rewritten; the real "never explains" lines kept (T7.4) | `F:07` ("the module" ×8) | No |
| CAST-6 | "Player" used for the character | Fixed (T7.4) | `F:07` | No |
| CAST-7 | Em-dash chains and "not X. It is Y" | Em dashes 129 → 45 (T7.4) | `F:07` L365 ("not what was taken… It is how much is left") | No |
| CAST-8 | An MM table filed as a player handout | "Rumors at the Ball *(DM table)*", outside Player Handouts (T2.5) | `F:08` "Handout 3 — The Rumor Table" | No |
| CAST-9 | A handout with no trigger and no recipient | Trigger line added; text untouched (T2.5) | `F:08` Handout 1 | No |
| CAST-10 | Pregens lack ideal, bond and flaw | **Gated Q16** | `F:characters/*.fof` | Light (d20 has Drives) |
| CAST-15 | Cast headers are uneven | Appositions plus pointers (T5.4) | `F:07` | No |
| CAST-16 | The personality block is a house shape, not an official one | "Roleplaying [Name]" plus **Quote:** lines (T5.4) | `F:07` | No |
| CAST-17 | Box labels don't match the legend's box types | "What [Name] Says", "DM Note — …" (T5.2) | `F:07` | Light (MM Note) |
| CAST-18 | A duplicated read-aloud and a duplicated quote | One copy plus a pointer (T5.2) | `F:07` | No |
| CAST-19 | DCs sit off the module's own ladder | O13: Callun DC 20; "Hard 18–20" (T3.5) | `F:07` | Light |
| CAST-20 | The intro miscounts the snakes | Recounted (T3.5) | 5e-only | 5e-only |
| CAST-23 | The rumor table has no truth notes where the module knows the answer | Notes on rumors 6, 8 and 11 only (T6.1) | `F:08` rumor table | No |
| CAST-24 | Cross-reference and emphasis typography | Prose done (T4.5, T9 italics sweep). **Partly:** "(Ch. IX)" left in Table VIII–1 | `F:08` "Ch. IV/V" (L157–204) | No |
| CAST-25 | Handout placement and naming | Grouped under "Player Handouts", "Player Handout N: …" (T2.5) | `F:08` | No |
| CAST-26 | The "one page" MM sheet is longer than a page | "The Night on Two Pages", split at *The pillars* (T2.5) | `F:08` L86 "One page." | No |
| CAST-27 | The palace diagram gives one key to three places | One "B5 THE GARDENS" box (T2.5) | `F:08` B5 | No |

---

## 3. Owner rulings that touch both editions

### 3.1 Q5: the Attendant's truthful-answer habit

**Grep result: no analog.** The Facets edition has no Attendant or "quiet guest" (`grep -i
"attendant\|quiet guest" adventures/oraga_night` = 0). Neither it nor `facets_d20/` has
"truthful", "literal answer" or "direct question". The habit was 5e invention #55, and the
owner removed it ("a weird mechanic I don't like"). A d20 fork from 5e inherits the version
**without** it: three habits; the Movement III sighting cut, not replaced (O3, Q22). Do not
bring back a fourth habit. That would be new canon.

### 3.2 Q10: the contract case (NIGHT-15), inherited

The mismatch is in the Facets source:
- The captain carries it: `F:05_The_Longest_Night.md` L327 ("a case chained to the captain's
  belt"), L333 ("which the captain alone has read"), `F:09_Scene_Cards.md` L174, and
  `F:enemies/bought_captain.fof` L23.
- A sergeant holds it at the gate before the captain is in the scene: `F:05` L359 (box) and
  `F:09` L127 (box). Also `F:enemies/bought_sergeant.fof` L14/L35 ("drawn first", "chained at
  the hip") and `F:09` L199 ("a captured Sergeant, contract case and all").

The audit recommends that the sergeant carries it and the captain alone has read the Second
Clause. **Still open.** One ruling fixes all three trees (Facets, 5e and any d20 edition). The 5e
site carries `<!-- TODO-Q10 -->`.

### 3.3 FRONT-21: the inherited aphorisms

5e fixed its copies (T7.6). Every one is still in the Facets edition:
- `F:README.md` L58 "not to tease you, but because…"
- `F:01_Overture.md` L104 and L211, "load-bearing" twice (keep one). Also `F:07` L80 "the
  load-bearing wall of his personality".
- `F:02_The_World_and_the_Night.md` L119 "not what was taken from them but…", and `F:07`
  L365, which has the same figure split into two sentences.
- `F:02` L210 "Not because the answers are dull — but…"
- `F:03_Masks_and_Agendas.md`: "not a problem but a spotlight" and "knowledge, not a bonus"
  (check the current wording). L58 "nobody and everybody" earns its place, so keep it.
  57 em dashes in 2,908 words.

Fix with a light touch (memory rule: keep the voice). The 5e replacement wording is in
`FRONT.md` FRONT-21.

### 3.4 Q11: Essin's "two bodies"

The source is `F:07_Cast_of_the_Ball.md` L268, "knows exactly where its two bodies are
[buried]". It could be the idiom or literal corpses. The 5e edition reads it literally and makes
it a bargaining chip (S13 *Broker a trade*, the Boranis line). **Gated** (`TODO-Q11` at 5e 07
and 09). If the owner says "idiom", the Facets wording stands and the 5e S13 out changes. If
"literal", it becomes canon for every edition.

### 3.5 Other cross-edition canon items (all open unless marked)

| Q | Item | Facets-edition site |
|---|---|---|
| Q1 | DM in 5e only; **the Facets editions keep MM** (ruled) | the d20 rules use MM |
| Q2 | Agendas out of the player chapter (ruled for 5e) | `F:03` and `F:08` L25 still route players to the "At midnight" notes |
| Q4 | The signed designer's note | `F:01` L134–142 |
| Q6 / Q23 | The ring at the east-wing doors (ruled 5e); "no husband" vs Raunu at the dinner (open) | `F:03` L128, `F:08` L40 |
| Q7 | May Veier confirm the pregnancy? | `F:01` L292, `F:06` L38 |
| Q8 | Attacking Master Vell: what does the table see? | `F:05` (Vell ×13) |
| Q9 | Trapping an Uninvited: does Raunu live? | `F:05` L448 |
| Q13 | Room sizes after midnight | `F:05`, `F:08` diagram |
| Q14 | Full XP for walk-away outs | moot under d20 (no XP); the Sparks analog is `F:09` L197 |
| Q15 | Prices and values (Callun's fee, the Church's favor, the coat) | `F:04`, `F:03` |
| Q16 | Pregen flaw; Ilesse's crystal as holy symbol | `F:characters/ilesse.fof` |
| Q17 | Pronunciations; "3164 PG"; the Blackwatch and Mazaa glosses | `F:README.md` L6, `F:06` L80, `F:02` L25 |
| Q19 | Initials on the agenda cards ("— R.C.") | `F:08` L29–41 |
| Q20 | **Sixty or eighty servants** (inherited: `F:07` L155 "sixty" vs `F:04` L491/L503 "eighty"); **the testament's witnesses** (`F:01` L6 "a Church notary and two witnesses" vs `F:04` L506 / `F:07` L132, Corval stood witness) | as listed |
| Q21 / Q22 | Redundancy cuts approved; no replacement habit (ruled, 5e) | — |

Q3, Q12 and Q18 are 5e-only: renumbering the 5e book, the S9 card, and alignment.

---

## 4. Process lessons

1. **Lint first, then fix.** Phase 0 built `lint_5e.py` test-first (124 tests, later 159),
   ported the math checkers, wrote `STYLE_5e.md` and recorded a baseline. That came before any
   module edit. Every later task ran `--check`, so regressions failed fast: 459 hard hits went
   to 0, and 2 structure hits went to 0. Re-baseline only after a task moves text between
   files, check that the total did not rise, and log it.
2. **Slice audits.** Six parallel auditors each took one slice. FRONT also owned the whole
   architecture; BESTIARY and CAST checked the math by script. Each finding had an ID, a P1–P3
   rating, a checklist citation and quoted text, and the slices were then consolidated (152
   findings, 20 owner Qs). Two conventions research docs (C-S1…52, C-V1…26, smells S1…S40) came
   first. Shared-brief errors spread to every slice (the party level was sent as 3rd and had to
   be corrected to 4th), so check the brief before fan-out.
3. **Sequencing** (DESIGN §5): tooling → P1 contradictions and rulings already given → architecture
   (moves text between files) → mechanics per chapter → mechanical sweeps → read-aloud and
   styling → knowledge lists → prose voice **last** → canon-gated tasks → ledger and
   verification. Rules change before wording, and sweeps see the final layout. Prose polishes
   the final text once.
4. **The line-drift rule** (DESIGN §2): audits cite lines that drift after the first edit.
   **Locate every site by quoted text, assert that it matches exactly once, and log and skip if
   it is gone. Never guess.** Every phase log records "Every edit was located by quoted text".
   It worked: zero skipped sites.
5. **Parallel workers and the shared scratchpad.** The Phase 7 workers ran in parallel on
   separate files. Each kept pre-edit snapshots and diff scripts in the one session scratchpad
   (see `prose_T7.4-5.md` and `prose_T7.6-7.md`). With the same scratchpad and generic file
   names, one worker can overwrite another's snapshot or script, and the number/DC diff then
   compares against the wrong baseline. **Give each worker its own subfolder
   (`scratchpad/T7.3/…`) and prefix file names with the task ID.** Separate files are not
   enough when scratch space is shared. *(The LOG does not record the incident in detail. This
   is from the coordinator's brief.)*
6. **Pilot, then calibrate.** The ch. IV prose pilot (T7.1) hit every target, but it
   **overshot**: 13.46 words a sentence and 1.54 em dashes per 1,000 words, against ceilings of
   19 and 8. That reads clipped. The coordinator set a band for T7.2–T7.7: **14–19 words a
   sentence and about 3–8 em dashes per 1,000, without atomizing.** Lesson: give prose targets
   as **bands with floors**, not ceilings alone, and send one chapter's before/after samples to
   the owner before fanning out.
7. **Joined-line greps.** Pointers and rules wrap across lines in Markdown. The
   "Knives in the Dark" rename missed `("Knives in the` / `Dark", Phern)` at 05 L173–174
   (NIGHT-8 partly fixed). The linter already reads a bare "DC 15 Strength /
   saving throw" across the wrap, and T4.3 grepped for wrapped "or DC" alternatives. **For any
   rename or pointer sweep, grep a whitespace-normalized copy** (e.g.
   `tr '\n' ' ' < f | grep -o 'Knives in the Dark'`, or Python `re.sub(r'\s+',' ',text)`),
   then map hits back to line numbers.
8. **Smaller ones.** Number-preserving prose passes: a script diffs every `DC n`, dice
   expression and numeral before and after (T7.x). Every new block needs a ledger row in
   INVENTIONS with its sources (T9.1), because "from printed facts" content hides new canon.
   Cross-file mirrors (08 ↔ 05/09, 10 ↔ 05) are listed in every mechanics task. Flow-page
   anchors break when a heading gains an italic tag (T9.2, 19 refs).

---

## 5. Tools worth porting

All in `conversions/dnd5e/oraga_night/tools/` (pytest: `test_lint_5e.py`,
`test_bestiary_check.py`, `test_pregen_check.py`, fixtures in `fixtures/`).

**`lint_5e.py`** has three tiers: **hard** (must reach 0), **soft** (per-file metrics with
targets and tolerances), and **structure** (cross-file). It also has a baseline/`--check`
ratchet, a whitelist file (`file|quoted text|reason`), and line classes (read-aloud =
`> *`-led blockquote; quoted speech blanked; tables skipped for compression rules).

| Rule family | What it catches | For d20 |
|---|---|---|
| `role_name` | "MM", "Mirror Master" | **5e-specific; invert** (d20 forbids "DM"/"GM") |
| `lowercase_terms` | lowercase 5.2.1 rules terms | **5e-specific; invert or drop** (d20 lowercases advantage and rests) |
| `bare_dc` | DC with no ability, ranges, skill-only checks | Portable (d20 uses DCs); align with d20 check grammar |
| `roll_check` | "roll Strength", "beat the DC" | Portable if the d20 house grammar matches |
| `save_damage` | save template, bare dice, damage type | Partly portable: d20 uses **fixed damage** for monsters |
| `conversion_talk` | "the source", "the original", "this edition" | Portable |
| `narrator_voice` | "the module intends/notes…", "Honest note" | Portable |
| `designer_we` | we/our in MM prose | Portable |
| `deadly_budget` | 2014 "Deadly" on 5.2.1 budget lines | **5e-specific**; retarget to d20 tier words (Skirmish/Clash/Battle/Desperate) |
| `pcs` | "PC(s)" | Portable |
| `spelled_distance` | "twelve-foot" | Portable |
| `gp`, `british_spelling`, `grey` | house spelling | Portable (house choices) |
| `designers_note` | the signed note | Portable, pending Q4 |
| `attendant_habit` | the removed Q5 habit | 5e-only (the guard against reintroduction) |
| soft metrics | words a sentence, share of sentences over 30 words, em dashes/1k, paragraphs over 120 words; counts of "the players", "player character", "you", "perhaps", rhetorical questions, "not…but" | Portable. **Add floors** (§4.6) |
| structure `xref` | chapter/section/card/area/table pointers resolve | Portable once d20 chapter names are set |
| structure `creature_bold` | a bold creature name has a ch. X block | Needs a d20 stat-block home (5e ch. X ≈ `F:enemies/`) |
| structure `readaloud_trigger` | every box has a trigger line ending in ":" | Portable |

**`bestiary_check.py`**: re-derives each block's HP from its hit dice, ability modifiers, saves,
skills and XP, and cross-checks hand-entered AC/HP/CR/Gear/Initiative against the chapter text
(it fails loudly on drift). Its DMG 2014 CR estimate is informational. **5e-specific math.** For
d20, keep the "data vs printed text" cross-check pattern and swap the math for
`facets_d20` Threat pricing and fixed damage (`software/tools/d20_sim.py` covers balance).

**`pregen_check.py`**: SRD 5.2.1 legality for the five 4th-level pregens (array, background
ASIs, HP, AC, Initiative, Passive Perception, prepared and cantrip counts, O16 focus strings).
**5e-specific.** For d20, rebuild it against `facets_d20/data/facets_d20.yaml` (fixed HP per
`01_What_Is_Different.md` §6, talents, knacks). The same pattern also covers
`F:characters/*.fof`.

**Also:** `flow/build_flow_page.py` (the generated flow page; rebuild after any heading or
section change), and the repo's book invariants in `software/tests/test_docs_consistency.py`
(INV-9…27), which a d20 module could join instead of keeping a separate linter.

---

## 6. Owner rulings 2026-10-05 that apply to the Facets edition too

Recorded in `docs/AUDIT_oraga_5e_official_style.md` §5b and applied to the 5e edition in
Phase 8 (`INVENTIONS_5e.md` #72–#82). The Facets edition (`adventures/`) was **not** edited;
these are the sites to change there. Line numbers are from this doc's earlier sections and
will have drifted; locate by quote.

| Ruling | What changes | Facets-edition sites |
|---|---|---|
| **Q10 — the sergeant carries the case** | The sergeant who holds the gate carries the chained contract case and reads the first two tasks; only the captain has read the sealed third (the Second Clause). | `F:05_The_Longest_Night.md` L327 ("a case chained to the captain's belt"), L333; `F:09_Scene_Cards.md` L174; `F:enemies/bought_captain.fof` L23 (drop the case from the captain); `F:enemies/bought_sergeant.fof` L14/L35 and `F:05` L359, `F:09` L127/L199 already agree (§3.2) |
| **Q11 — the two bodies are literal** | The two cousins Vorlain killed in his year of rule; Essin knows where they are buried. Canon for every edition. | `F:07_Cast_of_the_Ball.md` L268 ("knows exactly where its two bodies are buried") stands as written; read it literally (§3.4) |
| **Q19 — no sign-offs on the agenda cards** | Drop the initials ("— R.C." etc.); the patron line already says who asked. | `F:08` L29–41 |
| **Q20a — the household was sixty** | Change "eighty" to sixty where it counts the household. The 5e text avoids a derived "servants let go" number (O31). Q20b: Sella and Corval are the testament's witnesses, as printed. | `F:04` L491/L503 ("eighty"); `F:07` L155 already says sixty; witnesses: `F:01` L6 ("a Church notary and two witnesses") vs `F:04` L506 / `F:07` L132 (Corval and Sella) |
| **Q24 — "Tell my cousin"** | Veier's quote: the cousin is the Thenyan chief, who sent the delegation. | `F:07_Cast_of_the_Ball.md` L63 ("Tell / my uncle his message took two years…") |

The other 2026-10-05 rulings (Q7, Q8, Q9, Q13, Q15, Q16, Q17, Q23) are recorded for 5e only;
§3.5 still lists their Facets sites if the owner wants them carried.
