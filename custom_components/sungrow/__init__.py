"""Custom Component for Sungrow Devices."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_CONNECTION_TYPE,
    CONF_CONNECTION_TYPE_SERIAL,
    CONF_CONNECTION_TYPE_TCP,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_MODBUS_ADDRESS,
    CONF_SERIAL_BAUDRATE,
    CONF_SERIAL_BYTESIZE,
    CONF_SERIAL_METHOD,
    CONF_SERIAL_PARITY,
    CONF_SERIAL_PORT,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
)
from .modbus_device import ModbusDevice, ModbusSerialDeviceConfig, ModbusTcpDeviceConfig

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Sungrow from a config entry."""

    connection_type = config_entry.data[CONF_CONNECTION_TYPE]

    config: ModbusTcpDeviceConfig | ModbusSerialDeviceConfig

    if connection_type == CONF_CONNECTION_TYPE_TCP:
        config = ModbusTcpDeviceConfig(
            name=config_entry.title,  # [CONF_DEVICE_NAME],
            device_type=config_entry.data[CONF_DEVICE_TYPE],
            modbus_address=config_entry.data[CONF_MODBUS_ADDRESS],
            host=config_entry.data[CONF_TCP_HOST],
            tcp_port=config_entry.data[CONF_TCP_PORT],
        )
    elif connection_type == CONF_CONNECTION_TYPE_SERIAL:
        config = ModbusSerialDeviceConfig(
            name=config_entry.title,  # .data[CONF_DEVICE_NAME],
            device_type=config_entry.data[CONF_DEVICE_TYPE],
            modbus_address=config_entry.data[CONF_MODBUS_ADDRESS],
            serial_port=config_entry.data[CONF_SERIAL_PORT],
            baudrate=config_entry.data[CONF_SERIAL_BAUDRATE],
            bytesize=config_entry.data[CONF_SERIAL_BYTESIZE],
            parity=config_entry.data[CONF_SERIAL_PARITY],
            method=config_entry.data[CONF_SERIAL_METHOD],
        )

    modbus_device = ModbusDevice(config)
    await modbus_device.connect()

    config_entry.runtime_data = modbus_device

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    if unload_ok:
        modbus_device: ModbusDevice = config_entry.runtime_data
        modbus_device.close()

    return unload_ok

    # # ModbusDevice-Instanz für das Gerät erstellen
    # modbus_device = ModbusDevice(host, port)
    # await modbus_device.connect()

    # # Coordinator erstellen
    # coordinator = ModbusCoordinator(hass, modbus_device, update_interval=30)
    # await coordinator.async_config_entry_first_refresh()

    # # Sensorspezifische Definitionen
    # entities = []

    # if device_type == "inverter":
    #     # entities.extend([
    #     #    ModbusSensor(modbus_device, "Inverter Power", "holding", 100, "W"),
    #     #    ModbusSensor(modbus_device, "Inverter Voltage", "input", 101, "V"),
    #     # ])
    #     # entities.append(ModbusInputNumber(modbus_device, "Inverter Max Power", 200, 0, 5000, 10))

    #     for sensor_def in ENTITIES[device_config["device_type"]]:
    #         entities.append(
    #             ModbusSensor(
    #                 coordinator,
    #                 sensor_def["name"],
    #                 sensor_def["type"],
    #                 sensor_def["register"],
    #                 sensor_def["unit"],
    #             )
    #         )
    # elif device_type == "battery":
    #     entities.extend(
    #         [
    #             ModbusSensor(coordinator, "Battery Charge", "holding", 200, "%"),
    #             ModbusSensor(coordinator, "Battery Voltage", "input", 201, "V"),
    #         ]
    #     )
    # elif device_type == "wallbox":
    #     entities.extend(
    #         [
    #             ModbusSensor(coordinator, "Wallbox Current", "holding", 300, "A"),
    #             ModbusSensor(coordinator, "Wallbox Status", "input", 301, ""),
    #         ]
    #     )

    # async_add_entities(entities)


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Unload the config entry."""
#     await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
#     hass.data[DOMAIN].pop(entry.entry_id)
#     return True
