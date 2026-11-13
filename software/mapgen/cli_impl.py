"""Subcommand implementations (kept apart so --help stays fast)."""
from __future__ import annotations


def cmd_render(args) -> int:
    raise NotImplementedError


def cmd_ops(args) -> int:
    raise NotImplementedError


def cmd_quality(args) -> int:
    raise NotImplementedError


def cmd_sheet(args) -> int:
    raise NotImplementedError
