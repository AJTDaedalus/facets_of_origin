"""Facets d20 simulator CLI. Drives ``facets_d20`` only; carries no rule logic.

    python -m tools.d20_sim fight --party fighter,rogue,wizard,priest --level 4 \\
        --foes owlbear,goblin_warrior:minion:3 -n 2000 --seed 1
    python -m tools.d20_sim encounters [--quick]    # Threat calibration, Tables 9–1..9–3
    python -m tools.d20_sim balance [--quick]       # §8 matrix: DPR, eDPR*, eHP, PI, band, swap
    python -m tools.d20_sim all [--quick] [--write] # both, then the report (and yaml with --write)

Results: ``software/research/facets_d20_sim_results.json``; report:
``docs/RESEARCH_facets_d20_sim.md``; with ``--write`` the fitted numbers go into
``facets_d20/data/facets_d20.yaml`` (``encounter_table``, ``encounter_adjustments``,
``monster_threat`` — the three fields DESIGN v0.2 §9 S-7 assigns to the simulator).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics
import sys
import time
from multiprocessing import Pool
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))

from facets_d20 import analysis as A  # noqa: E402
from facets_d20 import data as D  # noqa: E402
from facets_d20 import sim as S  # noqa: E402
from facets_d20.combat import RuleOptions  # noqa: E402

REPO = SOFTWARE.parent
RESULTS = SOFTWARE / "research" / "facets_d20_sim_results.json"
REPORT = REPO / "docs" / "RESEARCH_facets_d20_sim.md"
YAML = REPO / "facets_d20" / "data" / "facets_d20.yaml"
BASE_SEED = 20260928
LEVELS = list(range(1, 11))


def _call(args):
    fn, a, kw = args
    return fn(*a, **kw)


def pmap(fn, calls, procs):
    jobs = [(fn, a, kw) for a, kw in calls]
    if procs <= 1:
        return [_call(j) for j in jobs]
    with Pool(procs) as pool:
        return pool.map(_call, jobs, chunksize=1)


def sd(*key):
    return A.seed_for(BASE_SEED, *key)


# ================================================================ fight


def parse_foes(text):
    specs = []
    for part in text.split(","):
        bits = part.strip().split(":")
        mid, role, count = bits[0], "standard", 1
        for b in bits[1:]:
            if b.isdigit():
                count = int(b)
            else:
                role = b
        specs.append(S.FoeSpec(mid, role=role, count=count, leader=role != "minion"))
    return S.Encounter(tuple(specs))


def cmd_fight(a):
    party = [A.build_profile(p, a.level) for p in a.party.split(",")]
    s = S.simulate(party, parse_foes(a.foes), n=a.n, seed=a.seed,
                   resource_share=a.share)
    print(json.dumps({"summary": s.as_row(), "rounds_hist": s.rounds_hist,
                      "dpr_by_pc": {k: round(v, 2) for k, v in s.dpr_by_pc.items()},
                      "resources_spent": {k: round(v, 2) for k, v in s.resources_spent.items()}},
                     indent=2))


# ================================================================ encounters


def cmd_encounters(a, results):
    q = a.quick
    n_cal, n_fit, iters, n_eval = (150, 120, 7, 300) if q else (500, 300, 11, 700)
    n_val, samples = (60, 3) if q else (200, 6)
    t0 = time.time()
    # 1. calibrate the role multipliers
    calls = [((L, cr, role, n_cal, sd("cal", L, cr, role)), {})
             for L, cr in A.CALIBRATION_ANCHORS for role in ("minion", "boss", "never")]
    vals = pmap(A.task_calibrate, calls, a.procs)
    cal = {}
    for ((L, cr, role, *_), _), v in zip(calls, vals):
        cal.setdefault(role, []).append({"level": L, "cr": cr, "value": v})
    model = A.ThreatModel(minion_hp=statistics.median(x["value"] for x in cal["minion"]),
                          boss=statistics.median(x["value"] for x in cal["boss"]),
                          never=statistics.median(x["value"] for x in cal["never"]))
    results["calibration"] = {"anchors": cal, "model": model.__dict__}
    results["monster_threat"] = model.table()
    print(f"calibrated {model} in {time.time()-t0:.0f}s", flush=True)

    # 2. fit budgets: reference party, and the adjustment parties / tired party
    variants = [("ref4", False), ("ref3", False), ("ref5", False), ("ref6", False), ("ref4", True)]
    calls = [((pk, L, tier, model, n_fit, iters, sd("fit", pk, tired, L, tier)),
              {"tired": tired}) for pk, tired in variants for L in LEVELS for tier in A.TIERS]
    fits = pmap(A.task_fit, calls, a.procs)
    table = {}
    for ((pk, L, tier, *_), kw), r in zip(calls, fits):
        key = pk + ("_tired" if kw["tired"] else "")
        table.setdefault(key, {}).setdefault(L, {})[tier] = r["total"]
    results["fits"] = table
    print(f"fitted budgets in {time.time()-t0:.0f}s", flush=True)

    # 3. evaluate each reference cell at a larger n (CIs), all shapes
    calls = [(("ref4", L, table["ref4"][L][tier], model, n_eval, sd("eval", L, tier)), {})
             for L in LEVELS for tier in A.TIERS]
    evals = pmap(A.task_eval, calls, a.procs)
    results["evals"] = {f"{c[0][1]}:{t}": e for c, e, t in
                        zip(calls, evals, [t for L in LEVELS for t in A.TIERS])}

    # 4. validation with real SRD monsters, six composition classes
    calls = [((L, tier, table["ref4"][L][tier], cls, k, model, n_val, sd("val", L, tier, cls, k)), {})
             for L in LEVELS for tier in A.TIERS for cls in A.COMPOSITION_CLASSES
             for k in range(samples)]
    results["validation"] = pmap(A.task_validate, calls, a.procs)
    print(f"validated in {time.time()-t0:.0f}s", flush=True)

    # 5. robustness: 20 random parties of four distinct presets at the L4 Clash budget
    rs = D.load()
    rng = random.Random(sd("robust"))
    ids = sorted(rs.presets)
    parties = [tuple(rng.sample(ids, 4)) for _ in range(20)]
    calls = [((None, 4, table["ref4"][4][tier], model, n_eval // 2, sd("rob", p, tier)),
              {"party_ids": p}) for p in parties for tier in ("clash", "battle")]
    rob = pmap(A.task_eval, calls, a.procs)
    tiers = A.tiers_spec()
    results["robustness"] = [
        {"party": list(c[1]["party_ids"]), "tier": t, "outcome": o,
         "landed": A.classify(A.Outcome(**{k: o[k] for k in A.Outcome.__dataclass_fields__}), tiers)}
        for c, o, t in zip(calls, rob, [t for _ in parties for t in ("clash", "battle")])]

    # 5b. a lone boss: the mark-up that makes the Clash budget buy a Clash, per level
    calls = [((L, table["ref4"][L]["clash"], model, 150 if q else 400, sd("solo", L)), {})
             for L in LEVELS]
    so = pmap(A.task_solo_factor, calls, a.procs)
    results["solo_boss"] = {"by_level": so,
                            "factor": statistics.median(x["factor"] for x in so),
                            "hp_lost_x1": statistics.fmean(x["hp_lost_x1"] for x in so)}

    # 6. the day (yaml adventuring_day: three Clashes, two short rests) and, for comparison,
    #    the hard day (four Clashes, short rests after the 1st and 3rd), reference party
    nd = 100 if q else 500
    calls = [((L, table["ref4"][L]["clash"], model, nd, sd("day", L)), {}) for L in LEVELS]
    results["day"] = pmap(A.task_day, calls, a.procs)
    calls = [((L, table["ref4"][L]["clash"], model, nd, sd("hardday", L)),
              {"clashes": 4, "rests": (1, 3)}) for L in LEVELS]
    results["hard_day"] = pmap(A.task_day, calls, a.procs)
    print(f"encounters done in {time.time()-t0:.0f}s", flush=True)
    return model


# ================================================================ balance


def all_builds():
    rs = D.load()
    out = [(p, "facets", "preset") for p in rs.presets]
    out += [(b, "facets", "sim_build") for b in rs.sim_builds]
    out += [(b, "srd", "srd") for b in rs.raw["balance"]["srd_baselines"]]
    return out


def cmd_balance(a, results, model=None):
    q = a.quick
    if model is None:
        model = A.ThreatModel(**results["calibration"]["model"])
    clash = {int(L): v["clash"] for L, v in results["fits"]["ref4"].items()}
    levels = D.load().raw["balance"]["levels"]
    builds = all_builds()
    t0 = time.time()
    n_days, n_swap, n_dpr = (60, 60, 300) if q else (300, 250, 2000)
    calls = [((b, src, L, clash[L], model, n_days, sd("pi", b, L)), {})
             for b, src, _ in builds for L in levels]
    results["pi"] = pmap(A.task_pi, calls, a.procs)
    print(f"PI in {time.time()-t0:.0f}s", flush=True)
    # the swap test (primary): common random numbers — one seed per level for every build
    calls = [((b, src, L, clash[L], model, n_swap, sd("swap", L)), {})
             for b, src, _ in builds for L in levels]
    results["swap"] = pmap(A.task_swap, calls, a.procs)
    calls = [((b, src, L, n_dpr, sd("dpr", b, L)), {}) for b, src, _ in builds for L in levels]
    results["dummy_dpr"] = pmap(A.task_dummy_dpr, calls, a.procs)
    results["build_kinds"] = {b: k for b, _, k in builds}
    print(f"balance done in {time.time()-t0:.0f}s", flush=True)


# ================================================================ report + yaml


def band_verdicts(results):
    """DESIGN v0.2 §8, balance pass (V32): the swap test is the primary measure.

    Swap score = median preset HP lost per fight ÷ the build's − 1 (positive = the party
    loses less with the build in it = stronger). Band: every preset and every sim build
    within ±band_pct at each level; each Facet's preset mean within ±facet_band_pct;
    hybrids (item 7) at or below their Facet's best pure build (+ swap_tolerance, the
    sampling noise) and not beating the pure builds at their jobs (DPR₁ / DPR₃, +
    job_tolerance). PI is reported as the secondary measure."""
    rs = D.load()
    bal = rs.raw["balance"]
    kinds = results["build_kinds"]
    facet_of = {p: rs.presets[p]["facet"] for p in rs.presets}
    out = {}
    for L in bal["levels"]:
        rows = {r["build"]: r for r in results["pi"] if r["level"] == L}
        sw = {r["build"]: r for r in results["swap"] if r["level"] == L}
        presets = [b for b in sw if kinds[b] == "preset"]
        med = statistics.median(sw[b]["hp_lost"] for b in presets)
        med_pi = statistics.median(rows[b]["pi"] for b in presets)

        def score(b):
            return 100 * (med / sw[b]["hp_lost"] - 1)

        def pi_pct(b):
            return 100 * (rows[b]["pi"] / med_pi - 1)

        srd = [b for b in sw if kinds[b] == "srd"]
        srd_med = statistics.median(sw[b]["hp_lost"] for b in srd)
        v = {"median_hp_lost": med, "median_pi": med_pi, "presets": {}, "sim_builds": {},
             "facets": {}, "srd": {}}
        for b in sw:
            x = {"swap_pct": score(b), "pi_pct": pi_pct(b) if b in rows else None,
                 "in_band": abs(score(b)) <= bal["band_pct"]}
            if kinds[b] == "preset":
                v["presets"][b] = x
            elif kinds[b] == "sim_build":
                v["sim_builds"][b] = x
            else:
                v["srd"][b] = x
        for f in ("body", "mind", "soul"):
            m = statistics.fmean(score(b) for b in presets if facet_of[b] == f)
            v["facets"][f] = {"swap_pct": m, "in_band": abs(m) <= bal["facet_band_pct"]}
        # the SRD baselines' median build against the preset median (negative = SRD weaker)
        v["srd_swap_pct"] = 100 * (med / srd_med - 1)
        v["srd_pi_pct"] = 100 * (statistics.median(rows[b]["pi"] for b in srd) / med_pi - 1)
        # item 7 (Amendment 2): hybrids pay
        roles = bal.get("roles") or {}
        rule = bal.get("hybrid_rule") or {}
        sw_tol = rule.get("swap_tolerance_pct", 0)
        job_tol = 1 + rule.get("job_tolerance_pct", 5) / 100
        dd = {r["build"]: r for r in results.get("dummy_dpr", []) if r["level"] == L}
        casters_of = bal.get("tradition_casters") or {}

        def as_list(x):
            return [x] if isinstance(x, str) else list(x or [])

        v["hybrids"] = {}
        for facet, rr in roles.items():
            pure = [b for b in as_list(rr.get("pure_martial")) + as_list(rr.get("pure_caster")) if b in sw]
            martial = [b for b in as_list(rr.get("pure_martial")) if b in dd]
            for h in as_list(rr.get("hybrids")):
                if h not in sw or not pure:
                    continue
                best = max(pure, key=score)
                trad, main = _tradition_and_main(h, L)
                tcasters = [b for b in as_list(casters_of.get(trad)) if b in dd]
                chk = {"swap_vs_best_pure": score(h) - score(best), "best_pure": best,
                       "dpr1_vs_martial_pct": (100 * (dd[h]["dpr_1"] / max(dd[b]["dpr_1"] for b in martial) - 1)
                                               if martial and h in dd and main == "steel" else None),
                       "dpr3_vs_caster_pct": (100 * (dd[h]["dpr_3"] / max(dd[b]["dpr_3"] for b in tcasters) - 1)
                                              if tcasters and h in dd else None),
                       "tradition_caster": trad, "main": main}
                applies = L >= rule.get("from_level", 4)
                chk["ok"] = (not applies) or (
                    chk["swap_vs_best_pure"] <= sw_tol
                    and (chk["dpr1_vs_martial_pct"] is None or chk["dpr1_vs_martial_pct"] <= 100 * (job_tol - 1))
                    and (chk["dpr3_vs_caster_pct"] is None or chk["dpr3_vs_caster_pct"] <= 100 * (job_tol - 1)))
                v["hybrids"][h] = chk
        # PI (secondary) vs the swap test: rank agreement
        both = [b for b in sw if b in rows]
        pi_rank = sorted(both, key=lambda b: -rows[b]["pi"])
        sw_rank = sorted(both, key=lambda b: sw[b]["hp_lost"])
        pos_pi = {b: i for i, b in enumerate(pi_rank)}
        pos_sw = {b: i for i, b in enumerate(sw_rank)}
        n = len(both)
        d2 = sum((pos_pi[b] - pos_sw[b]) ** 2 for b in both)
        v["swap_spearman"] = 1 - 6 * d2 / (n * (n * n - 1))
        v["pi_band"] = {b: abs(pi_pct(b)) <= bal["band_pct"] for b in presets}
        out[L] = v
    return out


def _tradition_and_main(build_id, level):
    from facets_d20 import build as B
    rs = D.load()
    entry = rs.presets.get(build_id) or rs.sim_builds.get(build_id)
    if entry is None:
        return None, None
    p = B.Picks.from_entry(rs, entry, level)
    src = B._casting_sources(rs, p)
    return (src[0][1] if src else None), B.picks_main_track(rs, p)


def fmt(x, d=1):
    return f"{x:.{d}f}" if isinstance(x, (int, float)) else str(x)


def write_report(results, args):
    tiers = A.tiers_spec()
    lines = []
    w = lines.append
    model = results["calibration"]["model"]
    day = {r["level"]: r for r in results["day"]}
    hard = {r["level"]: r for r in results.get("hard_day", [])}
    w("# RESEARCH — Facets d20 simulation: encounter tables and the balance band")
    w("")
    w(f"*Generated by `software/tools/d20_sim.py all{' --quick' if args.quick else ''}` "
      f"on {time.strftime('%Y-%m-%d')} (balance pass). Rules: `software/facets_d20/` (every roll "
      "through `combat.py`). Data: `facets_d20/data/*.yaml` v0.2, SRD ladder "
      "`software/facets_d20/data/srd_monsters.yaml`, SRD baselines "
      "`software/facets_d20/data/srd_baselines.yaml`. Base seed "
      f"{BASE_SEED}; each cell's seed is `crc32(repr((base, task key)))`, so any cell reruns "
      "alone. Raw numbers: `software/research/facets_d20_sim_results.json`. Method: "
      "`docs/DESIGN_facets_d20_engine.md`; the tuning log: `docs/RESEARCH_facets_d20_balance.md`.*")
    w("")
    w("## Headline")
    w("")
    ev4 = results["evals"]["4:clash"]
    bv = results.get("band")
    clash_rounds = [results["evals"][f"{L}:clash"]["rounds"] for L in LEVELS]
    w(f"- **Clash at 4th level** (budget {results['fits']['ref4'][4]['clash'] / 4:.0f} Threat per "
      f"character): {fmt(ev4['rounds'], 2)} ± {fmt(ev4['ci_rounds'], 2)} rounds, "
      f"{100 * ev4['hp_lost']:.0f}% party HP lost, {100 * ev4['win']:.1f}% wins, a PC drops in "
      f"{100 * ev4['p_drop']:.0f}% of fights, a PC dies in {100 * ev4['p_death']:.1f}%. "
      f"Clash length at 1st–10th: {min(clash_rounds):.1f}–{max(clash_rounds):.1f} rounds.")
    w(f"- **Threat model** (measured): a boss = {model['boss']:.2f} standards of its CR; a "
      f"minion carries √({model['minion_hp']:.1f} × its damage per turn); a foe that never breaks "
      f"× {model['never']:.2f}.")
    w(f"- **The adventuring day** (three Clashes, short rests after the 1st and 2nd): the "
      f"reference party survives it {100 * min(d['survived'] for d in day.values()):.0f}–"
      f"{100 * max(d['survived'] for d in day.values()):.0f}% of the time across 1st–10th"
      + (f"; a hard day of four Clashes and two short rests: "
         f"{100 * min(d['survived'] for d in hard.values()):.0f}–"
         f"{100 * max(d['survived'] for d in hard.values()):.0f}%." if hard else "."))
    if bv:
        for L in sorted(bv):
            v = bv[L]
            out_p = [b for b, x in v["presets"].items() if not x["in_band"]]
            out_s = [b for b, x in v["sim_builds"].items() if not x["in_band"]]
            scores = [x["swap_pct"] for x in list(v["presets"].values()) + list(v["sim_builds"].values())]
            w(f"- **Balance, level {L} (swap test):** {len(v['presets']) - len(out_p)}/"
              f"{len(v['presets'])} presets and {len(v['sim_builds']) - len(out_s)}/"
              f"{len(v['sim_builds'])} sim builds inside ±15% (range {min(scores):+.0f}% to "
              f"{max(scores):+.0f}%)" + (f"; out: {', '.join(out_p + out_s)}" if out_p or out_s else "")
              + "; hybrids above their Facet's best pure build: "
              + (", ".join(h for h, x in v.get("hybrids", {}).items() if not x["ok"]) or "none")
              + f"; the SRD baselines' median {v['srd_swap_pct']:+.0f}% vs the preset median.")
    w("")
    w("## 1. Method")
    w("")
    w("- **Fights.** `sim.Fight` runs the §6.1–6.2 rules: one d20 per side for initiative "
      "(Alert = advantage), bosses act at the top of the round and again in their side's half, "
      "boss resolve, fixed monster damage (crits rolled), minions, morale (standard foes at first "
      "Bloodied, minions when the leader falls), E1 one rider a turn, one reaction, concentration, "
      "death saves, Sparks as +1d6 after a roll. The tactical AI is documented in `sim.py`'s "
      "docstring and is the same for every build; every foe attacks a random standing PC (§6.2).")
    w("- **Resources.** A single fight gets ⅓ of each long-rest pool (rounded up, plus any "
      "short-rest regain) and all short-rest pools — one of the day's three Clashes. The day "
      "runner carries HP, pools, Hit Dice and Sparks across the day's fights with short rests "
      "between them, pacing pools evenly.")
    w("- **Foes for fitting.** Continuous-CR generic foes: a smooth fit over the SRD ladder "
      "(AC, HP, to-hit, damage per turn, saves); the ladder's share of non-weapon damage "
      "(about 15%) arrives as a separate strike, so resistances count. Three shapes averaged: "
      "four standards; a boss (60% of the Threat) + minions; two standards + minions. Minions "
      "are at most half the CR of a standard of the same budget (more of them, not a few "
      "high-CR ones).")
    w("- **Tier targets** (yaml `encounter_tiers`). The search hits the middle of the tier's "
      "party-HP-lost band (Skirmish 10%, Clash 27.5%, Battle 45%); Desperate hits the middle of "
      "its win band (72.5%). Rounds, wins and drops are then checked against the rest of the "
      "targets and reported, never tuned into the table.")
    w("- **Validation.** Real SRD ladder monsters in the six composition classes of §7, "
      f"{'3' if args.quick else '6'} random encounters per class and cell.")
    w("")
    w("## 2. Threat by CR and role (Table 9–2)")
    w("")
    w("Calibration anchors (party level, CR → measured value):")
    w("")
    w("| Role | " + " | ".join(f"L{x['level']} CR {x['cr']}" for x in results['calibration']['anchors']['boss']) + " | Median |")
    w("|---|" + "---|" * (len(results['calibration']['anchors']['boss']) + 1))
    for role, label in (("minion", "minion HP-equivalent"), ("boss", "boss = N standards"),
                        ("never", "never-breaks ×")):
        xs = results["calibration"]["anchors"][role]
        w(f"| {label} | " + " | ".join(fmt(x["value"], 2) for x in xs) + f" | {fmt(statistics.median(x['value'] for x in xs), 2)} |")
    w("")
    w("**Table 9–2: Threat by CR** (SRD 5.2.1 ladder, smooth fit)")
    w("")
    w("| CR | Standard | Minion | Boss |")
    w("|---|---|---|---|")
    for cr, v in results["monster_threat"].items():
        w(f"| {cr} | {v['standard']} | {v['minion']} | {v['boss']} |")
    w("")
    w("A foe that never breaks: × " + f"{model['never']:.2f}" + " (round to the nearest whole number).")
    w("")
    w("## 3. Encounter budget (Table 9–1): Threat per character, party of four")
    w("")
    w("| Level | Skirmish | Clash | Battle | Desperate |")
    w("|---|---|---|---|---|")
    for L in LEVELS:
        row = results["fits"]["ref4"][L]
        w(f"| {L} | " + " | ".join(str(round(row[t] / 4)) for t in A.TIERS) + " |")
    w("")
    w("**Outcomes at the fitted budgets** (reference party; mean ± 95% CI; misses a yaml target → named):")
    w("")
    w("| Level | Tier | Rounds | HP lost | Wins | PC drops | PC dies | Misses |")
    w("|---|---|---|---|---|---|---|---|")
    for L in LEVELS:
        for t in A.TIERS:
            e = results["evals"][f"{L}:{t}"]
            miss = target_misses(e, tiers[t]["targets"])
            w(f"| {L} | {t} | {fmt(e['rounds'], 2)} ± {fmt(e['ci_rounds'], 2)} | "
              f"{100 * e['hp_lost']:.0f}% ± {100 * e['ci_hp']:.0f} | {100 * e['win']:.1f}% | "
              f"{100 * e['p_drop']:.0f}% | {100 * e['p_death']:.1f}% | {', '.join(miss) or '—'} |")
    w("")
    w("## 4. Composition classes (real SRD monsters)")
    w("")
    w("Share of random real-monster encounters built to the budget that land in the intended "
      "tier (by party HP lost; ≥ 80% wanted, < 80% flagged ⚠). A solo boss is priced with "
      "the boss column (see §5 for the solo-boss line).")
    w("")
    w("| Tier | " + " | ".join(A.COMPOSITION_CLASSES) + " |")
    w("|---|" + "---|" * len(A.COMPOSITION_CLASSES))
    for t in A.TIERS:
        cells = []
        for cls in A.COMPOSITION_CLASSES:
            rs_ = [v for v in results["validation"] if v["tier"] == t and v["class"] == cls]
            ok = sum(v["landed"] == t for v in rs_) / max(1, len(rs_))
            hp = statistics.fmean(v["outcome"]["hp_lost"] for v in rs_)
            cells.append(f"{100 * ok:.0f}% (HP {100 * hp:.0f}%)" + (" ⚠" if ok < 0.8 else ""))
        w(f"| {t} | " + " | ".join(cells) + " |")
    w("")
    w("## 5. Adjustments (Table 9–3)")
    w("")
    adj = results["adjustments"]
    w("| Party | " + " | ".join(A.TIERS) + " | Rule |")
    w("|---|---|---|---|---|---|")
    for key, label in (("three_players", "Three players"), ("five_players", "Five players"),
                       ("six_players", "Six players"), ("tired", "Tired (50% HP, ½ resources)")):
        a_ = adj[key]
        w(f"| {label} | " + " | ".join(f"{100 * a_['by_tier'][t]:+.0f}%" for t in A.TIERS)
          + f" | {a_['rule']} |")
    w("")
    w("Percentages are the change in the whole encounter's Threat, averaged over levels 1–10.")
    if results.get("solo_boss"):
        sb = results["solo_boss"]
        w("")
        w(f"**Lone boss.** A boss with no other foes, priced at its boss Threat and built to the "
          f"Clash budget, costs {100 * sb['hp_lost_x1']:.0f}% party HP on average (Clash band "
          f"20–35%). The mark-up that makes it a Clash, by level: "
          + ", ".join(f"{x['level']}: ×{x['factor']:.2f}" for x in sb["by_level"])
          + f" (median ×{sb['factor']:.2f}).")
    w("")
    w("## 6. Robustness: 20 random parties")
    w("")
    rob = results["robustness"]
    for t in ("clash", "battle"):
        xs = [r for r in rob if r["tier"] == t]
        same = sum(r["landed"] == t for r in xs) / len(xs)
        w(f"- **{t.title()} budget at 4th level:** {100 * same:.0f}% of 20 random parties of four "
          f"distinct presets land in the {t.title()} band (≥ 80% wanted). Their HP lost ranges "
          f"{100 * min(r['outcome']['hp_lost'] for r in xs):.0f}–"
          f"{100 * max(r['outcome']['hp_lost'] for r in xs):.0f}%.")
    w("")
    w("## 7. The adventuring day")
    w("")
    w("| Level | Standard day (3 Clashes, 2 short rests) | a PC dies | Hard day (4 Clashes, 2 short rests) |")
    w("|---|---|---|---|")
    for L in LEVELS:
        hd = hard.get(L)
        w(f"| {L} | {100 * day[L]['survived']:.0f}% | {100 * day[L]['any_death']:.0f}% | "
          + (f"{100 * hd['survived']:.0f}%" if hd else "—") + " |")
    w("")
    if "pi" in results:
        write_balance(results, w)
    w("")
    w("## Findings")
    w("")
    for f in results.get("findings", []):
        w(f"- {f}")
    w("")
    w("*This work includes material from the System Reference Document 5.2.1 (\"SRD 5.2.1\") by "
      "Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd, licensed under CC BY "
      "4.0.*")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def target_misses(e, t):
    miss = []
    if e["win"] * 100 < t.get("win_pct_min", 0) - 0.5:
        miss.append("wins")
    if "win_pct_max" in t and e["win"] * 100 > t["win_pct_max"] + 0.5:
        miss.append("wins")
    lo, hi = t["rounds"]
    if not lo <= e["rounds"] <= hi:
        miss.append("rounds")
    lo, hi = t["party_hp_lost_pct"]
    if not lo <= 100 * e["hp_lost"] <= hi:
        miss.append("HP")
    if "any_pc_down_pct_max" in t and 100 * e["p_drop"] > t["any_pc_down_pct_max"]:
        miss.append("drops")
    return miss


def write_balance(results, w):
    bv = results["band"]
    kinds = results["build_kinds"]
    rs = D.load()
    role_of = {}
    for f, rr in (rs.raw["balance"].get("roles") or {}).items():
        for k, v in rr.items():
            for b in ([v] if isinstance(v, str) else v):
                role_of[b] = f"{f} {k.replace('pure_', '')}".replace("hybrids", "hybrid")
    w("## 8. Balance band (§8) — the swap test is primary")
    w("")
    w("**Swap test** (primary, balance pass V32): the reference party (Fighter, Rogue, Wizard, "
      "Priest) with the build swapped in for each member in turn plays standard days (three "
      "Clashes at the level's Clash budget, short rests between); **HP lost** is the party's "
      "share of hit points lost per fight, and **vs median** = the preset median ÷ the build's "
      "− 1, so +10% means the party loses a tenth less with the build in it. Common random "
      "numbers: every build at a level plays the same dice. Band: every preset and every sim "
      "build within ±15%. **PI** (secondary) = eDPR\\* × eHP over the same days beside three "
      "reference companions; **DPR₁/DPR₃** = damage per round against one / three dummies "
      "(the martial and casting jobs of item 7).")
    w("")
    for L in sorted(bv, key=int):
        v = bv[L]
        sw = {r["build"]: r for r in results["swap"] if r["level"] == int(L)}
        dd = {r["build"]: r for r in results["dummy_dpr"] if r["level"] == int(L)}
        allx = {**v["presets"], **v["sim_builds"], **v["srd"]}
        w(f"### Level {L}")
        w("")
        w("| Build | Kind | Role | Swap vs median | HP lost / fight | Rounds | Days survived | DPR₁ | DPR₃ | PI vs median | Verdict |")
        w("|---|---|---|---|---|---|---|---|---|---|---|")
        for b in sorted(sw, key=lambda b: sw[b]["hp_lost"]):
            x = allx[b]
            k = kinds[b]
            verdict = "SRD" if k == "srd" else ("in band" if x["in_band"] else "**out of band**")
            w(f"| {b} | {k} | {role_of.get(b, '—')} | {x['swap_pct']:+.0f}% | "
              f"{100 * sw[b]['hp_lost']:.1f}% | {fmt(sw[b]['rounds'], 2)} | "
              f"{100 * sw[b]['days_survived']:.0f}% | {fmt(dd[b]['dpr_1'])} | {fmt(dd[b]['dpr_3'])} | "
              + (f"{x['pi_pct']:+.0f}%" if x.get("pi_pct") is not None else "—") + f" | {verdict} |")
        w("")
        w("Facet means (swap) vs the preset median: " + ", ".join(
            f"{f} {x['swap_pct']:+.0f}%{'' if x['in_band'] else ' **(out)**'}" for f, x in v["facets"].items())
          + f". SRD baselines' median vs the preset median: swap {v['srd_swap_pct']:+.0f}%, "
          f"PI {v['srd_pi_pct']:+.0f}%.")
        if v.get("hybrids"):
            w("")
            w("Hybrids (item 7, from 4th level): swap score minus the Facet's best pure build's "
              "(≤ +3 points, sampling noise); if Steel is main, DPR₁ vs the Facet's best pure martial "
              "(+5%); DPR₃ vs the best pure caster of its tradition (+5%).")
            w("")
            w("| Hybrid | Swap vs best pure | DPR₁ vs pure martial | DPR₃ vs tradition's caster | Verdict |")
            w("|---|---|---|---|---|")
            for h, x in v["hybrids"].items():
                def pc_(y):
                    return "—" if y is None else f"{y:+.0f}%"
                w(f"| {h} ({x['main'] or '—'} main) | {x['swap_vs_best_pure']:+.0f} pts ({x['best_pure']}) | "
                  f"{pc_(x['dpr1_vs_martial_pct'])} | "
                  f"{pc_(x['dpr3_vs_caster_pct'])} ({x['tradition_caster'] or '—'}) | "
                  f"{'ok' if x['ok'] else '**beats a pure build**'} |")
            w("")
        w(f"PI (secondary) vs the swap test, rank agreement: Spearman {v['swap_spearman']:.2f}. "
          f"Presets inside ±15% on PI: {sum(v['pi_band'].values())}/{len(v['pi_band'])}.")
        w("")


def adjustments(results):
    f = results["fits"]
    out = {}
    for key, pk in (("three_players", "ref3"), ("five_players", "ref5"), ("six_players", "ref6"),
                    ("tired", "ref4_tired")):
        by_tier = {}
        for t in A.TIERS:
            by_tier[t] = statistics.fmean(f[pk][L][t] / f["ref4"][L][t] - 1 for L in LEVELS)
        clash = by_tier["clash"]
        if key == "tired":
            rule = (f"remove {abs(100 * clash):.0f}% of the Threat, or drop one tier"
                    if clash < 0 else "no change")
        elif clash < 0:
            rule = f"remove foes worth {abs(100 * clash):.0f}% of the Threat"
        else:
            rule = f"add foes worth {100 * clash:.0f}% of the Threat"
        out[key] = {"by_tier": by_tier, "rule": rule,
                    "by_level_clash": {L: f[pk][L]["clash"] / f["ref4"][L]["clash"] - 1 for L in LEVELS}}
    results["adjustments"] = out


def write_yaml(results):
    """Replace the three simulator-owned top-level fields (S-7) in facets_d20.yaml."""
    import yaml as _y
    text = YAML.read_text(encoding="utf-8")
    table = {L: {t: round(results["fits"]["ref4"][L][t] / 4) for t in A.TIERS} for L in LEVELS}
    adj = {k: {"clash_pct": round(100 * v["by_tier"]["clash"]), "rule": v["rule"],
               "by_tier_pct": {t: round(100 * x) for t, x in v["by_tier"].items()}}
           for k, v in results["adjustments"].items()}
    model = results["calibration"]["model"]
    mt = {"model": {"standard": "sqrt(HP x damage per turn)",
                    "minion": f"sqrt({model['minion_hp']:.1f} x damage per turn)",
                    "boss": f"standard x {model['boss']:.2f}",
                    "never_breaks": f"x {model['never']:.2f}",
                    "lone_boss": "boss x 1.2 (V42; measured mark-up "
                                 + (f"x{results['solo_boss']['factor']:.2f} median)" if results.get("solo_boss") else "pending)")},
          "by_cr": results["monster_threat"]}
    blocks = {
        "encounter_table": "# Threat budget per character (party of four), fitted by software/tools/d20_sim.py\n"
                           + _y.safe_dump({"encounter_table": table}, sort_keys=False, width=100),
        "encounter_adjustments": _y.safe_dump({"encounter_adjustments": adj}, sort_keys=False, width=100),
        "monster_threat": _y.safe_dump({"monster_threat": mt}, sort_keys=False, width=100),
    }
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        key = line.split(":", 1)[0] if line and not line.startswith((" ", "#")) else None
        if key in blocks:
            out.append(blocks.pop(key).rstrip("\n"))
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("#  ")):
                i += 1
            continue
        out.append(line)
        i += 1
    for rest in blocks.values():
        out.append(rest.rstrip("\n"))
    YAML.write_text("\n".join(out), encoding="utf-8")


def findings(results):
    """Short, generated findings; the tuning narrative is docs/RESEARCH_facets_d20_balance.md."""
    tiers = A.tiers_spec()
    out = []
    for t in A.TIERS:
        rr = [results["evals"][f"{L}:{t}"] for L in LEVELS]
        miss = sorted({m for L, e in zip(LEVELS, rr) for m in target_misses(e, tiers[t]["targets"])})
        out.append(f"**{t.title()}**: {min(e['rounds'] for e in rr):.2f}–{max(e['rounds'] for e in rr):.2f} "
                   f"rounds, {100 * min(e['hp_lost'] for e in rr):.0f}–{100 * max(e['hp_lost'] for e in rr):.0f}% "
                   f"HP lost, {100 * min(e['win'] for e in rr):.0f}–{100 * max(e['win'] for e in rr):.0f}% wins "
                   f"across 1st–10th" + (f"; yaml targets missed somewhere: {', '.join(miss)}." if miss else "; every yaml target met."))
    day = results["day"]
    out.append(f"**Day**: the reference party survives the standard day "
               f"{100 * min(d['survived'] for d in day):.0f}–{100 * max(d['survived'] for d in day):.0f}% of the time.")
    if results.get("band"):
        bad = [(L, b) for L, v in results["band"].items()
               for b, x in list(v["presets"].items()) + list(v["sim_builds"].items()) if not x["in_band"]]
        hyb = [(L, h) for L, v in results["band"].items() for h, x in v["hybrids"].items() if not x["ok"]]
        out.append("**Band (swap test)**: " + ("every preset and sim build within ±15% at 1st, 4th, 7th and 10th"
                   if not bad else "outside ±15%: " + ", ".join(f"{b} (L{L})" for L, b in bad)) + "; "
                   + ("every hybrid at or below its Facet's best pure build and under the pure builds' jobs."
                      if not hyb else "hybrid checks failing: " + ", ".join(f"{h} (L{L})" for L, h in hyb)))
    return out


def cmd_all(a):
    results = {"base_seed": BASE_SEED, "quick": a.quick}
    model = cmd_encounters(a, results)
    adjustments(results)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(results, indent=1, default=str))
    if not a.skip_balance:
        cmd_balance(a, results, model)
        results["band"] = band_verdicts(results)
    results["findings"] = findings(results)
    RESULTS.write_text(json.dumps(results, indent=1, default=str))
    write_report(results, a)
    if a.write:
        write_yaml(results)
    print(f"wrote {REPORT} and {RESULTS}" + (" and the yaml" if a.write else ""))


def cmd_report(a):
    results = json.loads(RESULTS.read_text())
    results["fits"] = {k: {int(L): v for L, v in d.items()} for k, d in results["fits"].items()}
    if "pi" in results:
        results["band"] = band_verdicts(results)
    write_report(results, a)
    if a.write:
        write_yaml(results)
    print(f"wrote {REPORT}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="d20_sim", description=__doc__.splitlines()[0])
    ap.add_argument("--procs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fight")
    f.add_argument("--party", default="fighter,rogue,wizard,priest")
    f.add_argument("--level", type=int, default=4)
    f.add_argument("--foes", required=True)
    f.add_argument("-n", type=int, default=2000)
    f.add_argument("--seed", type=int, default=1)
    f.add_argument("--share", type=float, default=S.DEFAULT_SHARE)
    for name in ("encounters", "balance", "all", "report"):
        p = sub.add_parser(name)
        p.add_argument("--quick", action="store_true")
        p.add_argument("--write", action="store_true")
        p.add_argument("--skip-balance", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "fight":
        cmd_fight(a)
    elif a.cmd in ("all", "encounters"):
        if a.cmd == "encounters":
            a.skip_balance = True
        cmd_all(a)
    elif a.cmd == "balance":
        results = json.loads(RESULTS.read_text())
        results["fits"] = {k: {int(L): v for L, v in d.items()} for k, d in results["fits"].items()}
        cmd_balance(a, results)
        results["band"] = band_verdicts(results)
        RESULTS.write_text(json.dumps(results, indent=1, default=str))
        write_report(results, a)
    elif a.cmd == "report":
        cmd_report(a)


if __name__ == "__main__":
    main()
