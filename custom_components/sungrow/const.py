"""Consts for Sungrow component."""

DOMAIN = "sungrow"

CONF_DEVICE_NAME = "device_name"
CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_TYPE_INVERTER = "inverter"
CONF_DEVICE_TYPE_WALLBOX = "wallbox"

CONF_CONNECTION_TYPE = "connection_type"
CONF_CONNECTION_TYPE_TCP = "tcp"
CONF_TCP_HOST = "host"
CONF_TCP_PORT = "tcp_port"
CONF_CONNECTION_TYPE_SERIAL = "serial"
CONF_SERIAL_PORT = "serial_port"
CONF_SERIAL_EXTRAS = "serial_extras"
CONF_SERIAL_BAUDRATE = "baudrate"
CONF_SERIAL_METHOD = "method"
CONF_SERIAL_METHOD_RTU = "rtu"
CONF_SERIAL_METHOD_ASCII = "ascii"
CONF_SERIAL_BYTESIZE = "bytesize"
CONF_SERIAL_BYTESIZE_5 = "5"
CONF_SERIAL_BYTESIZE_6 = "6"
CONF_SERIAL_BYTESIZE_7 = "7"
CONF_SERIAL_BYTESIZE_8 = "8"
CONF_SERIAL_STOPBITS = "stopbits"
CONF_SERIAL_STOPBITS_1 = "1"
CONF_SERIAL_STOPBITS_2 = "2"
CONF_SERIAL_PARITY = "parity"
CONF_SERIAL_PARITY_NONE = "N"
CONF_SERIAL_PARITY_EVEN = "E"
CONF_SERIAL_PARITY_ODD = "O"

CONF_MODBUS_ADDRESS = "modbus_address"

OPTIONS = {
    CONF_DEVICE_TYPE: [CONF_DEVICE_TYPE_INVERTER, CONF_DEVICE_TYPE_WALLBOX],
    CONF_CONNECTION_TYPE: [CONF_CONNECTION_TYPE_TCP, CONF_CONNECTION_TYPE_SERIAL],
    CONF_SERIAL_METHOD: [
        CONF_SERIAL_METHOD_RTU,
        CONF_SERIAL_METHOD_ASCII,
    ],
    CONF_SERIAL_BYTESIZE: [
        CONF_SERIAL_BYTESIZE_8,
        CONF_SERIAL_BYTESIZE_7,
        CONF_SERIAL_BYTESIZE_6,
        CONF_SERIAL_BYTESIZE_5,
    ],
    CONF_SERIAL_STOPBITS: [
        CONF_SERIAL_STOPBITS_2,
        CONF_SERIAL_STOPBITS_1,
    ],
    CONF_SERIAL_PARITY: [
        CONF_SERIAL_PARITY_NONE,
        CONF_SERIAL_PARITY_EVEN,
        CONF_SERIAL_PARITY_ODD,
    ],
}

DEFAULTS = {
    CONF_TCP_HOST: "",
    CONF_TCP_PORT: "502",
    CONF_SERIAL_PORT: "/dev/ttyUSB0",
    CONF_SERIAL_BAUDRATE: "9600",
    CONF_SERIAL_METHOD: CONF_SERIAL_METHOD_RTU,
    CONF_SERIAL_BYTESIZE: CONF_SERIAL_BYTESIZE_8,
    CONF_SERIAL_STOPBITS: CONF_SERIAL_STOPBITS_2,
    CONF_SERIAL_PARITY: CONF_SERIAL_PARITY_NONE,
    CONF_MODBUS_ADDRESS: {
        CONF_DEVICE_TYPE_INVERTER: {
            CONF_CONNECTION_TYPE_TCP: "1",
            CONF_CONNECTION_TYPE_SERIAL: "1",
        },
        CONF_DEVICE_TYPE_WALLBOX: {
            CONF_CONNECTION_TYPE_TCP: "3",
            CONF_CONNECTION_TYPE_SERIAL: "248",
        },
    },
}

ENTITY_MODEL_NAME = "model_name"
ENTITY_SERIAL_NUMBER = "serial_number"

ENTITIES = {
    CONF_DEVICE_TYPE_INVERTER: {
        ENTITY_SERIAL_NUMBER: {
            "name": "Serial number",
            "register": 4989,
            "register_type": "input",
            "register_size": 10,
            "data_type": "string",
        },
        ENTITY_MODEL_NAME: {
            "name": "Model name",
            "register": 4999,
            "register_type": "input",
            "register_size": 1,
            "data_type": "uint16",
            "enum_values": {
                0x0D06: "SH3K6",
                0x0D07: "SH4K6",
                0x0D09: "SH5K-20",
                0x0D03: "SH5K-V13",
                0x0D0A: "SH3K6-30",
                0x0D0B: "SH4K6-30",
                0x0D0C: "SH5K-30",
                0x0D17: "SH3.RS",
                0x0D0D: "SH3.6RS",
                0x0D18: "SH4.0RS",
                0x0D0F: "SH5.0RS",
                0x0D10: "SH6.0RS",
                0x0D1A: "SH8.0RS",
                0x0D1B: "SH10RS",
                0x0E00: "SH5.0RT",
                0x0E01: "SH6.0RT",
                0x0E02: "SH8.0RT",
                0x0E03: "SH10RT",
                0x0E10: "SH5.0RT-20",
                0x0E11: "SH6.0RT-20",
                0x0E12: "SH8.0RT-20",
                0x0E13: "SH10RT-20",
                0x0E0C: "SH5.0RT-V112",
                0x0E0D: "SH6.0RT-V112",
                0x0E0E: "SH8.0RT-V112",
                0x0E0F: "SH10RT-V112",
                0x0E08: "SH5.0RT-V122",
                0x0E09: "SH6.0RT-V122",
                0x0E0A: "SH8.0RT-V122",
                0x0E0B: "SH10RT-V122",
                0x0D0E: "SH4.6RS",
            },
        },
    },
    CONF_DEVICE_TYPE_WALLBOX: {
        ENTITY_SERIAL_NUMBER: {
            "name": "Serial number",
            "register": 21200,
            "register_type": "input",
            "register_size": 10,
            "data_type": "string",
        },
        ENTITY_MODEL_NAME: {
            "name": "Model name",
            "register": 21223,
            "register_type": "input",
            "register_size": 1,
            "data_type": "uin16",
            "enum_values": {
                0x20ED: "AC007-00",
                0x20DA: "AC011E-01",
            },
        },
    },
}
