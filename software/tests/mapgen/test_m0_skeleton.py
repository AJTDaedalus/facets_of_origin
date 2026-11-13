"""T1-T6: package, recipe models, units, layer store, registry, engine, includes."""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from mapgen import __main__ as cli
from mapgen.recipe import RecipeError, load_recipe, parse_recipe
from mapgen.units import Frame
from mapgen.layers import Geometry, Mask, Field, Image, LayerStore
from mapgen.registry import OpRegistry, ParamModel
from mapgen.engine import Engine, step_seed
from tests.mapgen.conftest import header

SOFTWARE = Path(__file__).resolve().parents[2]


# ---------- T1 ----------
class TestCli:
    def test_help_lists_subcommands(self):
        r = subprocess.run([sys.executable, "-m", "mapgen", "--help"], cwd=SOFTWARE,
                           capture_output=True, text=True)
        assert r.returncode == 0
        for sub in ("render", "ops", "quality", "sheet"):
            assert sub in r.stdout

    def test_unknown_subcommand_fails(self):
        with pytest.raises(SystemExit) as e:
            cli.main(["frobnicate"])
        assert e.value.code != 0

    def test_no_subcommand_prints_help_and_fails(self, capsys):
        assert cli.main([]) == 2


# ---------- T2 ----------
class TestRecipeModels:
    def test_valid_recipe(self):
        r = parse_recipe({"map": header(), "steps": [{"op": "rect", "out": "a", "x": 0}]})
        assert r.map.width_ft == 20 and r.steps[0].op == "rect"
        assert r.steps[0].params() == {"x": 0}

    def test_missing_header(self):
        with pytest.raises(RecipeError, match="map"):
            parse_recipe({"steps": []})

    def test_negative_size_names_field(self):
        with pytest.raises(RecipeError, match="width_ft"):
            parse_recipe({"map": header(width_ft=-3), "steps": []})

    def test_bad_feet_per_square(self):
        with pytest.raises(RecipeError, match="feet_per_square"):
            parse_recipe({"map": header(feet_per_square=7), "steps": []})

    def test_unknown_top_level_key(self):
        with pytest.raises(RecipeError, match="bogus"):
            parse_recipe({"map": header(), "steps": [], "bogus": 1})

    def test_step_without_op(self):
        with pytest.raises(RecipeError, match="op"):
            parse_recipe({"map": header(), "steps": [{"out": "x"}]})

    def test_load_from_file(self, write_recipe):
        p = write_recipe({"map": header(title="Cave"), "steps": []})
        assert load_recipe(p).map.title == "Cave"

    def test_load_bad_yaml(self, write_recipe):
        p = write_recipe("map: [unclosed")
        with pytest.raises(RecipeError, match="YAML"):
            load_recipe(p)


# ---------- T3 ----------
class TestUnits:
    def _h(self, **kw):
        return parse_recipe({"map": header(**kw), "steps": []}).map

    def test_output_and_working_shape(self):
        f = Frame(self._h(width_ft=60, height_ft=40, px_per_square=70, supersample=2))
        assert f.out_size == (840, 560)
        assert f.shape == (1120, 1680)      # (h, w) working

    def test_draft(self):
        f = Frame(self._h(width_ft=60, height_ft=40, px_per_square=70, supersample=2), draft=True)
        assert f.out_size == (420, 280) and f.ss == 1

    def test_ft_to_px(self):
        f = Frame(self._h(px_per_square=70, supersample=2))
        assert f.px(5) == pytest.approx(140)
        assert f.ft(140) == pytest.approx(5)

    def test_ten_foot_squares(self):
        f = Frame(self._h(width_ft=100, height_ft=70, feet_per_square=10, px_per_square=50))
        assert f.out_size == (500, 350)

    def test_rounding(self):
        f = Frame(self._h(width_ft=12.4, height_ft=10, px_per_square=20))
        assert f.out_size == (50, 40)


# ---------- T4 ----------
class P(ParamModel):
    size: float = 1.0


