"""Sensor platform for Glow integration."""
from __future__ import annotations

from datetime import datetime
import logging
import math

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.sun import get_astral_location
from homeassistant.util import dt as dt_util

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
    
    # Create one sensor for each skin type
    entities = []
    for skin_type in range(1, 7):
        entities.append(
            GlowSensor(
                coordinator,
                entry,
                skin_type,
            )
        )
    
    async_add_entities(entities)


class GlowSensor(SensorEntity):
    """Representation of a Glow sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:sun-wireless"

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        skin_type: int,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.entry = entry
        self.skin_type = skin_type
        self._attr_unique_id = f"{entry.entry_id}_type_{skin_type}"
        self._attr_name = f"Type {skin_type} minutes"
        
        # Device info for grouping
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Glow: Sun Exposure for Vitamin D",
            "manufacturer": "Glow",
            "model": "Sun Exposure Calculator",
            "sw_version": "1.0.0",
        }

    @property
    def native_value(self) -> float | str | None:
        """Return the state of the sensor."""
        try:
            minutes = self._calculate_minutes()
            if isinstance(minutes, str):
                return None  # Return None for special states
            return round(minutes, 1)
        except Exception as err:
            _LOGGER.error("Error calculating minutes: %s", err)
            return None

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        attributes = {
            "skin_type": self.skin_type,
            "skin_type_name": SKIN_TYPES[self.skin_type]["name"],
            "recommended_time": "Midday (11 AM - 3 PM local time)",
            "target_iu": self.entry.options.get(CONF_TARGET_IU, DEFAULT_TARGET_IU),
            "body_exposure": "25% (face, arms, legs)",
        }
        
        # Add calculation details
        try:
            minutes = self._calculate_minutes()
            if isinstance(minutes, str):
                attributes["status"] = minutes
            else:
                uv_index = self._get_uv_index()
                attributes["uv_index_used"] = round(uv_index, 1)
                attributes["calculation_method"] = (
                    "real-time UV sensor" if self._get_uv_sensor_value() is not None 
                    else "monthly average for latitude"
                )
        except Exception as err:
            _LOGGER.debug("Could not add calculation details: %s", err)
        
        return attributes

    def _calculate_minutes(self) -> float | str:
        """Calculate required minutes of sun exposure."""
        # Check if sun is above horizon
        if not self._is_sun_up():
            return STATE_SUN_BELOW_HORIZON
        
        # Get UV index
        uv_index = self._get_uv_index()
        
        # Check if UV is sufficient
        if uv_index < 3:
            return STATE_INSUFFICIENT_UVB
        
        # Get target IU
        target_iu = self.entry.options.get(CONF_TARGET_IU, DEFAULT_TARGET_IU)
        
        # Get skin multiplier
        skin_multiplier = SKIN_TYPES[self.skin_type]["multiplier"]
        
        # Calculate minutes
        # Formula: baseline_minutes * (target_iu / 2000) * skin_multiplier * (7 / uv_index)
        # Baseline: 15 minutes for Type 1 skin at UV 7 produces 2000 IU
        minutes = (
            BASELINE_MINUTES 
            * (target_iu / 2000) 
            * skin_multiplier 
            * (7 / uv_index)
        )
        
        return minutes

    def _is_sun_up(self) -> bool:
        """Check if sun is above horizon."""
        try:
            location = get_astral_location(self.hass)
            now = dt_util.now()
            sun = location.sun(now, local=True)
            
            # Check if current time is between sunrise and sunset
            return sun["sunrise"] <= now <= sun["sunset"]
        except Exception as err:
            _LOGGER.error("Error checking sun position: %s", err)
            return False

    def _get_uv_index(self) -> float:
        """Get current UV index."""
        # First try to get from sensor
        sensor_value = self._get_uv_sensor_value()
        if sensor_value is not None:
            return sensor_value
        
        # Otherwise use monthly average based on latitude
        return self._get_monthly_average_uv()

    def _get_uv_sensor_value(self) -> float | None:
        """Get UV index from configured sensor."""
        uv_sensor = self.entry.options.get(CONF_UV_SENSOR)
        if not uv_sensor:
            return None
        
        state = self.hass.states.get(uv_sensor)
        if state is None or state.state in ("unknown", "unavailable"):
            return None
        
        try:
            return float(state.state)
        except (ValueError, TypeError):
            _LOGGER.warning("Could not parse UV sensor value: %s", state.state)
            return None

    def _get_monthly_average_uv(self) -> float:
        """Get monthly average UV index based on latitude."""
        # Get latitude
        latitude = self.hass.config.latitude
        abs_lat = abs(latitude)
        
        # Determine latitude range
        if abs_lat <= 15:
            lat_range = "0-15"
        elif abs_lat <= 30:
            lat_range = "15-30"
        elif abs_lat <= 45:
            lat_range = "30-45"
        elif abs_lat <= 60:
            lat_range = "45-60"
        else:
            lat_range = "60-75"
        
        # Get current month (0-11)
        month = datetime.now().month - 1
        
        # Adjust for southern hemisphere (reverse seasons)
        if latitude < 0:
            month = (month + 6) % 12
        
        # Get UV index from lookup table
        uv_index = MONTHLY_UV_DATA[lat_range][month]
        
        return float(uv_index)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )
