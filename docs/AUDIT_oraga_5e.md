# Critical Audit — Oraga Night, Fifth-Edition (PR #33)

*2026-09-27. Consolidates three independent audits:
[playability](AUDIT_oraga_5e_playability.md) (3 Critical · 10 Major · 12 Minor),
[combat & rules](AUDIT_oraga_5e_combat.md) (2 · 9 · 17, with Monte Carlo of every card),
[canon, licence & prose](AUDIT_oraga_5e_canon.md) (0 · 5 · 14).
Total **5 Critical · 24 Major · 43 Minor** before de-duplication.*

## Verdict

The conversion is faithful and the numbers are right:
- **Canon holds.** Every owner ruling is intact, the "Never Says" list stays shut
  (including against spells), and no private name leaked into the book.
- **The maths checks out.** Every stat block and pregen re-derives correctly, the XP
  sums match SRD 5.2.1, and there is no non-SRD content.
- **The snakes layer delivers.** It gives a 5e table the "snakes in the chicken pen"
  night the owner asked for, and no card before midnight risks a party wipe.

**It is not yet table-ready.** Midnight and the gate have rule holes that a 5e table
will find on the night. The book is about two sessions long while it claims one.
Estimated fix time: about a day. None of it needs a canon ruling except where marked.

## Already fixed during the audit

- **A-1 leak:** private-canon provenance scrubbed from `INVENTIONS_5e.md` (commit
  69ed58b). The earlier text is still in branch history on GitHub; purging it would
  need a history rewrite. That is the owner's call.
- **A-5 trademark:** PR #33 retitled "fifth-edition (SRD 5.2.1)". The flow page header
  and commit subject still say "D&D"; see F10.

## Critical themes

| # | Theme | Source | Problem | Fix |
|---|---|---|---|---|
| K1 | **Knocked-out characters never come back** | Play C1, Combat M4/M9 | Anyone the Uninvited drop is "out of the scene", which in 5e means 1d4 hours. The Wept hits 28 ×2 against 20–28 HP. "Stable when the scene ends" still means death saves until then, so a PC can die against the module's own rule. Leashed's throw punishes whoever lands the last blow. | Add a **Not Its Quarry** rule: a creature the Uninvited drop is automatically stable and wakes at the next beat with 1 HP and a level of exhaustion. Give Leashed's throw a save and put it in the next beat, not on the spot. |
| K2 | **"Force buys time" has no mechanics** | Play C2, Combat M9 | Midnight has no clocks, and damage does nothing. 157–187 HP with weapon resistance means the Wept's Bloodied Fracture is out of reach. The Radiant's *The Rite* can never fire (Multiattack excludes it). | Add a **Hunt clock** per Uninvited: every 20 damage in a round, or any condition that lands, pushes the errand back one segment. Bloodied means "a quarter of HP lost" for Fracture purposes. Put *The Rite* in Multiattack. |
| K3 | **The gate fight (S3) has no battlefield** | Play M, Combat C1 | Enemies are behind a gate barred from the far side, with no way through. The morale line says **or**, the ending says **and**, and that choice swings the fight from 14% to 75–85% chance of a PC dropping. The fire clock makes standing still the best play. | Add a sally port/wicket (DC 15 Athletics or 13 Thieves' Tools, or it opens on a sergeant's parley). Morale: **or**. The fire clock advances only while the party is not engaging or negotiating. |
| K4 | **Scaling puts five PCs on the "4th–5th level" line** | Combat C2 | The default five-pregen table gets over-scaled fights (scaled S13: 39% chance of a wipe, in a fire). Real 5th-level parties get fights at about half of Low. | Split each scaling line into "+1 PC: add one retainer" and "4th–5th level: …". Retune S13 to Moderate. |
| K5 | **It is two sessions, not one** | Play C3 | 84k words against the source's 37k. Realistic runtime 6.5–7.5 hours. | Sell it as two sessions, split at Movement IV (the audit's recommended cut), with a "one-night cut" sidebar listing what to drop. |

## Major themes

1. **Timing contradictions.** The last bell rings before the gate fight while the
   Bought's contract ends at that bell. The Crossing is in VII on the tracker but in VI
   in Chapter V. The appointment is "after the bells" yet S9 runs before midnight.
2. **The canon ending fails by default.** With no PC at the river gate, the rules as
   written trigger ⟨The child is taken⟩. Make Vell's escape the default unless players
   actively interfere.
3. **Unhandled spell answers.** *Tiny hut* (a safe room until the last bell), Web or a
   grapple on a Witnessed Radiant, *blindness*, *sanctuary*, *invisibility* on Veier,
   *slow*. Ward-steering has no use or duration limit (96% success next to Raunu, which
   holds the Wept off forever).
4. **Crowds and collateral.** No rules for 200 guests: area spells in the ballroom,
   collateral deaths, the Hollow's door rule, other retinues joining at the gate.
5. **Fights are back-loaded.** Before Movement V the only fight is a fistfight; then
   five cards fire at once, and the default heat sends several factions hot by midnight.
   Move one snake card into Movement II–III and lower the default heat.
6. **Individual cards.** S9's Provocation loop fills its clock before the party can
   act. S13 plays at High difficulty and its fire kills downed PCs. The XP budget
   undershoots multiattack NPCs, and the pregens are soft (mean AC about 13).
7. **Early violence.** Drawing in Movement I benches a player; there is no guidance for
   a snake leader killed early or for attacking Raunu at the summons.
8. **Prep load.** About 48–56k words of required reading; the "one-page" tracker is
   about six pages with six heat tracks and 13 clocks. Needs a true one-page MM sheet
   and **a map** (B13 even mentions "the plan").
9. **Heroic Inspiration is binary in 5e**, so about 20 printed awards mostly do nothing.
   Use a small token pool (max 3) as an explicit house rule, or convert to XP.
10. **Canon wording (owner-facing):**
    - **A-2:** the Uninvited are called "it" 44 times. The owner's ruling is that they
      are people.
    - **A-3:** "the one winnable fight" is contradicted by S6–S13.
    - **A-4:** Callun can learn of the heir with no player involved. This is invention
      #9 and needs a ruling.
    - Seven inventions are unlogged.
    - Four read-aloud boxes tell players what they think or see.
11. **Trademark and licence housekeeping.** Remove "D&D" from the flow page header.
    Add the SRD attribution to Chapter 11 and the flow page. Add a note of changes
    (CC BY 4.0 asks for one).
12. **Split party.** No guidance for four players in four rooms during Movements I–V.

Minor findings (43) are in the source reports.

## Owner rulings needed

1. **A-4:** can a snake learn of the heir without a player involved (invention #9)?
   Recommended: no; Callun's knife learns only "the house is hiding someone upstairs".
2. **K5:** accept two sessions as the default, split at Movement IV?
3. **Source contradictions:** the testament witnesses (paid strangers, or Corval and
   Mother Sella), sixty or eighty servants, and the honor-guard count.
4. **History purge:** rewrite branch history to remove the pre-scrub inventions text,
   or leave it?
5. **The "Review these first" list** in `INVENTIONS_5e.md`, especially #2, #9, #13
   and #17.

## Recommended fix order

K1 → K2 → K3 → K4 → timing (1) → default canon ending (2) → spell answers (3) → crowds (4)
→ card fixes (5, 6) → prep sheet and map (8) → Inspiration (9) → canon wording (10)
→ licence housekeeping (11) → K5 split → prose.