class TestLayersAndRegistry:
    def test_store_put_get_free(self):
        s = LayerStore()
        s.put("a", Mask(np.zeros((2, 2), np.float32)))
        assert isinstance(s.get("a"), Mask)
        s.free("a")
        assert "a" not in s

    def test_store_missing(self):
        with pytest.raises(KeyError):
            LayerStore().get("nope")

    def test_inverted_mask(self):
        s = LayerStore()
        s.put("a", Mask(np.array([[0.0, 0.25]], np.float32)))
        assert np.allclose(s.get("~a").data, [[1.0, 0.75]])

    def test_register_and_lookup(self):
        reg = OpRegistry()

        @reg.op("thing", params=P, output=Mask, group="test")
        def thing(ctx, p):
            """Make a thing."""
        spec = reg.get("thing")
        assert spec.params is P and spec.output is Mask and spec.doc == "Make a thing."

    def test_duplicate_name(self):
        reg = OpRegistry()
        reg.op("x", params=P)(lambda ctx, p: None)
        with pytest.raises(ValueError):
            reg.op("x", params=P)(lambda ctx, p: None)

    def test_unknown_op(self):
        with pytest.raises(KeyError):
            OpRegistry().get("zzz")

    def test_list_is_sorted_by_group_then_name(self):
        reg = OpRegistry()
        for g, n in [("b", "z"), ("a", "y"), ("a", "x")]:
            reg.op(n, params=P, group=g)(lambda ctx, p: None)
        assert [s.name for s in reg.list()] == ["x", "y", "z"]


# ---------- T5 ----------
def _reg():
    reg = OpRegistry()

    class MakeP(ParamModel):
        value: float = 1.0

    class UseP(ParamModel):
        src: str

    @reg.op("make", params=MakeP, output=Mask)
    def make(ctx, p):
        return Mask(np.full(ctx.frame.shape, p.value, np.float32))

    @reg.op("noise_field", params=MakeP, output=Field)
    def nf(ctx, p):
        return Field(ctx.rng.random(ctx.frame.shape).astype(np.float32))

    @reg.op("use", params=UseP, inputs={"src": Mask}, output=Mask)
    def use(ctx, p, src):
        return Mask(src.data * 0.5)

    return reg


def _recipe(steps, **h):
    return parse_recipe({"map": header(**h), "steps": steps})


class TestEngine:
    def test_runs_in_order(self):
        e = Engine(_recipe([{"op": "make", "out": "a", "value": 0.8},
                            {"op": "use", "out": "b", "src": "a"}]), registry=_reg())
        store = e.run(keep_all=True)
        assert np.allclose(store.get("b").data, 0.4)

    def test_missing_ref_names_step(self):
        e = Engine(_recipe([{"op": "use", "out": "b", "src": "ghost"}]), registry=_reg())
        with pytest.raises(RecipeError, match=r"step 1 .*use.*ghost"):
            e.run()

    def test_type_error_caught_before_running(self):
        ran = []
        reg = _reg()
        orig = reg.get("make").fn
        reg.get("make").fn = lambda ctx, p: ran.append(1) or orig(ctx, p)
        e = Engine(_recipe([{"op": "make", "out": "a"},
                            {"op": "noise_field", "out": "f"},
                            {"op": "use", "out": "b", "src": "f"}]), registry=reg)
        with pytest.raises(RecipeError, match="Mask"):
            e.run()
        assert ran == []

    def test_bad_param_names_step(self):
        e = Engine(_recipe([{"op": "make", "out": "a", "value": "lots"}]), registry=_reg())
        with pytest.raises(RecipeError, match=r"step 1.*value"):
            e.run()

    def test_unknown_op(self):
        e = Engine(_recipe([{"op": "teleport", "out": "a"}]), registry=_reg())
        with pytest.raises(RecipeError, match="teleport"):
            e.run()

    def test_inverted_ref_accepted(self):
        e = Engine(_recipe([{"op": "make", "out": "a", "value": 0.2},
                            {"op": "use", "out": "b", "src": "~a"}]), registry=_reg())
        assert np.allclose(e.run(keep_all=True).get("b").data, 0.4)

    def test_seed_stable_under_insertion(self):
        s1 = [{"op": "noise_field", "out": "f", "id": "n"}]
        s2 = [{"op": "make", "out": "a"}] + s1
        a = Engine(_recipe(s1), registry=_reg()).run(keep_all=True).get("f").data
        b = Engine(_recipe(s2), registry=_reg()).run(keep_all=True).get("f").data
        assert np.array_equal(a, b)

    def test_seed_changes_with_map_seed(self):
        assert step_seed(1, "n", 0) != step_seed(2, "n", 0)
        assert step_seed(1, "n", 0) != step_seed(1, "n", 1)

    def test_liveness_frees_dead_layers(self):
        e = Engine(_recipe([{"op": "make", "out": "a"},
                            {"op": "use", "out": "b", "src": "a"},
                            {"op": "make", "out": "canvas"}]), registry=_reg())
        store = e.run()
        assert "a" not in store and "b" not in store and "canvas" in store

    def test_output_required(self):
        e = Engine(_recipe([{"op": "make"}]), registry=_reg())
        with pytest.raises(RecipeError, match="out"):
            e.run()


