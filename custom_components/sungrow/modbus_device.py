"""ModbusDevice connects and communicates with a remote device either via TCP or Serial."""

from enum import Enum
import logging
import struct

from pymodbus.client.serial import AsyncModbusSerialClient
from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.pdu import ModbusPDU

_LOGGER = logging.getLogger(__name__)


class RegisterType(Enum):
    """Enumeration for Modbus register types."""

    INPUT = 1
    HOLDING = 2


class DataType(str, Enum):
    """Enumeration for Modbus data types."""

    SINT16 = "sint16"
    UINT16 = "uint16"
    SINT32 = "sint32"
    UINT32 = "uint32"


class ModbusDeviceConfig:
    """Configuration for a Modbus device."""

    def __init__(self, *, name: str, device_type: str, modbus_address: int) -> None:
        """Initialize the Modbus device configuration."""
        self.name: str = name
        self.device_type: str = device_type
        self.modbus_address: int = modbus_address

    def iscomplete(self) -> bool:
        """Check if the configuration is complete."""
        return bool(self.name) and bool(self.device_type) and bool(self.modbus_address)


class ModbusTcpDeviceConfig(ModbusDeviceConfig):
    """Configuration for a Modbus device connected via TCP."""

    def __init__(
        self,
        *,
        name: str,
        device_type: str,
        modbus_address: int,
        host: str,
        tcp_port: int,
    ) -> None:
        """Initialize the Modbus device configuration."""
        super().__init__(
            name=name, device_type=device_type, modbus_address=modbus_address
        )
        self.host: str = host
        self.tcp_port: int = tcp_port

    def iscomplete(self) -> bool:
        """Check if the configuration is complete."""
        return super().iscomplete() and bool(self.host) and bool(self.tcp_port)


class ModbusSerialDeviceConfig(ModbusDeviceConfig):
    """Configuration for a Modbus device connected via Serial."""

    def __init__(
        self,
        *,
        name: str,
        device_type: str,
        modbus_address: int,
        serial_port: str,
        baudrate: int,
        method: str,
        bytesize: int,
        stopbits: int,
        parity: str,
    ) -> None:
        """Initialize the Modbus device configuration."""
        super().__init__(
            name=name, device_type=device_type, modbus_address=modbus_address
        )
        self.serial_port: str = serial_port
        self.baudrate: int = baudrate
        self.method: str = method
        self.bytesize: int = bytesize
        self.stopbits: int = stopbits
        self.parity: str = parity

    def iscomplete(self) -> bool:
        """Check if the configuration is complete."""
        return (
            super().iscomplete()
            and bool(self.serial_port)
            and bool(self.baudrate)
            and bool(self.method)
            and bool(self.bytesize)
            and bool(self.stopbits)
            and bool(self.parity)
        )


class ModbusDevice:
    """Representation of a Modbus device."""

    def __init__(self, config: ModbusDeviceConfig) -> None:
        """Initialize the ModbusDevice with the given configuration."""

        self._modbus_client: AsyncModbusSerialClient | AsyncModbusTcpClient = None
        self.device_address: int = config.modbus_address
        self.device_type: str = config.device_type
        self.device_name: str = config.name

        if isinstance(config, ModbusTcpDeviceConfig):
            self._modbus_client = AsyncModbusTcpClient(
                name=config.name,
                host=config.host,
                port=config.tcp_port,
            )
        elif isinstance(config, ModbusSerialDeviceConfig):
            self._modbus_client = AsyncModbusSerialClient(
                name=config.name,
                port=config.serial_port,
                baudrate=config.baudrate,
                method=config.method,
                bytesize=config.bytesize,
                stopbits=config.stopbits,
                parity=config.parity,
            )

    async def connect(self) -> bool:
        """Connect to the Modbus device."""

        return await self._modbus_client.connect()

    def close(self) -> None:
        """Close the connection to the Modbus device."""

        self._modbus_client.close()

    async def write_register(self, register: int, value: bytes | int) -> bool:
        """Write a value to a holding register."""

        result = await self._modbus_client.write_register(
            address=register, value=value, slave=self.device_address
        )
        if result.isError():
            _LOGGER.warning("Failed to write Modbus register %s", register)
            return False
        return not result.isError()

    async def read_register(
        self,
        register: int,
        type=RegisterType.INPUT,
        count=1,
    ) -> list[int] | None:
        """Read a holding register."""

        result: ModbusPDU = None
        if type == RegisterType.INPUT:
            result = await self._modbus_client.read_input_registers(
                address=register, count=count, slave=self.device_address
            )
        else:
            result = await self._modbus_client.read_holding_registers(
                address=register, count=count, slave=self.device_address
            )

        if result.isError():
            _LOGGER.warning(
                "Failed to read Modbus register %s from %s",
                register,
                self.device_address,
            )
            return None
        return result.registers

    async def read_string(
        self,
        register: int,
        type=RegisterType.INPUT,
        length=1,
    ) -> str | None:
        """Read a string from the Modbus device."""

        # Read 16-bit words (2 bytes) since Modbus strings are typically stored as 16-bit characters
        result = await self.read_register(register, type, length)

        if result is not None:
            decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG)
            decoded_string = decoder.decode_string(length * 2).decode("utf-8")
            if "\x00" in decoded_string:
                decoded_string = decoded_string[: decoded_string.index("\x00")]
            return decoded_string
        return None

    async def read_int(
        self,
        register: int,
        type=RegisterType.INPUT,
        data_type=DataType.SINT16,
    ) -> int | None:
        """Read an integer from the Modbus device."""

        count = 1 if data_type in [DataType.SINT16, DataType.UINT16] else 2
        result = await self.read_register(register, type, count)

        if result is None:
            return None

        if count == 1:
            fmt = ">h" if data_type == DataType.SINT16 else ">H"
            return struct.unpack(fmt, struct.pack(">H", result[0]))[0]

        value = (result[1] << 16) | result[0]
        fmt = ">i" if data_type == DataType.SINT32 else ">I"
        return struct.unpack(fmt, struct.pack(">I", value))[0]
