# TASKS: Oraga Night 5e, three-player pass

*Planner output, 2026-10-21. Read first: `docs/DESIGN_oraga_5e_3p_pass.md` (§2–§4 mechanics, §5–§6
rulings), `docs/DECISIONS.md` "Oraga Night 5e — three-player pass" (TP1–TP26, authoritative), and
`docs/LEDGER_oraga_5e_3p.md` (L-001…L-111; each row has its sources and proposed fix). Line numbers
are from `b254fb0` and drift: **locate everything by quote.** Never quote or cite the private canon
folder. Never invent canon: if a task needs a fact the rulings do not give, stop, mark it ⛔ and
ask.*

`M/` = `conversions/dnd5e/oraga_night/` · `T/` = `M/tools/` · `F/` = `adventures/oraga_night/`
(the Facets edition) · `S/` = `research/oraga_5e_sim/` (created by T3.1).

---

## CONFIRM WITH OWNER (before the tasks that name them)

> **All answered 2026-10-22:** C1 confirmed, C1b as printed (TP28); C2 confirmed (TP29); C3 corrected in DESIGN and DECISIONS. E1 → option C, cut the dinner (TP27).

| # | Item | Default the tasks will use if confirmed | Tasks waiting |
|---|---|---|---|
| **C1** | **What seals at midnight (TP13 integrator default).** Only the double doors at the head of the east stair seal when the lights die; the wing's service stair and the garden stair stay open as drawn (Map VIII–5), as the party's routes to intercept the Radiant. **C1b:** this is the first crystal at the lights (05:144–146, "The east wing corridor booms shut… sealed from afar"). The corridors that "lock themselves behind her" (05:501–504; Table V–4 "every door Raunu sealed"; Raunu's last charge, 08:40) are a second sealing. Do they still lock behind Veier as printed? TP16 ("the doors behind Veier do not seal") depends on them existing. Planner default: yes, as printed | Only the double doors seal at the lights; the inner wing doors still lock behind Veier on Raunu's last charge | T4.11, T7.4, T7.21 (and T4.14, T8.3 depend on them) |
| **C2** | **S4 roster cut withdrawn?** DECISIONS withdraws the §4 roster cuts for S3, S8 and S10 by name. TUNING F12's S4 cut (one guard, the second arriving in round 2; L-079) is the same kind of softening, so the ledger treats it as withdrawn too. DECISIONS does not name S4 | S4's roster stands; its label is corrected upward (L-016) | T6.12 |
| **C3** | **TP13's table references.** TP13 says "rewrite Table V–2 tricks 1 and 5, Table V–3 trick 3". In the current text those are *Turn a sconce* and *Guests in her path* (the dais) and *Call a name* (the doors): none puts Veier in reach. The tricks that do are **Table V–4 trick 5** (*The service door*: "Take Veier out…"), **Table V–4 trick 1** (*Hold a sealed door*, the doors "behind Veier") and **Table V–5 trick 3** (*Through the beds*: "Take Veier off the gravel"). Planner reading: the ruling meant V–4 and V–5 (a renumbering slip) | Rewrite V–4 tricks 1 and 5 and V–5 trick 3; leave V–2 and V–3 tricks as they are (except V–3 trick 5, which TP9 retargets in T7.3) | T4.10, T4.11 |

## ESCALATION (owner canon question; blocks T7.6) — RESOLVED: option C, cut the dinner (TP27)

**E1. TP13 ("Veier is never met directly… all night") collides with the owner-ruled *Dinner for
Two* scene.**
- **What exists:** 04 *Dinner for Two (B9)* (INVENTIONS #58, owner ruling Q6; amended by #72, owner
  rulings Q23 and Q7): after the toast the Agenda 4 character is walked up, eats with Raunu and
  Veier, is given "a minute alone", puts the ring "into Veier's hand", and may hear her confirm the
  child. Pointers: 04 B9, Undercurrent C (04:750–770, "Getting through them needs Agenda 4's…"),
  04:1174, 04:1221; 07 Veier (07:92 "reachable only by characters who earn the east wing", 07:100,
  07:107, 07:120 "she makes a moment"); 09 S10 (09:425–430, 09:1478–1479: going with Maiven's
  delegation "turns a wall-climb into an escort"); `flow.json` `sc-dinner`. The Facets edition
  carries it too (F/04:805, F/07:56: "find her eating dinner").
- **Why it blocks:** TP13 says Agenda 4 "is done through the east-wing door". Taken literally, the
  face-to-face dinner, the ring into her hand and the in-person confirmation of the child are all
  retired, along with two earlier owner rulings. The TP13 text does not mention the dinner, so the
  Planner cannot tell whether that was intended.
- **Options (for the owner, none is canon):**
  - **A.** The dinner becomes a conversation **through the east-wing door**. Raunu is seen;
    Veier is heard. The ring is handed to Raunu or a guard for her (this changes Q23's "her hand
    alone"). The child is confirmed through the door.
  - **B.** TP13 governs **midnight only**, and the owner-ruled dinner stands. This contradicts
    "all night".
  - **C.** **Cut the dinner.** Agenda 4 is the message at the door and Veier's voice at midnight;
    the heir is found only through Undercurrent C's other clues.
- **Also check, once ruled:** S10's "escort" with Maiven (does the delegation reach her?), and 07
  Maiven's "for Veier alone".
- **Checked and clear:** DESIGN §3.6 *The Last Rite* and §3.5 do **not** depend on being near
  Veier. The rite is staged where the Radiant is (a lit room, watchers, a rite he must answer), and
  every Stop and End is made within 30 ft of the *Uninvited*, never of Veier. The Wept's Mercy is on
  the dais, the Hollow's Permission at the doors. TP13 changes only who moves her (Vell and the
  household), so §3.5–§3.6 stand as written. In the Crossing rewrite (T4.10) the household is
  referred to only as "the household": no names and no count.

---

## Standard acceptance

**SA (every task that edits `M/`)**, run from `M/`:
1. `python tools/lint_5e.py --check` (0 problems)
2. `python tools/fact_check.py --check` (0 problems)
3. `python tools/bestiary_check.py` (0 mismatches) and `python tools/pregen_check.py` (0 issues)
4. `python -m pytest tools -q` (currently **422 passed**; the count may only rise)
5. If `flow/flow.json` changed: `cd flow && python build_flow_page.py`. If `facts.yaml` `maps`
   changed: `python maps/build_maps.py`.
6. Add a row to `M/INVENTIONS_5e.md` (next is **#89**) for any derived or invented detail, citing
   the TP ruling or Planner note it rests on. Add a Planner note (**TPN-n**) under the three-player
   section of `docs/DECISIONS.md` for any Planner call made in the task.
7. Mark the task ☑ in the status table and the body, and append to `docs/LOG_oraga_5e_3p_pass.md`
   the commands run, the results and any failures.

**SA+F (the task also edits `F/`):** SA, plus, from `software/`:
`python -m pytest tests/test_docs_consistency.py -q` (currently **37 passed**). Facets edits carry
**lore and canon only**. Mechanics (DCs, Delay, the dial, HP, rosters) are 5e-only and never go
into `F/`.

**FACTS:** a task on a ledger row flagged `FACTS` writes or extends the `facts.yaml` guard
**first**, then runs `python tools/fact_check.py --report` to list the worklist, then edits the
text until `--check` is clean. A guard that can never fire (for example, a pattern that matches
nothing in the old text either) does not count.

**SIM:** numbers come from the harness in `S/` (T3.1), 2,000 runs or more per cell, with the seed
logged. Results go to `research/oraga_5e_simulation_notes.md`. The book prints table advice, never
simulation jargon (the lint rule enforces this).

**DIAL:** the text says what changes at Gentle, Sharp and Merciless. Sharp is the printed default.

**Commits:** one per WP, staging specific files. Before any push, run
`software/tests/test_no_private_canon.py` and scan `main..HEAD` for private canon.

**Status key:** ☐ open · ☑ done · ⛔ blocked (OWNER = owner ruling or wording needed; C1–C3 =
confirm item above; E1 = escalation above). *Open (after X)* means the task is open but should run
after X.

---

## Status

| Task | WP | Status | Title |
|---|---|---|---|
| T1.1 | WP1 | done | Tells column in Table VIII–1 |
| T1.2 | WP1 | done | Tell bullets in Movements III–V |
| T1.3 | WP1 | done | Prep box step 4 |
| T1.4 | WP1 | waiting (commit on owner's word) | Commit WP1 |
| T3.1 | WP3 | open | Simulation harness into the repo |
| T3.2 | WP3 | open | `facts.yaml`: three-player baseline guard |
| T3.3 | WP3 | open | Party-size rule, once; Table IX–1 |
| T3.4 | WP3 | open | "Three at the Table" box |
| T3.5 | WP3 | open | Chapter X blocks print three-player numbers |
| T3.6 | WP3 | open | Chapter V numbers, three first |
| T3.7 | WP3 | open | DM sheet numbers; Wept turn and Radiant beat |
| T3.8 | WP3 | open | Card format S1–S7 |
| T3.9 | WP3 | open | Card format S8–S14; read-aloud head counts; S9 |
| T3.10 | WP3 | open | Solo-line simulations |
| T3.11 | WP3 | open | Solo lines in the cards |
| T3.12 | WP3 | open | Movement V time budget |
| T3.13 | WP3 | open | Four-player assumptions in passing |
| T3.14 | WP3 | open | Commit WP3 |
| T2.1 | WP2 | open | "The east-wing doors" fix |
| T2.2 | WP2 | open | Bell glossary; S3 clock wording |
| T2.3 | WP2 | open | Midnight Tracker, first version |
| T2.4 | WP2 | open | Beats that vanish at three |
| T2.5 | WP2 | open | Commit WP2 |
| T2.6 | WP2 | open (after WP4–WP6) | Tracker refresh |
| T4.1 | WP4 | open | `facts.yaml`: Slow / Stop / End guards |
| T4.2 | WP4 | open | Buying Time (Slow) rewrite |
| T4.3 | WP4 | open | Chapter X "what spells buy" |
| T4.4 | WP4 | open | Speed-to-turn rule; Radiant's 20-ft floor |
| T4.5 | WP4 | open (after T5.2) | Stop; Table V–6 |
| T4.6 | WP4 | open | Themes and Stop effects per Uninvited |
| T4.7 | WP4 | open | End: Mercy, Permission, the Root route |
| T4.8 | WP4 | open | The Last Rite |
| T4.9 | WP4 | open | TP15: the Radiant at the Crossing |
| T4.10 | WP4 | open | TP13: Crossing steps, Speed 15 note, Table V–5 |
| T4.11 | WP4 | open | TP13: Table V–4 tricks 1 and 5; the east-wing bullet |
| T4.12 | WP4 | open | TP13: sweep for Veier in reach |
| T4.13 | WP4 | open (after T4.8, T5.2) | Crossing rules paragraph (L-004); Vell into the boat |
| T4.14 | WP4 | open (after T7.21) | Saving Raunu (TP16) |
| T4.15 | WP4 | open | ⟨If History Breaks⟩ at the boat (TP25) |
| T4.16 | WP4 | open | Chapter X Uninvited blocks aligned |
| T4.17 | WP4 | open | Commit WP4 |
| T5.1 | WP5 | open | `facts.yaml`: threat rule guard |
| T5.2 | WP5 | open | The threat rule |
| T5.3 | WP5 | open | Damage to a set-aside creature, per dial |
| T5.4 | WP5 | open | Rule copies become pointers |
| T5.5 | WP5 | open | Attendant: lethal, *Clears the Way* |
| T5.6 | WP5 | open | Distraction at three; edge rules |
| T5.7 | WP5 | open | S14 control note, tie, scene binding, the Root |
| T5.8 | WP5 | open | Update `s14.py` to the new rules |
| T5.9 | WP5 | open | S14 re-simulation |
| T5.10 | WP5 | open | S14 text from the re-sim |
| T5.11 | WP5 | open | Vell's immunities |
| T5.12 | WP5 | open | Commit WP5 |
| T6.1 | WP6 | open | "How Hard to Go" dial box |
| T6.2 | WP6 | open | Rule 2 rewritten; one snake everywhere |
| T6.3 | WP6 | open | Heat-4 rows, part 1 (incl. TP24 Circle beat) |
| T6.4 | WP6 | open | Heat-4 rows, part 2 |
| T6.5 | WP6 | open | A drop costs something before midnight |
| T6.6 | WP6 | open | Lethal after midnight |
| T6.7 | WP6 | open | Two cards live by default |
| T6.8 | WP6 | open | Resources: chapel rest, Hit Die, potions |
| T6.9 | WP6 | open | Update `skirm.py` / `chain.py` |
| T6.10 | WP6 | open | Before-midnight re-budget sims |
| T6.11 | WP6 | open | Before-midnight card text, labels, CR |
| T6.12 | WP6 | open | S4 roster and label |
| T6.13 | WP6 | open | After-midnight re-budget sims; chain run |
| T6.14 | WP6 | open | After-midnight card text and labels |
| T6.15 | WP6 | open | S11 door XP, balustrade, non-lethal, *Sleep* |
| T6.16 | WP6 | open | Commit WP6 |
| T7.1 | WP7 | open | Propagate TP11 |
| T7.2 | WP7 | open | The Root (TP8, TP17, TP18) |
| T7.3 | WP7 | open | The garden doors (TP9) |
| T7.4 | WP7 | open | `facts.yaml`: midnight wing routes |
| T7.5 | WP7 | open | Agenda 4's midnight note (TP13) |
| T7.6 | WP7 | open (option C) | Dinner for Two, Undercurrent C, 07 Veier, S10 escort |
| T7.7 | WP7 | open | Acting early: refusals and two payoffs (TP14) |
| T7.8 | WP7 | ⛔ OWNER | Acting early: which door Corval opens |
| T7.9 | WP7 | open | Vell's sword (TP19) |
| T7.10 | WP7 | open | "Both rivers, one spring" note (TP20) |
| T7.11 | WP7 | open | Second Clause cut (TP21); the contract void |
| T7.12 | WP7 | open | Draft midwife and minister positions (TP23) |
| T7.13 | WP7 | ⛔ OWNER | Apply approved positions (TP23) |
| T7.14 | WP7 | ⛔ OWNER | Aftermath: the Circle knows (TP24) |
| T7.15 | WP7 | open | Vell's midnight route |
| T7.16 | WP7 | open | Agenda 6's reveal |
| T7.17 | WP7 | open (after WP4) | Endings box; the dream line |
| T7.18 | WP7 | open | Agenda 3 completion; Agenda 2 mechanism |
| T7.19 | WP7 | open | Patron's Errand; Corval's doubling; "publicly" |
| T7.20 | WP7 | open | Slingers at midnight |
| T7.21 | WP7 | open | The Radiant's chase line (L-091) |
| T7.22 | WP7 | open | Commit WP7 |
| T8.1 | WP8 | open | `facts.yaml`: gallery geometry and residue values |
| T8.2 | WP8 | open | Redraw VIII–3; sightlines |
| T8.3 | WP8 | open (after T7.4) | Map residue; ward-points; the sealed doors |
| T8.4 | WP8 | ⛔ OWNER | Garden-stair top door; S10 terrain |
| T8.5 | WP8 | open | S4 on a gate draw |
| T8.6 | WP8 | open | Commit WP8 |
| T10.1 | WP10 | open | NPC saves; casting as steel |
| T10.2 | WP10 | open | Success at a cost: scope |
| T10.3 | WP10 | open | Dassa's armour; even charges |
| T10.4 | WP10 | open | Free-hand grapples |
| T10.5 | WP10 | open | Serane's SRD wording |
| T10.6 | WP10 | open | Charge text, moving charges, alignment, Gift Knack |
| T10.7 | WP10 | open | Commit WP10 |
| T9.1 | WP9 | open | Prep box re-costed; 60-minute path |
| T9.2 | WP9 | open | Three-player runtime; cut list; S14 cap |
| T9.3 | WP9 | open | "The maps"; vague cross-refs; V–5 row 2; notation |
| T9.4 | WP9 | open | Open R2 polish |
| T9.5 | WP9 | open | Cast cues in chapter VII |
| T9.6 | WP9 | open | Print build: tests and skeleton |
| T9.7 | WP9 | open | DM packet |
| T9.8 | WP9 | open | Player packet |
| T9.9 | WP9 | open | Card deck |
| T9.10 | WP9 | open | Pregen sheets |
| T9.11 | WP9 | open | The flow page |
| T9.12 | WP9 | open | Two player handouts |
| T9.13 | WP9 | open | Commit WP9 |
| T11.1 | WP11 | open | "Words of the Night" glossary |
| T11.2 | WP11 | open | Overloaded terms |
| T11.3 | WP11 | open | Meta and kickers |
| T11.4 | WP11 | open | De-colon: chapters I–IV |
| T11.5 | WP11 | open | De-colon: chapter V |
| T11.6 | WP11 | open | De-colon: chapters VI–XI |
| T11.7 | WP11 | open | Rhythm tics |
| T11.8 | WP11 | open | B5 and B8 read-aloud |
| T11.9 | WP11 | open | Read-aloud slips; blank cheque; Captain; DC names |
| T11.10 | WP11 | open | Draft mid-tier speech habits (TP22) |
| T11.11 | WP11 | ⛔ OWNER | Apply approved habits (TP22) |
| T11.12 | WP11 | open | Final checks and commit |

**Counts:** WP1 4 · WP2 6 · WP3 14 · WP4 17 · WP5 12 · WP6 16 · WP7 22 · WP8 6 · WP9 13 · WP10 7 ·
WP11 12 = **129 tasks**. **⛔ 5:** OWNER 5 (T7.8, T7.13, T7.14, T8.4, T11.11); the 4 confirm items and E1 were answered 2026-10-22
(confirm: T4.11, T6.12, T7.4, T7.21; escalation: T7.6).

**Run order** (the ledger's §7): WP1 → WP3 → WP2 (T2.1–T2.5) → WP4 + WP5 (T5.1–T5.2 before T4.5) →
WP6 → WP7 → WP8 → WP10 → WP9 → T2.6 → WP11.

**Ledger rows needing no task:** L-018, L-019, L-044, L-079 (WITHDRAWN; L-079 subject to C2) ·
L-023 (DONE, TP11) · L-041, L-093 (DISPUTED; L-041 re-checked in T5.9) · L-042 (SUPERSEDED;
confirmed in T5.9) · L-109 (TP26: Handout 1 stays, no note) · L-006 (answered by TP16, done in
T4.14).

---

## WP1: Tells on the run path (`FRI`)

### ☑ T1.1 Tells column in Table VIII–1 *(L-001, L-096)*
- **Do:** add a "Fracture tells to show" column to Table VIII–1 (08:83–86, the by-Movement block),
  filled only from Table V–6 (05:765–771) and the existing tell lines. Note that the Movement V
  glint repeats the Attendant's crystal-and-light habit (04:896–897).
- **Files:** `M/08_Handouts.md`; read-only `M/05_The_Longest_Night.md` Table V–6, `M/04_The_Ball.md`.
- **Accept:** every tell in Table V–6 appears in the column under a Movement where 04 stages it.
  No new tell is invented. The term is "Fracture tell" (L-069), or the name WP4 settles on.
- **Checks:** SA. **Time:** 20 min.

### ☑ T1.2 Tell bullets in Movements III–V *(L-001)*
- **Do:** add one bullet per Movement (III, IV, V) in chapter IV naming the tells to show that
  Movement and pointing to Table V–6.
- **Files:** `M/04_The_Ball.md` (the Movement III–V time boxes).
- **Accept:** a search of 04 finds each Table V–6 tell at least once (it found 0 before). The
  bullets match T1.1's column.
- **Checks:** SA. **Time:** 20 min.

### ☑ T1.3 Prep box step 4 *(L-001)*
- **Do:** put "The Fractures: Slow / Stop / End, chapter V" in prep step 4 (01:3–36), pointing to
  Table VIII–1's tells column. The full prep re-cost is T9.1.
- **Files:** `M/01_Overture.md`.
- **Accept:** step 4 names the Fractures and the tells column.
- **Checks:** SA. **Time:** 10 min.

### ☐ T1.4 Commit WP1
- `Oraga 5e 3p pass: WP1 tells on the run path`.

---

## WP3: Three-player baseline (TP10) (`FRI`)

### ☐ T3.1 Simulation harness into the repo *(prerequisite for every `SIM` row)*
- **Do:** the TUNING_3P harness (`s14.py`, `skirm.py`, `chain.py`) lives only in a session
  scratchpad (`/tmp/claude-0/-root-facets-of-origin/407a720b-0f36-453e-bd9b-cec22a9c9c7f/scratchpad/`),
  which is not durable. Copy the three scripts (scripts only: no `refs*`, `srd` or `scripts/`
  folders) to `S/`. If they are gone, rebuild them from TUNING_3P §2. Write `S/test_smoke.py`
  first: each script runs at N=200 with a fixed seed, plus one regression assertion per script.
- **Files:** `S/s14.py`, `S/skirm.py`, `S/chain.py`, `S/test_smoke.py`.
- **Accept:** `python -m pytest research/oraga_5e_sim -q` passes. At 4,000 runs on the old rules,
  `s14.py` reproduces TUNING_3P's C1 S14 engaged-distraction win (90–96%) within ±3 points.
- **Checks:** the smoke tests; SA unchanged (no `M/` edit). **Time:** 30 min.

### ☐ T3.2 `facts.yaml`: three-player baseline guard *(L-022, `FACTS`)*
- **Do:** add fact `party_baseline`. The Delay lump is 20 at three (30 at four). The Attendant
  prints 180 HP. The Wept reaches Raunu on her 4th turn at three. The Radiant reaches the stair at
  the fall + 3 beats. Add count/forbid checks that flag a four-player value printed as the default
  (for example "30 damage" without "at four", or "229" without the four-player context). Run
  `--report` and paste the hits into the LOG as the T3.5–T3.7 worklist.
- **Files:** `M/facts.yaml`; a fixture test in `T/test_fact_check.py` if a new check shape is needed.
- **Accept:** the guard fires on the current text, and its hits are logged.
- **Checks:** `pytest tools`; fact_check is expected to fail until T3.7 is done (do not
  re-baseline). **Time:** 25 min.

### ☐ T3.3 Party-size rule, once; Table IX–1 *(L-084)*
- **Do:** write the party-size rule once, three-player first, with four and five at 5th as the
  adjustment lines. Put it in chapter IX (09:96–97) and make 05:289 a pointer. Reorder Table IX–1
  so three comes first.
- **Files:** `M/09_The_Snakes.md`, `M/05_The_Longest_Night.md`.
- **Accept:** one full statement; the other site is a pointer that names the table.
- **Checks:** SA. **Time:** 20 min.

### ☐ T3.4 "Three at the Table" box *(L-020)*
- **Do:** add the box to chapter I (near 01:219–221). Deal Dassa, Ilesse and Serane, with Agendas
  4 / 8 / 2 dealt openly. For more steel, swap Serane for Pello. Never drop Ilesse unless someone
  else heals. Agenda 4 is always dealt. Repoint 03:196–199, 11:22–31 and README:8–10 to the box.
  Describe Agenda 4 as "the route to the east-wing door", never "to Veier" (TP13).
- **Files:** `M/01_Overture.md`, `M/03_Masks_and_Agendas.md`, `M/11_Pregenerated_Characters.md`,
  `M/README.md`.
- **Accept:** one box with three pointers. No text promises that a character reaches Veier.
- **Checks:** SA, plus `pregen_check`. **Time:** 25 min.

### ☐ T3.5 Chapter X blocks print three-player numbers *(L-022)*
- **Do:** the Attendant prints 180 HP (10:200), with 229 on the four-player line. Make the Delay
  lump in 10:145 three-first. Change any other block that carries a party-size number.
- **Files:** `M/10_Bestiary.md`.
- **Accept:** `bestiary_check` passes. If 180 HP needs a different Hit Dice expression, fix the
  dice so the average matches. T3.2's guard is clean for 10.
- **Checks:** SA. **Time:** 20 min.

### ☐ T3.6 Chapter V numbers, three first *(L-022)*
- **Do:** Table V–1, 05:260, 272, 285–297, 681, 706: three-player values printed first, with four
  and five as adjustment lines.
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** T3.2's guard is clean for 05.
- **Checks:** SA. **Time:** 25 min.

### ☐ T3.7 DM sheet numbers; Wept turn and Radiant beat *(L-022)*
- **Do:** 08:36–37 and 08:64–70 get the three-player numbers. Add "the Wept: 4th turn" and "the
  Radiant: stair at the fall + 3 beats" to Table VIII–2. Fix 09:1920 if it prints a four-player
  value.
- **Files:** `M/08_Handouts.md`, `M/09_The_Snakes.md`.
- **Accept:** `fact_check --check` is clean (T3.2's guard is satisfied everywhere).
- **Checks:** SA. **Time:** 20 min.

### ☐ T3.8 Card format S1–S7 *(L-022, L-077)*
- **Do:** in cards S1–S7, the three-character line becomes the printed roster and the four-player
  roster moves to the adjustment line. Read-aloud boxes print three-player head counts (S2's "four
  people" becomes three). Rosters and budgets are re-tuned later in WP6; this task only swaps the
  format.
- **Files:** `M/09_The_Snakes.md`.
- **Accept:** every card S1–S7 leads with three. Box head counts match the printed roster.
- **Checks:** SA. **Time:** 30 min.

### ☐ T3.9 Card format S8–S14; read-aloud head counts; S9 *(L-022, L-077)*
- **Do:** as T3.8 for S8–S14, including S11's "three big men" and S13's "three men". For S9, write
  the one-side rosters and fix the Nastier line that still uses the dropped veteran (09:1403–1406).
- **Files:** `M/09_The_Snakes.md`.
- **Accept:** as T3.8. S9 states who fights when only one side engages.
- **Checks:** SA. **Time:** 30 min.

### ☐ T3.10 Solo-line simulations *(L-021, `SIM`)*
- **Do:** with `S/skirm.py`, build a solo line for each card that a lone PC can walk into (S2, S4,
  S7, S8, S9, S10, S13 at least), aiming at *dangerous but fair*: about High for one character, a
  drop chance that is real but not certain. Two PCs use the three-character line. Log a table:
  card, solo roster, drop % for each of the five pregens.
- **Files:** `S/`, `research/oraga_5e_simulation_notes.md`.
- **Accept:** each solo roster's drop rate is logged for every pregen. None is a token fight
  (drop rate under 15%) or a near-certain loss (over 70%).
- **Checks:** `pytest research/oraga_5e_sim`. **Time:** 30 min.

### ☐ T3.11 Solo lines in the cards *(L-021)*
- **Do:** print T3.10's solo line on each card. Rewrite "one card per group" (09:505–512;
  04:1324–1327; 08:22; 04:446) to size each card to who walks in. S14's solo rule ("with one PC,
  the Focused second turn makes no attack") goes in after T5.5.
- **Files:** `M/09_The_Snakes.md`, `M/04_The_Ball.md`, `M/08_Handouts.md`.
- **Accept:** every card in T3.10 has a solo line, and the group rule names it.
- **Checks:** SA. **Time:** 25 min.

### ☐ T3.12 Movement V time budget *(L-047, `DIAL`)*
- **Do:** at 09:505–512 and 04:1324–1328 add "Past 2:40, at most one card on screen; the others
  resolve offstage *with their consequence* (clock filled, heat moved)". Add a dial clause: the
  same at every setting, because it cuts table time, not risk.
- **Files:** `M/09_The_Snakes.md`, `M/04_The_Ball.md`.
- **Accept:** both sites carry the sentence, and the consequence is named.
- **Checks:** SA. **Time:** 10 min.

### ☐ T3.13 Four-player assumptions in passing *(L-083)*
- **Do:** 04:1038 "two [summoned] should be PCs" is restated for three. 01:322's XP total is
  recomputed for three, with four on the adjustment line.
- **Files:** `M/04_The_Ball.md`, `M/01_Overture.md`.
- **Accept:** both restated. The XP figure is derived and the arithmetic is shown in the LOG.
- **Checks:** SA. **Time:** 15 min.

### ☐ T3.14 Commit WP3
- `Oraga 5e 3p pass: WP3 three-player baseline (TP10)`.

---

## WP2: Midnight Tracker and DM-sheet numbers (`FRI`)

### ☐ T2.1 "The east-wing doors" fix *(L-086)*
- **Do:** Table VIII–6 "Wept: east doors" (08:243) → "Wept: the east-wing doors".
- **Files:** `M/08_Handouts.md`. **Accept:** the row matches 05:769. **Checks:** SA. **Time:** 5 min.

### ☐ T2.2 Bell glossary; S3 clock wording *(L-057)*
- **Do:** add a one-line bell glossary to the DM sheet (which bell is which, and the last bell as
  the leash's hard limit). Reword the S3 clock as "the sect guard's arrival", with the last bell as
  its signal (09:783–791). At 04:90–91, print the Bought's schedule (from 05:1180) or cut the
  pointer.
- **Files:** `M/08_Handouts.md`, `M/09_The_Snakes.md`, `M/04_The_Ball.md`.
- **Accept:** no pointer leads to a schedule the DM sheet lacks. The bell terms are consistent
  across 02:131–133, 05:62–95 and 10:131–132.
- **Checks:** SA. **Time:** 20 min.

### ☐ T2.3 Midnight Tracker, first version *(L-029)*
- **Do:** add a one-page Midnight Tracker to chapter VIII (a numbered table or box per the lint's
  INV rules). It holds three Delay tracks with arrival lines (three-player first, from WP3); the
  Attendant's state, breaks and HP 180; a Fracture-tells-seen grid; ward-point boxes (four dais,
  two doors); the S3 clocks; a dial-word box. Leave labelled rows for threat marks, Stop used per
  scene per Uninvited, and End attempts, to be filled in T2.6.
- **Files:** `M/08_Handouts.md`.
- **Accept:** every live state named in L-029 has a box. It fits one printed page (count the
  rows; at most about 45 lines).
- **Checks:** SA. **Time:** 30 min.

### ☐ T2.4 Beats that vanish at three *(L-046)*
- **Do:** add a one-line note to the DM sheet listing the agenda-dependent beats: Anha empties the
  galleries (Agenda 8), the S11 out, DC 13 ward-steering (Agenda 5), the S8 out (Agenda 2), the
  Agenda 6 reveal. Give each of the three agenda-only snake cooling exits a fallback using its
  existing −1 boxes. Point at the non-Pello routes to the Root (S8's wardens, the keys, DC 18
  Arcana).
- **Files:** `M/08_Handouts.md`, `M/09_The_Snakes.md`.
- **Accept:** every cooling exit has a non-agenda route. No new mechanic is invented: each
  fallback uses a −1 box already printed.
- **Checks:** SA. **Time:** 25 min.

### ☐ T2.5 Commit WP2 (T2.1–T2.4)
- `Oraga 5e 3p pass: WP2 Midnight Tracker and DM-sheet numbers`.

### ☐ T2.6 Tracker refresh *(L-029; open after WP4–WP6)*
- **Do:** fill the tracker's threat-mark, Stop-used and End-attempt rows from WP4/WP5's final
  terms. Add the two live cards (T6.7) and the Last Rite's "rite kept this round" box. Check every
  number against T3.2's guard.
- **Files:** `M/08_Handouts.md`.
- **Accept:** every term on the tracker exists in chapter V or X. fact_check is clean.
- **Checks:** SA. **Time:** 20 min.

---

## WP4: Slow / Stop / End (DESIGN §3.2–§3.7; TP7, TP13, TP15, TP16, TP25)

### ☐ T4.1 `facts.yaml`: Slow / Stop / End guards *(L-002, L-003, `FACTS`)*
- **Do:** replace or extend fact `fracture_rule`:
  - forbid "nothing bought", "Each Fracture works once", "DC 18 with one tell" and
    "if it lands, that is the success";
  - `require` the spells-roll sentence verbatim in both 05 and 10;
  - `require` the cap: "at most three turns per scene";
  - `rule_copy` with home 05.
  Run `--report` and log the worklist.
- **Files:** `M/facts.yaml`. **Accept:** the guard fires on today's text, and the hits are logged.
- **Checks:** `pytest tools`. **Time:** 20 min.

### ☐ T4.2 Buying Time (Slow) rewrite *(L-002, L-003 cap, L-042 confirm)*
- **Do:** rewrite "Earn it by being clever" (05:242–262, 250) to DESIGN §3.2:
  - any creative action that lands earns 1 Delay; DC 13, then DC 15 the second time, never a
    third;
  - spells roll (the attack or save; *Centuries of Practice* refuses 3/day; otherwise a trick
    check with the spellcasting ability, DC 13);
  - a spell counts once per Uninvited;
  - theme pays 2;
  - the lump is 20 at three (30 at four);
  - the cap is three turns per scene, and further Delay gets named people out (Table V–1's "each
    point" column).
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** T4.1's guard is clean for 05. Nothing implies Delay changes history (End's job).
- **Checks:** SA. **Time:** 30 min.

### ☐ T4.3 Chapter X "what spells buy" *(L-007, L-002)*
- **Do:** replace the spell table (10:143–166) with a short list under one rule: lands → 1 Delay;
  on theme → 2. Condition immunities stay, and the effect ends at once. Add Prone and "laughter,
  or anything that would leave them helpless" to *Held by Something Else* (10:1127, 1399, 1924,
  1145). Rewrite 10:128 to "every door a clever table tries opens a little". Print the spells-roll
  sentence word for word as in 05.
- **Files:** `M/10_Bestiary.md`.
- **Accept:** no "nothing bought" row remains. The *Hideous Laughter* Prone contradiction is gone.
  T4.1's guard is clean.
- **Checks:** SA. **Time:** 30 min.

### ☐ T4.4 Speed-to-turn rule; the Radiant's 20-ft floor *(L-039)*
- **Do:** add to Buying Time: "an Uninvited whose Speed is halved, or cut to 20 ft or less, for a
  whole turn makes half a turn's progress; two such turns are 1 Delay (within the cap)". Make
  "nothing slows him below 20 ft" a global clause on the Radiant (10:1444–1449; 10:158).
- **Files:** `M/05_The_Longest_Night.md`, `M/10_Bestiary.md`.
- **Accept:** *Witnessed*, *Slow*, *Ray of Frost* and the Radiant's Stop all resolve through the
  one sentence.
- **Checks:** SA. **Time:** 15 min.

### ☐ T4.5 Stop; Table V–6 *(L-008, L-075; open after T5.2)*
- **Do:** rewrite "The Fractures" (05:742–761) as Stop, DESIGN §3.3:
  - routes: (a) words, DC 15 with any fitting skill, +2 per tell (+4 at most); (b) three thematic
    successes in a scene; (c) a printed room freeze;
  - every Stop earns 2 Delay, marks the speaker (a pointer to T5.2's threat rule), and is usable
    once per scene per Uninvited;
  - fail by 4 or less lands at a cost; fail by 5 or more misses and the scene worsens;
  - a voice carried by a spell (*Message*) does not count; the speaker must be within 30 ft;
  - the Intimidation and Deception bans are lifted except the Hollow and Intimidation.
  In Table V–6, the DC rows become +2 per tell, and "each Fracture works once" becomes "End once;
  Stop once per scene".
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** T4.1's guard is clean. The cross-reference to the threat rule resolves (lint).
- **Checks:** SA. **Time:** 30 min.

### ☐ T4.6 Themes and Stop effects per Uninvited *(L-009)*
- **Do:** write the per-Uninvited block from DESIGN §3.5's table:
  - themes drawn only from each printed "Truth" (05:773–818);
  - Stop effects: the Wept freezes one full round; the Radiant falters for the scene (Speed 20,
    *Shadow-Step* once a minute); the Hollow steps off the doors for one round.
  "Cannot be turned" (10:1421) stays.
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** each theme list cites a printed trait. No new fact about any Uninvited.
- **Checks:** SA. **Time:** 25 min.

### ☐ T4.7 End: Mercy, Permission, the Root route *(L-009)*
- **Do:** write End, DESIGN §3.4. It needs 2+ witnessed tells plus the method.
  - **On success:** out of the attack or errand forfeit, Heroic Inspiration, the matching ⟨If
    History Breaks⟩.
  - **On failure:** it counts as a Stop attempt, and can be retried after a new tell.
  - **Methods:** the Wept's Mercy (with a pointer to T4.14 for what follows) and the Hollow's
    Permission (Intimidation never works).
  - **The Root trap:** stays a second route for all three, as a pointer to 05:1124 (rewritten in
    T7.2).
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** every End names its tells requirement, method, success and failure.
- **Checks:** SA. **Time:** 25 min.

### ☐ T4.8 The Last Rite *(TP7; L-009, L-004 part)*
- **Do:** write the Radiant's End from DESIGN §3.6:
  - **Trigger:** two tells, plus a congregation and a liturgy (a lit room, watchers, and
    Charisma (Performance) or Intelligence (Religion)).
  - **Effect:** he stops hunting to officiate.
  - **Duration:** one character's action per round keeps the rite going, with no check.
  - **The ending:** the leash takes him at the altar he made once the boat is out of reach.
  The rite is staged where the Radiant is: a door, corridor, terrace or garden between him and
  the household's route (TP13). Never beside Veier. "Cannot be turned" stays literally true.
  Add a one-line pointer to his block in 10.
- **Files:** `M/05_The_Longest_Night.md`, `M/10_Bestiary.md`.
- **Accept:** the rite works in the east wing, on the terrace and at the gate. No sentence
  places a character within reach of Veier.
- **Checks:** SA. **Time:** 25 min.

### ☐ T4.9 TP15: the Radiant at the Crossing *(L-048)*
- **Do:** add the DM line: "What he means to do when he reaches her, the module does not say. Never
  narrate an attack on Veier herself; his violence goes to whoever is marked under the threat rule
  and stands in his way." Put it in 05 (the Crossing) and as a pointer in 10. In the Facets
  edition, add the same "the module does not say" line to F/05's Crossing (canon framing, no
  mechanics).
- **Files:** `M/05_The_Longest_Night.md`, `M/10_Bestiary.md`, `F/05_The_Longest_Night.md`.
- **Accept:** the line is present in both editions. No text states his intent.
- **Checks:** SA+F. **Time:** 15 min.

### ☐ T4.10 TP13: Crossing steps, Speed 15 note, Table V–5 *(TP13, C3)*
- **Do:**
  - **Opener (05:553–556):** "Any character with her (Agenda 4 above all) is welcome company"
    becomes: the characters hold the terrace and stair behind her, and Vell and the household move
    her.
  - **Step 2 (05:583–590):** Vell's *"Take her. The gate. Don't stop."* is said to the household,
    not the characters. Cut the Speed 15 / carry / Help note. The household moves her at the
    beat's pace, and the characters' job is to keep the Radiant off her line.
  - **Table V–5 trick 3** (*Through the beds*): rewrite so the characters draw or hold the Radiant
    off the gravel, never take Veier.
  - **Table V–5 trick 5** (*Push the boat off*): check it against TP13. A character at the boat's
    stern is not escorting her, so keep it if it reads that way, otherwise re-aim it at the
    mooring line.
  - **The read-aloud (INVENTIONS #66; TP19 says it stands):** keep it word for word unless it
    places a character within reach of her. "The pale man walking with Veier" seen ahead of the
    characters is fine. If a minimal edit is needed, log it on #66.
  - **Facets edition:** apply the canon part to F/05's Crossing (F/05:160–200, "Take her"): Vell
    and the household move her, and the party holds the Radiant off. Mechanics untouched.
- **Files:** `M/05_The_Longest_Night.md`, `F/05_The_Longest_Night.md`, `M/INVENTIONS_5e.md`.
- **Accept:** in both editions' Crossing, no sentence has a character carrying, supporting,
  escorting or touching Veier. Add `facts.yaml` fact `veier_unmet`: forbid "carry her", "support
  her", "Take Veier", "with Veier" and "beside Veier" in 04/05/09 DM text, each with an `unless`
  for the household.
- **Checks:** SA+F. **Time:** 30 min.

### ☐ T4.11 TP13: Table V–4 tricks 1 and 5; the east-wing bullet *(TP13; C1, C3)*
- **Do (once C1 and C3 are confirmed):**
  - **Trick 1** (*Hold a sealed door*): retarget it to the doors that lock behind Veier, per C1b.
    The character holds the seal from the Radiant's side, never at her side.
  - **Trick 5** (*The service door*): the household takes her into the service run; the
    character's trick is to hold or clear that door, or lead the Radiant into the run's dark.
  - **The east-wing bullet (05:501–519):** keep "buying Veier hallway after hallway", which is
    framed as distance. Check its rules note against C1.
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** T4.10's `veier_unmet` guard is clean for Table V–4. Under C1 the open routes are
  the service and garden stairs, and the text uses them.
- **Checks:** SA. **Time:** 25 min.

### ☐ T4.12 TP13: sweep for Veier in reach *(TP13)*
- **Do:** search 04, 05, 07, 08, 09 and 11 for every read-aloud or instruction placing a character
  with Veier from midnight onward: Movement VI–VII bullets, Table VIII–2 notes, S10/S12 midnight
  lines, the 11:438 Agenda 4 summary. Rewrite each to the TP13 model. **Exclude** the Dinner for
  Two and Undercurrent C complex, which is T7.6 (E1). Mirror canon fixes in F/04, F/05, F/07 and
  F/08 where the same claim is made.
- **Files:** as found; list each in the LOG.
- **Accept:** `veier_unmet` is clean module-wide except the T7.6 sites, which get a temporary
  `unless` noting E1.
- **Checks:** SA+F. **Time:** 30 min.

### ☐ T4.13 Crossing rules paragraph; Vell into the boat *(L-004, L-053 folded in from WP7; after T4.8, T5.2)*
- **Do:** rewrite 05:597–611:
  - **No Delay and no Last Rite:** the Radiant's turn at the gate runs under the threat rule and
    can kill a marked creature in his way.
  - **The Last Rite:** holds him at the altar until the boat is out of reach.
  - **Delay carried down:** is spent at the gate as now.
  - **The escape still holds (canon):** it fails only by TP25's routes (T4.15).
  - **Delete** "the margin should be the characters, not luck" unless the rewrite makes it true.
  - **TP9 reward:** a crowd in the gardens makes him *Witnessed* at the Crossing.
  - **TP16:** add a pointer to the beats he gains if Mercy landed.
  - **L-053:** one sentence using Vell's printed *Elsewhere* action: when the Radiant breaks past,
    Vell is already at the oars. Check it against TP12 (north up the tributary).
  Fit VOICE R13 and R16 to the new text.
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** a failure path exists that costs a character, not the escape. DIAL lines say what
  the Radiant does to a marked creature at each setting.
- **Checks:** SA. **Time:** 30 min.

### ☐ T4.14 Saving Raunu (TP16) *(L-005, L-006; open after T7.21)*
- **Do:** rewrite ⟨They save Raunu⟩ (05:1090–1103) as numbered steps:
  1. Mercy lands (T4.7); the Wept leaves the dais.
  2. Raunu spends the twin crystal on himself and lives, "by his own choice".
  3. The doors behind Veier do not seal. The Radiant gains the beats those seals bought (the
     number fixed by T7.21), and the party is all that stands between them.
  Raise dais ward-steering to DC 13 unless the character studied the wards (the FIX-NEW part).
  Replace the "takes them out of the fight… Stable" note (05:495–499) with the threat rule. Facets
  edition: if F/05's ⟨If History Breaks⟩ carries a save-Raunu entry, apply the narrative part
  (twin crystal on himself; the doors behind Veier unsealed). No mechanics.
- **Files:** `M/05_The_Longest_Night.md`, `F/05_The_Longest_Night.md` (if applicable).
- **Accept:** the steps run from the trigger to the Crossing with no gap. "By his own choice"
  stays literally true.
- **Checks:** SA (+F if F/05 is touched). **Time:** 25 min.

### ☐ T4.15 ⟨If History Breaks⟩ at the boat (TP25)
- **Do:** in ⟨The child is taken⟩ (05:1109–1112), cut "holds Veier back from it, drags her to the
  front gate instead, or otherwise stands between her and the water". History breaks only if a
  character stops the boat or bars the river gate, from a distance. Apply the same to F/05's
  equivalent (F/05:411ff).
- **Files:** `M/05_The_Longest_Night.md`, `F/05_The_Longest_Night.md`, `M/facts.yaml`.
- **Accept:** a `forbid` for "holds Veier back" is added to `veier_unmet`. Both editions agree.
- **Checks:** SA+F. **Time:** 15 min.

### ☐ T4.16 Chapter X Uninvited blocks aligned *(L-002, L-007, L-009)*
- **Do:** align the three Uninvited blocks with WP4: *Centuries of Practice* 3/day, Stop effects,
  the Radiant's Speed floor, the Last Rite pointer, *Held by Something Else*. Leave *The Post* /
  *Only the Doors* for T7.3.
- **Files:** `M/10_Bestiary.md`.
- **Accept:** `bestiary_check` passes. No block restates a chapter V rule in full (`rule_copy`).
- **Checks:** SA. **Time:** 25 min.

### ☐ T4.17 Commit WP4
- `Oraga 5e 3p pass: WP4 Slow / Stop / End, the Last Rite, TP13 Crossing`.

---

## WP5: Threat rule and lethal Attendant (DESIGN §3.1, §4; TP17)

### ☐ T5.1 `facts.yaml`: threat rule guard *(L-010, `FACTS`)*
- **Do:** replace fact `down_not_out` with `threat_rule`:
  - forbid "only ever in mortal danger by choice" and "deadly but not lethal";
  - `require` the mark line (*"She looks at you — properly, for the first time."* or the final
    wording);
  - `rule_copy` with home 05.
  Log the worklist.
- **Files:** `M/facts.yaml`. **Accept:** fires on today's text. **Checks:** `pytest tools`.
  **Time:** 20 min.

### ☐ T5.2 The threat rule *(L-010, `DIAL`)*
- **Do:** replace "Down, Not Out" for the Uninvited (05:204–235) with DESIGN §3.1:
  - **the three triggers:** a Stop; Delay earned three times in a scene; the last blow;
  - **the line said aloud;**
  - **unmarked:** set aside, Stable, and the crowd rule applies;
  - **marked:** normal dying rules, and at Sharp they finish only if the creature is still in the
    way;
  - **the quarry is unchanged;**
  - **the mark lasts the scene;**
  - **Gentle and Merciless lines** from §2.1.
  Retire 05:27–28.
- **Files:** `M/05_The_Longest_Night.md`.
- **Accept:** T5.1's guard is clean for 05. Each dial setting is stated.
- **Checks:** SA. **Time:** 30 min.

### ☐ T5.3 Damage to a set-aside creature, per dial *(L-040, `DIAL`)*
- **Do:** at Gentle, a set-aside creature takes no damage until it is up. At Sharp and Merciless
  the rules as written apply: damage is a death-save failure and ends Stable, but the Uninvited
  never *target* a set-aside creature. Cover crossfire, *Put Aside*'s Emanation, trample and area
  spells (05:206–209, 631–647; 10:283; 05:377–379).
- **Files:** `M/05_The_Longest_Night.md`, `M/10_Bestiary.md`.
- **Accept:** one statement with pointers.
- **Checks:** SA. **Time:** 15 min.

### ☐ T5.4 Rule copies become pointers *(L-010)*
- **Do:** 08, 09 and 10 copies of Down, Not Out become pointers to the threat rule plus their
  local rule only. The Uninvited blocks' trait is renamed.
- **Files:** `M/08_Handouts.md`, `M/09_The_Snakes.md`, `M/10_Bestiary.md`.
- **Accept:** T5.1's `rule_copy` is clean everywhere.
- **Checks:** SA. **Time:** 20 min.

### ☐ T5.5 Attendant: lethal, *Clears the Way* *(L-013, L-003, L-037 timing)*
- **Do:** rewrite the Attendant block (10:200–260) per DESIGN §4:
  - **Down, Not Out goes.** Idle, a creature it drops is set aside, Stable. Focused, normal dying
    rules apply. At Sharp, it attacks a downed creature only if that creature interrupted since
    its last turn.
  - ***Clears the Way*** costs one turn's action, at the start of that turn, with no adjacency
    condition. Idle, it clears when nobody struck it since its last turn. Focused, it attacks on
    its first turn and clears on its second. A lost turn means no clearing.
  - **One PC:** add S14's solo line (the Focused second turn makes no attack; for T3.11).
  Change 05:428 to match.
- **Files:** `M/10_Bestiary.md`, `M/05_The_Longest_Night.md`, `M/09_The_Snakes.md`.
- **Accept:** `bestiary_check` passes. "Deadly but not lethal" appears 0 times. Each dial
  setting's Attendant behaviour is stated (§2.1).
- **Checks:** SA. **Time:** 30 min.

### ☐ T5.6 Distraction at three; edge rules *(L-074, DESIGN §4)*
- **Do:**
  - **Distraction:** Help applies; the Focused DC is 18.
  - **Idle tricks:** a trick tried while it is Idle is not spent.
  - **The natural 20 while Idle:** give it an effect from the existing distraction outcomes, or
    cut it.
  - ***Literal Orders***: "since the end of its last turn" becomes "since the start of its
    previous round".
- **Files:** `M/09_The_Snakes.md` (S14), `M/10_Bestiary.md`.
- **Accept:** consistent in 09 and 10.
- **Checks:** SA. **Time:** 20 min.

### ☐ T5.7 S14 control note, tie, scene binding, the Root *(L-037 FIX-NEW, L-038; TP17)*
- **Do:**
  - **The two-line control note:** *Sleep* fails; *Hold Person* can't target it; a turn lost to
    *Command* or *Laughter* is a lost turn, but not a break.
  - **Tie rule:** the Wept acts first.
  - **Scene binding:** "It goes to the first Uninvited the party interrupts and stays in that
    scene; it cannot be in two. With no Uninvited left in the scene it follows the nearest, or
    leaves (*Not Here*): the card ends, no XP."
  - **TP17:** one line that it enters the Root wherever its three go, unaffected.
- **Files:** `M/09_The_Snakes.md`, `M/10_Bestiary.md`.
- **Accept:** each item appears once, with pointers. Add to `facts.yaml` fact `root`: `require`
  the TP17 line in 10.
- **Checks:** SA. **Time:** 20 min.

### ☐ T5.8 Update `s14.py` to the new rules *(`SIM`)*
- **Do:** model the threat rule, lethal Focused drops and dial behaviour, *Clears the Way* as an
  action, Help on distractions, DC 18, the three-turn Delay cap, spells rolling, 180 HP, and the
  T5.6 edge rules. Add smoke tests for each new switch.
- **Files:** `S/s14.py`, `S/test_smoke.py`.
- **Accept:** tests pass. A run with the new switches off reproduces T3.1's baseline.
- **Checks:** `pytest research/oraga_5e_sim`. **Time:** 30 min.

### ☐ T5.9 S14 re-simulation *(L-013, L-003, L-041, L-042, L-043, L-074, `SIM` `DIAL`)*
- **Do:** run C1–C5 at Gentle, Sharp and Merciless, engaged and slugging. Report:
  - win %, PC death %, whole-party-down % and rounds;
  - the hit-hard HP value for three (L-043);
  - whether the extra Wept turn at three still holds (L-042);
  - the L-041 timeout claim;
  - whether Idle-grind XP needs halving (L-003).
  **Targets at Sharp:** engaged win ≥ 85%; a PC death ≤ 10% for an engaged party; slugging mostly
  loses, with death possible. If the targets are missed, tune only the §4 numbers (DC, HP),
  record a TPN note, and re-run. If two tuning rounds can't meet the targets, add an `##
  ESCALATION` block to the LOG for the Planner.
- **Files:** `S/`, `research/oraga_5e_simulation_notes.md`, `docs/LOG_oraga_5e_3p_pass.md`.
- **Accept:** the table of rates is logged at every dial setting, and the targets are met or
  escalated.
- **Time:** 30 min.

### ☐ T5.10 S14 text from the re-sim *(L-043, L-078, `DIAL`)*
- **Do:** print the hit-hard line's three-player HP and say it combines with the party-size line
  (09:1808–1812, 1927). Rewrite "how it plays" (09:1816–1818) from T5.9 as table advice for each
  setting. If T5.9 says so, halve the Idle-grind XP.
- **Files:** `M/09_The_Snakes.md`, `M/10_Bestiary.md`.
- **Accept:** no simulation jargon (lint). The numbers match T5.9.
- **Checks:** SA. **Time:** 20 min.

### ☐ T5.11 Vell's immunities *(L-076)*
- **Do:** add the Paralyzed, Stunned, Incapacitated and Unconscious immunities (10:2084, 2110), or
  "no spell or effect stops him taking his action" in *Beyond Reach*. Pick one and record it as a
  TPN note.
- **Files:** `M/10_Bestiary.md`.
- **Accept:** `bestiary_check` passes. *Hold Person* at the Crossing can't open ⟨The child is
  taken⟩.
- **Checks:** SA. **Time:** 10 min.

### ☐ T5.12 Commit WP5
- `Oraga 5e 3p pass: WP5 threat rule and lethal Attendant`.

---

## WP6: Risk options, re-budget and re-sims (DESIGN §2; TP24 midnight beat)

### ☐ T6.1 "How Hard to Go" dial box *(L-011, `DIAL`)*
- **Do:** add the box to chapter I with the §2.1 table (Gentle / Sharp / Merciless × snakes,
  dying, Uninvited, Attendant) and the session-zero line ("tonight the knives are real"). Add a
  dial-word line to the DM sheet.
- **Files:** `M/01_Overture.md`, `M/08_Handouts.md`.
- **Accept:** the box matches §2.1 cell for cell, and the book says it is written at Sharp.
- **Checks:** SA. **Time:** 25 min.

### ☐ T6.2 Rule 2 rewritten; one snake everywhere *(L-011, L-066)*
- **Do:** chapter IX rule 2 (09:53–58) becomes "Every ambush is foreshadowed. No snake moves on a
  character whose tell the table has not been shown." The snake-per-Movement count becomes "one"
  everywhere (04:908, 940, 975, 1133; 09:71), with the dial in one place.
- **Files:** `M/09_The_Snakes.md`, `M/04_The_Ball.md`.
- **Accept:** the old rule 2 text appears 0 times. Add a `forbid` to `facts.yaml` (fact
  `risk_dial`) for "no snake is the reason a character dies".
- **Checks:** SA. **Time:** 20 min.

### ☐ T6.3 Heat-4 rows, part 1 (incl. TP24) *(L-011; TP24)*
- **Do:** for half the factions (the Circle first), add a *Heat 4: they come for you* row naming
  who, where and which existing card. **The Circle (TP24):** when Callun is sold the nursery, the
  Circle goes to heat 4, and in the dark its knives go for the east wing's service door, into the
  Radiant's path. This uses S7's roster. Remove the nursery → S12 link (09:184–185); S12 keeps its
  other triggers. The beat must not put any character in contact with Veier (TP13).
- **Files:** `M/09_The_Snakes.md`, `M/08_Handouts.md` (Table VIII–5).
- **Accept:** each row reuses an existing card roster. No new NPC. Log an INVENTIONS row for each
  staging choice.
- **Checks:** SA. **Time:** 30 min.

### ☐ T6.4 Heat-4 rows, part 2 *(L-011)*
- **Do:** as T6.3 for the remaining factions (the Draunel row uses S9's duelists on the terrace,
  per §2.2).
- **Files:** `M/09_The_Snakes.md`, `M/08_Handouts.md`.
- **Accept:** every faction line has a heat-4 row. Table VIII–5 matches.
- **Checks:** SA. **Time:** 30 min.

### ☐ T6.5 A drop costs something before midnight *(L-011, `DIAL`)*
- **Do:** add the cost table to "Death before midnight" (09:544): robbed of an agenda item or a
  crystal charge; held, missing the next beat; marked for the inquest; wakes in the gatehouse cell
  (S3's existing cell). It never kills at any setting. Say how it is rolled or chosen per dial.
- **Files:** `M/09_The_Snakes.md`.
- **Accept:** the "Stable at once with 1 HP" free reset is gone. Four entries, each using an
  existing place or mechanic.
- **Checks:** SA. **Time:** 20 min.

### ☐ T6.6 Lethal after midnight *(L-012, `DIAL`)*
- **Do:** rewrite 09:549–552 and 05:232–235: normal dying rules in every snake and Bought fight.
  The crowd rule covers only creatures an Uninvited set aside. At Sharp, a heat-4 snake finishes a
  downed character who crossed its line. S13 (09:1698–1704) becomes "a creature the *fire* drops".
  Add a "say it when the lights die" line.
- **Files:** `M/09_The_Snakes.md`, `M/05_The_Longest_Night.md`.
- **Accept:** no text half-promises a rescue. The dial cells match T6.1.
- **Checks:** SA. **Time:** 20 min.

### ☐ T6.7 Two cards live by default *(L-017, `FACTS`)*
- **Do:** first add `facts.yaml` fact `default_live_cards` (S11 and S12; the Circle starts at heat
  2). Then move the default heats (09:475–481), update Table VIII–2 and `flow/flow.json`, and
  rebuild the flow page.
- **Files:** `M/facts.yaml`, `M/09_The_Snakes.md`, `M/08_Handouts.md`, `M/flow/flow.json`.
- **Accept:** the guard is clean; the flow page is rebuilt.
- **Checks:** SA. **Time:** 20 min.

### ☐ T6.8 Resources: chapel rest, Hit Die, potions *(L-014)*
- **Do:**
  - **The chapel short rest** costs half a Movement and advances every visible snake clock by one
    (01:285–286; 04:286–287).
  - **One Hit Die** each at the toast.
  - **One healing potion per character** in the Table X loot (10:2155–2232), placed in rooms
    already described, where an exploring party finds them.
  Log the placements in INVENTIONS.
- **Files:** `M/01_Overture.md`, `M/04_The_Ball.md`, `M/10_Bestiary.md`, `M/INVENTIONS_5e.md`.
- **Accept:** three potions at the three-player baseline, with the four-player line saying four.
  No new room or NPC.
- **Checks:** SA. **Time:** 25 min.

### ☐ T6.9 Update `skirm.py` / `chain.py` *(`SIM`)*
- **Do:** model the after-midnight lethal rules, morale "half down" after midnight, the heat-4
  finish at Sharp, the potions, the Hit Die and the chapel rest. Add smoke tests.
- **Files:** `S/skirm.py`, `S/chain.py`, `S/test_smoke.py`.
- **Accept:** tests pass.
- **Checks:** `pytest research/oraga_5e_sim`. **Time:** 30 min.

### ☐ T6.10 Before-midnight re-budget sims *(L-015, L-016, `SIM`)*
- **Do:** for S1, S2, S4, S6, S7, S8, S9 and S10 (09:537's "before midnight" list) at three PCs,
  target Low or Moderate (750 / 1,125). **S3, S8 and S10 keep their rosters** (DECISIONS
  withdrawal). Only their labels move up. S4 is run both ways for C2. Build new three-player
  rosters for the rest from existing blocks. Log the rates and the derived XP.
- **Files:** `S/`, `research/oraga_5e_simulation_notes.md`.
- **Accept:** each card has a roster, XP, label and drop rate logged.
- **Time:** 30 min.

### ☐ T6.11 Before-midnight card text, labels, CR *(L-015, L-016)*
- **Do:** print T6.10's rosters, budgets and corrected labels. Settle the CR question: re-derive
  the five blocks whose CR reads a step high (10:312–313; RULES §1) by the SRD method, or state
  that the labels read high. Record it as a TPN note, and extend `bestiary_check` (test first) if
  CR is re-derived.
- **Files:** `M/09_The_Snakes.md`, `M/10_Bestiary.md`, `T/bestiary_check.py` (if needed).
- **Accept:** labels match the re-sim. `bestiary_check` passes.
- **Checks:** SA. **Time:** 30 min.

### ☐ T6.12 S4 roster and label *(L-016, L-079; C2)*
- **Do (after C2):** if confirmed withdrawn, keep S4's roster and correct the label upward from
  T6.10. If the owner allows the cut, print TUNING F12's line.
- **Files:** `M/09_The_Snakes.md`. **Checks:** SA. **Time:** 10 min.

### ☐ T6.13 After-midnight re-budget sims; chain run *(L-015, L-016, L-014, `SIM`)*
- **Do:** S3, S5, S8's dark half, S11, S12 and S13 at three PCs, targeting Moderate or High
  (1,125 / 1,500), with morale at "half down". Then run `chain.py` (S14 → S13 → S3) with the WP6
  resources and report the HP at the gate per dial (TUNING's 5–21% was the old figure).
- **Files:** `S/`, `research/oraga_5e_simulation_notes.md`.
- **Accept:** rates logged per card, and the chain result per dial.
- **Time:** 30 min.

### ☐ T6.14 After-midnight card text and labels *(L-015, L-016)*
- **Do:** print T6.13's rosters, budgets, morale triggers and labels. S14's "nearly twice High"
  becomes the true multiple.
- **Files:** `M/09_The_Snakes.md`. **Accept:** labels match the re-sim. **Checks:** SA.
  **Time:** 30 min.

### ☐ T6.15 S11 door XP, balustrade, non-lethal, *Sleep* *(L-045, L-080, L-081, L-082)*
- **Do:**
  - **S11:** "Holding the door counts once, as one person carried out, for each character who
    held it" (09:1583–1584; Table I–4).
  - **The balustrade:** add "unless it makes a DC 13 Strength (Athletics) check to catch the
    rail" (09:1365–1366).
  - **The non-lethal rule:** "As the SRD's Knocking Out a Creature, for any attack roll; never for
    an area effect" (09:125–128; 10:36–42).
  - ***Sleep***: "anyone left Unconscious on the floor at the end of a round" (05:376–379).
- **Files:** `M/09_The_Snakes.md`, `M/01_Overture.md`, `M/10_Bestiary.md`,
  `M/05_The_Longest_Night.md`.
- **Accept:** all four are applied.
- **Checks:** SA. **Time:** 20 min.

### ☐ T6.16 Commit WP6
- `Oraga 5e 3p pass: WP6 risk dial, lethal after midnight, three-player budgets`.

---

## WP7: Logic fixes (TP8, TP9, TP11, TP13, TP14, TP17–TP21, TP23, TP24)

### ☐ T7.1 Propagate TP11 *(L-024, `CANON` `FACTS`)*
- **Do:** first add `facts.yaml` fact `raunu_plan`: Raunu meant to keep Veier in the sealed east
  wing until the birth. Forbid "send(s) her (away|off) by boat" and similar. Then:
  - add the one-line plan to 07 Raunu and 07 Veier;
  - repoint 04:831 at what chapter V shows (the sealed wing and the crystals);
  - add the plan to the matching `flow.json` node;
  - **Facets edition:** add the same line to F/07 Raunu and Veier (F/02 already has it from
    TP11).
- **Files:** `M/facts.yaml`, `M/07_Cast_of_the_Ball.md`, `M/04_The_Ball.md`, `M/flow/flow.json`,
  `F/07_Cast_of_the_Ball.md`.
- **Accept:** the guard is clean. Both editions' 07 carry the plan.
- **Checks:** SA+F. **Time:** 20 min.

### ☐ T7.2 The Root (TP8, TP17, TP18) *(L-025, L-050, L-051, `CANON` `FACTS`)*
- **Do:** first add `facts.yaml` fact `root`:
  - the Root is Raunu's gift-research workshop;
  - its effect on the Uninvited is a side effect, and they don't know to avoid it;
  - Raunu doesn't know of the effect;
  - the Attendant enters it unaffected.
  Forbid "will not (go|enter|cross)" near "Root". Then rewrite 04:706–711, 05:50–55, 08:90 and
  10:172 so an Uninvited who enters or is lured in is caught (the Root-trap End). Make 05:1124–1136
  consistent. Add the TP18 DM line: "nobody has seen the effect until creatures like these stand in
  it". **Facets edition:** check F/04:259–265 and 483, and F/05:24–25 and 441, for refuge or
  "won't enter" language, or a claim that Raunu knows, and apply the same canon.
- **Files:** `M/facts.yaml`, `M/04_The_Ball.md`, `M/05_The_Longest_Night.md`, `M/08_Handouts.md`,
  `M/10_Bestiary.md`, `F/04_The_Ball.md`, `F/05_The_Longest_Night.md`.
- **Accept:** the guard is clean in both editions. LOGIC P2-12's contradiction is gone.
- **Checks:** SA+F. **Time:** 30 min.

### ☐ T7.3 The garden doors (TP9) *(L-026, `FACTS`)*
- **Do:** first add `facts.yaml` fact `garden_doors`: the Hollow's *Post* holds the main doors and
  the Court's garden doors. Until he turns east or is Stopped or Ended, the crowd leaves only by
  the service doors and the gallery-side door. Then:
  - name both sets of doors in *The Post* and *Only the Doors* (10);
  - have him shadow-step between them;
  - retarget Table V–3 trick 5;
  - fix 05:150, 05:382–384, 05:861, 08:38, 08:189–190, 09:866 and 09:1596–1597;
  - reconcile "the one open door" with "service doors";
  - state the reward: once the garden doors open, the crowd in the gardens makes the Radiant
    *Witnessed* at the Crossing.
  **Facets edition:** if F/ says the garden doors are open at midnight, correct the fiction (not
  the mechanics).
- **Files:** `M/facts.yaml`, `M/10_Bestiary.md`, `M/05_The_Longest_Night.md`, `M/08_Handouts.md`,
  `M/09_The_Snakes.md`; `F/05` if needed.
- **Accept:** the guard is clean. S3's "trapped at a barred gate" and the Crossing's "dark, empty
  terraces" hold.
- **Checks:** SA (+F). **Time:** 30 min.

### ☐ T7.4 `facts.yaml`: midnight wing routes *(L-027; TP13; C1)*
- **Do (after C1):** add fact `midnight_wing_routes`:
  - the first crystal seals only the double doors at the head of the east stair;
  - the service and garden stairs stay open;
  - the inner doors lock behind Veier on Raunu's last charge (C1b).
  Then:
  - fix 05:145–146 to name the double doors;
  - reconcile S4's doubled guard behind the service door (09:1122–1124, 1149–1151): an open
    route can still be guarded;
  - strike Anha's passages as a way *to Veier* (LEDGER R-01 note), keeping them as a route into
    the wing;
  - mirror the seal wording in F/05 if it names doors.
- **Files:** `M/facts.yaml`, `M/05_The_Longest_Night.md`, `M/09_The_Snakes.md`, `F/05` if needed.
- **Accept:** the guard is clean. Every route into the wing at midnight is drawn on Map VIII–5.
- **Checks:** SA (+F). **Time:** 25 min.

### ☐ T7.5 Agenda 4's midnight note (TP13) *(`CANON` `FACTS`)*
- **Do:** 02:355's "a character beside Veier at the Unmasking. Chapter V leans on it." is
  reworded: at midnight she listens for that character's voice through the door. Fix the matching
  claims at 03:199 ("somebody reaching Veier"), 11:438, 01:30, 04:576 and 09:425–430, but only the
  midnight claims. The dinner is T7.6. **Facets edition:** F/03:135 gets the same rewording.
  Extend `veier_unmet` with a `forbid` for "beside Veier".
- **Files:** `M/02_The_World_and_the_Night.md`, `M/03_Masks_and_Agendas.md`,
  `M/11_Pregenerated_Characters.md`, `M/01_Overture.md`, `M/04_The_Ball.md`, `M/09_The_Snakes.md`,
  `F/03_Masks_and_Agendas.md`, `M/facts.yaml`.
- **Accept:** "beside Veier" appears 0 times in both editions. No new fact beyond TP13's words.
- **Checks:** SA+F. **Time:** 25 min.

### ☐ T7.6 Dinner for Two, Undercurrent C, 07 Veier, S10 escort *(TP13; E1)*
- **Do (E1 ruled: option C, cut the dinner, TP27):** cut the scene and its pointers, and make Agenda 4 a door errand (a guard carries word; log how the ring travels as an INVENTIONS row), in:
  - 04 *Dinner for Two (B9)*, 04 B9, Undercurrent C, 04:1174 and 04:1221;
  - 07 Veier (07:92–120) and 07 Maiven;
  - 09 S10 (09:425–430, 1478–1479);
  - `flow.json` `sc-dinner`;
  - INVENTIONS #58 and #72 (mark them amended or superseded);
  - the Facets edition (F/04:805, F/07:56, F/08:131).
  Remove T4.12's temporary `unless`.
- **Accept:** `veier_unmet` is clean with no exception. Both editions agree.
- **Checks:** SA+F. **Time:** 30 min (option A or C); 10 min (option B).

### ☐ T7.7 Acting early: refusals and two payoffs (TP14) *(L-028, `CANON`)*
- **Do:**
  - **Refusals:** Veier and Raunu refuse to move, in character (TP11 plan; her printed want).
  - **Guests moved early:** they are not among the dead.
  - **A warned character:** starts midnight in position.
  Write these at 01:423–425, Table I–1 Movement V, 04:825–838 and 02:383–384. Keep 01's promise
  through the payoffs. Under TP13, Veier's refusal is heard through the door. The Corval payoff is
  T7.8. **Facets edition:** if F/01 or F/04 carry the same promise, add the refusals and payoffs as
  narrative (canon), without mechanics.
- **Files:** `M/01_Overture.md`, `M/04_The_Ball.md`, `M/02_The_World_and_the_Night.md`; F/ as
  found.
- **Accept:** each early act a table will try has a printed answer.
- **Checks:** SA (+F). **Time:** 25 min.

### ⛔ T7.8 Acting early: which door Corval opens *(TP14; OWNER)*
- **Question for the owner:** TP14 says "a convinced Corval opens a door". Which door, and to
  what? For example, the wing's service door for the party, a door the honor guard holds for the
  crowd, or the east-wing double doors before they seal. Under C1 the sealed doors are magical, so
  Corval may not be able to open them.
- **Do (after the ruling):** write the payoff at the T7.7 sites, in both editions if it is
  narrative.
- **Checks:** SA (+F). **Time:** 10 min.

### ☐ T7.9 Vell's sword (TP19) *(L-052, `CANON`)*
- **Do:** 07:520–522 and 566, and 10:2141–2142, change to: he holds the Radiant off without
  drawing it, and the sword stays on his back. Chapter V and the #66 read-aloud stand. **Facets
  edition:** F/05:170 already agrees. Check F/07:299–307 and `F/enemies/` Vell, and fix any
  "wielded bound" text.
- **Files:** `M/07_Cast_of_the_Ball.md`, `M/10_Bestiary.md`; F/ as found; `M/facts.yaml` (fact
  `vell_sword`: forbid "fights … with it (still )?(bound|wrapped)").
- **Accept:** the guard is clean in both editions.
- **Checks:** SA (+F). **Time:** 15 min.

### ☐ T7.10 "Both rivers, one spring" note (TP20) *(L-055)*
- **Do:** add a DM note at 04:692–696 that most tables won't see it. No echo elsewhere. 5e only
  (a DM note, not canon).
- **Files:** `M/04_The_Ball.md`. **Checks:** SA. **Time:** 5 min.

### ☐ T7.11 Second Clause cut (TP21); the contract void *(L-058, `CANON`)*
- **Do:**
  - **Cut "and send word to the river"**, so the clause ends at "hold her": 05:965, 07:749, and
    anywhere else.
  - **The captain-route reword** (05:1020–1022; 07:730–731; 09:852–854): "the clause he was
    really paid for is dead; he won't hold a gate for a fee's leftovers".
  - **Facets edition:** cut the phrase at F/05:334 and F/07:453.
  - **Guard:** add `facts.yaml` fact `second_clause`: forbid "send word to the river".
- **Files:** `M/05_The_Longest_Night.md`, `M/07_Cast_of_the_Ball.md`, `M/09_The_Snakes.md`,
  `F/05_The_Longest_Night.md`, `F/07_Cast_of_the_Ball.md`, `M/facts.yaml`.
- **Accept:** the guard is clean, and the phrase appears 0 times in either edition.
- **Checks:** SA+F. **Time:** 20 min.

### ☐ T7.12 Draft midwife and minister positions (TP23) *(L-087)*
- **Do:** propose a midnight position for the midwife and for "the elder" and "the younger" Tithe
  minister, unnamed, using only rooms on the existing maps and printed movements (06:28–29;
  02:294–296; Agenda 1; S12; Corval's line). Under TP13, the midwife's position must not give the
  party a route to Veier. Write the proposal as a block in the LOG, give each position a rationale
  citing printed text, and ask the owner to approve. Do not edit `M/`.
- **Files:** `docs/LOG_oraga_5e_3p_pass.md`.
- **Accept:** three positions, each with a cited rationale, sent to the owner.
- **Time:** 20 min.

### ⛔ T7.13 Apply approved positions (TP23) *(OWNER)*
- **Do (after approval):** add the positions to Tables VIII–2 and VIII–6 and to `facts.yaml`
  (fact `midnight_positions`). Mirror them in F/08's position table (F/08:131), as canon.
- **Checks:** SA+F. **Time:** 15 min.

### ⛔ T7.14 Aftermath: the Circle knows (TP24) *(L-049; OWNER, wording)*
- **Question for the owner:** TP24 says chapter VI gains a line that the Circle knows, as the
  exception to "the pregnancy never gets out", and that the owner words the consequence. Please
  supply the line.
- **Do (after the wording):** add it to 06:28–32 and F/06:38, word for word in both. Add
  `facts.yaml` fact `pregnancy_secret`, with a `require` that the exception sits beside "never gets
  out". The midnight beat itself is T6.3.
- **Checks:** SA+F. **Time:** 10 min.

### ☐ T7.15 Vell's midnight route *(L-090, `CANON`)*
- **Do:** add one line at 08:42 and 05:171–173: from the river gate he climbs back to the foot of
  the garden stair to meet her. Check it against TP12 (the boat is unchanged) and TP13 (he and the
  household move her).
- **Files:** `M/08_Handouts.md`, `M/05_The_Longest_Night.md`. **Checks:** SA. **Time:** 10 min.

### ☐ T7.16 Agenda 6's reveal *(L-054, `CANON`)*
- **Do:** reword 02:391–394 to "one of the reasons, and the one that let Vell spend his second way
  on something else". Add a gate beat in which Vell looks at that character, drawn only from
  07:556–560's printed "crack in the ice". **Facets edition:** apply the same reword if F/02's
  Agenda 6 carries the same claim.
- **Files:** `M/02_The_World_and_the_Night.md`, `M/05_The_Longest_Night.md`; `F/02` if
  applicable.
- **Checks:** SA (+F). **Time:** 15 min.

### ☐ T7.17 Endings box; the dream line *(L-056; open after WP4)*
- **Do:** add an endings box to 05:1059–1072 setting each printed state variable against one
  replacement sentence: Raunu (incl. TP16's Raunu-lives), Maiven, Corval and the minister,
  Vorlain, slate and drawer, the Bought, the Wept looked back, the Hollow sent home, the Last
  Rite. Change 04:1376's dream line to "the one she danced with".
- **Files:** `M/05_The_Longest_Night.md`, `M/04_The_Ball.md`.
- **Accept:** every replacement sentence uses printed outcomes only.
- **Checks:** SA. **Time:** 25 min.

### ☐ T7.18 Agenda 3 completion; Agenda 2 mechanism *(L-059, L-092)*
- **Do:**
  - **Agenda 3:** any drunk line, carried to Draunel and *framed* as an understanding (Deception
    DC 13 against Draunel), counts (02:325–330; 09:291, 470).
  - **Agenda 2:** any sincere judgment completes it. A shaded one is caught by the Prelate's
    printed Insight (08:329–330; 02:235). No lore.
- **Files:** `M/02_The_World_and_the_Night.md`, `M/09_The_Snakes.md`, `M/08_Handouts.md`.
- **Checks:** SA. **Time:** 15 min.

### ☐ T7.19 Patron's Errand; Corval's doubling; "publicly" *(L-060, L-085, L-088)*
- **Do:**
  - 01:237: "…your patron may be a snake".
  - Table VIII–7: "four if the wing was forced".
  - 04:1037 and 07:21: add "publicly".
- **Files:** `M/01_Overture.md`, `M/08_Handouts.md`, `M/04_The_Ball.md`,
  `M/07_Cast_of_the_Ball.md`.
- **Accept:** the honor-guard fact in `facts.yaml` is extended for the forced-wing four.
- **Checks:** SA. **Time:** 15 min.

### ☐ T7.20 Slingers at midnight *(L-089)*
- **Do:** add to S10's Development: "the cell opens at the lights; her slingers are with her".
  Align S10's box count with its three-player line. Settle the S4 guard count in Movement V
  (08:218–221; 05:877; 04:72–74) against Table VIII–7.
- **Files:** `M/09_The_Snakes.md`, `M/08_Handouts.md`, `M/05_The_Longest_Night.md`,
  `M/04_The_Ball.md`.
- **Checks:** SA. **Time:** 15 min.

### ☐ T7.21 The Radiant's chase line *(L-091; C1)*
- **Do (after C1 and T7.4):** add one sentence to 05:84–86 and 501–506: the inner doors that lock
  behind Veier, plus *Witnessed*, account for the three beats. State how many beats the locking
  doors are worth, because T4.14 (TP16) removes exactly those beats. Record the number as a TPN
  note.
- **Files:** `M/05_The_Longest_Night.md`. **Checks:** SA. **Time:** 15 min.

### ☐ T7.22 Commit WP7
- `Oraga 5e 3p pass: WP7 logic fixes and TP13–TP24 canon (both editions)`.

---

## WP8: N4 geometry and maps

### ☐ T8.1 `facts.yaml`: gallery geometry and residue values *(L-032, L-062, `FACTS`)*
- **Do:** in the `maps` block and facts, settle:
  - two gallery stairs;
  - the S11 and B4 doors at floor level under a mezzanine;
  - the galleries overlooking the dais;
  - one rail-drop value (the majority form, 12 ft or 10 ft);
  - S10's window level.
  Record the Planner choices as TPN notes and log them in INVENTIONS.
- **Files:** `M/facts.yaml`, `M/INVENTIONS_5e.md`.
- **Accept:** `fact_check --report` lists the text worklist.
- **Checks:** `pytest tools` (`test_maps`). **Time:** 25 min.

### ☐ T8.2 Redraw VIII–3; sightlines *(L-032)*
- **Do:** update `maps/build_maps.py` for VIII–3 and fix its caption. Fix 05:177 and 384, 09:1510,
  and 04:1170–1172. Move or cut the slingers' view of the wing corridor (04:1160–1161) and the
  toast sightline (05:925–926).
- **Files:** `M/maps/build_maps.py`, the maps, `M/05`, `M/09`, `M/04`.
- **Accept:** the crowd can reach S11's door on the map. `test_maps` passes. Render the PNG for
  the owner.
- **Checks:** SA. **Time:** 30 min.

### ☐ T8.3 Map residue; ward-points; the sealed doors *(L-062; open after T7.4)*
- **Do:** remove "other positions approximate" from the four maps. Replace VIII–1's schematic boxes
  (N11). Give the walk rail its own symbol. Draw the four dais and two door ward-points. Mark the
  doors that seal at midnight (C1) on VIII–5. Fix the "second floor" vs gallery-level wording
  (09:1431; 04:1016, 231, 1141; 05:306).
- **Files:** `M/maps/build_maps.py`, maps, chapter text as found.
- **Accept:** "approximate" appears 0 times in captions. `test_maps` passes.
- **Checks:** SA. **Time:** 30 min.

### ⛔ T8.4 Garden-stair top door; S10 terrain *(L-061; OWNER)*
- **Question for the owner:** is the door at the top of the east wing's garden stair shut (and
  locked?) at Movement V's half-bell, when Maiven's slingers climb to the lit window? The ledger
  says the owner confirms this physical fact. Note that C1 keeps the garden stair open *at
  midnight*.
- **Do (after the ruling):** record it in `facts.yaml` and add one terrain line to S10
  (09:1430–1463; 05:457–459).
- **Checks:** SA. **Time:** 10 min.

### ☐ T8.5 S4 on a gate draw *(L-099)*
- **Do:** add to S4's *Where and when*: "run in B1 on a gate draw; the corridor terrain doesn't
  apply" (08:18; 09:899–902).
- **Files:** `M/09_The_Snakes.md`. **Checks:** SA. **Time:** 5 min.

### ☐ T8.6 Commit WP8
- `Oraga 5e 3p pass: WP8 gallery geometry and maps`.

---

## WP10: Rules accuracy sweep

### ☐ T10.1 NPC saves; casting as steel *(L-067)*
- **Do:**
  - add one save line (Wis and Cha) per noncombatant (10:2026–2057), derived from their printed
    abilities;
  - add "saving throws are not checks; NPCs roll them" at 01:275–276;
  - casting with Verbal or Somatic components in a guest's view is noticed on DC 13 Perception,
    and noticed means steel (09:119–124).
  **Do not** add a Charmed immunity for Raunu. Log it as an owner question (non-blocking) in the
  LOG.
- **Files:** `M/10_Bestiary.md`, `M/01_Overture.md`, `M/09_The_Snakes.md`.
- **Accept:** `bestiary_check` passes.
- **Checks:** SA. **Time:** 25 min.

### ☐ T10.2 Success at a cost: scope *(L-068)*
- **Do:** it applies to talk and exploration before midnight. It does not apply to Delay tricks,
  Stop, End, ward-steering, Attendant distractions or Very Hard DCs (01:269–273). 01:515 becomes
  "arrives, if you offer it".
- **Files:** `M/01_Overture.md`. **Checks:** SA. **Time:** 10 min.

### ☐ T10.3 Dassa's armour; even charges *(L-102)*
- **Do:** give Dassa chain mail (AC 17, if her Strength meets 13) or scale mail (AC 16, Stealth
  Disadvantage). Pick whichever `pregen_check` validates, and record it as a TPN note. Even the
  common charges to one each (11:293, 342).
- **Files:** `M/11_Pregenerated_Characters.md`. **Accept:** `pregen_check` reports 0 issues.
- **Checks:** SA. **Time:** 15 min.

### ☐ T10.4 Free-hand grapples *(L-103)*
- **Do:** add "it lets go of its weapon to do this", or "it grapples with its shield arm", to the
  Honor Guard's *Seize* (10:456), the Warden's *Seize for Questioning* (10:701) and the Blade's
  *To the Terms* (10:514–517).
- **Files:** `M/10_Bestiary.md`. **Checks:** SA. **Time:** 10 min.

### ☐ T10.5 Serane's SRD wording *(L-104)*
- **Do:** copy SRD 5.2.1 (CC BY 4.0) wording for Bardic Inspiration ("another creature", "see or
  hear") and *Vicious Mockery* ("before the end of its next turn") (11:90–96).
- **Files:** `M/11_Pregenerated_Characters.md`. **Checks:** SA; `tools/copyright_scan.py` stays
  clean. **Time:** 10 min.

### ☐ T10.6 Charge text, moving charges, alignment, Gift Knack *(L-105, L-106, L-107)*
- **Do:**
  - 05:139–142: add "(it still works; see the sidebar)".
  - *A Veil of Quiet* and *Dark-Burst* (10:2189, 2195): "The effect stays where it was released."
  - The "—" alignment on the Uninvited and Vell: change to "Neutral" or "Unaligned".
  - Rule in one sentence whether the Orthaen *Gift Knack* gives Advantage on a crystal
    distraction (03:90–91; 09:1830), and record it as a TPN note.
- **Files:** `M/05_The_Longest_Night.md`, `M/10_Bestiary.md`, `M/03_Masks_and_Agendas.md`,
  `M/09_The_Snakes.md`.
- **Checks:** SA. **Time:** 20 min.

### ☐ T10.7 Commit WP10
- `Oraga 5e 3p pass: WP10 rules accuracy sweep`.

---

## WP9: Prep and runtime honesty; the print build

### ☐ T9.1 Prep box re-costed; 60-minute path *(L-030)*
- **Do:**
  - re-cost each prep step honestly (01:3–36);
  - add a true 60-minute path and a five-block "know these" list;
  - include Slow / Stop / End, the dial and S11 + S12 (the two default live cards);
  - fix the chapter VII skip/skim contradiction (01:28 vs 01:551–553; 01:30).
- **Files:** `M/01_Overture.md`.
- **Accept:** the minutes add up to the stated total.
- **Checks:** SA. **Time:** 25 min.

### ☐ T9.2 Three-player runtime; cut list; S14 cap *(L-031, `DIAL`)*
- **Do:** make the three-player runtime the printed column in Table I–1 (01:180–207; 08:13–30). Add
  S14 and the dark-hour cards to the cut list. Any S14 cap ends with the errand *completing*,
  never with the party let off. Say it applies at every setting.
- **Files:** `M/01_Overture.md`, `M/08_Handouts.md`, `M/09_The_Snakes.md`.
- **Checks:** SA. **Time:** 20 min.

### ☐ T9.3 "The maps"; vague cross-refs; V–5 row 2; notation *(L-094, L-095, L-097, L-098)*
- **Do:**
  - "the palace diagram" becomes "the maps (VIII–1 to VIII–5)" (01:16, 109; 04:50, 407);
  - the 08:3–5 print line matches the print build (T9.6);
  - name the section, table or row for each of the nine vague cross-references (04:1424, 04:1043,
    the six "→ chapter IX" pointers, 05:226);
  - Table V–5 row 2: add "(or the Crossing's first beat did)";
  - one notation for automatic heat ticks in Tables VIII–5 and IX–2.
- **Files:** `M/01`, `M/04`, `M/05`, `M/08`, `M/09`. **Checks:** SA. **Time:** 25 min.

### ☐ T9.4 Open R2 polish *(L-100, `CANON`)*
- **Do:**
  - gloss Svara (01:438) using printed facts only. If the module prints none, mark this sub-item
    ⛔ OWNER in the LOG and skip it;
  - give the skill list one form (07:527; 08:117);
  - cut the "yardstick" commentary (09:1796–1802; 10:313);
  - rule N28 (the Prickle against an unseen attacker's Advantage, 03:110–111) in one sentence and
    record it as a TPN note.
- **Files:** `M/01`, `M/07`, `M/08`, `M/09`, `M/10`, `M/03`. **Checks:** SA. **Time:** 20 min.

### ☐ T9.5 Cast cues in chapter VII *(L-063)*
- **Do:** open each chapter VII entry with a two-line cue (wants; where at midnight), drawn only
  from the printed entry and Table VIII–2. The speech habits are T11.10.
- **Files:** `M/07_Cast_of_the_Ball.md`.
- **Accept:** every cue sentence traces to the entry's own text.
- **Checks:** SA. **Time:** 30 min.

### ☐ T9.6 Print build: tests and skeleton *(L-033)*
- **Do:** write `T/test_build_print.py` first (at least 3 tests per public function). Then write
  `T/build_print.py`: Markdown to standalone HTML with a print stylesheet (PDF via the browser's
  print, or `weasyprint` if installed), outputting to `M/print/` (gitignored, or committed: record
  the choice as a TPN note). It strips repo paths and marks cut lines.
- **Files:** `T/build_print.py`, `T/test_build_print.py`.
- **Accept:** tests pass; `pytest tools` count rises.
- **Checks:** SA. **Time:** 30 min.

### ☐ T9.7 DM packet *(L-033)*
- **Do:** the build emits the DM packet: the DM sheet, the Midnight Tracker and the five maps. The
  DM-sheet tables become print-friendly (the sheet's "two pages" claim made true, or reworded).
- **Files:** `T/build_print.py`, `M/08_Handouts.md`.
- **Accept:** the packet renders, and its page count is logged.
- **Checks:** SA. **Time:** 30 min.

### ☐ T9.8 Player packet *(L-033)*
- **Do:** the build emits the handouts with cut lines and with DM italics stripped (08:289–290,
  317).
- **Files:** `T/build_print.py`. **Accept:** no DM text in the player packet (a test asserts this).
  **Checks:** SA. **Time:** 25 min.

### ☐ T9.9 Card deck *(L-033)*
- **Do:** the build emits one page per card, with that card's stat blocks appended from chapter X.
- **Files:** `T/build_print.py`. **Accept:** every card's blocks are present (a test asserts this).
  **Checks:** SA. **Time:** 30 min.

### ☐ T9.10 Pregen sheets *(L-064)*
- **Do:** in the print build, merge the shared preamble (11:33–43) into each sheet and add HP,
  slot and charge trackers, one line per spell, and an "on your turn" line.
- **Files:** `T/build_print.py`, `M/11_Pregenerated_Characters.md` if a source line is needed.
- **Accept:** `pregen_check` passes, and each sheet prints standalone.
- **Checks:** SA. **Time:** 30 min.

### ☐ T9.11 The flow page *(L-065)*
- **Do:** label the flow page a contributor tool (README:89) and keep it out of the DM's path.
  Strip repo paths and the provenance footer from anything DM-facing.
- **Files:** `M/README.md`, `M/flow/flow_page.template.html`. Rebuild the page.
- **Checks:** SA. **Time:** 15 min.

### ☐ T9.12 Two player handouts *(L-101, `CANON`)*
- **Do:** add a public-room sketch (from the public rooms on the maps only) and a one-page
  "tonight's customs" (no disarming, masks, the Unmasking, the Dead Dance), built from printed text
  only. Add both to the player packet. Log them in INVENTIONS.
- **Files:** `M/08_Handouts.md`, `M/maps/build_maps.py` (sketch), `M/INVENTIONS_5e.md`.
- **Accept:** every custom traces to a printed line, and no private room appears.
- **Checks:** SA. **Time:** 30 min.

### ☐ T9.13 Commit WP9
- `Oraga 5e 3p pass: WP9 prep, runtime and print build`.

---

## WP11: Voice pass, by ear, last

*Light touch: keep the voice (the owner's rule). Use `python tools/lint_5e.py --report` for the tic
metric before and after each task, and log both. Run `python tools/copyright_scan.py` at the end
of each task.*

### ☐ T11.1 "Words of the Night" glossary *(L-036)*
- **Do:** add a box to chapter I with about 15 lines: Delay, the Uninvited, the Wept / Radiant /
  Hollow, the Bought, Slow / Stop / End, Fracture tell, threat (marked), the dial, the Midnight
  Order (if T11.2 adopts it), and others. Gloss Delay and the Wept inline at first use (01:177,
  399–405, 479–493). Add new terms to `T/terms.txt`.
- **Files:** `M/01_Overture.md`, `T/terms.txt`. **Checks:** SA (defined-terms check).
  **Time:** 25 min.

### ☐ T11.2 Overloaded terms *(L-069)*
- **Do:** write "Fracture tell" every time (or the WP4 name). Spell out "threat line" at first use.
  Decide on "Midnight Order" (TPN note). Move the gloss of "the fourth iron" before its first use
  (09:262). Leave 07:415 (disputed, consistent).
- **Files:** `M/01`, `M/05`, `M/09`. **Checks:** SA. **Time:** 25 min.

### ☐ T11.3 Meta and kickers *(L-035)*
- **Do:** apply VOICE R1, R2 and R9–R18. Cut the designer meta ("a load-bearing sentence", "This
  is the crescendo") and keep the instruction. R17 says "horses", not "carter" (TP12). R13 and R16
  must fit T4.13's text. Keep the kickers at 01:428–429 and 01:449–450.
- **Files:** `M/01`, `M/05`, `M/07`. **Checks:** SA. **Time:** 30 min.

### ☐ T11.4 De-colon: chapters I–IV *(L-034)*
- **Do:** turn every second colon in a sentence into a period, and half the rest into a period or
  "so". Thin the semicolons. Judge by ear.
- **Files:** `M/01`–`M/04`. **Accept:** the colon and semicolon rates fall (log the before and
  after). **Checks:** SA. **Time:** 30 min.

### ☐ T11.5 De-colon: chapter V *(L-034)*
- As T11.4 for `M/05`. **Time:** 30 min.

### ☐ T11.6 De-colon: chapters VI–XI *(L-034)*
- As T11.4 for `M/06`–`M/11` (stat blocks excepted). **Time:** 30 min.

### ☐ T11.7 Rhythm tics *(L-108)*
- **Do:** cut "the way X" similes to the two best. Keep "arriving" only in the #66 read-aloud.
  Where a chapter repeats a fact, keep the fact and drop the flourish. Check the short-sentence
  share.
- **Files:** as the tic table lists. **Accept:** the lint tic count falls.
- **Checks:** SA. **Time:** 30 min.

### ☐ T11.8 B5 and B8 read-aloud *(L-070, `CANON`)*
- **Do:** write 35–50-word boxes for B5 (the Crossing's ground) and B8 (the study), using only
  printed details. B5 must not place the characters with Veier (TP13). Do B3, B7 and B10 if time
  allows. Log each in INVENTIONS.
- **Files:** `M/04_The_Ball.md`, `M/INVENTIONS_5e.md`.
- **Accept:** each box element traces to a printed line (list them in the INVENTIONS row).
- **Checks:** SA. **Time:** 25 min.

### ☐ T11.9 Read-aloud slips; blank cheque; Captain; DC names *(L-071, L-072, L-110, L-111)*
- **Do:**
  - VOICE R5–R7 and R20 (04:231–232, 255–256, 1343–1344; 05:1065–1066);
  - 06's "larger at your discretion" gets a default ("one favor; double it if…");
  - R21 for the Captain's line (07:752), with no new facts;
  - align the DC ladder tier names (01:252–262) with the SRD's, or leave them with the
    explanation (TPN note).
- **Files:** `M/04`, `M/05`, `M/06`, `M/07`, `M/01`. **Checks:** SA. **Time:** 25 min.

### ☐ T11.10 Draft mid-tier speech habits (TP22) *(L-073)*
- **Do:** draft **one speech habit each, with no sample quotes**, for Kovaun, Callun, Draunel,
  Essin, Maiven, Anha, Tavva and the two Bought officers (the Sergeant and the Captain). Draw each
  strictly from the NPC's printed traits, Wants and Secret, and cite the line it rests on. Write
  them as a proposal block in the LOG for owner approval. Do not edit `M/`.
- **Files:** `docs/LOG_oraga_5e_3p_pass.md`. **Accept:** nine habits, each cited.
- **Time:** 25 min.

### ⛔ T11.11 Apply approved habits (TP22) *(OWNER)*
- **Do (after approval):** add each habit to its chapter VII entry (07:263, 301, 363, 418–420, 443,
  473, 671, 722, 752) and resolve the shared "forgettable on purpose" note. Habits are voice, not
  canon facts, so 5e only unless the owner says otherwise. Log them in INVENTIONS.
- **Checks:** SA. **Time:** 15 min.

### ☐ T11.12 Final checks and commit
- **Do:**
  - run SA in full, plus SA+F, `python tools/copyright_scan.py`, `pytest research/oraga_5e_sim`
    and `software/tests/test_no_private_canon.py`;
  - confirm every ledger row is ☑, ⛔ (with its question) or in the no-task list;
  - update the LEDGER's §5 counts;
  - commit `Oraga 5e 3p pass: WP11 voice pass; close tasks`;
  - scan `main..HEAD` for private canon before any push.
- **Time:** 20 min.
