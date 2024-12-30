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

CONF_STEP_USER_DEVICE_TYPE = "user_device_type"
CONF_STEP_USER_DEVICE_TCP = "user_device_tcp"
CONF_STEP_USER_DEVICE_SERIAL = "user_device_serial"

CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_TYPE_INVERTER = "device_type_inverter"
CONF_DEVICE_TYPE_WALLBOX = "device_type_wallbox"

CONF_CONNECTION_TYPE = "connection_type"
CONF_CONNECTION_TYPE_TCP = "connection_type_tcp"
CONF_CONNECTION_TYPE_SERIAL = "connection_type_serial"
