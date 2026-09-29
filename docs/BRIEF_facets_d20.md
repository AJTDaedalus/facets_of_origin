# BRIEF — Facets d20 (the third ruleset option)

*Brain output, 2026-09-27. Owner request (verbatim): "a third 'facets' option, taking
the pathfinder-like approach of basing it off of opend20 rules, hedging close to D&D,
but putting our own spin on it. In our case, our spin is facets giving flexibility to
where instead of classes you build a character how you want and play them with an RP
focus (spirit facet can be druid, oracle, or priest depending), as well as keeping
rules easy to pick up and combat not overly long."*

## 1. Problem and motivation

The project now has two rulesets: v0.3 (2d6, Conditions, no HP — pinned at tag
`pre-lean-facets`) and Lean Facets v1.0/v1.1 (2d6, HP, talents — on `feat/lean-facets`).
Both ask a table to learn a new engine. The owner wants a third option a D&D table can
sit down with tonight: familiar d20 chassis, so players bring what they know, with the
Facets idea doing the one job classes do badly — letting a character be the person the
player imagined rather than a row in a class table.

Pathfinder is the precedent: it took an open d20 reference document and changed what it
thought was wrong. Our "what's wrong" is narrower: **classes are fences, the rules are
heavier than a first-time table needs, and fights run long.**

## 2. Goals

1. **D&D-literate in ten minutes.** A 5e player reads one page of "what's different"
   and plays. d20 + modifier vs DC, six abilities, AC, HP, proficiency bonus,
   advantage/disadvantage, spell slots, short/long rest — all kept.
2. **Facets instead of classes.** Three Facets — **Body, Mind, Soul** (the owner's
   "spirit facet" is the Soul Facet) — own the numbers (hit die, saves, armor/weapon
   training, spellcasting progression). Inside a Facet you **build**: every level you
   take a talent from your Facet's menu. **Preset classes are suggested builds, not
   fences** — a Soul character can be a Priest, a Druid or an Oracle depending on which
   talents and which tradition-flavour they take, and a custom build is equally legal.
