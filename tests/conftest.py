"""Shared test fixtures for Glow integration tests."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = MagicMock()
    hass.config.latitude = 41.9  # Rome
    hass.config.longitude = 12.5

    # Default: sun is up
    sun_state = MagicMock()
    sun_state.state = "above_horizon"
    hass.states.get.return_value = sun_state

    return hass


@pytest.fixture
def mock_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {
        "target_iu": 2000,
        "body_exposure": 25,
    }
    return entry


@pytest.fixture
def coordinator(mock_hass, mock_entry):
    """Create a GlowDataUpdateCoordinator for testing."""
    from custom_components.glow_vitd import GlowDataUpdateCoordinator

    coord = GlowDataUpdateCoordinator.__new__(GlowDataUpdateCoordinator)
    coord.hass = mock_hass
    coord.entry = mock_entry
    coord.logger = MagicMock()
    coord.name = "glow_vitd"
    coord.data = {}
    return coord
