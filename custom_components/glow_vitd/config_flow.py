from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_TARGET_IU, CONF_UV_ENTITY, DEFAULT_TARGET_IU, DOMAIN

class GlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            self._data = user_input
            return await self.async_step_iu()

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    async def async_step_iu(self, user_input=None) -> FlowResult:
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_uv()

        return self.async_show_form(
            step_id="iu",
            data_schema=vol.Schema(
                {vol.Required(CONF_TARGET_IU, default=DEFAULT_TARGET_IU): vol.All(vol.Coerce(int), vol.Range(min=1000, max=4000))}
            ),
        )

    async def async_step_uv(self, user_input=None) -> FlowResult:
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title="Glow: Sun Exposure for Vitamin D", data=self._data)

        return self.async_show_form(
            step_id="uv",
            data_schema=vol.Schema(
                {vol.Optional(CONF_UV_ENTITY): EntitySelector(EntitySelectorConfig(domain="sensor"))}
            ),
        )