3. **RP focus.** Backgrounds with a Specialty; **Sparks** (earned for playing your
   character's drives, spent for advantage or a reroll); social scenes resolved with the
   same d20 and rewarded as well as fights. The Mirror Master (MM) — never GM/DM.
4. **Easy to pick up.** One core roll. No feats-as-separate-subsystem (talents ARE the
   feats). No multiclass rules (cross-Facet talents replace them). Levels **1–10** only.
   A player-facing rules book target of ~40 printed pages, not 300.
5. **Combat not overly long.** Target **3–4 rounds** for a standard fight. Levers
   (decided below): side initiative, morale at Bloodied, fixed monster damage, minions,
   bounded HP growth, one reaction, no attacks-of-opportunity bookkeeping beyond one
   rule.
6. **Converts cleanly.** SRD monsters and adventures run with light-touch conversion
   (a one-page MM conversion note). This also makes the Oraga Night 5e edition
   (parallel track, `docs/BRIEF_oraga_5e.md`) a stepping stone rather than a detour.

## 3. Non-goals

- Not a 5e clone with renamed classes. If a rule survives unchanged it is referenced by
  the SRD, not re-explained at length.
- No levels 11–20, no epic tier, no 6th–9th level spells.
- No software engine work in this pass. CLAUDE.md's sync rule binds **the core PHB**;
  Facets d20 is an *option* living in its own tree. A machine-readable
  `facets_d20/data/facets_d20.yaml` (talent menus, progression table) is in scope so a
  later engine pass has a source of truth; the engine is not.
- Not replacing Lean Facets. Three options coexist until the owner picks.
- No new Shattered Origin / Val'loh lore. Setting-neutral rules text; examples may use
  the established cast (MM, Zahna, Mordai, Zulnut — see `references/phb-examples.md`).

## 4. Approach selected

### 4.1 Licence base — SRD 5.2.1 under CC BY 4.0 (decided)

"Open d20" has three candidate bases:

| Base | Licence | GPLv3-compatible? | Verdict |
|---|---|---|---|
| **SRD 5.2.1** (2024 rules) | CC BY 4.0 | Yes (FSF lists CC BY 4.0 as GPLv3-compatible, one-way) | **Selected** |
| SRD 5.1 (2014 rules) | CC BY 4.0 (since 2023) | Yes | Acceptable fallback; prefer 5.2.1 terms |
| d20 SRD 3.5 (Pathfinder's base) | OGL 1.0a | No — OGL's Product Identity and "no other terms" clauses conflict with GPL | Rejected as a text source; *ideas* only |

Consequence: every book in `facets_d20/` carries the SRD 5.2.1 attribution statement
(§4.6). We may quote and adapt SRD text; we never pull from non-SRD WotC material
(non-SRD subclasses, monsters, settings, named spells outside the SRD).

### 4.2 Chassis kept from the SRD

Six abilities (Str/Dex/Con/Int/Wis/Cha) and their modifiers; point buy or standard
array; proficiency bonus (+2 at 1–4, +3 at 5–8, +4 at 9–10); skills (SRD list — keep
it, D&D players expect it); AC; HP; saving throws; advantage/disadvantage; conditions
(SRD list, referenced not re-written); spell slots and SRD spells up to 5th level;
short and long rests; SRD equipment.

### 4.3 The spin — Facets, talents, builds

- **Choose a Facet at level 1.** It sets: hit die (Body d10, Soul d8, Mind d6),
  two saving-throw proficiencies, armor/weapon training, skill picks, and the
  **talent menu** you draw from. It also sets your caster access: Body = none by
  default (canon: Body has no magic tradition), Mind = **Thaumaturgy** (scholarly,
  Intelligence), Soul = **Invocation** (intuitive, Wisdom *or* Charisma — the player's
  choice at the talent that grants it; this is what lets Soul be Priest, Druid or
  Oracle from one menu).
- **Talents** are the only build currency. You take **two at level 1 and one at every
  level after** (so 11 by level 10). Each Facet menu has ~20 talents in three tiers
  (tier 1 from level 1, tier 2 from level 3, tier 3 from level 6); some have
  prerequisites (one earlier talent), none has more than one.
- **Spellcasting is a talent chain, not a class.** "Invocation"/"Thaumaturgy" talent
  grants cantrips + slots on the **single shared caster table** (full-caster slots to
  5th-level spells at level 9). A half-investment talent path gives half-caster slots
  (for the paladin-ish Soul warrior or a Body character who cross-trains). No
  third-caster maths.
- **Spell lists by domain, not class.** Spells come from the SRD, grouped into the
  project's existing magic domains (see `player_handbook/Appendix_Magic_Domains.md`)
  so a Druid (Soul, domains e.g. growth/beasts/weather) and a Priest (Soul, domains
  e.g. healing/protection/light) pull different spells without two class spell lists.
  Each caster picks **two domains** at their first spellcasting talent (a talent can add
  a third). Curate: ~8–15 SRD spells per domain, levels 0–5.
- **Cross-Facet talents** replace multiclassing: from level 2, any tier-1 talent of
  another Facet may be taken at the cost of one talent pick (no penalty beyond the
  opportunity cost); tier 2+ of another Facet requires two talents already taken from
  that Facet.
- **Preset classes** (build cards: concept line, ability priority, level-1 talents,
  recommended picks to level 5, kit): four per Facet, twelve total. Must include the
  owner's three Soul examples. Recommended set:
  - Body: **Fighter, Rogue, Barbarian, Monk** (Body's non-magic canon holds; the
    paladin/ranger shapes are Body↔Soul cross-builds, shown as worked examples)
  - Mind: **Wizard, Artificer-style "Tinker"** (only if SRD-safe wording),
    **Investigator, Bard-style "Loremaster"**
  - Soul: **Priest, Druid, Oracle, Paladin-style "Oathsworn"** (amended 2026-09-27:
    the Oathsworn is a non-caster — full slots on top of heavy armor, Extra Attack and
    a smite was too much for one card; see DESIGN §7)
  Final names are the drafter's call inside these shapes, but "Priest", "Druid",
  "Oracle" are required verbatim. (Druid, Bard, Paladin, Monk, Fighter, Rogue, Wizard,
  Barbarian are SRD class names and safe.)
- **Signature** at level 3: each Facet has six; one per character; a big identity
  ability (kept from Lean — the level-3 "commit" moment the Oraga module already
  references).

### 4.4 RP layer

- **Background** (SRD 5.2 shape: ability bumps, two skill proficiencies, a tool, an
  origin talent — but our origin feat slot is a tier-1 talent from **any** Facet) plus a
  **Specialty**: a narrow fictional expertise; when it applies, the roll has advantage.
  This is the RP-first hook: one line the player wrote does real mechanical work.
- **Drives**: two short sentences per character (a want, a line they won't cross).
- **Sparks**: start each session with 1, cap 3. Earn one when a Drive costs you
  something, on a nat-1 you narrate gracefully, or at the MM's call for a great moment.
  Spend: advantage on a roll *before* rolling, reroll after, or +1d6 to an ally's roll
  you help narrate. (Replaces Inspiration.)
- **Social rules**: one page — attitude track (Hostile/Wary/Neutral/Friendly/Ally),
  a check shifts it one step, Specialty/leverage grants advantage. No social HP.

### 4.5 Short-combat levers (all adopted)

1. **Side initiative.** Players act in any order they like, then enemies, then players.
   First side is decided by one d20 contest (or by surprise). Kills initiative tracking.
2. **Bloodied & morale.** Every non-boss enemy at or below half HP checks morale (a
   flat DC 10 Wis save, or auto-breaks if its leader falls) — breaking means flee,
   surrender, or bargain. Fights end when the *will* breaks, not the last HP.
3. **Fixed monster damage** (the SRD average), rolled only for crits.
4. **Minions**: 1 HP, never take damage on a successful save, fixed damage — groups
   stay cheap to run.
5. **Bounded PC HP**: max hit die + Con at 1st, then fixed average per level (no
   rolling). Levels cap at 10 so HP never balloons.
6. **One reaction**; opportunity attacks kept only as "leaving a foe's reach provokes"
   — one sentence.
7. **Boss rule**: a boss acts **twice per enemy phase** and has a Bloodied phase
   change. That is the whole solo-monster rule (no legendary actions, no lair actions).
8. **Round-count guidance for the MM**: encounter-budget table tuned so a Standard fight
   is 3–4 rounds for a party of four.

### 4.6 Attribution text (required in every book of this option)

> This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1")
> by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1
> is licensed under the Creative Commons Attribution 4.0 International License,
> available at https://creativecommons.org/licenses/by/4.0/legalcode.

## 5. Tool / format decisions

- Tree: `facets_d20/` at repo root (outside `player_handbook/`, `mm_manual/`, `bestiary/`,
  `adventures/` so the Lean invariants in `test_docs_consistency.py` do not bind it).
  Files: `README.md`, `01_What_Is_Different.md`, `02_Characters.md`,
  `03_Facet_of_the_Body.md`, `04_Facet_of_the_Mind.md`, `05_Facet_of_the_Soul.md`,
  `06_Backgrounds_Sparks_and_Social.md`, `07_Magic.md` (domains → SRD spell lists),
  `08_Combat.md`, `09_Mirror_Masters_Guide.md` (encounter budget, morale, minions,
  bosses, converting SRD monsters), `10_Quick_Reference.md`,
  `data/facets_d20.yaml`.
- Markdown, same house conventions as the PHB (numbered tables `Table N–k:`, MM term).
- Tests: `software/tests/test_facets_d20_data.py` — the YAML parses; every talent named
  in a preset card exists in its Facet menu (or is marked cross-Facet); every spell in a
  domain list is an SRD 5.2.1 spell of level ≤5 (listed in the yaml); tier/level
  prerequisites are satisfiable by each preset's recommended picks. TDD per CLAUDE.md.

## 6. Downstream robustness

- **Balance anchor**: a preset at level N should match an SRD class at level N within
  ~±10% on the numbers that matter (HP, attack bonus, damage/round, slot count). The
  drafter records the comparison for Fighter/Rogue/Wizard/Priest at levels 1, 5, 10 in
  `docs/DESIGN_facets_d20.md`.
- **Dominant-pick risk** (Lean's Sentinel problem): no talent may be strictly better
  than another at the same tier; a reviewer pass checks for it.
- **Spell creep**: capping at 5th-level spells removes the worst SRD offenders
  (wish-tier, mass teleport, raise dead remains at 5th — keep, it's RP-useful).
- **Lore**: Invocation/Thaumaturgy names are canon; nothing else setting-specific.

## 7. Open questions handed to Planner / owner

1. Point buy vs standard array default (default: standard array printed, point buy
   allowed).
2. Should Body get a single "no-spells, but" compensation (e.g. extra talent at 1st)?
   Default: yes — Body takes **three** talents at level 1; drafter confirms in the
   balance table.
3. Does the Oraga Night 5e edition become the first Facets d20 adventure later? Not now.

Resolved enough to plan. Return to Planner/Worker to continue from
`docs/DESIGN_facets_d20.md` (to be written) and `facets_d20/`.

---

## Amendment 1 — owner rulings after the critical audit (2026-09-28)

Resolves `docs/AUDIT_facets_d20.md`. These override anything above that conflicts.

1. **Simpler than 5e — measurably.** "It must be simpler than 5e, though 5e isn't as
   complex as 3.5 so it doesn't need to be orders of magnitude." "Iterate on this until
   you get it right." Targets, measured and recorded each iteration:
   - Character creation from a preset: **≤ 12 decisions**; custom: **≤ 18** (SRD cleric ≈ 18).
   - Levelling: a level-up is **one choice at most** (many levels are zero choices).
   - **≤ 5 exception rules** in the whole player book; **one mechanic per job**
     (one way to add a die, one way to get advantage, one reroll).
   - A fresh reader who knows 5e can build a character from 01+02 alone.
2. **Encounters use tables, the way the DMG does** — our own difficulty tables for
   Facets d20, built for the baseline party of **four 4th-level characters**, with a
   by-level table 1–10 and simple adjustment options ("five players: add X"; "three
   players: remove Y"; "the party is tired: …"). Derived from simulation, not asserted.
3. **Balance by simulation.** Build a real rules engine and combat simulator and use
   them: every preset and every flagged combo build lands within a moderate band of the
   others and of the SRD baselines at levels 1, 4, 7, 10. Show the numbers.
4. **Magic is flexible.** Both traditions must offer area damage and the classic
   evocation shapes; a wizard-shaped Mind caster can cast a fireball. Less structure,
   not more: prefer fewer, broader domains or a shared core list over narrow lists
   that trap a 1st-level choice.
5. **Concepts are free; mechanics are ours.** Rewrite every talent that mirrors a
   non-SRD feat or subclass feature as an original mechanic. Generic fantasy concepts
   (a tough fighter, a sharpshooter, a shapeshifting druid) stay.
6. **Tests test rules.** Replace wording checks with direct rule tests driven through
   the engine: computed HP, attack bonus, save DC, slots, damage per round, build
   legality, encounter outcomes, the exploit builds from the audit staying inside the
   band.

Consequence for the chassis: the Planner may cut, merge or restructure talents,
signatures, domains and Facet features freely to meet (1), provided the owner's spin
survives — Facets not classes, build freedom, Soul → Priest/Druid/Oracle by picks, RP
focus, short fights.

## Amendment 2 — owner rulings (2026-09-28, second round)

1. **No Steel/Spell path.** Owner: "We need to find a way, like 5e does, to make it to
   where you can be a full caster, a hybrid, or a melee user while still being balanced
   *inside the choices you make*. The 'jack of all trades, master of none' balance tends
   to work in D&D where picking heavy armor and extra attack means you won't be able to
   pick the things that make magic powerful, the trade off holds the constraints."
   → Balance must come from **opportunity cost inside the talent budget**, not from a
   gate. A character invests picks in magic, in steel, or splits them; a hybrid is
   genuinely viable but masters neither; a pure build of either kind is the strongest at
   its thing. No "you can't take X" rules. Verified by simulation across pure caster,
   pure martial and hybrid builds of every Facet.
2. **Prismatic domains open from 1st level** in Facets d20 (d20 only; the core rules and
   canon are unchanged).
3. **Mordai's Drives are canon** as drafted: *protect people who can't protect
   themselves*; *never leave a fight while someone weaker is still in it*. The "eleven
   years" detail is still removed. Zulnut's invented details stay removed.
4. **v0.3 books go in the tree** as a read-only snapshot, `rulesets/v0.3/`.
5. **4th and 8th level:** one pick: +2 to one ability, +1 to two, or one extra knack
   (DESIGN v0.2 V21).

## Amendment 3 — owner rulings (2026-09-28, third round)

1. **Prismatic domains are the Deep Magic reward** (DESIGN v0.2 §5.1 option a): they
   open only through Deep Magic, the third Spell talent on a caster's main track (from
   5th). The Oracle starts on Presence with *Turn the Odds* and gains Fate at 5th.
   Supersedes Amendment 2 item 2 ("open from 1st").
2. **Ranks lapse.** The main track is always recomputed from current talents; shifting
   investment changes what a character is best at, and the builder shows it before the
   pick is confirmed.

## Amendment 4 — owner rulings on the balance pass (2026-09-28)

1. **A standard day is three Clashes**, with a short rest after the first and second.
   Four Clashes is described as a hard day.
2. **Monster pricing:** add a per-monster threat appendix (Table 9–2) generated by the
   engine from each SRD 5.2.1 stat block, plus the interim rule "a group of hard-hitting
   monsters counts as the next tier up".
3. **Presets stronger than their SRD classes is accepted:** heroic and forgiving. The MM
   guide notes that published 5e adventures may need slightly tougher encounters.
4. **Bosses have twice their stat block's HP** (V-rule kept).

## Amendment 5 — owner rulings after the fresh-eyes playtests (2026-09-28)

Context: the fresh player found the build freedom thin ("a class you assemble from five
cards") and the even levels empty.

1. **Edges.** Keep the five talents at 1/3/5/7/9 and add a small combat or utility pick,
   an **edge** (feat-sized, clearly smaller than a talent), at 2/4/6/8/10, alongside that
   level's knack or ability pick. The simulator re-checks the balance band with edges.
2. **Even levels** therefore become "an edge, plus a knack or the ability pick".
3. **Simplicity budget amended:** an even-level level-up is two small picks; odd levels
   stay one. Character creation is unchanged (edges start at 2nd). The ≤5 exception
   rules and one-mechanic-per-job targets stand.

## Amendment 6 — owner rulings on the playtest fix pass (2026-09-28)

1. **Preset names stay familiar** (Fighter, Rogue, Wizard…) for the first human table;
   revisit afterwards. (PQ-1)
2. **Talking can end a foe's fight:** a foe moved to Neutral or better stops fighting, as
   if broken. Watch it at the first human table; the fallback is "only against a Bloodied
   foe". (PQ-4)
3. **Hard hitters:** the measured mark-up (×1.06 at the fix pass, ×1.07 after edges; regenerated each run) in Table 9–2 and Recharge pricing replace
   Amendment 4 item 2's "next tier up" rule of thumb. (PQ-2)
4. **The Tinker** takes Weapon Expert at 1st and Clockwork Guardian at 3rd (PQ-3:
   adopted on the fix pass's recommendation; not put to the owner separately).
