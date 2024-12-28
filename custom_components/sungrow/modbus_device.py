from pymodbus.client.async_tcp import AsyncModbusTcpClient

class ModbusDevice:
    """Representation of a Modbus device."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None

    async def connect(self):
        self.client = AsyncModbusTcpClient(self.host, self.port)
        await self.client.connect()

    async def write_holding_register(self, address, value):
        if self.client is None or not self.client.connected:
            await self.connect()
        result = await self.client.write_register(address, value)
        if result.isError():
            _LOGGER.warning("Failed to read Modbus register %s", address)
            return False
        return not result.isError()

    async def read_holding_register(self, address, count=1):
        if self.client is None or not self.client.connected:
            await self.connect()
        result = await self.client.read_holding_registers(address, count)
        if result.isError():
            _LOGGER.warning("Failed to read Modbus register %s", address)
            return None
        return result.registers

    async def read_input_register(self, address, count=1):
        if self.client is None or not self.client.connected:
            await self.connect()
        result = await self.client.read_input_registers(address, count)
        if result.isError():
            return None
        return result.registers
