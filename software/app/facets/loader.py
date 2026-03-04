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


# FOF envelope keys that are not part of the FacetFile schema.
_FOF_ENVELOPE_KEYS = frozenset({
    "fof_version", "type", "requires", "incompatible_with",
    "scope", "merge_hints", "changelog",
})


def _normalize_fof(raw: dict) -> dict:
    """Normalize a .fof raw dict into the shape FacetFile.model_validate() expects.

    Does not mutate the input. Returns a new dict.

    Transformations:
    - Strips FOF envelope keys not present in FacetFile schema.
    - Renames ``character_facets`` → ``facets``.
    - Moves top-level ``attribute_distribution`` into ``attributes.distribution``.
    """
    result = {k: v for k, v in raw.items() if k not in _FOF_ENVELOPE_KEYS}

    # character_facets → facets
    if "character_facets" in result:
        result["facets"] = result.pop("character_facets")

    # top-level attribute_distribution → attributes.distribution
    if "attribute_distribution" in result:
        dist = result.pop("attribute_distribution")
        attrs = result.setdefault("attributes", {})
        if isinstance(attrs, dict):
            attrs["distribution"] = dist

    return result


def load_facet_file(path: Path) -> FacetFile:
    """Load and validate a single Facet YAML or .fof file.

    Args:
        path: Absolute or relative path to a facet.yaml or .fof file.

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

    if path.suffix == ".fof":
        raw = _normalize_fof(raw)

    try:
        return FacetFile.model_validate(raw)
    except ValidationError as e:
        lines = [f"{path.name}: Schema validation failed —"]
        for err in e.errors():
            loc = " → ".join(str(p) for p in err["loc"])
            lines.append(f"  [{loc}] {err['msg']}")
        raise FacetLoadError("\n".join(lines)) from e


def discover_facet_files(facets_dir: Path) -> list[Path]:
    """Return all ruleset files found under facets_dir, sorted by path.

    Searches recursively for ``facet.yaml`` and ``*.fof`` files. For .fof
    files, only those with ``type: ruleset`` (or no ``type`` key) are included.

    If a directory contains both a ``facet.yaml`` and a ``*.fof`` ruleset file,
    the .fof takes precedence and the facet.yaml is excluded.

    Args:
        facets_dir: Root directory to search.

    Returns:
        Sorted list of Path objects pointing to ruleset files.
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
        fof_type = raw.get("type")
        if fof_type == "ruleset" or fof_type is None:
            fof_paths.append(fof_path)

    # Directories that have at least one .fof ruleset — facet.yaml files there are superseded.
    fof_dirs = {p.parent for p in fof_paths}
    yaml_paths = {p for p in yaml_paths if p.parent not in fof_dirs}

    return sorted(yaml_paths | set(fof_paths))
