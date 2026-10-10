"""Tests for maps/build_maps.py, the keyed palace maps (review-fix task R4.1, owner QR5).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q

What they hold the maps to:
- the five maps build, parse as SVG, and carry a title, a legend and (when drawn to
  scale) a scale bar;
- every room code chapter IV uses (B0–B13) is on the overview, with the floor it is on;
- every measured shape agrees with the `maps` block of facts.yaml (the O28 sizes);
- the committed SVGs are what the script builds (no hand edits), each has a PNG;
- chapter VIII embeds every map, and the cards' Terrain lines point at them.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml

TOOLS = Path(__file__).resolve().parent
MODULE = TOOLS.parent
MAPS = MODULE / "maps"
sys.path.insert(0, str(MAPS))
import build_maps as B  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"
FACTS = yaml.safe_load((MODULE / "facts.yaml").read_text(encoding="utf-8"))["maps"]
SCALED = ["map_viii_2_gatehouse", "map_viii_3_court", "map_viii_4_terraces", "map_viii_5_east_wing"]
ALL = ["map_viii_1_palace"] + SCALED


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("maps")
    paths = B.build_all(out, png=False)
    return {p.stem: p for p in paths}


def root(path):
    return ET.parse(path).getroot()


def texts(el):
    return [("".join(t.itertext())).strip() for t in el.iter(SVG_NS + "text")]


def fact(dotted):
    node = FACTS
    for part in dotted.split("."):
        node = node[part]
    return node


# --------------------------------------------------------------------------- building

def test_build_all_writes_the_five_maps(built):
    assert sorted(built) == sorted(ALL)


def test_every_map_parses_as_svg_with_a_viewbox(built):
    for name, p in built.items():
        r = root(p)
        assert r.tag == SVG_NS + "svg", name
        assert len(r.get("viewBox").split()) == 4, name


def test_every_map_has_a_title_cartouche_and_a_legend(built):
    for name, p in built.items():
        ids = {e.get("id") for e in root(p).iter()}
        assert {"title", "legend", "caption"} <= ids, name


def test_scaled_maps_have_a_scale_bar_and_a_grid_layer(built):
    for name in SCALED:
        ids = {e.get("id") for e in root(built[name]).iter()}
        assert "scalebar" in ids and "grid" in ids, name


def test_overview_says_it_is_not_to_scale(built):
    assert any("not to scale" in t.lower() for t in texts(root(built["map_viii_1_palace"])))


def test_grid_can_be_left_out(tmp_path):
    p = B.build_one("map_viii_3_court", tmp_path, png=False, grid=False)
    ids = {e.get("id") for e in root(p).iter()}
    assert "grid" not in ids and "scalebar" in ids


def test_unknown_map_name_is_an_error(tmp_path):
    with pytest.raises(KeyError):
        B.build_one("map_of_nowhere", tmp_path, png=False)


def test_missing_maps_block_is_a_clear_error(tmp_path):
    bad = tmp_path / "facts.yaml"
    bad.write_text("version: 1\nfacts: []\n", encoding="utf-8")
    with pytest.raises(ValueError, match="maps"):
        B.load_dims(bad)


def test_missing_dimension_is_a_clear_error(tmp_path):
    data = yaml.safe_load((MODULE / "facts.yaml").read_text(encoding="utf-8"))
    del data["maps"]["court"]["width"]
    bad = tmp_path / "facts.yaml"
    bad.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ValueError, match="court.width"):
        B.load_dims(bad)


def test_every_map_says_what_is_approximate(built):
    for name, p in built.items():
        cap = [e for e in root(p).iter() if e.get("id") == "caption"][0]
        assert "pproximate" in " ".join(texts(cap)) or "schematic" in " ".join(texts(cap)), name


# --------------------------------------------------------------------------- the overview

def room_codes_in_04():
    text = (MODULE / "04_The_Ball.md").read_text(encoding="utf-8")
    return sorted(set(re.findall(r"\bB(\d{1,2})\b", text)), key=int)


def test_chapter_iv_codes_are_b0_to_b13():
    assert room_codes_in_04() == [str(n) for n in range(14)]


def test_every_room_code_in_04_is_on_the_overview(built):
    labels = " ".join(texts(root(built["map_viii_1_palace"])))
    for n in room_codes_in_04():
        assert re.search(rf"\bB{n}\b", labels), f"B{n} missing from the overview"


def test_every_overview_room_states_its_floor(built):
    boxes = [e for e in root(built["map_viii_1_palace"]).iter() if e.get("data-room")]
    codes = {e.get("data-room") for e in boxes}
    assert {f"B{n}" for n in range(14)} <= codes
    for e in boxes:
        assert e.get("data-floor"), e.get("data-room")


def test_overview_floors_follow_the_text(built):
    floors = {e.get("data-room"): e.get("data-floor")
              for e in root(built["map_viii_1_palace"]).iter() if e.get("data-room")}
    assert floors["B2"] == "ground"
    assert floors["B3"] == "gallery" and floors["B9"] == "gallery"
    assert floors["B8"] == "second"
    assert floors["B11"] == "cellar"


# --------------------------------------------------------------------------- dimensions

def measured(r):
    """(element, feet) pairs for every shape that declares the dimension it draws."""
    root_scale = float(r.get("data-px-per-ft"))
    for e in r.iter():
        scale = float(e.get("data-px-per-ft", root_scale))
        for axis, attr in (("w", "width"), ("h", "height")):
            key = e.get(f"data-fact-{axis}")
            if key:
                yield e, key, float(e.get(attr)) / scale
        key = e.get("data-fact-len")
        if key:
            x1, y1, x2, y2 = (float(e.get(a)) for a in ("x1", "y1", "x2", "y2"))
            yield e, key, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / scale


def expected(key):
    if re.fullmatch(r"\d+(\.\d+)?", key):
        return float(key)
    return float(fact(key))


def test_scaled_maps_measure_enough_shapes(built):
    need = {"map_viii_2_gatehouse": 4, "map_viii_3_court": 6,
            "map_viii_4_terraces": 6, "map_viii_5_east_wing": 5}
    for name, n in need.items():
        assert len(list(measured(root(built[name])))) >= n, name


def test_measured_shapes_match_facts_yaml(built):
    for name in SCALED:
        for e, key, feet in measured(root(built[name])):
            assert feet == pytest.approx(expected(key), abs=0.01), (name, key, e.get("id"))


def test_room_widths_in_the_east_wing_are_20_to_30_feet(built):
    lo, hi = fact("east_wing.room_across.min"), fact("east_wing.room_across.max")
    r = root(built["map_viii_5_east_wing"])
    scale = float(r.get("data-px-per-ft"))
    rooms = [e for e in r.iter() if e.get("data-room-across")]
    assert len(rooms) == 3
    for e in rooms:
        across = float(e.get(e.get("data-room-across"))) / scale
        assert lo <= across <= hi, e.get("id")


def test_labelled_numbers_match_facts_yaml(built):
    seen = 0
    for name in ALL:
        for e in root(built[name]).iter(SVG_NS + "text"):
            key = e.get("data-fact")
            if key:
                seen += 1
                value = fact(key)
                assert re.search(rf"\b{value}\b", "".join(e.itertext())), (name, key)
    assert seen >= 6


def test_scale_bars_are_true(built):
    for name in SCALED:
        bar = [e for e in root(built[name]).iter() if e.get("id") == "scalebar-span"]
        assert bar, name
        assert any(k == "50" or k == "20" for _, k, _ in measured(root(built[name]))), name


def test_facts_maps_block_agrees_with_chapter_v():
    text = re.sub(r"\s+", " ", (MODULE / "05_The_Longest_Night.md").read_text(encoding="utf-8"))
    c, t, w = FACTS["court"], FACTS["terraces"], FACTS["east_wing"]
    for phrase in (f"about {c['length']} feet long and {c['width']} feet wide",
                   f"some {c['vault']} feet high", f"main doors ({c['main_doors']} feet wide)",
                   f"({c['dais_high']} feet high, {c['dais_across']} feet across)",
                   f"about {c['dais_from_doors']} feet from them",
                   f"rails {c['gallery_rail']} feet above the floor",
                   f"rises {c['east_stair_rise']} feet",
                   f"about {t['deep']} feet deep and {t['wide']} feet wide",
                   f"{t['drop']}-foot drop", f"about {t['lower_garden']} feet to the river gate",
                   f"{w['cleared_corridor']['wide']} feet wide and about "
                   f"{w['cleared_corridor']['long']} feet long",
                   f"about {w['inner_corridor']['long']} feet long",
                   f"{w['room_across']['min']} to {w['room_across']['max']} feet across"):
        assert phrase in text, phrase


def test_facts_gatehouse_block_agrees_with_card_s3():
    text = re.sub(r"\s+", " ", (MODULE / "09_The_Snakes.md").read_text(encoding="utf-8"))
    g = FACTS["gatehouse"]
    assert f"{g['gate_walk_height']} feet above the arch" in text
    assert f"{g['walk_to_street_drop']}-foot drop to the street" in text
    assert f"falls {g['stair_fall']} feet" in text
    assert f"{g['wicket_wide']} feet wide" in text
    assert f"{g['blades_out']} feet out from the gate" in text


# --------------------------------------------------------------------------- committed files

def test_committed_svgs_match_the_script(built):
    for name, p in built.items():
        committed = MAPS / f"{name}.svg"
        assert committed.exists(), f"run python maps/build_maps.py ({name}.svg missing)"
        assert committed.read_text(encoding="utf-8") == p.read_text(encoding="utf-8"), (
            f"{name}.svg is stale or hand-edited: run python maps/build_maps.py")


def test_every_committed_svg_has_a_png():
    for name in ALL:
        assert (MAPS / f"{name}.png").stat().st_size > 10_000, name


# --------------------------------------------------------------------------- the book

def test_chapter_viii_embeds_every_map_with_a_png_link():
    text = (MODULE / "08_Handouts.md").read_text(encoding="utf-8")
    for name in ALL:
        assert f"](maps/{name}.svg)" in text, name
        assert f"](maps/{name}.png)" in text, name


def test_chapter_viii_has_no_ascii_palace_figure_left():
    text = (MODULE / "08_Handouts.md").read_text(encoding="utf-8")
    section = text.split("## The Palace, Keyed")[1].split("\n## ")[0]
    assert "```" not in section
    assert "**Rooms the text does not place:**" in section


def test_chapter_viii_numbers_its_maps_in_order():
    text = (MODULE / "08_Handouts.md").read_text(encoding="utf-8")
    nums = [int(n) for n in re.findall(r"\*\*Map VIII–(\d):", text)]
    assert nums == [1, 2, 3, 4, 5]


def card_terrain(card):
    text = (MODULE / "09_The_Snakes.md").read_text(encoding="utf-8")
    body = text.split(f"\n## {card}. ")[1].split("\n## ")[0]
    para = body.split("**Terrain as rules.**")[1][:400]
    return para


@pytest.mark.parametrize("card,mapno", [("S1", 3), ("S2", 5), ("S3", 2), ("S6", 4), ("S7", 5),
                                        ("S9", 4), ("S10", 5), ("S11", 3), ("S13", 3)])
def test_card_terrain_lines_point_to_their_map(card, mapno):
    assert re.search(rf"(?i)see map VIII–{mapno}\b", card_terrain(card))


def test_chapter_v_general_features_points_to_the_maps():
    text = (MODULE / "05_The_Longest_Night.md").read_text(encoding="utf-8")
    gf = text.split("### The Palace After Midnight: General Features")[1].split("\n### ")[0]
    assert re.search(r"(?i)see maps VIII–1 to VIII–5", gf)


@pytest.mark.parametrize("area,mapno", [("B1", 2), ("B2", 3), ("B3", 3), ("B5", 4),
                                        ("B9", 5), ("B10", 5)])
def test_chapter_iv_areas_point_to_their_map(area, mapno):
    text = (MODULE / "04_The_Ball.md").read_text(encoding="utf-8")
    body = text.split(f"\n**{area}. ")[1].split("\n**B")[0]
    assert re.search(rf"(?i)see map VIII–{mapno}\b", body)
