"""Sensor entity type for Sungrow."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo


class ModbusSensor(SensorEntity):
    """Representation of a Modbus sensor."""

    def __init__(
        self, coordinator, name, register_type, register_address, unit_of_measurement
    ):
        self._coordinator = coordinator
        self._name = name
        self._register_type = register_type
        self._register_address = register_address
        self._unit_of_measurement = unit_of_measurement
        self._state = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    async def async_update(self):
        """Fetch new state data from Modbus."""
        if self._register_type == "holding":
            value = await self._device.read_holding_register(self._register_address)
        elif self._register_type == "input":
            value = await self._device.read_input_register(self._register_address)
        else:
            value = None

        if value is not None:
            self._state = value[0]  # Lies das erste Register aus
