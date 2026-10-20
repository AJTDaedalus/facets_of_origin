# TASKS — Oraga Night, Rebuilt

**Design:** `docs/DESIGN_oraga_rewrite.md` · **Brief:** `docs/BRIEF_oraga_rewrite.md`
**Log:** `docs/LOG_oraga_rewrite.md` · **Branch:** `feat/oraga-rewrite`
**Blocked until:** `TASKS_lineage.md` L15, `TASKS_valloh_facet.md` V17, and `TASKS_fun_second_act.md` T18
are all done.

**Standing out-of-scope rule.** The agendas, omens, undercurrents, cast, Fractures and the tell-table,
the read-aloud discipline, the safety text, the ⟨If History Breaks⟩ sidebars, the Crossing, and the
epilogue question are untouched. Any task that finds itself editing their prose beyond adding a pointer
line stops and comes back to Planner. That is not a failure; it is the constraint working.

---

## M1 — Data first

**O1. Module-local Bought reskins.** — 40 min
Files: `adventures/oraga_night/enemies/bought_{blade,sergeant,captain}.fof`.
Copy from `enemies/bought_*.fof`; override `description` and `organization` with Val'loh flavour only.
**Never** override Resolve, attack, armor or Techniques — those are `fun_second_act`'s settled numbers
(T17) and forking them here recreates the divergence the iron law forbids.
Accept: three files; a diff against the Bestiary originals touches flavour fields only; the Bestiary
files are unchanged (B9).

**O2. Five pregens as `.fof`.** — 90 min
Files: `adventures/oraga_night/characters/{serane,pello,andra,dassa,ilesse}.fof`,
`software/tests/test_character_fof.py`.
Built through Lineage and the Val'loh Facet, to DESIGN §3/M1's table. Dassa is the ungifted case: no
gift, keeps her Background's secondary skill, Heritage in play. Each carries the Technique named for
Facet level 1 (Serane *Read the Room*; Pello *Fleet Step*; Andra *Sharp Analysis*; Dassa *Weapon
Mastery — blades*; Ilesse *Lasting Impression*).
Accept: all five load and validate; two are Endurance 4–5; exactly one holds a domain the module's own
examples cast at Minor scope; the gifted pregens' domains are `lineage_gift` domains and their
`domain_source` is `"lineage"`.

**O3. Generate `03`'s pregen entries from the `.fof` files.** — 60 min
Files: `software/tools/build_scene_cards.py` (new, or extend `build_bestiary.py`),
`adventures/oraga_night/03_Masks_and_Agendas.md`, `software/tests/test_docs_consistency.py`.
The character block in each pregen entry becomes a generated marker; the prose around it stays
hand-written.
Accept: a no-diff invariant on the generated blocks; changing a `.fof` and not regenerating fails the
suite.

## M2 — Simulate, then fix the numbers *(blocked on `fun_second_act` T18)*

**O4. Simulate S3, the gate.** — 60 min
Files: `software/tools/combat_sim.py`, `research/simulation_log.md`, `docs/LOG_oraga_rewrite.md`.
Setup and acceptance in DESIGN §3/M2. Tune the captain's Resolve and entry point only — never the
recipe.
Accept: Hard band 40–60% counting any of the three endings as a win; phase fires in exchange 2 of the
captain's presence in ≥70% of runs; median 3–4 exchanges. **Record that exchange-3 entry is the sim's
proxy for the clock's third segment** (DESIGN ruling 5), or a later reader will print it as a rule.

**O5. Simulate S2, knives in the dark.** — 40 min
Accept: Standard band 65–85%; Tavva's stance triggers and Technique both fire in the logs.

## M3 — The Overture

**O6. Rebuild `01_Overture.md` to the front-matter battery.** — 120 min
Eight elements in DESIGN §3/M3's order, including the six named hooks and the format legend. Keep tone,
safety, canon-and-your-table, what-the-MM-knows, what-the-night-pays.
Accept: every hook is 3–6 sentences, names its agendas, and ends *"Begin at the Gatehouse Court, B1,
Movement I."*; the legend covers keys, read-aloud, sidebar species, S1–S5, enemy notation, clock column;
one signed designer's note saying why the Uninvited cannot be beaten and what the fights are for.

**O7. Delete the prelude wing; keep the aftermath.** — 45 min
Files: `adventures/oraga_night/06_Wings.md`.
The mask-maker becomes one aftermath paragraph (her casting-blanks still prove the gray masks came from
nowhere).
Accept: no prelude wing; nothing the prelude carried is lost — each item is either a hook (O6), a fact in
the introduction, or the mask-maker paragraph.

**O8. Trim and repoint `02` and `03`.** — 60 min
`02`: trim the public section to what a player needs on the night; the rest is `settings/valloh/V3`'s
gazetteer; MM-only truth unchanged. `03`: rewrite *Making Characters* to the seven steps with the Facet
loaded (one page; must not restate the Facet); *How You Got In* moves to the Overture as the hooks.
Accept: `02` has no duplicate of `V3`; `03` fits one page and points at `settings/valloh/`; agendas
verbatim.

## M4 — The ball, the clock, the alert state

**O9. B0. The Approach and the Line.** — 90 min
Files: `adventures/oraga_night/04_The_Ball.md`.
DESIGN §3/M4. Read-aloud under 120 words, naming no creature and resolving no action. The omen unchanged.
Accept: the scene contains Corval receiving by name, the Thenya delegation, the footman selling a card,
the hired swords with *House Boranis hired none*, and the pale factor already inside; the first roll is
social at Standard with the 7–9 named.

**O10. The palace on alert.** — 45 min
Files: `04_The_Ball.md`, above the keyed rooms.
One paragraph: steel bared, east wing forced, lights dead, and what the Bought do at each bell.
Accept: room entries say *if alerted* and stop; no room repeats the alert rules.

