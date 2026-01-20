"""Config flow for Glow integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
import voluptuous as vol

from .const import (
    CONF_TARGET_IU,
    CONF_UV_SENSOR,
    DEFAULT_TARGET_IU,
    DOMAIN,
    MAX_TARGET_IU,
    MIN_TARGET_IU,
)

_LOGGER = logging.getLogger(__name__)


class GlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Glow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Check if already configured
            await self.async_set_unique_id("glow_vitd_integration")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Glow: Sun Exposure for Vitamin D",
                data={},
                options=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_TARGET_IU, default=DEFAULT_TARGET_IU
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_TARGET_IU, max=MAX_TARGET_IU)),
                vol.Optional(CONF_UV_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "min_iu": str(MIN_TARGET_IU),
                "max_iu": str(MAX_TARGET_IU),
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GlowOptionsFlowHandler:
        """Get the options flow for this handler."""
        return GlowOptionsFlowHandler()


class GlowOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Glow options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_TARGET_IU,
                    default=options.get(CONF_TARGET_IU, DEFAULT_TARGET_IU),
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_TARGET_IU, max=MAX_TARGET_IU)),
                vol.Optional(
                    CONF_UV_SENSOR,
                    default=options.get(CONF_UV_SENSOR),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
