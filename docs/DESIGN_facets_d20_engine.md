# DESIGN — Facets d20 rules engine and simulator

*Engine builder, 2026-09-28. Binds to `docs/DESIGN_facets_d20_v0_2.md` §1 (schema),
§1.4a, §6–§9 and the owner's rulings in `docs/BRIEF_facets_d20.md` Amendments 1–2 and
V21. This file records how the engine reads the rules, every decision the spec left
open, and what the Designer must change. Numbers live in
`docs/RESEARCH_facets_d20_sim.md`.*

## 0. Status

*Final run 2026-09-28: `python -m tools.d20_sim all --write` on the Amendment 2/3 track
chassis (§1.2 binding), V21 ability picks; tests 376 engine / 490 d20 / 1,586 full suite
(excluding e2e), all passing. Results: `docs/RESEARCH_facets_d20_sim.md`; the engine's PI
table replaced DESIGN v0.2 §8.1's harness table (P-18).*

- **Done and tested:** rules module (`combat.py`), loader/validator, character builder
  and legality checker, SRD monster ladder (61 SRD 5.2 monsters, CR 1/8–12), spell models
  from `sim_spells`, fight simulator with a documented AI, the adventuring-day runner,
  SRD baselines as engine builds, the Threat model and the encounter-table search, the
  §8 metrics (eDPR\*, eHP, PI, band verdicts, swap test), CLI, report and the yaml
  write-back of `encounter_table`, `encounter_adjustments`, `monster_threat`.
- **Bound to the Amendment 2 track chassis** (yaml `tracks:`, talents tagged
  `track: steel | spell`), read as described in §3. The balance matrix runs every preset
  and `sim_build` — pure caster, pure martial and hybrid for each Facet via
  `balance.roles` — plus the six SRD baselines, and checks band items 1–7.
- Q-2 is answered by DESIGN §1.2 (rank `main` flags, `facet_weight`); the engine reads
  the data, not an inference. Amendment 3: prismatic domains only through Deep Magic
  (final), and ranks lapse — the main track is recomputed from the talents held at every
  build (tests: a 2/2 Priest drops to the Half table; retraining back restores Full).

## 1. Layout

| Module | Job |
|---|---|
| `software/facets_d20/dice.py` | dice expressions, d20 with advantage/disadvantage |
| `software/facets_d20/combat.py` | **every combat rule, one function each**: attack roll, hit chance, crits, fixed monster damage (extra dice on crits), saves, minions, Evasion, `apply_damage` (temp HP, resistance, Bloodied, death, massive damage, drop-to-1, Undead Fortitude, concentration DC), concentration, morale and its triggers, side initiative, round order, turns per phase, `inflict` (boss resolve), `begin_turn`, `roll_recharge`, reactions, opportunity attacks, death saves, healing, the Spark die |
| `software/facets_d20/data.py` | loads both yaml v0.2 files (and the SRD baselines); an unknown effect type, condition keyword, expression term or sim-spell model is a `DataError` |
| `software/facets_d20/build.py` | `Picks` (preset, sim build or custom) → `Character` (HP, AC, attacks, DC, slots, lists, resources) → `CombatProfile`; `check()` lists every legality error; `build()` raises `BuildError` |
| `software/facets_d20/profile.py` | the combat profile (numbers and switches only) |
| `software/facets_d20/spells.py` | parses `sim_spells` (the yaml is the single source) |
| `software/facets_d20/monsters.py` | SRD ladder (`data/srd_monsters.yaml`), CR templates, MM-guide conversion |
| `software/facets_d20/sim.py` | fights, the tactical AI, the day runner, DPR-vs-dummy |
| `software/facets_d20/analysis.py` | continuous-CR foes, Threat model, calibration, budget search, validation, §8 metrics |
| `software/facets_d20/data/srd_baselines.yaml` | the six SRD 5.2.1 baselines in the effect vocabulary |
| `software/tools/build_srd_monsters.py` | regenerates the ladder from the SRD 5.2 creature data (Open5e `srd-2024`) |
| `software/tools/d20_sim.py` | CLI (`fight`, `encounters`, `balance`, `all`, `report`); drives the package only |

The simulator calls `combat.py` for every roll and rule; it only chooses actions.

## 2. How the engine reads the rules (decisions)

- **E-D1 Monster ladder from retrieved SRD data.** 61 SRD 5.2 monsters, CR 1/8–12, 2–5
  per CR, melee, ranged and casters, generated from the Open5e `srd-2024` data (the
  source `RESEARCH_facets_d20_srd_check.md` already used). Damage = the average the SRD
  prints ("13 (2d6 + 6) Slashing damage plus 3 (1d6) Fire damage" → 16); conditional
  riders ("if the attack roll had Advantage") are excluded. The Multiattack composition is
  curated in the tool and the SRD's Multiattack sentence is copied into the yaml.
