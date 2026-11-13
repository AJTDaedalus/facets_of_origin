"""Fixtures for the mapgen tests (docs/DESIGN_mapgen.md)."""
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def tmp_out(tmp_path) -> Path:
    out = tmp_path / "out"
    out.mkdir()
    return out


@pytest.fixture
def write_recipe(tmp_path):
    """Write a recipe dict (or YAML text) to disk and return its path."""
    def _write(data, name="test.map.yaml", folder=None):
        folder = Path(folder) if folder else tmp_path
        folder.mkdir(parents=True, exist_ok=True)
        p = folder / name
        p.write_text(data if isinstance(data, str) else yaml.safe_dump(data, sort_keys=False))
        return p
    return _write


def header(**kw):
    h = {"title": "T", "width_ft": 20, "height_ft": 10, "feet_per_square": 5,
         "px_per_square": 20, "supersample": 1, "seed": 1}
    h.update(kw)
    return h
