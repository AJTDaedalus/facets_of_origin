"""Detail round (owner, 2026-11-13: "more detail ... shading lines"): prop shading and wall texture."""
from pathlib import Path

import numpy as np
import pytest
import yaml

from mapgen.ops.props import shade_crescent
from shapely.geometry import box
from tests.mapgen.helpers import run

H = dict(width_ft=40, height_ft=30, px_per_square=40, supersample=1)     # 8 px/ft
STYLE = yaml.safe_load((Path(__file__).resolve().parents[2] / "mapgen" / "styles" / "inked_parchment.yaml").read_text())


def canvas(steps, styled=False, **h):
    store, _ = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}] + steps,
                   style=STYLE if styled else None, **dict(H, **h))
    return store.get("canvas").data


def dark(c, thr=0.45):
    return c[..., :3].mean(-1) < thr


class TestPropShading:
    @pytest.mark.parametrize("rotate", [0, 180])
    def test_crate_shaded_south_east_even_rotated(self, rotate):
        c = dark(canvas([{"op": "prop", "kind": "crate", "at": [20, 15], "size": 6, "rotate": rotate, "shadow": 0, "id": "p"}]))
        # crate spans x 17..23, y 12..18 ft -> px 136..184, 96..144; compare SE and NW quarters
        se, nw = c[122:144, 162:184].sum(), c[96:118, 136:158].sum()
        assert se > nw

    def test_crescent_helper(self):
        h = shade_crescent(box(0, 0, 4, 4))
        k = 4 * 0.2                                   # the crescent: the south and east strips, k wide
        mids = [l.interpolate(0.5, normalized=True) for l in h.geoms]
        assert h is not None and len(mids) > 4
        assert all(m.x >= 4 - k - 1e-6 or m.y >= 4 - k - 1e-6 for m in mids)
        assert shade_crescent(box(0, 0, 0, 0)) is None

    def test_markers_and_flat_props_are_not_hatched(self):
        from mapgen.ops.props import MARKERS, NO_AUTO_SHADE
        assert {"rug", "banner"} <= NO_AUTO_SHADE and "city" in MARKERS
        # markers draw nothing beyond their own symbol: identical with or without a size jitter seed
        a = canvas([{"op": "prop", "kind": "city", "at": [20, 15], "size": 2, "id": "m1"}])
        b = canvas([{"op": "prop", "kind": "city", "at": [20, 15], "size": 2, "id": "m2"}])
        assert np.array_equal(a, b)

    @pytest.mark.parametrize("kind", ["barrel", "bed", "chest", "boulder", "pillar"])
    def test_detail_lines_present(self, kind):
        c = dark(canvas([{"op": "prop", "kind": kind, "at": [20, 15], "size": 6, "shadow": 0, "id": "p"}]))
        assert c.sum() > 200


class TestWallTexture:
    def test_cave_walls_get_rock_texture(self):
        steps = [{"op": "polygon", "out": "cave", "points": [[6, 6], [34, 6], [34, 24], [6, 24]]}]
        bare = canvas(steps + [{"op": "wall", "src": "cave", "name": "rock", "style": "rough", "thickness": 1.5,
                                "material": "cave_rock", "id": "w"}], styled=True)
        rich = canvas(steps + [{"op": "cave_walls", "src": "cave", "wall": "rock", "thickness": 1.5}], styled=True)
        band = (slice(30, 48), slice(60, 260))       # the north wall band
        assert dark(rich[band], 0.35).sum() > dark(bare[band], 0.35).sum()

    def test_stone_room_walls_get_weathering(self):
        steps = [{"op": "rect", "out": "room", "x": 8, "y": 8, "w": 24, "h": 14}]
        c = canvas(steps + [{"op": "stone_room", "src": "room", "wall": "w"}], styled=True)
        assert dark(c[52:64, 80:240], 0.3).sum() > 50

    def test_heavier_ink_weights(self):
        assert STYLE["ink"]["bold"] >= 0.75 and STYLE["ink"]["fine"] >= 0.12
