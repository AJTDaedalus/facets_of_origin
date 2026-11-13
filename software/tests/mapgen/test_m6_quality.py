"""T27-T29: image metrics, comparator manifest/bands, contact sheet."""
import os
from pathlib import Path

import numpy as np
import pytest
from PIL import Image as PImage

from mapgen import quality as Q

REF = Path(os.environ.get("MAPGEN_REF_DIR", "/mnt/e/books/DandD 5E"))
HAVE_REFS = REF.is_dir()


def img(arr):
    a = np.asarray(arr, np.float32)
    if a.ndim == 2:
        a = np.repeat(a[..., None], 3, -1)
    return PImage.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


FLAT = img(np.full((200, 200), 0.5))
CHECK = img((np.indices((200, 200)).sum(0) // 5 % 2).astype(float))
NOISE = img(np.random.default_rng(0).random((200, 200)))


class TestMetrics:
    def test_flat_grey(self):
        m = Q.metrics(FLAT, px_per_square=50)
        assert m["Q1"] < 0.01 and m["Q2"] < 0.001 and m["Q3"] < 0.001 and m["Q4"] < 0.001

    def test_checkerboard_has_ink(self):
        assert Q.metrics(CHECK, px_per_square=50)["Q4"] > 0.3

    def test_noise_has_detail(self):
        m = Q.metrics(NOISE, px_per_square=50)
        assert m["Q2"] > 0.1 and m["Q1"] > 0.8

    def test_q3_blotches(self):
        y = np.indices((200, 200))[1] / 200
        m = Q.metrics(img(y), px_per_square=50)
        assert m["Q3"] > 0.1 and m["Q2"] < 0.02

    def test_two_hue_clusters(self):
        a = np.zeros((100, 100, 3))
        a[:, :50] = [0.9, 0.1, 0.1]
        a[:, 50:] = [0.1, 0.1, 0.9]
        m = Q.metrics(img(a), px_per_square=50)
        assert m["Q5h"] == 2 and m["Q5s"] > 0.7

    def test_grey_has_no_hues(self):
        assert Q.metrics(NOISE, px_per_square=50)["Q5h"] == 0

    def test_normalises_scale(self):
        big = NOISE.resize((400, 400), PImage.NEAREST)
        a, b = Q.metrics(NOISE, px_per_square=50), Q.metrics(big, px_per_square=100)
        assert a["Q4"] == pytest.approx(b["Q4"], rel=0.2)

    def test_normalises_per_foot(self):
        # a 10-ft square at 100 px is the same scale as a 5-ft square at 50 px
        big = NOISE.resize((400, 400), PImage.NEAREST)
        a = Q.metrics(NOISE, px_per_square=50)
        b = Q.metrics(big, px_per_square=200, feet_per_square=10)
        assert a["Q4"] == pytest.approx(b["Q4"], rel=0.2)

    def test_crop_and_exclude(self):
        a = np.full((200, 200), 0.5)
        a[:, 100:] = np.random.default_rng(1).random((200, 100))
        m = Q.metrics(img(a), px_per_square=50, crop=[0, 0, 0.5, 1])
        assert m["Q2"] < 0.001
        m2 = Q.metrics(img(a), px_per_square=50, exclude=[[0.5, 0, 1, 1]])
        assert m2["Q2"] < 0.01

    def test_q6_grid_subordination(self):
        L = np.full((100, 100), 0.8)
        grid = np.zeros((100, 100))
        grid[:, ::20] = 1
        walls = np.zeros((100, 100))
        walls[50, :] = 1
        L2 = L.copy()
        L2[grid > 0] = 0.7
        L2[walls > 0] = 0.1
        assert Q.q6(L2, grid, walls) < 0.3
        L3 = L.copy()
        L3[grid > 0] = 0.1
        L3[walls > 0] = 0.6
        assert Q.q6(L3, grid, walls) > 1.0


class TestManifestAndBands:
    def test_manifest_shape(self):
        man = Q.load_manifest()
        assert set(man["comparators"]) >= {f"C{i}" for i in range(1, 8)}
        for cat in ("built_interior", "cave", "outdoor"):
            assert man["categories"][cat]

    def test_band_check(self):
        bands = {"cave": {"Q1": [0.2, 0.6]}}
        assert Q.check_bands({"Q1": 0.4}, bands, "cave") == {"Q1": (0.4, [0.2, 0.6], True)}
        assert Q.check_bands({"Q1": 0.9}, bands, "cave")["Q1"][2] is False

    def test_bands_from_values(self):
        b = Q.bands_from({"C1": {"Q1": 0.5}, "C2": {"Q1": 0.7}}, ["C1", "C2"])
        assert b["Q1"] == [pytest.approx(0.425), pytest.approx(0.805)]

    def test_recorded_bands_cover_phase1(self):
        bands = Q.load_bands()
        for cat in ("built_interior", "cave", "outdoor"):
            assert {"Q1", "Q2", "Q3", "Q4", "Q5s"} <= set(bands[cat])

    @pytest.mark.skipif(not HAVE_REFS, reason="comparator packs not present (MAPGEN_REF_DIR)")
    def test_live_comparator_metrics_match_recorded(self):
        live = Q.comparator_metrics("C2", REF)
        rec = Q.load_bands()["_values"]["C2"]
        for k in ("Q1", "Q2", "Q4"):
            assert live[k] == pytest.approx(rec[k], rel=0.02)


class TestSheet:
    def test_sheet_shapes_and_scale(self, tmp_path):
        ours = img(np.random.default_rng(2).random((140, 140)))
        theirs = img(np.random.default_rng(3).random((600, 900)))
        out = tmp_path / "s.png"
        Q.make_sheet(ours, 70, theirs, 150, out)
        s = PImage.open(out)
        assert s.size[1] == 100 + Q.SHEET_LABEL_H and s.size[0] >= 200

    def test_refuses_repo_path(self, tmp_path):
        ours = img(np.zeros((10, 10)))
        with pytest.raises(ValueError, match="repo"):
            Q.make_sheet(ours, 70, ours, 70, Path(Q.REPO_ROOT) / "software" / "x.png")

    def test_sheet_limits_comparator_to_our_size(self, tmp_path):
        ours = img(np.zeros((70, 70)))
        theirs = img(np.ones((3000, 3000)))
        out = tmp_path / "s.png"
        Q.make_sheet(ours, 70, theirs, 150, out)
        assert PImage.open(out).size[0] <= 50 * 2 + 40
