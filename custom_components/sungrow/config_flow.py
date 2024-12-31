"""Config flow for Sungrow integration."""

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_CONNECTION_TYPE,
    CONF_CONNECTION_TYPE_SERIAL,
    CONF_CONNECTION_TYPE_TCP,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
    DOMAIN,
)

# TODO: learn more about https://www.home-assistant.io/docs/blueprint/selectors/


class SungrowConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Modbus Integration."""

    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle step user."""

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_DEVICE_TYPE): SelectSelector(
                            SelectSelectorConfig(
                                options=[
                                    CONF_DEVICE_TYPE_INVERTER,
                                    CONF_DEVICE_TYPE_WALLBOX,
                                ],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key=CONF_DEVICE_TYPE,
                                sort=False,
                            )
                        ),
                        vol.Required(CONF_CONNECTION_TYPE): SelectSelector(
                            SelectSelectorConfig(
                                options=[
                                    CONF_CONNECTION_TYPE_TCP,
                                    CONF_CONNECTION_TYPE_SERIAL,
                                ],
                                mode=SelectSelectorMode.LIST,
                                translation_key=CONF_CONNECTION_TYPE,
                                sort=False,
                            )
                        ),
                    }
                ),
                last_step=False,
            )

        # device_type = user_input.get("device_type")
        connection_type = user_input.get("connection_type")

        if connection_type == "TCP":
            return self.async_show_form(
                step_id="user_inverter",
                data_schema=vol.Schema(
                    {
                        vol.Required("host"): str,
                        vol.Optional("port", default=502): vol.Coerce(int),
                    }
                ),
                last_step=True,
            )

        if user_input["device_type"] == "Wallbox":
            connection_type = user_input.get("connection_type")
            if connection_type is None:
                return self.async_show_form(
                    step_id="user_connection",
                    data_schema=vol.Schema(
                        {
                            vol.Required("connection_type", default="TCP"): vol.In(
                                ("TCP", "Serial")
                            ),
                        }
                    ),
                    last_step=False,
                )

        return None

    #         # validate input is a real IP address
    #         if not self._is_valid_ip(user_input["host"]):
    #             errors["host"] = "invalid_host"
    #         else:
    #             # validate device is already added
    #             for entry in self._async_current_entries():
    #                 if entry.data.get("host") == user_input["host"]:
    #                     errors["host"] = "already_configured"
    #                     break
