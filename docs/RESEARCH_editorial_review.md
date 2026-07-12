# Editorial Review — Player's Handbook & Mirror Master's Manual

**Reviewer role:** TTRPG publisher's editor. **Bar:** production quality of published
works (D&D 5e, Pathfinder 2e, Call of Cthulhu 7e).
**Scope:** all 16 PHB files + MM1–MM5 (5,265 lines), cross-checked against
`characters/*.fof`, `enemies/*.fof`, and `docs/TODO.md`.
**Date:** 2026-07-11 (post v0.3 revision, main @ 902a33c)

**Verdict: NEEDS REVISION — but close.** The prose voice, vignettes, and MM-craft
chapters are already at or above the bar of published work. What blocks a
production stamp is a set of *rules-text contradictions* between chapters — the
exact class of error that erodes table trust in a published rulebook. All are
fixable without new design work except two (F2, F4), which need a design ruling.

---

## Scorecard (pre-publish checklist, adapted)

| Section | Result | One-line note |
|---|---|---|
| Content (rules accuracy) | **FAIL** | IV.1 armor contradicts III.3; 2 Techniques reference mechanics that don't exist; prismatic-access gap |
| Structure | PASS w/ notes | Chapter numbering (II.4/4b/4c), II.4 doing double duty, skill text triplicated |
| Clarity | PASS w/ notes | "Standard" domain terminology overloaded; magic-roll formula ambiguous across books |
| Style | **PASS** | Voice is consistent, distinctive, and genuinely publishable — a real asset |
| Polish | PASS w/ notes | Roll-annotation errors in examples; `--` vs em-dash in MM5; vignette roll markers vary (→ vs >) |
| Final (intent) | PASS w/ notes | Books achieve their design intent; production apparatus (index, glossary, char sheet) missing |

---

## A. Critical — rules contradictions (fix before any release)

### F1. IV.1 Equipment ships the *old* armor model — direct contradiction with III.3
- `player_handbook/IV.1_Equipment.md:33-48` says: Light = "Tier 2 Conditions
  become Tier 1" (always), Heavy = "Tier 3 (Broken) becomes Tier 2".
- `player_handbook/III.3_Combat.md:277-287` (canonical, v0.3): armor is a
  **per-scene downgrade budget** — Light softens the first **2** incoming
  Conditions by one tier, Heavy the first **4**; armor never touches Broken
  (Broken comes from Tier 2 stacking, and downgrades apply before it lands).
- MM5 (`MM5_Quick_Reference.md:182-190`) and the Enemy Attacks section agree
  with III.3. IV.1 is the sole stale copy — it predates the v0.3 revision.
- **Severity:** a player reading the Equipment chapter (the natural place to
  look up armor) learns a mechanic that no longer exists, including a
  Broken-prevention effect heavy armor does not have. This is the single most
  important fix in the review.
- Also stale in IV.1: "a successful Strike applies a Condition of the
  appropriate tier" (line 21) — against enemies, Strikes now deplete Resolve;
  Conditions apply only to PCs and as 10+ riders. And line 41 "you are still
  Staggered and hurting" describes the old model's outcome.

### F2. Prismatic domains are promised but unacquirable (rules gap)
- `II.3_Magic.md:190,244` and `Appendix_Magic_Domains.md:15,142,277`: prismatic
  domains "require a Tier 3 Technique in the appropriate Facet."
- Neither Technique tree contains such a Technique. Mind Tier 3
  (`II.4b:57-63,93-99,129-135`): The Deduction, Pressure Point, First Move,
  Pattern Recognition, The Knowledge That Saves, Deep Archive — none grants a
  domain. Soul Tier 3 has **Second Domain** (`II.4c:126-127`), but it says
  "choose a second domain from the Domains of the Soul list" without saying
  whether prismatic domains qualify — and a Mind character has no
  second-domain Technique at all.
- **Needs a design ruling**, not just editing: either (a) add a prismatic-access
  Technique to each tree's Tier 3, (b) state that Second Domain (and a Mind
  counterpart to be written) may select prismatic domains, or (c) soften the
  II.3/appendix promise. Escalation-worthy per the Brain/Planner split.

