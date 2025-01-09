"""Entity descriptions for Sungrow integration."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
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

from .const import (
    CONF_DEVICE_TYPE_BATTERY,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
)
from .helpers import DataType, RegisterType


class SungrowBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Sungrow binary sensor entity."""

    register: int
    register_type: RegisterType = RegisterType.INPUT
    data_type: DataType
    data_count: int = 1
    related_models: list[str] | None = None
    entity_class: str | None = None


@dataclass(frozen=True)
class SungrowSensorEntityDescription(SensorEntityDescription):
    """Describes Sungrow sensor entity."""

    register: int
    register_type: RegisterType = RegisterType.INPUT
    data_type: DataType
    data_count: int = 1
    scale: float = 1.0
    enum_values: dict[int, str] | None = None
    related_models: list[str] | None = None
    entity_class: str | None = None


type SungrowEntityTuple = tuple[SungrowSensorEntityDescription, ...]

PLATFORMS = [Platform.SENSOR]

ENTITY_PROTOCOL_NUMBER = "protocol_number"
ENTITY_PROTOCOL_VERSION = "protocol_version"
ENTITY_ARM_SOFTWARE_VERSION = "arm_software_version"
ENTITY_DSP_SOFTWARE_VERSION = "dsp_software_version"
ENTITY_SERIAL_NUMBER = "serial_number"
ENTITY_MODEL_NAME = "model_name"
ENTITY_NOMINAL_OUTPUT_POWER = "nominal_output_power"
ENTITY_OUTPUT_TYPE = "output_type"
ENTITY_OUTPUT_ENERGY_TODAY = "output_energy_today"
ENTITY_OUTPUT_ENERGY_TOTAL = "output_energy_total"
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
ENTITY_MINIMUM_EXPORT_POWER_LIMIT = "minimum_export_power_limit"
ENTITY_MAXIMUM_EXPORT_POWER_LIMIT = "maximum_export_power_limit"
ENTITY_PHASE_A_BACKUP_CURRENT = "phase_a_backup_current"
ENTITY_PHASE_B_BACKUP_CURRENT = "phase_b_backup_current"
ENTITY_PHASE_C_BACKUP_CURRENT = "phase_c_backup_current"
ENTITY_PHASE_A_BACKUP_POWER = "phase_a_backup_power"
ENTITY_PHASE_B_BACKUP_POWER = "phase_b_backup_power"
ENTITY_PHASE_C_BACKUP_POWER = "phase_c_backup_power"
ENTITY_TOTAL_BACKUP_POWER = "total_backup_power"
ENTITY_PHASE_A_BACKUP_VOLTAGE = "phase_a_backup_voltage"
ENTITY_PHASE_B_BACKUP_VOLTAGE = "phase_b_backup_voltage"
ENTITY_PHASE_C_BACKUP_VOLTAGE = "phase_c_backup_voltage"
ENTITY_BACKUP_FREQUENCY = "backup_frequency"
ENTITY_PV_POWER_NOW = "pv_power_now"
ENTITY_PV_ENERGY_TODAY = "pv_energy_today"
ENTITY_PV_ENERGY_THIS_MONTH = "pv_energy_this_month"
ENTITY_PV_ENERGY_THIS_YEAR = "pv_energy_this_year"
ENTITY_PV_ENERGY_TOTAL = "pv_energy_total"
ENTITY_DIRECT_POWER_CONSUMPTION_NOW = "direct_power_consumption_now"
ENTITY_DIRECT_ENERGY_CONSUMPTION_TODAY = "direct_energy_consumption_today"
ENTITY_DIRECT_ENERGY_CONSUMPTION_THIS_MONTH = "direct_energy_consumption_this_month"
ENTITY_DIRECT_ENERGY_CONSUMPTION_THIS_YEAR = "direct_energy_consumption_this_year"
ENTITY_DIRECT_ENERGY_CONSUMPTION_TOTAL = "direct_energy_consumption_total"
ENTITY_EXPORT_PV_POWER_NOW = "export_pv_power_now"
ENTITY_EXPORT_PV_ENERGY_TODAY = "export_pv_energy_today"
ENTITY_EXPORT_PV_ENERGY_THIS_MONTH = "export_pv_energy_this_month"
ENTITY_EXPORT_PV_ENERGY_THIS_YEAR = "export_pv_energy_this_year"
ENTITY_EXPORT_PV_ENERGY_TOTAL = "export_pv_energy_total"
ENTITY_IMPORT_ENERGY_TODAY = "import_energy_today"
ENTITY_IMPORT_ENERGY_TOTAL = "import_energy_total"
ENTITY_EXPORT_ENERGY_TODAY = "export_energy_today"
ENTITY_EXPORT_ENERGY_TOTAL = "export_energy_total"


