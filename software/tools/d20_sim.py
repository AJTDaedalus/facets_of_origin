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

    # 6. the day: four Clashes, two short rests, reference party, per level
    calls = [(("fighter", "facets", L, table["ref4"][L]["clash"], model, 60 if q else 250,
               sd("day", L)), {}) for L in LEVELS]
    results["day"] = pmap(A.task_pi, calls, a.procs)
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
    n_days, n_swap, n_dpr = (60, 60, 300) if q else (500, 200, 2000)
    calls = [((b, src, L, clash[L], model, n_days, sd("pi", b, L)), {})
             for b, src, _ in builds for L in levels]
    results["pi"] = pmap(A.task_pi, calls, a.procs)
    print(f"PI in {time.time()-t0:.0f}s", flush=True)
    calls = [((b, src, L, clash[L], model, n_swap, sd("swap", b, L)), {})
             for b, src, _ in builds for L in levels]
    results["swap"] = pmap(A.task_swap, calls, a.procs)
    calls = [((b, src, L, n_dpr, sd("dpr", b, L)), {}) for b, src, _ in builds for L in levels]
    results["dummy_dpr"] = pmap(A.task_dummy_dpr, calls, a.procs)
    results["build_kinds"] = {b: k for b, _, k in builds}
    print(f"balance done in {time.time()-t0:.0f}s", flush=True)


# ================================================================ report + yaml


