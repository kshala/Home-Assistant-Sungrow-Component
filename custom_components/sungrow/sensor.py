"""Sensor entity type for Sungrow."""

from dataclasses import dataclass
from enum import Enum
from typing import Final

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfReactivePower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_DEVICE_TYPE_BATTERY,
    CONF_DEVICE_TYPE_INVERTER,
    CONF_DEVICE_TYPE_WALLBOX,
)
from .helpers import DataType, RegisterType


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Sungrow sensors."""
    device_entity_descriptions = ENTITIES[CONF_DEVICE_TYPE_INVERTER]
    device_entities: list[SungrowSensor] = [
        SungrowSensor(description) for description in device_entity_descriptions
    ]
    async_add_entities(device_entities)


@dataclass(frozen=True, kw_only=True)
class SungrowBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Sungrow binary sensor entity."""

    icon_off: str | None = None
    icon_on: str | None = None


@dataclass(frozen=True, kw_only=True)
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
    sensors: list[SungrowBinarySensorEntityDescription] | None = None


class Entities(str, Enum):
    """Enum for all Sensor related entities."""

    # Inverter input sensors
    ProtocolNumber = "protocol_number"
    ProtocolVersion = "protocol_version"
    ArmSoftwareVersion = "arm_software_version"
    DspSoftwareVersion = "dsp_software_version"
    SerialNumber = "serial_number"
    ModelName = "model_name"
    NominalOutputPower = "nominal_output_power"
    OutputType = "output_type"
    OutputEnergyToday = "output_energy_today"
    OutputEnergyTotal = "output_energy_total"
    Temperature = "temperature"
    Mppt1Voltage = "mppt1_voltage"
    Mppt1Current = "mppt1_current"
    Mppt2Voltage = "mppt2_voltage"
    Mppt2Current = "mppt2_current"
    Mppt3Voltage = "mppt3_voltage"
    Mppt3Current = "mppt3_current"
    Mppt4Voltage = "mppt4_voltage"
    Mppt4Current = "mppt4_current"
    PvPower = "pv_power"
    PhaseAVoltage = "phase_a_voltage"
    PhaseBVoltage = "phase_b_voltage"
    PhaseCVoltage = "phase_c_voltage"
    ReactivePower = "reactive_power"
    PowerFactor = "power_factor"
    GridFrequency = "grid_frequency"
    MeterPhaseAActivePower = "meter_phase_a_active_power"
    MeterPhaseBActivePower = "meter_phase_b_active_power"
    MeterPhaseCActivePower = "meter_phase_c_active_power"
    MinimumExportPowerLimit = "minimum_export_power_limit"
    MaximumExportPowerLimit = "maximum_export_power_limit"
    PhaseABackupCurrent = "phase_a_backup_current"
    PhaseBBackupCurrent = "phase_b_backup_current"
    PhaseCBackupCurrent = "phase_c_backup_current"
    PhaseABackupPower = "phase_a_backup_power"
    PhaseBBackupPower = "phase_b_backup_power"
    PhaseCBackupPower = "phase_c_backup_power"
    TotalBackupPower = "total_backup_power"
    PhaseABackupVoltage = "phase_a_backup_voltage"
    PhaseBBackupVoltage = "phase_b_backup_voltage"
    PhaseCBackupVoltage = "phase_c_backup_voltage"
    BackupFrequency = "backup_frequency"
    PvPowerNow = "pv_power_now"
    PvEnergyToday = "pv_energy_today"
    PvEnergyThisMonth = "pv_energy_this_month"
    PvEnergyThisYear = "pv_energy_this_year"
    PvEnergyTotal = "pv_energy_total"
    DirectPowerConsumptionNow = "direct_power_consumption_now"
    DirectEnergyConsumptionToday = "direct_energy_consumption_today"
    DirectEnergyConsumptionThisMonth = "direct_energy_consumption_this_month"
    DirectEnergyConsumptionThisYear = "direct_energy_consumption_this_year"
    DirectEnergyConsumptionTotal = "direct_energy_consumption_total"
    ExportPvPowerNow = "export_pv_power_now"
    ExportPvEnergyToday = "export_pv_energy_today"
    ExportPvEnergyThisMonth = "export_pv_energy_this_month"
    ExportPvEnergyThisYear = "export_pv_energy_this_year"
    ExportPvEnergyTotal = "export_pv_energy_total"
    ImportEnergyToday = "import_energy_today"
    ImportEnergyTotal = "import_energy_total"
    ExportEnergyToday = "export_energy_today"
    ExportEnergyTotal = "export_energy_total"
    SystemState = "system_state"
    LoadPower = "load_power"
    ExportPower = "export_power"
    SelfConsumptionToday = "self_consumption_today"
    PhaseACurrent = "phase_a_current"
    PhaseBCurrent = "phase_b_current"
    PhaseCCurrent = "phase_c_current"
    TotalActivePower = "total_active_power"
    DrmState = "drm_state"

    # Inverter power flow bit array
    PowerFlowStatus = "power_flow_status"
    PvGeneratingPower = "pv_generating_power"
    BatteryCharging = "battery_charging"
    BatteryDischarging = "battery_discharging"
    PositiveLoadPower = "positive_load_power"
    ExportingPower = "exporting_power"
    ImportingPower = "importing_power"
    NegativeLoadPower = "negative_load_power"

    # Inverter realted alarms and faults
    InverterAlarm = "inverter_alarm"
    GridSideFault = "grid_side_fault"
    SystemFault1 = "system_fault_1"
    SystemFault2 = "system_fault_2"
    DcSideFault = "dc_side_fault"
    PermanentFault = "permanent_fault"

    # Inverter holding sensors
    SystemClockYear = "system_clock_year"
    SystemClockMonth = "system_clock_month"
    SystemClockDay = "system_clock_day"
    SystemClockHour = "system_clock_hour"
    SystemClockMinute = "system_clock_minute"
    SystemClockSecond = "system_clock_second"
    StartStop = "start_stop"

    # Battery input sensors
    BatteryPower = "battery_power"
    BatteryVoltage = "battery_voltage"
    BatteryCurrent = "battery_current"
    BdcRatedPower = "bdc_rated_power"
    MaximumChargeCurrent = "maximum_charge_current"
    MaximumDischargeCurrent = "maximum_discharge_current"
    BatteryCapacity = "battery_capacity"
    BatterySoc = "battery_soc"
    BatterySoh = "battery_soh"
    BatteryTemperature = "battery_temperature"
    ChargePowerNow = "charge_power_now"
    PvChargeEnergyToday = "pv_charge_energy_today"
    PvChargeEnergyThisMonth = "pv_charge_energy_this_month"
    PvChargeEnergyThisYear = "pv_charge_energy_this_year"
    PvChargeEnergyTotal = "pv_charge_energy_total"
    ChargeEnergyToday = "charge_energy_today"
    ChargeEnergyTotal = "charge_energy_total"
    DischargeEnergyToday = "discharge_energy_today"
    DischargeEnergyTotal = "discharge_energy_total"

    # Battery related alarms and faults
    BdcSideFault = "bdc_side_fault"
    BdcSidePermanentFault = "bdc_side_permanent_fault"
    BatteryFault = "battery_fault"
    BatteryAlarm = "battery_alarm"
    BmsAlarm1 = "bms_alarm_1"
    BmsAlarm2 = "bms_alarm_2"
    BmsFault1 = "bms_fault_1"
    BmsFault2 = "bms_fault_2"
    BmsProtection = "bms_protection"


