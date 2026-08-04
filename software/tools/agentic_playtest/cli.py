"""Command line for the agentic playtest harness.

    python -m tools.agentic_playtest.cli pilot --arm A --seed 1
    python -m tools.agentic_playtest.cli batch --sessions-per-arm 8
    python -m tools.agentic_playtest.cli analyse playtest/08_npc_variance/runs

`pilot` is the gate: run one instrumented session, read the transcript, and check
the measured cost before committing to a batch.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = SOFTWARE_DIR.parent
DEFAULT_OUT = REPO_ROOT / "playtest" / "08_npc_variance" / "runs"
MM_PASSWORD = "agentic-playtest-harness"

# Importable from anywhere, not only from `software/`.
if str(SOFTWARE_DIR) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_DIR))


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class AppServer:
    """The application under test, on its own port and data directory."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.port = _free_port()
        self.data_dir = data_dir or (SOFTWARE_DIR / "data" / "agentic_playtest")
        self.proc: subprocess.Popen | None = None

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def __enter__(self) -> "AppServer":
        self.data_dir.mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "DATA_DIR": str(self.data_dir),
               "PORT": str(self.port), "HOST": "127.0.0.1"}
        self.proc = subprocess.Popen(
            [sys.executable, "run.py"], cwd=SOFTWARE_DIR, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(150):
            if self.proc.poll() is not None:
                raise RuntimeError("server exited during startup")
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.2):
                    return self
            except OSError:
                time.sleep(0.1)
        raise RuntimeError("server did not start")

    def __exit__(self, *exc) -> None:
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def _client():
    """Fail before starting a server, not after."""
    try:
        import anthropic
    except ImportError:
        sys.exit("The anthropic SDK is not installed. `pip install anthropic`")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. The harness runs entirely on the "
                 "API; there is nothing to run without it.")
    return anthropic.Anthropic()


def run_one(client, base_url: str, mm_token: str, scenario_key: str, arm: str,
            seed: int, out_dir: Path, max_beats: int) -> dict:
    """One session, written to disk. Returns its summary."""
    from tools.agentic_playtest.debrief import collect, to_dict
    from tools.agentic_playtest.metrics import compute, summarise
    from tools.agentic_playtest.run import Budget, build_session
    from tools.agentic_playtest.scenarios import CAST_BLURB, PARTY, SCENARIOS

    scenario = SCENARIOS[scenario_key]
    session = build_session(
        client=client, base_url=base_url, mm_token=mm_token,
        scenario=scenario.briefing, prep=scenario.prep, cast_blurb=CAST_BLURB,
        party=PARTY, enemies=scenario.enemies, seed=seed, arm=arm,
        session_name=f"{scenario_key}-{arm}-{seed}",
        budget=Budget(max_beats=max_beats),
    )

    name = f"{scenario_key}_arm{arm}_seed{seed}"
    print(f"  playing {name} ...", flush=True)
    result = session.play()

    metrics = compute(session.table.log,
                      [p["player_name"] for p in PARTY])
    debriefs = {}
    for player in session.players:
        try:
            debriefs[player.name] = to_dict(collect(client, player))
        except Exception as e:
            debriefs[player.name] = {"error": str(e)}

    out_dir.mkdir(parents=True, exist_ok=True)
    result.write(out_dir, name)
    session.table.log.write(out_dir / f"{name}.events.jsonl")
    (out_dir / f"{name}.metrics.json").write_text(
        json.dumps(metrics.to_dict(), indent=2), encoding="utf-8")
    (out_dir / f"{name}.debriefs.json").write_text(
        json.dumps(debriefs, indent=2), encoding="utf-8")

    session.table.close()

    output_tokens = sum(u.output_tokens for u in result.usage.values())
    cache_read = sum(u.cache_read for u in result.usage.values())
    print(summarise(metrics))
    print(f"  validation: {'ok' if result.validation_ok else 'FAILED'}"
          f" · output tokens {output_tokens:,} · cache reads {cache_read:,}")
    if not result.validation_ok:
        print("  " + result.validation_report.replace("\n", "\n  "))

    return {"name": name, "arm": arm, "scenario": scenario_key, "seed": seed,
            "beats": result.beats, "validation_ok": result.validation_ok,
            "stopped_because": result.stopped_because,
            "output_tokens": output_tokens, "cache_read": cache_read,
            "rules_gaps": result.rules_gaps}


def cmd_rehearse(args) -> int:
    """The free gate before the paid one.

    Runs the real scenario, the real party, and the real server with a scripted
    stand-in for the model. Anything that would break the pilot on wiring rather
    than on judgement breaks here first, at no cost.
    """
    from tools.agentic_playtest.client import login_mm
    from tools.agentic_playtest.rehearsal import ScriptedClient, rehearsal_script
    from tools.agentic_playtest.run import Budget, build_session
    from tools.agentic_playtest.scenarios import CAST_BLURB, PARTY, SCENARIOS

    scenario = SCENARIOS[args.scenario]
    script = rehearsal_script(scenario.enemies[0]["id"], PARTY[0]["player_name"])

    with AppServer() as server:
        token = login_mm(server.base_url, MM_PASSWORD)
        session = build_session(
            client=ScriptedClient(script), base_url=server.base_url,
            mm_token=token, scenario=scenario.briefing, prep=scenario.prep,
            cast_blurb=CAST_BLURB, party=PARTY, enemies=scenario.enemies,
            seed=args.seed, arm=args.arm, session_name=f"rehearsal-{args.scenario}",
            budget=Budget(max_beats=2),
        )
        result = session.play()
        session.table.close()

    print(result.transcript)
    print(f"\nRehearsal ran {result.beats} beats against the real engine.")
    print(f"validation: {'ok' if result.validation_ok else 'FAILED'}")
    if not result.validation_ok:
        print(result.validation_report)
    print("\nWiring is sound. `pilot` is the next gate, and it costs money.")
    return 0 if result.validation_ok else 1


