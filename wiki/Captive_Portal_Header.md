# Captive Portal Header

> 9 nodes

## Key Concepts

- **Sensor::loop()** (13 connections) — `src/Sensors.cpp`
- **begin** (2 connections) — `include/ModbusMaster.h`
- **getResponseBuffer** (2 connections) — `include/ModbusMaster.h`
- **clearResponseBuffer** (2 connections) — `include/ModbusMaster.h`
- **available** (2 connections) — `include/ModbusMaster.h`
- **readInputRegisters** (2 connections) — `include/ModbusMaster.h`
- **readLastProfile** (2 connections) — `include/ModbusMaster.h`
- **.isInitialized()** (2 connections) — `include/Sensors.h`
- **.setError()** (2 connections) — `include/Sensors.h`

## Relationships

- [System Lifecycle & Network Provisioning](System_Lifecycle_&_Network_Provisioning.md) (6 shared connections)
- [MQTT Client & HA Discovery](MQTT_Client_&_HA_Discovery.md) (2 shared connections)
- [Shutter Calibration & Math](Shutter_Calibration_&_Math.md) (2 shared connections)
- [Utility Binary Operations](Utility_Binary_Operations.md) (2 shared connections)
- [Hardware Access & Sensor Drivers](Hardware_Access_&_Sensor_Drivers.md) (1 shared connections)

## Source Files

- `include/ModbusMaster.h`
- `include/Sensors.h`
- `src/Sensors.cpp`

## Audit Trail

- EXTRACTED: 10 (34%)
- INFERRED: 19 (66%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*