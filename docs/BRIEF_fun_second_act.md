# BRIEF — The Second Act: Open That Expires, and a Strike That Chooses

**Date:** 2026-09-08 · **Tier:** Brain · **Source:** `docs/RESEARCH_fun_audit_2026-09.md` §4.3, §9 R2/R3/R7
**Feeds:** `docs/DESIGN_fun_second_act.md`, `docs/TASKS_fun_second_act.md`
**Sequence (owner ruling S1, DECISIONS D19):** this brief is simmed and settled **before** `BRIEF_oraga_rewrite.md` tunes its scene cards. It is independent of the Lineage and Val'loh briefs and may run in parallel with them.
**Shape of the deliverable:** two rules changes, each gated by simulation, each adopted or rejected on the numbers; then the same-commit sync the iron law prescribes (III.3 body text, Table III.3-3 and the quick-reference tables, MM5, Quick Start's combat primer, `facet.yaml`, `combat.py`, the simulator, the app's strike confirm), and a rewritten Guardian vignette so the book shows the result.

---

## 1. The problem, in one paragraph

Under current rules every Named and Boss fight has one shape: the first 10+ hangs Open on the enemy, every later Strike from anyone is at +4 or better (72% full success, 89% with any extra die), and the enemy's only answer forfeits its one attack. A solo Boss has a median of two exchanges; its phase at Resolve 2 fires in the exchange the fight ends; the vignette that teaches the exchange is six consecutive full successes against a Boss that "is Measured — it always is." The fight has a slope and no tension on it, and the Strike is always the same sentence (`RESEARCH_fun_audit_2026-09.md` §4.2–4.4). The comparative landscape's finding: every well-liked fast-combat system has a real decision before the roll or real agency after it, and the most praised have both (`RESEARCH_comparative_combat_landscape.md` §2.4).

## 2. R2 — Open clears at the end of the exchange

**Rule (draft):** *A full-success Strike may leave the enemy Open: Easy to Strike for everyone **until the end of this exchange.** Open clears with the Tier 1 Conditions. An enemy that is Open may still act.*

**What it changes.** Open becomes a tempo tag ("exploit it *now*") instead of a switch flipped once; the enemy keeps its action, so a Named or Boss can change stance, use a Technique, or press a target while Open, which is the enemy texture MM1 built and the book never shows; a Boss fight lengthens toward the 3–4 band without adding Resolve, so phases have room to land mid-fight.

**Data.** `combat.enemy_durability.open_clears: end_of_exchange` (the field exists; the value is new; keep `enemy_action` as the legal alternative so a setting could choose it). Engine: `end_exchange` clears `enemy.open` when the mode says so (today it deliberately does not — `combat.py:670-679`); `open_clear_mode` consumers in `websocket.py` and the simulator's `_should_clear_open` policy read the mode rather than assuming the enemy-action spend. Boss `special_no_clear_open` (the Guardian's Reduced Mode) becomes meaningless under this mode and the phase must be re-authored (§5).

**Sim acceptance** (Series-10 method: `run_simulation`, n=200, seeds 1/2/3/7/42, default AI, PS-3 `standard_party()`):
- Solo Archive Guardian median **3 exchanges** (was 2), mean ≤ 4.5, win rate still ~100% (a solo Boss is not an encounter by MM1), Sparks spent ≥ 5/9 and Endurance drawn down (the "expensive" signal from G1).
- Recipe Table rows at PS-3 hold their bands within ±5 percentage points: Standard 65–85%, Hard 40–60%, Deadly 15–35%. If a row drifts out, retune Boss/Named Resolve by −1 first, never the recipe.
- Guardian phase (Resolve ≤ 2) fires in ≥ 60% of runs *before* the final exchange.

**Reject if:** any recipe row leaves its band after a one-point Resolve retune, or the Guardian median exceeds 5. Then fall back to the alternative in the audit: keep persistent Open and move phase thresholds to half Resolve.

## 3. R3 — A 10+ Strike chooses one rider

**Rule (draft, Table III.3-3's full-success row):** *10+ — deplete 2 Resolve **and choose one**: **Open** (Easy to Strike for everyone until the end of the exchange); **Position** (you or an ally of your choice may act as though a Maneuver's full success applied against this target — Easy for the *next* roll against it, this exchange or next); or **Cover** (name an ally: their next reaction this exchange is free). 7–9 — deplete 1; the MM names the cost. 6− — a consequence for the attacker.*

**Why these three.** They are the three things the fight already lets you do, folded into the roll that everyone actually makes: Open is today's option; Position is the Maneuver result (which stops being dominated because it now arrives on a Strike, and Maneuver stays for the character who wants the *action* rather than the rider); Cover is Intercept's effect without the Endurance, the mechanic every report on record calls a peak, arriving as a reward for a good hit. The choice is made after the roll, which is the first post-roll decision in combat that is not "pay or don't." Three options, one line each, one row on the card; no arithmetic.

**Interactions.** Open and Position are both Easy tags and do not stack (III.1's precedence rule already says so). Cover is a free reaction, not a free Dodge success; the roll still happens. Against a Mook a 10+ removes it and no rider applies. Against another character (PvP) the row is unchanged (Tier 2 Condition). Techniques that key off "leave the enemy Open" (*Overwhelming Force*, the natural 12's example) read "choose a rider" instead; *The Final Blow* is unaffected.

