"""Importing this package registers every op in :data:`mapgen.registry.REGISTRY`."""
from ..registry import REGISTRY  # noqa: F401

from . import geometry, masks, fields, paint, materials, semantic, props, overlay, terrain, city  # noqa: F401,E402
