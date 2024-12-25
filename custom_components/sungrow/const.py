DOMAIN = "my_modbus"
DEFAULT_PORT = 502
DEFAULT_TIMEOUT = 10

SENSOR_DEFINITIONS = {
    "inverter": [
        {"name": "Inverter Power", "register": 100, "type": "holding", "unit": "W"},
        {"name": "Inverter Voltage", "register": 101, "type": "input", "unit": "V"},
    ],
    "battery": [
        {"name": "Battery Charge", "register": 300, "type": "holding", "unit": "%"},
        {"name": "Battery Voltage", "register": 301, "type": "input", "unit": "V"},
    ],
}
