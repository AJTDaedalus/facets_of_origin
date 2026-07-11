# PT03 — Boss Stress Test: Results

**Scenario:** The Iron Crucible (`scenario.md`)
**Task:** A13 — human acceptance test for D1/D2 (Resolve durability + armor budget)
**First run:** 2026-07-11 (escalated — see below)
**Re-run:** 2026-07-11, post-A14, against the revised §5-quater Accept
**Party:** Standard PS-3 party — Mordai, Zahna, Zulnut (Option A)
**Driver:** `playtest/03_boss_stress_test/run_pt03.py`

---

## Re-run verdict (2026-07-11, post-A14, revised Accept §5-quater) — **PASS**

The first run (below) escalated two blockers to Planner: a void-derived win-rate Accept bar (F0) and an incoherent Boss phase-change subsystem (F3–F5, F8). Both were resolved — the Accept was revised (DESIGN §5-quater item 1: win rate is *reported, not gated*; gate on exchanges + cost + phase-fire) and **A14** rebuilt the phase subsystem (enemies no longer react/self-deplete via Parry — F5/F8; the phase-crossing invariant is enforced and tested — F4; MM1's phase vocabulary was made D1-native — F3). This is the re-run against that revised bar, with the buggy parry/phase model gone.

| Revised Accept criterion (§5-quater) | Result (n=300 × 7 seeds) | Status |
|---|---|---|
| (a) median **≥ 3 exchanges** | median **3** in every seed (min 3) | **PASS** |
| (b) cost signal **recorded** | Sparks **6.6–6.7 / 9** (~2.2/player); Endurance remaining **~1.6–1.7**; PC-Broken **0.20–0.33/fight** | **PASS** |
| (c) phase change fires in a **meaningful fraction** | **100%** (was ~0% pre-A14) | **PASS** |
| No house rules | ran entirely by the book | **PASS** |
| Win rate | 99.3–100% — *reported, not gated* (lone Boss vs. full party is not an even fight by doctrine) | reported |

**Median ≥ 3 held without any Boss Resolve retune** — the sanctioned §5-bis scalar lever was not needed. The near-empty Endurance-remaining (~1.7) and ~2.2 Sparks/player are the cost signal that evidences "survivable but expensive": the party wins, but arrives at the kill with pools drained and Sparks nearly gone. The phase now fires structurally every fight (defeat requires depleting past the mid-Resolve threshold), landing around exchange 2 of a 3-exchange fight — the mid-fight pivot the scenario was written to test.

**A13 CLOSED.** The escalation-era write-up is preserved below as the record of how the phase subsystem gap was found.

### Re-run aggregate — 7 seeds × n=300 (post-A14)

```
seed   win     exch(mean/med/min/max)   phase-fired   Broken/fight   Sparks/9   End-remain
  1    100.0%   3.3 / 3 / 3 / 6            100%          0.21           6.7        1.7
  2    100.0%   3.4 / 3 / 3 / 8            100%          0.27           6.7        1.6
  3    100.0%   3.3 / 3 / 3 / 7            100%          0.21           6.7        1.7
  7    100.0%   3.3 / 3 / 3 / 6            100%          0.22           6.7        1.7
 13     99.3%   3.4 / 3 / 3 / 7            100%          0.33           6.6        1.6
 42    100.0%   3.3 / 3 / 3 / 6            100%          0.22           6.6        1.7
 99    100.0%   3.3 / 3 / 3 / 6            100%          0.20           6.7        1.7
```

Median 3 and 100% phase-fire are stable across every seed; the min never dropped below 3 (the pre-A14 min was 1). Zahna (the fragile Mind PC run as a weak striker — F7) absorbs most of the Broken incidence.

### Re-run narrative — seed 1 (the "table session")

*Verbatim from the engine (`--table --seed 1`).*

- **Exchange 1** — All three open Aggressive and focus-fire. Mordai `[3,5]+2 = 11` full → −2 Resolve **+ Staggered rider (T2)**; the rider drops the Crucible's difficulty to **Easy**, so Zahna strikes at Easy (`[4,4]−1 = 9` partial, −1) and Zulnut at Easy (`[4,6]+2 = 14` full, −2 **+ Cornered rider**). Resolve 12 → 7. Forge Slam hits Zahna (Dodge fails → Staggered) and Zulnut (Parry partial → Winded). *(The enemy no longer Parries or spends Resolve to defend — A14/F5.)*
- **Exchange 2** — Mordai `[5,6]+2 = 15` full (Easy) → Resolve 7 → **5, crossing the threshold-6 phase**: *"the Crucible's shell cracks — Heat Surge online."* Zahna and Zulnut Withdraw from 0 Endurance to recover. Heat Surge lands Winded on Mordai. The mid-fight pivot fires exactly as scenario.md intended (line 94).
- **Exchange 3 (Cracked Shell, atk +3)** — The recovered party finishes it: Mordai → Resolve 3, Zahna → 1, Zulnut → **0, defeated.**

**Result:** party wins in **3 exchanges**, **0 Broken**, everyone ends at Endurance 2, **7/9 Sparks spent.** The phase change fired mid-fight and reshaped the last two exchanges (Heat Surge pressure + the recovered PCs re-engaging) — the flagship beat PT03 exists to validate, now working.

---

## Original run verdict (pre-A14 — escalated to Planner, since resolved)

> *Historical. The blockers below (F0 = void-derived Accept; F3–F5/F8 = phase subsystem) were resolved by the §5-quater revision and task A14. Retained as the discovery record.*

**The acceptance criteria as written cannot be met, and the reason is a finding, not a failure of the run.** Two of the three criteria are in direct conflict with rules the project settled *after* this scenario and task were authored:

| Accept criterion | Result | Status |
|---|---|---|
| Boss fight runs **≥ 3 exchanges** | mean **2.9**, median 3, min 1, max 7 | **Borderline fail** — many fights end in 2 |
| Won at **≈ Hard rates (~50%)** | **99.7%** win (299/300) | **Fail** — but the criterion is void-derived (see F0) |
| **No house rules required** | True — ran entirely by the book | **Pass** |

The 99.7% is not a bug. It is the same action-economy truth the project already ratified in **DESIGN §5-bis** and wrote into the PHB at **III.3:325**: *"A lone Boss facing a full party is not meant to be an even fight on its own — a party concentrating its Strikes will grind through any Resolve pool eventually."* PT03 was designed (scenario.md line 38, "test the Boss mechanics straight," no lateral solution) to produce exactly the matchup canon now says is trivial. **A13's "won at approximately Hard rates" criterion is the last surviving instance of the Q3-voided "Hard ≈ 50%" win-rate mapping.** It needs the same revision G1 and G4 already received. See the escalation in `docs/LOG_v0.3_ruleset_revision.md`.

More seriously, the run surfaced that **the flagship mechanic PT03 exists to validate — the phase change — barely fires under the current engine**, for reasons unrelated to the action-economy problem. That is the real payload of this playtest (findings **F3–F5, F8**).

---

## Methodology — "by the book"

- **Every roll and rule computation routes through `app.game.combat`** — the same module the WebSocket server uses. The driver supplies only the Iron Crucible's *authored* stat-block behaviour (Forge Slam, Heat Surge, the phase change); it re-implements no rule. This satisfies the C1 constraint (*"the simulator may only drive `app/game/combat.py`"*).
- **Modifier columns reconciled against the sheets** (`characters/*.fof`):
  - **Mordai** — Strike `2d6+2` (Str +1, Combat Practiced +1); Dodge `2d6+0` (Dex 2); Endurance 5; Con +1.
  - **Zahna** — Strike `2d6−1` (Str −1, no Combat); Dodge `2d6+1` (Dex 3); Endurance 3; Con −1. *(See F7: her Inscription magic is not modelled — she is run as a weak striker, the conservative assumption for a stress test.)*
  - **Zulnut** — Strike `2d6+2` (**Finesse**: Dex +1, Finesse Practiced +1, per the Phase-0 "Strike accepts any attribute/skill" rule); Dodge `2d6+1` (Dex 3); Endurance 3; Con −1. *(The stock `zulnut_def()` in `tools/combat_sim.py` strikes at +0 — an undercount corrected here; see F6.)*
- **Zero house rules.** Where the rules were silent or the scenario predated D1, the run used the literal current rule and the gap was logged as a finding rather than patched.

---

## The Iron Crucible — as actually run (D1-translated)

`scenario.md` was authored **2026-03-15, before the D1 Resolve rewrite** (A1–A11). Its stat block speaks the retired condition-track vocabulary. Translated faithfully into the current model:

| scenario.md (pre-D1) | As run (D1) | Finding |
|---|---|---|
| Endurance 10 | **Resolve 10** → effective **12** (heavy armor +2) | F1 |
| TR 13 (old durability formula) | **TR 16** = offense 4 + resolve 10 + armor 2 | F1 |
| Phase on "first Tier 2 condition" | Phase re-keyed to **Resolve threshold 6** (half of 12) | F2 |
| Phase: armor cracks Heavy→Light | **No mechanical effect** under D1 (see F3) | F3 |
| Phase: attack +2 → +3; posture Aggressive → Measured | Modelled as authored | — |
| Heat Surge (Con check or Winded) | Modelled as authored | — |
| Forge Slam (two targets/exchange) | Two attacks/exchange vs the two lowest-Endurance PCs | — |

---

## Narrative run — seed 13 (the "table session")

*Postures, dice, and outcomes below are verbatim from the engine.*

**Exchange 1** — All three PCs open Aggressive and focus-fire.
- Mordai Strikes: `[6,6]+2 = 15` full success. The Crucible **Parries** (partial) — net **−1 Resolve** *and it pays 2 Resolve for the Parry itself*. Resolve 12 → 9.
- Zahna Strikes: `[2,6]−1 = 8` partial. Resolve 9 → 8.
- Zulnut Strikes (Finesse): `[6,6]+2 = 15` full. Crucible Parries (partial). It pays 2 Resolve, takes −1. Resolve 8 → **exactly 6, then 5**.
- **Forge Slam** hits Zahna and Zulnut (both End 3). Zahna Dodges partial → Winded. Zulnut Parries → fails → **Staggered (Tier 2)**.
- *End of exchange:* both fragile PCs are at **0 Endurance**.

**Exchange 2** — Zahna and Zulnut Withdraw (0 Endurance, recovering). Only Mordai attacks.
- Mordai Strikes: `[5,6]+2 = 14` full. Crucible Parries → **fails** → full −2 depletion **plus a Staggered rider**. Resolve 5 → 1.
- Forge Slam hits the two Withdrawn PCs; Zahna → Staggered, Zulnut → Winded.

**Exchange 3** — The Crucible is Staggered (its own rider) → **Easy to Strike**.
- Mordai Strikes at Easy: `[4,6]+2 = 13` full → **−2 → Resolve 0. Defeated.**

**Result:** Party wins in **3 exchanges**. **Zero PCs Broken.** Everyone ends at Endurance 2. Sparks spent: 5/9. **The phase change never fired** — the Crucible died Intact.

---

## Aggregate (n = 300, seed 1)

```
Win rate:           99.7% (299/300)
Exchanges:          mean 2.9, median 3, min 1, max 7
PCs Broken/fight:   mean 0.20   (Zahna 38, Zulnut 22, Mordai 1 — the fragile PCs)
Sparks spent/fight: mean 5.3 of 9
```

**Phase-change fire rate under the by-the-book run: near zero.** In the seed-13 narrative and the great majority of the 300 fights, the Crucible was defeated before crossing its Resolve-6 threshold, because it **spends its own Resolve to Parry** (F8) — accelerating its defeat past the very threshold it needed to survive to.

### Diagnostic — boss Parry disabled (n = 300)

Because III.3 never states what an enemy pays for a reaction (F5), I re-ran with the boss *not* Parrying (the "enemy reactions are free/absent" reading):

```
Win rate:  100.0%    Exchanges: mean 3.3, median 3, max 6
Phase fired: 300/300 (100%)    PCs Broken/fight: mean 0.21
```

With the self-depleting Parry removed, **the phase fires every fight** and the fight lasts marginally longer — but it is *still* a 100% curbstomp. This cleanly separates the two problems: the Parry interaction suppresses the phase mechanic, and *independently*, the lone-boss action-economy problem makes the fight trivial no matter what the boss does.

---

## Post-fight questions (scenario.md)

1. **How many exchanges?** ~3 (mean 2.9). Meets the letter of the ≥3 floor only at the median; a meaningful share of fights end in 2, one-shot outliers in 1.
2. **Did the phase change create a meaningful tactical shift?** **No — it almost never occurred.** When forced to occur (diagnostic), it arrived in the final exchange or two and changed nothing the party did, because the fight was already won. The "trade durability for danger, forcing a strategy pivot" design intent (scenario.md line 94) did not materialise. See F3/F4.
3. **When did the first PC get Broken? Avoidable?** Rarely Broken at all (0.20/fight, always Zahna or Zulnut). The fragile PCs survive by Withdrawing to 0-Endurance safety once emptied — the correct, available play. No death cascade observed.
4. **Did players spend Sparks? Regret?** Yes — 5.3/9 mean, mostly Press/finish against the Boss. No hoarding-under-pressure problem here because there was no real pressure; Sparks were spent to *end it faster*, not to survive.
5. **0-Endurance Absorb spiral — death sentence or manageable?** **Manageable, verging on irrelevant.** With A6 (the 0-Endurance escalation retired), an empty PC simply Withdraws and recovers 2/exchange. The "spiral" the scenario feared no longer exists in the rules.
6. **Was it fun? Epic even in defeat?** **Untestable as designed** — there is essentially no defeat to feel, and the flagship phase-change beat did not fire. The one genuinely good moment (exchange 3: the Crucible's own rider leaves it Easy to Strike for the killing blow) is the D1 rider mechanic working exactly as intended — but that is not what PT03 set out to validate.

---

## Findings

*Status added on re-run: **RESOLVED** findings were closed by the §5-quater revision and task A14; the re-run confirms.*

- **F0 — A13's "≈ Hard rate" acceptance criterion is void-derived.** ✅ **RESOLVED (§5-quater item 1).** It was the last live instance of the Q3-voided win-rate→difficulty mapping. Canon (§5-bis, III.3:325) already states a lone Boss vs. a full party is not an even fight. The Accept was revised: win rate is *reported, not gated*; the gate is exchanges + cost + phase-fire. Re-run PASSes it.
- **F1 — `scenario.md` durability/TR are pre-D1.** Endurance 10 → Resolve 10 (eff. 12); TR 13 → 16. The *driver* runs the D1 translation faithfully; the scenario prose still carries the pre-D1 stat block. Cosmetic doc debt, not a rules gap — left as-is (updating the archival scenario prose is out of A13's scope).
- **F2 — `scenario.md` phase trigger has no D1 analogue.** "First Tier 2 condition" — enemies have no condition track. Re-keyed to Resolve threshold 6 in the driver; same doc-debt note as F1.
- **F3 — The phase's flagship effect is hollow under D1.** ✅ **RESOLVED (A14).** "Armor cracks Heavy→Light" is a no-op under D1 (armor is a flat one-time Resolve bonus). A14 rewrote MM1's Boss phase vocabulary to what the engine honours — raise danger / grant-revoke a Special / second wind / MM-narrated targeting — and explicitly forbade the "crack own armor" pattern. The Crucible's phase now uses `special_attack_mod` (+3) + Heat Surge, both engine-honoured; it fires and matters.
- **F4 — `phase_crossed` could be silently stepped over by a reaction-cost deduction.** ✅ **RESOLVED (A14).** With enemies no longer spending Resolve to react (F5), the only `resolve_current` changes are Strike depletions routed through `apply_resolve_damage`/`phase_crossed`; A14 added the exactly-on-threshold hardening tests. Re-run: phase fires 100%.
- **F5 — Enemy reaction cost was unspecified in III.3.** ✅ **RESOLVED (A14).** Ruling: **enemies do not react** — a Strike against a Named/Boss depletes Resolve by outcome only. `should_enemy_react` and both enemy-Parry blocks removed from the sim. This is why the driver shows the Crucible taking full depletion with no defensive Parry.
- **F8 — Enemy Parry was strictly self-defeating.** ✅ **DISSOLVED (A14, via F5).** With enemies not reacting at all, there is no self-defeating Parry to model.
- **F6 — `zulnut_def()` undercounts Zulnut's Strike (+0 vs the sheet's Finesse +2).** Still open (minor). Corrected in this driver via `pt03_party()`; the stock `tools/combat_sim.py` def is unchanged. Fixing the stock def so all sims match the sheet is a small follow-up, out of A13's scope.
- **F7 — Combat magic is unmodelled.** Still open (design, out of scope). Zahna's Inscription (control, not damage per III.3:514) has no engine representation, so a Mind PC contributes only a weak Strike in every simulation — our boss-fight data systematically omits one-third of a standard party's real toolkit. Flagged for a future workstream; makes the re-run's Broken/cost numbers *conservative* (the real party is stronger).

---

## Bottom line for the ruleset

D1/D2 **held up** in the acceptance test on both runs: Resolve depletion, the rider→Easy mechanic (the fight's best moment), the per-scene armor budget, and the retired 0-Endurance rule all behaved correctly with zero house rules. The first run's two blockers — a void-derived win-rate Accept bar (F0) and an incoherent Boss phase-change subsystem (F3–F5, F8) — were both resolved above the Worker tier (§5-quater revision + task A14). **The re-run passes the revised Accept on every count: median 3 exchanges, phase fires 100%, cost signal recorded (Sparks ~2.2/player, Endurance drained to ~1.7), no house rules.** The remaining open findings (F6 stock-def undercount, F7 unmodelled combat magic) are minor and out of D1/D2's scope, and both make the measured cost a conservative floor rather than a ceiling. A13 is closed; WS-A can close.
