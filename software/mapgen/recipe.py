"""Recipe models, YAML loading, style includes and macro expansion (T2, T6)."""
from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

PACKAGE_DIR = Path(__file__).resolve().parent
MAX_MACRO_DEPTH = 12


class RecipeError(Exception):
    """A recipe is malformed or cannot run. The message names the step and field."""


class MapHeader(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = "Untitled map"
    width_ft: float = Field(gt=0, le=5000)
    height_ft: float = Field(gt=0, le=5000)
    unit: Literal["ft", "mi"] = "ft"
    feet_per_square: float = Field(5, gt=0)   # grid size in `unit` (name kept for battle maps)
    px_per_square: int = Field(70, ge=10, le=300)
    supersample: int = Field(2, ge=1, le=4)
    seed: int = 0
    include: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _battle_grid(self):
        if self.unit == "ft" and self.feet_per_square not in (5, 10, 25, 50, 100):
            raise ValueError("feet_per_square must be 5 or 10 for a battle map, or 25/50/100 for a town map "
                             "(unit: ft); use unit: mi for region maps")
        return self


class Step(BaseModel):
    model_config = ConfigDict(extra="allow")

    op: str
    out: str | None = None
    id: str | None = None
    seed_offset: int = 0

    def params(self) -> dict[str, Any]:
        return dict(self.model_extra or {})


class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")

    palette: dict[str, Any] = Field(default_factory=dict)
    materials: dict[str, dict[str, Any]] = Field(default_factory=dict)
    defaults: dict[str, dict[str, Any]] = Field(default_factory=dict)
    macros: dict[str, dict[str, Any]] = Field(default_factory=dict)
    ink: dict[str, float] = Field(default_factory=dict)


class Recipe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    map: MapHeader
    steps: list[Step] = Field(default_factory=list)
    measure: dict[str, dict[str, float]] = Field(default_factory=dict)
    style: Style = Field(default_factory=Style)
    source: str | None = None


def _fmt_validation(e: ValidationError, prefix: str = "") -> str:
    parts = []
    for err in e.errors():
        loc = ".".join(str(x) for x in err["loc"])
        parts.append(f"{prefix}{loc}: {err['msg']}")
    return "; ".join(parts)


def parse_recipe(data: Any, style: Style | None = None, source: str | None = None) -> Recipe:
    """Validate a recipe dict. Macros and defaults from ``style`` are applied."""
    if not isinstance(data, dict):
        raise RecipeError("a recipe must be a mapping with 'map' and 'steps'")
    if "map" not in data:
        raise RecipeError("recipe has no 'map' header")
    data = dict(data)
    style = style or Style()
    raw_steps = data.get("steps") or []
    if not isinstance(raw_steps, list):
        raise RecipeError("'steps' must be a list")
    for i, s in enumerate(raw_steps, 1):
        if not isinstance(s, dict) or "op" not in s:
            raise RecipeError(f"step {i}: every step needs an 'op'")
    data["steps"] = _expand(raw_steps, style)
    try:
        r = Recipe(**data, style=style, source=source)
    except ValidationError as e:
        raise RecipeError(_fmt_validation(e)) from None
    return r


# ---------- includes ----------

def _resolve_include(name: str, base: Path) -> Path:
    for cand in (base / name, PACKAGE_DIR / name):
        if cand.is_file():
            return cand
    raise RecipeError(f"include not found: {name} (looked beside the recipe and in mapgen/)")


def _merge_style(into: dict, new: dict) -> dict:
    for key, val in new.items():
        if key == "include":
            continue
        if isinstance(val, dict) and isinstance(into.get(key), dict):
            for k, v in val.items():
                if isinstance(v, dict) and isinstance(into[key].get(k), dict) and key == "defaults":
                    into[key][k] = {**into[key][k], **v}
                else:
                    into[key][k] = v
        else:
            into[key] = copy.deepcopy(val)
    return into


def _load_style(includes: list[str], base: Path, seen: tuple = ()) -> dict:
    merged: dict = {}
    for name in includes:
        path = _resolve_include(name, base)
        if path in seen:
            raise RecipeError(f"include recursion: {path.name}")
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as e:
            raise RecipeError(f"YAML error in include {name}: {e}") from None
        if data.get("include"):
            merged = _merge_style(merged, _load_style(data["include"], path.parent, seen + (path,)))
        merged = _merge_style(merged, data)
    return merged


def load_recipe(path: str | Path) -> Recipe:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise RecipeError(f"YAML error in {path.name}: {e}") from None
    except OSError as e:
        raise RecipeError(f"cannot read recipe {path}: {e}") from None
    if not isinstance(data, dict):
        raise RecipeError(f"{path.name}: a recipe must be a mapping")
    includes = (data.get("map") or {}).get("include") or []
    try:
        style = Style(**_load_style(includes, path.parent))
    except ValidationError as e:
        raise RecipeError(_fmt_validation(e, "style.")) from None
    return parse_recipe(data, style=style, source=str(path))


# ---------- macros and defaults ----------

_VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _subst(value: Any, env: dict, macro: str) -> Any:
    if isinstance(value, str):
        m = _VAR.fullmatch(value)
        if m:
            if m.group(1) not in env:
                raise RecipeError(f"macro '{macro}': unknown parameter ${{{m.group(1)}}}")
            return copy.deepcopy(env[m.group(1)])

        def rep(mm):
            if mm.group(1) not in env:
                raise RecipeError(f"macro '{macro}': unknown parameter ${{{mm.group(1)}}}")
            return str(env[mm.group(1)])
        return _VAR.sub(rep, value)
    if isinstance(value, list):
        return [_subst(v, env, macro) for v in value]
    if isinstance(value, dict):
        return {k: _subst(v, env, macro) for k, v in value.items()}
    return value


def _expand(steps: list[dict], style: Style, depth: int = 0, parent: str | None = None) -> list[dict]:
    if depth > MAX_MACRO_DEPTH:
        raise RecipeError("macro recursion is too deep (a macro calls itself?)")
    out: list[dict] = []
    for i, step in enumerate(steps):
        step = dict(step)
        if parent is not None:
            step["id"] = f"{parent}/{i}" if "id" not in step else f"{parent}/{step['id']}"
        op = step["op"]
        if op in style.macros:
            macro = style.macros[op]
            env = dict(macro.get("params") or {})
            call_id = step.pop("id", None)
            step.pop("op")
            env.update(step)
            body = _subst(copy.deepcopy(macro.get("steps") or []), env, op)
            cid = call_id if call_id is not None else (f"{parent}/{i}" if parent else f"{op}@{len(out)}")
            out.extend(_expand(body, style, depth + 1, parent=cid))
        else:
            defaults = style.defaults.get(op) or {}
            out.append({**copy.deepcopy(defaults), **step})
    return out
