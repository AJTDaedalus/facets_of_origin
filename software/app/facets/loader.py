"""Load and validate Facet YAML files from disk.

Facet files define rulesets, skills, techniques, and game economy values.
Every file is validated against the FacetFile Pydantic schema on load.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from app.facets.schema import FacetFile


class FacetLoadError(Exception):
    """Raised when a Facet file cannot be loaded or fails schema validation.

    The exception message includes the file name and a human-readable
    description of every validation error, suitable for display to the MM.
    """


def load_facet_file(path: Path) -> FacetFile:
    """Load and validate a single Facet YAML file.

    Args:
        path: Absolute or relative path to a facet.yaml file.

    Returns:
        A validated FacetFile instance.

    Raises:
        FacetLoadError: If the file cannot be read, is not valid YAML,
            is not a YAML mapping, or fails Pydantic schema validation.
    """
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise FacetLoadError(f"{path.name}: YAML parse error — {e}") from e
    except OSError as e:
        raise FacetLoadError(f"{path.name}: Cannot read file — {e}") from e

    if not isinstance(raw, dict):
        raise FacetLoadError(f"{path.name}: Facet file must be a YAML mapping, got {type(raw).__name__}.")

    try:
        return FacetFile.model_validate(raw)
    except ValidationError as e:
        lines = [f"{path.name}: Schema validation failed —"]
        for err in e.errors():
            loc = " → ".join(str(p) for p in err["loc"])
            lines.append(f"  [{loc}] {err['msg']}")
        raise FacetLoadError("\n".join(lines)) from e


def discover_facet_files(facets_dir: Path) -> list[Path]:
    """Return all facet.yaml files found under facets_dir, sorted by path.

    Searches recursively. Non-existent directories return an empty list.

    Args:
        facets_dir: Root directory to search.

    Returns:
        Sorted list of Path objects pointing to facet.yaml files.
    """
    if not facets_dir.is_dir():
        return []
    return sorted(facets_dir.rglob("facet.yaml"))
