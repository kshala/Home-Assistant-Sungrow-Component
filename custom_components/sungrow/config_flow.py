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
    CONF_MODBUS_ADDRESS,
    CONF_CONNECTION_TYPE_SERIAL,
    CONF_CONNECTION_TYPE_SERIAL_BAUDRATE,
    CONF_CONNECTION_TYPE_SERIAL_BYTESIZE,
    CONF_CONNECTION_TYPE_SERIAL_METHOD,
    CONF_CONNECTION_TYPE_SERIAL_PARITY,
    CONF_CONNECTION_TYPE_SERIAL_PORT,
    CONF_CONNECTION_TYPE_SERIAL_STOPBITS,
    CONF_CONNECTION_TYPE_TCP,
    CONF_CONNECTION_TYPE_TCP_HOST,
    CONF_CONNECTION_TYPE_TCP_PORT,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
    DEFAULTS,
    DOMAIN,
    OPTIONS
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
            return self.show_form_init()

        device_type = user_input.get(CONF_DEVICE_TYPE)
        connection_type = user_input.get(CONF_CONNECTION_TYPE)

        if connection_type == CONF_CONNECTION_TYPE_TCP:
            tcp_host = user_input.get(CONF_CONNECTION_TYPE_TCP_HOST)
            tcp_port = user_input.get(CONF_CONNECTION_TYPE_TCP_PORT)
            modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

            if tcp_host is None:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Required(CONF_CONNECTION_TYPE_TCP_HOST): str,
                            vol.Required(
                                CONF_CONNECTION_TYPE_TCP_PORT,
                                default=DEFAULTS[CONF_CONNECTION_TYPE_TCP_PORT],
                            ): vol.Coerce(int),
                            vol.Required(
                                CONF_MODBUS_ADDRESS,
                                default=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                                    connection_type
                                ],
                            ): vol.Coerce(int),
                        }
                    ),
                    last_step=True,
                )

        if connection_type == CONF_CONNECTION_TYPE_SERIAL:
            serial_port = user_input.get(CONF_CONNECTION_TYPE_SERIAL_PORT)
            baudrate = user_input.get(CONF_CONNECTION_TYPE_SERIAL_BAUDRATE)
            method = user_input.get(CONF_CONNECTION_TYPE_SERIAL_METHOD)
            bytesize = user_input.get(CONF_CONNECTION_TYPE_SERIAL_BYTESIZE)
            stopbits = user_input.get(CONF_CONNECTION_TYPE_SERIAL_STOPBITS)
            parity = user_input.get(CONF_CONNECTION_TYPE_SERIAL_PARITY)
            modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

            if serial_port is None:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Required(
                                CONF_CONNECTION_TYPE_SERIAL_PORT,
                                default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_PORT],
                            ): vol.Coerce(int),
                            vol.Required(
                                CONF_CONNECTION_TYPE_SERIAL_BAUDRATE,
                                default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_BAUDRATE],
                            ): vol.Coerce(int),
                            vol.Required(
                                CONF_CONNECTION_TYPE_SERIAL_METHOD,
                                default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_METHOD]
                            ): str
                            vol.Required(
                                CONF_MODBUS_ADDRESS,
                                default=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                                    connection_type
                                ],
                            ): vol.Coerce(int),
                        }
                    ),
                    last_step=False,
                )

        return None

    def show_form_init(self):
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=OPTIONS[CONF_DEVICE_TYPE],
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_DEVICE_TYPE,
                            sort=False,
                        )
                    ),
                    vol.Required(CONF_CONNECTION_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=OPTIONS[CONF_CONNECTION_TYPE],
                            mode=SelectSelectorMode.LIST,
                            translation_key=CONF_CONNECTION_TYPE,
                            sort=False,
                        )
                    ),
                }
            ),
            last_step=False,
        )

    #         # validate input is a real IP address
    #         if not self._is_valid_ip(user_input["host"]):
    #             errors["host"] = "invalid_host"
    #         else:
    #             # validate device is already added
    #             for entry in self._async_current_entries():
    #                 if entry.data.get("host") == user_input["host"]:
    #                     errors["host"] = "already_configured"
    #                     break
