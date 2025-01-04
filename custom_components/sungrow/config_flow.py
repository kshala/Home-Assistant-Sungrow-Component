"""Config flow for Sungrow integration."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.data_entry_flow import section
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_CONNECTION_TYPE,
    CONF_CONNECTION_TYPE_SERIAL,
    CONF_CONNECTION_TYPE_TCP,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_MODBUS_ADDRESS,
    CONF_SERIAL_BAUDRATE,
    CONF_SERIAL_BYTESIZE,
    CONF_SERIAL_EXTRAS,
    CONF_SERIAL_METHOD,
    CONF_SERIAL_PARITY,
    CONF_SERIAL_PORT,
    CONF_SERIAL_STOPBITS,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    DEFAULTS,
    DOMAIN,
    ENTITIES,
    ENTITY_MODEL_NAME,
    ENTITY_SERIAL_NUMBER,
    OPTIONS,
)
from .modbus_device import (
    DataType,
    ModbusDevice,
    ModbusSerialDeviceConfig,
    ModbusTcpDeviceConfig,
)

_LOGGER = logging.getLogger(__name__)


class VerifyDeviceConfigResult:
    """Result of verifying the device configuration."""

    def __init__(self, model_name: str, serial_number: str, error: str) -> None:
        """Initialize the result."""
        self.model_name = model_name
        self.serial_number = serial_number
        self.error = error


class SungrowConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Modbus Integration."""

    VERSION = 1
    MINOR_VERSION = 0

    def __init__(self) -> None:
        """Initialize the config flow."""

        self.connection_type: str = None
        self.config: ModbusTcpDeviceConfig | ModbusSerialDeviceConfig = None

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

        device_name = user_input.get(CONF_DEVICE_NAME)
        device_type = user_input.get(CONF_DEVICE_TYPE)
        if self.config is None:
            self.config = ModbusTcpDeviceConfig(
                name=device_name,
                device_type=device_type,
                host=DEFAULTS[CONF_TCP_HOST],
                port=DEFAULTS[CONF_TCP_PORT],
                modbus_address=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                    CONF_CONNECTION_TYPE_TCP
                ],
            )

        host = user_input.get(CONF_TCP_HOST)
        port = user_input.get(CONF_TCP_PORT)
        modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

        if host is not None:
            self.config.host = host

        if port is not None:
            self.config.port = port

        if modbus_address is not None:
            self.config.modbus_address = modbus_address

        errors: dict[str, str] = None

        if self.config.iscomplete():
            verify_result = await self.async_verify_device_config()
            if verify_result.error is None:
                return self.async_create_entry(
                    title=self.config.name,
                    data={
                        CONF_DEVICE_NAME: self.config.name,
                        CONF_DEVICE_TYPE: self.config.device_type,
                        CONF_CONNECTION_TYPE: CONF_CONNECTION_TYPE_TCP,
                        CONF_TCP_HOST: self.config.host,
                        CONF_TCP_PORT: self.config.port,
                        CONF_MODBUS_ADDRESS: self.config.modbus_address,
                    },
                )

            if verify_result.error is not None:
                errors = {"base": verify_result.error}

        if not self.config.iscomplete() or errors is not None:
            return self.async_show_form(
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_TCP_HOST,
                            default=self.config.host,
                        ): str,
                        vol.Required(
                            CONF_TCP_PORT,
                            default=self.config.port,
                        ): vol.Coerce(int),
                        vol.Required(
                            CONF_MODBUS_ADDRESS,
                            default=self.config.modbus_address,
                        ): vol.Coerce(int),
                    }
                ),
                errors=errors,
                last_step=True,
            )

        return None

    async def async_handle_connection_type_serial(
        self, user_input: dict[str, Any], device_name: str, device_type: str
    ) -> ConfigFlowResult:
        """Handle connection type serial."""

        if self.config is None:
            self.config = ModbusSerialDeviceConfig(
                name=user_input.get(CONF_DEVICE_NAME),
                device_type=user_input.get(CONF_DEVICE_TYPE),
                serial_port=None,
                baudrate=None,
                method=None,
                bytesize=None,
                stopbits=None,
                parity=None,
                modbus_address=None,
            )

        if self.config.serial_port is None:
            self.config.serial_port = user_input.get(CONF_SERIAL_EXTRAS).get(
                CONF_SERIAL_PORT
            )

        if self.config.baudrate is None:
            self.config.baudrate = user_input.get(CONF_SERIAL_BAUDRATE)

        if self.config.method is None:
            self.config.method = user_input.get(CONF_SERIAL_METHOD)

        if self.config.bytesize is None:
            self.config.bytesize = user_input.get(CONF_SERIAL_BYTESIZE)

        if self.config.stopbits is None:
            self.config.stopbits = user_input.get(CONF_SERIAL_STOPBITS)

        if self.config.parity is None:
            self.config.parity = user_input.get(CONF_SERIAL_PARITY)

        if self.config.modbus_address is None:
            self.config.modbus_address = user_input.get(CONF_MODBUS_ADDRESS)

        if self.config.serial_port is None:
            return self.async_show_form(
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_SERIAL_PORT,
                            default=DEFAULTS[CONF_SERIAL_PORT],
                        ): vol.Coerce(int),
                        CONF_SERIAL_EXTRAS: section(
                            {"collapsed": True},
                            {
                                vol.Required(
                                    CONF_SERIAL_BAUDRATE,
                                    default=DEFAULTS[CONF_SERIAL_BAUDRATE],
                                ): vol.Coerce(int),
                                vol.Required(
                                    CONF_SERIAL_METHOD,
                                    default=DEFAULTS[CONF_SERIAL_METHOD],
                                ): SelectSelector(
                                    SelectSelectorConfig(
                                        options=OPTIONS[CONF_SERIAL_METHOD],
                                        mode=SelectSelectorMode.DROPDOWN,
                                        translation_key=CONF_SERIAL_METHOD,
                                        sort=False,
                                    )
                                ),
                                vol.Required(
                                    CONF_SERIAL_BYTESIZE,
                                    default=DEFAULTS[CONF_SERIAL_BYTESIZE],
                                ): SelectSelector(
                                    SelectSelectorConfig(
                                        options=OPTIONS[CONF_SERIAL_BYTESIZE],
                                        mode=SelectSelectorMode.DROPDOWN,
                                        translation_key=CONF_SERIAL_BYTESIZE,
                                        sort=False,
                                    )
                                ),
                                vol.Required(
                                    CONF_SERIAL_STOPBITS,
                                    default=DEFAULTS[CONF_SERIAL_STOPBITS],
                                ): SelectSelector(
                                    SelectSelectorConfig(
                                        options=OPTIONS[CONF_SERIAL_STOPBITS],
                                        mode=SelectSelectorMode.DROPDOWN,
                                        translation_key=CONF_SERIAL_STOPBITS,
                                        sort=False,
                                    )
                                ),
                                vol.Required(
                                    CONF_SERIAL_PARITY,
                                    default=DEFAULTS[CONF_SERIAL_PARITY],
                                ): SelectSelector(
                                    SelectSelectorConfig(
                                        options=OPTIONS[CONF_SERIAL_PARITY],
                                        mode=SelectSelectorMode.DROPDOWN,
                                        translation_key=CONF_SERIAL_PARITY,
                                        sort=False,
                                    )
                                ),
                            },
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

    async def async_verify_device_config(self) -> VerifyDeviceConfigResult:
        """Test the connection to the Modbus device."""

        modbus_device = ModbusDevice(self.config)
        device_type = self.config.device_type
        model_name_value: str = None
        serial_number_value: str = None
        error_message: str = None

        try:
            await modbus_device.connect()

            entity_model_name = ENTITIES[device_type][ENTITY_MODEL_NAME]
            register = entity_model_name["register"]
            result = await modbus_device.read_int(register, data_type=DataType.UINT16)
            model_name_value = entity_model_name["enum_values"][result]

            entity_serial_number = ENTITIES[device_type][ENTITY_SERIAL_NUMBER]
            register = entity_serial_number["register"]
            register_size = entity_serial_number["register_size"]
            result = await modbus_device.read_string(register, length=register_size)
            serial_number_value = result

            _LOGGER.debug("Model name: %s", model_name_value)
        except Exception as exc:
            error_message = f"Test Modbus device failed. {exc}"
            _LOGGER.warning(error_message)

        modbus_device.close()
        modbus_device = None
        return VerifyDeviceConfigResult(
            model_name_value, serial_number_value, error_message
        )
