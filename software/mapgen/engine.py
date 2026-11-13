"""Runs a recipe: dry-pass validation, per-step seeding, liveness freeing (T5)."""
from __future__ import annotations

import zlib
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from pydantic import ValidationError

from .layers import Geometry, Image, LayerStore, Mask
from .recipe import Recipe, RecipeError, Step
from .registry import OpRegistry, OpSpec
from .units import Frame

KEEP = {"canvas"}


def step_seed(map_seed: int, key: str, offset: int) -> int:
    return zlib.crc32(f"{map_seed}|{key}|{offset}".encode()) & 0x7FFFFFFF


@dataclass
class Collector:
    """What ops emit besides pixels: VTT data, legend entries, named geometry."""
    los: list = field(default_factory=list)          # LineStrings in feet
    portals: list = field(default_factory=list)      # dicts in feet
    lights: list = field(default_factory=list)
    legend: dict = field(default_factory=dict)       # kind -> label
    geometry: dict = field(default_factory=dict)     # name -> shapely geom (feet)
    masks: dict = field(default_factory=dict)        # named masks kept for metrics (e.g. grid)


@dataclass
class Context:
    frame: Frame
    recipe: Recipe
    store: LayerStore
    collector: Collector
    index: int = 0
    step: Step | None = None
    seed: int = 0
    rng: np.random.Generator | None = None

    @property
    def style(self):
        return self.recipe.style


def _type_name(t) -> str:
    if isinstance(t, tuple):
        return " or ".join(x.__name__ for x in t)
    return t.__name__


def _accepts(expected, actual) -> bool:
    exp = expected if isinstance(expected, tuple) else (expected,)
    return actual in exp


class Engine:
    def __init__(self, recipe: Recipe, registry: OpRegistry | None = None, draft: bool = False):
        if registry is None:
            from .ops import REGISTRY as registry  # noqa: N811  (loads every op module)
        self.recipe = recipe
        self.registry = registry
        self.frame = Frame(recipe.map, draft=draft)
        self.collector = Collector()

    def _where(self, i: int, step: Step) -> str:
        sid = f" [{step.id}]" if step.id else ""
        return f"step {i} (op '{step.op}'){sid}"

    def plan(self) -> list[tuple[Step, OpSpec, Any, dict]]:
        """Dry pass: resolve ops, validate params and layer types. Runs nothing."""
        types: dict[str, Any] = {}
        planned = []
        for i, step in enumerate(self.recipe.steps, 1):
            where = self._where(i, step)
            if step.op not in self.registry:
                raise RecipeError(f"{where}: unknown op '{step.op}'")
            spec = self.registry.get(step.op)
            try:
                params = spec.params(**step.params())
            except ValidationError as e:
                msgs = "; ".join(f"{'.'.join(map(str, er['loc']))}: {er['msg']}" for er in e.errors())
                raise RecipeError(f"{where}: {msgs}") from None
            refs = {}
            for pname, expected in spec.inputs.items():
                ref = getattr(params, pname, None)
                if ref is None:
                    continue
                for r in (ref if isinstance(ref, list) else [ref]):
                    base = r[1:] if r.startswith("~") else r
                    if base not in types:
                        raise RecipeError(f"{where}: '{pname}' refers to '{base}', which no earlier step makes")
                    actual = types[base]
                    if r.startswith("~") and actual is not Mask:
                        raise RecipeError(f"{where}: only a Mask can be inverted with '~' ({r})")
                    if not _accepts(expected, actual):
                        raise RecipeError(f"{where}: '{pname}' needs a {_type_name(expected)}, "
                                          f"but '{base}' is a {actual.__name__}")
                refs[pname] = ref
            if spec.output is not None:
                if not step.out:
                    raise RecipeError(f"{where}: this op makes a layer; give it a name with 'out'")
                out_t = spec.output
                if out_t == "same":
                    first = next(iter(refs.values()), None)
                    if isinstance(first, list):
                        first = first[0]
                    out_t = types[first.lstrip("~")] if first else None
                types[step.out] = out_t
            planned.append((step, spec, params, refs))
        return planned

    def _last_use(self, planned) -> dict[str, int]:
        last: dict[str, int] = {}
        for i, (step, spec, params, refs) in enumerate(planned):
            for ref in refs.values():
                for r in (ref if isinstance(ref, list) else [ref]):
                    last[r.lstrip("~")] = i
            if step.out:
                last.setdefault(step.out, i)
                last[step.out] = max(last[step.out], i)
        return last

    def run(self, keep_all: bool = False) -> LayerStore:
        planned = self.plan()
        last = self._last_use(planned)
        store = LayerStore()
        ctx = Context(self.frame, self.recipe, store, self.collector)
        for i, (step, spec, params, refs) in enumerate(planned):
            key = step.id if step.id else f"#{i}"
            ctx.index, ctx.step = i, step
            ctx.seed = step_seed(self.recipe.map.seed, key, step.seed_offset)
            ctx.rng = np.random.default_rng(ctx.seed)
            inputs = {}
            for pname, ref in refs.items():
                inputs[pname] = [store.get(r) for r in ref] if isinstance(ref, list) else store.get(ref)
            try:
                result = spec.fn(ctx, params, **inputs)
            except RecipeError as e:
                raise RecipeError(f"{self._where(i + 1, step)}: {e}") from None
            if spec.output is not None:
                if result is None:
                    raise RecipeError(f"{self._where(i + 1, step)}: op returned no layer")
                store.put(step.out, result)
            if not keep_all:
                for name, idx in last.items():
                    if idx == i and name not in KEEP and name in store:
                        store.free(name)
        return store