### F3. Two Techniques reference combat mechanics that don't exist
- **Overwhelming Force** (`II.4_Character_Creation_Facets.md:123-124`):
  1. "succeed on a Combat roll … by 3 or more above the threshold" — the system
     has outcome tiers, not margins of success; "threshold" is undefined.
  2. "the target is staggered — they act last in the next exchange and cannot
     take reactions until they do" — exchanges are simultaneous; there is no
     "act last." And lowercase "staggered" collides with the **Staggered**
     Condition, which has a different effect (−1 offense).
  3. Against enemies, Conditions land as 10+ riders — this Technique's trigger
     and payload both bypass the Resolve/rider model.
- **First Move** (`II.4b:95-96`): "Everyone in the party acts first in the next
  exchange" — again, no turn order exists to act first *in*. The intent
  (pre-empt an ambush) is good; the wording needs re-grounding in exchange
  terms (e.g., "the opposition's actions this exchange resolve after the
  party's" is still order-language — better: enemies cannot react this
  exchange, or the party's actions resolve before any enemy attack lands).
- These read like text written against a draft initiative system and never
  updated for exchanges. Both need mechanical rewrites.

### F4. Magic-granting Backgrounds: rule says "replace," every example grants both
- Rule (`II.5:15`): "Magic-granting Backgrounds replace the Secondary Skill
  with a domain origin." Guild Apprentice and Hedge Scholar entries carry the
  "(if magical, replaces secondary skill)" label.
- But: **Temple Acolyte** (`II.5:283-289`) lists a Secondary Skill *and* a
  "Domain origin (if magical)" with no "replaces" note; **Zahna** — the flagship
  example character — has both Investigate (Novice, 1 mark) *and* the
  Inscription domain in `Quick_Start.md:34-35` **and** `characters/Zahna.fof`
  (secondary_skill: investigate + domain: inscription).
- Either the rule is stale (design moved to "you get both") or the examples are
  wrong. **Needs a design ruling**, then propagation to II.5 (rule + Temple
  Acolyte), Quick Start, Zahna.fof, and `facet.yaml`/engine if encoded there.

### F5. Does a magic roll include a skill? The books disagree
- `II.3:103` and `Quick_Start.md:143`: roll **Knowledge or Spirit** — attribute
  only. `III.3:389` ("Attune (Spirit): … Spirit is the roll") is consistent.
- `MM5_Quick_Reference.md:108`: "Magic | 2d6 + **attribute + skill**".
- MM5 introduces a modifier the canonical text never grants — a violation of
  the project's own "quick references are compressions, not paraphrases" law.
  Whichever way the engine implements it, one side must be corrected, and the
  engine/`facet.yaml` checked to match.

### F6. Tier 1 Condition duration: "end of exchange" vs "end of scene"
- `III.3:231`: Tier 1 clears **end of exchange**. `III.2_Adventuring.md:29`:
  Tier 1 "clears automatically at the end of the **scene** it was applied in,"
  under the banner "Recovery works the same regardless of where the Condition
  came from" — which it thereby doesn't.
- The out-of-combat adaptation is sensible (no exchanges exist outside a
  fight), but the "works the same" claim is false as written. One sentence
  fixes it: Tier 1 clears at the end of the exchange in combat, or at the end
  of the current beat/scene outside it.

---

## B. High — stat-block and example-math errors

### F7. "Combat Expert (+1) / (+2 that sums wrong)" error cluster
- `III.3:319`: veteran soldier "Strength +2, Combat **Expert (+1)**" — Expert
  is +2; MM1's matching Veteran Soldier (TR 10, offense value 5) requires
  attack +3 = Strength +2 + Combat **Practiced** +1. Rank label is wrong.
- `MM1:63` Archive Guardian "Attack: +3 (Strength +2, Combat **Expert +2**)" —
  the parenthetical sums to +4, not +3. Same line in
  `enemies/archive_guardian.fof:19`.
- `MM1:64` Guardian "Defense: +1 (Dexterity −1, Combat Practiced +1…)" — sums
  to +0, not +1.
- One inconsistent breakdown in a published stat block spawns errata threads;
  three is a pattern. Sweep every stat block's parentheticals against the rank
  table (Novice +0 / Practiced +1 / Expert +2 / Master +3).

### F8. Example roll annotations omit modifiers the character has
- Zahna's Lore (Practiced, +1) is missing from every itemized lore-flavored
  Knowledge roll in the vignettes: `II.2:166`, `II.3:154,272`, `III.3:430`.
  Quick Start annotates the *same scene* correctly as "2d6+2 (Knowledge +1,
  Lore +1)" (`Quick_Start.md:39,101`). In `III.3:430` this is outcome-relevant:
  7 (partial) with Lore would have been 8 — same tier, but a reader doing the
  math loses trust.
