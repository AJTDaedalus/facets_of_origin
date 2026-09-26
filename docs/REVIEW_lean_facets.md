# REVIEW: Lean Facets v1.0, consolidated critical review

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` (revert pin: tag `pre-lean-facets`)
**Scope:** everything the overhaul produced: rules data, three books, module, engine, WebSocket layer, and app.
**Method:** five independent adversarial reviewers, each read-only and each instructed to verify its claims. Code and app findings were reproduced (scripts, Playwright), and design findings were measured with the real engine through `tools/combat_sim.py`. This file merges and de-duplicates them. The full reports, with quotes, line numbers, repro steps and screenshots, are:

| Report | Lens | C / M / m / nit |
|---|---|---|
| `REVIEW_lean_design.md` | Design, fun, balance, simplicity (sim-measured) | 3 / 12 / 13 / 6 |
| `REVIEW_lean_consistency.md` | Books ↔ data ↔ engine ↔ app ↔ module; canon | 1 / 11 / 27 / 21 (+4 canon rulings) |
| `REVIEW_lean_code.md` | Correctness, security, test quality (all C/M reproduced) | 1 / 14 / 17 / 5 |
| `REVIEW_lean_app.md` | Hands-on browser session, desktop and phone | 2 / 12 / 19 / 7 |
| `REVIEW_lean_prose.md` | Prose, AI texture, canon, licensing | 7 / 29 / ~55 / ~20 |

---

## Verdict

**As execution, it's strong. As design, it doesn't impress yet.** Every reviewer said some version of that sentence.

**What holds up:**
- The chassis is sound: 2d6 three tiers, HP and damage, flat armor, enemies rolling in the open, and levels 1–10.
- The monster card and the MM Toolbox are the best things on the branch. They are the "MM-driven variety" the owner asked for.
- The books agree with `facet.yaml` down to every talent's wording.
- The rules prose mostly reads human; the PHB rates B+.
- The app runs a full session with no JavaScript errors and no retired vocabulary.
- Novel-rule load fell from about 55 to about 20–25. A D&D player recognises most of the sheet.

**What doesn't:**
1. **It isn't simple yet.** Counted the way the complexity audit counted v0.3, a player holds **about 85 rules**, not the promised ~25. The ~25 came from bundling. It is far more *familiar* than v0.3, but it is not early-D&D *light*. (design C3)
2. **Half the presets can't fight, and it gets worse with level.**

   | Preset | Solo win rate vs one Standard foe of its own level |
   |---|---|
   | Warrior | 100% at every level |
   | Thaumaturge | 60% at level 1, 7% at level 10 |
   | Physician, Investigator | 21% at level 1, 0% at level 10 |

   An all-Mind party loses a standard fight 27–39% of the time. The Quick Start's claim that the presets are "balanced against each other" is false.
   
   The cause is a ruling I accepted from the PHB pass (attacks always roll Body), stacked on the smallest grit die, no armor, and HP that scales with Body. (design C1)
3. **Magic has no frame where it matters.** A 1-Fatigue control working ("a person bound") ends Boss fights, and the book's own showcase fight is won that way. From level 3, *Arcane Mastery* makes a signature working free forever. Casting ignores the level-gap rule, and nothing says whether casting counts as an attack. The simulator invented its own answer, which breaks the CLAUDE.md rule. (design C2, M5; code M)
4. **One talent turns the telegraph off.** *Sentinel* intercepts every attack on every ally, which cuts the chance of a PC dropping to a level 5 Boss from 56% to 10%. (design M1)
5. **The app has real security holes.** One is new: a character name is rendered without escaping, so a player can run script in the MM's browser and steal the MM token. The rest predate the overhaul:
   - MM notes leak through the character list and through `.fof` export.
   - Uploaded `.fof` files skip validation.
   - The server keeps everything, including the MM password, in memory, so a restart lets anyone re-run setup.
6. **Several rules exist in the books but not in the app, or the app gets them wrong:**
   - Weapon Master is a no-op for app-built characters, so the Warrior preset rolls d8, not the promised d10.
   - Exposure only reaches the foe you attacked.
   - Studied Foe, Anatomist and Warding Presence can never trigger.
   - Defend doesn't stop you attacking.
   - A stunt benefits the attacker instead of an ally.
   - The Harm toggle sticks between casts.
   - Costs the feed prints are never applied.
   - Nothing limits actions per exchange (one player attacked 8 times).
7. **The worked examples are wrong where I retuned the numbers.** MM1's worked examples still use the pre-retune damage row in four places. I updated the tables and the Toll Ogre card during the Boss retune and missed the prose below them. Two reviewers caught it independently.
8. **The G0 gate (a human session before any book rewrite) was skipped.** That followed the owner's `/goal` instruction, but it means none of this has met a table.

---

## Findings by severity (merged)

✚ = introduced by the overhaul · ○ = already present at `pre-lean-facets` · Sources: D design, K consistency, C code, A app, P prose.

### Critical
| # | Finding | Src | New? |
|---|---|---|---|
| X1 | **Stored XSS.** `app.js:307` renders a character name unescaped; the CSP allows inline scripts and any WebSocket host, so a player can take the MM's token (reproduced with Playwright). v0.3 escaped this. | C | ✚ |
| X2 | **Preset imbalance.** Mind and non-casting Soul presets lose to single same-level foes, worsening with level; the "balanced" claim is false. | D | ✚ |
| X3 | **Magic unbounded.** Control workings end Boss fights for 1 Fatigue; Arcane Mastery makes a working permanently free; casting skips the level gap. | D | ✚ |
| X4 | **~85 rules, not ~25.** The simplicity goal isn't met. | D | ✚ |
| X5 | **Weapon Master no-op** for every app-built character, the Warrior preset included (generic weapon items carry no kind). | K | ✚ |
| X6 | **MM notes leak.** Through a player's `.fof` export and through `GET /api/characters/{sid}` with any valid token, even from another session. | A, C | ○ |
| X7 | **Restart wipes everything.** Sessions, library, tracker, clocks and the MM password live in memory. After a restart anyone can run setup; tabs loop on "Session not found"; there's no import UI. | A | ○ |
| X8 | **Prose criticals.** MM1's worked-example damage is wrong (see 7); two Bestiary lines must not print (a `CLAUDE.md` citation and an in-joke); the Credits claim "none of their text" while III.1 uses two Dungeon World phrases verbatim. | P, K | ✚ |

### Major (grouped)
**Rules and design**
- Sentinel intercept-all is a dominant strategy. (D)
- MM1's fight-danger table is wrong in both directions: 4 Standard foes rated "real" drop a PC in 5% of fights; a Boss two levels up rated the same wins only 30%. (D)
- "Reach" is undefined, so ranged strictly dominates melee. (D)
- Whether casting is an attack is undefined. (D)
- The custom class is "pick 2 of 12", and armor, the biggest build lever, belongs to nobody. (D)
- The caster budget doesn't grow with level. (D)
- Mook mobs reward splitting, and area effects are dead against them. (D)
- Difficulty stacking (Hard/Easy sources) is unstated, and the engine silently decides. (K)
- III.1 contradicts itself on max dice and on Help. (K)
- Enemy naturals, stunt duration, and area magic against mobs are unruled. (K; owner ruling)

**Engine and app correctness**
- A Major working that repeats the same target in the list applies damage once per repeat (40 → 0 in one roll). (C)
- Breathers are unlimited mid-fight. (C)
- Healing before Hold On leaves a pending roll; healing or levelling a dying character leaves them "dying" above 0 HP. (C)
- Taking a casting talent at level-up leaves no magic block, so the character can't cast. (C)
- Respec drops Wider Domain's second domain. (C)
- A natural-2 Graceful Fail can pay twice over HTTP. (C)
- One broken optional Facet stops every session from being created. (C)
- Exposure only reaches the foe you attacked. (K)
- Studied Foe, Anatomist and Warding Presence can't be triggered, and Studied Foe expires early and applies to the studier. (C, K, D)
- Defend doesn't stop attacking, and improved Sentinel's attack at Hard isn't applied. (C, K)
- A stunt helps the attacker, not an ally. (A)
- Intercept pulls hits onto an ally already at 0 HP. (A)
- The Harm toggle and cast target persist between casts. (A)
- Printed costs are never applied, and there are no Fatigue or coin controls. (A)
- No per-exchange action or attack accounting. (A)
- The MM can't see who is Defending, Exposed or Covered. (A)
- A reload during a 10+ pick soft-locks the player. (A)
- An MM reload loses pending Spark calls and private results. (A)
- "Show the table at once" does nothing for most Toolbox buttons. (A)
- A player's seat is tied to one tab with a single-use invite. (A)
- On phones there's no 0 HP / dying alert, and the actions sit ~1,300px down. (A)
- No coin, respec or import UI. (A)

**Security (the rest)**
- `.fof` upload bypasses every rule: a level-10 character with 99 Sparks got through. (C)
- A cross-session same-name export includes MM notes. (C)
- A character name can write a file outside the session directory (MM-only, but X1 hands a player the MM token). (C)

**Simulator**
- `combat_sim.py:176` exposes casters on a 7–9. The engine has no such rule, so this breaks CLAUDE.md and skews calibration for parties with casters. (C, D)

**Books, data, canon**
- `spec/` still documents v0.1 .fof; README still mentions Threat Rating. (K)
- Oraga pregens carry Val'loh charges at 0 slots, while IV.2 and the app say 1. (K)
- The Uninvited cards say "it" against the owner's ruling that they are human. (P)
- Oraga's Overture contradicts chapters 04, 06 and 07 on the testament witnesses. (P)
- Val'loh has "consult by letter" in a world that bans writing. (P)
- "Chiefs' Concourse" is invented and unlogged. (P)
- The Artificers' Guild is stated as fact in `Zahna.fof`, `archive_guardian.fof` and B3, though it's an open ruling. (K, P)
- V0 inverts the Orthaen gift rate. (K)
- Zahna's signature workings are printed as fact while pending review. (K)

**Prose**
- Untouched v0.3 prose (Bestiary lore, Oraga 04–05, Val'loh) still carries heavy AI texture.
- All ten Bestiary *Adaptation* paragraphs share one template.
- Duplicated scenes and sidebars: the Quick Start retells II.3's door; III.3 and MM1 share a sidebar; MM6 repeats MM2.
- The model custom class breaks its own knack rule.
- Weak tables: Fight Complications, Exploration Complications, NPC Wants; Fight 24 is circular. (P)

**Licensing**
- Verbatim Dungeon World phrases in III.1.
- "NASTIER" is 13th Age's label.
- The Credits misattribute Fatigue-in-slots (it's Cairn's) and omit Blades, OSE/B-X, Ironsworn and the Alexandrian. The MM Manual and Bestiary have no credits.
- A corrected Credits draft is in `REVIEW_lean_prose.md` Appendix C. (P)

**Tests**
- One test locks in the notes leak.
- Scripted dice silently clamp out-of-range values.
- None of the Major paths above has a test. (C)

Minor and nit findings (about 130 in total) are in the source reports.

---

## Owner rulings needed (blocking some fixes)

1. **How every Facet fights.** Choose one:
   - attacks roll your Facet's stat;
   - the class knack names the attack stat;
   - keep Body and give Mind and Soul fighting talents.
   
   And whether to narrow the grit dice to d10 / d8 / d8.
2. **Magic's frame.**
   - A working aimed at a foe counts as an attack (level gap, cover, exposure).
   - Control effects on an Elite or Boss last one exchange.
   - *Arcane Mastery* becomes once per scene.
   - Casters get a Fatigue or slot budget that grows with level.
3. **The combination rules**, as one ruling:
   - How Hard and Easy sources stack.
   - Enemy naturals.
   - Stunt duration and beneficiary.
   - Area workings against mobs.
   - Define **engaged / reach**.
   - Cap Sparks per roll.
4. **The simplicity budget.** Hold the line at a real two-page card and move the rest to optional or MM-side, or accept "familiar, ~85 rules" as the goal.
5. **Canon:**
   - Is the Artificers' Guild canon? (Long-standing.)
   - The Uninvited's pronouns.
   - The testament witnesses.
   - The Val'loh letter line.
   - The Chiefs' Concourse.
   - The Orthaen gift rate.
   - Zahna's signature workings.
   - The custom class and pregen names.
   - The monsters' twists.
   
   (`references/*/INVENTIONS_FOR_REVIEW.md`)
6. **Keep "NASTIER"?** Rename it (e.g. *WORSE*, *HARDER*) to avoid 13th Age's label; it's a data and app rename as well as a books one.

---

## Recommended fix plan

**Phase 1: no ruling needed, do now (safety and correctness)**
1. **Security:**
   - Escape every user string in the SPA and tighten the CSP (X1).
   - Strip `notes_mm` from the list and export routes for players and check session membership (X6).
   - Validate uploads against the ruleset (level, Sparks, stats, HP).
   - Sanitize file names.
   - Reserve the "mm" identity.
   
   Tests first for each.
2. **Persistence:** save sessions, the MM password hash and combat state to disk and restore them on start, and add an import UI (X7). This was "planned" since v0.2.
3. **Engine bugs:**
   - Duplicate Major targets.
   - Breather limit in combat.
   - Hold On / heal / dying state machine.
   - Casting talent at level-up creates the magic block.
   - Respec keeps Wider Domain.
   - Double Graceful Fail over HTTP.
   - Broken optional Facet isolation.
   - Weapon kind on generic weapon items (X5).
   - Exposure from every foe in reach.
   - Defend blocks attacking.
   - Stunt beneficiary.
   - Intercept skips a fallen ally.
4. **App:**
   - Wire Studied Foe, Anatomist and Warding Presence.
   - Clear the Harm toggle and target after a cast.
   - Apply printed costs, and add Fatigue and coin controls.
   - Per-exchange action accounting and foe attack counts.
   - Show Defending, Exposed and Covered to the MM.
   - Persist pending 10+ picks and MM private state across reloads.
   - Make "show at once" work.
   - Reconnectable player seats.
   - A mobile 0 HP / dying alert, and put actions first on phones.
5. **Simulator:** remove the invented caster exposure; make its policy use Defend, Help and knacks.
6. **Books:**
   - Fix MM1's four worked examples.
   - Cut the two Bestiary lines.
   - Reword the Dungeon World phrases.
   - Replace the Credits with the corrected draft.
   - Fix III.1's dice and Help contradictions.
   - Fix pregen charge slots.
   - Rewrite `spec/`.
   - Widen INV-27 to README, `spec/` and `references/`.

**Phase 2: after rulings 1–4 (design)**
- Facet parity: a preset-parity test suite in the sim (each preset ≥60% solo vs a same-level Standard foe; per-PC Boss drop rates within 2×).
- The magic frame.
- The combination rules.
- Sentinel limited to one foe.
- Mob and area-effect fix.
- Regenerate MM1–4 from the sim.
- The actual two-page player and MM card, with everything off-card marked optional.

**Phase 3: G0**
- One human session, clocked, with the BRIEF's three questions and one fight each way (enemies roll / player-facing) before any further book work.
- Then the prose pass: a human line-edit of the Introduction, Bestiary adaptations, Oraga 04–05 and Val'loh; de-duplicate scenes; strengthen the weak tables.

**My view.** None of this argues for reverting to `pre-lean-facets`. The reviewers agree the chassis is right, and the worst security items were inherited, not introduced. Phase 1 is mechanical and should happen regardless. Phase 2 is where the owner's "does it impress" is decided, and it needs rulings 1–4 first.
