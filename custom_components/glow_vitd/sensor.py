"""Sensor platform for Glow integration."""
from __future__ import annotations

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
    DOMAIN,
    SKIN_TYPES,
    VERSION,
)

_LOGGER = logging.getLogger(__name__)

DOCUMENTATION_URL = "https://github.com/cinghialino/glow-sun-exposure-vitamin-d"


def _device_info(entry: ConfigEntry) -> dict:
    """Return shared device info for all Glow sensors."""
    return {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": "Glow: Sun Exposure for Vitamin D",
        "manufacturer": "Glow",
        "model": "Sun Exposure Calculator",
        "sw_version": VERSION,
        "configuration_url": DOCUMENTATION_URL,
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Glow sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for skin_type in range(1, 7):
        entities.append(GlowMinutesSensor(coordinator, entry, skin_type))
        entities.append(GlowStatusSensor(coordinator, entry, skin_type))

    entities.append(GlowUVIndexSensor(coordinator, entry))
    entities.append(GlowCalculationMethodSensor(coordinator, entry))

    async_add_entities(entities)


class GlowBaseSensor(SensorEntity):
    """Base class for all Glow sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the base sensor."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_device_info = _device_info(entry)

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


class GlowMinutesSensor(GlowBaseSensor):
    """Sensor showing minutes of sun exposure needed per skin type."""

    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:sun-wireless"

    def __init__(self, coordinator, entry: ConfigEntry, skin_type: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self.skin_type = skin_type
        self._attr_unique_id = f"glow_vitamin_d_sun_exposure_type_{skin_type}"
        self._attr_name = f"Type {skin_type}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data:
            return None
        minutes = data["minutes_per_type"].get(self.skin_type)
        if isinstance(minutes, str):
            return None
        return minutes

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        data = self.coordinator.data or {}
        minutes = data.get("minutes_per_type", {}).get(self.skin_type)

        attributes = {
            "skin_type": self.skin_type,
            "skin_type_name": SKIN_TYPES[self.skin_type]["name"],
            "recommended_time": "Midday (11 AM - 3 PM local time)",
            "target_iu": data.get("target_iu"),
            "body_exposure": f"{data.get('body_exposure', 25)}%",
        }

        if isinstance(minutes, str):
            attributes["status"] = minutes
        else:
            attributes["uv_index_used"] = data.get("uv_index")
            attributes["calculation_method"] = data.get("calculation_method")

        return attributes


class GlowStatusSensor(GlowBaseSensor):
    """Sensor showing human-readable exposure status per skin type."""

    _attr_icon = "mdi:information-outline"

    def __init__(self, coordinator, entry: ConfigEntry, skin_type: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self.skin_type = skin_type
        self._attr_unique_id = f"glow_vitamin_d_sun_exposure_type_{skin_type}_status"
        self._attr_name = f"Type {skin_type} Status"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data:
            return None
        minutes = data["minutes_per_type"].get(self.skin_type)
        if isinstance(minutes, str):
            return minutes

        if minutes < 15:
            return "Quick exposure needed"
        elif minutes < 30:
            return "Moderate exposure needed"
        elif minutes < 60:
            return "Extended exposure needed"
        return "Long exposure needed"

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        data = self.coordinator.data or {}
        minutes = data.get("minutes_per_type", {}).get(self.skin_type)

        attributes = {
            "skin_type": self.skin_type,
            "skin_type_name": SKIN_TYPES[self.skin_type]["name"],
        }

        if not isinstance(minutes, str):
            attributes["minutes_needed"] = minutes
            attributes["uv_index"] = data.get("uv_index")

        return attributes


class GlowUVIndexSensor(GlowBaseSensor):
    """Sensor that displays the current UV index being used."""

    _attr_icon = "mdi:weather-sunny"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = "glow_vitamin_d_sun_exposure_uv_index"
        self._attr_name = "UV Index"

    @property
    def native_value(self) -> float | None:
        """Return the UV index."""
        data = self.coordinator.data
        if not data:
            return None
        return data.get("uv_index")

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        data = self.coordinator.data or {}
        uv_sensor_entity = data.get("uv_sensor_entity")

        if uv_sensor_entity and data.get("uv_sensor_value") is not None:
            return {
                "source": "UV sensor",
                "sensor_entity": uv_sensor_entity,
            }

        attributes = {"source": "Monthly average"}
        if uv_sensor_entity:
            attributes["sensor_entity"] = uv_sensor_entity
            attributes["sensor_status"] = "unavailable"
        else:
            attributes["latitude"] = data.get("latitude")

        return attributes


class GlowCalculationMethodSensor(GlowBaseSensor):
    """Sensor that displays the calculation method being used."""

    _attr_icon = "mdi:calculator"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = "glow_vitamin_d_sun_exposure_calculation_method"
        self._attr_name = "Calculation Method"

    @property
    def native_value(self) -> str | None:
        """Return the calculation method."""
        data = self.coordinator.data
        if not data:
            return None
        return data.get("calculation_method")

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        data = self.coordinator.data or {}
        attributes = {
            "target_iu": data.get("target_iu"),
            "body_exposure": f"{data.get('body_exposure', 25)}%",
            "latitude": data.get("latitude"),
        }

        uv_sensor_entity = data.get("uv_sensor_entity")
        if uv_sensor_entity:
            attributes["uv_sensor_entity"] = uv_sensor_entity

        return attributes
