# AUDIT — Facets d20: rules correctness, balance and exploits

*2026-09-27, branch `feat/facets-d20` (PR #32). Read-only audit; nothing else in the
repo was changed. Scope: `facets_d20/*.md`, `facets_d20/data/*.yaml`,
`software/tests/test_facets_d20_*.py`, `docs/DESIGN_facets_d20.md` (§1–§7),
`docs/RESEARCH_facets_d20_dominance.md`, `docs/RESEARCH_facets_d20_srd_check.md`.
Lens: a rules lawyer and a min-maxer working together. Suite state at audit time:
`206 passed`.*

**Method.** All damage figures use DESIGN §6's own method so they compare directly
with Table 6–1: hit chance p = (21 − (14 − attack bonus))/20 against AC 14; crit 5%
(10% on 19–20); a save-based effect uses target save +2, so fail = (DC − 3)/20. Where
a build spends daily resources, I use the dominance audit's "day": four fights of
about 3.5 rounds and two short rests, so **14 rounds**. Resources are spread over
those rounds. SRD 5.2.1 spell behaviour is as printed in the SRD (e.g. *True Strike*,
*Divine Smite*, *Spirit Guardians*, *Goodberry*).

---

## Executive verdict

The core numbers hold together. HP, proficiency, slot tables, tier gates and preset
legality are internally consistent across the chapters, both yaml files and DESIGN §1–§2.
The spell lists in 07 match the yaml exactly: I diffed every domain by name and level.
The dominance audit fixed the single-talent outliers it looked at.

It didn't look at **combinations of talents**, and that's where the game breaks:

1. **A Soul full caster can buy the whole Oathsworn chassis.** Heavy armor, Extra Attack,
   *Sworn Strike*, *Radiant Strikes* and *Divine Smite* sit on top of full-caster
   *Spirit Guardians*, all legal from 1st level. That's about **+50% over the SRD
   paladin at 5th and +100% at 10th**. It makes the Oathsworn a trap, and it removes
   Body's reason to exist at 10th. Ruling (f) said this exact combination was "more
   than we wanted on one card", but the menu hands it to any Soul player who takes
   *Invocation* at 1st. Ruling (a) only closed the late-caster route.
2. **A Mind full caster matches or beats the non-caster Investigator.** *True Strike*
   (Divination, Fate, Chronomancy) makes weapon attacks off Intelligence, and
   *Exploit Weakness* adds rogue dice. That's **+92% over the Wizard preset at 5th**,
   at or above the Investigator at every level, with full spellcasting on top. So the
   Mind "never casts and still keeps up" pillar is dominated by a caster.
3. **The stated balance evidence is partly wrong.** DESIGN §6 models the Wizard with
   *Fire Bolt*, which is on no Thaumaturgy domain. Thaumaturgy has no area-damage
   spell at all; *Fireball*, *Lightning Bolt*, *Shatter* and *Cone of Cold* are all
   Invocation. The "Wizard vs SRD Evoker" parity claim compares against something the
   Mind Facet can't do.
4. **Healing and sustain loops break the adventuring-day maths.** *Font of Life* pays
   out per instance, so *Mending Hands* 1-point pings and *Goodberry* both loop.
   *Field Medic* heals the party for free once per short rest per creature. *Survivor*
   is here at 6th instead of the SRD's 18th. A party with a Priest can run about
   **2.7× the party's HP** in healing per day at 5th, against a budget that assumes
   2–3 fights per long rest.
5. **Boss rules cover stun and nothing else.** Paralysis (*Hold Person*/*Monster*),
   banishment, *Hypnotic Pattern* and *Polymorph* still end a boss fight in one failed
   save. Legendary Resistance's status isn't stated. *Glimpses* can give the boss
   disadvantage on that save.
6. **Several structural rules questions have no answer.** How shared talents count
   toward the cross-Facet "two talents" gate; what a second tradition gives (cantrips?
   which ability sets prepared count?); what happens if the traditions are taken in
   the "wrong" order; how summons and PC-side monsters work under side initiative and
   fixed damage; which of your talents work in Wild Shape.
7. **The tests pin strings and hand-typed copies of the contract, not rules.** The
   caster-level tests exercise a helper defined inside the test file, and the build
   checker disagrees with the book on origin talents. Nothing recomputes §6. Every
   Critical below passes the suite.

**Counts: 3 Critical, 10 Major, 16 Minor.** Fix the Criticals before any playtest
result is taken as evidence about Facet balance.

---

## Findings

### Critical

#### C1 — The Battle Priest: full caster + Oathsworn chassis from 1st level

- **Location.** 05 *Martial Training* (Soul: heavy armor), *Extra Attack*, *Sworn
  Strike*, *Radiant Strikes*; 07 Presence (*Divine Smite*, *Spiritual Weapon*,
  *Spirit Guardians*); 05 sidebar "why the Oathsworn doesn't cast"; DESIGN §7 B
  decision on Oathsworn, Planner ruling (f).
- **Evidence.** Every piece is on the Soul menu with no gate against the others. The
  build (Appendix A1) is Invocation (Cha, Presence + The Tide) and *Martial Training*
  at 1st, *Sworn Strike* at 2nd, *Extra Attack* at 5th and *Radiant Strikes* at 6th.

  | Level | Battle Priest (day avg/round) | SRD Paladin | SRD Cleric | Oathsworn preset |
  |---|---|---|---|---|
  | 5 | **≈ 30.2** | ≈ 20.3 | ≈ 16–19 | ≈ 17 |
  | 10 | **≈ 53.5** | ≈ 26.9 | ≈ 31.4 | ≈ 24.5 |

  It also has AC 20–22 (plate + shield + *Shield of Faith*), Cha-save proficiency,
  *Aura of Resolve* by 9th, and a full caster's *Revivify*, *Mass Healing Word*,
  *Banishment* and *Hold Monster* (with *Wider Study*).
- **Why it matters.** It breaks the ±10% target by +49% and +99%. It makes the
  Oathsworn preset strictly worse than "the same card plus *Invocation* at 1st"
  (cost: *Mending Hands* at 2nd). The 05 sidebar tells players the opposite: "Your
  slots start from the level you take it, not from 1st". And it takes away Body's
  identity: Body's compensation for no magic (a third talent at 1st, free Extra
  Attack, heavy armor) costs the Battle Priest exactly two picks (*Martial Training*,
  *Extra Attack*), and the Priest keeps full casting.
- **Recommended fix** (pick one):
  - (a) *Extra Attack* (Mind/Soul) requires that you **don't** hold your own
    tradition's caster talent. The SRD bladesinger precedent, if you want a softer
    version, is "one of the attacks can be a cantrip".
  - (b) *Martial Training*'s heavy-armor step is barred to full casters.
  - (c) **Preferred:** "a character with their own tradition's caster talent can't take
    *Extra Attack*, *Sworn Strike* or *Radiant Strikes*". That's one line on each
    entry, and the Oathsworn stays the Soul warrior. Add a test that replays the A1
    build and expects it to be illegal.

#### C2 — The Spellblade: a Mind full caster dominates the non-caster Investigator

- **Location.** 04 *Exploit Weakness*, *Studied Eye*, *Martial Training*, *Anatomist*,
  sidebar "the Mind character who never casts"; 07 Divination, Fate and Chronomancy
  (*True Strike*); dominance audit "Exploit Weakness — Watch … needs Dex".
- **Evidence.** SRD 5.2.1 *True Strike* makes one weapon attack using your
  **spellcasting ability** for attack and damage, and adds +1d6 radiant from 5th.
  That's a weapon attack, so *Exploit Weakness* applies; the one-attack clause is no
  cost because *True Strike* is one attack. The audit's mitigation ("needs Dex")
  disappears. Build in Appendix A2 (one-handed quarterstaff 1d6, shield from
  *Martial Training*):

  | Level | Spellblade | Investigator (§6) | Wizard preset (§6) |
  |---|---|---|---|
  | 1 | 7.0 | 7.0 | 3.6 |
  | 5 | **15.9** | 14.1 | 8.3 (+92%) |
  | 10 | **24.8** (26.0 with *Anatomist*) | 23.8 | 13.4 (+85%) |

  It also has full 5th-level slots, *Shield*, *Mage Armor* or medium armor and a
  shield (AC 18–19), and *Decisive Strike* if wanted. A Soul caster gets the same
  pattern: *Sneak Attack* as a cross pick with a dagger, *True Strike* from Fate or
  Divination, and *Glimpses* for advantage. That's the Oracle preset plus one pick.
- **Why it matters.** 04 says "a Mind character who never casts should be as good in a
  fight as one who does. … Neither is carrying the other." Here the caster carries
  both jobs.
- **Recommended fix.**
  - *Exploit Weakness* and *Sneak Attack* only trigger on an attack made with the
    **Attack action**. That cuts *True Strike*, *Contingency Plan* and Ready, and
    keeps opportunity attacks per the SRD.
  - Or the riders scale with levels in the Facet's non-caster line (e.g. "1d6 per two
    talents you hold from this menu").
  - Also settle the dominance audit's open question 1 (level-scaled riders on casters)
    as **fix**, not watch.

#### C3 — DESIGN §6 validates the Mind caster against spells it cannot cast

- **Location.** DESIGN §6 Table 6–1 Wizard row ("Wizard (Fire Bolt) vs SRD Wizard
  (Evoker)"); yaml preset `wizard.domains: [constructed_force, warding]`; 07 domain
  lists.
- **Evidence.** *Fire Bolt* is only on Fire, which is an Invocation domain. The Wizard
  preset's only damage cantrip is *Eldritch Blast* (Constructed Force). It happens to
  give the same expected damage (2 × 0.8 × 5.5 + 5 = 12.8 + 0.55 crit = 13.35 at
  10th), so the number survives by luck. The comparison to an *Evoker* doesn't
  survive. No Thaumaturgy domain has an area-damage spell of 1st–5th level except
  *Glyph of Warding* (set-up only). SRD wizard at 5th, *Fireball* on three targets:
  28 × (0.6 + 0.4 × 0.5) × 3 ≈ **67** per 3rd-level slot. The Mind wizard's best
  3rd-level damage is *Magic Missile* upcast: 5 × 3.5 = **17.5**. *Fireball*,
  *Lightning Bolt*, *Shatter*, *Ice Storm*, *Cone of Cold*, *Flame Strike*, *Spirit
  Guardians* and *Insect Plague* are all Invocation.
- **Why it matters.** The one quantitative balance claim in the PR is invalid for the
  caster Facet it most needs to support. Mind casters are pushed into a second
  tradition (M5) to blast, and then cast those spells off Wis or Cha.
- **Recommended fix.**
  - Redo §6's Wizard row with *Eldritch Blast* and the preset's real 3rd-level options.
  - Add a Thaumaturgy area spell or two where the canon allows. Constructed Force can
    reasonably hold *Thunderwave* or *Shatter*-style force effects; check canon before
    adding.
  - Or state plainly that Thaumaturgy is the control tradition and that its damage is
    deliberately lower. Then say what Mind gets in exchange.
  - Add a test: every spell named in a preset's §6 row or card is on that preset's
    domains.

### Major

#### M1 — *Font of Life* pays per instance: *Mending Hands* and *Goodberry* loop

- **Location.** 05 *Font of Life*, *Mending Hands*; 07 Verdance / The Living World
  (*Goodberry*).
- **Evidence.**
  - *Mending Hands* lets you "restore any number of hit points from the pool" as a
    bonus action, and *Font* adds +2 to each restoration. Out of combat, spend 1 point
    at a time and each point heals 3. That's a 25-point pool → **75 HP** at 5th and a
    50-point pool → **150 HP** at 10th.
  - *Goodberry* is a 1st-level spell with ten berries at 1 HP each, and *Font* adds
    2 + 1 per berry. That's **40 HP per 1st-level slot**, or 160 HP from four slots at
    5th.
  - SRD 5.2.1's Disciple of Life closed this with "on the turn you cast the spell" and
    "with a spell slot". *Font* has neither.
- **Why it matters.** It's a known 5e exploit, reintroduced, and it compounds with M2.
- **Recommended fix.** Once per turn per creature; only when you cast a spell with a
  slot or use *Channel*; for *Mending Hands*, only on a restoration of 5 or more
  points.

#### M2 — *Field Medic* gives unlimited, resource-free healing for an origin talent

- **Location.** 04 *Field Medic*; the budget assumptions in 09 ("about a third of the
  party's health … two or three fights before a long rest").
- **Evidence.** Each creature regains 1d6 + PB + level once per short rest. The
  healer's kit uses aren't mentioned, and no Hit Dice are spent. With the "day" of two
  short rests, each of four PCs can benefit 3 times:
  - 5th level: 3 × 4 × (3.5 + 3 + 5) = **138 HP** against party HP ≈ 152 (91%).
  - 10th level: 3 × 4 × 17.5 = **210 HP** against ≈ 292 (72%).

  The Priest preset carries both this and the M1 loop. Appendix A4 totals **≈ 418
  HP/day at 5th, 2.75× the party's HP**, before *Cure Wounds* or *Healing Word*.
- **Why it matters.** The encounter budget's danger column assumes attrition that never
  happens. A party with this healer can run 6–8 Standard fights per long rest, and the
  MM will have to escalate fights to Deadly to matter.
- **Recommended fix.**
  - *Field Medic*: the target spends one Hit Die and regains that roll + PB + level (the
    SRD 5.2.1 Healer shape).
  - Or limit it to PB uses per long rest.
  - Add a note to 09 that the budget assumes about 1 party-HP of healing per day.

#### M3 — *Survivor* at 6th makes a raging Body character unkillable in Standard fights

- **Location.** 03 *Survivor* (T3), Barbarian preset (6th), dominance audit "Survivor —
  Watch".
- **Evidence.**
  - SRD Champion gets this at **18th**.
  - Barbarian preset at 6th (Con 16): it heals 8 a turn while Bloodied. Rage resistance
    doubles that to **16 effective HP a round**.
  - The Standard danger budget at 6th is 72 across the party if every attack hits. At
    about 50% hits and about half the fire on the tank, incoming is ≈ 18, or ≈ 9 after
    resistance. That's **less than *Survivor* heals**.
  - At 10th: HP 124 (with *Tough*) and 9 a turn healed. The SRD barbarian at 10th has
    115 and no regeneration.
- **Why it matters.** Once Bloodied and raging, the barbarian can't lose a Standard
  fight to bludgeoning, piercing or slashing damage. Morale and a 3–4 round fight make
  it worse: the character never has to stop.
- **Recommended fix.**
  - Make it once per round **only if you took damage since your last turn**, and not
    while raging.
  - Or proficiency-bonus uses per long rest.
  - Or move it to a Body signature (one per character, no stacking with *Rage*).

#### M4 — Shared talents double-count toward the cross-Facet "two talents" gate; checker and book disagree

- **Location.** 02 *Cross-Facet Talents* ("needs you to already have two talents from
  that Facet"; "an origin talent from another Facet counts"); yaml shared talents
  (*Expertise* Body+Mind; *Magic Initiate*, *Martial Training*, *Wider Study*,
  *Potent Cantrips* and *Extra Attack* Mind+Soul); test `build_errors()`.
- **Evidence.**
  - The book never says whether a talent on **your own** menu that is also on another
    menu counts as "from that Facet".
  - Read literally, a Mind caster with *Martial Training* (own) and *Magic Initiate*
    (origin) holds "two Soul talents". That opens *Interpose* at 3rd and *Aura of
    Resolve* at 6th without spending one cross pick.
  - The Wizard preset (origin *Tough*, 2nd *Expertise*) already holds "two Body
    talents", which opens *Uncanny Dodge*, *Evasion* and *Survivor*.
  - The test checker reads it the other way: it excludes own-menu shared talents.
  - The checker also ignores origin talents altogether: they're never added to
    `taken`, although 02 says they count.
- **Why it matters.** The dominance audit's F3 fix (gate *Aura of Resolve* behind
  *Interpose*) can be bypassed. And the only machine encoding of the rule contradicts
  the book in two places.
- **Recommended fix.**
  - Rule: "A talent on your own Facet's menu never counts as another Facet's, even if
    that menu lists it too."
  - Put origin talents into the checker's `taken` list, and add tests for both cases.

#### M5 — Taking the second tradition dominates *Wider Study*, and the rules for it have holes

- **Location.** 07 "A character never has two slot tables…"; 04 Scholar-Priest; 04/05
  *Wider Study*; DESIGN §2.
- **Evidence.**
  - Choosing between them:
    - The other tradition's talent is **T1 from 2nd level** and gives **two** domains
      on the full-caster table you already have.
    - *Wider Study* is **T2 from 3rd** and gives one.
    - For every spell that ignores DC and attack (*Bless*, *Haste*, *Shield*, *Mage
      Armor*, *Revivify*, *Aid*, *Tiny Hut*, *Healing Word*), the second ability is
      irrelevant. So a Mind caster with Invocation (Presence + The Tide), or a Priest
      with Thaumaturgy (Constructed Force + Chronomancy, which gives *Shield*, *Mage
      Armor* and *Haste*), wins outright.
  - Questions the rules don't answer:
    - (i) Does the second caster talent grant its two cantrips ("When you take it,
      you gain … Cantrips")?
    - (ii) Prepared spells = "casting modifier + caster level": which modifier?
    - (iii) Whose caster level? It's defined per talent ("levels you have held this
      talent").
  - An ordering trap: a Soul character who takes Thaumaturgy at 2nd (half caster)
    and then Invocation at 3rd "keeps the table you have" and stays a **half caster
    forever**. A Mind character's order is forced, but a Soul or Body player can walk
    into this.
- **Why it matters.** It makes a T2 talent a trap, invites MAD-free domain hoarding
  ("the widest spell list in the game"), and leaves three table-arguments unresolved.
- **Recommended fix.**
  - The second tradition gives **one** domain and no cantrips.
  - Prepared count uses the first tradition's ability, and caster level counts from
    the first caster talent.
  - "If either of your caster talents is your own tradition's, you use the Full table."
  - Or: *Wider Study* gives two domains.

#### M6 — Bosses can still be ended by one failed save; Legendary Resistance undefined

- **Location.** 08 *Kinds of Foe*; 09 *Bosses* and conversion step 4; DESIGN §3 ruling
  (d).
- **Evidence.** Ruling (d) caps only **stun**. Everything else still works on a boss:
  - *Hold Person* (Binding, 2nd, from caster level 3) on a humanoid boss: paralysed,
    auto-crits within 5 ft.
  - *Hypnotic Pattern* (Illusion, 3rd): incapacitated with no save repeat.
  - *Banishment* (Binding and The Arcane, 4th).
  - *Polymorph* (4th), *Resilient Sphere*, *Wall of Force*.
  - *Hold Monster* (5th).

  09 says to "cross out legendary and lair actions" but says nothing about the
  separate **Legendary Resistance** trait. *Glimpses* (Soul T1) gives disadvantage on
  the boss's save, and *Bane* stacks. A boss held at full HP never reaches its
  Bloodied phase change, which is the design's only other boss safeguard. There is
  partial mitigation: a paralysed boss repeats its save at the end of each of its two
  turns.
- **Why it matters.** The "Boss" pillar (two turns, a Bloodied change, no LR) is
  weaker than the SRD's against control casters at exactly the levels this game covers.
- **Recommended fix.**
  - Generalise ruling (d): "Any effect that would make a boss incapacitated (stunned,
    paralysed, banished, polymorphed, asleep, charmed into inaction…) costs it one of
    its two turns and then ends."
  - Or: "a boss has Legendary Resistance (1/Bloodied phase): when it fails a save, it
    can succeed instead."
  - State explicitly whether SRD Legendary Resistance is kept or crossed out.

#### M7 — Summons, companions and PC-side creatures have no rules under side initiative, fixed damage or the budget

- **Location.** 08 *The Round*, *Attacks and Damage*; 09 budget; 07 *Animate Dead*
  (The Undying), *Animate Objects* (The Constructed Mind), *Find Familiar*,
  *Conjure Animals*, *Giant Insect*, *Polymorph*; 04 *Clockwork Companion*; 05
  *Wild Shape*.
- **Evidence.** 08 says "every creature on that side takes its turn, in any order the
  side likes". Unanswered:
  - Do summons get separate turns anywhere in the order? (SRD 5.2.1 ties most to the
    caster's turn.)
  - Do PC-controlled monster blocks deal fixed or rolled damage?
  - Does the party-size multiplier count them?

  *Animate Dead* builds up across days. With three 3rd-level slots at caster level 6,
  one reassert-4 casting plus two creations gives 6–8 undead by caster level 7 and
  10+ with 4th/5th upcasts. Eight skeletons with shortbows at +4 against AC 14 is
  8 × 0.55 × 5.5 ≈ **24/round**: +50% party damage, and a combat-length problem that
  the 3–4 round target and the minion rules don't touch.
- **Why it matters.** "A standard fight should take three or four rounds" and the
  budget both assume four PCs.
- **Recommended fix.**
  - "A creature you summon or control acts on your turn, immediately after you, and
    deals fixed damage like any monster."
  - "*Animate Dead* controls at most (PB) undead."
  - "Count each summoned combatant as 0.5 PC for the party-size multiplier."
  - "*Wild Shape* keeps your talents and Facet features except spellcasting."

#### M8 — Facet balance at 1/5/10: Soul out-classes both others once it combines lines

- **Location.** 02 Table 2–2, 03–05 menus, DESIGN §6.
- **Evidence** (at-will or day-average damage/round against AC 14, with defence
  notes):

  | Build | L1 | L5 | L10 | Defence at 10 |
  |---|---|---|---|---|
  | Body Fighter (§6) | 5.9 | 15.2 | 19.3 | AC 20–21, 104 HP (124 with *Tough*) |
  | Body Rogue (§6) | 7.0 | 14.1 | 22.7 | 104 HP |
  | Mind Wizard (§6, real cantrip) | 3.6 | 8.3 | 13.4 + control slots | 62 HP, AC 15 + *Shield* |
  | Mind Investigator (§6) | 7.0 | 14.1 | 23.8 | **62 HP (−33% vs SRD rogue's 93)**, AC 19 |
  | Mind Spellblade (C2) | 7.0 | 15.9 | 24.8 + full slots | 62–82 HP, AC 18–19 |
  | Soul Priest (§6) | 2.3 | 5.4 (+ *Spirit Guardians*) | 9.8 (+ SG) | 73 HP, AC 18–20 |
  | Soul Oathsworn | ≈ 4.7 | ≈ 17 | ≈ 24.5 | AC 20, *Aura* |
  | **Soul Battle Priest (C1)** | ≈ 4.7 | **≈ 30.2** | **≈ 53.5** | AC 20–22, 83 HP, *Aura* |

  - **Body's compensation for no magic** is "d10, heavy armor, 3rd talent at 1st,
    free Extra Attack". Soul buys the parts that matter in fights (heavy armor and
    Extra Attack) with two picks. Body's remaining edge over Soul is +1 HP/level
    (+10 HP at 10th, ≈ +12%) and Str/Con saves, which are worse than Wis/Cha against
    the effects that end fights. Body's T3 menu is thin: *Indomitable*, *Reliable
    Talent* and *Cleaving Blow* are narrow, and *Survivor* is overtuned (M3).
  - **Mind non-casters keep up on damage but not durability.** The Investigator is
    outside the ±10% HP band at all three levels (8/10, 32/43, 62/93). §6's verdict
    lists HP parity only for Fighter, Wizard and Priest and doesn't flag this.
  - **Mind casters trail Soul casters** on every chassis axis (d6 vs d8, light vs
    medium + shield, Int/Wis vs Wis/Cha saves) and on damage lists (C3). Mind's real
    compensation is *Shield*, *Counterspell*, *Haste*/*Slow*, *Hypnotic Pattern* and
    *Wall of Force*. That's strong, but §6 doesn't make that case.
- **Why it matters.** It's the core promise of the three-Facet split.
- **Recommended fix.**
  - Fix C1 and C2 first. Then re-run §6 for all twelve presets **and** for the best
    build per Facet (Appendix A). Add a Body T3 worth taking.
  - Consider *Weapon Mastery* as a free Body feature (dominance open question 2). That
    also buys back the pick every Body card spends on it.

#### M9 — Sneak Attack / Exploit Weakness ordering with extra attacks is undefined

- **Location.** 03 *Sneak Attack*, *Cleaving Blow*, Weapon Mastery *Cleave*/*Nick*,
  *Action Surge*; 04 *Exploit Weakness*.
- **Evidence.** "You can't use it on a turn in which you make more than one attack" is
  a whole-turn condition checked **after** the fact. Cases with no answer:
  - A Sneak Attack hit that drops a creature triggers *Cleaving Blow*'s free attack.
    Is the Sneak Attack void? Is the Cleave forbidden?
  - The same question for *Cleave* mastery, the *Nick* extra attack, and an *Action
    Surge* second Attack action.
- **Why it matters.** Rogues and Investigators hit this every session once *Cleaving
  Blow*/*Action Surge* are on the sheet. Rulings will vary by table and the damage
  swing is 3d6–5d6.
- **Recommended fix.** "Once per turn, when you hit with the first attack you make on
  your turn… After you use it, you can't make another attack this turn." It's
  forward-looking, so there's nothing to undo.

#### M10 — Test suite: every Critical above passes; the tests pin strings, not rules

- **Location.** `software/tests/test_facets_d20_data.py`,
  `software/tests/test_facets_d20_spells.py`.
- **Evidence**, with the gaps named:
  - **T1.** `TestCasterLevel` checks `caster_level()` and `slots()`, which are defined
    **in the test file**. It proves the helper agrees with a yaml string
    (`full_table_index: caster_level`), not that any rule or engine does.
  - **T2.** `build_errors()` never adds the **origin talent** to `taken` (02 says it
    counts toward the cross-Facet two), and it silently decides the shared-talent
    question the book leaves open (M4).
  - **T3.** No test checks any rule **number** in the chapters against the yaml:
    - dice: *Sworn Strike* 2d8/3d8/4d8, *Sneak Attack* ceil(level/2)d6, *Channel*,
      *Wild Shape* CRs;
    - uses: *Rage*, *Second Wind*, *Glimpses*, *Inspiring Word*;
    - ranges.

    Summaries are free text. `TestDominanceAudit` pins phrases ("No limit",
    "advantage on Dex saves"), not mechanics.
  - **T4.** `test_every_spell_named_in_chapter` is a whole-chapter **substring**
    search. *Shield* is found inside "Shield of Faith", *Light* inside "Lightning
    Bolt", and *Fear* is on two lists, so a spell dropped from its domain in 07 still
    passes. Levels in 07 are never checked. (I ran the missing check by hand: 07 and
    the yaml currently agree exactly, domain by domain and level by level.)
  - **T5.** DESIGN §6 is hand arithmetic with no test. Nothing checks that a preset's
    modelled cantrip is on its domains (C3 would have failed).
  - **T6.** Chapters 01, 02, 06, 08, 09 and 10 are untested apart from attribution.
    Table 2–2, 2–4, 2–5, 10–1 and 9–1 could all drift from the yaml. (I checked by
    hand: 2–5 and 9–1 are arithmetically right today.) `EXPECTED_NUMBERS` is a hand
    copy of DESIGN §1, so yaml and test can drift together.
  - **T7.** `test_card_picks_match` checks that a pick's name appears **somewhere** on
    the "Picks" line, not at its level ("2nd X · 3rd Y" swapped passes). A card's
    **Domains** line is never compared with `presets[].domains`, and preset domains
    are never checked to belong to the preset's tradition.
  - **T8.** Nothing tests a **non-preset** build. The Battle Priest (C1), Spellblade
    (C2) and double-count builds (M4) are all "legal" and pass. The only thing that
    exercises exploits is the preset roster.
- **Why it matters.** 206 green tests read as "rules verified". They verify the file
  shapes, the preset roster and some wording.
- **Recommended fix.**
  - Move `caster_level`, `slots` and `build_errors` into a module under
    `software/facets_d20/` and test that module.
  - Add a small damage-model module that recomputes Table 6–1 from the yaml, with
    ±10% assertions for each preset and for a pinned list of "known-strong" builds
    (Appendix A).
  - Parse each 07 domain section and compare it with the yaml by name and level.
  - Add tests for the origin talent and shared-talent gating, and for card domains and
    pick levels.

### Minor

| ID | Location | Issue | Fix |
|---|---|---|---|
| m1 | 06 Sparks, 10 | A natural 1 earns a Spark ("You still fail"), and a Spark can be spent **after** a roll to reroll it. Can you earn on the nat 1 and spend the same Spark to reroll that roll? The rules contradict each other. | "A Spark earned from a roll can't be spent on that roll." |
| m2 | 05 *Prophecy* | Self-fulfilling prophecies ("we will eat breakfast") refill glimpses and give each ally a Spark every day. Two Oracles double the ally Sparks. | "It must name something the Oracle can't simply make happen; the MM can veto trivial ones." Also cap it at one Prophecy Spark per ally per day. |
| m3 | 05 *Twist of Fate* vs *Glimpses* | *Glimpses* is "once per round"; *Twist* is a separate spend with no round limit. Can one creature get disadvantage and then a forced reroll in the same round, or can you *Twist* three times in a round? Does a reroll of a roll with disadvantage roll two dice? | "Glimpses, however spent, once per round" and "the reroll keeps any advantage or disadvantage". |
| m4 | 04 *Well-Timed Word* | It subtracts from "a damage roll", but monsters don't roll damage (08). It's either dead text or should reduce fixed damage. | "…or reduce a creature's fixed damage by the roll." |
| m5 | 04 *Studied Recovery* | Recovers "half your **level**": character level, not caster level. A late or half caster (Body taking Thaumaturgy at 2nd, 9th caster level at 10th) recovers slots sized to its character level. | "Half your caster level, rounded up." |
| m6 | 06 origin list; DESIGN A-log | *Magic Initiate* as an origin talent gives a Body character cantrips and a 1st-level spell (e.g. *Shield*) at 1st. That contradicts the stated canon "Body has no magic" and the contract's "only as a cross-Facet pick from 2nd". | Either note the exception deliberately or bar *Magic Initiate* as Body's origin. |
| m7 | 02–07 | No rule for retraining talents, domains or prepared-list domains. Only cantrips (one per level), Weapon Mastery kinds and Drives can change. The owner has to decide what happens to domains and spells if a caster talent is dropped. | One line in 02: "When you gain a level you may swap one talent for another you qualify for; a caster talent can't be swapped out." |
| m8 | 09 Owlbear example | "two turns would be 56, which is Deadly at 3rd". Table 9–1 at 3rd has Hard 53 and Deadly 72, so 56 is **Hard**. | Change to "past Hard at 3rd". |
| m9 | 09 Standard example | "add two Goblin Warriors: 109 HP, 35 damage. That's Hard." Hard at 3rd is 115/53; neither sum reaches it. | "…between Standard and Hard" or add a third goblin (119 HP). |
| m10 | 07 Table 7–4, DESIGN §6 | Cantrips known are 2/3/4, against SRD wizard and cleric 3/4/5 (the druid's 2/3/4). §6's "identical by construction" covers slots only. | Note it in §6, or use 3/4/5. |
| m11 | 03 *Weapon Mastery* + 08 minions | *Graze* deals damage **on a miss**, so a Graze weapon kills a minion with every swing. *Cleave* chains to a second minion. Minions "die to any hit" but aren't said to die to damage on a miss. | "A minion dies to any damage", and accept Graze as the minion-mower, or exempt minions from Graze. |
| m12 | 03 Extra Attack + 04/05 *Extra Attack* talent | A Body character can take the Mind/Soul *Extra Attack* talent (via *Martial Training* plus one more talent). Both say "twice instead of once", so they don't stack, but only by wording. *Wild Shape* multiattack and Extra Attack are also silent. | "Extra Attack from more than one source doesn't stack." |
| m13 | 05 *Interpose* | "Take the hit instead": do riders (grapple, poison, prone) move with it? Is the level reduction applied before or after resistance (*Rage*)? | "You take the hit and all its effects; subtract your level before resistance." |
| m14 | 08 initiative, 09 budget | The party uses its best of four rolls against one MM roll, with ties to the players. With equal modifiers the party goes first **82%** of the time: P(MM wins) = Σₖ₌₀¹⁹ k⁴ / 20⁵ ≈ 0.176. That's before *Alert*. The danger budget assumes enemies act on the first round. | Acknowledge it in 09, or let the MM also roll best-of for groups of 3+ foes. |
| m15 | 03 *Stunning Strike*, ruling (d) | Ruling (d) caps a stun at one turn, but a monk can re-stun every turn for 1 focus point. A 5th-level monk halves a boss's output for five rounds, and two monks remove both of its turns. | "A boss that has shrugged off a stun is immune to stun until the end of its next half-round." |
| m16 | 05 *Silver Tongue*, 06 social track | With no downside on a failure, the only brake is "that argument won't work again this scene". A Silver Tongue character with Expertise in Persuasion (+9 at 5th) and advantage reaches DC + 5 on about 75% of rolls against a DC 15 NPC (d20 ≥ 11 on either of two dice). Hostile to Ally takes about 2–3 checks. | Limit it to one social check per NPC per scene, or have *Silver Tongue* turn a failure into "no change" only once per scene. |

Also noted, not scored: DESIGN §7 Drafter A's "Mordai … HP 12, AC 18" line is stale;
the later A entry and 02 give 14 and 19. The §6 method excludes the Body Fighter's
third 1st-level talent (*Tough*) from HP "because the SRD character gets an origin
feat too", but the Fighter card has **both** *Tough* and an origin (*Alert*). Body's
+1 feat is real and is hidden by the method.

---

## Spell-domain notes (brief 5)

- **Must-haves.**
  - **Presence**: *Bless*, *Divine Smite*, *Spiritual Weapon*, *Spirit Guardians*. It's
    the strongest Invocation domain and the engine of C1.
  - **Binding**: *Hold Person* from caster level 3, *Banishment*, *Hold Monster*. It's
    the M6 engine.
  - **Constructed Force**: *Shield*, *Mage Armor*, *Magic Missile*, *Eldritch Blast*,
    *Wall of Force*. Every Mind caster wants it.
  - **Chronomancy**: *Haste*, *Slow*, *Blink*, *True Strike*.
- **Traps.**
  - **Resonance** tops out at 3rd level, with one 1st-level spell. 07 says so honestly.
  - **Inscription** has little in combat (*Magic Weapon*, *Glyph of Warding*).
  - **Warding** has one 2nd-level spell (*Arcane Lock*).
  - **The Constructed Mind** is utility until 5th (*Animate Objects*).

  Prismatic domains opened at 1st are fine: their lists aren't longer.
- **Problem spells in this chassis, levels 1–5.**
  - *Goodberry* + *Font of Life* (M1).
  - *True Strike* + level-scaled riders (C2).
  - *Divine Smite* on a full caster with Extra Attack (C1).
  - *Animate Dead* army-building (M7).
  - *Hypnotic Pattern*, *Hold Person*, *Banishment* and *Polymorph* against bosses
    (M6).
  - *Polymorph* on an ally at 7th–10th: a Giant Ape at CR 7, or CR 8 forms at 8th,
    gives about 150+ temporary HP in a game capped at 10th. It's SRD, but at the top
    of this curve it outclasses every Body talent.
  - *Magic Missile* and *Spirit Guardians* against minions work as designed, and the
    minion budget of 7/10 HP already prices them.
- **SRD accuracy.** I took the SRD-check report's 202-spell verification as given, and
  confirmed only that 07 and the yaml agree (script diff, zero mismatches).

---

## Appendix — exploit builds (all legal under the current rules)

Standard array 15/14/13/12/10/8. A custom background is allowed (06 "Writing Your Own
Background").

### A1 — Battle Priest (Soul) → C1

- **Abilities.** Str 15, Cha 14, Con 13, Wis 12, Dex 10, Int 8. Custom background
  (Str/Cha/Con), +2 Cha and +1 Str → **Str 16, Cha 16**, Con 13. Origin *Tough*.
- **1st.** *Invocation* (Cha; Presence + The Tide) and *Martial Training* (heavy
  armor, martial weapons). 100 gp buys chain mail, a shield and a longsword: AC 18,
  HP 11.
- **Later picks.**
  - 2nd *Sworn Strike* (3 uses).
  - 3rd *Channel*, signature *Miracle*.
  - 4th ASI (Str 18).
  - 5th *Extra Attack*.
  - 6th *Radiant Strikes*.
  - 7th *Interpose*.
  - 8th ASI (Str 20).
  - 9th *Aura of Resolve*.
  - 10th *Wider Study* (Binding).
- **5th level.** Longsword +7, p 0.70.
  - Weapon: 2 × (0.70 × 8.5 + 0.05 × 4.5) = **12.35**.
  - *Sworn Strike* 3d8: (3 + 2 short-rest) uses × 13.5 / 14 = **4.8**.
  - *Spirit Guardians* (DC 14, fail 0.55): 13.5 × (0.55 + 0.45 × 0.5) = 10.46 per enemy,
    × 2 enemies = 20.9 per round while it's up. Two 3rd-level slots cover 7 of 14
    rounds → **10.5**.
  - *Divine Smite* with four 1st-level slots: 4 × 9 / 14 = **2.6**.
  - **Total ≈ 30.2.**
  - SRD Paladin 5 (Dueling, 4/2 slots): 15.15 + 63/14 + Paladin's Smite 9/14 ≈ **20.3**.
- **10th level.** +9, p 0.80.
  - Weapon: 2 × (0.8 × 9.5 + 0.225) = **15.65**.
  - *Radiant Strikes*: 4.5 × (1 − 0.2²) = **4.3**.
  - *Sworn Strike* 4d8 × 5 / 14 = **6.4**.
  - *Spirit Guardians* (DC 15, fail 0.6): 10.8 × 2 = **21.6**, up in all four fights
    (three 3rd-level slots and one 4th).
  - Smites from the leftover 1st and 2nd slots: (4 × 9 + 3 × 13.5) / 14 = **5.5**.
  - **Total ≈ 53.5.**
  - SRD Paladin 10: 18.85 + 112.5/14 ≈ **26.9**.
  - SRD Cleric 10: *Spirit Guardians* 21.6 + *Sacred Flame* with Potent 9.8 ≈ **31.4**.
- **Defence.** Plate + shield + *Shield of Faith* = AC 22. HP at 10th = 9 + 9 × 6 + 20
  (*Tough*) = 83. Proficient in Wis and Cha saves, plus its own *Aura* (+3).

### A2 — Spellblade (Mind) → C2

- **Abilities.** Int 15, Con 14, Dex 13, Wis 12, Cha 10, Str 8. Guild Apprentice, +2 Int
  and +1 Dex → **Int 17**, Dex 14. Origin *Tough*.
- **1st.** *Thaumaturgy* (Divination + Constructed Force: *True Strike*, *Eldritch
  Blast*, *Shield*, *Mage Armor*) and *Exploit Weakness*.
- **Later picks.** 2nd *Martial Training* (medium armor and a shield: AC 18–19). 4th
  ASI (Int 19). 8th ASI (Int 20). Signature *Anatomist* (it has no caster
  requirement). Otherwise caster picks.
- **Each turn.** A bonus-action *Studied Eye* on the first turn gives advantage; the
  studied target lasts the whole fight. Then *True Strike* with a quarterstaff held
  one-handed (1d6).
- **1st level.** +5, p 0.6: 0.6 × (3.5 + 3 + 3.5) + 0.05 × 7 = **6.35** (7.0 with a
  two-handed d8).
- **5th level.** +7, p 0.7: 0.7 × (3.5 + 4 + 3.5 [TS radiant] + 10.5) + 0.05 × 17.5 =
  **15.9**.
- **10th level.** +9, p 0.8: 0.8 × (3.5 + 5 + 3.5 + 17.5) + 0.05 × 24.5 = **24.8**. With
  *Anatomist*'s 10% crits: **26.0**.
- **Soul version.** An Oracle with *Sneak Attack* at 2nd, a dagger and Wis-based *True
  Strike* (Fate) uses *Glimpses* or an adjacent ally for the Sneak Attack condition.
  Same shape, same numbers ±1.

### A3 — Unbreakable (Body) → M3 (and M7/m12 for the Wild Shape variant)

- **Build.** The Barbarian preset as printed: *Rage*, *Reckless Attack*, *Unarmored
  Defense* (Con) or medium armor + shield, *Survivor* at 6th, *Tough* at 7th. Con 18
  by 8th.
- **10th level.** HP 10 + 54 + 40 + 20 = **124**. BPS resistance doubles that to 248
  effective. *Survivor* heals 9 a turn while Bloodied, 18 effective after resistance.
  Add *Second Wind* (1d10 + 10) ×3 and *Relentless Rage* from 3rd (SRD: 11th).
  Against the Standard 10th-level danger budget (117 party-wide if all hit), the
  barbarian out-heals its share once Bloodied.
- **Wild Shape variant.**
  - Origin *Wild Kin*, 2nd *Wild Shape*, 3rd *Beast Heart*. *Wild Kin* and *Wild Shape*
    are the two Soul talents that open the T2 gate.
  - Each shape adds 3 × level temp HP (30 at 10th), twice per short rest.
  - Whether *Rage*, Extra Attack and *Survivor* work in beast form is unwritten (M7).

### A4 — Healing engine (Soul) → M1, M2

- **Build.** The Priest preset (*Font of Life*, *Mending Hands*, origin *Field Medic*)
  with *Wider Study* → Verdance instead of the preset's third domain.
- **Per day at 5th:**
  - *Mending Hands* in 1-point pings: 25 × 3 = **75**.
  - *Goodberry* on four 1st-level slots: 4 × 40 = **160**.
  - *Field Medic*: 12 applications × 11.5 = **138**.
  - *Channel* ×3: (2d8 + 4 + 2) × 3 ≈ **45**.
  - **≈ 418 HP/day**, against party HP ≈ 152: **2.75×**, before any *Cure Wounds* or
    *Healing Word*.

### A5 — Dual-tradition Wizard (Mind) → M5

- **1st.** *Thaumaturgy* (Constructed Force + Chronomancy).
- **2nd.** *Invocation* (Wis) with Presence + The Tide. Full table kept.
- **Result.** For one T1 pick at 2nd it adds *Bless*, *Healing Word*, *Aid*, *Revivify*,
  *Spirit Guardians* and *Spiritual Weapon* to *Shield*, *Mage Armor*, *Haste* and
  *Slow*. The Invocation spells that need no DC work at full value. *Wider Study*
  (T2, 3rd) would have bought one domain.
- **Unresolved.** Does the second talent add two cantrips? Which modifier sets
  prepared count?

---

*Nothing in the repo was edited except this file. No commit made.*
