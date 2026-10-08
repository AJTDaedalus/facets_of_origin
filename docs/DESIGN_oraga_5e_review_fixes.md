# DESIGN: Oraga Night 5e, fixes from the critical review

*Planner output, 2026-10-08. Input: `docs/REVIEW_oraga_5e_official_critical.md` (6.5/10;
0 P0, 7 P1, 24 P2, 24 P3). Tasks: `docs/TASKS_oraga_5e_review_fixes.md`. Log:
`docs/LOG_oraga_5e_official_audit.md`, new "Review-fix pass" sections. Scope:
`conversions/dnd5e/oraga_night/` only. Everything in `docs/DESIGN_oraga_5e_official.md`
still applies: §2 (locate by quote), §3 (style sheet) and the standard acceptance.*

## 1. Goal

Raise the module from 6.5 to 9 by fixing the classes of defect the first pass's tools couldn't
see:
- cross-chapter continuity;
- rules that contradict each other;
- development scaffolding printed in the book;
- no maps;
- repetition and verbal tics.

**Non-goals:** no new canon without an owner ruling; no change to the night's design; the
Facets edition stays untouched (cross-edition items go into the carryover doc).

## 2. Root cause, and the first fix

Every P1 except S14 and the maps belongs to one class: **facts that must agree across
chapters**. The fix pass had a line linter and two arithmetic checkers, so none of these was
visible to it. The pass therefore starts with tooling (phase R0) that makes these defects
machine-visible. Every later task then has an objective acceptance check, and these defects
can't creep back.

- **`M/facts.yaml`, the continuity bible.** It holds one entry per load-bearing fact:
  - the household size and how many stayed;
  - the honor guards' count and where they stand in each Movement;
  - the faction retinue sizes;
  - the Bought company's size;
  - the Movement in which each NPC and Uninvited arrives;
  - each room's floor, elevation and size (O28);
  - which stair connects which places.

  Each entry lists the **phrases that express it**, plus regexes for the phrasings that would
  contradict it.
- **`T/fact_check.py`.** It scans the unwrapped text for every phrasing of each fact and fails
  on a contradiction (for example "four-fold" next to a household of sixty with 22 staying, or
  "forty blades" against a company of 21). It is written test-first.
- **Linter upgrades (`T/lint_5e.py`):**
  - paragraphs are unwrapped before the regex rules run, which fixes the 8+ blind spots where a
    DC wraps across a line;
  - allowlist entries are scoped to one rule (`file|rule|text|reason`);
  - new rule families:
    - emphasis italics;
    - "(X or Y)" skills;
    - HTML comments;
    - repo file names in body text;
    - simulation jargon ("simulat", "Monte Carlo", "one fight in N", "runs in");
    - wider conversion talk ("Facets edition", "fifth-edition conversion", "old domains",
      "Inventions" in body text);
    - trigger-line format;
    - box-label format;
    - modern anachronisms (a short list: "memo", "businessperson");
  - a **defined-terms** check: every capitalized people or proper term in body text must be
    defined in the glossary or ledger list (`T/terms.txt`). This catches "Scora" and "Kshalo".

## 3. Planner decisions in this pass (to be logged in DECISIONS.md as O32 onward)

