# RESEARCH — Facets d20 dominant-pick audit

*BRIEF §6 "dominant-pick risk" check, 2026-09-27, branch `feat/facets-d20`. Scope: the
three talent menus in `facets_d20/03–05` and `data/facets_d20.yaml`, plus cross-Facet
dips. Precedent: Lean Facets' *Sentinel* (`docs/REVIEW_lean_design.md` M1), where one
unlimited talent made itself every Guardian's pick and made a whole choice irrelevant.*

## Method

- **Criteria.** *Dominated*: another talent at the same or a lower tier does the same
  job at least as well on every axis. *Dominant*: so strong that every build of the
  Facet (or every build of a role) takes it. *Trap*: never worth a pick against the
  obvious alternative. *Dip*: a tier 1 talent of another Facet that every build should
  buy for one pick.
- **Axes.** Damage per round against AC 14 (DESIGN §6 method: hit chance
  (21 − (14 − bonus))/20, 5% crit), action economy, defense, control, utility.
- **Day.** Four fights of about 3.5 rounds and two short rests (14 rounds), matching
  09's budget assumptions. A per-rest resource is converted to damage per round over
  that day.
- **Baseline.** A typical own-Facet pick is worth about +10–18% damage (ASI ≈ +10%, a
  second *Fighting Style* such as Dueling ≈ +17%). A pick that is worth 2× that, with
  no matching cost, is a problem.
- **Signal.** A talent that all four presets of one Facet take is a red flag in itself.

## Findings that changed the rules

