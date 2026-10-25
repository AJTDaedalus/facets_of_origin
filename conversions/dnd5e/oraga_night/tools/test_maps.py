"""Tests for maps/build_maps.py, the keyed palace maps (review-fix task R4.1, owner QR5).

Run: python -m pytest conversions/dnd5e/oraga_night/tools -q

What they hold the maps to:
- the five maps build, parse as SVG, and carry a title, a legend and (when drawn to
  scale) a scale bar;
- every room code chapter IV uses (B0–B13) is on the overview, with the floor it is on;
- every measured shape agrees with the `maps` block of facts.yaml (the O28 sizes);
- the committed SVGs are what the script builds (no hand edits), each has a PNG;
- no map label prints development scaffolding (decision IDs, "?", "not given"), and each
  map has one clean caption line (R6.2);
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


def test_overview_states_its_scale(built):
    # T8.3 (N11): the overview is a small-scale plan now, not a schematic of boxes
    r = root(built["map_viii_1_palace"])
    assert any("small-scale plan" in t.lower() for t in texts(caption_of(built["map_viii_1_palace"])))
    ids = {e.get("id") for e in r.iter()}
    assert "overview-scale" in ids and "grid" not in ids


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


def caption_of(path):
    return [e for e in root(path).iter() if e.get("id") == "caption"][0]


def test_every_map_has_one_clean_caption_line(built):
    # R6.2 (review 2, N3): one caption line, in a reader's voice, not an audit note
    for name, p in built.items():
        lines = [t for t in texts(caption_of(p)) if t]
        assert len(lines) == 1, (name, lines)
        assert len(lines[0]) <= 110, (name, lines[0])


SCAFFOLDING = [r"\bO\d{2}\b", r"\?", r"(?i)not given", r"(?i)plausib", r"(?i)not placed",
               r"(?i)\bthe text\b", r"(?i)east only", r"(?i)placed by connection"]


@pytest.mark.parametrize("pattern", SCAFFOLDING)
def test_no_map_label_prints_development_scaffolding(built, pattern):
    # decision IDs, question marks and hedges belong in facts.yaml and DECISIONS, not on a map
    for name, p in built.items():
        for t in texts(root(p)):
            assert not re.search(pattern, t), (name, t)


def test_no_map_says_approximate(built):
    # T8.3 (L-062): the "other positions approximate" hedge is gone from every caption too
    for name, p in built.items():
        for t in texts(root(p)):
            assert "pproximate" not in t, (name, t)


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

def test_chapter_viii_embeds_every_map_without_file_links():
    # R6.2 (review 2, N3): the book embeds each map; it prints no "[PNG]" file links
    text = (MODULE / "08_Handouts.md").read_text(encoding="utf-8")
    for name in ALL:
        assert f"](maps/{name}.svg)" in text, name
        assert f"](maps/{name}.png)" not in text, name
    assert "[PNG]" not in text
    assert "plausibl" not in text
    assert "does not place" not in text


def test_chapter_viii_has_no_ascii_palace_figure_left():
    text = (MODULE / "08_Handouts.md").read_text(encoding="utf-8")
    section = text.split("## The Palace, Keyed")[1].split("\n## ")[0]
    assert "```" not in section
    assert "**Rooms beyond maps VIII–2 to VIII–5:**" in section
    assert "by connection" not in section


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
    assert re.search(rf"(?i)(?:see|, and) map VIII–{mapno}\b", body)


# --------------------------------------------------------------------------- WP8 geometry

def test_rail_drops_agree_with_the_room_sizes():
    # T8.1 (L-062): one drop per rail; the gallery and terrace values are the printed ones
    r = FACTS["rails"]
    assert r["gallery"] == FACTS["court"]["gallery_rail"] == 12
    assert r["terrace"] == FACTS["terraces"]["drop"] == 10
    assert 0 < r["walk"] < r["terrace"]


def test_s10_wall_adds_up():
    # T8.1 (TP64, brief §1.5): wing floor 12 + sill 3 + the garden 5 below the Court = 20
    w = FACTS["east_wing"]
    assert w["floor"] + w["window_sill"] + w["garden_below_court"] == w["window_wall"] == 20


def test_gallery_geometry_values():
    c = FACTS["court"]
    assert c["aisle_deep"] == (FACTS["terraces"]["wide"] - c["width"]) / 2   # aisle under the gallery
    assert c["gallery_stairs"] == 2 and c["gallery_stair_rise"] == c["gallery_rail"]
    assert c["ward_points_dais"] == 4 and c["ward_points_doors"] == 2
    wd = c["west_doors"]
    assert 0 < wd["b4_at"] < wd["b4_at"] + wd["b4_wide"] < wd["service_at"] < c["length"]


def test_missing_rails_block_is_a_clear_error(tmp_path):
    data = yaml.safe_load((MODULE / "facts.yaml").read_text(encoding="utf-8"))
    del data["maps"]["rails"]
    bad = tmp_path / "facts.yaml"
    bad.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ValueError, match="rails.gallery"):
        B.load_dims(bad)


def test_overview_places_every_room_without_by_connection_boxes(built):
    # T8.3 (N11): no room is boxed "by connection"; B13 and B11 carry their own levels
    r = root(built["map_viii_1_palace"])
    floors = {e.get("data-room"): e.get("data-floor") for e in r.iter() if e.get("data-room")}
    assert "unknown" not in floors.values()
    assert floors["B4"] == "ground" and floors["B6"] == "ground" and floors["B7"] == "gallery"
    assert floors["B13"] == "terrace"
    assert not any("by connection" in t.lower() for t in texts(r))


def test_court_map_draws_the_gallery_stairs_and_floor_level_aisles(built):
    # T8.2 (L-032): two stairs up to the galleries; the aisles are ground level
    r = root(built["map_viii_3_court"])
    ids = {e.get("id") for e in r.iter()}
    assert {"west-aisle", "east-aisle", "musicians-gallery", "high-gallery"} <= ids
    labels = " ".join(texts(r))
    assert labels.count("stair up") >= 3          # two gallery stairs and the east stair
    assert "at floor level" in labels
    piers = [e for e in r.iter() if e.get("data-pier")]
    assert len(piers) == 14


def test_court_map_draws_the_six_ward_points(built):
    # T8.3 (L-062): Tables V–2 and V–3 count four on the dais and two by the doors
    r = root(built["map_viii_3_court"])
    wards = [e.get("data-ward") for e in r.iter() if e.get("data-ward")]
    assert wards.count("dais") == FACTS["court"]["ward_points_dais"]
    assert wards.count("doors") == FACTS["court"]["ward_points_doors"]


def test_only_the_double_doors_are_marked_to_seal(built):
    # T8.3 (TP28): one seal mark on VIII–5, across the double doors (10 ft)
    r = root(built["map_viii_5_east_wing"])
    scale = float(r.get("data-px-per-ft"))
    seals = [e for e in r.iter() if e.get("data-seal")]
    assert len(seals) == 1
    e = seals[0]
    length = abs(float(e.get("x2")) - float(e.get("x1"))) / scale
    assert length == pytest.approx(FACTS["east_wing"]["cleared_corridor"]["wide"])


@pytest.mark.parametrize("name", ["map_viii_3_court", "map_viii_4_terraces", "map_viii_5_east_wing"])
def test_the_walk_rail_has_its_own_symbol(built, name):
    # T8.3 (L-062): the garden walk's rail is not drawn as a terrace balustrade
    legend = [e for e in root(built[name]).iter() if e.get("id") == "legend"][0]
    assert any("garden walk's rail" in t.lower() for t in texts(legend))
