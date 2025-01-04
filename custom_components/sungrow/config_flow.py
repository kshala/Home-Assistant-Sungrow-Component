"""Config flow for Sungrow integration."""

import logging
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
    CONF_MODBUS_ADDRESS,
    DEFAULTS,
    DOMAIN,
    ENTITIES,
    ENTITY_DEVICE_TYPE_CODE,
    OPTIONS,
)
from .modbus_device import ModbusDevice, ModbusSerialDeviceConfig, ModbusTcpDeviceConfig

_LOGGER = logging.getLogger(__name__)


class SungrowConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Modbus Integration."""

    VERSION = 1
    MINOR_VERSION = 0

    connection_type = None

    tcp_config: ModbusTcpDeviceConfig = None
    serial_config: ModbusSerialDeviceConfig = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle step user."""

        if user_input is None:
            return await self.async_show_form_init()

        if self.connection_type is None:
            self.connection_type = user_input.get(CONF_CONNECTION_TYPE)

        if self.connection_type == CONF_CONNECTION_TYPE_TCP:
            return await self.async_handle_connection_type_tcp(user_input)

        if self.connection_type == CONF_CONNECTION_TYPE_SERIAL:
            return await self.async_handle_connection_type_serial(user_input)

        return None

    async def async_show_form_init(self) -> ConfigFlowResult:
        """Show the initial form."""
        return self.async_show_form(
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

    async def async_handle_connection_type_tcp(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle connection type TCP."""

        if self.tcp_config is None:
            self.tcp_config = ModbusTcpDeviceConfig(
                name=user_input.get(CONF_DEVICE_NAME),
                device_type=user_input.get(CONF_DEVICE_TYPE),
                host=user_input.get(CONF_CONNECTION_TYPE_TCP_HOST),
                port=user_input.get(CONF_CONNECTION_TYPE_TCP_PORT),
                modbus_address=user_input.get(CONF_MODBUS_ADDRESS),
            )

        if self.tcp_config.host is None:
            self.tcp_config.host = user_input.get(CONF_CONNECTION_TYPE_TCP_HOST)

        if self.tcp_config.port is None:
            self.tcp_config.port = user_input.get(CONF_CONNECTION_TYPE_TCP_PORT)

        if self.tcp_config.modbus_address is None:
            self.tcp_config.modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

        errors: dict[str, str] = None

        if self.tcp_config.iscomplete():
            modbus_device: ModbusDevice = ModbusDevice(self.tcp_config)
            errors = await self.async_test_device(modbus_device)

        if self.tcp_config.host is None or errors is not None:
            return self.async_show_form(
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_CONNECTION_TYPE_TCP_HOST): str,
                        vol.Required(
                            CONF_CONNECTION_TYPE_TCP_PORT,
                            default=DEFAULTS[CONF_CONNECTION_TYPE_TCP_PORT],
                        ): vol.Coerce(int),
                        vol.Required(
                            CONF_MODBUS_ADDRESS,
                            default=DEFAULTS[CONF_MODBUS_ADDRESS][
                                self.tcp_config.device_type
                            ][CONF_CONNECTION_TYPE_TCP],
                        ): vol.Coerce(int),
                    }
                ),
                errors=errors,
                last_step=False,
            )

        return None

    async def async_handle_connection_type_serial(
        self, user_input: dict[str, Any], device_name: str, device_type: str
    ) -> ConfigFlowResult:
        """Handle connection type serial."""

        if self.serial_config is None:
            self.serial_config = ModbusSerialDeviceConfig(
                name=user_input.get(CONF_DEVICE_NAME),
                device_type=user_input.get(CONF_DEVICE_TYPE),
                serial_port=user_input.get(CONF_CONNECTION_TYPE_SERIAL_PORT),
                baudrate=user_input.get(CONF_CONNECTION_TYPE_SERIAL_BAUDRATE),
                method=user_input.get(CONF_CONNECTION_TYPE_SERIAL_METHOD),
                bytesize=user_input.get(CONF_CONNECTION_TYPE_SERIAL_BYTESIZE),
                stopbits=user_input.get(CONF_CONNECTION_TYPE_SERIAL_STOPBITS),
                parity=user_input.get(CONF_CONNECTION_TYPE_SERIAL_PARITY),
                modbus_address=user_input.get(CONF_MODBUS_ADDRESS),
            )

        if self.serial_config.serial_port is None:
            self.serial_config.serial_port = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_PORT
            )

        if self.serial_config.baudrate is None:
            self.serial_config.baudrate = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_BAUDRATE
            )

        if self.serial_config.method is None:
            self.serial_config.method = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_METHOD
            )

        if self.serial_config.bytesize is None:
            self.serial_config.bytesize = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_BYTESIZE
            )

        if self.serial_config.stopbits is None:
            self.serial_config.stopbits = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_STOPBITS
            )

        if self.serial_config.parity is None:
            self.serial_config.parity = user_input.get(
                CONF_CONNECTION_TYPE_SERIAL_PARITY
            )

        if self.serial_config.modbus_address is None:
            self.serial_config.modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

        if self.serial_config.serial_port is None:
            return self.async_show_form(
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

    async def async_test_device(
        self, modbus_device: ModbusDevice
    ) -> tuple[str, dict[str, str]]:
        """Test the connection to the Modbus device."""

        device_type_code = ENTITIES[modbus_device.device_type][ENTITY_DEVICE_TYPE_CODE]
        register = device_type_code["register"]
        size = device_type_code["register_size"]

        device_type = None

        try:
            await modbus_device.connect()
            result = await modbus_device.read_input_register(register, count=size)
            await modbus_device.close()

            value = result[0]

            device_type = device_type_code["data_values"][value]

            _LOGGER.debug("Device type code: %s", device_type)

        except Exception as exc:
            message = f"Test Modbus device failed. {exc}"
            _LOGGER.warning(message)
            return [None, {"base": message}]

        return [device_type, None]