| # | Talent | Problem | Numbers | Fix |
|---|---|---|---|---|
| F1 | *Sworn Strike* (Soul T1) | **Dip.** Uses = proficiency bonus, so a Body fighter with Cha 8 gets the Oathsworn's full smite for one cross-Facet pick at 2nd. | Fighter, 5th: 3 uses + 2 short-rest returns × 3d8 = 67.5/day ≈ +4.8/round, **+32%** over the SRD fighter's 15.2. 10th: 6 × 4d8 ≈ +7.7/round, **+40%**. Best own-Facet alternatives: Dueling +17%, ASI +10%. | Uses = **Soul modifier (minimum 1)**. A Body dip with Wis/Cha +1 gets 1 use (≈3 a day with short rests): +19–20%, the same as a *Fighting Style*. The Oathsworn (Cha 15, +2) keeps 2 uses at 1st–4th; with the natural ASI order (Str to 20, then Cha) it matches its old proficiency-bonus count at every level except 5th–6th (2 not 3). |
| F2 | *Radiant Strikes* (Soul T3) | **Dominant** for any melee character with *Sworn Strike*, and the payoff of the dip above. +1d8 on every hit from 6th (SRD paladin: 11th). | Oathsworn 10th (Str 20, longsword, two attacks, p 0.8): 16.1 base + 7.2 Radiant + 4.1 Sworn ≈ 27.4 vs SRD paladin ≈ 24.6 (**+11%**). Body fighter with Sworn + any Soul T1 + Radiant: ≈ +54% over the SRD fighter for three picks. | **Once on each of your turns.** Oathsworn 10th ≈ 24.5 (parity with the SRD paladin). The Body dip's Radiant pick falls to ≈ +4/round, in line with a T3. |
| F3 | *Aura of Resolve* (Soul T3) | **Dominant.** SRD Aura of Protection, open to every Soul character with no prerequisite; it was the only open T3 for most builds. **All four Soul presets took it.** | +3 to +5 on every save for the party within 10 ft. Nothing else on any menu touches party saves at that size. | **Prerequisite: *Interpose*.** It becomes the protector line's capstone (stand in front, and they stand firm). Oathsworn keeps it (Interpose at 3rd). Priest now takes *Interpose* at 9th and *Aura* at 10th (replacing an ASI that §6 doesn't model). Druid 10th → *Interpose*; Oracle 10th → *Channel*. |
| F4 | *Anticipate* (Mind T2) | **Dominated** by *Glimpses* (Soul T1, a legal cross pick) and by *Well-Timed Word* (Mind T1). | *Glimpses*: same uses (PB/long rest), no reaction, any creature's any d20 test, advantage or disadvantage, 60 ft. *Anticipate*: PB/long rest, reaction, studied target's attacks only, disadvantage only, 30 ft. *Well-Timed Word*: Int-mod uses per **short** rest (≈3× the daily uses), 60 ft, attacks/checks/damage. Two presets (Investigator, the Physician build) spent their 3rd-level pick on it. | **No use limit** beyond the one reaction a round. Now the unlimited-but-narrow option (one studied creature, one attack a round), the Mind cousin of *Protection* and *Uncanny Dodge*. Not Sentinel: a boss making four to six attacks a round has one of them at disadvantage. |
| F5 | *Unarmored Defense*, Constitution (Body T1) | **Trap.** Body has every armor. For a Strength build it buys less AC than 50 gp of scale mail. | Barbarian card (Str 17, Con 15, Dex 13): AC 13 unarmored vs 15 in scale mail (or 16 in half plate), and still worse at 10th (14 vs 16). The SRD barbarian gets this free; here it costs one of three 1st-level talents. | The Constitution version also grants **advantage on Dexterity saves while unarmored** (the SRD barbarian's Danger Sense). Something armor can't buy; the Wisdom (monk) version is unchanged because *Martial Arts* already needs it. |
| — | *Potent Cantrips* (shared T2) | Consistency, not dominance: yaml summary said "any cantrip", 04/05 say "one of its damage rolls". | — | yaml summary now matches the chapters. |

All six changes are in the chapter and the yaml together, pinned by
`TestDominanceAudit` and a new general check, `TestMenuTablePrerequisites` (every menu
table's prerequisite column and every entry's **Prerequisite** line match the yaml).

## Body (03)

| Talent | Tier | Verdict | Reason | Action |
|---|---|---|---|---|
| Ability Score Improvement | 1 | OK | Baseline pick (+~10%). Front-loading at 1st beats the SRD curve by one point for a few levels; accepted in §6. | — |
| Alert | 1 | OK / weak as a pick | Party-wide no-surprise doesn't stack, and the party already takes its best initiative roll, so a second *Alert* in a party adds almost nothing. Fine as an origin talent. Four presets carry it (Fighter, Barbarian, Oracle, Oathsworn as origin; Monk 2nd, Rogue 7th): a table of preset characters will double up. | Note for the owner; no rule change. |
| Cunning Action | 1 | OK | Competes for the bonus action with Second Wind, *Martial Arts*, Studied Eye, Inspiring Word. Strong origin for casters, not universal. | — |
| Expertise | 1 | OK | Skills only. | — |
| Fighting Style | 1 | OK | Each style is SRD. Dueling/Archery ≈ +17% is the menu's damage yardstick. | — |
| Focus | 1 | OK | Monk chassis; gated by *Martial Arts*. | — |
| Martial Arts | 1 | OK | Monk chassis. | — |
| Rage | 1 | OK | SRD barbarian Rage; medium armor + shield + Rage is the SRD barbarian too. | — |
| Reckless Attack | 1 | OK | SRD. | — |
| Sneak Attack | 1 | Watch | Dice scale with character level, so it's full rogue damage for anyone who takes it. At 1st–4th it roughly doubles any single-attack finesse/ranged build; from 5th the one-attack clause makes it a choice against Extra Attack (§6 Rogue). As a cross pick for Soul/Mind weapon users it lifts them to SRD rogue damage, not past it, now that *Sworn Strike*/*Radiant Strikes* stack less (F1, F2). Can't combine with *Exploit Weakness*, and monks' bonus-action strikes switch it off. | Playtest; see open question 1. |
| Tough | 1 | OK | SRD origin feat; popular (six presets carry it), not dominant. | — |
| Unarmored Defense | 1 | **Trap (Con)** | F5. | **Fixed.** |
| Weapon Mastery | 1 | Watch (tax) | Every weapon Body card takes it by 2nd (Fighter, Rogue, Barbarian). It's the SRD martials' free feature, so taking it keeps parity rather than beating it; skipping it leaves you slightly behind. | Open question 2. |
| Action Surge | 2 | OK | Best offense T2 (≈ one extra turn per short rest), but *Evasion*/*Uncanny Dodge* buy defense and the rogue/monk lines don't want it. Presets diverge at 3rd. | — |
| Evasion | 2 | OK | Narrow (Dex-save areas) but no rival does that job. | — |
| Relentless Rage | 2 | OK | Barbarian line. | — |
| Stunning Strike | 2 | OK | Boss ruling (d) already caps it. | — |
| Uncanny Dodge | 2 | OK | At-will reaction, ≈ half of one hit a round. Strong, SRD. | — |
| Cleaving Blow | 3 | OK | Fires often against minions; once a turn. | — |
| Indomitable | 3 | OK / weak | One reroll a day; answers the Body's save weakness. Different job from *Survivor*. | — |
| Reliable Talent | 3 | OK | Out of combat. | — |
| Survivor | 3 | Watch | SRD Champion 18th, here from 6th. ≈ 7–9 HP a turn while Bloodied, roughly on par with *Uncanny Dodge*. Three Body presets take it, but late (6th, 10th, 10th). | Playtest. |

## Mind (04)

| Talent | Tier | Verdict | Reason | Action |
|---|---|---|---|---|
| Ability Score Improvement | 1 | OK | — | — |
| Expertise | 1 | OK | — | — |
| Exploit Weakness | 1 | Watch | The Investigator's engine; §6 parity. On a **caster** with a crossbow it beats cantrips: Wizard 5th ≈ 9.6 vs *Fire Bolt* 8.3 (+15%); ≈ 12.8 on the Studied Eye turn with advantage. It bypasses the 7th-level gate on *Potent Cantrips* at low levels. Not must-take: it competes with *Studied Recovery* and needs Dex. | Open question 1. |
| Field Medic | 1 | OK | Out-heals *Mending Hands* per day but costs an action and a kit; different job (between fights vs in fight). Party-redundant. | — |
| Gadgeteer | 1 | OK | Int-keyed DC limits it off Mind; similar weight to *Magic Initiate*. | — |
| Magic Initiate | 1 | OK | SRD origin feat shape. | — |
| Martial Training (Mind) | 1 | Watch | A Mind caster buys Soul's armor (AC 12 → 17 with medium armor + shield) for one pick. Popular, possibly near-universal among optimised Mind casters, but it only buys the chassis Soul casters get for free, and the d6 remains. The Tinker card uses it. | Open question 3. |
| Skilled | 1 | OK | — | — |
| Studied Recovery | 1 | OK | SRD Arcane Recovery. | — |
| Thaumaturgy | 1 | OK (by design) | The caster talent; the Investigator shows the non-caster road holds. | — |
| Well-Timed Word | 1 | OK | Strong (SRD Cutting Words at T1), but Int-keyed uses self-limit off Mind, and it spends the reaction. | — |
| Anticipate | 2 | **Dominated** | F4. | **Fixed.** |
| Careful Casting | 2 | OK | — | — |
| Extra Attack | 2 | OK | Needs *Martial Training* and 5th. | — |
| Infuse Item | 2 | OK | Party-facing; +1 items. | — |
| Potent Cantrips | 2 | OK | Gated at 7th (§6). Summary fixed. | yaml summary. |
| Wider Study | 2 | OK | — | — |
| Contingency Plan | 3 | OK | — | — |
| Decisive Strike | 3 | OK | One auto-crit per short rest. | — |
| Empowered Spell | 3 | OK | Once per long rest. | — |
| Iron Mind | 3 | OK | Resilient-style save. Every Mind preset takes it, but last (10th) and the Mind menu's other T3s have prerequisites; that's scarcity at the top, not dominance. | — |

## Soul (05)

| Talent | Tier | Verdict | Reason | Action |
|---|---|---|---|---|
| Ability Score Improvement | 1 | OK | — | — |
| Channel | 1 | OK | Limited uses; heal or damage. | — |
| Font of Life | 1 | OK | Healer line only; a trap only for builds with no healing, which is obvious. | — |
| Glimpses | 1 | Watch | A broader SRD *Lucky* (any creature, any d20 test, no action) for a full pick. Cheap to dip and useful to everyone, but only 2–4 uses a day. It no longer makes *Anticipate* redundant (F4). | Playtest. |
| Invocation | 1 | OK (by design) | — | — |
| Magic Initiate | 1 | OK | — | — |
| Martial Training (Soul) | 1 | OK | Heavy armor adds ≤ +1 AC over medium for a Dex-14 caster. | — |
| Mending Hands | 1 | OK | In-fight bonus-action burst; *Field Medic* is the between-fights heal. | — |
| Silver Tongue | 1 | OK | Social. | — |
| Sworn Strike | 1 | **Dip** | F1. | **Fixed.** |
| Wild Kin | 1 | OK | Social/utility. | — |
| Wild Shape | 1 | OK | SRD shape. | — |
| Beast Heart | 2 | OK | SRD moon-druid numbers. | — |
| Extra Attack | 2 | OK | — | — |
| Interpose | 2 | OK | One reaction a round, so it redirects one hit, not every hit: **not** the Sentinel problem. Now also the gate to *Aura of Resolve*. | — |
| Potent Cantrips | 2 | OK | — | — |
| Prophecy | 2 | OK | MM-gated. | — |
| Wider Study | 2 | OK | — | — |
| Aura of Resolve | 3 | **Dominant** | F3 (all four Soul presets took it). | **Fixed.** |
| Radiant Strikes | 3 | **Dominant** (melee) | F2. | **Fixed.** |
| Twist of Fate | 3 | OK | Spends glimpses; shares their budget. | — |
| Wellspring | 3 | OK | Capped at half max HP. | — |

## Cross-Facet dips

| Dip | Verdict | Why |
|---|---|---|
| *Sworn Strike* → Body/Mind melee | **Fixed (F1)** | Was +32–40% for one pick. |
| *Sworn Strike* + *Radiant Strikes* → Body | **Fixed (F1, F2)** | Was ≈ +54% for three picks. |
| *Aura of Resolve* → anyone with two Soul talents | **Fixed (F3)** | Now needs *Interpose* too (four Soul picks). |
| *Sneak Attack* → Soul/Mind weapon users, casters | Watch | Rogue parity, not above it; one-attack clause. Oathsworn at 3rd–4th with a rapier roughly doubles its at-will damage (≈ 8.7 vs 4.5), then it's the rogue's choice from 5th. |
| *Glimpses* → anyone | Watch | Strong utility; limited uses. |
| *Martial Training* (Mind) → casters of Mind | Watch | Chassis parity with Soul. |
| *Tough*, *Alert*, *Cunning Action*, *Field Medic* as origin talents | OK | SRD origin-feat weight; doesn't cost a pick. *Alert* and *Field Medic* don't stack within a party. |
| *Well-Timed Word*, *Gadgeteer* → non-Mind | OK | Int-keyed; weak off Mind. |
| *Rage*, *Wild Shape*, *Martial Arts* → others | OK | Armor/spell restrictions make them self-limiting. |

## Signatures (spot check, not a pick)

No change. *Deadeye* beats *Champion's Edge* on damage for an archer (+PB a turn vs a
19–20 crit range), but only at range; each Facet's six do different jobs, and one per
character with no respec keeps any imbalance local.

## Balance check (DESIGN §6)

The only §6 preset touched is the **Priest** (9th *Aura of Resolve* → *Interpose*, 10th
ASI → *Aura of Resolve*). §6 models the Priest's ASIs at 4th and 8th only (Wis 20 at
8th), so HP 73 / DC 17 / 9.8 damage at 10th stand. Fighter, Rogue, Wizard and
Investigator picks are unchanged; *Anticipate* stays on the Investigator (§6 note still
true). Druid, Oracle and Oathsworn are not in §6; the Oathsworn now sits at about SRD
paladin damage at 10th (≈ 24.5 vs 24.6).

## Open questions for the owner

1. **Level-scaled riders on cross picks.** *Sneak Attack* and *Exploit Weakness* scale
   with character level, whoever takes them. That's fine for the rogue and the
   investigator; on a caster it quietly beats cantrips by ~15% at 5th. Left alone
   because it lifts to rogue parity, not past it, and BRIEF §4.3 says a cross pick
   has "no penalty beyond the opportunity cost". Playtest before touching it.
2. **Weapon Mastery as a tax.** Every weapon Body card takes it. Folding it into the
   Body chassis would free a pick and change DESIGN §1 ("exactly one Facet feature"),
   so it's the owner's call.
3. **Armored Mind casters.** *Martial Training* gives a Mind caster Soul's AC for one
   pick. Keep (current), or exclude shields from Mind's version?
4. **Alert duplication.** Four presets start with *Alert*; a preset party doubles up.
   Swap one or two cards' origin talents?
