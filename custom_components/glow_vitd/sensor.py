import datetime
import math
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import Throttle
from homeassistant.const import STATE_UNKNOWN

from .const import BASE_TIMES, CONF_TARGET_IU, CONF_UV_ENTITY, DEFAULT_TARGET_IU, DOMAIN, SKIN_MULTIPLIERS, UV_CONSTANT

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=30)

class GlowSensor(SensorEntity):
    """Vitamin D sensor for a skin type."""

    def __init__(self, entry: ConfigEntry, skin_type: int):
        self._entry = entry
        self._skin_type = skin_type
        self._attr_name = f"Glow Type {skin_type} Minutes"
        self._attr_native_unit_of_measurement = "min"
        self._attr_icon = "mdi:sun-wireless"
        self._attr_unique_id = f"{DOMAIN}_type_{skin_type}"
        self._target_iu = entry.data.get(CONF_TARGET_IU, DEFAULT_TARGET_IU)
        self._uv_entity = entry.data.get(CONF_UV_ENTITY)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {"recommended_time": "Midday (11 AM - 3 PM local time)"}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        sun_state = self.hass.states.get("sun.sun")
        if sun_state is None or sun_state.attributes.get("elevation", 0) <= 0:
            self._attr_native_value = STATE_UNKNOWN
            return

        lat = self.hass.config.latitude
        month = datetime.datetime.now().month - 1

        # Base time from all-sky table
        lower_lat = math.floor(lat / 10) * 10
        upper_lat = math.ceil(lat / 10) * 10
        if lower_lat == upper_lat:
            base_time = BASE_TIMES.get(lower_lat, [None] * 12)[month]
        else:
            lower_time = BASE_TIMES.get(lower_lat, [None] * 12)[month]
            upper_time = BASE_TIMES.get(upper_lat, [None] * 12)[month]
            if lower_time is None and upper_time is None:
                base_time = None
            elif lower_time is None:
                base_time = upper_time
            elif upper_time is None:
                base_time = lower_time
            else:
                frac = (lat - lower_lat) / (upper_lat - lower_lat)
                base_time = lower_time + frac * (upper_time - lower_time)

        multiplier = SKIN_MULTIPLIERS[self._skin_type]
        dose_mult = self._target_iu / 1000.0

        if self._uv_entity:
            uv_state = self.hass.states.get(self._uv_entity)
            if uv_state and uv_state.state not in (STATE_UNKNOWN, None):
                try:
                    current_uv = float(uv_state.state)
                    if current_uv > 0:
                        exposure_time = (UV_CONSTANT / current_uv) * multiplier * dose_mult
                        self._attr_native_value = round(exposure_time)
                        return
                except ValueError:
                    pass

        # Fallback to table
        if base_time is None:
            self._attr_native_value = "Insufficient UVB"
        else:
            exposure_time = base_time * multiplier * dose_mult
            self._attr_native_value = round(exposure_time)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    entities = [GlowSensor(entry, skin_type) for skin_type in range(1, 7)]
    async_add_entities(entities)
