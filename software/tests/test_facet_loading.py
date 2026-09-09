"""Tests for Facet YAML loading, schema validation, and cross-reference checks."""
import textwrap
from pathlib import Path

import pytest
import yaml

from app.facets.loader import FacetLoadError, load_facet_file
from app.facets.registry import MergedRuleset, build_ruleset
from app.facets.schema import FacetFile


# ---------------------------------------------------------------------------
# Base ruleset loading
# ---------------------------------------------------------------------------

class TestBaseRulesetLoading:
    def test_base_loads_without_error(self, ruleset):
        assert ruleset is not None

    def test_minor_attributes_count(self, ruleset):
        assert len(ruleset.minor_attributes) == 9

    def test_all_nine_minor_attributes_present(self, ruleset):
        ids = {a.id for a in ruleset.minor_attributes}
        expected = {"strength", "dexterity", "constitution",
                    "intelligence", "wisdom", "knowledge",
                    "spirit", "luck", "charisma"}
        assert ids == expected

    def test_three_major_attributes(self, ruleset):
        assert len(ruleset.major_attributes) == 3
        ids = {a.id for a in ruleset.major_attributes}
        assert ids == {"body", "mind", "soul"}

    def test_three_character_facets(self, ruleset):
        assert len(ruleset.character_facets) == 3
        ids = {cf.id for cf in ruleset.character_facets}
        assert ids == {"body", "mind", "soul"}

    def test_skills_loaded(self, ruleset):
        assert len(ruleset.skills) > 0

    def test_five_body_skills_active(self, ruleset):
        body_skills = [s for s in ruleset.skills if s.facet == "body" and s.status == "active"]
        assert len(body_skills) == 5
        skill_ids = {s.id for s in body_skills}
        assert skill_ids == {"athletics", "combat", "stealth", "finesse", "endurance"}

    def test_roll_resolution_loaded(self, ruleset):
        assert ruleset.roll_resolution is not None
        assert ruleset.roll_resolution.thresholds["full_success"] == 10
        assert ruleset.roll_resolution.thresholds["partial_success"] == 7

    def test_spark_loaded(self, ruleset):
        assert ruleset.spark is not None
        assert ruleset.spark.base_sparks_per_session == 3
        assert len(ruleset.spark.earn_methods) == 4

    def test_advancement_loaded(self, ruleset):
        adv = ruleset.advancement
        assert adv is not None
        assert adv.session_skill_points == 4
        assert (adv.marks_per_rank.practiced,
                adv.marks_per_rank.expert,
                adv.marks_per_rank.master) == (3, 5, 8)
        assert adv.rank_caps.beyond_practiced == 3
        assert adv.rank_caps.master == 1
        assert adv.facet_level_threshold == 3
        assert adv.major_advancement_threshold == 3

    def test_attribute_ratings_three_tiers(self, ruleset):
        assert len(ruleset.attribute_ratings) == 3
        mods = {r.rating: r.modifier for r in ruleset.attribute_ratings}
        assert mods == {1: -1, 2: 0, 3: 1}

    def test_attribute_distribution_correct(self, ruleset):
        dist = ruleset.attribute_distribution
        assert dist is not None
        assert dist.total_points == 18
        assert dist.min_per_attribute == 1
        assert dist.max_per_attribute == 3

    def test_body_techniques_loaded(self, ruleset):
        assert "body" in ruleset.techniques
        body_tree = ruleset.techniques["body"]
        branch_ids = {b.id for b in body_tree.branches}
        assert branch_ids == {"might", "grace", "iron"}

    def test_each_branch_has_three_tiers(self, ruleset):
        body_tree = ruleset.techniques["body"]
        for branch in body_tree.branches:
            tier_nums = {t.tier for t in branch.tiers}
            assert tier_nums == {1, 2, 3}, f"Branch {branch.id} missing tiers: {tier_nums}"

    def test_difficulty_modifiers_four_levels(self, ruleset):
        mods = {d.label: d.modifier for d in ruleset.roll_resolution.difficulty_modifiers}
        assert mods["Easy"] == 1
        assert mods["Standard"] == 0
        assert mods["Hard"] == -1
        assert mods["Very Hard"] == -2

    def test_skill_point_costs_all_contexts(self, ruleset):
        costs = {c.context: c.cost for c in ruleset.advancement.skill_point_costs}
        assert costs["primary_facet"] == 1
        assert costs["cross_facet"] == 2

    def test_pc_armor_per_scene_budgets_loaded(self, ruleset):
        armor = ruleset.combat.armor
        assert armor.light.downgrades_per_scene == 2
        assert armor.light.tiers_reduced == 1
        assert armor.heavy.downgrades_per_scene == 4
        assert armor.heavy.tiers_reduced == 1

    def test_enemy_durability_loaded(self, ruleset):
        durability = ruleset.combat.enemy_durability
        assert durability.strike_depletion.full_success == 2
        assert durability.strike_depletion.partial_success == 1
        assert durability.strike_depletion.failure == 0
        assert durability.armor_resolve_bonus.light == 1
        assert durability.armor_resolve_bonus.heavy == 2
        assert durability.mook_removed_on == "partial_success"
        assert durability.armored_mook_removed_on == "full_success"

    def test_hazards_threat_clock_loaded(self, ruleset):
        clock = ruleset.hazards.threat_clock
        assert clock.segments == 4
        assert clock.advances_on == ["partial_success", "failure"]
        assert clock.wind_back_cost == "1_action"
        assert clock.wind_back_requires_roll is False

    def test_death_rule_loaded(self, ruleset):
        death = ruleset.death
        assert death.broken_is_lethal is False
        assert death.doom_gate == ["permanent_scar", "heroic_death"]

    def test_spark_refund_variant_defaults_off(self, ruleset):
        assert ruleset.spark.variants.refund_on_failed_pretechnique_cast is False

    def test_graceful_fail_is_structured(self, ruleset):
        methods = {m.id: m for m in ruleset.spark.earn_methods}
        assert methods["graceful_fail"].structured is True

    # L-1 (docs/RESEARCH_completeness_audit.md): the "Spark?" peer call
    # (III.1:70) is an explicit earn method; spark_for_weakness was folded
    # into mm_award per III.1's text, not kept as a separate method.
    def test_peer_call_earn_method_present(self, ruleset):
        methods = {m.id: m for m in ruleset.spark.earn_methods}
        assert "peer_call" in methods
        assert "spark_for_weakness" not in methods

    # L-6 (docs/RESEARCH_completeness_audit.md): minor-attribute descriptions
    # restore the PHB clauses the yaml had trimmed (II.2).
    def test_minor_attribute_descriptions_match_phb_clauses(self, ruleset):
        attrs = {a.id: a.description for a in ruleset.minor_attributes}
        assert "keeping your footing on treacherous ground" in attrs["dexterity"]
        assert "functioning on no sleep or food" in attrs["constitution"]
        assert "finding the flaw in a plan" in attrs["intelligence"]
        assert "finding your way through unfamiliar territory" in attrs["wisdom"]
        assert "Identifying a historical figure or artifact" in attrs["knowledge"]
        assert "holding the line of a ritual" in attrs["spirit"]
        assert "Bending fate in your favor" in attrs["luck"]
        assert "making something you said feel true even when it isn't" in attrs["charisma"]

    # L-8 (docs/RESEARCH_completeness_audit.md): Technique descriptions
    # restore the PHB parentheticals/clauses the yaml had trimmed.
    def test_technique_descriptions_match_phb_clauses(self, ruleset):
        body_iron = next(b for b in ruleset.techniques["body"].branches if b.id == "iron")
        grinding_advance = next(
            t for tier in body_iron.tiers for t in tier.techniques if t.id == "grinding_advance"
        )
        assert "a Spark, a second wind, a reserve of will" in grinding_advance.description

        mind_clarity = next(b for b in ruleset.techniques["mind"].branches if b.id == "clarity")
        sharp_analysis = next(
            t for tier in mind_clarity.tiers for t in tier.techniques if t.id == "sharp_analysis"
        )
        assert "not speculation about future events" in sharp_analysis.description

        soul_presence = next(b for b in ruleset.techniques["soul"].branches if b.id == "presence")
        commanding_presence = next(
            t for tier in soul_presence.tiers for t in tier.techniques
            if t.id == "commanding_presence"
        )
        assert "active, established fictional reasons" in commanding_presence.description
        unforgettable = next(
            t for tier in soul_presence.tiers for t in tier.techniques if t.id == "unforgettable"
        )
        assert "glad to see you" in unforgettable.description