- **E-D2 Morale "never"** for constructs, oozes, undead with Int ≤ 6 and plants with Int
  ≤ 3.
- **E-D3 Monster area sizes**: a 5-ft sphere catches 1 PC; cones and lines up to 30 ft,
  2; 40 ft and larger, 3.
- **E-D4 Sparks** (V15): +1d6 after a roll, spent only when it can turn the result (the
  roller's own first, else an ally's). Session Sparks and MM awards are roleplay and are
  not modelled; *Kindle* and *Turn the Odds* are.
- **E-D5 Smite spells count toward E1** and use the bonus action; *Hunter's Mark*
  (`per_hit`) is not a rider (Q-1).
- **E-D6 ASI (V21).** `Picks.asi = {4: {plus2: a} | {plus1: [a, b]} | {knack: id}}`,
  validated (one form, abilities ≤ 20, knack real and not a duplicate). Presets and sim
  builds default to **+2 on the primary ability** — the casting ability when Spell is
  the main track, otherwise the main weapon's (Dex for ranged, finesse with Dex > Str,
  or Martial Arts). So a Steel-main hybrid (Oathsworn, Tinker) raises its weapon ability.
  If +2 would pass 20 the overflow goes +1/+1 to the next-highest score. A preset may pin
  its picks with `asi:`. SRD baselines use `asi_rule: plus_two_primary`.
- **E-D7 `save_proficiency: choose`** takes the options in listed order (Iron Mind →
  Con). The Designer may pin with `abilities:`.
- **E-D8 Mage Armor** (`ac_set`, `precast`) is cast once a day when it beats the
  character's AC; it costs one 1st-level slot a day.
- **E-D9 Domains arrive with casting.** A preset's `domain` only counts from the level
  its casting talent is taken (a Steel Mind taking *Thaumaturgy* at 3rd has no domain at
  1st).
- **E-D10 Resources per fight.** A single fight gets ¼ of each long-rest pool (rounded
  up, plus any `short_rest_regain`) and all short-rest pools. The day runner carries HP,
  pools, Hit Dice and Sparks over four fights, short rests after the 1st and 3rd, pacing
  long-rest pools evenly (`ceil(left ÷ fights left)`); after a won fight a PC at 0 is
  patched up to 1 HP; Hit Dice are spent on a short rest while a die would not overheal.
- **E-D11a Generic foes.** For the budget search, a foe at a continuous CR takes its
  stats from a smooth fit over all 61 ladder monsters (log HP, log damage per turn, AC,
  to-hit and saves, each quadratic in log CR). The per-CR medians are not monotone (the
  CR 10 median hits softer than CR 9's) and extrapolated badly past CR 12 (a first run
  produced a "CR 30" foe with 42 HP and −24 to hit, which sent the six-player Battle
  budget to 3,700). Table 9–2 uses the same fit.
- **E-D11b HP lost** is measured against the HP the party starts the fight with, so the
  tired-party fit (50% HP) is like-for-like.
- **E-D11c Validation encounters** use real ladder monsters priced by their own Threat,
  with counts chosen to match the budget (one of the three closest fits drawn at random),
  so a class that misses its tier is the Threat model's miss, not a rounding error.