- Mordai declares **Aggressive** (+1 offense) in all three exchanges of the
  III.3 set-piece; the itemized Strike breakdowns (`III.3:460,540,580`) never
  include the +1, even though the chapter's own quick-ref flow (line 645) says
  posture modifier is part of the roll.
- Publisher standard: every worked example's arithmetic must be reproducible
  by the reader. Recommend a dedicated math-audit pass over all vignettes.

### F9. The III.3 set-piece breaks two of its own rules
- **The Absorb that never lands** (`III.3:585-590`): Mordai, 0 Endurance,
  Absorbs a Boss attack — incoming Tier 2 by the Enemy Attacks table — and no
  Condition is applied; it's narrated away ("almost nothing behind it"). If
  Reduced Mode drops the Guardian's attacks to Tier 1, the stat block and the
  narration must say so; as written the flagship combat example demonstrates
  that Absorb is free, which is the opposite of its design tension.
- **Combat chaos adds difficulty after all** (`III.3:514` vs `III.3:379`): the
  rule says "the chaos of combat does not add difficulty on its own"; the
  example raises Zahna's Minor/Focused working from Easy to **Hard** — two
  steps — "because you're writing this during an active fight." Either the
  rule needs a carve-out (time pressure ≠ chaos?) or the example should land
  at Standard.

### F10. "Every Background … has four elements" — five follow (`II.5:15`)
Title, Description, Starting Skill, Secondary Skill, Specialty. Count error.

---

## C. Medium — cross-book consistency

- **F11.** `MM2:167` "the Named NPC is Staggered, **out of Endurance**…" —
  enemies no longer have Endurance (Resolve model, v0.3). Stale.
- **F12.** `MM3:257` cites a Technique "**Analytical Eye**" that doesn't exist
  (nearest real options: Sharp Analysis, Structural Weakness). Weapon Mastery
  and Commanding Presence in the same sentence are real.
- **F13.** career_advances bands disagree: `II.4:277-283` uses
  0–2 / 3–5 / 6–10 / 11–15 / 16+; `MM3:229-235` uses
  0–2 / 3–6 / 7–12 / 13–20 / 21+. Same metric, different brackets, different
  labels ("Veteran" at 16+ vs 21+). Align them (the tables serve different
  purposes but must not contradict on where "Seasoned/Veteran" begins).
- **F14.** Terminology overload: the Appendix's "**Standard** Soul Domains"
  heading (`Appendix:19`) contains **Focused**-type domains (Fire, Shadow) —
  "standard" is used both as a domain *type* and as "non-prismatic." Rename
  the availability class (e.g., "Core Domains"). Related: II.3's domain table
  column header "Key scope" (`II.3:195,211`) actually lists *coverage*, not
  scope — rename to "Territory" or "Covers."
- **F15.** III.3 posture quick-ref (`III.3:658`) lists Withdrawn reaction cost
  as "+0" — that's Measured's value; Withdrawn is **free**. Body text and MM5
  ("Free (0)") are correct. Quick-ref cell error.
- **F16.** Zulnut's Background "Wandering Disciple" appears in Quick Start and
  II.5's closing In Play notes, but is not among II.5's pre-builts and is
  never labeled a custom Background. A new reader will search II.5 for it and
  fail. Add "(a custom Background — see Creating a Custom Background)" where
  first used.