# ---------------------------------------------------------------------------
# Schema validation — malformed Facet files
# ---------------------------------------------------------------------------

class TestFacetSchemaValidation:
    def _write_yaml(self, tmp_path, content: str) -> Path:
        p = tmp_path / "facet.yaml"
        p.write_text(textwrap.dedent(content))
        return p

    def test_missing_required_id_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            name: "Test"
            version: "1.0"
        """)
        with pytest.raises(FacetLoadError, match="id"):
            load_facet_file(path)

    def test_invalid_id_slug_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "invalid id with spaces"
            name: "Test"
            version: "1.0"
        """)
        with pytest.raises(FacetLoadError):
            load_facet_file(path)

    def test_yaml_parse_error_raises(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(": this is not valid yaml: {{{")
        with pytest.raises(FacetLoadError, match="YAML parse error"):
            load_facet_file(path)

    def test_not_a_mapping_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, "- item1\n- item2\n")
        with pytest.raises(FacetLoadError, match="mapping"):
            load_facet_file(path)

    def test_attribute_rating_out_of_range_raises(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "test"
            name: "Test"
            version: "1.0"
            attributes:
              ratings:
                - rating: 0
                  label: Zero
                  modifier: -99
        """)
        with pytest.raises(FacetLoadError):
            load_facet_file(path)

    def test_nonexistent_file_raises(self, tmp_path):
        with pytest.raises(FacetLoadError, match="Cannot read file"):
            load_facet_file(tmp_path / "doesnotexist.yaml")

    def test_valid_minimal_facet_loads(self, tmp_path):
        path = self._write_yaml(tmp_path, """
            id: "minimal"
            name: "Minimal Facet"
            version: "0.0.1"
        """)
        ff = load_facet_file(path)
        assert ff.id == "minimal"
        assert ff.name == "Minimal Facet"


# ---------------------------------------------------------------------------
# Cross-reference validation
# ---------------------------------------------------------------------------

class TestCrossReferenceValidation:
    def test_skill_referencing_unknown_attribute_fails(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "bad-skill"
            name: "Bad Skill Facet"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: "Body"
                description: "test"
                major_attribute: body
            skills:
              - id: bad_skill
                name: "Bad Skill"
                facet: body
                attribute: nonexistent_attribute
                description: "test"
        """))
        from app.facets.loader import load_facet_file as lff
        ff = lff(path)
        with pytest.raises(FacetLoadError, match="unknown attribute"):
            MergedRuleset([ff])

    def test_skill_referencing_unknown_facet_fails(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "bad-facet-ref"
            name: "Test"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: "Body"
                description: "test"
                major_attribute: body
            skills:
              - id: bad_skill
                name: "Bad"
                facet: nonexistent_facet
                attribute: strength
                description: "test"
        """))
        from app.facets.loader import load_facet_file as lff
        ff = lff(path)
        with pytest.raises(FacetLoadError, match="unknown facet"):
            MergedRuleset([ff])


# ---------------------------------------------------------------------------
# Facet composition / override
# ---------------------------------------------------------------------------

class TestFacetComposition:
    def test_later_facet_overrides_skill(self, tmp_path):
        """A second Facet file with the same skill ID wins."""
        from app.facets.loader import load_facet_file as lff

        base_path = tmp_path / "base.yaml"
        base_path.write_text(textwrap.dedent("""
            id: "base-mini"
            name: "Base"
            version: "1.0"
            priority: 0
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: "test"
                  major: body
              major:
                - id: body
                  name: Body
                  description: "test"
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: "test"
                major_attribute: body
            skills:
              - id: athletics
                name: Athletics
                facet: body
                attribute: strength
                description: "Original description"
        """))

        override_path = tmp_path / "override.yaml"
        override_path.write_text(textwrap.dedent("""
            id: "override"
            name: "Override"
            version: "1.0"
            priority: 10
            skills:
              - id: athletics
                name: Athletics
                facet: body
                attribute: strength
                description: "Overridden description"
        """))

        base_ff = lff(base_path)
        override_ff = lff(override_path)
        merged = MergedRuleset([base_ff, override_ff])
        skill = merged.get_skill("athletics")
        assert skill is not None
        assert skill.description == "Overridden description"


# ---------------------------------------------------------------------------
# discover_facet_files edge cases
# ---------------------------------------------------------------------------

class TestDiscoverFacetFiles:
    def test_empty_directory_returns_empty_list(self, tmp_path):
        from app.facets.loader import discover_facet_files
        result = discover_facet_files(tmp_path)
        assert result == []

    def test_nonexistent_directory_returns_empty_list(self, tmp_path):
        from app.facets.loader import discover_facet_files
        result = discover_facet_files(tmp_path / "does_not_exist")
        assert result == []

    def test_directory_with_non_yaml_files_returns_empty(self, tmp_path):
        from app.facets.loader import discover_facet_files
        (tmp_path / "readme.txt").write_text("not a facet")
        (tmp_path / "data.json").write_text("{}")
        result = discover_facet_files(tmp_path)
        assert result == []

    def test_discovers_yaml_in_subdirectory(self, tmp_path):
        from app.facets.loader import discover_facet_files
        sub = tmp_path / "mymod"
        sub.mkdir()
        (sub / "facet.yaml").write_text("id: mymod\nname: My Mod\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        assert len(result) == 1

    def test_discovers_multiple_facets(self, tmp_path):
        from app.facets.loader import discover_facet_files
        for name in ("mod_a", "mod_b", "mod_c"):
            d = tmp_path / name
            d.mkdir()
            (d / "facet.yaml").write_text(f"id: '{name}'\nname: '{name}'\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        assert len(result) == 3

    def test_returns_sorted_paths(self, tmp_path):
        from app.facets.loader import discover_facet_files
        for name in ("c_mod", "a_mod", "b_mod"):
            d = tmp_path / name
            d.mkdir()
            (d / "facet.yaml").write_text(f"id: '{name}'\nname: '{name}'\nversion: '1.0'\n")
        result = discover_facet_files(tmp_path)
        names = [p.parent.name for p in result]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# load_facet_file additional edge cases
# ---------------------------------------------------------------------------

class TestLoadFacetFileEdgeCases:
    def test_facet_with_all_optional_sections_absent(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("id: bare\nname: Bare\nversion: '1.0'\n")
        ff = load_facet_file(path)
        assert ff.facets == []
        assert ff.skills == []
        assert ff.roll_resolution is None
        assert ff.spark is None
        assert ff.advancement is None

    def test_facet_with_valid_technique_prerequisites(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "tech-test"
            name: "Tech Test"
            version: "1.0"
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: test
                  major: body
              major:
                - id: body
                  name: Body
                  description: test
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: test
                major_attribute: body
            techniques:
              body:
                branches:
                  - id: might
                    name: Might
                    attribute: strength
                    tiers:
                      - tier: 1
                        techniques:
                          - id: tier1
                            name: Tier 1
                            description: First tier.
                            prerequisites: []
                      - tier: 2
                        techniques:
                          - id: tier2
                            name: Tier 2
                            description: Requires tier1.
                            prerequisites: [tier1]
                      - tier: 3
                        techniques:
                          - id: tier3
                            name: Tier 3
                            description: Requires tier2.
                            prerequisites: [tier2]
        """))
        ff = load_facet_file(path)
        body_tree = ff.techniques.get("body")
        assert body_tree is not None
        tier2 = body_tree.branches[0].tiers[1].techniques[0]
        assert "tier1" in tier2.prerequisites

    def test_facet_priority_zero_accepted(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text("id: base\nname: Base\nversion: '1.0'\npriority: 0\n")
        ff = load_facet_file(path)
        assert ff.priority == 0

    def test_facet_with_authors_list(self, tmp_path):
        path = tmp_path / "facet.yaml"
        path.write_text(textwrap.dedent("""
            id: "authored"
            name: "Authored Facet"
            version: "1.0"
            authors:
              - Alice
              - Bob
        """))
        ff = load_facet_file(path)
        assert len(ff.authors) == 2
        assert "Alice" in ff.authors


# ---------------------------------------------------------------------------
# Override priority ordering
# ---------------------------------------------------------------------------

class TestFacetOverridePriority:
    def _make_facet_yaml(self, tmp_path, id_, priority, skill_desc):
        d = tmp_path / id_
        d.mkdir()
        (d / "facet.yaml").write_text(textwrap.dedent(f"""
            id: "{id_}"
            name: "{id_}"
            version: "1.0"
            priority: {priority}
            attributes:
              minor:
                - id: strength
                  name: Strength
                  description: test
                  major: body
              major:
                - id: body
                  name: Body
                  description: test
                  minor_attributes: [strength]
            facets:
              - id: body
                name: Body
                description: test
                major_attribute: body
            skills:
              - id: common_skill
                name: Common
                facet: body
                attribute: strength
                description: "{skill_desc}"
        """))
        return d / "facet.yaml"

    def test_higher_priority_wins(self, tmp_path):
        from app.facets.loader import load_facet_file as lff
        path_low = self._make_facet_yaml(tmp_path, "low", 0, "Low priority description")
        path_high = self._make_facet_yaml(tmp_path, "high", 20, "High priority description")
        merged = MergedRuleset([lff(path_low), lff(path_high)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "High priority description"

    def test_equal_priority_last_in_list_wins(self, tmp_path):
        from app.facets.loader import load_facet_file as lff
        path_a = self._make_facet_yaml(tmp_path, "aaa", 10, "AAA description")
        path_b = self._make_facet_yaml(tmp_path, "bbb", 10, "BBB description")
        # bbb appears second in the list
        merged = MergedRuleset([lff(path_a), lff(path_b)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "BBB description"

    def test_base_priority_zero_is_lowest(self, tmp_path):
        """Priority 0 (base) must yield to any module with higher priority."""
        from app.facets.loader import load_facet_file as lff
        path_base = self._make_facet_yaml(tmp_path, "base_mod", 0, "Base description")
        path_mod = self._make_facet_yaml(tmp_path, "expansion", 5, "Expansion description")
        merged = MergedRuleset([lff(path_base), lff(path_mod)])
        skill = merged.get_skill("common_skill")
        assert skill.description == "Expansion description"


# ---------------------------------------------------------------------------
# Lineages merge (D18)
# ---------------------------------------------------------------------------

class TestLineageMerge:
    """Lineages merge by id exactly as Backgrounds do, so a setting Facet adds
    its peoples without disturbing the core's Human — the property the Val'loh
    Facet is built on.
    """

    def _facet(self, **kw):
        return FacetFile(id=kw.pop("id", "extra"), name="Extra",
                         version="0.0.1", **kw)

    def test_base_ships_exactly_one_lineage(self, ruleset):
        assert [lin.id for lin in ruleset.lineages] == ["human"]

    def test_the_core_lineage_is_deliberately_empty(self, ruleset):
        """Human is the baseline every other lineage is measured against, so
        it carries no gift and no heritage — not as an oversight."""
        human = ruleset.get_lineage("human")
        assert human.gift_domains == []
        assert human.heritage is None
        assert human.gift_rate is None

    def test_a_second_module_adds_a_lineage_and_human_survives(self):
        base = load_facet_file(
            Path(__file__).resolve().parents[1] / "facets" / "base" / "facet.yaml")
        extra = self._facet(lineages=[{
            "id": "orthaen", "name": "Orthaen", "description": "Crystal-growers.",
            "gift_domains": [], "heritage": "Reads grown crystalwork.",
        }])
        merged = MergedRuleset([base, extra])
        ids = {lin.id for lin in merged.lineages}
        assert ids == {"human", "orthaen"}

    def test_a_collision_replaces_by_id(self):
        a = self._facet(id="a", lineages=[
            {"id": "human", "name": "Human", "description": "first"}])
        b = self._facet(id="b", lineages=[
            {"id": "human", "name": "Human", "description": "second"}])
        merged = MergedRuleset([a, b])
        assert len(merged.lineages) == 1
        assert merged.get_lineage("human").description == "second"

    def test_unknown_lineage_lookup_returns_none(self, ruleset):
        assert ruleset.get_lineage("nope") is None

    def test_lineages_are_serialized_to_clients(self, ruleset):
        """The builder's Lineage picker renders from the session payload, so a
        lineage the server knows and never sends is a lineage no player can
        choose."""
        assert "lineages" in ruleset.to_client_dict()
        assert ruleset.to_client_dict()["lineages"][0]["id"] == "human"


class TestLineageGiftDomainsResolve:
    """INV-16: every id in a lineage's `gift_domains` resolves in the merged
    domain catalog. INV-7's sibling, and the guard that stops a setting Facet
    from shipping a gift that points at nothing.
    """

    def _domain_ids(self, ruleset) -> set[str]:
        ids = set()
        magic = ruleset.magic
        for attr in ("mind_domains", "soul_domains", "prismatic_domains"):
            for dom in getattr(magic, attr, None) or []:
                ids.add(dom.id)
        return ids

    def test_every_base_gift_domain_resolves(self, ruleset):
        known = self._domain_ids(ruleset)
        for lin in ruleset.lineages:
            for domain_id in lin.gift_domains:
                assert domain_id in known, (
                    f"lineage '{lin.id}' carries gift domain '{domain_id}', "
                    "which is in no loaded domain catalog"
                )

    def test_human_has_nothing_to_resolve(self, ruleset):
        assert ruleset.get_lineage("human").gift_domains == []

    def test_a_dangling_gift_domain_is_detectable(self, ruleset):
        """The invariant has to be able to fail, or it is decoration."""
        known = self._domain_ids(ruleset)
        assert "not_a_real_domain" not in known


class TestItemMerge:
    """Items merge by id like every other collection. The base ruleset ships
    none — loot is a setting's business, not the core's.
    """

    def _facet(self, **kw):
        return FacetFile(id=kw.pop("id", "extra"), name="Extra",
                         version="0.0.1", **kw)

    def test_the_core_ships_no_items(self, ruleset):
        assert ruleset.items == []

    def test_a_module_adds_items(self):
        merged = MergedRuleset([self._facet(items=[
            {"id": "steady_light", "name": "Steady Light", "kind": "consumable",
             "scope": "minor", "effect": "Sheds steady light for a scene."},
        ])])
        assert [i.id for i in merged.items] == ["steady_light"]
        assert merged.get_item("steady_light").name == "Steady Light"

    def test_a_collision_replaces_by_id(self):
        a = self._facet(id="a", items=[
            {"id": "warmth", "name": "Warmth", "effect": "first"}])
        b = self._facet(id="b", items=[
            {"id": "warmth", "name": "Warmth", "effect": "second"}])
        merged = MergedRuleset([a, b])
        assert len(merged.items) == 1
        assert merged.get_item("warmth").effect == "second"

    def test_unknown_item_lookup_returns_none(self, ruleset):
        assert ruleset.get_item("nope") is None

    def test_items_are_serialized_to_clients(self, ruleset):
        assert "items" in ruleset.to_client_dict()


class TestMagicDomainsMergeAsCollections:
    """`magic` mixes two kinds of thing: RULES (traditions, domain types,
    the pre-Technique cap, the Spark rules) and CATALOGS (`soul_domains`,
    `mind_domains`). The rules are singleton — one game, one answer. The
    catalogs are collections keyed by `id`, exactly as `skills` and
    `backgrounds` are.

    Before this was fixed, `magic` was replaced wholesale by the last module
    to declare it, so a setting Facet that added one domain silently deleted
    the core's twenty-one, both traditions, and every domain type. Nothing
    failed; the ruleset simply came back empty of magic.
    """

    def _base(self):
        return load_facet_file(
            Path(__file__).resolve().parents[1] / "facets" / "base" / "facet.yaml")

    def _setting(self, **magic):
        return FacetFile(id="setting", name="Setting", version="0.0.1",
                         priority=1, magic=magic)

    def test_a_setting_domain_is_appended_not_substituted(self):
        base = self._base()
        base_ids = {d.id for d in base.magic.soul_domains}
        merged = MergedRuleset([base, self._setting(soul_domains=[{
            "id": "crystal", "name": "Crystal", "type": "focused",
            "tradition": "intuitive", "description": "Soul-crystal.",
            "lineage_gift": True,
        }])])
        merged_ids = {d.id for d in merged.magic.soul_domains}
        assert base_ids < merged_ids
        assert "crystal" in merged_ids

    def test_the_rules_survive_a_setting_that_only_adds_domains(self):
        base = self._base()
        merged = MergedRuleset([base, self._setting(soul_domains=[{
            "id": "crystal", "name": "Crystal", "type": "focused",
            "tradition": "intuitive", "description": "Soul-crystal.",
        }])])
        assert merged.magic.traditions == base.magic.traditions
        assert merged.magic.domain_types == base.magic.domain_types
        assert merged.magic.pre_technique_scope_limit == (
            base.magic.pre_technique_scope_limit)

    def test_mind_domains_survive_a_soul_only_setting(self):
        base = self._base()
        merged = MergedRuleset([base, self._setting(soul_domains=[{
            "id": "crystal", "name": "Crystal", "type": "focused",
            "tradition": "intuitive", "description": "Soul-crystal.",
        }])])
        assert {d.id for d in merged.magic.mind_domains} == {
            d.id for d in base.magic.mind_domains}

    def test_a_domain_collision_replaces_by_id(self):
        base = self._base()
        original = next(d for d in base.magic.soul_domains if d.id == "fire")
        merged = MergedRuleset([base, self._setting(soul_domains=[{
            "id": "fire", "name": "Fire", "type": "standard",
            "tradition": "intuitive", "description": "Rewritten by the setting.",
        }])])
        fire = next(d for d in merged.magic.soul_domains if d.id == "fire")
        assert fire.type == "standard"
        assert fire.description != original.description

    def test_a_setting_may_still_replace_the_rules(self):
        """A setting that genuinely wants a different magic *rule* is allowed
        to say so — that is what a singleton section is for."""
        base = self._base()
        merged = MergedRuleset([base, self._setting(
            pre_technique_scope_limit="significant")])
        assert merged.magic.pre_technique_scope_limit == "significant"

    def test_base_alone_is_unchanged(self, ruleset):
        """The regression guard: loading only `base` must give exactly what it
        gave before any of this existed."""
        assert len(ruleset.magic.soul_domains) == 12
        assert len(ruleset.magic.mind_domains) == 9
