"""Sensor platform for Glow Vitamin D Sun Exposure."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

SKIN_TYPES = [1, 2, 3, 4, 5, 6]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Glow Vitamin D sensors."""
    
    # Get your coordinator or data from hass.data
    # coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create time sensors for each skin type
    for skin_type in SKIN_TYPES:
        entities.append(GlowVitaminDTimeSensor(config_entry, skin_type))
        entities.append(GlowVitaminDStatusSensor(config_entry, skin_type))
    
    # Add UV Index sensor
    entities.append(GlowVitaminDUVIndexSensor(config_entry))
    
    # Add Calculation Method sensor
    entities.append(GlowVitaminDCalculationMethodSensor(config_entry))
    
    async_add_entities(entities)


class GlowVitaminDBaseSensor(SensorEntity):
    """Base class for Glow Vitamin D sensors."""
    
    _attr_has_entity_name = True
    
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name="Vitamin D Sun Exposure",
            manufacturer="Glow",
            model="Sun Exposure Calculator",
            sw_version="2.0",
        )


class GlowVitaminDTimeSensor(GlowVitaminDBaseSensor):
    """Sensor for sun exposure time for specific skin type."""
    
    def __init__(self, config_entry: ConfigEntry, skin_type: int) -> None:
        """Initialize the time sensor."""
        super().__init__(config_entry)
        self._skin_type = skin_type
        
        self._attr_name = f"Time {skin_type}"
        self._attr_unique_id = f"{config_entry.entry_id}_time_{skin_type}"
        self._attr_icon = "mdi:sun-clock"
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        # TODO: Replace with your actual calculation logic
        # Example: return self.coordinator.data.get(f"time_{self._skin_type}")
        return None


class GlowVitaminDStatusSensor(GlowVitaminDBaseSensor):
    """Status sensor for sun exposure time."""
    
    def __init__(self, config_entry: ConfigEntry, skin_type: int) -> None:
        """Initialize the status sensor."""
        super().__init__(config_entry)
        self._skin_type = skin_type
        
        self._attr_name = f"Time {skin_type} status"
        self._attr_unique_id = f"{config_entry.entry_id}_time_{skin_type}_status"
        self._attr_icon = "mdi:information-outline"
    
    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # TODO: Replace with your actual status logic
        # Example: return self.coordinator.data.get(f"status_{self._skin_type}")
        return None


class GlowVitaminDUVIndexSensor(GlowVitaminDBaseSensor):
    """UV Index sensor."""
    
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize UV index sensor."""
        super().__init__(config_entry)
        
        self._attr_name = "UV index"
        self._attr_unique_id = f"{config_entry.entry_id}_uv_index"
        self._attr_icon = "mdi:weather-sunny-alert"
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> float | None:
        """Return the UV index."""
        # TODO: Replace with your actual UV index retrieval
        # Example: return self.coordinator.data.get("uv_index")
        return None


class GlowVitaminDCalculationMethodSensor(GlowVitaminDBaseSensor):
    """Calculation method sensor."""
    
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize calculation method sensor."""
        super().__init__(config_entry)
        
        self._attr_name = "Calculation method"
        self._attr_unique_id = f"{config_entry.entry_id}_calculation_method"
        self._attr_icon = "mdi:calculator"
    
    @property
    def native_value(self) -> str | None:
        """Return the calculation method."""
        # TODO: Replace with your actual calculation method
        # Example: return self.coordinator.data.get("calculation_method")
        return None
