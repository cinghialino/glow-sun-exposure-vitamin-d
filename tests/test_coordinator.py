"""Tests for the GlowDataUpdateCoordinator._async_update_data output."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
from datetime import datetime

import pytest
import pytest_asyncio

from custom_components.glow_vitd.const import (
    SKIN_TYPES,
    STATE_INSUFFICIENT_UVB,
    STATE_SUN_BELOW_HORIZON,
)


@pytest.mark.asyncio
class TestAsyncUpdateData:
    """Test the full coordinator update cycle."""

    @pytest.fixture(autouse=True)
    def patch_datetime(self):
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            yield mock_dt

    async def test_returns_all_keys(self, coordinator):
        data = await coordinator._async_update_data()
        expected_keys = {
            "sun_is_up", "uv_index", "uv_sensor_value",
            "calculation_method", "target_iu", "body_exposure",
            "latitude", "uv_sensor_entity", "minutes_per_type",
        }
        assert set(data.keys()) == expected_keys

    async def test_minutes_per_type_has_all_skin_types(self, coordinator):
        data = await coordinator._async_update_data()
        assert set(data["minutes_per_type"].keys()) == set(range(1, 7))

    async def test_sun_up_with_uv_sensor(self, coordinator):
        """With sun up and a UV sensor, should use real-time values."""
        coordinator.entry.options["uv_sensor"] = "sensor.uv_index"
        uv_state = MagicMock()
        uv_state.state = "8.0"

        def get_state(entity_id):
            if entity_id == "sun.sun":
                s = MagicMock()
                s.state = "above_horizon"
                return s
            if entity_id == "sensor.uv_index":
                return uv_state
            return None

        coordinator.hass.states.get.side_effect = get_state
        data = await coordinator._async_update_data()

        assert data["sun_is_up"] is True
        assert data["uv_sensor_value"] == 8.0
        assert data["uv_index"] == 8.0
        assert data["calculation_method"] == "Real-time UV sensor"
        # Type 1 at UV 8: 15 * 1.0 * (7/8) = 13.1
        assert data["minutes_per_type"][1] == 13.1

    async def test_sun_up_without_uv_sensor_uses_monthly(self, coordinator):
        """Without a UV sensor, should fall back to monthly average."""
        data = await coordinator._async_update_data()
        assert data["uv_sensor_value"] is None
        assert data["calculation_method"] == "Monthly average for latitude"
        assert isinstance(data["uv_index"], float)

    async def test_sun_down_all_types_below_horizon(self, coordinator):
        """When sun is down, all skin types should report below horizon."""
        sun_state = MagicMock()
        sun_state.state = "below_horizon"
        coordinator.hass.states.get.return_value = sun_state

        data = await coordinator._async_update_data()
        assert data["sun_is_up"] is False
        for skin_type in range(1, 7):
            assert data["minutes_per_type"][skin_type] == STATE_SUN_BELOW_HORIZON

    async def test_low_uv_all_types_insufficient(self, coordinator):
        """When monthly UV is very low, all types should be insufficient."""
        coordinator.hass.config.latitude = 70
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 12, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            data = await coordinator._async_update_data()

        for skin_type in range(1, 7):
            assert data["minutes_per_type"][skin_type] == STATE_INSUFFICIENT_UVB

    async def test_body_exposure_affects_result(self, coordinator):
        """Higher body exposure should reduce required minutes."""
        coordinator.entry.options["body_exposure"] = 25
        data_25 = await coordinator._async_update_data()

        coordinator.entry.options["body_exposure"] = 50
        data_50 = await coordinator._async_update_data()

        min_25 = data_25["minutes_per_type"][1]
        min_50 = data_50["minutes_per_type"][1]

        if isinstance(min_25, str) or isinstance(min_50, str):
            pytest.skip("UV too low for numeric comparison")

        assert min_50 < min_25, "50% exposure should need less time than 25%"

    async def test_target_iu_stored_in_data(self, coordinator):
        coordinator.entry.options["target_iu"] = 3000
        data = await coordinator._async_update_data()
        assert data["target_iu"] == 3000

    async def test_uv_sensor_unavailable_shows_fallback_method(self, coordinator):
        """When UV sensor is configured but unavailable, method should indicate that."""
        coordinator.entry.options["uv_sensor"] = "sensor.uv_index"
        uv_state = MagicMock()
        uv_state.state = "unavailable"

        def get_state(entity_id):
            if entity_id == "sun.sun":
                s = MagicMock()
                s.state = "above_horizon"
                return s
            if entity_id == "sensor.uv_index":
                return uv_state
            return None

        coordinator.hass.states.get.side_effect = get_state
        data = await coordinator._async_update_data()

        assert data["calculation_method"] == "Monthly average (sensor unavailable)"
        assert data["uv_sensor_value"] is None