- **F17.** `II.5:351` (In Play commentary): "his Lore at Practiced means the MM
  can call that Standard rather than Hard" — conflates skill rank with
  difficulty, contradicting `III.1:48` ("difficulty — a statement about the
  circumstances, not a judgment about your character"). Skill rank is a roll
  modifier; it never moves difficulty. Rewrite the commentary (the Zulnut
  paragraph beneath it makes the *correct* version of this point — fiction,
  not rank, justified the Easy call).
- **F18.** `II.6:7` "advance toward Practiced and eventually Expert" — omits
  Master. Also `II.6:115` "There are no starting skill bonuses from character
  creation" is immediately contradicted by the next paragraph's Background
  exceptions; reword ("Apart from your Background's two skills…").
- **F19.** Spark earning lists drift across books: III.1 (MM award / peer
  "Spark?" / Act Break Nomination / Graceful Fail), MM2 adds **Spark for
  Weakness** as a named category, MM5's table lists only three triggers and
  drops the plain MM award. Player-facing and MM-facing lists should mirror,
  with MM-only guidance clearly marked as elaboration. MM2's hoarding stats
  (`MM2:480`) also mix per-player and per-table framing ("their 3 session
  Sparks … 2 of 9 available") — clarify units.
- **F20.** Armor-charge consumption on a redundant downgrade is code-only canon
  — already tracked as `docs/TODO.md` **T1**; this review concurs it belongs in
  III.3 body text + MM5 before print.
- **F21.** `II.1:20` sheet table: "Session Skill Points **remaining to spend at
  session end**" reads as a mid-session pool; II.4 awards 4 points *at*
  session end. Minor wording tune.

---

## D. Production apparatus — gaps vs published standards

None of these are errors; all are things D&D/PF2/CoC ship with and this text
does not yet have. Roughly in priority order for a print/PDF milestone:

1. **Glossary of terms.** The system introduces ~30 proper nouns (Spark,
   Exchange, Posture, Resolve, rider, Threat Clock, Facet, mark, career
   advance, Specialty, scope tiers…). A two-page glossary is table stakes.
2. **Index** (or, for digital-first, a linked cross-reference layer). The
   text's cross-references are good ("see Chapter III.1") but one-directional.
3. **Character sheet appendix.** II.1 describes the sheet's six sections;
   no sheet exists in the book. Even digital-first games print one.
4. **Chapter numbering.** II.4 / II.4b / II.4c with no II.4a, and II.4 doing
   triple duty (Facet concept + all shared advancement rules + Body tree).
   Recommend: II.4 Facets & Advancement (shared rules), II.4a/b/c the three
   trees. The ToC's "II.4 Facets & Advancement (Body)" already gestures at
   this.
5. **Skill text triplication.** Skill descriptions appear in the Facet
   chapters, again in II.6's table, and again in II.6's prose list — three
   near-copies of 15 descriptions is a maintenance hazard the project's own
   quick-ref law exists to prevent. Make II.6 canonical; have Facet chapters
   carry one-line summaries + pointer.
6. **Branch intro paragraphs are inconsistent.** Mind branches (Clarity/
   Instinct/Archive) each get a flavor intro; Body and Soul branches get none.
   Pick one template for all nine branches.
7. **Vignette roll-notation varies:** `→` in PHB vignettes, `>` blockquote in
   MM2/MM4. Standardize.
8. **MM5 uses ASCII `--` and `-->` throughout** where the PHB uses true
   em-dashes/arrows; it will render as literal double-hyphens. Normalize.
9. **Front matter.** No credits/license page, no "how to read this book," no
   "what is a roleplaying game" for the true-novice reader the Introduction
   courts (Quick Start partially covers this; the Introduction should point
   to it explicitly).
10. **III.2 is thin for print** (46 lines) — deliberately scoped, and the
    scope note is honest, but in a bound book it will look vestigial next to
    its siblings. Consider folding it into III.1 or III.3, or growing it with
    the recovery/hazard worked examples it currently lacks (it is the only
    rules chapter with no In Play vignette).

---

## E. What is already at publication quality (keep, do not touch)

- **The voice.** Dry, warm, confident, consistently maintained across ~5,300
  lines and two books. "That is not a failure. That is Tuesday." This is a
  differentiator; protect it in editing passes.
- **The vignettes.** The recurring cast teaching mechanics through play is the
  best version of this device I've seen outside published PbtA texts. The
  III.3 Archive Guardian set-piece is an exemplary full-combat walkthrough
  (once F8/F9's math is repaired).
- **MM2–MM4.** The session/campaign/table-craft chapters are genuinely
  competitive with published GM guidance (3-Clue Rule attribution-free but
  standard practice; safety tools section correctly credits the TTRPG Safety
  Toolkit). MM4's "difficult situations" framing is kinder and more practical
  than most published equivalents.
- **MM1's intellectual honesty.** Publishing "our TR budget is explicitly
  non-predictive; use the simulation-validated recipe table" is rare and
  admirable. Keep the caveats exactly as loud as they are.
- **The v0.3 sync discipline.** III.3 ↔ MM1 ↔ MM5 ↔ enemy `.fof` files are
  almost perfectly aligned on the new Resolve/armor-budget/enemy-attack rules.
  The stragglers (IV.1, MM2:167, the Techniques in F3) are the exceptions that
  prove the pass worked.

---

## F. Recommended fix order

1. **F1** (IV.1 armor) — one chapter rewrite, no design decisions needed.
2. **F7 + F8 + F9** — stat-block and example math sweep (mechanical, no design).
3. **F5, F6, F10–F18, F21** — one editorial consistency pass (mechanical).
4. **F2 + F4** — need design rulings (prismatic access; magic Backgrounds
   secondary skill). Per the collaboration model these are Brain-level calls;
   everything downstream (II.3, II.5, Quick Start, Zahna.fof, facet.yaml,
   engine) propagates from them in one pass per the lore-correction rule.
5. **F3** — Technique rewrites (Overwhelming Force, First Move); small design
   ruling on wording, then text.
6. **Section D items** — production apparatus, schedule against the print/PDF
   milestone rather than the next content branch.

Per the Software-PHB Sync workflow: F1, F3, F4, F5, and F20 all potentially
touch `facets/base/facet.yaml` / the engine — check each during the fix pass
and keep quick refs as compressions of the corrected body text.

---

## Addendum — fixes applied (2026-07-11, same day)

All findings in sections A–C were fixed in the editorial pass that followed
this review. Design rulings from the project owner:

- **F2 → Ascendant Domain.** New Tier 3 Technique in each tree (Archive and
  Communion branches) grants a prismatic domain; Second Domain is now
  explicitly standard-domains-only. Added to II.4b, II.4c, `facet.yaml`
  (`ascendant_domain_mind` / `ascendant_domain_soul`); II.3 and the Appendix
  now name the Technique.
- **F4 → Replace stands.** Temple Acolyte's entry restructured to the
  Guild Apprentice format; Quick Start Zahna and `characters/Zahna.fof` lose
  the Investigate secondary; `facet.yaml` temple_acolyte gained the missing
  `domain_replaces_secondary: true`; the API test asserting "keeps both" was
  inverted to codify the ruling (plus a no-domain companion test).
- **F3 →** Overwhelming Force and First Move rewritten in exchange-native
  terms (no margins, no turn order); flagged for owner review as the only
  fixes that required new mechanical wording.
- **F9a →** Reduced Mode now states its blows land as Tier 1 (MM1 stat block,
  `.fof` phase, and the III.3 example, where Mordai's Absorb now takes Winded).
- **F20/T1 →** armor-charge consumption rule written into III.3 and MM5;
  `docs/TODO.md` T1 struck.
- Everything else in B/C (stat-block parentheticals, vignette math, career
  bands, Analytical Eye → Sharp Analysis, MM5 magic row, Withdrawn quick-ref
  cell, "four elements", Core vs Standard domain headings, MM punctuation
  normalization) applied as recommended.

Tests: **965 passed**; the single failure is the pre-existing,
environment-sensitive `test_default_port_is_8000` tracked as TODO T4.

A light prose de-patterning pass (per owner ruling) also ran across both
books: repeated "It is not X. It is Y." reframes thinned, stacked kicker
lines cut (~a dozen), anaphora triples broken up, self-commentary
("This is deliberate/intentional") varied, and a handful of dash-negations
converted. Voice preserved; section D production apparatus remains open.
