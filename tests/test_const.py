"""Tests for constants and configuration values."""
from __future__ import annotations

from custom_components.glow_vitd.const import (
    BASELINE_BODY_EXPOSURE,
    BASELINE_MINUTES,
    DEFAULT_BODY_EXPOSURE,
    DEFAULT_TARGET_IU,
    MAX_BODY_EXPOSURE,
    MAX_TARGET_IU,
    MIN_BODY_EXPOSURE,
    MIN_TARGET_IU,
    MIN_UV_INDEX,
    SKIN_TYPES,
    VERSION,
)


class TestConstants:
    """Validate constant values and relationships."""

    def test_default_target_iu_in_range(self):
        assert MIN_TARGET_IU <= DEFAULT_TARGET_IU <= MAX_TARGET_IU

    def test_default_body_exposure_in_range(self):
        assert MIN_BODY_EXPOSURE <= DEFAULT_BODY_EXPOSURE <= MAX_BODY_EXPOSURE

    def test_min_uv_index_positive(self):
        assert MIN_UV_INDEX > 0

    def test_baseline_minutes_positive(self):
        assert BASELINE_MINUTES > 0

    def test_baseline_body_exposure_matches_default(self):
        assert BASELINE_BODY_EXPOSURE == DEFAULT_BODY_EXPOSURE

    def test_version_format(self):
        parts = VERSION.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()


class TestSkinTypes:
    """Validate the Fitzpatrick skin type data."""

    def test_six_skin_types(self):
        assert len(SKIN_TYPES) == 6

    def test_types_are_1_through_6(self):
        assert set(SKIN_TYPES.keys()) == {1, 2, 3, 4, 5, 6}

    def test_all_have_name_and_multiplier(self):
        for skin_type, info in SKIN_TYPES.items():
            assert "name" in info, f"Type {skin_type} missing 'name'"
            assert "multiplier" in info, f"Type {skin_type} missing 'multiplier'"

    def test_multipliers_are_increasing(self):
        multipliers = [SKIN_TYPES[i]["multiplier"] for i in range(1, 7)]
        for i in range(len(multipliers) - 1):
            assert multipliers[i] < multipliers[i + 1]

    def test_type1_multiplier_is_baseline(self):
        assert SKIN_TYPES[1]["multiplier"] == 1.0

    def test_all_multipliers_positive(self):
        for skin_type, info in SKIN_TYPES.items():
            assert info["multiplier"] > 0