def cmd_pilot(args) -> int:
    """One instrumented session. The gate before spending a batch."""
    from tools.agentic_playtest.client import login_mm

    client = _client()
    with AppServer() as server:
        token = login_mm(server.base_url, MM_PASSWORD)
        started = time.monotonic()
        summary = run_one(client, server.base_url, token, args.scenario, args.arm,
                          args.seed, Path(args.out), args.max_beats)
        elapsed = time.monotonic() - started

    print()
    print(f"Pilot complete in {elapsed / 60:.1f} min.")
    print(f"Output tokens: {summary['output_tokens']:,} "
          f"(~${summary['output_tokens'] * 25 / 1_000_000:.2f} at Opus-5 output rates,"
          f" input extra)")
    print(f"Transcript: {Path(args.out) / (summary['name'] + '.md')}")
    print()
    print("Read the transcript before running a batch. Check: does it read like a "
          "table? Is there out-of-character talk? Did anyone refuse a hook?")
    return 0 if summary["validation_ok"] else 1


def cmd_batch(args) -> int:
    """Paired runs: each (scenario, seed) played once in each arm."""
    from tools.agentic_playtest.client import login_mm

    client = _client()
    out = Path(args.out)
    summaries = []

    with AppServer() as server:
        token = login_mm(server.base_url, MM_PASSWORD)
        for i in range(args.sessions_per_arm):
            scenario = ("guardian_chamber", "aldermans_office")[i % 2]
            seed = args.seed_base + i
            for arm in ("A", "B"):
                try:
                    summaries.append(run_one(client, server.base_url, token,
                                             scenario, arm, seed, out,
                                             args.max_beats))
                except Exception as e:
                    print(f"  session failed: {e}")
                    summaries.append({"name": f"{scenario}_arm{arm}_seed{seed}",
                                      "arm": arm, "error": str(e)})

    (out / "batch_summary.json").write_text(json.dumps(summaries, indent=2),
                                            encoding="utf-8")
    print(f"\n{len(summaries)} sessions written to {out}")
    return 0


def cmd_analyse(args) -> int:
    """Batch dice check, then blind pairwise judgement of the arms."""
    from tools.agentic_playtest.events import EventLog
    from tools.agentic_playtest.judge import compare, tally
    from tools.agentic_playtest.validate import dice_distribution

    out = Path(args.runs)
    logs = [EventLog.read(p) for p in sorted(out.glob("*.events.jsonl"))]
    if not logs:
        sys.exit(f"No event logs in {out}")

    dice = dice_distribution(logs)
    print("Dice distribution across the batch:")
    print(f"  {dice}")
    if not dice.passed:
        print("  ^ FAILED. Do not report any number from this batch.")

    transcripts = {p.stem: p.read_text(encoding="utf-8")
                   for p in sorted(out.glob("*.md"))}
    pairs = []
    for name in transcripts:
        if "_armA_" not in name:
            continue
        partner = name.replace("_armA_", "_armB_")
        if partner in transcripts:
            pairs.append((name, partner))

    if not pairs:
        print("\nNo A/B pairs found — nothing to judge.")
        return 0

    client = _client()
    verdicts = []
    print(f"\nJudging {len(pairs)} pairs blind, both orderings each ...")
    for a_name, b_name in pairs:
        verdict = compare(client, transcripts[a_name], transcripts[b_name], "A", "B")
        verdicts.append(verdict)
        print(f"  {a_name} vs {b_name}: "
              f"{verdict.winner or 'order-dependent (no signal)'}")

    result = tally(verdicts)
    (out / "judgement.json").write_text(json.dumps(
        {"tally": result, "verdicts": [v.to_dict() for v in verdicts],
         "dice": {"n": dice.n, "chi_square": dice.chi_square,
                  "passed": dice.passed}},
        indent=2), encoding="utf-8")

    print(f"\nAgreed preferences: {result['agreed']}")
    print(f"Order-dependent (discarded): {result['order_dependent']} of "
          f"{result['pairs']}")
    print("\nThis is signal-finding, not significance. Report differences as "
          "observations to check with human playtesters.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentic_playtest",
                                     description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("pilot", help="one instrumented session (the cost gate)")
    p.add_argument("--arm", choices=["A", "B"], default="A")
    p.add_argument("--scenario", default="guardian_chamber")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--max-beats", type=int, default=12)
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.set_defaults(func=cmd_pilot)

    b = sub.add_parser("batch", help="paired A/B runs")
    b.add_argument("--sessions-per-arm", type=int, default=8)
    b.add_argument("--seed-base", type=int, default=100)
    b.add_argument("--max-beats", type=int, default=25)
    b.add_argument("--out", default=str(DEFAULT_OUT))
    b.set_defaults(func=cmd_batch)

    r = sub.add_parser("rehearse",
                       help="free wiring check — real server, scripted agents")
    r.add_argument("--scenario", default="guardian_chamber")
    r.add_argument("--arm", choices=["A", "B"], default="A")
    r.add_argument("--seed", type=int, default=1)
    r.set_defaults(func=cmd_rehearse)

    a = sub.add_parser("analyse", help="dice check and blind judgement")
    a.add_argument("runs", nargs="?", default=str(DEFAULT_OUT))
    a.set_defaults(func=cmd_analyse)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
