"""The Glow: Sun Exposure for Vitamin D integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    BASELINE_BODY_EXPOSURE,
    BASELINE_MINUTES,
    CONF_BODY_EXPOSURE,
    CONF_TARGET_IU,
    CONF_UV_SENSOR,
    DEFAULT_BODY_EXPOSURE,
    DEFAULT_TARGET_IU,
    DOMAIN,
    MIN_UV_INDEX,
    MONTHLY_UV_DATA,
    SKIN_TYPES,
    STATE_INSUFFICIENT_UVB,
    STATE_SUN_BELOW_HORIZON,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Glow from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = GlowDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


class GlowDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator that centralizes all Glow calculations."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self) -> dict:
        """Calculate all sensor data."""
        sun_is_up = self._is_sun_up()
        uv_sensor_value = self._get_uv_sensor_value()
        monthly_avg = self._get_monthly_average_uv()
        uv_index = uv_sensor_value if uv_sensor_value is not None else monthly_avg
        calculation_method = (
            "Real-time UV sensor"
            if uv_sensor_value is not None
            else "Monthly average for latitude"
        )

        # Check if the configured UV sensor exists but is unavailable
        uv_sensor_entity = self.entry.options.get(CONF_UV_SENSOR)
        if uv_sensor_entity and uv_sensor_value is None:
            state = self.hass.states.get(uv_sensor_entity)
            if state is not None and state.state in ("unknown", "unavailable"):
                calculation_method = "Monthly average (sensor unavailable)"

        target_iu = self.entry.options.get(CONF_TARGET_IU, DEFAULT_TARGET_IU)
        body_exposure = self.entry.options.get(CONF_BODY_EXPOSURE, DEFAULT_BODY_EXPOSURE)
        body_exposure_factor = body_exposure / BASELINE_BODY_EXPOSURE

        # Calculate minutes per skin type
        minutes_per_type: dict[int, float | str] = {}
        for skin_type, info in SKIN_TYPES.items():
            minutes_per_type[skin_type] = self._calculate_minutes(
                sun_is_up, uv_index, target_iu, info["multiplier"], body_exposure_factor,
            )

        return {
            "sun_is_up": sun_is_up,
            "uv_index": round(uv_index, 1),
            "uv_sensor_value": uv_sensor_value,
            "calculation_method": calculation_method,
            "target_iu": target_iu,
            "body_exposure": body_exposure,
            "latitude": self.hass.config.latitude,
            "uv_sensor_entity": uv_sensor_entity,
            "minutes_per_type": minutes_per_type,
        }

    def _calculate_minutes(
        self,
        sun_is_up: bool,
        uv_index: float,
        target_iu: int,
        skin_multiplier: float,
        body_exposure_factor: float,
    ) -> float | str:
        """Calculate required minutes of sun exposure."""
        if not sun_is_up:
            return STATE_SUN_BELOW_HORIZON

        if uv_index < MIN_UV_INDEX:
            return STATE_INSUFFICIENT_UVB

        minutes = (
            BASELINE_MINUTES
            * (target_iu / 2000)
            * skin_multiplier
            * (7 / uv_index)
            / body_exposure_factor
        )
        return round(minutes, 1)

    def _is_sun_up(self) -> bool:
        """Check if sun is above horizon."""
        sun_state = self.hass.states.get("sun.sun")
        if sun_state is None:
            _LOGGER.warning("sun.sun entity not found")
            return False
        return sun_state.state == "above_horizon"

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
        latitude = self.hass.config.latitude
        abs_lat = abs(latitude)

        if abs_lat <= 15:
            lat_range = "0-15"
        elif abs_lat <= 30:
            lat_range = "15-30"
        elif abs_lat <= 45:
            lat_range = "30-45"
        elif abs_lat <= 60:
            lat_range = "45-60"
        elif abs_lat <= 75:
            lat_range = "60-75"
        else:
            lat_range = "75-90"

        month = datetime.now().month - 1

        # Adjust for southern hemisphere (reverse seasons)
        if latitude < 0:
            month = (month + 6) % 12

        return float(MONTHLY_UV_DATA[lat_range][month])