**Data.** `combat.enemy_durability.strike_riders: [open, position, cover]` with a short def per rider (`{id, label, effect, duration}`), so the app renders the three-way confirm from data and a setting can add or remove a rider. Engine: the existing Open confirm on a 10+ (`final_blow_confirm`'s sibling path; `websocket.py:1778` `open` flag) becomes a `rider` field; `combat.py` gains `apply_rider(...)`; Character/enemy state gains nothing new (Position writes an Easy tag on the target scoped to a roll count; Cover writes a one-shot flag on the ally). Simulator: a rider policy (`open` if target not Open; else `cover` on the lowest-Endurance ally if an attack is incoming; else `position`) plus a "worst case" policy of always-Open so the snowball is still measured at its strongest.

**Sim acceptance.** Same harness. Bands hold as in §2. Additional: with the "mixed" rider policy, mean PCs-Broken in the Hard row does not rise more than 0.1 over the Open-only policy (Cover must not make the party unbreakable) and does not fall below it by more than 0.15 (Cover must matter). Decision-count instrumentation: log rider choices per exchange so the DESIGN can report "decisions per exchange" as a number.

**Reject if:** Cover breaks the Hard/Deadly rows by more than the band tolerance after one Resolve retune; then ship R3 with two riders (Open, Position) and note Cover as a future Technique instead.

## 4. What the book changes (same commit as the data and engine)

- III.3 *Strike* (the enemy paragraph and Table III.3-3), *Maneuver* (one sentence: the Strike's Position rider is the Maneuver result arriving on a hit; Maneuver remains the action for reshaping the fight without striking), *Reactions* (Cover, one sentence under Intercept), the Combat Quick Reference tables III.3-12 and the exchange flow's step 5.
- III.1 *The Natural 12* example ("the enemy is left Open without you having to choose") → "you take a rider without having to choose."
- MM1 *Enemy Stat Blocks* paragraph ("Spending that action is your legitimate anti-snowball move") → rewritten: Open expires on its own; the enemy's anti-snowball moves are stance, Technique, and target.
- MM5 card: Strike Outcomes and Reactions rows.
- Quick Start combat primer line 3.
- II.4a *Overwhelming Force* Normal line; *The Final Blow* Normal line.
- Glossary: Open (duration), Rider, Cover, Position.
- INV-14 (Technique headers agree with yaml) and INV-9/10 regenerate.

## 5. R7 — show it: the Guardian vignette and the Bestiary phase

Rewrite *In Play: The Archive's Guardian* (III.3) so the Boss **changes stance once** (a conduct trigger the MM states aloud: Measured while both arms work; Aggressive once Open), **acts while Open** (the party's exchange-two decision is whether to spend the Open on damage or on Cover for Mordai), and **lands one Technique** (Telegraphed Finisher from MM1, telegraphed one exchange ahead so the table sees Intercept matter). At least one roll in the vignette must be a 7–9 and one a 6−, per the style guide's example-of-play rule. Re-author the Guardian's Reduced Mode phase for the new Open (it can no longer "never clear Open"; give it one of MM1's four legal levers — recommended: *raise its danger* — its blows land Tier 2 again and it fixes on whoever Opened it). Update `enemies/archive_guardian.fof`, `combat_sim.py`'s `archive_guardian_def()`, the Bestiary marker (generated), and the TR.

Sweep the Bestiary's other two Bosses (`bought_captain`, `glassback_bull`, `the_unfinished`) for phases or Techniques that assume persistent Open; re-author any that do.

## 6. Tests

- Data: `open_clears` accepts both values; `strike_riders` loads; unknown rider id rejected.
- Engine: Open set on a 10+ clears at `end_exchange` under the new mode and does not under `enemy_action`; each rider applies its effect exactly once and expires as specified; Open and Position do not stack; Cover makes exactly one reaction free and only for the named ally; Mooks take no rider; PvP unchanged.
- Simulator: rider policies selectable; the Series-10 harness reproduces prior numbers under `open_clears: enemy_action` (regression guard) before the new numbers are recorded.
- App: the strike confirm offers three riders from data; the MM's relay events carry `rider` and `open_until`.
- Docs: INV-9/10/14 green; the vignette's rolls reconcile with the printed modifiers (there is a test for worked arithmetic in the PHB examples; extend it to this vignette).

## 7. Order of work

1. Regression run of Series 10 under current data (baseline numbers into `research/simulation_log.md` Series 12 Part A).
2. R2: data value + `end_exchange` hook + sim policies; Series 12 Part B; adopt/reject.
3. R3: data + `apply_rider` + app confirm + sim policies; Series 12 Part C (riders on top of the adopted R2 state); adopt/reject/trim to two riders.
4. Book sync (§4) and the Guardian rewrite (§5); DECISIONS entry D20 with the numbers.
5. Hand the adopted rules to `BRIEF_oraga_rewrite.md` §11 for S2/S3 tuning.

## 8. Watch-outs

- **Do not fix length with Resolve.** The audit's do-not list and Series 7 both showed that buys exchanges, not tension. Retune by at most one point and only to hold a recipe band.
- **The riders must stay three.** A fourth option on the most common outcome is where PbtA pick-lists stop being fast.
- **Cover is the risky one.** It is Intercept for free; the sim gate on PCs-Broken exists to catch it making the party unbreakable.
- **Enemy stances now matter more**, because an Open enemy acts. Every Named/Boss in the core examples needs a `triggers:` line before the vignette is rewritten (audit R7).
