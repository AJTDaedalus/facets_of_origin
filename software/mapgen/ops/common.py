"""Shared param types and helpers for ops."""
from __future__ import annotations

from typing import Annotated, Literal

import numpy as np
import shapely
from pydantic import Field
from scipy import ndimage
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon

Point = Annotated[list[float], Field(min_length=2, max_length=2)]
Ref = str
PosFt = Annotated[float, Field(gt=0)]
NonNegFt = Annotated[float, Field(ge=0)]
Unit = Annotated[float, Field(ge=0, le=1)]
Side = Literal["outside", "inside", "both"]


def polygonal(g):
    """Keep only polygonal parts, repaired."""
    if g.is_empty:
        return Polygon()
    if not g.is_valid:
        g = shapely.make_valid(g)
    if isinstance(g, (Polygon, MultiPolygon)):
        return g
    if isinstance(g, GeometryCollection) or hasattr(g, "geoms"):
        parts = [p for p in getattr(g, "geoms", []) if isinstance(p, (Polygon, MultiPolygon))]
        return shapely.unary_union(parts) if parts else Polygon()
    return Polygon()


def signed_distance(data: np.ndarray) -> np.ndarray:
    """Signed distance in pixels to the 0.5 contour; positive outside."""
    inside = data >= 0.5
    if not inside.any():
        return np.full(data.shape, 1e6, np.float32)
    if inside.all():
        return np.full(data.shape, -1e6, np.float32)
    d_out = ndimage.distance_transform_edt(~inside)
    d_in = ndimage.distance_transform_edt(inside)
    return np.where(inside, -(d_in - 0.5), d_out - 0.5).astype(np.float32)


def soft_step(sd_px: np.ndarray, edge_px: float = 0.0) -> np.ndarray:
    """Antialiased coverage of the region sd < edge."""
    return np.clip(0.5 - (sd_px - edge_px), 0, 1).astype(np.float32)
