"""Tests for the Encounter model — TR budget, action economy, serialization."""
import json
import pytest

from app.game.encounter import Encounter, EncounterEnemy, compute_band


# ---------------------------------------------------------------------------
# Construction and defaults
# ---------------------------------------------------------------------------

class TestEncounterDefaults:
    def test_defaults(self):
        e = Encounter(id="test", name="Test Encounter")
        assert e.difficulty == "standard"
        assert e.enemies == []
        assert e.rewards_sparks == 0

    def test_with_enemies(self):
        e = Encounter(id="ambush", name="Ambush", enemies=[
            EncounterEnemy(enemy_id="thug", count=4),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        assert len(e.enemies) == 2
        assert e.total_enemy_count() == 5


# ---------------------------------------------------------------------------
# Difficulty multiplier
# ---------------------------------------------------------------------------

class TestDifficultyMultiplier:
    @pytest.mark.parametrize("diff,mult", [
        ("skirmish", 1.0),
        ("standard", 2.0),
        ("hard", 3.0),
        ("deadly", 4.0),
    ])
    def test_multipliers(self, diff, mult):
        assert Encounter.difficulty_multiplier(diff) == mult

    def test_unknown_difficulty_defaults_standard(self):
        assert Encounter.difficulty_multiplier("legendary") == 2.0


# ---------------------------------------------------------------------------
# Action economy multiplier
# ---------------------------------------------------------------------------

class TestActionEconomy:
    def test_solo(self):
        assert Encounter.action_economy_multiplier(1) == 0.75

    def test_small_group(self):
        assert Encounter.action_economy_multiplier(3) == 1.0

    def test_medium_group(self):
        assert Encounter.action_economy_multiplier(5) == 1.25

    def test_medium_group_mooks(self):
        assert Encounter.action_economy_multiplier(5, all_mooks=True) == 1.1

    def test_large_group(self):
        assert Encounter.action_economy_multiplier(8) == 1.5


# ---------------------------------------------------------------------------
# Budget calculation
# ---------------------------------------------------------------------------

class TestBudgetCalculation:
    def test_standard_budget(self):
        # 3 career advances * 2.0 = 6.0
        assert Encounter.calculate_budget(3, "standard") == 6.0

    def test_hard_budget(self):
        assert Encounter.calculate_budget(5, "hard") == 15.0

    def test_skirmish_budget(self):
        assert Encounter.calculate_budget(10, "skirmish") == 10.0


# ---------------------------------------------------------------------------
# Effective TR calculation
# ---------------------------------------------------------------------------

class TestEffectiveTR:
    def test_solo_named_enemy(self):
        e = Encounter(id="duel", name="Duel", enemies=[
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"sergeant": 8}
        # Solo: 8 * 0.75 = 6.0
        assert e.calculate_effective_tr(trs) == 6.0

    def test_group_of_mooks(self):
        e = Encounter(id="brawl", name="Brawl", enemies=[
            EncounterEnemy(enemy_id="thug", count=5),
        ])
        trs = {"thug": 1}
        # 5 mooks, all_mooks=True, medium group → 5 * 1.1 = 5.5
        assert e.calculate_effective_tr(trs) == 5.5

    def test_mixed_group(self):
        e = Encounter(id="ambush", name="Ambush", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"thug": 1, "sergeant": 8}
        # 4 enemies, not all mooks → raw = 3 + 8 = 11, * 1.25 = 13.75
        assert e.calculate_effective_tr(trs) == 13.75

    def test_unknown_enemy_id_treated_as_zero_tr(self):
        e = Encounter(id="mystery", name="Mystery", enemies=[
            EncounterEnemy(enemy_id="unknown_creature", count=2),
        ])
        assert e.calculate_effective_tr({}) == 0.0


# ---------------------------------------------------------------------------
# Tier-weighted effective TR (new simulation-calibrated formula)
# ---------------------------------------------------------------------------

class TestTierWeightedTR:
    def test_mook_weight_halves_tr(self):
        e = Encounter(id="mooks", name="Mooks", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
        ])
        trs = {"thug": 1}
        tiers = {"thug": "mook"}
        # 3 mooks × TR 1 × 0.5 weight × 1.0 group mod = 1.5
        assert e.calculate_effective_tr(trs, tiers) == 1.5

    def test_named_weight_is_one(self):
        e = Encounter(id="duel", name="Duel", enemies=[
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"sergeant": 8}
        tiers = {"sergeant": "named"}
        # 1 named × TR 8 × 1.0 weight × 1.0 group mod = 8.0
        assert e.calculate_effective_tr(trs, tiers) == 8.0

    def test_boss_weight_increases_tr(self):
        e = Encounter(id="boss", name="Boss Fight", enemies=[
            EncounterEnemy(enemy_id="guardian", count=1),
        ])
        trs = {"guardian": 16}
        tiers = {"guardian": "boss"}
        # 1 boss × TR 16 × 1.25 weight × 1.0 group mod = 20.0
        assert e.calculate_effective_tr(trs, tiers) == 20.0

    def test_mixed_group_with_tiers(self):
        e = Encounter(id="mixed", name="Mixed", enemies=[
            EncounterEnemy(enemy_id="thug", count=3),
            EncounterEnemy(enemy_id="sergeant", count=1),
        ])
        trs = {"thug": 1, "sergeant": 8}
        tiers = {"thug": "mook", "sergeant": "named"}
        # (3×1×0.5 + 1×8×1.0) × 1.1 (4 enemies) = 9.5 × 1.1 = 10.45
        assert e.calculate_effective_tr(trs, tiers) == pytest.approx(10.45)

    def test_large_group_modifier(self):
        e = Encounter(id="swarm", name="Swarm", enemies=[
            EncounterEnemy(enemy_id="thug", count=10),
        ])
        trs = {"thug": 1}
        tiers = {"thug": "mook"}
        # 10 mooks × 1 × 0.5 × 1.2 (7+ enemies) = 6.0
        assert e.calculate_effective_tr(trs, tiers) == 6.0

    def test_boss_plus_mooks(self):
        e = Encounter(id="boss-adds", name="Boss + Adds", enemies=[
            EncounterEnemy(enemy_id="boss", count=1),
            EncounterEnemy(enemy_id="minion", count=4),
        ])
        trs = {"boss": 12, "minion": 1}
        tiers = {"boss": "boss", "minion": "mook"}
        # (1×12×1.25 + 4×1×0.5) × 1.1 (5 enemies) = 17.0 × 1.1 = 18.7
        assert e.calculate_effective_tr(trs, tiers) == pytest.approx(18.7)

    def test_fallback_without_tiers_uses_legacy(self):
        """Without tier info, falls back to the legacy action economy path."""
        e = Encounter(id="legacy", name="Legacy", enemies=[
            EncounterEnemy(enemy_id="thug", count=5),
        ])
        trs = {"thug": 1}
        # Legacy: 5 × 1 × 1.1 (mook-only medium group) = 5.5
        assert e.calculate_effective_tr(trs) == 5.5


class TestFormulaIsRoughHeuristicNotPredictor:
    """The TR-budget formula is a demoted rough ordering check (task A10 /
    DESIGN §5-ter), not a difficulty predictor.

    These tests assert the *documented* behavior of the demoted formula: it
    preserves a few loose ordering intuitions (more of the same enemy is not
    cheaper; a Boss outweighs a Named of equal TR; a solo enemy is discounted)
    while being explicitly non-predictive for multi-Named/Boss rosters — a
    property we pin with a known-mis-ranking test so nobody "fixes" the
    constants into false precision. The calibrated difficulty numbers live in
    the simulator (`test_combat_sim.py::TestRecipeCalibration`), not here.
    """

    def test_more_of_the_same_enemy_never_scores_lower(self):
        """Rough monotonicity: adding identical enemies does not reduce TR."""
        trs = {"named": 8}
        tiers = {"named": "named"}
        prev = -1.0
        for count in range(1, 8):
            e = Encounter(id="e", name="E", enemies=[
                EncounterEnemy(enemy_id="named", count=count),
            ])
            eff = e.calculate_effective_tr(trs, tiers)
            assert eff >= prev
            prev = eff

    def test_boss_outweighs_named_of_equal_tr(self):
        """Tier ordering: boss weight > named weight > mook weight at equal TR."""
        trs = {"x": 10}
        base = Encounter(id="e", name="E", enemies=[EncounterEnemy(enemy_id="x", count=1)])
        boss = base.calculate_effective_tr(trs, {"x": "boss"})
        named = base.calculate_effective_tr(trs, {"x": "named"})
        mook = base.calculate_effective_tr(trs, {"x": "mook"})
        assert boss > named > mook

    def test_solo_enemy_is_discounted_in_legacy_path(self):
        """The legacy (no-tier) path discounts a solo enemy below its raw TR —
        a rough nod to 'the party concentrates fire on one target'."""
        e = Encounter(id="e", name="E", enemies=[EncounterEnemy(enemy_id="x", count=1)])
        assert e.calculate_effective_tr({"x": 8}) < 8

    def test_formula_mis_ranks_the_actor_count_cliff(self):
        """DOCUMENTED LIMITATION — do not "fix" this.

        Simulation (Series 9) measured 2 Bosses (TR 17) at ~83% party win
        (nearly trivial) and 4 Named (TR 8) at ~20% (Deadly). The weighted-sum
        formula ranks them the *opposite* way — it scores the two Bosses higher
        (i.e. flags them as harder) than the four Named. This inversion is
        inherent to any linear weighted-TR-sum and is exactly why the formula
        is non-predictive for multi-Named/Boss rosters and why the Recipe Table
        supersedes it. This test pins the inversion so that a future attempt to
        retune the constants toward the four listed recipes — which would
        reintroduce the false-precision trap A10 escalated — trips a test and a
        reviewer instead of shipping silently.
        """
        two_bosses = Encounter(id="b", name="2 Boss", enemies=[
            EncounterEnemy(enemy_id="boss", count=2),
        ]).calculate_effective_tr({"boss": 17}, {"boss": "boss"})
        four_named = Encounter(id="n", name="4 Named", enemies=[
            EncounterEnemy(enemy_id="named", count=4),
        ]).calculate_effective_tr({"named": 8}, {"named": "named"})

        # Formula's ranking (backwards vs. the simulator's measured difficulty).
        assert two_bosses == pytest.approx(42.5)
        assert four_named == pytest.approx(35.2)
        assert two_bosses > four_named  # the mis-ranking, pinned deliberately


class TestGroupSizeModifier:
    def test_small(self):
        assert Encounter.group_size_modifier(1) == 1.0
        assert Encounter.group_size_modifier(3) == 1.0

    def test_medium(self):
        assert Encounter.group_size_modifier(4) == 1.1
        assert Encounter.group_size_modifier(6) == 1.1

    def test_large(self):
        assert Encounter.group_size_modifier(7) == 1.2
        assert Encounter.group_size_modifier(15) == 1.2


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

class TestEncounterSerialization:
    def test_to_fof_roundtrip(self):
        e = Encounter(
            id="archive-fight", name="Archive Battle",
            difficulty="hard", environment="Cramped stone basement",
            description="The guardian attacks.",
            enemies=[
                EncounterEnemy(enemy_id="guardian", count=1),
                EncounterEnemy(enemy_id="construct", count=3),
            ],
            lateral_solutions=["Disable sensory matrix", "Exploit shoulder weakness"],
            rewards_sparks=1,
            rewards_narrative="Access to restricted archive",
            notes="Designed above budget.",
        )
        fof = e.to_fof()
        loaded = Encounter.from_fof(fof)
        assert loaded.id == "archive-fight"
        assert loaded.difficulty == "hard"
        assert len(loaded.enemies) == 2
        assert loaded.enemies[0].enemy_id == "guardian"
        assert loaded.enemies[1].count == 3
        assert loaded.lateral_solutions == ["Disable sensory matrix", "Exploit shoulder weakness"]
        assert loaded.rewards_sparks == 1
        assert loaded.notes == "Designed above budget."

    def test_from_fof_wrong_type_raises(self):
        with pytest.raises(ValueError, match="Expected type 'encounter'"):
            Encounter.from_fof({"type": "character"})

    def test_from_fof_missing_encounter_block_raises(self):
        with pytest.raises(ValueError, match="Missing or invalid 'encounter'"):
            Encounter.from_fof({"type": "encounter"})

    def test_to_client_dict_is_json_safe(self):
        e = Encounter(id="test", name="Test")
        json.dumps(e.to_client_dict())

    def test_fof_includes_type(self):
        e = Encounter(id="test", name="Test")
        assert e.to_fof()["type"] == "encounter"


# ---------------------------------------------------------------------------
# compute_band (T6.1, K-3) — Recipe-Table difficulty band from actor counts
# ---------------------------------------------------------------------------

class TestComputeBandPS3CalibratedRows:
    """Every expectation here is keyed to a published simulation row:
    MM1 Table MM1-5 (Series 9 Part D, seeds 1/2/3) or the MM1 'Sizing an
    Encounter' prose it summarizes. No invented numbers."""

    def test_mook_only_is_skirmish(self):
        # MM1-5 Skirmish row: 3-7 Mooks, sim 100%/100%/100%.
        result = compute_band(["mook"] * 5, party_strength=3)
        assert result["band"] == "skirmish"
        assert result["calibrated"] is True

    def test_three_named_one_mook_is_standard(self):
        # MM1-5 Standard row: 3 Named + 1 Mook, sim 76%/74.5%/80%.
        result = compute_band(["named"] * 3 + ["mook"], party_strength=3)
        assert result["band"] == "standard"
        assert result["calibrated"] is True

    def test_three_named_two_mooks_is_hard(self):
        # MM1-5 Hard row: 3 Named + 2 Mooks, sim 47.5%/48%/47%.
        result = compute_band(["named"] * 3 + ["mook"] * 2, party_strength=3)
        assert result["band"] == "hard"
        assert result["calibrated"] is True

    def test_three_named_three_mooks_is_deadly(self):
        # MM1-5 Deadly row (first composition): 3 Named + 3 Mooks, sim 20%/20%/22.5%.
        result = compute_band(["named"] * 3 + ["mook"] * 3, party_strength=3)
        assert result["band"] == "deadly"
        assert result["calibrated"] is True

    def test_four_named_one_mook_is_deadly(self):
        # MM1-5 Deadly row (second composition): 4 Named + 1 Mook, sim 20%/16.5%/21%.
        result = compute_band(["named"] * 4 + ["mook"], party_strength=3)
        assert result["band"] == "deadly"
        assert result["calibrated"] is True

    def test_one_mook_is_one_band(self):
        # MM1 Five-Minute Method: "one Mook is one difficulty band (76% -> 47% -> 20%)."
        core = ["named"] * 3
        bands = [
            compute_band(core + ["mook"] * m, party_strength=3)["band_index"]
            for m in (1, 2, 3)
        ]
        assert bands == [1, 2, 3]  # standard -> hard -> deadly, one step per Mook


class TestComputeBandPS3Edges:
    def test_three_named_alone_is_skirmish(self):
        # MM1 Sizing an Encounter: three Named on their own is a near-clean
        # win (~96%) - inside the Skirmish target band (85-100%).
        result = compute_band(["named"] * 3, party_strength=3)
        assert result["band"] == "skirmish"

    def test_four_named_alone_is_hard(self):
        # MM1 Sizing an Encounter: "four Named is a coin-flip (Hard)".
        result = compute_band(["named"] * 4, party_strength=3)
        assert result["band"] == "hard"

    def test_five_named_is_deadly_with_loss_warning(self):
        # MM1 Scaling Notes: "five is a near-certain party loss" - beyond the
        # published Deadly target (15-35%); the band clamps and the note says so.
        result = compute_band(["named"] * 5, party_strength=3)
        assert result["band"] == "deadly"
        assert "near-certain" in result["note"]

    def test_two_named_with_mooks_is_skirmish(self):
        # MM1 Scaling Notes: "one or two Named/Boss enemies is trivial at any
        # TR"; Mooks alone never make it dangerous.
        result = compute_band(["named"] * 2 + ["mook"] * 10, party_strength=3)
        assert result["band"] == "skirmish"

    def test_boss_counts_as_a_named_boss_actor(self):
        # The dial is "the number of Named/Boss enemies acting at once" -
        # a Boss is one actor in that count, same as a Named.
        result = compute_band(["named"] * 2 + ["boss"] + ["mook"], party_strength=3)
        assert result["band"] == "standard"

    def test_thirty_mooks_still_skirmish(self):
        # MM1 Scaling Notes: mean PCs Broken stays at zero through 30 Mooks.
        result = compute_band(["mook"] * 30, party_strength=3)
        assert result["band"] == "skirmish"

    def test_empty_roster_has_no_band(self):
        result = compute_band([], party_strength=3)
        assert result["band"] is None
        assert result["band_index"] is None


class TestComputeBandOutsidePS3:
    """PS-4 rows come from MM1 Table MM1-6, which the book itself flags as
    un-simulated extrapolation ("Do not present them to players as
    calibrated") - the function must carry the same honesty flag."""

    def test_ps4_four_named_is_standard_uncalibrated(self):
        # MM1-6 Standard row: 4 Named.
        result = compute_band(["named"] * 4, party_strength=4)
        assert result["band"] == "standard"
        assert result["calibrated"] is False

    def test_ps4_four_named_one_mook_is_hard_uncalibrated(self):
        # MM1-6 Hard row: 4 Named + 1 Mook.
        result = compute_band(["named"] * 4 + ["mook"], party_strength=4)
        assert result["band"] == "hard"
        assert result["calibrated"] is False

    def test_ps4_five_named_is_deadly_uncalibrated(self):
        # MM1-6 Deadly row: 5 Named.
        result = compute_band(["named"] * 5, party_strength=4)
        assert result["band"] == "deadly"
        assert result["calibrated"] is False

    def test_ps4_mook_only_is_skirmish_uncalibrated(self):
        # MM1-6 Skirmish row: 4-8 Mooks.
        result = compute_band(["mook"] * 6, party_strength=4)
        assert result["band"] == "skirmish"
        assert result["calibrated"] is False

    def test_ps5_extrapolates_and_says_so(self):
        # "Each additional PC shifts the actor-count thresholds up by roughly
        # one Named" (unvalidated beyond PS 3) - the note must admit it.
        result = compute_band(["named"] * 5, party_strength=5)
        assert result["band"] == "standard"
        assert result["calibrated"] is False
        assert "un-simulated" in result["note"]


class TestComputeBandErrors:
    def test_unknown_tier_raises(self):
        with pytest.raises(ValueError, match="tier"):
            compute_band(["named", "dragon"], party_strength=3)

    def test_nonpositive_party_strength_raises(self):
        with pytest.raises(ValueError, match="party_strength"):
            compute_band(["mook"], party_strength=0)

    def test_tier_is_case_insensitive(self):
        result = compute_band(["Named"] * 3 + ["Mook"], party_strength=3)
        assert result["band"] == "standard"
