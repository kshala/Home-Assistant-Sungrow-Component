from homeassistant.components.input_number import InputNumberEntity
from homeassistant.core import HomeAssistant

class ModbusInputNumber(InputNumberEntity):
    """Representation of a Modbus holding register as an input number."""

    def __init__(self, device, name, register_address, min_value, max_value, step):
        self._device = device  # ModbusDevice-Instanz
        self._name = name
        self._register_address = register_address
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def step(self):
        return self._step

    async def async_update(self):
        """Fetch the current value from the Modbus register."""
        value = await self._device.read_holding_register(self._register_address)
        if value is not None:
            self._state = value[0]  # Lies das erste Register aus

    async def async_set_value(self, value):
        """Set a new value to the Modbus register."""
        if self._min_value <= value <= self._max_value:
            await self._device.write_holding_register(self._register_address, int(value))
            self._state = value
