# AUDIT — Facets d20: goal fit, simplicity and fun

*Critical audit, 2026-09-27, branch `feat/facets-d20` (PR #32). Read-only on content.
Scope: `facets_d20/` (README, 01–10, `data/`), `docs/BRIEF_facets_d20.md`,
`docs/DESIGN_facets_d20.md`, `docs/REVIEW_facets_d20.md`,
`docs/RESEARCH_facets_d20_dominance.md`. Lens: does it deliver the owner's request
(facets instead of classes, RP focus, easy pickup, short combat, close to D&D), and is it
simple and fun? Findings already fixed by the dominance audit are not repeated.*

## Executive verdict

Facets d20 is a competent, well-edited 5e variant, and it gets one of the owner's asks
fully right: **Soul** really does become a priest, druid or oracle through picks, and
domain spell lists are its best idea. The other asks are only partly met. Combat is not
too long. It is **too short and front-loaded**: the encounter budget undercounts the
party by roughly 25–45%, and side initiative plus leader-triggered morale mean most
"Standard" fights are decided in round 1. The boss-with-retinue pattern the MM guide
recommends usually dies before the boss acts. Build freedom is real in Soul, thinner in
Body, where the menu is four SRD class chassis unbundled, and dominated by a cheap
full-caster gish. The RP layer does real work: Specialty and the attitude track are
good. But it sits inside a single talent economy where every social pick costs combat
power, and it has too many overlapping "add a die / grant advantage" rules for the
owner's "one way to do each thing" test. Nobody has played it yet. The fixes are tuning
and consolidation, not a redesign.

**Counts:** Critical 1 · Major 10 · Minor 8.

---

## Findings (ranked by severity)

### GF-C1 — Critical — Fights end in 1–2 rounds, and bosses die before they act

**Location:** `09_Mirror_Masters_Guide.md` §Building an Encounter (Table 9–1, "How the
Budget Was Tuned"), §Bosses, §Bloodied and Morale; `08_Combat.md` §Who Goes First, §Morale.

**Evidence.** Expected-value simulation with a preset party (Fighter, Rogue, Wizard,
Priest, built from their cards), using the book's own worked encounters (method at the
end of this file):

| Fight | Budget says | What happens (EV) |
|---|---|---|
| **L3, the book's own Standard example**: Ogre + 3 Bandit minions (89 HP / 25 dmg) | 3–4 rounds, "a third of the party's health" | Party goes first (~85%: best of four Dex checks, ties to players, *Alert*). One 1st-level *Magic Missile* auto-kills all three minions. Fighter with *Action Surge* (~15), Rogue with *Ambush* (~21) and Priest (~8) put ~45 into the 68-HP Ogre. It is Bloodied and makes a DC 10 Wis save at −2, so **it breaks 55% of the time in round 1**, and otherwise dies in round 2. **~1.5 rounds, ~5 damage taken of ~118 party HP.** |
| **L3, 7 Goblin Warriors** (70 HP / 35 dmg, Standard) | 3–4 rounds | ~2.8 goblins down or broken in R1 and ~2.4 in R2; the rest mop up in R3. **~3 rounds, ~15 damage taken (~13% of party HP).** The one composition that hits the target. |
| **L8, Owlbear boss + Ogre + 4 Goblin Warriors** (167 HP / 89 dmg, Standard, built by 09's "choose a boss" rule) | 3–4 rounds, boss takes 2 turns | Fighter *Action Surge* (4 attacks at +8 vs AC 13, ~39) and Rogue *Ambush* (~32) average ~70 against the Owlbear's 59 HP, **before the Wizard's 4th-level *Magic Missile* (21, auto-hit)**. The boss dies in R1 before its first turn roughly 80–90% of the time. "Leader falls" then triggers morale for the whole group (~50% break). **~2 rounds, under 10% of ~295 party HP.** |
| **L9, Young Red Dragon, solo boss** (178 HP / 96 dmg) | Standard | R1 alpha ~85, it is Bloodied in R1–R2 and dead in R3. It deals ~130–150 across its turns plus breath. **~3 rounds, ~45% of party HP.** A single boss sized to the whole HP budget works. |

Causes:
1. **Party damage per round is undercounted.** The table says 25 at L3 and 50 at L8. The
   presets do about 31 and 65 sustained, and about 45 and 90 in round 1 (*Action Surge*,
   *Ambush*, the best slot, all landing before the enemy moves).
2. **Party HP is undercounted.** The table uses "40 + 28/level" (96 at L3, 236 at L8).
   Three of the four presets carry *Tough* (Fighter's L1 talent, Rogue's and Wizard's
   origin talent), so the real numbers are ~118 and ~295 (+23%).
3. **"Morale and overkill roughly cancel" (09) is false for a single big foe.** A DC 10
   save at first Bloodied removes about half the foe's remaining HP half the time.
4. **Side initiative + ~85% party-first + round-1 nova** means the enemy's first half
   often arrives after the fight is decided. A boss's two turns do nothing if it never
   gets one. "Leader falls → the whole group checks" rewards the same single tactic in
   every fight, and 09 tells the MM to reward it.
5. **Minions are budgeted at 7/10 HP but die to auto-hit and aura damage.** Each *Magic
   Missile* dart kills one. *Spirit Guardians* kills any that fail.

**Why it matters.** The owner asked for "combat not overly long", not for combat that
doesn't happen. A Standard fight that costs 5–10% of the party's HP has no tension. A
boss that never acts is the worst anticlimax a d20 game can produce. And an MM who
notices will overcorrect toward Deadly, where side initiative lets the whole enemy side
spend its fixed damage on one PC before the healer moves (see GF-m7). Table 9–1 is the
MM's only tuning tool, and it is wrong in the direction that makes fights hollow.
REVIEW §6 Q7 already calls it "arithmetic, not play".

**Recommended fix.**
- Re-derive party DPR from the preset cards: L3 ≈ 31, L5 ≈ 45, L8 ≈ 65, L10 ≈ 75. Add a
  round-1 nova factor of ×1.4. Re-derive party HP from the cards, *Tough* included.
- **Boss rule.** A boss always takes one of its turns **at the top of every round**,
  before either side, and the other in its side's half. A PF2/Draw Steel-style "boss acts
  regardless" costs one sentence and removes the "dies before acting" failure. Also add a
  floor: a boss's own HP should be at least 60% of the difficulty's HP budget.
- **Leader morale** applies to minions only. Standard foes check when *their side* is
  Bloodied as a whole. Otherwise "kill the leader" stays the answer to every fight.
- Budget minions at 1 HP plus "each one adds 1 attack", and warn in 09 that auto-hit
  and aura spells clear them.
- Build a 20-line EV/Monte-Carlo sim that drives the presets from `data/facets_d20.yaml`,
  and require a human playtest of one L3 and one L8 fight before the budget ships.

---

### GF-M1 — Major — A full caster with heavy armor and Extra Attack costs two picks

**Location:** `05_Facet_of_the_Soul.md` (*Invocation*, *Martial Training*, *Extra Attack*,
*Sworn Strike*; the "why the Oathsworn doesn't cast" sidebar); `04` (*Martial Training*
(Mind), *Extra Attack*). Not covered by `RESEARCH_facets_d20_dominance.md`, which rates
Soul *Martial Training* "OK: heavy armor adds ≤ +1 AC".

**Evidence.** The Oathsworn sidebar says: "A full caster in heavy armor with Extra Attack
and a smite was more than we wanted on one card." That exact build is legal for a custom
Soul character: L1 *Invocation* (Cha) + *Martial Training*, L2 *Sworn Strike*, L4 ASI,
L5 *Extra Attack*. At 5th level it has 4/3/2 slots, *Spirit Guardians*, *Divine Smite*
(Presence), two attacks, heavy armor and a shield, and 3d8 *Sworn Strike*. That is an
SRD cleric and paladin combined, for four picks, one of them optional. The Mind version
(*Thaumaturgy* + *Martial Training* + *Extra Attack*, with *Shield* and *Haste* from
Constructed Force and Chronomancy) is a bladesinger at 5th with medium armor and a
shield. B's flag in DESIGN §7 ("the strongest thing in the game") was closed by the
caster-level ruling, but that ruling only affects characters who take the caster talent
late. This build takes it at 1st.

**Why it matters.** Build freedom collapses into one right answer: every optimising Mind
or Soul player goes gish. The pure-caster and the non-caster presets then look like
traps next to it, and the Oathsworn's own design reason is undercut in the same chapter.

**Recommended fix.** Pick one:
- *Extra Attack* (Mind/Soul) requires "no caster talent". Casters get a
  cantrip-plus-weapon feature instead, like the SRD's True Strike/Booming Blade pattern.
- Taking *Martial Training* or *Extra Attack* while holding a caster talent drops you to
  the Half table. This mirrors the SRD paladin.

Either way, add the gish to the dominance audit's list and to DESIGN §6.

### GF-M2 — Major — The "Wizard" can't cast Fireball, and Mind has no blasting at all

**Location:** `07_Magic.md` §Domain Spell Lists; `04` Wizard card; DESIGN §6 Table 6–1
(Wizard vs SRD Evoker).

**Evidence.** Every fire, lightning, cold and thunder spell is on an Invocation domain:
*Fire Bolt, Burning Hands, Scorching Ray, Fireball, Lightning Bolt, Thunderwave, Shatter,
Cone of Cold* (spells.yaml lines 59–135). No Thaumaturgy domain has a damaging area
spell of 2nd or 3rd level. The Wizard card (Constructed Force + Warding) gets these 3rd-
level spells at 5th: *Glyph of Warding, Magic Circle, Nondetection, Protection from
Energy, Tiny Hut*. None deals damage in a fight. Table 6–1 claims Wizard/Evoker parity
using *Fire Bolt*, which the Wizard card's domains don't contain (Eldritch Blast has the
same numbers). The parity check also ignores leveled spells, which are most of an
evoker's output. The card's 3rd-level pick, *Careful Casting* (sculpt allies out of an
area), has almost nothing to sculpt until *Wider Study* adds Illusion.

**Why it matters.** This is the most likely unpleasant surprise for a 5e table: "I'm
the wizard, where's Fireball?" It breaks "hedging close to D&D" on the most iconic
class/spell pairing. The blaster archetype does exist, but as a Charisma Soul caster
with Fire + Storm (the sorcerer shape), and no card or sidebar says so.

**Recommended fix.** Either give Thaumaturgy an evocation domain ("Force & Element": the
fire/lightning/cold staples, constructed rather than felt), or make Fire/Storm
dual-tradition like Divination. Then fix Table 6–1 to compare leveled-spell output, and
add a "Sorcerer shape (Soul, Cha, Fire + Storm)" sidebar.

### GF-M3 — Major — Domain choice is an irreversible 1st-level trap

**Location:** `07` Table 7–5 and the domain lists; `04` Tinker card.

**Evidence.** Combat weight varies enormously between domains:
- **Fire** has a damaging spell at every level.
- **Inscription** has no damaging cantrip and nothing but *Glyph of Warding* through 5th.
- **Transmutation** has *Acid Splash*, then no damage until *Wall of Stone*.
- **Warding** has no damage at all.
- **Divination** has *True Strike* and *Guidance*.

The Tinker card takes Inscription + Transmutation. At 3rd level its combat magic is one
Acid Splash (1d6), so it fights with a light crossbow. The Oracle pair (Fate +
Divination) gets *Augury* as its only 2nd-level Fate spell. Domains are chosen at 1st
level, can't be changed, and come with no guidance on which ones fight.

**Why it matters.** A new player picks on theme ("I'm an inscriber") and finds out at
3rd–5th that their character can't contribute to fights. That is the classic trap
option. It is worse here because the book promises "any two domains make a legal
caster".

**Recommended fix.** Guarantee a floor for every domain: one damaging or controlling
cantrip, and one combat-relevant spell at each of 1st–3rd. Tag each domain in Table 7–5
with a column (Offense / Control / Support / Utility), and add one line: "pair a utility
domain with a combat one." Allow one domain swap when you gain a level.

### GF-M4 — Major — Presets are SRD classes rebuilt, and only presets were tested

**Location:** DESIGN §6 (Table 6–1 "0% difference by construction"); `03` Body menu;
`01` item 1.

**Evidence.** The balance anchor measured the Fighter, Rogue, Wizard and Priest cards
against SRD classes and tuned them to match exactly. No custom build was measured. The
Body menu is the fighter, rogue, barbarian and monk class features with the labels
removed, joined by prerequisite chains (*Focus* → *Martial Arts*, *Stunning Strike* →
*Focus*, *Relentless Rage* → *Rage*; the signatures *Fury* and *Still Water* require
their chassis talent). Mixing across those chassis is mostly anti-synergistic:
- *Rage* forbids casting and heavy armor.
- *Martial Arts* needs no armor.
- *Sneak Attack* turns off with *Extra Attack*, *Martial Arts* and *Flurry*.
- *Cunning Action* and *Martial Arts* want the same bonus action (03 warns about this
  itself).

The Zulnut custom build works because it takes a monk chassis minus *Focus*.

**Why it matters.** The owner's spin is "build a character how you want". In Body, the
realistic builds are the four classes or a lightly edited class. The freedom is real in
Soul (see What works) and partial in Mind. A 5e player will read Body, correctly, as
"classes with extra steps".

**Recommended fix.** Add 3–4 Body **bridge talents** that reward mixing chassis: armored
*Martial Arts* at a smaller die, a *Rage* that works with *Sneak Attack* ("once per rage,
a single brutal hit"), a skirmisher talent that lets *Cunning Action* move share the
*Martial Arts* bonus action. Extend DESIGN §6 to at least six custom builds (Zulnut, the
Physician, the Lucky Swindler, the Hedge Witch, a Body/Soul ranger, an armored monk)
measured against the presets.

### GF-M5 — Major — The RP layer shares one talent economy with combat, so RP always costs power

**Location:** `06` §Backgrounds, §Drives, §Social Play; the talent menus in 03–05;
`09` §Levels.

**Evidence.** Of about 60 talents, the ones that work mainly outside a fight are
*Expertise, Skilled, Silver Tongue, Wild Kin, Field Medic, Gadgeteer* and *Reliable
Talent*. Each one uses the same once-per-level pick as *Action Surge* or *Extra Attack*.
The only free social slot is the origin talent at 1st level. Levels come from MM
milestones; nothing ties advancement to Drives or social outcomes. README says social
scenes "count as much as fights", but mechanically only fights consume and reward the
build.

**Why it matters.** Players optimise what the build rewards. With one pick a level, a
player who wants to be the silver-tongued envoy is paying a visible combat tax each
time. The RP focus becomes something the table does despite the rules, which is where
5e already is.

**Recommended fix.** Add a second, parallel pick for non-combat talents (the Pathfinder
2e skill-feat model): a free **knack** at 3rd, 5th, 7th and 9th, from a list of
origin-weight, non-combat talents (*Silver Tongue*, *Wild Kin*, *Skilled*, *Expertise*,
new social/exploration knacks). Let a Drive fulfilled or broken for good count as a
milestone (09 §Levels). This is also the strongest candidate for "our distinctive value"
(GF-M10).

### GF-M6 — Major — Nine rules do three jobs ("add a die", "advantage", "reroll")

**Location:** `06` Sparks; `05` *Inspiring Word*, *Glimpses*, *Twist of Fate*;
`04` *Well-Timed Word*, *Anticipate*, *Studied Eye*; `08` Help action.

**Evidence.**
- **Add a die to an ally's roll after it is rolled:** Spark help (+1d6) and the Heart die
  from *Inspiring Word* (d6/d8). Same timing, same die.
- **Advantage or disadvantage before a roll:** a Spark, *Glimpses*, the Help action,
  *Studied Eye*, *Anticipate*, leverage, a Specialty, *Reckless Attack*, *Ambush*.
- **After-roll changes:** a Spark reroll, *Twist of Fate*, *Well-Timed Word*
  (subtract a die).

The Oracle's whole kit is the Spark economy with a second currency. Because advantage
doesn't stack, a Spark spent for advantage is often wasted: a Specialty, leverage or a
glimpse already gave it.

**Why it matters.** The owner's rule is "one way to do each thing, no exception rules".
It also slows combat: every enemy attack roll becomes a moment where someone may want
to interject (Heart die, glimpse, Well-Timed Word, Anticipate, Spark help). That is
where the enemy half of the round will drag.

**Recommended fix.**
- Fold the Heart die into Sparks: *Inspiring Word* = "give an ally a Spark (it doesn't
  count toward their cap and expires at the end of the scene)".
- Keep one "help" mechanic: the Spark +1d6 or the Help action, not both.
- Rewrite *Glimpses* as "you may spend Sparks on any creature you can see, including
  enemies (to impose disadvantage)". The Oracle becomes the Spark specialist rather than
  a parallel economy.
- Add one sentence to 06: "If you already have advantage, a Spark can't give it; reroll
  instead."

### GF-M7 — Major — The exception-rule count is high for "easy to pick up"

**Location:** throughout; tallied from 01–08.

**Evidence.** These are the carve-outs a player can meet in normal play:
1. *Sneak Attack* / *Exploit Weakness*: not on a turn with more than one attack,
   bonus-action attacks included.
2. The two never combine.
3. A stunned boss loses one turn, not two (03, 09).
4. A boss's Recharge rolls once per half-round.
5. *Master Plan* and *Seen It Coming* skip the initiative contest.
6. Caster talents can't be origin talents.
7. ASI always counts as your own Facet's.
8. An origin talent counts toward the cross-Facet "two".
9. *Martial Training* grants different armor depending on which Facet you are (GF-m1).
10. Casters run two clocks: slots and prepared spells go by caster level, while cantrips
    (Table 7–4), *Studied Recovery* ("half your level"; REVIEW Q5) and *Potent
    Cantrips*' 7th-level gate go by character level.
11. "Soul modifier" means the casting ability, or the higher of Wis and Cha if you don't
    cast.
12. A character never has two slot tables, but spells use the ability of the tradition
    they came through.
13. A signature costs no pick, is always from your own Facet, can't be changed, and some
    have a "Requires".
14. Minions count 7 HP at 1st–4th and 10 at 5th–10th; never-break foes count ×1.25.
15. Wild Shape: nothing with a flying speed before 8th.

**Why it matters.** Each rule is defensible alone. Together they fail the owner's "felt
simplicity" test. Several exist only to patch another rule: 1–2 exist because Body gets
free *Extra Attack*, 3 because bosses get two turns, 10 because of the late-caster
ruling.

**Recommended fix.**
- Replace 1–2 with a single "Precision" rider: "once per turn, +Xd6; if you use it, you
  make no other attacks this turn". One sentence, stated once, with *Exploit Weakness*
  as the same talent on the Mind menu.
- Put everything a caster has (cantrips included) on caster level.
- Make *Martial Training* identical on both menus (GF-m1).
- Fold 3 into the boss-turn fix in GF-C1.
- Keep a visible "Exceptions" box in 10 so any that survive are at least listed in one
  place.

### GF-M8 — Major — Character creation is no lighter than 5e, and levelling is heavier

**Location:** `02` Table 2–1 and Steps 1–7; the preset cards in 03–05.

**Evidence.** Decision count for a **Priest built from its card**:
- concept, want, line (3)
- array placement (1)
- ASI split (1)
- Specialty (1)
- Facet skills (3)
- cantrips (2)
- prepared spells (4)
- kit options (3)
- languages (2)

That is **≈20**. A **custom Soul caster** adds Facet, background, origin talent, two
talents, casting ability and two domains, for **≈28–30**. An SRD 5.2.1 cleric at 1st is
about 18. The cards don't list skills, cantrips or 1st-day prepared spells, so "take as
printed and you are ready to play" (03) isn't quite true. The step order is circular:
Step 2 (abilities) asks you to know your background (Step 4) and your Facet (Step 3).
After 1st level, **every** level is a feat-weight choice from 11–22 own-Facet talents
plus ~40 cross-Facet ones. In the SRD most levels hand you fixed features.

**Why it matters.** "Easy to pick up" rests almost entirely on 5e familiarity. For the
README's "new players" audience, and for anyone going off-card, the decision load is
higher than 5e's.

**Recommended fix.**
- Put skills, cantrips and a default prepared list on every card, making it a true
  zero-decision sheet.
- Reorder the steps: Concept → Facet → Background → Abilities.
- Add a "fast custom" rule: at 1st level take a preset's L1 talents and customise from
  2nd.
- Consider a small fixed ladder per Facet at 5th and 9th (Body: Extra Attack at 5th is
  already one), so that not every level is a shopping trip.

### GF-M9 — Major — Drives are left to the MM, and there is no player-side trigger

**Location:** `06` §Drives, §Sparks; `09` §Rewarding Drives.

**Evidence.** A Drive earns a Spark only "when one of your Drives costs you something",
judged by the MM, and 09 asks the MM to "build at least one scene a session" around it.
There is no procedure a **player** can start: no "I invoke my line: offer me the Spark or
the complication". A Spark's pay-off (advantage, reroll, +1d6) is Heroic Inspiration
under another name, and its advantage mode is often redundant (GF-M6). Drives never
touch levels, talents or signatures. The one exception is the Oathsworn's *Oath
Unbroken*, which is a good model.

**Why it matters.** At a table with a busy or new MM, Drives go quiet by session three.
Then Sparks come only from natural 1s and "great moment" calls, and the RP layer is
decoration.

**Recommended fix.** Add a player-side compel: "Once per scene, when your Drive would
make things harder, say so. If the MM accepts, take the complication and a Spark." This
is Fate's compel, a general idea and free to use. Tie advancement to Drives (GF-M5).
Give each Facet one Drive-linked signature on the *Oath Unbroken* model.

### GF-M10 — Major — The distinctive value isn't yet enough to beat "5e plus house rules"

**Location:** README; `01`; BRIEF §1 (the Pathfinder precedent).

**Evidence.** Pathfinder 1e's value over 3.5 was fixing dead levels and class balance.
PF2e's was a feat at every level across four tracks (class, ancestry, skill, general).
Our package, piece by piece:
- Side initiative is a 5e DMG variant.
- Fixed damage is already printed on every SRD stat block.
- Minions come from 4e and MCDM.
- Morale is an OSR and DMG staple.
- Two-turn solo bosses are a common homebrew.
- Talents are the SRD class features relabelled (GF-M4).
- Sparks are Heroic Inspiration with a trigger.
- A Specialty is 13th Age's background idea narrowed.

Facet identity is chassis numbers plus one 1st-level feature. The Body/Mind/Soul idea
from the core game barely appears in play: nothing makes a Mind character play
differently in a social scene or earn Sparks differently. **Domains as spell lists** is
the only piece a 5e table can't already get from a house-rules page.

**Why it matters.** "Why not play 5e with these house rules?" is the question every
reviewer will ask, and right now the honest answer is "curation". That is worth
something, but it is not Pathfinder-scale.

**Recommended fix.** Build the identity on the two things we have that others don't:
1. **Domains** as the headline, with the floors from GF-M3 and dual-tradition overlap.
2. **Facets that mean something at the table:** a Facet-flavoured Spark trigger or
   social approach (Body earns by enduring, Mind by being right, Soul by standing with
   someone), plus the knack track from GF-M5.

Say this plainly on the README's first screen.

---

### GF-m1 — Minor — *Martial Training* has two texts, and 05 says they read the same

**Location:** `04` *Martial Training* ("medium armor and shields"); `05` *Martial
Training* ("heavy armor") and the note under Table 5–2 ("…are on the Mind menu too, and
read the same there"); `data/facets_d20.yaml` `martial_training` (one id with
Facet-dependent text).
**Why it matters.** It is a factual error in 05. It also leaves open what a Mind
character gets when taking the Soul version cross-Facet, or the reverse.
**Fix.** Make it one rule with one text ("martial weapons, and one armor step above
your Facet's"). Correct the 05 note.

### GF-m2 — Minor — The Oracle card doubles up its surprise protection

**Location:** `05` Oracle card (origin *Alert*, signature *Seen It Coming*).
**Evidence.** Both say "your side can't be surprised". *Alert* is also the origin talent
on three other cards, so a party of presets duplicates it (dominance audit Q4).
**Fix.** Give the Oracle *Wild Kin* or *Skilled* as its origin talent. Make *Seen It
Coming* do something *Alert* can't.

### GF-m3 — Minor — 01 lists unchanged rules as changes and omits one real change

**Location:** `01` item 10.
**Evidence.** "You get one reaction a round, and leaving an enemy's reach provokes one
attack" is the SRD rule. Meanwhile, surprise meaning "the other side simply goes first"
does differ from the SRD (where surprise gives disadvantage on initiative), and 01
doesn't say so.
**Fix.** Replace the reaction sentence with the surprise rule.

### GF-m4 — Minor — For a caster, taking the other tradition beats *Wider Study*

**Location:** `07` §Full and Half Casters; *Wider Study* (04, 05).
**Evidence.** From 2nd level, a caster who takes the other tradition's talent (tier 1)
gets **two** domains and keeps the Full table. *Wider Study* (tier 2) gives one. A Priest
who takes *Thaumaturgy* gets *Shield*, *Mage Armor* and *Haste*, none of which care about
Intelligence. The rules also don't say which modifier sets the prepared count once you
hold two traditions.
**Fix.** The other tradition's talent adds **one** domain for an existing caster. State
that the prepared count uses your first tradition's ability.

### GF-m5 — Minor — A 5e rogue who dual-wields loses Sneak Attack

**Location:** `03` *Sneak Attack* ("counting bonus-action attacks").
**Evidence.** In the SRD, two-weapon fighting (and the *Nick* mastery) plus a single
Sneak Attack is a standard rogue turn. Here it turns Sneak Attack off.
**Fix.** Exempt the off-hand attack (count only Attack-action attacks), or say so in 01.

### GF-m6 — Minor — Fixed damage makes low-level one-shots certain

**Location:** `08` §Attacks and Damage; `04` Wizard card ("a d6 hit die needs [*Tough*]").
**Evidence.** A 1st-level Mind character without *Tough* has 8 HP. Any Ogre hit (fixed
13) drops them every time, and a 5e table's "maybe it rolls low" never happens. The
card's own note admits the d6 hit die needs a tax.
**Fix.** At 1st–2nd level, monsters deal the lower of fixed damage and the target's
current HP − 1 on the first hit of a fight. Or raise Mind to 8 + Con at 1st.

### GF-m7 — Minor — Side initiative plus fixed damage makes focus-fire exact

**Location:** `08` §The Round; `09` §The Enemy Half.
**Evidence.** The whole enemy side acts together with known damage, so the MM can see
exactly which PC drops if everything targets them, before the healer moves. At Deadly
(the likely overcorrection from GF-C1) that becomes a PC dropped in round 1 with no
chance of a low roll.
**Fix.** Add an MM Note: "Spread a side's attacks unless the fiction demands focus; a
PC drops to 0 at most once per enemy half." Alternatively, the boss top-of-round turn
from GF-C1 splits the enemy volley on its own.

### GF-m8 — Minor — Minions are budgeted against weapons, not spells

**Location:** `09` Table 9–1 "What counts" (minion = 7/10 HP).
**Evidence.** One *Magic Missile* dart (auto-hit) kills a minion, so a 1st-level slot
removes 21 budget-HP at 3rd and a 4th-level slot removes 60 at 8th. *Spirit Guardians*
kills every minion that fails its save.
**Fix.** Add a line in 09 ("in parties with auto-hit or aura casters, count minions at
half") and fold it into the rebuilt budget (GF-C1).

---

## What works

- **Soul delivers the owner's headline example.** Priest, Druid and Oracle start from
  the same *Invocation* talent and diverge through real picks: *Font of Life/Channel*,
  *Wild Shape/Beast Heart*, *Glimpses/Prophecy*, and different domain pairs that "will
  never cast the same spell on the same day". The Hedge Witch shows mixing working.
- **Domains as spell lists** are the best idea in the option: one engine, many subjects.
  The fiction-first MM Note ("Shadow's *Sleep* is dark closing over the eyes") is exactly
  the right tone.
- **01 is a genuine one-page diff.** Twelve items, written for a 5e player; the 21 → 12
  merge in the review pass was the right call.
- **Specialty does real work.** Advantage plus "routine things just happen" is a clean
  RP-first rule, and the example shows it working.
- **The attitude track** is short, clear, has no social HP, and has good DC guidance.
  "Anything inside what their attitude allows, you get by asking" is excellent.
- **Morale feeds the RP layer.** Broken foes become prisoners and bargains, and 09's
  "mercy has to pay off more often than it bites" is the right design instinct.
- **Fixed damage with rolled crits**, open enemy rolls, and "a fight is over when its
  question has been answered" all shorten the enemy half without taking anything from
  players.
- **The single-boss case works.** The Young Red Dragon lands at ~3 rounds with real
  danger.
- **Non-caster roads exist in every Facet** (Investigator, Oathsworn), and the
  dominance audit already caught the worst dips.
- **Scope discipline.** Levels 1–10, spells to 5th, SRD by reference, a player-facing
  read of ~21,500 words (01–08 + 10, about 90 minutes). "Read it in an evening" is true.
- **Editorial quality** is high. The MM Notes' default/dial/cost format and the preset
  "Play it like" lines are the voice of a book people will enjoy reading.

## Top risks

1. **Nothing has been played.** The budget, the boss rule, morale rates and every parity
   claim are EV arithmetic (REVIEW §6 Q7). GF-C1 shows that the arithmetic already
   disagrees with itself.
2. **Hollow fights leading to overcorrection.** MMs discover Standard is trivial, push
   to Deadly, and side initiative turns Deadly into swingy PC deaths (GF-C1, GF-m7).
3. **Build freedom collapses into gish optimisation** (GF-M1) and domain traps (GF-M3).
   That produces the opposite of the promise: a right answer and wrong answers.
4. **The RP layer sits on top of the combat engine rather than inside it** (GF-M5,
   GF-M9). In play it shrinks to Heroic Inspiration.
5. **Weak differentiation** (GF-M10). The option risks being "5e with house rules" in
   reviewers' eyes.
6. **Three live rulesets** (v0.3 pinned, Lean v1.x, d20) split the owner's playtest
   attention. Pick which one gets the first human table.

---

## Method notes (combat simulation)

- **Party:** preset cards as printed, standard array plus background bonuses, ASIs on
  the card's schedule.
  - *L3:* Fighter +5, 1d8+5 (Defense + Dueling), *Action Surge*, *Champion's Edge*.
    Rogue +5, rapier 1d8+3, Sneak Attack 2d6, *Ambush* (+2d6, advantage in R1). Wizard
    +5, Eldritch Blast 1d10, *Magic Missile*, slots 4/2. Priest DC 13, Sacred Flame 1d8,
    *Spiritual Weapon* 1d8+3.
  - *L8:* Fighter +8, 2 attacks of 1d8+7. Rogue +8, 1d8+5 + 4d6. Wizard +8, 2-beam
    Eldritch Blast with *Potent Cantrips*, 4th-level *Magic Missile* (6 darts). Priest DC
    16, *Spirit Guardians*.
- **Hit chance** = (21 − (AC − bonus))/20, clamped; crits 5% (10% for *Champion's
  Edge*). Advantage = 1 − (1 − p)².
- **Initiative:** party first ≈ 85% (best of four Dex checks, ties to players) vs one
  enemy roll at the best enemy Dex modifier.
- **Morale:** DC 10 Wis save with the monster's Wis modifier: Ogre −2 (breaks 55%),
  Goblin −1 (breaks 50%).
- **Party HP from the cards**, *Tough* included: L3 ≈ 118, L8 ≈ 295. The book's formula
  gives 96 and 236.
- SRD monster numbers are the ones printed in 09's worked conversions.

These figures are expected values, not a Monte-Carlo run. They are good enough to show
the direction and rough size of the miscalibration, not the exact round counts.
