# DESIGN — Lean Facets v1.0 (first pass)

**Date:** 2026-09-25 · **Tier:** Planner (run on Opus 5.5)
**Implements:** `docs/BRIEF_lean_facets.md`, with every §9 recommendation adopted for the first pass (owner's `/goal`, 2026-09-25: *"implement a first pass of this, with a pin on the repo so we can revert if this fails to impress after building. Work it all the way through, from the documentation, to the app, to the module."*).
**Revert pin:** git tag `pre-lean-facets` (commit `b264318`). Work happens on branch `feat/lean-facets`.
**Source of truth for numbers:** `software/facets/base/facet.yaml` v1.0.0. This document explains it; where they disagree, the YAML wins and this document is the bug.

---

## 1. The rules in one page (what every artifact must agree with)

**Roll.** 2d6 + stat (+1 if one of your knacks applies; knacks never stack) ± difficulty (Easy +1, Standard 0, Hard −1, Very Hard −2). Stat + knack + talent bonuses never exceed +4. **10+** full success · **7–9** success with a cost · **6−** things go wrong, the story moves.
**Extra dice** (each: add a d6, keep the best two): a **Spark** (3 per session, no carry-over), **Help** (an ally's action; they share your cost), **Borrowed Trouble** (accept a complication that happens regardless; max one per roll). All stack.
**Naturals** (on the kept dice): 6+6 = full success whatever the modifiers, plus something more the player names. 1+1 on a failed roll = Graceful Fail auto-confirmed.
**Sparks** are earned by MM award, peer call, act-break nomination, and the Graceful Fail (narrate a 6− into something richer; MM confirms).
**Avoid** (the old saving throw): 2d6 + the stat that fits what is acting on you. 10+ avoid it, 7–9 the worst of it, 6− it takes hold.

**Character.** Facet (Body / Mind / Soul) → your Facet's stat **+2**, one other **+1**, the last **+0** (max +3; +1 to a stat at levels 4 and 8). **Class**: preset or custom — a name, a one-sentence concept, a **class knack**, two starting **talents** from the Facet menu, a starting **kit**, and at level 3 a **signature**. **Background**: a history, a **background knack**, and a **Specialty** (one narrow thing: routine or informational tasks inside it just happen; risky ones are Easy). **Lineage**: Human by default; a setting's gifted lineage adds a **gift knack** and may allow **Minor-only** workings in one domain. Casters are those who take **Thaumaturgy** (Mind) or **Invocation** (Soul).
**HP** = grit die max + Body at level 1 (Body d10, Soul d8, Mind d6); each level adds the die (or its average: 6 / 5 / 4), minimum 1. **Slots** = 10 + Body. **Sparks** = 3.

**Levels 1–10, called by the MM.** At session end the app shows five prompts (discovery · treasure · goal · change · moment); the MM calls level-ups. Default pacing: level 2 after session 1, level 3 after session 3, then every 2–3 sessions, level 10 near session 22. **Each level:** HP (die or average) + one pick: a new talent from your Facet menu (another Facet's needs a teacher found in play) **or** the improved form of a talent held at least one level. **Level 3:** the pick is your signature, and rebuilding stops being free. **Levels 4 and 8:** +1 stat. **Levels 5 and 9:** casters name another signature working. **Damage bonus:** +1 at level 3, +2 at 6, +3 at 9 on every damage roll.

**Combat, per exchange.** (1) The MM telegraphs what each foe is about to do and to whom. (2) Players say what they do, any order, and roll. **Attack:** 10+ deal weapon die and pick one (+1d6 damage · stunt · cover); 7–9 deal weapon die but you are **exposed** (if a foe can reach you, its next attack on you this exchange rolls an extra die, keep best two); 6− miss and the MM makes a move. (3) **Enemies roll in the open** (the app rolls): 2d6 + attack bonus; 10+ hard hit (damage +2), 7–9 hit, 6− miss; natural 12 = something more (MM names it), natural 2 = the target's next attack on it is Easy. Armor subtracts from damage (min 1). (4) The MM narrates. (5) Exchange effects expire.
**Defend:** no attack; attacks on you are Hard. **Intercept:** Defend, and attacks aimed at an ally within reach come to you. **Level gap:** your attacks on a foe 3+ levels above you are Hard, 6+ Very Hard. **Mooks** drop to any hit (7+) and attack as one mob (+1 damage per extra Mook, max +4). **Morale:** at a trigger (first to fall, half down, leader down, lone and hurt) the MM rolls 2d6; over the foe's morale it breaks (flees, surrenders, parleys). **Bloodied** (half HP): the card's WHEN BLOODIED line fires; Bosses change phase.
**Damage:** weapon die (unarmed d4 · light d6 · standard d8 · heavy d10 · ranged d8) + level damage bonus; armor light 1 / heavy 2 / shield +1, cap 3.

**0 HP.** Take a **Wound** (d6 table; it fills a slot; rolls that strain it are Hard) and roll **Hold On** (2d6 + Body): 10+ stand at 1 HP · 7–9 out of the fight, conscious · 6− dying: an ally who tends you before the scene ends saves you; otherwise the **death choice** (a heroic final action that succeeds, or live with a permanent Scar, d12 table).
**Recovery.** Breather (a few quiet minutes; in danger, the MM rolls the Pressure die): half max HP. Night's rest in safety: full HP, all Fatigue cleared, one Wound cleared.

**Magic.** Domain + Intent + Scope, cast with Mind (Thaumaturgy) or Soul (Invocation), +1 if a knack applies.
| Scope | Difficulty | Fatigue | From level | Harm |
|---|---|---|---|---|
| Minor | Standard | 0 | 1 | none — in a fight it is a stunt |
| Significant | Standard | 1 | 1 | 1d8 to one target |
| Major | Hard | 2 | 3 | 2d8 to a group |
Fatigue fills a slot; a night's rest clears it. No free slot, no full working. **Signature workings** (2 at creation, +1 at levels 5 and 9) are one step Easier. Heavy armor: +1 Fatigue per full working. Wider Domain: a second domain, one step Harder until improved. 7–9: it works; pick one of two costs the app offers from `magic_complications`. 6−: `magic_mishaps`, and the Graceful Fail applies. The v0.3 full-form rule survives: meaningful power or precision is never Minor; Minor never deals damage.

**Gear.** Items take 1 slot (heavy armor and heavy weapons 2); Wounds and Fatigue take slots; 100 coin per slot. **Usage die** (d8 → d6 → d4 → gone): roll after a scene of use; 1–2 steps it down. Curios (one-use, carry 3), relics (a power and a quirk; anyone may use one — a relic does not make its bearer a caster).

**Monsters.** Level 1–10 sets HP / damage / attack from `monsters.level_table`; role modifies (Mook, Standard, Elite ×2 HP two attacks, Boss ×5 HP two attacks +2 damage +1 attack and a Bloodied phase); armor 0–2; morale 2–12 (default 7, fearless 12). The card: WANTS · SPECIAL · WHEN BLOODIED · TELLS · BREAKS · TWISTS (d6) · NASTIER (optional).

---

## 2. Rulings adopted for the first pass (record in DECISIONS.md as L1–L14)

| # | Ruling | Supersedes |
|---|---|---|
| L1 | Overhaul proceeds; `pre-lean-facets` is the revert pin | — |
| L2 | Enemies roll their attacks in the open; NPCs still never roll against PCs outside combat | "NPCs never roll" (combat only) |
| L3 | HP and damage dice for PCs and foes | D26, Resolve, Conditions-as-HP |
| L4 | Three stats Body / Mind / Soul | nine Minor + three Major attributes |
| L5 | Magic limit is Fatigue in slots | D23 readied intents, D17 |
| L6 | Domain types replaced by signature workings; breadth is the Wider Domain talent | Focused/Standard/Prismatic, Ascendant Domain, Second Domain |
| L7 | Inventory slots unify gear, Wounds and Fatigue | armor budget, Endurance Pool, Tier-1 Conditions |
| L8 | Levels 1–10, MM-called with prompts; no skill list, no marks | skills, marks, Facet levels, D16 caps, Major Advancement, career advances |
| L9 | 12 presets, 4 per Facet (Warrior, Scout, Guardian, Brawler · Thaumaturge, Investigator, Physician, Tactician · Invoker, Speaker, Wanderer, Captain); custom classes from the same menus | Backgrounds-as-build, Techniques |
| L10 | Relics are usable by anyone and never make a Body character a caster; "Body has no magic" stands for characters | — |
| L11 | Scars table in (used by the death choice) | — |
| L12 | Generator tables ship setting-neutral; no new Shattered Origin names | — |
| L13 | Build on `feat/full-form-magic` (contains PR #30 and #31 canon); `fix/engine-housekeeping` is abandoned | — |
| L14 | A gifted lineage = a gift knack + optional Minor-only domain (the player's choice of domain, D24's spirit) | D18/D24 formalization mechanics |

Canon is untouched: Shattered Origin, the cast, Mordai's scar, Invocation/Thaumaturgy, Val'loh's tribes, Oraga Night's story. Only mechanics change.

---

## 3. File formats

### 3.1 `software/facets/base/facet.yaml` v1.0.0
As committed. Top-level keys: `stats, stat_rules, facets, talents, classes, roll_resolution, spark, advancement, hp, recovery, wounds, hold_on, death, slots, magic, combat, monsters, hazards, exploration, equipment, treasure, tables_file, lineages, backgrounds, magic_domains`.
A **setting Facet** (e.g. `software/facets/valloh/facet.yaml`) is additive only: it may add `lineages`, `talents`, `classes`, `backgrounds`, `equipment.items`, `magic_domains`, and tables; it may not change any number in the core sections (INV-17's spirit).

### 3.2 `software/facets/base/tables.yaml` (MM toolbox data; MM6 is generated from it)
```yaml
tables:
  - id: reaction            # unique
    name: "Reaction"
    die: "2d6"              # one of: 1d6, 1d8, 1d12, 1d20, 2d6, d66
    pillar: social          # fight | explore | social | magic | treasure | npc | oracle | body
    use: "When the party meets someone whose attitude the fiction hasn't fixed."
    entries:
      - {roll: "2-4", text: "Hostile. ..."}      # ranges "a-b" or single values; d66 uses "11".."66"
```
Every table's entries must cover every possible result of its die exactly once. Required ids (content owned by the MM agent):
`reaction` (2d6, five bands: 2–4 hostile, 5–6 wary, 7–9 uncertain, 10–11 open, 12 friendly) · `reaction_wants` (d66) · `pressure_generic` (1d6: encounter, sign, local hazard, cost, opportunity, quiet) · `pressure_underground`, `pressure_wild`, `pressure_settlement`, `pressure_occasion` (1d6 each) · `trouble` (1d6, the MM's index of moves) · `complications_fight`, `complications_explore`, `complications_social` (d66 each; one-line costs usable on a 7–9 or moves on a 6−) · `magic_complications` (1d12, 7–9 costs) · `magic_mishaps` (1d12, 6− results) · `wounds` (1d6) · `scars` (1d12) · `trinkets` (d66) · `curios` (1d20; each a one-use effect stated mechanically) · `relics` (1d20; power + quirk) · `npc_names` (d66, setting-neutral) · `npc_traits` (d66) · `npc_wants` (d66) · `npc_secrets` (1d20) · `oracle_actions` (d66) · `oracle_themes` (d66).

### 3.3 Character `.fof` v1.0
```yaml
fof_version: '1.0'
type: character
id: mordai
name: Mordai
ruleset: {modules: [{id: base, version: 1.0.0}]}
character:
  name: Mordai
  player_name: Mordai
  facet: body
  level: 1
  class: {id: warrior, name: Warrior, concept: "...", custom: false}
  stats: {body: 2, mind: 0, soul: 1}
  hp: {max: 16, current: 16}
  knacks: ["Soldiering", "City Watch"]         # class knack, background knack, (gift knack)
  specialty: "..."
  background: {id: city_watch_veteran, name: "City Watch Veteran", description: "..."}
  lineage: {id: human}
  talents: [{id: weapon_master, improved: false, choice: blades}, {id: tough, improved: false}]
  signature: null
  magic: null        # or {tradition: thaumaturgy, domains: [inscription], signature_workings: ["...", "..."]}
  inventory:
    - {id: standard_weapon, name: "Longsword", slots: 1, kind: blades}
    - {id: rations, name: "Rations", slots: 1, usage_die: 6}
  equipped: {weapon: standard_weapon, armor: heavy, shield: true}
  coin: 40
  fatigue: 0
  wounds: []         # [{name: "Cracked ribs"}]
  scars: []          # [{name: "..."}]
  sparks: 3
  talent_uses: {}    # {talent_id: uses_spent_this_scene_or_session}
  notes_player: ""
  notes_mm: ""
```
`hp.max` is stored but always recomputable (validator warns on mismatch). A **custom class** sets `class.custom: true` and supplies its own `name`, `concept`, and its class knack in `knacks[0]`.

### 3.4 Enemy `.fof` v1.0
```yaml
fof_version: '1.0'
type: enemy
id: city_watch_sergeant
name: City Watch Sergeant
ruleset: {modules: [{id: base, version: 1.0.0}]}
enemy:
  level: 3
  role: standard            # mook | standard | elite | boss
  armor: 1                  # 0-2
  morale: 8                 # 2-12
  weapon: "Cudgel"          # flavour only
  # optional overrides (use sparingly; the Bestiary prints a † when present):
  # hp: 20
  # damage: 5
  # attack: 2
  # attacks: 2
  wants: "..."
  special: "..."            # one gimmick, stated so the MM can run it
  when_bloodied: "..."
  tells: "..."
  breaks: "..."             # what it does when morale breaks
  twists: ["...", "...", "...", "...", "...", "..."]   # exactly six
  nastier: "..."            # optional
  description: "..."
  notes: "..."
  reskin_of: null           # a module reskin names its Bestiary original; numbers must match (INV-18)
```

### 3.5 Generated blocks (never hand-edited)
- **Bestiary** stat blocks inside `<!-- statblock: id -->…<!-- /statblock -->` in `bestiary/B*.md`, and `bestiary/Finding_Aids.md` (creatures sorted by level, then role), from `enemies/*.fof` via `python -m tools.build_bestiary`.
- **Adventure** `<!-- statline: id -->` blocks on scene cards and `<!-- pregen: slug -->` blocks, via `python -m tools.build_scene_cards`.
- **MM6** tables inside `<!-- table: id -->…<!-- /table -->` in `mm_manual/MM6_The_Toolbox.md`, via `python -m tools.build_toolbox` (new).
- `player_handbook/Index.md`, `List_of_Tables.md`, `List_of_Boxes.md` via `python tools/build_index.py` and `python tools/build_table_register.py`.

---

## 4. Software architecture

Keep: FastAPI app shell, auth (`app/auth`), session store and invites, `app/game/dice.py`, the three-tab SPA, threat clocks, the Spark economy code paths, facet discovery/loading.
Rewrite: `app/facets/schema.py` (Pydantic models for v1 YAML + tables), `app/facets/registry.py` (merge: talents, classes, backgrounds, lineages, items, domains, tables; additive-only setting Facets), `app/game/character.py`, `app/game/combat.py`, `app/game/engine.py`, `app/game/enemy.py`, `app/game/encounter.py` (no TR: a danger read from role counts vs party size/level), `app/game/session.py` (adapt), `app/api/websocket.py`, the REST routes, the static JS/CSS/HTML, `tools/combat_sim.py` (drives `combat.py` only), `tools/build_bestiary.py`, `tools/build_scene_cards.py`. New: `app/game/magic.py` (casting), `app/game/toolbox.py` (table rolls, reaction, morale, pressure, oracle), `tools/build_toolbox.py`.
Delete (preserved at the pin): `tools/agentic_playtest/`, `tools/run_9_playtests.py`, `tools/run_playtest_06.py`, `tools/run_unscripted_final.py`, and every test that exists only for a retired mechanic.

### 4.1 Engine responsibilities (pure functions, all ruleset-driven)
- `engine.resolve_roll(stat, knack, difficulty, sparks, help, borrowed_trouble, bonus)` → dice, kept, total, tier, naturals.
- `character`: create from preset / custom; validate; `hp_max`, `slots_total`, `slots_used`, `armor_value`, `weapon_die`, `damage_bonus`; `level_up(pick)` (talent / improve / signature / stat); `take_damage`, `hold_on`, `add_wound`, `breather`, `night_rest`; `add_fatigue`; sparks; talent use tracking; `to_fof` / `from_fof`.
- `combat`: `resolve_attack` (tier, damage, options, exposure), `resolve_enemy_attack` (roll, exposure die, defend/cover Hard, armor, naturals), `apply_damage_to_enemy` (Mook drop, bloodied crossing, defeat), `morale_check`, `level_gap_difficulty`, `mob_damage`.
- `magic.resolve_cast(scope, domain, signature, …)` → difficulty, Fatigue cost (heavy armor, Arcane Mastery, improved casting talents), damage roll for harm, complications to offer.
- `toolbox.roll_table(id)`, `reaction_roll()`, `pressure_roll(variant)`, `oracle(odds)`.

### 4.2 WebSocket events (client → server; the server broadcasts results)
Kept: `ping`, `roll` (general), `spend_spark`/`award_spark`/`peer_call`/`act_break`/`graceful_fail`, `chat`, `threat_clock_*`.
New/changed: `attack {target, weapon?, sparks, help, borrowed_trouble, option}` → `attack_result`; `choose_option {option}` (on a 10+); `enemy_attack {enemy, target}` (MM) → `enemy_attack_result`; `defend {intercept_for?}`; `cast {domain, scope, intent, signature?, target?}` → `cast_result`; `avoid {stat}`; `hold_on` → `hold_on_result`; `rest {kind: breather|night}`; `usage_roll {item}`; `wound_add/remove`; `level_up {character}` (MM) → `level_up_ready`; `level_pick {kind, id, choice?}` → `character_updated`; `enemy_spawn/update/remove` (MM; card-based); `morale_check {enemy}` (MM); `toolbox_roll {table}` (MM; private unless revealed); `reaction_roll`, `pressure_roll {variant}`, `oracle {odds}` (MM); `end_exchange`; `start_combat`/`end_combat`.

### 4.3 App (three tabs, vanilla JS)
- **Build**: a creation wizard — Facet → stats → preset class (default) or "write your own" → background (15 examples or custom) → knacks/Specialty → kit (tap items until slots fill) → magic (domain + two signature workings, if a caster). Monster-card builder for the MM (level + role → numbers; card fields). Level-up screen with the pick menu.
- **Play**: the character sheet (stats, HP bar, slots grid showing items/Wounds/Fatigue, knacks, talents with use trackers, magic panel), roll/attack/cast/defend controls, Sparks, chat. MM view: combat tracker (enemy HP, attack buttons that roll in the open, morale, bloodied flags), threat clocks, **Toolbox** panel (reaction, pressure die with terrain variants, complication tables, loot, NPC, oracle, and a **Stuck?** button offering three options), session-end level-up prompts.
- **Tools**: rules reference (from the ruleset), inventory, notes.

---

## 5. Documentation plan

**PHB** (`player_handbook/`), same house style (`style/STYLE_GUIDE.md` if present), vignettes with the recurring cast (`references/phb-examples.md`), sarcastic and light:
Front_Matter · Table_of_Contents · I_Introduction · Quick_Start · II.1 Character Creation Overview · **II.2 Stats** (replaces Attributes) · II.3 Magic · **II.4 Facets, Classes and Levels** · **II.4a/b/c** Body / Mind / Soul talent menus and presets · II.5 Lineage · **II.6 Backgrounds, Knacks and Specialties** · III.1 Core Resolution · III.2 Adventuring (exploration turns, Pressure die, hazards and clocks, rest, Wounds, Hold On, death) · III.3 Combat · IV.1 Equipment (slots, weapons, armor, gear, usage die, coin) · **IV.2 Treasure** (curios, relics, trinkets) · Appendix Character Sheet · Appendix Magic Domains · Glossary · generated Index / List of Tables / List of Boxes. **II.7 Skills is deleted.**
**MM Manual** (`mm_manual/`): MM1 Encounters and Enemies (monster cards, level table, roles, morale, reaction, building fights) · MM2 Session Design · MM3 Campaign Design (level pacing, prompts, name level, treasure) · MM4 Running the Table · MM5 Quick Reference · **MM6 The Toolbox** (procedures + generated tables).
**Bestiary**: 18 enemies migrated to cards; family prose updated; finding aids by level.
**Module**: Oraga Night (all chapters, 5 pregens, 10 enemies, scene cards) and the Val'loh setting Facet (book + YAML).
**Cast**: `characters/Zahna.fof` (Mind, Thaumaturge, domain Inscription, background knack *Guild Apprentice*; stats Mind 2, Soul 1, Body 0), `Mordai.fof` (Body, Warrior, *City Watch*; Body 2, Soul 1, Mind 0), `Zulnut.fof` (Body, **custom** class *Wandering Disciple* — Unarmored Discipline + Athlete, signature Ghost; Body 2, Soul 1, Mind 0).

---

## 6. Testing strategy

- TDD per CLAUDE.md: tests first for each engine function; ≥3 tests per public function (happy, edge, error).
- **Invariants carried over** (rewritten against v1): INV-3 glossary pointers, INV-4 index no-diff, INV-5/20 chapter references resolve, INV-6 MM5 dashes, INV-7 domain catalog = appendix, INV-9/10 numbered tables and registers, INV-11 no vague pointers, INV-12 capitalized terms defined, INV-13 box species, INV-15 Bestiary generated/complete, INV-16 lineage gifts resolve, INV-17 setting Facet additive, INV-18 reskins keep numbers, INV-19 statlines/pregens no-diff, INV-21 read-aloud length.
- **New invariants:** INV-22 every talent in `facet.yaml` has `use`, `text`, `normal` and appears in II.4a/b/c with a matching header; INV-23 every preset class's talents/kit resolve; INV-24 every table in `tables.yaml` covers its die exactly; INV-25 MM6 tables regenerate to no diff; INV-26 the books print the level table, the monster level table and weapon dice exactly as `facet.yaml` has them; INV-27 no retired v0.3 term survives in any book (Endurance Pool, Posture, Resolve, Technique, Facet level, skill point, mark, readied intent, Tier 1/2 Condition, Press, Maneuver, Strike as a rules term).
- **Simulation:** `tools/combat_sim.py` drives `combat.py`; a pacing test asserts the encounter ladder (4 Mooks trivial; mixed standard fights 2–4 exchanges; level-1 Boss dangerous) at levels 1, 5, 10.
- Full suite + e2e run before completion; report counts.

---

## 7. Work partition (parallel agents; disjoint files)

| Agent | Owns | Must not touch |
|---|---|---|
| **SW-core** | `software/app/facets/*`, `software/app/game/*`, `software/app/api/routes/*`, `software/tools/*.py` (not content), `software/tests/*` except `test_docs_consistency.py`, `software/facets/valloh/facet.yaml` (schema conversion only) | `facet.yaml` numbers (report issues), books, `.fof` content |
| **PHB** | `player_handbook/*` (not generated files' contents), `style/` read-only | software, other books |
| **MM** | `mm_manual/*`, `software/facets/base/tables.yaml` | software code, PHB |
| **Bestiary** | `bestiary/*.md` prose, `enemies/*.fof` | generated blocks (leave markers), software |
| **Module** | `adventures/oraga_night/**`, `settings/valloh/*.md`, `characters/*.fof`, `references/valloh/*`, `references/oraga_night/*` | software, core books |
| **APP** (after SW-core) | `software/app/api/websocket.py`, `software/app/static/**`, `software/tests/test_websocket.py`, `software/tests/e2e/**` | engine semantics (ask SW-core's code, don't fork rules) |
| **Integration** (me) | `software/tests/test_docs_consistency.py`, generators run, `docs/DECISIONS.md`, `docs/LOG_lean_facets.md`, `docs/TASKS_lean_facets.md`, CLAUDE.md/README touch-ups | — |

Every agent appends its progress to `docs/LOG_lean_facets.md` under its own heading and never edits another agent's section.