ENTITIES = {
    CONF_DEVICE_TYPE_INVERTER: (
        SungrowSensorEntityDescription(
            key=Entities.ProtocolNumber,
            register=4949,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ProtocolVersion,
            register=4951,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ArmSoftwareVersion,
            register=4953,
            data_type=DataType.STRING,
            data_count=32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DspSoftwareVersion,
            register=4968,
            data_type=DataType.STRING,
            data_count=32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.SerialNumber,
            register=4989,
            data_type=DataType.STRING,
            data_count=20,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ModelName,
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
            key=Entities.NominalOutputPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT,
            suggested_display_precision=1,
            register=5000,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.OutputType,
            register=5001,
            data_type=DataType.UINT16,
            enum_values={
                0x0000: "Single phase",
                0x0001: "1-3P4L",
                0x0002: "2-3P3L",
            },
        ),
        SungrowSensorEntityDescription(
            key=Entities.OutputEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5002,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.OutputEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=5003,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Temperature,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            register=5007,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt1Voltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5010,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt1Current,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5011,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt2Voltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5012,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt2Current,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5013,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt3Voltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5014,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt3Current,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5015,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.Mppt4Voltage,
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
            key=Entities.Mppt4Current,
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
            key=Entities.PvPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5016,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseAVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5018,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseBVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5019,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseCVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5020,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ReactivePower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.REACTIVE_POWER,
            native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
            suggested_display_precision=0,
            register=5032,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PowerFactor,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER_FACTOR,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=5034,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.GridFrequency,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.FREQUENCY,
            native_unit_of_measurement=UnitOfFrequency.HERTZ,
            suggested_display_precision=2,
            register=5241,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MeterPhaseAActivePower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5602,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MeterPhaseBActivePower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5604,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MeterPhaseCActivePower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5606,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MinimumExportPowerLimit,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5621,
            data_type=DataType.UINT16,
            scale=10,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MaximumExportPowerLimit,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5622,
            data_type=DataType.UINT16,
            scale=10,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseABackupCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5719,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseBBackupCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5720,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseCBackupCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5721,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseABackupPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5722,
            data_type=DataType.SINT16,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseBBackupPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5723,
            data_type=DataType.SINT16,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseCBackupPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5724,
            data_type=DataType.UINT16,
        ),
        SungrowSensorEntityDescription(
            key=Entities.TotalBackupPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5725,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseABackupVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5730,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseBBackupVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5731,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseCBackupVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=5732,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BackupFrequency,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.FREQUENCY,
            native_unit_of_measurement=UnitOfFrequency.HERTZ,
            suggested_display_precision=2,
            register=5733,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PvPowerNow,
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
            key=Entities.PvEnergyToday,
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
            key=Entities.PvEnergyToday,
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
            key=Entities.PvEnergyThisMonth,
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
            key=Entities.PvEnergyThisYear,
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
            key=Entities.PvEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13002,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DirectPowerConsumptionNow,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6289,
            data_count=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.DirectEnergyConsumptionToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6385,
            data_count=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.DirectEnergyConsumptionToday,
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
            key=Entities.DirectEnergyConsumptionThisMonth,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6416,
            data_count=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.DirectEnergyConsumptionThisYear,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6428,
            data_count=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.DirectEnergyConsumptionTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13017,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPvPowerNow,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6468,
            data_count=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPvEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6564,
            data_count=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPvEnergyToday,
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
            key=Entities.ExportPvEnergyThisMonth,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6595,
            data_count=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPvEnergyThisYear,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6607,
            data_count=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPvEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13006,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ImportEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13035,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ImportEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13036,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13044,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13045,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.SystemState,
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
            key=Entities.LoadPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13007,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ExportPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13009,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.SelfConsumptionToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13028,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseACurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13030,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseBCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13031,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PhaseCCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=13032,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.TotalActivePower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=13033,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DrmState,
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
        SungrowSensorEntityDescription(
            key=Entities.InverterAlarm,
            register=13049,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.GridSideFault,
            register=13051,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.SystemFault1,
            register=13053,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.SystemFault2,
            register=13055,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DcSideFault,
            register=13057,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PermanentFault,
            register=13059,
            data_type=DataType.UINT32,
        ),
    ),
    CONF_DEVICE_TYPE_BATTERY: (
        SungrowSensorEntityDescription(
            key=Entities.BdcRatedPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            register=5627,
            data_type=DataType.UINT16,
            scale=100,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryPower,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=5214,
            data_type=DataType.SINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            suggested_display_precision=1,
            register=5630,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryVoltage,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=1,
            register=13019,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryCapacity,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.ENERGY_STORAGE,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=2,
            register=5638,
            data_type=DataType.UINT16,
            scale=0.01,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MaximumChargeCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            register=5634,
            data_type=DataType.UINT16,
        ),
        SungrowSensorEntityDescription(
            key=Entities.MaximumDischargeCurrent,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.CURRENT,
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            register=5635,
            data_type=DataType.UINT16,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatterySoc,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13022,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatterySoh,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            suggested_display_precision=1,
            register=13023,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryTemperature,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            register=13024,
            data_type=DataType.SINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ChargePowerNow,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.WATT,
            suggested_display_precision=0,
            register=6647,
            data_count=96,
            data_type=DataType.UINT16,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.PvChargeEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6743,
            data_count=31,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.PvChargeEnergyToday,
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
            key=Entities.PvChargeEnergyThisMonth,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6774,
            data_count=12,
            data_type=DataType.UINT16,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.PvChargeEnergyThisYear,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=6786,
            data_count=20,
            data_type=DataType.UINT32,
            scale=0.1,
            entity_class="SungrowAttributedDataSensor",
            related_models=["SH?.0RT*", "SH10RT*"],
        ),
        SungrowSensorEntityDescription(
            key=Entities.PvChargeEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13012,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ChargeEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13039,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ChargeEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13040,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DischargeEnergyToday,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13025,
            data_type=DataType.UINT16,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.DischargeEnergyTotal,
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=1,
            register=13026,
            data_type=DataType.UINT32,
            scale=0.1,
        ),
        SungrowSensorEntityDescription(
            key=Entities.PowerFlowStatus,
            register=13000,
            data_type=DataType.UINT16,
            sensors=[
                SungrowBinarySensorEntityDescription(
                    key=Entities.PvGeneratingPower,
                    icon_on="mdi:solar-power",
                    icon_off="mdi:weather-night-partly-cloudy",
                ),
                SungrowBinarySensorEntityDescription(
                    key=Entities.BatteryCharging,
                    icon_on="mdi:battery-plus",
                    icon_off="mdi:battery",
                ),
                SungrowBinarySensorEntityDescription(
                    key=Entities.BatteryDischarging,
                    icon_on="mdi:battery-minus",
                    icon_off="mdi:battery",
                ),
                SungrowBinarySensorEntityDescription(
                    key=Entities.PositiveLoadPower,
                    icon_on="mdi:transmission-tower",
                    icon_off="mdi:transmission-tower-off",
                ),
                SungrowBinarySensorEntityDescription(
                    key=Entities.ExportingPower,
                    icon_on="mdi:transmission-tower",
                    icon_off="mdi:transmission-tower-off",
                ),
                SungrowBinarySensorEntityDescription(
                    key=Entities.ImportingPower,
                    icon_on="mdi:transmission-tower",
                    icon_off="mdi:transmission-tower-off",
                ),
                None,  # Placeholder for bit 6. Reserved as specified by the protocol.
                SungrowBinarySensorEntityDescription(
                    key=Entities.NegativeLoadPower,
                    icon_on="mdi:transmission-tower",
                    icon_off="mdi:transmission-tower-off",
                ),
            ],
        ),
        SungrowSensorEntityDescription(
            key=Entities.BdcSideFault,
            register=13061,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BdcSidePermanentFault,
            register=13063,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryFault,
            register=13065,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BatteryAlarm,
            register=13067,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BmsAlarm1,
            register=13069,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BmsAlarm2,
            register=13077,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BmsFault1,
            register=13073,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BmsFault2,
            register=13075,
            data_type=DataType.UINT32,
        ),
        SungrowSensorEntityDescription(
            key=Entities.BmsProtection,
            register=13071,
            data_type=DataType.UINT32,
        ),
    ),
    CONF_DEVICE_TYPE_WALLBOX: (
        SungrowSensorEntityDescription(
            key=Entities.SerialNumber,
            register=21200,
            data_count=20,
            data_type=DataType.STRING,
        ),
        SungrowSensorEntityDescription(
            key=Entities.ModelName,
            register=21223,
            data_type=DataType.UINT16,
            enum_values={
                0x20ED: "AC007-00",
                0x20DA: "AC011E-01",
            },
        ),
    ),
}


class SungrowSensor(SensorEntity):
    """Representation of a Modbus sensor."""

    def __init__(self, description: SungrowSensorEntityDescription) -> None:
        """Initialize the sensor."""
        self._description = description

    async def async_update(self):
        """Fetch new state data from Modbus."""
        # if self._register_type == "holding":
        #    value = await self._device.read_holding_register(self._register_address)
        # elif self._register_type == "input":
        #    value = await self._device.read_input_register(self._register_address)
        # else:
        #    value = None#

        # if value is not None:
        #    self._state = value[0]  # Lies das erste Register aus
