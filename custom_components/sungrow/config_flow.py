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
    CONF_CONNECTION_TYPE_TCP,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_MODBUS_ADDRESS,
    CONF_OPTIONS,
    CONF_SERIAL_BAUDRATE,
    CONF_SERIAL_BYTESIZE,
    CONF_SERIAL_METHOD,
    CONF_SERIAL_PARITY,
    CONF_SERIAL_PORT,
    CONF_SERIAL_STOPBITS,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    DEFAULTS,
    DOMAIN,
)
from .entity_descriptions import ENTITIES, ENTITY_MODEL_NAME, ENTITY_SERIAL_NUMBER
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

        if user_input is not None:
            connection_type = user_input.get(CONF_CONNECTION_TYPE)
            if connection_type is not None:
                self.connection_type = connection_type

        if self.connection_type == CONF_CONNECTION_TYPE_TCP:
            return await self.async_handle_connection_type_tcp(user_input)

        if self.connection_type == CONF_CONNECTION_TYPE_SERIAL:
            return await self.async_handle_connection_type_serial(user_input)

        return await self.async_show_form_init()

    async def async_show_form_init(self) -> ConfigFlowResult:
        """Show the initial form."""
        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_NAME): str,
                    vol.Required(CONF_DEVICE_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=CONF_OPTIONS[CONF_DEVICE_TYPE],
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_DEVICE_TYPE,
                            sort=False,
                        )
                    ),
                    vol.Required(CONF_CONNECTION_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=CONF_OPTIONS[CONF_CONNECTION_TYPE],
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

        user_input_required = False

        device_name = user_input.get(CONF_DEVICE_NAME)
        device_type = user_input.get(CONF_DEVICE_TYPE)
        modbus_address = user_input.get(CONF_MODBUS_ADDRESS)
        host = user_input.get(CONF_TCP_HOST)
        tcp_port = user_input.get(CONF_TCP_PORT)

        if self.config is None:
            user_input_required = True
            self.config = ModbusTcpDeviceConfig(
                name=device_name,
                device_type=device_type,
                modbus_address=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                    CONF_CONNECTION_TYPE_TCP
                ],
                host=DEFAULTS[CONF_TCP_HOST],
                tcp_port=DEFAULTS[CONF_TCP_PORT],
            )

        if modbus_address is not None:
            self.config.modbus_address = modbus_address

        if host is not None:
            self.config.host = host

        if tcp_port is not None:
            self.config.tcp_port = tcp_port

        errors: dict[str, str] = None
        if self.config.iscomplete() and not user_input_required:
            verify_result = await self.async_verify_device_config()
            if verify_result.error is not None:
                user_input_required = True
                errors = {"base": verify_result.error}
            else:
                return self.async_create_entry(
                    title=self.config.name,
                    data={
                        CONF_DEVICE_TYPE: self.config.device_type,
                        CONF_CONNECTION_TYPE: CONF_CONNECTION_TYPE_TCP,
                        CONF_MODBUS_ADDRESS: self.config.modbus_address,
                        CONF_TCP_HOST: self.config.host,
                        CONF_TCP_PORT: self.config.tcp_port,
                    },
                )

        return self.async_show_form(
            data_schema=self.create_data_schema_tcp(),
            errors=errors,
            last_step=True,
        )

    async def async_handle_connection_type_serial(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle connection type serial."""

        user_input_required = False

        device_name = user_input.get(CONF_DEVICE_NAME)
        device_type = user_input.get(CONF_DEVICE_TYPE)
        modbus_address = user_input.get(CONF_MODBUS_ADDRESS)
        serial_port = user_input.get(CONF_SERIAL_PORT)
        baudrate = user_input.get(CONF_SERIAL_BAUDRATE)
        method = user_input.get(CONF_SERIAL_METHOD)
        bytesize = user_input.get(CONF_SERIAL_BYTESIZE)
        stopbits = user_input.get(CONF_SERIAL_STOPBITS)
        parity = user_input.get(CONF_SERIAL_PARITY)

        if self.config is None:
            user_input_required = True
            self.config = ModbusSerialDeviceConfig(
                name=device_name,
                device_type=device_type,
                modbus_address=DEFAULTS[CONF_MODBUS_ADDRESS][device_type][
                    CONF_CONNECTION_TYPE_SERIAL
                ],
                serial_port=DEFAULTS[CONF_SERIAL_PORT],
                baudrate=DEFAULTS[CONF_SERIAL_BAUDRATE],
                method=DEFAULTS[CONF_SERIAL_METHOD],
                bytesize=DEFAULTS[CONF_SERIAL_BYTESIZE],
                stopbits=DEFAULTS[CONF_SERIAL_STOPBITS],
                parity=DEFAULTS[CONF_SERIAL_PARITY],
            )

        if serial_port is not None:
            self.config.serial_port = serial_port

        if modbus_address is not None:
            self.config.modbus_address = modbus_address

        if baudrate is not None:
            self.config.baudrate = baudrate

        if method is not None:
            self.config.method = method

        if bytesize is not None:
            self.config.bytesize = bytesize

        if stopbits is not None:
            self.config.stopbits = stopbits

        if parity is not None:
            self.config.parity = parity

        errors: dict[str, str] = None
        if self.config.iscomplete() and not user_input_required:
            verify_result = await self.async_verify_device_config()
            if verify_result.error is not None:
                user_input_required = True
                errors = {"base": verify_result.error}
            else:
                return self.async_create_entry(
                    title=self.config.name,
                    data={
                        CONF_DEVICE_TYPE: self.config.device_type,
                        CONF_CONNECTION_TYPE: CONF_CONNECTION_TYPE_SERIAL,
                        CONF_MODBUS_ADDRESS: self.config.modbus_address,
                        CONF_SERIAL_PORT: self.config.serial_port,
                        CONF_SERIAL_BAUDRATE: self.config.baudrate,
                        CONF_SERIAL_METHOD: self.config.method,
                        CONF_SERIAL_BYTESIZE: self.config.bytesize,
                        CONF_SERIAL_STOPBITS: self.config.stopbits,
                        CONF_SERIAL_PARITY: self.config.parity,
                    },
                )

        return self.async_show_form(
            data_schema=self.create_data_schema_serial(),
            errors=errors,
            last_step=True,
        )

    def create_data_schema_tcp(self) -> vol.Schema:
        """Create the data schema for the TCP form."""

        return vol.Schema(
            {
                vol.Required(
                    CONF_MODBUS_ADDRESS, default=self.config.modbus_address
                ): vol.Coerce(int),
                vol.Required(CONF_TCP_HOST, default=self.config.host): str,
                vol.Required(CONF_TCP_PORT, default=self.config.tcp_port): vol.Coerce(
                    int
                ),
            }
        )

    def create_data_schema_serial(self) -> vol.Schema:
        """Create the data schema for the serial form."""

        return vol.Schema(
            {
                vol.Required(
                    CONF_MODBUS_ADDRESS, default=self.config.modbus_address
                ): vol.Coerce(int),
                vol.Required(
                    CONF_SERIAL_PORT, default=self.config.serial_port
                ): vol.Coerce(str),
                vol.Required(
                    CONF_SERIAL_BAUDRATE, default=self.config.baudrate
                ): vol.Coerce(int),
                vol.Required(
                    CONF_SERIAL_METHOD, default=self.config.method
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=CONF_OPTIONS[CONF_SERIAL_METHOD],
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key=CONF_SERIAL_METHOD,
                        sort=False,
                    )
                ),
                vol.Required(
                    CONF_SERIAL_BYTESIZE, default=self.config.bytesize
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=CONF_OPTIONS[CONF_SERIAL_BYTESIZE],
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key=CONF_SERIAL_BYTESIZE,
                        sort=False,
                    )
                ),
                vol.Required(
                    CONF_SERIAL_STOPBITS, default=self.config.stopbits
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=CONF_OPTIONS[CONF_SERIAL_STOPBITS],
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key=CONF_SERIAL_STOPBITS,
                        sort=False,
                    )
                ),
                vol.Required(
                    CONF_SERIAL_PARITY, default=self.config.parity
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=CONF_OPTIONS[CONF_SERIAL_PARITY],
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key=CONF_SERIAL_PARITY,
                        sort=False,
                    )
                ),
            }
        )

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
        except Exception as exc:  # noqa: BLE001
            error_message = f"Test Modbus device failed. {exc}"
            _LOGGER.warning(error_message)

        modbus_device.close()
        modbus_device = None
        return VerifyDeviceConfigResult(
            model_name_value, serial_number_value, error_message
        )
