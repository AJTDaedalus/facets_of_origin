# RESEARCH — Fun Audit: Evidence Digest from Playtests and Simulations

**Date:** 2026-09-08
**Purpose:** Evidence base for a Brain-tier audit of the question *"In chasing simplicity, has the game lost fun? Is combat fast but flat? Are player decisions meaningful or dominated?"* This file extracts what the playtests and simulations actually observed, with `file:line` citations. It does not judge the rules.
**Scope read:** `playtest/01`–`08` (every file), `research/simulation_log.md`, `research/armored_enemy_breaking_problem.md`, `docs/DESIGN_agentic_playtests.md`, and `git log` for fix dates.

**Read this first.** No human has ever played this game in the record. Every "player quote" below was written by a language model. Section 1 grades each source; the rest of the file should be read with that grade in hand.

---

## 1. Provenance

### 1.1 Producer, date, and rules version per playtest

| # | Playtest | Produced by | Date | Party | Rules version tested | Reliability grade |
|---|---|---|---|---|---|---|
| 01 | Thornwall Undercroft | LLM-written session log using **pre-generated dice (seed 42)** (`playtest/01_thornwall_undercroft/session_log.md:4-9`); characters, scenario, report all LLM-authored | 2026-03-13 (log :4); committed 1d9bbb1 2026-03-14 | 3 PCs + MM, PS 3 (`playtest_report.md:5`) | v0.1 (`playtest_report.md:2`): enemies had Endurance + condition track (`session_log.md:429` "Endurance 6"), pre-technique magic **one step harder** (:161), no NPC-attack rules, no group-roll rule | **B-** — dice are real (pre-rolled), rules mostly followed, but the "table" and all quotes are fiction |
| 02 | Silence of Ashenmoor | LLM-written log, pre-generated dice (seed 73) (`playtest/02_silence_of_ashenmoor/session_log.md:9`); 25 Playwright e2e tests ran the *tool*, not the session (`digital_tool_log.md:1-3`) | 2026-03-13 (`playtest_report.md:3`); committed 1d9bbb1 2026-03-14 | 4 PCs + MM (`playtest_report.md:5`) | v0.2 post-audit (`playtest_report.md:4`): pre-technique penalty removed, NPC-attack tiers, group rolls added (:14); enemies still on Endurance/condition track (`session_log.md:544`, :711 "Endurance 10") | **B-** — same as 01 |
| 03 | Boss Stress Test | **Monte Carlo script** `run_pt03.py` driving `app.game.combat` (`playtest/03_boss_stress_test/results.md:75`); n=300 × 7 seeds | 2026-07-11 (:5-6); committed c0553ed | Mordai/Zahna/Zulnut PS 3 (:7) | v0.3 D1/D2 (Resolve, armor budget); re-run post-A14 (enemies never react) (:14) | **A** for arithmetic, **n/a** for feel — posture/reaction/Spark choices are heuristics (see §3.6) |
| 04 | Resource Tax | **Script against the live server**, real `random.randint` dice, 5 sessions (`playtest/04_resource_tax/results.md:5, :11`); driver `run_pt04_live.py` | 2026-07-11; committed c0553ed | Mordai/Zahna/Zulnut | v0.3 with Recipe-Table rosters (`scenario.md:76-80`) | **A** for arithmetic; driver "never attempts the lateral solutions" (`results.md:21`) |
| 05 | Technique Showcase | Script driving `Character.advance_skill` / `select_technique` — **advancement pacing only**; the arena combat scenario "remains available for a later session", i.e. **never run** (`playtest/05_technique_showcase/results.md:6-17`) | 2026-07-11 (:3) | one Soul character (:24) | v0.3 pacing (`facet_level_threshold: 5`) — **superseded by D16** 2026-08-10 (`docs/DECISIONS.md:895-960`) | **A** for the formula it checks; says nothing about play |
| 06 | Expert/Novice "campaign" | LLM-written scripted log (`session_log.md`), an LLM "agent-on-agent" log (`agent_playtest_log.md`), one **live server-rolled** session (`live_unscripted_playtest_log.md:4`), and 9 one-exchange "adventures" claimed server-rolled (`agentic_playtest_compendium.md:3`) | July 9–10 2026 (`playtest_report.md:3`; `live_unscripted_playtest_log.md:4`); committed c0553ed 2026-07-11 | 4 PCs + MM (scripted); 2 PCs (compendium) | "Pre-Release" (`session_log.md:3`) — but **played with invented HP-style rules**: "A standard strike deals 2 damage… Light Armor… downgrades the damage by 1. Alaric takes 1 damage to his Endurance pool" (`session_log.md:97`), "Medium Armor (Armor 2)… blocks the 2 damage" (:186), "critical 13… 3 damage, completely bypassing its armor" (:232), Steam Blast "1 Endurance damage" (:170); live session: "armor is permanently shattered! The golem takes 2 damage… 10 Endurance to 8" (`live_unscripted_playtest_log.md:97`) | **D** — Endurance was treated as hit points, armor as damage reduction, and 0 Endurance as death (`fun_and_consequence_review.md:26`). None of that is the ruleset. Compendium dice repeat implausibly ([5,4]/[4,4] pairs in adventures 5, 6, 7 at `agentic_playtest_compendium.md:94-97, :117-121, :139-143`) |
| 07 | Oraga Night ×20 | LLM-written scene logs with **LLM-invented dice** plus a **hardcoded script** whose engine rolls were **over-counted 4×** (`playtest/07_oraga_night_playtests/playtest_report.md:3-30`; `docs/DESIGN_agentic_playtests.md:16-56`) | committed dc60dee 2026-07-31 with the invalidity notice | 4 pregens Facet Level 1 (`characters.md:10`) | v0.3-era (Tavva "Resolve 3" `session_log_20.md:41`; armor charges `session_log_09.md:57`) but MM invents mechanics ("'Watched' condition (Tier 1)" `session_log_01.md:56`; "2 damage… Prone (Tier 1)" `session_log_09.md:41`) | **F for numbers** (project's own ruling, `playtest_report.md:8`); qualitative MM-behaviour notes "may still be worth something" (`DESIGN_agentic_playtests.md:80-82`) |
| 08 | NPC-variance subagent session | **Five Claude subagents on the real app**, each with its own account; every die from the engine; validator found **no confabulated mechanics** (`playtest/08_npc_variance/subagent_session/report.md:8-12, :24-30`) | 2026-07-31 (:3); committed 62afb3a 2026-08-02 | 4 PCs (Zahna/Mordai/Zulnut + Ilesse) (`scenario.md:73-78`) | v0.3 + Wave-4 audit; pre-WS-1..6 fun/ease fixes | **A-** for what it recorded; **two beats, one exchange, n=1** (:19-20, :153) |

### 1.2 What the project itself says about the corpus

- "The dice in the session logs were not rolled… Across roughly 60 dice there is not a single 1, and almost no 6s" (`docs/DESIGN_agentic_playtests.md:16-29`). "The 'play' was a hardcoded script… No agent chose anything" (:48-56). "The narrative was not a record of a session; it was fan-fiction about one" (:74-77).
- "Agentic playtests cannot validate fun… Whether the game is enjoyable to humans is not measurable here" (`docs/DESIGN_agentic_playtests.md:378-384`). "A confirmed problem is real; an unconfirmed one is not evidence of absence" (:392-394).
- "Playtest 07 used 'Novice/Expert', which mostly generated rules-lawyering — a correction loop, not a table" (:131-134).
- All PC-side simulation figures before Series 7 are "SUPERSEDED (v0.2 semantics)… every PC-side figure below (win rate, Broken rate, exchange count, lethality) is invalidated" (`research/simulation_log.md:5-17`).
- PT02's comparison table misreports PT01: it lists PT01 at 24 rolls, 2 magic uses, 0 Sparks (`playtest/02_silence_of_ashenmoor/playtest_report.md:188-191`) where PT01's own report says 33 rolls, 5 magic uses, 2 Sparks (`playtest/01_thornwall_undercroft/playtest_report.md:7-9`). The LLM-authored reports are not internally reliable even about each other.

### 1.3 Rules that changed after the playtests that tested them (git dates)

| Rule change | Commit | Date | Playtests that predate it |
|---|---|---|---|
| Pre-technique magic penalty removed (Minor scope only, no difficulty step); NPC attack incoming tiers (Mook=T1, Named/Boss=T2, posture shifts reaction difficulty); Group Rolls | 1d9bbb1 | 2026-03-14 | 01 |
| Combat simulator, Spark cadence, encounter recalibration | 4d73321 | 2026-03-15 | 01, 02 |
| **v0.3**: enemy Endurance/condition track → **Resolve** pool (D1); PC armor per-scene downgrade budget (D2); 0-Endurance escalation retired (A6); **K1** Aggressive surcharge on first reaction only; **enemies never react** (A14, enemy Parry removed); Boss phase re-keyed to Resolve threshold; Threat Clocks for hazards (III.2); Trouble Table; domain example intents; Spark refund variant flag (default off) | c0553ed | 2026-07-11 | 01, 02, 06, (03 first run) |
| "0 Endurance = Absorb only, absolutely" | 6d1e935 | 2026-07-31 | 01–07 |
| Reckless Press cut | 6dbe6cd | 2026-07-31 | 01–07 |
| MM2 "Adjudicating Magic"; Trouble Table canonical home | ae2577c, d9f1363 | 2026-07-31 | 01–07 |
| Strike accepts any attribute/skill pairing in the book (F1); Specialty "when no skill fits" (F3); one-click Apply on strike (F4) | 62afb3a | 2026-08-02 | 01–08 (08 found them) |
| Sparks reset to 3 each session, no carry-over (D1 fun/ease) | 9142c90 | 2026-08-08 | all |
| **Open tag** replaces rider menu vs enemies | 036557a | 2026-08-08 | all |
| Uncontested exchanges advance the situation free; Withdrawn recovers up to pool | 15037bf | 2026-08-08 | all |
| TR-budget/multiplier tables cut; actor count is the dial | 582c14b | 2026-08-08 | all |
| Enemy stances from conduct triggers; three worked enemy Techniques in MM1 | 890f2d6, 8a28738 | 2026-08-08 | all |
| Casting adds the tradition's skill (Attune/Lore) | 41631ee | 2026-08-09 | all |
| Skill-point bank; Body has no magic; traditions named | 66e74e8, 859b65c, 0cfa79d | 2026-08-09 | all |
| Quick Start rebuilt | b556a3d | 2026-08-10 | all |
| **D16** rank caps + escalating mark curve (3/5/8); D16a | ba4457c, b616148 | 2026-08-10/11 | all (05 measured the superseded curve) |
| **Natural 12 / natural 2 / Borrowed Trouble**; social 7-9 texture | 4551a71 | 2026-08-13 | all |

The most recent play artifact of any kind is PT08 (2026-07-31). Every rule from 2026-08-02 onward is untested at any table, simulated or otherwise, except where Series 10/11 sims cover it (Open tag, uncontested rule, casting curves).

---

## 2. Combat duration and share

### 2.1 Exchanges per fight

| Source | Fight | Exchanges | Citation |
|---|---|---|---|
| PT01 | 3 Mooks (Skirmish) | 2 (+1 free opening Strike) | `playtest/01_thornwall_undercroft/playtest_report.md:35`; `session_log.md:225-341` |
| PT01 | Archive Guardian (Named TR 8, v0.1) | 3 | `playtest_report.md:35`; `session_log.md:442-656` |
| PT02 | 4+2 Husks (Mooks) | 2 | `playtest/02_silence_of_ashenmoor/playtest_report.md:100`; `PROGRESS.md:31` |
| PT02 | The Hollow + 2 Husks (Hard, TR 11) | 2 | `playtest_report.md:205`; `session_log.md:568` |
| PT02 | The Resonance (Boss TR 14, Deadly) | 2, bypassed by lateral solution | `playtest_report.md:139-145` |
| PT03 (n=300×7) | Iron Crucible (Boss, eff. Resolve 12) post-A14 | median **3** every seed; mean 3.3–3.4; min 3; max 6–8 | `playtest/03_boss_stress_test/results.md:18, :31-38` |
| PT03 pre-A14 | same | mean 2.9, median 3, **min 1**, max 7 | `results.md:63, :126` |
| PT04 live, session 1 | Skirmish (3 Mooks) / Standard (3 Named + 1 Mook) / Hard (3 Named + 2 Mooks) | **1 / 4 / 3** | `playtest/04_resource_tax/results.md:38-42` |
| PT06 scripted | 4 Sentinels (Mooks) / Sentry Golem "TR 9" | 2 / 2 | `playtest/06_expert_novice_campaign/session_log.md:58-136, :156-239` |
| PT06 live | 2 Sentinels / Golem | 1 / 2 (+ a final magic strike) | `live_unscripted_playtest_log.md:42-79, :83-146` |
| PT06 compendium ×9 | one exchange each, 2 PCs | 1 | `agentic_playtest_compendium.md` (every roll table is one exchange) |
| PT07 (invalid) | every combat scene (04, 09, 14, 15, 19, 20) | 1 — each log ends after a single exchange | e.g. `session_log_04.md:77`, `session_log_09.md:63`, `session_log_20.md:58` |
| PT08 | 2 Dust Constructs (Mooks) | 1; second construct "lost interest" without a second exchange | `subagent_session/transcript.md:119-126`; `metrics.json:62` `total_exchanges: 1` |
| Sim Series 9 Part A (v0.3) | 3/5/7 Mooks; Sergeant solo; Guardian solo | median 2.0 / 2.5 / 4.0 / **1.0** / 3.0 | `research/simulation_log.md:531-537` |
| Sim Series 7 G1 | Guardian solo (Resolve 8) | median 3.0, mean 2.8 | `simulation_log.md:430-434` |
| Sim Series 10 Part C | Guardian solo, by-the-book with Open tag | **median 2** (floor of the 2–4 acceptance band) | `simulation_log.md:688-694` |
| Sim Series 10 Part B | 15 Mooks | mean 7.5–7.7 (default AI); pure-turtle stalls to the 20-exchange cap without a clock, loses in exactly 4 with one | `simulation_log.md:668-673` |
| Sim Series 6 (**superseded**) | Named solo TR 8/10/12 | 5.2 / 7.6 / 10.6 | `simulation_log.md:294-296` |
| Sim Series 6 (**superseded**) | Boss TR 12/16 | 14.6 / 12.8 ("long… but not grindy") | `simulation_log.md:310-311, :382` |

Under current rules no measured or written fight has exceeded 4 exchanges except the Mook-swarm and PT03 tails. The superseded v0.2 boss fights of 12–16 exchanges (`simulation_log.md:310-313`) are the only long fights on record, and the project retired that model.

### 2.2 Minutes per fight and session share

All minute figures are **estimates written by the LLM narrator**; nothing was clocked.

| Source | Figure | Citation |
|---|---|---|
| PT01 | "Combat was quick (2-3 exchanges per fight, ~10-20 minutes real time)" | `playtest/01_thornwall_undercroft/playtest_report.md:15` |
| PT01 | Mook fight "~10 minutes", Guardian "~20 minutes" | `playtest_report.md:35`; player aside "Maybe ten minutes of real time?" `session_log.md:343` |
| PT01 | Act I social ~15 min / 2 rolls; Act II exploration+Mook fight ~60 min / 20 rolls; Act III Guardian+vault ~30 min / 11 rolls; whole session "~2.5 hours simulated" | `playtest_report.md:4, :67-69` |
| PT02 | "~3 hours simulated" | `playtest/02_silence_of_ashenmoor/playtest_report.md:8` |
| PT06 | "roughly 2 hours"; simultaneous exchanges "cut the time of typical skirmish encounters by half compared to traditional TTRPGs" | `playtest/06_expert_novice_campaign/playtest_report.md:13, :20` |
| PT06 scenario | planned Act I 20 min / Act II 50 min / Act III 50 min | `scenario.md:18, :24, :29` |

### 2.3 Rolls per fight and combat share of rolls

| Source | Combat rolls | Non-combat rolls | Combat share | Citation |
|---|---|---|---|---|
| PT01 | Mook fight 6 (rolls 11–16); Guardian 12 (rolls 20–31, incl. 3 forced re-rolls) = 18 | 15 (rolls 1–10, 17–19, 32–33) | 55% of 33 | `playtest/01_thornwall_undercroft/session_log.md:781-815` |
| PT02 | Husks 11 (rolls 6–16); Hollow 9 (17–25); Resonance 6 (27–32) = 26 | 6 (rolls 1–5, 26) | 81% of 32 | `playtest/02_silence_of_ashenmoor/session_log.md:845-880` |
| PT04 live s1 | 25 rolls across 3 fights (Mordai 12, Zahna 4, Zulnut 9); 133 rolls across 5 sessions | 0 — scenario is "pure Strike/reaction combat" | 100% | `playtest/04_resource_tax/results.md:27-32, :51, :55` |
| PT06 scripted | ~15 of ~24 (rolls 4–10, 12–24) | 4 (rolls 1–3, 11) | ~80% | `dice_rolls.txt:5-80` |
| PT06 batch (9 vignettes + 1) | 51 server rolls total, every one a strike / dodge / cast inside one exchange | 0 | 100% | `playtest_batch_report.md:9-17` |
| PT07 (invalid) | ~4 per combat scene | 4 per social scene (one check per player) | ~50% of scenes | `dice_rolls.txt:1-40` |
| PT08 | 1 (Penny's Strike) | 3 (Sophia Lore, Penny stealth-ish, Toby Attune) | 25% of 4; `decision_to_roll_ratio: 1.25` | `subagent_session/transcript.md:14, :22, :26, :96`; `metrics.json:56` |

---

## 3. Decision dominance

### 3.1 Posture declarations actually recorded

| Source | Declarations (Aggressive / Measured / Defensive / Withdrawn) | Notes | Citation |
|---|---|---|---|
| PT01 (5 exchanges × 3 PCs) | **6 / 5 / 3 / 1** | Kael Aggressive 4 of 5; Mira Withdrawn once at low Endurance ("has nothing left") | `playtest/01_thornwall_undercroft/session_log.md:245-249, :299-303, :444-448, :518-522, :618-622` |
| PT02 (5 exchanges × 4 PCs) | **7 / 7 / 5 / 1** | Rowan Withdrawn at 1 Endurance to recover, then free Intercept from Withdrawn | `playtest/02_silence_of_ashenmoor/session_log.md:243-246, :308-311, :427-430, :518-524, :640-643, :558-564` |
| PT06 scripted (4 exchanges × 4 PCs) | **1 / 11 / 3 / 1** | Alaric Defensive every exchange; Measured is the default | `playtest/06_expert_novice_campaign/session_log.md:66-69, :118-121, :158-161, :214-217` |
| PT07 (invalid dice; 6 combat scenes) | Dassa **Defensive 6/6**; Pello Aggressive 2, Measured 4; others Measured; one Withdrawn (Ilesse, 09) | In 14 and 15 the MM assigns postures for the players (`session_log_14.md:16`) | `session_log_04.md:23-29`, `_09.md:18-24`, `_14.md:16`, `_15.md:17`, `_19.md:17-18`, `_20.md:18-19` |
| PT08 (1 exchange × 4 PCs) | **0 / 4 / 0 / 0** — one explicit declaration (Penny, Measured) with the arithmetic done out loud; three players never declared and defaulted to Measured | `events.jsonl:38` (`combat_started` shows all four `"posture": "measured"`), `:41` (single `posture_declared`); `transcript.md:93-94` |
| Simulations (all series) | not a decision: `choose_pc_posture` returns Aggressive above 66% Endurance, Measured 33–66%, Defensive below, Withdrawn at 0 | `software/tools/combat_sim.py:267-282`; PT04 driver same shape at 80%/25% (`playtest/04_resource_tax/run_pt04_live.py:292-302`); PT03 uses the sim function (`run_pt03.py:133`) |

Reasons given for posture at the (fictional) table: Aggressive "These are Mooks. I want to hit hard" (`01/session_log.md:245`); Measured "I don't want to get caught in Aggressive if one comes at me" (:247); Defensive "Mira's not a fighter" (:249); Measured vs Guardian "I want to feel this thing out first" (:444); Withdrawn "I have nothing left" (:622) / "I need to recover" (`02/session_log.md:518`); Aggressive as casters "If magic is what works, I need to be on offense" (`02/session_log.md:430`). PT08's only reasoned declaration: "Aggressive is off the table — offense +1 but reactions cost 2 each, that is 4 Endurance for two dodges and I own 3. It would literally kill me. Defensive makes both dodges free but costs me my offense… So Measured" (`08/transcript.md:93`).

### 3.2 "Always correct" strategies and dominance findings

| Finding | Source | Citation |
|---|---|---|
| Vs Mooks, "the optimal strategy is always Aggressive posture" because Mooks are Measured and die in one hit | PT01 report | `playtest/01_thornwall_undercroft/playtest_report.md:137` |
| Aggressive at low Endurance is the catastrophic error ("That single posture decision was the difference between survival and defeat") | Sim Series 3 (superseded) | `research/simulation_log.md:103, :111, :180` |
| Over a fight to conclusion, **Aggressive vs Measured made no measurable difference** (~84% Broken both, n=1000): "A reaction ROLL's success chance never depends on posture, only the Endurance to attempt one does" | Sim Series 8 | `simulation_log.md:488` |
| K1 (surcharge on first reaction only) cut Aggressive Broken rate 89%→75% (15.7–18.7% across seeds) while preserving the ≤1.7pp offense edge — i.e. Aggressive's *win-rate* advantage over Measured in a 2-exchange window is 1.1–1.7 percentage points | Sim Series 8 | `simulation_log.md:494-515` |
| A5 15-Mook fight won 98% "via Withdrawn cycling… Mordai solos remaining Mooks over 14.5 exchanges" (superseded model) | Sim Series 6 | `simulation_log.md:282, :287` |
| Under current rules the default AI contests every exchange (0 uncontested); a **pure-turtle party loses 100%** once a 4-segment clock is present; "the stall itself is dead" | Sim Series 10 | `simulation_log.md:668-684` |
| "Mook swarms never threaten the party at all: even at 30 Mooks, mean Broken = 0.00"; Mook count "is not a usable Standard/Hard/Deadly lever" | Sim Series 9 | `simulation_log.md:568` |
| "The dominant variable is simultaneous Named/Boss-tier actor count, not weighted TR. A solo enemy is ~100% regardless of TR" | Sim Series 9 | `simulation_log.md:570` |
| Rider→Easy snowball: one 10+ makes every subsequent Strike Easy; Guardian dies exchange 1 in the verbose run | Sim Series 7 | `simulation_log.md:415` |
| Solo Boss has "exactly one attack per exchange, against one PC"; a PC needs two same-type Tier 2 hits to Break — "a cadence a solo, single-target attacker essentially never sustains" | Sim Series 7 | `simulation_log.md:416-418` |
| Focus-fire opens every PT03 fight: "All three open Aggressive and focus-fire" | PT03 | `playtest/03_boss_stress_test/results.md:47, :104` |
| Sparks vs a Boss "were spent to *end it faster*, not to survive" | PT03 | `results.md:151` |

### 3.3 Reaction choice frequency

| Source | Dodge | Parry | Absorb | Intercept | Other | Citation |
|---|---|---|---|---|---|---|
| PT01 | 1 (failed) | 3 | 2 (1 chosen deliberately to keep the action for magic; 1 **forced** at 1 Endurance in Aggressive) | 1 (2 End + Parry at 2 End = 4 of 5) | — | `playtest/01_thornwall_undercroft/session_log.md:271, :329, :476, :530-546, :644` |
| PT02 | 3 | 2 | 0 | 1 (free, from Withdrawn) | 1 Warding cast used *instead of* a reaction (:341-347); 1 Soul save (:679) | `playtest/02_silence_of_ashenmoor/session_log.md:278, :286, :335, :484, :494, :558-564` |
| PT06 scripted | 1 (cost 2 in Aggressive → "wiped out half her pool in one roll") | 3 | 1 | 1 (cost 1 in Defensive) | 4 invented "Steam Blast" saves | `session_log.md:80-84, :91-97, :179-182, :221-226, :167-176`; `retrospective_reviews.md:42` |
| PT06 agent log | 1 | — | — | 1 | Press once | `agent_playtest_log.md:57-67, :95-100, :104-113` |
| PT07 (invalid) | 4 (2 failed) | 4 (2 failed) | 1 forced ("low on Endurance, so you are forced to Absorb") → rescued by Intercept | 1 | — | `session_log_04.md:45-54, :69-76`; `_09.md:34-57`; `_15.md:40-54`; `_19.md:33-36`; `_20.md:43-53` |
| PT08 | 0 | 0 | 1 (the enemy attack simply lands "winded"; no reaction event) | 0 | — | `transcript.md:115`; `metrics.json:64-65` |
| Simulations | chosen by better modifier: "parry if parry_mod >= dodge_mod else dodge"; Absorb when unaffordable or when armored vs Tier 1 | | | not modelled as a choice | | `software/tools/combat_sim.py:395-414`; `run_pt04_live.py:334-337` |

Intercept is the single most-praised mechanic across the LLM reports: "The Intercept was a standout moment… mechanically expensive, narratively powerful" (`01/playtest_report.md:40`), "the most stressful decision I've made in a game" (:253), "one of the most mechanically satisfying loops I've played" (`06/retrospective_reviews.md:38`), "Guardian-Striker synergy" (`07/playtest_report.md:77, :92`).

### 3.4 Press usage

- PT01, PT02: never used (Press absent from both roll tables `01/session_log.md:781-815`, `02/session_log.md:845-880`).
- PT06 agent log: once, by the expert persona (`agent_playtest_log.md:95-100`); scripted PT06: never.
- PT03: Sparks "mostly Press/finish" (`results.md:151`) — driver policy, not a choice.
- PT08: explicitly declined — "I am spending a Spark rather than Pressing, because Press costs Endurance and Endurance is the exact thing I have none of. Which, for the record, is the system working" (`transcript.md:93`).
- Reckless Press was cut 2026-07-31 (6dbe6cd) without any playtest having used it.

### 3.5 Spark spend vs hoard

| Source | Available | Spent | Earned | Note | Citation |
|---|---|---|---|---|---|
| PT01 | 9 | **2** (both Mira, both on magic) | 0 mid-session, 2 post-session nominations | "Hoarding instinct… Unclear spending moments… No re-earn path in session" | `playtest/01_thornwall_undercroft/playtest_report.md:8, :121-128`; `session_log.md:750-760` |
| PT02 | 12 | 2 (both Morgan, both on the climactic Attune rolls) | 2 (1 MM award, 1 peer) | "Spark earning rate… feels low"; Morgan ended at 1 | `playtest/02_silence_of_ashenmoor/playtest_report.md:157-169` |
| PT03 | 9 | 6.6–6.7 mean (7 in the narrative seed) | — | policy-driven | `playtest/03_boss_stress_test/results.md:19, :51` |
| PT04 live ×5 | 9 + 2 nominations | mean **3.27/player** (10 in session 1) | 2 per session via Act Break Nomination | `player_like` policy spends whenever holding ≥2 (`run_pt04_live.py:318-331`) | `playtest/04_resource_tax/results.md:11-19, :44-47` |
| PT06 scripted | 12 | 6 (Sylvia 2, Pippa 3, Thorne 1) | — | "Toby forgets to spend a Spark" once (:109) | `session_log.md:102, :143, :175, :197, :204, :230` |
| PT06 agent log | 3 (Billy) | 0 then 1 | — | "hoarding paralysis… causing him to fail a basic spell" | `agent_playtest_log.md:43, :84-89, :126` |
| PT07 (invalid) | 12 | Serane in 06/08/10, Ilesse in 10/18, **four Sparks in one exchange** in 20 (two on Strikes, two on reactions) | — | | `session_log_06.md:23`, `_08.md:22`, `_10.md:21, :33`, `_18.md:21`, `_20.md:22-24, :43` |
| PT08 | 12 | 1 (Penny, on the Strike) | 2 (Toby for information-not-theory; Penny Graceful Fail) | | `metrics.json:12-13, :37-38, :46`; `transcript.md:62-64` |
| Sim Series 6 (superseded) | 9 | 6.6–8.8 vs Named/Boss; 0.2–1.4 vs Mooks | — | "Hoarding in playtests was a behavioral issue, not a mechanical one" | `research/simulation_log.md:294-319, :386` |
| Sim Series 7 G1 | 9 | 6.2 | — | | `simulation_log.md:435` |

DESIGN note: "Does the Spark economy actually cycle, or do Sparks hoard? (Playtest 01 found hoarding; nothing has re-checked it since.)" (`docs/DESIGN_agentic_playtests.md:268-270`). Since then, Sparks reset to 3 each session (9142c90, 2026-08-08) and the natural-12 rule was written partly "a reason to spend rather than hoard" (`docs/RESEARCH_fun_gap_analysis.md:72`) — neither has been played.

### 3.6 Maneuver and Support

- PT01: one Support (Mira, Charisma+Persuade → extra die for Kael, `session_log.md:285-293`); one Maneuver (Vessa Investigate → finds the ward-lantern link, `:492-498`), described as "seamless integration" (`playtest_report.md:262`).
- PT02: one Support (Casey Investigate → Easy for Morgan, `session_log.md:528-538`); one Maneuver (Rowan Athletics → weak point, `:657-663`).
- PT06, PT07, PT08: **zero** Maneuvers or Supports in any log.
- Simulations: not modelled — "PCs always Strike (non-combat PCs use raw Strength — underestimates Support/Maneuver contributions)" (`research/simulation_log.md:271, :390`); PT03 F7 "Combat magic is unmodelled… our boss-fight data systematically omits one-third of a standard party's real toolkit" (`playtest/03_boss_stress_test/results.md:169`).

### 3.7 Turtle / Withdrawn-stall

- Series 6 A5 (superseded): 15 Mooks, 98% win over 14.5 exchanges by Withdrawn cycling (`simulation_log.md:282, :287`).
- Series 10: under current rules the default party never goes uncontested; a forced all-Withdrawn party loses 100% in `clock` exchanges when a clock exists and stalls to the 20-exchange cap without one (`simulation_log.md:668-684`). MM1 now requires every Mook-only encounter to carry a clock or objective (`mm_manual/MM1_Encounters_and_Enemies.md:182`).
- At the (LLM) table, Withdrawn was chosen 3 times total across PT01/02/06 and always as recovery, never as a stall.

### 3.8 The spotlight problem (PT08)

"Four players, one fight, one participant — and it worked, because Penny did the arithmetic out loud beforehand and everybody trusted it. I do not know yet whether that is the system working or the system letting three people idle" (`08/transcript.md:118`; report F5 `:139-149`). `spotlight_spread` 0.60; Luke 0 actions, 0 rolls, 519 words (`metrics.json:19-27, :55`).

---

## 4. Peaks and memorable moments

### 4.1 Flagged as exciting / memorable

| Moment | Words used | Citation |
|---|---|---|
| Kael's Intercept at 4 of 5 Endurance to shield Mira | "standout moment", "the most stressful decision I've made in a game, and that's exactly what good design feels like", "Best moment… That's the kind of moment this system is built for" | `playtest/01_thornwall_undercroft/playtest_report.md:40, :253, :273`; `session_log.md:530-546` |
| Double sixes through the Guardian's forced re-roll | "the best moment of the session. The system created that moment"; "(Table erupts)" | `playtest_report.md:257`; `session_log.md:566-576` |
| Snake-eyes breaks the key in the lock | "unanimously praised… better than 'the door doesn't open'"; "(Table groans. Alex laughs.)" | `playtest_report.md:28`; `session_log.md:135-147` |
| Guardian phase change mid-fight | "raised stakes at the right moment"; "made the fight evolve" | `playtest_report.md:39`; `session_log.md:684` |
| Morgan's four-note counter-song shatters the Resonance | "the session highlight"; "I had the best session of my life… It felt like I solved a puzzle with a musical instrument… that Spark felt *decisive*" | `playtest/02_silence_of_ashenmoor/playtest_report.md:18, :38`; `session_log.md:721-735, :825` |
| First-timer Drew | "Can we play again next week?" | `session_log.md:827` |
| Rowan going Withdrawn so the caster could finish | "felt like actual tactics… genuine teamwork" | `session_log.md:817` |
| Pippa's slide under the Golem; Thorne jamming the valves with Resonance | "that slide under the legs was amazing! I love how fast combat resolves"; "The Spark system really saved me"; "Rolling 3d6 on a hard check and succeeding felt like a true movie moment" | `playtest/06_expert_novice_campaign/session_log.md:249-250`; `fun_and_consequence_review.md:12` |
| Defensive posture + Intercept | "brilliant. It makes playing a guardian actually feel active"; "Defensive posture felt amazing" | `playtest_report.md:24`; `fun_and_consequence_review.md:11` |
| PT08 refusals and self-correction | Sophia refuses the hook; Luke refuses Sophia; Penny "had a guess with a confident voice on it"; Toby refuses to act on theories — "Nobody was steered" | `playtest/08_npc_variance/subagent_session/report.md:32-45`; `transcript.md:12, :16, :23-24` |
| PT08 Graceful Fail earned on narration | "That is worth more to this table than a success would have been" | `transcript.md:63-64` |
| Wept's Fracture halted by the cradle-song (PT07, invalid dice) | "a beautiful narrative move" | `session_log_10.md:31-41` |

### 4.2 Flagged as flat / anticlimactic / rote

| Moment | Words used | Citation |
|---|---|---|
| PT01 Mook fight | "Mook Combat Is Fun but Mechanically Thin… the optimal strategy is always Aggressive… In a 2-exchange fight, Tier 1 conditions clear before they matter" | `playtest/01_thornwall_undercroft/playtest_report.md:135-141` |
| PT01 forward-looking worry | "Will it still feel tactical when I have 7-8 Endurance and multiple Techniques? Or will it just be 'I Strike, I Strike, I Strike' with occasional posture switches?" | `playtest_report.md:255` |
| PT02 Husk ambush | "no meaningful resource expenditure… Total Endurance spent: 2. Total Sparks spent: 0… a speed bump" | `playtest/02_silence_of_ashenmoor/playtest_report.md:100-111` |
| PT02 Warding vs Boss | "The successes were flavor rather than mechanically decisive"; "I felt its limits hard" | `playtest_report.md:127`; `session_log.md:823` |
| PT02 Boss bypassed | never used Cacophony, Phase Change, or the post-phase Husks — "the Boss design was never stress-tested" | `playtest_report.md:139-147` |
| PT02 Specialty never triggered | "mechanically available but narratively absent. That's an MM failure" | `session_log.md:819-821` |
| PT03 fun question | "Was it fun? Epic even in defeat? **Untestable as designed** — there is essentially no defeat to feel, and the flagship phase-change beat did not fire" (first run) | `playtest/03_boss_stress_test/results.md:153` |
| PT03 phase change (first run) | "When forced to occur (diagnostic), it arrived in the final exchange or two and changed nothing the party did" | `results.md:149` |
| PT06 TPK vignettes (invented hazard rules) | "It wasn't fun at all… I was just rolling saves to not die"; "I felt like an executioner, not a GM"; "Death felt accidental and cheap" | `playtest/06_expert_novice_campaign/fun_and_consequence_review.md:15-19` |
| PT06 lost sword on a 7-9 | "felt a bit harsh" | `playtest_report.md:36` |
| PT06 novice MM on a 6- | "nothing happens?" | `agent_playtest_log.md:52` |
| PT07 novice-MM social scenes | four Hard checks, four 6s, "You learn nothing"; "That was extremely punishing. We couldn't get a single success because of the Hard modifier" | `session_log_02.md:20-60`, `session_log_12.md:62` |
| PT07 Vanisher with no roll allowed | "You can't roll… You are left standing in the dark"; "extremely powerful if GMs don't allow creative player counters" | `session_log_15.md:57-61` |
| PT08 one-player fight | "one player fought that entire fight while three watched" | `subagent_session/report.md:139-141` |
| PT08 the "careful vs reckless resolved identically" test | Toby pre-registers: "If the answer to all three is a shrug, then the careful option and the reckless option resolved identically" — the MM answered with information, not a shrug | `transcript.md:27, :51-61` |

---

## 5. Boss fights

| Source | Boss | Length | Phase change | "Felt like a boss"? | Citation |
|---|---|---|---|---|---|
| PT01 | Archive Guardian (Named TR 8, v0.1 Endurance 6, Defensive Ward re-roll) | 3 exchanges | Yes — on first Staggered, all attacks Hard until the lantern was dealt with; the party's Maneuver + magic answered it | "That fight was GREAT… the phase change made the fight evolve… the Defensive Ward re-roll technique was annoying in the best way — it made me sweat even on good rolls" | `playtest/01_thornwall_undercroft/session_log.md:429, :462-470, :580-588, :684-688` |
| PT02 | The Resonance (Boss TR 14) | 2 exchanges, ended by lateral solution | **Never triggered** | Best abilities unseen; MM ruled the counter-song a "unique narrative action, not a standard scope table roll" | `playtest/02_silence_of_ashenmoor/session_log.md:624-626, :717`; `playtest_report.md:139-147` |
| PT03 pre-A14 | Iron Crucible (Resolve 10 + heavy armor) | mean 2.9, min 1 | fired **~0%** because the Boss spent its own Resolve to Parry | "the Crucible died Intact"; 99.7% party win | `playtest/03_boss_stress_test/results.md:63, :118, :131` |
| PT03 post-A14 | same | median 3, min 3 | fires **100%**, "landing around exchange 2 of a 3-exchange fight" | "survivable but expensive": Sparks ~2.2/player, Endurance ~1.7 left; win 99.3–100% "reported, not gated" | `results.md:16-24, :31-51` |
| PT06 scripted | Sentry Golem ("TR 9", Endurance 8, invented Armor 2) | 2 exchanges | "+1 damage" phase (invented); Steam Blast jammed by Resonance | "Wow, that was tense!" (under HP rules that do not exist) | `playtest/06_expert_novice_campaign/session_log.md:163, :212, :249` |
| PT06 live | Sentry Golem | 2 exchanges + finishing cast | MM narrated armor "permanently shattered" on a 6,6 | — | `live_unscripted_playtest_log.md:91-97, :140-146` |
| PT07 (invalid) | Wept TR 18, Radiant TR 12 ("narratively undefeatable"); Tavva TR 9 (Resolve 3) | 1 exchange each; Tavva to Resolve 0 in one exchange with 4 Sparks | none | Tavva "a clean, winnable combat sequence" | `playtest_report.md:52`; `session_log_20.md:22-58` |
| PT08 | Archive Guardian (Resolve 8, Reduced Mode at 2) | **never woke** — trigger was the vault door, nobody touched it | not exercised | "Boss severity… was not exercised" | `subagent_session/report.md:43-45, :180-182` |
| Sim Series 7 G1 | Guardian solo, Resolve 5→20 sweep | median 2.0 at Resolve 5–6, 3.0 at 8–12, 6.0 at 20 | riders modelled live | win **100%** at every value ≤17, 95.5% at Resolve 20; "an offense/action-economy problem, not a durability problem" | `research/simulation_log.md:402-418` |
| Sim Series 7 G1 re-run | Guardian Resolve 8 (TR 17) | median 3.0 across 7 seeds; Resolve 7 flips between 2 and 3 by seed | | win 100%, Sparks 6.2/9, Broken 0.03 | `simulation_log.md:426-441` |
| Sim Series 10 Part C | Guardian by-the-book with Open tag | **median 2** (floor of the 2–4 band); "a solo Boss is explicitly not an encounter (MM1)" | Reduced Mode never clears Open | flagged "for WS-5/playtest attention rather than retuned" | `simulation_log.md:686-702` |
| Sim Series 6 (superseded) | Boss TR 12/16 | 12.6–15.8 exchanges | on first Broken | "Boss fights feel right at Hard difficulty… long but not grindy"; 55–65% win | `simulation_log.md:308-319, :382` |

Related: `research/armored_enemy_breaking_problem.md:41-47` records the v0.2 infinite loop (armored Named NPC could never be Broken), dissolved by the Resolve model (:8-17).

---

## 6. Enemy differentiation

| Source | Enemies | Differentiated how | Citation |
|---|---|---|---|
| PT01 | Dust Constructs (Mooks) vs Archive Guardian | Guardian had a forced re-roll Technique (used 3×) and a phase change; Mooks "don't react, have no Endurance, and fall to any successful Strike" | `playtest/01_thornwall_undercroft/session_log.md:233, :462-470, :572, :632`; `playtest_report.md:137` |
| PT02 | Husks / Hollow / Resonance | Hollow: Silence Aura + Phase Shift (Strikes Hard unless magical); Resonance: Voice Weaponization (Soul save), Cacophony, Light Armor — only Voice Weaponization ever fired, once | `playtest/02_silence_of_ashenmoor/session_log.md:421, :624-626, :677` |
| PT03 | Iron Crucible | Forge Slam (two targets/exchange), Heat Surge (Con check or Winded), phase to atk +3 | `playtest/03_boss_stress_test/results.md:94-96, :47-49` |
| PT04 | Bandit Lieutenants ×3 + Captain | Captain "identical to Bandit Lieutenant… her distinction is narrative (she commands, she offers terms), not a hidden TR bonus" | `playtest/04_resource_tax/scenario.md:99-122` |
| PT06 | Sentinels / Golem / 9 vignette monsters | Golem: Steam Blast (invented Wisdom saves); vignettes: miasma, sonic scream, lava, webs, spores, steel armor, void drag, lightning, steam — all invented per-adventure hazards, most conflicting with the ruleset | `playtest/06_expert_novice_campaign/session_log.md:163-176`; `agentic_playtest_compendium.md:12, :35-39, :61, :84, :107, :129-130, :153, :177, :200` |
| PT07 (invalid) | Hollow / Wept / Radiant / Tavva / Gallery Knives | Tavva: Vanisher (dark-burst escape) — ruled unanswerable by the novice MM, counterable by the expert; Wept: Fracture (Sorrow) invoked by a cradle-song | `session_log_15.md:55-61`, `_20.md:42`, `_10.md:31-40` |
| PT08 | Dust Constructs | narrative only ("made of the room… came up like a sheet off a line"); they "lost interest the way water loses a shape" | `subagent_session/transcript.md:72-77, :120-126` |
| Simulations | `generic_named_def(tr)`, `generic_boss_def(tr)`, chickens | enemies are TR numbers; "per-enemy TR is a second-order knob"; enemies never react | `research/simulation_log.md:587, :607`; `playtest/03_boss_stress_test/results.md:166` |

Since the last playtest, MM1 gained three worked enemy Techniques and telegraphed finishers (8a28738, 2026-08-08) and enemy stances stated from conduct triggers (890f2d6). No table has used either.

---

## 7. Magic at the table

| Observation | Source | Citation |
|---|---|---|
| Five distinct effects from two domains, "none resembled 'I cast Fireball'"; "required MM collaboration" | PT01 | `playtest/01_thornwall_undercroft/playtest_report.md:52-62` |
| "brilliant and terrifying… the MM has enormous authority over how that's interpreted. I said 'flash of disorienting light' and Jamie ruled it as a combat effect that kills a Mook. Another MM might have said 'it flinches'" | PT01 (Sam) | `playtest_report.md:260` |
| Standard-domain pre-technique caster failed 2 of 3 (v0.1 penalty); "the one success… only happened because I spent a Spark" | PT01 (Riley) | `playtest_report.md:98-114, :269` |
| MM burden: "every 7-9 requires me to invent a complication on the spot, and the magic system requires me to adjudicate intent/scope in real time" | PT01 (Jamie) | `playtest_report.md:276` |
| After the penalty was removed: Warding 2/3, Resonance 5/6 successes; "The scope limitation (Minor only) was sufficient restriction" | PT02 | `playtest/02_silence_of_ashenmoor/playtest_report.md:47-53` |
| Minor wards vs a Boss: "flavor rather than mechanically decisive" | PT02 | `playtest_report.md:122-134` |
| The climactic counter-song required the MM to step outside the scope table entirely ("a unique narrative action") | PT02 | `session_log.md:717` |
| "explaining 'pre-technique' magic difficulty modifications was the biggest cognitive bottleneck of the session" | PT06 (Cyrus) | `playtest/06_expert_novice_campaign/playtest_report.md:21` |
| "novices struggle to conceptualize what they are allowed to do. They tend to ask 'Can I do X?' rather than declaring their intent" | PT06 | `playtest_report.md:51-52`; `retrospective_reviews.md:14` |
| "I was really worried about not having a spell list… It felt like I was 'cheating' by making up my own spells" | PT06 (Billy) | `retrospective_reviews.md:56` |
| "Can I cast a fireball?" / "there are no spell lists in this book? How do I know how much damage a fireball does?" | PT06 novice MM | `agent_playtest_log.md:28-30` |
| Server rejected a Significant-scope cast pre-Technique; player rescoped to Minor | PT06 live | `live_unscripted_playtest_log.md:129-143` |
| "Vibrating air? That's not a spell. You should just throw a rock"; Attune refused for listening | PT07 novice MM (invalid) | `session_log_05.md:36`, `session_log_13.md:19-21` |
| Magic failure rate 50% (5/10 casts) in the vignettes | PT06 batch | `playtest_batch_report.md:34` |
| Combat magic is unmodelled in every simulation | PT03 F7 | `playtest/03_boss_stress_test/results.md:169` |
| Casting curves now: pre-Technique Minor for a starting Focused caster (Zahna, +2) 91.8%; Broad Minor at +0 41.5% | Sim Series 11 | `research/simulation_log.md:736-757, :768` |
| No magic was cast in PT04 (scenario had none, `results.md:51`) or PT08 (no `cast` event) | | |

Fixes since: example intents per domain per scope (c0553ed; "Requested independently in three playtest documents", `docs/BRIEF_v0.3_ruleset_revision.md:101`; spell packages rejected there); MM2 "Adjudicating Magic" (ae2577c); casting adds the tradition's skill (41631ee). None played since.

---

## 8. Non-combat pillars

| Source | What social/exploration looked like mechanically | Rolls | Rich or thin? | Citation |
|---|---|---|---|---|
| PT01 | Insight on the patron (7 → "too prepared"), Lore, Investigate ×3, Attune, group Stealth, Persuade vs construct (failed), Insight on the vault (10) | 15 of 33 non-combat; Act I: 2 rolls in ~15 min | "I love the social system. Partial success on Insight gave me enough to be suspicious without solving the mystery" | `playtest/01_thornwall_undercroft/session_log.md:43, :83, :105, :117, :205-207, :401, :718`; `playtest_report.md:67, :267` |
| PT02 | Investigate (fail → new clue), Lore on maps, Attune on drawings, Wisdom on tunnels; one **no-roll Specialty** read | 6 of 32 | Investigation "smooth"; the social NPCs (Hale, Calder, Maren) carried no rolls | `playtest/02_silence_of_ashenmoor/session_log.md:49, :77, :121, :143, :175`; `playtest_report.md:41` |
| PT07 (invalid) | "Go around the room": exactly one check per player per scene, each a Persuade/Finesse/Strength "social check"; novice MM sets everything Hard and reads 7-9 as "-1 to your next roll" | 4 per scene | Novice MM: "You learn nothing" ×4; expert MM: every 7-9 becomes a debt, a doubled guard, a restricted movement | `session_log_02.md:16-60`, `_03.md:29`, `_07.md:28-53`, `_11.md`, `_16.md:27-62` |
| PT08 | Lore read of the maker's mark (10), a Watch challenge resolved **without a roll** off the Specialty, Attune with three pre-stated questions (12), a stealth approach (6 → Graceful Fail) | 3 of 4 | 81 callbacks; OOC:IC 0.76; four rules gaps; "it reads like a table" | `subagent_session/transcript.md:14, :19, :27, :39-40, :51-61`; `metrics.json:56-60`; `report.md:30-45` |
| PT08 scenario B (social-heavy, opt-in fight) | designed as the control arm | **never run** | — | `playtest/08_npc_variance/scenario.md:40-63`; `report.md:184` |
| Fun-gap analysis | "Social is the thinnest pillar" | — | item 5 (social 7-9 shapes) built 2026-08-13, unplayed | `docs/RESEARCH_fun_gap_analysis.md:176, :288-294` |

Reports of it feeling thin: PT01's Mook-fight critique is the only place a *scene type* was called mechanically thin, and it was combat. The social critiques on record are about the **novice MM**, not the rules — and the one social rules gap logged is "four of nine attributes carry exactly one skill" (`08/report.md:79-104`), which has no fix.

---

## 9. Advancement / growth feel

| Observation | Source | Citation |
|---|---|---|
| End of one session: 4 SP each; Vessa's Investigate went 1 mark → Practiced ("my second career advance!"); the MM "wouldn't dread advancement bookkeeping" | PT01 | `playtest/01_thornwall_undercroft/session_log.md:762-775`; `playtest_report.md:282` |
| End of session: one mark each into a used skill | PT02 | `playtest/02_silence_of_ashenmoor/session_log.md:785-804` |
| Forward-looking worry that Techniques and a larger pool turn combat into "I Strike, I Strike" | PT01 | `playtest_report.md:255` |
| PT05 verified the v0.3 formula: Facet level 1/2/3 at sessions 4/8/12 (100% SP efficiency) or 5/10/15 (80%); Tier 3 + Prismatic reachable at s12 — **pacing only, no play**; arena showcase never run | PT05 | `playtest/05_technique_showcase/results.md:10-17, :41-58` |
| That curve was then judged the defect: "every one of them arrives at the identical sheet… in roughly eleven sessions" → D16 rank caps and 3/5/8 mark curve; level 1 now lands at a 2.25-session floor | D16/D16a | `docs/DECISIONS.md:895-960` |
| PT06 is titled "campaign" but is one session plus nine one-exchange vignettes; **no advancement recorded** | PT06 | `playtest/06_expert_novice_campaign/PROGRESS.md`; `session_log.md:247-250` |
| PT07 pregens are Facet Level 1; twenty independent one-scene runs, no advancement | PT07 | `playtest/07_oraga_night_playtests/characters.md:10` |
| PT08 ended with "Advancement is open — four Skill Points each, only on skills you actually used tonight"; MM marked Insight for the no-roll challenge so the ruling would not cost the mark | PT08 | `subagent_session/transcript.md:153` |
| Superseded sim: "Advancement feels meaningful: Standard party at 55% vs Boss TR 12 → Advanced party at 88%" | Sim Series 6 E (v0.2) | `research/simulation_log.md:339-346` |
| Fun-gap item 4: "A session-one character has almost nothing distinctive… Worth a playtest before acting, specifically watching whether Body characters feel flat" | fun-gap analysis | `docs/RESEARCH_fun_gap_analysis.md:145, :301-304` |

**No playtest has ever advanced a character and played it again.** Techniques have never been used at a table by a PC (PT05's arena was not run; PT01's Guardian's Defensive Ward is the only Technique ever exercised, and it was an enemy's).

---

## 10. Issues raised and whether fixed

| # | Issue | Raised by | Status | Evidence |
|---|---|---|---|---|
| 1 | NPC posture → reaction difficulty unspecified | PT01 `playtest_report.md:81-84` | **Fixed** 1d9bbb1 (2026-03-14); later re-expressed as stated stances from conduct triggers 890f2d6 (2026-08-08) | memory + git |
| 2 | Absorb vs Named NPC — which tier? | PT01 `:86-89` | **Fixed** 1d9bbb1 (incoming tier Mook=T1, Named/Boss=T2); PT02 confirms "No confusion about who rolls what" `02/playtest_report.md:68-75` | |
| 3 | Armor + Parry downgrade stacking | PT01 `:91-94` | **Fixed** 1d9bbb1; encoded 8144e97 (2026-07-31) | |
| 4 | Pre-technique penalty too harsh for Standard/Broad | PT01 `:96-119` | **Fixed** 1d9bbb1 (penalty removed, Minor-only); PT02 validates `02/playtest_report.md:47-53`; Series 11 guards the number `simulation_log.md:750-757` | |
| 5 | Spark hoarding / no mid-session earn path | PT01 `:121-133`; PT02 `:154-169`; PT06 `agent_playtest_log.md:43` | **Partly addressed**: MM5/MM2 midpoint diagnostic (`mm_manual/MM5_Quick_Reference.md:96`, `MM2_Session_Design.md:831`); Act-Break Nomination (PT04 `results.md:44-47`); Sparks reset to 3/session 9142c90; natural-2 auto Graceful Fail 4551a71; app nudge a458abf. **Never re-tested at a table** (`DESIGN_agentic_playtests.md:268-270`) | |
| 6 | Mook combat mechanically thin; Aggressive always optimal | PT01 `:135-141` | **Addressed by doctrine**: "Skirmish encounters are tutorial encounters" `mm_manual/MM2_Session_Design.md:213`; "A Mook-only encounter must carry a clock or an objective" `MM1:182`; uncontested-exchange rule 15037bf. Whether Mook fights now *feel* less thin: untested | |
| 7 | Group rolls ad hoc | PT01 `:143-147` | **Fixed** 1d9bbb1; never used narratively in PT02 (`02/playtest_report.md:171-176`); group Stealth used in PT01 only | |
| 8 | 0-Endurance death spiral | PT01 `:238-240` | **Dissolved**: A6 retired the escalation (c0553ed); "0 Endurance = Absorb only, absolutely" 6d1e935; PT03: "Manageable, verging on irrelevant" `03/results.md:152` | |
| 9 | Tool: auto-suggest Conditions, Endurance display, Technique display, Spark prompt, enemy posture | PT01 `:204-214` | **Mostly fixed**: one-click Apply 62afb3a; enemy posture panel 4171fa1; Spark-flow nudge a458abf; front-end audit bb29200 (46 findings) | |
| 10 | Husk ambush too easy | PT02 `:97-111` | **Superseded** by Recipe Table (582c14b) and MM1:182 | |
| 11 | Specialty never triggered; MM should audit Specialties pre-session | PT02 `:113-120` | **Open** — no Specialty audit line in MM2 prep (grep of `mm_manual/MM2_Session_Design.md` finds Specialty only at :89). Related F3 "when no skill fits" fixed 62afb3a | |
| 12 | Minor wards weak vs Boss; guidance for pre-technique casters | PT02 `:122-134` | **Open/unverified** — no MM guidance located; casting now adds skill 41631ee | |
| 13 | Boss bypassed; lateral solutions "should feel earned" | PT02 `:136-152` | **Open** — no "lateral" guidance found in MM2 (grep); PT03 built to remove the bypass | |
| 14 | Boss phase change never validated | PT02 `:213`; PT03 scenario `:5` | **Fixed** A14 (c0553ed): phase fires 100% `03/results.md:20`; then Open tag (036557a) pulled the solo-boss median to 2 (`simulation_log.md:688-702`, "flagged for playtest attention") | |
| 15 | Enemy Parry self-depleting; enemy reaction cost unspecified | PT03 F5/F8 `:166-167` | **Fixed** A14: enemies never react | |
| 16 | "Hard ≈ 50% win" acceptance bar void | PT03 F0 `:161` | **Fixed** §5-quater: win rate reported, not gated | |
| 17 | Combat magic unmodelled in sims | PT03 F7 `:169` | **Open** — still true of every sim series | |
| 18 | `zulnut_def()` undercounts Finesse | PT03 F6 `:168` | **Open (minor)** per results | |
| 19 | Three-encounter session wins 0/5 live, 5.5% Monte Carlo | PT04 `results.md:13-21` | **Noted, not changed** — attributed to the driver never taking lateral options; Hard recipe kept at 47.5% (`simulation_log.md:615`) | |
| 20 | Aggressive posture too punishing without armor | PT06 `retrospective_reviews.md:42-45`, `playtest_batch_report.md:27-30`; PT07 `playtest_report.md:75-77` | **Fixed** K1 first-reaction-only (c0553ed; Series 8 `simulation_log.md:494-517`). "Armor ignores the surcharge once per combat" (`playtest_batch_report.md:47`) **not adopted** | |
| 21 | Pre-technique magic "VERY HIGH" risk, 50% fail | PT06 `playtest_batch_report.md:32-35` | **Superseded** — vignettes applied the removed −1 penalty; current Minor Focused at +2 = 91.8% (`simulation_log.md:768`) | |
| 22 | Environmental hazards + TR 9 boss = TPK | PT06 `playtest_batch_report.md:37-40`, `fun_and_consequence_review.md:15-28` | **Addressed** by Threat Clocks (`player_handbook/III.2_Adventuring.md:7-23`, c0553ed) — and the "damage every turn" rule never existed | |
| 23 | Doom Gate (death as a choice) | PT06 `fun_and_consequence_review.md:36-41` | **Not adopted as written**; endorsed in `docs/REVIEW_editorial_2026-07-10.md:74`; III.2 carries its own death rule (not audited here) | |
| 24 | Catch Breath (Withdrawn recovery) | PT06 `:51-54` | **Already existed** (Withdrawn recovers 2); now "up to the pool" 15037bf | |
| 25 | Spark refund on failed pre-technique cast | PT06 `:56-58` | **Implemented as an off-by-default variant** `software/facets/base/facet.yaml:1362`; never exercised (`04/results.md:51`) | |
| 26 | Common-intents reference per domain | PT06 `playtest_report.md:58-59`, `retrospective_reviews.md:17` | **Fixed** c0553ed (162 example intents, `docs/DESIGN_v0.3_ruleset_revision.md:389`); pre-set spell packages **rejected** (`BRIEF_v0.3_ruleset_revision.md:101`) | |
| 27 | Movement complications too harsh (lost weapon on 7-9) | PT06 `playtest_report.md:60-65` | **Addressed** by Trouble Table (c0553ed; canonical home d9f1363) and "7-9 names the cost before narrating" 58ef299 | |
| 28 | Novice MM says "nothing happens" on a 6- | PT06 `retrospective_reviews.md:28-31` | **Fixed** Trouble Table (d9f1363) | |
| 29 | Novice MM reverts to initiative / turn order | PT06 `:27`; PT07 `session_log_04.md:17-19` | **Open** — no worksheet/sidebar located; combat panel already sequences declare→reveal | |
| 30 | Thief escape techniques (Vanisher) need counter-play guidance | PT07 `playtest_report.md:83-91` | **Open** — no "escape technique" text in MM manual (grep); module-specific | |
| 31 | Guardian-Striker synergy sidebar | PT07 `:92` | **Unverified** — Intercept section exists (`player_handbook/III.3_Combat.md:235-243`); no synergy sidebar located | |
| 32 | Book forbids Finesse for unarmed Strikes; engine allows it | PT08 F1 `report.md:49-77` | **Fixed** 62afb3a (INV-8); then 377038c "Fixed skill-attribute pairs; the Strike is the named exception" | |
| 33 | Four of nine attributes carry exactly one skill (Con, Kno, Luck, Spirit); Luck "dead" for a Body character | PT08 F2 `:79-104, :246-249` | **Open — needs a design decision**; no mention in `docs/DECISIONS.md` or `TODO.md` (grep) | |
| 34 | Specialty has no behaviour when no skill fits | PT08 F3 `:106-119` | **Fixed** 62afb3a (II.5 "When no skill fits") | |
| 35 | Strike → enemy removal two-actor handshake | PT08 F4 `:121-137` | **Fixed** 62afb3a | |
| 36 | Spotlight metric counts only mechanics | PT08 F5 `:139-149` | **Noted** | |
| 37 | Playtest 07 numbers invalid; harness needed | DESIGN `:16-82` | **Fixed** harness (dc60dee, 62afb3a); **A/B batch (Arm B) never run** (`08/report.md:184, :251`) | |
| 38 | Armored enemies unbreakable (infinite loop) | `research/armored_enemy_breaking_problem.md:41-47` | **Dissolved** by Resolve model (:8-17), 2026-07-10 | |
| 39 | Encounter budget formula cannot express actor-count cliff | Series 9 `simulation_log.md:572` | **Fixed** 582c14b (tables cut; Recipe Table in MM1) | |
| 40 | Solo boss median 2 under Open tag | Series 10 `:694-702` | **Open — "flagged for WS-5/playtest attention"** | |
| 41 | Withdrawn-cycling exploit | Series 6 `:287` | **Dissolved** — clock/objective rule (Series 10 `:675-684`; MM1:182) | |
| 42 | Post-roll agency outside combat | fun-gap item 3 `RESEARCH_fun_gap_analysis.md:298-300` | **Open — needs owner ruling** | |
| 43 | Session-one Body characters may feel flat | fun-gap item 4 `:302-304` | **Open — "worth a playtest before acting"** | |

---

## 11. Evidence gaps

What has never been tested, in the order the audit question needs it:

1. **Real humans.** Zero human sessions. Every quoted player is an LLM persona; the only sessions with real (engine) dice *and* free agent choice are PT08 (one exchange, two beats) and PT04 (a script). The DESIGN doc's own limit: "Whether the game is enjoyable to humans is not measurable here" (`docs/DESIGN_agentic_playtests.md:378-384`).
2. **Any rule dated 2026-08-02 or later, at any table**: Open tag, uncontested exchanges, Withdrawn-to-pool, Sparks reset per session, enemy stances from triggers, enemy Techniques in MM1, casting adds skill, skill-point bank, Body-has-no-magic, D16 rank caps and 3/5/8 curve, **natural 12 / natural 2 / Borrowed Trouble**, social 7-9 shapes. The last play artifact is PT08 (2026-07-31). Only Series 10 (Open tag, uncontested rule) and Series 11 (casting curves) touch any of these, and only as Monte Carlo.
3. **Combat under the current ruleset with free agents.** PT08's one exchange was two Mooks; the Guardian never woke (`08/report.md:180-182`). PT03/PT04 are heuristic policies (`combat_sim.py:267-282, :395-414`; `run_pt04_live.py:292-337`) — they cannot say whether posture, reaction, Press, or Spark choices *feel* like choices. The only free-agent combat decisions on record under any version are PT01/PT02 (LLM fiction, v0.1/v0.2) and PT08's single Measured declaration.
4. **Fights longer than 4 exchanges under current rules.** None recorded outside Mook-swarm tails; every Boss median is 2–3. Whether a 2-exchange boss fight reads as "fast" or "flat" has not been asked of anyone.
5. **Minutes per fight / session share.** Never clocked; all figures are narrator estimates (`01/playtest_report.md:15, :35, :67-69`; `06/playtest_report.md:13, :20`).
6. **Techniques in a PC's hands.** PT05's arena "remains available for a later session" (`05/results.md:16-17`); PT01's worry about "I Strike, I Strike" at higher levels (`01/playtest_report.md:255`) is unanswered. Second Domain, Prismatic domains, Ascendant Domain: never cast.
7. **Advancement over more than one session.** No character has ever been advanced and then played. PT06's "campaign" is one session; PT07 is twenty disconnected scenes.
8. **Five-player tables.** Only Series D sims (`simulation_log.md:325-328`, superseded) — 5 PCs at 100%. PT02 is the only four-player fiction with posture variety claims (`02/playtest_report.md:27-34`).
9. **Social-heavy sessions under the validated harness.** Scenario B was designed as the control arm and never run (`08/scenario.md:40-63`; `08/report.md:184`). All social evidence is either LLM fiction (PT01/02/07) or two beats (PT08).
10. **Arm B (variable enemy severity) and the "do Bosses feel same-y?" question** — the A/B batch was never run (`08/report.md:184, :251`); pre-registered predictions (`DESIGN_agentic_playtests.md:249-262`) are untested.
11. **Spark cycling after the reset rule** (`DESIGN_agentic_playtests.md:268-270`), and whether the natural-12 incentive changes hoarding.
12. **Maneuver and Support** — used twice each in v0.1/v0.2 fiction, never since, never in sims (`simulation_log.md:271, :390`).
13. **Enemy differentiation as felt** — every current-rules fight uses `generic_named_def`-style enemies or Mooks; the three worked MM1 enemy Techniques (8a28738) have never been run.
14. **MM cognitive load measured** — PT01/PT06 assert "easier than D&D but harder than Fate" and "every 7-9 requires me to invent a complication" (`01/playtest_report.md:276`) without any instrument; rules-gap count exists only for PT08 (4 gaps in 2 beats, `metrics.json:60`).
15. **Fun-gap item 4** (Body characters flat in session one) is explicitly "worth a playtest before acting" (`docs/RESEARCH_fun_gap_analysis.md:302-304`).
16. **Losing.** No free-agent session has ended in a loss under current rules; PT03 found "there is essentially no defeat to feel" (`03/results.md:153`); PT04's five losses were scripted; PT06's TPKs used invented HP rules.

---

## Appendix — where the numbers for §2–§3 come from (roll-log ranges)

- PT01 roll table: `playtest/01_thornwall_undercroft/session_log.md:781-830` (33 rolls: 7 full / 17 partial / 9 fail; 2 Sparks; 3 re-rolls).
- PT02 roll table: `playtest/02_silence_of_ashenmoor/session_log.md:845-882` (32 rolls: 9 / 14 / 9).
- PT03 aggregate: `playtest/03_boss_stress_test/results.md:28-39` (post-A14), `:122-129` (pre-A14).
- PT04 aggregate: `playtest/04_resource_tax/results.md:9-42`.
- PT06 dice: `playtest/06_expert_novice_campaign/dice_rolls.txt`; batch: `playtest_batch_report.md:9-17` (51 rolls: 17.6% / 49.0% / 33.3%).
- PT07 (invalid): `playtest/07_oraga_night_playtests/dice_rolls.txt` (72 lines, identical totals in groups of four).
- PT08: `playtest/08_npc_variance/subagent_session/metrics.json`, `events.jsonl` (56 events).
- Simulation series index: Series 1–6 superseded (`research/simulation_log.md:5-17`); Series 7 `:394-475`; Series 8 `:479-519`; Series 9 `:523-622`; Series 10 `:626-714`; Series 11 `:718-779`.
