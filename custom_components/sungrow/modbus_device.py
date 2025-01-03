"""ModbusDevice connects and communicates with a remote device either via TCP or Serial."""

import logging
from typing import TypedDict

from pymodbus.client import ModbusBaseClient
from pymodbus.client.serial import AsyncModbusSerialClient
from pymodbus.client.tcp import AsyncModbusTcpClient

from .const import ENTITIES

_LOGGER = logging.getLogger(__name__)


class ModbusDeviceConfig(TypedDict):
    """Configuration for a Modbus device."""

    name: str
    device_type: str
    modbus_address: int


class ModbusTcpDeviceConfig(ModbusDeviceConfig):
    """Configuration for a Modbus device connected via TCP."""

    host: str
    port: int


class ModbusSerialDeviceConfig(ModbusDeviceConfig):
    """Configuration for a Modbus device connected via Serial."""

    serial_port: str
    baudrate: int
    method: str
    bytesize: int
    stopbits: int
    parity: str


class ModbusDevice:
    """Representation of a Modbus device."""

    def __init__(self, config: ModbusDeviceConfig) -> None:
        """Initialize the ModbusDevice with the given configuration."""

        # self._config: ModbusDeviceConfig = config
        self._modbus_client: ModbusBaseClient = None

        self.device_address: int = config["modbus_address"]
        self.device_type: str = config["device_type"]
        self.device_name: str = config["name"]

        if isinstance(config, ModbusTcpDeviceConfig):
            self._modbus_client = AsyncModbusTcpClient(
                name=config["name"],
                host=config["host"],
                port=config["port"],
            )
        elif isinstance(config, ModbusSerialDeviceConfig):
            self._modbus_client = AsyncModbusSerialClient(
                name=config["name"],
                port=config["serial_port"],
                baudrate=config["baudrate"],
                method=config["method"],
                bytesize=config["bytesize"],
                stopbits=config["stopbits"],
                parity=config["parity"],
            )

    async def connect(self):
        """Connect to the Modbus device."""

        await self._modbus_client.connect()

    async def close(self):
        """Close the connection to the Modbus device."""

        await self._modbus_client.close()

    async def write_holding_register(self, register: int, value: bytes | int) -> bool:
        """Write a value to a holding register."""

        result = await self._modbus_client.write_register(
            address=register, value=value, slave=self._device_address
        )
        if result.isError():
            _LOGGER.warning("Failed to write Modbus register %s", register)
            return False
        return not result.isError()

    async def read_holding_register(
        self, register: int, count: int = 1
    ) -> list[int] | None:
        """Read a holding register."""

        result = await self._modbus_client.read_holding_registers(
            address=register, count=count, slave=self._device_address
        )
        if result.isError():
            _LOGGER.warning(
                "Failed to read Modbus register %s from %s",
                register,
                self._device_address,
            )
            return None
        return result.registers

    async def read_input_register(
        self, register: int, count: int = 1
    ) -> list[int] | None:
        """Read an input register."""

        result = await self._modbus_client.read_input_registers(
            address=register, count=count, slave=self._device_address
        )
        if result.isError():
            _LOGGER.warning(
                "Failed to read Modbus register %s from %s",
                register,
                self._device_address,
            )
            return None
        return result.registers
