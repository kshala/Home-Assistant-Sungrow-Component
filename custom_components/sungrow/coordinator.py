from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

_LOGGER = logging.getLogger(__name__)

class ModbusCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Modbus devices."""

    def __init__(self, hass, modbus_device, update_interval):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Modbus Coordinator",
            update_interval=timedelta(seconds=update_interval),
        )
        self.modbus_device = modbus_device

    async def _async_update_data(self):
        """Fetch data from Modbus registers."""
        try:
            registers = await self.modbus_device.read_all_registers()
            _LOGGER.debug("Fetched data from Modbus: %s", registers)
            return registers
        except Exception as err:
            _LOGGER.error("Failed to fetch data from Modbus: %s", err)
            raise UpdateFailed(f"Error communicating with Modbus device: {err}")
