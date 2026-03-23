"""Tests for monthly UV average lookup and latitude handling."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
from datetime import datetime

import pytest

from custom_components.glow_vitd.const import MONTHLY_UV_DATA


class TestGetMonthlyAverageUv:
    """Test the _get_monthly_average_uv method."""

    def _set_latitude(self, coordinator, lat):
        coordinator.hass.config.latitude = lat

    @pytest.mark.parametrize("latitude,expected_range", [
        (0, "0-15"),
        (10, "0-15"),
        (15, "0-15"),
        (20, "15-30"),
        (30, "15-30"),
        (35, "30-45"),
        (45, "30-45"),
        (50, "45-60"),
        (60, "45-60"),
        (65, "60-75"),
        (75, "60-75"),
        (80, "75-90"),
        (90, "75-90"),
    ])
    def test_latitude_ranges(self, coordinator, latitude, expected_range):
        """Each latitude should map to the correct UV data range."""
        self._set_latitude(coordinator, latitude)
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        # July (index 6) value for the expected range
        assert result == float(MONTHLY_UV_DATA[expected_range][6])

    def test_southern_hemisphere_season_offset(self, coordinator):
        """Southern hemisphere should offset by 6 months."""
        # January in southern hemisphere = July UV data
        self._set_latitude(coordinator, -35)  # maps to 30-45
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 1, 15)  # January
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        # January with -6 offset = July (index 6)
        assert result == float(MONTHLY_UV_DATA["30-45"][6])

    def test_negative_latitude_uses_abs_for_range(self, coordinator):
        """Negative latitude should use absolute value for range lookup."""
        self._set_latitude(coordinator, -10)  # abs = 10, range 0-15
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 7, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        # July with 6-month offset = January (index 0) for 0-15
        assert result == float(MONTHLY_UV_DATA["0-15"][0])

    def test_arctic_latitude_returns_data(self, coordinator):
        """Latitudes > 75 should return data from 75-90 range."""
        self._set_latitude(coordinator, 85)
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 6, 15)  # June
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        assert result == float(MONTHLY_UV_DATA["75-90"][5])

    def test_extreme_latitude_90(self, coordinator):
        """Latitude 90 (North Pole) should not raise."""
        self._set_latitude(coordinator, 90)
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 6, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        assert isinstance(result, float)

    def test_equator_high_uv_year_round(self, coordinator):
        """Equator should have high UV values all year."""
        self._set_latitude(coordinator, 0)
        for month in range(1, 13):
            with patch("custom_components.glow_vitd.datetime") as mock_dt:
                mock_dt.now.return_value = datetime(2026, month, 15)
                mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
                result = coordinator._get_monthly_average_uv()
            assert result >= 9.0, f"Equator UV in month {month} should be >= 9, got {result}"

    def test_arctic_winter_zero_uv(self, coordinator):
        """Arctic winter months should have zero UV."""
        self._set_latitude(coordinator, 70)
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 12, 15)  # December
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        assert result == 0.0

    def test_returns_float(self, coordinator):
        """Should always return a float, even if table has int."""
        self._set_latitude(coordinator, 45)
        with patch("custom_components.glow_vitd.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 1, 15)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = coordinator._get_monthly_average_uv()
        assert isinstance(result, float)


class TestMonthlyUvDataIntegrity:
    """Test the MONTHLY_UV_DATA table itself."""

    def test_all_ranges_have_12_months(self):
        for lat_range, values in MONTHLY_UV_DATA.items():
            assert len(values) == 12, f"{lat_range} has {len(values)} months, expected 12"

    def test_all_values_non_negative(self):
        for lat_range, values in MONTHLY_UV_DATA.items():
            for i, v in enumerate(values):
                assert v >= 0, f"{lat_range} month {i+1} has negative UV: {v}"

    def test_expected_ranges_exist(self):
        expected = ["0-15", "15-30", "30-45", "45-60", "60-75", "75-90"]
        assert list(MONTHLY_UV_DATA.keys()) == expected

    def test_tropical_higher_than_arctic(self):
        """Tropical UV should always be >= Arctic UV for same month."""
        for month in range(12):
            tropical = MONTHLY_UV_DATA["0-15"][month]
            arctic = MONTHLY_UV_DATA["75-90"][month]
            assert tropical >= arctic, (
                f"Month {month+1}: tropical ({tropical}) < arctic ({arctic})"
            )
