# R5.3 tic line-edit: 01, 02, 03, 06, 08, 11, README

*Parallel worker, 2026-10-10. P2-23, P2-24, O39. M/ = `conversions/dnd5e/oraga_night/`, T/ = `M/tools/`.
Budget and method from `docs/LOG_oraga_5e_official_audit.md`, "Review-fix pass — R5.3 pilot (04)".
Not committed, not re-baselined; TASKS/LOG untouched.*

## Metrics (`lint_5e.py --report --file`, DM prose)

| file | words | wps before → after | >30% before → after | —/1k | hard before → after | not…but (soft) |
|---|---|---|---|---|---|---|
| 01_Overture | 4,833 → 4,842 | 14.43 → **15.27** | 5.34 → 5.59 | 1.86 = | 0 → 0 | 9 = |
| 02_The_World_and_the_Night | 4,192 → 4,191 | 14.26 → **15.30** | 6.54 → 7.22 | 1.67 = | 0 → 0 | 5 = |
| 03_Masks_and_Agendas | 1,793 → 1,790 | 14.34 → **15.43** | 5.80 → 6.82 | 0.00 = | 1 → **0** | 1 = |
| 06_Aftermath | 1,089 → 1,092 | 14.52 → **15.38** | 5.00 → 5.26 | 0.92 = | 0 → 0 | 2 = |
| 08_Handouts | 2,480 → 2,483 | 12.59 → 12.80 | 4.80 → 5.31 | 4.03 = | 4 → **0** | 1 = |
| 11_Pregenerated_Characters | 3,205 → 3,209 | 11.29 → 11.42 | 2.14 → 2.15 | 1.56 = | 1 → **0** | 2 = |
| README | 842 → 844 | 17.91 → 17.96 | 5.66 = | 1.19 → 1.18 | 0 → 0 | 0 = |

08 and 11 stay below 14.5 on purpose. Their means are set by the DM-sheet tables and the stat lines, and
the prose in them was rejoined only where a fragment was scaffolding. README was already high, so only
its tic changed.

## Tics, after / LOG budget

| file | exactly | the whole | quietly | out loud | genuinely | say so |
|---|---|---|---|---|---|---|
| 01 | 0 / 0 (was 2) | 1 / 1 (3) | 0 / 0 (1) | 0 / 0 (1) | 1 / 1 (3) | 1 / 1 (3) |
| 02 | 1 / 1 (5) | 0 / 0 | **0 / 1** (3) | 0 / 0 | 0 / 0 | 0 / 0 |
| 03 | 1 / 1 (2) | 1 / 1 (3) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| 06 | 0 / 0 | 0 / 0 (1) | 0 / 0 | 0 / 0 | 0 / 0 (1) | 0 / 0 |
| 08 | 0 / 0 | 1 / 1 (2) | **2 / 1** (2) | 0 / 0 | 0 / 0 | 1 / 1 |
| 11 | 1 / 1 (2) | 0 / 0 | 0 / 0 (1) | 0 / 0 | 0 / 0 | 0 / 0 |
| README | 0 / 0 | 0 / 0 (1) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

**One swap, total held.** Both of 08's "quietly" are Snake Tracker triggers ("knife turned or caught
quietly", "S6 ends quietly"). They copy chapter IX's Table IX–2 wording, which another worker is
editing, so 08 keeps 2 and 02 goes to 0 instead. The set's quietly total is 2, the same as its budget.

**Kept on purpose:** 01 "It is not the whole truth" (a real contrast), "political fencing is genuinely fun",
and "Say so: 'Nobody has drawn yet…'" (a functional cue); 02 "feared exactly one person" (Vorlain); 03
"worth exactly what the fiction says" and "the whole history of House Boranis"; 08 "thread the whole
palace" (map intro, matching 04's keep) and "they say so" (Table VIII–4 cost); 11 "exactly the kind of
lock he is good at".

**Table I–3 trigger.** "The pattern said out loud" became "The pattern named aloud". No other file
quotes the row label.

## Emphasis italics (family now 0 in all seven files)