def band_verdicts(results):
    rs = D.load()
    bal = rs.raw["balance"]
    kinds = results["build_kinds"]
    facet_of = {p: rs.presets[p]["facet"] for p in rs.presets}
    out = {}
    for L in bal["levels"]:
        rows = {r["build"]: r for r in results["pi"] if r["level"] == L}
        presets = [b for b in rows if kinds[b] == "preset"]
        med = statistics.median(rows[b]["pi"] for b in presets)
        med_e = statistics.median(rows[b]["edpr"] for b in presets)
        med_h = statistics.median(rows[b]["ehp"] for b in presets)
        srd_med = statistics.median(rows[b]["pi"] for b in rows if kinds[b] == "srd")
        v = {"median_pi": med, "srd_median_pi": srd_med, "presets": {}, "sim_builds": {},
             "facets": {}, "srd": {}}
        for b in presets:
            r = rows[b]
            v["presets"][b] = {"pi_pct": 100 * (r["pi"] / med - 1),
                               "in_band": abs(r["pi"] / med - 1) <= bal["band_pct"] / 100,
                               "edpr_pct": 100 * r["edpr"] / med_e, "ehp_pct": 100 * r["ehp"] / med_h,
                               "role_ok": 50 <= 100 * r["edpr"] / med_e <= 200
                               and 50 <= 100 * r["ehp"] / med_h <= 200}
        for f in ("body", "mind", "soul"):
            m = statistics.fmean(rows[b]["pi"] for b in presets if facet_of[b] == f)
            v["facets"][f] = {"pi_pct": 100 * (m / med - 1),
                              "in_band": abs(m / med - 1) <= bal["facet_band_pct"] / 100}
        for b in rows:
            if kinds[b] == "sim_build":
                p = 100 * (rows[b]["pi"] / med - 1)
                v["sim_builds"][b] = {"pi_pct": p, "ok": p <= bal["combo_ceiling_pct"]}
            if kinds[b] == "srd":
                v["srd"][b] = {"pi_pct": 100 * (rows[b]["pi"] / med - 1)}
        v["srd_ok"] = abs(med / srd_med - 1) <= bal["srd_band_pct"] / 100
        v["srd_pct"] = 100 * (med / srd_med - 1)
        # item 7 (Amendment 2): hybrids pay (DESIGN §8 item 7, balance.hybrid_rule)
        roles = bal.get("roles") or {}
        rule = bal.get("hybrid_rule") or {}
        pi_tol = 1 + rule.get("pi_tolerance_pct", 15) / 100
        job_tol = 1 + rule.get("job_tolerance_pct", 5) / 100
        dd = {r["build"]: r for r in results.get("dummy_dpr", []) if r["level"] == L}
        casters_of = bal.get("tradition_casters") or {}

        def as_list(x):
            return [x] if isinstance(x, str) else list(x or [])

        v["hybrids"] = {}
        for facet, rr in roles.items():
            pure = [b for b in as_list(rr.get("pure_martial")) + as_list(rr.get("pure_caster")) if b in rows]
            martial = [b for b in as_list(rr.get("pure_martial")) if b in dd]
            for h in as_list(rr.get("hybrids")):
                if h not in rows or not pure:
                    continue
                best_pi = max(rows[b]["pi"] for b in pure)
                trad, main = _tradition_and_main(h, L)
                tcasters = [b for b in as_list(casters_of.get(trad)) if b in dd]
                chk = {"pi_vs_best_pure_pct": 100 * (rows[h]["pi"] / best_pi - 1),
                       "dpr1_vs_martial_pct": (100 * (dd[h]["dpr_1"] / max(dd[b]["dpr_1"] for b in martial) - 1)
                                               if martial and h in dd and main == "steel" else None),
                       "dpr3_vs_caster_pct": (100 * (dd[h]["dpr_3"] / max(dd[b]["dpr_3"] for b in tcasters) - 1)
                                              if tcasters and h in dd else None),
                       "tradition_caster": trad, "main": main}
                applies = L >= rule.get("from_level", 4)
                chk["ok"] = (not applies) or (
                    rows[h]["pi"] <= best_pi * pi_tol
                    and (chk["dpr1_vs_martial_pct"] is None or chk["dpr1_vs_martial_pct"] <= 100 * (job_tol - 1))
                    and (chk["dpr3_vs_caster_pct"] is None or chk["dpr3_vs_caster_pct"] <= 100 * (job_tol - 1)))
                v["hybrids"][h] = chk
        # swap test agreement
        sw = {r["build"]: r for r in results["swap"] if r["level"] == L}
        pi_rank = sorted(rows, key=lambda b: -rows[b]["pi"])
        sw_rank = sorted(sw, key=lambda b: (sw[b]["hp_lost"], sw[b]["rounds"]))
        pos_pi = {b: i for i, b in enumerate(pi_rank)}
        pos_sw = {b: i for i, b in enumerate(sw_rank)}
        n = len(pi_rank)
        d2 = sum((pos_pi[b] - pos_sw[b]) ** 2 for b in pi_rank)
        v["swap_spearman"] = 1 - 6 * d2 / (n * (n * n - 1))
        v["swap_displaced"] = sorted(((b, pos_pi[b] + 1, pos_sw[b] + 1) for b in pi_rank
                                      if abs(pos_pi[b] - pos_sw[b]) > 1), key=lambda x: x[1])
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
    w("# RESEARCH — Facets d20 simulation: encounter tables and the balance band")
    w("")
    w(f"*Engine builder, generated by `software/tools/d20_sim.py all{' --quick' if args.quick else ''}` "
      f"on {time.strftime('%Y-%m-%d')}. Rules: `software/facets_d20/` (every roll through "
      "`combat.py`). Data: `facets_d20/data/*.yaml` v0.2, SRD ladder "
      "`software/facets_d20/data/srd_monsters.yaml`, SRD baselines "
      "`software/facets_d20/data/srd_baselines.yaml`. Base seed "
      f"{BASE_SEED}; each cell's seed is `crc32(repr((base, task key)))`, so any cell reruns "
      "alone. Raw numbers: `software/research/facets_d20_sim_results.json`. Method and "
      "decisions: `docs/DESIGN_facets_d20_engine.md`.*")
    w("")
    w("## Headline")
    w("")
    ev4 = results["evals"]["4:clash"]
    day = {r["level"]: r for r in results["day"]}
    bv = results.get("band")
    w(f"- **Clash at 4th level** (budget {results['fits']['ref4'][4]['clash'] / 4:.0f} Threat per "
      f"character): {fmt(ev4['rounds'], 2)} ± {fmt(ev4['ci_rounds'], 2)} rounds, "
      f"{100 * ev4['hp_lost']:.0f}% party HP lost, {100 * ev4['win']:.1f}% wins, a PC drops in "
      f"{100 * ev4['p_drop']:.0f}% of fights, a PC dies in {100 * ev4['p_death']:.1f}%.")
    w(f"- **Threat model** (measured): a boss = {model['boss']:.2f} standards of its CR; a "
      f"minion carries √({model['minion_hp']:.1f} × its damage per turn); a foe that never breaks "
      f"× {model['never']:.2f}.")
    w(f"- **A day of four Clashes** (two short rests) at 4th: the reference party survives it "
      f"{100 * day[4]['days_survived']:.0f}% of the time.")
    if bv:
        for L in sorted(bv):
            v = bv[L]
            out_band = [b for b, x in v["presets"].items() if not x["in_band"]]
            over = [b for b, x in v["sim_builds"].items() if not x["ok"]]
            w(f"- **Balance, level {L}:** {12 - len(out_band)}/12 presets inside ±15% of the "
              f"median PI" + (f" (out: {', '.join(out_band)})" if out_band else "")
              + f"; preset median vs SRD median {v['srd_pct']:+.0f}%; combos over the ceiling: "
              + (", ".join(over) if over else "none")
              + (f"; hybrids beating a pure build: "
                 + (", ".join(h for h, x in v.get("hybrids", {}).items() if not x["ok"]) or "none")
                 if v.get("hybrids") else "") + ".")
    w("")
    w("## 1. Method")
    w("")
    w("- **Fights.** `sim.Fight` runs the §6.1–6.2 rules: one d20 per side for initiative "
      "(Alert = advantage), bosses act at the top of the round and again in their side's half, "
      "boss resolve, fixed monster damage (crits rolled), minions, morale (standard foes at first "
      "Bloodied, minions when the leader falls), E1 one rider a turn, one reaction, concentration, "
      "death saves, Sparks as +1d6 after a roll. The tactical AI is documented in `sim.py`'s "
      "docstring and is the same for every build.")
    w("- **Resources.** A single fight gets ¼ of each long-rest pool (rounded up, plus any "
      "short-rest regain) and all short-rest pools — one of the day's four Clashes. The day "
      "runner carries HP, pools, Hit Dice and Sparks across four fights with short rests after "
      "the 1st and 3rd, pacing pools evenly.")
    w("- **Foes for fitting.** Continuous-CR generic foes: the SRD ladder's per-CR medians "
      "(AC, HP, to-hit, damage per turn, saves), log-interpolated. Three shapes averaged: "
      "four standards; a boss (60% of the Threat) + minions; two standards + minions.")
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
    w("**Table 9–2: Threat by CR** (SRD 5.2.1 ladder medians)")
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
    w("**Outcomes at the fitted budgets** (reference party; mean ± 95% CI; ✗ = misses a yaml target):")
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
      "tier (by party HP lost; ≥ 80% wanted, < 80% flagged ⚠):")
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
    w("| Level | Days survived (4 Clashes, 2 short rests) |")
    w("|---|---|")
    for L in LEVELS:
        w(f"| {L} | {100 * day[L]['days_survived']:.0f}% |")
    w("")
    if "pi" in results:
        write_balance(results, w)
    w("")
    w("## Findings for the Designer")
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
    w("## 8. Balance band (§8)")
    w("")
    w("Metrics per build and level, over 500 standard days (2,000 Clashes) beside three "
      "reference-party companions. **eDPR\\*** = (damage dealt + healing restored to allies + "
      "enemy damage prevented for allies, incl. disabled enemy turns) ÷ rounds. **eHP** = (HP + "
      "temp HP per fight + self-healing per fight) × (0.55 ÷ measured hit rate against it) × "
      "(printed damage per hit ÷ damage actually taken per hit). **PI** = eDPR\\* × eHP. "
      "DPR₁/DPR₃ = damage per round against one / three dummies (AC of the level's foes, 4 rounds).")
    w("")
    for L in sorted(bv, key=int):
        v = bv[L]
        rows = sorted([r for r in results["pi"] if r["level"] == int(L)], key=lambda r: -r["pi"])
        dd = {r["build"]: r for r in results["dummy_dpr"] if r["level"] == int(L)}
        sw = {r["build"]: r for r in results["swap"] if r["level"] == int(L)}
        w(f"### Level {L}")
        w("")
        w("| Build | Kind | DPR₁ | DPR₃ | eDPR* | eHP | PI | vs median | Swap HP lost | Verdict |")
        w("|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            b = r["build"]
            k = kinds[b]
            pct = 100 * (r["pi"] / v["median_pi"] - 1)
            if k == "preset":
                x = v["presets"][b]
                verdict = ("in band" if x["in_band"] else "**out of band**") + \
                          ("" if x["role_ok"] else "; **role**")
            elif k == "sim_build":
                verdict = "ok" if v["sim_builds"][b]["ok"] else "**over ceiling**"
            else:
                verdict = "SRD"
            w(f"| {b} | {k} | {fmt(dd[b]['dpr_1'])} | {fmt(dd[b]['dpr_3'])} | {fmt(r['edpr'])} | "
              f"{fmt(r['ehp'], 0)} | {fmt(r['pi'], 0)} | {pct:+.0f}% | "
              f"{100 * sw[b]['hp_lost']:.1f}% | {verdict} |")
        w("")
        w("Facet means vs the preset median: " + ", ".join(
            f"{f} {x['pi_pct']:+.0f}%{'' if x['in_band'] else ' **(out)**'}" for f, x in v["facets"].items())
          + f". Preset median vs SRD median: {v['srd_pct']:+.0f}% "
          + ("(inside ±15%)." if v["srd_ok"] else "(**outside ±15%**)."))
        if v.get("hybrids"):
            w("")
            w("Hybrids (item 7, from 4th level): PI vs the Facet's best pure build (+15% allowed); "
              "if Steel is main, DPR₁ vs the Facet's best pure martial (+5%); DPR₃ vs the best "
              "pure caster of its tradition (+5%).")
            w("")
            w("| Hybrid | PI vs best pure | DPR₁ vs pure martial | DPR₃ vs tradition's caster | Verdict |")
            w("|---|---|---|---|---|")
            for h, x in v["hybrids"].items():
                def pc_(y):
                    return "—" if y is None else f"{y:+.0f}%"
                w(f"| {h} ({x['main'] or '—'} main) | {pc_(x['pi_vs_best_pure_pct'])} | "
                  f"{pc_(x['dpr1_vs_martial_pct'])} | "
                  f"{pc_(x['dpr3_vs_caster_pct'])} ({x['tradition_caster'] or '—'}) | "
                  f"{'ok' if x['ok'] else '**beats a pure build**'} |")
            w("")
        w(f"Swap test vs PI rank: Spearman {v['swap_spearman']:.2f}; displaced by more than one "
          "place: " + (", ".join(f"{b} (PI #{a}, swap #{c})" for b, a, c in v["swap_displaced"])
                       or "none") + ".")
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
                    "never_breaks": f"x {model['never']:.2f}"},
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


def cmd_all(a):
    results = {"base_seed": BASE_SEED, "quick": a.quick}
    model = cmd_encounters(a, results)
    adjustments(results)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(results, indent=1, default=str))
    if not a.skip_balance:
        cmd_balance(a, results, model)
        results["band"] = band_verdicts(results)
    results["findings"] = results.get("findings", [])
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