ENTITY_SYSTEM_STATE = "system_state"
ENTITY_LOAD_POWER = "load_power"
ENTITY_EXPORT_POWER = "export_power"
ENTITY_SELF_CONSUMPTION_TODAY = "self_consumption_today"
ENTITY_PHASE_A_CURRENT = "phase_a_current"
ENTITY_PHASE_B_CURRENT = "phase_b_current"
ENTITY_PHASE_C_CURRENT = "phase_c_current"
ENTITY_TOTAL_ACTIVE_POWER = "total_active_power"
ENTITY_DRM_STATE = "drm_state"

ENTITY_BATTERY_POWER = "battery_power"
ENTITY_BATTERY_VOLTAGE = "battery_voltage"
ENTITY_BATTERY_CURRENT = "battery_current"
ENTTIY_BDC_RATED_POWER = "bdc_rated_power"
ENTITY_MAXIMUM_CHARGE_CURRENT = "maximum_charge_current"
ENTITY_MAXIMUM_DISCHARGE_CURRENT = "maximum_discharge_current"
ENTITY_BATTERY_CAPACITY = "battery_capacity"
ENTITY_BATTERY_SOC = "battery_soc"
ENTITY_BATTERY_SOH = "battery_soh"
ENTITY_BATTERY_TEMPERATURE = "battery_temperature"
ENTTIY_CHARGE_POWER_NOW = "charge_power_now"
ENTITY_PV_CHARGE_ENERGY_TODAY = "pv_charge_energy_today"
ENTITY_PV_CHARGE_ENERGY_THIS_MONTH = "pv_charge_energy_this_month"
ENTITY_PV_CHARGE_ENERGY_THIS_YEAR = "pv_charge_energy_this_year"
ENTITY_PV_CHARGE_ENERGY_TOTAL = "pv_charge_energy_total"
ENTITY_CHARGE_ENERGY_TODAY = "charge_energy_today"
ENTITY_CHARGE_ENERGY_TOTAL = "charge_energy_total"
ENTITY_DISCHARGE_ENERGY_TODAY = "discharge_energy_today"
ENTITY_DISCHARGE_ENERGY_TOTAL = "discharge_energy_total"


