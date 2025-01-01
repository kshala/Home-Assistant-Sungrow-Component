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
    CONF_CONNECTION_TYPE_SERIAL_BAUDRATE,
    CONF_CONNECTION_TYPE_SERIAL_BYTESIZE,
    CONF_CONNECTION_TYPE_SERIAL_METHOD,
    CONF_CONNECTION_TYPE_SERIAL_PARITY,
    CONF_CONNECTION_TYPE_SERIAL_PORT,
    CONF_CONNECTION_TYPE_SERIAL_STOPBITS,
    CONF_CONNECTION_TYPE_TCP,
    CONF_CONNECTION_TYPE_TCP_HOST,
    CONF_CONNECTION_TYPE_TCP_PORT,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
    CONF_MODBUS_ADDRESS,
    DEFAULTS,
    DOMAIN,
    OPTIONS,
)


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

        device_name = user_input.get(CONF_DEVICE_NAME)
        device_type = user_input.get(CONF_DEVICE_TYPE)
        connection_type = user_input.get(CONF_CONNECTION_TYPE)

        if connection_type == CONF_CONNECTION_TYPE_TCP:
            return self.handle_connection_type_tcp(user_input, device_name, device_type)

        if connection_type == CONF_CONNECTION_TYPE_SERIAL:
            return self.handle_connection_type_serial(
                user_input, device_name, device_type
            )

        return None

    def show_form_init(self) -> ConfigFlowResult:
        """Show the initial form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_NAME): str,
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
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_CONNECTION_TYPE,
                            sort=False,
                        )
                    ),
                }
            ),
            last_step=False,
        )

    def handle_connection_type_tcp(
        self, user_input: dict[str, Any], device_name: str, device_type: str
    ) -> ConfigFlowResult:
        """Handle connection type TCP."""
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
                                CONF_CONNECTION_TYPE_TCP
                            ],
                        ): vol.Coerce(int),
                    }
                ),
                last_step=True,
            )

        return None

    def handle_connection_type_serial(
        self, user_input: dict[str, Any], device_name: str, device_type: str
    ) -> ConfigFlowResult:
        """Handle connection type serial."""
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
                            default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_METHOD],
                        ): SelectSelector(
                            SelectSelectorConfig(
                                options=OPTIONS[CONF_CONNECTION_TYPE_SERIAL_METHOD],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key=CONF_CONNECTION_TYPE_SERIAL_METHOD,
                                sort=False,
                            )
                        ),
                        vol.Required(
                            CONF_CONNECTION_TYPE_SERIAL_BYTESIZE,
                            default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_BYTESIZE],
                        ): SelectSelector(
                            SelectSelectorConfig(
                                options=OPTIONS[CONF_CONNECTION_TYPE_SERIAL_BYTESIZE],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key=CONF_CONNECTION_TYPE_SERIAL_BYTESIZE,
                                sort=False,
                            )
                        ),
                        vol.Required(
                            CONF_CONNECTION_TYPE_SERIAL_STOPBITS,
                            default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_STOPBITS],
                        ): SelectSelector(
                            SelectSelectorConfig(
                                options=OPTIONS[CONF_CONNECTION_TYPE_SERIAL_STOPBITS],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key=CONF_CONNECTION_TYPE_SERIAL_STOPBITS,
                                sort=False,
                            )
                        ),
                        vol.Required(
                            CONF_CONNECTION_TYPE_SERIAL_PARITY,
                            default=DEFAULTS[CONF_CONNECTION_TYPE_SERIAL_PARITY],
                        ): SelectSelector(
                            SelectSelectorConfig(
                                options=OPTIONS[CONF_CONNECTION_TYPE_SERIAL_PARITY],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key=CONF_CONNECTION_TYPE_SERIAL_PARITY,
                                sort=False,
                            )
                        ),
                        vol.Required(
                            CONF_MODBUS_ADDRESS,
                            default=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                                CONF_CONNECTION_TYPE_SERIAL
                            ],
                        ): vol.Coerce(int),
                    }
                ),
                last_step=False,
            )

        return None
