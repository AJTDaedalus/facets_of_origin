# Critical Audit — Facets d20 (PR #32)

*2026-09-27. Consolidates three independent audits:
[goal fit](AUDIT_facets_d20_goal_fit.md) (1 Critical · 10 Major · 8 Minor),
[rules & exploits](AUDIT_facets_d20_rules.md) (3 · 10 · 16),
[book & licence](AUDIT_facets_d20_book.md) (0 · 8 · 20).
Total **4 Critical · 28 Major · 44 Minor** before de-duplication; the themes below
merge the overlaps.*

## Verdict

A well-edited, internally consistent 5e variant that fully delivers **one** of the
owner's asks: a Soul character really does become a Priest, a Druid or an Oracle
through its picks, and domain spell lists are the best new idea in it. It does **not**
yet deliver the other three:

- **Combat is not "3–4 rounds". It is 1–2.** The encounter budget undercounts the
  party, so fights are too short and bosses die before they act.
- **Build freedom is broken at the seams.** Two talent combinations produce characters
  about 50–90% stronger than the presets, and the balance table that claims parity
  rests on an error.
- **It is not simpler than 5e.** It adds rules on top of it: about 20–30 decisions at
  creation, about 15 exception rules, and three mechanics doing the same job.

**Not ready to merge as a playable option.** It is ready as a strong first draft for a
focused v0.2. Nothing here has been played by humans.

## Critical themes (fix before anyone plays it)

| # | Theme | Source findings | Evidence | Fix direction |
|---|---|---|---|---|
| K1 | **Fights end in ~1.5 rounds, not 3–4** | GF-C1 | Budget undercounts party damage by 25–45% and HP by 23% (3 of 4 presets carry *Tough*). The party goes first ~82–85% of the time, and "leader falls" morale ends the rest. The book's own 3rd-level example ends in ~1.5 rounds; an 8th-level boss dies before its first turn. | Re-derive Table 9–1 from the preset cards. A boss acts at the top of every round, whoever won initiative. "Leader falls" morale applies to minions only. |
| K2 | **Battle Priest**: full caster + heavy armor + Extra Attack + smites | Rules C1, GF-M1 | ~30 dmg/round at 5th vs the SRD paladin's ~20; ~53 vs ~27 at 10th. Costs the two picks that were meant to be Body's compensation. Makes the Oathsworn a trap and breaks ruling (f). | *Martial Training* grants heavy armor only to non-casters, or a caster's Extra Attack caps weapon riders. Recommended: a character with a full-caster tradition cannot take *Extra Attack* (half casters can). |
| K3 | **Spellblade**: True Strike + Exploit Weakness | Rules C2 | +92% over the Wizard at 5th, while keeping full spellcasting. | Sneak Attack and Exploit Weakness apply only to attacks made with the Attack action. |
| K4 | **The Wizard parity claim is false** | Rules C3, GF-M2 | §6 models the Wizard with *Fire Bolt*, which is on no Thaumaturgy domain. Thaumaturgy has no area-damage spell, so the "Wizard" cannot cast Fireball. | Rebalance elemental domains across the traditions (give Thaumaturgy fire/force evocation), then redo §6 honestly. |

## Major themes

1. **Non-SRD mechanics (licence).** About nine talents closely follow material that is
   not in SRD 5.2.1: Tough, Sharpshooter→*Deadeye*, Sentinel→*Bulwark*, Great Weapon
   Master→*Cleaving Blow*, Healer→*Field Medic*, Assassin→*Ambush*, Moon
   druid→*Beast Heart*, and the artificer's *Infuse Item* and *Clockwork Companion*.
   DESIGN wrongly says Tough is in the SRD. *Dueling* and *Protection* come from SRD
   5.1. No text was copied, so legal risk is low, but the brief forbids it. *Needs
   checking against the SRD PDF and an owner ruling* (Book LIC-1).
2. **Healing loops and sustain.** *Font of Life* pays out per healing instance, so it
   loops with 1-point *Mending Hands* pings and with *Goodberry*. *Field Medic* heals
   for free, so a Priest can add about 2.75× the party's HP per day at 5th. *Survivor*
   comes at 6th instead of 18th (Rules).