# ---------- T6 ----------
STYLE = """
palette: {ink: "#222222", floor: "#eeeeee"}
defaults:
  make: {value: 0.3}
macros:
  pair:
    params: {name: m, v: 0.5}
    steps:
      - {op: make, out: "${name}", value: "${v}"}
      - {op: use, out: "${name}_half", src: "${name}"}
"""


class TestIncludes:
    def test_palette_and_defaults(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text(STYLE)
        p = write_recipe({"map": header(include=["style.yaml"]),
                          "steps": [{"op": "make", "out": "a"}]})
        r = load_recipe(p)
        assert r.style.palette["ink"] == "#222222"
        assert r.steps[0].params()["value"] == 0.3

    def test_recipe_params_beat_defaults(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text(STYLE)
        p = write_recipe({"map": header(include=["style.yaml"]),
                          "steps": [{"op": "make", "out": "a", "value": 0.9}]})
        assert load_recipe(p).steps[0].params()["value"] == 0.9

    def test_macro_expansion_keeps_types(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text(STYLE)
        p = write_recipe({"map": header(include=["style.yaml"]),
                          "steps": [{"op": "pair", "name": "room", "v": 0.8, "id": "r"}]})
        r = load_recipe(p)
        assert [s.op for s in r.steps] == ["make", "use"]
        assert r.steps[0].out == "room" and r.steps[0].params()["value"] == 0.8
        assert r.steps[1].params()["src"] == "room" and r.steps[1].out == "room_half"
        assert r.steps[0].id == "r/0"

    def test_macro_default_params(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text(STYLE)
        p = write_recipe({"map": header(include=["style.yaml"]), "steps": [{"op": "pair"}]})
        r = load_recipe(p)
        assert r.steps[0].out == "m" and r.steps[0].params()["value"] == 0.5

    def test_unknown_macro_param(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text(STYLE.replace('"${v}"', '"${nope}"'))
        p = write_recipe({"map": header(include=["style.yaml"]), "steps": [{"op": "pair"}]})
        with pytest.raises(RecipeError, match="nope"):
            load_recipe(p)

    def test_recursion_guard(self, write_recipe, tmp_path):
        (tmp_path / "style.yaml").write_text("macros:\n  loop:\n    steps:\n      - {op: loop}\n")
        p = write_recipe({"map": header(include=["style.yaml"]), "steps": [{"op": "loop"}]})
        with pytest.raises(RecipeError, match="recurs"):
            load_recipe(p)

    def test_include_relative_to_recipe(self, write_recipe, tmp_path):
        sub = tmp_path / "deep"
        sub.mkdir()
        (sub / "s.yaml").write_text(STYLE)
        p = write_recipe({"map": header(include=["s.yaml"]), "steps": []}, folder=sub)
        assert load_recipe(p).style.palette["floor"] == "#eeeeee"

    def test_missing_include(self, write_recipe):
        p = write_recipe({"map": header(include=["nope.yaml"]), "steps": []})
        with pytest.raises(RecipeError, match="nope.yaml"):
            load_recipe(p)

    def test_builtin_style_include(self, write_recipe):
        p = write_recipe({"map": header(include=["styles/inked_parchment.yaml"]), "steps": []})
        assert "ink" in load_recipe(p).style.palette
