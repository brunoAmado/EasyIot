# MQTT Client & HA Discovery

> 26 nodes

## Key Concepts

- **Sensor** (30 connections) — `include/Sensors.h`
- **String** (3 connections)
- **.familyToText()** (2 connections) — `include/Sensors.h`
- **.driverToText()** (2 connections) — `include/Sensors.h`
- **uniqueId** (1 connections) — `include/Sensors.h`
- **name** (1 connections) — `include/Sensors.h`
- **hwAddress** (1 connections) — `include/Sensors.h`
- **SensorDriver** (1 connections)
- **driver** (1 connections) — `include/Sensors.h`
- **state** (1 connections) — `include/Sensors.h`
- **readTopic** (1 connections) — `include/Sensors.h`
- **cloudIOreadTopic** (1 connections) — `include/Sensors.h`
- **vector** (1 connections)
- **inputs** (1 connections) — `include/Sensors.h`
- **lastBinaryState** (1 connections) — `include/Sensors.h`
- **delayRead** (1 connections) — `include/Sensors.h`
- **lastRead** (1 connections) — `include/Sensors.h`
- **initialized** (1 connections) — `include/Sensors.h`
- **error** (1 connections) — `include/Sensors.h`
- **errorCounter** (1 connections) — `include/Sensors.h`
- **lastErrorTimestamp** (1 connections) — `include/Sensors.h`
- **id** (1 connections) — `include/Sensors.h`
- **.reInit()** (1 connections) — `include/Sensors.h`
- **.clearError()** (1 connections) — `include/Sensors.h`
- **loop** (1 connections) — `include/Sensors.h`
- *... and 1 more nodes in this community*

## Relationships

- [Captive Portal Header](Captive_Portal_Header.md) (2 shared connections)
- [Device Components & Core Headers](Device_Components_&_Core_Headers.md) (1 shared connections)
- [Shutter Calibration & Math](Shutter_Calibration_&_Math.md) (1 shared connections)
- [Hardware Access & Sensor Drivers](Hardware_Access_&_Sensor_Drivers.md) (1 shared connections)

## Source Files

- `include/Sensors.h`

## Audit Trail

- EXTRACTED: 59 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*