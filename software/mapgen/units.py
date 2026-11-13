"""Feet <-> pixel transform (T3). Origin is the north-west corner, y runs south."""
from __future__ import annotations

from .recipe import MapHeader

DRAFT_PX_PER_SQUARE = 35


class Frame:
    def __init__(self, header: MapHeader, draft: bool = False):
        self.header = header
        self.draft = draft
        self.pps = DRAFT_PX_PER_SQUARE if draft else header.px_per_square
        self.ss = 1 if draft else header.supersample
        self.fps = header.feet_per_square
        self.unit = header.unit
        out_w = round(header.width_ft / self.fps * self.pps)
        out_h = round(header.height_ft / self.fps * self.pps)
        if out_w < 1 or out_h < 1:
            from .recipe import RecipeError
            raise RecipeError(f"map renders to {out_w}×{out_h} px: make it bigger or raise px_per_square")
        self.out_size = (out_w, out_h)                 # (w, h) of the exported PNG
        self.shape = (out_h * self.ss, out_w * self.ss)  # (h, w) working arrays
        self.scale = self.pps * self.ss / self.fps      # working px per foot

    @property
    def width_ft(self) -> float:
        return self.header.width_ft

    @property
    def height_ft(self) -> float:
        return self.header.height_ft

    def px(self, feet: float) -> float:
        """Feet to working pixels."""
        return feet * self.scale

    def ft(self, px: float) -> float:
        """Working pixels to feet."""
        return px / self.scale

    @property
    def square_px(self) -> float:
        return self.pps * self.ss
