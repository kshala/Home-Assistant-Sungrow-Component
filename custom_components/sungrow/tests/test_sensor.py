def test_modbus_sensor_state():
    sensor = ModbusSensor("Test Sensor", "hub1", 1, "°C")
    assert sensor.name == "Test Sensor"
