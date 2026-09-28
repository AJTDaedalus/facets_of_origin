# DESIGN — Facets d20 v0.2 (the simplified chassis)

*Planner output, 2026-09-28. Implements `docs/BRIEF_facets_d20.md` **Amendment 1**
(owner rulings 1–6) against the audit in `docs/AUDIT_facets_d20.md` and its three
sources, **revised for Amendment 2** (no Steel/Spell path: casting and martial power
are bought with the same talent picks). Supersedes `docs/DESIGN_facets_d20.md` §1–§4
wherever they conflict; v0.1's §6–§7 stay as the historical record. Data:
`facets_d20/data/facets_d20.yaml` and `facets_d20_spells.yaml`, both `version: 0.2`. The
chapter prose (`facets_d20/*.md`) is still v0.1 and is rewritten later from this file.*

**Status of this file.** §1 (Data schema) is the engine contract. The Amendment 2
revision (Designer, 2026-09-28) replaced the path sections with **tracks** (§1.2, §3),
re-measured §2, added §3.5 *Why this holds*, §5.1 *Prismatic domains — options for the
owner*, band item 7 and its first numbers in §8, and decisions V22–V31 in §12. The
engine work this needs is listed exactly in *Planner → engine*, P-5 onward, at the end.

---

## 1. Data schema (engine contract)

The engine reads two files. Everything a rule needs is a typed field; prose lives in
`summary` and is never parsed. **If the engine needs a field that isn't here, add it
here first, then to the yaml.**

### 1.1 `facets_d20.yaml` — top level

```yaml
version: 0.2
levels: {min: 1, max: 10}
proficiency_bonus: {1: 2, ..., 10: 4}
advancement:                      # what each level-up gives (ruling 1: ≤ 1 choice)
  talent_levels: [1, 3, 5, 7, 9]  # one talent pick at each
  knack_levels: [2, 6, 10]        # one knack pick at each (background gives one at 1st)
  asi_levels: [4, 8]
  asi_rule: choice                # V21: +2 to one, +1 to two, or one extra knack
build_rules:
  cross_facet_talent_cap: 2       # at most 2 of your 5 talents from other Facets' menus
  one_tradition: true             # a character casts from at most one tradition
  rider_limit_per_turn: 1         # exception E1
  controlled_creature_limit: 1    # exception E2
  max_hit_die: 12
tracks: {scaling_depth: ..., main_track: ..., facet_weight: ..., steel: {...}, spell: {...}}
facets: {body: {...}, mind: {...}, soul: {...}}
talents: [ ... ]                  # each tagged track: steel | spell | null
knacks: [ ... ]
backgrounds: [ ... ]
presets: [ ... ]
balance: {...}                    # §8, incl. roles and hybrid_rule
sim_builds: [ ... ]
```

There is no `paths` key and no `requires_path` field (Amendment 2, V22).

### 1.2 Facets and tracks

```yaml
facets:
  mind:
    name: Mind
    hit_die: 6                    # before Martial Training and Hardy
    saves: [int, wis]
    armor: [light]
    weapons: [simple]
    skill_picks: 2
    skills: [arcana, history, ...]
    tradition: thaumaturgy        # body: null (E3)
    casting_ability: int          # soul: soul (the higher of Wis/Cha); body: null
    features:                     # automatic, zero-choice ladder
      - {id: study, name: Study, level: 1, effects: [...]}
tracks:
  scaling_depth: {5: 2, 9: 3}     # a tracked talent's 5th-level scaling line needs depth 2 in
                                  # its track; its 9th-level line depth 3
  main_track: {rule: more_talents, tie: steel}
  facet_weight: {body: {steel: 2}}
  steel:
    ranks:
      - {id: martial_weapons, depth: 1, main: false, effects: [{type: weapon_proficiency, categories: [martial]}]}
      - {id: martial_training, depth: 1, main: true, effects: [
          {type: armor_proficiency, categories: {body: [], mind: [medium, shields], soul: [heavy]}},
          {type: hit_die_step, value: 1, facets: [mind, soul]}]}
      - {id: extra_attack, depth: 2, main: true, level: 5, effects: [{type: extra_attack, attacks: 2}]}
      - {id: veteran, depth: 3, main: true, effects: [{type: hp_per_level, value: 1},
                                                      {type: damage_bonus, value: 2, weapon: any}]}
  spell:
    ranks:
      - {id: spellcasting, depth: 1, main: false, effects: [{type: casting, progression: half}, {type: domains, count: 1}]}
      - {id: full_casting, depth: 2, main: true, effects: [{type: casting, progression: full}]}
      - {id: deep_magic, depth: 3, main: true, effects: [{type: domains, count: 1, prismatic: true}]}
```

**How the engine reads tracks (binding).** At character level L, over the talents taken
at levels ≤ L:

1. `depth[t]` = the number of taken talents whose `track` is `t` (any menu counts).
2. `main` = `steel` if `depth.steel + weight.steel ≥ depth.spell + weight.spell`, else
   `spell` (`weight` from `facet_weight[facet]`, default 0). Recomputed every level: a
   rank can lapse when the main track changes (V25).
3. A rank applies iff `depth[t] ≥ rank.depth`, `L ≥ rank.level` (default 1), and
   (`rank.main` is false or `main == t`). Its effects join the character's effects like a
   feature's. An effect with `facets: [...]` applies only to those Facets.
4. **Casting.** If any `casting` rank applies, the character casts: `progression` from the
   highest applicable casting rank (full replaces half); tradition = `facet.tradition`, or
   the build's `tradition` for Body (E3); ability = `facet.casting_ability`, or the
   tradition's (`facets_d20_spells.yaml` `traditions.<t>.ability`) for Body. Talents never
   carry `casting` effects.
5. **Domains.** The number of domains = the sum of applicable `domains` effects (ranks
   and talents, e.g. *Wider Study*). Prismatic domains are allowed only up to the count of
   applicable `domains` effects with `prismatic: true` (so only via *Deep Magic*).
6. **Upgrades.** For a talent with `track: t`, a `scaling` line at level N applies only if
   `L ≥ N` and, when N is a key of `scaling_depth`, `depth[t] ≥ scaling_depth[N]`.
   Untracked talents scale by level only. `by_level` inside a tracked talent's
   `resource` is not used: tracked growth lives in `scaling` so the gate covers it.

HP = `hit_die + Con` at 1st, then `hit_die/2 + 1 + Con` per level (fixed), with
`hit_die` = the Facet's die, one step per applicable `hit_die_step` (Martial Training,
*Hardy*), capped at `max_hit_die`, then `hp_per_level` (Veteran) added. Body's ladder
(Second Wind 1st, Action Surge 2nd, Indomitable 9th) sits in `facets.body.features`;
Extra Attack is no longer a Body feature: it is the Steel rank every martial reaches.

### 1.3 Talents and knacks

```yaml
- id: precision                     # snake_case, unique across talents+knacks
  name: Precision
  menus: [body, mind]               # printed once; listed on each menu
  track: steel                      # steel | spell | null (V22)
  requires: null                    # null | talent id — no talent uses one in v0.2
  basis: "SRD 5.2.1 Rogue: Sneak Attack"   # or "original"
  summary: One line of rules text for the card.
  effects:                          # active from the level you take it
    - {type: extra_damage_dice, dice: 1d6, rider: true, frequency: once_per_turn,
       weapon: [finesse, ranged], condition_any: [has_advantage, ally_adjacent_to_target, studied_target]}
  scaling:                          # effect changes at character level N (replace by id/type)
    5: [{type: extra_damage_dice, dice: 2d6, ...}]    # needs Steel depth 2 (tracks.scaling_depth)
    9: [{type: extra_damage_dice, dice: 3d6, ...}]    # needs Steel depth 3
```

Rules for `scaling`: at level N, every effect listed **replaces** the effect of the same
`type` (and same `id`, if given) from the base list; an effect whose type isn't in the
base list is **added**. Levels are character levels. For a tracked talent the depth gate
in §1.2 step 6 applies on top.

Knacks live in their own top-level `knacks:` list with `id`, `name`, `basis`, `summary`
and `effects` (no menus, track or scaling); they may only use the non-combat effect types
marked **(N)** below. A test enforces it. Facet `features` and track `ranks` use the
talent shape plus `level:` (and, for ranks, `depth:` and `main:`).

### 1.4 Effect vocabulary

Every effect is a map with a `type`. Expressions (`value`, `uses`, `dc`, `amount`) are an
integer or a string from this grammar: `pb`, `level`, `half_level` (round down),
`<ability>` (`str`…`cha`, meaning the modifier), `casting` (casting-ability modifier),
`soul` (casting modifier if Invocation, else the higher of Wis/Cha), sums joined with
`+` (e.g. `"8+pb+dex"`, `"1d10+level"`), and `min:N` as a separate key.

| type | fields | meaning |
|---|---|---|
| `hp_per_level` | value | +value max HP per character level (retroactive) |
| `hit_die_step` | value, facets | hit die one size larger per step (recalculate HP); `facets: [...]` limits it to those Facets (Martial Training) |
| `ac_formula` | base, add: [abilities], shield_allowed, condition: unarmored | alternative AC; use the higher |
| `ac_bonus` | value, condition | flat AC (condition: `armored`, `shield`, `adjacent_ally_aura`) |
| `attack_bonus` | value, weapon: [ranged\|melee\|any] | to attack rolls |
| `damage_bonus` | value, weapon, condition | flat, per hit (NOT a rider) |
| `extra_damage_dice` | dice, rider, frequency, weapon, condition, damage_type, resource | extra dice on a hit; `rider: true` counts toward the one-rider limit |
| `crit_range` | min, condition | crit on d20 ≥ min |
| `extra_attack` | attacks | Attack action makes this many attacks (no stacking) |
| `bonus_attack` | die, ability, condition, resource | one extra attack as a bonus action |
| `extra_action` | resource, forbid: [spell] | one extra action on your turn |
| `advantage` | roll: [attack\|save\|check\|initiative], scope, condition, resource | grants advantage |
| `impose_disadvantage` | roll, trigger, action: reaction, resource | enemy roll at disadvantage |
| `resistance` | damage_types, condition | halve those types |
| `damage_reduction` | amount, trigger, action: reaction, resource | reduce one hit by amount |
| `redirect_hit` | range_ft, reduce_by, action: reaction | take an adjacent ally's hit instead |
| `heal` | amount, action, range_ft, targets, resource | restore HP |
| `heal_pool` | size, action, per_use_min | pool of HP refilled on long rest |
| `heal_boost` | amount, trigger: slot_spell_heal, targets: 1 | extra HP when you heal with a slot spell as you cast it |
| `temp_hp` | amount, trigger, resource | temporary HP |
| `drop_to_one` | trigger: would_drop_to_0, condition, resource | stay at 1 HP instead |
| `reroll` | roll: failed_save, add, resource | THE one reroll mechanic |
| `save_proficiency` | abilities \| choose: N, from | |
| `save_bonus` | value, aura_ft, targets: [self, allies] | add value to saves |
| `condition_on_hit` | inflicts, save, dc, resource, frequency | e.g. inflicts: stunned until your next turn |
| `aoe_rider` | damage, targets: second_adjacent, weapon | damage to a second creature on a hit (not a rider) |
| `speed_bonus` | value, condition | |
| `spark` | grant, targets, action, resource / spend_on: [any_creature] | Spark rules (see §4) |
| `resource` | id, uses, recharge: short\|long, by_level: {lvl: uses} | declares a use pool other effects reference by `resource: id` |
| `casting` | progression: full\|half | only in `tracks.spell.ranks` (§1.2 step 4): makes you a caster; tradition and ability come from the Facet, or the build's `tradition` for Body. Never on a talent (V23) |
| `domains` | count, prismatic | domain(s) of your tradition (Spellcasting rank, *Wider Study*, Deep Magic); `prismatic: true` lets that domain be prismatic (§1.2 step 5) |
| `spells_known` | spells: [names], domain: any, max_level, free_cast: {uses, recharge} | a fixed spell or cantrip grant (Magic Initiate) |
| `wild_shape` | max_cr: {lvl: cr}, temp_hp, uses, keeps: [talents, facet_features], no_spells_until | beast form |
| `companion` | ac, hp, action: help\|guard, guard: {reduce: expr} | controlled creature (limit E2) |
| `surprise_immunity` | radius_ft | your side can't be surprised |
| `weapon_proficiency` | categories: [martial] | weapon training (Steel rank *Martial Weapons*; answers engine E-7) |
| `armor_proficiency` | categories: [..] or {facet: [..]} | armor training; the map form gives each Facet its own step (Steel rank *Martial Training*; E-7) |
| `skill_proficiency` **(N)** | choose, from | |
| `expertise` **(N)** | choose | doubled proficiency on two skills |
| `tool_proficiency` **(N)** | choose | |
| `languages` **(N)** | count | |
| `narrative` **(N)** | text | a non-numeric benefit the engine ignores and the sheet prints |

`condition` keywords the engine must understand: `advantage_or_ally_adjacent`,
`studied_target`, `raging`, `unarmored`, `armored`, `shield`, `no_shield`,
`one_handed_melee`, `heavy_or_versatile`, `ranged_weapon`, `bloodied`,
`first_round`, `attack_action`. Unknown keywords are a load error, not a silent pass.

#### 1.4a Additions used by the v0.2 yaml (Planner, 2026-09-28 — binding)

Written after the first yaml draft; the engine must accept all of these. Where an
Engine note (E-n, end of file) asked for something, the answer is here.

**Field name `roll`, not `on`.** YAML 1.1 (PyYAML) reads a bare `on:` key as boolean
`True`, so the roll a modifier applies to is `roll:` everywhere (`advantage`,
`impose_disadvantage`, `reroll`). Likewise the condition a hit inflicts is `inflicts:`,
so `condition` always means "when this applies".

**More expression terms.** `N*term` (e.g. `"5*level"`, `"2*level"`), `slot_level` (the
slot a spell was cast with), `half_level_round_up`, and dice terms inside sums
(`"1d10+level"`, `"2d8+casting"`, `"1d8+int"`). `min: N` sits beside the expression as
its own key (e.g. `{uses: soul, min: 1}`).

