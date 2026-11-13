"""CLI: python -m mapgen render|ops|quality|sheet (T1, T25)."""
from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mapgen", description="Recipe-driven map building.")
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("render", help="render a recipe to PNG + dd2vtt + meta.json")
    r.add_argument("recipe")
    r.add_argument("--out", help="output directory (default: beside the recipe, in mapgen/)")
    r.add_argument("--draft", action="store_true", help="fast preview: 35 px/square, no supersampling")
    r.add_argument("--only-png", action="store_true")
    o = sub.add_parser("ops", help="list the available ops")
    o.add_argument("--markdown", action="store_true")
    q = sub.add_parser("quality", help="image metrics against comparator bands")
    q.add_argument("png", nargs="?")
    q.add_argument("--baseline", action="store_true", help="recompute comparator bands (needs MAPGEN_REF_DIR)")
    q.add_argument("--research", default=None, help="with --baseline: also write this RESEARCH markdown")
    q.add_argument("--category", required=False)
    q.add_argument("--px-per-square", type=float, default=None)
    q.add_argument("--recipe", default=None, help="recipe of the PNG (gives scale and grid mask)")
    s = sub.add_parser("sheet", help="side-by-side contact sheet with a comparator")
    s.add_argument("png")
    s.add_argument("--vs", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--px-per-square", type=float, default=None)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 2
    from . import cli_impl
    return getattr(cli_impl, f"cmd_{args.cmd}")(args)


if __name__ == "__main__":
    sys.exit(main())
