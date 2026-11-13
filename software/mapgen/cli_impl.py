"""Subcommand implementations (kept apart so --help stays fast)."""
from __future__ import annotations

import sys

from .recipe import RecipeError


def cmd_render(args) -> int:
    from .export import render_recipe
    try:
        r = render_recipe(args.recipe, out_dir=args.out, draft=args.draft, only_png=args.only_png)
    except RecipeError as e:
        print(f"mapgen: {e}", file=sys.stderr)
        return 2
    for k in ("png", "dd2vtt", "meta"):
        if k in r:
            print(f"{k}: {r[k]}")
    return 0


def cmd_ops(args) -> int:
    from .docs import ops_markdown
    from .ops import REGISTRY
    if args.markdown:
        sys.stdout.write(ops_markdown(REGISTRY))
        return 0
    for spec in REGISTRY.list():
        first = (spec.doc or "").split(". ")[0]
        print(f"{spec.name:<16} {first}")
    return 0


def cmd_quality(args) -> int:
    from .quality import cli_quality
    return cli_quality(args)


def cmd_sheet(args) -> int:
    from .quality import cli_sheet
    return cli_sheet(args)
