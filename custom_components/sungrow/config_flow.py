from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN  # Dein Domain-Name

class MyModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Modbus Integration."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # validate input is a real IP address
            if not self._is_valid_ip(user_input["host"]):
                errors["host"] = "invalid_host"
            else:
                # validate device is already added
                for entry in self._async_current_entries():
                    if entry.data.get("host") == user_input["host"]:
                        errors["host"] = "already_configured"
                        break

                if not errors:
                    # create a new device
                    return self.async_create_entry(title=f"Modbus Device ({user_input['host']})", data=user_input)

        # show form to user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("port", default=502): vol.Coerce(int),
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def _is_valid_ip(ip):
        """Einfacher Check für gültige IP-Adresse."""
        import ipaddress
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