- 03: "how it *shows itself*" is now roman.
- 08: the rumor table's "*empty*", "*actually*" and "*in*", and Handout 3's "*common*", are now roman.
- 11: "Andra *is* her research" became "Andra and her research are the same thing".
- The linter misses these, and they are fixed too:
  - 01: "*House Boranis hired none.*" is folded into its sentence, as in 04. "*the module does not say*" is now in quotation marks. The two italic lines the DM says to the players ("This is a glittering party…") are now in quotation marks.
  - 06: "*Where it ends*" is now roman.
  - 08: the DM-to-player lines in Table VIII–1 ("what does your mask look like?", "what do you carry out?") and the Attendant's state calls ("It's locked on you" / "It's drifting.") are now in quotation marks.
- Untouched: canon NPC speech in Table VIII–1 (Raunu's toast line, the Radiant's omen), labels, spells and items.

## Staccato and reframes

- 06, as the review cited: "It leads nowhere. / It is the moment…" became "It leads nowhere, and that is the moment the
  investigation stops having a suspect and starts having a hole in it."
- 02's anaphora triple: "He is not here to save Raunu. He is not, strictly, here to save Veier. He is here so that…" became
  "He is not here to save Raunu, nor, strictly, Veier. He is here so that…"
- About 50 other merges across the set, all with a colon, a semicolon or ", and". The same pair from the toast in 04 sets the pattern:
  - "Let the table enjoy the party. Their enjoyment is the ballroom floor…" became "…the party: their enjoyment…".
  - "Never underline an omen. Say it once…" became "…an omen: say it once…".
  - "The palace staff is cut by nearly two-thirds. A lively seat of power goes eerily quiet." became one sentence joined with ", and".
  - "Val'loh has the same magic as anywhere else. What differs is how it looks." became one sentence joined with a semicolon.
- Punches left alone: "Shorter sentences. Fewer adjectives. The party is over.", "The Wept is not going anywhere. The
  guest is.", "Nothing is written down. Nothing ever is.", "Corval is incorruptible by money. He is not
  incorruptible by kindness.", "The gift is not in her. The knowing is.", "Some will be burned."
- No reframe was turned into ", not" (soft `not_but` unchanged everywhere). No em dashes were added.

## DM Notes (O39)

None of these files has a **Default / The dial / The cost** triad. The DM Notes and Troubleshooting boxes
in 01 and 02 already use different forms. Each box got only line edits:
- 01: "chapter IV prints it at B0 for that reason"; "…the conversation, which is what the masquerade is for".
- 02: "…which is what this section says; it changes what they are ready to do…".

## Before → after samples

1. **06, Otta Vesh (P2-23 cite).**
   - **Before:** "…and the material is wrong. It leads nowhere. / It is the moment the investigation stops having a suspect and starts having a hole in it."
   - **After:** "…and the material is wrong. It leads nowhere, and that is the moment the investigation stops having a suspect and starts having a hole in it."
2. **01, the snakes' premise (emphasis italic, staccato).**
   - **Before:** "Every great house hired extra swords this season. *House Boranis hired none.*"
   - **After:** "Every great house hired extra swords this season, and House Boranis hired none."
3. **02, Vell (tics and a split).**
   - **Before:** "Vell will not fight the Uninvited if he can avoid it. He knows exactly what they are, and they may know him. He prepares quietly, all night, and he is very good at it."
   - **After:** "Vell will not fight the Uninvited if he can avoid it: he knows what they are, and they may know him. He spends the night preparing, unseen, and he is very good at it."

## Wording only: script checks

Each file was compared against its pre-edit copy (`scratchpad/r53_rest/verify.py`):
- The multisets of `DC n`, dice and numerals are identical in all seven files.
- All unwrapped read-aloud blocks are identical (08 has 3, the other files none).
- In 08, Player Handout 1 (the invitation), Player Handout 2 (the agenda cards) and the whole of "The Palace, Keyed" (map intro and captions) are byte-identical.

## Commands

| command | result |
|---|---|
| `python T/lint_5e.py --report --file <f>` | each of the seven files: 0 hard, 0 struct |
| `python T/lint_5e.py --check` | OK (0 problems; 11 hard hits remain module-wide, none in these files) |
| `python T/fact_check.py --check` | OK (0 problems) |
| `python T/bestiary_check.py --quiet` | 28 blocks + 1 Nastier, 0 mismatches |
| `python T/pregen_check.py --quiet` | 5 pregens, 0 issues |
| `python -m pytest T -q` | 394 passed, test_maps included |
