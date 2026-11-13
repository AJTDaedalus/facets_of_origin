"""Typed layers and the layer store (T4)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class Geometry:
    """A shapely geometry in feet."""
    geom: Any


@dataclass
class Mask:
    """Coverage in 0..1, float32, shape (h, w)."""
    data: np.ndarray


@dataclass
class Field:
    """Unbounded scalar field, float32, shape (h, w)."""
    data: np.ndarray


@dataclass
class Image:
    """Premultiplied RGBA in 0..1, float32, shape (h, w, 4)."""
    data: np.ndarray


LAYER_TYPES = (Geometry, Mask, Field, Image)


class LayerStore:
    def __init__(self):
        self._layers: dict[str, Any] = {}

    def put(self, name: str, layer) -> None:
        if not isinstance(layer, LAYER_TYPES):
            raise TypeError(f"layer {name!r} is not a mapgen layer: {type(layer).__name__}")
        self._layers[name] = layer

    def get(self, ref: str):
        if ref.startswith("~"):
            base = self._layers[ref[1:]]
            if not isinstance(base, Mask):
                raise TypeError(f"only masks can be inverted: {ref}")
            return Mask(1.0 - base.data)
        return self._layers[ref]

    def free(self, name: str) -> None:
        self._layers.pop(name, None)

    def __contains__(self, name: str) -> bool:
        return name in self._layers

    def names(self) -> list[str]:
        return list(self._layers)
