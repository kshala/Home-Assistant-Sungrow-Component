"""Consts for Sungrow component."""

DOMAIN = "sungrow"

CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_TYPE_INVERTER = "inverter"
CONF_DEVICE_TYPE_WALLBOX = "wallbox"

CONF_CONNECTION_TYPE = "connection_type"
CONF_CONNECTION_TYPE_TCP = "tcp"
CONF_CONNECTION_TYPE_TCP_HOST = "host"
CONF_CONNECTION_TYPE_TCP_PORT = "tcp_port"
CONF_CONNECTION_TYPE_SERIAL = "serial"
CONF_CONNECTION_TYPE_SERIAL_PORT = "serial_port"
CONF_CONNECTION_TYPE_SERIAL_BAUDRATE = "baudrate"
CONF_CONNECTION_TYPE_SERIAL_METHOD = "method"
CONF_CONNECTION_TYPE_SERIAL_BYTESIZE = "bytesize"
CONF_CONNECTION_TYPE_SERIAL_STOPBITS = "stopbits"
CONF_CONNECTION_TYPE_SERIAL_PARITY = "parity"

CONF_MODBUS_ADDRESS = "modbus_address"

OPTIONS = {
    CONF_DEVICE_TYPE: [CONF_DEVICE_TYPE_INVERTER, CONF_DEVICE_TYPE_WALLBOX],
    CONF_CONNECTION_TYPE: [CONF_CONNECTION_TYPE_TCP, CONF_CONNECTION_TYPE_SERIAL],
}

DEFAULTS = {
    CONF_CONNECTION_TYPE_TCP_PORT: 502,
    CONF_CONNECTION_TYPE_SERIAL_PORT: "/dev/ttyUSB0",
    CONF_CONNECTION_TYPE_SERIAL_BAUDRATE: 9600,
    CONF_CONNECTION_TYPE_SERIAL_METHOD: "rtu",
    CONF_CONNECTION_TYPE_SERIAL_BYTESIZE: 8,
    CONF_CONNECTION_TYPE_SERIAL_STOPBITS: 2,
    CONF_CONNECTION_TYPE_SERIAL_PARITY: "N",
    CONF_MODBUS_ADDRESS: {
        CONF_DEVICE_TYPE_INVERTER: {
            CONF_CONNECTION_TYPE_TCP: 1,
            CONF_CONNECTION_TYPE_SERIAL: 1,
        },
        CONF_DEVICE_TYPE_WALLBOX: {
            CONF_CONNECTION_TYPE_TCP: 3,
            CONF_CONNECTION_TYPE_SERIAL: 248,
        },
    },
}

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
