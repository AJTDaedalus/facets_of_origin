"""Load and validate Lean Facets v1.0 ruleset files from disk.

A ruleset file (`facet.yaml`, or a `.fof` with `type: ruleset`) is validated
against `FacetFile`. If it names a `tables_file`, that file is loaded beside it
and every table is checked for exact coverage of its die (INV-24). A missing
tables file is tolerated with a warning, so the engine keeps working while the
MM toolbox is being written; a present but malformed one fails loudly.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from app.facets.schema import FacetFile, TablesFile, table_coverage_errors


class FacetLoadError(Exception):
    """Raised when a Facet file cannot be loaded or fails validation.

    The message names the file and every problem, for display to the MM.
    """


# FOF envelope keys that are not part of the FacetFile schema.
_FOF_ENVELOPE_KEYS = frozenset({
    "fof_version", "type", "requires", "incompatible_with",
    "scope", "merge_hints", "changelog", "ruleset",
})


def _format_validation(name: str, e: ValidationError) -> str:
    lines = [f"{name}: Schema validation failed —"]
    for err in e.errors():
        loc = " → ".join(str(p) for p in err["loc"])
        lines.append(f"  [{loc}] {err['msg']}")
    return "\n".join(lines)


def _read_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise FacetLoadError(f"{path.name}: YAML parse error — {e}") from e
    except OSError as e:
        raise FacetLoadError(f"{path.name}: Cannot read file — {e}") from e


def load_tables_file(path: Path) -> TablesFile:
    """Load and validate a tables.yaml. Every table must cover its die exactly once.

    Raises:
        FacetLoadError: unreadable, not a mapping, schema failure, duplicate
            table ids, or any coverage gap/overlap.
    """
    raw = _read_yaml(path)
    if raw is None:
        return TablesFile()
    if not isinstance(raw, dict):
        raise FacetLoadError(f"{path.name}: tables file must be a YAML mapping.")
    try:
        tf = TablesFile.model_validate(raw)
    except ValidationError as e:
        raise FacetLoadError(_format_validation(path.name, e)) from e
    errors: list[str] = []
    seen: set[str] = set()
    for table in tf.tables:
        if table.id in seen:
            errors.append(f"duplicate table id {table.id!r}")
        seen.add(table.id)
        errors.extend(table_coverage_errors(table))
    if errors:
        raise FacetLoadError(f"{path.name}: table validation failed —\n"
                             + "\n".join(f"  {e}" for e in errors))
    return tf


def load_facet_file(path: Path) -> FacetFile:
    """Load and validate one ruleset file (and its tables file, if any).

    Raises:
        FacetLoadError: unreadable, not a mapping, or fails schema validation.
    """
    raw = _read_yaml(path)
    if not isinstance(raw, dict):
        raise FacetLoadError(
            f"{path.name}: Facet file must be a YAML mapping, got {type(raw).__name__}.")

    if path.suffix == ".fof":
        raw = {k: v for k, v in raw.items() if k not in _FOF_ENVELOPE_KEYS}

    try:
        ff = FacetFile.model_validate(raw)
    except ValidationError as e:
        raise FacetLoadError(_format_validation(path.name, e)) from e

    for table in ff.tables:
        errs = table_coverage_errors(table)
        if errs:
            raise FacetLoadError(f"{path.name}: " + "; ".join(errs))

    if ff.tables_file:
        tables_path = path.parent / ff.tables_file
        if tables_path.exists():
            ff.loaded_tables = load_tables_file(tables_path).tables
        else:
            ff.load_warnings.append(
                f"{path.name}: tables file {ff.tables_file!r} not found; "
                "the MM toolbox tables are unavailable.")
    return ff


def discover_facet_files(facets_dir: Path) -> list[Path]:
    """All ruleset files under facets_dir, sorted by path.

    Finds `facet.yaml` and `*.fof` files with `type: ruleset` (or no type). A
    `.fof` ruleset supersedes a `facet.yaml` in the same directory.
    """
    if not facets_dir.is_dir():
        return []

    yaml_paths: set[Path] = set(facets_dir.rglob("facet.yaml"))

    fof_paths: list[Path] = []
    for fof_path in facets_dir.rglob("*.fof"):
        try:
            raw = yaml.safe_load(fof_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(raw, dict):
            continue
        if raw.get("type") in ("ruleset", None):
            fof_paths.append(fof_path)

    fof_dirs = {p.parent for p in fof_paths}
    yaml_paths = {p for p in yaml_paths if p.parent not in fof_dirs}
    return sorted(yaml_paths | set(fof_paths))
