async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors for a specific device."""
    device_config = hass.data[DOMAIN][config_entry.entry_id]
    host = device_config["host"]
    port = device_config["port"]

    # Beispiel: Sensoren für dieses Gerät erstellen
    async_add_entities([
        ModbusSensor("Temperature Sensor", host, port, 1, "°C"),
        ModbusSensor("Power Sensor", host, port, 2, "W"),
    ])


class ModbusSensor(SensorEntity):
    """Representation of a Modbus sensor."""

    def __init__(self, name, host, port, register, unit):
        self._name = name
        self._host = host
        self._port = port
        self._register = register
        self._unit = unit
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Beispiel: Verbindung herstellen und Register auslesen
        from pymodbus.client.async_tcp import AsyncModbusTcpClient

        async with AsyncModbusTcpClient(self._host, self._port) as client:
            result = await client.read_holding_registers(self._register, 1)
            if not result.isError():
                self._state = result.registers[0]
