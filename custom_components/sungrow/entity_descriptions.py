"""Entity descriptions for Sungrow integration."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    Platform,
    UnitOfApparentPower,
    UnitOfConductivity,
    UnitOfDataRate,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfInformation,
    UnitOfPower,
    UnitOfReactivePower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify

from .const import CONF_DEVICE_TYPE_INVERTER, CONF_DEVICE_TYPE_WALLBOX
from .helpers import DataType, RegisterType


@dataclass(frozen=True)
class SungrowSensorEntityDescription(SensorEntityDescription):
    """Describes Sungrow sensor entity."""

    register: int | None = None
    register_type: RegisterType | None = None
    register_size: int | None = None
    data_type: DataType | None = None
    scale: float | None = None
    enum_values: dict[int, str] | None = None
    related_models: list[str] | None = None


type SungrowEntityTuple = tuple[SungrowSensorEntityDescription, ...]

PLATFORMS = [Platform.SENSOR]

ENTITY_SERIAL_NUMBER = "serial_number"
ENTITY_MODEL_NAME = "model_name"
ENTITY_NOMINAL_OUTPUT_POWER = "nominal_output_power"
ENTITY_OUTPUT_TYPE = "output_type"
ENTITY_DAILY_OUTPUT_ENERGY = "daily_output_energy"
ENTITY_TOTAL_OUTPUT_ENERGY = "total_output_energy"
ENTITY_TEMPERATURE = "temperature"
ENTITY_MPPT1_VOLTAGE = "mppt1_voltage"
ENTITY_MPPT1_CURRENT = "mppt1_current"
ENTITY_MPPT2_VOLTAGE = "mppt2_voltage"
ENTITY_MPPT2_CURRENT = "mppt2_current"
ENTITY_MPPT3_VOLTAGE = "mppt3_voltage"
ENTITY_MPPT3_CURRENT = "mppt3_current"
ENTITY_MPPT4_VOLTAGE = "mppt4_voltage"
ENTITY_MPPT4_CURRENT = "mppt4_current"
ENTITY_PV_POWER = "pv_power"
ENTITY_PHASE_A_VOLTAGE = "phase_a_voltage"
ENTITY_PHASE_B_VOLTAGE = "phase_b_voltage"
ENTITY_PHASE_C_VOLTAGE = "phase_c_voltage"
ENTITY_REACTIVE_POWER = "reactive_power"
ENTITY_POWER_FACTOR = "power_factor"
ENTITY_GRID_FREQUENCY = "grid_frequency"
ENTITY_METER_PHASE_A_ACTIVE_POWER = "meter_phase_a_active_power"
ENTITY_METER_PHASE_B_ACTIVE_POWER = "meter_phase_b_active_power"
ENTITY_METER_PHASE_C_ACTIVE_POWER = "meter_phase_c_active_power"

ENTITY_BATTERY_POWER = "battery_power"

ENTITIES = {
    CONF_DEVICE_TYPE_INVERTER: SungrowEntityTuple(
        SungrowSensorEntityDescription(
            key=ENTITY_SERIAL_NUMBER,
            translation_key=ENTITY_SERIAL_NUMBER,
            register=4989,
            register_type=RegisterType.INPUT,
            register_size=10,
            data_type=DataType.STRING,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MODEL_NAME,
            translation_key=ENTITY_MODEL_NAME,
            register=4999,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            enum_values={
                0x0D03: "SH5K-V13",
                0x0D06: "SH3K6",
                0x0D07: "SH4K6",
                0x0D09: "SH5K-20",
                0x0D0A: "SH3K6-30",
                0x0D0B: "SH4K6-30",
                0x0D0C: "SH5K-30",
                0x0D0D: "SH3.6RS",
                0x0D0E: "SH4.6RS",
                0x0D0F: "SH5.0RS",
                0x0D10: "SH6.0RS",
                0x0D17: "SH3.0RS",
                0x0D18: "SH4.0RS",
                0x0D1A: "SH8.0RS",
                0x0D1B: "SH10RS",
                0x0E00: "SH5.0RT",
                0x0E01: "SH6.0RT",
                0x0E02: "SH8.0RT",
                0x0E03: "SH10RT",
                0x0E08: "SH5.0RT-V122",
                0x0E09: "SH6.0RT-V122",
                0x0E0A: "SH8.0RT-V122",
                0x0E0B: "SH10RT-V122",
                0x0E0C: "SH5.0RT-V112",
                0x0E0D: "SH6.0RT-V112",
                0x0E0E: "SH8.0RT-V112",
                0x0E0F: "SH10RT-V112",
                0x0E10: "SH5.0RT-20",
                0x0E11: "SH6.0RT-20",
                0x0E12: "SH8.0RT-20",
                0x0E13: "SH10RT-20",
                0x0E20: "SH5T-V11",
                0x0E21: "SH6T-V11",
                0x0E22: "SH8T-V11",
                0x0E23: "SH10T-V11",
                0x0E24: "SH12T-V11",
                0x0E25: "SH15T-V11",
                0x0E26: "SH20T-V11",
                0x0E28: "SH25T-V11",
            },
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_NOMINAL_OUTPUT_POWER,
            translation_key=ENTITY_NOMINAL_OUTPUT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            unit_of_measurement=UnitOfPower.KILO_WATT,
            suggested_display_precision=1,
            register=5000,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_OUTPUT_TYPE,
            translation_key=ENTITY_OUTPUT_TYPE,
            register=5001,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            enum_values={
                0x0000: "Single phase",
                0x0001: "1-3P4L",
                0x0002: "2-3P3L",
            },
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DAILY_OUTPUT_ENERGY,
            translation_key=ENTITY_DAILY_OUTPUT_ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5002,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_TOTAL_OUTPUT_ENERGY,
            translation_key=ENTITY_TOTAL_OUTPUT_ENERGY,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5003,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_TEMPERATURE,
            translation_key=ENTITY_TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            register=5007,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT1_VOLTAGE,
            translation_key=ENTITY_MPPT1_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5010,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT1_CURRENT,
            translation_key=ENTITY_MPPT1_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5011,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT2_VOLTAGE,
            translation_key=ENTITY_MPPT2_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5012,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT2_CURRENT,
            translation_key=ENTITY_MPPT2_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5013,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT3_VOLTAGE,
            translation_key=ENTITY_MPPT3_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5014,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT3_CURRENT,
            translation_key=ENTITY_MPPT3_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5015,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT4_VOLTAGE,
            translation_key=ENTITY_MPPT4_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5114,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH8.0RS", "SH10RS"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT4_CURRENT,
            translation_key=ENTITY_MPPT4_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5115,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH8.0RS", "SH10RS"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_POWER,
            translation_key=ENTITY_PV_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5016,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.UINT32,
            scale=1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_VOLTAGE,
            translation_key=ENTITY_PHASE_A_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5018,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_VOLTAGE,
            translation_key=ENTITY_PHASE_B_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5019,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_VOLTAGE,
            translation_key=ENTITY_PHASE_C_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5020,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_REACTIVE_POWER,
            translation_key=ENTITY_REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.REACTIVE_POWER,
            unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
            suggested_display_precision=0,
            register=5032,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.SINT32,
            scale=1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_POWER_FACTOR,
            translation_key=ENTITY_POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER_FACTOR,
            unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=5034,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_GRID_FREQUENCY,
            translation_key=ENTITY_GRID_FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.FREQUENCY,
            unit_of_measurement=UnitOfFrequency.HERTZ,
            suggested_display_precision=2,
            register=5241,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_A_ACTIVE_POWER,
            translation_key=ENTITY_METER_PHASE_A_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5602,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.SINT32,
            scale=1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_B_ACTIVE_POWER,
            translation_key=ENTITY_METER_PHASE_B_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5604,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.SINT32,
            scale=1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_C_ACTIVE_POWER,
            translation_key=ENTITY_METER_PHASE_C_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5606,
            register_type=RegisterType.INPUT,
            register_size=2,
            data_type=DataType.SINT32,
            scale=1,
        ),
    ),
    CONF_DEVICE_TYPE_WALLBOX: SungrowEntityTuple(
        SungrowSensorEntityDescription(
            key=ENTITY_SERIAL_NUMBER,
            translation_key=ENTITY_SERIAL_NUMBER,
            register=21200,
            register_type=RegisterType.INPUT,
            register_size=10,
            data_type=DataType.STRING,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MODEL_NAME,
            translation_key=ENTITY_MODEL_NAME,
            register=21223,
            register_type=RegisterType.INPUT,
            register_size=1,
            data_type=DataType.UINT16,
            enum_values={
                0x20ED: "AC007-00",
                0x20DA: "AC011E-01",
            },
        ),
    ),
}
