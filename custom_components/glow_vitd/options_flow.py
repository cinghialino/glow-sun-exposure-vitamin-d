from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_TARGET_IU, CONF_UV_ENTITY, DEFAULT_TARGET_IU

class GlowOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_TARGET_IU, default=self.config_entry.data.get(CONF_TARGET_IU, DEFAULT_TARGET_IU)): vol.All(vol.Coerce(int), vol.Range(min=1000, max=4000)),
                vol.Optional(CONF_UV_ENTITY, default=self.config_entry.data.get(CONF_UV_ENTITY)): EntitySelector(EntitySelectorConfig(domain="sensor")),
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)