**More condition keys.** `condition` is **all-of**; a new key `condition_any: [...]` is
**any-of**. New keywords: `has_advantage` (this attack roll has advantage),
`ally_adjacent_to_target`, `not_moved` (you haven't moved this turn), `planned` (the
MM agrees a planning scene happened; the sim treats it as true once per short rest),
`oath_kept` (sim: always true), `conscious`. `advantage` may take `roll: [initiative]`
(scope `side_roll`: the side's single initiative roll has advantage — Alert). `evasion` may
take `applies: spell_saves` (Iron Mind: no damage on a successful save against a spell). `condition_target: [studied_target]` restricts the
creature an effect applies to.

**More effect types.**

| type | fields | meaning |
|---|---|---|
| `stance` | id, action, duration: fight, resource, forbid_armor | enter a named state (e.g. `raging`) that other effects' `condition` reads |
| `reckless` | condition | on your first attack of a turn you may: advantage on Str melee attacks this turn, and attacks against you have advantage until your next turn. **Answers E-2** (a type, not an `advantage` flag) |
| `forbid` | what: [spellcasting, concentration], condition | while the condition holds you can't do these |
| `martial_die` | die, ability, applies: [unarmed, simple_melee, light_melee], condition | weapon die floor and Dex option for those weapons |
| `bonus_attack` (extra fields) | count, weapon, resource, cost, replaces_free | Flurry: `count: 2` for `cost` focus, replacing the free one |
| `cunning_action` | options | Dash/Disengage/Hide as a bonus action (sim: Disengage after attacking when adjacent foes > 1) |
| `halve_damage` | action: reaction, trigger: hit_by_seen_attacker | Uncanny Dodge |
| `evasion` | — | Dex-save half effects: 0 on success, half on failure |
| `sculpt` | count | allies in your area spell auto-succeed and take nothing (sim: area spells never hit allies for this caster; others must place areas to avoid allies) |
| `maximize_spell` | resource | one damaging spell deals max on every die |
| `damage_bonus` (extra fields) | applies: spell, frequency: once_per_spell | + value to one damage roll of each damaging spell |
| `studied_target` | action, range_ft, duration, resource | marks the creature `studied_target` refers to |
| `slot_recovery` | amount, max_slot, trigger: short_rest, resource | Arcane Recovery |
| `initiative_bonus` | value | added to your side's single initiative roll when you roll it (§6.1) |
| `save_damage` | dice, add, save, dc: spell, half_on_success, damage_type, action, range_ft, resource, alternative_to | an at-will or resource-paid save-for-damage effect that isn't a spell; `alternative_to` names the effect it shares a use with |
| `heal` (extra fields) | trigger: on_crit | heal when the trigger fires |
| `condition_on_hit` (extra fields) | trigger: crit, cost, duration, condition_target | |
| `condition_immunity` | conditions | |
| `resource_refill` | resource, trigger | refill another pool when the trigger fires |
| `max_damage_next_hit` | trigger | your next hit this fight deals maximum damage |
| `spark` (fields) | grant, targets, range_ft, action, resource, trigger, frequency / spend_on: any_creature, subtract / floor, trigger: fight_start | Kindle, Prophecy, Turn the Odds (§5) |
| `temp_hp` (fields) | amount, trigger: fight_start, targets: {self: bool, allies: expr} | Field Kit |
| `companion` (fields) | ac, hp, speed, attacks: false, actions: [help, guard], guard: {reduce, hits, range_ft} | Clockwork Guardian; limited by E2 |
| `wild_shape` (fields) | max_cr, temp_hp, action, keeps, no_spells, flying, resource, sim_form | `sim_form` is the SRD 5.2.1 beast the sim uses (wolf, black_bear, dire_wolf — engine verifies against the SRD) |
| `hit_dice_bonus` **(N\*)** | amount, trigger: short_rest | extra HP per Hit Die spent on a short rest (Field Medic knack). The only knack effect the sim models; allowed in knacks because it's bounded by Hit Dice |
| `advantage` with `roll: [check]` only **(N)** | scope | a knack may grant advantage on ability checks, never attacks, saves or initiative |

An effect entry may carry `id:` to disambiguate two effects of the same type in
`scaling` (Sworn Strike's 9th-level `radiant_edge`), and `fallback: true` meaning
"applies only on a turn the other same-type effect wasn't used".

**Answers to the engine notes.** E-1: `sim_spells` in the spells yaml uses exactly the
engine's model names (`attack`, `save`, `auto`, `heal`, `aura`, `weapon_rider`,
`weapon_cantrip`, `disable`, `shield`, `buff_attack`). E-2: see `reckless` above.
E-3: accepted — the engine breaks ties by the order str, dex, con, int, wis, cha; the
book says "ties: you choose", and a preset may pin its choice with `asi_priority:
[abil, abil]`. E-4: accepted.

### 1.5 Backgrounds and presets

```yaml
backgrounds:
  - id: city_watch_veteran
    name: City Watch Veteran
    abilities: [str, con, wis]         # +1 to each; no split decision
    skills: [athletics, insight]
    tool: gaming_set                   # listed backgrounds only; a written one names none
    knack: streetwise                  # the 1st-level knack
presets:
  - id: priest
    name: Priest
    facet: soul
    domain: the_tide                   # arrives with the first Spell talent (engine E-D9)
    background: temple_acolyte
    abilities: {str: 13, dex: 10, con: 14, int: 9, wis: 16, cha: 13}   # final, background included
    skills: [medicine, persuasion]     # the Facet's two picks
    talents: {1: channel, 3: wider_study, 5: mending_hands, 7: warden, 9: hardy}
    extra_domains: {3: presence}       # {level taken: domain} for each Wider Study
    deep_domain: the_living_world      # Deep Magic's domain; arrives at Spell depth 3 (may be prismatic)
    knacks: {2: field_medic, 6: well_travelled, 10: silver_tongue}   # background knack is separate
    kit: {armor: scale_mail, shield: true, weapons: [mace], focus: holy_symbol}
    # optional: tradition: invocation|thaumaturgy   (Body builds that cast, E3)
    # optional: kit_by_level: {3: {armor: breastplate, shield: true}}  (dict-merged into kit from that level)
    # optional: cross: [talent ids from another Facet's menu] (≤ 2); asi: {4: {plus2: wis}}
sim_builds:                            # same shape as a preset, plus `audit:` and `role:`; or {id, audit, role, preset}
```

`role` is `pure_martial`, `pure_caster` or `hybrid` (Amendment 2); `balance.roles` lists
which builds fill each role per Facet (§8 item 7).

### 1.6 `facets_d20_spells.yaml`

```yaml
version: 0.2
traditions:
  thaumaturgy: {facet: mind, ability: [int]}
  invocation:  {facet: soul, ability: [soul]}      # soul = the higher of Wis and Cha
common_list:                    # every caster of either tradition casts these
  - {name: Fire Bolt, level: 0}
  ...
casting:
  known: all_on_lists           # no preparation: cast any spell on your lists of a level you have a slot for
  cantrips: all_on_lists
  domains_from: tracks          # domains come from `domains` effects (Spellcasting, Wider Study, Deep Magic)
  prismatic_from: deep_magic    # a prismatic domain only as Deep Magic's domain (§5.1, pending owner)
  domain_swap: retrain
full_table: {1: [2], ..., 10: [4, 3, 3, 3, 2]}   # by CHARACTER level
half_table: {1: [2], ..., 10: [4, 3, 2]}         # by CHARACTER level
domains:
  - id: the_tide
    name: The Tide
    tradition: invocation       # exactly one (canon); Divination is thaumaturgy
    prismatic: false
    role: support               # offense | control | support | utility (Table 7–5 tag)
    spells: [{name: Cure Wounds, level: 1}, ...]
sim_spells:                     # the subset the engine models mechanically (§9)
  - {name: Fireball, level: 3, model: save, dice: 8d6, save: dex, half_on_success: true, targets: 3, upcast: 1d6}
```

A spell appears on **either** `common_list` **or** domain lists, never both (a
domain-to-domain duplicate is fine and counts once). **No smite spell** (*Divine Smite*,
*Searing Smite*) is on any list (V24).

---

## 2. Simplicity budget (ruling 1), measured

**Counting method** (the goal-fit audit's, GF-M8, so v0.1 and v0.2 compare directly):
a *decision* is one pick a player makes; choosing N items from one list is N decisions;
writing a free-text line (name, Drive, Specialty) is one. Reading a card and accepting a
printed value is zero. An *exception rule* is a rule that makes one case behave
differently from the general rule it sits under (a carve-out a player has to remember),
not a talent's own trigger. Numbers below are for the **player book**; MM-only rules are
listed separately. "v0.2 paths" is this file before the Amendment 2 revision; "v0.2
tracks" is now.

### 2.1 Headline numbers

| Measure | Target (Amendment 1) | v0.1 | v0.2 paths | **v0.2 tracks** |
|---|---|---|---|---|
| Creation from a preset card | ≤ 12 | ≈ 20 (Priest card) | 6 | **6** |
| Creation, custom, listed background | ≤ 18 | ≈ 28–30 (Soul caster) | 14 caster · 13 Mind/Soul Steel · 12 Body | **13** caster · **12** non-caster · **14** Body casting from 1st |
| Creation, custom, written background | ≤ 18 | ≈ 33 | 18 (caster, worst case) | **17** caster · **16** non-caster · **18** Body casting from 1st |
| Choices at a level-up | ≤ 1 | 1 every level, **2 at 3rd**, plus sub-picks | ≤ 1 | **≤ 1** (a Spell talent that brings a domain names it as part of the pick; Body's first also names its tradition) |
| Choices over levels 2–10 | — | ≈ 12 | 10 (with V21) | **9 picks** (4 talents, 3 knacks, 2 ability picks) + 0–2 domain namings (Wider Study, Deep Magic) |
| Exception rules, player book | ≤ 5 | ≈ 15 (GF-M7) | 3 | **3** (§2.4) |
| Mechanics per job (add a die / grant advantage / reroll / weapon damage from a resource) | 1 / 1 / 1 / 1 | 3 / 3 currencies / 3 / 3 | 1 / 1 / 1 / 3 (*Sworn Strike*, *Divine Smite*, *Searing Smite*) | **1 / 1 / 1 / 1** (*Sworn Strike*; V24) |
| Chassis rules a player reads | — | classes-as-talent-chains, caster level, 3 caster carve-outs | a path choice, a 5-column path table, 4 path tags, "needs casting" | **a 3-column Facet table, a 7-rank depth table, one main-track sentence, one upgrade sentence; a [Steel]/[Spell] tag on each talent card** |
| Gates ("you can't take X") | 0 wanted | 3 carve-outs | 1 (the path) + 4 path tags | **0** |
| Talent entries a player reads | — | 57 talents + 18 signatures | 28 talents + 13 knacks; menus 10/13/12 | **26 talents + 13 knacks**; menus 10 / 13 / 12 |
| Spells a caster tracks | — | 2 domains (~26), prepare ~4–14 daily | Common (14) + 1 domain (~12); no preparation | Common (14) + 1 domain (~12); **+1 domain at Spell depth 3**; no preparation |
| Clocks a caster runs | — | 2 | 1 | **1** (character level) |

**Reading the change.** The revision removes one creation decision (the path) and every
gate, and costs reading: one table of seven ranks and two sentences replace the path
table and its tags. Decisions stay inside every cap. The main-track rule (§3.2) is new
reading a player must learn; it is a core rule, not an exception, because it applies the
same way to every character and both tracks.

### 2.2 Creation, decision by decision

| # | Step | v0.1 preset | v0.2 preset | v0.1 custom (Soul caster) | v0.2 paths custom | **v0.2 tracks custom** |
|---|---|---|---|---|---|---|
| 1 | Choose the card / concept | 1 | 1 | 1 | 1 | 1 |
| 2 | Name | (in 1) | (in 1) | (in 1) | (in 1) | (in 1) |
| 3 | Drives (want, line) | 2 | 2 | 2 | 2 | 2 |
| 4 | Facet | 0 | 0 | 1 | 1 | 1 |
| 5 | Path (Steel / Spell) | — | 0 | — | 1 | **— (removed)** |
| 6 | Casting ability | 0 | 0 | 1 | 0 | 0 (Soul = higher of Wis/Cha) |
| 7 | Domains | 0 | 0 | 2 | 1 | **1**, only if the 1st-level talent is a Spell talent |
| 8 | Background | 0 | 0 | 1 | 1 | 1 |
| 9 | Background ability split | 1 | 0 | 1 | 0 | 0 (+1/+1/+1 fixed) |
| 10 | Origin talent / knack | 0 | 0 | 1 | 0 | 0 (background's knack is fixed) |
| 11 | Specialty | 1 | 1 | 1 | 1 | 1 |
| 12 | Array placement | 1 | 0 | 1 | 1 | 1 |
| 13 | Facet skills | 3 | 0 | 3 | 2 | 2 |
| 14 | 1st-level talent | 0 | 0 | 2 | 1 | 1 |
| 15 | Cantrips | 2 | 0 | 2 | 0 | 0 (all on your lists) |
| 16 | Prepared spells | 4 | 0 | 4 | 0 | 0 (no preparation) |
| 17 | Kit | 3 | 0 | 3 | 1 | 1 (the kit for what your talents open, or 100 gp) |
| 18 | Languages | 2 | 1 | 2 | 1 | 1 |
| 19 | Keep the card's background or swap it | — | 1 | — | — | — |
| | **Total** | **≈ 20** | **6** | **≈ 28** | **14** | **13** |

A custom character whose 1st-level talent is not a Spell talent skips step 7 (**12**).
A Body character whose 1st-level talent is a cross-Facet Spell talent also names its
tradition (E3): **14**. A written background adds 3 abilities (1), 2 skills (2) and a
knack (1): **17** for a caster, **18** for the Body caster, the cap exactly.

### 2.3 Level-ups

| Level | v0.1 choices | v0.2 tracks choices | Automatic |
|---|---|---|---|
| 2 | talent | **knack** | Body *Action Surge*; Mind *Studied Recovery* (does nothing without slots) |
| 3 | talent + signature | **talent** | the ranks its track count reaches (§3.2) |
| 4 | talent | **ability pick** (V21) | |
| 5 | talent | **talent** | *Extra Attack* (Steel depth 2, Steel main); 3rd-level slots (Full) or 2nd (Half); tracked talents' 5th-level lines at depth 2 |
| 6 | talent | **knack** | |
| 7 | talent | **talent** | |
| 8 | talent | **ability pick** | |
| 9 | talent | **talent** | Body *Indomitable*; tracked talents' 9th-level lines at depth 3 |
| 10 | talent | **knack** | |

Talents grow on their own at 5th and 9th (their `scaling`, gated by depth for tracked
talents), so power keeps rising on levels with no talent pick. HP rises by a fixed amount
every level. A talent pick at 3rd, 5th, 7th or 9th can change the main track; the sheet
(and the app) shows, before the pick, which ranks it brings and which lapse (§3.2).

### 2.4 Exception rules

**Player book (v0.2 tracks): three.**

| # | Rule | Why it survives |
|---|---|---|
| E1 | **One rider a turn.** Extra damage dice that a talent adds to a hit (*Precision*, *Sworn Strike*, *Hunter's Mark* is not one: it is per hit and concentration) are **riders**; only one applies on a turn. | Replaces three v0.1 carve-outs with one rule, and caps every future rider talent. With smite spells gone (V24) E1 now only has to police talents. |
| E2 | **One controlled creature.** You control at most one summoned or conjured creature, companion or undead at a time; it acts right after you and deals fixed damage like a monster. | Summons and armies (audit M7) in one sentence. |
| E3 | **Body has no tradition of its own.** A Body character names Invocation or Thaumaturgy with its first Spell talent, and its Facet counts as two Steel talents when finding its main track — so it casts on the Half table. | Canon (Body has no magic tradition), and the Body chassis (d10, all armor, *Second Wind*, *Action Surge*) is a Steel investment already: without the weight a Body full caster measured +66–78% over the preset median at 9th–10th (§3.5). |

**Not exceptions** (they apply to everyone the same way): the main-track rule and the
upgrade-depth rule (§3.2); the cross-Facet cap of two; one tradition per character.

**Gone from v0.1's fifteen (GF-M7):** as in v0.2 paths, plus v0.2's own path gate and its
four `requires_path` tags (V22).

**MM book (not counted against the cap; MMs learn them once):** boss top-of-round turn;
a boss loses at most one turn a round to incapacitating effects; minions die to any damage;
mindless and bound foes never break. (§6)

### 2.5 One mechanic per job

| Job | v0.1 | v0.2 |
|---|---|---|
| Add a die after the roll | Spark help +1d6; *Inspiring Word* Heart die; *Well-Timed Word* subtracts | **The Spark die** (1d6, added — or subtracted with *Turn the Odds*). SRD spells (*Bless*, *Guidance*) stay as spells. |
| Roll twice, keep one | Spark for advantage; *Glimpses* (a second currency); plus SRD advantage | **Advantage/disadvantage** (SRD) only. Sparks never grant it; sources are ordinary triggers (Specialty, *Study*, *Marksman*, *Master Plan*, *Anticipate*, *Alert*). |
| Reroll | Spark reroll; *Twist of Fate*; *Indomitable* | **Indomitable** (Body, 9th) only. |
| Extra weapon damage bought with a resource | *Divine Smite*, *Searing Smite*, *Sworn Strike* | ***Sworn Strike*** only (a Steel talent). Slots never buy weapon damage (V24). |

Help (SRD action) stays: it is advantage, the one advantage mechanic.

---

## 3. The chassis

### 3.1 The Facets

| | Body | Mind | Soul |
|---|---|---|---|
| Hit die | d10 | d6 | d8 |
| Saves | Str, Con | Int, Wis | Wis, Cha |
| Armor | all, shields | light | light, medium, shields |
| Weapons | simple, martial | simple | simple |
| Tradition | none (E3) | Thaumaturgy (Int) | Invocation (the higher of Wis/Cha) |
| 1st-level feature | *Second Wind* | *Study* | *Kindle* |
| Automatic ladder | *Action Surge* 2nd · *Indomitable* 9th | *Studied Recovery* 2nd (if you have slots) | — |
| Skill picks | 2 of 8 | 2 of 8 | 2 of 10 |
| Main-track weight | Steel +2 (E3) | — | — |

The three dice and armor rows are the SRD's fighter, wizard and cleric. Everything else a
character becomes comes from its talents: *Martial Training* raises a Mind or Soul die one
size and *Hardy* one more (d12 at most).

### 3.2 Tracks: what the picks buy

Every talent is tagged **Steel** (weapons and armor), **Spell** (magic) or neither
(general). Your **depth** in a track is how many of your talents carry its tag. Your
**main track** is the one you hold more talents in; Steel wins a tie; a Body character
counts two extra Steel talents (E3).

| Depth | Steel | Spell |
|---|---|---|
| 1 — whatever your main track | **Martial weapons** | **Spellcasting**: your tradition, one domain plus the Common list, the **Half** table |
| 1 — Steel is main | **Martial Training**: one armor step (Mind: medium and shields; Soul: heavy) and, for Mind and Soul, a hit die one size larger | — |
| 2 — this track is main | **Extra Attack** (from 5th) | **Full** table |
| 3 — this track is main | **Veteran**: +1 HP per level, +2 damage on weapon hits | **Deep Magic**: one more domain, which may be prismatic (§5.1) |

**Upgrades.** A Steel or Spell talent's 5th-level line needs two talents of its track, and
its 9th-level line three. General talents grow by level alone.

That is the whole chassis. No talent is forbidden to anyone. The opportunity cost is the
point: every pick in one track is a pick not in the other, and only your main track grows
past its first rank.

**The shapes it produces** (5 talents by 9th):

| Shape | Steel · Spell · general | What it has at 9th | 5e analogue |
|---|---|---|---|
| Pure martial | 3+ · 0 · rest | armor step, Extra Attack, Veteran, every Steel talent's 9th-level line | fighter |
| Pure caster | 0 · 3+ · rest | Full table (14 slots, 5th-level spells), 3 domains incl. one prismatic, every Spell talent's 9th-level line | wizard, cleric |
| Paladin shape | 2 · 1 · 2 | Steel main: armor, Extra Attack, Half table (9 slots, 3rd-level spells), 1 domain; Steel talents' 5th-level lines | paladin, ranger |
| Artificer shape | 1 · 1 · 3 | tie → Steel main: armor step and die, Half table, no Extra Attack | artificer |
| Even hybrid | 2 · 2 · 1 | tie → Steel main: Extra Attack, armor, **Half** table; no depth-3 ranks, no 9th-level lines | paladin with a dip |
| Caster-leaning hybrid | 2 · 3 · 0 | Spell main: Full table and Deep Magic; its Steel side is martial weapons plus its two talents' own effects — no armor step, no Extra Attack | cleric/wizard who bought weapon talents |
| Caster with a Steel pick | 1 · 3 · 1 | Spell main: the Steel talent brings martial weapons and its own effect, nothing else | wizard with a weapon feat |

**Ranks can lapse.** The main track is recomputed whenever your talents change. A Battle
Priest with two Spell talents who takes a second Steel talent becomes Steel-main: it gains
Extra Attack and heavy armor and its slots fall to the Half table. That is the trade the
owner asked for, made visible at the moment of the pick; the sheet shows what a pick
brings and what lapses before it is taken, and the once-per-level retrain (§3.3) undoes a
regretted pick. The presets never flip.

**Why a majority, not a threshold.** With plain thresholds (two Spell talents = Full,
two Steel talents = Extra Attack) a 2/2 build had both masteries and heavy armor; the
engine measured it at +30–47% over the preset median at 9th–10th, above both pure Soul
builds (§3.5, V25). A path fixes that with a gate; the majority fixes it with the picks
themselves.

### 3.3 Talents, knacks, abilities

- **Talents** at 1st, 3rd, 5th, 7th and 9th (five in all). Each is broad and grows at 5th
  and 9th by itself (gated by depth, §3.2). No tiers, no prerequisite chains, no path tags.
- **Why five, still.** Five picks and depth thresholds of 1/2/3 make the budget bite:
  a pure build reaches depth 3 on its track with two picks to spare; a hybrid can have
  depth 2 in one track and 1–2 in the other, but never depth 3 in both, never both
  depth-2 ranks at once (the main track has them), and every talent under depth 3 keeps
  its 9th-level line locked. Six picks would let a 3/3 build keep every 9th-level line on
  both tracks; four would leave a pure build no general pick. Five also keeps knacks on
  the even levels and a level-up at one choice.
- **Cross-Facet:** at most **two** of your five talents may come from another Facet's
  menu. A talent printed on your own menu is never a cross pick. Cross picks count toward
  depth like any other.
- **Knacks** at 2nd, 6th and 10th, plus the background's at 1st: small, non-combat,
  from a list of 13 (§4.3).
- **Abilities:** standard array (or SRD point buy), then the background's **+1/+1/+1**.
  At 4th and 8th, **one simple pick** (V21): **+2 to one ability**, **or +1 to two
  abilities**, **or one extra knack**. Max 20.
- **HP:** hit die max + Con at 1st; then half the die + 1 + Con per level. Fixed.
- **Retraining:** once each level, after a long rest, swap one talent, knack or domain for
  another you qualify for. Never your Facet.
- **Signatures:** removed (as v0.2).

### 3.4 Background

Name, history (two or three sentences), **three abilities (+1 each)**, **two skills**,
**one tool** (listed backgrounds only), **one knack**, a **Specialty**. The eight v0.1
backgrounds keep their names and skills; their ability triples and knacks are in the yaml.
Specialty is unchanged (advantage when it applies; routine things inside it need no roll).

### 3.5 Why this holds — the opportunity cost in numbers

All figures are engine-built sheets (`software/facets_d20/build.py`) and simulator runs
(`sim.run_day`, 250 standard days of four Clashes per cell, the §8 method) of the builds
in the yaml, 2026-09-28 (Designer's measuring harness; the engine agent reruns them once
it implements §1.2 — P-5). PI is relative to the preset median at that level.

**Soul, the Facet with all three shapes on one menu:**

| 5th level | Priest (Spell 3) | Soul champion (Steel 3) | Oathsworn (Steel 2 · Spell 1) | Battle Priest (Spell 2 · Steel 1) |
|---|---|---|---|---|
| Slots (highest) | 9 (3rd) | 0 | 6 (2nd) | 9 (3rd) |
| Domains | 3, one prismatic | 0 | 1 | 2 |
| Extra Attack | no | yes | yes | no |
| HP / AC / die | 38 / 16 / d8 | 49 / 19 / d10 | 44 / 19 / d10 | 38 / 16 / d8 |
| Spell DC | 15 | — | 14 | 15 |
| Talent 5th-level lines | all | all | all | 1 of 2 (*Sworn Strike* stays 2d8) |
| DPR₁ / DPR₃ | 20.3 / 23.4 | 25.9 / 25.9 | 25.1 / 26.2 | 21.6 / 25.4 |

| 9th level | Priest (Spell 3) | Soul champion (Steel 3) | Battle Priest (2/2, Steel main) | Battle Priest, deep (Steel 2 · Spell 3, Spell main) |
|---|---|---|---|---|
| Slots (highest) | 14 (5th) | 0 | 9 (3rd) | 14 (5th) |
| Domains | 3, one prismatic | 0 | 2 | 3, one prismatic |
| Extra Attack | no | yes | yes | **lapsed** |
| HP / AC / die | 76 / 16 / d10 (*Hardy*) | 95 / 19 / d12 | 76 / 19 / d10 | 66 / 17 / d8 (armor step and die lapsed) |
| Talent lines active / locked | 4 / 0 | 7 / 0 | 5 / 3 | 4 / 2 |
| DPR₁ / DPR₃ | 36.7 / 65.2 | 32.2 / 32.2 | 31.0 / 32.5 | 35.5 / 62.1 |
| PI vs median | −6% | +1% | −13% | −11% |

**What a hybrid gives up, in numbers:**

- **At 5th**, the paladin-shaped hybrid (Steel 2 · Spell 1) against the pure caster:
  **one third of the slots** (6 against 9), **no 3rd-level spells** until 9th (no
  *Spirit Guardians*, no *Fireball*), **two fewer domains** and no prismatic one, and a
  spell DC one lower (its spare ability points went to Strength). Against the pure
  martial: **5 HP and 2 damage a hit** (Veteran) and, from 9th, *Sworn Strike*'s 4d8 and
  the heal on a crit — its Steel talents stop at their 5th-level lines.
- **At 9th**, the even hybrid (2/2) against the pure caster: **5 of 14 slots (36%)**, every
  4th- and 5th-level slot, one domain (the prismatic one) and **3 of its 8 talent lines**
  (*Channel* 3d8, *Sworn Strike* 4d8, *Weapon Expert*'s heal). Against the pure martial:
  **19 HP (20%)**, Veteran's +2 a hit, and the same three locked lines.
- **At 9th**, the caster-leaning hybrid (2/3) keeps the pure caster's slots and Deep
  Magic but **loses Extra Attack, the armor step and the hit die** it had at 5th–8th: it
  ends a Priest with two weapon talents, 10 HP and one domain line short of the real one.
- **The cheap dip is closed.** A Wizard who spends one pick on *Weapon Expert* gets
  martial weapons and +1 to hit — no armor, no hit die, because Spell is still its main
  track — and measures 5% *below* the Wizard at 9th (3,388 against 3,566). Before the
  main-track rule the same pick bought medium armor, a shield and d8, and that build ran
  +58–92% over the preset median from 5th on.
- **Body's chassis is priced.** Body casts on the Half table (E3); its best caster (two
  cross Spell talents) is −11–22% from 4th, against +66–78% at 9th–10th without the weight.

**Across every Facet** (full table in §8): from 4th level no hybrid's PI is more than
+13% over its Facet's better pure build (Soul at 4th: *paladin_max*), and at 9th–10th
every hybrid is at or below it; a Steel-main hybrid's single-target damage (DPR₁) is at or
below its Facet's best pure martial's, and a Spell-main hybrid's area damage (DPR₃) at or
below the best pure caster of its tradition's. The exception is the **Tinker** (Steel 1 · Spell 1): its PI runs +15–100% over
the best pure Mind build at 4th–7th while both its damage figures are 35–74% under — the
excess is *Clockwork Guardian* and *Field Kit* (support prevented and temp HP), a talent
tuning item for the balance pass, not the chassis.

---

## 4. Talents and knacks (ruling 5)

### 4.1 The menus

Shared talents are printed **once**, in one "Shared talents" section, and the menus list
their names (fixes ORG-1/ORG-2). **[St]** = Steel, **[Sp]** = Spell, untagged = general
(§3.2). No talent carries a path, Facet or casting requirement.

| Body (10) | Mind (13) | Soul (12) |
|---|---|---|
| *Alert* (all) | *Alert* (all) | *Alert* (all) |
| *Hardy* (all) | *Hardy* (all) | *Hardy* (all) |
| *Weapon Expert* [St] (all) | *Weapon Expert* [St] (all) | *Weapon Expert* [St] (all) |
| *Precision* [St] (Body, Mind) | *Precision* [St] (Body, Mind) | *Turn the Odds* [Sp] (Mind, Soul) |
| *Rage* [St] | *Turn the Odds* [Sp] (Mind, Soul) | *Wider Study* [Sp] (Mind, Soul) |
| *Martial Arts* [St] | *Wider Study* [Sp] (Mind, Soul) | *Channel* [Sp] |
| *Cunning* | *Evoker* [Sp] | *Wild Shape* [Sp] |
| *Guardian* [St] | *Clockwork Guardian* [Sp] | *Mending Hands* [Sp] |
| *Marksman* [St] | *Anatomist* [St] | *Prophecy* [Sp] |
| *Cleave* [St] | *Anticipate* | *Sworn Strike* [St] |
| | *Iron Mind* | *Warden* |
| | *Master Plan* | *Oath Unbroken* |
| | *Field Kit* | |

Track counts per menu — Body: 7 Steel, 0 Spell, 3 general; Mind: 3 Steel, 4 Spell, 6
general; Soul: 2 Steel, 6 Spell, 4 general. Every Facet can build a pure caster (Body only
through its two cross picks, E3), a pure martial (Soul through one cross pick) and any
hybrid. Rules text for each is the yaml `summary`; the mechanics are its
`effects`/`scaling`. Priest, Druid and Oracle are all Soul casters and differ by picks:
Priest = *Channel*, *Wider Study*, *Mending Hands* + The Tide; Druid = *Wild Shape*,
*Wider Study*, *Channel* + Verdance; Oracle = *Turn the Odds*, *Wider Study*, *Prophecy* +
Presence, with Fate as its Deep Magic domain at 5th.

**Tagging rule.** Steel = a talent about fighting with weapons or armor; Spell = a talent
that is magic (so *Turn the Odds*, *Prophecy*, *Wild Shape*, *Mending Hands* and
*Clockwork Guardian* are Spell: each makes you a caster if it is your first); general =
everything a caster and a warrior want alike (*Alert*, *Hardy*, *Cunning*, *Anticipate*,
*Iron Mind*, *Master Plan*, *Field Kit*, *Warden*, *Oath Unbroken*). *Hardy* and the other
general talents are what a pure build spends its two spare picks on.

### 4.2 Rewrites (ruling 5: concepts free, mechanics ours)

Every v0.1 talent the book audit (LIC-1) or this pass found mirroring a non-SRD feat or
subclass feature, and what replaced it.

| v0.1 | Resembled (non-SRD) | v0.2 | New mechanic |
|---|---|---|---|
| *Tough* | PHB *Tough* feat (+2 HP/level) | *Hardy* | Hit die one size larger (≈ +1 HP/level, bigger at 1st). DESIGN v0.1 L118's "Tough is in both" was wrong; corrected here. |
| *Deadeye* | *Sharpshooter* | *Marksman* | SRD *Steady Aim* (advantage, don't move) + SRD Archery (+2, at 5th) + ranged crit 19–20 at 9th. No cover-ignoring, no long-range clause. |
| *Bulwark* | *Sentinel* | *Guardian* | Reaction: take an adjacent ally's hit yourself, reduced by your level (2× from 9th). No speed-0, no reach punishment. |
| *Cleaving Blow* | *Great Weapon Master* | *Cleave* | On a heavy/versatile melee hit, a second adjacent foe takes Str (Str + PB from 5th) damage, no roll. From the SRD 5.2.1 Cleave *mastery idea*; no bonus attack on kill or crit. |
| *Field Medic* | *Healer* feat | *Field Medic* **knack** | Bonus-action stabilize; on a short rest each Hit Die a tended creature spends restores + PB. Needs Hit Dice; no free heals. |
| *Ambush* | Assassin's *Assassinate* | cut | First-round edge lives in *Master Plan* (advantage for the whole party after a planning scene; original). |
| *Beast Heart* | Circle of the Moon | cut | *Wild Shape* is the SRD druid's CR ladder (1/4 → 1/2 at 5th → 1 at 9th), temp HP = level. |
| *Infuse Item* | Artificer infusions | *Field Kit* | Fight-start temporary HP (= level) for you and PB allies. No +1 items, no stored spells. |
| *Clockwork Companion* | Artificer Steel Defender | *Clockwork Guardian* | A construct that never attacks: it Helps (advantage) or Guards (first hit on an adjacent ally loses 1d8 + Int). Under E2. |
| *Fighting Style* (*Dueling*, *Protection*) | SRD **5.1** styles, not in 5.2.1 | *Weapon Expert* | Uses only 5.2.1's Archery/Defense numbers (+1 attack, +1 AC armored), then SRD Champion crit 19–20 (5th), heal on crit (9th, original). |
| *Alert* (v0.1 "can't be surprised") | 2014 PHB *Alert* | *Alert* | Your side's single initiative roll has advantage. Original; no surprise immunity anywhere. |
| *Iron Mind* (save proficiency) | *Resilient* feat | *Iron Mind* | Advantage vs charm/fear; no damage on a successful save vs a spell (5th); advantage on Int/Wis/Cha saves (9th). |
| *Linguist* (knack draft) | PHB *Linguist* feat | *Well-Travelled* | Two languages + find a translator in any settlement. |
| *Many Faces* (knack draft) | PHB *Actor* feat | *Many Faces* | Disguise holds to a casual look with no roll (the Specialty idea applied to disguise). |
| *Survivor*, *Arcane Mastery*, *Contingency Plan*, *Still Water*, *Fury*, *Wild Heart*, *Seen It Coming*, *Rallying Cry*, *Unbreakable Will*, *Encyclopedic* (sig.) | SRD high-level features, or fine | cut / folded | Cut for load or balance (audit M3: *Survivor*); *Encyclopedic* became a knack; *Unbreakable Will* folded into *Warden* (9th). |
| *Glimpses*, *Twist of Fate*, *Well-Timed Word*, *Inspiring Word* | original, but three "add/subtract/reroll" currencies | *Turn the Odds*, *Kindle* | Folded into the Spark die (§2.5). |
| *Martial Training*, *Extra Attack* (talent), *Magic Initiate*, *Ability Score Improvement*, *Expertise* (talent), *Skilled* (talent) | — | track ranks / V21 pick / knack | Martial training and Extra Attack are Steel ranks (§3.2); the ability pick is V21; *Expertise* and *Skilled* are knacks; *Magic Initiate* cut (the first Spell talent does its job). |
| *Thaumaturgy*, *Invocation* (v0.2-paths half-caster talents) | — | cut (V23) | The Spellcasting rank: any first Spell talent makes you a Half caster. |
| *Divine Smite*, *Searing Smite* (SRD spells on Presence, Fire) | — | off the lists (V24) | *Sworn Strike* is the one resource-paid weapon rider. |

Kept with SRD 5.2.1 basis (named in each yaml `basis`): *Precision* (Sneak Attack, smaller
dice), *Rage* (+ Reckless, Unarmored Defense, simplified Relentless), *Martial Arts* (+
Focus, Stunning Strike), *Cunning* (Cunning Action, Uncanny Dodge, Evasion), *Evoker*
(Sculpt, Empowered Evocation), *Channel* (Divine Spark + Disciple of Life), *Wild Shape*,
*Mending Hands* (Lay On Hands), *Warden* (Aura of Protection, earlier and smaller),
*Second Wind*, *Action Surge*, *Indomitable*, *Studied Recovery* (Arcane Recovery),
*Expertise*, *Skilled*. Original: *Hardy*, *Guardian*, *Cleave* (reworked), *Anatomist*,
*Anticipate*, *Iron Mind*, *Master Plan*, *Clockwork Guardian*, *Field Kit*, *Turn the
Odds*, *Prophecy*, *Oath Unbroken*, *Sworn Strike*, *Study*, *Kindle*, and all knacks
except *Expertise* and *Skilled*.

### 4.3 Knacks

*Expertise*, *Skilled*, *Silver Tongue*, *Wild Kin*, *Field Medic*, *Gadgeteer*,
*Encyclopedic*, *Well-Travelled*, *Streetwise*, *Performer*, *Pathfinder*, *Artisan*,
*Many Faces*. Rule: **a knack never changes attack rolls, damage, AC, HP, saves,
initiative or spell slots** (enforced by test via the (N) types). *Field Medic* is the one
knack the simulator sees (between-fight healing, bounded by Hit Dice). *Silver Tongue*
now works once per NPC per scene (audit m16).

---

## 5. Magic (ruling 4)

- **Two traditions, canon names:** **Thaumaturgy** (Mind, Intelligence, scholarly) and
  **Invocation** (Soul, the higher of Wisdom and Charisma, intuitive). Body has none; a
  Body character names one with its first Spell talent (E3). One tradition per character.
- **Casting comes from Spell talents** (§3.2): the first makes you a caster on the
  **Half** table; a second, with Spell your main track, moves you to the **Full** table;
  a third gives **Deep Magic**. SRD full / half tables, **by character level**. No caster
  level, no separate half-caster talents (V23).
- **Lists:** every caster has the **Common list** and **one domain** of their tradition;
  *Wider Study* adds a domain, Deep Magic another. **You can cast any spell on your lists
  of a level you have a slot for; you know every cantrip on them.** No preparation, no
  cantrip picks. Rituals: any list spell with the ritual tag.
- **The Common list** (15 SRD 5.2.1 spells, both traditions): *Fire Bolt*, *Light*,
  *Message*; *Burning Hands*, *Magic Missile*, *Thunderwave*, *Detect Magic*, *Mage Armor*
  (balance pass V36, moved from Constructed Force);
  *Scorching Ray*, *Shatter*; *Fireball*, *Lightning Bolt*, *Dispel Magic*; *Ice Storm*;
  *Cone of Cold*. Area damage at every spell level for both traditions; the wizard-shaped
  Mind caster casts *Fireball*. A spell on the Common list is on no domain list.
- **Domains** are flavour and specialty: the 21 canon domains, each with one tradition
  (canon), a role tag (offense / control / support / utility) for Table 7–5, and its v0.1
  SRD list minus the Common spells. With the Common list as a floor, no domain leaves a
  caster without damage (fixes GF-M3's trap); retraining lets you swap a domain anyway.
- **No smite spells** (V24): *Divine Smite* (Presence) and *Searing Smite* (Fire) are off
  the lists. *Sworn Strike* (a Steel talent) is the one way to add resource-paid damage to
  a weapon hit, so a character's slot count never becomes weapon damage. *Hunter's Mark*
  (per hit, concentration, Beasts) stays; the engine does not treat it as a rider.
- **Divination:** **Thaumaturgy only** (canon).
- **Spell DC** 8 + PB + casting modifier; **spell attack** PB + casting modifier.
  Concentration: SRD.

### 5.1 Prismatic domains — options for the owner

*Owner, 2026-09-28: "We may want to revisit prismatic facets entirely, they were meant to
be penultimate casting paths but with the new SRD-like style we may want to rethink them
entirely." This supersedes Amendment 2 item 2 (prismatic open from 1st) until the owner
rules.* In the core rules the six prismatic domains — The Undying, Fate, The Living World
(Invocation); The Arcane, The Constructed Mind, Chronomancy (Thaumaturgy) — are the
pinnacle kinds of magic, and no character starts with one.

| | (a) Capstone of deep magic — **recommended, implemented provisionally** | (b) Fold into standard domains | (c) Leave them out of d20 |
|---|---|---|---|
| **Mechanics** | A prismatic domain can be learned only as the domain *Deep Magic* grants: three Spell talents with Spell the main track (5th level at the earliest). Lists unchanged. One line in the depth table; nothing else to learn. | Drop the tier: the six become ordinary domains, open from 1st to any caster of their tradition (Amendment 2 item 2 as written). The `prismatic` flag goes; Deep Magic becomes "one more domain". | Remove the six from `facets_d20_spells.yaml`; d20 has 15 domains. Their best spells (*Animate Dead*, *Polymorph*, *Counterspell*, *Banishment*, *Haste*…) move to the nearest standard domain or drop. Deep Magic becomes "one more domain". |
| **The Oracle** | Starts on **Presence** (Bless, Command, Heroism; *Turn the Odds* and *Kindle* carry the luck-bender at 1st), adds Binding at 3rd, and gains **Fate** at 5th as its Deep Magic domain — the moment the Oracle "comes into" prophecy. Viable at 1st: a full-strength support caster from its first pick. | Starts on **Fate** at 1st, as v0.2 had it. | Keeps no Fate: Oracle = Presence + Binding, the fate flavour living in *Turn the Odds* and *Prophecy*. Loses its signature domain. |
| **Simplicity** | +0 decisions (the Deep Magic domain is a pick either way); +1 clause in the depth table. | −1 clause; −1 term ("prismatic") to explain; 21 domains open at 1st (longest list to choose from at creation). | −6 domains to read; +1 migration note; canon friction (the catalogue has 21). |
| **Balance** | Prismatic lists hold the strongest control and utility (*Polymorph*, *Animate Dead*, *Haste*/*Slow*, *Counterspell*, *Banishment*). Tying them to Spell depth 3 makes "the best spells" something only a pure caster (or a 2/3 caster-leaning hybrid that gives up its Steel ranks) reaches — the owner's "things that make magic powerful". Hybrids never get them. | The strongest lists open to every 1-talent dip (a fighter with one Spell talent could take Chronomancy for *Haste*). Needs its own watch-list entry; removes a pure-caster reward. | Removes the problem and the reward. Pure casters' only depth-3 reward becomes breadth (a third standard domain). |
| **Canon** | Keeps the core rules' meaning (pinnacle magic) in d20 terms. | Diverges from canon (prismatic is a canon category). | Omits canon content; no contradiction. |

**Recommendation: (a).** It turns the prismatic tier into exactly what Amendment 2 needs —
the reward at the top of the magic ladder that a hybrid gives up — keeps canon's meaning,
costs no decision and keeps the Oracle whole at 1st. Implemented provisionally in the
data (`tracks.spell.ranks.deep_magic`, `casting.prismatic_from: deep_magic`, the presets'
`deep_domain`), flagged in both yaml files as **pending owner ruling**. Switching to (b)
is a data change (drop the `prismatic` gate and move the Oracle's Fate back to `domain`);
switching to (c) also deletes six domains and re-homes their sim spells.

---

## 6. Combat and encounters (ruling 2)

### 6.1 Player-facing rules (chapter 08)

1. **Side initiative, one roll a side.** Each side rolls one d20 + its best initiative
   modifier (the party's best Dex modifier; the MM's best among the foes). Higher side
   goes first; ties go to the players. *Alert* gives the party's roll advantage. A
   surprised side goes second. (v0.1's best-of-four gave the party the first move ~82% of
   the time — audit m14/GF-C1; one roll each is ~52% with equal modifiers.)
2. Within a side, creatures act in any order, each taking a whole SRD turn.
3. **Monsters deal fixed damage** (the SRD average); a crit rolls the dice (doubled) + mod.
4. **One reaction a round**; leaving a foe's reach provokes one opportunity attack (SRD).
5. **E1** one rider a turn; **E2** one controlled creature, acting right after you, fixed
   damage.
6. **Death**: SRD death saves.
7. **Sparks** (§6.3) are spent after a roll, before the outcome.

### 6.2 MM rules (chapter 09) — fixes K1/GF-C1, M6, M7, m15

- **Bosses act at the top of every round.** A boss takes one turn at the start of each
  round, before either side, and a second turn in its side's half. So a boss always acts
  before the party can finish it. Recharge rolls happen at the start of each of its turns.
- **Boss resolve** (generalises v0.1 ruling (d)): when a boss fails a save against an
  effect that would stun, paralyse, incapacitate, banish, polymorph or put it to sleep,
  it **loses its next turn instead, and the effect ends**. It can lose at most one turn a
  round this way. SRD Legendary Resistance and legendary/lair actions are crossed out.
- **Bloodied phase:** a boss changes at Bloodied (the MM's choice from 09's list).
- **Morale:** a standard (non-boss, non-minion) foe checks once, when it is first
  Bloodied: DC 10 Wisdom save; fail = flee, surrender or bargain. **Minions** check when
  their leader falls (the only "leader falls" trigger). Bosses, mindless and bound
  creatures never check.
- **Minions:** 1 HP; any damage kills one (hit, *Graze*-type or area); a successful save
  against damage takes none; fixed damage.
- **Focus fire:** MM guidance — spread the enemy side's attacks unless the fiction demands
  otherwise (GF-m7).

### 6.3 Sparks, Drives and social play (chapter 06)

- **Sparks:** start each session with 1; cap 3. **Earn:** (a) **a compel** — once per
  scene, when one of your Drives would make things harder, say so; if the MM agrees, you
  take the complication and a Spark (player-invoked, GF-M9); (b) the MM's call for a
  great moment; (c) *Kindle*, *Prophecy*, *Turn the Odds*. **Spend:** after any d20 test
  by you or an ally whose help you describe, before the MM says what happens, add **1d6**.
  One Spark per roll per player. No nat-1 earning (removes audit m1).
- **Drives:** two per character (a want, a line). Rewrite one at the end of any session.
  Suggested milestone: a Drive fulfilled or broken for good is a good time to level.
- **Attitude track:** unchanged from v0.1 06 (Hostile → Ally, one step per success, two on
  beating the DC by 10, down one on a miss by 5+; DCs 10/15/20 by how hard the NPC is to
  move). *Silver Tongue* per §4.3.

---

## 7. Encounter tables — specification (ruling 2)

**Balance pass result (2026-09-28, full run of `tools/d20_sim.py all --write`; the yaml
holds these numbers).** The MM's whole arithmetic: look up the Threat of each foe in
Table 9–2, add until the sum reaches Table 9–1's budget per character × the number of
players. Three adjustment lines: *a boss has twice its stat block's hit points* (V37, the
boss column already prices it); *a lone boss counts ×1.2* (V42); *a tired party (about half
HP and resources): build one tier down*. Party size needs no line — the budget is per
character (measured: three players −26%, five +24%, six +43% of the four-player Threat,
against −25/+25/+50% by the per-character rule).

**Table 9–1: Threat budget per character** (the baseline party is the 4th-level row)

| Level | Skirmish | Clash | Battle | Desperate |
|---|---|---|---|---|
| 1 | 10 | 16 | 19 | 23 |
| 2 | 12 | 19 | 23 | 27 |
| 3 | 16 | 25 | 31 | 34 |
| **4** | **19** | **30** | **34** | **41** |
| 5 | 33 | 49 | 60 | 68 |
| 6 | 34 | 52 | 63 | 71 |
| 7 | 40 | 63 | 76 | 84 |
| 8 | 46 | 69 | 82 | 94 |
| 9 | 62 | 91 | 105 | 116 |
| 10 | 66 | 95 | 110 | 120 |

**Table 9–2: Threat by CR** — standard √(HP × damage per turn); minion √(10.5 × damage per
turn); boss = standard × 3.34 (with doubled HP); never-breaks × 1.16; lone boss ×1.2.

| CR | 1/8 | 1/4 | 1/2 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Standard | 6 | 8 | 12 | 18 | 28 | 37 | 46 | 55 | 64 | 72 | 81 | 89 | 98 | 106 | 114 |
| Minion | 6 | 7 | 9 | 11 | 13 | 15 | 17 | 18 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| Boss | 20 | 27 | 39 | 60 | 94 | 124 | 154 | 184 | 213 | 239 | 269 | 298 | 327 | 353 | 382 |

**Outcomes at the budgets** (reference party, three shapes): Skirmish 1.9–2.4 rounds, 10%
HP; **Clash 2.97–3.58 rounds (3.46 at 4th), 26–28% HP, 99–100% wins, a PC dies in ≤ 1.4%
of 1st-level Clashes**; Battle 4.0–4.6 rounds, 43–48% HP, 85–95% wins; Desperate 4.1–5.1
rounds, 57–65% HP, 67–77% wins. **The day** (three Clashes, two short rests, V34): survived
90–99% at every level; the hard day (four Clashes) 41–78%. Robustness: 95% of random
parties land a Clash at the 4th-level Clash budget, 90% a Battle at the Battle budget.
Open item: real SRD monsters of a single kind built to the Clash budget (the *standards*
and *standards + minions* classes) land in the Clash band only 32–47% of the time and cost
40–45% HP on average — the Threat model underprices some real stat blocks (owner question
OQ-2 in `RESEARCH_facets_d20_balance.md`).

The DMG approach: every foe has a **Threat** value; each difficulty tier has a **Threat
budget per character** by party level; add foes until the sum reaches the budget.
**All numbers are derived by the simulator**; this section fixes the shape, the names
and the targets they must hit.

- **Tiers (our names):** **Skirmish**, **Clash**, **Battle**, **Desperate**. Targets are
  in the yaml (`encounter_tiers`): Skirmish 2–3 rounds, 5–15% party HP lost, ≥ 99% wins;
  **Clash** (the standard fight) **3–4 rounds**, 20–35% HP lost, ≥ 97% wins, a PC drops in
  ≤ 30% of fights; Battle 3–5 rounds, 35–55%, ≥ 90%; Desperate 4–5 rounds, 55–90%,
  60–85% wins. An adventuring day = three or four Clashes with two short rests.
- **Baseline party:** four 4th-level PCs, the reference party (Fighter, Rogue, Wizard,
  Priest presets). Robustness check: 20 random parties of four distinct presets must land
  in the same tier ≥ 80% of the time.
- **Table 9–1 (by level 1–10 × tier):** Threat budget per character.
- **Table 9–2 (Threat by CR and role):** for SRD 5.2.1 CR 1/8–12, columns *standard*,
  *minion*, *boss*. Minion Threat must price auto-hit and area spells (GF-m8).
- **Composition rules** the budget must hold across: solo boss; boss + minions; boss +
  standards; 2–6 standards; standards + minions; minion swarm. A boss encounter's boss is
  ≥ 50% of the budget. The sim reports any composition class that misses its tier ≥ 20% of
  the time; the table then carries a note or a multiplier for it, not a hidden fudge.
- **Adjustments (Table 9–3), phrased as the owner asked** ("five players: add X"):
  - three players: remove foes worth *x* Threat (or: use the next tier down's budget if
    closer);
  - five players / six players: add a standard foe worth *y* / *z* Threat;
  - **tired party** (entering at ~50% HP and ~50% daily resources): drop one tier, or
    remove *w* Threat. Each derived by rerunning the fit under that condition.
- **If Clash cannot land in 3–4 rounds by budget alone** (e.g. the boss rule or morale
  makes fights too short or long at some levels), the sim reports it and the Planner
  changes a rule; the table is never bent to hide a rules problem.

---

## 8. Balance band (ruling 3)

**Balance pass (V32).** The **swap test is the primary measure**: the reference party with
the build swapped in for each member in turn plays standard days (three Clashes, two short
rests); the score is the party's HP lost per fight against the preset median. Band: every
preset **and every sim build** within ±15% at 1st, 4th, 7th and 10th; Facet means within
±10%; item 7 on the swap score (a hybrid at or below its Facet's best pure build, +3
points of sampling noise) and on DPR₁/DPR₃ as before. PI (below) is kept as the
secondary measure and reported beside it. Final table: §8.1 addendum and
`RESEARCH_facets_d20_balance.md`. Items 1–7 below are the original PI version, kept as
the record.

- **Metrics per build and level** (L = 1, 4, 7, 10), measured by the simulator over a
  standard day (four Clashes, two short rests) against the level's reference foes:
  - **eDPR\***: mean damage dealt per round, plus support converted to the same unit:
    enemy damage prevented (reactions, *Guardian*, *Warden*-saved effects, disabled enemy
    turns × that enemy's DPR) and healing actually restored to allies (no overheal).
  - **eHP**: HP + temporary HP + self-healing per fight, divided by the reference
    attacker's hit chance against the build (so AC, resistance and *Shield*-type
    reactions count), normalised to a 55% baseline hit chance.
  - **PI** (power index) = eDPR\* × eHP.
  - **DPR₁ / DPR₃**: damage per round against one / three dummies (the engine's
    `damage_per_round`) — the *martial job* and the *casting job* of item 7.
- **The band:**
  1. Every preset's PI within **±15%** of the median preset PI, at each of 1/4/7/10.
  2. Each Facet's preset mean PI within **±10%** of the overall median.
  3. Every `sim_build` (flagged combo) **≤ median + 15%** (weaker is allowed).
  4. Median preset PI within **±15%** of the median SRD baseline PI (SRD 5.2.1 Fighter
     Champion, Rogue Thief, Wizard Evoker, Cleric Life, Paladin Devotion, Barbarian
     Berserker, built to the same method).
  5. Sanity: no preset's eDPR\* or eHP below 50% or above 200% of the median (roles stay
     roles).
  6. Cross-check: the **swap test** (the reference party with the build swapped in for
     each member in turn, Clash set) must rank builds in the same order as PI to within one
     place; big disagreements are reported for the Planner.
  7. **Hybrids pay (Amendment 2).** From 4th level, for every build `balance.roles` lists
     as a hybrid: (a) its PI ≤ the best pure build of its Facet (either role) + 15%;
     (b) if Steel is its main track at that level, its DPR₁ ≤ the best pure martial of its
     Facet + 5%; (c) its DPR₃ ≤ the best pure caster of its tradition + 5%
     (`balance.tradition_casters`). "Best" = highest among the builds listed for that role.
- **Builds the sim must run:** all 12 presets and all `sim_builds` in the yaml. By
  Facet and role (`balance.roles`):

  | Facet | Pure martial | Pure caster | Hybrids (Steel · Spell at 10th) |
  |---|---|---|---|
  | Body | Fighter, Rogue, Barbarian, Monk, *unbreakable* (M3), *reckless_striker* | *body_caster* (Spell 2, Half table, E3) | *body_ranger* (3·1, M8), *body_battlemage* (2·2, C1 on Body) |
  | Mind | Investigator | Wizard, Loremaster, *mind_controller* (M6), *double_cross* (M4) | Tinker (1·1), *spellblade* (2·2, C2), *armored_caster* (1·3) |
  | Soul | *soul_champion* (3·0) | Priest, Druid, Oracle, *healer_engine* (M1), *soul_blaster* (GF-M2), *summoner* (M7) | Oathsworn (2·1), *battle_priest* (2·2, C1), *battle_priest_deep* (2·3, C1 worst case), *paladin_max* (2·2, C1) |

  plus *monk_stunner* (m15, the Monk preset against bosses).
- **Tuning knobs** (what the balance pass may change without a Planner decision): dice
  and flat numbers inside talents (`dice`, `value`, `uses`, `by_level`), which level a
  scaling step lands on (5th/9th ± 1), the Veteran numbers, and preset picks/kit.
  Anything else — a new rule, a track tag, the depth thresholds, the main-track rule,
  removing a talent — goes back to the Planner.
- **Watch list** for the tuner: *Alert* (side-initiative advantage in 3-round fights);
  *Precision* dice with Extra Attack; *Field Kit* temp HP at 9th–10th; *Master Plan*
  first-round party advantage; *Turn the Odds* fight-start Spark; *Shillelagh* (Verdance)
  lets a Soul hybrid attack with Wisdom, which removes the hybrid's two-ability tax;
  a player flipping main track by retraining every level (the retrain rule allows one swap
  a level — watch that it does not become routine).

### 8.1 First measurement of the tracks chassis (Designer, 2026-09-28)

Designer's harness (scratch; it translates §1.2 into the talent effects the engine
already reads and calls the engine for every number — no rule outside
`software/facets_d20/`), 250 standard days per cell, reference-party companions, the
calibrated Threat model and Clash budgets from `software/research/facets_d20_sim_results.json`.
PI relative to the preset median at that level (medians 45 / 369 / 1,491 / 3,350). The
engine agent reruns the full §8/§9 report once P-5 lands; these numbers are for the
chassis decision, not the final band.

**Engine run (P-18, 2026-09-28).** The table below is `software/tools/d20_sim.py all` (500 standard days per cell, Clash budgets and Threat model from the same run; preset-median PI 47 / 342 / 1581 / 2991); it replaces the harness numbers. Full tables, eDPR\*/eHP/DPR and the swap test: `docs/RESEARCH_facets_d20_sim.md` §8. **Item 7 fails only for the Tinker at 4th (+161% over the best pure Mind build)**; every other hybrid passes at 4th, 7th and 10th.

| Facet | Role | Build | L1 | L4 | L7 | L10 |
|---|---|---|---|---|---|---|
| Body | pure martial | Fighter | +69% | +21% | +35% | +23% |
| Body | pure martial | Rogue | +5% | -1% | +37% | +19% |
| Body | pure martial | Barbarian | +61% | +59% | +16% | +13% |
| Body | pure martial | Monk | +39% | +57% | +15% | +21% |
| Body | pure martial | *unbreakable* | +56% | +50% | +20% | +23% |
| Body | pure martial | *reckless_striker* | +38% | +48% | +27% | +26% |
| Body | pure caster | *body_caster* | +66% | -15% | -32% | -32% |
| Body | hybrid | *body_ranger* | -12% | +16% | +4% | +14% |
| Body | hybrid | *body_battlemage* | +40% | +24% | -4% | -26% |
| Mind | pure martial | Investigator | -15% | -31% | -39% | -20% |
| Mind | pure caster | Wizard | -57% | -40% | +6% | +27% |
| Mind | pure caster | Loremaster | -63% | -54% | -51% | -58% |
| Mind | pure caster | *mind_controller* | -64% | -39% | -19% | -30% |
| Mind | pure caster | *double_cross* | -58% | -36% | +4% | +10% |
| Mind | hybrid | Tinker | +30% | +80% | +17% | +3% |
| Mind | hybrid | *spellblade* | -22% | -33% | -50% | -43% |
| Mind | hybrid | *armored_caster* | -57% | -43% | +4% | +14% |
| Soul | pure martial | *soul_champion* | +33% | -4% | -23% | -6% |
| Soul | pure caster | Priest | -5% | +1% | -18% | -3% |
| Soul | pure caster | Druid | -33% | -54% | -41% | -41% |
| Soul | pure caster | Oracle | -8% | -9% | -26% | -19% |
| Soul | pure caster | *healer_engine* | -9% | +3% | -18% | -6% |
| Soul | pure caster | *soul_blaster* | -48% | -38% | -5% | +1% |
| Soul | pure caster | *summoner* | -19% | -29% | -36% | -32% |
| Soul | hybrid | Oathsworn | +22% | +15% | -6% | -30% |
| Soul | hybrid | *battle_priest* | -2% | -1% | -10% | -30% |
| Soul | hybrid | *battle_priest_deep* | +33% | -5% | -10% | -11% |
| Soul | hybrid | *paladin_max* | +36% | +14% | -8% | -22% |
| — | combo | *monk_stunner* | +38% | +60% | +22% | +17% |

**Item 7 (hybrids pay), from 4th:** holds for every hybrid except the **Tinker** at 4th
and 7th (PI +100% / +15% over the best pure Mind build while its DPR₁ is −35–50% and its
DPR₃ −44–74% of the pure builds'): the excess is *Clockwork Guardian*'s guard and *Field
Kit*'s temp HP, both support the eDPR\* counts as prevented damage — a talent-number
item for the tuner. Soul's hybrids sit within +13% of the better pure Soul build at 4th
and within +3% at 7th, at or below it at 10th; Body's are below its pure martials at every
level; the *armored_caster* stays within +3% of the Wizard from 5th.

**Items 1–3 are not met yet, and were not met under paths either** (engine report of the
same date): Body presets run high (Fighter, Monk), Mind casters low at 1st–4th (d6, AC
12–15) and high at 10th (Wizard), Loremaster and Druid low throughout, Investigator low.
None of those gaps comes from the chassis change — they were there before it — and all
are tuning-knob work. Level 1 is dominated by the Body chassis (d10, AC 18–19) because
PI multiplies eHP; the engine's E-9 (make the swap test primary) bears on this and is
still open for the Planner.

---

**Balance pass, final (swap test, primary; 2026-09-28, full run).** Swap score vs the
preset median (positive = the party loses less with the build in it). Every preset and sim
build is inside ±15% at every level; Facet means within ±7%; every hybrid at or below its
Facet's best pure build, and no Steel-main hybrid out-hits its Facet's pure martials (DPR₁)
nor any hybrid its tradition's casters (DPR₃) by more than 5%. PI (secondary) in the last
column. The PI table above is the pre-pass record.

| Build | Kind | L1 | L4 | L7 | L10 | PI L1/4/7/10 |
|---|---|---|---|---|---|---|
| Fighter | preset | +5% | +1% | +2% | -1% | +42/-9/+30/-1 |
| Rogue | preset | -3% | -5% | +8% | +8% | +13/-20/+60/+31 |
| Barbarian | preset | +9% | +10% | +10% | +6% | +49/+29/+27/+2 |
| Monk | preset | +9% | +12% | +6% | +11% | +25/+7/+21/+7 |
| Wizard | preset | -6% | -1% | -2% | +1% | -19/+9/+27/+6 |
| Investigator | preset | +0% | -6% | -7% | -4% | +1/-22/-1/+1 |
| Loremaster | preset | -5% | -11% | -9% | -3% | -36/-29/-21/-29 |
| Tinker | preset | -1% | -1% | -6% | -7% | -12/-1/-15/-30 |
| Priest | preset | -0% | +7% | +6% | +4% | -1/+8/+1/+6 |
| Druid | preset | -10% | -7% | +7% | +6% | -31/-14/-2/-18 |
| Oracle | preset | +2% | +9% | -9% | -7% | -9/+1/-15/-22 |
| Oathsworn | preset | +6% | +1% | -4% | -10% | +52/+20/-1/-17 |
| sim builds (17) | | −8…+9% | −8…+12% | −6…+12% | −10…+12% | |
| SRD baselines (6) | | −28…−7% | −20…−1% | −21…+2% | −24…−8% | |

## 9. Simulator requirements (for the engine agent)

What the Planner needs from `software/facets_d20/`, in priority order.

- **S-1 Loader** for both yaml v0.2 files against §1 (and §1.4a); an unknown effect type
  or keyword is a load error.
- **S-2 Character builder and legality checker** for presets, sim builds and custom
  builds at any level 1–10: HP, AC, attack bonus, save DC, spell attack, slots, resources,
  lists. The checker implements `build_rules` and the tracks (§1.2), and rejects three cross
  picks, a Body caster with no `tradition`, a domain of the wrong tradition and a
  prismatic domain without Deep Magic. (The v0.1 Battle Priest and Spellblade shapes are
  now *legal* hybrids, measured by band item 7.)
- **S-3 Combat engine** implementing §6.1–§6.2 exactly: side initiative (one roll each),
  boss top-of-round turn and resolve, fixed damage and crits, minions, morale (first
  Bloodied for standard foes; leader-falls for minions), E1, E2, concentration, one
  reaction (*Shield*, *Guardian*, *Anticipate*, *Cunning*'s halve), Sparks (spend policy:
  only when +1d6 can turn the result), resources across a day with short rests. The
  simulator may only call the shared rules module (CLAUDE.md: never a second rules copy).
- **S-4 Spell models:** the engine's E-1 set plus `ac_set` (*Mage Armor*, precast),
  `ac_bonus` (*Shield of Faith*), `sustain` (spells that re-attack on later turns), and
  `per_hit` on `weapon_rider` (*Hunter's Mark*). Spells not in `sim_spells` are never cast
  by the sim.
- **S-5 Policies:** simple and documented: focus the lowest-HP threatening foe; area spell
  when its `targets` assumption holds (≥ 2 foes, allies safe or *Sculpt*); healers heal an
  ally below 50% or at 0; pace daily resources evenly across the day's four fights; take
  the highest expected-value option each turn. The same policy for every build (no
  per-build tuning).
- **S-6 Monsters:** SRD 5.2.1 stat blocks, numbers verified against the PDF
  (`docs/RESEARCH_facets_d20_srd_check.md` names it): the six 09 conversions plus a CR
  ladder 1/8–12 (≥ 2 per CR, mixing melee, ranged, casters), each usable as standard,
  minion (1 HP) or boss.
- **S-7 Outputs:** per build × level: eDPR\*, eHP, PI and band verdict (§8); swap test;
  encounter fits (Tables 9–1 to 9–3); round counts and HP lost per tier. Write the fitted
  numbers back to the yaml (`encounter_table`, `encounter_adjustments`, `monster_threat`)
  and the full report to `docs/RESEARCH_facets_d20_sim.md`. Seeded; N ≥ 2,000 fights a
  cell; report confidence intervals.
- **S-8 Rule tests** (ruling 6): computed HP / AC / attack / DC / slots for all 12
  presets at 1, 4, 7, 10 pinned; each exploit build illegal or inside the band; a
  small-N smoke test that a baseline Clash lasts 3–4 rounds; E1/E2/boss-resolve unit
  tests. Replace no data test with a wording test.
- **S-9 SRD baselines** as builds the same engine runs (§8 item 4), not hand numbers.

---

## 10. Presets (card contents)

In the yaml (`presets`). Each card prints: concept line, Facet, its track shape (Steel ·
Spell at 10th and the main track), domain, final ability scores, background, the two
Facet skills, the five talents by level with their [St]/[Sp] tags, the three knack
suggestions, kit and the resulting AC/HP/attack at 1st, plus a one-line "Play it like".
Cards are complete sheets: a player chooses only name, Drives, Specialty and a language
(§2.2). No preset ever changes its main track while levelling.

| Facet | Preset | Shape (St · Sp) | Domain (+ Wider Study, Deep Magic) | Talents 1 · 3 · 5 · 7 · 9 |
|---|---|---|---|---|
| Body | Fighter | 3 · 0 | — | Weapon Expert · Guardian · Cleave · Hardy · Alert |
| Body | Rogue | 3 · 0 | — | Precision · Cunning · Marksman · Weapon Expert · Alert |
| Body | Barbarian | 3 · 0 | — | Rage · Hardy · Cleave · Guardian · Alert |
| Body | Monk | 2 · 0 | — | Martial Arts · Cunning · Weapon Expert · Hardy · Alert |
| Mind | Wizard | 0 · 3 | Constructed Force (+ Illusion 3rd, The Arcane 5th) | Evoker · Wider Study · Turn the Odds · Iron Mind · Hardy |
| Mind | Investigator | 3 · 0 | — | Precision · Anatomist · Anticipate · Weapon Expert · Hardy |
| Mind | Loremaster | 0 · 3 | Illusion (+ Divination 3rd, Chronomancy 9th) | Turn the Odds · Wider Study · Master Plan · Hardy · Evoker |
| Mind | Tinker | 1 · 1 (tie: Steel) | Transmutation | Clockwork Guardian · Weapon Expert · Field Kit · Hardy · Anticipate |
| Soul | Priest | 0 · 3 | The Tide (+ Presence 3rd, The Living World 5th) | Channel · Wider Study · Mending Hands · Warden · Hardy |
| Soul | Druid | 0 · 3 | Verdance (+ The Tide 3rd, The Living World 5th) | Wild Shape · Wider Study · Channel · Hardy · Warden |
| Soul | Oracle | 0 · 3 | Presence (+ Binding 3rd, **Fate** 5th) | Turn the Odds · Wider Study · Prophecy · Warden · Alert |
| Soul | Oathsworn | 2 · 1 | Presence (from 3rd) | Sworn Strike · Mending Hands · Weapon Expert · Warden · Oath Unbroken |

The Oathsworn is now the natural hybrid (the paladin shape: Extra Attack, heavy armor,
Half table from 3rd, *Mending Hands*). The Tinker is the artificer shape (armor and a
bigger die from its Steel pick, Half table, no Extra Attack). Loremaster is a caster who
spends three picks on general talents and so never reaches Deep Magic — a legitimate
choice, and the weakest preset in §8.1 (tuning item). The Monk keeps Extra Attack at 5th
but stops at Steel 2 (no Veteran, *Martial Arts* never reaches d10) — the Monk ran far
above the band under paths.

---

## 11. Canon

- **Divination: Thaumaturgy only**, as the catalogue says (CAN-1).
- **Prismatic domains** — §5.1, pending owner ruling; option (a) is in the data
  provisionally. Amendment 2 item 2 (open from 1st) is suspended by the owner's later
  message until that ruling.
- **The Common list is a rules device, not lore.** 07 must not describe how a Thaumaturge
  makes fire or relate it to the Fire domain; it says only that every caster of either
  tradition can learn these spells (owner ruling 4). The domain catalogue's territories
  are unchanged.
- **Body has no tradition of its own** (canon). In d20 a Body character may still learn
  magic through cross-Facet Spell talents and names Invocation or Thaumaturgy when it does
  (E3) — a rules option like the Common list, not a claim that Body has a tradition. The
  prose must not invent a Body tradition name (the Wildcraft/Root shortlist stays void).
- **The recurring cast (CAN-2):** Mordai's two Drives are canon (Amendment 2 item 3):
  *protect people who can't protect themselves*; *never leave a fight while someone weaker
  is still in it*. "Eleven years" stays removed ("for years"). Zulnut: keep "Wandering
  Disciple" and his Facet; the invented teacher and Specialty wording stay removed. The
  alley leader loses "Watch training, years ago". Zahna: only established facts.
- Traditions keep their canon names and styles. Mirror Master (MM), never GM/DM.

**Open questions for the owner:** Q1 (the path) — **answered by Amendment 2**: no path;
tracks and the main-track rule (§3.2). Q2 — prismatic domains, §5.1 (recommend (a)).
Q4 (new) — is a rank that *lapses* when the main track flips acceptable at the table
(§3.2, V25), or should ranks, once gained, be kept? Keeping them re-opens the 3/2 build
that holds Full casting and Extra Attack at 9th–10th (measured +34% over the median
under thresholds), so the recommendation is to let them lapse.

---

## 12. Decisions

- **Owner rulings (2026-09-28, BRIEF Amendment 3):** §5.1 option (a) — prismatic domains only through Deep Magic — is **confirmed**, no longer provisional. Q4 — **ranks lapse** — confirmed.

- **V21 (owner, 2026-09-28):** 4th and 8th are no longer zero-choice levels: pick +2 to one ability, +1 to two, or one extra knack. Simplicity budget: level-up stays ≤1 choice; "zero at 4th and 8th" no longer holds; choices over levels 2–10 go from 8 to 10.

| # | Decision | Why | Rejected |
|---|---|---|---|
| V1 | ~~**Path** (Steel/Spell) chosen at 1st by Mind and Soul; Body always Steel~~ — **superseded by V22 (Amendment 2)** | One structural choice replaces v0.1's three anti-gish carve-outs (C1, C2, GF-M1) and the half/full ordering trap (M5) | Recommended fix (c) "casters can't take X"; "*Martial Training* drops you to the Half table" (two rules, still exceptions) |
| V2 | **Five talents** (1/3/5/7/9) that scale at 5th/9th; no tiers, prerequisites or signatures | Level-up ≤ 1 choice; menus of 10–13; talents big enough to carry a character | 11 small talents + signature (v0.1); talents at even levels (would leave no room for knacks without 2-choice levels) |
| V3 | **Knacks** at 2/6/10 + background | Roleplay picks stop competing with combat (GF-M5); they are small, so total load drops even though the count of picks is similar | Knacks at every odd level (PF2e skill feats — too many); no knack track (fails ruling-brief RP intent) |
| V4 | ~~**ASI automatic** (+1 to two highest at 4th and 8th)~~ — **superseded by V21** | Two zero-choice levels; removes ASI-vs-talent trade | ASI as a talent (v0.1); a free +2 choice (still a choice) |
| V5 | **Background +1/+1/+1**, fixed knack | Removes the split decision and origin-talent pick | SRD +2/+1 split |
| V6 | **Common list + one domain; no preparation; all list cantrips known** | Ruling 4 (fireball for Mind), and four to fourteen decisions gone at creation and daily | Evocation domain for Thaumaturgy (canon: Constructed Force excludes elemental force); Fire/Storm dual-tradition (another Divination-style canon change); fewer broader domains (would redraw canon territories) |
| V7 | **Slots by character level**, one clock — kept; the table (Half/Full) now comes from Spell depth and main track (V22, V25) | Late-caster loophole is moot under V1 (full casting is a 1st-level path); half casters taking the talent late just missed earlier levels | Caster level (v0.1 ruling (a)) |
| V8 | **One tradition per character** | Removes M5's four unanswered questions | Rules for dual traditions |
| V9 | **Cross-Facet cap of two**, no tier gate | One number replaces the "two from that Facet" gate and its double-counting bug (M4) | v0.1 gate |
| V10 | **Riders: one a turn** (E1) | One rule for every present and future extra-damage stack | Per-talent carve-outs |
| V11 | **One controlled creature** (E2) | Summons/armies (M7) | Per-spell caps; counting summons as 0.5 PC |
| V12 | **Boss top-of-round turn + resolve**; Legendary Resistance crossed out | K1: bosses always act; M6 and m15 in one rule | "Shrugs off first effect" (LR-style) — still lets two control effects remove a round |
| V13 | **Morale: first Bloodied for standard foes; leader-falls for minions only** | GF-C1 cause 4 | v0.1 leader-falls for all |
| V14 | **Side initiative: one roll a side** | Party-first drops from ~82% to ~52%; simpler than best-of-four | Best-of-four with MM best-of-group |
| V15 | **Sparks = +1d6 after the roll only**; compels are player-invoked; no nat-1 earn | One mechanic per job; RP trigger players own (GF-M9); removes m1 | Spark advantage/reroll modes |
| V16 | **Healing:** *Channel*'s boost only on a slot spell's healing as cast, one creature; *Field Medic* a Hit-Die knack; *Survivor* cut | M1, M2, M3 structurally | Once-per-turn caps on a per-instance boost |
| V17 | **Divination Thaumaturgy-only**; prismatic → §5.1 and V31 | Canon iron law | Keeping v0.1's dual Divination |
| V18 | **Tinker = half caster in armor** — restated under tracks: Steel 1 · Spell 1, a tie, so Steel main (armor step, d8) and the Half table, no Extra Attack | Artificer shape; a preset exercises half casting | Spell-path Tinker (v0.1: crossbow-only at 3rd, GF-M3) |
| V19 | Rewrites in §4.2, including *Alert*, *Iron Mind*, *Linguist*, *Many Faces* found beyond the audit's nine | Ruling 5 | Keeping resemblance with a note |
| V20 | Chapter-agreement tests retired until the prose pass; data tests check the contract (types and keywords must appear in this file's §1) | Ruling 6: tests test rules; the engine owns computed-rule tests | Keeping v0.1 wording tests red |
| **V22** | **No paths. Every talent is tagged Steel, Spell or general; depth in a track buys its ranks** (§3.2) | Amendment 2: casting and martial power bought with the same picks; no gates | Steel/Spell path (owner rejected); "casters can't take X" carve-outs |
| **V23** | **Casting is a rank, not a talent.** The first Spell talent of any kind makes you a Half caster; the separate *Thaumaturgy*/*Invocation* half-caster talents and *Wider Study*'s "needs casting" are cut | One way to become a caster; the owner's "one talent = half, two = full" | Keeping tradition talents (a pick with no rider, and a second route to casting) |
| **V24** | **No smite spells on any list**; *Sworn Strike* is the one resource-paid weapon rider | Slots otherwise convert into weapon damage, so a full-slot hybrid out-strikes the pure martial; one mechanic per job | Capping smite slot level; smites off E1 |
| **V25** | **Main track = the track with more talents (Steel on a tie); ranks past depth 1 (and Martial Training) need it; recomputed live, so ranks can lapse** | Plain thresholds let a 2/2 build hold Full casting, Extra Attack and heavy armor: +30–47% over the median at 9th–10th, above both pure Soul builds. The majority lets one track master and makes the hybrid choose | Thresholds only (measured, fails); ranks kept once gained (re-opens 3/2 at +25–34%); a declared main track (a path by another name) |
| **V26** | **Martial Training (armor step, hit die) needs Steel main; martial weapons don't** | A full caster's one Steel pick bought medium armor, a shield and d8 and ran +58–92% over the median; with the rule it measures ≈ the Wizard | Armor from the Facet only (Mind martials in light armor; Tinker loses its identity); armor step at depth 2 (Mind martials armorless at 1st–2nd) |
| **V27** | **Body counts two extra Steel talents toward its main track** (E3): Body casts on the Half table | The Body chassis (d10, all armor, *Second Wind*, *Action Surge*) is free Steel; a Body full caster measured +66–78% at 9th–10th | "Body can't take Spell talents" (a gate); Body counting one extra (still Full with two cross Spell picks) |
| **V28** | **Upgrades need depth**: a tracked talent's 5th-level line needs 2 of its track, its 9th-level line 3 | The owner's "riders that key off investment" in one sentence; a one-talent dip never grows | Per-talent scaling by count (more text on every card) |
| **V29** | **Steel depth 3 = Veteran** (+1 HP/level, +2 weapon damage); **Spell depth 3 = Deep Magic** (+1 domain, may be prismatic) | Both tracks reward depth symmetrically; without Veteran a Soul 2/1 hybrid out-hit the Soul pure martial at 5th | +1 HP/level only (too small); a hit die step (dead with *Hardy* at d12); +1 AC (AC inflation) |
| **V30** | **Weapon Expert on all three menus** | Every Facet needs a Steel talent of its own so a Mind or Soul martial doesn't depend on cross picks | A new Soul/Mind weapon talent (menu growth) |
| **V31** | **Prismatic domains: option (a), capstone of Deep Magic — provisional** (§5.1) | Owner reopened the question; (a) is the pure caster's reward and keeps canon | (b) fold in, (c) drop — both listed for the owner |

**Balance pass (Balance tuner, 2026-09-28).** Log and numbers:
`docs/RESEARCH_facets_d20_balance.md`; simulator report `docs/RESEARCH_facets_d20_sim.md`.

| # | Decision | Why | Rejected |
|---|---|---|---|
| **V32** | **The swap test is the band's primary measure; PI is secondary.** The reference party with the build swapped in for each member plays standard days; score = the party's HP lost per fight against the preset median. Every preset *and* every sim build within ±15% at 1st/4th/7th/10th | It measures what the owner cares about (does the party do better with this character in it) and credits healers, control and protection that PI undercounts; PI multiplies a build's damage by its own toughness, so it ranked Body duelists top and healers bottom and disagreed with party outcomes (Spearman 0.46–0.82, engine E-9). Days, not single fights, so daily resources are paced as at the table | PI primary (rewards self-sufficient duelists); eDPR\* + k·eHP (a weight to pick, still solo) |
| **V33** | **E-9: the +2 (or +1/+1) at 4th and 8th goes to the ability your main track uses** — your casting ability if Spell is main, otherwise your main weapon's. Every preset card prints its picks (`asi:`), and a test holds them to the rule | One sentence, the same rule the main track already teaches; a Steel-main hybrid is a weapon-user first. Measured: raising the casting ability instead helped the Soul hybrids 1–3 points at 10th and cost the Body hybrids 4–12 | Casting ability for anything that casts (the Designer's harness) |
| **V34** | **The adventuring day is three Clashes with a short rest after the first and the second** (yaml `adventuring_day`); a single Clash gets a third of each daily pool. Four Clashes with two short rests is a hard day | At a Clash that costs about 27% of the party's HP, four in a row were survived 33–81% of the time; three are survived 81–99%. Fits the RP-first, short-fight table | A stronger short rest (Hit Dice at maximum moved the four-fight day only 2–10 points); a cheaper Clash (the day needs Clashes near 16% HP, below the tier) |
| **V35** | **1st-level hit points = hit die + 8 + Constitution modifier** (then as before) | A 1st-level Clash killed a PC 15% of the time (8-HP wizards against 8-damage hits). +8 takes it to about 2%; a flat bonus helps the d6 as much as the d10, so Body stops dominating 1st level (twice the hit die was tried: fine for lethality, but Body +10 HP against Mind +6) | Twice the hit die; a death-save rule (an exception) |
| **V36** | **Mage Armor moves to the Common list** | Every unarmored caster can defend itself; Mind casters without Constructed Force sat at AC 12 and died in a tenth of 10th-level days. Owner ruling 4: fewer choices that trap a 1st-level pick | Adding light armor to casters' kits (a d6 caster in leather is still AC 12) |
| **V37** | **A boss has twice its stat block's hit points** (MM rule; Table 9–2's boss column already prices it) | Bosses died in two rounds, so boss fights ran 2.1–2.6 rounds and 5th–6th-level Clashes under 3; doubled, the Clash is 3.0–3.7 rounds at every level, and a lone boss is mispriced far less | Monster HP scaled by party level (a table the MM must apply to every foe); lone bosses only (leaves boss + minions short) |
| **V38** | **Encounter method** (no rule): minions in fitted shapes are at most half the CR of a standard of the budget; generic foes deal the SRD ladder's share (15%) of non-weapon damage; every foe attacks a random standing PC (§6.2); the AI takes the higher expected value between the Attack action and area, aura and disable spells (S-5) | A few high-CR "minions" were ending 5th–10th-level Clashes in 2.6 rounds; rage's resistance met only weapon damage; bosses focusing the weakest PC contradicted §6.2; hybrids spent actions on low-DC spells | — |
| **V39** | **Talent numbers** (the §8 knobs): *Channel* 1 use (2 from 5th, 3 from 9th); *Evoker*'s +casting-modifier damage from 1st (was 5th); *Guardian* reduces by half your level (round up), no 9th-level doubling; *Weapon Expert*'s crit heal = half your level; *Martial Arts* d4/d6/d8 die, focus = half your level, Flurry costs 2; *Second Wind* 1 use (2 from 5th); *Field Kit* temp HP = half your level; *Anatomist* adds your Int modifier to weapon damage against your studied target; *Master Plan* holds through the second round from 5th | Each closes a measured gap: 1st-level healers and the Body caster (Channel), Mind weak early (Evoker, Anatomist), the raging tank at 10th (Guardian, Weapon Expert), the Monk +33% at 7th (Martial Arts), Body at 1st–4th (Second Wind), the Tinker (Field Kit + E-D16), the Loremaster (Master Plan) | Cutting Stunning Strike (the Monk stayed +20%); a Study buff (+2–3 points for all Mind; not needed); rage damage +1 (little effect) |
| **V40** | **Preset picks and kits**: Monk takes Hardy at 7th and Alert at 9th (Alert was worth ~10 points at 7th); Investigator Anatomist 3rd, Anticipate 5th, Weapon Expert 7th (Veteran from 7th); Loremaster Hardy 7th and Evoker 9th (Deep Magic, Chronomancy) instead of Alert/Iron Mind, Con 14, no armor; Druid's Wider Study domain is The Tide (was Beasts). Sim builds: *spellblade* takes Clockwork Guardian and Turn the Odds as its Spell picks and Dex 16/Int 15 (the strongest version of the C2 shape); *soul_blaster* unarmored | Each preset stays its concept; the spellblade tests the shape at its best, as an audit build should | Keeping the Loremaster's three general picks (−22% at 10th) |
| **V41** | **Tier targets**: Skirmish lasts "about two rounds" (1.5–2.5); Battle wins 85–95% | The owner's definitions; a Skirmish that costs 10% of HP cannot last 2–3 rounds (engine E-10) | — |
| **V42** | **A lone boss counts ×1.2 its boss Threat** (one line under Table 9–2) — see §7 | Measured mark-up that makes the Clash budget buy a Clash: ×1.11–1.15 at 1st–4th, ×1.20–1.24 at 5th–8th, ×1.33–1.35 at 9th–10th (median ×1.20) | ×1.5 (the engine's first guess; with V37 it makes a lone boss a Skirmish) |
| — | *Tried and dropped:* a 9th-level scaling depth of 2 (V28 kept) | It lifted hybrids 4 points at 10th, but after V37–V40 every hybrid was inside the band without it, and with it two Soul hybrids out-hit the Soul pure martial | — |

Resolved enough to implement. **Return to the engine agent for *Planner → engine* P-5
onward (end of file), then to the balance pass (§8 tuning items), then to a prose pass
from §2–§11.**

---

## Engine notes

*Appended by the Engine builder (2026-09-28). Details in
`docs/DESIGN_facets_d20_engine.md`. The engine binds to §1 as written; these are the
points where it needs a decision or an extra field.*

- **E-1 `sim_spells` models.** The engine understands these `model:` values (anything
  else is a load error): `attack` (spell attack; `dice`, `beams`, `beams_upcast`),
  `save` (single or area: `dice`, `save`, `half_on_success`, `targets`),
  `auto` (Magic Missile: `dice`, `beams`, `beams_upcast`, `plus`), `heal` (`dice`,
  `add_mod`, `targets`, `action: action|bonus`), `aura` (concentration, ticks once a
  round on up to `targets` foes: `dice`, `save`), `weapon_rider` (Divine Smite-type:
  `dice`), `weapon_cantrip` (True Strike / Shillelagh), `disable` (`save`, repeat save
  each turn), `shield` (reaction +5 AC). `area_save_damage` is accepted as an alias of
  `save` with `targets ≥ 2`. Optional on every entry: `upcast` (dice per slot level),
  `concentration`, `action`, `damage_type`. Until `sim_spells` lands the engine uses its
  own table in `software/facets_d20/spells.py` (same fields) and will switch to the yaml.
- **E-2 `advantage` needs a cost field for Reckless-type talents**: e.g.
  `{type: advantage, on: [attack], scope: melee_str, grants_foes_advantage: true}`.
  Without it the engine can't tell Reckless Attack from a free advantage.
- **E-3 ASI tie-break.** "+1 to your two highest" — engine rule: the two highest scores
  below 20; ties broken by the preset's `abilities` order as written (str, dex, con, int,
  wis, cha). Say so in the book or give presets an explicit order.
- **E-4 Custom-build abilities.** Presets give final scores. For a custom build the
  engine validates `base_abilities` (standard array permutation or 27-point buy) +
  background `abilities`. Fine as specified; noting it.

## Planner → engine (2026-09-28, after reading the engine code)

- **P-1** The yaml now uses `roll:` where §1 first said `on:` (PyYAML turns a bare `on:`
  key into `True`), and `condition_on_hit` names its condition `inflicts:`. `data.py`
  still reads `effect.get("on")` — switch to `roll`.
- **P-2** Side initiative is **one d20 per side** (§6.1: the side's best modifier, ties to
  players, *Alert* = advantage on the party's roll). `combat.py`'s docstring still says
  "party's best d20+Dex vs one enemy roll" — if that means best-of-four, change it.
- **P-3** Bosses take a turn at the **top of every round** plus one in their side's half,
  and "boss resolve" (§6.2) replaces the v0.1 stun-only rule. Morale: standard foes at
  first Bloodied; the leader-falls trigger is for minions only.
- **P-4** New effect types and keywords are in §1.4a; everything the yaml uses is listed
  there, and `test_facets_d20_data.py::TestEffectsFollowContract` fails if the yaml ever
  uses one that isn't.

## Planner → engine: the Amendment 2 revision (Designer, 2026-09-28)

The yaml already carries the tracks schema (§1.2); the engine's current `track_ranks`
(build.py, "Engine reading … Q-2") reads it almost exactly right. What remains, in order:

- **P-5 Answer to Q-2 (binding, §1.2 steps 1–6).** Ranks carry `main: true|false`. Read
  the flag instead of the hard-coded `SECONDARY_STEEL_KEEPS`: a rank applies iff
  `depth ≥ rank.depth`, `level ≥ rank.level`, and (`not rank.main` or the track is main).
  With today's yaml that gives the same result as the engine's reading (secondary Steel
  → martial weapons only; secondary Spell → Spellcasting, Half table, one domain), but the
  flag is the contract. **Scaling depth counts every talent of the track, main or not**:
  a secondary track's talents still unlock their 5th-level lines at depth 2 (a 2/2 build's
  Spell talents grow at 5th; none of its talents reach 9th).
- **P-6 `facet_weight` (E3, V27) is not implemented yet.** `main_track` must add
  `tracks.facet_weight[facet]` (Body: `{steel: 2}`) before comparing: Body with two Spell
  talents and no Steel talent is a tie → Steel main → Half table. Today the engine makes
  *body_caster* a Full caster (measured +66–78% over the median at 9th–10th). Test: Body,
  `{1: channel, 3: wider_study}`, level 5 → `progression == "half"`, slots `[4, 2]`.
- **P-7 `main_track` with no tracked talent** returns None today; that's fine (no ranks),
  but with a `facet_weight` it must return Steel for Body (martial weapons are already
  Body's; nothing changes on the sheet).
- **P-8 Tradition for Body casters** comes from the build's `tradition:` field (engine
  already reads `picks.tradition`); `check()` must error when a Body build has a Spell
  talent and no `tradition`, and when any domain's tradition differs from it.
- **P-9 Prismatic gate (§1.2 step 5).** `check()`: the number of chosen domains with
  `prismatic: true` must be ≤ the number of applicable `domains` effects with
  `prismatic: true` (0 below Spell depth 3 or when Spell isn't main). `from_entry`
  already adds `deep_domain` only when Deep Magic applies — keep that. Tests: a Soul
  caster at 3rd with `domain: fate` is illegal; the Oracle at 5th has Fate.
- **P-10 No `casting` effects on talents any more** (V23). Keep the talent-`casting`
  branch in `_casting_sources` only for the SRD baselines file if it needs it; the Facets
  data never uses it. `requires: {casting: any}` is gone from *Wider Study*.
- **P-11 Smite spells removed from the lists and from `sim_spells`** (V24). The SRD
  baselines (`software/facets_d20/data/srd_baselines.yaml`) list *Divine Smite* and
  *Searing Smite* for the Paladin baseline and take their models from the main
  `sim_spells`: move those two entries into `sim_spells_extra` there, verbatim:
  `{name: Divine Smite, level: 1, model: weapon_rider, dice: 2d8, upcast: 1d8, damage_type: radiant, action: bonus}`
  and `{name: Searing Smite, level: 1, model: weapon_rider, dice: 1d6, upcast: 1d6, damage_type: fire, action: bonus}`.
  Otherwise the Paladin baseline silently loses its smite. Q-1 is moot for Facets data
  (no smites) and stays "yes" for the baselines.
- **P-12 `casting.domains_on_path` is gone** from the spells yaml (replaced by
  `domains_from: tracks`, `prismatic_from: deep_magic`). The engine already counts
  domains from ranks when `tracks` exist (`_domain_count`), so nothing double-counts;
  `data._normalise_spells`' `setdefault("domains_on_path", 1)` is now dead for the Facets
  data — remove it when convenient. Check kept by the harness: the Priest at 5th has
  exactly 3 domains (the_tide, presence, the_living_world).
- **P-13 `kit_by_level`** (dict-merged into `kit` from that level) is already read by
  `from_entry`; `check()` validates armor against the proficiencies *at that level*, which
  is what the presets need (the Tinker buys a breastplate at 3rd; *battle_priest_deep*
  drops to scale mail at 9th when heavy armor training lapses).
- **P-14 Veteran** (`steel` depth 3, main) adds `hp_per_level: 1` and
  `damage_bonus: {value: 2, weapon: any}` — a flat per-hit bonus like Rage's, **not** a
  rider (E1 does not count it).
- **P-15 Balance band item 7** (§8): read `balance.roles`, `balance.tradition_casters`
  and `balance.hybrid_rule` and report, from 4th level, per hybrid: PI ÷ best pure PI of
  its Facet, and (if Steel main) DPR₁ ÷ best pure-martial DPR₁ of its Facet, DPR₃ ÷ best
  pure-caster DPR₃ of its tradition, each against the tolerance. Add the verdict column to
  the report's §8 tables. `role:` on sim builds is informational.
- **P-16 Pinned preset numbers change.** `test_facets_d20_engine.py::PRESET_NUMBERS`
  must be re-derived (Veteran HP, the Monk/Rogue/Tinker/Wizard/Druid/Oracle/Oathsworn
  picks, kit_by_level weapons). The Designer's harness gives, as (HP, AC, to-hit with the
  kit's first weapon at that level, save DC, slots), with V21's default ability picks:

  ```python
  "fighter": {1: (12, 19, 6, None, []), 4: (36, 19, 7, None, []), 7: (75, 19, 8, None, []), 10: (105, 19, 10, None, [])},
  "rogue": {1: (12, 14, 5, None, []), 4: (36, 15, 6, None, []), 7: (67, 16, 8, None, []), 10: (94, 17, 10, None, [])},
  "barbarian": {1: (12, 14, 5, None, []), 4: (41, 14, 6, None, []), 7: (75, 14, 7, None, []), 10: (105, 14, 9, None, [])},
  "monk": {1: (12, 15, 5, None, []), 4: (36, 16, 6, None, []), 7: (60, 16, 8, None, []), 10: (95, 17, 10, None, [])},
  "wizard": {1: (8, 12, 1, 13, [2]), 4: (26, 12, 1, 14, [4, 3]), 7: (44, 12, 2, 15, [4, 3, 3, 1]), 10: (73, 12, 3, 17, [4, 3, 3, 3, 2])},
  "investigator": {1: (9, 17, 5, None, []), 4: (27, 17, 6, None, []), 7: (53, 17, 7, None, []), 10: (84, 18, 10, None, [])},
  "loremaster": {1: (7, 12, 3, 13, [2]), 4: (22, 12, 3, 14, [4, 3]), 7: (37, 12, 4, 15, [4, 3, 3, 1]), 10: (52, 12, 5, 17, [4, 3, 3, 3, 2])},
  "tinker": {1: (7, 13, 4, 13, [2]), 4: (27, 19, 5, 14, [3]), 7: (53, 19, 6, 15, [4, 3]), 10: (74, 19, 7, 17, [4, 3, 2])},
  "priest": {1: (10, 16, 3, 13, [2]), 4: (31, 16, 3, 14, [4, 3]), 7: (52, 16, 4, 15, [4, 3, 3, 1]), 10: (84, 16, 5, 17, [4, 3, 3, 3, 2])},
  "druid": {1: (10, 15, 1, 13, [2]), 4: (31, 15, 1, 14, [4, 3]), 7: (60, 15, 2, 15, [4, 3, 3, 1]), 10: (84, 15, 3, 17, [4, 3, 3, 3, 2])},
  "oracle": {1: (9, 16, 1, 13, [2]), 4: (27, 16, 1, 14, [4, 3]), 7: (45, 16, 2, 15, [4, 3, 3, 1]), 10: (63, 16, 3, 17, [4, 3, 3, 3, 2])},
  "oathsworn": {1: (12, 18, 5, None, []), 4: (36, 18, 5, 13, [3]), 7: (60, 19, 7, 14, [4, 3]), 10: (84, 19, 8, 16, [4, 3, 2])},
  ```

  Derive them yourself from the engine once P-5–P-14 land and pin what the engine says;
  where it disagrees with this list, tell the Designer which is wrong. (The test reads the
  first weapon of `kit`, not of the level's merged kit: for the Tinker at 4th+ the first
  weapon is the rapier from `kit_by_level`.)
- **P-17 Tests that the schema change affects.** In `test_facets_d20_engine.py`:
  `TestAuditExploitBuilds::test_v01_battle_priest_is_illegal` and `…spellblade…` build
  `Picks(path="spell", …)` — still errors ("no paths"), so they pass, but they now test
  the wrong thing: replace them with the tracks versions — the v0.1 Battle Priest shape
  (Soul, `{1: sworn_strike, 3: channel, 5: weapon_expert}`) is **legal** and at 5th has
  Extra Attack and the Half table, never Full; a 2-Spell/1-Steel Soul at 5th has the Full
  table and no Extra Attack and can't wear chain mail. The `mini_no_paths` fixture's
  talent-borne `casting`/`extra_attack` (engine E-7 era) no longer matches the data
  contract; keep it only if the engine still supports talent-borne ranks for the
  baselines. `PRESET_NUMBERS` per P-16.
- **P-18 Re-run** `tools/d20_sim.py all` after P-5–P-15 and replace §8.1's table with the
  report's; flag any hybrid that fails item 7.

Resolved. Return to the engine agent to continue from P-5.
