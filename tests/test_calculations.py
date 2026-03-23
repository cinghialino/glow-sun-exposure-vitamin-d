"""Tests for the core Glow calculation logic."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.glow_vitd.const import (
    BASELINE_MINUTES,
    MIN_UV_INDEX,
    SKIN_TYPES,
    STATE_INSUFFICIENT_UVB,
    STATE_SUN_BELOW_HORIZON,
)


class TestCalculateMinutes:
    """Test the _calculate_minutes method."""

    def test_baseline_type1_uv7_2000iu(self, coordinator):
        """Baseline: Type 1, UV 7, 2000 IU, 25% exposure = 15 min."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == 15.0

    def test_type2_uv7_2000iu(self, coordinator):
        """Type 2 needs 20% more time than Type 1."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=2000,
            skin_multiplier=1.2, body_exposure_factor=1.0,
        )
        assert result == 18.0

    def test_type6_uv7_2000iu(self, coordinator):
        """Type 6 needs 4x the time of Type 1."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=2000,
            skin_multiplier=4.0, body_exposure_factor=1.0,
        )
        assert result == 60.0

    def test_higher_target_iu(self, coordinator):
        """4000 IU should double the time vs 2000 IU."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=4000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == 30.0

    def test_lower_target_iu(self, coordinator):
        """1000 IU should halve the time vs 2000 IU."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=1000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == 7.5

    def test_higher_uv_reduces_time(self, coordinator):
        """UV 14 (double baseline) should halve the time."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=14.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == 7.5

    def test_lower_uv_increases_time(self, coordinator):
        """UV 3.5 (half baseline) should double the time."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=3.5, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == 30.0

    def test_more_body_exposure_reduces_time(self, coordinator):
        """50% body exposure (2x baseline) should halve the time."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=2.0,
        )
        assert result == 7.5

    def test_less_body_exposure_increases_time(self, coordinator):
        """~12.5% body exposure (0.5x baseline) should double the time."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=7.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=0.5,
        )
        assert result == 30.0

    def test_sun_below_horizon(self, coordinator):
        """Should return state string when sun is down."""
        result = coordinator._calculate_minutes(
            sun_is_up=False, uv_index=7.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == STATE_SUN_BELOW_HORIZON

    def test_insufficient_uvb_at_zero(self, coordinator):
        """UV 0 should return insufficient UVB."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=0.0, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == STATE_INSUFFICIENT_UVB

    def test_insufficient_uvb_below_threshold(self, coordinator):
        """UV just below MIN_UV_INDEX should return insufficient UVB."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=MIN_UV_INDEX - 0.1, target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        assert result == STATE_INSUFFICIENT_UVB

    def test_sufficient_uvb_at_threshold(self, coordinator):
        """UV exactly at MIN_UV_INDEX should calculate normally."""
        result = coordinator._calculate_minutes(
            sun_is_up=True, uv_index=float(MIN_UV_INDEX), target_iu=2000,
            skin_multiplier=1.0, body_exposure_factor=1.0,
        )
        expected = round(BASELINE_MINUTES * (7 / MIN_UV_INDEX), 1)
        assert result == expected

    def test_all_skin_types_produce_increasing_times(self, coordinator):
        """Higher skin types should always need more time."""
        results = []
        for skin_type in range(1, 7):
            multiplier = SKIN_TYPES[skin_type]["multiplier"]
            result = coordinator._calculate_minutes(
                sun_is_up=True, uv_index=7.0, target_iu=2000,
                skin_multiplier=multiplier, body_exposure_factor=1.0,
            )
            results.append(result)

        for i in range(len(results) - 1):
            assert results[i] < results[i + 1], (
                f"Type {i+1} ({results[i]} min) should be less than "
                f"Type {i+2} ({results[i+1]} min)"
            )


class TestIsSunUp:
    """Test the _is_sun_up method."""

    def test_sun_above_horizon(self, coordinator):
        sun_state = MagicMock()
        sun_state.state = "above_horizon"
        coordinator.hass.states.get.return_value = sun_state
        assert coordinator._is_sun_up() is True

    def test_sun_below_horizon(self, coordinator):
        sun_state = MagicMock()
        sun_state.state = "below_horizon"
        coordinator.hass.states.get.return_value = sun_state
        assert coordinator._is_sun_up() is False

    def test_sun_entity_missing(self, coordinator):
        coordinator.hass.states.get.return_value = None
        assert coordinator._is_sun_up() is False


class TestGetUvSensorValue:
    """Test the _get_uv_sensor_value method."""

    def test_no_sensor_configured(self, coordinator):
        coordinator.entry.options = {"target_iu": 2000}
        assert coordinator._get_uv_sensor_value() is None

    def test_sensor_returns_valid_float(self, coordinator):
        coordinator.entry.options = {"uv_sensor": "sensor.uv_index"}
        state = MagicMock()
        state.state = "5.3"
        coordinator.hass.states.get.return_value = state
        assert coordinator._get_uv_sensor_value() == 5.3

    def test_sensor_unavailable(self, coordinator):
        coordinator.entry.options = {"uv_sensor": "sensor.uv_index"}
        state = MagicMock()
        state.state = "unavailable"
        coordinator.hass.states.get.return_value = state
        assert coordinator._get_uv_sensor_value() is None

    def test_sensor_unknown(self, coordinator):
        coordinator.entry.options = {"uv_sensor": "sensor.uv_index"}
        state = MagicMock()
        state.state = "unknown"
        coordinator.hass.states.get.return_value = state
        assert coordinator._get_uv_sensor_value() is None

    def test_sensor_entity_missing(self, coordinator):
        coordinator.entry.options = {"uv_sensor": "sensor.uv_index"}
        coordinator.hass.states.get.return_value = None
        assert coordinator._get_uv_sensor_value() is None

    def test_sensor_non_numeric(self, coordinator):
        coordinator.entry.options = {"uv_sensor": "sensor.uv_index"}
        state = MagicMock()
        state.state = "not_a_number"
        coordinator.hass.states.get.return_value = state
        assert coordinator._get_uv_sensor_value() is None
