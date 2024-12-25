from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "my_modbus"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up each device as a separate entry."""
    hass.data.setdefault(DOMAIN, {})

    # Speichere die Konfigurationsdaten für das Gerät
    hass.data[DOMAIN][entry.entry_id] = {
        "host": entry.data["host"],
        "port": entry.data.get("port", 502),
    }

    # Lade Plattformen für das Gerät (z. B. Sensoren, Schalter)
    hass.config_entries.async_setup_platforms(entry, ["sensor", "switch"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the config entry."""
    await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