- **O32. S14 "Argue its orders" becomes a distraction** (the bestiary's version, P1-3).
  - While the Attendant is Focused, a success breaks its focus and counts toward the four.
  - While it is Idle, a success makes that one character "furniture" to it for the rest of the
    scene: it ignores them, but the Attendant keeps acting.
  - The argument is removed from the Rewards trigger list.
  - S14 hint 5 is rewritten as "show the glance big when one of the three next has no Delay"
    (P2-15).
  - The "more than a party can out-slug" claim is dropped (P2-16).
- **O33. The east wing is upstairs** (P1-5). This is a design fact, of the kind Q13 approved.
  Most passages already say it (B8 is "second floor, dark wing", S10's second-floor window, a
  service stair down from the wing's doors, "booms shut above", "along the gallery").
  - The Court's east doors open onto a stair that rises 12 feet to the gallery level. O28's
    10 × 60 ft cleared corridor runs at gallery level to the wing's double doors.
  - The wing's private stair is **the** garden stair: it runs down the wing's outer wall to the
    upper terrace.
  - Update 05 General Features (add an *Elevations* bullet), 04's B9 and B2 notes, 08's caption,
    and `facts.yaml`.
- **O34. Terrace geometry** (P1-5).
  - S9's box becomes "on the upper terrace, below the rail of the Court's garden walk", which
    keeps the crowd looking down. The duel stays where it is.
  - "Two terraces below" (04:1391, 09:1355) becomes "down at the river gate".
- **O35. Arrival timing** (P1-4). The Attendant has been at the ball since Movement I (most
  passages agree), so 01:63 changes to match. Table V–6's Hollow tells start at Movement III.
- **O36. "Down, Not Out" lives in one place** (05). Every other copy becomes a pointer plus its
  local rule only. S13's "round after next" is corrected to 05's "the round after" (P2-18).
- **O37. The bell-clock default** (the gap the review found in O25). If no character reaches the
  gate by the end of Movement VII, the sect guard arrives and ending 3 runs offstage.
- **O38. Repeated NPC dossiers** (P2-22). Chapter VII is the one home. Chapter IX keeps only the
  threat line plus "see chapter VII". Chapter X's lore tail keeps only what a fighting DM needs.
- **O39. The DM Note form varies.** The *Default / The dial / The cost* triad is kept where it
  earns its place, and the other notes become plain prose (P2-23).
- **O40. Other rules fixes, as the review proposes:**
  - P2-14: the grapple works as the Radiant's saving throw.
  - P2-17: S3's ending 1, where the Blades pull back to search and the gate is open.
  - P2-10: S4's out ends the fight, not the door.
  - P2-11: the "Bought change sides" route becomes a sergeant's runner at the gate in
    Movement V.
  - P2-12: the tracker trigger becomes "Callun's coin refused".
  - P2-19: an "At a 2014 table" glossary box in chapter X.

## 4. Owner rulings needed (gates)

| Q | Review | Question (asked separately, with background) |
|---|---|---|
| QR1 | P1-1 | Household: (a) sixty, with 22 staying ("cut by two-thirds"); (b) sixty cut four-fold, so 15 stay; (c) revert to a hundred, with eighty let go |
| QR2 | P1-2 | The east wing at midnight: does it have its own guard, outside the nine (new canon), or do two of the nine stay at B9, so that "seven go to the dais"? |
| QR3 | P1-7 | Retinue sizes: the cards field four Wardens and four Circle knives, while the ledger says each brought three. Make the retinues four, or cut the cards back to three and give each card a real "Nastier" dial again? |
| QR4 | P2-6 | "Forty blades" against a company of 21 (inherited from the Facets source): change it to "twenty"? |
| QR5 | P1-6 | Maps: (a) I draw original keyed maps (SVG, generated from `facts.yaml` at O28 sizes), (b) commission an artist later and relabel the ASCII figure for now, or (c) no maps |
| QR6 | P2-1 | Simulation numbers on the cards (an earlier fix plan asked for them): replace them with table advice ("expect one character to drop") and move the data to `research/`? |
| QR7 | O30 | Should "Shout" (S6) and "Make enough noise to lose" (S2) also pay no XP, as walk-away outs? |

Gated tasks are marked ⛔ in TASKS. Everything else can run now.

**Owner rulings, 2026-10-08 (all seven answered, so nothing is gated any more):**
- **QR1:** sixty, with twenty-two staying. Drop "four-fold" and say "cut by nearly two-thirds".
- **QR2:** two of the nine guard the east-wing doors, so "seven go to the dais".
- **QR3:** each faction brought four. Fix the text, and give each card a new Nastier dial.
- **QR4:** "twenty blades" and "twenty sworn witnesses". This also goes to the Facets carryover list.
- **QR5:** I draw five original keyed SVG maps (option a). The owner reviews a render before they go in.
- **QR6:** simulation data becomes table advice, and the numbers move to `research/`.
- **QR7:** "Shout" (S6) and "Make enough noise to lose" (S2) are marked "(no XP)".

## 5. Order of work

| Phase | Work | Why here |
|---|---|---|
| R0 | Tooling: `facts.yaml`, the fact checker, linter upgrades, the terms list; a new baseline | Every later task's acceptance check depends on it. Its first run *lists* the remaining defects |
| R1 | Rules and exploits (O32, O36, O37, O40, P1-7 after QR3) | Changes rule meaning before wording passes |
| R2 | Continuity (O33–O35, QR1, QR2, QR4, P2-5/7/8/9, the P3 continuity items) | Geometry has to settle before the maps |
| R3 | Scaffolding and conversion artefacts (P2-1 after QR6, P2-2/3/4/13, P3-24) | Mechanical |
| R4 | Maps (QR5) | Needs R2's geometry settled |
| R5 | Layout and voice: trigger and box formats, dossier dedupe (O38), a tic line-edit (O39), emphasis italics, the remaining P3s | Last, so it polishes final text |
| R6 | Verification: re-extract the official reference PDFs from E: and run the copyright phrasing check; a fresh critical re-review; push | Closeout |

## 6. Risks

- **The fact checker produces false positives** (for example "nine" used in another sense).
  Mitigation: entries match nouns within a window, and every hit is shown with context. A rule-scoped
  allowlist covers the rest.
- **The tic line-edit flattens the voice.** Mitigation: the same pilot-then-calibrate approach
  as Phase 7. The tic targets are reductions (for example "exactly" from 51 to 15 or fewer), not
  zero.
- **Generated maps look amateur.** Mitigation: clean SVG styling (thin walls, labeled keys, a
  scale bar), and the owner can choose option (b) instead.
- **Copyright check.** The reference extracts are gone, so R6 re-extracts them from the PDFs on
  E: before checking phrasing.
