"""Sensor platform for Glow integration."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BASELINE_MINUTES,
    CONF_TARGET_IU,
    CONF_UV_SENSOR,
    DEFAULT_TARGET_IU,
    DOMAIN,
    MONTHLY_UV_DATA,
    SKIN_TYPES,
    STATE_INSUFFICIENT_UVB,
    STATE_SUN_BELOW_HORIZON,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Glow sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create sensors for each skin type (minutes + status)
    entities = []
    for skin_type in range(1, 7):
        # Add minutes sensor
        entities.append(
            GlowMinutesSensor(
                coordinator,
                entry,
                skin_type,
            )
        )
        # Add status sensor
        entities.append(
            GlowStatusSensor(
                coordinator,
                entry,
                skin_type,
            )
        )
    
    # Add UV index sensor
    entities.append(GlowUVIndexSensor(coordi
