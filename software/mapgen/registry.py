"""Op registry (T4). Each op declares a param model, its layer inputs and output."""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict


class ParamModel(BaseModel):
    """Base for op parameters: unknown keys are errors."""
    model_config = ConfigDict(extra="forbid")


@dataclass
class OpSpec:
    name: str
    fn: Callable
    params: type[ParamModel]
    inputs: dict[str, Any] = field(default_factory=dict)   # param name -> layer type or tuple
    output: Any = None
    group: str = "misc"
    doc: str = ""


class OpRegistry:
    def __init__(self):
        self._ops: dict[str, OpSpec] = {}

    def op(self, name: str, params: type[ParamModel], inputs: dict | None = None,
           output: Any = None, group: str = "misc"):
        def deco(fn):
            if name in self._ops:
                raise ValueError(f"op already registered: {name}")
            doc = inspect.getdoc(fn) or ""
            self._ops[name] = OpSpec(name, fn, params, dict(inputs or {}), output, group,
                                     doc.strip())
            return fn
        return deco

    def get(self, name: str) -> OpSpec:
        if name not in self._ops:
            raise KeyError(name)
        return self._ops[name]

    def __contains__(self, name: str) -> bool:
        return name in self._ops

    def list(self) -> list[OpSpec]:
        return sorted(self._ops.values(), key=lambda s: (s.group, s.name))


REGISTRY = OpRegistry()
op = REGISTRY.op
