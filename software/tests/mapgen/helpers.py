"""Shared helpers for op tests: run one op through a real Engine."""
import numpy as np

from mapgen.engine import Engine
from mapgen.recipe import parse_recipe

from tests.mapgen.conftest import header


def run(steps, keep="canvas", draft=False, style=None, **h):
    from mapgen.recipe import Style
    r = parse_recipe({"map": header(**h), "steps": steps}, style=Style(**(style or {})))
    e = Engine(r, draft=draft)
    store = e.run(keep_all=True)
    return store, e


def layer(steps, name, **h):
    store, _ = run(steps, **h)
    return store.get(name)
