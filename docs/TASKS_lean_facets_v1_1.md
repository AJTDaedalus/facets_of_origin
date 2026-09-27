# TASKS — Lean Facets v1.1 (addressing the critical review)

Source findings: `docs/REVIEW_lean_facets.md` (IDs X1–X8 and the grouped Majors) and the five `REVIEW_lean_*.md` reports.
Strategic decisions: `docs/BRIEF_lean_facets_v1_1.md` (D1–D10, with research and recommendations).
Rules: TDD for every behaviour change (test first, ≥3 per public function); `combat.py` / `magic.py` / `character.py` remain the only rules implementations; every rules change updates facet.yaml → engine → books → quick refs → app text in the same commit (CLAUDE.md sync workflow); full suite green before each phase closes.

Owner guidance (2026-09-26): the two-page budget is a guide, not a limit — the target is **felt simplicity** (few concepts before play, one way to do each thing, no exception rules).

---

## Phase 1 — Safety and correctness (no ruling needed; start immediately)

| # | Task | Files | Acceptance (tests first) | Review IDs |
|---|---|---|---|---|
| P1.1 | **Escape every user string in the SPA**; one `esc()` helper used by every template; tighten CSP (no `unsafe-inline` scripts, `connect-src 'self'`) | `app/static/js/*.js`, `app/main.py` | Playwright test: a character named `<img src=x onerror=...>` renders as text on MM and player pages; CSP header test | X1 |
| P1.2 | **MM notes never reach players**: strip `notes_mm` from list and export for non-MM tokens; enforce session membership on every character route | `routes/character.py` | tests: player token on list/export gets no `notes_mm`; cross-session token → 403; replace the test that locked the leak in | X6 |
| P1.3 | **Validate uploads** against the ruleset (level 1–10, Sparks ≤ 3, stats per creation rule + level raises, HP ≤ computed max, talents legal); reject with reasons | `routes/character.py`, `character.py` | tests: the reviewer's level-10 / 99-Spark file is refused; a legal pregen passes | Code M |
| P1.4 | **Safe file names** for character persistence; reserve the `mm` identity for the MM | `session.py`, `routes/session.py` | tests: `../` names cannot escape the dir; invite named "mm" refused | Code M/m |
| P1.5 | **Persist sessions**: sessions, MM password hash, library, tracker, clocks, combat state to `data/`; restore on start; setup refuses when a password exists; SPA recovers from "Session not found" with a clear message; **import .fof** in the Build tab | `session.py`, `routes/session.py`, `main.py`, static | tests: restart round-trip; setup-after-restart refused; import happy/illegal/garbled | X7, App M |
| P1.6 | **Engine state machine**: Hold On pending cleared by heal; healing/levelling from dying sets status correctly; breather refused while combat is running (or once per scene); duplicate Major targets de-duplicated; Graceful Fail pays once; casting talent at level-up creates the magic block (domain + two workings required); respec keeps Wider Domain; one broken optional Facet does not block base-only sessions | `character.py`, `magic.py`, `engine.py`, `registry.py`, `routes/rolls.py` | one failing test per reviewer repro (`REVIEW_lean_code.md`), then green | Code M ×8 |
| P1.7 | **Books-promised behaviour the engine/app lacks**: weapon `kind` on generic weapon items and in the creation wizard (Weapon Master works for app-built Warriors); exposure applies to every foe in reach (pending D3's definition — implement "every foe engaged with you"); Defend forbids attacking; improved Sentinel attacks at Hard; stunt opening benefits an **ally**; Intercept skips allies at 0 HP; wire Studied Foe / Anatomist / Warding Presence (WS events + UI) | `facet.yaml` items, `combat.py`, `websocket.py`, static | tests per behaviour; e2e: Warrior deals d10 with Weapon Master | X5, K/A/C Majors |
| P1.8 | **Simulator obeys CLAUDE.md**: delete the invented caster-exposure rule; policy uses knacks, Defend, Help | `tools/combat_sim.py` | grep-based test that the sim imports every rule it applies; rerun ladder, log numbers | Code M, D M5 |
| P1.9 | **App table-state**: per-exchange action accounting (one action per PC, `attacks` per foe) with MM override; MM sees Defending / Exposed / Covered / Openings; persist pending 10+ pick and MM-private results across reload; "show at once" works for all Toolbox buttons; clear Harm toggle and target after each cast; apply printed costs (Fatigue, damage) or offer one-click apply; coin and Fatigue controls; reconnectable player seats (re-issue invite / resume token); mobile: 0 HP / dying modal, actions above the sheet | `websocket.py`, `session.py`, static | ws tests + e2e flows for each; mobile screenshot check | App Majors ×10 |
| P1.10 | **Books corrections**: MM1's four worked examples use the current damage row; cut Bestiary Front_Matter:19 (`CLAUDE.md`) and B1:303 in-joke; reword III.1's two Dungeon-World phrases; replace Credits with the corrected draft (all three books); fix III.1 max-dice and Help contradictions; pregen curio slots agree with IV.2; `spec/` rewritten for .fof v1; README residue; widen INV-27 to README, `spec/`, `references/phb-examples.md`; add INV-28 "worked-example numbers recompute from facet.yaml" for MM1 | books, `spec/`, `tests/test_docs_consistency.py` | new invariants fail first, then pass | X8, K/P Majors |
| P1.11 | **Canon holding pattern** (no invention): the Uninvited back to he/she per ruling; Artificers' Guild removed from `archive_guardian.fof`, `Zahna.fof`, B3 until ruled; Oraga testament-witness contradiction and V1 "by letter" and V3 "Chiefs' Concourse" and V0 Orthaen rate flagged in `INVENTIONS_FOR_REVIEW.md` and reverted to the pinned canon wording where one exists | books, `.fof`, references | consistency test passes; owner list updated | K/P canon |

**Phase 1 exit:** full suite green incl. e2e; reviewers' repro scripts (scratchpad `test_repro_ws.py`, `repro_*.py`) all fail to reproduce; LOG updated.

---

## Phase 2 — Design changes (after the owner approves BRIEF v1.1 decisions D1–D10)

Implements `docs/BRIEF_lean_facets_v1_1.md` D1–D10 as approved. Each task: facet.yaml → engine (tests first) → app → books (body, Quick Start, MM5, Glossary) → regenerate → full suite. Research files hold the sim drivers' logic; port what a test needs into `tools/combat_sim.py` (never a private rule).

| # | Task | Decision | Acceptance (tests first) |
|---|---|---|---|
| P2.1 | **Attack with your Facet's stat**; Mind grit d6→d8; light armor in Investigator/Physician/Speaker/Wanderer kits; "attack with Body" boxed dial | D1 | engine tests; **new parity suite** in `test_combat_sim.py`: every preset solo vs same-level Standard ≥70% at L1/L5 and ≥50% at L10; per-PC Boss drop rates within 2× |
| P2.2 | **Intercept = one telegraphed attack aimed at an ally you can reach; Sentinel = one from each of two foes** | D2 | engine + ws tests; sim: allies-down vs L5 Boss with a Guardian 10–30% |
| P2.3 | **Engagement by telegraph**: telegraphing a melee attack engages; ranged attacks/workings while engaged are Hard; exposure applies to the next attack from any foe; Cleave/Whirlwind/Intercept key to engaged; delete "out of reach" line | D3 | engine tests; app shows Engaged chips; III.3 rewritten |
| P2.4 | **Facet armor row** (Body heavy+shield, Soul light+shield, Mind light); over-armored → attacks and workings Hard (replaces heavy-armor Fatigue); **custom class may take one starting talent from any Facet** (never casting) | D4 | engine + wizard tests; sim: heavy-armored Mind Tactician ≤ Warrior |
| P2.5 | **Control sized by role** sentence + strict dial; engine applies "hindered one exchange" to Elite/Boss; Archive Guardian vignette replaced by the research beat | D5 | magic tests (Mook/Standard stopped; Elite/Boss hindered; Bloodied+Major ends); INV-8b arithmetic passes |
| P2.6 | **Working aimed at a foe is an attack** for Easier/Harder; 7–9 cost menu always includes "you are exposed"; harm damage re-tuned (weapon die +1 step or 1d10, by sim) | D6 | magic/combat tests; sim has no private exposure rule (P1.8) |
| P2.7 | **Casting talent: +1 Fatigue-only slot at 3/5/7/9**; **Arcane Mastery once per scene** (and on the Soul menu if approved) | D7 | character/magic tests; sim: caster share of daily actions 45–60% at L1/5/9 |
| P2.8 | **One step, one cap, one clock**: Easier/Harder cancel and never stack; ≤2 extra dice per roll; all fight states expire at exchange end; stunt benefits someone else; doubles as ruled; mob drop rate by damage (sim first); cut +4 ceiling and Very Hard level-gap band | D8 | engine tests replacing the old stacking tests; III.1 contradictions gone; new INV: no "unless/except" on the cards |
| P2.9 | **Cards and the MM-side move**: player card (~35 rules) + caster box + level-up box + MM card as Quick Start / MM5; move ~40 rules to MM-side chapters; dials boxed beside their rules | D9 | docs tests: card rule count ≤ target; every dial states its default; G0 checklist written |
| P2.10 | **One action each; foe attacks as carded and telegraphed**; app action tokens, attack pips, state chips, one-click end of exchange | D10 | ws + e2e tests: a second attack in one exchange refused; an Elite's third attack refused; chips visible to MM |
| P2.11 | **Retune and regenerate**: re-sim the ladder after P2.1–P2.10; adjust monster damage/attack in facet.yaml; regenerate MM1–4 fight-reading table from the sim, MM1 level table, Bestiary, scene cards; fix every worked example | D1–D8 | ladder suite (trivial / standard 2–4 exchanges / Boss drops a PC ≥25%) and parity suite green; INV-26/28 green |

---

## Phase 3 — G0 and the prose pass

| # | Task | Acceptance |
|---|---|---|
| P3.1 | **G0 human session**: one clocked session with 3–4 people; one fight with enemies rolling and one player-facing; the three questions (*fast or flat? did anyone miss a rule? could the MM keep up?*) | notes in `docs/LOG_lean_facets.md`; decisions revisited |
| P3.2 | **Human line-edit** of I_Introduction, Bestiary Adaptations (de-template), Oraga 04–05, Val'loh | prose review's AI-texture metrics below 5 em-dashes / 1,000 words; no "not X — it's Y" |
| P3.3 | **De-duplicate** repeated scenes/sidebars (Quick Start door vs II.3; III.3 vs MM1 sidebar; MM6 vs MM2) — one home each, pointers elsewhere | INV-11/5 pass; prose review items closed |
| P3.4 | **Strengthen weak tables** (Fight/Exploration Complications, NPC Wants; fix Fight 24) | table review re-graded ≥ B+ |
