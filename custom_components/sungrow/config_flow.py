"""Config flow for Sungrow integration."""

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import (
    DOMAIN,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
    CONF_CONNECTION_TYPE,
    CONF_CONNECTION_TYPE_TCP,
    CONF_CONNECTION_TYPE_SERIAL,
)

# possiblly you need to add following code to support localization of the option data schema
# from homeassistant.helpers.selector import localize
# self.hass.helpers.translation.localize("config.step.user_device_type.data.device_type.inverter")


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
                step_id="user_device_type",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_DEVICE_TYPE, default=CONF_DEVICE_TYPE_INVERTER
                        ): vol.In(
                            (CONF_DEVICE_TYPE_INVERTER, CONF_DEVICE_TYPE_WALLBOX)
                        ),
                        vol.Required(
                            CONF_CONNECTION_TYPE, default=CONF_CONNECTION_TYPE_TCP
                        ): vol.In(
                            (CONF_CONNECTION_TYPE_TCP, CONF_CONNECTION_TYPE_SERIAL)
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
