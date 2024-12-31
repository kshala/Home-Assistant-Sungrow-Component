"""Consts for Sungrow component."""

DOMAIN = "sungrow"

ENTITIES = {
    "inverter": [
        {"name": "Inverter Power", "register": 100, "type": "holding", "unit": "W"},
        {"name": "Inverter Voltage", "register": 101, "type": "input", "unit": "V"},
    ],
    "battery": [
        {"name": "Battery Charge", "register": 300, "type": "holding", "unit": "%"},
        {"name": "Battery Voltage", "register": 301, "type": "input", "unit": "V"},
    ],
}

CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_TYPE_INVERTER = "inverter"
CONF_DEVICE_TYPE_WALLBOX = "wallbox"

CONF_CONNECTION_TYPE = "connection_type"
CONF_CONNECTION_TYPE_TCP = "tcp"
CONF_CONNECTION_TYPE_SERIAL = "serial"