3. **Save-or-lose against bosses.** Paralysis, banishment, *Hypnotic Pattern* and
   *Polymorph* still end a boss on one failed save; only stun is capped. Needs a single
   boss rule: a boss shrugs off the first such effect each fight (Rules).
4. **No rules for summons or companions** under side initiative and fixed damage;
   *Animate Dead* adds about 50% to party damage (Rules).
5. **The cross-tradition caster rules are underspecified.** Taking both traditions has
   no rule for cantrips or prepared spells; taking them in the wrong order locks you
   as a half caster; *Wider Study* is pointless next to a second tradition talent.
   Shared talents also count twice toward the cross-Facet gate (Rules, GF).
6. **Facet parity.** Soul out-classes Body and Mind. The Investigator has 33% less HP
   than the SRD rogue. Custom builds were never balance-tested, only the presets
   (Rules, GF-M4).
7. **Complexity budget.** About 20 decisions from a preset card and 28–30 for a custom
   build, against about 18 for an SRD cleric. About 15 exception rules. Nine rules do
   three jobs (the Heart die and the Spark's +1d6 help are the same mechanic).
   Levelling asks for a feat-weight choice every level (GF-M6/M7/M8).
8. **Roleplay costs combat power.** Social talents compete with combat talents for the
   same once-per-level pick, and only the MM can trigger a Drive. Recommended: a
   separate free non-combat pick every other level (the PF2e skill-feat idea), and let
   players invoke their own Drives (GF-M5/M9).
9. **Domain choice is a 1st-level trap.** Utility domains (Inscription, Transmutation)
   leave the Tinker with a crossbow. Allow a domain swap at each level-up (GF-M3).
10. **Duplicated shared talents** caused a real contradiction: *Martial Training*
    grants different armor on the Mind and Soul menus, while both chapters say the
    entries "read the same". Cantrip progression is also stated three ways
    (Book ORG-1/2/3). Print shared talents once.
11. **Canon.** Divination was moved into Invocation, which contradicts the canon
    catalogue (Thaumaturgy only). New facts were given to the recurring cast: Mordai's
    "eleven years" and Drives, Zulnut's teacher (Book CAN-1/2). Owner ruling needed.
12. **Missing apparatus.** No character sheet, glossary, index or A–Z talent list
    (Book ORG-4).
13. **Prose.** About 70 "not X but Y" reframes and punchy closers, densest in 07 and
    09. A light pass over about 40 sentences (Book PRO-1).
14. **Tests check wording, not rules.** The caster-level tests exercise a helper written
    inside the test file; the spell check is a substring search; §6 and chapters
    01/02/06/08/09/10 are untested; no non-preset build is tested (Rules).
15. **Differentiation.** Every combat change is a known 5e house rule. Domains are the
    only thing a 5e table can't already get elsewhere (GF-M10).

Minor findings (44) are listed in the three source reports.

## Recommended plan

**Phase A — rulings needed from the owner first:**
1. **K2:** full casters cannot take *Extra Attack*. Accept?
2. **Licence:** rewrite the ~9 non-SRD-shaped talents as original mechanics, or keep
   them because none of the text is copied? Recommended: rewrite.
3. **Divination:** allow it in both traditions for this option, or restore it to
   Thaumaturgy only?
4. **The recurring cast:** approve or strike the new facts about Mordai and Zulnut.
5. **Scope:** is Facets d20 meant to be *simpler than 5e* (cut talents, add a separate
   roleplay pick track), or *5e with Facets* (keep the depth, fix the balance)? Most
   Major themes depend on this answer.

**Phase B — fixes that need no ruling:** K1 (re-derive the budget; boss turn at the top
of every round; minion-only morale), K3, K4 with a new §6, healing loops, the boss
save rule, summons, cross-tradition rules, printing shared talents once, cantrip
progression, and real rule tests (a build validator and simulated fights in pytest).

**Phase C:** the prose pass, the apparatus (sheet, glossary, A–Z talent list), and then
**a human table**. With three rulesets live, the owner should pick which one gets the
first playtest.