- **E-D11 Threat.** Lanchester square-law strength: standard √(HP × DPT); minion
  √(H × DPT) (a minion's durability is one hit whatever its CR); boss × B; never-breaks
  × N. H, B and N are **measured** by matching party HP lost at eight (level, CR) anchors
  and taking the median. Encounter Threat is the sum over foes.
- **E-D12 Budget search.** Per level and tier, bisection on the encounter's total
  Threat until the mean party HP lost hits the middle of the tier's band (Skirmish 10%,
  Clash 27.5%, Battle 45%; Desperate: 72.5% wins), averaged over three shapes (four
  standards; boss 60% + minions; two standards + minions) of continuous-CR generic foes
  (the SRD ladder's medians, log-interpolated). Rounds, wins and drops are measured at
  the fitted budget and reported, never fitted.
- **E-D13 Tier of an outcome** (validation and robustness): by mean party HP lost —
  Skirmish < 17.5%, Clash 17.5–35%, Battle 35–55%, Desperate above, or any fight whose
  win rate is 5 points under Battle's minimum.
- **E-D14 §8 metrics.** A build is measured over N standard days beside three
  reference-party companions (the reference party minus the build's own id).
  eDPR\* = (damage dealt, no overkill + healing restored to allies, no overheal +
  damage prevented *for allies*: Guardian's reduction, Clockwork Guard, Anticipate
  (expected), Turn the Odds flips, Warden-saved damage, disabled enemy turns × that
  enemy's expected damage) ÷ rounds. Self-protection is counted in eHP instead:
  eHP = (HP + temp HP per fight + self-healing per fight) × (0.55 ÷ measured hit rate on
  the build) × (printed damage per hit ÷ damage actually taken per hit). PI = eDPR\* × eHP.
- **E-D15 Adjustment parties.** Three players: Fighter, Wizard, Priest. Five: reference
  + Oathsworn. Six: + Druid. Tired: 50% HP and half the fight's resource share.

## 3. Amendment 2 (no paths) — how the engine reads tracks

Implements DESIGN v0.2 §1.2 steps 1–6 (binding, P-5 to P-14):

- **Depth** = the number of taken talents tagged with the track (any menu).
- **Main track** (`build.picks_main_track`) = Steel if depth.steel + weight.steel ≥
  depth.spell + weight.spell, else Spell; `tracks.facet_weight` gives Body +2 Steel (E3),
  so a Body build needs three Spell talents before Spell is main. Recomputed every level.
- **Ranks** (`build.track_ranks`) apply iff depth ≥ `rank.depth`, level ≥ `rank.level`,
  and (`rank.main` is false or the track is main). The `main` flag is read from data; the
  engine no longer hard-codes what a secondary track keeps.
- **Scaling** of a tracked talent at 5th/9th needs depth `tracks.scaling_depth[level]`
  in its track, counting every talent of the track, main or not.
- An effect with `facets: [...]` applies only to those Facets (Martial Training's die
  step skips Body).
- **Casting** comes from the highest applicable `casting` rank; tradition = the Facet's,
  or for Body the build's `tradition` (missing → legality error); ability = the Facet's
  `casting_ability` (`soul` = higher of Wis/Cha) or the tradition's.
- **Domains** = the applicable `domains` effects (ranks and talents); prismatic domains
  only up to the applicable `prismatic: true` grants (Deep Magic). A preset's
  `deep_domain` arrives with that rank; `extra_domains` by level; `kit_by_level` merges
  into the kit from its level on, and legality checks armor at that level.
- **Veteran**'s +2 weapon damage is a flat per-hit bonus (like Rage's), not a rider.

### 3a. Legacy paths and talent-borne casting

Kept only for the SRD baselines file, which models classes with `paths:
{martial, full, half}`. The Facets data has no paths and no talent-borne `casting`.

- `Picks.path` is optional. When the ruleset has no `paths`, a path in the picks is an
  error, `requires_path` is ignored, and nothing else reads it.
- Casting comes from any `casting` effect (`progression: full|half`, `tradition`,
  `ability`). Martial power comes from ordinary effects (`extra_attack`,
  `attack_bonus`, riders, `ac_formula`…). Two new effect types (**E-7**, below) carry
  what the path column used to: `armor_proficiency {categories: [...] | {facet: [...]}}`
  and `weapon_proficiency {categories: [...]}`.
- Facet/path `features` may carry `requires_talent: id` (a ladder feature that only
  applies once a talent is taken), so "casting power scales with talents invested" can be
  written as talent-gated ladders if the Designer wants.
- `one_tradition`, `cross_facet_talent_cap`, E1, E2 stay as `build_rules`.

## 4. Not simulated (listed in each profile's `notes`)

*Wild Shape* (the Druid fights as a caster), *Cunning* bonus-action mobility,
*Studied Recovery*, *Sculpt* (the sim never catches allies in areas), speed, prone from
*Anatomist*, *Master Plan*'s save half (attack half is modelled), knacks other than
*Field Medic*, summoning spells, *Shield of Faith* (never cast by the AI).

## 4a. Balance pass (Balance tuner, 2026-09-28)

Changes the balance pass made to the engine, each with rule tests in
`tests/test_facets_d20_engine.py`. Numbers and the tuning log:
`docs/RESEARCH_facets_d20_balance.md`; decisions V32–V41 in DESIGN v0.2 §12.

- **E-D16 Clockwork Guardian's 5-ft reach** (`sim.Fight.guard_step`). The construct acts
  right after its maker and steps beside one ally — the standing PC with the lowest share
  of its HP — and Guards only that ally, the first hit until the maker's next turn. The
  sim used to cut the first hit on *any* ally every round, which was the Tinker's +161%.
- **E-D17 Study on spell attacks.** Mind's Study gives "your next attack roll" advantage;
  the sim now applies it to a spell attack roll too, not only a weapon attack.
- **E-D18 The AI takes the higher expected value (S-5).** `Fight.attack_ev` counts what
  the Attack action really does (advantage from Study, a plan, a held or desperate target,
  reckless rage; the studied-target bonus; crit range; riders if any attack hits). An
  area spell, an aura (two rounds of it) or a disable (chance to fail × the foe's turn
  × two) is cast only when it beats that. Pure casters (no real weapon) behave as before;
  hybrids stop spending actions on low-DC spells.
- **E-D19 Every foe attacks a random standing PC** (DESIGN §6.2: the MM spreads the enemy
  side's attacks). Bosses used to pick the lowest-HP PC.
- **E-D20 Encounter method** (analysis only; no rule): minions in the fitting shapes are
  at most half the CR of a standard of the same budget (a few CR 13 "minions" at 7th level
  were deciding fights in two rounds); generic foes deal the SRD ladder's share of
  non-weapon damage (15%) as a separate strike, so resistances count as against real
  monsters.
- **E-D21 The swap test runs days.** `analysis.task_swap` plays the adventuring day
  (three Clashes, short rests between) so daily resources are paced as at the table; one
  seed per level for every build (common random numbers). It is the band's primary
  measure (V32); PI is secondary.
- **E-D22 Boss hit points** (`RuleOptions.boss_hp_multiplier = 2`, `monsters.convert`):
  a boss has twice its stat block's HP (V37).
- **E-D23 1st-level hit points** from `advancement.hp_first`: `hit_die_plus_con` (SRD,
  the baselines) or `hit_die_plus_eight_plus_con` (Facets d20, V35).
- **E-D24 New readings of existing vocabulary:** `damage_bonus` with
  `condition: [studied_target]` (Anatomist: + Int against your studied target, flat, not a
  rider) and `advantage` with `condition: [first_round, …]` and `rounds: N` (Master Plan
  holds for N rounds).
- **E-D25 The adventuring day is data** (`adventuring_day` in the yaml); a single fight
  gets 1/clashes of each long-rest pool (`sim.DEFAULT_SHARE = 1/3`).

**Answers.** Q-3 / E-9: the +2 at 4th and 8th goes to the ability the main track uses
(V33); every preset pins it (`asi:`) and a test holds the pins to the engine's rule.
E-9 (PI vs swap): the swap test is primary (V32). E-10 (targets pull apart): with the
minion cap, the day of three, 1st-level HP and boss HP the Clash lands at 3.0–3.7 rounds
at every level; Skirmish's rounds target became "about 2" (1.5–2.5) and Battle's wins
85–95%, the task's definitions (V41).

## 5. Questions and changes for the Designer

- **Q-2** Answered (DESIGN §1.2, P-5). Closed.
- **Q-3 V21 default for Steel-main hybrids (P-16 disagreement).** The engine raises the
  *main track's* ability (a Steel-main hybrid raises Str/Dex); the Designer's harness
  raises the casting ability for anything that casts. Only the Tinker and Oathsworn
  differ: engine Tinker L4 (27, 19, +6, DC 13, [3]) vs harness (27, 19, +5, DC 14, [3]);
  engine Oathsworn L4 (36, 18, +6, DC 12, [3]) vs harness (36, 18, +5, DC 13, [3]).
  The engine's reading follows "+2 on their primary attack or casting ability" by main
  track; if the Designer wants casting for every caster, set `asi:` on those two presets
  (or say so and the engine's default changes in one line).
- **Q-1** Are smite spells (`weapon_rider` without `per_hit`) riders under E1? The engine
  says yes (E-D5).
- **E-6** *Alert* uses `condition: [conscious]`; list `conscious` in §1.4a.
- **E-7** Done by the Designer (`armor_proficiency`, `weapon_proficiency` in §1.4).
- **E-8** `Precision`/`Sworn Strike` etc. use `frequency: once_per_turn`; the engine now
  enforces per-rider once-per-turn separately from E1 (needed for the SRD baselines, whose
  rider limit is unbounded).
- **E-9 PI vs the swap test disagree** (Spearman ≈ 0.7 at 1st level): PI multiplies a
  duelist's damage by its own toughness, so tanks and strikers rank high and healers low,
  while the swap test (party outcomes) ranks healers near the top. Recommend making the
  **swap test the band's primary measure** (party HP lost and rounds with the build in the
  reference party) and PI a diagnostic, or changing PI to eDPR\* + k·eHP.
- **E-10** The rounds targets and the HP-lost targets pull against each other at the
  ends of the range: a Skirmish that costs 10% HP is over in under two rounds, and
  Battle/Desperate fights run past five rounds at low levels (report §3). That is a rules
  signal for §7 ("the Planner changes a rule"), not something the table can fix.
- **E-11** `test_facets_d20_data.py` no longer carries its own legality helper: legality
  is checked through `facets_d20.build.check` (the audit's T1/T8). The v0.2 path-gate
  tests there ("needs steel") were dropped with Amendment 2.