**O11. Pointer lines and Q&A blocks.** — 60 min
Files: `04_The_Ball.md`, `07_Cast_of_the_Ball.md`.
*Trouble You Can Walk Into* becomes pointer lines to the scene cards. Three Q&A blocks (Corval at the
gate, Vorlain by the wine, Raunu's summons) in the italic-question / quoted-answer / "if friendly" tier
format, 6–10 exchanges each, using lines already in the module wherever they exist.
Accept: every new answer line is flagged for O18; the three grey masks make Corval's answer slide.

**O12. The night clock.** — 60 min
Files: `08_Handouts.md`.
The table in brief §5.1: bell · the Uninvited · the Bought · what the players can move. The night-tracker
gains the clock column and the three scene-card IDs in the Optional Steel table.
Accept: one page; every conditional line names a thing a player can actually do.

## M5 — The gate

**O13. B12. The Gatehouse Court, Held.** — 120 min
Files: `05_The_Longest_Night.md`.
DESIGN §3/M6 in full: the contract, the trigger read-aloud, the fire clock, the objective, the three
endings as paired conditionals, tactics, Sparks printed, development.
Accept: nobody in the Bought goes Aggressive; the sergeant opens by naming the terms; the captain
negotiates from Resolve 3; "old coin" is written so it *can* be untangled and never confirmed; the factor
has no face and no name.

**O14. ⟨If History Breaks⟩ — the Bought change sides.** — 45 min
Files: `05_The_Longest_Night.md`, `06_Wings.md`.
The buy-out-before-midnight branch (brief §6.4) and the branch where a table somehow brings Veier to the
front — the captain's honour clause and the sect guard are the outs.
Accept: canon holds (the Radiant is faster than doors; Raunu still dies on his own choice); **the Second
Clause never succeeds**; the aftermath is visibly different and the module says so.

**O15. The aftermath thread and the advancement beat.** — 60 min
Files: `06_Wings.md`.
The inquest's interest in the company; the old coin matching nothing minted in Val'loh; the bought-out
captain as a patron. Plus: the one-shot ends with the standard 4 skill points and a reflection scene at
the epilogue question, and the aftermath wing over two sessions lands Facet level 1 under D16a's floor,
with the reflection scene placed at the inquest.
Accept: a character who plays the module through has grown, and the text says where and when.

## M6 — Scene cards

**O16. `09_Scene_Cards.md` with generated stat lines.** — 120 min
Files: new `adventures/oraga_night/09_Scene_Cards.md`, `software/tools/build_scene_cards.py`,
`software/tests/test_docs_consistency.py`.
S1–S3 full, S4–S5 half, fixed field order per DESIGN §3/M7. Stat lines generated into
`<!-- statblock: id -->` markers from the module's `.fof` files.
Accept: no-diff invariant on the generated blocks; each card has a *Use with* pointer and a Development
line pointing back; each enemy has an opening move, a priority target and a morale line; two or three
terrain-as-rules lines per card; S3's numbers are O4's.

**O17. Invariants and prose tests.** — 60 min
Files: `software/tests/test_docs_consistency.py`.
Extend INV-5's `Chapter X.Y` resolution to `adventures/`. Add the read-aloud word-count test (italic
blocks with a trigger line, under 120 words). Verify every scene-card enemy exists as a `.fof` and its TR
recomputes.
Accept: all three green; a deliberately broken pointer and an over-long read-aloud both fail.

## M7 — Apparatus and close-out

**O18. Troubleshooting sidebars, designer's notes, abridged box.** — 75 min
Files: `01_Overture.md`, `04`, `05`, `06`.
Four sidebars, each naming the derailment and giving two in-fiction answers: the table will not stop
hitting the Wept · the MM keeps defaulting to Hard · a 7–9 is not a penalty · someone asked whose turn it
is. One signed designer's note per Part. The abridged-run box (four hours: cut Undercurrent A and the
east-wing scene; run S1 or S2, not both; the gate as written).
Accept: every sidebar declares its species; INV-13 green.

**O19. README and the module's own front door.** — 30 min
Files: `adventures/oraga_night/README.md`.
Rewrite the contents table for the new file list; add the "what you need" line pointing at
`settings/valloh/`.
Accept: the contents table matches the directory; the Chapter VIII pointer from V14 is folded in.

**O20. `INVENTIONS_FOR_REVIEW.md` Revision 4.** — 45 min
Files: `references/oraga_night/INVENTIONS_FOR_REVIEW.md`.
Table every invention in this workstream: the Bought's contract and its three tasks, the factor, the old
coin's dynasty, the six hooks' details, B0's line scenes, every new Q&A line.
Accept: one table the owner can rule on; each row points at its file.

**O21. Style pass and close-out.** — 60 min
Run the humanizer and the style guide's amateur-tells list over every new block. Confirm the acceptance
question in DESIGN §1: can a table play this and use every flagship mechanic once?
Files: `docs/LOG_oraga_rewrite.md`, `docs/DECISIONS.md`.
Accept: `style/analysis/adventures.md` §9's checklist ticked item by item in the LOG; full suite green
with a reported pass count; a stated running time for the full and abridged runs; the LOG answers the
acceptance question with where each mechanic appears.

---

## STATUS: COMPLETE (O1–O21) — 2026-09-09

Every task in this file is done. Full suite green.

Rebuilt as the starter module. S2/S3 simulated (Series 13); the captain's phase re-authored as a conduct trigger (D22). §9 checklist: 16 of 18 met, 1 partial, 1 n/a. Module chapters renumbered I–IX after VIII's deletion.

Execution record, including what the numbers changed and what went wrong on the way: `docs/LOG_oraga_rewrite.md`.
