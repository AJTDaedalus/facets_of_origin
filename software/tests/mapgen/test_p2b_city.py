"""Phase 2b: town maps — larger squares, street frontage lots, gabled buildings."""
import numpy as np
import pytest
import shapely

from mapgen.recipe import RecipeError, parse_recipe
from tests.mapgen.conftest import header
from tests.mapgen.helpers import layer, run

TOWN = dict(width_ft=400, height_ft=300, feet_per_square=50, px_per_square=50, supersample=1)
ROAD = [{"op": "path", "out": "road", "points": [[0, 150], [400, 150]], "line": True}]


class TestTownScale:
    @pytest.mark.parametrize("fps", [25, 50, 100])
    def test_town_squares_allowed(self, fps):
        assert parse_recipe({"map": header(feet_per_square=fps), "steps": []}).map.feet_per_square == fps

    def test_odd_feet_still_rejected(self):
        with pytest.raises(RecipeError, match="feet_per_square"):
            parse_recipe({"map": header(feet_per_square=7), "steps": []})


class TestFrontage:
    def _lots(self, **kw):
        return layer(ROAD + [{"op": "frontage", "out": "lots", "roads": ["road"], "road_width": 20, "id": "f", **kw}],
                     "lots", **TOWN).geom

    def test_makes_buildings_both_sides(self):
        g = self._lots()
        parts = list(g.geoms)
        assert len(parts) > 10
        ys = [p.centroid.y for p in parts]
        assert min(ys) < 140 and max(ys) > 160

    def test_no_overlap_and_clear_of_road(self):
        parts = list(self._lots().geoms)
        road = shapely.geometry.LineString([(0, 150), (400, 150)]).buffer(10)
        assert all(not p.intersects(road) for p in parts)
        assert sum(p.area for p in parts) == pytest.approx(shapely.unary_union(parts).area, rel=1e-6)

    def test_deterministic(self):
        assert self._lots().equals(self._lots())

    def test_fill_controls_count(self):
        assert len(self._lots(fill=0.3).geoms) < len(self._lots(fill=1.0).geoms)

    def test_avoid_and_within(self):
        g = layer(ROAD + [{"op": "rect", "out": "plaza", "x": 150, "y": 100, "w": 100, "h": 100},
                          {"op": "rect", "out": "town", "x": 0, "y": 0, "w": 300, "h": 300},
                          {"op": "frontage", "out": "lots", "roads": ["road"], "road_width": 20,
                           "avoid": "plaza", "within": "town", "id": "f"}], "lots", **TOWN).geom
        plaza = shapely.geometry.box(150, 100, 250, 200)
        assert all(not p.intersects(plaza) and p.bounds[2] <= 300.01 for p in g.geoms)


class TestOrganic:
    def _lots(self, **kw):
        return layer(ROAD + [{"op": "frontage", "out": "lots", "roads": ["road"], "road_width": 20, "id": "f", **kw}],
                     "lots", **TOWN).geom

    def test_rotate_jitter_tilts_buildings(self):
        import math
        def angles(g):
            out = []
            for p in g.geoms:
                c = list(p.minimum_rotated_rectangle.exterior.coords)
                out.append(round(math.degrees(math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0])) % 90, 1))
            return set(out)
        assert len(angles(self._lots(rotate_jitter=12))) > len(angles(self._lots())) 

    def test_l_shape_adds_wings(self):
        assert len(self._lots(l_shape=1.0).geoms) > len(self._lots(l_shape=0.0).geoms) * 1.2

    def test_wings_clear_of_road(self):
        road = shapely.geometry.LineString([(0, 150), (400, 150)]).buffer(10)
        assert all(not p.intersects(road) for p in self._lots(l_shape=1.0, rotate_jitter=10).geoms)


class TestBuildings:
    def test_buildings_paint_roofs(self):
        store, col = run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, *ROAD,
                          {"op": "frontage", "out": "lots", "roads": ["road"], "road_width": 20, "id": "f"},
                          {"op": "buildings", "src": "lots", "id": "b"}], **TOWN)
        c = store.get("canvas").data
        assert (np.abs(c[..., :3] - 1).max(-1) > 0.1).mean() > 0.05
        assert "building" in col.collector.legend

    def test_building_needs_polygons(self):
        with pytest.raises(RecipeError, match="polygon"):
            run([{"op": "canvas", "out": "canvas", "color": "#ffffff"}, *ROAD,
                 {"op": "buildings", "src": "road"}], **TOWN)
