from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import { DOMAIN, ENTITY_DEFINITIONS }

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Modbus sensors for a specific device."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    device_type = config["device_type"]
    host = config["host"]
    port = config["port"]

    # ModbusDevice-Instanz für das Gerät erstellen
    modbus_device = ModbusDevice(host, port)
    await modbus_device.connect()

    # Coordinator erstellen
    coordinator = ModbusCoordinator(hass, modbus_device, update_interval=30)
    await coordinator.async_config_entry_first_refresh()

    # Sensorspezifische Definitionen
    entities = []

    if device_type == "inverter":
        #entities.extend([
        #    ModbusSensor(modbus_device, "Inverter Power", "holding", 100, "W"),
        #    ModbusSensor(modbus_device, "Inverter Voltage", "input", 101, "V"),
        #])
        #entities.append(ModbusInputNumber(modbus_device, "Inverter Max Power", 200, 0, 5000, 10))

        for sensor_def in SENSOR_DEFINITIONS[device_config["device_type"]]:
            entities.append(
                ModbusSensor(
                    coordinator,
                    sensor_def["name"],
                    sensor_def["type"],
                    sensor_def["register"],
                    sensor_def["unit"],
                )
            )
    elif device_type == "battery":
        entities.extend([
            ModbusSensor(coordinator, "Battery Charge", "holding", 200, "%"),
            ModbusSensor(coordinator, "Battery Voltage", "input", 201, "V"),
        ])
    elif device_type == "wallbox":
        entities.extend([
            ModbusSensor(coordinator, "Wallbox Current", "holding", 300, "A"),
            ModbusSensor(coordinator, "Wallbox Status", "input", 301, ""),
        ])

    async_add_entities(sensors)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the config entry."""
    await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
