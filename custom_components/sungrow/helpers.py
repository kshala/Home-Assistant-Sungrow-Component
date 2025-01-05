"""Helper functions for the Sungrow integration."""

from enum import Enum


class DataType(str, Enum):
    """Enumeration for Modbus data types."""

    SINT16 = "sint16"
    UINT16 = "uint16"
    SINT32 = "sint32"
    UINT32 = "uint32"
    STRING = "string"


class RegisterType(str, Enum):
    """Enumeration for Modbus register types."""

    INPUT = "input"
    HOLDING = "holding"