ENTITIES = {
    CONF_DEVICE_TYPE_INVERTER: SungrowEntityTuple(
        SungrowSensorEntityDescription(
            key=ENTITY_PROTOCOL_NUMBER,
            register=4949,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PROTOCOL_VERSION,
            register=4951,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_ARM_SOFTWARE_VERSION,
            register=4953,
            data_type=DataType.STRING,
            data_count=32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DSP_SOFTWARE_VERSION,
            register=4968,
            data_type=DataType.STRING,
            data_count=32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_SERIAL_NUMBER,
            register=4989,
            data_type=DataType.STRING,
            data_count=20,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MODEL_NAME,
            register=4999,
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
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT,
            suggested_display_precision=1,
            register=5000,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_OUTPUT_TYPE,
            register=5001,
            data_type=DataType.UINT16,
            enum_values={
                0x0000: "Single phase",
                0x0001: "1-3P4L",
                0x0002: "2-3P3L",
            },
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_OUTPUT_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5002,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_OUTPUT_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5003,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            register=5007,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT1_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5010,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT1_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5011,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT2_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5012,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT2_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5013,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT3_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5014,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT3_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5015,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT4_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5114,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH8.0RS", "SH10RS"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MPPT4_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5115,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH8.0RS", "SH10RS"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5016,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5018,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5019,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5020,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.REACTIVE_POWER,
            native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
            suggested_display_precision=0,
            register=5032,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER_FACTOR,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=5034,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_GRID_FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.FREQUENCY,
            native_unit_of_measurement=UnitOfFrequency.HERTZ,
            suggested_display_precision=2,
            register=5241,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_A_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5602,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_B_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5604,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_METER_PHASE_C_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5606,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MINIMUM_EXPORT_POWER_LIMIT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5621,
            data_type=DataType.UINT16,
            scale=10,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MAXIMUM_EXPORT_POWER_LIMIT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5622,
            data_type=DataType.UINT16,
            scale=10,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_BACKUP_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5719,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_BACKUP_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5720,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_BACKUP_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5721,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_BACKUP_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5722,
            data_type=DataType.SINT16,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_BACKUP_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5723,
            data_type=DataType.SINT16,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_BACKUP_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5724,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_TOTAL_BACKUP_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5725,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_BACKUP_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5730,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_BACKUP_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5731,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_BACKUP_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5732,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BACKUP_FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.FREQUENCY,
            native_unit_of_measurement=UnitOfFrequency.HERTZ,
            suggested_display_precision=2,
            register=5733,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_POWER_NOW,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6099,
            data_count=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6195,
            data_count=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13001,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH?K*", "SH?.?RS", "SH10RS", "SH*T-V11"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_ENERGY_THIS_MONTH,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6226,
            data_count=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_ENERGY_THIS_YEAR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6249,
            data_count=20,
            data_type=DataType.UINT32,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13002,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_POWER_CONSUMPTION_NOW,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6289,
            register_size=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_ENERGY_CONSUMPTION_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6385,
            register_size=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_ENERGY_CONSUMPTION_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13016,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH?K*", "SH?.?RS", "SH10RS", "SH*T-V11"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_ENERGY_CONSUMPTION_THIS_MONTH,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6416,
            register_size=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_ENERGY_CONSUMPTION_THIS_YEAR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6428,
            register_size=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DIRECT_ENERGY_CONSUMPTION_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13017,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_POWER_NOW,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6468,
            register_size=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6564,
            register_size=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13004,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH?K*", "SH?.?RS", "SH10RS", "SH*T-V11"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_ENERGY_THIS_MONTH,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6595,
            register_size=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_ENERGY_THIS_YEAR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6607,
            register_size=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_PV_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13006,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_IMPORT_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13035,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_IMPORT_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13036,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13044,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13045,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_SYSTEM_STATE,
            register=12999,
            data_type=DataType.UINT16,
            enum_values={
                0x1500: "Emergency Stop",
                0x0004: "Emergency Stop",
                0x0001: "Stop",
                0x8000: "Stop",
                0x0002: "Shutdown",
                0x1300: "Shutdown",
                0x0008: "Standby",
                0x1400: "Standby",
                0x0010: "Initial Standby",
                0x1200: "Initial Standby",
                0x0020: "Startup",
                0x1600: "Startup",
                0x0000: "Running",
                0x0040: "Running",
                0x0100: "Fault",
                0x5500: "Fault",
                0x0400: "Maintain mode",
                0x0800: "Forced mode",
                0x1000: "Off-grid mode",
                0x0041: "Off-grid charge",
                0x2501: "Restarting",
                0x4000: "External EMS mode",
                0x0200: "Update failed",
                0x1111: "Uninitialized",
                0x1700: "AFCI self-test shutdown",
                0x1800: "Intelligent Station Building Status",
                0x1900: "Safe Mode",
                0x2000: "Open loop",
                0x4001: "Emergency Charging Operation",
                0x8100: "Derating Running",
                0x8200: "Dispatch Running",
                0x9100: "Warn Run",
            },
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_LOAD_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13007,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_EXPORT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13009,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_SELF_CONSUMPTION_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13028,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_A_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13030,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_B_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13031,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PHASE_C_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13032,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_TOTAL_ACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13033,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DRM_STATE,
            register=13042,
            data_type=DataType.UINT16,
            enum_values={
                0x0000: "DRM0: Normal",
                0x0001: "DRM1: Stop export",
                0x0002: "DRM2: Limited export",
                0x0003: "DRM3: No export, local only",
                0x0004: "DRM4: Limited import",
                0x0005: "DRM5: No import",
                0x0006: "DRM6: Limited import and export",
                0x0007: "DRM7: Power saving mode",
                0x0008: "DRM8: Vendor specific",
            },
        ),
    ),
    CONF_DEVICE_TYPE_BATTERY: SungrowEntityTuple(
        SungrowSensorEntityDescription(
            key=ENTTIY_BDC_RATED_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            register=5627,
            data_type=DataType.UINT16,
            scale=100,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5214,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5630,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=13019,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_CAPACITY,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.ENERGY_STORAGE,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=2,
            register=5638,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MAXIMUM_CHARGE_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            register=5634,
            data_type=DataType.UINT16,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MAXIMUM_DISCHARGE_CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            register=5635,
            data_type=DataType.UINT16,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_SOC,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13022,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_SOH,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13023,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_BATTERY_TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            register=13024,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTTIY_CHARGE_POWER_NOW,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6647,
            register_size=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_CHARGE_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6743,
            register_size=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_CHARGE_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13011,
            data_type=DataType.UINT16,
            scale=0.1,
            related_models=["SH?K*", "SH?.?RS", "SH10RS", "SH*T-V11"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_CHARGE_ENERGY_THIS_MONTH,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6774,
            register_size=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_CHARGE_ENERGY_THIS_YEAR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6786,
            register_size=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_PV_CHARGE_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13012,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_CHARGE_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13039,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_CHARGE_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13040,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DISCHARGE_ENERGY_TODAY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13025,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_DISCHARGE_ENERGY_TOTAL,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13026,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
    ),
    CONF_DEVICE_TYPE_WALLBOX: SungrowEntityTuple(
        SungrowSensorEntityDescription(
            key=ENTITY_SERIAL_NUMBER,
            register=21200,
            register_size=20,
            data_type=DataType.STRING,
        ),
        SungrowSensorEntityDescription(
            key=ENTITY_MODEL_NAME,
            register=21223,
            data_type=DataType.UINT16,
            enum_values={
                0x20ED: "AC007-00",
                0x20DA: "AC011E-01",
            },
        ),
    ),
}
